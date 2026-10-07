# VPC, the networking service

A Virtual Private Cloud is your own isolated network inside AWS. Nothing you launch
can talk to anything until you decide the address ranges, where the exits are and
what the firewalls allow. The Session 19 Terraform project builds exactly this.

## CIDR

The address range of the network, written as a base address and a prefix length.
10.20.0.0/16 means the first 16 bits are fixed and the remaining 16 are available,
65,536 addresses. The VPC gets one range and every subnet carves a smaller block out
of it. Private ranges are used, 10.0.0.0/8, 172.16.0.0/12 or 192.168.0.0/16, and the
range should not overlap with any network you will later connect to, such as an
office VPN.

## Subnets

A slice of the VPC's range placed in one availability zone. 10.20.1.0/24 is 256
addresses in zone a. AWS reserves five of them in each subnet. Having subnets in two
or three zones is what lets an application survive a datacenter failure.

## Route tables

Each subnet is associated with one route table, which says where traffic for each
destination goes. Every table has a local route for the VPC's own range. What else it
contains decides what kind of subnet it is.

## Internet Gateway

The VPC's door to the internet. One per VPC, attached once. A route table with
0.0.0.0/0 pointing at the internet gateway sends everything not local out to the
internet, and lets inbound traffic reach instances that have public IPs.

## NAT Gateway

Lets instances in a private subnet reach out to the internet, for package updates
and external APIs, without being reachable from it. It lives in a public subnet and
the private subnet's route table sends 0.0.0.0/0 to it. It is billed hourly plus
per gigabyte, which is why small projects sometimes skip it.

## Public versus private subnet

The only difference is the route table. A subnet whose table routes 0.0.0.0/0 to an
internet gateway is public, and instances in it with public IPs are reachable from
outside. A subnet whose table routes 0.0.0.0/0 to a NAT gateway, or nowhere, is
private. Load balancers and bastions go in public subnets. Application servers and
databases go in private ones.

## Security groups and network ACLs

Both are firewalls, at different layers. A security group is attached to an instance,
is stateful, and only has allow rules. A network ACL is attached to a subnet, is
stateless so replies need their own rule, and has numbered allow and deny rules
evaluated in order. The default network ACL allows everything and most setups leave
it that way, using security groups for the real control and ACLs only to block a
known bad range at the subnet edge.

## How the Session 19 project fits together

    Internet
       |
    Internet Gateway
       |
    VPC 10.20.0.0/16
       |
    Route table: 0.0.0.0/0 -> igw
       |
    Public subnet 10.20.1.0/24
       |
    Security group: 80 from anywhere, 22 from allowed range
       |
    EC2 web server
