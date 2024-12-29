# VinmonopoletDiscord

**This project is heavily inspired by spritjakt.no**

This is a Discord app to query Vinmonopolets products.

The app can post paged embeds for cheapest products, largest buy volume and lowest price per raw alcohol.

### Commads

```/student``` Returns products from Vinmonopolet, 10 at a time, sorted by the raw alcohol price.

```/price``` Returns products from Vinmonopolet, 10 at a time, sorted by the lowest price.

```/largest``` Returns products from Vinmonopolet, 10 at a time, sorted by the product's volume.


### Exsisting running bot to use:

https://discord.com/oauth2/authorize?client_id=1321879506981617724&permissions=8&integration_type=0&scope=bot

### Use the code 

To be able to run the code yourself you will have to run:

- pip install discord.py
- pip install requests
- pip install python-dotenv


you will have to create a .env file and add "DISCORD_TOKEN=TOKEN" with your Discord app token. 