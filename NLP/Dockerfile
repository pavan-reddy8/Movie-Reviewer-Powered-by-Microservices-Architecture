#Pull base image
FROM ubuntu:18.04

#Update gnu and install python3-pip
RUN apt update; apt install -y gnupg2
RUN apt install -y python3-pip
RUN python3 -m pip install --upgrade pip
#Move requiremnets to docker app path
COPY ./requirements.txt /app/requirements.txt

#Change working directory
WORKDIR /app

#Install flask apps
RUN pip3 install -r requirements.txt

#Copy content to app
COPY . /app
#RUN export GOOGLE_APPLICATION_CREDENTIALS="rapid-pottery-303217-08b9580fdd45.json"

#Set ENTRYPOINT as python3
ENTRYPOINT ["sh"]

#Run application
CMD ["run.sh"]