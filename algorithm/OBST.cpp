#include <iostream>
using namespace std;
#define N 4
//float p[4] = {(float)3/8, (float)3/8, (float)1/8, (float)1/8};
float p[4] = {(float)5/8, (float)1/8, (float)3/8, (float)1/8};
struct nodetype{
    int key;
    nodetype* left;
    nodetype* right;
};

void search(nodetype* tree, int keyin, nodetype*& p) {
    bool found;
    p = tree;
    found = false;
    while(!found){
        if (p -> key == keyin) found = true;
        else if(keyin < p -> key) p = p -> left;
        else p = p -> right;
    }
}

float sum(int start, int end, const float p[]){
    float result = 0;
    for(int i = start; i <= end; i++){
        result += p[i - 1];
    }
    return result;
}

void optsearchtree(int n, const float p[], float& minavg, int (*R)[N + 2]){
    int i, j, k, diagonal;
    float A[n + 2][n + 2];
    for(int i = 0; i < N + 2; i++){
        for(int j = 0; j < N + 2; j++){
            A[i][j] = 999;
        }
    }

    for(i = 0; i < n; i++){
        j = i + 1;
        A[j][i] = 0;
        A[j][j] = p[i];

        R[j][j] = j;
        R[j][i] = 0;
    }

    A[n + 1][n] = 0;
    R[n + 1][n] = 0;

    for(diagonal = 1; diagonal <= n - 1; diagonal++){
        for(i = 1; i <= n - diagonal; i++){
            j = i + diagonal;

            for(int k = i; k <= j; k++){
                if(A[i][j] > A[i][k - 1] + A[k + 1][j] + sum(i, j, p)){
                    A[i][j] = A[i][k - 1] + A[k + 1][j] + sum(i, j, p);
                    R[i][j] = k;
                }
            }
        }
    }

    cout << "***** A *****" <<endl;
    for(int i = 0; i < N + 2; i++){
        for(int j = 0; j < N + 2; j++){
            //cout.width(6);
            if(A[i][j]!=999)
                cout << A[i][j]<<"\t";
            if(A[i][j]==999)
                cout<<"\t";
        }
        cout << endl;
    }
    cout << endl;
    minavg = A[1][n];
}

int main(void) {
    
    int R[N + 2][N + 2];
    for(int i = 0; i < N + 2; i++){
        for(int j = 0; j < N + 2; j++){
            R[i][j] = 0;
        }
    }
    float minavg = 999;
    optsearchtree(N, p, minavg, R);


    cout << "***** R *****" <<endl;
    for(int i = 0; i < N + 2; i++){
        for(int j = 0; j < N + 2; j++){
            if(R[i][j]!=0)
                cout << R[i][j]<<"\t";
            if(R[i][j]==0)
                cout <<"\t";
        }
        cout << endl;
    }
    cout << endl;
}