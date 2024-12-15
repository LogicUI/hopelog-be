#!/bin/bash

docker build -t hopelogdev . # hopelogdev is the image name

docker run -it --rm -v $(pwd)/app:/app -p 5000:5000 hopelogdev # hopelogdev is the image name