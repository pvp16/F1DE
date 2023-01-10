terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

  required_version = ">= 1.2.0"
}

provider "aws" {
  shared_config_files      = ["/home/prithvivp/.aws/config"]
  shared_credentials_files = ["/home/prithvivp/.aws/credentials"]

}
resource "aws_security_group" "f1de_security_group" {
  name        = "f1de_security_group"
  description = "Security group to allow inbound SCP & outbound 8080 (Airflow) connections"

  ingress {
    description = "Inbound SCP"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
resource "tls_private_key" "f1dersa" {
  algorithm = "RSA"
}

resource "local_file" "f1dekey" {
  content  = tls_private_key.f1dersa.private_key_pem
  filename = "f1dekey.pem"
}

resource "aws_key_pair" "f1dekey" {
  key_name   = "f1dekeypair"
  public_key = tls_private_key.f1dersa.public_key_openssh
}
resource "aws_instance" "f1de-server" {
  ami           = "ami-0f69bc5520884278e"
  instance_type = "t2.micro"
  key_name      = aws_key_pair.f1dekey.key_name
  security_groups = [aws_security_group.f1de_security_group.name]
}

resource "aws_redshift_cluster" "f1de-redshift" {
  cluster_identifier = "f1de-redshift-cluster"
  database_name      = "f1de"
  master_username    = "f1de"
  master_password    = "Pvp286c1229"
  node_type          = "dc2.large"
  cluster_type       = "single-node"
  
}

resource "aws_s3_bucket" "f1de-bucket" {
  bucket = "f1de-data-lake"
  acl    = "private"
  versioning {
    enabled = true
  }
}