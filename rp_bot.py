#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Maël — outout"
__licence__ = "WTFPL Licence 2.0"


#################
#   IMPORTS     #
#################
from botassets import *
from botassets.imports import *
client = discord.Client()
status = "dnd"
wikipedia.set_lang("fr")

###########################################
#                                         #
#               LOGGER                    #
#                                         #
###########################################
from logging.handlers import RotatingFileHandler
logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s // [%(levelname)s] : %(message)s')
file_handler = RotatingFileHandler('logs/activity.log', 'a', 1000000, 1)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.info(' \n \n New TuxBot instance \n \n')

###########################################
#           OPEN GAME FILE NAME           #
###########################################
game = open('msg/game.txt').read()

#### SQL #####
conn = sqlite3.connect('tuxbot.db') #Connexion SQL

cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
     id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
     userid TEXT,
     username TEXT,
     usermention TEXT,
     histoire TEXT,
     physique TEXT,
     sexe TEXT,
     image TEXT,
     talent TEXT,
     cidate TEXT
)
""")# Creation table Utilisateur si premiere fois
conn.commit()


###########################################
#                                         #
#             ON_READY                    #
#                                         #
###########################################
@client.event
async def on_ready():
    logger.info('BOT READY !')
    print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
    print("TuxBot " + version)
    logger.log(logging.DEBUG, 'TuxBot ' + version)
    print(" ")
    print("Pret ! ")
    print("Vous pouvez l'utiliser.")
    await client.change_presence(game=discord.Game(name=game), status=discord.Status(status), afk=False) ## Game set in config.py
    print("Jeu joué : " + game)
    print("Pseudo : " + client.user.name)
    print("ID : " + client.user.id)
    logger.debug('Bot ID : ' + client.user.id)
    print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")

###########################################
#                                         #
#             JOIN AND LEAVE              #
#                                         #
###########################################
@client.event
async def on_member_join(member):
    logger.log(logging.INFO, member.name + ' joined the server !')
    server = member.server
    prv = await client.start_private_message(member)
    welcome_msg = random.choice(arrays.wlcm_msgs)
    if member.server.name == "Aide GNU/Linux-fr":
        fmt = 'Bienvenue {0.mention} sur le suberbe serveur discord **' + member.server.name + '** ! Je te conseil de lire #regles pour commencer et te créer une fiche-rp dans ``#fiche_personnage`` grâce à la commande ``.ci-register`` et la personnaliser :smile: !'
    else:
        fmt = 'Bienvenue {0.mention} sur le discord **'+ member.server.name +'**, j\'espère que tu passeras un bon moment avec nous !' ##Multi-Server
    await client.send_message(prv, fmt.format(member))
    await client.send_message(member.server.default_channel, "**{0}**".format(welcome_msg.format(member)))

@client.event
async def on_member_remove(member):
    adios_msg = random.choice(arrays.adios_msgs)
    logger.log(logging.INFO, member.name + ' left the server !')
    await client.send_message(member.server.default_channel, "**{0}**".format(adios_msg.format(member)))
###########################################
#                                         #
#             DELETE MESSAGE              #
#                                         #
###########################################
@client.event
async def on_message_delete(message):
    if not message.channel.is_private and not message.author.bot:
        msg_log = open('logs/deleted_msg.log', 'a')
        date = time.localtime(time.time())
        msg_log.write(str(message.author.name) + " (" + message.author.id + ")\n")
        msg_log.write("  -> serveur : " + message.server.name + " \n")
        msg_log.write("  -> date    : " + str(time.strftime("%d %b %Y %H:%M:%S", date)) + "\n")
        msg_log.write("  -> message : " + str(message.content) + "\n")
        msg_log.write("--------------------------------------------------------------------------------------------------\n")
        msg_log.close()

@client.event
async def on_message(message):
###########################################
#                                         #
#             CUSTOMS FUNCTIONS           #
#              BLOCKING AND ...           #
#                                         #
###########################################
    roles = ["bot-commander", "Admin", "Admin test"]
    role = message.author.roles

    def cmd(cmd_name):
        if not message.channel.is_private and not message.author.bot:
            return message.content.startswith(prefix + cmd_name)

    def authadmin():
        role = message.author.roles
        print("A")
        try:
            if str(role[0]) in roles or str(role[1]) in roles or str(role[2]) in roles or str(role[3]) in roles or str(role[4]) in roles:
                return True
            else:
                return False
        except IndexError:
            return False

    def civerify(argu):
        if not argu:
            return("Non renseigné")
        else:
            return(argu)


    if message.channel.is_private and not message.author.bot:
        await client.send_message(message.channel, "Désolé mais mon papa m'a dit de ne pas parler par Message Privé, viens plutot sur un serveur discord !")


###########################################
#                                         #
#                ADMIN COMMANDS           #
#                                         #
###########################################

    if cmd("sendlogs"):
        if str(role[0]) in roles or str(role[1]) in roles or str(role[2]) in roles or str(role[3]) in roles or str(role[4]) in roles:
            wait = await client.send_message(message.channel, message.author.mention + " Le contenue du fichier log est entrain d'être envoyé... Veuillez patienter, cela peut prendre du temps !")
            await client.send_file(message.author, fp="logs/activity.log", filename="activity.log", content="Voci mon fichier ``activity.log`` comme demandé !", tts=False)
            await client.edit_message(wait, message.author.mention + " C'est bon vous venez de recevoir par message privé mon fichier de logs")
        else:
            await client.send_message(message.channel, "[**ERREUR**] Vous n'avez pas la permission d'executer cette commande")

    elif cmd("say"): #Control
        if str(role[0]) in roles or str(role[1]) in roles or str(role[2]) in roles or str(role[3]) in roles or str(role[4]) in roles:
            try:
                args = message.content.split("say ")
                await client.send_message(message.channel, args[1])
                logger.info(message.author.name + ' ordered TuxBot to say : ' + args[1])
                await client.delete_message(message)
            except IndexError:
                await client.send_message(message.author, "**[ERREUR]** Merci de fournir le paramètre du message à dire, je ne suis pas dans ta tête !")
                await client.delete_message(message)
        else:
            await client.send_message(message.channel, message.author.mention + "[**ERREUR**] Vous n'avez pas la permission d'executer cette commande")

##############
#Listing    #
#############
    elif cmd("servers-list"):
        nbmr = 0
        msg = ""
        for serveur in list(client.servers):
            nbmr = nbmr + 1
            msg = msg + "=> **{}** \n".format(serveur.name)
        msg = msg + "{} se trouve sur **{} serveur(s)** au total !".format(client.user.name, nbmr)
        em = discord.Embed(title='Liste des serveurs où se trouve ' + client.user.name, description=msg, colour=0x36D7B7)
        em.set_author(name=client.user.name, icon_url=client.user.avatar_url)
        await client.send_message(message.channel, embed=em)

    elif cmd("count-members"):
        nbmr = 0
        for name in list(client.get_all_members()):
            nbmr = nbmr + 1
        msg = "Il y'a **{} membres** sur le serveur Discord **{}**".format(nbmr, message.server.name)
        em = discord.Embed(title='Compteur de membres', description=msg, colour=0x9A12B3)
        await client.send_message(message.channel, embed=em)

###################
# IDENTIY SYSTEM  #
###################

    elif cmd("perso-register"):
        cursor.execute("""INSERT INTO users(userid, username, usermention, cidate) VALUES(?, ?, ?, ?)""", (message.author.id, message.author.name, message.author.mention, message.timestamp))
        conn.commit()
        await client.send_message(message.channel, message.author.mention + "> **Votre fiche personnage à été enregistrée !** Pour la modifier et obtenir plus d'informations sur les fiches personnage tapez la commande ``{}perso-info`` !".format(prefix))

    elif cmd("perso-settalent"):
        try:
            args = message.content.split("perso-settalent ")
            cursor.execute("""UPDATE users SET talent = ? WHERE usermention = ?""", (args[1], message.author.mention))
            conn.commit()
            await client.send_message(message.channel, message.author.mention + " l'information à bien été modifié sur votre carte d'identité !")
        except IndexError:
            await client.send_message(message.channel, message.author.mention + " [**ERREUR**] : Veuillez argumenter la commande !")

    elif cmd("perso-setphysique"):
        try:
            args = message.content.split("perso-setphysique ")
            cursor.execute("""UPDATE users SET physique = ? WHERE usermention = ?""", (args[1], message.author.mention))
            conn.commit()
            await client.send_message(message.channel, message.author.mention + " l'information à bien été modifié sur votre carte d'identité !")
        except IndexError:
            await client.send_message(message.channel, message.author.mention + " [**ERREUR**] : Veuillez argumenter la commande !")

    elif cmd("perso-sethistoire"):
        try:
            args = message.content.split("perso-sethistoire ")
            cursor.execute("""UPDATE users SET histoire = ? WHERE usermention = ?""", (args[1], message.author.mention))
            conn.commit()
            await client.send_message(message.channel, message.author.mention + " l'information à bien été modifié sur votre carte d'identité !")
        except IndexError:
            await client.send_message(message.channel, message.author.mention + " [**ERREUR**] : Veuillez argumenter la commande !")

    elif cmd("perso-setimage"):
        try:
            args = message.content.split("perso-setimage ")
            cursor.execute("""UPDATE users SET image = ? WHERE usermention = ?""", (args[1], message.author.mention))
            conn.commit()
            await client.send_message(message.channel, message.author.mention + " l'information à bien été modifié sur votre carte d'identité !")
        except IndexError:
            await client.send_message(message.channel, message.author.mention + " [**ERREUR**] : Veuillez argumenter la commande !")

    elif cmd("perso-setsexe"):
        try:
            args = message.content.split("perso-setsexe ")
            cursor.execute("""UPDATE users SET sexe = ? WHERE usermention = ?""", (args[1], message.author.mention))
            conn.commit()
            await client.send_message(message.channel, message.author.mention + " l'information à bien été modifié sur votre carte d'identité !")
        except IndexError:
            await client.send_message(message.channel, message.author.mention + " [**ERREUR**] : Veuillez argumenter la commande !")


    elif cmd("perso-info"):
        cinfomd = open('msg/perso-info.md').read()
        em = discord.Embed(title='Aide sur les fiches personnage', description=cinfomd.format(prefix), colour=0xDEADBF)
        await client.send_message(message.channel, embed=em)

    elif cmd("perso"):
        try:
            args = message.content.split("perso ")
            cursor.execute("""SELECT userid, username, histoire, physique, sexe, image, talent FROM users WHERE usermention=?""", (args[1],))
            result = cursor.fetchone()
            if not result:
                await client.send_message(message.channel, message.author.mention + "> Désolé mais {} n'a pas fait enregistrer sa fiche personnage".format(args[1]))
            else:
                userid = result[0]
                username = result[1]
                histoire = civerify(result[2])
                physique = civerify(result[3])
                sexe = civerify(result[4])
                image = civerify(result[5])
                talent = civerify(result[6])
                em_content = open('msg/identity.md').read()
                em = discord.Embed(title='Fiche Perso de '+ username, description=em_content.format(username, histoire, physique, sexe, image, talent), colour=0xDEADBF)
                await client.send_message(message.channel, embed=em)
        except IndexError:
            await client.send_message(message.channel, message.author.mention + " [**ERREUR**] : Veuillez argumenter la commande !")

###########################################
#                                         #
#          HELP AND FIX COMMANDS          #
#                                         #
###########################################
    elif cmd('help'): ##HELP
        await client.send_typing(message.channel)
        text = open('msg/help.md').read()
        em = discord.Embed(title='Liste des Commandes', description=text.format(prefix), colour=0x89C4F4)
        await client.send_message(message.channel, embed=em)

    elif cmd("info"): ##info
        text = open('msg/info.md').read()
        em = discord.Embed(title='Informations sur ' + client.user.name, description=text, colour=0x89C4F9)
        await client.send_message(message.channel, embed=em)

    elif cmd('github'): ##Link to github
        await client.send_typing(message.channel)
        text = "Le bot est basé sur un autre bot discord du nom de TuxBot développé par la même personne, tu peux voir son code ici => !\n https://github.com/outout14/tuxbot-bot"
        em = discord.Embed(title='Repos TuxBot-Bot', description=text, colour=0xE9D460)
        em.set_author(name='Outout', icon_url="https://avatars0.githubusercontent.com/u/14958554?v=3&s=400")
        await client.send_message(message.channel, embed=em)


###########################################
#                                         #
#          AUTOMATICS FUNCTIONS           #
#                                         #
###########################################
    if message.content == message.content.upper() and not message.author.bot:
        if len(message.content) > 5:
            await client.send_message(message.channel, message.author.mention + " pas que des capitales dans ton message quand même !")

client.run(token)
