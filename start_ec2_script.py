import boto3
import os

session = boto3.Session(
        aws_access_key_id = os.environ['access_key_id'],
        aws_secret_access_key = os.environ['secret_access_key'])

regions = ["us-east-1","sa-east-1"]

instances_start = []
instancesAlreadStart = []

def lambda_handler(event, context):
    for region in regions:
        print(region+"\n")
        ec2 = session.client('ec2',region_name=region)
        instances = ec2.describe_instances()
        for r in instances['Reservations']:
            for i in r['Instances']:
                for tag in i.get('Tags',[]):
                    if tag['Key'] == 'Name':
                        instanceName = tag['Value']
                        if i['State']['Name'] == 'stopped':
                            instances_start.append(i['InstanceId'])
                            ec2.start_instances(InstanceIds=instances_start)
                        elif i['State']['Name'] == 'terminated':
                            continue
                        else:
                            print('Instância '+instanceName+' já está rodando.\n' )
                            instancesAlreadStart.append(instanceName)
        print('\n')
    print(str(len(instances_start))+ " instância(s) esta(ão) sendo iniciada(s) .... \n")   
    
    return {
    "InstanciasIniciadas": instancesAlreadStart,
    "InstanciasSendoIniciadas": instances_start
    }