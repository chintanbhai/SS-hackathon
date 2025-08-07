from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import google.generativeai as genai
import os
from .models import Product, Consumer, Order

# Configure Gemini API
genai.configure(api_key=os.getenv('GEMINI_API_KEY', 'your-api-key-here'))

# Create your views here.

def home(request):
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
