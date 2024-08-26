# Outdoor_Cattle_Tracking_LoRaWAN
This repository contains the code made by Simon BEUREL during the project "Outdoor Cattle Tracking LoRaWAN" at the DNIIT. 
## Repository's architecture :
### Card_Cattle : 
This folder contains the code for the card that will be attached to the cattle. The card is also linked to an accelerometer, with the goal of detecting the cattle's activity.
### docs :
This repository is used for stock some useful documents which could help you to understand the project.
### Python_scripts : 
This folder contains the code for a python script which is calling Chirpstack's API, parse all the data and then run a Flask server which is an API for external applications like Grafana.
## Dockerhub :
To be sure that the project will work on every computer, I made some docker images which are available on Dockerhub. Here is the list of the images :
- [Python Application](https://hub.docker.com/repository/docker/simonbeurel/python_application_vietnam/general): simonbeurel/python_application_vietnam
- [Grafana image with specific plugins](https://hub.docker.com/repository/docker/simonbeurel/grafana_vietnam/general): simonbeurel/grafana_vietnam
## How to launch the project on your own computer : 
First of all, you need to install docker and docker-compose on your computer. It will be really useful to launch the project because there are already some docker images ready in Dockerhub. You have also to be sure that the 3010 port and the 8080 port is open and not used by another application. 
Then, you have to do the following steps :
1. Clone the repository
```bash
git clone https://github.com/vanlictran/2024internshipCattleTracking/tree/main
```
2. Be sure docker is running on your computer
3. Make the following command in the root folder of the project : 
```bash
docker-compose up -d --build
```
4. Wait for the docker images to be downloaded and the containers to be launched
5. Go to your browser and type the following URL : http://localhost:3010
6. You should see the Grafana interface. You can connect with the following credentials : 
```bash
username: admin
password: admin
```
## DNIIT's server :
If you want to use the DNIIT's server, you have nothing to do because the project is already working on the server. You can access the Grafana interface with the following URL : http://10.196.160.77:3010/d/bdqemgkdymcqoe/vietnam-internship?orgId=1&refresh=1m

Please be sure to be connected to the DNIIT's VPN to access the server.
## What's next ?
Here is a list of smalls features which could be added to the project later of someone wants to continue the project :
- Add a GPS module to the card to have the cattle's position instead of use RSSI signal which is too complicated
- Add a temperature sensor to the card to have the cattle's temperature
- Build a central website for every farmer to see their cattle's activity instead of one grafana interface for each farmer