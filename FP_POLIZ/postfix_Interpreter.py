from  lex_my_lang_03 import lex, tableToPrint
from  lex_my_lang_03 import tableOfSymb, tableOfIdents, tableOfConst, tableOfLabel, sourceCode
from  postfixExpr_translator_02 import postfixTranslator, postfixCode, FSuccess
from stack01 import Stack

stack = Stack()

toView = True

def postfixInterpreter():
    FSuccess = postfixTranslator()
    # чи була успішною трансляція
    if (True,'Translator') == FSuccess:
        print('\nПостфіксний код: \n{0}'.format(postfixCode))
        return postfixProcessing()
    else:
        # Повідомити про факт виявлення помилки
        print('Interpreter: Translator завершив роботу аварійно')
        return False

print('-'*30)

# tableToPrint('All')
# print('\nПочатковий код програми: \n{0}'.format(sourceCode))

# while len(str(postfixCode))==0: pass
print('\nКод програми у постфіксній формі (ПОЛІЗ): \n{0}'.format(postfixCode))

# lenCode=len(str(postfixCode))
# print('\n---------------Код програми у постфіксній формі (ПОЛІЗ): \n{0}'.format(postfixCode))



def postfixProcessing():
    global stack, postfixCode
    maxNumb=len(postfixCode)
    try:
        for i in range(0,maxNumb):
            lex,tok = postfixCode.pop(0)

            if tok in ('int', 'real', 'ident', 'bool'):
               stack.push((lex,tok))
            else: doIt(lex,tok)
            if toView: configToPrint(i+1,lex,tok,maxNumb)
        return True
    except SystemExit as e:
        # Повідомити про факт виявлення помилки
        print('RunTime: Аварійне завершення програми з кодом {0}'.format(e))
    return True


def configToPrint(step,lex,tok,maxN):
    if step == 1:
        print('='*30+'\nInterpreter run\n')
        tableToPrint('All')

    print('\nКрок інтерпретації: {0}'.format(step))
    if tok in ('int','real'):
        print('Лексема: {0} у таблиці констант: {1}'.format((lex,tok),lex + ':' +str(tableOfConst[lex])))
    elif tok in ('ident'):
        print('Лексема: {0} у таблиці ідентифікаторів: {1}'.format((lex,tok), lex + ':' + str(tableOfIdents[lex])))
    elif tok in ('bool'):
        print('Лексема: {0} у таблиці ідентифікаторів: {1}'.format((lex,tok), lex + ':' + str(tableOfIdents[lex])))
    else:
        print('Лексема: {0}'.format((lex,tok)))

    print('postfixCode={0}'.format(postfixCode)) 
    stack.print()

    if  step == maxN: 
            for Tbl in ('Id','Const','Label'):
                tableToPrint(Tbl)
    return True

def doIt(lex,tok):
    global stack, postfixCode, tableOfIdents, tableOfConst, tableOfLabel
    if (lex,tok) == ('=', 'assign_op'):
        # зняти з вершини стека запис (правий операнд = число)
        (lexL,tokL) = stack.pop()
        # зняти з вершини стека ідентифікатор (лівий операнд)
        (lexR,tokR) = stack.pop()

        # виконати операцію:
        # оновлюємо запис у таблиці ідентифікаторів
        # ідентифікатор/змінна  
        # (index не змінюється, 
        # тип - як у константи,  
        # значення - як у константи)
        tableOfIdents[lexR] = (tableOfIdents[lexR][0], tableOfConst[lexL][1], tableOfConst[lexL][2])
    elif tok in ('add_op','mult_op'):
        # зняти з вершини стека запис (правий операнд)
        (lexR,tokR) = stack.pop()
        # зняти з вершини стека запис (лівий операнд)
        (lexL,tokL) = stack.pop()

        if (tokL,tokR) in (('int', 'real'),('real','int')):
            failRunTime('невідповідність типів',((lexL,tokL),lex,(lexR,tokR)))
        else:
            processing_add_mult_op((lexL,tokL),lex,(lexR,tokR))
            # stack.push()
            pass
    elif tok in ('pow_op'):
        # зняти з вершини стека запис (правий операнд)
        (lexR,tokR) = stack.pop()
        # зняти з вершини стека запис (лівий операнд)
        (lexL,tokL) = stack.pop()

        processing_pow_op((lexL,tokL),lex,(lexR,tokR))
        # stack.push()
        pass
    return True


