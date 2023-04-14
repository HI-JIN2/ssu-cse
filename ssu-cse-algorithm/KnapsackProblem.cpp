#include <iostream>
#include <vector>
#include <string>
#define n 4
using namespace std;

int W = 16;
int w[n + 1] = {0, 2, 5, 10, 5};
int p[n + 1] = {0, 40, 30, 50, 10};
int maxprofit = 0;
int numbest = 0;
int bestset[n + 1];
int include[n + 1];

bool promising(int i, int profit, int weight)
{
    int j, k;
    int totweight; //지금까지의 무게합+앞으로 넣을 수 있는 무게합
    float bound;   //지금까지 profit합+앞으로 더해질 profit+partial profit
    if (weight >= W)
        return false;
    else
    {
        j = i + 1;
        bound = profit;
        totweight = weight;
        while ((j <= n) && (totweight + w[j] <= W))
        {
            totweight = totweight + w[j];
            bound = bound + p[j];
            j++;
        }
        k = j;
        if (k <= n)
            bound = bound + (W - totweight) * p[k] / w[k];
        return bound > maxprofit;
    }
}

void knapsack(int i, int profit, int weight)
{

    if (weight <= W && profit > maxprofit) // best so far
    {
        maxprofit = profit;
        numbest = i;
        for (int j = 1; j <= numbest; j++)
            bestset[j] = include[j];
    }
    if (promising(i, profit, weight))
    {
        include[i + 1] = 1; // Include w[i+1]
        knapsack(i + 1, profit + p[i + 1], weight + w[i + 1]);
        include[i + 1] = 0; // Not include w[i+1]
        knapsack(i + 1, profit, weight);
    }
}

int main()
{

    knapsack(0, 0, 0);

    for (int i = 1; i <= numbest; i++)
    {
        cout << bestset[i];
    }
}