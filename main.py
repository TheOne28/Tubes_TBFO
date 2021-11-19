import sys
import re

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
    r'\<([^=])': r" < \1",
    r'\>([^=])': r" > \1",
    '\==': " == ",
    '\!=': " != ",
    r'(.)\,(.)': r"\1 , \2", 
    r'(.)\:(.)': r"\1 : \2", 
    r' \=([^=])': r" = \1", 
}
def preprocess(nama_file):
    #membuka file
    lines = open(nama_file,'r')
    #preprocess
    #Status multiline comment:  False berarti yg terakhir dibaca end comment/belum baca sama sekali, True berarti yang terakhir baca start comment
    start_multiline_comment = False
    lines_list = []
    for line in lines:
        #Kalau si line berada dalam multiline, maka dihapus saja
        if(start_multiline_comment):
            line = ''
        #Jika ketemu start multiline
        if(re.search(r"\"\"\"",line)):
            if start_multiline_comment: #ketemu end komentar
                start_multiline_comment = False
            else: #Ketemu start dari komentar
                start_multiline_comment = True
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
            if(line!=''): #jika jadi string kosong maka tidak perlu diappend
                line_array = line.split()
                #line_array = line
                lines_list.append(line_array)
    return lines_list


#meminta nama file
nama_file = sys.argv[1]
hasil_tokenisasi = preprocess(nama_file)
print(hasil_tokenisasi)