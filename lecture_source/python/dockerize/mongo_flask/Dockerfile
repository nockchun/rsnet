FROM python

RUN pip install flask pymongo
COPY app /app

ENV MONGO_USERNAME admin
ENV MONGO_PASSWORD password
ENV MONGO_SERVER mongodb
EXPOSE 5000

WORKDIR /app
CMD ["python", "app.py"]
