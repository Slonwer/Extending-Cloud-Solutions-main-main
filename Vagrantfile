Vagrant.configure("2") do |config|
  
  # Definir a primeira máquina "web_1"
  config.vm.define "web_1" do |web|
    # Defina a box base que será utilizada (centos/7)
    web.vm.box = "centos/7"
    
    # Configuração de rede: cria uma rede privada com DHCP
    web.vm.network "private_network", type: "dhcp"
    
    
  end

end
