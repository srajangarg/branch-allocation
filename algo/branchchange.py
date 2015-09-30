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
		self.maxStrength = int(self.sancStrength) + round(self.sancStrength/10,0)

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
# 	print(curbranch.name,curbranch.sancStrength,curbranch.curStrength,sep = " ")

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

for curstudent in students:
	print(curstudent.name,curstudent.preferences,curstudent.cpi,sep = " ")