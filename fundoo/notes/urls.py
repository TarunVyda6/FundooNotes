from django.urls import path
from . import views as note_view

urlpatterns = [

    path('note/', note_view.Notes.as_view(), name="note"),
    path('note/<int:pk>', note_view.Notes.as_view(), name="single-note"),
    path('note/archived/', note_view.ArchivedView.as_view(), name="archived"),
    path('note/archived/<int:pk>', note_view.ArchivedView.as_view(), name="single-archived"),
    path('note/pinned/', note_view.PinnedView.as_view(), name="pinned"),
    path('note/pinned/<int:pk>', note_view.PinnedView.as_view(), name="single-pinned"),
    path('note/trash/', note_view.TrashView.as_view(), name="trash"),
    path('note/trash/<int:pk>', note_view.TrashView.as_view(), name="single-trash"),
    path('note/search/', note_view.SearchNote.as_view(), name="search")
]