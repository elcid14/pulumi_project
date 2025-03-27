import pulumi
import pulumi_aws as aws
import pulumi_random as random

def create_rds_postgresql():
    # Generate a random password for the database
    db_password = random.RandomPassword("dbPassword",
        length=16,
        special=False
    )

    #security groupd for rds
    db_security_group = aws.ec2.SecurityGroup("rdsSecurityGroup",
        description="Allow inbound access to RDS PostgreSQL",
        ingress=[
            {
                "protocol": "tcp",
                "from_port": 5432,
                "to_port": 5432,
                "cidr_blocks": ["0.0.0.0/0"],  # Adjust for security
            }
        ],
        egress=[
            {
                "protocol": "-1",
                "from_port": 0,
                "to_port": 0,
                "cidr_blocks": ["0.0.0.0/0"],
            }
        ]
    )

    # Create an RDS PostgreSQL instance
    rds_instance = aws.rds.Instance("logistics-tracking-dev-db",
        allocated_storage=20,
        engine="postgres",
        engine_version="14",
        instance_class="db.t3.micro",
        name="logisticstrackingdb",
        username="pulumi",
        password=db_password.result,
        publicly_accessible=False,
        multi_az=False,
        skip_final_snapshot=True,
        vpc_security_group_ids=[db_security_group.id]
    )

    pulumi.export("RDS_Endpoint", rds_instance.endpoint)
    pulumi.export("RDS_DB_Name", rds_instance.name)
    pulumi.export("RDS_Username", rds_instance.username)
    pulumi.export("RDS_Password", rds_instance.password)
    
    return rds_instance
