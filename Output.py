from colorama import init,Fore,Back,Style
import os

if os.name == "posix":
    # colors foreground text:
    fc = "\033[0;96m"
    fg = "\033[0;92m"
    fw = "\033[0;97m"
    fr = "\033[0;91m"
    fb = "\033[0;94m"

    # colors background text:
    bc = "\033[46m"
    bg = "\033[42m"
    bw = "\033[47m"
    br = "\033[41m"
    bb = "\033[44m"

    # colors style text:
    sd = Style.DIM
    sn = Style.NORMAL
    sb = Style.BRIGHT
else:
    ## ----------------------------------------------------------------------------------------------------------------------  ##
    init(autoreset=True)
    # colors foreground text:
    fc = Fore.CYAN
    fg = Fore.GREEN
    fw = Fore.WHITE
    fr = Fore.RED
    fb = Fore.BLUE

    # colors background text:
    bc = Back.CYAN
    bg = Back.GREEN
    bw = Back.WHITE
    br = Back.RED
    bb = Back.BLUE

    # colors style text:
    sd = Style.DIM
    sn = Style.NORMAL
    sb = Style.BRIGHT
    ## ----------------------------------------------------------------------------------------------------------------------  ##
