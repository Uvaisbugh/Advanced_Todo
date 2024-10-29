from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Todo_model(models.Model):
    PRIORITY_CHOICES = [
        ('L', 'Low'),
        ('M', 'Medium'),
        ('H', 'High'),
    ]
     
    title = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField()
    completed = models.BooleanField(default=False)
    priority = models.CharField(max_length=1, choices=PRIORITY_CHOICES, default='M')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        ordering = ['-created']
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
        
    def __str__(self):
        return f"{self.title} - {self.get_priority_display()} Priority - {'Completed' if self.completed else 'Pending'}"
    
    def is_overdue(self):
        return not self.completed and self.due_date < timezone.now().date()
