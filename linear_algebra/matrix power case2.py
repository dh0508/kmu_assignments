import numpy as np

def get_characteristic_polynomial(A):
    return np.poly(A)

def cayley_hamilton_power(A, m):
    n = A.shape[0]
    coeffs = get_characteristic_polynomial(A)
    coeffs = -coeffs[1:]

    powers = [np.eye(n), A.copy()]
    for i in range(2, n):
        powers.append(A @ powers[-1])

    if m < n:
        return powers[m]
    else:
        for k in range(n, m + 1):
            Ak = np.zeros((n, n))
            for i in range(1, n + 1):
                Ak += coeffs[i - 1] * powers[k - i]
            powers.append(Ak)
        return powers[m]


size = int(input("행렬의 크기를 입력하세요 (정수): "))
matrix = np.zeros((size, size))

print(f"{size}x{size} 행렬의 값을 입력하세요 (공백으로 구분)")
for i in range(size):
    row = input(f"{i + 1}번째 행의 값을 입력하세요 (예: 1 2 3): ").split()
    matrix[i] = list(map(float, row))

power_input = int(input("멱승을 할 것인지 입력하세요 (정수): "))
result = cayley_hamilton_power(matrix, power_input)

print(f"입력 행렬의 {power_input} 제곱 결과 (소수점 셋째자리까지 표시):")
for row in result:
    print(" ".join(map(lambda x: f"{float(round(x,3))}", row)))