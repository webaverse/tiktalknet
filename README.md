# Automatic Tik Talk

Fork of https://github.com/SortAnon/ControllableTalkNet.

Though this project comes with sample characters, none of that data is in this repo. This project just links to the GDrive ids of various people and projects, largely pones at https://www.kickscondor.com/pony-voice-preservation-project/.

Datasets:

https://mega.nz/folder/jkwimSTa#_xk0VnR30C8Ljsy4RCGSig/folder/OloAmDqZ
https://mega.nz/folder/gVYUEZrI#6dQHH3P2cFYWm3UkQveHxQ/folder/JQ43mCyB

## Building dataset from YouTube

Check the (README)[youtube/README.md] in the youtube folder on how to build an LJSpeech dataset from youtube data. Even if it's imperfect, should get you started.

# TikTalknet Installation (works on AWS and CoreWeave)

Currently requires python 3.7

First we need to install anaconda. Anaconda is a python environment manager, which lets us create multiple separate virtual environments and install Python packages into them. It works with pip, and will make working with Python a lot easier.

Here's how to install Anacaonda
```bash
wget https://repo.anaconda.com/archive/Anaconda3-2022.05-Linux-x86_64.sh
bash Anaconda3-2022.05-Linux-x86_64.sh
# proceed through instructions
source ~/.bashrc # reset the bash terminal
conda # should bring up the conda menu
```

We will create the environment and install python 3.7 into it
```bash
conda create env --name 'voice' python==3.7
```

Now we need to activate it
```bash
conda activate voice
```

Next we will install some basic dependencies into Linux.

First, update apt
```bash
apt update # you will probably need sudo
```

Next, install these dependencies
```bash
apt-get install sox libsndfile1 ffmpeg # you will probably need sudo
```

Most machine learning stuff uses CUDA, which is a low-level library for interacting with the GPU. The easiest way to solve this is to install cudatoolkit using conda.
```bash
conda install cudatoolkit
```

Now we will install the basic python dependencies we need for inference
```bash
pip install tensorflow==2.4.1 dash==1.21.0 dash-bootstrap-components==0.13.0 jupyter-dash==0.4.0 psola wget unidecode pysptk frozendict torchvision==0.9.1 torchaudio==0.8.1 torchtext==0.9.1 torch_stft kaldiio pydub pyannote.audio g2p_en pesq pystoi crepe resampy ffmpeg-python torchcrepe einops taming-transformers-rom1504==0.0.6 tensorflow-hub werkzeug==2.0.3 editdistance gdown

# or
pip install -r requirements.txt
pip install -r requirements-windows.txt

```

We are using a custom (read: old) version of NeMo. Talk Net was deprecated in newer versions, so we need to use this one and install it directly from Github:
```bash
python -m pip install git+https://github.com/SortAnon/NeMo.git
```

Now we need to add the HiFi GAN dependencies
```bash
git clone -q --recursive https://github.com/SortAnon/hifi-gan
```

You need to run the server on port 80 which requires sudo, also you might be SSH'd in so you want to exit the session but leave everything running using nohup
```bash
sudo nohup /home/ubuntu/anaconda3/envs/voice/bin/python3.7 controllable_talknet.py > out.log 2> out.err < /dev/null &
```

### ValueError: numpy.ndarray size changed, may indicate binary incompatibility. Expected 88 from C header, got 80 from PyObject
```bash
pip install numpy==1.20.0
```

### Could not load dynamic library 'libcudart.so.11.0'

CUDA is not installed. We need CUDA 11.0. Follow instructions here: https://developer.nvidia.com/cuda-11.0-download-archive

## Could not import Denoiser from denoiser
The denoiser file is locally referenced in the hifi-gan folder
Clone hifi-gan (above) and make sure you pip uninstall denoiser if you tried that


# Training

1. put LJSpeech-formatted dataset into /example folder, replacing metadata.csv and wavs
2. edit train_filelist.txt and val_filelist.txt (just split metadata.csv 90/10% between them)
3. follow installation intrusctions for dependencies
4. `bash start_training.sh`

### Pipeline Troubleshooting

`Could not load dynamic library 'libcufft.so.10'; dlerror: libcufft.so.10: cannot open shared object file: No such file or directory`
```
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-ubuntu2004.pin
sudo mv cuda-ubuntu2004.pin /etc/apt/preferences.d/cuda-repository-pin-600
sudo apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/7fa2af80.pub
sudo add-apt-repository "deb https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/ /"
sudo apt-get update
