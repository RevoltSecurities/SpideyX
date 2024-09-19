from colorama import Fore,Back,Style
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

def main_help():
    
    print(f"""
[{bold}{blue}DESCRIPTION{reset}]: {bold}{white}spideyX - A Web Reconnaissance Penetration Testing tool for Penetration Testers and Ethical Hackers{reset}
          
[{bold}{blue}MODES{reset}]: {bold}{white}

    - crawler        : spideyX asynchronous crawler mode to crawl urls with more user controllables settings.
    - paramfuzzer    : spideyX pramfuzzer mode , a faster mode to fuzz hidden parameters.
    - jsscrapy       : spideyX jsscrapy mode, included with asynchronous concurrency and find hidden endpoint and secrets using yaml template based regex.
    - update         : spideyX update mode to update and get latest update logs of spideyX

[{bold}{blue}FLAGS{reset}{bold}{white}]: 

    -h,  --help   : Shows this help message and exits.
              
[{bold}{blue}Usage{reset}{bold}{white}]:
          
        spideyx [commands]
        
        Available Commands:
    
            - crawler          : Executes web crawling mode of spideyX.
            - paramfuzzer      : Excecutes paramfuzzer bruteforcing mode of spideyX.
            - jsscrapy         : Executes jscrawl mode of spideyX to crawl js  hidden endpoints & credentials using template based regex.
            - update           : Executes the update mode of spideyX
            
        Help Commands:
        
            - crawler         : spideyx crawler  -h
            - paramfuzzer     : spideyx paramfuzzer -h
            - jsscrapy        : spideyx jsscrapy -h
            - update          : spideyx update -h{reset}""")
    
def crawler_help():
    print(f"""  
    [{bold}{blue}MODE{reset}]: {bold}{white}spideyX crawler mode!{reset}
                
    [{bold}{blue}Usage{reset}]: {bold}{white}
              
            spidey crawler [options]
              
            Options for crawler mode:
                
                [{bold}{blue}input{reset}{bold}{white}]: 
                    
                  -site,  --site          : target url for spideyX to crawl
                  -sties, --sites         : target urls for spideyX to crawl
                  stdin/stdout            : target urls for spideyX using stdin
                
                [{bold}{blue}configurations{reset}{bold}{white}]:
                    
                  -tgs, --tags-attrs      : spideyx crawling tags can be configured using this flags you can control spideyx crawling  (ex: -tgs 'a:href,link:src,src:script')
                  -dept, --dept           : dept value to crawl for urls by spideyx (info: only in active crawling) (default: 1)
                  -X,  --method           : request method for crawling (default: get) (choices: "get", "post", "head", "put", "delete", "patch", "trace", "connect", "options")
                  -H,  --headers          : custom headers & cookies to send in http request for authenticated or custom header crawling
                  -ra, --random-agent     : use random user agents for each request in crawling urls instead of using default user-agent of spideyx
                  -to , --timeout          : timeout values for each request in crawling urls (default: 15)
                  -px, --proxy            : http proxy url to send request via proxy
                  -ar, --allow-redirect   : follow redirects for each http request
                  -mr, --max-redirect     : values for max redirection to follow
                  -mxr, --max-redirection : specify maximum value for maximum redirection to be followed when making requests.
                  -cp, --config-path      : configuration file path for spideyX
                  --http2, --http2        : use http2 protocol to give request and crawl urls, endpoints
                   
                [{bold}{blue}scope{reset}{bold}{white}]: 
                    
                  -hic, --host-include    : specify hosts to include urls of it and show in results with comma seperated values  (ex: -hc api.google.com,admin.google.com)
                  -hex, --host-exclude    : speify  hosts to exclude urls of it and show in results with comma seperated values   (ex: -hex class.google.com,nothing.google.com)
                  -cs,  --crawl-scope     : specify the inscope url to be crawled by spideyx (ex: -cs /api/products or -cs inscope.txt)
                  -cos, --crawl-out-scope : specify the outscope url to be not crawled by spideyx (ex: -cos /api/products or -cos outscope.txt)
                
                [{bold}{blue}filters{reset}{bold}{white}]: 
                    
                 -em, --extension-match  : extensions to blacklist and avoid including in output with comma seperated values (ex: -wl php,asp,jspx,html)
                 -ef, --extension-filter : extensions to whitelist and include in output with comma seperated values (ex: -bl jpg,css,woff)
                 -mr, --match-regex      : sepcify a regex or list of regex to match in output by spideyx
                 -fr, --filter-regex     : specify a regex or list of regex to exclude in output by spideyx
                  
                [{bold}{blue}passive{reset}{bold}{white}]: 
                    
                  -ps, --passive          : use passive resources for crawling (alienvault, commoncrawl, virustotal)
                  -pss, --passive-source  : passive sources to use for finding endpoints with comma seperated values (ex: -pss alienvault,virustotal)
                   
                [{bold}{blue}rate-limits{reset}{bold}{white}]: 
                
                  -c,  --concurrency      : no of concurrency values for concurrent crawling (default: 50)
                  -pl, --parallelism      : no of parallelism values for parallel crawling for urls (default: 2)
                  -delay, --delay         : specify a delay value between each concurrent requests (default: 0.1)
                [{bold}{blue}output{reset}{bold}{white}]: 
                    
                  -o, --output            : output file to store results of spideyX
                
                [{bold}{blue}debug{reset}{bold}{white}]: 
                  -s,  --silent          : display only output to console
                  -vr, --verbose          : increase the verbosity of the output{reset}""")

