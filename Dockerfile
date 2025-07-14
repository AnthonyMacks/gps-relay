# 🟦 Use Node.js base image (if you still need it)
FROM node:18

# 🧰 Install Python (minimal)
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    pip3 install flask requests

# 📁 Set working directory
WORKDIR /app

# 📦 Install Node dependencies (optional if index.js is used)
COPY package*.json ./
RUN npm install

# 🔁 Copy all app files (including gps-relay.py)
COPY . .

# 🌐 Expose relay port
EXPOSE 3000

# 🚀 Start the Python GPS relay
CMD ["python3", "gps-relay.py"]
