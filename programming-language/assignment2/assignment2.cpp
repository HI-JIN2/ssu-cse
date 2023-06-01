#include <iostream>
#include <cstring>
#include <queue>
using namespace std;

queue<string> Q;

// function
void error();
int dec(string, int);
void tokenParse(string);
bool expr();
bool bexpr();
double aexpr();
double term();
double factor();
int number();
string lex();
bool relop();
string nextValue();
void queueClear();

void error()
{
    cout << "syntax error!!\n";
    queueClear();
}

int dec(string str, int index)
{
    string temp = "";
    int cnt = 0;
    for (int i = index; i < str.length(); i++, cnt++)
    {
        if (str[i] >= '0' && str[i] <= '9')
            temp += str[i];
        else if (str[i] == ' ')
            continue;
        else
            break;
    }
    Q.push(temp);
    return cnt - 1; // i++ is already in tokenParse()
}


void tokenParse(string str) {
    for(int i=0; i<str.length(); i++) {
        if(str[i] == ' ') continue;
        else if(str[i] >= '0' && str[i] <= '9') {
            i += dec(str, i);
        }
        else if(str[i] == '*' || str[i] == '/' || str[i] == '+' ||
                str[i] == '-' || str[i] == '(' || str[i] == ')') {
            string temp = "";
            temp += str[i];
            Q.push(temp);
        }
        else if(str[i] == '=' && str[i+1] == '='){ // == 추가
            string temp = "";
            temp += "==";
            Q.push(temp);
            i++;
        }
        else if(str[i] == '!' && str[i+1] == '='){ // != 추가
            string temp = "";
            temp += "!=";
            Q.push(temp);
            i++;
        }
        else if(str[i] == '<' && str[i+1] == '='){ // <= 추가
            string temp = "";
            temp += "<=";
            Q.push(temp);
            i++;
        }
        else if(str[i] == '>' && str[i+1] == '='){ // >= 추가
            string temp = "";
            temp += ">=";
            Q.push(temp);
            i++;
        }
        else if(str[i] == '<' || str[i] == '>' ){ // <, >, 추가
            error();
        }
        else {
            error();
        }
    }
}bool bexpr() {
    bool left = expr();  // 식을 반환하는 expr 함수 호출
    if (relop()) {
        string oper = lex();  // 비교 연산자를 읽어옴
        bool right = expr();  // 식을 반환하는 expr 함수 호출
        if (oper == "<") return left < right;
        else if (oper == ">") return left > right;
        else if (oper == "==") return left == right;
        else if (oper == "!=") return left != right;
        else if (oper == "<=") return left <= right;
        else if (oper == ">=") return left >= right;
        else error();
    }
    else {
        return left;
    }
}

bool relop() {
    string temp = nextValue();
    if (temp == "<" || temp == ">" || temp == "==" || temp == "!=" || temp == "<=" || temp == ">=") {
        lex();  // 다음 토큰을 가져옴
        return true;
    }
    else {
        return false;
    }
}


bool expr(){
    if (lex() == "==" || lex() == "!=" || lex() == "<" || lex() == ">" || lex() == "<=" || lex() == ">="){
        return bexpr();
    }
    else {
        return aexpr()!=0;
    }
}

double aexpr()
{
    double data = 0;
    data = term();

    while (nextValue() == "*" || nextValue() == "/")
    {
        char oper;
        oper = lex()[0];

        if (oper == '*')
            data *= term();
        else if (oper == '/')
            data /= term();
    }
    return data;
}

double term()
{
    double data = 0;
    data = factor();
    while (nextValue() == "+" || nextValue() == "-")
    {
        char oper;
        oper = lex()[0];
        if (oper == '+')
            data += factor();
        else if (oper == '-')
            data -= factor();
    }
    return data;
}

double factor()
{
    double data = 0;
    char oper = '+';
    if (nextValue() == "-")
    {
        oper = lex()[0];
    }
    // if nextValue is digit
    if (nextValue()[0] >= '0' && nextValue()[0] <= '9')
        data = number();
    //( <expr> )
    else
    {
        if (nextValue() == "(")
        {
            lex();
            data = aexpr();
            if (nextValue() == ")")
            {
                lex();
            }
            else{
                error();
            }
        }
        else{
                error();
            }
    }
    if (oper == '-')
        return -data;
    else
        return data;
}

int number()
{
    string NUM = lex();
    return stoi(NUM);
}

string lex()
{
    if (!Q.empty())
    {
        string value = Q.front();
        Q.pop();
        return value;
    }
    else
        return "";
}

string nextValue()
{
    if (!Q.empty())
        return Q.front();
    else
        return "";
}

void queueClear()
{
    while (!Q.empty())
        Q.pop();
}

int main()
{
    while (1)
    {
        double ans = 0;
        string str;
        queueClear();
        cout << ">> ";
        getline(cin, str);
        if (str == "")
            break; // 입력된 수식이 없으면 종료
        tokenParse(str);
        ans = aexpr();
        if (!Q.empty())
        {
            error();
            continue;
        }
        cout << ans << '\n';
    }
}