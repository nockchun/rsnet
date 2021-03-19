FROM python

# Install system packages
RUN sed -i 's/archive.ubuntu.com/ftp.harukasan.org/g' /etc/apt/sources.list \
 && apt clean && apt update && apt install -yq --no-install-recommends apt-utils \
    vim net-tools openssh-server sudo cmake python-opengl locales \
 && echo "en_US.UTF-8 UTF-8" > /etc/locale.gen \
 && locale-gen

# Install web service environments
RUN pip install flask pymongo
COPY app /app

# Config server environments
ENV MONGO_USERNAME admin
ENV MONGO_PASSWORD password
ENV MONGO_SERVER mongodb
EXPOSE 5000

# Run Service
WORKDIR /app
CMD ["python", "app.py"]
