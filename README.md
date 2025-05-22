# Traffic Monitoring System

This project implement ubiwhere interview challenge.

A Django-based platform to monitor vehicle traffic across road segments using sensor. 
Sensors report license plate sightings in bulk via authenticated API requests. 


## Features

- Register and annotate road segments.
- Record vehicle speed readings per segment.
- Accept bulk vehicle passage reports from mobile sensors.
- Filter road segments by latest traffic intensity.

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

