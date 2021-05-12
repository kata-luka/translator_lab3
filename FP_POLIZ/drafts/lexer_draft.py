AnalyzingLogs = []

FSuccess = (True, 'Lexer')

tableOfLanguageTokens = {
    'integer': 'keyword',
    'real': 'keyword',
    'boolean': 'keyword',
    'read': 'keyword',
    'write': 'keyword',
    'startprogram': 'keyword',
    'endprogram': 'keyword',
    'program': 'keyword',
    'do': 'keyword',
    'while': 'keyword',
    'if': 'keyword',
    '=': 'assign_op',
    '+': 'add_op',
    '-': 'add_op',
    '*': 'mult_op',
    '/': 'mult_op',
    '<': 'rel_op',
    '>': 'rel_op',
    '>=': 'rel_op',
    '<=': 'rel_op',
    '==': 'rel_op',
    '!=': 'rel_op',
    '&&': 'and',
    '^': 'mult_op',
    '^E': 'exponent',
    '||': 'or',
    '(': 'brackets_op',
    ')': 'brackets_op',
    '{': 'brackets_op',
    '}': 'brackets_op',
    '.': 'dot',
    ',': 'punct',
    '?': 'punct',
    ':': 'punct',
    ';': 'punct',
    ' ': 'ws',
    '\t': 'ws',
    '\n': 'eol',
    '\0': 'eof'
}

tableIdentFloatInt = {
    2: 'ident',
    6: 'float',
    4: 'int'
}

stf = {
    (0, 'ws'): 0,
    (0, ','): 11,
    (0, 'Letter'): 1,
    (0, 'Digit'): 3,
    (0, ':'): 11,
    (0, '<'): 12,
    (0, '>'): 12,
    (0, '('): 11,
    (0, ')'): 11,
    (0, '*'): 22,
    (0, '^'): 23,
    (23, 'Letter'): 24,
    (23, 'other'): 25,
    (0, '/'): 22,
    (0, ';'): 11,
    (0, '+'): 22,
    (0, '!'): 15,
    (0, '{'): 11,
    (0, '?'): 11,
    (0, '}'): 11,
    (0, '-'): 22,
    (0, '&'): 7,
    (0, '|'): 9,
    (0, '='): 21,
    (0, 'eol'): 18,
    (0, 'eof'): 20,
    (0, 'other'): 105,
    (0, 'dot'): 11,
    (1, 'Letter'): 1,
    (1, 'Digit'): 1,
    (1, 'other'): 2,
    (3, 'Digit'): 3,
    (3, 'dot'): 5,
    (3, 'other'): 4,
    (5, 'Digit'): 5,
    (5, 'other'): 6,
    (12, '='): 13,
    (12, 'other'): 14,
    (15, '='): 16,
    (15, 'other'): 103,
    (7, '&'): 8,
    (7, 'other'): 101,
    (9, '|'): 10,
    (9, 'other'): 102,
}

initState = 0
state = initState

F = {2, 4, 6, 13, 11, 102, 10, 101, 22, 8, 14, 16, 103, 18, 21, 104, 19, 20, 105, 24, 25}
Fstar = {2, 4, 6, 14, 25}
Ferror = {101, 102, 103, 105}

tableOfIdents = {}
tableOfConst = {}
tableOfSymb = {}
tableOfLabel = {}
tableOfWrite = {}

f = open('test.lang', 'r')
sourceCode = f.read()
f.close()
lenCode = len(sourceCode) - 1
numLine = 1
numCharInLine = 0
numChar = -1
char = ''
lexeme = ''
failed = 0


def lex():
    global state, char, lexeme, FSuccess  # ,numChar, numLine
    try:
        while numChar < lenCode:
            char = nextChar()
            classCh = classOfChar(char)
            state = nextState(state, classCh)
            if (is_final(state)):
                processing()
                # if state in Ferror:
                # break
            elif state == 0:
                lexeme = ''
            else:
                lexeme += char
                # tableToPrint('All')
    except SystemExit as e:
        # Встановити ознаку неуспішності
        FSuccess = (False, 'Lexer')
        # Повідомити про факт виявлення помилки
        print('Lexer: Аварійне завершення програми з кодом {0}'.format(e))


