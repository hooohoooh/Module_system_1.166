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

simple_triggers_gekokujo = [
  (1,
   [
	#gekokujo don't change training ground position from default if possible
    #  (try_begin),
    #    (eq, "$training_ground_position_changed", 0),
    #    (assign, "$training_ground_position_changed", 1),
	#	(set_fixed_point_multiplier, 100),
    #    (position_set_x, pos0, 7050),
    #    (position_set_y, pos0, 7200),
    #    (party_set_position, "p_training_ground_3", pos0),
    #  (try_end),
	
#	#gekokujo move kobe, hyogo, and training ground 4 from 1.9
#      (try_begin),
#        (eq, "$training_ground_position_changed", 0),
#        (assign, "$training_ground_position_changed", 1),
#		(set_fixed_point_multiplier, 100),
#		
#		#kobe castle -> sumoto castle
#        (position_set_x, pos0, -12800),
#        (position_set_y, pos0, -20200),		
#        (party_set_position, "p_castle_6", pos0),
#		
#		#hyogo -> sumoto
#        (position_set_x, pos1, -12900),
#        (position_set_y, pos1, -20600),
#        (party_set_position, "p_village_26", pos1),
#		
#		#training ground 4 awaji -> iga
#        (position_set_x, pos2, -21780),
#        (position_set_y, pos2, -17780),
#        (party_set_position, "p_training_ground_4", pos2),
#      (try_end),



 #kamigyo is renamed to keihoku because kamigyo is where the imperial palace is
	  #imperial palace is going to be in a future version of gekokujo and shouldn't be a village
	  #kameoka should also be further out
	  #(try_begin),
	  #  (eq, "$kyoto_changed", 0),
		#(assign, "$kyoto_changed", 1),
		#
		#(set_fixed_point_multiplier, 100),
		#
		#(party_set_name, "p_village_16", "@Keihoku"), #kamigyo-keihoku
		#
		#(position_set_x, pos2, -9580), #from -8880
		#(position_set_y, pos2, -16600), #from -16900
		#(party_set_position, "p_village_17", pos2), #kameoka's new position
    #    
    #    #use this for kanto fixes as well
		#(position_set_x, pos2, 9430), #from -9930
		#(position_set_y, pos2, -12000), #from -12500
		#(party_set_position, "p_castle_49", pos2), #kawagoe castle's new position
    #    
		#(position_set_x, pos2, 9630), #from -10130
		#(position_set_y, pos2, -12150), #from -12650
		#(party_set_position, "p_village_136", pos2), #kawagoe's new position
    #    
		#(party_set_name, "p_village_112", "@Bubaigawara"), #shiki-bubaigawara
		#(position_set_x, pos2, 10300), #from 10650
		#(position_set_y, pos2, -13400), #from -12150
		#(party_set_position, "p_village_112", pos2), #bubaigawara's new position
    #    
		#(party_set_name, "p_village_3", "@Oizumi"), #kiyose-oizumi
    #    
		#(party_set_name, "p_village_1", "@Atsugi"), #yamakita-atsugi
		#(position_set_x, pos2, 8800), #from 8350
		#(position_set_y, pos2, -14200), #from -15000
		#(party_set_position, "p_village_1", pos2), #atsugi's new position
    #    
    #    #gekokujo 3.1 bogmir's quests start
    #    #let's hijack this for the hidden village
    #    (party_set_name, "p_hidden_village", "@Hidden"), #p_reserved_5 is now p_hidden_village
    #    (party_set_icon, "p_hidden_village", "icon_bandit_lair"),
    #    (party_set_flags, "p_hidden_village", pf_disabled, 0),
    #    (party_set_flags, "p_hidden_village", pf_hide_defenders, 1),
    #    (party_set_faction, "p_hidden_village", "fac_neutral"),
    #    (position_set_x, pos2, -5500),
    #    (position_set_y, pos2, -16300),
    #    (party_set_position, "p_hidden_village", pos2), #hidden village moved north of the pass at iga
    #    (party_clear, "p_hidden_village"),
    #    #gekokujo 3.1 bogmir's quests end
		#
	  #(try_end),
	  #gekokujo 3.1 kyoto changes end

      #gekokujo 3.0 move hamada castle 1 unit south start
	  #this is only for fixing existing beta saves. this is not necessary for new games
	  #disable this on release
      #(try_begin),
      #  (eq, "$training_ground_position_changed", 0),
      #  (assign, "$training_ground_position_changed", 1),
		
	  #  (set_fixed_point_multiplier, 100),
      #  (position_set_x, pos2, -25420),
      #  (position_set_y, pos2, -17230),
		
      #  (party_set_position, "p_castle_25", pos2),
		
		#get whoever is stuck back to land by piling them on top of each other next to hamada
		#i don't even know if this will work or if it will be a disaster
		
      #  (position_set_x, pos2, -25520), #1 unit east
      #  (position_set_y, pos2, -17330), #1 unit south
		
	  #  (try_for_parties, ":party_no"),
      #    (party_get_current_terrain, ":current_terrain", ":party_no"),
      #    (eq, ":current_terrain", rt_river),
	  #    (party_set_position, ":party_no", pos2),
      #  (try_end),
      #(try_end),
      #gekokujo 3.0 move hamada castle 1 unit south start
	  
      (gt,"$auto_besiege_town",0),
      (gt,"$g_player_besiege_town", 0),
      (ge, "$g_siege_method", 1),
      (store_current_hours, ":cur_hours"),
      (eq, "$g_siege_force_wait", 0),
      (ge, ":cur_hours", "$g_siege_method_finish_hours"),
      (neg|is_currently_night),
      (rest_for_hours, 0, 0, 0), #stop resting
    ]),
  (0,
   [
      (try_begin),
        (eq, "$bug_fix_version", 0),     
      
        #fix for hiding test_scene in older savegames
        (disable_party, "p_test_scene"),
        #fix for correcting town_1 siege type #gekokujo deprecated
        #(party_set_slot, "p_town_1", slot_center_siege_with_belfry, 0),
        #fix for hiding player_faction notes
        (faction_set_note_available, "fac_player_faction", 0),
        #fix for hiding faction 0 notes
        (faction_set_note_available, "fac_no_faction", 0),
        #fix for removing kidnapped girl from party
        (try_begin),
          (neg|check_quest_active, "qst_kidnapped_girl"),
          (party_remove_members, "p_main_party", "trp_kidnapped_girl", 1),
        (try_end),
        #fix for not occupied but belong to a faction lords
        (try_for_range, ":cur_troop", lords_begin, lords_end),
          (try_begin),                
            (troop_slot_eq, ":cur_troop", slot_troop_occupation, slto_inactive),
            (store_troop_faction, ":cur_troop_faction", ":cur_troop"),
            (is_between, ":cur_troop_faction", "fac_kingdom_1", kingdoms_end),          
            (troop_set_slot, ":cur_troop", slot_troop_occupation, slto_kingdom_hero),          
          (try_end),
        (try_end),  
        #fix for an error in 1.105, also fills new slot values
        (call_script, "script_initialize_item_info"),  
		
        #gekokujo forgot to call these in 1.9
		(faction_set_slot, "fac_culture_20", slot_faction_town_walker_male_troop, "trp_town_walker_1"),
        (faction_set_slot, "fac_culture_20", slot_faction_town_walker_female_troop, "trp_town_walker_2"),
        (faction_set_slot, "fac_culture_20", slot_faction_village_walker_male_troop, "trp_village_walker_1"),
        (faction_set_slot, "fac_culture_20", slot_faction_village_walker_female_troop, "trp_village_walker_2"),
        (faction_set_slot, "fac_culture_20", slot_faction_town_spy_male_troop, "trp_spy_walker_1"),
        (faction_set_slot, "fac_culture_20", slot_faction_town_spy_female_troop, "trp_spy_walker_2"),
		
        (assign, "$bug_fix_version", 1),     
      (try_end),  

      (eq,"$g_player_is_captive",1),
      (gt, "$capturer_party", 0),
      (party_is_active, "$capturer_party"),
      (party_relocate_near_party, "p_main_party", "$capturer_party", 0),
    ]),
  

#Party AI: pruning some of the prisoners in each center (once a week)
  (24*7,
   [
       #gekokujo 3.1 fort prison fix start
	   #cull fort prisons too, but don't give money to anyone -- these are escapees
	   #(try_for_range, ":center_no", centers_begin, centers_end),
	   (try_for_range, ":center_no", centers_begin, forts_end),
       #gekokujo 3.1 fort prison fix end
         (party_get_num_prisoner_stacks, ":num_prisoner_stacks",":center_no"),
         (try_for_range_backwards, ":stack_no", 0, ":num_prisoner_stacks"),
           (party_prisoner_stack_get_troop_id, ":stack_troop",":center_no",":stack_no"),
           (neg|troop_is_hero, ":stack_troop"),
           (party_prisoner_stack_get_size, ":stack_size",":center_no",":stack_no"),
           (store_random_in_range, ":rand_no", 0, 40),
           (val_mul, ":stack_size", ":rand_no"),
           (val_div, ":stack_size", 100),
           (party_remove_prisoners, ":center_no", ":stack_troop", ":stack_size"),
		   ##diplomacy start+ add prisoner value to center wealth
		   (try_begin),
		      (ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_HIGH),#must be explicitly enabled
			  (ge, ":center_no", 1),
			  (this_or_next|party_slot_eq, ":center_no", slot_party_type, spt_town),
				(party_slot_eq, ":center_no", slot_party_type, spt_castle),
			  (party_slot_ge, ":center_no", slot_town_lord, 1),#"wealth" isn't used for player garrisons
			  (party_get_slot, ":cur_wealth", ":center_no", slot_town_wealth),
			  (lt, ":cur_wealth", 6000),
			  (store_mul, ":ransom_profits", ":stack_size", 10),#a fraction of what it could be sold for (50 would be a rule of thumb)
			  (val_add, ":cur_wealth", ":ransom_profits"),
			  (party_set_slot, ":center_no", slot_town_wealth, ":cur_wealth"),
		   (try_end),
		   ##diplomacy end+
         (try_end),
       (try_end),
    ]),
  #gekokujo 3.0 microfactions! have garrisons refresh every week start
  #let's hijack an existing, but unused simple trigger for this -- convenient!
  ##Converging center prosperity to ideal prosperity once in every 15 days
  #(24*15,
  # []),
  (24*7,[
    (try_for_range, ":center_no", forts_begin, forts_end),
	  (party_slot_eq, ":center_no", slot_fort_timer, 0), #countdown reached 0
	  (party_slot_eq, ":center_no", slot_fort_captured, 0), #the player doesn't own it
	  
	  (party_clear, ":center_no"), #empty it out first
	  
	  (try_begin),
		(party_slot_eq, ":center_no", slot_fort_type, sft_village), #ainu villages don't get mercenaries
		(store_random_in_range, ":rand_recruits", 15, 62), #15 to 61, so that there will always be at least 15 of each
		(store_sub, ":rand_bandits", 76, ":rand_recruits"),
		(assign, ":rand_melee", 0),
	  (else_try),
		(store_random_in_range, ":rand_recruits", 10, 41), #10 to 40, so that there will always be at least 10 of each
		(store_sub, ":rand_bandits", 50, ":rand_recruits"),
		(store_random_in_range, ":rand_melee", 5, 22), #5 to 21, so that there will always be at least 5 of each
		(store_sub, ":rand_ranged", 26, ":rand_melee"),
	  (try_end),

	  (party_get_slot, ":recruit", ":center_no", slot_fort_recruit_type),
	  (party_get_slot, ":bandit", ":center_no", slot_fort_bandit_type),
	  (party_add_members, ":center_no", ":recruit", ":rand_recruits"),
	  (party_add_members, ":center_no", ":bandit", ":rand_bandits"),

	  (try_begin),
		(neq, ":rand_melee", 0),
		(party_add_members, ":center_no", "trp_hired_warrior", ":rand_melee"),
		(party_add_members, ":center_no", "trp_hired_gunner", ":rand_ranged"),
	  (try_end),
	(try_end),
    ]),
  #gekokujo 3.0 microfactions! have garrisons refresh every week end

  #Checking if the troops are resting at a half payment point
  (6,
   [(store_current_day, ":cur_day"),
    (try_begin),
      (neq, ":cur_day", "$g_last_half_payment_check_day"),
      (assign, "$g_last_half_payment_check_day", ":cur_day"),
      (try_begin),
        (eq, "$g_half_payment_checkpoint", 1),
        (val_add, "$g_cur_week_half_daily_wage_payments", 1), #half payment for yesterday
      (try_end),
      (assign, "$g_half_payment_checkpoint", 1),
    (try_end),
    (assign, ":resting_at_manor_or_walled_center", 0),
    (try_begin),
      (neg|map_free),
      (ge, "$g_last_rest_center", 0),
      (this_or_next|party_slot_eq, "$g_last_rest_center", slot_center_has_manor, 1),
      (is_between, "$g_last_rest_center", walled_centers_begin, walled_centers_end),
      (assign, ":resting_at_manor_or_walled_center", 1),
    (else_try),
	  #gekokujo 3.0 microfactions! start
	  #let's include resting in a fort
      (neg|map_free),
      (ge, "$g_last_rest_center", 0),
      (is_between, "$g_last_rest_center", forts_begin, forts_end),
      (assign, ":resting_at_manor_or_walled_center", 1),
	  #gekokujo 3.0 microfactions! end
    (try_end),
    (eq, ":resting_at_manor_or_walled_center", 0),
    (assign, "$g_half_payment_checkpoint", 0),
    ]),
  #diplomatic indices
  #gekokujo 2.1 split diplomatic indices so some go every day and some go every 4 days
  #this is where the ones that happened 4 every days remained
  #gekokujo 3.0 changed it so that the split is so that random provocations have their own trigger
  (24,
	[
	#Random Provocations
	(try_begin),
		#1. pick a random village
		(store_random_in_range, ":acting_village", villages_begin, villages_end),
		(store_faction_of_party, ":acting_faction", ":acting_village"),
		
		##gekokujo debug start
		#(str_store_party_name, s8, ":acting_village"),
		#(str_store_faction_name, s9, ":acting_faction"),
		#(display_log_message, "@Provoking Village: {s8} of the {s9}"),
		##gekokujo debug end
		
		#2. find all the villages within 60 units from non-allied factions
		(assign, ":no_villages", 0),
		(try_for_range, ":cur_village", villages_begin, villages_end),
			(store_faction_of_party, ":cur_faction", ":cur_village"),
			(neq, ":cur_faction", ":acting_faction"),
			
			(call_script, "script_diplomacy_faction_get_diplomatic_status_with_faction", ":cur_faction", ":acting_faction"),
			(eq, reg0, 0),
			
			(set_fixed_point_multiplier, 1),
			(store_distance_to_party_from_party, ":distance", ":cur_village", ":acting_village"),
			(lt, ":distance", 60),
			
			(val_add, ":no_villages", 1),
		(try_end),
		
		##gekokujo debug start
		#(assign, reg9, ":no_villages"),
		#(display_log_message, "@Potential Target Villages: {reg9}"),
		##gekokujo debug end
		
		#2.a fail if there are no villages
		(gt, ":no_villages", 0),
		
		#3. pick one of those random villages
		(store_random_in_range, ":random_village", 0, ":no_villages"),
		(assign, ":no_villages", 0),
		(assign, ":result", -1),
		(try_for_range,":cur_village", villages_begin, villages_end),
			(eq, ":result", -1),
			
			(store_faction_of_party, ":cur_faction", ":cur_village"),
			(neq, ":cur_faction", ":acting_faction"),
			
			(call_script, "script_diplomacy_faction_get_diplomatic_status_with_faction", ":cur_faction", ":acting_faction"),
			(eq, reg0, 0),
			
			(set_fixed_point_multiplier, 1),
			(store_distance_to_party_from_party, ":distance", ":cur_village", ":acting_village"),
			(lt, ":distance", 60),
			
			(val_add, ":no_villages", 1),
			
			(gt, ":no_villages", ":random_village"),
			(assign, ":result", ":cur_village"),
		(try_end),
		
		(assign, ":target_village", ":result"),
		(store_faction_of_party, ":target_faction", ":target_village"),
		
		##gekokujo debug start
		#(str_store_party_name, s8, ":target_village"),
		#(str_store_faction_name, s9, ":target_faction"),
		#(display_log_message, "@Target Village: {s8} of the {s9}"),
		##gekokujo debug end
		
		##gekokujo debug start
		#(str_store_faction_name, s8, ":acting_faction"),
		#(str_store_faction_name, s9, ":target_faction"),
		#(display_log_message, "@{s9} provoked by the {s8}"),
		##gekokujo debug end
		
		#4. pick the type of provocation
		(try_begin),
			#acting village formerly owned by target faction
			(this_or_next|party_slot_eq, ":acting_village", slot_center_original_faction, ":target_faction"),
			(party_slot_eq, ":acting_village", slot_center_ex_faction, ":target_faction"),
			
			(str_store_party_name, s1, ":acting_village"),
		    (str_store_faction_name, s3, ":acting_faction"),
		    (str_store_faction_name, s4, ":target_faction"),
			(faction_get_slot, ":target_leader", ":target_faction", slot_faction_leader),
		    (str_store_troop_name, s5, ":target_leader"),
			
			(str_store_string, s9, "str_local_notables_from_s1_a_village_claimed_by_the_s4_have_been_mistreated_by_their_overlords_from_the_s3_and_petition_s5_for_protection"),
			(display_log_message, "@There has been an alleged border incident: {s9}"),
			
			(call_script, "script_add_log_entry", logent_border_incident_subjects_mistreated, ":acting_village", -1, -1, ":acting_faction"),
		(else_try),
			#acting village has never been owned by target faction
			(str_store_party_name, s1, ":acting_village"),
			(str_store_party_name, s2, ":target_village"),
			
			(store_random_in_range, ":random", 0, 3),
			(try_begin),
				(eq, ":random", 0),

				(str_store_string, s9, "str_villagers_from_s1_stole_some_cattle_from_s2"),
				(display_log_message, "@There has been an alleged border incident: {s9}"),
				(call_script, "script_add_log_entry", logent_border_incident_cattle_stolen, ":acting_village", ":target_village", -1,":acting_faction"),
			(else_try),
				(eq, ":random", 1),

				(str_store_string, s9, "str_villagers_from_s1_abducted_a_woman_from_a_prominent_family_in_s2_to_marry_one_of_their_boys"),
				(display_log_message, "@There has been an alleged border incident: {s9}"),				
				(call_script, "script_add_log_entry", logent_border_incident_bride_abducted, ":acting_village", ":target_village", -1, ":acting_faction"),
			(else_try),	
				(eq, ":random", 2),
				
				(str_store_string, s9, "str_villagers_from_s1_killed_some_farmers_from_s2_in_a_fight_over_the_diversion_of_a_stream"),
				(display_log_message, "@There has been an alleged border incident: {s9}"),
			    (call_script, "script_add_log_entry", logent_border_incident_villagers_killed, ":acting_village", ":target_village", -1,":acting_faction"),
			(try_end),
		(try_end),
		
		#(str_store_faction_name, s3, ":acting_faction"),
		#(str_store_faction_name, s4, ":target_faction"),
		
		(store_add, ":slot_provocation_days", ":acting_faction", slot_faction_provocation_days_with_factions_begin),
		(val_sub, ":slot_provocation_days", kingdoms_begin),
		(faction_set_slot, ":target_faction", ":slot_provocation_days", 60),
		
		#Old Random Provocation Start
		#(store_random_in_range, ":acting_village", villages_begin, villages_end),
		#(store_random_in_range, ":target_village", villages_begin, villages_end),
		#(store_faction_of_party, ":acting_faction", ":acting_village"),
		#(store_faction_of_party, ":target_faction", ":target_village"), #target faction receives the provocation
		#(neq, ":acting_village", ":target_village"),
		#(neq, ":acting_faction", ":target_faction"),
		
		#(call_script, "script_diplomacy_faction_get_diplomatic_status_with_faction", ":target_faction", ":acting_faction"),
		#(eq, reg0, 0),
		
		#(try_begin),
		#	(party_slot_eq, ":acting_village", slot_center_original_faction, ":target_faction"),
		#	(call_script, "script_add_notification_menu", "mnu_notification_border_incident", ":acting_village", -1),
		#(else_try),
		#	(party_slot_eq, ":acting_village", slot_center_ex_faction, ":target_faction"),
		#	(call_script, "script_add_notification_menu", "mnu_notification_border_incident", ":acting_village", -1),
		#(else_try),
		#	(lt, ":distance", 25),
		#	(call_script, "script_add_notification_menu", "mnu_notification_border_incident", ":acting_village", ":target_village"),
		#(try_end),
		#Old Random Provocation End
	(try_end),
	]),
		
    #POLITICAL TRIGGERS
	#POLITICAL TRIGGER #1`
	#gekokujo 3.0 reduce political triggers
   (12, #decreased from 8
    [	  
	(call_script, "script_cf_random_political_event"),
	
	#Added Nov 2010 begins - do this twice
	(call_script, "script_cf_random_political_event"),
	#Added Nov 2010 ends
	
	#This generates quarrels and occasional reconciliations and interventions	
	]),
    #gekokujo 3.1 rebellions end

  # Process alarms - perhaps break this down into several groups, with a modula
   (1, #this now calls 1/3 of all centers each time, thus hopefully lightening the CPU load
   [
     (call_script, "script_process_alarms"),

     (call_script, "script_allow_vassals_to_join_indoor_battle"),
     
     (call_script, "script_process_kingdom_parties_ai"),
   ]),
		
  # During rebellion, removing troops from player faction randomly because of low relation points
  # Deprecated -- should be part of regular political events


  # Reset kingdom lady current centers
##   (28,
##   [
##       (try_for_range, ":troop_no", heroes_begin, heroes_end),
##         (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_lady),
##
##         # Find the active quest ladies
##         (assign, ":not_ok", 0),
##         (try_for_range, ":quest_no", lord_quests_begin, lord_quests_end),
##           (eq, ":not_ok", 0),
##           (check_quest_active, ":quest_no"),
##           (quest_slot_eq, ":quest_no", slot_quest_object_troop, ":troop_no"),
##           (assign, ":not_ok", 1),
##         (try_end),
##         (eq, ":not_ok", 0),
##
##         (troop_get_slot, ":troop_center", ":troop_no", slot_troop_cur_center),
##         (assign, ":is_under_siege", 0),
##         (try_begin),
##           (is_between, ":troop_center", walled_centers_begin, walled_centers_end),
##           (party_get_battle_opponent, ":besieger_party", ":troop_center"),
##           (gt, ":besieger_party", 0),
##           (assign, ":is_under_siege", 1),
##         (try_end),
##
##         (eq, ":is_under_siege", 0),# Omit ladies in centers under siege
##
##         (try_begin),
##           (store_random_in_range, ":random_num",0, 100),
##           (lt, ":random_num", 20),
##           (store_troop_faction, ":cur_faction", ":troop_no"),
##           (call_script, "script_cf_select_random_town_with_faction", ":cur_faction"),#Can fail
##           (troop_set_slot, ":troop_no", slot_troop_cur_center, reg0),
##         (try_end),
##       
##         (store_random_in_range, ":random_num",0, 100),
##         (lt, ":random_num", 50),
##         (troop_get_slot, ":lord_no", ":troop_no", slot_troop_father),
##         (try_begin),
##           (eq, ":lord_no", 0),
##           (troop_get_slot, ":lord_no", ":troop_no", slot_troop_spouse),
##         (try_end),
##         (gt, ":lord_no", 0),
##         (troop_get_slot, ":cur_party", ":lord_no", slot_troop_leaded_party),
##         (gt, ":cur_party", 0),
##         (party_get_attached_to, ":cur_center", ":cur_party"),
##         (gt, ":cur_center", 0),
##
##         (troop_set_slot, ":troop_no", slot_troop_cur_center, ":cur_center"),
##       (try_end),
##    ]),


  # Attach Lord Parties to the town they are in
  (0.1,
   [
       (try_for_range, ":troop_no", heroes_begin, heroes_end),
         (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
         (troop_get_slot, ":troop_party_no", ":troop_no", slot_troop_leaded_party),
         (ge, ":troop_party_no", 1),
		 (party_is_active, ":troop_party_no"),
		 
         (party_get_attached_to, ":cur_attached_town", ":troop_party_no"),
         (lt, ":cur_attached_town", 1),
         (party_get_cur_town, ":destination", ":troop_party_no"),
         (is_between, ":destination", centers_begin, centers_end),
         (call_script, "script_get_relation_between_parties", ":destination", ":troop_party_no"),
         (try_begin),
           (ge, reg0, 0),
           (party_attach_to_party, ":troop_party_no", ":destination"),
         (else_try),
           (party_set_ai_behavior, ":troop_party_no", ai_bhvr_hold),
         (try_end),
         
         (try_begin),
           (this_or_next|party_slot_eq, ":destination", slot_party_type, spt_town),
           (party_slot_eq, ":destination", slot_party_type, spt_castle),
           (store_faction_of_party, ":troop_faction_no", ":troop_party_no"),
           (store_faction_of_party, ":destination_faction_no", ":destination"),
           (eq, ":troop_faction_no", ":destination_faction_no"),
           (party_get_num_prisoner_stacks, ":num_stacks", ":troop_party_no"),
           (gt, ":num_stacks", 0),
           (assign, "$g_move_heroes", 1),
           (call_script, "script_party_prisoners_add_party_prisoners", ":destination", ":troop_party_no"),#Moving prisoners to the center
           (assign, "$g_move_heroes", 1),
           (call_script, "script_party_remove_all_prisoners", ":troop_party_no"),
         (try_end),
       (try_end),
	   	   
	   (try_for_parties, ":bandit_camp"),
	 	 (gt, ":bandit_camp", "p_spawn_points_end"),
		 #Can't have party is active here, because it will fail for inactive parties
		 (party_get_template_id, ":template", ":bandit_camp"),
		 (ge, ":template", "pt_seto_pirate_lair"),
		
		 (store_distance_to_party_from_party, ":distance", "p_main_party", ":bandit_camp"),
	     #(lt, ":distance", 3), #gekokujo 3.0 increase bandit camp search range
	     (lt, ":distance", 6),
		 
	     (party_set_flags, ":bandit_camp", pf_disabled, 0),
	     (party_set_flags, ":bandit_camp", pf_always_visible, 1),	   
	   (try_end),
    ]),
  
  # Consuming food at every 14 hours
  (14,
   [
    (eq, "$g_player_is_captive", 0),
    #gekokujo 3.1 labor start
    #disable while working in a village
    (eq, "$gekokujo_labor_disable_food", 0),
    #gekokujo 3.1 labor end
    (party_get_num_companion_stacks, ":num_stacks","p_main_party"),
    (assign, ":num_men", 0),
    (try_for_range, ":i_stack", 0, ":num_stacks"),
      (party_stack_get_size, ":stack_size","p_main_party",":i_stack"),
      (val_add, ":num_men", ":stack_size"),
    (try_end),
    (val_div, ":num_men", 3),
    (try_begin),
      (eq, ":num_men", 0),
      (val_add, ":num_men", 1),
    (try_end),
	
	#gekokujo 3.0 foraging skill start
	## Jrider + FORAGING v1.0, add foraging
	(call_script, "script_forage_for_food"),

    # backup original number for message display
    (assign, ":orig_men", ":num_men"),
    (try_begin), 
      # set min consumption to 1 unit of food in inventory
      (ge, reg4, ":num_men"),
      (assign, ":num_men", 1),
    (else_try),
      # else deduct foraged amount from consumed from party size
      (val_sub, ":num_men", reg4),
    (try_end),
    ## Jrider -
	#gekokujo 3.0 foraging skill end
    
    (try_begin),
      (assign, ":number_of_foods_player_has", 0),
      (try_for_range, ":cur_edible", food_begin, food_end),      
        (call_script, "script_cf_player_has_item_without_modifier", ":cur_edible", imod_rotten),
        (val_add, ":number_of_foods_player_has", 1),
      (try_end),
      (try_begin),
        (ge, ":number_of_foods_player_has", 6),
        (unlock_achievement, ACHIEVEMENT_ABUNDANT_FEAST),        
      (try_end),
    (try_end),
    
    (assign, ":consumption_amount", ":num_men"),
    (assign, ":no_food_displayed", 0),
    (try_for_range, ":unused", 0, ":consumption_amount"),
      (assign, ":available_food", 0),
      (try_for_range, ":cur_food", food_begin, food_end),
        (item_set_slot, ":cur_food", slot_item_is_checked, 0),
        (call_script, "script_cf_player_has_item_without_modifier", ":cur_food", imod_rotten),
        (val_add, ":available_food", 1),
      (try_end),
      (try_begin),
        (gt, ":available_food", 0),
        (store_random_in_range, ":selected_food", 0, ":available_food"),
        (call_script, "script_consume_food", ":selected_food"),
      (else_try),
        (eq, ":no_food_displayed", 0),
        (display_message, "@Party has nothing to eat!", 0xFF0000),
        (call_script, "script_change_player_party_morale", -3),
        (assign, ":no_food_displayed", 1),
#NPC companion changes begin
        (try_begin),
            (call_script, "script_party_count_fit_regulars", "p_main_party"),
            (gt, reg0, 0),
            (call_script, "script_objectionable_action", tmt_egalitarian, "str_men_hungry"),
        (try_end),
#NPC companion changes end
      (try_end),
    (try_end),
	
	#gekokujo 3.0 foraging skill start
    ## Jrider + FORAGING v1.0, call food consummed/left script
    (call_script, "script_food_consumption_display_message", ":orig_men"),
    ## Jrider -
	#gekokujo 3.0 foraging skill end
    ]),
  
  # Updating player icon in every frame
  (0,
   [(troop_get_inventory_slot, ":cur_horse", "trp_player", 8), #horse slot
	(assign, ":new_icon", -1),
    (party_get_num_companions, ":num_men", "p_main_party"),
	(try_begin),
		(eq, "$g_player_icon_state", pis_normal),
		(try_begin),
            #gekokujo 3.1 lord icon for large player parties start
            (ge, ":num_men", 60),
            (assign, ":new_icon", "icon_flagbearer_a"),
            #gekokujo 3.1 lord icon for large player parties end
        (else_try),
            #gekokujo 3.1 lord icon for player leaders start
            (gt, "$players_kingdom", 0),
            (ge, ":num_men", 30), #smaller amount needed to change icon
            (assign, ":new_icon", "icon_flagbearer_a"),
            #gekokujo 3.1 lord icon for player leaders end
        (else_try),
			(ge, ":cur_horse", 0),
			(assign, ":new_icon", "icon_player_horseman"),
		(else_try),
			(eq, "$character_gender", 1), #character is a woman
			(assign, ":new_icon", "icon_woman_b"),
		(else_try),
			(assign, ":new_icon", "icon_player"),
		(try_end),
	(else_try),
		(eq, "$g_player_icon_state", pis_camping),
		(assign, ":new_icon", "icon_camp"),
	(else_try),
		(eq, "$g_player_icon_state", pis_ship),
		(assign, ":new_icon", "icon_ship"),
	(try_end),
	
	#gekokujo 3.0 seafaring start -- let's piggyback this trigger to do our work
	(try_begin),
		(party_get_current_terrain, ":terrain", "p_main_party"),
		(eq, ":terrain", rt_bridge),
		(assign, ":new_icon", "icon_ship"), #don't bother changing $player_icon_state so we don't have to check for the player leaving rt_bridge
	(try_end), 
	#gekokujo 3.0 seafaring end
	
	(try_begin),
		(neq, ":new_icon", "$g_player_party_icon"),
		(assign, "$g_player_party_icon", ":new_icon"),
		(party_set_icon, "p_main_party", ":new_icon"),
	(try_end),
	
	#gekokujo 3.0 seafaring start -- more trigger hijacking
	(try_for_parties, ":cur_party"),
		(party_get_current_terrain, ":cur_terrain", ":cur_party"),
		(party_get_template_id, ":cur_template_id", ":cur_party"),
		(party_get_icon, ":cur_icon", ":cur_party"),
		
		(this_or_next|eq, ":cur_template_id", "pt_dplmc_recruiter"),
		(this_or_next|eq, ":cur_template_id", "pt_dplmc_spouse"),
		(this_or_next|eq, ":cur_template_id", "pt_dplmc_gift_caravan"),
		(is_between, ":cur_template_id", seafaring_parties_begin, seafaring_parties_end),
		
		#let's set the default icon in slot_party_default_icon
		#first: icon_ship is NEVER the default icon
		#second: don't bother changing it if its already set
		#it's probably computationally expensive to keep changing it every frame
		#checks are probably cheaper
		
		#(try_begin),
		#	(neq, ":cur_icon", "icon_ship"), 
		#	(party_get_slot, ":default_icon", ":cur_party", slot_party_default_icon), #fuck fuck fuck
		#	(neq, ":cur_icon", ":default_icon"),  #this didn't turn out to be reliable at all
		#	(party_set_slot, ":cur_party", slot_party_default_icon, ":cur_icon"),
		#(try_end),
		
		(try_begin), #this is such inelegant bullshit
			(this_or_next|eq, ":cur_template_id", "pt_looters"),
			(this_or_next|eq, ":cur_template_id", "pt_seto_pirates"),
			(this_or_next|eq, ":cur_template_id", "pt_kanto_rebels"),
			(this_or_next|eq, ":cur_template_id", "pt_northern_raiders"),
			(this_or_next|eq, ":cur_template_id", "pt_shinano_rebels"),
			(this_or_next|eq, ":cur_template_id", "pt_kinai_rebels"),
			(this_or_next|eq, ":cur_template_id", "pt_woku_pirates"),
			(this_or_next|eq, ":cur_template_id", "pt_monk_rebels"),
            (this_or_next|eq, ":cur_template_id", "pt_jianhuizu"),
			(this_or_next|eq, ":cur_template_id", "pt_troublesome_bandits"),
			(this_or_next|eq, ":cur_template_id", "pt_bandits_awaiting_ransom"),
			(eq, ":cur_template_id", "pt_center_reinforcements"),
			(assign, ":default_icon", "icon_axeman"),
		(else_try),
			(this_or_next|eq, ":cur_template_id", "pt_manhunters"),
			(this_or_next|eq, ":cur_template_id", "pt_merchant_caravan"),
			(this_or_next|eq, ":cur_template_id", "pt_spy_partners"),
			(this_or_next|eq, ":cur_template_id", "pt_spy"),
			(this_or_next|eq, ":cur_template_id", "pt_sacrificed_messenger"),
			(this_or_next|eq, ":cur_template_id", "pt_forager_party"),
			(this_or_next|eq, ":cur_template_id", "pt_scout_party"),
			(this_or_next|eq, ":cur_template_id", "pt_patrol_party"),
			(this_or_next|eq, ":cur_template_id", "pt_messenger_party"),
			(this_or_next|eq, ":cur_template_id", "pt_raider_party"),
			(this_or_next|eq, ":cur_template_id", "pt_prisoner_train_party"),
			(eq, ":cur_template_id", "pt_dplmc_recruiter"),
			(assign, ":default_icon", "icon_gray_knight"),
		(else_try),
			(this_or_next|eq, ":cur_template_id", "pt_kidnapped_girl"),
			(eq, ":cur_template_id", "pt_dplmc_spouse"),
			(assign, ":default_icon", "icon_woman"),
		(else_try),
			(this_or_next|eq, ":cur_template_id", "pt_village_farmers"),
			(eq, ":cur_template_id", "pt_runaway_serfs"),
			(assign, ":default_icon", "icon_peasant"),
		(else_try),
			(this_or_next|eq, ":cur_template_id", "pt_kingdom_caravan_party"),
			(eq, ":cur_template_id", "pt_dplmc_gift_caravan"),
			(assign, ":default_icon", "icon_mule"),
		(else_try),
			(this_or_next|eq, ":cur_template_id", "pt_deserters"),
			(eq, ":cur_template_id", "pt_routed_warriors"),
			(assign, ":default_icon", "icon_vaegir_knight"),
		(else_try),
			(eq, ":cur_template_id", "pt_kingdom_hero_party"),
			(assign, ":default_icon", "icon_flagbearer_a"),
		(try_end),
		
		#remember -- don't bother changing anything if it's already set
		(try_begin),
			(eq, ":cur_terrain", rt_bridge),
			(neq, ":cur_icon", "icon_ship"),
			(party_set_icon, ":cur_party", "icon_ship"),
		(else_try),
			#(eq, ":cur_icon", "icon_ship"),
			(neq, ":cur_terrain", rt_bridge), #oh jesus christ please don't tell me this is actually necessary #damnit apparently it is
			(neq, ":cur_icon", ":default_icon"),
			(party_set_icon, ":cur_party", ":default_icon"),
		(try_end),
	(try_end),
	#gekokujo 3.0 seafaring end
	
    ]),
  
 #Update how good a target player is for bandits
  (2,
   [
       (store_troop_gold, ":total_value", "trp_player"),
	   
	   #gekokujo 3.1 fix bandit swarm start
	   #this was in the wrong spot. it should have been UNDER the loop that added together inventory item values
	   #note: this is an oversight in native, not only gekokujo
       #(store_div, ":bandit_attraction", ":total_value", (10000/100)), #10000 gold = excellent_target
	   #gekokujo 3.1 fix bandit swarm end

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
	   
	   #gekokujo 3.1 fix bandit swarm start
	   #NOW we modify 'total value' into 'bandit_attraction'
	   #since making tons of mon in gekokujo in the endgame is easy (and since we now add inventory value)
	   (store_sqrt, ":bandit_attraction", ":total_value"), #we find the square root first
	   (val_div, ":bandit_attraction", 3), #and THEN we divide it
	   #100000 mon: old attraction = 100, new attraction = 100
	   #10000 mon: old attraction = 100, new attraction = 33
	   #1000 mon: old attraction = 10, new attraction = 11
	   #100 mon: old attraction = 1, new attraction = 3
	   #10 mon: old attraction = 0, new attraction = 1
	   #i have no freaking idea if this is related to the bandit swarms but #YOLO
	   #gekokujo 3.1 fix bandit swarm end
	   
       (val_clamp, ":bandit_attraction", 0, 100),
       (party_set_bandit_attraction, "p_main_party", ":bandit_attraction"),
    ]),
   
  #gekokujo 2.1 split diplomatic indices so some go every day and some go every 4 days
  #this is where the ones that happen every day were moved
  #gekokujo 3.0 changed it so that the split is so that random provocations have their own trigger
  (24,
   [
   (call_script, "script_randomly_start_war_peace_new", 1),
   
   (try_for_range, ":faction_1", kingdoms_begin, kingdoms_end),
		(faction_slot_eq, ":faction_1", slot_faction_state, sfs_active),
		(try_for_range, ":faction_2", kingdoms_begin, kingdoms_end),
			(neq, ":faction_1", ":faction_2"),
			(faction_slot_eq, ":faction_2", slot_faction_state, sfs_active),

			#remove provocations
			(store_add, ":slot_truce_days", ":faction_2", slot_faction_truce_days_with_factions_begin),
			(val_sub, ":slot_truce_days", kingdoms_begin),
			(faction_get_slot, ":truce_days", ":faction_1", ":slot_truce_days"),
			(try_begin),
				(ge, ":truce_days", 1),
				(try_begin),
					(eq, ":truce_days", 1),
					(call_script, "script_update_faction_notes", ":faction_1"),
					(lt, ":faction_1", ":faction_2"),
					#gekokujo diplomacy - less notification menus start
					(str_store_faction_name_link, s1, ":faction_1"),
					(str_store_faction_name_link, s2, ":faction_2"),
					(display_log_message, "@The truce between {s1} and {s2} has expired."),
					(try_begin),
						(this_or_next|eq, "$players_kingdom", ":faction_1"),
						(eq, "$players_kingdom", ":faction_2"),
						(call_script, "script_add_notification_menu", "mnu_notification_truce_expired", ":faction_1", ":faction_2"),
					(try_end),
					#gekokujo diplomacy - less notification menus end,
				##diplomacy begin
				##nested diplomacy start+ Replace "magic numbers" with named constants
				(else_try),
					(eq, ":truce_days", dplmc_treaty_alliance_days_expire + 1),#replaced 61
					(call_script, "script_update_faction_notes", ":faction_1"),
					(lt, ":faction_1", ":faction_2"),
					#gekokujo diplomacy - less notification menus start
					(str_store_faction_name_link, s1, ":faction_1"),
					(str_store_faction_name_link, s2, ":faction_2"),
					(display_log_message, "@The alliance between {s1} and {s2} has expired."),
					(try_begin),
						(this_or_next|eq, "$players_kingdom", ":faction_1"),
						(eq, "$players_kingdom", ":faction_2"),
						(call_script, "script_add_notification_menu", "mnu_dplmc_notification_alliance_expired", ":faction_1", ":faction_2"),
					(try_end),
					#gekokujo diplomacy - less notification menus end
				(else_try),
					(eq, ":truce_days",dplmc_treaty_defense_days_expire + 1),#replaced 41
					(call_script, "script_update_faction_notes", ":faction_1"),
					(lt, ":faction_1", ":faction_2"),
					#gekokujo diplomacy - less notification menus start
					(str_store_faction_name_link, s1, ":faction_1"),
					(str_store_faction_name_link, s2, ":faction_2"),
					(display_log_message, "@The defensive pact between {s1} and {s2} has expired."),
					(try_begin),
						(this_or_next|eq, "$players_kingdom", ":faction_1"),
						(eq, "$players_kingdom", ":faction_2"),
						(call_script, "script_add_notification_menu", "mnu_dplmc_notification_defensive_expired", ":faction_1", ":faction_2"),
					(try_end),
					#gekokujo diplomacy - less notification menus end
				(else_try),
					(eq, ":truce_days", dplmc_treaty_trade_days_expire + 1),#replaced 21
					(call_script, "script_update_faction_notes", ":faction_1"),
					(lt, ":faction_1", ":faction_2"),
					#gekokujo diplomacy - less notification menus start
					(str_store_faction_name_link, s1, ":faction_1"),
					(str_store_faction_name_link, s2, ":faction_2"),
					(display_log_message, "@The trade pact between {s1} and {s2} has expired."),
					(try_begin),
						(this_or_next|eq, "$players_kingdom", ":faction_1"),
						(eq, "$players_kingdom", ":faction_2"),
						(call_script, "script_add_notification_menu", "mnu_dplmc_notification_trade_expired", ":faction_1", ":faction_2"),
					(try_end),
					#gekokujo diplomacy - less notification menus end
				##nested diplomacy end+
				##diplomacy end
				(try_end),
				(val_sub, ":truce_days", 1),
				(faction_set_slot, ":faction_1", ":slot_truce_days", ":truce_days"),
			(try_end),

			(store_add, ":slot_provocation_days", ":faction_2", slot_faction_provocation_days_with_factions_begin),
			(val_sub, ":slot_provocation_days", kingdoms_begin),
			(faction_get_slot, ":provocation_days", ":faction_1", ":slot_provocation_days"),
			(try_begin),
				(ge, ":provocation_days", 1),
				(try_begin),#factions already at war
					(store_relation, ":relation", ":faction_1", ":faction_2"),
					(lt, ":relation", 0),
					(faction_set_slot, ":faction_1", ":slot_provocation_days", 0),
				(else_try), #Provocation expires
					(eq, ":provocation_days", 1),
					#gekokujo diplomacy - less notification menus start
					#kingdom fails to respond is now a display log message unless it involves own faction
					(str_store_faction_name_link, s1, ":faction_1"),
					(str_store_faction_name_link, s2, ":faction_2"),
					(display_log_message, "@{s1} has not responded to {s2}'s provocations."),
					#gekokujo 2.1a oh dear god forgot to add the policy change effect
					(call_script, "script_faction_follows_controversial_policy", ":faction_1", logent_policy_ruler_ignores_provocation),
					#gekokujo diplomacy - on second thought, this is probably not important
					#(try_begin),
					#	(this_or_next|eq, "$players_kingdom", ":faction_1"),
					#	(eq, "$players_kingdom", ":faction_2"),
					#	(call_script, "script_add_notification_menu", "mnu_notification_casus_belli_expired", ":faction_1", ":faction_2"),
					#(try_end),
					#gekokujo diplomacy - less notification menus end
					(faction_set_slot, ":faction_1", ":slot_provocation_days", 0),
				(else_try),
					(val_sub, ":provocation_days", 1),
					(faction_set_slot, ":faction_1", ":slot_provocation_days", ":provocation_days"),
				(try_end),
			(try_end),

			(try_begin), #at war
				(store_relation, ":relation", ":faction_1", ":faction_2"),
				(lt, ":relation", 0),
				(store_add, ":slot_war_damage", ":faction_2", slot_faction_war_damage_inflicted_on_factions_begin),
				(val_sub, ":slot_war_damage", kingdoms_begin),
				(faction_get_slot, ":war_damage", ":faction_1", ":slot_war_damage"),
				(val_add, ":war_damage", 1),
				(faction_set_slot, ":faction_1", ":slot_war_damage", ":war_damage"),
			(try_end),

		(try_end),
		(call_script, "script_update_faction_notes", ":faction_1"),
	(try_end),
   ]),
   
#gekokujo 3.1 random encounters start (triggers)
#please note, submodders, that i *took* 2 empty triggers, and filled them
#i did not add new triggers. the trigger count of 3.0 and 3.1 are the same
#THIS IS FOR SAVE COMPATIBILITY
#if you add triggers, rather than hijacking existing triggers, SAVES WILL NOT BE COMPATIBLE
  (24, #this checks for random events -- only check once every day
   [
	 (eq, "$freelancer_state", 0), #don't trigger while freelancer is on, not even while on leave
     (eq, "$gekokujo_labor_disable_food", 0), #don't trigger while doing labor
     (neq, "$g_gekokujo_encounter_rate", 2), #don't trigger at all if the feature is disabled ffs
	 
	 (party_get_num_companions, ":party_size", "p_main_party"),
	 
	 #first, determine the trigger chance from the party size actual and encounter rate
	 #random encounters are meant for loners, not for generals
	 #they can still happen, just very very rarely
	 (try_begin),
	   (eq, "$g_gekokujo_encounter_rate", 0), #standard mode
	   (try_begin),
	     (eq, ":party_size", 1), #player is alone (triggers most)
		 (assign, ":chance", 50), #50% (once per 2 days)
	   (else_try),
	     (le, ":party_size", 15), #player party has 2 to 15 troops
		 (assign, ":chance", 25), #25% (once per 4 days)
	   (else_try),
	     (le, ":party_size", 30), #player party has 16 to 30 troops
		 (assign, ":chance", 10), #10% (once per 10 days)
	   (else_try),
	     #player party has 31+ troops (triggers least)
		 (assign, ":chance", 5), #5% (once per 20 days)
	   (try_end),
	 (else_try),
	   #reduced mode
	   (try_begin),
	     (eq, ":party_size", 1), #player is alone
		 (assign, ":chance", 25), #25%
	   (else_try),
	     (le, ":party_size", 15), #player party has 2 to 15 troops
		 (assign, ":chance", 10), #10%
	   (else_try),
	     (le, ":party_size", 30), #player party has 16 to 30 troops
		 (assign, ":chance", 5), #5%
	   (else_try),
	     #player party has 31+ troops
		 (assign, ":chance", 0), #0% (never trigger)
	   (try_end),
	 (end_try),
	 
	 #second, roll the dice	and see if it triggers!
	 #if it does trigger, also determine what time of day this should occur
	 #0 means don't trigger at all aka failure
	 #1 means "now", 2 means 6 hours from now, 3 means 12 hours, and 4 means 18 hours
	 #5 *would* mean 24 hours, but thats when the next 24-hour trigger fires
	 (store_random_in_range, ":seed", 0, 100),
	 (try_begin),
	   (le, ":seed", ":chance"), 
	   (store_random_in_range, ":timer", 1, 5),
	 (else_try),
	   (assign, ":timer", 0),
	 (try_end),
	 
	 (assign, "$gekokujo_encounter_timer", ":timer"),
	 
	 ##DEBUG START
	 #(assign, reg11, ":chance"),
	 #(assign, reg12, ":seed"),
	 #(assign, reg13, ":timer"),
	 #(display_log_message, "@Encounter Chance: {reg11}, Encounter Seed: {reg12}, Encounter Timer: {reg13}"),
	 ##DEBUG END
     
     #gekokujo 3.1 fix bandit swarm start
     #let us also use this trigger to reset relations with bandits every day just in case
     #(call_script, "script_set_player_relation_with_faction", "fac_outlaws", -15),
     #(call_script, "script_set_player_relation_with_faction", "fac_deserters", -10),
     #(call_script, "script_set_player_relation_with_faction", "fac_woku_pirates", -15),
     #(call_script, "script_set_player_relation_with_faction", "fac_shinano_rebel", -15), #WHY IS THERE A SHINANO "REBEL" SINGULAR
     #(call_script, "script_set_player_relation_with_faction", "fac_shinano_rebels", -40),
     (set_relation, "fac_outlaws", "fac_player_faction", -15),
     (set_relation, "fac_deserters", "fac_player_faction", -10),
     (set_relation, "fac_woku_pirates", "fac_player_faction", -15),
     (set_relation, "fac_shinano_rebel", "fac_player_faction", -15),
     (set_relation, "fac_shinano_rebels", "fac_player_faction", -40),
     #gekokujo 3.1 fix bandit swarm end
   ]),
   
  (6, #this executes the random events -- separate from the check so that it can happen at different times of day
   [
	 (eq, "$freelancer_state", 0), #don't trigger while freelancer is on, not even while on leave
     (neq, "$g_gekokujo_encounter_rate", 2), #don't trigger at all if the feature is disabled ffs
	 (gt, "$gekokujo_encounter_timer", 0), #0 means either the check failed or the encounter already ran 6+ hours ago
	 
	 ##DEBUG START
	 #(assign, reg14, "$gekokujo_encounter_timer"),
	 #(display_log_message, "@Encounter Timer: {reg14}"),
	 ##DEBUG END
	 
	 (try_begin),
	   (eq, "$gekokujo_encounter_timer", 1), #only run the encounter once timer reaches 1
	   
       (jump_to_menu, "mnu_encounter"),
	   ##DEBUG START
	   #(display_log_message, "@Encounter Triggered"),
	   ##DEBUG END
	 (try_end),
	 
	 (val_sub, "$gekokujo_encounter_timer", 1), #run down the timer
   ]),
#gekokujo 3.1 random encounters end

  (24,
   []),
]
