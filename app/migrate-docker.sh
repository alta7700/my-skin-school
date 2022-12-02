# don`t run makemigrations in docker image
export MIGRATION_ALERT=1
python manage.py migrate && python manage.py collectstatic --noinput
unset MIGRATION_ALERT