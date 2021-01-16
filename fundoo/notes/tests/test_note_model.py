from mixer.backend.django import mixer
import pytest


@pytest.mark.django_db
class TestModels:
    """
    this class will test model and matches note title and note description after creation of note
    """

    def test_note_model(self):
        """
        this method will test model and matches note title and note description as sample after creation of note
        """
        note = mixer.blend('notes.Note', title='sample note', description='this is a sample note')
        assert note.title == 'sample note'
        assert note.description == 'this is a sample note'
