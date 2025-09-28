from django.shortcuts import render
from .models import Order, Item, CheckoutFeedback
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.db.models import Q
# Create your views here.
from django.shortcuts import get_object_or_404, redirect
from movies.models import Movie
from .utils import calculate_cart_total
from .forms import CheckoutFeedbackForm  # Make sure you have this
def index(request):
    cart_total = 0
    movies_in_cart = []
    cart = request.session.get('cart', {})
    movie_ids = list(cart.keys())
    if (movie_ids != []): movies_in_cart = Movie.objects.filter(id__in=movie_ids)
    cart_total = calculate_cart_total(cart, movies_in_cart)
    template_data = {}
    template_data['title'] = 'Cart'
    template_data['movies_in_cart'] = movies_in_cart
    template_data['cart_total'] = cart_total
    return render(request, 'cart/index.html',{'template_data': template_data})

def add(request, id):
    get_object_or_404(Movie, id=id)
    cart = request.session.get('cart', {})
    cart[id] = request.POST['quantity']
    request.session['cart'] = cart
    return redirect('cart.index')

def clear(request):
    request.session['cart'] = {}
    return redirect('cart.index')

@login_required
def purchase(request):
    cart = request.session.get('cart', {})
    movie_ids = list(cart.keys())
    if (movie_ids == []):
        return redirect('cart.index')
    movies_in_cart = Movie.objects.filter(id__in=movie_ids)
    cart_total = calculate_cart_total(cart, movies_in_cart)
    order = Order()
    order.user = request.user
    order.total = cart_total
    order.save()
    for movie in movies_in_cart:
        item = Item()
        item.movie = movie
        item.price = movie.price
        item.order = order
        item.quantity = cart[str(movie.id)]
        item.save()
    request.session['cart'] = {}
    
    # Redirect to confirmation page with feedback form
    return redirect('cart.purchase_confirmation', order_id=order.id)  # This line is important!

@login_required
def purchase_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    # Check if feedback already exists for this order
    feedback_exists = CheckoutFeedback.objects.filter(order=order).exists()
    
    if request.method == 'POST' and not feedback_exists:
        form = CheckoutFeedbackForm(request.POST, initial={'user': request.user})
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.order = order
            feedback.user = request.user
            
            # If anonymous is checked, don't save username
            if form.cleaned_data['anonymous']:
                feedback.username = None
                
            feedback.save()
            return redirect('cart.purchase_confirmation', order_id=order.id)
    else:
        form = CheckoutFeedbackForm(initial={'user': request.user})
    
    template_data = {
        'title': 'Purchase Confirmation',
        'order_id': order.id,
        'form': form,
        'feedback_exists': feedback_exists,
    }
    return render(request, 'cart/purchase_confirmation.html', {'template_data': template_data})

@login_required
def feedback_list(request):
    # Regular users see only their own feedback, staff see all feedback
    if request.user.is_staff:
        feedbacks = CheckoutFeedback.objects.all().order_by('-created_at')
    else:
        feedbacks = CheckoutFeedback.objects.filter(
            Q(user=request.user) | Q(username=request.user.username)
        ).order_by('-created_at')
    
    # Add pagination
    paginator = Paginator(feedbacks, 10)  # Show 10 feedbacks per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    template_data = {
        'title': 'My Checkout Feedback',
        'feedbacks': page_obj,
        'page_obj': page_obj,
        'is_staff': request.user.is_staff,
    }
    return render(request, 'cart/feedback_list.html', {'template_data': template_data})