# ใช้ภาพฐานของ Python 3.8
FROM python:3.8

# ตั้งโฟลเดอร์ทำงานเป็น /app
WORKDIR /app

# คัดลอกไฟล์ requirements.txt และติดตั้ง dependencies จากภายนอก
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# คัดลอกโมเดลที่คุณใช้จากพื้นที่ของเครื่องคอมพิวเตอร์
COPY model_fruit.h5 /app/model_fruit.h5

# คัดลอกคำสั่งรันไฟล์ main.py ลงใน /app
COPY main.py /app/main.py

# คำสั่งเริ่มต้นที่จะรันเมื่อเปิด container
CMD [ "python", "main.py" ]
