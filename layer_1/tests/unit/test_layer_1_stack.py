import aws_cdk as core
import aws_cdk.assertions as assertions

from layer_1.layer_1_stack import Layer1Stack

# example tests. To run these tests, uncomment this file along with the example
# resource in layer_1/layer_1_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = Layer1Stack(app, "layer-1")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
