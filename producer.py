import csv
import json
import time
from kafka import KafkaProducer

# 1. Cấu hình Kafka
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    # IP này phải sửa thành IP máy ảo nếu chạy từ máy khác
    # bootstrap_servers=['192.168.x.x:9092'], 
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

topic_name = 'water_quality_stream'

print(f"--- Bắt đầu stream dữ liệu Water Quality ---")

input_file = '2025-C.csv' # Đảm bảo tên file đúng với file bạn tải lên

try:
    with open(input_file, mode='r', encoding='utf-8-sig') as file:
        csv_reader = csv.DictReader(file)
        
        current_location = ""
        
        for row in csv_reader:
            # --- Xử lý dữ liệu (như code cũ) ---
            raw_result = row.get('result', 0)
            try:
                if isinstance(raw_result, str):
                    clean_result = float(raw_result.replace('<', '').strip())
                else:
                    clean_result = float(raw_result)
            except:
                clean_result = 0.0

            message = {
                'id': row.get('@id', 'N/A'),
                'location': row.get('sample.samplingPoint.label', 'Unknown'), # Lấy tên địa điểm
                'date': row.get('sample.sampleDateTime', ''),
                'parameter': row.get('determinand.label', 'Unknown'),
                'value': clean_result,
                'unit': row.get('determinand.unit.label', '')
            }

            # --- GỬI VÀO KAFKA ---
            producer.send(topic_name, value=message)
            
            # --- LOG THÔNG MINH HƠN ---
            # Chỉ in đậm khi chuyển sang một ĐỊA ĐIỂM mới
            new_location = message['location']
            
            if new_location != current_location:
                print("\n" + "="*50)
                print(f"⚡ CHUYỂN ĐỊA ĐIỂM MỚI: {new_location}")
                print("="*50)
                current_location = new_location
                time.sleep(1) # Dừng lại 1 chút ở địa điểm mới để bạn kịp đọc tên
            else:
                # Nếu vẫn là địa điểm cũ, in gọn nhẹ hoặc không in để đỡ rối mắt
                # print(f"   -> Đo {message['parameter']}: {message['value']}") 
                pass 
                
            # Stream cực nhanh: 0.01 giây/dòng (để lướt nhanh qua các dòng giống nhau)
            time.sleep(0.01)

except FileNotFoundError:
    print(f"Lỗi: Không tìm thấy file {input_file}. Hãy chắc chắn file nằm cùng thư mục.")
except Exception as e:
    print(f"Có lỗi: {e}")

producer.flush()
print("--- Hoàn tất ---")