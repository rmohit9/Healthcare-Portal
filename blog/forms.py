from django import forms
from .models import BlogPost, Category

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'category', 'image', 'summary', 'content', 'is_draft']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter blog post title'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'summary': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Brief summary of your blog post (max 500 characters)'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 10,
                'placeholder': 'Write your full blog content here...'
            }),
            'is_draft': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
        labels = {
            'title': 'Blog Title',
            'category': 'Category',
            'image': 'Featured Image',
            'summary': 'Summary',
            'content': 'Content',
            'is_draft': 'Save as Draft'
        }
        help_texts = {
            'title': 'Choose a catchy and descriptive title',
            'image': 'Upload an image to make your post more engaging',
            'summary': 'This will be shown in the blog list view',
            'content': 'Write the full content of your blog post',
            'is_draft': 'Check this to save as draft (not visible to patients)'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ensure categories are available
        self.fields['category'].queryset = Category.objects.all()

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 5:
            raise forms.ValidationError("Title must be at least 5 characters long.")
        return title

    def clean_summary(self):
        summary = self.cleaned_data.get('summary')
        if len(summary) < 20:
            raise forms.ValidationError("Summary must be at least 20 characters long.")
        return summary

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content) < 100:
            raise forms.ValidationError("Content must be at least 100 characters long.")
        return content

class CategoryFilterForm(forms.Form):
    """Form for filtering blog posts by category"""
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label="All Categories",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
