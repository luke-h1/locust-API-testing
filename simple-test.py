from locust import HttpUser, SequentialTaskSet, TaskSet, task, between, events, constant 
import logging 
import sys
import os 
import time 
from dotenv import load_dotenv

# 60 minute test 
# pipenv run locust -f simple-test.py --headless --html simple-test.html --spawn-rate 5 -u 90 --run-time 60m 


class UserBehaviour(TaskSet):
    def __init__(self, parent):
        super().__init__(parent)
    @task(20)

    class make_api_request(SequentialTaskSet):
        @task()
        def make_first_api_request(self): 
            # replace with the endpoint you want to hit 
            # in this example I'm testing a weather API 
            self.client.get('/api/weather/sheffield')


class MyUser(HttpUser):
    wait_time=between(0, 20)
    tasks=[UserBehaviour]
    load_dotenv(verbose=True)
    api_url = os.getenv('API_URL')
    assert api_url is not None
    host=f'{api_url}'