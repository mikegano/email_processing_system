# app/models/job.py

class Job:
    def __init__(self, title, company, location, url, workplace_type):
        self.title = title
        self.company = company
        self.location = location
        self.url = url
        self.workplace_type = workplace_type
        # Additional details
        self.description = None
        self.requirements = None
        # ... other fields

    def update_details(self, details):
        self.description = details.get('description', self.description)
        self.requirements = details.get('requirements', self.requirements)
        # Update other fields as needed
