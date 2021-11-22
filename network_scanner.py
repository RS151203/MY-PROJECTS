import scapy.all as scapy
import argparse# A updated version of class optparse


def parse():
    Parser = argparse.ArgumentParser()  # change OptionParser() to ArgumentParser()
    # change optparse to argparse
    Parser.add_argument("-i", "--ip", dest="ip_range",
                        help="Specify range of ip address or ip address of whose mac you want")
    # instead of add_option use arg_option
    options = Parser.parse_args()  # options is a variable name and can be changed according to me
    return options.ip_range


def scan(ip):
    # scapy.arping(ip)
    # Above class is for use directly since we are going to create our own method commenting it out.
    global number_of_element_in_list
    arp_request = scapy.ARP(pdst=ip)  # arp_request is a variable
    # ARP stands for address resolution protocol
    # pdst states where the packet should go
    # arp_request.pdst=ip
    # above can be shown in highlighted way also
    # print(arp_request.summary())
    # ABOVE IS USED TO SHOW WHAT THE ARP REQUEST IS DOING IN THIS CASE
    # SENDING THE ARP REQUEST FROM ONE IP TO OTHER STATED IP
    # print(arp_request.show())
    # show gives kind of more details than summary
    # scapy.ls(scapy.ARP())
    # ABOVE IS SPECIALLY BUILT IN FUNCTION IN SCAPY WHICH HELPS US TO
    # KNOW ABOUT ANY OTHER CLASS FUNCTIONALITIES IN SCAPY
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    # broadcast is a variable.Ether is a class in scapy
    # which is used to broadcast the arp request created in the entire netowrk
    # print(broadcast.summary())
    # Same as mentioned above
    # print(broadcast.show())
    # Same as mentioned above
    # scapy.ls(scapy.Ether)
    # Same as mentioned above
    arp_broadcast = broadcast / arp_request  # /acts as a kind of aadition of both the packets
    # Same as mentioned above
    # print(arp_broadcast.summary())
    # Same as mentioned above
    # print(arp_broadcast.show())
    # Same as mentioned above
    # answered,unanswered=scapy.srp(arp_broadcast,timeout=1)#timeout says to end it after sending the packets within a time lapse of 1 s
    # srp means send and recieve packets in form of two lists
    # which in these case are stored in answered and unanswered
    # srp has custom ether whereas normal one just send and recieve packet but
    # without a custom ether
    answered_list = scapy.srp(arp_broadcast, timeout=1, verbose=False)[0]
    # since we don't need the unanswered part filtering it out with above steps
    # print(answered_list.summary())
    # In above case both show and summary shows same result
    # print("----------------------------------------------\nIP ADDRESS OF TARGET\tMAC ADDRESS OF TARGET\n- - - - - - - - - - \t- - - - - - - - - - -  ")
    # for each_element in answered_list:
    #     print(each_element[1].psrc,"\t\t",each_element[1].hwsrc,"\n-------------------------------------------")
    # [] accesing elelment in a list should be done by using square brackers
    # psrc stands for ip of target and hwsrc stands for mac address of target
    target_list = []
    for each_element in answered_list:
        target_dict = {"IP address of target": each_element[1].psrc, "MAC address of target": each_element[1].hwsrc}
        target_list.append(target_dict)
        number_of_element_in_list = len((target_list))
    return (target_list, number_of_element_in_list)  # returning len of string so as to create a loop


def output(ip_mac, number_of_client):
    i = 0
    number_of_client = number_of_client - 1  # Remember that when you get string length it calculates it in form of natural
    # number not whole number.That's why decreasing number of client to match list.
    print(
        "----------------------------------------------\nIP ADDRESS OF TARGET\tMAC ADDRESS OF TARGET\n- - - - - - - - - - \t- - - - - - - - - - -  ")
    while i <= number_of_client:
        print(ip_mac[i]["IP address of target"], "\t\t", ip_mac[i]["MAC address of target"])
        i = i + 1


ip_address = parse()
target, number_of_element = scan(ip_address)
output(target, number_of_element)
