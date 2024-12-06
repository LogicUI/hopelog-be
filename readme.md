
## How to Run

1. Clone the Repository

```bash
 git clone <repository-url>
 cd <repository-folder>
```

2. Build the Docker Image

```bash
docker build -t build-with-ai-hackaton-be .

```
- The -t build-with-ai-hackaton-be assigns a tag (build-with-ai-hackaton-be) to the image.

- The . specifies the context (current directory) where the Dockerfile is located.

3. Run the Docker Container

```bash 
docker run -p 5000:5000 build-with-ai-hackaton-be
``` 
- The -p 5000:5000 maps port 5000 on your local machine to port 5000 in the container.
- The app will be accessible at http://localhost:5000.

4. Verify the Application
You can test the endpoints in your browser or using a tool like curl:

```bash 
curl http://localhost:5000/
```

```json 
{"message": "Welcome to the ECS Flask App!"}
```

```bash 
curl http://localhost:5000/health
``` 

```json 
{"status": "healthy"}
```

Additional Notes
Stopping the Container
To stop the running container, press CTRL+C in the terminal where it is running.

Alternatively, list all running containers and stop the specific one:

```bash 
docker ps
docker stop <container-id>
```

Removing the Image
If you want to delete the Docker image, run:

```bash 
docker rmi build-with-ai-hackaton-be
```

## Troubleshooting
Port Already in Use
If port 5000 is already being used, modify the run command to use a different host port:

```bash 
docker run -p 8080:5000 build-with-ai-hackaton-be
```

