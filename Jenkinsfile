node {
    stage("prepare")
    println "**** PREPARE ****"
    sh "docker login"
    def app_name = "homecontrol-webserver"

    stage("checkout")
    println "**** CHECKOUT ****"
    git url: "https://github.com/robe16/HomeControl-webserver.git"
    sh "git rev-parse HEAD > .git/commit-id"
    def commit_id = readFile('.git/commit-id').trim()
    println commit_id

    stage("build")
    println "**** BUILD ****"
    def app = docker.build "${app_name}"

    stage("publish")
    println "**** PUBLISH ****"
    app.push "${commit_id}"
}