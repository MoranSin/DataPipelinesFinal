# First Stage: Build Python dependencies
FROM python:3.11 AS python-base

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy requirements.txt and install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Second Stage: Install Node.js and Serverless
FROM node:18-slim AS node-base

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the package.json and package-lock.json and install dependencies
COPY package*.json ./

# Install serverless and other Node.js dependencies
RUN npm install

# Install serverless globally (if needed)
RUN npm install -g serverless

# Copy the rest of your application code
COPY . .


# Copy the installed Python dependencies from the first stage
COPY --from=python-base /usr/local/lib/python3.11 /usr/local/lib/python3.11

# Expose the port that the serverless offline runs on (default is 3000)
EXPOSE 3000

# Set the default command to run serverless offline
CMD ["serverless", "offline", "start"]
