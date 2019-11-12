import boto3
import os

session = boto3.Session(
        aws_access_key_id = os.environ['access_key_id'],
        aws_secret_access_key = os.environ['secret_access_key'])

regions = ["us-east-1","sa-east-1"]

instances_stop = []
instancesAlreadStop = []

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
                        if i['State']['Name'] == 'running':
                            instances_stop.append(i['InstanceId'])
                            ec2.stop_instances(InstanceIds=instances_stop)
                        elif i['State']['Name'] == 'terminated':
                            continue
                        else:
                            print('Instância '+instanceName+' já está pausada.\n' )
                            instancesAlreadStop.append(instanceName)
        print('\n')
    print(str(len(instances_stop))+ " instância(s) esta(ão) sendo stopada(s) .... \n")   
    
    return {
    "InstanciasPausadas": instancesAlreadStop,
    "InstanciasSendoStopadas": instances_stop
    }