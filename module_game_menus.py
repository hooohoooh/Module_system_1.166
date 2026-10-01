# -*- coding: UTF-8 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *

from module_constants import *
from ym_gatling_shop import *

####################################################################################################################
#  (menu-id, menu-flags, menu_text, mesh-name, [<operations>], [<options>]),
#
#   Each game menu is a tuple that contains the following fields:
#  
#  1) Game-menu id (string): used for referencing game-menus in other files.
#     The prefix menu_ is automatically added before each game-menu-id
#
#  2) Game-menu flags (int). See header_game_menus.py for a list of available flags.
#     You can also specify menu text color here, with the menu_text_color macro
#  3) Game-menu text (string).
#  4) mesh-name (string). Not currently used. Must be the string "none"
#  5) Operations block (list). A list of operations. See header_operations.py for reference.
#     The operations block is executed when the game menu is activated.
#  6) List of Menu options (List).
#     Each menu-option record is a tuple containing the following fields:
#   6.1) Menu-option-id (string) used for referencing game-menus in other files.
#        The prefix mno_ is automatically added before each menu-option.
#   6.2) Conditions block (list). This must be a valid operation block. See header_operations.py for reference. 
#        The conditions are executed for each menu option to decide whether the option will be shown to the player or not.
#   6.3) Menu-option text (string).
#   6.4) Consequences block (list). This must be a valid operation block. See header_operations.py for reference. 
#        The consequences are executed for the menu option that has been selected by the player.
#
#
# Note: The first Menu is the initial character creation menu.
####################################################################################################################


##split modules begin
from module_game_menus_character import game_menus_character
from module_game_menus_camp_cheat import game_menus_camp_cheat
from module_game_menus_reports import game_menus_reports
from module_game_menus_encounter_battle import game_menus_encounter_battle
from module_game_menus_town_castle_siege import game_menus_town_castle_siege
from module_game_menus_village_quests import game_menus_village_quests
from module_game_menus_trade_ship import game_menus_trade_ship
from module_game_menus_tournament_training import game_menus_tournament_training
from module_game_menus_faction_politics import game_menus_faction_politics
from module_game_menus_gekokujo import game_menus_gekokujo
from module_game_menus_recruitment_lco import game_menus_recruitment_lco
from module_game_menus_core_misc import game_menus_core_misc
##split modules end

game_menus = game_menus_character + game_menus_camp_cheat + game_menus_reports + game_menus_encounter_battle + game_menus_town_castle_siege + game_menus_village_quests + game_menus_trade_ship + game_menus_tournament_training + game_menus_faction_politics + game_menus_gekokujo + game_menus_recruitment_lco + game_menus_core_misc

# modmerger_start version=201 type=2
try:
    component_name = "game_menus"
    var_set = { "game_menus" : game_menus }
    from modmerger import modmerge
    modmerge(var_set)
except:
    raise
# modmerger_end
