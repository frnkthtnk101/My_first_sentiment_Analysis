py = python3.4

train:
	-rm bad.txt good.txt bi_good.txt bi_bad.txt averagebad.txt averagegood.txt GoodWords.csv BadWords.csv keys.csv

test:
	$(py) test.py