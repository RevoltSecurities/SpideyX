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
from yarl import URL
import re
import json
from datetime import datetime
import urllib
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

class ActiveAsyncSpidey:
    
    def __init__(
        self, 
        site: str, 
        domain: str,
        dept: int, 
        method: str, 
        headers, 
        random_agent: bool, 
        timeout: int,  
        proxy: str, 
        allow_redirect: bool, 
        max_redirect: int, 
        blacklist: list[str],  
        whitelist: list[str], 
        http2: bool, 
        host_include: list[str], 
        host_exclude: list[str],  
        concurrency: int, 
        output: str, 
        silent: bool, 
        verbose: bool,
        crawl_scope: list[str], 
        crawl_out_scope: list[str], 
        match_regex: list[str], 
        filter_regex: list[str],
        delay: float,
        tags: dict) -> None:
        self.site = site
        self.domain = domain
        self.max_dept = dept if dept != 0 else 3
        self.method = method
        self.Headers = dict(headers)
        self.random_agent = random_agent
        self.timeout = timeout
        self.proxy = proxy
        self.allow_redirect = allow_redirect
        self.max_redirect = max_redirect
        self.blacklist_extensions = blacklist
        self.whitelist_extensions = whitelist
        self.http2 = http2
        self.valid_hosts = host_include
        self.invalid_hosts = host_exclude
        self.concurrency = concurrency
        self.Semaphore = asyncio.Semaphore(self.concurrency)
        self.output = output
        self.silent = silent
        self.verbose = verbose
        self.inscope = crawl_scope
        self.outscope = crawl_out_scope
        self.match_rgxs = match_regex
        self.filter_rgxs = filter_regex 
        self.delay = delay
        self.visiteds = set()
        self.found = set()
        self.tags = tags

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
            
    async def request(self, 
        site: str,  
        session: httpx.AsyncClient, 
        method: str, 
        headers: dict, 
        random_agent: bool, 
        timeout: int, 
        allow_redirect: bool, 
        verbose: bool):
        try:
            await self.Semaphore.acquire()
            await asyncio.sleep(0.000000001)
            redirect = True if self.allow_redirect else False
            self.Headers["User-Agent"] = UserAgent().random if random_agent else "git+spideyX/V1"
            response = await session.request(self.method.upper(), site, headers=self.Headers, timeout=self.timeout, follow_redirects=redirect)
            await asyncio.sleep(0.000000001)
            return response
        except KeyboardInterrupt as e:
            exit()
        except asyncio.CancelledError as e:
            exit()
        except httpx.RemoteProtocolError:
            pass
        except httpx.ConnectError as e:
            if self.verbose:
                    print(f"[{bold}{red}WRN{reset}]: {bold}{white}Unable to connect {site} , may be server unreachable or check your internet connection!{reset}")
        except httpx.ReadTimeout:
            if self.verbose:
                print(f"[{bold}{red}WRN{reset}]: {bold}{white}Unable to response from {url}, please try again!{reset}")
        except Exception as e: 
            if self.verbose:
                print(f"Exception at active crawler request: {e}, {type(e)}")
        finally:
            self.Semaphore.release()
    
    async def validator_exts(self,parsed_url) -> bool:
        try:            
            path = parsed_url.path
            ext = path.rsplit('.', 1)[-1] if '.' in path else ''
            ext = f".{ext}"
            if self.blacklist_extensions and  ext in self.blacklist_extensions:
                return False
            if not self.whitelist_extensions or ext in self.whitelist_extensions:
                return True
            return False
        except Exception as e: 
            if self.verbose:
                print(f"Exception at active crawler extensions validator: {e}, {type(e)}")
    
    async def validator_hosts(self,parsed_url) -> bool:
        try:
            host = parsed_url.hostname
            if self.valid_hosts and host not in self.valid_hosts:
                return False
            if self.invalid_hosts and host in self.invalid_hosts:
                return False
            return True
        except Exception as e: 
            if self.verbose:
                print(f"Exception at active crawler hosts validator: {e}, {type(e)}")  
    
    async def validator_scope(self,path) -> bool:
        try:
            if self.outscope :
                for route in self.outscope:
                    if route in path:
                        return False
                    else:
                        return True
            if self.inscope and any(ins_scope in path for ins_scope in self.inscope):
                return True
            if not self.inscope and not self.outscope:
                return True
        except Exception as e: 
            if self.verbose:
                print(f"Exception at active crawler scope validator: {e}, {type(e)}")
    
    async def validator_regx(self,url) -> bool:
        try:
            if self.match_rgxs:
                for pattern in self.match_rgxs:
                    if re.match(pattern,url):
                        return True
            if self.filter_rgxs :
                for pattern in self.filter_rgxs:
                    if not re.match(pattern, url):
                        return True
            if not self.filter_rgxs and not self.match_rgxs:       
                return True
        except Exception as e: 
            if self.verbose:
                print(f"Exception at active crawler scope validator: {e}, {type(e)}")
    
    async def scraper(self, response, url: str, domain: str):
        try:
            await asyncio.sleep(0.000000001)
            urls = set()
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", category=UserWarning)
                warnings.filterwarnings('ignore', category=XMLParsedAsHTMLWarning)
                warnings.filterwarnings("ignore", category=MarkupResemblesLocatorWarning)
                soup = BeautifulSoup(response.text, "lxml")
            for tag, attr in self.tags.items(): #Done with filtering as much as possible !
                for element in soup.find_all(tag, attrs={attr: True}):
                    href = element.get(attr)
                    if href and "mailto" not in href and "about:blank" not in href:
                        if href.startswith("\\\"https") or href.startswith("\\\"http"):
                            try:
                                href = href.replace('\\"', '').replace('\\/', '/')
                            except json.JSONDecodeError:
                                pass
                        if href.startswith("http://") or href.startswith("https://"):
                            absolute_url = href
                        else:
                            absolute_url = urljoin(url, href)
                        parsed_url = urlsplit(absolute_url)
                        hostname = parsed_url.netloc
                        if hostname == domain or hostname.endswith(f".{domain}"):
                            if await self.validator_scope(absolute_url) and await self.validator_exts(parsed_url) and await self.validator_hosts(parsed_url) and await self.validator_regx(absolute_url):
                                urls.add(absolute_url)
            return urls
        except KeyboardInterrupt:
            print(f"[{bold}{blue}INFO{reset}]: {bold}{white}\nCtrl+C Pressed{reset}")
            exit()
        except asyncio.CancelledError:
            exit()
        except httpx.InvalidURL:
            pass
        except UnicodeError:
            pass
        except Exception as e:
            if self.verbose:
                print(f"Exception at active crawler scraper: {e}, {type(e)}")
        
    async def Crawler(self, dept, url, domain, session):
        try:
            if dept > self.max_dept:
                return 
            if url in self.visiteds:
                return
            self.visiteds.add(url)
            await asyncio.sleep(self.delay)
            response = await self.request(url, session, self.method, self.Headers, self.random_agent, self.timeout, self.allow_redirect, self.verbose)
            if response is None:
                return
            urls = await self.scraper(response, url, domain)
            tasks = []
            await asyncio.sleep(0.000000001)
            if urls:
                urls = sorted(urls)
                for url in urls:
                    if url not in self.found:
                        print(f"{reset}{url}")
                        self.found.add(url)
                        if self.output:
                            await self.save(url, self.output)
                    extracted = tldextract.extract(url)
                    domain = f"{extracted.domain}.{extracted.suffix}"
                    task = asyncio.ensure_future(self.Crawler(dept+1, url, domain, session))
                    tasks.append(task)
                await asyncio.gather(*tasks)
        except KeyboardInterrupt:
            print(f"[{bold}{blue}INFO{reset}]: {bold}{white}\nCtrl+C Pressed{reset}")
            exit()
        except httpx.InvalidURL as e:
            if self.verbose:
                    print(f"Exception at active crawler dept invalid url: {e}, {type(e)}")
        except asyncio.CancelledError:
            exit()
        except ValueError as e:
            print(e, url)
        except Exception as e:
            if self.verbose:
                    print(f"Exception at active crawler dept: {e}, {type(e)}")
    
    async def start(self, dept=None, site=None, domain=None):
        try:
            dept = 0 if dept is None else dept
            site = self.site if site is None else site
            domain = self.domain if domain is None else domain
            proxy = self.proxy if self.proxy else None
            async with httpx.AsyncClient(verify=False, http2=self.http2, proxy=proxy) as session:
                await self.Crawler(0, self.site, self.domain, session)
        except KeyboardInterrupt:
            exit()
        except asyncio.CancelledError:
            exit()
        except Exception as e:
            if self.verbose:
                    print(f"Exception at active crawler start: {e}, {type(e)}")
                    


