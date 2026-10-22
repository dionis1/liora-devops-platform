variable "project_name" {
  type = string
  default = "liora-devops"
}
variable "location" {
  type = string
  default = "nbg1"
}
variable "server_type" {
  type = string
  default = "cx43"
}
variable "ssh_public_key" {
  description = "SSH public key (not private)"
  type = string
}
variable "ssh_allowed_cidrs" {
  type = list(string)
  validation {
    condition = length(var.ssh_allowed_cidrs) > 0 && !contains(var.ssh_allowed_cidrs, "0.0.0.0/0") && !contains(var.ssh_allowed_cidrs, "::/0")
    error_message = "Provide your trusted SSH IP range, not unrestricted internet access."
  }
}
