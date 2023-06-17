#!/usr/bin/env python

from constructs import Construct
from cdktf import App, TerraformStack, TerraformOutput, CloudBackend, NamedCloudWorkspace
from cdktf_cdktf_provider_aws.provider import AwsProvider
from imports.vpc import Vpc

class ModuleStack(TerraformStack):
    def __init__(self, scope: Construct, id: str):
        super().__init__(scope, id)

        AwsProvider(self, "aws",
            region = "eu-west-3",
        )

        vpc = Vpc(self, "MyCdktfPythonVpc",
            name = "my-cdktf-python-vpc",
            cidr = "10.0.0.0/16",
            azs = ['eu-west-3a', 'eu-west-3b', 'eu-west-3c'],
            private_subnets = ['10.0.1.0/24', '10.0.2.0/24', '10.0.3.0/24'],
            public_subnets = ['10.0.101.0/24', '10.0.102.0/24', '10.0.103.0/24'],
            enable_nat_gateway = False
        )

        TerraformOutput(self, "vpc_cidr",
                        value=vpc.cidr,
                        )
        TerraformOutput(self, "public_subnet_arn",
                        value=vpc.public_subnet_arns_output
                        )
        

app = App()
network_stack = ModuleStack(app, "cdktf-python-vpc-module")

CloudBackend(network_stack,
  hostname='app.terraform.io',
  organization='hashikral',
  workspaces=NamedCloudWorkspace('cdktf-python-vpc')
)

app.synth()
