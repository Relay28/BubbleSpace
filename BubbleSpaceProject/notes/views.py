# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Note
from .forms import NoteForm

# def notes_list(request):
#     notes = Note.objects.all()
#     return render(request, 'notes/notes_list.html', {'notes': notes})



@login_required
def notes_list(request):
    notes = Note.objects.filter(user=request.user)  # Only display notes for the logged-in user
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
@login_required
def add_note(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)  # Create the note instance without saving to the database
            note.user = request.user       # Set the user field to the current logged-in user
            note.save()                    # Now save the note with the user field
            return redirect('notes_list')
    else:
        form = NoteForm()
    return render(request, 'notes/add_note.html', {'form': form})

def edit_note(request, pk):
    note = get_object_or_404(Note, pk=pk)  # Fetch the note
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect('note_detail', pk=note.pk)  # Ensure note.pk is passed here
    else:
        form = NoteForm(instance=note)
    
    # Ensure 'note' is included in the context
    return render(request, 'notes/edit_note.html', {'form': form, 'note': note})


def delete_note(request, pk):
    note = get_object_or_404(Note, pk=pk)  
    if request.method == 'POST':
        note.delete()
        return redirect('notes_list')  
    return render(request, 'notes/delete_note.html', {'note': note})  


