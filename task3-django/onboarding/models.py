# Name: Ujjwal [Last Name]
# Contact: [Email / LinkedIn / GitHub]

from django.db import models
import uuid

class LSA(models.Model):
    """Stub model for Learning Support Assistant."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)

class StudentOnboarding(models.Model):
    CLEARANCE_CHOICES = [
        ('CLEARED', 'Cleared'),
        ('BLOCKED', 'Blocked'),
    ]

    student_full_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    learning_difficulty_confirmed = models.BooleanField()
    parent_consent_signed = models.BooleanField()
    emergency_contact_name = models.CharField(max_length=100)
    emergency_contact_phone = models.CharField(max_length=20)
    school_grade = models.PositiveSmallIntegerField()
    iep_document_attached = models.BooleanField(default=False)
    assigned_lsa = models.ForeignKey(LSA, on_delete=models.SET_NULL, null=True, blank=True)
    dcyn_clearance_status = models.CharField(max_length=10, choices=CLEARANCE_CHOICES, editable=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'student_onboarding'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['assigned_lsa']),
            models.Index(fields=['dcyn_clearance_status']),
        ]

class StudentAuditLog(models.Model):
    ACTION_CHOICES = [
        ('CREATED', 'Created'),
        ('UPDATED', 'Updated'),
    ]
    student = models.ForeignKey(StudentOnboarding, on_delete=models.CASCADE)
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    dcyn_clearance_status = models.CharField(max_length=10)
