pipeline {
  agent any
  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }
    stage('Build') {
      steps {
        powershell 'scripts/build.ps1'
      }
    }
    stage('Test') {
      steps {
        echo "This stage will be skipped because Build fails."
      }
    }
  }
  post {
    failure {
      script {
        if (fileExists('build.log')) {
          echo "=== build.log contents ==="
          powershell 'Get-Content build.log'
        }
      }
    }
  }
}
