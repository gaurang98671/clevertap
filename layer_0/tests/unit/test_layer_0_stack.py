import aws_cdk as core
import aws_cdk.assertions as assertions

from layer_0.layer_0_stack import Layer0Stack

# example tests. To run these tests, uncomment this file along with the example
# resource in layer_0/layer_0_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = Layer0Stack(app, "layer-0")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
