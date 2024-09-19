import json
from colorama import Fore,Style 
import asyncclick as click
import random
import sys
import asyncio
import time
from yarl import URL
import os

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

try:
    from spideyx.modules.banner.banner import banner
    from spideyx.modules.config.config import config, custompath, username, cachedir
    from spideyx.modules.extractor.extracter import Extractor
    from spideyx.modules.help.help import main_help, crawler_help, jsscrapy_help, paramfuzzer_help, update_help
    from spideyx.modules.jsScrapy.jsScrapy import JsScrapy
    from spideyx.modules.paramfuzzer.paramfuzzer import AsyncSpideyFuzzer
    from spideyx.modules.scraper.scraper import ActiveAsyncSpidey, PassiveAsyncSpidey
    from spideyx.modules.update.update import zip_url, latest_update, updatelog
    from spideyx.modules.verify.verify import getverify
    from spideyx.modules.version.version import Version
except ImportError as e:
    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Import Error occured in Module imports due to: {e}{reset}")
    print(f"[{bold}{blue}INFO{reset}]: {bold}{white}If you are encountering this issue more than a time please report the issues in SpideyX Github page.. {reset}")
    exit()
    
banner = banner()
configpath = config()
username = username() #this is nothitng just to know your name for spideyX
def gitversion():
    latest = Version()
    current = "v1.0.0"
    if not latest:
        print(f"[{bold}{red}WRN{reset}]: {bold}{white}Unable to get latest version of spideyx from git!{reset}", file=sys.stderr)
        return
    if latest == current:
        print(f"[{bold}{blue}version{reset}]: {bold}{white}spideyx current version {current} ({green}latest{reset}{bold}{white}){reset}", file=sys.stderr)
    else:
        print(f"[{bold}{blue}version{reset}]: {bold}{white}spideyx current version {current} ({red}outdated{reset}{bold}{white}){reset}", file=sys.stderr)
        
async def url_manager(site, dept, method, headers, random_agent, timeout,  proxy, allow_redirect, max_redirect, blacklist, whitelist , http2, host_include, host_exclude,  concurrency, output, silent, verbose,crawl_scope, crawl_out_scope, match_regex, filter_regex, delay,tags_attrs, passive, passive_resources):
    try:
        url = URL(site)
        domain = url.host
        if not passive:
            Activespidey = ActiveAsyncSpidey(site, domain,dept, method, headers, random_agent, timeout, proxy, allow_redirect, max_redirect, blacklist, whitelist , http2, host_include, host_exclude,  concurrency, output, silent, verbose,crawl_scope, crawl_out_scope, match_regex, filter_regex, delay,tags_attrs)
            print(f"[{bold}{blue}INFO{reset}]: {bold}{white}started active crawling 🕸️  ==> {url}{reset}", file=sys.stderr )
            await Activespidey.start()
        else:
            PassiveSpidey = PassiveAsyncSpidey(site, domain,dept, method, headers, random_agent, timeout, proxy, allow_redirect, max_redirect, blacklist, whitelist , http2, host_include, host_exclude,  concurrency, output, silent, verbose,crawl_scope, crawl_out_scope, match_regex, filter_regex, delay,tags_attrs, passive_resources)
            print(f"[{bold}{blue}INFO{reset}]: {bold}{white}started passive crawling 🕸️  ==> {url}{reset}", file=sys.stderr)
            await PassiveSpidey.starts()
    except Exception as e:
        print(f"[{bold}{red}WRN{reset}]: {bold}{white}Exception in URL manager: {e}, {type(e)}{reset}", file=sys.stderr)
    
async def processor(sem, site, dept, method, headers, random_agent, timeout,  proxy, allow_redirect, max_redirect, extension_filter, extension_match , http2, host_include, host_exclude,  concurrency, output, silent, verbose,crawl_scope, crawl_out_scope, match_regex, filter_regex, delay,tags_attrs,passive, passive_resources):
    try:
        async with sem:
            await url_manager(site, dept, method, headers, random_agent, timeout,  proxy, allow_redirect, max_redirect, extension_filter, extension_match, http2, host_include, host_exclude, concurrency, output, silent, verbose,crawl_scope, crawl_out_scope, match_regex, filter_regex,delay,tags_attrs,passive, passive_resources)
    except Exception as e:
        print(f"[{bold}{red}WRN{reset}]: Warning from parallel processor due to: {e}, {type(e)}", file=sys.stderr)
        

