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