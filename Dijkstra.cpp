#include <iostream>
#include<vector>
using namespace std;
#define INF 999
#define n 5
vector<pair<int,int>> F;
/*int W[6][6] = {
    {0, 0, 0, 0, 0, 0},
    {0, 0, 7, 4, 6, 1},
    {0, INF, 0, INF, INF, INF},
    {0, INF, 2, 0, 5, INF},
    {0, INF, 3, INF, 0, INF},
    {0, INF, INF, INF, 1, 0}};*/
int W[6][6] = {
    {0, 0, 0, 0, 0, 0},
    {0, 0, 1,5,4,2},
    {0, INF, 0, INF, INF, INF},
    {0, INF, INF, 0, 1, INF},
    {0, INF, 2, INF, 0, INF},
    {0, INF, INF, INF, 1, 0}};
void dijkstra()
{
    int vnear;
    int touch[n + 1]; 
    int length[n + 1];
    int min;

    for (int i = 2; i <= n; i++)
    {
        touch[i] = 1;
        length[i] = W[1][i];
    }


    for (int k = 1; k <= n - 1; k++) // repeat n-1번
    {
        min = INF;
        for (int i = 2; i <= n; i++)
        {
            if (0 <= length[i] && length[i] <= min)
            {
                min = length[i];
                vnear = i;       
            }
        }

        cout << "min=" << min << " vnear=" << vnear << endl;
        F.push_back({touch[vnear], vnear});

        for (int i = 2; i <= n; i++)
        {
            if (length[vnear] + W[vnear][i] < length[i])
            {
                length[i] = length[vnear] + W[vnear][i];
                touch[i] = vnear;
                cout << "length[" << i << "]=" << length[i] << " touch[" << i << "]=" << vnear << endl;
            }
            
        } 
        length[vnear] = -1;
        
        for (int i = 2; i <= n; i++)
        {
            cout << touch[i] << " ";
        }
        cout << endl;
        for (int i = 2; i <= n; i++)
        {
            cout << length[i] << " ";
        }
        cout << endl;
        cout<<"---------------------"<<endl;
    }

    cout << endl;
    
     for (auto iter : F)
    {
        cout << "(" << iter.first << ", " << iter.second << ") ";
    }
};

int main()
{
    dijkstra();
    //정점 개수, 거리 배열, (저장할 맵 구조 F) 인데 다 전역변수로 날려버림 ㅋㅋㅋㅋ
}