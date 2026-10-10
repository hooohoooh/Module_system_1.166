from header_common import *
from header_presentations import *
from header_mission_templates import *
from ID_meshes import *
from header_operations import *
from header_triggers import *
from module_constants import *
from module_meshes import *
import string
##diplomacy start+ Import for use with terrain advantage
from header_terrain_types import *
##diplomacy end+

##diplomacy begin
from module_items import *
##diplomacy end

####################################################################################################################
#  Each presentation record contains the following fields:
#  1) Presentation id: used for referencing presentations in other files. The prefix prsnt_ is automatically added before each presentation id.
#  2) Presentation flags. See header_presentations.py for a list of available flags
#  3) Presentation background mesh: See module_meshes.py for a list of available background meshes
#  4) Triggers: Simple triggers that are associated with the presentation
####################################################################################################################


##split modules begin
from module_presentations_multiplayer import presentations_multiplayer
from module_presentations_banner import presentations_banner
from module_presentations_politics_reports import presentations_politics_reports
from module_presentations_battle import presentations_battle
from module_presentations_army_management import presentations_army_management
from module_presentations_core_misc import presentations_core_misc
from module_presentations_game_start import presentations_game_start
##split modules end

presentations = presentations_multiplayer + presentations_banner + presentations_politics_reports + presentations_battle + presentations_army_management + presentations_core_misc + presentations_game_start

# modmerger_start version=201 type=2
try:
    component_name = "presentations"
    var_set = { "presentations" : presentations }
    from modmerger import modmerge
    modmerge(var_set)
except:
    raise
# modmerger_end
