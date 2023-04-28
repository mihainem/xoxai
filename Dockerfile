FROM python:3.10-slim

# Set the working directory to /code
WORKDIR /code

# Copy requirements.txt to the working directory
COPY ./requirements.txt .
# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy src to the src directory inside the container
COPY ./src ./src

# Run ws.py when the container launches
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]
