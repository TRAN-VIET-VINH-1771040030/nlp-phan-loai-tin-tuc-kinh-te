# Phân loại chuyên mục tin tức tiếng Việt và phân tích nhóm tin kinh tế

Bài tập lớn học phần **Xử lí ngôn ngữ tự nhiên** (CSC4007), Trường Đại học Đại Nam.
Giảng viên hướng dẫn: ThS. Lê Thị Thùy Trang. Sinh viên: Trần Việt Vinh (MSSV 1771040030).

## Nội dung

Dự án dùng lại bộ dữ liệu **UVN-1 (VietNewsSense)** và mô hình **TF-IDF (1, 2) + LinearSVM** đã làm ở Lab 2
rồi phân tích sâu nhóm tin kinh tế (chuyên mục *Kinh doanh*):

- Kết quả phân loại 13 chuyên mục: Accuracy 0,8716, Macro-F1 0,7421 (tập test 327 bài).
- Lớp Kinh doanh: Precision 0,8640, Recall 0,9643, F1 0,9114 (108 TP, 17 FP, 4 FN).
- Từ khóa đặc trưng, danh sách bài bị đoán sai, thống kê theo năm và độ dài.
- Kiểm tra yếu tố nguồn báo: nhãn Kinh doanh gần trùng nguồn Dân trí; quy tắc chỉ dùng nguồn đạt F1 0,9126,
  ngang mô hình (0,9114). Việc mô hình có dùng dấu hiệu nguồn hay không mới là giả thuyết, chưa kiểm chứng.

## Cấu trúc thư mục

```
code/        kinhte_analysis.py, kinhte_source_check.py
ket_qua/     bảng CSV, biểu đồ và các tệp tóm tắt do hai script tạo ra
bao_cao/     báo cáo Word và slide
```

## Cách chạy lại

Cần Python 3.9+ với `pandas`, `numpy`, `scikit-learn`, `matplotlib`.
Hai script đọc kết quả của Lab 2 (`outputs/vietnews_v0/predictions/test_predictions.csv` và `splits/train.csv`, `val.csv`):

```powershell
python code\kinhte_analysis.py --lab2 D:\Xu_li_NNTN\lab2 --out ket_qua
python code\kinhte_source_check.py --lab2 D:\Xu_li_NNTN\lab2 --out ket_qua
```

## Lưu ý về dữ liệu

Repo **không chứa** nội dung các bài báo (dữ liệu UVN-1 và tệp dự đoán của Lab 2). Dữ liệu lấy từ
`undertheseanlp/UVN-1` trên Hugging Face; hãy tải về và chạy lại Lab 2 để có các tệp đầu vào.
Một số tệp trong `ket_qua/` có tiêu đề bài báo (ví dụ `kinhdoanh_errors.csv`).

## Hạn chế

Một lần chạy với một hạt giống, tập test 327 bài, các lớp nhỏ rất ít mẫu, dữ liệu dồn vào hai năm 2025–2026.
