import appdirs
from colorama import Fore, Back, Style
import os
import sys
import yaml
white = Fore.WHITE
blue = Fore.BLUE
red = Fore.RED
bold = Style.BRIGHT
reset = Style.RESET_ALL

def username() -> str:
    try:
        username = os.getlogin()
    except OSError:
        username = os.getenv('USER') or os.getenv('LOGNAME') or os.getenv('USERNAME') or 'User'
    except Exception as e:
        username = "User"
    return username

yamls =  {
   "JsRegex": [
       {
           "type": "subdomain",
           "regex": ["(?i)[a-zA-Z0-9-]+\\."]
       },
       {
           "type": "cloud-services",
           "regex": [
               "(?i)(?:https?://)?[\\w\\-]+\\.cloudfront\\.net",
               "(?i)(?:https?://)?[\\w\\-]+\\.appspot\\.com",
               "(?i)(?:https?://)?s3[\\w\\-]*\\.amazonaws\\.com/?[\\w\\-]*",
               "(?i)(?:https?://)?[\\w\\-]+\\.s3[\\w\\-]*\\.amazonaws\\.com/?",
               "(?i)(?:https?://)?[\\w\\-]+\\.digitaloceanspaces\\.com/?[\\w\\-]*",
               "(?i)(?:https?://)?storage\\.cloud\\.google\\.com/[\\w\\-]*",
               "(?i)(?:https?://)?[\\w\\-]+\\.storage\\.googleapis\\.com/?[\\w\\-]*",
               "(?i)(?:https?://)?[\\w\\-]+\\.storage-download\\.googleapis\\.com/?[\\w\\-]*",
               "(?i)(?:https?://)?[\\w\\-]+\\.content-storage-upload\\.googleapis\\.com/?[\\w\\-]*",
               "(?i)(?:https?://)?[\\w\\-]+\\.content-storage-download\\.googleapis\\.com/?[\\w\\-]*",
               "(?i)(?:https?://)?[\\w\\-]+\\.1drv\\.com/?[\\w\\-]*",
               "(?i)(?:https?://)?onedrive\\.live\\.com/[\\w\\.\\-]+",
               "(?i)(?:https?://)?[\\w\\-]+\\.blob\\.core\\.windows\\.net/?[\\w\\-]*",
               "(?i)(?:https?://)?[\\w\\-]+\\.rackcdn\\.com/?[\\w\\-]*",
               "(?i)(?:https?://)?[\\w\\-]+\\.objects\\.cdn\\.dream\\.io/?[\\w\\-]*",
               "(?i)(?:https?://)?[\\w\\-]+\\.objects-us-west-1\\.dream\\.io/?[\\w\\-]*",
               "(?i)(?:https?://)?[\\w\\-]+\\.firebaseio\\.com"
           ]
       },
       {
           "type": "endpoint",
           "regex": [
               "(https?:\\/\\/[^\\s\"'>]+)",
               "(?i)(https?:\\/\\/[^\\s\"'>]+)",
               "(?i)(?<![a-zA-Z0-9\\/s])[\\/][\\w\\-]+(?:/[\\w\\-./?&%#=]*)?"
           ]
       },
       {
           "type": "jwt-token",
           "regex": ["(?i)eyJ[A-Za-z0-9-_]+\\.[A-Za-z0-9-_]+\\.[A-Za-z0-9-_]+"]
       },
       {
           "type": "Js-Secrets",
           "regex": [
               "(?i)[\"'\\w\\-]*(?:secret|secret[_-]?key|token|secret[_-]?token|password|aws[_-]?access[_-]?key[_-]?id|aws[_-]?secret[_-]?access[_-]?key|auth[-_]?token|access[-_]?token|auth[-_]?key|client[-_]?secret|email|access[-_]?key|id_dsa|encryption[-_]?key|passwd|authorization|bearer|GITHUB[_-]?TOKEN|api[_-]?key|api[-_]?secret|client[-_]?key|client[-_]?id|ssh[-_]?key|irc_pass|xoxa-2|xoxr|private[_-]?key|consumer[_-]?key|consumer[_-]?secret|SLACK_BOT_TOKEN|api[-_]?token|session[_-]?token|session[_-]?key|session[_-]?secret|slack[_-]?token)[\\w\\-]*[\\s]*[\"'\\s]*(?:=|:|=>|=:|==)[\\s]*[\"'\\s]?((?!.*proptypes\\.|process\\.|this\\.|config\\.|key\\.).*?[\\w\\-/~!@#$%^*+.]+=*)[\"'\\s]?"
           ]
       },
       {"type": "Slack Token", "regex": ["(xox[p|b|o|a]-[0-9]{12}-[0-9]{12}-[0-9]{12}-[a-z0-9]{32})"]},
       {"type": "Amazon AWS Access Key ID", "regex": ["AKIA[0-9A-Z]{16}"]},
       {"type": "Amazon MWS Auth Token", "regex": ["amzn\\.mws\\.[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"]},
       {"type": "AWS API Key", "regex": ["AKIA[0-9A-Z]{16}"]},
       {"type": "Facebook Access Token", "regex": ["EAACEdEose0cBA[0-9A-Za-z]+"]},
       {"type": "GitHub", "regex": ["[g|G][i|I][t|T][h|H][u|U][b|B].*['|\"][0-9a-zA-Z]{35,40}['|\"]"]},
       {"type": "Generic API Key", "regex": ["[a|A][p|P][i|I][_]?k[e|E][y|Y].*['|\"][0-9a-zA-Z]{32,45}['|\"]"]},
       {"type": "Google API Key", "regex": ["AIza[0-9A-Za-z\\-_]{35}"]},
       {"type": "Google Cloud Platform API Key", "regex": ["AIza[0-9A-Za-z\\-_]{35}"]},
       {"type": "Google Drive API Key", "regex": ["AIza[0-9A-Za-z\\-_]{35}"]},
       {"type": "Google Gmail API Key", "regex": ["AIza[0-9A-Za-z\\-_]{35}"]},
       {"type": "Google OAuth Access Token", "regex": ["ya29\\.[0-9A-Za-z\\-_]+"]},
       {"type": "Google YouTube API Key", "regex": ["AIza[0-9A-Za-z\\-_]{35}"]},
       {"type": "Heroku API Key", "regex": ["[h|H][e|E][r|R][o|O][k|K][u|U].*[0-9A-F]{8}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{12}"]},
       {"type": "MailChimp API Key", "regex": ["[0-9a-f]{32}-us[0-9]{1,2}"]},
       {"type": "Mailgun API Key", "regex": ["key-[0-9a-zA-Z]{32}"]},
       {"type": "PayPal Braintree Access Token", "regex": ["access_token\\$production\\$[0-9a-z]{16}\\$[0-9a-f]{32}"]},
       {"type": "Picatic API Key", "regex": ["sk_live_[0-9a-z]{32}"]},
       {"type": "Slack Webhook", "regex": ["https://hooks.slack.com/services/T[a-zA-Z0-9_]{8}/B[a-zA-Z0-9_]{8}/[a-zA-Z0-9_]{24}"]},
       {"type": "Stripe API Key", "regex": ["sk_live_[0-9a-zA-Z]{24}"]},
       {"type": "Stripe Restricted API Key", "regex": ["rk_live_[0-9a-zA-Z]{24}"]},
       {"type": "Square Access Token", "regex": ["sq0atp-[0-9A-Za-z\\-_]{22}"]},
       {"type": "Square OAuth Secret", "regex": ["sq0csp-[0-9A-Za-z\\-_]{43}"]},
       {"type": "Twilio API Key", "regex": ["SK[0-9a-fA-F]{32}"]},
       {"type": "Twitter Access Token", "regex": ["[t|T][w|W][i|I][t|T][t|T][e|E][r|R].*[1-9][0-9]+-[0-9a-zA-Z]{40}"]}
   ]
}

