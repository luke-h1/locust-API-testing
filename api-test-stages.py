from locust import HttpUser, SequentialTaskSet, TaskSet, task, between, events, constant
from locust import LoadTestShape 
import logging 
import sys
import os 
import time 
from dotenv import load_dotenv

# 60 minute test with a custom load shape that ramps up and down 
# pipenv run locust -f api-test-stages.py --headless --html simple-test.html --run-time 60m 


class UserTasks(TaskSet):
    def __init__(self, parent):
        super().__init__(parent)
    @task(20)

    class make_api_request(SequentialTaskSet):
        @task()
        def make_first_api_request(self): 
            # replace with the endpoint you want to hit 
            # in this example I'm testing a weather API 
            self.client.get('/api/weather/sheffield')


class customLoadShape(LoadTestShape):
    stages = [
        { "duration": 600, "users": 10, "spawn_rate": 10 },
        { "duration": 300, "users": 50, "spawn_rate": 10 },
        { "duration": 700, "users": 100, "spawn_rate": 50 },
        { "duration": 800, "users": 30, "spawn_rate": 10 },
        { "duration": 600, "users": 10, "spawn_rate": 10 },
        { "duration": 600, "users": 1, "spawn_rate": 1 },
    ]

    def tick(self): 
        run_time = self.get_run_time()
        for stage in self.stages:
            if run_time < stage['duration']:
                tick_data = (stage['users'], stage['spawn_rate'])
                return tick_data

        return None  


class MyUser(HttpUser):
    wait_time=between(0, 20)
    tasks=[UserTasks]
    load_dotenv(verbose=True)
    api_url = os.getenv('API_URL')
    assert api_url is not None
    host=f'{api_url}'