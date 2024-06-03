# Use the official Python base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the Python dependencies
RUN pip install -r requirements.txt

# Copy the application code to the working directory
COPY . .

# Expose the port on which the application will run
EXPOSE 8888

# Set environment variables
ARG PRODUCTION
ARG SUPABASE_URL
ARG SUPABASE_KEY

ARG CL_CLOUDNAME
ARG CL_APIKEY
ARG CL_APISECRET
ARG CL_PRESET

ARG AUTH_BE

# set environment variables
ENV PRODUCTION=${PRODUCTION}

ENV SUPABASE_URL=${SUPABASE_URL}
ENV SUPABASE_KEY=${SUPABASE_KEY}

ENV CL_CLOUDNAME=${CL_CLOUDNAME}
ENV CL_APIKEY=${CL_APIKEY}
ENV CL_APISECRET=${CL_APISECRET}
ENV CL_PRESET=${CL_PRESET}

ENV AUTH_BE=${AUTH_BE}


CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8888"]