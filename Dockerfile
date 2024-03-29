FROM python:3.8

WORKDIR /app

# Copy the environment.yaml file to the working directory, install conda and create env based on yaml
COPY environment.yaml .

RUN apt-get update && \
    apt-get install -y wget && \
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh && \
    bash Miniconda3-latest-Linux-x86_64.sh -b -p /opt/conda && \
    rm Miniconda3-latest-Linux-x86_64.sh && \
    /opt/conda/bin/conda env create -f environment.yaml

# Activate the Conda environment
RUN echo "source activate $(head -1 environment.yaml | cut -d' ' -f2)" >> ~/.bashrc
ENV PATH /opt/conda/envs/$(head -1 environment.yaml | cut -d' ' -f2)/bin:$PATH

COPY . .

CMD ["python", "main.py"]