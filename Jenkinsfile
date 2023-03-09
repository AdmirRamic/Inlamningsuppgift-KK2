pipeline {
    agent any

    stages {
        stage('Check out repo'){
            steps {
                checkout scmGit(branches: [[name: '**']], extensions: [], userRemoteConfigs: [[credentialsId: '5de8c485-fac5-4331-a12a-e793c2b254f3', url: 'https://github.com/AdmirRamic/Inlamningsuppgift-KK2.git']])
                }
            }
        
        stage('Test') {
            steps {
                dir('C:/Users/Admir/.jenkins/workspace/Inlamningsuppgift(KK2)/Tests'){ 
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
