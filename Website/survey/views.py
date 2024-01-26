import os
import pandas as pd
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

        # Create a DataFrame with the survey response data
        survey_data = pd.DataFrame({
            'Full Name': [full_name],
            'Email': [email],
            'Age': [age],
            'Clarity Rating': [clarity_rating],
            'Strongest Language': [strongest_language],
            'Front-End': ['Front-End' if 'front-end' in strengths else ''],
            'Back-End': ['Back-End' if 'back-end' in strengths else ''],
            'UI/UX': ['UI/UX' if 'ui/ux' in strengths else ''],
            'Code Organization and Readability': ['Code Organization and Readability' if 'organization' in strengths else ''],
            'Project Documentation': ['Project Documentation' if 'documentation' in strengths else ''],
            'Problem Solving': ['Problem Solving' if 'problem-solving' in strengths else ''],
            'Testing and Quality Assurance': ['Testing and Quality Assurance' if 'testing' in strengths else ''],
            'Improvements': [improvements]
        })

        # Check if the Excel file already exists
        file_exists = os.path.isfile(excel_file_path)

        # If the file doesn't exist, write the header row
        if not file_exists:
            survey_data.to_excel(excel_file_path, index=False, engine='openpyxl', sheet_name='Sheet1')
        else:
            # Read the existing Excel file
            existing_data = pd.read_excel(excel_file_path, sheet_name='Sheet1')
            
            # Concatenate the existing data with the new data
            updated_data = pd.concat([existing_data, survey_data], ignore_index=True)
            
            # Write the updated data back to the Excel file
            updated_data.to_excel(excel_file_path, index=False, engine='openpyxl', sheet_name='Sheet1')

        return HttpResponse('Form submitted successfully and data saved to Excel.')

    return render(request, 'survey.html')