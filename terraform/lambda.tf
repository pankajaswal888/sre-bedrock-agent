resource "aws_lambda_function" "scaling_lambda" {
  function_name = "sre-scaling-lambda"
  role          = aws_iam_role.orchestrator_role.arn
  package_type  = "Image"
  image_uri     = "YOUR_ECR_IMAGE_URI"
}

resource "aws_lambda_function" "orchestrator_lambda" {
  function_name = "sre-orchestrator-lambda"
  role          = aws_iam_role.orchestrator_role.arn
  package_type  = "Image"
  image_uri     = "YOUR_ECR_IMAGE_URI"

  environment {
    variables = {
      MODEL_ID = var.model_id
      SCALING_LAMBDA_NAME = aws_lambda_function.scaling_lambda.function_name
    }
  }
}
