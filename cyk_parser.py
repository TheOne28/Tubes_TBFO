from os import pardir


def cyk_parser(grammar, prob):
    #grammar -> a dictionary of CNF
    #prob -> string problem

    #Set up variable
    numb = len(prob)

    if(numb == 0):
        return True
    parsetable = [[[] for i in range(numb)] for j in range(numb)]

    #CYK Algorithm
    #Fill first row
    for i in range(numb):
        terminal = prob[i]
        #Get all nonterminal that produces prob[i]
        terminal = [terminal]
        # print(terminal)
        for nonterm in grammar:
            if(terminal in grammar[nonterm]):
                parsetable[i][i].append(nonterm)
    
    #Fill the rest of parsetable

    for i in range(1, numb):
        for j in range(numb - i):
            ind = j + i
            for k in range(j, ind):
                for nonterm in grammar:
                    for prod in grammar[nonterm]:
                        if(len(prod) != 1):
                            if((prod[0] in parsetable[j][k]) and (prod[1] in parsetable[k + 1][ind]) and (nonterm not in parsetable[j][ind])):
                                parsetable[j][ind].append(nonterm)  

    for line in parsetable:
        print(line)

    if('S' in parsetable[0][numb-1]):
        return True
    else:
        return False

'''
S -> [['S_NONTERMINAL_1', 'BOOL_EXP'], ['S_NONTERMINAL_2', 'CLOSE_BRACKET'], ['True'], ['False']]
BOOL_EXP -> [['BOOL_EXP_NONTERMINAL_1', 'BOOL_EXP'], ['BOOL_EXP_NONTERMINAL_2', 'CLOSE_BRACKET'], ['True'], ['False']]
BOOL_OP -> [['and'], ['or'], ['not']]
AND -> [['and']]
OR -> [['or']]
NOT -> [['not']]
OPEN_BRACKET -> [['(']]
CLOSE_BRACKET -> [[')']]
BOOL -> [['True'], ['False']]
S_NONTERMINAL_1 -> [['BOOL', 'BOOL_OP']]
S_NONTERMINAL_2 -> [['OPEN_BRACKET', 'BOOL_EXP']]
BOOL_EXP_NONTERMINAL_1 -> [['BOOL', 'BOOL_OP']]
BOOL_EXP_NONTERMINAL_2 -> [['OPEN_BRACKET', 'BOOL_EXP']]'''