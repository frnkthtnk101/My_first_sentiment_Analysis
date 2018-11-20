import math, os, pickle, re, csv

class Bayes_Classifier:


   def __init__(self):
      '''self method initializes and trains the Naive Bayes Sentiment Classifier.  If a 
      cache of a trained classifier has been stored, it loads self cache.  Otherwise, 
      the system will proceed through training.  After running self method, the classifier 
      is ready to classify input text.'''
      if os.path.exists('good.txt'):
         self.GoodWords = self.load('good.txt')
         self.BadWords = self.load('bad.txt')
      else:
         self.train()


   def train(self):   
      '''Trains the Naive Bayes Sentiment Classifier.'''
      IFileList = []
      self.GoodWords = {}
      self.BadWords = {}
      for fFileObj in os.walk('movies_reviews/'):
         IFileList = fFileObj[2]
         break
      for ifl in IFileList:
         full_text = self.loadFile('movies_reviews/'+ifl)
         text = self.tokenize(full_text)
         if  re.match('movies-1-\d+.txt$', ifl):
            for U_t in text:
               t= U_t.lower()
               if t in self.BadWords.keys():
                  self.BadWords[t]+=1
               else:
                  self.BadWords[t] = 1
            continue
         if re.match('movies-5-\d+.txt$', ifl):
            for U_t in text:
               t=U_t.lower()
               if t in self.GoodWords.keys():
                  self.GoodWords[t]+=1
               else:
                  self.GoodWords[t] = 1
      self.save(self.GoodWords,'good.txt')
      self.save(self.BadWords,'bad.txt')

      
      
    
   def classify(self, sText):
      '''Given a target string sText, self function returns the most likely document
      class to which the target string belongs. self function should return one of three
      strings: "positive", "negative" or "neutral".
      '''
      GoodSum=0
      BadSum=0
      GoodProbability=1
      BadProbability=1
      GoodKeys = self.GoodWords.keys()
      BadKeys = self.BadWords.keys()
      ListText =self.tokenize(sText)
      WordsInDictionary = True
      for i in GoodKeys:
         GoodSum += self.GoodWords[i]
      for i in BadKeys:
         BadSum += self.BadWords[i]
      for i in ListText:
         if i not in BadKeys:
            self.BadWords[i] = 1
            BadSum+=1
         if i not in GoodKeys:
            self.GoodWords[i] = 1
            GoodSum += 1

      for i in ListText:
         BadProbability += math.log10(self.BadWords[i] / BadSum)
         GoodProbability += math.log10(self.GoodWords[i] / GoodSum)
      
      if -0.5<GoodProbability - BadProbability<.5:
         return 'neutral'
      if GoodProbability > BadProbability:
         return 'positive'
      if GoodProbability < BadProbability:
         return 'negative'
      return 'neutral'
         

   def loadFile(self, sFilename):
      '''Given a file name, return the contents of the file as a string.'''

      f = open(sFilename, "r")
      sTxt = f.read()
      f.close()
      return sTxt
   
   def save(self, dObj, sFilename):
      '''Given an object and a file name, write the object to the file using pickle.'''

      f = open(sFilename, "wb")
      p = pickle.Pickler(f)
      p.dump(dObj)
      f.close()
   
   def load(self, sFilename):
      '''Given a file name, load and return the object stored in the file.'''
      f = open(sFilename, "rb")
      u = pickle.Unpickler(f)
      dObj = u.load()
      f.close()
      return dObj

   def tokenize(self, sText): 
      '''Given a string of text sText, returns a list of the individual tokens that 
      occur in that string (in order).'''

      lTokens = []
      sToken = ""
      for c in sText:
         if re.match("[a-zA-Z0-9]", str(c)) != None or c == "\'" or c == "_" or c == '-':
            sToken += c
         else:
            if sToken != "":
               lTokens.append(sToken)
               sToken = ""
            if c.strip() != "":
               lTokens.append(str(c.strip()))
               
      if sToken != "":
         lTokens.append(sToken)

      return lTokens

   def get_counts(self):
      good_keys = self.GoodWords.keys()
      bad_keys = self.BadWords.keys()
      with open('GoodWords.csv','w') as csvfile:
         writer = csv.writer(csvfile,delimiter = ',',quoting=csv.QUOTE_MINIMAL)
         writer.writerow(["word","count"])
         for gk in good_keys:
            writer.writerow([gk,self.GoodWords[gk]])
      with open('BadWords.csv','w') as csvfile:
         writer = csv.writer(csvfile,delimiter = ',',quoting=csv.QUOTE_MINIMAL)
         writer.writerow(["word","count"])
         for gk in bad_keys:
            writer.writerow([gk,self.BadWords[gk]])
      with open('keys.csv','w') as csvfile:
         writer = csv.writer(csvfile,delimiter = ',',quoting=csv.QUOTE_MINIMAL)
         writer.writerow(["keys_set","count"])
         writer.writerow(["good set",len(good_keys)])
         writer.writerow(["bad set",len(bad_keys)])

