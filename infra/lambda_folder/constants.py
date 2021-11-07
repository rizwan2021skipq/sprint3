'''
This file defines constants to be used in the project
'''
# Constant defining name of namespace for metrica and alarm
URL_MONITOR_NAMESPACE="URL_MONITOR_BY_RIZWAN"
# Constant defining name of availability metric
URL_MONITOR_METRIC_AVAILABILITY="WEBSITE_AVAILABLE?"
# Constant defining name of latency metric
URL_MONITOR_METRIC_LATENCY="WEBSITE_LATENCY"
# Constant defining threshold of availability for all websites
THRESHOLD_OF_AVAILABILITY=1
# Constant defining threshold of latency for all websites
THRESHOLD_OF_LATENCY=0.100
THRESHOLD_OF_DURATION=0.1E-3
THRESHOLD_OF_ERRORS=1
EMAIL="rizwan.s@skipq.org"
LAMBDA_ARN="arn:aws:lambda:us-east-2:315997497220:function:InfraStackRizwan-loggerlambda7BA3B318-XCPO1vGRhJD4"

TOPIC_ARN='arn:aws:sns:us-east-2:315997497220:alarms_testing'
TOPIC_NAME='alarms_testing'
BUCKET_NAME="rizwanbucket2021"
FILE_IN_BUCKET='website_data.json'
TABLE_NAME="NEWS"



