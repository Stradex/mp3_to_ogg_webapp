variable "do_token" {
  type = string
  sensitive= true
  description = "Digital ocean API Token"
}

variable "spaces_access_id" {
  type = string
  sensitive= true
  description = "Digital ocean Spaces ACCESS ID"
}

variable "spaces_access_key" {
  type = string
  sensitive= true
  description = "Digital ocean Spaces ACCESS KEY"
}
