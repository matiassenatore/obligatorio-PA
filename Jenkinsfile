pipeline {
    agent any
    environment {
        EMAIL_RECIPIENT = 'mnsenatore@hotmail.com'
    }
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
                    // Verifica el directorio de trabajo y lista los archivos
                    sh 'pwd'
                    sh 'ls -la'
                    try {
                        switch (params.ENTREGABLE_OPTION) {
                            case '1':
                                echo 'Ejecutando Entregable 1: Trivia'
                                sh 'ls obligatorio-PA/obg1_trivia 2'  // Lista el contenido del directorio para asegurarnos de que el archivo está allí
                                sh 'pwd'
                                sh 'ls -la obligatorio-PA/obg1_trivia 2'  // Lista los archivos específicos del directorio de trivia
                                sh 'python3 obligatorio-PA/obg1_trivia 2/obg1_prog_avz.py'
                                break
                            case '2':
                                echo 'Ejecutando Entregable 2: Procesamiento de Pedidos'
                                sh 'pwd'
                                sh 'ls -la'
                                sh 'javac obligatorio-PA/Entregable_2-1/Entregable2/target/classes/uy/edu/um/Main.java'
                                sh 'java -cp obligatorio-PA/Entregable_2-1/Entregable2/target/classes uy.edu.um.Main'
                                break
                            case '3':
                                echo 'Ejecutando Entregable 3: Consultas en USQL'
                                sh 'pwd'
                                sh 'ls -la'
                                sh 'python3 obligatorio-PA/obligatorio_PA/usql/usql_translator.py'
                                break
                            default:
                                error 'Opción inválida seleccionada'
                        }
                    } catch (Exception e) {
                        echo 'Error ejecutando el entregable seleccionado: ' + e.getMessage()
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
                    // Prueba que cada opción pueda ser ejecutada sin errores
                    try {
                        echo 'Probando Entregable 1'
                        timeout(time: 5, unit: 'MINUTES') {
                            sh 'ls -la obligatorio-PA/obg1_trivia 2'  // Lista los archivos antes de la prueba
                            sh 'python3 obligatorio-PA/obg1_trivia 2/obg1_prog_avz.py --test'
                        }

                        echo 'Probando Entregable 2'
                        timeout(time: 5, unit: 'MINUTES') {
                            sh 'javac obligatorio-PA/Entregable_2-1/Entregable2/target/classes/uy/edu/um/Main.java'
                            sh 'java -cp obligatorio-PA/Entregable_2-1/Entregable2/target/classes uy.edu.um.Main --test'
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
        success {
            echo 'La ejecución del pipeline fue exitosa para el Entregable ${params.ENTREGABLE_OPTION}.'
        }
        failure {
            echo 'Hubo un fallo en la ejecución del pipeline para el Entregable ${params.ENTREGABLE_OPTION}. Revisa los detalles en Jenkins para más información.'
        }
    }
}





