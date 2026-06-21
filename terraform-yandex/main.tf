provider "yandex" {
  service_account_key_file = "key.json"
  cloud_id                 = var.cloud_id
  folder_id                = var.folder_id
  zone                     = var.zone
}

# Используем уже существующую default сеть
data "yandex_vpc_network" "default" {
  name = "default"
}

data "yandex_vpc_subnet" "default" {
  name = "default-${var.zone}"
}

resource "yandex_compute_instance" "audit-vm" {
  name        = "vandyshev-audit-vm"
  platform_id = "standard-v3"
  zone        = var.zone

  resources {
    cores  = 2
    memory = 4
  }

    boot_disk {
    initialize_params {
      image_id = "fd8hrphlcsmi293sjc74"   # Актуальный Ubuntu 22.04 (июнь 2026)
      size     = 20
    }
  }

  network_interface {
    subnet_id = data.yandex_vpc_subnet.default.id
    nat       = true
  }

  metadata = {
    ssh-keys = "ubuntu:${file("~/.ssh/id_rsa.pub")}"
    user-data = <<-EOF
      #cloud-config
      package_update: true
      packages:
        - docker.io
      runcmd:
        - systemctl enable --now docker
        - docker pull ${var.docker_image}
        - docker run -d --restart always --name audit-service -p 8000:8000 ${var.docker_image}
      EOF
  }
}

output "public_ip" {
  value = yandex_compute_instance.audit-vm.network_interface[0].nat_ip_address
}

output "service_url" {
  value = "http://${yandex_compute_instance.audit-vm.network_interface[0].nat_ip_address}:8000"
}