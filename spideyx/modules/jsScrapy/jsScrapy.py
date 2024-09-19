import asyncio
import httpx
import aiofiles
import os  
from colorama import Fore,Style
import random
from bs4 import BeautifulSoup, XMLParsedAsHTMLWarning, MarkupResemblesLocatorWarning
import warnings
from fake_useragent import UserAgent
from urllib.parse import urljoin, urlparse, urlsplit
import re
import urllib
from alive_progress import alive_bar
import tldextract
red =  Fore.RED
green = Fore.GREEN
magenta = Fore.MAGENTA
cyan = Fore.CYAN
mixed = Fore.RED + Fore.BLUE
blue = Fore.BLUE
yellow = Fore.YELLOW
white = Fore.WHITE
lm = Fore.LIGHTMAGENTA_EX
reset = Style.RESET_ALL
bold = Style.BRIGHT
colors = [ white, cyan, blue]
random_color = random.choice(colors)

class JsScrapy:
    def __init__(
        self,
        regex_configurations,
        sites: list[str], 
        concurrency: int,
        proxy: str,
        disable_redirect: bool,
        verbose: bool,
        timeout: int,
        output: str,
        headers
        ) -> None:
        self.re_configs = regex_configurations
        self.urls = sites
        self.concurrency = concurrency
        self.Semaphore = asyncio.Semaphore(self.concurrency)
        self.output = output
        self.proxy = proxy
        self.timeout=timeout
        self.dis_redir = disable_redirect
        self.verbose = verbose
        self.Headers = dict(headers)
        
    async def save(self, result: str, output: str) -> None:
        try:
            if output:
                if os.path.isdir(output):
                    filename = os.path.join(output, "spideyX_results.txt")
                else:
                    filename = output
            async with aiofiles.open(output, "a") as streamw:
                await streamw.write(result + '\n')
        except KeyboardInterrupt :
            exit()
        except asyncio.CancelledError:
            exit()
        except Exception as e:
            pass
            
    async def compiler(self, domain):
        try:
            compiled_patterns = {}
            for entry in self.re_configs.get('JsRegex', []):
                if 'type' in entry and 'regex' in entry:
                    pattern_type = entry['type']
                    patterns = entry['regex']
                    compiled_patterns[pattern_type] = []
                    for p in patterns:
                        if pattern_type == "subdomain":
                            p = p.strip('"').strip("'")+domain
                        else:
                            p = p.strip('"').strip("'")
                        try:
                            compiled_pattern = re.compile(p)
                            compiled_patterns[pattern_type].append(compiled_pattern)
                        except KeyboardInterrupt as e:
                            exit()
                        except asyncio.CancelledError as e:
                            exit()
                        except re.error as e:
                            print(f"[{bold}{red}WRN{red}]: {bold}{white}Compilation error for patter '{p}' due to: {e}, please check your pattern{reset}")
                        except Exception as e:
                            pass
            return compiled_patterns
        except KeyboardInterrupt:
            print(f"[{bold}{blue}INFO{reset}]: {bold}{white}\nCtrl+C Pressed{reset}")
            exit()
        except asyncio.CancelledError:
            exit()
        except Exception as e:
            if self.verbose:
                print(f"Exception at  JSscraper compiler: {e}, {type(e)}")
                
    async def request(self, session: httpx.AsyncClient, url: str):
        try:
            self.Headers["User-Agent"] = UserAgent().random 
            response = await session.request("GET", url, headers=self.Headers)
            await asyncio.sleep(0.1)
            return response.text
        except KeyboardInterrupt as e:
            exit()
        except asyncio.CancelledError as e:
            exit()
        except httpx.RemoteProtocolError:
            pass
        except httpx.ConnectError as e:
            print(f"[{bold}{red}WRN{reset}]: {bold}{white}Unable to connect {url} , may be server unreachable or check your internet connection{reset}")
        except httpx.ReadTimeout:
            pass
        except Exception as e: 
            if self.verbose:
                print(f"Exception at JSscraper request: {e}, {type(e)}")
    
    async def matcher(self, responsed, compiled):
        try:
            await asyncio.sleep(0.1)
            results = set()
            for pattern_type, patterns in compiled.items():
                for pattern in patterns:
                    matches = pattern.findall(responsed)
                    for match in matches:
                        results.add(f"{pattern_type},{match}")
            return sorted(results)
        except KeyboardInterrupt as e:
            exit()
        except asyncio.CancelledError as e:
            exit()
        except Exception as e:
            if self.verbose:
                print(f"Exception at JSscraper matcher: {e}, {type(e)}")
    
    async def core(self, url, bar, compiled, session: httpx.AsyncClient):
        try:
            responsed = await self.request(session, url)
            await asyncio.sleep(0.1)
            if responsed is None:
                return
            results = await self.matcher(responsed, compiled)
            await asyncio.sleep(0.1)
            if results:
                for result in results:
                    typer,data = result.split(",", 1)
                    print(f"[{bold}{white}{url}{reset}] [{bold}{green}{typer}{reset}]: {bold}{white}{data}{reset}")
                    if self.output:
                        await self.save(f"{url} ==> {data} [{typer}]", self.output)
        except KeyboardInterrupt as e:
            exit()
        except asyncio.CancelledError as e:
            exit()
        except Exception as e:
            if self.verbose:
                print(f"Exception at JSscraper core: {e}, {type(e)}")
        finally:
            self.Semaphore.release()
            bar()
            
    async def start(self):
        try:
            batch = 50000
            redirect = False if  self.dis_redir else True
            async with httpx.AsyncClient(verify=False, proxy=self.proxy, follow_redirects=redirect, timeout=httpx.Timeout(read=60.0, connect=self.timeout, write=None, pool=None)) as session:
                with alive_bar(title=f"SpideyX", total=len(self.urls), enrich_print=False) as bar:
                    for i in range(0, len(self.urls), batch):
                        batch_urls = self.urls[i:i + batch]
                        tasks =[]
                        for url in batch_urls:
                            extracted = tldextract.extract(url)
                            domain = f"{extracted.domain}.{extracted.suffix}"
                            compiled = await self.compiler(domain)
                            await self.Semaphore.acquire()
                            task = asyncio.ensure_future(self.core(url, bar, compiled, session))
                            tasks.append(task)
                        await asyncio.gather(*tasks)
        except KeyboardInterrupt as e:
            exit()
        except asyncio.CancelledError as e:
            exit()
        except Exception as e:
            if self.verbose:
                print(f"Exception at JSscraper start: {e}, {type(e)}")