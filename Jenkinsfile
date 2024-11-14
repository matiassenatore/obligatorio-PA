pipeline {
    agent any
    parameters {
        choice(name: 'ENTREGABLE_OPTION', choices: ['1', '2', '3'], description: 'Selecciona el entregable a ejecutar (1: Trivia, 2: Procesamiento de Pedidos, 3: Consultas en USQL)')
    }
    stages {
        stage('Checkout') {
            steps {
                // Clona el repositorio
                git url: 'https://github.com/matiassenatore/obligatorio-PA.git', branch: 'main'
            }
        }
        stage('Select Entregable') {
            steps {
                script {
                    try {
                        switch (params.ENTREGABLE_OPTION) {
                            case '1':
                                echo 'Ejecutando Entregable 1: Trivia'
                                sh 'python3 "obligatorio-PA/obg1_trivia 2/obg1_prog_avz.py"'
                                break
                            case '2':
                                echo 'Ejecutando Entregable 2: Procesamiento de Pedidos'
                                sh 'mvn -f obligatorio-PA/Entregable%202-1/Entregable2/pom.xml clean compile exec:java -Dexec.mainClass="uy.edu.um.Main"'
                                break
                            case '3':
                                echo 'Ejecutando Entregable 3: Consultas en USQL'
                                sh 'python3 obligatorio-PA/obligatorio_PA/usql/usql_translator.py'
                                break
                            default:
                                error 'Opción inválida seleccionada'
                        }
                    } catch (Exception e) {
                        echo 'Error ejecutando el entregable seleccionado: ' + e.getMessage()
                        currentBuild.description = "Falló en ${params.ENTREGABLE_OPTION}"
                        currentBuild.result = 'FAILURE'
                        error('Falló la ejecución del entregable seleccionado. Revisa los detalles.')
                    }
                }
            }
        }
        stage('Test Selection Menu') {
            steps {
                script {
                    echo 'Probando el menú de selección...'
                    try {
                        echo 'Probando Entregable 1'
                        timeout(time: 5, unit: 'MINUTES') {
                            sh 'python3 "obligatorio-PA/obg1_trivia 2/obg1_prog_avz.py" --test'
                        }

                        echo 'Probando Entregable 2'
                        timeout(time: 5, unit: 'MINUTES') {
                            sh 'mvn -f obligatorio-PA/Entregable%202-1/Entregable2/pom.xml test'
                        }

                        echo 'Probando Entregable 3'
                        timeout(time: 5, unit: 'MINUTES') {
                            sh 'python3 obligatorio-PA/obligatorio_PA/usql/usql_translator.py --test'
                        }
                    } catch (Exception e) {
                        echo 'Error en la prueba del menú de selección: ' + e.getMessage()
                        currentBuild.result = 'FAILURE'
                        error('La prueba del menú de selección falló. Revisa los detalles.')
                    }
                }
            }
        }
    }
    post {
        always {
            // Envía un correo al finalizar la pipeline
            emailext(
                subject: "Pipeline ${env.JOB_NAME} - Build #${env.BUILD_NUMBER} - ${currentBuild.currentResult}",
                body: """
                    <p>Pipeline: ${env.JOB_NAME}</p>
                    <p>Build Number: ${env.BUILD_NUMBER}</p>
                    <p>Status: ${currentBuild.currentResult}</p>
                    <p>Revisa Jenkins para más detalles: <a href=\"${env.BUILD_URL}\">${env.BUILD_URL}</a></p>
                """,
                recipientProviders: [[$class: 'DevelopersRecipientProvider'], [$class: 'RequesterRecipientProvider']],
                to: 'mnsenatore@gmail.com', // Aquí se envía la notificación a tu correo
                mimeType: 'text/html'
            )
        }
    }
}
