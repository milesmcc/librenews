from colorama import Fore, Style

name = "LibreNews Server"

prefix = Fore.CYAN + "["+name+"] " + Fore.RESET


def say(message):
    print(prefix + Style.DIM + message + Style.RESET_ALL)


def ok(message, detail=""):
    level = Fore.GREEN + "[OK] " + Fore.RESET
    print(prefix + level + Style.BRIGHT + message + Style.RESET_ALL + " " + detail +
          Style.RESET_ALL)


def warn(message, detail=""):
    level = Fore.YELLOW + "[WARN] " + Fore.RESET
    print(prefix + level + Style.BRIGHT + message + Style.RESET_ALL + " " + detail +
          Style.RESET_ALL)


def error(message, detail=""):
    level = Fore.RED + "[ERR] " + Fore.RESET
    print(prefix + level + Style.BRIGHT + message + Style.RESET_ALL + " " + detail +
          Style.RESET_ALL)
