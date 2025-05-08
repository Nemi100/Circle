from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Job

PROJECT_TITLE_CHOICES = [
    ('Build a website', 'I want to build a website'),
    ('Redesign website', 'I want to redesign my website'),
    ('Improve search rankings', 'I need help improving my search rankings'),
    ('Create a mobile app', 'I want to create a mobile app'),
    ('Business database', 'I need a database for my business'),
    ('Promotional video game', 'I want to create a promotional video game'),
    ('Content writing', 'I need help writing content for my website or blog'),
    ('Fix website speed', 'I want to fix my website\'s speed or performance'),
    ('Design website or app', 'I need help designing my website or app\'s look'),
    ('Project management', 'I need someone to manage my project and keep it on track'),
]


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'skills_required', 'budget', 'deadline']
        widgets = {
            'title': forms.Select(choices=Job.TITLE_CHOICES, attrs={
                'class': 'form-select',
                'aria-label': 'Project Title',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Describe your project requirements',
                'rows': 4,
                'aria-label': 'Project Description',
            }),
            'skills_required': forms.CheckboxSelectMultiple(attrs={
                'class': 'form-check',
                'aria-label': 'Skills Required',
            }),
            'budget': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter budget in USD',
                'aria-label': 'Budget',
            }),
            'deadline': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'aria-label': 'Deadline',
            }),
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if not title:
            raise forms.ValidationError("Please select a valid project type.")
        return title


    def __init__(self, *args, **kwargs):
        super(JobForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Post Job', css_class="btn btn-primary mt-3"))