FROM ubuntu:16.04

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev
# Use subdirectory as working directory


# Copy any additional custom requirements, if necessary (uncomment next line)
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app
# Change back to root user to install dependencies


# Install extra requirements for actions code, if necessary (uncomment next line)
RUN pip install -r requirements.txt

# Copy actions folder to working directory
COPY . /app
COPY ./templates /app/templates

ENTRYPOINT ["python"]


CMD ["app.py", "run", "-h", "0.0.0.0", "-p", "5000"]