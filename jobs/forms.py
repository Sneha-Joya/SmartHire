from django import forms
from .models import Job, Application, Category, ProjectUpdate, ProjectFeedback


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'category', 'budget', 'hourly_rate', 'required_skills', 'deadline']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 6, 'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'budget': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Fixed budget (optional)'}),
            'hourly_rate': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Hourly rate (optional)'}),
            'required_skills': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Python, Django, JavaScript'}),
            'deadline': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
        help_texts = {
            'budget': 'Enter either a fixed budget or hourly rate (or both)',
            'hourly_rate': 'Enter either a fixed budget or hourly rate (or both)',
        }


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['proposal', 'proposed_rate', 'estimated_hours']
        widgets = {
            'proposal': forms.Textarea(attrs={'rows': 6, 'class': 'form-control', 'placeholder': 'Explain why you are the best fit for this job...'}),
            'proposed_rate': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Your proposed rate'}),
            'estimated_hours': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Estimated hours to complete'}),
        }


class ProjectUpdateForm(forms.ModelForm):
    class Meta:
        model = ProjectUpdate
        fields = ['status', 'title', 'description', 'attachment']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Update title (e.g., Milestone 1 Complete)'}),
            'description': forms.Textarea(attrs={'rows': 6, 'class': 'form-control', 'placeholder': 'Describe the progress, what has been completed, and any notes...'}),
            'attachment': forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf,.doc,.docx,.zip,.rar'}),
        }


class ProjectFeedbackForm(forms.ModelForm):
    class Meta:
        model = ProjectFeedback
        fields = ['feedback_type', 'comment', 'is_approved']
        widgets = {
            'feedback_type': forms.Select(attrs={'class': 'form-select'}),
            'comment': forms.Textarea(attrs={'rows': 5, 'class': 'form-control', 'placeholder': 'Provide your feedback, approval, or request revisions...'}),
            'is_approved': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

