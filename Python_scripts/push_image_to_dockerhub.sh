#!/bin/bash
docker login
docker tag docker_api_chirpstack simonbeurel/python_application_vietnam:latest
docker push simonbeurel/python_application_vietnam:latest

