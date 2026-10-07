# DynamoDB and RDS, the database services

Two very different ways to store data. RDS runs a traditional relational database
engine on managed servers. DynamoDB is a key value store AWS built, with no servers
to see at all. Which one fits depends on how the data will be queried.

## DynamoDB

NoSQL means there is no fixed schema and no joins. Each item is a JSON like document
and only the key attributes are required. The trade is that queries are limited to
what the keys support, in return for single digit millisecond reads at any scale.

A table holds items. An item is one record, up to 400 KB. Attributes are the fields
on an item, and different items in the same table can have different attributes.

The partition key is the attribute DynamoDB hashes to decide where the item is
stored. Every read has to supply it, so it should be something you always know,
such as a member id. A sort key is optional and, when present, the two together form
the primary key. Items with the same partition key are stored together ordered by
sort key, which lets you ask for all loans of one member in date order with a single
query.

    Table: Loans
    partition key: member_id      sort key: borrowed_at
    member_id=42  borrowed_at=2026-10-01  book="Accelerate"  due=2026-10-15
    member_id=42  borrowed_at=2026-10-05  book="SRE"         due=2026-10-19

Use cases are session stores, shopping carts, IoT event streams, leaderboards and
anything with a simple access pattern and unpredictable scale. It pairs naturally
with Lambda because there is nothing to connect to, just an API.

## RDS

A relational database with tables, rows, foreign keys, transactions and SQL. AWS
runs the engine, handles patching, backups and failover, and you connect to an
endpoint as you would to any database server.

Supported engines are PostgreSQL, MySQL, MariaDB, Oracle, SQL Server, and Aurora,
which is AWS's own MySQL and PostgreSQL compatible engine with storage that scales
on its own.

A DB instance is the server, chosen by class such as db.t3.micro and storage size.
It lives in a subnet group inside your VPC, which is how it ends up private.

Security is the VPC first: the instance sits in a private subnet and its security
group only allows 5432 from the application servers' security group. Then database
users and passwords, which should come from Secrets Manager rather than config
files. Encryption at rest with KMS and TLS in transit are both a checkbox.

Backups are automatic daily snapshots plus transaction logs, kept for a configurable
number of days, which gives point in time restore to any second in that window.
Manual snapshots are kept until deleted.

Multi-AZ keeps a synchronous standby copy in a second availability zone. If the
primary fails, the DNS endpoint moves to the standby in about a minute with no data
loss. It is for availability, not for extra read capacity.

Read replicas are asynchronous copies that can serve read queries. They take report
and dashboard load off the primary, and can be in another region for disaster
recovery. Writes still go only to the primary.

Use cases are anything with relational data and complex queries: the catalog and
lending records of a library, orders and customers, user accounts, any existing
application written against PostgreSQL or MySQL.

## Choosing between them

If the queries are known, simple and keyed, and the scale is large or spiky,
DynamoDB. If the data is relational, the queries are ad hoc, or the application
already speaks SQL, RDS. Many systems use both, RDS for the core records and
DynamoDB for sessions and events.
