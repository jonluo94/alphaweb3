all: build-base-docker

build-base-docker:
	docker build -t alphaweb3:latest .

run-docker:
	docker run -d --name alphaweb3 -p 17861:7861 -v /root/alphaweb3/token:/usr/local/alphaweb3/token alphaweb3:latest