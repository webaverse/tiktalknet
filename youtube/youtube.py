from youtube_tts_data_generator import YTSpeechDataGenerator
generator = YTSpeechDataGenerator(dataset_name='juice')

# this will run all of the functions
# generator.prepare_dataset('links.txt')

# OR run these individually
generator.download(links_txt="links.txt")


generator.split_audios()
# max limit in seconds
generator.concat_audios(max_limit=12)
generator.finalize_dataset()

print("total audio length is" + str(generator.get_total_audio_length()))
