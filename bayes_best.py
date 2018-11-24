import math, os, pickle, re, csv, string, statistics

class Bayes_Classifier:
   #some stuff was taken from here https://machinelearningmastery.com/deep-learning-bag-of-words-model-sentiment-analysis/
   #the concept of stop words and the new tokenize method
   stop_words = ['ourselves', 'hers', 'between', 'yourself', 'but', 'again', 'there', 'about', 
   'once', 'during', 'out', 'very', 'having', 'with', 'they', 'own', 'an', 'be', 'some', 'for',
   'do', 'its', 'yours', 'such', 'into', 'of', 'most', 'itself', 'other', 'off', 'is', 's', 'am', 
   'or', 'who', 'as', 'from', 'him', 'each', 'the', 'themselves', 'until', 'below', 'are', 'we', 
   'these', 'your', 'his', 'through', 'don', 'nor', 'me', 'were', 'her', 'more', 'himself', 'this', 
   'down', 'should', 'our', 'their', 'while', 'above', 'both', 'up', 'to', 'ours', 'had', 'she', 'all', 
   'no', 'when', 'at', 'any', 'before', 'them', 'same', 'and', 'been', 'have', 'in', 'will', 'on', 'does',
   'yourselves', 'then', 'that', 'because', 'what', 'over', 'why', 'so', 'can', 'did', 'not',
   'now', 'under', 'he', 'you', 'herself', 'has', 'just', 'where', 'too', 'only', 'myself', 'which',
   'those', 'i', 'after', 'few', 'whom', 't', 'being', 'if', 'theirs', 'my', 'against', 'a', 'by',
   'doing', 'it', 'how', 'further', 'was', 'here', 'than' ]
   def __init__(self):
      '''self method initializes and trains the Naive Bayes Sentiment Classifier.  If a 
      cache of a trained classifier has been stored, it loads self cache.  Otherwise, 
      the system will proceed through training.  After running self method, the classifier 
      is ready to classify input text.'''
      if os.path.exists('good.txt'):
         self.GoodWords = self.load('good.txt')
         self.BadWords = self.load('bad.txt')
         self.BigramsGoodWords = self.load('bi_good.txt')
         self.BigramsBadWords = self.load('bi_bad.txt')
      else:
         self.train()


   def train(self):   
      '''Trains the Naive Bayes Sentiment Classifier.'''
      IFileList = []
      self.GoodWords = {}
      self.BadWords = {}
      self.BigramsBadWords = {}
      self.BigramsGoodWords = {}
      for fFileObj in os.walk('movies_reviews/'):
         IFileList = fFileObj[2]
         break
      for ifl in IFileList:
         if ifl == 'movies-5-24670.txt':
            print('hello')
         full_text = self.loadFile('movies_reviews/'+ifl)
         text = self.tokenize(full_text)
         if  re.match('movies-1-\d+.txt$', ifl):
            for U_t in text:
               t= U_t.lower()
               if t in self.BadWords.keys():
                  self.BadWords[t]+=1
               else:
                  self.BadWords[t] = 1
            length = len(text)
            for i in range(0,length):
               if i + 1 < length:
                  if text[i]+' '+text[i+1] in self.BigramsBadWords.keys():
                     self.BigramsBadWords[text[i]+' '+text[i+1]] += 1
                  else:
                     self.BigramsBadWords[text[i]+' '+text[i+1]] = 1
            continue
         if re.match('movies-5-\d+.txt$', ifl):
            for U_t in text:
               t=U_t.lower()
               if t in self.GoodWords.keys():
                  self.GoodWords[t]+=1
               else:
                  self.GoodWords[t] = 1
            length = len(text)
            for i in range(0,length):
               if i + 1 < length:
                  if text[i]+' '+text[i+1] in self.BigramsGoodWords.keys():
                     self.BigramsGoodWords[(text[i]+' '+text[i+1])] += 1
                  else:
                     self.BigramsGoodWords[(text[i]+' '+text[i+1])] = 1
      
      self.save(self.BigramsGoodWords,'bi_good.txt')
      self.save(self.BigramsBadWords,'bi_bad.txt')
      self.save(self.GoodWords,'good.txt')
      self.save(self.BadWords,'bad.txt')

   def classify_bi(self,sText):
      '''same thing as classiffy but for bigram feature turned on'''
      GoodSum=0
      BadSum=0
      GoodProbability=1
      BadProbability=1
      GoodKeys = self.BigramsGoodWords.keys()
      BadKeys = self.BigramsBadWords.keys()
      ListText =self.tokenize_bi(sText)
      for i in GoodKeys:
         GoodSum += self.BigramsGoodWords[i]
      for i in BadKeys:
         BadSum += self.BigramsBadWords[i]
      for i in ListText:
         if i not in BadKeys:
            self.BigramsBadWords[i] = 1
            BadSum+=1
         if i not in GoodKeys:
            self.BigramsGoodWords[i] = 1
            GoodSum += 1 
      for i in ListText:
         BadProbability += math.log10(self.BigramsBadWords[i] / BadSum)
         GoodProbability += math.log10(self.BigramsGoodWords[i] / GoodSum)
      if -.3< GoodProbability - BadProbability < .3:
         return 'neutral'
      if GoodProbability > BadProbability:
         return 'positive'
      if GoodProbability < BadProbability:
         return 'negative'
      return 'neutral'
      
    
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
      if -.3< GoodProbability - BadProbability < .3:
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

   def tokenize_bi(self,sText):
      '''just like tokenize but for bigrams'''
      sText = str.lower(sText)
      bigram = []
      tokens = sText.split()
      table = str.maketrans('', '', string.punctuation)
      tokens = [w.translate(table) for w in tokens]
      tokens = [word for word in tokens if word.isalpha()]
      tokens = [w for w in tokens if not w in self.stop_words]
      tokens = [word for word in tokens if len(word) > 1]
      length = len(tokens)
      for i in range(0,length):
         if i + 1 < length:
            bigram.append(tokens[i]+' '+tokens[i+1])
      return bigram




   def tokenize(self, sText): 
      '''Given a string of text sText, returns a list of the individual tokens that 
      occur in that string (in order).'''
      sText = str.lower(sText)
      sText.replace('-', ' ')
      tokens = sText.split()
      table = str.maketrans('', '', string.punctuation)
      tokens = [w.translate(table) for w in tokens]
      tokens = [word for word in tokens if word.isalpha()]
      tokens = [w for w in tokens if not w in self.stop_words]
      tokens = [word for word in tokens if len(word) > 1]
      return  tokens


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

