import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'validator_project.settings')
django.setup()

from idea_validator.models import IdeaValidationReport
from idea_validator.gemini_service import generate_validation_report

def main():
    print("Starting verification checks...")
    
    # 1. Clean existing records to keep verification clean
    IdeaValidationReport.objects.all().delete()
    print("Cleaned database records.")

    # 2. Test parameters
    idea = "A subscription-based micro-farming box that grows mushrooms at home via IoT"
    audience = "Urban culinary enthusiasts and home cooks who value fresh ingredients"
    budget = "$5,000"
    industry = "SaaS" # Tapped as tech/subscription

    print(f"\nSimulating report generation for:")
    print(f" - Idea: {idea}")
    print(f" - Audience: {audience}")
    print(f" - Budget: {budget}")
    print(f" - Industry: {industry}")

    # 3. Trigger validation report
    report_data = generate_validation_report(idea, audience, budget, industry)
    print(f"Generated report successfully (Mode: {report_data.get('generation_mode')})")
    
    # 4. Save to database
    report = IdeaValidationReport.objects.create(
        startup_idea=idea,
        target_audience=audience,
        budget=budget,
        industry=industry,
        report_data=report_data
    )
    print(f"Persisted report to database. (ID: {report.pk})")

    # 5. Retrieve and verify properties
    retrieved = IdeaValidationReport.objects.get(pk=report.pk)
    print("\nVerifying stored data:")
    print(f" - String representation: {str(retrieved)}")
    print(f" - SWOT Strengths count: {len(retrieved.swot.get('strengths', []))}")
    print(f" - Competitor count: {len(retrieved.competitors.get('competitors', []))}")
    print(f" - Investor Pitch Hook: {retrieved.investor_pitch.get('hook')}")
    print(f" - Improvement suggestions: {len(retrieved.improvements)}")

    assert len(retrieved.swot.get('strengths', [])) > 0
    assert len(retrieved.competitors.get('competitors', [])) > 0
    assert retrieved.investor_pitch.get('hook') is not None
    
    print("\nVerification check PASSED successfully!")

if __name__ == '__main__':
    main()
