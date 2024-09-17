# mini-project-team-5


You will need to install docker, postgresql, python, and django.


I'm on Linux, I can help you if you're on a Linux Machine.

If your on Mac, use brew for installing stuff, it's basically Linux

If your Windows, use WSL to emulate Linux if you want to mimic my setup, otherwise you should figure out how to install everything on windows.

UPDATE:

Now both the django app and the database are DOCKERIZED, meaning that both will run in containers, which is good!

If this is your first time setting up the new docker environment, remove ALL old containers, volumes, and images, as they are just taking up space. And Make sure NO CONTAINERS ARE RUNNING.

You can see running containers with:

```
$ docker ps
```
Once you have cleaned out your old containers, run ./spinup.sh from the root directory (mini-project-team-5)
This will perform a fresh setup of the dev environment.

In order to test your app now, you will need to spin up the containers each time instead of just running the app.

Read the script line by line, there may be situations where you want to just perform a single step of the setup (like starting the app again because you changed your code, but keeping the database the same)




