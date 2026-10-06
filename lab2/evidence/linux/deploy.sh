# Deploy my masterpiece. Makes a git pull just to be sure it has everything.
set -e

REMOTE_HOST="fenix-prod"
REPOSITORY="git@gitlab.com:MuskyBoi/peixinho.git"

echo "Deploying website to $REMOTE_HOST"

ssh -t "$REMOTE_HOST" "
    set -e

    if [ -d \"\$HOME/fenix/peixinho/.git\" ]; then
        echo \"Updating existing repository\"
        git -C \"\$HOME/fenix/peixinho\" pull --ff-only
    else
        echo \"Cloning repository\"
        git clone \"$REPOSITORY\" \"\$HOME/fenix\"
    fi

    echo \"Starting website\"
    cd \"\$HOME/fenix/peixinho\"
    sudo docker compose up -d --build
"

echo "Deployment finished"
