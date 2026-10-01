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


dialogs_dplmc = [
[anyone, "dplmc_drunk_attempt_placate", [
(neq, "$g_talk_troop", "trp_hired_assassin"),
#Right now this is the same as the check in Native to persuade a companion to stay in your party
(store_skill_level, reg1, "skl_persuasion", "trp_player"),
(store_random_in_range, reg0, -2, 13),
(try_begin),
   (ge, "$cheat_mode", 1),
	(display_message, "@{!}Persuasion attempt: skill {reg1} versus random roll {reg0} (-2 through 12)"),
(try_end),
(le, reg0, reg1),
#The persuasion attempt succeeded.
(call_script, "script_deactivate_tavern_attackers"),
],
"I'll let it slide... this time.  Now buzz off.", "close_window", [
]],
[anyone, "dplmc_drunk_attempt_placate", [],
#The persuasion attempt failed.  Fall back to the standard behavior.
"I'll wipe that smirk right off your face!", "close_window", [
(troop_set_slot, "trp_belligerent_drunk", slot_troop_cur_center, 0),
]],
[trp_dplmc_recruiter|plyr, "dplmc_recruiter_talk", [], "Ok, keep going.", "close_window",[(assign, "$g_leave_encounter",1)]],
[trp_dplmc_recruiter|plyr, "dplmc_recruiter_talk", [], "I want you to recruit different troops.", "dplmc_recruiter_talk_2",[]],
[trp_dplmc_recruiter, "dplmc_recruiter_talk_2", [
(party_get_slot, reg1, "$g_encountered_party", dplmc_slot_party_recruiter_needed_recruits),
(party_get_slot, ":recruit_faction", "$g_encountered_party", dplmc_slot_party_recruiter_needed_recruits_faction),

(store_sub, ":offset", ":recruit_faction", "fac_kingdom_1"),
(val_add, ":offset", "str_kingdom_1_adjective"),
(str_store_string, s1, ":offset"),

], "My current task is to recruit {reg1} {s1} troops for you. Should I recruit different soldiers from now on?", "dplmc_recruiter_talk_3",[]],
[trp_dplmc_recruiter|plyr, "dplmc_recruiter_talk_3", [], "No, keep going.", "close_window",[(assign, "$g_leave_encounter",1)]],
[trp_dplmc_recruiter|plyr|repeat_for_factions, "dplmc_recruiter_talk_3",
[
(store_repeat_object, ":faction_no"),
##diplomacy start+ Sometimes the player may be the ruler or co-ruler of an NPC kingdom.
#Do not allow sending emissaries in those cases.
(neq, ":faction_no", "$players_kingdom"),
##diplomacy end+
(is_between, ":faction_no", npc_kingdoms_begin, npc_kingdoms_end),
(store_sub, ":offset", ":faction_no", "fac_kingdom_1"),
(val_add, ":offset", "str_kingdom_1_adjective"),
(str_store_string, s11, ":offset"),
],
"{s11}.", "dplmc_recruiter_talk_4",
[
(store_repeat_object, ":faction_no"),
(assign, "$temp", ":faction_no"),
]],
[trp_dplmc_recruiter|plyr, "dplmc_recruiter_talk_3", [], "Recruit any troops.", "dplmc_recruiter_talk_4",[(assign,"$temp",-1)]],
[trp_dplmc_recruiter, "dplmc_recruiter_talk_4", [(party_set_slot, "$g_encountered_party", dplmc_slot_party_recruiter_needed_recruits_faction, "$temp"),
##diplomacy start+ replace {reg65?madame:sir} with {s0}
(call_script, "script_dplmc_print_subordinate_says_sir_madame_to_s0"),
], "Sure {s0}. I will. Anything else you want?", "dplmc_recruiter_talk",[]],
[trp_dplmc_messenger|plyr, "dplmc_messenger_talk", [], "Alright, I don't want to delay you. Godspeed!", "dplmc_messenger_talk_farewell",[]],
[trp_dplmc_messenger, "dplmc_messenger_talk_farewell", [], "Thank you. Farewell!", "close_window", [(assign, "$g_leave_encounter", 1),]],
[anyone, "dplmc_patrol_pretalk", [
(call_script, "script_dplmc_print_subordinate_says_sir_madame_to_s0"),
], "Greetings, {s0}. Do you have new orders?", "dplmc_patrol_talk",
##nested diplomacy end+
[]],
[anyone|plyr, "dplmc_patrol_talk", [], "Please patrol a new area.", "dplmc_patrol_orders_area_ask",
[]],
[anyone, "dplmc_patrol_orders_area_ask", [], "Where should we go?", "dplmc_patrol_orders_area",
[]],
[anyone|plyr|repeat_for_parties, "dplmc_patrol_orders_area",
[
(store_repeat_object, ":party_no"),
(is_between, ":party_no", centers_begin, centers_end),
(store_faction_of_party, ":party_faction", ":party_no"),
(eq, ":party_faction", "$players_kingdom"),
(str_store_party_name, s11, ":party_no"),
],
"{s11}.", "dplmc_patrol_confirm_ask",
[
(store_repeat_object, "$diplomacy_var"),
]
],
[anyone|plyr, "dplmc_patrol_orders_area", [], "Nevermind.", "dplmc_patrol_pretalk",
[]],
[anyone, "dplmc_patrol_confirm_ask",
[(str_store_party_name, s5, "$diplomacy_var"),],
"As you wish, we will patrol {s5}.", "dplmc_patrol_confirm",
[]
],
[anyone|plyr, "dplmc_patrol_confirm", [(str_store_party_name, s5, "$diplomacy_var"),], "Thank you.", "close_window",
[
(party_set_name, "$g_encountered_party", "@{s5} patrol"),
(party_set_slot, "$g_encountered_party", slot_party_ai_object, "$diplomacy_var"),
(party_set_slot, "$g_encountered_party", slot_party_ai_state, spai_patrolling_around_center),
(party_set_ai_behavior, "$g_encountered_party", ai_bhvr_travel_to_party),
(party_set_ai_object, "$g_encountered_party", "$diplomacy_var"),
(assign, "$g_leave_encounter", 1),
]],
[anyone|plyr, "dplmc_patrol_confirm", [], "Wait, I changed my mind.", "dplmc_patrol_pretalk",
[]],
[anyone|plyr, "dplmc_patrol_talk", [], "I need you to reinforce a garrison.", "dplmc_patrol_orders_garrison_ask",
[]],
[anyone, "dplmc_patrol_orders_garrison_ask", [], "Where should we go?", "dplmc_patrol_garrison_target",
[]],
[anyone|plyr|repeat_for_parties, "dplmc_patrol_garrison_target",
[
(store_repeat_object, ":party_no"),
(is_between, ":party_no", centers_begin, centers_end),
(store_faction_of_party, ":party_faction", ":party_no"),
(eq, ":party_faction", "$players_kingdom"),
(str_store_party_name, s11, ":party_no"),
],
"{!}{s11}.", "dplmc_patrol_garrison_confirm_ask",
[
(store_repeat_object, "$diplomacy_var"),
]
],
[anyone|plyr, "dplmc_patrol_garrison_target", [], "Nevermind.", "dplmc_patrol_pretalk",
[]],
[anyone, "dplmc_patrol_garrison_confirm_ask",
[(str_store_party_name, s5, "$diplomacy_var"),],
"As you wish, we will reinforce {s5}.", "dplmc_patrol_garrison_confirm",
[]
],
[anyone|plyr, "dplmc_patrol_garrison_confirm", [(str_store_party_name, s5, "$diplomacy_var"),], "Thank you.", "close_window",
[
(party_set_name, "$g_encountered_party", "@{s5} patrol"),
(party_set_slot, "$g_encountered_party", slot_party_ai_object, "$diplomacy_var"),
(party_set_slot, "$g_encountered_party", slot_party_ai_state, spai_retreating_to_center),
(party_set_ai_behavior, "$g_encountered_party", ai_bhvr_travel_to_party),
(party_set_ai_object, "$g_encountered_party", "$diplomacy_var"),
(assign, "$g_leave_encounter", 1),
]],
[anyone|plyr, "dplmc_patrol_garrison_confirm", [], "Wait, I changed my mind.", "dplmc_patrol_pretalk",
[]],
[anyone|plyr,"dplmc_patrol_talk", [],
"I want to give some troops to you.", "dplmc_patrol_give_troops",[]],
[anyone,"dplmc_patrol_give_troops", [],
"Well, I could use some good soldiers. Thank you.", "dplmc_patrol_pretalk",
[
(change_screen_give_members, "$g_talk_troop_party"),
(change_screen_exchange_members,0),
]],
[anyone|plyr, "dplmc_patrol_talk", [], "I don't need you any longer. Please disband.", "close_window",
[
(remove_party, "$g_encountered_party"),
(assign, "$g_leave_encounter", 1),
]],
[anyone|plyr, "dplmc_patrol_talk", [], "Please continue.", "close_window",
[(assign, "$g_leave_encounter", 1),]],
[pt_dplmc_gift_caravan|party_tpl, "dplmc_gift_talk", [], "Very well! Have a nice trip.", "dplmc_gift_talk_farewell",[]],
[pt_dplmc_gift_caravan|party_tpl, "dplmc_gift_talk_farewell", [], "Thank you. Farewell!", "close_window", [(assign, "$g_leave_encounter", 1),]],
[anyone|plyr,"dplmc_scout_talk",[
],
"Ok, please go on.", "close_window",
[]],
[anyone,"dplmc_chancellor_pretalk",
[],
"Do you need anything else, my {lord/lady}?", "dplmc_chancellor_talk",[
]],
[anyone|plyr,"dplmc_chancellor_talk",[
],
"Let's talk about domestic policy.", "dplmc_chancellor_domestic_policy_options_ask",
##nested diplomacy start+
[
(try_begin),
	(neq, "$players_kingdom", "fac_player_supporters_faction"),
	(is_between, "$players_kingdom", kingdoms_begin, kingdoms_end),
	(try_for_range, ":slot_no", dplmc_slot_faction_policies_begin, dplmc_slot_faction_policies_end),
		(faction_get_slot, reg0, "$players_kingdom", ":slot_no"),
		(faction_set_slot, "fac_player_supporters_faction", ":slot_no",  reg0),
	(try_end),
(try_end),
##nested diplomacy end+
]],
[anyone,"dplmc_chancellor_domestic_policy_options_ask",
[],
"As you wish, my {lord/lady}.", "dplmc_chancellor_domestic_policy_options",[
]],
[anyone|plyr, "dplmc_chancellor_domestic_policy_options",
[
(is_between, "$g_player_minister", active_npcs_begin, kingdom_ladies_end),
],
##diplomacy start+ add apostrophe
"I wish to select the kingdom's culture.", "dplmc_chancellor_kingdom_culture_ask",
##diplomacy end+
[]],
[anyone, "dplmc_chancellor_kingdom_culture_ask",
[
(is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
(assign, ":end_cond", active_npcs_end),
(try_for_range, ":lord", active_npcs_begin, ":end_cond"),
	(store_faction_of_troop, reg0, ":lord"),
	(eq, reg0, "$players_kingdom"),
	(troop_slot_eq, ":lord", slot_troop_original_faction, "$players_kingdom"),
	(assign, ":end_cond", ":lord"),
(try_end),
(lt, ":end_cond", active_npcs_end),
(str_store_faction_name, s11, "$players_kingdom"),
(call_script, "script_dplmc_print_cultural_word_to_sreg", ":end_cond", DPLMC_CULTURAL_TERM_LORD_PLURAL,0),
], "The {s0} of the {s11} would be unlikely to accept the imposition of other culture.", "dplmc_chancellor_talk",
[]],
[anyone, "dplmc_chancellor_kingdom_culture_ask",
[
(try_begin),
(this_or_next|le, "$g_player_culture", 0),
(neg|is_between, "$g_player_culture", npc_kingdoms_begin, npc_kingdoms_end),
(str_store_string, s11, "@Your domain has no specified culture"),
(else_try),
(store_sub, ":offset", "$g_player_culture", "fac_kingdom_1"),
(val_add, ":offset", "str_kingdom_1_adjective"),
(str_store_string, s11, ":offset"),
(str_store_string, s11, "@Your domain culture is: {s11}"),
(try_end),
],
"{s11}. Do you want to change it?", "dplmc_chancellor_kingdom_culture_select",
[]],
[anyone|plyr|repeat_for_factions, "dplmc_chancellor_kingdom_culture_select",
[
(store_repeat_object, ":faction_no"),
(is_between, ":faction_no", npc_kingdoms_begin, npc_kingdoms_end),
##nested diplomacy start+
#To be eligible to establish a culture, you need some connection to it.
(assign, ":faction_allowed", 0),
(try_begin),
   #If it is the faction you left (or is otherwise somehow your faction)
   (this_or_next|eq, ":faction_no", "$players_oath_renounced_against_kingdom"),
   (eq, ":faction_no", "$players_kingdom"),
   (assign, ":faction_allowed", 1),
(else_try),
   #If it's the faction of the town you started in
   (is_between, "$g_starting_town", centers_begin, centers_end),
   (party_slot_eq, "$g_starting_town", slot_center_original_faction, ":faction_no"),
   (assign, ":faction_allowed", 1),
(else_try),
   #If you currently control any centers of that faction
   (assign, ":end_cond", walled_centers_end),
   (try_for_range, ":iter_no", walled_centers_begin, ":end_cond"),
      (store_faction_of_party, ":iter_faction", ":iter_no"),
      (eq, ":iter_faction", "$players_kingdom"),
      (party_slot_eq, ":iter_no", slot_center_original_faction, ":faction_no"),
#      (party_slot_eq, ":iter_no", slot_town_lord, "trp_player"),
      (assign, ":end_cond", ":iter_no"),
      (assign, ":faction_allowed", 1),
   (try_end),
   (eq, ":faction_allowed", 1),
(else_try),
   #If any of your lords come from that faction
   (assign, ":end_cond", heroes_end),
   (try_for_range, ":iter_no", heroes_begin, ":end_cond"),
      (store_faction_of_troop, ":iter_faction", ":iter_no"),
      (eq, ":iter_faction", "$players_kingdom"),
      (troop_slot_eq, ":iter_no", slot_troop_original_faction, ":faction_no"),
      (assign, ":end_cond", ":iter_no"),
      (assign, ":faction_allowed", 1),
   (try_end),
(try_end),
(eq, ":faction_allowed", 1),
##nested diplomacy end+
(store_sub, ":offset", ":faction_no", "fac_kingdom_1"),
(val_add, ":offset", "str_kingdom_1_adjective"),
(str_store_string, s11, ":offset"),
],
"{s11}.", "dplmc_chancellor_pretalk",
[
(store_repeat_object, ":faction_no"),
(assign, "$g_player_culture", ":faction_no"),
(try_begin),
(this_or_next|le, "$g_player_culture", 0),
(neg|is_between, "$g_player_culture", npc_kingdoms_begin, npc_kingdoms_end),
(str_store_string, s11, "@Kingdom culture: None"),
(else_try),
(store_sub, ":offset", "$g_player_culture", "fac_kingdom_1"),
(val_add, ":offset", "str_kingdom_1_adjective"),
(str_store_string, s11, ":offset"),
(str_store_string, s11, "@Kingdom culture: {s11}"),
(try_end),
(display_message, "@{s11}")
]],
[anyone|plyr, "dplmc_chancellor_kingdom_culture_select",
[],
##diplomacy start+ Reword
#"None.", "dplmc_chancellor_pretalk",
"Favor no culture over others.", "dplmc_chancellor_pretalk",
##diplomacy end+
[(assign, "$g_player_culture", 0),
]],
[anyone|plyr, "dplmc_chancellor_kingdom_culture_select",
[],
"Make no change.", "dplmc_chancellor_pretalk",
[]],
[anyone|plyr,"dplmc_chancellor_domestic_policy_options",[
(faction_slot_eq, "fac_player_supporters_faction", slot_faction_state, sfs_active),
],
"Please give me information about the domestic policy of a clan.", "dplmc_chancellor_domestic_policy_info_ask",
[]],
[anyone,"dplmc_chancellor_domestic_policy_info_ask",
[],
"Which clan do you need information on?", "dplmc_chancellor_domestic_policy_info_select",[
]],
[anyone|plyr|repeat_for_factions,"dplmc_chancellor_domestic_policy_info_select",[
(store_repeat_object, ":faction"),
(is_between, ":faction", npc_kingdoms_begin, npc_kingdoms_end),
(str_store_faction_name, s10, ":faction"),
],
"{s10}.", "dplmc_chancellor_domestic_policy_info",
[(store_repeat_object, "$diplomacy_var"),]],
[anyone|plyr,"dplmc_chancellor_domestic_policy_info_select",[],
"None.", "dplmc_chancellor_pretalk",
[]],
[anyone,"dplmc_chancellor_domestic_policy_info",
[
(str_store_faction_name_link, s10, "$diplomacy_var"),
(assign, ":string", "str_dplmc_neither_centralize_nor_decentralized"),
(faction_get_slot, ":centralization", "$diplomacy_var", dplmc_slot_faction_centralization),
(val_add, ":string", ":centralization"),
(str_store_string, s4, ":string"),
(str_store_string, s4, "@The goverment of the {s10} is {s4}."),

(assign, ":string", "str_dplmc_neither_aristocratic_nor_plutocratic"),
(faction_get_slot, ":aristocraty", "$diplomacy_var", dplmc_slot_faction_aristocracy),
(val_add, ":string", ":aristocraty"),
(str_store_string, s5, ":string"),
(str_store_string, s5, "@The upper class society is {s5}."),

(assign, ":string", "str_dplmc_mixture_serfs"),
(faction_get_slot, ":serfdom", "$diplomacy_var", dplmc_slot_faction_serfdom),
(val_add, ":string", ":serfdom"),
(str_store_string, s6, ":string"),
(str_store_string, s6, "@The people are {s6}."),

(assign, ":string", "str_dplmc_mediocre_quality"),
(faction_get_slot, ":quality", "$diplomacy_var", dplmc_slot_faction_quality),
(val_add, ":string", ":quality"),
(str_store_string, s7, ":string"),
(str_store_string, s7, "@The troops have {s7}."),

##nested diplomacy start+ add mercantilism
(assign, ":string", "str_dplmc_neither_mercantilist_nor_laissez_faire"),
(faction_get_slot, ":mercantilism", "$diplomacy_var", dplmc_slot_faction_mercantilism),
(val_add, ":string", ":mercantilism"),
(str_store_string, s0, ":string"),
(str_store_string, s0, "@The government's approach to trade is {s0}."),
],
"{s4} {s5} {s6} {s7} {s0}", "dplmc_chancellor_domestic_policy_info_ask",[#<- dplmc+ added {s0}
]],
[anyone|plyr,"dplmc_chancellor_domestic_policy_options",[
(faction_slot_eq, "fac_player_supporters_faction", slot_faction_state, sfs_active),
],
"Let's change our domestic policy.", "dplmc_chancellor_domestic_policy_ask",
[]],
[anyone|plyr,"dplmc_chancellor_domestic_policy_options",[
],
"Nevermind.", "dplmc_chancellor_pretalk",
[]],
[anyone,"dplmc_chancellor_domestic_policy_ask",[
(store_current_hours, ":current_hours"),
##zParsifal 2011-10-07: Change the policy change interval from always 30 days to (Centralization * 5) + 30 days.
(faction_get_slot, ":policy_time", "fac_player_supporters_faction", dplmc_slot_faction_centralization),
(val_mul, ":policy_time", -5),
(val_add, ":policy_time", 30),
(val_clamp, ":policy_time", 15, 46),#This line should be unnecessary
(val_mul, ":policy_time", 24),
(val_sub, ":current_hours", ":policy_time"),
(faction_get_slot, ":policy_time", "fac_player_supporters_faction", dplmc_slot_faction_policy_time),
(ge, ":current_hours", ":policy_time"),

(assign, ":string", "str_dplmc_neither_centralize_nor_decentralized"),
(faction_get_slot, ":centralization", "fac_player_supporters_faction", dplmc_slot_faction_centralization),
(val_add, ":string", ":centralization"),
(str_store_string, s4, ":string"),
(str_store_string, s4, "@Our goverment is {s4}."),

(assign, ":string", "str_dplmc_neither_aristocratic_nor_plutocratic"),
(faction_get_slot, ":aristocraty", "fac_player_supporters_faction", dplmc_slot_faction_aristocracy),
(val_add, ":string", ":aristocraty"),
(str_store_string, s5, ":string"),
(str_store_string, s5, "@The upper class society is {s5}."),

(assign, ":string", "str_dplmc_mixture_serfs"),
(faction_get_slot, ":serfdom", "fac_player_supporters_faction", dplmc_slot_faction_serfdom),
(val_add, ":string", ":serfdom"),
(str_store_string, s6, ":string"),
(str_store_string, s6, "@Our people are {s6}."),

(assign, ":string", "str_dplmc_mediocre_quality"),
(faction_get_slot, ":quality", "fac_player_supporters_faction", dplmc_slot_faction_quality),
(val_add, ":string", ":quality"),
(str_store_string, s7, ":string"),
(str_store_string, s7, "@Our troops have {s7}."),

##nested diplomacy start+ add mercantilism
(assign, ":string", "str_dplmc_neither_mercantilist_nor_laissez_faire"),
(faction_get_slot, ":mercantilism", "fac_player_supporters_faction", dplmc_slot_faction_mercantilism),
(val_add, ":string", ":mercantilism"),
(str_store_string, s0, ":string"),
(str_store_string, s0, "@Our approach to trade is {s0}."),
],
"{s4} {s5} {s6} {s7} {s0} What do you want to change?", "dplmc_chancellor_domestic_policy",#<- dplmc+ added {s0}
[]],
[anyone,"dplmc_chancellor_domestic_policy_ask",[
(assign, ":string", "str_dplmc_neither_centralize_nor_decentralized"),
(faction_get_slot, ":centralization", "fac_player_supporters_faction", dplmc_slot_faction_centralization),
(val_add, ":string", ":centralization"),
(str_store_string, s4, ":string"),
(str_store_string, s4, "@Our goverment is {s4}."),

(assign, ":string", "str_dplmc_neither_aristocratic_nor_plutocratic"),
(faction_get_slot, ":aristocraty", "fac_player_supporters_faction", dplmc_slot_faction_aristocracy),
(val_add, ":string", ":aristocraty"),
(str_store_string, s5, ":string"),
(str_store_string, s5, "@The upper class society is {s5}."),

(assign, ":string", "str_dplmc_mixture_serfs"),
(faction_get_slot, ":serfdom", "fac_player_supporters_faction", dplmc_slot_faction_serfdom),
(val_add, ":string", ":serfdom"),
(str_store_string, s6, ":string"),
(str_store_string, s6, "@Our people are {s6}."),

(assign, ":string", "str_dplmc_mediocre_quality"),
(faction_get_slot, ":quality", "fac_player_supporters_faction", dplmc_slot_faction_quality),
(val_add, ":string", ":quality"),
(str_store_string, s7, ":string"),
(str_store_string, s7, "@Our troops have {s7}."),

##nested diplomacy start+ add mercantilism
(assign, ":string", "str_dplmc_neither_mercantilist_nor_laissez_faire"),
(faction_get_slot, ":mercantilism", "fac_player_supporters_faction", dplmc_slot_faction_mercantilism),
(val_add, ":string", ":mercantilism"),
(str_store_string, s0, ":string"),
(str_store_string, s0, "@Our approach to trade is {s0}."),
##nested diplomacy end+

(store_current_hours, ":current_hours"),
##zParsifal 2011-10-07: Change the policy change interval from always 30 days to (Centralization * 5) + 30 days.
(store_mul, reg1, ":centralization", -5),#Use reg1 for the number of days you have to wait, to display further below.
(val_add, reg1, 30),
(val_clamp, reg1, 15, 46),#This line should be unnecessary
(store_mul, ":policy_time", reg1, 24),
(val_sub, ":current_hours", ":policy_time"),
(faction_get_slot, ":policy_time", "fac_player_supporters_faction", dplmc_slot_faction_policy_time),
(store_sub, ":wait_hours" , ":policy_time", ":current_hours"),
(store_div, ":wait_days", ":wait_hours", 24),
(store_mod, ":wait_mod", ":wait_hours", 24),
(try_begin),
(lt, ":wait_mod", 0),
(val_add, ":wait_days", 1),
(try_end),
(assign, reg0, ":wait_days"),
],
##nested diplomacy start+
"{s4} {s5} {s6} {s7} {s0} We can only change the policy every {reg1} days, the people have to get used to it. We have to wait {reg0} days.",#<- dplmc+ added {s0}
 "dplmc_chancellor_pretalk",[]],
[anyone|plyr,"dplmc_chancellor_domestic_policy",
[
(faction_get_slot, ":serfdom", "fac_player_supporters_faction", dplmc_slot_faction_serfdom),
(lt, ":serfdom", 3),
],
"Bring more people into the peasantry.", "dplmc_chancellor_domestic_policy_confirm",
[
(faction_get_slot, ":serfdom", "fac_player_supporters_faction", dplmc_slot_faction_serfdom),
(val_add, ":serfdom", 1),
(faction_set_slot, "fac_player_supporters_faction", dplmc_slot_faction_serfdom ,":serfdom"),
]],
[anyone|plyr,"dplmc_chancellor_domestic_policy",
[
(faction_get_slot, ":serfdom", "fac_player_supporters_faction", dplmc_slot_faction_serfdom),
(gt, ":serfdom", -3),
],
"I want more freedom for the people.", "dplmc_chancellor_domestic_policy_confirm",
[
(faction_get_slot, ":serfdom", "fac_player_supporters_faction", dplmc_slot_faction_serfdom),
(val_sub, ":serfdom", 1),
(faction_set_slot, "fac_player_supporters_faction", dplmc_slot_faction_serfdom ,":serfdom"),
]],
[anyone|plyr,"dplmc_chancellor_domestic_policy",
[
(faction_get_slot, ":centralization", "fac_player_supporters_faction", dplmc_slot_faction_centralization),
(lt, ":centralization", 3),
],
"Let's centralize the decisions.", "dplmc_chancellor_domestic_policy_confirm",
[
(faction_get_slot, ":centralization", "fac_player_supporters_faction", dplmc_slot_faction_centralization),
(val_add, ":centralization", 1),
(faction_set_slot, "fac_player_supporters_faction", dplmc_slot_faction_centralization,  ":centralization"),
]],
[anyone|plyr,"dplmc_chancellor_domestic_policy",
[
(faction_get_slot, ":centralization", "fac_player_supporters_faction", dplmc_slot_faction_centralization),
(gt, ":centralization", -3),
],
#diplomacy start+
#changed "Give the lords more authority to decide" to "Grant increased autonomy to local regions"
"Grant increased autonomy to local authorities.", "dplmc_chancellor_domestic_policy_confirm",
#diplomacy end+
[
(faction_get_slot, ":centralization", "fac_player_supporters_faction", dplmc_slot_faction_centralization),
(val_sub, ":centralization", 1),
(faction_set_slot,  "fac_player_supporters_faction", dplmc_slot_faction_centralization, ":centralization"),
]],
[anyone|plyr,"dplmc_chancellor_domestic_policy",
[
(faction_get_slot, ":quality", "fac_player_supporters_faction", dplmc_slot_faction_quality),
(lt, ":quality", 3),
],
"I prefer quality troops to many troops.", "dplmc_chancellor_domestic_policy_confirm",
[
(faction_get_slot, ":quality", "fac_player_supporters_faction", dplmc_slot_faction_quality),
(val_add, ":quality", 1),
(faction_set_slot, "fac_player_supporters_faction", dplmc_slot_faction_quality, ":quality"),
]],
[anyone|plyr,"dplmc_chancellor_domestic_policy",
[
(faction_get_slot, ":quality", "fac_player_supporters_faction", dplmc_slot_faction_quality),
(gt, ":quality", -3),
],
#diplomacy start+
"Quantity has a quality of its own.  I prefer many troops to few quality troops.", "dplmc_chancellor_domestic_policy_confirm",
#diplomacy start+
[
(faction_get_slot, ":quality", "fac_player_supporters_faction", dplmc_slot_faction_quality),
(val_sub, ":quality", 1),
(faction_set_slot, "fac_player_supporters_faction", dplmc_slot_faction_quality, ":quality"),
]],
[anyone|plyr,"dplmc_chancellor_domestic_policy",
[
(faction_get_slot, ":aristocraty", "fac_player_supporters_faction", dplmc_slot_faction_aristocracy),
(lt, ":aristocraty", 3),
],
"Give the samurai more power.", "dplmc_chancellor_domestic_policy_confirm",
[
(faction_get_slot, ":aristocraty", "fac_player_supporters_faction", dplmc_slot_faction_aristocracy),
(val_add, ":aristocraty", 1),
(faction_set_slot, "fac_player_supporters_faction", dplmc_slot_faction_aristocracy,  ":aristocraty"),
]],
[anyone|plyr,"dplmc_chancellor_domestic_policy",
[
(faction_get_slot, ":aristocraty", "fac_player_supporters_faction", dplmc_slot_faction_aristocracy),
(gt, ":aristocraty", -3),
],
#diplomacy start+
"Give the merchants and trade guilds more power.", "dplmc_chancellor_domestic_policy_confirm",#dplmc+ edited
#diplomacy end+
[
(faction_get_slot, ":aristocraty", "fac_player_supporters_faction", dplmc_slot_faction_aristocracy),
(val_sub, ":aristocraty", 1),
(faction_set_slot, "fac_player_supporters_faction", dplmc_slot_faction_aristocracy,  ":aristocraty"),
]],
[anyone|plyr,"dplmc_chancellor_domestic_policy",
[
(faction_get_slot, ":mercantilism", "fac_player_supporters_faction", dplmc_slot_faction_mercantilism),
(lt, ":mercantilism", 3),
],
"Manage the economy more actively to increase production and maximize exports.", "dplmc_chancellor_domestic_policy_confirm",
[
(faction_get_slot, ":mercantilism", "fac_player_supporters_faction", dplmc_slot_faction_mercantilism),
(val_add, ":mercantilism", 1),
(faction_set_slot, "fac_player_supporters_faction", dplmc_slot_faction_mercantilism,  ":mercantilism"),
]],
[anyone|plyr,"dplmc_chancellor_domestic_policy",
[
(faction_get_slot, ":mercantilism", "fac_player_supporters_faction", dplmc_slot_faction_mercantilism),
(gt, ":mercantilism", -3),
],
"Reduce the crown's role in managing industry and commerce.", "dplmc_chancellor_domestic_policy_confirm",
[
(faction_get_slot, ":mercantilism", "fac_player_supporters_faction", dplmc_slot_faction_mercantilism),
(val_sub, ":mercantilism", 1),
(faction_set_slot, "fac_player_supporters_faction", dplmc_slot_faction_mercantilism,  ":mercantilism"),
]],
[anyone|plyr,"dplmc_chancellor_domestic_policy",
[],
"Never mind.", "dplmc_chancellor_pretalk",
[]],
[anyone,"dplmc_chancellor_domestic_policy_confirm",
[],
"I will initiate all necessary steps.", "dplmc_chancellor_pretalk",[
(store_current_hours, ":current_hours"),
(faction_set_slot, "fac_player_supporters_faction", dplmc_slot_faction_policy_time, ":current_hours"),
##diplomacy start+
(try_begin),
	(neq, "$players_kingdom", "fac_player_supporters_faction"),
	(is_between, "$players_kingdom", kingdoms_begin, kingdoms_end),
	(try_for_range, ":slot_no", dplmc_slot_faction_policies_begin, dplmc_slot_faction_policies_end),
	   (faction_get_slot, reg0, "fac_player_supporters_faction", ":slot_no"),
		(faction_set_slot, "$players_kingdom", ":slot_no",  reg0),
	(try_end),
(try_end),
##diplomacy end+
]],
[anyone|plyr,"dplmc_chancellor_talk",[
                      ],
"Please give me some information about a lord.", "dplmc_chancellor_info_kingdom_ask",[]],
[anyone,"dplmc_chancellor_info_kingdom_ask",
[],
"Where is he from?", "dplmc_chancellor_info_kingdom_select",[
]],
[anyone|plyr|repeat_for_factions, "dplmc_chancellor_info_kingdom_select",
[
(store_repeat_object, ":faction_no"),
(is_between, ":faction_no", kingdoms_begin, kingdoms_end),
(faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
(str_store_faction_name, s11, ":faction_no"),
],
"{s11}.", "dplmc_chancellor_info_person_ask",
[
(store_repeat_object, "$g_faction_selected"),
]],
[anyone|plyr, "dplmc_chancellor_info_kingdom_select",
[
],
"Never mind.", "dplmc_chancellor_pretalk",[
]],
[anyone,"dplmc_chancellor_info_person_ask",
[],
"About which lord do you want information?", "dplmc_chancellor_info_person_select",[
]],
[anyone|plyr|repeat_for_troops, "dplmc_chancellor_info_person_select",
[
(store_repeat_object, ":troop_no"),
(neq, "$g_talk_troop", ":troop_no"),
(is_between, ":troop_no", active_npcs_begin, kingdom_ladies_end),
(neq, ":troop_no", "trp_player"),
(neg|faction_slot_eq, "$g_faction_selected", slot_faction_leader, ":troop_no"),
(troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
(store_troop_faction, ":faction_no", ":troop_no"),
(eq, "$g_faction_selected", ":faction_no"),
(str_store_troop_name, s1, ":troop_no"),
],"{s1}.", "dplmc_chancellor_info_person",
[
(store_repeat_object, "$lord_selected"),
]],
[anyone|plyr, "dplmc_chancellor_info_person_select",
[
],
"About no one.", "dplmc_chancellor_pretalk",[
]],
[anyone,"dplmc_chancellor_info_person",
[
(call_script, "script_dplmc_troop_political_notes_to_s47", "$lord_selected"),
],
"{s47}", "dplmc_chancellor_pretalk",[
]],
[anyone|plyr,"dplmc_chancellor_talk",[
               (faction_get_slot, ":political_issue", "$players_kingdom", slot_faction_political_issue),
               (is_between, ":political_issue", centers_begin, centers_end),
               (str_store_party_name, s4, ":political_issue"),
                      ],
"What's the mood of the lords regarding the fief of {s4}?", "dplmc_chancellor_cur_stance",[]],
[anyone, "dplmc_chancellor_cur_stance",
[
##diplomacy start+ Handle player is co-ruler of kingdom
(assign, ":alt_faction", "fac_player_supporters_faction"),
(try_begin),
	(is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
	(call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", "$players_kingdom"),
	(ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
	(assign, ":alt_faction", "$players_kingdom"),
(try_end),
##diplomacy end+
(try_for_parties, ":party_no"),
(party_slot_eq, ":party_no", slot_party_type, spt_kingdom_hero_party),
(store_faction_of_party, ":faction_no", ":party_no"),
##diplomacy start+
(this_or_next|eq, ":alt_faction", ":faction_no"),
##diplomacy end+
(eq, "fac_player_supporters_faction", ":faction_no"),
(party_stack_get_troop_id, ":party_leader", ":party_no", 0),
(is_between, ":party_leader", heroes_begin, heroes_end),
(troop_set_slot, ":party_leader", dplmc_slot_troop_political_stance, 0),
(try_end),

(try_for_parties, ":party_no"),
(party_slot_eq, ":party_no", slot_party_type, spt_kingdom_hero_party),
(store_faction_of_party, ":faction_no", ":party_no"),
##diplomacy start+
(this_or_next|eq, ":alt_faction", ":faction_no"),
##diplomacy end+
(eq, "fac_player_supporters_faction", ":faction_no"),
(party_stack_get_troop_id, ":party_leader", ":party_no", 0),
(is_between, ":party_leader", heroes_begin, heroes_end),
(troop_get_slot, ":fav_troop", ":party_leader", slot_troop_stance_on_faction_issue),
(is_between, ":fav_troop", heroes_begin, heroes_end),
(troop_get_slot, ":stance", ":fav_troop", dplmc_slot_troop_political_stance),
(val_add, ":stance", 1),
(troop_set_slot, ":fav_troop", dplmc_slot_troop_political_stance, ":stance"),
(try_end),

(assign, ":report", 0),
(str_store_string, s10, "@According  to the report of our spies"),
(try_for_parties, ":party_no"),
(party_slot_eq, ":party_no", slot_party_type, spt_kingdom_hero_party),
(store_faction_of_party, ":faction_no", ":party_no"),
##diplomacy start+
(this_or_next|eq, ":alt_faction", ":faction_no"),
##diplomacy end+
(eq, "fac_player_supporters_faction", ":faction_no"),
(party_stack_get_troop_id, ":party_leader", ":party_no", 0),
(is_between, ":party_leader", heroes_begin, heroes_end),
(troop_get_slot, ":stance", ":party_leader", dplmc_slot_troop_political_stance),
(try_begin),
  (gt, ":stance", 0),
  (str_store_troop_name, s9, ":party_leader"),
  (assign, reg3, ":stance"),
  (str_store_string, s10, "@{s10} {reg3} lords support {s9}."),
  (assign, ":report", 1),
(try_end),
(try_end),

(try_begin),
(eq, ":report",0),
(str_store_string, s10, "@Sorry, currently I can't provide any information about the lords mood, our spies haven't reported back yet."),
(try_end),
],
"{s10}", "dplmc_chancellor_pretalk",[
]],
[anyone|plyr, "dplmc_chancellor_talk",
[],
"Please send a message to another lord.", "dplmc_chancellor_message_ask_type",
[]],
[anyone, "dplmc_chancellor_message_ask_type",
[
],
"To whom do you like to send the message?", "dplmc_chancellor_message_lord_select",[
]],
[anyone|plyr|repeat_for_troops, "dplmc_chancellor_message_lord_select",
[
(store_repeat_object, ":troop_no"),
(neq, "$g_talk_troop", ":troop_no"),
(is_between, ":troop_no", active_npcs_begin, kingdom_ladies_end),
(neq, ":troop_no", "trp_player"),
(troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
(store_troop_faction, ":faction_no", ":troop_no"),
(eq, "$players_kingdom", ":faction_no"),
(str_store_troop_name, s1, ":troop_no"),

],"{s1}.", "dplmc_chancellor_message_ask",
[
(store_repeat_object, "$lord_selected"),
]],
[anyone|plyr, "dplmc_chancellor_message_lord_select",
[],"Nevermind.", "dplmc_chancellor_pretalk",
[]],
[anyone|plyr, "dplmc_chancellor_gift_lord_select",
[
],
"I can't think of anyone.", "dplmc_chancellor_pretalk",[
]],
[anyone, "dplmc_chancellor_message_ask",
[
(str_store_troop_name, s6, "$lord_selected"),
##diplomacy start+ Save gender to reg4
(assign, reg4, 0),
(try_begin),
(call_script, "script_cf_dplmc_troop_is_female", "$lord_selected"),
(assign, reg4, 1),
(try_end),
##diplomacy end+
],
"What do you want to tell {s6}?", "dplmc_chancellor_message_select",[
]],
[anyone|plyr, "dplmc_chancellor_message_select",
[
],
##diplomacy start+ make gender correct using reg4 (set above)
"Ask {reg4?her:him} if {reg4?she:he} is willing to accompany me in the field.", "dplmc_chancellor_message_lord_ask",
##diplomacy end+
[
(assign, "$temp", spai_accompanying_army),
(assign, "$temp_2", "p_main_party"),
]],
[anyone|plyr, "dplmc_chancellor_message_select",
[
],
##diplomacy start+ make gender correct using reg4 (set above)
"Ask {reg4?her:him} if {reg4?she:he} is willing to go to a location.", "dplmc_chancellor_message_goto_lord_ask",
##diplomacy end+
[
(assign, "$temp", spai_holding_center),
]],
[anyone|plyr, "dplmc_chancellor_message_select",
[
],
##diplomacy start+ make gender correct using reg4 (set above)
"Ask {reg4?her:him} if {reg4?she:he} is willing to patrol a location.", "dplmc_chancellor_message_goto_lord_ask",
##diplomacy end+
[
(assign, "$temp", spai_patrolling_around_center),
]],
[anyone|plyr, "dplmc_chancellor_message_select",
[
],
##diplomacy start+ make gender correct using reg4 (set above)
"Ask {reg4?her:him} if {reg4?she:he} is willing to flee to a location.", "dplmc_chancellor_message_goto_lord_ask",
##diplomacy end+
[
(assign, "$temp", spai_retreating_to_center),
]],
[anyone|plyr, "dplmc_chancellor_message_select",
[
],
##diplomacy start+ make gender correct using reg4 (set above)
"Ask {reg4?her:him} if {reg4?she:he} is willing to besiege a location.", "dplmc_chancellor_message_goto_lord_ask",
##diplomacy end+
[
(assign, "$temp", spai_besieging_center),
]],
[anyone|plyr, "dplmc_chancellor_message_select",
[
],
##diplomacy start+ make gender correct using reg4 (set above)
"Ask {reg4?her:him} if {reg4?she:he} is willing to raid around a location.", "dplmc_chancellor_message_goto_lord_ask",
##diplomacy end+
[
(assign, "$temp", spai_raiding_around_center),
]],
[anyone|plyr, "dplmc_chancellor_message_select",
[
],
"Never mind.", "dplmc_chancellor_pretalk",
[]],
[anyone,"dplmc_chancellor_message_goto_lord_ask", [],
##diplomacy start+ make gender correct using reg4 (set above)
"Where do you order {reg4?her:him}?", "dplmc_chancellor_message_order_details",[]],
[anyone|plyr|repeat_for_parties, "dplmc_chancellor_message_order_details",
[
(store_repeat_object, ":party_no"),
(store_faction_of_party, ":party_faction", ":party_no"),
(store_relation, ":relation", ":party_faction", "$players_kingdom"),
(assign, ":continue", 0),
(try_begin),
 (this_or_next|eq, "$temp", spai_retreating_to_center),
   (eq, "$temp", spai_holding_center),
 (try_begin),
   (this_or_next|party_slot_eq, ":party_no", slot_party_type, spt_castle),
   (party_slot_eq, ":party_no", slot_party_type, spt_town),
   (eq, ":party_faction", "$players_kingdom"),
   (assign, ":continue", 1),
 (try_end),
(else_try),
 (eq, "$temp", spai_raiding_around_center),
 (try_begin),
   (party_slot_eq, ":party_no", slot_party_type, spt_village),
   (lt, ":relation", 0),
   (assign, ":continue", 1),
 (try_end),
(else_try),
 (eq, "$temp", spai_besieging_center),
 (try_begin),
   (this_or_next|party_slot_eq, ":party_no", slot_party_type, spt_castle),
   (party_slot_eq, ":party_no", slot_party_type, spt_town),
 (party_slot_eq, ":party_no", slot_center_is_besieged_by, -1),
   (lt, ":relation", 0),
   (assign, ":continue", 1),
 (try_end),


(else_try),
 (eq, "$temp", spai_patrolling_around_center),
 (try_begin),
   (eq, ":party_faction", "$players_kingdom"),
   (is_between, ":party_no", centers_begin, centers_end),
   (assign, ":continue", 1),
(else_try),
   (is_between, ":party_no", centers_begin, centers_end),

 (store_distance_to_party_from_party, ":distance", ":party_no", "p_main_party"),
 (le, ":distance", 25),
   (assign, ":continue", 1),

 (try_end),
(try_end),
(eq, ":continue", 1),
(neq, ":party_no", "$g_encountered_party"),
(str_store_party_name, s1, ":party_no")],
"{s1}", "dplmc_chancellor_message_lord_ask",
[
(store_repeat_object, "$temp_2"),
(store_current_hours, ":hours"),
(party_set_slot, "$g_talk_troop_party", slot_party_following_orders_of_troop, "trp_kingdom_heroes_including_player_begin"),
(party_set_slot, "$g_talk_troop_party", slot_party_orders_type, "$temp"),
(party_set_slot, "$g_talk_troop_party", slot_party_orders_object, "$temp_2"),
(party_set_slot, "$g_talk_troop_party", slot_party_orders_time, ":hours"),

]],
[anyone|plyr, "dplmc_chancellor_message_order_details",
[
],
"Nowhere.", "dplmc_chancellor_pretalk",
[]],
[anyone, "dplmc_chancellor_message_lord_ask",
[
##diplomacy start+ make center correct
(assign, reg4, 0),
(try_begin),
(call_script, "script_cf_dplmc_troop_is_female", "$lord_selected"),
(assign, reg4, 1),
(try_end),
##diplomacy end+
(eq, "$temp", spai_accompanying_army),
(str_store_troop_name, s11, "$lord_selected"),
],
##diplomacy start+ make gender correct using reg4 (set above)
"Of course, I will send a messenger to {s11} and ask {reg4?her:him} if {reg4?she:he} is willing to accompany you in the field.", "dplmc_message_send_confirm",[
##diplomacy end+
]],
[anyone, "dplmc_chancellor_message_lord_ask",
[
(eq, "$temp", spai_holding_center),
(str_store_troop_name, s11, "$lord_selected"),
(str_store_party_name, s12, "$temp_2"),
],
##diplomacy start+ make gender correct using reg4 (set above)
"Of course, I will send a messenger to {s11} and ask {reg4?her:him} if {reg4?she:he} is willing to go to {s12}.", "dplmc_message_send_confirm",[
##diplomacy end+
]],
[anyone, "dplmc_chancellor_message_lord_ask",
[
(eq, "$temp", spai_patrolling_around_center),
(str_store_troop_name, s11, "$lord_selected"),
(str_store_party_name, s12, "$temp_2"),
],
##diplomacy start+ make gender correct using reg4 (set above)
"Of course, I will send a messenger to {s11} and ask {reg4?her:him} if {reg4?she:he} is willing to patrol around {s12}.", "dplmc_message_send_confirm",[
##diplomacy end+
]],
[anyone, "dplmc_chancellor_message_lord_ask",
[
(eq, "$temp", spai_retreating_to_center),
(str_store_troop_name, s11, "$lord_selected"),
(str_store_party_name, s12, "$temp_2"),
],
##diplomacy start+ make gender correct using reg4 (set above)
"Of course, I will send a messenger to {s11} and ask {reg4?her:him} if {reg4?she:he} is willing to retreat to {s12}.", "dplmc_message_send_confirm",[
##diplomacy end+
]],
[anyone, "dplmc_chancellor_message_lord_ask",
[
(eq, "$temp", spai_besieging_center),
(str_store_troop_name, s11, "$lord_selected"),
(str_store_party_name, s12, "$temp_2"),
],
##diplomacy start+ make gender correct using reg4 (set above)
"Of course, I will send a messenger to {s11} and ask {reg4?her:him} if {reg4?she:he} is willing to besiege {s12}.", "dplmc_message_send_confirm",[
##diplomacy end+
]],
[anyone, "dplmc_chancellor_message_lord_ask",
[
(eq, "$temp", spai_raiding_around_center),
(str_store_troop_name, s11, "$lord_selected"),
(str_store_party_name, s12, "$temp_2"),
],
##diplomacy start+ make gender correct using reg4 (set above)
"Of course, I will send a messenger to {s11} and ask {reg4?her:him} if {reg4?she:he} is willing to raid around {s12}.", "dplmc_message_send_confirm",[
##diplomacy end+
]],
[anyone|plyr, "dplmc_message_send_confirm",
[
],
"Thank you.", "dplmc_chancellor_pretalk",[
(call_script, "script_dplmc_send_messenger_to_troop", "$lord_selected", "$temp", "$temp_2"),
]],
[anyone|plyr, "dplmc_message_send_confirm",
[
],
"I changed my mind.", "dplmc_chancellor_pretalk",[
]],
[anyone|plyr, "dplmc_chancellor_talk",
[],
"Please send a gift.", "dplmc_chancellor_gift_ask_where",
[]],
[anyone, "dplmc_chancellor_gift_ask_where",
[
(store_troop_gold, ":gold", "trp_household_possessions"),
(le, ":gold", 50),
],
"We don't have enough money in our treasury to send a gift! It will cost us 50 mon to send a gift.", "dplmc_chancellor_pretalk",
[]],
[anyone, "dplmc_chancellor_gift_ask_where",
[
(store_troop_gold, ":gold", "trp_household_possessions"),
(ge, ":gold", 50),
],
"Sending a gift will cost us 50 mon. I will withdraw the money from the treasury. Do you want to send your gift to a person or a settlement?", "dplmc_chancellor_gift_where",
[]],
[anyone|plyr, "dplmc_chancellor_gift_where",
[],
"To a person.", "dplmc_chancellor_gift_ask_person",
[]],
[anyone|plyr, "dplmc_chancellor_gift_where",
[],
"To a settlement.", "dplmc_chancellor_center_gift_ask_type",
[]],
[anyone|plyr, "dplmc_chancellor_gift_where",
[],
"Nowhere.", "dplmc_chancellor_pretalk",
[]],
[anyone, "dplmc_chancellor_center_gift_ask_type",
[
],
"I recommend to send 300 units of sea fish, tofu, or natto. If we have enough in our household I will induce a servant to deliver it.", "dplmc_chancellor_center_gift_select",[
]],
[anyone|plyr, "dplmc_chancellor_center_gift_select",
[
(troop_get_inventory_capacity, ":capacity", "trp_household_possessions"),
(assign, ":amount", 0),
(try_for_range, ":inventory_slot", 0, ":capacity"),
  (troop_get_inventory_slot, ":item", "trp_household_possessions", ":inventory_slot"),
  (eq, ":item", "itm_smoked_fish"),
  (troop_inventory_slot_get_item_amount, ":tmp_amount", "trp_household_possessions", ":inventory_slot"),
  (val_add, ":amount", ":tmp_amount"),
(try_end),
(ge, ":amount", 300),
],
"Send some fish.", "dplmc_chancellor_center_gift_kingdom_ask",[
(assign, "$diplomacy_var", "itm_smoked_fish"),
(assign, "$diplomacy_var2", 300),
]],
[anyone|plyr, "dplmc_chancellor_center_gift_select",
[
(troop_get_inventory_capacity, ":capacity", "trp_household_possessions"),
(assign, ":amount", 0),
(try_for_range, ":inventory_slot", 0, ":capacity"),
  (troop_get_inventory_slot, ":item", "trp_household_possessions", ":inventory_slot"),
  (eq, ":item", "itm_cheese"),
  (troop_inventory_slot_get_item_amount, ":tmp_amount", "trp_household_possessions", ":inventory_slot"),
(val_add, ":amount", ":tmp_amount"),
(try_end),
(ge, ":amount", 300),
],
"Send some tofu.", "dplmc_chancellor_center_gift_kingdom_ask",[
(assign, "$diplomacy_var", "itm_cheese"),
(assign, "$diplomacy_var2", 300),
]],
[anyone|plyr, "dplmc_chancellor_center_gift_select",
[
(troop_get_inventory_capacity, ":capacity", "trp_household_possessions"),
(assign, ":amount", 0),
(try_for_range, ":inventory_slot", 0, ":capacity"),
  (troop_get_inventory_slot, ":item", "trp_household_possessions", ":inventory_slot"),
  (eq, ":item", "itm_honey"),
  (troop_inventory_slot_get_item_amount, ":tmp_amount", "trp_household_possessions", ":inventory_slot"),
(val_add, ":amount", ":tmp_amount"),
(try_end),
(ge, ":amount", 300),
],
"Send some natto.", "dplmc_chancellor_center_gift_kingdom_ask",[
(assign, "$diplomacy_var", "itm_honey"),
(assign, "$diplomacy_var2", 300),
]],
[anyone|plyr, "dplmc_chancellor_center_gift_select",
[
],
"Never mind.", "dplmc_chancellor_pretalk",[
]],
[anyone, "dplmc_chancellor_center_gift_kingdom_ask",
[
],
"Where is the settlement?", "dplmc_chancellor_center_gift_kingdom_select",[
]],
[anyone|plyr|repeat_for_factions, "dplmc_chancellor_center_gift_kingdom_select",
[
(store_repeat_object, ":faction_no"),
(is_between, ":faction_no", kingdoms_begin, kingdoms_end),
(faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
(str_store_faction_name, s11, ":faction_no"),
],
"In {s11}.", "dplmc_chancellor_center_gift_lord_ask",
[
(store_repeat_object, "$g_faction_selected"),
]],
[anyone|plyr, "dplmc_chancellor_center_gift_kingdom_select",
[
],
"Never mind.", "dplmc_chancellor_pretalk",[
]],
[anyone, "dplmc_chancellor_center_gift_lord_ask",
[
(is_between, "$g_faction_selected", npc_kingdoms_begin, npc_kingdoms_end),
(neg|is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
(store_relation, reg0, "$players_kingdom", "$g_faction_selected"),
(lt, reg0, 0),
(neg|faction_slot_ge, "$g_faction_selected", slot_faction_recognized_player, 1),
],
"Given that we are currently at war with the {s11} and they do not officially recognize your legitimacy, any messengers we sent would run the risk of being hanged as bandits.", "dplmc_chancellor_pretalk",[
]],
[anyone, "dplmc_chancellor_center_gift_lord_ask",
[
],
"To which settlement do you like to send the gift?", "dplmc_chancellor_center_gift_lord_select",[
]],
[anyone|plyr|repeat_for_parties, "dplmc_chancellor_center_gift_lord_select",
[
(store_repeat_object, ":party_no"),
(this_or_next|party_slot_eq, ":party_no", slot_party_type, spt_town),
(party_slot_eq, ":party_no", slot_party_type, spt_village),
(store_faction_of_party, ":faction_no", ":party_no"),
(eq, ":faction_no", "$g_faction_selected"),
(str_store_party_name, s11, ":party_no"),

],"{s11}.", "dplmc_chancellor_center_gift_send_ask",
[
(store_repeat_object, "$lord_selected"),
]],
[anyone|plyr, "dplmc_chancellor_center_gift_lord_select",
[
],
"I changed my mind.", "dplmc_chancellor_pretalk",[
]],
[anyone, "dplmc_chancellor_center_gift_send_ask",
[
(str_store_item_name,s6,"$diplomacy_var"),
(str_store_party_name, s11, "$lord_selected"),
],
"I will send a servant with the {s6} to {s11}.", "dplmc_chancellor_center_gift_send_confirm",[

]],
[anyone|plyr, "dplmc_chancellor_center_gift_send_confirm",
[
],
"Thank you.", "dplmc_chancellor_pretalk",[
(call_script, "script_dplmc_send_gift_to_center", "$lord_selected", "$diplomacy_var", "$diplomacy_var2"),
]],
[anyone|plyr, "dplmc_chancellor_center_gift_send_confirm",
[
],
"Never mind.", "dplmc_chancellor_pretalk",[
]],
[anyone, "dplmc_chancellor_gift_ask_person",
[],
"Do you want to send your gift to a lady or to a lord?.", "dplmc_chancellor_gift_lady_or_lord",
[]],
[anyone|plyr, "dplmc_chancellor_gift_lady_or_lord",
[],
"Please send a gift to a lord.", "dplmc_chancellor_gift_ask_type",
[]],
[anyone, "dplmc_chancellor_gift_ask_type",
[
],
"I recommend to send 150 units of Sake, Soy Sauce or Fish Sauce. If we have enough in our household I will induce a servant to deliver it.", "dplmc_chancellor_gift_select",[
]],
[anyone|plyr, "dplmc_chancellor_gift_select",
[
(troop_get_inventory_capacity, ":capacity", "trp_household_possessions"),
(assign, ":amount", 0),
(try_for_range, ":inventory_slot", 0, ":capacity"),
  (troop_get_inventory_slot, ":item", "trp_household_possessions", ":inventory_slot"),
  (eq, ":item", "itm_ale"),
  (troop_inventory_slot_get_item_amount, ":tmp_amount", "trp_household_possessions", ":inventory_slot"),
  (val_add, ":amount", ":tmp_amount"),
(try_end),
(ge, ":amount", 150),
],
"Send some sake.", "dplmc_chancellor_gift_kingdom_ask",[
(assign, "$diplomacy_var", "itm_ale"),
(assign, "$diplomacy_var2", 150),
]],
[anyone|plyr, "dplmc_chancellor_gift_select",
[
(troop_get_inventory_capacity, ":capacity", "trp_household_possessions"),
(assign, ":amount", 0),
(try_for_range, ":inventory_slot", 0, ":capacity"),
  (troop_get_inventory_slot, ":item", "trp_household_possessions", ":inventory_slot"),
  (eq, ":item", "itm_wine"),
  (troop_inventory_slot_get_item_amount, ":tmp_amount", "trp_household_possessions", ":inventory_slot"),
(val_add, ":amount", ":tmp_amount"),
(try_end),
(ge, ":amount", 150),
],
"Send some soy sauce.", "dplmc_chancellor_gift_kingdom_ask",[
(assign, "$diplomacy_var", "itm_wine"),
(assign, "$diplomacy_var2", 150),
]],
[anyone|plyr, "dplmc_chancellor_gift_select",
[
(troop_get_inventory_capacity, ":capacity", "trp_household_possessions"),
(assign, ":amount", 0),
(try_for_range, ":inventory_slot", 0, ":capacity"),
  (troop_get_inventory_slot, ":item", "trp_household_possessions", ":inventory_slot"),
  (eq, ":item", "itm_oil"),
  (troop_inventory_slot_get_item_amount, ":tmp_amount", "trp_household_possessions", ":inventory_slot"),
(val_add, ":amount", ":tmp_amount"),
(try_end),
(ge, ":amount", 150),
],
"Send some fish sauce.", "dplmc_chancellor_gift_kingdom_ask",[
(assign, "$diplomacy_var", "itm_oil"),
(assign, "$diplomacy_var2", 150),
]],
[anyone|plyr, "dplmc_chancellor_gift_select",
[
],
"Never mind.", "dplmc_chancellor_pretalk",[
]],
[anyone, "dplmc_chancellor_gift_kingdom_ask",
[
],
"Where does the lord live whom you want to make a present?", "dplmc_chancellor_gift_kingdom_select",[
]],
[anyone|plyr|repeat_for_factions, "dplmc_chancellor_gift_kingdom_select",
[
(store_repeat_object, ":faction_no"),
(is_between, ":faction_no", kingdoms_begin, kingdoms_end),
(faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
(str_store_faction_name, s11, ":faction_no"),
],
"In {s11}.", "dplmc_chancellor_gift_lord_ask",
[
(store_repeat_object, "$g_faction_selected"),
]],
[anyone|plyr, "dplmc_chancellor_gift_kingdom_select",
[
],
"Never mind.", "dplmc_chancellor_pretalk",[
]],
[anyone, "dplmc_chancellor_gift_lord_ask",
[
(is_between, "$g_faction_selected", npc_kingdoms_begin, npc_kingdoms_end),
(neg|is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
(store_relation, reg0, "$players_kingdom", "$g_faction_selected"),
(lt, reg0, 0),
(neg|faction_slot_ge, "$g_faction_selected", slot_faction_recognized_player, 1),
],
"Given that we are currently at war with the {s11} but they do not officially recognize your legitimacy, any messengers we sent would run the risk of being hanged as bandits.", "dplmc_chancellor_pretalk",[
]],
[anyone, "dplmc_chancellor_gift_lord_ask",
[
],
"To whom do you like to send the gift?", "dplmc_chancellor_gift_lord_select",[
]],
[anyone|plyr|repeat_for_troops, "dplmc_chancellor_gift_lord_select",
[
(store_repeat_object, ":troop_no"),
(troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
(neg|troop_slot_ge, ":troop_no", slot_troop_prisoner_of_party, 0),
(troop_slot_eq, ":troop_no", slot_troop_met, 1),
(neq, "trp_player", ":troop_no"),
(troop_get_slot, ":target_party", ":troop_no", slot_troop_leaded_party),
(gt, ":target_party", 0),
(store_troop_faction, ":faction_no", ":troop_no"),
(eq, ":faction_no", "$g_faction_selected"),
(str_store_troop_name, s11, ":troop_no"),

],"{s11}.", "dplmc_chancellor_gift_send_ask",
[
(store_repeat_object, "$lord_selected"),
]],
[anyone|plyr, "dplmc_chancellor_gift_lord_select",
[
],
"I can't think of anyone.", "dplmc_chancellor_pretalk",[
]],
[anyone, "dplmc_chancellor_gift_send_ask",
[
(str_store_item_name,s6,"$diplomacy_var"),
(str_store_troop_name, s11, "$lord_selected"),
],
"I will send a servant with the {s6} to {s11}.", "dplmc_chancellor_gift_send_confirm",[

]],
[anyone|plyr, "dplmc_chancellor_gift_send_confirm",
[
],
"Thank you.", "dplmc_chancellor_pretalk",[
(call_script, "script_dplmc_send_gift", "$lord_selected", "$diplomacy_var", "$diplomacy_var2"),
]],
[anyone|plyr, "dplmc_chancellor_gift_send_confirm",
[
],
"Never mind.", "dplmc_chancellor_pretalk",[
]],
[anyone|plyr, "dplmc_chancellor_gift_lady_or_lord",
[],
"Please send a gift to a lady.", "dplmc_chancellor_lady_gift_ask_type",
[]],
[anyone|plyr, "dplmc_chancellor_gift_lady_or_lord",
[],
"Never mind.", "dplmc_chancellor_pretalk",
[]],
[anyone, "dplmc_chancellor_lady_gift_ask_type",
[
],
"I recommend to send dyes, raw silk, or finished silk. If we have enough in our household I will induce a servant to deliver it.", "dplmc_chancellor_lady_gift_select",[
]],
[anyone|plyr, "dplmc_chancellor_lady_gift_select",
[
(troop_get_inventory_capacity, ":capacity", "trp_household_possessions"),
(assign, ":amount", 0),
(try_for_range, ":inventory_slot", 0, ":capacity"),
  (troop_get_inventory_slot, ":item", "trp_household_possessions", ":inventory_slot"),
  (eq, ":item", "itm_raw_dyes"),
  (val_add, ":amount", 1),
(try_end),
(ge, ":amount", 1),
],
"Send dyes.", "dplmc_chancellor_lady_gift_kingdom_ask",[
(assign, "$diplomacy_var", "itm_raw_dyes"),
(assign, "$diplomacy_var2", 1),
]],
[anyone|plyr, "dplmc_chancellor_lady_gift_select",
[
(troop_get_inventory_capacity, ":capacity", "trp_household_possessions"),
(assign, ":amount", 0),
(try_for_range, ":inventory_slot", 0, ":capacity"),
  (troop_get_inventory_slot, ":item", "trp_household_possessions", ":inventory_slot"),
  (eq, ":item", "itm_raw_silk"),
  (val_add, ":amount", 1),
(try_end),
(ge, ":amount", 1),
],
"Send raw silk.", "dplmc_chancellor_lady_gift_kingdom_ask",[
(assign, "$diplomacy_var", "itm_raw_silk"),
(assign, "$diplomacy_var2", 1),
]],
[anyone|plyr, "dplmc_chancellor_lady_gift_select",
[
(troop_get_inventory_capacity, ":capacity", "trp_household_possessions"),
(assign, ":amount", 0),
(try_for_range, ":inventory_slot", 0, ":capacity"),
  (troop_get_inventory_slot, ":item", "trp_household_possessions", ":inventory_slot"),
  (eq, ":item", "itm_velvet"),
  (val_add, ":amount", 1),
(try_end),
(ge, ":amount", 1),
],
"Send finished silk.", "dplmc_chancellor_lady_gift_kingdom_ask",[
(assign, "$diplomacy_var", "itm_velvet"),
(assign, "$diplomacy_var2", 1),
]],
[anyone|plyr, "dplmc_chancellor_lady_gift_select",
[
],
"Never mind.", "dplmc_chancellor_pretalk",[
]],
[anyone, "dplmc_chancellor_lady_gift_kingdom_ask",
[
],
"Where does the lady live?", "dplmc_chancellor_lady_gift_kingdom_select",[
]],
[anyone|plyr|repeat_for_factions, "dplmc_chancellor_lady_gift_kingdom_select",
[
(store_repeat_object, ":faction_no"),
(is_between, ":faction_no", kingdoms_begin, kingdoms_end),
(faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
(str_store_faction_name, s11, ":faction_no"),
],
"In {s11}.", "dplmc_chancellor_lady_gift_lady_ask",
[
(store_repeat_object, "$g_faction_selected"),
]],
[anyone|plyr, "dplmc_chancellor_lady_gift_kingdom_select",
[
],
"Never mind.", "dplmc_chancellor_pretalk",[
]],
[anyone, "dplmc_chancellor_lady_gift_lady_ask",
[
(is_between, "$g_faction_selected", npc_kingdoms_begin, npc_kingdoms_end),
(neg|is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
(store_relation, reg0, "$players_kingdom", "$g_faction_selected"),
(lt, reg0, 0),
(neg|faction_slot_ge, "$g_faction_selected", slot_faction_recognized_player, 1),
],
"Given that we are currently at war with the {s11} but they do not officially recognize your legitimacy, any messengers we sent would run the risk of being hanged as bandits.", "dplmc_chancellor_pretalk",[
]],
[anyone, "dplmc_chancellor_lady_gift_lady_ask",
[
],
"Which lady should receive the gift?", "dplmc_chancellor_lady_gift_lady_select",[
]],
[anyone|plyr|repeat_for_troops, "dplmc_chancellor_lady_gift_lady_select",
[
(store_repeat_object, ":troop_no"),
(troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_lady),
(neg|troop_slot_ge, ":troop_no", slot_troop_prisoner_of_party, 0),
(troop_slot_eq, ":troop_no", slot_troop_met, 1),
(neq, "trp_player", ":troop_no"),
(store_troop_faction, ":faction_no", ":troop_no"),
(eq, ":faction_no", "$g_faction_selected"),
(str_store_troop_name, s11, ":troop_no"),

],"{s11}.", "dplmc_chancellor_lady_gift_send_ask",
[
(store_repeat_object, "$lord_selected"),
]],
[anyone|plyr, "dplmc_chancellor_lady_gift_lady_select",
[
],
"I can't think of anyone.", "dplmc_chancellor_pretalk",[
]],
[anyone, "dplmc_chancellor_lady_gift_send_ask",
[
(str_store_item_name,s6,"$diplomacy_var"),
(str_store_troop_name, s11, "$lord_selected"),
],
"I will send a servant with the {s6} to {s11}.", "dplmc_chancellor_lady_gift_send_confirm",[

]],
[anyone|plyr, "dplmc_chancellor_lady_gift_send_confirm",
[
],
"Thank you.", "dplmc_chancellor_pretalk",[
(call_script, "script_dplmc_send_gift", "$lord_selected", "$diplomacy_var", "$diplomacy_var2"),
]],
[anyone|plyr, "dplmc_chancellor_lady_gift_send_confirm",
[
],
"Never mind.", "dplmc_chancellor_pretalk",[
]],
[anyone|plyr, "dplmc_chancellor_talk",
[
],
"Let us check our household possessions.", "dplmc_chancellor_talk_household",[
(change_screen_loot, "trp_household_possessions"),
]],
[anyone, "dplmc_chancellor_talk_household",
[
],
"You should store all important things in the household.", "dplmc_chancellor_pretalk",[
]],
[anyone|plyr, "dplmc_chancellor_talk",
[(eq, 0, 1),],
"I would like to take a look through the items in my secondary storage houses.", "dplmc_chancellor_pretalk",
[(change_screen_loot, "trp_dplmc_chancellor"),]],
[anyone|plyr, "dplmc_chancellor_talk",
[],
"I no longer need your services.", "dplmc_chancellor_dismiss_confirm_ask",
[]],
[anyone, "dplmc_chancellor_dismiss_confirm_ask",
[
],
"Are you sure that you don't need me anymore?", "dplmc_chancellor_dismiss_confirm",
[]],
[anyone|plyr, "dplmc_chancellor_dismiss_confirm",
[
],
"Yes I am.", "dplmc_chancellor_dismiss_confirm_yes",
[]],
[anyone, "dplmc_chancellor_dismiss_confirm_yes",
[
],
"As you wish.", "close_window",
[
(assign, "$g_player_chancellor", -1),
]],
[anyone|plyr, "dplmc_chancellor_dismiss_confirm",
[
],
"No I am not.", "dplmc_chancellor_pretalk",
[]],
[anyone|plyr, "dplmc_chancellor_talk",
[],
"Farewell!", "close_window",
[]],
[anyone,"dplmc_constable_pretalk",
##diplomacy start+ Replace "Sire" with {s0}
#[],
#"Do you need anything else, Sire?", "dplmc_constable_talk",[
[(call_script, "script_dplmc_print_subordinate_says_sir_madame_to_s0"),
],
"Do you need anything else, {s0}?", "dplmc_constable_talk",[
##diplomacy end+
]],
[anyone|plyr,"dplmc_constable_talk", [],
"How goes the war?", "dplmc_constable_talk_ask_war",[]],
[anyone,"dplmc_constable_talk_ask_war", [],
"{s12}", "dplmc_constable_talk_ask_war_2",
[
(assign, ":num_enemies", 0),
(try_for_range_backwards, ":cur_faction", kingdoms_begin, kingdoms_end),
(faction_slot_eq, ":cur_faction", slot_faction_state, sfs_active),
(store_relation, ":cur_relation", ":cur_faction", "fac_player_supporters_faction"),
(lt, ":cur_relation", 0),
(try_begin),
  (eq, ":num_enemies", 0),
  (str_store_faction_name_link, s12, ":cur_faction"),
(else_try),
  (eq, ":num_enemies", 1),
  (str_store_faction_name_link, s11, ":cur_faction"),
  (str_store_string, s12, "@{s11} and {s12}"),
(else_try),
  (str_store_faction_name_link, s11, ":cur_faction"),
  (str_store_string, s12, "@{!}{s11}, {s12}"),
(try_end),
(val_add, ":num_enemies", 1),
(try_end),
(try_begin),
(eq, ":num_enemies", 0),
(str_store_string, s12, "@We are not at war with anyone."),
(else_try),
(str_store_string, s12, "@We are at war with {s12}."),
(try_end),
]],
[anyone|plyr|repeat_for_factions, "dplmc_constable_talk_ask_war_2", [(store_repeat_object, ":faction_no"),
                                                            (is_between, ":faction_no", kingdoms_begin, kingdoms_end),
                                                            (faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
                                                               (store_relation, ":cur_relation", ":faction_no", "fac_player_supporters_faction"),
                                                               (lt, ":cur_relation", 0),
                                                               (str_store_faction_name, s1, ":faction_no")],
"Tell me more about the war with {s1}.", "dplmc_constable_talk_ask_war_details",[(store_repeat_object, "$faction_requested_to_learn_more_details_about_the_war_against")]],
[anyone|plyr,"dplmc_constable_talk_ask_war_2", [], "That's all I wanted to know. Thank you.", "dplmc_constable_pretalk",[]],
[anyone,"dplmc_constable_talk_ask_war_details", [],
"{!}{s9}.",
"dplmc_constable_talk_ask_war_2",
[
(store_add, ":war_damage_slot", "$faction_requested_to_learn_more_details_about_the_war_against", slot_faction_war_damage_inflicted_on_factions_begin),
(val_sub, ":war_damage_slot", kingdoms_begin),
 (faction_get_slot, ":war_damage_inflicted", "fac_player_supporters_faction", ":war_damage_slot"),

(store_add, ":war_damage_slot", "fac_player_supporters_faction", slot_faction_war_damage_inflicted_on_factions_begin),
(val_sub, ":war_damage_slot", kingdoms_begin),
 (faction_get_slot, ":war_damage_suffered", "$faction_requested_to_learn_more_details_about_the_war_against", ":war_damage_slot"),

(val_max, ":war_damage_suffered", 1),

(store_mul, ":war_damage_ratio", ":war_damage_inflicted", 100),
(val_div, ":war_damage_ratio", ":war_damage_suffered"),

(try_begin),
   (eq, "$cheat_mode", 1),
   (assign, reg3, ":war_damage_inflicted"),
   (assign, reg4, ":war_damage_suffered"),
   (assign, reg5, ":war_damage_ratio"),
   (display_message, "str_war_damage_inflicted_reg3_suffered_reg4_ratio_reg5"),
(try_end),

(str_store_string, s9, "str_error__did_not_calculate_war_progress_string_properly"),
(try_begin),
   (lt, ":war_damage_inflicted", 5),
   (str_store_string, s9, "str_the_war_has_barely_begun_so_and_it_is_too_early_to_say_who_is_winning_and_who_is_losing"),
(else_try),
   (gt, ":war_damage_inflicted", 100),
   (gt, ":war_damage_ratio", 200),
   (str_store_string, s9, "str_we_have_been_hitting_them_very_hard_and_giving_them_little_chance_to_recover"),
(else_try),
   (gt, ":war_damage_inflicted", 80),
   (gt, ":war_damage_ratio", 150),
   (str_store_string, s9, "str_the_fighting_has_been_hard_but_we_have_definitely_been_getting_the_better_of_them"),
(else_try),
   (gt, ":war_damage_suffered", 100),
   (lt, ":war_damage_ratio", 50),
   (str_store_string, s9, "str_they_have_been_hitting_us_very_hard_and_causing_great_suffering"),
(else_try),
   (gt, ":war_damage_suffered", 80),
   (lt, ":war_damage_ratio", 68),
   (str_store_string, s9, "str_the_fighting_has_been_hard_and_i_am_afraid_that_we_have_been_having_the_worst_of_it"),
(else_try),
   (gt, ":war_damage_suffered", 50),
   (gt, ":war_damage_inflicted", 50),
   (gt, ":war_damage_ratio", 65),
   (str_store_string, s9, "str_both_sides_have_suffered_in_the_fighting"),
(else_try),
   (gt, ":war_damage_ratio", 125),
   (str_store_string, s9, "str_no_clear_winner_has_yet_emerged_in_the_fighting_but_i_think_we_are_getting_the_better_of_them"),
(else_try),
   (gt, ":war_damage_ratio", 80),
   (str_store_string, s9, "str_no_clear_winner_has_yet_emerged_in_the_fighting_but_i_fear_they_may_be_getting_the_better_of_us"),
(else_try),
   (str_store_string, s9, "str_no_clear_winner_has_yet_emerged_in_the_fighting"),
(try_end),

(try_begin),
   (neg|faction_slot_eq, "fac_player_supporters_faction", slot_faction_leader, "$g_talk_troop"),
   (call_script, "script_npc_decision_checklist_peace_or_war", "$players_kingdom", "$faction_requested_to_learn_more_details_about_the_war_against", -1),
   (str_store_string, s9, "str_s9_s14"),
  (try_end),
]],
[anyone|plyr, "dplmc_constable_talk",
[],
"I want information about a settlement.", "dplmc_constable_scout_ask",
[]],
[anyone, "dplmc_constable_scout_ask",
[
],
"We can send a spy which will cost you 300 mon. Where do you want to send the spy?", "dplmc_constable_scout_location",[
]],
[anyone|plyr|repeat_for_factions, "dplmc_constable_scout_location",
[
(store_troop_gold, ":cur_gold", "trp_household_possessions"),
(ge, ":cur_gold", 300),
(store_repeat_object, ":faction"),
(is_between, ":faction", kingdoms_begin, kingdoms_end),
(str_store_faction_name, s11, ":faction"),
],
"{!}{s11}.", "dplmc_constable_scout_location_confirm_ask",
[
(store_repeat_object, "$diplomacy_var"),
]
],
[anyone|plyr, "dplmc_constable_scout_location",
[],
"I changed my mind.", "dplmc_constable_pretalk",
[]],
[anyone, "dplmc_constable_scout_location_confirm_ask",
[
],
"Which settlement do you want to spy out?", "dplmc_constable_scout_location2",[
]],
[anyone|plyr|repeat_for_parties, "dplmc_constable_scout_location2",
[
(store_repeat_object, ":party_no"),
(is_between, ":party_no", walled_centers_begin, walled_centers_end),
(store_faction_of_party, ":faction", ":party_no"),
(eq, ":faction", "$diplomacy_var"),
(str_store_party_name, s11, ":party_no"),
],
"{!}{s11}.", "dplmc_constable_scout_location_confirm_ask2",
[
(store_repeat_object, "$diplomacy_var"),
]
],
[anyone|plyr, "dplmc_constable_scout_location2",
[],
"I changed my mind.", "dplmc_constable_pretalk",
[]],
[anyone, "dplmc_constable_scout_location_confirm_ask2",
[(str_store_party_name, s11, "$diplomacy_var"),
],
"As you wish, I will send a spy to {s11} and withdraw 300 mon from your treasury.", "dplmc_constable_scout_location_confirm",[
]],
[anyone|plyr, "dplmc_constable_scout_location_confirm",
[
],
"Great.", "dplmc_constable_pretalk",
[  (call_script, "script_dplmc_withdraw_from_treasury", 300),
(call_script, "script_dplmc_send_scout_party", "$current_town", "$diplomacy_var", "$players_kingdom"),
]],
[anyone|plyr, "dplmc_constable_scout_location_confirm",
[],
"Hold on!", "dplmc_constable_pretalk",
[]],
[anyone|plyr,"dplmc_constable_talk", [],
"I want to release a prisoner.", "dplmc_constable_talk_ask_prisoner",[]],
[anyone,"dplmc_constable_talk_ask_prisoner",
[],
"Alright, which prisoner do you want to release?", "dplmc_constable_talk_prisoner_select",[
]],
[anyone|plyr|repeat_for_troops, "dplmc_constable_talk_prisoner_select",
[
(store_repeat_object, ":troop_no"),
(troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
(is_between, ":troop_no", kings_begin, lords_end),
(troop_get_slot, ":party", ":troop_no", slot_troop_prisoner_of_party),

(assign, ":can_release", 0),
(try_begin),
(is_between, ":party", walled_centers_begin, walled_centers_end),
(party_slot_eq, ":party", slot_town_lord, "trp_player"),
(assign, ":can_release", 1),
(else_try),
(eq, ":party", "p_main_party"),
(assign, ":can_release", 1),
(try_end),
(eq, ":can_release", 1),

(str_store_troop_name, s10, ":troop_no"),
(store_faction_of_troop, ":faction_no", ":troop_no"),
(str_store_faction_name_link, s11, ":faction_no"),
],
"{s10} of {s11}.", "dplmc_constable_exchange_prisoner_ask_confirm",
[
(store_repeat_object, "$diplomacy_var"),
(store_faction_of_troop, "$g_faction_selected", "$diplomacy_var"),
]],
[anyone|plyr,"dplmc_constable_talk_prisoner_select", [],
"No one.", "dplmc_constable_pretalk",
[
]],
[anyone,"dplmc_constable_exchange_prisoner_ask_confirm",
[
(str_store_troop_name, s10, "$diplomacy_var"),
(store_faction_of_troop, ":faction_no", "$diplomacy_var"),
(str_store_faction_name_link, s11, ":faction_no"),
],
"As you wish, I will tell the prison guard to release {s10} of {s11}.", "dplmc_constable_exchange_prisoner_confirm",[
]],
[anyone|plyr,"dplmc_constable_exchange_prisoner_confirm", [],
"Very well.", "dplmc_constable_pretalk",
[
(troop_get_slot, ":party", "$diplomacy_var", slot_troop_prisoner_of_party),

(try_begin),
  (eq, "$cheat_mode", 1),
  (str_store_party_name, s7, ":party"), #debug
  (display_message, "@{!}DEBUG - prisoner of: {s7}"),
(try_end),

(party_remove_prisoners, ":party", "$diplomacy_var", 1),
(try_begin),
  (main_party_has_troop, "$diplomacy_var"),
  (party_remove_prisoners, "p_main_party", "$diplomacy_var", 1),
(try_end),
(call_script, "script_remove_troop_from_prison", "$diplomacy_var"),
(str_store_troop_name, s7, "$diplomacy_var"),
(display_message, "str_dplmc_has_been_set_free"),
(call_script, "script_change_player_relation_with_troop", "$diplomacy_var", 3),
(call_script, "script_change_player_honor", 1),
]],
[anyone|plyr,"dplmc_constable_exchange_prisoner_confirm", [],
"No, I changed my mind.", "dplmc_constable_pretalk",[]],
[anyone|plyr, "dplmc_constable_talk",
[],
"Please give me a report.", "dplmc_constable_reports_ask",
[]],
[anyone, "dplmc_constable_reports_ask",
[],
"About what do you want to have a report?", "dplmc_constable_reports",
[]],
[anyone|plyr, "dplmc_constable_reports",
[
##diplomacy start+ Handle player is co-ruler of kingdom
(assign, ":is_coruler", 0),
(try_begin),
	(is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
	(call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", "$players_kingdom"),
	(ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
	(assign, ":is_coruler", 1),
(try_end),
(this_or_next|eq, ":is_coruler", 1),
##diplomacy end+
 (eq, "$players_kingdom", "fac_player_supporters_faction"),
],
"Please give me a report about the clan's army.", "dplmc_constable_kingdom_overview",
[]],
[anyone, "dplmc_constable_kingdom_overview",
[
(assign, ":garrison_size", 0),
(assign, ":field_size", 0),
(assign, ":castle_count", 0),
(assign, ":town_count", 0),
##diplomacy start+ Handle player is co-ruler of kingdom
(assign, ":alt_faction", "fac_player_supporters_faction"),
(try_begin),
	(is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
	(call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", "$players_kingdom"),
	(ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
	(assign, ":alt_faction", "$players_kingdom"),
(try_end),
##diplomacy end+

(try_for_parties, ":selected_party"),
(try_begin),
  (this_or_next|party_slot_eq, ":selected_party", slot_party_type, spt_town),
  (party_slot_eq, ":selected_party", slot_party_type, spt_castle),
  (store_faction_of_party, ":party_faction", ":selected_party"),
  ##diplomacy start+
  (this_or_next|eq, ":party_faction", ":alt_faction"),
  ##diplomacy end+
  (eq, ":party_faction", "fac_player_supporters_faction"),

  (party_get_num_companion_stacks, ":num_stacks", ":selected_party"),
  (try_for_range, ":i_stack", 0, ":num_stacks"),
    (party_stack_get_size, ":stack_size", ":selected_party", ":i_stack"),
    (val_add, ":garrison_size", ":stack_size"),
  (try_end),

  (try_begin),
    (party_slot_eq, ":selected_party", slot_party_type, spt_castle),
    (val_add, ":castle_count", 1),
  (else_try),
    (val_add, ":town_count", 1),
  (try_end),
(else_try),
  (party_slot_eq, ":selected_party", slot_party_type, spt_kingdom_hero_party),
  (store_faction_of_party, ":party_faction", ":selected_party"),
  ##diplomacy start+
  (this_or_next|eq, ":party_faction", ":alt_faction"),
  ##diplomacy end+
  (eq, ":party_faction", "fac_player_supporters_faction"),
  (party_get_num_companion_stacks, ":num_stacks", ":selected_party"),
  (try_for_range, ":i_stack", 0, ":num_stacks"),
    (party_stack_get_size, ":stack_size", ":selected_party", ":i_stack"),
    (val_add, ":field_size", ":stack_size"),
  (try_end),
(else_try),
  (eq, ":selected_party", "p_main_party"),
  (party_get_num_companion_stacks, ":num_stacks", ":selected_party"),
  (try_for_range, ":i_stack", 0, ":num_stacks"),
    (party_stack_get_size, ":stack_size", ":selected_party", ":i_stack"),
    (val_add, ":field_size", ":stack_size"),
  (try_end),
(try_end),

(try_end),
(assign, reg2, ":garrison_size"),
(str_store_string, s6, "@Our domain currently has {reg2} soldiers"),
(assign, reg2, ":town_count"),
(str_store_string, s6, "@{s6} garrisoned in {reg2} towns"),
(assign, reg2, ":castle_count"),
(str_store_string, s6, "@{s6} and {reg2} castles."),
(try_begin),
(gt, ":field_size", 0),
(assign, reg2, ":field_size"),
(str_store_string, s6, "@{s6} In addition we have {reg2} soldiers in the field."),
(try_end),

],
"{!}{s6}", "dplmc_constable_reports_ask",
[]],
[anyone|plyr, "dplmc_constable_reports",
[
],
"Please give me a report about my army.", "dplmc_constable_overview",
[]],
[anyone, "dplmc_constable_overview",
[

(assign, ":garrison_size", 0),
(assign, ":field_size", 0),
(assign, ":patrol_size", 0),
(assign, ":castle_count", 0),
(assign, ":town_count", 0),
(try_for_parties, ":selected_party"),

(try_begin),
  (this_or_next|party_slot_eq, ":selected_party", slot_party_type, spt_town),
  (party_slot_eq, ":selected_party", slot_party_type, spt_castle),
  (party_slot_eq, ":selected_party", slot_town_lord, "trp_player"),

  (party_get_num_companion_stacks, ":num_stacks", ":selected_party"),
  (try_for_range, ":i_stack", 0, ":num_stacks"),
    (party_stack_get_size, ":stack_size", ":selected_party", ":i_stack"),
    (val_add, ":garrison_size", ":stack_size"),
  (try_end),

  (try_begin),
    (party_slot_eq, ":selected_party", slot_party_type, spt_castle),
    (val_add, ":castle_count", 1),
  (else_try),
    (val_add, ":town_count", 1),
  (try_end),
(else_try),
  (eq, ":selected_party", "p_main_party"),
  (party_get_num_companion_stacks, ":num_stacks", ":selected_party"),
  (try_for_range, ":i_stack", 0, ":num_stacks"),
    (party_stack_get_size, ":stack_size", ":selected_party", ":i_stack"),
    (val_add, ":field_size", ":stack_size"),
  (try_end),
(else_try),
  (party_slot_eq, ":selected_party", slot_party_type, spt_patrol),
  (party_slot_eq, ":selected_party", dplmc_slot_party_mission_diplomacy, "trp_player"),
  (party_get_num_companion_stacks, ":num_stacks", ":selected_party"),
  (try_for_range, ":i_stack", 0, ":num_stacks"),
    (party_stack_get_size, ":stack_size", ":selected_party", ":i_stack"),
    (val_add, ":patrol_size", ":stack_size"),
  (try_end),
(try_end),

(try_end),
(assign, reg2, ":garrison_size"),
(str_store_string, s6, "@We currently have {reg2} soldiers"),
(assign, reg2, ":town_count"),
(str_store_string, s6, "@{s6} garrisoned in {reg2} towns"),
(assign, reg2, ":castle_count"),
(str_store_string, s6, "@{s6} and {reg2} castles."),
(try_begin),
(gt, ":field_size", 0),
(assign, reg2, ":field_size"),
(assign, reg3, ":patrol_size"),
(str_store_string, s6, "@{s6} In addition you have {reg2} soldiers in your army and {reg3} soldiers in patrols."),
(try_end),

],
"{!}{s6}", "dplmc_constable_reports_ask",
[]],
[anyone|plyr, "dplmc_constable_reports",
[
],
"Please give me a status report about the army of a lord.", "dplmc_constable_lord",
[]],
[anyone, "dplmc_constable_lord",
[],
"About which lord do you like to be informed?", "dplmc_constable_status_lord_select",
[]],
[anyone|plyr|repeat_for_troops, "dplmc_constable_status_lord_select",
[
(store_repeat_object, ":troop_no"),
(troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
(neq, "trp_player", ":troop_no"),
(troop_slot_ge, ":troop_no", slot_troop_leaded_party, 0),
(neg|troop_slot_ge, ":troop_no", slot_troop_prisoner_of_party, 0),
(store_troop_faction, ":faction_no", ":troop_no"),
##diplomacy start+ Handle player is co-ruler of faction
##OLD:
#(eq, ":faction_no", "fac_player_supporters_faction"),
##NEW:
(call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", ":faction_no"),
(ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
##diplomacy end+
(str_store_troop_name, s11, ":troop_no"),
],
"{!}{s11}.", "dplmc_constable_status_lord_info",
[
(store_repeat_object, "$diplomacy_var"),
]],
[anyone|plyr, "dplmc_constable_status_lord_select",
[],
"Never mind.", "dplmc_constable_reports_ask",
[]],
[anyone, "dplmc_constable_status_lord_info",
[
(assign, ":selected_troop", "$diplomacy_var"),
(str_store_troop_name, s60, ":selected_troop"),


(call_script, "script_update_troop_location_notes", ":selected_troop", 1),
(call_script, "script_get_information_about_troops_position", ":selected_troop", 0),

(assign, ":party_size", 0),
(troop_get_slot, ":selected_party", ":selected_troop", slot_troop_leaded_party),
(str_store_string, s52, "str_empty_string"),
(party_get_num_companion_stacks, ":num_stacks", ":selected_party"),

(le, ":num_stacks", 20),

(try_for_range, ":i_stack", 1, ":num_stacks"),
(party_stack_get_troop_id, ":stack_troop", ":selected_party", ":i_stack"),
(party_stack_get_size, ":stack_size", ":selected_party", ":i_stack"),
(val_add, ":party_size", ":stack_size"),
(assign, reg2, ":stack_size"),
(str_store_troop_name, s53, ":stack_troop"),
(str_store_string, s52, "@{!}{s52} {reg2} {s53}."),
(try_end),

(assign, reg2, ":party_size"),
(str_store_string, s51, "@He fields {reg2} soldiers."),
],
"{!}{s1} {s51} {s52}", "dplmc_constable_lord",
[]],
[anyone, "dplmc_constable_status_lord_info",
[
(assign, ":selected_troop", "$diplomacy_var"),
(str_store_troop_name, s60, ":selected_troop"),


(call_script, "script_update_troop_location_notes", ":selected_troop", 1),
(call_script, "script_get_information_about_troops_position", ":selected_troop", 0),

(assign, ":party_size", 0),
(troop_get_slot, ":selected_party", ":selected_troop", slot_troop_leaded_party),
(str_store_string, s52, "str_empty_string"),
(party_get_num_companion_stacks, ":num_stacks", ":selected_party"),

(try_for_range, ":i_stack", 1, ":num_stacks"),
(party_stack_get_troop_id, ":stack_troop", ":selected_party", ":i_stack"),
(party_stack_get_size, ":stack_size", ":selected_party", ":i_stack"),
(val_add, ":party_size", ":stack_size"),
(try_begin),
  (le, ":i_stack", 20),
  (assign, reg2, ":stack_size"),
  (str_store_troop_name, s53, ":stack_troop"),
  (str_store_string, s52, "@{!}{s52} {reg2} {s53}."),
(try_end),
(try_end),

(assign, reg2, ":party_size"),
(str_store_string, s51, "@He fields {reg2} soldiers."),
],
"{!}{s1} {s51} {s52}", "dplmc_constable_status_lord_info_6",
[]],
[anyone, "dplmc_constable_status_lord_info_6",
[
(assign, ":selected_troop", "$diplomacy_var"),
(str_store_troop_name, s60, ":selected_troop"),

(assign, ":party_size", 0),
(troop_get_slot, ":selected_party", ":selected_troop", slot_troop_leaded_party),
(str_store_string, s52, "str_empty_string"),
(party_get_num_companion_stacks, ":num_stacks", ":selected_party"),

(try_for_range, ":i_stack", 20, ":num_stacks"),
(party_stack_get_troop_id, ":stack_troop", ":selected_party", ":i_stack"),
(party_stack_get_size, ":stack_size", ":selected_party", ":i_stack"),
(val_add, ":party_size", ":stack_size"),
(assign, reg2, ":stack_size"),
(str_store_troop_name, s53, ":stack_troop"),
(str_store_string, s52, "@{!}{s52} {reg2} {s53}."),
(try_end),

(assign, reg2, ":party_size"),
],
"{!}{s52}", "dplmc_constable_lord",
[]],
[anyone|plyr, "dplmc_constable_reports",
[
],
"Please give me a status report about the garrison of a fief.", "dplmc_constable_status",
[]],
[anyone, "dplmc_constable_status",
[],
"About which fief do you like to be informed?", "dplmc_constable_status_select_fief",
[]],
[anyone|plyr|repeat_for_parties, "dplmc_constable_status_select_fief",
[
(store_repeat_object, ":party_no"),
(is_between, ":party_no", walled_centers_begin, walled_centers_end),
(store_faction_of_party, ":party_faction", ":party_no"),
(this_or_next|party_slot_eq, ":party_no", slot_town_lord, "trp_player"),
##diplomacy start+ Handle player is co-ruler of faction
##OLD:
#(eq, ":party_faction", "fac_player_supporters_faction"),
##NEW:
(call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", ":party_faction"),
(ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
##diplomacy end+
(str_store_party_name, s60, ":party_no"),
],
"{!}{s60}.", "dplmc_constable_status_info",
[
(store_repeat_object, "$diplomacy_var"),
]],
[anyone, "dplmc_constable_status_info",
[
(assign, ":selected_party", "$diplomacy_var"),
(str_store_party_name, s60, ":selected_party"),

(assign, ":garrison_size", 0),

(str_store_string, s52, "str_empty_string"),
(party_get_num_companion_stacks, ":num_stacks", ":selected_party"),

(le, ":num_stacks", 20),

(try_for_range, ":i_stack", 0, ":num_stacks"),
(party_stack_get_troop_id, ":stack_troop", ":selected_party", ":i_stack"),
(party_stack_get_size, ":stack_size", ":selected_party", ":i_stack"),
(val_add, ":garrison_size", ":stack_size"),
(assign, reg2, ":stack_size"),
(str_store_troop_name, s53, ":stack_troop"),
(str_store_string, s52, "@{!}{s52} {reg2} {s53}."),
(try_end),

(assign, reg2, ":garrison_size"),
(str_store_string, s51, "@We currently have {reg2} soldiers garrisoned in {s60}."),
],
"{!}{s51} {s52}", "dplmc_constable_status",
[]],
[anyone, "dplmc_constable_status_info",
[
(assign, ":selected_party", "$diplomacy_var"),
(str_store_party_name, s60, ":selected_party"),

(assign, ":garrison_size", 0),

(str_store_string, s52, "str_empty_string"),
(party_get_num_companion_stacks, ":num_stacks", ":selected_party"),

(try_for_range, ":i_stack", 0, ":num_stacks"),
(party_stack_get_troop_id, ":stack_troop", ":selected_party", ":i_stack"),
(party_stack_get_size, ":stack_size", ":selected_party", ":i_stack"),
(val_add, ":garrison_size", ":stack_size"),
(try_begin),
  (le, ":i_stack", 20),
  (assign, reg2, ":stack_size"),
  (str_store_troop_name, s53, ":stack_troop"),
  (str_store_string, s52, "@{!}{s52} {reg2} {s53}."),
(try_end),
(try_end),

(assign, reg2, ":garrison_size"),
(str_store_string, s51, "@We currently have {reg2} soldiers garrisoned in {s60}."),
],
"{!}{s51} {s52}", "dplmc_constable_status_info_6",
[]],
[anyone, "dplmc_constable_status_info_6",
[
(assign, ":selected_party", "$diplomacy_var"),
(str_store_party_name, s60, ":selected_party"),

(str_store_string, s52, "str_empty_string"),
(party_get_num_companion_stacks, ":num_stacks", ":selected_party"),

(try_for_range, ":i_stack", 20, ":num_stacks"),
(party_stack_get_troop_id, ":stack_troop", ":selected_party", ":i_stack"),
(party_stack_get_size, ":stack_size", ":selected_party", ":i_stack"),
(assign, reg2, ":stack_size"),
(str_store_troop_name, s53, ":stack_troop"),
(str_store_string, s52, "@{!}{s52} {reg2} {s53}."),
(try_end),

],
"{!}{s52}", "dplmc_constable_status",
[]],
[anyone|plyr, "dplmc_constable_status_select_fief",
[],
"Never mind.", "dplmc_constable_reports_ask",
[]],
[anyone|plyr, "dplmc_constable_reports",
[
],
"Thank you, that's all for now.", "dplmc_constable_pretalk",
[]],
[anyone|plyr, "dplmc_constable_talk",
[],
"I would like to take a look at the armory.", "dplmc_constable_pretalk",
[(change_screen_loot, "trp_dplmc_constable"),]],
[anyone|plyr, "dplmc_constable_talk",
[],
"Let's talk about recruits and training.", "dplmc_constable_recruits_and_training_ask",
[]],
[anyone, "dplmc_constable_recruits_and_training_ask",
[],
"Of course.", "dplmc_constable_recruits_and_training",
[]],
[anyone|plyr, "dplmc_constable_recruits_and_training",
[
(neg|is_between, "$g_constable_training_center", walled_centers_begin, walled_centers_end),
],
"Can you train some recruits, please?", "dplmc_constable_train_ask",
[]
],
[anyone, "dplmc_constable_train_ask",
[],
"Of course, where should I train them?", "dplmc_constable_train_select",
[]
],
[anyone|plyr|repeat_for_parties, "dplmc_constable_train_select",
[
(store_repeat_object, ":party_no"),
(this_or_next|party_slot_eq, ":party_no", slot_party_type, spt_town),
(party_slot_eq, ":party_no", slot_party_type, spt_castle),
(party_slot_eq, ":party_no", slot_town_lord, "trp_player"),
(str_store_party_name, s11, ":party_no"),
],
"{!}{s11}.", "dplmc_constable_train_type_ask",
[
(store_repeat_object, "$diplomacy_var"),
]
],
[anyone, "dplmc_constable_train_type_ask",
[
(str_store_party_name, s11, "$diplomacy_var"),
],
"Do you prefer melee or ranged units?", "dplmc_constable_train_type",
[]
],
[anyone|plyr, "dplmc_constable_train_type",
[],
"Melee.", "dplmc_constable_train_improved_ask",
[(assign, "$g_constable_training_type", 0),]
],
[anyone|plyr, "dplmc_constable_train_type",
[],
"Ranged.", "dplmc_constable_train_improved_ask",
[(assign, "$g_constable_training_type", 1),]
],
[anyone|plyr, "dplmc_constable_train_type",
[],
"Neither.", "dplmc_constable_pretalk",
[]
],
[anyone, "dplmc_constable_train_improved_ask",
[],
"If you want I can hire additional trainers so we can train the recruits faster and better. This will cost 10 mon extra per day.", "dplmc_constable_train_improved",
[]
],
[anyone|plyr, "dplmc_constable_train_improved",
[],
"Yes, please hire additional trainers.", "dplmc_constable_train_center",
[(assign, "$g_constable_training_improved", 1),]
],
[anyone|plyr, "dplmc_constable_train_improved",
[],
"No, you have to train them alone.", "dplmc_constable_train_center",
[(assign, "$g_constable_training_improved", 0),]
],
[anyone, "dplmc_constable_train_center",
[
(str_store_party_name, s11, "$diplomacy_var"),
(try_begin),
(eq, "$g_constable_training_type", 0),
(str_store_string, s12, "@You are preferring melee units."),
(else_try),
(str_store_string, s12, "@You are preferring ranged units."),
(try_end),

(str_clear, s13),
(try_begin),
(eq, "$g_constable_training_improved", 1),
(str_store_string, s13, "@ and the additional trainers"),
(try_end),
],
"Alright, I will train the recruits in {s11}. {s12} Please, make sure we have enough money in the treasury to pay the equipment{s13}.", "dplmc_constable_pretalk",
[(assign, "$g_constable_training_center", "$diplomacy_var"),]
],
[anyone|plyr, "dplmc_constable_train_select",
[],
"I changed my mind, maybe you shouldn't train them.", "dplmc_constable_pretalk",
[]
],
[anyone|plyr, "dplmc_constable_recruits_and_training",
[
(is_between, "$g_constable_training_center", walled_centers_begin, walled_centers_end),
(str_store_party_name, s11, "$g_constable_training_center"),

],
"Please stop training the recruits in {s11}.", "dplmc_constable_train_stop",
[]
],
[anyone, "dplmc_constable_train_stop",
[
(is_between, "$g_constable_training_center", walled_centers_begin, walled_centers_end),

],
"As you wish.", "dplmc_constable_pretalk",
[(assign, "$g_constable_training_center", -1),]
],
[anyone|plyr, "dplmc_constable_recruits_and_training",
[
],
"I want to recruit new soldiers.", "dplmc_constable_recruit",
[]],
[anyone, "dplmc_constable_recruit",
[
(le, "$g_player_chamberlain", 0),
],
"We need a treasury to recruit new soldiers. You have to appoint a treasurer first.", "dplmc_constable_pretalk",
[]],
[anyone, "dplmc_constable_recruit",
[
(gt, "$g_player_chamberlain", 0),
(assign, ":recruiter_amount", 0),

(try_begin),
  (party_slot_eq, "$current_town", slot_party_type, spt_town),
  (assign, ":max_recruiters", 4),
  (assign, reg0, 1),
(else_try),
  (assign, ":max_recruiters", 2),
  (assign, reg0, 0),
(try_end),

(try_for_parties, ":party_no"),
  (party_slot_eq,":party_no", slot_party_type, dplmc_spt_recruiter),
  (party_slot_eq, ":party_no", dplmc_slot_party_recruiter_origin, "$current_town"),
  (val_add, ":recruiter_amount", 1),
(try_end),

(ge, ":recruiter_amount", ":max_recruiters"),
],
"You have already hired the maximum amount of {reg0?4:2} recruiters from this {reg0?town:castle}.", "dplmc_constable_pretalk",
[]],
[anyone, "dplmc_constable_recruit",
[
(gt, "$g_player_chamberlain", 0),
(assign, ":recruiter_amount", 0),

(try_begin),
  (party_slot_eq, "$current_town", slot_party_type, spt_town),
  (assign, ":max_recruiters", 4),
(else_try),
  (assign, ":max_recruiters", 2),
(try_end),

(try_for_parties, ":party_no"),
  (party_slot_eq,":party_no", slot_party_type, dplmc_spt_recruiter),
  (party_slot_eq, ":party_no", dplmc_slot_party_recruiter_origin, "$current_town"),
  (val_add, ":recruiter_amount", 1),
(try_end),

(lt, ":recruiter_amount", ":max_recruiters"),
],
"If you want, I will send someone to visit villages and recruit population to your forces. \
After he has collected the amount you ordered he returns to this {reg0?town:castle} and puts the recruits in the garrison. \
There's a limit for concurrent recruiters, which is 2 for castles and 4 for towns. \
You also need to make sure there's enough money in the treasurer's treasury. \
What kind of recruits do you want?", "dplmc_constable_recruit_select",
[]],
[anyone|plyr|repeat_for_factions, "dplmc_constable_recruit_select",
[
(store_repeat_object, ":faction_no"),
(is_between, ":faction_no", npc_kingdoms_begin, npc_kingdoms_end),
(store_sub, ":offset", ":faction_no", "fac_kingdom_1"),
(val_add, ":offset", "str_kingdom_1_adjective"),
(str_store_string, s11, ":offset"),
],
"{s11}.", "dplmc_constable_recruit_amount",
[
(store_repeat_object, ":faction_no"),
(assign, "$temp", ":faction_no"),
]],
[anyone, "dplmc_constable_recruit_amount",
[
],
"You have to pay 20 mon for each recruit and 10 mon for the recruiter. I will take the money from the treasury. How many recruits are you willing to pay for?", "dplmc_constable_recruit_amount_select",
[]],
[anyone|plyr,"dplmc_constable_recruit_amount_select",
[(store_troop_gold,":gold","trp_household_possessions"), (ge,":gold",110),],
"5.", "dplmc_constable_recruit_confirm_ask",[

(assign, "$diplomacy_var", 5),
]],
[anyone|plyr,"dplmc_constable_recruit_amount_select",
[(store_troop_gold,":gold","trp_household_possessions"), (ge,":gold",210),],
"10.", "dplmc_constable_recruit_confirm_ask",[
(assign, "$diplomacy_var", 10),
]],
[anyone|plyr,"dplmc_constable_recruit_amount_select",
[(store_troop_gold,":gold","trp_household_possessions"), (ge,":gold",410),],
"20.", "dplmc_constable_recruit_confirm_ask",[
(assign, "$diplomacy_var", 20),
]],
[anyone|plyr,"dplmc_constable_recruit_amount_select",
[(store_troop_gold,":gold","trp_household_possessions"), (ge,":gold",610),],
"30.", "dplmc_constable_recruit_confirm_ask",[
(assign, "$diplomacy_var", 30),
]],
[anyone|plyr,"dplmc_constable_recruit_amount_select",
[(store_troop_gold,":gold","trp_household_possessions"), (ge,":gold",810),],
"40.", "dplmc_constable_recruit_confirm_ask",[
(assign, "$diplomacy_var", 40),
]],
[anyone|plyr,"dplmc_constable_recruit_amount_select",
[(store_troop_gold,":gold","trp_household_possessions"), (ge,":gold",1110),],
"50.", "dplmc_constable_recruit_confirm_ask",[
(assign, "$diplomacy_var", 50),
]],
[anyone|plyr,"dplmc_constable_recruit_confirm_ask",
[
(assign, reg2, "$diplomacy_var"),
(str_store_string, s6, "@{!}{reg2}"),
(store_sub, ":offset", "$temp", "fac_kingdom_1"),
(val_add, ":offset", "str_kingdom_1_adjective"),
(str_store_string, s11, ":offset"),
],
"Do you really want to recruit {s6} {s11} peasants?", "dplmc_constable_recruit_confirm",[
]],
[anyone|plyr,"dplmc_constable_recruit_confirm",
[],
"Yes.", "dplmc_constable_pretalk",[
(call_script, "script_dplmc_send_recruiter", "$diplomacy_var", "$temp"),
]],
[anyone|plyr,"dplmc_constable_recruit_confirm",
[],
"No.", "dplmc_constable_pretalk",[
]],
[anyone|plyr,"dplmc_constable_recruit_amount_select",
[],
"None.", "dplmc_constable_pretalk",[
]],
[anyone|plyr, "dplmc_constable_recruits_and_training",
[
],
"I changed my mind.", "dplmc_constable_pretalk",
[]
],
[anyone|plyr, "dplmc_constable_talk",
[
],
"Let's talk about patrols and troop movement.", "dplmc_constable_security_ask",
[]],
[anyone, "dplmc_constable_security_ask",
[
],
"Of course.", "dplmc_constable_security",
[]],
[anyone|plyr, "dplmc_constable_security",
[],
"I want to move troops to another location.", "dplmc_constable_move_troops",
[
(party_clear, "p_temp_party"),
(assign, "$g_move_heroes", 1),
(call_script, "script_party_add_party", "p_temp_party", "p_main_party"),
(party_clear, "p_main_party"),
(party_remove_members, "p_main_party", "trp_player", 1),

(change_screen_exchange_members, 1),
]],
[anyone, "dplmc_constable_move_troops",
[
],
"Where do you want to move the troops?", "dplmc_constable_move_troops_location",
[]],
[anyone|plyr|repeat_for_parties, "dplmc_constable_move_troops_location",
[
(store_repeat_object, ":party_no"),
(is_between, ":party_no", towns_begin, castles_end),
(neq, ":party_no", "$current_town"),
(store_faction_of_party, ":party_faction", ":party_no"),
(eq, ":party_faction", "$players_kingdom"),
(str_store_party_name, s11, ":party_no"),
],
"{!}{s11}.", "dplmc_constable_move_troops_location_confirm_ask",
[
(store_repeat_object, "$diplomacy_var"),
(party_clear, "p_temp_party_2"),
(try_begin),
(store_party_size, ":party_size", "p_main_party"),
(gt, ":party_size", 0),
(call_script, "script_party_add_party","p_temp_party_2", "p_main_party"),
(party_clear, "p_main_party"),
(party_stack_get_troop_id, ":troop_id", "p_main_party", 0),

(try_begin),
  (ge, ":troop_id", 0),
  (party_stack_get_size, ":troop_size", "p_main_party", 0),
  (party_remove_members, "p_main_party",":troop_id",":troop_size"),
(try_end),
(party_stack_get_troop_id, ":troop_id", "p_main_party", 1),
(try_begin),
  (ge, ":troop_id", 0),
  (party_stack_get_size, ":troop_size", "p_main_party", 1),
  (party_remove_members, "p_main_party",":troop_id",":troop_size"),
(try_end),
(try_end),

(call_script, "script_party_add_party", "p_main_party", "p_temp_party"),
(assign, "$g_move_heroes", 0),
]],
[anyone|plyr, "dplmc_constable_move_troops_location",
[],
"Nowhere.", "dplmc_constable_pretalk",
[
(party_clear, "p_temp_party_2"),
(try_begin),
(store_party_size, ":party_size", "p_main_party"),
(gt, ":party_size", 0),
(call_script, "script_party_add_party","p_temp_party_2", "p_main_party"),
(party_clear, "p_main_party"),
(party_stack_get_troop_id, ":troop_id", "p_main_party", 0),

(try_begin),
  (ge, ":troop_id", 0),
  (party_stack_get_size, ":troop_size", "p_main_party", 0),
  (party_remove_members, "p_main_party",":troop_id",":troop_size"),
(try_end),
(party_stack_get_troop_id, ":troop_id", "p_main_party", 1),
(try_begin),
  (ge, ":troop_id", 0),
  (party_stack_get_size, ":troop_size", "p_main_party", 1),
  (party_remove_members, "p_main_party",":troop_id",":troop_size"),
(try_end),
(try_end),

(call_script, "script_party_add_party", "p_main_party", "p_temp_party"),
(assign, "$g_move_heroes", 0),

#reset town party
(call_script, "script_party_add_party", "$current_town", "p_temp_party_2"),
(party_clear, "p_temp_party_2"),
]],
[anyone, "dplmc_constable_move_troops_location_confirm_ask",
[
(store_party_size, ":party_size", "p_temp_party_2"),

  (assign, ":prisoner_size", 0),
  (party_get_num_prisoner_stacks, ":num_prisoner_stacks","p_temp_party_2"),
  (try_for_range_backwards, ":stack_no", 0, ":num_prisoner_stacks"),
    (party_prisoner_stack_get_size, ":stack_size","p_temp_party_2",":stack_no"),
    (val_add, ":prisoner_size", ":stack_size"),
  (try_end),

  (le, ":party_size", ":prisoner_size"),

],
"You didn't choose any soldiers. Seems like you changed your mind.", "dplmc_constable_pretalk",
[]],
[anyone, "dplmc_constable_move_troops_location_confirm_ask",
[
(str_store_party_name, s9, "$diplomacy_var"),
(store_party_size, ":party_size", "p_temp_party_2"),
(store_mul, reg5, ":party_size", 5),
],
"Do you really want to send the troops to {s9}? This will cost us {reg5} mon.", "dplmc_constable_move_troops_location_confirm",
[]],
[anyone|plyr, "dplmc_constable_move_troops_location_confirm",
[
(store_troop_gold, ":player_wealth", "trp_household_possessions"),
(ge, ":player_wealth", reg5),
],
"Yes.", "dplmc_constable_pretalk",
[
(call_script, "script_dplmc_withdraw_from_treasury", reg5),
(call_script, "script_dplmc_move_troops_party", "$current_town", "$diplomacy_var", "p_temp_party_2", "fac_player_faction"),
(party_clear, "p_temp_party_2"),
]
],
[anyone|plyr, "dplmc_constable_move_troops_location_confirm",
[],
"No. Let me check if we can afford that.", "dplmc_constable_pretalk",
[
(call_script, "script_party_add_party", "$current_town", "p_temp_party_2"),
(party_clear, "p_temp_party_2"),
]],
[anyone|plyr, "dplmc_constable_security",
[],
"I want to enlist a patrol.", "dplmc_constable_patrol_size_ask",
[]],
[anyone, "dplmc_constable_patrol_size_ask",
[
(store_current_hours, ":current_hours"),
(val_sub, ":current_hours", 24 * 7),
(faction_get_slot, ":policy_time", "fac_player_faction", dplmc_slot_faction_patrol_time),
(ge, ":current_hours", ":policy_time"),
],
"You can take troops from your garrison or enlist fresh troops. In the latter case you can enlist a small patrol for 1000 mon, a medium patrol for 2000 mon or a big patrol for 3000 mon. You can also enlist a small elite patrol for 2000 mon. We have to pay weekly wages for the soldiers so make sure you have enough money in the treasury.", "dplmc_constable_patrol_size",
[]],
[anyone, "dplmc_constable_patrol_size_ask",
[

(store_current_hours, ":current_hours"),
(val_sub, ":current_hours", 24 * 7),
(faction_get_slot, ":policy_time", "fac_player_faction", dplmc_slot_faction_patrol_time),
(store_sub, ":wait_hours" , ":policy_time", ":current_hours"),
(store_div, ":wait_days", ":wait_hours", 24),
(store_mod, ":wait_mod", ":wait_hours", 24),
(try_begin),
(lt, ":wait_mod", 0),
(val_add, ":wait_days", 1),
(try_end),
(assign, reg0, ":wait_days"),

],
"Currently there are no fresh troops available. We have to wait {reg0} days. But you can take troops from your garrison.", "dplmc_constable_patrol_size",
[]],
[anyone|plyr, "dplmc_constable_patrol_size",
[],
"Take troops out of the garrison.", "dplmc_constable_patrol_garrison",
[
(store_party_size_wo_prisoners, ":garrison_size", "$current_town"),			#zerilius changes
(gt, ":garrison_size", 0),								#zerilius changes
(party_clear, "p_temp_party"),
(assign, "$g_move_heroes", 1),
(call_script, "script_party_add_party", "p_temp_party", "p_main_party"),
(party_clear, "p_main_party"),
(party_remove_members, "p_main_party", "trp_player", 1),

(change_screen_exchange_members, 1),
]],
[anyone, "dplmc_constable_patrol_garrison",
[
 (store_party_size_wo_prisoners, ":garrison_size", "$current_town"),
 (le, ":garrison_size", 0),
],
"We do not have any troops in the garrison.", "dplmc_constable_patrol_size",
[]],
[anyone, "dplmc_constable_patrol_garrison",
[],
"My {lord/lady}, lets muster the patrol troops.", "dplmc_constable_patrol_garrison_2",
[]],
[anyone, "dplmc_constable_patrol_garrison_2",
[
 (store_party_size_wo_prisoners, ":garrison_size", "p_main_party"),
 (le, ":garrison_size", 0),
 (party_add_members, "p_main_party", "trp_gekokujo_uesugi_jizamurai", 1),				#zerilius included otherwise gives errors
],
"You didn't choose any soldiers. Seems like you changed your mind.", "dplmc_constable_pretalk",
[
(party_remove_members, "p_main_party", "trp_gekokujo_uesugi_jizamurai", 1),
(call_script, "script_party_add_party", "p_main_party", "p_temp_party"),
(assign, "$g_move_heroes", 0),
]],
[anyone, "dplmc_constable_patrol_garrison_2",
[
],
"Where do you want to send the patrol?", "dplmc_constable_patrol_garrison_location",
[]],
[anyone|plyr|repeat_for_parties, "dplmc_constable_patrol_garrison_location",
[
(store_repeat_object, ":party_no"),
(is_between, ":party_no", centers_begin, centers_end),
(store_faction_of_party, ":party_faction", ":party_no"),
(eq, ":party_faction", "$players_kingdom"),
(str_store_party_name, s11, ":party_no"),
],
"{!}{s11}.", "dplmc_constable_patrol_garrison_confirm_ask",
[
(store_repeat_object, "$diplomacy_var"),
(party_clear, "p_temp_party_2"),
(call_script, "script_party_add_party","p_temp_party_2", "p_main_party"),
(party_clear, "p_main_party"),
(party_stack_get_troop_id, ":troop_id", "p_main_party", 0),
(try_begin),
(ge, ":troop_id", 0),
(party_stack_get_size, ":troop_size", "p_main_party", 0),
(party_remove_members, "p_main_party",":troop_id",":troop_size"),
(try_end),
(party_stack_get_troop_id, ":troop_id", "p_main_party", 1),
(try_begin),
(ge, ":troop_id", 0),
(party_stack_get_size, ":troop_size", "p_main_party", 1),
(party_remove_members, "p_main_party",":troop_id",":troop_size"),
(try_end),

(call_script, "script_party_add_party", "p_main_party", "p_temp_party"),
(assign, "$g_move_heroes", 0),
]],
[anyone, "dplmc_constable_patrol_garrison_confirm_ask",
[
(store_party_size, ":party_size", "p_temp_party_2"),

  (assign, ":prisoner_size", 0),
  (party_get_num_prisoner_stacks, ":num_prisoner_stacks","p_temp_party_2"),
  (try_for_range_backwards, ":stack_no", 0, ":num_prisoner_stacks"),
    (party_prisoner_stack_get_size, ":stack_size","p_temp_party_2",":stack_no"),
    (val_add, ":prisoner_size", ":stack_size"),
  (try_end),

  (le, ":party_size", ":prisoner_size"),

],
"You didn't choose any soldiers. Seems like you changed your mind.", "dplmc_constable_pretalk",
[]],
[anyone, "dplmc_constable_patrol_garrison_confirm_ask",
[
(str_store_party_name, s9, "$diplomacy_var"),
],
"Do you really want to send the patrol to {s9}?", "dplmc_constable_patrol_garrison_confirm",
[]],
[anyone|plyr, "dplmc_constable_patrol_garrison_confirm",
[],
"Yes.", "dplmc_constable_pretalk",
[
(call_script, "script_dplmc_send_patrol_party", "$current_town", "$diplomacy_var", "p_temp_party_2", "$players_kingdom", "trp_player"),
(party_clear, "p_temp_party_2"),
]
],
[anyone|plyr, "dplmc_constable_patrol_garrison_confirm",
[],
"No.", "dplmc_constable_pretalk",
[
(call_script, "script_party_add_party", "$current_town", "p_temp_party_2"),
(party_clear, "p_temp_party_2"),
]],
[anyone|plyr, "dplmc_constable_patrol_size",
[
(store_current_hours, ":current_hours"),
(val_sub, ":current_hours", 24 * 7),
(faction_get_slot, ":policy_time", "fac_player_faction", dplmc_slot_faction_patrol_time),
(ge, ":current_hours", ":policy_time"),

(store_troop_gold,":gold","trp_household_possessions"),
(ge,":gold",1000),
],
"A small one.", "dplmc_constable_patrol_location_ask",
[
(assign, "$temp", 0),
]],
[anyone|plyr, "dplmc_constable_patrol_size",
[
(store_current_hours, ":current_hours"),
(val_sub, ":current_hours", 24 * 7),
(faction_get_slot, ":policy_time", "fac_player_faction", dplmc_slot_faction_patrol_time),
(ge, ":current_hours", ":policy_time"),

(store_troop_gold,":gold","trp_household_possessions"),
(ge,":gold",2000),
],
"A medium one.", "dplmc_constable_patrol_location_ask",
[
(assign, "$temp", 1),
]],
[anyone|plyr, "dplmc_constable_patrol_size",
[
(store_current_hours, ":current_hours"),
(val_sub, ":current_hours", 24 * 7),
(faction_get_slot, ":policy_time", "fac_player_faction", dplmc_slot_faction_patrol_time),
(ge, ":current_hours", ":policy_time"),

(store_troop_gold,":gold","trp_household_possessions"),
(ge,":gold",3000),
],
"A big one.", "dplmc_constable_patrol_location_ask",
[
(assign, "$temp", 2),
]],
[anyone|plyr, "dplmc_constable_patrol_size",
[
(store_current_hours, ":current_hours"),
(val_sub, ":current_hours", 24 * 7),
(faction_get_slot, ":policy_time", "fac_player_faction", dplmc_slot_faction_patrol_time),
(ge, ":current_hours", ":policy_time"),

(store_troop_gold,":gold","trp_household_possessions"),
(ge,":gold",2000),
],
"Get the best troops around.", "dplmc_constable_patrol_location_ask",
[
(assign, "$temp", 3),
]],
[anyone|plyr, "dplmc_constable_patrol_size",
[],
"None.", "dplmc_constable_pretalk",
[]],
[anyone, "dplmc_constable_patrol_location_ask",
[],
"Where do you want to send the patrol?", "dplmc_constable_patrol_location",
[]],
[anyone|plyr|repeat_for_parties, "dplmc_constable_patrol_location",
[
(store_repeat_object, ":party_no"),
(is_between, ":party_no", centers_begin, centers_end),
(store_faction_of_party, ":party_faction", ":party_no"),
(eq, ":party_faction", "$players_kingdom"),
(str_store_party_name, s11, ":party_no"),
],
"{!}{s11}.", "dplmc_constable_patrol_confirm_ask",
[
(store_repeat_object, "$diplomacy_var"),
]
],
[anyone|plyr, "dplmc_constable_patrol_location",
[],
"Nowhere.", "dplmc_constable_pretalk",
[]],
[anyone, "dplmc_constable_patrol_confirm_ask",
[
(assign, ":size", "str_dplmc_small"),
(val_add, ":size", "$temp"),
(str_store_string, s8, ":size"),
(str_store_party_name, s9, "$diplomacy_var"),
],
"Do you really want to send a {s8} patrol to {s9}?", "dplmc_constable_patrol_confirm",
[]],
[anyone|plyr, "dplmc_constable_patrol_confirm",
[],
"Yes.", "dplmc_constable_pretalk",
[
(store_current_hours, ":current_hours"),
(faction_set_slot, "fac_player_faction", dplmc_slot_faction_patrol_time, ":current_hours"),
(call_script, "script_dplmc_send_patrol", "$current_town", "$diplomacy_var", "$temp", "$players_kingdom", "trp_player"),
]
],
[anyone|plyr, "dplmc_constable_patrol_confirm",
[],
"No.", "dplmc_constable_pretalk",
[]],
[anyone|plyr, "dplmc_constable_security",
[],
"I want to change the target of a patrol.", "dplmc_constable_patrol_change_ask",
[]],
[anyone, "dplmc_constable_patrol_change_ask",
[],
"Which patrol should change the target?", "dplmc_constable_patrol_change",
[]],
[anyone|plyr|repeat_for_parties, "dplmc_constable_patrol_change",
[
(store_repeat_object, ":party_no"),
(party_slot_eq,":party_no", slot_party_type, spt_patrol),
(party_slot_eq, ":party_no", dplmc_slot_party_mission_diplomacy, "trp_player"),
(str_store_party_name, s11, ":party_no"),
],
"{!}{s11}.", "dplmc_constable_patrol_change_target_ask",
[
(store_repeat_object, "$diplomacy_var"),
]],
[anyone|plyr, "dplmc_constable_patrol_change",
[],
"None.", "dplmc_constable_security_ask",
[]],
[anyone, "dplmc_constable_patrol_change_target_ask",
[],
"Where do you want to send it?", "dplmc_constable_patrol_change_target",
[]],
[anyone|plyr|repeat_for_parties, "dplmc_constable_patrol_change_target",
[
(store_repeat_object, ":party_no"),
(is_between, ":party_no", centers_begin, centers_end),
(store_faction_of_party, ":party_faction", ":party_no"),
(eq, ":party_faction", "$players_kingdom"),
(str_store_party_name, s11, ":party_no"),
],
"{!}{s11}.", "dplmc_constable_patrol_change_target_confirm_ask",
[
(store_repeat_object, "$temp"),
]
],
[anyone|plyr, "dplmc_constable_patrol_change_target",
[],
"Nowhere.", "dplmc_constable_security_ask",
[]],
[anyone, "dplmc_constable_patrol_change_target_confirm_ask",
[
(str_store_party_name, s5, "$diplomacy_var"),
(str_store_party_name, s6, "$temp"),
],
"As you wish, I will send a messenger carrying the orders to patrol {s6} to the {s5}.", "dplmc_constable_patrol_change_target_confirm",
[]],
[anyone|plyr, "dplmc_constable_patrol_change_target_confirm",
[],
"Thank you.", "dplmc_constable_security_ask",
[
(call_script, "script_dplmc_send_messenger_to_party", "$diplomacy_var", spai_patrolling_around_center, "$temp"),
]],
[anyone|plyr, "dplmc_constable_patrol_change_target_confirm",
[],
"Oh maybe not.", "dplmc_constable_security_ask",
[]],
[anyone|plyr, "dplmc_constable_security",
[],
"I want a patrol to return to a center.", "dplmc_constable_patrol_to_center_ask",
[]],
[anyone, "dplmc_constable_patrol_to_center_ask",
[],
"Which patrol should move to a center?", "dplmc_constable_patrol_to_center",
[]],
[anyone|plyr|repeat_for_parties, "dplmc_constable_patrol_to_center",
[
(store_repeat_object, ":party_no"),
(party_slot_eq,":party_no", slot_party_type, spt_patrol),
(party_slot_eq, ":party_no", dplmc_slot_party_mission_diplomacy, "trp_player"),
(str_store_party_name, s11, ":party_no"),
],
"{!}{s11}.", "dplmc_constable_patrol_to_center_target_ask",
[
(store_repeat_object, "$diplomacy_var"),
]],
[anyone|plyr, "dplmc_constable_patrol_to_center",
[],
"None.", "dplmc_constable_security_ask",
[]],
[anyone, "dplmc_constable_patrol_to_center_target_ask",
[],
"Where do you want to send it?", "dplmc_constable_patrol_to_center_target",
[]],
[anyone|plyr|repeat_for_parties, "dplmc_constable_patrol_to_center_target",
[
(store_repeat_object, ":party_no"),
(is_between, ":party_no", centers_begin, centers_end),
(store_faction_of_party, ":party_faction", ":party_no"),
(eq, ":party_faction", "$players_kingdom"),
(str_store_party_name, s11, ":party_no"),
],
"{!}{s11}.", "dplmc_constable_patrol_change_to_center_confirm_ask",
[
(store_repeat_object, "$temp"),
]
],
[anyone|plyr, "dplmc_constable_patrol_to_center_target",
[],
"Nowhere.", "dplmc_constable_security_ask",
[]],
[anyone, "dplmc_constable_patrol_change_to_center_confirm_ask",
[
(str_store_party_name, s5, "$diplomacy_var"),
(str_store_party_name, s6, "$temp"),
],
"As you wish, I will send a messenger carrying the orders to move to {s6} to the {s5}.", "dplmc_constable_patrol_to_center_confirm",
[]],
[anyone|plyr, "dplmc_constable_patrol_to_center_confirm",
[],
"Thank you.", "dplmc_constable_security_ask",
[
(call_script, "script_dplmc_send_messenger_to_party", "$diplomacy_var", spai_retreating_to_center, "$temp"),
]],
[anyone|plyr, "dplmc_constable_patrol_to_center_confirm",
[],
"Oh maybe not.", "dplmc_constable_security_ask",
[]],
[anyone|plyr, "dplmc_constable_security",
[],
"I want to disband a patrol.", "dplmc_constable_patrol_disband_ask",
[]],
[anyone, "dplmc_constable_patrol_disband_ask",
[],
"Which patrol do you want to disband?", "dplmc_constable_patrol_disband",
[]],
[anyone|plyr|repeat_for_parties, "dplmc_constable_patrol_disband",
[
(store_repeat_object, ":party_no"),
(party_slot_eq,":party_no", slot_party_type, spt_patrol),
(party_slot_eq, ":party_no", dplmc_slot_party_mission_diplomacy, "trp_player"),
(str_store_party_name, s11, ":party_no"),
],
"{!}{s11}.", "dplmc_constable_patrol_disband_confirm_ask",
[
(store_repeat_object, "$diplomacy_var"),
]],
[anyone|plyr, "dplmc_constable_patrol_disband",
[],
"None.", "dplmc_constable_pretalk",
[]],
[anyone, "dplmc_constable_patrol_disband_confirm_ask",
[
(str_store_party_name, s5, "$diplomacy_var"),
],
"As you wish, I will send a messenger who will tell {s5} to disband.", "dplmc_constable_patrol_disband_confirm",
[]],
[anyone|plyr, "dplmc_constable_patrol_disband_confirm",
[],
"Thank you.", "dplmc_constable_security_ask",
[
##diplomacy start+
#fix for the disbanding bug, credit Caba`drin
#OLD:
#(call_script, "script_dplmc_send_messenger_to_party", "$diplomacy_var", spai_retreating_to_center, -1),
#NEW:
(call_script, "script_dplmc_send_messenger_to_party", "$diplomacy_var", spai_undefined, -1),
##diplomacy end+
]],
[anyone|plyr, "dplmc_constable_patrol_disband_confirm",
[],
"No.", "dplmc_constable_security_ask",
[]],
[anyone|plyr, "dplmc_constable_security",
[],
"Nevermind.", "dplmc_constable_pretalk",
[]],
[anyone|plyr,"dplmc_constable_talk",
[(store_num_regular_prisoners,reg0),(ge,reg0,1)],
"I have some prisoners can you sell them for me?", "dplmc_constable_prisoner",[]],
[anyone,"dplmc_constable_prisoner", [],
"Of course, my {lord/lady}", "dplmc_constable_pretalk",
[[change_screen_trade_prisoners]]],
[anyone|plyr, "dplmc_constable_talk",
[
],
"You are dismissed.", "dplmc_constable_dismiss_confirm_ask",
[]],
[anyone, "dplmc_constable_dismiss_confirm_ask",
[
],
"Are you sure that you don't need me anymore?", "dplmc_constable_dismiss_confirm",
[]],
[anyone|plyr, "dplmc_constable_dismiss_confirm",
[
],
"Yes I am.", "dplmc_constable_dismiss_confirm_yes",
[]],
[anyone, "dplmc_constable_dismiss_confirm_yes",
[
],
"As you wish.", "close_window",
[
(assign, "$g_player_constable", -1),
(assign, "$g_constable_training_center", -1),
]],
[anyone|plyr, "dplmc_constable_dismiss_confirm",
[
],
"No I am not.", "dplmc_constable_pretalk",
[]],
[anyone|plyr,"dplmc_constable_talk",
[],
"Thank you, I will come back to you later.", "close_window",[
]],
[anyone,"dplmc_chamberlain_pretalk",
[],
"Anything else, my {lord/lady}?", "dplmc_chamberlain_talk",[
]],
[anyone|plyr, "dplmc_chamberlain_talk",
[
],
"Please give me a report about the financial affairs.", "dplmc_chamberlain_overview",
[]],
[anyone, "dplmc_chamberlain_overview",
[
(assign, ":income", 0),
(assign, ":total_wage", 0),
(assign, ":num_owned_center_values_for_tax_efficiency", 0),
(try_for_range, ":selected_party", centers_begin, centers_end),
  (party_slot_eq, ":selected_party", slot_town_lord, "trp_player"),

  (val_add, ":num_owned_center_values_for_tax_efficiency", 1),

  (party_get_slot, ":accumulated_rents", ":selected_party", slot_center_accumulated_rents),
  (val_add, ":income", ":accumulated_rents"),

  (str_clear, s60),
  (try_begin),
    (this_or_next|party_slot_eq, ":selected_party", slot_party_type, spt_town),
    (party_slot_eq, ":selected_party", slot_party_type, spt_castle),
    (party_get_num_companion_stacks, ":num_stacks", ":selected_party"),

    (assign, ":troop_size", 0),
    (party_get_num_companion_stacks, ":num_stacks", ":selected_party"),
    (try_for_range, ":i_stack", 0, ":num_stacks"),
      (party_stack_get_troop_id, ":stack_troop", ":selected_party", ":i_stack"),
      (party_stack_get_size, ":stack_size", ":selected_party", ":i_stack"),
      (val_add, ":troop_size", ":stack_size"),
      (call_script, "script_game_get_troop_wage", ":stack_troop", ":selected_party"),
      (assign, ":cur_wage", reg0),
      (val_mul, ":cur_wage", ":stack_size"),
      (val_add, ":total_wage", ":cur_wage"),
    (try_end),

    (try_begin),
      (party_slot_eq, ":selected_party", slot_party_type, spt_town),

      (val_add, ":num_owned_center_values_for_tax_efficiency", 1),
      (party_get_slot, ":accumulated_tariffs", ":selected_party", slot_center_accumulated_tariffs),
      (assign, reg0, ":accumulated_tariffs"),
      (val_add, ":income", ":accumulated_tariffs"),
    (try_end),
  (try_end),
(try_end),

#gekokujo 3.0 microfactions! start
#let's include forts in the count
#they don't count against tax efficiency so we can ignore that part
(try_for_range, ":selected_party", forts_begin, forts_end),
  (party_slot_eq, ":selected_party", slot_fort_captured, 1),
  
  (assign, ":troop_size", 0),
  (party_get_num_companion_stacks, ":num_stacks", ":selected_party"),
  (try_for_range, ":i_stack", 0, ":num_stacks"),
    (party_stack_get_troop_id, ":stack_troop", ":selected_party", ":i_stack"),
    (party_stack_get_size, ":stack_size", ":selected_party", ":i_stack"),
    (val_add, ":troop_size", ":stack_size"),
    (call_script, "script_game_get_troop_wage", ":stack_troop", ":selected_party"),
    (assign, ":cur_wage", reg0),
    (val_mul, ":cur_wage", ":stack_size"),
    (val_add, ":total_wage", ":cur_wage"),
  (try_end),
(try_end),
#gekokujo 3.0 microfactions! end

(val_div, ":total_wage", 2), #Half payment for garrisons
(assign, reg0, ":income"),
(assign, reg1, ":total_wage"),

(str_store_string, s6, "@We currently have an income of {reg0} mon and costs of {reg1} mon from fiefs and garrions."),

(assign, ":tax_lost", 0),
(try_begin),
(gt, ":num_owned_center_values_for_tax_efficiency", 3),
(store_sub, ":ratio_lost", ":num_owned_center_values_for_tax_efficiency", 3),
(val_mul, ":ratio_lost", 9),
(val_min, ":ratio_lost", 140),
(store_mul, ":tax_lost", ":income", ":ratio_lost"),
(val_div, ":tax_lost", 200),
(try_end),

(try_begin),
(gt, ":tax_lost", 0),
(store_mul, ":tax_lost_percent", ":tax_lost", 100),
(val_div, ":tax_lost_percent", ":income"),
(assign, reg0, ":tax_lost"),
(assign, reg1, ":tax_lost_percent"),
(str_store_string, s6, "@{s6} We are losing {reg0} mon due to tax inefficiency. That means {reg1} percent."),
(try_end),

(assign, ":overall", ":income"),
(val_sub, ":overall", ":total_wage"),
(val_sub, ":overall", ":tax_lost"),
(assign, reg0, ":overall"),
(str_store_string, s6, "@{s6} Overall this sums up to {reg0} mon."),
],
"{!}{s6}", "dplmc_chamberlain_pretalk",
[]],
[anyone|plyr, "dplmc_chamberlain_talk",
[
],
"Let us inspect the treasury.", "dplmc_chamberlain_treasury",
[]],
[anyone, "dplmc_chamberlain_treasury",
[
(store_troop_gold, ":treasury", "trp_household_possessions"),
(assign, reg0, ":treasury"),
(str_store_string, s4, "@{!}{reg0}"),
(try_begin),
(gt, "$g_player_debt_to_party_members", 0),
(assign, reg0, "$g_player_debt_to_party_members"),
(str_store_string, s6, "@{reg0} mon"),
(else_try),
(str_store_string, s6, "@no"),
(try_end),
],
"There are currently {s4} mon in the treasury and we have {s6} debts. What do you want to do?", "dplmc_chamberlain_treasury_action",
[]],
[anyone|plyr, "dplmc_chamberlain_treasury_action",
[
],
"I would like to pay into the treasury.", "dplmc_chamberlain_treasury_action_pay",
[]],
[anyone, "dplmc_chamberlain_treasury_action_pay",
[
(store_troop_gold, ":treasury", "trp_household_possessions"),
(assign, reg0, ":treasury"),
(str_store_string, s4, "@{!}{reg0}"),
],
"We currently have {s4} mon in the treasury. How much money do you like to pay into the treasury, my {lord/lady}?", "dplmc_chamberlain_treasury_action_pay_select",
[]],
[anyone|plyr, "dplmc_chamberlain_treasury_action_pay_select",
[
(store_troop_gold, ":gold", "trp_player"),
(ge, ":gold", 100),
],
"100.", "dplmc_chamberlain_treasury_action_pay",
[
(troop_remove_gold, "trp_player", 100),
(call_script, "script_dplmc_pay_into_treasury", 100),
]],
[anyone|plyr, "dplmc_chamberlain_treasury_action_pay_select",
[
(store_troop_gold, ":gold", "trp_player"),
(ge, ":gold", 200),
],
"200.", "dplmc_chamberlain_treasury_action_pay",
[
(troop_remove_gold, "trp_player", 200),
(call_script, "script_dplmc_pay_into_treasury", 200),
]],
[anyone|plyr, "dplmc_chamberlain_treasury_action_pay_select",
[
(store_troop_gold, ":gold", "trp_player"),
(ge, ":gold", 500),
],
"500.", "dplmc_chamberlain_treasury_action_pay",
[
(troop_remove_gold, "trp_player", 500),
(call_script, "script_dplmc_pay_into_treasury", 500),
]],
[anyone|plyr, "dplmc_chamberlain_treasury_action_pay_select",
[
(store_troop_gold, ":gold", "trp_player"),
(ge, ":gold", 1000),
],
"1000.", "dplmc_chamberlain_treasury_action_pay",
[
(troop_remove_gold, "trp_player", 1000),
(call_script, "script_dplmc_pay_into_treasury", 1000),
]],
[anyone|plyr, "dplmc_chamberlain_treasury_action_pay_select",
[
(store_troop_gold, ":gold", "trp_player"),
(ge, ":gold", 2000),
],
"2000.", "dplmc_chamberlain_treasury_action_pay",
[
(troop_remove_gold, "trp_player", 2000),
(call_script, "script_dplmc_pay_into_treasury", 2000),
]],
[anyone|plyr, "dplmc_chamberlain_treasury_action_pay_select",
[
(store_troop_gold, ":gold", "trp_player"),
(ge, ":gold", 5000),
],
"5000.", "dplmc_chamberlain_treasury_action_pay",
[
(troop_remove_gold, "trp_player", 5000),
(call_script, "script_dplmc_pay_into_treasury", 5000),
]],
[anyone|plyr, "dplmc_chamberlain_treasury_action_pay_select",
[
(store_troop_gold, ":gold", "trp_player"),
(ge, ":gold", 10000),
],
"10000.", "dplmc_chamberlain_treasury_action_pay",
[
(troop_remove_gold, "trp_player", 10000),
(call_script, "script_dplmc_pay_into_treasury", 10000),
]],
[anyone|plyr, "dplmc_chamberlain_treasury_action_pay_select",
[],
"Never mind.", "dplmc_chamberlain_pretalk",
[]],
[anyone|plyr, "dplmc_chamberlain_treasury_action",
[
],
"I would like to withdraw money from the treasury.", "dplmc_chamberlain_treasury_action_withdraw",
[]],
[anyone, "dplmc_chamberlain_treasury_action_withdraw",
[
(store_troop_gold, ":treasury", "trp_household_possessions"),
(assign, reg0, ":treasury"),
(str_store_string, s4, "@{!}{reg0}"),
],
"We currently have {s4} mon in the treasury. How much money do you like to withdraw from the treasury, my {lord/lady}?", "dplmc_chamberlain_treasury_action_withdraw_select",
[]],
[anyone|plyr, "dplmc_chamberlain_treasury_action_withdraw_select",
[
(store_troop_gold, ":gold", "trp_household_possessions"),
(ge, ":gold", 100),
],
"100.", "dplmc_chamberlain_treasury_action_withdraw",
[
(call_script, "script_dplmc_withdraw_from_treasury", 100),
(troop_add_gold, "trp_player", 100),
]],
[anyone|plyr, "dplmc_chamberlain_treasury_action_withdraw_select",
[
(store_troop_gold, ":gold", "trp_household_possessions"),
(ge, ":gold", 200),
],
"200.", "dplmc_chamberlain_treasury_action_withdraw",
[
(call_script, "script_dplmc_withdraw_from_treasury", 200),
(troop_add_gold, "trp_player", 200),
]],
[anyone|plyr, "dplmc_chamberlain_treasury_action_withdraw_select",
[
(store_troop_gold, ":gold", "trp_household_possessions"),
(ge, ":gold", 500),
],
"500.", "dplmc_chamberlain_treasury_action_withdraw",
[
(call_script, "script_dplmc_withdraw_from_treasury", 500),
(troop_add_gold, "trp_player", 500),
]],
[anyone|plyr, "dplmc_chamberlain_treasury_action_withdraw_select",
[
(store_troop_gold, ":gold", "trp_household_possessions"),
(ge, ":gold", 1000),
],
"1000.", "dplmc_chamberlain_treasury_action_withdraw",
[
(call_script, "script_dplmc_withdraw_from_treasury", 1000),
(troop_add_gold, "trp_player", 1000),
]],
[anyone|plyr, "dplmc_chamberlain_treasury_action_withdraw_select",
[
(store_troop_gold, ":gold", "trp_household_possessions"),
(ge, ":gold", 2000),
],
"2000.", "dplmc_chamberlain_treasury_action_withdraw",
[
(call_script, "script_dplmc_withdraw_from_treasury", 2000),
(troop_add_gold, "trp_player", 2000),
]],
[anyone|plyr, "dplmc_chamberlain_treasury_action_withdraw_select",
[
(store_troop_gold, ":gold", "trp_household_possessions"),
(ge, ":gold", 5000),
],
"5000.", "dplmc_chamberlain_treasury_action_withdraw",
[
(call_script, "script_dplmc_withdraw_from_treasury", 5000),
(troop_add_gold, "trp_player", 5000),
]],
[anyone|plyr, "dplmc_chamberlain_treasury_action_withdraw_select",
[
(store_troop_gold, ":gold", "trp_household_possessions"),
(ge, ":gold", 10000),
],
"10000.", "dplmc_chamberlain_treasury_action_withdraw",
[
(call_script, "script_dplmc_withdraw_from_treasury", 10000),
(troop_add_gold, "trp_player", 10000),
]],
[anyone|plyr, "dplmc_chamberlain_treasury_action_withdraw_select",
[],
"Never mind.", "dplmc_chamberlain_pretalk",
[]],
[anyone|plyr, "dplmc_chamberlain_treasury_action",
[
],
"Thank you, let's talk about something else.", "dplmc_chamberlain_pretalk",
[]],
[anyone|plyr, "dplmc_chamberlain_talk",
[
],
"Please give me a status report about the financial situation of a fief.", "dplmc_chamberlain_status",
[]],
[anyone, "dplmc_chamberlain_status",
[],
"About which fief do you like to be informed?", "dplmc_chamberlain_status_select_fief",
[]],
[anyone|plyr|repeat_for_parties, "dplmc_chamberlain_status_select_fief",
[
(store_repeat_object, ":party_no"),
(is_between, ":party_no", centers_begin, centers_end),
(party_slot_eq, ":party_no", slot_town_lord, "trp_player"),
(str_store_party_name, s60, ":party_no"),
],
"{!}{s60}", "dplmc_chamberlain_status_info",
[
(store_repeat_object, "$diplomacy_var"),
]],
[anyone|plyr, "dplmc_chamberlain_status_select_fief",
[],
"Never mind.", "dplmc_chamberlain_pretalk",
[]],
[anyone, "dplmc_chamberlain_status_info",
[
(assign, ":selected_party", "$diplomacy_var"),
(str_store_party_name, s60, ":selected_party"),
(try_begin),
  (party_slot_ge, ":selected_party", slot_village_infested_by_bandits, 1),
  (str_store_string, s51, "@{s60} is currently occupied by outlaws you should counter them as soon as possible."),
(else_try),
  (party_get_slot, ":relation", ":selected_party", slot_center_player_relation),
  (call_script, "script_describe_center_relation_to_s3", ":relation"),
  (party_get_slot, ":tax_rate", ":selected_party", dplmc_slot_center_taxation),
  (call_script, "script_dplmc_describe_tax_rate_to_s50", ":tax_rate"),

  (party_get_slot, ":accumulated_rents", ":selected_party", slot_center_accumulated_rents),
  (assign, reg0, ":accumulated_rents"),
  (str_store_string, s61, "@ We are expecting {reg0} mon for rents"),

  (assign, ":overall", ":accumulated_rents"),
  (assign, ":total_wage", 0),
  (str_clear, s59),
  (try_begin),
    (this_or_next|party_slot_eq, ":selected_party", slot_party_type, spt_town),
    (party_slot_eq, ":selected_party", slot_party_type, spt_castle),
    (party_get_num_companion_stacks, ":num_stacks", ":selected_party"),

    (assign, ":troop_size", 0),
    (party_get_num_companion_stacks, ":num_stacks", ":selected_party"),
    (try_for_range, ":i_stack", 0, ":num_stacks"),
      (party_stack_get_troop_id, ":stack_troop", ":selected_party", ":i_stack"),
      (party_stack_get_size, ":stack_size", ":selected_party", ":i_stack"),
      (val_add, ":troop_size", ":stack_size"),
      (call_script, "script_game_get_troop_wage", ":stack_troop", ":selected_party"),
      (assign, ":cur_wage", reg0),
      (val_mul, ":cur_wage", ":stack_size"),
      (val_add, ":total_wage", ":cur_wage"),
    (try_end),
    (val_div, ":total_wage", 2), #Half payment for garrisons
    (assign, reg0, ":troop_size"),
    (assign, reg1, ":total_wage"),
    (str_store_string, s59, "@ The troop wages for {reg0} troops cost us {reg1} mon."),


    (try_begin),
      (party_slot_eq, ":selected_party", slot_party_type, spt_town),
      (party_get_slot, ":accumulated_tariffs", ":selected_party", slot_center_accumulated_tariffs),
      (assign, reg0, ":accumulated_tariffs"),
      (str_store_string, s61, "@{s61} and {reg0} mon for tariffs"),
      (val_add, ":overall", ":accumulated_tariffs"),
    (try_end),
  (try_end),

  (try_begin),
    (this_or_next|is_between, ":selected_party", villages_begin, villages_end),
    (is_between, ":selected_party", towns_begin, towns_end),
    (call_script, "script_dplmc_describe_prosperity_to_s4", ":selected_party"),
  (else_try),
    (str_store_string, s4, "@Well, {s60}."),
  (try_end),

  (val_sub, ":overall", ":total_wage"),
  (assign, reg0, ":overall"),
  (str_store_string, s62, "@{!}{reg0}"),

  (str_store_string, s51, "@{s4} {s3}. The tax rate is {s50}.{s59}{s61}. Overall this sums up to {s62} mon."),
(try_end),
],
"{!}{s51}", "dplmc_chamberlain_status",
[]],
[anyone|plyr, "dplmc_chamberlain_talk",
[
],
"I wish to change the tax rate for a fief.", "dplmc_chamberlain_tax",
[]],
[anyone, "dplmc_chamberlain_tax",
[
],
"For which fief?", "dplmc_chamberlain_tax_select_center",
[]],
[anyone|plyr|repeat_for_parties, "dplmc_chamberlain_tax_select_center",
[
(store_repeat_object, ":center_no"),
(this_or_next|is_between, ":center_no", towns_begin, towns_end),
(is_between, ":center_no", villages_begin, villages_end),
(party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
(store_faction_of_party, ":center_faction", ":center_no"),
(this_or_next|eq, ":center_faction", "fac_player_supporters_faction"),
(eq, ":center_faction", "$players_kingdom"),
(str_store_party_name, s6, ":center_no"),
],
"{!}{s6}", "dplmc_chamberlain_tax_ask_rate",
[
(store_repeat_object, "$diplomacy_var"),
]],
[anyone|plyr, "dplmc_chamberlain_tax_select_center",
[
],
"Never mind.", "dplmc_chamberlain_pretalk",
[]],
[anyone, "dplmc_chamberlain_tax_ask_rate",
[
(str_store_party_name, s6, "$diplomacy_var"),
],
"How high do you want to set the tax rate for {s6}?", "dplmc_chamberlain_tax_select_rate",
[
]],
[anyone|plyr, "dplmc_chamberlain_tax_select_rate",
[
(neg|party_slot_eq, "$diplomacy_var", dplmc_slot_center_taxation, -50),
],
"Very low.", "dplmc_chamberlain_tax_ask_confirm",
[
(str_store_string, s11, "str_dplmc_tax_very_low"),
(assign, "$diplomacy_tax_rate", -50),
]],
[anyone|plyr, "dplmc_chamberlain_tax_select_rate",
[
(neg|party_slot_eq, "$diplomacy_var", dplmc_slot_center_taxation, -25),
],
"Low.", "dplmc_chamberlain_tax_ask_confirm",
[
(str_store_string, s11, "str_dplmc_tax_low"),
(assign, "$diplomacy_tax_rate", -25),
]],
[anyone|plyr, "dplmc_chamberlain_tax_select_rate",
[
(neg|party_slot_eq, "$diplomacy_var", dplmc_slot_center_taxation, 0),
],
"Normal.", "dplmc_chamberlain_tax_ask_confirm",
[
(str_store_string, s11, "str_dplmc_tax_normal"),
(assign, "$diplomacy_tax_rate", 0),
]],
[anyone|plyr, "dplmc_chamberlain_tax_select_rate",
[
(neg|party_slot_eq, "$diplomacy_var", dplmc_slot_center_taxation, 25),
],
"High.", "dplmc_chamberlain_tax_ask_confirm",
[
(str_store_string, s11, "str_dplmc_tax_high"),
(assign, "$diplomacy_tax_rate", 25),
]],
[anyone|plyr, "dplmc_chamberlain_tax_select_rate",
[
(neg|party_slot_eq, "$diplomacy_var", dplmc_slot_center_taxation, 50),
],
"Very High.", "dplmc_chamberlain_tax_ask_confirm",
[
(str_store_string, s11, "str_dplmc_tax_very_high"),
(assign, "$diplomacy_tax_rate", 50),
]],
[anyone|plyr, "dplmc_chamberlain_tax_select_rate",
[
],
"Never mind.", "dplmc_chamberlain_pretalk",
[]],
[anyone, "dplmc_chamberlain_tax_ask_confirm",
[
],
"Do you really want to set the tax rate for {s6} to {s11}?", "dplmc_chamberlain_tax_confirm",
[]],
[anyone|plyr, "dplmc_chamberlain_tax_confirm",
[
],
"Yes.", "dplmc_chamberlain_pretalk",
[
(party_set_slot, "$diplomacy_var", dplmc_slot_center_taxation, "$diplomacy_tax_rate"),
(display_message, "@Tax rate for {s6}: {s11}"),
]],
[anyone|plyr, "dplmc_chamberlain_tax_confirm",
[
],
"No I changed, my mind.", "dplmc_chamberlain_pretalk",
[
]],
[anyone|plyr, "dplmc_chamberlain_talk",
[
],
"I would like to manage fief improvements.", "dplmc_chamberlain_manage_fiefs",
[]],
[anyone, "dplmc_chamberlain_manage_fiefs",
[
(assign, ":fief_count", 0),
(assign, ":center_count", 0),
(assign, ":num_improvements", 0),
(try_for_parties, ":center_no"),
(this_or_next|is_between, ":center_no", towns_begin, towns_end),
(is_between, ":center_no", villages_begin, villages_end),
(party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
(store_faction_of_party, ":center_faction", ":center_no"),
(this_or_next|eq, ":center_faction", "fac_player_supporters_faction"),
(eq, ":center_faction", "$players_kingdom"),

(val_add, ":fief_count", 1),

(try_begin),
  (party_slot_eq, ":center_no", slot_party_type, spt_village),
  (assign, ":begin", village_improvements_begin),
  (assign, ":end", village_improvements_end),
(else_try),
  (party_slot_eq, ":center_no", slot_party_type, spt_town),
  (assign, ":begin", walled_center_improvements_begin),
  (assign, ":end", walled_center_improvements_end),
(try_end),

(assign, ":has_building", 0),
(try_for_range, ":improvement_no", ":begin", ":end"),
  (party_slot_ge, ":center_no", ":improvement_no", 1),
  (val_add,  ":num_improvements", 1),
  (assign, ":has_building", 1),
(try_end),

(val_add, ":center_count", ":has_building"),

(try_end),

(assign, reg0, ":num_improvements"),
(assign, reg1, ":center_count"),
(assign, reg2, ":fief_count"),

],
"We are currently have {reg0} improvements in {reg1} of your {reg2} fiefs. Do you want to build another one?", "dplmc_chamberlain_manage_fiefs_options",
[]],
[anyone|plyr, "dplmc_chamberlain_manage_fiefs_options",
[
],
"Yes, I want to build an improvement.", "dplmc_chamberlain_manage_fiefs_build",
[]],
[anyone|plyr, "dplmc_chamberlain_manage_fiefs_options",
[
],
"No.", "dplmc_chamberlain_pretalk",
[]],
[anyone, "dplmc_chamberlain_manage_fiefs_build",
[
],
"Where do you want to build an improvement?", "dplmc_chamberlain_manage_fiefs_build_location",
[]],
[anyone|plyr|repeat_for_parties, "dplmc_chamberlain_manage_fiefs_build_location",
[
(store_repeat_object, ":center_no"),
(is_between, ":center_no", centers_begin, centers_end),
(party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
(store_faction_of_party, ":center_faction", ":center_no"),
(this_or_next|eq, ":center_faction", "fac_player_supporters_faction"),
(eq, ":center_faction", "$players_kingdom"),

(assign, ":improvement_possible", 0),
(try_begin),
(party_slot_eq, ":center_no", slot_party_type, spt_village),
(assign, ":begin", village_improvements_begin),
(assign, ":end", village_improvements_end),
(else_try),
(assign, ":begin", walled_center_improvements_begin),
(assign, ":end", walled_center_improvements_end),
(try_end),

(try_for_range, ":improvement_no", ":begin", ":end"),
(party_slot_eq, ":center_no", ":improvement_no", 0),
(assign, ":improvement_possible", 1),
(try_end),
(eq, ":improvement_possible", 1),

(str_store_party_name, s2, ":center_no"),

],
"{s2}.", "dplmc_chamberlain_manage_fiefs_build_ask",
[
(store_repeat_object, "$diplomacy_var"),
]],
[anyone|plyr, "dplmc_chamberlain_manage_fiefs_build_location",
[
],
"Nowhere.", "dplmc_chamberlain_pretalk",
[]],
[anyone, "dplmc_chamberlain_manage_fiefs_build_ask",
[

(try_begin),
 (party_slot_eq, "$diplomacy_var", slot_party_type, spt_village),
 (assign, ":begin", village_improvements_begin),
 (assign, ":end", village_improvements_end),
 (str_store_string, s17, "@village"),
(else_try),
 (assign, ":begin", walled_center_improvements_begin),
 (assign, ":end", walled_center_improvements_end),
 (party_slot_eq, "$diplomacy_var", slot_party_type, spt_town),
 (str_store_string, s17, "@town"),
(else_try),
 (str_store_string, s17, "@castle"),
(try_end),

(assign, ":num_improvements", 0),
(try_for_range, ":improvement_no", ":begin", ":end"),
 (party_slot_ge, "$diplomacy_var", ":improvement_no", 1),
 (val_add,  ":num_improvements", 1),
 (call_script, "script_get_improvement_details", ":improvement_no"),
 (try_begin),
   (eq,  ":num_improvements", 1),
   (str_store_string, s18, "@{!}{s0}"),
 (else_try),
   (str_store_string, s18, "@{!}{s18}, {s0}"),
 (try_end),
(try_end),

(try_begin),
 (eq,  ":num_improvements", 0),
 (str_store_string, s19, "@The {s17} has no improvements."),
(else_try),
 (str_store_string, s19, "@The {s17} has the following improvements: {s18}."),
(try_end),

(party_get_slot, ":cur_improvement", "$diplomacy_var", slot_center_current_improvement),
(gt, ":cur_improvement", 0),
(call_script, "script_get_improvement_details", ":cur_improvement"),
(str_store_string, s7, s0),
(assign, reg6, 1),
(store_current_hours, ":cur_hours"),
(party_get_slot, ":finish_time", "$diplomacy_var", slot_center_improvement_end_hour),
(val_sub, ":finish_time", ":cur_hours"),
(store_div, reg8, ":finish_time", 24),
(val_max, reg8, 1),
(store_sub, reg9, reg8, 1),

],
"{s19}  You are currently building {s7}. The building will be completed after {reg8} day{reg9?s:}. We have to wait until it's finished.", "dplmc_chamberlain_pretalk",
[]],
[anyone, "dplmc_chamberlain_manage_fiefs_build_ask",
[

(try_begin),
 (party_slot_eq, "$diplomacy_var", slot_party_type, spt_village),
 (assign, ":begin", village_improvements_begin),
 (assign, ":end", village_improvements_end),
 (str_store_string, s17, "@village"),
(else_try),
 (assign, ":begin", walled_center_improvements_begin),
 (assign, ":end", walled_center_improvements_end),
 (party_slot_eq, "$diplomacy_var", slot_party_type, spt_town),
 (str_store_string, s17, "@town"),
(else_try),
 (str_store_string, s17, "@castle"),
(try_end),

(assign, ":num_improvements", 0),
(try_for_range, ":improvement_no", ":begin", ":end"),
 (party_slot_ge, "$diplomacy_var", ":improvement_no", 1),
 (val_add,  ":num_improvements", 1),
 (call_script, "script_get_improvement_details", ":improvement_no"),
 (try_begin),
   (eq,  ":num_improvements", 1),
   (str_store_string, s18, "@{!}{s0}"),
 (else_try),
   (str_store_string, s18, "@{!}{s18}, {s0}"),
 (try_end),
(try_end),

(try_begin),
 (eq,  ":num_improvements", 0),
 (str_store_string, s19, "@The {s17} has no improvements."),
(else_try),
 (str_store_string, s19, "@The {s17} has the following improvements: {s18}."),
(try_end),
],
"{s19}  What do you want to build?", "dplmc_chamberlain_manage_fiefs_build_ask2",
[]],
[anyone|plyr, "dplmc_chamberlain_manage_fiefs_build_ask2",
[
(party_slot_eq, "$diplomacy_var", slot_party_type, spt_village),
(party_slot_eq, "$diplomacy_var", slot_center_has_manor, 0),
],
"Build a manor.", "dplmc_chamberlain_manage_fiefs_build_confirm_ask",
[(assign, "$g_improvement_type", slot_center_has_manor),]
],
[anyone|plyr, "dplmc_chamberlain_manage_fiefs_build_ask2",
[
(party_slot_eq, "$diplomacy_var", slot_party_type, spt_village),
(party_slot_eq, "$diplomacy_var", slot_center_has_fish_pond, 0),
],
"Build a mill.", "dplmc_chamberlain_manage_fiefs_build_confirm_ask",
[(assign, "$g_improvement_type", slot_center_has_fish_pond),]
],
[anyone|plyr, "dplmc_chamberlain_manage_fiefs_build_ask2",
[
(party_slot_eq, "$diplomacy_var", slot_party_type, spt_village),
(party_slot_eq, "$diplomacy_var", slot_center_has_watch_tower, 0),
],
"Build a watch tower.", "dplmc_chamberlain_manage_fiefs_build_confirm_ask",
[(assign, "$g_improvement_type", slot_center_has_watch_tower),]
],
[anyone|plyr, "dplmc_chamberlain_manage_fiefs_build_ask2",
[
(party_slot_eq, "$diplomacy_var", slot_party_type, spt_village),
(party_slot_eq, "$diplomacy_var", slot_center_has_school, 0),
],
"Build a shrine.", "dplmc_chamberlain_manage_fiefs_build_confirm_ask",
[(assign, "$g_improvement_type", slot_center_has_school),]
],
[anyone|plyr, "dplmc_chamberlain_manage_fiefs_build_ask2",
[
(party_slot_eq, "$diplomacy_var", slot_party_type, spt_village),
(party_slot_eq, "$diplomacy_var", slot_center_has_messenger_post, 0),
],
"Build a messenger post.", "dplmc_chamberlain_manage_fiefs_build_confirm_ask",
[(assign, "$g_improvement_type", slot_center_has_messenger_post),]
],
[anyone|plyr, "dplmc_chamberlain_manage_fiefs_build_ask2",
[
(this_or_next|party_slot_eq, "$diplomacy_var", slot_party_type, spt_town),
(party_slot_eq, "$diplomacy_var", slot_party_type, spt_castle),
(party_slot_eq, "$diplomacy_var", slot_center_has_prisoner_tower, 0),
],
"Build a prisoner tower.", "dplmc_chamberlain_manage_fiefs_build_confirm_ask",
[(assign, "$g_improvement_type", slot_center_has_prisoner_tower),]
],
[anyone|plyr, "dplmc_chamberlain_manage_fiefs_build_ask2",
[
],
"Nothing.", "dplmc_chamberlain_pretalk",
[]],
[anyone, "dplmc_chamberlain_manage_fiefs_build_confirm_ask",
[
(str_store_party_name, s2, "$diplomacy_var"),

(call_script, "script_get_improvement_details", "$g_improvement_type"),
(assign, ":improvement_cost", reg0),
(str_store_string, s4, s0),
(str_store_string, s19, s1),
(call_script, "script_get_max_skill_of_player_party", "skl_engineer"),
(assign, ":max_skill", reg0),
(assign, ":max_skill_owner", reg1),
(assign, reg2, ":max_skill"),

(store_sub, ":multiplier", 21, ":max_skill"),
(val_mul, ":improvement_cost", ":multiplier"),
(val_div, ":improvement_cost", 20),

(store_div, ":improvement_time", ":improvement_cost", 100),
(val_add, ":improvement_time", 4),

(assign, reg5, ":improvement_cost"),
(assign, reg6, ":improvement_time"),

(try_begin),
 (eq, ":max_skill_owner", "trp_player"),
 (assign, reg3, 1),
(else_try),
 (assign, reg3, 0),
 (str_store_troop_name, s3, ":max_skill_owner"),
(try_end),

(store_troop_gold, reg7, "trp_household_possessions"),
],
"Are you sure that you want to build a {s4} for {reg5} in {s2}? It will take {reg6} days. We currently have {reg7} mon in the treasury.", "dplmc_chamberlain_manage_fiefs_confirm",
[]],
[anyone|plyr, "dplmc_chamberlain_manage_fiefs_confirm",
[
(store_troop_gold, ":cur_gold", "trp_household_possessions"),
(ge, ":cur_gold", reg5),
],
"Yes.", "dplmc_chamberlain_pretalk",
[
(call_script, "script_dplmc_withdraw_from_treasury", reg5),
(party_set_slot, "$diplomacy_var", slot_center_current_improvement, "$g_improvement_type"),
(store_current_hours, ":cur_hours"),
(store_mul, ":hours_takes", reg6, 24),
(val_add, ":hours_takes", ":cur_hours"),
(party_set_slot, "$diplomacy_var", slot_center_improvement_end_hour, ":hours_takes"),
]],
[anyone|plyr, "dplmc_chamberlain_manage_fiefs_confirm",
[],
"No, I don't have the money.", "dplmc_chamberlain_pretalk",
[]],
[anyone|plyr, "dplmc_chamberlain_talk",
[
##diplomacy start+
(assign, ":can_use_secondary_storage", 0),
(try_begin),
   #If the player already has things in the former item pool, allow access to it.
   (troop_get_inventory_capacity, ":capacity", "trp_dplmc_chamberlain"),
   (try_for_range, ":inventory_slot", ek_food + 1, ":capacity"),
     (troop_inventory_slot_get_item_amount, reg0, "trp_dplmc_chamberlain", ":inventory_slot"),
     (gt, reg0, 0),
     (troop_get_inventory_slot, reg0, "trp_dplmc_chamberlain", ":inventory_slot"),
     (neg|troop_has_item_equipped, "trp_dplmc_chamberlain", reg0),
     (assign, ":can_use_secondary_storage", 1),
     (assign, ":capacity", ":inventory_slot"),#stop the loop
   (try_end),
   (eq, ":can_use_secondary_storage", 1),
(else_try),
   #If the player owns any towns or castles, allow use of the former item pool
   #as secondary storage.
   (try_for_range, reg0, walled_centers_begin, walled_centers_end),
      (party_slot_eq, reg0, slot_town_lord, "trp_player"),
	  (assign, ":can_use_secondary_storage", 1),
   (try_end),
(try_end),
(assign, reg0, ":can_use_secondary_storage"),
##diplomacy end+
],
##diplomacy end+
#"I would like to manage the item pool and household.", "dplmc_chamberlain_pools_ask",
"I would like to manage the {reg0?household and secondary storage:household}.", "dplmc_chamberlain_pools_ask",
##diplomacy end+
[]],
[anyone|plyr, "dplmc_chamberlain_pools_ask",
[
],
"What do you want to do?", "dplmc_chamberlain_pools",
[]],
[anyone|plyr, "dplmc_chamberlain_pools",
##diplomacy start+
[
(assign, ":can_use_secondary_storage", 0),
(try_begin),
   #If the player already has things in the former item pool, allow access to it.
   (troop_get_inventory_capacity, ":capacity", "trp_dplmc_chamberlain"),
   (try_for_range, ":inventory_slot", ek_food + 1, ":capacity"),
     (troop_inventory_slot_get_item_amount, reg0, "trp_dplmc_chamberlain", ":inventory_slot"),
     (gt, reg0, 0),
     (troop_get_inventory_slot, reg0, "trp_dplmc_chamberlain", ":inventory_slot"),
     (neg|troop_has_item_equipped, "trp_dplmc_chamberlain", reg0),
     (assign, ":can_use_secondary_storage", 1),
     (assign, ":capacity", ":inventory_slot"),#stop the loop
   (try_end),
   (eq, ":can_use_secondary_storage", 1),
(else_try),
   #If the player owns any towns or castles, allow use of the former item pool
   #as secondary storage.
   (try_for_range, reg0, walled_centers_begin, walled_centers_end),
      (party_slot_eq, reg0, slot_town_lord, "trp_player"),
	  (assign, ":can_use_secondary_storage", 1),
   (try_end),
(try_end),
(eq, ":can_use_secondary_storage", 1),
],
#"I would like to manage the item pool.", "dplmc_chamberlain_pretalk",
"I would like to manage the goods in secondary storage.", "dplmc_chamberlain_pretalk",
[(change_screen_loot, "trp_dplmc_chamberlain"),]],
[anyone|plyr, "dplmc_chamberlain_pools",
[
##diplomacy start+
(eq, 0, 1),#This is no longer used as the primary autoloot pool!
##diplomacy end+
   (eq, "$g_autoloot", 1),
(store_skill_level, ":inv_skill", "skl_inventory_management", "trp_player"),
(gt, "$g_player_chamberlain", 0),
(ge, ":inv_skill", 3),
],
"Let my companions take the items out of the item pool.", "dplmc_chamberlain_item_pool",
[]],
[anyone, "dplmc_chamberlain_item_pool",
[
],
"Are you sure you wish to do this?", "dplmc_chamberlain_item_pool_confirm",
[]],
[anyone|plyr, "dplmc_chamberlain_item_pool_confirm",
[
##diplomacy start+
(eq, 0, 1),#This is no longer used as the primary autoloot pool!
##diplomacy end+
],
"Yes.", "dplmc_chamberlain_pretalk",
[
(call_script, "script_dplmc_auto_loot_all"),
]],
[anyone|plyr, "dplmc_chamberlain_item_pool_confirm",
[
],
"No I changed, my mind.", "dplmc_chamberlain_pretalk",
[
]],
[anyone|plyr, "dplmc_chamberlain_pools",
[
],
"I would like to manage the household.", "dplmc_chamberlain_pretalk",
[(change_screen_loot, "trp_household_possessions"),]],
[anyone|plyr, "dplmc_chamberlain_pools",
[],
"Nevermind.", "dplmc_chamberlain_pretalk",
[]],
[anyone|plyr, "dplmc_chamberlain_talk",
[
],
"You are dismissed.", "dplmc_chamberlain_dismiss_confirm_ask",
[]],
[anyone, "dplmc_chamberlain_dismiss_confirm_ask",
[
],
"Are you sure that you want to handle all financial affairs by yourself?", "dplmc_chamberlain_dismiss_confirm",
[]],
[anyone|plyr, "dplmc_chamberlain_dismiss_confirm",
[
],
"Yes I am.", "dplmc_chamberlain_dismiss_confirm_yes",
[]],
[anyone|plyr, "dplmc_chamberlain_dismiss_confirm",
[
],
"No I am not.", "dplmc_chamberlain_pretalk",
[]],
[anyone, "dplmc_chamberlain_dismiss_confirm_yes",
[
],
"As you wish. Let's go through the documents and hand over your estate.", "close_window",
[
(assign, "$g_player_chamberlain", -1),
(store_troop_gold, ":treasury", "trp_household_possessions"),
(call_script, "script_dplmc_withdraw_from_treasury",  ":treasury"),
(troop_add_gold, "trp_player", ":treasury"),
]],
[anyone|plyr,"dplmc_chamberlain_talk",
[],
"Oh nothing, I just wanted to check the documents.", "close_window",[
]],
[anyone, "dplmc_spouse_staff_talk_ask",
[
],
##diplomacy start+ rephrase
#"Which staff member do you like to hire?", "dplmc_talk_staff",
"What sort of staff member would you like to hire?", "dplmc_talk_staff",
##diplomacy end+
[]],
[anyone|plyr, "dplmc_talk_staff",
[
(le, "$g_player_constable", 0),
(assign, ":has_fief", 0),
(try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
(party_get_slot,  ":lord_troop_id", ":center_no", slot_town_lord),
(eq, ":lord_troop_id", "trp_player"),
(assign, ":has_fief", 1),
(try_end),
##diplomacy start+ remove superfluous
#(try_begin),
##diplomacy end+
(eq, ":has_fief", 1),
],
"I want to appoint an army inspector.", "dplmc_talk_appoint_constable",
[]],
[anyone, "dplmc_talk_appoint_constable",
[(troop_slot_ge, "trp_dplmc_constable", slot_troop_met, 1),
],
"I assume you will want to rehire your former army inspector Terumoto?  His rate is still 15 mon each week, and the appointment will cost us 20 mon.", "dplmc_talk_appoint_constable_confirm", []],
[anyone, "dplmc_talk_appoint_constable", [
	#gekokujo 3.0 microfactions! include fort companions start
    #(is_between, "$g_talk_troop", companions_begin, companions_end),
    (is_between, "$g_talk_troop", companions_begin, fort_companions_end),
	#gekokujo 3.0 microfactions! include fort companions end
  ], "I have heard good things about a local samurai by the name of Terumoto, and I believe he would be well-suited for the job. He demands 15 mon each week, though. The appointment will cost us 20 mon.", "dplmc_talk_appoint_constable_confirm", []],
[anyone, "dplmc_talk_appoint_constable",
[
],
"That's a wise idea. May I suggest a very capable samurai and friend of my family? His name is Terumoto. He demands 15 mon each week, though. The appointment will cost us 20 mon.", "dplmc_talk_appoint_constable_confirm",
[]],
[anyone|plyr, "dplmc_talk_appoint_constable_confirm",
[
(store_troop_gold, ":gold", "trp_player"),
(ge, ":gold", 20),
],
"So be it.", "dplmc_talk_appoint_confirm_yes",
[
(call_script, "script_dplmc_appoint_constable"),
(troop_remove_gold, "trp_player", 20),
]],
[anyone|plyr, "dplmc_talk_appoint_constable_confirm",
[
(troop_get_slot, ":player_spouse", "trp_player", slot_troop_spouse),
##diplomacy start+ Handle non-reflexive spouse slots (for example, for polygamy)
(this_or_next|troop_slot_eq, "$g_talk_troop", slot_troop_spouse, "trp_player"),
	(eq, "$g_talk_troop", ":player_spouse"),
(this_or_next|is_between, "$g_talk_troop", heroes_begin, heroes_end),#slot_troop_spouse may not be initialized to -1
 ##diplomacy end+
(eq, "$g_talk_troop", ":player_spouse"),
],
"Maybe later.", "spouse_pretalk",
[]],
[anyone|plyr, "dplmc_talk_appoint_constable_confirm",
[
(eq, "$g_talk_troop", "$g_player_minister"),
(troop_get_slot, ":player_spouse", "trp_player", slot_troop_spouse),
##diplomacy start+ Handle non-reflexive spouse slots (for example, for polygamy)
(this_or_next|neg|is_between, "$g_talk_troop", heroes_begin, heroes_end),#slot_troop_spouse may not be initialized to -1
   (neg|troop_slot_eq, "$g_talk_troop", slot_troop_spouse, "trp_player"),
##diplomacy end+
(neq, ":player_spouse", "$g_player_minister"),
],
"Maybe later.", "minister_pretalk",
[]],
[anyone, "dplmc_talk_appoint_confirm_yes",
[
(troop_get_slot, ":player_spouse", "trp_player", slot_troop_spouse),
##diplomacy start+ Handle non-reflexive spouse slots (for example, for polygamy)
(this_or_next|troop_slot_eq, "$g_talk_troop", slot_troop_spouse, "trp_player"),
	(eq, "$g_talk_troop", ":player_spouse"),
(this_or_next|is_between, "$g_talk_troop", heroes_begin, heroes_end),#slot_troop_spouse may not be initialized to -1
 ##diplomacy end+
(eq, "$g_talk_troop", ":player_spouse"),
],
"I will send him a letter he should arrive at the palace soon.", "spouse_pretalk",
[]],
[anyone, "dplmc_talk_appoint_confirm_yes",
[
(eq, "$g_talk_troop", "$g_player_minister"),
],
"I will send him a letter he should arrive at the palace soon.", "minister_pretalk",
[]],
[anyone|plyr, "dplmc_talk_staff",
[
(le, "$g_player_chamberlain", 0),
(assign, ":has_fief", 0),
(try_for_range, ":center_no", centers_begin, centers_end),
(party_get_slot,  ":lord_troop_id", ":center_no", slot_town_lord),
(eq, ":lord_troop_id", "trp_player"),
(assign, ":has_fief", 1),
(try_end),
##diplomacy start+ remove superfluous
#(try_begin),
##diplomacy end+
(eq, ":has_fief", 1),
],
"I want to appoint a treasurer to handle financial affairs.", "dplmc_talk_appoint_chamberlain",
[]],
[anyone, "dplmc_talk_appoint_chamberlain",
[(troop_slot_ge, "trp_dplmc_chamberlain", slot_troop_met, 1),
],
"I assume you will want to rehire your former treasurer Rikyu?  His rate is still 15 mon each week, and the appointment will cost us 20 mon.", "dplmc_talk_appoint_chamberlain_confirm", []],
[anyone, "dplmc_talk_appoint_chamberlain", [
	#gekokujo 3.0 microfactions! include fort companions start
    #(is_between, "$g_talk_troop", companions_begin, companions_end),
    (is_between, "$g_talk_troop", companions_begin, fort_companions_end),
	#gekokujo 3.0 microfactions! include fort companions end
  ], "I have heard good things about a local nobleman by the name of Rikyu, and I believe he would be well-suited for the job. He demands 15 mon each week, though. The appointment will cost us 20 mon.", "dplmc_talk_appoint_chamberlain_confirm", []],
[anyone, "dplmc_talk_appoint_chamberlain",
[
],
"That's a wise idea. May I suggest a very capable nobleman and friend of my family? His name is Rikyu. He demands 15 mon each week, though. The appointment will cost us 20 mon.", "dplmc_talk_appoint_chamberlain_confirm",
[]],
[anyone|plyr, "dplmc_talk_appoint_chamberlain_confirm",
[
(store_troop_gold, ":gold", "trp_player"),
(ge, ":gold", 20),
],
"So be it.", "dplmc_talk_appoint_confirm_yes",
[
  (call_script, "script_dplmc_appoint_chamberlain"),
  (troop_remove_gold, "trp_player", 20),
]],
[anyone|plyr, "dplmc_talk_appoint_chamberlain_confirm",
[
(troop_get_slot, ":player_spouse", "trp_player", slot_troop_spouse),
##diplomacy start+
(this_or_next|troop_slot_eq, "$g_talk_troop", slot_troop_spouse, "trp_player"),
	(troop_slot_eq, "trp_player", slot_troop_spouse, "$g_talk_troop"),
(this_or_next|is_between, "$g_talk_troop", heroes_begin, heroes_end),
##diplomacy end+
(eq, "$g_talk_troop", ":player_spouse"),
],
"Maybe later.", "spouse_pretalk",
[]],
[anyone|plyr, "dplmc_talk_appoint_chamberlain_confirm",
[
(eq, "$g_talk_troop", "$g_player_minister"),
(troop_get_slot, ":player_spouse", "trp_player", slot_troop_spouse),
##diplomacy start+
(this_or_next|neg|troop_slot_eq, "$g_talk_troop", slot_troop_spouse, "trp_player"),
	(neg|is_between, "$g_talk_troop", heroes_begin, heroes_end),
##diplomacy end+
(neq, ":player_spouse", "$g_player_minister"),
],
"Maybe later.", "minister_pretalk",
[]],
[anyone|plyr, "dplmc_talk_staff",
[
(le, "$g_player_chancellor", 0),
(assign, ":has_fief", 0),
(try_for_range, ":center_no", towns_begin, towns_end),
(party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
(assign, ":has_fief", 1),
(try_end),
(eq, ":has_fief", 1),
],
"I want to appoint an administrator.", "dplmc_talk_appoint_chancellor",
[]],
[anyone, "dplmc_talk_appoint_chancellor",
[(troop_slot_ge, "trp_dplmc_chamberlain", slot_troop_met, 1),
],
"I assume you will want to rehire your former administrator Mitsunari?  His rate is still 20 mon each week, and the appointment will cost us 20 mon.", "dplmc_talk_appoint_chancellor_confirm", []],
[anyone, "dplmc_talk_appoint_chancellor", [
    #gekokujo 3.0 microfactions! include fort companions start
    #(is_between, "$g_talk_troop", companions_begin, companions_end),
    (is_between, "$g_talk_troop", companions_begin, fort_companions_end),
	#gekokujo 3.0 microfactions! include fort companions end
  ], "I have heard good things about a local samurai by the name of Mitsunari, and I believe he would be well-suited for the job. He demands 20 mon each week, though. The appointment will cost us 20 mon.", "dplmc_talk_appoint_chancellor_confirm", []],
[anyone, "dplmc_talk_appoint_chancellor",
[
],
"That's a wise idea. May I suggest a very capable samurai and friend of my family? His name is Mitsunari. He demands 20 mon each week, though. The appointment will cost us 20 mon.", "dplmc_talk_appoint_chancellor_confirm",
[]],
[anyone|plyr, "dplmc_talk_appoint_chancellor_confirm",
[
(store_troop_gold, ":gold", "trp_player"),
(ge, ":gold", 20),
],
"So be it.", "dplmc_talk_appoint_confirm_yes",
[
  (call_script, "script_dplmc_appoint_chancellor"),
  (troop_remove_gold, "trp_player", 20),
]],
[anyone|plyr, "dplmc_talk_appoint_chancellor_confirm",
[
(troop_get_slot, ":player_spouse", "trp_player", slot_troop_spouse),
(eq, "$g_talk_troop", ":player_spouse"),
],
"Maybe later.", "spouse_pretalk",
[]],
[anyone|plyr, "dplmc_talk_appoint_chancellor_confirm",
[
(eq, "$g_talk_troop", "$g_player_minister"),
(troop_get_slot, ":player_spouse", "trp_player", slot_troop_spouse),
(neq, ":player_spouse", "$g_player_minister"),
],
"Maybe later.", "minister_pretalk",
[]],
[anyone|plyr, "dplmc_talk_staff",
[
(eq, "$g_talk_troop", "$g_player_minister"),
],
"None.", "minister_pretalk",
[]],
[anyone|plyr, "dplmc_talk_staff",
[
(troop_get_slot, ":player_spouse", "trp_player", slot_troop_spouse),
(eq, "$g_talk_troop", ":player_spouse"),
(neq, ":player_spouse", "$g_player_minister"),
],
"None.", "spouse_pretalk",
[]],
[anyone, "dplmc_spouse_talk_buy_food_amount_ask",
[
],
##diplomacy start+ "like" to "want"
"How much bread do you want?", "dplmc_spouse_talk_buy_food_amount",
##diplomacy end+
[]],
[anyone|plyr, "dplmc_spouse_talk_buy_food_amount",
[
],
"{!}50.", "dplmc_spouse_talk_buy_food",
[
(troop_get_slot, ":player_spouse", "trp_player", slot_troop_spouse),
(troop_set_slot, ":player_spouse", dplmc_slot_troop_mission_diplomacy, 1),
]],
[anyone|plyr, "dplmc_spouse_talk_buy_food_amount",
[
],
"{!}100.", "dplmc_spouse_talk_buy_food",
[
(troop_get_slot, ":player_spouse", "trp_player", slot_troop_spouse),
(troop_set_slot, ":player_spouse", dplmc_slot_troop_mission_diplomacy, 2),
]],
[anyone|plyr, "dplmc_spouse_talk_buy_food_amount",
[
],
"{!}150.", "dplmc_spouse_talk_buy_food",
[
(troop_get_slot, ":player_spouse", "trp_player", slot_troop_spouse),
(troop_set_slot, ":player_spouse", dplmc_slot_troop_mission_diplomacy, 3),
]],
[anyone|plyr, "dplmc_spouse_talk_buy_food_amount",
[
],
"{!}200.", "dplmc_spouse_talk_buy_food",
[
(troop_get_slot, ":player_spouse", "trp_player", slot_troop_spouse),
(troop_set_slot, ":player_spouse", dplmc_slot_troop_mission_diplomacy, 4),
]],
[anyone|plyr, "dplmc_spouse_talk_buy_food_amount",
[
],
"Nothing.", "spouse_pretalk",
[]],
[anyone, "dplmc_spouse_talk_buy_food",
[
(troop_get_slot, ":player_spouse", "trp_player", slot_troop_spouse),
(troop_slot_eq, ":player_spouse", slot_troop_cur_center, "$current_town"),
(troop_get_slot, ":amount", ":player_spouse", dplmc_slot_troop_mission_diplomacy),

(assign, ":can_leave", 1),
(try_begin),
(is_between,"$current_town",castles_begin, castles_end),
(try_begin),
 (is_between, "$current_town", walled_centers_begin, walled_centers_end),
 (neg|party_slot_eq, "$current_town", slot_center_is_besieged_by, -1),
 (assign, ":can_leave", 0),
(try_end),
(try_end),
(eq, ":can_leave", 1),

(assign, ":mission_object", -1),
(try_begin),
(store_faction_of_party, ":party_faction", "$current_town"),
(assign, ":distance", 1000),
(try_for_range, ":center_no", centers_begin, centers_end),
  (neg|is_between, ":center_no", castles_begin, castles_end),
  (store_faction_of_party, ":center_faction", ":center_no"),
  (eq, ":center_faction", ":party_faction"),

  (assign, ":proceed", 1),
  (try_begin),
    (is_between, ":center_no", towns_begin, towns_end),
    (party_get_slot,":cur_merchant",":center_no",slot_town_merchant),
  (else_try),
    (is_between, ":center_no", villages_begin, villages_end),
    (party_get_slot,":cur_merchant",":center_no", slot_town_elder),
    (neg|party_slot_eq, ":center_no", slot_village_state, svs_normal),
    (assign, ":proceed", 0),
  (try_end),
  (eq, ":proceed", 1),


  (troop_get_inventory_capacity, ":capacity", ":cur_merchant"),
  (assign, ":bread_amount", 0),
  (try_for_range, ":inventory_slot", 0, ":capacity"),
     (troop_get_inventory_slot, ":item", ":cur_merchant", ":inventory_slot"),
     (eq, ":item", "itm_bread"),
     (val_add, ":bread_amount", 1),
   (try_end),
   (ge, ":bread_amount", ":amount"),

  (store_distance_to_party_from_party, ":tmp_distance", ":center_no", "$current_town"),
  (lt, ":tmp_distance", ":distance"),
  (assign, ":distance", ":tmp_distance"),

  (assign, ":mission_object", ":center_no"),
(try_end),
(try_end),

(neq, ":mission_object", -1),
(troop_set_slot, ":player_spouse", slot_troop_mission_object, ":mission_object"),

##nested diplomacy start+
#(call_script, "script_dplmc_get_item_buy_price_factor", "itm_bread", ":mission_object"),
#Use player skill for now (we could revisit this, but it's not important)
(call_script, "script_dplmc_get_item_buy_price_factor", "itm_bread", ":mission_object", "trp_player", -1),
##nested diplomacy end+
(store_item_value, ":value", "itm_bread"),
(store_mul, ":price", ":value", reg0),
(val_div, ":price", 100),
(val_max, ":price", 1),
(val_mul, ":price", ":amount"),
(assign, reg0, ":price"),
(str_store_party_name, s6, ":mission_object"),
],
"Yes of course, I will go to the merchant in {s6} and buy some bread. This will cost us {reg0} mon.", "dplmc_spouse_talk_buy_food_confirm",
[]],
[anyone, "dplmc_spouse_talk_buy_food",
[
],
"Currently no merchant has enough bread. We have to wait.", "spouse_pretalk",
[]],
[anyone|plyr, "dplmc_spouse_talk_buy_food_confirm",
[
(store_troop_gold, ":gold", "trp_player"),
(ge, ":gold", reg0),
],
"Ok, we can afford that, please go. Thank you.", "close_window",
[
(troop_get_slot, ":player_spouse", "trp_player", slot_troop_spouse),
(troop_get_slot, ":mission_object", ":player_spouse", slot_troop_mission_object),
(troop_remove_gold, "trp_player", reg0),
(try_begin),
(neq, ":mission_object", "$current_town"),

(try_begin),
  (troop_get_slot, ":player_spouse", "trp_player", slot_troop_spouse),

  (set_spawn_radius, 1),
  (spawn_around_party, "$g_encountered_party", "pt_dplmc_spouse"),
  (assign, ":spouse_party", reg0),

  (party_add_members, ":spouse_party", ":player_spouse", 1),
  (party_set_faction, ":spouse_party", "fac_neutral"), #no capture
  (party_set_slot, ":spouse_party", slot_party_home_center, "$g_encountered_party"),
  (party_set_slot, ":spouse_party", slot_party_type, dplmc_spt_spouse),
  (party_set_slot, ":spouse_party", slot_party_orders_object, ":mission_object"),
  (party_set_ai_object, ":spouse_party", ":mission_object"),
  (party_set_ai_behavior, ":spouse_party", ai_bhvr_travel_to_party),
  (party_set_slot, ":spouse_party", slot_party_ai_state, spai_undefined),
  (troop_set_slot, ":player_spouse", slot_troop_cur_center, -1),
(try_end),
(else_try),
(party_get_slot,":cur_merchant",":mission_object",slot_town_merchant),
(troop_remove_items, ":cur_merchant", "itm_bread", 2),
(troop_add_items, "trp_household_possessions", "itm_bread", 2),
(try_end),
]],
[anyone|plyr, "dplmc_spouse_talk_buy_food_confirm",
[
],
"Oh, maybe later.", "close_window",
[
]],
[anyone, "dplmc_minister_staff_talk_ask",
[
],
##diplomacy start+ rephrase
#"Which staff member do you like to hire?", "dplmc_talk_staff",
"What sort of staff member would you like to hire?", "dplmc_talk_staff",
##diplomacy end+
[]],
[anyone, "dplmc_lord_give_back_fief",
[
], "Oh, so you can't manage it? Well, which fief do you have in mind?", "dplmc_lord_give_back_fief_select",
[]],
[anyone|plyr|repeat_for_parties,"dplmc_lord_give_back_fief_select", [
(store_repeat_object, ":center"),
(is_between, ":center", centers_begin, centers_end),
(neq, ":center", "$g_player_court"), #court can't be returned
(party_slot_eq, ":center", slot_center_is_besieged_by, -1),
(party_slot_eq, ":center", slot_town_lord, "trp_player"),
(str_store_party_name, s11, ":center"),
],
"{!}{s11}.", "dplmc_lord_give_back_fief_confirm_ask",[
(store_repeat_object, "$diplomacy_var"),
]],
[anyone|plyr,"dplmc_lord_give_back_fief_select", [],
"Never mind.", "lord_pretalk",[
]],
[anyone, "dplmc_lord_give_back_fief_confirm_ask",
[
(str_store_party_name, s11, "$diplomacy_var"),
], "So you think you can't fulfill your promise and manage {s11}?", "dplmc_lord_give_back_fief_confirm",
[]],
[anyone|plyr, "dplmc_lord_give_back_fief_confirm",
[
(str_store_party_name, s11, "$diplomacy_var"),
], "Yes I want to give up on {s11}.", "lord_pretalk",
[
(call_script, "script_change_player_honor", -1),
(call_script, "script_change_player_relation_with_troop", "$g_talk_troop", -3),
(troop_get_slot, ":player_renown", "trp_player", slot_troop_renown),
(val_sub, ":player_renown", 5),
(val_max, ":player_renown", 0),
(troop_set_slot, "trp_player", slot_troop_renown, ":player_renown"),
(call_script, "script_give_center_to_faction", "$diplomacy_var", "fac_neutral"),
(call_script, "script_give_center_to_faction", "$diplomacy_var", "$players_kingdom"),
]],
[anyone|plyr, "dplmc_lord_give_back_fief_confirm",
[
(str_store_party_name, s11, "$diplomacy_var"),
], "No, I will keep the promise.", "lord_pretalk",
[]],
[anyone, "dplmc_lord_declare_war",
[
(troop_get_slot, ":renown", "trp_player", slot_troop_renown), #reown
(lt, ":renown", 150),
(troop_get_slot, ":relation_to_king", "$g_talk_troop", slot_troop_player_relation),
(lt, ":relation_to_king", 5),
(val_sub, ":relation_to_king", 5),
(assign, ":sum", ":renown"),
(val_mul, ":relation_to_king", 5),
(val_add, ":sum", ":relation_to_king"),
(val_add, ":sum", "$player_honor"),

(try_begin), #debug
(eq, "$cheat_mode", 1),
(assign, reg0, ":sum"),
(display_message, "@{!}DEBUG : sum: {reg0}"),
(try_end),

(lt, ":sum", 300),
], "How can you dare? Who do you think you are? Get out of my sight!", "close_window",
[
(call_script, "script_change_player_relation_with_troop", "$g_talk_troop", -1),
(eq,"$talk_context",tc_party_encounter), #Added line by zerilius
(assign, "$g_leave_encounter", 1), #Added line by zerilius
]],
[anyone, "dplmc_lord_declare_war",
[], "Against whom?", "dplmc_lord_declare_war_kingdoms_select",
[]],
[anyone|plyr|repeat_for_factions, "dplmc_lord_declare_war_kingdoms_select",
[
(store_repeat_object, ":faction_no"),
(is_between, ":faction_no", kingdoms_begin, kingdoms_end),
##diplomacy start+
(neq, ":faction_no", "fac_player_supporters_faction"),
(neq, ":faction_no", "$g_talk_troop_faction"),
##diplomacy end+
(neq, ":faction_no", "$players_kingdom"),
(call_script, "script_diplomacy_faction_get_diplomatic_status_with_faction", "$players_kingdom", ":faction_no"),
(ge, reg0, -1),
(faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
(faction_get_slot, ":leader_no", ":faction_no", slot_faction_leader),
(str_store_troop_name, s10, ":leader_no"),
(str_store_faction_name, s11, ":faction_no"),
],
"{s11}", "dplmc_lord_declare_war_ask_why",
[
(store_repeat_object, "$g_faction_selected"),
(call_script, "script_npc_decision_checklist_peace_or_war", "$players_kingdom", "$g_faction_selected", "trp_player"),
(assign, "$diplomacy_var", reg0),
(val_mul, "$diplomacy_var", -6),
(val_min, "$diplomacy_var", 2),

(try_for_range, ":kingdom", kingdoms_begin, kingdoms_end),
(neq, ":kingdom", "$players_kingdom"),
(neq, ":kingdom", "$g_faction_selected"),
(call_script, "script_diplomacy_faction_get_diplomatic_status_with_faction",  "$players_kingdom", ":kingdom"),
(eq, reg0, -2),
(val_sub, "$diplomacy_var", 4),
(try_end),

(store_skill_level, ":player_persuasion_skill", "skl_persuasion", "trp_player"),
(val_add, "$diplomacy_var", ":player_persuasion_skill"),

(assign, reg50, 0),
(assign, reg51, 0),
(assign, reg52, 0),
(assign, reg53, 0),

(try_begin), #debug
(eq, "$cheat_mode", 1),
(assign, reg0, "$diplomacy_var"),
(display_message, "@{!}DEBUG : diplomacy_var: {reg0}"),
(try_end),
]],
[anyone|plyr, "dplmc_lord_declare_war_kingdoms_select",
[], "Never mind", "lord_pretalk",
[]],
[anyone, "dplmc_lord_declare_war_ask_why",
[
(str_store_faction_name, s11, "$g_faction_selected"),
##nested diplomacy start+ Fix capitalization
], "Why should I declare war against the {s11}?", "dplmc_lord_declare_war_why",
##nested diplomacy end+
[]],
[anyone|plyr, "dplmc_lord_declare_war_why",
[
(eq, reg50, 0),
], "They are weaker and we can easily beat them.", "dplmc_lord_declare_war_anything_else",
[
(assign, reg50, 1),
(assign, ":persuasion", -1),
(assign, ":player_kingdom_str", 0),
(assign, ":target_kingdom_str", 0),

(try_for_parties, ":party_no"),
(assign, ":party_value", 0),
(try_begin),
   (is_between, ":party_no", towns_begin, towns_end),
   (assign, ":party_value", 3),
(else_try),
   (is_between, ":party_no", castles_begin, castles_end),
   (assign, ":party_value", 2),
(else_try),
   (is_between, ":party_no", villages_begin, villages_end),
   (assign, ":party_value", 1),
(else_try),
   (party_get_template_id, ":template", ":party_no"),
   (eq, ":template", "pt_kingdom_hero_party"),
   (assign, ":party_value", 2),
(try_end),

(store_faction_of_party, ":party_current_faction", ":party_no"),
(try_begin),
  (eq, ":party_current_faction", "$players_kingdom"),
  (val_add, ":player_kingdom_str", ":party_value"),
(else_try),
  (eq, ":party_current_faction", "$g_faction_selected"),
  (val_add, ":target_kingdom_str", ":party_value"),
(try_end),
(try_end),

(try_begin),
(gt, ":player_kingdom_str", ":target_kingdom_str"),
(assign, ":persuasion", 1),
(try_end),

(store_skill_level, ":player_persuasion_skill", "skl_persuasion", "trp_player"),
(val_mul, ":player_persuasion_skill", ":persuasion"),
(val_add, ":persuasion", ":player_persuasion_skill"),
(val_add, "$diplomacy_var", ":persuasion"),

(try_begin), #debug
(eq, "$cheat_mode", 1),
(assign, reg0, ":persuasion"),
(display_message, "@{!}DEBUG : persuasion: {reg0}"),
(assign, reg0, "$diplomacy_var"),
(display_message, "@{!}DEBUG : diplomacy_var: {reg0}"),
(try_end),
]],
[anyone|plyr, "dplmc_lord_declare_war_why",
[
(eq, reg51, 0),
], "We can't tolerate their provocations any longer.", "dplmc_lord_declare_war_anything_else",
[
(assign, reg51, 1),
(assign, ":persuasion", -1),
(call_script, "script_diplomacy_faction_get_diplomatic_status_with_faction", "$players_kingdom", "$g_faction_selected"),
(assign, ":war_peace_truce_status", reg0),

(try_begin),
(eq, ":war_peace_truce_status", -1),
(assign, ":persuasion", 1),
(try_end),
(store_skill_level, ":player_persuasion_skill", "skl_persuasion", "trp_player"),
(val_mul, ":player_persuasion_skill", ":persuasion"),
(val_add, ":persuasion", ":player_persuasion_skill"),
(val_add, "$diplomacy_var", ":persuasion"),

(try_begin), #debug
(eq, "$cheat_mode", 1),
(assign, reg0, ":persuasion"),
(display_message, "@{!}DEBUG : persuasion: {reg0}"),
(assign, reg0, "$diplomacy_var"),
(display_message, "@{!}DEBUG : diplomacy_var: {reg0}"),
(try_end),
]],
[anyone|plyr, "dplmc_lord_declare_war_why",
[
(eq, reg52, 0),
], "They are already in war and currently distracted.", "dplmc_lord_declare_war_anything_else",
[
(assign, reg52, 1),
(assign, ":persuasion", -1),
(try_for_range, ":kingdom", kingdoms_begin, kingdoms_end),
(neq, ":kingdom", "$players_kingdom"),
(neq, ":kingdom", "$g_faction_selected"),
(call_script, "script_diplomacy_faction_get_diplomatic_status_with_faction",  "$g_faction_selected", ":kingdom"),
(eq, reg0, -2),
(assign, ":persuasion", 1),
(try_end),
(store_skill_level, ":player_persuasion_skill", "skl_persuasion", "trp_player"),
(val_mul, ":player_persuasion_skill", ":persuasion"),
(val_add, ":persuasion", ":player_persuasion_skill"),
(val_add, "$diplomacy_var", ":persuasion"),

(try_begin), #debug
(eq, "$cheat_mode", 1),
(assign, reg0, ":persuasion"),
(display_message, "@{!}DEBUG : persuasion: {reg0}"),
(assign, reg0, "$diplomacy_var"),
(display_message, "@{!}DEBUG : diplomacy_var: {reg0}"),
(try_end),
]],
[anyone|plyr, "dplmc_lord_declare_war_why",
[
(eq, reg53, 0),
], "It's the right time to attack.", "dplmc_lord_declare_war_anything_else",
[
(assign, reg53, 1),
(assign, ":persuasion", 1),
(try_for_range, ":kingdom", kingdoms_begin, kingdoms_end),
(neq, ":kingdom", "$g_faction_selected"),
(call_script, "script_diplomacy_faction_get_diplomatic_status_with_faction",  "$players_kingdom", ":kingdom"),
(eq, reg0, -2),
(assign, ":persuasion", -1),
(try_end),
(store_skill_level, ":player_persuasion_skill", "skl_persuasion", "trp_player"),
(val_mul, ":player_persuasion_skill", ":persuasion"),
(val_add, ":persuasion", ":player_persuasion_skill"),
(val_add, "$diplomacy_var", ":persuasion"),

(try_begin), #debug
(eq, "$cheat_mode", 1),
(assign, reg0, ":persuasion"),
(display_message, "@{!}DEBUG : persuasion: {reg0}"),
(assign, reg0, "$diplomacy_var"),
(display_message, "@{!}DEBUG : diplomacy_var: {reg0}"),
(try_end),
]],
[anyone|plyr, "dplmc_lord_declare_war_why",
[
(eq, reg54, 0),
], "We should get back our lost land.", "dplmc_lord_declare_war_anything_else",
[
(assign, reg54, 1),
(assign, ":persuasion", -1),
(try_for_parties, ":party_no"),
(store_faction_of_party, ":party_current_faction", ":party_no"),
(party_get_slot, ":party_original_faction", ":party_no", slot_center_original_faction),
(party_get_slot, ":party_ex_faction", ":party_no", slot_center_ex_faction),
   (eq, ":party_current_faction", "$g_faction_selected"),
   (this_or_next|eq, ":party_original_faction", "$players_kingdom"),
  (eq, ":party_ex_faction", "$players_kingdom"),
  (assign, ":persuasion", 1),
(try_end),
(store_skill_level, ":player_persuasion_skill", "skl_persuasion", "trp_player"),
(val_mul, ":player_persuasion_skill", ":persuasion"),
(val_add, ":persuasion", ":player_persuasion_skill"),
(val_add, "$diplomacy_var", ":persuasion"),

(try_begin), #debug
(eq, "$cheat_mode", 1),
(assign, reg0, ":persuasion"),
(display_message, "@{!}DEBUG : persuasion: {reg0}"),
(assign, reg0, "$diplomacy_var"),
(display_message, "@{!}DEBUG : diplomacy_var: {reg0}"),
(try_end),
]],
[anyone|plyr, "dplmc_lord_declare_war_why",
[
], "I mentioned all reasons for war. Please think about it!", "dplmc_lord_declare_war_decision",
[]],
[anyone|plyr, "dplmc_lord_declare_war_why",
[], "I need to think about that in peace and quiet.", "lord_pretalk",
[]],
[anyone, "dplmc_lord_declare_war_anything_else",
[
], "Well, anything else?", "dplmc_lord_declare_war_why",
[]],
[anyone, "dplmc_lord_declare_war_decision",
[
(troop_get_slot, ":relation_to_king", "$g_talk_troop", slot_troop_player_relation),
(val_sub, ":relation_to_king", 15),
(val_min, ":relation_to_king", 35),
(val_add, "$diplomacy_var", ":relation_to_king"),
##nested diplomacy start+
#If there is currently a treaty, apply a penalty to the persuasion attempt.
(call_script, "script_dplmc_get_faction_truce_length_with_faction", "$players_kingdom", "$g_faction_selected"),
(try_begin),
	(gt, reg0, 0),

    (try_begin),
       (eq, "$cheat_mode", 1),
       (assign, reg0, "$diplomacy_var"),
       (display_message, "@{!}DEBUG : pre-treaty diplomacy_var: {reg0}"),
    (try_end),

        ##TODO: Perhaps re-enable this later, but also balance it with the
        ##lords who would be pleased by the declaration of war.
	#(try_for_range, ":troop_no", heroes_begin, heroes_end),
	#   (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
	#   (neq, ":troop_no", "$g_talk_troop"),
	#   (store_troop_faction, ":troop_faction"),
	#   (eq, ":troop_faction", "$g_talk_troop_faction"),
	#   #Would be angered by breaking the treaty
	#   (this_or_next|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_martial),
	#   (this_or_next|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_goodnatured),
	#   (this_or_next|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_selfrighteous),
	#   (this_or_next|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_benefactor), #new for enfiefed commoners
	#   (this_or_next|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_custodian), #new for enfiefed commoners
	#      (troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_upstanding),
	#   (val_sub, "$diplomacy_var", 1),
	#(try_end),
    (try_begin),
    (gt, reg0, dplmc_treaty_alliance_days_expire),
      (val_div, "$diplomacy_var", 5),
      (val_min, "$diplomacy_var", 15),
    (else_try),
      (gt, reg0, dplmc_treaty_defense_days_expire),
      (val_div, "$diplomacy_var", 4),
      (val_min, "$diplomacy_var", 17),
    (else_try),
      (gt, reg0, dplmc_treaty_trade_days_expire),
      (val_div, "$diplomacy_var", 3),
      (val_min, "$diplomacy_var", 19),
    (else_try),
      (gt, reg0, dplmc_treaty_truce_days_expire),
      (val_div, "$diplomacy_var", 2),
      (val_min, "$diplomacy_var", 21),
    (try_end),
(try_end),
##diplomacy end+
(store_random_in_range, ":random", 5, 25),

(try_begin), #debug
(eq, "$cheat_mode", 1),
(assign, reg0, ":random"),
(display_message, "@{!}DEBUG : random: {reg0}"),
(assign, reg0, "$diplomacy_var"),
(display_message, "@{!}DEBUG : final diplomacy_var: {reg0}"),
(try_end),

(gt, "$diplomacy_var", ":random"),

##diplomacy start+
#Replace "sword" with a culturally-appropriate alternative (TODO: does "gird" make sense for everything?)
(call_script, "script_dplmc_print_cultural_word_to_sreg", "$g_talk_troop", DPLMC_CULTURAL_TERM_WEAPON, 0),
], "Gird your {s0} we are going to war against {s11}.", "close_window",
##nested diplomacy end+
[
(call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 1),
(call_script, "script_diplomacy_start_war_between_kingdoms", "$players_kingdom", "$g_faction_selected", 1),
(eq,"$talk_context",tc_party_encounter), #Added line by zerilius
(assign, "$g_leave_encounter", 1), #Added line by zerilius
]],
[anyone, "dplmc_lord_declare_war_decision",
[
], "No, I am not convinced. We won't attack {s11}.", "close_window",
[
(call_script, "script_change_player_relation_with_troop", "$g_talk_troop", -1),
(eq,"$talk_context",tc_party_encounter), #Added line by zerilius
(assign, "$g_leave_encounter", 1), #Added line by zerilius
]],
[anyone,"dplmc_lord_family_affiliate_end", [],
"What did you say?.", "script_dplmc_affiliate_confirm",[
]],
[anyone,"dplmc_lord_family_affiliate_leave", [],
"You dare stand and face me to declaim your disavowal ! Well, your betrayal cannot make up for frankness. You disappoint the confidence my clan have put in you, {playername}. Each will condemn you in all conscience... but since I avouched your phoney allegiance, I will personally report to samurai about your frivolous plot.", "close_window",[
(call_script, "script_dplmc_affiliate_end", 0),
]],
[anyone, "dplmc_lord_family_affiliate",
[
(str_clear, s10),
(assign, ":approved", 0),
(troop_get_slot, ":lord_renown", "$g_talk_troop", slot_troop_renown),
(try_begin),
(troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_martial),
(troop_get_slot, ":player_renown", "trp_player", slot_troop_renown),
(try_begin),
  (ge, ":player_renown", ":lord_renown"),
  (str_store_string, s10, "@You have shown great strength on the battlefield. But why should I enlist you within us?"),
  (assign, ":approved", 1),
(try_end),

(else_try),
##diplomacy start+ Add support for additional types
(this_or_next|troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_ambitious),
##diplomacy end+
(troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_cunning),
(assign, ":has_center", 0),
(try_for_range, ":center_no", centers_begin, centers_end),
  (this_or_next|party_slot_eq, ":center_no", slot_party_type, spt_town),
  (party_slot_eq, ":center_no", slot_party_type, spt_castle),
  (party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
  (assign, ":has_center", 1),
(try_end),
(try_begin),
  (eq, ":has_center", 1),
  (str_store_string, s10, "@All of life is about pros and cons. Why would we allow you to be our fellow?"),
  (assign, ":approved", 1),
(try_end),
(else_try),
(troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_debauched),
(try_begin),
  (le, "$player_honor", -10),
  (str_store_string, s10, "@I know, people do fear your harshness. Should we though?"),
  (assign, ":approved", 1),
(try_end),
(else_try),
##diplomacy start+ Add support for additional types
(this_or_next|troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_moralist),
##diplomacy end+
(troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_upstanding),
(try_begin),
  (ge, "$player_honor", 10),
  (str_store_string, s10, "@Indeed, I have heard of your loyalty and valor. But is it enough to join us?"),
  (assign, ":approved", 1),
(try_end),
(else_try),
##diplomacy start+ Add support for additional types
(this_or_next|troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_conventional),
##diplomacy end+
(troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_goodnatured),
(try_begin),
  (ge, "$g_talk_troop_faction_relation", 60),
  (str_store_string, s10, "@I'm glad you want to support us. But, would it be wise for you, to affiliate to our family?"),
  (assign, ":approved", 1),
(try_end),
(else_try),
(troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_selfrighteous),
(try_begin),
  (store_troop_gold, ":wealth", "trp_household_possessions"),
  (store_troop_gold, ":cash", "trp_player"),
  (val_add, ":wealth", ":cash"),
  (val_sub, ":wealth", "$g_player_debt_to_party_members"),

  (val_mul, ":lord_renown", 65),
  (ge, ":wealth", ":lord_renown"),

  (str_store_string, s10, "@Beside your wealth, how could you possibly serve me and my family?"),
  (assign, ":approved", 1),
(try_end),
(else_try),
(try_begin),
  (call_script, "script_troop_get_player_relation", "$g_talk_troop"),
  (gt, reg0, 18),
  ##diplomacy start+ Reworded
  #(str_store_string, s10, "@My friend, I see you reasoning. But would you really risk our friendship on partnership?"),
  (str_store_string, s10, "@My friend, I see your reasoning. But would you really risk straining our friendship by entering into a formal partnership?"),
  ##diplomacy end+
  (assign, ":approved", 1),
(try_end),
(try_end),
(eq, ":approved", 1),
],
"{!}{s10}", "dplmc_lord_family_affiliate_response",[
]],
[anyone, "dplmc_lord_family_affiliate",
[(ge, "$g_talk_troop_relation", 0),
(assign, reg0, 0),
(try_begin),
  (ge, "$g_talk_troop_relation", 18),
  (assign, reg0, 1),
(try_end),
],
"I {reg0?like you well enough:have nothing against you}, but I just don't think it would work out, so I will not sponsor you.", "lord_pretalk",[
]],
[anyone, "dplmc_lord_family_affiliate",
[
],
"Not a chance. Since I dislike you, I will not sponsor you.", "lord_pretalk",[
]],
[anyone|plyr, "dplmc_lord_family_affiliate_response",
[
],
"Please allow me to serve your family.", "dplmc_lord_family_affiliate_persuasion",[
]],
[anyone|plyr, "dplmc_lord_family_affiliate_response",
[
],
"On second thought, I have to reconsider this decision.", "lord_pretalk",[
]],
[anyone, "dplmc_lord_family_affiliate_persuasion",
[
(troop_get_slot, ":lord_renown", "$g_talk_troop", slot_troop_renown),
(store_skill_level, ":player_persuasion_skill", "skl_persuasion", "trp_player"),
(val_add, ":player_persuasion_skill", 1),

(call_script, "script_troop_get_player_relation", "$g_talk_troop"),
(assign, ":relation", 0),
(try_for_range, ":aristocrat", lords_begin, kingdom_ladies_end),
(neq, ":aristocrat", "$g_talk_troop"),
(call_script, "script_troop_get_family_relation_to_troop", ":aristocrat", "$g_talk_troop"),
(gt, reg0, 0),
(call_script, "script_troop_get_player_relation", "$g_talk_troop"),
(val_add, ":relation", reg0),
(try_end),

(ge, ":relation", 0),

(assign, ":approved", 0),
(try_for_range, ":skill_level", 0, ":player_persuasion_skill"),
(store_random_in_range, ":random_lord_renown", 0, ":lord_renown"),
(store_random_in_range, ":random_lord_relation", 0, ":relation"),
(val_add, ":random_lord_relation", ":skill_level"),

(try_begin),
  (le, ":random_lord_renown", ":random_lord_relation"),
  (assign, ":approved", 1),
(try_end),
(try_end),

(eq, ":approved", 1),

(str_clear, s10),
(try_begin),
(troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_martial),
(str_store_string, s10, "@Agreed! Your words convice me as much as your blade."),
(else_try),
(troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_cunning),
(str_store_string, s10, "@I trust you, my family could use your resourcefulness. Together we will spread our influence all over Japan."),
(else_try),
(troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_debauched),
(str_store_string, s10, "@May God have mercy on our enemy souls, because we won't!"),
(else_try),
(troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_upstanding),
(str_store_string, s10, "@So be it. We are honored to accept you into our family."),
(else_try),
(troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_goodnatured),
(str_store_string, s10, "@ I will appreciate you as much as a son."),
(else_try),
(troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_selfrighteous),
(str_store_string, s10, "@I accept your request. We will support you if you support my family."),
(else_try),
(str_store_string, s10, "@Since you have turned out to be a worthy fellow, you should be worthy for our entire family."),
(try_end),
],
"{!}{s10}", "dplmc_lord_family_affiliate_thank",[
(assign, "$g_player_affiliated_troop", "$g_talk_troop"),
(store_current_hours, ":cur_hours"),
(assign, "$g_player_affiliated_time", ":cur_hours"),

(try_for_range, ":family_member", lords_begin, kingdom_ladies_end),
(call_script, "script_dplmc_is_affiliated_family_member", ":family_member"),
(gt, reg0, 0),
(troop_set_slot, ":family_member", dplmc_slot_troop_affiliated, 1),
(try_end),
]],
[anyone, "dplmc_lord_family_affiliate_persuasion",
[],
"Maybe I have not good enough appraisal from my family about you. Or maybe I just need some time to get used to the idea. Let's talk further about it next week.", "lord_pretalk",
[
(store_current_hours, "$g_last_affiliate_attempt"),
]],
[anyone|plyr, "dplmc_lord_family_affiliate_thank",
[],
"I am honored and grateful to be affiliated with your family.", "dplmc_lord_family_affiliate_conclusion",[
]],
[anyone, "dplmc_lord_family_affiliate_conclusion",
[],
"You have pledged allegiance to our family, now all of my brethen are your brethren. Never betray your family, always protect it.", "lord_pretalk",[

(try_for_range, ":aristocrat", lords_begin, kingdom_ladies_end),
(neq, ":aristocrat", "$g_talk_troop"),
(call_script, "script_troop_get_family_relation_to_troop", ":aristocrat", "$g_talk_troop"),
(gt, reg0, 0),
(call_script, "script_change_player_relation_with_troop", ":aristocrat", 10),
(try_end),

(try_for_range, ":kingdom_hero", active_npcs_begin, active_npcs_end),
(call_script, "script_troop_get_relation_with_troop", "$g_talk_troop", ":kingdom_hero"),
(lt, reg0, -10),
(call_script, "script_change_player_relation_with_troop", ":kingdom_hero", -8),
(try_end),
]],
[anyone, "dplmc_spouse_move_residence_ask",
[
],
"To move our residence will require a small refurbishment. In particular, we need a set of tools and two piles of hemp cloth in our househould.", "dplmc_spouse_move_residence_tools",[
]],
[anyone|plyr, "dplmc_spouse_move_residence_tools",
[
(troop_get_inventory_capacity, ":capacity", "trp_household_possessions"),

(assign, ":amount", 0),
(try_for_range, ":inventory_slot", 0, ":capacity"),
  (troop_get_inventory_slot, ":item", "trp_household_possessions", ":inventory_slot"),
  (eq, ":item", "itm_wool_cloth"),
(val_add, ":amount", 1),
(try_end),
(ge, ":amount", 2),

(assign, ":amount", 0),
(try_for_range, ":inventory_slot", 0, ":capacity"),
  (troop_get_inventory_slot, ":item", "trp_household_possessions", ":inventory_slot"),
  (eq, ":item", "itm_tools"),
(val_add, ":amount", 1),
(try_end),
(ge, ":amount", 1),
],
"Ok, I think we have all necessary things to establish the residence.", "dplmc_spouse_move_residence_select_ask",[
]],
[anyone|plyr, "dplmc_spouse_move_residence_tools",
[],
"Well, I guess I have to get the set of tools and the piles of wool first.", "spouse_pretalk",[
]],
[anyone, "dplmc_spouse_move_residence_select_ask",
[],
"Where do you want to move the residence?", "dplmc_spouse_move_residence_select",[
]],
[anyone|plyr|repeat_for_parties, "dplmc_spouse_move_residence_select",
[
(store_repeat_object, ":center"),
(is_between, ":center", walled_centers_begin, walled_centers_end),
(troop_get_slot, ":cur_residence", "$g_talk_troop", slot_troop_cur_center),
(neq, ":center", ":cur_residence"),
(party_slot_eq, ":center", slot_town_lord, "trp_player"),
(str_store_party_name, s6, ":center"),
],
"{s6}.", "dplmc_spouse_move_residence_ask_confirm",[
(store_repeat_object, "$diplomacy_var"),
]],
[anyone|plyr, "dplmc_spouse_move_residence_select",
[],
"I changed my mind.", "spouse_pretalk",[
]],
[anyone, "dplmc_spouse_move_residence_ask_confirm",
[
 (str_store_party_name, s6, "$diplomacy_var"),
],
"Are you sure that you want to move your residence to {s6}?", "dplmc_spouse_move_residence_confirm",[
]],
[anyone|plyr, "dplmc_spouse_move_residence_confirm",
[],
"Yes,  please arrange everything.", "dplmc_spouse_move_residence_moved",[
(troop_remove_items, "trp_household_possessions", "itm_wool_cloth", 2),
(troop_remove_item, "trp_household_possessions", "itm_tools"),
##diplomacy start+
#Fix bug: do not set spouse's current center if spouse is active or a party member
(try_begin),
  (troop_get_slot, ":player_spouse", "trp_player", slot_troop_spouse),
(troop_slot_eq, ":player_spouse", slot_troop_occupation, slto_kingdom_lady),
##diplomacy end+
(troop_set_slot, "$g_talk_troop", slot_troop_cur_center, "$diplomacy_var"),
##diplomacy start+
(try_end),
##diplomacy end+
]],
[anyone|plyr, "dplmc_spouse_move_residence_confirm",
[],
"No.", "spouse_pretalk",[
]],
[anyone, "dplmc_spouse_move_residence_moved",
[],
"As you wish, I will move the residence to {s6}.", "spouse_pretalk",[
]],
[anyone, "dplmc_companion_threaten_request_response", [
(troop_get_slot, ":mission_object", "$g_talk_troop", slot_troop_mission_object),
(gt, "$g_player_chamberlain", 0),
(call_script, "script_diplomacy_faction_get_diplomatic_status_with_faction", "$players_kingdom", ":mission_object"),
(neq, reg0, -2), #no war
(ge, "$g_mission_result", 2), #doesn't want war with us
(store_random_in_range, ":random", 1000, 8000),

(val_div, ":random", 100),
(val_mul, ":random", 100),
(assign, reg0, ":random"),
(str_store_string, s21, "@{!}{reg0}"),
],
"They paid {s21} mon and are expecting that you leave them alone. I agreed on a truce of 40 days.","companion_rejoin_response",
[
(call_script, "script_dplmc_pay_into_treasury", reg0),
(troop_get_slot, ":mission_object", "$g_talk_troop", slot_troop_mission_object),
(call_script, "script_diplomacy_start_peace_between_kingdoms", ":mission_object", "fac_player_supporters_faction", 1),
]],
[anyone, "dplmc_companion_threaten_request_response", [
(troop_get_slot, ":mission_object", "$g_talk_troop", slot_troop_mission_object),
(call_script, "script_diplomacy_faction_get_diplomatic_status_with_faction", "$players_kingdom", ":mission_object"),
(neq, reg0, -2), #no war
(le, "$g_mission_result", 0), #they want war or are undecided
],
"They send you a declaration of war.","companion_rejoin_response", [
(troop_get_slot, ":mission_object", "$g_talk_troop", slot_troop_mission_object),
(call_script, "script_diplomacy_start_war_between_kingdoms", ":mission_object", "fac_player_supporters_faction", 1),
]],
[anyone, "dplmc_companion_threaten_request_response", [
],
"They are not willing to fold facing your threats.","companion_rejoin_response", [
         ]],
[anyone, "dplmc_minister_gift_type",
[
(gt, "$g_player_chamberlain", 0),
(assign, ":companion_found", 0),
#gekokujo 3.0 microfactions! include fort companions start
#(try_for_range, ":emissary", companions_begin, companions_end),
(try_for_range, ":emissary", companions_begin, fort_companions_end),
#gekokujo 3.0 microfactions! include fort companions end
  (main_party_has_troop, ":emissary"),
  (assign, ":companion_found", 1),
  (try_end),
(eq, ":companion_found", 1),

],
"We can send them some excellent horses from the best horse breeder in our domain or we can hand over a fief.", "dplmc_minister_gift_type_select",
[]],
[anyone, "dplmc_minister_gift_type",
[
(le, "$g_player_chamberlain", 0),
(assign, ":companion_found", 0),
#gekokujo 3.0 microfactions! include fort companions start
#(try_for_range, ":emissary", companions_begin, companions_end),
(try_for_range, ":emissary", companions_begin, fort_companions_end),
#gekokujo 3.0 microfactions! include fort companions end
  (main_party_has_troop, ":emissary"),
  (assign, ":companion_found", 1),
(try_end),
(eq, ":companion_found", 1),
],
"We currently only have the option to hand over a fief since we don't have a treasurer.", "dplmc_minister_gift_type_select",
[]],
[anyone|plyr, "dplmc_minister_gift_type_select",
[
(gt, "$g_player_chamberlain", 0),
(store_troop_gold, ":gold", "trp_household_possessions"),
(try_begin),
(lt, ":gold", 3000),
(store_troop_gold, ":gold", "trp_player"),
(try_end),
(ge, ":gold", 3000),
],
"Send horses for 3000 mon.", "minister_diplomatic_emissary",
[
(assign, "$g_initiative_selected", dplmc_npc_mission_gift_horses_request),
(assign, "$diplomacy_var", 3000), # 6000 mon
]],
[anyone|plyr, "dplmc_minister_gift_type_select",
[
(gt, "$g_player_chamberlain", 0),
(store_troop_gold, ":gold", "trp_household_possessions"),
(try_begin),
(lt, ":gold", 6000),
(store_troop_gold, ":gold", "trp_player"),
(try_end),
(ge, ":gold", 6000),
],
"Send horses for 6000 mon.", "minister_diplomatic_emissary",
[
(assign, "$g_initiative_selected", dplmc_npc_mission_gift_horses_request),
(assign, "$diplomacy_var", 6000), # 6000 mon
]],
[anyone|plyr, "dplmc_minister_gift_type_select",
[
],
"Hand over a fief", "dplmc_minister_gift_fief",
[]],
[anyone|plyr, "dplmc_minister_gift_type_select",
[
],
"Never mind.", "minister_pretalk",
[]],
[anyone, "dplmc_minister_gift_fief",
[
],
"Which fief do you want to hand over?", "dplmc_minister_gift_fief_select",
[]],
[anyone|plyr|repeat_for_parties, "dplmc_minister_gift_fief_select",
[
(store_repeat_object, ":center_no"),
(is_between, ":center_no", centers_begin, centers_end),
(neq, ":center_no", "$g_player_court"),
(store_faction_of_party, ":center_faction", ":center_no"),
##diplomacy start+ Handle player is co-ruler of faction
##OLD:
#(eq, ":center_faction", "fac_player_supporters_faction"),
##NEW:
(call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", ":center_faction"),
(ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
##diplomacy end+
(str_store_party_name, s1, ":center_no"),

],"{s1}", "minister_diplomatic_emissary",
[
(store_repeat_object, "$diplomacy_var"),
(assign, "$g_initiative_selected", dplmc_npc_mission_gift_fief_request),
]],
[anyone, "dplmc_minister_exchange_prisoner_ask",
[
(assign, ":companion_found", 0),
#gekokujo 3.0 microfactions! include fort companions start
#(try_for_range, ":emissary", companions_begin, companions_end),
(try_for_range, ":emissary", companions_begin, fort_companions_end),
#gekokujo 3.0 microfactions! include fort companions end
  (main_party_has_troop, ":emissary"),
  (assign, ":companion_found", 1),
  (try_end),
(eq, ":companion_found", 1),

],
"Which prisoner do you want to exchange?", "dplmc_minister_exchange_prisoner_select",
[]],
[anyone, "dplmc_minister_exchange_prisoner_ask",
[
],
"Unfortunately, there is no one to send right now.", "minister_pretalk",
[]],
[anyone|plyr|repeat_for_troops, "dplmc_minister_exchange_prisoner_select",
[
(store_repeat_object, ":troop_no"),
(troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
(troop_get_slot, ":party", ":troop_no", slot_troop_prisoner_of_party),
(is_between, ":party", walled_centers_begin, walled_centers_end),
(party_slot_eq, ":party", slot_town_lord, "trp_player"),
(str_store_troop_name, s10, ":troop_no"),
(store_faction_of_troop, ":faction_no", ":troop_no"),
(str_store_faction_name, s11, ":faction_no"),
],
"{s10} of {s11}", "dplmc_minister_exchange_prisoner_lord_ask",
[
(store_repeat_object, "$diplomacy_var"),
(store_faction_of_troop, "$g_faction_selected", "$diplomacy_var"),
(assign, "$g_initiative_selected", dplmc_npc_mission_prisoner_exchange)
]],
[anyone|plyr, "dplmc_minister_exchange_prisoner_select",
[],
"Nobody.", "minister_pretalk",
[]],
[anyone, "dplmc_minister_exchange_prisoner_lord_ask",
[
],
"Which of our lords do you like to you want to set free?", "dplmc_minister_exchange_prisoner_lord_select",
[]],
[anyone|plyr|repeat_for_troops, "dplmc_minister_exchange_prisoner_lord_select",
[
(store_repeat_object, ":troop_no"),
(troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
(store_faction_of_troop, ":troop_faction", ":troop_no"),
##diplomacy start+ Handle player is co-ruler of kingdom
##OLD:
#(eq, ":troop_faction", "fac_player_supporters_faction"),
##NEW:
(call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", ":troop_faction"),
(ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
##diplomacy end+
(troop_get_slot, ":party", ":troop_no", slot_troop_prisoner_of_party),
(is_between, ":party", walled_centers_begin, walled_centers_end),
(store_faction_of_party, ":party_faction", ":party"),
(eq, ":party_faction", "$g_faction_selected"),
(str_store_troop_name, s10, ":troop_no"),
],
"{s10}.", "dplmc_minister_prisoner_emissary",
[
(store_repeat_object, "$diplomacy_var2"),
]],
[anyone|plyr, "dplmc_minister_exchange_prisoner_lord_select",
[],
"Nobody.", "minister_pretalk",
[]],
[anyone, "dplmc_minister_prisoner_emissary",
[], "Who shall negotiate the exchange?", "minister_emissary_select",
[]],
[anyone|plyr, "dplmc_companion_prisoner_exchange_confirm",
[],
##diplomacy start+ correct pronount using reg4
"Yes set {reg4?her:him} free.", "companion_rejoin_response",
##diplomacy end+
[  (troop_get_slot, ":enemy_prisoner", "$g_talk_troop", dplmc_slot_troop_mission_diplomacy),
(troop_get_slot, ":own_prisoner", "$g_talk_troop", dplmc_slot_troop_mission_diplomacy2),
(call_script, "script_remove_troop_from_prison", ":enemy_prisoner"),
(call_script, "script_remove_troop_from_prison", ":own_prisoner"),
(str_store_troop_name, s7, ":enemy_prisoner"),
(display_message, "str_dplmc_has_been_set_free"),
(str_store_troop_name, s7, ":own_prisoner"),
(display_message, "str_dplmc_has_been_set_free"),
(call_script, "script_change_player_relation_with_troop", ":own_prisoner", 3),
(call_script, "script_change_player_relation_with_troop", ":enemy_prisoner", 1),
(call_script, "script_change_player_honor", 1),
(call_script, "script_update_troop_notes", ":enemy_prisoner"),
(call_script, "script_update_troop_notes", ":own_prisoner"),
]],
[anyone|plyr, "dplmc_companion_prisoner_exchange_confirm",
[],
##diplomacy start+ correct pronount using reg4
"No don't set {reg4?her:him} free.", "companion_rejoin_response",
##diplomacy end+
[
(troop_get_slot, ":enemy_prisoner", "$g_talk_troop", dplmc_slot_troop_mission_diplomacy),
(troop_get_slot, ":own_prisoner", "$g_talk_troop", dplmc_slot_troop_mission_diplomacy2),
(troop_set_slot, ":own_prisoner", slot_troop_prisoner_of_party, -1),
(str_store_troop_name, s7, ":own_prisoner"),
(display_message, "str_dplmc_has_been_set_free"),
(call_script, "script_change_player_relation_with_troop", ":own_prisoner", 1),
(store_faction_of_troop, ":enemy_faction", ":enemy_prisoner"),
(call_script, "script_change_player_relation_with_faction", ":enemy_faction", -6),
(call_script, "script_change_player_honor", -2),
(call_script, "script_update_troop_notes", ":own_prisoner"),
]],
[anyone, "dplmc_minister_persuasion_fief_ask",
[
(assign, ":companion_found", 0),
#gekokujo 3.0 microfactions! include fort companions start
#(try_for_range, ":emissary", companions_begin, companions_end),
(try_for_range, ":emissary", companions_begin, fort_companions_end),
#gekokujo 3.0 microfactions! include fort companions end
(main_party_has_troop, ":emissary"),
(assign, ":companion_found", 1),
(try_end),
(eq, ":companion_found", 1),

],
"Your emissary can't go with empty hands we have to offer a fief. Which one do you want to offer?", "dplmc_minister_persuasion_fief",
[]],
[anyone, "dplmc_minister_persuasion_fief_ask",
[
],
"Unfortunately, there is no one to send right now.", "minister_pretalk",
[]],
[anyone|plyr|repeat_for_parties,"dplmc_minister_persuasion_fief", [
(store_repeat_object, ":center"),
  (is_between, ":center", centers_begin, centers_end),
(neq, ":center", "$g_player_court"),
(store_faction_of_party, ":center_faction", ":center"),
##diplomacy start+ Handle player is co-ruler of kingdom
(assign, ":alt_faction", "fac_player_supporters_faction"),
(try_begin),
	(is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
	(call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", "$players_kingdom"),
	(ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
	(assign, ":alt_faction", "$players_kingdom"),
(try_end),
(this_or_next|eq, ":alt_faction", ":center_faction"),
##diplomacy end+
(eq, ":center_faction", "fac_player_supporters_faction"),
(neg|party_slot_ge, ":center", slot_town_lord, active_npcs_begin), #ie, owned by player or unassigned
(str_store_party_name, s11, ":center"),

  ], "{s11}", "dplmc_minister_persuade_lord_faction_ask",[
(store_repeat_object, "$diplomacy_var2"),
]],
[anyone|plyr, "dplmc_minister_persuasion_fief", [
  ], "Never mind -- there is no fief I can offer.", "minister_pretalk",[
]],
[anyone, "dplmc_minister_persuade_lord_faction_ask",
[ ],
"Where does the lord live you want to persuade?", "dplmc_minister_persuade_lord_faction",
[]],
[anyone|plyr|repeat_for_factions, "dplmc_minister_persuade_lord_faction",
[
(store_repeat_object, ":faction_no"),
(is_between, ":faction_no", npc_kingdoms_begin, npc_kingdoms_end),
(faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
(str_store_faction_name, s11, ":faction_no"),
],
"{s11}", "dplmc_minister_persuade_lord_ask",
[
(store_repeat_object, "$g_faction_selected"),
]],
[anyone|plyr, "dplmc_minister_persuade_lord_faction", [
  ], "Nowhere.", "minister_pretalk",[
]],
[anyone, "dplmc_minister_persuade_lord_ask",
[
],
"Who shall be convinced?", "dplmc_minister_persuade_lord",
[]],
[anyone|plyr|repeat_for_troops, "dplmc_minister_persuade_lord",
[
(store_repeat_object, ":troop_no"),
(troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
(store_faction_of_troop, ":faction", ":troop_no"),
(is_between, ":faction", npc_kingdoms_begin, npc_kingdoms_end),
(faction_get_slot, ":faction_leader", ":faction", slot_faction_leader),
(neq, ":faction_leader", ":troop_no"),

(eq, ":faction", "$g_faction_selected"),
(troop_slot_eq, ":troop_no", slot_troop_met, 1),
#target still wants to talk
(neg|troop_slot_ge, ":troop_no", slot_troop_intrigue_impatience, 100),
(str_store_troop_name, s11, ":troop_no"),
],
"{s11}", "dplmc_minister_persuasion_emissary",
[
(store_repeat_object, "$diplomacy_var"),
(assign, "$g_initiative_selected", dplmc_npc_mission_persuasion),
]],
[anyone|plyr, "dplmc_minister_persuade_lord", [
  ], "I can't think of anyone.", "minister_pretalk",[
]],
[anyone, "dplmc_minister_persuasion_emissary",
[], "Who shall I send? You should choose one who has skills in persuasion!", "minister_emissary_select",
[]],
[anyone, "dplmc_minister_spy_kingdoms",
[
(assign, ":companion_found", 0),
#gekokujo 3.0 microfactions! include fort companions start
#(try_for_range, ":emissary", companions_begin, companions_end),
(try_for_range, ":emissary", companions_begin, fort_companions_end),
#gekokujo 3.0 microfactions! include fort companions end
(main_party_has_troop, ":emissary"),
(assign, ":companion_found", 1),
(try_end),
(eq, ":companion_found", 1),

],
"To whom do you wish to send this spy?", "dplmc_minister_spy_kingdoms_select",
[]],
[anyone, "dplmc_minister_spy_kingdoms",
[
],
"Unfortunately, there is no one to send right now.", "minister_pretalk",
[]],
[anyone|plyr|repeat_for_factions, "dplmc_minister_spy_kingdoms_select",
[
(store_repeat_object, ":faction_no"),
(is_between, ":faction_no", npc_kingdoms_begin, npc_kingdoms_end),
(faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
(faction_get_slot, ":leader_no", ":faction_no", slot_faction_leader),
(str_store_troop_name, s10, ":leader_no"),
(str_store_faction_name, s11, ":faction_no"),
(str_clear, s14),
],
"{s11}{s14}", "dplmc_minister_spy_emissary",
[
(store_repeat_object, "$g_faction_selected"),
(assign, "$g_initiative_selected", dplmc_npc_mission_spy_request)
]],
[anyone, "dplmc_minister_spy_emissary",
[], "Who shall be your spy? You should choose one whom you trust - and who has skills in spotting!", "minister_emissary_select",
[]],
[anyone|plyr|repeat_for_parties, "dplmc_companion_spy_request_select_center",
[
(store_repeat_object, ":center_no"),
(troop_get_slot, ":mission_object", "$g_talk_troop", slot_troop_mission_object),
(is_between, ":center_no", centers_begin, centers_end),
(store_faction_of_party, ":center_faction", ":center_no"),
(eq, ":center_faction", ":mission_object"),
(str_store_party_name, s60, ":center_no"),
],"{s60}", "dplmc_companion_spy_request_center_selected",
[
(store_repeat_object, "$spy_center_selected"),
]],
[anyone, "dplmc_companion_spy_request_center_selected", [
(call_script, "script_dplmc_party_calculate_strength", "$spy_center_selected", 0),
(try_begin),
  (le, reg0, 1),
  (str_store_string, s31, "str_dplmc_nearly_no"),
(else_try),
  (is_between, reg0, 1, 100),
  (str_store_string, s31, "str_dplmc_less_than_one_hundred"),
(else_try),
  (is_between, reg0, 101, 200),
  (str_store_string, s31, "str_dplmc_more_than_one_hundred"),
(else_try),
  (is_between, reg0, 201, 500),
  (str_store_string, s31, "str_dplmc_more_than_two_hundred"),
(else_try),
  (ge, reg0, 500),
  (str_store_string, s31, "str_dplmc_more_than_five_hundred"),
(try_end),

(call_script, "script_dplmc_describe_prosperity_to_s4", "$spy_center_selected"),

(party_get_slot, ":center_relation", "$spy_center_selected", slot_center_player_relation),
(call_script, "script_describe_center_relation_to_s3", ":center_relation"),

],  "{s4} {s3} and there are {s31} troops around.", "dplmc_companion_spy_request_select_newcenter", [
    ]],
[anyone, "dplmc_companion_spy_request_select_newcenter", [
],  "Do you need information about another location?", "dplmc_companion_spy_request_select_center", [
    ]],
[anyone|plyr, "dplmc_companion_spy_request_select_center", [
],  "Never mind.", "companion_rejoin_response", [
    ]],
[anyone, "dplmc_companion_alliance_request_response", [
(troop_slot_eq, "$g_talk_troop", slot_troop_current_mission, dplmc_npc_mission_alliance_request),
(troop_get_slot, ":mission_object", "$g_talk_troop", slot_troop_mission_object),
(call_script, "script_diplomacy_faction_get_diplomatic_status_with_faction", "fac_player_supporters_faction", ":mission_object"),
(ge, reg0, 0),  #player is at peace or truce with the mission_faction
(eq, "$g_concession_demanded", 0), #doesn't want a center from us
(ge, "$g_mission_result_with_player", 1), #doesn't want war with us
(store_relation, ":relation", "fac_player_supporters_faction", ":mission_object"),
(store_random_in_range,":random", 20, 95),
(ge, ":relation", ":random"),
(store_random_in_range,":random", 5, 75),
(ge, "$player_honor", ":random"),
(store_random_in_range,":random", 5, 50),
(ge, "$player_right_to_rule", ":random"),
(faction_get_slot, ":emissary_object", ":mission_object", slot_faction_leader),
(str_store_troop_name, s4, ":emissary_object"),
],
"{s4} is willing to form an alliance with you.","dplmc_companion_alliance_confirm", [
         ]],
[anyone|plyr, "dplmc_companion_alliance_confirm", [
(troop_get_slot, ":mission_object", "$g_talk_troop", slot_troop_mission_object),
(str_store_faction_name, s4, ":mission_object"),
],
"Very well - let this alliance with {s4} be concluded.","companion_rejoin_response", [
(troop_get_slot, ":mission_object", "$g_talk_troop", slot_troop_mission_object),
(call_script, "script_dplmc_start_alliance_between_kingdoms", ":mission_object", "$players_kingdom", 1),
(str_store_faction_name, s4, ":mission_object"),
]],
[anyone|plyr, "dplmc_companion_alliance_confirm", [],
"On second thought, perhaps this is not now in our interests.","companion_rejoin_response", [
         ]],
[anyone, "dplmc_companion_alliance_request_response", [
(troop_slot_eq, "$g_talk_troop", slot_troop_current_mission, dplmc_npc_mission_alliance_request),
(troop_get_slot, ":mission_object", "$g_talk_troop", slot_troop_mission_object),
(faction_get_slot, ":emissary_object", ":mission_object", slot_faction_leader),
(str_store_troop_name, s4, ":emissary_object"),
],
"{s4} is not willing to form an alliance with you.","companion_rejoin_response", [
         ]],
[anyone, "dplmc_companion_defensive_request_response", [
(troop_slot_eq, "$g_talk_troop", slot_troop_current_mission, dplmc_npc_mission_defensive_request),
(troop_get_slot, ":mission_object", "$g_talk_troop", slot_troop_mission_object),
(call_script, "script_diplomacy_faction_get_diplomatic_status_with_faction", "fac_player_supporters_faction", ":mission_object"),
(ge, reg0, 0),  #player is at peace or truce with the mission_faction
(eq, "$g_concession_demanded", 0), #doesn't want a center from us
(ge, "$g_mission_result_with_player", 1), #doesn't want war with us
(store_relation, ":relation", "fac_player_supporters_faction", ":mission_object"),
(store_random_in_range,":random", 15, 70), #20 96 alliance
(ge, ":relation", ":random"),
(store_random_in_range,":random", 0, 50), #5 75 alliance
(ge, "$player_honor", ":random"),
(store_random_in_range,":random", 5, 30), #5 50 alliance
(ge, "$player_right_to_rule", ":random"),
(faction_get_slot, ":emissary_object", ":mission_object", slot_faction_leader),
(str_store_troop_name, s4, ":emissary_object"),
],
"{s4} is willing to form a defensive pact with you.","dplmc_companion_defensive_confirm", [
         ]],
[anyone|plyr, "dplmc_companion_defensive_confirm", [
(troop_get_slot, ":mission_object", "$g_talk_troop", slot_troop_mission_object),
(str_store_faction_name, s4, ":mission_object"),
],
"Very well - let this defensive pact with {s4} be concluded.","companion_rejoin_response", [
(troop_get_slot, ":mission_object", "$g_talk_troop", slot_troop_mission_object),
(call_script, "script_dplmc_start_defensive_between_kingdoms", ":mission_object", "$players_kingdom", 1),
(str_store_faction_name, s4, ":mission_object"),
]],
[anyone|plyr, "dplmc_companion_defensive_confirm", [],
"On second thought, perhaps this is not now in our interests.","companion_rejoin_response", [
         ]],
[anyone, "dplmc_companion_defensive_request_response", [
(troop_slot_eq, "$g_talk_troop", slot_troop_current_mission, dplmc_npc_mission_defensive_request),
(troop_get_slot, ":mission_object", "$g_talk_troop", slot_troop_mission_object),
(faction_get_slot, ":emissary_object", ":mission_object", slot_faction_leader),
(str_store_troop_name, s4, ":emissary_object"),
],
"{s4} is not willing to conclude a defensive pact with you.","companion_rejoin_response", [
         ]],
[anyone, "dplmc_companion_trade_request_response", [
(troop_slot_eq, "$g_talk_troop", slot_troop_current_mission, dplmc_npc_mission_trade_request),
(troop_get_slot, ":mission_object", "$g_talk_troop", slot_troop_mission_object),
(call_script, "script_diplomacy_faction_get_diplomatic_status_with_faction", "fac_player_supporters_faction", ":mission_object"),
(ge, reg0, 0),  #player is at peace or truce with the mission_faction
(eq, "$g_concession_demanded", 0), #doesn't want a center from us
(ge, "$g_mission_result_with_player", 1), #doesn't want war with us
(store_relation, ":relation", "fac_player_supporters_faction", ":mission_object"),
(store_random_in_range,":random", 10, 50), #20 96 alliance
(ge, ":relation", ":random"),
(store_random_in_range,":random", 0, 25), #5 75 alliance
(ge, "$player_honor", ":random"),
(store_random_in_range,":random", 5, 15), #5 50 alliance
(ge, "$player_right_to_rule", ":random"),
(faction_get_slot, ":emissary_object", ":mission_object", slot_faction_leader),
(str_store_troop_name, s4, ":emissary_object"),
],
"{s4} is willing to sign a trade agreement with you.","dplmc_companion_trade_confirm", [
         ]],
[anyone|plyr, "dplmc_companion_trade_confirm", [
(troop_get_slot, ":mission_object", "$g_talk_troop", slot_troop_mission_object),
(str_store_faction_name, s4, ":mission_object"),
],
"Very well - let's sign the trade agreement with {s4}.","companion_rejoin_response", [
(troop_get_slot, ":mission_object", "$g_talk_troop", slot_troop_mission_object),
(call_script, "script_dplmc_start_trade_between_kingdoms", ":mission_object", "$players_kingdom", 1),
(str_store_faction_name, s4, ":mission_object"),
]],
[anyone|plyr, "dplmc_companion_trade_confirm", [],
"On second thought, perhaps this is not now in our interests.","companion_rejoin_response", [
         ]],
[anyone, "dplmc_companion_trade_request_response", [
(troop_slot_eq, "$g_talk_troop", slot_troop_current_mission, dplmc_npc_mission_trade_request),
(troop_get_slot, ":mission_object", "$g_talk_troop", slot_troop_mission_object),
(faction_get_slot, ":emissary_object", ":mission_object", slot_faction_leader),
(str_store_troop_name, s4, ":emissary_object"),
],
"{s4} is not willing to sign a trade agreement.","companion_rejoin_response", [
         ]],
[anyone, "dplmc_companion_nonaggression_request_response", [
(troop_slot_eq, "$g_talk_troop", slot_troop_current_mission, dplmc_npc_mission_nonaggression_request),
(troop_get_slot, ":mission_object", "$g_talk_troop", slot_troop_mission_object),
(call_script, "script_diplomacy_faction_get_diplomatic_status_with_faction", "fac_player_supporters_faction", ":mission_object"),
(ge, reg0, 0),  #player is at peace or truce with the mission_faction
(eq, "$g_concession_demanded", 0), #doesn't want a center from us
(ge, "$g_mission_result_with_player", 1), #doesn't want war with us
(store_relation, ":relation", "fac_player_supporters_faction", ":mission_object"),
(store_random_in_range,":random", 5, 25), #20 96 alliance
(ge, ":relation", ":random"),
(store_random_in_range,":random", 0, 20), #5 75 alliance
(ge, "$player_honor", ":random"),
(store_random_in_range,":random", 5, 10), #5 50 alliance
(ge, "$player_right_to_rule", ":random"),
(faction_get_slot, ":emissary_object", ":mission_object", slot_faction_leader),
(str_store_troop_name, s4, ":emissary_object"),
],
"{s4} is willing to conclude a non-aggression treaty with you.","dplmc_companion_nonaggression_confirm", [
         ]],
[anyone|plyr, "dplmc_companion_nonaggression_confirm", [
(troop_get_slot, ":mission_object", "$g_talk_troop", slot_troop_mission_object),
(str_store_faction_name, s4, ":mission_object"),
],
"Very well - let this non-aggression treaty with {s4} be concluded.","companion_rejoin_response", [
(troop_get_slot, ":mission_object", "$g_talk_troop", slot_troop_mission_object),
(call_script, "script_dplmc_start_nonaggression_between_kingdoms", ":mission_object", "$players_kingdom", 1),
(str_store_faction_name, s4, ":mission_object"),
]],
[anyone|plyr, "dplmc_companion_nonaggression_confirm", [],
"On second thought, perhaps this is not now in our interests.","companion_rejoin_response", [
         ]],
[anyone, "dplmc_companion_nonaggression_request_response", [
(troop_slot_eq, "$g_talk_troop", slot_troop_current_mission, dplmc_npc_mission_nonaggression_request),
(troop_get_slot, ":mission_object", "$g_talk_troop", slot_troop_mission_object),
(faction_get_slot, ":emissary_object", ":mission_object", slot_faction_leader),
(str_store_troop_name, s4, ":emissary_object"),
],
"{s4} is not willing to conclude a non-aggression treaty with you.","companion_rejoin_response", [
         ]],
[anyone, "dplmc_companion_war_request_response", [
(troop_slot_eq, "$g_talk_troop", slot_troop_current_mission, dplmc_npc_mission_war_request),
(lt, "$g_mission_result_with_target", 0), #<0 want's war with target
(ge, "$g_mission_result_with_player", 2), #doesn't want war with us
(eq, "$g_concession_demanded", 0), #doesn't want a center from us
(troop_get_slot, ":mission_object", "$g_talk_troop", slot_troop_mission_object),
(call_script, "script_diplomacy_faction_get_diplomatic_status_with_faction", "fac_player_supporters_faction", ":mission_object"),
(ge, reg0, 0),  #player is at peace or truce with the mission_faction
(troop_get_slot, ":war_target_faction", "$g_talk_troop", dplmc_slot_troop_mission_diplomacy),
##diplomacy start+
#The other kingdom will only agree to declare war without asking for money in return
#if the player's kingdom is also at war with it, or if it is in an alliance with the
#player's kingdom.
(store_relation, ":player_faction_relation_with_war_target", ":war_target_faction", "$players_kingdom"),
(call_script, "script_dplmc_get_faction_truce_length_with_faction", ":mission_object", "$players_kingdom"),
(this_or_next|ge, reg0, dplmc_treaty_defense_days_half_done),
   (lt, ":player_faction_relation_with_war_target", 0),
##diplomacy end+
(str_store_faction_name, s31, ":war_target_faction"),
(faction_get_slot, ":emissary_object", ":mission_object", slot_faction_leader),
(str_store_troop_name, s4, ":emissary_object"),
],
"{s4} is willing to start a war with {s31}.","companion_rejoin_response", [
(troop_get_slot, ":mission_object", "$g_talk_troop", slot_troop_mission_object),
(troop_get_slot, ":war_target_faction", "$g_talk_troop", dplmc_slot_troop_mission_diplomacy),
(call_script, "script_diplomacy_start_war_between_kingdoms",  ":mission_object", ":war_target_faction", 1)
         ]],
[anyone, "dplmc_companion_war_request_response", [
(troop_slot_eq, "$g_talk_troop", slot_troop_current_mission, dplmc_npc_mission_war_request),
##diplomacy start+
(this_or_next|lt, "$g_mission_result_with_target", 0),
##diplomacy end+
(eq, "$g_mission_result_with_target", 0), #undecided about war
(ge, "$g_mission_result_with_player", 2), #doesn't want war with us
(eq, "$g_concession_demanded", 0), #doesn't want a center from us
(troop_get_slot, ":mission_object", "$g_talk_troop", slot_troop_mission_object),
(call_script, "script_diplomacy_faction_get_diplomatic_status_with_faction", "fac_player_supporters_faction", ":mission_object"),
(ge, reg0, 0),  #player is at peace or truce with the mission_faction
(troop_get_slot, ":war_target_faction", "$g_talk_troop", dplmc_slot_troop_mission_diplomacy),
(str_store_faction_name, s31, ":war_target_faction"),
(faction_get_slot, ":emissary_object", ":mission_object", slot_faction_leader),
(str_store_troop_name, s4, ":emissary_object"),
##diplomacy start+
#Set the payment amount to something less arbitrary than a flat 5000.
#For example, using the same mercenary payment calculation used for the player.
(assign, ":total_fee", 0),
(try_for_parties, ":party_no"),
   (gt, ":party_no", centers_end),
	(party_is_active, ":party_no"),
   (store_faction_of_party, ":party_faction", ":party_no"),
	(eq, ":party_faction", ":mission_object"),
	(this_or_next|party_slot_eq, ":party_no", slot_party_type, spt_kingdom_hero_party),
	   (party_slot_eq, ":party_no", slot_party_type, spt_patrol),
	(try_begin),
	   (eq, "$g_dplmc_terrain_advantage", DPLMC_TERRAIN_ADVANTAGE_ENABLE),
		(call_script, "script_dplmc_get_terrain_code_for_battle", -1, ":party_no"),
		(call_script, "script_dplmc_party_calculate_strength_in_terrain", ":party_no", reg0, 0, 1),
		#Cache terrain value, but use non-terrain value for cost
		(assign, reg0, reg1),
	(else_try),
	   (call_script, "script_party_calculate_strength", ":party_no", 0),
	(try_end),
	(val_div, reg0, 2),
	(val_add, reg0, 30),
	(call_script, "script_round_value", reg0),
	(val_max, reg0, 50),#at least 50 mon per party
	(val_add, ":total_fee", reg0),
(try_end),
(val_mul, ":total_fee", 2),#The mercenary fee for two weeks

(try_begin),
	#Lessen the fee if the other kingdom particularly wants war
	(lt, "$g_mission_result_with_target", 0),
	(val_div, ":total_fee", 2),
(try_end),
(try_begin),
	#Increase the fee if the player's faction is allied with the target
	#(note: this should probably be disabled altogether...)
	(call_script, "script_dplmc_get_faction_truce_length_with_faction", ":mission_object", "$players_kingdom"),
	(ge, reg0, dplmc_treaty_defense_days_expire),
	(val_mul, ":total_fee", 3),
(else_try),
	(store_relation, reg0, ":war_target_faction", "$players_kingdom"),
	(val_mul, reg0, 2),
(try_end),

(game_get_reduce_campaign_ai, ":reduce_campaign_ai"),
(try_begin),
   (eq, ":reduce_campaign_ai", 0),#Hard: 150%
	(val_mul, ":total_fee", 3),
	(val_div, ":total_fee", 2),
(else_try),
   (eq, ":reduce_campaign_ai", 1),#Medium: 100%
(else_try),
   (eq, ":reduce_campaign_ai", 2),#Easy: 50%
	(val_div, ":total_fee", 2),
(try_end),

(val_max, ":total_fee", 5000),

(call_script, "script_dplmc_store_troop_is_female", ":mission_object"),
(assign, reg1, ":total_fee"),
(assign, "$temp_2", ":total_fee"),#save for later
],
#"{s4} is willing to start a war with {s31} but needs 5000 mon to prepare his army.","dplmc_companion_war_pay", [
"{s4} is willing to start a war with {s31} but needs {reg1} mon to prepare {reg0?her:his} army.","dplmc_companion_war_pay", [
         ]],
[anyone|plyr, "dplmc_companion_war_pay", [
(troop_get_slot, ":mission_object", "$g_talk_troop", slot_troop_mission_object),
(str_store_faction_name, s4, ":mission_object"),
(gt, "$g_player_chamberlain", 0),
(store_troop_gold, ":gold", "trp_household_possessions"),
##diplomacy start+
#(ge, ":gold", 5000),
(ge, ":gold", "$temp_2"),
(call_script, "script_dplmc_store_troop_is_female", ":mission_object"),
(assign, reg1, "$temp_2"),
],
#"Pay 5000 mon from the treasury and tell him to start the war.","companion_rejoin_response", [
"Pay {reg1} mon from the treasury and tell {reg0?her:him} to start the war.","companion_rejoin_response", [
#(call_script, "script_dplmc_withdraw_from_treasury", 5000),
(assign, ":paid_gold", "$temp_2"),
(call_script, "script_dplmc_withdraw_from_treasury", ":paid_gold"),
##diplomacy end+
(troop_get_slot, ":mission_object", "$g_talk_troop", slot_troop_mission_object),
##diplomacy start+ actually give gold to other kingdom
(call_script, "script_dplmc_faction_leader_splits_gold", ":mission_object", ":paid_gold"),
##diplomacy end+
(troop_get_slot, ":war_target_faction", "$g_talk_troop", dplmc_slot_troop_mission_diplomacy),
(call_script, "script_diplomacy_start_war_between_kingdoms",  ":mission_object", ":war_target_faction", 1)
]],
[anyone|plyr, "dplmc_companion_war_pay", [],
"On second thought, I don't think we can take so much money from the treasury.","companion_rejoin_response", [
         ]],
[anyone, "dplmc_companion_war_request_response", [
(troop_slot_eq, "$g_talk_troop", slot_troop_current_mission, dplmc_npc_mission_war_request),
(troop_get_slot, ":mission_object", "$g_talk_troop", slot_troop_mission_object),
(troop_get_slot, ":war_target_faction", "$g_talk_troop", dplmc_slot_troop_mission_diplomacy),
(str_store_faction_name, s31, ":war_target_faction"),
(faction_get_slot, ":emissary_object", ":mission_object", slot_faction_leader),
(str_store_troop_name, s4, ":emissary_object"),
],
"{s4} is not willing to start a war with {s31}.","companion_rejoin_response", [
         ]],
[anyone|plyr, "dplmc_companion_truce_pay", [
(troop_get_slot, ":mission_object", "$g_talk_troop", slot_troop_mission_object),
(str_store_faction_name, s4, ":mission_object"),
(store_troop_gold, ":gold", "trp_player"),#
##diplomacy start+
(assign, reg0, "$temp"),
(gt, reg0, 0),
(ge, ":gold", reg0),
],
"Pay {reg0} mon and let the truce with the {s4} be concluded","companion_rejoin_response", [
(troop_get_slot, ":mission_object", "$g_talk_troop", slot_troop_mission_object),
(troop_remove_gold, "trp_player", "$temp"),#todo change amount
#actually give gold to other kingdom
(call_script, "script_dplmc_faction_leader_splits_gold", ":mission_object", "$temp"),
##diplomacy end+
(call_script, "script_diplomacy_start_peace_between_kingdoms", ":mission_object", "$players_kingdom", 1),
(str_store_faction_name, s4, ":mission_object"),
]],
[anyone|plyr, "dplmc_companion_truce_pay", [
(troop_get_slot, ":mission_object", "$g_talk_troop", slot_troop_mission_object),
(str_store_faction_name, s4, ":mission_object"),
(store_troop_gold, ":gold", "trp_player"),
##diplomacy start+
(assign, reg1, "$temp_2"),
(gt, reg1, 0),
(ge, ":gold", reg1),
(faction_get_slot, ":emissary_object", ":mission_object", slot_faction_leader),
(assign, reg4, 0),
(try_begin),
	(call_script, "script_cf_dplmc_troop_is_female", ":emissary_object"),
	(assign, reg4, 1),
(try_end),
],
"Pay {reg1} mon and give {reg4?her:him} {s18} let this truce with the {s4} be concluded","companion_rejoin_response", [
(troop_get_slot, ":mission_object", "$g_talk_troop", slot_troop_mission_object),
(troop_remove_gold, "trp_player", reg1),#todo change amount
#actually give gold to other kingdom
(call_script, "script_dplmc_faction_leader_splits_gold", ":mission_object", reg0),
##diplomacy end+
(call_script, "script_give_center_to_faction", "$g_concession_demanded", ":mission_object"),
(call_script, "script_diplomacy_start_peace_between_kingdoms", ":mission_object", "$players_kingdom", 1),
(str_store_faction_name, s4, ":mission_object"),
]],
[anyone|plyr, "dplmc_companion_truce_pay", [
(troop_get_slot, ":mission_object", "$g_talk_troop", slot_troop_mission_object),
(str_store_faction_name, s4, ":mission_object"),
(gt, "$g_concession_demanded", 0),
##diplomacy start+
(eq, "$temp_2", 0),
(faction_get_slot, ":leader_no", ":mission_object", slot_faction_leader),
(call_script, "script_dplmc_store_troop_is_female", ":leader_no"),
],#next line "him" to {reg0?her:him}
"Give {reg0?her:him} {s18} let this truce with the {s4} be concluded","companion_rejoin_response", [
##diplomacy end+
(troop_get_slot, ":mission_object", "$g_talk_troop", slot_troop_mission_object),
(call_script, "script_give_center_to_faction", "$g_concession_demanded", ":mission_object"),
(call_script, "script_diplomacy_start_peace_between_kingdoms", ":mission_object", "$players_kingdom", 1),
(str_store_faction_name, s4, ":mission_object"),
]],
[anyone|plyr, "dplmc_companion_truce_pay", [],
"On second thought, perhaps this is not now in our interests..","companion_rejoin_response", [
         ]],
[anyone|plyr, "dplmc_minister_nevermind", [],
	"I might go do so.", "close_window",[]],
[anyone|plyr, "dplmc_minister_nevermind", [],
	"Never mind.", "minister_pretalk",[]],
[anyone|plyr, "dplmc_companion_quitting_lord_1", [
], "Farewell, then.", "dplmc_companion_quitting_lord_2", [
    ]],
[anyone|plyr, "dplmc_companion_quitting_lord_1", [
(eq, "$player_can_persuade_npc", 1),
], "Perhaps I can persuade you to change your mind.", "dplmc_companion_quitting_lord_persuasion", [
(assign, "$player_can_persuade_npc", 0),
    ]],
[anyone, "dplmc_companion_quitting_lord_persuasion", [
          (store_random_in_range, ":random", -2, 13),
          (store_skill_level, ":persuasion", "skl_persuasion", "trp_player"),
          (le, ":random", ":persuasion"),
               ],
"Hm.  I suppose I can afford to put it off a bit longer.", "close_window",
[
          (troop_get_slot, ":morality_penalties", "$map_talk_troop", slot_troop_morality_penalties),
          (val_div, ":morality_penalties", 2),
          (troop_set_slot, "$map_talk_troop", slot_troop_morality_penalties, ":morality_penalties"),

          (troop_get_slot, ":personalityclash_penalties", "$map_talk_troop", slot_troop_personalityclash_penalties),
          (val_div, ":personalityclash_penalties", 2),
          (troop_set_slot, "$map_talk_troop", slot_troop_personalityclash_penalties, ":personalityclash_penalties"),
 ]],
[anyone, "dplmc_companion_quitting_lord_persuasion", [
               ],
"I'm sorry, but I can't put it off any longer.", "dplmc_companion_quitting_lord_1",
[
 ]],
[anyone|plyr, "dplmc_companion_quitting_lord_2", [
], "Farewell, then.", "lord_leave", [#Jump to standard lord farewell dialog
	(try_begin),
		(this_or_next|troop_slot_eq, "$map_talk_troop", slot_troop_playerparty_history, dplmc_pp_history_granted_fief),
		(this_or_next|troop_slot_eq, "$map_talk_troop", slot_troop_playerparty_history, dplmc_pp_history_lord_rejoined),
		#(troop_slot_eq, "$map_talk_troop", slot_troop_occupation, slto_player_companion),
		(troop_set_slot, "$map_talk_troop", slot_troop_occupation, slto_kingdom_hero),
	(try_end),
	(remove_member_from_party, "$map_talk_troop", "p_main_party"),

	(troop_set_slot, "$map_talk_troop", slot_troop_personalityclash_penalties, 0),
	(troop_set_slot, "$map_talk_troop", slot_troop_morality_penalties, 0),
]],
[anyone, "dplmc_companion_quitting_persuasion_start", [
	#First line, respond in slightly-more-formal diction.
	(troop_get_slot, ":personality", "$map_talk_troop", slot_lord_reputation_type),
	(assign, ":formal_response", 0),#accept or reject
	(try_begin),
		#Nobles and well-educated commoners answer this way.
		(this_or_next|ge, ":personality", lrep_benefactor),#includes lrep_benefactor and all kingdom lady personalities
			(is_between, ":personality", lrep_none, lrep_roguish),
		#Exclude quarrelsome and debauched.  They are not inclined to mince words when they're discontent.
		(neq, ":personality", lrep_quarrelsome),
		(neq, ":personality", lrep_debauched),
		(assign, ":formal_response", 1),
	(else_try),
		#"Well-educated commoners" includes some custodians but not others.
		#(For example, in Native compare Katrin with Artimenner.)
		(eq, ":personality", lrep_custodian),

		#Checking intelligence by itself isn't enough, since there isn't all
		#that much variation at the starting levels, and many companions
		#will have their intelligence raised for party skills regardless of
		#their background.
		(store_attribute_level, ":intelligence", "$map_talk_troop", ca_intelligence),
		(ge, ":intelligence", 12),

		#As the lesser of several evils, I'll add a secondary check for Engineer,
		#which is obviously arbitrary somewhat targeted but may catch Artimenner-like
		#characters in other mods.
		(store_skill_level, ":engineer", "$map_talk_troop", "skl_engineer"),
		(ge, ":engineer", 4),
		(assign, ":formal_response", 1),
	(try_end),
	(neq, ":formal_response", 0),
], "Very well, I shall hear you out.", "dplmc_companion_quitting_persuasion_1", [
]],
[anyone, "dplmc_companion_quitting_persuasion_start", [#Less-formal response
], "I'm listening.", "dplmc_companion_quitting_persuasion_1", [
]],
[anyone|plyr, "dplmc_companion_quitting_persuasion_1", [
], "We've had some good times.  Things might not be going to your liking now, but stay with me a while longer and the situation will turn around.", "companion_quitting_persuasion", [
]],
[anyone|plyr, "dplmc_companion_quitting_persuasion_1", [
	#The same calculation as ransoming a companion from a ransom broker.
	#(From a game balance perspective, the effect is similar: you are
	#paying to avoid losing access to your companion.)
	(store_character_level, ":companion_level", "$map_talk_troop"),
	(store_add, ":cost", ":companion_level", 20),
	(val_mul, ":cost", ":companion_level"),
	(val_mul, ":cost", 5), #Level 1: 110, level 40: 12,000

	#Since there's no random check here, instead the persuasion skill
	#is used to reduce the price.
	(store_skill_level, ":persuasion", "skl_persuasion", "trp_player"),

	#Because this pertains to the handling of subordinates, in my
	#opinion skl_leadership is also directly relevant (since this is
	#how it works with non-hero troops, where your leadership
	#raises their morale and makes them less likely to desert).
	(store_skill_level, reg0, "skl_leadership", "trp_player"),
	(val_max, ":persuasion", reg0),

	(val_clamp, ":persuasion", 0, 19),
	(store_sub, reg0, 20, ":persuasion"),
	(val_mul, ":cost", reg0),
	(val_div, ":cost", 20),

	#Check if the player can afford it.
	(store_troop_gold, ":treasury", "trp_household_possessions"),
	(store_troop_gold, ":purse", "trp_player"),
	(store_add, ":available_funds", ":treasury", ":purse"),
	(ge, ":available_funds", ":cost"),

	(assign, "$temp", ":cost"),
	
	#gekokujo companion bribe - make sure the quoted price matches the actual price
	(assign, reg0, ":cost"),


], "Would {reg0} mon convince you to remain a while longer?", "dplmc_companion_quitting_persuasion_bribe", [
      (assign, "$player_can_persuade_npc", 0),
    ]],
[anyone|plyr, "dplmc_companion_quitting_persuasion_1", [
], "Actually, nevermind.  I meant to say something else.", "companion_quitting_response", [
	(assign, "$player_can_persuade_npc", 1),#revert
]],
[anyone, "dplmc_companion_quitting_persuasion_bribe", [
	#Player bribes companion to remain
               ],
"Hm. When you put it like that, I suppose I can stay a while longer, see if things improve.", "close_window",
[
		  (assign, reg0, "$temp"),#cost to pay
		  #Remove the gold from the player
		  (val_max, reg0, 0),
		  (store_troop_gold, ":funds", "trp_player"),
		  (val_min, ":funds", reg0),
		  (val_sub, reg0, ":funds"),
		  (troop_remove_gold, "trp_player", ":funds"),

		  #Remove any remaining gold from the treasury
		  (store_troop_gold, ":funds", "trp_household_possessions"),
		  (val_min, ":funds", reg0),
		  (val_sub, reg0, ":funds"),
		  (call_script, "script_dplmc_withdraw_from_treasury", ":funds"),

		  #Reduce penalties per a successful persuasion attempt
          (troop_get_slot, ":morality_penalties", "$map_talk_troop", slot_troop_morality_penalties),
          (val_div, ":morality_penalties", 2),
          (troop_set_slot, "$map_talk_troop", slot_troop_morality_penalties, ":morality_penalties"),

          (troop_get_slot, ":personalityclash_penalties", "$map_talk_troop", slot_troop_personalityclash_penalties),
          (val_div, ":personalityclash_penalties", 2),
          (troop_set_slot, "$map_talk_troop", slot_troop_personalityclash_penalties, ":personalityclash_penalties"),
 ]],
[anyone, "dplmc_lord_internal_politics_plyr_request_support_1", [],
"Whom did you have in mind?", "dplmc_lord_internal_politics_plyr_request_support_1",
[]
],
[anyone|plyr,"dplmc_lord_internal_politics_plyr_request_support_1", [
],
"Never mind.", "lord_pretalk",
[
]],
[anyone|plyr|repeat_for_troops,"dplmc_lord_internal_politics_plyr_request_support_1", [
(store_repeat_object, ":candidate"),
(is_between, ":candidate", heroes_begin, heroes_end),
(troop_slot_eq, ":candidate", slot_troop_occupation, slto_kingdom_hero),
(store_faction_of_troop, ":candidate_faction", ":candidate"),
(eq, ":candidate_faction", "$players_kingdom"),
(neq, ":candidate", "$g_talk_troop"),
(neg|troop_slot_eq, "$g_talk_troop", slot_troop_stance_on_faction_issue, ":candidate"),
(str_store_troop_name, s4, ":candidate"),
(try_begin),
	(neg|troop_slot_eq, "$g_talk_troop", slot_troop_met, 0),
	(neg|troop_slot_eq, ":candidate", slot_troop_met, 0),
	(call_script, "script_dplmc_cap_troop_describes_troop_to_troop_s1", 1, "trp_player", ":candidate", "$g_talk_troop"),
	(str_store_string_reg, s4, s1),
(try_end),
],
"{s4}", "dplmc_lord_internal_politics_plyr_request_support_2",
[
(store_repeat_object, ":candidate"),
(assign, "$lord_selected", ":candidate"),
]],
[anyone|plyr,"dplmc_lord_internal_politics_plyr_request_support_1", [
],
"Never mind.", "lord_pretalk",
[
]],
[anyone, "dplmc_lord_internal_politics_plyr_request_support_2", [
#fail if relation with player is too low
(lt, "$g_talk_troop_effective_relation", -5),#-5 for most troops
(call_script, "script_dplmc_is_affiliated_family_member", "$g_talk_troop"),#-10 for affiliated family members
(this_or_next|eq, reg0, 0),
   (le, "$g_talk_troop_effective_relation", -10),#redundant, since script_dplmc_is_affiliated_family_member checks relation too
],
"Given our relationship, I would prefer to keep my own counsel on this matter.", "lord_pretalk",
[]
],
[anyone, "dplmc_lord_internal_politics_plyr_request_support_2", [
#fail if target controversy is too high
(troop_slot_ge, "$lord_selected", slot_troop_controversy, 25),
(this_or_next|faction_slot_eq, "$players_kingdom", slot_faction_political_issue, 1),
(troop_slot_ge, "$lord_selected", slot_troop_controversy, 50),
(str_store_troop_name, s4, "$lord_selected"),
(assign, reg3, 0),
(try_begin),
	(call_script, "script_cf_dplmc_troop_is_female", "$lord_selected"),
	(assign, reg3, 1),
(try_end),
],
"{s4} has engendered too much controversy for {reg3?her:him} to be a viable candidate right now.  I would advise {reg3?her:him} to wait a little while before seeking any further honors.", "lord_pretalk",
[]
],
[anyone,"dplmc_lord_internal_politics_plyr_request_support_2", [
#for fiefs, fail if the target has too many fiefs for his renown
(faction_get_slot, ":faction_issue", "$players_kingdom", slot_faction_political_issue),
(is_between, ":faction_issue", centers_begin, centers_end),

(troop_get_slot, ":other_pick", "$g_talk_troop", slot_troop_stance_on_faction_issue),

(troop_get_slot, ":player_pick_renown", "$lord_selected", slot_troop_renown),
(assign, ":other_pick_renown", 0),#default to 0 if talk troop is undecided
(try_begin),
   (this_or_next|is_between, ":other_pick", heroes_begin, heroes_end),
      (eq, ":other_pick", "trp_player"),
   (troop_get_slot, ":other_pick_renown", ":other_pick", slot_troop_renown),
(try_end),

(call_script, "script_dplmc_center_point_calc", "$g_talk_troop_faction", "$lord_selected", ":other_pick", 2),
(assign, ":average_renown_per_point", reg0),# faction total renown / total center points (or 0 for no points)
(assign, ":player_pick_points", reg1),# player_pick total center points
(assign, ":other_pick_points", reg3),#other_pick total center points
#(assign, ":average_renown", reg4),#unused

#Using val_max is a bad way of doing things, because it erases the difference
#between someone with one fief and someone with no fiefs, but I've left it like
#this for now to match the Native logic for convincing an NPC to support the
#player for a fief.
(val_max, ":player_pick_points", 1),
(store_div, ":player_pick_renown_per_center_point",  ":player_pick_renown", ":player_pick_points",),

(val_max, ":other_pick_points", 1),
(store_div, ":other_pick_renown_per_center_point",  ":other_pick_renown", ":other_pick_points",),

##save for use below
(assign, "$temp", ":player_pick_renown_per_center_point"),
(assign, "$temp_2", ":other_pick_renown_per_center_point"),

(store_mul, ":threshhold", ":average_renown_per_point", 3),
(val_div, ":threshhold", 4),
(lt, ":player_pick_renown_per_center_point", ":threshhold"),
(str_store_troop_name, s4, "$lord_selected"),
(call_script, "script_dplmc_store_troop_is_female_reg", "$lord_selected", 3),
],
"{s4} has already been well-rewarded with fiefs appropriate to {reg3?her:his} accomplishments, I would say.", "lord_pretalk",
[
]],
[anyone,"dplmc_lord_internal_politics_plyr_request_support_2", [
#for marshall, fail if the target's renown is too low
(faction_slot_eq, "$players_kingdom", slot_faction_political_issue, 1),
(troop_get_slot, ":player_pick_renown", "$lord_selected", slot_troop_renown),
(lt, ":player_pick_renown", 400),
(str_store_troop_name, s4, "$lord_selected"),
(assign, reg3, 0),
(try_begin),
	(call_script, "script_cf_dplmc_troop_is_female", "$lord_selected"),
	(assign, reg3, 1),
(try_end),
(try_begin),
	(ge, "$cheat_mode", 1),
	(assign, reg0, ":player_pick_renown"),
	(str_store_string, s0, "str_score_reg0"),
	(assign, reg0, 400),
	(str_store_string, s1, "str_score_reg0"),
	(display_message, "@{!}DEBUG support check, {s4} {s0}, Threshold {s1}"),
(try_end),
],
"I think {s4} would need to prove {reg3?herself:himself} further before {reg3?she:he} is eligible for that position.", "lord_pretalk",
[
]],
[anyone,"dplmc_lord_internal_politics_plyr_request_support_2", [
#for fiefs, fail if the target's renown per the center point is bad compared to the previous pick's
(faction_get_slot, ":faction_issue", "$players_kingdom", slot_faction_political_issue),
(is_between, ":faction_issue", centers_begin, centers_end),
(troop_get_slot, ":other_pick", "$g_talk_troop", slot_troop_stance_on_faction_issue),
(gt, ":other_pick", -1),
#load values calculated above
(assign, ":player_pick_renown_per_center_point", "$temp"),
(assign, ":threshold", "$temp_2"),#other_pick_renown_per_center_point
(val_mul, ":threshold", 3),
(val_div, ":threshold", 4),
(lt, ":player_pick_renown_per_center_point", ":threshold"),
(str_store_troop_name, s3, ":other_pick"),
(str_store_troop_name, s4, "$lord_selected"),
(try_begin),
	(ge, "$cheat_mode", 1),
	(assign, reg0, ":player_pick_renown_per_center_point"),
	(str_store_string, s0, "str_score_reg0"),
	(assign, reg0, ":threshold"),
	(str_store_string, s1, "str_score_reg0"),
	(display_message, "@{!}DEBUG support check, {s4} {s0}, Threshold {s1}"),
(try_end),
(str_store_party_name, s0, ":faction_issue"),
],
"{s3} deserves to receive {s0} more than {s4}, I would say.", "lord_pretalk",
[
]],
[anyone,"dplmc_lord_internal_politics_plyr_request_support_2", [
#for marshall, fail if the target's renown is too low compared to existing pick
(faction_slot_eq, "$players_kingdom", slot_faction_political_issue, 1),
(troop_get_slot, ":other_pick", "$g_talk_troop", slot_troop_stance_on_faction_issue),
(gt, ":other_pick", -1),

(troop_get_slot, ":player_pick_renown", "$lord_selected", slot_troop_renown),
(troop_get_slot, ":threshold", ":other_pick", slot_troop_renown),
(val_mul, ":threshold", 3),
(val_div, ":threshold", 4),
(lt, ":player_pick_renown", ":threshold"),

(str_store_troop_name, s4, "$lord_selected"),
(assign, reg3, 0),
(try_begin),
	(call_script, "script_cf_dplmc_troop_is_female", "$lord_selected"),
	(assign, reg3, 1),
(try_end),
(try_begin),
	(ge, "$cheat_mode", 1),
	(assign, reg0, ":player_pick_renown"),
	(str_store_string, s0, "str_score_reg0"),
	(assign, reg0, ":threshold"),
	(str_store_string, s1, "str_score_reg0"),
	(display_message, "@{!}DEBUG support check, {s4} {s0}, Threshold {s1}"),
(try_end),
],
"I think {s4} would need to prove {reg3?herself:himself} further before {reg3?she:he} is eligible for that position.", "lord_pretalk",
[
]],
[anyone,"dplmc_lord_internal_politics_plyr_request_support_2", [
(call_script, "script_troop_get_relation_with_troop", "$g_talk_troop", "$lord_selected"),
(assign, ":player_pick_unaltered_relation", reg0),
(assign, ":player_pick_relation", reg0),
#if the one being addressed is much more fond of the player than the suggested
#candidate *and* the currently-preferred candidate, this can provide some
#advantage.  the advantage is a portion of the relationship difference.
(assign, ":relation_modifier", 0),
(troop_get_slot, ":other_pick", "$g_talk_troop", slot_troop_stance_on_faction_issue),
(assign, ":other_pick_relation", 0),
(try_begin),
	(gt, ":other_pick", -1),
	(neq, ":other_pick", "trp_player"),
	(call_script, "script_troop_get_relation_with_troop", "$g_talk_troop", ":other_pick"),
	(assign, ":other_pick_relation", reg0),
(try_end),
(try_begin),
	(val_max, reg0, ":player_pick_relation"),#higher of the lord's relations with his pick or the suggested pick
	(val_max, reg0, 0),
	#relation with player is greater than that with both suggested lord and currently-picked lord
	(gt, "$g_talk_troop_relation", reg0),
	#add 1/10th of the difference, rounded up
	(store_sub, ":relation_modifier", "$g_talk_troop_relation", reg0),
	(val_add, ":relation_modifier", 5),
	(val_div, ":relation_modifier", 10),
(try_end),
#alter effective relation using player's persuasion, then apply the relation modifier
(store_skill_level, ":persuasion", "skl_persuasion", "trp_player"),
(val_add, ":player_pick_relation", ":persuasion"),
(try_begin),
   (gt, ":player_pick_relation", 0),
   (val_add, ":player_pick_relation", ":relation_modifier"),#add before multiplication
   (store_add, ":persuasion_modifier", 10, ":persuasion"),
   (val_mul, ":player_pick_relation", ":persuasion_modifier"),
   (val_div, ":player_pick_relation", 10),
(else_try),
   (lt, ":player_pick_relation", 0),
   (store_sub, ":persuasion_modifier", 20, ":persuasion"),
   (val_mul, ":player_pick_relation", ":persuasion_modifier"),
   (val_div, ":player_pick_relation", 20),
   (val_add, ":player_pick_relation", ":relation_modifier"),#add after multiplication
(try_end),
(assign, "$temp", ":player_pick_relation"),#<-- store to $temp, overwrites reknown/center if it was there
#Reject with derogatory comment if relation with candidate is still negative after modification
#or if it was negative before modification and was not enough to surpass the new candidate.
(this_or_next|lt, "$temp", 0),
	(ge, ":other_pick_relation", "$temp"),
(lt, ":player_pick_unaltered_relation", 0),

(call_script, "script_lord_comment_to_s43", "$g_talk_troop", "str_lord_insult_default"),
(str_store_troop_name, s4, "$lord_selected"),
(str_store_string, s1, "str_dplmc_refuse_support_s43_named_s4"),
],
"{s1}", "lord_pretalk",
[
]],
[anyone,"dplmc_lord_internal_politics_plyr_request_support_2", [
#reject if relations don't meet the normal threshold with either the player or the target
(lt, "$temp", 10),#<-- persuasion-modified relation to $lord_selected
(lt, "$g_talk_troop_effective_relation", 10),
],
"Hmm... That is too much to ask, given the state of my relationship with the two of you.", "lord_pretalk",
[
]],
[anyone,"dplmc_lord_internal_politics_plyr_request_support_2", [
(troop_get_slot, ":other_pick", "$g_talk_troop", slot_troop_stance_on_faction_issue),
(gt, ":other_pick", -1),
(assign, ":player_pick_relation", "$temp"),#load persuasion-modified relation from variable
#compare to relation with other choice
(call_script, "script_troop_get_relation_with_troop", "$g_talk_troop", ":other_pick"),
(ge, reg0, ":player_pick_relation"),
(assign, ":other_pick_relation", reg0),
#don't make this comment if the lord's supported candidate actually favors the player's pick
(troop_get_slot, reg0, ":other_pick", slot_troop_stance_on_faction_issue),
(neq, reg0, "$lord_selected"),
#also don't make this comment if the other candidate is the player
(neq, ":other_pick", "trp_player"),
(str_store_troop_name, s4, ":other_pick"),
(try_begin),
	(ge, "$cheat_mode", 1),
	(assign, reg0, ":player_pick_relation"),
	(str_store_troop_name, s3, "$lord_selected"),#s3 not s4
	(str_store_string, s0, "str_score_reg0"),
	(assign, reg0, ":other_pick_relation"),
	(str_store_string, s1, "str_score_reg0"),
	(display_message, "@{!}DEBUG support check, {s3} {s0}, Threshold {s1}"),#s3 not s4
(try_end),
],
"I am sorry. I would not wish to strain my relationship with {s4}", "lord_pretalk",
[
]],
[anyone, "dplmc_lord_internal_politics_plyr_request_support_2", [
(str_store_troop_name, s4, "$lord_selected"),
],#if no objection, succeed
"I will gladly support {s4}.", "lord_pretalk",
[(troop_set_slot, "$g_talk_troop", slot_troop_stance_on_faction_issue, "$lord_selected"),
#The player is now committed as a supporter of his candidate if he wasn't already
(troop_set_slot, "trp_player", slot_troop_stance_on_faction_issue, "$lord_selected"),
]
],
[anyone|plyr,"dplmc_lord_ask_pardon_ruler_1",
[
(assign, ":valid_demand", 0),
(assign, ":money_alone", "$temp",),
(assign, ":money_and_fief", "$temp_2",),
(assign, ":needed_gold", 0),

#Store demand string to s0
(try_begin),
	#A fief and mon
	(ge, ":money_and_fief", 1),
	(ge, "$g_concession_demanded", 1),
	(str_store_party_name, s0, "$g_concession_demanded"),
	(assign, reg1, ":money_and_fief"),
	(str_store_string, s1, "str_reg1_denars"),
	(str_store_string, s0, "str_dplmc_s0_and_s1"),
	(assign, ":needed_gold", ":money_and_fief"),
	(assign, ":valid_demand", 1),
(else_try),
	#Just a fief
	(ge, "$g_concession_demanded", 1),
	(str_store_party_name, s0, "$g_concession_demanded"),
	(assign, ":needed_gold", 0),
	(assign, ":valid_demand", 1),
(else_try),
	#Just mon
	(neq, reg0, 1),
	(assign, reg1, ":money_alone"),
	(str_store_string, s0, "str_reg1_denars"),
	(assign, ":valid_demand", 1),
	(assign, ":needed_gold", ":money_alone"),
(try_end),

(assign, "$temp", ":valid_demand"),
(assign, "$temp_2", ":needed_gold"),

(eq, ":valid_demand", 1),
(store_troop_gold, ":player_gold", "trp_player"),
(ge, ":player_gold", ":needed_gold"),
],
"I accept.  I will give you {s0}, and let there be peace.","close_window", [
(assign, ":gold", "$temp_2"),

(troop_remove_gold, "trp_player", ":gold"),
(call_script, "script_dplmc_faction_leader_splits_gold", "$g_talk_troop_faction", ":gold"),

(try_begin),
	(ge, "$g_concession_demanded", 1),
	(call_script, "script_give_center_to_faction", "$g_concession_demanded", "$g_talk_troop_faction"),
(try_end),
	(call_script, "script_diplomacy_start_peace_between_kingdoms", "$g_talk_troop_faction", "$players_kingdom", 1),
	##zerilius changes begin
	(eq,"$talk_context",tc_party_encounter),
	(assign, "$g_leave_encounter", 1),
	##zerilius changes end
]],
[anyone|plyr,"dplmc_lord_ask_pardon_ruler_1",
[
(assign, ":valid_demand", "$temp",),
(assign, ":needed_gold", "$temp_2",),
(eq, ":valid_demand", 1),

(store_troop_gold, ":player_gold", "trp_player"),
(lt, ":player_gold", ":needed_gold"),
(assign, reg1, ":needed_gold"),
(str_store_string, s0, "str_reg1_denars"),
], "I don't have {s0} with me.", "dplmc_lord_ask_pardon_ruler_2a",
[]],
[anyone, "dplmc_lord_ask_pardon_ruler_2a", [],
	"In that case, the war will continue.", "lord_pretalk",[]],
[anyone|plyr,"dplmc_lord_ask_pardon_ruler_1",
[], "On second thought, such an accord would not be in my interests.", "lord_pretalk",[]],
[anyone, "dplmc_lord_ask_exchange_fief_1",
 [(lt, "$g_talk_troop_effective_relation", 0),
  (str_store_string, s19, "str_dplmc_fief_exchange_not_interested"),
  ],
 "{s19}", "lord_pretalk", [],
 ],
[anyone, "dplmc_lord_ask_exchange_fief_1",
   [#(faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, "$g_talk_troop"),
  	 (call_script, "script_dplmc_get_troop_standing_in_faction", "$g_talk_troop", "$g_talk_troop_faction"),
	 (ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
    (str_store_string, s19, "str_dplmc_fief_exchange_listen"),],
   "{s19}", "dplmc_lord_exchange_fief_select_1",
   [],
],
[anyone, "dplmc_lord_ask_exchange_fief_1",
   [(faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, "trp_player"),
    (str_store_string, s19, "str_dplmc_fief_exchange_listen_player_approval"),],
    "{s19}", "dplmc_lord_exchange_fief_select_1",
    [],
],
[anyone, "dplmc_lord_ask_exchange_fief_1",
   [#(eq, "$g_talk_troop_faction", "$players_kingdom"),
    #load name of king
    (faction_get_slot, ":faction_leader","$g_talk_troop_faction",slot_faction_leader),
    (str_store_troop_name, s10, ":faction_leader"),
    (str_store_string, s19, "str_dplmc_fief_exchange_listen_s10_approval"),
   ],
   "{s19}", "dplmc_lord_exchange_fief_select_1",
   [],
],
[anyone|plyr|repeat_for_parties, "dplmc_lord_exchange_fief_select_1",
[
(store_repeat_object, ":center_no"),
(is_between, ":center_no", centers_begin, centers_end),
(neg|party_slot_eq, ":center_no", slot_village_infested_by_bandits, "trp_peasant_woman"),
(party_slot_eq, ":center_no", slot_town_lord, "$g_talk_troop"),
(str_store_party_name, s1, ":center_no"),

],"{s1}", "dplmc_lord_exchange_fief_select_2",
[
(store_repeat_object, "$fief_selected"),
]],
[anyone|plyr, "dplmc_lord_exchange_fief_select_1",
[
],"Never mind", "lord_pretalk",
[]],
[anyone, "dplmc_lord_exchange_fief_select_2", [
   (str_store_string, s19, "str_dplmc_fief_exchange_listen_2"),
    ],
   "{s19}", "dplmc_lord_exchange_fief_select_2",
   [],
],
[anyone|plyr|repeat_for_parties, "dplmc_lord_exchange_fief_select_2",
[
(store_repeat_object, ":center_no"),
(is_between, ":center_no", centers_begin, centers_end),
(neg|party_slot_eq, ":center_no", slot_village_infested_by_bandits, "trp_peasant_woman"),
(party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
(str_store_party_name, s1, ":center_no"),

],"{s1}", "dplmc_lord_exchange_fief_select_3",
[
(store_repeat_object, "$diplomacy_var"),
]],
[anyone|plyr, "dplmc_lord_exchange_fief_select_2",
[
],"Never mind", "lord_pretalk",
[]],
[anyone, "dplmc_lord_exchange_fief_select_3", [
    (call_script, "script_dplmc_evaluate_fief_exchange", "$g_talk_troop","$fief_selected","trp_player","$diplomacy_var"),
    #Result stored in reg0, reason string stored in s14
    (ge, reg0, 0),
    (assign, reg3, reg0),
     ],
   "{s14}", "dplmc_lord_exchange_fief_confirm",
   [],
],
[anyone, "dplmc_lord_exchange_fief_select_3", [
    #Call this again to make sure s14 and reg0 have the right values,
    #but don't actually use reg0 for anything (if it is non-negative, that means
    #script_dplmc_evaluate_fief_exchange is bugged and producing inconsistent results)
    (call_script, "script_dplmc_evaluate_fief_exchange", "$g_talk_troop","$fief_selected","trp_player","$diplomacy_var"),
     ],
   "{s14}", "lord_pretalk",
   [],
],
[anyone|plyr,"dplmc_lord_exchange_fief_confirm", [
    #Call this again to make sure s14 and reg0 have the right values
    (call_script, "script_dplmc_evaluate_fief_exchange", "$g_talk_troop","$fief_selected","trp_player","$diplomacy_var"),
    #Result stored in reg0, reason string stored in s14
    (ge, reg0, 0),
    (assign, reg3, reg0),
    #Make sure the player can afford the cost if it's above zero
    (store_troop_gold, ":gold", "trp_player"),
    (ge, ":gold", reg3),
    #Set string appropriately
    (try_begin),
       (ge, reg3, 1),
       (str_store_string, s14, "str_dplmc_fief_exchange_confirm_reg3_denars"),
    (else_try),
       (str_store_string, s14, "str_dplmc_fief_exchange_confirm"),
    (try_end),
    ],
 "{s14}", "lord_pretalk",
 [#Consequence block
(assign, ":push_g_move_heroes", "$g_move_heroes"),#revert this at the end of the script
(assign, "$g_move_heroes", 1),
 (try_begin),
 (assign, ":from_lord_fief", "$fief_selected"), #fief to give to player
 (assign, ":from_player_fief", "$diplomacy_var"), #fief to give to lord
  #Call this again to make sure s14 and reg0 have the right values
  (call_script, "script_dplmc_evaluate_fief_exchange", "$g_talk_troop",":from_lord_fief","trp_player",":from_player_fief"),
  #Result stored in reg0, reason string stored in s14
  #Remove gold
  (try_begin),
     (assign, ":gold_cost", reg0),
     (ge, ":gold_cost", 1),
     (troop_remove_gold, "trp_player", ":gold_cost"),
     #add gold to lord
     (call_script, "script_dplmc_distribute_gold_to_lord_and_holdings", ":gold_cost", "$g_talk_troop"),
  (try_end),
  #Exchange fiefs
  #(call_script, "script_give_center_to_lord", "$diplomacy_var", "$g_talk_troop", 0),
  #(call_script, "script_give_center_to_lord", "$fief_selected", "trp_player", 0),
  #Don't use those scripts, as they have some unwanted side-effects.

#is the lord's old fief walled (i.e. can it potentially have a garrison)
(assign, ":from_lord_fief_walled", 0),
 (try_begin),
    (is_between, ":from_lord_fief", walled_centers_begin, walled_centers_end),
   (assign, ":from_lord_fief_walled", 1),
  (try_end),
 #is the player's old fief walled (i.e. can it potentially have a garrison)
 (assign, ":from_player_fief_walled", 0),
 (try_begin),
    (is_between, ":from_player_fief", walled_centers_begin, walled_centers_end),
   (assign, ":from_player_fief_walled", 1),
  (try_end),

 #To avoid exploitative use of this, the lords take their garrisons and prisoners with them
 (party_clear, "p_temp_party"),#contains lord's old center's garrison and prisoners
(party_clear, "p_temp_party_2"),#contains player's old center's garrison and prisoners

(try_begin),
   (eq, ":from_lord_fief_walled", 1),
   (call_script, "script_party_add_party", "p_temp_party", ":from_lord_fief"),
   (party_clear, ":from_lord_fief"),
(try_end),

(try_begin),
   (eq, ":from_player_fief_walled", 1),
   (call_script, "script_party_add_party", "p_temp_party_2", ":from_player_fief"),
   (party_clear, ":from_player_fief"),
(try_end),

  #Remove player fief and assign it to the lord
  (assign, ":give_fief", ":from_player_fief"),
  (assign, ":to_lord", "$g_talk_troop"),
  #Reset fief properties
  (party_set_slot, ":give_fief", dplmc_slot_center_taxation, 0),
  (try_begin),
     (party_slot_eq, ":give_fief", slot_village_infested_by_bandits, "trp_peasant_woman"),
     (party_set_slot, ":give_fief", slot_village_infested_by_bandits, 0),
  (try_end),
  (try_begin),
      #Reset banner if applicable
      (is_between, ":give_fief", walled_centers_begin, walled_centers_end),
      (troop_get_slot, ":cur_banner", ":to_lord", slot_troop_banner_scene_prop),
      (gt, ":cur_banner", 0),
      (val_sub, ":cur_banner", banner_scene_props_begin),
      (val_add, ":cur_banner", banner_map_icons_begin),
      (party_set_banner_icon, ":give_fief", ":cur_banner"),
  (try_end),
  #transfer to lord
  (party_set_slot, ":give_fief", slot_town_lord, ":to_lord"),
  (call_script, "script_update_center_notes", ":give_fief"),

  #Now remove lord fief and assign it to the player
  (assign, ":give_fief", ":from_lord_fief"),
  (assign, ":to_lord", "trp_player"),
  #Reset fief properties
  (party_set_slot, ":give_fief", dplmc_slot_center_taxation, 0),
  (try_begin),
     (party_slot_eq, ":give_fief", slot_village_infested_by_bandits, "trp_peasant_woman"),
     (party_set_slot, ":give_fief", slot_village_infested_by_bandits, 0),
  (try_end),
  (try_begin),
      #Reset banner if applicable
      (is_between, ":give_fief", walled_centers_begin, walled_centers_end),
      (troop_get_slot, ":cur_banner", ":to_lord", slot_troop_banner_scene_prop),
      (gt, ":cur_banner", 0),
      (val_sub, ":cur_banner", banner_scene_props_begin),
      (val_add, ":cur_banner", banner_map_icons_begin),
      (party_set_banner_icon, ":give_fief", ":cur_banner"),
  (try_end),
  #transfer to lord
  (party_set_slot, ":give_fief", slot_town_lord, ":to_lord"),
  (call_script, "script_update_center_notes", ":give_fief"),

  #Player's troops transfer to new fief if possible
 #and lord's troops transfer to new fief if possible
  (try_begin),
   (eq, ":from_player_fief_walled", 1),
   (eq, ":from_lord_fief_walled", 1),
   (call_script, "script_party_add_party", ":from_lord_fief", "p_temp_party_2"),
   (call_script, "script_party_add_party", ":from_player_fief", "p_temp_party"),
  (else_try),
   (eq, ":from_player_fief_walled", 1),
   (neq, ":from_lord_fief_walled", 1),
   (call_script, "script_party_add_party", ":from_player_fief", "p_temp_party_2"),
   (call_script, "script_party_add_party", ":from_player_fief", "p_temp_party"),
  (else_try),
   #This exchange shouldn't happen, but handle it anyway.
   (neq, ":from_player_fief_walled", 1),
   (eq, ":from_lord_fief_walled", 1),
   (call_script, "script_party_add_party", ":from_lord_fief", "p_temp_party_2"),
   (call_script, "script_party_add_party", ":from_lord_fief", "p_temp_party"),
  (try_end),

  #Lord's troops transfer to new fief if possible

  #Final tasks
  (call_script, "script_update_troop_notes", "$g_talk_troop"),
  (call_script, "script_update_troop_notes", "trp_player"),
  (party_clear, "p_temp_party"),
  (party_clear, "p_temp_party_2"),
 #Display mesage
(str_store_troop_name, s1, "trp_player"),
(str_store_party_name, s2, "$diplomacy_var"),
(str_store_troop_name, s3, "$g_talk_troop"),
(str_store_party_name, s4, "$fief_selected"),
(display_log_message, "@{s1} exchanged {s2} to {s3} for {s4}."),
 (else_try),
    (display_message, "str_ERROR_string"),
 (try_end),
(assign, "$g_move_heroes", ":push_g_move_heroes"),#revert this at the end of the script
 ],
],
[anyone|plyr, "dplmc_lord_exchange_fief_confirm",
[
],"Actually, forget about this for now.", "lord_pretalk",
[]],
[anyone|plyr,"dplmc_claimant_marriage_proposal_pc_confirm", [
],
"Yes. That is my proposal.",
"dplmc_claimant_marriage_proposal_pc_reax",[
]],
[anyone|plyr,"dplmc_claimant_marriage_proposal_pc_confirm", [
],
"No, I think you have misunderstood me.  Forget I brought it up.",
"lord_pretalk",[
]],
[anyone|plyr,"dplmc_claimant_marriage_proposal_pc_confirm", [
#It's possible the player did not intend this
(lt, "$g_disable_condescending_comments", 2),
(eq, reg65, "$character_gender"),
],
"Oh, HELL no!  No, you totally have the wrong idea... forget I said anything.",
"lord_pretalk",[
]],
[anyone, "dplmc_claimant_marriage_proposal_pc_reax", [
	#This probably can't occur, but make sure.
	(this_or_next|troop_slot_eq,"$g_talk_troop", slot_troop_betrothed, "trp_player"),
	(troop_slot_eq, "trp_player", slot_troop_betrothed, "$g_talk_troop"),
], "Have no fear, I have no intention of changing my mind.  We will be married as soon as there is an opportunity worthy of the august event.", "lord_pretalk", []],
[anyone, "dplmc_claimant_marriage_proposal_pc_reax", [
	#The claimant must not be married.  This probably can't occur, but make sure.
	(troop_get_slot, ":spouse", "$g_talk_troop", slot_troop_spouse),
	(ge, ":spouse", 0),
	(str_store_troop_name, s0, ":spouse"),#This probably can't occur, but make sure.
], "Unfortunately this is impossible, since I am already married to {s0}.", "lord_pretalk", []],
[anyone, "dplmc_claimant_marriage_proposal_pc_reax", [
	#The player must not be married.  This probably can't occur, but make sure.
	(troop_get_slot, ":spouse", "trp_player", slot_troop_spouse),
	(ge, ":spouse", 1),
	(str_store_troop_name, s0, ":spouse"),
], "Unfortunately this is impossible, since you are already married to {s0}.", "lord_pretalk", []],
[anyone, "dplmc_claimant_marriage_proposal_pc_reax", [
	#The claimant must not be engaged.  This probably can't occur, but make sure.
	(troop_get_slot, ":betrothed", "$g_talk_troop", slot_troop_betrothed),
	(ge, ":betrothed", 0),
	(str_store_troop_name, s0, ":betrothed"),
], "Unfortunately this is impossible, since I am already engaged to {s0}.", "lord_pretalk", []],
[anyone, "dplmc_claimant_marriage_proposal_pc_reax", [
	#The player must not be engaged.  This probably can't occur, but make sure.
	(troop_get_slot, ":betrothed", "trp_player", slot_troop_betrothed),
	(ge, ":betrothed", 1),
	(str_store_troop_name, s0, ":betrothed"),
], "Unfortunately this is impossible, since you are already engaged to {s0}.", "lord_pretalk", []],
[anyone, "dplmc_claimant_marriage_proposal_pc_reax", [
	(assign, reg0, -1),
	(str_store_string, s14, "str_ERROR_string"),
	(try_begin),
		(call_script, "script_cf_dplmc_evaluate_pretender_proposal", "$g_talk_troop"),
	(try_end),
	(lt, reg0, 1),
], "{s14}", "lord_pretalk", []],
[anyone,"dplmc_claimant_marriage_proposal_pc_reax", [
],
"{s14}",
"lord_marriage_proposal_female_pc_confirm_engagement",#jump to confirm engagement dialogue (despite the name, it is now unisex)
[]],
[anyone,"dplmc_prisoner_chat_let_go", [],
  "{s43}", "close_window", [
   (call_script, "script_lord_comment_to_s43", "$g_talk_troop", "str_prisoner_released_default"),
   (party_remove_prisoners, "$current_town", "$g_talk_troop",1),
	#Ensure the freeing works properly.
	(try_begin),
		(party_count_prisoners_of_type, ":holding_as_prisoner",  "$current_town", "$g_talk_troop"),
		(gt, ":holding_as_prisoner", 0),
		(party_remove_prisoners, "$g_encountered_party", "$g_talk_troop", 1),
	(else_try),
		(party_count_prisoners_of_type, ":holding_as_prisoner",  "p_main_party", "$g_talk_troop"),
		(gt, ":holding_as_prisoner", 0),
		(party_remove_prisoners, "p_main_party", "$g_talk_troop", 1),
	(else_try),
		(troop_get_slot, ":captor_party", "$g_talk_troop", slot_troop_prisoner_of_party),
		(ge, ":captor_party", 0),
		(party_count_prisoners_of_type, ":holding_as_prisoner",  ":captor_party", "$g_talk_troop"),
		(gt, ":holding_as_prisoner", 0),
		(party_remove_prisoners, ":captor_party", "$g_talk_troop", 1),
	(try_end),

	(troop_set_slot, "$g_talk_troop", slot_troop_prisoner_of_party, -1),
	#close any open quests
	(call_script, "script_remove_troop_from_prison", "$g_talk_troop"),
	(str_store_troop_name, s7, "$g_talk_troop"),
	(display_message, "str_dplmc_has_been_set_free"),
      ]],
[anyone,"dplmc_spouse_tournament_dedication_reaction", [],
   "{s9}", "spouse_pretalk",
   []],
[anyone,"dplmc_lady_relations2",
   [],
   "About which lord do you want information?", "dplmc_lady_info_relative_select",[
 ]],
[anyone|plyr|repeat_for_troops, "dplmc_lady_info_relative_select",
   [
    (store_repeat_object, ":troop_no"),
    (neq, "$g_talk_troop", ":troop_no"),
    (is_between, ":troop_no", active_npcs_begin, kingdom_ladies_end),
    (neq, ":troop_no", "trp_player"),#don't talk about the player
    (neq, ":troop_no", "$g_talk_troop"),#don't talk about yourself
    (troop_slot_ge, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
    (neg|troop_slot_ge, ":troop_no", slot_troop_occupation, slto_inactive_pretender),
    (neg|troop_slot_eq, ":troop_no", slot_troop_occupation, slto_retirement),
    #Only give info on relatives
    (call_script, "script_troop_get_family_relation_to_troop", ":troop_no", "$g_talk_troop"),
    (assign, ":relation_strength", reg0),
    (ge, ":relation_strength", 2),#2+: cousin, niece
    (str_store_troop_name, s18, ":troop_no"),
   ], "Your {s11} {s18}", "dplmc_lady_info_relative_1",
   [
      (store_repeat_object, "$lord_selected"),
   ]],
[anyone|plyr, "dplmc_lady_info_relative_select",
   [
   ],
   "Never mind.", "lady_pretalk",[
 ]],
[anyone,"dplmc_lady_info_relative_1",
   [(lt,"$g_talk_troop_effective_relation",0),
       ],
   "Pardon, but I do not feel comfortable discussing such personal matters with you.", "lady_pretalk",[
 ]],
[anyone,"dplmc_lady_info_relative_1",
   [
    (call_script, "script_dplmc_troop_political_notes_to_s47", "$lord_selected"),
   ],
   "{s47}", "dplmc_lady_info_relative_2",[
 ]],
[anyone,"dplmc_lady_info_relative_1",
   [
    (is_between,"$lord_selected",kingdom_ladies_begin,kingdom_ladies_end),
    (troop_slot_eq, "$lord_selected", slot_troop_spouse, -1),
    (assign,":lady","$lord_selected"),
	(troop_get_slot, ":betrothed", ":lady", slot_troop_betrothed),
	(is_between, ":betrothed", active_npcs_begin, active_npcs_end),

	(str_store_troop_name, s9, ":lady"),
	(str_store_troop_name, s11, ":betrothed"),

	(str_store_string, s12, "str_s9_is_now_betrothed_to_s11_soon_we_believe_there_shall_be_a_wedding"),
	(try_begin),
		(troop_slot_eq, ":lady", slot_troop_met, 2),
		(assign, "$romantic_rival", ":betrothed"),
	(try_end),
   ],
   "{12}", "lady_pretalk",[
 ]],
[anyone,"dplmc_lady_info_relative_2",
   [
    (is_between,"$lord_selected",kingdom_ladies_begin,kingdom_ladies_end),
    (assign, "$lady_selected", "$lord_selected"),
    (try_begin),
	    (str_store_string, s12, "str_i_have_not_heard_any_news_about_her"),

		(str_store_troop_name, s9, "$lady_selected"), #lady

		(try_begin),
			(eq, "$cheat_mode", 1), #for some reason, speaking to tavern merchant does not yield rumor. Try for Lady Baoth, Lord Etr
			(display_message, "str_searching_for_rumors_for_s9"),
		(try_end),

		(assign, "$romantic_rival", -1),
		(assign, ":last_lady_noted", 0),
		(try_for_range, ":log_entry", 0, "$num_log_entries"),
			(troop_slot_eq, "trp_log_array_actor", ":log_entry", "$lady_selected"),


			#Presumably possible for some events involving a lady to not involve troops
			(troop_get_slot, ":suitor", "trp_log_array_troop_object", ":log_entry"),
			(str_clear, s11),
			(try_begin),
				(is_between, ":suitor", 0, kingdom_ladies_end),
				(str_store_troop_name, s11, ":suitor"),
			(try_end),

			(troop_get_slot, ":third_party", "trp_log_array_center_object", ":log_entry"),
			(str_clear, s10),
			(try_begin),
				(is_between, ":third_party", 0, kingdom_ladies_end),
				(str_store_troop_name, s10, ":third_party"),
			(try_end),

			(assign, ":lady", "$lady_selected"),

			(try_begin),
				(troop_slot_eq, "trp_log_array_entry_type",  ":log_entry", logent_lady_favors_suitor),
				(str_store_string, s12, "str_they_say_that_s9_has_shown_favor_to_s11_perhaps_it_will_not_be_long_until_they_are_betrothed__if_her_family_permits"),
				(assign, ":last_lady_noted", ":lady"),
				(assign, ":last_suitor_noted", ":suitor"),

				(try_begin),
					(troop_slot_eq, ":lady", slot_troop_met, 2),
					(this_or_next|troop_slot_eq, ":suitor", slot_troop_love_interest_1, ":lady"),
					(this_or_next|troop_slot_eq, ":suitor", slot_troop_love_interest_2, ":lady"),
						(troop_slot_eq, ":suitor", slot_troop_love_interest_3, ":lady"),

					(assign, "$romantic_rival", ":suitor"),
				(try_end),
			(else_try),
				(troop_slot_eq, "trp_log_array_entry_type",  ":log_entry", logent_lady_betrothed_to_suitor_by_family),
				(str_store_string, s12, "str_they_say_that_s9_has_been_forced_by_her_family_into_betrothal_with_s11"),
				(assign, ":last_lady_noted", ":lady"),
				(assign, ":last_suitor_noted", ":suitor"),

				(try_begin),
					(troop_slot_eq, ":lady", slot_troop_met, 2),
					(assign, "$romantic_rival", ":suitor"),
				(try_end),
			(else_try),
				(troop_slot_eq, "trp_log_array_entry_type",  ":log_entry", logent_lady_betrothed_to_suitor_by_choice),
				(str_store_string, s12, "str_they_say_that_s9_has_agreed_to_s11s_suit_and_the_two_are_now_betrothed"),
				(assign, ":last_lady_noted", ":lady"),
				(assign, ":last_suitor_noted", ":suitor"),

				(try_begin),
					(troop_slot_eq, ":lady", slot_troop_met, 2),
					(this_or_next|troop_slot_eq, ":suitor", slot_troop_love_interest_1, ":lady"),
					(this_or_next|troop_slot_eq, ":suitor", slot_troop_love_interest_2, ":lady"),
						(troop_slot_eq, ":suitor", slot_troop_love_interest_3, ":lady"),


					(assign, "$romantic_rival", ":suitor"),
				(try_end),

			(else_try),
				(troop_slot_eq, "trp_log_array_entry_type",  ":log_entry", logent_lady_betrothed_to_suitor_by_pressure),
				(str_store_string, s12, "str_they_say_that_s9_under_pressure_from_her_family_has_agreed_to_betrothal_with_s11"),
				(assign, ":last_lady_noted", ":lady"),
				(assign, ":last_suitor_noted", ":suitor"),

				(try_begin),
					(troop_slot_eq, ":lady", slot_troop_met, 2),
					(this_or_next|troop_slot_eq, ":suitor", slot_troop_love_interest_1, ":lady"),
					(this_or_next|troop_slot_eq, ":suitor", slot_troop_love_interest_2, ":lady"),
						(troop_slot_eq, ":suitor", slot_troop_love_interest_3, ":lady"),

					(assign, "$romantic_rival", ":suitor"),
				(try_end),

			(else_try),

				(troop_slot_eq, "trp_log_array_entry_type",  ":log_entry", logent_lady_rejects_suitor),
				(str_store_string, s12, "str_they_say_that_s9_has_refused_s11s_suit"),
				(assign, ":last_lady_noted", ":lady"),
				(assign, ":last_suitor_noted", ":suitor"),

			(else_try),

				(troop_slot_eq, "trp_log_array_entry_type",  ":log_entry", logent_lady_rejected_by_suitor),
				(str_store_string, s12, "str_they_say_that_s11_has_tired_of_pursuing_s9"),
				(assign, ":last_lady_noted", ":lady"),
				(assign, ":last_suitor_noted", ":suitor"),


			(else_try),
				(troop_slot_eq, "trp_log_array_entry_type",  ":log_entry", logent_lady_father_rejects_suitor),
				(str_store_string, s12, "str_they_say_that_s9s_family_has_forced_her_to_renounce_s11_whom_she_much_loved"),
				(assign, ":last_lady_noted", ":lady"),
				(assign, ":last_suitor_noted", ":suitor"),

			(else_try),
				(troop_slot_eq, "trp_log_array_entry_type",  ":log_entry", logent_lady_elopes_with_lord),
				(str_store_string, s12, "str_they_say_that_s9_has_run_away_with_s11_causing_her_family_much_grievance"),
				(assign, ":last_lady_noted", ":lady"),
				(assign, ":last_suitor_noted", ":suitor"),

			(else_try),
				(troop_slot_eq, "trp_log_array_entry_type",  ":log_entry", logent_lady_marries_lord),
				(str_store_string, s12, "str_they_say_that_s9_and_s11_have_wed"),
				(assign, ":last_lady_noted", ":lady"),
				(assign, ":last_suitor_noted", ":suitor"),
			(else_try),
				(troop_get_slot, ":suitor", ":lady", slot_lady_last_suitor),
				(is_between, ":suitor", active_npcs_begin, active_npcs_end),
				(str_store_troop_name, s11, ":suitor"),

				(str_store_string, s12, "str_they_say_that_s9_was_recently_visited_by_s11_who_knows_where_that_might_lead"),
				(assign, ":last_lady_noted", ":lady"),
				(assign, ":last_suitor_noted", ":suitor"),
				(try_begin),
					(troop_slot_eq, ":lady", slot_troop_met, 2),
					(this_or_next|troop_slot_eq, ":suitor", slot_troop_love_interest_1, ":lady"),
					(this_or_next|troop_slot_eq, ":suitor", slot_troop_love_interest_2, ":lady"),
						(troop_slot_eq, ":suitor", slot_troop_love_interest_3, ":lady"),

					(assign, "$romantic_rival", ":suitor"),
				(try_end),
			(try_end),

		(try_end),

		(try_begin),
			(neq, ":last_suitor_noted", "$romantic_rival"),
			(assign, "$romantic_rival", -1),
		(try_end),

		(try_begin),
			(gt, ":last_lady_noted", 0),
			(call_script, "script_add_rumor_string_to_troop_notes", ":last_lady_noted", ":last_suitor_noted", 12),
		(try_end),
	(else_try),
		(eq, "$lady_selected", -1),
		(str_store_string, s12, "str_there_is_not_much_to_tell_but_it_is_still_early_in_the_season"),
	(else_try),
		(assign, reg4, "$lady_selected"),
		(str_store_troop_name, s9, "$lady_selected"),
		(str_store_string, s12, "str_error_lady_selected_=_s9"),
	(try_end),
   ],
   "{s12}.",
   "lady_pretalk", []],
[anyone,"dplmc_lady_info_relative_2",
   [
     (call_script, "script_update_troop_location_notes", "$lord_selected", 1),
     (call_script, "script_get_information_about_troops_position", "$lord_selected", 0),
     ],
   "{s1}", "lady_pretalk",[]],
[anyone, "dplmc_lady_feasts", [

  (str_clear, s12),
  (assign, ":feast_found", 0),
  (try_for_range, ":kingdom", kingdoms_begin, kingdoms_end),
	##zerilius changes begin
	##Bug Fix since they tell about feasts of eliminated kingdoms also.
	(faction_slot_eq, ":kingdom", slot_faction_state, sfs_active),
	##zerilius changes end
	(faction_slot_eq, ":kingdom", slot_faction_ai_state, sfai_feast),
    (assign, ":feast_found", 1),

	(faction_get_slot, ":feast_venue", ":kingdom", slot_faction_ai_object),
	(str_store_party_name, s4, ":feast_venue"),
	(str_store_faction_name, s3, ":kingdom"),

	(store_current_hours, ":hour"),
	(store_sub, ":hours_since_start", ":hour", 72),
	(faction_get_slot, ":feast_time", ":kingdom", slot_faction_last_feast_start_time),
	(val_add, ":hours_since_start", ":feast_time"),

	(try_begin),
		(gt, ":hours_since_start", 48),
		(str_store_string, s12, "str_s12there_is_a_feast_of_the_s3_in_progress_at_s4_but_it_has_been_going_on_for_a_couple_of_days_and_is_about_to_end_"),
	(else_try),
		(gt, ":hours_since_start", 24),
		(str_store_string, s12, "str_s12there_is_a_feast_of_the_s3_in_progress_at_s4_which_should_last_for_at_least_another_day_"),
	(else_try),
		(str_store_string, s12, "str_s12there_is_a_feast_of_the_s3_in_progress_at_s4_which_has_only_just_begun_"),
	(try_end),
  (try_end),

  (try_begin),
    (eq, ":feast_found", 0),
	(str_store_string, s12, "str_not_at_this_time_no"),
  (else_try),
	(str_store_string, s12, "str_s12the_great_lords_bring_their_daughters_and_sisters_to_these_occasions_to_see_and_be_seen_so_they_represent_an_excellent_opportunity_to_make_a_ladys_acquaintance"),
  (try_end),

  ],
   "{s12}",
"lady_pretalk", []],
[anyone,"dplmc_prison_guard_talk_ask_prisoner",
   [],
   "Alright, which prisoner shall I set free?", "dplmc_prison_guard_talk_prisoner_select",[
 ]],
[anyone|plyr|repeat_for_troops, "dplmc_prison_guard_talk_prisoner_select",
   [
     (store_repeat_object, ":troop_no"),
     (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
     (troop_get_slot, ":party", ":troop_no", slot_troop_prisoner_of_party),
     (eq, ":party", "$g_encountered_party"),
     (str_store_troop_name, s10, ":troop_no"),
     (store_faction_of_troop, ":faction_no", ":troop_no"),
     (str_store_faction_name, s11, ":faction_no"),
     ],
   "{s10} of {s11}.", "dplmc_prison_guard_exchange_prisoner_ask_confirm",
   [
     (store_repeat_object, "$diplomacy_var"),
     (store_faction_of_troop, "$g_faction_selected", "$diplomacy_var"),
     ]],
[anyone|plyr,"dplmc_prison_guard_talk_prisoner_select", [],
   "No one.", "close_window",
   [
   ]],
[anyone,"dplmc_prison_guard_exchange_prisoner_ask_confirm",
   [
     (str_store_troop_name, s10, "$diplomacy_var"),
     (store_faction_of_troop, ":faction_no", "$diplomacy_var"),
     (str_store_faction_name, s11, ":faction_no"),
   ],
   "As you wish, I will release {s10} of {s11}.", "dplmc_prison_guard_exchange_prisoner_confirm",[
 ]],
[anyone|plyr,"dplmc_prison_guard_exchange_prisoner_confirm", [],
   "Very well.", "close_window",
   [
      (party_remove_prisoners, "$g_encountered_party", "$diplomacy_var", 1),
      (call_script, "script_remove_troop_from_prison", "$diplomacy_var"),
      (str_store_troop_name, s7, "$diplomacy_var"),
      (display_message, "str_dplmc_has_been_set_free"),
      (call_script, "script_change_player_relation_with_troop", "$diplomacy_var", 3),
      (call_script, "script_change_player_honor", 1),
      (call_script, "script_update_troop_notes", "$diplomacy_var"),
   ]],
[anyone|plyr,"dplmc_prison_guard_exchange_prisoner_confirm", [],
   "No, I changed my mind.", "close_window",[]],
[anyone, "dplmc_tavern_traveler_employee_1", [], "Maybe I can help you. Who are you looking for?", "dplmc_tavern_traveler_employee_2", []],
[anyone|plyr, "dplmc_tavern_traveler_employee_2",
[
#Check is chamberlain dismissed
(eq, "$g_player_chamberlain", -1),
(neg|troop_slot_eq, "trp_dplmc_chamberlain", slot_troop_met, 0),
#Check if chamberlain could return
(assign, ":player_center", centers_end),
(try_for_range, ":center_no", centers_begin, ":player_center"),
   (party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
   (assign, ":player_center", ":center_no"),#set result and break loop
(try_end),
(is_between, ":player_center", centers_begin, centers_end),
(str_store_troop_name, s11, "trp_dplmc_chamberlain"),
], "My fomer treasurer, {s11}.", "dplmc_tavern_traveler_employee_3", [
(assign, "$temp", "trp_dplmc_chamberlain"),
]],
[anyone|plyr, "dplmc_tavern_traveler_employee_2",
[
#Check is constable dismissed
(eq, "$g_player_constable", -1),
(neg|troop_slot_eq, "trp_dplmc_constable", slot_troop_met, 0),
#Check if constable could return
(assign, ":player_center", walled_centers_end),
(try_for_range, ":center_no", walled_centers_begin, ":player_center"),
   (party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
   (assign, ":player_center", ":center_no"),#set result and break loop
(try_end),
(is_between, ":player_center", walled_centers_begin, walled_centers_end),
(str_store_troop_name, s11, "trp_dplmc_constable"),
], "My fomer army inspector, {s11}.", "dplmc_tavern_traveler_employee_3", [
(assign, "$temp", "trp_dplmc_constable"),
]],
[anyone|plyr, "dplmc_tavern_traveler_employee_2",
[
#Check is chancellor dismissed
(eq, "$g_player_chancellor", -1),
(neg|troop_slot_eq, "trp_dplmc_chancellor", slot_troop_met, 0),
#Check if chancellor could return
(assign, ":player_center", towns_end),
(try_for_range, ":center_no", towns_begin, ":player_center"),
   (party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
   (assign, ":player_center", ":center_no"),#set result and break loop
(try_end),
(is_between, ":player_center", towns_begin, towns_end),
(str_store_troop_name, s11, "trp_dplmc_chancellor"),
], "My former administrator, {s11}.", "dplmc_tavern_traveler_employee_3", [
(assign, "$temp", "trp_dplmc_chancellor"),
]],
[anyone|plyr, "dplmc_tavern_traveler_employee_2",
   [],  "Never mind.", "tavern_traveler_pretalk", []],
[anyone, "dplmc_tavern_traveler_employee_3",
[
(this_or_next|eq, "$temp", "trp_dplmc_chamberlain",),
(this_or_next|eq, "$temp", "trp_dplmc_constable",),
   (eq, "$temp", "trp_dplmc_chancellor",),
(neg|troop_slot_eq, "$temp", slot_troop_occupation, dplmc_slto_dead),
(neg|troop_slot_eq, "$temp", slot_troop_occupation, slto_kingdom_hero),
(neg|troop_slot_ge, "$temp", slot_troop_prisoner_of_party, 1),#deliberately not 0, in case of uninitialized slotm

(try_begin),
   (eq, "$temp", "trp_dplmc_chamberlain",),
	(assign, "$g_player_chamberlain", 0),
(else_try),
   (eq, "$temp", "trp_dplmc_constable",),
   (assign, "$g_player_constable", 0),
(else_try),
   (eq, "$temp", "trp_dplmc_chancellor",),
   (assign, "$g_player_chancellor", 0),
(try_end),
(call_script, "script_dplmc_store_troop_is_female", "$temp"),
], "I will send word to {reg0?her:him} that you are looking for {reg0?her:him}.",
"tavern_traveler_pretalk", []],
[anyone|plyr, "dplmc_tavern_traveler_employee_3",
   [],  "I am afraid I'm not able to help you.", "tavern_traveler_pretalk", []],
[anyone, "dplmc_trade_autosell_1", [
    (call_script, "script_dplmc_initialize_autoloot", 0),#0 means only run if uninitialized
    (call_script, "script_dplmc_auto_sell", "trp_player", "$g_talk_troop", "$g_dplmc_auto_sell_price_limit", "$temp", "$temp_2", 0),
	 #reg0 = mon, reg1 = number of items
	 (gt, reg0, 0),
	 (gt, reg1, 0),
	 (store_sub, reg2, reg0, 1),
     (store_sub, reg3, reg1, 1),
	 ], "Let's see, aside from your personal equipment, I see {reg1} {reg3?things:thing} that I would buy for {reg0} {reg2?mon:mon}.  Do we have a deal?", "dplmc_trade_autosell_2a",
	 []],
[anyone|plyr, "dplmc_trade_autosell_2a", [
	], "Sure.  Pleasure doing business with you.", "merchant_trade",
	[
      (call_script, "script_dplmc_auto_sell", "trp_player", "$g_talk_troop", "$g_dplmc_auto_sell_price_limit", "$temp", "$temp_2", 2),
	]],
[anyone|plyr, "dplmc_trade_autosell_2a", [], "Not exactly.  Let me show you what I meant.", "merchant_trade",
      [(change_screen_trade),]],
[anyone|plyr, "dplmc_trade_autosell_2a", [], "Nevermind.", "merchant_trade", []],
[anyone|plyr, "dplmc_trade_autosell_1", [],
   "Aside from what I presume is your personal equipment, I don't see anything that I would be interested in buying.", "dplmc_trade_autosell_2b",
	[]],
[anyone|plyr, "dplmc_trade_autosell_2b", [], "Let me show you what I meant.", "merchant_trade",
      [(change_screen_trade),]],
[anyone|plyr, "dplmc_trade_autosell_2b", [], "Nevermind then.", "merchant_trade", []],
[anyone,"dplmc_view_regular_inventory",
    [(call_script, "script_dplmc_print_subordinate_says_sir_madame_to_s0"),], "Very well {s0}, here is what I am using...", "dplmc_do_view_regular_inventory",#Use {s0} instead of {sir/madam}
    [
      (call_script, "script_dplmc_copy_inventory", "$g_player_troop", "trp_temp_array_a"),
      (call_script, "script_dplmc_copy_inventory", "$g_talk_troop", "trp_temp_array_b"),

      (try_for_range, ":i_slot", 0, 10),
        (troop_get_inventory_slot, ":item", "trp_temp_array_b", ":i_slot"),
        (gt, ":item", -1),
        (troop_get_inventory_slot_modifier, ":imod", "trp_temp_array_b", ":i_slot"),
        (troop_add_item,"trp_temp_array_b", ":item", ":imod"),
        (troop_set_inventory_slot, "trp_temp_array_b", ":i_slot", -1),
      (try_end),

      (change_screen_loot, "trp_temp_array_b"),
    ]],
[anyone,"dplmc_do_view_regular_inventory", [(call_script, "script_dplmc_print_subordinate_says_sir_madame_to_s0"),],
   "Is that satisfactory, {s0}?", "dplmc_do_view_regular_inventory_2", []#Use {s0} instead of {sir/madam}
  ],
[anyone|plyr,"dplmc_do_view_regular_inventory_2",
    [
      (call_script, "script_dplmc_copy_inventory", "trp_temp_array_a", "$g_player_troop"),
    ],
   "Indeed.", "do_regular_member_view_char", []
  ],
[anyone,"dplmc_devel_merchant_quest_skip",
  [],
  "{!}Okay.  I'll just give you the reward, and we can assume that all of this already happened.", "close_window",
  [
	#Setup quest 1: recruit 5 men
	(troop_add_gold, "trp_player", 100),
    (str_store_troop_name, s9, "$g_talk_troop"),
    (str_store_party_name, s1, "$g_starting_town"),
    (str_store_string, s2, "str_start_up_quest_message_1"),
	(call_script, "script_start_quest", "qst_collect_men", "$g_talk_troop"),
	(party_get_position, pos1, "$current_town"),
	#Finish quest 1
	(call_script, "script_succeed_quest", "qst_collect_men"),
	(call_script, "script_end_quest", "qst_collect_men"),
	#Setup quest 2: find location of brother
	(str_store_party_name, s9, "$current_town"),
	(str_store_string, s2, "str_start_up_quest_message_2"),
	(call_script, "script_start_quest", "qst_learn_where_merchant_brother_is", "$g_talk_troop"),
	#Finish quest 2
	(call_script, "script_succeed_quest", "qst_learn_where_merchant_brother_is"),
	(call_script, "script_end_quest", "qst_learn_where_merchant_brother_is"),
	#Setup quest 3: rescue brother
	(str_store_troop_name, s10, "$g_talk_troop"),
	(str_store_string, s2, "str_find_the_lair_near_s9_and_free_the_brother_of_the_prominent_s10_merchant"),
	(call_script, "script_start_quest", "qst_save_relative_of_merchant", "$g_talk_troop"),
	#Finish quest 3
	(assign, "$relative_of_merchant_is_found", 1),
	(call_script, "script_succeed_quest", "qst_save_relative_of_merchant"),
	(call_script, "script_finish_quest", "qst_save_relative_of_merchant", 100),
	(troop_add_gold, "trp_player", 200),
	#Setup quest 4: fight bandits
	(str_store_party_name_link, s9, "$g_starting_town"),
	(str_store_string, s2, "str_save_town_from_bandits"),
	(call_script, "script_start_quest", "qst_save_town_from_bandits", "$g_talk_troop"),
	#Finish quest 4
	(assign, "$current_startup_quest_phase", 4),
	(call_script, "script_change_player_relation_with_center", "$g_starting_town", 1),
	(troop_add_gold, "trp_player", 200),
    (call_script, "script_succeed_quest", "qst_save_town_from_bandits"),
    (call_script, "script_end_quest", "qst_save_town_from_bandits"),
	#So he'll reappear in the tavern (unless you don't immediately speak with him)
	(assign, "$dialog_with_merchant_ended", 1),
	(assign, "$g_do_one_more_meeting_with_merchant", 1),
	#Fix a subsequent-dialog bug if you speak with him again in his house at the start
	(neg|is_between, "$g_encountered_party_faction", npc_kingdoms_begin, npc_kingdoms_end),
	(store_faction_of_party, "$g_encountered_party_faction", "$g_starting_town"),
  ]],
[anyone,"dplmc_lord_ask_leave_service_rebellion", [
	(ge, "$g_talk_troop_relation", 15)],
	"Hrmph. Now do not be hasty with such words, {playername}. I deserve more respect than that, I think. Those lands belong to me and my heirs as you swore. If you continue down this route you will do me great offense, and there is no need for this to come to blows.",
		"dplmc_lord_ask_leave_service_rebellion_verify",[]],
[anyone,"dplmc_lord_ask_leave_service_rebellion", [
  ],
  "You've grown rash, {playername}. Your oath binds you to me and you govern what you do at my will. Think about what it is you are saying, as it is far from wise and will end poorly for you. You'd do well to reconsider.",
	"dplmc_lord_ask_leave_service_rebellion_verify",[]],
[anyone|plyr ,"dplmc_lord_ask_leave_service_rebellion_verify", [], "You are right, {s65}. The lands are yours, but still I must go.", "lord_ask_leave_service_3",[]],
[anyone|plyr ,"dplmc_lord_ask_leave_service_rebellion_verify", [], "My blood and sweat earned those lands, not yours. They are mine.", "dplmc_lord_ask_leave_rebellion_confirm",[
   ##diplomacy start+
	#The relation change with the liege is exacerbated by the number of fiefs
	#lost.  The "-10" figure is the previous relation hit for defecting; this now
	#scales up with the number of centers taken.
	(assign, ":relation_change", 0),
	(try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
		(party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
		(val_add, ":relation_change", -10),
	(try_end),

	#Defecting from a supposedly-beloved lord causes a greater hit to honor than if
	#the defection isn't so out-of-the-blue.
	(store_add, ":honor_change", "$g_talk_troop_relation", 5),
	(val_div, ":honor_change", -10),
	(val_min, ":honor_change", 0),
	#Defecting during a time of war is more dishonorable than defecting during a time
	#of peace.
	(try_begin),
		(assign, ":is_war", 0),
		(try_for_range, ":faction_no", npc_kingdoms_begin, npc_kingdoms_end),
			(faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
			(neq, ":faction_no", "$g_talk_troop_faction"),
			(store_relation, ":reln", ":faction_no", "$g_talk_troop_faction"),
			(lt, ":reln", 0),
			(assign, ":is_war", 1),
		(try_end),
		(gt, ":is_war", 0),
		(val_add, ":honor_change", -5),
	(try_end),
	#The baseline change is -10.  The greatest possible is -25 (100 relation with the king, and at war).
	(val_sub, ":honor_change", 10),

	#If the player was insufficiently recognized for his service, the honor loss
	#is lower.  (This will further modify the reaction of some lords.)
	(call_script, "script_dplmc_center_point_calc", "$g_talk_troop_faction", "trp_player", "$g_talk_troop", 3),
	(assign, ":avg_renown_per_center_point", reg0),
	(assign, ":player_center_points", reg1),
	(assign, ":king_center_points", reg2),
	(troop_get_slot, ":player_renown", "trp_player", slot_troop_renown),
	(troop_get_slot, ":king_renown", "$g_talk_troop", slot_troop_renown),
	(assign, ":fief_unfairness", 0),#0 = no justification on basis of unfairness, 1 = justified by unfairness

	(try_begin),
		(eq, ":player_center_points", 0),
		#Unfair if the player has no fiefs and at least 3/4 of average renown per center point
		(try_begin),
			(store_mul, reg0, ":avg_renown_per_center_point", 3),
			(val_div, reg0, 4),
			(ge, ":player_renown", reg0),
			(assign, ":fief_unfairness", 1),
			(val_add, ":honor_change", 5),
		(try_end),
	(else_try),
		#Unfair if the player's (renown / center points) is more than 5/4 the average
        (gt, ":player_center_points", 0),
		(store_div, ":player_renown_per_point", ":player_renown", ":player_center_points"),
		(store_mul, reg0, ":avg_renown_per_center_point", 5),
		(val_div, reg0, 4),
		#player is insufficiently rewarded for his renown
		(ge, ":player_renown_per_point", reg0),
		(assign, ":fief_unfairness", 1),
		(val_add, ":honor_change", 5),
   	(else_try),
        #Unfair if the player's renown per center point is more than 5/4 that of the king,
        #and not less than 3/4 of the faction average
        (store_mul, reg0, ":avg_renown_per_center_point", 3),
        (val_div, reg0, 4),
        (ge, ":player_renown_per_point", reg0),

        (store_mul, reg0, ":king_renown", 5),
        (val_div, reg0, 4),
        (gt, ":king_center_points", 0),
        (val_div, reg0, ":king_center_points"),
		#player is insufficiently rewarded for his renown
		(ge, ":player_renown_per_point", reg0),
		(assign, ":fief_unfairness", 1),
	(try_end),

    (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", ":relation_change"),
	(val_min, ":honor_change", -10),#In any event there will be some level of honor loss.
	(call_script, "script_change_player_honor", ":honor_change"),

	#If the player's departure is not justified by some other cause (such as
	#not being granted the rights to a fief that he had conquered, which Martial lords
	#would be sympathetic to at least in principle), he takes a general relations hit.
	(try_for_range, ":troop_no", heroes_begin, heroes_end),
		(troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
		(neq, ":troop_no", "$g_talk_troop"),
		(neq, ":troop_no", active_npcs_including_player_begin),
		(store_troop_faction, ":faction_no", ":troop_no"),
		(eq, ":faction_no", "$g_talk_troop_faction"),

		#Calculate the relationship penalty, if any
		(assign, ":relation_penalty", 0),

		#Relevant factors are:
		#The troop's relation with the player, the troop's relation with his liege,
		#the troop's primary reputation, and whether the troop has the tmt_honest
		#morality subtype (which despite its name is primarily related to keeping
		#bargains), and whether this defection is causing the troop to lose any fiefs.
		(call_script, "script_troop_get_player_relation", ":troop_no"),
		(assign, ":troop_player_relation", reg0),

		(call_script, "script_troop_get_relation_with_troop", ":troop_no", "$g_talk_troop"),
		(assign, ":troop_king_relation", reg0),

		(troop_get_slot, ":reputation", ":troop_no", slot_lord_reputation_type),
		(call_script, "script_dplmc_get_troop_morality_value", ":troop_no", tmt_honest),
		(assign, ":honest_val", reg0),

		(assign, ":fiefs_lost", 0),
		(try_for_range, ":village_no", villages_begin, villages_end),
			(party_slot_eq, ":village_no", slot_town_lord, ":troop_no"),
			(party_get_slot, ":bound_center", ":village_no", slot_village_bound_center),
			(ge, ":bound_center", 1),
			(party_slot_eq, ":bound_center", slot_town_lord, "trp_player"),
			(val_add, ":fiefs_lost", 1),
		(try_end),

		#Modify for relationship with liege
		(try_begin),
			(this_or_next|ge, ":honest_val", 1),
			(this_or_next|eq, ":reputation", lrep_upstanding),
				(eq, ":reputation", lrep_moralist),
			(ge, ":troop_king_relation", 5),
			(val_sub, ":relation_penalty", 1),
		(else_try),
			(this_or_next|lt, ":honest_val", 0),
			(this_or_next|eq, ":reputation", lrep_debauched),
			(this_or_next|eq, ":reputation", lrep_roguish),
				(eq, ":reputation", lrep_ambitious),
			(ge, ":troop_king_relation", 25),
			(val_sub, ":relation_penalty", 1),
		(else_try),
			(ge, ":troop_king_relation", 15),
			(val_sub, ":relation_penalty", 1),
		(try_end),

		#Those who like the king more than the player will take his side,
		#if they met the above relation threshold.
		(try_begin),
			(lt, ":relation_penalty", 0),
			(ge, ":troop_king_relation", ":troop_player_relation"),
			(val_sub, ":relation_penalty", 1),
		(try_end),

		#Lords who would consider the rebellion more justified if the player was "under-fiefed"
		#(some will only care if they liked the player; others have a more general sense of fairness).
		(try_begin),
			(ge, ":fief_unfairness", 1),
			(try_begin),
				(ge, ":honest_val", 0),
				(neq, ":reputation", lrep_debauched),
				(neq, ":reputation", lrep_selfrighteous),
				(neq, ":reputation", lrep_quarrelsome),
				(neq, ":reputation", lrep_cunning),
				(neq, ":reputation", lrep_ambitious),
				(ge, ":troop_player_relation", 0),
				(val_add, ":relation_penalty", ":fief_unfairness"),
			(else_try),
				(ge, ":troop_player_relation", 20),
				(val_add, ":relation_penalty", ":fief_unfairness"),
			(try_end),
		(try_end),

		#Subtract a penalty for lost fiefs
		(try_begin),
			(ge, ":fiefs_lost", 1),
			#apply -2 times fiefs lost
			(this_or_next|eq, ":reputation", lrep_custodian),
			(this_or_next|eq, ":reputation", lrep_ambitious),
            (this_or_next|eq, ":reputation", lrep_quarrelsome),
            (this_or_next|eq, ":reputation", lrep_selfrighteous),
            (this_or_next|eq, ":reputation", lrep_cunning),
            (this_or_next|eq, ":reputation", lrep_debauched),
				(eq, ":reputation", lrep_martial),
			(val_sub, ":relation_penalty", ":fiefs_lost"),
			(val_sub, ":relation_penalty", ":fiefs_lost"),
		(else_try),
			(ge, ":fiefs_lost", 1),
			#apply -1 times fiefs lost
			(neg|ge, ":reputation", lrep_conventional),
			(neq, ":reputation", lrep_goodnatured),
			(val_sub, ":relation_penalty", ":fiefs_lost"),
		(try_end),

		#Apply a non-zero (and non-positive) penalty
		(lt, ":relation_penalty", 0),
		(call_script, "script_change_player_relation_with_troop", ":troop_no", ":relation_penalty"),
	(try_end),
	##diplomacy end+
	]],
[anyone, "dplmc_lord_ask_leave_rebellion_confirm", [
	(ge, "$g_talk_troop_relation", 25)],
	"You disappoint me greatly, {playername}. You may have once had my confidence, but this is beyond reason. Do not doubt that I will defend my house's honor from your insult. This is war between us.", "dplmc_lord_ask_leave_rebellion_confirm_final", [
	(call_script, "script_player_leave_faction", 0), #"1" would mean give back fiefs
    (call_script, "script_activate_player_faction", "trp_player"),]],
[anyone, "dplmc_lord_ask_leave_rebellion_confirm", [
   ], "I should have seen your treachery coming. I must be growing soft to have been fool enough to miss your schemes. No matter. Your time will yet come, {playername}. Justice is switftest on a field of battle.", "dplmc_lord_ask_leave_rebellion_confirm_final", [
    (call_script, "script_player_leave_faction", 0), #"1" would mean give back fiefs
    (call_script, "script_activate_player_faction", "trp_player")]],
[anyone|plyr, "dplmc_lord_ask_leave_rebellion_confirm_final", [
   ], "I hold you in no ill-esteem, {s65}. I do only what is just.", "dplmc_lord_ask_leave_rebellion_end", []],
[anyone|plyr, "dplmc_lord_ask_leave_rebellion_confirm_final", [
   ], "We all do what we must. Good bye.", "dplmc_lord_ask_leave_rebellion_end", []],
[anyone|plyr, "dplmc_lord_ask_leave_rebellion_confirm_final", [
   ], "Then I await the day we meet in battle.", "dplmc_lord_ask_leave_rebellion_end", []],
[anyone, "dplmc_lord_ask_leave_rebellion_end", [
	(ge, "$g_talk_troop_relation", 25),
	(str_store_faction_name, s1, "$g_talk_troop_faction")
	],
	"This is a dark day, {playername}. It will be marked and rued throughout the {s1}. Your treachery will not be soon forgotten. It would be best if you left quickly.", "close_window", [
	(assign, "$g_leave_encounter", 1)]],
[anyone, "dplmc_lord_ask_leave_rebellion_end", [
   ], "You are not the same {man/woman} I took as my vassal, {playername}. Be gone from my sight before I end this now.", "close_window", [(assign, "$g_leave_encounter", 1)]],
]
