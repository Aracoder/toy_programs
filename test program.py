class Variant:
    def __init__(self, chromosome=0, position=0, variant='', variantType='', variantFrequency=0, alleleDistribution=[], missingData=0, missingDistribution=[], annotation='', methylation=''):
        self.c = chromosome
        self.p = position
        self.v = variant

    def print(self):
        print(self.c, self.p, self.v)

test = []

for i in range(10):
    test.append(Variant())
    test[i].c = i
    test[i].p = i*100
    test[i].v = 'a'
    test[i].print()

import pickle

print('\n')

file = open('python_output.txt','wb')

pickle._dump(test,file)

file.close()

file = open('python_output.txt','rb')

reconstituted = pickle.load(file)

for i in range(10):
    reconstituted[i].print()



