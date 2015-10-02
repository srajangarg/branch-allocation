import ldap
import csv

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

	return