<h3> Описание проекта </h3>
Team Flame Bot - это интеграция web версиии с приложением telegram, теперь управлять своим проектом можно через уоманды бота. Для использования бота нужно пройти регистрацию/авторизацию после чего открываются все возможности управления задачами Team Flame. Присутсвуют такие команды, как создание Пространсва/проекта/задач, а так же взаимодействия с ними.

<h3> Перед запуском </h3>

```
git clone https://github.com/alex-s2222/integration_team_flame_bots.git
```

```
cd integration_team_flame_bots/tg_bot
```

В Dockerfile изменить: <br>
#TOKEN -> YOU-TOKEN (Полученный у BotFather)

<h3>Запуск приложения</h3>

```
docker bild -t team_flame_bot
```

```
docker run -d team_flame_bot
```