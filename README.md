docker-compose up -d  
docker exec sberparser python3 /home/app/main.py -f urls_file.txt -p pause_int --proxies proxies_list_file.txt
