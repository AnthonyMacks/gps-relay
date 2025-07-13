<<<<<<< HEAD
# Use Node.js base image
FROM node:18

# Set working directory
WORKDIR /app

# Copy everything
COPY . .

# Install dependencies
RUN npm install

# Expose the port
EXPOSE 3000

# Run the server
=======
# Use Node.js base image
FROM node:18

# Set working directory
WORKDIR /app

# Copy everything
COPY . .

# Install dependencies
RUN npm install

# Expose the port
EXPOSE 3000

# Run the server
>>>>>>> 6ea2398 (Initial project setup with relay, map, worker, and supporting files)
CMD ["node", "index.js"]