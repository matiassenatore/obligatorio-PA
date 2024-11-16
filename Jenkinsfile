pipeline {
    agent any

    parameters {
        booleanParam(name: 'RUN_PROJECT_1', defaultValue: true, description: 'Jugar Trivia')
        booleanParam(name: 'RUN_PROJECT_2', defaultValue: true, description: 'Procesar pedidos')
        booleanParam(name: 'RUN_PROJECT_3', defaultValue: true, description: 'Realizar consultas en USQL')
    }

    stages {
        stage('Jugar Trivia') {
            when {
                expression { params.RUN_PROJECT_1 }
            }
            steps {
                script {
                    stage('Checkout El juego de la trivia') {
                        git url: 'https://github.com/matiassenatore/obligatorio-PA/tree/main/obg1_trivia%202.git', branch: 'main'
                        if (!fileExists('obligatorio-PA/obg1_trivia 2/')) {
                            error 'Archivo entregable 1 no encontrado.'
                        }
                    }
                    stage('Install Dependencies El juego de la trivia') {
                        sh 'python3 -m pip install -r requirements.txt'
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

        stage('Procesar pedidos') {
            when {
                expression { params.RUN_PROJECT_2 }
            }
            steps {
                script {
                    stage('Checkout Procesar pedidos') {
                        git url: 'https://github.com/matiassenatore/obligatorio-PA/tree/main/Entregable%202-1.git', branch: 'main'
                        if (!fileExists('obligatorio-PA/Entregable%202-1/Entregable2/')) {
                            error 'Archivo entregable 2 no encontrado.'
                        }
                    }
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

                    }
                }
            }
        }

        stage('Realizar consultas en USQL') {
            when {
                expression { params.RUN_PROJECT_3 }
            }
            steps {
                script {
                    stage('Checkout Consultas en USQL') {
                        git url: 'https://github.com/matiassenatore/obligatorio-PA/tree/main/obligatorio_PA.git', branch: 'main'
                        if (!fileExists('obligatorio-PA/obligatorio_PA/usql/')) {
                            error 'Archivo entregable 3 no encontrado.'
                        }
                    }
                    stage('Install Dependencies Consultas en USQL') {
                        sh 'python3 -m pip install -r requirements.txt'
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

    post {
        always {
            mail to: 'mnsenatore@gmail.com',
                 subject: "Pipeline ${currentBuild.fullDisplayName} - ${currentBuild.currentResult}",
                 body: "Consulta Jenkins para más detalles."
        }
    }
}
