from django.shortcuts import render, redirect
from django.http import HttpResponse
import csv
from miscfx import *
from algo import *
from algochallenge import *

categories = ["GEN", "OBC", "SC", "ST", "PwD"]

def index(request):

	try:
		del request.session['user']
	except:
		pass

	return render(request, "bcapp/login.html")

def admin(request):

	try:
		print request.session['user']
		return render(request, "bcapp/admin.html")
	except:
		return render(request, "bcapp/notadmin.html")	

def submit(request):

	if request.method == 'GET':
	    
	    return render(request, "bcapp/lost.html")

	if request.method == 'POST':
	    
	    userLDAP = request.POST.get("ldapid")
	    userPASS = request.POST.get("ldappass")

	    if userLDAP == "" or userPASS == "":
	    	return render(request,"bcapp/login.html", {"ldapid":userLDAP,"error":"Both fields must be filled!"})


	    ################### SET ADMIN USERNAME BELOW #######################
	    ADMIN = "admin"
	    ####################################################################


	    ############# UNCOMMENT BELOW  FOR LDAP AUTHENTICATION #############
	    #(auth,rollno) = doLogin(userLDAP, userPASS)
	    ####################################################################

	    							### OR ###

	    ############### UNCOMMENT FOR NO AUTHENTICATION ################
	    rollno = userLDAP
	    auth = True
	    ####################################################################

	    if auth:

	    	if userLDAP == ADMIN:

	    		request.session['user'] = "admin"
	    		return redirect("admin")
	    	else:
	    		oldPrefs = getContents(rollno)
	    		branches = getbranches()

	    		if not branches:
	    			return render(request,"bcapp/login.html", {"ldapid":userLDAP,"error":"branches.csv has not been uploaded by admin"})

	    		return render(request,"bcapp/index.html", {"userLDAP": userLDAP, "rollno": rollno, "oldPrefs": oldPrefs, "branches": branches, "categories":categories, "range":range(len(oldPrefs)-5), "bcpref":oldPrefs[5:]})
	    else:
	    	return render(request,"bcapp/login.html", {"ldapid":userLDAP,"error":"Your credentials are incorrect!"})


def saved(request):

	if request.method == 'GET':
		return render(request, "bcapp/lost.html")

	if request.method == 'POST':
		postData = request.POST
		error = isCorrect(postData)

		if error == "none":
			editCSV(postData)
			warn = ""

			if postData.get("category")=="GEN":
				 if float(postData.get("cpi")) < 8:
				  	warn = "Your CPI is below the cutoff, but the form was submitted!"
			else:
				if float(postData.get("cpi")) < 7:
					warn = "Your CPI is below the cutoff, but the form was submitted!"

			return render(request,"bcapp/saved.html",{"warn":warn})
			
		else:
			rollno = postData.get("rollno")
			userLDAP =  postData.get("userldap")
			oldPrefs = [rollno, postData.get("uname"), postData.get("currb"), postData.get("cpi"), postData.get("category")]
			
			for i in range(len(postData) - 7):
				oldPrefs.append(postData.get("pref"+str(i+1)))
			branches = getbranches()
			
			return render(request,"bcapp/index.html", {"userLDAP": userLDAP, "rollno": rollno, "oldPrefs": oldPrefs, "branches": branches, "categories":categories, "range":range(len(oldPrefs)-5), "bcpref":oldPrefs[5:], "error":error})


def upload(request):

	if request.method == 'GET':
		return render(request, "bcapp/lost.html")

	if request.method == 'POST':

		if len(request.FILES) != 2 :
			return render(request,"bcapp/admin.html", {"error":"Choose both files!"})

		dealWith(request.FILES['file1'], request.FILES['file2'])
		return render(request,"bcapp/uploaded.html")

def resultcsv(request):

	try:
		print request.session['user']

		response = HttpResponse(content_type='text/csv')
		response['Content-Disposition'] = 'attachment; filename="result.csv"'

		myList = branchchange("static/branches.csv", "static/students.csv")
		writer = csv.writer(response)

		for curr in myList:
			writer.writerow([curr[0], curr[1], curr[2], curr[3]])

		return response

	except:
		return render(request, "bcapp/notadmin.html")

def resultcsvchallenge(request):

	try:
		print request.session['user']

		response = HttpResponse(content_type='text/csv')
		response['Content-Disposition'] = 'attachment; filename="result.csv"'

		myList = branchchangechallenge("static/branches.csv", "static/students.csv")
		writer = csv.writer(response)

		for curr in myList:
			writer.writerow([curr[0], curr[1], curr[2], curr[3]])

		return response

	except:
		return render(request, "bcapp/notadmin.html")

def resultview(request):

	try:
		print request.session['user']

		myList = branchchange("static/branches.csv", "static/students.csv")
		return render(request, "bcapp/result.html", {"finalList":myList})

	except:
		return render(request, "bcapp/notadmin.html")

def resultviewchallenge(request):

	try:
		print request.session['user']

		myList = branchchangechallenge("static/branches.csv", "static/students.csv")
		return render(request, "bcapp/result.html", {"finalList":myList})

	except:
		return render(request, "bcapp/notadmin.html")