def customizer_help(ctx, param, value): #https://click.palletsprojects.com/en/8.1.x/options/#callbacks-and-eager-options
    if value and not ctx.resilient_parsing:
        if not ctx.invoked_subcommand:
            print(f"{random_color}{banner}{reset}")
            main_help()
            exit()
        else:
            ctx.invoke(ctx.command, ['--help'])
            
print(f"{bold}{white}")
@click.group(context_settings={'help_option_names': ['-h', '--help']})
@click.option("-h", "--help", is_flag=True, is_eager=True, expose_value=False, callback=customizer_help)
async def cli():
    pass

@cli.command()
@click.option("-h", "--help", is_flag=True)
@click.option("-site", "--site", type=str)
@click.option("-sites", "--sites", type=str)
@click.option("-dept", "--dept", type=int, default=1)
@click.option("-X", "--method",  default="get", type=click.Choice(choices=["get", "post", "head", "put", "delete", "patch", "trace", "connect", "options"], case_sensitive=False))
@click.option("-H", "--headers", type=(str,str), multiple=True)
@click.option("-ra", "--random-agent", is_flag=True)
@click.option("-to", "--timeout", type=int, default=30)
@click.option("-r", "--robots", is_flag=True)
@click.option("-st", "--sitemap", is_flag=True)
@click.option("-px", "--proxy", type=str)
@click.option("-ar", "--allow-redirect", is_flag=True)
@click.option("-mr", "--max-redirect", type=int, default=10)
@click.option("-ef", "--extension-filter", type=str, callback=Extractor.blacklist)
@click.option("-em", "--extension-match", type=str,callback=Extractor.extract)
@click.option("-cp", "--config-path", type=str)
@click.option("-http2", "--http2", is_flag=True)
@click.option("-hic", "--host-include", type=str,callback=Extractor.extract)
@click.option("-hex", "--host-exclude", type=str,callback=Extractor.extract)
@click.option("-ps", "--passive", is_flag=True)
@click.option("-pss", "--passive-source", type=str,callback=Extractor.extract)
@click.option("-c", "--concurrency", type=int, default=10)
@click.option("-pl", "--parallelism", type=int, default=2)
@click.option("-o", "--output", type=str)
@click.option("-s", "--silent", is_flag=True)
@click.option("-vr", "--verbose", is_flag=True)
@click.option("-cs", "--crawl-scope", type=str)
@click.option("-cos", "--crawl-out-scope", type=str)
@click.option("-mr", "--match-regex", type=str,callback=Extractor.extract)
@click.option("-fr", "--filter-regex", type=str,callback=Extractor.extract)
@click.option("-delay", "--delay", default=1, type=float)
@click.option("-tgs", "--tags-attrs", type=str,callback=Extractor.tagshandler)
async def crawler(help, site, sites, dept, method, headers, random_agent, timeout, robots, sitemap, proxy, allow_redirect, max_redirect, extension_filter, extension_match,config_path,  http2, host_include, host_exclude, passive, passive_source, concurrency, parallelism, output, silent, verbose, crawl_scope, crawl_out_scope, match_regex, filter_regex,delay,tags_attrs):
    if not silent:
        click.echo(f"{random_color}{banner}{reset}")
        
    if help:
        crawler_help()
        exit()
    if not silent:
        gitversion()
    sem = asyncio.BoundedSemaphore(parallelism)
    crawl_scope = await Extractor.ScopeReader(crawl_scope)
    crawl_out_scope = await Extractor.ScopeReader(crawl_out_scope)
    if site:
        if site.startswith("https://") or  site.startswith("http://"):
            pass
        else:
            site = f"https://{site}"
        await url_manager(site, dept, method, headers, random_agent, timeout,  proxy, allow_redirect, max_redirect, extension_filter, extension_match, http2, host_include, host_exclude, concurrency, output, silent, verbose,crawl_scope, crawl_out_scope, match_regex, filter_regex,delay,tags_attrs,passive, passive_source)
        exit()
        
    if sites:
        sem = asyncio.Semaphore(parallelism)
        urls = await Extractor.Reader(sites)
        tasks = []
        if urls:
            for site in urls:
                if  site.startswith("https://") or  site.startswith("http://"):
                    pass
                else:
                    site = f"https://{site}"
                task = asyncio.ensure_future(processor(sem, site, dept, method, headers, random_agent, timeout,  proxy, allow_redirect, max_redirect, extension_filter, extension_match, http2, host_include, host_exclude, concurrency, output, silent, verbose,crawl_scope, crawl_out_scope, match_regex, filter_regex,delay,tags_attrs,passive, passive_source))
                tasks.append(task)
                await asyncio.gather(*tasks)
        exit()
        
    if sys.stdin.isatty():
        print(f"[{bold}{red}WRN{reset}]: {bold}{white}no input provided for spideyX 🕸️{reset}")
        exit()
    
    tasks = []
    for site in sys.stdin:
        site = site.strip()
        if  site.startswith("https://") or  site.startswith("http://"):
            pass
        else:
            site = f"https://{site}"
        task = asyncio.ensure_future(processor(sem, site, dept, method, headers, random_agent, timeout,  proxy, allow_redirect, max_redirect, extension_filter, extension_match, http2, host_include, host_exclude, concurrency, output, silent, verbose,crawl_scope, crawl_out_scope, match_regex, filter_regex,delay,tags_attrs,passive, passive_source))
        tasks.append(task)
    await asyncio.gather(*tasks)
    exit()

