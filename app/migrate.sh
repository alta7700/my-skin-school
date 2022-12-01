export MIGRATION_ALERT=1
python manage.py makemigrations && python manage.py migrate
unset MIGRATION_ALERT