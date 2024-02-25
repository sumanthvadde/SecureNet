# from checkBrand import checkBrand
import gib_detect as gib
from tqdm import tqdm
import statistics
import tldextract
import json
import csv
import re
import os
import sys
from checkBrand import checkBrand

brandPath = "allbrands.txt"
keywordPath = "keywords.txt"
brand = checkBrand(brandPath)

def numOfSubdom(site):
	s = re.search("//",site)
	if s:
		site = site[s.end():]
	e = re.search("/",site)
	if e:
		site = site[:e.end()-1]
	site = site.split(".")
	# one for domain extension eg. com,edu,in 
	num = len(site)-1
	if 'www' in site:
		num = num-1
	return num

def separateWords(site):
	return re.split(r"\.|\/|-|\?|=|#|&|_|@|:\/\/",site)

def wordfeatures(wordList):
	smallest = len(wordList[0])
	largest = 0
	avg = 0
	count = 0
	if(wordList[0]=='www'):
		smallest = len(wordList[1])
	for word in wordList:
		if len(word) != 0:
			if word!='www' and len(word)<smallest:
				smallest = len(word)
			if len(word)> largest:
				largest = len(word)
			avg += len(word)
			count+=1
	avg = int(avg/count)
	return([smallest,largest,avg])

def keyCount(wordList):
	count = 0
	for word in wordList:
		if word in keywordList:
			count += 1
	return count

def findsd(wordList):
	lenList = []
	for word in wordList:
		if(len(word)!=0):
			lenList.append(len(word))
	return round(statistics.stdev(lenList),2)

def checktld(site):
	# count for www, .com, presence of tld, len of path
	result = [0,0,0,0]
	s = re.search("//",site)
	if s:
		site = site[s.end():]
	e = re.search("/",site)
	if e:
		path = site[e.end():]
		site = site[:e.end()-1]
	dot = re.search(".",site)
	site = site[dot.end()-1:]
	arr = re.split(r"\.",site)
	tld = arr[-1]
	www = arr[0]
	if tld == "com":
		result[1] = 1
	if www == "www":
		result[0] = 1
	if tld in ["com","org","net","gov","in"]:
		result[2] = 1
	result[3] = len(site)
	return result

def checkAlexa(site):
	if site in top:
		return 1
	return 0

def domainAnalysis(site):
	res = tldextract.extract(site)
	subdomain = res.subdomain
	domain = res.domain
	suffix = res.suffix
	result = [len(subdomain),len(domain+suffix)]
	result.append(checkAlexa(domain+"."+suffix))
	extracted = subdomain.split(r"\.")+domain.split(r"\.")
	if gib.check_word(extracted) == 0:
		result.append(0)
	else:
		result.append(1)
	return result

def countDig(site):
#	subdomain, domain, path
	result = [0,0,0]
	res = tldextract.extract(site)
	subdomain = res.subdomain
	domain = res.domain
	s = re.search("//",site)
	if s:
		site = site[s.end():]
	e = re.search("/",site)
	path = ""
	if e:
		path = site[e.end():]
	result[0] = len(re.findall(r"[0-9]",subdomain))
	result[1] = len(re.findall(r"[0-9]",domain))
	result[2] = len(re.findall(r"[0-9]",path))
	return result

def pathAnalysis(site):
	result = [0,0,0,0,0,0,0,0]
	s = re.search("//",site)
	if s:
		site = site[s.end():]
	e = re.search("/",site)
	path = ""
	if e:
		path = site[e.end():]
	result[0] = len(re.findall(r"\-",path))
	result[1] = len(re.findall(r"\.",path))
	result[2] = len(re.findall(r"\/",path))
	result[3] = len(re.findall("@",path))
	result[4] = len(re.findall(r"\?",path))
	result[5] = len(re.findall("&",path))
	result[6] = len(re.findall(r"=",path))
	result[7] = len(re.findall("_",path))
	return result

with open(keywordPath,'r') as keywords:
	# print("Processing keywords")
	keywordList=[]
	for word in keywords:
		keywordList.append(word.lower().strip())

with open('top-1m.csv','r') as top1m:
	# print('Generating Alexa top1m')
	top=[]
	for line in top1m:
		top.append(line.strip().split(',')[1].lower())
all_feature = []
for i in range(1, len(sys.argv)):
	site = sys.argv[i]
	feature=[]
	allWords = separateWords(site)
	feature.append(len(allWords))
	if re.search('^https', site):
		feature.append(1)
	else:
		feature.append(0)
	feature.append(numOfSubdom(site))
	feature += brand.check(allWords)
	feature.append(gib.check_word(allWords))
	feature += wordfeatures(allWords)
	feature.append(keyCount(allWords))
	feature.append(findsd(allWords))
	feature += checktld(site)
	feature += domainAnalysis(site)
	feature += pathAnalysis(site)
	feature += countDig(site)
	all_feature.append(feature)

import keras
from keras.models import Sequential
from keras.models import model_from_json
from keras.layers import Dense
import sys
import numpy as np
import os

all_feature = np.array(all_feature)

json_file = open('classifier.json', 'r')
loaded_classifier_json = json_file.read()
json_file.close()
loaded_classifier = model_from_json(loaded_classifier_json)
# load weights into new classifier
loaded_classifier.load_weights("classifier.h5")

loaded_classifier.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])
output = loaded_classifier.predict(all_feature)
print(output>0.95)

# file_list = ["data_legitimate_36400.json","data_phishing_37175.json"]

# for i in range(2):
# 	phishing = i
# 	with open(file_list[i],'r') as legim:
# 	# with open("test.json",'r') as legim:
# 		legim = json.load(legim)
# 		if i == 0:
# 			method = 'w'
# 		else:
# 			method = 'a'
# 		count = 0
# 		with open("final.csv",method,encoding="utf-8",newline="") as final:
# 			csvWriter = csv.writer(final, delimiter=",")
# 			if i==0:
# 				csvWriter.writerow(['raw_length','https','countSubdomain','countRandom','smallestWord','largestWord','avgWord','keyword Count','sd of words','com','www','tld','pathLen','subdomainLen','domainLen','Alexa_top_1m','domain_gibb','dash','dot','slash','at','question','ampersand','equal','underscore','phishing'])
# 			for site in tqdm(legim):
# 				feature=[]
# 				allWords = separateWords(site)
# 				feature.append(len(allWords))
# 				if re.search('^https', site):
# 					feature.append(1)
# 				else:
# 					feature.append(0)
# 				feature.append(numOfSubdom(site))
# 				# feature += brand.check(allWords)
# 				feature.append(gib.check_word(allWords))
# 				feature += wordfeatures(allWords)
# 				feature.append(keyCount(allWords))
# 				feature.append(findsd(allWords))
# 				feature += checktld(site)
# 				feature += domainAnalysis(site)
# 				feature += pathAnalysis(site)
# 				feature.append(phishing)
# 				count += 1
# 				csvWriter.writerow(feature)

