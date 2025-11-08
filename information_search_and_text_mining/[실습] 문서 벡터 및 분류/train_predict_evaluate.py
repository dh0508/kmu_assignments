from pathlib import Path
import pandas as pd
from scipy import sparse
import time

# 분류기들
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier

from sklearn.metrics import accuracy_score, classification_report

# 인풋 파일 경로
DIR = r"D:\SITE\●국민대\2학년 2학기\교과\정보검색과텍스트마이닝\과제\[실습] 문서 벡터 및 분류"
BIGRAM_TRAIN = Path(DIR) / "train_Tfidf_bigram.txt"
BIGRAM_TEST  = Path(DIR) / "test_Tfidf_bigram.txt"
MORPH_TRAIN  = Path(DIR) / "train_Tfidf_morph.txt"
MORPH_TEST   = Path(DIR) / "test_Tfidf_morph.txt"
TRAIN_LBL = Path(DIR) / "train.txt"
TEST_LBL  = Path(DIR) / "test.txt"

# 좌표형 TXT --> CSR 로더
def load_sparse_txt(path):
    with open(path, "r", encoding="utf-8") as f:
        shape_line = f.readline().strip().split("\t")
        _ = f.readline(); _ = f.readline()
        n_rows, n_cols = int(shape_line[1]), int(shape_line[2])
        rows, cols, vals = [], [], []
        for line in f:
            r, c, v = line.strip().split("\t")
            rows.append(int(r)); cols.append(int(c)); vals.append(float(v))
    return sparse.coo_matrix((vals, (rows, cols)), shape=(n_rows, n_cols)).tocsr()

#토큰 방식, 모델 선택
print("토큰 방식을 선택해 주세요.")
token_key = int(input("번호를 입력하세요 (1: 음절 bigram, 2: 형태소)"))

print("모델을 선택해 주세요.")
model_key = int(input("번호를 입력하세요 (1: SVM, 2: NaiveBayes, 3: DecisionTree, 4: RandomForest, 5: MLP)"))

model_map = {
    1: "SVM",
    2: "NaiveBayes",
    3: "DecisionTree",
    4: "RandomForest",
    5: "MLP",
}
token_map = {
    1: "bigram",
    2: "morph",
}
model_name = model_map[model_key]
token_name = token_map[token_key]

# 토큰 방식에 맞는 데이터 로드
if token_name == "bigram":
    train_mat = BIGRAM_TRAIN
    test_mat  = BIGRAM_TEST
else:
    train_mat = MORPH_TRAIN
    test_mat  = MORPH_TEST

X_train = load_sparse_txt(train_mat)
X_test  = load_sparse_txt(test_mat)

# 라벨 로드
y_train = pd.read_csv(TRAIN_LBL, encoding="utf-8")["label"].astype(int).values
y_test  = pd.read_csv(TEST_LBL,  encoding="utf-8")["label"].astype(int).values

# 입력에 맞는 모델 로드
def make_model(name: str):
    if name == "SVM":
        return LinearSVC(C=1.0, dual=True, max_iter=5000, random_state=42)
    if name == "NaiveBayes":
        return MultinomialNB()
    if name == "DecisionTree":
        return DecisionTreeClassifier(max_depth=None, random_state=42)
    if name == "RandomForest":
        return RandomForestClassifier(
            n_estimators=200, max_depth=None, n_jobs=-1, random_state=42
        )
    if name == "MLP":
        return MLPClassifier(
            hidden_layer_sizes=(128,),
            activation="relu",
            solver="adam",
            alpha=1e-4,
            batch_size=4096,
            learning_rate_init=5e-3,
            early_stopping=True,
            n_iter_no_change=3,
            max_iter=35,
            random_state=42,
            verbose=False,
        )

clf = make_model(model_name)

# 학습
print(f"[정보] 모델={model_name}, 토큰화={token_name}")
t0 = time.perf_counter()
clf.fit(X_train, y_train)
t1 = time.perf_counter()
print(f"학습 시간: {t1-t0:.3f}초")

# 예측, 평가
y_pred = clf.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print(f"Accuracy: {acc:.5f}")

print(classification_report(y_test, y_pred, digits=4))
