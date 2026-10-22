output "server_public_ipv4" {
  value = hcloud_server.k3s.ipv4_address
}
output "server_private_ipv4" {
  value = "10.70.1.10"
}
output "ssh_command" {
  value = "ssh root@${hcloud_server.k3s.ipv4_address}"
}
