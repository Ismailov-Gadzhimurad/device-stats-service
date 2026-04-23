import random
from locust import HttpUser, task, between


class DeviceStatsUser(HttpUser):
    wait_time = between(1, 3)

    @task(3)
    def post_stats(self):
        device_id = random.randint(1, 100)
        payload = {
            "x": round(random.uniform(-100, 100), 2),
            "y": round(random.uniform(-100, 100), 2),
            "z": round(random.uniform(-100, 100), 2)
        }
        self.client.post(
            f"/api/v1/devices/{device_id}/stats",
            json=payload
        )

    @task(1)
    def get_analytics(self):
        device_id = random.randint(1, 100)
        self.client.get(
            f"/api/v1/devices/{device_id}/stats"
        )