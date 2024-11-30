## HOW TO USE WITH DOCKER

### 1. Build the image

```bash
# Build the image
docker build -t background-removal-app .
```

# Then run your container with the command

```bash

docker run -d \
  -p 5000:5000 \
  -v $(pwd)/inputs:/app/inputs \
  -v $(pwd)/outputs:/app/outputs \
  -e FLASK_APP=main.py \
  -e SERVER_BASE_URL=http://localhost:5000 \
  --name background-removal-service \
  background-removal-app

```
