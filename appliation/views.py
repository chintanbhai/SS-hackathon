from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods, require_POST
import json
import google.generativeai as genai
import os
from .models import Product, Consumer, Order
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django import forms

# Configure Gemini API
genai.configure(api_key=os.getenv('GEMINI_API_KEY', 'your-api-key-here'))

# Create your views here.

def index(request):
    return render(request, 'index.html')

def chatbot(request):
    """Render the chatbot page"""
    return render(request, 'chatbot.html')

@csrf_exempt
@require_http_methods(["POST"])
def chat_api(request):
    """API endpoint for chatbot interactions"""
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '')
        
        if not user_message:
            return JsonResponse({
                'error': 'Message is required',
                'status': 'error'
            }, status=400)
        
        # Check if API key is configured
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key or api_key == 'your-api-key-here':
            return JsonResponse({
                'error': 'Gemini API key not configured. Please add your API key to the .env file.',
                'status': 'error'
            }, status=500)
        
        # Initialize the Gemini model with better configuration
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Configure generation parameters for better responses
        generation_config = genai.types.GenerationConfig(
            candidate_count=1,
            max_output_tokens=1000,
            temperature=0.7,
        )
        
        # Create a more conversational prompt
        enhanced_prompt = f"""You are a helpful and friendly AI assistant. Please provide a clear, concise, and conversational response to the following question or message. Use a warm and engaging tone, and format your response in a way that's easy to read and understand.

User message: {user_message}

Response:"""
        
        # Generate response with enhanced prompt and configuration
        response = model.generate_content(
            enhanced_prompt,
            generation_config=generation_config
        )
        
        # Check if response has text
        if not response.text:
            return JsonResponse({
                'error': 'No response generated from the AI model',
                'status': 'error'
            }, status=500)
        
        return JsonResponse({
            'response': response.text,
            'status': 'success'
        })
        
    except Exception as e:
        return JsonResponse({
            'error': f'Error: {str(e)}',
            'status': 'error'
        }, status=500)

def api_home(request):
    """API endpoint for the home page"""
    return JsonResponse({
        'message': 'Welcome to the API',
        'status': 'success'
    })

def about(request):
    """About page view"""
    return render(request, 'about.html')

def contact(request):
    """Contact page view"""
    return render(request, 'contact.html')

def product_list(request):
    query = request.GET.get('q', '')
    products = Product.objects.all()
    if query:
        products = products.filter(name__icontains=query)
    return render(request, 'consumer/product_list.html', {'products': products, 'query': query})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'consumer/product_detail.html', {'product': product})

@csrf_exempt
@require_http_methods(["POST"])
def place_order(request, pk):
    product = get_object_or_404(Product, pk=pk)
    data = request.POST or json.loads(request.body)
    consumer_id = data.get('consumer_id')
    quantity = int(data.get('quantity', 1))
    order_type = data.get('order_type', 'one_time')
    consumer = get_object_or_404(Consumer, pk=consumer_id)
    order = Order.objects.create(
        consumer=consumer,
        product=product,
        quantity=quantity,
        order_type=order_type
    )
    if request.method == 'POST':
        return redirect('product_detail', pk=product.pk)
    return JsonResponse({'status': 'success', 'order_id': order.id})

@login_required
def consumer_dashboard(request):
    # Example: show recent orders and available products
    consumer = None
    orders = []
    if request.user.is_authenticated and hasattr(request.user, 'consumer'):
        consumer = request.user.consumer
        orders = Order.objects.filter(consumer=consumer).order_by('-order_date')[:5]
    products = Product.objects.all()[:6]
    return render(request, 'consumer/dashboard.html', {
        'consumer': consumer,
        'orders': orders,
        'products': products,
    })

class ConsumerSignUpForm(forms.ModelForm):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = Consumer
        fields = ['name', 'email', 'address', 'phone']

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password']
        )
        consumer = super().save(commit=False)
        consumer.user = user
        if commit:
            consumer.save()
        return consumer

def consumer_signup(request):
    if request.method == 'POST':
        form = ConsumerSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('consumer_signin')
    else:
        form = ConsumerSignUpForm()
    return render(request, 'consumer/signup.html', {'form': form})

def consumer_signin(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('product_list')
    else:
        form = AuthenticationForm()
    return render(request, 'consumer/signin.html', {'form': form})

def consumer_logout(request):
    logout(request)
    return redirect('index')

def get_cart(request):
    return request.session.setdefault('cart', {})

def save_cart(request, cart):
    request.session['cart'] = cart
    request.session.modified = True

def cart_view(request):
    cart = get_cart(request)
    product_ids = cart.keys()
    products = Product.objects.filter(id__in=product_ids)
    cart_items = []
    total = 0
    for product in products:
        quantity = cart[str(product.id)]
        subtotal = product.price * quantity
        total += subtotal
        cart_items.append({'product': product, 'quantity': quantity, 'subtotal': subtotal})
    return render(request, 'consumer/cart.html', {'cart_items': cart_items, 'total': total})

@require_POST
def add_to_cart(request, pk):
    cart = get_cart(request)
    quantity = int(request.POST.get('quantity', 1))
    cart[str(pk)] = cart.get(str(pk), 0) + quantity
    save_cart(request, cart)
    return redirect('cart_view')

@require_POST
def remove_from_cart(request, pk):
    cart = get_cart(request)
    if str(pk) in cart:
        del cart[str(pk)]
        save_cart(request, cart)
    return redirect('cart_view')

@require_POST
def update_cart_quantity(request, pk):
    cart = get_cart(request)
    quantity = int(request.POST.get('quantity', 1))
    if quantity > 0:
        cart[str(pk)] = quantity
    else:
        cart.pop(str(pk), None)
    save_cart(request, cart)
    return redirect('cart_view')
