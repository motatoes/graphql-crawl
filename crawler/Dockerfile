FROM python:3.7  

# RUN apk update && apk add --virtual build-dependencies build-base gcc 

RUN pip install scrapy scrapyrt bs4 pymongo

WORKDIR /app

# run a fictional daemon process
CMD ["scrapyrt", "-p", "9901"]
# CMD [ "/bin/bash", "-c", "--" , "while true; do sleep 30; done;"]
