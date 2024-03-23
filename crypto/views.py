import binascii
import secrets

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from django.shortcuts import render, redirect
from hashlib import sha256


def index(request):
    return render(request, "index.html")


def generate_random(request):
    if request.method == "POST":
        random_data = secrets.token_hex(int(request.POST['random_input']))
    else:
        random_data = secrets.token_hex(32)
    context = {"random": random_data}
    return render(request, "random/index.html", context)


def calculate_hash(request):
    if request.method == "POST":
        hash_sha256 = sha256(request.POST["hash_input"].encode("utf-8")).hexdigest()
    else:
        hash_sha256 = None
    context = {"hash": hash_sha256}
    return render(request, "hash/index.html", context)


def symmetric_cipher(request):
    if request.session.get("iv") and request.session.get("key") and request.session.get("plaintext") and request.session.get("ciphertext"):
        iv = request.session.get("iv")
        key = request.session.get("key")
        plaintext = request.session.get("plaintext")
        ciphertext = request.session.get("ciphertext")
        decipheredtext = request.session.get("decipheredtext")
        return render(request, "symmetric/index.html", {
            "iv": iv,
            "key": key,
            "plaintext": plaintext,
            "ciphertext": ciphertext,
            "decipheredtext": decipheredtext
        })
    return render(request, "symmetric/index.html", {
        "iv": "0271f0be77083acfad6f34feca7c8c2c",
        "key": "6c7e8b1a7debd2a55d99b521b77c4dff",
        "plaintext": "Some text to encrypt",
        "ciphertext": None,
        "decipheredtext": None
    })


def encrypt_symmetric_cipher(request):
    cipher = AES.new(binascii.unhexlify(request.POST["key_input"].encode("utf-8")),
                     AES.MODE_CBC,
                     binascii.unhexlify(request.POST["iv_input"].encode("utf-8")))
    ciphertext = cipher.encrypt(pad(request.POST["plaintext_input"].encode("utf-8"), AES.block_size)).hex()
    request.session["iv"] = request.POST["iv_input"]
    request.session["key"] = request.POST["key_input"]
    request.session["plaintext"] = request.POST["plaintext_input"]
    request.session["ciphertext"] = ciphertext
    return redirect("crypto:symmetric")


def decrypt_symmetric_cipher(request):
    cipher = AES.new(binascii.unhexlify(request.POST["key_input"].encode("utf-8")),
                     AES.MODE_CBC,
                     binascii.unhexlify(request.POST["iv_input"].encode("utf-8")))
    decipheredtext = cipher.decrypt(request.POST["cyphertext_input"].encode("utf-8"))
    request.session["iv"] = request.POST["iv_input"]
    request.session["key"] = request.POST["key_input"]
    request.session["decipheredtext"] = decipheredtext
    request.session.save()
    return redirect("crypto:symmetric")


def clear_symmetric_session(request):
    request.session.clear()
    return redirect("crypto:symmetric")
