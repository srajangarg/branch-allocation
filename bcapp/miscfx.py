import ldap, os, csv

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

	for i in range(len(postData) - 6):
		userData.append(postData.get("pref"+str(i+1)))
	
	if not os.path.isfile("main.csv"):
		f = open("main.csv","w")
		f.write("RollNo,Name,CurrentBranch,CPI,Category,Options\n")
		f.close()

	with open('main.csv', 'r') as inp, open('first_edit.csv', 'w') as out:
	
		writer = csv.writer(out)

		for row in csv.reader(inp):
			
			if found or (row[0] != postData.get("rollno") and row[1] != postData.get("uname")):
				writer.writerow(row)
			else:
				found = True

		writer.writerow(userData)

	os.remove("main.csv")
	os.rename("first_edit.csv", "main.csv")

def getContents(rollno):

	with open('main.csv', 'r') as inp:
		for row in csv.reader(inp):
			if row[0] == rollno:
				return row

	return ["","","","",""]