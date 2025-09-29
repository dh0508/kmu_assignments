# 행렬 입력 step1
equation_cnt = int(input("방정식의 수를 입력하세요 (정수): "))
matrix = [list(map(float, input("방정식의 계수를 입력하세요 (ax + by = c인 경우 a b c 형식으로 입력): ").strip().split())) for _ in range(equation_cnt)]
augmented_matrix = [[matrix[i].pop(-1)] for i in range(equation_cnt)]


# 가역 판별 step2
def invertible_matrix_judgeent(matrix):  # 행렬이 가역인지 판별

    def square_matrix(matrix):  # 정방행렬인지 판별
        for i in range(equation_cnt):
            if equation_cnt != len(matrix[i]):
                return False
        return True

    def determinant(matrix):  # 행렬식을 구하는 함수
        a = 0
        if len(matrix) == 2:
            return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
        else:
            for i in range(len(matrix)):
                if i % 2 == 0:
                    a += matrix[0][i] * determinant(
                        [[value for index, value in enumerate(matrix[j]) if index != i] for j in range(1, len(matrix))])
                else:
                    a -= matrix[0][i] * determinant(
                        [[value for index, value in enumerate(matrix[j]) if index != i] for j in range(1, len(matrix))])
            return a

    if square_matrix(matrix):  # 정방행렬이고
        if determinant(matrix) != 0:  # 행렬식이 0이 아니면
            return True  # 가역행렬
    return False  # 비가역행렬


def matrix_multiplication(arr1, arr2):  # 행렬의 곱셈
    answer = []
    m, n, r = len(arr1), len(arr1[0]), len(arr2[0])

    for i in range(m):
        arr = arr1[i]
        result = []
        for j in range(r):
            hap = 0
            for k in range(n):
                hap += arr[k] * arr2[k][j]
            result.append(hap)
        answer.append(result)

    return answer


def use_invertible_matrix(matrix):  # 역행렬을 이용해 해 구하기 step3

    def change_inverse_matrix(matrix):
        n = len(matrix)
        identity = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        augmented = [matrix[i] + identity[i] for i in range(n)]

        for i in range(n):
            diag_value = augmented[i][i]

            if abs(diag_value) < 1e-10:  # 피벗이 0이면 다른 행과 교환(zerodivision 해결을 위함)
                for j in range(i + 1, n):
                    if abs(augmented[j][i]) > 1e-10:  # 0이 아닌 값을 찾으면
                        augmented[i], augmented[j] = augmented[j], augmented[i] # 두 행을 교환
                        diag_value = augmented[i][i]
                        break
                else:
                    print("가역행렬이 아니므로 역행렬을 구할 수 없습니다.")
                    return None  # 역행렬을 구할 수 없는 경우

            # 피벗을 1로
            for k in range(2 * n):
                augmented[i][k] /= diag_value

            # 다른 행의 해당 열을 0으로
            for j in range(n):
                if j != i:
                    factor = augmented[j][i]
                    for k in range(2 * n):
                        augmented[j][k] -= factor * augmented[i][k]

        # 역행렬 부분 찾아서 리턴
        inverse = [row[n:] for row in augmented]
        return inverse

    return matrix_multiplication(change_inverse_matrix(matrix), augmented_matrix)


def gauss_jordan_elimination(matrix, b):
    n = len(matrix)  # 방정식의 수
    m = len(matrix[0])  # 미지수의 수

    # 첨가행렬 (A|b) 생성
    augmented = [matrix[i] + [b[i][0]] for i in range(n)]

    # 가우스 조던 소거법
    for i in range(n):
        # 피벗이 0이면 다른 행과 교환(zerodivision 해결을 위함 위와 동일)
        if abs(augmented[i][i]) < 1e-10:
            for j in range(i + 1, n):
                if abs(augmented[j][i]) > 1e-10:
                    augmented[i], augmented[j] = augmented[j], augmented[i]
                    break

        if abs(augmented[i][i]) < 1e-10:
            continue

        # 피벗을 1로
        pivot = augmented[i][i]
        for k in range(m + 1):
            augmented[i][k] /= pivot

        # 다른 행의 해당 열을 0으로
        for j in range(n):
            if j != i:
                factor = augmented[j][i]
                for k in range(m + 1):
                    augmented[j][k] -= factor * augmented[i][k]

    # 해가 없는지 판별
    for i in range(n):
        if all(abs(augmented[i][j]) < 1e-10 for j in range(m)) and abs(augmented[i][-1]) > 1e-10:
            print("해가 없음")
            return

    # 자유변수 및 해 구하기
    solution = [0] * m  # 기본 해(0으로 초기화)
    free_variables = []  # 자유변수 리스트

    # 자유변수 여부 확인
    pivot_positions = [-1] * m  # 각 열에 대한 피벗 위치(-1: 피벗 없음)
    for i in range(n):
        for j in range(m):
            if abs(augmented[i][j]) > 1e-10:
                pivot_positions[j] = i
                break

    for j in range(m):
        if pivot_positions[j] == -1:  # 자유변수
            free_variables.append(j)

    # 해를 구하기
    for i in range(n):
        pivot_col = next((j for j in range(m) if abs(augmented[i][j]) > 1e-10), None)
        if pivot_col is not None:
            solution[pivot_col] = augmented[i][-1]

    # 결과 출력
    results = []
    for j in range(m):
        if j in free_variables:
            expr = f"x{j + 1} = t{free_variables.index(j) + 1}"
        else:
            expr = f"x{j + 1} = {round(solution[j], 3)}"
            for free_var in free_variables:
                coeff = -augmented[pivot_positions[j]][free_var] if pivot_positions[j] != -1 else 0
                if abs(coeff) > 1e-10:
                    expr += f" + {round(coeff, 3)}t{free_variables.index(free_var) + 1}"
        results.append(expr)

    for result in results:
        print(result)



if invertible_matrix_judgeent(matrix):  # 가역행렬이면
    for i, sublist in enumerate(use_invertible_matrix(matrix)):  # 출력 형식 처리
        value = round(sublist[0], 3)
        print(f"x{i + 1} = {value}")

else: # 아니면 가우스 조던 소거법
    gauss_jordan_elimination(matrix, augmented_matrix) # 출력 형식도 함수 내에서 처리