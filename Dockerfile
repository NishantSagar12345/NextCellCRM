# Use Python 3.11 slim for a production-grade foundation [cite: 26]
FROM python:3.11-slim

# Set work directory
WORKDIR /code

# Install dependencies from the root
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the contents of your code folder into the container's app folder
# This maps your local 'crm_backbone' to '/code/app' inside Docker
COPY ./crm_backbone /code

# Set PYTHONPATH so python can find the 'app' package
ENV PYTHONPATH=/code

# Run the FastAPI app using the new path [cite: 58]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]