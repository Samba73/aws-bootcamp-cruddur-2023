# Week 1 — App Containerization

## Pariticipated in live session
## Completed all videos for this week
## Completed the quiz for security and spend

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
