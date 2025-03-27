logistics-tracking/
│── infrastructure/              
│   ├── __main__.py               # Pulumi script to set up AWS infrastructure
│   ├── appsync.py                # AppSync GraphQL setup for subscriptions and API
│   ├── ecs.py                    # ECS cluster for Celery workers (auto-scaling)
│   ├── rds.py                    # PostgreSQL RDS setup for storing shipment data
│   ├── sqs.py                    # SQS queue setup for Celery task distribution
│   ├── redis.py                  # Redis (ElastiCache) setup for task results and caching
│   ├── sns.py                    # SNS topic setup for AppSync subscriptions
│   ├── monitoring.py             # CloudWatch setup for monitoring ECS and Celery tasks
│── backend/                      
│   ├── app.py                    # AppSync resolvers and API (queries, mutations, subscriptions)
│   ├── tasks.py                  # Celery tasks for processing updates and database interaction
│   ├── worker.py                 # Celery worker setup and configuration
│   ├── database.py               # SQLAlchemy models for PostgreSQL (e.g., shipments)
│   ├── schema.graphql            # AppSync GraphQL schema for queries, mutations, and subscriptions
│   ├── websocket.py              # WebSocket server for real-time updates
│── docker-compose.yml            # Local testing setup with Docker (ECS, Redis, etc.)
│── README.md                     # Project documentation
