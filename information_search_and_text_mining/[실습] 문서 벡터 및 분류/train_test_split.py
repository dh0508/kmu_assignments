from pathlib import Path
import csv

# 인풋 파일 경로
dir_path = r"D:\SITE\●국민대\2학년 2학기\교과\정보검색과텍스트마이닝\과제\[실습] 문서 벡터 및 분류"
src_name = "NSMC_282K(ratings200K+kmuNP82K).txt"
src = Path(dir_path) / src_name

dst_train = Path(dir_path) / "train.txt"
dst_test  = Path(dir_path) / "test.txt"

def open_reader(path):
    f = open(path, "r", encoding="utf-8", newline="")
    reader = csv.reader(f)
    return f, reader

src_f, reader = open_reader(src)

with open(dst_train, "w", encoding="utf-8", newline="") as ftr, \
     open(dst_test,  "w", encoding="utf-8", newline="") as fte:

    wtr_train = csv.writer(ftr, quoting=csv.QUOTE_MINIMAL)
    wtr_test  = csv.writer(fte, quoting=csv.QUOTE_MINIMAL)

    header = next(reader, None)
    header_wo_id = header[1:]  # idx 제거
    wtr_train.writerow(header_wo_id)
    wtr_test.writerow(header_wo_id)

    n_train = n_test = n_skipped = 0

    # 데이터 행 1부터 카운트
    for i, row in enumerate(reader, start=1):
        row_wo_id = row[1:]

        # 10번째마다 test로
        if i % 10 == 0:
            wtr_test.writerow(row_wo_id)
            n_test += 1
        else:
            wtr_train.writerow(row_wo_id)
            n_train += 1

src_f.close()

print(f"train={n_train:,}  test={n_test:,}")
