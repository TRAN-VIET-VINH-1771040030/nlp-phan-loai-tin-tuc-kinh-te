# Kiem tra yeu to nguon bao (source) cho nhom Kinh doanh

## 1. Nhan Kinh doanh va nguon bao

- dantri: 969/976 bai la Kinh doanh (99.28%)

- 969/1113 bai Kinh doanh (87.06%) den tu dantri


| source | Công đoàn | Giáo dục | Giải trí | Khoa học | Kinh doanh | Pháp luật | Sức khỏe | Thế giới | Thể thao | Thời sự | Xe | Xã hội | Đời sống | tong |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| vnexpress | 0 | 418 | 0 | 441 | 6 | 27 | 50 | 6 | 0 | 6 | 0 | 0 | 46 | 1000 |
| dantri | 0 | 0 | 7 | 0 | 969 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 976 |
| thanhnien | 0 | 64 | 52 | 43 | 50 | 37 | 61 | 57 | 52 | 105 | 0 | 0 | 58 | 579 |
| nguoilaodong | 39 | 0 | 0 | 35 | 37 | 40 | 37 | 0 | 35 | 40 | 0 | 0 | 0 | 263 |
| tienphong | 0 | 25 | 23 | 0 | 35 | 28 | 20 | 24 | 28 | 0 | 0 | 36 | 21 | 240 |
| tuoitre | 0 | 21 | 18 | 0 | 16 | 18 | 22 | 20 | 28 | 21 | 24 | 0 | 22 | 210 |


## 2. Hieu nang lop Kinh doanh tren tap test, tach theo nguon

| nhom | so_bai_test | so_bai_KD_that | TP | FP | FN | precision | recall | F1 |
|---|---|---|---|---|---|---|---|---|
| Tat ca | 327 | 112 | 108 | 17 | 4 | 0.8640 | 0.9643 | 0.9114 |
| Chi dantri | 94 | 94 | 93 | 0 | 1 | 1.0000 | 0.9894 | 0.9947 |
| Cac nguon khac (khong dantri) | 233 | 18 | 15 | 17 | 3 | 0.4688 | 0.8333 | 0.6000 |
| Baseline: doan Kinh doanh neu source == dantri | 327 | 112 | 94 | 0 | 18 | 1.0000 | 0.8393 | 0.9126 |


## 3. Tu khoa dac trung: tat ca nguon va chi cac nguon khong phai dantri

- Mo hinh A: toan bo train (2614 bai, 890 Kinh doanh). Mo hinh B: chi bai khong phai dantri (1832 bai, 115 Kinh doanh).

- So tu khoa trung nhau trong top 30: 14


| top_A_tat_ca_nguon | top_B_khong_dantri |
|---|---|
| tỷ | đầu tư |
| doanh | công ty |
| đầu tư | ty |
| công ty | doanh |
| khách hàng | công thương |
| ty | thương |
| tỷ đồng | thuế |
| hàng | tổng công |
| thị trường | khẩu |
| công thương | xuất khẩu |
| cổ | ngân hàng |
| tư | mua |
| ngân hàng | thương mại |
| sản | tỉ đồng |
| khẩu | tnhh |
| doanh nghiệp | mại |
| thuế | nhà đầu |
| xuất khẩu | vn |
| nhà đầu | ty tnhh |
| triển bền | chủ đầu |
| esg | thị trường |
| tphcm | kinh doanh |
| ảnh | long thành |
| ngành | doanh nghiệp |
| usd | cổ |
| dịch | bạc |
| nhà máy | nhập khẩu |
| tỷ usd | khách hàng |
| tỷ phú | tỉ |
| khách | cung ứng |


## 4. Ty le bai chua tu khoa (train) theo nhom

So bai: KD & dantri = 775; KD & khac dantri = 115; khong KD & khac dantri = 1717


| tu_khoa | KD & dantri (%) | KD & khac dantri (%) | khong KD & khac dantri (%) |
|---|---|---|---|
| tỷ | 63.0 | 21.7 | 17.2 |
| doanh | 68.9 | 69.6 | 19.2 |
| đầu tư | 59.7 | 67.0 | 13.4 |
| công ty | 52.8 | 54.8 | 18.1 |
| khách hàng | 23.2 | 20.0 | 4.1 |
| ty | 52.8 | 54.8 | 18.1 |
| tỷ đồng | 37.3 | 6.1 | 4.1 |
| hàng | 81.7 | 73.9 | 45.3 |
| thị trường | 64.3 | 48.7 | 10.3 |
| công thương | 7.4 | 13.9 | 1.6 |
| cổ | 44.6 | 25.2 | 9.6 |
| tư | 72.0 | 73.9 | 34.0 |
| ngân hàng | 36.1 | 27.8 | 4.7 |
| sản | 70.8 | 71.3 | 31.2 |
| khẩu | 23.4 | 27.0 | 6.6 |
| doanh nghiệp | 53.4 | 57.4 | 12.5 |
| thuế | 25.5 | 26.1 | 3.3 |
| xuất khẩu | 13.8 | 20.9 | 1.3 |
| nhà đầu | 29.5 | 28.7 | 2.2 |
| triển bền | 15.0 | 9.6 | 2.7 |
| esg | 7.9 | 1.7 | 0.1 |
| tphcm | 17.8 | 9.6 | 4.1 |
| ảnh | 91.4 | 61.7 | 52.4 |
| ngành | 43.2 | 44.3 | 22.8 |
| usd | 36.8 | 22.6 | 8.9 |
| dịch | 64.1 | 53.9 | 21.7 |
| nhà máy | 11.4 | 12.2 | 3.3 |
| tỷ usd | 21.0 | 5.2 | 2.3 |
| tỷ phú | 9.3 | 1.7 | 0.7 |
| khách | 31.6 | 35.7 | 14.2 |
