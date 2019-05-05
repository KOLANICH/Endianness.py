from plumbum import cli
from . import *

class EndiannessCLI(cli.Application):
	debug=cli.Flag(("d", "debug"), help="Shows the remapping")
	
	def main(self, encoded:str="l4", size: int=2, number:int=None):
		e=Endianness.parse(encoded)
		m=EndiannessMapping(e, size*8)
		
		slice2remap = slice(0, size*8, 1)
		slice2remap = slice(size*8-1, -1, -1)
		
		btz=[(s.index, s.indexee) for s in m.encode(slice2remap)]
		#print("btz", btz)
		print("="*64)
		
		for l in zip(*btz):
			print([list(slice2range(s)) for s in l])
		
		if number is not None:
			pass

if __name__ == "__main__":
	EndiannessCLI.run()
