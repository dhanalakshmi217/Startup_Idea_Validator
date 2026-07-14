from django.db import models

class IdeaValidationReport(models.Model):
    startup_idea = models.TextField()
    target_audience = models.TextField()
    budget = models.CharField(max_length=100)
    industry = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    report_data = models.JSONField()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.industry} - {self.startup_idea[:30]}..."

    @property
    def swot(self):
        return self.report_data.get('swot', {})

    @property
    def competitors(self):
        return self.report_data.get('competitors', {})

    @property
    def business_model(self):
        return self.report_data.get('business_model', {})

    @property
    def marketing_plan(self):
        return self.report_data.get('marketing_plan', {})

    @property
    def revenue_model(self):
        return self.report_data.get('revenue_model', {})

    @property
    def risks(self):
        return self.report_data.get('risks', [])

    @property
    def improvements(self):
        return self.report_data.get('improvements', [])

    @property
    def investor_pitch(self):
        return self.report_data.get('investor_pitch', {})
