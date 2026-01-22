# 1. 파이썬 3.10 슬림 베이스 이미지 (서버 C는 DB 부하를 고려해 가벼운 이미지 권장)
FROM python:3.10-slim

# 2. 필수 시스템 패키지 설치
# Oracle용 libaio1과 PostgreSQL용 libpq-dev가 핵심입니다.
RUN apt-get update && apt-get install -y \
    libpq-dev \
    libaio1 \
    wget \
    unzip \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 3. Oracle Instant Client 설치 (Oracle DB 접속에 필수)
WORKDIR /opt/oracle
RUN wget https://download.oracle.com/otn_software/linux/instantclient/instantclient-basic-linuxx64.el9.zip && \
    unzip *.zip && rm -f *.zip
ENV LD_LIBRARY_PATH=/opt/oracle/instantclient_19_25:$LD_LIBRARY_PATH

# 4. 작업 디렉토리 설정
WORKDIR /app

# 5. 파이썬 패키지 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6. 소스 코드 복사
COPY . .

# 7. 실행 환경 설정
ENV PYTHONUNBUFFERED=1

# 배치 프로그램 실행 파일 지정 (예: batch_main.py)
CMD ["python", "batch_main.py"]