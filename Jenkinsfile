echo "Running Build ID: ${env.BUILD_ID}"

String commit_id
String build_args
String docker_img_name
def docker_img

node {

    deleteDir()

    stage("parameters") {
        // Parameters passed through from the Jenkins Pipeline configuration
        string(defaultValue: 'https://github.com/robe16/HomeControl-webserver.git', description: 'GitHub URL for checking out project', name: 'githubUrl')
        string(defaultValue: 'homecontrol-webserver', description: 'Name of application for Docker image and container', name: 'appName')
        string(defaultValue: '*', description: 'Server to deploy the Docker container', name: 'deploymentServer')
        string(defaultValue: '8080', description: 'Port number for python application running within container', name: 'portApplication')
        string(defaultValue: '8080', description: 'Port number to map portApplication to', name: 'portMapped')
        string(defaultValue: '1600', description: 'Port number that the core server application listens on', name: 'portServer')
        //
        build_args = ["--build-arg portApplication=${params.portApplication}",
                      "--build-arg portServer=${params.portServer}"].join(" ")
    }

    stage("checkout") {
        git url: "${params.githubUrl}"
        sh "git rev-parse HEAD > .git/commit-id"
        commit_id = readFile('.git/commit-id').trim()
        echo "Git commit ID: ${commit_id}"
    }

    docker_img_name = "${params.appName}:${commit_id}"

    stage("build") {
        //try {sh "docker image rm ${params.appName}:latest"} catch (error) {}
        docker_img = docker.build "${docker_img_name}", "${build_args}"
    }

    stage("deploy"){
        //try {
        //    docker.withRegistry("${params.deploymentServer}", 'docker-hub-credentials') {
        //        docker_img.push("${env.BUILD_NUMBER}")
        //        docker_img.push("latest")
        //    }
        //} catch (error) {
        //    echo "Error attempting to deploy image to server"
        //}
        // See:    https://jenkins.io/doc/book/pipeline/docker/#using-a-remote-docker-server
        echo "Deployment to server 'on hold' - awaiting future development"
    }

    stage("start container"){
        sh "docker rm -f ${params.appName} && echo \"container ${params.appName} removed\" || echo \"container ${params.appName} does not exist\""
        sh "docker run -d -p ${params.portMapped}:${params.portApplication} --name ${params.appName} ${docker_img_name}"

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
