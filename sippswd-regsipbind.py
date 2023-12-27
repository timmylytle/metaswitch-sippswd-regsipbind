# sippswd_regsipbind.py
# This tool pulls SIP password and current UA strings from Registerd SIP bindings
# to operate preload TNs in target_list.csv, run scripts, output will be printed to output.csv in the same directory
#
# Author: Timothy Lytle
# created on: 2020/02/03

#import libraries
import sys
import csv
import requests
from bs4 import BeautifulSoup as bs
import getpass

# define variables
username = input("MetaViewWeb Username: ")
password = getpass.getpass()
mvw_ip = input("MetaViewWeb Address: ")
mvw_port = input("MetaViewWeb port: ")
switchversion = input("MetaViewWeb version (example: 9.3): ")
target_list = input("Path to target list file: ")
url="http://{}:{}/mvweb/services/ShService".format(mvw_ip, mvw_port)
headers = {'content-type': 'text/xml'}

#create output file, direct all print funcitons to file
file = open('output.csv','a')
sys.stdout = file

#write headers of output_CSV
print('DN;BGName;Pass_state;SIPPassword;Reg_UA1;Reg_UA2;Reg_UA3;Reg_UA4') 

def get_pswd_rsb():
    body_base = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:sh="http://www.metaswitch.com/srb/soap/sh"> 
    <soapenv:Header/> 
    <soapenv:Body> 
        <sh:ShPull> 
            <sh:UserIdentity>{}</sh:UserIdentity>
            <sh:DataReference>0</sh:DataReference> 
            <sh:ServiceIndication>Meta_Subscriber_BaseInformation</sh:ServiceIndication>
            <sh:OriginHost>?clientVersion={}&amp;ignoreSequenceNumber=true</sh:OriginHost>
        </sh:ShPull> 
    </soapenv:Body>
    </soapenv:Envelope>""".format(sub_dn, switchversion)
    body_rsb = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:sh="http://www.metaswitch.com/srb/soap/sh"> 
        <soapenv:Header/> 
        <soapenv:Body> 
            <sh:ShPull> 
                <sh:UserIdentity>{}</sh:UserIdentity>
                <sh:DataReference>0</sh:DataReference> 
                <sh:ServiceIndication>Meta_Subscriber_RegisteredSIPBindingsList</sh:ServiceIndication>
                <sh:OriginHost>?clientVersion={}&amp;ignoreSequenceNumber=true</sh:OriginHost>
            </sh:ShPull> 
        </soapenv:Body>
    </soapenv:Envelope>""".format(sub_dn, switchversion)

    base_r = requests.post(url,data=body_base,headers=headers, auth=(username, password))
    base_soup = bs(base_r.content, 'xml')

    rsb_r = requests.post(url,data=body_rsb,headers=headers, auth=(username, password))
    rsb_soup = bs(rsb_r.content, 'xml')

    output = [sub_dn]
    # Define bad strings for password, these will be searched in the string
    bad_pass1 = 'password'
    bad_pass2 = '1234'
    bad_pass3 = '4321'
        
    for sippswd in base_soup.findAll('SIPPassword'):
        pswd = sippswd.text
        if sub_dn in pswd:
            pswd_state = 'bad pass' 
        elif bad_pass1 in pswd:
            pswd_state = 'bad pass'
        elif bad_pass2 in pswd:
            pswd_state = 'bad pass'
        elif bad_pass3 in pswd:
            pswd_state = 'bad pass'
        else:
            pswd_state = 'ok'
        output.insert(2,pswd_state)
        output.insert(3, pswd)

    for bgname in base_soup.findAll('BusinessGroupName'):
        bg = bgname.text
        output.insert(1, bg)        

    for rsb in rsb_soup.findAll('RegisteredSIPBinding'):
        ua = rsb.find('UserAgentInformation').text.strip()
        output.insert(4, ua)

    print(';'.join(output))
           

#open list of subs, and start loop
# with open('target_list.csv','r') as csv_file:
with open(target_list,'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader)
    for line in csv_reader:
        sub_dn = line[0]
        get_pswd_rsb()
        
file.close()