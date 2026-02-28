import json
import os
from kubernetes import client, config

def handler(event, context):

    deployment_name = event["deployment"]
    namespace = event["namespace"]
    replicas = event["replicas"]

    # Load EKS cluster config (using IAM auth)
    config.load_kube_config()

    apps = client.AppsV1Api()

    body = {
        "spec": {
            "replicas": replicas
        }
    }

    apps.patch_namespaced_deployment(
        name=deployment_name,
        namespace=namespace,
        body=body
    )

    return {
        "status": "deployment_scaled",
        "deployment": deployment_name,
        "replicas": replicas
    }
