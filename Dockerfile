FROM python:3.8
WORKDIR /home/learning-platform
COPY requirements.txt .
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
CMD ["python", "node_run.py"]