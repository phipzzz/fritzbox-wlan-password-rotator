from app.config import (
    PW_CHARSET_ASCII_LOWERCASE, 
    PW_CHARSET_ASCII_UPPERCASE, 
    PW_CHARSET_DIGITS, 
    PW_CHARSET_PUNCTUATION_USE_CUSTOM, 
    PW_CHARSET_PUNCTUATION, 
    PW_CHARSET_PUNCTUATION_CUSTOM, 
    PW_LENGTH,
)
import string
import secrets
import hashlib
import binascii

def guarantee_contains(charset):
    return secrets.choice(charset)

def generate_password():

    pw_temp = []
    guaranteed_count = 0

    char_set = ""
    if PW_CHARSET_ASCII_LOWERCASE:
        char_set += string.ascii_lowercase
        pw_temp.append(guarantee_contains(string.ascii_lowercase))
        guaranteed_count += 1
    if PW_CHARSET_ASCII_UPPERCASE:
        char_set += string.ascii_uppercase
        pw_temp.append(guarantee_contains(string.ascii_uppercase))
        guaranteed_count += 1
    if PW_CHARSET_DIGITS:
        char_set += string.digits
        pw_temp.append(guarantee_contains(string.digits))
        guaranteed_count += 1
    if PW_CHARSET_PUNCTUATION:
        if PW_CHARSET_PUNCTUATION_USE_CUSTOM:
            char_set += PW_CHARSET_PUNCTUATION_CUSTOM
            pw_temp.append(guarantee_contains(PW_CHARSET_PUNCTUATION_CUSTOM))
            guaranteed_count += 1
        else:
            char_set += string.punctuation
            pw_temp.append(guarantee_contains(string.punctuation))
            guaranteed_count += 1

    remaining_chars = [secrets.choice(char_set) for _ in range(PW_LENGTH - guaranteed_count)]

    password = pw_temp + remaining_chars

    secrets.SystemRandom().shuffle(password)

    return ''.join(password)

def calculate_psk(passphrase, ssid):

    salt = ssid.encode('utf-8')
    psk = hashlib.pbkdf2_hmac('sha1', passphrase.encode('utf-8'), salt, 4096, 32)

    return binascii.hexlify(psk).decode('utf-8').upper()