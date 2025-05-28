# web/gui/react/Dockerfile
FROM node:22.1.0

WORKDIR /web

# Copy Package & Install Package
COPY package*.json ./
RUN npm install

# Copy All to Docker
COPY . .

# ( + ) Set Port
ENV PORT=1000

# Run Web in Docker
CMD ["npm", "start"]
