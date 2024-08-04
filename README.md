# test_to_veklich
(инструкция для linux)
1. убедитесь что у вас установлен docker и docker-compose
2. установите git
3. скопируйте содержимое репозитория в папку в которой буде работать
   git clone <url> 
4. Для корректной работы Redis выполните 2 комманды
   add 'vm.overcommit_memory = 1' to /etc/sysctl.conf and then reboot or run the command 'sysctl vm.overcommit_memory=1' for this to take effect.
5. В папке бот создайте файл config.py
BOT_TOKEN=<токен вашего бота>
6. Замените ip адрес на свой в конфигурации nginx и handlers.py бота
7. sudo docker-compose up --build