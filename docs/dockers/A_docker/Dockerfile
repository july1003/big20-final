# 1. GPU 지원 및 파이썬 환경을 위한 NVIDIA CUDA 베이스 이미지 사용
# 윈도우 Docker Desktop(WSL2) 환경에서 GPU를 원활히 쓰기 위해 최적화된 버전입니다.
FROM nvidia/cuda:12.1.0-base-ubuntu22.04

# 2. 파이썬 및 필수 시스템 패키지 설치
# OpenCV(얼굴인식), PostgreSQL, Oracle 클라이언트 설치를 위한 설정입니다.
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libpq-dev \
    libaio1 \
    wget \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# 3. 작업 디렉토리 설정
WORKDIR /app

# 4. 파이썬 패키지 설치
# 이전에 추천드린 requirements.txt 파일을 복사하여 설치합니다.
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# 5. 소스 코드 복사
COPY . .

# 6. 환경 변수 설정
# 파이썬 출력을 실시간으로 확인하기 위한 설정입니다.
ENV PYTHONUNBUFFERED=1

# 7. 실행 (docker-compose의 command에서 덮어쓰므로 여기서는 기본값만 설정)
CMD ["python3", "main.py"]