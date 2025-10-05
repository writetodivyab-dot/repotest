pipeline {
    agent any

    environment {
        OPENAI_API_KEY = credentials('openai_api_key')  // Set in Jenkins > Manage Credentials
    }

    stages {
        stage('Setup') {
            steps {
                echo "Installing Python dependencies..."
                powershell '''
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Build') {
            steps {
                echo "Running build..."
                powershell '''
                    mkdir -Force build_logs | Out-Null
                    try {
                        # Run build and capture both console + file output
                        python src/app.py *>&1 | Tee-Object -FilePath build_logs/build_output.txt
                        exit 0
                    } catch {
                        Write-Host "Build failed — capturing logs"
                        exit 1
                    }
                '''
            }
        }

        stage('Analyze Failure') {
            when {
                expression { currentBuild.currentResult == 'FAILURE' }
            }
            steps {
                echo "Analyzing failed build logs using OpenAI..."
                powershell '''
                    python scripts/analyze_log.py build_logs/build_output.txt
                '''
            }
        }
    }

    post {
        always {
            echo "Build completed. Archiving build and analysis logs..."
            archiveArtifacts artifacts: 'build_logs/*.txt', fingerprint: true
            echo "Logs archived successfully — check the 'Last Successful Artifacts' section."
        }
    }
}
