export $(grep -v '^#' devenv.env | xargs)
export FLASK_APP=git_project_management.api
export DISPLAY=:0
export FLASK_DEBUG=1
flask run
