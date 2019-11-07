import os
import json
import boto3
 
def lambda_handler(event, context):
    message_unicode = event['Records'][0]['Sns']['Message']
    print(message_unicode)
    id = message_unicode.strip('{ "').strip('"}')
    print(id)

    unauthorized_ipv4 = os.environ['unauthorized_ipv4']
    authorized_global_ipv4 = os.environ['global_ipv4']

    describe_sg_all = boto3.client('ec2')
    handle_sg_all = boto3.resource('ec2')
    describe_sg = describe_sg_all.describe_security_groups(GroupIds=[id])
    handle_sg = handle_sg_all.SecurityGroup(id)
    
    print(describe_sg)
    
    for i in describe_sg['SecurityGroups']:
        print("Security Group Name: "+i['GroupName'])
        print("The Ingress rules are as follows: ")
        for j in i['IpPermissions']:
            print("IP Protocol: "+j['IpProtocol'])
            try:
                print("FromPORT: "+str(j['FromPort']))
                print("ToPORT: "+str(j['ToPort']))

                for k in j['IpRanges']:
                    print("IP Ranges: "+k['CidrIp'])

                    if k['CidrIp'] == unauthorized_ipv4 :
                        authorize_response = handle_sg.authorize_ingress(
                                    IpPermissions=[
                                        {
                                            'FromPort': int(j['FromPort']),
                                            'IpProtocol': j['IpProtocol'],
                                            'ToPort': int(j['ToPort']),
                                            'IpRanges': [
                                                {
                                                    'CidrIp': authorized_global_ipv4
                                                }
                                            ]
                                        }
                                    ]
                        )
                        revoke_response = handle_sg.revoke_ingress(
                                    IpPermissions=[
                                        {
                                            'FromPort': int(j['FromPort']),
                                            'IpProtocol': j['IpProtocol'],
                                            'ToPort': int(j['ToPort']),
                                            'IpRanges': [
                                                {
                                                    'CidrIp': unauthorized_ipv4
                                                }
                                            ]
                                        }
                                    ]
                        )
                        print("Security Group Changed")
                    else:
                        print("No Security Group Changed")
            except Exception as e:
                    print(e.args)
                    print("No value for ports and ip ranges available for this security group")
                    continue
        return 'end'