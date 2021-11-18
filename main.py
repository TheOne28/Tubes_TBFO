import sys
import re

#meminta nama file
nama_file = sys.argv[1]
#membuka file
lines = open(nama_file,'r')
#preprocess
lines_list = []
for line in lines:
    #mengganti new line dengan string kosong
    line  = re.sub('\n','',line)
    #menghilangkan komentar
    line = re.sub(" *#.*",'',line)
    if(line!=''): #jika jadi string kosong maka tidak perlu diappend
        lines_list.append(line)
print(lines_list)