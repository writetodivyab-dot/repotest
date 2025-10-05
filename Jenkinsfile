pipeline {
    agent any

    environment {
        OPENAI_API_KEY = credentials('openai-api-key')
    }

    options {
        ansiColor('xterm')  // Enables color in Jenkins console
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
                script {
                    def logFile = "${env.WORKSPACE}\\build_logs\\build_output_${env.BUILD_NUMBER}.txt"
                    powershell """
                        mkdir -Force build_logs | Out-Null
                        try {
                            python src/app.py *>&1 | Tee-Object -FilePath '${logFile}'
                            exit 0
                        } catch {
                            Write-Host "Build failed — captured logs to ${logFile}"
                            exit 1
                        }
                    """
                }
            }
        }

        stage('Analyze Failure') {
            when {
                expression { currentBuild.currentResult == 'FAILURE' }
            }
            steps {
                echo "Analyzing failed build logs using OpenAI..."
                script {
                    def logFile = "${env.WORKSPACE}\\build_logs\\build_output_${env.BUILD_NUMBER}.txt"
                    def analysisFile = "${env.WORKSPACE}\\build_logs\\ai_analysis_${env.BUILD_NUMBER}.txt"

                    powershell """
                        Write-Host "Starting AI analysis..." -ForegroundColor Yellow
                        python scripts/analyze_log.py '${logFile}' '${analysisFile}'
                        if (Test-Path '${analysisFile}') {
                            Write-Host "`n===== AI Analysis Saved To: ${analysisFile} =====`n" -ForegroundColor Green
                        } else {
                            Write-Host "⚠️  AI analysis file not created." -ForegroundColor Red
                        }
                    """
                }
            }
        }

        stage('Archive Logs') {
            steps {
                echo "Archiving build and analysis logs..."
                archiveArtifacts artifacts: 'build_logs/*.txt', fingerprint: true
            }
        }
    }

    post {
        always {
            echo "\u001B[36mBuild complete. Check artifacts for AI insights.\u001B[0m"
        }
    }
}
