import json
import boto3
import os

bedrock = boto3.client("bedrock-runtime")
lambda_client = boto3.client("lambda")

MODEL_ID = os.environ.get("MODEL_ID")
SCALING_LAMBDA_NAME = os.environ.get("SCALING_LAMBDA_NAME")


def ask_bedrock(restarts, memory_ratio):
    prompt = f"""
You are an SRE decision engine.

If restarts > 5 AND memory_ratio > 0.8:
Return JSON: {{"action": "SCALE"}}

Otherwise:
Return JSON: {{"action": "NO_ACTION"}}

Respond ONLY in valid JSON.

Input:
restarts={restarts}
memory_ratio={memory_ratio}
"""

    body = {
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 100,
        "anthropic_version": "bedrock-2023-05-31"
    }

    response = bedrock.invoke_model(
        modelId=MODEL_ID,
        body=json.dumps(body)
    )

    result = json.loads(response["body"].read())
    output_text = result["content"][0]["text"]

    return json.loads(output_text)


def handler(event, context):

    # For PoC — can be replaced with CloudWatch query later
    restarts = event.get("restarts", 0)
    memory_ratio = event.get("memory_ratio", 0.0)
    deployment = event.get("deployment")
    namespace = event.get("namespace")

    decision = ask_bedrock(restarts, memory_ratio)

    if decision["action"] == "SCALE":

        lambda_client.invoke(
            FunctionName=SCALING_LAMBDA_NAME,
            InvocationType="Event",
            Payload=json.dumps({
                "deployment": deployment,
                "namespace": namespace,
                "replicas": 5
            })
        )

        return {
            "status": "scaled"
        }

    return {
        "status": "no_action"
    }
