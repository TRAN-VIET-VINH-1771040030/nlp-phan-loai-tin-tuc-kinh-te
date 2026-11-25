"""Trang chính: dự đoán chuyên mục. Chạy: streamlit run app/Home.py"""
import numpy as np
import pandas as pd
import streamlit as st

from common import load_model, normalize

st.set_page_config(page_title="Phân loại tin tức tiếng Việt", page_icon="📰", layout="wide")
st.title("📰 Phân loại chuyên mục tin tức tiếng Việt")
st.caption("TF-IDF (1,2) + LinearSVM · dữ liệu UVN-1 · CSC4007 – Nhóm 10")

model = load_model()
if model is None:
    st.error("Chưa có model/model.joblib. Chạy `python train_model.py` trước.")
    st.stop()

tfidf, svm = model.named_steps["tfidf"], model.named_steps["svm"]

col_in, col_out = st.columns([3, 2])
with col_in:
    title = st.text_input("Tiêu đề (không bắt buộc)")
    content = st.text_area("Nội dung bài báo", height=300, placeholder="Dán nội dung bài báo vào đây...")
    use_title = st.checkbox("Ghép tiêu đề vào nội dung", value=False,
                            help="Dữ liệu train hầu như không chứa tiêu đề trong cột text.")
    go = st.button("Dự đoán", type="primary")

if go:
    raw = f"{title} . {content}" if use_title and title else content
    if len(raw.split()) < 20:
        col_out.warning("Nên nhập ít nhất khoảng 20 từ để dự đoán đáng tin cậy.")
        st.stop()

    X = tfidf.transform([normalize(raw)])
    scores = svm.decision_function(X)[0]
    order = np.argsort(scores)[::-1]
    classes = svm.classes_
    pred = classes[order[0]]

    with col_out:
        st.subheader(f"Kết quả: {pred}")
        margin = scores[order[0]] - scores[order[1]]
        st.metric("Biên với lớp xếp thứ 2", f"{margin:.3f}",
                  help="Biên nhỏ nghĩa là mô hình lưỡng lự giữa hai chuyên mục.")
        st.bar_chart(pd.Series(scores, index=classes, name="điểm quyết định").sort_values(),
                     horizontal=True)

        # Từ/cụm từ đóng góp nhiều nhất = hệ số * giá trị TF-IDF của lớp được chọn
        idx = list(classes).index(pred)
        coef = svm.coef_[idx] if len(classes) > 2 else svm.coef_[0]
        row = X.tocoo()
        contrib = pd.Series(coef[row.col] * row.data, index=tfidf.get_feature_names_out()[row.col])
        st.markdown("**Từ/cụm từ đóng góp nhiều nhất**")
        st.dataframe(contrib.sort_values(ascending=False).head(10).rename("đóng góp").to_frame())

    if pred == "Kinh doanh":
        st.info("⚠️ Nhãn Kinh doanh trong dữ liệu train gần như trùng nguồn Dân trí (99,3% bài Dân trí là Kinh doanh). "
                "Trên các nguồn khác, F1 lớp này chỉ còn 0,60. Xem trang *Kiểm tra nguồn báo*.")

st.divider()
st.caption("Lưu ý: mô hình trong demo gần khớp, chưa trùng tuyệt đối với mô hình Lab 2 "
           "(Macro-F1 0,7419 so với 0,7421 trong báo cáo).")
