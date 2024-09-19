from genericpath import isfile
import aiofiles
from colorama import Fore,Style
import os
import yaml
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
class Extractor:
    @staticmethod
    def blacklist(ctx, param,values:str) -> list[str]:
        try:
            if values is None:
                extensions = [".3g2", ".3gp", ".7z", ".apk", ".arj", ".avi", ".axd", ".bmp", ".csv", ".deb", ".dll", ".doc", ".drv", ".eot", ".exe", ".flv", ".gif", ".gifv", ".gz", ".h264", ".ico", ".iso", ".jar", ".jpeg", ".jpg", ".lock", ".m4a", ".m4v", ".map", ".mkv", ".mov", ".mp3", ".mp4", ".mpeg", ".mpg", ".msi", ".ogg", ".ogm", ".ogv", ".otf", ".pdf", ".pkg", ".png", ".ppt", ".psd", ".rar", ".rm", ".rpm", ".svg", ".swf", ".sys", ".tar.gz", ".tar", ".tif", ".tiff", ".ttf", ".txt", ".vob", ".wav", ".webm", ".webp", ".wmv", ".woff", ".woff2", ".xcf", ".xls", ".xlsx", ".zip"]
                return extensions
            
            ext = []
            extensions = values.split(",")
            for extension in extensions:
                ext.append(str(f"{extension}"))
            return ext
        except Exception as e:
            print(f"[{bold}{blue}INFO{reset}]: {bold}{white}Unknow Exception occured int Extracter extract due to: {e}, {type(e)}{reset}")
    
    @staticmethod
    def extract(ctx,param,values:str) -> list[str]:
        if values is None:
            return 
        ext = []
        extensions = values.split(",")
        for extension in extensions:
            ext.append(str(f"{extension}"))
        return ext
    
    @staticmethod
    async def ScopeReader(scope) -> list:
        try:
            if scope is None:
                return 
            if os.path.isfile(scope):
                async with aiofiles.open(scope, "r") as streamr:
                    data = await streamr.read()
                    return [line.strip() for line in data.splitlines() if line.strip()]
            else:
                return [s.strip() for s in scope.split(',') if s.strip()]            
        except FileNotFoundError:
            print(f"[{bold}{red}WRN{reset}]: {bold}{white}{scope} no such file or directory exists{reset}")
            exit()
        except Exception as e:
            print(f"[{bold}{blue}INFO{reset}]: {bold}{white}Unknow Exception occured in Extractor scope reader due to: {e}, {type(e)}{reset}")       
    
    @staticmethod
    def tagshandler(ctx, param, values:str) -> dict:
        try:
            tags ={}
            if values is None:
                return {'a': 'href','link': 'href','script': 'src','iframe': 'src','object': 'data','embed': 'src','area': 'href', 'img': 'src', 'form': 'action', 'source': 'src', 
                    'base':'href', 'frame':'src', 'video':'src', 'input':'src'}

            values = values.split(",")
            for keys in values:
                header,value = keys.split(":", 1)
                tags[header.strip()] = value.strip()
            return tags
        except Exception as e:
            print(f"[{bold}{blue}INFO{reset}]: {bold}{white}Unknow Exception occured in scope reader due to: {e}, {type(e)}{reset}")
        
    @staticmethod
    async def Reader(filename:str):
        try:
            async with aiofiles.open(filename, "r") as streamr:
                data = await streamr.read()
            return [line.strip() for line in data.splitlines() if line.strip()]
        except FileNotFoundError:
            print(f"[{bold}{red}WRN{reset}]: {bold}{white}{filename} no such file or directory exists{reset}")
            exit()
        except Exception as e:
            print(f"[{bold}{blue}INFO{reset}]: {bold}{white}Unknow Exception occured in Extractor File reader due to: {e}, {type(e)}{reset}")
            
    @staticmethod
    async def Yamlreader(filename: str):
        try:
            async with aiofiles.open(filename, "r") as streamr:
                data = await streamr.read()
            return yaml.safe_load(data)
        except FileNotFoundError:
            print(f"[{bold}{red}WRN{reset}]: {bold}{white}{filename} no such file or directory exists{reset}")
            exit()
        except Exception as e:
            print(f"[{bold}{blue}INFO{reset}]: {bold}{white}Unknow Exception occured in Extractor yaml reader due to: {e}, {type(e)}{reset}")