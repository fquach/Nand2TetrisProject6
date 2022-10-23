from parser import Parser
from code import Code

# opens input file (Prog.asm) and gets ready to process it
class AssemblerNoSymb:
	def __init__(self,path):
		self.parser = Parser(path)
		self.code = Code()
		ind1 = path.find('/')
		ind2 = path.find('.')
		writefile = path[:ind1] + "/" + path[ind1+1:ind2]
		self.file = open(writefile + '1.hack', 'w')

	def binary(self,str):
		return "{0:b}".format(int(str))
	
	def createOutput(self):
		while self.parser.hasMoreCommands():
			self.parser.advance()
			instructType = self.parser.instructionType()

			match instructType:
				case 'A_INSTR': 	# A Instruction
					symbol = self.parser.symbol()
					bin_symbol = self.binary(symbol)
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
	for path in ["add/Add.asm", "max/MaxL.asm", "pong/PongL.asm", "rect/RectL.asm"]:
		assemb_nosymb = AssemblerNoSymb(path)
		assemb_nosymb.createOutput()