from mixer.backend.django import mixer
import pytest


@pytest.mark.django_db
class TestModels:
    """
    this class will test model and matches user id after creation of account
    """
    def test_account_id_should_be_one_after_creation(self):
        """
        this method will test model and matches user id as 1 after creation of account
        """
        user = mixer.blend('fundooapp.Account')
        assert user.id == 1

    def test_account_id_should_not_be_zero_after_creation(self):
        """
        this method will test model and should not match user id as 0 after creation of account
        """
        user = mixer.blend('fundooapp.Account')
        assert user.id != 0
