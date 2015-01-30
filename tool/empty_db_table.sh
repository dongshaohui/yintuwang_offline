HOST="rdsjjuvbqjjuvbqout.mysql.rds.aliyuncs.com"
PORT="3306"
USER="dongsh"
PWD="5561225"
mysql -hrdsjjuvbqjjuvbqout.mysql.rds.aliyuncs.com -P3306 -udongsh  -p5561225 <<EOF
	use financal_product;
	delete from $1;
EOF
