from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import EmailMessage

@csrf_exempt
def survey(request):
    # Default email address for notifications
    email = 'nicholas.jarrett10@gmail.com'

    if request.method == 'POST':
        # Extracting form data from the POST request
        full_name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        age = request.POST.get('number', '')
        clarity_rating = request.POST.get('dropdown', '')
        strongest_language = request.POST.get('strongest-lang', '')
        strengths = request.POST.getlist('strengths')
        improvements = request.POST.get('textbox', '')

        # Format survey data
        strengths_text = ', '.join(strengths)
        survey_data = f"Full Name: {full_name}\nEmail: {email}\nAge: {age}\nClarity Rating: {clarity_rating}\n" \
                      f"Strongest Language: {strongest_language}\nStrengths: {strengths_text}\n" \
                      f"Improvements: {improvements}"

        # Sending an email notification with the formatted survey data
        subject = 'New GitHub Portfolio Review'
        message = survey_data
        from_email = 'nicholas.jarrett10@gmail.com'
        recipient_list = [email]

        email = EmailMessage(subject, message, from_email, recipient_list)
        email.send()

        # Returning a success message.
        return HttpResponse('Form submitted successfully. Data sent via email.')

    # Rendering the survey form template.
    return render(request, 'survey.html')