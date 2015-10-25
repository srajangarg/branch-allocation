import csv, sys;

def branchchange(branchfile, studentfile):
	
	class Branch:
		def __init__(self,information,deptcode):
			self.code = deptcode
			self.sancStrength = int(information[1])
			self.name = information[0]
			self.curStrength = int(information[2])
			self.maxStrength = int(self.sancStrength + round(self.sancStrength/10,0))
			# self.minStrength = self.sancStrength*0.75
			self.maxRemove = self.curStrength - 0.75*self.sancStrength
			self.MaxUnallowedCPI = 6.99
			self.MinAllowedCPI = 10.0
			self.removed = 0
			# self.minStrength = int(self.sancStrength - round(self.sancStrength/4,0))
		def updateRemove(self):
			self.maxRemove = self.curStrength - 0.75*self.sancStrength
			self.removed = 0

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
				#print(name,branches[index].curStrength)
				if(branches[dept].curStrength < branches[dept].maxStrength):
					
					updatedRemoved = branches[self.tempbranch].removed + 1

					if(CPI >= 9.00 or (updatedRemoved <= branches[self.tempbranch].maxRemove and CPI > branches[dept].MaxUnallowedCPI)):
						branches[dept].curStrength = branches[dept].curStrength + 1
						branches[self.tempbranch].curStrength = branches[self.tempbranch].curStrength - 1
						branches[self.tempbranch].removed = updatedRemoved
						branches[dept].MinAllowedCPI = min(branches[dept].MinAllowedCPI,CPI)
						self.tempbranch = dept
						index = dept
						break
				
				elif(CPI == branches[dept].MinAllowedCPI):
					
					branches[dept].curStrength = branches[dept].curStrength + 1
					branches[self.tempbranch].curStrength = branches[self.tempbranch].curStrength - 1
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

	with open(branchfile,'r') as csvfile:
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

	with open(studentfile,'r') as csvfile:
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

	toDelete = []
	tempStudents = students[:]
	changed = len(students)
	iterations =0
	
	while(len(tempStudents) !=0 and iterations!=1):
		iterations=0
		changed = len(tempStudents)
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
						if(curStudent.branch != branchAlloted):
							branches[curStudent.branch].MaxUnallowedCPI = max(curStudent.cpi,branches[curStudent.branch].MaxUnallowedCPI)
						else:
							break
				else:
					for key in curStudent.preferences:
						branches[curStudent.branch].MaxUnallowedCPI = max(curStudent.cpi,branches[curStudent.branch].MaxUnallowedCPI)

			toDelete = toDelete[::-1]
			for i in toDelete:
				 tempStudents.pop(i)
			del toDelete[:]
			iterations = iterations+1
		for curbranch in branches:
			curbranch.updateRemove()

	# finalList = []

	# for curStudent in students:
	# 	if(curStudent.tempbranch != curStudent.branch):
	# 		finalList.append([curStudent.roll, curStudent.name, branches[curStudent.branch].name, branches[curStudent.tempbranch].name])

	# return finalList
	with open("result.csv", 'w') as csvfile:
		writer = csv.writer(csvfile)
		# writer.writerow(['RollNumber','Name','Current Branch', 'Destination Branch'])
		for curStudent in students:
			if(curStudent.tempbranch != curStudent.branch):
				writer.writerow([curStudent.roll,curStudent.name,branches[curStudent.branch].name,branches[curStudent.tempbranch].name])
			else:
				writer.writerow([curStudent.roll,curStudent.name,branches[curStudent.branch].name,"Branch Unchanged"])


branchchange(sys.argv[1],sys.argv[2])