from os import remove
import sys
import re
from cnfgenerator import CNFfromFile
from cyk_parser import cyk_parser

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
    r'(\<<)': " << ",
    r'\>>': " >> ",
    r'(.*)&=': r"\1& =",
    r'(.*)& ([^=])': r"\1 & \2",#Kopi untuk aturan lain
    r'\|': " | ",
    r'\^': " ^ ",
    r'\~': " ~ ",
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
    r'\,': r" , ", 
    r'(.*)\:(.*)': r"\1 : \2", 
    r' \=([^=])': r" = \1", 
    r'\@{1}([^\=])': r" @ \1",
    r'\+{1}([^\=])': r" + \1",
    r'\-{1}([^\=])': r" - \1",
    r'[^\*]\*{1}([^\=\*])': r" * \1",
    r'[^\/]\/{1}([^\=\/])': r" / \1",
    r'\%([^\=])': r" % \1",
    r'//([^=])': r" // \1",
    r'\*\*([^=])': r" ** \1",
}
#list berisii symbol di  python
python_symbols = ('False','class','finally','is','return','None','continue','for','lambda','try','True','def','from','nonlocal','while',
                    'and','del','global','not','with','as','elif','if','or','yield','assert','else','import','pass','break','except','in',
                    'raise','(',')','[',']','{','}','.',',','<=','>=','<<','>>','&','|','^','~','<','>','==','!=',':','@','+','-','*','/',
                    '%','//','**',"__str__",
)
assignment_operator = ('=','+=','-=','*=','/=','@=','**=','//=','%=')
brackets = ('[',']','(',')','{','}')
def preprocess(nama_file):
    #membuka file
    lines = open(nama_file,'r')
    #preprocess
    #Status multiline comment:  False berarti yg terakhir dibaca end comment/belum baca sama sekali, True berarti yang terakhir baca start comment
    start_multiline_comment = False
    multiline_comment = ''
    lines_list = []
    for line in lines:
        #Jika ketemu start multiline
        if(re.search(r"\"\"\"",line)):
            if start_multiline_comment and multiline_comment=='"""': #ketemu end komentar
                start_multiline_comment = False
                multiline_comment = ''
            elif not start_multiline_comment: #Ketemu start dari komentar
                start_multiline_comment = True
                multiline_comment = '"""'
            line = ''
        if(re.search(r"\'\'\'",line)):
            if start_multiline_comment  and multiline_comment=="'''": #ketemu end komentar
                start_multiline_comment = False
                multiline_comment = ''
            elif not start_multiline_comment: #Ketemu start dari komentar
                start_multiline_comment = True
                multiline_comment = "'''"
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
            #print(line)
            line = re.sub(r'([([{ ,:])".*"',r'\1 __str__',line)
            #memproses char
            print(line)
            line = re.sub("'.'","__str__",line)
            line = re.sub(r"'[^0-9\s]*[^.\s][^0-9\s]*'\s*","__str__",line)
        #mengganti setiap simbol menjadi "spasi simbol spasi"
            for token,rep in symbol_dict.items():
                line = re.sub(token,rep,line)
            #handle dot operator
            line = re.sub(r"([a-zA-Z_])(\w+)*(\.)([a-zA-Z_])(\w+)*",r"\1\2 . \4\5",line)
            if(line!=''): #jika jadi string kosong maka tidak perlu diappend
                line_array = line.split()
                filtered_list = []
                for i in range(len(line_array)):
                    if line_array[i] not in python_symbols and isVarValid(line_array[i]):
                        line_array[i] = '__var__'
                        filtered_list.append(line_array[i])
                    elif line_array[i] in python_symbols or line_array[i] in assignment_operator:
                        filtered_list.append(line_array[i])
                    else:
                        try:
                            line_array[i] = float(line_array[i])
                            line_array[i] = '__num__'
                        except ValueError:
                            continue
                        else:
                            filtered_list.append(line_array[i])
                    for operator in assignment_operator:
                        if operator in filtered_list: #Memeriksa jika ada assignment
                            idx_assignment = filtered_list.index(operator)-1
                            while(idx_assignment>=0):
                                if filtered_list[idx_assignment]=='__num__':
                                    filtered_list.pop(idx_assignment)
                                idx_assignment -= 1
                line_array = filtered_list
                lines_list += line_array + ['\n']

    return lines_list

def isVarValid(variabel):
    num=  '0123456789'
    lowercase = 'abcdefghijklmnopqrstuvwxyz'
    uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    underscore = '_'
    valid_for_title = lowercase+uppercase+underscore
    valid_for_back = valid_for_title+num
    #current_state= ['start','accepted','rejected']
    current_state = 'start'
    #Cek huruf pertama
    for i in range(len(variabel)):
        if(i==0 and variabel[i] in valid_for_title and current_state!='rejected'):
            current_state = 'accepted'
        elif(i>0 and variabel[i] in valid_for_back and current_state!='rejected'):
            current_state = 'accepted'
        else:
            current_state = 'rejected'
    return current_state == 'accepted'
'''
def AssignedValue(variabel):
    num=  '0123456789'
    lowercase = 'abcdefghijklmnopqrstuvwxyz'
    uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    underscore = '_'
    dot = '.'
    valid_for_title = lowercase+uppercase+underscore
    valid_for_back = valid_for_title+num
    #current_state= ['start','accepted_num','dot_transition,accepted_var,rejected']
    current_state = 'start'
    #Cek huruf pertama
    for i in range(len(variabel)):
        if(i==0 and variabel[i] in num and current_state=='start'):
            current_state = 'accepted_num'
        elif(i==0 and variabel[i] in valid_for_title and current_state=='start'):
            current_state = 'accepted_var'
        elif(i>0 and variabel[i] in valid_for_back and current_state=='accepted_var'):
            current_state = 'accepted_var'
        elif(i>0 and variabel[i] in num and current_state=='accepted_num'):
            current_state = 'accepted_num'
        elif(i>0 and variabel[i] in dot and current_state=='accepted_num'):
            current_state = 'dot_transition'
        elif(i>0 and variabel[i] in num and current_state=='dot_transition'):
            current_state = 'accepted_num'
        else:
            current_state = 'rejected'
    if(current_state == 'accepted_var' or current_state == 'accepted_num'):
        return current_state
    else:
        return 'rejected'
'''
def main():
    #meminta nama file
    nama_file = sys.argv[1]
    hasil_tokenisasi = preprocess(nama_file)
    print(hasil_tokenisasi)
    CNF = CNFfromFile("grammar2.txt")
    with open("cnfResult.txt", "w") as f:
        for rule in CNF:
            f.write(str(rule)+" -> "+ str(CNF[rule]) + "\n")
            
        # f.write(str(CNF))
    
    # print(CNF)
    if (cyk_parser(CNF, hasil_tokenisasi)):
        print("CNF valid")
    else:
        print("CNF invalid")

if __name__ == '__main__':
    main()