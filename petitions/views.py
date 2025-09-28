from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import MoviePetition, Vote
from .forms import MoviePetitionForm

def petition_list(request):
    petitions = MoviePetition.objects.all().order_by('-created_at')
    
    # Get which petitions the current user has voted for
    user_votes = []
    if request.user.is_authenticated:
        user_votes = Vote.objects.filter(user=request.user).values_list('petition_id', flat=True)
    
    return render(request, 'petitions/petition_list.html', {
        'petitions': petitions,
        'user_votes': user_votes,
    })

@login_required
def create_petition(request):
    if request.method == 'POST':
        form = MoviePetitionForm(request.POST)
        if form.is_valid():
            petition = form.save(commit=False)
            petition.user = request.user
            petition.save()
            messages.success(request, 'Your movie petition has been created successfully!')
            return redirect('petitions:list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = MoviePetitionForm()
    
    return render(request, 'petitions/create_petition.html', {'form': form})

@login_required
def vote_petition(request, petition_id):
    petition = get_object_or_404(MoviePetition, id=petition_id)
    
    # Check if user already voted
    existing_vote = Vote.objects.filter(petition=petition, user=request.user).first()
    
    if existing_vote:
        existing_vote.delete()
        messages.success(request, f'You unvoted for "{petition.title}"')
    else:
        Vote.objects.create(petition=petition, user=request.user)
        messages.success(request, f'You voted for "{petition.title}"')
    
    return redirect('petitions:list')