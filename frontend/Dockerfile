
FROM node:lts-trixie

WORKDIR /frontend

COPY ./frontend /frontend
RUN npm install

CMD ["npm", "run", "dev","--", "--host"] 
