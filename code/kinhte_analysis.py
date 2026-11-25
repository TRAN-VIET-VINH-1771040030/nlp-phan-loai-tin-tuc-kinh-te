"""Phan tich nhom tin KINH TE ("Kinh doanh") tren bo VietNewsSense (UVN-1), dung ket qua Lab 2.

Khong thu thap du lieu moi. Dung lai:
  - lab2/outputs/<variant>/predictions/test_predictions.csv  (cot: id,text,label,source,url,title,publish_date,pred_label)
  - lab2/outputs/<variant>/splits/{train,val}.csv            (cung schema, khong co pred_label)

Chay (mac dinh variant = vietnews_v0, la ban tot nhat cua Lab 2):
    python kinhte_analysis.py
    python kinhte_analysis.py --lab2 D:\\Xu_li_NNTN\\lab2 --out D:\\Xu_li_NNTN\\project\\outputs

Dau ra trong thu muc --out: cac file CSV, hinh PNG va kinhte_summary.md (moi so deu tinh tu du lieu that).
"""
import argparse
import sys
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_recall_fscore_support
from sklearn.svm import LinearSVC

TARGET = "Kinh doanh"


def read(path):
    return pd.read_csv(path, encoding="utf-8-sig")


def md_table(df, floatfmt="{:.4f}"):
    cols = list(df.columns)
    out = ["| " + " | ".join(str(c) for c in cols) + " |", "|" + "|".join(["---"] * len(cols)) + "|"]
    for _, r in df.iterrows():
        cells = []
        for c in cols:
            v = r[c]
            if isinstance(v, (float, np.floating)):
                cells.append("" if pd.isna(v) else floatfmt.format(v))
            else:
                cells.append(str(v))
        out.append("| " + " | ".join(cells) + " |")
    return "\n".join(out)


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
    full = pd.concat([train.assign(split="train"), val.assign(split="val"),
                      pred.drop(columns=["pred_label"]).assign(split="test")], ignore_index=True)
    md = []
    md.append(f"# Phan tich nhom tin Kinh te (lop \"{TARGET}\")\n")
    md.append(f"Nguon: `{v}` | train={len(train)}, val={len(val)}, test={len(pred)}, tong={len(full)}\n")

    # ---------- 1. Hieu nang tung lop ----------
    labels = list(pred["label"].value_counts().index)
    p, r, f, s = precision_recall_fscore_support(pred["label"], pred["pred_label"], labels=labels, zero_division=0)
    per = pd.DataFrame({"lop": labels, "precision": p, "recall": r, "f1": f, "support_test": s})
    per.to_csv(out / "per_class_metrics.csv", index=False, encoding="utf-8-sig")
    acc = accuracy_score(pred["label"], pred["pred_label"])
    mf1 = f1_score(pred["label"], pred["pred_label"], average="macro", labels=labels, zero_division=0)
    md.append("## 1. Hieu nang phan loai (tap test)\n")
    md.append(f"Accuracy = {acc:.4f}; Macro-F1 = {mf1:.4f} (Lab 2 bao cao V0: 0.8716 / 0.7421; neu khac thi kiem tra --variant)\n")
    md.append(md_table(per) + "\n")
    kd = per[per["lop"] == TARGET].iloc[0]
    md.append(f"\nLop {TARGET}: precision={kd['precision']:.4f}, recall={kd['recall']:.4f}, F1={kd['f1']:.4f}, support={int(kd['support_test'])}\n")

    # ---------- 2. Confusion matrix ----------
    cm = confusion_matrix(pred["label"], pred["pred_label"], labels=labels)
    cmdf = pd.DataFrame(cm, index=[f"that:{l}" for l in labels], columns=[f"doan:{l}" for l in labels])
    cmdf.to_csv(out / "confusion_matrix.csv", encoding="utf-8-sig")

    # ---------- 3. Nham lan quanh Kinh doanh ----------
    rows = []
    sub = pred[(pred["label"] == TARGET) & (pred["pred_label"] != TARGET)]
    for k, n in Counter(sub["pred_label"]).most_common():
        rows.append({"huong": f"{TARGET} -> (bi doan thanh)", "lop_khac": k, "so_bai": n})
    sub2 = pred[(pred["pred_label"] == TARGET) & (pred["label"] != TARGET)]
    for k, n in Counter(sub2["label"]).most_common():
        rows.append({"huong": f"(that la) -> {TARGET}", "lop_khac": k, "so_bai": n})
    conf = pd.DataFrame(rows)
    conf.to_csv(out / "kinhdoanh_confusions.csv", index=False, encoding="utf-8-sig")
    md.append("\n## 2. Nham lan quanh lop Kinh doanh (tap test)\n")
    md.append(f"- Bai Kinh doanh bi doan sai: {len(sub)}/{int((pred['label'] == TARGET).sum())}\n")
    md.append(f"- Bai lop khac bi doan thanh Kinh doanh: {len(sub2)}\n\n")
    md.append((md_table(conf) if len(conf) else "(khong co nham lan)") + "\n")

    err = pred[((pred["label"] == TARGET) | (pred["pred_label"] == TARGET)) & (pred["label"] != pred["pred_label"])]
    err = err[["id", "title", "label", "pred_label", "source", "publish_date", "url"]]
    err.to_csv(out / "kinhdoanh_errors.csv", index=False, encoding="utf-8-sig")

    # ---------- 4. Tu khoa dac trung (binary: Kinh doanh vs con lai, chi dung train) ----------
    vec = TfidfVectorizer(ngram_range=(1, 2), min_df=3, max_df=0.9, sublinear_tf=True)
    Xtr = vec.fit_transform(train["text"].astype(str))
    ytr = (train["label"] == TARGET).values
    clf = LinearSVC(C=1.0, class_weight="balanced", random_state=42).fit(Xtr, ytr)
    terms = np.array(vec.get_feature_names_out())
    coef = clf.coef_[0]
    binX = (Xtr > 0).astype(int)
    df_kd = np.asarray(binX[ytr].sum(axis=0)).ravel()
    df_ot = np.asarray(binX[~ytr].sum(axis=0)).ravel()
    n_kd, n_ot = int(ytr.sum()), int((~ytr).sum())

    def top(idx):
        return pd.DataFrame({"tu_khoa": terms[idx], "he_so": coef[idx],
                             "ty_le_bai_KD_chua(%)": 100 * df_kd[idx] / max(n_kd, 1),
                             "ty_le_bai_khac_chua(%)": 100 * df_ot[idx] / max(n_ot, 1)})
    pos = top(np.argsort(-coef)[:a.topn])
    neg = top(np.argsort(coef)[:a.topn])
    pos.to_csv(out / "keywords_kinhdoanh.csv", index=False, encoding="utf-8-sig")
    neg.to_csv(out / "keywords_not_kinhdoanh.csv", index=False, encoding="utf-8-sig")
    md.append(f"\n## 3. Tu khoa dac trung cua nhom Kinh doanh\n")
    md.append("Mo hinh nhi phan LinearSVC (Kinh doanh vs con lai) tren tap train, TF-IDF (1,2), min_df=3. "
              "He so duong lon = tu khoa nghieng ve Kinh doanh. Day la phan tich tu khoa, khong phai mo hinh 13 lop cua Lab 2.\n\n")
    md.append(md_table(pos, "{:.3f}") + "\n")

    # ---------- 5. Theo nguon bao ----------
    full["is_kd"] = full["label"] == TARGET
    by_src = full.groupby("source").agg(tong_bai=("id", "count"), bai_KD=("is_kd", "sum")).reset_index()
    by_src["ty_le_KD(%)"] = 100 * by_src["bai_KD"] / by_src["tong_bai"]
    tk = pred.assign(is_kd=pred["label"] == TARGET)
    rec = []
    for src, g in tk.groupby("source"):
        g_kd = g[g["is_kd"]]
        rec.append({"source": src, "test_KD": len(g_kd),
                    "recall_KD_test": (g_kd["pred_label"] == TARGET).mean() if len(g_kd) else np.nan})
    by_src = by_src.merge(pd.DataFrame(rec), on="source", how="left").sort_values("tong_bai", ascending=False)
    by_src.to_csv(out / "kinhdoanh_by_source.csv", index=False, encoding="utf-8-sig")
    md.append("\n## 4. Nhom Kinh doanh theo nguon bao (toan bo du lieu)\n")
    md.append(md_table(by_src, "{:.2f}") + "\n")

    # ---------- 6. Theo thoi gian ----------
    dt = pd.to_datetime(full["publish_date"], errors="coerce")
    bad = int(dt.isna().sum())
    full["year"] = dt.dt.year
    by_year = full.dropna(subset=["year"]).groupby("year").agg(tong_bai=("id", "count"), bai_KD=("is_kd", "sum")).reset_index()
    by_year["year"] = by_year["year"].astype(int)
    by_year["ty_le_KD(%)"] = 100 * by_year["bai_KD"] / by_year["tong_bai"]
    by_year["luu_y"] = np.where(by_year["tong_bai"] < 30, "it bai (<30), ty le khong on dinh", "")
    by_year.to_csv(out / "kinhdoanh_by_year.csv", index=False, encoding="utf-8-sig")
    md.append(f"\n## 5. Nhom Kinh doanh theo nam dang (khong parse duoc ngay: {bad} bai)\n")
    md.append(md_table(by_year, "{:.2f}") + "\n")

    # ---------- 7. Do dai bai ----------
    full["n_words"] = full["text"].astype(str).str.split().str.len()
    ln = full.groupby("is_kd")["n_words"].agg(["count", "median", "mean", lambda x: x.quantile(0.9)]).reset_index()
    ln.columns = ["la_Kinh_doanh", "so_bai", "median_tu", "mean_tu", "p90_tu"]
    ln.to_csv(out / "length_stats.csv", index=False, encoding="utf-8-sig")
    md.append("\n## 6. Do dai bai (so tu theo khoang trang)\n")
    md.append(md_table(ln, "{:.1f}") + "\n")

    (out / "kinhte_summary.md").write_text("\n".join(md), encoding="utf-8")

    # ---------- Hinh ----------
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(10, 8))
        ax.imshow(cm, cmap="Blues")
        ax.set_xticks(range(len(labels)))
        ax.set_yticks(range(len(labels)))
        ax.set_xticklabels(labels, rotation=60, ha="right")
        ax.set_yticklabels(labels)
        for i in range(len(labels)):
            for j in range(len(labels)):
                if cm[i, j]:
                    ax.text(j, i, cm[i, j], ha="center", va="center",
                            color="white" if cm[i, j] > cm.max() / 2 else "black", fontsize=8)
        ax.set_xlabel("Du doan")
        ax.set_ylabel("That")
        ax.set_title("Confusion matrix (test)")
        fig.tight_layout()
        fig.savefig(out / "confusion_matrix.png", dpi=150)
        plt.close(fig)

        fig, ax = plt.subplots(figsize=(8, 7))
        t = pos.iloc[::-1]
        ax.barh(t["tu_khoa"], t["he_so"], color="#1f4e79")
        ax.set_title(f"Top {a.topn} tu khoa nghieng ve {TARGET}")
        ax.set_xlabel("He so LinearSVC")
        fig.tight_layout()
        fig.savefig(out / "keywords_kinhdoanh.png", dpi=150)
        plt.close(fig)

        fig, ax = plt.subplots(figsize=(8, 4))
        ax.bar(by_year["year"].astype(str), by_year["ty_le_KD(%)"], color="#b85c00")
        ax.set_ylabel(f"Ty le bai {TARGET} (%)")
        ax.set_title("Ty le nhom Kinh doanh theo nam")
        plt.xticks(rotation=45)
        fig.tight_layout()
        fig.savefig(out / "kinhdoanh_by_year.png", dpi=150)
        plt.close(fig)
    except Exception as e:  # khong co matplotlib van tiep tuc
        print("Bo qua hinh ve:", e)

    print(f"Accuracy={acc:.4f}  Macro-F1={mf1:.4f}  (Lab 2 V0: 0.8716 / 0.7421)")
    print(f"{TARGET}: P={kd['precision']:.4f} R={kd['recall']:.4f} F1={kd['f1']:.4f} support={int(kd['support_test'])}")
    print("Nham lan lien quan Kinh doanh (test):")
    print(conf.to_string(index=False) if len(conf) else "  (khong co)")
    print("Top tu khoa Kinh doanh:", ", ".join(pos["tu_khoa"].head(15)))
    print("Ghi vao:", out)


if __name__ == "__main__":
    sys.exit(main())
