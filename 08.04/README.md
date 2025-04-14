# ETL-процесс для обработки данных форума

## Описание
Этот проект представляет собой процесс ETL, который извлекает данные из базы данных, преобразует их и загружает в CSV файл.

## Установка и настройка Jenkins

### 1. Установка Jenkins
Для установки Jenkins на Docker выполните следующие шаги:

1. Создайте сеть для Jenkins
    docker network create jenkins-net


2. Установите Jenkins через Docker (Windows):
    docker run -d --name jenkins -p 8080:8080 -p 50001:50000 -v jenkins_home:/var/jenkins_home jenkins/jenkins:lts-jdk11 -v /var/run/docker.sock:/var/run/docker.sock \ -v "C:\Program Files\Docker\docker.exe":"/usr/bin/docker" \

3. Откройте Jenkins в браузере по URL: [http://localhost:8080](http://localhost:8080)

4. Узнайте пароль для входа через команду
    docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword

### 2. Установка необходимых плагинов
После входа в Jenkins, установите следующие плагины:
- **Git Plugin**
- **Pipeline Plugin**
- **Docker Pipeline**

Или же выберете стандартную установку, где данные плагины будут установлены

### 3. Создание нового пользователя
1. Перейдите в `Manage Jenkins > Manage Users`.
2. Создайте нового пользователя с правами администратора.

## Настройка Jenkins Pipeline

### 1. Создание нового проекта
1. В Jenkins выберите **New Item**.
2. Введите название проекта (например, **ETL**).
3. Выберите **Pipeline** и нажмите **OK**.

### 2. Настройка пайплайна
Добавьте следующий код пайплайна в раздел **Pipeline Script**:

```groovy
pipeline {
    agent any
    stages {
        stage('ETL') {
            steps {
                script {
                    docker.image('python:3.9-slim').inside {
                    sh """
                    pip install psycopg2-binary
                    python etl.py ${START_DATE} ${END_DATE}
                    """
            }
        }
    }
        }
        stage('Save Artifact') {
            steps {
                archiveArtifacts artifacts: 'forum_report.csv', fingerprint: true
            }
        }
    }
}