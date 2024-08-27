FROM python:3.9

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy requirements.txt (if you have one) and install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Step 2: Install Node.js and Serverless
FROM node:18-slim AS node-base

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the package.json and package-lock.json (if available)
COPY package*.json ./

# Install serverless and other dependencies
RUN npm install

# Install serverless globally (optional, if you want to run serverless commands globally)
RUN npm install -g serverless

# Copy the rest of your application
COPY . .

# Copy the installed Python dependencies from the first stage
COPY --from=python-base /usr/local/lib/python3.11 /usr/local/lib/python3.11

# Expose the port that the serverless offline runs on (default is 3000)
EXPOSE 3000

# Set the default command to run serverless offline
CMD ["./node_modules/.bin/serverless", "offline", "start"]
