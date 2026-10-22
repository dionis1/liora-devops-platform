resource "hcloud_ssh_key" "admin" {
  name = "${var.project_name}-admin"
  public_key = var.ssh_public_key
}
resource "hcloud_firewall" "edge" {
  name = "${var.project_name}-edge"
  rule {
    direction = "in"
    protocol = "tcp"
    port = "22"
    source_ips = var.ssh_allowed_cidrs
  }
  rule {
    direction = "in"
    protocol = "tcp"
    port = "80"
    source_ips = ["0.0.0.0/0", "::/0"]
  }
  rule {
    direction = "in"
    protocol = "tcp"
    port = "443"
    source_ips = ["0.0.0.0/0", "::/0"]
  }
}
resource "hcloud_network" "cluster" {
  name = "${var.project_name}-private"
  ip_range = "10.70.0.0/16"
}
resource "hcloud_network_subnet" "cluster" {
  network_id = hcloud_network.cluster.id
  type = "cloud"
  network_zone = "eu-central"
  ip_range = "10.70.1.0/24"
}
resource "hcloud_server" "k3s" {
  name = "${var.project_name}-k3s-01"
  image = "ubuntu-24.04"
  server_type = var.server_type
  location = var.location
  ssh_keys = [hcloud_ssh_key.admin.id]
  firewall_ids = [hcloud_firewall.edge.id]
  public_net {
    ipv4_enabled = true
    ipv6_enabled = true
  }
  network {
    network_id = hcloud_network.cluster.id
    ip = "10.70.1.10"
  }
  depends_on = [hcloud_network_subnet.cluster]
  labels = { project = var.project_name, role = "k3s" }
}
