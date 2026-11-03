"""Local catalogue workload. Run only against the explicitly selected QA server."""

from locust import HttpUser, LoadTestShape, between, task


class CatalogueUser(HttpUser):
    wait_time = between(0.02, 0.05)

    @task(3)
    def browse_catalogue(self):
        with self.client.get(
            "/api/shop/products", name="catalogue", catch_response=True
        ) as response:
            if response.status_code == 200 and len(response.json()) == 3:
                response.success()
            else:
                response.failure("Invalid catalogue response")

    @task
    def search_catalogue(self):
        with self.client.get(
            "/api/shop/products?q=KEYBOARD", name="search", catch_response=True
        ) as response:
            if response.status_code == 200 and response.json()[0]["id"] == 1:
                response.success()
            else:
                response.failure("Invalid search response")


class SpikeShape(LoadTestShape):
    """Used only when LOCUST_SPIKE=1, otherwise CLI user count controls the run."""

    def tick(self):
        import os

        if os.getenv("LOCUST_SPIKE") != "1":
            return None
        elapsed = self.get_run_time()
        if elapsed < 3:
            return 10, 50
        if elapsed < 6:
            return 100, 100
        if elapsed < 9:
            return 10, 100
        return None


# Normal CLI runs must not auto-select the optional spike shape.
import os  # noqa: E402

if os.getenv("LOCUST_SPIKE") != "1":
    del SpikeShape
