docker-compose up -d  
docker exec sberparser python3 /home/app/main.py -f urls_file.txt -p pause_int --proxy socks5://username:password@host:port
