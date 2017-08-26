echo "Running Build ID: ${env.BUILD_ID}"

def commit_id
def docker_img


pipeline {

    agent none

    stages {

        stage("parameters") {
            agent any
            steps {
                // Parameters passed through from the Jenkins Pipeline configuration
                string(defaultValue: 'https://github.com/robe16/HomeControl-webserver.git', description: 'GitHub URL for checking out project', name: 'githubUrl')
                string(defaultValue: 'homecontrol-webserver', description: 'Name of application for Docker image and container', name: 'appName')
                string(defaultValue: '*', description: 'Server to deploy the Docker container', name: 'deploymentServer')
                string(defaultValue: '8080', description: 'Port number for python application running within container', name: 'portApplication')
                string(defaultValue: '8080', description: 'Port number to map portApplication to', name: 'portMapped')
                string(defaultValue: '1600', description: 'Port number that the core server application listens on', name: 'portServer')
            }
        }

        stage("checkout") {
            agent any
            steps {
                git url: "${params.githubUrl}"
                sh "git rev-parse HEAD > .git/commit-id"
                commit_id = readFile('.git/commit-id').trim()
                echo "Git commit ID: ${commit_id}"
            }
        }

        stage("build") {
            agent {dockerfile {
                    additionalBuildArgs "--build-arg portApplication=${params.portApplication} portServer=${params.portServer}"
                }}
            steps {
                /*try {
                    sh "docker image rm ${params.appName}:latest"
                } catch (error) {}*/
                docker.build("${params.appName}:${commit_id}")
            }
        }

        stage("deploy") {
            agent any
            steps {
                // See:    https://jenkins.io/doc/book/pipeline/docker/#using-a-remote-docker-server
                echo "Deployment to server 'on hold' - awaiting future development"
            }
        }

        stage("start container") {
            agent any
            steps {
                sh "docker rm -f ${params.appName} && echo \"container ${params.appName} removed\" || echo \"container ${params.appName} does not exist\""
                sh "docker run -d -p ${params.portMapped}:${params.portApplication} --name ${params.appName} ${params.appName}:${commit_id}"
            }
        }

    }
}