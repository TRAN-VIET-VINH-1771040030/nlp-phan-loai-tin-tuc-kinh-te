"""Kiem tra yeu to NGUON BAO (source) trong bai toan phan loai nhom Kinh doanh.

Ly do: trong du lieu, 969/976 bai cua 'dantri' co nhan Kinh doanh (99.28%) va 969/1113 bai Kinh doanh la cua dantri.
Script tra loi: hieu nang tren dantri va tren cac nguon khac khac nhau the nao; mot bo phan loai CHI dua vao nguon
(source == dantri) dat bao nhieu; cac tu khoa dac trung co phai dac trung cua nguon khong.

Dung lai ket qua Lab 2 (khong lay du lieu moi):
    python kinhte_source_check.py
    python kinhte_source_check.py --lab2 D:\\Xu_li_NNTN\\lab2 --out D:\\Xu_li_NNTN\\project\\outputs
"""
import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC

TARGET = "Kinh doanh"
SRC = "dantri"


def read(p):
    return pd.read_csv(p, encoding="utf-8-sig")


def prf(y_true, y_pred):
    tp = int(((y_true) & (y_pred)).sum())
    fp = int((~y_true & y_pred).sum())
    fn = int((y_true & ~y_pred).sum())
    p = tp / (tp + fp) if tp + fp else float("nan")
    r = tp / (tp + fn) if tp + fn else float("nan")
    f = 2 * p * r / (p + r) if (p == p and r == r and p + r) else float("nan")
    return dict(TP=tp, FP=fp, FN=fn, precision=p, recall=r, F1=f)


def md_table(df, fmt="{:.4f}"):
    cols = list(df.columns)
    out = ["| " + " | ".join(map(str, cols)) + " |", "|" + "|".join(["---"] * len(cols)) + "|"]
    for _, r in df.iterrows():
        out.append("| " + " | ".join(
            ("" if pd.isna(r[c]) else fmt.format(r[c])) if isinstance(r[c], (float, np.floating)) else str(r[c])
            for c in cols) + " |")
    return "\n".join(out)


