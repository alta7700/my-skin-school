set MIGRATION_ALERT=1
python manage.py makemigrations && python manage.py migrate
set MIGRATION_ALERT=