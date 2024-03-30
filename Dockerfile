# Use an official Python runtime as the base image
# FROM python:3.11
# FROM public.ecr.aws/lambda/python:3.11
# FROM ubuntu:jammy
FROM mcr.microsoft.com/playwright:v1.42.1-jammy

RUN apt-get update
RUN apt-get install -y python3-pip

# Copy the current directory contents into the container at /app
#COPY ./app ${LAMBDA_TASK_ROOT}

#COPY ./requirements.txt ${LAMBDA_TASK_ROOT}
COPY ./requirements.txt .

# Install any needed dependencies specified in requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

COPY ./app .
COPY ./scrapper.yaml .

# Run your application
CMD ["python3", "main.py"]
