from locust import task, FastHttpUser, between
from locust import run_single_user
from insert_product import login


class AddToCart(FastHttpUser):
    host = "http://localhost:5000"
    
    # Default headers for all requests
    default_headers = {
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "DNT": "1",
        "Sec-GPC": "1",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
    }

    # Adding wait time between tasks to simulate real user behavior
    wait_time = between(1, 3)

    def on_start(self):
        """This method will be executed before any tasks are executed."""
        self.username = "test123"
        self.password = "test123"
        
        # Call the login function and retrieve the token
        cookies = login(self.username, self.password)
        
        # Ensure token is available
        if cookies:
            self.token = cookies.get("token")
        else:
            self.token = None
            print("Failed to log in, token not received.")

    @task
    def add_product_to_cart(self):
        if self.token:
            response = self.client.get(
                "/cart",
                headers={
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8",
                    "Cookie": f"token={self.token}",
                    "Host": "localhost:5000",
                    "Priority": "u=0, i",
                    "Referer": "http://localhost:5000/product/1",
                    "Sec-Fetch-Dest": "document",
                    "Sec-Fetch-Mode": "navigate",
                    "Sec-Fetch-Site": "same-origin",
                    "Sec-Fetch-User": "?1",
                    "Upgrade-Insecure-Requests": "1",
                },
            )
            
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Failed to add product to cart, status code: {response.status_code}")
        else:
            print("No token available, cannot proceed with the request.")

if __name__ == "__main__":
    run_single_user(AddToCart)
