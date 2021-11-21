import copy
import string

def readCFGRule(grammarFile):
  # Mengembalikan aturan CFG yang dibaca dari file

  # KAMUS
  # CFG : dictionary
  # lines : list of list of string
  # listString: list of string
  # elmt: string
  # splitted: list of string
  # line: list of string
  # key: string
  # rawVals: list of list of string
  # value: list of list of string
  # rawVal: list of string

  # ALGORITMA
  CFG = {}
  with open(grammarFile, 'r') as f:
    lines = []
    listString = f.read().split('\n') # membagi string file menjadi baris sesuai newline
    for elmt in listString: # mengiterasi setiap line dari file
      splitted = elmt.split(' -> ') # memisahkan setiap line pada tanda panah
      if (len(splitted) == 2): # jika sesuai format, yaitu terdapat string di kiri dan kanan tanda panah
        lines.append(splitted) # tambahkan rule ke lines 
    for line in lines: # iterasi setiap baris rules
      key = line[0].replace(" ", "") # simpan elemen pertama sebagai key
      rawVals = [production.split() for production in line[1].split('|')] # jadikan hasil produksi menjadi list of list of string
      value = []
      for rawVal in rawVals: # iterasi setiap hasil produksi
        value.append( # tambahkan hasil produksi ke value
          [" " if unit == "__space__"  
           else "|" if unit == "__or_sym__" 
           else "\n" if unit == "__new_line__" 
           else unit # jika bukan aturan khusus
           for unit in rawVal 
           ]
          )
      CFG.update({key: value}) # tambahkan pasangan key dan value ke CFG
  return CFG

def isNonTerminal(symbol):
  # mengembalikan true jika simbol bukan terminal simbol
  
  # KAMUS
  # char: character
  
  # ALGORITMA
  if len(symbol) == 1: 
    return False # jika cuma 1 huruf
  for char in symbol:
    if char not in (string.ascii_uppercase + string.digits + "_"):
      return False  # jika terdapat char non huruf besar atau angka atau _
  return True

def simplify(CFG):
  # Mengembalikan aturan CFG yang telah disederhanakan
  
  # KAMUS
  # key: string
  # products: list of list of string
  # loop: boolean
  # product: list of string
  # newProducts: list of string

  # ALGORITMA  
  for key in CFG: # ambil setiap key pada CFG
    products = CFG[key] # ambil hasil produksi untuk simbol key
    loop = True
    while loop: # looping sampai kondisi yang ditentukan
      loop = False
      for product in products:
        if len(product) == 1 and isNonTerminal(product[0]): 
          # jika terdapat aturan A -> B dan B -> _, maka ganti dengan A -> _
          products.remove(product)
          newProduct = copy.deepcopy([
            product for product in CFG[product[0]]
            if product not in products
          ])
          products.extend(newProduct)
          loop = True
          break
  return CFG
          
def convertToCNF(CFG):
  # Mengembalikan CNF hasil convert dari CFG
  
  # KAMUS
  # CNF: dictionary
  # key: string
  # terminals: set of string
  # product: list of list of string
  # nonSingleProducts: list of list of string
  # nonSingleProduct : list of string
  # symbol: string
  # listTerminal: list of string
  # i: integer
  # terminal: string
  # j: integer
  # product: list of string
  
  addedRule = {}
  for key in CFG: # iterasi setiap key pada CFG
    terminals = [] # inisialisasi set
    products = CFG[key]
    
    # memfilter products yang panjangnya lebih dari 1
    nonSingleProducts = [product for product in products if len(product) > 1]
    for nonSingleProduct in nonSingleProducts: # iterasi setiap produksi yang panjangnya lebih dari 1
      for symbol in nonSingleProduct: # ambil setiap simbol pada product
        if (not isNonTerminal(symbol) and symbol not in terminals): # jika simbol bukan non terminal dan belum ada di set
          terminals.append(symbol)
    
    for i, terminal in enumerate(terminals):
      # tambahkan aturan baru untuk setiap terminal
      addedRule.update({f"{key}_TERMINAL_{i+1}": [[terminal]]})
      for j, product in enumerate(products):
        if len(product) > 1:
          for k in range(len(product)):
            if (len(products[j][k]) == len(terminal)):
              # ganti terminal simbol dengan nonterminal simbol
              products[j][k] = products[j][k].replace(terminal, f"{key}_TERMINAL_{i+1}") 
    
    idx = 1
    for i in range(len(products)):
      while (len(products[i]) > 2): # selama panjang products lebih dari 2
        # ubah aturan sehingga hanya ada 2 aturan
        addedRule.update({f"{key}_NONTERMINAL_{idx}": [[products[i][0], products[i][1]]]})
        products[i] = products[i][1:]
        products[i][0] = f"{key}_NONTERMINAL_{idx}"
        idx += 1

  # tambahkan ke CFG
  CFG.update(addedRule)
  return CFG

def CNFfromFile(filePath):
  # Mengembalikan aturan CNF berdasarkan input lokasi file
  
  # ALGORITMA
  return convertToCNF(simplify(readCFGRule(filePath)))