# nomopai-GPT

This repository contains a FastAPI & Langchain based nomopai-GPT application.

## Instructions

### 1. Git Clone Repository
Clone this repository to your local machine using the following command:
```
git clone https://github.com/Innayy/generative.git
```

### 2. Run Application with Docker

To run the application using Docker, follow these steps:

1. Make sure you have Docker installed on your machine. If not, download and install Docker from [here](https://www.docker.com/get-started).

2. Navigate to the cloned repository directory:
   ```
   cd <repository_directory>
   ```
   Replace `<repository_directory>` with the directory path where the repository is cloned.

3. Change env.test file to .env and update API_KEY and OPENAI_API_KEY in env file.

4. Build the Docker image for the application. Run the following command:
   ```
   docker build -t nomopai-gpt .
   ```

5. Once the image is built successfully, you can start the container with the following command:
   ```
   docker run -d -p 8000:8000 nomopai-gpt
   ```
   This command will run the container in detached mode (`-d`) and map port `8000` on your local machine to port `8000` inside the container.

6. Access the application in your browser or using tools like cURL or Postman:
   ```
   http://localhost:8000/
   ```
   You should see the application running successfully.

7. Access the API docs using:
   ```
   http://localhost:8000/docs
   ```
   You should see the list of APIs.

## Additional Notes

- If you need to stop the running Docker container, you can use the following command:
  ```
  docker stop <container_id>
  ```
  Replace `<container_id>` with the ID of the running container. You can get the container ID by running `docker ps`.