def processing_pow_op(ltL,lex,ltR):
    global stack, postfixCode, tableOfIdents, tableOfConst, tableOfLabel
    lexL,tokL = ltL
    lexR,tokR = ltR
    if tokL == 'ident':
        # print(('===========',tokL , tableOfId[lexL][1]))
        # tokL = tableOfId[lexL][1]
        if tableOfIdents[lexL][1] == 'type_undef':
            failRunTime('неініціалізована змінна', (lexL, tableOfIdents[lexL], (lexL, tokL), lex, (lexR, tokR)))
        else:
            valL,tokL = (tableOfIdents[lexL][2], tableOfIdents[lexL][1])
    else:
        valL = tableOfConst[lexL][2]
    if tokR == 'ident':
        # print(('===========',tokL , tableOfId[lexL][1]))
        # tokL = tableOfId[lexL][1]
        if tableOfIdents[lexR][1] == 'type_undef':
            failRunTime('неініціалізована змінна', (lexR, tableOfIdents[lexR], (lexL, tokL), lex, (lexR, tokR)))
        else:
            valR,tokR = (tableOfIdents[lexR][2], tableOfIdents[lexR][1])
    else:
        valR = tableOfConst[lexR][2]
    # if :
        # print(('lexL',lexL,tableOfConst))
        # valL = tableOfConst[lexL][2]
        # valR = tableOfConst[lexR][2]
    getValue((valL,lexL,tokL),lex,(valR,lexR,tokR))


def processing_add_mult_op(ltL,lex,ltR): 
    global stack, postfixCode, tableOfIdents, tableOfConst, tableOfLabel
    lexL,tokL = ltL
    lexR,tokR = ltR
    if tokL == 'ident':
        # print(('===========',tokL , tableOfId[lexL][1]))
        # tokL = tableOfId[lexL][1]
        if tableOfIdents[lexL][1] == 'type_undef':
            failRunTime('неініціалізована змінна', (lexL, tableOfIdents[lexL], (lexL, tokL), lex, (lexR, tokR)))
        else:
            valL,tokL = (tableOfIdents[lexL][2], tableOfIdents[lexL][1])
    else:
        valL = tableOfConst[lexL][2]
    if tokR == 'ident':
        # print(('===========',tokL , tableOfId[lexL][1]))
        # tokL = tableOfId[lexL][1]
        if tableOfIdents[lexR][1] == 'type_undef':
            failRunTime('неініціалізована змінна', (lexR, tableOfIdents[lexR], (lexL, tokL), lex, (lexR, tokR)))
        else:
            valR,tokR = (tableOfIdents[lexR][2], tableOfIdents[lexR][1])
    else:
        valR = tableOfConst[lexR][2]
    # if :
        # print(('lexL',lexL,tableOfConst))
        # valL = tableOfConst[lexL][2]
        # valR = tableOfConst[lexR][2]
    getValue((valL,lexL,tokL),lex,(valR,lexR,tokR))

def getValue(vtL,lex,vtR):
    global stack, postfixCode, tableOfIdents, tableOfConst, tableOfLabel
    valL,lexL,tokL = vtL
    valR,lexR,tokR = vtR
    if (tokL,tokR) in (('int', 'real'),('real' ,'int')) and lex!='^':
        failRunTime('невідповідність типів',((lexL,tokL),lex,(lexR,tokR)))
    elif lex == '+':
        value = valL + valR
    elif lex == '-':
        value = valL - valR
    elif lex == '*':
        value = valL * valR
    elif lex == '^':
        value = valL ** valR
    elif lex == '/' and valR ==0:
        failRunTime('ділення на нуль',((lexL,tokL),lex,(lexR,tokR)))
    elif lex == '/' and tokL=='real':
        value = valL / valR
    elif lex == '/' and tokL=='int':
        value = valL / valR
    else:
        pass

    stack.push((str(value),tokL))
    toTableOfConst(value,tokL)
        # tableOfId[lexR] = (tableOfId[lexR][0],  tableOfConst[lexL][1], tableOfConst[lexL][2])

def toTableOfConst(val,tok):
    lexeme = str(val)
    indx1=tableOfConst.get(lexeme)   
    if indx1 is None:
        indx = len(tableOfConst)+1 
        tableOfConst[lexeme]=(indx,tok,val)


def failRunTime(str,tuple):
    if str == 'невідповідність типів':
        ((lexL,tokL),lex,(lexR,tokR))=tuple
        if lex == 'true': return ''
        else:
            print('RunTime ERROR: \n\t Типи операндів відрізняються у {0} {1} {2}'.format((lexL,tokL),lex,(lexR,tokR)))
            exit(1)
    elif str == 'неініціалізована змінна':
        (lx,rec,(lexL,tokL),lex,(lexR,tokR))=tuple
        print('RunTime ERROR: \n\t Значення змінної {0}:{1} не визначене. Зустрілось у {2} {3} {4}'.format(lx,rec,(lexL,tokL),lex,(lexR,tokR)))
        exit(2)
    elif str == 'ділення на нуль':
        ((lexL,tokL),lex,(lexR,tokR))=tuple
        print('RunTime ERROR: \n\t Ділення на нуль у {0} {1} {2}. '.format((lexL,tokL),lex,(lexR,tokR)))
        exit(3)



postfixInterpreter()

tableToPrint('tableOfId')
print(tableOfIdents)
print(tableOfConst)