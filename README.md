The project contains 2 CDK stacks

# **layer_0**

`layer_0` project contains the basic low level infra needed for all the teams and projects. Things like VPC, RDS, IAM role goes in it. Below are the resource created for this project

| Service              |    Region                 |
|----------------------|---------------------------|
| VPC                  | `ap-south-1`, `eu-west-1` |
| RDS writer instance  | `ap-south-1`              |
| RDS reader instance  | `eu-west-2`               |
| ECR repo             | `ap-south-1`, `eu-west-2` |
| ECS cluster          | `ap-south-1`, `eu-west-2` |
| NAT gateway          | `ap-south-1`, `eu-west-2` |
| Internet gateway     | `ap-south-1`, `eu-west-2` |
| IAM Roles            | `ap-south-1`, `eu-west-2` |

We will use `ap-south-1` as primary region and `eu-west-2` as secondary region. We can have as many secondary regions as we want by updating the `SECONDARY_REGIONS` list in `layer_0/app.py` file. Secondary regions will have a 1 read replica of the RDS instance. This projects will be usually managed by the core Cloud or DevOps team of the org.

# **layer_1**
This is a actual backend project but any other project which handles business logic by any other team will come under `layer_1`. When setting up new account or region we always first deploy `layer_0` infra before we start migrating all projects. Currently we have a simple `flask` API server. This project is respnosible for following things
- Create and packge docker image
- Push the image to ECR repo created by `layer_0` project
- Create ECS Task definition revision
- Create ECS service and ALB

The advantage of splitting infra between 2 projects is to give developer teams to have slight flexibility on their own infra. Moving the ECS service and definition logic to `layer_1` projects has following advantages
- Allows devs to create their custom `layer_1` infra
- They dont have to worry about setting up VPC and other low level stuff but only the things that their service might need
- They can update the task definition CPU and memory assignments without relying on SRE/Platform team
- Allowing them to have control over their load balancing strageties
- Allowing them to have control over the ECS Service deployment strageties
- Gives them more freedom to test and change the auto scaling strageties


# **Deployment strategy**
For stack deployment we will create a release/deployment role in each account. We will have a single user in our master account which has enough permissions to assume this role in each account for deployment. Since this is a very pervilige role assuming it makes the sessions short and we don't have to store credentials for long term. All the configs and sercrets will be stored in secret manager of whatever CI/CD service that we are using. Before moving to new region/account SRE/Cloud team will always make sure that the core `layer_0` infra is deploy on that account/region. After that its each teams responsibility to migrate their stacks/projects to the new region/account.