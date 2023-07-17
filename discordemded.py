class DiscordEmbed:
    def __init__(self, title=None, description=None, color=None, thumbnail=None, footer=None):
        self.title = title
        self.description = description
        self.color = color
        self.fields = []
        self.thumbnail = thumbnail
        self.footer = footer

    def add_field(self, name, value, inline=True):
        self.fields.append({"name": name, "value": value, "inline": inline})

    def build(self):
        embed = {
            "title": self.title,
            "description": self.description,
            "color": self.color,
            "fields": self.fields,
            "thumbnail": {"url": self.thumbnail} ,
            "footer": {"text": self.footer}
        }
        return embed
