# What can we do whit this
replace aws's security group unauthorized ports  

It's a AWS's lambda function to help management your security groups.  
If there are ports which ingress 0.0.0.0/0, this function will replace it to your authorized ip, you know full automatic.

# How to use it
- enable AWS's config to monitoring EC2 resources
- add a AWS's config rule which names __VPC_SG_OPEN_ONLY_TO_AUTHORIZED_PORTS__ , it will evaluates your AWS resources(in there, Security Group)
- create a remediation action names __PublishSNSNotification__
- add s SNS topic to receive the notification

# Create your own lambda function
code likes this repo.

# Trigger it
set a SNS trigger to the lambda function you created before.   
Absolutely, the topic is what you created before too.

# Set environment variables
set a Environment variables to replace the 0.0.0.0/0 stuff.  
like,  
__authorized_global_ipv4__  8.8.8.8/32


