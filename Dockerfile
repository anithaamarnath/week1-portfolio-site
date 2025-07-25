# FROM quay.io/centos/centos:stream9

# RUN dnf install -y python3.9 python3-pip

# WORKDIR /week1-porfolio-site

# COPY . .

# RUN pip3 install -r requirements.txt

# CMD [ "flask", "run", "--host=0.0.0.0"]


# EXPOSE 5000


FROM python:3.9-slim-buster

WORKDIR /week1-portfolio-site

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .

CMD ["flask", "run", "--host=0.0.0.0"]

EXPOSE 5000