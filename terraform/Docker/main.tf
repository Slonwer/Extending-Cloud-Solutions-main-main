provider "proxmox" {
  pm_api_url      = "https://<SEU-PROXMOX-IP>:8006/api2/json"
  pm_api_token_id = "<usuário>@pam!<nome-do-token>"
  pm_api_token_secret = "<token-secreto>"
  pm_tls_insecure = true  # Apenas para testes, desative em produção
}

variable "pve_node_name" {
  default = "pve"
}

variable "storage_pool_name" {
  default = "local-lvm"
}

resource "proxmox_vm_qemu" "web_1" {
  name        = "web_1"
  target_node = var.pve_node_name

  clone = "centos7-template"

  network {
    model  = "virtio"
    bridge = "vmbr0"
  }

  disk {
    storage = var.storage_pool_name
    size    = "250G"
    type    = "scsi"
    slot    = 0
  }

  agent     = 1
  ipconfig0 = "ip=dhcp"
}
