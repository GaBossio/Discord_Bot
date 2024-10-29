import asyncio
from datetime import timedelta

import nextcord as discord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands

import random
from utils_common import CustomContext
from utils_common import get_random_response
from keys import TEST_GUILD_ID


class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client

    @discord.slash_command(name="duelo", description="Reta a un miembro a un duelo", guild_ids=[TEST_GUILD_ID])
    async def duel(self,
                   interaction: Interaction,
                   oponente: discord.Member = SlashOption(description="Miembro a retar", required=True),
                   silenciado: bool = SlashOption(description="Invocar al coro para el duelo?", default=False,
                                                  required=False)):
        # Enviar mensaje inicial invitando al oponente al duelo
        await interaction.response.send_message(
            f"{oponente.mention}, {interaction.user.mention} te ha desafiado al duelo sagrado."
            f"\n\nReacciona para aceptar o rechazar el desafío."
        )
        # Obtener el mensaje de respuesta completo
        duel_invite_message = await interaction.original_message()
        await duel_invite_message.add_reaction("✅")
        await duel_invite_message.add_reaction("❌")

        # Check if the bot is muted
        if not silenciado:

            # Get the `play` command from the Music cog
            play_command = self.client.get_command("play_now")
            ctx = CustomContext(interaction)
            if play_command:
                await play_command(ctx, 'Duel', 'True')  # Call the play command with context and arguments
            else:
                print("Play command not found.")

        def check(reaction, user):
            return (
                    user == oponente
                    and str(reaction.emoji) in ["✅", "❌"]
                    and reaction.message.id == duel_invite_message.id
            )

        try:
            reaction, _ = await self.client.wait_for("reaction_add", timeout=60.0, check=check)

            if str(reaction.emoji) == "✅":
                response = get_random_response("actions", "duel_accept")
                await interaction.channel.send(
                    f"{response}\n\nOponente: **{oponente.display_name}** ha aceptado el duelo."
                )

                # Add countdown for suspense
                await interaction.channel.send("El duelo comienza en 3...")
                await asyncio.sleep(1)
                await interaction.channel.send("2...")
                await asyncio.sleep(1)
                await interaction.channel.send("1...")
                await asyncio.sleep(1)
                await interaction.channel.send("¡Que comience el duelo!")
                await interaction.channel.send(
                    "--------------------------------------------------------------------------")

                # Duel mechanics: Health bars and rounds
                user_health = ["❤", "❤", "❤"]
                opponent_health = ["❤", "❤", "❤"]

                # Assume user_health and opponent_health are lists containing the health state, e.g. ["❤️", "❤️", "❤️"] for 3 lives
                while user_health and opponent_health:
                    await asyncio.sleep(1)
                    async with interaction.channel.typing():
                        # Select the attacker randomly
                        attacker = random.choice([interaction.user, oponente])
                        defender = oponente if attacker == interaction.user else interaction.user

                        # Describe attacks with random outcomes
                        attack_dialogues = random.choice([
                            f"**{attacker.display_name}** desata una furia oscura, golpeando con la ira del Consejo...",
                            f"**{attacker.display_name}** canaliza la voluntad del Consejo y se lanza a la carga, como una sombra vengativa...",
                            f"**{attacker.display_name}** invoca un golpe envuelto en penumbra, impactando con precisión oscura...",
                            f"Con la determinación de los fieles, **{attacker.display_name}** avanza y asesta un golpe implacable...",
                            f"Con un grito que resuena en el vacío, **{attacker.display_name}** lanza un ataque que tiembla la tierra...",
                            f"Imbuido de la ira del Consejo, **{attacker.display_name}** lanza un golpe que desafía las leyes mortales...",
                            f"**{attacker.display_name}** clama al Consejo por fuerza y desata un ataque que retumba en el abismo...",
                            f"Como una sombra desatada, **{attacker.display_name}** ataca sin misericordia, su golpe resuena en la oscuridad..."
                        ])

                        await asyncio.sleep(1.5)
                        await interaction.channel.send(attack_dialogues)

                        # Deflect chance: 30% probability to deflect the attack
                        deflect_chance = random.random() < 0.3

                        # Dialogue outcomes for defender when deflecting
                        deflect_dialogues = [
                            f"El ataque de **{attacker.display_name}** falla cuando **{defender.display_name}** ejecuta un impresionante contraataque de defensa.",
                            f"Con una agilidad sobrenatural, **{defender.display_name}** desvía el golpe de **{attacker.display_name}**, dejando solo sombras tras de sí.",
                            f"**{defender.display_name}** levanta su guardia, y el ataque de **{attacker.display_name}** se desvanece como un susurro en la penumbra.",
                            f"**{defender.display_name}** responde con una defensa magistral, el ataque de **{attacker.display_name}** queda atrapado en el vacío.",
                            f"Un brillo de determinación ilumina los ojos de **{defender.display_name}**, que desbarata el ataque de **{attacker.display_name}** con un movimiento sublime.",
                            f"Con la sabiduría del Consejo, **{defender.display_name}** anticipa el ataque de **{attacker.display_name}**, eludiéndolo con destreza.",
                            f"**{defender.display_name}** invoca la protección del Consejo y el ataque de **{attacker.display_name}** se detiene en seco, impotente.",
                            f"Con la calma de un anciano del Consejo, **{defender.display_name}** neutraliza el ataque de **{attacker.display_name}** con un giro preciso."
                        ]

                        # Determine if the defender deflects or takes damage
                        if deflect_chance:
                            deflect_message = random.choice(deflect_dialogues)
                            await interaction.channel.send(deflect_message)
                        else:
                            # Apply damage if the attack is not deflected
                            if defender == oponente:
                                if opponent_health:
                                    opponent_health.pop()
                                    # Check if opponent has lost all health
                                    if not opponent_health:
                                        await interaction.channel.send(
                                            f"**{oponente.display_name}** ha sido derrotado! ☠")
                                        break  # End duel if opponent is defeated
                                    else:
                                        await interaction.channel.send(
                                            f"**{oponente.display_name}** pierde fuerzas: {''.join(opponent_health)}")
                            else:
                                if user_health:
                                    user_health.pop()
                                    # Check if user has lost all health
                                    if not user_health:
                                        await interaction.channel.send(
                                            f"**{interaction.user.display_name}** ha sido derrotado! ☠")
                                        break  # End duel if user is defeated
                                    else:
                                        await interaction.channel.send(
                                            f"**{interaction.user.display_name}** pierde fuerzas: {''.join(user_health)}")

                # Announce the winner
                if user_health:
                    await interaction.channel.send(
                        '--------------------------------------------------------------------------')
                    await interaction.channel.send(
                        f"\n\n¡El duelo ha terminado! **{interaction.user.display_name}** ha ganado.")
                    loser = oponente
                else:
                    await interaction.channel.send(
                        '--------------------------------------------------------------------------')
                    await interaction.channel.send(f"¡El duelo ha terminado! **{oponente.display_name}** ha ganado.")
                    loser = interaction.user

                # Timeout the loser as punishment
                timeout_duration = timedelta(minutes=5)
                try:
                    await loser.timeout(timeout_duration)
                    await interaction.channel.send(
                        f"{loser.display_name} ha sido castigado a aislamiento por 5 minutos.")
                except discord.Forbidden:
                    await interaction.channel.send("No tengo permisos para hacer timeout a este miembro.")
                except discord.HTTPException as e:
                    await interaction.channel.send(f"Error al aplicar timeout a {loser.display_name}: {e}")

            else:
                response = get_random_response("actions", "duel_reject")
                await interaction.channel.send(
                    f"{response}\n\nOponente: **{oponente.display_name}** ha rechazado el duelo."
                )

        except asyncio.TimeoutError:
            response = get_random_response("actions", "duel_timeout")
            await interaction.followup.send(
                f"{response}\n\nOponente: **{oponente.display_name}** no respondió a tiempo."
            )


def setup(client, db):
    client.add_cog(Fun(client))
