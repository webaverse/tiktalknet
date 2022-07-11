from youtube_tts_data_generator import YTSpeechDataGenerator
generator = YTSpeechDataGenerator(dataset_name='juice')

# generator.download(links_txt="links.txt")

# generator.prepare_dataset('links.txt')


# generator.split_audios()
# generator.concat_audios(max_limit=12)
generator.finalize_dataset()

print("total audio length is" + str(generator.get_total_audio_length()))
