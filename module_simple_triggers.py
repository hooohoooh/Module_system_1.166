from header_common import *
from header_operations import *
from header_parties import *
from header_items import *
from header_skills import *
from header_triggers import *
from header_troops import *
from header_music import *
##diplomacy start+
from header_terrain_types import *
from module_factions import dplmc_factions_end
##diplomacy end+

from module_constants import *

####################################################################################################################
# Simple triggers are the alternative to old style triggers. They do not preserve state, and thus simpler to maintain.
#
#  Each simple trigger contains the following fields:
# 1) Check interval: How frequently this trigger will be checked
# 2) Operation block: This must be a valid operation block. See header_operations.py for reference. 
####################################################################################################################




##split modules begin
from module_simple_triggers_quests import simple_triggers_quests
from module_simple_triggers_dk_invasion_lco import simple_triggers_dk_invasion_lco
from module_simple_triggers_gekokujo import simple_triggers_gekokujo
from module_simple_triggers_economy_trade import simple_triggers_economy_trade
from module_simple_triggers_politics_ai import simple_triggers_politics_ai
from module_simple_triggers_dplmc import simple_triggers_dplmc
from module_simple_triggers_core_daily import simple_triggers_core_daily
##split modules end

simple_triggers = simple_triggers_quests + simple_triggers_dk_invasion_lco + simple_triggers_gekokujo + simple_triggers_economy_trade + simple_triggers_politics_ai + simple_triggers_dplmc + simple_triggers_core_daily

# modmerger_start version=201 type=2
try:
    component_name = "simple_triggers"
    var_set = { "simple_triggers" : simple_triggers }
    from modmerger import modmerge
    modmerge(var_set)
except:
    raise
# modmerger_end
