#2. Perspective Transform (수동)
# 임의의 체커 보드 이미지에 대해 perspective transform을 적용하여 정방형으로 보드가 나오도록 변환하세요.
# 사용자로부터 네 모서리 정보를 마우스 클릭으로 입력 받으세요.
# 좌상단부터 시계방향으로 입력 받는다고 가정
# 보드 이외의 부분은 crop 하세요.

import cv2
import numpy as np

# 마우스 이벤트를 처리하는 콜백 함수
def select_point(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        param.append((x, y))

# 이미지를 로드합니다.
image = cv2.imread('checkerboard8_1.jpeg')

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

# 변환된 이미지를 출력합니다.
cv2.imshow('Transformed Image', result)
cv2.waitKey(0)
cv2.destroyAllWindows()
