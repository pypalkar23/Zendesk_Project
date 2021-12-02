from main import *
import unittest


class TestTicketUtility(unittest.TestCase):
    def test_tickets_url_reader(self):
        #Test for correct retrieval of URL to retrieve multiple tickets from config
        self.assertEqual(get_tickets_url(
        ), "https://zccpypalkar23.zendesk.com/api/v2/tickets.json?page[size]=25")

    def test_ticket_url_reader(self):
        #Test for correct retrieval of URL to retrieve single ticket from config
        self.assertEqual(
            get_ticket_url(), "https://zccpypalkar23.zendesk.com/api/v2/tickets/{}.json")

    def test_correct_tickets_resp(self):
        #Test to check the accuracy of tickets parsed by the program
        correct_url = "https://zccpypalkar23.zendesk.com/api/v2/tickets.json?page[size]=25"
        
        resp, prev, next = get_tickets(correct_url)
        tickets_sample = ""
        with open("tickets_sample.txt") as f:
            tickets_sample = "".join(f.readlines())
        self.assertEqual(resp, tickets_sample)
        self.assertEqual(
            prev, "https://zccpypalkar23.zendesk.com/api/v2/tickets.json?page%5Bbefore%5D=eyJvIjoibmljZV9pZCIsInYiOiJhUUVBQUFBQUFBQUEifQ%3D%3D&page%5Bsize%5D=25")
        self.assertEqual(
            next, "https://zccpypalkar23.zendesk.com/api/v2/tickets.json?page%5Bafter%5D=eyJvIjoibmljZV9pZCIsInYiOiJhUmtBQUFBQUFBQUEifQ%3D%3D&page%5Bsize%5D=25")

    def test_incorrect_tickets_resp(self):
        #Test to check error handling by the program by passing incorrect url
        incorrect_url = "https://zcpypalkar23.zendesk.com/api/v2/tickets.json?page[size]=25"
        resp, next, prev = get_tickets(incorrect_url)
        self.assertEqual(resp, "Something went wrong please try again")
        self.assertEqual(next, None)
        self.assertEqual(prev, None)

    def test_ticket_resp_does_not_exist(self):
         #Test to check error handling by the program if a particular ticket id does not exist in the system
        ticket_id = "102"
        resp = get_ticket(ticket_id)
        self.assertEqual(
            resp, "<---- Ticket with such id does not exist ----->")

    def test_ticket_resp_wrong_input(self):
        #Test to check error handling by the program if a particular ticket id does not have the required format
        ticket_id = "abc"
        resp = get_ticket(ticket_id)
        self.assertEqual(
            resp, "<------------Enter correct Ticket number--------------->")

    def test_ticket_correct_input(self):
        #Test to check the accuracy of a individual ticket details parsed by the program
        ticket_id = "101"
        resp = get_ticket(ticket_id)

        ticket_sample = ""
        with open("ticket_sample.txt") as f:
            ticket_sample = "".join(f.readlines())

        self.assertEqual(resp, ticket_sample)
