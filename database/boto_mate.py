import os
import boto3
from dotenv import load_dotenv

load_dotenv()

aws_access_key = os.getenv("aws_access_key")
aws_secret_key = os.getenv("aws_secret_key")
region_name = 'ap-south-1'
ami_id = 'ami-0d980397a6e8935cd'
instance_type = 't2.micro'
key_pair_name = 'NewInstanceKey'   
private_key_file = f"{key_pair_name}.pem"


ec2_resource = boto3.resource('ec2', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key, region_name=region_name)


existing_key_pairs = [key.name for key in ec2_resource.key_pairs.all()]
if key_pair_name not in existing_key_pairs:
    key_pair = ec2_resource.create_key_pair(KeyName=key_pair_name)
    with open(private_key_file, 'w') as key_file:
        key_file.write(key_pair.key_material)
    os.chmod(private_key_file, 0o400)
    print(f"Key pair '{key_pair_name}' created and private key saved.\n")
else:
    print(f"Key pair '{key_pair_name}' already exists.\n")

existing_instances = [instance.id for instance in ec2_resource.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])]
if not existing_instances:
    instance = ec2_resource.create_instances(
        ImageId=ami_id,
        InstanceType=instance_type,
        KeyName=key_pair_name,
        MinCount=1,
        MaxCount=1,
    )[0]  
    instance_id = instance.id
    print(f"Instance {instance_id} is launching.\n")
    instance.wait_until_running()
    print(f"Instance {instance_id} is now running.\n")
    public_ip = instance.public_ip_address
    ssh_command = f"ssh -i {private_key_file} ec2-user@{public_ip}"
    print(f"SSH command: {ssh_command}\n")
else:
    print(f"An existing running instance was found. No new instance launched.\n")
    instance_id = existing_instances[0]
    
    ec2_client = boto3.client('ec2', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key, region_name=region_name)   
    instance = ec2_resource.Instance(instance_id)

    instance_ip_address = instance.public_ip_address
    print(f"Instance {instance_id} is running at IP address {instance_ip_address}.\n")
    
    ssh_command = f"ssh -i {private_key_file} ec2-user@{instance_ip_address}"
    print(f"SSH command:\n{ssh_command}")
