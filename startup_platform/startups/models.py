from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Startup(models.Model):
    INDUSTRY_CHOICES = [
        ('technology', 'Technology'),
        ('healthcare', 'Healthcare'),
        ('finance', 'Finance'),
        ('education', 'Education'),
        ('ecommerce', 'E-commerce'),
        ('clean_energy', 'Clean Energy'),
        ('food_beverage', 'Food & Beverage'),
        ('transportation', 'Transportation'),
        ('real_estate', 'Real Estate'),
        ('other', 'Other'),
    ]

    STAGE_CHOICES = [
        ('idea', 'Idea'),
        ('mvp', 'MVP'),
        ('seed', 'Seed'),
        ('series_a', 'Series A'),
        ('series_b', 'Series B'),
        ('growth', 'Growth'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField()
    industry = models.CharField(max_length=50, choices=INDUSTRY_CHOICES)
    stage = models.CharField(max_length=20, choices=STAGE_CHOICES)
    location = models.CharField(max_length=200, blank=True)
    website = models.URLField(blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    logo = models.CharField(max_length=10, default='🚀')  # Emoji logo
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Relationships
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='startups')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_startups')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    approved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    @property
    def is_approved(self):
        return self.status == 'approved'