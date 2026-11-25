import streamlit as st

from common import RESULTS, load_csv

st.title("📊 Kết quả mô hình (tập test 327 bài)")
m = load_csv("per_class_metrics.csv")

c1, c2, c3 = st.columns(3)
c1.metric("Accuracy", "0,8716")
c2.metric("Macro-F1", "0,7421")
c3.metric("F1 lớp Kinh doanh", "0,9114")

st.subheader("Chỉ số theo lớp")
st.dataframe(m.style.format({"precision": "{:.3f}", "recall": "{:.3f}", "f1": "{:.3f}"}),
             hide_index=True)
st.bar_chart(m.set_index("lop")["f1"])
st.caption("Các lớp nhỏ (Xã hội: 4 bài, Xe: 2 bài, Công đoàn: 4 bài) rất ít mẫu nên F1 dao động mạnh.")

st.subheader("Ma trận nhầm lẫn")
cm = load_csv("confusion_matrix.csv").set_index("Unnamed: 0")
cm.index = cm.index.str.replace("that:", "", regex=False)
cm.columns = cm.columns.str.replace("doan:", "", regex=False)
st.dataframe(cm.style.background_gradient(cmap="Blues"))
st.image(str(RESULTS / "confusion_matrix.png"), caption="Hàng: nhãn thật · Cột: nhãn dự đoán")

st.subheader("Nhầm lẫn quanh lớp Kinh doanh")
st.dataframe(load_csv("kinhdoanh_confusions.csv"), hide_index=True)
