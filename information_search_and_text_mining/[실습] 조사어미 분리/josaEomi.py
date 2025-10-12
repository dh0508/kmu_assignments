'''
20243187 홍동형
정보검색과텍스트마이닝 과제

변경 요약:
1. 제거 대상 부호 리스트에 "?"와 "!"를 새로 포함.
2. 조사/어미 탐색 함수에서 성공 여부를 반환하도록 하여,
   분리 실패 시 메인 루프에서 메시지를 출력하게 함.
'''

import re

# 텍스트 파일에서 조사/어미 목록을 읽어 리스트로 반환
def read_list(path):
    result = []
    with open(path, 'r') as f:
        for line in f:
            result.append(line.strip())
    return result

# 문자열에서 불필요한 기호 제거
def clean_token(token):
    symbols = ['\n', '\r\n', '\'', '\"', '-', '=', '/', '.', '(', ')', '!', '?']
    for s in symbols:
        token = token.replace(s, '')
    return token

# 주어진 어절에 조사/어미가 포함되어 있는지 확인 후 분리
def split_josaeomi(word, cand_list, tag):
    found = False
    for cand in cand_list:
        regex = re.compile(r".+" + cand + r"$")
        if regex.match(word.strip()):
            stem = word.replace(cand, "", 1)
            print(f"\t{stem} + {cand}{tag}")
            found = True
    return found


# 조사와 어미 목록 불러오기
josa = read_list("./josa96.txt")
print("Loaded Josa:", josa)

eomi = read_list("./eomi152.txt")
print("Loaded Eomi:", eomi)

# 테스트 파일 읽기
with open("./test.txt", 'r') as f:
    for line in f:
        if not line or len(line) < 2:
            continue

        line = clean_token(line)
        words = line.split(' ')

        for w in words:
            print(w)
            has_josa = split_josaeomi(w, josa, "/조사")
            has_eomi = split_josaeomi(w, eomi, "/어미")

            if not (has_josa or has_eomi):
                print("\t==> 조사/어미 분리 실패")
