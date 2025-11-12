FROM python:3.10-slim

# 필요한 패키지 설치
RUN apt-get update && apt-get install -y \
    git \
    curl \
    wget \
    ffmpeg \
    libsm6 \
    libxext6 \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# 작업 디렉토리 설정
WORKDIR /app

# 필요한 파일 복사
COPY requirements.txt .
COPY scripts/ ./scripts/
COPY install_dependencies.sh .

# 필요한 Python 패키지 설치
RUN pip install --no-cache-dir -r requirements.txt

# NVIDIA CUDA 환경 설정을 위한 환경 변수
ENV NVIDIA_VISIBLE_DEVICES all
ENV NVIDIA_DRIVER_CAPABILITIES compute,utility

# 권한 설정
RUN chmod +x /app/scripts/main_launcher.py
RUN chmod +x /app/install_dependencies.sh

# 실행 명령
CMD ["python", "/app/scripts/main_launcher.py"] 