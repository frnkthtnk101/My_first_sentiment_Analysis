'''
script to interact with the bayes sentiment analyizer
'''
import math, os, pickle, re,argparse

def remove_training_files():
    '''Removes the train files so the program can be trained
    again'''
    try:
        os.remove('good.txt')
        os.remove('bad.txt')
        os.remove('bi_bad.txt')
        os.remove('bi_good.txt')
    except:
        print('An exception was raise while removing files.\nThat is ok.')
        return True
    return True
    

def main(test_files,best,bigram,rows):
    '''
    main function
        decides what bayes to execute and captures the files
        from the directory. After, it classifies each file's
        contents
    '''
    if(best):
        execfile('bayes_best.py')
    else:
        execfile('bayes.py')
    bc = Bayes_Classifier()
    iFileList = []
    for fFileObj in os.walk(test_files ):
        iFileList = fFileObj[2]
        break
    results = {"negative":0, "neutral":0, "positive":0}
    print("\nFile Classifications:")
    for filename in iFileList:
        fileText = bc.loadFile(test_files + filename)
        if bigram:
            result = bc.classify_bi(fileText)
        else:
            result = bc.classify(fileText)
        if rows:
            print(filename,result)
        results[result] += 1

    print("\nResults Summary: ",str(len(iFileList)))
    for r in results:
	    print (r,':', results[r])



if __name__ == '__main__':
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument('testfiles',help='takes the path of a directory of text files',type = str)
    group = PARSER.add_argument_group()
    group.add_argument('-b','--best',action='store_true',help='use the best')
    group.add_argument('-bi','--bigram',action='store_true',help='use the bigram')
    group.add_argument('-t','--train',action='store_true',help='use to train the program')
    group.add_argument('-s','--showrows',action='store_true',help='show results')
    ARGS = PARSER.parse_args()
    if ARGS.bigram is True and ARGS.best is False:
        raise ValueError('you cannot call bigragm option with the best option')
    else:
        if ARGS.train:
            remove_training_files()
        main(ARGS.testfiles,ARGS.best,ARGS.bigram,ARGS.showrows)
