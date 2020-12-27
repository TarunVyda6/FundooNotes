from mixer.backend.django import mixer
import pytest


@pytest.mark.django_db
class TestModels:

    def test_account_id_should_be_one_after_creation(self):
        user = mixer.blend('fundooapp.Account')
        assert user.id == 1

    def test_account_id_should_not_be_zero_after_creation(self):
        user = mixer.blend('fundooapp.Account')
        assert user.id != 0
