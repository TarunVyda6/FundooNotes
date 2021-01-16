from django.urls import reverse, resolve


class TestUrls:
    def test_label_url(self):
        """
        this method will test label url and matches result with view name as label-post
        """
        path = reverse("label-post")
        assert resolve(path).view_name == "label-post"

    def test_specific_label_url(self):
        """
        this method will test specific label url and matches result with view name as label
        """
        path = reverse("label", args=[1])
        assert resolve(path).view_name == "label"
