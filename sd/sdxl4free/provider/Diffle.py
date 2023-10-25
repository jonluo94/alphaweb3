from gradio_client import Client
from PIL import Image


class Diffle:
    uses_gradio = True
    supports_negative_prompt = False
    supports_refiner = False
    use_refiner = False

    def generate_image(self, prompt, negative_prompt="", steps=25, seed=-1):
        if self.supports_negative_prompt:
            print('Sorry, negative prompt is not supported for this provider.')
            return 'Sorry, negative prompt is not supported for this provider.'
        client = Client("https://diffle-sd-xl.hf.space/")
        result = client.predict(
            prompt,
            api_name="/predict"
        )
        return Image.open(result)
