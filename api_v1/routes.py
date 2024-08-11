from api_v1 import views


def setup_routes(app):
    app.router.add_get('/nodes', views.get_nodes)
    app.router.add_post('/nodes', views.add_node)
    app.router.add_delete('/nodes/{node_id}', views.remove_node)

    app.router.add_get('/jobs', views.get_jobs)
    app.router.add_post('/jobs', views.submit_job)
    app.router.add_delete('/jobs/{job_id}', views.terminate_job)
