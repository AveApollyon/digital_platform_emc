from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords

class HistoricalUser(User):
    class Meta:
        proxy = True
    history = HistoricalRecords()
