import os
import openpyxl
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

        # Excel file path
        excel_file_path = 'survey_responses.xlsx'

        # Create or load the workbook
        if not os.path.isfile(excel_file_path):
            workbook = openpyxl.Workbook()
            sheet = workbook.active
            # Write header row
            header = ['Full Name', 'Email', 'Age', 'Clarity Rating', 'Strongest Language',
                      'Front-End', 'Back-End', 'UI/UX', 'Code Organization and Readability',
                      'Project Documentation', 'Problem Solving', 'Testing and Quality Assurance', 'Improvements']
            sheet.append(header)
        else:
            workbook = openpyxl.load_workbook(excel_file_path)
            sheet = workbook.active

        # Add survey data to the worksheet
        survey_data = [full_name, email, age, clarity_rating, strongest_language,
                       'Front-End' if 'front-end' in strengths else '',
                       'Back-End' if 'back-end' in strengths else '',
                       'UI/UX' if 'ui/ux' in strengths else '',
                       'Code Organization and Readability' if 'organization' in strengths else '',
                       'Project Documentation' if 'documentation' in strengths else '',
                       'Problem Solving' if 'problem-solving' in strengths else '',
                       'Testing and Quality Assurance' if 'testing' in strengths else '',
                       improvements]
        sheet.append(survey_data)

        # Save the workbook
        workbook.save(excel_file_path)

        return HttpResponse('Form submitted successfully and data saved to Excel.')

    return render(request, 'survey.html')