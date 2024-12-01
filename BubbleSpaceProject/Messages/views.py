from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Chat, Message
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from Login.models import Users_Account  # Import your custom user model if needed
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import json
from django.conf import settings


User = get_user_model()  # Get the custom user model

@login_required
def get_user_chats(request):
    """Retrieve all unique chats linked to the logged-in user, displaying only the recipient's username."""
    chats = Chat.objects.filter(sender=request.user) | Chat.objects.filter(recipient=request.user)
    unique_recipients = set()
    chat_data = []

    for chat in chats:
        # Determine the other user in the chat
        if chat.sender == request.user:
            other_user = chat.recipient
        else:
            other_user = chat.sender

        # Only add unique recipient IDs to chat_data
        if other_user.id not in unique_recipients:
            unique_recipients.add(other_user.id)
            chat_data.append({
                'username': other_user.username,
                'recipient_id': other_user.id,  # Send recipient_id instead of chat_id
                'profile_picture': other_user.profile_picture.url if other_user.profile_picture else '/static/default-avatar.jpg',
            })

    return JsonResponse({'status': 'success', 'chats': chat_data})


@login_required
def chat_list(request):
    """View to display a list of all chats for the logged-in user."""
    chats = Chat.objects.filter(sender=request.user) | Chat.objects.filter(recipient=request.user)
    return render(request, 'messages/chat_list.html', {'chats': chats})

@csrf_exempt
@login_required
def send_message(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            recipient_id = data.get("recipient_id")
            message_text = data.get("message")

            # Validate recipient
            try:
                recipient = User.objects.get(id=recipient_id)
            except User.DoesNotExist:
                return JsonResponse({"status": "error", "message": "Recipient not found."})

            # Save message to the database
            Message.objects.create(
                sender=request.user,
                recipient=recipient,
                message=message_text,
            )

            return JsonResponse({"status": "success", "message": "Message sent successfully."})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})

    return JsonResponse({"status": "error", "message": "Invalid request method."})

@login_required
@require_POST
def edit_message(request, message_id):
    """Edit a specific message by ID."""
    message = get_object_or_404(Message, id=message_id, sender=request.user)
    new_content = request.POST.get('message', '').strip()
    if not new_content:
        return JsonResponse({'status': 'error', 'message': 'Message content cannot be empty.'}, status=400)

    message.message = new_content
    message.save()
    return JsonResponse({'status': 'success', 'message': 'Message updated successfully.'})

@login_required
@require_POST
def delete_message(request, message_id):
    """Delete a specific message by ID."""
    message = get_object_or_404(Message, id=message_id, sender=request.user)
    message.delete()
    return JsonResponse({'status': 'success', 'message': 'Message deleted successfully.'})

@login_required
def load_chat_history(request, recipient_id):
    """Load chat history with a specific recipient, sorted by time."""
    try:
        recipient = Users_Account.objects.get(id=recipient_id)

        messages = Message.objects.filter(
            Q(sender=request.user, recipient=recipient) |
            Q(sender=recipient, recipient=request.user)
        ).order_by('date_sent').values(
            'id', 'sender__username', 'message', 'date_sent'
        )

        return JsonResponse({
            'status': 'success',
            'messages': list(messages),
            'current_user': request.user.username  # Add the current user's username
        })

    except Users_Account.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Recipient not found.'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


@login_required
@csrf_exempt
def send_message(request, recipient_id):
    """Send a message to a specific recipient."""
    if request.method == 'POST':
        message_text = request.POST.get('message', '').strip()
        if not message_text:
            return JsonResponse({'status': 'error', 'message': 'Message cannot be empty.'}, status=400)

        sender = request.user
        try:
            recipient = Users_Account.objects.get(id=recipient_id)
            chat, created = Chat.objects.get_or_create(sender=sender, recipient=recipient)

            message = Message.objects.create(chat=chat, sender=sender, recipient=recipient, message=message_text)

            return JsonResponse({'status': 'success', 'message_id': message.id}, status=201)

        except Users_Account.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Recipient not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)

@login_required
def search_users(request):
    """Fetch users that match the search query."""
    query = request.GET.get('q', '')
    users = User.objects.filter(username__icontains=query).values('id', 'username', 'profile_picture')
    user_list = []
    for user in users:
        user_list.append({
            'id': user['id'],
            'username': user['username'],
            'profile_picture': f"{settings.MEDIA_URL}{user['profile_picture']}" if user['profile_picture'] else '/static/default-avatar.jpg',

        })
    return JsonResponse(user_list, safe=False)


@login_required
def get_new_messages(request, chat_id):
    """Fetch new messages for a specific chat based on the last message ID."""
    chat = get_object_or_404(Chat, id=chat_id)
    last_message_id = request.GET.get('last_message_id', 0)

    # Fetch new messages after the last message ID, sorted by date_sent in ascending order
    new_messages = chat.messages.filter(id__gt=last_message_id).order_by('date_sent')
    message_data = [
        {
            'id': msg.id,
            'sender': msg.sender.username,
            'content': msg.message,
            'date_sent': msg.date_sent.strftime('%Y-%m-%d %H:%M:%S')
        }
        for msg in new_messages
    ]
    
    return JsonResponse({'messages': message_data})

def get_chat_messages(request, chat_id):
    """Fetch messages associated with the chat_id."""
    try:
        # Fetch messages associated with the chat_id
        messages = Message.objects.filter(chat_id=chat_id).values(
            'sender__username', 'message', 'date_sent'
        )
        message_list = list(messages)  # Convert QuerySet to a list
        return JsonResponse({'status': 'success', 'messages': message_list}, safe=False)

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


