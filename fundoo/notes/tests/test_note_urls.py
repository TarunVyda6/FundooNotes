from django.urls import reverse, resolve


class TestUrls:
    """
    this class will test url's and checks it with matching view_name
    """

    def test_note_url(self):
        """
        this method will test url and matches result with view name as note
        """
        path = reverse("note")
        assert resolve(path).view_name == "note"

    def test_note_archived_url(self):
        """
        this method will test url and matches result with view name as archived
        """
        path = reverse("archived")
        assert resolve(path).view_name == "archived"

    def test_note_pinned_url(self):
        """
        this method will test url and matches result with view name as pinned
        """
        path = reverse("pinned")
        assert resolve(path).view_name == "pinned"

    def test_note_trash_url(self):
        """
        this method will test url and matches result with view name as trash
        """
        path = reverse("trash")
        assert resolve(path).view_name == "trash"

    def test_note_search_url(self):
        """
        this method will test url and matches result with view name as search
        """
        path = reverse("search")
        assert resolve(path).view_name == "search"
