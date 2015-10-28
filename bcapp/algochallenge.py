import csv, sys;
status = False
def branchchangechallenge(branchfile, studentfile):
	global status
	class Branch:
		def __init__(self,information,deptcode):
			self.code = deptcode
			self.sancStrength = int(information[1])
			self.name = information[0]
			self.origStrength = int(information[2])
			self.curStrength = int(information[2])
			self.maxStrength = int(self.sancStrength + round(self.sancStrength/10.0))
			self.minStrength = self.sancStrength*0.75
			self.MaxUnallowedCPI = 6.99
			self.MaxUntransferredCPI = 6.99
			self.MinAllowedCPI = 10.1
			self.MinTransferredCPI = 10.1
			# self.minStrength = int(self.sancStrength - round(self.sancStrength/4,0))
		def resetdata(self):
			self.MaxUnallowedCPI = 6.99
			self.MaxUntransferredCPI = 6.99

		def cutoffCPI(self):
			if self.MinAllowedCPI==10.1:
				return "NA"
			else:
				return self.MinAllowedCPI

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

		def finalStatus(self):
			if(not self.isEligible()):
				return "Ineligible"
			elif(self.tempbranch == self.branch):
				return "Branch Unchanged"
			else:
				return branches[self.tempbranch].name
		
		def allotBranch(self):
			status = -1
			for dept in self.preferences:
				CPI = self.cpi
				if(dept == self.tempbranch):
					break
				#print(name,branches[status].curStrength)
					
				if(CPI == branches[dept].MinAllowedCPI):
					branches[dept].curStrength = branches[dept].curStrength + 1
					branches[self.tempbranch].curStrength = branches[self.tempbranch].curStrength -1
					branches[self.tempbranch].MinTransferredCPI = CPI
					self.tempbranch = dept
					status = dept
					break

				elif(branches[dept].curStrength < branches[dept].maxStrength):
					if(CPI < branches[self.tempbranch].MaxUntransferredCPI):
						break;
					updatedStrength = branches[self.tempbranch].curStrength -1

					if(CPI >= 9.00 or ((updatedStrength >= branches[self.tempbranch].minStrength or CPI == branches[self.tempbranch].MinTransferredCPI) and CPI >= branches[dept].MaxUnallowedCPI)):
						branches[dept].curStrength = branches[dept].curStrength + 1
						branches[self.tempbranch].curStrength = updatedStrength
						branches[self.tempbranch].MinTransferredCPI = CPI
						branches[dept].MinAllowedCPI = min(branches[dept].MinAllowedCPI,CPI)
						self.tempbranch = dept
						status = dept
						break


			if(status !=-1):
				self.preferences = self.preferences[0:self.preferences.index(status)]
			elif(branches[self.tempbranch].curStrength -1 < branches[self.tempbranch].minStrength):
				branches[self.tempbranch].MaxUntransferredCPI = max(curStudent.cpi, branches[self.tempbranch].MaxUntransferredCPI)
			return status

	def explore(i,initialbranch):
		global status
		for pref in tempStudents[i].preferences:
			curstack.append([i,pref])
			if pref == initialbranch:
				status = True;
				return
			for j,newStudent in enumerate(tempStudents):
				if (newStudent.tempbranch == pref):
					isparent = False
					for parent in curstack:
						if(parent[0]==j):
							isparent = True
							break;
					if not isparent:
						explore(j,initialbranch)
						if status:
							return
			curstack.pop()

	branches = []
	students = []
	numbranches = 0
	branchmap = {}
	ineligibleStudents = []
	finalList = []
	finalBranchList = []

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
	 
	#for curbranch in branches:
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
			
			if(not curStudent.preferences):
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
		for branch in branches:
			branch.resetdata()
	curstack = []
	status = False		
	for i,curStudent in enumerate(tempStudents):
		curstack = []
		status = False
		explore(i,curStudent.tempbranch)
		for j in curstack:
			tempStudents[j[0]].tempbranch = j[1]
			tempStudents[j[0]].preferences = tempStudents[j[0]].preferences[0:tempStudents[j[0]].preferences.index(j[1])]

	students.extend(ineligibleStudents)
	students = list(sorted( students, key = lambda x: (x.roll,x.name.lower())))
	for curStudent in students:
		finalList.append([curStudent.roll, curStudent.name, branches[curStudent.branch].name,curStudent.finalStatus()])
	for curbranch in branches:
		finalBranchList.append([curbranch.name, curbranch.cutoffCPI(), curbranch.sancStrength, curbranch.origStrength, curbranch.curStrength])
	return finalList,finalBranchList

