
FROM node:lts-trixie

WORKDIR /frontend

COPY package.json package-lock.json ./
RUN npm install

COPY . .
CMD ["npm", "run", "dev","--", "--host"] 
