# kernel/Dockerfile

FROM python:3.10-slim

# Work Directory in Docker
WORKDIR /kernel

RUN apt-get update && \
    apt-get install -y curl gnupg && \
    curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs && \
    apt-get clean

COPY require_kernel.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r require_kernel.txt

# Copy All to Docker
COPY . ./

# Set Root Directory
ENV PYTHONPATH=/

# Run Kernel in Docker
CMD ["uvicorn", "kernel_server:app", "--host", "0.0.0.0", "--port", "4000"]
