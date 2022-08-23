# About

A web app that uses [stable-diffusion](https://github.com/CompVis/stable-diffusion) or [latent diffusion](https://github.com/CompVis/latent-diffusion) to create images. 

Made using latent diffusion, flask, next.js, and [diffusers](https://github.com/huggingface/diffusers)

# Requirements

TODO

# Setup

## Setup backend

### Install dependencies
`cd backend`

`poetry install`

### Download the model

https://huggingface.co/CompVis/stable-diffusion-v1-4

Clone it and link it like so

`ln -s /wherever/you/cloned/stable-diffusion-v1-4/ backend/models/stable-diffusion-v1-4`

## Setup frontend

`cd frontend`

`npm ci`

# Running the project

To run the frontend run 

`sh start-fe.sh`

To run the backend run

`sh start-be.sh`


access the frontend through http://localhost:3000/