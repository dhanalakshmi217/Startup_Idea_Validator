from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count
from .models import IdeaValidationReport
from .forms import IdeaValidationForm
from .gemini_service import generate_validation_report

def dashboard(request):
    """
    Renders the main dashboard landing page showing past validation reports and metric cards.
    """
    reports = IdeaValidationReport.objects.all()
    total_count = reports.count()
    
    # Calculate top industry
    industry_stats = reports.values('industry').annotate(count=Count('id')).order_by('-count')
    top_industry = industry_stats[0]['industry'] if industry_stats.exists() else "N/A"
    
    return render(request, 'idea_validator/home.html', {
        'reports': reports,
        'total_count': total_count,
        'top_industry': top_industry,
    })

def validate_idea(request):
    """
    Handles rendering and submission of the startup idea entry form.
    Calls gemini_service to generate SWOT, Pitch, Competitors etc.
    """
    if request.method == 'POST':
        form = IdeaValidationForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            
            # Generate Gemini Report (returns a dict containing SWOT, Marketing, Pitch, etc.)
            report_data = generate_validation_report(
                idea=report.startup_idea,
                target_audience=report.target_audience,
                budget=report.budget,
                industry=report.industry
            )
            
            report.report_data = report_data
            report.save()
            return redirect('report_detail', pk=report.pk)
    else:
        form = IdeaValidationForm()
        
    return render(request, 'idea_validator/validate.html', {'form': form})

def report_detail(request, pk):
    """
    Renders the detailed multi-tab analysis report.
    """
    report = get_object_or_404(IdeaValidationReport, pk=pk)
    return render(request, 'idea_validator/report_detail.html', {'report': report})

def delete_report(request, pk):
    """
    Deletes a saved validation report.
    """
    report = get_object_or_404(IdeaValidationReport, pk=pk)
    if request.method == 'POST':
        report.delete()
    return redirect('dashboard')
