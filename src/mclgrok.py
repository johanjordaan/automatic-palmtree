TIME = "\\[(?P<time>\\d\\d:\\d\\d:\\d\\d)\\]"
THREAD_LEVEL = "\\[(?P<thread>.*)\/(?P<level>.*)\\]"
IP = "(?P<ip>\\d*\\d*\\d+\.\\d*\\d*\\d+\.\\d*\\d*\\d+\.\\d*\\d*\\d+)"
PORT = "(?P<port>\\d+)"
def COORDINATE(name):
    return f'(?P<{name}>-*\\d*\.\\d+)'
COORDINATES = f"{COORDINATE('x')},[ ]*{COORDINATE('y')},[ ]*{COORDINATE('z')}"
COUNT = "\\d+"
DISTANCE = "\\d+"
def BLOCK_COORDINATE(name):
    return f'(?P<{name}>(-*\\d+)|~)'
BLOCK_COORDINATES = f"{BLOCK_COORDINATE('x')},[ ]*{BLOCK_COORDINATE('y')},[ ]*{BLOCK_COORDINATE('z')}"
PLAYER_NAME = "(?P<player_name>[A-Za-z0-9_]+)"
SHORT_HASH = "[a-z\\d]+"
NPC_TYPE = "(?P<npc_type>[A-Za-z0-9_]+)"


