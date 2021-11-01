''' this file defines the InfraStack'''
from aws_cdk import core as cdk

# For consistency with other languages, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.

# Importing the required libraries
from aws_cdk import core
from aws_cdk import aws_lambda_event_sources
#from aws_cdk.aws_lambda_event_sources import SnsEventSource
from aws_cdk import aws_dynamodb as dynamodb
from aws_cdk import aws_lambda as lambda_
from aws_cdk import aws_events
from aws_cdk import aws_events_targets
from aws_cdk import aws_iam
from aws_cdk import aws_cloudwatch as cloudwatch
from aws_cdk import aws_sns
from aws_cdk import aws_cloudwatch_actions

# Import files to be used
from lambda_folder import constants
from lambda_folder import url_retriever

class InfraStackRizwan(cdk.Stack):
    # InfraStackRizwan constructor
    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        role  = self.create_lambda_role()
        
        # The code that defines your stack goes here
        # Creating  the lambda function below, function has been named firstlambda, and its handler function named health_web
        # is available in file named mult_whp
        web_health_lambda = self.create_lambda('firstlambda', './lambda_folder','mult_whp.health_web',role)
        logger_lambda = self.create_lambda('loggerlambda', './lambda_folder','mult_whp.log_lambda',role)
        # Defining schedule to run Lambda function periodically
        lambda_schedule=aws_events.Schedule.rate(core.Duration.minutes(5))
        # Defining which event will occur periodically, in our case Lambda function will be called periodically
        event_lambda_target=aws_events_targets.LambdaFunction(handler=web_health_lambda)
        # Combining the schedule and target 
        lambda_run_rule=aws_events.Rule(self,"web_health_lambdarule", description="Periodic_lambda",schedule=lambda_schedule, targets=[event_lambda_target])
        # Getting list of websites to monitor from a S3 bucket, the function to retrieve the list from bucket has been defined
        # in a file named bucket_challenge
        URLS=url_retriever.url_list()
        #URLS= ["https://www.skipq.org", "https://www.espn.com.au/", "https://www.bbc.com/news", "https://shaukatkhanum.org.pk/"]
        # ARN of topic named alarms_testing, this topic will publish alarms and mail them to subscribers
        topic_arn=constants.TOPIC_ARN
        # Retreiving the topic "alarms_testing" from list of topics
        topic=aws_sns.Topic.from_topic_arn(self, id="main alarm_topic", topic_arn=topic_arn)
        
        #table = dynamodb.Table(self, id="Rizwan_Table",  table_name="logging_table_rizwan",   partition_key = dynamodb.Attribute(name="id", type=dynamodb.AttributeType.STRING))    
        
        event_source=logger_lambda.add_event_source(aws_lambda_event_sources.SnsEventSource(topic))
        
        
        
        for i in URLS:
            # Defining dimensions of metrics
            dimensions={'website name':i}
	        # Defining availability metric
            #availability_metric=cloudwatch.Metric( metric_name=constants.URL_MONITOR_METRIC_AVAILABILITY, namespace=constants.URL_MONITOR_NAMESPACE, dimensions=dimensions, label='pip_Availability_metric_of _{}'.format(i))
            # Defining latency metric
            #latency_metric=cloudwatch.Metric( metric_name=constants.URL_MONITOR_METRIC_LATENCY, namespace=constants.URL_MONITOR_NAMESPACE, dimensions=dimensions, label='pip_Latency_metric_of_{}'.format(i))
            
            availability_metric=cloudwatch.Metric( metric_name=constants.URL_MONITOR_METRIC_AVAILABILITY, namespace=constants.URL_MONITOR_NAMESPACE, dimensions=dimensions)
            # Defining latency metric
            latency_metric=cloudwatch.Metric( metric_name=constants.URL_MONITOR_METRIC_LATENCY, namespace=constants.URL_MONITOR_NAMESPACE, dimensions=dimensions)

            # Defining latency metric
            alarm_latency=cloudwatch.Alarm(self, metric=latency_metric, id='URL_MONITOR_METRIC_LATENCY_ALARM_{}'.format(i), treat_missing_data=cloudwatch.TreatMissingData.BREACHING
            , evaluation_periods=1, threshold=constants.THRESHOLD_OF_LATENCY,  comparison_operator=cloudwatch.ComparisonOperator.GREATER_THAN_THRESHOLD, datapoints_to_alarm=1)
            
            # Defining availability alarm
            alarm_availability=cloudwatch.Alarm(self, metric= availability_metric,  id='URL_MONITOR_METRIC_AVAILABILITY_ALARM_{}'.format(i), treat_missing_data=cloudwatch.TreatMissingData.BREACHING
            , evaluation_periods=1, threshold=constants.THRESHOLD_OF_AVAILABILITY, comparison_operator=cloudwatch.ComparisonOperator.LESS_THAN_THRESHOLD, datapoints_to_alarm=1)
            
            #alarm_latency=cloudwatch.Alarm(self, metric=latency_metric, id='URL_MONITOR_METRIC_LATENCY_ALARM_{}'.format(i), treat_missing_data=cloudwatch.TreatMissingData.BREACHING
            #, evaluation_periods=1, threshold=constants.THRESHOLD_OF_LATENCY, alarm_name='Pipelined_Latency_Alarm_of__{}'.format(i), comparison_operator=cloudwatch.ComparisonOperator.GREATER_THAN_THRESHOLD, datapoints_to_alarm=1)
            
            # Defining availability alarm
            #alarm_availability=cloudwatch.Alarm(self, metric= availability_metric,  id='URL_MONITOR_METRIC_AVAILABILITY_ALARM_{}'.format(i), treat_missing_data=cloudwatch.TreatMissingData.BREACHING
            #, evaluation_periods=1, threshold=constants.THRESHOLD_OF_AVAILABILITY,alarm_name='Pipelined_Availability_Alarm_of__{}'.format(i), comparison_operator=cloudwatch.ComparisonOperator.LESS_THAN_THRESHOLD, datapoints_to_alarm=1)
            
            # Defining latency alarm
            alarm_latency.add_alarm_action(aws_cloudwatch_actions.SnsAction(topic))
            # Defining availability alarm
            alarm_availability.add_alarm_action(aws_cloudwatch_actions.SnsAction(topic))
            
            
            
            
    # A function to create lambda function
    def create_lambda(self, id, asset, handler, role):
        
        # Returning lambda function 
        return lambda_.Function(self, id,
        code=lambda_.Code.asset(asset),
        handler=handler, timeout=core.Duration.seconds(100),
        runtime=lambda_.Runtime.PYTHON_3_6, role=role)
    
    # A function to create lambda role    
    def create_lambda_role(self):
        # Create a role
        lambdaRole = aws_iam.Role(self, "lambda-role", 
            assumed_by=aws_iam.ServicePrincipal('lambda.amazonaws.com'), 
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
                                aws_iam.ManagedPolicy.from_aws_managed_policy_name('AdministratorAccess')
                                
                                
                                ])
        
        return lambdaRole
        
    
    
    
    