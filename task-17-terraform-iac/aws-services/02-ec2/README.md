# EC2, the compute service

EC2 rents virtual machines by the second. You pick an operating system image, a
size, a network to sit in and a firewall, and a few minutes later you have a server
you can SSH into. Everything else in this document is one of those choices.

## AMI

An Amazon Machine Image is the template an instance boots from: operating system,
installed packages and any files that were on disk when the image was made. AWS
publishes Amazon Linux, Ubuntu and Windows images, and you can snapshot a configured
instance into your own AMI so new servers start already set up. AMI ids are per
region, which is why Terraform looks them up by name rather than hard coding one.

## Instance types

The size and shape of the machine. The family letter says what it is good at, the
size says how much of it you get. t3 and t4g are burstable general purpose, good for
small web servers. m is balanced, c is compute heavy, r is memory heavy, g and p
have GPUs. t3.micro, 2 vCPU and 1 GiB, is the free tier size and is what a homework
web server needs.

## Key pairs

SSH access. AWS keeps the public key and injects it into the instance at launch, you
keep the private key file. There is no password login. Lose the private key and you
cannot get into that instance, so the key is created before the instance and the
file is treated like a credential.

## Security groups

A stateful firewall attached to the instance's network interface. Rules are allow
only, there is no deny, and anything not allowed is dropped. A typical web server
group allows 80 and 443 from anywhere and 22 from your own IP only. Because it is
stateful, the reply to an allowed inbound request is let out automatically.

## EBS

Elastic Block Store is the disk. The root volume holds the operating system and
extra volumes can be attached for data. EBS volumes live independently of the
instance, so a data volume survives the instance being terminated if you tell it to,
and can be snapshotted to S3 for backup. gp3 is the default general purpose type.

## Public and private IP

Every instance gets a private IP from its subnet, and that is how other things in
the VPC reach it. A public IP is optional, comes from AWS's pool, and changes every
time the instance stops and starts. An Elastic IP is a public address you own and
can move between instances, which is what you use when DNS points at a server.

## Instance lifecycle

pending while it launches, running while it works, stopping and stopped when it is
shut down but kept, with the EBS root volume intact and no compute charge, and
shutting down then terminated when it is deleted for good. Rebooting stays in
running. Stopping and starting moves it to new hardware and gives it a new public
IP unless it has an Elastic IP.

## Where it shows up

Web and API servers behind a load balancer. Batch jobs that run for an hour and are
terminated. Bastion hosts for reaching private resources. Self hosted CI runners.
The worker nodes of a Kubernetes cluster are EC2 instances too.
