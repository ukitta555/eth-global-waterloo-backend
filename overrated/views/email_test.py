import os

import yagmail
from dotenv import load_dotenv
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

dotenv_path = os.path.join('/home/vladyslav/PycharmProjects/eth_waterloo_backend/eth_waterloo_backend/.env')
load_dotenv(dotenv_path)
print(os.environ.get("DB_NAME"))

class EmailTestView(APIView):

    def post(self, request):
        yag = yagmail.SMTP('vladyslav.nekriach', os.environ.get("YAGMAIL_SECRET"))
        contents = [
            "This is the body, and here is just text http://somedomain/image.png",
            "You can find an audio file attached.", '/local/path/to/song.mp3'
        ]
        yag.send('nekriach_vv@knu.ua', 'hey, here is an email', contents)
        # Alternatively, with a simple one-liner:
        return Response("EMAIL SENT!!!!", status=status.HTTP_200_OK)