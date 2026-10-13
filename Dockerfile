FROM python:3.15
COPY requirements.txt .
RUN pip install -r requirements.txt
CMD ["python", "/app/code/run.py"]