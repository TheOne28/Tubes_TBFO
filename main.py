#File ini adalah main program yang digunakan
#Pada file ini, dilakukan preprocessing kode program dan tokenisasi, kemudian dilakukan pemanggilan fungsi-fungsi dari file lain

import sys
from cnfgenerator import CNFfromFile
from cyk_parser import cyk_parser

#Tuple berisi keyword di  python
python_symbols = ('False','class','is','return','None','continue','for','True','def','from','while', 'and','not','with','as','elif','if','or','assert','else','import','pass','break','except','in','raise')
compare_operator = ('<=', '>=', '==', '!=') #Tuple berisi Compare operator
assignment_operator = ('+=','-=','**=','*=','//=','/=','@=','%=', '&=', '|=', '^=', '~=', '>>=', '<<=') #Tuple berisi Assignment Operator
brackets = ('[',']','(',')','{','}')  #Tuple berisi bracket  
substitute = ("__str__", "__assign__", "__comp__", "__doubleop__") #Tuple berisi Substitute value, digunakan untuk membantu grammar
double_operator = ('>>' , '<<', '//', '**',) #Tuple berisi operator-operator yang berupa simbol ganda
bitwise_operator = ('&', '|', '~', '^') #Tuple berisi bitwise operator
other_symbol = (',', '=', ':', '<', '>', '.') #Tuple berisi symmbol-symbol lain 
ar_operator = ('+', '-', '*', '/', '%', '@') #Tuple berisi aritmatika operator

def preprocess(nama_file):
    #membuka file
    lines = open(nama_file,'r')

    #preprocess

    lines_list = []
    lines = str(lines.read())

    #Proses menghilangkan multiline comment, multiline comment akan diganti dengan __str__
    #Apabila terjadi error, preproses akan berhenti, dan tidak akan dilanjutkan ke parser
    while(True):
        idxFirstOne = lines.find("'''")
        idxFirstTwo = lines.find('"""')
        idxSecond = -1
        if(idxFirstOne == -1 and idxFirstTwo == -1):
            break
        elif(idxFirstOne == -1):
            idxSecond = lines.find('"""', idxFirstTwo + 3)
        elif(idxFirstTwo == -1): 
            idxSecond = lines.find("'''", idxFirstOne + 3)
        else:
            if(idxFirstOne > idxFirstTwo):
                idxSecond = lines.find('"""', idxFirstTwo + 3)
            else:
                idxSecond = lines.find("'''", idxFirstOne + 3)

        if ((idxFirstOne != -1) and (idxFirstTwo != -1)):
            if (idxFirstOne < idxFirstTwo):
                lines = lines.replace(lines[idxFirstOne:idxSecond + 3], "__str__")
            else:
                lines = lines.replace(lines[idxFirstTwo:idxSecond + 3], "__str__")
        elif((idxFirstOne == -1) and (idxSecond != -1)):
            lines = lines.replace(lines[idxFirstTwo:idxSecond + 3], "__str__")
        elif((idxFirstTwo == -1) and (idxSecond != -1)):
            lines = lines.replace(lines[idxFirstOne:idxSecond + 3], "__str__")
        else:
            return [], -2

    count = 0
    lines = lines.split('\n')

    #Pemrosesan tiap baris listnya 
    for line in lines:
        #mengganti new line dengan string kosong
        
        line  = line.replace('\n', '')

        #Mengganti isi string valid dengan __str__
        #Apabila terjadi error, preproses akan berhenti, dan tidak akan dilanjutkan ke parser
        while(True):
            idxFirstOne = line.find("'")
            idxFirstTwo = line.find('"')
            idxSecond = -1
            if(idxFirstOne == -1 and idxFirstTwo == -1):
                break
            elif(idxFirstOne == -1):
                idxSecond = line.find('"', idxFirstTwo + 1)
            elif(idxFirstTwo == -1):
                idxSecond = line.find("'", idxFirstOne + 1)
            else:
                if(idxFirstOne < idxFirstTwo):
                    idxSecond = line.find("'", idxFirstOne + 1)
                else:
                    idxSecond = line.find('"', idxFirstTwo + 1)
    
            if ((idxFirstOne != -1) and (idxFirstTwo != -1)):
                if (idxFirstOne < idxFirstTwo):
                    line = line.replace(line[idxFirstOne:idxSecond + 1], "__str__")
                else:
                    line = line.replace(line[idxFirstTwo:idxSecond + 1], "__str__")                    
            elif((idxFirstOne == -1) and (idxSecond != -1)):
                line = line.replace(line[idxFirstTwo:idxSecond + 1], "__str__")
            elif((idxFirstTwo == -1) and (idxSecond != -1)):
                line = line.replace(line[idxFirstOne:idxSecond + 1], "__str__")
            else:
                return [], -3

        #Menghilangkan komen per baris (ditandai dengan #)
        if(line.find('#') != -1):
            line = line.replace(line[line.find('#'):], '')

        #Penggantian simbol-simbol dengan pengganti yang sesuai, atau menambahkan whitespace di antara symbol
        for symbol in assignment_operator:
            line = line.replace(symbol, " __assign__ ")
        
        for symbol in compare_operator:
            line = line.replace(symbol, " __comp__ ")

        for symbol in double_operator:
            line = line.replace(symbol, " __doubleop__ ")

        for symbol in brackets:
            line = line.replace(symbol, ' {} '.format(symbol))

        for symbol in bitwise_operator:
            line = line.replace(symbol, ' {} '.format(symbol))

        for symbol in ar_operator:
            line = line.replace(symbol, ' {} '.format(symbol))

        for symbol in other_symbol:
            line = line.replace(symbol, ' {} '.format(symbol))


        if(line!=''): 
            #Pengubahan word yang tidak termasuk keeyword menjadi __var__
            #Apabila terjadi error, preproses akan berhenti, dan tidak akan dilanjutkan ke parser
            line_array = line.split()
            filtered_list = []
            for i in range(len(line_array)):
                if line_array[i] in python_symbols or line_array[i] in assignment_operator or line_array[i] in substitute:
                    filtered_list.append(line_array[i])
                elif isVarValid(line_array[i]):
                    line_array[i] = '__var__'
                    filtered_list.append(line_array[i])  
                else:
                    try:
                        line_array[i] = float(line_array[i])
                        line_array[i] = '__num__'
                        filtered_list.append(line_array[i])
                    except ValueError:
                        return [], count          
                            
                for operator in assignment_operator:
                    if operator in filtered_list: 
                        idx_assignment = filtered_list.index(operator)-1
                        while(idx_assignment>=0):
                            if filtered_list[idx_assignment] =='__num__':
                                filtered_list.pop(idx_assignment)
                            idx_assignment -= 1
            line_array = filtered_list
            lines_list += line_array + ['\n']
        count += 1
    return lines_list, -1

