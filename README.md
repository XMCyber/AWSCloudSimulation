## Cloud Permission Simulation
The purpose of this project is to allow Blue Teams to understand the impact of certain cloud access keys\users on the their cloud environment in a graph way, similar to [BloodHound](https://github.com/BloodHoundAD/BloodHound).
The project is in very early POC stage.

## How it works?

1. We gather metadata info from AWS - list of S3, EC2, Lambda, Roles, etc.
2. We are then creating `SyetemConnection` between various cloud resources. For example a connection between AccessKey to User or between User\Role and some action on some S3 bucket. 
3. We then use the various `SystemConnection` we created in order to create full attack vector called `attack`.
4. We then export this to a Neo4j graph in order to allow Blue Teams to investigate.

## How it looks?

The attack map:

![](https://github.com/smulikHakipod/CloudSimulation/raw/master/imgs/image12.png "")

SystemConnection:

![](https://github.com/smulikHakipod/CloudSimulation/raw/master/imgs/image2.png "")
![](https://github.com/smulikHakipod/CloudSimulation/raw/master/imgs/image8.png "")
![](https://github.com/smulikHakipod/CloudSimulation/raw/master/imgs/image9.png "")


## What can you do with it?
You can query the database for insights. For example:

```
MATCH (start:IAMAccessKey{NodeId: "iam_access_key_AKIAIL4WCUER5XXXXX"}), (end:EC2Instance{NodeId:"ec2_instance_i-0e6e9db484fXXXXXX"})
MATCH p = (start)-[r:Attack*]->(end)  RETURN p AS shortestPath, reduce(cost=0, rel in relationships(p) | cost + rel.weight) AS totalCost
ORDER BY totalCost ASC
SKIP 1
LIMIT 1
```
Which means give me the shortest path from some access key to some EC2 instance sorted by the "attack" cost.
This can also be recursive, meaning multiple attack legs can be achieved. 
Things like the network "choke points" can be located and mitigated, and much more.

## Requirements
* A Neo4j database. 
* Python 3. 
* AWS account to run the simulation on. Its probably good to start with staging environment. 

Under requirements.txt there are all the python dependencies.
Its recommended to install those using [Python Virtual Environments](https://docs.python.org/3/tutorial/venv.html). 

## Configuration

Configure the AWS account on the machine the script is running.
Its recommended to use a different profile.
[AWS How To](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html)

Setup the account username and password for Neo4j.

Once those configured, specify the details under `config.json`

## Running 

`python main.py`