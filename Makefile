.PHONY: help install docs

IMAGE_NAME = marino-nicky-food-facilities-challenge

help:  ## Show this help.
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

build:  ## Build a Docker image of this project
	docker build -t $(IMAGE_NAME):latest .

run:  ## Run the Docker image of this project
	docker run -p 80:80 $(IMAGE_NAME):latest

install:  ## Installs this package for local dev and testing
	pip3 install -r requirements.dev.txt

dev:  ## Run a local dev version of this project
	uvicorn app.main:app --reload

test:  ## Run the test suite
	pytest
