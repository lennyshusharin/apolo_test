import pytest
from api_v1.main import init_app


@pytest.fixture
async def client(aiohttp_client):
    app = init_app()
    return await aiohttp_client(app)


@pytest.mark.asyncio
async def test_get_nodes(client):
    response = await client.get('/nodes')
    assert response.status == 200
    nodes = await response.json()
    assert isinstance(nodes, list)


@pytest.mark.asyncio
async def test_add_node(client):
    node_data = {
        'max_jobs': 5
    }
    response = await client.post('/nodes', json=node_data)
    assert response.status == 200
    node = await response.json()
    assert 'id' in node
    assert node['max_jobs'] == 5
    assert node['available_jobs'] == 5


@pytest.mark.asyncio
async def test_remove_node(client):
    node_data = {'max_jobs': 3}
    response = await client.post('/nodes', json=node_data)
    node = await response.json()
    response = await client.delete(f'/nodes/{node["id"]}')
    assert response.status == 200
    result = await response.json()
    assert result['success'] is True


@pytest.mark.asyncio
async def test_submit_job(client):
    node_data = {'max_jobs': 2}
    response = await client.post('/nodes', json=node_data)
    node = await response.json()

    job_data = {
        'total_run_time': 2
    }
    response = await client.post('/jobs', json=job_data)
    assert response.status == 200
    job = await response.json()
    assert 'id' in job
    assert job['status'] in ['running', 'queued']
    assert job['node_id'] == node['id']

@pytest.mark.asyncio
async def test_submit_job_no_node(client):
    job_data = {
        'total_run_time': 2
    }
    response = await client.post('/jobs', json=job_data)
    assert response.status == 400
    result = await response.json()
    assert result['error'] == 'No nodes available'

@pytest.mark.asyncio
async def test_submit_job_no_capacity(client):
    node_data = {'max_jobs': 0}
    response = await client.post('/nodes', json=node_data)
    node = await response.json()

    job_data = {
        'total_run_time': 2
    }
    response = await client.post('/jobs', json=job_data)
    assert response.status == 400
    result = await response.json()
    assert result['error'] == 'No nodes available'

@pytest.mark.asyncio
async def test_submit_multiple_jobs(client):
    node_data = {'max_jobs': 2}
    response = await client.post('/nodes', json=node_data)
    node = await response.json()

    job_data = {
        'total_run_time': 2
    }
    response = await client.post('/jobs', json=job_data)
    job1 = await response.json()

    response = await client.post('/jobs', json=job_data)
    job2 = await response.json()

    assert job1['status'] in ['running', 'queued']
    assert job2['status'] in ['running', 'queued']
    assert job1['node_id'] == node['id']
    assert job2['node_id'] == node['id']
    assert job1['id'] != job2['id']

    response = await client.get('/nodes')
    nodes = await response.json()
    assert len(nodes) == 1
    assert nodes[0]['available_jobs'] == 0


@pytest.mark.asyncio
async def test_job_balancing_between_nodes(client):
    node_data = {'max_jobs': 1}
    response = await client.post('/nodes', json=node_data)
    node1 = await response.json()

    node_data = {'max_jobs': 1}
    response = await client.post('/nodes', json=node_data)
    node2 = await response.json()

    job_data = {
        'total_run_time': 2
    }
    response = await client.post('/jobs', json=job_data)
    job1 = await response.json()

    response = await client.post('/jobs', json=job_data)
    job2 = await response.json()

    assert job1['status'] in ['running', 'queued']
    assert job2['status'] in ['running', 'queued']
    assert job1['node_id'] != job2['node_id']

    response = await client.get('/nodes')
    nodes = await response.json()
    assert len(nodes) == 2
    assert nodes[0]['available_jobs'] == 0
    assert nodes[1]['available_jobs'] == 0

@pytest.mark.asyncio
async def test_get_jobs(client):
    response = await client.get('/jobs')
    assert response.status == 200
    jobs = await response.json()
    assert isinstance(jobs, list)


@pytest.mark.asyncio
async def test_terminate_job(client):
    node_data = {'max_jobs': 1}
    response = await client.post('/nodes', json=node_data)
    node = await response.json()
    job_data = {'total_run_time': 2}
    response = await client.post('/jobs', json=job_data)
    job = await response.json()
    response = await client.delete(f'/jobs/{job["id"]}')
    assert response.status == 200
    result = await response.json()
    assert result['success'] is True
