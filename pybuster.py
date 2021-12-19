# Importing Modules
import requests
import argparse
import os
import time
import colorama
from colorama import Fore

# Constants & Variables
website_url=""
wordlist_words=[]
recur = False

# Functions
def print_banner():
    banner = """\
       ,-~~-.___.              ____        ____             __        
      / |  x     \            / __ \__  __/ __ )__  _______/ /____  _____
     (  )        0           / /_/ / / / / __  / / / / ___/ __/ _ \/ ___/
      \_/-, ,----'  ____    / ____/ /_/ / /_/ / /_/ (__  ) /_/  __/ /    
         ====      ||   \_ /_/    \__, /_____/\__,_/____/\__/\___/_/ 
        /  \-'~;   ||     |      /____/                                         
       /  __/~| ...||__/|-"   Directory Busting Tool for Web-App Pentester
     =(  _____||________|                 ~anukulpandey~
    """
    print(Fore.WHITE + banner)

print_banner()
def validate_file(l):
    if not os.path.exists(l):
        raise argparse.ArgumentTypeError(Fore.RED + "{0} does not exist".format(l))
    else:
        with open(l) as file:
            wl = file.read()
            print(Fore.YELLOW + f'[!] Wordlist Status : {Fore.BLUE} Generating')
            time.sleep(2)
            for elems in wl.splitlines():
                wordlist_words.append(elems)
            print(Fore.YELLOW + f'[!] Wordlist Status :{Fore.GREEN} Added {wordlist_words.__len__()} words from {l}')
            
def validate_url(u):
    try:
        res = requests.get(u)
        print(f'{Fore.YELLOW}[!] URL :{Fore.BLUE} {u}')
        print(f"{Fore.YELLOW}[!] URL Status :{Fore.GREEN} VALID\n")
        time.sleep(3)
        directory_buster(u,wordlist_words)

    except Exception as e:
        print(Fore.RED+'[-] URL Status: INVALID')

def directory_buster(website_url,wordlist_words):
        print(Fore.GREEN+'\t\t[+] URL ')
        print(Fore.GREEN+'\t\t[+] Wordlist\n')
        if(website_url[-1]=='/'):
            website_url[-1]=''
        print(Fore.CYAN+'Starting Directory Busting...')
        print(Fore.WHITE+'-'*58)
        print(Fore.WHITE+'\tSTATUS CODE\t\tVISIT\t\tPAYLOAD')
        print(Fore.WHITE+'-'*58)
        for elems in wordlist_words:
            try:
                res=requests.get(f'{website_url}/{elems}')
                print(f'Checking {elems}',end="\r")
                if(res.status_code!=404):
                    if(res.status_code==200):
                        print(Fore.GREEN+f'[{res.status_code}]     {Fore.WHITE}{website_url}/{elems}\t\{elems}')
                        if(recur):
                            directory_buster(f'{website_url}/{elems}',wordlist_words)
                    else:

                        print(Fore.YELLOW+f'[{res.status_code}]     {Fore.WHITE}{website_url}/{elems}')
            except Exception as e:
                pass
# Flags
parser = argparse.ArgumentParser()

parser.add_argument("-w", "--wordlist", dest="filename", required=True, type=validate_file,help="provide location to wordlist")

parser.add_argument("-u", "--url", dest="url", required=True, type=validate_url,help="enter the url for directory busting")

parser.add_argument("-r", "--recursive", dest="url", required=False, type=validate_url,help="search for directories recursively")

args = parser.parse_args()
