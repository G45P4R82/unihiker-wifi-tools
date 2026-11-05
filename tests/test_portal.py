import os
import tempfile
import unittest

from wifi_tools.portal import TrainingPortal


class PortalTest(unittest.TestCase):
    def test_training_submission_does_not_store_password_field(self):
        with tempfile.TemporaryDirectory() as directory:
            portal = TrainingPortal(data_dir=directory)
            client = portal.app.test_client()
            response = client.post("/training", data={"campaign": "Test", "training_code": "DEMO"})
            self.assertEqual(response.status_code, 200)
            with open(os.path.join(directory, "events.jsonl")) as stream:
                content = stream.read()
            self.assertIn("DEMO", content)
            self.assertNotIn("password", content.lower())


if __name__ == "__main__":
    unittest.main()
