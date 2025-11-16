"""
20243187 홍동형
이산수학 Report 2
"""

# 1. 관계 행렬 입력 기능
def input_relation_matrix():
    print("각 행을 0과 1로 5개씩 공백으로 구분하여 입력하시오.")
    n = 5
    matrix = []
    for i in range(n):
        print(f"{i+1}번 행을 입력하시오 (예: 1 0 1 0 1)")
        row = list(map(int, input().strip().split()))
        matrix.append(row)
    return n, matrix

# 2. 동치 관계 판별 기능
# 반사 핀별
def is_reflexive(n, matrix):
    for i in range(n):
        if matrix[i][i] != 1:
            return False
    return True

# 대칭 판별
def is_symmetric(n, matrix):
    for i in range(n):
        for j in range(n):
            if matrix[i][j] != matrix[j][i]:
                return False
    return True

# 추이 판별
def is_transitive(n, matrix):
    for i in range(n):
        for j in range(n):
            if matrix[i][j] == 1:
                for k in range(n):
                    if matrix[j][k] == 1 and matrix[i][k] == 0:
                        return False
    return True

# 전체 동치 판단 및 출력
def is_equivalence(n, matrix, print_tf):
    reflexive = is_reflexive(n, matrix)
    symmetric = is_symmetric(n, matrix)
    transitive = is_transitive(n, matrix)

    if print_tf:
        if reflexive:
            print("반사 관계입니다.")
        else:
            print("반사 관계가 아닙니다.")

        if symmetric:
            print("대칭 관계입니다.")
        else:
            print("대칭 관계가 아닙니다.")

        if transitive:
            print("추이 관계입니다.")
        else:
            print("추이 관계가 아닙니다.")

        if reflexive and symmetric and transitive:
            print("이 관계는 동치 관계입니다.")
        else:
            print("이 관계는 동치 관계가 아님니다.")

    return reflexive and symmetric and transitive


# 3. 동치 관계일 경우 동치류 출력 기능
# 동치류 구하기
def get_equivalence_classes(n, matrix):
    classes = []

    for i in range(n):
        eq_class = []
        for j in range(n):
            if matrix[i][j] == 1:
                eq_class.append(j + 1)

        classes.append(eq_class)

    return classes


# 출력하기
def print_equivalence_classes(n, matrix):
    if not is_equivalence(n, matrix, True):
        print("동치관계가 아니므로 동치류를 구할 수 없습니다.")
        return

    classes = get_equivalence_classes(n, matrix)

    print("--- 각 원소에 대한 동치류 출력 ---")
    for i in range(n):
        eq_class = classes[i]
        print(f"{i+1} 의 동치류 : {{", end="")
        for j, val in enumerate(eq_class):
            print(val, end="")
            if j != len(eq_class) - 1:
                print(", ", end="")
        print("}")


# 4. 폐포 구현 기능
# 관계 행렬 출력
def print_relation_matrix(n, matrix):
    print("관계 행렬:")
    for i in range(n):
        for j in range(n):
            print(matrix[i][j], end=" ")
        print()
    print()

# 반사 폐포 함수
def reflexive_closure(n, matrix):
    new_matrix = [row[:] for row in matrix]
    for i in range(n):
        new_matrix[i][i] = 1
    return new_matrix

# 대칭 폐포 함수
def symmetric_closure(n, matrix):
    new_matrix = [row[:] for row in matrix]
    for i in range(n):
        for j in range(n):
            if matrix[i][j] == 1:
                new_matrix[i][j] = 1
                new_matrix[j][i] = 1
    return new_matrix

# 추이 폐포 함수
def transitive_closure(n, matrix):
    new_matrix = [row[:] for row in matrix]
    for k in range(n):
        for i in range(n):
            if new_matrix[i][k] == 1:
                for j in range(n):
                    if new_matrix[k][j] == 1:
                        new_matrix[i][j] = 1
    return new_matrix

