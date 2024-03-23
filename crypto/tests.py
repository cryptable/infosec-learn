import pytest
from django.test import Client
from.views import calculate_hash


@pytest.fixture
def client():
    return Client()


@pytest.mark.django_db
def test_hash_with_post_request(client):
    response = client.post(
        "/crypto/hash/",
        data={"hash_input": "test input"},
    )
    assert response.context["hash"] == "9dfe6f15d1ab73af898739394fd22fd72a03db01834582f24bb2e1c66c7aaeae"


@pytest.mark.django_db
def test_hash_with_get_request(client):
    response = client.get(
        "/crypto/hash/",
        data={"hash_input": "test input"},
    )
    assert response.context["hash"] is None


@pytest.mark.django_db
def test_symmetric_cipher_with_get_request(client):
    response = client.get(
        "/crypto/symmetric/"
    )
    assert response.context["iv"] == "0271f0be77083acfad6f34feca7c8c2c"
    assert response.context["key"] == "6c7e8b1a7debd2a55d99b521b77c4dff"
    assert response.context["plaintext"] == "Some text to encrypt"


@pytest.mark.django_db
def test_symmetric_cipher_with_post_request_ciphertext(client):
    response = client.post(
        "/crypto/symmetric/encrypt/",
        follow=True,
        data={
            "iv_input": "0271f0be77083acfad6f34feca7c8c2c",
            "key_input": "6c7e8b1a7debd2a55d99b521b77c4dff",
            "plaintext_input": "Some text to encrypt",
        }
    )
    assert response.context["iv"] == "0271f0be77083acfad6f34feca7c8c2c"
    assert response.context["key"] == "6c7e8b1a7debd2a55d99b521b77c4dff"
    assert response.context["plaintext"] == "Some text to encrypt"
    assert response.context["ciphertext"] == "5aed98f33a87f7803e5e8d9c4c624fd474cc1f205f0f889f0de1fe3bd3541df2"
    assert response.context["decipheredtext"] == None


@pytest.mark.django_db
def test_symmetric_cipher_with_post_request_deciphertext(client):
    response = client.post(
        "/crypto/symmetric/decrypt/",
        follow=True,
        data={
            "iv_input": "0271f0be77083acfad6f34feca7c8c2c",
            "key_input": "6c7e8b1a7debd2a55d99b521b77c4dff",
            "plaintext_input": "Some text to encrypt",
            "ciphertext_input": "5aed98f33a87f7803e5e8d9c4c624fd474cc1f205f0f889f0de1fe3bd3541df2",
        }
    )
    assert response.context["iv"] == "0271f0be77083acfad6f34feca7c8c2c"
    assert response.context["key"] == "6c7e8b1a7debd2a55d99b521b77c4dff"
    assert response.context["plaintext"] == "Some text to encrypt"
    assert response.context["ciphertext"] == "5aed98f33a87f7803e5e8d9c4c624fd474cc1f205f0f889f0de1fe3bd3541df2"
    assert response.context["decipheredtext"] == "Some text to encrypt"
