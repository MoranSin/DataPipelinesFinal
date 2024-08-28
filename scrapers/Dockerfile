FROM public.ecr.aws/lambda/python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any necessary dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables
ARG SCHEDULER_NAME
ENV SCHEDULER_NAME=${SCHEDULER_NAME}

# Command to run the chosen scheduler
CMD ["sh", "-c", "exec python -m ${SCHEDULER_NAME}"]