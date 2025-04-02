FROM python:3.12-slim

WORKDIR /app

# Install uv
RUN pip install uv

# Install requirements in two steps to avoid syntax issues
RUN uv pip install --no-cache-dir torch==2.0.0+cpu --index-url https://download.pytorch.org/whl/cpu

COPY requirements.txt .
RUN grep -v "torch" requirements.txt > requirements_no_torch.txt
RUN pip install --no-cache-dir -r requirements_no_torch.txt

# Copy the rest of the application
COPY . .
RUN mkdir -p data

EXPOSE 8000
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]