pyc:
	find . -name \*.pyc -delete
	find . -name __pycache__ -delete

flush:
	echo "flush_all" | nc -w 2 localhost 11211

restart:
	sudo systemctl restart spirsa
	sudo systemctl restart nginx
