node {
    docker.withRegistry('registry') {

        git url: "https://github.com/robe16/HomeControl-webserver.git"

        sh "git rev-parse HEAD > .git/commit-id"
        def commit_id = readFile('.git/commit-id').trim()
        println commit_id

        stage "build"
        def app = docker.build "HomeControl-webserver"

        stage "publish"
        app.push 'master'
        app.push "${commit_id}"
    }
}