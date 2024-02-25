class checkBrand:
	def __init__(self,brandPath):
		# print("Initialising")
		self.brandPath = brandPath
		self.brandList = []
		with open(self.brandPath,'r') as f:
			for line in f:
				self.brandList.append(line.lower().strip())
	def check(self,wordList):
		l = len(wordList)
		result = [0,0] 
		for i in range(l):
			if len(wordList[i])>5:
				if wordList[i].lower() in self.brandList:
					result[0]=1
					result[1]+=1
		return result