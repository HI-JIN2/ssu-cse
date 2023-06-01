# #code by 유진


import time

# 소수 판별 함수
def is_prime(N):
    if N < 2: # 1은 소수가 아님
        return False
    for i in range(2, int(N**0.5)+1):
        if N % i == 0:
            return False
    return True


# 사용자로부터 입력 받기
N = int(input("Input the number of numbers to process: "))

        

nums = list(map(int, input("Input the numbers to be processed: ").split()))

# 실행 시간 측정 시작
start_time = time.time()

nums = list(set(nums)) # 중복 제거
nums.sort() # 정렬

for i in range(len(nums)-1):
    start, end = nums[i], nums[i+1]
    count = sum(is_prime(j) for j in range(start, end+1))
    print(f"Number of prime numbers between {start}, {end}: {count}")

# 실행 시간 측정 종료 및 출력
end_time = time.time()
duration = end_time - start_time
print(f"Total execution time using Python is {duration} seconds!")


