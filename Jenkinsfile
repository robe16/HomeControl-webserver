node {
    docker.withRegistry('registry') {

        stage("prepare")
        def app_name = "homecontrol-webserver"
        git url: "https://github.com/robe16/HomeControl-webserver.git"
        sh "git rev-parse HEAD > .git/commit-id"
        def commit_id = readFile('.git/commit-id').trim()
        println commit_id

        stage("build")
        def app = docker.build "homecontrol-webserver"

        stage("publish")
        app.push "${commit_id}"

    }
}