def process_closures(n, matrix):

    reflexive = is_reflexive(n, matrix)
    symmetric = is_symmetric(n, matrix)
    transitive = is_transitive(n, matrix)

    print("--- 반사 폐포 ---")
    if reflexive:
        print("이미 반사 관계임")
    else:
        print("반사 폐포 변환 전 관계 행렬:")
        print_relation_matrix(n, matrix)

        ref_matrix = reflexive_closure(n, matrix)

        print("반사 폐포 변환 후 관계 행렬:")
        print_relation_matrix(n, ref_matrix)

        print("반사 폐포 변환 후 동치 관계 판별 및 동치류:")
        print_equivalence_classes(n, ref_matrix)

    print("--- 대칭 폐포 ---")
    if symmetric:
        print("이미 대칭 관계임")
    else:
        print("대칭 폐포 변환 전 관계 행렬:")
        print_relation_matrix(n, matrix)

        sym_matrix = symmetric_closure(n, matrix)

        print("대칭 폐포 변환 후 관계 행렬:")
        print_relation_matrix(n, sym_matrix)

        print("대칭 폐포 변환 후 동치 관계 판별 및 동치류:")
        print_equivalence_classes(n, sym_matrix)

    print("--- 추이 폐포 ---")
    if transitive:
        print("이미 추이 관계임")
    else:
        print("추이 폐포 변환 전 관계 행렬:")
        print_relation_matrix(n, matrix)

        trans_matrix = transitive_closure(n, matrix)

        print("추이 폐포 변환 후 관계 행렬:")
        print_relation_matrix(n, trans_matrix)

        print("추이 폐포 변환 후 동치 관계 판별 및 동치류:")
        print_equivalence_classes(n, trans_matrix)


# 5. 추가 기능 : 동치류로 관계를 재구성하여 검산
# 동치류 중복 없이 구하기
def get_unique_equivalence_classes(n, matrix):
    all_classes = get_equivalence_classes(n, matrix)

    classes = []
    for i in all_classes:
        eq_class_sorted = tuple(sorted(i))
        if eq_class_sorted not in classes:
            classes.append(eq_class_sorted)

    unique_classes = [list(i) for i in classes]
    return unique_classes


# 동치류로 관계 행렬 재구성
def build_relation_from_classes(n, classes):
    new_matrix = [[0 for _ in range(n)] for _ in range(n)]

    for eq_class in classes:
        for i in eq_class:
            for j in eq_class:
                new_matrix[i - 1][j - 1] = 1

    return new_matrix


# 두 관계 행렬 비교
def compare_relations(n, matrix1, matrix2):
    same = True
    for i in range(n):
        for j in range(n):
            if matrix1[i][j] != matrix2[i][j]:
                same = False
                break
        if not same:
            break

    if same:
        print("재구성한 관계 행렬이 원래 관계 행렬과 동일합니다.")
    else:
        print("재구성한 관계 행렬이 원래 관계 행렬과 다릅니다.")


# 전체 검산 기능
def verify_equivalence_classes(n, matrix):
    print("--- 추가 기능 : 동치류 검산 기능 ---")

    if not is_equivalence(n, matrix, False):
        print("이 관계는 동치 관계가 아니므로 동치류 검산을 수행할 수 없습니다.")
        return

    classes = get_unique_equivalence_classes(n, matrix)
    print("서로 다른 동치류들:")
    for idx, eq_class in enumerate(classes, start=1):
        print(f"클래스 {idx} : {{", end="")
        for i, val in enumerate(eq_class):
            print(val, end="")
            if i != len(eq_class) - 1:
                print(", ", end="")
        print("}")

    rebuilt = build_relation_from_classes(n, classes)
    print()
    print("동치류로부터 재구성한 관계 행렬:")
    for i in range(n):
        for j in range(n):
            print(rebuilt[i][j], end=" ")
        print()

    compare_relations(n, matrix, rebuilt)



n, matrix = input_relation_matrix()
# print_relation_matrix(n, matrix)
# is_equivalence(n, matrix, True)
# print_equivalence_classes(n, matrix)
# process_closures(n, matrix)
# verify_equivalence_classes(n, matrix)
