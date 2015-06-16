__author__ = 'weigel'

# Read .gff file
filePath_gff = 'Athaliana_167_TAIR10.gene_exons_1M.gff3'
gff = open(filePath_gff)
filePathRepGeneModels = 'TAIR10_representative_gene_models.txt'
repGeneModels = open(filePathRepGeneModels)


# count lines in files
with gff as f:
    for linesInGffFile, l in enumerate(f):
        pass
with repGeneModels as f:
    for linesInRGMFile, l in enumerate(f):
        pass

print(linesInGffFile)

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
# start analyzing lines
for line in range(linesInGffFile - lastHeaderLine):
    # convert current_line into list elements_cl
    currentLine = gff.readline()
    elementsCL = currentLine.split()
    print(elementsCL)
    if elementsCL[2] == 'gene' and elementsCL[5] == '+':
        print(elementsCL[2:4],'gene on plus strand')








