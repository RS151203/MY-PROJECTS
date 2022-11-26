import subprocess
import sys
import os
import operator
from datetime import date
from zipfile import ZipFile

incrementer=0

final_result="<html>\n\t<head>\n\t\t<title>APACHE AUDIT REPORT</title>\n\n\t\t<style>\n\t\t\ttable,tr,td{text-align:center;padding:5px;border:solid 2px}\n\t\t</style>\n\t</head>\n<body>\n\n<h1 style=text-align:center>AUDIT REPORT FOR APACHE.</h1>\n<table>\n\n\t<tr>\n\t\t<th>Sr No.</th>\n\t\t<th>Checking</th>\n\t\t<th>Ideal Condition</th>\n\t\t<th>Your System Condition</th>\n\t</tr>"


def check_whether_enabled(operand1,operator,operand2,text_for_part1):
    global final_result
    global incrementer
    incrementer+=1

    print(f"\n---------->Checking {text_for_part1} is enabled or not<----------")
    try:
        operand1=operand1.replace("\n","")
    except(Exception):
        pass

    final_result=final_result+f"\n\t<tr>\n\t\t<td>{incrementer}</td>"
    final_result=final_result+f"\n\t\t<td>{text_for_part1}</td>\n\t\t<td>Enabled</td>"
    if  operator(operand1,operand2):
        final_result=final_result+"\n\t\t<td>Enabled</td>\n\t</tr>"
    else:
        final_result=final_result+"\n\t\t<td style=background-color:red;color:white>Disabled</td>\n\t</tr>"

def check_whether_disabled(operand1,operator,operand2,text_for_part1):
    global final_result
    global incrementer
    incrementer+=1

    print(f"\n---------->Checking {text_for_part1} is disabled or not<----------")
    try:
        operand1=operand1.replace("\n","")
    except(Exception):
        pass

    final_result=final_result+f"\n\t<tr>\n\t\t<td>{incrementer}</td>"
    final_result=final_result+f"\n\t\t<td>{text_for_part1}</td>\n\t\t<td>Disabled</td>"
    if  operator(operand1,operand2):
        final_result=final_result+"\n\t\t<td>Disabled</td>\n\t</tr>"
    else:
        final_result=final_result+"\n\t\t<td style=background-color:red;color:white>Enabled</td>\n\t</tr>"

