# Django Gemini Chatbot

A Django web application featuring an AI chatbot powered by Google's Gemini API.

## Features

- 🤖 AI-powered chatbot using Google Gemini
- 💬 Real-time chat interface
- 🎨 Modern, responsive design
- ⚡ Fast and reliable responses
- 🔒 Secure API integration

## Setup Instructions

### 1. Install Dependencies

Make sure you have Python installed, then install the required packages:

```bash
pip install django google-generativeai python-dotenv
```

### 2. Get Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the API key

### 3. Configure Environment Variables

1. Open the `.env` file in the root directory
2. Replace `your-gemini-api-key-here` with your actual Gemini API key:

```
GEMINI_API_KEY=your-actual-api-key-here
```

### 4. Run the Application

1. Navigate to the project directory:
```bash
cd "f:\SS hackathon"
```

2. Run Django migrations (if needed):
```bash
python manage.py migrate
```

3. Start the development server:
```bash
python manage.py runserver
```

4. Open your browser and go to: `http://127.0.0.1:8000/`

## Usage

1. **Home Page**: Visit the main page to see the application overview
2. **Chatbot**: Click on the "🤖 Chatbot" link to start chatting
3. **Chat**: Type your message and press Enter or click Send
4. **AI Response**: The Gemini AI will respond to your queries

## Project Structure

```
project/
├── manage.py
├── .env                    # Environment variables
├── appliation/             # Main Django app
│   ├── views.py           # Chatbot logic and views
│   ├── urls.py            # URL routing
│   ├── templates/         # HTML templates
│   │   ├── index.html     # Home page
│   │   └── chatbot.html   # Chatbot interface
│   └── ...
└── project/               # Django project settings
    ├── settings.py        # Main settings
    ├── urls.py           # Main URL configuration
    └── ...
```

## API Endpoints

- `/` - Home page
- `/chatbot/` - Chatbot interface
- `/api/chat/` - Chat API endpoint (POST)

## Features of the Chatbot

- **Natural Language Processing**: Powered by Google's Gemini AI
- **Real-time Responses**: Fast API integration
- **Error Handling**: Graceful error messages
- **Typing Indicators**: Visual feedback during processing
- **Responsive Design**: Works on desktop and mobile
- **Message History**: Scrollable chat history

## Troubleshooting

### Common Issues

1. **API Key Error**: Make sure your Gemini API key is correctly set in the `.env` file
2. **Module Not Found**: Ensure all dependencies are installed with pip
3. **CSRF Error**: The chatbot handles CSRF tokens automatically
4. **Connection Error**: Check your internet connection for API calls

### Getting Help

- Check the Django console for error messages
- Verify your API key is valid at Google AI Studio
- Ensure all required packages are installed

## Security Notes

- Never commit your API key to version control
- Keep your `.env` file secure and private
- Use environment variables for production deployment

## License

This project is for educational purposes. Make sure to follow Google's Gemini API terms of service.
