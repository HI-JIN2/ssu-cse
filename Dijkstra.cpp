#include <iostream>
#include <map>
using namespace std;
#define INF 999
#define n 5
map<int, int> F;
int W[6][6] = {
    {0, 0, 0, 0, 0, 0},
    {0, 0, 7, 4, 6, 1},
    {0, INF, 0, INF, INF, INF},
    {0, INF, 2, 0, 5, INF},
    {0, INF, 3, INF, 0, INF},
    {0, INF, INF, INF, 1, 0}};

void dijkstra()
{
    int i; //인덱스
    int vnear, e;
    int touch[n + 1];
    int length[n + 1];
    /*
        for(int i=0;i<n+1;i++)
            touch[i]=1;

        for(int i=0;i<n+1;i++)
            length[i]=W[1][i]; //1
    */

    for (int i = 0; i <= n; i++)
    {
        touch[i] = 1; // start vertex
        length[i] = W[1][i];
    }

    for (int k=0;k<n-1;k++) //repeat n-1번
    {
        int min = INF;
        for (int i = 2; i <= n; i++)
        {
            if (0 <= length[i] && length[i] <= min)
            {
                min = length[i];
                vnear = i;
            }
        }
        // e = 엣지 프롬 벌텍스 인덱스 바이 touch[vnear] to vertex index by vnear
        // e를 F 배열에 넣기

        cout << "min=" << min << " vnear=" << vnear << endl;
        F.insert({touch[vnear], vnear});

        for (int i = 0 ; i <= n; i++)
        {
            if (length[vnear] + W[vnear][i] < length[i])
            {
                length[i] = length[vnear] + W[vnear][i]; //여기서 잘못 됨
                cout<<length[i]<<" = "<< length[vnear]<< " + " <<W[vnear][i]<<endl; 
                //length[4]=2, touch[4]=5

                touch[i] = vnear;
                cout << "length[" << i << "]=" << length[i] << " touch[" << i << "]=" << vnear << endl;
            }
            length[vnear] = -1;
        }
    }
    for (int i = 0; i <= n; i++)
    {
        cout << touch[i] << " ";
    }
    cout << endl;
    for (int i = 0; i <= n; i++)
    {
        cout << length[i] << " ";
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