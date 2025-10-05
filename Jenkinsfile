pipeline {
    agent any

    environment {
        OPENAI_API_KEY = credentials('openai_api_key')  // Add in Jenkins > Manage Credentials
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
                        python src/app.py > build_logs/build_output.txt 2>&1
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
            echo "Build completed. Check above for AI-powered analysis."
        }
    }
}
