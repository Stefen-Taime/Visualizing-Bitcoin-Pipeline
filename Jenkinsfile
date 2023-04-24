pipeline {
    agent {
        label 'ubuntu'
    }
    stages {
        stage('Build and Deploy prometheus, grafana, and redis') {
            steps {
                dir('/home/stefen/deploy/adminer') {
                    sh 'pwd' // Ajout de la commande pwd pour vérifier le répertoire de travail
                    sh 'ls -la'
                    sh 'docker-compose up -d'
                }
            }
        }
        stage('Build and Deploy API') {
            steps {
                sleep(time: 30, unit: 'SECONDS') // Wait for 30 seconds
                dir('/home/stefen/deploy/api') {
                    sh 'pwd' // Check the current working directory
                    sh 'ls -la'
                    sh 'docker-compose up --build -d'
                }
            }
        }
        stage('Fetch and Print getexchangedata') {
            steps {
                script {
                    def response = httpRequest 'http://localhost:5000/getexchangedata'
                    echo "Response: ${response.content}"
                }
            }
        }
        stage('Fetch and Print Exchangemetrics') {
            steps {
                script {
                    def response = httpRequest 'http://localhost:5000/exchangemetrics'
                    echo "Response: ${response.content}"
                }
            }
        }
    }
    post {
        always {
            script {
                def prometheusURL = 'http://localhost:9090'
                def grafanaURL = 'http://localhost:3000'
                def redisURL = 'http://localhost:6379'
                def apiURL = 'http://localhost:5000'

                echo "Prometheus URL: ${prometheusURL}"
                echo "Grafana URL: ${grafanaURL}"
                echo "Redis URL: ${redisURL}"
                echo "API URL: ${apiURL}"
            }
        }
    }
}
