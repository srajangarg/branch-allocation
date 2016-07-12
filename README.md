## Basic Dependenices
* python2.7
* django1.8 for 2.7

## LDAP Authentication Dependenices ######

* python-dev
* libldap2-dev
* libsasl2-dev
* python-ldap

## Running

Before running these things need to be set :

* In file /bcapp/views.py :

	* line 42 	:			The username of the admin must be set by you

	* line 46-55	:			Only one of the given options must be enabled (uncommented)

* Make sure these two files exist :

	* /static/students.csv :	Contains the students information, maybe empty

	* /static/branches.csv : 	Must be filled with the correct branch data of the year!


To run the server, simply `python manage.py migrate`
and then `python manage.py runserver`

The webapp can be accessed on `http://127.0.0.1:8000/bcapp/`

### Screenshots

![](/scr1.png)

![](/scr2.png)

![](/scr3.png)

### Notes

We have made the app, keeping in mind that it is to simulate what a real world app would be like
So, we have implemented LDAP authentication from ldap.iitb.ac.in
This means we have not implemented a "create user" mechanism

The two static csv files must be present at all times. Also, the user get the options dynamically 
from the branches.csv file (Only those options, which actually exist in the file)

To test the algorithmic part of the project, one can switch off the ldap, and goto the admin page,
by logging in using the set admin name

Also, we have not used models in this project. We felt that using a databse was overkill (for the required task
and redundant. We know this is bad programming practice, but it was really not needed in our project
