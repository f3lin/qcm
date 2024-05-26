# Dockerfile to build a FastAPI and Angular App
#   - Ubuntu 22.04
#   - Python 3
#   - Pip 3
#   - Oh-My-Posh
#   - NodeJs 20.13.1 and Angular Cli via .devcontainer file
###############################################

FROM ubuntu:22.04

# Set environment variables
ENV DEBIAN_FRONTEND noninteractive

# Update packages and install necessary dependencies
RUN apt-get update && \
    apt-get install -y \
    python3 \
    python3-pip \
    curl \
    git \
    unzip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Downloading and installing Oh My Posh
RUN bash -c "$(curl -fsSL https://ohmyposh.dev/install.sh)"

# Download Oh My Posh's “Bubbles” theme from the my GitHub repository
RUN curl -fsSL -o /root/dev-remote.omp.yaml https://raw.githubusercontent.com/f3lin/my-terminal/main/themes/dev-remote.omp.yaml

# Configuring the Bash shell to use Oh My Posh
RUN echo 'eval "$(oh-my-posh --init --shell bash --config /root/dev-remote.omp.yaml)"' >> ~/.bashrc

# Set up a directory for your FastAPI and Angular App
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install FastAPI dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Set the entry point and default command to start FastAPI
WORKDIR /app

# Default command for starting the Bash shell
CMD ["/bin/bash"]