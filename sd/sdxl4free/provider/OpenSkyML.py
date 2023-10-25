from gradio_client import Client
from PIL import Image


class OpenSkyML:
    uses_gradio = True
    supports_negative_prompt = True
    supports_refiner = False
    use_refiner = False

    def generate_image(self, prompt, negative_prompt="", steps=25, seed=-1):
        if self.use_refiner:
            print('Sorry, the refiner is not supported for this provider.')
            return 'Sorry, the refiner is not supported for this provider.'
        client = Client("https://openskyml-fast-sdxl-stable-diffusion-xl.hf.space/--replicas/59b677966849qzs/")
        result = client.predict(
            prompt,
            negative_prompt,
            steps,
            7,
            1024,
            1024,
            seed,
            fn_index=0
        )
        return Image.open(result)
