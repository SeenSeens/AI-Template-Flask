FROM python:bullseye

# Đặt thư mục làm việc
WORKDIR /app

# Copy và cài đặt thư viện
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ project vào container
COPY . .

# Mở port 5000 cho Flask
EXPOSE 5000

# Chạy app
CMD ["python", "application.py"]
