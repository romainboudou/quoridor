# ---------------- imports --------------------
from statemachine import StateMachine, State


# -------------- CLASSE QUI GERE LE STATUS DU JEU --------------#
class GameStatus(StateMachine):
    # ETATS PRINCIPAUX
    menu_principal = State(initial=True)
    menu_mod = State()
    menu_load = State()
    menu_settings = State()

    # ETATS LIES A MOD
    menu_new_game = State()
    menu_client_serveur = State()
    menu_client_serveur_load = State()

    # ETATS LIES A LOAD
    menu_mod_load = State()

    # ETATS LIES A MOD_LOAD
    menu_new_room = State()

    # ETATS LIES A CLIENT_SERVEUR
    menu_waiting_serveur = State()
    menu_waiting_client = State()


    # ETATS LIES A CLIENT_SERVEUR_LOAD
    menu_waiting_load_serveur = State()

    # ETATS LIES A GAME
    game = State()
    game_server = State()
    game_client = State()
    menu_ingame_settings = State()
    menu_ingame_settings_client = State()
    menu_ingame_settings_server = State()
    menu_fin = State()
    tooltip = State()
    tooltip_server = State()
    tooltip_client = State()
    restart = State() # pour savoir si on a le droit de recommencer la partie ou pas (dans le cas du multijoueur, non)

    # TRANSISTIONS

    # transition menu_principal - settings
    principal_to_settings = menu_principal.to(menu_settings)
    settings_to_principal = menu_settings.to(menu_principal)

    # transition menu_principal - load
    principal_to_load = menu_principal.to(menu_load)
    load_to_principal = menu_load.to(menu_principal)

    # transition menu_principal - mod
    principal_to_mod = menu_principal.to(menu_mod)
    mod_to_principal = menu_mod.to(menu_principal)

    # transition menu_load - mod_load
    menu_load_to_menu_mod_load = menu_load.to(menu_mod_load)
    menu_mod_load_to_menu_load = menu_mod_load.to(menu_load)

    # transition mod - new_game
    mod_to_newgame = menu_mod.to(menu_new_game)
    newgame_to_mod = menu_new_game.to(menu_mod)

    # transition client_serveur - mod
    clientserveur_to_mod = menu_client_serveur.to(menu_mod)
    mod_to_clientserveur = menu_mod.to(menu_client_serveur)


    # transition menu_client_server - menu_new_room
    client_serveur_to_new_room = menu_client_serveur.to(menu_new_room)
    new_room_to_client_serveur = menu_new_room.to(menu_client_serveur)

    # VERS CLIENT_SERVEUR_LOAD
    menu_mod_load_to_menu_client_serveur_load = menu_mod_load.to(menu_client_serveur_load)
    menu_client_serveur_load_to_mod_load = menu_client_serveur_load.to(menu_mod_load)

    # VERS LES MENUS WAITING

    # transition menu_new_room - menu_waiting_serveur
    menu_new_room_to_menu_waiting_serveur = menu_new_room.to(menu_waiting_serveur)

    # transition menu_client_serveur - menu_waiting_client
    menu_client_serveur_to_menu_waiting_client = menu_client_serveur.to(menu_waiting_client)

    # transition menu_client_serveur_load - menu_waiting_load_serveur
    menu_client_serveur_load_to_menu_waiting_load_serveur = menu_client_serveur_load.to(menu_waiting_load_serveur)


    # VERS GAME

    # transition menu_new_room - game
    new_room_to_game = menu_new_room.to(game)

    # transition new_game - game
    newgame_to_game = menu_new_game.to(game)

    # transition menu_mod_load - game
    menu_mod_load_to_game = menu_mod_load.to(game)

    # VERS INGAME_SETTINGS
    game_to_menu_ingame_settings = game.to(menu_ingame_settings)
    menu_ingame_settings_to_game = menu_ingame_settings.to(game)
    menu_ingame_settings_to_principal = menu_ingame_settings.to(menu_principal)

    game_client_to_menu_ingame_settings_client = game_client.to(menu_ingame_settings_client)
    game_server_to_menu_ingame_settings_server = game_server.to(menu_ingame_settings_server)

    menu_ingame_settings_client_to_game_client = menu_ingame_settings_client.to(game_client)
    menu_ingame_settings_server_to_game_server = menu_ingame_settings_server.to(game_server)


    # VERS TOOLTIP
    game_to_tooltip = game.to(tooltip)
    game_client_to_tooltip_client = game_client.to(tooltip_client)
    game_server_to_tooltip_server = game_server.to(tooltip_server)
    tooltip_to_game = tooltip.to(game)
    tooltip_client_to_game_client = tooltip_client.to(game_client)
    tooltip_server_to_game_server = tooltip_server.to(game_server)

    # transitions de tout les menus waiting vers game
    menu_waiting_serveur_to_game_server = menu_waiting_serveur.to(game_server)
    menu_waiting_client_to_game_client = menu_waiting_client.to(game_client)
    menu_waiting_load_serveur_to_game_server = menu_waiting_load_serveur.to(game_server)


    # VERS MENU FIN
    # transition game - menu_fin
    game_to_menu_fin = game.to(menu_fin)
    game_client_to_menu_fin = game_client.to(menu_fin)
    game_server_to_menu_fin = game_server.to(menu_fin)

    # RETOUR AU PRINCIPAL
    # transition menu_fin - menu_principal
    menu_fin_to_principal = menu_fin.to(menu_principal)

    menu_ingame_settings_to_restart = menu_ingame_settings.to(restart)
    restart_to_game = restart.to(game)
