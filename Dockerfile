FROM python:3.10
WORKDIR /app
COPY . .
RUN pip3 install -r requirements.txt
RUN apt update
RUN apt-get install ffmpeg libsm6 libxext6 libgl1-mesa-glx -y
RUN apt-get install libqt5gui5 -y