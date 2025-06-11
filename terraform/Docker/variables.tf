variable "proxmox_host_ip" {
  description = "Endereço IP do host Proxmox"
  type        = string
}

variable "proxmox_user" {
  description = "Usuário do Proxmox (ex: root@pam)"
  type        = string
}

variable "proxmox_password" {
  description = "Senha do Proxmox"
  type        = string
  sensitive   = true  # Evita que a senha seja exibida nos logs
}
