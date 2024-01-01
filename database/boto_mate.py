import boto3

# Set your AWS credentials and region
aws_access_key = 'your_access_key'
aws_secret_key = 'your_secret_key'
region_name = 'your_region'

# Set the AMI ID, instance type, key pair name, and security group IDs
ami_id = 'ami-xxxxxxxxxxxxxxxxx'  # Replace with your AMI ID
instance_type = 't2.micro'        # Choose your instance type

# Create an key-pair before running this script
# Will have to use the key pair to connect to instance later.
key_pair_name = 'your_key_pair'   # Replace with your key pair name
# Same goes with security-group create a security group and attach it
# here with group-id
security_group_ids = ['sg-xxxxxxxxxxxxxxxxx']  # Replace with your security group IDs

# Create a new EC2 client
ec2_client = boto3.client('ec2', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key, region_name=region_name)

# Launch a new EC2 instance
response = ec2_client.run_instances(
    ImageId=ami_id,
    InstanceType=instance_type,
    KeyName=key_pair_name,
    MinCount=1,
    MaxCount=1,
    SecurityGroupIds=security_group_ids,
)

# Get the instance ID from the response
instance_id = response['Instances'][0]['InstanceId']

print(f"Instance {instance_id} is launching.")

# Wait for the instance to be running
ec2_client.get_waiter('instance_running').wait(InstanceIds=[instance_id])

print(f"Instance {instance_id} is now running.")
