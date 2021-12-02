# Zendesk Command Line Utility for Tickets

- This project was made as an assignment for Zendesk Internship Assessment.
- The utility is built in `python3`.

### Dependencies:
As mentioned in the requirements.txt, the project is dependent on following external python modules
*  certifi==2021.10.8
* charset-normalizer==2.0.8
* idna==3.3
* requests==2.26.0
* urllib3==1.26.7


The dependencies can be installed with python's `pip` utility .  
* `pip3 install -r requirements.txt`   

## Execution:
After successful installation of dependencies, one can execute the program by following command.
* `python3 main.py`

## Tests:
The unit test cases are in test_util.py. To run the unit test run the following command
* `python3 -m unittest test_util.py`

## Description
As mentioned in the requirement this program can 
- Connect to the Zendesk API
- Request all the tickets for an account
- Display them in a list
- Display individual ticket details
- Page through tickets when more than 25 are returned

# Screenshots
Below are the screenshots for the program to demonstrate the functionality

- Initial Menu:   
![initial_menu](https://github.com/pypalkar23/Zendesk_Project/blob/main/images/first_menu.png)

- Menu when user has already paged through more than or equal to first 50 tickets and more tickets are available in the system.  
![next_menu](https://github.com/pypalkar23/Zendesk_Project/blob/main/images/next_menu.png)

- Menu when user has paged through all the tickets for the account.
![last_menu](https://github.com/pypalkar23/Zendesk_Project/blob/main/images/last_menu.png)

- Ticket List:   
![ticket_list](https://github.com/pypalkar23/Zendesk_Project/blob/main/images/ticket_list.png)

- Error shown when tickets can't be retrieved  
![error_shown](https://github.com/pypalkar23/Zendesk_Project/blob/main/images/Error.png)

- Individual Ticket Flow:  
![individual_ticket](https://github.com/pypalkar23/Zendesk_Project/blob/main/images/ticket_display.png)

- Error when ticket user has asked for does not exist in the system. 
    ![ticket_not_available](https://github.com/pypalkar23/Zendesk_Project/blob/main/images/ticket_does_not_exist.png)

