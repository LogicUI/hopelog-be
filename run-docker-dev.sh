#!/bin/bash
docker build -t build-with-ai-hackaton-be .

# Run the container
docker run -p 5050:5050 build-with-ai-hackaton-be