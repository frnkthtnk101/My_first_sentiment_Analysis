import time

testFile = "bayes_template.py"
trainDir = "movies_reviews/"
testDir = "db_txt_files/"

execfile(testFile)
bc = Bayes_Classifier(trainDir)
	
iFileList = []

for fFileObj in os.walk(testDir ):
	iFileList = fFileObj[2]
	break
print('%d test reviews.', len(iFileList))

results = {"negative":0, "neutral":0, "positive":0}

print("\nFile Classifications:")
i =0
t = time.time()
for filename in iFileList:
	fileText = bc.loadFile(testDir + filename)
	result = bc.classify(fileText)
	if i %1000 == 0 :
		te = time.time() - t
		print(i, te)
		t =time.time()
	results[result] += 1
	i+=1

print("\nResults Summary:")
for r in results:
	print ("%s: %d",r, results[r])