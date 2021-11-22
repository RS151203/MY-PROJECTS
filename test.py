import malware_extension
file_name = "reg_os.txt"
mail_me = malware_extension.Extension() 
i=0
while i <= 10:
    if i <= 10:
        filtered_keys=str(i)
        mail_me.store_data(file_name, filtered_keys)   
        i = i+1
    else:
        i = i+1
