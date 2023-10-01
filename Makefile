all: build-base-docker

build-base-docker:
	docker build -t alphaweb3:latest .