def jsscrapy_help():
    print(f"""  
    [{bold}{blue}MODE{reset}]: {bold}{white}spideyX jsscrapy mode!{reset}
                
    [{bold}{blue}Usage{reset}]: {bold}{white}
              
            spidey jsscrapy [options]
              
            Options for jsscrapy mode:
                
                [{bold}{blue}input{reset}{bold}{white}]: 
                    
                  -site,  --site          : target url for spideyX to jscrawl
                  -sties, --sites         : target urls for spideyX to jscrawl
                  stdin/stdout            : target urls for spideyX using stdin
                   
                [{bold}{blue}configurations{reset}{bold}{white}]:
                    
                  -H,  --header           : custom headers & cookies to send in http request for authenticated or custom header jscrawling
                  -to , --timeout          : timeout values for each request in jscrawling urls (default: 15)
                  -px, --proxy            : http proxy url to send request via proxy
                  -dr, --disable-redirect : disable following redirects for each http request
                  -cp, --config-path      : configuration file path for spideyX                   

                [{bold}{blue}rate-limits{reset}{bold}{white}]: 
                
                  -c,  --concurrency      : no of concurrency values for concurrent crawling (default: 50)

                [{bold}{blue}output{reset}{bold}{white}]: 
                    
                  -o, --output            : output file to store results of spideyX
                
                [{bold}{blue}debug{reset}{bold}{white}]: 
                  -s,  --silent          : display only output to console
                  -vr, --verbose         : increase the verbosity of the output{reset}
        """)
    
def paramfuzzer_help():
    print(f"""    
    [{bold}{blue}MODE{reset}]: {bold}{white}spideyX paramfuzzer mode!{reset}
                
    [{bold}{blue}Usage{reset}]: {bold}{white}
              
            spidey paramfuzzer [options]
              
            Options for paramfuzzer mode:
                
                [{bold}{blue}input{reset}{bold}{white}]: 
                    
                  -site,  --site          : target url for spideyX to paramfuzzer
                  -sties, --sites         : target urls for spideyX to paramfuzzer
                  -w,     --wordlist      : wordlist file that contains parameters for fuzzing
                  stdin/stdout            : target urls for spideyX using stdin
                   
                [{bold}{blue}configurations{reset}{bold}{white}]:
                    
                  -H,  --header           : custom headers & cookies to send in http request for authenticated or custom header parameter fuzzing
                  -X,  --method           : request method for parameter fuzzing (default: get) (choices: "get", "post", "head", "put", "delete", "patch", "trace", "connect", "options")
                  -to , --timeout         : timeout values for each request for parameter fuzzing (default: 15)
                  -px, --proxy            : http proxy url to send request via proxy
                  -dr, --disable-redirect : disable following redirects for each http request
                  -ch, --chunks           : chunks for parameters from wordlist to send at a time (default: 100)
                  -body, --body           : body value to be sent in request and should contain value $pideyx so it will be replaced with chunked params (ex: -body {{"user":"admin", $pideyx}} -fmt json), 
                                            see documentation to use it wisely!
                  -fmt, --format          : specify the body type format to send with request body (choices: json, xml, html), see documentation to use it wisely!
                  --http-raw              : pass a http raw request under single quotes for fuzzing params and see documentation to use it wisely!
                  -ra, --random-agent     : use random user agents for each request in fuzzing params instead of using default user-agent of spideyx

                [{bold}{blue}rate-limits{reset}{bold}{white}]: 
                
                  -c,  --concurrency      : no of concurrency values for concurrent parameter fuzzing (default: 5)
                  -delay, --delay         : specify a delay value between each concurrent requests (default: 0.1)
                  
                [{bold}{blue}output{reset}{bold}{white}]: 
                    
                  -o, --output            : output file to store results of spideyX
                
                [{bold}{blue}debug{reset}{bold}{white}]: 

                  -s,  --silent          : display only output to console
                  -vr, --verbose         : increase the verbosity of the output{reset}
""")
    
def update_help():
    print(f"""  
    [{bold}{blue}MODE{reset}]: {bold}{white}spideyX update mode!{reset}
                
    [{bold}{blue}Usage{reset}]: {bold}{white}
              
            spidey update [options]
              
            Options for update mode:
                
                [{bold}{blue}commands{reset}{bold}{white}]: 
        
                  -sup,  --show-update    : shows latest version updates of spideyX
                  -lt,  --latest          : updates the spideyx to latest version{reset}""")