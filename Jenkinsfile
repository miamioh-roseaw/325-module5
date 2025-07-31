pipeline {
    agent any

    environment {
        SCRIPT = 'get_uptime.py'
        PATH = "${HOME}/.local/bin:${env.PATH}"
        PYTHONPATH = "${HOME}/.local/lib/python3.10/site-packages"
    }

    stages {
        stage('Install Nornir and Dependencies') {
            steps {
                sh '''
                    echo "[INFO] Installing Python packages..."
                    if ! command -v pip3 > /dev/null; then
                        echo "[INFO] pip3 not found. Installing..."
                        wget https://bootstrap.pypa.io/get-pip.py -O get-pip.py
                        python3 get-pip.py --user
                    fi
                    ~/.local/bin/pip3 install --user nornir nornir-netmiko nornir-utils netmiko paramiko
                '''
            }
        }

        stage('Run Nornir Script') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'cisco-ssh-creds', usernameVariable: 'CISCO_USER', passwordVariable: 'CISCO_PASS')]) {
                    sh '''
                        echo "[INFO] Running Nornir uptime collection..."
                        export CISCO_USER="${CISCO_USER}"
                        export CISCO_PASS="${CISCO_PASS}"
                        python3 ${SCRIPT}
                    '''
                }
            }
        }

        stage('Archive Outputs') {
            steps {
                script {
                    def artifactsExist = sh(script: "ls *_uptime.txt 2>/dev/null || true", returnStdout: true).trim()
                    if (artifactsExist) {
                        echo "[INFO] Archiving uptime result files..."
                        archiveArtifacts artifacts: '*_uptime.txt', allowEmptyArchive: false
                    } else {
                        echo "[WARNING] No uptime files were generated to archive."
                    }
                }
            }
        }
    }

    post {
        failure {
            echo "[ERROR] Pipeline failed."
        }
        always {
            echo "[INFO] Pipeline completed."
        }
    }
}
