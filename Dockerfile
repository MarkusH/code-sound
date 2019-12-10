FROM python:3.8-buster

RUN apt-get update -y \
    && apt-get install -y sox libasound2-dev
WORKDIR /src
COPY setup.py /src/
COPY code_sound /src/code_sound
RUN pip install .

CMD ["/usr/local/bin/run-action"]
