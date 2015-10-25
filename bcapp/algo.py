import csv, sys;

def branchchange(branchfile, studentfile):
	
	class Branch:
		def __init__(self,information,deptcode):
			self.code = deptcode
			self.sancStrength = int(information[1])
			self.name = information[0]
			self.curStrength = int(information[2])
			self.maxStrength = int(self.sancStrength + round(self.sancStrength/10,0))
			self.minStrength = self.sancStrength*0.75
			self.MaxUnallowedCPI = 6.99
			self.MinAllowedCPI = 10.0
			# self.minStrength = int(self.sancStrength - round(self.sancStrength/4,0))
	class Student:
		def __init__(self, information):
		self.roll = information[0]
		self.name = information[1]
		self.branch = branchmap[information[2]]
		self.cpi = float(information[3])
		self.category = information[4]
		self.preferences = []
		for branchpref in information[5:]:
			if branchpref:
				self.preferences.append(branchmap[branchpref])
		self.tempbranch = self.branch
		# self.preferences = information[5:]
	
		# Validate whether a student is eligible for branch change or not according
		# to the CPI criterion
		def isEligible(self):
			if((self.category == "GE") | (self.category == "OBC")):
				return (self.cpi >= 8.00)
			else:
				return (self.cpi >= 7.00)

		def allotBranch(self):
			index = -1
			for dept in self.preferences:
				CPI = self.cpi
				if(dept == self.tempbranch):
					break
				#print(name,branches[index].curStrength)
				if(branches[dept].curStrength < branches[dept].maxStrength):
					
					updatedStrength = branches[self.tempbranch].curStrength -1

					if(CPI >= 9.00 or (updatedStrength >= branches[self.tempbranch].minStrength and CPI > branches[dept].MaxUnallowedCPI)):
						branches[dept].curStrength = branches[dept].curStrength + 1
						branches[self.tempbranch].curStrength = updatedStrength
						branches[dept].MinAllowedCPI = min(branches[dept].MinAllowedCPI,CPI)
						self.tempbranch = dept
						index = dept
						break
				
				elif(CPI == branches[dept].MinAllowedCPI):
					updatedStrength = branches[self.tempbranch].curStrength -1

					if(CPI >= 9.00 or (updatedStrength >= branches[self.tempbranch].minStrength and CPI > branches[dept].MaxUnallowedCPI)):
						branches[dept].curStrength = branches[dept].curStrength + 1
						branches[self.tempbranch].curStrength = updatedStrength
						self.tempbranch = dept
						index = dept
						break

			# if(index != -1):
			# 	self.preferences = self.preferences[0:index]
			return index


	def changedBranch(candidate):
		if(candidate.tempbranch == candidate.branch):
			return "Branch Unchanged"
		else:
			return branches[candidate.tempbranch].name

	branches = []
	students = []
	numbranches = 0
	branchmap = {}
	ineligibleStudents = []
	finalList = []

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
	#  	print(curbranch.name,curbranch.code,curbranch.sancStrength,curbranch.curStrength,sep = " ")

	with open(sys.argv[2],'r') as csvfile:
		studentreader = csv.reader(csvfile)
		for row in studentreader:
			if(row[0] == "RollNo"):
				studentheader = row
			else:
				newstudent = Student(row)
				if(newstudent.isEligible()):
					students.append(newstudent)
				else:
					ineligibleStudents.append(newstudent)

	students = list(reversed(sorted( students, key = lambda x: x.cpi)))

	# for curstudent in students:
		# print(curstudent.name,curstudent.preferences,curstudent.cpi,sep = " ")

	toDelete = []
	tempStudents = students[:]
	changed = len(students)
	# iterations =0

	# while(len(tempstudents) !=0 and iterations!=1):
	# 	iterations=0
	while (len(tempStudents) != 0 and changed != 0):
		
		# Denotes the no of Students whose branch changed
		changed = 0						

		for i,curStudent in enumerate(tempStudents):
			curbranch = curStudent.tempbranch
			branchAlloted = curStudent.allotBranch()
			
			if(branchAlloted == curStudent.preferences[0]):
				changed = changed + 1
				toDelete.append(i)
			
			elif(branchAlloted != -1 ):
				if(curbranch != branchAlloted):
					changed = changed + 1
				for key in curStudent.preferences:			
					if(key != branchAlloted):
						branches[key].MaxUnallowedCPI = max(curStudent.cpi,branches[key].MaxUnallowedCPI)
					else:
						break
			else:
				for key in curStudent.preferences:
					branches[key].MaxUnallowedCPI = max(curStudent.cpi,branches[key].MaxUnallowedCPI)

		toDelete = toDelete[::-1]
		for i in toDelete:
			 tempStudents.pop(i)
		del toDelete[:]

	students.extend(ineligibleStudents)
	students = list(sorted( students, key = lambda x: (x.roll,x.name.lower())))
	for curStudent in students:
		if(curStudent.tempbranch != curStudent.branch):
			finalList.append([curStudent.roll, curStudent.name, branches[curStudent.branch].name, branches[curStudent.tempbranch].name])
		elif curStudent.isEligible():
			finalList.append([curStudent.roll,curStudent.name,branches[curStudent.branch].name,"Branch Unchanged"])
		else:
			finalList.append([curStudent.roll,curStudent.name,branches[curStudent.branch].name,"Ineligible"])
	return finalList
