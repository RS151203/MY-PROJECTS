import subprocess
import re
def only_mac_address():
    #eth0 = subprocess.check_output("ifconfig eth0", shell=True)#Getting output of ifconfig rth0 and storing it in eth0
    #mac_initial = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(eth0))#it is imp to convert eth0 which is  an object to string
    #storing value of result obtained through regx class in mac_initial
    eth0 = subprocess.getoutput("ifconfig eth0")
    mac_initial = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", eth0)
    return mac_initial.group(0)#.group(0) is essential or shows kinda different result
mac_address=only_mac_address()
print("Mac address process for reverting it back to normal.")
subprocess.call("sudo ifconfig eth0 down", shell=True)
subprocess.call("sudo ifconfig eth0 hw ether 08:00:27:d5:88:a8 ", shell=True)
subprocess.call("sudo ifconfig eth0 up", shell=True)
print(mac_address,"Mac address back to normal.")