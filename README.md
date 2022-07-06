# Automatic Tik Talk

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
```

# Training

Place your LJSpeech dataset in the "example" folder
```
bash start_training.sh

```

Pipeline Troubleshooting

`Could not load dynamic library 'libcufft.so.10'; dlerror: libcufft.so.10: cannot open shared object file: No such file or directory`
```
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-ubuntu2004.pin
sudo mv cuda-ubuntu2004.pin /etc/apt/preferences.d/cuda-repository-pin-600
sudo apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/7fa2af80.pub
sudo add-apt-repository "deb https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/ /"
sudo apt-get update
```