def top_terms(train, topn, mask=None):
    d = train if mask is None else train[mask]
    vec = TfidfVectorizer(ngram_range=(1, 2), min_df=3, max_df=0.9, sublinear_tf=True)
    X = vec.fit_transform(d["text"].astype(str))
    y = (d["label"] == TARGET).values
    clf = LinearSVC(C=1.0, class_weight="balanced", random_state=42).fit(X, y)
    terms = np.array(vec.get_feature_names_out())
    idx = np.argsort(-clf.coef_[0])[:topn]
    return list(terms[idx]), int(y.sum()), len(y)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lab2", default=r"D:\Xu_li_NNTN\lab2")
    ap.add_argument("--variant", default="vietnews_v0")
    ap.add_argument("--out", default=str(Path(__file__).resolve().parent / "outputs"))
    ap.add_argument("--topn", type=int, default=30)
    a = ap.parse_args()
    v = Path(a.lab2) / "outputs" / a.variant
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)

    pred = read(v / "predictions/test_predictions.csv")
    train = read(v / "splits/train.csv")
    val = read(v / "splits/val.csv")
    full = pd.concat([train, val, pred.drop(columns=["pred_label"])], ignore_index=True)
    md = ["# Kiem tra yeu to nguon bao (source) cho nhom Kinh doanh\n"]

    # ---- 1. Nguon x chuyen muc ----
    ct = pd.crosstab(full["source"], full["label"])
    ct["tong"] = ct.sum(axis=1)
    ct = ct.sort_values("tong", ascending=False)
    ct.to_csv(out / "source_by_label.csv", encoding="utf-8-sig")
    kd_total = int((full["label"] == TARGET).sum())
    kd_src = int(((full["label"] == TARGET) & (full["source"] == SRC)).sum())
    n_src = int((full["source"] == SRC).sum())
    md.append("## 1. Nhan Kinh doanh va nguon bao\n")
    md.append(f"- {SRC}: {kd_src}/{n_src} bai la Kinh doanh ({100 * kd_src / n_src:.2f}%)\n")
    md.append(f"- {kd_src}/{kd_total} bai Kinh doanh ({100 * kd_src / kd_total:.2f}%) den tu {SRC}\n\n")
    md.append(md_table(ct.reset_index(), "{:.0f}") + "\n")

    # ---- 2. Hieu nang tach theo nguon (test) ----
    t = pred.copy()
    yt = (t["label"] == TARGET).values
    yp = (t["pred_label"] == TARGET).values
    is_src = (t["source"] == SRC).values
    rows = []
    for name, m in [("Tat ca", np.ones(len(t), bool)), (f"Chi {SRC}", is_src), (f"Cac nguon khac (khong {SRC})", ~is_src)]:
        r = prf(yt[m], yp[m])
        r.update(nhom=name, so_bai_test=int(m.sum()), so_bai_KD_that=int(yt[m].sum()))
        rows.append(r)
    # bo phan loai chi dua vao nguon
    base = prf(yt, is_src)
    base.update(nhom=f"Baseline: doan Kinh doanh neu source == {SRC}", so_bai_test=len(t), so_bai_KD_that=int(yt.sum()))
    rows.append(base)
    res = pd.DataFrame(rows)[["nhom", "so_bai_test", "so_bai_KD_that", "TP", "FP", "FN", "precision", "recall", "F1"]]
    res.to_csv(out / "kinhdoanh_by_source_group.csv", index=False, encoding="utf-8-sig")
    md.append("\n## 2. Hieu nang lop Kinh doanh tren tap test, tach theo nguon\n")
    md.append(md_table(res) + "\n")

    # ---- 3. Tu khoa: toan bo train vs chi nguon khac ----
    kw_all, nkd_a, n_a = top_terms(train, a.topn)
    m_other = (train["source"] != SRC).values
    kw_oth, nkd_o, n_o = top_terms(train, a.topn, m_other)
    both = [k for k in kw_all if k in kw_oth]
    md.append(f"\n## 3. Tu khoa dac trung: tat ca nguon va chi cac nguon khong phai {SRC}\n")
    md.append(f"- Mo hinh A: toan bo train ({n_a} bai, {nkd_a} Kinh doanh). Mo hinh B: chi bai khong phai {SRC} ({n_o} bai, {nkd_o} Kinh doanh).\n")
    md.append(f"- So tu khoa trung nhau trong top {a.topn}: {len(both)}\n\n")
    md.append(md_table(pd.DataFrame({"top_A_tat_ca_nguon": kw_all, "top_B_khong_dantri": kw_oth}), "{:.0f}") + "\n")
    pd.DataFrame({"A_tat_ca": kw_all, "B_khong_dantri": kw_oth}).to_csv(out / "keywords_A_vs_B.csv", index=False, encoding="utf-8-sig")

    # ---- 4. Ty le bai chua tu khoa theo nhom ----
    vec = TfidfVectorizer(ngram_range=(1, 2), min_df=3, max_df=0.9, sublinear_tf=True)
    X = (vec.fit_transform(train["text"].astype(str)) > 0).astype(int)
    vocab = vec.vocabulary_
    g1 = ((train["label"] == TARGET) & (train["source"] == SRC)).values
    g2 = ((train["label"] == TARGET) & (train["source"] != SRC)).values
    g3 = ((train["label"] != TARGET) & (train["source"] != SRC)).values
    rows = []
    for k in kw_all:
        j = vocab.get(k)
        if j is None:
            continue
        col = np.asarray(X[:, j].todense()).ravel()
        rows.append({"tu_khoa": k, f"KD & {SRC} (%)": 100 * col[g1].mean() if g1.any() else np.nan,
                     f"KD & khac {SRC} (%)": 100 * col[g2].mean() if g2.any() else np.nan,
                     f"khong KD & khac {SRC} (%)": 100 * col[g3].mean() if g3.any() else np.nan})
    kdf = pd.DataFrame(rows)
    kdf.to_csv(out / "keyword_share_by_group.csv", index=False, encoding="utf-8-sig")
    md.append(f"\n## 4. Ty le bai chua tu khoa (train) theo nhom\n")
    md.append(f"So bai: KD & {SRC} = {int(g1.sum())}; KD & khac {SRC} = {int(g2.sum())}; khong KD & khac {SRC} = {int(g3.sum())}\n\n")
    md.append(md_table(kdf, "{:.1f}") + "\n")

    (out / "kinhte_source_check.md").write_text("\n".join(md), encoding="utf-8")
    print(res.to_string(index=False))
    print(f"\n{SRC}: {kd_src}/{n_src} bai la Kinh doanh; {kd_src}/{kd_total} bai Kinh doanh den tu {SRC}")
    print(f"Tu khoa trung nhau (A va B) trong top {a.topn}: {len(both)}")
    print("Top B (khong dantri):", ", ".join(kw_oth[:15]))
    print("Ghi vao:", out)


if __name__ == "__main__":
    main()
