#include <iostream>
#include <algorithm>
#include <vector>
using namespace std;

vector<int> Parent;
vector<pair<int, pair<int, int>>> W;
vector<pair<int, pair<int, int>>> F;
/*
1 2 1
1 3 3
2 3 3
2 4 6
3 4 4
3 5 2
4 5 5
*/

typedef int set_pointer;
struct nodetype
{
    int parent;
    int depth;
};
/*
typedef nodetype universe[n];
universe U;
void makeset (int i) {
    U[i].parent = i;
    U[i].depth = 0; }*/

/*int W[3][7] = {
    { 1, 2, 1 },
    { 1, 3, 3 },
    { 2, 3, 3 },
    { 2, 4, 6 },
    { 3, 4, 4 },
    { 3, 5, 2 },
    { 4, 5, 5 }};*/

/*
int U;

void makeset (int i) {
    U[i] = i; }

void initial (int n) {
    int i;
    for (i=1; i<=n; i++)
        makeset(i);   }
*/
// 2. 1번 과정을 위해서, 부모를 찾는 find함수
int find(vector<int> &parent, int x) // 노드 x의 부모를 찾는 함수
{
    if (parent[x] == x)
        return x;
    return parent[x] = find(parent, parent[x]);
}

// 3. 서로 다른 부모일 경우, 두 개의 노드를 연결해주는 union 함수
void merge(vector<int> &parent, int x, int y) // 노드 x와 y를 합쳐주는 함수
{
    x = find(parent, x);
    y = find(parent, y);
    if (x < y)
        parent[y] = x;
    else
        parent[x] = y;
}
// 1. 서로 같은 부모를 갖는지 판단해주는 함수
bool equal(vector<int> &parent, int x, int y) // 노드 x와 y가 서로 같은 부모를 갖는지 아닌지 판단해주는 함수
{
    x = find(Parent, x); // 노드 x의 부모 찾기
    y = find(Parent, y); // 노드 y의 부모 찾기

    if (x == y)
        return true; // 두 부모가 같은 부모라면, true를 반환
    else
        return false; // 두 부모가 서로 다른 부모라면, false를 반환
}

int main()
{
    //정점, 간선 개수
    int v = 5, e = 7;

    //부모배열의 크기 resize
    Parent.resize(v + 1);
    // 부모 배열 초기화
    for (int i = 1; i <= v; i++)
        Parent[i] = i;

    // 1. 간선의 크기만큼 그래프를 생성
    // F.resize(e);

    // 2.[거리 ,[시작노드, 끝노드]] 순으로 그래프에 넣어주기
    for (int i = 0; i < e; i++)
    {
        int a, b, c;
        scanf("%d %d %d", &a, &b, &c);
        W.push_back(make_pair(c, make_pair(a, b))); // make_pair(a,b) : a,b가 들어간 pair를 만들어준다
    }
    // 3.그래프의 가중치를 오름차순으로 정리한다.
    sort(W.begin(), W.end());

    cout << "-----sort-----" << endl
         << "weight, (a,b)" << endl;
    for (int i = 0; i < e; i++)
        cout << W[i].first << " " << W[i].second.first << " " << W[i].second.second << endl;

    int sum = 0; //가중치를 합하자

    // 4. 간선값이 가장 작은 녀석부터 이어간다
    for (int i = 0; i < e; i++)
    {
        //시작노드와 끝노드가 이미 합집합이라면!??!??! 이미 이어진거니까 최소비용이 아니다! 넘겨버리자.
        if (!equal(Parent, W[i].second.first, W[i].second.second))
        {
            // 시작 노드와 끝노드를 합집합하자. => union 사용
            merge(Parent, W[i].second.first, W[i].second.second);

            // 시작노드와 끝노드가 합집합이라는건 길이 연결됐다는 뜻이므로 가중치를 더해주자.
            sum += W[i].first;

            // add e to F;
            F.push_back({W[i].first, {W[i].second.first, W[i].second.second}});
        }
    }

    cout << "-----F-----" << endl;
    for (int i = 0; i < v-1; i++)
        cout << F[i].first << " " << F[i].second.first << " " << F[i].second.second << endl;
    
    cout << "sum of weight=" << sum << endl;
}