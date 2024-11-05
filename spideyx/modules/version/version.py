#!/usr/bin/env python3
import random 
import os  
from colorama import Fore,Style
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
requests.packages.urllib3.disable_warnings()

red =  Fore.RED
green = Fore.GREEN
magenta = Fore.MAGENTA
cyan = Fore.CYAN
mixed = Fore.RED + Fore.BLUE
blue = Fore.BLUE
yellow = Fore.YELLOW
white = Fore.WHITE
reset = Style.RESET_ALL
bold = Style.BRIGHT
colors = [ green, cyan, blue]
random_color = random.choice(colors)

def Version():
    url = f"https://api.github.com/repos/Revoltsecurities/SpideyX/releases/latest"
    try:
        response = requests.get(url, verify=True, timeout=10)
        if response.status_code == 200:
            data = response.json()
            latest = data.get('tag_name')
            return latest
    except KeyboardInterrupt as e:
        quit()
    except Exception as e:
        pass

def get_version_info():
    url = f"https://api.github.com/repos/Revoltsecurities/SpideyX/releases/latest"
    try:
        response = requests.get(url, verify=True, timeout=10)
        if response.status_code == 200:
            data = response.json()
            version_info = {
                "tag_name": data.get('tag_name'),
                "name": data.get('name'),
                "body": data.get('body'),
                "published_at": data.get('published_at')
            }
            return version_info
    except KeyboardInterrupt as e:
        quit()
    except Exception as e:
        pass

def print_version_info():
    version_info = get_version_info()
    if version_info:
        print(f"Version: {version_info['tag_name']}")
        print(f"Name: {version_info['name']}")
        print(f"Description: {version_info['body']}")
        print(f"Published at: {version_info['published_at']}")
    else:
        print("Unable to fetch version information.")
