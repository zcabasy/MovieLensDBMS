<h1 align="center">Database and Information Systems COMP0022</h1>
<h3 align="center">Group 1</h3>
<p align="center">Ali Reyazat<br>Mohammad Syed<br>Karan Chawla<br>Dylan Hoi</p>

## Deployment Guide

You will need to have [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/) installed.

1. Clone this repository.
    ```bash
    git clone https://github.com/zcabasy/MovieLensDBMS
    ```

2. Navigate into the directory containg the [Flask](https://flask.palletsprojects.com/en/2.0.x/) project.
    ```bash
    cd MovieLensDBMS/webapp
    ```

3. Build the Docker image.
    ```bash
    docker-compose build
    ```
    > This may take several minutes.

4. Deploy the containers.
    ```bash
    docker-compose up
    ```
    > Please wait for the output of this command to stop and stabilise before moving on to the next step as you may expereince an error otherwise. This command may take several minutes before it stabilises.

5. Access the website on [localhost:5001](http://localhost:5001/).
6. To stop the server, interrupt the process initiated by step 4 by pressing `Ctrl+C`.
7. Stop the containers.
   ```bash
   docker-compose down
   ```