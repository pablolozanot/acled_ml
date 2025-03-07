# Use the official Python image as the base
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Step 1: Confirm the container build
RUN echo "Step 1: Container base image loaded"

# Copy all files to the container
COPY . /app
RUN echo "Step 2: Files copied to /app"

# Install required Python packages
RUN pip install -r /app/requirements.txt
RUN echo "Step 3: Python packages installed"

# List all files in the /app directory to confirm main.py is present
RUN ls -l /app
RUN echo "Step 4: Verified contents of /app directory"

# Add a sleep command to keep the container alive for observation
CMD ["sh", "-c", "echo 'Step 5: Running main.py' && python /app/main.py && echo 'Step 6: main.py completed' && sleep 30"]
