import sys
from cnfgenerator import CNFfromFile
from cyk_parser import cyk_parser

#list berisii symbol di  python
python_symbols = ('False','class','finally','is','return','None','continue','for','lambda','try','True','def','from','nonlocal','while',
                    'and','del','global','not','with','as','elif','if','or','yield','assert','else','import','pass','break','except','in','raise','(',')','[',']','{','}','.',',','<=','>=','<<','>>','&','|','^','~','<','>','==','!=',':','@','+','-','*','/', '%','//','**',"__str__", "="
)
compare_operator = ('<=', '>=', '==', '!=')
assignment_operator = ('+=','-=','**=','*=','//=','/=','@=','%=', '&=', '|=', '^=', '~=', '>>=', '<<=')
brackets = ('[',']','(',')','{','}')    
substitute = ("__str__", "__assign__", "__comp__", "__doubleop__")
double_operator = ('>>' , '<<', '//', '**',)
bitwise_operator = ('&', '|', '~', '^')
other_symbol = (',', '=', ':', '<', '>', '.')
ar_operator = ('+', '-', '*', '/', '%', '@')

def preprocess(nama_file):
    #membuka file
    lines = open(nama_file,'r')

    #preprocess
    #Status multiline comment:  False berarti yg terakhir dibaca end comment/belum baca sama sekali, True berarti yang terakhir baca start comment
    lines_list = []
    lines = str(lines.read())

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
            return [], False

    count = 0
    lines = lines.split('\n')
    for line in lines:
        #mengganti new line dengan string kosong( Ngaruh ke isi string juga, tapi karena entar isi string dikosongin, mestinya gak ngaruh ke validasi program)
        line  = line.replace('\n', '')
        #menghilangkan komentar 1 baris
        
        #menghilangkan isi semua string valid
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
                return [], False
        #mengganti setiap simbol menjadi "spasi simbol spasi"
        if(line.find('#') != -1):
            line = line.replace(line[line.find('#'):], '')

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


        if(line!=''): # jika jadi string kosong maka tidak perlu diappend
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
                    if operator in filtered_list: # Memeriksa jika ada assignment
                        idx_assignment = filtered_list.index(operator)-1
                        while(idx_assignment>=0):
                            if filtered_list[idx_assignment]=='__num__':
                                filtered_list.pop(idx_assignment)
                            idx_assignment -= 1
            line_array = filtered_list
            lines_list += line_array + ['\n']
        count += 1
    return lines_list, -1

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

def validateBreakConReturn(hasil_tokenisasi):
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
    RED = "\033[1;37;41m"
    ENDC = '\033[0m'
    #meminta nama file
    nama_file = sys.argv[1]
    
    displaySrc(nama_file)
    
    print("\nCHECKING SYNTAX...")
    print("\nRESULT: \n")
    
    hasil_tokenisasi, flag = preprocess(nama_file)
    CNF = CNFfromFile("grammar2.txt")
    
    flagToken, count = validateBreakConReturn(hasil_tokenisasi)
    if (flagToken and flag == -1):
        if (cyk_parser(CNF, hasil_tokenisasi)):
            print("Accepted")
        else:
            print("Syntax Error")
    else:
        if (flag != -1): count = flag
        with (open(nama_file, "r")) as f:
            i = 0
            while (i<=count):
                line = f.readline()
                if (line != "\n"):
                    i += 1
            if (flag == -1): line = line[:len(line)-1]
            
            print(RED + line + ENDC)
            print(f"^Syntax Error on line {count+1}\n")

if __name__ == '__main__':
    main()