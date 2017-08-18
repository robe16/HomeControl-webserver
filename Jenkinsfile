echo "Running Build ID: ${env.BUILD_ID}"

def git_url = "https://github.com/robe16/HomeControl-webserver.git"
def app_name = "homecontrol-webserver"
def deployment_server = "192.168.0.102"

def commit_id
def docker_img

node {

    stage("checkout") {
        git url: "${git_url}"
        sh "git rev-parse HEAD > .git/commit-id"
        commit_id = readFile('.git/commit-id').trim()
        echo "Git commit ID: ${commit_id}"
    }

    stage("build") {
        try {
            sh "docker image rm ${app_name}:latest"
        } catch (error) {}
        docker_img = docker.build "${app_name}:${commit_id}"
        //docker_img = docker.build "${app_name}"
    }

    stage("deploy"){
        try {
            docker.withRegistry("${deployment_server}", 'docker-hub-credentials') {
                docker_img.push("${env.BUILD_NUMBER}")
                docker_img.push("latest")
            }
        } catch (error) {
            echo "Error attempting to deploy image to server"
        }
    }

    stage("start container"){
        sh 'docker rm -f ${app_name} && echo "container ${app_name} removed" || echo "container ${app_name} does not exist"'
        sh "docker run -d -p 8081:8080 --name ${app_name} ${app_name}:${commit_id}"
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
