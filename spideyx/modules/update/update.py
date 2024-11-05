import requests
from colorama import Fore, Style
import subprocess
import os
from rich.console import Console
from rich.markdown import Markdown
console = Console()
bold =Style.BRIGHT
blue = Fore.BLUE
red  = Fore.RED
white = Fore.WHITE
reset = Style.RESET_ALL

def zip_url(username):
    try:
        url = "https://api.github.com/repos/RevoltSecurities/SpideyX/releases/latest"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json()['zipball_url']
        else:
            print(f"[{bold}{red}WRN{reset}]: {bold}{white}Hey {username} Update Failed for SpideyX, Please try to update it manually{reset}")
            quit()
    except Exception as e:
        pass
        
def latest_update(url, username, path):
    try:
        response = requests.get(url, timeout=20, stream=True)
        filepath = f"{path}/spideyX.zip"
        if response.status_code == 200:
            print(f"[{bold}{blue}INFO{reset}]: {bold}{white}Hey {username}, Updating SpideyX please wait..{reset}")
            with open(f"{filepath}", "wb") as streamw:
                for data in response.iter_content():
                    if data:
                        streamw.write(data)
            try:
                subprocess.run(["pip", "install", f"{filepath}"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                os.remove(filepath)
            except Exception as e:
                print(f"[{bold}{red}WRN{reset}]: {bold}{white}Hey {username} Update Failed for SpideyX, Please try to update it manually{reset}")
                os.remove(filepath)
                quit() 
        else:
            print(f"[{bold}{red}WRN{reset}]: {bold}{white}Hey {username} Update Failed for SpideyX, Please try to update it manually{reset}")
            quit()
            
    except Exception as e:
        pass


def updatelog():
    try:
        url = f"https://raw.githubusercontent.com/RevoltSecurities/SpideyX/main/spideyx/updatelog.md"
        response = requests.get(url, timeout=20, stream=True)
        if response.status_code == 200:
            loader = response.text
            console.print(Markdown(loader))
        else:
            print(f"[{bold}{red}ALERT{reset}]: {bold}{white}Hey  unable to fetch update logs so please visit here --> https://github.com/RevoltSecurities/SpideyX{reset}")
            quit()
    except Exception as e:
        print(f"[{bold}{red}ALERT{reset}]: {bold}{white}Hey  unable to fetch update logs so please visit here --> https://github.com/RevoltSecurities/SpideyX{reset}")
        quit()

def check_for_updates():
    try:
        url = "https://api.github.com/repos/RevoltSecurities/SpideyX/releases/latest"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            latest_version = response.json()['tag_name']
            return latest_version
        else:
            print(f"[{bold}{red}WRN{reset}]: {bold}{white}Unable to check for updates. Please try again later.{reset}")
            return None
    except Exception as e:
        print(f"[{bold}{red}WRN{reset}]: {bold}{white}Exception occurred while checking for updates: {e}{reset}")
        return None

def notify_user_of_update(current_version, latest_version):
    if current_version != latest_version:
        print(f"[{bold}{blue}INFO{reset}]: {bold}{white}A new version of SpideyX is available! Current version: {current_version}, Latest version: {latest_version}{reset}")
        print(f"[{bold}{blue}INFO{reset}]: {bold}{white}Please update SpideyX to the latest version for new features and improvements.{reset}")
    else:
        print(f"[{bold}{blue}INFO{reset}]: {bold}{white}You are using the latest version of SpideyX.{reset}")

def auto_update():
    current_version = "v1.0.0"
    latest_version = check_for_updates()
    if latest_version:
        notify_user_of_update(current_version, latest_version)
        if current_version != latest_version:
            url = zip_url("User")
            if url:
                latest_update(url, "User", "/tmp")
                print(f"[{bold}{blue}INFO{reset}]: {bold}{white}SpideyX has been updated to the latest version!{reset}")
            else:
                print(f"[{bold}{red}WRN{reset}]: {bold}{white}Failed to get the update URL. Please update manually.{reset}")
