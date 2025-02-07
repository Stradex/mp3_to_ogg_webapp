output "bucket_connection_info" {
  value = {
    name     = digitalocean_spaces_bucket.local_bucket.name
    host     = digitalocean_spaces_bucket.local_bucket.bucket_domain_name
    endpoint  = digitalocean_spaces_bucket.local_bucket.endpoint
    urn		  = digitalocean_spaces_bucket.local_bucket.urn
  }
  sensitive = false
}
