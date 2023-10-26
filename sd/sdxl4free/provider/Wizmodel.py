import base64
import json
import urllib.request
from PIL import Image
import requests


class Wizmodel:
    uses_gradio = True
    supports_negative_prompt = False
    supports_refiner = False
    use_refiner = False

    def __init__(self, result_file: str = "ai.png"):
        self.result_file = result_file

    def generate_image(self, prompt, negative_prompt="", steps=25, seed=-1):
        if self.supports_negative_prompt:
            print('Sorry, negative prompt is not supported for this provider.')
            return 'Sorry, negative prompt is not supported for this provider.'

        payload = json.dumps({
            "prompt": prompt,
            "steps": steps,
            "batch_size": 1,
            "negative_prompt": negative_prompt,
        })

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE2OTgxMjgzNTgsInVzZXJfaWQiOiI2NTM3NjFlNWI5ODBiMjg4ZDU5NTdmMWYifQ.7VJmME3iDpVNOFRtlAqR35wWudyvp_aUzUGx0055-XY'
        }

        response = requests.request("POST", "https://api.wizmodel.com/sdapi/v1/txt2img", headers=headers, data=payload)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            try:
                # Get the list of image data from the JSON response
                response_json = response.json()
                image_data_list = response_json.get('images')

                # Check if image data is present
                if image_data_list:
                    for i, image_data_base64 in enumerate(image_data_list):
                        # Decode the base64 image data
                        image_data = base64.b64decode(image_data_base64)

                        # Save each image to a file
                        image_filename = self.result_file
                        with open(image_filename, "wb") as image_file:
                            image_file.write(image_data)
                        print(f"Image {i + 1} saved as '{image_filename}'")
                else:
                    print("Image data list not found in the response JSON.")
            except json.JSONDecodeError:
                print("Error decoding JSON response.")
        else:
            print("Error:", response.status_code, response.text)

        return Image.open(self.result_file)
