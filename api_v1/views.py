from aiohttp import web


async def get_nodes(request):
    scheduler = request.app['scheduler']
    nodes = scheduler.get_nodes()
    return web.json_response(nodes)


async def add_node(request):
    scheduler = request.app['scheduler']
    data = await request.json()
    node = scheduler.add_node(data)
    return web.json_response(node)


async def remove_node(request):
    scheduler = request.app['scheduler']
    node_id = request.match_info['node_id']
    success = scheduler.remove_node(node_id)
    return web.json_response({'success': success})


async def get_jobs(request):
    scheduler = request.app['scheduler']
    jobs = scheduler.get_jobs()
    return web.json_response(jobs)


async def submit_job(request):
    scheduler = request.app['scheduler']
    data = await request.json()
    try:
        job = scheduler.submit_job(data)
    except Exception as e:
        return web.json_response({'error': str(e)}, status=400)
    return web.json_response(job)


async def terminate_job(request):
    scheduler = request.app['scheduler']
    job_id = request.match_info['job_id']
    success = scheduler.terminate_job(job_id)
    return web.json_response({'success': success})



