__author__ = 'weigel'

# this program reads in a .gff file
# it generates the geneModels list of objects
# in the list, first gene models on plus, then minus strand
# in this way, no overlap, allows range analysis of each variant

# exactly one gene model for each gene, as per .txt file that contains the representative gene models for each gene
# other info: range of gene models, type of gene, strand

import os
# import regular expressions
import re
# import pickle
import pickle

# this function reads main genes from .gff files
def readGeneModels(geneModelCounter, elementsCL, strandGeneModelCounter):
    if ['gene','pseudogene'].count(elementsCL[2]) == 1 or re.search('transposable_element', elementsCL[2]):
        geneModelCounter += 1
        # the following prevents that absence of 'ID=' prefix returns some nonsense
        gene = re.search('ID=(.+?);', elementsCL[8])
        if gene:
            strandGeneModelCounter += 1
            geneModels.append(GeneModel())
            geneModels[geneModelCounter-1].g = gene.group(1)
            geneModelIndex.append(geneModels[geneModelCounter-1].g)
            geneModels[geneModelCounter-1].c = elementsCL[0].replace('Chr','')
            geneModels[geneModelCounter-1].s = elementsCL[6]
        elif re.search('transposable_element', elementsCL[2]):
            geneModels[geneModelCounter-1].gt = 'TE'
        geneModels[geneModelCounter-1].print
    return(geneModels, geneModelIndex, geneModelCounter, strandGeneModelCounter)

# this class defines the object and its methods for the gene models
class GeneModel:
    def __init__(self, genemodel = '', repgenemodel ='', chromosome = 0, location = range(0,0),
                 strand = '', genetype = '', fiveprimeutr = range(0,0), cds = range(0,0), exon = [], intron = [],
                 threeprimeutr = range(0,0)):
        self.g = genemodel
        self.r = repgenemodel
        self.c = chromosome
        self.l = location
        self.s = strand
        self.gt = genetype
        self.f = fiveprimeutr
        self.cds = cds
        self.exon = exon
        self.intron = intron
        self.t =  threeprimeutr

    # this function determines whether a gene model is in the representative gene models list; if yes, it adds this info to gene model object
    def idRepGeneModel(self, elementsCL):
        found = False
        if ['mRNA', 'snoRNA', 'ncRNA', 'tRNA','pseudogenic_transcript','miRNA'].count(elementsCL[2]) == 1:
            gene = re.search('ID=(.+?);', elementsCL[8])
            if gene and gene.group(1) in repGeneModels and self.g == gene.group(1)[:-2]:
                self.r = gene.group(1)
                self.l = range(int(elementsCL[3]), int(elementsCL[4]))
                self.gt = elementsCL[2]
                found = True
            else:
                None
        return(geneModels,found)

    # this function associates UTRs, exons, introns with gene model objects
    def geneModelParts(self, elementsCL):
        if 'five_prime_UTR' == elementsCL[2]:
            self.f = range(int(elementsCL[3]), int(elementsCL[4]))
        elif 'cds' == elementsCL[2]:
            self.cds = range(int(elementsCL[3]), int(elementsCL[4]))
        elif 'three_prime_UTR' == elementsCL[2]:
            self.t = range(int(elementsCL[3]), int(elementsCL[4]))
        elif 'exon' == elementsCL[2]:
            self.exon.append(range(int(elementsCL[3]), int(elementsCL[4])))
        elif 'pseudogenic_exon' == elementsCL[2]:
            self.exon.append(range(int(elementsCL[3]), int(elementsCL[4])))
        elif 'transposon_fragment' == elementsCL[2]:
            self.exon.append(range(int(elementsCL[3]), int(elementsCL[4])))
        else:
            None
        return(self)




    def print(self):
        print(self.g, self.r, self.c, self.l, self.s, self.gt, self.f, self.cds, self.exon, self.intron, self.t)



#######################################################################################

# Read .gff file
filePath_gff = os.path.expanduser('~/PycharmProjects/data_files/TAIR10_GFF3_genes_transposons_1M.gff')
gff = open(filePath_gff)
# count lines in gff file
with gff as f:
    for linesInGffFile, l in enumerate(f):
        pass

