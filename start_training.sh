ipython --TerminalIPythonApp.file_to_run=TalkNet_Training_Offline.ipynb

#!/bin/sh
# TODO: rename all files in example/wavs from zhongli-*.wav to example-*.wav
# Path: rename_wavs.sh
for file in `ls example/wavs/*.wav`; do mv $file `echo $file | sed 's/zhongli-/example-/'`; done