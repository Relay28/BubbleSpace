from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Note
from .forms import NoteForm

# In views.py, the notes_list view:
@login_required
def notes_list(request):
    notes = Note.objects.filter(user=request.user)
    return render(request, 'notes/notes_list.html', {'notes': notes})

@login_required
def note_detail_api(request, pk):
    # Ensure the note exists and belongs to the currently authenticated user
    note = get_object_or_404(Note, pk=pk, user=request.user)

    # Return the note details in JSON format
    data = {
        "title": note.title,
        "description": note.description,
        "content": note.content,
    }
    return JsonResponse(data)




@login_required
def add_note(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            return redirect('notes_list')
    else:
        form = NoteForm()
    return render(request, 'notes/add_note.html', {'form': form})

@login_required
def edit_note(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect('notes_list')
    else:
        form = NoteForm(instance=note)
    return render(request, 'notes/edit_note.html', {'form': form, 'note': note})

@login_required
def delete_note(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    if request.method == 'POST':
        note.delete()
        return redirect('notes_list')
    return render(request, 'notes/delete_note.html', {'note': note})
