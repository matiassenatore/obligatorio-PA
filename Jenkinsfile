pipeline {
    agent any

    parameters {
        booleanParam(name: 'RUN_PROJECT_1', defaultValue: true, description: 'Jugar Trivia')
        booleanParam(name: 'RUN_PROJECT_2', defaultValue: true, description: 'Procesar pedidos')
        booleanParam(name: 'RUN_PROJECT_3', defaultValue: true, description: 'Realizar consultas en USQL')
    }

    stages {
        
            }
        }
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
                            bat 'python -m pip install -r ../../requirements.txt'
                        }
                        stage('Test El juego de la trivia') {
                            bat 'pytest tests/'
                        }
                        stage('Run El juego de la trivia') {
                            bat 'python obg1_prog_avz.py'
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
                            bat 'mvn clean install'
                        }
                        stage('Test Procesar pedidos') {
                            bat 'mvn test'
                        }
                        stage('Package Procesar pedidos') {
                            bat 'mvn package'
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
                            bat 'python -m pip install -r ../../requirements.txt'
                        }
                        stage('Test Consultas en USQL') {
                            bat 'pytest tests/'
                        }
                        stage('Run Consultas en USQL') {
                            sh 'python obligatorio_PA/usql/usql_translator.py'
                        }
                    }
                }
            }
        }
    }

    post {
        always {
            script {
                try {
                    mail to: 'mnsenatore@gmail.com',
                         subject: "Pipeline ${currentBuild.fullDisplayName} - ${currentBuild.currentResult}",
                         body: "Consulta Jenkins para más detalles."
                } catch (Exception e) {
                    echo 'Error al enviar el correo. Verifique la configuración SMTP.'
                }
            }
        }
    }
}
