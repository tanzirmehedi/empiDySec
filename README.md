# TensorFlow 2.11 GPU Setup on WSL2

Run the entire setup in one go. This will:
- Install Miniconda (if not already installed)
- Create environment
- Install CUDA + cuDNN
- Install TensorFlow 2.11
- Fix libraries
- Test GPU
- Make configuration permanent

---

```bash
# ================================
# 1. Check GPU visibility
# ================================
nvidia-smi

# ================================
# 2. Install Miniconda (skip if already installed)
# ================================
cd ~
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
source ~/.bashrc

# ================================
# 3. Accept Conda Terms (ignore if already accepted)
# ================================
conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/main || true
conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/r || true

# ================================
# 4. Create environment
# ================================
conda create -n tf211gpu python=3.10 -y
conda activate tf211gpu

which python
python --version

# ================================
# 5. Install CUDA & cuDNN
# ================================
conda install -c conda-forge cudatoolkit=11.2 cudnn=8.1.0 -y

# ================================
# 6. Install TensorFlow 2.11
# ================================
pip install --upgrade pip setuptools wheel
pip install tensorflow==2.11.0

# ================================
# 7. Verify installation
# ================================
conda list | egrep "tensorflow|cudatoolkit|cudnn"

echo $CONDA_PREFIX
ls -l $CONDA_PREFIX/lib/libcudart.so*
ls -l $CONDA_PREFIX/lib/libcudnn.so*

# ================================
# 8. Fix CUDA symlinks
# ================================
cd $CONDA_PREFIX/lib
ln -sf libcudart.so libcudart.so.11.0
ln -sf libcudnn.so libcudnn.so.8

# ================================
# 9. Export library path (CRITICAL)
# ================================
export LD_LIBRARY_PATH="$CONDA_PREFIX/lib:$LD_LIBRARY_PATH"
echo "LD_LIBRARY_PATH=$LD_LIBRARY_PATH"

# ================================
# 10. Test CUDA libraries
# ================================
python - <<'PY'
import ctypes
ctypes.CDLL("libcudart.so.11.0")
print("✔ CUDA runtime loaded")
ctypes.CDLL("libcudnn.so.8")
print("✔ cuDNN loaded")
PY

# ================================
# 11. Test TensorFlow GPU
# ================================
python - <<'PY'
import os
import tensorflow as tf

print("\n===== TensorFlow GPU Test =====")
print("TF version:", tf.__version__)
print("Built with CUDA:", tf.test.is_built_with_cuda())
print("LD_LIBRARY_PATH:", os.environ.get("LD_LIBRARY_PATH"))
print("GPUs:", tf.config.list_physical_devices('GPU'))
PY

# ================================
# 12. Make LD_LIBRARY_PATH permanent
# ================================
mkdir -p "$CONDA_PREFIX/etc/conda/activate.d"

cat > "$CONDA_PREFIX/etc/conda/activate.d/env_vars.sh" <<'EOF'
export LD_LIBRARY_PATH="$CONDA_PREFIX/lib:$LD_LIBRARY_PATH"
EOF

# ================================
# 12. Jupyter Notebook
# ================================

conda activate tf211gpu
pip install notebook
export LD_LIBRARY_PATH="$CONDA_PREFIX/lib:$LD_LIBRARY_PATH"
jupyter notebook

# Jupyter Verification Cell

import os
import tensorflow as tf

print("TensorFlow Version:", tf.__version__)
print("Built with CUDA:", tf.test.is_built_with_cuda())
print("LD_LIBRARY_PATH:", os.environ.get("LD_LIBRARY_PATH"))
print("Available GPUs:", tf.config.list_physical_devices('GPU'))

echo "Setup complete!"
