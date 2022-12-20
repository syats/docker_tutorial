FROM	ubuntu:latest
RUN		apt-get update && apt-get -y install python3 pip curl
WORKDIR	/code
COPY    requirements.txt /code/requirements.txt
RUN		pip install -r requirements.txt 
COPY	./src /code/app

EXPOSE	8080
CMD 	["uvicorn", "app.main:app", "--host", "0.0.0.0"]