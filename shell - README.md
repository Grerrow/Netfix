useful shell commands for testing:
----------------------------------

from users.models import User, Customer, Company


user = User.objects.create(username="testuser", email="test@example.com", is_company=True)
user.set_password("testpassword")
user.save()
user.is_active = True

user = User.objects.get(username="testuser") (for a new instance of this object/user every time i open shell)

company = Company.objects.create(user=user, field="Electricity")
Company.objects.all()

==================================================================================================================
checks:
    user.id
    User.objects.filter(email="test@example.com").exists()
    User.objects.all()
    print(user.is_active)

    all_usernames = User.objects.values_list('username', flat=True)
    print(list(username))

==================================================================================================================
Login:
    user = authenticate(username="testuser", password="testpassword")
print(user)

==================================================================================================================
delete:
    user = User.objects.get(username='testuser')
    user = User.objects.get(id=1)
    user.delete()

    User.objects.get(username="admin").delete() => delete the admin

    User.objects.all().delete()

==================================================================================================================
reset DB pk:
    go to c:/Program Files/SQLite and rename "sqlite3_disabled.exe" back to "sqlite3.exe"
    python manage.py dbshell
    DELETE FROM sqlite_sequence WHERE name='users_user';