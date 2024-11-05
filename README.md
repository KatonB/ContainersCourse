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
   docker build -t shop_api_bad -f DockerFileBad .
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

❗ Обратите внимание, что плохие и хорошие практики описаны внутри соответствующих DockerFileBad и DockerFileGood.

#### Доп. вопросы:
1. **Когда не стоит использовать контейнеры. Приведите 2 примера.** \
Ответ: Первый вариант - если приложению необходим доступ к железу, например, к видеокарте, или изменению системных настроек
то использование контейнеров нецелесообразно, так как такие приложения могут требовать прямого доступа к устройствам
или нуждаться в высоких привилегиях, в то время как контейнеры работают в изолированной среде и, обычно, с ограниченными. 
привелегиями. Чтобы обеспечить доступ к аппаратным ресурсам из контейнера можно использовать флаги --privileged, но
это может повысить риск безопасности. \
Второй вариант - если приложение имеет сложный графический интерфейс, так как контейнеры проектируются для серверного
окружения и не оптимизированы для работы с графикой. А также необходимо учитывать, что для взаимодействия пользователя
с интерфейсом, необходимо пробрасывать ввод-вывод, что добавляет сложность и может увеличить время отклика.