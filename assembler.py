from parser import Parser
from code import Code
from symboltable import SymbolTable

# opens input file (Prog.asm) and gets ready to process it
class Assembler:
	def __init__(self,path):
		self.parser = Parser(path)
		self.code = Code()
		self.symb_table = SymbolTable()

		ind1 = path.find('/')
		ind2 = path.find('.')

		writefile = path[:ind1] + "/" + path[ind1+1:ind2]
		self.file = open(writefile + '2.hack', 'w')

	def binary(self,str):
		return "{0:b}".format(int(str))

	def firstPass(self):
		counter = 0
		while self.parser.hasMoreCommands():
			self.parser.advance()
			instructType = self.parser.instructionType()
			match instructType:
				case 'A_INSTR': 	# A Instruction
					counter += 1
				case 'C_INSTR':		# C Instruction
					counter += 1
				case 'L_INSTR':
					symbol = self.parser.symbol()
					self.symb_table.addEntry(symbol,counter)
				case _:
					raise ValueError("Instruction type must be A, C, or L.")

	def secondPass(self):
		ram_addr = 16
		self.parser.i = -1

		while self.parser.hasMoreCommands():
			self.parser.advance()
			instructType = self.parser.instructionType()

			if instructType == 'A_INSTR':
				symbol = self.parser.symbol()
				
				if (not symbol.isdigit()) and (not self.symb_table.contains(symbol)):
					self.symb_table.addEntry(symbol, ram_addr)
					ram_addr += 1
	
	def createOutput(self):
		self.parser.i = -1
		while self.parser.hasMoreCommands():
			self.parser.advance()
			instructType = self.parser.instructionType()

			match instructType:
				case 'A_INSTR': 	# A Instruction
					symbol = self.parser.symbol()
					if symbol.isdigit():
						bin_symbol = self.binary(symbol)
					else:
						symb_add = self.symb_table.getAddress(symbol)
						bin_symbol = self.binary(symb_add)
					a_instr = '0' * (16 - len(bin_symbol)) + bin_symbol
					self.file.write(a_instr + '\n')
				case 'C_INSTR':
					dest_p = self.parser.dest()
					dest = self.code.dest(dest_p)

					comp_p = self.parser.comp()
					comp = self.code.comp(comp_p)

					jump_p = self.parser.jump()
					jump = self.code.jump(jump_p)

					c_instr = '111' + comp + dest + jump
					self.file.write(c_instr + '\n')
				case _:
					pass
		self.file.close()

if __name__ == "__main__":
	for path in ["add/Add.asm", "max/Max.asm", "pong/Pong.asm", "rect/Rect.asm"]:
		assemb = Assembler(path)
		assemb.firstPass()
		assemb.secondPass()
		assemb.createOutput()