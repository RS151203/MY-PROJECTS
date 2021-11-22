#!/usr/bin/env python
import subprocess  # A class
import optparse  # A class
import re  # A class used for filtering desired result


def parser():
    Parser = optparse.OptionParser()  # let it be Parser or RS it doesn't make a difference stands for a name
    # optparse(option for parser to create options for us,
    Parser.add_option("-m", "--mac", dest="mac_address", help="Use for entering new mac address.")
    # add_option to create option with name inn which parser is stored in this case Parser.
    # First we state the type of convention to use to access options in this case -m & --mac for mac address
    # dest shows us what that options are really for.
    # complete information about given convention is provided inside help by using --help
    (options, arguments) = Parser.parse_args()
    # Parser.parse_args() is a method that will pass our arguments first into option then too arguments.
    # options and arguments are variable can be replaced by anything else
    return options.mac_address  # dest=mac_address should be the same as of options.mac_address
    # mac_address=options.mac_address #giving the mac address received after executing parser commands to mac_address variable.
    # since there is no use of arguments in this case hence not created arguments.mac_address
    # Remember both options and arguments are completely variables and can be changed according to my needs.
    # AS CREATED FUNCTION PASSING DIRECTLY options.mac_address value to it.


def mac_changer(mac_address):  # intaking value as mac address from declaration of function
    subprocess.call("sudo ifconfig eth0 down", shell=True)
    subprocess.call("sudo ifconfig eth0 hw ether " + mac_address,
                    shell=True)  # It is important to use + and not , before mac_address
    subprocess.call("sudo ifconfig eth0 up", shell=True)


def only_mac_address():
    # eth0 = subprocess.check_output("ifconfig eth0", shell=True)#Getting output of ifconfig rth0 and storing it in eth0
    # mac_initial = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(eth0))#it is imp to convert eth0 which is  an object to string
    # storing value of result obtained through regx class in mac_initial
    eth0 = subprocess.getoutput("ifconfig eth0")
    mac_initial = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", eth0)
    return mac_initial.group(0)  # .group(0) is essential or shows kinda different result


print("Mac address initially:", only_mac_address())
print(
    "$IF ANY ISSUE OCCURS REMEMBER EXECUTE THE COMMAND IN THE WAY python3 mac_changer.py --mac OR -m FOLLOWED BY MAC ADDRESS AND EXECUTE WITH python3 mac_changer.py --help TO KNOW WHAT EACH COMMADND DOES AND TO KNOW THEIR FUNCTIONALITY$")
options = parser()  # options is a variable name
mac_changer(options)  # declaring function and passing mac address via parser(function)
print("Mac address finally:", only_mac_address())
