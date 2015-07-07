import re


gff = "Parent=AT1G01040.1,AT1G01040.2;ID=AT1G01040:exon:8;Name=DCL1:exon:8Parent=AT1G01040.1,AT1G01040.2;ID=AT1G01040:exon:8;Name=DCL1:exon:8"

id_semicolon = re.search('ID=(.+?);', gff)
id_colon = re.search('ID=(.+?):', gff)


parent = re.search('Parent=(.+?);', gff)

if id_colon and id_semicolon:
    if (id_colon.group(1)).__len__() < (id_semicolon.group(1)).__len__():
        id = id_colon.group(1)
    else:
        id = id_semicolon.group(1)

elif id_colon:
    id = id_colon.group(1)
elif id_semicolon:
    id = id_semicolon.group(1)

if parent:
    parent = parent.group(1)

print("id", id)
print("parent", parent)
