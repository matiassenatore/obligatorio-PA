pipeline {
    agent any

    parameters {
        booleanParam(name: 'RUN_PROJECT_1', defaultValue: true, description: 'Ejecutar El juego de la trivia')
        booleanParam(name: 'RUN_PROJECT_2', defaultValue: true, description: 'Ejecutar Procesar pedidos')
        booleanParam(name: 'RUN_PROJECT_3', defaultValue: true, description: 'Ejecutar Consultas en USQL')
    }

    stages {
        stage('El juego de la trivia') {
            when {
                expression { params.RUN_PROJECT_1 }
            }
            steps {
                script {
                    stage('Checkout El juego de la trivia') {
                        git url: 'https://github.com/jzangaro/Obg_UNO.git', branch: 'main'
                    }
                    stage('Build El juego de la trivia') {
                        sh 'mvn clean install'
                    }
                    stage('Test El juego de la trivia') {
                        sh 'mvn test'
                    }
                    stage('Package El juego de la trivia') {
                        sh 'mvn package'
                    }
                    stage('Deploy El juego de la trivia') {
                        // Comando de despliegue específico para El juego de la trivia
                        // sh 'comando de despliegue proyecto trivia'
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
                        git url: 'https://github.com/jzangaro/Obg_DOS.git', branch: 'main'
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
                        // Comando de despliegue específico para Procesar pedidos
                        // sh 'comando de despliegue proyecto pedidos'
                    }
                }
            }
        }

        stage('Consultas en USQL') {
            when {
                expression { params.RUN_PROJECT_3 }
            }
            steps {
                script {
                    stage('Checkout Consultas en USQL') {
                        git url: 'https://github.com/jzangaro/Obg_TRES.git', branch: 'main'
                    }
                    stage('Build Consultas en USQL') {
                        sh 'mvn clean install'
                    }
                    stage('Test Consultas en USQL') {
                        sh 'mvn test'
                    }
                    stage('Package Consultas en USQL') {
                        sh 'mvn package'
                    }
                    stage('Deploy Consultas en USQL') {
                        // Comando de despliegue específico para Consultas en USQL
                        // sh 'comando de despliegue proyecto usql'
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
