pipeline {
    agent any

    environment {
        OPENAI_API_KEY = credentials('openai-api-key')
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
                powershell """
                    mkdir -Force build_logs | Out-Null
                    \$buildLog = "build_logs/build_output_${env:BUILD_NUMBER}.txt"
                    try {
                        python src/app.py *>&1 | Tee-Object -FilePath \$buildLog
                        exit 0
                    } catch {
                        Write-Host "Build failed — captured logs to \$buildLog"
                        exit 1
                    }
                """
            }
        }

        stage('Analyze Failure') {
            when {
                expression { currentBuild.currentResult == 'FAILURE' }
            }
            steps {
                echo "Analyzing failed build logs using OpenAI..."
                powershell """
                    \$logFile = "build_logs/build_output_${env:BUILD_NUMBER}.txt"
                    \$analysisFile = "build_logs/ai_analysis_${env:BUILD_NUMBER}.txt"
                    python scripts/analyze_log.py \$logFile > \$analysisFile
                """
            }
        }

        stage('Archive Logs') {
            steps {
                echo "Archiving build and analysis logs..."
                archiveArtifacts artifacts: 'build_logs/*.txt', fingerprint: true
            }
        }
    }
}
