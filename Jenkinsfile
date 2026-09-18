pipeline {

    agent any

    environment {
        DOCKER_IMAGE = "yuviiee/docker-py-backend-app"
        PREVIOUS_IMAGE = ""
    }

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main',
                url: 'https://github.com/Yuvanesh-P/docker-py-backend-app.git'
            }
        }   

        stage('Test') {
            steps {
                bat 'python -m pytest'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t %DOCKER_IMAGE%:%BUILD_NUMBER% .'
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-credentials',
                        usernameVariable: 'DOCKER_USERNAME',
                        passwordVariable: 'DOCKER_PASSWORD'
                    )
                ]) {
                    bat 'docker login -u "%DOCKER_USERNAME%" -p "%DOCKER_PASSWORD%"'
                    bat 'docker push %DOCKER_IMAGE%:%BUILD_NUMBER%'
                    bat 'docker logout'
                }
            }
        }
        stage('Deploy to DEV') {
            steps {
                bat '''
                docker rm -f dev-app 2>NUL || exit 0
                docker run -d --name dev-app -p 5001:5000 %DOCKER_IMAGE%:%BUILD_NUMBER%
                '''
            }
        }
        stage('Deploy to STAGING') {
            steps {
                bat '''
                docker rm -f staging-app 2>NUL || exit 0
                docker run -d --name staging-app -p 5002:5000 %DOCKER_IMAGE%:%BUILD_NUMBER%
                '''
            }
        }
        stage('Production Approval') {
            steps {
                input message: 'Deploy to Production?', ok: 'Deploy'
            }
        }
        stage('Deploy to PRODUCTION') {
            steps {
                timeout(time: 5, unit: 'MINUTES') {
                    bat '''
                    docker inspect --format="{{.Config.Image}}" prod-app > previous_image.txt 2>NUL || echo NONE > previous_image.txt
                    docker rm -f prod-app 2>NUL || exit 0
                    docker run -d --name prod-app -p 5003:5000 %DOCKER_IMAGE%:%BUILD_NUMBER%
                    '''
                }       
            }
        }
    }
}