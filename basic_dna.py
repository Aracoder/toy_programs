__author__ = 'weigel'

dna1 = 'agctggt'
dna2 = 'aggggggtc'

dna3 = dna1 + dna2
print(dna3)

print('length =', len(dna3))

print ('count =', dna3.count('a'))

print (dna3.__getitem__(0))