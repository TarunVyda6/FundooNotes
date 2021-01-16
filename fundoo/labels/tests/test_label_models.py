from mixer.backend.django import mixer
import pytest


@pytest.mark.django_db
class TestModels:
    """
    this class will test model and matches label_name after creation of label
    """

    def test_label_model(self):
        """
        this method will test model and matches label_name as sample after creation of label
        """
        label = mixer.blend('labels.Label', label_name='sample')
        assert label.label_name == 'sample'
