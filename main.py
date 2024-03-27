from datetime import datetime
import requests
import os

ENDPOINT_WEBSITES_BLOCKED = "https://api.anablock.net.br/api/domain/all"
FILE_DOMAINS_BLOCKED = "Websites_for_block"
FILE_VERSION = "version"

new_sites = []

# Function for get domains blocked
def get_domains(endpoint):
    try:
        response = requests.get(endpoint)
        if response.status_code == 200:
            return response.text.splitlines()
        else:
            return []
    except Exception as e:
        print(f"Error for get domains: {e}")
        return []

# Function for load domains from file
def load_domains_from_file(file_name):
    try:
        if not os.path.exists(file_name):
            return []
        
        with open(file_name, 'r') as file:
            return [line.strip() for line in file.readlines()]
    except Exception as e:
        print(f"Error for load domains from file: {e}")
        return []

# Function for save domains to file
def save_domains_to_file(file_name, domains):
    try:
        with open(file_name, 'w') as file:
            for domain in domains:
                file.write(domain + '\n')
    except Exception as e:
        print(f"Error for save domains to file: {e}")

# Function for load version from file
def load_version_from_file(file_name):
    try:
        with open(file_name, 'r') as file:
            version = file.readline().strip()
            return version
    except Exception as e:
        print(f"Error for load version from file: {e}")
        return None

# Function for save new version to file
def save_new_version(file_name, new_version):
    try:
        with open(file_name, 'w') as file:
            file.write(new_version)
    except Exception as e:
        print(f"Error for save new version to file: {e}")

# Function for generate new version
def generate_new_version(old_version):
    date_now = datetime.now().strftime("%Y%m%d")

    if old_version[:8] == date_now:
        new_version = int(old_version[8:]) + 1
        new_version = str(new_version).zfill(2)
    else:
        new_version = "01"
    return f"{date_now}{new_version}"

# Function main
def main():
    domains = get_domains(ENDPOINT_WEBSITES_BLOCKED)
    print(f"Total domains returned: {len(domains)}")

    domains_file = load_domains_from_file(FILE_DOMAINS_BLOCKED)
    print(f"Total domains in file: {len(domains_file)}")

    new_sites = [domain for domain in domains if domain not in domains_file]

    if new_sites:
        print(f"Total new sites: {len(new_sites)}")
        domains_file.extend(new_sites)
        save_domains_to_file(FILE_DOMAINS_BLOCKED, domains_file)
        
        version = load_version_from_file(FILE_VERSION)
        print(f"Old version: {version}")

        new_version = generate_new_version(version)
        print(f"New version: {new_version}")

        save_new_version(FILE_VERSION, new_version)
    else:
        print("Not found new sites.")

# Execute the main function
if __name__ == "__main__":
    print("Starting the program for checking and adding new sites...")
    main()
    print("End of program.")
