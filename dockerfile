FROM python:3.8-slim-buster
WORKDIR /app

COPY app.py .
COPY denoiser.py .
COPY template .
COPY requirements.txt .
COPY static .

RUN pip3 install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"] 