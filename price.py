import api
import discord
import json

base_url = "https://www.vinmonopolet.no"

class PriceView(discord.ui.View):
    page = 1

    @discord.ui.button(label="previous", style=discord.ButtonStyle.primary)
    async def previous(self, interaction: discord.Interaction, button: discord.ui.Button):

        if self.page <= 1:
            self.page = api.total_pages
        else: 
            self.page -= 1
        embed = priceEmbed(self.page)
        await interaction.response.edit_message(embed=embed)


    @discord.ui.button(label="next", style=discord.ButtonStyle.primary)
    async def next(self, interaction: discord.Interaction, button: discord.ui.Button):

        if self.page >= api.total_pages:
            self.page = 1
        else:
            self.page += 1 
        embed = priceEmbed(self.page)
        await interaction.response.edit_message(embed=embed)


def priceEmbed(page: int):
    products = load_products_from_json("lowPrice.json")
    embed = discord.Embed(
        title=f"**Price | Cheapest items | Page {page}**",
        color=discord.Color.green()
    )

    # Fetch the products for the current page
    page_items = products[(page - 1) * 10: min((page) * 10, len(products))]
    
    for i, product in enumerate(page_items):
        # Link the product name in the field value
        linked_name = f"[{product['name']}]({base_url + product['sufix']})"
        image_link = f"[Image]({product['image']})" if product["image"] else "No Image Available"
            
        # Add a field with the hyperlink in the value (not the name)
        embed.add_field(
            name=f"Number: {((page -1) * 10) + i + 1}",
            value=(
                f"**Product**: {linked_name}\n"
                f"**Alcohol**: {product['alcohol']}%\n"
                f"**Price**: {product['price']} NOK\n"
                f"**Raw Alcohol Price**: {product['rawAlcoholPrice']} NOK/L\n"
                f"**Volume**: {product['volume']}cl\n"
                f"{image_link}\n"
                f"{'**Unavailable**' if not product['buyable'] else ''}" 
            ),                
            inline=True  # Use inline=True to display in rows
        )
        
        
        # Insert a blank field every 2 products to create spacing between rows
        if (i + 1) % 2 == 0:
            embed.add_field(name="\u200b", value="\u200b", inline=False)

    return embed

# Function to load data from the JSON file
def load_products_from_json(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)
