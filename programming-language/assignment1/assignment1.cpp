// code by 유진

#include <iostream>
#include <vector>
#include <algorithm>
#include <cmath>
#include <ctime>

using namespace std;

int primeArr(int n)
{
    vector<bool> arr(n + 1);
    int cnt = 0;

    arr[1] = true; // 1은 소수가 아니므로 true

    for (int i = 2; i <= sqrt(n); i++)
    {
        if (arr[i])
            continue;                       // 이미 체크 됐으면 continue;
        for (int j = i + i; j <= n; j += i) // i를 제외한 i의 배수들은 소수가 아니다.
            arr[j] = true;
    }

    // 소수 출력
    for (int i = 2; i <= n; i++)
    {
        if (!arr[i])
        {
            // cout<< i << endl;
            cnt++;
        }
    }
    return cnt;
}

int main()
{
    clock_t start, finish;
    double duration;

    int N;
    cout << "Input the number of numbers to process: ";
    cin >> N;

    cout << "Input the numbers to be processed: " << endl;
    int arr[30];
    for (int i = 0; i < N; i++)
        cin >> arr[i];

    start = clock();
    // 정렬
    sort(arr, arr + N);

    // 중복제거
    int arr2[30];
    int i, n = 1;
    arr2[0] = arr[0];

    int cnt = 0;

    for (int i = 1; i < N; i++)
        if (arr[i] != arr2[n - 1])
            arr2[n++] = arr[i];
    for (int i = 0; i < n; i++)
    {
        // printf("%d ", arr2[i]);
        cnt++;
    }
    printf("\n");

    // 에라토스테네스의 체
    // 가장 큰수로 소수 판별이 된 배열을 만들어오기
    primeArr(arr2[cnt]);

    for (int i = 0; i < cnt - 1; i++)
        cout << "Number of prime numbers between " << arr2[i] << "," << arr2[i + 1] << ": " << primeArr(arr2[i + 1]) - primeArr(arr2[i]) << endl;

    finish = clock();

    duration = (double)(finish - start) / CLOCKS_PER_SEC;
    cout << "Total execution time using C++ is " << duration << " seconds!";

    return 0;
}