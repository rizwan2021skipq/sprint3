''' This file contains unit tests'''

import pytest
from aws_cdk import core
from infra.infra_stack import InfraStackRizwan


# This test checks whether we have two lambda functions
def test_lambda():
        """
        Test that an available website is actually available
        """
        app=core.App()
        InfraStackRizwan(app, "testingstack")
        template=app.synth().get_stack_by_name("testingstack").template
        functions=[ resource for resource in template['Resources'].values() if resource['Type']=='AWS::Lambda::Function']
        
        assert len(functions)==3
 