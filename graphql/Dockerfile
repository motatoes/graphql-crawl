FROM node:8.16.0-alpine

WORKDIR /app
COPY package.json .
RUN npm install
COPY . .
CMD ["node", "index.js"]
# CMD [ "/bin/sh", "-c", "--" , "while true; do sleep 30; done;"]



