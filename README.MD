**Log Analyzer**

Run in docker:
`docker-compose up`

Check admin interface at 0.0.0.0:8000/admin , login `admin`, password `pass` 

Download and save log file:
`docker exec -it <container_name> ./manage.py download_log  http://www.almhuette-raith.at/apache-log/access.log`

Show stats:
`docker exec -it <container_name> ./manage.py get_stats`

Run tests in docker:
`docker exec -it <container_name> ./manage.py test`