@cli.command()
@click.option("-h", "--help", is_flag=True)
@click.option("-site", "--site", type=str)
@click.option("-sites", "--sites", type=str)
@click.option("-cp", "--config-path", type=str)
@click.option("-c", "--concurrency", type=int, default=30)
@click.option("-vr", "--verbose", is_flag=True)
@click.option("-o", "--output", type=str)
@click.option("-H", "--header", type=(str,str), multiple=True)
@click.option("-dr", "--disable-redirect", is_flag=True, default=True)
@click.option("-px", "--proxy", type=str, default=None)
@click.option("-s", "--silent", is_flag=True)
@click.option("-to", "--timeout", type=int, default=15)
async def jsscrapy(help, site, sites, config_path, concurrency, verbose, output, header, disable_redirect, proxy, silent, timeout):
    if not silent:
        click.echo(f"{random_color}{banner}{reset}")
    if help:
        jsscrapy_help()
        exit()
    if not silent:
        gitversion()
    yaml_path = config_path if config_path else configpath
    yaml_content = await Extractor.Yamlreader(yaml_path)
    print(f"[{bold}{blue}INFO{reset}]: {bold}{white}Loading config file from {yaml_path}{reset}", file=sys.stderr)
    urls = [] 
    if site:
        urls.append(site)
        jsSpidey = JsScrapy(yaml_content, urls, concurrency, proxy, disable_redirect, verbose, timeout, output,header)
        await jsSpidey.start()
        exit()
        
    if sites:
        loaded = await Extractor.Reader(sites)
        if loaded:  
            for url in loaded:
                urls.append(url)
            jsSpidey = JsScrapy(yaml_content, urls, concurrency, proxy, disable_redirect, verbose, timeout, output,header)
            await jsSpidey.start()
            exit()
            
    if sys.stdin.isatty():
        print(f"[{bold}{red}WRN{reset}]: {bold}{white}no input provided for spideyX 🕸️{reset}")
        exit()    
    for url in sys.stdin:
        url = url.strip()
        urls.append(url)
    jsSpidey = JsScrapy(yaml_content, urls, concurrency, proxy, disable_redirect, verbose, timeout, output,header)
    await jsSpidey.start()
    exit()
   

