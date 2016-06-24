from django.test import TestCase

# Create your tests here.




task_sample = {
    'id': '#1234',
    'module' :'cmd',
    'action' :'execute',
    'data'   :"json data",
    'callback_queue':'#1234-callback',
    "callback": 'save_log_to_db',
    'host_ids':"[1,2,5,6,9]"
}


raw_task_sample = {
    'module' :'cmd',
    'action' :'execute',
    'data'   :"json data",
    'host_ids':"[1,2,5,6,9]"
}


