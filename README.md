# Automatic Tik Talk

Fork of https://github.com/SortAnon/ControllableTalkNet.

Should work out of the box. Runs on GPU instances. Driver/CUDA setup is not part of these instructions, but assuming you can run accelerated PyTorch you should be OK.

This fork adds a standalone server w/ direct API instead of Jupyter-Dash, and multi-character support for quick swap (lag-free synthesis in a server setting).

Though this project comes with sample characters, none of that data is in this repo. This project just links to the GDrive ids of various people and projects, largely pones at https://www.kickscondor.com/pony-voice-preservation-project/.

Research is here: https://docs.google.com/document/d/1xe1Clvdg6EFFDtIkkFwT-NPLRDPvkV4G675SUKjxVRU/edit

Datasets:

https://mega.nz/folder/jkwimSTa#_xk0VnR30C8Ljsy4RCGSig/folder/OloAmDqZ
https://mega.nz/folder/gVYUEZrI#6dQHH3P2cFYWm3UkQveHxQ/folder/JQ43mCyB

## Building dataset from YouTube

Check the (README)[youtube/README.md] in the youtube folder on how to build an LJSpeech dataset from youtube data. Even if it's imperfect, should get you started.

## Install

```sh

# install
sudo apt-get install sox libsndfile1 ffmpeg
pip install -r requirements.txt

# for windows
pip install -r requirements-windows.txt
```

# create data directory
mkdir /content
cd /content

# clone some stuff

if [ ! -e hifi-gan ]; then
    !git clone -q --recursive https://github.com/SortAnon/hifi-gan
fi

git clone -q https://github.com/SortAnon/ControllableTalkNet
cd /content/ControllableTalkNet
git archive --output=./files.tar --format=tar HEAD
cd ..
tar xf ControllableTalkNet/files.tar
rm -rf ControllableTalkNet

# Run

python3 controllable_talknet.py

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
```
