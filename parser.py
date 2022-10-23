# reads and parses an instruction
class Parser:

	# path: datapath of file to read
	# creates a Parser and opens the src text file
	def __init__(self,path):
		self.file = open(path,'r')
		self.raw_lines = self.file.readlines()	# raw_lines is a list of file's lines
		self.processed_lines = []				# start as empty list

		for line in self.raw_lines:
			# skip if line is comment or empty
			if line[:2] == "//" or line == "\n":	
				continue						

			# if line contains comment, omit comment
			if "//" in line:
				line = line[:line.find("//")]

			# remove spaces
			line = line.replace(" ","")

			# final processing before adding to list
			ln = []
			for char in line:
				if char not in ['','\n']:
					ln.append(char)
			self.processed_lines.append(''.join(ln))

		self.i = -1					# index of current instruction
		self.instruction = None		# current instruction
		self.total_instrs = len(self.processed_lines)

	# check if there is more work to do
	def hasMoreCommands(self):
		return self.i < self.total_instrs - 1
		
	# gets next instruction and makes it the current instruction
	def advance(self):
		if self.hasMoreCommands():
			self.i += 1
			self.instruction = self.processed_lines[self.i]
			# self.instruction = self.process_symbol(self.instruction)

	# returns instruction type (A, L, or C) of current instruction
	def instructionType(self):
		if self.instruction[0] == '@':
			return 'A_INSTR'
		elif self.instruction[0] == '(':
			return 'L_INSTR'
		else:
			return 'C_INSTR'

	# returns instruction's symbol (string)
	def symbol(self):
		if self.instructionType() == 'A_INSTR':
			return self.instruction[1:]		# return instruction without @
		elif self.instructionType() == 'L_INSTR':
			return self.instruction[1:-1]		# return instruction without ()
		else:
			raise ValueError("Instruction type should be A or L.")

	# returns instruction's dest field
	def dest(self):
		if self.instructionType() == 'C_INSTR':
			ind = self.instruction.find('=')
			if ind != -1:
				return self.instruction[:ind]		# dest is part before =
			else:
				return 'null'
		else:
			raise ValueError("Instruction type should be C.")

	# returns instruction's comp field
	def comp(self):
		if self.instructionType() == 'C_INSTR':
			ind1 = self.instruction.find('=')
			ind2 = self.instruction.find(';')
			if (ind1 != -1) and (ind2 != -1):
				return self.instruction[ind1+1:ind2]	# between = and ;
			elif (ind1 != -1) and (ind2 == -1):
				return self.instruction[ind1+1:]		# after =
			elif (ind1 == -1) and (ind2 != -1):	
				return self.instruction[:ind2]			# before ;
			elif (ind1 == -1) and (ind2 == -1):
				return self.instruction					# it's the only part that exists
		else:
			raise ValueError("Instruction type should be C.")

	# returns instruction's jump field
	def jump(self):
		if self.instructionType() == 'C_INSTR':
			ind = self.instruction.find(';')
			if ind != -1:
				return self.instruction[ind+1:]		# jump is part after ;
			else:
				return 'null'
		else:
			raise ValueError("Instruction type should be C.")
	
		