def processing():
    global state, lexeme, char, numLine, numChar, tableOfSymb
    if state == 20:
        is_final(state)
    if state in (2, 6, 4):  # keyword, ident, float, int
        token = getToken(state, lexeme)
        if token != 'keyword':  # не keyword
            index = indexVarConst(state, lexeme, token)
            tableOfSymb[len(tableOfSymb) + 1] = (numLine, lexeme, token, index)
        else:  # якщо keyword
            tableOfSymb[len(tableOfSymb) + 1] = (numLine, lexeme, token, '')
        print('{0:<3d} {1:<10s} {2:<10s} '.format(numLine, lexeme, token))
        lexeme = ''
        numChar = putCharBack(numChar)  # зірочка
        state = 0
    if state in (14, 25):  # keyword, ident, float, int
        token = getToken(state, lexeme)
        print('{0:<3d} {1:<10s} {2:<10s} '.format(numLine, lexeme, token))
        tableOfSymb[len(tableOfSymb) + 1] = (numLine, lexeme, token, '')
        lexeme = ''
        state = 0
        numChar = putCharBack(numChar)  # зірочка
    if state in (21, 24):  # assign_op
        lexeme += char
        token = getToken(state, lexeme)
        print('{0:<3d} {1:<10s} {2:<10s} '.format(numLine, lexeme, token))
        tableOfSymb[len(tableOfSymb) + 1] = (numLine, lexeme, token, '')
        lexeme = ''
        state = 0
    if state in (22, 13, 16, 8, 10, 11, 18):
        lexeme += char
        token = getToken(state, lexeme)
        print('{0:<3d} {1:<10s} {2:<10s} '.format(numLine, lexeme, token))
        tableOfSymb[len(tableOfSymb) + 1] = (numLine, lexeme, token, '')
        lexeme = ''
        state = 0
    if state in (101, 102, 103, 104, 105):  # ERROR
        fail()


def fail():
    global state, numLine, char
    print(numLine)
    if state == 101:
        print('у рядку ', numLine, ' неочікуваний символ після &' + char)
    if state == 102:
        print('у рядку ', numLine, ' неочікуваний символ після | ' + char)
    if state == 103:
        print('у рядку ', numLine, ' неочікуваний символ після ! ' + char)
    if state == 105:
        print('у рядку ', numLine, ' неочікуваний символ ' + char)


def is_final(state):
    if (state in F):
        return True
    else:
        return False


def nextState(state, classCh):
    try:
        return stf[(state, classCh)]
    except KeyError:
        return stf[(state, 'other')]


def nextChar():
    global numChar
    numChar += 1
    return sourceCode[numChar]


def putCharBack(numChar):
    return numChar - 1


def classOfChar(char):
    if char in '.':
        res = "dot"
    elif char in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMOPQRSTUVWXYZ':
        res = "Letter"
    elif char in "0123456789":
        res = "Digit"
    elif char in " \t":
        res = "ws"
    elif char in "\n":
        res = "eol"
    elif char in "\0":
        res = "eof"
    elif char in "+-:=()&|<>*/{}?,;.^":
        res = char
    return res


def getToken(state, lexeme):
    try:
        return tableOfLanguageTokens[lexeme]
    except KeyError:
        return tableIdentFloatInt[state]


def indexVarConst(state, lexeme, token):
    indx = 0
    if state == 2:
        indx1 = tableOfIdents.get(lexeme)
        if indx1 is None:
            indx = len(tableOfIdents) + 1
            tableOfIdents[lexeme] = (indx, 'type_undef', 'val_undef')
    if state in (6, 4):
        indx1 = tableOfConst.get(lexeme)
        if indx1 is None:
            indx = len(tableOfConst) + 1
    if state == 6:
        val = float(lexeme)
    elif state == 4:
        val = int(lexeme)
        tableOfConst[lexeme] = (indx, token, val)
    return indx


