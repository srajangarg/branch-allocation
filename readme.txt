Group 01 : kuchbhi

	RollNo		 Name					Contribution

	140050017 	 Srajan Garg       		100%
	140050019 	 Rishabh Agarwal	  	100%	
	140050024 	 Anuj Mittal       		100%

Honour Code :

	I, Srajan Garg, pledge on our honour that I have not given or received any unauthorized assistance on this project or any previous task

	I, Rishabh Agarwal, pledge on our honour that I have not given or received any unauthorized assistance on this project or any previous task

	I, Anuj Mittal, pledge on our honour that I have not given or received any unauthorized assistance on this project or any previous task

Dependencies :
	
	######## Basic Dependenices ######

	python2.7 				pre-installed on ubuntu systems
	django1.8 for 2.7			sudo pip install django

	####### LDAP Authentication ######

	python-dev package		sudo apt-get install python-dev
	ldap2-dev library		sudo apt-get install libldap2-dev
	sasl2-dev library		sudo apt-get install libsasl2-dev

Running :

	Before running these things need to be set :

		In file /bcapp/views.py :

			line 42 	:			The username of the admin must be set by you

			line 46-55	:			Only one of the given options must be enabled (uncommented)

		Make sure these two files exist :

			/static/students.csv :	Contains the students information, maybe empty

			/static/branches.csv : 	Must be filled with the correct branch data of the year!

	To run the server, simply "python manage.py runserver"

	The webapp can be accessed on "http://127.0.0.1:8000/bcapp/"

Notes :

	We have made the app, keeping in mind that it is to simulate what a real world app would be like
	So, we have implemented LDAP authentication from ldap.iitb.ac.in
	This means we have not implemented a "create user" mechanism

	The two static csv files must be present at all times. Also, the user get the options dynamically 
	from the branches.csv file (Only those options, which actually exist in the file)

	To test the algorithmic part of the project, one can switch off the ldap, and goto the admin page,
	by logging in using the set admin name.

Citations :

	http://www.tangowithdjango.com/book17/
	https://docs.djangoproject.com/en/1.8/howto/custom-template-tags/
	https://github.com/DheerendraRathor/django-auth-ldap-ng
	http://materializecss.com/
	http://www.python-ldap.org/doc/html/index.html
	http://stackoverflow.com/questions/8321217/django-csrf-token-missing-or-incorrect
	https://docs.djangoproject.com/en/1.8/topics/templates/