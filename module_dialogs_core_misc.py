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


dialogs_core_misc = [
[anyone ,"event_triggered", [(store_conversation_troop, "$g_talk_troop"),
                     (try_begin),
					 
						 #gekokujo 3.0 microfactions! include fort companions start
                         #(is_between, "$g_talk_troop", companions_begin, companions_end),
                         (is_between, "$g_talk_troop", companions_begin, fort_companions_end),
						 #gekokujo 3.0 microfactions! include fort companions end
                         (talk_info_show, 1),
                         (call_script, "script_setup_talk_info_companions"),
                     (try_end),

	 			##diplomacy start+ Get gender for troop
				##OLD:
				#(troop_get_type, reg65, "$g_talk_troop"),
				##NEW:
				(try_begin),
					(call_script, "script_cf_dplmc_troop_is_female", "$g_talk_troop"),
					(assign, reg65, 1),
				(else_try),
					(assign, reg65, 0),
				(try_end),
				##diplomacy end+
               (try_begin),
                 (faction_slot_eq,"$g_talk_troop_faction",slot_faction_leader,"$g_talk_troop"),
                 (str_store_string,s64,"@{reg65?my Lady:my Lord}"), #bug fix
                 (str_store_string,s65,"@{reg65?my Lady:my Lord}"),
                 (str_store_string,s66,"@{reg65?My Lady:My Lord}"),
               (else_try),
                 (str_store_string,s64,"@{reg65?madame:sir}"), #bug fix
                 (str_store_string,s65,"@{reg65?madame:sir}"),
                 (str_store_string,s66,"@{reg65?Madame:Sir}"),
               (try_end),


               (eq, 1, 0)],
"{!}Warning: This line is never displayed. It is just for storing conversation variables.", "close_window", []],
[anyone, "event_triggered",
[
(eq, "$talk_context", tc_give_center_to_fief),

(assign, ":there_are_vassals", 0),
##diplomacy start+ Handle player is co-ruler of kingdom
(assign, ":alt_faction", "fac_player_supporters_faction"),
(try_begin),
	(is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
	(call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", "$players_kingdom"),
	(ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
	(assign, ":alt_faction", "$players_kingdom"),
(try_end),
#Support promoted ladies
#(assign, ":end_cond", active_npcs_end),
(assign, ":end_cond", heroes_end),
##diplomacy end+
(try_for_range, ":troop_no", active_npcs_begin, ":end_cond"),
 (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
 (neq, "trp_player", ":troop_no"),
 (store_troop_faction, ":faction_no", ":troop_no"),
 ##diplomacy start+
 (this_or_next|eq, ":faction_no", ":alt_faction"),
 ##diplomacy end+
 (eq, ":faction_no", "fac_player_supporters_faction"),
 (val_add, ":there_are_vassals", 1),
 (assign, ":end_cond", 0),
(try_end),

(try_begin),
 (gt, ":there_are_vassals", 0),
 (str_store_string, s2, "str_do_you_wish_to_award_it_to_one_of_your_vassals"),
(else_try),
 (str_store_string, s2, "str_who_do_you_wish_to_give_it_to"),
(try_end),

(str_store_party_name, s1, "$g_center_taken_by_player_faction"),
(str_store_string, s5, "str_sire_my_lady_we_have_taken_s1_s2"),
],
"{!}{s5}", "award_fief_to_vassal",
[]],
[anyone|plyr, "award_fief_to_vassal",
[
(is_between, "$g_player_court", centers_begin, centers_end),
(store_faction_of_party, ":player_court_faction", "$g_player_court"),
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
(eq, ":player_court_faction", "fac_player_supporters_faction"),
],
"I wish to defer the appointment of a lord, until I take the counsel of my vassals", "award_fief_to_vassal_defer",
[
]],
[anyone, "award_fief_to_vassal_defer",
[
],
"As you wish, tono. You may decide this matter at a later date.", "close_window",
[
(try_begin),
(faction_slot_eq, "$players_kingdom", slot_faction_political_issue, -1),
(faction_set_slot, "$players_kingdom", slot_faction_political_issue, "$g_center_taken_by_player_faction"),
(try_end),
(call_script, "script_give_center_to_lord", "$g_center_taken_by_player_faction", -1, 0), #-1 for the faction lord in this script is used exclusively in this context
#It is only used because script_give_center_to_faction does not reset the town lord if fac_player_supporters_faction is the attacker

(assign, "$g_center_taken_by_player_faction", -1),

#new start
(try_begin),
 (eq, "$g_next_menu", "mnu_castle_taken"),
 (jump_to_menu, "$g_next_menu"),
(try_end),
#new end

]],
[anyone|plyr|repeat_for_troops,"award_fief_to_vassal",
[
(store_repeat_object, ":troop_no"),
(troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
(neq, "trp_player", ":troop_no"),
(store_troop_faction, ":faction_no", ":troop_no"),
##diplomacy start+ Handle player is co-ruler of kingdom
(assign, ":alt_faction", "fac_player_supporters_faction"),
(try_begin),
	(is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
	(call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", "$players_kingdom"),
	(ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
	(assign, ":alt_faction", "$players_kingdom"),
(try_end),
(this_or_next|eq, ":faction_no", ":alt_faction"),
##diplomacy end+
(eq, ":faction_no", "fac_player_supporters_faction"),
(str_store_troop_name, s11, ":troop_no"),
(call_script, "script_print_troop_owned_centers_in_numbers_to_s0", ":troop_no"),

(try_begin),
##diplomacy start+ fixed bug that was preventing "promised fief" from appearing
(troop_slot_eq, ":troop_no", slot_lord_recruitment_argument, argument_benefit),
##diplomacy end+
(str_store_string, s12, "str__promised_fief"),
(else_try),
(str_clear, s12),
(try_end),

(try_begin),
 (eq, reg0, 0),
  ##diplomacy start+ write to s0 instead of s1
 (str_store_string, s0, "str_no_fiefss12"),
 ##diplomacy end+
(else_try),
 ##diplomacy start+ write to s0 instead of s1
 (str_store_string, s0, "str_fiefs_s0s12"),
 ##diplomacy end+
(try_end),

##diplomacy start+ add relation to list of lords
#add relation string
(str_store_string_reg, s12, s63),#save s63, clobbering s12 (overwritten earlier)
(call_script, "script_troop_get_player_relation", ":troop_no"),
(call_script, "script_describe_relation_to_s63", reg0),
(str_store_string_reg, s1, s63),#clobber s1
(str_store_string_reg, s63, s12),#revert s63
(str_store_string, s1, "str_dplmc_s0_comma_s1"),#write to s1
##diplomacy end+
],
"{!}{s11} {s1}.", "award_fief_to_vassal_2",[(store_repeat_object, "$temp")]],
[anyone|plyr, "award_fief_to_vassal",
[
(call_script, "script_print_troop_owned_centers_in_numbers_to_s0", "trp_player"),
(str_store_party_name, s1, "$g_center_taken_by_player_faction"),

(try_begin),
(is_between, "$g_talk_troop", pretenders_begin, pretenders_end),
(str_store_string, s12, "str_please_s65_"),
(else_try),
(str_clear, s12),
(try_end),

(assign, ":there_are_vassals", 0),
##diplomacy start+
#Support promoted ladies
#(assign, ":end_cond", active_npcs_end),
(assign, ":end_cond", heroes_end),
#Handle player is co-ruler of kingdom
(assign, ":alt_faction", "fac_player_supporters_faction"),
(try_begin),
	(is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
	(call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", "$players_kingdom"),
	(ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
	(assign, ":alt_faction", "$players_kingdom"),
(try_end),
##diplomacy end+
(try_for_range, ":troop_no", active_npcs_begin, ":end_cond"),
 (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
 (neq, "trp_player", ":troop_no"),
 (store_troop_faction, ":faction_no", ":troop_no"),
 ##diplomacy start+
 (this_or_next|eq, ":faction_no", ":alt_faction"),
 ##diplomacy end+
 (eq, ":faction_no", "fac_player_supporters_faction"),
 (val_add, ":there_are_vassals", 1),
 (assign, ":end_cond", 0),
(try_end),

(try_begin),
 (gt, ":there_are_vassals", 0),
(str_store_string, s2, "str_fiefs_s0"),
(else_try),
(str_clear, s2),
(try_end),

(str_store_string, s5, "str_s12i_want_to_have_s1_for_myself"),
],
"{!}{s5}", "award_fief_to_vassal_2",
[
(assign, "$temp", "trp_player"),
]],
[anyone, "award_fief_to_vassal_2",
[
],
"As you wish, tono. {reg6?I:{reg7?You:{s11}}} will be the new {reg3?lady:lord} of {s1}.", "close_window",
[
(assign, ":new_owner", "$temp"),

(call_script, "script_give_center_to_lord", "$g_center_taken_by_player_faction", ":new_owner", 0),
(try_begin),
(faction_slot_eq, "$players_kingdom", slot_faction_political_issue, "$g_center_taken_by_player_faction"),
(faction_set_slot, "$players_kingdom", slot_faction_political_issue, -1),
(try_end),

(assign, reg6, 0),
(assign, reg7, 0),
(try_begin),
 (eq, ":new_owner", "$g_talk_troop"),
 (assign, reg6, 1),
(else_try),
 (eq, ":new_owner", "trp_player"),
 (assign, reg7, 1),
(else_try),
 (str_store_troop_name, s11, ":new_owner"),
(try_end),
(str_store_party_name, s1, "$g_center_taken_by_player_faction"),
##diplomacy start+
##OLD: #(troop_get_type, reg3, ":new_owner"),
##NEW:
(assign, reg3, 0),
(try_begin),
	(call_script, "script_cf_dplmc_troop_is_female", ":new_owner"),
	(assign, reg3, 1),
(try_end),
##diplomacy end+

(assign, "$g_center_taken_by_player_faction", -1),

#new start
(try_begin),
 (eq, "$g_next_menu", "mnu_castle_taken"),
 (jump_to_menu, "$g_next_menu"),
(try_end),
#new end
]],
[anyone, "event_triggered",
[
##diplomacy start+ Handle g_talk_troop and player are co-rulers of kingdom
(assign, ":is_coruler", 0),
(try_begin),
	(is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
	(faction_slot_eq, "$players_kingdom", slot_faction_leader, "$g_talk_troop"),
	(call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", "$players_kingdom"),
	(ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
	(assign, ":is_coruler", 1),
(try_end),
(this_or_next|eq, ":is_coruler", 1),
##diplomacy end+
(faction_slot_eq, "fac_player_supporters_faction", slot_faction_leader, "$g_talk_troop"),
(ge, "$g_center_taken_by_player_faction", 0),
(str_store_party_name, s1, "$g_center_taken_by_player_faction"),
],
"{s1} is not being managed by anyone. Who shall be put in charge?", "center_captured_rebellion",
[]],
[anyone|plyr|repeat_for_troops, "center_captured_rebellion",
[
(store_repeat_object, ":troop_no"),
(troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
(neq, "$g_talk_troop", ":troop_no"),
(neq, "trp_player", ":troop_no"),
(store_troop_faction, ":faction_no", ":troop_no"),
##diplomacy start+ Handle player is co-ruler of kingdom
(assign, ":alt_faction", "fac_player_supporters_faction"),
(try_begin),
	(is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
	(call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", "$players_kingdom"),
	(ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
	(assign, ":alt_faction", "$players_kingdom"),
(try_end),
(this_or_next|eq, ":faction_no", ":alt_faction"),
##diplomacy end+
(eq, ":faction_no", "fac_player_supporters_faction"),
(str_store_troop_name, s11, ":troop_no"),
(call_script, "script_print_troop_owned_centers_in_numbers_to_s0", ":troop_no"),
(try_begin),
 (eq, reg0, 0),
 (str_store_string, s1, "@(no fiefs)"),
(else_try),
 (str_store_string, s1, "@(fiefs: {s0})"),
(try_end),
],
"{s11}. {s1}", "center_captured_rebellion_2",
[
(store_repeat_object, "$temp"),
]],
[anyone|plyr, "center_captured_rebellion",
[
(call_script, "script_print_troop_owned_centers_in_numbers_to_s0", "trp_player"),
(str_store_party_name, s1, "$g_center_taken_by_player_faction"),
##diplomacy start+
#Remove the "please" if the player is co-ruler
(assign, reg0, 0),
(try_begin),
	(this_or_next|troop_slot_eq, "trp_player", slot_troop_spouse, "$g_talk_troop"),
	(troop_slot_eq, "$g_talk_troop", slot_troop_spouse, "trp_player"),
(try_end),
],
#"Please {s65}, I want to have {s1} for myself. (fiefs: {s0})", "center_captured_rebellion_2",
"{reg0?{s65}:Please {s65}}, I want to have {s1} for myself. (fiefs: {s0})", "center_captured_rebellion_2",
##diplomacy end+
[
(assign, "$temp", "trp_player"),
]],
[anyone|plyr, "center_captured_rebellion",
[
(call_script, "script_print_troop_owned_centers_in_numbers_to_s0", "$g_talk_troop"),
(str_store_party_name, s1, "$g_center_taken_by_player_faction"),
],
"{s66}, you should have {s1} for yourself. (fiefs: {s0})", "center_captured_rebellion_2",
[
(assign, "$temp", "$g_talk_troop"),
]],
[anyone|plyr, "center_captured_rebellion",
[
(str_store_party_name, s1, "$g_center_taken_by_player_faction"),
],
"You should appoint no one yet, and decide later.",
 "center_captured_rebellion_2_defer",
[
]],
[anyone, "center_captured_rebellion_2_defer",
[
],
"Hmmm. All right, {playername}. I value your counsel highly.  I shall defer appointment of a lord for {s1} for the time.", "close_window",
[
 (call_script, "script_give_center_to_lord", "$g_center_taken_by_player_faction", -1, 0),
 (try_begin),
          (faction_slot_eq, "$players_kingdom", slot_faction_political_issue, "$g_center_taken_by_player_faction"),
(faction_set_slot, "$players_kingdom", slot_faction_political_issue, -1),
(try_end),
 (str_store_party_name, s1, "$g_center_taken_by_player_faction"),
 (assign, "$g_center_taken_by_player_faction", -1),
 #new start
 (try_begin),
    (eq, "$g_next_menu", "mnu_castle_taken"),
    (jump_to_menu, "$g_next_menu"),
 (try_end),
],
],
[anyone, "center_captured_rebellion_2",
[
#     (faction_slot_eq, "fac_player_supporters_faction", slot_faction_leader, "$g_talk_troop"),
#     (ge, "$g_center_taken_by_player_faction", 0),
],
"Hmmm. All right, {playername}. I value your counsel highly. {reg6?I:{reg7?You:{s11}}} will be the new {reg3?lady:lord} of {s1}.", "close_window",
[
(assign, ":new_owner", "$temp"),
(call_script, "script_calculate_troop_score_for_center", ":new_owner", "$g_center_taken_by_player_faction"),
(assign, ":new_owner_score", reg0),
##diplomacy start+
#(assign, ":total_negative_effect"),
(assign, ":total_negative_effect", 0),
##Handle player is co-ruler of kingdom
(assign, ":alt_faction", "fac_player_supporters_faction"),
(try_begin),
	(is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
	(call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", "$players_kingdom"),
	(ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
	(assign, ":alt_faction", "$players_kingdom"),
(try_end),
##Change next line to support promoted kingdom ladies:
#(try_for_range, ":cur_troop", active_npcs_begin, active_npcs_end),
(try_for_range, ":cur_troop", heroes_begin, heroes_end),
##diplomacy end+
(troop_slot_eq, ":cur_troop", slot_troop_occupation, slto_kingdom_hero),
 (store_troop_faction, ":cur_faction", ":cur_troop"),
 ##diplomacy start+
 (this_or_next|eq, ":cur_faction", ":alt_faction"),
 ##diplomacy end+
 (eq, ":cur_faction", "fac_player_supporters_faction"),
 (neq, ":cur_troop", ":new_owner"),
(neg|troop_slot_eq, ":cur_troop", slot_troop_stance_on_faction_issue, ":new_owner"),
(call_script, "script_troop_get_relation_with_troop", ":cur_troop", ":new_owner"),
(lt, reg0, 25),


 (call_script, "script_calculate_troop_score_for_center", ":cur_troop", "$g_center_taken_by_player_faction"),
 (assign, ":cur_troop_score", reg0),
 (gt, ":cur_troop_score", ":new_owner_score"),
 (store_sub, ":difference", ":cur_troop_score", ":new_owner_score"),
 (store_random_in_range, ":random_dif", 0, ":difference"),
 (val_div, ":random_dif", 1000),
 (gt, ":random_dif", 0),
 (val_add, ":total_negative_effect", ":random_dif"),
 (val_mul, ":random_dif", -1),
 (call_script, "script_change_player_relation_with_troop", ":cur_troop", ":random_dif"),
(try_end),
(val_mul, ":total_negative_effect", 2),
(val_div, ":total_negative_effect", 3),
(val_add, ":total_negative_effect", 5),
(try_begin),
 (neq, ":new_owner", "trp_player"),
 (val_min, ":total_negative_effect", 30),
 (call_script, "script_change_player_relation_with_troop", ":new_owner", ":total_negative_effect"),
(try_end),

(call_script, "script_give_center_to_lord", "$g_center_taken_by_player_faction", ":new_owner", 0),
(try_begin),
(faction_slot_eq, "$players_kingdom", slot_faction_political_issue, "$g_center_taken_by_player_faction"),
(faction_set_slot, "$players_kingdom", slot_faction_political_issue, -1),
(try_end),

(assign, reg6, 0),
(assign, reg7, 0),
(try_begin),
 (eq, ":new_owner", "$g_talk_troop"),
 (assign, reg6, 1),
(else_try),
 (eq, ":new_owner", "trp_player"),
 (assign, reg7, 1),
(else_try),
 (str_store_troop_name, s11, ":new_owner"),
(try_end),
(str_store_party_name, s1, "$g_center_taken_by_player_faction"),
##diplomacy start+
##OLD:
#(troop_get_type, reg3, ":new_owner"),
##NEW:
(assign, reg3, 0),
(try_begin),
	(call_script, "script_cf_dplmc_troop_is_female", ":new_owner"),
	(assign, reg3, 1),
(try_end),
##diplomacy end+

(assign, "$g_center_taken_by_player_faction", -1),

#new start
(try_begin),
 (eq, "$g_next_menu", "mnu_castle_taken"),
 (jump_to_menu, "$g_next_menu"),
(try_end),
#new end
]],
[trp_tutorial_master_archer, "ranged_end", [],
"Now, you can go talk with the melee fighters or the horsemanship trainer if you haven't already done so. They can teach you important skills too.",
"close_window", []],
[anyone|plyr, "archer_talk",
[
(eq, "$g_tutorial_training_ground_archer_trainer_completed_chapters", 0),
],
"Yes, show me how to use ranged weapons.", "archer_challenge", []],
[anyone|plyr, "archer_talk",
[],
"No, not now.", "close_window", []],
[trp_tutorial_master_archer, "archer_challenge",
[
(eq, "$g_tutorial_training_ground_archer_trainer_completed_chapters", 0),
],
"All right. Your first training will be in bowmanship. The bow is a difficult weapon to master. But once you are sufficiently good at it, you can shoot quickly and with great power.\
Go pick up the bow and arrows you see over there now and shoot those targets.", "archer_challenge_2",
[]],
[anyone|plyr, "archer_challenge_2",
[],
"All right. I am ready.", "close_window",
[
(assign, "$g_tutorial_training_ground_archer_trainer_state", 1),
(try_begin),
 (eq, "$g_tutorial_training_ground_archer_trainer_completed_chapters", 0),
 (assign, "$g_tutorial_training_ground_archer_trainer_item_1", "itm_gekokujo_practice_yumi"),
 (assign, "$g_tutorial_training_ground_archer_trainer_item_2", "itm_gekokujo_practice_arrows"),
(else_try),
 (eq, "$g_tutorial_training_ground_archer_trainer_completed_chapters", 1),
 (assign, "$g_tutorial_training_ground_archer_trainer_item_1", "itm_gekokujo_practice_yumi"),
 (assign, "$g_tutorial_training_ground_archer_trainer_item_2", "itm_gekokujo_practice_arrows"),
(else_try),
 (assign, "$g_tutorial_training_ground_archer_trainer_item_1", "itm_gekokujo_practice_yumi"),
 (assign, "$g_tutorial_training_ground_archer_trainer_item_2", "itm_gekokujo_practice_arrows"),
(try_end),
]],
[anyone|plyr, "archer_challenge_2",
[],
"Just a minute. I want to do something else first.", "close_window",
[]],
[trp_tutorial_master_horseman, "horsemanship_end",
[
],
"Now, you can go talk with the melee fighters or the archery trainer if you haven't already done so. You need to learn everything you can to be prepared when you have to defend yourself.", "close_window",
[]],
[anyone|plyr, "horseman_talk",
[],
"Yes, I would like to practice riding.", "horseman_challenge", []],
[anyone|plyr, "horseman_talk",
[],
"Uhm. Maybe later.", "close_window", []],
[trp_tutorial_master_horseman, "horseman_challenge",
[
(eq, "$g_tutorial_training_ground_horseman_trainer_completed_chapters", 0),
],
"Good. Now, I will give you a few exercises that'll teach you riding and horseback weapon use.\
Your first assignment is simple. Just take your horse for a ride around the course.\
Go as slow or as fast as you like.\
Come back when you feel confident as a rider and I'll give you some tougher exercises.", "horseman_melee_challenge_2",
[]],
[anyone|plyr, "horseman_melee_challenge_2",
[],
"All right. I am ready.", "close_window",
[
(assign, "$g_tutorial_training_ground_horseman_trainer_state", 1),
(try_begin),
 (eq, "$g_tutorial_training_ground_horseman_trainer_completed_chapters", 0),
 (assign, "$g_tutorial_training_ground_horseman_trainer_item_1", -1),
 (assign, "$g_tutorial_training_ground_horseman_trainer_item_2", -1),
(else_try),
 (eq, "$g_tutorial_training_ground_horseman_trainer_completed_chapters", 1),
 (assign, "$g_tutorial_training_ground_horseman_trainer_item_1", "itm_gekokujo_practice_yari"),
 (assign, "$g_tutorial_training_ground_horseman_trainer_item_2", -1),
(else_try),
 (assign, "$g_tutorial_training_ground_horseman_trainer_item_1", "itm_gekokujo_practice_yumi"),
 (assign, "$g_tutorial_training_ground_horseman_trainer_item_2", "itm_gekokujo_practice_arrows"),
(try_end),
]],
[anyone|plyr, "horseman_melee_challenge_2",
[],
"Just a minute. I need to do something else first.", "close_window", []],
[anyone|plyr, "player_duel_response", [],
"Such a waste...", "close_window", [
]],
[anyone|plyr, "player_duel_response", [],
"Better him than me", "close_window", [
]],
[anyone|plyr, "drunk_response", [],
"I'm not sure... Some sort of animal, clearly", "drunk_fight_start", [
]],
[anyone|plyr, "drunk_response", [],
##diplomacy start+ Change this so there is some chance of success
#to avoid a fight.
##OLD:
#"Excuse me -- please accept my apologies", "drunk_fight_start", [
#]],
##NEW:
"Excuse me -- please accept my apologies", "dplmc_drunk_attempt_placate", [
]],
[anyone, "drunk_fight_start", [],
"I'll wipe that smirk right off your face!", "close_window", [
(troop_set_slot, "trp_belligerent_drunk", slot_troop_cur_center, 0),
]],
[anyone|plyr, "drunk_response",
[
##diplomacy start+
#In Native this only shows up when it is guaranteed to succeed, but that
#isn't particularly interesting.
##REMOVED:
#(troop_slot_ge, "trp_player", slot_troop_renown, 150),
##diplomacy end+
],
"Do you have any idea who I am?", "drunk_player_high_renown", [
]],
[anyone, "drunk_player_high_renown", [
##diplomacy start+ Failure is also possible because you can get to this line with insufficient renown
(this_or_next|neg|troop_slot_ge, "trp_player", slot_troop_renown, 150),
##diplomacy end+
(eq, "$g_talk_troop", "trp_hired_assassin"),
],
"Do I care?", "drunk_fight_start", [
]],
[anyone, "drunk_player_high_renown", [
   (lt, "$g_disable_condescending_comments", 0),#prejudice mode: high
   (call_script, "script_cf_dplmc_faction_has_bias_against_gender", "$g_encountered_party_faction", "$character_gender"),
   (neg|troop_slot_ge, "trp_player", slot_troop_renown, 300),
],
"Big talk from a little runt.  I'll put you in your place!", "drunk_fight_start", [
]],
[anyone, "drunk_player_high_renown", [
##diplomacy start+ change to use script_dplmc_print_subordinate_says_sir_madame_to_s0
(call_script, "script_dplmc_print_subordinate_says_sir_madame_to_s0"),
##diplomacy end+
],
##diplomacy start+ change to use script_dplmc_print_subordinate_says_sir_madame_to_s0
"Emmm... Actually... Yes, yes, I do know who you are, {s0}. Please forgive me, {playername}-dono -- it must be the drink. I'll be leaving, now...", "drunk_player_high_renown", [
##diplomacy end+
]],
[anyone|plyr, "drunk_player_high_renown", [],
"Why, if you want a fight, you shall have one!", "drunk_fight_start", [
]],
[anyone|plyr, "drunk_player_high_renown", [],
"I thought as much. Now, remove yourself from here", "close_window",
[
(assign, "$drunks_dont_pick_fights", 1),
(troop_set_slot, "trp_belligerent_drunk", slot_troop_cur_center, 0),

(call_script, "script_deactivate_tavern_attackers"),

(assign, "$g_belligerent_drunk_leaving", "$g_main_attacker_agent"),

(mission_enable_talk),

(try_for_agents, ":agent"),
 (agent_is_alive, ":agent"),
 (agent_get_position, pos4, ":agent"),
 (agent_set_scripted_destination, ":agent", pos4),
(try_end),

(entry_point_get_position, pos1, 0),
(agent_set_scripted_destination, "$g_main_attacker_agent", pos1),

(assign, "$g_main_attacker_agent", 0),
]],
[party_tpl|pt_looters,"looters_1", [], "{s4}", "looters_2",[]],
[party_tpl|pt_looters|plyr,"looters_2", [[store_character_level,reg(1),"trp_player"],[lt,reg(1),4]], "I'm not afraid of you. Come at me!", "close_window",
[[encounter_attack]]],
[party_tpl|pt_looters|plyr,"looters_2", [[store_character_level,reg(1),"trp_player"],[ge,reg(1),4]], "You'll have nothing of mine but cold steel.", "close_window",
[[encounter_attack]]],
[anyone,"farmer_bandit_information", [
(call_script, "script_get_manhunt_information_to_s15", "qst_track_down_bandits"),
], "{s15}", "village_farmer_talk",[]],
[trp_kidnapped_girl|plyr,"kidnapped_girl_chat_1", [], "Not yet.", "kidnapped_girl_chat_2",[]],
[trp_kidnapped_girl,"kidnapped_girl_chat_2", [], "I can't wait to get back. I've missed my family so much, I'd give anything to see them again.", "close_window",[]],
[anyone ,"supported_pretender_pretalk", [],
"Anything else?", "supported_pretender_talk", []],
[anyone|plyr,"supported_pretender_talk", [],
"What do you think about our progress so far?", "pretender_progress",[]],
[anyone,"pretender_progress", [
 (assign, reg11, 0),(assign, reg13, 0),(assign, reg14, 0),(assign, reg15, 0),
 (assign, reg21, 0),(assign, reg23, 0),(assign, reg24, 0),(assign, reg25, 0),

 (try_for_range, ":troop_no", active_npcs_begin, active_npcs_end),
  (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
   (store_troop_faction, ":troop_faction", ":troop_no"),
   (try_begin),
     (eq, ":troop_faction", "fac_player_supporters_faction"),
     (neq, ":troop_no", "trp_player"),
     (neq, ":troop_no", "$supported_pretender"),
     (val_add, reg11, 1),
   (else_try),
     (eq, ":troop_faction", "$supported_pretender_old_faction"),
     (neg|faction_slot_eq, "$supported_pretender_old_faction", slot_faction_leader, ":troop_no"),
     (val_add, reg21, 1),
   (try_end),
 (try_end),
 (try_for_range, ":center_no", centers_begin, centers_end),
   (store_faction_of_party, ":center_faction", ":center_no"),
   (try_begin),
     (eq, ":center_faction", "fac_player_supporters_faction"),
     (try_begin),
       (party_slot_eq, ":center_no", slot_party_type, spt_town),
       (val_add, reg13, 1),
     (else_try),
       (party_slot_eq, ":center_no", slot_party_type, spt_castle),
       (val_add, reg14, 1),
     (else_try),
       (party_slot_eq, ":center_no", slot_party_type, spt_village),
       (val_add, reg15, 1),
     (try_end),
   (else_try),
     (eq, ":center_faction", "$supported_pretender_old_faction"),
     (try_begin),
       (party_slot_eq, ":center_no", slot_party_type, spt_town),
       (val_add, reg23, 1),
     (else_try),
       (party_slot_eq, ":center_no", slot_party_type, spt_castle),
       (val_add, reg24, 1),
     (else_try),
       (party_slot_eq, ":center_no", slot_party_type, spt_village),
       (val_add, reg25, 1),
     (try_end),
   (try_end),
 (try_end),
 (store_add, reg19, reg13, reg14),
 (val_add, reg19, reg15),
 (store_add, reg29, reg23, reg24),
 (val_add, reg29, reg25),
 (store_add, ":our_score", reg13, reg14),
 (val_add, ":our_score", reg11),
 (store_add, ":their_score", reg23, reg24),
 (val_add, ":their_score", reg21),
 (store_add, ":total_score", ":our_score", ":their_score"),
 (val_mul, ":our_score", 100),
 (store_div, ":our_ratio", ":our_score", ":total_score"),
 (try_begin),
   (lt, ":our_ratio", 10),
   (str_store_string, s30, "@we have made very little progress so far"),
 (else_try),
   (lt, ":our_ratio", 30),
   (str_store_string, s30, "@we have suceeded in gaining some ground, but we still have a long way to go"),
 (else_try),
   (lt, ":our_ratio", 50),
   (str_store_string, s30, "@we have become a significant force, and we have an even chance of victory"),
 (else_try),
   (lt, ":our_ratio", 75),
   (str_store_string, s30, "@we are winning the war, but our enemies are still holding on."),
 (else_try),
   (str_store_string, s30, "@we are on the verge of victory. The remaining enemies pose no threat, but we still need to hunt them down."),
 (try_end),
 (faction_get_slot, ":enemy_king", "$supported_pretender_old_faction", slot_faction_leader),
 (str_store_troop_name, s9, ":enemy_king"),
##diplomacy start+: Replace "lords" with "{s0}"; "no lord" with "no {s0}"; and use correct gender for enemy king
(call_script, "script_dplmc_print_cultural_word_to_sreg", "$g_talk_troop", DPLMC_CULTURAL_TERM_LORD_PLURAL, 0),
(call_script, "script_dplmc_store_troop_is_female", ":enemy_king"),
],
##OLD:
#"{reg11?We have {reg11} lords on our side:We have no lord with us yet},\
#whereas {reg21?{s9} still has {reg21} lords supporting him:{s9} has no loyal lords left}.\
#{reg19?We control {reg13?{reg13} towns:} {reg14?{reg14} castles:} {reg15?and {reg15} villages:}:We don't control any settlements},\
#while {reg29?they have {reg23?{reg23} towns:} {reg24?{reg24} castles:} {reg25?and {reg25} villages:}:they have no remaining settlements}.\
#Overall, {s30}.", "pretender_progress_2",[]],
##NEW:
"{reg11?We have {reg11} {s0} on our side:We have no {s0} with us yet},\
whereas {reg21?{s9} still has {reg21} {s0} supporting {reg0?her:him}:{s9} has no loyal {s0} left}.\
{reg19?We control {reg13?{reg13} towns:} {reg14?{reg14} castles:} {reg15?and {reg15} villages:}:We don't control any settlements},\
while {reg29?they have {reg23?{reg23} towns:} {reg24?{reg24} castles:} {reg25?and {reg25} villages:}:they have no remaining settlements}.\
Overall, {s30}.", "pretender_progress_2",[]],
[anyone|plyr,"pretender_progress_2", [],
"Then, we must keep fighting and rally our supporters!", "supported_pretender_pretalk",[]],
[anyone|plyr,"pretender_progress_2", [],
"It seems this rebellion is not going anywhere. We must give up.", "pretender_quit_rebel_confirm",[]],
[anyone,"pretender_quit_rebel_confirm", [],
"{playername}, you can't abandon me now. Are you serious?", "pretender_quit_rebel_confirm_2",[]],
[anyone|plyr,"pretender_quit_rebel_confirm_2", [],
"Indeed, I am. I can't support you any longer.", "pretender_quit_rebel_confirm_3",[]],
[anyone|plyr,"pretender_quit_rebel_confirm_2", [],
"I was joking. I will fight for you until we win.", "supported_pretender_pretalk",[]],
[anyone,"pretender_quit_rebel_confirm_3", [],
"Are you absolutely sure? I will never forgive you if you abandon my cause.", "pretender_quit_rebel_confirm_4",[]],
[anyone|plyr,"pretender_quit_rebel_confirm_4", [],
"I am sure.", "pretender_quit_rebel",[]],
[anyone|plyr,"pretender_quit_rebel_confirm_4", [],
"Let me think about this some more.", "supported_pretender_pretalk",[]],
[anyone,"pretender_quit_rebel", [],
"So be it. Then my cause is lost. There is only one thing to do for me now. I will go from Japan and never come back. With me gone, you may try to make your peace with {s4}.", "close_window",
[
(troop_get_slot, ":original_faction", "$g_talk_troop", slot_troop_original_faction),
(faction_get_slot, ":original_faction_leader", ":original_faction", slot_faction_leader),
(str_store_troop_name, s4, ":original_faction_leader"),

##diplomacy start+ Support promoted kingdom ladies
#(try_for_range, ":cur_troop", active_npcs_begin, active_npcs_end),##OLD
(try_for_range, ":cur_troop", heroes_begin, heroes_end),##NEW
##diplomacy end+
(troop_slot_eq, ":cur_troop", slot_troop_occupation, slto_kingdom_hero),
(neq, "$supported_pretender", ":cur_troop"),
 (store_troop_faction, ":cur_faction", ":cur_troop"),
 (eq, ":cur_faction", "fac_player_supporters_faction"),
 (call_script, "script_change_troop_faction", ":cur_troop", ":original_faction"),
(try_end),
(troop_set_faction, "$g_talk_troop", "fac_neutral"),
(faction_set_slot, "fac_player_supporters_faction", slot_faction_leader, "trp_player"),
(assign, ":has_center", 0),
(try_for_range, ":cur_center", centers_begin, centers_end),
 (store_faction_of_party, ":cur_faction", ":cur_center"),
 (eq, ":cur_faction", "fac_player_supporters_faction"),
 (assign, ":has_center", 1),
 (neg|party_slot_eq, ":cur_center", slot_town_lord, "trp_player"),
 (call_script, "script_give_center_to_lord", ":cur_center", "trp_player", 0),
(try_end),
(party_remove_members, "p_main_party", "$supported_pretender", 1),
(faction_set_slot, ":original_faction", slot_faction_has_rebellion_chance, 0),
(assign, "$supported_pretender", 0),
(try_begin), #Still has center
 (eq, ":has_center", 1),
 (faction_set_color, "fac_player_supporters_faction", 0xFF0000),
(try_begin), #added to prevent no minister if player gives up rebellion
(eq, "$g_player_minister", 0),
(assign, "$g_player_minister", "trp_temporary_minister"),
(try_end),
(else_try), #No center
 (call_script, "script_deactivate_player_faction"),
(try_end),
(call_script, "script_change_player_honor", -20),
(call_script, "script_fail_quest", "qst_rebel_against_kingdom"),
(call_script, "script_end_quest", "qst_rebel_against_kingdom"),
]],
[anyone|plyr,"supported_pretender_talk", [],
"{reg65?My lady:My lord}, would you allow me to check out your equipment?", "supported_pretender_equip",[]],
[anyone,"supported_pretender_equip", [], "Very well, it's all here...", "supported_pretender_pretalk",[
(change_screen_equip_other),
]],
[anyone|plyr,"supported_pretender_talk", [], "If it would please you, can you tell me about your skills?", "pretneder_view_char_requested",[]],
[anyone,"pretneder_view_char_requested", [], "Well, all right.", "supported_pretender_pretalk",[(change_screen_view_character)]],
[anyone|plyr,"supported_pretender_talk", [
##diplomacy start+ Handle player is co-ruler of NPC kingdom
(assign, ":alt_faction", "fac_player_supporters_faction"),
(try_begin),
	(is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
	(call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", "$players_kingdom"),
	(ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
	(assign, ":alt_faction", "$players_kingdom"),
(try_end),
##diplomacy end+
(assign, ":center_found", 0),
(try_for_range, ":fief_to_grant", centers_begin, centers_end),
(store_faction_of_party, ":fief_faction", ":fief_to_grant"),
##diplomacy start+
(this_or_next|eq, ":fief_faction", ":alt_faction"),
##diplomacy end+
(eq, ":fief_faction", "fac_player_supporters_faction"),
(party_slot_eq, ":fief_to_grant", slot_town_lord, -1),
(assign, ":center_found", 1),
(try_end),
(eq, ":center_found", 1),

],
"I suggest that you decide who should hold a fief that does not have a lord.", "supported_pretender_grant_fief",[]],
[anyone,"supported_pretender_grant_fief", [
],
"Which fief did you have in mind?", "supported_pretender_grant_fief_select",[]],
[anyone|plyr|repeat_for_parties,"supported_pretender_grant_fief_select", [
(store_repeat_object, ":fief_to_grant"),
(is_between, ":fief_to_grant", centers_begin, centers_end),
(store_faction_of_party, ":fief_faction", ":fief_to_grant"),
##diplomacy start+ Handle player is co-ruler of NPC kingdom
(assign, ":alt_faction", "fac_player_supporters_faction"),
(try_begin),
	(is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
	(call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", "$players_kingdom"),
	(ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
	(assign, ":alt_faction", "$players_kingdom"),
(try_end),
(this_or_next|eq, ":fief_faction", ":alt_faction"),
##diplomacy end+
(eq, ":fief_faction", "fac_player_supporters_faction"),
(party_slot_eq, ":fief_to_grant", slot_town_lord, -1),
(str_store_party_name, s4, ":fief_to_grant"),
],
"{s4}", "supported_pretender_grant_fief_choose_recipient",[
(store_repeat_object, "$g_center_taken_by_player_faction"),
]],
[anyone,"supported_pretender_grant_fief_choose_recipient", [
],
"And who should receive it?", "center_captured_rebellion",[
(str_store_party_name, s4, "$g_center_taken_by_player_faction"),
]],
[anyone|plyr,"supported_pretender_grant_fief_select", [
],
"Never mind.", "supported_pretender_pretalk",[]],
[anyone|plyr,"supported_pretender_talk", [],
"Let us keep going, {reg65?my lady:sir}.", "close_window",[]],
[anyone,"do_member_trade", [], "Anything else?", "member_talk",[]],
[anyone,"do_member_trade", [], "Anything else?", "member_talk",[]],
[anyone,"view_member_char_requested", [], "All right, let me tell you...", "do_member_view_char",[(change_screen_view_character)]],
[trp_smithy_master|plyr, "smithy_master_talk", [], "Yes. Show me what you have for sale.", "smithy_master_buy", []],
[trp_smithy_master,"smithy_master_buy", [], "Of course {sir/madam}.", "smithy_trade_completed",[[change_screen_trade]]],
[trp_smithy_master,"smithy_trade_completed", [], "Anything else?", "smithy_master_talk",[]],
[trp_smithy_master|plyr, "smithy_master_talk", [(troop_has_item_equipped,"trp_player","itm_calradia_broken_sword")], "You can reforge the sword?", "smithy_sword_1", []],
[trp_smithy_master,"smithy_sword_1", [], "Show that you have.", "smithy_sword_2",[]],
[trp_smithy_master|plyr, "smithy_sword_2", [], "Here.", "smithy_sword_3",[(troop_remove_item, "trp_player","itm_calradia_broken_sword")]],
[trp_smithy_master,"smithy_sword_3", [], "Mmm.. good steel, I can reforge, but I need more iron. Bring me oil and iron.", "smithy_sword_4",
  [
    (str_store_string, s2, "str_find_some_iron"),
    (call_script, "script_start_quest", "qst_find_iron_for_reforge", "trp_smithy_master"),
  ]],
[trp_smithy_master|plyr,"smithy_sword_4", [], "Thanks.", "close_window",[]],
[trp_smithy_master|plyr, "smithy_master_talk",
  [
    (check_quest_active, "qst_find_iron_for_reforge"),
    (player_has_item, "itm_oil"),
    (player_has_item, "itm_iron"),
  ],
  "I'm find materials.", "iron_for_smith", []],
[trp_smithy_master, "iron_for_smith", [], "Great, give me materials.", "iron_for_smith_1", 
  [
   (troop_remove_item, "trp_player", "itm_oil"),
   (troop_remove_item, "trp_player", "itm_iron"),
   ]],
[trp_smithy_master|plyr,"iron_for_smith_1", [], "Sword reforged?", "iron_for_smith_2",[]],
[trp_smithy_master,"iron_for_smith_2", [], "Oh... yes, take your sword.", "close_window",
  [
    (troop_add_item, "trp_player","itm_calradia_steel_sword",imod_tempered),
    (add_xp_as_reward, 500),
    (call_script, "script_succeed_quest", "qst_find_iron_for_reforge"),
    (call_script, "script_end_quest", "qst_find_iron_for_reforge"),
  ]],
[trp_smithy_master|plyr,"smithy_master_talk", [], "Nothing. Thanks.", "close_window",[]],
[trp_black_swordsman|plyr,"swordmaster_talk", [], "Hello, who are you?", "swordmaster_talk_2",[]],
[trp_black_swordsman|plyr, "swordmaster_talk", [], "Please forgive me, I'll be leaving, now...", "close_window",[]],
[trp_black_swordsman,"swordmaster_talk_2",[],"I wandering warrior, You can help me?", "swordmaster_talk_3",[]],
[trp_black_swordsman|plyr, "swordmaster_talk_3", [], "Help?", "swordmaster_talk_4",[]],
[trp_black_swordsman,"swordmaster_talk_4",[],"Yes, my old sword is broken in last battle, you can restore it?", "swordmaster_talk_5",[]],
[trp_black_swordsman|plyr, "swordmaster_talk_5", [], "Hmm. I'll think about it.", "close_window",[[assign,"$brok_sword",1]]],
[trp_black_swordsman|plyr,"swordmaster_help", [], "Think, I can help.", "swordmaster_help_2",[]],
[trp_black_swordsman|plyr, "swordmaster_help", [], "Later.", "close_window",[]],
[trp_black_swordsman,"swordmaster_help_2", [], "Great! Heh, well, this must be my lucky day.Here, take my sword.","swordmaster_help_3",[(troop_add_item, "trp_player","itm_calradia_broken_sword")]],
[trp_black_swordsman|plyr,"swordmaster_help_3", [], "I'd better be going.", "close_window",[[assign,"$brok_sword",2]]],
[trp_black_swordsman|plyr, "sword_restored", [(player_has_item,"itm_calradia_steel_sword")], "Yes! It was quite difficult.", "sword_restored_1",[(troop_remove_item, "trp_player","itm_calradia_steel_sword")]],
[trp_black_swordsman,"sword_restored_1",[],"Yes, my old sword, thanks man.", "sword_restored_2",
   [   
     (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 7),
     (add_xp_as_reward, 2000),
     (call_script, "script_troop_add_gold", "trp_player", 500),
     ]],
[trp_black_swordsman|plyr,"sword_restored_2",[],"A pleasure doing business with you, goodbye.", "close_window",[[assign,"$brok_sword",3]]],
[trp_black_swordsman|plyr, "sword_restored", [], "No, not yet.", "close_window",[]],
[trp_black_swordsman|plyr, "black_question", [(neg|main_party_has_troop, "$g_talk_troop")], "Join to my party.", "black_question_1",[]],
[trp_black_swordsman|plyr, "black_question", [], "Nothing, go", "close_window",[]],
[trp_black_swordsman,"black_question_1",[(hero_can_join,"p_main_party")],"I am at your service, {sire/my lady}.", "close_window",[
       (assign, "$g_move_heroes", 1),
       (call_script, "script_recruit_troop_as_companion", "$g_talk_troop"),
       ]],
[trp_black_swordsman,"black_question_1",[(neg|hero_can_join, "p_main_party")], "Not place in your party for me.", "close_window",[]],
[anyone,"do_member_view_char", [], "Anything else?", "member_talk",[]],
[anyone|plyr, "relative_saved_1a",
[],
"Horenbo? Your brother hired me to find and rescue you. I'm a little surprised -- he didn't say anything about you being a monk.", "relative_saved_1b",
[
]],
[anyone, "relative_saved_1b",
[
(str_store_party_name, s9, "$g_starting_town"),
],
"Brother? I don't have a brother, haha. My friend, I believe someone in {s9} owes you an explanation. As for me, off I go!", "relative_saved_1c",
[
]],
[anyone|plyr, "relative_saved_1c",
[],
"...", "close_window",
[
]],
[anyone|plyr,"looter_leader_1",
[
(store_faction_of_party, ":starting_town_faction", "$g_starting_town"),
(try_begin),
(eq, ":starting_town_faction", "fac_kingdom_11"),
(assign, ":troop_of_merchant", "trp_tsu_merchant"),
(else_try),
(eq, ":starting_town_faction", "fac_kingdom_10"),
(assign, ":troop_of_merchant", "trp_hirosaki_merchant"),
(else_try),
(eq, ":starting_town_faction", "fac_kingdom_1"),
(assign, ":troop_of_merchant", "trp_niigata_merchant"),
(else_try),
(eq, ":starting_town_faction", "fac_kingdom_13"),
(assign, ":troop_of_merchant", "trp_edo_merchant"),
(else_try),
(eq, ":starting_town_faction", "fac_kingdom_7"),
(assign, ":troop_of_merchant", "trp_sakai_merchant"),
(else_try),
(eq, ":starting_town_faction", "fac_kingdom_9"),
(assign, ":troop_of_merchant", "trp_hakata_merchant"),
(try_end),

(str_store_troop_name, s9, ":troop_of_merchant"),
],
"I've been looking for you. Tell me who your lord is and where he lives, and I will let you go.", "looter_leader_2",
[]],
[anyone|plyr,"looter_leader_1",
[],
"Nothing. I apologize for getting in your way.", "close_window",
[
(assign, "$g_leave_encounter", 1),
]],
[anyone,"looter_leader_2",
[],
"Are you serious? You've just told me that you wanted to die.", "looter_leader_3",
[]],
[anyone|plyr,"looter_leader_3",
[],
"We shall see who dies today.", "close_window",
[]],
[anyone|plyr,"rescue_prisoner_succeed_2", [], "Always an honour to serve, {s65}.", "lord_pretalk",[]],
[anyone, "start_up_quest_1_next",
[],
"Are you all right? Well... I guess you're alive, at any rate. I'm not sure that we can say the same for the ronin. That's one less murderous maniac to trouble our streets, although the gods know he won't be the last... Anyway, maybe you can help me with something... Let's talk more inside. Out here, we don't know who's listening", "close_window",
[
(assign, "$talked_with_merchant", 1),
(mission_disable_talk),
]],
[anyone, "start_up_quest_2_next",
[],
"{!}{s11}", "close_window",
[]],
[anyone, "minister_issues",
[
(check_quest_active, "qst_consult_with_minister"),
(eq, "$g_minister_notification_quest", "qst_resolve_dispute"),

(setup_quest_text,"qst_resolve_dispute"),

(quest_get_slot, ":lord_1", "qst_resolve_dispute", slot_quest_target_troop),
(str_store_troop_name, s11, ":lord_1"),

(quest_get_slot, ":lord_2", "qst_resolve_dispute", slot_quest_object_troop),
(str_store_troop_name, s12, ":lord_2"),

(str_store_string, s2, "str_resolve_the_dispute_between_s11_and_s12"),
(call_script, "script_start_quest", "qst_resolve_dispute", -1),
(quest_set_slot, "qst_resolve_dispute", slot_quest_expiration_days, 30),
(quest_set_slot, "qst_resolve_dispute", slot_quest_giver_troop, "$g_player_minister"),
(quest_set_slot, "qst_resolve_dispute", slot_quest_target_state, 0),
(quest_set_slot, "qst_resolve_dispute", slot_quest_object_state, 0),

(quest_get_slot, ":lord_1", "qst_resolve_dispute", slot_quest_target_troop), #this block just to check if the slots work
(str_store_troop_name, s11, ":lord_1"),
(quest_get_slot, ":lord_2", "qst_resolve_dispute", slot_quest_object_troop),
(str_store_troop_name, s12, ":lord_2"),

],
"There is a matter which needs your attention. The quarrel between {s11} and {s12} has esclatated to a point where it has become unseemly. If you do intervene, you risk offending one of the lords. However, if you do nothing, you risk appearing weak. Such are the burdens of lordship, my {lord/lady}.", "minister_pretalk",
[
(call_script, "script_end_quest", "qst_consult_with_minister"),
]],
[anyone, "minister_issues",
[
(assign, "$g_center_taken_by_player_faction", -1),
(try_for_range, ":center_no", centers_begin, centers_end),
(eq, "$g_center_taken_by_player_faction", -1),
(store_faction_of_party, ":center_faction", ":center_no"),
##diplomacy start+ Handle player is co-ruler of kingdom
(assign, ":alt_faction", 0),
(try_begin),
	(eq, ":center_faction", "$players_kingdom"),
	(is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
	(call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", "$players_kingdom"),
	(ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
	(assign, ":alt_faction", 1),
(try_end),
(this_or_next|eq, ":alt_faction",  1),
##diplomacy end+
(eq, ":center_faction", "fac_player_supporters_faction"),
(neg|party_slot_ge, ":center_no", slot_town_lord, 0),
(assign, "$g_center_taken_by_player_faction", ":center_no"),
(try_end),
(is_between, "$g_center_taken_by_player_faction", centers_begin, centers_end),
(str_store_party_name, s1, "$g_center_taken_by_player_faction"),
],
"{s1} currently does not have a lord. You may wish to keep it this way, as lords will sometimes gravitate towards daimyo who have land to offer, but for the time being, no one is collecting any of its rents.", "minister_talk",
[]],
[anyone, "minister_issues",
[
(neg|is_between, "$g_player_minister", active_npcs_begin, kingdom_ladies_end),
],
"At this point, there are no particularly urgent matters which need your attention. I should point out though, that I am not very skilled in the ways of politics, and that I am anxious to return to private life. If you wish to issue any but the most basic directives, I suggest appointing a trusted companion in my stead. In the meantime, is there anything you wish done?", "minister_talk",[]],
[anyone, "minister_issues",
[
(eq, 1, 0),
],
"{!}[Should not appear - there to prevent error related to center_captured_lord_advice]", "center_captured_lord_advice",[]],
[anyone, "minister_issues",
[
(lt, "$player_right_to_rule", 30),
],
"If I may offer you a world of advice, my {lord/lady}, it seems that your right to rule as an independent daimyo is not sufficiently recognized, and this may bring us problems further down the road. It may be advisable to find another clan with whom you have shared interests and seek its recognition, to establish yourself as an equal with Japan's other daimyo.", "minister_talk",[]],
[anyone, "minister_issues",
[],
"At this point, there are no particularly urgent matters which need your attention. Is there anything you wish done?", "minister_talk",[]],
[anyone, "minister_pretalk",
[],
"Is there anything you wish done?", "minister_talk",
[]],
[anyone|plyr,"minister_talk",
[
(is_between, "$g_player_minister", active_npcs_begin, kingdom_ladies_end),
],
"Do you have any ideas to strengthen our kingdom's unity?", "combined_political_quests",[
(call_script, "script_get_political_quest", "$g_talk_troop"),
(assign, "$political_quest_found", reg0),
(assign, "$political_quest_target_troop", reg1),
(assign, "$political_quest_object_troop", reg2),

]],
[anyone|plyr,"minister_talk", [
	(check_quest_active, "qst_offer_gift"),
    (quest_slot_eq, "qst_offer_gift", slot_quest_giver_troop, "$g_talk_troop"),
	
    (quest_get_slot, ":target_troop", "qst_offer_gift", slot_quest_target_troop),
	(str_store_troop_name, s4, ":target_troop"),
	(player_has_item, "itm_furs"),
	(player_has_item, "itm_velvet"),
   ],
   "I have the materials for {s4}'s gift.", "offer_gift_quest_complete",[
   ]],
[anyone,"offer_gift_quest_complete", [
   (quest_get_slot, ":target_troop", "qst_offer_gift", slot_quest_target_troop),
   (troop_get_type, reg4, ":target_troop"),
   ],
   "Ah, let me take those. Hopefully this will mend the quarrel between you two. You may wish to speak to {reg4?her:him}, and see if I had any success.", "close_window",[
   (quest_set_slot, "qst_offer_gift", slot_quest_current_state, 2),
   (quest_set_slot, "qst_offer_gift", slot_quest_expiration_days, 365),
   (troop_remove_item, "trp_player", "itm_furs"),
   (troop_remove_item, "trp_player", "itm_velvet"),
   (assign, "$g_leave_encounter", 1),
]],
[anyone|plyr,"minister_talk",
[
(assign, "$political_quest_to_cancel", -1),
(try_begin),
(check_quest_active, "qst_offer_gift"),
(quest_slot_eq, "qst_offer_gift", slot_quest_giver_troop, "$g_talk_troop"),
(assign, "$political_quest_to_cancel", "qst_offer_gift"),
(str_store_string, s10, "str_offer_gift_description"),
(else_try),
(check_quest_active, "qst_resolve_dispute"),
(quest_slot_eq, "qst_resolve_dispute", slot_quest_giver_troop, "$g_talk_troop"),
(assign, "$political_quest_to_cancel", "qst_resolve_dispute"),
(str_store_string, s10, "str_resolve_dispute_description"),
(try_end),
(gt, "$political_quest_to_cancel", 0),
],
"Let's abandon our plan to {s10}.", "minister_cancel_political_quest",[
]],
[anyone,"minister_cancel_political_quest",
[],
"Are you sure you want to drop that idea?", "minister_cancel_political_quest_confirm",[
]],
[anyone|plyr,"minister_cancel_political_quest_confirm",
[],
"Yes, I am sure. Let's abandon that idea.", "minister_pretalk",[
(call_script, "script_abort_quest", "$political_quest_to_cancel", 1),
]],
[anyone|plyr,"minister_cancel_political_quest_confirm",
[],
"Actually, never mind.", "minister_pretalk",[
]],
[anyone|plyr, "minister_talk",
[
(is_between, "$g_player_minister", active_npcs_begin, kingdom_ladies_end),
],
"I wish to dispatch an emissary.", "minister_diplomatic_kingdoms",
[]],
[anyone|plyr, "minister_talk",
[
(is_between, "$g_player_minister", active_npcs_begin, kingdom_ladies_end),
],
"I wish to indict a disloyal vassal for treason.", "minister_indict",
[]],
[anyone|plyr, "minister_talk",
[
(faction_get_slot, ":current_marshal", "$players_kingdom", slot_faction_marshall),
(ge, ":current_marshal", 0),
(try_begin),
(gt, ":current_marshal", 0),
(str_store_troop_name, s4, ":current_marshal"),
(else_try),
(str_store_string, s4, "str_myself"),
(try_end),
],
"I wish to replace {s4} as strategist.", "minister_change_marshal",
[]],
[anyone|plyr, "minister_talk",
[
(faction_slot_eq,  "$players_kingdom", slot_faction_marshall, -1),
],
"I wish to appoint a new strategist.", "minister_change_marshal",
[]],
[anyone, "minister_change_marshal",
[
(store_current_hours, ":hours"),
(val_sub, ":hours", "$g_player_faction_last_marshal_appointment"),
##diplomacy start+ Change based on centralization
#(lt, ":hours", 48), (Standard 48 hours, minimum 24 hours, maximum 72 hours)
(faction_get_slot, ":centralization", "fac_player_supporters_faction", dplmc_slot_faction_centralization),
(val_clamp, ":centralization", -3, 4),
(store_mul, ":reset_time", ":centralization", 8),
(val_add, ":reset_time", 48),
(lt, ":hours", ":reset_time"),
##diplomacy end+
],
"You have just made such an appointment, my {lord/lady}. If you countermand your decree so soon, there will be great confusion. We will need to wait a few days.", "minister_pretalk",
[]],
[anyone|plyr, "minister_talk",
[
(neg|is_between, "$g_player_minister", active_npcs_begin, active_npcs_end),
],
"I wish for you to retire as minister.", "minister_replace",
[]],
[anyone|plyr, "minister_talk",
[
(is_between, "$g_player_minister", active_npcs_begin, active_npcs_end),
(neg|troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_hero),

],
"I wish you to rejoin my party.", "minister_replace",
[]],
[anyone|plyr, "minister_talk",
[
(is_between, "$g_player_minister", active_npcs_begin, kingdom_ladies_end),
],
"I wish you to grant one of my vassals a fief.", "minister_grant_fief",
[]],
[anyone|plyr, "minister_talk",
[
(is_between, "$g_player_minister", active_npcs_begin, kingdom_ladies_end),
(assign, ":fief_found", -1),
##diplomacy start+ Handle player is co-ruler of kingdom
(assign, ":alt_faction", "fac_player_supporters_faction"),
(try_begin),
	(is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
	(call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", "$players_kingdom"),
	(ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
	(assign, ":alt_faction", "$players_kingdom"),
(try_end),
##diplomacy end+
(try_for_range, ":center", centers_begin, centers_end),
(eq, ":fief_found", -1),
(store_faction_of_party, ":center_faction", ":center"),
##diplomacy start+ Handle player is co-ruler of kingdom
(this_or_next|eq, ":center_faction", ":alt_faction"),
##diploamcy end+
(eq, ":center_faction", "fac_player_supporters_faction"),
(party_get_slot, ":town_lord", ":center", slot_town_lord),
(try_begin),
(ge, ":town_lord", active_npcs_begin),
(store_faction_of_troop, ":town_lord_faction", ":town_lord"),
##diplomacy start+ Handle player is co-ruler of kingdom
(neq, ":town_lord_faction", ":alt_faction"),
##diplomacy end+
(neq, ":town_lord_faction", "fac_player_supporters_faction"),
(assign, ":town_lord", -1),
(try_end),
(lt, ":town_lord", 0),
(assign, ":fief_found", ":center"),
(try_end),
(gt, ":fief_found", -1),
(str_store_party_name, s4, ":fief_found"),
],
"I wish to make myself lord of {s4}.", "minister_grant_self_fief",
[]],
[anyone, "minister_grant_self_fief",
[
],
"As you wish. You shall be lord of {s4}.", "minister_pretalk",
[
(assign, ":fief_found", -1),
##diplomacy start+ Handle player is co-ruler of kingdom
(assign, ":alt_faction", "fac_player_supporters_faction"),
(try_begin),
	(is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
	(call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", "$players_kingdom"),
	(ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
	(assign, ":alt_faction", "$players_kingdom"),
(try_end),
##diplomacy end+
(try_for_range, ":center", centers_begin, centers_end),
(eq, ":fief_found", -1),
(store_faction_of_party, ":center_faction", ":center"),
##diplomacy start+ Handle player is co-ruler of kingdom
(this_or_next|eq, ":center_faction", ":alt_faction"),
##diplomacy end+
(eq, ":center_faction", "fac_player_supporters_faction"),
(party_get_slot, ":town_lord", ":center", slot_town_lord),
(try_begin),
(ge, ":town_lord", active_npcs_begin),
(store_faction_of_troop, ":town_lord_faction", ":town_lord"),
##diplomacy start+ Handle player is co-ruler of kingdom
(neq, ":town_lord_faction", ":alt_faction"),
##diplomacy end+
(neq, ":town_lord_faction", "fac_player_supporters_faction"),
(assign, ":town_lord", -1),
(try_end),
(lt, ":town_lord", 0),
(assign, ":fief_found", ":center"),
(try_end),


(call_script, "script_give_center_to_lord", ":fief_found", "trp_player", 0),
(try_begin),
(faction_slot_eq, "$players_kingdom", slot_faction_political_issue, ":fief_found"),
(faction_set_slot, "$players_kingdom", slot_faction_political_issue, -1),
(try_end),
(str_store_party_name, s4, ":fief_found"),

]],
[anyone|plyr, "spouse_talk",
[
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
"I want to hire a new staff member.", "dplmc_spouse_staff_talk_ask",
[]],
[anyone|plyr, "spouse_talk",
[ ##diplomacy start+
#
##OLD:
#(troop_get_slot, ":player_spouse", "trp_player", slot_troop_spouse),
#(troop_slot_ge, ":player_spouse", slot_troop_cur_center, -1),
##NEW:
(assign, ":player_spouse", "$g_talk_troop"),
(troop_slot_ge, ":player_spouse", slot_troop_cur_center, -1),#what is the point of this?
##Also, to avoid strange bugs, do not enable this for heroes or ministers
(neg|troop_slot_eq, ":player_spouse", slot_troop_occupation, slto_kingdom_hero),
(neq, "$g_talk_troop", "$g_player_minister"),
(neg|troop_slot_ge, ":player_spouse", slot_troop_leaded_party, 1),
(neg|troop_slot_ge, ":player_spouse", slot_troop_prisoner_of_party, 0),
##diplomacy end+

#make sure no spouse party exists
(assign, ":spouse_party_exists", 0),
(try_for_parties, ":spouse_party"),
  (party_slot_eq, ":spouse_party", slot_party_type, dplmc_spt_spouse),
  (assign, ":spouse_party_exists", 1),
(try_end),
(neq, ":spouse_party_exists", 1),

],
"Can you please buy some bread?", "dplmc_spouse_talk_buy_food_amount_ask",
[]],
[anyone|plyr, "minister_talk",
[
(troop_get_slot, ":player_spouse", "trp_player", slot_troop_spouse),
(neq,"$g_talk_troop",":player_spouse"), #only if spouse != minister
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
"I want to hire a new staff member.", "dplmc_minister_staff_talk_ask",
[]],
[anyone|plyr,"script_dplmc_affiliate_confirm", [],
"I do not want to be related to your house anymore.", "dplmc_lord_family_affiliate_leave",[
]],
[anyone|plyr,"script_dplmc_affiliate_confirm", [],
"Oh nothing.", "lord_pretalk",[
]],
[anyone|plyr, "spouse_talk",
[
(assign, ":has_fief", 0),
(try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
(party_get_slot,  ":lord_troop_id", ":center_no", slot_town_lord),
(eq, ":lord_troop_id", "trp_player"),
(val_add, ":has_fief", 1),
(try_end),
(gt, ":has_fief", 1),
],
"I want to move our residence.", "dplmc_spouse_move_residence_ask",[
]],
[anyone|plyr, "minister_diplomatic_initiative_type_select",
[
(call_script, "script_diplomacy_faction_get_diplomatic_status_with_faction", "$players_kingdom", "$g_faction_selected"),
(is_between, reg0, -1, 1), #no war, no truce
(gt, "$g_player_chamberlain", 0),
],
"Threaten them with war and see what you can squeeze out of them.", "minister_diplomatic_emissary",
[(assign, "$g_initiative_selected", dplmc_npc_mission_threaten_request)]],
[anyone, "event_triggered", [
(store_conversation_troop, "$map_talk_troop"),
(eq, "$map_talk_troop", "$npc_to_rejoin_party"),
(troop_slot_eq, "$g_talk_troop", slot_troop_current_mission, dplmc_npc_mission_threaten_request),
(troop_get_slot, ":string", "$map_talk_troop", slot_troop_honorific),
(str_store_string, 21, ":string"),
  (troop_get_slot, ":mission_object", "$g_talk_troop", slot_troop_mission_object),
   (str_store_faction_name, s31, ":mission_object"),
(call_script, "script_npc_decision_checklist_peace_or_war", ":mission_object", "fac_player_supporters_faction", "$g_talk_troop"),
(assign, "$g_mission_result", reg0),
],
"Well, {s21}, at last I've found you. I have returned from my mission to {s31}.","dplmc_companion_threaten_request_response",
[
(troop_get_slot, ":mission_object", "$g_talk_troop", slot_troop_mission_object),
(store_relation, ":player_relation", ":mission_object", "fac_player_supporters_faction"),
(val_sub, ":player_relation", 3),
(val_max, ":player_relation", 0),
(set_relation, ":mission_object", "fac_player_supporters_faction", ":player_relation"),
]],
[anyone|plyr, "minister_diplomatic_initiative_type_select",
[],
"I want to send a gift.", "dplmc_minister_gift_type",
[(assign, "$g_initiative_selected", npc_mission_peace_request)]],
[anyone, "minister_emissary_dispatch",
[
(str_store_troop_name, s11, "$g_emissary_selected"),
(str_store_faction_name, s12, "$g_faction_selected"),
(this_or_next|eq, "$g_initiative_selected", dplmc_npc_mission_gift_fief_request),
(eq, "$g_initiative_selected", dplmc_npc_mission_gift_horses_request),
(str_store_string, s14, "str_dplmc_bring_gift"),
], "Very well -- I shall send {s11} to the {s12} to {s14}.", "minister_diplomatic_dispatch_confirm",[
]],
[anyone, "event_triggered", [
(store_conversation_troop, "$map_talk_troop"),
(eq, "$map_talk_troop", "$npc_to_rejoin_party"),
(troop_get_slot, ":mission", "$g_talk_troop", slot_troop_current_mission),
(this_or_next|eq, ":mission", dplmc_npc_mission_gift_fief_request),
(eq, ":mission", dplmc_npc_mission_gift_horses_request),
(troop_get_slot, ":string", "$map_talk_troop", slot_troop_honorific),
(str_store_string, 21, ":string"),
(troop_get_slot, ":mission_object", "$g_talk_troop", slot_troop_mission_object),
(str_store_faction_name, s31, ":mission_object"),
],
"Well, {s21}, at last I've found you. I have returned from my mission to {s31}. They were agreeably surprised.","companion_rejoin_response", [
(troop_get_slot, ":dipomacy_var", "$g_talk_troop", dplmc_slot_troop_mission_diplomacy),
(troop_get_slot, ":mission", "$g_talk_troop", slot_troop_current_mission),
(try_begin),
(troop_get_slot, ":mission_object", "$g_talk_troop", slot_troop_mission_object),
(eq, ":mission", dplmc_npc_mission_gift_fief_request),
(call_script, "script_give_center_to_faction", ":dipomacy_var", ":mission_object"),
(assign, ":concession_value", 1),
(try_begin),
 (is_between, ":dipomacy_var", towns_begin, towns_end),
 (assign, ":concession_value", 6),
(else_try),
  (is_between, ":dipomacy_var", castles_begin, castles_end),
  (assign, ":concession_value", 4),
(else_try),
  (is_between, ":dipomacy_var", villages_begin, villages_end),
  (assign, ":concession_value", 2),
(try_end),
(call_script, "script_change_troop_renown", "trp_player", ":concession_value"),
(val_mul, ":concession_value", 2),
(call_script, "script_change_player_relation_with_faction", ":mission_object", ":concession_value"),
(else_try),
(eq, ":mission", dplmc_npc_mission_gift_horses_request),
(try_begin),
  (le, ":dipomacy_var", 3000),
  (call_script, "script_change_player_relation_with_faction", ":mission_object", 2),
  (call_script, "script_change_troop_renown", "trp_player", 1),
(else_try),
  (gt, ":dipomacy_var", 3000),
  (call_script, "script_change_player_relation_with_faction", ":mission_object", 4),
  (call_script, "script_change_troop_renown", "trp_player", 2),
(try_end),
(try_end),
]],
[anyone|plyr, "minister_talk",
[
(is_between, "$g_player_minister", active_npcs_begin, kingdom_ladies_end),
],
"I wish to exchange a prisoner.", "dplmc_minister_exchange_prisoner_ask",
[]],
[anyone, "minister_emissary_dispatch",
[
(str_store_troop_name, s11, "$g_emissary_selected"),
(str_store_faction_name, s12, "$g_faction_selected"),
(eq, "$g_initiative_selected", dplmc_npc_mission_prisoner_exchange),
(str_store_troop_name, s10, "$diplomacy_var"),
(str_store_troop_name, s11, "$diplomacy_var2"),
(str_store_string, s14, "str_dplmc_exchange_prisoner"),
], "Very well -- I shall send {s11} to the {s12} to {s14}.", "minister_diplomatic_dispatch_confirm",[]],
[anyone, "event_triggered", [
(store_conversation_troop, "$map_talk_troop"),
(eq, "$map_talk_troop", "$npc_to_rejoin_party"),

(troop_get_slot, ":mission", "$g_talk_troop", slot_troop_current_mission),
  (eq, ":mission", dplmc_npc_mission_prisoner_exchange),

(troop_get_slot, ":enemy_prisoner", "$g_talk_troop", dplmc_slot_troop_mission_diplomacy),
(troop_get_slot, ":own_prisoner", "$g_talk_troop", dplmc_slot_troop_mission_diplomacy2),

(troop_get_slot, ":own_prison", ":enemy_prisoner", slot_troop_prisoner_of_party),
(troop_get_slot, ":enemy_prison", ":own_prisoner", slot_troop_prisoner_of_party),
(is_between, ":own_prison", walled_centers_begin, walled_centers_end),
(is_between, ":enemy_prison", walled_centers_begin, walkers_end),


(call_script, "script_calculate_ransom_amount_for_troop", ":enemy_prisoner"),
(assign, ":enemy_value", reg0),
(call_script, "script_calculate_ransom_amount_for_troop", ":own_prisoner"),
(assign, ":own_value", reg0),
(ge, ":enemy_value", ":own_value"),

(troop_get_slot, ":string", "$map_talk_troop", slot_troop_honorific),
(str_store_string, 21, ":string"),
(str_store_troop_name, s32, ":enemy_prisoner"),
(str_store_troop_name, s33, ":own_prisoner"),
##diplomacy start+ Make pronouns correct
(call_script, "script_dplmc_store_troop_is_female", ":enemy_prisoner"),
(assign, reg4, reg0),
               ],#Next line, "exchange {s32} against {s33}"  -> "exchange {s32} for {s33}"
"Well, {s21}, at last I've found you.They agreed to exchange {s32} for {s33}. {s33} has accompanied me back here. Do you want to set {s32} free?","dplmc_companion_prisoner_exchange_confirm", [
              ]],
[anyone, "event_triggered", [
(store_conversation_troop, "$map_talk_troop"),
(eq, "$map_talk_troop", "$npc_to_rejoin_party"),

(troop_get_slot, ":mission", "$g_talk_troop", slot_troop_current_mission),
  (eq, ":mission", dplmc_npc_mission_prisoner_exchange),

(troop_get_slot, ":enemy_prisoner", "$g_talk_troop", dplmc_slot_troop_mission_diplomacy),
(troop_get_slot, ":own_prisoner", "$g_talk_troop", dplmc_slot_troop_mission_diplomacy2),

(troop_get_slot, ":string", "$map_talk_troop", slot_troop_honorific),
(str_store_string, 21, ":string"),
(str_store_troop_name, s32, ":enemy_prisoner"),
(str_store_troop_name, s33, ":own_prisoner"),
               ],##diplomacy start+ Change "exchange against" to "exchange for"
"Well, {s21}, at last I've found you. They didn't agree to exchange {s32} for {s33}.","companion_rejoin_response", [
              ]],
[anyone|plyr, "minister_talk",
[
(is_between, "$g_player_minister", active_npcs_begin, kingdom_ladies_end),
(faction_get_slot, ":faction_leader", "fac_player_supporters_faction", slot_faction_leader),
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
(eq, ":faction_leader", "trp_player"),
],
"I want to persuade a lord of joining our clan.", "dplmc_minister_persuasion_fief_ask",
[]],
[anyone, "minister_emissary_dispatch",
[
(str_store_troop_name, s11, "$g_emissary_selected"),
(str_store_faction_name, s12, "$g_faction_selected"),
(eq, "$g_initiative_selected", dplmc_npc_mission_persuasion),
(str_store_troop_name, s13, "$diplomacy_var"),
(str_store_party_name, s14, "$diplomacy_var2"),
##diplomacy start+ Use correct pronoun
(call_script, "script_dplmc_store_troop_is_female", "$diplomacy_var"),
(assign, reg4, reg0),#Next line, "him" -> {reg4?her:him}
], "Very well -- I shall send {s11} to {s12} to persuade {s13} and offer {reg4?her:him} {s14}.", "minister_diplomatic_dispatch_confirm",[
##diplomacy end+
]],
[anyone, "event_triggered", [
(store_conversation_troop, "$map_talk_troop"),
(eq, "$map_talk_troop", "$npc_to_rejoin_party"),
(troop_get_slot, ":mission", "$g_talk_troop", slot_troop_current_mission),
  (eq, ":mission", dplmc_npc_mission_persuasion),
(troop_get_slot, ":string", "$map_talk_troop", slot_troop_honorific),
(str_store_string, 21, ":string"),
  (troop_get_slot, ":mission_object", "$g_talk_troop", slot_troop_mission_object),
   (str_store_faction_name, s30, ":mission_object"),
   (troop_get_slot, ":target_troop", "$g_talk_troop", dplmc_slot_troop_mission_diplomacy),
(str_store_troop_name, s14, ":target_troop"),
 (troop_set_slot, "$g_talk_troop", slot_troop_intrigue_impatience, 500),


(assign, ":no_join", 0),
(str_clear, s40),

  #player is still king
(faction_get_slot, ":faction_leader", "fac_player_supporters_faction", slot_faction_leader),
(try_begin),
  (neq, ":faction_leader", "trp_player"),
  (str_store_string, s40, "@Your leader is not even a daimyo and I shall join you?"),
  (assign, ":no_join", 1),
(try_end),

#player has fief
(assign, ":one_fortress_found", 0),
(try_for_range, ":walled_center", walled_centers_begin, walled_centers_end),
   (this_or_next|party_slot_eq, ":walled_center", slot_town_lord, "$g_talk_troop"),
  (party_slot_eq, ":walled_center", slot_town_lord, "trp_player"),
   (assign, ":one_fortress_found", 1),
(try_end),

(try_begin),
  (eq, ":one_fortress_found", 0),
  (str_store_string, s40, "@{s40} I would never join someone who doesn't own a town or castle."),
  (assign, ":no_join", 1),
(try_end),

(assign, ":enough_renown", 1),
(try_begin),
  (troop_slot_eq, ":target_troop", slot_lord_reputation_type, lrep_martial),
  (this_or_next|lt, "$player_right_to_rule", 10),
  (neg|troop_slot_ge, "trp_player", slot_troop_renown, 400),
  (assign, ":enough_renown", 0),
(else_try),
  (troop_slot_eq, ":target_troop", slot_lord_reputation_type, lrep_upstanding),
  (this_or_next|lt, "$player_right_to_rule", 20),
  (neg|troop_slot_ge, "trp_player", slot_troop_renown, 200),
  (assign, ":enough_renown", 0),
(else_try),
  (troop_slot_eq, ":target_troop", slot_lord_reputation_type, lrep_selfrighteous),
  (this_or_next|lt, "$player_right_to_rule", 10),
  (neg|troop_slot_ge, "trp_player", slot_troop_renown, 200),
  (assign, ":enough_renown", 0),
(else_try),
  (troop_slot_eq, ":target_troop", slot_lord_reputation_type, lrep_cunning),
  (neg|troop_slot_ge, "trp_player", slot_troop_renown, 400),
    (assign, ":enough_renown", 0),
(else_try),
  (neg|troop_slot_ge, "trp_player", slot_troop_renown, 200),
  (assign, ":enough_renown", 0),
(try_end),

(try_begin),
  (eq, ":enough_renown", 0),
  ##diplomacy start+ "to" to "too"
  (str_store_string, s40, "@{s40} I know too little about your leader."),
  ##diplomacy end+
  (assign, ":no_join", 1),
(try_end),

#init random seed
(troop_get_slot, ":temp_ai_seed", ":target_troop", slot_troop_temp_decision_seed),
(store_div, ":persuasion_random", ":temp_ai_seed", 100),  #I used div instead of mod to have a different random value, value generated from (mod 100) will be used in next steps. These two values should be non-related.
##diplomacy start+
(troop_get_slot, ":target_reputation", ":target_troop", slot_lord_reputation_type),
(try_begin),
	(store_mod, reg0, ":target_troop", 2),
	(eq, reg0, 0),
	(val_add, ":persuasion_random", 50),#because we take mod 100, the average effect of this is zero, but it addresses problems such as "all high" or "all low"
(try_end),
(val_mod, ":persuasion_random", 100),#should take mod 100 after division
##diplomacy end+
(val_add, ":persuasion_random", 1),
(store_skill_level, ":persuasion_skill", "skl_persuasion", "$g_talk_troop"),
(val_mul, ":persuasion_skill", 7),
##diplomacy start+
#Add a base success chance, so that skill 5 has a 50% chance of failure instead of a 65% chance of failure.
(val_add, ":persuasion_skill", 15),
##diplomacy end+
(try_begin),
  (lt, ":persuasion_skill", ":persuasion_random"),
##diplomacy start+
##OLD:
#  (str_store_string, s40, "@{s40} Next time I prefer to talk to someone who doesn't act like a fool."),
#  (assign, ":no_join", 1),
##NEW:
  (try_begin),
     (ge, "$cheat_mode", 1),
	 (assign, reg0, ":persuasion_random"),
	 (assign, reg1, ":persuasion_skill"),
	 (display_message, "@{!} Emissary persuasion attempt: skill factor {reg1} versus random number {reg0}"),
  (try_end),
  (store_mul, reg0, ":persuasion_skill", 2),
  (try_begin),
     (this_or_next|ge, reg0, ":persuasion_random"),
		(eq, ":target_reputation", lrep_goodnatured),
	 (neq, ":target_reputation", lrep_debauched),
	 (neq, ":target_reputation", lrep_quarrelsome),
	 (str_store_string, s40, "@{s40} I found your messenger unconvincing."),
  (else_try),
	 (this_or_next|eq, ":target_reputation", lrep_debauched),
	 (this_or_next|eq, ":target_reputation", lrep_quarrelsome),
	 (this_or_next|eq, ":target_reputation", lrep_selfrighteous),
	 (this_or_next|eq, ":target_reputation", lrep_ambitious),
		(is_between, ":target_reputation", lrep_roguish, lrep_conventional),
     (str_store_string, s40, "@{s40} Next time I would prefer to talk to someone who doesn't act like a fool."),
  (else_try),
     (str_store_string, s40, "@{s40} Next time I would prefer to talk to someone more versed in courtly manners."),
  (try_end),
  (assign, ":no_join", 1),
(try_end),
##diplomacy end+

   (call_script, "script_calculate_troop_political_factors_for_liege", ":target_troop", "trp_player"),
   (assign, ":result_for_security", reg2),
(assign, ":result_for_political", reg4),
   (assign, ":change_penalty", reg10),
   (assign, ":result_for_new_liege", reg0),
   (store_faction_of_troop, ":target_faction", ":target_troop"),
   (faction_get_slot, ":cur_liege", ":target_faction", slot_faction_leader),
   (call_script, "script_calculate_troop_political_factors_for_liege", ":target_troop", ":cur_liege"),

   (store_sub, ":result_for_security_comparative", ":result_for_security", reg2),
   (store_sub, ":result_for_political_comparative", ":result_for_political", reg4),
   (assign, ":result_for_old_liege", reg0),
   (store_sub, "$pledge_chance", ":result_for_new_liege", ":result_for_old_liege"),
   (val_add, "$pledge_chance", 50),
   (val_div, "$pledge_chance", 2),

(store_mod, ":random", ":temp_ai_seed", 100),

(try_begin),
  (eq, "$cheat_mode", 1),
  (assign, reg2, ":result_for_security"),
  (display_message, "@{!}DEBUG - result_for_security: {reg2} > 10"),
  (assign, reg2, ":result_for_political"),
  (display_message, "@{!}DEBUG - result_for_political: {reg2} > 0"),
  (assign, reg2, ":change_penalty"),
  (display_message, "@{!}DEBUG - change_penalty: {reg2} < 20"),
  (assign, reg2, ":random"),
  (display_message, "@{!}DEBUG - random: {reg2}"),
  (assign, reg2, "$pledge_chance"),
  (display_message, "@{!}DEBUG - > pledge_chance: {reg2}"),
  (assign, reg2, ":result_for_security_comparative"),
  (display_message, "@{!}DEBUG - result_for_security_comparative: {reg2} > 0"),
  (assign, reg2, ":result_for_political_comparative"),
  (display_message, "@{!}DEBUG - result_for_political_comparative: {reg2} > 0"),
(try_end),

(try_begin),
  (le, ":random", "$pledge_chance"),
  (assign, ":no_join", 1),
  (str_store_string, s40, "@{s40} I rather stay with my current overlord."),
(try_end),

(try_begin),
  (eq, ":no_join", 0),
   (try_begin),
      (lt, ":result_for_political", 0),
    (assign, ":no_join", 1),

      (try_begin),
         (troop_slot_eq, ":target_troop", slot_lord_reputation_type, lrep_upstanding),
         (str_store_string, s31, "str_i_worry_about_those_with_whom_you_have_chosen_to_surround_yourself" ),
      (else_try),
         (troop_slot_eq, ":target_troop", slot_lord_reputation_type, lrep_martial),
         (str_store_string, s31, "str_there_are_some_outstanding_matters_between_me_and_some_of_your_vassals_"),
         (try_begin),
           (assign, reg41, ":result_for_political"),
           ##diplomacy start+ Only show debug messages with cheat mode on
           (ge, "$cheat_mode", 1),
           ##diplomacy end+
           (display_message, "str_result_for_political_=_reg41"),
         (try_end),
      (else_try),
         (troop_slot_eq, ":target_troop", slot_lord_reputation_type, lrep_quarrelsome),
         (str_store_string, s31, "str_my_liege_has_his_faults_but_i_dont_care_for_your_toadies"),
      (else_try),
         (troop_slot_eq, ":target_troop", slot_lord_reputation_type, lrep_goodnatured),
         (str_store_string, s31, "str_i_think_youre_a_good_man_but_im_worried_that_you_might_be_pushed_in_the_wrong_direction_by_some_of_those_around_you"),
      (else_try),
         (troop_slot_eq, ":target_troop", slot_lord_reputation_type, lrep_selfrighteous),
         (str_store_string, s31, "str_i_am_loathe_to_fight_alongside_you_so_long_as_you_take_under_your_wing_varlots_and_base_men"),
      (else_try),
         (troop_slot_eq, ":target_troop", slot_lord_reputation_type, lrep_cunning),
         (str_store_string, s31, "str_ill_be_honest__with_some_of_those_who_follow_you_i_think_id_be_more_comfortable_fighting_against_you_than_with_you"),
      (else_try),
         (troop_slot_eq, ":target_troop", slot_lord_reputation_type, lrep_debauched),
         (str_store_string, s31, "str_i_say_that_you_can_judge_a_man_by_the_company_he_keeps_and_you_have_surrounded_yourself_with_vipers_and_vultures"),
      (else_try),
         (troop_slot_ge, ":target_troop", slot_lord_reputation_type, lrep_roguish),
         (str_store_string, s31, "str_you_know_that_i_have_always_had_a_problem_with_some_of_our_companions"),
      (try_end),
   (else_try),
      (lt, ":result_for_political_comparative", 0),
      (assign, ":no_join", 1),
      (str_store_string, s31, "str_politically_i_would_be_a_better_position_in_the_court_of_my_current_liege_than_in_yours"),
   (else_try),
      (str_store_string, s31, "str_i_am_more_comfortable_with_you_and_your_companions_than_with_my_current_liege"),
   (try_end),

   (try_begin),
      (lt, ":result_for_security", 10),
      (assign, ":no_join", 1),

      (try_begin),
         (this_or_next|troop_slot_eq, ":target_troop", slot_lord_reputation_type, lrep_cunning),
         (troop_slot_ge, ":target_troop", slot_lord_reputation_type, lrep_roguish),
         (str_store_string, s32, "str_militarily_youre_in_no_position_to_protect_me_should_i_be_attacked_id_be_reluctant_to_join_you_until_you_could"),
      (else_try),
         (troop_slot_eq, ":target_troop", slot_lord_reputation_type, lrep_upstanding),
         (str_store_string, s32, "str_militarily_when_i_consider_the_lay_of_the_land_i_realize_that_to_pledge_myself_to_you_now_would_endanger_my_faithful_retainers_and_my_family"),
      (else_try),
         (troop_slot_eq, ":target_troop", slot_lord_reputation_type, lrep_martial),
         (str_store_string, s32, "str_militarily_youre_in_no_position_to_come_to_my_help_if_someone_attacked_me_i_dont_mind_a_good_fight_but_i_like_to_have_a_chance_of_winning"),
      (else_try),
         (troop_slot_eq, ":target_troop", slot_lord_reputation_type, lrep_goodnatured),
         (str_store_string, s32, "str_militarily_youre_in_no_position_to_come_to_my_help_if_someone_attacked_me_i_dont_mind_a_good_fight_but_i_like_to_have_a_chance_of_winning"),
      (else_try),
         (troop_slot_eq, ":target_troop", slot_lord_reputation_type, lrep_debauched),
         (str_store_string, s32, "str_militarily_you_would_have_me_join_you_only_to_find_myself_isolated_amid_a_sea_of_enemies"),
      (else_try),
         (troop_slot_eq, ":target_troop", slot_lord_reputation_type, lrep_selfrighteous),
         (str_store_string, s32, "str_militarily_you_would_have_me_join_you_only_to_find_myself_isolated_amid_a_sea_of_enemies"),
      (else_try),
         (troop_slot_eq, ":target_troop", slot_lord_reputation_type, lrep_quarrelsome),
         (str_store_string, s32, "str_militarily_youre_in_no_position_to_come_to_my_help_if_someone_attacked_me_youd_let_me_be_cut_down_like_a_dog_id_bet"),
      (try_end),
   (else_try),
      (lt, ":result_for_security_comparative", 0),
      (assign, ":no_join", 1),
      (str_store_string, s32, "str_militarily_i_wouldnt_be_any_safer_if_i_joined_you"),
   (else_try),
      (str_store_string, s32, "str_militarily_i_might_be_safer_if_i_joined_you"),
   (try_end),

   (try_begin),
      (gt, ":change_penalty", 40),
      (assign, ":no_join", 1),
      (str_store_string, s34, "str_finally_there_is_a_cost_to_ones_reputation_to_change_sides_in_this_case_the_cost_would_be_very_high"),
   (else_try),
      (gt, ":change_penalty", 20),
      (assign, ":no_join", 1),
      (str_store_string, s34, "str_finally_there_is_a_cost_to_ones_reputation_to_change_sides_in_this_case_the_cost_would_be_significant"),
   (else_try),
      (str_store_string, s34, "str_finally_there_is_a_cost_to_ones_reputation_to_change_sides_in_this_case_however_many_men_would_understand"),
   (try_end),
   (str_store_string, s40, "@{s31} {s32} {s34}"),
(try_end),

(eq, ":no_join", 1),
##diplomacy start+ use reg0 for gender
(call_script, "script_dplmc_store_troop_is_female", ":target_troop"),
],#Next line "He" to {reg0?She:he}
"Well, {s21}, at last I've found you. I have returned from my persuasion mission to {s30}. {s14} doesn't want to join you. {reg0?She:He} said: {s40}","companion_rejoin_response",
##diplomacy end+
[
]],
[anyone, "event_triggered", [
(store_conversation_troop, "$map_talk_troop"),
(eq, "$map_talk_troop", "$npc_to_rejoin_party"),
(troop_get_slot, ":mission", "$g_talk_troop", slot_troop_current_mission),
  (eq, ":mission", dplmc_npc_mission_persuasion),
(troop_get_slot, ":string", "$map_talk_troop", slot_troop_honorific),
(str_store_string, 21, ":string"),
  (troop_get_slot, ":mission_object", "$g_talk_troop", slot_troop_mission_object),
   (str_store_faction_name, s31, ":mission_object"),
   (troop_get_slot, ":target_troop", "$g_talk_troop", dplmc_slot_troop_mission_diplomacy),

(str_store_troop_name, s14, ":target_troop"),
               ],
"Well, {s21}, at last I've found you. I have returned from my persuasion mission to {s31}. {s14} agreed to join you.","companion_rejoin_response", [
   (troop_get_slot, ":target_troop", "$g_talk_troop", dplmc_slot_troop_mission_diplomacy),
(call_script, "script_change_troop_faction", ":target_troop", "$players_kingdom"),

(store_faction_of_troop, ":target_faction", ":target_troop"),
(faction_get_slot, ":other_liege", ":target_faction", slot_faction_leader),
(try_begin),
  (store_relation, ":relation", "$players_kingdom", ":target_faction"),
  (ge, ":relation", 0),

  (call_script, "script_add_log_entry", logent_border_incident_troop_suborns_lord, "trp_player", -1, ":target_troop",":target_faction"),
  (store_add, ":slot_provocation_days", "$players_kingdom", slot_faction_provocation_days_with_factions_begin),
  (val_sub, ":slot_provocation_days", kingdoms_begin),
  #gekokujo 3.0 provocation days increase start
  (faction_set_slot, ":target_faction", ":slot_provocation_days", 60),
  #(faction_set_slot, ":target_faction", ":slot_provocation_days", 30),
  #gekokujo 3.0 provocation days increase end

  (faction_get_slot, ":other_liege", ":target_faction", slot_faction_leader),
  (call_script, "script_troop_change_relation_with_troop", "trp_player", ":other_liege", -3),
(try_end),

  (call_script, "script_change_player_right_to_rule", 2),
]],
[anyone|plyr, "minister_talk",
[
(is_between, "$g_player_minister", active_npcs_begin, kingdom_ladies_end),
],
"I wish to spy out another clan.", "dplmc_minister_spy_kingdoms",
[]],
[anyone, "minister_emissary_dispatch",
[
(str_store_troop_name, s11, "$g_emissary_selected"),
(str_store_faction_name, s12, "$g_faction_selected"),
(eq, "$g_initiative_selected", dplmc_npc_mission_spy_request),
(str_store_string, s14, "str_dplmc_gather_information"),
(store_skill_level, ":emissary_spotting", "skl_spotting", "$g_emissary_selected"),
(val_mul, ":emissary_spotting", 5),
(val_add, ":emissary_spotting", 65),
(val_min, ":emissary_spotting", 95),
(store_random_in_range, ":random", 0, 100),

(try_begin),#debug
(eq, "$cheat_mode", 1),
(assign, reg0, ":emissary_spotting"),
(display_message, "@{!}DEBUG : emissary_spotting: {reg0}"),
(assign, reg0, ":random"),
(display_message, "@{!}DEBUG : random: {reg0}"),
(try_end),

(try_begin),
(ge, ":emissary_spotting", ":random"),
(assign, "$diplomacy_var", 0), # not caught
(else_try),
 (lt, ":emissary_spotting", ":random"),
 (assign, "$diplomacy_var", 1), # caught
(try_end),
], "Very well -- I shall send {s11} to the {s12} to {s14}.", "minister_diplomatic_dispatch_confirm",[]],
[anyone, "event_triggered", [
    (store_conversation_troop, "$map_talk_troop"),
    (eq, "$map_talk_troop", "$npc_to_rejoin_party"),
    (troop_get_slot, ":mission", "$g_talk_troop", slot_troop_current_mission),
    (eq, ":mission", dplmc_npc_mission_spy_request),
    (troop_get_slot, ":emissary_caught", "$g_talk_troop", dplmc_slot_troop_mission_diplomacy),
    (troop_get_slot, ":mission_object", "$g_talk_troop", slot_troop_mission_object),
    (this_or_next|eq, ":emissary_caught", 0),
    (faction_slot_eq, ":mission_object", slot_faction_state, sfs_defeated),
    (troop_get_slot, ":string", "$map_talk_troop", slot_troop_honorific),
    (str_store_string, 21, ":string"),
    (str_store_faction_name, s31, ":mission_object"),
],
"Well, {s21}, at last I've found you. I have returned from my reconnaissance mission to {s31}. About which location do you need information?","dplmc_companion_spy_request_select_center", [
              ]],
[trp_hired_warrior_veteran, "event_triggered", [
    (store_conversation_troop, "$map_talk_troop"),
    (troop_get_slot, "$g_talk_troop", "$g_talk_troop", slot_troop_mission_object), #switching npc
    (troop_get_slot, ":mission", "$g_talk_troop", slot_troop_current_mission),
    (eq, ":mission", dplmc_npc_mission_spy_request),
    (troop_get_slot, ":emissary_caught", "$g_talk_troop", dplmc_slot_troop_mission_diplomacy),
	(gt, ":emissary_caught", 0),

    (troop_get_slot, ":mission_object", "$g_talk_troop", slot_troop_mission_object),
    (str_store_faction_name, s31, ":mission_object"),
    (str_store_troop_name, s11, "$g_talk_troop"),
               ],
"My, lord. I am coming back from the reconnaissance mission to {s31}. I am sorry, we were caught  off  guard and they got {s11}. I barely escaped.","close_window", [
  (troop_set_slot, "$g_talk_troop", slot_troop_current_mission, 0),
  (troop_set_slot, "$g_talk_troop", slot_troop_days_on_mission, 0),
  (troop_set_slot, "$g_talk_troop", slot_troop_occupation, 0),
  (assign, "$npc_to_rejoin_party", 0),

  (troop_get_slot, ":mission_object", "$g_talk_troop", slot_troop_mission_object),

  (call_script, "script_change_player_relation_with_faction", ":mission_object", -3),
  (call_script, "script_change_player_honor", -2),
  (call_script, "script_change_troop_renown", "trp_player", -5),

  (faction_get_slot, ":faction_leader", ":mission_object", slot_faction_leader),
  (call_script, "script_lord_get_home_center", ":faction_leader"),
  (try_begin),
    (neq, reg0, -1),
    (assign, ":target_party", reg0),
  (else_try),
    (try_for_range, ":walled_center", walled_centers_begin, walled_centers_end),
      (store_faction_of_party, ":center_faction", ":walled_center"),
         (eq, ":mission_object", ":center_faction"),
         (assign, ":target_party", ":walled_center"),
       (try_end),
  (try_end),
  (try_begin),
    (is_between, ":target_party", walled_centers_begin, walled_centers_end),
    (party_add_prisoners, ":target_party", "$g_talk_troop", 1),
  (try_end),
]],
[anyone|plyr, "minister_diplomatic_initiative_type_select",
[
(call_script, "script_diplomacy_faction_get_diplomatic_status_with_faction", "fac_player_supporters_faction", "$g_faction_selected"),
(eq, reg0, 1),  #player is at truce with the mission_faction

(assign, ":proceed", 0),
(try_begin),
(store_add, ":slot_truce_days", "$g_faction_selected", slot_faction_truce_days_with_factions_begin),
(val_sub, ":slot_truce_days", kingdoms_begin),
(faction_get_slot, ":truce_days", "fac_player_supporters_faction", ":slot_truce_days"),
(is_between, ":truce_days", 20, 50), #you need a trade aggreement or defensive pact for an alliance
(assign, ":proceed", 1),
(try_end),
(eq, ":proceed", 1),

(faction_slot_eq, "$g_faction_selected", slot_faction_recognized_player, 1), #recognized us
(faction_slot_eq, "$g_faction_selected", slot_faction_state, sfs_active),
(faction_get_slot, ":leader_no", "$g_faction_selected", slot_faction_leader),

(str_store_troop_name, s10, ":leader_no"),
(str_store_faction_name, s11, "$g_faction_selected"),
(str_clear, s14),
],
"Tell {s10} that I want to form an alliance with him.", "minister_diplomatic_emissary",
[ (assign, "$g_initiative_selected", dplmc_npc_mission_alliance_request),
]],
[anyone, "event_triggered", [
     (store_conversation_troop, "$map_talk_troop"),
     (eq, "$map_talk_troop", "$npc_to_rejoin_party"),
     (troop_get_slot, ":mission", "$g_talk_troop", slot_troop_current_mission),
          (eq, ":mission", dplmc_npc_mission_alliance_request),

          (troop_get_slot, ":string", "$map_talk_troop", slot_troop_honorific),
     (str_store_string, 21, ":string"),
          (troop_get_slot, ":mission_object", "$g_talk_troop", slot_troop_mission_object),
          (str_store_faction_name, s31, ":mission_object"),

          (call_script, "script_npc_decision_checklist_peace_or_war", ":mission_object", "fac_player_supporters_faction", "$g_talk_troop"),
          (assign, "$g_mission_result_with_player", reg0),
               ],
"Well, {s21}, at last I've found you. I have returned from my mission to {s31}. ","dplmc_companion_alliance_request_response", [
              ]],
[anyone|plyr, "minister_diplomatic_initiative_type_select",
[
(call_script, "script_diplomacy_faction_get_diplomatic_status_with_faction", "fac_player_supporters_faction", "$g_faction_selected"),
(eq, reg0, 1),  #player is at truce with the mission_faction

(assign, ":proceed", 0),
(try_begin),
(store_add, ":slot_truce_days", "$g_faction_selected", slot_faction_truce_days_with_factions_begin),
(val_sub, ":slot_truce_days", kingdoms_begin),
(faction_get_slot, ":truce_days", "fac_player_supporters_faction", ":slot_truce_days"),
#(gt, ":truce_days", 20), #if we have more than 20 truce days left don't proceed
(is_between, ":truce_days", 0, 30), #you need a non-aggression or trade aggreement for an defensive pact
(assign, ":proceed", 1),
(try_end),
(eq, ":proceed", 1),

(faction_slot_eq, "$g_faction_selected", slot_faction_recognized_player, 1), #recognized us
(faction_slot_eq, "$g_faction_selected", slot_faction_state, sfs_active),
(faction_get_slot, ":leader_no", "$g_faction_selected", slot_faction_leader),

(str_store_troop_name, s10, ":leader_no"),
(str_store_faction_name, s11, "$g_faction_selected"),
(str_clear, s14),
###diplomacy start+ Use reg0 for gender
(call_script, "script_dplmc_store_troop_is_female", ":leader_no"),
],#Next line "him" to {reg0?her:him}
"Tell {s10} that I want to conclude a defensive pact with {reg0?her:him}.", "minister_diplomatic_emissary",
##diplomacy end+
[ (assign, "$g_initiative_selected", dplmc_npc_mission_defensive_request),
]],
[anyone, "event_triggered", [
     (store_conversation_troop, "$map_talk_troop"),
     (eq, "$map_talk_troop", "$npc_to_rejoin_party"),
     (troop_get_slot, ":mission", "$g_talk_troop", slot_troop_current_mission),
          (eq, ":mission", dplmc_npc_mission_defensive_request),

          (troop_get_slot, ":string", "$map_talk_troop", slot_troop_honorific),
     (str_store_string, 21, ":string"),
          (troop_get_slot, ":mission_object", "$g_talk_troop", slot_troop_mission_object),
          (str_store_faction_name, s31, ":mission_object"),

          (call_script, "script_npc_decision_checklist_peace_or_war", ":mission_object", "fac_player_supporters_faction", "$g_talk_troop"),
          (assign, "$g_mission_result_with_player", reg0),
               ],
"Well, {s21}, at last I've found you. I have returned from my mission to {s31}. ","dplmc_companion_defensive_request_response", [
              ]],
[anyone|plyr, "minister_diplomatic_initiative_type_select",
[
(call_script, "script_diplomacy_faction_get_diplomatic_status_with_faction", "fac_player_supporters_faction", "$g_faction_selected"),
(ge, reg0, 0),  #player is at peace or truce with the mission_faction

(assign, ":proceed", 0),
(try_begin),
(store_add, ":slot_truce_days", "$g_faction_selected", slot_faction_truce_days_with_factions_begin),
(val_sub, ":slot_truce_days", kingdoms_begin),
(faction_get_slot, ":truce_days", "fac_player_supporters_faction", ":slot_truce_days"),
(lt, ":truce_days", 10), #you need a non-aggression or peace for a trade pact
(assign, ":proceed", 1),
(try_end),
(eq, ":proceed", 1),

(faction_slot_eq, "$g_faction_selected", slot_faction_recognized_player, 1), #recognized us
(faction_slot_eq, "$g_faction_selected", slot_faction_state, sfs_active),
(faction_get_slot, ":leader_no", "$g_faction_selected", slot_faction_leader),

(str_store_troop_name, s10, ":leader_no"),
(str_store_faction_name, s11, "$g_faction_selected"),
(str_clear, s14),
##diplomacy start+ correct pronouns
(call_script, "script_dplmc_store_troop_is_female", ":leader_no"),
],
"Tell {s10} that I want to sign a trade agreement with {reg0?her:him}.", "minister_diplomatic_emissary",
##diplomacy end+
[ (assign, "$g_initiative_selected", dplmc_npc_mission_trade_request),
]],
[anyone, "event_triggered", [
     (store_conversation_troop, "$map_talk_troop"),
     (eq, "$map_talk_troop", "$npc_to_rejoin_party"),
     (troop_get_slot, ":mission", "$g_talk_troop", slot_troop_current_mission),
          (eq, ":mission", dplmc_npc_mission_trade_request),

          (troop_get_slot, ":string", "$map_talk_troop", slot_troop_honorific),
     (str_store_string, 21, ":string"),
          (troop_get_slot, ":mission_object", "$g_talk_troop", slot_troop_mission_object),
          (str_store_faction_name, s31, ":mission_object"),

          (call_script, "script_npc_decision_checklist_peace_or_war", ":mission_object", "fac_player_supporters_faction", "$g_talk_troop"),
          (assign, "$g_mission_result_with_player", reg0),
               ],
"Well, {s21}, at last I've found you. I have returned from my mission to {s31}. ","dplmc_companion_trade_request_response", [
              ]],
[anyone|plyr, "minister_diplomatic_initiative_type_select",
[
(call_script, "script_diplomacy_faction_get_diplomatic_status_with_faction", "fac_player_supporters_faction", "$g_faction_selected"),
(eq, reg0, 0),  #player is at peace

(faction_slot_eq, "$g_faction_selected", slot_faction_state, sfs_active),
(faction_get_slot, ":leader_no", "$g_faction_selected", slot_faction_leader),

(str_store_troop_name, s10, ":leader_no"),
(str_store_faction_name, s11, "$g_faction_selected"),
(str_clear, s14),
###diplomacy start+ Use reg0 for gender
(call_script, "script_dplmc_store_troop_is_female", ":leader_no"),
],#next line "him" to {reg0?her:him}
"Tell {s10} that I want to conclude a non-aggression treaty with {reg0?her:him}.", "minister_diplomatic_emissary",
##diplomacy end+
[ (assign, "$g_initiative_selected", dplmc_npc_mission_nonaggression_request),
]],
[anyone, "event_triggered", [
     (store_conversation_troop, "$map_talk_troop"),
     (eq, "$map_talk_troop", "$npc_to_rejoin_party"),
     (troop_get_slot, ":mission", "$g_talk_troop", slot_troop_current_mission),
          (eq, ":mission", dplmc_npc_mission_nonaggression_request),

          (troop_get_slot, ":string", "$map_talk_troop", slot_troop_honorific),
     (str_store_string, 21, ":string"),
          (troop_get_slot, ":mission_object", "$g_talk_troop", slot_troop_mission_object),
          (str_store_faction_name, s31, ":mission_object"),

          (call_script, "script_npc_decision_checklist_peace_or_war", ":mission_object", "fac_player_supporters_faction", "$g_talk_troop"),
          (assign, "$g_mission_result_with_player", reg0),
               ],
"Well, {s21}, at last I've found you. I have returned from my mission to {s31}. ","dplmc_companion_nonaggression_request_response", [
              ]],
[anyone|plyr|repeat_for_factions, "minister_diplomatic_initiative_type_select",
[
(assign, ":proceed", 1),
(try_begin),
(eq, reg0, 2), #truce
(store_add, ":slot_truce_days", "$g_faction_selected", slot_faction_truce_days_with_factions_begin),
(val_sub, ":slot_truce_days", kingdoms_begin),
(faction_get_slot, ":truce_days", "fac_player_supporters_faction", ":slot_truce_days"),
(gt, ":truce_days", 0), #you need at least a non-aggression pact
(assign, ":proceed", 0),
(try_end),
(eq, ":proceed", 1),

(store_repeat_object, ":faction_no"),
(is_between, ":faction_no", kingdoms_begin, kingdoms_end),
(neq, ":faction_no", "fac_player_supporters_faction"),
(neq, ":faction_no", "$g_faction_selected"),
(call_script, "script_diplomacy_faction_get_diplomatic_status_with_faction", "fac_player_supporters_faction", ":faction_no"),
(eq, reg0, -2), #player is at war with the target faction
(call_script, "script_diplomacy_faction_get_diplomatic_status_with_faction", "fac_player_supporters_faction", "$g_faction_selected"),
(ge, reg0, 0),  #player is at peace or truce with the mission_faction
(call_script, "script_diplomacy_faction_get_diplomatic_status_with_faction", "$g_faction_selected", ":faction_no"),
(is_between, reg0, -1, 1),  #mission_faction provocated or peace with target_faction
(faction_slot_eq, "$g_faction_selected", slot_faction_recognized_player, 1), #recognized us
(faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
(faction_get_slot, ":leader_no", ":faction_no", slot_faction_leader),
(str_store_troop_name, s10, ":leader_no"),
(str_store_faction_name, s11, ":faction_no"),
(str_clear, s14),
###diplomacy start+ Use reg0 for gender
(call_script, "script_dplmc_store_troop_is_female", ":leader_no"),
],#next line "him" to {reg0?her:him}
"That I want {reg0?her:him} to help me and attack {s11}{s14}.", "minister_diplomatic_emissary",
##diplomacy end+
[ (assign, "$g_initiative_selected", dplmc_npc_mission_war_request),
(store_repeat_object, "$diplomacy_var"),
]],
[anyone, "event_triggered", [
(store_conversation_troop, "$map_talk_troop"),
(eq, "$map_talk_troop", "$npc_to_rejoin_party"),
(troop_get_slot, ":mission", "$g_talk_troop", slot_troop_current_mission),
(eq, ":mission", dplmc_npc_mission_war_request),

(troop_get_slot, ":string", "$map_talk_troop", slot_troop_honorific),
(str_store_string, 21, ":string"),
(troop_get_slot, ":mission_object", "$g_talk_troop", slot_troop_mission_object),
(str_store_faction_name, s31, ":mission_object"),

(call_script, "script_npc_decision_checklist_peace_or_war", ":mission_object", "fac_player_supporters_faction", "$g_talk_troop"),
(assign, "$g_mission_result_with_player", reg0),
(call_script, "script_npc_decision_checklist_peace_or_war", ":mission_object", "$diplomacy_var", -1),
(assign, "$g_mission_result_with_target", reg0),
##diplomacy start+
#Disable agreeing to declare war when the kingdoms are allied.
#Make it less likely when they have other treaties.
(call_script, "script_dplmc_get_faction_truce_length_with_faction", ":mission_object", "$diplomacy_var"),
(try_begin),
	#TODO: Later there should be other intrigue options, but for now let's just
	#make it so refusal is automatic for alliances, and possible for other types.
	(gt, reg0, dplmc_treaty_defense_days_expire),
	(val_max, "$g_mission_result_with_target", 3),#Positive means does not want war
(else_try),
	(gt, reg0, dplmc_treaty_truce_days_expire),
	(store_random_in_range, reg0, 0, 2),
	(try_begin),
		(eq, reg0, 1),
		(val_max, "$g_mission_result_with_target", 3),#Positive means does not want war
	(else_try),
		(val_add, "$g_mission_result_with_target", 1),#If was undecided, choose no
		(val_max, "$g_mission_result_with_target", 0),#Best result is "undecided"
	(try_end),
(try_end),
##diplomacy end+
               ],
"Well, {s21}, at last I've found you. I have returned from my mission to {s31}. ","dplmc_companion_war_request_response", [
              ]],
[anyone|plyr, "minister_talk",
[],
"That is all for now.", "close_window",
[]],
[anyone, "minister_change_marshal",
[],
"Who should be the new strategist?", "minister_change_marshal_choose",
[]],
[anyone|plyr, "minister_change_marshal_choose",
[],
"I shall be the strategist", "minister_pretalk",
[
(call_script, "script_appoint_faction_marshall", "fac_player_supporters_faction", "trp_player"),
(store_current_hours, ":hours"),
(assign, "$g_recalculate_ais", 1),
(assign, "$g_player_faction_last_marshal_appointment", ":hours"),

##diplomacy start+ Handle player is co-ruler of NPC kingdom
#Added section begin
(assign, ":ruled_faction", "fac_player_supporters_faction"),
(try_begin),
	(neg|faction_slot_eq, "fac_player_supporters_faction", slot_faction_state, sfs_active),
	(is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
	(call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", "$players_kingdom"),
	(ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
	(assign, ":ruled_faction", "$players_kingdom"),
(try_end),
#Added section end
#In the following section, replace references to "fac_player_supporter_faction" with ":ruled_faction"
(try_begin),
	#(faction_slot_eq, "fac_player_supporters_faction", slot_faction_political_issue, 1),
	#(faction_set_slot, "fac_player_supporters_faction", slot_faction_political_issue, 0),
	(faction_slot_eq, ":ruled_faction", slot_faction_political_issue, 1),
	(faction_set_slot, ":ruled_faction", slot_faction_political_issue, 0),
	(faction_set_slot, "fac_player_supporters_faction", slot_faction_political_issue, 0),

	(troop_set_slot, "trp_player",  slot_troop_stance_on_faction_issue, -1),
	#Also change to support promoted kingdom ladies
	#(try_for_range, ":active_npc", active_npcs_begin, active_npcs_end),
	(try_for_range, ":active_npc", heroes_begin, heroes_end),
	   (this_or_next|is_between, ":active_npc", active_npcs_begin, active_npcs_end),
	      (troop_slot_eq, ":active_npc", slot_troop_occupation, slto_kingdom_hero),
	   (store_faction_of_troop, ":active_npc_faction", ":active_npc"),
	   (eq, ":active_npc_faction", ":ruled_faction"),
	   (troop_set_slot, ":active_npc", slot_troop_stance_on_faction_issue, -1),
	(try_end),
(try_end),
##diplomacy end+
]],
[anyone|plyr, "minister_change_marshal_choose",
[],
"For a short while, we should have no strategist", "minister_pretalk",
[
##diplomacy start+ Handle player is co-ruler of NPC kingdom
#Added section begin
(assign, ":ruled_faction", "fac_player_supporters_faction"),
(try_begin),
	(neg|faction_slot_eq, "fac_player_supporters_faction", slot_faction_state, sfs_active),
	(is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
	(call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", "$players_kingdom"),
	(ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
	(assign, ":ruled_faction", "$players_kingdom"),
(try_end),
#Added section end
#In the following section, replace references to "fac_player_supporter_faction" with ":ruled_faction"
(call_script, "script_appoint_faction_marshall", ":ruled_faction", -1),
(try_begin),
	(faction_slot_eq, ":ruled_faction", slot_faction_political_issue, 1),
	(faction_set_slot, ":ruled_faction", slot_faction_political_issue, 0),
	(faction_set_slot, "fac_player_supporters_faction", slot_faction_political_issue, 0),#if not the same as ruled faction

	(troop_set_slot, "trp_player",  slot_troop_stance_on_faction_issue, -1),
	(try_for_range, ":active_npc", heroes_begin, heroes_end),#Also change this to support all herose
	   (this_or_next|is_between, ":active_npc", active_npcs_begin, active_npcs_end),
	      (troop_slot_eq, ":active_npc", slot_troop_occupation, slto_kingdom_hero),
	   (store_faction_of_troop, ":active_npc_faction", ":active_npc"),
	   (eq, ":active_npc_faction", ":ruled_faction"),
	   (troop_set_slot, ":active_npc", slot_troop_stance_on_faction_issue, -1),
	(try_end),
(try_end),
##diplomacy end+ (replacing fac_player_supporters_faction with :ruled_faction)
(assign, "$g_recalculate_ais", 1),

]],
[anyone|plyr|repeat_for_troops, "minister_change_marshal_choose",
[
(store_repeat_object, ":lord"),
##diplomacy start+ support promoted ladies
#(is_between, ":lord", active_npcs_begin, active_npcs_end),
(is_between, ":lord", heroes_begin, heroes_end),
##diplomacy end+
(troop_slot_eq, ":lord", slot_troop_occupation, slto_kingdom_hero),
(store_faction_of_troop, ":lord_faction", ":lord"),
##diplomacy start+ Handle player is co-ruler of NPC kingdom
(assign, ":is_faction_member", 0),
(try_begin),
	(eq, ":lord_faction", "$players_kingdom"),
	(is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
	(call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", "$players_kingdom"),
	(ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
	(assign, ":is_faction_member", 1),
(try_end),
(this_or_next|eq, ":is_faction_member", 1),
##diplomacy end+
(eq, ":lord_faction", "fac_player_supporters_faction"),
(str_store_troop_name, s4, ":lord"),
],
"{s4}", "minister_pretalk",
[
(store_repeat_object, ":lord"),
##diplomacy start+ Handle player is co-ruler of NPC kingdom
#Added section begin
(assign, ":ruled_faction", "fac_player_supporters_faction"),
(try_begin),
	(neg|faction_slot_eq, "fac_player_supporters_faction", slot_faction_state, sfs_active),
	(is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
	(call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", "$players_kingdom"),
	(ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
	(assign, ":ruled_faction", "$players_kingdom"),
(try_end),
#Added section end
#In the following section, replace references to "fac_player_supporter_faction" with ":ruled_faction"
(call_script, "script_appoint_faction_marshall", ":ruled_faction", ":lord"),#dplmc+ changed
(store_current_hours, ":hours"),
(assign, "$g_player_faction_last_marshal_appointment", ":hours"),
#xxx TODO: Modify both fac_player_supporters_faction and players_kingdom in parallel
(try_begin),
	(faction_slot_eq, ":ruled_faction", slot_faction_political_issue, 1),#dplmc+ changed
	(faction_set_slot, ":ruled_faction", slot_faction_political_issue, 0),#dplmc+ changed
	(faction_set_slot, "fac_player_supporters_faction", slot_faction_political_issue, 0),#dplmc+ added

	(troop_set_slot, "trp_player",  slot_troop_stance_on_faction_issue, -1),
	#(try_for_range, ":active_npc", active_npcs_begin, active_npcs_end),#Changed this to support promoted kingdom ladies
	(try_for_range, ":active_npc", heroes_begin, heroes_end),
		(this_or_next|is_between, ":active_npc", active_npcs_begin, active_npcs_end),
			(troop_slot_eq, ":active_npc", slot_troop_occupation, slto_kingdom_hero),
	   (store_faction_of_troop, ":active_npc_faction", ":active_npc"),
	   (eq, ":active_npc_faction", ":ruled_faction"),#dplmc+ changed
	   (troop_set_slot, ":active_npc", slot_troop_stance_on_faction_issue, -1),
	(try_end),
(try_end),
##diplomacy end+
(assign, "$g_recalculate_ais", 1),
]],
[anyone|plyr, "minister_change_marshal_choose",
[],
"Never mind", "minister_pretalk",
[]],
[anyone, "minister_diplomatic_kingdoms",
[
##diplomacy start+
#Speed up, and also support non-traditional companions.
##OLD:
#(assign, ":companion_found", 0),
#(try_for_range, ":emissary", companions_begin, companions_end),
#(main_party_has_troop, ":emissary"),
#(assign, ":companion_found", 1),
#(try_end),
#(eq, ":companion_found", 1),
(assign, ":end_cond", heroes_end),
(try_for_range, ":emissary", heroes_begin, ":end_cond"),
	#gekokujo 3.0 microfactions! include fort companions start
	#(this_or_next|is_between, ":emissary", companions_begin, companions_end),
	(this_or_next|is_between, ":emissary", companions_begin, fort_companions_end),
	#gekokujo 3.0 microfactions! include fort companions end
		(troop_slot_eq, ":emissary", slot_troop_occupation, slto_player_companion),
	(main_party_has_troop, ":emissary"),
	(assign, ":end_cond", ":emissary"),
(try_end),
(lt, ":end_cond", heroes_end),
],
"To whom do you wish to send this emissary?", "minister_diplomatic_kingdoms_select",
[]],
[anyone, "minister_diplomatic_kingdoms",
[
],
"Unfortunately, there is no one to send right now.", "minister_pretalk",
[]],
[anyone, "minister_diplomatic_kingdoms",
[],
"To whom do you wish to send this emissary?", "minister_diplomatic_kingdoms_select",
[]],
[anyone|plyr|repeat_for_factions, "minister_diplomatic_kingdoms_select",
[
(store_repeat_object, ":faction_no"),
(is_between, ":faction_no", kingdoms_begin, kingdoms_end),
##diplomacy start+ Required if the player can be ruler or co-ruler of another faction
(neg|faction_slot_eq, ":faction_no", slot_faction_leader, "trp_player"),
(neq, ":faction_no", "$players_kingdom"),
##diplomacy end+
(neq, ":faction_no", "fac_player_supporters_faction"),
(faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
(faction_get_slot, ":leader_no", ":faction_no", slot_faction_leader),
(str_store_troop_name, s10, ":leader_no"),
(str_store_faction_name, s11, ":faction_no"),
(str_clear, s14),
#Has/has not recognized us a monarch
],
"{s10} of the {s11}{s14}", "minister_diplomatic_initiative_type",
[
(store_repeat_object, "$g_faction_selected"),
]],
[anyone|plyr, "minister_diplomatic_kingdoms_select",
[],
"Never mind", "minister_pretalk",
[]],
[anyone, "minister_diplomatic_initiative_type",
##diplomacy start+
#[],
[
(faction_get_slot, ":leader_no", "$g_faction_selected", slot_faction_leader),#Use reg0 for gender
(call_script, "script_dplmc_store_troop_is_female", ":leader_no"),
],#next line "him" to {reg0?her:him}
"What do you wish to tell {reg0?her:him}?", "minister_diplomatic_initiative_type_select",
[]],
[anyone|plyr, "minister_diplomatic_initiative_type_select",
[(store_relation, ":relation", "fac_player_supporters_faction", "$g_faction_selected"),
(lt, ":relation", 0),],
"That our two domains should enter into truce.", "minister_diplomatic_emissary",
[(assign, "$g_initiative_selected", npc_mission_peace_request)]],
[anyone|plyr, "minister_diplomatic_initiative_type_select",
##diplomacy start+
#[],
[
#Disable when the player is the ruler or co-ruler of an NPC kingdom.
#Setting up a separate dialog for this is something to do later, but
#not a high priority.
#TODO: Consider if there should be an alternative when the player is married to a pretender.
(neg|is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
(faction_get_slot, ":leader_no", "$g_faction_selected", slot_faction_leader),#Use reg0 for gender
(call_script, "script_dplmc_store_troop_is_female", ":leader_no"),
],#next line "his" to {reg0?her:his}
"That I wish to put myself under {reg0?her:his} protection, as {reg0?her:his} vassal.", "minister_diplomatic_emissary",
##diplomacy end+
[(assign, "$g_initiative_selected", npc_mission_pledge_vassal)]],
[anyone|plyr, "minister_diplomatic_initiative_type_select",
[(store_relation, ":relation", "fac_player_supporters_faction", "$g_faction_selected"),
(faction_slot_eq, "$g_faction_selected", slot_faction_recognized_player, 0),
(ge, ":relation", 0),],
"That I wish to express my goodwill, as one monarch to another.", "minister_diplomatic_emissary",
[(assign, "$g_initiative_selected", npc_mission_seek_recognition),]],
[anyone|plyr, "minister_diplomatic_initiative_type_select",
[(store_relation, ":relation", "fac_player_supporters_faction", "$g_faction_selected"),
(ge, ":relation", 0),##diplomacy start+],
#(neg|is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),#Disable when the player shares power
(faction_get_slot, ":leader_no", "$g_faction_selected", slot_faction_leader),#Use reg0 for gender
(call_script, "script_dplmc_store_troop_is_female", ":leader_no"),
],#next line "him" to {reg0?her:him}
"That I declare war upon {reg0?her:him}.", "minister_declare_war",
                     ##diplomacy end+
[]],
[anyone|plyr, "minister_diplomatic_initiative_type_select",[], "Never mind", "close_window",[]],
[anyone, "minister_declare_war",
[
   (assign, ":veto_troop", 0),
   (try_begin),
      (gt, "$players_kingdom", -1),
      (faction_get_slot, reg0, "$players_kingdom", slot_faction_leader),
      (gt, reg0, "trp_player"),
      (assign, ":veto_troop", reg0),
   (else_try),
      (is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
      (troop_get_slot, reg0, "trp_player", slot_troop_spouse),
	  (gt, reg0, 0),
      (assign, ":veto_troop", reg0),
   (try_end),
   (gt, ":veto_troop", 0),
   (str_store_troop_name, s0, ":veto_troop"),
], "For that you should first speak to {s0}.", "dplmc_minister_nevermind", []],
[anyone, "minister_declare_war",
[(try_begin),
   (call_script, "script_diplomacy_faction_get_diplomatic_status_with_faction", "fac_player_supporters_faction", "$g_faction_selected"),
(eq, reg0, 1),
(str_store_string, s12, "str_in_doing_so_you_will_be_in_violation_of_your_truce_is_that_what_you_want"),
(else_try),
   (call_script, "script_diplomacy_faction_get_diplomatic_status_with_faction", "fac_player_supporters_faction", "$g_faction_selected"),
(neq, reg0, -1),
(str_store_string, s12, "str_if_you_attack_without_provocation_some_of_your_vassals_may_consider_you_to_be_too_warlike_is_that_what_you_want"),
(else_try),
(str_store_string, s12, "str_our_men_are_ready_to_ride_forth_at_your_bidding_are_you_sure_this_is_what_you_want"),
(try_end),
], "{s12}", "minister_declare_war_confirm",
[]],
[anyone|plyr, "minister_declare_war_confirm",
[(str_store_faction_name, s12, "$g_faction_selected"),
],
"It is. I wish to make war on {s12}.", "minister_declare_war_confirm_yes",
[
(call_script, "script_diplomacy_start_war_between_kingdoms",  "fac_player_supporters_faction", "$g_faction_selected", 1),
]],
[anyone|plyr, "minister_declare_war_confirm",
[(str_store_faction_name, s12, "$g_faction_selected"),
],
"Hmm. Perhaps not.", "minister_pretalk",
[
]],
[anyone, "minister_declare_war_confirm_yes",
[(str_store_faction_name, s12, "$g_faction_selected"),
],
"As you command. We are now at war with the {s12}. May the heavens grant us victory.", "minister_pretalk",
[
]],
[anyone, "minister_diplomatic_emissary",
[], "Who shall be your emissary? You should choose one whom you trust, but who is also persuasive -- one who can negotiate without giving offense.", "minister_emissary_select",
[]],
[anyone|plyr|repeat_for_troops, "minister_emissary_select",[
(store_repeat_object, ":emissary"),
(main_party_has_troop, ":emissary"),
##diplomacy start+
##OLD:
#(is_between, ":emissary", companions_begin, companions_end),
#(troop_slot_eq, ":emissary", slot_troop_prisoner_of_party, -1),
#(is_between, ":emissary", active_npcs_begin, active_npcs_end),
##NEW:
# Support alternate possible companions
(is_between, ":emissary", heroes_begin, heroes_end),
(troop_slot_eq, ":emissary", slot_troop_prisoner_of_party, -1),
#gekokujo 3.0 microfactions! include fort companions start
#(this_or_next|is_between, ":emissary", companions_begin, companions_end),
(this_or_next|is_between, ":emissary", companions_begin, fort_companions_end),
#gekokujo 3.0 microfactions! include fort companions end
	(troop_slot_eq, ":emissary", slot_troop_occupation, slto_player_companion),
##diplomacy end+
(str_store_troop_name, s11, ":emissary"),
], "{s11}", "minister_emissary_dispatch",[
(store_repeat_object, "$g_emissary_selected"),
]],
[anyone|plyr, "minister_emissary_select",[
], "Actually, I can't think of anyone.", "minister_pretalk",[]],
[anyone, "minister_emissary_dispatch",
[
(str_store_troop_name, s11, "$g_emissary_selected"),
(str_store_faction_name, s12, "$g_faction_selected"),
(try_begin),
(eq, "$g_initiative_selected", npc_mission_seek_recognition),
(str_store_string, s14, "str_seek_recognition"),
(else_try),
(eq, "$g_initiative_selected", npc_mission_pledge_vassal),
(str_store_string, s14, "str_seek_vassalhood"),
(else_try),
(eq, "$g_initiative_selected", npc_mission_peace_request),
(str_store_string, s14, "str_seek_a_truce"),
##diplomacy begin
(else_try),
(eq, "$g_initiative_selected", dplmc_npc_mission_nonaggression_request),
(str_store_string, s14, "str_dplmc_conclude_non_agression"),
##diplomacy end
(try_end),
], "Very well -- I shall send {s11} to the {s12} to {s14}.", "minister_diplomatic_dispatch_confirm",[]],
[anyone|plyr, "minister_diplomatic_dispatch_confirm",[], "Yes, do that", "minister_pretalk",[
(troop_set_slot, "$g_emissary_selected", slot_troop_days_on_mission, 3),
(troop_set_slot, "$g_emissary_selected", slot_troop_current_mission, "$g_initiative_selected"),
(troop_set_slot, "$g_emissary_selected", slot_troop_mission_object, "$g_faction_selected"),
##diplomacy begin
(try_begin),
    (eq, "$g_initiative_selected", dplmc_npc_mission_gift_horses_request),
    (call_script, "script_dplmc_withdraw_from_treasury", "$diplomacy_var"),
(try_end),

(troop_set_slot, "$g_emissary_selected", dplmc_slot_troop_mission_diplomacy, "$diplomacy_var"),
(troop_set_slot, "$g_emissary_selected", dplmc_slot_troop_mission_diplomacy2, "$diplomacy_var2"),
##diplomacy end

(remove_member_from_party, "$g_emissary_selected", "p_main_party"),
]],
[anyone|plyr, "minister_diplomatic_dispatch_confirm",[], "Actually, hold off on that", "minister_pretalk",[]],
[anyone, "minister_replace",
[], "Very good. Whom will you appoint in my stead?", "minister_replace_select",
[]],
[anyone|plyr|repeat_for_troops, "minister_replace_select",
[
(store_repeat_object, ":troop_no"),
#gekokujo 3.0 microfactions! include fort companions start
#(is_between, ":troop_no", companions_begin, companions_end),
(is_between, ":troop_no", companions_begin, fort_companions_end),
#gekokujo 3.0 microfactions! include fort companions end
(main_party_has_troop, ":troop_no"),
(troop_slot_eq, ":troop_no", slot_troop_prisoner_of_party, -1),
##diplomacy start+
##OLD:
#(str_store_troop_name, s4, ":troop_no"),
##NEW:
(call_script, "script_dplmc_cap_troop_describes_troop_to_troop_s1", 1, "trp_player", ":troop_no", "$g_talk_troop"),
(str_store_string_reg, s4, s1),
##diplomacy end+
], "{s4}", "minister_replace_confirm",
[
(store_repeat_object, "$g_player_minister"),
]],
[anyone|plyr, "minister_replace_select",
[
(troop_get_slot, ":spouse", "trp_player", slot_troop_spouse),
(gt, ":spouse", 0),
##diplomacy start+
##OLD:
#(troop_get_type, ":is_female", ":spouse"),
#(neg|troop_slot_eq, ":spouse", slot_troop_occupation, slto_kingdom_hero),
#(eq, ":is_female", 1),
##NEW:
#Most of this logic has been moved to the next dialog.  Use this solely for handling
#spouses outside the normal hero range.
(neg|is_between, ":spouse", heroes_begin, heroes_end),
(troop_slot_eq, ":spouse", slot_troop_occupation, slto_kingdom_hero),
(neg|troop_slot_ge, ":spouse", slot_troop_occupation, slto_retirement),#not retired, in exile, or dead
(call_script, "script_dplmc_store_troop_is_female", ":spouse"),
##diplomacy end+

(str_store_troop_name, s4, ":spouse"),
(neq, ":spouse", "$g_talk_troop"),
##diplomacy start+
##OLD:
#], "My wife, {s4}.", "minister_replace_confirm", #husband disabled, as he's an active lord
##NEW:
], "My {reg0?wife:husband}, {s4}.", "minister_replace_confirm", #Gender assumptions like that aren't useful
##diplomacy end+
[
(troop_get_slot, "$g_player_minister", "trp_player", slot_troop_spouse),
]],
[anyone|plyr|repeat_for_troops, "minister_replace_select",
[
(store_repeat_object, ":troop_no"),
(is_between, ":troop_no", heroes_begin, heroes_end),#is a valid hero
(this_or_next|is_between, ":troop_no", kingdom_ladies_begin, kingdom_ladies_end),#is a kingdom lady
	(troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_lady),
(neg|troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),#Not a promoted kingdom lady
(neg|troop_slot_ge, ":troop_no", slot_troop_occupation, slto_retirement),#Not retired, dead, exiled, etc.
(neg|troop_slot_ge, ":troop_no", slot_troop_prisoner_of_party, 0),#Not a prisoner
#gekokujo 3.0 microfactions! include fort companions start
#(this_or_next|neg|is_between, ":troop_no", companions_begin, companions_end),#Don't double-list companions
(this_or_next|neg|is_between, ":troop_no", companions_begin, fort_companions_end),
#gekokujo 3.0 microfactions! include fort companions end
	(neg|main_party_has_troop, ":troop_no"),

(neq, ":troop_no", "$g_talk_troop"),

(call_script, "script_dplmc_troop_get_family_relation_to_troop", ":troop_no", "trp_player"),
(gt, reg0, 0),#Related
#(assign, ":relation_string_index", reg1),

(try_begin),
	(this_or_next|ge, reg0, 15),#Spouse, child, parent
	(this_or_next|eq, reg1, "str_dplmc_sister_wife"),
		(eq, reg1, "str_dplmc_co_husband"),
(else_try),
	#Otherwise, disallow if the troop has a (valid) guardian who is not the
	#player or themself
	(call_script, "script_get_kingdom_lady_social_determinants", ":troop_no"),
	(try_begin),
		(this_or_next|le, reg0, "trp_player"),#the player or a negative value
			(eq, reg0, ":troop_no"),
		(assign, reg0, 1),
	(else_try),
		(assign, reg0, 0),
	(try_end),
(try_end),
(ge, reg0, 0),
#(str_store_string, s11, ":relation_string_index"),
#(str_store_troop_name, s4, ":troop_no"),
(call_script, "script_dplmc_cap_troop_describes_troop_to_troop_s1", 1, "trp_player", ":troop_no", "$g_talk_troop"),
(str_store_string_reg, s4, s1),
], "{s4}.", "minister_replace_confirm", #husband disabled, as he's an active lord
[
(store_repeat_object, "$g_player_minister"),
]],
[anyone|plyr, "minister_replace_select",
[], "Actually, hold off on that.", "minister_pretalk",
[]],
[anyone, "minister_replace_confirm",
[
(troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_player_companion),
], "Very good. {s9} is your new minister. I shall make ready to rejoin you.", "close_window",
[
(str_store_troop_name, s9, "$g_player_minister"),
(party_add_members, "p_main_party", "$g_talk_troop", 1),
(assign, "$g_leave_encounter", 1),
(try_begin),
(main_party_has_troop, "$g_player_minister"),
(party_remove_members, "p_main_party", "$g_player_minister", 1),
(try_end),

(try_for_range, ":minister_quest", all_quests_begin, all_quests_end),
(quest_slot_eq, ":minister_quest", slot_quest_giver_troop, "$g_talk_troop"),
(call_script, "script_abort_quest", ":minister_quest", 0),
(try_end),
]],
[anyone, "minister_replace_confirm",
[
], "Very good. {s9} is your new minister. It has been an honor to serve you.", "close_window",
[
(str_store_troop_name, s9, "$g_player_minister"),
(try_begin),
(main_party_has_troop, "$g_player_minister"),
(party_remove_members, "p_main_party", "$g_player_minister", 1),
(try_end),
##diplomacy start+ Occupation cleanup
(try_begin),
	#Nothing needs to be done for non-heroes, or if the occupation is already kingdom hero or kingdom lady.
	(this_or_next|neg|is_between, "$g_talk_troop", heroes_begin, heroes_end),
	(this_or_next|troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_hero),
		(troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_lady),
(else_try),
	(is_between, "$g_talk_troop", kingdom_ladies_begin, kingdom_ladies_end),
	(neg|troop_slot_eq, "$g_talk_troop", slot_troop_playerparty_history, dplmc_pp_history_granted_fief),
	(neg|troop_slot_eq, "$g_talk_troop", slot_troop_playerparty_history, dplmc_pp_history_lord_rejoined),
	(troop_set_slot, "$g_talk_troop", slot_troop_occupation, slto_kingdom_lady),
(else_try),
	#This can't be reached right now, but if it is, make sure that the companion goes
	#back to the taverns instead of suddenly becoming a hero.
	#gekokujo 3.0 microfactions! include fort companions start (just in case)
	#(is_between, "$g_talk_troop", companions_begin, companions_end),
	(is_between, "$g_talk_troop", companions_begin, fort_companions_end),
	#gekokujo 3.0 microfactions! include fort companions end
	(neg|troop_slot_eq, "$g_talk_troop", slot_troop_playerparty_history, dplmc_pp_history_granted_fief),
	(neg|troop_slot_eq, "$g_talk_troop", slot_troop_playerparty_history, dplmc_pp_history_lord_rejoined),
	(neg|troop_slot_eq, "$g_talk_troop", slot_troop_playerparty_history, dplmc_pp_history_nonplayer_entry),
	(troop_set_slot, "$g_talk_troop", slot_troop_occupation, slto_inactive),
(else_try),
	(troop_set_slot, "$g_talk_troop", slot_troop_occupation, slto_kingdom_hero),
(else_try),

(try_end),
##diplomacy end+
]],
[anyone, "minister_grant_fief", [
    (faction_get_slot, ":fief_on_agenda", "$players_kingdom", slot_faction_political_issue),
    (str_clear, s12),
    (try_begin),
      (is_between, ":fief_on_agenda", centers_begin, centers_end),
      (str_store_party_name, s4, ":fief_on_agenda"),
      (str_store_string, s12, "str_minister_advice_select_fief"),
    (else_try),
      (eq, ":fief_on_agenda", 1),
      (str_store_string, s12, "str_minister_advice_select_fief_wait"),
    (try_end),
  ], "Which of your fiefs did you wish to grant?{s12} I would also like to remind you that if you wish to elevate one of your companions to a vassal with a fief, you should talk directly with them about it.", "minister_grant_fief_select", []],
[anyone|plyr|repeat_for_parties, "minister_grant_fief_select",
[
(store_repeat_object, ":center_no"),
(is_between, ":center_no", centers_begin, centers_end),
(store_faction_of_party, ":center_faction", ":center_no"),
(eq, ":center_faction", "fac_player_supporters_faction"),
##diplomacy begin
(neg|party_slot_eq, ":center_no", slot_village_infested_by_bandits, "trp_peasant_woman"),
##diplomacy end
(neq, ":center_no", "$g_player_court"),
(party_get_slot, ":town_lord", ":center_no", slot_town_lord),
(try_begin),
(ge, ":town_lord", active_npcs_begin),
(store_faction_of_troop, ":town_lord_faction", ":town_lord"),
(neq, ":town_lord_faction", "fac_player_supporters_faction"),
(assign, ":town_lord", -1),
(try_end),
(le, ":town_lord", 0),

(str_store_party_name, s1, ":center_no"),
(str_clear, s12),
(try_begin),
(party_slot_eq, ":center_no", slot_town_lord, -1),
(str_store_string, s12, "str_unassigned_center"),
(try_end),

],"{s1}{s12}", "minister_grant_fief_select_recipient",
[
(store_repeat_object, "$fief_selected"),
]],
[anyone|plyr, "minister_grant_fief_select",
[
],"Never mind", "minister_pretalk",
[]],
[anyone, "minister_grant_fief_select_recipient",
[
(str_clear, s12),
(try_begin),
(faction_slot_eq, "$players_kingdom", slot_faction_political_issue, "$fief_selected"),

##diplomacy start+ support promoted ladies
#(try_for_range, ":active_npc", active_npcs_begin, active_npcs_end),
(try_for_range, ":active_npc", heroes_begin, heroes_end),
##diplomacy end+
(troop_set_slot, ":active_npc", slot_troop_temp_slot, 0),
(try_end),

(assign, ":popular_favorite", -1),
(assign, ":votes_for_popular_favorite", 0),
##diplomacy start+
(troop_set_slot, "trp_player", slot_troop_temp_slot, 0),
#support promoted ladies
#(try_for_range, ":active_npc", active_npcs_begin, active_npcs_end),
(try_for_range, ":active_npc", heroes_begin, heroes_end),
    (this_or_next|is_between, ":active_npc", active_npcs_begin, active_npcs_end),
       (troop_slot_eq, ":active_npc", slot_troop_occupation, slto_kingdom_hero),
##dipolomacy end+
(store_faction_of_troop, ":active_npc_faction", ":active_npc"),
(eq, ":active_npc_faction", "fac_player_supporters_faction"),
(troop_get_slot, ":selected_npc", ":active_npc", slot_troop_stance_on_faction_issue),
(ge, ":selected_npc", 0),

(troop_get_slot, ":votes_accumulated", ":selected_npc", slot_troop_temp_slot),
(val_add, ":votes_accumulated", 1),
(troop_set_slot, ":selected_npc", slot_troop_temp_slot, ":votes_accumulated"),

(gt, ":votes_accumulated", ":votes_for_popular_favorite"),
(assign,  ":votes_for_popular_favorite", ":votes_accumulated"),
(assign, ":popular_favorite", ":selected_npc"),
(try_end),

##diplomacy start+ support promoted ladies
#(is_between, ":popular_favorite", active_npcs_begin, active_npcs_end),
(is_between, ":popular_favorite", heroes_begin, heroes_end),
##diplomacy end+
(str_store_troop_name, s4, ":popular_favorite"),
(assign, reg4, ":votes_for_popular_favorite"),

(str_store_string, s12, "str_minister_advice_fief_leading_vassal"),
(try_end),

],"And who will you choose to receive the fief?{s12}", "minister_grant_fief_select_recipient_choice",
[]],
[anyone|plyr|repeat_for_troops, "minister_grant_fief_select_recipient_choice",
[
(store_repeat_object, ":troop_no"),
(troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
##diplomacy start+ add support for promoted ladies
#(is_between, ":troop_no", active_npcs_begin, active_npcs_end),
(is_between, ":troop_no", heroes_begin, heroes_end),
##diplomacy end+
(store_faction_of_troop, ":troop_faction", ":troop_no"),
##diplomacy start+ add support for player is ruler/co-ruler of NPC kingdom
(is_between, ":troop_faction", kingdoms_begin, kingdoms_end),
(this_or_next|eq, ":troop_faction", "$players_kingdom"),
##diplomacy end+
(eq, ":troop_faction", "fac_player_supporters_faction"),
##diplomacy start+ show number of fiefs
#(str_store_troop_name, s1, ":troop_no"),
(str_store_troop_name, s11, ":troop_no"),
(call_script, "script_print_troop_owned_centers_in_numbers_to_s0", ":troop_no"),
(try_begin),
	(troop_slot_eq, "$g_talk_troop", slot_lord_recruitment_argument, argument_benefit),
	(str_store_string, s12, "str__promised_fief"),
(else_try),
	(str_clear, s12),
(try_end),
(try_begin),
	(eq, reg0, 0),
	(str_store_string, s0, "str_no_fiefss12"),
(else_try),
	(str_store_string, s0, "str_fiefs_s0s12"),
(try_end),
#add relation string
(str_store_string_reg, s12, s63),#save s63, clobbering s12 (perhaps already overwritten)
(call_script, "script_troop_get_player_relation", ":troop_no"),
(call_script, "script_describe_relation_to_s63", reg0),
(str_store_string_reg, s1, s63),#clobber s1
(str_store_string_reg, s63, s12),#revert s63
(str_store_string, s1, "str_dplmc_s0_comma_s1"),#write to s1

#(try_end),
##diplomacy end+

],"{!}{s11} {s1}.", "minister_grant_fief_complete",
[
(store_repeat_object, "$lord_selected"),
]],
[anyone|plyr, "minister_grant_fief_select_recipient_choice",
[
],"Never mind", "minister_pretalk",
[]],
[anyone, "minister_grant_fief_complete",
[
],"Very well - {s2} shall receive {s1}.", "minister_pretalk",
[
(call_script, "script_give_center_to_lord", "$fief_selected", "$lord_selected", 0),
(str_store_party_name, s1, "$fief_selected"),
(str_store_troop_name, s2, "$lord_selected"),

(try_begin),
(faction_slot_eq, "$players_kingdom", slot_faction_political_issue, "$fief_selected"),
(faction_set_slot, "$players_kingdom", slot_faction_political_issue, -1),
(try_end),

(call_script, "script_add_log_entry", logent_castle_given_to_lord_by_player, "trp_player", "$fief_selected", "$lord_selected", "$g_encountered_party_faction"),
]],
[anyone, "minister_indict",
[], "Grim news, my {lord/lady}. Who do you believe is planning to betray you?", "minister_indict_select",
[]],
[anyone|plyr|repeat_for_troops, "minister_indict_select",
[
(store_repeat_object, ":troop_no"),
(troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
(store_faction_of_troop, ":faction", ":troop_no"),
##diplomacy start+
(troop_is_hero, ":troop_no"),
(neq, ":troop_no", "trp_player"),
#Prevent problems when the player is co-ruler of a kingdom.
(neg|faction_slot_eq, "fac_player_supporters_faction", slot_faction_leader, ":troop_no"),
(neg|faction_slot_eq, "$players_kingdom", slot_faction_leader, ":troop_no"),
##diplomacy end+
(eq, ":faction", "fac_player_supporters_faction"),
(str_store_troop_name, s11, ":troop_no"),
], "{s11}", "minister_indict_confirm",
[
(store_repeat_object, "$lord_selected"),
]],
[anyone|plyr, "minister_indict_select",
[], "Never mind.", "minister_pretalk",
[]],
[anyone, "minister_indict_confirm",
[
(str_store_troop_name, s4, "$lord_selected"),
##diplomacy start+
##OLD:
#(troop_get_type, reg4, "$lord_selected"),
##NEW:
(assign, reg4, 0),
(try_begin),
	(call_script, "script_cf_dplmc_troop_is_female", "$lord_selected"),
	(assign, reg4, 1),
(try_end),
##diplomacy end+
], "Think carefully on this, my {lord/lady}. If you indict {s4} for treason unjustly, you may find that others become nervous about serving you. On the other hand, if you truly believe that {reg4?she:he} is about to betray you, then perhaps it is best to move first, to secure control of {reg4?her:his} fortresses.", "minister_indict_confirm_answer",
[]],
[anyone|plyr, "minister_indict_confirm_answer",[], "I have thought long enough. Issue the indictment!", "minister_indict_conclude",[]],
[anyone|plyr, "minister_indict_confirm_answer",[], "Perhaps I should wait a little while longer..", "minister_pretalk",[]],
[anyone, "minister_indict_conclude",
[], "It has been sent, my {lord/lady}.", "minister_pretalk",
[
(call_script, "script_indict_lord_for_treason", "$lord_selected", "fac_player_supporters_faction"),
]],
[anyone|plyr|repeat_for_troops, "center_captured_lord_advice",
[
(store_repeat_object, ":troop_no"),
(troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
(neq, "$g_talk_troop", ":troop_no"),
(neq, "trp_player", ":troop_no"),
(store_troop_faction, ":faction_no", ":troop_no"),
##diplomacy start+ Handle player is co-ruler of kingdom
(call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", ":faction_no"),
(this_or_next|ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
##diplomacy end+
(eq, ":faction_no", "fac_player_supporters_faction"),
(str_store_troop_name, s11, ":troop_no"),
(call_script, "script_print_troop_owned_centers_in_numbers_to_s0", ":troop_no"),

(try_begin),
##diplomacy start+ fixed bug that was preventing "promised fief" from appearing
(troop_slot_eq, ":troop_no", slot_lord_recruitment_argument, argument_benefit),#changed "$g_talk_troop" to ":troop_no"
##diplomacy end+
(str_store_string, s12, "str__promised_fief"),
(else_try),
(str_clear, s12),
(try_end),

(try_begin),
 (eq, reg0, 0),
 ##diplomacy start+ write to s0 instead of s1
 (str_store_string, s0, "str_no_fiefss12"),
 ##diplomacy end_
(else_try),
 ##diplomacy start+ write to s0 instead of s1
 (str_store_string, s0, "str_fiefs_s0s12"),
 ##diplomacy end+
(try_end),
##diplomacy start+ add relation to list of lords
#add relation string
(str_store_string_reg, s12, s63),#save s63, clobbering s12 (perhaps overwritten earlier)
(call_script, "script_troop_get_player_relation", ":troop_no"),
(call_script, "script_describe_relation_to_s63", reg0),
(str_store_string_reg, s1, s63),#clobber s1
(str_store_string_reg, s63, s12),#revert s63
(str_store_string, s1, "str_dplmc_s0_comma_s1"),#write to s1
##diplomacy end+
],
"{s11}. {s1}", "center_captured_lord_advice_2",
[
(store_repeat_object, "$temp"),
]],
[anyone|plyr, "center_captured_lord_advice",
[
(call_script, "script_print_troop_owned_centers_in_numbers_to_s0", "trp_player"),
(str_store_party_name, s1, "$g_center_taken_by_player_faction"),

(try_begin),
(is_between, "$g_talk_troop", pretenders_begin, pretenders_end),
(str_store_string, s12, "str_please_s65_"),
(else_try),
(str_clear, s12),
(try_end),
],
"{s12}I want to have {s1} for myself. (fiefs: {s0})", "center_captured_lord_advice_2",
[
(assign, "$temp", "trp_player"),
]],
[anyone|plyr, "center_captured_lord_advice",
[
(call_script, "script_print_troop_owned_centers_in_numbers_to_s0", "$g_talk_troop"),
(str_store_party_name, s1, "$g_center_taken_by_player_faction"),
(is_between, "$g_talk_troop", pretenders_begin, pretenders_end),
],
"{s66}, you should have {s1} for yourself. (fiefs: {s0})", "center_captured_lord_advice_2",
[
(assign, "$temp", "$g_talk_troop"),
]],
[anyone, "center_captured_lord_advice_2",
[
(eq, "$g_talk_troop", "$g_player_minister"),
],
"As you wish, my {lord/lady}. {reg6?I:{reg7?You:{s11}}} will be the new {reg3?lady:lord} of {s1}.", "minister_issues",
[
(assign, ":new_owner", "$temp"),

(call_script, "script_give_center_to_lord", "$g_center_taken_by_player_faction", ":new_owner", 0),

(try_begin),
(faction_slot_eq, "$players_kingdom", slot_faction_political_issue, "$g_center_taken_by_player_faction"),
(faction_set_slot, "$players_kingdom", slot_faction_political_issue, -1),
(try_end),

(try_begin),
 (neq, ":new_owner", "trp_player"),
 (try_for_range, ":unused", 0, 4),
   (call_script, "script_cf_reinforce_party", "$g_center_taken_by_player_faction"),
 (try_end),
(try_end),

(assign, reg6, 0),
(assign, reg7, 0),
(try_begin),
 (eq, ":new_owner", "$g_talk_troop"),
 (assign, reg6, 1),
(else_try),
 (eq, ":new_owner", "trp_player"),
 (assign, reg7, 1),
(else_try),
 (str_store_troop_name, s11, ":new_owner"),
(try_end),
(str_store_party_name, s1, "$g_center_taken_by_player_faction"),
##diplomacy start+
##OLD:
#(troop_get_type, reg3, ":new_owner"),
##NEW:
(assign, reg3, 0),
(try_begin),
	(call_script, "script_cf_dplmc_troop_is_female", ":new_owner"),
	(assign, reg3, 1),
(try_end),
##diplomacy end+
(assign, "$g_center_taken_by_player_faction", -1),
]],
[anyone, "center_captured_lord_advice_2",
[
],
"Hmmm. All right, {playername}. I value your counsel highly. {reg6?I:{reg7?You:{s11}}} will be the new {reg3?lady:lord} of {s1}.", "close_window",
[
(assign, ":new_owner", "$temp"),

(troop_set_slot, ":new_owner", slot_lord_recruitment_argument, 0),

(call_script, "script_give_center_to_lord", "$g_center_taken_by_player_faction", ":new_owner", 0),
(try_begin),
(faction_slot_eq, "$players_kingdom", slot_faction_political_issue, "$g_center_taken_by_player_faction"),
(faction_set_slot, "$players_kingdom", slot_faction_political_issue, -1),
(try_end),

(try_begin),
 (neq, ":new_owner", "trp_player"),
 (try_for_range, ":unused", 0, 4),
   (call_script, "script_cf_reinforce_party", "$g_center_taken_by_player_faction"),
 (try_end),
(try_end),

(assign, reg6, 0),
(assign, reg7, 0),
(try_begin),
 (eq, ":new_owner", "$g_talk_troop"),
 (assign, reg6, 1),
(else_try),
 (eq, ":new_owner", "trp_player"),
 (assign, reg7, 1),
(else_try),
 (str_store_troop_name, s11, ":new_owner"),
(try_end),
(str_store_party_name, s1, "$g_center_taken_by_player_faction"),
##diplomacy start+
##OLD:
#(troop_get_type, reg3, ":new_owner"),
##NEW:
(assign, reg3, 0),
(try_begin),
	(call_script, "script_cf_dplmc_troop_is_female", ":new_owner"),
	(assign, reg3, 1),
(try_end),
##diplomacy end+
(assign, "$g_center_taken_by_player_faction", -1),
]],
[anyone, "event_triggered", [
               (eq, "$g_infinite_camping", 0),
               (store_conversation_troop, "$map_talk_troop"),
          (is_between, "$map_talk_troop", companions_begin, companions_end),
               (eq, "$map_talk_troop", "$npc_is_quitting"),
               (troop_get_slot, ":honorific", "$map_talk_troop", slot_troop_honorific),
               (str_store_string, 5, ":honorific")],
"Excuse me {s5} -- there is something I need to tell you.", "companion_quitting", [
              (assign, "$npc_is_quitting", 0),
              (assign, "$player_can_persuade_npc", 1),
              (assign, "$player_can_refuse_npc_quitting", 1),
 ]],
[anyone, "event_triggered", [
               (store_conversation_troop, "$map_talk_troop"),
          (is_between, "$map_talk_troop", companions_begin, companions_end),

               (eq, "$map_talk_troop", "$npc_with_grievance"),
               (eq, "$npc_map_talk_context", slot_troop_morality_state),


               (try_begin),
                   (eq, "$npc_grievance_slot", slot_troop_morality_state),
                   (troop_get_slot, ":speech", "$map_talk_troop", slot_troop_morality_speech),
               (else_try),
                   (troop_get_slot, ":speech", "$map_talk_troop", slot_troop_2ary_morality_speech),
               (try_end),
               (str_store_string, 21, "$npc_grievance_string"),
               (str_store_string, 5, ":speech"),
               ],
"{s5}", "companion_objection_response", [
              (assign, "$npc_with_grievance", 0),
 ]],
[anyone, "event_triggered", [
               (store_conversation_troop, "$map_talk_troop"),
          (is_between, "$map_talk_troop", companions_begin, companions_end),

               (eq, "$map_talk_troop", "$npc_with_personality_clash_2"),
               (eq, "$npc_map_talk_context", slot_troop_personalityclash2_state),

               (troop_get_slot, ":speech", "$map_talk_troop", slot_troop_personalityclash2_speech),
               (troop_get_slot, ":object", "$map_talk_troop", slot_troop_personalityclash2_object),
               (str_store_troop_name, 11, ":object"),
               (str_store_string, 5, ":speech"),
               ],
"{s5}", "companion_personalityclash2_b", [
              (assign, "$npc_with_personality_clash_2", 0),
              (troop_get_slot, ":grievance", "$map_talk_troop", slot_troop_personalityclash_penalties),
              (val_add, ":grievance", 5),
              (troop_set_slot, "$map_talk_troop", slot_troop_personalityclash_penalties, ":grievance"),

              (troop_get_slot, ":object", "$map_talk_troop", slot_troop_personalityclash2_object),
         (call_script, "script_troop_change_relation_with_troop", "$map_talk_troop", ":object", -15),
 ]],
[anyone, "event_triggered", [
               (store_conversation_troop, "$map_talk_troop"),
          (is_between, "$map_talk_troop", companions_begin, companions_end),

               (eq, "$map_talk_troop", "$npc_with_personality_clash"),
               (eq, "$npc_map_talk_context", slot_troop_personalityclash_state),

               (troop_get_slot, ":speech", "$map_talk_troop", slot_troop_personalityclash_speech),
               (troop_get_slot, ":object", "$map_talk_troop", slot_troop_personalityclash_object),
               (str_store_troop_name, 11, ":object"),
               (str_store_string, 5, ":speech"),
               ],
"{s5}", "companion_personalityclash_b", [
              (assign, "$npc_with_personality_clash", 0),
              (troop_get_slot, ":grievance", "$map_talk_troop", slot_troop_personalityclash_penalties),
              (val_add, ":grievance", 5),
              (troop_set_slot, "$map_talk_troop", slot_troop_personalityclash_penalties, ":grievance"),

              (troop_get_slot, ":object", "$map_talk_troop", slot_troop_personalityclash_object),
         (call_script, "script_troop_change_relation_with_troop", "$map_talk_troop", ":object", -15),

 ]],
[anyone, "event_triggered", [
               (eq, "$npc_map_talk_context", slot_troop_personalitymatch_state),
               (store_conversation_troop, "$map_talk_troop"),
          (is_between, "$map_talk_troop", companions_begin, companions_end),

               (eq, "$map_talk_troop", "$npc_with_personality_match"),

               (troop_get_slot, ":speech", "$map_talk_troop", slot_troop_personalitymatch_speech),
               (troop_get_slot, ":object", "$map_talk_troop", slot_troop_personalitymatch_object),
               (str_store_troop_name, 11, ":object"),
               (str_store_string, 5, ":speech"),

               ],
"{s5}", "companion_personalitymatch_b", [
              (assign, "$npc_with_personality_match", 0),
              (troop_get_slot, ":object", "$map_talk_troop", slot_troop_personalitymatch_object),
         (call_script, "script_troop_change_relation_with_troop", "$map_talk_troop", ":object", 15),

 ]],
[anyone, "event_triggered", [
               (eq, "$npc_map_talk_context", slot_troop_woman_to_woman_string),
               (store_conversation_troop, "$map_talk_troop"),
          (is_between, "$map_talk_troop", companions_begin, companions_end),

             (store_sub, ":npc_no", "$map_talk_troop", "trp_npc1"),
             (store_add, ":speech", "str_npc1_woman_to_woman", ":npc_no"),
#                     (troop_get_slot, ":speech", "$map_talk_troop", slot_troop_woman_to_woman_string),
               (str_store_string, s5, ":speech"),
               ],
"{s5}", "companion_sisterly_advice", [
              (troop_set_slot, "$map_talk_troop", slot_troop_woman_to_woman_string, -1),
         (assign, "$npc_with_sisterly_advice", 0),
 ]],
[anyone, "event_triggered", [
               (eq, "$g_infinite_camping", 0),
               (eq, "$npc_map_talk_context", slot_troop_home),
               (store_conversation_troop, "$map_talk_troop"),
          (is_between, "$map_talk_troop", companions_begin, companions_end),

               (troop_get_slot, ":speech", "$map_talk_troop", slot_troop_home_intro),
               (str_store_string, s5, ":speech"),
               ],
"{s5}", "companion_home_description", [
              (troop_set_slot, "$map_talk_troop", slot_troop_home_speech_delivered, 1),
 ]],
[anyone,"event_triggered", [
(eq, "$talk_context", tc_rebel_thanks),
(store_conversation_troop, "$g_talk_troop"),
(is_between, "$g_talk_troop", pretenders_begin, pretenders_end),

(troop_get_slot, ":old_faction", "$g_talk_troop", slot_troop_original_faction),
(str_store_faction_name, s3, ":old_faction"),
(str_store_string, s6, "@{playername}, when we started our long walk, few people had the courage to support me.\
And fewer still would be willing to put their lives at risk for my cause.\
But you didn't hesitate for a moment in throwing yourself at my enemies.\
We have gone through a lot together, and there were times I came close to losing all hope.\
But with God's help, we prevailed. It is now time for me to leave your company and take what's rightfully mine.\
From now on, I will carry out the great responsibility of ruling {s3}.\
There still lie many challanges ahead and I count on your help in overcoming those.\
And of course, you will always remain as my foremost vassal."),
],
"{s6}", "rebel_thanks_answer",
[

(unlock_achievement, ACHIEVEMENT_KINGMAKER),
(call_script, "script_end_quest", "qst_rebel_against_kingdom"),

     (try_begin),
       (troop_get_type, ":is_female", "trp_player"),
       (eq, ":is_female", 1),

       (troop_get_type, ":is_female", "$g_talk_troop"),
       (eq, ":is_female", 1),

       (unlock_achievement, ACHIEVEMENT_GIRL_POWER),
     (try_end),
 ]],
[anyone|plyr,"rebel_thanks_answer", [], "It was an honour to fight for your cause, {reg65?madame:my lord}.", "rebel_thanks_answer_2", []],
[anyone|plyr,"rebel_thanks_answer", [], "You will always have my loyal support, {reg65?my lady:sir}.", "rebel_thanks_answer_2", []],
[anyone,"rebel_thanks_answer_2", [], "I will miss living this life of adventure with you, but my duties await me. So... farewell for now, {playername}.\
I hope I'll see you again soon.", "close_window", []],
[anyone, "event_triggered", [
               (store_conversation_troop, "$map_talk_troop"),
          (is_between, "$map_talk_troop", companions_begin, companions_end),

               (eq, "$map_talk_troop", "$npc_with_political_grievance"),
               (eq, "$npc_map_talk_context", slot_troop_kingsupport_objection_state),

          (store_sub, ":npc_no", "$g_talk_troop", "trp_npc1"),
          (store_add, ":string", "str_npc1_kingsupport_objection", ":npc_no"),
#					 (troop_get_slot, ":string", "$map_talk_troop", slot_troop_kingsupport_objection_string),
               (str_store_string, 21, ":string"),
               ],
"{s21}", "companion_political_grievance_response", [
              (assign, "$npc_with_political_grievance", 0),
         (troop_set_slot, "$map_talk_troop", slot_troop_kingsupport_objection_state, 2),

 ]],
[anyone, "event_triggered", [
               (store_conversation_troop, "$map_talk_troop"),
		  #gekokujo 3.0 microfactions! include fort companions start
          #(is_between, "$map_talk_troop", companions_begin, companions_end),
          (is_between, "$map_talk_troop", companions_begin, fort_companions_end),
		  #gekokujo 3.0 microfactions! include fort companions end

               (eq, "$map_talk_troop", "$npc_to_rejoin_party"),
          (neg|main_party_has_troop, "$map_talk_troop"),

               (troop_slot_eq, "$map_talk_troop", slot_troop_current_mission, npc_mission_rejoin_when_possible),
          (troop_slot_eq, "$map_talk_troop", slot_troop_occupation, slto_player_companion),
          (troop_get_slot, ":string", "$map_talk_troop", slot_troop_honorific),
               (str_store_string, 21, ":string"),
          ],
"Greetings, {s21}. Are you ready for me to rejoin you?"	,
          "companion_rejoin_response",
         [
              (assign, "$npc_to_rejoin_party", 0),
         ]],
[anyone, "event_triggered", [
               (store_conversation_troop, "$map_talk_troop"),
          (is_between, "$map_talk_troop", companions_begin, companions_end),

               (eq, "$map_talk_troop", "$npc_to_rejoin_party"),
#                     (eq, "$npc_map_talk_context", slot_troop_days_on_mission),
               (troop_slot_eq, "$g_talk_troop", slot_troop_current_mission, npc_mission_kingsupport),

          (troop_get_slot, ":string", "$map_talk_troop", slot_troop_honorific),
               (str_store_string, 21, ":string"),
               ],
"Well, {s21}, at last I've found you. I've been out spreading the word about your claim, and am now ready to rejoin the company.", "companion_rejoin_response", [
              (assign, "$npc_to_rejoin_party", 0),
         (call_script, "script_change_player_right_to_rule", 3),
         (troop_set_slot, "$g_talk_troop", slot_troop_kingsupport_state, 1),

         (try_begin),
            (is_between, "$player_right_to_rule", 10, 15),
            (call_script, "script_add_log_entry", logent_player_claims_throne_1, "trp_player", 0, 0, 0),
         (else_try),
            (is_between, "$player_right_to_rule", 20, 25),
            (call_script, "script_add_log_entry", logent_player_claims_throne_2, "trp_player", 0, 0, 0),
         (try_end),
         ]],
[anyone, "event_triggered", [
 (store_conversation_troop, "$map_talk_troop"),
#gekokujo 3.0 microfactions! include fort companions start
#(is_between, "$map_talk_troop", companions_begin, companions_end),
(is_between, "$map_talk_troop", companions_begin, fort_companions_end),
#gekokujo 3.0 microfactions! include fort companions end
 (eq, "$map_talk_troop", "$npc_to_rejoin_party"),
#                     (eq, "$npc_map_talk_context", slot_troop_days_on_mission),
 (troop_slot_eq, "$map_talk_troop", slot_troop_current_mission, npc_mission_gather_intel),

(troop_get_slot, ":string", "$map_talk_troop", slot_troop_honorific),
 (str_store_string, 21, ":string"),

(troop_get_slot, ":town_with_contacts", "$map_talk_troop", slot_troop_town_with_contacts),
(store_faction_of_party, ":town_faction", ":town_with_contacts"),

(call_script, "script_update_faction_political_notes", ":town_faction"),
(assign, ":instability_index", reg0),
(val_add, ":instability_index", reg0),
(val_add, ":instability_index", reg1),


(str_store_faction_name, s12, ":town_faction"),
(try_begin),
   (ge, ":instability_index", 60),
   (str_store_string, s11, "str_the_s12_is_a_labyrinth_of_rivalries_and_grudges_lords_ignore_their_lieges_summons_and_many_are_ripe_to_defect"),
(else_try),
   (ge, ":instability_index", 40),
   (str_store_string, s11, "str_the_s12_is_shaky_many_lords_do_not_cooperate_with_each_other_and_some_might_be_tempted_to_defect_to_a_liege_that_they_consider_more_worthy"),
(else_try),
   (ge, ":instability_index", 20),
   (str_store_string, s11, "str_the_s12_is_fairly_solid_some_lords_bear_enmities_for_each_other_but_they_tend_to_stand_together_against_outside_enemies"),
(else_try),
   (str_store_string, s11, "str_the_s12_is_a_rock_of_stability_politically_speaking_whatever_the_lords_may_think_of_each_other_they_fight_as_one_against_the_common_foe"),
(try_end),

(try_for_range, ":lord", active_npcs_begin, active_npcs_end),
   (troop_slot_eq, ":lord", slot_troop_occupation, slto_kingdom_hero),
   (store_faction_of_troop, ":lord_faction", ":lord"),
   (eq, ":lord_faction", ":town_faction"),
   (call_script, "script_update_troop_political_notes", ":lord"),
(try_end),

 ],
"Well, {s21}, at last I've found you. {s11}. The rest of my report I submit to you in writing.", "companion_rejoin_response", [
]],
[anyone, "event_triggered", [
               (store_conversation_troop, "$map_talk_troop"),
		  #gekokujo 3.0 microfactions! include fort companions start
          #(is_between, "$map_talk_troop", companions_begin, companions_end),
          (is_between, "$map_talk_troop", companions_begin, fort_companions_end),
		  #gekokujo 3.0 microfactions! include fort companions end

               (eq, "$map_talk_troop", "$npc_to_rejoin_party"),
#                     (eq, "$npc_map_talk_context", slot_troop_days_on_mission),
               (troop_get_slot, ":mission", "$g_talk_troop", slot_troop_current_mission),
          (this_or_next|eq, ":mission", npc_mission_peace_request),
          (this_or_next|eq, ":mission", npc_mission_pledge_vassal),
          (this_or_next|eq, ":mission", npc_mission_test_waters),
          (this_or_next|eq, ":mission", npc_mission_non_aggression),
            (eq, ":mission", npc_mission_seek_recognition),

          (troop_get_slot, ":string", "$map_talk_troop", slot_troop_honorific),
               (str_store_string, 21, ":string"),
          (troop_get_slot, ":mission_object", "$g_talk_troop", slot_troop_mission_object),
          (str_store_faction_name, s31, ":mission_object"),

          (call_script, "script_npc_decision_checklist_peace_or_war", ":mission_object", "fac_player_supporters_faction", "$g_talk_troop"),
          (assign, "$g_mission_result", reg0),
##diplomacy start+
		(try_begin),
			(ge, "$cheat_mode", 1),
			(display_message, "@{!} DEBUG - Native checklist-peace-or-war result {reg0}, because {s14}"),
		(try_end),
		#make gender correct
		(faction_get_slot, ":emissary_object", ":mission_object", slot_faction_leader),
		(call_script, "script_dplmc_store_troop_is_female", ":emissary_object"),
               ],#next line "him" to {reg0?her:him}
#diplomacy begin
"Well, {s21}, at last I've found you. I have returned from my mission to {s31}. In general, I would say, {s14}. Nevertheless I tried to convince {reg0?her:him}.","companion_embassy_results", [
#diplomacy end
         ]],
[anyone|plyr, "vassalage_offer_confirm", [],
##diplomacy start+ next line "him" to {reg0?her:him}
"Tell {reg0?her:him} that I accept {reg0?her:his} terms...", "companion_rejoin_response", [
##diplomacy end+

(troop_get_slot, "$g_invite_faction", "$g_talk_troop", slot_troop_mission_object),
(faction_get_slot, "$g_invite_faction_lord", "$g_invite_faction", slot_faction_leader),

(str_store_troop_name,s1,"$g_invite_faction_lord"),
  (setup_quest_text,"qst_join_faction"),

  (str_store_troop_name_link, s3, "$g_invite_faction_lord"),
  (str_store_faction_name_link, s4, "$g_invite_faction"),
  (quest_set_slot, "qst_join_faction", slot_quest_giver_troop, "$g_invite_faction_lord"),
  ##diplomacy start
  (quest_set_slot, "qst_join_faction", slot_quest_expiration_days, 20),
  ##diplomacy end

(try_begin),
   (store_relation, ":relation", "$g_invite_faction", "fac_player_supporters_faction"),
   (lt, ":relation", 0),
   (call_script, "script_diplomacy_start_peace_between_kingdoms", "$g_invite_faction", "fac_player_supporters_faction", 0),
   (quest_set_slot, "qst_join_faction", slot_quest_failure_consequence, 1),
(try_end),

  (str_store_string, s2, "@Find and speak with {s3} of {s4} to give him your oath of loyalty."),
  (call_script, "script_start_quest", "qst_join_faction", "$g_invite_faction_lord"),
  (call_script, "script_report_quest_troop_positions", "qst_join_faction", "$g_invite_faction_lord", 3),
]],
[anyone, "event_triggered", [
#gekokujo 3.0 microfactions! include fort companions start
#(is_between, "$g_talk_troop", companions_begin, companions_end),
(is_between, "$g_talk_troop", companions_begin, fort_companions_end),
#gekokujo 3.0 microfactions! include fort companions end
(neg|troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_hero),
(neg|main_party_has_troop, "$g_talk_troop"),
               ],
"Would you have me rejoin you?", "companion_rejoin_response", [
(assign, "$map_talk_troop", "$g_talk_troop"),
 ]],
[anyone, "event_triggered",
[(eq, "$caravan_escort_state",1),
(eq, "$g_encountered_party","$caravan_escort_party_id"),
(le, "$talk_context",tc_party_encounter),
(store_distance_to_party_from_party, reg0, "$caravan_escort_destination_town", "$caravan_escort_party_id"),
(lt, reg0, 5),
(str_store_party_name, s3, "$caravan_escort_destination_town"),
(assign, reg3, "$caravan_escort_agreed_reward"),
],
"There! I can see the walls of {s3} in the distance. We've made it safely.\
Here, take this purse of {reg3} mon, as I promised. I hope we can travel together again someday.", "close_window",
[
(assign,"$caravan_escort_state",0),
(call_script, "script_troop_add_gold", "trp_player", "$caravan_escort_agreed_reward"),
(assign,reg(4), "$caravan_escort_agreed_reward"),
(val_mul,reg(4), 1),
(add_xp_as_reward,reg(4)),
(assign, "$g_leave_encounter",1),
]],
[anyone, "event_triggered", 
  [
    (eq, "$npc_map_talk_context", tc_gekokujo_encounter),
    (store_conversation_troop, "$encounter_talk_troop"),
    (eq, "$encounter_talk_troop", "$gekokujo_encounter_boss"),
    
    (store_random_in_range, ":offset", 0, 20),
    (val_add, ":offset", "str_gekokujo_encounter_dialogue_1"),
    (str_store_string, s5, ":offset"),
    
    #let's hope this works
    (store_random_in_range, "$gekokujo_encounter_reply_1", 0, 10),
    (val_add, "$gekokujo_encounter_reply_1", "str_gekokujo_encounter_choice_1"),
    
    (store_random_in_range, "$gekokujo_encounter_reply_2", 0, 9),
    (try_begin),
      (eq, "$gekokujo_encounter_reply_1", "$gekokujo_encounter_reply_2"),
      (val_add, "$gekokujo_encounter_reply_2", 1),
    (try_end),
    (val_add, "$gekokujo_encounter_reply_2", "str_gekokujo_encounter_choice_1"),
  ],
  "{s5}", 
  "gekokujo_encounter_reply_1", []],
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
[anyone, "event_triggered", [
               ],
"{!}Sorry -- just talking to myself [ERROR- {s51}]", "close_window", [
 ]],
[anyone|plyr, "female_pc_marriage_vow", [
],
#diplomacy start+ (female player/male lord) or (male player/female lord)
"I vow to take you as my {reg65?wife:husband}.", "lord_groom_wedding_complete", [
#diplomacy end+
(call_script, "script_courtship_event_bride_marry_groom", "trp_player", "$g_talk_troop", 0),
(call_script, "script_end_quest", "qst_wed_betrothed_female"),
]],
[anyone|plyr, "female_pc_marriage_vow", [
],
"Wait -- I need to think about this.", "close_window", [
(assign, "$g_leave_encounter", 1),
]],
[anyone|plyr,"freed_lord_answer", [(lt, "$g_talk_troop_faction_relation", 0)],
"You're not going anywhere, 'friend'. You're my prisoner now.", "freed_lord_answer_1",
[#(troop_set_slot, "$g_talk_troop", slot_troop_is_prisoner, 1),
(troop_set_slot, "$g_talk_troop", slot_troop_prisoner_of_party, "p_main_party"),
(party_force_add_prisoners, "p_main_party", "$g_talk_troop", 1),
(call_script, "script_change_player_relation_with_troop", "$g_talk_troop", -30),
(call_script, "script_change_player_relation_with_faction_ex", "$g_talk_troop_faction", -2),
(call_script, "script_event_hero_taken_prisoner_by_player", "$g_talk_troop"),
]],
[anyone,"freed_lord_answer_1", [],
##diplomacy start+ make insult switch by gender
"I'll have your head on a pike for this, you {bastard/bitch}! Someday!", "close_window", []],
[anyone|plyr,"freed_lord_answer", [
],
"You are free to go wherever you want, sir.", "freed_lord_answer_2",
[(call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 7),
(call_script, "script_change_player_honor", 2),
#    (troop_get_slot, ":cur_rank", "$g_talk_troop", slot_troop_kingdom_rank),
#    (val_mul, ":cur_rank", 1),
##diplomacy start+
#Relationship boost for freeing lords.
(call_script, "script_dplmc_is_affiliated_family_member", "$g_talk_troop"),
(assign, ":talk_troop_is_affiliate", reg0),
(try_for_range, ":npc", heroes_begin, heroes_end),
	(store_troop_faction, ":npc_faction", ":npc"),
	(store_relation, reg0, ":npc_faction", "$g_talk_troop_faction"),
	(this_or_next|eq, ":npc_faction", "$g_talk_troop_faction"),
		(ge, reg0, 0),
	(neq, ":npc", "$g_talk_troop"),
	(neg|troop_slot_eq, ":npc", slot_troop_occupation, dplmc_slto_dead),
	(call_script, "script_troop_get_player_relation", ":npc"),
	(assign, ":relation_with_player", reg0),
	(assign, ":player_relation_change", 0),
	(try_begin),
		#Affiliate to a family: improve relations for freeing lords
		(ge, ":talk_troop_is_affiliate", 1),
		(call_script, "script_dplmc_is_affiliated_family_member", ":npc"),
		(ge, reg0, 1),

		(try_begin),
			(lt, ":relation_with_player", 0),
			(assign, ":player_relation_change", 2),
		(else_try),
			(lt, ":relation_with_player", 10),
			(assign, ":player_relation_change", 2),
		(else_try),
			(lt, ":relation_with_player", 20),
			(store_random_in_range, ":player_relation_change", 0, 2),
		(else_try),
			(lt, ":relation_with_player", 40),
			(store_random_in_range, ":player_relation_change", -1, 2),
			(val_max, ":player_relation_change", 0),
		(try_end),
		(gt, ":player_relation_change", 0),
		(call_script, "script_change_player_relation_with_troop", ":npc", ":player_relation_change"),
	(else_try),
		#Lords friendly and/or related to the troop
		(call_script, "script_troop_get_relation_with_troop", ":npc", "$g_talk_troop"),
		(assign, ":relation", reg0),
		(try_begin),
			(ge, ":relation", 20),
			(store_random_in_range, reg0, 0, 2),
			(this_or_next|ge, ":relation", ":relation_with_player"),
				(eq, reg0, 1),
			(assign, ":player_relation_change", 1),
		(try_end),
		(try_begin),
			(ge, ":relation", 0),
			(troop_slot_eq, ":npc", slot_troop_betrothed, "$g_talk_troop"),
			(val_add, ":player_relation_change", 1),
		(else_try),
			(ge, ":relation", 0),
			(this_or_next|troop_slot_eq, ":npc", slot_troop_occupation, slto_kingdom_lady),
				(is_between, ":npc", kingdom_ladies_begin, kingdom_ladies_end),
			(call_script, "script_troop_get_family_relation_to_troop", ":npc", "$g_talk_troop"),
			(ge, reg0, 4),
			(store_random_in_range, reg0, 0, 2),
			(this_or_next|troop_slot_eq, ":npc", slot_lord_reputation_type, lrep_conventional),
			   (eq, reg0, 1),
			(val_add, ":player_relation_change", 1),
		(try_end),
		(gt, ":player_relation_change", 0),
		(call_script, "script_change_player_relation_with_troop", ":npc", ":player_relation_change"),
	(try_end),
(try_end),
##diplomacy end+
(call_script, "script_change_player_relation_with_faction_ex", "$g_talk_troop_faction", 2)]],
[anyone,"freed_lord_answer_2", [],
"Thank you. I never forget someone who's done me a good turn.", "close_window",
[
(assign, "$g_leave_encounter", 1), #Not sure why this is necessary
]],
[anyone|plyr,"defeat_lord_answer", [],
"You are my prisoner now.", "defeat_lord_answer_1",
[
#(troop_set_slot, "$g_talk_troop", slot_troop_is_prisoner, 1),
(troop_set_slot, "$g_talk_troop", slot_troop_prisoner_of_party, "p_main_party"),
(party_force_add_prisoners, "p_main_party", "$g_talk_troop", 1),#take prisoner
(call_script, "script_change_player_relation_with_troop", "$g_talk_troop", -3),
(call_script, "script_change_player_relation_with_faction_ex", "$g_talk_troop_faction", -3),
(call_script, "script_event_hero_taken_prisoner_by_player", "$g_talk_troop"),
(call_script, "script_add_log_entry", logent_lord_captured_by_player, "trp_player",  -1, "$g_talk_troop", "$g_talk_troop_faction"),
]],
[anyone,"defeat_lord_answer_1", [],
"I am at your mercy.", "close_window", []],
[anyone|plyr,"defeat_lord_answer", [],
"You have fought well. You are free to go.", "defeat_lord_answer_2",
[(call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 5),
(call_script, "script_change_player_honor", 3),
(call_script, "script_add_log_entry", logent_lord_defeated_but_let_go_by_player, "trp_player",  -1, "$g_talk_troop", "$g_talk_troop_faction")]],
[anyone,"defeat_lord_answer_2", [],
"{s43}", "close_window", [
(call_script, "script_lord_comment_to_s43", "$g_talk_troop", "str_prisoner_released_default"),
 ]],
[anyone,"party_encounter_lord_hostile_attacker", [
(gt, "$g_comment_found", 0),
              ],
"{s42}", "party_encounter_lord_hostile_attacker", [
                   (try_begin),
                     (neq, "$log_comment_relation_change", 0),
                     (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", "$log_comment_relation_change"),
                   (try_end),
                   (assign, "$g_comment_found", 0),
              ]],
[anyone,"party_encounter_lord_hostile_attacker", [
              ],
"{s43}", "party_encounter_lord_hostile_attacker_2",
[
(call_script, "script_lord_comment_to_s43", "$g_talk_troop", "str_surrender_demand_default"),
 ]],
[anyone|plyr,"party_encounter_lord_hostile_attacker_2", [
              ],
"We will fight you to the end!", "close_window", []],
[anyone|plyr,"party_encounter_lord_hostile_attacker_2", [
##diplomacy start+ Support promoted ladies
#(is_between, "$g_talk_troop", active_npcs_begin, active_npcs_end),
(is_between, "$g_talk_troop", heroes_begin, heroes_end),
##diplomacy end+
(neg|faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, "$g_talk_troop"),
              ],
"Stay your hand! There is something I must tell you in private.", "lord_recruit_1_relation", []],
[anyone|plyr,"party_encounter_lord_hostile_attacker_2", [
              ],
"Is there no way to avoid this battle? I don't want to fight with you.", "party_encounter_offer_dont_fight", []],
[anyone|plyr,"party_encounter_lord_hostile_attacker_2", [
              ],
"Don't attack! We surrender.", "close_window", [(assign,"$g_player_surrenders",1)]],
[anyone, "party_encounter_offer_dont_fight", [(gt, "$g_talk_troop_effective_relation", 30),
#TODO: Add adition conditions, lord personalities, battle advantage, etc...
              ],
"I owe you a favor, don't I. Well... all right then. I will let you go just this once.", "close_window", [
(call_script, "script_change_player_relation_with_troop","$g_talk_troop", -7),
(store_current_hours,":protected_until"),
(val_add, ":protected_until", 72),
(party_set_slot,"$g_encountered_party",slot_party_ignore_player_until,":protected_until"),
(party_ignore_player, "$g_encountered_party", 72),
(assign, "$g_leave_encounter",1)
 ]],
[anyone, "party_encounter_offer_dont_fight", [
(troop_get_slot,":reputation", "$g_talk_troop", slot_lord_reputation_type),
(neq, ":reputation", lrep_upstanding),
(neq, ":reputation", lrep_debauched),
##diplomacy start+
(neq, ":reputation", lrep_moralist),
#Martial does not accept when marshall
(this_or_next|neq, ":reputation", lrep_martial),
   (neg|faction_slot_eq, "$g_talk_troop_faction", slot_faction_marshall, "$g_talk_troop"),

#Leaders of kingdoms never accept this (for lieges this shouldn't appear anyway)
(this_or_next|neg|is_between, "$g_talk_troop_faction", kingdoms_begin, kingdoms_end),
   (neg|faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, "$g_talk_troop"),

(assign, ":can_intrigue", 0),
(try_begin),
   (neg|is_between, "$g_talk_troop_faction", kingdoms_begin, kingdoms_end),
   (assign, ":can_intrigue", 1),
(else_try),
   (call_script, "script_cf_troop_can_intrigue", "$g_talk_troop", 1),
   (assign, ":can_intrigue", 1),
(try_end),
(eq, ":can_intrigue", 1),
##diplomacy end+

(gt, "$g_talk_troop_effective_relation", 0),
(store_mul, ":rel_sq", "$g_talk_troop_effective_relation", "$g_talk_troop_effective_relation"),
(val_mul, ":rel_sq", 5),
(store_random_in_range, ":random", 5000, 10000),
(store_sub, ":amount", ":random", ":rel_sq"),
(val_max, ":amount", 0),
##diplomacy start+ Alternate calculation, since the player is effectively "ransoming himself"
(call_script, "script_calculate_ransom_amount_for_troop", "trp_player"),
(game_get_reduce_campaign_ai, ":reduce_campaign_ai"),
(try_begin),
   (le, ":reduce_campaign_ai", 0),#Hard
   (val_mul, reg0, 3),
   (val_div, reg0, 4),
(else_try),
   (le, ":reduce_campaign_ai", 1),#Medium
   (val_div, reg0, 2),
(else_try),
   (ge, ":reduce_campaign_ai", 2),#Easy
   (val_div, reg0, 4),
(try_end),
(val_max, ":amount", reg0),
##diplomacy end+

(party_get_num_companion_stacks, ":num_stacks", "p_main_party"),
(try_for_range, ":i_stack", 0, ":num_stacks"),
(party_stack_get_size, ":stack_size", "p_main_party", ":i_stack"),
(val_mul, ":stack_size", 12),
(val_add, ":amount", ":stack_size"),
(try_end),

(val_div, ":amount", 10),
(val_mul, ":amount", 10),
(assign, reg0, ":amount"),
],
"If you pay me {reg0} mon cash I will let you go, recreant.", "party_encounter_offer_money", [
 ]],
[anyone|plyr,"party_encounter_offer_money", [
(store_troop_gold, ":cur_gold", "trp_player"),
(gt, ":cur_gold", reg0),
],
"Don't attack! I pay.", "close_window", [
##nested diplomacy start+ actually give the gold to the enemy lord
(troop_remove_gold, "trp_player", reg0),
(try_begin),
   (troop_is_hero, "$g_talk_troop"),
   (call_script, "script_dplmc_distribute_gold_to_lord_and_holdings", reg0, "$g_talk_troop"),
(try_end),
##nested diplomacy end+
(call_script, "script_change_player_relation_with_troop","$g_talk_troop", -2),
(call_script, "script_change_player_honor", -2),
(store_current_hours,":protected_until"),
(val_add, ":protected_until",  72),
(party_set_slot,"$g_encountered_party",slot_party_ignore_player_until,":protected_until"),
(party_ignore_player, "$g_encountered_party",  72),
(assign, "$g_leave_encounter",1)]
],
[anyone|plyr,"party_encounter_offer_money", [
              ],
"Let's fight!", "party_encounter_offer_money_no",
[]
],
[anyone, "party_encounter_offer_money_no", [
(call_script, "script_lord_comment_to_s43", "$g_talk_troop", "str_lord_declines_negotiation_offer_default"),
              ],
"{s43}", "close_window", []],
[anyone, "party_encounter_offer_dont_fight", [
(call_script, "script_lord_comment_to_s43", "$g_talk_troop", "str_lord_declines_negotiation_offer_default"),
              ],
"{s43}", "close_window", []],
[anyone|plyr ,"pretender_intro_1", [], "My name is {playername}. At your service.", "pretender_intro_2", []],
[anyone|plyr ,"pretender_intro_1", [], "I am {playername}. Perhaps you have heard of my exploits.", "pretender_intro_2", []],
[anyone ,"pretender_intro_2", [(troop_get_slot, ":rebellion_string", "$g_talk_troop", slot_troop_original_faction),
                           (val_sub, ":rebellion_string", "fac_kingdom_1"),
                           (val_add, ":rebellion_string", "str_swadian_rebellion_pretender_intro"),
                           (str_store_string, 48, ":rebellion_string"),],
"{s48}", "pretender_intro_3", []],
[anyone|plyr ,"pretender_intro_3", [(troop_get_slot, ":original_faction", "$g_talk_troop", slot_troop_original_faction),
                                (str_store_faction_name, s12, ":original_faction"),
                                (faction_get_slot, ":original_ruler", ":original_faction", slot_faction_leader),
                                (str_store_troop_name, s11, ":original_ruler"),],
#gekokujo 3.0 pretender dialogue tweaks start
#"I thought {s12} was ruled by {s11}?", "pretender_rebellion_cause_1", [
"Isn't that ruled by {s11} of the {s12}?", "pretender_rebellion_cause_1", [
#gekokujo 3.0 pretender dialogue tweaks end
(troop_set_slot, "$g_talk_troop", slot_troop_discussed_rebellion, 1)
]],
[anyone|plyr ,"pretender_start",
[
(troop_slot_eq, "$g_talk_troop", slot_troop_discussed_rebellion, 1),
(eq, "$pretender_told_story", 0)
],
"What was your story again, {reg65?my lady:sir}?", "pretender_rebellion_cause_prelim", [
]],
[anyone,"pretender_rebellion_cause_prelim", [],
"I shall tell you.", "pretender_rebellion_cause_1", [
               ]],
[anyone,"pretender_rebellion_cause_1", [],
"{s48}", "pretender_rebellion_cause_2", [
               (assign, "$pretender_told_story", 1),
               (troop_get_slot, ":rebellion_string", "$g_talk_troop", slot_troop_original_faction),
               (val_sub, ":rebellion_string", "fac_kingdom_1"),
               (val_add, ":rebellion_string", "str_swadian_rebellion_pretender_story_1"),
               (str_store_string, 48, ":rebellion_string"),
               ]],
[anyone,"pretender_rebellion_cause_2", [],
"{s48}", "pretender_rebellion_cause_3", [
               (troop_get_slot, ":rebellion_string", "$g_talk_troop", slot_troop_original_faction),
               (val_sub, ":rebellion_string", "fac_kingdom_1"),
               (val_add, ":rebellion_string", "str_swadian_rebellion_pretender_story_2"),
               (str_store_string, 48, ":rebellion_string"),
               ]],
[anyone,"pretender_rebellion_cause_3", [],
"{s48}", "pretender_start", [
               (troop_get_slot, ":rebellion_string", "$g_talk_troop", slot_troop_original_faction),
               (val_sub, ":rebellion_string", "fac_kingdom_1"),
               (val_add, ":rebellion_string", "str_swadian_rebellion_pretender_story_3"),
               (str_store_string, 48, ":rebellion_string"),
               ]],
[anyone|plyr ,"pretender_start", [
              (troop_slot_eq, "$g_talk_troop", slot_troop_discussed_rebellion, 1),
               ],
"I want to take up your cause and help you reclaim your clan!", "pretender_discuss_rebellion_1", [
]],
[anyone|plyr ,"pretender_start", [
               ],
"I must leave now.", "pretender_end", [
]],
[anyone ,"pretender_discuss_rebellion_1", [(troop_get_slot, ":original_faction", "$g_talk_troop", slot_troop_original_faction),
                                       (faction_get_slot, ":original_ruler", ":original_faction", slot_faction_leader),
##diplomacy start+ Change "lords" to {s0}
                                       (call_script, "script_dplmc_print_cultural_word_to_sreg", "$g_talk_troop", DPLMC_CULTURAL_TERM_LORD_PLURAL,0),
                                       (str_store_troop_name, s11, ":original_ruler")],
"Are you sure you will be up to the task, {playername}? Reclaiming my clan will be no simple matter.\
The {s0} of our domain have all sworn oaths of loyalty to {s11}.\
Such oaths to a usurper are of course invalid, and we can expect some of the {s0} to side with us, but it will be a very tough and challenging struggle ahead.", "pretender_discuss_rebellion_2a", []],
[anyone ,"pretender_discuss_rebellion_2a",[
                           (troop_get_slot, ":original_faction", "$g_talk_troop", slot_troop_original_faction),
                                      (faction_get_slot, ":original_ruler", ":original_faction", slot_faction_leader),
                           (str_store_troop_name, s12, ":original_ruler"),
                                      (call_script, "script_evaluate_realm_stability", ":original_faction"),
                           (assign, ":instability_index", reg0),
                           (val_add, ":instability_index", reg0),
                           (val_add, ":instability_index", reg1),
                           (try_begin),
                              (gt, ":instability_index", 60),
                              (str_store_string, s11, "str_one_thing_in_our_favor_is_that_s12s_grip_is_very_shaky_he_rules_over_a_labyrinth_of_rivalries_and_grudges_lords_often_fail_to_cooperate_and_many_would_happily_seek_a_better_liege"),
                           (else_try),
                              (is_between, ":instability_index", 40, 60),
                              (str_store_string, s11, "str_thankfully_s12s_grip_is_fairly_shaky_many_lords_do_not_cooperate_with_each_other_and_some_might_be_tempted_to_seek_a_better_liege"),
                           (else_try),
                              (is_between, ":instability_index", 20, 40),
                              (str_store_string, s11, "str_unfortunately_s12s_grip_is_fairly_strong_until_we_can_shake_it_we_may_have_to_look_long_and_hard_for_allies"),
                           (else_try),
                              (lt, ":instability_index", 20),
                              (str_store_string, s11, "str_unfortunately_s12s_grip_is_very_strong_unless_we_can_loosen_it_it_may_be_difficult_to_find_allies"),
                           (try_end),
                            ],
"{s11}", "pretender_discuss_rebellion_2", []],
[anyone|plyr ,"pretender_discuss_rebellion_2", [],  "I am ready for this struggle.", "pretender_discuss_rebellion_3", []],
[anyone|plyr ,"pretender_discuss_rebellion_2", [],  "You are right. Perhaps, I should think about this some more.", "pretender_end", []],
[anyone ,"pretender_discuss_rebellion_3", [(this_or_next|neg|faction_slot_eq, "fac_player_supporters_faction", slot_faction_state, sfs_active),
                            (neg|faction_slot_eq, "fac_player_supporters_faction", slot_faction_leader, "trp_player"),
                            (neg|troop_slot_ge, "trp_player",slot_troop_renown, 200),
                                       (troop_get_slot, ":original_faction", "$g_talk_troop", slot_troop_original_faction),
                                       (faction_get_slot, ":original_ruler", ":original_faction", slot_faction_leader),
                                       (str_store_troop_name, s11, ":original_ruler")],
"I have no doubt that your support for my cause is heartfelt, {playername}, and I am grateful to you for it. \
But I don't think we have much of a chance of success. \
If you can gain renown in the battlefield and make a name for yourself as a great commander, then our friends would not hesitate to join our cause, \
and our enemies would be wary to take up arms against us. When that time comes, I will come with you gladly. \
But until that time, it will be wiser not to openly challange the usurper, {s11}.", "close_window", []],
[anyone ,"pretender_discuss_rebellion_3", [(this_or_next|neg|faction_slot_eq, "fac_player_supporters_faction", slot_faction_state, sfs_active),
                            (neg|faction_slot_eq, "fac_player_supporters_faction", slot_faction_leader, "trp_player"),
                            (gt, "$supported_pretender", 0),
                                       (str_store_troop_name, s17, "$supported_pretender")],
"Haven't you already taken up the cause of {s17}? \
You must have a very strong sense of justice, indeed. \
But no, thank you. I will not be part of your game.", "close_window", []],
[anyone ,"pretender_discuss_rebellion_3", [(this_or_next|neg|faction_slot_eq, "fac_player_supporters_faction", slot_faction_state, sfs_active),
                            (neg|faction_slot_eq, "fac_player_supporters_faction", slot_faction_leader, "trp_player"),
                            (gt, "$players_kingdom", 0),
                                       (neq, "$players_kingdom", "fac_player_supporters_faction"),
                                       (neq, "$players_kingdom", "fac_player_faction"),
                                       (troop_get_slot, ":original_faction", "$g_talk_troop", slot_troop_original_faction),
                                       (neq, "$players_kingdom", ":original_faction"),
                                       (eq, "$player_has_homage", 1),

                                       (str_store_faction_name, s16, "$players_kingdom"),
                                       (faction_get_slot, ":player_ruler", "$players_kingdom", slot_faction_leader),
                                       (str_store_troop_name, s15, ":player_ruler"),
                                       (str_store_faction_name, s17, ":original_faction"),
                                       ],
"{playername}, you are already oath-bound to serve {s15}.\
As such, I cannot allow you to take up my cause, and let my enemies claim that I am but a mere puppet of {s16}.\
No, if I am to have the overlordship of {s17}, I must do it due to the righteousness of my cause and the support of my vassals alone.\
If you want to help me, you must first free yourself of your oath to {s15}.", "close_window", []],
[anyone ,"pretender_discuss_rebellion_3", [(faction_slot_eq, "fac_player_supporters_faction", slot_faction_state, sfs_active),
                            (faction_slot_eq, "fac_player_supporters_faction", slot_faction_leader, "trp_player")],
"You are a monarch in your own right, {sir/my lady}. If you were to back me, I would be merely your puppet.", "close_window", []],
[anyone ,"pretender_discuss_rebellion_3", [(troop_get_slot, ":original_faction", "$g_talk_troop", slot_troop_original_faction),
                                       (str_store_faction_name, s12, ":original_faction"),
                                       (faction_get_slot, ":original_ruler", ":original_faction", slot_faction_leader),
                                       (str_store_troop_name, s11, ":original_ruler"),
##diplomacy start+ replace "his" with "{reg0?her:his}"
(call_script, "script_dplmc_store_troop_is_female", ":original_ruler"),
],
"You are a capable warrior, {playername}, and I am sure with your renown as a commander, and my righteous cause, the samurai and the good people of {s12} will flock to our support.\
The time is ripe for us to act! I will come with you, and together, we will topple the usurper {s11} and take the overlordship from {reg0?her:his} bloodied hands.\
But first, you must give me your oath of loyalty and accept me as your overlord {reg65?lady:lord}.", "pretender_rebellion_ready", []],
[anyone|plyr ,"pretender_rebellion_ready", [
			##diplomacy start+
            ##OLD:   (troop_get_type, reg3, "$g_talk_troop"),
			(assign, reg3, 0),
			(try_begin),
				(call_script, "script_cf_dplmc_troop_is_female", "$g_talk_troop"),
				(assign, reg3, 1),
			(try_end),
			(assign, reg65, reg3),
			##diplomacy end+
               ],
"I am ready to pledge myself to your cause, {reg3?my lady:sir}.", "lord_give_oath_2", [
]],
[anyone|plyr ,"pretender_rebellion_ready", [
               ],
"Let us bide our time a little longer.", "pretender_end", [
]],
[anyone ,"pretender_end", [
               ],
"Farewell for now, then.", "close_window", [
]],
[anyone,"lair_quest_intermediate_1",
[
], "Splendid work, {playername} -- your audacious attack is the talk of the clan. No doubt they, or others like them, will soon be back, but for a short while you have bought this land a small respite. We are most grateful to you.", "lord_pretalk",
[
(quest_get_slot, ":quest_gold_reward", "qst_destroy_bandit_lair", slot_quest_gold_reward),
(call_script, "script_troop_add_gold", "trp_player", ":quest_gold_reward"),
(assign, ":xp_reward", ":quest_gold_reward"),
(val_mul, ":xp_reward", 2),
(add_xp_as_reward, ":xp_reward"),
(call_script, "script_change_troop_renown", "trp_player", 3),
(call_script, "script_troop_change_relation_with_troop", "trp_player", "$g_talk_troop", 4),
(call_script, "script_end_quest", "qst_destroy_bandit_lair"),
(assign, reg5, ":quest_gold_reward"),
]],
[anyone,"lair_quest_intermediate_2",
[], "Well, {playername}, I guess that at least some of those brigands eluded you -- and of course, it will be the peaceful travellers of this land who will pay the price. Still, it was good of you to try.", "lord_pretalk",
[
(call_script, "script_end_quest", "qst_destroy_bandit_lair"),
]],
[anyone|plyr, "quest_meet_spy_in_enemy_town_completed", [],
"I have the reports you wanted right here.", "quest_meet_spy_in_enemy_town_completed_2",[]],
[anyone, "quest_meet_spy_in_enemy_town_completed_2", [],
"Ahh, well done. It's good to have competent {men/people} on my side. Here is the payment I promised you.", "lord_pretalk",
[
(call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 3),
(add_xp_as_reward, 500),
(quest_get_slot, ":gold", "qst_meet_spy_in_enemy_town", slot_quest_gold_reward),
(call_script, "script_troop_add_gold", "trp_player", ":gold"),
(call_script, "script_end_quest", "qst_meet_spy_in_enemy_town"),
]],
[anyone,"offer_gift_quest_complete", [
(quest_get_slot, ":target_troop", "qst_offer_gift", slot_quest_target_troop),
##diplomacy start+
#(troop_get_type, reg4, ":target_troop"),
(call_script, "script_dplmc_store_troop_is_female_reg", ":target_troop", 4),
##diplomacy end+
],
"Ah, let me take those. Hopefully this will mend the quarrel between you two. You may wish to speak to {reg4?her:him}, and see if I had any success.", "close_window",[
(quest_set_slot, "qst_offer_gift", slot_quest_current_state, 2),
#gekokujo 3.0 integrating 1.158 change start
(quest_set_slot, "qst_offer_gift", slot_quest_expiration_days, 365),
#gekokujo 3.0 integrating 1.158 change end
(troop_remove_item, "trp_player", "itm_furs"),
(troop_remove_item, "trp_player", "itm_velvet"),
(assign, "$g_leave_encounter", 1),
]],
[anyone,"intrigue_quest_state_complaint", [
(assign, ":continue", 1),
(try_begin),
(call_script, "script_cf_troop_can_intrigue", "$g_talk_troop", 1),
(assign, ":continue", 0),
(try_end),
(eq, ":continue", 1),
],
"Whatever you have to say, I would ask you to wait until we are alone.", "lord_pretalk",[
]],
[anyone,"intrigue_quest_state_complaint", [
],
##diplomacy start+ change "sew" to "sow"
"What is it? I value your opinion, although I hope that you are not trying to sow dissension among my vassals? ", "intrigue_quest_state_complaint_plyr",[
##diplomacy end+

(quest_get_slot, ":target_troop", "qst_intrigue_against_lord", slot_quest_target_troop),
(call_script, "script_troop_get_relation_with_troop", ":target_troop", "$g_talk_troop"),
(assign, reg4, reg0),
(str_store_troop_name, s4, ":target_troop"),
(assign, reg5, "$g_talk_troop_effective_relation"),

(try_begin),
(eq, "$cheat_mode", 1),
(str_store_string, s12, "str_intrigue_success_chance"),
(display_message, "str_s12"),
(try_end),
]],
[anyone|plyr,"intrigue_quest_state_complaint_plyr", [
(check_quest_active, "qst_intrigue_against_lord"),
(quest_get_slot, ":target_troop", "qst_intrigue_against_lord", slot_quest_target_troop),
(str_store_troop_name, s4, ":target_troop"),
(troop_get_slot, ":reputation_string", ":target_troop", slot_lord_reputation_type),
(val_add, ":reputation_string", "str_lord_derogatory_default"),
(str_store_string, s5, ":reputation_string"),
],
"Oyakata-sama -- {s4} is widely held by your vassals to be {s5}, and a liability to your domain", "lord_intrigue_quest_complaint_stated",[
]],
[anyone|plyr,"intrigue_quest_state_complaint_plyr", [
],
"Actually, oyakata-sama, never mind.", "lord_pretalk",[
(call_script, "script_fail_quest", "qst_intrigue_against_lord"),
]],
[anyone|plyr,"intrigue_quest_state_complaint_failed", [
],
"I stand by my words, oyakata-sama.", "intrigue_quest_state_accept_blame",[
(call_script, "script_change_player_honor", 1),
]],
[anyone|plyr,"intrigue_quest_state_complaint_failed", [
(quest_get_slot, ":giver_troop", "qst_intrigue_against_lord", slot_quest_giver_troop),
(quest_get_slot, ":target_troop", "qst_intrigue_against_lord", slot_quest_target_troop),

(str_store_troop_name, s4, ":giver_troop"),
(str_store_troop_name, s5, ":target_troop"),
],
"Yes, my {lord/lady} -- {s4} put me up to denouncing {s5}!", "intrigue_quest_state_deflect_blame",[
(quest_get_slot, ":giver_troop", "qst_intrigue_against_lord", slot_quest_giver_troop),
(call_script, "script_troop_change_relation_with_troop", "$g_talk_troop", ":giver_troop", -5),
(call_script, "script_troop_change_relation_with_troop", "$g_talk_troop", "trp_player", 4),
(call_script, "script_change_player_honor", -2),
]],
[anyone,"intrigue_quest_state_accept_blame", [
],
"Indeed. You may stand by your words, but keep them to yourself. I will not have you undercutting my faithful follower {s4}.", "lord_pretalk",[
]],
[anyone,"intrigue_quest_state_deflect_blame", [
],
"I thought as much. Here's some advice for you, {lad/lassie} -- don't meddle in the quarrels of others. Now, enough of this.", "lord_pretalk",[
]],
[anyone,"hero_pretalk", [],
"Anything else?", "lord_talk",[]],
[anyone,"denounce_lord_results",[
(check_quest_succeeded, "qst_denounce_lord"),
(faction_get_slot, ":faction_leader", "$g_talk_troop_faction", slot_faction_leader),
(str_store_troop_name, s4, ":faction_leader"),
##diplomacy start+ Get gender of quest target
(quest_get_slot, ":target_troop", "qst_denounce_lord", slot_quest_target_troop),
(call_script, "script_dplmc_store_troop_is_female", ":target_troop"),
##diplomacy end+

],
##diplomacy start+ replace "him" with "{reg0?her:him}"
"Yes, and hopefully now {s4} will think twice before entrusting {reg0?her:him} with any additional fiefs, honors, or offices. We are grateful to you.", "lord_pretalk",
##diplomacy end+
[
(call_script, "script_succeed_quest", "qst_denounce_lord"),
(call_script, "script_end_quest", "qst_denounce_lord"),
(call_script, "script_troop_change_relation_with_troop", "$g_talk_troop", "trp_player", 8),
(add_xp_as_reward, 1000),
]],
[anyone,
"denounce_lord_results",[
#	(check_quest_failed, "qst_denounce_lord"),
##diplomacy start+ Get gender of quest target
(quest_get_slot, ":target_troop", "qst_denounce_lord", slot_quest_target_troop),
(call_script, "script_dplmc_store_troop_is_female", ":target_troop"),
##diplomacy end+
],
##diplomacy start+ next line, replace "he" with "{reg0?she:he}"
"So you did -- and we have heard that {reg0?she:he} forced you to retract your words, and thus emerged from this affair looking stronger than before. You will forgive me, {sir/my lady}, if my gratitude to you is somewhat muted.", "close_window",
##diplomacy end+
[
(call_script, "script_end_quest", "qst_denounce_lord"),

]],
[anyone,"convince_accept",[(check_quest_active, "qst_collect_debt"),
                       (quest_slot_eq, "qst_collect_debt", slot_quest_target_troop, "$g_talk_troop"),
                       (quest_get_slot, ":quest_giver_troop", "qst_collect_debt", slot_quest_giver_troop),
                       (str_store_troop_name,s8,":quest_giver_troop"),
                       ##diplomacy start+ #Store gender of creditor
                       (call_script, "script_dplmc_store_troop_is_female", ":quest_giver_troop"),
                       ##diplomacy end+
                       (quest_get_slot, reg10, "qst_collect_debt", slot_quest_target_amount)],
##diplomacy start+ Next lines, replace "him" with "{reg0?her:him}"
"My debt to {s8} has long been overdue and was a source of great discomfort to me.\
Thank you for accepting to take the money to {reg0?her:him}.\
Please give {reg0?her:him} these {reg10} mon and thank {reg0?her:him} on my behalf.", "close_window",
##diplomacy end+
[(call_script, "script_troop_add_gold", "trp_player", reg10),
(quest_set_slot,  "qst_collect_debt", slot_quest_current_state, 1),
(call_script, "script_succeed_quest", "qst_collect_debt"),
(assign, "$g_leave_encounter", 1),
]],
[anyone,"convince_accept",[(check_quest_active, "qst_persuade_lords_to_make_peace"),
                       (this_or_next|quest_slot_eq, "qst_persuade_lords_to_make_peace", slot_quest_target_troop, "$g_talk_troop"),
                       (quest_slot_eq, "qst_persuade_lords_to_make_peace", slot_quest_object_troop, "$g_talk_troop"),
                       (quest_get_slot, ":quest_object_faction", "qst_persuade_lords_to_make_peace", slot_quest_object_faction),
                       (quest_get_slot, ":quest_target_faction", "qst_persuade_lords_to_make_peace", slot_quest_target_faction),
                       (str_store_faction_name, s12, ":quest_object_faction"),
                       (str_store_faction_name, s13, ":quest_target_faction"),
                       (try_begin), # store name of other faction
                         (eq,":quest_object_faction","$g_talk_troop_faction"),
                         (str_store_faction_name, s14, ":quest_target_faction"),
                         (else_try),
                         (str_store_faction_name, s14, ":quest_object_faction"),
                       (try_end),
                       ],
"You... have convinced me, {playername}. Very well then, you've my blessing to bring a peace offer to {s14}. I cannot guarantee they will accept it, but on the off-chance they do, I will stand by it.", "close_window",
[(store_mul, ":new_value", "$g_talk_troop", -1),
(try_begin),
(quest_slot_eq, "qst_persuade_lords_to_make_peace", slot_quest_target_troop, "$g_talk_troop"),
(quest_set_slot, "qst_persuade_lords_to_make_peace", slot_quest_target_troop, ":new_value"),
(else_try),
(quest_set_slot, "qst_persuade_lords_to_make_peace", slot_quest_object_troop, ":new_value"),
(try_end),
(quest_set_slot, "qst_persuade_lords_to_make_peace", slot_quest_convince_value, 1500),#reseting convince value for the second persuasion
(assign, "$g_leave_encounter", 1),
(neg|quest_slot_ge, "qst_persuade_lords_to_make_peace", slot_quest_target_troop, 0),
(neg|quest_slot_ge, "qst_persuade_lords_to_make_peace", slot_quest_object_troop, 0),
(call_script, "script_succeed_quest", "qst_persuade_lords_to_make_peace"),
]],
[anyone,"combined_political_quests", [
(troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_hero),
(lt, "$g_talk_troop_effective_relation", -5),
##diplomacy start+
#For affiliated family members, increase willingness to intrigue
(call_script, "script_dplmc_is_affiliated_family_member", "$g_talk_troop"),
(lt, reg0, 1),
##diplomacy end+
],
"I do not imagine that you and I have many mutual interests.", "lord_pretalk",[
]],
[anyone,"combined_political_quests", [
(troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_hero),
(gt, "$political_quest_found", 0),
(assign, ":continue", 1),
(try_begin),
(call_script, "script_cf_troop_can_intrigue", "$g_talk_troop", 1),
(assign, ":continue", 0),
(try_end),
(eq, ":continue", 1),
],
"Hmm.. Perhaps we can discuss this matter in a more private setting, at a later date.", "lord_pretalk",[
]],
[anyone,"combined_political_quests", [
(this_or_next|eq, "$political_quest_found", "qst_intrigue_against_lord"),
(eq, "$political_quest_found", "qst_denounce_lord"),

(troop_slot_ge, "trp_player", slot_troop_controversy, 30),

##diplomacy start+ Use culturally-appropriate term
(call_script, "script_dplmc_print_cultural_word_to_sreg", "$g_talk_troop", DPLMC_CULTURAL_TERM_LORD_PLURAL,0),
],
##Next line, replace "lords" with {s0}
"Hmm.. I do have an idea, but it would require you that you be free of controversy. If you were to wait some time without getting into any arguments with the other {s0} of our domain, perhaps we could proceed further.", "lord_pretalk",[
##diplomacy end+
]],
[anyone,"party_encounter_lord_hostile_ultimatum_surrender", [],
"{s43}", "close_window", [
    (call_script, "script_lord_comment_to_s43", "$g_talk_troop", "str_lord_challenged_default"),

    (call_script, "script_make_kingdom_hostile_to_player", "$g_encountered_party_faction", -3),

    (try_begin),
      (gt, "$g_talk_troop_relation", -10),
      (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", -1),
    (try_end),
    (assign,"$encountered_party_hostile",1),
    (assign,"$encountered_party_friendly",0),]],
[anyone,"liege_defends_claim_1", [],
"Oh really? It is not everyone who dares mention that name in my presence. I am not sure whether to reward your bravery, or punish you for your impudence.", "liege_defends_claim_2", [
                         (troop_set_slot, "$g_talk_troop", slot_troop_discussed_rebellion, 1),
                 ]],
[anyone,"liege_defends_claim_2", [],
"Very well. I will indulge your curiosity. But listen closely, because I do not wish to speak of this matter again.", "liege_defends_claim_3", [
                 ]],
[anyone,"liege_defends_claim_3", [],
"{s48}", "liege_defends_claim_4", [
                  (store_sub, ":rebellion_string", "$g_talk_troop_faction", "fac_kingdom_1"),
                  (val_add, ":rebellion_string", "str_swadian_rebellion_monarch_response_1"),
                  (str_store_string, 48, ":rebellion_string"),
                  ]],
[anyone,"liege_defends_claim_4", [],
"{s48}", "lord_talk", [
                  (store_sub, ":rebellion_string", "$g_talk_troop_faction", "fac_kingdom_1"),
                  (val_add, ":rebellion_string", "str_swadian_rebellion_monarch_response_2"),
                  (str_store_string, 48, ":rebellion_string"),
                  ]],
[anyone|plyr,"party_encounter_lord_hostile_attacker_2",
[
  (eq, "$cheat_mode", 2),
  (gt, "$supported_pretender", 0),
  (eq, "$supported_pretender_old_faction", "$g_talk_troop_faction"),
  (neg|faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, "$g_talk_troop"),
  (troop_slot_ge, "$g_talk_troop", slot_troop_leaded_party, 1),
  ],
"{!}CHEAT - Join our cause by force.", "lord_join_rebellion_suggest_cheat",[]],
[anyone ,"knight_offer_join", [(call_script, "script_cf_is_quest_troop", "$g_talk_troop")],
"I fear I cannot join you at the moment, {playername}, I've important business to attend to and it cannot wait.", "hero_pretalk",[]],
[anyone ,"knight_offer_join", [(lt, "$g_talk_troop_relation", 5),
                              (store_character_level,":player_level","trp_player"),
                              (store_character_level,":talk_troop_level","$g_talk_troop"),
                              (val_mul,":player_level",2),
                              (lt, ":player_level", ":talk_troop_level")],
"You forget your place, {sir/madam}. I do not take orders from the likes of you.", "hero_pretalk",[]],
[anyone ,"knight_offer_join", [
    (assign, ":num_player_companions",0),
    (try_for_range, ":hero_id", heroes_begin, heroes_end),
      (troop_slot_eq, ":hero_id",slot_troop_occupation, slto_player_companion),
      (val_add, ":num_player_companions",1),
    (try_end),
    (assign, reg5, ":num_player_companions"),
    (store_add, reg6, reg5, 1),
    (val_mul, reg6,reg6),
    (val_mul, reg6, 1000),
    (gt, reg6,0)], #note that we abuse the value of reg6 in the next line.
"I would be glad to fight at your side, my friend, but there is a problem...\
The thing is, I've found myself in a bit of debt that I must repay very soon. {reg6} mon altogether,\
and I am honour-bound to return every coin. Unless you've got {reg6} mon with you that you can spare,\
I've to keep my mind on getting this weight off my neck.", "knight_offer_join_2",[]],
[anyone ,"knight_offer_join", [(gt,reg6, 100000)], "Join you? I think not.", "close_window",[]],
[anyone ,"knight_offer_join", [], "Aye, my friend, I'll be happy to join you.", "knight_offer_join_2",[]],
[anyone|plyr,"knight_offer_join_2", [(gt, reg6,0),(store_troop_gold, ":gold", "trp_player"),(gt,":gold",reg6)],
"Here, take it, all {reg6} mon you need. 'Tis only money.", "knight_offer_join_accept",[(troop_remove_gold, "trp_player",reg6)]],
[anyone|plyr,"knight_offer_join_2", [(le, reg6,0)], "Then let us ride together, my friend.", "knight_offer_join_accept",[]],
[anyone|plyr,"knight_offer_join_2", [(eq, "$talk_context", tc_hero_freed)], "That's good to know. I will think on it.", "close_window",[]],
[anyone|plyr,"knight_offer_join_2", [(neq, "$talk_context", tc_hero_freed)], "That's good to know. I will think on it.", "hero_pretalk",[]],
[anyone ,"knight_offer_join_accept", [(troop_slot_ge, "$g_talk_troop", slot_troop_leaded_party, 1)],
"I've some trusted men in my band who could be of use to you. What do you wish to do with them?", "knight_offer_join_accept_party",[
   ]],
[anyone ,"knight_offer_join_accept", [], "Ah, certainly, it might be fun!", "close_window",[
   (call_script, "script_recruit_troop_as_companion", "$g_talk_troop"),
   (assign, "$g_leave_encounter",1)
   ]],
[anyone|plyr,"knight_offer_join_accept_party", [], "You may disband your men. I've no need for other troops.", "knight_join_party_disband",[]],
[anyone|plyr,"knight_offer_join_accept_party", [(troop_get_slot, ":companions_party","$g_talk_troop", slot_troop_leaded_party),
                                    (party_can_join_party,":companions_party","p_main_party"),
   ], "Your men may join as well. We need every soldier we can muster.", "knight_join_party_join",[]],
[anyone|plyr,"knight_offer_join_accept_party", [(is_between,"$g_encountered_party",centers_begin, centers_end)], "Lead your men out of the town. I shall catch up with you on the road.", "knight_join_party_lead_out",[]],
[anyone|plyr,"knight_offer_join_accept_party", [(neg|is_between,"$g_encountered_party",centers_begin, centers_end)],
"Keep doing what you were doing. I'll catch up with you later.", "knight_join_party_lead_out",[]],
[anyone ,"knight_join_party_disband", [], "Ah . . . Very well, {playername}. Much as I dislike losing good men,\
the decision is yours. I'll disband my troops and join you.", "close_window",[
   (call_script, "script_recruit_troop_as_companion", "$g_talk_troop"),

   (troop_get_slot, ":companions_party","$g_talk_troop", slot_troop_leaded_party),
   (party_detach, ":companions_party"),
   (remove_party, ":companions_party"),
   (assign, "$g_leave_encounter",1)
   ]],
[anyone ,"knight_join_party_join", [], "Excellent.\
My lads and I will ride with you.", "close_window",[
   (call_script, "script_recruit_troop_as_companion", "$g_talk_troop"),
   (party_remove_members, "p_main_party", "$g_talk_troop", 1),

   (troop_get_slot, ":companions_party","$g_talk_troop", slot_troop_leaded_party),
   (assign, "$g_move_heroes", 1),
   (call_script, "script_party_add_party", "p_main_party", ":companions_party"),
   (party_detach, ":companions_party"),
   (remove_party, ":companions_party"),
   (assign, "$g_leave_encounter",1)
   ]],
[anyone ,"knight_join_party_lead_out", [], "Very well then.\
I shall maintain a patrol of this area. Return if you have further orders for me.", "close_window",[
   (call_script, "script_recruit_troop_as_companion", "$g_talk_troop"),
   (party_remove_members, "p_main_party", "$g_talk_troop", 1),

   (troop_get_slot, ":companions_party","$g_talk_troop", slot_troop_leaded_party),
   (party_set_faction, ":companions_party", "fac_player_supporters_faction"),
   (party_detach, ":companions_party"),
   (party_set_ai_behavior, ":companions_party", ai_bhvr_patrol_location),
   (party_set_flags, ":companions_party", pf_default_behavior, 0),
   ]],
[anyone,"capture_enemy_hero_thank", [],
"Many thanks, my friend. He will serve very well for a bargain. You've done a fine work here. Please accept these {reg5} mon for your help.", "capture_enemy_hero_thank_2",
[(quest_get_slot, ":quest_target_troop", "qst_capture_enemy_hero", slot_quest_target_troop),
  (quest_get_slot, ":quest_target_faction", "qst_capture_enemy_hero", slot_quest_target_faction),
  (party_remove_prisoners, "p_main_party", ":quest_target_troop", 1),
  (store_relation, ":reln", "$g_encountered_party_faction", ":quest_target_faction"),
  (try_begin),
    (lt, ":reln", 0),
    (party_add_prisoners, "$g_encountered_party", ":quest_target_troop", 1), #Adding him to the dungeon
  (else_try),
    #Do not add a non-enemy lord to the dungeon (due to recent diplomatic changes or due to a neutral town/castle)
    #(troop_set_slot, ":quest_target_troop", slot_troop_is_prisoner, 0),
    (troop_set_slot, ":quest_target_troop", slot_troop_prisoner_of_party, -1),
  (try_end),
  (quest_get_slot, ":reward", "qst_capture_enemy_hero", slot_quest_gold_reward),
  (assign, reg5, ":reward"),
  (call_script, "script_troop_add_gold", "trp_player", ":reward"),
  (add_xp_as_reward, 2500),
  (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 4),
  (call_script, "script_end_quest", "qst_capture_enemy_hero"),
]],
[anyone|plyr,"capture_enemy_hero_thank_2", [],
"Certainly, {s65}.", "lord_pretalk",[]],
[anyone|plyr,"capture_enemy_hero_thank_2", [],
"It was nothing.", "lord_pretalk",[]],
[anyone|plyr,"capture_enemy_hero_thank_2", [],
"Give me more of a challenge next time.", "lord_pretalk",[]],
[anyone,"quest_meet_spy_in_enemy_town_accepted", [], "Excellent! Make your way to {s13} as soon as you can, the spy will be waiting.", "quest_meet_spy_in_enemy_town_accepted_response",
   [
     (quest_get_slot, ":quest_target_center", "$random_quest_no", slot_quest_target_center),
     (quest_get_slot, ":secret_sign", "$random_quest_no", slot_quest_target_amount),
     (store_sub, ":countersign", ":secret_sign", secret_signs_begin),
     (val_add, ":countersign", countersigns_begin),
     (str_store_troop_name_link, s9, "$g_talk_troop"),
     (str_store_string, s11, ":secret_sign"),
     (str_store_string, s12, ":countersign"),
     (str_store_party_name_link, s13, ":quest_target_center"),
     (setup_quest_text, "$random_quest_no"),
     (str_store_string, s2, "@{s9} has asked you to meet with a spy in {s13}."),
     (call_script, "script_start_quest", "$random_quest_no", "$g_talk_troop"),
     (call_script, "script_cf_center_get_free_walker", ":quest_target_center"),
     (call_script, "script_center_set_walker_to_type", ":quest_target_center", reg0, walkert_spy),
     (str_store_item_name,s14,"$spy_item_worn"),
     #TODO: Change this value
     (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 1),
     (assign, "$g_leave_encounter",1),
    ]],
[anyone|plyr,"quest_meet_spy_in_enemy_town_accepted_response", [(quest_get_slot, ":quest_target_center", "$random_quest_no", slot_quest_target_center),
                                                                  (str_store_party_name_link, s13, ":quest_target_center")],
   "{s13} is heavily defended. How can I get close without being noticed?", "quest_meet_spy_in_enemy_town_accepted_2",
   []],
[anyone,"quest_meet_spy_in_enemy_town_accepted_2", [], "You shall have to use stealth. Take care to avoid enemy strongholds, villages and patrols, and don't bring too many men with you. If you fail to sneak in the first time, give it a while for the garrison to lower its guard again, or you may have a difficult time infiltrating the town.", "quest_meet_spy_in_enemy_town_accepted_response",
   []],
[anyone|plyr,"quest_meet_spy_in_enemy_town_accepted_response", [], "How will I recognise the spy?", "quest_meet_spy_in_enemy_town_accepted_3",
   []],
[anyone,"quest_meet_spy_in_enemy_town_accepted_3", [(quest_get_slot, ":quest_target_center", "$random_quest_no", slot_quest_target_center),
                                                      (str_store_party_name_link, s13, ":quest_target_center"),
													  ##diplomacy start+ Use script for gender
                                                      #(troop_get_type, reg7, "$spy_quest_troop"),
													  (assign, reg7, 0),
													  (try_begin),
														(call_script, "script_cf_dplmc_troop_is_female", "$spy_quest_troop"),
														(assign, reg7, 1),
													  (try_end),
													  ##diplomacy end+
                                                      (quest_get_slot, ":secret_sign", "$random_quest_no", slot_quest_target_amount),
                                                      (store_sub, ":countersign", ":secret_sign", secret_signs_begin),
                                                      (val_add, ":countersign", countersigns_begin),
                                                      (str_store_string, s11, ":secret_sign"),
                                                      (str_store_string, s12, ":countersign"),],
   "Once you get to {s13} you must talk to the locals, the spy will be one of them. If you think you've found the spy, say the phrase '{s11}' The spy will respond with the phrase '{s12}' Thus you will know the other, and {reg7?she:he} will give you any information {reg7?she:he}'s gathered in my service.", "quest_meet_spy_in_enemy_town_accepted_response",
   []],
[anyone|plyr,"quest_meet_spy_in_enemy_town_accepted_response", [], "Will I be paid?", "quest_meet_spy_in_enemy_town_accepted_4",
   []],
[anyone,"quest_meet_spy_in_enemy_town_accepted_4", [], "Of course, I have plenty of silver in my coffers for loyal {men/women} like you. Do well by me, {playername}, and you'll rise high.", "quest_meet_spy_in_enemy_town_accepted_response",
   []],
[anyone|plyr,"quest_meet_spy_in_enemy_town_accepted_response", [], "I know what to do. Farewell, my lord.", "quest_meet_spy_in_enemy_town_accepted_end",
   []],
[anyone,"quest_meet_spy_in_enemy_town_accepted_end", [(quest_get_slot, ":secret_sign", "$random_quest_no", slot_quest_target_amount),
                                                        (store_sub, ":countersign", ":secret_sign", secret_signs_begin),
                                                        (val_add, ":countersign", countersigns_begin),
                                                        (str_store_string, s11, ":secret_sign"),
                                                        (str_store_string, s12, ":countersign")],
   "Good luck, {playername}. Remember, the secret phrase is '{s11}' The counterphrase is '{s12}' Bring any reports back to me, and I'll compensate you for your trouble.", "lord_pretalk",
   []],
[anyone,"quest_meet_spy_in_enemy_town_rejected", [], "As you wish, {playername}, but I strongly advise you to forget anything I told you about any spies. They do not exist, have never existed, and no one will ever find them. Remember that.", "lord_pretalk",
   [(troop_set_slot, "$g_talk_troop", slot_troop_does_not_give_quest, 1)]],
[anyone,"quest_raid_caravan_to_start_war_accepted", [], "Very good!\
 A raid on a caravan, or, if you can't manage that, an attack on one of their villages, should do the trick.\
 Now, good luck and good hunting. Go set the borders aflame!", "close_window",
   [
     (quest_get_slot, ":quest_target_faction", "$random_quest_no", slot_quest_target_faction),
     (quest_get_slot, ":quest_target_amount", "$random_quest_no", slot_quest_target_amount),
     (str_store_troop_name_link, s9, "$g_talk_troop"),
     (str_store_faction_name_link, s13, ":quest_target_faction"),
     (assign, reg13, ":quest_target_amount"),
     (setup_quest_text,"$random_quest_no"),
     (str_store_string, s2, "str_s9_asked_you_to_attack_a_village_or_some_caravans_as_to_provoke_a_war_with_s13"),
     (call_script, "script_start_quest", "$random_quest_no", "$g_talk_troop"),
#     (call_script, "script_change_player_relation_with_troop","$g_talk_troop",5),
     (assign, "$g_leave_encounter",1),
    ]],
[anyone,"quest_raid_caravan_to_start_war_rejected_1", [], "Ah, you think so? But how long will your precious peace last? Not long, believe me.", "lord_pretalk",
   [(troop_set_slot, "$g_talk_troop", slot_troop_does_not_give_quest, 1)]],
[anyone,"quest_raid_caravan_to_start_war_rejected_2", [], "Hm. As you wish, {playername}.\
 I thought you had some fire in you, but it seems I was wrong.", "lord_pretalk",
   [(troop_set_slot, "$g_talk_troop", slot_troop_does_not_give_quest, 1)]],
[anyone,"enemy_lord_tell_mission", [(eq,"$random_quest_no","qst_lend_surgeon")],
   "I have a friend here, an old warrior, who is very sick. Pestilence has infected an old battle wound,\
 and unless he is seen to by a surgeon soon,  he will surely die. This man is dear to me, {playername},\
 but he's also stubborn as a hog and refuses to have anyone look at his injury because he doesn't trust the physicians here.\
 I have heard that you've a capable surgeon with you. If you would let your surgeon come here and have a look,\
 {reg3?she:he} may be able to convince him to give his consent to an operation.\
 Please, I will be deeply indebted to you if you grant me this request.", "lord_mission_told",
   [
     (quest_get_slot, ":quest_object_troop", "$random_quest_no", slot_quest_object_troop),
     (str_store_troop_name_link,1,"$g_talk_troop"),
##     (str_store_party_name,2,"$g_encountered_party"),
     (str_store_troop_name,3,":quest_object_troop"),
	 ##diplomacy start+ Use script for gender
     #(troop_get_type, reg3, ":quest_object_troop"),
	 (assign, reg3, 0),
	 (try_begin),
		(call_script, "script_cf_dplmc_troop_is_female", ":quest_object_troop"),
		(assign, reg3, 1),
	 (try_end),
	 ##diplomacy end+
     (setup_quest_text,"$random_quest_no"),
##     (try_begin),
##       (is_between, "$g_encountered_party", centers_begin, centers_end),
##       (setup_quest_giver, "$random_quest_no", "str_given_by_s1_at_s2"),
##     (else_try),
##       (setup_quest_giver,"$random_quest_no", "str_given_by_s1_in_wilderness"),
##     (try_end),
     (str_store_string, s2, "@Lend your experienced surgeon {s3} to {s1}."),
   ]],
[anyone,"enemy_lord_tell_mission", [(str_store_quest_name, s7, "$random_quest_no")],
   "{!}ERROR: MATCHED WITH QUEST: {s7}.", "close_window",
   []],
[anyone|plyr,"spouse_talk",
   [
   (eq, "$g_player_minister", "$g_talk_troop"),
   ],
   "As you are my chief minister, I wish to speak to about affairs of state", "minister_issues",[
 ]],
[anyone|plyr,"spouse_talk", [
	(check_quest_active, "qst_offer_gift"),
    (quest_slot_eq, "qst_offer_gift", slot_quest_giver_troop, "$g_talk_troop"),
	
    (quest_get_slot, ":target_troop", "qst_offer_gift", slot_quest_target_troop),
	(str_store_troop_name, s4, ":target_troop"),
	(player_has_item, "itm_furs"),
	(player_has_item, "itm_velvet"),
   ],
   "I have the materials for {s4}'s gift.", "offer_gift_quest_complete",[
   ]],
[anyone,"offer_gift_quest_complete", [
   (quest_get_slot, ":target_troop", "qst_offer_gift", slot_quest_target_troop),
   (troop_get_type, reg4, ":target_troop"),
   ],
   "Ah, let me take those. Hopefully this will mend the quarrel between you two. You may wish to speak to {reg4?her:him}, and see if I had any success.", "close_window",[
   (quest_set_slot, "qst_offer_gift", slot_quest_current_state, 2),
   (quest_set_slot, "qst_offer_gift", slot_quest_expiration_days, 365),
   (troop_remove_item, "trp_player", "itm_furs"),
   (troop_remove_item, "trp_player", "itm_velvet"),
   (assign, "$g_leave_encounter", 1),
]],
[anyone|plyr,"spouse_talk",
   [
   (assign, "$political_quest_to_cancel", -1),
   (try_begin),
	(check_quest_active, "qst_offer_gift"),
	(quest_slot_eq, "qst_offer_gift", slot_quest_giver_troop, "$g_talk_troop"),
    (assign, "$political_quest_to_cancel", "qst_offer_gift"),
	(str_store_string, s10, "str_offer_gift_description"),
   (else_try),
	(check_quest_active, "qst_resolve_dispute"),
	(quest_slot_eq, "qst_resolve_dispute", slot_quest_giver_troop, "$g_talk_troop"),
    (assign, "$political_quest_to_cancel", "qst_resolve_dispute"),
	(str_store_string, s10, "str_resolve_dispute_description"),
   (try_end),
   (gt, "$political_quest_to_cancel", 0),
   ],
   "Let's abandon our plan to {s10}.", "spouse_cancel_political_quest",[
 ]],
[anyone,"spouse_cancel_political_quest",
   [],
   "Are you sure you want to drop that idea?", "spouse_cancel_political_quest_confirm",[
 ]],
[anyone|plyr,"spouse_cancel_political_quest_confirm",
   [],
   "Yes, I am sure. Let's abandon that idea.", "spouse_pretalk",[
   (call_script, "script_abort_quest", "$political_quest_to_cancel", 1),
 ]],
[anyone|plyr,"spouse_cancel_political_quest_confirm",
   [],
   "Actually, never mind.", "spouse_pretalk",[
 ]],
[anyone|plyr,"spouse_talk",
   [],
   "Let us think of a way to improve our standing in this domain", "combined_political_quests",[
   (call_script, "script_get_political_quest", "$g_talk_troop"),
   (assign, "$political_quest_found", reg0),
   (assign, "$political_quest_target_troop", reg1),
   (assign, "$political_quest_object_troop", reg2),
 ]],
[anyone|plyr,"spouse_talk",
   [
	(gt, "$g_player_tournament_placement", 3),

    (this_or_next|troop_slot_ge, "$g_talk_troop", slot_lord_reputation_type, lrep_conventional),
    (this_or_next|troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_lady),
		(is_between, "$g_talk_troop", kingdom_ladies_begin, kingdom_ladies_end),
	],
   "My {reg65?wife/husband}, I would like to dedicate my successes in this recent tournament to you", "dplmc_spouse_tournament_dedication_reaction",
	[

	(try_begin),
		(gt, "$g_player_tournament_placement", 3),
		(val_sub, "$g_player_tournament_placement", 3),
		(val_mul, "$g_player_tournament_placement", 2),
	(else_try),
		(assign, "$g_player_tournament_placement", 0),
	(try_end),

    #Other spouses may be jealous.
	(try_for_range, ":spouse", heroes_begin, heroes_end),#<- Iterate because of the possibility of polygamy
		(neg|troop_slot_eq, ":spouse", slot_troop_occupation, dplmc_slto_dead),
		(neq, ":spouse", "$g_talk_troop"),
		(this_or_next|troop_slot_eq, "trp_player", slot_troop_spouse, ":spouse"),
		(this_or_next|troop_slot_eq, ":spouse", slot_troop_spouse, "trp_player"),
			(troop_slot_eq, "trp_player", slot_troop_betrothed, ":spouse"),
		(call_script, "script_troop_change_relation_with_troop", ":spouse", "trp_player", -1),
	(try_end),

	(try_begin),
		(troop_slot_eq, "$g_talk_troop", slot_lady_used_tournament, 1),
		(val_div, "$g_player_tournament_placement", 3),
		(str_store_string, s9, "str_another_tournament_dedication_oh_i_suppose_it_is_always_flattering"),
	(else_try),
		(troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_conventional),
		(val_mul, "$g_player_tournament_placement", 2),
		(str_store_string, s9, "str_do_you_why_what_a_most_gallant_thing_to_say"),
	(else_try),
		(troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_moralist),
		(val_div, "$g_player_tournament_placement", 2),
		(str_store_string, s9, "str_hmm_i_cannot_say_that_i_altogether_approve_of_such_frivolity_but_i_must_confess_myself_a_bit_flattered"),
	(else_try),
		(str_store_string, s9, "str_why_thank_you_you_are_most_kind_to_do_so"),
	(try_end),

	(call_script, "script_troop_change_relation_with_troop", "$g_talk_troop", "trp_player", "$g_player_tournament_placement"),
	(assign, "$g_player_tournament_placement", 0),
	(troop_set_slot, "$g_talk_troop", slot_lady_used_tournament, 1),
	]],
[anyone|plyr, "spouse_talk",
   [
	(neg|check_quest_active, "qst_organize_feast"),
   ],
   "I was thinking that perhaps we could host a feast", "spouse_organize_feast",[
 ]],
[anyone|plyr, "spouse_talk",
   [
   ],
   "Let us take inventory of our household possessions", "spouse_household_possessions",[
   (change_screen_loot, "trp_household_possessions"),
 ]],
[anyone, "spouse_household_possessions",
   [
   ],
   "Anyway, that is the content of our larder.", "spouse_pretalk",[
 ]],
[anyone|plyr, "spouse_talk",
   [], 
   "Let me see your equipment.", "spouse_review_equipment", 
   []],
[anyone, "spouse_review_equipment", 
   [], 
   "Very well, it's all here...", "spouse_pretalk",
   [(change_screen_equip_other)]],
[anyone|plyr,"spouse_talk",
   [],
   "We shall speak later, my {wife/husband}", "close_window",[
   	(assign, "$g_leave_encounter", 1),
 ]],
[anyone,"wedding_ceremony_bride_vow",
   [
#    (troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_lady),
#	(check_quest_active, "qst_wed_betrothed"),
#	(quest_slot_eq, "qst_wed_betrothed", slot_quest_target_troop, "$g_talk_troop"),
#	(quest_slot_eq, "qst_wed_betrothed", slot_quest_current_state, 2),
#	(neg|quest_slot_ge, "qst_wed_betrothed", slot_quest_expiration_days, 2),
    ],
   "My husband, I hearby pledge to be your wife, to stand with you in good times and bad. May the heavens smile upon us and bless us with children, livestock, and land.", "wedding_ceremony_player_vow",[
   (quest_get_slot, ":bride", "qst_wed_betrothed", slot_quest_target_troop),
   (set_conversation_speaker_troop, ":bride"),
 ]],
[anyone|plyr,"wedding_ceremony_player_vow",
   [],
   "I pledge the same. Let us be husband and wife.", "wedding_ceremony_vows_complete",[
 ]],
[anyone|plyr,"wedding_ceremony_player_vow",
   [],
   "Wait -- hold on... I'm not quite ready for this.", "close_window",[
 ]],
[anyone,"wedding_ceremony_vows_complete",
   [],
   "I now declare you and {s3} to be husband and wife. Go now to the chamber prepared for you, and we shall make arrangements for your bride to join you in your hall in {s11}.", "close_window",[
   	(call_script, "script_courtship_event_bride_marry_groom", "$g_player_bride", "trp_player", 0), #parameters from dialog
	(call_script, "script_get_kingdom_lady_social_determinants", "$g_player_bride"),
	(str_store_troop_name, s3, "$g_player_bride"),

    (try_begin),
		(neq, reg0, "trp_player"),
		(str_store_string, s11, "str_error__player_not_logged_as_groom"),
	(else_try),
		(str_store_party_name, s11, reg1),
		(troop_set_slot, "$g_player_bride", slot_troop_cur_center, reg1),
	(try_end),
 ]],
[anyone, "spouse_pretalk",
##diplomacy start+ use relation string
#   [],
#   "Is there anything else, my {husband/wife}?", "spouse_talk",[
 [	#load relation text into s0
    (call_script, "script_dplmc_print_player_spouse_says_my_husband_wife_to_s0", "$g_talk_troop", 0),
    ##diplomacy end+
],
	"Is there anything else, {s0}?", "spouse_talk", [
 ]],
[anyone,"spouse_organize_feast",
   [
   (faction_slot_eq, "$players_kingdom", slot_faction_ai_state, sfai_feast),
   (faction_slot_eq, "$players_kingdom", slot_faction_ai_object, "$g_encountered_party"),
	##diplomacy start+ load relation text into s0
    (call_script, "script_dplmc_print_player_spouse_says_my_husband_wife_to_s0", "$g_talk_troop", 0),
	##diplomacy end+
   ],
##diplomacy start+ use s0
   "A splendid idea, {s0}. However, let us wait for the current feast here to conclude, before organizing another.", "spouse_pretalk",[
]],
[anyone,"spouse_organize_feast",
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
   (neg|is_between, "$g_player_court", centers_begin, centers_end),
   	##diplomacy start+ load relation text into s0
    (call_script, "script_dplmc_print_player_spouse_says_my_husband_wife_to_s0", "$g_talk_troop", 0),
    ##diplomacy end+
   ],
   ##diplomacy start+
   "A splendid idea, {s0}. However, we must establish a court before hosting a feast.", "spouse_pretalk",[
   ##diplomacy end+
 ]],
[anyone,"spouse_organize_feast",
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
   (store_current_hours, ":hours_since_last_feast"),
   (faction_get_slot, ":last_feast_time", "$players_kingdom", slot_faction_last_feast_start_time),
   (val_sub, ":hours_since_last_feast", ":last_feast_time"),
   (try_begin),
	(ge, "$cheat_mode", 1),
	(assign, reg4, ":hours_since_last_feast"),
	(str_store_faction_name, s4, "$players_kingdom"),
	(display_message, "@{!}DEBUG -- {reg4} hours since last feast for {s4}"),
   (try_end),
   (lt, ":hours_since_last_feast", 120),
   (store_sub, ":days_to_wait", 168, ":hours_since_last_feast"),
   (val_div, ":days_to_wait", 24),
   (assign, reg3, ":days_to_wait"),
   	##diplomacy start+ load relation text into s0
    (call_script, "script_dplmc_print_player_spouse_says_my_husband_wife_to_s0", "$g_talk_troop", 0),
    ##diplomacy end+
   ],
   ##diplomacy start+
   "A splendid idea, {s0}. However, our domain has recently had a feast. Perhaps we should wait another {reg3} days before we organize another one.", "spouse_pretalk",[
   ##diplomacy end+
]],
[anyone,"spouse_organize_feast",
 	##diplomacy start+ load relation text into s0
	[
    (call_script, "script_dplmc_print_player_spouse_says_my_husband_wife_to_s0", "$g_talk_troop", 0),
   #[],
   ],
   "A splendid idea, {s0}. However, to not insult our guests, we must make sure that we can provide a large and varied repast, for the lords, their families, and their retinues. All told, we should count on a couple of hundred mouths to feed, over several days. Let us take an inventory of our household possessions...", "spouse_evaluate_larder_for_feast",[
   ##diplomacy end+
]],
[anyone, "spouse_evaluate_larder_for_feast",
   [
   (call_script, "script_internal_politics_rate_feast_to_s9", "trp_household_possessions", 600, "$players_kingdom", 0),   #party, number of guests, taste, consume items
   (assign, "$feast_quality", reg0),
   ],
   "{s9}",   "spouse_feast_confirm",[]],
[anyone|plyr, "spouse_feast_confirm",
   [
   ],
   "Let me add more items to our storehouses",   "spouse_feast_added_items", [
   (change_screen_loot, "trp_household_possessions"),
   ]],
[anyone, "spouse_feast_added_items",
   [],
   "All right -- let me reevalute what is there...",   "spouse_evaluate_larder_for_feast",[]],
[anyone|plyr, "spouse_feast_confirm",
   [
   (gt, "$feast_quality", 1),
   ],
   "Let us dispatch the invitations",   "spouse_feast_confirm_yes", []],
[anyone|plyr, "spouse_feast_confirm",
   [
   ],
   "Let us wait, then",   "spouse_pretalk",[]],
[anyone, "spouse_feast_confirm_yes",
   [ (neq, "$players_kingdom", "fac_player_supporters_faction"),],
   "I shall send word, then, that we will host a feast as soon as conditions in the land permit. You perhaps should continue to stock our larder, so that we may do justice to our reputation for hospitality.",   "spouse_pretalk",[


    (assign, ":feast_venue", -1),
    (try_begin),
		(is_between, "$g_encountered_party", walled_centers_begin, walled_centers_end),
		(this_or_next|party_slot_eq, "$g_encountered_party", slot_town_lord, "trp_player"),
			(party_slot_eq, "$g_encountered_party", slot_town_lord, "$g_talk_troop"),
		(assign, ":feast_venue", "$g_encountered_party"),
	(else_try),
		(try_for_range, ":center", walled_centers_begin, walled_centers_end),
			(eq, ":feast_venue", -1),
			(this_or_next|party_slot_eq, ":center", slot_town_lord, "trp_player"),
				(party_slot_eq, ":center", slot_town_lord, "$g_talk_troop"),
			(assign, ":feast_venue", ":center"),
		(try_end),
	(else_try),
		(is_between, "$g_encountered_party", walled_centers_begin, walled_centers_end),
		(assign, ":feast_venue", "$g_encountered_party"),
    (try_end),


	(str_store_party_name, s9, ":feast_venue"),
	(setup_quest_text, "qst_organize_feast"),
	(str_store_string, s2, "str_you_intend_to_bring_goods_to_s9_in_preparation_for_the_feast_which_will_be_held_as_soon_as_conditions_permit"),

	(quest_set_slot, "qst_organize_feast", slot_quest_target_center, ":feast_venue"),
	(quest_set_slot, "qst_organize_feast", slot_quest_expiration_days, 30),
	(call_script, "script_start_quest", "qst_organize_feast", "$g_talk_troop"),
   ]],
[anyone, "spouse_feast_confirm_yes",
   [
   ],
   "Very well, then. Let the feast begin immediately at our court {reg4?here:} in {s9}. You perhaps should continue to stock our larder, so that we may do justice to our reputation for hospitality. You may declare the feast to be concluded at any time, either by beginning a campaign or by letting it be known that the vassals can return to their homes.",   "spouse_pretalk",[

   (str_store_party_name, s9, "$g_player_court"),
   (setup_quest_text, "qst_organize_feast"),
   (str_store_string, s2, "str_you_intend_to_bring_goods_to_s9_in_preparation_for_the_feast_which_will_be_held_as_soon_as_conditions_permit"),

   (quest_set_slot, "qst_organize_feast", slot_quest_target_center, "$g_player_court"),
   (quest_set_slot, "qst_organize_feast", slot_quest_expiration_days, 30),
   (call_script, "script_start_quest", "qst_organize_feast", "$g_talk_troop"),

   (faction_set_slot, "$players_kingdom", slot_faction_ai_state, sfai_feast),
   (faction_set_slot, "$players_kingdom", slot_faction_ai_object, "$g_player_court"),

   (assign, "$player_marshal_ai_state", sfai_feast),
   (assign, "$player_marshal_ai_object", "$g_player_court"),

   (assign, "$g_recalculate_ais", 1),
   (assign, reg4, 1),
   (try_begin),
	(neq, "$g_encountered_party", "$g_player_court"),
	(assign, reg4, 0),
   (try_end),
   ]],
[anyone|plyr,"kingdom_lady_captive",
   [],
   "Then write to your family, and ask them to hurry up with the ransom!", "close_window",[
 ]],
[anyone|plyr,"kingdom_lady_captive",
   [],
   "I have changed my mind -- you are free to go", "close_window",[
    ##diplomacy start+
    #(troop_set_slot, "$g_talk_troop", slot_troop_prisoner_of_party, -1),
	#(troop_set_slot, "$g_talk_troop", slot_troop_met, 1),

	##Ensure the freeing works properly.
	(try_begin),
		#Add this for dual-use situations, such as if the lady is a prisoner of the party
		(party_count_prisoners_of_type, ":holding_as_prisoner",  "p_main_party", "$g_talk_troop"),
		(gt, ":holding_as_prisoner", 0),
		(party_remove_prisoners, "p_main_party", "$g_talk_troop", 1),
	(else_try),
		(party_count_prisoners_of_type, ":holding_as_prisoner",  "$g_encountered_party", "$g_talk_troop"),
		(gt, ":holding_as_prisoner", 0),
		(party_remove_prisoners, "$g_encountered_party", "$g_talk_troop", 1),
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
	##diplomacy end+
	]],
[anyone|plyr,"rescue_prisoner_succeed_1", [], "Always an honour to serve, {s65}.", "lady_pretalk",[]],
[anyone,"convince_begin", [], "I still don't see why I should accept what you're asking of me.", "convince_options",
   [(quest_get_slot, "$convince_value", "$g_convince_quest", slot_quest_convince_value),
    ]],
[anyone|plyr,"convince_options", [(assign, reg8, "$convince_value")], "Then I'll make it worth your while. ({reg8} mon)", "convince_bribe",[]],
[anyone|plyr,"convince_options",
  [(store_div, "$convince_relation_penalty", "$convince_value", 300),
   (val_add, "$convince_relation_penalty", 1),
   (assign, reg9, "$convince_relation_penalty")],
   "Please, do it for the sake of our friendship. (-{reg9} to relation)", "convince_friendship",[]],
[anyone|plyr,"convince_options", [], "Let me try and convince you. (Persuasion)", "convince_persuade_begin", []],
[anyone|plyr,"convince_options", [], "Never mind.", "lord_pretalk",[]],
[anyone,"convince_bribe", [], "Mmm, a generous gift to my coffers would certainly help matters...\
 {reg8} mon should do it. If you agree, then I'll go with your suggestion.", "convince_bribe_verify",[]],
[anyone|plyr,"convince_bribe_verify", [(store_troop_gold, ":gold", "trp_player"),
                                         (lt, ":gold", "$convince_value")],
   "I'm afraid my finances will not allow for such a gift.", "convince_bribe_cant_afford",[]],
[anyone|plyr,"convince_bribe_verify", [(store_troop_gold, ":gold", "trp_player"),
                                         (ge, ":gold", "$convince_value")],
  "Very well, please accept these {reg8} mon as a token of my gratitude.", "convince_bribe_goon",[]],
[anyone|plyr,"convince_bribe_verify", [], "Let me think about this some more.", "convince_begin",[]],
[anyone,"convince_bribe_cant_afford", [], "Ah. In that case, there is little I can do,\
 unless you have some further argument to make.", "convince_options",[]],
[anyone,"convince_bribe_goon", [], "My dear {playername}, your generous gift has led me to reconsider what you ask,\
 and I have come to appreciate the wisdom of your proposal.", "convince_accept",[
 ##diplomacy start+ add removed gold to bribed lord
 (call_script, "script_dplmc_distribute_gold_to_lord_and_holdings", "$convince_value", "$g_talk_troop"),
 ##diplomacy end+
 (troop_remove_gold, "trp_player","$convince_value")]],
[anyone,"convince_friendship",
   [(store_add, ":min_relation", 5, "$convince_relation_penalty"),
    (ge, "$g_talk_troop_effective_relation", ":min_relation")], "You've done well by me in the past, {playername},\
 and for that I will go along with your request, but know that I do not like you using our relationship this way.", "convince_friendship_verify",[]],
[anyone|plyr,"convince_friendship_verify", [], "I am sorry, my friend, but I need your help in this.", "convince_friendship_go_on",[]],
[anyone|plyr,"convince_friendship_verify", [], "If it will not please you, then I'll try something else.", "lord_pretalk",[]],
[anyone,"convince_friendship_go_on", [], "All right then, {playername}, I will accept this for your sake. But remember, you owe me for this.", "convince_accept",
   [(store_sub, ":relation_change", 0, "$convince_relation_penalty"),
    (call_script, "script_change_player_relation_with_troop","$g_talk_troop",":relation_change")]],
[anyone,"convince_friendship",
   [(ge, "$g_talk_troop_relation", -5)], "I don't think I owe you such a favor {playername}.\
 I see no reason to accept this for you.", "lord_pretalk",[]],
[anyone,"convince_friendship", [], "Is this a joke? You've some nerve asking me for favours, {playername},\
 and let me assure you you'll get none.", "lord_pretalk",[]],
[anyone,"convince_persuade_begin",
  [(troop_get_slot, ":last_persuasion_time", "$g_talk_troop", slot_troop_last_persuasion_time),
   (store_current_hours, ":cur_hours"),
   (store_add, ":valid_time", ":last_persuasion_time", 24),
   (gt, ":cur_hours", ":valid_time"),
   ],
   "Very well. Make your case.", "convince_persuade_begin_2",[]],
[anyone|plyr,"convince_persuade_begin_2", [], "[Attempt to persuade]", "convince_persuade",[
        (try_begin),
          (store_random_in_range, ":rand", 0, 100),
          (lt, ":rand", 30),
          (store_current_hours, ":cur_hours"),
          (troop_set_slot, "$g_talk_troop", slot_troop_last_persuasion_time, ":cur_hours"),
        (try_end),
        (store_skill_level, ":persuasion_level", "skl_persuasion", "trp_player"),
        (store_add, ":persuasion_potential", ":persuasion_level", 5),

        (store_random_in_range, ":random_1", 0, ":persuasion_potential"),
        (store_random_in_range, ":random_2", 0, ":persuasion_potential"),
        (store_add, ":rand", ":random_1", ":random_2"),

        (assign, ":persuasion_difficulty", "$convince_value"),
        (convert_to_fixed_point, ":persuasion_difficulty"),
        (store_sqrt, ":persuasion_difficulty", ":persuasion_difficulty"),
        (convert_from_fixed_point, ":persuasion_difficulty"),
        (val_div, ":persuasion_difficulty", 10),
        (val_add, ":persuasion_difficulty", 4),

        (store_sub, "$persuasion_strength", ":rand", ":persuasion_difficulty"),
        (val_mul, "$persuasion_strength", 20),
        (assign, reg5, "$persuasion_strength"),
        (val_sub, "$convince_value", "$persuasion_strength"),
        (quest_set_slot, "$g_convince_quest", slot_quest_convince_value, "$convince_value"),
        (str_store_troop_name, s50, "$g_talk_troop"),
		##diplomacy start+
		##OLD:
        #(troop_get_type, reg51, "$g_talk_troop"),
		##NEW:
		(try_begin),
			(call_script, "script_cf_dplmc_troop_is_female", "$g_talk_troop"),
			(assign, reg51, 1),
			(assign, reg65, 1),
		(else_try),
			(assign, reg51, 0),
			(assign, reg65, 0),
		(try_end),
		##diplomacy end+
        (try_begin),
          (lt, "$persuasion_strength", -30),
          (str_store_string, s5, "str_persuasion_summary_very_bad"),
        (else_try),
          (lt, "$persuasion_strength", -10),
          (str_store_string, s5, "str_persuasion_summary_bad"),
        (else_try),
          (lt, "$persuasion_strength", 10),
          (str_store_string, s5, "str_persuasion_summary_average"),
        (else_try),
          (lt, "$persuasion_strength", 30),
          (str_store_string, s5, "str_persuasion_summary_good"),
        (else_try),
          (str_store_string, s5, "str_persuasion_summary_very_good"),
        (try_end),
        (dialog_box, "@{s5} (Persuasion strength: {reg5})", "@Persuasion Attempt"),
  ]],
[anyone|plyr,"convince_persuade_begin_2", [], "Wait, perhaps there is another way to convince you.", "convince_begin",[]],
[anyone,"convince_persuade_begin", [], "By God's grace, {playername}!\
 Haven't we talked enough already? I am tired of listening to you,\
 and I do not want to hear any more of it right now.", "lord_pretalk",[]],
[anyone,"convince_persuade", [(le, "$convince_value", 0)], "All right, all right. You have persuaded me to it.\
 I'll go ahead with what you suggest.", "convince_accept",[]],
[anyone,"convince_persuade", [(gt, "$persuasion_strength", 5)], "You've a point, {playername},\
 I'll admit that much. However I am not yet convinced I should do as you bid.", "convince_options",[]],
[anyone,"convince_persuade", [(gt, "$persuasion_strength", -5)], "Enough, {playername}.\
 You've a lot of arguments, but I find none of them truly convincing. I stand by what I said before.", "convince_options",[]],
[anyone,"convince_persuade", [], "Truthfully, {playername}, I fail to see the virtue of your reasoning.\
 What you ask for makes even less sense now than it did before.", "convince_options",[]],
[anyone|plyr,"seneschal_intro_1", [],  "A pleasure to meet you, {s65}.", "seneschal_intro_1a",[]],
[anyone,"seneschal_intro_1a", [], "How can I help you?", "seneschal_talk",[]],
[anyone|plyr,"seneschal_intro_1", [],  "What exactly do you do here?", "seneschal_intro_1b",[]],
[anyone,"seneschal_intro_1b", [], "Ah, a seneschal's duties are many, good {sire/woman}.\
 For example, I collect the rents from my lord's estates, I manage the castle's storerooms,\
 I deal with the local peasantry, I take care of castle staff, I arrange supplies for the garrison...\
 All mundane matters on this fief are my responsibility, on behalf of my lord.\
 Everything except commanding the soldiers themselves.", "seneschal_talk",[]],
[anyone,"seneschal_pretalk", [], "Anything else?", "seneschal_talk",[]],
[anyone|plyr,"seneschal_talk", [(store_relation, ":cur_rel", "fac_player_supporters_faction", "$g_encountered_party_faction"),
                                  (ge, ":cur_rel", 0),],
   "I would like to ask you a question...", "seneschal_ask_something",[]],
[anyone|plyr,"seneschal_talk", [(store_relation, ":cur_rel", "fac_player_supporters_faction", "$g_encountered_party_faction"),
                                  (ge, ":cur_rel", 0),],
   "I wish to know more about someone...", "seneschal_ask_about_someone",[]],
[anyone,"seneschal_ask_about_someone", [],
   "Perhaps I may be able to help. Whom did you have in mind?", "seneschal_ask_about_someone_2",[]],
[anyone|plyr,"seneschal_ask_about_someone_2", [], "Never mind.", "seneschal_pretalk",[]],
[anyone|plyr,"seneschal_talk", [], "I must take my leave of you now. Farewell.", "close_window",[]],
[anyone,"seneschal_ask_something", [],
   "I'll do what I can to help, of course. What did you wish to ask?", "seneschal_ask_something_2",[]],
[anyone|plyr,"seneschal_ask_something_2", [],
   "Perhaps you know where to find someone...", "seneschal_ask_location",[]],
[anyone,"seneschal_ask_location", [],
   "Well, a man in my position does hear a lot of things. Of whom were you thinking?", "seneschal_ask_location_2",[]],
[anyone|plyr|repeat_for_troops,"seneschal_ask_location_2", [(store_repeat_object, ":troop_no"),
                                                              (is_between, ":troop_no", heroes_begin, heroes_end),
                                                              (store_troop_faction, ":faction_no", ":troop_no"),
                                                              (eq, "$g_encountered_party_faction", ":faction_no"),
                                                              (str_store_troop_name, s1, ":troop_no")],
   "{s1}", "seneschal_ask_location_3",[(store_repeat_object, "$hero_requested_to_learn_location")]],
[anyone|plyr,"seneschal_ask_location_2", [], "Never mind.", "seneschal_pretalk",[]],
[anyone,"seneschal_ask_location_3", [(call_script, "script_get_information_about_troops_position", "$hero_requested_to_learn_location", 0)],
   "{s1}", "seneschal_pretalk",[]],
[anyone|plyr,"talk_caravan_escort", [],
   "There might be bandits nearby. Stay close.", "talk_caravan_escort_2a",[]],
[anyone,"talk_caravan_escort_2a", [],
   "Trust me, {playername}, we're already staying as close to you as we can. Lead the way.", "close_window",[(assign, "$g_leave_encounter",1)]],
[anyone|plyr,"talk_caravan_escort", [],
   "No sign of trouble, we can breathe easy.", "talk_caravan_escort_2b",[]],
[anyone,"talk_caravan_escort_2b", [],
   "I'll breathe easy when we reach {s1} and not a moment sooner. Let's keep moving.", "close_window",[[str_store_party_name,s1,"$caravan_escort_destination_town"],(assign, "$g_leave_encounter",1)]],
[anyone,"caravan_start_war_quest_1", [(quest_get_slot, ":giver_troop", "qst_cause_provocation", slot_quest_giver_troop),
								 (store_faction_of_troop, ":giver_troop_faction", ":giver_troop"),
                                 (str_store_faction_name, s17, ":giver_troop_faction"),
  ],
   "What? What nonsense is this? We are at peace with the {s17}, and are free to cross its lands!", "caravan_start_war_quest_2",[]],
[anyone|plyr,"caravan_start_war_quest_2", [], "We'll see about that! Defend yourselves!", "merchant_attack",[]],
[anyone|plyr,"caravan_start_war_quest_2", [], "Hmm. Maybe this was all a misunderstanding. Farewell.", "close_window",[(assign, "$g_leave_encounter",1)]],
[anyone,"caravan_offer_protection", [],
   "These roads are dangerous indeed. One can never have enough protection.", "caravan_offer_protection_2",
   [(get_party_ai_object,":caravan_destination","$g_encountered_party"),
    (store_distance_to_party_from_party, "$caravan_distance_to_target",":caravan_destination","$g_encountered_party"),
    (assign,"$caravan_escort_offer","$caravan_distance_to_target"),
    (val_sub, "$caravan_escort_offer", 10),
    (call_script, "script_party_calculate_strength", "p_main_party", 0),
    (assign, ":player_strength", reg0),
    (val_min, ":player_strength", 200),
    (val_add, ":player_strength", 20),
    (val_mul,"$caravan_escort_offer",":player_strength"),
    (val_div,"$caravan_escort_offer",50),
    (val_max, "$caravan_escort_offer", 5),
    ]],
[anyone,"caravan_offer_protection_2", [[lt,"$caravan_distance_to_target",10]],
   "An escort? We're almost there already! Thank you for the offer, though.", "close_window",[(assign, "$g_leave_encounter",1)]],
[anyone,"caravan_offer_protection_2", [(get_party_ai_object,":caravan_destination","$g_encountered_party"),
    (str_store_party_name,1,":caravan_destination"),
    (assign,reg(2),"$caravan_escort_offer")],
   "We are heading to {s1}. I will pay you {reg2} mon if you escort us there.", "caravan_offer_protection_3",
   []],
[anyone|plyr,"caravan_offer_protection_3", [],
   "Agreed.", "caravan_offer_protection_4",[]],
[anyone,"caravan_offer_protection_4", [],
   "I want you to stay close to us along the way.\
 We'll need your help if we get ambushed by bandits.", "caravan_offer_protection_5",[]],
[anyone|plyr,"caravan_offer_protection_5", [],
   "Don't worry, you can trust me.", "caravan_offer_protection_6",[]],
[anyone,"caravan_offer_protection_6", [(get_party_ai_object,":caravan_destination","$g_encountered_party"),
    (str_store_party_name,1,":caravan_destination")],
   "Good. Come and collect your money when we're within sight of {s1}. For now, let's just get underway.", "close_window",
   [(get_party_ai_object,":caravan_destination","$g_encountered_party"),
    (assign, "$caravan_escort_destination_town", ":caravan_destination"),
    (assign, "$caravan_escort_party_id", "$g_encountered_party"),
    (assign, "$caravan_escort_agreed_reward", "$caravan_escort_offer"),
    (assign, "$caravan_escort_state", 1),
    (assign, "$g_leave_encounter",1)
   ]],
[anyone|plyr,"caravan_offer_protection_3", [],
   "Forget it.", "caravan_offer_protection_4b",[]],
[anyone,"caravan_offer_protection_4b", [],
   "Perhaps another time, then.", "close_window",[(assign, "$g_leave_encounter",1)]],
[anyone,"talk_caravan_enemy_2", [],
   "Never. It is our duty to protect these goods. You shall have to fight us, brigand!", "close_window",
   [
    (store_relation,":rel","$g_encountered_party_faction","fac_player_supporters_faction"),
    (val_min,":rel",0),
    (val_sub,":rel",4),
    (call_script, "script_set_player_relation_with_faction", "$g_encountered_party_faction", ":rel"),
	(call_script, "script_diplomacy_party_attacks_neutral", "p_main_party", "$g_encountered_party"),
    ]],
[anyone|plyr,"prison_guard_players", [],
   "Yes. Unlock the door.", "close_window",[(call_script, "script_enter_dungeon", "$current_town", "mt_visit_town_castle")]],
[anyone|plyr,"prison_guard_players", [],
   "No, not now.", "close_window",[]],
[anyone|plyr,"prison_guard_talk", [],
   "Who is imprisoned here?", "prison_guard_ask_prisoners",[]],
[anyone|plyr,"prison_guard_talk", [],
   "I want to speak with a prisoner.", "prison_guard_visit_prison",[]],
[anyone|plyr,"prison_guard_talk", [
    (party_slot_eq, "$g_encountered_party", slot_town_lord, "trp_player"),
    ],
   "I want to release a prisoner.", "dplmc_prison_guard_talk_ask_prisoner",[]],
[anyone,"prison_guard_ask_prisoners", [],
   "Currently, {s50} {reg1?are:is} imprisoned here.{s49}","prison_guard_talk",[
    (party_clear, "p_temp_party"),
	(party_clear, "p_temp_party_2"),
    (assign, ":num_heroes_in_dungeon", 0),
    (assign, ":num_heroes_given_parole", 0),

    (party_get_num_prisoner_stacks, ":num_stacks","$g_encountered_party"),
    (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_prisoner_stack_get_troop_id, ":stack_troop","$g_encountered_party",":i_stack"),
        (troop_is_hero, ":stack_troop"),
		(try_begin),
			(call_script, "script_cf_prisoner_offered_parole", ":stack_troop"),
			(party_add_members, "p_temp_party_2", ":stack_troop", 1),
			(val_add, ":num_heroes_given_parole", 1),
		(else_try),
			(party_add_members, "p_temp_party", ":stack_troop", 1),
			(val_add, ":num_heroes_in_dungeon", 1),
		(try_end),
    (try_end),
    (call_script, "script_print_party_members", "p_temp_party"),
	(str_store_string, s50, "str_s51"),
    (try_begin),
        (gt, ":num_heroes_in_dungeon", 1),
        (assign, reg1, 1),
    (else_try),
        (assign, reg1, 0),
    (try_end),

	(str_clear, s49),
    (try_begin),
        (ge, ":num_heroes_given_parole", 1),
		(call_script, "script_print_party_members", "p_temp_party_2"),
		(try_begin),
			(ge, ":num_heroes_given_parole", 2),
			(assign, reg2, 1),
		(else_try),
			(assign, reg2, 0),
		(try_end),
		(str_store_string, s49, "str__meanwhile_s51_reg2areis_being_held_in_the_castle_but_reg2havehas_made_pledges_not_to_escape_and_reg2areis_being_held_in_more_comfortable_quarters" ), #somewhat awkward wording prevents both gender and singular/plural pronoun issues
    (try_end)


	]],
[anyone,"prison_guard_visit_prison",
  [
    (this_or_next|faction_slot_eq, "$g_encountered_party_faction", slot_faction_marshall, "trp_player"),
    (this_or_next|party_slot_eq, "$g_encountered_party", slot_town_lord, "trp_player"),
    (eq, "$g_encountered_party_faction", "$players_kingdom"),
  ],
   "Of course, {sir/madam}. Go in.", "close_window",
   [
     (call_script, "script_enter_dungeon", "$current_town", "mt_visit_town_castle")
   ]],
[anyone, "prison_guard_visit_prison",
  [
    #below condition is added by ozan, please lets discuss if it is needed or not. But I think this condition is needed because if there is nobody in prison
    #prison guard should not say you need to get permission, or take me money ext to let player go inside.
    (assign, ":num_heroes_in_dungeon", 0),
    (party_get_num_prisoner_stacks, ":num_stacks", "$g_encountered_party"),
    (assign, ":end_condition", ":num_stacks"),
    (try_for_range, ":i_stack", 0, ":end_condition"),
      (party_prisoner_stack_get_troop_id, ":stack_troop","$g_encountered_party",":i_stack"),
      (troop_is_hero, ":stack_troop"),
      (try_begin),
        (call_script, "script_cf_prisoner_offered_parole", ":stack_troop"),
      (else_try),
        (val_add, ":num_heroes_in_dungeon", 1),
        (assign, ":end_condition", 0),
      (try_end),
    (try_end),

    (ge, ":num_heroes_in_dungeon", 1),
   ],
   "You need to get permission from the lord to talk to prisoners.", "prison_guard_visit_prison_2",[]],
[anyone, "prison_guard_visit_prison", [], "There is nobody inside, therefore you can freely go inside and look around.", "prison_guard_visit_prison_nobody", []],
[anyone|plyr,"prison_guard_visit_prison_nobody", [], "All right then. I'll take a look at the prison.", "close_window",
  [
    (call_script, "script_enter_dungeon", "$current_town", "mt_visit_town_castle"),
  ]],
[anyone|plyr,"prison_guard_visit_prison_nobody", [], "I have more important business to do.", "close_window",[]],
[anyone|plyr,"prison_guard_visit_prison_2", [], "All right then. I'll try that.", "close_window",[]],
[anyone|plyr,"prison_guard_visit_prison_2", [], "Come on now. I thought you were the boss here.", "prison_guard_visit_prison_3",[]],
[anyone,"prison_guard_visit_prison_3", [], "He-heh. You got that right. Still, I can't let you into the prison.", "prison_guard_visit_prison_4",[]],
[anyone|plyr,"prison_guard_visit_prison_4", [], "All right then. I'll leave now.", "close_window",[]],
[anyone|plyr,"prison_guard_visit_prison_4", [(store_troop_gold,":gold","trp_player"),(ge,":gold",100)],
   "I found a purse with 100 mon a few paces away. I reckon it belongs to you.", "prison_guard_visit_prison_5",[]],
[anyone,"prison_guard_visit_prison_5", [], "Ah! I was looking for this all day. How good of you to bring it back {sir/madam}.\
 Well, now that I know what an honest {man/lady} you are, there can be no harm in letting you inside for a look. Go in.... Just so you know, though -- I'll be hanging onto the keys, in case you were thinking about undoing anyone's chains.", "close_window",
 [(troop_remove_gold, "trp_player",100),(call_script, "script_enter_dungeon", "$current_town", "mt_visit_town_castle")]],
[anyone|plyr,"prison_guard_visit_prison_4", [],
   "Give me the keys to the cells -- now!", "prison_guard_visit_break",[
   ]],
[anyone,"prison_guard_visit_break", [], "Help! Help! Prison break!", "close_window",[
  (call_script, "script_activate_town_guard"),
  (assign, "$g_main_attacker_agent", "$g_talk_agent"),
  (assign, "$talk_context", tc_prison_break),
#  (try_begin),
#		(store_relation, ":relation", "fac_player_faction", "$g_encountered_party_faction"),
#	Reduce relation with town
# (try_end),

	 (assign, ":end_cond", kingdom_ladies_end),
     (try_for_range, ":prisoner", active_npcs_begin, ":end_cond"),
	   (troop_set_slot, ":prisoner", slot_troop_mission_participation, 0), #new
	 (try_end),
  ]],
[anyone|plyr,"prison_guard_talk", [],
   "Never mind.", "close_window",[]],
[anyone,"request_meeting_castle_lord", [(party_get_slot, ":castle_lord", "$g_encountered_party", slot_town_lord),
                                         (call_script, "script_get_troop_attached_party", ":castle_lord"),
                                         (eq, "$g_encountered_party", reg0),
                                         (str_store_troop_name, s2, ":castle_lord"),
                                         (assign, "$lord_requested_to_talk_to", ":castle_lord"),
                                          ],  "Wait here. {s2} will see you.", "close_window",[]],
[anyone,"request_meeting_castle_lord", [],  "My lord is not here now.", "castle_gate_guard_pretalk",[]],
[anyone,"request_meeting_other", [],  "Who is that?", "request_meeting_3",[]],
[anyone|plyr|repeat_for_troops,"request_meeting_3", [(store_repeat_object, ":troop_no"),
                                                       (troop_is_hero, ":troop_no"),
                                                       (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
                                                       (call_script, "script_get_troop_attached_party", ":troop_no"),
                                                       (eq, "$g_encountered_party", reg0),
                                                       (str_store_troop_name, s3, ":troop_no"),
                                                       ],
   "{s3}", "request_meeting_4",[(store_repeat_object, "$lord_requested_to_talk_to")]],
[anyone|plyr,"request_meeting_3", [], "Never mind.", "close_window",[(assign, "$lord_requested_to_talk_to", 0)]],
[anyone,"request_meeting_4", [##diplomacy start+ correct pronoun
  (call_script, "script_dplmc_store_troop_is_female",  "$lord_requested_to_talk_to"),
], "Wait there. I'll send {reg0?her:him} your request.", "request_meeting_5",[]],
[anyone|plyr,"request_meeting_5", [], "I'm waiting...", "request_meeting_6",[]],
[anyone,"request_meeting_6",
   [
     (call_script, "script_troop_get_player_relation", "$lord_requested_to_talk_to"),
     (assign, ":lord_relation", reg0),
     (gt, ":lord_relation", -20),
    ], "All right. {s2} will talk to you now.", "close_window",[(str_store_troop_name, s2, "$lord_requested_to_talk_to")]],
[anyone,"request_meeting_6", [(str_store_troop_name, s2, "$lord_requested_to_talk_to"),
  ##diplomacy start+ correct pronoun
  (call_script, "script_dplmc_store_troop_is_female",  "$lord_requested_to_talk_to"),
  ], "{s2} says {reg0?she:he} will not see you. Begone now.", "close_window",[]],
[anyone|plyr,"ally_thanks_meet", [], "My name is {playername}.", "ally_thanks_meet_2", []],
[anyone, "ally_thanks_meet_2", [(ge, "$g_talk_troop_relation", 15),(str_store_troop_name, s1, "$g_talk_troop")],
   "Well met indeed {playername}. My name is {s1} and I am forever in your debt. If there is ever anything I can help you with, just let me know...", "close_window", []],
[anyone, "ally_thanks_meet_2", [(ge, "$g_talk_troop_relation", 5),], "Well met {playername}. I am in your debt for what you just did. I hope one day I will find a way to repay it.", "close_window", []],
[anyone, "ally_thanks_meet_2", [], "Well met {playername}. I am {s1}. Thanks for your help and I hope we meet again.", "close_window", []],
[anyone|plyr,"freed_hero_answer", [],
   "You're not going anywhere. You'll be my prisoner now!", "freed_hero_answer_1",
   [
     (store_conversation_troop, ":cur_troop_id"),
     (party_add_prisoners, "p_main_party", ":cur_troop_id", 1),#take prisoner
    ]],
[anyone,"freed_hero_answer_1", [],
   "Alas. Will my luck never change?", "close_window",
   []],
[anyone|plyr,"freed_hero_answer", [],
   "You're free to go, {s65}.", "freed_hero_answer_2",
   [
    ]],
[anyone,"freed_hero_answer_2", [],
   "Thank you. I never forget someone who's done me a good turn.", "close_window",
   []],
[anyone|plyr,"freed_hero_answer", [],
   "Would you like to join me?", "freed_hero_answer_3",
   []],
[anyone,"freed_hero_answer_3", [(store_random_in_range, ":random_no",0,2),(eq, ":random_no", 0)],
   "All right I will join you.", "close_window",
   [
     (store_conversation_troop, ":cur_troop_id"),
     (party_add_members, "p_main_party", ":cur_troop_id", 1),#join hero
   ]],
[anyone,"freed_hero_answer_3", [],
   "No, I want to go on my own.", "close_window",
   [
    ]],
[anyone|plyr,"defeat_hero_answer", [],
   "You are my prisoner now.", "defeat_hero_answer_1",
   [
     (party_add_prisoners, "p_main_party", "$g_talk_troop", 1),#take prisoner
     #(troop_set_slot, "$g_talk_troop", slot_troop_is_prisoner, 1),
     (troop_set_slot, "$g_talk_troop", slot_troop_prisoner_of_party, "p_main_party"),
     (call_script, "script_event_hero_taken_prisoner_by_player", "$g_talk_troop"),
    ]],
[anyone,"defeat_hero_answer_1", [],
   "Damn you. You will regret this.", "close_window",
   []],
[anyone|plyr,"defeat_hero_answer", [],
   "You're free to go this time, but don't cross my path again.", "defeat_hero_answer_2",
   []],
[anyone,"defeat_hero_answer_2", [],
   "We will meet again.", "close_window",
   []],
[anyone,"combined_political_quests", [
  (eq, "$political_quest_found", "qst_resolve_dispute"),
	],
   "{s9}", "political_quest_suggested",
   [
   (quest_set_slot, "qst_resolve_dispute", slot_quest_target_troop, "$political_quest_target_troop"),
   (quest_set_slot, "qst_resolve_dispute", slot_quest_object_troop, "$political_quest_object_troop"),

   (quest_get_slot, ":target_troop", "qst_resolve_dispute", slot_quest_target_troop),
   (quest_get_slot, ":object_troop", "qst_resolve_dispute", slot_quest_object_troop),
   (str_store_troop_name, s4, ":target_troop"),
   (str_store_troop_name, s5, ":object_troop"),
   (faction_get_slot, ":faction_leader", "$players_kingdom", slot_faction_leader),
   (str_store_troop_name, s7, ":faction_leader"),
   (try_begin),
      (eq, "$players_kingdom", "fac_player_supporters_faction"),
	  (faction_slot_eq, "fac_player_supporters_faction", slot_faction_leader, "trp_player"),
	  (str_store_string, s9, "str_you_may_be_aware_my_lord_of_the_quarrel_between_s4_and_s5_which_is_damaging_the_unity_of_this_realm_and_sapping_your_authority_if_you_could_persuade_the_lords_to_reconcile_it_would_boost_your_own_standing_however_in_taking_this_on_you_run_the_risk_of_one_the_lords_deciding_that_you_have_taken_the_rivals_side"),
   (else_try),
	  (str_store_string, s9, "str_you_may_be_aware_my_lord_of_the_quarrel_between_s4_and_s5_which_is_damaging_the_unity_of_this_realm_and_sapping_your_authority_if_you_could_persuade_the_lords_to_reconcile_i_imagine_that_s7_would_be_most_pleased_however_in_taking_this_on_you_run_the_risk_of_one_the_lords_deciding_that_you_have_taken_the_rivals_side"),
   (try_end),
   ]],
[anyone,"political_quest_follow_on", [
  (eq, "$political_quest_found", "qst_resolve_dispute"),
	],
   "I think that is a wise move. Good luck to you.", "close_window",
   [
    (assign, "$g_leave_encounter", 1),
    (setup_quest_text,"qst_resolve_dispute"),

	(quest_get_slot, ":lord_1", "qst_resolve_dispute", slot_quest_target_troop),
	(str_store_troop_name_link, s11, ":lord_1"),

	(quest_get_slot, ":lord_2", "qst_resolve_dispute", slot_quest_object_troop),
	(str_store_troop_name_link, s12, ":lord_2"),

	(str_store_string, s2, "str_resolve_the_dispute_between_s11_and_s12"),
	(call_script, "script_start_quest", "qst_resolve_dispute", -1),
	(quest_set_slot, "qst_resolve_dispute", slot_quest_expiration_days, 30),
	(quest_set_slot, "qst_resolve_dispute", slot_quest_giver_troop, "$g_talk_troop"),
	(quest_set_slot, "qst_resolve_dispute", slot_quest_target_state, 0),
	(quest_set_slot, "qst_resolve_dispute", slot_quest_object_state, 0),

	(quest_get_slot, ":lord_1", "qst_resolve_dispute", slot_quest_target_troop), #this block just to check if the slots work
	(str_store_troop_name, s11, ":lord_1"),
	(quest_get_slot, ":lord_2", "qst_resolve_dispute", slot_quest_object_troop),
	(str_store_troop_name, s12, ":lord_2"),
	],
   ],
[anyone,"combined_political_quests", [

  (eq, "$political_quest_found", "qst_offer_gift"),
  (quest_set_slot, "qst_offer_gift", slot_quest_target_troop, "$political_quest_target_troop"),
  #gekokujo 3.0 integrating 1.158 change start
  (quest_set_slot, "qst_offer_gift", slot_quest_giver_troop, "$g_talk_troop"),
  #gekokujo 3.0 integrating 1.158 change end

  (quest_get_slot, ":target_troop", "qst_offer_gift", slot_quest_target_troop),
  (str_store_troop_name, s4, ":target_troop"),
  (troop_get_type, reg4, ":target_troop"),
  (call_script, "script_troop_get_family_relation_to_troop", ":target_troop", "$g_talk_troop"),

	],
   "Your relations with {s4} are not all that they could be. As {reg4?she:he} is my {s11}, I can mediate to attempt to mend your quarrel. Perhaps the best way for me to do this would be to send {reg4?her:him} a gift -- a fur-trimmed velvet robe, perhaps. If you can provide me with a bolt of velvet and a length of furs, I can have one made and sent to {reg4?her:him.}", "political_quest_suggested",
   [
   (quest_get_slot, ":target_troop", "qst_offer_gift", slot_quest_target_troop),
   (troop_get_type, reg4, ":target_troop"),
   ]],
[anyone,"political_quest_follow_on", [
  (eq, "$political_quest_found", "qst_offer_gift"),
  ],
   "Splendid. I shall await the materials.", "close_window",
   [
   (assign, "$g_leave_encounter", 1),
    (setup_quest_text,"qst_offer_gift"),

	(quest_get_slot, ":lord_1", "qst_offer_gift", slot_quest_target_troop),
	(str_store_troop_name, s14, ":lord_1"),
	(str_store_troop_name, s12, "$g_talk_troop"),
	##diplomacy start+
	#(troop_get_type, reg4, "$g_talk_troop"),
	(assign, reg4, reg65),
	##diplomacy end+

	(str_store_string, s2, "str_you_intend_to_bring_gift_for_s14"),

   (call_script, "script_start_quest", "qst_offer_gift", "$g_talk_troop"),
   (quest_set_slot, "qst_offer_gift", slot_quest_expiration_days, 30),
   ]],
[anyone,"combined_political_quests", [
   (eq, "$political_quest_found", "qst_denounce_lord"),
   (this_or_next|eq, "$g_talk_troop", "$g_player_minister"),
		(troop_slot_eq, "trp_player", slot_troop_spouse, "$g_talk_troop"),

   (str_store_troop_name, s4, "$political_quest_target_troop"),
   ##diplomacy start+ use script for gender
   #(troop_get_type, reg4, "$political_quest_target_troop"),
   (call_script, "script_dplmc_store_troop_is_female_reg", "$political_quest_target_troop", 4),
   ##diplomacy end+
   (str_store_faction_name, s5, "$players_kingdom"),

   (troop_get_slot, ":reputation_string", "$political_quest_target_troop", slot_lord_reputation_type),
   (val_add, ":reputation_string", "str_lord_derogatory_default"),
   (str_store_string, s7, ":reputation_string"),

   (troop_get_slot, ":reputation_string", "$political_quest_target_troop", slot_lord_reputation_type),
   (val_add, ":reputation_string", "str_lord_derogatory_result"),
   (str_store_string, s8, ":reputation_string"),

	],
   "As you may realize, {s4} has many enemies among the lords of the {s5}. In particular, they feel that {reg4?she:he} is {s7}, and worry that {reg4?she:he} will {s8}. Were you to denounce {s4} to {reg4?her:his} face, you may reap much popularity -- although, of course, you would make an enemy of {reg4?her:him}, and risk being challenged to a duel.", "political_quest_suggested",
   [
   ]],
[anyone,"combined_political_quests", [
    (eq, "$political_quest_found", "qst_denounce_lord"),
    ##diplomacy start+ use script for gender
    #(troop_get_type, reg4, "$political_quest_target_troop"),
    (call_script, "script_dplmc_store_troop_is_female_reg", "$political_quest_target_troop", 4),
    ##diplomacy end+

	(str_clear, s9),
	(call_script, "script_troop_get_relation_with_troop", "trp_player", "$g_talk_troop"),
	(assign, ":player_relation_with_target", reg0),

    (str_store_troop_name, s4, "$political_quest_target_troop"),
	(try_begin),
		(ge, ":player_relation_with_target", 2),
		(neg|troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_debauched),
		(neg|troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_quarrelsome),
		(str_store_string, s9, "str_i_realize_that_you_are_on_good_terms_with_s4_but_we_ask_you_to_do_this_for_the_good_of_the_realm"),
	(else_try),
		(ge, ":player_relation_with_target", 2),
		(str_store_string, s9, "str_i_realize_that_you_are_on_good_terms_with_s4_but_the_blow_will_hurt_him_more"),
	(try_end),

    (str_store_faction_name, s5, "$players_kingdom"),
    (str_store_troop_name, s4, "$political_quest_target_troop"),

    (troop_get_slot, ":reputation_string", "$political_quest_target_troop", slot_lord_reputation_type),
    (val_add, ":reputation_string", "str_lord_derogatory_default"),
    (str_store_string, s7, ":reputation_string"),

    (troop_get_slot, ":reputation_string", "$political_quest_target_troop", slot_lord_reputation_type),
    (val_add, ":reputation_string", "str_lord_derogatory_result"),
    (str_store_string, s8, ":reputation_string"),


	],

    "As you may realize, many of us hereditary vassals of the {s5} consider {s4} to be {s7}, and a liability to our cause. We worry that {reg4?she:he} will {s8}. People know my views on {s4} already, but if you were to denounce {reg4?her:him} to {reg4?her:his} face, you would further erode his standing -- and discourage our great lord from entrusting {reg4?her:him} with any more power or responsibility. Of course, you would make an enemy of {reg4?her:him}, and risk being challenged to a duel.{s9}", "political_quest_suggested",
    [


	]],
[anyone,"political_quest_follow_on", [
	(eq, "$political_quest_found", "qst_denounce_lord"),
	(this_or_next|eq, "$g_talk_troop", "$g_player_minister"),
		(troop_slot_eq, "trp_player", slot_troop_spouse, "$g_talk_troop"),
  ],
   "We appreciate what you are doing. I find such intrigues distasteful, but it is all for the good of the {s5}.", "close_window",
   [
   (quest_set_slot, "qst_denounce_lord", slot_quest_target_troop, "$political_quest_target_troop"),

   (quest_get_slot, ":target_troop", "qst_denounce_lord", slot_quest_target_troop),
   (str_store_troop_name_link, s14, ":target_troop"),
   (str_store_troop_name_link, s12, "$g_talk_troop"),

   (str_store_string, s2, "str_you_intend_to_denounce_s14_to_his_face_on_behalf_of_s14"),
   (setup_quest_text, "qst_denounce_lord"),

   (call_script, "script_start_quest", "$political_quest_found", "$g_talk_troop"),
   (quest_set_slot, "qst_denounce_lord", slot_quest_expiration_days, 60),

   (str_store_faction_name, s5, "$players_kingdom"),
   (assign, "$g_leave_encounter", 1),
   ]],
[anyone,"political_quest_follow_on", [
	(eq, "$political_quest_found", "qst_denounce_lord"),
  ],
   "Very well. It is always risky to involve yourself in intrigues of this sort, but in this case, I think you will benefit.", "close_window",
   [
   (quest_set_slot, "qst_denounce_lord", slot_quest_target_troop, "$political_quest_target_troop"),

   (quest_get_slot, ":target_troop", "qst_denounce_lord", slot_quest_target_troop),
   (str_store_troop_name_link, s14, ":target_troop"),
   (str_store_troop_name_link, s12, "$g_talk_troop"),

   (str_store_string, s2, "str_you_intend_to_denounce_s14_to_his_face_on_behalf_of_s14"),
   (setup_quest_text, "qst_denounce_lord"),

   (call_script, "script_start_quest", "$political_quest_found", "$g_talk_troop"),
   (assign, "$g_leave_encounter", 1),
]],
[anyone,"combined_political_quests", [
    (eq, "$political_quest_found", "qst_intrigue_against_lord"),
    (str_store_troop_name, s4, "$political_quest_target_troop"),
       ##diplomacy start+ use script for gender
   #(troop_get_type, reg4, "$political_quest_target_troop"),
   (call_script, "script_dplmc_store_troop_is_female_reg", "$political_quest_target_troop", 4),
   ##diplomacy end+
    (str_store_faction_name, s5, "$players_kingdom"),
    (troop_get_slot, ":reputation_string", "$political_quest_target_troop", slot_lord_reputation_type),
    (val_add, ":reputation_string", "str_lord_derogatory_default"),
    (str_store_string, s7, ":reputation_string"),

    (troop_get_slot, ":reputation_string_2", "$political_quest_target_troop", slot_lord_reputation_type),
    (val_add, ":reputation_string_2", "str_lord_derogatory_result"),
    (str_store_string, s8, ":reputation_string_2"),

	(faction_get_slot, ":faction_leader", "$players_kingdom", slot_faction_leader),
	(str_store_troop_name, s9, ":faction_leader"),
	],
   "You and I have a common interest in seeking to curtail the rise of {s4}. I feel that {reg4?she:he} is {s7}, and worry that {reg4?she:he} will {s8}. Were you to tell our leader {s9} your opinion of {s4}, it might discourage {s9} from granting {s4} any further powers or responsibilities, at least for a while, and I would be much obliged to you.", "political_quest_suggested",
   []],
[anyone,"political_quest_follow_on", [
	(eq, "$political_quest_found", "qst_intrigue_against_lord"),
#	(this_or_next|eq, "$g_talk_troop", "$g_player_minister"),
#		(troop_slot_eq, "trp_player", slot_troop_spouse, "$g_talk_troop"),
    (str_store_faction_name, s5, "$players_kingdom"),

  ],
   "We appreciate what you are doing. I find such intrigues distasteful, but it is all for the good of the {s5}.", "close_window",
   [
   (quest_set_slot, "qst_intrigue_against_lord", slot_quest_target_troop, "$political_quest_target_troop"),

   (quest_get_slot, ":target_troop", "qst_intrigue_against_lord", slot_quest_target_troop),
   (store_faction_of_troop, ":target_troop_faction", ":target_troop"),
   (faction_get_slot, ":faction_liege", ":target_troop_faction", slot_faction_leader),
   (str_store_troop_name_link, s14, ":target_troop"),
   (str_store_troop_name_link, s13, ":faction_liege"),
   (str_store_troop_name_link, s12, "$g_talk_troop"),

   (str_store_string, s2, "str_you_intend_to_denounce_s14_to_s13_on_behalf_of_s12"),
   (setup_quest_text, "qst_intrigue_against_lord"),

   (call_script, "script_start_quest", "$political_quest_found", "$g_talk_troop"),
   (quest_set_slot, "qst_intrigue_against_lord", slot_quest_expiration_days, 60),
   (assign, "$g_leave_encounter", 1),
   ]],
[anyone,"combined_political_quests", [],
   "I cannot think of anything right now, but we will have some items of mutual interest in the future.", "political_quest_suggested",
   []],
[anyone|plyr,"political_quest_suggested", [
  (gt, "$political_quest_found", 0),
  ],
   "I like that idea.", "political_quest_follow_on",
   [
   ]],
[anyone|plyr,"political_quest_suggested", [
  (gt, "$political_quest_found", 0),
  ],
   "Hmm.. Maybe you can think of something else?", "combined_political_quests",
   [
   (quest_set_slot, "$political_quest_found", slot_quest_dont_give_again_remaining_days, 3),
   (call_script, "script_get_political_quest", "$g_talk_troop"),
   (assign, "$political_quest_found", reg0),
   (assign, "$political_quest_target_troop", reg1),
   (assign, "$political_quest_object_troop", reg2),

   ]],
[anyone|plyr,"political_quest_suggested", [],
   "Let us discuss another topic", "political_quests_end",
   []],
[anyone,"political_quests_end", [
  (troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_hero),
  ],
   "Very well.", "lord_pretalk",
   []],
[anyone,"political_quests_end", [
  (troop_slot_eq, "trp_player", slot_troop_spouse, "$g_talk_troop"),
  ],
   "Very well.", "spouse_pretalk",
   []],
[anyone,"political_quests_end", [
  (eq, "$g_talk_troop", "$g_player_minister"),
  ],
   "Very well.", "minister_pretalk",
   []],
[anyone,"political_quests_end", [
  ],
   "Very well.", "close_window",
   [
   (assign, "$g_leave_encounter", 1),
   ]],
[anyone|plyr,"local_merchant_mercy", [(quest_get_slot, ":quest_giver_troop", "qst_kill_local_merchant", slot_quest_giver_troop),(str_store_troop_name, s2, ":quest_giver_troop"),
  ##diplomacy start+ Initialize reg4 for use below
  (assign, reg4, 0),
  (try_begin),
	(call_script, "script_cf_dplmc_troop_is_female", ":quest_giver_troop"),
	(assign, reg4, 1),
  (try_end),
  ],#next line man to {reg65?woman:man}
   "I have nothing against you {reg65?woman:man}. But {s2} wants you dead. Sorry.", "local_merchant_mercy_no",[]],
[anyone,"local_merchant_mercy_no", [], "Damn you! May you burn in Hell!", "close_window",[]],
[anyone|plyr,"local_merchant_mercy", [], "I'll let you live, if you promise me...", "local_merchant_mercy_yes",[]],
[anyone,"local_merchant_mercy_yes", [], "Of course, I promise, I'll do anything. Just spare my life... ", "local_merchant_mercy_yes_2",[]],
[anyone|plyr,"local_merchant_mercy_yes_2", [], "You are going to forget about {s2}'s debt to you. And you will sign a paper stating that {reg4?she:he} owes you nothing.", "local_merchant_mercy_yes_3",[]],
[anyone,"local_merchant_mercy_yes_3", [], "Yes, of course. I'll do as you say.", "local_merchant_mercy_yes_4",[]],
[anyone|plyr,"local_merchant_mercy_yes_4", [], "And if my lord hears so much of a hint of a complaint about this issue, then I'll come back for you,\
 and it won't matter how much you scream for mercy then.\
 Do you understand me?", "local_merchant_mercy_yes_5",[]],
[anyone,"local_merchant_mercy_yes_5", [], "Yes {sir/madam}. Don't worry. I won't make any complaint.", "local_merchant_mercy_yes_6",[]],
[anyone|plyr,"local_merchant_mercy_yes_6", [], "Good. Go now, before I change my mind.", "close_window",
   [(quest_set_slot, "qst_kill_local_merchant", slot_quest_current_state, 2),
    (call_script, "script_succeed_quest", "qst_kill_local_merchant"),
    (finish_mission),
    ]],
[trp_fugitive|plyr,"fugitive_1", [
     (quest_get_slot, ":quest_target_dna", "qst_hunt_down_fugitive", slot_quest_target_dna),
     (call_script, "script_get_name_from_dna_to_s50", ":quest_target_dna"),
     (str_store_string, s4, s50),
      ], "I am looking for a murderer by the name of {s4}. You fit his description.", "fugitive_2",[]],
[trp_fugitive|plyr,"fugitive_1", [], "Nothing. Sorry to trouble you.", "close_window",[]],
[trp_fugitive,"fugitive_2", [], "I don't understand, {sir/madam}.\
 I never killed anyone. I think you've got the wrong man.", "fugitive_3",[]],
[trp_fugitive|plyr,"fugitive_3", [], "Then drop your sword. If you are innocent, you have nothing to fear.\
 We'll go now and talk to your neighbours, and if they verify your story, I'll go on my way.", "fugitive_4",[]],
[anyone,"fugitive_4", [], "I'm not going anywhere, friend. You're going to have to fight for your silver, today.", "fugitive_5",
   []],
[trp_fugitive|plyr,"fugitive_5", [], "No problem. I really just need your head, anyway.", "fugitive_fight_start",[]],
[trp_fugitive|plyr,"fugitive_5", [], "I come not for money, but to execute the law!", "fugitive_fight_start",[]],
[trp_fugitive|plyr,"fugitive_5", [], "Alas, that you cannot be made to see reason.", "fugitive_fight_start",[]],
[anyone,"fugitive_fight_start", [], "Die, dog!", "close_window",
   [
	(set_party_battle_mode),
    (quest_set_slot, "qst_hunt_down_fugitive", slot_quest_current_state, 1),
    (call_script, "script_activate_tavern_attackers"),
   ]],
[anyone|plyr,"sacrificed_messenger_1", [(quest_get_slot, ":quest_target_center", "qst_incriminate_loyal_commander", slot_quest_target_center),
                                          (str_store_party_name, s1, ":quest_target_center"),
                                          (quest_get_slot, ":quest_object_troop", "qst_incriminate_loyal_commander", slot_quest_object_troop),
                                          (str_store_troop_name, s2, ":quest_object_troop"),],
   "Take this letter to {s1} and give it to {s2}.", "sacrificed_messenger_2",[]],
[anyone|plyr,"sacrificed_messenger_1", [],
   "Nothing. Nothing at all.", "close_window",[]],
[anyone,"sacrificed_messenger_2", [],
   "Yes {sir/madam}. You can trust me. I will not fail you.", "sacrificed_messenger_3",[]],
[anyone|plyr,"sacrificed_messenger_3", [],
   "Good. I will not forget your service. You will be rewarded when you return.", "close_window",[(party_remove_members, "p_main_party", "$g_talk_troop", 1),
                                     (set_spawn_radius, 0),
                                     (spawn_around_party, "p_main_party", "pt_sacrificed_messenger"),
                                     (assign, ":new_party", reg0),
                                     (party_add_members, ":new_party", "$g_talk_troop", 1),
                                     (party_set_ai_behavior, ":new_party", ai_bhvr_travel_to_party),
                                     (quest_get_slot, ":quest_target_center", "qst_incriminate_loyal_commander", slot_quest_target_center),
                                     (party_set_ai_object, ":new_party", ":quest_target_center"),
                                     (party_set_flags, ":new_party", pf_default_behavior, 0),
                                     (quest_set_slot, "qst_incriminate_loyal_commander", slot_quest_current_state, 2),
                                     (quest_set_slot, "qst_incriminate_loyal_commander", slot_quest_target_party, ":new_party")]],
[anyone|plyr,"sacrificed_messenger_3", [], "Arggh! I can't do this. I can't send you to your own death!", "sacrificed_messenger_cancel",[]],
[anyone,"sacrificed_messenger_cancel", [], "What do you mean {sir/madam}", "sacrificed_messenger_cancel_2",[]],
[anyone|plyr,"sacrificed_messenger_cancel_2", [(quest_get_slot, ":quest_giver", "qst_incriminate_loyal_commander", slot_quest_giver_troop),
                                                 (str_store_troop_name, s3, ":quest_giver"),
      ], "There's a trap set up for you in the town.\
 {s3} ordered me to sacrifice one of my chosen warriors to fool the enemy,\
 but he will just need to find another way.", "sacrificed_messenger_cancel_3",[
     (quest_get_slot, ":quest_giver", "qst_incriminate_loyal_commander", slot_quest_giver_troop),
     (quest_set_slot, "qst_incriminate_loyal_commander", slot_quest_current_state, 1),
     (call_script, "script_change_player_relation_with_troop",":quest_giver",-5),
     (call_script, "script_change_player_honor", 3),
     (call_script, "script_fail_quest", "qst_incriminate_loyal_commander"),
     ]],
[anyone,"sacrificed_messenger_cancel_3", [], "Thank you, {sir/madam}.\
 I will follow you to the gates of hell. But this would not be a good death.", "close_window",[]],
[anyone|plyr, "follow_spy_talk",
   [
     (quest_get_slot, ":quest_giver", "qst_follow_spy", slot_quest_giver_troop),
     (str_store_troop_name, s1, ":quest_giver"),
     ],
   "In the name of {s1}, you are under arrest!", "follow_spy_talk_2", []],
[anyone, "follow_spy_talk_2", [], "You won't get me alive!", "close_window", []],
[anyone|plyr, "follow_spy_talk", [], "Never mind me. I was just passing by.", "close_window", [(assign, "$g_leave_encounter",1)]],
[anyone|plyr,"spy_partners_talk",
   [
     (quest_get_slot, ":quest_giver", "qst_follow_spy", slot_quest_giver_troop),
     (str_store_troop_name, s1, ":quest_giver"),
     ],
   "In the name of {s1} You are under arrest!", "spy_partners_talk_2",[]],
[anyone,"spy_partners_talk_2", [], "You will have to fight us first!", "close_window",[]],
[anyone|plyr,"spy_partners_talk", [], "Never mind me. I was just passing by.", "close_window",[(assign, "$g_leave_encounter",1)]],
[anyone|plyr,"runaway_serf_intro_1", [(quest_get_slot, ":lord", "qst_bring_back_runaway_serfs", slot_quest_giver_troop),
                                        (str_store_troop_name, s4, ":lord")],
   "I have been sent by your {s4} whom you are running from. He will not punish you if you return now.", "runaway_serf_intro_2",[]],
[anyone,"runaway_serf_intro_2", [(quest_get_slot, ":target_center", "qst_bring_back_runaway_serfs", slot_quest_target_center),
                                   (str_store_party_name, s6, ":target_center"),
                                   (quest_get_slot, ":quest_object_center", "qst_bring_back_runaway_serfs", slot_quest_object_center),
                                   (str_store_party_name, s1, ":quest_object_center")],
   "My good {sir/madam}. Our lives at our village {s1} was unbearable. We worked all day long and still went to bed hungry.\
 We are going to {s6} to start a new life, where we will be treated like humans.", "runaway_serf_intro_3",[]],
[anyone|plyr,"runaway_serf_intro_3", [(quest_get_slot, ":quest_object_center", "qst_bring_back_runaway_serfs", slot_quest_object_center),
                                        (str_store_party_name, s1, ":quest_object_center"),],
   "You have gone against our laws by running from your bondage. You will go back to {s1} now!", "runaway_serf_go_back",
   [(quest_get_slot, ":quest_object_center", "qst_bring_back_runaway_serfs", slot_quest_object_center),
    (call_script, "script_change_player_relation_with_center", ":quest_object_center", -1)]],
[anyone|plyr,"runaway_serf_intro_3", [], "Well, maybe you are right. All right then. If anyone asks, I haven't seen you.", "runaway_serf_let_go",
   [(quest_get_slot, ":quest_object_center", "qst_bring_back_runaway_serfs", slot_quest_object_center),
    (call_script, "script_change_player_relation_with_center", ":quest_object_center", 1)]],
[party_tpl|pt_runaway_serfs,"runaway_serf_go_back", [(quest_get_slot, ":home_center", "qst_bring_back_runaway_serfs", slot_quest_object_center),
                                                       (str_store_party_name, s5, ":home_center")],
   "All right {sir/madam}. As you wish. We'll head back to {s5} now.", "close_window",
   [(quest_get_slot, ":quest_object_center", "qst_bring_back_runaway_serfs", slot_quest_object_center),
    (party_set_ai_object, "$g_encountered_party", ":quest_object_center"),
    (assign, "$g_leave_encounter",1)]],
[anyone,"runaway_serf_let_go", [], "God bless you, {sir/madam}. We will not forget your help.", "close_window",
   [(party_set_slot, "$g_encountered_party", slot_town_castle, 1),
    (assign, "$g_leave_encounter",1)]],
[anyone|plyr,"runaway_serf_reconsider", [], "I have changed my mind. You must back to your village!", "runaway_serf_go_back",
   [(party_set_slot, "$g_encountered_party", slot_town_castle, 0),
    (quest_get_slot, ":quest_object_center", "qst_bring_back_runaway_serfs", slot_quest_object_center),
    (call_script, "script_change_player_relation_with_center", ":quest_object_center", -2)]],
[anyone|plyr,"runaway_serf_reconsider", [], "Good. Go quickly now before I change my mind.", "runaway_serf_let_go",[]],
[anyone|plyr,"runaway_serf_talk_caught", [], "Do not test my patience. You are going back now!", "runaway_serf_go_back",[]],
[anyone|plyr,"runaway_serf_talk_caught", [], "Well, if you are that eager to go, then go.", "runaway_serf_let_go",
   [(quest_get_slot, ":quest_object_center", "qst_bring_back_runaway_serfs", slot_quest_object_center),
    (call_script, "script_change_player_relation_with_center", ":quest_object_center", 1)]],
[anyone|plyr,"runaway_serf_talk_again_return", [], "Make haste now. The sooner you return the better.", "runaway_serf_talk_again_return_2",[]],
[anyone|plyr,"runaway_serf_talk_again_return", [], "Good. Keep going.", "runaway_serf_talk_again_return_2",[]],
[anyone|plyr,"runaway_serf_talk_again_return_2", [], "Yes {sir/madam}. As you wish.", "close_window",[(assign, "$g_leave_encounter",1)]],
[anyone|plyr,"troublesome_bandits_intro_1", [],
   "Heh. For me, you are nothing more than walking money bags.\
 A merchant in {s1} offered me good money for your heads.",
   "troublesome_bandits_intro_2", [(quest_get_slot, ":quest_giver_center", "qst_track_down_bandits", slot_quest_giver_center),
                                   (str_store_party_name, s1, ":quest_giver_center")
                                   ]],
[anyone,"troublesome_bandits_intro_2", [],
   "A bounty hunter! Kill {him/her}! Kill {him/her} now!", "close_window",[
   (encounter_attack)]],
[anyone|plyr,"deserter_paid_talk", [], "Sorry to trouble you. I'll be on my way now.", "deserter_paid_talk_2a",[]],
[anyone,"deserter_paid_talk_2a", [], "Yeah. Stop fooling around and go make some money.\
 I want to see that purse full next time I see you.", "close_window",[(assign, "$g_leave_encounter",1)]],
[anyone|plyr,"deserter_paid_talk", [], "No. It's your turn to pay me this time.", "deserter_paid_talk_2b",[]],
[anyone,"deserter_paid_talk_2b", [], "What nonsense are you talking about? You want trouble? You got it.", "close_window",[
       (party_set_slot,"$g_encountered_party",slot_party_ignore_player_until,0),
       (party_ignore_player, "$g_encountered_party", 0),
    ]],
[anyone|plyr,"deserter_talk", [], "When I'm done with you, you'll regret ever leaving your army.", "close_window",[]],
[anyone|plyr,"deserter_talk", [], "There's no need to fight. I am ready to pay for free passage.", "deserter_barter",[]],
[anyone,"deserter_barter", [], "Good. You are clever. Now, having a look at your baggage, I reckon a fellow like you could pretty easily afford {reg5} mon. We wouldn't want to be too greedy, now would we? Pay us, and then you can go.", "deserter_barter_2",[
    (store_troop_gold, ":total_value", "trp_player"),
    (troop_get_inventory_capacity, ":inv_size", "trp_player"),
    (try_for_range, ":i_slot", 0, ":inv_size"),
         (troop_get_inventory_slot, ":item_id", "trp_player", ":i_slot"),
         (ge, ":item_id", 0),
         (try_begin),
           (is_between, ":item_id", trade_goods_begin, trade_goods_end),
           (store_item_value, ":item_value", ":item_id"),
           (val_add, ":total_value", ":item_value"),
         (try_end),
    (try_end),
    (store_div, "$g_tribute_amount", ":total_value", 10), #10000 gold = excellent_target
    (val_max, "$g_tribute_amount", 10),
    (assign,reg(5),"$g_tribute_amount")]],
[anyone|plyr,"deserter_barter_2", [(store_troop_gold,reg(2)),(ge,reg(2),"$g_tribute_amount"),(assign,reg(5),"$g_tribute_amount")],
   "All right here's your {reg5} mon.", "deserter_barter_3a",[(troop_remove_gold, "trp_player","$g_tribute_amount")]],
[anyone|plyr,"deserter_barter_2", [],
   "I don't have that much money with me", "deserter_barter_3b",[]],
[anyone,"deserter_barter_3b", [],
   "Too bad. Then we'll have to sell you to the slavers.", "close_window",[]],
[anyone,"deserter_barter_3a", [], "Heh. That wasn't difficult, now, was it? All right. Go now.", "close_window",[
    (store_current_hours,":protected_until"),
    (val_add, ":protected_until", 72),
    (party_set_slot,"$g_encountered_party",slot_party_ignore_player_until,":protected_until"),
    (party_ignore_player, "$g_encountered_party", 72),

    (assign, "$g_leave_encounter",1)
    ]],
[anyone,"tavernkeeper_pretalk", [], "Anything else?", "tavernkeeper_talk",[]],
[anyone|plyr,"tavernkeeper_talk", [(check_quest_active,"qst_deliver_wine"),
                                     (quest_slot_eq, "qst_deliver_wine", slot_quest_target_center, "$g_encountered_party"),
                                     (quest_get_slot, ":quest_target_item", "qst_deliver_wine", slot_quest_target_item),
                                     (quest_get_slot, ":quest_target_amount", "qst_deliver_wine", slot_quest_target_amount),
                                     (store_item_kind_count, ":item_count", ":quest_target_item"),
                                     (ge, ":item_count", ":quest_target_amount"),
                                     (assign, reg9, ":quest_target_amount"),
                                     (str_store_item_name, s4, ":quest_target_item"),
                                     ],
   "I was told to deliver you {reg9} units of {s4}.", "tavernkeeper_deliver_wine",[]],
[anyone,"tavernkeeper_deliver_wine", [],
 "At last! My stock was almost depleted.\
 I had paid the cost of the {s4} in advance.\
 Here, take these {reg5} mon. That should cover your pay.\
 And give {s9} my regards.\
 I'll put in a good word for you next time I deal with him.", "tavernkeeper_pretalk",
   [(quest_get_slot, ":quest_target_item", "qst_deliver_wine", slot_quest_target_item),
    (quest_get_slot, ":quest_target_amount", "qst_deliver_wine", slot_quest_target_amount),
    (quest_get_slot, ":quest_gold_reward", "qst_deliver_wine", slot_quest_gold_reward),
    (quest_get_slot, ":quest_giver_troop", "qst_deliver_wine", slot_quest_giver_troop),
    (troop_remove_items, "trp_player", ":quest_target_item", ":quest_target_amount"),
    (call_script, "script_troop_add_gold", "trp_player", ":quest_gold_reward"),
    (assign, ":xp_reward", ":quest_gold_reward"),
    (val_mul, ":xp_reward", 4),
    (add_xp_as_reward, ":xp_reward"),
    (assign, reg5, ":quest_gold_reward"),
    (str_store_item_name, s4, ":quest_target_item"),
    (str_store_troop_name, s9, ":quest_giver_troop"),

    (quest_get_slot, ":giver_town", "qst_deliver_wine", slot_quest_giver_center),
    (call_script, "script_change_player_relation_with_center", ":giver_town", 2),
    (call_script, "script_change_player_relation_with_center", "$current_town", 1),
    (call_script, "script_end_quest", "qst_deliver_wine"),
    ]],
[anyone|plyr,"tavernkeeper_talk", [(check_quest_active,"qst_deliver_wine"),
                                     (quest_slot_eq, "qst_deliver_wine", slot_quest_target_center, "$g_encountered_party"),
                                     (quest_get_slot, ":quest_target_item", "qst_deliver_wine", slot_quest_target_item),
                                     (quest_get_slot, ":quest_target_amount", "qst_deliver_wine", slot_quest_target_amount),
                                     (store_item_kind_count, ":item_count", ":quest_target_item"),
                                     (lt, ":item_count", ":quest_target_amount"),
                                     (gt, ":item_count", 0),
                                     (assign, reg9, ":quest_target_amount"),
                                     (str_store_item_name, s4, ":quest_target_item"),
                                     ],
   "I was told to deliver you {reg9} units of {s4}, but I lost some of the cargo on the way.", "tavernkeeper_deliver_wine_incomplete",[]],
[anyone,"tavernkeeper_deliver_wine_incomplete", [],
 "Attacked by bandits eh?\
 You are lucky they left you alive.\
 Anyway, I can pay you no more than {reg5} mon for this.\
 And I will let {s1} know that my order was delivered less than completely,\
 so you will probably be charged for this loss.", "tavernkeeper_pretalk",
   [(quest_get_slot, ":quest_target_item", "qst_deliver_wine", slot_quest_target_item),
    (quest_get_slot, ":quest_target_amount", "qst_deliver_wine", slot_quest_target_amount),
    (quest_get_slot, ":quest_gold_reward", "qst_deliver_wine", slot_quest_gold_reward),
    (quest_get_slot, ":quest_giver_troop", "qst_deliver_wine", slot_quest_giver_troop),
    (store_item_kind_count, ":item_count", ":quest_target_item"),
    (troop_remove_items, "trp_player", ":quest_target_item", ":item_count"),
    (val_mul, ":quest_gold_reward", ":item_count"),
    (val_div, ":quest_gold_reward", ":quest_target_amount"),
    (call_script, "script_troop_add_gold", "trp_player", ":quest_gold_reward"),
    (assign, reg5, ":quest_gold_reward"),
    (assign, ":xp_reward", ":quest_gold_reward"),
    (val_mul, ":xp_reward", 4),
    (add_xp_as_reward, ":xp_reward"),
    (str_store_troop_name, s1, ":quest_giver_troop"),
    (assign, ":debt", "$qst_deliver_wine_debt"),
    (store_sub, ":item_left", ":quest_target_amount", ":item_count"),
    (val_mul, ":debt", ":item_left"),
    (val_div, ":debt", ":quest_target_amount"),
    (val_add, "$debt_to_merchants_guild", ":debt"),
    (quest_get_slot, ":giver_town", "qst_deliver_wine", slot_quest_giver_center),
    (call_script, "script_change_player_relation_with_center", ":giver_town", 1),
    (call_script, "script_end_quest", "qst_deliver_wine"),
    ]],
[anyone|plyr,"tavernkeeper_talk", [(check_quest_active,"qst_deliver_wine"),
                                     (quest_slot_eq, "qst_deliver_wine", slot_quest_target_center, "$g_encountered_party"),
                                     (quest_get_slot, ":quest_target_item", "qst_deliver_wine", slot_quest_target_item),
                                     (store_item_kind_count, ":item_count", ":quest_target_item"),
                                     (eq, ":item_count", 0),
                                     (quest_get_slot, reg9, "qst_deliver_wine", slot_quest_target_amount),
                                     (str_store_item_name, s4, ":quest_target_item"),
                                     ],
   "I was told to deliver you {reg9} units of {s4}, but I lost the cargo on the way.", "tavernkeeper_deliver_wine_lost",[]],
[anyone,"tavernkeeper_deliver_wine_lost", [],
 "What? I was waiting for that {s4} for weeks!\
 And now you are telling me that you lost it?\
 You may rest assured that I will let {s1} know about this.", "tavernkeeper_pretalk",
   [(add_xp_as_reward, 40),
    (quest_get_slot, ":quest_target_item", "qst_deliver_wine", slot_quest_target_item),
    (quest_get_slot, ":quest_giver_troop", "qst_deliver_wine", slot_quest_giver_troop),
    (str_store_item_name, s4, ":quest_target_item"),
    (str_store_troop_name, s1, ":quest_giver_troop"),
    (val_add, "$debt_to_merchants_guild", "$qst_deliver_wine_debt"),
    (call_script, "script_end_quest", "qst_deliver_wine"),
   ]],
[anyone|plyr,"tavernkeeper_talk", [
      (store_current_hours,":cur_hours"),
      (val_sub, ":cur_hours", 24),
      (gt, ":cur_hours", "$buy_drinks_last_time"),
	  ##diplomacy start+ Replace with cultural equivalent
	  ##OLD:
      #], "I'd like to buy every man who comes in here tonight a jar of your best wine.", "tavernkeeper_buy_drinks",[]],
	  ##NEW:
	  (call_script, "script_dplmc_print_cultural_word_to_sreg", "$g_talk_troop", DPLMC_CULTURAL_TERM_TAVERNWINE, 0),
	  ], "I'd like to buy every man who comes in here tonight a jar of your best {s0}.", "tavernkeeper_buy_drinks",[]],
[anyone,"tavernkeeper_buy_drinks",
   [
    ], "Of course, {my lord/my lady}. I reckon {reg5} mon should be enough for that. What should I tell everyone?", "tavernkeeper_buy_drinks_2",[
        (assign, "$temp", 1000),
        (assign, reg5, "$temp"),
        ]],
[anyone|plyr,"tavernkeeper_buy_drinks_2",
   [
        (store_troop_gold, ":gold", "trp_player"),
        (ge, ":gold", "$temp"),
        (str_store_party_name, s10, "$current_town"),
    ], "Let everyone know of the generosity of {playername} to the people of {s10}.", "tavernkeeper_buy_drinks_end",[

        ]],
[anyone,"tavernkeeper_buy_drinks_end",
  ##diplomacy start+ Replace {sir/madam} with {s0}
   #[], "Don't worry {sir/madam}. Your name will be cheered and toasted here all night.", "tavernkeeper_pretalk",
   [(call_script, "script_dplmc_print_commoner_at_arg1_says_sir_madame_to_s0", "$current_town"),
   ], "Don't worry {s0}. Your name will be cheered and toasted here all night.", "tavernkeeper_pretalk",
   ##diplomacy end+
   [
       (troop_remove_gold, "trp_player", "$temp"),
       (call_script, "script_change_player_relation_with_center", "$current_town", 1),
       (store_current_hours,":cur_hours"),
       (assign, "$buy_drinks_last_time", ":cur_hours"),
       ]],
[anyone|plyr,"tavernkeeper_buy_drinks_2", [], "Actually, cancel that order.", "tavernkeeper_pretalk",[]],
[anyone|plyr,"tavernkeeper_talk", [
  (neq, "$g_encountered_party_faction", "fac_player_supporters_faction"),
  ],
   "Have you heard of anyone in this domain who might have a job for a {man/woman} like myself?", "tavernkeeper_job_ask",[
   ]],
[anyone,"tavernkeeper_job_ask",
   [
	(str_store_string, s9, "str__of_course_the_land_is_currently_at_peace_so_you_may_have_better_luck_in_other_realms"),
	(try_for_range, ":faction", kingdoms_begin, kingdoms_end),
		(store_relation, ":relation", "$g_encountered_party_faction", ":faction"),
		(lt, ":relation", 0),
		(str_clear, s9),
	(try_end),
	(faction_get_slot, ":leader",  "$g_encountered_party_faction", slot_faction_leader),
	(str_store_troop_name, s10, ":leader"),
	##diplomacy start+ Fix pronoun "his" -> {reg0?her:his}
	(call_script, "script_dplmc_store_troop_is_female", ":leader"),
   ], "Hmm... Well, {s10} is often looking for mercenaries to fight in {reg0?her:his} wars.{s9}", "tavernkeeper_job_search",
   ##diplomacy end+
    [
   (assign, "$g_troop_list_no", 0),
    ]],
[anyone, "tavernkeeper_job_search",
  [],
  "Let me think some more...", "tavernkeeper_job_result",
  [
    (call_script, "script_npc_find_quest_for_player_to_s11", "$g_encountered_party_faction"),
	(assign, ":quest_giver", reg0),

	(call_script, "script_get_dynamic_quest", ":quest_giver"),
	(assign, ":quest_type", reg0),

	(try_begin),
		(gt, ":quest_giver", -1),
		(str_store_troop_name, s7, ":quest_giver"),
		(str_clear, s9), #location string

		(assign, ":location", -1),
		(try_begin),
			(troop_slot_eq, ":quest_giver", slot_troop_occupation, slto_kingdom_hero),
			(troop_get_slot, ":quest_giver_party", ":quest_giver", slot_troop_leaded_party),
			(party_is_active, ":quest_giver_party"),
			(party_get_attached_to, ":location", ":quest_giver_party"),
		(else_try),
			(is_between, ":quest_giver", mayors_begin, mayors_end),
			(try_for_range, ":town", towns_begin, towns_end),
				(party_slot_eq, ":town", slot_town_elder, ":quest_giver"),
				(assign, ":location", ":town"),
			(try_end),
		(try_end),

		(try_begin),
			(gt, ":location", -1),
			(try_begin),
				(eq, ":location", "$g_encountered_party"),
				(str_store_string, s8, "str_here"),
			(else_try),
				(str_store_string, s8, "str_over"),
			(try_end),
			(str_store_party_name, s12, ":location"),
			(str_store_string, s9, "str_s8_in_s12"),
		(try_end),

		##diplomacy start+ Do this first
		(call_script, "script_dplmc_store_troop_is_female_reg", ":quest_giver", 4),
		##diplomacy end+
		(try_begin),
			(eq, ":quest_type", "qst_track_down_bandits"),
			(str_store_string, s10, "str__has_put_together_a_bounty_on_some_bandits_who_have_been_attacking_travellers_in_the_area"),
		(else_try),
			(eq, ":quest_type", "qst_destroy_bandit_lair"),
			(str_store_string, s10, "str__has_been_worried_about_bandits_establishing_a_hideout_near_his_home"),
		(else_try),
			(eq, ":quest_type", "qst_retaliate_for_border_incident"),
			(str_store_string, s10, "str__is_looking_for_a_way_to_avoid_an_impending_war"),
		(else_try),
			(eq, ":quest_type", "qst_rescue_prisoner"),
			(str_store_string, s10, "str__may_need_help_rescuing_an_imprisoned_family_member"),
		(else_try),
			(eq, ":quest_type", "qst_cause_provocation"),
			(str_store_string, s10, "str__has_been_asking_around_for_someone_who_might_want_work_id_watch_yourself_with_him_though"),
		(else_try),
			(str_store_string, s10, "str_tavernkeeper_invalid_quest"),
		(try_end),

		##diplomacy start+
		#(troop_get_type, reg4, ":quest_giver"),
		(call_script, "script_dplmc_store_troop_is_female_reg", ":quest_giver", 4),
		##diplomacy end+
	(try_end),

  ]],
[anyone, "tavernkeeper_job_result", [
  	(store_sub, ":last_troop", mayors_end, 1),
	(lt, "$g_troop_list_no", ":last_troop"),
  ], "I have heard that {s7} {s9}{s10} You may want to speak with {reg4?her:him}.", "tavernkeeper_job_search",
   [
       ]],
[anyone, "tavernkeeper_job_result", [
  (store_sub, ":last_troop", mayors_end, 1),
  (ge, "$g_troop_list_no", ":last_troop"),
  ], "There may be other work, of course -- lords and merchants often have other tasks which we don't hear about. Also, the villages around here frequently need help, although they'd be more likely to pay you with a wedge of cheese and goodwill than with cold hard mon.", "tavernkeeper_job_result_2",
   [
       ]],
[anyone,"tavernkeeper_job_result_2", [], "I'll keep my ears open for other opportunities. You may want to ask again from time to time.", "close_window",[]],
[anyone|plyr,"tavernkeeper_talk", [], "I guess I should leave now.", "close_window",[]],
[anyone|plyr, "bookseller_talk", [], "Yes. Show me what you have for sale.", "bookseller_buy", []],
[anyone,"bookseller_buy", [], "Of course {sir/madam}.", "book_trade_completed",[[change_screen_trade]]],
[anyone,"book_trade_completed", [], "Anything else?", "bookseller_talk",[]],
[anyone|plyr,"bookseller_talk", [], "Nothing. Thanks.", "close_window",[]],
[anyone|plyr, "minstrel_1", [(eq, "$minstrels_introduced", 0),],
   "What is it you do?", "minstrel_job_description",
   [(assign, "$minstrels_introduced", 1), ]],
[anyone|plyr, "minstrel_1", [(eq, "$minstrels_introduced", 1)  ],
   "I have some questions about courtship in Japan",
   "minstrel_courtship_questions", []],
[anyone|plyr, "minstrel_1", [(eq, "$minstrels_introduced", 1)  ],
   "Can you teach me any poems?",
   "minstrel_courtship_poem", []],
[anyone, "minstrel_courtship_poem", [
    (eq, "$allegoric_poem_recitations", 0),
	(this_or_next|eq, "$g_talk_troop", "trp_tavern_minstrel_1"),
		(eq, "$g_talk_troop", "trp_tavern_minstrel_5"),
  ],
   "I can teach you the poem, 'The Storming of the Castle of Love.' It is short enough to be easily learned. It is an allegoric poem, replete with symbols and metaphor. It describes how a brave but rough warrior wins the heart of his lady by upholding, becoming a dutiful and honorable samurai. Its theme -- that the role of a woman is to inspire but also civilize a man -- is appreciated by some noble ladies, but not all.",
   "minstrel_courtship_poem_teach", [
    (assign, "$poem_selected", courtship_poem_allegoric),
   ]],
[anyone, "minstrel_courtship_poem", [
    (eq, "$mystic_poem_recitations", 0),
	(this_or_next|eq, "$g_talk_troop", "trp_tavern_minstrel_3"),
		(eq, "$g_talk_troop", "trp_tavern_minstrel_1"),
  ],
   "I can teach you the poem, 'The Heart's Desire.' It is a lyrical poem, which can be interpreted either erotically or spiritually. The lover realizes the majesty of the divine by gazing upon the body of his beloved. I believe that it appeals to women of a certain romantic temperament, but you risk scandalizing or boring others.",
   "minstrel_courtship_poem_teach", [
   (assign, "$poem_selected", courtship_poem_mystic),
   ]],
[anyone, "minstrel_courtship_poem", [
  	(eq, "$tragic_poem_recitations", 0),
	(this_or_next|eq, "$g_talk_troop", "trp_tavern_minstrel_3"),
		(eq, "$g_talk_troop", "trp_tavern_minstrel_2"),  ],
   "I can teach you the tale of Naniha and Futo no Kata. It is a sad and simple story -- the farmhand Naniha and the nobleman's daughter Futo no Kata love each other, but they can never marry. The poem is Naniha's lament as he wanders alone, unwilling to forget his true love, driving himself mad with longing. Some ladies melt at the sweetness of his sorrows; others glaze over at his self-pity.",
   "minstrel_courtship_poem_teach", [
   (assign, "$poem_selected", courtship_poem_tragic),

   ]],
[anyone, "minstrel_courtship_poem", [
	(eq, "$heroic_poem_recitations", 0),
	(this_or_next|eq, "$g_talk_troop", "trp_tavern_minstrel_4"),
		(eq, "$g_talk_troop", "trp_tavern_minstrel_2"),

  ],
   "I can teach you part of the saga of Yoshinaka and Tomoe. It is a heroic tale, full of blood and battle. The maiden Tomoe chooses the warrior Yoshinaka as her lover, as he is the only man who can defeat her in combat. Her father, who pledged her to another, comes with his sons and his samurai to kill Yoshinaka. They fight, and Yoshinaka and Tomoe slaughter the entire host except for Tomoe's beloved younger brother -- who, alas, grows up to avenge his father by slaying Yoshinaka. The depiction of warrior and maiden as equals will appeal to some women, but a yoroi-wearing, blood-spattered heroine will shock and repulse others.",
   "minstrel_courtship_poem_teach", [
   (assign, "$poem_selected", courtship_poem_heroic),
   ]],
[anyone, "minstrel_courtship_poem", [
    (eq, "$comic_poem_recitations", 0),
	(this_or_next|eq, "$g_talk_troop", "trp_tavern_minstrel_5"),
		(eq, "$g_talk_troop", "trp_tavern_minstrel_4"),
  ],
   "I can teach you the poem, 'An Argument in the Garden.' It is a comic poem, which satirizes the conventions of courtly love. A lover steals into a garden in Kyoto, and plies her with lots of witty lines to persuade his lover to submit to his embraces. She shoots down all of his advances one by one, then when he is downcast, she takes him in her arms and tells him that she wanted him all along, except on her terms, not his. A lady with a sense of humor may find it amusing, but others might feel that they are the ones who are being mocked.",
   "minstrel_courtship_poem_teach", [
   (assign, "$poem_selected", courtship_poem_comic),
   ]],
[anyone, "minstrel_courtship_poem_teach", [],
   "To teach it to you, I will need some hours of your time -- and, of course, a small fee for my services. About 300 mon would suffice.",
   "minstrel_courtship_poem_teach_2", []],
[anyone, "minstrel_courtship_poem", [],
   "I believe you already know the poems I am best equipped to teach.",
   "minstrel_pretalk", []],
[anyone|plyr, "minstrel_courtship_poem_teach_2", [
  (store_troop_gold, ":gold", "trp_player"),
  (ge, ":gold", 300),
  ],
   "Yes -- teach me that one",
   "minstrel_courtship_poem_teach_3", []],
[anyone|plyr, "minstrel_courtship_poem_teach_2", [],
   "Never mind",
   "minstrel_pretalk", []],
[anyone, "minstrel_courtship_poem_teach_3", [
  (eq, "$poem_selected", courtship_poem_allegoric),
  ],
   "Very well -- repeat after me:^\
   I deflected her skeptical questioning darts^\
   with armor made of purest devotion^\
   purged in the forge of my heart^\
   from the slag of any baser emotion",
   "minstrel_courtship_poem_teach_4", []],
[anyone, "minstrel_courtship_poem_teach_3", [
  (eq, "$poem_selected", courtship_poem_mystic),
  ],
   "Very well -- repeat after me:^\
   You are the first and the last^\
   the outer and the inner^\
   When I drink from the cup of love^\
   I escape the tread of time^\
   A moment in solitude with you^\
   Would have no beginning and no end",
   "minstrel_courtship_poem_teach_4", []],
[anyone, "minstrel_courtship_poem_teach_3", [
  (eq, "$poem_selected", courtship_poem_tragic),
  ],
  "Very well -- repeat after me:^\
  The wind that blows the dry road's dust^\
  Stirs the curtains in your tower^\
  The moon that lights my drunken path home^\
  Looks on you sleeping in your bower^\
  If I cried out to the wind^\
  Could it carry a message from my lips?^\
  If I wept before the moon^\
  Would it grant me just a glimpse?",
  "minstrel_courtship_poem_teach_4", [
   ]],
[anyone, "minstrel_courtship_poem_teach_3", [
  (eq, "$poem_selected", courtship_poem_heroic),
  ],
  "Very well -- repeat after me:^\
   A light pierced the gloom over Kyushu's cliffs...^\
   Where charge of surf broke on the wall of the shore^\
   Grey-helmed and grey-cloaked the maiden stood^\
   On wave-steed's prow, the sailcloth snapping^\
   Over din of oars, of timbers cracking^\
   She cried out to her own brothers, arrayed for war",
   "minstrel_courtship_poem_teach_4", [
   ]],
[anyone, "minstrel_courtship_poem_teach_3", [
  (eq, "$poem_selected", courtship_poem_comic),
  ],
  "Very well -- repeat after me:^All the silks of China, all the furs of the Jurchen^\
   Would buy you not the briefest kiss^What I bestow, I bestow for love^\
   And the sake of my own happiness^But brought you a gift? Let us see! Let us see!^\
   Or should tell my father how you came to see me?",
  "minstrel_courtship_poem_teach_4", [
   ]],
[anyone|plyr, "minstrel_courtship_poem_teach_4", [
  (eq, "$poem_selected", courtship_poem_allegoric),
  ],
  "'I deflected her skeptical questioning darts...'",
  "minstrel_learn_poem_continue", [
    (troop_remove_gold, "trp_player", 300),
    (val_add, "$allegoric_poem_recitations", 1),
  ]],
[anyone|plyr, "minstrel_courtship_poem_teach_4", [
  (eq, "$poem_selected", courtship_poem_mystic),
  ],
  "'You are the first and the last..'",
  "minstrel_learn_poem_continue", [
    (troop_remove_gold, "trp_player", 300),
    (val_add, "$mystic_poem_recitations", 1),
  ]],
[anyone|plyr, "minstrel_courtship_poem_teach_4", [
  (eq, "$poem_selected", courtship_poem_tragic),
  ],
  "'The wind that blows the dry road's dust...'",
  "minstrel_learn_poem_continue", [
    (troop_remove_gold, "trp_player", 300),
	(val_add, "$tragic_poem_recitations", 1),
  ]],
[anyone|plyr, "minstrel_courtship_poem_teach_4", [
  (eq, "$poem_selected", courtship_poem_heroic),
  ],
  "'A light pierced the gloom over Kyushu's cliffs...'",
  "minstrel_learn_poem_continue", [
    (troop_remove_gold, "trp_player", 300),
	(val_add, "$heroic_poem_recitations", 1),
  ]],
[anyone|plyr, "minstrel_courtship_poem_teach_4", [
  (eq, "$poem_selected", courtship_poem_comic),
  ],
  "'All the silks of China...'",
  "minstrel_learn_poem_continue", [
    (troop_remove_gold, "trp_player", 300),
	(val_add, "$comic_poem_recitations", 1),
  ]],
[anyone|plyr, "minstrel_courtship_poem_teach_4", [
  ],
  "Bah... What kind of filth are you trying to teach me?",
  "minstrel_courtship_poem_teach_reject", []],
[anyone, "minstrel_courtship_poem_teach_reject", [
  ],
  "Very well. If the poem is not to your taste, then keep your money. But remember -- with poets and with lovers, what is important is not what pleases you. What is important is what your pleases your audience. If you wish to learn the poem, I am still willing to teach.",
  "minstrel_pretalk", []],
[anyone, "minstrel_learn_poem_continue", [
  ],
   "Very good -- but there are many stanzas to go. Now, listen closely...", "close_window",
   [
    (try_begin),
      (try_begin),
        (eq, "$poem_selected", courtship_poem_mystic),
        (set_achievement_stat, ACHIEVEMENT_ROMANTIC_WARRIOR, 0, 1),
      (else_try),
        (eq, "$poem_selected", courtship_poem_tragic),
        (set_achievement_stat, ACHIEVEMENT_ROMANTIC_WARRIOR, 1, 1),
      (else_try),
        (eq, "$poem_selected", courtship_poem_heroic),
        (set_achievement_stat, ACHIEVEMENT_ROMANTIC_WARRIOR, 2, 1),
      (else_try),
        (eq, "$poem_selected", courtship_poem_comic),
        (set_achievement_stat, ACHIEVEMENT_ROMANTIC_WARRIOR, 3, 1),
      (else_try),
        (eq, "$poem_selected", courtship_poem_allegoric),
        (set_achievement_stat, ACHIEVEMENT_ROMANTIC_WARRIOR, 4, 1),
      (try_end),

      (assign, ":number_of_poems_player_know", 0),
      (try_for_range, ":poem_number", 0, 5),
        (get_achievement_stat, ":poem_is_known", ACHIEVEMENT_ROMANTIC_WARRIOR, ":poem_number"),
        (eq, ":poem_is_known", 1),
        (val_add, ":number_of_poems_player_know", 1),
      (try_end),

      (try_begin),
        (ge, ":number_of_poems_player_know", 3),
        (unlock_achievement, ACHIEVEMENT_ROMANTIC_WARRIOR),
      (try_end),
    (try_end),

    (assign, "$g_leave_town",1),
    (rest_for_hours, 2, 2, 0),
    (finish_mission),
   ]],
[anyone|plyr, "minstrel_1", [(eq, "$minstrels_introduced", 1)  ],
   "Can you tell me anything about the eligible maidens in this domain?",
   "minstrel_gossip", [
   ]],
[anyone, "minstrel_gossip",
  [],
   "About whom did you wish to know?",
   "minstrel_gossip_select", []],
[anyone|plyr,"minstrel_gossip_select",
   [],
   "Just tell me the latest piece of gossip",
   "minstrel_gossip_maiden_selected_2", [

    (assign, "$lady_selected", -1),
	(assign, "$romantic_rival", -1),

    (try_for_range, ":log_entry", 0, "$num_log_entries"),
		(troop_get_slot, ":lady", "trp_log_array_actor", ":log_entry"),
		(is_between, ":lady", kingdom_ladies_begin, kingdom_ladies_end),
		(neg|troop_slot_eq, "trp_player", slot_troop_spouse, ":lady"),

		(troop_get_slot, ":type", "trp_log_array_entry_type", ":log_entry"),
		(is_between, ":type", 50, 65), #excludes log entries in which a party is an actor

		(store_faction_of_troop, ":lady_faction", ":lady"),
		(store_faction_of_party, ":town_faction", "$g_encountered_party"),
		(eq, ":lady_faction", ":town_faction"),
		(assign, "$lady_selected", ":lady"),
		(try_begin),
			(eq, "$cheat_mode", 1),
			(str_store_troop_name, s4, ":lady"),
			(troop_get_slot, reg4, "trp_log_array_entry_type", ":log_entry"),
			(assign, reg5, "$num_log_entries"),
			(display_message, "str_log_entry_type_reg4_for_s4_total_entries_reg5"),
		(try_end),
	(try_end),

   ]],
[anyone|plyr|repeat_for_troops,"minstrel_gossip_select",
   [
   (store_repeat_object, "$temp"),
   (troop_slot_eq, "$temp", slot_troop_occupation, slto_kingdom_lady),
   (troop_slot_eq, "$temp", slot_troop_spouse, -1),
   (store_faction_of_troop, ":lady_faction", "$temp"),
   (store_faction_of_party, ":town_faction", "$g_encountered_party"),
   (eq, ":lady_faction", ":town_faction"),
   (str_store_troop_name, s10, "$temp"),
   ],
   "{s10}",
   "minstrel_gossip_maiden_selected", [
    (store_repeat_object, "$lady_selected"),
   ]],
[anyone|plyr,"minstrel_gossip_select",
   [], "Never mind", "minstrel_pretalk", []],
[anyone,"minstrel_gossip_maiden_selected",
   [
	(try_begin),
		(eq, "$cheat_mode", 1),
		(assign, reg3, "$lady_selected"),
		(display_message, "@{!}DEBUG: Gossip for troop {reg3}"),
		(gt, reg3, -1),
		(display_message, "@{!}DEBUG: {s3}"),
	(try_end),

	(try_begin),
	   (gt, "$lady_selected", -1),
	   (str_store_troop_name, s9, "$lady_selected"), #lady

      ##diplomacy start+ Make gender-correct
      (try_begin),
         (call_script, "script_cf_dplmc_troop_is_female", "$lady_selected"),
         (assign, reg4, 1),
      (else_try),
         (assign, reg4, 0),
      (try_end),
      #the strings below have been modified to use reg4 for gender
      ##diplomacy end+
	   (str_store_string, s10, "str_error__reputation_type_for_s9_not_within_range"),
	   (try_begin),
			(troop_slot_eq, "$lady_selected", slot_lord_reputation_type, lrep_conventional),
			(str_store_string, s16, "str_they_say_that_s9_is_a_most_conventional_maiden__devoted_to_her_family_of_a_kind_and_gentle_temperament_a_lady_in_all_her_way"),
	   (else_try),
			(troop_slot_eq, "$lady_selected", slot_lord_reputation_type, lrep_otherworldly),
			(str_store_string, s16, "str_they_say_that_s9_is_a_bit_of_a_romantic_a_dreamer__of_a_gentle_temperament_yet_unpredictable_she_is_likely_to_be_led_by_her_passions_and_will_be_trouble_for_her_family_ill_wager"),
	   (else_try),
			(troop_slot_eq, "$lady_selected", slot_lord_reputation_type, lrep_ambitious),
			(str_store_string, s16, "str_they_say_that_s9_is_determined_to_marry_well_and_make_her_mark_in_the_world_she_may_be_a_tremendous_asset_for_her_husband__provided_he_can_satisfy_her_ambition"),
	   (else_try),
			(troop_slot_eq, "$lady_selected", slot_lord_reputation_type, lrep_adventurous),
			(str_store_string, s16, "str_they_say_that_s9_loves_to_hunt_and_ride_maybe_she_wishes_she_were_a_man_whoever_she_marries_will_have_a_tough_job_keeping_the_upper_hand_i_would_say"),
	   (else_try),
			(troop_slot_eq, "$lady_selected", slot_lord_reputation_type, lrep_moralist),
			(str_store_string, s16, "str_they_say_that_s9_is_a_lady_of_the_highest_moral_standards_very_admirable_very_admirable__and_very_hard_to_please_ill_warrant"),
	   (try_end),

	   (call_script, "script_add_rumor_string_to_troop_notes", "$lady_selected", -1, 16),
   (try_end),
   ],
   "{s16}",
   "minstrel_gossip_maiden_selected_2", [
   ]],
[anyone,"minstrel_gossip_maiden_selected_2",
   [
	##diplomacy+
	##OLD:
	#(troop_slot_eq, "trp_player", slot_troop_spouse, "$lady_selected"),
	#(is_between, "$lady_selected", kingdom_ladies_begin, kingdom_ladies_end),
	##NEW:
	(is_between, "$lady_selected", heroes_begin, heroes_end),
	(this_or_next|troop_slot_eq, "$lady_selected", slot_troop_spouse, "trp_player"),
		(troop_slot_eq, "trp_player", slot_troop_spouse, "$lady_selected"),
	(call_script, "script_dplmc_store_troop_is_female",  "$lady_selected"),#Add support for male version
	],#Next line, "She" -> {reg0?She:He} , "she" -> {reg0?she:he}
	"{reg0?She:He} is married to you, of course! Clearly, no one would dream that {reg0?she:he} would do anything to engender gossip.",
   "minstrel_postgossip",
   ##diplomacy end+
	[]],
[anyone,"minstrel_gossip_maiden_selected_2",
   [
    (gt, "$lady_selected", -1),
	(assign, ":lady", "$lady_selected"),
	(neg|troop_slot_ge, ":lady", slot_troop_spouse, active_npcs_begin),
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
	"{s12}.",
   "minstrel_postgossip", []],
[anyone,"minstrel_gossip_maiden_selected_2",
   [
      ##diplomacy start+ Make gender-correct
      #xxx TODO ensure this actually works, untangle how this is used
      #The strings below have been modified to use reg4 for gender
     (try_begin),
        (call_script, "script_cf_dplmc_troop_is_female", "$lady_selected"),
        (assign, reg4, 1),
	 (else_try),
        (assign, reg4, 0),
     (try_end),
      ##diplomacy end+
    (try_begin),
		(is_between, "$lady_selected", kingdom_ladies_begin, kingdom_ladies_end),
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
   "minstrel_postgossip", []],
[anyone|plyr, "minstrel_postgossip", [],
   "Very interesting -- but let us speak of something else.",
   "minstrel_pretalk", []],
[anyone|plyr, "minstrel_postgossip", [],
   "Very interesting -- is there any more news?",
   "minstrel_gossip", []],
[anyone|plyr, "minstrel_postgossip", [
  (is_between, "$romantic_rival", active_npcs_begin, active_npcs_end),
  (neg|check_quest_active, "qst_duel_courtship_rival"),
  (neg|troop_slot_ge, "trp_player", slot_troop_spouse, kingdom_ladies_begin),
  #diplomacy start+ extra check since the wife may be a lord
  (neg|troop_slot_ge, "trp_player", slot_troop_spouse, active_npcs_begin),
  #diplomacy end+
  ],
   "What? I'll make that miscreant face my sword",
   "minstrel_duel_confirm", []],
[anyone, "minstrel_duel_confirm", [
  (str_store_troop_name, s11, "$romantic_rival"),
  ],
   "Do you mean that? {s11} will be honor-bound to fight you, but challenging a lord to duel over a woman is seen as a bit hot-headed, even in this warlike age.",
   "minstrel_duel_confirm_2", []],
[anyone|plyr, "minstrel_duel_confirm_2", [
  (str_store_troop_name, s11, "$romantic_rival"),
  (str_store_troop_name, s12, "$lady_selected"),
  ],
   "Yes -- I intend to force {s11} to relinquish his suit of {s12}",
   "minstrel_duel_issued", []],
[anyone|plyr, "minstrel_duel_confirm_2", [
  ],
   "No -- I let my passions run away with me, there",
   "minstrel_pretalk", []],
[anyone, "minstrel_duel_issued", [
  ],
   "As you wish. I'll spead the word of your intentions, so that {s13} does not try to back out...",
   "minstrel_pretalk", [
	(str_store_troop_name, s11, "$lady_selected"),
    (str_store_troop_name_link, s13, "$romantic_rival"),
	 ##diplomacy start+ use correct pronoun for gender
	 (call_script, "script_dplmc_store_troop_is_female_reg", "$romantic_rival", 4),
	 ##diplomacy end+
    (str_store_string, s2, "str_you_intend_to_challenge_s13_to_force_him_to_relinquish_his_suit_of_s11"),
    (setup_quest_text, "qst_duel_courtship_rival"),
    (call_script, "script_start_quest", "qst_duel_courtship_rival", "$lady_selected"),
    (quest_set_slot, "qst_duel_courtship_rival", slot_quest_giver_troop, "$lady_selected"),

    (quest_set_slot, "qst_duel_courtship_rival", slot_quest_target_troop, "$romantic_rival"),
    (quest_set_slot, "qst_duel_courtship_rival", slot_quest_xp_reward, 400),
    (quest_set_slot, "qst_duel_courtship_rival", slot_quest_expiration_days, 60),
    (quest_set_slot, "qst_duel_courtship_rival", slot_quest_current_state, 0),
   ]],
[anyone|plyr, "minstrel_1", [(eq, "$minstrels_introduced", 1)  ],
   "Do you know of any ongoing feasts?",
   "minstrel_courtship_locations", []],
[anyone, "minstrel_courtship_locations", [

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
"minstrel_pretalk", []],
[anyone|plyr, "minstrel_1", [],
   "Good-bye.", "close_window", []],
[anyone, "minstrel_courtship_questions", [],
   "What do you wish to know?",
"minstrel_courtship_questions_2", []],
[anyone, "minstrel_courtship_prequestions", [],
   "Can I answer any other questions for you?",
"minstrel_courtship_questions_2", []],
[anyone|plyr, "minstrel_courtship_questions_2", [
  (eq, "$minstrels_discussed_love", 1),
  ],
   "Is there a place for me in the game of love?",
   "minstrel_player_role", [
   (assign, "$minstrels_discussed_player_role", 1),
   ]],
[anyone|plyr, "minstrel_courtship_questions_2", [
   (eq, "$minstrels_discussed_player_role", 1),
  ],
   "How would a suitor meet a lady?",
   "minstrel_player_advice_meet", [
    (assign, "$minstrels_discussed_meetings", 1),
   ]],
[anyone|plyr, "minstrel_courtship_questions_2", [
   (eq, "$minstrels_discussed_meetings", 1),
  ],
   "Having met a lady, how would the suitor woo her?",
   "minstrel_player_advice_woo", [
   ]],
[anyone|plyr, "minstrel_courtship_questions_2", [],
   "Tell me about marriage and love among the nobility of Japan",
   "minstrel_nobles", [
   (assign, "$minstrels_discussed_love", 1),
   ]],
[anyone, "minstrel_nobles", [],
   "Nobles are an odd lot. In Japan, a daughter is a political asset, to be given away to a lord with whom her father wishes to make an alliance. Yet the great families of this land idealize pure love between man and woman, and I have seen many a hardened warrior weep copious tears at the doomed ardour of Sahira and Janun in the songs -- even as he made plans to break his own daughter's heart.",
"minstrel_nobles_2", []],
[anyone, "minstrel_nobles_2", [],
   "Fathers differ, of course. Some parents will let their daughters choose a husband who pleases them. Others, however, feel that to allow their daughters any choice at all would be to diminish their own authority, and insist on imposing a groom whether she likes it or not.",
"minstrel_nobles_3", []],
[anyone, "minstrel_nobles_3", [], "But the majority will steer a middle course -- they will want to make the final decision about a groom, but will weigh their daughter's preferences heavily. Among other factors, a happy marriage is more likely to produce heirs. So, there is a place for courtship, and for the use of skill and passion to win a lady's heart.",
"minstrel_prequestions", []],
[anyone|plyr, "minstrel_courtship_questions_2", [
  (eq, "$minstrels_discussed_love", 1),
  ],
   "What if a lady and her father disagree about a suitor?",
   "minstrel_daughter_father", []],
[anyone, "minstrel_daughter_father", [], "It happens sometimes that a bride elopes. This is a major blow to the father's prestige, leading to lasting enmities. Indeed, it is possible that a war may be fought over a woman. Now, that is a fine topic for a song.",
   "minstrel_daughter_father_2", []],
[anyone, "minstrel_daughter_father_2", [], "In the end, however, most brides will submit to their parents' choice. A noblewoman's family is everything to her, and few are brave enough to risk its disapproval for the sake of man she barely knows. She may pine for her lover, but still accept the groom -- and without tragic love, what would we have to sing about?",
   "minstrel_prequestions", []],
[anyone, "minstrel_player_role", [
   (troop_get_type, ":is_female", "trp_player"),
   (eq, ":is_female", 0),
   ], "Of course! Samurai make a great deal of lineage, but in the end, lands and money speak louder than one's ancestors. Even though you are a foreigner, if you are coming up in the world, then many parents will consider you a fine catch.",
   "minstrel_player_role_2", []],
[anyone, "minstrel_player_role_2", [
   ], "You will have to compete with many other lords of your domain, however, who will have an advantage -- they have known these ladies from childhood, and will have been sized up as grooms by carefully discerning mothers and aunts. Some ladies may be fascinated by the stranger, yet opt for the familiar.",
   "minstrel_player_role_3", []],
[anyone, "minstrel_player_role_3", [
   ], "So know this -- you may have your heart broken. But to enter the arena of love fearing heartbreak is like entering the battlefield fearing the enemy's arrows. Be brave, and shrug off the sting of rejection, and victory may yet be yours.",
   "minstrel_prequestions", []],
[anyone, "minstrel_player_role", [
   ], "{Sir/Lady} -- I will speak bluntly. Most of the {ladies/lords} of this land are looking for a demure {lad/maiden}, whose skin as fair as snow -- and your skin is burnt brown by the sun. They want a {boy/maiden} whose voice is soft as bells -- and your voice is hoarse from commanding {soldiers/men} in battle. Also, athough the {ladies/lords} of Japan appreciate poems about love, most also want heirs, and few {men/women} can ride and fight while {caring for their children/with child}.",
   "minstrel_female_player_3", []],
[anyone, "minstrel_female_player_3", [
   ], "However, not all {ladies/lords} will be so conventionally minded. We poets sing of shield {boys/maidens} and of {hunters/huntresses}, of {men/women} who forged their own path without having sacrificed the chance for love. I would not tell you that it would be easy for you to find a devoted {wife/husband} who will accept your ways, but I would not say that it is impossible.",
   "minstrel_prequestions", []],
[anyone|plyr, "minstrel_courtship_questions_2", [
  (eq, "$minstrels_discussed_love", 1),
  ],
   "What advantage is there in seeking a {wife/husband}?",
   "minstrel_spouse_benefits", []],
[anyone, "minstrel_spouse_benefits", [
  (troop_get_type, ":is_female", "trp_player"),
  (eq, ":is_female", 0),
  ],
   "Ah! You are quite the romantic, I see! Well, aside from the obvious benefits of love, companionship and other, em, domestic matters, to marry among the nobility brings great assets. You may forge a strong alliance with the bride's family, and a wife may also assist you in manipulating the politics of the clan to your advantage.",
   "minstrel_wife_benefits_2", []],
[anyone, "minstrel_wife_benefits_2", [
  ],
   "What's more, most of the great samurai families of Japan have at some point intermarried with court nobility, which would boost your own claim to rule -- should you ever choose to assert it...",
   "minstrel_prequestions", []],
[anyone, "minstrel_spouse_benefits", [
  (troop_get_type, ":is_female", "trp_player"),
  (eq, ":is_female", 1),
  ],
   "Ah! You are quite the romantic, I see! Well, aside from the obvious benefits of love, companionship and other, em, domestic matters, to marry among the nobility brings great assets. You may have access to the groom's castles and properties, and be able to work with him to advance both of your standings in the clan.",
   "minstrel_wife_benefits_2", []],
[anyone, "minstrel_player_advice_meet", [
   ], "Every so often, a samurai lord of Japan will hold a feast. In towns they will often be accompanied by tournaments, and in castles they will be accompanied by hunts. The feasts provide a chance for the lords to repair some of the rivalries that may undermine the strength of the clan. They also provide an opportunity for families to show off their eligible daughters, and ladies will often be allowed to mingle unsupervised with the guests.",
   "minstrel_player_advice_meet_2", []],
[anyone, "minstrel_player_advice_meet_2", [
   ], "If you have the opportunity, you may attempt to pay the lady a compliment. This indicates to her that you are a potential suitor, and she will usually know if she wishes you to continue your suit. Incidentally, if you come to her fresh from having distinguished yourself in the tournament or in the hunt, then you may make a stronger first impression than otherwise.",
   "minstrel_prequestions", []],
[anyone, "minstrel_player_advice_woo", [
   ], "To woo a lady takes a certain amount of time and patience, and several meetings spaced over a period of months. A lady who is interested in you will often find ways of letting you know if she wishes you to come visit her. Alternately, you may simply go and ask her father or brother for permission. If you do not have permission from her guardian, it may be possible to arrange an assignation through other means.",
   "minstrel_player_advice_woo_2", []],
[anyone, "minstrel_player_advice_woo_2", [
   ], "Having arranged an assignment, you may then attempt to charm her and win her favor. Perhaps one of the most difficult aspects of this is finding a topic of conversation. Most Japanese noblewomen lead a cloistered life, at least until they are married, and thus will have little to say that will interest you. On other hand, she will soon tire of hearing of your own deeds in the outside world.",
   "minstrel_player_advice_woo_3", []],
[anyone, "minstrel_player_advice_woo_3", [
   ], "One time-tested mode of courtship is simply to recite a popular poem, and discuss it. This way, you are both on an equal footing, and neither will have an advantage in knowledge or experience. Of course, different ladies will have different tastes in poetry.",
   "minstrel_player_advice_woo_4", []],
[anyone, "minstrel_player_advice_woo_4", [
   ], "At some point, you will be able to discuss directly the issue of marriage. She will then let you know if you measure up to what she wants in a husband. Some ladies will coolly assess who is the most prestigious of her suitors, others will be guided by their passions. Some will look to your companions, to see whether you are the kind of husband who will treat her as an equal, while others will follow the lead of their fathers.",
   "minstrel_player_advice_woo_5", []],
[anyone, "minstrel_player_advice_woo_5", [
   ], "At any rate, it is a challenging business -- and do not forget, you may find that your suit prospers with a lady, only to have it falter on a father's political ambitions. So you must ask yourself: are you willing to risk disappointment and heartbreak? Alternately, are you willing to throw away your standing in society, to make enemies of allies, in pursuit of a forbidden love? Because if you are, then perhaps some day we will write poems about you.",
   "minstrel_prequestions", []],
[anyone|plyr, "minstrel_courtship_questions_2", [],
   "What is it that you poets and musicians do again?",
   "minstrel_job_description", []],
[anyone, "minstrel_job_description", [],
   "I compose and write songs for the lords of the land, and their ladies. Sometimes I sing about war, sometimes about the virtues of kings, and sometimes, for the more sophisticated audiences, about the virtues of sake. For most audiences, however, I sing of love.", "minstrel_courtship_prequestions", []],
[anyone|plyr, "minstrel_courtship_questions_2", [],
   "No, that is all.",
   "minstrel_pretalk", []],
[anyone, "minstrel_prequestions", [
   ], "Do you have any other questions?",
   "minstrel_courtship_questions_2", []],
[anyone, "minstrel_pretalk", [],
   "Is there anything else?",
   "minstrel_1", []],
[anyone|plyr, "farmer_from_bandit_village_1", [
  ##diplomacy start+ either gender
  ],# "man" -> "{reg65?woman:man}"
   "What is the matter, my good {reg65?woman:man}?", "farmer_from_bandit_village_2", []],
[anyone|plyr, "farmer_from_bandit_village_1", [],
   "What are you burbling about peasant? Speak out.", "farmer_from_bandit_village_2", []],
[anyone, "farmer_from_bandit_village_2", [
   (assign, ":lord_is_player", 0),
   (try_begin),
      (party_slot_eq, "$temp", slot_town_lord, "trp_player"),
      (store_faction_of_party, ":village_faction", "$temp"),
      (this_or_next|eq, ":village_faction", "$players_kingdom"),
         (eq, ":village_faction", "fac_player_supporters_faction"),
      (assign, ":lord_is_player", 1),
   (try_end),
   (neq, ":lord_is_player", 0),

  (call_script, "script_dplmc_print_subordinate_says_sir_madame_to_s0"),
  ],
   "A band of brigands have taken refuge in our village. They take everything we have, force us to serve them, and do us much evil.\
 If one of us so much as breathes a word of protest, they kill the poor soul on the spot right away.\
 Our lives have become unbearable. I risked my skin and ran away to find someone who can help us.\
 Please {s0}, you are a {man/lady} of valor and a fearsome warrior, with many friends and soldiers at your service.\
 If there is anyone who can help us, it's you.", "farmer_from_bandit_village_5", [(assign, "$temp", 0)]],
[anyone, "farmer_from_bandit_village_2", [],
   "A band of brigands have taken refuge in our village. They take everything we have, force us to serve them, and do us much evil.\
 If one of us so much as breathes a word of protest, they kill the poor soul on the spot right away.\
 Our lives have become unbearable. I risked my skin and ran away to find someone who can help us.", "farmer_from_bandit_village_3", []],
[anyone|plyr, "farmer_from_bandit_village_3", [
     (assign, reg0, 0),
	  (try_begin),
	     (gt, "$temp", 1),
		  (party_slot_ge, "$temp", slot_town_lord, 1),
		  (party_get_slot, ":town_lord", "$temp", slot_town_lord),
		  (troop_slot_ge, ":town_lord", slot_troop_met, 1),
		  (call_script, "script_dplmc_store_troop_is_female", ":town_lord"),
	  (try_end),
  ],
   "Why don't you go to the {reg0?mistress:lord} of your village? {reg0?She:He} should take care of the vermin.", "farmer_from_bandit_village_4", []],
[anyone, "farmer_from_bandit_village_4", [
  (gt, "$temp", 1),
  (party_slot_ge, "$temp", slot_town_lord, 1),
  (party_get_slot, ":town_lord", "$temp", slot_town_lord),
  (troop_slot_ge, ":town_lord", slot_troop_prisoner_of_party, 0),
  (call_script, "script_dplmc_print_commoner_at_arg1_says_sir_madame_to_s0", "$g_encountered_party"),
  (call_script, "script_dplmc_store_troop_is_female", ":town_lord"),
  (assign, reg1, "$temp_2"),
  ],
   "Our {reg0?lady:lord} is imprisoned, so we cannot go to {reg0?her:him} for protection.\
 Please {s0}, you {reg1?are:look like} a {man/lady} of valor, {reg1?with:and you have no doubt} many friends and soldiers at your service. \
 If there is anyone who can help us, it's you.", "farmer_from_bandit_village_5", [(assign, "$temp", 0)]],
[anyone, "farmer_from_bandit_village_4", [
  (gt, "$temp", 1),
  (neg|party_slot_ge, "$temp", slot_town_lord, 1),
  (call_script, "script_dplmc_print_commoner_at_arg1_says_sir_madame_to_s0", "$g_encountered_party"),
  (assign, reg1, "$temp_2"),
  ],
   "We have no lord, so we cannot go to him for protection.\
 Please {s0}, you {reg1?are:look like} a {man/lady} of valor, {reg1?with:and you have no doubt} many friends and soldiers at your service. \
 If there is anyone who can help us, it's you.", "farmer_from_bandit_village_5", [(assign, "$temp", 0)]],
[anyone, "farmer_from_bandit_village_4", [
  (call_script, "script_dplmc_print_commoner_at_arg1_says_sir_madame_to_s0", "$g_encountered_party"),
  (party_get_slot, ":town_lord", "$temp", slot_town_lord),
  (call_script, "script_dplmc_store_troop_is_female", ":town_lord"),
  (assign, reg1, "$temp_2"),
  ],
   "I did, {s0}, but our {reg0?lady:lord}'s {reg0?servants:men} did not let me see {reg0?her:him} and said {reg0?she:he} was occupied with more important matters and that we should deal with our own problem ourselves.\
 Please {s0}, you {reg1?are:look like} a {man/lady} of valor and a fearsome warrior, {reg1?with:and you have no doubt} many friends and soldiers at your service. \
 If there is anyone who can help us, it's you.", "farmer_from_bandit_village_5", [(assign, "$temp", 0)]],
[anyone|plyr, "farmer_from_bandit_village_5", [],
   "Very well, I'll help you. Where is this village?", "farmer_from_bandit_village_accepted", []],
[anyone|plyr, "farmer_from_bandit_village_5", [],
   "I can't be bothered with this right now.", "farmer_from_bandit_village_denied", []],
[anyone|plyr, "farmer_from_bandit_village_5", [(eq, "$temp", 0)],
   "Why would I fight these bandits? What's in it for me?", "farmer_from_bandit_village_barter", []],
[anyone, "farmer_from_bandit_village_accepted", [##diplomacy start+
    (call_script, "script_dplmc_print_commoner_at_arg1_says_sir_madame_to_s0", "$g_encountered_party"),
  ],#Next line, replace {sir/madam} with {s0}
   #"God bless you, {sir/madam}. Our village is {s7}. It is not too far from here.", "close_window",
   "God bless you, {s0}. Our village is {s7}. It is not too far from here.", "close_window",
   ##diplomacy end+
   [(quest_get_slot, ":target_center", "qst_eliminate_bandits_infesting_village", slot_quest_target_center),
    (str_store_party_name_link,s7,":target_center"),
    (setup_quest_text, "qst_eliminate_bandits_infesting_village"),
    (str_store_string, s2, "@A villager from {s7} begged you to save their village from the bandits that took refuge there."),
    (call_script, "script_start_quest", "qst_eliminate_bandits_infesting_village", "$g_talk_troop"),
    ]],
[anyone, "farmer_from_bandit_village_denied", [],"As you say {sir/madam}. Forgive me for bothering you.", "close_window", []],
[anyone, "farmer_from_bandit_village_barter", [##diplomacy start+
  (call_script, "script_dplmc_print_commoner_at_arg1_says_sir_madame_to_s0", "$g_encountered_party"),
    ],#Next line, replace {sir/madam} with {s0}
   "We are but poor farmers {s0}, and the bandits have already got most of what we have on this world.\
 but we'll be glad to share with you whatever we have got.\
 And we'll always be in your gratitude if you help us.", "farmer_from_bandit_village_5", [(assign, "$temp", 1)]],
[anyone|plyr,"novicemaster_finish_training", [], "Thank you master.", "novicemaster_finish_training_2",[]],
[anyone,"novicemaster_finish_training_2", [], "I wish you good luck in the tournaments. And, don't forget,\
  if you want to practice your swordwork anytime, just come and say the word.", "close_window",[]],
[anyone|plyr,"novicemaster_are_you_ready", [], "Yes I am.", "novicemaster_ready_to_fight",[]],
[anyone,"novicemaster_ready_to_fight", [], "Here you go then. Good luck.", "close_window",
   [
     (assign, "$training_fight_won", 0),
     (assign, "$waiting_for_training_fight_result", 1),
     (modify_visitors_at_site, "$g_training_ground_melee_training_scene"),
     (reset_visitors),
     (assign, reg0, 0),
     (assign, reg1, 1),
     (assign, reg2, 2),
     (assign, reg3, 3),
     (shuffle_range, 0, 4),
     (set_visitor, reg0, "trp_player"),
     (set_visitor, reg1, "$novicemaster_opponent_troop"),
     (set_visitor, 4, "$g_talk_troop"),
     (set_jump_mission, "mt_training_ground_trainer_training"),
     (jump_to_scene, "$g_training_ground_melee_training_scene"),
     ]],
[anyone|plyr,"novicemaster_are_you_ready", [], "Just a minute. I am not ready yet.", "novicemaster_not_ready",[]],
[anyone,"novicemaster_not_ready", [], "Hey, You will never make it if you don't practice.", "close_window",[]],
[anyone,"start_craftsman_soon", [
  ],
   "Good day, my {lord/lady}. We hope to begin production in about {reg4} days", "close_window",[]],
[anyone,"master_craftsman_pretalk", [],
   "Very good, my {lord/lady}. Do you require anything else?", "master_craftsman_talk",[]],
[anyone|plyr,"master_craftsman_talk", [],
   "Let's go over the accounts.", "master_craftsman_accounts",[]],
[anyone|plyr,"master_craftsman_talk", [],
   "Let's check the inventories.", "master_craftsman_pretalk",[
   (change_screen_loot, "$g_talk_troop"),
   ]],
[anyone|plyr,"master_craftsman_talk", [
  (party_slot_eq, "$g_encountered_party", slot_center_player_enterprise_production_order, 1),
  ],
   "I'd like you to sell goods as they are produced.", "master_craftsman_pretalk",[
  (party_set_slot, "$g_encountered_party", slot_center_player_enterprise_production_order, 0),
   ]],
[anyone|plyr,"master_craftsman_talk", [
  (party_slot_eq, "$g_encountered_party", slot_center_player_enterprise_production_order, 0),
  ],
   "I'd like you to keep all goods in the warehouse until I arrive.", "master_craftsman_pretalk",[
  (party_set_slot, "$g_encountered_party", slot_center_player_enterprise_production_order, 1),
   ]],
[anyone,"master_craftsman_accounts", [
  ], "We currently produce {s3} worth {reg1} mon each week, while the quantity of {s4} needed to manufacture it costs {reg2}, and labor and upkeep are {reg3}.{s9} This means that we theoretically make a {s12} of {reg0} mon a week, assuming that we have no raw materials in the inventories, and that we sell directly to the market.", "master_craftsman_pretalk",
  [
    (party_get_slot, ":item_produced", "$g_encountered_party", slot_center_player_enterprise),
    (call_script, "script_process_player_enterprise", ":item_produced", "$g_encountered_party"),

    (try_begin),
	  (ge, reg0, 0),
	  (str_store_string, s12, "str_profit"),
    (else_try),
	  (str_store_string, s12, "str_loss"),
    (try_end),

    (str_store_item_name, s3, ":item_produced"),
    (item_get_slot, ":primary_raw_material", ":item_produced", slot_item_primary_raw_material),
    (str_store_item_name, s4, ":primary_raw_material"),

    (item_get_slot, ":secondary_raw_material", ":item_produced", slot_item_secondary_raw_material),
    (str_clear, s9),
    (try_begin),
	  (gt, ":secondary_raw_material", 0),
	  (str_store_item_name, s11, ":secondary_raw_material"),
	  (str_store_string, s9, "str_describe_secondary_input"),
    (try_end),
  ]],
[anyone|plyr,"master_craftsman_talk", [
  ], "Could you explain my options related to production?", "master_craftsman_production_options",[]],
[anyone,"master_craftsman_production_options", [
  (str_store_party_name, s5, "$g_encountered_party"),
  ], "Certainly, my {lord/lady}. Most of the time, the most profitable thing for you to do would be to let us buy raw materials and sell the finished goods directly to the market. Because of our longstanding relations with the local merchants, we can usually get a very good price.", "master_craftsman_production_options_2",[]],
[anyone,"master_craftsman_production_options_2", [
  (str_store_party_name, s5, "$g_encountered_party"),
  ], "However, if you find that you can acquire raw materials cheaper outside {s5}, you may place them in the inventories, and we will use them instead of buying from the market. Likewise, if you feel that you can get a better price for the finished goods elsewhere, then you may ask us to deposit what we produce in our warehouses for you to take.", "master_craftsman_pretalk",[]],
[anyone|plyr,"master_craftsman_talk", [
  ], "It will no longer be possible for me to continue operating this shop.", "master_craftsman_auction_price",[]],
[anyone,"master_craftsman_auction_price", [
  (party_get_slot, ":item_produced", "$g_encountered_party", slot_center_player_enterprise),
  (item_get_slot, ":base_price",":item_produced", slot_item_base_price),
  (item_get_slot, ":number_runs", ":item_produced", slot_item_output_per_run),
  (store_mul, "$liquidation_price", ":base_price", ":number_runs"),
  (val_mul, "$liquidation_price", 4),

  (troop_get_inventory_capacity, ":total_capacity", "$g_talk_troop"),
  (try_for_range, ":capacity_iterator", 0, ":total_capacity"),
		(troop_get_inventory_slot, ":item_in_slot", "$g_talk_troop", ":capacity_iterator"),
		(gt, ":item_in_slot", 0),
		(item_get_slot, ":price_for_inventory_item", ":item_in_slot", slot_item_base_price),
#		(troop_inventory_slot_get_item_amount, ":item_ammo", "$g_talk_troop", ":capacity_iterator"),
#		(troop_inventory_slot_get_item_max_amount, ":item_max_ammo", "$g_talk_troop", ":capacity_iterator"),
#		(try_begin),
#			(lt, ":item_ammo", ":item_max_ammo"),
#			(val_mul, ":price_for_inventory_item", ":item_ammo"),
#			(val_div, ":price_for_inventory_item", ":item_max_ammo"),
#		(try_end),

        (store_sub, ":item_slot_no", ":item_in_slot", trade_goods_begin),
        (val_add, ":item_slot_no", slot_town_trade_good_prices_begin),
        (party_get_slot, ":index", "$g_encountered_party", ":item_slot_no"),
		(val_mul, ":price_for_inventory_item", ":index"),
		(val_div, ":price_for_inventory_item", 1200),
		#modify by site
		#divide by 1200 not 1000
		(val_add, "$liquidation_price", ":price_for_inventory_item"),
  (try_end),

  (assign, reg4, "$liquidation_price"),

  ], "A pity, my {lord/lady}. If we sell the land and the equipment, and liquidate the inventories, I estimate that we can get {reg4} mon.", "master_craftsman_auction_decide",[]],
[anyone|plyr,"master_craftsman_auction_decide", [
  ], "That sounds reasonable. Please proceed with the sale.", "master_craftsman_liquidation",[
  (troop_add_gold, "trp_player", "$liquidation_price"),
  (troop_clear_inventory, "$g_talk_troop"),
  (party_set_slot, "$g_encountered_party", slot_center_player_enterprise, 0),
  (party_set_slot, "$g_encountered_party", slot_center_player_enterprise_production_order, 0),

  ]],
[anyone|plyr,"master_craftsman_auction_decide", [
  ], "Hmm. Let's hold off on that.", "master_craftsman_pretalk",[]],
[anyone,"master_craftsman_liquidation", [
  ], "As you wish. It was an honor to have been in your employ.", "close_window",[
    (finish_mission),
  ]],
[anyone|plyr,"master_craftsman_talk", [
  (eq, 1, 0),
  ], "{!}As you wish, {sir/my lady}. It was an honor to work in your employ.", "close_window",[]],
[anyone|plyr,"master_craftsman_talk", [],
   "That is all for now.", "close_window",[]],
[anyone|plyr ,"move_cattle_herd_failed", [],
   "I am sorry. But I was attacked on the way.", "move_cattle_herd_failed_2",[]],
[anyone|plyr ,"move_cattle_herd_failed", [],
   "I am sorry. The stupid animals wandered off during the night.", "move_cattle_herd_failed_2",[]],
[anyone,"move_cattle_herd_failed_2", [],
   "Well, it was your responsibility to deliver that herd safely, no matter what.\
 You should know that the owner of the herd demanded to be compensated for his loss, and I had to pay him 1000 mon.\
 So you now owe me that money.", "merchant_ask_for_debts",
   [(assign, "$debt_to_merchants_guild", 1000),
    (call_script, "script_end_quest", "qst_move_cattle_herd"),]],
[anyone,"destroy_lair_quest_brief", [
     (eq,"$random_quest_no", "qst_destroy_bandit_lair"),
	 (quest_get_slot, ":bandit_lair", "qst_destroy_bandit_lair", slot_quest_target_party),
	 (party_get_template_id, ":bandit_type", ":bandit_lair"),
	 (eq, ":bandit_type", "pt_kinai_rebel_lair"),
	 ],
	#gekokujo "sea raiders" now get mountain hideout
	#"The raiders are likely to have laid up their ships in a well-concealed cove, somewhere along the coastline, preferably next to a small stream where they have some water. The best way to discover its location would be to find a group of sea raiders who appear to be heading back to their base to resupply, and follow them.", "merchant_quest_track_bandit_lair_choice",
	"Bandits such as these will usually operate from mansions in the countryside. The best way to discover its location would be to find a group of rebels who appear to be heading home to resupply, and follow them.", "merchant_quest_track_bandit_lair_choice",
   []],
[anyone,"destroy_lair_quest_brief", [
     (eq,"$random_quest_no", "qst_destroy_bandit_lair"),
	 (quest_get_slot, ":bandit_lair", "qst_destroy_bandit_lair", slot_quest_target_party),
	 (party_get_template_id, ":bandit_type", ":bandit_lair"),
	 (eq, ":bandit_type", "pt_northern_raider_lair"),
	 ],
	#desert bandits now get forest hideout
	#"Bandits such as these usually establish their hideouts in the foothills on the edge of the desert, often in a canyon near a spring. This gives them both water and concealment. The best way to discover its location would be to find a group of desert bandits who appear to be heading back to their base to resupply, and follow them.", "merchant_quest_track_bandit_lair_choice",
	"Bandits such as these will usually set up their encampments far north, where it is cold. The best way to discover its location would be to find a group of warriors who appear to be heading back to their base to resupply, and follow them.", "merchant_quest_track_bandit_lair_choice",
   []],
[anyone,"destroy_lair_quest_brief", [
     (eq,"$random_quest_no", "qst_destroy_bandit_lair"),
	 (quest_get_slot, ":bandit_lair", "qst_destroy_bandit_lair", slot_quest_target_party),
	 (party_get_template_id, ":bandit_type", ":bandit_lair"),
	 (eq, ":bandit_type", "pt_woku_pirate_lair"),
	 ],
	"Bandits such as these will usually establish a base on the coast. The best way to discover its location would be to find a group of pirates who appear to be heading back to their base to resupply, and follow them.", "merchant_quest_track_bandit_lair_choice",
   []],
[anyone,"destroy_lair_quest_brief", [
     (eq,"$random_quest_no", "qst_destroy_bandit_lair"),
	 (quest_get_slot, ":bandit_lair", "qst_destroy_bandit_lair", slot_quest_target_party),
	 (party_get_template_id, ":bandit_type", ":bandit_lair"),
	 (eq, ":bandit_type", "pt_shinano_rebel_lair"),
	 ],
	"Bandits such as these usually operate in a far-flung mansion deep in the woods, in a hidden valley. The best way to discover its location would be to find a group of rebels who appear to be heading back home to resupply, and follow them.", "merchant_quest_track_bandit_lair_choice",
   []],
[anyone,"destroy_lair_quest_brief", [
     (eq,"$random_quest_no", "qst_destroy_bandit_lair"),
	 (quest_get_slot, ":bandit_lair", "qst_destroy_bandit_lair", slot_quest_target_party),
	 (party_get_template_id, ":bandit_type", ":bandit_lair"),
	 (eq, ":bandit_type", "pt_seto_pirate_lair"),
	 ],
	#gekokujo "steppe bandits" now get mountain hideout
	#"Bandits such as these will usually set up their encampments in the woodland on the steppe, where they have some concealment. The best way to discover its location would be to find a group of steppe bandits who appear to be heading back to their base to resupply, and follow them.", "merchant_quest_track_bandit_lair_choice",
	"Bandits such as these will usually establish a base among the small islands of the inland sea. This makes them difficult to assault. The best way to discover its location would be to find a group of pirates who appear to be heading back to their base to resupply, and follow them.", "merchant_quest_track_bandit_lair_choice",
   []],
[anyone,"destroy_lair_quest_brief", [
     (eq,"$random_quest_no", "qst_destroy_bandit_lair"),
	 (quest_get_slot, ":bandit_lair", "qst_destroy_bandit_lair", slot_quest_target_party),
	 (party_get_template_id, ":bandit_type", ":bandit_lair"),
	 (eq, ":bandit_type", "pt_kanto_rebel_lair"),
	 ],
	"Bandits such as these usually operate from out of the way fortified mansions. The best way to discover its location would be to find a group of rebels who appear to be heading back to their mansion to resupply, and follow them.", "merchant_quest_track_bandit_lair_choice",
   []],
[anyone,"destroy_lair_quest_brief", [
     (eq,"$random_quest_no", "qst_destroy_bandit_lair"),
	 (quest_get_slot, ":bandit_lair", "qst_destroy_bandit_lair", slot_quest_target_party),
	 (party_get_template_id, ":bandit_type", ":bandit_lair"),
	 (eq, ":bandit_type", "pt_monk_rebel_lair"),
	 ],
	"Bandits such as these will usually set up their encampments in rural temples, probably fortified. The best way to discover its location would be to find a group of monks who appear to be heading back to their temple to resupply, and follow them.", "merchant_quest_track_bandit_lair_choice",
   []],
[anyone|plyr,"escort_merchant_caravan_quest_brief", [(store_party_size_wo_prisoners, ":party_size", "p_main_party"),
                                                       (quest_get_slot, ":quest_target_amount", "qst_escort_merchant_caravan", slot_quest_target_amount),
                                                       (ge,":party_size",":quest_target_amount"),
                                                       ],
   "Alright. I will escort the caravan.", "merchant_quest_taken",
   [(quest_get_slot, ":quest_target_center", "qst_escort_merchant_caravan", slot_quest_target_center),
    (set_spawn_radius, 1),
    (spawn_around_party,"$g_encountered_party","pt_merchant_caravan"),
    (assign, ":quest_target_party", reg0),
    (party_set_ai_behavior, ":quest_target_party", ai_bhvr_track_party),
    (party_set_ai_object, ":quest_target_party", "p_main_party"),
    (party_set_flags, ":quest_target_party", pf_default_behavior, 0),
    (quest_set_slot, "qst_escort_merchant_caravan", slot_quest_target_party, ":quest_target_party"),
    (quest_set_slot, "qst_escort_merchant_caravan", slot_quest_current_state, 0),
    (str_store_party_name_link, s8, ":quest_target_center"),
    (setup_quest_text, "qst_escort_merchant_caravan"),
    (str_store_string, s2, "@Escort the merchant caravan to the town of {s8}."),
    (call_script, "script_start_quest", "qst_escort_merchant_caravan", "$g_talk_troop"),
    ]],
[anyone|plyr,"escort_merchant_caravan_quest_brief", [(store_party_size_wo_prisoners, ":party_size", "p_main_party"),
                                                       (quest_get_slot, ":quest_target_amount", "qst_escort_merchant_caravan", slot_quest_target_amount),
                                                       (lt,":party_size",":quest_target_amount"),],
   "I am afraid I don't have that many soldiers with me.", "merchant_quest_stall",[]],
[anyone|plyr,"escort_merchant_caravan_quest_brief", [(store_party_size_wo_prisoners, ":party_size", "p_main_party"),
                                                       (quest_get_slot, ":quest_target_amount", "qst_escort_merchant_caravan", slot_quest_target_amount),
                                                       (ge,":party_size",":quest_target_amount"),],
   "Sorry. I can't do that right now", "merchant_quest_stall",[]],
[anyone|plyr,"escort_merchant_caravan_talk", [], "You follow my lead. I'll take you through a safe route.", "merchant_caravan_follow_lead",[]],
[anyone|plyr,"escort_merchant_caravan_talk", [], "You stay here for a while. I'll go ahead and check the road.", "merchant_caravan_stay_here",[]],
[anyone|plyr,"troublesome_bandits_quest_brief", [],
   "Very well. I will hunt down those bandits.", "merchant_quest_taken_bandits",
   [(set_spawn_radius,7),
    (quest_get_slot, ":quest_giver_center", "qst_troublesome_bandits", slot_quest_giver_center),
    (spawn_around_party,":quest_giver_center","pt_troublesome_bandits"),
    (quest_set_slot, "qst_troublesome_bandits", slot_quest_target_party, reg0),
    (store_num_parties_destroyed,"$qst_troublesome_bandits_eliminated","pt_troublesome_bandits"),
    (store_num_parties_destroyed_by_player, "$qst_troublesome_bandits_eliminated_by_player", "pt_troublesome_bandits"),
    (str_store_troop_name, s9, "$g_talk_troop"),
    (str_store_party_name_link, s4, "$g_encountered_party"),
    (setup_quest_text,"qst_troublesome_bandits"),
    (str_store_string, s2, "@Merchant {s9} of {s4} asked you to hunt down the troublesome bandits in the vicinity of the town."),
    (call_script, "script_start_quest", "qst_troublesome_bandits", "$g_talk_troop"),
    ]],
[anyone|plyr,"troublesome_bandits_quest_brief", [],
   "Sorry. I don't have time for this right now.", "merchant_quest_stall",[]],
[anyone|plyr,"kidnapped_girl_quest_brief", [],
      "All right. I will take the ransom money to the bandits and bring back the girl.",
   "kidnapped_girl_quest_taken",[(set_spawn_radius, 4),
                                 (quest_get_slot, ":quest_target_center", "qst_kidnapped_girl", slot_quest_target_center),
                                 (quest_get_slot, ":quest_target_amount", "qst_kidnapped_girl", slot_quest_target_amount),
                                 (spawn_around_party,":quest_target_center","pt_bandits_awaiting_ransom"),
                                 (assign, ":quest_target_party", reg0),
                                 (quest_set_slot, "qst_kidnapped_girl", slot_quest_target_party, ":quest_target_party"),
                                 (party_set_ai_behavior, ":quest_target_party", ai_bhvr_hold),
                                 (party_set_ai_object, ":quest_target_party", "p_main_party"),
                                 (party_set_flags, ":quest_target_party", pf_default_behavior, 0),
                                 (call_script, "script_troop_add_gold", "trp_player", ":quest_target_amount"),
                                 (assign, reg12, ":quest_target_amount"),
                                 (str_store_troop_name, s1, "$g_talk_troop"),
                                 (str_store_party_name_link, s4, "$g_encountered_party"),
                                 (str_store_party_name_link, s3, ":quest_target_center"),
                                 (setup_quest_text, "qst_kidnapped_girl"),
                                 (str_store_string, s2, "@The chief merchant of {s4} gave you {reg12} mon to pay the ransom of a girl kidnapped by bandits.\
 You are to meet the bandits near {s3} and pay them the ransom fee.\
 After that you are to bring the girl back to {s4}."),
                                 (call_script, "script_start_quest", "qst_kidnapped_girl", "$g_talk_troop"),
                                 ]],
[anyone,"kidnapped_girl_quest_taken", [], "Good. I knew we could trust you at this.\
 Here is the ransom money, {reg12} mon.\
 Count it before taking it.\
 And please, don't attempt to do anything rash.\
 Keep in mind that the girl's well being is more important than anything else...", "close_window",
   []],
[anyone|plyr,"kidnapped_girl_quest_brief", [],
   "Sorry. I don't have time for this right now.", "merchant_quest_stall",[]],
[trp_kidnapped_girl|plyr,"kidnapped_girl_liberated_map", [], "Yes. Come with me. We are going home.", "kidnapped_girl_liberated_map_2a",[]],
[trp_kidnapped_girl,"kidnapped_girl_liberated_map_2a", [(neg|party_can_join)], "Unfortunately. You do not have room in your party for me.", "close_window",[(assign, "$g_leave_encounter",1)]],
[trp_kidnapped_girl,"kidnapped_girl_liberated_map_2a", [], "Oh really? Thank you so much!",
   "close_window", [(party_join),
                    (quest_set_slot, "qst_kidnapped_girl", slot_quest_current_state, 3),
                    (assign, "$g_leave_encounter",1)]],
[trp_kidnapped_girl|plyr,"kidnapped_girl_liberated_map", [], "Wait here a while longer. I'll come back for you.", "kidnapped_girl_liberated_map_2b",[]],
[trp_kidnapped_girl,"kidnapped_girl_liberated_map_2b", [], "Oh, please {sir/madam}, do not leave me here all alone!", "close_window",[(assign, "$g_leave_encounter",1)]],
[trp_kidnapped_girl|plyr,"kidnapped_girl_liberated_battle", [], "Yes. Come with me. We are going home.", "kidnapped_girl_liberated_battle_2a",[]],
[trp_kidnapped_girl,"kidnapped_girl_liberated_battle_2a", [(neg|hero_can_join, "p_main_party")], "Unfortunately. You do not have room in your party for me.", "kidnapped_girl_liberated_battle_2b",[]],
[trp_kidnapped_girl,"kidnapped_girl_liberated_battle_2a", [], "Oh really? Thank you so much!",
   "close_window",[(party_add_members, "p_main_party","trp_kidnapped_girl",1),
                   (quest_set_slot, "qst_kidnapped_girl", slot_quest_current_state, 3),
                   ]],
[trp_kidnapped_girl|plyr,"kidnapped_girl_liberated_battle", [], "Wait here a while longer. I'll come back for you.", "kidnapped_girl_liberated_battle_2b",[]],
[trp_kidnapped_girl,"kidnapped_girl_liberated_battle_2b", [], "Oh, please {sir/madam}, do not leave me here all alone!",
   "close_window", [(add_companion_party,"trp_kidnapped_girl"),
                    (assign, "$g_leave_encounter",1)]],
[party_tpl|pt_bandits_awaiting_ransom|plyr, "bandits_awaiting_ransom_intro_1", [(store_troop_gold, ":cur_gold"),
                                                                                  (quest_get_slot, ":quest_target_amount", "qst_kidnapped_girl", slot_quest_target_amount),
                                                                                  (ge, ":cur_gold", ":quest_target_amount")
                                                                                  ],
   "Here, take the money. Just set the girl free.", "bandits_awaiting_ransom_pay",[]],
[party_tpl|pt_bandits_awaiting_ransom, "bandits_awaiting_ransom_pay", [],
   "Heh. You've brought the money all right.\
 You can take the girl now.\
 It was a pleasure doing business with you...", "close_window",
   [(quest_get_slot, ":quest_target_amount", "qst_kidnapped_girl", slot_quest_target_amount),
    (quest_get_slot, ":quest_target_party", "qst_kidnapped_girl", slot_quest_target_party),
    (quest_get_slot, ":quest_target_center", "qst_kidnapped_girl", slot_quest_target_center),
    (troop_remove_gold, "trp_player", ":quest_target_amount"),
    (remove_member_from_party, "trp_kidnapped_girl", ":quest_target_party"),
    (set_spawn_radius, 1),
    (spawn_around_party, ":quest_target_party", "pt_kidnapped_girl"),
    (assign, ":girl_party", reg0),
    (party_set_ai_behavior, ":girl_party", ai_bhvr_hold),
    (party_set_flags, ":girl_party", pf_default_behavior, 0),
    (quest_set_slot, "qst_kidnapped_girl", slot_quest_current_state, 2),
    (party_set_ai_behavior, ":quest_target_party", ai_bhvr_travel_to_party),
    (party_set_ai_object, ":quest_target_party", ":quest_target_center"),
    (party_set_flags, ":quest_target_party", pf_default_behavior, 0),
    (add_gold_to_party, ":quest_target_amount", ":quest_target_party"),
    (assign, "$g_leave_encounter",1),
    ]],
[anyone|plyr, "bandits_awaiting_ransom_intro_1", [],
   "No way! You release the girl first.", "bandits_awaiting_ransom_b",[]],
[anyone, "bandits_awaiting_ransom_b", [],
   "You fool! Stop playing games and give us the money! ", "bandits_awaiting_ransom_b2",[]],
[anyone|plyr, "bandits_awaiting_ransom_b2", [(store_troop_gold, ":cur_gold"),
                                               (quest_get_slot, ":quest_target_amount", "qst_kidnapped_girl", slot_quest_target_amount),
                                               (ge, ":cur_gold", ":quest_target_amount")],
   "All right. Here's your money. Let the girl go now.", "bandits_awaiting_ransom_pay",[]],
[anyone|plyr, "bandits_awaiting_ransom_b2", [],
   "I had left the money in a safe place. Let me go fetch it.", "bandits_awaiting_ransom_no_money",[]],
[anyone, "bandits_awaiting_ransom_no_money", [],
   "Are you testing our patience or something?  Go and bring that money here quickly.", "close_window",[(assign, "$g_leave_encounter",1)]],
[anyone|plyr, "bandits_awaiting_ransom_b2", [],
   "I have no intention to pay you anything. I demand that you release the girl now!", "bandits_awaiting_ransom_fight",[]],
[anyone, "bandits_awaiting_ransom_fight", [],
   "You won't be demanding anything when you're dead.", "close_window",[(encounter_attack),]],
[anyone|plyr,"bandits_awaiting_remeet", [],
   "Sorry to bother you. I'll be on my way now.", "close_window",[(assign, "$g_leave_encounter",1)]],
[anyone|plyr,"bandits_awaiting_remeet", [],
   "We have one more business. You'll give the money back to me.", "bandits_awaiting_remeet_2",[]],
[anyone,"bandits_awaiting_remeet_2", [],
   "Oh, that business! Of course. Let us get down to it.", "close_window",[(encounter_attack)]],
[anyone|plyr,"kidnapped_girl_encounter_1", [], "Yes. Come with me. I'll take you home.", "kidnapped_girl_join",[]],
[anyone,"kidnapped_girl_join", [(neg|party_can_join)], "Unfortunately. You do not have room in your party for me.", "close_window",[(assign, "$g_leave_encounter",1)]],
[anyone,"kidnapped_girl_join", [], "Oh, thank you so much!",
   "close_window",[(party_join),
                   (quest_set_slot, "qst_kidnapped_girl", slot_quest_current_state, 3),
                   (assign, "$g_leave_encounter",1)]],
[anyone|plyr,"kidnapped_girl_encounter_1", [], "Wait here a while longer. I'll come back for you.", "kidnapped_girl_wait",[]],
[anyone,"kidnapped_girl_wait", [], "Oh, please {sir/madam}, do not leave me here all alone!", "close_window",[(assign, "$g_leave_encounter",1)]],
[anyone,"lost_kidnapped_girl", [],
   "Oh no! How am I going to tell this to my friend?", "lost_kidnapped_girl_2",[]],
[anyone|plyr,"lost_kidnapped_girl_2", [],
   "I'm sorry. I could do nothing about it.", "lost_kidnapped_girl_3",[]],
[anyone,"lost_kidnapped_girl_3", [],
   "You let me down {playername}. I had trusted you.\
 I will let people know of your incompetence at this task.\
 Also, I want back that {reg8} mon I gave you as the ransom fee.", "lost_kidnapped_girl_4",
   [(quest_get_slot, reg8, "qst_kidnapped_girl", slot_quest_target_amount),
    (try_for_parties, ":cur_party"),
      (party_count_members_of_type, ":num_members", ":cur_party", "trp_kidnapped_girl"),
      (gt, ":num_members", 0),
      (party_remove_members, ":cur_party", "trp_kidnapped_girl", 1),
      (party_remove_prisoners, ":cur_party", "trp_kidnapped_girl", 1),
    (try_end),
    (call_script, "script_end_quest", "qst_kidnapped_girl"),
    (call_script, "script_change_troop_renown", "trp_player", -5),
    ]],
[anyone|plyr, "lost_kidnapped_girl_4", [(store_troop_gold,":gold"),
                                          (quest_get_slot, ":quest_target_amount", "qst_kidnapped_girl", slot_quest_target_amount),
                                          (ge,":gold",":quest_target_amount"),
                                          ],
   "Of course. Here you are...", "merchant_quest_about_job_5a",[(quest_get_slot, ":quest_target_amount", "qst_kidnapped_girl", slot_quest_target_amount),
                                                                (troop_remove_gold, "trp_player",":quest_target_amount"),
                                                                ]],
[anyone|plyr,"lost_kidnapped_girl_4", [],
   "Sorry. I don't have that amount with me.", "merchant_quest_about_job_5b",[]],
[anyone,"deal_with_night_bandits_quest_taken", [], "That takes a weight off my shoulders, {playername}.\
 You can expect a fine reward if you come back successful. Just don't get yourself killed, eh?", "mayor_pretalk",[]],
[anyone|plyr,"move_cattle_herd_quest_brief", [],  "Aye, I can take the herd to {s13}.",
   "move_cattle_herd_quest_taken",
   [
     (call_script, "script_create_cattle_herd", "$g_encountered_party", 0),
     (quest_set_slot, "qst_move_cattle_herd", slot_quest_target_party, reg0),
     (str_store_party_name_link, s10,"$g_encountered_party"),
     (quest_get_slot, ":target_center", "qst_move_cattle_herd", slot_quest_target_center),
     (str_store_party_name_link, s13, ":target_center"),
     (quest_get_slot, reg8, "qst_move_cattle_herd", slot_quest_gold_reward),
     (setup_quest_text, "qst_move_cattle_herd"),
     (str_store_string, s2, "@The elder merchant of {s10} asked you to move a cattle herd to {s13}. You will earn {reg8} mon in return."),
     (call_script, "script_start_quest", "qst_move_cattle_herd", "$g_talk_troop"),
     ]],
[anyone|plyr,"move_cattle_herd_quest_brief", [],
   "I am sorry, but no.", "merchant_quest_stall",[]],
[anyone,"move_cattle_herd_quest_taken", [], "Splendid. You can find the herd right outside the town.\
 After you take the animals to {s13}, return back to me and I will give you your pay.", "mayor_pretalk",[]],
[anyone,"goods_merchant_pretalk", [], "Anything else?", "goods_merchant_talk",[]],
[anyone|plyr,"goods_merchant_talk", [], "I want to buy a few items... and perhaps sell some.", "goods_trade_requested",[]],
[anyone,"goods_trade_requested", [], "Sure, sure... Here, have a look at my stock...", "goods_trade_completed",[[change_screen_trade]]],
[anyone,"goods_trade_completed", [], "Anything else?", "goods_merchant_talk",[]],
[anyone|plyr,"goods_merchant_talk", [], "What goods should I buy here to trade with other towns?", "trade_info_request",[]],
[anyone|plyr,"goods_merchant_talk", [], "Nothing. Thanks.", "close_window",[]],
[trp_galeas|plyr,"galeas_talk",
   [[store_num_regular_prisoners,reg(0)],[ge,reg(0),1]],
   "Then you'd better bring your purse. I have got prisoners to sell.", "galeas_sell_prisoners",[]],
[trp_galeas|plyr,"galeas_talk",[], "Not this time. Good-bye.", "close_window",[]],
[trp_galeas,"galeas_sell_prisoners", [],
  "Let me see what you have...", "galeas_sell_prisoners_2",
   [[change_screen_trade_prisoners]]],
[trp_galeas, "galeas_sell_prisoners_2", [], "You take more prisoners, bring them to me. I will pay well.", "close_window",[]],
[anyone|plyr,"disbanded_troop_ask", [], "Yes. Let us ride together.", "disbanded_troop_join",[]],
[anyone|plyr,"disbanded_troop_ask", [], "No. Not at this time.", "close_window",[(assign, "$g_leave_encounter",1)]],
[anyone,"disbanded_troop_join", [[neg|party_can_join]], "Unfortunately. You do not have room in your party for us.", "close_window",[(assign, "$g_leave_encounter",1)]],
[anyone,"disbanded_troop_join", [], "We are at your command.", "close_window",[[party_join],(assign, "$g_leave_encounter",1)]],
[party_tpl|pt_enemy|plyr,"enemy_talk_1", [], "You don't have a chance against me. Give up.", "enemy_talk_2",[]],
[party_tpl|pt_enemy,"enemy_talk_2", [], "I will give up when you are dead!", "close_window",[[encounter_attack]]],
[party_tpl|pt_routed_warriors|plyr, "party_encounter_routed_agents_are_caught", [],
   "Do you think you can run away from me? You will be my prisoner or die!", "party_encounter_routed_agents_are_caught2",
   []],
[party_tpl|pt_routed_warriors|plyr,"party_encounter_routed_agents_are_caught", [],
   "Ok. We'll leave you in peace for this time, do not face with us again.", "close_window", [(assign, "$g_leave_encounter",1)]],
[party_tpl|pt_routed_warriors, "party_encounter_routed_agents_are_caught2",
   [
     #(store_party_size_wo_prisoners, ":routed_party_size", "$g_encountered_party"),
     #(store_party_size_wo_prisoners, ":main_party_size", "p_main_party"),

    # calculate power of routed party
    (assign, ":routed_party_power", 0),
    (party_get_num_companion_stacks, ":num_stacks", "$g_encountered_party"),
    (try_for_range, ":i_stack", 0, ":num_stacks"),
      (party_stack_get_troop_id, ":stack_troop", "$g_encountered_party", ":i_stack"),
      (store_character_level, ":troop_level", ":stack_troop"),
      (try_begin),
        (troop_is_mounted, ":stack_troop"),
        (val_add, ":troop_level", 5),
      (try_end),
      (party_stack_get_size, ":stack_size", "$g_encountered_party", ":i_stack"),
      (val_mul, ":troop_level", ":stack_size"),
      (val_add, ":routed_party_power", ":troop_level"),
    (try_end),

    # calculate power of our party
    (assign, ":main_party_power", 0),
    (party_get_num_companion_stacks, ":num_stacks", "p_main_party"),
    (try_for_range, ":i_stack", 0, ":num_stacks"),
      (party_stack_get_troop_id, ":stack_troop", "p_main_party", ":i_stack"),
      (store_character_level, ":troop_level", ":stack_troop"),
      (try_begin),
        (troop_is_mounted, ":stack_troop"),
        (val_add, ":troop_level", 5),
      (try_end),
      (party_stack_get_size, ":stack_size", "p_main_party", ":i_stack"),
      (val_mul, ":troop_level", ":stack_size"),
      (val_add, ":main_party_power", ":troop_level"),
    (try_end),

    (store_div, ":main_party_power_divided_by_5", ":main_party_power", 5),

    #find num attached parties to routed warriors
    (party_get_num_attached_parties, ":num_attached_parties", "$g_encountered_party"),

    (this_or_next|gt, ":num_attached_parties", 0), #always fight
    (ge, ":routed_party_power", ":main_party_power_divided_by_5"),
    ],
   "Haven't you got any mercy? Ok, we will fight you to the last man!", "close_window",
   []],
[party_tpl|pt_routed_warriors, "party_encounter_routed_agents_are_caught2",
    [
      #(store_party_size_wo_prisoners, ":routed_party_size", "$g_encountered_party"),
      #(store_party_size_wo_prisoners, ":main_party_size", "p_main_party"),

      # calculate power of routed party
      (assign, ":routed_party_population", 0),
      (assign, ":routed_party_power", 0),
      (party_get_num_companion_stacks, ":num_stacks", "$g_encountered_party"),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop", "$g_encountered_party", ":i_stack"),
        (store_character_level, ":troop_level", ":stack_troop"),
        (try_begin),
          (troop_is_mounted, ":stack_troop"),
          (val_add, ":troop_level", 5),
        (try_end),
        (party_stack_get_size, ":stack_size", "$g_encountered_party", ":i_stack"),
        (val_mul, ":troop_level", ":stack_size"),
        (val_add, ":routed_party_power", ":troop_level"),
        (val_add, ":routed_party_population", ":stack_size"),
      (try_end),

      # calculate power of our party
      (assign, ":main_party_power", 0),
      (party_get_num_companion_stacks, ":num_stacks", "p_main_party"),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop", "p_main_party", ":i_stack"),
        (store_character_level, ":troop_level", ":stack_troop"),
        (try_begin),
          (troop_is_mounted, ":stack_troop"),
          (val_add, ":troop_level", 5),
        (try_end),
        (party_stack_get_size, ":stack_size", "p_main_party", ":i_stack"),
        (val_mul, ":troop_level", ":stack_size"),
        (val_add, ":main_party_power", ":troop_level"),
      (try_end),

      (store_div, ":main_party_power_divided_by_5", ":main_party_power", 5),
      (lt, ":routed_party_power", ":main_party_power_divided_by_5"),

      (store_party_size_wo_prisoners, ":routed_party_size", "$g_encountered_party"),
      (assign, reg3, ":routed_party_size"),

      (try_begin),
        (gt, ":routed_party_population", 1),
        (str_store_string, s1, "str_we_resign"),
      (else_try),
        (str_store_string, s1, "str_i_resign"),
      (try_end),
    ],
    "{s1}", "close_window",
    [(assign,"$g_enemy_surrenders", 1),
     (call_script, "script_party_wound_all_members", "$g_encountered_party"),
     (call_script, "script_party_copy", "p_total_enemy_casualties", "$g_encountered_party"),
     #(change_screen_exchange_with_party, "$g_encountered_party"),
     ]],
[anyone|plyr,"player_castle_guard_talk", [], "How goes the watch, soldier?", "player_castle_guard_talk_2",[]],
[anyone,"player_castle_guard_talk_2", [], "All is quiet {s0}. Nothing to report.", "player_castle_guard_talk_3",[]],
[anyone|plyr,"player_castle_guard_talk_3", [], "Good. Keep your eyes open.", "close_window",[]],
[anyone|plyr,"hall_guard_talk", [], "Stay on duty and let me know if anyone comes to see me.", "hall_guard_duty",[]],
[anyone,"hall_guard_duty", [(call_script, "script_dplmc_print_subordinate_says_sir_madame_to_s0"),], "Yes, {s0}. As you wish.", "close_window",[]],
[anyone|plyr,"hall_guard_talk", [
  (eq, 1, 0),
  ], "I want you to arrest this man immediately!", "hall_guard_arrest",[]],
[anyone,"hall_guard_arrest", [(call_script, "script_dplmc_print_subordinate_says_sir_madame_to_s0"),], "Who do you want arrested {s0}?", "hall_guard_arrest_2",[]],
[anyone|plyr,"hall_guard_arrest_2", [], "Ah, never mind my high spirits.", "close_window",[]],
[anyone|plyr,"hall_guard_arrest_2", [], "Forget it. I will find another way to deal with this.", "close_window",[]],
[anyone|plyr,"regular_member_talk", [], "Tell me about yourself", "view_regular_char_requested",[]],
[anyone,"view_regular_char_requested", [(call_script, "script_dplmc_print_subordinate_says_sir_madame_to_s0"),], "Aye {s0}. Let me tell you all there is to know about me.", "do_regular_member_view_char",[[change_screen_view_character]]],
[anyone,"do_regular_member_view_char", [], "Anything else?", "regular_member_talk",[]],
[anyone|plyr,"regular_member_talk", [],
   "Let me see your equipment.", "dplmc_view_regular_inventory", []
  ],
[anyone|plyr,"regular_member_talk", [], "Nothing. Keep moving.", "close_window",[]],
[anyone|plyr,"party_encounter_hostile_attacker", [
                    ],
   "We will fight you to the end!", "close_window", []],
[anyone|plyr,"party_encounter_hostile_attacker", [
                    ],
   "Don't attack! We surrender.", "close_window", [(assign,"$g_player_surrenders",1)]],
[anyone|plyr,"party_encounter_hostile_defender", [],
   "Surrender or die!", "party_encounter_hostile_ultimatum_surrender", [

       ]],
[anyone,"party_encounter_hostile_ultimatum_surrender", [],
   "{s43}", "close_window", [
       (call_script, "script_lord_comment_to_s43", "$g_talk_troop", "str_lord_challenged_default"),
       ]],
[anyone|plyr,"party_encounter_hostile_defender", [],
   "Nothing. We'll leave you in peace.", "close_window", [(assign, "$g_leave_encounter",1)]],
[anyone|plyr, "fort_conquest_response", [
      (store_sub, ":offset", "$current_town", forts_begin),
      (store_add, ":conquer_response", "str_gekokujo_fort_1_deputy_conquer_response", ":offset"),
      (str_store_string, s46, ":conquer_response"),
    ], "{s46}","close_window", []],
[anyone, "fort_deputy_discuss", [], "Anything else?","fort_deputy_discuss_options", []],
[anyone|plyr, "fort_deputy_discuss_options", [
      (party_get_slot, ":companion", "$current_town", slot_fort_npc_2),
      (troop_slot_ge, ":companion", slot_troop_met, 1),
	  (str_store_troop_name, s2, ":companion"),
	  (try_begin),
	    (this_or_next|party_slot_eq, "$current_town", slot_fort_npc_2_state, 3), #companion has been recruited
	    (party_slot_eq, "$current_town", slot_fort_npc_2_state, 4), #companion has been promoted to lord
        (str_store_string, s2, "@Would you like to know how {s2} has been doing?"),
	  (else_try),
        (str_store_string, s2, "@I wish to ask about {s2}."), #default request
	  (try_end),
    ], "{s2}", "fort_deputy_discuss_companion", []],
[anyone, "fort_deputy_discuss_companion", [ 
      (store_sub, ":offset", "$current_town", forts_begin),
	  (try_begin),
	    (party_slot_eq, "$current_town", slot_fort_npc_2_state, 4), #companion has been promoted to lord
	    (store_add, ":deputy_talk", "str_gekokujo_fort_1_deputy_ask_companion_promoted", ":offset"),
	  (else_try),
	    (party_slot_eq, "$current_town", slot_fort_npc_2_state, 3), #companion has been recruited
	    (store_add, ":deputy_talk", "str_gekokujo_fort_1_deputy_ask_companion_recruited", ":offset"),
	  (else_try),
	    (party_slot_eq, "$current_town", slot_fort_npc_2_state, 2), #companion has returned temporarily
        (party_get_slot, ":companion", "$current_town", slot_fort_npc_2),
		(str_store_troop_name, s3, ":companion"),
        (assign, ":deputy_talk", "str_gekokujo_fort_deputy_ask_companion_returned"),
	  (else_try),
        (store_add, ":deputy_talk", "str_gekokujo_fort_1_deputy_ask_companion", ":offset"), #default response
	  (try_end),
      (str_store_string, s45, ":deputy_talk"),
    ], "{s45}","fort_deputy_discuss", []],
[anyone|plyr, "fort_deputy_discuss_options", [
      (party_slot_eq, "$current_town", slot_fort_npc_2_state, 1), #this should only show up if you've already asked companion to join
      (party_get_slot, ":companion", "$current_town", slot_fort_npc_2),
      (troop_slot_ge, ":companion", slot_troop_met, 1),
	  (str_store_troop_name, s2, ":companion"),
    ], "I wish for {s2} to join me.", "fort_deputy_discuss_companion_recruit", []],
[anyone, "fort_deputy_discuss_companion_recruit", [ 
      (store_sub, ":offset", "$current_town", forts_begin),
      (store_add, ":deputy_talk", "str_gekokujo_fort_1_deputy_ask_companion_recruit", ":offset"),
      (str_store_string, s45, ":deputy_talk"),
    ], "{s45}","fort_deputy_discuss", [
	  (party_set_slot, "$current_town", slot_fort_npc_2_state, 3), #set to "companion recruited"
	  (party_get_slot, ":companion", "$current_town", slot_fort_npc_2),
	  #(party_add_members, "p_main_party", ":companion", 1),
	  (call_script, "script_recruit_troop_as_companion", ":companion")
	]],
[anyone|plyr, "fort_deputy_discuss_options", [
      (str_store_party_name, s3, "$current_town"),
    ], "What does {s3} have to offer?", "fort_deputy_discuss_specialty", []],
[anyone, "fort_deputy_discuss_specialty", [
      (store_sub, ":offset", "$current_town", forts_begin),
      (store_add, ":deputy_talk", "str_gekokujo_fort_1_deputy_ask_specialty", ":offset"),
      (str_store_string, s45, ":deputy_talk"),
    ], "{s45}","fort_deputy_discuss", []],
[anyone|plyr, "fort_deputy_discuss_options", [
      (party_slot_eq, "$current_town", slot_fort_timer, 0),
    ], "I wish to recruit some men.", "fort_deputy_discuss_recruit", []],
[anyone, "fort_deputy_discuss_recruit", [], "Very well.", "fort_deputy_discuss", [
      (party_set_slot, "$current_town", slot_fort_timer, 7), #reset the timer
      (store_random_in_range, ":rand_recruits", 15, 31), #15 to 31 recruits
      (party_get_slot, ":recruit", "$current_town", slot_fort_recruit_type), #determine the type of recruits
      (party_add_members, "$current_town", ":recruit", ":rand_recruits"), #give them to the town garrison
      (change_screen_exchange_members, 1, "$current_town"), #change to the garrison screen
    ]],
[anyone|plyr, "fort_deputy_discuss_options", [
      (party_slot_eq, "$current_town", slot_fort_timer, 0),
    ], "I wish to produce some goods.", "fort_deputy_discuss_produce", []],
[anyone, "fort_deputy_discuss_produce", [], "They are ready to be shipped, my {lord/lady}.", "fort_deputy_discuss", [
      (party_set_slot, "$current_town", slot_fort_timer, 7), #reset the timer
	  
      (try_begin),
	    (eq, "$current_town", "p_fort_1"), #sado produces 5-10 dried sea fish
        (store_random_in_range, ":rand_goods", 5, 11),
        (assign, ":goods", "itm_smoked_fish"),
      (else_try),
	    (eq, "$current_town", "p_fort_2"), #tsushima produces 1-3 spice
        (store_random_in_range, ":rand_goods", 1, 4),
        (assign, ":goods", "itm_spice"),
      (else_try),
	    (eq, "$current_town", "p_fort_3"), #kokawa-dera produces 5-8 lacquer ware
        (store_random_in_range, ":rand_goods", 5, 9),
        (assign, ":goods", "itm_leatherwork"),
      (else_try),
	    (eq, "$current_town", "p_fort_4"), #mii-dera produces 4-8 linen cloth
        (store_random_in_range, ":rand_goods", 4, 9),
        (assign, ":goods", "itm_linen"),
      (else_try),
	    (eq, "$current_town", "p_fort_5"), #niputay produces 4-7 iron
        (store_random_in_range, ":rand_goods", 4, 8),
        (assign, ":goods", "itm_iron"),
      (else_try),
	    (eq, "$current_town", "p_fort_6"), #otasut produces 3-4 furs
        (store_random_in_range, ":rand_goods", 3, 5),
        (assign, ":goods", "itm_furs"),
      (try_end),
	  
      (troop_add_items, "$g_talk_troop", ":goods", ":rand_goods"), #give them to the deputy aka warehouse inventory
      (change_screen_loot, "$g_talk_troop"), #change to the warehouse inventry screen
    ]],
[anyone|plyr, "fort_deputy_discuss_options", [
      (party_slot_ge, "$current_town", slot_fort_timer, 1),
    ], "When are you able to recruit men or produce goods again?", "fort_deputy_discuss_timer", []],
[anyone, "fort_deputy_discuss_timer", [
      (party_get_slot, reg2, "$current_town", slot_fort_timer),
	  (try_begin),
	    (gt, reg2, 1),
		(str_store_string, s3, "@{reg2} days"),
	  (else_try),
		(str_store_string, s3, "@another day"),
	  (try_end),
    ], "At the pace we are going, surely no more than {s3}.", "fort_deputy_discuss", []],
[anyone|plyr,"fort_deputy_discuss_options", [],
    "Let's check the warehouse inventories.", "fort_deputy_discuss", [
      (change_screen_loot, "$g_talk_troop"),
    ]],
[anyone|plyr,"fort_deputy_discuss_options", [], "Let me see your equipment.", "fort_deputy_discuss_equipment", []],
[anyone,"fort_deputy_discuss_equipment", [], "Very well, it's all here...", "fort_deputy_discuss", [(change_screen_equip_other)]],
[anyone|plyr,"fort_deputy_discuss_options", [],
    "That is all for now.", "close_window", []],
[anyone, "fort_companion_discuss", [], "Anything else?","fort_companion_discuss_options", []],
[anyone|plyr, "fort_companion_discuss_options", [], 
    "Could you tell me a little about yourself?", "fort_companion_discuss_companion", []],
[anyone, "fort_companion_discuss_companion", [
      (store_sub, ":offset", "$current_town", forts_begin),
      (store_add, ":companion_talk", "str_gekokujo_fort_1_companion_about", ":offset"),
      (str_store_string, s45, ":companion_talk"),
    ], "{s45}","fort_companion_discuss", []],
[anyone|plyr, "fort_companion_discuss_options", [
      (party_slot_eq, "$current_town", slot_fort_npc_2_state, 2), #temporarily returned
	  (party_get_free_companions_capacity, ":free_capacity","p_main_party"),
	  (ge, ":free_capacity", 1),
    ], 
    "I would like for you to rejoin me.", "fort_companion_discuss_companion_rejoin", []],
[anyone, "fort_companion_discuss_companion_rejoin", [], "Very well, {playername}.","fort_companion_discuss", [
	  (party_set_slot, "$current_town", slot_fort_npc_2_state, 3), #set to "companion recruited"
	  (call_script, "script_recruit_troop_as_companion", "$g_talk_troop")
	]],
[anyone|plyr, "fort_companion_discuss_options", [
      (this_or_next|party_slot_eq, "$current_town", slot_fort_npc_2_state, 0), #haven't asked yet
      (party_slot_eq, "$current_town", slot_fort_npc_2_state, 1), #already asked, but haven't confirmed
	  (party_get_free_companions_capacity, ":free_capacity","p_main_party"),
	  (ge, ":free_capacity", 1),
    ], 
    "I would like for you to join me on my travels.", "fort_companion_discuss_companion_recruit", []],
[anyone, "fort_companion_discuss_companion_recruit", [
      (party_slot_eq, "$current_town", slot_fort_npc_2_state, 0), #haven't asked yet
      (store_sub, ":offset", "$current_town", forts_begin),
      (store_add, ":companion_talk", "str_gekokujo_fort_1_companion_recruit", ":offset"),
      (str_store_string, s45, ":companion_talk"),
    ], "{s45}", "fort_companion_discuss_companion_recruit_2", []],
[anyone, "fort_companion_discuss_companion_recruit", [
      (party_slot_eq, "$current_town", slot_fort_npc_2_state, 1), #already asked, but haven't confirmed
	  (party_get_slot, ":deputy", "$current_town", slot_fort_npc_1),
	  (str_store_troop_name, s2, ":deputy"),
    ], "Have you spoken to {s2} about allowing me to join you?", "fort_companion_discuss_companion_recruit_2", []],
[anyone|plyr, "fort_companion_discuss_companion_recruit_2", [
      (party_slot_eq, "$current_town", slot_fort_npc_2_state, 0), #haven't asked yet
	], 
    "Yes. Please join me.", "fort_companion_discuss_companion_recruit_3", [
	  (party_set_slot, "$current_town", slot_fort_npc_2_state, 1), #set to "already asked"
	]],
[anyone|plyr, "fort_companion_discuss_companion_recruit_2", [
      (party_slot_eq, "$current_town", slot_fort_npc_2_state, 1), #already asked, but haven't confirmed
    ], 
    "Not yet.", "fort_companion_discuss", []],
[anyone|plyr, "fort_companion_discuss_companion_recruit_2", [], 
    "On second thought, forget it.", "fort_companion_discuss", [
	  (party_set_slot, "$current_town", slot_fort_npc_2_state, 0), #reset to "not asked"
	]],
[anyone, "fort_companion_discuss_companion_recruit_3", [
      (party_get_slot, ":deputy", "$current_town", slot_fort_npc_1),
	  (str_store_troop_name, s2, ":deputy"),
    ], 
    "I would love to go, but it is not up to me. Please ask {s2} for permission on my behalf.", "fort_companion_discuss", []],
[anyone|plyr,"fort_companion_discuss_options", [],
    "That is all for now.", "close_window", []],
[anyone|plyr,"battle_reason_stated", [], "I am not afraid of you. I will fight.", "close_window",[[encounter_attack]]],
[anyone|plyr,"free", [[neg|in_meta_mission]], "Tell me about yourself", "view_char_requested",[]],
[anyone,"view_char_requested", [], "Very well, listen to this...", "view_char",[[change_screen_view_character]]],
[anyone,"view_char", [], "Anything else?", "free",[]],
[anyone|plyr,"end", [], "[Done]", "close_window",[]],
[anyone,"threaten_1", [], "We will fight you first", "end",[[encounter_attack]]],
[anyone|plyr,"free", [[in_meta_mission]], " Good-bye.", "close_window",[]],
[anyone|plyr,"free", [[neg|in_meta_mission]], " [Leave]", "close_window",[]],
]
