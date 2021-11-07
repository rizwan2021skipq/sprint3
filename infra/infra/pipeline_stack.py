'''File defining PipelineStack '''

# Importing Libraries
from aws_cdk import core
from aws_cdk import aws_codepipeline_actions as cpactions
from aws_cdk import pipelines
from infra_stage import InfraStage
from aws_cdk.pipelines import ManualApprovalStep
from aws_cdk import aws_iam
from aws_cdk import aws_codebuild as codebuild
from aws_cdk import aws_iam


class PipelineStackRizwan(core.Stack):
    def __init__(self,scope:core.Construct, id:str, **kwargs):
        super().__init__(scope,id, **kwargs)
        
        # Defining roles for codebuild
        cbRole = aws_iam.Role(self, "cb-role", 
            assumed_by=aws_iam.ServicePrincipal('codebuild.amazonaws.com'), 
            managed_policies=[  
                                
                                aws_iam.ManagedPolicy.from_aws_managed_policy_name('service-role/AWSLambdaBasicExecutionRole'),
                                aws_iam.ManagedPolicy.from_aws_managed_policy_name('CloudWatchFullAccess'),
                                aws_iam.ManagedPolicy.from_aws_managed_policy_name('AmazonS3FullAccess'),
                                aws_iam.ManagedPolicy.from_aws_managed_policy_name('AmazonDynamoDBFullAccess'),
                                aws_iam.ManagedPolicy.from_aws_managed_policy_name('AWSCodePipeline_FullAccess'),
                                aws_iam.ManagedPolicy.from_aws_managed_policy_name('AWSCodeDeployFullAccess'),
                                aws_iam.ManagedPolicy.from_aws_managed_policy_name('AmazonSSMFullAccess'),
                                
                                
                                
                                
                                ])
                                
        
        cbRole.add_to_policy(aws_iam.PolicyStatement(
            resources=["*"],
            actions=["sts:AssumeRole"],
            
      
            ))
        cbRole.add_to_policy(aws_iam.PolicyStatement(
            resources=["*"],
            actions=['ssm:GetParameter']
            ))
        
        

        # Source Step
        source=pipelines.CodePipelineSource.git_hub(repo_string='rizwan2021skipq/sprint3', branch='main', authentication=core.SecretValue.secrets_manager('rizwan_github_token')
        , trigger=cpactions.GitHubTrigger.POLL)
        
        # Build Step
        synth=pipelines.CodeBuildStep('synth_rizwan', input=source, commands=["cd infra", "pip install -r requirements.txt", "npm install -g aws-cdk"
        , "cdk synth"] ,primary_output_directory='infra/cdk.out', role= cbRole)
        #synth=pipelines.ShellStep('synth',input=source, commands=["cd infra", "pip install -r requirements.txt", "npm install -g aws-cdk"
        #, "cdk synth"],primary_output_directory='infra/cdk.out')
        
        # Defining Pipeline for stages
        pipeline=pipelines.CodePipeline(self,'CodePipelineRizwan', synth=synth)
        
        
        # Defining Beta Stage
        beta=InfraStage(self, "BetaRizwan", env={
            
            'account':'315997497220',
            'region':'us-east-2'
        })
        
        
        # Defining Production Stage
        prod=InfraStage(self, "ProductionRizwan", env={
            
            'account':'315997497220',
            'region':'us-east-2'
        })
        
        #Adding Beta Stage to Pipeline
        beta_stage=pipeline.add_stage(beta, 
        post=[
        pipelines.CodeBuildStep('unittest_rizwan',  commands=["cd infra", "pip install -r requirements.txt"
        , "pytest infra/unit_test.py"] , role= cbRole)
            
            ])
        
        # Adding Pre step to Beta Stage    
        makestep=beta_stage.add_pre(pipelines.CodeBuildStep('making_things',  commands=["cd infra", "pip install -r requirements.txt", "python3 automate_bucket.py", "python3 automate_topic.py","python3 automate_table.py" ]
        , role= cbRole))
        
        # Adding Production Stage to pipeline
        prod_stage=pipeline.add_stage(prod)
        
        # Adding Manual Approval for Production Stage
        production_stage_preapproval= prod_stage.add_pre(ManualApprovalStep('production_approval_rizwan'))
        

    