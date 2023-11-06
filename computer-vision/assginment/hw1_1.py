# 1. Checkerboard
# 임의의 체커 보드판 이미지에서 체커 보드판에 있는 칸의 수를 판별하여 
# 국제 룰과 영/미식 룰 중 어떤 규격의 판인지 판별하여 콘솔에 크기를 출력하세요.
# 예시)국제룰:10x10크기 10x10콘솔출력 
# 예시)영/미식룰:8x8크기 8x8콘솔출력

import cv2
import numpy as np



# 마우스 이벤트를 처리하는 콜백 함수
def select_point(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        param.append((x, y))

# 이미지를 로드합니다.
image = cv2.imread('checkerboard8_1.jpeg')

if image is None:
    print("failed")
    exit()

# 사용자가 선택한 점을 저장할 리스트를 생성합니다.
points = []

# 마우스 콜백 함수를 설정합니다.
cv2.namedWindow('image')
cv2.setMouseCallback('image', select_point, points)

# 사용자가 네 점을 선택할 때까지 기다립니다.
while len(points) < 4:
    cv2.imshow('image', image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()

# 사용자가 선택한 점을 기반으로 원근 변환을 수행합니다.
pts1 = np.float32(points)
pts2 = np.float32([[0, 0], [300, 0], [300, 300], [0, 300]])
matrix = cv2.getPerspectiveTransform(pts1, pts2)
result = cv2.warpPerspective(image, matrix, (300, 300))

# 변환된 이미지에서 체스보드 패턴의 크기를 판별합니다.
for pattern_size in [(10, 10), (8, 8)]:
    found, _ = cv2.findChessboardCorners(result, pattern_size)
    if found:
        print(f'{pattern_size[0]}x{pattern_size[1]} 크기')
        break
else:
    print('체스보드 패턴을 찾을 수 없습니다.')
