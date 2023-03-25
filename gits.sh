# if no command line arguments
if [ $# -eq 0 ]
  then
    # add commit pull push with a default commit message
    echo "No message supplied"
    git add .
    git commit -m "pushing"
    git pull -u origin main
    git push -u origin main
fi

# if a commit message was passed in as a command-line argument
if [ $# -eq 1 ]
  then
    # add commit pull push with the passed-in commit
    # message from the command line
    git add .
    git commit -m "$1"
    git pull -u origin main
    git push -u origin main
fi