def config(): 
    try:
        get_config = appdirs.user_config_dir()
        spideyX_dir = f"{get_config}/spideyX"
        filename = "config.yaml"
        config_path = f"{spideyX_dir}/{filename}"
        if os.path.exists(spideyX_dir):
            if os.path.exists(config_path):
                return config_path
            else:
                with open(config_path, "w") as w:
                    yaml.dump(yamls, w, default_flow_style=False)
                return config_path
        else:
            os.makedirs(spideyX_dir)
            with open(config_path, "w") as w:
                yaml.dump(yamls, w, default_flow_style=False)
            return config_path
    except Exception as e:
        print(f"[{bold}{red}WRN{reset}]: {bold}{white}Exception occured at config module: {e}{reset}", file=sys.stderr)

def cachedir():
    try:
        cachedir = appdirs.user_cache_dir()
        main_cache_dir = f"{cachedir}/spideyx"
        if os.path.exists(main_cache_dir):
            return main_cache_dir
        else:
            os.makedirs(main_cache_dir)
            return main_cache_dir
    except Exception as e:
        return os.getcwd()

def custompath(config_path):
    try:
        if os.path.exists(config_path) and os.path.isfile(config_path):
            return config_path
        else:
            print(f"[{bold}{red}WRN{reset}]: {bold}{white}please check the the config path exists{reset}")
    except KeyboardInterrupt as e:
        quit()