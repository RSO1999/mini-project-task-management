# mini-project-team-5


You will need to install docker, postgresql, python, and django.


I'm on Linux, I can help you if you're on a Linux Machine.

If your on Mac, use brew for installing stuff, it's basically Linux

If your Windows, use WSL to emulate Linux if you want to mimic my setup, otherwise you should figure out how to install everything on windows.

Watch the youtube vid, up until he starts configuring the DB. That's where I stopped since we need to use Postgres.
https://www.youtube.com/watch?v=nGIg40xs9e4&t=962s

For Docker, read documentation, watch youtube. As long as you know what an Image and a Container are, you should be good to go.

Docker is pretty complex, we need to decide how we want the db to look before I can finish configuring the container, but rn it's able to run a fresh database. We will need to decide our schema soon.


Once you install docker, if you want to spin up the db use this:


```
$ docker pull postgres
```
This will pull the postgres image from postgres' website, stored magically on ur computer

From your root directory, run this:

```
$ docker build -t mini1-postgres-image .
```
This builds the IMAGE for the db, called 'mini1-postgres-image'

```
$ docker run --name miniproject1-postgres-container -d -p 2202:5432 mini1-postgres-image
```
This will RUN the IMAGE in a CONTAINER. This will spin up the DB on localhost:2022 on a container called miniproject1-postgres-container

TO TEST IF THE DB IS RUNNING

```
$ docker logs miniproject1-postgres-container
```
this will give the logs from the container


```
$ docker exec -it miniproject1-postgres-container    
```
this lets you "ssh" into the container when its running. Not really ssh but its close enough.

```
$ psql -h localhost -p 2202 -U postgres 
```
once you have postgres installed, this will try and connect you to the database (on localhost port 2202), if you can get in congrats! you did it. Your database is up.

NOTE: Data is NOT permanent in the DB yet. Once you stop the container, it will refresh the db's data. Still looking into a volume for that.

Once the DB is configured, I can make the docker process a simple shellscript.

-Alex
