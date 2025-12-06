import json
import os
import glob
from aws_cdk import (
    Stack,
    aws_iam as iam,
)
from constructs import Construct



class IAMStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, env_name: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)
        

        for team_config_file in glob.glob("stacks/policies/teams/*.json"):
            with open(team_config_file, 'r') as file:
                team_config = json.load(file)

            role_name = team_config["role_name"]
            actions = team_config.get(env_name, {}).get("actions", [])
            common_actions = team_config.get("common", {}).get("actions", [])
            
            merged_actions = common_actions + actions
            

            #TODO: Integrate with Azure AD and SAML
            role = iam.Role(
                self,
                f"{role_name}",
                role_name=f"{role_name}",
                assumed_by=iam.CompositePrincipal(
                    iam.AccountRootPrincipal()  # For testing, allow account root
                ),
                description=f"{role_name} for {env_name} environment"
            )
    
            if merged_actions:
                policy = iam.Policy(
                    self,
                    f"{role_name}-{env_name}-Policy",
                    policy_name=f"{role_name}-{env_name}-Policy",
                    statements=[
                        iam.PolicyStatement(
                            actions=merged_actions,
                            resources=["*"] # Temp
                        )
                    ]
                )
                policy.attach_to_role(role)