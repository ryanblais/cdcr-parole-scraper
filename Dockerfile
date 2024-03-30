# Use an official Python runtime as the base image
# FROM python:3.11
FROM public.ecr.aws/lambda/python:3.11

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Print list of installed packages (for verification)
RUN pip freeze > installed_packages.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Run your application
CMD ["python", "app/main.py"]
