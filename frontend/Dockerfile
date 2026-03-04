
FROM node:lts-trixie

WORKDIR /frontend

COPY . .
RUN npm install

CMD ["npm", "run", "dev","--", "--host"] 
