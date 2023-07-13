---
title: "Adventures With Docker Multistage Build"
date: 2023-07-11T23:54:15+05:30
# weight: 1
# aliases: ["/first"]
tags: ["docker", "dev-ops"]
author: ["Vibhakar \"Gala\" Solanki"]
showToc: true
TocOpen: false
draft: false
hidemeta: false
comments: false
description: "fascinating world of docker multi stage builds.."
disableShare: false
disableHLJS: true
hideSummary: false
searchHidden: true
ShowReadingTime: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
ShowWordCount: true
ShowRssButtonInSectionTermList: true
UseHugoToc: true
cover:
    image: "img/multi_stage_docker_builds.png" # image path/url
    alt: "docker file showcasing multistage build" # alt text
    caption: "The difference is clear" # display caption under cover
    relative: true # when using page bundles set this to true
    hidden: false # only hide on current single page
editPost:
    URL: "https://github.com/p0lygun/p0lygun.github.io/tree/main/content/blog"
    Text: "Suggest Changes" # edit text
    appendFilePath: true # to append file path to Edit link
---


> I thought damm a lot of users must have uploaded content only to find out that the **docker images were taking up all the space**,  



This week I dived into the fascinating world of multi-stage docker build  
  
## The Problem

In [https://bfportal.gg](https://bfportal.gg) i use a relatively simple stack,  
  
[#wagtail](https://www.linkedin.com/feed/hashtag/?keywords=wagtail&highlightedUpdateUrns=urn%3Ali%3Aactivity%3A7084619263340130304) (a cms that runs on [#django](https://www.linkedin.com/feed/hashtag/?keywords=django&highlightedUpdateUrns=urn%3Ali%3Aactivity%3A7084619263340130304) ) + [#docker](https://www.linkedin.com/feed/hashtag/?keywords=docker&highlightedUpdateUrns=urn%3Ali%3Aactivity%3A7084619263340130304) + [#tailwind](https://www.linkedin.com/feed/hashtag/?keywords=tailwind&highlightedUpdateUrns=urn%3Ali%3Aactivity%3A7084619263340130304).  
  
Then one day I woke up to an alert on [#datadog](https://www.linkedin.com/feed/hashtag/?keywords=datadog&highlightedUpdateUrns=urn%3Ali%3Aactivity%3A7084619263340130304) that almost all of the disk space on the VPS has been used, 

  
so I did an image prune and thought the size of the images must be quite big to fill up all the space  
  
lo and behold it was 2 gigs for each image 💀 ( no wonder my poor VPS was all full )  
  
so I went on looking for how to reduce the size of the image.  
it was docker multi-stage builds,  


{{<details "At this point i had this good ol' dockerfile ( Click to expand ) " >}}

```dockerfile
# Use an official Python runtime based on Debian 10 "buster" as a parent image.
FROM python:3.11-slim-buster as dev

# Add user that will be used in the container.
RUN useradd --create-home wagtail

# Port used by this container to serve HTTP.
EXPOSE 8000

# Set environment variables.
# 1. Force Python stdout and stderr streams to be unbuffered.
# 2. Set PORT variable that is used by Gunicorn. This should match "EXPOSE"
#    command.
ENV PYTHONUNBUFFERED=1 \
    PORT=8000 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="${PATH}:/home/wagtail/.local/bin" \
    USER="wagtail"

# Install system packages required by Wagtail and Django.
RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    build-essential \
    curl \
    libpq-dev \
    libmariadbclient-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libwebp-dev \
    software-properties-common \
    zip \
    unzip \
    git \
    npm \
    && rm -rf /var/lib/apt/lists/* /usr/share/doc /usr/share/man \
    && apt-get clean

RUN npm install npm@8.18.0 -g && \
    npm install n -g && \
    n 18.8.0

# Install the application server.
RUN pip install "gunicorn==20.0.4"

# Install the project requirements.
COPY requirements.txt /
RUN pip install -r /requirements.txt

# Use /app folder as a directory where the source code is stored.
WORKDIR /app

# Set this directory to be owned by the "wagtail" user. This Wagtail project
# uses SQLite, the folder needs to be owned by the user that
# will be writing to the database file.
RUN chown wagtail:wagtail /app

# Copy the source code of the project into the container.
COPY --chown=wagtail:wagtail . .

# Use user "wagtail" to run the build commands below and the server itself.
USER wagtail

FROM dev as final

RUN python manage.py tailwind install --no-input;
RUN python manage.py tailwind build --no-input
RUN python manage.py collectstatic --noinput --clear
```  

{{< /details>}}  
Ugly rht ? 🥲  
Its basically this 

{{< figure src="/tradiational_stack.png" title="A traditional dockerfile"  width="50%"  align="center" >}}


## The Solution
So i started with separating the tools from dependencies, there were two clear things that i can separate,   
1. Python Virtual Environment
2. Node binary  

So i made two separate images for each  

### Python  

In this project i now use `poetry`, so if you want a reliable way to install poetry in a docker image, here you go

```dockerfile
FROM python:3.11-buster as builder
RUN pip install poetry==1.5.1
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1

WORKDIR /venv
RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends git
RUN touch README.md

COPY ["pyproject.toml", "poetry.lock", "./"]
RUN poetry config installer.max-workers 10
RUN poetry install --without dev --no-root --no-cache
```


gave it the name `builder` so that i can later take advantage of  `COPY --from=`, next up was 
### Node

```dockerfile {linenostart=16}
FROM node:latest as node_base
RUN echo "NODE Version:" && node --version
RUN echo "NPM Version:" && npm --version
```  


( PS: why is it so hard to install node in debian images ? making a separate image is sooo much easier )  

Now that we have our base images ready we can take advantage of `multistage` builds  

The docker image is then split into two parts :

- **Dev** is for local development and contains npm and tailwind binaries
- **Final** is for production an i remove the `node_modules` folder from it to save space

( Previously we only had final :x ) 

### dev
```dockerfile {linenostart=20}
FROM python:3.11-slim-buster as dev

WORKDIR /app
RUN useradd --create-home wagtail

# Port used by this container to serve HTTP.
EXPOSE 8000
# Install system packages required by Wagtail and Django.
RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    build-essential \
    libpq-dev \
    libmariadbclient-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libwebp-dev \
    curl \
&& rm -rf /var/lib/apt/lists/*
# Set environment variables.
# 1. Force Python stdout and stderr streams to be unbuffered.
#    command.
ENV PYTHONUNBUFFERED=1 \
    PORT=8000 \
    PYTHONDONTWRITEBYTECODE=1 \
    USER="wagtail" \
    VIRTUAL_ENV=/venv/.venv

ENV PATH="${VIRTUAL_ENV}/bin:${PATH}:/home/wagtail/.local/bin"
COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}


COPY --chown=wagtail:wagtail --from=node_base /usr/local/bin /usr/local/bin
COPY --chown=wagtail:wagtail --from=node_base /usr/local/lib/node_modules/npm /usr/local/lib/node_modules/npm
COPY ./bfportal ./
RUN chown -R wagtail:wagtail /app
USER wagtail
RUN npm install
```


the important lines are `46 - 51` , in these line we take full advantage by copying only the things we need 😁.  

then we finally move onto **final** stage
### Final
```dockerfile {linenostart=61}
FROM dev as final

RUN npx tailwindcss -i ./bfportal/static/src/styles.css  -o ./bfportal/static/css/bfportal.css --minify
RUN python manage.py collectstatic --noinput --clear  -i static/src/*
```

Now by using `buildx` ( `docker buildx build --target=final` ) one day and a few hours of head-scratching later I was able to bring the size of the image down to just **600MB** 😮 .

To my understanding we did this 

{{< figure src="/multi_stage_build.png" title="A Multi Stage Docker Build"  align="center" >}}


now all my CI/CD pipelines for [bfportal.gg](http://bfportal.gg) are super fast  
( it was around 7 mins before, now it's < 3 mins ) all thanks to docker ❤️

## Further Optimizations
- Make use of python-alpine image to have even smaller final image size
	- But [Python=>Speed](https://pythonspeed.com/articles/base-image-python-docker-images/) recommends against it
- Find better way to write file so that we can have less layers and more caching
## Conclusion
- Must use `buildx` for faster build times and better cache
- Copy only the final compiled tools from a base image
- MUST REMOVE `node_modules` IN THE END

All in all I find docker to be a awesome technology :) , Have a good day 

PS : Let me know if you have any ideas how to make it better :), you can find me at discord or twitter (gala_vs)