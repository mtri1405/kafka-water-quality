# 🌊 Water Quality Streaming System (Kafka)

Dự án xây dựng hệ thống Streaming dữ liệu quan trắc môi trường (nước) theo thời gian thực sử dụng **Apache Kafka** và **Python**.

Hệ thống đóng vai trò **Data Ingestion** (Thu thập dữ liệu), đọc dữ liệu từ các file báo cáo tuân thủ (Compliance CSV), làm sạch và chuẩn hóa, sau đó đẩy lên Kafka Topic để team Analysis/Visualization tiêu thụ.

---

## 📂 Cấu trúc dự án

```text
kafka-demo/
├── docker-compose.yml    # Cấu hình hạ tầng Kafka & Zookeeper
├── producer.py           # Code đọc file CSV và gửi dữ liệu (Producer)
├── consumer.py           # Code kiểm tra dữ liệu nhận được (Consumer)
├── 2025-C.csv            # Dữ liệu nguồn (Data mẫu nước)
├── venv/                 # Môi trường ảo Python
└── README.md             # Hướng dẫn sử dụng

# 🚀 Hướng dẫn cài đặt & Kích hoạt
1. Chuẩn bị môi trường (Prerequisites)
Yêu cầu máy chủ (Ubuntu VM) đã cài đặt:

Docker & Docker Compose (V2)

Python 3.x

2. Khởi động hạ tầng Kafka
Mở terminal tại thư mục dự án và chạy:

Bash

# Khởi tạo các container Kafka và Zookeeper dưới nền (detached mode)
docker compose up -d
Để kiểm tra trạng thái hoạt động:

Bash

docker compose ps
3. Cài đặt thư viện Python
Sử dụng môi trường ảo (venv) để tránh xung đột hệ thống:

Bash

# Tạo môi trường ảo (chỉ chạy 1 lần đầu)
python3 -m venv venv

# Kích hoạt môi trường
source venv/bin/activate

# Cài đặt thư viện Kafka Client
pip install kafka-python
▶️ Cách vận hành (Workflow)
Để thấy luồng dữ liệu chạy, khuyến khích mở 2 cửa sổ Terminal song song.

Bước 1: Bật Consumer (Người nhận)
Tại Terminal 1, chạy lệnh sau để lắng nghe topic water_quality_stream. Consumer sẽ nằm chờ dữ liệu tới.

Bash

source venv/bin/activate
python3 consumer.py
Bước 2: Bật Producer (Người gửi)
Tại Terminal 2, chạy lệnh sau để bắt đầu đọc file CSV và bắn dữ liệu.

Bash

source venv/bin/activate
python3 producer.py
Kết quả: Bạn sẽ thấy bên Producer thông báo gửi thành công và bên Consumer hiện dữ liệu tương ứng ngay lập tức.

📊 Cấu trúc Dữ liệu (Data Schema)
Dữ liệu được gửi lên Kafka topic water_quality_stream dưới dạng JSON, đã được làm sạch và ép kiểu dữ liệu chuẩn xác phục vụ cho phân tích.

Mẫu bản tin (Message Sample):

JSON

{
  "id": "[http://environment.data.gov.uk/.../AN-011624](http://environment.data.gov.uk/.../AN-011624)",
  "location": "APOLLO OFFICE UNITS RADCLIVE RD GAWCOTT",
  "date": "2025-01-13T12:04:00",
  "parameter": "pH",
  "value": 7.5,
  "unit": "pH units",
  "compliance": true
}
