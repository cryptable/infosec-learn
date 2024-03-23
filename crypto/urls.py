from django.urls import path

from . import views

app_name = "crypto"
urlpatterns = [
    path("", views.index, name="index"),
    path("random/", views.generate_random, name="random"),
    path("hash/", views.calculate_hash, name="hash"),
    path('symmetric/', views.symmetric_cipher, name="symmetric"),
    path("symmetric/encrypt/", views.encrypt_symmetric_cipher, name="symmetric_encrypt"),
    path("symmetric/decrypt/", views.decrypt_symmetric_cipher, name="symmetric_decrypt"),
    path("symmetric/clear/", views.clear_symmetric_session, name="clear_session"),
]
