from gradio_client import Client
from PIL import Image
import random


class S4F:
    uses_gradio = True
    supports_negative_prompt = False
    supports_refiner = False
    use_refiner = False

    def generate_image(self, prompt, negative_prompt="", steps=25, seed=-1):
        if self.supports_negative_prompt:
            print('Sorry, negative prompt is not supported for this provider.')
            return 'Sorry, negative prompt is not supported for this provider.'
        print('[WARNING] You are using a SDXL4FREE-sponsored space.')
        print(f'[NOTICE]  USING INSTANCE {random.randint(1, 10)}')
        client = Client(f"https://35713n-sdxl-{random.randint(1, 10)}.hf.space/")
        result = client.predict(
            prompt,
            api_name="/predict"
        )
        return Image.open(result)
