FROM python:3.12-alpine
COPY check.py .
CMD ["python", "-u", "check.py"]
