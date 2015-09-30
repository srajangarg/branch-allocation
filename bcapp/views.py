from django.shortcuts import render
from django.http import HttpResponse
from ldapfx import *
# Create your views here.

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

	if request.method == 'GET':
	    
	    return render(request, "bcapp/lost.html")

	if request.method == 'POST':
	    
	    userLDAP = request.POST.get("ldapid")
	    userPASS = request.POST.get("ldappass")

	    (auth,rollno) = doLogin(userLDAP, userPASS)

	    if auth:
	    	return render(request,"bcapp/index.html", {"userLDAP": userLDAP, "rollno": rollno})
	    else:
	    	return render(request,"bcapp/loginfail.html")
