from django.shortcuts import render
from django.http import HttpResponse
from miscfx import *

def index(request):

	return render(request, "bcapp/login.html")

def user(request):
	
	if request.method == 'GET':
	    
	    return render(request, "bcapp/lost.html")

	if request.method == 'POST':
	    
	    userLDAP = request.POST.get("ldapid")
	    userPASS = request.POST.get("ldappass")

	    return HttpResponse("Srajan says hey there world!")

def submit(request):

	branches = ["Branch 1","Branch 2","Branch 3","Branch 4","Branch 5"]
	categories = ["GEN", "OBC", "SC", "ST", "PwD"]

	if request.method == 'GET':
	    
	    return render(request, "bcapp/lost.html")

	if request.method == 'POST':
	    
	    userLDAP = request.POST.get("ldapid")
	    userPASS = request.POST.get("ldappass")

	    #(auth,rollno) = doLogin(userLDAP, userPASS)
	    rollno = userLDAP
	    auth = True
	    if auth:

	    	oldPrefs = getContents(rollno)
	    	print oldPrefs
	    	return render(request,"bcapp/index.html", {"userLDAP": userLDAP, "rollno": rollno, "oldPrefs": oldPrefs, "branches": branches, "categories":categories, "range":range(len(oldPrefs)-5), "bcpref":oldPrefs[5:]})
	    else:
	    	return render(request,"bcapp/loginfail.html")
	
	return render(request,"bcapp/index.html", {"userLDAP": "garg", "rollno": "140050017"})

def saved(request):

	if request.method == 'GET':
		return render(request, "bcapp/lost.html")

	if request.method == 'POST':
		# len(request.POST) -6 is number of preferences
		editCSV(request.POST)
		return render(request,"bcapp/saved.html")