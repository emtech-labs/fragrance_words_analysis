# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/bionic64"
  config.vm.box_check_update = false
  config.vm.provider :virtualbox do |vb|
    vb.memory = 8192
    vb.cpus = 4
    config.disksize.size = '300GB'
    vb.gui = false
  end

  config.vm.network :forwarded_port, guest: 80, host: 80
  config.vm.network :forwarded_port, guest: 8888, host: 8888
  config.vm.network :private_network, ip: "192.168.33.110"
  config.vm.synced_folder "./", "/home/vagrant/working"

  config.vm.provision "shell", inline: <<-SHELL
    sudo apt-get -y update
    sudo apt-get dist-upgrade
    sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common

    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
    sudo apt-key fingerprint 0EBFCD88
    sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
    sudo apt-get update
    sudo apt-get install -y docker-ce

    apt-cache madison docker-ce
    sudo apt-get install -y docker-ce=18.06.1~ce~3-0~ubuntu

    sudo usermod -aG docker vagrant

    sudo curl -L "https://github.com/docker/compose/releases/download/1.22.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    docker-compose --version
  SHELL
end