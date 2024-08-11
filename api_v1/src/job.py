import asyncio

class Job:
    STATUS_PENDING = 'pending'
    STATUS_RUNNING = 'running'
    STATUS_QUEUED = 'queued'
    STATUS_TERMINATED = 'terminated'

    def __init__(self, job_id, total_run_time):
        self.id = job_id
        self.total_run_time = total_run_time
        self.status = self.STATUS_PENDING
        self.node_id = None

    def assign_node(self, node_id):
        self.node_id = node_id
        self.status = self.STATUS_RUNNING

    def mark_as_queued(self):
        self.status = self.STATUS_QUEUED

    async def run(self, scheduler):
        print(f"Job {self.id} started running on Node {self.node_id}.")
        await asyncio.sleep(self.total_run_time)
        print(f"Job {self.id} finished running on Node {self.node_id}.")
        scheduler.complete_job(self.id)

    def to_dict(self):
        return {
            'id': self.id,
            'total_run_time': self.total_run_time,
            'status': self.status,
            'node_id': self.node_id
        }
