import os, csv, ldap

def doLogin(userName, passWord):

	userName = "uid="+userName
	conn = ldap.initialize('ldap://ldap.iitb.ac.in')
	search_result = conn.search_s('dc=iitb,dc=ac,dc=in', ldap.SCOPE_SUBTREE, userName, ['uid','employeeNumber'])

	try:

		if search_result:
			authenticate = conn.bind_s(search_result[0][0],passWord)
			# print search_result[0][1]['employeeNumber'][0] #roll
			# print search_result[0][1]['uid'][0] #username
			return(True, search_result[0][1]['employeeNumber'][0])
			
		else:
			return (False, "")

	except ldap.INVALID_CREDENTIALS:
		return (False, "")

def editCSV(postData):

	found = False
	userData = [postData.get("rollno"), postData.get("uname"), postData.get("currb"), postData.get("cpi"), postData.get("category")]

	for i in range(len(postData) - 7):
		userData.append(postData.get("pref"+str(i+1)))
	
	if not os.path.isfile("static/students.csv"):
		f = open("static/students.csv","w")
		f.write("RollNo,Name,CurrentBranch,CPI,Category,Options\n")
		f.close()

	with open('static/students.csv', 'r') as inp, open('static/first_edit.csv', 'w') as out:
	
		writer = csv.writer(out)

		for row in csv.reader(inp):
			
			if found or (row[0] != postData.get("rollno") and row[1] != postData.get("uname")):
				writer.writerow(row)
			else:
				found = True

		writer.writerow(userData)

	os.remove("static/students.csv")
	os.rename("static/first_edit.csv", "static/students.csv")

def getContents(rollno):

	with open('static/students.csv', 'r') as inp:
		for row in csv.reader(inp):
			if row[0] == rollno:
				return row

	return ["","","","",""]

def getbranches():
	branches = []
	with open('static/branches.csv', 'r') as inp:
		for row in csv.reader(inp):
			if row[0] != "BranchName":
				branches.append(row[0])
	return branches

def dealWith(f1, f2):

	with open('static/students.csv', 'w') as destination:
	    for chunk in f1.chunks():
	        destination.write(chunk)

	with open('static/branches.csv', 'w') as destination:
	    for chunk in f2.chunks():
	        destination.write(chunk)

def isCorrect(postData):

	if(postData.get("uname") == ""):
		return "Please enter your name!"

	cpi = postData.get("cpi")

	if(cpi == ""):
		return "You have not entered your CPI! Please enter it correct upto 2 decimal places"
	isNum = True
	countDot = 0
	for x in range(0,len(cpi)):
		if( (not cpi[x].isdigit()) and cpi[x] != '.'):
			isNum = False
			break
		elif(cpi[x] == '.'):
			countDot = countDot + 1
			if(countDot > 1):
				isNum = False
				break

	if(isNum):
		val = float(cpi)
		if(val > 10):
			return "Your CPI is out of bounds!"	
		elif(len(cpi) != 4 and val != 10):
			return "Please follow the standard CPI format and don't add any extra prefix zeroes!"
	else:
		return "Your CPI isn't a positive number!"

	chosenB = postData.get("currb")
	prefs = []

	if len(postData) == 7:
		return "Please choose at least 1 preference!"

	for i in range(len(postData) - 7):
		prefs.append(postData.get("pref"+str(i+1)))

	for pref in prefs:
		if pref == chosenB:
			return "You can't have your current branch as a preference!"

	for i in range(len(prefs)):
		for j in range(i+1, len(prefs)):
			if prefs[i] == prefs[j]:
				return "No two preferences can be the same!"

	return "none"