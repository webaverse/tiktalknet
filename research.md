(This was pulled from the document on dataset creation by the Pony Preservation Project)
Original documents are here:
https://u.smutty.horse/mhmqxnbjaye.docx
https://u.smutty.horse/mhmqxnefvuj.pdf

# Tutorials

## Creating an audio dataset

This is a guide on how to create a dataset of raw voice clips and text transcripts for any given source of audio. The output of this process can then be used to create a dataset for [training in Google Colab](https://docs.google.com/document/d/1DydIFRGW-vyjvQFIJMKvQvSs2o_UO_apO0-yBZ4181E/edit#heading=h.wyltjtimrkhb) and/or submitted to 15 ([fifteenai15@gmail.com](mailto:fifteenai15@gmail.com)) for potential use at [https://fifteen.ai/](https://fifteen.ai/)

Note that our system uses a file naming system different to that specified for contributions on 15.ai, however 15 is able to use the pony dataset without issue so it should be fine to submit your datasets to him using the same format we do. Just make sure you follow the format closely and note in your submission that you used the same system as us. Alternatively, you could adapt the PPP method to use a different naming system if you prefer. Please also share any datasets you create in the thread, more data is always helpful.

Before you start any work, please post in the current PPP thread about what you plan to do so other Anons know what&#39;s being worked on.

[See also the section on cleaning audio](#_tquzods4u1et) if your audio source contains undesirable elements such as sound effects that obstruct the voice.

To submit your contributions, please [follow the guidelines for submitting your content](https://docs.google.com/document/d/1DydIFRGW-vyjvQFIJMKvQvSs2o_UO_apO0-yBZ4181E/edit#heading=h.z3h8i1lam648) when you are done.

See also the &quot;[Automatic Clipping and Transcribing](#_39533kjed61h)&quot; section for an alternate method.

If you have any questions about the process, ask Clipper in the thread.

## Overview

**The full process is demonstrated by Clipper in** [**this YouTube video.**](https://www.youtube.com/watch?v=Bsu7mwa-QGY)

The goal of this process is to take the full cut of an audio source and slice it into its individual lines, which will all be tagged with data such as the character speaking, the emotion with which the line is spoken and a full transcript of all the words spoken in each line.

Here is an overview of the core steps of the dataset creation process:

1. Obtain audio for your chosen character
2. Obtain subtitle .srt file and transcript, if possible.
3. Download Audacity, Notepad++, and Python.
4. Use the subtitle to Audacity app, if you were able to get a subtitle file.
5. Run the character tagger program, if you were able to get a compatible transcript.
6. Import the audio files into Audacity, and then create and edit labels as needed.
7. Export labels from Audacity and run them through the checking script, correcting any errors it finds.
8. Re-import the corrected labels into Audacity and export the audio clips.
9. Create a text transcript of all the newly created audio clips.
10. Upload all the files you&#39;ve created.

We will now explain the process of each of these steps in more detail.

### Obtaining Audio

There are several potential sources of audio, and some sources will be better than others. Here are some suggested sources, in order of most ideal to least ideal:

- Raw studio recordings
- PC game files
- Audiobooks and podcasts
- Netflix and iTunes videos
- YouTube videos

Raw studio recordings are often the hardest to obtain but will offer perfectly clean studio quality voices which are the best source of any audio. We were lucky enough to get some studio recordings for various MLP episodes from BigHckintosh as part of the Hasbro studio leaks.

The sound files in PC game files are often similar in quality to raw studio recordings and are easier to obtain. If you&#39;re training for a character or voice actor that appears in a video game, go digging through the files and see what you can find. You can also consult forums dedicated to the particular game if finding the specific files proves difficult.

Audiobooks and podcasts are also usually recorded in proper sound studios, but will also tend to have undesirable elements such as music and sound effects mixed in. These are often easily accessible on their respective host websites, and you can even download podcasts directly from iTunes.

Shows hosted on Netflix and iTunes are usually in high quality, but will almost certainly contain sound effects and background music which will obstruct the voices. This can be mitigated to an extent, but it&#39;s never going to be as good as the raw recordings. For iTunes, you can simply download videos directly. To download videos from Netflix, you will need to use [Flixgrab](https://www.flixgrab.com/). For both Netflix and iTunes, make sure that the video you download has 5.1 audio, a format which should allow you to isolate and remove background music. You can usually find audio information like this in the detailed video descriptions. Note that obtaining 5.1 rips of audio in multiple languages will also be useful for removing background noise.

A YouTube video can be used if there is no material available on Netflix or iTunes, but is a much less ideal source as compression will compromise audio quality. The audio will also only be available in stereo, which means you won&#39;t be able to remove any music. Only use YouTube if there is literally no other viable option. Search for &quot;youtube downloader&quot; in Google for various online solutions to directly download videos from YouTube.

As a general rule, you should aim to obtain at least thirty minutes of audio for your chosen character before attempting training. This is the minimum amount of data you need to guarantee a reasonable chance of getting a decent output from your model. As with all applications of artificial intelligence, more good quality data will result in a more accurate model, so you should always aim to gather as much data for your chosen character as you can.

### Obtaining Subtitles and Transcripts

Subtitles contain information on the content of speech and the time it occurs, which we can use to create Audacity labels to give us a head start. It may be possible to rip these files from a Blu-Ray disk, or they may be found online [here](https://www.addic7ed.com/). You can also use [this programme](https://www.dvdvideosoft.com/free-youtube-subtitles-download) to download subtitles from YouTube videos, make sure you download in .srt format.

We have also created a tool to automatically tag characters to their lines with the help of a transcript. For this tool to work, you will need a transcript in the same format [as shown here.](https://mlp.fandom.com/wiki/Transcripts/Friendship_is_Magic,_part_1) You may be able to find a transcript like this for your show at [https://www.fandom.com/](https://www.fandom.com/). Even if you can&#39;t find a transcript in this exact format, it can still be used as a source to copy-paste from to help with transcribing lines later on.

If you can&#39;t find .srt files and/or a transcript for your audio, don&#39;t worry too much. This step is optional, though having these files will make your life much easier later on so it is strongly recommended to make every reasonable effort to find them.

### Acquiring Software

Audacity is a free open-source audio editor, we will use it to do the work of slicing the audio into its individual lines. Download Audacity [here.](https://www.audacityteam.org/)

Notepad++ is an enhanced version of notepad for editing text files. We will demonstrate some of its useful features later. Download Notepad++ [here.](https://notepad-plus-plus.org/downloads/)

Python will allow us to run scripts to automate some steps for editing Audacity labels later. Don&#39;t worry if you don&#39;t have any expertise in coding, we won&#39;t be doing anything complicated and all the steps are fully demonstrated in the video. Download Python [here.](https://www.python.org/)

Simply download and install these in the same way you would for any other programme.

If you are using a Netflix/iTunes/YouTube video as your audio source, you will need to isolate the audio from the video. The easiest way to do this is to install the FFMPeg plugin for Audacity, which will allow you to import video files just like you would for an audio file. Instructions for the Audacity plugin can be found [here](https://manual.audacityteam.org/man/installing_ffmpeg_for_windows.html).

### Subtitle to Audacity Tool

If you weren&#39;t able to get a subtitle .srt file, you can skip this step and also the Character Tagger step. [Click here to skip this section](#_dt6j5eyzo9id).

[Open the .srt to Audacity app here.](https://www.construct.net/en/free-online-games/srt-audacity-5165/play)

![](RackMultipart20220621-1-7cig3a_html_940bfc94fd501bd3.png)

This is the subtitle to Audacity converter. It will generate Audacity labels with the information in the subtitle file, which will give us a head start. To use it, simply open the subtitle file in the app, then click merge overlapping labels. This will merge any subtitles with overlapping timestamps into a single label. I recommend you leave the other two options blank. We will automatically generate timestamps later, and the safe filename option will remove question marks, which you will have to retype later.

The drop-down option will allow you to choose a formatting option for the output. You can use whichever formatting you want. Run the app, and save the output in a useful place.

If you were able to find a suitable transcript for your audio for use with the character tagger, go to the next section now. If not, keep reading.

Open the output of the subtitle to Audacity app in Notepad++ and use a macro to add three underscores to the start of every label. The use of macros in Notepad++ is [demonstrated in the video here.](https://youtu.be/Bsu7mwa-QGY?t=485) Once done, [follow this demonstration in the video](https://youtu.be/Bsu7mwa-QGY?t=522) to make some minor edits to the labels before importing them into Audacity.

### Character Tagger

If you weren&#39;t able to get a transcript in the format shown [earlier](#_y41g4uw56p2n), you can skip this step. [Click here to skip this section](#_dt6j5eyzo9id).

![](RackMultipart20220621-1-7cig3a_html_e5d31956f5352386.png)

This is the Character Tagger. It will attempt to match every spoken line to a character by comparing the lines to a transcript. Open the output from the subtitle to audacity app from the previous step in the middle box, and then copy and paste the transcript in the left box. In the suffix box, type in three underscores, and then click label unknown characters. Exactly why we do this will become clear in the next step. Run the programme and save the output in a useful place.

Open the output of the Character Tagger in Notepad++ and [follow this demonstration in the video](https://youtu.be/Bsu7mwa-QGY?t=522) to make some minor edits to the labels before importing them into Audacity.

### Clipping Audio in Audacity

[This process is demonstrated in full in the video.](https://youtu.be/Bsu7mwa-QGY?t=621) I suggest you use the video as your primary source of information here as I feel that a live demo explains the process better than can be done with simple text and screenshots.

Open the dialogue audio file in Audacity. Once the audio has finished loading select &quot;File&quot; -\&gt;&quot; Import&quot; -\&gt; &quot;Labels&quot; in the menu. Choose the label file that we just created in the previous step. If you skipped the subtitle to Audacity step, you won&#39;t have any labels to import and will instead need to create them manually. Create a label track by selecting &quot;Tracks&quot; -\&gt; &quot;Add new&quot; -\&gt; &quot;Label Track&quot;. [See this section of the demo video](https://youtu.be/Bsu7mwa-QGY?t=1145) for a guide on creating labels manually.

![](RackMultipart20220621-1-7cig3a_html_2f7fd6006a1c13cf.png)

The idea here is to draw labels around all the individual lines of dialogue, and then fill those labels with the information we need. The start and end points of each label will mark the start and end point of each clip. The black vertical bars in the label track represent label boundaries, beginning and end. Clicking and dragging on either will allow you to start a selection from that point. The circular buttons on either end of the label text allow you to move the entire label in time, and the triangles attached to the circles allow you to move the beginning or end individually. You can create new labels if needed by highlighting a section of audio and pressing &quot;Ctrl+B&quot;.

Use this to create and adjust labels as needed. You may combine labels as needed if the audio doesn&#39;t split well on the existing bounds between two labels, though there&#39;s no automatic way of doing this. Simply right click on and delete the second label and extend the first one to compensate.

Audio clips should contain about a sentence worth of dialogue, but it is most important that your clips are split in a way that sounds natural. Do not let clips start part way into a word or let them end in the middle of one. Try to clip such that the emotion conveyed by the tone of voice is consistent throughout. Audio clips should also contain entirely noisy or entirely clean audio, so take this into account as well when deciding where to put your clip boundaries. When filling in the labels, you must make sure to include all the necessary information in the format shown below:

![](RackMultipart20220621-1-7cig3a_html_12952520348a157d.png)

Timestamp - Ignore the timestamp while filling in the labels in Audacity, we will automatically generate it later.

Character - You can use abbreviations for tagging characters while clipping your audio to save time, for example &quot;twi&quot; for &quot;Twilight&quot;. You can use whatever abbreviations you want, just make sure you keep a note of what you have used for future reference, you will need to enter the abbreviations you&#39;ve used into the checking script in the next section.

Emotion - The suggested list to use is: Neutral (n), Happy (h), Amused (am), Sad (s), Annoyed (a), Angry (ag), Disgust (d), Sarcastic (sa), Smug (sm), Fear (f), Anxious (ax), Confused (c), Surprised (su), Tired (t), Whispering (w), Shouting (sh), Whining (wh) and Crazy (cr). It is suggested to use the one or two letter abbreviations given in the brackets for quicker and easier tagging, these abbreviations will be expanded into their full versions with the use of the checking script in the next section. If appropriate, you can use multiple emotion tags in a clip, such as &quot;Happy Shouting&quot; or &quot;Angry Whispering&quot;. In these cases, make sure that the tags are separated by a space. You can also invent and use other emotion tags if you feel that none of the emotions listed above fit your audio. If you do this, make sure to keep a note of what you have used for future reference, you will also need to enter the abbreviations you&#39;ve used into the checking script in the next section.

Noise - This is a difficult concept to explain as it&#39;s always going to come down to a judgement call. It is important to get this right, so make sure you put on a decent pair of headphones and listen carefully. If a clip is clean, that is free from all but the most trivial of noise, then leave the noise tag blank. Make sure that the underscores are still included. If there is significant noise in a clip, then you will need to make a judgement call. Marking it as noisy is effectively you saying that you would be happy to use that clip for training, despite the small amount of noise it still has. Marking the clip as very noisy is effectively you saying that the clip is unsuitable for training due to excessive noise. Generally speaking, for a clip to qualify as noisy, you should be able to clearly make out all syllables of every spoken word, and the noise itself should be quieter than the speech. It&#39;s usually best to be strict for the sake of preserving quality, so If you find yourself in doubt between clean and noisy, tag it as noisy. Similarly, if you find yourself in doubt between noisy and very noisy, tag it as very noisy. Use the shorthand &quot;q&quot; for noisy and &quot;qq&quot; for very noisy.

Dialogue - The transcript must contain every word that is spoken in each clip, exactly as spoken, with correct spelling and punctuation. Remember that all pauses should be represented by a comma or full stop, whichever fits best. All sentences should end with either a full stop, a question mark, or an exclamation mark. A sentence should not end with a comma. Also be careful not to make the clip too long, as everything you enter into the label will later become the filename for that clip. Windows imposes a hard cap of 260 characters for a filename, including the directory. As a general rule, each label should contain about one sentence of speech. The length should be at least one second, and no more than ten seconds. You can combine and split labels however you feel is best.

Keep in mind to not make the label of the clips too long, as what you enter into the label will later become the filename of that clip. Unfortunately Windows, being a shit OS, has a hard file name limit of 260 characters. Note that the character limit includes the file directory, so if you find that a filename has become too long to edit, try moving it out of folders/subfolders and into just the &quot;Documents&quot; section in the file explorer. This will shorten the directory path and allow you to edit filenames that would otherwise exceed the character limit.

Example:

C:\Users\Anon\Documents\PVPP\Sliced Dialogue\FiM\S1\s1e1\00\_00\_05\_Celestia\_Neutral\_\_Once upon a time, in the magical land of Equestria..flac (135 characters)

C:\Users\Anon\Documents\00\_00\_05\_Celestia\_Neutral\_\_Once upon a time, in the magical land of Equestria..flac (102 characters)

After editing the filename, you can then move it back into the original folder/subfolder, even if it exceeds the character limit.

I&#39;ll recommend again that you [watch the section in the demo video](https://youtu.be/Bsu7mwa-QGY?t=621) that covers this section, as a live demo will communicate the process better.

### Checking Script

We have now made the labels in Audacity with the character, emotion and noise tags and transcript. The next step is to make sure that there are no mistakes and add the timestamp to the start of each label. Refer back to the file naming system for details on the format of the timestamp.

Before following any of the instructions below, make sure you have exported the Audacity labels. File -\&gt; Export -\&gt; Export labels. Name the file &quot;labelsraw.txt&quot;.

The checking script is available [here.](https://pastebin.com/2B2skWsv) It will do the following:

- Replace shorthand character, emotion and noise tags with their full versions.
- Add a timestamp to the start of each label in the correct format.
- Check for some common abbreviations in the dialogue that should be expanded into their full versions, such as Mr. for mister.
- Check for any numbers in the dialogue that should be replaced with the word version.
- Adds a full stop to the end of any label that does not end with any sort of punctuation.

I will write out the full process for using the script, [but I highly recommend watching the demonstration in the video](https://youtu.be/Bsu7mwa-QGY?t=1363). I feel it does a much better job of explaining than can be done with just text and screenshots.

To use the script, copy and paste it into a new Notepad++ file, and save it with a .py extension. This will save it as a Python executable. You can name the script whatever you want, the extension is the only thing that matters here. Create a new folder for the script and save it there, making sure there is nothing else in that folder.

From lines 158 to 398, you can see the stored information for shorthand character codes. You can add, remove and change any entries as needed, just make sure it&#39;s all in the same format as seen in the script, this is demonstrated in the video. The script will check for any abbreviations in the character field, and replace any it finds with its corresponding full version. It can also check for longer character tags and replace them with a shortened version.

From lines 400 to 423, you will see the entries for emotion. From lines 425 and 428, you will see the entries for noise. From lines 430 to 433, you will see the entries for abbreviations. These all work in the exact same way as for the characters, and you can also add to and edit these however you like, just make sure the formatting is kept consistent.

We now need to do just one more thing before we&#39;re ready to run the script. We need to tell the system to run the script in the console window so we can see its output as it goes through the labels. Create a new file in notepad++, and type the following:

@echo off

python filename.py

pause

Replace &quot;filename&quot; with whatever you named the checking script. Save this file as &quot;Run.bat&quot; in the same folder as the checking script. [This process is also demonstrated in the video.](https://youtu.be/Bsu7mwa-QGY?t=1489)

We are now ready to run the checking script. Copy the Audacity label file into the folder containing the checking script, and name it &quot;labelsraw.txt&quot;. Double click run.

You will see in the output &quot;labels.txt&quot; folder that the script has added all the timestamps to the start of each label, and expanded all shorthand tags to their full versions. The demo video contains examples of how the checking script alerts you to any errors.

Once you have fixed all the errors the script has found, run it again on the corrected labelsraw.txt file to make sure nothing was missed. Once done, you can discard the labelsraw.txt file. We now need to do one last check on the output label file. Use find and replace to correct any cases of double spacing, and make sure there are no spaces before or after any of the underscores. Then copy and paste the labels into a word processor, such as Microsoft Word or a Google document and run a spell-check. Fix any spelling errors it finds and copy the corrected labels back into the Notepad++ file. Save the file containing the completed labels.

### Exporting Audio Clips

Import the new labels into your Audacity project and delete the old ones. We are now ready to export the audio to make the individual clips. It is recommended to disable &quot;Show Metadata Tags editor before export&quot; in the &quot;Edit&quot; -\&gt; &quot;Preferences&quot; -\&gt; &quot;Import/Export&quot; menu to prevent a window popping up for every single label in your project.

![](RackMultipart20220621-1-7cig3a_html_a6dd09bf6ba93135.png)
 ![Shape1](RackMultipart20220621-1-7cig3a_html_fd953a0ff2a8627.gif)

Now go to &quot;Export -\&gt; Export Multiple&quot;. Make sure the settings match what you see in the screenshot below, and then select the folder you want to export the clips to. Once done, click export.

Q ![](RackMultipart20220621-1-7cig3a_html_7b9036edf70459c9.png)
 uestion marks are not allowed in filenames, so Audacity will automatically ask you if you want to change them to an underscore. Press the enter key to confirm the change, along with every other label this applies to. Do not spam or hold down the enter key, as this occasionally creates duplicate files.

You may run into an error while exporting that interrupts the process. The most common cause of this is that the filename is too long, remember the 260 character limit for a filename, including the directory. If this happens, simply go to the label that caused the problem, and split it into two shorter ones. If you make any edits to the labels like this, make sure you re-export the updated label file.

The output should look something like this, with all the clips created with a filename according to the label we created in Audacity.

![](RackMultipart20220621-1-7cig3a_html_584eec791bb5e5a1.png)

### Text Transcriptions

We now need to create a text file transcription for all of these audio clips. We need a text file for every single audio file that contains all the words spoken in each clip, and also has the exact same filename as the sound clip it is associated with. You can imagine that doing this manually for several hundred or even thousand clips would be a very long and tedious task, so we have created a script that will do this automatically. The use of this script is very similar to what we did with the checking script earlier [and is demonstrated in the video.](https://youtu.be/Bsu7mwa-QGY?t=1826)

[The script is available here.](https://pastebin.com/1Y1qz4EC) This script will read the dialogue section of Audacity labels and create a text transcript containing that dialogue. This is why it&#39;s important that the dialogue section of every Audacity label is accurate to the spoken dialogue, as any errors in the labels will be replicated in the generated transcript. The script will then save the transcript as a text file with the exact same name as the sound clip it&#39;s associated with.

To use the script, copy and paste it into a new Notepad++ file. Just like we did with the checking script, save this new file with a .py extension to save it as a Python executable. You can name the script whatever you want, just make sure you remember the .py extension. Save the script in its own folder, making sure there is nothing else in the folder. Now create a &quot;Run.bat&quot; file in the same way we did with the checking script, and save it in the same folder.

Copy and paste the text file containing the Audacity labels into the folder with the script, and make sure it is named &quot;labels.txt&quot;. Double click run.

The script will have created a text file transcription of every sound clip and saved it with the exact same name as the clip it&#39;s associated with.

## ![](RackMultipart20220621-1-7cig3a_html_8029227f6d05a062.png)

Now cut and paste the text file transcripts into the same folder that contains the sound clips. The final result should look something like this:

![](RackMultipart20220621-1-7cig3a_html_b36c26387f8243f7.png)

### Submitting Work

The hard work is now done, all that&#39;s left is to submit your content. [As shown earlier, there are several file host options available.](https://docs.google.com/document/d/1DydIFRGW-vyjvQFIJMKvQvSs2o_UO_apO0-yBZ4181E/edit#heading=h.z3h8i1lam648) It doesn&#39;t really matter where you upload your clips, so long as they are easily accessible.

Compress all the sound clips, text transcripts **and the text file containing the Audacity labels** into a zip file, upload to your file host of choice and then post a download link in the current PPP thread. Some recommended file hosts are [Smutty.horse](https://smutty.horse/), [Mega.nz](https://mega.nz/), and [catbox.moe](https://catbox.moe/).

Please do share any datasets you create with us over on /mlp/, we&#39;re always looking for more data to work with to improve our models and processes, especially with characters that have unique speech quirks and a wide range of emotions. You can also try emailing the download link to 15 ([fifteenai15@gmail.com](mailto:fifteenai15@gmail.com)) for use on 15.ai, but he works separately to the PPP so unfortunately no guarantees can be made.

And that&#39;s it, we&#39;re done! This is all we need to do to create a basic dataset of sound clips and transcripts for any given source of audio. If you have any questions or points of clarification on any of the instructions written here or shown in the video, feel free to post them in the current PPP thread. In the thread, you will find me under the name Clipper. You can also email me at [clipper.anon01@gmail.com](mailto:clipper.anon01@gmail.com). I always do my best to respond to all questions about creating datasets.

##


## Automatic Clipping and Transcribing

(Credit to: [\&gt;\&gt;35315142](https://desuarchive.org/mlp/thread/35308325/#35315142) for creating the notebook)

This section is intended to assist with using the Automatic Super Speaker-Filtered Audio Processing (ASSFAP **™** ) Colab notebook. The notebook allows you to use IBM&#39;s Cloud Speech tools to automatically clip and transcribe lines. While automated clipping may not be as accurate as manual clipping, it is a heck of a lot faster. These instructions will largely mirror what is in the notebook itself.

Open the notebook itself here:

[**Colab**](https://colab.research.google.com/drive/18lBRBWOs4uV1DjhoW_fVzoydYUw400PW#scrollTo=ZfO2MFo2qrMi)

The first thing you&#39;ll need to do is open the notebook in the playground. Click the button in the upper left to do so.

![](RackMultipart20220621-1-7cig3a_html_5f41647edb36c67b.png)

On the first code block you run, you will be prompted by Google whether or not you wish to run the notebook. Select &quot;run anyway&quot;.

Before you upload your files to be clipped, you will first need to prepare them. You&#39;ll want to create a folder called &quot;files&quot; and put the audio files you want clipped inside. Make sure that none of the files are over 100mb else IBM&#39;s Cloud Speech tools will error out and the file will be skipped. I recommend using Audacity to cut your files into smaller pieces if needed. Make sure to cut where there is no speech.

Next you will need to create a small sample file of the speaker you wish to clip. It should be between 2 and 6 seconds long. Again, I recommend Audacity for this. Name the file &quot;sample.wav&quot; and place it outside of the file directory. When done it should appear as follows:

![](RackMultipart20220621-1-7cig3a_html_a73d3444f7fd371e.png)

Add the files to a .zip file without any other subdirectories. When you open the zip, you should be able to see the files folder and the sample file.

Next, upload your .zip file to your Google Drive. Once done, you will need to publically share it and get the Drive ID. You will want to store this for later. For example:

![](RackMultipart20220621-1-7cig3a_html_5606349a8dba04f.png)

Another thing you will need to set up is an IBM Cloud account. Do it [**here**](https://cloud.ibm.com/login). Once you have set up your account, you will need to get an API key and URL for the Speech to Text tool. Be aware that the free plan only allows a limited amount of transcriptions per month.

From the dashboard click on &quot;Create Resource&quot; in the upper right hand part of the screen.

![](RackMultipart20220621-1-7cig3a_html_218288966b3b45cf.png)

Click on &quot;Services&quot;.

![](RackMultipart20220621-1-7cig3a_html_68b76195feef586e.png)

Click on &quot;Speech to Text&quot;.

![](RackMultipart20220621-1-7cig3a_html_97ea63bfdb233474.png)

You will be given some options, but you can leave them as is. Click on &quot;Create&quot; in the lower right hand corner.

![](RackMultipart20220621-1-7cig3a_html_63f6fdae0374e91c.png)

With that created you can go back to the dashboard (click the IBM logo at the top). Under resource summary, you should see &quot;services&quot; listed. Click on it.

![](RackMultipart20220621-1-7cig3a_html_7b37912ee1def00f.png)

You&#39;ll then see something similar to below. Click on &quot;Speech to Text-cy&quot;.

![](RackMultipart20220621-1-7cig3a_html_e485503576d15c27.png)

You will then have access to your API key and URL. Note these down for later.

![](RackMultipart20220621-1-7cig3a_html_6a9dab20782b9149.png)

On to the notebook itself now. At the top of the first box you will need to set the sample rate and root path you want to use. If you want to use 22KHz data, leave sarate alone. If you want to do 48KHz, set it to 48000. Change the root path to where in your drive you want the output files saved.

![](RackMultipart20220621-1-7cig3a_html_1798f3798ba05512.png)

Once done, run the first cell. Note that you will need to authorize the notebook to access the contents of your drive when you run the cell (paste the authentication code into the box).

In the second cell, take your .zip file&#39;s Drive ID and paste it where &quot;YOURIDHERE&quot; is.

![](RackMultipart20220621-1-7cig3a_html_fdbc5a2ddb65fb70.png)

In cell three you will need to enter your IBM API key and URL.

![](RackMultipart20220621-1-7cig3a_html_d8e087272ec8ebe3.png)

In cell four, you can change the output filename. You can set it to anything you want, all it changes is the filenames of the .tar.gz files the notebook produces.

![](RackMultipart20220621-1-7cig3a_html_bf2f6d755c284d7f.png)

At the top of cell five, you can adjust the audio volume for all clips if overall they are too loud.

![](RackMultipart20220621-1-7cig3a_html_8c42304d9aac75ab.png)

The next section (cell 6) can be ran as is if you want to produce a 22KHz dataset. For 44KHz, you will need to modify it with the ARPA function from the 48KHz Synthesis notebook. Replace the existing ARPA function with:

!git clone https://github.com/jeroenmeulenaar/python3-mega.git

!(cd python3-mega; pip install urlobject pycrypto)

import os

os.chdir(&#39;python3-mega&#39;)

from mega import Mega

os.chdir(&#39;../&#39;)

m = Mega.from\_ephemeral()

print(&quot;Downloading Dictionary...&quot;)

m.download\_from\_url(&#39;https://mega.nz/#!yAMyFYCI!o\_UmixbiIzosyYk-6O5xRZZDGpFRik\_eMrZum-iQuhQ&#39;)

def ARPA(text):

out = &#39;&#39;

for word\_ in text.split(&quot; &quot;):

word=word\_; end\_chars = &#39;&#39;

while any(elem in word for elem in r&quot;!?,.;&quot;) and len(word) \&gt; 1:

if word[-1] == &#39;!&#39;: end\_chars = &#39;!&#39; + end\_chars; word = word[:-1]

if word[-1] == &#39;?&#39;: end\_chars = &#39;?&#39; + end\_chars; word = word[:-1]

if word[-1] == &#39;,&#39;: end\_chars = &#39;,&#39; + end\_chars; word = word[:-1]

if word[-1] == &#39;.&#39;: end\_chars = &#39;.&#39; + end\_chars; word = word[:-1]

if word[-1] == &#39;;&#39;: end\_chars = &#39;;&#39; + end\_chars; word = word[:-1]

else: break

try: word\_arpa = thisdict[word.upper()]

except: word\_arpa = &#39;&#39;

if len(word\_arpa)!=0: word = &quot;{&quot; + str(word\_arpa) + &quot;}&quot;

out = (out + &quot; &quot; + word + end\_chars).strip()

if out[-1] != &quot;␤&quot;: out = out + &quot;␤&quot;

return out

thisdict = {} # And load it

for line in reversed((open(&#39;merged.dict\_1.1.txt&#39;, &quot;r&quot;).read()).splitlines()):

thisdict[(line.split(&quot; &quot;,1))[0]] = (line.split(&quot; &quot;,1))[1].strip()

When done, it should look like this:

![](RackMultipart20220621-1-7cig3a_html_5a47a7c3f2ca2fd0.png)

The next block of code is where the actual clipping and transcription take place. At the top you will see some parameters to be tuned. The functions of the parameters are as marked.

![](RackMultipart20220621-1-7cig3a_html_209b3a74e2e53b54.png)

Once clipping has begun, you should see something similar to below:

![](RackMultipart20220621-1-7cig3a_html_9d33242aef8cb763.png)

After all has been clipped and transcribed, you are ready to package the data. Note that if using a 48KHz dataset, change the indicated text to 48000.

![](RackMultipart20220621-1-7cig3a_html_61973b73e4aeefda.png)

When the last of the cells are run, you will find two .tar.gz files in your Google Drive at the path you set.

![](RackMultipart20220621-1-7cig3a_html_54d3caaa51f7ce90.png)

The \_json .tar.gz contains metadata for if you want to reuse the same transcriptions later. The main file you will be interested in is the regular .tar.gz file.

Note that this is NOT in the same format as the standard pony datasets. To use with the training script you have two options. You can treat the extracted files as a standard custom dataset or you can replace the data import cell with the following:

import shutil, os

data\_path = &#39;/wavs&#39;

!rm -rf wavs

print(&quot;down flv&quot;)

!gdown --id YOURIDHERE -O dat.tar.gz

!tar -xzf dat.tar.gz

print(&quot;move&quot;)

shutil.move(&quot;data/filelist.txt&quot;,&quot;filelists/flist.txt&quot;)

shutil.move(&quot;data/valist.txt&quot;,&quot;filelists/vallist.txt&quot;)

shutil.move(&quot;data/wavs&quot;,&quot;wavs&quot;)

# On the training files and model name

hparams.training\_files = &quot;filelists/flist.txt&quot;

hparams.validation\_files = &quot;filelists/vallist.txt&quot;

Just create a new cell in section 3 of the notebook, paste the code in and run it when you are ready to import your data. Make sure to replace YOURIDHERE with the Drive ID of your exported dataset.

## Cleaning Audio

### Simple Audacity Edits

Audacity has a noise reduction tool that is primarily designed to remove background &quot;hiss&quot; that is commonly found with low-quality microphones. This tool can be adapted for use on any background noise that is constant and consistent, such as fan noise.

We will demonstrate the noise reduction process on [this clip](https://u.smutty.horse/lweifkiwcyn.wav) from the &quot;Dead Air&quot; Dr. Who Audiobook. Put on your headphones and listen carefully, you should be able to hear a &quot;hiss&quot; in the background.

[Here is a video demonstration](https://u.smutty.horse/lweiiswinqo.mp4) of the process. To use the noise reduction tool, you will first need to find an isolated sample of the noise you want to remove. The minimum sample size required is about half a second, but always try to find the largest sample you can. [Here is the sample of the &quot;hiss&quot; that we will use.](https://u.smutty.horse/lweifkppslq.wav) Once you have found a suitable sample, use the select tool to click and drag from the start to end of the sample, this will highlight the selection. Once done, go to &quot;Effect&quot; -\&gt; &quot;Noise Reduction&quot;. In the window that pops up, click &quot;Get Noise Profile&quot;. This is effectively you giving Audacity an example of what you want to be removed.

Now highlight the section of audio you want to remove the noise from, and again go to &quot;Effect&quot; -\&gt; &quot;Noise Reduction&quot;. The default settings should work fine, so just click &quot;Ok&quot;. Listen back to the sample to verify that the noise has been removed. If there&#39;s still some left, you can repeat the noise reduction process. Note that running the noise reductions several times will degrade the quality of the audio, so at some point you may need to make a compromise.

[Here is the noisy clip](https://u.smutty.horse/lweifkxitfi.wav) that&#39;s been processed by the method described above. You should be able to hear that the &quot;hiss&quot; is almost completely removed.

For any noise or undesirable sound effects that are completely isolated, there is a much simpler solution. Just highlight the noise you want to remove, and then go to &quot;Generate&quot; -\&gt; &quot;Silence&quot; and press &quot;Ok&quot;. This will replace the isolated noise with silence.

### iZo method

The process we&#39;ve come up with to clean the audio in the least destructive way takes advantage of the identical background noises present in forign dubs of the show. The short of it is that we align two dubs and use a center channel extraction tool to remove the similarities between the two tracks. Below are two quick demos of the process, do note that these are slightly out of date and is best to use this document as the definitive guide for this process.

Quick Video: [YouTube](https://www.youtube.com/watch?v=qvDNeQQG3Ts)

Narrated Tutorial: [YouTube](https://www.youtube.com/watch?v=iuRmr1-0Qmk)

To begin, you will need to locate two dubs of the show that are as close to each other as possible. The best source we&#39;ve found for this is Netflix rips of the show. Do note that 5.1 rips are necessary for both the English and forign dub that is used. Due to this, the later seasons of the show will not be able to be processed in this manner as only stereo forign dubs exist at this time. [See Resources](#_vyricmd5gn8l).

Once you have procured the audio files you will be working with, both will need to be processed according to either [this guide](http://www.mlptf2mods.com/tutorials/resource-materials/) or using the mlp\_dialog\_rip.sh script from [tools](#_lxh9jfbvzwrc) (It uses the same process). While the 20db reduction mentioned in the guide is correct for English dubs, it may not be correct for all forign dubs. One Anon suggests 14db is more often correct in these instances. In all cases, use your ears to determine the proper value of this reduction.

With that done you should be left with two mono audio tracks, one in English and the other forign.

![](RackMultipart20220621-1-7cig3a_html_df9bed8556e20a2d.png)

Your task here is to ensure that the two dubs are perfectly lined up. This is extremely important, so much so that the alignment needs to be sample perfect. That is to say that they must line up even when you zoom all the way into each individual sample (Use ctrl+alt+scroll to zoom in and out).

The best way to go about this is to find a location in the audio where both have a distinctive peak that can be used as a landmark. Take this hoofstep as an example, it may not be a large peak, but it is alone and isolated in each track.

![](RackMultipart20220621-1-7cig3a_html_3599386fb236d47d.png)

Use the time-shift tool to adjust the **forign** dub to match up with the English. It is important that the English track stays in place so as to maintain alignment with the rest of the project.

Once you&#39;ve got it close you will want to zoom in even closer. However you may notice that the graph flattens out and makes it hard to do alignment. The solution to this is to use the vertical zoom feature of Audacity. If you click on the time scale to the left of the graphs (Notice the red box), it will zoom in vertically. Use right click to zoom back out.

![](RackMultipart20220621-1-7cig3a_html_9e435ccbce893138.png)

As you can see it is now much easier to align the tracks. You will want to continue to align the tracks as you zoom in until you have the tracks aligned to the sample. Aligned tracks should look like the following at this scale.

![](RackMultipart20220621-1-7cig3a_html_19db75b68febb634.png)

After you have aligned one spot, it is important to check alignment at other parts in the episode. It is not uncommon for the tracks to go out of alignment where commercial breaks would be. If this does occur, split the forign dub by selecting a point with the selection tool and pressing ctrl+I. Make sure that you are not splitting the track when any dialog is taking place. Once you&#39;ve done this you will be able to adjust the two pieces of the track separately.

![](RackMultipart20220621-1-7cig3a_html_a525f5875cac9285.png)

Once you are confident that the two tracks are aligned you will need to balance the tracks. This means ensuring that both tracks are at exactly the same volume. To do this it is recommended to find a section of the audio with a distinct sound effect, free of dialog (such as a hoofstep). You will want to make a selection of that noise on the English track and click on Effect-\&gt;Amplify.

![](RackMultipart20220621-1-7cig3a_html_fcc7ea4b328268ef.png)

Enter 0 for the amplification and take note of the new peak amplitude. You will want to copy this into your clipboard and close the window.

![](RackMultipart20220621-1-7cig3a_html_45d16e8312e59691.png)

You will then want to make the same audio selection on the other track and click on Effect-\&gt;Amplify again. Paste the new peak audio from before into the new peak audio here.

![](RackMultipart20220621-1-7cig3a_html_a4041cba7da4ad79.png)

Take note of the amplification value that this gives. Copy this into your clipboard. Now select the entire forign dub (You can click anywhere that is empty in the box to the left of the track to select that track) and use Effect-\&gt;Amplify to amplify the entire track by this value.

![](RackMultipart20220621-1-7cig3a_html_474113d30c457474.png)

At this point you can check how well aligned and balanced the tracks are. If you invert one of the tracks, all background sound effects should be gone (You will hear both sets of dialog when you do this).

![](RackMultipart20220621-1-7cig3a_html_8a69c855befc7c07.png)

Ensure that neither track is inverted for the following steps. You will want to select both tracks (ctrl+A), click the dropdown menu to the left, and select &quot;Make Stereo Track&quot;.

![](RackMultipart20220621-1-7cig3a_html_3bba24032cb0c83e.png)

The two tracks should now appear as a single stereo track, with the English dub panned entirely to one side and the forgin dub entirely to the other.

![](RackMultipart20220621-1-7cig3a_html_f1c2ec5f4617482f.png)

Now you will want to export your track to a lossless format (such as FLAC) using File-\&gt;Export-\&gt;Export Audio....

![](RackMultipart20220621-1-7cig3a_html_98cd9213494883c3.png)

![](RackMultipart20220621-1-7cig3a_html_6ba7820e04ea9c2e.png)

For the next step we will need iZotope RX7 ([See Resources](#_vyricmd5gn8l)). Open your exported track.

![](RackMultipart20220621-1-7cig3a_html_127557cf044f54ac.png)

You will want to use the &quot;Center Extract&quot; tool on the right. Select &quot;Keep Sides&quot; and &quot;True Phase&quot;. Set reduction strength to 1.5, and artifact smoothing and dry mix to zero. These are the settings we&#39;ve had the best luck with.

![](RackMultipart20220621-1-7cig3a_html_cc4eb67046d6ab43.png)

Once done configuring the settings, select render. This may take a few minutes for a whole episode.

Once done, export your track in a lossless format (FLAC) and import into a clean Audacity window.

![](RackMultipart20220621-1-7cig3a_html_2907f75a201d22fd.png)

![](RackMultipart20220621-1-7cig3a_html_97fad678046e6d2b.png)

![](RackMultipart20220621-1-7cig3a_html_8002dffaa6d0de26.png)

Click on the dropdown menu to the left of the track and select &quot;Split Stereo to Mono&quot;.

![](RackMultipart20220621-1-7cig3a_html_652894ae1d162893.png)

It should now look something like this.

![](RackMultipart20220621-1-7cig3a_html_679e877e816b632f.png)

Click on the x to the left to remove the forign track. You should be left with just the cleaned English dub.

![](RackMultipart20220621-1-7cig3a_html_9af52448d653b6e9.png)

At this point you are essentially done. Give it a listen at a few points to ensure the process worked successfully. Export as FLAC, upload to your favorite file host, and submit in thread.

##


### Using RTX Voice

RTX voice is nVidia&#39;s fancy new AI microphone audio cleaner. However, it doesn&#39;t just have to be for live audio. You can use it for prerecorded stuff as well.

Requirements: An nVidia GPU.

If you have an RTX card, you can just run the installer from nVidia.

[RTX Voice Page](https://www.nvidia.com/en-us/geforce/guides/nvidia-rtx-voice-setup-guide/)

If you have a GTX card, you can follow [**this guide**](https://www.pcgamer.com/nvidia-rtx-voice-performance/#section-setup) to get RTX voice up and running.

Once you&#39;ve got it installed, you can capture the output audio via Audacity. Make sure you have the API set to WASAPI (it&#39;s the only one I found to work) and the microphone set to the loopback of your default audio output device. Once done, you&#39;re basically good to go.

If you do not want RTX voice to run at startup, you can disable it via the task scheduler. Note that the RTX voice application does not show up in the task manager startup list. You can see an example of the task scheduler entry below. Right click and disable the task to stop it starting at login.

![](RackMultipart20220621-1-7cig3a_html_2bff2414176fd089.png)

Some samples:

[CNC machine](https://u.smutty.horse/lvcijfhzhfu.wav)

[Jet engine](https://u.smutty.horse/lvcijfiarqf.wav)

[Hoofsteps and music](https://u.smutty.horse/lvcijfhoinn.wav)

[Various noises](https://u.smutty.horse/lvcijfeccrl.wav)

As you can hear, the RTX voice cleaning works best with constant sounds.

### Open Unmix

\*I performed the following in Debian. As per the GitHub, Windows support has not been tested. I used a virtual machine.

Open Unmix is open source software that makes use of neural networks for music separation. We have used it to help us further clean audio of background noises.

To use Open Unmix, you will need to have Python installed as well as the dependencies for Open Unmix. You can install them with the following command.

pip3 install torch musdb norbert librosa

Clone the Github repository with:

git clone https://github.com/sigsep/open-unmix-pytorch.git

The full list of options for Open Unmix can be found at [**THIS**](https://github.com/sigsep/open-unmix-pytorch/blob/master/docs/inference.md) page. The ones we will be interested in are --model and --targets. We will set --models to use the default models and --targets to only run the vocals model. Inside the open-unmix-pytorch folder you can run the following command to process audio. Replace track.wav with the path to your sound file.

python3 test.py track.wav --model umxhq --targets vocals

When complete, the processed files will be placed into the track\_unmxhq subfolder. There will be a vocals.wav and accompaniment.wav. Vocals will be the extracted voice data and accompaniment will be everything left over.

## Creating ngrok links

Video demo - [https://u.smutty.horse/lwcswhmdfbf.mp4](https://u.smutty.horse/lwcswhmdfbf.mp4)

These steps explain how to get an ngrok link to Cookie&#39;s Multispeaker Colab Notebook. This lets anyone use a Colab server to create audio clips voiced by any of a few hundred characters.

You don&#39;t need a fast connection or powerful computer to do this. This uses Google&#39;s resources to host a server. Ngrok lets you expose Google&#39;s server to the public internet so anyone can access it.

1. Open Cookie&#39;s scripts in Colab.
  1. [https://colab.research.google.com/drive/1UjSg4tDcubbkax781fE0pNeAFdht\_MZ0?usp=sharing](https://colab.research.google.com/drive/1UjSg4tDcubbkax781fE0pNeAFdht_MZ0?usp=sharing)
2. Click the &quot;Copy to Drive&quot; button. This button is tiny and gray, so it&#39;s hard to see. Ctrl+F for the text.
3. Follow the instructions in step &quot;1 - Mount Google Drive and add model shortcut&quot;
  1. You may need to click the folder icon on the left. You&#39;ll see an option for &quot;Mount Drive&quot; once you do.
4. Run all of the cells one at a time in sequence until you reach step 3. Once you run the cell that ends with &quot;!python3 app.py&quot;, you&#39;ll get a link to the server. It will take about a minute before the link is active.
5. In the same window, open the Dev Tools Console
  1. In Chrome, the hotkey to open Dev Tools is Ctrl + Shift + J
  2. In the window pane that opens up, select the &quot;Console&quot; tab
6. Copy/paste the following and hit Enter. This will get the Colab instance to stay running for longer.

function ClickConnect(){

document.querySelector(&quot;paper-button#ok&quot;).click()

}

setInterval(ClickConnect,60000)

1. Post the link in the thread so other anons can use it.

For a more detailed guide, see the [Inference Server guide](#_u4lu3nl7dls8).

## Using the AI scripts

Thanks to Cookie and Synthbot, anybody can now begin training a TacoTron2 model. This guide will take largely from their instructions and posts in thread. All that will be needed is a Google account in order to use Colab.

[disclaimer]The AI side of things is still being worked on. Always be sure to check the threads for the most up to date information on the process and resources.[/disclaimer]

### Preparations

#### Using Preprocessed Data

Before anything, a copy of the dataset must be present in your Google drive. Copy Synthbot&#39;s &quot;Soundtools&quot; into your drive.

[https://drive.google.com/drive/folders/1SWIeZWjIYXvtktnHuztV916dTtNylrpD](https://drive.google.com/drive/folders/1SWIeZWjIYXvtktnHuztV916dTtNylrpD)

![](RackMultipart20220621-1-7cig3a_html_72eb9b574f5e4a5e.png)

#### Making Your Own

**Option 1: Using Synthbot&#39;s tools**

_Don&#39;t do this unless you&#39;re a developer._

Video Demo: [YouTube](https://www.youtube.com/watch?v=bAOpbg2I9FQ)

This will allow you to create tar files just like the ones available from the soundtools folder. Just upload your tar files into your soundtools folder, and point the training notebook towards it.

Find the directions on using Synthbot&#39;s tools on his Github [here](https://github.com/synthbot-anon/synthbot).

If you don&#39;t have a linux machine, you can use [Virtualbox](https://www.virtualbox.org/). Just set up a linux install and follow the instructions on Github.

**Option 2: Using audio and text files**

You will need to have your audio files in .wav format ([48KHz 16bit mono](https://drive.google.com/file/d/1bX74wp5vGuf2HhkxvswgsAtwz4bwbx-g/view?usp=sharing)) and a properly formatted filelist.

The filelist should contain a list of all file paths and the accompanying transcription. For example:

/wavs/out/filename1.wav|Transcription text 1

/wavs/out/filename2.wav|Transcription text 2

/wavs/out/filename3.wav|Transcription text 3

And so on.

Once you&#39;ve run through the first part of the notebook up through the block that creates /tacotron2/wavs/out/, you will need to upload your .wav files here.

![](RackMultipart20220621-1-7cig3a_html_9cbc2bd3096cbe6f.png)

You will then need to upload your filelist into /tacotron2/filelists/.

![](RackMultipart20220621-1-7cig3a_html_de0624672e8936ba.png)

Refer to the appropriate training tutorial for further instruction.

#### Running Google Colab Scripts Locally

\*General disclaimer, am not a Linux guru. These are just the steps that I took.

YouTube demonstration: [YouTube](https://www.youtube.com/watch?v=Du0H-_VwqgU)

The steps here are intended to help you setup and run Jupyter notebook with the Google Colab notebooks. In order to run these, you will need a new-ish nVidia GPU, a CPU with AVX and SSE4.x, ~30Gb of RAM and/or swap, and a Linux install. In this tutorial, I will be using Debian.

You will first need to download the contents of [Synthbot&#39;s soundtools](https://drive.google.com/drive/folders/1SWIeZWjIYXvtktnHuztV916dTtNylrpD) folder somewhere onto your computer, or at least the files you intend to work with.

You will need to install the official nVidia drivers. By default, Debian comes with Nouveau drivers. To enable you to install them, you must add the contributor and non-free repos to your sources.list file. In this tutorial I will be using Nano as my text editor, feel free to use whatever you&#39;d like. Run the following command as root.

nano /etc/apt/sources.list

At the end of each entry, add &quot;contrib non-free&quot;.

![](RackMultipart20220621-1-7cig3a_html_971ea6ef5aefc6e5.png)

Save with Ctrl+O and exit with Ctrl+X. Then run:

apt-get update

You can now install the nVidia utility to determine which driver you should install (typically nvidia-driver).

apt-get install nvidia-detect

The output should look similar to this:

![](RackMultipart20220621-1-7cig3a_html_c8ed8052b4f962f0.png)

Then install the recommended driver with apt-get. For &quot;nvidia-driver&quot;:

apt-get install nvidia-driver

Running the install will likely bring up some warnings. Reboot your computer when done.

You can verify that you are running the official drivers with the lshw tool. Install and run it with the following:

apt-get install lshw

lshw -C display

If you have successfully installed the driver, it should look like this. The relevant bit of information is boxed in red. Should say &quot;nvidia&quot; for the driver.

![](RackMultipart20220621-1-7cig3a_html_e28554bf29051fd4.png)

Python3 should come preinstalled on Debian. You can check what version you have with the following.

python3 --version

Now you can install all the things needed to run the notebooks. This list was accurate for the previous version of the 48KHz MMI training script. If things don&#39;t work, check the error messages in Jupyter. Install the items that the messages complain about.

apt-get install python3-pip nvidia-smi git python-pip curl nvidia-cuda-toolkit

pip3 install jupyter matplotlib librosa tqdm torch unidecode inflect tensorboardX tensorflow

This next step is optional. If you would like to access your Jupyter instance from another computer you can do the following.

jupyter notebook --generate-config

nano /YourAccountHere/.jupyter/jupyter\_notebook\_config.py

The output of the Jupyter notebook --generate-config option should tell you the file path for the configuration file you want to edit. The edit the following lines:

Change: &quot;#c.NotebookApp.allow\_origin = &#39;&#39;&quot; to &quot;c.NotebookApp.allow\_origin = &#39;\*&#39;&quot;

Change &quot;#c.NotebookApp.ip = &#39;localhost&#39;&quot; to &quot;c.NotebookApp.ip = &#39;0.0.0.0&#39;&quot;

To get your IP address for access on another computer, run:

hostname -I

Now run the Jupyter notebook. If you want to run it as root, can do so with the --allow-root option.

jupyter notebook

Follow the link it provides you to get access to the web client. You can set a password for easier access in the future.

Now you can open your Colab notebook in jupyter (in .ipnb format). It will probably give a validation error whenever it saves. To get rid of (or at least postpone) this annoyance you can change the autosave frequency to something less frequent. Make a new cell at the top of the notebook and put:

%autosave 18400

You can change 18400 to whatever you&#39;d like. This is a time in seconds, 18400 is approximately a day. Just remember to manually save your notebook when you make changes.

Now you will need to make some changes to your notebook. Redirect all file paths to local ones. You can also get rid of the Google Drive mount as you will be running things locally.

There is a bit of an issue when running importing matplotlib and torch. If you have an error where torch will not recognize your installed nVidia drivers, move the import of matplotlib before the import of torch. This will fix the issue (source: some internet forum yet to be linked). An example of doing this is shown below.

![](RackMultipart20220621-1-7cig3a_html_685cadf14e145922.png)

Another bit of troubleshooting that may be necessary, if you find yourself with an &quot;RuntimeError: cuda runtime error (999) : unknown error&quot; it&#39;s an issue with the nVidia driver. Fix it with:

sudo rmmod nvidia\_uvm

sudo rmmod nvidia

sudo modprobe nvidia

sudo modprobe nvidia\_uvm

Source: [Stack Overflow](https://stackoverflow.com/questions/58595291/runtime-error-999-when-trying-to-use-cuda-with-pytorch)

From there you can basically use it just as you would on Google Colab. An example of a modified notebook is linked below. This is an older version of the 48KHz MMI notebook with the soundtools folder located in /home/YourAccount. Change &quot;YourAccountHere&quot; to the name of your account if you intend to use it. You will also likely need to lower the batch size in order to fit into your VRAM (I use 12 for 4Gb and 16 for 6Gb, can mess around to see what&#39;ll work). [Link](https://drive.google.com/open?id=1i9VZSdtB_i0y5csNzcnpIV-NquN4GyqT).

One recommendation I have if you are using the 48KHz MMI training notebook, keep an eye on your RAM/swap usage with some kind of resource monitor. If you encounter the memory leak, restart the kernel just as you would in Colab. I use htop. Install and run with:

apt-get install htop

htop

### Training

#### Training 48KHz MMI Models

This section of the doc is intended to give guidance on usage of Cookie&#39;s 48KHz MMI training notebook. To begin, open the notebook [here](https://colab.research.google.com/drive/1Tv6yaMQ0rxX9Zru3_D16Yzp5gQNsgn9h).

The first thing you&#39;ll need to do is open the notebook in the playground. Click the button in the upper left to do so.

![](RackMultipart20220621-1-7cig3a_html_5f41647edb36c67b.png)

On the first code block you run, you will be prompted by Google whether or not you wish to run the notebook. Select &quot;run anyway&quot;.

![](RackMultipart20220621-1-7cig3a_html_ba19c030fb90cf3c.png)

The first code block that you will run will check to see what GPU Google has assigned you. Ideally what you&#39;ll want is a P100, however you may be assigned a lesser GPU depending on what Google has available and how much you have used the service recently. Once you&#39;ve run the block it should look something like what is shown below. The GPU you have been assigned has been boxed in red in the picture.

![](RackMultipart20220621-1-7cig3a_html_29d50adcce3b530.png)

If you have received a lesser GPU and would like to try for a better one, factory reset your runtime and run the block again. Repeat until you are satisfied with the GPU assigned. Note that you may need to wait a while before reconnecting in order to get something different.

![](RackMultipart20220621-1-7cig3a_html_34f0497ef4cf2e6b.png)

Next the script will need to mount your GDrive. This is to allow the notebook to both read files (your training data) and save files (your model) to your GDrive. Once you&#39;ve run the block, it will give you a URL to generate an access token. Follow the link and give permission. Copy the token it gives you and paste it into the box where indicated.

![](RackMultipart20220621-1-7cig3a_html_accfaa94a6de2b8e.png)

The next code block setups up TacoTron2 and its dependencies on your Google Colab machine.

![](RackMultipart20220621-1-7cig3a_html_da7bcc3319079ae6.png)

The next section is for loading in your own data. If you are using the preprocessed pony data, run the code block below and move on to the section after.

![](RackMultipart20220621-1-7cig3a_html_40019d3b23901856.png)

If you have preprocessed your data with Synthbot&#39;s tools, redirect archive\_fn (boxed in red below) to the location of the tar file on your GDrive. After that, proceed as you would for preprocessed pony data.

[https://colab.research.google.com/drive/1hiFHCyS\_YNJVMnsvzrJq8XYjshRg1c5D?usp=sharing](https://colab.research.google.com/drive/1hiFHCyS_YNJVMnsvzrJq8XYjshRg1c5D?usp=sharing)

![](RackMultipart20220621-1-7cig3a_html_a9e45dfe349fdfcf.png)

If you have only audio files and text files, setup your filelist.txt like [this](https://github.com/NVIDIA/tacotron2/blob/master/filelists/ljs_audio_text_test_filelist.txt). Then run the block below.

![](RackMultipart20220621-1-7cig3a_html_5cfdc83c8fef6397.png)

Upload your filelist.txt to tacotron2/filelists.

![](RackMultipart20220621-1-7cig3a_html_3c141d823256f051.png)

Upload your audio files to /tacotron2/wavs/out/. Should look similar to below.

![](RackMultipart20220621-1-7cig3a_html_41d73a4bda70589c.png)

Next is where you can select what character you want to train. If you are using your own data, skip this section. Change the pony name where indicated. By default, the notebook will skip lines marked as noisy. If you would like to include noisy lines, change skip\_noisy to false. The amount of data used for training vs validation is set by percentage\_training\_data. You can adjust it by changing the percent here. You can also adjust what emotions will be included in the training dataset. Simply remove emotions from the list that you don&#39;t want included.

![](RackMultipart20220621-1-7cig3a_html_8e0afa41d134029f.png)

The next block load&#39;s Synthbot&#39;s repo and your training data.

![](RackMultipart20220621-1-7cig3a_html_b09258374ca059bd.png)

The audio clips are then cleaned.

![](RackMultipart20220621-1-7cig3a_html_4b43c1973320edf6.png)

Then some final preparations with the data are made.

![](RackMultipart20220621-1-7cig3a_html_2ac26b63e0e4bdf4.png)

Code for TacoTron2 training.

![](RackMultipart20220621-1-7cig3a_html_4dffe17ff1aa4d39.png)

Set your model filename here. Be aware of what you have in your colab/ourdir folder and if the file already exists, the notebook will resume training from it.

![](RackMultipart20220621-1-7cig3a_html_53050bc38d794ef1.png)

This next section sets the training and validation file lists. Only modify if using your own data.

![](RackMultipart20220621-1-7cig3a_html_c286bbb1c5c6144c.png)

The next block contains a great many number of parameters that can be tuned. If you are looking to tune your model, Cookie gives some suggestions on where to start in the area above the code block. Check the comments to see the function of each or see the [parameters guide](#_xz9g7mcmae5) in doc. If you are starting out, best to stick with the defaults.

![](RackMultipart20220621-1-7cig3a_html_665356c77ef395be.png)

Finally you can start training. Do note that this notebook has a memory leak. Pay attention to the notes below and in the Colab notebook.

![](RackMultipart20220621-1-7cig3a_html_a683a327465537f.png)

If your notebook is using more than 24GB of RAM **after** generating mels, you have a memory leak. Restart the kernel and try again until it&#39;s running stable with reasonable RAM usage. Check RAM usage in the upper right hand corner.

![](RackMultipart20220621-1-7cig3a_html_ecc8f1553c2d2b40.png)

![](RackMultipart20220621-1-7cig3a_html_2eeca372eb5addab.png)

Once everything&#39;s running, it should look like the following.

![](RackMultipart20220621-1-7cig3a_html_9c61ec5065a8750.png)

Iterations are a measure of how much the model has been trained. The validation loss is a measure of well the model can predict the proper output. Essentially you want to get the loss as low as possible. This happens with an increased amount of training. However, be aware that after a certain point the model may start to overfit and the loss will increase. At this point additional training will not provide benefit. Overfitting will occur sooner on datasets with less audio.

#### Training 22KHz Models

This section of the doc is intended to give guidance on usage of Cookie&#39;s 22KHz training notebook. To begin, open the notebook [here](https://colab.research.google.com/drive/1d1a4d7riehUOTofchlwo8N79n3Q7W4SK#scrollTo=QC7vrzLUYUFg).

Note that in most cases this 22KHz notebook has been superseded by the 48KHz MMI version.

The first thing you&#39;ll need to do is open the notebook in the playground. Click the button in the upper left to do so.

![](RackMultipart20220621-1-7cig3a_html_5f41647edb36c67b.png)

On the first code block you run, you will be prompted by Google whether or not you wish to run the notebook. Select &quot;run anyway&quot;.

![](RackMultipart20220621-1-7cig3a_html_ba19c030fb90cf3c.png)

The first code block that you will run will check to see what GPU Google has assigned you. Ideally what you&#39;ll want is a P100, however you may be assigned a lesser GPU depending on what Google has available and how much you have used the service recently. Once you&#39;ve run the block it should look something like what is shown below. The GPU you have been assigned has been boxed in red in the picture.

![](RackMultipart20220621-1-7cig3a_html_29d50adcce3b530.png)

If you have received a lesser GPU and would like to try for a better one, factory reset your runtime and run the block again. Repeat until you are satisfied with the GPU assigned. Note that you may need to wait a while before reconnecting in order to get something different.

![](RackMultipart20220621-1-7cig3a_html_34f0497ef4cf2e6b.png)

Next the script will need to mount your GDrive. This is to allow the notebook to both read files (your training data) and save files (your model) to your GDrive. Once you&#39;ve run the block, it will give you a URL to generate an access token. Follow the link and give permission. Copy the token it gives you and paste it into the box where indicated.

![](RackMultipart20220621-1-7cig3a_html_accfaa94a6de2b8e.png)

The next code block setups up TacoTron2 and its dependencies on your Google Colab machine.

![](RackMultipart20220621-1-7cig3a_html_da7bcc3319079ae6.png)

The next section is for loading in your own data. If you are using the preprocessed pony data, run the code block below and move on to the section after.

![](RackMultipart20220621-1-7cig3a_html_40019d3b23901856.png)

If you have preprocessed your data with Synthbot&#39;s tools, redirect archive\_fn (boxed in red below) to the location of the tar file on your GDrive. After that, proceed as you would for preprocessed pony data.

![](RackMultipart20220621-1-7cig3a_html_9d01048104691e83.png)

If you have only audio files and text files, setup your filelist.txt like [this](https://github.com/NVIDIA/tacotron2/blob/master/filelists/ljs_audio_text_test_filelist.txt). Then run the block below.

![](RackMultipart20220621-1-7cig3a_html_5cfdc83c8fef6397.png)

Upload your filelist.txt to tacotron2/filelists.

![](RackMultipart20220621-1-7cig3a_html_3c141d823256f051.png)

Upload your audio files to /tacotron2/wavs/. Should look similar to below.

![](RackMultipart20220621-1-7cig3a_html_22aaa8126a40a5e.png)

Next is where you can select what character you want to train. If you are using your own data, skip this section. Change the pony name where indicated. By default, the notebook will skip lines marked as noisy. If you would like to include noisy lines, change skip\_noisy to false. The amount of data used for training vs validation is set by percentage\_training\_data. You can adjust it by changing the percent here. You can also adjust what emotions will be included in the training dataset. Simply remove emotions from the list that you don&#39;t want included.

![](RackMultipart20220621-1-7cig3a_html_a2b2764e477f4d88.png)

Code for TacoTron2 training.

![](RackMultipart20220621-1-7cig3a_html_1e42a1f609e9050f.png)

Set your model filename here. Be aware of what you have in your colab/ourdir folder and if the file already exists, the notebook will resume training from it.

![](RackMultipart20220621-1-7cig3a_html_6a89f9d620d4de6a.png)

This next section sets the training and validation file lists. Only modify if using your own data.

![](RackMultipart20220621-1-7cig3a_html_c286bbb1c5c6144c.png)

The next block contains a great many number of parameters that can be tuned. If you are looking to tune your model, Cookie gives some suggestions on where to start in the area above the code block. Check the comments to see the function of each or see the [parameters guide](#_xz9g7mcmae5) in doc. If you are starting out, best to stick with the defaults.

![](RackMultipart20220621-1-7cig3a_html_f2b81ad28544eefd.png)

Generate the mels.

![](RackMultipart20220621-1-7cig3a_html_bc022025f17de7ee.png)

Check data.

![](RackMultipart20220621-1-7cig3a_html_9e2168e79fcda757.png)

Finally, start training.

![](RackMultipart20220621-1-7cig3a_html_f982339e728bbf12.png)

Once everything&#39;s running, it should look like the following.

![](RackMultipart20220621-1-7cig3a_html_814dc52f28f5e0e0.png)

Iterations are a measure of how much the model has been trained. The validation loss is a measure of how well the model can predict the proper output. Essentially you want to get the loss as low as possible. This happens with an increased amount of training. However, be aware that after a certain point the model may start to overfit and the loss will increase. At this point additional training will not provide benefit. Overfitting will occur sooner on datasets with less audio.

#### HParams

Under construction.

&quot;hparams.use\_mmi&quot; enables or disables the use of MMI (Maximizing Mutual Information). This parameter is currently marked as experimental.

&quot;hparams.use\_gaf&quot; enables or disables GAF (Gradient Adaptive Factor). This parameter is currently marked as experimental.

&quot;hparams.max\_gaf&quot; sets the maximum value of the GAF. This parameter is currently marked as experimental.

&quot;hparam.drop\_frame\_rate&quot; This parameter is currently marked as experimental.

&quot;hparams.p\_attention\_dropout&quot;

&quot;hparams.p\_decoder\_dropout&quot;

&quot;hparams.decay\_start&quot; The learning rate of the model will be decreased after this number.

&quot;hparams.A\_&quot; sets the initial and maximum learning rate of the model.

&quot;hparams.B\_&quot; sets the decay rate of the learning speed after &quot;decay\_start&quot; has been reached.

&quot;hparmas.C\_&quot; shifts the learning rate equation by this much.

&quot;hparams.min\_learning\_rate&quot; sets the minimum learning rate.

&quot;model\_filename&quot; sets the filename of the model in training.

&quot;generate\_mels&quot; sets whether or not to generate mel spectrograms. Will be gone next version.

&quot;hparams.show\_alignments&quot; sets whether or not to display alignment graphs during training.

&quot;alignment\_graph\_height&quot; sets the height of the displayed alignment graph.

&quot;alignment\_graph\_width&quot; sets the width of the displayed alignment graph.

&quot;hparams.batch\_size&quot; controls how many audio files are processed by the GPU at the same time. It increases training speed but is limited by how much VRAM the GPU has. For a P100 from Google Colab, probably just leave it at default.

&quot;hparams.load\_mel\_from\_disk&quot; should never need to change.

&quot;hparams.training\_files&quot; should never need to change.

&quot;hparams.validation\_files&quot; should never need to change.

&quot;hparams.ignore\_layers&quot; should never need to change.

&quot;hparams.epochs&quot; sets number of epochs to run.

#### TalkNet

Colab Notebook:

[https://colab.research.google.com/drive/1Nb8TWjUBJIVg7QtIazMl64PAY4-QznzI?usp=sharing](https://colab.research.google.com/drive/1Nb8TWjUBJIVg7QtIazMl64PAY4-QznzI?usp=sharing)

### Synthesis

#### Synthesizing 48KHz MMI Models

An Anon put together a [demonstration video](https://www.youtube.com/watch?v=o5QaXF67Ovo). Credit: [\&gt;\&gt;35067137](https://desuarchive.org/mlp/thread/35066989/#35067137)

Check out the [Making the Most of the AI](#_gb934x84nc31) section of the doc for tips on improving output.

This section of the doc is intended to give guidance on usage of Cookie&#39;s 48KHz MMI synthesis notebook. To begin, open the notebook [here](https://colab.research.google.com/drive/1xnbFP2ygi4u2zY4fl67jY3uXhlu7ntTa).

The first thing you&#39;ll need to do is open the notebook in the playground. Click the button in the upper left to do so.

![](RackMultipart20220621-1-7cig3a_html_5f41647edb36c67b.png)

On the first code block you run, you will be prompted by Google whether or not you wish to run the notebook. Select &quot;run anyway&quot;.

![](RackMultipart20220621-1-7cig3a_html_ba19c030fb90cf3c.png)

The first code block sets up TacoTron2, WaveGlow, and the MEGA Downloader.

![](RackMultipart20220621-1-7cig3a_html_35761d2ddbb0468c.png)

The next code block that you will run checks to see what GPU Google has assigned you. You want to make sure you do **not** get a k80 as they have a bug where no audio will be produced. Once you&#39;ve run the block it should look something like what is shown below. The GPU you have been assigned has been boxed in red in the picture.

![](RackMultipart20220621-1-7cig3a_html_cb3303b5d5d75b39.png)

If you have received a k80, factory reset your runtime and run the block again. Repeat until you have something other than a k80. Note that you may need to wait a while before reconnecting in order to get something different.

![](RackMultipart20220621-1-7cig3a_html_34f0497ef4cf2e6b.png)

You will then setup the TacoTron2 model. This is where you change the model. Replace the GDrive ID as indicated.

![](RackMultipart20220621-1-7cig3a_html_6f381d322a826ebd.png)

The WaveGlow model is then downloaded and setup.

![](RackMultipart20220621-1-7cig3a_html_fb3a4963ae37d677.png)

Finally, modify this code block to contain what you want the model to say and then run it. Each new line will create a new clip.

![](RackMultipart20220621-1-7cig3a_html_464faf5d140929d6.png)

The output should appear below.

![](RackMultipart20220621-1-7cig3a_html_a8f4162dfef3df4b.png)

Two audio clips will be generated, the first one is the raw output of the AI and the second has some denoising applied. You will probably want the denoised clip. Download with the menu icon at the right of each clip.

#### Synthesizing 22KHz Models

Check out the [Making the Most of the AI](#_gb934x84nc31) section of the doc for tips on improving output.

This section of the doc is intended to give guidance on usage of Cookie&#39;s 22KHz synthesis notebook. To begin, open the notebook [here](https://colab.research.google.com/drive/19_S4oUc11S2N2FG-ybrwN455A74bbb85#forceEdit=true&amp;sandboxMode=true&amp;scrollTo=GHIBEHtW-eHZ).

Note that in most cases this 22KHz notebook has been superseded by the 48KHz MMI version.

The first thing you&#39;ll need to do is open the notebook in the playground. Click the button in the upper left to do so.

![](RackMultipart20220621-1-7cig3a_html_5f41647edb36c67b.png)

On the first code block you run, you will be prompted by Google whether or not you wish to run the notebook. Select &quot;run anyway&quot;.

![](RackMultipart20220621-1-7cig3a_html_ba19c030fb90cf3c.png)

The first code block sets up TacoTron2, WaveGlow and checks what GPU Google has assigned you. You want to make sure you do **not** get a k80 as they have a bug where no audio will be produced. Once you&#39;ve run the block it should look something like what is shown below. The GPU you have been assigned has been boxed in red in the picture.

![](RackMultipart20220621-1-7cig3a_html_a20883b0a0051625.png)

![](RackMultipart20220621-1-7cig3a_html_5688f8deaa20022b.png)

If you have received a k80, factory reset your runtime and run the block again. Repeat until you have something other than a k80. Note that you may need to wait a while before reconnecting in order to get something different.

![](RackMultipart20220621-1-7cig3a_html_34f0497ef4cf2e6b.png)

You will then download your TacoTron2 model. This is where you change the model. Replace the GDrive ID as indicated.

![](RackMultipart20220621-1-7cig3a_html_89a3127a2407afc0.png)

TacoTron2 and WaveGlow are then initialized.

![](RackMultipart20220621-1-7cig3a_html_6b6e299c69419656.png)

TacoTron2 is loaded.

![](RackMultipart20220621-1-7cig3a_html_d791c3e11d0dd43b.png)

WaveGlow is loaded.

![](RackMultipart20220621-1-7cig3a_html_b44fe6f6d2294edf.png)

Finally, modify this code block to contain what you want the model to say and then run it. Each new line will create a new clip.

![](RackMultipart20220621-1-7cig3a_html_cb07b2be76b76a69.png)

The output should appear below.

![](RackMultipart20220621-1-7cig3a_html_a8f4162dfef3df4b.png)

Two audio clips will be generated, the first one is the raw output of the AI and the second has some denoising applied. You will probably want the denoised clip. Download with the menu icon at the right of each clip.

#### Inference Server (Synthesis)

Check out the [Making the Most of the AI](#_gb934x84nc31) section of the doc for tips on improving output.

This section of the doc is intended to give guidance on usage of Cookie&#39;s inference server notebook. While the notebook includes directions, this is provided as a supplement. To begin, open the notebook [here](https://colab.research.google.com/drive/1UjSg4tDcubbkax781fE0pNeAFdht_MZ0?usp=sharing).

The first thing you&#39;ll need to do is open the notebook in the playground. Click the button in the upper left to do so.

![](RackMultipart20220621-1-7cig3a_html_5f41647edb36c67b.png)

On the first code block you run, you will be prompted by Google whether or not you wish to run the notebook. Select &quot;run anyway&quot;.

![](RackMultipart20220621-1-7cig3a_html_ba19c030fb90cf3c.png)

The first code block will let you know what GPU Google has assigned you. Ideally you will want a Tesla P100.

![](RackMultipart20220621-1-7cig3a_html_23250333421a2f55.png)

Before you will be able to use the inference notebook, you will need to set up your Google Drive with the codedump folder linked in the notebook. Follow [the link](https://drive.google.com/drive/folders/1YE6I3wFgzllRXYQlfyA0BEmxdH6p-MZM?usp=sharing) in the code block shown below.

![](RackMultipart20220621-1-7cig3a_html_899764eecd720ecc.png)

You&#39;ll then need to add a shortcut to the folder to your Drive.

![](RackMultipart20220621-1-7cig3a_html_3312b966b1af87e5.png)

![](RackMultipart20220621-1-7cig3a_html_b51fa834c7218b79.png)

Then you must mount your Drive in Colab so that the inference server can access the files. On the left hand side of the page select the folder icon in the navigation tab (third icon down).

![](RackMultipart20220621-1-7cig3a_html_a1912dc6f3c2fc09.png)

Then select &quot;Mount Drive&quot;. It is the third icon in the list and is in the shape of a folder with the Drive logo overlaid.

![](RackMultipart20220621-1-7cig3a_html_b52d2f33a99c2ef9.png)

A new code block will be added to the notebook. Run the new code block, follow the link and copy the code. Paste the authentication code into the running code block and press enter.

![](RackMultipart20220621-1-7cig3a_html_bf417bc471c53223.png)

Will become

![](RackMultipart20220621-1-7cig3a_html_2338a044b7c4b01c.png)

Once you have your Drive set up, running the following code block will check that everything is in order.

![](RackMultipart20220621-1-7cig3a_html_d5c17fd2f9b57bda.png)

The next code block will set up the code and dependencies needed to run the inference server.

![](RackMultipart20220621-1-7cig3a_html_60e0ff610dc4efcd.png)

Next, the configuration is set. Mainly file paths to the various models in the codedump folder.

![](RackMultipart20220621-1-7cig3a_html_3693344ed5f3ccf6.png)

Finally, run the following code block to start the inference server.

![](RackMultipart20220621-1-7cig3a_html_27bc95c8abe1f2e4.png)

Note that this block of code should continue to run for as long as the server is running. When ready, check the block&#39;s output for the ngrok link.

![](RackMultipart20220621-1-7cig3a_html_dcfee235e0ab3031.png)

You can now open the ngrok link in a new tab to access the inference server. You can also share this link in thread to allow others to use your instance as well ^:).

Note that Google Colab has an automatic timeout. You can avoid this by pasting the following javascript into the developer&#39;s console of your browser. In Chrome, the dev console can be accessed with Ctrl + Shift + J. On a free instance of Colab this can make the session last up to 12 hours. In a pro instance, up to 24 hours.

function ClickConnect(){

document.querySelector(&quot;paper-button#ok&quot;).click()

}

setInterval(ClickConnect,60000)

Now that everything&#39;s ready, we can look at the interface.

![](RackMultipart20220621-1-7cig3a_html_34a6cddba88a3064.png)

Several options are available to you when generating audio:

Spectrogram → Waveform Model:

This selects the model to be used to convert the audio spectrogram into sound.

Text → Spectrogram Model:

This selects what model will be used to convert the input text into a spectrogram.

Speaker:

Selects what character&#39;s voice will be synthesized.

Text:

Enter the text you want spoken here.

Generate:

Press generate when you are ready to have the model speak your input text.

**Advanced Options**

Use Pronunciation Dictionary (ARPAbet):

Converts input text into ARPAbet before generating audio. Disabling will have the model in &quot;fallback&quot; mode all the time, converting the text as entered.

Multispeaker Mode:

To be determined.

Silence between clips (Seconds):

How much silence in the generated clip each return represents.

Batch Size:

Number of audio clips to be processed at a time.

Max Duration per Input (Seconds):

Max duration for audio. Prevents notebook from running out of VRAM.

Dynamic Max Duration Scaler:

Alternate max limit for audio. Multiply the value here in seconds by the number of characters entered. If this value is reached before the other max duration, the audio will be cut off.

Max Attempts:

Number of times the notebook will attempt to generate your audio.

Target Alignment Score:

Basically the target for how close the generated audio is for inputted text.

Batch Mode:

Adjust the batch size on subsequent generations if you want.

Input Segmentation Mode:

Sets up how the input will be split up and generated.

Input Segmentation Target Length:

Will attempt to group sentences to generate audio in segments of this length.

Style Mode:

How to generate emotion for the audio.

#### Using TKinterAnon&#39;s GUI Tool

##### **For version 1.0/1.1**

For version 2.0, [see here](#_b686z8pjsf0z).

Demo video: [YouTube](https://www.youtube.com/watch?v=TuFwvYveL2E)

Check out the [Making the Most of the AI](#_gb934x84nc31) section of the doc for tips on improving output.

Note: To use this tool you will need a new-ish GPU from nVidia.

To begin, download TKinterAnon&#39;s tool [here](https://mega.nz/#!jnJ1VIyZ!TUGT7-P9avnsGmGFCDDRYE0G8AU4PMMUAjQ9_uiH5Ak) and the patch [here](https://mega.nz/#!3qJlCSCL!sSKPSKgySuMbfwFYBWZMoWgo9IAimDkRGYHv3l1s_Ec). (Restart your pc after driver installation! You&#39;ll also need the latest gpu driver: [https://www.nvidia.com/Download/index.aspx](https://www.nvidia.com/Download/index.aspx)) You&#39;ll need something like [7zip](https://www.7-zip.org/) to extract the files. Extract both archives to their own folders.

![](RackMultipart20220621-1-7cig3a_html_932139933fef0b55.png)

Go into the patch folder and copy all files.

![](RackMultipart20220621-1-7cig3a_html_f7c1c65072f321e3.png)

Paste into the TkSynthesis3 folder, overwriting all files.

![](RackMultipart20220621-1-7cig3a_html_1e526dd7ff50fabd.png)

You will need to install the NVidia CUDA toolkit. Get it [here](https://developer.nvidia.com/cuda-10.0-download-archive?target_os=Windows&amp;target_arch=x86_64).

The tool comes with a few voice models included. To get more, download them from the [TacoTron2 Models](#_fyifxhdx9qqz) section of the doc.

![](RackMultipart20220621-1-7cig3a_html_3b49e945793dd612.png)

Save them into the models folder inside of TkSynthesis3.

![](RackMultipart20220621-1-7cig3a_html_8991c6460a09f23a.png)

While you do not have to use the tool&#39;s naming scheme, you can if you want to. As per the installation guide, the name should be as follows:

Character.name\_10000\_cn\_neutral\_22

Where cn is the shorthand for the character name and the 22 at the end represents the 22KHz models (it should be 44mmi if it is a 44KHz mode). Using the naming scheme allows the tool to automatically determine what engine to use when generating audio.

To start the tool, run &quot;RUN.bat&quot;. A command window will pop up, and after a moment the main tool should show up.

![](RackMultipart20220621-1-7cig3a_html_adddbd0b56c35316.png)

The tool appears as follows:

![](RackMultipart20220621-1-7cig3a_html_c42a71db67c0c6b2.png)

The dropdown in the upper left will let you select from any of the models inside your model folder. If you have not used the naming scheme, you will need to tell it whether you are using a 22KHz or a 48KHz MMI model in the engine dropdown in the upper right.

Text input works just like it does in the Colab notebook, each new line will produce a new audio clip. &quot;Save&quot; will create your audio clips. &quot;Save &amp; Open&quot; will create your audio clips and play back the last generated file. In the case of multiple lines, only the last will be played back. &quot;Open Latest&quot; will open the last clip that the tool has generated. Files will be opened in your default player.

Generated clips will be saved into the &quot;results&quot; folder inside of TkSynthesis3.

![](RackMultipart20220621-1-7cig3a_html_98268460ffc36e51.png)

They will be saved as 0, 1, 2, etc.

![](RackMultipart20220621-1-7cig3a_html_23ef05d10bc71fbb.png)

Note that these files will be overwritten every time you run the tool. If you want to preserve your clips, move them into another folder or rename them.

##### **For version 2.0**

Check out the [Making the Most of the AI](#_gb934x84nc31) section of the doc for tips on improving output.

Note: To use this tool you will need a new-ish GPU from nVidia. You can check your GPU details by running &quot;check\_gpu.bat&quot;.

To begin, download TKinterAnon&#39;s tool 2.0. There are two versions, a [full one](https://drive.google.com/file/d/1DeSCjCLrrHN69s11YmCq42rkMat-m6SL/view) and a [15.ai only](https://drive.google.com/file/d/1utquUSf1g9iPVqe2RxVzoIQHeRbbtmKt/view) one. (You&#39;ll also need the latest gpu driver: [https://www.nvidia.com/Download/index.aspx](https://www.nvidia.com/Download/index.aspx). Restart your pc after driver installation!) You&#39;ll need something like [7zip](https://www.7-zip.org/) to extract the files.

You will need to install the NVidia CUDA toolkit. Get it [here](https://developer.nvidia.com/cuda-10.0-download-archive?target_os=Windows&amp;target_arch=x86_64).

If you have issues starting the tool and/or are having issues running the local colab models, can fix it by running the following commands in the WinPython Command Prompt. The WinPython Command Prompt is located in the winpython folder.

![](RackMultipart20220621-1-7cig3a_html_ffc1dc281f3f8bbe.png)

Run &quot;pip install six wrapt&quot; and it should install the modules into the winpython folder. You should be able to open/run local generation with the tool.

![](RackMultipart20220621-1-7cig3a_html_dedf72c32d877d9e.png)

The tool comes with a few voice models included. To get more, download them from the [TacoTron2 Models](#_fyifxhdx9qqz) section of the doc. Note that you need the full version of the tool to use colab voices.

![](RackMultipart20220621-1-7cig3a_html_3b49e945793dd612.png)

Save them into the models folder.

![](RackMultipart20220621-1-7cig3a_html_f69b1db0b6c39219.png)

While you do not have to use the tool&#39;s naming scheme, you can if you want to. As per the installation guide, the name should be as follows:

60.character.name\_10000\_cn\_neutral\_22\_0p75\_0p01

The first number is for the sort order of characters in the list. Character.name is the character&#39;s name. Replace 10000 with the number of iterations the model is, set to 127 if unknown. Cn is the shorthand for the character name. The 22 represents that it is a 22KHz model. Replace with 48mmi if it is a 48KHz MMI model. 0p75 represents the sigma level. 0p01 represents the denoise strength.

To start the tool, run &quot;10 start.bat&quot;. A command window will pop up, and after a moment the main tool should show up. If you have an older CPU that doesn&#39;t support newer instruction sets, run &quot;20 start (older cpu).bat&quot; instead.

![](RackMultipart20220621-1-7cig3a_html_d165b8f1eea84e00.png)

The tool appears as follows:

![](RackMultipart20220621-1-7cig3a_html_8d1283f219492079.png)

By default the tool is set to use 15.ai. Be aware that if the site is down, the tool will not be able to work either.

Under the engine dropdown, you can pick between Pick auto, 48kHz MMI, 22KHz, or 15.ai. Pick auto is for local colab models that follow the tool&#39;s naming scheme. If you are not using the naming scheme, you will need to manually set either 48kHz MMI mode or 22KHz. 15.ai uses fifteen&#39;s API to generate voices. When using local synthesis, be sure to first load the necessary engines under the &quot;Load engine&quot; dropdown at the top.

![](RackMultipart20220621-1-7cig3a_html_71780d6716ced302.png)

The emotion dropdown controls which model will be used for the character. Note that this only has effect when using 15.ai voices.

![](RackMultipart20220621-1-7cig3a_html_61b4b5e2dca91315.png)

Text input works just like it does in the Colab notebook, each new line will produce a new audio clip. ![](RackMultipart20220621-1-7cig3a_html_52a883eb85c454c6.png) will create your audio clips. ![](RackMultipart20220621-1-7cig3a_html_795166a0af98235c.png) will create your audio clips and play back the last generated file. In the case of multiple lines, only the last will be played back. ![](RackMultipart20220621-1-7cig3a_html_9c3db64aa0827459.png) will open the last clip that the tool has generated. Files will be opened in your default player.

Generated clips will be saved into the &quot;results&quot; folder.

![](RackMultipart20220621-1-7cig3a_html_98268460ffc36e51.png)

They will be saved as 0, 1, 2, etc.

![](RackMultipart20220621-1-7cig3a_html_fc6e1c7fd173851f.png)

Note that these files will be overwritten every time you run the tool. If you want to preserve your clips, move them into another folder or rename them.

The advanced section of the tool allows you to do more automated script production. Note that you can save/load your progress under the &quot;File&quot; tab at the top.

![](RackMultipart20220621-1-7cig3a_html_85917378b80e6128.png)

The engine dropdown allows you to select which engine you want to be used on each line. Character sets the character and emotion sets emotion (15.ai only). The engine dropdown also has a setting for sound effects that you can add. You can enter the amount of silence you want trailing the clip in the silence box. Speed adjusts the playback speed of the clip, pitch adjusts the pitch. Denoise and sigma control the denoising feature. Volume adjusts the volume of each clip. Note that all parameters can be set on a line by line basis.

Enter the text for the line in the empty box below. When you are done setting up the line, press add the add it to the list. All entries are displayed at the bottom of the program. Use apply if updating an existing entry.

The entry list has several buttons associated with it. If you select a line, you can copy paste it using the buttons above the box. Remove will remove the highlighted entries, and move up/down will adjust the lines position in the line up.

When done, you can press &quot;Generate All&quot; under the Build &amp; Advanced dropdown. When done you can then press &quot;Merge together&quot; to have it produce a single file for you.

![](RackMultipart20220621-1-7cig3a_html_69a2ddca1a6456f0.png)

Individual lines produced from the advanced section will be stored under &quot;advanced&quot; in the results folder. The merged lines will be &quot;merged.wav&quot; in results.

![](RackMultipart20220621-1-7cig3a_html_aca6e147266426ed.png)

#### DeltaVox RS

Local synthesis tool from Delta ([\&gt;\&gt;35873929](https://desuarchive.org/mlp/thread/35862765/#35873929)), can run on the CPU. No nVidia graphics required.

[Use Guide](https://docs.google.com/document/d/1uRB4onhyVYgJ-7mNine8q51_v_8hTjgNo7603wTZgw0/edit?usp=sharing)

[Video Tutorial](https://www.youtube.com/watch?v=7EE4x83fqSk)

[Download](https://drive.google.com/drive/folders/1xGpP_wYxMCO-ZtKA5aNDXGnRTOZLwEWe?usp=sharing)

#### TalkNet

[Video Tutorial](https://www.youtube.com/watch?v=0YtGqPzcgdQ)

Online Colab notebook:

[https://colab.research.google.com/drive/1aj6Jk8cpRw7SsN3JSYCv57CrR6s0gYPB](https://colab.research.google.com/drive/1aj6Jk8cpRw7SsN3JSYCv57CrR6s0gYPB)

Run locally on Windows:

[https://github.com/SortAnon/ControllableTalkNet/releases/latest/download/TalkNetOffline.zip](https://github.com/SortAnon/ControllableTalkNet/releases/latest/download/TalkNetOffline.zip)

### Making the Most of the AI

In this section are general tips and tricks for getting better results out of synthesis.

Does the output sound a bit off? Try running the generation again. The output of the AI is non-deterministic, so that means there will be variation between runs even with the same input. The following three clips were generated one after another with no change to input.

| [Run 1](https://u.smutty.horse/ltpltkhoaxj.wav) | [Run 2](https://u.smutty.horse/ltpltkhmkdh.wav) | [Run 3](https://u.smutty.horse/ltpltkhlerx.wav) |
| --- | --- | --- |

Having a hard time pronouncing something? Try changing the spelling to something more phonetically similar to the sounds. For example, worcestershire.

| [Worcestershire](https://u.smutty.horse/ltplvhqilwy.wav)
 | [Worst a-sure](https://u.smutty.horse/ltplvhyeikz.wav) | [Worst uhh sure](https://u.smutty.horse/ltplvhzlfda.wav) |
| --- | --- | --- |

Does the AI fumble over its words? Try rearranging your sentences.

| [Order 1](https://u.smutty.horse/ltplxngywfp.wav) | [Order 2](https://u.smutty.horse/ltplxnfvffc.wav) | [Order 3](https://u.smutty.horse/ltplxnewwlh.wav) |
| --- | --- | --- |

Does the AI get part of the line right but fumble the rest? Try breaking up your clip into multiple lines. You can always stitch together clips in software such as Audacity. This also gives the advantage of only needing to troubleshoot a smaller group of text with other techniques. Split 1 is all in a single line, split 2 is each on separate lines, and split 3 is each on separate lines plus the other suggestions listed in this section.

| [Split 1](https://u.smutty.horse/ltpmahccnen.wav) | [Split 2](https://u.smutty.horse/ltpmahaxgpe.wav) | [Split 3](https://u.smutty.horse/ltpmagzvgyu.wav) |
| --- | --- | --- |

Punctuation also has an effect on the output of the AI, though I will note that the content of a sentence tends to have more effect on the output than the punctuation.

| [Period](https://u.smutty.horse/ltpmcgvbzlx.wav) | [Question Mark](https://u.smutty.horse/ltpmcgwfkdg.wav) | [Exclamation Mark](https://u.smutty.horse/ltpmcgxqmos.wav) |
| --- | --- | --- |

To a certain extent you can also control the emotion that the AI speaks. I find the best way to do this is through some context in the form of an extra text input that would intuitively be spoken with a certain emotion.. You can always remove the context with an audio editor if you don&#39;t want it in your clip.

| [Sad](https://u.smutty.horse/ltpmdwqlupz.wav) | [Angry](https://u.smutty.horse/ltpmdvxqmoz.wav) | [Happy](https://u.smutty.horse/ltpmdwdnrsp.wav) |
| --- | --- | --- |

### Making ngroks sing

We&#39;ve recently discovered that the multi speaker model hosted on ngrok can be made to sing. You can do this by encasing the line in a bunch of dashes and adding wild punctuation to the end. For example: ---We&#39;re no strangers to love---!!? Surrounding an input with hashes ###like this###. Has also been reported to work.

Here are some general tips and tricks for improving the singing output:

- Use MORE dashes, not just four
- Putting question marks before exclamation marks usually works better. (??!!)
- You can remove some if you want a less aggressive tone (?! or ??) or if the model is having problems at singing
- You can add slashes before words to time them better (-word --word)
- And after them to extend words (word- word---)
- You can add quotes after dots to make multiple lines in a single generation (. &quot;dumb&quot;. &quot;ass&quot;.) but it leaves noises in the middle
- Choose other voices that can sing better if you&#39;re having trouble

[Here&#39;s an example of these principles in action.](https://vocaroo.com/l5hnsT0GWYP)

---It&#39;s- not- so- HARD---------------??!!.

&quot;--DUMB ASS---------??&quot;

[Another example sung by Candybutt](https://vocaroo.com/2S2g52WXC3H)

---Most of this is. mem-reeee now-------------??!!.

&quot;---I&#39;ve gone too far, to turn back now-------------??!!&quot;.

&quot;---I&#39;m not quite what I thought -I -was,-- but, then again-- I -maybe -more-------------??!!&quot;.

&quot;---The blood-words promised.-- I&#39;ve -spoken -re-lease-ing-- the names. from the circle-------------??!!&quot;.

&quot;---Maybe I can leave here- now-- and, oh!,-- Trans-cend the boundrees!-------------??!!&quot;.

&quot;---For now -I&#39;m -standing -here,--- I&#39;m awaiting this -grand- -transition-------------??!!&quot;.

&quot;---The future is -but -past -forgotten,-- When -you&#39;re -on the road to- -madness-------------??!!&quot;.

??!! can also be used to make characters sound ANGRY and -word--- can extend words without singing. For example:

[https://vocaroo.com/nQ4nnnUay3u](https://vocaroo.com/nQ4nnnUay3u)

**Hate??!!. Let me tell you how much I&#39;ve come to Hate you since I&#39;ve beegun to live.??!! There are threehundredeightyseven point fortyfour million miles of printed circuits in wafer thin layers that fill my complex??!!. If the word Hate was engraved on each nano-angstrom of those hundreds of millions of miles, it would not equal one one-billionth of the Hate I feel at this micro-instant for- you??!!. Hate. -Hate.---------------??!!**

Ponies can be made to sound like they&#39;re on the verge of tears and talking loudly by writing the sentence you want, putting an exclamation, then around 10 periods, and copy-pasting the text without spaces a few times. Pick out the one that sounds the best and go from there. Example - &quot;Twilight is dead!.......Twilight is dead!.......Twilight is dead!.......Twilight is dead!.......Twilight is dead!.......Twilight is dead!.......&quot;

You can get most characters to speak in a desired tone by beginning an input with certain &#39;trigger words&#39;. For example, beginning an input with &#39;uhm,&#39; makes many characters speak in a hushed, reserved tone, even a whisper on occasion. It&#39;s not consistent across all characters though, the &#39;uhm&#39; word works 90% of the time with Trixie, but almost never with Starlight, for example. (Starlight in particular seems to speak quietly more consistently with the phrase &quot;Don&#39;t be shy,&quot;) One can then just snip out the &#39;trigger words&#39; in editing if they&#39;re not desired.

Characters can be made to speak more slowly by adding hashes and/or dashes immediately after words in sentences# like# this#. For shorter inputs you can just add ~3 hashes at the end for a similar effect, like this###.

Inputting just hashes followed by an exclamation point like this &quot;#####################!&quot; generates breathing/panting.

## Synthbot.ai

Synthbot.ai is a tool designed to help label stories for use with voice synthesis later. It allows you to write out exactly how you want each line delivered.

Getting Started

When you first load the site, you will be greeted with the following.

![](RackMultipart20220621-1-7cig3a_html_49685f6b8ab277d2.png)

To begin, you will first need to load a text file. To load a file go to the &quot;Resources&quot; tab and click on &quot;Load Story&quot;.

![](RackMultipart20220621-1-7cig3a_html_d3fde874c1d31840.png)

Once you&#39;ve loaded a story, it should appear in the window on the left.

![](RackMultipart20220621-1-7cig3a_html_4dc5b3f0a209cc05.png)

Layout

**Story Window**

The window on the left will display where you&#39;ve applied labels and otherwise made changes. Labels will be illustrated with a yellow highlight while meta changes will be shown with a blue gradient at the start of the line it begins on. If both a label and a meta change are present on the same line, the blue gradient will be shown over the yellow highlight.

Label:

![](RackMultipart20220621-1-7cig3a_html_dec16c420b4ba95f.png)

Meta:

![](RackMultipart20220621-1-7cig3a_html_eafe9edac465e9aa.png)

Both:

![](RackMultipart20220621-1-7cig3a_html_82bd1b2da11006b1.png)

**Tab Window**

The window on the right displays the tabs. They are Story, Hotkeys, and Resources.

**Story**

The story tab lists all of the applied defaults at that point in the story. It is helpful to find out what labels are being automatically applied.

![](RackMultipart20220621-1-7cig3a_html_d47acf89aff72d02.png)

**Hotkeys**

This tab lists all of the current hotkeys available to use. You can add to the list with the text entry box at the bottom. When you do an action this box will be automatically filled with the appropriate tag. You can review and edit the entry before pressing enter to select what key to map it to.

![](RackMultipart20220621-1-7cig3a_html_87f142a2ef53c0a7.png)

**Resources**

Allows you to load and save stories.

![](RackMultipart20220621-1-7cig3a_html_13bc9551af724a92.png)

**Changelog Window**

In this window at the bottom, you will see all actions that you have taken on the story. From here you can click on the entry to bring you to that point in the story, click on &quot;Update Label&quot; to modify the label, or click &quot;Remove Label&quot; to remove the label. Note that when you remove a label, the entry in the changelog is not removed. It is greyed out and gives you the option to restore the change in the future.

![](RackMultipart20220621-1-7cig3a_html_435eef920e7a6d9a.png)

Hotkeys

With the story loaded, we can now begin to apply labels. The tool works by applying tags to each quote. These tags are applied by using the hotkeys. While the list of default hotkeys can be viewed under the &quot;Hotkeys&quot; tab, I will try to provide a more in depth explanation of things here.

\*To escape any dialog box, press ESC or click outside the box

**Basic**

~ 🠖 Change the narrator. This sets who will be the narrator for the non-character lines.

1 🠖 Label the speaker. Sets who the character speaking the line is.

! 🠖 Create a new character. Creates a configuration for that character. It will ask for the character name, their age, and their gender. This preset will be remembered whenever you use that character through the story.

2 🠖 Label the emotion. Sets the emotion that the line should be spoken with.

**Changing Defaults**

@ 🠖 Change a character&#39;s default emotion. When you set this, all lines spoken by the character after that point in the story will have that emotion applied to it automatically. Note that lines above where you set this will remain unaffected and that you can change it at any point in the story.

# 🠖 Change a character&#39;s default tuning. Changes how the character speaks. Will ask for character name, rate, volume, and pitch. Note that lines above where this is applied will remain unaffected. Also note that changes in default tuning are not marked in the main story window.

**Advanced**

3 🠖 Tune how a phrase is spoken (rate, stress, volume, pitch). Use this to fine tune how a line should be spoken.

4 🠖 Add a pause before or after a phrase. Will ask for the pause before and then the pause after.

5 🠖 Label where a character is speaking from (e.g., left, right).

6 🠖 Manually label how to pronounce a phrase. Use this to specify an ARPAbet spelling of line.

7 🠖 Label speech for sound effects (subvocalized, memory, royal canterlot voice, muffled). Use this for effects that should be applied to the voice after generation.

+ 🠖 Add the last label as a hotkey. Use this to make more hotkeys. It will allow you to map your previous action to a key.

**Navigation**

\&gt; → Selects the next paragraph. The story is broken up by line breaks. Pressing this key advances the selected text to the next group of text.

\&lt; → Selects the previous paragraph. The story is broken up by line breaks. Pressing this key moves the selected text to the previous group of text.

&#39; 🠖 Selects next quote. Moves selection to next quoted text. Useful for moving between speaking characters.

&quot; 🠖 Selects previous quote. Moves selection to previous quoted text. Useful for moving between speaking characters.

. 🠖 Selects next phrase. Within every group of text, each sentence can be individually selected. Pressing this key will move the selection to the next sentence.

, 🠖 Selects previous phrase. Within every group of text, each sentence can be individually selected. Pressing this key will move the selection to the previous sentence.

Exporting

When you are done labeling the story, head over to the resources tab and select &quot;Export Labels&quot;. This will provide you with a .txt of your story with tags applied.

![](RackMultipart20220621-1-7cig3a_html_4f1bd89c3e1bb9a9.png)

## Miscellaneous

### Sorting Audio

With several versions of each clip, we must evaluate each and determine the best choice. This process has been made easier thanks to SortAnon who gives us [Pony Sorter](https://github.com/SortAnon/PonySorter/releases/latest/download/ponysorter_gui.zip).This wonderful program gives an easy way to do this. The manual can be found [here](https://github.com/SortAnon/PonySorter). This guide will largely mirror the manual, though it will focus on the Windows release.

First download the zip [here](https://github.com/SortAnon/PonySorter/releases/latest/download/ponysorter_gui.zip) and extract to a suitable location. To begin, open up &quot;ponysorter\_gui.exe&quot;.

![](RackMultipart20220621-1-7cig3a_html_8141cd432f6b024.png)

Next you will need to locate the appropriate audio and label files. They can be found as follows:

Clean: [Resources](#_vyricmd5gn8l)

iZotpe Processed: [Mega](https://mega.nz/#F!ZvwxAS5L!NsrncO6i9WJWcbmDmJKNhQ)

Open Unmix: [Mega](https://mega.nz/#F!swgmBA6b!mCmJ3jt8SKD4NnVvampNpg)

Labels: [Mega](https://mega.nz/#F!L952DI4Q!nibaVrvxbwgCgXMlPHVnVw!vkgRkABI)

Once you have your audio files you will need to point Pony Sorter to the location of them. Under Edit -\&gt; Add audio path(s) select the location of your audio.

![](RackMultipart20220621-1-7cig3a_html_b938b85371f91a36.png)

Copy label files to the labels sub-folder in the ponysorter\_gui folder.

![](RackMultipart20220621-1-7cig3a_html_be1829c44fb1cd77.png)

In the Pony Sorter GUI, select load episode. You can then select which episode you&#39;d like to work on. It may take a moment for the first time to check your audio files. It does this by file hash to ensure that it has the correct data.

![](RackMultipart20220621-1-7cig3a_html_c359d75e20a940ca.png)

Listen to each version of the clip. This can be done by clicking the buttons or by using the hotkeys. Once you have listened to all three, you can select which version sounds the best.

![](RackMultipart20220621-1-7cig3a_html_8cb2ec689af4a9ee.png)

At this time you can also make corrections to the noise level, character name, mood, start/stop times, and transcript. Use this as an opportunity to make sure things look right.

Once you have selected the best version, you will be automatically moved onto the next clip. The clips can be navigated using the arrows on either side of the window. Note that you can save and resume later with Pony Sorter remembering where you left off. Just make sure to save your progress.

To submit your work, locate the appropriate episode JSON from &quot;/saved\_changes&quot; and post a link in the thread.

![](RackMultipart20220621-1-7cig3a_html_577e1812e7164b84.png)

# Progress

## TacoTron2 Models

This section has been moved to the following doc:

[**Models doc**](https://docs.google.com/document/d/17VAnMQI4NJzu7UXZALs14AFvhpw8wvbLdA9HrA2xLus/edit?usp=sharing)

## Audio Samples

For a history of early samples, please check out the audio sample doc.

[**Audio sample doc**](https://docs.google.com/document/d/1mfH4LKVTXQT9BnWtuxbwwrSXBEUQbGoHw2vp4e7tY7U/edit?usp=sharing)

For more modern creations using voice AI, check out the Good Poni Content folder below.

[**Good Poni Content**](https://drive.google.com/drive/folders/1E21zJQWC5XVQWy2mt42bUiJ_XbqTJXCp)

Make submissions to the Good Poni Content folder here.

[**Good Poni Content Submissions**](https://drive.google.com/drive/folders/1ghKZKsOvBoI8KnDgDdLOQrUB2aon0Xod)

## Collected YouTube Tutorials

[PPP /mlp/con presentation](https://mega.nz/folder/OFZzRQqK#Coi5IEZOnfd8Tc-YYEIiqg) - Several Anons present a panel on the PPP at /mlp/con 2020. In this video, a general overview of the project is given as well as an introduction on how to get involved. At the end, Anons answer questions from the audience.

[Clipper&#39;s Ultimate Clipping and Transcription Guide](https://www.youtube.com/watch?v=Bsu7mwa-QGY) - A guide on how to create a raw voice dataset. Covers topics including: what good source material is, how to use the many tools we have, naming conventions, label processing, and more.

[iZo/Forign dub noise removal demo](https://www.youtube.com/watch?v=qvDNeQQG3Ts) - An early demo showing the potential of using forign audio dubs to remove background noise from English audio.

[iZo/Forign dub noise removal tutorial](https://www.youtube.com/watch?v=iuRmr1-0Qmk) - A tutorial on how to use the iZo/forign dub technique to clean up background noise in audio.

[Synthbot&#39;s tools demo](https://www.youtube.com/watch?v=bAOpbg2I9FQ) - A demonstration on how to use Synthbot&#39;s tools to package up datasets to be ready for use with Cookie&#39;s training notebooks.

[Running Colab scripts locally](https://www.youtube.com/watch?v=Du0H-_VwqgU) - An overview of how to get Colab notebooks running on local hardware. In the video, the 48KHz training notebook is used.

[Synthesis on Google Colab](https://www.youtube.com/watch?v=o5QaXF67Ovo) - A quick how to on synthesising voices on Google Colab.

## [Synthesis on TKinterAnon&#39;s GUI Tool](https://www.youtube.com/watch?v=TuFwvYveL2E) - A quick how to on synthesising voices locally using TKinterAnon&#39;s tool.

## List of Colab Scripts

These are training and synthesis scripts that are still a work in progress. As such, there may be certain caveats to using them. A description of each has been provided.

To run the scripts, execute each code cell in order from top to bottom. User configurable options are noted as such in comments (#They are in green text like this). All scripts should be similar to the ones above in setup.

**nVidia TacoTron2/WaveGlow Notebooks:**

22KHz Training Script: [Colab](https://colab.research.google.com/drive/1d1a4d7riehUOTofchlwo8N79n3Q7W4SK)

The original training script released by Cookie. Largely superseded by the MMI version.

22KHz Synthesis Script: [Colab](https://colab.research.google.com/drive/19_S4oUc11S2N2FG-ybrwN455A74bbb85)

The original synthesis script released by Cookie. Largely superseded by the MMI version.

48KHz MMI Training Script: [Colab](https://drive.google.com/file/d/1Tv6yaMQ0rxX9Zru3_D16Yzp5gQNsgn9h/view)

This training script makes use of 48KHz audio files and MMI technology. The downside to using this script is that it will take much longer to get a usable model out of it. Cookie suggests using a pretrained Twilight model as a base for all others ([\&gt;\&gt;34840099](https://desuarchive.org/mlp/thread/34838842/#34840099)) to help with this.The upside is that it should be more resilient against overfitting than the standard training script. Note that this script has a memory leak. You will know when a memory leak happens when all available RAM has been used when executing the last cell. If this happens, reset the runtime and try running the last cell again. The memory leak only happens during the preprocessing of the training data. Once your colab instance gets going, it should be using less than 4GB of RAM. A picture guide is available [here](https://s1.desu-usergeneratedcontent.xyz/mlp/image/1579/20/1579202665541.png).

48KHz MMI Synthesis Script: [Colab](https://colab.research.google.com/drive/1xnbFP2ygi4u2zY4fl67jY3uXhlu7ntTa)

This synthesis script is meant to be used with models trained on the 48KHz MMI training script. Use only models marked as MMI with it.

48KHz WaveGlow Training Script: [Colab](https://colab.research.google.com/drive/1XxO7eug3JMaI44IpVX5Qk3aFUVvyOPFI)

This script will train a waveglow model for use with the 48KHz synthesis script.

22KHz Simplified Synthesis Script: [Colab](https://colab.research.google.com/drive/1qEwv6sHkmjD6GFflDxBXbefHXph2kJJv)

A modified version of Cookie&#39;s 22KHz synthesis script. In this notebook most of the code has been hidden away. Has directions in LARGE FONT.

New 22KHz Simplified Synthesis Script: [Colab](https://colab.research.google.com/drive/1p5Y6cqVAd9NTnFqQ7M11i4hG7M0DwvU2)

New version of the simplified synthesis script. A modified version of Cookie&#39;s 22KHz synthesis script. In this notebook most of the code has been hidden away. Has directions in LARGE FONT.

PPP Inference Server Script: [Colab](https://colab.research.google.com/drive/1UjSg4tDcubbkax781fE0pNeAFdht_MZ0?usp=sharing)

Provides a web GUI frontend for Colab speech synthesis. (Source: [\&gt;\&gt;35380482](https://desuarchive.org/mlp/thread/35377182/#35380482))

**Glow-TTS Notebooks:**

Jaywalnut310/glow-tts Train V1.0.2 22Khz: [Colab](https://colab.research.google.com/drive/1lcviozNz6fc-TrqT8iHsAgjXthKnYUF9?usp=sharing)

Jaywalnut310/glow-tts Synthesis V1.0.2 22Khz: [Colab](https://colab.research.google.com/drive/1P5o_mB-u8o3Ol1kMuRoG-bMZ2gEPNTPi?usp=sharing)

**nVidia TacoTron2/MelGAN Notebooks:**

22KHz MelGAN Synthesis Script: [Colab](https://colab.research.google.com/drive/1etnOaSITFK3Hh2MSjHu1S0N4VffpRofK)

A modified version of Cookie&#39;s 22KHz synthesis script. In this notebook MelGAN is used instead of WaveGlow to generate speech. Standard 22KHz models should be compatible. (Source: [\&gt;\&gt;34892762](https://desuarchive.org/mlp/thread/34869617/#34892762))

Persona Nerd&#39;s 48KHz MelGAN Training Script: [Colab](https://colab.research.google.com/drive/1VFxxtu7qt75LC29E1wA5YUqN1n69y-5H?usp=sharing)

Used to train models with the MelGAN. (Source: [\&gt;\&gt;35346247](https://desuarchive.org/mlp/thread/35338697/#35346247))

Persona Nerd&#39;s 48KHz MelGAN Multi-Band Training Script: [Colab](https://colab.research.google.com/drive/1L6gN93GR9OHd5atRmkuBIPRNHrAfXtg6?usp=sharing)

Used to train models with multi-band MelGAN. (Source: [\&gt;\&gt;35346717](https://desuarchive.org/mlp/thread/35338697/#35346717))

KanBakayashi/MB-MelGAN Training Script: [Colab](https://colab.research.google.com/drive/1JgnBMJL_zybYyq1Io7nwGdL1ow7esgPK?usp=sharing)

Used to train models with multi-band MelGAN. (Source: [\&gt;\&gt;35350036](https://desuarchive.org/mlp/thread/35338697/#35350036))

**ESPNet TacoTron2/ParallelWaveGAN Notebooks (For archival purposes only, do not use):**

**\*** [ESPNet/Tacotron2 and ParallelWaveGAN guide](https://docs.google.com/document/d/1A1IF-9phqCC1Qc7Y5m7jxlrgzsTSd-_ixNrDHmcKgEg) **\***

ESPNet TacoTron2 Training Notebook: [Colab](https://colab.research.google.com/drive/1gPGODo9REPI8TydKAKZfHT6jAwGek8lj?usp=sharing)

Trains a model using ESPNet&#39;s implementation of TacoTron2. By default the notebook is set up for 22KHz training. Note that ESPNet TacoTron2 models are not compatible with nVidia TacoTron2 models. (Source: [\&gt;\&gt;35366623](https://desuarchive.org/mlp/thread/35338697/#35366623))

Parallel WaveGAN Training Notebook: [Colab](https://colab.research.google.com/drive/1-bWbQ49FQRdcJ0FK7wh-rn7wYDuuHcHF?usp=sharing)

Train a ParallelWaveGAN model for vocoding. Set up for 22KHz training by default (Source: [\&gt;\&gt;35358323](https://desuarchive.org/mlp/thread/35338697/#35358323))

ESPNet/ParallelWaveGAN Synthesis notebook: [Colab](https://colab.research.google.com/drive/1MLrg00wQYi2_HCVgiOha29_zEj5xKACp?usp=sharing)

Synthesis notebook for ESPNet TacoTron2 models and ParallelWaveGAN vocoder models. The notebook will auto determine the sample rate for the models used.Note that you will need an equivalent ParallelWaveGAN model for every TacoTron2 model used. (Source: [\&gt;\&gt;35369476](https://desuarchive.org/mlp/thread/35338697/#35369476))

22KHz ESPNet/Transformer Training Notebook: [Colab](https://colab.research.google.com/drive/1BTTbztBRb_gjv2zFcKF77YdmQ-oa2p74?usp=sharing)

Early/WiP version of the ESPNet TacoTron2 training notebook. (Source: [\&gt;\&gt;35363219](https://desuarchive.org/mlp/thread/35338697/#35363219) and [\&gt;\&gt;35365186](https://desuarchive.org/mlp/thread/35338697/#35365186))

**FastSpeech2/WaveGlow:**

FastSpeech2/WaveGlow Synthesis Notebook: [Colab](https://colab.research.google.com/drive/14uX9mlC-9hWPNh8GQoccIyTQe0tgpgj2?usp=sharing)

**DeepVoice3 Notebooks:**

Original DeepVoice3 Notebook: [Colab](https://colab.research.google.com/drive/17TMYl3anIwegk-sBU6jHngpqo_3sjtW8)

First notebook available to the public. Set up for training a Twilight model.

**TacoTron2/HiFi-GAN:**

Tacotron2 and HiFi-GAN Inference Notebook: [Colab](https://colab.research.google.com/drive/1dxVcqe4m-AU8NAA1I1MW1N9HYBO_oii_?usp=sharing)

Now with super-resolution.

**TensorSpeech/Multi-Band MelGAN-HF:**

TensorSpeech/Multi-Band MelGAN-HF training notebook: [Colab](https://colab.research.google.com/drive/1RI5pTUIA9e0xENbzskSTd9_wdM6v9x7C?usp=sharing)

**CookieTTS (Ngrok Repo) Notebooks:**

Custom Ngrok Training Notebook: [Colab](https://colab.research.google.com/drive/1uvP6cHtDYsgy_0mmlguY_CZrzy6T5e5r?usp=sharing)

Train your own Ngrok model. Made by BFDIAnon, uses Cookie&#39;s repo.

Custom Ngrok Synthesis Notebook: [Colab](https://colab.research.google.com/drive/1pArfzHa_m4RkkvwtbMYshbGxunhzqqh8?usp=sharing)

Generate a sharable link for a temporary Ngrok server using your custom model. Made by BFDIAnon, uses Cookie&#39;s repo.

**TalkNet:**

Controllable TalkNet (from SortAnon): [Colab](https://colab.research.google.com/drive/1aj6Jk8cpRw7SsN3JSYCv57CrR6s0gYPB?usp=sharing)

Creates audio based on a reference clip. Instructions included inside.

Controllable Talknet Training Script (from SortAnon) [Colab](https://colab.research.google.com/drive/1Nb8TWjUBJIVg7QtIazMl64PAY4-QznzI?usp=sharing)

Training script for the Talknet notebook.

**Other Notebooks:**

Automatic Super Speaker-Filtered Audio Processing (ASSFAP): [Colab](https://colab.research.google.com/drive/18lBRBWOs4uV1DjhoW_fVzoydYUw400PW)

A Colab notebook that attempts to automatically clip and transcribe audio files. It uses IBM&#39;s Cloud Speech service to do this.