def check_config_file(httpd_conf,apache_modules):
    
    global final_result
    
    log_config=subprocess.run(f"grep log_config {apache_modules}",capture_output=True,shell=True,universal_newlines=True)
    
    check_whether_enabled(log_config.stdout,operator.ne,"","Status of log_config Module")

    web_dav=subprocess.run(f"grep dav_ {apache_modules}",capture_output=True,shell=True,universal_newlines=True)

    check_whether_disabled(web_dav.stdout,operator.eq,"","Status of WebDav Module")

    status=subprocess.run(f"grep status_module {apache_modules}",capture_output=True,shell=True,universal_newlines=True)

    check_whether_disabled(status.stdout,operator.eq,"","Status of Status Module")

    auto_index=subprocess.run(f"grep auto_index {apache_modules}",capture_output=True,shell=True,universal_newlines=True)

    check_whether_disabled(auto_index.stdout,operator.eq,"","Status of AutoIndex Module")

    proxy_module=subprocess.run(f"grep proxy {apache_modules}",capture_output=True,shell=True,universal_newlines=True)

    check_whether_disabled(auto_index.stdout,operator.eq,"","Status of Proxy Module")

    user_directory=subprocess.run(f"grep user_dir {apache_modules}",capture_output=True,shell=True,universal_newlines=True)

    check_whether_disabled(auto_index.stdout,operator.eq,"","Status of UserDirectory Module")

    info=subprocess.run(f"grep info_module {apache_modules}",capture_output=True,shell=True,universal_newlines=True)

    check_whether_disabled(info.stdout,operator.eq,"","Status of Info Module")

    auth_basic_module=subprocess.run(f"grep auth_basic_module {apache_modules}",capture_output=True,shell=True,universal_newlines=True)

    check_whether_disabled(info.stdout,operator.eq,"","Status of Basic HTTP Authentication Module")

    auth_basic_module=subprocess.run(f"grep auth_digest_module {apache_modules}",capture_output=True,shell=True,universal_newlines=True)

    check_whether_disabled(info.stdout,operator.eq,"","Status of Basic HTTP Digest Module")

    mod_security=subprocess.run(f"grep security1_module {apache_modules}",capture_output=True,shell=True,universal_newlines=True)

    check_whether_enabled(mod_security.stdout,operator.ne,"","Status of ModSecurity Module")

    ssl_module=subprocess.run(f"grep ssl_module {apache_modules}",capture_output=True,shell=True,universal_newlines=True)

    check_whether_enabled(ssl_module.stdout,operator.ne,"","Status of SSL Module")

    nss_module=subprocess.run(f"grep nss_module {apache_modules}",capture_output=True,shell=True,universal_newlines=True)

    check_whether_enabled(nss_module.stdout,operator.ne,"","Status of NSS Module")

    reqtimeout_module=subprocess.run(f"grep reqtimeout_module {apache_modules}",capture_output=True,shell=True,universal_newlines=True)

    check_whether_enabled(mod_security.stdout,operator.ne,"","Status of ReqTimeOut Module")

    user_name=subprocess.run("grep -i '^User' " + httpd_conf + " | awk '{print $2}'",capture_output=True,shell=True,universal_newlines=True)

    user_name=user_name.stdout.replace("\n","")

    check_whether_enabled(user_name,operator.ne,"","Status for seperate user for Apache")

    group_name=subprocess.run("grep -i '^Group' " + httpd_conf + " | awk '{print $2}'",capture_output=True,shell=True,universal_newlines=True)

    group_name=group_name.stdout.replace("\n","")

    check_whether_enabled(group_name,operator.ne,"","Status for seperate group for Apache")

    os_root_dir=subprocess.run("perl -ne 'print if /^ *<Directory *\//i .. /<\/Directory/i' " + httpd_conf,shell=True,capture_output=True,universal_newlines=True)

    os_root_dir_allow_deny=(operator.or_((operator.contains(os_root_dir.stdout,"Allow ")),(operator.contains(os_root_dir.stdout,"Deny "))))

    os_root_dir_require=(operator.not_(operator.contains(os_root_dir.stdout,"Require all denied")))

    check_whether_disabled(operator.or_(os_root_dir_allow_deny,os_root_dir_require),operator.eq,False,"Status of OS Root Directory access")

    check_whether_enabled(operator.or_(operator.contains(os_root_dir.stdout,"AllowOverride none"),(operator.contains(os_root_dir.stdout,"AllowOverride None"))),operator.eq,True,"Status of whether command which prevents overriding of root directory")

    check_whether_disabled(operator.contains(os_root_dir.stdout,"AllowOverrideList"),operator.eq,False,"Status of whether root directory can be overrided")

    all_dir_override=subprocess.run("grep -i -c '  AllowOverride none' " + httpd_conf,shell=True,capture_output=True,universal_newlines=True)

    if all_dir_override.stdout=="":

        check_whether_enabled(all_dir_override.stdout,operator.ne,"","Status of whether directive which prevents overriding on directories")

    else:
        check_whether_enabled(int(all_dir_override.stdout),operator.gt,0,"Status of whether directive which prevents overriding on directories")

    all_dir_overridelist=subprocess.run("grep -i -c '    AllowOverrideList ' " + httpd_conf,shell=True,capture_output=True,universal_newlines=True)

    if all_dir_overridelist.stdout=="":

        check_whether_disabled(all_dir_overridelist.stdout,operator.eq,"","Status of whether directories can be overrided")

    else:

        check_whether_disabled(int(all_dir_overridelist.stdout),operator.eq,0,"Status of whether directories can be overrided")

    options_directive_total=subprocess.run("perl -ne 'print if /^ *<Directory */i .. /<\/Directory/i' " + httpd_conf + " | grep -ci '    Options'",shell=True,capture_output=True,universal_newlines=True)

    options_directive_none_enabled=subprocess.run("perl -ne 'print if /^ *<Directory */i .. /<\/Directory/i' " + httpd_conf + " | grep -ci '    Options None'",shell=True,capture_output=True,universal_newlines=True)

    if options_directive_total.stdout=="" or options_directive_none_enabled.stdout=="":

        check_whether_disabled(options_directive_total.stdout,operator.eq,"","status of whether options directive contains values other  than none")

    else:

        check_whether_disabled(int(options_directive_total.stdout),operator.eq,int(options_directive_none_enabled.stdout),"status of whether options directive contains values other  than none")

    other_handler_configurations=subprocess.run("grep -i '^<Location ' " + httpd_conf,shell=True,capture_output=True,universal_newlines=True)

    check_whether_disabled(other_handler_configurations.stdout,operator.eq,"","Status for other handler configurations")

    other_configuration_files=subprocess.run("grep -i '^<IfModule ' " + httpd_conf,shell=True,capture_output=True,universal_newlines=True)

    check_whether_disabled(other_configuration_files.stdout,operator.eq,"","Status for other configuration files")

    cgi_location=subprocess.run("""grep -i '    Script' """ + httpd_conf +""" | cut -d '"' -f 2""",shell=True,capture_output=True,universal_newlines=True)

    working_dir_curr=os.getcwd()

    try:
        os.chdir(cgi_location.stdout.replace("\n",""))

        cgi_file=subprocess.run("ls",shell=True,capture_output=True,universal_newlines=True)

        check_whether_disabled(cgi_file.stdout,operator.eq,"","Status for cgi files(Enable only required files)")

    except(Exception):
        final_result=f"{final_result}\n<br>No CGI-BIN IS CREATED TO STORE CGI FILES<br>\n"
        pass

    os.chdir(working_dir_curr)

    log_level=subprocess.run("grep -i '^LogLevel '  " + httpd_conf,shell=True,capture_output=True,universal_newlines=True)

    check_whether_enabled(log_level.stdout,operator.eq,"LogLevel notice","Status of log_level notice option(notice provides extra secutity over other options not mandatory can slow down performance))")

    error_log=subprocess.run("grep -i '^ErrorLog' " + httpd_conf,shell=True,capture_output=True,universal_newlines=True)

    check_whether_enabled(error_log.stdout,operator.ne,"","Status of error_log")

    error_log_syslog=subprocess.run("""grep -i '^ErrorLog "syslog:' """ + httpd_conf,shell=True,capture_output=True,universal_newlines=True)

    check_whether_enabled(error_log_syslog.stdout,operator.ne,"","Status of error_log with syslog facility")

    log_format=subprocess.run("""grep -i "    LogFormat.*combined$" """ + httpd_conf,shell=True,capture_output=True,universal_newlines=True)

    custom_log=subprocess.run("""grep -i "    CustomLog" """ + httpd_conf,shell=True,capture_output=True,universal_newlines=True)

    if custom_log.stdout.replace("\n","") == '    CustomLog "logs/access_log" combined':
        check_whether_enabled(operator.and_(operator.eq(log_format.stdout.replace("\n",""),'    LogFormat "%h %l %u %t \\"%r\\" %>s %b \\"%{Referer}i\\" \\"%{User-Agent}i\\"" combined'),operator.eq(custom_log.stdout.replace("\n",""),"""    CustomLog "logs/access_log" combined""")),operator.and_,True,"Status of log format securty")

    elif custom_log.stdout.replace("\n","") =='    CustomLog log/access_log "%h %l %u %t \\"%r\\" %>s %b \\"%{Referer}i\\"\\"%{User- agent}i\\""':
       check_whether_enabled(custom_log.stdout,operator.eq,'    CustomLog log/access_log "%h %l %u %t \\"%r\\" %>s %b \\"%{Referer}i\\"\\"%{User- agent}i\\""',"Status of log format securty")

    else:
        pass

    server_tokens=subprocess.run("grep -i '^ServerTokens ' " + httpd_conf,shell=True,capture_output=True,universal_newlines=True)

    check_whether_enabled(server_tokens.stdout,operator.eq,"ServerTokens Prod","Status of server_tokens directive")

    server_signature=subprocess.run("grep -i ^ServerSignature " + httpd_conf,shell=True,capture_output=True,universal_newlines=True)

    check_whether_enabled(server_signature.stdout,operator.eq,"ServerSignature Off","Status of server_signature directive")

    file_etag=subprocess.run("grep -i '^FileETag ' " + httpd_conf,shell=True,capture_output=True,universal_newlines=True)

    check_whether_disabled(operator.or_(operator.contains(file_etag.stdout,"All"),operator.contains(file_etag.stdout,"INode")),operator.ne,True,"Status of FileETag directive with vulnerable options")

    timeout=subprocess.run("grep -i '^Timeout ' " + httpd_conf + " | awk '{print $2}'",shell=True,capture_output=True,universal_newlines=True)

    if timeout.stdout=="":

        check_whether_enabled(timeout.stdout,operator.ne,"","Status of timeout directive maximum seconds for timeout")

    else:

        check_whether_enabled(int(timeout.stdout),operator.le,10,"Status of timeout directive maximum seconds for timeout")

    keep_alive=subprocess.run("grep -i '^KeepAlive ' " + httpd_conf,shell=True,capture_output=True,universal_newlines=True)

    check_whether_enabled(operator.or_(operator.eq(keep_alive.stdout.replace("\n",""),"KeepAlive On"),operator.eq(keep_alive.stdout,"")),operator.ne,False,"Status of KeepAlive directive")

    max_keep_alive_requests=subprocess.run("grep -i '^MaxKeepAliveRequests ' " + httpd_conf + " | awk '{print $2}'",shell=True,capture_output=True,universal_newlines=True)

    if max_keep_alive_requests.stdout=="":

        check_whether_enabled(max_keep_alive_requests.stdout,operator.eq,"","Status of MaxKeepAliveRequests requests to respond to")

    else:

        check_whether_enabled(int(max_keep_alive_requests.stdout),operator.ge,100,"Status of MaxKeepAliveRequests requests to respond to")

    keep_alive_timeout=subprocess.run("grep -i '^KeepAliveTimeout ' " + httpd_conf + " | awk '{print $2}'",shell=True,capture_output=True,universal_newlines=True)

    if keep_alive_timeout.stdout=="":

        check_whether_enabled(keep_alive_timeout.stdout,operator.eq,"","Status of KeepAliveTimeout directive")

    else:

        check_whether_enabled(int(keep_alive_timeout.stdout),operator.le,15,"Status of KeepAliveTimeout directive")

    limit_request_line=subprocess.run("grep -i 'LimitRequestLine ' " + httpd_conf + " | awk '{print $2}'",shell=True,capture_output=True,universal_newlines=True)

    if limit_request_line.stdout=="":

        check_whether_enabled(limit_request_line.stdout,operator.ne,"","Status of LimitRequestLine directive")

    else:

        check_whether_enabled(int(limit_request_line.stdout),operator.le,512,"Status of LimitRequestLine directive")

    limit_request_fields=subprocess.run("grep 'LimitRequestFields ' " + httpd_conf + " | awk '{print $2}'",shell=True,capture_output=True,universal_newlines=True)

    if limit_request_fields.stdout=="":

        check_whether_enabled(limit_request_fields.stdout,operator.ne,"","Status of LimitRequestFields directive")

    else:

        check_whether_enabled(int(limit_request_fields.stdout),operator.le,100,"Status of LimitRequestFields directive")

    limit_request_field_size=subprocess.run("grep -i 'LimitRequestFieldSize ' " + httpd_conf + " | awk '{print $2}'",shell=True,capture_output=True,universal_newlines=True)

    if limit_request_field_size.stdout=="":

        check_whether_enabled(limit_request_field_size.stdout,operator.ne,"","Status of LimitRequestFieldSize directive")

    else:

        check_whether_enabled(int(limit_request_field_size.stdout),operator.le,1024,"Status of LimitRequestFieldSize directive")

    limit_request_body=subprocess.run("grep -i 'LimitRequestBody ' " + httpd_conf + " | awk '{print $2}'",shell=True,capture_output=True,universal_newlines=True)

    if limit_request_body.stdout=="":

        check_whether_enabled(limit_request_field_size.stdout,operator.ne,"","Status of LimitRequestBody directive")

    else:

        check_whether_enabled(int(limit_request_field_size.stdout),operator.le,102400,"Status of LimitRequestBody directive")


    final_result=final_result + "\n</table>\n<br>SSL Module implementation needs to be checked manually.<br>\n\t<body>\n\t</html>"


zip_dir=input("Enter absolute directory location where zip files are stored:")

try:
    os.chdir(zip_dir)
except:
    print("Entered directory doesn't exist please check for typos:(")
    sys.exit()

zips=input("Enter zip files with .zip extension and space in between each of them:")
zips_list=zips.split(" ")

for zipped in zips_list:
    
    with ZipFile(zipped,'r') as zip_file:
        zipped_file=zipped.replace(".zip","")

        os.mkdir(zipped_file)

        os.chdir(zipped_file)

        zip_file.extractall()

        list_of_files=os.listdir()

        for file in list_of_files:
            if file.endswith(".conf")==True:
                httpd_conf=file
            else:
                apache_modules=file

        check_config_file(httpd_conf,apache_modules)

        os.chdir(zip_dir + "/" + zipped_file)

        with open(zipped_file + ".html","w") as audit:
            audit.write(final_result)

        os.chdir(zip_dir)
