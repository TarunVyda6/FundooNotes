from django.urls import path
from . import views as note_view

urlpatterns = [

    path('notes/', note_view.Notes.as_view(), name="note"),
    path('notes/<int:pk>', note_view.Notes.as_view(), name="single-note"),
    path('notes/archived/', note_view.ArchivedView.as_view(), name="archived"),
    path('notes/archived/<int:pk>', note_view.ArchivedView.as_view(), name="single-archived"),
    path('notes/pinned/', note_view.PinnedView.as_view(), name="pinned"),
    path('notes/pinned/<int:pk>', note_view.PinnedView.as_view(), name="single-pinned"),
    path('notes/trash/', note_view.TrashView.as_view(), name="trash"),
    path('notes/trash/<int:pk>', note_view.TrashView.as_view(), name="single-trash"),
    path('notes/search/', note_view.SearchNote.as_view(), name="search")
]