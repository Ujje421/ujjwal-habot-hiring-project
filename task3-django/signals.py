# Name: Ujjwal [Last Name]
# Contact: [Email / LinkedIn / GitHub]

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import StudentOnboarding, StudentAuditLog

@receiver(post_save, sender=StudentOnboarding)
def audit_student_onboarding(sender, instance, created, **kwargs):
    """
    Automatically log any creation or update of a StudentOnboarding record.
    This eliminates the need for manual audit trailing and ensures compliance.
    """
    action = 'CREATED' if created else 'UPDATED'
    
    all_true = (
        instance.learning_difficulty_confirmed and
        instance.parent_consent_signed and
        instance.iep_document_attached
    )
    status = 'CLEARED' if all_true else 'BLOCKED'

    StudentAuditLog.objects.create(
        student=instance,
        action=action,
        dcyn_clearance_status=status
    )
