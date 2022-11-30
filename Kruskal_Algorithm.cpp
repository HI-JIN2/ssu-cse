#include <iostream>
#include <algorithm>
#include <vector>
using namespace std;

//vector<int> U;
vector<pair<int, pair<int, int>>> E;
vector<pair<int, pair<int, int>>> F;

/* 교재 데이터
1 2 1
1 3 3
2 3 3
2 4 6
3 4 4
3 5 2
4 5 5
*/

typedef struct{
    int parent;
    int depth;
}nodetype;

void initial(nodetype* U, int n){
    for(int i = 1; i <= n; i++){
        U[i].parent = i;
        U[i].depth = 0;
    }
}

// 부모를 찾는 find 함수
int find(nodetype* U, int i)
{
    int j;    
    j = i;
    while (U[j].parent != j) 
        j=U[j].parent;    
    
    return j;
}

// 서로 다른 부모일 경우, 두 개의 노드를 연결해주는 함수
void merge(nodetype* U, int p, int q) // 노드 x와 y를 합쳐주는 함수
{   
    if (U[p].depth == U[q].depth) { 
        U[p].depth =+1; 
        U[q].parent =p;        
        }
    else if (U[p].depth < U[q].depth) 
        U[p].parent =q; 
    else U[q].parent = p;
}

// 서로 같은 부모를 갖는지 판단해주는 함수
bool equal(nodetype* U, int x, int y) // 노드 x와 y가 서로 같은 부모를 갖는지 아닌지 판단해주는 함수
{
    
    x = find(U, x); // 노드 x의 부모 찾기
    y = find(U, y); // 노드 y의 부모 찾기

    if (x == y)
        return true; // 두 부모가 같은 부모라면, true를 반환
    else
        return false; // 두 부모가 서로 다른 부모라면, false를 반환
}

int kruskal(int v, int e, vector<pair<int, pair<int, int>>> E,vector<pair<int, pair<int, int>>>& F)
{
    nodetype U[v + 1];
    initial(U, v);
    //initial
    //[거리 ,[시작노드, 끝노드]] 순으로 그래프에 넣어주기
    for (int i = 0; i < e; i++)
    {
        int a, b, c;
        scanf("%d %d %d", &a, &b, &c);
        E.push_back(make_pair(c, make_pair(a, b))); // make_pair(a,b) : a,b가 들어간 pair를 만들어준다
    }
    //그래프의 가중치를 오름차순으로 정리한다.
    sort(E.begin(), E.end());

    cout << "-----sort-----" << endl
         << "weight, <a,b>" << endl;
    for (int i = 0; i < e; i++)
        cout << E[i].first << " " << E[i].second.first << " " << E[i].second.second << endl;

    int sum = 0; //가중치를 합하자

    //간선값이 가장 작은 녀석부터 이어간다
    for (int i = 0; i < e; i++)
    {

        //시작노드와 끝노드가 이미 합집합이라면, 이미 이어진거니까 최소비용이 아니다 넘겨버리자.
        if (!equal(U,E[i].second.first,E[i].second.second))
        {
            // 시작 노드와 끝노드를 합집합하자.
            merge(U, E[i].second.first, E[i].second.second);

            // 시작노드와 끝노드가 합집합이라는건 길이 연결됐다는 뜻이므로 가중치를 더해주자.
            sum += E[i].first;

            // add e to F;
            F.push_back({E[i].first, {E[i].second.first, E[i].second.second}});
        }
    }

    cout << "-----F-----" << endl;
    for (int i = 0; i < v-1; i++)
        cout << F[i].first << " " << F[i].second.first << " " << F[i].second.second << endl;
    
    return sum;
}

int main()
{
    //정점, 간선 개수
    int v = 5, e = 7;

    int sum=kruskal(v, e, E, F);   
    cout << "sum of weight=" << sum << endl;
}