patterns = [
    ## Help and interactiove input
    #
    #[07:43:18] [Server thread/INFO]: /advancement (grant|revoke)
    {'type': 'help', 'pattern': f'{TIME} {THREAD_LEVEL}: /(?P<command>[A-Za-z0-9_-]+) (?P<params>.*)'},
    #[07:43:18] [Server thread/INFO]: /reload
    {'type': 'help', 'pattern': f'{TIME} {THREAD_LEVEL}: /(?P<command>[A-Za-z0-9_-]+)'},

    ## Exceptions
    #
    #[09:53:14] [Server console handler/ERROR]: Exception handling console input
    {'type': 'exception', 'pattern': f'{TIME} {THREAD_LEVEL}: Exception handling console input'},
    {'type': 'exception_line', 'pattern': f'java.io.IOException: '},        # TODO Capture actual line info
    {'type': 'exception_line', 'pattern': f'[ \\t]*at .*'},                 # TODO Capture actual line info

    ## warnings
    # [20:09:43] [Server thread/WARN]: Horse (vehicle of UnicornTaimer) moved wrongly! 0.42138890999933665
    {'type': 'warning', 'pattern': f'{TIME} {THREAD_LEVEL}: Horse \(vehicle of {PLAYER_NAME}\) moved wrongly!'},

    # [13:45:22] [ServerMain/WARN]: Ambiguity between arguments [teleport, location] and [teleport, destination] with inputs: [0.1 -0.5 .9, 0 0 0]
    {'type': 'warning', 'pattern': f'{TIME} {THREAD_LEVEL}: (?P<message>Ambiguity between arguments .*)'},

    #[07:45:25] [Server thread/WARN]: Skrag001 moved too quickly! -1021.7776033719905,26.149999982118608,-437.83710108435537
    {'type': 'warning', 'pattern': f'{TIME} {THREAD_LEVEL}: {PLAYER_NAME} moved too quickly! {COORDINATES}'},

    #[19:40:56] [Server thread/WARN]: handleDisconnection() called twice
    {'type': 'warning', 'pattern': f'{TIME} {THREAD_LEVEL}: handleDisconnection\(\) called twice'},

    #[19:28:45] [Server thread/INFO]: Unknown or incomplete command, see below for error
    {'type': 'warning', 'pattern': f'{TIME} {THREAD_LEVEL}: Unknown or incomplete command, see below for error'},

    #[19:28:45] [Server thread/INFO]: <--[HERE]
    {'type': 'warning', 'pattern': f'{TIME} {THREAD_LEVEL}: <--\[HERE\]'},

    #[07:46:57] [Server thread/INFO]: No player was found
    {'type': 'warning', 'pattern': f'{TIME} {THREAD_LEVEL}: No player was found'},

    ## Server startup
    ##

    #[13:45:47] [Server thread/INFO]: Preparing start region for dimension minecraft:overworld
    {'type': 'preparing_start_region', 'pattern': f'{TIME} {THREAD_LEVEL}: Preparing start region for dimension (?P<name>.*)'},

    #[13:45:36] [Server thread/INFO]: Preparing level "world"
    {'type': 'preparing_world', 'pattern': f'{TIME} {THREAD_LEVEL}: Preparing level \"(?P<name>.*)\"'},

    #[13:45:50] [Worker-Main-14/INFO]: Preparing spawn area: 0%
    {'type': 'preparing_spawn_area', 'pattern': f'{TIME} {THREAD_LEVEL}: Preparing spawn area: (?P<percentage>[\d]+)%'},

    #[13:45:35] [Server thread/INFO]: Starting minecraft server version 1.18
    {'type': 'server_start', 'pattern': f'{TIME} {THREAD_LEVEL}: Starting minecraft server version (?P<version>[\d]+\.[\d]+)'},

    #[13:45:36] [Server thread/INFO]: Starting Minecraft server on *:25565
    {'type': 'server_port', 'pattern': f'{TIME} {THREAD_LEVEL}: Starting Minecraft server on \*:(?P<port>[\d]+)'},

    #[13:46:32] [Server thread/INFO]: Done (55.762s)! For help, type "help"
    {'type': 'server_ready', 'pattern': f'{TIME} {THREAD_LEVEL}: Done \((?P<startup_time>[\d]+\.[\d]+)s\)! For help, type "help"'},

    #[13:46:47] [Server thread/INFO]: Stopping server
    {'type': 'server_stop', 'pattern': f'{TIME} {THREAD_LEVEL}: Stopping server'},

    #[13:46:32] [Server thread/INFO]: Time elapsed: 45280 ms
    {'type': 'run_time', 'pattern': f'{TIME} {THREAD_LEVEL}: Time elapsed: (?P<elapsed_time>\d+) ms'},

    #[13:45:21] [ServerMain/INFO]: Environment: authHost='https://authserver.mojang.com', accountsHost='https://api.mojang.com', sessionHost='https://sessionserver.mojang.com', servicesHost='https://api.minecraftservices.com', name='PROD'
    {'type': 'environment', 'pattern': f'{TIME} {THREAD_LEVEL}: Environment: (?P<environment>.*)'},

    #[13:46:47] [Server thread/INFO]: ThreadedAnvilChunkStorage (world): All chunks are saved
    {'type': 'saved', 'pattern': f'{TIME} {THREAD_LEVEL}: ThreadedAnvilChunkStorage \((?P<level_code>.*)\): All (?P<object>[A-Za-z0-9_]+) are saved'},

    # [13:46:47] [Server thread/INFO]: ThreadedAnvilChunkStorage: All dimensions are saved
    {'type': 'saved', 'pattern': f'{TIME} {THREAD_LEVEL}: ThreadedAnvilChunkStorage: All (?P<object>[A-Za-z0-9_]+) are saved'},

    # [13:46:47] [Server thread/INFO]: Saving chunks for level 'ServerLevel[world]'/minecraft:the_end
    {'type': 'saving', 'pattern': f'{TIME} {THREAD_LEVEL}: Saving (?P<object>.*) for level (?P<level_name>.*)'},

    #[13:46:47] [Server thread/INFO]: Saving players
    {'type': 'saving', 'pattern': f'{TIME} {THREAD_LEVEL}: Saving (?P<object>\w)'},

    #[13:45:22] [Worker-Main-12/INFO]: Loaded 7 recipes
    {'type': 'loaded', 'pattern': f'{TIME} {THREAD_LEVEL}: Loaded (?P<count>\d+) (?P<object>.*)'},

    #[13:45:35] [Server thread/INFO]: Loading properties
    {'type': 'loading', 'pattern': f'{TIME} {THREAD_LEVEL}: Loading (?P<object>.*)'},


    #[13:45:35] [Server thread/INFO]: Generating keypair
    {'type': 'generating', 'pattern': f'{TIME} {THREAD_LEVEL}: Generating (?P<object>.*)'},

    #[13:45:36] [Server thread/INFO]: Using default channel type
    {'type': 'using', 'pattern': f'{TIME} {THREAD_LEVEL}: Using (?P<name>[A-Za-z0-9_]+) (?P<object>.*)'},

    #[13:45:35] [Server thread/INFO]: Default game type: SURVIVAL
    {'type': 'default_game_type', 'pattern': f'{TIME} {THREAD_LEVEL}: Default game type: (?P<game_type>.*)'},

    # [13:45:22] [ServerMain/INFO]: Reloading ResourceManager: Default
    {'type': 'reloading', 'pattern': f'{TIME} {THREAD_LEVEL}: Reloading (?P<object>[A-Za-z0-9_]+): (?P<name>.*)'},


    ## Events after startup
    #
    #[19:45:47] [Server thread/INFO]: UnicornTaimer joined the game
    {'type': 'joined', 'pattern': f'{TIME} {THREAD_LEVEL}: {PLAYER_NAME} joined the game'},

    #[19:45:47] [Server thread/INFO]: UnicornTaimer[/192.168.0.12:57775] logged in with entity id 31880 at (-456.97696281546695, 68.0, -376.1927880149626)
    {'type': 'login', 'pattern': f'{TIME} {THREAD_LEVEL}: {PLAYER_NAME}\[\/{IP}:{PORT}\] logged in with entity id (?P<entity_id>\\d+) at \({COORDINATES}\)'},

    #[09:11:24] [Server thread/INFO]: UnicornTaimer left the game
    {'type': 'left', 'pattern': f'{TIME} {THREAD_LEVEL}: {PLAYER_NAME} left the game'},

    #[09:09:48] [Server thread/INFO]: Skrag001 lost connection: Disconnected
    {'type': 'disconnect', 'pattern': f'{TIME} {THREAD_LEVEL}: {PLAYER_NAME} lost connection: Disconnected'},

    #[19:33:00] [Server thread/INFO]: Skrag001 lost connection: Timed out
    {'type': 'disconnect', 'pattern': f'{TIME} {THREAD_LEVEL}: {PLAYER_NAME} lost connection: Timed out'},


    #[07:42:12] [Server thread/INFO]: com.mojang.authlib.GameProfile@3e14f6ec[id=<null>,name=Skrag001,properties={},legacy=false] (/192.168.0.138:58006) lost connection: Disconnected
    {'type': 'disconnect','pattern': f'{TIME} {THREAD_LEVEL}: com.mojang.authlib.GameProfile@{SHORT_HASH}\[.*,name={PLAYER_NAME},.*\] \(\/{IP}:{PORT}\) lost connection: Disconnected'},

    #[19:45:47] [User Authenticator #11/INFO]: UUID of player UnicornTaimer is 986162f6-2d57-4d1b-b834-037b9265e0e6
    {'type': 'player_uuid', 'pattern': f'{TIME} {THREAD_LEVEL}: UUID of player {PLAYER_NAME} is (?P<uuid>.*)'},


    # Commands

    #[07:45:25] [Server thread/INFO]: Teleported Skrag001 to -489.500000, 68.000000, -367.500000
    {'type': 'teleported', 'pattern': f'{TIME} {THREAD_LEVEL}: Teleported (?P<player_name>[A-Za-z0-9_]+) to {COORDINATES}'},

    #[07:47:16] [Server thread/INFO]: Gave 3 [Saddle] to UnicornTaimer
    {'type': 'teleported','pattern': f'{TIME} {THREAD_LEVEL}: Gave {COUNT} \[(?P<item>[A-Za-z0-9_]+)\] to (?P<player_name>[A-Za-z0-9_]+)'},

    #[19:30:10] [Server thread/INFO]: The nearest desert_pyramid is at [-352, ~, 0] (385 blocks away)
    {'type': 'nearest','pattern': f'{TIME} {THREAD_LEVEL}: The nearest (?P<item>[A-Za-z0-9_]+) is at \[{BLOCK_COORDINATES}\] \({DISTANCE} blocks away\)'},

    # chat
    #
    #[17:04:17] [Server thread/INFO]: <UnicornTaimer> when are you comeing home?
    {'type': 'advanced','pattern': f'{TIME} {THREAD_LEVEL}: <{PLAYER_NAME}> (?P<message>.*)'},

    # Game events
    #[19:02:08] [Server thread/INFO]: Villager bjr['Villager'/10666, l='ServerLevel[world]', x=-455.51, y=67.94, z=-375.24] died, message: 'Villager was slain by UnicornTaimer'
    {'type': 'kill','pattern': f'{TIME} {THREAD_LEVEL}: Villager .* message: \'{NPC_TYPE} was slain by {PLAYER_NAME}\''},

    #[19:01:12] [Server thread/INFO]: TurtleGroomer has made the advancement [We Need to Go Deeper]
    {'type': 'advanced','pattern': f'{TIME} {THREAD_LEVEL}: {PLAYER_NAME} has made the advancement \[(?P<advancement_name>.*)\]'},

    #[19:19:42] [Server thread/INFO]: TurtleGroomer tried to swim in lava
    {'type': 'swim_lava','pattern': f'{TIME} {THREAD_LEVEL}: {PLAYER_NAME} tried to swim in lava'},


]
