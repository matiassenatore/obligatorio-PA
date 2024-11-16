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
                            try {
                                bat 'python -m pip install -r ../requirements.txt'
                            } catch (Exception e) {
                                echo 'Fallo en la etapa de Install Dependencies El juego de la trivia'
                                currentBuild.result = 'FAILURE'
                            }
                        }
                        stage('Test El juego de la trivia') {
                            try {
                                bat 'pytest Test.py'
                            } catch (Exception e) {
                                echo 'Fallo en la etapa de Test El juego de la trivia'
                                currentBuild.result = 'FAILURE'
                            }
                        }
                        stage('Run El juego de la trivia') {
                            try {
                                bat 'python obg1_prog_avz.py'
                            } catch (Exception e) {
                                echo 'Fallo en la etapa de Run El juego de la trivia'
                                currentBuild.result = 'FAILURE'
                            }
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
                            try {
                                bat 'mvn clean install'
                            } catch (Exception e) {
                                echo 'Fallo en la etapa de Build Procesar pedidos'
                                currentBuild.result = 'FAILURE'
                            }
                        }
                        stage('Test Procesar pedidos') {
                            try {
                                bat 'mvn test'
                            } catch (Exception e) {
                                echo 'Fallo en la etapa de Test Procesar pedidos'
                                currentBuild.result = 'FAILURE'
                            }
                        }
                        stage('Package Procesar pedidos') {
                            try {
                                bat 'mvn package'
                            } catch (Exception e) {
                                echo 'Fallo en la etapa de Package Procesar pedidos'
                                currentBuild.result = 'FAILURE'
                            }
                        }
                        stage('Deploy Procesar pedidos') {
                            try {
                                // Comando de despliegue específico para Procesar pedidos
                                // sh 'comando de despliegue proyecto pedidos'
                            } catch (Exception e) {
                                echo 'Fallo en la etapa de Deploy Procesar pedidos'
                                currentBuild.result = 'FAILURE'
                            }
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
                            try {
                                bat 'python -m pip install -r ../../requirements.txt'
                            } catch (Exception e) {
                                echo 'Fallo en la etapa de Install Dependencies Consultas en USQL'
                                currentBuild.result = 'FAILURE'
                            }
                        }
                        stage('Test Consultas en USQL') {
                            timeout(time: 5, unit: 'MINUTES') {
                                try {
                                    bat 'pytest tests.py -v'
                                } catch (Exception e) {
                                    echo 'Fallo en la etapa de Test Consultas en USQL'
                                    currentBuild.result = 'FAILURE'
                                }
                            }
                        }
                        stage('Run Consultas en USQL') {
                            try {
                                sh 'python usql_translator.py'
                            } catch (Exception e) {
                                echo 'Fallo en la etapa de Run Consultas en USQL'
                                currentBuild.result = 'FAILURE'
                            }
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
