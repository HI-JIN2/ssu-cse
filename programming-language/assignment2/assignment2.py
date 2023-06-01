from collections import deque

def error():
    print("syntax error!!")

def DIGIT(i_str, index, lexeme):
    temp = ""
    i = index
    cnt = 0
    while i < len(i_str):
        if i_str[i].isnumeric():
            temp += i_str[i]
        elif i_str[i] == ' ':
            pass
        else:
            break
        cnt += 1
        i += 1
    lexeme.append(temp)
    return cnt - 1

def tokenParse(i_str, lexeme):
    i = 0
    while i < len(i_str):
        if i_str[i] == ' ': 
            i += 1
            continue
        elif i_str[i] >= '0' and i_str[i] <= '9':
            i += DIGIT(i_str, i, lexeme)
        elif i_str[i] == '*' or i_str[i] == '/' or i_str[i] == '+' or i_str[i] == '-' or i_str[i] == '(' or i_str[i] == ')':
            lexeme.append(i_str[i])
        elif i_str[i] == '>' or i_str[i] == '<' or i_str[i:i+2] == ">=" or i_str[i:i+2] == "<=" or i_str[i:i+2] == "==" or i_str[i:i+2] == "!=":
            lexeme.append(i_str[i:i+2])
            i += 1
        else:
            error()
            return
        i += 1

def bexpr(lexeme):
    left = aexpr(lexeme)
    if nextValue(lexeme) in ["<", ">"]:
        oper = lex(lexeme)
        right = aexpr(lexeme)
        if oper == "<":
            return left < right
        elif oper == ">":
            return left > right
    elif nextValue(lexeme) in ["<=", ">=", "==", "!="]:
        oper = lex(lexeme)
        right = aexpr(lexeme)
        if oper == "<=":
            return left <= right
        elif oper == ">=":
            return left >= right
        elif oper == "==":
            return left == right
        elif oper == "!=":
            return left != right
    else:
        error()
        return
    
def relOp(lexeme):
    op = lex(lexeme)
    
    if op in ["==", "!=", "<", ">", "<=", ">="]:
        return op
    else:
        error()
        return

def expr(lexeme):
    if nextValue(lexeme) == "(" or nextValue(lexeme).isnumeric():
        if nextValue(lexeme) == "(":
            lex(lexeme)
            data = aexpr(lexeme)
            if nextValue(lexeme) == ")":
                lex(lexeme)
            else:
                error()
                return
        else:
            data = aexpr(lexeme)

        if nextValue(lexeme) in ["==", "!=", "<", ">", "<=", ">="]:
            return bexpr(lexeme)
        else:
            return data
    else:
        error()
        return


def aexpr(lexeme):
    data = term(lexeme)

    while nextValue(lexeme) == "*" or nextValue(lexeme) == "/":
        oper = lex(lexeme)

        if oper == "*":
            data *= term(lexeme)
        elif oper == "/":
            data /= term(lexeme)
        else:
            error()
            return
    return data

def term(lexeme):
    data = factor(lexeme)
    while nextValue(lexeme) == "+" or nextValue(lexeme) == "-":
        oper = lex(lexeme)
        if oper == "+":
            data += factor(lexeme)
        elif oper == "-":
            data -= factor(lexeme)
        else:
            error()
            return
    return data

def factor(lexeme):
    oper = "+"
    if nextValue(lexeme) == "-":
        oper = lex(lexeme)
    
    if nextValue(lexeme).isnumeric():
        data = number(lexeme)
    else:
        if nextValue(lexeme) == "(":
            lex(lexeme)
            data = aexpr(lexeme)
            if nextValue(lexeme) == ")":
                lex(lexeme)
            else:
                error()
                return
        else:
            error()
            return
    
    if oper == "-":
        return -data
    else:
        return data

def number(lexeme):
    num = lex(lexeme)
    return int(num)

def lex(lexeme):
    if lexeme:
        return lexeme.popleft()
    else:
        return ""


def nextValue(lexeme):
    if lexeme:
        returnData = lexeme.popleft()
        lexeme.appendleft(returnData)
        return returnData
    else:
        return ""

while True:
    inputStr = input('>> ')
    if not inputStr:
        break

    lexeme = deque()
    tokenParse(inputStr, lexeme)
        # aexpr() 함수에서 error() 함수를 호출한 경우, 에러 메시지를 출력하고 다시 입력 받기
    try:
        ans = aexpr(lexeme)
    except:
        error()
        continue

    if lexeme:
        error()
        continue

    print(ans)
