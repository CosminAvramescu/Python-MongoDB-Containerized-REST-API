FROM python:3.6
WORKDIR /app
COPY requirements.txt ./
RUN pip install -U setuptools
RUN pip install -r requirements.txt
COPY ../src .
EXPOSE 6000
CMD ["flask", "run", "--host=0.0.0.0", "--port=6000"]
