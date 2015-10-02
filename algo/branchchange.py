#!/usr/bin/python3
import csv, sys;

class Branch:
	code = 0
	name = ""
	sancStrength = 0
	curStrength = 0
	maxStrength = 0
	def __init__(self,information,deptcode):
		self.code = deptcode
		self.name = information[0]
		self.sancStrength = int(information[1])
		self.curStrength = int(information[2])
		self.maxStrength = int(self.sancStrength + round(self.sancStrength/10,0))

class Student:
	roll = ""
	name = ""
	cpi = 0.0
	branch = 0
	category = ""
	tempbranch = 0
	# info = []
	preferences = []

	def __init__(self, information):
		self.roll = information[0]
		self.name = information[1]
		self.branch = information[2]
		self.cpi = float(information[3])
		self.category = information[4]
		self.preferences = information[5:]
	
	# Validate whether a student is eligible for branch change or not according
	# to the CPI criterion
	def isEligible(self):
		if((self.category == "GE") | (self.category == "OBC")):
			return (self.cpi >= 8.00)
		else:
			return (self.cpi >= 7.00)

branches = []
students = []
numbranches = 0
branchmap = {}

with open(sys.argv[1],'r') as csvfile:
	branchreader = csv.reader(csvfile)
	for row in branchreader:
		if(row[0] == "BranchName"):
			branchheader = row
		else:
			newbranch = Branch(row,numbranches)
			branches.append(newbranch)
			branchmap[newbranch.name] = newbranch.code;
			numbranches = numbranches+1
 
# for curbranch in branches:
#  	print(curbranch.name,curbranch.sancStrength,curbranch.curStrength,sep = " ")

with open(sys.argv[2],'r') as csvfile:
	studentreader = csv.reader(csvfile)
	for row in studentreader:
		if(row[0] == "RollNo"):
			studentheader = row
		else:
			newstudent = Student(row)
			if(newstudent.isEligible()):
				students.append(newstudent)

students = list(reversed(sorted( students, key = lambda x: x.cpi)))

# for curstudent in students:
	# print(curstudent.name,curstudent.preferences,curstudent.cpi,sep = " ")

for curStudent in students:
	curStudent.tempbranch = branchmap[curStudent.branch]

MaxUnallowedCPI = {}
MinAllowedCPI = {}
codeToBranch = {}

for key,value in branchmap.items():
	MaxUnallowedCPI[value] = 6.99
	MinAllowedCPI[value] = 10.00
	codeToBranch[value] = key

def allotBranch(candidate):
	index = -1
	for name in candidate.preferences:
		
		index = branchmap[name]
		CPI = candidate.cpi
		print(name,branches[index].curStrength)
		if(branches[index].curStrength < branches[index].maxStrength):
			
			updatedStrength = branches[candidate.tempbranch].curStrength -1
			minStrength = branches[candidate.tempbranch].sancStrength*0.75
			
			if(CPI >= 9.00 or (updatedStrength >= minStrength and CPI > MaxUnallowedCPI[index])):
				branches[index].curStrength = branches[index].curStrength + 1
				branches[candidate.tempbranch].curStrength = updatedStrength
				MinAllowedCPI[index] = min(MinAllowedCPI[index],CPI)
				candidate.tempbranch = index
				break
		
		elif(CPI == MinAllowedCPI[index]):
			
			branches[index].curStrength = branches[index].curStrength + 1
			branches[candidate.tempbranch].curStrength = updatedStrength
			candidate.tempbranch = index
			break

	if(index != -1):
		candidate.preferences = candidate.preferences[0:index]
	return index

toDelete = []
tempStudents = students[:]
changed = len(students)

while (len(tempStudents) != 0 and changed != 0):
	
	# Denotes the no of Students whose branch changed
	changed = 0						

	for i,curStudent in enumerate(tempStudents):
		curbranch = curStudent.tempbranch	
		branchAlloted = allotBranch(curStudent)
		
		if(branchAlloted == branchmap[curStudent.preferences[0]]):
			changed = changed + 1
			toDelete.append(i)
		
		elif(branchAlloted != -1 ):

			if(curbranch != branchAlloted):
				changed = changed + 1
			for key in curStudent.preferences:
				
				branchCode = branchmap[key]
				if(branchAlloted > branchCode):
					MaxUnallowedCPI[branchCode] = max(curStudent.cpi,MaxUnallowedCPI[branchCode])
				else:
					break
		else:
			for key in curStudent.preferences:
				MaxUnallowedCPI[branchmap[key]] = max(curStudent.cpi,MaxUnallowedCPI[branchmap[key]])

	toDelete = toDelete[::-1] 
	for i in toDelete:	
		 tempStudents.pop(i)
	del toDelete[:]

def changedBranch(candidate):
	curbranch = codeToBranch[candidate.tempbranch]
	if(curbranch == candidate.branch):
		return "Branch Unchanged"
	else:
		return curbranch

for curStudent in students:
	print(curStudent.roll,curStudent.name,curStudent.branch,changedBranch(curStudent),sep = " ")