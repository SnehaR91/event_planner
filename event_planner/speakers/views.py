from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Guest, Speaker
from events.models import Event

@login_required
def add_guest(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST.get('phone', '')
        organization = request.POST.get('organization', '')

        guest, created = Guest.objects.get_or_create(event=event, email=email, defaults={
            'name': name, 'phone': phone, 'organization': organization
        })

        if created:
            messages.success(request, "Guest added successfully!")
        else:
            messages.info(request, "Guest already registered for this event.")

        return redirect('guest_list', event_id=event.id)

    return render(request, 'speakers/add_guest.html', {'event': event})

@login_required
def guest_list(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    guests = Guest.objects.filter(event=event)
    return render(request, 'speakers/guest_list.html', {'event': event, 'guests': guests})

@login_required
def add_speaker(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        bio = request.POST['bio']
        topic = request.POST['topic']

        speaker, created = Speaker.objects.get_or_create(event=event, email=email, defaults={
            'name': name, 'bio': bio, 'topic': topic
        })

        if created:
            messages.success(request, "Speaker added successfully!")
        else:
            messages.info(request, "Speaker already registered for this event.")

        return redirect('speaker_list', event_id=event.id)

    return render(request, 'speakers/add_speaker.html', {'event': event})

@login_required
def speaker_list(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    speakers = Speaker.objects.filter(event=event)
    return render(request, 'speakers/speaker_list.html', {'event': event, 'speakers': speakers})
