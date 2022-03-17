# main.tf - compatible with terraform 0.12 only

# Add your SSH public key
resource "aws_key_pair" "ssh_key" {
    key_name = "name_of_key"
    public_key = "ssh-rsa AAAABBBCCC..."
}

# We are using the default AWS VPC network so leave empty
resource "aws_default_vpc" "default" {

}

# Add firewall rule to allow SSH from our Bounce Server IP only, outgoing is ok!
resource "aws_security_group" "SSHAdmin" {
    name = "SSHAdmin"
    description = "SSH traffic"
    vpc_id = aws_default_vpc . default . id
    ingress {
        from_port = 0
        to_port = 22
        protocol = "tcp"
        cidr_blocks = ["123.123.123.123/32"]
    }
    egress {
        from_port = 0
        to_port = 0
        protocol = "-1"
        cidr_blocks = ["0.0.0.0/0"]
    }
}

# Link ssh key and security group to ec2 instance

resource "aws_instance" "basic_ec2" {
    ami = "ami-0039c41a10b230acb"
    instance_type = "t2.micro"

    vpc_security_group_ids = aws_security_group.SSHAdmin.id
    key_name = aws . ssh_key.id
    associate_public_ip_address = "true"
    root_block_device {
        volume_size = "25"
    }

    user_data = <<EOF

    #!/bin/bash
    DOMAIN = "www.linux-update-packets.org";
    C2IP = "172.31.31.13";

    sleep 10
    sudo add-repository \
     "deb [arch=amd64]https://download.docker.com/linux/ubuntu \
     $(lsb_release -cs) \
     stable"
    apt update
    apt install -y docker-ce
    docker run -dti -p80:80 -p443:443 \
    -e DOMAIN="www.somedomain.com"
    -e C2IP="$C2IP" \
    -v /opt/letsencrypt:/etc/letsencrypt \
    blv_pro/nginx

    EOF
}

# Print the server's public id
output "public_ip" {
    value = aws_instance.basic_ec2 . public_ip
}