import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'acme_corp.settings')
django.setup()

from django.contrib.auth.models import User

def create_test_users():
    """Create test users with weak passwords for brute force testing"""
    
    users = [
        ('admin', 'admin123'),
        ('john', 'password123'),
        ('sarah', 'sarah2023'),
        ('mike', 'letmein'),
        ('test', 'test'),
        ('user1', '123456'),
        ('user2', 'qwerty'),
        ('user3', 'password'),
        ('user4', 'admin'),
        ('user5', 'welcome'),
    ]
    
    print("Creating test users for brute force practice...")
    
    for username, password in users:
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(username=username, password=password)
            print(f"✓ Created user: {username} / {password}")
        else:
            print(f"⚠ User already exists: {username}")
    
    print("\nSetup complete! Users are ready for testing.")

if __name__ == "__main__":
    create_test_users()