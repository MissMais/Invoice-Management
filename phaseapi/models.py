from django.db import models

# Create your models here.
class Phase(models.Model):
    phase_id = models.AutoField(primary_key=True)
    phase_value = models.CharField(max_length=100)

    class Meta:
        db_table = 'phase'