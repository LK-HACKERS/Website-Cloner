import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin, urlparse

# Colors for a hacker look
RED = '\033[31m'
GREEN = '\033[32m'
BLUE = '\033[34m'
YELLOW = '\033[33m'
NC = '\033[0m'

def banner():
    print(f"{BLUE}")
    print(r"   ██╗    ██╗███████╗██████╗ ███████╗██╗████████╗███████╗     ██████╗██╗      ██████╗ ███╗   ██╗███████╗██████╗")
    print(r"   ██║    ██║██╔════╝██╔══██╗██╔════╝██║╚══██╔══╝██╔════╝    ██╔════╝██║     ██╔═══██╗████╗  ██║██╔════╝██╔══██╗")
    print(r"   ██║ █╗ ██║█████╗  ██████╔╝███████╗██║   ██║   █████╗      ██║     ██║     ██║   ██║██╔██╗ ██║█████╗  ██████╔╝")
    print(r"   ██║███╗██║██╔══╝  ██╔══██╗╚════██║██║   ██║   ██╔══╝      ██║     ██║     ██║   ██║██║╚██╗██║██╔══╝  ██╔══██╗")
    print(r"   ╚███╔███╔╝███████╗██████╔╝███████║██║   ██║   ███████╗    ╚██████╗███████╗╚██████╔╝██║ ╚████║███████╗██║  ██║")
    print(r"    ╚══╝╚══╝ ╚══════╝╚═════╝ ╚══════╝╚═╝   ╚═╝   ╚══════╝     ╚═════╝╚══════╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝")
    print(f"{RED}          --- CYBER BLACK LION Website Cloner ---{NC}")
    print(f"{YELLOW}-------------------------------------------------------------------{NC}")

def clone_site():
    banner()
    target_url = input(f"{GREEN}[+] Enter the URL to clone (e.g., https://google.com): {NC}")

    if not target_url.startswith('http'):
        print(f"{RED}[!] Please include http:// or https://{NC}")
        return

    # Create a folder based on the domain name
    domain = urlparse(target_url).netloc
    folder_name = domain.replace('.', '_')
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    print(f"{BLUE}[*] Cloning {target_url}... Please wait...{NC}")

    try:
        # Get the HTML content
        response = requests.get(target_url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Save the main HTML file
        with open(f"{folder_name}/index.html", "w", encoding="utf-8") as f:
            f.write(soup.prettify())

        # Find and download assets (CSS, JS, Images)
        tags = {'img': 'src', 'link': 'href', 'script': 'src'}

        for tag, attr in tags.items():
            for element in soup.find_all(tag):
                asset_url = element.get(attr)
                if asset_url:
                    # Make the URL absolute
                    full_url = urljoin(target_url, asset_url)
                    asset_name = os.path.basename(urlparse(full_url).path)

                    if asset_name:
                        try:
                            # Create subfolders for assets
                            asset_folder = f"{folder_name}/{tag}"
                            if not os.path.exists(asset_folder):
                                os.makedirs(asset_folder)

                            # Download the asset
                            asset_data = requests.get(full_url, timeout=5).content
                            with open(f"{asset_folder}/{asset_name}", "wb") as f:
                                f.write(asset_data)

                            # Update the HTML to point to the local asset
                            element[attr] = f"{tag}/{asset_name}"
                        except:
                            continue

        print(f"{GREEN}\n[+] Success! Website cloned into folder: {folder_name}{NC}")
        print(f"{YELLOW}[!] Now you can edit index.html to capture data!{NC}")

    except Exception as e:
        print(f"{RED}[!] Error: {str(e)}{NC}")

if __name__ == "__main__":
    clone_site()
