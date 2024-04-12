from celery import shared_task

# [tasks]
#  . mysite.celery.debug_task
#  . news.tasks.bar
@shared_task
def bar():
    return "Hello World"