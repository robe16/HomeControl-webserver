echo "Running Build ID: ${env.BUILD_ID}"

def commit_id
def docker_img

node {

    stage("parameters") {
        // Parameters passed through from the Jenkins Pipeline configuration
        string(defaultValue: '*', description: 'GitHub URL for checking out project', name: 'githubUrl')
        string(defaultValue: '*', description: 'Name of application for Docker image and container', name: 'appName')
        string(defaultValue: '*', description: 'Server to deploy the Docker container', name: 'deploymentServer')
    }

    stage("checkout") {
        git url: "${params.githubUrl}"
        sh "git rev-parse HEAD > .git/commit-id"
        commit_id = readFile('.git/commit-id').trim()
        echo "Git commit ID: ${commit_id}"
    }

    stage("build") {
        try {
            sh "docker image rm ${params.appName}:latest"
        } catch (error) {}
        docker_img = docker.build "${params.appName}:${commit_id}"
        //docker_img = docker.build "${params.appName}"
    }

    stage("deploy"){
        try {
            docker.withRegistry("${params.deploymentServer}", 'docker-hub-credentials') {
                docker_img.push("${env.BUILD_NUMBER}")
                docker_img.push("latest")
            }
        } catch (error) {
            echo "Error attempting to deploy image to server"
        }
    }

    stage("start container"){
        sh 'docker rm -f ${params.appName} && echo "container ${params.appName} removed" || echo "container ${params.appName} does not exist"'
        sh "docker run -d -p 8081:8080 --name ${params.appName} ${params.appName}:${commit_id}"

    }

}

/*
    try {
        def container_running = "echo curl -X GET http://${deployment_server}:2375/containers/json?all=false \
                                | ./jq '[ .[].Names | .[] | . == ${app_name} ] \
                                | reduce .[] as $item (false; . | $item)'"
        println "Container running status: ${container_running}"
    } catch (error) {
        println "Error determining container status"
    }
*/
