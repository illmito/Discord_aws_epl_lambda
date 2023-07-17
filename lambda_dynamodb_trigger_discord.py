import json
import requests
from DiscordEmbed import DiscordEmbed
import random

numbers = [15861084, 3407936, 520946, 389740, 15397381]
color = random.choice(numbers)


def embed_thumbnail(fthg, ftag, home_team, away_team):
    logo = 'epllogo'

    if int(fthg) > int(ftag):
        logo = home_team
    elif int(fthg) < int(ftag):
        logo = away_team

    return logo


def lambda_handler(event, context):
    if event['Records'][0]['eventName'] == 'INSERT':
        new_item = event['Records'][0]['dynamodb']['NewImage']
        json_data = json.dumps(new_item)

        data = json.loads(json_data)

        date = data['Date']['S']
        home_team = data['HomeTeam']['S']
        fthg = data['FTHG']['N']
        away_team = data['AwayTeam']['S']
        ftag = data['FTAG']['N']

        thumbnail = embed_thumbnail(fthg, ftag, home_team, away_team)
        # thumbnail will not print with space in name. below ads in %20 to allow to work.
        club_logo = thumbnail.replace(" ", "%20")

        embed = DiscordEmbed(title="", description="", color=color,
                             thumbnail=f'https://discordfootball.s3.amazonaws.com/logos/{thumbnail}.png',
                             footer=date)

        embed.add_field(name=f"**{home_team}**", value=f"> {fthg}")
        embed.add_field(name=f"**{away_team}**", value=f"> {ftag}", inline=True)

        discord_embed = embed.build()

        send_json_data(discord_embed)

        return {
            'statusCode': 200,
            'body': 'JSON data saved successfully.'
        }

    return {
        'statusCode': 200,
        'body': 'No action required.'
    }


def send_json_data(json_data):
    token = ''
    channel_id = ''

    message_content = json_data

    url = f'https://discord.com/api/channels/{channel_id}/messages'

    headers = {
        'Authorization': f'Bot {token}',
        'Content-Type': 'application/json'
    }

    payload = {
        'content': '',
        'embed': json_data
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        print('Message posted successfully.')
    else:
        print('Failed to post message. Error:', response.text)

    print(f"JSON Data: {json_data}")
