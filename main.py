#!/usr/bin/python3
import json
from base64 import b64encode
from configparser import RawConfigParser 
import requests

config_file = "project.props"
cred_file = "cred.props"
line_seperator = "-"*80+"\n"
def get_api_url():
    parser = RawConfigParser()
    parser.read(config_file)
    url = parser.get('config', 'api_url')
    return url

def get_token():
    parser = RawConfigParser()
    parser.read(cred_file)
    email = parser.get('config', 'email')
    token = parser.get('config', 'token')
    auth_string = "{}/token:{}".format(email,token)
    encoded_token = (b64encode(auth_string.encode('ascii'))).decode('ascii')
    return encoded_token

def get_auth_headers():
    return {'Authorization': "Basic {}".format(get_token())}

def parse_ticket(ticket):
    ticket_line = []
    ticket_line.append(line_seperator)
    ticket_line.append("*Id-> {}\n".format(ticket["id"]))
    ticket_line.append("*Subject-> {}\n".format(ticket["subject"]))
    ticket_line.append("*Description->\n{}\n".format(ticket["description"]))
    ticket_line.append("\n")
    return ticket_line


def parse_tickets(tickets_str):
    ticket_json = json.loads(tickets_str)
    tickets_list = ticket_json["tickets"]
    ticket_lines = []
    next_url = None
    prev_url = None
    ticket_lines.append("Here is the list of tickets\n")
    for ticket in tickets_list:
        ticket_lines.extend(parse_ticket(ticket))
        

    if(ticket_json["links"]):
        if(ticket_json["links"]["prev"]):
            prev_url =  ticket_json["links"]["prev"]
        if(ticket_json["meta"] and ticket_json["meta"]["has_more"]):
            if(ticket_json["links"]["next"]):
                next_url =  ticket_json["links"]["next"]

    print(prev_url,end="\n")
    print(next_url,end="\n")
    return "".join(ticket_lines), prev_url, next_url
     
def get_tickets(url):
    r = requests.get(url,headers=get_auth_headers())
    if r.ok:
        return(parse_tickets(r.text))
    else:
        return "Something went wrong please try again \n\n", None, None

def get_menu(prev=False,next=False):
    resp = '''--------Welcome to Zendesk Tickets Command Line Utility------\n'''
    count = 1
    if next==False and prev == False:
        resp += '''\t* Enter 1 to get first 25 tickets\n'''
        count+=1

    
    if next == True:
        resp += '''\t* Enter 1 to get next 25 tickets\n'''
        count+=1
    

    if prev == True:
        resp += '''\t* Enter 2 to get previous 25 tickets\n'''
        count+=1

    resp+='''\t* Enter 0 to exit\n\n'''

    return resp
    
def main():
    api_url = get_api_url()    
    user_input = ""
    prev_url = None
    next_url = api_url
    curr_url = None
    page=0
    while user_input != "0" :
        print(get_menu((page>=2 and prev_url!=None),next_url!=None))
        user_input = input("Enter here :").strip()
        if next_url!=None and user_input=="1":
            curr_url = next_url
            page+=1

        elif (page>=2 and prev_url!=None) and user_input=="2":
            curr_url = prev_url
            page-=1
        
        if(curr_url!=None):
            tickets,prev_url,next_url = get_tickets(curr_url)
            curr_url = None
            print(tickets)
    
       
if __name__ == "__main__":
    main()