FROM python:3.10
COPY server.py .
CMD ["python3", "server.py"]
