def parse_scope(scope):
    args_list = scope.split(' ')
    return '+'.join(args_list)

def check_for_guild(guilds, allowed_guild_id):
    for guild in guilds:
        if int(guild['id']) == allowed_guild_id:
            return True, {"id": guild['id'], "name": guild['name']}
    return False, None
