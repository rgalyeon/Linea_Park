from utils.password_handler import get_user_password, encrypt_private_keys
import cryptography
from loguru import logger
import os
from config import ENCRYPTED_DATA_PATH


def encrypt_privates(force=True):

    logger.info('Start encrypting')

    is_keys_encrypted = os.path.exists(ENCRYPTED_DATA_PATH)

    if force:
        is_keys_encrypted = False

    try:
        password = get_user_password(is_keys_encrypted)
        encrypt_private_keys(password)
    except cryptography.fernet.InvalidToken:
        print('Wrong Password')

    logger.info('Successfully encrypted')
