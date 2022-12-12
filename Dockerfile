FROM python:3.10-slim 

WORKDIR /docker-flask-dir
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# copy the rest of the files
COPY . .

RUN chmod +x bootstrap.sh
CMD ["/bin/bash", "bootstrap.sh"]