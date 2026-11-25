# Phan tich nhom tin Kinh te (lop "Kinh doanh")

Nguon: `D:\Xu_li_NNTN\lab2\outputs\vietnews_v0` | train=2614, val=327, test=327, tong=3268

## 1. Hieu nang phan loai (tap test)

Accuracy = 0.8716; Macro-F1 = 0.7421 (Lab 2 bao cao V0: 0.8716 / 0.7421; neu khac thi kiem tra --variant)

| lop | precision | recall | f1 | support_test |
|---|---|---|---|---|
| Kinh doanh | 0.8640 | 0.9643 | 0.9114 | 112 |
| Giáo dục | 0.9615 | 0.9434 | 0.9524 | 53 |
| Khoa học | 0.8246 | 0.9038 | 0.8624 | 52 |
| Sức khỏe | 0.9000 | 0.9474 | 0.9231 | 19 |
| Thời sự | 0.8000 | 0.4706 | 0.5926 | 17 |
| Pháp luật | 0.8462 | 0.7333 | 0.7857 | 15 |
| Đời sống | 0.7500 | 0.6429 | 0.6923 | 14 |
| Thể thao | 1.0000 | 1.0000 | 1.0000 | 14 |
| Thế giới | 1.0000 | 0.6364 | 0.7778 | 11 |
| Giải trí | 0.9000 | 0.9000 | 0.9000 | 10 |
| Xã hội | 0.0000 | 0.0000 | 0.0000 | 4 |
| Công đoàn | 0.7500 | 0.7500 | 0.7500 | 4 |
| Xe | 0.5000 | 0.5000 | 0.5000 | 2 |


Lop Kinh doanh: precision=0.8640, recall=0.9643, F1=0.9114, support=112


## 2. Nham lan quanh lop Kinh doanh (tap test)

- Bai Kinh doanh bi doan sai: 4/112

- Bai lop khac bi doan thanh Kinh doanh: 17


| huong | lop_khac | so_bai |
|---|---|---|
| Kinh doanh -> (bi doan thanh) | Khoa học | 2 |
| Kinh doanh -> (bi doan thanh) | Xã hội | 1 |
| Kinh doanh -> (bi doan thanh) | Công đoàn | 1 |
| (that la) -> Kinh doanh | Thời sự | 5 |
| (that la) -> Kinh doanh | Khoa học | 5 |
| (that la) -> Kinh doanh | Xã hội | 2 |
| (that la) -> Kinh doanh | Đời sống | 1 |
| (that la) -> Kinh doanh | Thế giới | 1 |
| (that la) -> Kinh doanh | Xe | 1 |
| (that la) -> Kinh doanh | Sức khỏe | 1 |
| (that la) -> Kinh doanh | Giải trí | 1 |


## 3. Tu khoa dac trung cua nhom Kinh doanh

Mo hinh nhi phan LinearSVC (Kinh doanh vs con lai) tren tap train, TF-IDF (1,2), min_df=3. He so duong lon = tu khoa nghieng ve Kinh doanh. Day la phan tich tu khoa, khong phai mo hinh 13 lop cua Lab 2.


| tu_khoa | he_so | ty_le_bai_KD_chua(%) | ty_le_bai_khac_chua(%) |
|---|---|---|---|
| tỷ | 1.519 | 57.640 | 17.285 |
| doanh | 1.341 | 68.989 | 19.258 |
| đầu tư | 1.176 | 60.674 | 13.399 |
| công ty | 1.061 | 53.034 | 18.039 |
| khách hàng | 1.061 | 22.809 | 4.060 |
| ty | 1.061 | 53.034 | 18.039 |
| tỷ đồng | 1.059 | 33.258 | 4.118 |
| hàng | 1.033 | 80.674 | 45.244 |
| thị trường | 0.978 | 62.247 | 10.325 |
| công thương | 0.944 | 8.202 | 1.624 |
| cổ | 0.934 | 42.135 | 9.571 |
| tư | 0.874 | 72.247 | 33.933 |
| ngân hàng | 0.863 | 35.056 | 4.698 |
| sản | 0.848 | 70.899 | 31.265 |
| khẩu | 0.836 | 23.820 | 6.671 |
| doanh nghiệp | 0.826 | 53.933 | 12.413 |
| thuế | 0.809 | 25.618 | 3.306 |
| xuất khẩu | 0.792 | 14.719 | 1.334 |
| nhà đầu | 0.772 | 29.438 | 2.146 |
| triển bền | 0.768 | 14.270 | 2.726 |
| esg | 0.753 | 7.079 | 0.058 |
| tphcm | 0.747 | 16.742 | 4.176 |
| ảnh | 0.736 | 87.528 | 52.552 |
| ngành | 0.716 | 43.371 | 22.796 |
| usd | 0.704 | 34.944 | 8.875 |
| dịch | 0.700 | 62.809 | 21.752 |
| nhà máy | 0.699 | 11.461 | 3.306 |
| tỷ usd | 0.695 | 18.989 | 2.320 |
| tỷ phú | 0.693 | 8.315 | 0.754 |
| khách | 0.681 | 32.135 | 14.327 |


## 4. Nhom Kinh doanh theo nguon bao (toan bo du lieu)

| source | tong_bai | bai_KD | ty_le_KD(%) | test_KD | recall_KD_test |
|---|---|---|---|---|---|
| vnexpress | 1000 | 6 | 0.60 | 1 | 1.00 |
| dantri | 976 | 969 | 99.28 | 94 | 0.99 |
| thanhnien | 579 | 50 | 8.64 | 6 | 0.83 |
| nguoilaodong | 263 | 37 | 14.07 | 4 | 1.00 |
| tienphong | 240 | 35 | 14.58 | 6 | 0.67 |
| tuoitre | 210 | 16 | 7.62 | 1 | 1.00 |


## 5. Nhom Kinh doanh theo nam dang (khong parse duoc ngay: 0 bai)

| year | tong_bai | bai_KD | ty_le_KD(%) | luu_y |
|---|---|---|---|---|
| 2011 | 1 | 0 | 0.00 | it bai (<30), ty le khong on dinh |
| 2014 | 1 | 1 | 100.00 | it bai (<30), ty le khong on dinh |
| 2021 | 4 | 0 | 0.00 | it bai (<30), ty le khong on dinh |
| 2022 | 10 | 0 | 0.00 | it bai (<30), ty le khong on dinh |
| 2023 | 41 | 26 | 63.41 |  |
| 2024 | 70 | 44 | 62.86 |  |
| 2025 | 1376 | 399 | 29.00 |  |
| 2026 | 1765 | 643 | 36.43 |  |


## 6. Do dai bai (so tu theo khoang trang)

| la_Kinh_doanh | so_bai | median_tu | mean_tu | p90_tu |
|---|---|---|---|---|
| False | 2155 | 638.0 | 731.2 | 1237.6 |
| True | 1113 | 808.0 | 920.2 | 1552.8 |
