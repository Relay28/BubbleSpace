# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Note
from .forms import NoteForm

# def notes_list(request):
#     notes = Note.objects.all()
#     return render(request, 'notes/notes_list.html', {'notes': notes})



def notes_list(request):
    notes = Note.objects.all()  # Retrieve all notes
    return render(request, 'notes/notes_list.html', {'notes': notes})


def note_detail(request, pk):
    note = get_object_or_404(Note, pk=pk)
    return render(request, 'notes/note_detail.html', {'note': note})

# def add_note(request):
#     if request.method == 'POST':
#         form = NoteForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('notes_list')
#     else:
#         form = NoteForm()
#     return render(request, 'notes/add_note.html', {'form': form})
def add_note(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('notes_list')
    else:
        form = NoteForm()
    return render(request, 'notes/add_note.html', {'form': form})

def edit_note(request, pk):
    note = get_object_or_404(Note, pk=pk)
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect('notes_list')
    else:
        form = NoteForm(instance=note)
    return render(request, 'notes/edit_note.html', {'form': form})

def delete_note(request, pk):
    note = get_object_or_404(Note, pk=pk)
    if request.method == 'POST':
        note.delete()
        return redirect('notes_list')
    return render(request, 'notes/delete_note.html', {'note': note})
