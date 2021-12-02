#!/usr/bin/python3
from json import loads
from base64 import b64encode
from configparser import RawConfigParser
from requests import get
from datetime import datetime

config_file = "project.props"
cred_file = "cred.props"
ticket_seperator = "-"*80+"\n"
line_seperator = "*"*80+"\n"

def get_tickets_url():
    parser = RawConfigParser()
    parser.read(config_file)
    url = parser.get('config', 'api_url')
    endpoint = parser.get('config', 'tickets_handle')
    return url + endpoint

def get_ticket_url():
    parser = RawConfigParser()
    parser.read(config_file)
    url = parser.get('config', 'api_url')
    endpoint = parser.get('config', 'ticket_handle')
    return url + endpoint

def get_token():
    parser = RawConfigParser()
    parser.read(cred_file)
    email = parser.get('config', 'email')
    token = parser.get('config', 'token')
    auth_string = "{}/token:{}".format(email,token)
    encoded_token = (b64encode(auth_string.encode('ascii'))).decode('ascii')
    return encoded_token

def is_empty(object,key):
    if key in object and object[key]!=None and object[key]!="null":
        return False
    print(object[key])
    return True

def get_auth_headers():
    return {'Authorization': "Basic {}".format(get_token())}

def get_formatted_date(date_str):
    return datetime.fromisoformat(date_str[:-1]).strftime("%b %d,%Y %H:%M:%S")

def parse_ticket(ticket_json):
    ticket_lines = []
    ticket_lines.append(ticket_seperator)
    if("error" in ticket_json):
        ticket_lines.append("<---- Ticket with such id does not exist ----->")
    
    else:
        ticket= ticket_json["ticket"]
        ticket_lines.append("Here are the details for the ticket\n")
        ticket_lines.append("* Id-> {}\n".format(ticket["id"]))
        if not is_empty(ticket,"type"):
            ticket_lines.append("* Type -> {}\n".format(ticket["type"]))
        ticket_lines.append("* Subject -> {}\n".format(ticket["subject"]))
        ticket_lines.append("* status -> {}\n".format(ticket["status"]))
        ticket_lines.append("* Priority -> {}\n".format(ticket["priority"]))
        ticket_lines.append("* Tags -> {}\n".format(",".join(ticket["tags"])))
        ticket_lines.append("* Requested By -> {}\n".format(ticket["requester_id"]))
        ticket_lines.append("* Submitted By -> {}\n".format(ticket["submitter_id"]))
        ticket_lines.append("* Assigned To -> {}\n".format(ticket["assignee_id"]))
        ticket_lines.append("* Form Id -> {}\n".format(ticket["ticket_form_id"]))
        ticket_lines.append("* Brand Id -> {}\n".format(ticket["brand_id"]))
        if not is_empty(ticket,"organization_id"):
            ticket_lines.append("* Organization -> {}\n".format(ticket["organization_id"]))
        if not is_empty(ticket,"group_id"):
            ticket_lines.append("* Group -> {}\n".format(ticket["group_id"]))
        ticket_lines.append("* Created on -> {}\n".format(get_formatted_date(ticket["created_at"])))
        ticket_lines.append("* Modified on -> {}\n".format(get_formatted_date(ticket["updated_at"])))
        if not is_empty(ticket,"due_at"):
            ticket_lines.append("* Due on -> {}\n".format(get_formatted_date(ticket["due_at"])))
        ticket_lines.append("* Description ->\n{}\n".format(ticket["description"]))
    
    ticket_lines.append("\n")
    return "".join(ticket_lines)

def parse_ticket_summary(ticket):
     ticket_lines = []
     ticket_lines.append("Id -> {} | ".format(ticket["id"]))
     ticket_lines.append("Subject -> {}| ".format(ticket["subject"]))
     ticket_lines.append("Requested By -> {} | ".format(ticket["requester_id"]))
     ticket_lines.append("Created On -> {}".format(get_formatted_date(ticket["created_at"])))
     ticket_lines.append("\n\n")
     return "".join(ticket_lines)


def get_ticket(url):
    resp = get(url,headers=get_auth_headers())
    if resp.ok or resp.status_code==404:
        return parse_ticket(loads(resp.text))
    else: 
        return "Some Error Occured"


def parse_tickets(tickets_str):
    ticket_json = loads(tickets_str)
    tickets_list = ticket_json["tickets"]
    ticket_lines = []
    next_url = None
    prev_url = None
    ticket_lines.append("Here is the list of tickets\n")
    for ticket in tickets_list:
        ticket_lines.append(parse_ticket_summary(ticket))
        

    if(ticket_json["links"]):
        if(ticket_json["links"]["prev"]):
            prev_url =  ticket_json["links"]["prev"]
        if(ticket_json["meta"] and ticket_json["meta"]["has_more"]):
            if(ticket_json["links"]["next"]):
                next_url =  ticket_json["links"]["next"]

    #print(prev_url,end="\n")
    #print(next_url,end="\n")
    return "".join(ticket_lines), prev_url, next_url
     
def get_tickets(url):
    r = get(url,headers=get_auth_headers())
    if r.ok:
        return(parse_tickets(r.text))
    else:
        return "Something went wrong please try again \n\n", None, None

def get_menu(prev=False,next=False):
    lines = []
    lines.append(line_seperator)
    lines.append("Welcome to Zendesk Tickets Command Line Utility\n")

    if next==False and prev == False:
        lines.append("\t* Enter 1 to get first 25 tickets\n")
        
    if next == True:
        lines.append("\t* Enter 1 to get next 25 tickets\n")
        
    if prev == True:
        lines.append("\t* Enter 2 to get previous 25 tickets\n")
        
    lines.append("\t* Enter 3 to see a ticket in detail\n")
    lines.append("\t* Enter 0 to exit\n\n")
    lines.append(line_seperator)
    
    return "".join(lines)
    
def main():
    tickets_url = get_tickets_url()   
    ticket_url  = get_ticket_url()
    user_input = ""
    prev_url = None
    next_url = tickets_url
    curr_url = None
    page=0
    while user_input != "0" :
        print(get_menu((page>=2 and prev_url!=None),next_url!=None))
        user_input = input("Enter here :").strip()
        if user_input=="1" or user_input=="2":
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
        elif user_input=="3":
            ticket_no = input("Enter ticket Id:")
            if ticket_no.isdigit():
               ticket = get_ticket(ticket_url.format(ticket_no))
               print(ticket)
            

    
       
if __name__ == "__main__":
    main()