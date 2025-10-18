# 🧠 Computer Vision Lab 2 — Blur & Anonymize Faces

## 👤 Thông tin sinh viên
- **Họ và tên:** [Điền tên bạn]
- **MSSV:** [Điền MSSV của bạn]
- **Lớp:** [VD: K67TĐT]

---

## 📘 Mô tả
Ứng dụng cho phép **phát hiện khuôn mặt** và **làm mờ hoặc ẩn danh (anonymize)** khuôn mặt trong ảnh, video hoặc webcam.  
Mục tiêu là bảo vệ danh tính của các đối tượng trong hình ảnh bằng các kỹ thuật xử lý ảnh.

---

## ⚙️ Tính năng chính
1. **Phát hiện khuôn mặt** bằng **Haar Cascade** (OpenCV).
2. **Chế độ ẩn danh khuôn mặt**:
   - `BLUR`: Làm mờ bằng Gaussian blur.
   - `PIXEL`: Làm mờ dạng pixel (chia khối vuông).
   - `STICKER`: Dán sticker (emoji hoặc icon tuỳ chọn).
3. **Điều chỉnh cường độ** bằng thanh **Strength (Trackbar)**.
4. **Hỗ trợ nhiều nguồn dữ liệu**:
   - Ảnh (Image file)
   - Video file
   - Webcam (realtime)
5. **Chức năng tiện ích**:
   - Dừng / chạy lại video
   - Lưu frame kết quả (`Save Frame`)
6. **Giao diện đơn giản với Tkinter** – trực quan, dễ thao tác.

---

## 🧩 Thư viện sử dụng

| Thư viện | Mục đích |
|-----------|----------|
| `opencv-python` | Xử lý ảnh/video, phát hiện khuôn mặt |
| `numpy` | Xử lý mảng ảnh |
| `Pillow` | Hiển thị ảnh trong Tkinter |
| `tkinter` | Tạo giao diện người dùng |
| `threading` | Chạy video / webcam song song (realtime) |

---

## 💻 Cài đặt môi trường

### 1️⃣ Tạo môi trường ảo (tuỳ chọn)
```bash
python -m venv venv
source venv/bin/activate   # (Linux / macOS)
venv\Scripts\activate      # (Windows)
```

### 2️⃣ Cài các thư viện cần thiết
```bash
pip install -r requirements.txt
```

### 3️⃣ File `requirements.txt` gồm:
```
opencv-python
numpy
Pillow
```

---

## 🚀 Cách chạy chương trình

```bash
python anonymize_gui.py
```

---

## 🧠 Cách sử dụng GUI

1. **Mở ảnh hoặc video**:
   - Nhấn **Open Image** hoặc **Open Video** để chọn tệp.
2. **Dùng webcam**:
   - Nhấn **Start Webcam** để phát hiện và ẩn danh realtime.
3. **Chọn chế độ ẩn danh**:
   - Dropdown “Mode” → chọn `BLUR`, `PIXEL`, hoặc `STICKER`.
4. **Điều chỉnh mức độ mờ**:
   - Thanh **Strength** điều chỉnh độ mạnh yếu của hiệu ứng.
5. **Lưu kết quả**:
   - Nhấn **Save Frame** để lưu khung hình hiện tại.
6. **Dừng video/webcam**:
   - Nhấn **Stop** khi muốn dừng xử lý.

---

## 📁 Cấu trúc thư mục nộp bài

```
Lab2_Blur_Anonymize/
│
├── anonymize_gui.py           # Mã nguồn chính
├── requirements.txt           # Danh sách thư viện
├── README.md                  # File mô tả (file này)
├── stickers/                  # (tuỳ chọn) folder chứa sticker của bạn
└── demo/                      # (tuỳ chọn) chứa hình ảnh / video demo
```

---

## 📝 Ghi chú

- Có thể thay đổi sticker bằng ảnh PNG riêng (có nền trong suốt).
- Mọi thao tác realtime, dễ dàng chuyển đổi giữa các chế độ.
- Mã nguồn chạy ổn định trên Windows, Linux và macOS.

---

## 🎯 Kết luận

Ứng dụng đáp ứng đầy đủ yêu cầu của bài Lab 2:
- Phát hiện khuôn mặt.
- Làm mờ và ẩn danh bằng nhiều phương pháp.
- Có GUI thân thiện, dễ thao tác.
- Có thể xử lý cả ảnh, video và webcam.
