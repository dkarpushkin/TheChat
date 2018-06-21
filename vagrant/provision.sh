#!/bin/sh -e

# Edit the following to change the name of the database user that will be created:
APP_DB_USER=vagrant
APP_DB_PASS=vagrant

# Edit the following to change the name of the database that is created (defaults to the user name)
APP_DB_NAME=$APP_DB_USER

# Edit the following to change the version of PostgreSQL that is installed
PG_VERSION=9.5

###########################################################
# Changes below this line are probably not necessary
###########################################################
print_db_usage () {
  echo "Your PostgreSQL database has been setup and can be accessed on your local machine on the forwarded port (default: 15432)"
  echo "  Host: localhost"
  echo "  Port: 15432"
  echo "  Database: $APP_DB_NAME"
  echo "  Username: $APP_DB_USER"
  echo "  Password: $APP_DB_PASS"
  echo ""
  echo "Admin access to postgres user via VM:"
  echo "  vagrant ssh"
  echo "  sudo su - postgres"
  echo ""
  echo "psql access to app database user via VM:"
  echo "  vagrant ssh"
  echo "  sudo su - postgres"
  echo "  PGUSER=$APP_DB_USER PGPASSWORD=$APP_DB_PASS psql -h localhost $APP_DB_NAME"
  echo ""
  echo "Env variable for application development:"
  echo "  DATABASE_URL=postgresql://$APP_DB_USER:$APP_DB_PASS@localhost:15432/$APP_DB_NAME"
  echo ""
  echo "Local command to access the database via psql:"
  echo "  PGUSER=$APP_DB_USER PGPASSWORD=$APP_DB_PASS psql -h localhost -p 15432 $APP_DB_NAME"
}

export DEBIAN_FRONTEND=noninteractive

PROVISIONED_ON=/etc/vm_provision_on_timestamp
if [ -f "$PROVISIONED_ON" ]
then
  echo "VM was already provisioned at: $(cat $PROVISIONED_ON)"
  echo "To run system updates manually login via 'vagrant ssh' and run 'apt-get update && apt-get upgrade'"
  echo ""
  print_db_usage
  exit
fi

PG_REPO_APT_SOURCE=/etc/apt/sources.list.d/pgdg.list
if [ ! -f "$PG_REPO_APT_SOURCE" ]
then
  # Add PG apt repo:
  echo "deb http://apt.postgresql.org/pub/repos/apt/ trusty-pgdg main" > "$PG_REPO_APT_SOURCE"

  # Add PGDG repo key:
  wget --quiet -O - https://apt.postgresql.org/pub/repos/apt/ACCC4CF8.asc | apt-key add -
fi

# Update package list and upgrade all packages
apt-get update
apt-get -y upgrade

apt-get -y install "postgresql-$PG_VERSION" "postgresql-contrib-$PG_VERSION"

PG_CONF="/etc/postgresql/$PG_VERSION/main/postgresql.conf"
PG_HBA="/etc/postgresql/$PG_VERSION/main/pg_hba.conf"
PG_DIR="/var/lib/postgresql/$PG_VERSION/main"

# Edit postgresql.conf to change listen address to '*':
sed -i "s/#listen_addresses = 'localhost'/listen_addresses = '*'/" "$PG_CONF"

# Append to pg_hba.conf to add password auth:
echo "host    all             all             all                     md5" >> "$PG_HBA"

# Explicitly set default client_encoding
echo "client_encoding = utf8" >> "$PG_CONF"

# Restart so that all new config is loaded:
service postgresql restart

cat << EOF | su - postgres -c psql
-- Create the database user:
CREATE USER $APP_DB_USER WITH PASSWORD '$APP_DB_PASS';

create database chat with owner=$APP_DB_USER template=template0;
EOF

#	Disabling firewall
sudo ufw disable

# Tag the provision time:
date > "$PROVISIONED_ON"

echo "Successfully created PostgreSQL dev virtual machine."
echo ""


#	Linux utils
apt-get install -y linux-headers-$(uname -r) build-essential git-core
apt-get install -y libxml2-dev libxslt-dev curl libcurl4-openssl-dev
apt-get install -y libreadline-dev
apt-get install -y libxslt1-dev libffi-dev libssl-dev

#	Python utils
apt-get install -y python3 python3-setuptools python3-dev libpq-dev pep8

#	pip, ipython and virtualenv
sudo apt-get -y install python-dev python-pip
apt-get install -y python3-pip ipython3
pip3 install virtualenv
pip3 install virtualenvwrapper

#	Pillow requirements
apt-get install -y libtiff5-dev libjpeg8-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python-tk

#	Scrapy requirements
apt-get install -y python3-lxml

#	apt-get cleanup
apt-get clean


#	python django
pip3 install -r /project/requirements.txt
python3 /project/manage.py migrate
python3 /project/manage.py fill_db


apt-get install supervisor

echo '#########################################################################'
echo '#                                NGINX                                  #'
echo '#########################################################################'

apt-get install -y nginx
sed "s/# \(server_names_hash_bucket_size 64\)/\1/" -i /etc/nginx/nginx.conf
sed "s/# \(gzip_vary\)/\1/"                        -i /etc/nginx/nginx.conf
sed "s/# \(gzip_proxied\)/\1/"                     -i /etc/nginx/nginx.conf
sed "s/# \(gzip_comp_level\)/\1/"                  -i /etc/nginx/nginx.conf
sed "s/# \(gzip_buffers\)/\1/"                     -i /etc/nginx/nginx.conf
sed "s/# \(gzip_http_version\)/\1/"                -i /etc/nginx/nginx.conf
line='text\/css text\/csv text\/html text\/javascript text\/plain text\/xml application\/javascript application\/x-javascript'
sed "s/# \(gzip_types\)[^;]*/\1 $line/"            -i /etc/nginx/nginx.conf

rm /etc/nginx/sites-enabled/default

cp /project/vagrant/nginx/80.conf /etc/nginx/sites-available/
cp /project/vagrant/nginx/8000.conf /etc/nginx/sites-available/

ln -s /etc/nginx/sites-available/80.conf /etc/nginx/sites-enabled/80.conf
ln -s /etc/nginx/sites-available/8000.conf /etc/nginx/sites-enabled/8000.conf

/etc/init.d/nginx restart


echo '#########################################################################'
echo '#                                REDIS                                  #'
echo '#########################################################################'

cd /usr/src
wget http://download.redis.io/redis-stable.tar.gz
tar xvzf redis-stable.tar.gz
cd redis-stable
make
# make test
make install
mkdir -p /etc/redis
mkdir -p /var/redis/6379
cp utils/redis_init_script /etc/init.d/redis_6379
cp redis.conf /etc/redis/6379.conf
sed -e "s|daemonize no|daemonize yes|" \
    -i /etc/redis/6379.conf
sed -e "s|pidfile /var/run/redis\.pid|pidfile /run/redis_6379.pid|" \
    -i /etc/redis/6379.conf
sed -e "s|logfile \"\"|logfile \"/var/log/redis_6379.log\"|" \
    -i /etc/redis/6379.conf
sed -e "s|dir \./|dir /var/redis/6379|" \
    -i /etc/redis/6379.conf
update-rc.d redis_6379 defaults
/etc/init.d/redis_6379 start

mkdir -p /var/redis/6379

print_db_usage