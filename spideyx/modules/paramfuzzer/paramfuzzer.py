import asyncio
import httpx
import random
import string
import aiofiles
from alive_progress import alive_bar
from itertools import islice
import os
from colorama import Fore,Style
import random
import warnings
from fake_useragent import UserAgent
from urllib.parse import urljoin, urlparse, urlsplit, urlencode
import json
from dicttoxml import dicttoxml
import string
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

class AsyncSpideyFuzzer:
    def __init__(
        self, 
        url: str,
        wordlists: list,
        concurrency: int,
        chunks: int,
        header,
        method: str,
        proxy: str,
        redirections: bool,
        body: str,
        format: str,
        http_raw: str,
        verbose: bool,
        timeout: int,
        delay: int,
        random_agent: bool,
        output: str
    ) -> None:
        self.url = url
        self.wordlists = wordlists
        self.concurrency = concurrency
        self.chunks = chunks
        self.Headers = dict(header)
        self.method = method
        self.proxy = proxy if proxy else None
        self.redirs = redirections
        self.body = body
        self.format = format
        self.raw_http = http_raw
        self.verbose = verbose
        self.timeout = timeout
        self.delay = delay
        self.random_agent = random_agent
        self.output = output
        self.Semaphore = asyncio.Semaphore(concurrency)
        
    @staticmethod   
    async def raw_http_reader(raw_http:str) :
        try:
            lines = raw_http.splitlines()
            request_line = lines[0].split()
            method = request_line[0]
            url = request_line[1]
        
            headers = {}
            i = 1
            while i < len(lines):
                line = lines[i]
                if not line.strip(): 
                    break
                if ':' in line:
                    key, value = line.split(':', 1)
                    headers[key.strip()] = value.strip()
                i += 1
            body = None
            if i + 1 < len(lines):  
                body = '\n'.join(lines[i+1:]).strip()
            return method, url, headers, body
        except KeyboardInterrupt as e:
            exit()
        except asyncio.CancelledError as e:
            exit()
        except Exception as e:
                print(f"[{bold}{red}WRN{reset}]: {bold}{white}Unknown exception occured in Raw Requests reader due to: {e}, {type(e)}{reset}")
        
    async def randomizer(self):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=7))
        
    def chunked(self, params: list, size: int):
        iters = iter(params)
        while chunk := list(islice(iters, size)):
            yield chunk
    
    async def replacer(self, data: str, value):
        return data.replace("$pidey", f"{value}")
    
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
    
    async def Requests(self, url: str, method="GET", params=None):
        async with self.Semaphore:
            try:
                Json=None
                data=None
                if self.body:
                    if "$pideyx" in self.body and self.format == "json":
                        formatted_params = json.dumps(params)[1:-1] 
                        modified_body = self.body.replace('$pideyx', formatted_params)
                        try:
                            Json = json.loads(modified_body)
                            params = None
                        except json.JSONDecodeError as e:
                            if self.verbose:
                                print(f"[{bold}{red}WRN{reset}]: {bold}{white}Unable to Jsonify the data!: {e}{reset}")
                        except KeyboardInterrupt as e:
                            exit()
                        except asyncio.CancelledError as e:
                            exit()
                        except Exception as e:
                            if self.verbose:
                                print(f"[{bold}{red}WRN{reset}]: {bold}{white}Unknown exception occured in Requests josnifier due to: {e}, {type(e)}{reset}")
                    elif "$pideyx" in self.body and self.format == "xml":
                        data=dicttoxml(params, root=False, attr_type=False).decode('utf-8')
                        params=None
                    elif "$pideyx" in self.body and self.format == "html":
                        encoded_params = urlencode(params)
                        data = self.body.replace('$pideyx', encoded_params)
                        params = None
                    else:
                        params=params
                else:
                    params=params
                await asyncio.sleep(self.delay)
                self.Headers["User-Agent"] = UserAgent().random if self.random_agent else "git+spideyX/V1"
                async with httpx.AsyncClient(verify=False, timeout=self.timeout, http2=True, follow_redirects=self.redirs, proxy=self.proxy, max_redirects=30) as requests:
                    response = await requests.request(method.upper(), url=url, data=data, headers=self.Headers, params=params,json=Json)
                    return response
            except httpx.ReadTimeout:
                print(f"[{bold}{red}WRN{reset}]: {bold}{white}Unable to response from {url}, please try again!{reset}")
            except httpx.ConnectError:
                print(f"[{bold}{red}WRN{reset}]: {bold}{white}Unable to connect host, may be server unreachable or check your internet connection!{reset}")
            except httpx.ConnectTimeout:
                print(f"[{bold}{red}WRN{reset}]: {bold}{white}Connection Timeout reached for connection to {url}, try with --timeout 30 or host may be unreachable!{reset}")
            except httpx.RemoteProtocolError:
                print(f"[{bold}{red}WRN{reset}]: {bold}{white}A malformed http request protocol violated by the server!{reset}")
            except KeyboardInterrupt as e:
                exit()
            except asyncio.CancelledError as e:
                exit()
            except Exception as e:
                if self.verbose:
                    print(f"[{bold}{red}WRN{reset}]: {bold}{white}Unknown exception occured in Requests due to: {e}, {type(e)}{reset}")
    
    async def variations(self, base_response: httpx.Response , param_chunks: dict, url: str) -> list:
        factors=[]
        try:
            new_response = await self.Requests(url, self.method, params=param_chunks)
            await asyncio.sleep(0.001)
            if new_response is None:
                return factors
            base_headers = set(base_response.headers.keys())
            new_headers =  set(new_response.headers.keys())
            variated_headers = new_headers - base_headers
            if variated_headers:
                factors.append(f"New Headers Detected: {', '.join(variated_headers)}")
            if base_response.status_code != new_response.status_code:
                factors.append(f"Response status code variation from {base_response.status_code} -> {new_response.status_code}")
            if len(base_response.content) != len(new_response.content):
                factors.append(f"Response content length variation from {len(base_response.content)} -> {len(new_response.content)}")
            if base_response.text != new_response.text:
                factors.append(f"Response body variation detected")
            if base_response.text.count('\n') != new_response.text.count('\n'):
                factors.append("Response body count variation from %s -> %s" % (base_response.text.count("\n"), new_response.text.count("\n")))
            if urlparse(base_response.headers.get('Location', '')).path != urlparse(new_response.headers.get('Location', '')).path:
                factors.append(f"Response redirection variation from {urlparse(base_response.headers.get('Location', '')).path} -> {urlparse(new_response.headers.get('Location', '')).path}")
        except KeyboardInterrupt as e:
            exit()
        except asyncio.CancelledError as e:
            exit()  
        except Exception as e:
            if self.verbose:
                print(f"[{bold}{red}WRN{reset}]: {bold}{white}Unknown exception occured in variation finder due to: {e}, {type(e)}{reset}")
        return factors
    
    async def root_cause(self, url:str, params_chunks:dict, base_response: httpx.Response, max_chunkies=1): 
        try:
            await asyncio.sleep(0.0001)
            if len(params_chunks) <= max_chunkies:
                tasks = []
                for param, value in params_chunks.items():
                    individual_params = {param: value}
                    task = asyncio.ensure_future(self.variations(base_response,individual_params,url))
                    tasks.append(task)
                results = await asyncio.gather(*tasks, return_exceptions=False)
                causative_params = {}
                for param, factors in zip(params_chunks, results):
                    if factors:
                        causative_params[param] = factors
                return causative_params
            mid = len(params_chunks) // 2
            first_half = list(params_chunks.items())[:mid]
            second_half = list(params_chunks.items())[mid:]
            sub_chunks = [dict(first_half), dict(second_half)]
            tasks = []
            for chunk in sub_chunks:
                task = asyncio.ensure_future(self.variations(base_response, chunk, url))
                tasks.append(task)
            results = await asyncio.gather(*tasks, return_exceptions=False)
            isolated_params = {}
            if results[0]:
                first_half_params = await self.root_cause(url, sub_chunks[0],base_response)
                isolated_params.update(first_half_params)
    
            if results[1]: 
                second_half_params = await self.root_cause(url, sub_chunks[1],base_response)
                isolated_params.update(second_half_params)
            return isolated_params
        except KeyboardInterrupt as e:
            exit()
        except asyncio.CancelledError as e:
            exit()
        except Exception as e:
            if self.verbose:
                print(f"[{bold}{red}WRN{reset}]: {bold}{white}Unknown exception occured in causative param finder due to: {e}, {type(e)}{reset}")
    
    async def core(self, url: str, params_chunks: dict, base_response: httpx.Response, bar):
            try:
                factors = await self.variations(base_response, params_chunks, url)
                if factors:
                    causative_params = await self.root_cause(url, params_chunks, base_response)
                    if causative_params:
                        for param, reasons in causative_params.items():
                            print(f"{bold}{white}[{bold}{green}+{reset}{bold}] Hidden Parameters Found: {param}")
                            if self.output:
                                await self.save(f"Hidden Parameter Found: {param}", self.output)
                            for reason in reasons:
                                print(f"{bold}{white}      - {reason}{reset}")
            except KeyboardInterrupt as e:
                exit()
            except asyncio.CancelledError as e:
                exit()
            except Exception as e:
                if self.verbose:
                    print(f"[{bold}{red}WRN{reset}]: {bold}{white}Unknown error in core: {e}, {type(e)}{reset}")
            finally:
                bar()
        
    async def start(self):
            try:
                print(f"[{bold}{blue}INFO{reset}]: {bold}{white}Probing for target stability!{reset}")
                base_response = await self.Requests(self.url, method=self.method, params={"test": "value1"})
                if base_response:
                    print(f"{bold}{blue}URL{reset}:{bold}{white}{base_response.request.url}{reset}")
                    print(f"{bold}{green}METHOD{reset}:{bold}{white}{base_response.request.method}{reset}")
                    print(f"{bold}{green}WORDLISTS LEN{reset}:{bold}{white}{len(self.wordlists)}{reset}")
                    with alive_bar(len(self.wordlists) // self.chunks + 1, title=f"{bold}{white}SpideyX{reset}", enrich_print=False) as bar:
                        tasks = []
                        for params_chunk in self.chunked(self.wordlists, self.chunks):
                            random_params = {}
                            for param in params_chunk:
                                random_value = await self.randomizer()
                                random_params[param] = random_value
                            task = asyncio.ensure_future(self.core(self.url, random_params, base_response, bar))
                            tasks.append(task)
                        await asyncio.gather(*tasks, return_exceptions=False)
                else:
                    print(f"[{bold}{red}WRN{reset}]: {bold}{white}Target is not stable, try again with --verbose enabled{reset}")
                    exit()
            except KeyboardInterrupt as e:
                exit()
            except asyncio.CancelledError as e:
                exit()
            except Exception as e:
                if self.verbose:
                    print(f"[{bold}{red}WRN{reset}]: {bold}{white}Unknown error in start: {e}, {type(e)}{reset}")
