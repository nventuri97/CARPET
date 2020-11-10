#set base image
FROM python:3.6.9

#set working directory in the container
WORKDIR /code

# copy the dependencies file to the working directory
COPY ./ClientDoc/requirements.txt .

#install dependecies
RUN pip install -r requirements.txt

# copy the content of the local src directory to the working directory
COPY ./src/Client/ .

# command to run on container start
CMD ["python", "./client.py"]