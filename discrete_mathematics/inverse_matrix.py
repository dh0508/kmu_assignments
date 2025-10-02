"""
20243187 홍동형
이산수학 Report 1 : 역행렬을 구하는 프로그램을 작성하라.
"""

#  1. 행렬 입력 기능
def input_matrix():
    n = int(input("차수를 입력하시오"))
    matrix = []
    for i in range(n):
        print(f"{i+1}번 행을 입력하시오(공백으로 구분)")
        row = list(map(int, input().strip().split()))
        if len(row) != n:
            print("잘못 입력됨")
            exit()
        matrix.append(row)
    return n, matrix


#  2. 행렬식을 이용한 역행렬 계산 기능
def get_inverse_matrices_by_determinant(n, matrix):
    # 행렬식
    def determinant(matrix):
        if len(matrix) == 1:
            return matrix[0][0]
        if len(matrix) == 2:
            return matrix[0][0]*matrix[1][1] - matrix[0][1]*matrix[1][0]
        det = 0
        for col in range(len(matrix)):
            minor = [row[:col] + row[col+1:] for row in matrix[1:]]
            det += ((-1)**col) * matrix[0][col] * determinant(minor)
        return det

    # 여인수 행렬 생성
    def cofactor_matrix(matrix):
        cofactors = []
        for row in range(len(matrix)):
            cofactor_row = []
            for col in range(len(matrix)):
                minor = [r[:col] + r[col+1:] for i, r in enumerate(matrix) if i != row]
                cofactor_row.append(((-1)**(row+col)) * determinant(minor))
            cofactor_row = cofactor_row
            cofactors.append(cofactor_row)
        return cofactors

    det = determinant(matrix)
    if det == 0:
        print("역행렬이 존재하지 않습니다 (det=0).")
        return False

    # 수반행렬
    cof = cofactor_matrix(matrix)
    adj = [[cof[j][i] for j in range(n)] for i in range(n)]

    # 역행렬
    inverse = [[adj[i][j]/det for j in range(n)] for i in range(n)]
    return inverse




#  3. 가우스-조던 소거법(Gauss-Jordan elimination)을 이용한 역행렬 계산 기능
def get_inverse_matrices_by_Gauss_Jordan_dlimination(n, matrix):
    # 단위 행렬 생성
    identity = [[0 if i != j else 1 for j in range(n)] for i in range(n)]

    # 확장 행렬 생성
    aug_matrix = [row[:] + identity_row[:] for row, identity_row in zip(matrix, identity)]

    # 가우스-조던 소거
    for i in range(n):
        # 피벗 선택
        pivot = aug_matrix[i][i]
        if pivot == 0:
            # 피벗이 0이면 행 교환
            for k in range(i+1, n):
                if aug_matrix[k][i] != 0:
                    aug_matrix[i], aug_matrix[k] = aug_matrix[k], aug_matrix[i]
                    pivot = aug_matrix[i][i]
                    break
            else:
                print("역행렬이 존재하지 않습니다 (pivot=0).")
                return False

        # 피벗을 1로 만들기 위해 해당 행을 pivot으로 나누기
        aug_matrix[i] = [x / pivot for x in aug_matrix[i]]

        # 다른 행에서 피벗 열 제거
        for j in range(n):
            if j != i:
                factor = aug_matrix[j][i]
                aug_matrix[j] = [aj - factor * ai for aj, ai in zip(aug_matrix[j], aug_matrix[i])]

    # 역행렬은 [matrix | I]에서 오른쪽 부분
    inverse = [row[n:] for row in aug_matrix]
    return inverse



# 4. 결과 출력 기능
def print_matrix(matrix):
    if matrix:
        n = len(matrix)
        print("┌" + "        " * n + "┐")
        for i in range(n):
            print("|", end=" ")
            for j in range(n):
                print("%7.3f" % matrix[i][j], end=" ")
            print("|")
        print("└" + "        " * n + "┘")
    else:
        print("행렬 존재하지 않음")


# 4. 비교 기능
def compare(matrix1, matrix2):
    if matrix1 and matrix2:
        if len(matrix1) != len(matrix2):
            print("두 행렬은 다릅니다.")
            return
        is_equal = True
        for i in range(n):
            for j in range(n):
                if matrix1[i][j] != matrix2[i][j]:
                    is_equal = False
                    break
            if not is_equal:
                break

        if is_equal:
            print("두 행렬은 동일합니다.")
        else:
            print("두 행렬은 다릅니다.")


# 5. 추가기능 검산기능
def verify_inverse(matrix, inverse):
    if not matrix or not inverse:
        print("검산 불가 (역행렬이 존재하지 않음)")
        return

    n = len(matrix)
    # 행렬 곱하기
    product = [[sum(matrix[i][k] * inverse[k][j] for k in range(n)) for j in range(n)] for i in range(n)]

    print("\n=== 원래 행렬 × 역행렬 ===")
    print_matrix(product)


    # 단위행렬인지 확인 (부동소수 오차 고려)
    is_identity = True
    for i in range(n):
        for j in range(n):
            if i == j:
                if abs(product[i][j] - 1) > 1e-6:
                    is_identity = False
            else:
                if abs(product[i][j]) > 1e-6:
                    is_identity = False

    if is_identity:
        print("곱한 결과 단위행렬이 맞으므로 역행렬이 맞습니다.")
    else:
        print("곱한 결과 단위행렬이 아니므로 역행렬이 아닙니다.")



n, matrix = input_matrix()
print("입력받은 행렬")
print_matrix(matrix)

print("행렬식으로 구한 역행렬")
det_inv_mat = get_inverse_matrices_by_determinant(n, matrix)
print_matrix(det_inv_mat)

print("가우스 조던 소거법으로 구한 역행렬")
gauss_inv_mat = get_inverse_matrices_by_Gauss_Jordan_dlimination(n, matrix)
print_matrix(gauss_inv_mat)

print("비교 결과")
compare(det_inv_mat, gauss_inv_mat)

print("검산 결과")
verify_inverse(matrix, det_inv_mat)
