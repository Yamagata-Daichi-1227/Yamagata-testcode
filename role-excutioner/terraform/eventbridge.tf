resource "aws_cloudwatch_event_rule" "role-excutioner" {
  name        = "role-excutioner"
  description = "Capture SecurityHub Findings Import Event"

  event_pattern = jsonencode({
    "source" : ["aws.securityhub"],
    "detail-type" : ["Security Hub Findings - Imported"],
    "detail" : {
      "findings" : {
        "Compliance" : {
          "Status" : ["FAILED"]
        }
      }
    }
  })
}

resource "aws_cloudwatch_event_target" "role-excutioner" {
  rule = aws_cloudwatch_event_rule.role-excutioner.name
  arn  = aws_lambda_function.lambda-role-excutioner.arn
}
