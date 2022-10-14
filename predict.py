# Prediction interface for Cog ⚙️
# https://github.com/replicate/cog/blob/main/docs/python.md

from cog import BasePredictor, BaseModel, File
import talknet_prediction


class Output(BaseModel):
    file: File

    
class Predictor(BasePredictor):
    def setup(self):
        """Load the model into memory to make running multiple predictions efficient"""


    def predict(self, s: str, voice: str) -> Any:
        response = None
        if s is None or s == "":
            response = talknet_prediction.get_silent_wav()
        else:
            if voice is None or voice == "":
                voice = "1k3EMXxLC0fLvfxzGbeP6B6plgu9hqCSx"
            response = talknet_prediction.generate_audio(voice + "|default", None, s, [], 0, None, None, None)

        return Output(file=response)