# import representative gene models as list
repGeneModelsFile = open(os.path.expanduser('~/PycharmProjects/data_files/TAIR10_representative_gene_models_no_header_1M.txt'))
# count lines in repGeneModelsFile
with repGeneModelsFile as f:
    for linesInRGMFile, l in enumerate(f):
        pass
# read in lines in repGeneModelsFile, convert to list
repGeneModelsFile = open(os.path.expanduser('~/PycharmProjects/data_files/TAIR10_representative_gene_models_no_header_1M.txt'))
repGeneModels = []
# read lines of RGMfile, strip new line character
for line in range(linesInRGMFile+1):
        currentLine = repGeneModelsFile.readline().rstrip('\n')
        repGeneModels.append(currentLine)

# start reading data lines
gff = open(filePath_gff)
lineCounter = 0
# find first data line
for line in range(linesInGffFile):
    currentLine = gff.readline()
    elementsCL = currentLine.split()
    if not elementsCL[0].startswith('#'):
        lastHeaderLine = line
        break
# set read pointer back to beginning of file
gff.seek(0)
# go back to first line before first data line
for line in range(lastHeaderLine):
    gff.readline()

# geneModels is the list of gene model objects
geneModels = []
geneModelIndex = []
geneModelCounter = 0
plusGeneModelCounter = 0
minusGeneModelCounter = 0

# read gene models on plus strand into object list
for line in range(linesInGffFile - lastHeaderLine):
    # convert current line into list of elements of current line
    elementsCL = gff.readline().split()
    # create first all genes/TEs on plus strand
    if elementsCL[6] == '+':
        geneModels, geneModelIndex, geneModelCounter, plusGeneModelCounter = readGeneModels(geneModelCounter, elementsCL, plusGeneModelCounter)
# next, genes/TEs on minus strand
gff.seek(0)
# go back to first line before first data line
for line in range(lastHeaderLine):
    gff.readline()
# read gene models on minus strand into object list
for line in range(linesInGffFile - lastHeaderLine):
    # convert current line into list of elements of current line
    elementsCL = gff.readline().split()
    if elementsCL[6] == '-':
        geneModels, geneModelIndex, geneModelCounter, minusGeneModelCounter = readGeneModels(geneModelCounter, elementsCL, minusGeneModelCounter)
print('Done with generating gene models; total number is ' + str(len(geneModels)) + '.\n' + 'Number of reprensentative gene models is ' + str(len(repGeneModels))+'.\n')


# associate each object in gene model list with its representative gene model
gff.seek(0)
for line in range(linesInGffFile - lastHeaderLine):
    # convert current line into list of elements of current line
    elementsCL = gff.readline().split()
    for i in range(geneModelCounter):
        geneModels, found = geneModels[i].idRepGeneModel(elementsCL)
        if found:
            break
print('Done with finding representative gene models.\n')

# asssociate each gene model with its parts (UTRs, exons, introns)
gff.seek(0)
print('Now printing gene models after adding info on parts.\n')
for line in range(linesInGffFile - lastHeaderLine):
    # convert current line into list of elements of current line
    elementsCL = gff.readline().split()
    id = re.search('ID=(.+?);', elementsCL[8]).group(1)
    parent = re.search('Parent=(.+?);', elementsCL[8]).group(1)
    print('line 177', id, parent)
    if parent in geneModelIndex or id in geneModelIndex:
        i = geneModelIndex.index(re.search('ID=(.+?);', elementsCL[8]).group(1))
        geneModels[i].geneModelParts(elementsCL)
        print('line 182')
        geneModels[i].print()








# dump geneModels to output file
file = open(os.path.expanduser('~/PycharmProjects/data_files/TAIR10_gene_models.pkl'),'wb')
pickle._dump(geneModels,file)
file.close()


# test reading back in variantList

file = open(os.path.expanduser('~/PycharmProjects/data_files/TAIR10_gene_models.pkl'),'rb')
reconstituted = pickle.load(file)
print('Now printing reconstituted gene models read from file.')
for i in range(geneModelCounter):
    reconstituted[i].print()











