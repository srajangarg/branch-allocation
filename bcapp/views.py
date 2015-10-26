from django.shortcuts import render, redirect
from django.http import HttpResponse
import csv
from miscfx import *
from algo import *

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

	categories = ["GEN", "OBC", "SC", "ST", "PwD"]

	if request.method == 'GET':
	    
	    return render(request, "bcapp/lost.html")

	if request.method == 'POST':
	    
	    userLDAP = request.POST.get("ldapid")
	    userPASS = request.POST.get("ldappass")

	    if userLDAP == "" or userPASS == "":
	    	return render(request,"bcapp/login.html", {"error":"Both fields must be filled!"})


	    ################### SET ADMIN USERNAME BELOW #######################
	    ADMIN = "garg"
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
	    		return render(request,"bcapp/index.html", {"userLDAP": userLDAP, "rollno": rollno, "oldPrefs": oldPrefs, "branches": branches, "categories":categories, "range":range(len(oldPrefs)-5), "bcpref":oldPrefs[5:]})
	    else:
	    	return render(request,"bcapp/loginfail.html")


def saved(request):

	if request.method == 'GET':
		return render(request, "bcapp/lost.html")

	if request.method == 'POST':
		# len(request.POST) -6 is number of preferences
		editCSV(request.POST)
		return render(request,"bcapp/saved.html")

def upload(request):

	if request.method == 'GET':
		return render(request, "bcapp/lost.html")

	if request.method == 'POST':
		# len(request.POST) -6 is number of preferences
		dealWith(request.FILES['file1'], request.FILES['file2'])
		return render(request,"bcapp/uploaded.html")

def resultcsv(request):

	try:
		print request.session['user']

		response = HttpResponse(content_type='text/csv')
		response['Content-Disposition'] = 'attachment; filename="result.csv"'

		myList = branchchange("static/input_programmes.csv", "static/input_options.csv")
		writer = csv.writer(response)

		for curr in myList:
			writer.writerow([curr[0], curr[1], curr[2], curr[3]])

		return response

	except:
		return render(request, "bcapp/notadmin.html")

def resultview(request):

	try:
		print request.session['user']

		myList = branchchange("static/input_programmes.csv", "static/input_options.csv")
		return render(request, "bcapp/result.html", {"finalList":myList})

	except:
		return render(request, "bcapp/notadmin.html")