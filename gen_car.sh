ip_intersection=$1
while sleep $[ ( $RANDOM % 10 )  + 1 ]s; do
	time_id=$(date +%s)
	choose_car=`shuf -e 0 1 -n 1`
#	id=`shuf -i 1-4 -n 1`
	if [ $choose_car -eq "0" ]; then
		pos_inicial="0,-300"
		vel_inicial="40,0"
	else
		pos_inicial="300,0"
		vel_inicial="0,-40"
	fi
	screen -S car_$time_id -dm python ~/TrayectoriaCarro.py $time_id $pos_inicial $vel_inicial $ip_intersection
done

