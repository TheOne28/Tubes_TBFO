import sys
import re
from cnfgenerator import CNFfromFile

#dictionary buat konversi symbol
symbol_dict = {
    '\(': " ( ",
    '\)': " ) ",
    '\[': " [ ",
    '\]': " ] ",
    '\{': " { ",
    '\}': " } ",
    r'(\<=)': " <= ",
    r'\>=': " >= ",
    r'(\@=)': " @= ",
    r'(\+=)': " += ",
    r'(\-=)': " -= ",
    r'(\*\*=)': " **= ",
    r'(//=)': " //= ",
    r'([^\*])(\*=)': " *= ",
    r'([^\/])(\/=)': " /= ",
    r'(\%=)': " %= ",
    r'\<([^=])': r" < \1",
    r'\>([^=])': r" > \1",
    '\==': " == ",
    '\!=': " != ",
    r'(.)\,(.)': r"\1 , \2", 
    r'(.)\:': r"\1 : ", 
    r' \=([^=])': r" = \1", 
}
#list berisii symbol di  python
python_symbols = ('False','class','finally','is','return','None','continue','for','lambda','try','True','def','from','nonlocal','while',
                    'and','del','global','not','with','as','elif','if','or','yield','assert','else','import','pass','break','except','in',
                    'raise',
)
def preprocess(nama_file):
    #membuka file
    lines = open(nama_file,'r')
    #preprocess
    #Status multiline comment:  False berarti yg terakhir dibaca end comment/belum baca sama sekali, True berarti yang terakhir baca start comment
    start_multiline_comment = False
    lines_list = []
    for line in lines:
        #Jika ketemu start multiline
        if(re.search(r"\"\"\"",line)):
            if start_multiline_comment: #ketemu end komentar
                start_multiline_comment = False
            else: #Ketemu start dari komentar
                start_multiline_comment = True
            line = ''
                #Kalau si line berada dalam multiline, maka dihapus saja
        if(start_multiline_comment):
            line = ''
        else:#Bukan komentar multiline
            #mengganti new line dengan string kosong( Ngaruh ke isi string juga, tapi karena entar isi string dikosongin, mestinya gak ngaruh ke validasi program)
            line  = re.sub('\n','',line)
            #menghilangkan komentar 1 baris
            line = re.sub(" *#.*",'',line)
            #menghilangkan isi semua string valid
            line = re.sub('".*"',' " " ',line)
            #memproses char
            line = re.sub("'.'"," ' ' ",line)
            #line = re.sub(r"'[^0-9]*[^.][^0-9]*'",r" ' ' ",line)
            line = re.sub(r"'[^0-9\s]*[^.\s][^0-9\s]*'\s*"," ' ' ",line)
            #print(line)
        #mengganti setiap simbol menjadi "spasi simbol spasi"
        #"""
            for token,rep in symbol_dict.items():
                line = re.sub(token,rep,line)
            #handle dot operator
            line = re.sub(r"([a-zA-Z_])(\w+)*(\.)([a-zA-Z_])(\w+)*",r"\1\2 . \4\5",line)
            #Memeriksa variabel(jika ada),kalau valid masukkin ke token kalau gak gak dimasukin
            for baris in re.findall(r".* \= .*",line):
                #print(re.findall(r".* \= .*",line)
                #Memeriksa tiap elemen baris yang memenuhi
                #Menghilangkan = dan isi (), {},serta []
                baris = re.sub(r'=',"",baris)
                baris = baris.split()
                print(baris)
                for token in baris: #Periksa tiap token
                    if(token not in python_symbols and True):#Periksa yang gak ada di symbols
                        pass
            #        #cek validitas
            #        if(not re.search(r"[a-zA-Z_][a-zA-Z_0-9]*",token)):#token gak  valid
            #            line = re.sub(token,'',line)
            #        else:
            #            line = re.sub(token,'VAR',line)
            #menambahkan token di suatu line ke lines_list
            if(line!=''): #jika jadi string kosong maka tidak perlu diappend
                line_array = line.split()
                #line_array = line
                lines_list.append(line_array)
    return lines_list



def main():
    #meminta nama file
    nama_file = sys.argv[1]
    hasil_tokenisasi = preprocess(nama_file)
    print(hasil_tokenisasi)
    CNF = CNFfromFile("grammar.txt")
    with open("cnfResult.txt", "w") as f:
        f.write(str(CNF))

if __name__ == '__main__':
    main()