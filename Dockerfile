FROM python:3.7

COPY . /tmp
WORKDIR /tmp
RUN mkdir /tmp/output

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

CMD make run