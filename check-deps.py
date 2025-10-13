#!/usr/bin/env python3
import requests
import json
import sys
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor
import threading

def get_github_files(repo_url, token=None):
    parsed = urlparse(repo_url)
    path_parts = parsed.path.strip('/').split('/')
    headers = {'Authorization': f'token {token}'} if token else {}
    
    if len(path_parts) == 1:
        org = path_parts[0]
        repos_url = f"https://api.github.com/orgs/{org}/repos"
        response = requests.get(repos_url, headers=headers)
        if response.status_code != 200:
            return []
        repo_names = [r['full_name'] for r in response.json()]
    else:
        repo_names = ['/'.join(path_parts[:2])]
    
    package_files = []
    for repo_name in repo_names:
        search_url = f"https://api.github.com/search/code?q=filename:package.json+repo:{repo_name}"
        result = requests.get(search_url, headers=headers)
        if result.status_code != 200:
            continue
            
        for item in result.json().get('items', []):
            try:
                content = requests.get(item['url'], headers=headers).json()
                package_content = requests.get(content['download_url']).text
                package_files.append({
                    'repo': repo_name,
                    'path': item['path'],
                    'content': json.loads(package_content)
                })
            except:
                continue
    
    return package_files

def check_dependency_exists(dep_name):
    url = f"https://registry.npmjs.org/{dep_name}"
    try:
        return requests.get(url, timeout=5).status_code == 200
    except:
        return False

def check_package_deps(pkg, missing_deps, lock):
    deps = {**pkg['content'].get('dependencies', {}), 
            **pkg['content'].get('devDependencies', {})}
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(check_dependency_exists, dep): dep for dep in deps}
        
        for future in futures:
            dep_name = futures[future]
            if not future.result():
                with lock:
                    missing_deps.append({
                        'repo': pkg['repo'],
                        'path': pkg['path'],
                        'dependency': dep_name
                    })

def main():
    if len(sys.argv) < 2:
        print("Usage: python check-deps.py <github_url> [token]")
        sys.exit(1)
    
    repo_url = sys.argv[1]
    token = sys.argv[2] if len(sys.argv) > 2 else None
    
    packages = get_github_files(repo_url, token)
    if not packages:
        return
    
    missing_deps = []
    lock = threading.Lock()
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(check_package_deps, pkg, missing_deps, lock) for pkg in packages]
        for future in futures:
            future.result()
    
    for item in missing_deps:
        print(f"{item['repo']}/{item['path']}: {item['dependency']}")

if __name__ == "__main__":
    main()
