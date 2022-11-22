# Webaverse TTS

Fast text-to-speech based on NeMo and Talk net, forked from this repo: https://github.com/SortAnon/ControllableTalkNet.

Though this project comes with sample characters, none of that data is in this repo. This project just links to the GDrive ids of various people and projects, largely pones at https://www.kickscondor.com/pony-voice-preservation-project/.

# Training

Tools are provided here for creating datasets, as well as a training notebook that should "just work".
https://github.com/webaverse/LJSpeechTools

# TikTalknet Installation (works on AWS and CoreWeave)

Currently requires python 3.8

First we need to install anaconda. Anaconda is a python environment manager, which lets us create multiple separate virtual environments and install Python packages into them. It works with pip, and will make working with Python a lot easier.

Here's how to install Anacaonda
```bash
wget https://repo.anaconda.com/archive/Anaconda3-2022.05-Linux-x86_64.sh
bash Anaconda3-2022.05-Linux-x86_64.sh
# proceed through instructions
source ~/.bashrc # reset the bash terminal
conda # should bring up the conda menu
```

We will create the environment and install python 3.8 into it
```bash
conda create env --name 'voice' python==3.8
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

You need to run the server on port 80 which requires sudo, also you might be SSH'd in so you want to exit the session but leave everything running using nohup
```bash
sudo nohup /home/ubuntu/anaconda3/envs/voice/bin/python3.8 controllable_talknet.py > out.log 2> out.err < /dev/null &
```

### Could not load dynamic library 'libcudart.so.11.0'

CUDA is not installed. We need CUDA 11.0. Follow instructions here: https://developer.nvidia.com/cuda-11.0-download-archive

## Could not import Denoiser from denoiser
The denoiser file is locally referenced in the hifi-gan folder
Clone hifi-gan (above) and make sure you pip uninstall denoiser if you tried that
