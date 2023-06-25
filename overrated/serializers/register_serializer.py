import datetime
import os

from django.contrib.auth.hashers import make_password
from dotenv import load_dotenv
from eth_typing import Address

from rest_framework import serializers
from web3 import Web3

from overrated.consts import REPUTATION_CONTRACT_ADDRESS, REPUTATION_CONTRACT_ABI, DEPLOYER_ADDRESS, SEPOLIA_NETWORK_ID
from overrated.models import MyUser

dotenv_path = '/home/vladyslav/PycharmProjects/eth_waterloo_backend/eth_waterloo_backend/.env'
load_dotenv(dotenv_path)

w3 = Web3(Web3.HTTPProvider(os.environ.get("QUICKNODE_PROVIDER")))
reputation_contract = w3.eth.contract(address=Web3.to_checksum_address(REPUTATION_CONTRACT_ADDRESS),
                                      abi=REPUTATION_CONTRACT_ABI)

class RegisterSerializer(serializers.Serializer):
    """
    This serializer defines two fields for authentication:
      * username
      * password.
    It will try to authenticate the user with when validated.
    """
    email = serializers.EmailField(
        label="Email",
    )
    password = serializers.CharField(
        label="Password",
        # This will be used when the DRF browsable API is enabled
        style={'input_type': 'password'},
        trim_whitespace=False,
    )
    public_key = serializers.CharField(
        label="Public key",
        trim_whitespace=True,
    )

    def validate(self, attrs):
        # Take username and password from request
        email = attrs.get('email')
        password = attrs.get('password')
        public_key = attrs.get('public_key')
        # TODO: add check whether it is a valid hex num
        if len(public_key) != 42:
            msg = '"public_key" should have length 42.'
            raise serializers.ValidationError(msg, code=400)
        if email and password and public_key:
            maybe_user = MyUser.objects.filter(
                email=email
            )
            if maybe_user.exists():
                maybe_user.update(
                    password=make_password(password),
                    public_key=public_key,
                    date_of_birth=datetime.date(year=2000, month=1, day=1)
                )
                user = maybe_user[0]

                print("Starting to send a tx for registering phantom account...")
                nonce = w3.eth.get_transaction_count(DEPLOYER_ADDRESS)
                user_creation_txn = reputation_contract.functions.mintUser(
                    Address(public_key),
                    200,
                    user.reputation_before_removing_phantom()
                ).build_transaction({
                    'chainId': SEPOLIA_NETWORK_ID,
                    'gas': 300000,
                    'maxFeePerGas': w3.to_wei('30', 'gwei'),
                    'maxPriorityFeePerGas': w3.to_wei('15', 'gwei'),
                    'nonce': nonce,
                })
                private_key: str = os.environ.get("DEPLOYER_PRIVATE_KEY")
                signed_txn = w3.eth.account.sign_transaction(
                    user_creation_txn,
                    private_key=private_key
                )
                print(f"Signed txn for referring a friend: {str(signed_txn.hash)}")
                w3.eth.send_raw_transaction(signed_txn.rawTransaction)
                print("Sent tx!")
            else:
                user = MyUser.objects.create(
                    email=email,
                    password=make_password(password),
                    public_key=public_key,
                    date_of_birth=datetime.date(year=2000, month=1, day=1)
                )
        else:
            msg = '"username","password" and "public_key" are required.'
            raise serializers.ValidationError(msg, code=400)
        return user