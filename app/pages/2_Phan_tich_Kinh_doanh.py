import streamlit as st

from common import RESULTS, load_csv

st.title("🔎 Phân tích nhóm Kinh doanh")

tab1, tab2, tab3 = st.tabs(["Từ khóa đặc trưng", "Theo năm", "Độ dài bài"])

with tab1:
    kw = load_csv("keywords_kinhdoanh.csv")
    n = st.slider("Số từ khóa hiển thị", 10, 30, 20)
    st.bar_chart(kw.head(n).set_index("tu_khoa")["he_so"], horizontal=True)
    st.dataframe(kw.head(n), hide_index=True)
    st.caption("Hệ số LinearSVC nhị phân (Kinh doanh vs còn lại), TF-IDF (1,2), min_df=3. "
               "Đây là phân tích từ khóa, không phải mô hình 13 lớp.")

with tab2:
    y = load_csv("kinhdoanh_by_year.csv")
    st.bar_chart(y.set_index("year")["ty_le_KD(%)"])
    st.dataframe(y, hide_index=True)
    st.warning("Dữ liệu dồn vào 2025–2026; các năm trước 2023 chỉ có vài bài nên tỷ lệ không ổn định.")

with tab3:
    st.dataframe(load_csv("length_stats.csv"), hide_index=True)
    st.caption("Độ dài tính theo số từ tách bằng khoảng trắng. Bài Kinh doanh dài hơn (median 808 so với 638 từ).")
