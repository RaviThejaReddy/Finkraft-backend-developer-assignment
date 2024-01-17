# Use an official Python runtime as a parent image
FROM python:3.9

# Set working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY ./app /app

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port that your app runs on
EXPOSE 6000

# Define environment variable
ENV FLASK_APP=app.py

# Run app.py when the container launches
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "6000"]
