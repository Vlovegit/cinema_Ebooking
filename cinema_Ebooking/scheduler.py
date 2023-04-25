from django.utils import timezone
from models import Tickets

def expire_old_tickets():
    ten_minutes_ago = timezone.now() - timezone.timedelta(minutes=10)
    tickets_to_expire = Tickets.objects.filter(isBooked=False, time_created__lt=ten_minutes_ago, status='Active')
    print('I am in the scheduler')
    for ticket in tickets_to_expire:
        ticket.status = 'Expired'
        ticket.save()
