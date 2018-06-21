
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

cp /webapp/vagrant/80.conf /etc/nginx/sites-available/
cp /webapp/vagrant/8000.conf /etc/nginx/sites-available/

ln -s /etc/nginx/sites-available/80.conf /etc/nginx/sites-enabled/80.conf
ln -s /etc/nginx/sites-available/8000.conf /etc/nginx/sites-enabled/8000.conf

/etc/init.d/nginx restart