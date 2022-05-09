data "aws_caller_identity" "current" {}

data "archive_file" "role-excutioner-lambda" {
  type        = "zip"
  source_dir  = "../src"
  output_path = "../src.zip"
}



resource "aws_lambda_function" "lambda-role-excutioner" {
  filename         = data.archive_file.role-excutioner-lambda.output_path
  function_name = "role-excutioner"
  role          = aws_iam_role.iam_for_lambda.arn
  handler       = "lambda_function.lambda_handler"
  source_code_hash = data.archive_file.role-excutioner-lambda.output_base64sha256
  timeout       = 900
  memory_size   = 1024
  runtime       = "python3.8"
  }

  
resource "aws_lambda_permission" "role-excutioner" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda-role-excutioner.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.role-excutioner.arn
}

resource "aws_iam_role" "iam_for_lambda" {
  name = "role-excutioner-lambda"
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "lambda_base_policy" {
  role       = aws_iam_role.iam_for_lambda.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# tfsec:ignore:aws-iam-no-policy-wildcards
resource "aws_iam_role_policy" "lambda_container" {
  name = "role-excutioner-lambda-policy"
  role = aws_iam_role.iam_for_lambda.id
  policy = jsonencode(
   {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "logs:CreateLogGroup",
            "Resource": "arn:aws:logs:ap-northeast-1:167343241558:*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": [
                "arn:aws:logs:ap-northeast-1:167343241558:log-group:/aws/lambda/nakano-role-excutioner:*"
            ]
        }
    ]
   }
  )
}
