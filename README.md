# SRE Bedrock Agent (PoC)

## Goal
If:-
- pod restarts > 5
- memory_ratio > 0.8

Then:
Scale deployment in EKS.

## Architecture
CloudWatch → Lambda → Bedrock → Lambda → EKS

## How to Test

Invoke orchestrator lambda:

{
  "restarts": 8,
  "memory_ratio": 0.92,
  "deployment": "abc-service",
  "namespace": "xyz"
}

Expected:
Scaling Lambda invoked.
