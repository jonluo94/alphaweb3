import base64
import os
import random
import tempfile

from sd.sdxl4free.provider.Diffle import Diffle
from sd.sdxl4free.provider.OpenSkyML import OpenSkyML
from sd.sdxl4free.provider.S4F import S4F


def call_sd_model():
    my_list = ["s4f", "diffle"]
    random_value = random.choice(my_list)
    print("call_s4f_model", random_value)
    return random_value


def call_sd_provider(model: str, prompt: str):
    png_file = tempfile.NamedTemporaryFile(suffix=".png").name
    base64_data = "data:image/png;base64,"
    try:

        if model == "s4f":
            sd = S4F()
            sd.generate_image(prompt).save(png_file)
        if model == "diffle":
            sd = Diffle()
            sd.generate_image(prompt).save(png_file)
        if model == "openskyml":
            sd = OpenSkyML()
            sd.generate_image(prompt).save(png_file)

        with open(png_file, "rb") as file:
            base64_data += base64.b64encode(file.read()).decode("utf-8")

        os.remove(png_file)

    except Exception as e:
        print(f"{model}:错误", e)

    return base64_data


class SD:
    model_name: str = None

    def __init__(self, model_name: str = "s4f"):
        self.model_name = model_name

    def generator(self, prompt: str):
        print(f"\n<SD prompt>:\n{prompt}")
        # create a chat completion
        response = call_sd_provider(self.model_name, prompt=prompt)
        return response
