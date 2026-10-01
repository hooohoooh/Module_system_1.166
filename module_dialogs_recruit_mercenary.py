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

dialogs_recruit_mercenary = [
  [anyone|plyr, "mercenary_after_recruited", [],
   "Make your preparations. We'll be moving at dawn.", "mercenary_after_recruited_2", []],
  [anyone|plyr, "mercenary_after_recruited", [],
   "Take your time. We'll be staying in this town for a while.", "mercenary_after_recruited_2", []],
  [anyone, "mercenary_after_recruited_2", [], "Yes {sir/madam}. We'll be ready when you tell us to leave.", "close_window", []],
  [anyone|plyr, "mercenary_tavern_talk", [(party_get_slot, ":mercenary_amount", "$g_encountered_party", slot_center_mercenary_troop_amount),
                                          (eq, ":mercenary_amount", "$temp"),
                                          (party_get_slot, ":mercenary_troop", "$g_encountered_party", slot_center_mercenary_troop_type),
                                          (call_script, "script_game_get_join_cost", ":mercenary_troop"),
                                          (store_mul, reg5, "$temp", reg0),
                                          ],
   "All right. I will hire all of you. Here is {reg5} mon.", "mercenary_tavern_talk_hire", []],
  [anyone|plyr, "mercenary_tavern_talk", [(party_get_slot, ":mercenary_amount", "$g_encountered_party", slot_center_mercenary_troop_amount),
                                          (lt, "$temp", ":mercenary_amount"),
                                          (gt, "$temp", 0),
                                          (assign, reg6, "$temp"),
                                          (party_get_slot, ":mercenary_troop", "$g_encountered_party", slot_center_mercenary_troop_type),
                                          (call_script, "script_game_get_join_cost", ":mercenary_troop"),
                                          (store_mul, reg5, "$temp", reg0),
                                          ],
   "All right. But I can only hire {reg6} of you. Here is {reg5} mon.", "mercenary_tavern_talk_hire", []],
  [anyone, "mercenary_tavern_talk_hire", [(store_random_in_range, ":rand", 0, 4),
                                          (try_begin),
                                            (eq, ":rand", 0),
                                            (gt, "$temp", 1),
											##diplomacy start+ lads -> {reg65?companions:lads}; {sir/madame} -> {s0}
											(call_script, "script_dplmc_print_subordinate_says_sir_madame_to_s0"),
                                            (str_store_string, s17,
                                             "@You chose well, {s0}. My {reg65?companions:lads} know how to keep their word and earn their pay."),
											 ##diplomacy end+
                                          (else_try),
                                            (eq, ":rand", 1),
											##diplomacy start+ {sir/madame} -> {s0}
											(call_script, "script_dplmc_print_subordinate_says_sir_madame_to_s0"),
                                            (str_store_string, s17,
                                             "@Well done, {s0}. Keep the money and sake coming our way, and there's no foe in Japan you need fear."),
											 ##diplomacy end+
                                          (else_try),
                                            (eq, ":rand", 2),
											##diplomacy start+ {sir/madame} -> {s0}
											(call_script, "script_dplmc_print_subordinate_says_sir_madame_to_s0"),
                                            (str_store_string, s17,
                                             "@We are at your service, {s0}. Point us in the direction of those who need hurting, and we'll do the rest."),
											 ##diplomacy end+
                                          (else_try),
                                            (str_store_string, s17,
                                             "str_you_will_not_be_disappointed_sirmadam_you_will_not_find_better_warriors_in_all_calradia"),
                                          (try_end),],
   "{s17}", "close_window", [
                                          (party_get_slot, ":mercenary_troop", "$g_encountered_party", slot_center_mercenary_troop_type),
                                          (call_script, "script_game_get_join_cost", ":mercenary_troop"),
                                          (store_mul, ":total_cost", "$temp", reg0),
                                          (troop_remove_gold, "trp_player", ":total_cost"),
                                          (party_add_members, "p_main_party", ":mercenary_troop", "$temp"),
                                          (party_set_slot, "$g_encountered_party", slot_center_mercenary_troop_amount, 0),
                                          ]],
  [anyone|plyr, "mercenary_tavern_talk", [(eq, "$temp", 0),
                                          (party_get_free_companions_capacity, ":free_capacity", "p_main_party"),
                                          (ge, ":free_capacity", 1)],
##diplomacy start+ Gender-check to avoid accidental absurdities if there are female mercenaries
   "That sounds good. But I can't afford to hire any more {reg65?soldiers:men} right now.", "tavern_mercenary_cant_lead", []],
  [anyone|plyr, "mercenary_tavern_talk", [(eq, "$temp", 0),
                                          (party_get_free_companions_capacity, ":free_capacity", "p_main_party"),
                                          (eq, ":free_capacity", 0)],
##diplomacy start+ Gender-check to avoid accidental absurdities if there are female mercenaries
   "That sounds good. But I can't lead any more {reg65?soldiers:men} right now.", "tavern_mercenary_cant_lead", []],
##diplomacy end+

  [anyone|plyr, "mercenary_tavern_talk", [],
   "Sorry. I don't need any other men right now.", "close_window", []],
]
