# DockerCourse
## Project Structure
```
├─.github/: 
│   └── workflows/: Contains GitHub Actions workflows.
│       └── ci.yml: GitHub Actions CD workflow.
├─ api/: Contains the API implementation.
├─ chat/: Contains the chat implementation.
├─ db/: Contains the database implementation.
├─ store/: Contains the store implementation.
├─ .gitignore: Git ignore file.
├─ README.md: Project documentation.
├─ DockerFileBad: Dockerfile with some bad practices.
├─ DockerFileGood: The same DockerFile, but with fixed bad practices.
├─ main.py : Main file to run the application.
├─ requirements.txt: Python requirements file.
```
## Branching Strategy
There is a separate branch for each homework, which is named `hw<number>`.
(for example, the branch for homework 1 is `hw1`) and is merged into main by pull request.

## Getting Started
### HW 1
For remote checking, you can examine the project files and the pipeline CD to make sure that the containers are 
running and working correctly.

For local verification:
1. Clone the repo.
2. Change the directory to the project root.
    ```bash
    cd /path/to/DockerCourse
    ```
3. Create and fill .env file with the following content:
    ```bash
    DATABASE_URL=postgresql://shop_admin:111111@db:5432/shop_db
    ```
4. Create docker network:
    ```bash
    docker network create api_container
    ```
5. Build and run several containers using the following commands:
    **Postgres**
   - build and run
    ```bash
     docker run -d --name db --network api_container -e POSTGRES_DB=shop_db -e POSTGRES_USER=shop_admin -e POSTGRES_PASSWORD=111111 -v pgdata:/var/lib/postgresql/data_db_contaier postgres:latest
   ```
   **Good Container API**
   - build
   ```bash
   docker build -t shop_api_good -f DockerFileGood .
   ```
   - run
   ```bash
   docker run -d --name shop_api_good_container --network api_container -p 8080:8000 -v shop_api_volume:/api_data shop_api_good
   ```
   **Bad Container API**
   - build
   ```bash
   docker build -t shop_api_bad -f DockerFileGood .
   ```
   - run
   ```bash
   docker run -d --name shop_api_bad_container --network api_container -p 8000:8000 -v shop_api_volume:/api_data shop_api_bad
   ```
6. Test API by SWAGGER UI:
    - Open the following link in your browser and test the API by sending requests to the server:
    ```
    http://localhost:8080/docs
    ```
   for the good container and
    ```
    http://localhost:8000/docs
    ```
   for the bad container.