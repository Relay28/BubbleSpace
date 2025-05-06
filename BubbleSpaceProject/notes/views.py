# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest
from .models import Note
from .forms import NoteForm

# Notes list view
@login_required
def notes_list(request):
    notes = Note.objects.filter(user=request.user)
    return render(request, 'notes/notes_list.html', {'notes': notes})

# Note detail API view
@login_required
def note_detail_api(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    data = {
        "title": note.title,
        "description": note.description,
        "content": note.content,
    }
    return JsonResponse(data)

# Add a new note
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

# Edit an existing note
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

# Delete a note
@login_required
def delete_note(request, pk):
    if request.method == 'POST':
        note = get_object_or_404(Note, pk=pk, user=request.user)
        note.delete()
        return JsonResponse({'success': True})
    else:
        return HttpResponseBadRequest("Invalid request method.")
