import re
import itertools
from rangeslicetools import *
from copy import deepcopy

groupsRx=re.compile("([bl])(\d+)")

inf = float("inf")

def isPowerOf2(n:int):
	return not (n & (n-1))

class Level():
	__slots__=("size", "big")
	def __init__(self, size:int, big:bool):
		self.size=size
		self.big=big
	
	def __repr__(self):
		return self.__class__.__name__+"<"+("b" if self.big else "l") + str(self.size) +">"
	
	def cmpTuple(self):
		return (self.size, self.big)
	
	def __eq__(self, other):
		return self.cmpTuple() == other.cmpTuple()
	
	def __hash__(self):
		return hash(self.cmpTuple())


def parse_(encoded:str):
	cumulative=0
	prevSize = inf
	while(encoded):
		m=groupsRx.match(encoded)
		if not m:
			raise Exception("Invalid endianness encoded at pos "+str(cumulative)+": "+encoded)
		bl, sz = m.groups()
		bl = (bl == "b")
		sz = int(sz)
		assert sz > 0
		assert prevSize > sz
		assert isPowerOf2(sz)
		#assert prevSize % size == 0
		encoded=encoded[m.end():]
		cumulative+=m.end()
		yield Level(sz, bl)

def simplify(parsed:typing.Iterable[Level], initialBigStatus:bool=True):
	parsed = iter(parsed)
	
	prevLevel = Level(None, initialBigStatus)
	for l in parsed:
		#print("main", l, initialBigStatus, initialBigStatus != l.big)
		if prevLevel.big != l.big:
			yield l
		prevLevel = l
	

def parse(encoded:str):
	return tuple(simplify(parse_(encoded)))

def chunks(it:typing.Iterable[typing.Any], chunkLen:int):
	it = iter(it)
	chunkProto = [None]*chunkLen
	while True:
		chunk = type(chunkProto)(chunkProto)
		for i in range(chunkLen):
			chunk[i] = next(it)
		yield chunk

wellKnown = {}


class Endianness:
	"""
	levels:
		key: block size
		value: True if big endian, else False
	"""
	
	def __init__(self, levels):
		self.levels = levels
	
	def bits(self, levelChunks:typing.Union[int, typing.Iterable[slice]]):
		"""Returns a remapping mapping slices to big-endian bits.
		if `levelChunks` is of `int`, it is treated as size of a slice to remap
		if `levelChunks` is a slice or a range, it is remapped
		if `levelChunks` is an iterable of a range or a slice, it is remapped too.
		An example:
		let we have a 16-bit Big Endian number (8b in our notation), then its power of 2 sequence is
		15 14 13 12 11 10 09 08 07 06 05 04 03 02 01 00.
		It is encoded as an iterable [slice(15, -1, -1)]
		and let we want to remap it to LE (8l in our notation)
		so we call
		wellKnown["little"].bits(wellKnown["big"].bits(2*8))
		then we will get
		[slice(7, -1, -1), slice(15, 7, -1)]
		
		If our underlying hardware endian is little endian, we can remap
		yourCustomEndian.bits(wellKnown["little"].bits(2*8))
		
		calling 
		wellKnown["little"].bits(wellKnown["little"].bits(2*8))
		you are expected to get identity mapping (in BE notation)
		"""
		levelChunks = deepcopy(levelChunks)
		
		if isinstance(levelChunks, int):
			levelChunks = srev(slice(0, levelChunks, 1))
		if isinstance(levelChunks, (range, slice)):
			levelChunks = [levelChunks]
		if isinstance(levelChunks, tuple):
			levelChunks = list(levelChunks)
		
		for l in self.levels:
			#print("level", l)
			levelChunksNew = []
			for i in range(len(levelChunks)):
				#print("levelChunks[", i, "] 0", levelChunks[i])
				levelChunks[i] = schunks(levelChunks[i], l.size)
				#print("levelChunks[", i, "] 1", levelChunks[i])
				if not l.big:
					levelChunks[i] = list(reversed(levelChunks[i]))
				levelChunksNew += levelChunks[i]
			levelChunks = levelChunksNew
		
		#print("levelChunks final", levelChunks)
		return sjoin(levelChunks)
	
	def __repr__(self):
		return self.__class__.__name__+"("+repr(self.levels)+")"
	
	@classmethod
	def parse(cls, encoded:str):
		return cls(parse(encoded))
	
	

class EndiannessMapping():
	def __init__(self, endianness, size, old=None):
		self.size = size
		self.endianness = endianness
		if old is None:
			old = wellKnown["big"]
		self.oldBits = old.bits(self.size)
		
		#print("EndiannessMapping", "self.oldBits", self.oldBits[0]) # slice(15, -1, -1)
		self.mapping = self.endianness.bits(self.oldBits)
		#print("EndiannessMapping", "self.mapping", self.mapping) # [slice(7, -1, -1), slice(15, 7, -1)]
		#print("SliceSequence(", self.mapping, ",", self.oldBits[0], ")")
		self.forward = SliceSequence(self.mapping, self.oldBits[0])
		#print("EndiannessMapping", "self.forward", self.forward.tree) # <rangeslicetools._rangeslicetools.SliceSequence object at 0xb60cbdac>
	
	def encode(self, slc:slice):
		sliceRemap = mergeRangesInTreeLookupResult(self.forward[slc])
		return sliceRemap

wellKnown["be"] = wellKnown["big"] = Endianness(())
wellKnown["le"] = wellKnown["little"] = Endianness.parse("l8")
