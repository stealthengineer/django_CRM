# dcrm/views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from website.models import Record
from website.forms import SignupForm
import requests

GOOGLE_NEWS_API_KEY = '31dbd5d65ff7e02e8b65d85cf68afd08'  # Replace with your API key

def fetch_news():
    """
    Fetches latest news articles using GNews API.
    """
    url = f"https://gnews.io/api/v4/top-headlines?lang=en&country=us&max=10&apikey=31dbd5d65ff7e02e8b65d85cf68afd08"

    try:
        response = requests.get(url)
        data = response.json()

        # Debugging output
        print("API Response:", data)

        if "articles" in data:  # GNews does not have a "status" field
            return data["articles"]  # Return list of articles
        else:
            print("Error: Unexpected API response structure:", data)

    except Exception as e:
        print(f"Error fetching news: {e}")

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

    # Print for debugging
    print("News Articles:", news_articles)

    return render(request, 'website/home.html', {
        'records': records,
        'record_logged_in': logged_in_record,
        'news_articles': news_articles,  # Pass news articles to template
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

