import json
import argparse
import requests
import concurrent.futures
from colorama import Fore,Style
print(Fore.YELLOW)
print("""  __                                                   
|/  |                        |                         
|   | ___  ___  ___  ___  ___| ___  ___  ___  ___  ___ 
|   )|___)|   )|___)|   )|   )|   )|   )|    |___)|   )
|__/ |__  |__/ |__  |  / |__/ |__/||  / |__  |__  |    
          |                        By:- @https://x.com/gurudattch                                          
""")
print(Style.RESET_ALL)
def extract_dependency_names(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)

        # Extracting dependencies and devDependencies
        dependencies = data.get('dependencies', {})
        dev_dependencies = data.get('devDependencies', {})

        # Combining all dependencies
        all_dependencies = list(dependencies.keys()) + list(dev_dependencies.keys())

        return all_dependencies

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return []
    except json.JSONDecodeError:
        print(f"Error: The file '{file_path}' is not a valid JSON file.")
        return []

def fetch_dependency_status(dependency_name):
    try:
        response = requests.get(url=f"http://registry.npmjs.org/{dependency_name}")
        return dependency_name, response.status_code
    except requests.RequestException as e:
        return dependency_name, str(e)

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Extract dependency names from a package.json file.')
    parser.add_argument('-f', '--file', required=True, help='Path to the package.json file')

    args = parser.parse_args()

    # Extract dependencies
    dependency_names = extract_dependency_names(args.file)

    # Use a ThreadPoolExecutor to fetch dependency statuses concurrently
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Map the function to the dependency names
        results = executor.map(fetch_dependency_status, dependency_names)

    # Print the results
    print("Dependencies:")
    for name, status in results:
        if status == 404:
            print(Fore.RED)
            print(f"{name} ==> {status}")
            print(Style.RESET_ALL)
        else:
             print(f"{name} ==> {status}")

if __name__ == '__main__':
    main()
