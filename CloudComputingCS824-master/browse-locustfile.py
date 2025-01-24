from locust import task, FastHttpUser, between
from locust import run_single_user


class BrowseUser(FastHttpUser):
    host = "http://localhost:5000"
    
    # Default headers for all requests (can be adjusted for specific tasks)
    default_headers = {
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "DNT": "1",
        "Sec-GPC": "1",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
    }

    # Use the `between` function to add some delay between requests
    wait_time = between(1, 3)  # wait between 1 to 3 seconds between tasks

    # Task to perform a GET request to the /browse endpoint
    @task
    def browse_page(self):
        response = self.client.get(
            "/browse",
            headers={
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8",
                "Host": "localhost:5000",
                "Priority": "u=0, i",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "cross-site",
                "Upgrade-Insecure-Requests": "1",
            },
        )
        
        # Validate the response (Check if the status code is 200)
        if response.status_code != 200:
            response.failure(f"Failed to load /browse, status code: {response.status_code}")
        else:
            response.success()

if __name__ == "__main__":
    run_single_user(BrowseUser)
