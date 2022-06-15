# Automatic Tik Talk

This program automates and performs the steps presented in https://github.com/Appen/UHV-OTS-Speech to easily create high-quality speech datasets through a number of pretrained machine learning models. In particular we are connecting it to TalkNet to drive fast, responsive AI.

- Requirements:
    - Poetry installed

- Setup:
    - The program parses the /input folder to create speaker datasets. 
    - Simply create a subfolder, named after the speaker, and include any audio files you want to be parsed.
    - Additionaly, you can include a file named sources.json with youtube videos to be scraped and downloaded (example in /input/JuiceWRLD)

- Running:
    - Once inputs are prepared, simply run the program with "poetry run python pipeline.py"
    - The pipeline will parse inputs, scrape audio sources, and run through each step of the pipeline as explained below
    - If some steps need to be excluded, they can be easily commented out in the main loop of pipeline.py

- Pipeline:
    - Pre-Processing:
        - Synthetic Detection:
            - This model is trained to specifically detect synthetic speech (TTS) that if included in the speech dataset, would cause undesied results. 
                - Sections of the audio recordings it determines to be synthetic will be spliced and discarded now, so we don't have to worry about this

        - Source Separation:
            - This model is trained to split an audio recording into two separate files, one containing only the speech audio channel, and one containing only the background audio channel
                - The background audio will be discarded, and the rest of the pipeline works on the isolated speech.
                - This is useful to remove background sound that would otherwise be included (wind blowing, highway sounds) but can also be used to isolate vocals from music, allowing for the creation of specific datasets for people singing, rapping, etc 

    - Pre-Tagging:
        - Speech Detection:
            - This model detects sections of speech in an audio clip (without transcribing it), and produces a file with timestamped sections of speaking, silence, and other noise.
                - All non-speech sections can be discarded, greatly decreasing pipeline runtime by only running the following models on actual speech

        - Speaker Segmentation:
            - This model attempts to differentiate between speakers in the audio file, assigning a speaker label to each transcribed audio file
                - Audio files from other speakers can then be discarded (likely one of the big problems in prev. pipeline)

        - Speech Transcription:
            - This model transcribes the audio files from the desired speaker, producing a file with timestamped captions for each audio file

        - Topic Detection:
            - This model parses the transcribed audio files and assigns a topic label to each one
                - This has some interesting possibilities, could use it to create specific models for when speakers are talking about sad stuff, are angry, etc. Could be cool but maybe not necessary


# CUDA-based character voice synthesis

Fork of https://github.com/SortAnon/ControllableTalkNet.

Should work out of the box. Runs on GPU instances. Driver/CUDA setup is not part of these instructions, but assuming you can run accelerated PyTorch you should be OK.

This fork adds a standalone server w/ direct API instead of Jupyter-Dash, and multi-character support for quick swap (lag-free synthesis in a server setting).

Though this project comes with sample characters, none of that data is in this repo. This project just links to the GDrive ids of various people and projects, largely pones at https://www.kickscondor.com/pony-voice-preservation-project/.

Research is here: https://docs.google.com/document/d/1xe1Clvdg6EFFDtIkkFwT-NPLRDPvkV4G675SUKjxVRU/edit

Datasets:
- https://mega.nz/folder/jkwimSTa#_xk0VnR30C8Ljsy4RCGSig/folder/OloAmDqZ
- https://mega.nz/folder/gVYUEZrI#6dQHH3P2cFYWm3UkQveHxQ/folder/JQ43mCyB

## Install

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

# Run

python3 controllable_talknet.py
```
