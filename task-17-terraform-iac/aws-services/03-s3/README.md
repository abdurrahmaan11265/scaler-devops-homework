# S3, the storage service

S3 stores objects, meaning whole files with a name, not blocks or a filesystem. It
is effectively unlimited, durable to eleven nines, and reachable over HTTPS from
anywhere, which is why so many other services are built on top of it.

## Buckets and objects

A bucket is the top level container. Its name must be unique across all of AWS, not
just your account, and it lives in one region. Objects are the files inside it,
addressed by a key such as reports/2026/october.csv. There are no real folders, the
slashes are just part of the key, though the console draws them as folders. An
object can be up to 5 TB.

## Storage classes

The price per gigabyte against how quickly and how often you need the data back.
Standard is for data in active use. Standard-IA and One Zone-IA are cheaper to store
and cost a little to retrieve, for backups read once a month. Glacier Instant,
Flexible and Deep Archive are progressively cheaper with retrieval taking from
milliseconds to hours, for data kept for compliance. Intelligent-Tiering watches
access patterns and moves objects between tiers automatically.

## Versioning

Once enabled on a bucket, overwriting an object keeps the old copy under a version
id, and deleting adds a delete marker instead of removing anything. It is the undo
button for S3 and the Terraform demo turns it on. Old versions are still billed,
which is where lifecycle policies come in.

## Lifecycle policies

Rules that act on objects as they age: move to Standard-IA after 30 days, to Glacier
after 90, delete non current versions after a year, abort incomplete multipart
uploads after a week. This is how a log bucket stays cheap without anyone cleaning
it by hand.

## Encryption

Objects are encrypted at rest by default now with S3 managed keys, SSE-S3. SSE-KMS
uses a key from KMS instead, which gives an audit trail of every decrypt and lets
you control who may use the key. In transit it is HTTPS. Encryption is almost
always a compliance requirement rather than a performance decision.

## Bucket policies

A resource based IAM policy attached to the bucket. Used to grant another account
read access, to allow a CloudFront distribution to serve the objects, or to require
HTTPS. Block Public Access, which the Terraform demo turns on, sits above bucket
policies and refuses any policy that would make the bucket public, which is the
setting that prevents the classic leaked bucket.

## Where it shows up

Static website and frontend hosting. Backups and database snapshots. Log storage for
CloudTrail, load balancers and applications. Data lake storage for analytics. Build
artifacts and container layers. Terraform remote state.
