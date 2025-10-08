FROM node:20

WORKDIR /app

# Install dependencies
COPY package.json package-lock.json* ./
RUN npm install

# Copy source code
COPY public/ ./public
COPY src/ ./src

# Expose React dev server
EXPOSE 3000

# Start React app
CMD ["npm", "start"]
