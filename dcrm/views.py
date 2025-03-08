from django.shortcuts import render, redirect
from django.contrib import messages
from website.models import Record
from website.forms import SignupForm
import requests
from django.http import JsonResponse

def get_chat_message(request):
    return JsonResponse({
        "message": "Hello! This is a ChatGPT-style response from Django."
    })

GNEWS_API_KEY = "31dbd5d65ff7e02e8b65d85cf68afd08"  # Replace with your actual API key

def fetch_news():
    """
    Fetches news articles using GNews API.
    """
    url = f"https://gnews.io/api/v4/top-headlines?lang=en&country=us&max=10&apikey=31dbd5d65ff7e02e8b65d85cf68afd08"

    try:
        response = requests.get(url)
        print("Status Code:", response.status_code)  # Debugging

        if response.status_code == 200:
            data = response.json()
            print("API Response:", data)  # Debugging output

            # Check if "articles" exists in response instead of "data"
            if "articles" in data and isinstance(data["articles"], list):
                return data["articles"]  # Return the articles list

            print("Error: Unexpected API response structure. Check if 'articles' key exists.", data)
        else:
            print("Error: API request failed with status", response.status_code, response.text)

    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")

    return []  # Return empty list on error


def home(request):
    """
    Shows all records if a user is logged in (session-based),
    otherwise shows a login form.
    """
    logged_in_record = get_logged_in_record(request)
    if logged_in_record:
        records = Record.objects.all()
    else:
        records = []

    # Fetch news articles
    news_articles = fetch_news()

    # Debugging output
    print("News Articles:", news_articles)

    # Dynamic text for the typing effect
    dynamic_text = "Welcome to Crene! Your one-stop solution for managing records and news updates."

    return render(request, 'website/home.html', {
        'records': records,
        'record_logged_in': logged_in_record,
        'news_articles': news_articles,  # Pass news articles to template
        'dynamic_text': dynamic_text  # Pass dynamic text for typing effect
    })

def login_user(request):
    """
    Logs in a user by validating username/password in the Record model,
    then storing record_id in the session.
    """
    if request.method == "POST":
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        if not username or not password:
            messages.error(request, "Username and password are required.")
            return redirect('home')

        try:
            # Attempt to find matching record in the DB
            record = Record.objects.get(username=username, password=password)
            # If found, set a session variable to indicate "logged in"
            request.session['record_id'] = record.id
            messages.success(request, f"Logged in as {record.username}.")
        except Record.DoesNotExist:
            messages.error(request, "Invalid Record credentials.")

        return redirect('home')

    # If GET request, just go back home
    return redirect('home')

def logout_user(request):
    """
    Logs out the user by clearing the 'record_id' from session.
    """
    if 'record_id' in request.session:
        del request.session['record_id']
    messages.success(request, 'You have been logged out.')
    return redirect('home')

def dashboard(request):
    """
    Shows a protected page. If not logged in (no record_id in session),
    redirect them to home with an error message.
    """
    logged_in_record = get_logged_in_record(request)
    if not logged_in_record:
        messages.error(request, "You must be logged in first.")
        return redirect('home')

    # If logged in, show the dashboard. Maybe also pass the records or do something else.
    records = Record.objects.all()
    return render(request, 'website/dashboard.html', {
        'records': records,
        'record_logged_in': logged_in_record,
    })

def register(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            new_record = form.save()
            messages.success(request, "You've successfully registered!")
            return redirect('home')  # or wherever you want to go after registering
    else:
        form = SignupForm()

    return render(request, 'website/register.html', {'form': form})

# --- Helper Function ---

def get_logged_in_record(request):
    """
    Returns the Record object if the user is 'logged in' (record_id in session),
    otherwise None.
    """
    record_id = request.session.get('record_id')
    if record_id:
        try:
            return Record.objects.get(id=record_id)
        except Record.DoesNotExist:
            pass
    return None
