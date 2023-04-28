#include <iostream>
#include<cmath>
#include<algorithm>
using namespace std;
#define INF 999

int i, j, k, diagonal;

int minmult(int n, const int d[], int P[][])
{  
    int M[n][n];

    for (i = 1; i <= n; i++)
        M[i][i] = 0;
    for (diagonal = 1; diagonal <= n - 1; diagonal++)
        for (i = 1; i <= n - diagonal; i++)
        {
            j = i + diagonal;
            if(j==i){//diagonal 1
                M[i][j]=0;
                continue;
            }
            
            M[i][j]=INF;
            for(k=i;i<=j-1;k++){
                M[i][j] = min(M[i][j], M[i][k] + M[k+1][j] + d[i-1]*d[k] *d[j]);
                P[i][j] = k;
            }
        }
    return M[1][n];
}

void order(int i, int j)
{
    if (i == j)
        cout << "A" << i;
    else
    {
        k = P[i][j];
        cout << "(";
        order(i, k);
        order(k + 1, j);
        cout << ")";
    }
}

int main(){
    int n =4;

    minmult(n, diagonal, P);
    
}