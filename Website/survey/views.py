import csv
import os
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def survey(request):
    if request.method == 'POST':
        # Retrieve data from the form
        full_name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        age = request.POST.get('number', '')
        clarity_rating = request.POST.get('dropdown', '')
        strongest_language = request.POST.get('strongest-lang', '')
        strengths = request.POST.getlist('strengths')
        improvements = request.POST.get('textbox', '')

        # CSV file path
        csv_file_path = 'survey_responses.csv'

        # Check if the CSV file already exists
        file_exists = os.path.isfile(csv_file_path)

        # Open the CSV file in append mode
        with open(csv_file_path, 'a', newline='') as csv_file:
            # Create a CSV writer object
            csv_writer = csv.writer(csv_file)

            # If the file doesn't exist, write the header row
            if not file_exists:
                csv_writer.writerow(['Full Name', 'Email', 'Age', 'Clarity Rating', 'Strongest Language',
                                     'Front-End', 'Back-End', 'UI/UX', 'Code Organization and Readability',
                                     'Project Documentation', 'Problem Solving', 'Testing and Quality Assurance', 'Improvements'])

            # Write the survey response data to the CSV file
            csv_writer.writerow([full_name, email, age, clarity_rating, strongest_language,
                                'Front-End' if 'front-end' in strengths else '',
                                'Back-End' if 'back-end' in strengths else '',
                                'UI/UX' if 'ui/ux' in strengths else '',
                                'Code Organization and Readability' if 'organization' in strengths else '',
                                'Project Documentation' if 'documentation' in strengths else '',
                                'Problem Solving' if 'problem-solving' in strengths else '',
                                'Testing and Quality Assurance' if 'testing' in strengths else '',
                                improvements])

        return HttpResponse('Form submitted successfully and data saved to CSV.')

    return render(request, 'survey.html')