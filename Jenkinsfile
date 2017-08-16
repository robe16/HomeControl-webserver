node {

    echo "Running ${env.BUILD_ID} on ${env.JENKINS_URL}"

    stage("prepare")
    println "**** PREPARE ****"
    def app_name = "homecontrol-webserver"
    def deployment_server = "192.168.0.102"

    stage("checkout")
    println "**** CHECKOUT ****"
    git url: "https://github.com/robe16/HomeControl-webserver.git"
    sh "git rev-parse HEAD > .git/commit-id"
    def commit_id = readFile('.git/commit-id').trim()
    println commit_id

    stage("build")
    println "**** BUILD ****"
    def app = docker.build "${app_name}:${commit_id}"

    stage("deploy")
    println "**** DEPLOY ****"
    try {
        def container_running = "echo curl -X GET http://${deployment_server}:2375/containers/json?all=false \
                                | ./jq '[ .[].Names | .[] | . == ${app_name} ] \
                                | reduce .[] as $item (false; . | $item)'"
        println "Container running status: ${container_running}"
    } catch (error) {
    }

}
