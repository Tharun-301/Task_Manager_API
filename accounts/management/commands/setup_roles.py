from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):
    help = 'Creates Admin and User groups for RBAC'

    def handle(self, *args, **kwargs):
        admin_group, created = Group.objects.get_or_create(name='Admin')
        user_group, created2 = Group.objects.get_or_create(name='User')
        self.stdout.write(self.style.SUCCESS('✅ Roles created: Admin, User'))