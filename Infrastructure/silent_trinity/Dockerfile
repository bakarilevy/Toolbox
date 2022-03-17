# ~/SILENTTRINITY/Dockerfile
# Base Docker image with binaries for Python 3.7
FROM python:stretch-slim-3.7

# Install git, make, and gcc
RUN apt-get update && apt-get install -y git make gcc

# Download SILENTTRINITY
RUN git clone https://github.com/byt3bl33d3r/SILENTTRINITY/ /root/st/
WORKDIR /root/st/

# Install Python Requirements
RUN python3 -m pip install -r requirements.txt

# Inform Docker we need to bind port 5000
EXPOSE 5000

# Entrypoint runs command on container start
ENTRYPOINT ["python3","teamserver.py","0.0.0.0","password"]