import discord
from discord.ext import commands

# définit le préfixe pour utiliser les commandes
bot = commands.Bot(command_prefix='/')

@bot.command(name='create_tournament', help='Crée un nouveau tournoi sur le serveur')
@commands.has_permissions(administrator=True)
async def create_tournament(ctx):
    # Vérifie les permissions de l'utilisateur
    if not ctx.message.author.guild_permissions.administrator:
        await ctx.send("Vous n'avez pas les permissions nécessaires pour utiliser cette commande.")
        return

    # Récupère le serveur et le nom du tournoi
    server = ctx.message.guild
    tournament_name = "Tournoi"

    # Crée un nouveau rôle pour les joueurs inscrits
    tournament_role = await server.create_role(name=tournament_name + " Joueurs")

    # Crée les catégories et les salons pour le tournoi
    category1 = await server.create_category(name=tournament_name + " - Partie 1")
    category2 = await server.create_category(name=tournament_name + " - Partie 2")

    announcements = await server.create_text_channel(name="annonces", category=category1)
    rules_and_registration = await server.create_text_channel(name="règles_et_inscription", category=category1)
    chat = await server.create_text_channel(name="chat", category=category2)
    bracket = await server.create_text_channel(name="bracket", category=category2)
    results = await server.create_text_channel(name="résultats", category=category2)
    admin = await server.create_text_channel(name="admin", category=category2)

    # Définit les permissions pour chaque salon
    # Announcements et rules_and_registration seulement visible pour les administrateurs
    await announcements.set_permissions(server.default_role, read_messages=False)
    await announcements.set_permissions(server.get_role(server.roles), read_messages=True)
    await rules_and_registration.set_permissions(server.default_role, read_messages=False)
    await rules_and_registration.set_permissions(server.get_role(server.roles), read_messages=True)

    # Chat, bracket et results seulement visible pour le rôle du tournoi
    await chat.set_permissions(server.default_role, read_messages=False)
