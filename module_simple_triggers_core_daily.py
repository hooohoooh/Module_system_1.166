# -*- coding: UTF-8 -*-
# split feature file: simple_triggers - module
from header_common import *
from header_operations import *
from header_parties import *
from header_items import *
from header_skills import *
from header_triggers import *
from header_troops import *
from header_music import *
from header_terrain_types import *
from module_factions import dplmc_factions_end
from module_constants import *

simple_triggers_core_daily = [
# This trigger is deprecated. Use "script_game_event_party_encounter" in module_scripts.py instead  
  (ti_on_party_encounter,
   [
    ]),
# This trigger is deprecated. Use "script_game_event_simulate_battle" in module_scripts.py instead 
  (ti_simulate_battle,
   [
    ]),
#Notification menus
  (0,
   [
     (troop_slot_ge, "trp_notification_menu_types", 0, 1),
     (troop_get_slot, ":menu_type", "trp_notification_menu_types", 0),
     (troop_get_slot, "$g_notification_menu_var1", "trp_notification_menu_var1", 0),
     (troop_get_slot, "$g_notification_menu_var2", "trp_notification_menu_var2", 0),
     (jump_to_menu, ":menu_type"),
     (assign, ":end_cond", 2),
     (try_for_range, ":cur_slot", 1, ":end_cond"),
       (try_begin),
         (troop_slot_ge, "trp_notification_menu_types", ":cur_slot", 1),
         (val_add, ":end_cond", 1),
       (try_end),
       (store_sub, ":cur_slot_minus_one", ":cur_slot", 1),
       (troop_get_slot, ":local_temp", "trp_notification_menu_types", ":cur_slot"),
       (troop_set_slot, "trp_notification_menu_types", ":cur_slot_minus_one", ":local_temp"),
       (troop_get_slot, ":local_temp", "trp_notification_menu_var1", ":cur_slot"),
       (troop_set_slot, "trp_notification_menu_var1", ":cur_slot_minus_one", ":local_temp"),
       (troop_get_slot, ":local_temp", "trp_notification_menu_var2", ":cur_slot"),
       (troop_set_slot, "trp_notification_menu_var2", ":cur_slot_minus_one", ":local_temp"),
     (try_end),
    ]),
  #Music,
  (1,
   [
       (map_free),
       (call_script, "script_music_set_situation_with_culture", mtf_sit_travel),
	    ]),
	
 (2, #Error check for multiple parties on the map
	[
	(eq, "$cheat_mode", 1),
	(assign, ":debug_menu_noted", 0),
	(try_for_parties, ":party_no"),
		(gt, ":party_no", "p_spawn_points_end"),
		(party_stack_get_troop_id, ":commander", ":party_no", 0),
		##diplomacy start+
		(is_between, ":commander", heroes_begin, heroes_end),
		(this_or_next|troop_slot_eq, ":commander", slot_troop_occupation, slto_kingdom_hero),
		##diplomacy end+
		(is_between, ":commander", active_npcs_begin, active_npcs_end),
		(troop_get_slot, ":commander_party", ":commander", slot_troop_leaded_party),
		(neq, ":party_no", ":commander_party"),
		(assign, reg4, ":party_no"),
		(assign, reg5, ":commander_party"),

		(str_store_troop_name, s3, ":commander"),
		(display_message, "@{!}{s3} commander of party #{reg4} which is not his troop_leaded party {reg5}"),
		##diplomacy start+ Make it clear what the error was
		(try_begin),
			(gt, reg4, 0),
			(gt, reg5, 0),
			(str_store_party_name, s3, reg4),
			(str_store_party_name, s65, reg5),
			(display_message, "@{!} Commanded party #{reg4} is {s3}, troop_leaded party #{reg5} is {s65}"),
			(str_store_troop_name, s3, ":commander"),
		(try_end),
		##diplomacy end+
		(str_store_string, s65, "str_party_with_commander_mismatch__check_log_for_details_"),

		(try_begin),
			(eq, ":debug_menu_noted", 0),
			(call_script, "script_add_notification_menu", "mnu_debug_alert_from_s65", 0, 0),
			(assign, ":debug_menu_noted", 1),
		(try_end),
	(try_end),
	]),
   
   
#Player raiding a village
# This trigger will check if player's raid has been completed and will lead control to village menu.
  (1,
   [
      (ge,"$g_player_raiding_village",1),
      (try_begin),
        (neq, "$g_player_is_captive", 0),
        #(rest_for_hours, 0, 0, 0), #stop resting - abort
        (assign,"$g_player_raiding_village",0),
      (else_try),
        (map_free), #we have been attacked during raid
        (assign,"$g_player_raiding_village",0),
      (else_try),
        (this_or_next|party_slot_eq, "$g_player_raiding_village", slot_village_state, svs_looted),
        (party_slot_eq, "$g_player_raiding_village", slot_village_state, svs_deserted),
        (start_encounter, "$g_player_raiding_village"),
        (rest_for_hours, 0),
        (assign,"$g_player_raiding_village",0),
        (assign,"$g_player_raid_complete",1),
      (else_try),
        (party_slot_eq, "$g_player_raiding_village", slot_village_state, svs_being_raided),
        (rest_for_hours, 3, 5, 1), #rest while attackable
      (else_try),
        (rest_for_hours, 0, 0, 0), #stop resting - abort
        (assign,"$g_player_raiding_village",0),
        (assign,"$g_player_raid_complete",0),
      (try_end),
    ]),
  # Reducing luck by 1 in every 180 hours
  (180,
   [
     (val_sub, "$g_player_luck", 1),
     (val_max, "$g_player_luck", 0),
    ]),
	
  # Banner selection menu
  (24,
   [
    (eq, "$g_player_banner_granted", 1),
    (troop_slot_eq, "trp_player", slot_troop_banner_scene_prop, 0),
    (le,"$auto_menu",0),
#normal_banner_begin
    (start_presentation, "prsnt_banner_selection"),
#custom_banner_begin
#    (start_presentation, "prsnt_custom_banner"),
    ]),
  # Process village raids
   (2,
   [
       (call_script, "script_process_village_raids"),
    ]),
 #cache party strengths (to avoid re-calculating)
##  (2,
##   [
##       (try_for_range, ":cur_troop", heroes_begin, heroes_end),
##         (troop_slot_eq, ":cur_troop", slot_troop_occupation, slto_kingdom_hero),
##         (troop_get_slot, ":cur_party", ":cur_troop", slot_troop_leaded_party),
##         (ge, ":cur_party", 0),
##         (call_script, "script_party_calculate_strength", ":cur_party", 0), #will update slot_party_cached_strength
##       (try_end),
##    ]),
##  
##  (6,
##   [
##       (try_for_range, ":cur_center", walled_centers_begin, walled_centers_end),
##         (call_script, "script_party_calculate_strength", ":cur_center", 0), #will update slot_party_cached_strength
##       (try_end),
##    ]),

##  (1,
##   [
##       (try_for_range, ":cur_center", walled_centers_begin, walled_centers_end),
##         (store_random_in_range, ":rand", 0, 100),
##         (lt, ":rand", 10),
##         (store_faction_of_party, ":center_faction", ":cur_center"),
##         (assign, ":friend_strength", 0),
##         (try_for_range, ":cur_troop", heroes_begin, heroes_end),
##           (troop_slot_eq, ":cur_troop", slot_troop_occupation, slto_kingdom_hero),
##           (troop_get_slot, ":cur_troop_party", ":cur_troop", slot_troop_leaded_party),
##           (gt, ":cur_troop_party", 0),
##           (store_distance_to_party_from_party, ":distance", ":cur_troop_party", ":cur_center"),
##           (lt, ":distance", 10),
##           (store_troop_faction, ":army_faction", ":cur_troop"),
##           (store_relation, ":rel", ":army_faction", ":center_faction"),
##           (try_begin),
##             (gt, ":rel", 10),
##             (party_get_slot, ":str", ":cur_troop_party", slot_party_cached_strength),
##             (val_add, ":friend_strength", ":str"),
##           (try_end),
##         (try_end),
##         (party_set_slot, ":cur_center", slot_party_nearby_friend_strength, ":friend_strength"),
##       (try_end),
##    ]),

  # Make heroes running away from someone retreat to friendly centers
  (0.5,
   [
       (try_for_range, ":cur_troop", heroes_begin, heroes_end),
         (troop_slot_eq, ":cur_troop", slot_troop_occupation, slto_kingdom_hero),
         (troop_get_slot, ":cur_party", ":cur_troop", slot_troop_leaded_party),
         (gt, ":cur_party", 0),
         (try_begin),
           (party_is_active, ":cur_party"),
           (try_begin),
             (get_party_ai_current_behavior, ":ai_bhvr", ":cur_party"),
             (eq, ":ai_bhvr", ai_bhvr_avoid_party),
			 
			 #Certain lord personalities will not abandon a battlefield to flee to a fortress
			 (assign, ":continue", 1),
			 (try_begin),
				(this_or_next|troop_slot_eq, ":cur_troop", slot_lord_reputation_type, lrep_upstanding),
					(troop_slot_eq, ":cur_troop", slot_lord_reputation_type, lrep_martial),
				(get_party_ai_current_object, ":ai_object", ":cur_party"),
				(party_is_active, ":ai_object"),
				(party_get_battle_opponent, ":battle_opponent", ":ai_object"),
				(party_is_active, ":battle_opponent"),
				(assign, ":continue", 0),
			 (try_end),
			 (eq, ":continue", 1),
			 
			 
             (store_faction_of_party, ":party_faction", ":cur_party"),
             (party_get_slot, ":commander_party", ":cur_party", slot_party_commander_party),
             (faction_get_slot, ":faction_marshall", ":party_faction", slot_faction_marshall),
             (neq, ":faction_marshall", ":cur_troop"),
             (assign, ":continue", 1),
             (try_begin),
               (ge, ":faction_marshall", 0),
               (troop_get_slot, ":faction_marshall_party", ":faction_marshall", slot_troop_leaded_party),
               (party_is_active, ":faction_marshall_party", 0),
               (eq, ":commander_party", ":faction_marshall_party"),
               (assign, ":continue", 0),
             (try_end),
             (eq, ":continue", 1),
             (assign, ":done", 0),
             (try_for_range, ":cur_center", walled_centers_begin, walled_centers_end),
               (eq, ":done", 0),
               (party_slot_eq, ":cur_center", slot_center_is_besieged_by, -1),
               (store_faction_of_party, ":center_faction", ":cur_center"),
               (store_relation, ":cur_relation", ":center_faction", ":party_faction"),
               (gt, ":cur_relation", 0),
               (store_distance_to_party_from_party, ":cur_distance", ":cur_party", ":cur_center"),
               (lt, ":cur_distance", 20),
               (party_get_position, pos1, ":cur_party"),
               (party_get_position, pos2, ":cur_center"),
               (neg|position_is_behind_position, pos2, pos1),
               (call_script, "script_party_set_ai_state", ":cur_party", spai_retreating_to_center, ":cur_center"),
               (assign, ":done", 1),
             (try_end),
           (try_end),
         (else_try),
           (troop_set_slot, ":cur_troop", slot_troop_leaded_party, -1),
         (try_end),
       (try_end),
    ]),
  # Make parties larger as game progresses.
  (24,
   [
       (call_script, "script_update_party_creation_random_limits"),
    ]),
		
  # Reduce renown slightly by 0.5% every week
  (7 * 24,
   [
       (troop_get_slot, ":player_renown", "trp_player", slot_troop_renown),
       (store_div, ":renown_decrease", ":player_renown", 200),
       (val_sub, ":player_renown", ":renown_decrease"),
       (troop_set_slot, "trp_player", slot_troop_renown, ":player_renown"),
    ]),
  # Read books if player is resting.
  (1, [(neg|map_free),
       (gt, "$g_player_reading_book", 0),
       (player_has_item, "$g_player_reading_book"),
       (store_attribute_level, ":int", "trp_player", ca_intelligence),
       (item_get_slot, ":int_req", "$g_player_reading_book", slot_item_intelligence_requirement),
       (le, ":int_req", ":int"),
       (item_get_slot, ":book_reading_progress", "$g_player_reading_book", slot_item_book_reading_progress),
       (item_get_slot, ":book_read", "$g_player_reading_book", slot_item_book_read),
       (eq, ":book_read", 0),
       (val_add, ":book_reading_progress", 7),
       (item_set_slot, "$g_player_reading_book", slot_item_book_reading_progress, ":book_reading_progress"),
       (ge, ":book_reading_progress", 1000),
       (item_set_slot, "$g_player_reading_book", slot_item_book_read, 1),
       (str_store_item_name, s1, "$g_player_reading_book"),
       (str_clear, s2),
       (try_begin),
         (eq, "$g_player_reading_book", "itm_book_tactics"),
         (troop_raise_skill, "trp_player", "skl_tactics", 1),
         (str_store_string, s2, "@ Your tactics skill has increased by 1."),
       (else_try),
         (eq, "$g_player_reading_book", "itm_book_persuasion"),
         (troop_raise_skill, "trp_player", "skl_persuasion", 1),
         (str_store_string, s2, "@ Your persuasion skill has increased by 1."),
       (else_try),
         (eq, "$g_player_reading_book", "itm_book_leadership"),
         (troop_raise_skill, "trp_player", "skl_leadership", 1),
         (str_store_string, s2, "@ Your leadership skill has increased by 1."),
       (else_try),
         (eq, "$g_player_reading_book", "itm_book_intelligence"),
         (troop_raise_attribute, "trp_player", ca_intelligence, 1),
         (str_store_string, s2, "@ Your intelligence has increased by 1."),
       (else_try),
         (eq, "$g_player_reading_book", "itm_book_trade"),
         (troop_raise_skill, "trp_player", "skl_trade", 1),
         (str_store_string, s2, "@ Your trade skill has increased by 1."),
       (else_try),
         (eq, "$g_player_reading_book", "itm_book_weapon_mastery"),
         (troop_raise_skill, "trp_player", "skl_weapon_master", 1),
         (str_store_string, s2, "@ Your weapon master skill has increased by 1."),
       (else_try),
         (eq, "$g_player_reading_book", "itm_book_engineering"),
         (troop_raise_skill, "trp_player", "skl_engineer", 1),
         (str_store_string, s2, "@ Your engineer skill has increased by 1."),
       (try_end),
       
       (unlock_achievement, ACHIEVEMENT_BOOK_WORM),

       (try_begin),
         (eq, "$g_infinite_camping", 0),
         (dialog_box, "@You have finished reading {s1}.{s2}", "@Book Read"),
       (try_end),  
              
       (assign, "$g_player_reading_book", 0),	   	   
       ]),
(1, 
   [
     (store_current_day, ":cur_day"),
     (gt, ":cur_day", "$g_last_report_control_day"),
     (store_time_of_day, ":cur_hour"),
     (ge, ":cur_hour", 18),

     (store_random_in_range, ":rand_no", 0, 4),
     (this_or_next|ge, ":cur_hour", 22),
     (eq, ":rand_no", 0),
     
     (assign, "$g_last_report_control_day", ":cur_day"),
     
     (store_troop_gold, ":gold", "trp_player"),
     
     (try_begin),
       (lt, ":gold", 0),
       (store_sub, ":gold_difference", 0, ":gold"),
       (troop_add_gold, "trp_player", ":gold_difference"),
     (try_end),

     (party_get_morale, ":main_party_morale", "p_main_party"),     
     
     #(assign, ":swadian_soldiers_are_upset_message_showed", 0),
     #(assign, ":vaegir_soldiers_are_upset_message_showed", 0),
     #(assign, ":khergit_soldiers_are_upset_message_showed", 0),
     #(assign, ":nord_soldiers_are_upset_message_showed", 0),
     #(assign, ":rhodok_soldiers_are_upset_message_showed", 0),
    
     (try_begin),
       (str_store_string, s1, "str_party_morale_is_low"),            
       (str_clear, s2),

       (party_get_num_companion_stacks, ":num_stacks","p_main_party"),
       (assign, ":num_deserters_total", 0),
       (try_for_range_backwards, ":i_stack", 0, ":num_stacks"),
         (party_stack_get_troop_id, ":stack_troop", "p_main_party", ":i_stack"),
         (neg|troop_is_hero, ":stack_troop"),
         (party_stack_get_size, ":stack_size", "p_main_party", ":i_stack"),
         
         (store_troop_faction, ":faction_no", ":stack_troop"),
      
         (assign, ":troop_morale", ":main_party_morale"),         
         (try_begin),
           (ge, ":faction_no", npc_kingdoms_begin),
           (lt, ":faction_no", npc_kingdoms_end),
        
           (faction_get_slot, ":troop_morale_addition", ":faction_no",  slot_faction_morale_of_player_troops),
           (val_div, ":troop_morale_addition", 100),
           (val_add, ":troop_morale", ":troop_morale_addition"),
         (try_end),

         (lt, ":troop_morale", 32),
         (store_sub, ":desert_prob", 36, ":troop_morale"),
         (val_div, ":desert_prob", 4),

         (assign, ":num_deserters_from_that_troop", 0),
         (try_for_range, ":unused", 0, ":stack_size"),
           (store_random_in_range, ":rand_no", 0, 100),
           (lt, ":rand_no", ":desert_prob"),
           (val_add, ":num_deserters_from_that_troop", 1),
           #p.remove_members_from_stack(i_stack,cur_deserters, &main_party_instances);
           (remove_member_from_party, ":stack_troop", "p_main_party"),
         (try_end),
         (try_begin),
           (ge, ":num_deserters_from_that_troop", 1),           
           (str_store_troop_name, s2, ":stack_troop"),
           (assign, reg0, ":num_deserters_from_that_troop"),
           
#           (try_begin),           
#             (lt, ":troop_morale_addition", -2),
#             (ge, ":main_party_morale", 28),
#             (try_begin),
#               (eq, ":faction_no", "fac_kingdom_1"),  
#               (eq, ":swadian_soldiers_are_upset_message_showed", 0),
#               (str_store_string, s3, "str_swadian_soldiers_are_upset"),
#               (assign, ":swadian_soldiers_are_upset_message_showed", 1),
#             (else_try),
#               (eq, ":faction_no", "fac_kingdom_2"),  
#               (eq, ":vaegir_soldiers_are_upset_message_showed", 0),
#               (str_store_string, s3, "str_vaegir_soldiers_are_upset"),
#               (assign, ":vaegir_soldiers_are_upset_message_showed", 1),
#             (else_try),
#               (eq, ":faction_no", "fac_kingdom_3"),  
#               (eq, ":khergit_soldiers_are_upset_message_showed", 0),
#               (str_store_string, s3, "str_khergit_soldiers_are_upset"),
#               (assign, ":khergit_soldiers_are_upset_message_showed", 1),
#             (else_try),
#               (eq, ":faction_no", "fac_kingdom_4"),  
#               (eq, ":nord_soldiers_are_upset_message_showed", 0),
#               (str_store_string, s3, "str_nord_soldiers_are_upset"),
#               (assign, ":nord_soldiers_are_upset_message_showed", 1),
#             (else_try),
#               (eq, ":faction_no", "fac_kingdom_5"),  
#               (eq, ":rhodok_soldiers_are_upset_message_showed", 0),
#               (str_store_string, s3, "str_rhodok_soldiers_are_upset"),
#               (assign, ":rhodok_soldiers_are_upset_message_showed", 1),
#             (try_end),
#             (str_store_string, s1, "@{!}{s1} {s3}"),
#           (try_end),
           
           (try_begin),
             (ge, ":num_deserters_total", 1),
             (str_store_string, s1, "str_s1_reg0_s2"),
           (else_try),
             (str_store_string, s3, s1),
             (str_store_string, s1, "str_s3_reg0_s2"),
           (try_end),
           (val_add, ":num_deserters_total", ":num_deserters_from_that_troop"),
         (try_end),
       (try_end),

       (try_begin),
         (ge, ":num_deserters_total", 1),
  
         (try_begin),
           (ge, ":num_deserters_total", 2),
           (str_store_string, s2, "str_have_deserted_the_party"),
         (else_try),
           (str_store_string, s2, "str_has_deserted_the_party"),
         (try_end),          

         (str_store_string, s1, "str_s1_s2"),

         (eq, "$g_infinite_camping", 0),
         
         (tutorial_box, s1, "str_weekly_report"),
       (try_end), 
     (try_end),
 ]),
   
  (24,
   [
   (val_sub, "$g_dont_give_fief_to_player_days", 1),
   (val_max, "$g_dont_give_fief_to_player_days", -1),
   (val_sub, "$g_dont_give_marshalship_to_player_days", 1),
   (val_max, "$g_dont_give_marshalship_to_player_days", -1),

   ##diplomacy start+
   ##Add version checking, so the corrections are only applied once.
   ##This allows for more complicated things to be added here in the future
   (troop_get_slot, ":diplomacy_version_code", "trp_dplmc_chamberlain", dplmc_slot_troop_affiliated),#I've arbitrarily picked "when I started tracking this" as 0
   (store_mod, ":verification", ":diplomacy_version_code", 128),
   (assign, ":save_reg0", reg0),
   (assign, ":save_reg1", reg1),
   (try_begin),
		#Detect bad values
		(neq, ":diplomacy_version_code", 0),
		(neq, ":verification", 68),
		(assign, reg0, ":diplomacy_version_code"),
		(display_message, "@{!} A slot had an unexpected value: {reg0}.  This might be because you are using an incompatible troop list, or are using a non-native strange game.  This message will repeat daily."),
		(assign, ":diplomacy_version_code", -1),
	(else_try),
		(val_div, ":diplomacy_version_code", 128),
		#Update if necessary.
		(lt, ":diplomacy_version_code", DPLMC_CURRENT_VERSION_CODE),
		(ge, "$cheat_mode", 1),
		(assign, reg0, ":diplomacy_version_code"),

		(assign, reg1, DPLMC_CURRENT_VERSION_CODE),
		(display_message, "@{!} DEBUG - Detected a new version of diplomacy: previous version was {reg0}, and current version is {reg1}.  Performing updates."),
		(val_mul, reg1, 128),
		(val_add, reg1, DPLMC_VERSION_LOW_7_BITS),
		(troop_set_slot, "trp_dplmc_chamberlain", dplmc_slot_troop_affiliated, reg1),
	(try_end),

	#gekokujo fix?
	#(try_begin),
	#(is_between, ":diplomacy_version_code", -1, 1),#-1 or 0
	#Native behavior follows
	##diplomacy end+

   #gekokujo deprecated "fixes" start
   #this to correct string errors in games started in 1.104 or before
   #(party_set_name, "p_seto_pirate_spawn_point", "str_the_steppes"),
   #(party_set_name, "p_kanto_rebel_spawn_point", "str_the_tundra"),
   #(party_set_name, "p_shinano_rebel_spawn_point", "str_the_forests"),
   #(party_set_name, "p_woku_pirate_spawn_point", "str_the_highlands"),
   #(party_set_name, "p_kinai_rebel_spawn_point_1", "str_the_coast"),
   #(party_set_name, "p_monk_rebel_spawn_point_2", "str_the_coast"),
   #(party_set_name, "p_northern_raider_spawn_point", "str_the_deserts"),

   #gekokujo rename Kobe and Hyogo
#   (party_set_name, "p_castle_6", "@Sumoto Castle"),
#   (party_set_name, "p_village_26", "@Sumoto"),
   
   #gekokujo rename Yokosuka
#   (party_set_name, "p_village_5", "@Miura"),

   #this to correct inappropriate home strings - Katrin to Uxkhal, Matheld to Fearichen
   #(troop_set_slot, "trp_npc11", slot_troop_home, "p_town_7"),
   #(troop_set_slot, "trp_npc8", slot_troop_home, "p_village_35"),

   #(troop_set_slot, "trp_npc15", slot_troop_town_with_contacts, "p_town_20"), #durquba

   #this to correct linen production at villages of durquba
   #(party_set_slot, "p_village_93", slot_center_linen_looms, 0), #mazigh
   #(party_set_slot, "p_village_94", slot_center_linen_looms, 0), #sekhtem
   #(party_set_slot, "p_village_95", slot_center_linen_looms, 0), #qalyut
   #(party_set_slot, "p_village_96", slot_center_linen_looms, 0), #tilimsal
   #(party_set_slot, "p_village_97", slot_center_linen_looms, 0), #shibal zumr
   #(party_set_slot, "p_village_102", slot_center_linen_looms, 0), #tamnuh
   #(party_set_slot, "p_village_109", slot_center_linen_looms, 0), #habba

   #(party_set_slot, "p_village_67", slot_center_fishing_fleet, 0), #Tebandra
   #(party_set_slot, "p_village_5", slot_center_fishing_fleet, 15), #Kulum
   #gekokujo deprecated "fixes" end

   ##diplomacy start+
   #End the changes in Native
	#(try_end),

   #Behavior specific to a fresh Diplomacy version
	#(try_begin),
   #(ge, ":diplomacy_version_code", 0),#do not run this if the code is bad
   #(lt, ":diplomacy_version_code", 1),
#   #Add home centers for claimants (mods not using standard NPCs or map may wish to remove this)
#   (troop_set_slot, "trp_kingdom_1_pretender", slot_troop_home, "p_town_4"),#Lady Isolle - Suno
#   (troop_set_slot, "trp_kingdom_2_pretender", slot_troop_home, "p_town_11"),#Prince Valdym - Curaw
#   (troop_set_slot, "trp_kingdom_3_pretender", slot_troop_home, "p_town_18"),#Dustum Khan - Narra
#   (troop_set_slot, "trp_kingdom_4_pretender", slot_troop_home, "p_town_12"),#Lethwin Far-Seeker - Wercheg
#   (troop_set_slot, "trp_kingdom_5_pretender", slot_troop_home, "p_town_3"),#Lord Kastor - Veluca
#   (troop_set_slot, "trp_kingdom_6_pretender", slot_troop_home, "p_town_20"),#Arwa the Pearled One - Durquba
#   #add ancestral fiefs to home slots (mods not using standard NPCs or map should remove this)
#   (troop_set_slot, "trp_knight_2_10", slot_troop_home, "p_castle_29"), #Nelag_Castle
#   (troop_set_slot, "trp_knight_3_4", slot_troop_home, "p_castle_30"), #Asugan_Castle
#   (troop_set_slot, "trp_knight_1_3", slot_troop_home, "p_castle_35"), #Haringoth_Castle
#   (troop_set_slot, "trp_knight_5_11", slot_troop_home, "p_castle_33"), #Etrosq_Castle
#   #Also the primary six towns (mods not using standard NPCs or map may wish to remove this)
#   (troop_set_slot, "trp_kingdom_1_lord", slot_troop_home, "p_town_6"),#King Harlaus to Praven
#   (troop_set_slot, "trp_kingdom_2_lord", slot_troop_home, "p_town_8"),#King Yaroglek to Reyvadin
#   (troop_set_slot, "trp_kingdom_3_lord", slot_troop_home, "p_town_10"),#Sanjar Khan to Tulga
#   (troop_set_slot, "trp_kingdom_4_lord", slot_troop_home, "p_town_1"),#King Ragnar to Sargoth
#   (troop_set_slot, "trp_kingdom_5_lord", slot_troop_home, "p_town_5"),#King Graveth to Jelkala
#   (troop_set_slot, "trp_kingdom_6_lord", slot_troop_home, "p_town_19"),#Sultan Hakim to Shariz

#   #Set the "original lord" values corresponding to the above.
#   (try_for_range, ":troop_no", active_npcs_begin, active_npcs_end),
#		(this_or_next|eq, ":troop_no", "trp_knight_2_10"),#Nelag
#		(this_or_next|eq, ":troop_no", "trp_knight_3_4"),#Asugan
#		(this_or_next|eq, ":troop_no", "trp_knight_1_3"),#Haringoth
#		(this_or_next|eq, ":troop_no", "trp_knight_5_11"),#Etrosq
#		(this_or_next|is_between, ":troop_no", kings_begin, kings_end),
#			(is_between, ":troop_no", pretenders_begin, pretenders_end),
#
#		(troop_get_slot, ":center_no", ":troop_no", slot_troop_home),
#		(is_between, ":center_no", centers_begin, centers_end),
#		(neg|party_slot_ge, ":center_no", dplmc_slot_center_original_lord, 1),
#		(party_set_slot, ":center_no",  dplmc_slot_center_original_lord, ":troop_no"),
#
#		#Also set "ex-lord"
#		(neg|is_between, ":troop_no", pretenders_begin, pretenders_end),
#		(troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
#		(neg|party_slot_eq, ":center_no", slot_town_lord, ":troop_no"),
#		(neg|party_slot_ge, ":center_no", dplmc_slot_center_ex_lord, 1),
#		(party_set_slot, ":center_no", dplmc_slot_center_ex_lord, ":troop_no"),
   #(try_end),

   #Make sure the affiliation slot is set correctly.
   (try_begin),
	 (is_between, "$g_player_affiliated_troop", lords_begin, kingdom_ladies_end),
	 (troop_get_slot, ":slot_val", "$g_player_affiliated_troop", dplmc_slot_troop_affiliated),
	 (is_between, ":slot_val", 0, 3),#0 is default, 1 is asked, in previous versions there was no use of 2
	 (troop_set_slot, "$g_player_affiliated_troop", dplmc_slot_troop_affiliated, 3),#3 is affiliated
   (try_end),

   #Set father/mother slots for the unmarried medium-age lords, so checking for
   #being related will work as expected.
   (try_for_range, ":troop_no", lords_begin, lords_end),
		(troop_slot_eq, ":troop_no", slot_troop_father, -1),
		(troop_slot_eq, ":troop_no", slot_troop_mother, -1),
		(store_mul, ":father", ":troop_no", DPLMC_VIRTUAL_RELATIVE_MULTIPLIER),#defined in module_constants.py
		(val_add, ":father", DPLMC_VIRTUAL_RELATIVE_FATHER_OFFSET),
		(troop_set_slot, ":troop_no", slot_troop_father, ":father"),
		(store_add, ":mother", ":father", DPLMC_VIRTUAL_RELATIVE_MOTHER_OFFSET - DPLMC_VIRTUAL_RELATIVE_FATHER_OFFSET),
		(troop_set_slot, ":troop_no", slot_troop_mother, ":mother"),
   (try_end),

   #Fix kingdom lady daughters having "slot_troop_mother" set to themselves.
   #The old fix was in troop_get_family_relation_to_troop, but now we can
   #just do it once here.
   (try_for_range, ":troop_no", kingdom_ladies_begin, kingdom_ladies_end),
		(try_begin),
			(troop_slot_eq, ":troop_no", slot_troop_mother, ":troop_no"),
			(troop_get_slot, ":father", ":troop_no", slot_troop_father),
			(try_begin),
				(is_between, ":father", active_npcs_begin, active_npcs_end),
				(troop_get_slot, ":mother", ":father", slot_troop_spouse),
				(troop_set_slot, ":troop_no", slot_troop_mother, ":mother"),
				(try_begin),
					#Print a message if desired
					(ge, "$cheat_mode", 1),
					(str_store_troop_name, s0, ":troop_no"),
					(display_message, "@{!}DEBUG - Fixed slot_troop_mother for {s0}."),
				(try_end),
			(else_try),
				(troop_set_slot, ":troop_no", slot_troop_mother, -1),#better than being set to herself
				#Print a message if desired
				(ge, "$cheat_mode", 1),
				(str_store_troop_name, s0, ":troop_no"),
				(display_message, "@{!}DEBUG - When fixing slot_troop_mother for {s0}, could not find a valid mother."),
			(try_end),
	#While we're at it, also give parents to the sisters of the middle-aged lords.
		(else_try),
			(troop_slot_eq, ":troop_no", slot_troop_father, -1),
			(troop_slot_eq, ":troop_no", slot_troop_mother, -1),
			#"Guardian" here means brother
			(troop_get_slot, ":guardian", ":troop_no", slot_troop_guardian),
			(ge, ":guardian", 1),
			#Has brother's father
			(troop_get_slot, ":father", ":guardian", slot_troop_father),
			(troop_set_slot, ":troop_no", slot_troop_father, ":father"),
			#Has brother's mother
			(troop_get_slot, ":mother", ":guardian", slot_troop_mother),
			(troop_set_slot, ":troop_no", slot_troop_mother, ":mother"),
		(try_end),
   #Also set original factions for ladies.
	   (neg|troop_slot_ge, ":troop_no", slot_troop_original_faction, 1),
		(assign, ":guardian", -1),
		(try_begin),
		   (troop_slot_ge, ":troop_no", slot_troop_father, 1),
			(troop_get_slot, ":guardian", ":troop_no", slot_troop_father),
 	    (else_try),
		   (troop_slot_ge, ":troop_no", slot_troop_guardian, 1),
			(troop_get_slot, ":guardian", ":troop_no", slot_troop_guardian),
		(else_try),
		   (troop_slot_ge, ":troop_no", slot_troop_spouse, 1),
			(troop_get_slot, ":guardian", ":troop_no", slot_troop_spouse),
	    (try_end),
		(ge, ":guardian", 1),
		(troop_get_slot, ":original_faction", ":guardian", slot_troop_original_faction),
		(troop_set_slot, ":troop_no", slot_troop_original_faction, ":original_faction"),
   (try_end),

	  ##Set relations between kingdom ladies and their relatives.
	  ##Do *not* initialize their relations with anyone they aren't related to:
	  ##that is used for courtship.
	  ##  The purpose of this initialization is so if a kingdom lady gets promoted,
	  ##her relations aren't a featureless slate.  Also, it would be interesting to
	  ##further develop the idea of ladies as pursuing agendas even if they aren't
	  ##leading warbands, which would benefit from giving them relations with other
	  ##people.
	  #
	  #Because relations may already exist, only call this in instances where
	  #they are 0 or 1 (the latter just means "met" between NPCs).
     (try_for_range, ":lady", kingdom_ladies_begin, kingdom_ladies_end),
		(troop_slot_eq, ":lady", slot_troop_occupation, slto_kingdom_lady),
		(troop_get_slot, ":lady_faction", ":lady", slot_troop_original_faction),
		(ge, ":lady_faction", 1),

		(try_for_range, ":other_hero", heroes_begin, heroes_end),
		   (this_or_next|troop_slot_eq, ":other_hero", slot_troop_occupation, slto_kingdom_lady),
			(this_or_next|troop_slot_eq, ":other_hero", slot_troop_occupation, slto_kingdom_hero),
				(troop_slot_eq, ":other_hero", slot_troop_occupation, slto_inactive_pretender),
			(troop_slot_eq, ":other_hero", slot_troop_original_faction, ":lady_faction"),

			#Because this is not a new game: first check if relations have developed
			(call_script, "script_troop_get_relation_with_troop", ":lady", ":other_hero"),
			(is_between, reg0, 0, 2),#0 or 1

			(try_begin),
				(this_or_next|troop_slot_eq, ":lady", slot_troop_spouse, ":other_hero"),
				(troop_slot_eq, ":other_hero", slot_troop_spouse, ":lady"),
				(store_random_in_range, reg0, 0, 11),
			(else_try),
				#(call_script, "script_troop_get_family_relation_to_troop", ":lady", ":other_hero"),
				(call_script, "script_dplmc_troop_get_family_relation_to_troop", ":lady", ":other_hero"),
			(try_end),

			(call_script, "script_troop_change_relation_with_troop", ":lady", ":other_hero", reg0),

			#This relation change only applies between kingdom ladies.
			(troop_slot_eq, ":other_hero", slot_troop_occupation, slto_kingdom_lady),
			(is_between, ":other_hero", kingdom_ladies_begin, kingdom_ladies_end),

			(store_random_in_range, ":random", 0, 11),
			(call_script, "script_troop_change_relation_with_troop", ":lady", ":other_hero", ":random"),
		(try_end),
	 (try_end),

   #Change the occupation of exiled lords (not including pretenders or kings)
   (try_for_range, ":troop_no", lords_begin, lords_end),
		(store_troop_faction, ":faction_no", ":troop_no"),
		#A lord in the outlaw faction
		(eq, ":faction_no", "fac_outlaws"),
		#Possible values for his occupation if he's an exile (but there's some overlap between these and "bandit hero")
		(this_or_next|troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),#<- The default
		(this_or_next|troop_slot_eq, ":troop_no", slot_troop_occupation, slto_inactive),#<- This can happen joining the player faction
			(troop_slot_eq, ":troop_no", slot_troop_occupation, 0),#<- This gets set for prisoners
		#(Quick Check) Not leading a party or the prisoner of a party or at a center
		(neg|troop_slot_ge, ":troop_no", slot_troop_leaded_party, 0),
		(neg|troop_slot_ge, ":troop_no", slot_troop_prisoner_of_party, 0),
		(neg|troop_slot_ge, ":troop_no", slot_troop_cur_center, 1),#deliberately 1 instead of 0
		#(Slow check) Does not own any fiefs
		(assign, ":end", centers_end),
		(try_for_range, ":center_no", centers_begin, ":end"),
			(party_slot_eq, ":center_no", slot_town_lord, ":troop_no"),
			(assign, ":end", ":center_no"),#stop loop, and also signal failure
		(try_end),
		#(Slow check) Explicitly verify he is not a prisoner anywhere.
		(call_script, "script_search_troop_prisoner_of_party", ":troop_no"),
		(eq, reg0, -1),
		#(Slow check) Explicitly verify he's not a member of any party
		(assign, ":member_of_party", -1),
		(try_for_parties, ":party_no"),
			(eq, ":member_of_party", -1),
			(this_or_next|eq, ":party_no", "p_main_party"),
				(ge, ":party_no", centers_begin),
			(party_count_members_of_type, ":count", ":party_no", ":troop_no"),
			(gt, ":count", 0),
			(assign, ":member_of_party", ":party_no"),
		(try_end),
		(eq, ":member_of_party", -1),
		#Finally verified that he is in exile.  Set the slot value to make
		#this easier in the future.
		(troop_set_slot, ":troop_no", slot_troop_occupation, dplmc_slto_exile),
		(try_begin),
			(ge, "$cheat_mode", 1),
			(str_store_troop_name, s0, ":troop_no"),
			(display_message, "@{!}DEBUG - Changed occupation of {s0} to dplmc_slto_exile"),
		(try_end),
   (try_end),

   #Initialize histories for supported pretenders.
   (try_for_range, ":troop_no", pretenders_begin, pretenders_end),
      (neg|troop_slot_eq, ":troop_no", slot_troop_met, 0),
      (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
	  (troop_slot_eq, ":troop_no", slot_troop_playerparty_history, 0),
	  (troop_set_slot, ":troop_no", slot_troop_playerparty_history, dplmc_pp_history_granted_fief),
   (try_end),

   #Initialize histories for promoted companions
   #gekokujo 3.0 microfactions! include fort companions start
   #(try_for_range, ":troop_no", companions_begin, companions_end),
   (try_for_range, ":troop_no", companions_begin, fort_companions_end),
   #gekokujo 3.0 microfactions! include fort companions end
	  (neg|troop_slot_eq, ":troop_no", slot_troop_met, 0),
      (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
	  (neg|troop_slot_eq, ":troop_no", slot_troop_playerparty_history, dplmc_pp_history_nonplayer_entry),
	  (troop_set_slot, ":troop_no", slot_troop_playerparty_history, dplmc_pp_history_granted_fief),
   (try_end),

   #For all centers, update new slots
   (try_for_range, ":center_no", centers_begin, centers_end),
	  #Last attacker
	  (try_begin),
	     (party_slot_eq, ":center_no", dplmc_slot_center_last_attacker, 0),
		 (party_slot_eq, ":center_no", dplmc_slot_center_last_attacked_time, 0),
		 (party_set_slot, ":center_no", dplmc_slot_center_last_attacker, -1),
	  (try_end),

      (party_slot_eq, ":center_no", dplmc_slot_center_last_transfer_time, 0),
	  #Ex-lord
	  (try_begin),
  	     (party_slot_eq, ":center_no", dplmc_slot_center_ex_lord, 0),
	     (party_set_slot, ":center_no", dplmc_slot_center_ex_lord, -1),
	  (try_end),
	  #Original lord
	  (try_begin),
		(party_slot_eq, ":center_no", dplmc_slot_center_original_lord, 0),
		(neg|troop_slot_eq, "trp_player", slot_troop_home, ":center_no"),
		(party_set_slot, ":center_no", dplmc_slot_center_original_lord, -1),
	  (try_end),
   (try_end),

   #Don't bother filling in "last caravan arrival" slots with fake values.
   #Right now the scripts check and do that automatically if they aren't
   #set.

   #Perform initialization for autoloot / autosell.
   (call_script, "script_dplmc_initialize_autoloot", 1),#argument "1" forces this to make changes

   #Fix a mistake I had introduced before, where you could get the wrong
   #"marry betrothed" quest when courting a lady.
   (try_begin),
      (check_quest_active, "qst_wed_betrothed_female"),
	  (quest_get_slot, ":betrothed_troop", "qst_wed_betrothed_female", slot_quest_giver_troop),
	  (is_between, ":betrothed_troop", kingdom_ladies_begin, kingdom_ladies_end),
	  (display_message, "@{!}FIXED PROBLEM - Cancelled erroneous version of qst_wed_betrothed_female.  You should be able to marry normally if you try again."),
	  (call_script, "script_abort_quest", "qst_wed_betrothed_female", 0),#abort with type 0 "event" should give no penalties to the player
   (try_end),
   #End version-checked block.
   #(try_end), #gekokujo d'oh

   (try_begin),
    (ge, ":diplomacy_version_code", 1),
    (lt, ":diplomacy_version_code", 110615),
    #Fix a bug that was introduced in some version before 2011-06-15 that made
	#all "young unmarried lords" only have half-siblings, with either their own
	#father or mother slot uninitialized.
	(try_begin),
		(lt, 31, heroes_begin),
		(neg|troop_slot_eq, 31, 31, 0),#"slot_troop_father" was 31 in those saved games
		(troop_set_slot, 31, 31, -1),#(it still is 31 as far as I know, but this code should remain the same even if the slot value changes)
	(try_end),
	(try_begin),
		(lt, 32, heroes_begin),
		(neg|troop_slot_eq, 32,32,0),#"slot_troop_mother" was 32 in those saved games
		(troop_set_slot, 32, 32, -1),
	(try_end),
	(try_for_range, ":troop_no", lords_begin, lords_end),
		(troop_get_slot, reg0, ":troop_no", slot_troop_father),
		(troop_get_slot, reg1, ":troop_no", slot_troop_mother),
		(try_begin),
			(is_between, reg0, lords_begin, lords_end),
			(neg|is_between, reg1, kingdom_ladies_begin, kingdom_ladies_end),
			(troop_get_slot, reg1, reg0, slot_troop_spouse),
			(is_between, reg1, kingdom_ladies_begin, kingdom_ladies_end),
			(troop_set_slot, ":troop_no", slot_troop_mother, reg1),
			(call_script, "script_update_troop_notes", ":troop_no"),#Doesn't actually do anything
		(else_try),
			(is_between, reg1, kingdom_ladies_begin, kingdom_ladies_end),
			(neg|is_between, reg0, lords_begin, lords_end),
			(troop_get_slot, reg0, reg1, slot_troop_spouse),
			(is_between, reg0, lords_begin, lords_end),
			(troop_set_slot, ":troop_no", slot_troop_father, reg0),
			(call_script, "script_update_troop_notes", ":troop_no"),#Doesn't actually do anything
		(try_end),
	(try_end),

	#For old saved games, a reputation bug that was introduced in the release 2011-06-06 and was fixed on 2011-06-07.
	(eq, ":diplomacy_version_code", 1),
	(assign, reg0, 0),
	(try_for_range, ":troop_no", lords_begin, lords_end),
		(troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_none),
		(store_random_in_range, reg1, lrep_none, lrep_roguish),
		(val_max, reg1, lrep_none + 1),#So there's an extra chance of getting reputation 1, which is lrep_martial
		(troop_set_slot, ":troop_no", slot_lord_reputation_type, reg1),
		(val_add, reg0, 1),
	(try_end),

	(try_begin),
		(ge, "$cheat_mode", 1),
		(store_sub, reg1, reg0, 1),
		(display_message, "@{!} Bug fix: set personality types for {reg0} {reg1?lords:lord}"),
	(try_end),

	(assign, reg0, 0),
	(try_for_range, ":troop_no", kingdom_ladies_begin, kingdom_ladies_end),
		(neq, ":troop_no", "trp_knight_1_1_wife"),#That lady should not appear in the game
		(troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_none),
		(store_random_in_range, reg1, lrep_conventional - 1, lrep_moralist + 1),
		(val_max, reg1, lrep_conventional),#So there's an extra chance of getting lrep_conventional
		(troop_set_slot, ":troop_no", slot_lord_reputation_type, reg1),
		(val_add, reg0, 1),
	(try_end),

	(try_begin),
		(ge, "$cheat_mode", 1),
		(store_sub, reg1, reg0, 1),
		(display_message, "@{!} Bug fix: set personality types for {reg0} {reg1?ladies:lady}"),
	(try_end),
   (try_end),

   #Behavior for an upgrade from Native or pre-Diplomacy 4.0 to Diplomacy 4.0
   (try_begin),
      (is_between, ":diplomacy_version_code", 0, 111001),
      #Fix: slot_faction_leader and slot_faction_marshall should not equal trp_player
      #if the player is not a member of the faction.  (This is initially true because
      #trp_player is 0, and uninitialized slots default to 0.)
      (try_for_range, ":faction_no", 0, dplmc_factions_end),
         (neq, ":faction_no", "fac_player_faction"),
         (neq, ":faction_no", "fac_player_supporters_faction"),
         (this_or_next|neq, ":faction_no", "$players_kingdom"),
         (eq, ":faction_no", 0),
         #The player is not a member of the faction:
         (try_begin),
            (faction_slot_eq, ":faction_no", slot_faction_leader, 0),
            (faction_set_slot, ":faction_no", slot_faction_leader, -1),
         (try_end),
         (try_begin),
            (faction_slot_eq, ":faction_no", slot_faction_marshall, 0),
            (faction_set_slot, ":faction_no", slot_faction_marshall, -1),
         (try_end),
      (try_end),
      #Initialize home slots for town merchants, elders, etc.
      (try_for_range, ":center_no", centers_begin, centers_end),
         (try_for_range, ":troop_no", dplmc_slot_town_merchants_begin, dplmc_slot_town_merchants_end),
            (party_get_slot, ":troop_no", ":center_no", ":troop_no"),
            (gt, ":troop_no", walkers_end),
            (troop_is_hero, ":troop_no"),
            (troop_slot_eq, ":troop_no", slot_troop_home, 0),
            (troop_set_slot, ":troop_no", slot_troop_home, ":center_no"),
         (try_end),
      (try_end),
      #Initialize home slots for startup merchants.  (Merchant of Praven, etc.)
      #This should be done after kings have their home slots initialized.
      (try_for_range, ":troop_no", kings_begin, kings_end),
         (troop_get_slot, ":center_no", ":troop_no", slot_troop_home),
         (val_sub, ":troop_no", kings_begin),
         (val_add, ":troop_no", startup_merchants_begin),
         (is_between, ":troop_no", startup_merchants_begin, startup_merchants_end),#Right now there's a startup merchant for each faction.  Verify this hasn't unexpectedly changed.
         (neg|troop_slot_ge, ":troop_no", slot_troop_home, 1),#Verify that the home slot is not already set
         (troop_set_slot, ":troop_no", slot_troop_home, ":center_no"),
      (try_end),
      #Reset potentially bad value in "slot_troop_stance_on_faction_issue" (i.e. 153) from auto-loot
      (eq, 153, slot_troop_stance_on_faction_issue),
	  #gekokujo 3.0 microfactions! include fort companions start
      #(try_for_range, ":troop_no", companions_begin, companions_end),
      (try_for_range, ":troop_no", companions_begin, fort_companions_end),
	  #gekokujo 3.0 microfactions! include fort companions end
         (try_begin),
            (neg|troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
            (troop_set_slot, ":troop_no", slot_troop_stance_on_faction_issue, -1),
         (else_try),
            (troop_get_slot, ":slot_val", ":troop_no", slot_troop_stance_on_faction_issue),
            (neg|is_between, ":slot_val", -1, 1),#0 or -1
            (neg|is_between, ":slot_val", heroes_begin, heroes_end),
            (troop_set_slot, ":troop_no", slot_troop_stance_on_faction_issue, -1),
         (try_end),
      (try_end),
   (try_end),

   (assign, reg1, ":save_reg1"),#Revert register
   (assign, reg0, ":save_reg0"),#Revert register

   #Ensure $character_gender is set correctly
   (try_begin),
      (call_script, "script_cf_dplmc_troop_is_female", "trp_player"),
	  (assign, "$character_gender", 1),
   (else_try),
	  (assign, "$character_gender", 0),
   (try_end),
   ##diplomacy end+
   
   
   #The following scripts are to end quests which should have cancelled, but did not because of a bug
   (try_begin),
	(check_quest_active, "qst_formal_marriage_proposal"),
	(check_quest_failed, "qst_formal_marriage_proposal"),
    (call_script, "script_end_quest", "qst_formal_marriage_proposal"),
   (try_end),
   
   (try_begin),
	(check_quest_active, "qst_lend_companion"),
	(quest_get_slot, ":giver_troop", "qst_lend_companion", slot_quest_giver_troop),
	(store_faction_of_troop, ":giver_troop_faction", ":giver_troop"),
    (store_relation, ":faction_relation", ":giver_troop_faction", "$players_kingdom"),
    (this_or_next|lt, ":faction_relation", 0),
    (neg|is_between, ":giver_troop_faction", kingdoms_begin, kingdoms_end),
    (call_script, "script_abort_quest", "qst_lend_companion", 0),
   (try_end),


   
   (try_begin),
	(is_between, "$players_kingdom", kingdoms_begin, kingdoms_end),
	(neq, "$players_kingdom", "fac_player_supporters_faction"),
    (faction_slot_eq, "$players_kingdom", slot_faction_marshall, "trp_player"),
    (val_add, "$g_player_days_as_marshal", 1),
   (else_try),
    (assign, "$g_player_days_as_marshal", 0),
   (try_end),
   
   (try_for_range, ":town", towns_begin, towns_end),
	(party_get_slot, ":days_to_completion", ":town", slot_center_player_enterprise_days_until_complete),
    (ge, ":days_to_completion", 1),
	(val_sub, ":days_to_completion", 1),
	(party_set_slot, ":town", slot_center_player_enterprise_days_until_complete, ":days_to_completion"), 
   (try_end),
    ]),
  (24,
   []),
  (24,
   []),
  (24,
   []),
  (24,
   []),
  (24,
   []),
]
