# Install

```sh

# install
sudo apt-get install sox libsndfile1 ffmpeg
pip install tensorflow==2.4.1 dash==1.21.0 dash-bootstrap-components==0.13.0 jupyter-dash==0.4.0 psola wget unidecode pysptk frozendict torchvision==0.9.1 torchaudio==0.8.1 torchtext==0.9.1 torch_stft kaldiio pydub pyannote.audio g2p_en pesq pystoi crepe resampy ffmpeg-python torchcrepe einops taming-transformers-rom1504==0.0.6 tensorflow-hub
python -m pip install git+https://github.com/SortAnon/NeMo.git

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
```
