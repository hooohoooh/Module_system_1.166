# -*- coding: UTF-8 -*-
# split feature file: dialogs - module
from header_common import *
from header_dialogs import *
from header_operations import *
from header_parties import *
from header_item_modifiers import *
from header_skills import *
from header_triggers import *
from ID_troops import *
from ID_party_templates import *
from header_troops import ca_intelligence
from header_terrain_types import *
from header_items import * #For ek_food, and so forth
from module_constants import *

dialogs_artillery_lco = [
  
[anyone|plyr, "gekokujo_encounter_reply_1", 
  [
    (str_store_string, s6, "$gekokujo_encounter_reply_1"),
  ],
  "{s6}",
  "gekokujo_encounter_reply_2", []],
  
[anyone|plyr, "gekokujo_encounter_reply_1", 
  [
    (str_store_string, s7, "$gekokujo_encounter_reply_2"),
  ],
  "{s7}",
  "gekokujo_encounter_reply_2", []],
  
[anyone|plyr, "gekokujo_encounter_reply_2", 
  [
    (store_random_in_range, ":offset", 0, 10),
    (val_add, ":offset", "str_gekokujo_encounter_reply_1"),
    (str_store_string, s8, ":offset"),
  ],
  "{s8}",
  "close_window", 
  [
    (jump_to_menu, "mnu_encounter_setup"),
  ]],
  [anyone, "lco_conversation_end", [(assign,"$g_lco_operation",lco_run_presentation)], "It's a honor to serve you, {sir/my lady}!", "close_window", [(change_screen_return)]],
]
