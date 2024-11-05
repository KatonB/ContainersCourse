#locust -f stress_tests.py --host=http://127.0.0.1:8000
from locust import HttpUser, task, between

class ShopAPITest(HttpUser):
    wait_time = between(1,3)

    @task(2)
    def create_item(self):
        item_data = {
            "name": "Test Item",
            "description": "Test description",
            "price": 9.99,
            "quantity": 100
        }
        self.client.post("/item/", json=item_data)

    @task(1)
    def read_item(self):
        self.client.get("/item/1")

    @task(3)
    def read_items(self):
        self.client.get("/item/")

    @task(2)
    def create_cart(self):
        response = self.client.post("/cart/")
        if response.status_code == 201:
            cart_id = response.json()["id"]
            self.add_item_to_cart(cart_id, 1)

    def add_item_to_cart(self, cart_id, item_id):
        cart_item_data = {"quantity": 1}
        self.client.post(f"/cart/{cart_id}/add/{item_id}", json=cart_item_data)
