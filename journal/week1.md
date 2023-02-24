# Week 1 — App Containerization

### Pariticipated in live session
### Completed all videos for this week
### Completed the quiz for security and spend

# Stretch Homework

### 1) Run the Dockerfile command as external script
        **Tried both options 
            1) Script with docker build command and executing the script to build a docker image
            2) Run a script from Dockerfile
### 2) Push and tag a image to DockerHub
            1) Image is tagged first
            2) Post tag completion image is pushed to dockerhub (samba73/script-sample)
### 3) Use multi-stage building for a Dockerfile build
            1) First single stage build was done (react-js) and noted the size of image to be 1.19GB
            2) Created another dockerfile (Dockerfile-ms) with stage 0 and stage 1 and noted the size of image to be 144MB
                i) Built the  react-js app in stage 0
                ii) used nginx server in stage 1 and moved the build to nginx server
                iii) nginx server configuration is updated to listen to port 3000 (react-js)
            3) Was able to launch the frontend page in web browser
            4) Did exec to container and checked the build files in /usr/share/nginx/html folder to confirm
### 4) Tried healthcheck in docker compose for nginx but always give unheathy even though healthcheck provided was for existence of index.html file which was always available
              version: "3.8"
              services:
              ....
                frontend-react-js:
                  ...
                  build: 
                    context: ./frontend-react-js
                    dockerfile: Dockerfile-ms
                  ...   
                  healthcheck:
                    test: stat /usr/share/ngix/html/index.html || exit 1
                    interval: 30s
                    start_period: 10s
                    retries: 2
                    timeout: 5s
### 5) Dockerfile best practices
              1) Multistage option (demonstrated in homework 3
              2) Docker build through stdin
                     docker build -<<EOF
                     FROM busybox
                     RUN echo "Hello World"
              3) Docker build without sending build context
                      docker build -t img1:latest -<<EOF
                     FROM busybox
                     RUN echo "Hello World"
                     EOF
### 6) Run docker locally and build same images
              1) Unable to resolve the Docker daemon at /var/run/docker.sock error to run docker client
              tried many help by google but unable to resolve. Need to deep dive into it
### 7) Run docker container in EC2
              1) Created a new EC2 with ubuntu 20
              2) Installed docker
              3) Ran container docker run busyvbox echo hello world
              4) The container ran and displayed hello world
