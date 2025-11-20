from python:3.14.0

workdir /app

copy ..

run pip install --no-cache-dir -r requirements.txt

cmd echo "pytest test_endpoints.py"


