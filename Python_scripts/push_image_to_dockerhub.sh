#!/bin/bash
docker login
docker tag docker_api_chirpstack simonbeurel/python_application:latest
docker push simonbeurel/python_application:latest

