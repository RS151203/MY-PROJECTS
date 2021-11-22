import subprocess
import netfilterqueue  # Needs to be installed
import scapy.all as scapy
from scapy.layers import http


def processed_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
# IMP- TO GET TO KNOW WHICH REQ CORRESPOND TO WHICH RESPONSE CHECK PORT NO. AND ACK OF REQ SHOULD = SEQ OF RESPONSE
    if scapy_packet[scapy.TCP].dport == 80:
        if scapy_packet[scapy.TCP].flags == "PA":
            print("------  HTTP REQUEST !!!!!!!")
            print(scapy_packet.show())

    elif scapy_packet[scapy.TCP].sport == 80:

        del scapy_packet[http.HTTPResponse].Content_Encoding
        print("HTTP RESPONSE<<<<--------")
        del scapy_packet[scapy.IP].len
        del scapy_packet[scapy.IP].chksum
        del scapy_packet[scapy.TCP].chksum
        print(scapy_packet.show())
        packet.set_payload(bytes(scapy_packet))
    packet.accept()  # packet.drop can be used for not sending packets.


try:
    subprocess.call(
        "sudo iptables --insert INPUT --jump NFQUEUE --queue-num 0", shell=True)
    # subprocess.call(
    #    "sudo iptables --insert FORWARD --jump NFQUEUE --queue-num 0", shell=True)
    # subprocess.call(
    #    "sudo iptables --insert OUTPUT --jump NFQUEUE --queue-num 0", shell=True)
    subprocess.call(
        "sudo service apache2 start", shell=True)
    # Importing an object from netfilterqueue and assigning it to queue.
    queue = netfilterqueue.NetfilterQueue()
    # In which queue to store packets and next function to carry out operations to modify packet and send it target machine.
    queue.bind(0, processed_packet)
    queue.run()  # To make the desired queue whose number is 0 run.
except(KeyboardInterrupt):
    print("\nDetected Ctrl + C.Clearing queue please wait.")
    subprocess.call("sudo iptables --flush", shell=True)
    subprocess.call(
        "sudo service apache2 stop", shell=True)
