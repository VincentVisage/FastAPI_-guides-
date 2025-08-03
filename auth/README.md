Команда для создания секретного ключа
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
openssl genrsa -out jwt-private.pem 2048

Команда для создания публичного ключа
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
openssl rsa -pubout -in private_key.pem -out public_key.pem
