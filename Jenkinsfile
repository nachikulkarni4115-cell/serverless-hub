pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'nachiket1/my-cicd-app:latest'
        KUBECONFIG = '/var/lib/jenkins/kubeconfig'
    }

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/nachikulkarni4115-cell/serverless-hub.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $DOCKER_IMAGE .'
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub',
                        usernameVariable: 'DOCKER_USERNAME',
                        passwordVariable: 'DOCKER_PASSWORD'
                    )
                ]) {
                    sh '''
                        echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin
                        docker push $DOCKER_IMAGE
                        docker logout
                    '''
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh '''
                    kubectl --kubeconfig=$KUBECONFIG \
                    set image deployment/my-cicd-app \
                    my-cicd-app=$DOCKER_IMAGE

                    kubectl --kubeconfig=$KUBECONFIG \
                    rollout status deployment/my-cicd-app
                '''
            }
        }
    }
}
