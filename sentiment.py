import math, os, pickle, re,argparse,time


def main(test_files,best):
    print('remember to train the bayes')
    if(best):
        execfile('bayes_best.py')
    else:
        execfile('bayes.py')
    bc = Bayes_Classifier()
    iFileList = []
    for fFileObj in os.walk(test_files ):
        iFileList = fFileObj[2]
        break
    print('%d test reviews.', len(iFileList))
    results = {"negative":0, "neutral":0, "positive":0}
    print("\nFile Classifications:")
    t = time.time()

    for filename in iFileList:
        fileText = bc.loadFile(test_files + filename)
        result = bc.classify(fileText)
        te = time.time() - t
        print(filename,result,'%.2f seconds'%te)
        t = time.time()
        results[result] += 1

    print("\nResults Summary:")
    for r in results:
	    print (r,':', results[r])



if __name__ == '__main__':
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument('testfiles',help='takes the path of a directory of text files',type = str)
    PARSER.add_argument('best',help = 'use the best bay', type = bool)
    ARGS = PARSER.parse_args()
    main(ARGS.testfiles,ARGS.best)
