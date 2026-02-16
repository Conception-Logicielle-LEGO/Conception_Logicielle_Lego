
FROM node:lts-trixie
WORKDIR /app

COPY package.json package-lock.json ./frontend
RUN npm install

COPY . .
CMD ["npm", "run", "dev","--", "--host"] 
