import java.util.*;

public class homework1 {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        // 입력 받기
        int N = 0;

        System.out.print("Input the number of numbers to process : ");
        N = sc.nextInt();

        int[] arr = new int[N];
        System.out.print("Input the numbers to be processed: ");
        for (int i = 0; i < N; i++) {
            arr[i] = sc.nextInt();
        }
        long start = System.nanoTime();
        // 중복 제거
        arr = Arrays.stream(arr).distinct().toArray();

        // 정렬
        Arrays.sort(arr);

        // 소수 개수 계산
        
        for (int i = 0; i < arr.length - 1; i++) {
            int startNum = arr[i];
            int endNum = arr[i + 1];
            int count = 0;
            for (int j = startNum; j <= endNum; j++) {
                if (isPrime(j)) {
                    count++;
                }
            }
            System.out.printf("Number of prime numbers between %d, %d: %d\n", startNum, endNum, count);
        }
        long end = System.nanoTime();
        double executionTime = (end - start) / 1_000_000_000.0;
        System.out.printf("Total execution time using Java is %f seconds!\n", executionTime);
    }

    // 소수 판별 함수
    public static boolean isPrime(int n) {
        if (n < 2) {
            return false;
        }
        for (int i = 2; i <= Math.sqrt(n); i++) {
            if (n % i == 0) {
                return false;
            }
        }
        return true;
    }
}