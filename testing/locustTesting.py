from locust import HttpUser, TaskSet, task, between
import uuid
import json
import difflib
import colorama

class UserBehavior(TaskSet):

    def on_start(self):
        # Load the test file once during startup
        with open("/Users/varunchandrashekar/Downloads/BenchmarkingData/2-gather-process-analyze-data.png", "rb") as f:
            self.test_file = f.read()

    @task(1)
    def generate_template(self):
        # Simulate diagram upload
        unique_uuid = str(uuid.uuid4())
        files = {"ArchitectureDiagram": ("test_diagram.png", self.test_file, "image/png")}
        data = {"UUID": unique_uuid}
        response = self.client.post(
            "/generateawstemplate", 
            files=files,
            data=data
        )
        if response.status_code == 200:
            # Extract UUID from the response
            image_uuid = response.json().get("image_id")
            if image_uuid:
                # Simulate polling the result endpoint
                self.get_result(image_uuid)

    def get_template(self, response):
        valid_file_obj = json.loads(response)
        result_obj = json.loads(valid_file_obj["result"])
        valid_template = json.dumps(result_obj["template"])

        return valid_template

    def validate_template(self, template, uuid):
        with open("testingLocustTemplate.json", "r") as valid_file:
            #valid_file.read().replace("\\\\", "\\")
            valid_template = self.get_template(valid_file.read())
            new_template = self.get_template(template)

            if(valid_template == new_template):
                print("VALID", uuid)
            else:
                print("INVALID", uuid)

    def get_result(self, image_uuid):
        while True:  # Retry up to 10 times
            response = self.client.get(f"/result/?uuid={image_uuid}")
            if response.status_code == 200 and "result" in response.text:
                self.validate_template(response.text, image_uuid)
                break  # Template is ready
            self.wait_time()

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 5)  # Random wait between 1 and 5 seconds
