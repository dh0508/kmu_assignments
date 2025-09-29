import numpy as np

def fast_exponentiation(matrix, power):
    if power == 0:
        return np.eye(matrix.shape[0])
    if power == 1:
        return matrix

    result = np.eye(matrix.shape[0])
    base = matrix.copy()

    while power > 0:
        if power % 2 == 1:
            result = np.dot(result, base)
        base = np.dot(base, base)
        power //= 2

    return result

size = int(input("행렬의 크기를 입력하세요 (정수): "))
matrix = np.zeros((size, size))

print(f"{size}x{size} 행렬의 값을 입력하세요 (공백으로 구분)")
for i in range(size):
    row = input(f"{i + 1}번째 행의 값을 입력하세요 (예: 1 2 3): ").split()
    matrix[i] = list(map(float, row))

power_input = int(input("멱승을 할 것인지 입력하세요 (정수): "))

result = fast_exponentiation(matrix, power_input)

print(f"입력 행렬의 {power_input} 제곱 결과 (소수점 셋째자리까지 표시):")
for row in result:
    print(" ".join(map(lambda x: f"{float(round(x,3))}", row)))