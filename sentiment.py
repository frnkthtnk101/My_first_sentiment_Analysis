import math, os, pickle, re,argparse,time

def remove_training_files():
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
    results = {"negative":0, "neutral":0, "positive":0}
    print("\nFile Classifications:")
    t = time.time()
    for filename in iFileList:
        fileText = bc.loadFile(test_files + filename)
        if bigram:
            result = bc.classify_bi(fileText)
        else:
            result = bc.classify(fileText)
        if rows:
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
    group = PARSER.add_argument_group()
    group.add_argument('-b','--best',action='store_true',help='use the best')
    group.add_argument('-bi','--bigram',action='store_true',help='use the bigram')
    group.add_argument('-t','--train',action='store_true',help='use to train the program')
    group.add_argument('-s','--showrows',action='store_true',help='show results')

    ARGS = PARSER.parse_args()
    main(ARGS.testfiles,ARGS.best)
    if ARGS.train:
        remove_training_files()
    if ARGS.bigram is True and ARGS.best is False:
        raise ValueError('you cannot call bigragm option with the best option')
    else:
        main(ARGS.test_files,ARGS.best,ARGS.bigram,ARGS.showrows)
