resource "proxmox_vm_qemu" "web_1" {
  name        = "web_1"
  target_node = var.pve_node_name

  clone = "centos7-template"

  network {
    model  = "virtio"
    bridge = "vmbr0"
  }

  disks {
    storage = var.storage_pool_name
    size    = "250G"
  }

  agent = 1
  ipconfig0 = "ip=dhcp"
}
