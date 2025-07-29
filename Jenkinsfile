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
                    # Ensure pip is available
                    if ! command -v pip3 > /dev/null; then
                        echo "[INFO] pip not found. Installing..."
                        wget https://bootstrap.pypa.io/get-pip.py -O get-pip.py
                        python3 get-pip.py --user
                    fi

                    # Install Nornir and Netmiko
                    ~/.local/bin/pip3 install --user nornir nornir-netmiko nornir-utils netmiko
                '''
            }
        }

        stage('Run Nornir Script') {
            environment {
                CISCO_CREDS = credentials('cisco-ssh-creds')
            }
            steps {
                sh '''
                    echo "[INFO] Running Nornir uptime script..."

                    export CISCO_CREDS_USR="${CISCO_CREDS_USR}"
                    export CISCO_CREDS_PSW="${CISCO_CREDS_PSW}"

                    python3 ${SCRIPT}
                '''
            }
        }
    }

    post {
        always {
            echo '[INFO] Archiving uptime outputs...'
            archiveArtifacts artifacts: '*_uptime.txt', allowEmptyArchive: true
        }
    }
}
