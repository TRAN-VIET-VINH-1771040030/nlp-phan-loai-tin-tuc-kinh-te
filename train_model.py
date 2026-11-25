"""Huấn luyện mô hình TF-IDF + LinearSVM và lưu ra model/model.joblib cho app Streamlit.

Chạy (từ thư mục BTL):
    python train_model.py
Script in Accuracy / Macro-F1 trên tập test và so với pred_label của Lab 2 để biết đã khớp chưa.
"""
import argparse
from pathlib import Path

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, f1_score
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC

# ---- THAM SỐ: sửa ở đây khi có cấu hình đúng của Lab 2 ----------------------
# Cấu hình hiện tại là cấu hình GẦN NHẤT tìm được (Acc 0.8716, Macro-F1 0.7419,
# lệch 9/327 dự đoán so với Lab 2), chưa phải bản gốc.
TFIDF_PARAMS = dict(ngram_range=(1, 2), min_df=1, sublinear_tf=False)
SVM_PARAMS = dict(C=5.0, random_state=42)
# -----------------------------------------------------------------------------

ROOT = Path(__file__).resolve().parent


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", default=ROOT / "du_lieu_lab2")
    ap.add_argument("--out", default=ROOT / "model" / "model.joblib")
    args = ap.parse_args()
    data = Path(args.data_dir)

    train = pd.read_csv(data / "splits" / "train.csv")
    test = pd.read_csv(data / "predictions" / "test_predictions.csv")

    pipe = Pipeline([
        ("tfidf", TfidfVectorizer(**TFIDF_PARAMS)),
        ("svm", LinearSVC(**SVM_PARAMS)),
    ]).fit(train["text"], train["label"])

    pred = pipe.predict(test["text"])
    print(f"Accuracy : {accuracy_score(test['label'], pred):.4f}  (báo cáo: 0.8716)")
    print(f"Macro-F1 : {f1_score(test['label'], pred, average='macro'):.4f}  (báo cáo: 0.7421)")
    print(f"Lệch so với pred_label của Lab 2: {(pred != test['pred_label']).sum()}/{len(test)} bài")

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipe, out)
    print("Đã lưu:", out)


if __name__ == "__main__":
    main()
