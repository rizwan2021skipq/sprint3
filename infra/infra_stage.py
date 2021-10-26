from aws_cdk import core as cdk
#from infra.infra.infra_stack import InfraStack
from infra_stack import InfraStackRizwan

class InfraStage(cdk.Stage):
    def __init__(self,scope:cdk.Construct, construct_id:str, **kwargs)->None:
        super().__init__(scope, construct_id, **kwargs)
        
        infra_stack=InfraStackRizwan(self,'infrastack')