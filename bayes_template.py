import math, os, pickle, re

class Bayes_Classifier:

   self.GoodWords
   self.BadWords

   def __init__(self, trainDirectory = "movie_reviews/"):
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
         if  re.match('^movies-1-\d+.txt$', ifl):
            for t in text:
               if t in BadWords.keys():
                  BadWords[t]+=1
               else:
                  BadWords[t] = 1
            continue
         if re.match('^movies-5-\d+.txt$', ifl):
            for t in text:
               if t in GoodWords.keys():
                  GoodWords[t]+=1
               else:
                  GoodWords[t] = 1
      self.save(GoodWords,'good.txt')
      self.save(BadWords,'bad.txt')

      
      
    
   def classify(self, sText):
      '''Given a target string sText, self function returns the most likely document
      class to which the target string belongs. self function should return one of three
      strings: "positive", "negative" or "neutral".
      '''

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
