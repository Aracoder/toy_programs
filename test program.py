import os
f = open(os.path.expanduser('~/PycharmProjects/data_files/1001genomes_snp_short_indel_only_ACGTN_1Mb_100acc.vcf'))

print(f.readline())