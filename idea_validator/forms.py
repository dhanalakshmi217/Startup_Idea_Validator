from django import forms
from .models import IdeaValidationReport

class IdeaValidationForm(forms.ModelForm):
    # Optional field to capture custom industry if "Other" is chosen
    custom_industry = forms.CharField(
        required=False,
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Type your custom industry here...',
            'class': 'glass-input hidden',
            'id': 'id_custom_industry'
        })
    )

    class Meta:
        model = IdeaValidationReport
        fields = ['startup_idea', 'target_audience', 'budget', 'industry']
        widgets = {
            'startup_idea': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Describe your startup idea in detail (e.g., A subscription service for office plants with IoT water sensors)...',
                'class': 'glass-input',
                'required': 'required'
            }),
            'target_audience': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Who is your ideal customer? (e.g., Small to medium office managers, eco-conscious professionals)...',
                'class': 'glass-input',
                'required': 'required'
            }),
            'budget': forms.TextInput(attrs={
                'placeholder': 'E.g., $10,000 or $50k...',
                'class': 'glass-input',
                'required': 'required'
            }),
            'industry': forms.Select(choices=[
                ('SaaS', 'Software as a Service (SaaS)'),
                ('AI / ML', 'Artificial Intelligence / Machine Learning'),
                ('FinTech', 'Financial Technology (FinTech)'),
                ('E-commerce', 'E-commerce & Retail'),
                ('HealthTech', 'Health & Wellness Tech'),
                ('EdTech', 'Education Technology'),
                ('CleanTech', 'Clean & Green Tech'),
                ('Food & Beverage', 'Food & Beverage'),
                ('Other', 'Other (Specify)')
            ], attrs={
                'class': 'glass-input',
                'id': 'id_industry',
                'required': 'required'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        industry = cleaned_data.get('industry')
        custom_industry = cleaned_data.get('custom_industry')

        if industry == 'Other':
            if not custom_industry:
                self.add_error('custom_industry', 'Please specify your industry if you select "Other".')
            else:
                cleaned_data['industry'] = custom_industry
        
        return cleaned_data
