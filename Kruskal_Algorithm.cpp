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
// 2. 1�� ������ ���ؼ�, �θ� ã�� find�Լ�
int find(vector<int> &parent, int x) // ��� x�� �θ� ã�� �Լ�
{
    if (parent[x] == x)
        return x;
    return parent[x] = find(parent, parent[x]);
}

// 3. ���� �ٸ� �θ��� ���, �� ���� ��带 �������ִ� union �Լ�
void merge(vector<int> &parent, int x, int y) // ��� x�� y�� �����ִ� �Լ�
{
    x = find(parent, x);
    y = find(parent, y);
    if (x < y)
        parent[y] = x;
    else
        parent[x] = y;
}
// 1. ���� ���� �θ� ������ �Ǵ����ִ� �Լ�
bool equal(vector<int> &parent, int x, int y) // ��� x�� y�� ���� ���� �θ� ������ �ƴ��� �Ǵ����ִ� �Լ�
{
    x = find(Parent, x); // ��� x�� �θ� ã��
    y = find(Parent, y); // ��� y�� �θ� ã��

    if (x == y)
        return true; // �� �θ� ���� �θ���, true�� ��ȯ
    else
        return false; // �� �θ� ���� �ٸ� �θ���, false�� ��ȯ
}

int main()
{
    //����, ���� ����
    int v = 5, e = 7;

    //�θ�迭�� ũ�� resize
    Parent.resize(v + 1);
    // �θ� �迭 �ʱ�ȭ
    for (int i = 1; i <= v; i++)
        Parent[i] = i;

    // 1. ������ ũ�⸸ŭ �׷����� ����
    // F.resize(e);

    // 2.[�Ÿ� ,[���۳��, �����]] ������ �׷����� �־��ֱ�
    for (int i = 0; i < e; i++)
    {
        int a, b, c;
        scanf("%d %d %d", &a, &b, &c);
        W.push_back(make_pair(c, make_pair(a, b))); // make_pair(a,b) : a,b�� �� pair�� ������ش�
    }
    // 3.�׷����� ����ġ�� ������������ �����Ѵ�.
    sort(W.begin(), W.end());

    cout << "-----sort-----" << endl
         << "weight, (a,b)" << endl;
    for (int i = 0; i < e; i++)
        cout << W[i].first << " " << W[i].second.first << " " << W[i].second.second << endl;

    int sum = 0; //����ġ�� ������

    // 4. �������� ���� ���� �༮���� �̾��
    for (int i = 0; i < e; i++)
    {
        //���۳��� ����尡 �̹� �������̶��!??!??! �̹� �̾����Ŵϱ� �ּҺ���� �ƴϴ�! �Ѱܹ�����.
        if (!equal(Parent, W[i].second.first, W[i].second.second))
        {
            // ���� ���� ����带 ����������. => union ���
            merge(Parent, W[i].second.first, W[i].second.second);

            // ���۳��� ����尡 �������̶�°� ���� ����ƴٴ� ���̹Ƿ� ����ġ�� ��������.
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