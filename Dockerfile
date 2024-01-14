# Use an official Python runtime as a parent image
FROM python:3.9

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container to /app
WORKDIR /app

# Install Poetry
RUN pip install poetry

# Copy the poetry and runtime requirements
COPY pyproject.toml poetry.lock* /app/

# Install dependencies
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

# Copy the rest of the application
COPY . /app

# Make port available to the world outside this container
EXPOSE 80

# Command to run the application
CMD ["python", "app.py"]  # Modify as needed to run your specific app or server
