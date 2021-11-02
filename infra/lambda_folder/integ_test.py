import pytest
import pytest
from aws_cdk import core
from infra import infra_stack
from infra_stack import InfraStackRizwan



def test_lambda():
        """
        Test that an available website is actually available
        """
        app=core.App()
        InfraStackRizwan(app, "testing_stack")
        template=app.synth().get_stack_by_name("testing_stack").template
        functions=[ resource for resource in template['Resources'].values() if resource['Type']=='AWS::Lambda::Function']
        
        assert len(functions)==2
 