from aws_cdk import core
from aws_cdk import aws_codepipeline_actions as cpactions
from aws_cdk import pipelines
from infra_stage import InfraStage

class PipelineStack(core.Stack):
    def __init__(self,scope:core.Construct, id:str, **kwargs):
        super().__init__(scope,id, **kwargs)
        
        source=pipelines.CodePipelineSource.git_hub(repo_string='rizwan2021skipq/sprint3', branch='main', authentication=core.SecretValue.secrets_manager('rizwan_github_token')
        , trigger=cpactions.GitHubTrigger.POLL)
        
        synth=pipelines.ShellStep('synth',input=source, commands=["cd infra", "pip install -r requirements.txt", "npm install -g aws-cdk"
        , "cdk synth"],primary_output_directory='infra/cdk.out')
        
        pipeline=pipelines.CodePipeline(self,'Pipeline', synth=synth)
        
        
        
        beta=InfraStage(self, "Beta", env={
            
            'account':'315997497220',
            'region':'us-east-2'
        })
        
        gamma=InfraStage(self, "Gamma", env={
            
            'account':'315997497220',
            'region':'us-east-2'
        })
        
        prod=InfraStage(self, "Production", env={
            
            'account':'315997497220',
            'region':'us-east-2'
        })
        
        beta_stage=pipeline.add_stage(beta)
        beta_stage_preapproval= beta_stage.add_pre(pipeline.ManualApprovalStep('beta_approval'))
        
        gamma_stage=pipeline.add_stage(gamma)
        gamma_stage_preapproval= gamma_stage.add_pre(pipeline.ManualApprovalStep(' gamma_approval'))
        
        production_stage=pipeline.add_stage(prod)
        production_stage_preapproval= production_stage.add_pre(pipeline.ManualApprovalStep('production_approval'))
        