#! /bin/sh
echo "======================================================================"
echo "Welcome to to the setup. This will setup the local virtual env."
echo "And then it will install all the required python libraries."
echo "You can rerun this without any issues."
echo "----------------------------------------------------------------------"
if [ -d "node_modules" ];
then
    echo "node_modules folder exists."
else
    echo "Installing node modules"
    npm install
fi

npm run serve
