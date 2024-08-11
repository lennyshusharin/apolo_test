import uuid
import asyncio
from .node import Node
from .job import Job


class Scheduler:
    def __init__(self):
        self.nodes = {}
        self.jobs = {}

    def get_nodes(self):
        return [node.to_dict() for node in self.nodes.values()]

    def add_node(self, data):
        node_id = str(uuid.uuid4())
        node = Node(node_id, data['max_jobs'])
        self.nodes[node_id] = node
        return node.to_dict()

    def remove_node(self, node_id):
        if node_id in self.nodes:
            node = self.nodes.pop(node_id)
            for job_id in node.jobs:
                job = self.jobs[job_id]
                self.submit_job(job.to_dict())
            return True
        return False

    def get_jobs(self):
        return [job.to_dict() for job in self.jobs.values()]

    def submit_job(self, data):
        job_id = str(uuid.uuid4())
        job = Job(job_id, data['total_run_time'])
        for node in self.nodes.values():
            if node.can_accept_job():
                node.add_job(job_id)
                job.assign_node(node.id)
                self.jobs[job_id] = job
                asyncio.create_task(job.run(self))
                break
        else:
            raise Exception("No nodes available")
        return job.to_dict()

    def terminate_job(self, job_id):
        if job_id in self.jobs:
            job = self.jobs.pop(job_id)
            if job.node_id:
                node = self.nodes[job.node_id]
                node.remove_job(job_id)
            job.status = Job.STATUS_TERMINATED
            return True
        return False

    def complete_job(self, job_id):
        if job_id in self.jobs:
            job = self.jobs.pop(job_id)
            if job.node_id:
                node = self.nodes[job.node_id]
                node.remove_job(job_id)
            job.status = Job.STATUS_TERMINATED
            print(f"Job {job_id} completed and removed from scheduler.")



