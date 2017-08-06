node {
    stage("prepare")
    println "**** PREPARE ****"
    def app_name = "homecontrol-webserver"

    stage("checkout")
    println "**** CHECKOUT ****"
    git url: "https://github.com/robe16/HomeControl-webserver.git"
    sh "git rev-parse HEAD > .git/commit-id"
    def commit_id = readFile('.git/commit-id').trim()
    println commit_id

    stage("build")
    println "**** BUILD ****"
    def app = docker.build "${app_name}":"${commit_id}"

}