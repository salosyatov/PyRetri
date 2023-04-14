import base64
import io

import numpy as np
from PIL import Image
from flask import Flask, request, make_response

from main.single_index import Recognizer

# config

TOP_K = 5                     # api service provide top 5 now


app = Flask(__name__)


def get_top_similar(image: np.ndarray):
    recognizer = Recognizer()
    paths, names = recognizer.find_similar(image, k=TOP_K)
    top_similar = {"paths": paths, "labels": names}
    return top_similar


@app.route('/ping', methods=['GET'])
def ping():
    return make_response("It works", 200)


@app.route('/api/top_k', methods=['POST'])
def top_k():
    payload = request.form.to_dict(flat=False)

    im_b64 = payload['image'][0]  # remember that now each key corresponds to list.
    # see https://jdhao.github.io/2020/03/17/base64_opencv_pil_image_conversion/
    # for more info on how to convert base64 image to PIL Image object.
    im_binary = base64.b64decode(im_b64)
    buf = io.BytesIO(im_binary)
    image = Image.open(buf)

    top_similar = get_top_similar(image)
    return make_response(top_similar, 200)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
