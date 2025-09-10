import requests
from datetime import datetime
from colorama import Fore, Style, init

init(autoreset=True)

ascii_art = r"""


    ___    __   _       _                   _              _        ___   __  
  ,"___".  LJ  FJ_     FJ___     _    _    FJ___          /.\      F _ ", FJ  
  FJ---L]     J  _|   J  __ `.  J |  | L  J  __ J        //_\\    J `-' |J  L 
 J |  [""L FJ | |-'   | |--| |  | |  | |  | |--| |      / ___ \   |  __/F|  | 
 | \___] |J  LF |__-. F L  J J  F L__J J  F L__J J     / L___J \  F |__/ F  J 
 J\_____/FJ__L\_____/J__L  J__LJ\____,__LJ__,____/L   J__L   J__LJ__|   J____L
  J_____F |__|J_____F|__L  J__| J____,__FJ__,____F    |__L   J__||__L   |____|
                                                                              

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""


def get_rate_limit():
    try:
        response = requests.get("https://api.github.com/rate_limit")
        response.raise_for_status()
    except requests.RequestException as e:
        print(Fore.RED + "[ERROR] Failed to connect to GitHub API:", e)
        return

    data = response.json()
    core = data['resources']['core']
    
    remaining = core['remaining']
    used = core['used']
    limit = core['limit']
    reset = core['reset']

    reset_time = datetime.fromtimestamp(reset).strftime('%Y-%m-%d %H:%M:%S')

    status = f"{Fore.GREEN}Worked ✅" if remaining > 0 else f"{Fore.RED}Blocked ❌"

    print(Fore.CYAN + ascii_art)
    print(Fore.YELLOW + f"Used Requests     : {used}")
    print(Fore.YELLOW + f"Remaining Requests: {remaining}")
    print(Fore.YELLOW + f"Limit             : {limit}")
    print(Fore.YELLOW + f"Reset Time        : {reset_time}")
    print(Fore.YELLOW + f"Status            : {status}")

if __name__ == '__main__':
    get_rate_limit()

input("")