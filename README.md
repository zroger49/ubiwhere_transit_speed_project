# Traffic Monitoring System

This project implement ubiwhere interview challenge.

A Django-based platform to monitor vehicle traffic across road segments using sensor. 
Sensors report license plate sightings in bulk via authenticated API requests. 


## Features

- Register road segments.
- Register speed readings for a road segment. Dynamicaly assing traffic intensity
- Filter road segments by latest traffic intensity.
- Accept bulk vehicle passage reports from mobile sensors.
- Filters passages of vevehicle based on plate number


## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/zroger49/ubiwhere_transit_speed_project/
cd ubiwhere_transit_speed_project
```

### 2. Run Docker-Compose

```bash
docker-compose up
```

This step will build the Docker images and start the containers for the Django application. The data to be imported is in "data" folder.

### Testing: 

Postman requests for testing all the endpoints are available at project_traffict_monitor.postman_collection.json