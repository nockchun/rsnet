FROM continuumio/miniconda3
LABEL maintainer="nockchun <nockchun@gmail.com>"

ARG PYTHONVENV=app
ARG PYTHONVERSION=3.9
RUN conda update -n base conda
RUN conda install -n base -c conda-forge tini uvicorn fastapi apscheduler

WORKDIR /app/
EXPOSE 5000

RUN ["tini", "-g", "--"]