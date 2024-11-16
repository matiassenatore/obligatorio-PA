pipeline {
    agent any

    parameters {
        booleanParam(name: 'RUN_PROJECT_1', defaultValue: true, description: 'Jugar Trivia')
        booleanParam(name: 'RUN_PROJECT_2', defaultValue: true, description: 'Procesar pedidos')
        booleanParam(name: 'RUN_PROJECT_3', defaultValue: true, description: 'Realizar consultas en USQL')
    }

    stages {
        stage('Checkout Repositorio Principal') {
            steps {
                script {
                    git url: 'https://github.com/matiassenatore/obligatorio-PA.git', branch: 'main'
                }
            }
        }

        stage('Jugar Trivia') {
            when {
                expression { params.RUN_PROJECT_1 }
            }
            steps {
                dir('obg1_trivia 2') {
                    script {
                        stage('Install Dependencies El juego de la trivia') {
                            sh 'python3 -m pip install -r ../requirements.txt'
                        }
                        stage('Test El juego de la trivia') {
                            sh 'pytest tests/'
                        }
                        stage('Run El juego de la trivia') {
                            sh 'python3 main.py'
                        }
                    }
                }
            }
        }

        stage('Procesar pedidos') {
            when {
                expression { params.RUN_PROJECT_2 }
            }
            steps {
                dir('Entregable 2-1/Entregable2') {
                    script {
                        stage('Build Procesar pedidos') {
                            sh 'mvn clean install'
                        }
                        stage('Test Procesar pedidos') {
                            sh 'mvn test'
                        }
                        stage('Package Procesar pedidos') {
                            sh 'mvn package'
                        }
                        stage('Deploy Procesar pedidos') {
                            // Comando de despliegue específico para Procesar pedidos
                            // sh 'comando de despliegue proyecto pedidos'
                        }
                    }
                }
            }
        }

        stage('Realizar consultas en USQL') {
            when {
                expression { params.RUN_PROJECT_3 }
            }
            steps {
                dir('obligatorio_PA/usql') {
                    script {
                        stage('Install Dependencies Consultas en USQL') {
                            sh 'python3 -m pip install -r ../requirements.txt'
                        }
                        stage('Test Consultas en USQL') {
                            sh 'pytest tests/'
                        }
                        stage('Run Consultas en USQL') {
                            sh 'python3 usql_translator.py'
                        }
                    }
                }
            }
        }
    }

    post {
        always {
            mail to: 'mnsenatore@gmail.com',
                 subject: "Pipeline ${currentBuild.fullDisplayName} - ${currentBuild.currentResult}",
                 body: "Consulta Jenkins para más detalles."
        }
    }
}
