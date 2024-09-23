# FROM node:14

# WORKDIR /app

# COPY ./frontend-react/package*.json ./

# RUN npm install

# COPY . .

# EXPOSE 3000

# CMD ["npm", "start"]

FROM node:14
WORKDIR /app
COPY ./frontend-react/package*.json ./
RUN npm install
COPY ./frontend-react/ ./
EXPOSE 3000
CMD ["npm", "start"]
