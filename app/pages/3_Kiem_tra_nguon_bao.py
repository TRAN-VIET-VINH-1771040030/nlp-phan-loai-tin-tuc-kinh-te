import streamlit as st

from common import load_csv

st.title("📰 Kiểm tra yếu tố nguồn báo")
st.markdown(
    "**Phát hiện chính:** 969/1113 bài Kinh doanh (87,06%) đến từ Dân trí, và 99,28% bài Dân trí mang nhãn "
    "Kinh doanh. Một quy tắc chỉ nhìn nguồn báo đạt F1 gần bằng mô hình."
)

g = load_csv("kinhdoanh_by_source_group.csv")
st.subheader("Hiệu năng lớp Kinh doanh theo nhóm nguồn")
st.dataframe(g.style.format({"precision": "{:.4f}", "recall": "{:.4f}", "F1": "{:.4f}"}),
             hide_index=True)
st.bar_chart(g.set_index("nhom")["F1"])

c1, c2 = st.columns(2)
c1.metric("F1 – mô hình (tất cả nguồn)", "0,9114")
c2.metric("F1 – quy tắc “nguồn = Dân trí”", "0,9126")
st.error("Trên các nguồn không phải Dân trí, F1 chỉ còn 0,60 (precision 0,47). "
         "Việc mô hình có dựa vào dấu hiệu nguồn hay không mới là giả thuyết, chưa kiểm chứng.")

st.subheader("Tỷ lệ bài Kinh doanh theo nguồn")
s = load_csv("kinhdoanh_by_source.csv")
st.bar_chart(s.set_index("source")["ty_le_KD(%)"])
st.dataframe(s, hide_index=True)

st.subheader("Từ khóa: tất cả nguồn và chỉ nguồn khác Dân trí")
st.dataframe(load_csv("keywords_A_vs_B.csv").rename(
    columns={"A_tat_ca": "Mô hình A (tất cả nguồn)", "B_khong_dantri": "Mô hình B (không Dân trí)"}),
    hide_index=True)
st.subheader("Tỷ lệ bài chứa từ khóa theo nhóm (train)")
st.dataframe(load_csv("keyword_share_by_group.csv"), hide_index=True)
