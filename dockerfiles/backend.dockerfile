# 使用 Python 的官方映像檔作為基礎
FROM python:3.9

# 設定工作目錄
WORKDIR /backend

# 將 requirements.txt 複製到容器中並安裝依賴套件
COPY /backend/requirements.txt /backend
RUN pip install --no-cache-dir -r requirements.txt

# 複製整個目錄到容器中
COPY /backend /backend

# 定義容器啟動時要執行的命令
CMD ["python", "simple_server.py"]
EXPOSE 4000