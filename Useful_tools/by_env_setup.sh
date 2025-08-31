#!/bin/bash

# ================================
# Create and set up Behavython environment on macOS
# ================================

eval "$(mamba shell hook --shell bash)"

ENV_NAME="behavython"

echo "=== [STEP 1] Creating environment '${ENV_NAME}' with Python 3.10.18 ==="
mamba create -y -n $ENV_NAME python==3.10.18

echo "=== [STEP 2] Installing Python packages with pip inside '${ENV_NAME}' ==="

echo "--- Installing numpy ---"
mamba run -n $ENV_NAME pip install "numpy<2.0"

echo "--- Installing matplotlib ---"
mamba run -n $ENV_NAME pip install "matplotlib==3.8.3"

echo "--- Installing seaborn ---"
mamba run -n $ENV_NAME pip install seaborn

echo "--- Installing openpyxl ---"
mamba run -n $ENV_NAME pip install openpyxl

echo "--- Installing tensorflow ---"
mamba run -n $ENV_NAME pip install "tensorflow<2.11"

echo "--- Installing opencv-python ---"
mamba run -n $ENV_NAME pip install "opencv-python<4.10"

echo "--- Installing tables ---"
mamba run -n $ENV_NAME pip install tables

echo "--- Installing scikit-image ---"
mamba run -n $ENV_NAME pip install scikit-image

echo "--- Installing pyyaml ---"
mamba run -n $ENV_NAME pip install pyyaml

echo "--- Installing tqdm ---"
mamba run -n $ENV_NAME pip install tqdm

echo "--- Installing debugpy ---"
mamba run -n $ENV_NAME pip install debugpy

echo "--- Installing tensorpack ---"
mamba run -n $ENV_NAME pip install tensorpack

echo "--- Installing tf_slim ---"
mamba run -n $ENV_NAME pip install tf_slim

echo "--- Installing deeplabcut[gui] ---"
mamba run -n $ENV_NAME pip install "deeplabcut[gui]"

echo "--- Installing PySide6 ---"
mamba run -n $ENV_NAME pip install "pyside6==6.7.3"

echo
echo "======================================================"
echo "!!! IMPORTANT NOTICE !!!"
echo "We are about to run a command with 'sudo'."
echo
echo "This requires your macOS password to grant administrative"
echo "permissions because the repository will be cloned into"
echo "/opt/behavython, a protected system folder."
echo
echo "Your password will not be displayed on the screen as you type."
echo "Please enter it carefully when prompted."
echo
echo "This is necessary to allow the script to place files in /opt,"
echo "which is normally restricted to administrator access."
echo "======================================================"
echo

echo
echo "=== [STEP 3] Cloning Behavython repository ==="
echo

# Remove existing folder if it exists
if [ -d "/opt/behavython" ]; then
    echo "=== Removing existing /opt/behavython folder ==="
    sudo rm -rf /opt/behavython
fi

sudo git clone https://github.com/mrdrzit/behavython.git /opt/behavython

echo
echo "=== [STEP 4] Changing the directory to opt/behavython ==="
cd /opt/behavython

echo
echo "=============================="
echo "✅ Setup complete! Starting a new shell with '${ENV_NAME}' activated..."
echo "Now, test that everything is working by opening the interface by typing (with no quotes): "
echo "python by_front.py"
echo "=============================="

# Start a new interactive bash shell with the environment activated
exec bash --rcfile <(echo "eval \"\$(mamba shell hook --shell bash)\"; mamba activate $ENV_NAME")