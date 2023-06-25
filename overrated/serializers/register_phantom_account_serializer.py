import datetime
import os

import yagmail
from dotenv import load_dotenv
from rest_framework import serializers
from web3 import Web3

from overrated.consts import REPUTATION_CONTRACT_ABI, REPUTATION_CONTRACT_ADDRESS, SEPOLIA_NETWORK_ID, DEPLOYER_ADDRESS
from overrated.models import MyUser

dotenv_path = '/home/vladyslav/PycharmProjects/eth_waterloo_backend/eth_waterloo_backend/.env'
load_dotenv(dotenv_path)

w3 = Web3(Web3.HTTPProvider(os.environ.get("QUICKNODE_PROVIDER")))
reputation_contract = w3.eth.contract(address=Web3.to_checksum_address(REPUTATION_CONTRACT_ADDRESS),
                                      abi=REPUTATION_CONTRACT_ABI)


class RegisterPhantomSerializer(serializers.Serializer):
    """
    This serializer defines two fields for authentication:
      * username
      * password.
    It will try to authenticate the user with when validated.
    """
    sender_email = serializers.EmailField(
        label="Email",
    )
    recipient_email = serializers.EmailField(
        label="Email",
    )
    additional_reputation = serializers.IntegerField(
        label="Additional Reputation",
    )

    def validate(self, attrs):
        # Take username and password from request
        sender_email = attrs.get('sender_email')
        recipient_email = attrs.get('recipient_email')
        additional_reputation = attrs.get('additional_reputation')
        if sender_email and recipient_email and additional_reputation > 0:
            print("Starting to send a check balance tx for registering phantom account...")
            sender = MyUser.objects.filter(email=sender_email)[0]
            sender_number_of_token = reputation_contract.functions.peekBalance(sender.public_key).call()
            print(f"Sent tx! Number of tokens in senders wallet: f{sender_number_of_token}")
            if sender_number_of_token < additional_reputation:
                msg = 'Not enough reputation tokens to send to your friend...'
                raise serializers.ValidationError(msg, code=400)

            MyUser.objects.create(
                email=recipient_email,
                password="",
                public_key="",
                date_of_birth=datetime.date(year=2000, month=1, day=1),
                additional_reputation_for_phantom_account=additional_reputation,
                last_reputation_bump_for_phantom_account=datetime.datetime.now()
            )
            yag = yagmail.SMTP('vladyslav.nekriach', os.environ.get("YAGMAIL_SECRET"))
            contents = [
                f"Hey, it is time to game! Your friend has sent you {additional_reputation} rep in OverRated. Join him "
                f"at http://127.0.0.1:8000!"
            ]
            subject = 'Rate Raid: your friend invited you to OverRated!'
            yag.send('nekriach_vv@knu.ua', subject, contents)
        else:
            msg = '"username","password" and positive reputation bump are required.'
            raise serializers.ValidationError(msg, code=400)
        return recipient_email
