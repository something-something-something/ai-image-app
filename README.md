# About

A web app that uses [latent diffusion](https://github.com/CompVis/latent-diffusion) to create images. 

Made using latent diffusion, flask, next.js

# Requirements

*	python 3.10.4
*	python-poetry 1.1.13
*	cuda 11.6.1
*	nodejs 17.9.0
*	npm 8.5.5

NOTE: REQUIRES A GRAPHICS CARD WITH LOTS OF MEMORY


# Setup

## Setup backend

### Install dependencies
`cd backend`

`sh setup.sh`

### Download model

Download model from https://github.com/CompVis/latent-diffusion and save it as `backend/modelimg/model.ckpt`

## Setup frontend

`cd frontend`

`npm install`

# Running the project

To run the frontend run 

`sh start-fe.sh`

To run the backend run

`sh start-be.sh`


access the fronten through http://localhost:3000/