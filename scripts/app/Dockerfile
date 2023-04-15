FROM alpine:latest
RUN apk add --no-cache python3 py3-pip

ADD requirements.txt ./

ARG DB_HOST=127.0.0.1
ENV DB_HOST=$DB_HOST

EXPOSE 8081 8082
RUN pip install -r requirements.txt
ENTRYPOINT [ "python", "src/main.py" ]
