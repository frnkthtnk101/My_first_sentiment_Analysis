from bayes import Bayes_Classifier

bc = Bayes_Classifier()
statement = 'I love my AI class!'
print('classify   : '+bc.classify(statement))
#print('classify bi: '+bc.classify_bi(statement))
#bc.get_counts()