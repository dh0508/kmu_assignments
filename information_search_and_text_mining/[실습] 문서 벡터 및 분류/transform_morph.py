from pathlib import Path
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer

# 인풋 파일 경로
DIR = r"D:\SITE\●국민대\2학년 2학기\교과\정보검색과텍스트마이닝\과제\[실습] 문서 벡터 및 분류"
train_path = Path(DIR) / "train.txt"
test_path  = Path(DIR) / "test.txt"

train = pd.read_csv(train_path, encoding="utf-8")
test  = pd.read_csv(test_path,  encoding="utf-8")
assert {"review","label"}.issubset(train.columns) and {"review","label"}.issubset(test.columns)

X_train = train["review"].astype(str).str.strip().tolist()
X_test  = test["review"].astype(str).str.strip().tolist()

# 형태소 토크나이저
def get_morph_tokenizer():
    try:
        from konlpy.tag import Mecab
        mecab = Mecab()
        return lambda text: mecab.morphs(text)
    except Exception:
        try:
            from konlpy.tag import Okt
            okt = Okt()
            return lambda text: okt.morphs(text, stem=True)
        except Exception:
            return lambda text: text.split()

morph_tokenize = get_morph_tokenizer()

cv = CountVectorizer(
    analyzer=morph_tokenize,
    lowercase=False,
    token_pattern=None
)
Xtr_counts = cv.fit_transform(X_train)

tfidf = TfidfTransformer(sublinear_tf=True, smooth_idf=True, norm="l2")
Xtr_tfidf = tfidf.fit_transform(Xtr_counts) # train에서만 fit
Xte_tfidf = tfidf.transform(cv.transform(X_test)) # test는 transform만

# 희소행렬을 좌표형 TXT로
def save_sparse_txt(path, X):
    X = X.tocoo(copy=False)
    with open(path, "w", encoding="utf-8-sig") as f:
        f.write(f"# shape\t{X.shape[0]}\t{X.shape[1]}\n")
        f.write(f"# nnz\t{X.nnz}\n")
        f.write("# row\tcol\tvalue\n")
        for r, c, v in zip(X.row, X.col, X.data):
            f.write(f"{int(r)}\t{int(c)}\t{float(v):.6g}\n")

save_sparse_txt(Path(DIR) / "train_Tfidf_morph.txt", Xtr_tfidf)
save_sparse_txt(Path(DIR) / "test_Tfidf_morph.txt",  Xte_tfidf)

# feature 저장
with open(Path(DIR) / "feature_morph.txt", "w", encoding="utf-8-sig") as f:
    for tok in cv.get_feature_names_out():
        f.write(tok + "\n")

print("완료")