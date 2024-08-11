class Node:
    def __init__(self, node_id, max_jobs):
        self.id = node_id
        self.max_jobs = max_jobs
        self.jobs = []

    def can_accept_job(self):
        return len(self.jobs) < self.max_jobs

    def add_job(self, job_id):
        self.jobs.append(job_id)

    def remove_job(self, job_id):
        self.jobs.remove(job_id)

    def to_dict(self):
        return {
            'id': self.id,
            'max_jobs': self.max_jobs,
            'available_jobs': self.max_jobs - len(self.jobs)
        }
