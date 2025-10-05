pipeline {
  agent any

  environment {
    // Make sure you created a Jenkins secret text credential with ID 'openai-api-key'
    OPENAI_API_KEY = credentials('openai-api-key')
  }

  stages {
    stage('Checkout') {
      steps { checkout scm }
    }

    stage('Build') {
      steps {
        // Run the PowerShell build script that intentionally fails in this demo
        powershell 'scripts\\build.ps1'
      }
    }
  }

  post {
    failure {
      script {
        echo "Build failed. Checking for build.log and running AI analysis..."
        if (fileExists('build.log')) {
          echo "Found build.log — installing analyzer requirements and running analyzer..."

          // Install Python requirements if necessary (assumes Python & pip are on PATH)
          // If you don't want to install each run, install once on the agent manually.
          powershell '''
            python -m pip install --user -r requirements.txt
            python scripts\\analyze_log.py build.log
          '''
        } else {
          echo "No build.log found in workspace."
        }
      }
    }
  }
}
