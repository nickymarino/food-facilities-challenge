.PHONY: help install docs

IMAGE_NAME = marino-nicky-food-facilities-challenge

help:  ## Show this help.
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

build:  ## Build a Docker image of this project
	docker build -t $(IMAGE_NAME):latest .

run:  ## Run the Docker image of this project
	docker run -p 80:80 $(IMAGE_NAME):latest

dev:  ## Run a local dev version of this project
	uvicorn app.main:app --reload

# install:  ## Installs this package locally for your current Python environment
# 	pip3 install -r requirements.txt

# docs:  ## Builds the documentation and opens it in your default browser
# 	@cd docs && make html && open _build/html/index.html

# test:  ## Run the test suite
# 	pytest