from captcha.image import ImageCaptcha
from flask import Response, session
from flask_restful import Resource

from app.libs.helper import get_random_string


class ResourceCaptcha(Resource):
    def get(self):
        captcha = get_random_string(4)
        session["captcha"] = captcha
        image = ImageCaptcha()
        data = image.generate(captcha)
        return Response(data, mimetype="image/jpeg")