@cli.command()
@click.option("-h", "--help", is_flag=True)
@click.option("-site", "--site", type=str)
@click.option("-sites", "--sites", type=str)
@click.option("-w", "--wordlist", type=str)
@click.option("-H", "--header", type=(str, str), multiple=True)
@click.option("-X", "--method", type=click.Choice(choices=["get", "post", "head", "put", "delete", "patch", "trace", "connect", "options"], case_sensitive=False),default="get")
@click.option("-body", "--body", type=str)
@click.option("-fmt", "--format", type=click.Choice(choices=["html", "json", "xml"], case_sensitive=False))
@click.option("-to", "--timeout", type=int, default=15)
@click.option("-px", "--proxy", type=str)
@click.option("-ch", "--chunks", type=int, default=100)
@click.option("-c", "--concurrency", type=int, default=5)
@click.option("-dr", "--disable-redirect", is_flag=True, default=False)
@click.option("-s", "--silent", is_flag=True, default=False)
@click.option("-vr", "--verbose", is_flag=True, default=False)
@click.option("-o", "--output", type=str)
@click.option("--http-raw", type=str)
@click.option("-delay", "--delay", type=float, default=0.000001)
@click.option("-ra", "--random-agent", is_flag=True, default=False)
async def paramfuzzer(help, site, sites, wordlist, header, method, body, format, timeout, proxy, chunks, concurrency,disable_redirect, silent, verbose, output, http_raw, delay, random_agent):
    if not silent:
        click.echo(f"{random_color}{banner}{reset}")
    if help:
        paramfuzzer_help()
        quit()
    if not silent:
        gitversion()
    if site:
        if not wordlist:
            print(f"[{bold}{red}WRN{reset}]: {bold}{white}Please provide a wordlist for spideyX 🕸️{reset}")
        wordlists = await Extractor.Reader(wordlist)
        if wordlists:
            spideyfuzzer = AsyncSpideyFuzzer(site, wordlists,concurrency, chunks, header, method, proxy, disable_redirect, body, format, http_raw, verbose, timeout, delay, random_agent, output)
            await spideyfuzzer.start()
        exit()
        
    if http_raw:
        if not wordlist:
            print(f"[{bold}{red}WRN{reset}]: {bold}{white}Please provide a wordlist for spideyX 🕸️{reset}")
        wordlists = await Extractor.Reader(wordlist)
        method, site, header, body = await AsyncSpideyFuzzer.raw_http_reader(http_raw)
        contents = header.get("Content-Type")
        if contents and contents == "application/json":
            format = "json"
        elif contents and contents == "application/xml":
            format = "xml"
        else:
            format = "html"
        if wordlists:
            spideyfuzzer = AsyncSpideyFuzzer(site, wordlists,concurrency, chunks, header, method, proxy, disable_redirect, body, format, http_raw, verbose, timeout, delay, random_agent, output)
            await spideyfuzzer.start()
        exit()
    
    if sites:
        urls = await Extractor.Reader(sites)
        if not wordlist:
            print(f"[{bold}{red}WRN{reset}]: {bold}{white}Please provide a wordlist for spideyX 🕸️{reset}")
        wordlists = await Extractor.Reader(wordlist)
        if not wordlists:
            exit()
        if urls:  
            for site in urls:
                spideyfuzzer = AsyncSpideyFuzzer(site, wordlists,concurrency, chunks, header, method, proxy, disable_redirect, body, format, http_raw, verbose, timeout, delay, random_agent, output)
                await spideyfuzzer.start()
            exit()
    
    if sys.stdin.isatty():
        print(f"[{bold}{red}WRN{reset}]: {bold}{white}no input provided for spideyX 🕸️{reset}")
        exit()
    else:
        if not wordlist:
            print(f"[{bold}{red}WRN{reset}]: {bold}{white}Please provide a wordlist for spideyX 🕸️{reset}")
            exit()
        wordlists = await Extractor.Reader(wordlist) 
        if wordlists:
            for site in sys.stdin:
                site = site.strip()
                spideyfuzzer = AsyncSpideyFuzzer(site, wordlists,concurrency, chunks, header, method, proxy, disable_redirect, body, format, http_raw, verbose, timeout, delay, random_agent, output)
                await spideyfuzzer.start()
            exit()

@cli.command() #this wont update until user execute update mode!
@click.option("-sup", "--show-update", is_flag=True)
@click.option("-lt", "--latest", is_flag=True)
@click.option("-h", "--help", is_flag=True)
async def update(show_update, latest, help):
    click.echo(f"{random_color}{banner}{reset}")
    if help:
        update_help()
        exit()
    if show_update:
        updatelog()
        exit()
    if latest:
        current = "v1.0.0"
        oldpy = "1.0.0"
        git = Version()
        if not git:
            print(f"[{bold}{red}WRN{reset}]: {bold}{white}Hey {username} unable to git version, please try again to update{reset}")
            exit()
        if current == git:
            print(f"[{bold}{green}INFO{reset}]: {bold}{white}Hey {username} SpideyX 🕸️ is already in latest version!{reset}")
            exit()
        
        zipurl = zip_url(username)
        if not zipurl:
            print(f"[{bold}{red}WRN{reset}]: {bold}{white}Unable to get the latest version zip file of spideyx, so try to update with `pip` or `pipx`{reset}")
            exit()
        caches = cachedir()
        latest_update(zipurl, username,caches)
        pypiversion = getverify("spideyx")
        if oldpy == pypiversion:
            print(f"[{bold}{red}WRN{reset}]: {bold}{white}Unable to get the latest version zip file of spideyx, so try to update with `pip` or `pipx` also try with root or admin privileges if you didn't!{reset}")
            exit()
        updatelog()
        exit()
    if sys.stdin.isatty():
        print(f"[{bold}{red}WRN{reset}]: {bold}{white}stdin reader in not available in  spideyX 🕸️ update mode!{reset}")
        exit()
    
if __name__ == "__main__":
    cli()
