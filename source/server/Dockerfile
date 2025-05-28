# kernel/Dockerfile

FROM python:3.10-slim

# Work Directory in Docker
WORKDIR /server

COPY require_server.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r require_server.txt

# Copy All to Docker
COPY . ./

# ( + ) to Execute "wait-for-it.sh" for Synchronizing with MySQL DB
RUN chmod +x /server/wait-for-it.sh

# Set Root Directory
ENV PYTHONPATH=/

# Run Server in Docker
CMD ["/server/wait-for-it.sh", "db:3306", "--", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "3000"]
