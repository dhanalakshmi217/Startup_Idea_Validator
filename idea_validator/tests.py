from django.test import TestCase
from django.urls import reverse
from .models import IdeaValidationReport
from .forms import IdeaValidationForm
from .gemini_service import generate_mock_report

class IdeaValidationModelTest(TestCase):
    def setUp(self):
        self.report = IdeaValidationReport.objects.create(
            startup_idea="An AI personal assistant for plant watering",
            target_audience="Urban busy professionals",
            budget="$1,000",
            industry="AI / ML",
            report_data=generate_mock_report(
                "An AI personal assistant for plant watering",
                "Urban busy professionals",
                "$1,000",
                "AI / ML"
            )
        )

    def test_model_fields(self):
        self.assertEqual(self.report.industry, "AI / ML")
        self.assertEqual(self.report.budget, "$1,000")
        self.assertIn("swot", self.report.report_data)

    def test_model_properties(self):
        self.assertIsNotNone(self.report.swot)
        self.assertIsNotNone(self.report.competitors)
        self.assertIsNotNone(self.report.business_model)
        self.assertIsNotNone(self.report.investor_pitch)

    def test_string_representation(self):
        self.assertEqual(str(self.report), "AI / ML - An AI personal assistant for p...")


class IdeaValidationFormTest(TestCase):
    def test_valid_form(self):
        form_data = {
            'startup_idea': 'Test Idea description',
            'target_audience': 'Test target audience',
            'budget': '$5k',
            'industry': 'SaaS'
        }
        form = IdeaValidationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_missing_fields(self):
        form_data = {
            'startup_idea': '',
            'target_audience': 'Test target audience',
            'budget': '$5k',
            'industry': 'SaaS'
        }
        form = IdeaValidationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_other_industry_validation(self):
        # Without custom_industry it should fail
        form_data = {
            'startup_idea': 'Test Idea description',
            'target_audience': 'Test target audience',
            'budget': '$5k',
            'industry': 'Other',
            'custom_industry': ''
        }
        form = IdeaValidationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('custom_industry', form.errors)

        # With custom_industry it should succeed and replace "Other"
        form_data['custom_industry'] = 'My Custom Tech Sector'
        form = IdeaValidationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['industry'], 'My Custom Tech Sector')


class IdeaValidationViewsTest(TestCase):
    def setUp(self):
        self.report = IdeaValidationReport.objects.create(
            startup_idea="Test Startup Idea",
            target_audience="Test Target",
            budget="$5k",
            industry="SaaS",
            report_data=generate_mock_report("Test Startup Idea", "Test Target", "$5k", "SaaS")
        )

    def test_dashboard_view(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'idea_validator/home.html')
        self.assertContains(response, "Test Startup Idea")

    def test_validate_idea_get(self):
        response = self.client.get(reverse('validate_idea'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'idea_validator/validate.html')

    def test_validate_idea_post(self):
        form_data = {
            'startup_idea': 'New Posting Startup Idea',
            'target_audience': 'Target buyers',
            'budget': '$10,000',
            'industry': 'E-commerce'
        }
        # This will trigger Gemini service (since key is missing it uses mock)
        response = self.client.post(reverse('validate_idea'), data=form_data)
        new_report = IdeaValidationReport.objects.filter(startup_idea='New Posting Startup Idea').first()
        self.assertIsNotNone(new_report)
        self.assertEqual(response.status_code, 302) # Redirects to detail view
        self.assertRedirects(response, reverse('report_detail', args=[new_report.pk]))

    def test_report_detail_view(self):
        response = self.client.get(reverse('report_detail', args=[self.report.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'idea_validator/report_detail.html')
        self.assertContains(response, "SWOT Matrix")

    def test_delete_report_view(self):
        response = self.client.post(reverse('delete_report', args=[self.report.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('dashboard'))
        self.assertFalse(IdeaValidationReport.objects.filter(pk=self.report.pk).exists())
