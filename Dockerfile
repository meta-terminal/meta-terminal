FROM node:20-alpine
WORKDIR /app
COPY . .
RUN npm install
RUN chmod +x run.js
CMD ["node", "run.js"]
