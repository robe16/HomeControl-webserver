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
        docker_img = docker.build "${app_name}"
            docker_img.push("${commit_id}")
        //    docker_img.push("latest")
        //docker_img = docker.build "${app_name}:${commit_id}"
    }

    stage("deploy"){
        try {
            /*
            def container_running = "echo curl -X GET http://${deployment_server}:2375/containers/json?all=false \
                                    | ./jq '[ .[].Names | .[] | . == ${app_name} ] \
                                    | reduce .[] as $item (false; . | $item)'"
            println "Container running status: ${container_running}"
            */
        } catch (error) {
            println "Error determining container status"
        }
    }

}
