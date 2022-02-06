# Install

```python
import os

custom_lists = [
    #"https://gist.githubusercontent.com/SortAnon/997cda157954a189259c9876fd804e53/raw/example_models.json",
]

!apt-get install sox libsndfile1 ffmpeg
!pip install tensorflow==2.4.1 dash==1.21.0 dash-bootstrap-components==0.13.0 jupyter-dash==0.4.0 psola wget unidecode pysptk frozendict torchvision==0.9.1 torchaudio==0.8.1 torchtext==0.9.1 torch_stft kaldiio pydub pyannote.audio g2p_en pesq pystoi crepe resampy ffmpeg-python torchcrepe einops taming-transformers-rom1504==0.0.6 tensorflow-hub
!python -m pip install git+https://github.com/SortAnon/NeMo.git
if not os.path.exists("hifi-gan"):
    !git clone -q --recursive https://github.com/SortAnon/hifi-gan
!git clone -q https://github.com/SortAnon/ControllableTalkNet
os.chdir("/content/ControllableTalkNet")
!git archive --output=./files.tar --format=tar HEAD
os.chdir("/content")
!tar xf ControllableTalkNet/files.tar
!rm -rf ControllableTalkNet

os.chdir("/content/model_lists")
for c in custom_lists:
    !wget "{c}"
os.chdir("/content")
```
