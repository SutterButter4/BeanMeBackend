#Create a ubuntu base image with python 3 installed.
FROM python:3.8

RUN apt-get -y update

#Set the working directory
WORKDIR /usr/src/app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

#copy all the files
COPY . .

#Install the dependencies

#Expose the required port
EXPOSE 80

#Run the command
CMD ["python3", "./app.py"]