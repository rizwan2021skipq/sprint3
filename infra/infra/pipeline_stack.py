from aws_cdk import core
from aws_cdk import aws_codepipeline_actions as cpactions
from aws_cdk import pipelines
from infra.infra_stage import InfraStage

class PipelineStack(core.Stack):
    def __init__(self,scope:core.Construct, id:str, **kwargs):
        super().__init__(scope,id, **kwargs)
        
        source=pipelines.CodePipelineSource.git_hub(repo_string=, branch='main', authentication=core.SecretValue.secrets_manager('github/token/sprint3')
        , trigger=cpactions.GitHubTrigger.POLL)
        
        synth=pipelines.ShellStep('synth',input=source, commands=[],primary_output_directory=)
        
        pipeline=pipelines.CodePipeline(self,'Pipeline', synth=synth)
        
        beta=InfraStage(self, "Beta", env={
            
            'account':'',
            'region':''
        })
        
        beta=InfraStage(self, "Prod", env={
            
            'account':'',
            'region':''
        })