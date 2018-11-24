'''
percision = number of points classiffied correctly / all points
recall = total selected correctly / total selected correctly + total not selected correctly 
f-measure = 2PR/(P+R)

folder movies reviews

number total = 13865
5 = 11130
1 = 2735

'''

execfile('bayes_best.py')
bc = Bayes_Classifier()
iFileList = []
for fFileObj in os.walk("movies_reviews/"):
    iFileList = fFileObj[2]
    break
results = {'total' : 0, 'true positives' : 0, 'false positives': 0, 'true negatives': 0 ,'false negatives': 0}
for i in iFileList:
    fileText = bc.loadFile("movies_reviews/"+i)
    results['total'] += 1
    result = bc.classify_bi(fileText)
    if 'movies-5' in i:
        if result == 'positive':
            results['true positives'] += 1
        else:
            results['false positives'] += 1
    if 'movies-1' in i:
        if result == 'negative':
            results['true negatives'] += 1
        else:
            results['false negatives'] += 1
precision = results['true positives'] / (results['true positives'] + results['false positives'])
recall = results['true positives'] / (results['true positives'] + results['false negatives'])
fmeasure = (2 * precision * recall) / (precision + recall) 

print('prescsion '+str(precision))
print('recall '+ str(recall))
print('f-measure '+str(fmeasure))
