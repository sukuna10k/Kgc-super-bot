FROM python:3.10

RUN apt update && apt upgrade -y
RUN apt install git -y && apt install mediainfo -y && apt install ffmpeg -y
COPY requirements.txt /requirements.txt

RUN cd /
RUN pip3 install -r requirements.txt
RUN mkdir /YasirBot
WORKDIR /YasirBot
COPY start.sh /start.sh
CMD ["/bin/bash", "/start.sh"]
