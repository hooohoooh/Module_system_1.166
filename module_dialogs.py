# -*- coding: UTF-8 -*-
from header_common import *
from header_dialogs import *
from header_operations import *
from header_parties import *
from header_item_modifiers import *
from header_skills import *
from header_triggers import *
from ID_troops import *
from ID_party_templates import *
##diplomacy start+
from header_troops import ca_intelligence
from header_terrain_types import *
from header_items import * #For ek_food, and so forth
##diplomacy end+
from module_constants import *


####################################################################################################################
# During a dialog, the dialog lines are scanned from top to bottom.
# If the dialog-line is spoken by the player, all the matching lines are displayed for the player to pick from.
# If the dialog-line is spoken by another, the first (top-most) matching line is selected.
#
#  Each dialog line contains the following fields:
# 1) Dialogue partner: This should match the person player is talking to.
#    Usually this is a troop-id.
#    You can also use a party-template-id by appending '|party_tpl' to this field.
#    Use the constant 'anyone' if you'd like the line to match anybody.
#    Appending '|plyr' to this field means that the actual line is spoken by the player
#    Appending '|other(troop_id)' means that this line is spoken by a third person on the scene.
#       (You must make sure that this third person is present on the scene)
#
# 2) Starting dialog-state:
#    During a dialog there's always an active Dialog-state.
#    A dialog-line's starting dialog state must be the same as the active dialog state, for the line to be a possible candidate.
#    If the dialog is started by meeting a party on the map, initially, the active dialog state is "start"
#    If the dialog is started by speaking to an NPC in a town, initially, the active dialog state is "start"
#    If the dialog is started by helping a party defeat another party, initially, the active dialog state is "party_relieved"
#    If the dialog is started by liberating a prisoner, initially, the active dialog state is "prisoner_liberated"
#    If the dialog is started by defeating a party led by a hero, initially, the active dialog state is "enemy_defeated"
#    If the dialog is started by a trigger, initially, the active dialog state is "event_triggered"
# 3) Conditions block (list): This must be a valid operation block. See header_operations.py for reference.
# 4) Dialog Text (string):
# 5) Ending dialog-state:
#    If a dialog line is picked, the active dialog-state will become the picked line's ending dialog-state.
# 6) Consequences block (list): This must be a valid operation block. See header_operations.py for reference.
# 7) Voice-over (string): sound filename for the voice over. Leave here empty for no voice over
####################################################################################################################


##split modules begin
from module_dialogs_quest_npc import dialogs_quest_npc
from module_dialogs_lord_faction import dialogs_lord_faction
from module_dialogs_town_governance import dialogs_town_governance
from module_dialogs_trade_tavern import dialogs_trade_tavern
from module_dialogs_recruit_mercenary import dialogs_recruit_mercenary
from module_dialogs_siege import dialogs_siege
from module_dialogs_companion import dialogs_companion
from module_dialogs_dplmc import dialogs_dplmc
from module_dialogs_tutorial import dialogs_tutorial
from module_dialogs_artillery_lco import dialogs_artillery_lco
from module_dialogs_core_misc import dialogs_core_misc
##split modules end

dialogs = dialogs_quest_npc + dialogs_lord_faction + dialogs_town_governance + dialogs_trade_tavern + dialogs_recruit_mercenary + dialogs_siege + dialogs_companion + dialogs_dplmc + dialogs_tutorial + dialogs_artillery_lco + dialogs_core_misc

# modmerger_start version=201 type=2
try:
    component_name = "dialogs"
    var_set = { "dialogs" : dialogs }
    from modmerger import modmerge
    modmerge(var_set)
except:
    raise
# modmerger_end
