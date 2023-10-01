all: build-base-docker

build-base-docker:
	docker build -t alphaweb3:latest .

run-docker:
	docker run -d --name alphaweb3 -p 17861:7861  alphaweb3:latest