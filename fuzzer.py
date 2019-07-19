#########################################################################
#                       Developed by Chaitanya Dande                    #
#########################################################################

import whois
import sys
import requests
import mechanize
import mechanicalsoup
import re
import os
import json
from bs4 import BeautifulSoup
import builtwith
import socket
import sys
import dns.resolver
import nmap

print("\033[1;32m-----------------------------\033[1;m")
print("\033[1;32mWelcome to OWASP Vuln Fuzzer\033[1;m")
print("\033[1;32m-----------------------------\033[1;m")
print("1. Information Gathering")
print("2. Cross Site Scripting XSS")
print("3. Sql Injection")
print("4. Quit")
print("\033[1;32m-----------------------------\033[1;m")
choice = input('Enter your choice [1-4] :')
print("\033[1;32m-----------------------------\033[1;m")
choice = int(choice)

if choice == 1:
    url=raw_input("Website URL:")
    req = requests.get(url)
    print("\033[1;32m---------------------------------------------\033[1;m")
    print("Starting Information Gathering , Connecting to the URL..!")
    print("\033[1;32m---------------------------------------------\033[1;m")
    print("Status Code:",req.status_code)
spl=req.headers
    print("\033[1;32m---------------------------------------------\033[1;m")
    print("\033[1;32mHTTP Headers\033[1;m")
    print("\033[1;32m---------------------------------------------\033[1;m")
    for i, j in spl.items():
        print(i+':' +j)
    print("Encoding:",req.encoding)
    print("\033[1;32m---------------------------------------------\033[1;m")
    print("\033[1;32mForms Info\033[1;m")
    print("\033[1;32m---------------------------------------------\033[1;m")
    parseHTML = BeautifulSoup(req.content, 'html.parser')
    print(parseHTML.find_all('form'))
    print("\033[1;32m---------------------------------------------\033[1;m")
    print("\033[1;32mAll URLs/Redirections\033[1;m")
    print("\033[1;32m---------------------------------------------\033[1;m")
    for links in parseHTML.find_all('a'):
        print(links.get('href'))
         #print((links.get('href')).count())
    print("\033[1;32m---------------------------------------------\033[1;m")
    print("\033[1;32mTechnologies Used\033[1;m")
    print("\033[1;32m---------------------------------------------\033[1;m")
    tech=builtwith.parse(url)
       #tech.encode('utf-8').strip()
    for key,value in tech.items():
        print(key+":",",".join(value))
    print("\033[1;32m---------------------------------------------\033[1;m")
    print("\033[1;32mDNS/Whois Information\033[1;m")
    print("\033[1;32m---------------------------------------------\033[1;m")
    s = whois.whois(url)
    print(s)
    print("Expiration Date:",s.expiration_date)

    #hostname = socket.gethostname()
    #print(socket.gethostbyname(hostname))
    print("\033[1;32m---------------------------------------------\033[1;m")
    print("\033[1;32mRobots.txt\033[1;m")
    print("\033[1;32m---------------------------------------------\033[1;m")
    robo=requests.get(url+"/robots.txt")
    file=robo.text
    print(file)
    print("\033[1;32m---------------------------------------------\033[1;m")
    print("\033[1;32mSSL Ciphers Suites\033[1;m")
    print("\033[1;32m---------------------------------------------\033[1;m") nm="nmap -v --script ssl-enum-ciphers bigsmartdeals.com"
    print(os.system(nm))
    #print()
    """qtype in ['A','AAAA','CNAME','MX','NS']:
    res = dns.resolver.query(url,qtype,raise_on_no_answer=False)
    for serv in res:
    print(serv)"""
elif choice == 2:
        print("---------------------------------------------")
        print("\nStarting XSS Checker")
        print("---------------------------------------------")
        url = raw_input("Website URL:")
        req=requests.get(url)
        #browser = mechanicalsoup.StatefulBrowser()
        #browser.get_current_page()
        parseHTML=BeautifulSoup(req.text,'html.parser')
        #browser.select_form('form[method="post"]')
        print(parseHTML.find_all('form'))
        #browser.get_current_form().print_summary()
        htmlform=parseHTML.form
        formname=htmlform['id']
        print("Form Name:"+formname)
        inputs=htmlform.find_all('input')
        inputfields=[]
        for fields in inputs:
                if fields.has_attr('name'):
                        inputfields.append(fields['name'])
        print(inputfields)
        brobj=mechanize.Browser()
        brobj.open(url)
        brobj.form=list(brobj.forms())[0]
        print(brobj.form)
        print("\033[1;32m---------------------------------------------\033[1;m")
        print("Checking Forms")
        print("\033[1;32m---------------------------------------------\033[1;m")
        payload='&lt;script&gt;alert("vulnerable");&lt;/script&gt;'
        brobj.form[inputfields[0]] = payload
        for i in range(1,len(inputfields)):
                brobj.form[inputfields[i]] = "Any text for filling other fields incase of multiple fields"
        brobj.submit()
        finalResult = brobj.response().read()
 if finalResult.find('&lt;script&gt;')>=0:
                print("\033[1;32m---------------------------------------------\033[1;m")
                print("Application is XSS vulnerable")
                print("\033[1;32m---------------------------------------------\033[1;m")
        else:
                print("No XSS Vulnerability Found in Forms")
        print("\033[1;32m---------------------------------------------\033[1;m")
        print("Checking URL")
        print("\033[1;32m---------------------------------------------\033[1;m")
        fname = "xsspayloads.txt"
        with open(fname) as f:
                content = f.readlines()
        payloads = [x.strip() for x in content]
        vuln = []
        for payload in payloads:
                payload = payload
                xss_url = url+"/"+payload
                print(xss_url)
                r = requests.get(xss_url)
                if payload.lower() in r.text.lower():
                        print("\033[1;32m Vulnerable: " + payload)
                        if(payload not in vuln):
                                vuln.append(payload)
                else:
                        print("Not vulnerable!")
        print("--------------------\nAvailable Payloads:")
        print('\n'.join(vuln))
elif choice == 3:
         print("\nStarting Sql Injection Fuzzer")
elif choice == 4:
         print("\nHave a Great Day. Bye Exiting..!")
else:
        print("Invalid Selection, Try your luck again")
