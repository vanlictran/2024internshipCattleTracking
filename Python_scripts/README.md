# Python_scripts
This part of the project is about the code which is used to implement a web application which requests data from Chirpstack, parse it, and then make it available through a REST API (using Flask).
## Architecture:
### requirements.txt
Useful file if you want to launch the retrieve_data_from_chirpstack.py script. It contains all the libraries needed to run the script. You can install them by running the following command:
```bash
pip install -r requirements.txt
```
There is only two libraries in this file:
- requests
- Flask
### retrieve_data_from_chirpstack.py
It's the main script (and the only one) of the project. It's a script which requests data from Chirpstack, parse it, and then make it available through a REST API (using Flask). He is composed of two parts:
- The first part is requesting data from Chirpstack. It's a simple GET request to the Chirpstack API. The data is then parsed to keep only the useful information.
- The second part is the REST API. It's a simple API which returns the data requested by the user. The API is composed of many routes:
  - /states: returns the states of the cows (IMMOBILE, EATING, MOVING, etc.)
  - /card_active: returns the number of active cards
  - /card_inactive: returns the number of inactive cards
  - /last_date: returns the last date of the data
  - /geomap: returns the geolocation of the cows
### Dockerfile
This file is used to build the Docker image of the project. It's a simple Dockerfile which uses the official Python image as a base image. It installs the libraries needed to run the script and then copy the script into the image. The Dockerfile also exposes the port 5000 (the port used by the Flask server).
### launch_docker.sh & push_image_to_dockerhub.sh
These two scripts are used to build the Docker image and run it. The first script builds the Docker image and then runs it. The second script pushes the Docker image to DockerHub. You can run the first script by running the following command:
```bash
./launch_docker.sh
```
You can run the second script by running the following command:
```bash
./push_image_to_dockerhub.sh
```
## How to use it:
For launching the script, first you need to be sure that the port 5000 is not used. Then you can run the following command:
```bash
python3 retrieve_data_from_chirpstack.py
```
or 
```bash
./launch_docker.sh
```
Then you can access the API by going to the following URL: http://localhost:5000/. You can access the different routes by adding the route name to the URL. For example, to access the states of the cows, you can go to the following URL: http://localhost:5000/states.
