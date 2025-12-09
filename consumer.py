import json
from kafka import KafkaConsumer

topic_name = 'water_quality_stream'

consumer = KafkaConsumer(
    topic_name,
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='latest', # Đổi thành 'latest' để chỉ xem dữ liệu mới đang chạy
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

print(f"--- Đang chờ dữ liệu từ topic: {topic_name} ---")

for message in consumer:
    data = message.value
    
    # Hiển thị dạng bảng đơn giản
    print(f"Time: {data['date']} | {data['parameter']} = {data['value']} ({data['unit']})")