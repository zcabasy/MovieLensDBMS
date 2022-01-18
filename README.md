<h1 align="center">Database and Information Systems COMP0022</h1>
<h3 align="center">Group 1</h3>
<p align="center">Ali Reyazat<br>Mohammad Syed<br>Karan Chawla<br>Dylan Hoi</p>

## Deployment Guide

```
$ cd webapp
$ docker-compose build
$ docker-compose up -d
```

To log in to bash terminal of the SQL container run:
```
$ docker exec -it mariadb bash
```

Once in the container's bash terminal, the MySQL shell can be run using:
```
$ mysql -uroot -ppassword
```