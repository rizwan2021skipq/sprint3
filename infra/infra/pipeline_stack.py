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
        
        cbRole = aws_iam.Role(self, "cb-role", 
            assumed_by=aws_iam.ServicePrincipal('codebuild.amazonaws.com'), 
            managed_policies=[  
                                # Adding Lamda Execution
                                aws_iam.ManagedPolicy.from_aws_managed_policy_name('service-role/AWSLambdaBasicExecutionRole'),
                                # Adding CloudWatch Full Access
                                aws_iam.ManagedPolicy.from_aws_managed_policy_name('CloudWatchFullAccess'),
                                # Adding S3 Full Access
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
        
        
        #role=cbRole
        project = codebuild.PipelineProject(self, "MyProject")
        
        source=pipelines.CodePipelineSource.git_hub(repo_string='rizwan2021skipq/sprint3', branch='main', authentication=core.SecretValue.secrets_manager('rizwan_github_token')
        , trigger=cpactions.GitHubTrigger.POLL)
        
        synth=pipelines.CodeBuildStep('synth_rizwan', input=source, commands=["cd infra", "pip install -r requirements.txt", "npm install -g aws-cdk"
        , "cdk synth"] ,primary_output_directory='infra/cdk.out', role= cbRole)
        #synth=pipelines.ShellStep('synth',input=source, commands=["cd infra", "pip install -r requirements.txt", "npm install -g aws-cdk"
        #, "cdk synth"],primary_output_directory='infra/cdk.out')
        
        pipeline=pipelines.CodePipeline(self,'CodePipelineRizwan', synth=synth)
        
        
        
        beta=InfraStage(self, "BetaRizwan", env={
            
            'account':'315997497220',
            'region':'us-east-2'
        })
        '''
        gamma=InfraStage(self, "GammaRizwan", env={
            
            'account':'315997497220',
            'region':'us-east-2'
        })
        
        prod=InfraStage(self, "ProductionRizwan", env={
            
            'account':'315997497220',
            'region':'us-east-2'
        })
        '''
        beta_stage=pipeline.add_stage(beta, post=[
        pipelines.ShellStep("Approve",
            # Use the contents of the 'integ' directory from the synth step as the input
            #input=synth.add_output_directory("integ"),
            commands=["cd infra", "pip install -r requirements.txt", "cd lambda_folder", "pytest unit_tests", "pytest integ_test"]
                            )
            ])
        
        #pipeline.add_stage(beta_stage,
        
         #                   )
        #beta_stage_preapproval= beta_stage.add_pre(ManualApprovalStep('beta_approval_rizwan'))
        
        #gamma_stage=pipeline.add_stage(gamma)
        #gamma_stage_preapproval= gamma_stage.add_pre(ManualApprovalStep(' gamma_approval_rizwan'))
        
        #production_stage=pipeline.add_stage(prod)
        #production_stage_preapproval= production_stage.add_pre(ManualApprovalStep('production_approval_rizwan'))
        
        # Create a role

    