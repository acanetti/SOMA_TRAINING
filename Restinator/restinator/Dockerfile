FROM python:3.10
RUN apt-get update -y 
# We copy just the requirements.txt first to leverage Docker cache
COPY requirements.txt /tmp/ 
# fichier destination
WORKDIR /restinator
RUN pip install --upgrade pip
RUN pip install -r /tmp/requirements.txt

COPY . /restinator/

EXPOSE 3838

CMD [ "python3","run.py"]

# docker build -t <nom image> -f Dockerfile .
# docker run -d -p 8888:8787 <nom image>
