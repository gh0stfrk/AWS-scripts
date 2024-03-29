#!/usr/bin/bash
# Install mysql on Amazon Linux

# Check if script is run as root
if [ "$EUID" -ne 0 ]; then
    echo "Please run this script with sudo."
    exit 1
fi


echo "Started Running with superuser privileges!"


# Adding mysql's redhat repository to the list.
wget  https://dev.mysql.com/get/mysql80-community-release-el9-5.noarch.rpm

sudo dnf install mysql80-community-release-el9-5.noarch.rpm -y 
sudo dnf makecache
sudo dnf install mysql-community-server -y 
sudo service mysqld start

# Login without password 
# sudo echo 'skip-grant-tables' >> /etc/my.cnf
# Allows you to connect to the database with the public ip

sudo echo 'bind-address = 0.0.0.0' >> /etc/my.cnf

sudo service mysqld restart 


log_line=$(sudo grep 'temporary password' /var/log/mysqld.log)
# Extracting the password using awk and removing leading/trailing spaces
password=$(echo "$log_line" | awk -F ": " '{print $NF}' | awk '{gsub(/^[ \t]+|[ \t]+$/, ""); print}')

# Displaying the extracted password
# echo "Temporary root Password Extracted: $password"
sqluser='sal'
sqlpassword='p@ssW0rd'

# Create a deafault user 
mysql -u root -p$password -h localhost -e "USE mysql;CREATE USER '$sqluser'@'%' IDENTIFIED BY '$sqlpassword';
GRANT ALL PRIVILEGES ON *.* TO 'sal'@'%';
FLUSH PRIVILEGES;"

# Cleanig up
echo 'MySQL user account created';