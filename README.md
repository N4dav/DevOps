# DevOps Learning Project

### This repository contains a small web application written in Python with Flask that provides weather forecasts for 7 days by city name provided as input by the client, with added functionality of another microservice for image download from S3 bucket using boto3, as well as an HTML page and backend directory to backup history of requests made. This application was created to learn and practice DevOps skills.

## Virtualization -
deployed the application on a VM on an ESXi server.

## Containerization -
ran the application on a Docker container and on multiple containers with Nginx as a load balancer using Docker Compose.

## Cloud Computing -
I deployed the application on an EC2 instance.

## Kubernetes -
deployed the application on a Minikube cluster.

## CI/CD - 
I implemented a Jenkins pipeline that fetches the source code from my private GitLab repository, builds the Docker image, runs tests, and pushes the image to DockerHub. The pipeline then connects via SSH to an EC2 instance named "Prod" and pulls the artifact from DockerHub to run it.

# Main Project - 
I created a Jenkins pipeline that fetches the source code from Github, builds the artifact, and deploys it on an EKS cluster. I also configured permissions for the Jenkins agent and EKS master server with IAM roles and RBAC. Additionally, I configured the service.yml of ALB, and configured horizontal pod auto-scaling.

## Monitoring -
After learning monitoring, I used Prometheus exporter to scrape metrics and combined it with Grafana for monitoring the application.


### Infrastructure -

All the servers used besides Github and Dockerhub are EC2 instances installed with Docker. The following servers were used:

    Jenkins master
    Jenkins agent
    Gitlab server
    Sonarqube for static tests
    JFrog Artifactory

All these servers are provisioned on the same AZ and VPC so that traffic remains free. Webhooks were configured to automate the Jenkins pipeline.