def isVarValid(variabel):
    #FA untuk mengecek apakah variabel valid
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

def validateBreakConReturn(hasil_tokenisasi):
    #Pengecekan apakah ada break continue atau return yang tidak valid (diluar blok loop atau fungsi)
    flag = True
    isLoopHasExist = False
    isFuncHasExist = False
    count = 0
    
    for i in range(len(hasil_tokenisasi)):
        if (hasil_tokenisasi[i] == 'for' or hasil_tokenisasi[i] == 'while'):
            isLoopHasExist = True
        elif (hasil_tokenisasi[i] == 'def'):
            isFuncHasExist = True
        elif (hasil_tokenisasi[i] == 'return' and not isFuncHasExist):
            flag = False
            break
        elif ((hasil_tokenisasi[i] == 'break' or hasil_tokenisasi[i] == 'continue') and not isLoopHasExist):
            flag = False
            break
    
    if (not flag):
        for j in range(i):
            if (hasil_tokenisasi[j] == '\n'):
                count += 1

    return flag, count

def displaySrc(filename):
    #Mencetak source code untuk memperindah tampilan 
    print("\n\t\t\t\tSOURCE CODE")
    print("===================================================================")
    with open(filename, "r") as f:
        counter = 1
        for line in f:
            print(f"{counter}\t|", line,end="")
            counter += 1
            
    print("\n===================================================================")
    print("\t\t\t\tEND CODE")

def main():
    #Main program

    #Variabel untuk mencetak berwarna merah
    RED = "\033[1;37;41m"
    ENDC = '\033[0m'
    #meminta nama file
    nama_file = sys.argv[1]
    
    displaySrc(nama_file)
    
    print("\nCHECKING SYNTAX...")
    print("\nRESULT: \n")
    
    hasil_tokenisasi, flag = preprocess(nama_file)
    CNF = CNFfromFile("grammar.txt")
    
    flagToken, count = validateBreakConReturn(hasil_tokenisasi)
    if (flagToken and flag == -1):
        if (cyk_parser(CNF, hasil_tokenisasi)):
            print("Accepted")
        else:
            print("Syntax Error")
    else:
        if(flag == -2):
            print("Syntax error in multiline declaration")
        elif(flag == -3):
            print("Syntax error in string declaration")
        elif(flag != -1): 
            count = flag
            line = ""
            with (open(nama_file, "r")) as f:
                i = 0
                while (i<= count):
                    line = f.readline()
                    if(count == flag):
                        i += 1
                    else:
                        if(line != '\n'):
                            i += 1
                if (flag == -1): line = line[:len(line)-1]
            
                print(RED + line + ENDC)
                print(f"^Syntax Error on line {count+1}\n")
        else:
            line = ""
            with (open(nama_file, "r")) as f:
                i = 0
                while (i<= count):
                    line = f.readline()
                    if(line != '\n'):
                        i += 1
                if (flag == -1): line = line[:len(line)]
            
                print(RED + line + ENDC)
                print(f"^Syntax Error on line {count+1}\n")
if __name__ == '__main__':
    main()