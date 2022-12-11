# set BLENDER_INSTALL_DIR var to blender executable directory, by default ~/bin/blender-3.3.0-linux-x64/
# BLENDER_INSTALL_DIR=~/bin/blender-3.3.0-linux-x64/

# # if user passes in arg for BLENDER_INSTALL_DIR, set to that value
# # otherwise, set to default
# if [ -n "$1" ]; then
#     BLENDER_INSTALL_DIR=$1
# fi
# BLENDER_VERSION=3.3
# PYTHON_VERSION=3.10

# # if blender directory is not set check for blender on linux, osx or windows
# if [ -z "$BLENDER_INSTALL_DIR" ]; then
#     if [ -d "/Applications/Blender.app/Contents/MacOS" ]; then
#         BLENDER_INSTALL_DIR="/Applications/Blender.app/Contents/MacOS"
#     elif [ -d "/usr/bin" ]; then
#         BLENDER_INSTALL_DIR="/usr/bin"
#     elif [ -d "/usr/local/bin" ]; then
#         BLENDER_INSTALL_DIR="/usr/local/bin"
#     elif [ -d "/c/Program Files/Blender Foundation/Blender" ]; then
#         BLENDER_INSTALL_DIR="/c/Program Files/Blender Foundation/Blender"
#     elif [ -d "/c/Program Files (x86)/Blender Foundation/Blender" ]; then
#         BLENDER_INSTALL_DIR="/c/Program Files (x86)/Blender Foundation/Blender"
#     fi
# fi

# # if blender path still not found, inform the user and end program
# if [ -z "$BLENDER_INSTALL_DIR" ]; then
#     echo "Blender not found. Please set the BLENDER_INSTALL_DIR variable in this script to the path of your blender executable."
#     exit 1
# fi

# # find python/bin in the BLENDER_DIR folder
# # PYTHON_BIN is BLENDER_INSTALL_DIR + / + BLENDER_VERSION + /python/bin/python + python version
# PYTHON_BIN="$BLENDER_INSTALL_DIR/$BLENDER_VERSION/python/bin/python$PYTHON_VERSION"

# # call $PYTHON_BIN -m ensurepip --upgrade
# $PYTHON_BIN -m ensurepip --upgrade

# $PYTHON_BIN -m pip install Pillow

# check for node.js and download it with curl if it doesn't exist
if ! [ -x "$(command -v node)" ]; then
  echo 'Error: node is not installed.' >&2
  echo 'Installing node.js...'
  curl -sL https://deb.nodesource.com/setup_18.x | sudo -E bash -
  sudo apt-get install -y nodejs
fi
cd meshbaker && npm install --legacy-peer-deps

echo 'Installation complete!'