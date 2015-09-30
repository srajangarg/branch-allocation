import csv, sys;

class Branch:
	code = 0
	name = 0
	sancStrength = 0
	curStrength = 0
	maxStrength = 0
	def __init__(self,information):
		self.code = deptcode
		self.name = information[0]
		self.sancStrength = information[1]
		self.curStrength = information[2]
		self.maxStrength = sancStrength + round(sancStrength/10,0)


class Student:
	roll = ""
	name = ""
	cpi = 0.0
	branch = 0
	category = ""
	tempbranch = 0
	# info = []
	preferences = []

	def __init__(self, information, branchpref):
		self.roll = information[0]
		self.name = information[1]
		self.cpi = information[2]
		self.branch = 
		self.preferences = branchpref

branches = []
numbranches = 0

with open(sys.argv[2],'r') as csvfile:
	branchreader = csv.reader(csvfile)
	for row in branchreader:
		if(row[0] == "BranchName"):
			branchheader = row
		else:
			newbranch = Branch(row,numbranches + 1)
			numbranches = numbranches+1
			branches.append(row[0]);