class PassiveAsyncSpidey(ActiveAsyncSpidey):
    
    def __init__(self, site: str, 
        domain: str,
        dept: int, 
        method: str, 
        headers, 
        random_agent: bool, 
        timeout: int,  
        proxy: str, 
        allow_redirect: bool, 
        max_redirect: int, 
        blacklist: list[str],  
        whitelist: list[str], 
        http2: bool, 
        host_include: list[str], 
        host_exclude: list[str],  
        concurrency: int, 
        output: str, 
        silent: bool, 
        verbose: bool,
        crawl_scope: list[str], 
        crawl_out_scope: list[str], 
        match_regex: list[str], 
        filter_regex: list[str],
        delay: float,
        tags: dict,
        presources: list[str]) -> None:
        super().__init__(
        site, 
        domain, 
        dept, 
        method, 
        headers, 
        random_agent, 
        timeout, 
        proxy, 
        allow_redirect, 
        max_redirect, 
        blacklist, 
        whitelist, 
        http2, 
        host_include, 
        host_exclude, 
        concurrency, 
        output, 
        silent, 
        verbose, 
        crawl_scope, 
        crawl_out_scope, 
        match_regex, 
        filter_regex, 
        delay, 
        tags)
        self.presources = presources
        
    async def validator_exts(self,parsed_url) -> bool:
        try:        
            path = parsed_url.path
            if self.whitelist_extensions:
                for ext in self.whitelist_extensions:
                    if path.endswith(f"{ext}"):
                        return True
                    else:
                        return False
            if self.blacklist_extensions:
                for ext in self.blacklist_extensions:
                    if path.endswith(f"{ext}"):
                        return False
                    else:
                        return True
            if not self.blacklist_extensions and not self.whitelist_extensions:
                return True
        except Exception as e: 
            if self.verbose:
                print(f"Exception at active crawler extensions validator: {e}, {type(e)}")
    
    async def printf(self, url:str) -> None:
        try:
            if url not in self.found:
                parsed_url = urlsplit(url)
                hostname = parsed_url.netloc
                if hostname == self.domain or hostname.endswith(f".{self.domain}"):
                    if await self.validator_scope(url) and await self.validator_exts(parsed_url) and await self.validator_hosts(parsed_url) and await self.validator_regx(url):
                        print(url)
                        self.found.add(url)
                        if self.output:
                            await self.save(url, self.output)
        except KeyboardInterrupt:
            exit()
        except asyncio.CancelledError:
            exit()
        except Exception as e:
            if self.verbose:
                print(f"Exception at passive printer: {e}, {type(e)}")
                
    async def waybackarchive(self):
        try:
            if self.presources and "waybackarchive" not in self.presources:
                return
            headers = {
                "User-Agent": UserAgent().random
            }
            async with httpx.AsyncClient(timeout=httpx.Timeout(read=300.0, connect=self.timeout, write=None, pool=None), headers=headers, verify=False) as request:
                response = await  request.request("GET", f"https://web.archive.org/cdx/search/cdx?url=*.{self.domain}&collapse=urlkey&fl=original",follow_redirects=self.allow_redirect)
                urls = response.text.splitlines()
                for url in urls:
                    await self.printf(url)
        except KeyboardInterrupt:
            exit()
        except asyncio.CancelledError:
            exit()
        except httpx.RemoteProtocolError:
            pass
        except httpx.ReadTimeout:
            pass
        except Exception as e:
            if self.verbose:
                    print(f"Exception at passive crawler waybackarchive: {e}, {type(e)}")
    
    async def indexDB(self):
        try:
            headers = {
                "User-Agent": UserAgent().random
            }
            async with httpx.AsyncClient(headers=headers, timeout=self.timeout, verify=False,proxy=self.proxy if self.proxy else None) as session:
                response = await session.request("GET", "https://index.commoncrawl.org/collinfo.json", follow_redirects=self.allow_redirect)
                return response.json()
        except KeyboardInterrupt:
            exit()
        except asyncio.CancelledError:
            exit()
        except httpx.RemoteProtocolError:
            pass
        except httpx.ReadTimeout:
            pass
        except Exception as e:
            if self.verbose:
                    print(f"Exception at passive crawler CC index fetcher: {e}, {type(e)}")
                    
    async def CcClient(self,searchurl: str):
        try:
            headers = {
                "User-Agent": UserAgent().random
            }
            async with httpx.AsyncClient(timeout=httpx.Timeout(read=300.0, connect=self.timeout, write=None, pool=None), headers=headers, verify=False, proxy=self.proxy if self.proxy else None) as streamer:
                async with streamer.stream("GET", f"{searchurl}?url=*.{self.domain}&output=text&fl=url", follow_redirects=self.allow_redirect) as response:
                    async for url in response.aiter_text():
                        await self.printf(url)
        except KeyboardInterrupt:
            exit()
        except asyncio.CancelledError as e:
            exit()
        except httpx.RemoteProtocolError:
            pass
        except httpx.ReadTimeout:
            pass
        except Exception as e:
            if self.verbose:
                print(f"Exception at passive crawler CC url fetcher: {e}, {type(e)}")
    
    async def commoncrawl(self):
        try:
            if self.presources and "commoncrawl" not in self.presources:
                return
            indexurls = []
            responsed = await self.indexDB()
            if responsed is None:
                return 
                
            ctyear = datetime.now().year
            years = [str(ctyear - i) for i in range(6)]
            for year in years:
                for index in responsed:
                    if year in index.get("name"):
                        indexurls.append(index.get('cdx-api'))
            for url in indexurls:
                await self.CcClient(url)
        except KeyboardInterrupt:
            exit()
        except asyncio.CancelledError as e:
            exit()
        except Exception as e:
            if self.verbose:
                    print(f"Exception at passive crawler commoncrawl: {e}, {type(e)}")
    
    async def otx(self):
        try:
            if self.presources and "alienvault" not in self.presources:
                return
            page=1
            while True:
                async with httpx.AsyncClient(timeout=httpx.Timeout(read=300.0, connect=self.timeout, write=None, pool=None), headers={"User-Agent": UserAgent().random}, verify=False,proxy=self.proxy if self.proxy else None) as session:
                    response = await session.request("GET", f"https://otx.alienvault.com/api/v1/indicators/domain/{self.domain}/url_list?page={page}")
                    data = response.json()
                    await asyncio.sleep(0.001)
                    urls = [item['url'] for item in data['url_list']]
                    for url in urls:
                        await self.printf(url)
                    pages = data.get('has_next')
                    if not pages:
                        break
                    page+=1
        except KeyboardInterrupt:
            exit()
        except asyncio.CancelledError:
            exit()
        except httpx.RemoteProtocolError:
            pass
        except httpx.ReadTimeout:
            pass
        except Exception as e:
            if self.verbose:
                print(f"Exception at passive crawler CC url fetcher: {e}, {type(e)}")
    
    async def starts(self):
        try:
            await self.waybackarchive()
            await self.commoncrawl()
            await self.otx()
        except KeyboardInterrupt:
            exit()
        except asyncio.CancelledError:
            exit()
        except Exception as e:
            if self.verbose:
                print(f"Exception at passive crawler starter: {e}, {type(e)}")