# Use an official Python runtime as the base image
# FROM python:3.11
# FROM public.ecr.aws/lambda/python:3.11
# FROM ubuntu:jammy
FROM mcr.microsoft.com/playwright:v1.42.1-jammy

RUN apt-get update
RUN apt-get install -y python3-pip

#ARG FUNCTION_DIR="/function"
#RUN mkdir -p ${FUNCTION_DIR}

RUN pip3 install awslambdaric

#COPY ./requirements.txt ${LAMBDA_TASK_ROOT}
COPY ./requirements.txt .

# Install any needed dependencies specified in requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

COPY ./app .
COPY ./scrapper.yaml .

# Add Lambda Runtime Interface Emulator
# see https://docs.aws.amazon.com/lambda/latest/dg/images-test.html
COPY ./entry_script.sh /entry_script.sh
RUN chmod +x /entry_script.sh
ADD aws-lambda-rie /usr/local/bin/aws-lambda-rie

ENTRYPOINT [ "/entry_script.sh","main.lambda_handler" ]

# Run your application
#CMD ["main.lambda_handler"]
