# stacks/simple_ecs_service_stack.py
from aws_cdk import (
    Stack,
    aws_ecs as ecs,
    aws_ec2 as ec2,
    aws_elasticloadbalancingv2 as elbv2,
    aws_ecr as ecr,
    Duration
)
from constructs import Construct


class ECSServiceStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, vpc_name, cluster_name, ecr_repo_name: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        vpc = ec2.Vpc.from_lookup(
            self,
            "VPC",
            vpc_name=vpc_name
        )

        cluster = ecs.Cluster.from_cluster_attributes(
            self,
            "ECSCluster",
            cluster_name=cluster_name,
            vpc=vpc
        )

        ecr_repo = ecr.Repository.from_repository_name(
            self,
            "ECRRepo",
            repository_name=ecr_repo_name
        )
        
        task_definition = ecs.FargateTaskDefinition(
            self,
            "TaskDef",
            memory_limit_mib=512,
            cpu=256
        )
        
        container = task_definition.add_container(
            "AppContainer",
            image=ecs.ContainerImage.from_ecr_repository(ecr_repo, tag="stable"),
            port_mappings=[
                ecs.PortMapping(container_port=8080)
            ]
        )
        
        alb_sg = ec2.SecurityGroup(
            self,
            "ALBSG",
            vpc=vpc,
            allow_all_outbound=True
        )

        alb_sg.add_ingress_rule(
            ec2.Peer.any_ipv4(),
            ec2.Port.tcp(80),
            "Allow HTTP"
        )
        
        alb = elbv2.ApplicationLoadBalancer(
            self,
            "ALB",
            vpc=vpc,
            internet_facing=True,
            security_group=alb_sg
        )
        
        service_sg = ec2.SecurityGroup(
            self,
            "ServiceSG",
            vpc=vpc,
            allow_all_outbound=True
        )
        service_sg.add_ingress_rule(
            alb_sg,
            ec2.Port.tcp(8080),
            "Allow from ALB"
        )
        
        service = ecs.FargateService(
            self,
            "Service",
            cluster=cluster,
            task_definition=task_definition,
            desired_count=2,
            security_groups=[service_sg],
            assign_public_ip=True
        )
        
        scaling = service.auto_scale_task_count(
            min_capacity=2,
            max_capacity=10
        )
        
        scaling.scale_on_cpu_utilization(
            "CpuScaling",
            target_utilization_percent=60,
            scale_in_cooldown=Duration.seconds(60),
            scale_out_cooldown=Duration.seconds(30),
        )

        target_group = elbv2.ApplicationTargetGroup(
            self,
            "TargetGroup",
            vpc=vpc,
            port=8080,
            protocol=elbv2.ApplicationProtocol.HTTP,
            target_type=elbv2.TargetType.IP,
            health_check=elbv2.HealthCheck(
                path="/",
                interval=Duration.seconds(30)
            )
        )
    
        listener = alb.add_listener(
            "Listener",
            port=80,
            default_action=elbv2.ListenerAction.forward([target_group])
        )
    
        service.attach_to_application_target_group(target_group)
    
        self.alb_dns = alb.load_balancer_dns_name