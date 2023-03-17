pipeline {
    agent any

    stages {
        stage('Test') {
            steps {
                dir('C:/Users/Admir/.jenkins/workspace/Inlamningsuppgift(KK2)_multibranch/Tests'){ 
                    bat 'python -m unittest'
                }
            }
        }
        stage('Clean Workspace'){
            steps {
                cleanWs()
            }
        }
    }
}
