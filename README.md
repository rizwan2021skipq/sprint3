# Using CodePipeline with Multiple Stages to Deploy Lambda Function


## Description

The code performs the main function of creating a CodePipeline with two stages, one named Beta where unit and integration tests are performed and a production stage where after a manual approval our stack consisting of our lambda function is deployed. The stack performs the work of deploying two lambda functions  named health_web and log_lambda respectively:
* health_web finds latency and availability metrics, publishes them on CloudWatch and generates alarm whenever threshold is breached, while also publishing the details of alarm to a SNS topic. 
* log_lambda has been subscribed to the same SNS topic and it gets the details of the alarm from that topic and logs them into the DynamoDB table.

Additional features include rollback feature triggered by an alarm that gets into alert state whenever the duration of health_web lambda function fets more than the set threshold value. 
## Files in the Project

* infra_stack.py file defines the InfraStack and the Lambda functions to be used by the stack. CloudWatch metrics, alarms and SNS has been set up in this file. 
* pipeline_stack.py defines the complete code pipeline and its stages.
* infra_stage.py defines stage of pipeline and what it contains.
* unit_test.py contains unit tests.
* integ_test.py contains integration tests.
* mult_whp.py file contains definition of handler function named health_web used by Lambda function. Availability and latency of each website is found using functions defined in this file. 
* url_retriever.py file contains a function named url_list that is used to retrieve websites list from S3 bucket.
* constants.py file contains constants such as namespace names, metric names etc. used by the project. Threshold values for metrics have also been defined here.
* create_bucket_file.py can be used to create a S3 bucket to hold a file containing website list whose metrics need to be observed.
* create_table.py can be used to create a DynamoDB table that can store the SNS email alert data.
* create_topic_file.py file can be used to create a topic on SNS. 
* subscribe_topic_file.py can be used to subscribe to a topic on SNS. In our case, it is being used to subscribe a Lambda function to SNS topic using its ARN.
* cloud_watch.py defines CloudWatchMetrics class that defines a method to put metrics on CloudWatch.
* app.py defines the InfraStack to be used by the project.

## Setting up the Project

First step involves entering the sprint3 named directory:
```bash
$ cd sprint3/
```
Then you need to activate virtual environment:
```bash
$ source .venv/bin/activate
```
Install the libraries needed for the project to run by using the file named 'requirements.txt'. In order to do that you need to run the following CLI command:
```bash
$ pip install -r requirements.txt
```
This completes the process of setting up the project.

## Pushing Code to Github
First you need to set up remote repository, in our case it was this one [GitHub Repository](https://github.com/rizwan2021skipq/andromedaRepo_2021). Now you need to establish remote link with it using following commands at CLI:
```bash
$ git remote add pipo https://github.com/rizwan2021skipq/andromedaRepo_2021
```
To push your code to GitHub using the following commands:
```bash
$ git add . && git commit -m "message" && git push -u pipo main
```
## Deploying the Project

First you need to bootstrap using following CLI commands:

```bash
$ cdk bootstrap aws://315997497220/us-east-2 --cloudformation-execution-policies arn:aws:iam::aws:policy/AdministratorAccess --trust 315997497220 --qualifier rizwanaaa --toolkit-stack-name RizwanToolkit aws://315997497220/us-east-2
```
In the next step you need to deploy the CDK architecture using the following bash command:
```bash
$ cdk deploy PipelineStackRizwantw
```
After the pipeline has been successfully deployed you need to use the AWS Service CodePipeline to see the results.

## Verifying the Results

### CodePipeline 
Observe whether all stages are completed successfully. In optimum cases, all stages should be deployed successfully and you should be getting mails via SNS notifications when an alarm changes to alert state.


## Maintainer
Rizwan Amir, email: rizwan.s@skipq.org 