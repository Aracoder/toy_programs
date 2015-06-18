import re

repGeneModels = ['AT1G01020.1','AT1G02210.2']

test = 'AT1G01020'

gene = re.search('ID=(.+?);', 'ID=AT1G01020.1;Parent=AT1G01020;Name=AT1G01020.1;Index=1;Note=Arv1-like protein;conf_class=2;symbol=ARV1;computational_description=ARV1%3B CONTAINS InterPro DOMAIN/s: Arv1-like protein (InterPro:IPR007290)%3B BEST Arabidopsis thaliana protein match is: Arv1-like protein (TAIR:AT4G01510.1)%3B Has 311 Blast hits to 311 proteins in 154 species: Archae - 0%3B Bacteria - 0%3B Metazoa - 110%3B Fungi - 115%3B Plants - 42%3B Viruses - 0%3B Other Eukaryotes - 44 (source: NCBI BLink).;conf_rating=****;Dbxref=gene:2200939')

print(gene)
print(gene.group(1))

if gene and gene.group(1) in repGeneModels and test == gene.group(1)[:-2]:
    print(test)
    print('success')