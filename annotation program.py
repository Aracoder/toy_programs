__author__ = 'weigel'

# this program reads in .gff file
# it generates the geneModels list of objects
# in the list, frist gene models on plus, then minus strand
# in this way, no overlap, allows range analysis of each variant

# exactly one gene model for each gene, as per .txt file that contains the representative gene models for each gene
# other info: range of gene models, type of gene, strand

# import regular expressions
import re
# import pickle
import pickle

class GeneModel:
    def __init__(self, genemodel = '', chromosome = 0, location = range(0,0), strand = '', repgenemodel ='', genetype = '', fiveprimeutr = [], cds = [], threeprimeutr = []):
        self.g = genemodel
        self.c = chromosome
        self.l = location
        self.s = strand
        self.gt = genetype
        self.r = repgenemodel
        self.f = fiveprimeutr
        self.cds = cds
        self.t =  threeprimeutr

    def idRepGeneModel(self, elementsCL):
        if ['mRNA', 'snoRNA', 'ncRNA', 'tRNA','pseudogenic_transcript', 'miRNA'].count(elementsCL[2]) == 1:
            gene = re.search('ID=(.+?);', elementsCL[8])
            if gene and gene.group(1) in repGeneModels and self.g == gene.group(1)[:-2]:
                self.r = gene.group(1)
                print(self.g, self.r)
            else:
                None
        return(geneModels)

    def print(self):
        print(self.g, self.c, self.l, self.s, self.gt, self.r, self.f, self.cds, self.t)

def readGeneModels(geneModelCounter, elementsCL, strandGeneModelCounter):
    if ['gene','pseudogene'].count(elementsCL[2]) == 1 or re.search('transposable_element', elementsCL[2]):
        geneModelCounter += 1
        # the following prevents that absence of 'ID=' prefix returns some nonsense
        gene = re.search('ID=(.+?);', elementsCL[8])
        if gene:
            strandGeneModelCounter += 1
            geneModels.append(GeneModel())
            geneModels[geneModelCounter-1].g = gene.group(1)
            geneModels[geneModelCounter-1].c = elementsCL[0].replace('Chr','')
            geneModels[geneModelCounter-1].l = [int(elementsCL[3]), int(elementsCL[4])]
            geneModels[geneModelCounter-1].s = elementsCL[6]
        elif re.search('transposable_element', elementsCL[2]):
            geneModels[geneModelCounter-1].gt = 'TE'
    return([geneModels, geneModelCounter, strandGeneModelCounter])







#######################################################################################

# Read .gff file
filePath_gff = 'TAIR10_GFF3_genes_transposons_1M.gff'
gff = open(filePath_gff)
# count lines in gff file
with gff as f:
    for linesInGffFile, l in enumerate(f):
        pass

# import representative gene models as list
repGeneModelsFile = open('TAIR10_representative_gene_models_no_header.txt')
# count lines in repGeneModelsFile
with repGeneModelsFile as f:
    for linesInRGMFile, l in enumerate(f):
        pass
# read in lines in repGeneModelsFile, convert to list
repGeneModelsFile = open('TAIR10_representative_gene_models_no_header.txt')
repGeneModels = []
# read lines of RGMfile, strip new line character
for line in range(linesInRGMFile):
        currentLine = repGeneModelsFile.readline().rstrip('\n')
        repGeneModels.append(currentLine)
print(repGeneModels)

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
geneModelCounter = 0
plusGeneModelCounter = 0
minusGeneModelCounter = 0

# read gene models on plus strand into object list
for line in range(linesInGffFile - lastHeaderLine):
    # convert current line into list of elements of current line
    elementsCL = gff.readline().split()
    # create first all genes/TEs on plus strand
    if elementsCL[6] == '+':
        geneModels, geneModelCounter, plusGeneModelCounter = readGeneModels(geneModelCounter, elementsCL, plusGeneModelCounter)
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
        geneModels, geneModelCounter, minusGeneModelCounter = readGeneModels(geneModelCounter, elementsCL, minusGeneModelCounter)
# find representative gene models
gff.seek(0)
for line in range(linesInGffFile - lastHeaderLine):
    # convert current line into list of elements of current line
    elementsCL = gff.readline().split()
    for i in range(geneModelCounter):
        geneModels[i].idRepGeneModel(elementsCL)

# associate each gene model with representative gene model
# sanity check that range of representative gene model same as parent gene model



# dump geneModels to output file
file = open('TAIR10_gene_models.pkl','wb')
pickle._dump(geneModels,file)
file.close()


# test reading back in variantList

file = open('TAIR10_gene_models.pkl','rb')
reconstituted = pickle.load(file)
for i in range(geneModelCounter):
    reconstituted[i].print()











