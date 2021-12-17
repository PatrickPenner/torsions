rm redis.log # this is the log file redis uses on startup before it switches to redis/redis.log
rm redis/redis.log
rm celery/log/*.log
rm gunicorn/*.log