def printDict(dict):
    for key in dict:
        print(str(key) + ': {0}'.format(dict[key]))


def printResult():
    global failed
    if (not failed):
        for log in AnalyzingLogs:
            print(log)
        print('-' * 30)
        print('Analyzing: \n')
        print('-' * 30)
        print('Table of symbols: \n')
        printDict(tableOfSymb)
        print('-' * 30)
        print('Table of idents: \n')
        printDict(tableOfIdents)
        print('-' * 30)
        print('Table of consts: \n')
        printDict(tableOfConst)
        print('-' * 30)


def tableToPrint(Tbl):
    if Tbl == "Symb":
        tableOfSymbToPrint()
    elif Tbl == "Id":
        tableOfIdToPrint()
    elif Tbl == "Const":
        tableOfConstToPrint()
    elif Tbl == "Label":
        tableOfLabelToPrint()
    elif Tbl == "Write":
        tableOfWritePrint()
    else:
        tableOfSymbToPrint()
        tableOfIdToPrint()
        tableOfConstToPrint()
        tableOfLabelToPrint()
        tableOfWritePrint()
    return True


def tableOfSymbToPrint():
    print("\n Таблиця символів")
    s1 = '{0:<10s} {1:<10s} {2:<10s} {3:<10s} {4:<5s} '
    s2 = '{0:<10d} {1:<10d} {2:<10s} {3:<10s} {4:<5s} '
    print(s1.format("numRec", "numLine", "lexeme", "token", "index"))
    for numRec in tableOfSymb:  # range(1,lns+1):
        numLine, lexeme, token, index = tableOfSymb[numRec]
        print(s2.format(numRec, numLine, lexeme, token, str(index)))


def tableOfIdToPrint():
    print("\n Таблиця ідентифікаторів")
    s1 = '{0:<10s} {1:<15s} {2:<15s} {3:<10s} '
    print(s1.format("Ident", "Type", "Value", "Index"))
    s2 = '{0:<10s} {2:<15s} {3:<15s} {1:<10d} '
    for id in tableOfIdents:
        index, type, val = tableOfIdents[id]
        # print((id, index, type, str(val)))
        print(s2.format(id, index, type, str(val)))


def tableOfWritePrint():
    print("\n Таблиця виведених значень")
    if len(tableOfWrite) == 0:
        print("\n Таблиця виводу - порожня")
    else:
        s1 = '{0:<10s} {1:<15s} '
        print(s1.format("Змінна", "Значення"))
        s2 = '{0:<10s} {1:<10s} '
    for id in tableOfWrite:
        (lex, val) = tableOfWrite[id]
        # print((id, index, type, str(val)))
        print(s2.format(lex, str(val)))


def tableOfConstToPrint():
    print("\n Таблиця констант")
    s1 = '{0:<10s} {1:<10s} {2:<10s} {3:<10s} '
    print(s1.format("Const", "Type", "Value", "Index"))
    s2 = '{0:<10s} {2:<10s} {3:<10} {1:<10d} '
    for cnst in tableOfConst:
        index, type, val = tableOfConst[cnst]
        print(s2.format(str(cnst), index, type, val))


def tableOfLabelToPrint():
    if len(tableOfLabel) == 0:
        print("\n Таблиця міток - порожня")
    else:
        s1 = '{0:<10s} {1:<10s} '
        print("\n Таблиця міток")
        print(s1.format("Label", "Value"))
        s2 = '{0:<10s} {1:<10s} '
        for lbl in tableOfLabel:
            val = tableOfLabel[lbl]
            print(s2.format(lbl, val))


lex()
printResult()
# Таблиці: розбору, ідентифікаторів та констант
print('-' * 30)
print('Таблиця розбору tableOfSymb:{0}'.format(tableOfSymb))
print('-' * 30)
print('Таблиця ідентифікаторів tableOfVar:{0}'.format(tableOfIdents))
print('-' * 30)
print('таблиця констант tableOfConst:{0}'.format(tableOfConst))
