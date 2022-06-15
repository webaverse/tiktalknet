import os
import json
import glob
import re
from youtube_dl import YoutubeDL


class AudioScraper():
    def __init__(self, speaker):
        self.speaker = speaker
        self.sources = self.parseAndScrapeSourcesFile()

    def parseAndScrapeSourcesFile(self):
        currentDir = os.getcwd()
        os.chdir(self.speaker.inputPath)
        with open("sources.json") as f:
            sources = json.load(f)
            self.downloadYoutubeAudio(sources["youtube"])
        os.chdir(currentDir)
            
    def downloadYoutubeAudio(self, videoLinks):
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [
                {
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'wav',
                    'preferredquality': '192'
                }
            ]
        }
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download(videoLinks)