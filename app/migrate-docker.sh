# don`t run makemigrations in docker image
export MIGRATION_ALERT=1
python manage.py migrate
unset MIGRATION_ALERT