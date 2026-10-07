# IAM, the governance service

IAM is the service that decides who can do what in an AWS account. Every API call
AWS receives is checked against IAM before anything happens, so it sits underneath
every other service rather than beside them.

## The pieces

Users are identities for people or applications that need long lived credentials.
A user has a password for the console and up to two access keys for the CLI and SDKs.
Each real person gets their own user, never a shared one, so actions can be traced.

Groups are collections of users. Policies are attached to the group and every member
inherits them, so adding someone to the developers group is one action instead of
attaching five policies by hand. A user can be in several groups.

Roles are identities with no credentials of their own. Something assumes a role and
receives temporary credentials that expire, usually in an hour. An EC2 instance
assumes a role to reach S3, a Lambda function assumes one to write to DynamoDB, and a
user from another account assumes one to work in this account. Roles are how you
avoid putting access keys inside servers and code.

Policies are JSON documents that say which actions are allowed or denied on which
resources. An identity based policy is attached to a user, group or role. A resource
based policy, like an S3 bucket policy, is attached to the resource and can name
principals from other accounts.

    {
      "Version": "2012-10-17",
      "Statement": [{
        "Effect": "Allow",
        "Action": ["s3:GetObject", "s3:ListBucket"],
        "Resource": ["arn:aws:s3:::library-assets", "arn:aws:s3:::library-assets/*"]
      }]
    }

Permissions are the result of evaluating every policy that applies. The rule is that
everything is denied by default, an explicit Allow opens it, and an explicit Deny
anywhere wins over any Allow.

## Least privilege

Grant only the actions and resources a task actually needs, nothing broader. The
policy above lets an application read one bucket. It cannot write to it, delete from
it, or see any other bucket. If the application is compromised, the damage is limited
to what it could already do. Start narrow and widen when something fails, rather than
starting with AdministratorAccess and promising to tighten it later.

## Best practices

Lock the root user away with a hardware MFA device and never use it for daily work.
Turn on MFA for every human user. Use roles for anything running on AWS instead of
access keys. Rotate the access keys that do exist. Use groups rather than attaching
policies to users one by one. Review IAM Access Analyzer and the last used timestamps
to find permissions nobody uses, then remove them. Keep CloudTrail on so every IAM
decision is logged.

## Where it shows up

An EC2 instance role that lets a web server read secrets and write logs. A CI pipeline
that assumes a deployment role through OIDC instead of storing keys in GitHub. A
cross account role so an auditor can read, but not change, production. A bucket
policy that lets a CloudFront distribution serve private objects.
