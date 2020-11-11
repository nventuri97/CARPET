#set base image
FROM python:3.6.9

#set working directory in the container
WORKDIR /code

# copy the dependencies file to the working directory
COPY ./requirements.txt .

#install dependecies
RUN pip install -r requirements.txt

EXPOSE 4443

# copy the content of the local src directory to the working directory
COPY ./src .

# command to run on container start
CMD ["python", "./client.py"]