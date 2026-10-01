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

simple_triggers_politics_ai = [
#Auto-menu
  (0,
   [          
     (try_begin),
       (gt, "$g_last_rest_center", 0),
       (party_get_battle_opponent, ":besieger_party", "$g_last_rest_center"),
       (gt, ":besieger_party", 0),
       (store_faction_of_party, ":encountered_faction", "$g_last_rest_center"),
       (store_relation, ":faction_relation", ":encountered_faction", "fac_player_supporters_faction"),
       (store_faction_of_party, ":besieger_party_faction", ":besieger_party"),
       (store_relation, ":besieger_party_relation", ":besieger_party_faction", "fac_player_supporters_faction"),
       (ge, ":faction_relation", 0),
       (lt, ":besieger_party_relation", 0),
       (start_encounter, "$g_last_rest_center"),
       (rest_for_hours, 0, 0, 0), #stop resting
     (else_try),
       (store_current_hours, ":cur_hours"),
       (assign, ":check", 0),
       (try_begin),
         (neq, "$g_check_autos_at_hour", 0),
         (ge, ":cur_hours", "$g_check_autos_at_hour"),
         (assign, ":check", 1),
         (assign, "$g_check_autos_at_hour", 0),
       (try_end),
       (this_or_next|eq, ":check", 1),
       (map_free),
       (try_begin),
         (ge,"$auto_menu",1),
         (jump_to_menu,"$auto_menu"),
         (assign,"$auto_menu",-1),
       (else_try),
         (ge,"$auto_enter_town",1),
         (start_encounter, "$auto_enter_town"),
       (else_try),
         (ge,"$auto_besiege_town",1),
         (start_encounter, "$auto_besiege_town"),
       (else_try),
         (ge,"$g_camp_mode", 1),
         (assign, "$g_camp_mode", 0),
         (assign, "$g_infinite_camping", 0),
         (assign, "$g_player_icon_state", pis_normal),
         
         (rest_for_hours, 0, 0, 0), #stop camping
                  
         (display_message, "@Breaking camp..."),
       (try_end),
     (try_end),
     ]),
	
 (4, #Locate kingdom ladies
    [
      #change location for all ladies
      (try_for_range, ":troop_id", kingdom_ladies_begin, kingdom_ladies_end),
        ##diplomacy start+ do not set the troop's center when the troop is leading a party
        (troop_slot_eq, ":troop_id", slot_troop_occupation, slto_kingdom_lady),
        (troop_get_slot, ":leaded_party", ":troop_id", slot_troop_leaded_party),
		(try_begin),
			(gt, ":leaded_party", 0),
			(neg|party_is_active, ":leaded_party"),
			(assign, ":leaded_party", -1),
		(try_end),
        (lt, ":leaded_party", 1),#if the value is 0, it's a bug, so overlook it
        ##diplomacy end+
        (neg|troop_slot_ge, ":troop_id", slot_troop_prisoner_of_party, 0),
        (call_script, "script_get_kingdom_lady_social_determinants", ":troop_id"),
        (assign, ":location", reg1),
        (troop_set_slot, ":troop_id", slot_troop_cur_center, ":location"),
      (try_end),
	]),
	#courtship reset
  (72,
   [
     (assign, "$lady_flirtation_location", 0),
    ]),
	#reset time to spare
  (4,
   [
     (assign, "$g_time_to_spare", 1),

    (try_begin),
		(troop_slot_ge, "trp_player", slot_troop_spouse, active_npcs_begin),
		(assign, "$g_player_banner_granted", 1),
	(try_end),

	 ]),
		
  # Give some xp to hero parties
   (48,
   [
       ##diplomacy start+
       ##change to allow promoted kingdom ladies to hire troops
       #(try_for_range, ":troop_no", active_npcs_begin, active_npcs_end),
       (try_for_range, ":troop_no", heroes_begin, heroes_end),
       ##diplomacy end+
         (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),

         (troop_get_slot, ":hero_party", ":troop_no", slot_troop_leaded_party),
         (gt, ":hero_party", centers_end),
         (party_is_active, ":hero_party"),

         (store_skill_level, ":trainer_level", skl_trainer, ":troop_no"),
         (val_add, ":trainer_level", 5), #average trainer level is 3 for npc lords, worst : 0, best : 6
         (store_mul, ":xp_gain", ":trainer_level", 1000), #xp gain in two days of period for each lord, average : 8000.

         (assign, ":max_accepted_random_value", 30),
         (try_begin),
           (store_troop_faction, ":cur_troop_faction", ":troop_no"),
           (neq, ":cur_troop_faction", "$players_kingdom"),

           (game_get_reduce_campaign_ai, ":reduce_campaign_ai"),
           (try_begin),
             (eq, ":reduce_campaign_ai", 0), #hard (1.5x)
             (assign, ":max_accepted_random_value", 35),
             (val_mul, ":xp_gain", 3),
             (val_div, ":xp_gain", 2),
           (else_try),
             (eq, ":reduce_campaign_ai", 2), #easy (0.5x)
             (assign, ":max_accepted_random_value", 25),
             (val_div, ":xp_gain", 2),
           (try_end),
         (try_end),

         (store_random_in_range, ":rand", 0, 100),
         (le, ":rand", ":max_accepted_random_value"),

         (party_upgrade_with_xp, ":hero_party", ":xp_gain"),
       (try_end),

       (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
         (party_get_slot, ":center_lord", ":center_no", slot_town_lord),
         (neq, ":center_lord", "trp_player"),

         (assign, ":xp_gain", 3000), #xp gain in two days of period for each center, average : 3000.

         (assign, ":max_accepted_random_value", 30),
         (try_begin),
           (assign, ":cur_center_lord_faction", -1),
           (try_begin),
             (ge, ":center_lord", 0),
             (store_troop_faction, ":cur_center_lord_faction", ":center_lord"),
           (try_end),
           (neq, ":cur_center_lord_faction", "$players_kingdom"),

           (game_get_reduce_campaign_ai, ":reduce_campaign_ai"),
           (try_begin),
             (eq, ":reduce_campaign_ai", 0), #hard (1.5x)
             (assign, ":max_accepted_random_value", 35),
             (val_mul, ":xp_gain", 3),
             (val_div, ":xp_gain", 2),
           (else_try),
             (eq, ":reduce_campaign_ai", 2), #easy (0.5x)
             (assign, ":max_accepted_random_value", 25),
             (val_div, ":xp_gain", 2),
           (try_end),
         (try_end),

         (store_random_in_range, ":rand", 0, 100),
         (le, ":rand", ":max_accepted_random_value"),

         (party_upgrade_with_xp, ":center_no", ":xp_gain"),
       (try_end),
    ]),
  # Process sieges
   (24,
   [
       (call_script, "script_process_sieges"),
    ]),
  # Decide vassal ai
   (7,
    [
      (call_script, "script_init_ai_calculation"),
      #(call_script, "script_decide_kingdom_party_ais"),
	  ##diplomacy start+
	  #Also call script_calculate_troop_ai for kingdom ladies who have become slto_kingdom_heroes
      #(try_for_range, ":troop_no", active_npcs_begin, active_npcs_end),
	  (try_for_range, ":troop_no", heroes_begin, heroes_end),
	  ##diplomacy end+
        (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
        (call_script, "script_calculate_troop_ai", ":troop_no"),
      (try_end),
      ]),
  # Hold regular marshall elections for players_kingdom
   (24, #Disabled in favor of new system
    [
    #  (val_add, "$g_election_date", 1),
    #  (ge, "$g_election_date", 90), #elections holds once in every 90 days.
    #  (is_between, "$players_kingdom", kingdoms_begin, kingdoms_end),
    #  (neq, "$players_kingdom", "fac_player_supporters_faction"),
    #  (assign, "$g_presentation_input", -1),
    #  (assign, "$g_presentation_marshall_selection_1_vote", 0),
    #  (assign, "$g_presentation_marshall_selection_2_vote", 0),

    #  (assign, "$g_presentation_marshall_selection_max_renown_1", -10000),
    #  (assign, "$g_presentation_marshall_selection_max_renown_2", -10000),
    #  (assign, "$g_presentation_marshall_selection_max_renown_3", -10000),
    #  (assign, "$g_presentation_marshall_selection_max_renown_1_troop", -10000),
    #  (assign, "$g_presentation_marshall_selection_max_renown_2_troop", -10000),
    #  (assign, "$g_presentation_marshall_selection_max_renown_3_troop", -10000),
    #  (assign, ":num_men", 0),
    #  (try_for_range, ":loop_var", "trp_kingdom_heroes_including_player_begin", active_npcs_end),
    #    (assign, ":cur_troop", ":loop_var"),
    #    (assign, ":continue", 0),
    #    (try_begin),
    #      (eq, ":loop_var", "trp_kingdom_heroes_including_player_begin"),
    #      (assign, ":cur_troop", "trp_player"),
    #      (try_begin),
    #        (eq, "$g_player_is_captive", 0),
    #        (assign, ":continue", 1),
    #      (try_end),
    #    (else_try),
#		  (troop_slot_eq, ":cur_troop", slot_troop_occupation, slto_kingdom_hero),
 #         (store_troop_faction, ":cur_troop_faction", ":cur_troop"),
 #         (eq, "$players_kingdom", ":cur_troop_faction"),
  #        #(troop_slot_eq, ":cur_troop", slot_troop_is_prisoner, 0),
  #        (neg|troop_slot_ge, ":cur_troop", slot_troop_prisoner_of_party, 0),
   #       (troop_slot_ge, ":cur_troop", slot_troop_leaded_party, 1),
    #      (troop_slot_eq, ":cur_troop", slot_troop_occupation, slto_kingdom_hero),
    #      (neg|faction_slot_eq, ":cur_troop_faction", slot_faction_leader, ":cur_troop"),
    #      (troop_get_slot, ":cur_party", ":cur_troop", slot_troop_leaded_party),
    #      (gt, ":cur_party", 0),
    #      (party_is_active, ":cur_party"),
    #      (call_script, "script_party_count_fit_for_battle", ":cur_party"),
    #      (assign, ":party_fit_for_battle", reg0),
    #      (call_script, "script_party_get_ideal_size", ":cur_party"),
    #      (assign, ":ideal_size", reg0),
    #      (store_mul, ":relative_strength", ":party_fit_for_battle", 100),
    #      (val_div, ":relative_strength", ":ideal_size"),
    #      (ge, ":relative_strength", 25),
    #      (assign, ":continue", 1),
    #    (try_end),
    #    (eq, ":continue", 1),
    #    (val_add, ":num_men", 1),
    #    (troop_get_slot, ":renown", ":cur_troop", slot_troop_renown),
    #    (try_begin),
    #      (gt, ":renown", "$g_presentation_marshall_selection_max_renown_1"),
    #      (assign, "$g_presentation_marshall_selection_max_renown_3", "$g_presentation_marshall_selection_max_renown_2"),
    #      (assign, "$g_presentation_marshall_selection_max_renown_2", "$g_presentation_marshall_selection_max_renown_1"),
    #      (assign, "$g_presentation_marshall_selection_max_renown_1", ":renown"),
    #      (assign, "$g_presentation_marshall_selection_max_renown_3_troop", "$g_presentation_marshall_selection_max_renown_2_troop"),
    #      (assign, "$g_presentation_marshall_selection_max_renown_2_troop", "$g_presentation_marshall_selection_max_renown_1_troop"),
    #      (assign, "$g_presentation_marshall_selection_max_renown_1_troop", ":cur_troop"),
    #    (else_try),
    #      (gt, ":renown", "$g_presentation_marshall_selection_max_renown_2"),
    #      (assign, "$g_presentation_marshall_selection_max_renown_3", "$g_presentation_marshall_selection_max_renown_2"),
    #      (assign, "$g_presentation_marshall_selection_max_renown_2", ":renown"),
    #      (assign, "$g_presentation_marshall_selection_max_renown_3_troop", "$g_presentation_marshall_selection_max_renown_2_troop"),
    #      (assign, "$g_presentation_marshall_selection_max_renown_2_troop", ":cur_troop"),
    #    (else_try),
    #      (gt, ":renown", "$g_presentation_marshall_selection_max_renown_3"),
    #      (assign, "$g_presentation_marshall_selection_max_renown_3", ":renown"),
    #      (assign, "$g_presentation_marshall_selection_max_renown_3_troop", ":cur_troop"),
    #    (try_end),
    #  (try_end),
    #  (ge, "$g_presentation_marshall_selection_max_renown_1_troop", 0),
    #  (ge, "$g_presentation_marshall_selection_max_renown_2_troop", 0),
    #  (ge, "$g_presentation_marshall_selection_max_renown_3_troop", 0),
    #  (gt, ":num_men", 2), #at least 1 voter
    #  (assign, "$g_election_date", 0),
    #  (assign, "$g_presentation_marshall_selection_ended", 0),
    #  (try_begin),
    #    (neq, "$g_presentation_marshall_selection_max_renown_1_troop", "trp_player"),
    #    (neq, "$g_presentation_marshall_selection_max_renown_2_troop", "trp_player"),
    #    (start_presentation, "prsnt_marshall_selection"),
    #  (else_try),
    #    (jump_to_menu, "mnu_marshall_selection_candidate_ask"),
    #  (try_end),
      ]),
#

   (24,
    [
	##diplomacy start+ Add support for promoted kingdom ladies
	##OLD:
	#(try_for_range, ":kingdom_hero", active_npcs_begin, active_npcs_end),
	##NEW:
	(try_for_range, ":kingdom_hero", heroes_begin, heroes_end),
		(this_or_next|is_between, ":kingdom_hero", active_npcs_begin, active_npcs_end),
		(troop_slot_eq, ":kingdom_hero", slot_troop_occupation, slto_kingdom_hero),
	##diplomacy end+
		(troop_get_slot, ":impatience", ":kingdom_hero", slot_troop_intrigue_impatience),
		(val_sub, ":impatience", 5),
		(val_max, ":impatience", 0),
		(troop_set_slot, ":kingdom_hero", slot_troop_intrigue_impatience, ":impatience"),
	(try_end),

	(store_random_in_range, ":controversy_deduction", 1, 3),
	(val_min, ":controversy_deduction", 2),
#	(assign, ":controversy_deduction", 1),

	#This reduces controversy by one each round
	##diplomacy start+ Add support for promoted kingdom ladies
	##OLD:
	#(try_for_range, ":active_npc", active_npcs_begin, active_npcs_end),
	##NEW:
	(try_for_range, ":active_npc", heroes_begin, heroes_end),
		(this_or_next|is_between, ":active_npc", active_npcs_begin, active_npcs_end),
		(troop_slot_eq, ":active_npc", slot_troop_occupation, slto_kingdom_hero),
	##diplomacy end+
		(troop_get_slot, ":controversy", ":active_npc", slot_troop_controversy),
		(ge, ":controversy", 1),
		(val_sub, ":controversy", ":controversy_deduction"),
		(val_max, ":controversy", 0),
		(troop_set_slot, ":active_npc", slot_troop_controversy, ":controversy"),
	(try_end),

	(troop_get_slot, ":controversy", "trp_player", slot_troop_controversy),
	(val_sub, ":controversy", ":controversy_deduction"),
	(val_max, ":controversy", 0),
	(troop_set_slot, "trp_player", slot_troop_controversy, ":controversy"),

	]),
	
    #Individual lord political calculations
    #Check for lords without fiefs, auto-defections, etc
   (100,
    [
	##diplomacy start+
	#This is fairly complicated, and it was getting nearly unreadable so I reformatted it.
	#The old version is visible in version control.
	(assign, ":save_reg0", reg0),
	(val_add, "$g_lord_long_term_count", 1),
	(try_begin),
		(neg|is_between, "$g_lord_long_term_count", active_npcs_including_player_begin, active_npcs_end),
		(assign, "$g_lord_long_term_count", active_npcs_including_player_begin),
	(try_end),

	##Add political calculations for kingdom ladies.  Just extending the range would
	##slow down the political calculations cycle, which would have possibly-unforeseen results.
	##Instead, add a second iteration to deal with extensions.
	(try_for_range, ":iteration", 0, 2),
		(assign, ":troop_no", "$g_lord_long_term_count"),
		(try_begin),
			(eq, ":iteration", 1),
			(val_sub, ":troop_no", active_npcs_including_player_begin),
			(val_add, ":troop_no", active_npcs_end),
		(try_end),
		#Crude check to make sure that a careless modder (i.e. me) didn't decide it
		#would be a good idea to redefine active_npcs to include kingdom_ladies,
		#which would make the second iteration run off the end of the heroes list.
		(is_between, ":troop_no", active_npcs_including_player_begin, heroes_end),

		#Special handling for trp_player, and get the troop's faction
		(try_begin),
			(eq, ":troop_no", "trp_kingdom_heroes_including_player_begin"),
			(assign, ":troop_no", "trp_player"),
			(assign, ":faction", "$players_kingdom"),
		(else_try),
			(store_faction_of_troop, ":faction", ":troop_no"),
		(try_end),

		(try_begin),
			(eq, "$cheat_mode", 1),
			(str_store_troop_name, s9, ":troop_no"),
			(display_message, "@{!}DEBUG -- Doing political calculations for {s9}"),
		(try_end),

        #Tally the fiefs owned by the hero, and cache the value in slot.
		#If a lord owns no fiefs, his relations with his liege may deteriorate.
        (try_begin),
			(assign, reg0, 1),#Center points + 1
			(try_for_range, ":center", centers_begin, centers_end),
				(party_slot_eq, ":center", slot_town_lord, ":troop_no"),
				(try_begin),
					(is_between, ":center", towns_begin, towns_end),
					(val_add, reg0, 3),#3 points per town
				(else_try),
					(is_between, ":center", walled_centers_begin, walled_centers_end),
					(val_add, reg0, 2),#2 points per castle
				(else_try),
					(val_add, reg0, 1),#1 point per village
				(try_end),
			(try_end),
			#Update cached total
			(troop_set_slot, ":troop_no", dplmc_slot_troop_center_points_plus_one, reg0),
			#If a lord has no fiefs, relation loss potentially results.
			#Do not apply this to the player.
			(eq, reg0, 1),
			(troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
			(neq, ":troop_no", "trp_player"),

			#Don't apply this to the leader
			(faction_get_slot, ":faction_leader", ":faction", slot_faction_leader),
			(gt, ":faction_leader", -1),
			(neq, ":faction_leader", ":troop_no"),
			(neg|troop_slot_eq, ":faction_leader", slot_troop_spouse, ":troop_no"),
			(neg|troop_slot_eq, ":troop_no", slot_troop_spouse, ":faction_leader"),

			(troop_get_slot, ":troop_reputation", ":troop_no", slot_lord_reputation_type),
			(try_begin),
				(this_or_next|eq, ":troop_reputation", lrep_quarrelsome),
				(this_or_next|eq, ":troop_reputation", lrep_selfrighteous),
				(this_or_next|eq, ":troop_reputation", lrep_cunning),
				(eq, ":troop_reputation", lrep_debauched),
				(call_script, "script_troop_change_relation_with_troop", ":troop_no", ":faction_leader", -4),
				(val_add, "$total_no_fief_changes", -4),
			(else_try),
				(this_or_next|eq, ":troop_reputation", lrep_ambitious),#add support for lady personalities
				(eq, ":troop_reputation", lrep_martial),
				(call_script, "script_troop_change_relation_with_troop", ":troop_no", ":faction_leader", -2),
				(val_add, "$total_no_fief_changes", -2),
			(try_end),
        (try_end),

        #Auto-indictment or defection
        (try_begin),
			(this_or_next|troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
			(eq, ":troop_no", "trp_player"),

			#There must be a valid faction leader.  The faction leader won't defect from his own kingdom.
			#To avoid certain potential complications, also skip the defection/indictment check for the
			#spouse of the faction leader.  (Code to make that possible can be added elsewhere if
			#necessary.)
			(faction_get_slot, ":faction_leader", ":faction", slot_faction_leader),
			(gt, ":faction_leader", -1),
			(neq, ":troop_no", ":faction_leader"),
			(neg|troop_slot_eq, ":troop_no", slot_troop_spouse, ":faction_leader"),
			(neg|troop_slot_eq, ":faction_leader", slot_troop_spouse, ":troop_no"),

			#"I don't know why these are necessary, but they appear to be"
			#I am not about to put that to the test, even if I think it's silly.
			(neg|is_between, ":troop_no", "trp_kingdom_1_lord", "trp_knight_1_1"),
			(neg|is_between, ":troop_no", pretenders_begin, pretenders_end),

			#gekokujo 3.0 forgot to integrate start
			(assign, ":num_centers", 0),		  
			(try_for_range,":cur_center", walled_centers_begin, walled_centers_end),		    
			  (store_faction_of_party, ":faction_of_center", ":cur_center"),
			  (eq, ":faction_of_center", ":faction"),			
			  (val_add, ":num_centers", 1),
			(try_end),
			
			#we are counting num_centers to allow defection although there is high relation between faction leader and troop. 
			#but this rule should not applied for player's faction and player_supporters_faction so thats why here 1 is added to num_centers in that case.
		    (try_begin), 
		      (this_or_next|eq, ":faction", "$players_kingdom"),
			  (eq, ":faction", "fac_player_supporters_faction"),
			  (val_add, ":num_centers", 1),
		    (try_end),
			#gekokujo 3.0 forgot to integrate end

			(call_script, "script_troop_get_relation_with_troop", ":troop_no", ":faction_leader"),
			#gekokujo 3.0 forgot to integrate start
			#(le, reg0, -50), #was -75
			(this_or_next|le, reg0, -90), #was -75
			(eq, ":num_centers", 0), #if there is no walled centers that faction has defection happens 100%.
			#gekokujo 3.0 forgot to integrate end

			(call_script, "script_cf_troop_can_intrigue", ":troop_no", 0), #Should include battle, prisoner, in a castle with others

			#The more centralized the faction, the greater the chance the liege will indict
			#the lord before he defects.
			(faction_get_slot, reg0, ":faction", dplmc_slot_faction_centralization),
			(val_clamp, reg0, -3, 4),
			(val_add, reg0, 10),#7 minimum, 13 maximum
			(store_random_in_range, ":random", 0, reg0),
			#Random  < 5: The lord defects
			#Random >= 5: The liege indicts the lord for treason

			(try_begin),
				(lt, ":random", 1),
				(neq, ":troop_no", "trp_player"),
				#do a defection
				#gekokujo 3.0 forgot to integrate start
                #(assign, "$g_give_advantage_to_original_faction", ":troop_no"),#Note that I assign the troop number instead of 1 as is done in Native
				(try_begin),
				  (neq, ":num_centers", 0),
				  (assign, "$g_give_advantage_to_original_faction", ":troop_no"),
				(try_end),
				#gekokujo 3.0 forgot to integrate end
				(call_script, "script_lord_find_alternative_faction", ":troop_no"),
				(assign, ":new_faction", reg0),
				(assign, "$g_give_advantage_to_original_faction", 0),
				(neq, ":new_faction", ":faction"),
				(is_between, ":new_faction", kingdoms_begin, kingdoms_end),
				(str_store_troop_name_link, s1, ":troop_no"),
				(str_store_faction_name_link, s2, ":new_faction"),
				(str_store_faction_name_link, s3, ":faction"),
				(call_script, "script_change_troop_faction", ":troop_no", ":new_faction"),
				(try_begin),
					(ge, "$cheat_mode", 1),
					(str_store_troop_name, s4, ":troop_no"),
					(display_message, "@{!}DEBUG - {s4} faction changed in defection"),
				(try_end),
				(call_script, "script_dplmc_store_troop_is_female", ":troop_no"),
				(assign, reg4, reg0),
				(str_store_string, s4, "str_lord_defects_ordinary"),
				(display_log_message, "@{!}{s4}"),
				(try_begin),
					(eq, "$cheat_mode", 1),
					(this_or_next|eq, ":new_faction", "$players_kingdom"),
					(eq, ":faction", "$players_kingdom"),
					(call_script, "script_add_notification_menu", "mnu_notification_lord_defects", ":troop_no", ":faction"),
				(try_end),
			(else_try),
				(neq, ":faction_leader", "trp_player"),
                (call_script, "script_troop_get_relation_with_troop", ":troop_no", ":faction_leader"),
				#gekokujo 3.0 forgot to integrate
                #(le, reg0, -75),
				(le, reg0, -90), #was -75
				#gekokujo 3.0 forgot to integrate
				#do an indictment
				(call_script, "script_indict_lord_for_treason", ":troop_no", ":faction"),
			(try_end),

			#Update :faction if it has changed
			(try_begin),
				(eq, ":troop_no", "trp_player"),
				(assign, reg0, "$players_kingdom"),
			(else_try),
				(store_faction_of_troop, reg0, ":troop_no"),
			(try_end),
			(neq, reg0, ":faction"),#Fall through if indictment/defection didn't happen
			(assign, ":faction", reg0),
		(else_try),  #Take a stand on an issue
			(neq, ":troop_no", "trp_player"),
			(troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
			(faction_slot_ge, ":faction", slot_faction_political_issue, 1),
			#This bit of complication is needed for savegame compatibility -- if zero is in the slot, they'll choose anyway
			(neg|troop_slot_ge, ":troop_no", slot_troop_stance_on_faction_issue, 1),
			(this_or_next|troop_slot_eq, ":troop_no", slot_troop_stance_on_faction_issue, -1),
				(neq, "$players_kingdom", ":faction"),

			(call_script, "script_npc_decision_checklist_take_stand_on_issue", ":troop_no"),
			(troop_set_slot, ":troop_no", slot_troop_stance_on_faction_issue, reg0),
        (else_try),
			#OPTIONAL CHANGE (AI CHANGES HIGH):
			(ge, "$g_dplmc_ai_changes", DPLMC_AI_CHANGES_HIGH),
			#If an AI kingdom has fiefless lords and no free fiefs, the king
			#will consider giving up a village.  The king will not give up fiefs if
			#doing so would give him less territory than another lord of his faction.
			#(For simplicity, the AI will not do this while a marshall appointment
			#is pending.)
			(faction_slot_eq, ":faction", slot_faction_leader, ":troop_no"),
			(neq, ":troop_no", "trp_player"),
			#With fewer than 3 points we don't need to bother continuing, since 2 points means he only owns a single village.
         (troop_get_slot, ":local_temp", ":troop_no", dplmc_slot_troop_center_points_plus_one),
			(ge, ":local_temp", 3),
			#Don't do this while other business is pending
			(neg|faction_slot_ge, ":faction", slot_faction_political_issue, 1),
			#Find the fiefless lord of his faction that the king likes best.
			#Terminate the search early if he finds another lord whose fiefs
			#equal or exceed his own, or a lord whose fief point slot is not
			#initialized.
			(assign, ":end_cond", heroes_end),
			(assign, ":any_found", -200),
			(assign, ":best_active_npc", -1),
			(try_for_range, ":active_npc", heroes_begin, ":end_cond"),
				(neq, ":active_npc", ":troop_no"),
				(troop_slot_eq, ":active_npc", slot_troop_occupation, slto_kingdom_hero),
				(store_faction_of_troop, reg0, ":active_npc"),
				(eq, reg0, ":faction"),
				(troop_get_slot, reg0, ":active_npc", dplmc_slot_troop_center_points_plus_one),
				(try_begin),
					#Terminate.  The king cannot give up any points without being outfieffed (if he isn't already)
					(ge, reg0, ":local_temp"),
					(assign, ":end_cond", ":active_npc"),
				(else_try),
					#Terminate.  The first pass of political calculations aren't done, or things are in flux.
					(lt, reg0, 1),
					(assign, ":end_cond", ":active_npc"),
				(else_try),
					(eq, reg0, 1),
					(call_script, "script_troop_get_relation_with_troop", ":troop_no", ":active_npc"),
					(gt, reg0, ":any_found"),
					(assign, ":any_found", reg0),
					(assign, ":best_active_npc", ":active_npc"),
				(try_end),
			(try_end),
			(eq, ":end_cond", heroes_end),
			(is_between, ":best_active_npc", heroes_begin, heroes_end),
			(gt, ":any_found", -10),
			#Give up the least prosperous fief.
			(assign, ":local_temp", 101),
			(assign, ":any_found", -1),
			(try_for_range, ":center", villages_begin, villages_end),
				(party_slot_eq, ":center", slot_town_lord, ":troop_no"),
				(party_get_slot, reg0, ":center", slot_town_prosperity),
				(this_or_next|eq, ":any_found", -1),
				(lt, reg0, ":local_temp"),
				(assign, ":local_temp", reg0),
				(assign, ":any_found", ":center"),
			(try_end),
			#Clear village's lord
			(is_between, ":any_found", centers_begin, centers_end),
			(party_set_slot, ":any_found", slot_town_lord, -1),
			(troop_get_slot, reg0, ":troop_no", dplmc_slot_troop_center_points_plus_one),
			(val_sub, reg0, 1),
			(troop_set_slot, ":troop_no", dplmc_slot_troop_center_points_plus_one, reg0),
			(str_store_party_name_link, s4, ":any_found"),
			(str_store_troop_name_link, s5, ":troop_no"),
			(str_store_faction_name_link, s7, ":faction"),
			(display_log_message, "@{s5} has decided to grant {s4} to another lord of the {s7}."),
			#Reset faction issue
			(try_for_range, ":active_npc", heroes_begin, heroes_end),
				(store_faction_of_troop, reg0, ":active_npc"),
				(eq, reg0, ":faction"),
				(troop_set_slot, ":troop_no", slot_troop_stance_on_faction_issue, -1),
			(try_end),
			(store_current_hours, reg0),
			(faction_set_slot, ":faction", slot_faction_political_issue_time, reg0),
			(faction_set_slot, ":faction", slot_faction_political_issue, ":any_found"),
			#Set the liege's position on the issue, since he gave up the village with
			#something specific in mind.
			(troop_set_slot, ":troop_no", slot_troop_stance_on_faction_issue, ":best_active_npc"),
		(try_end),

		#Reduce grudges over time
		(try_begin),
			#Skip this for the dead
			(neg|troop_slot_eq, ":troop_no", slot_troop_occupation, dplmc_slto_dead),
			#Do not perform this for kingdom ladies, since it will potentially mess up courtship.
			(neg|troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_lady),

			(try_for_range, ":active_npc", heroes_begin, heroes_end),
				(neq, ":active_npc", ":troop_no"),
				(neg|troop_slot_eq, ":active_npc", slot_troop_occupation, slto_kingdom_lady),#Don't do for ladies
				(neg|troop_slot_eq, ":active_npc", slot_troop_occupation, dplmc_slto_dead),#Don't do for the dead

				#Fix: there are some NPCs that have "initial" relations with the player set,
				#but they can decay before ever meeting him, so keep them until the first meeting.
				(this_or_next|neq, ":troop_no", "trp_player"),
				(troop_slot_ge, ":troop_no", slot_troop_met, 1),

				(call_script, "script_troop_get_relation_with_troop", ":troop_no", ":active_npc"),
				(lt, reg0, 0),
				(store_sub, ":chance_of_convergence", 0, reg0),
				(store_random_in_range, ":random", 0, 300),
				(lt, ":random", ":chance_of_convergence"),
				(call_script, "script_troop_change_relation_with_troop", ":troop_no", ":active_npc", 1),
				(val_add, "$total_relation_changes_through_convergence", 1),
			(try_end),

			#Accelerate forgiveness for lords in exile (with their original faction only)
			(neq, ":troop_no", "trp_player"),
			(troop_slot_eq, ":troop_no", slot_troop_occupation, dplmc_slto_exile),
			(troop_get_slot, ":original_faction", ":troop_no", slot_troop_original_faction),
			(gt, ":original_faction", 0),

			(try_for_range, ":active_npc", heroes_begin, heroes_end),
				(neq, ":active_npc", ":troop_no"),
				(neg|troop_slot_eq, ":active_npc", slot_troop_occupation, slto_kingdom_lady),#Don't do for ladies
				(neg|troop_slot_eq, ":active_npc", slot_troop_occupation, dplmc_slto_dead),#Don't do for the dead
				#Only apply to heroes with the same original faction
				(troop_slot_eq, ":active_npc", slot_troop_original_faction, ":original_faction"),
				(call_script, "script_troop_get_relation_with_troop", ":troop_no", ":active_npc"),
				(lt, reg0, 0),
				(store_sub, ":chance_of_convergence", 0, reg0),
				(store_random_in_range, ":random", 0, 300),
				(lt, ":random", ":chance_of_convergence"),
				(call_script, "script_troop_change_relation_with_troop", ":troop_no", ":active_npc", 1),
				(val_add, "$total_relation_changes_through_convergence", 1),
			(try_end),
		(try_end),
	#Finish loop over the ":iteration" variable.
	(try_end),
	(assign, reg0, ":save_reg0"),
	##diplomacy end+
   ]),
	
#TEMPORARILY DISABLED, AS READINESS IS NOW A PRODUCT OF NPC_DECISION_CHECKLIST	
  # Changing readiness to join army
#   (10,
 #   [
 #     (try_for_range, ":troop_no", active_npcs_begin, active_npcs_end),
#		(eq, 1, 0),
#	    (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
#        (assign, ":modifier", 1),
#        (troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
#        (try_begin),
#          (gt, ":party_no", 0),
#          (party_get_slot, ":commander_party", ":party_no", slot_party_commander_party),
#          (ge, ":commander_party", 0),
#          (store_faction_of_party, ":faction_no", ":party_no"),
#          (faction_get_slot, ":faction_marshall", ":faction_no", slot_faction_marshall),
#          (ge, ":faction_marshall", 0),
#          (troop_get_slot, ":marshall_party", ":faction_marshall", slot_troop_leaded_party),
#          (eq, ":commander_party", ":marshall_party"),
#          (assign, ":modifier", -1),
#        (try_end),
#        (troop_get_slot, ":readiness", ":troop_no", slot_troop_readiness_to_join_army),
#        (val_add, ":readiness", ":modifier"),
#        (val_clamp, ":readiness", 0, 100),
#        (troop_set_slot, ":troop_no", slot_troop_readiness_to_join_army, ":readiness"),
#        (assign, ":modifier", 1),
#        (try_begin),
#          (gt, ":party_no", 0),
#          (store_troop_faction, ":troop_faction", ":troop_no"),
#          (eq, ":troop_faction", "fac_player_supporters_faction"),
#          (neg|troop_slot_eq, ":troop_no", slot_troop_player_order_state, spai_undefined),
#          (party_get_slot, ":party_ai_state", ":party_no", slot_party_ai_state),
#          (party_get_slot, ":party_ai_object", ":party_no", slot_party_ai_object),
#          #Check if party is following player orders
#          (try_begin),
#            (troop_slot_eq, ":troop_no", slot_troop_player_order_state, ":party_ai_state"),
#            (troop_slot_eq, ":troop_no", slot_troop_player_order_object, ":party_ai_object"),
#            (assign, ":modifier", -1),
#          (else_try),
#            #Leaving following player orders if the current party order is not the same.
#            (troop_set_slot, ":troop_no", slot_troop_player_order_state, spai_undefined),
#            (troop_set_slot, ":troop_no", slot_troop_player_order_object, -1),
#          (try_end),
#        (try_end),
#        (troop_get_slot, ":readiness", ":troop_no", slot_troop_readiness_to_follow_orders),
#        (val_add, ":readiness", ":modifier"),
#        (val_clamp, ":readiness", 0, 100),
#        (troop_set_slot, ":troop_no", slot_troop_readiness_to_follow_orders, ":readiness"),
#        (try_begin),
#          (lt, ":readiness", 10),
#          (troop_set_slot, ":troop_no", slot_troop_player_order_state, spai_undefined),
#          (troop_set_slot, ":troop_no", slot_troop_player_order_object, -1),
#        (try_end),
#      (try_end),
 #     ]),
  
    #gekokujo 3.1 rebellions start
    #first we hijack this empty trigger
#  # Process vassal ai
#   (2,
#   [
#     #(call_script, "script_process_kingdom_parties_ai"), #moved to below trigger (per 1 hour) in order to allow it processed more frequent.
#   ]),
  (24*7,
  [
    #first count how many active factions there are
    (assign, ":num_active_factions", 0),
    (try_for_range, ":cur_kingdom", kingdoms_begin, kingdoms_end),
      (faction_slot_eq, ":cur_kingdom", slot_faction_state, sfs_active),
      (val_add, ":num_active_factions", 1),
    (try_end),
    
    #rebellions only happen if there are 10 factions or less
    (le, ":num_active_factions", 10),
    
    #don't keep piling on rebellion after rebellion -- factions + 10 ensures there should be 3 at most
    (store_num_parties_of_template, ":num_deserters", "pt_deserters"),
    (store_add, ":max_deserters", ":num_active_factions", 10),
    (lt,":num_deserters", ":max_deserters"),
    
    #given the above conditions, determine if a rebellion triggers
    #it should be 50% chance with 1 active faction, 5% with 10
    (store_mul, ":chance", ":num_active_factions", -5),
    (val_add, ":chance", 55),
    (store_random_in_range, ":seed", 0, 100),
    (le, ":seed", ":chance"),
    
    #pick a random defeated faction
    #note that the ikko don't get picked if the player faction is active -- this is on purpose
    (store_sub, ":num_defeated_factions", 20, ":num_active_factions"),
    (store_random_in_range, ":seed", 0, ":num_defeated_factions"),
    (assign, ":break", 0),
    (try_for_range, ":cur_kingdom", kingdoms_begin, kingdoms_end),
      (eq, ":break", 0),
      (faction_slot_eq, ":cur_kingdom", slot_faction_state, sfs_defeated),
      (try_begin),
        (gt, ":seed", 0),
        (val_sub, ":seed", 1),
      (else_try),
        (assign, ":faction", ":cur_kingdom"),
        (assign, ":break", 1),
      (try_end),
    (try_end),
    
    #pick a town that was originally of the defeated faction
    #this will always pick the last town in order -- oh well
    (try_for_range, ":spawn_point", towns_begin, towns_end),
      (party_get_slot, ":spawn_point_faction", ":spawn_point", slot_center_original_faction),
      (eq, ":spawn_point_faction", ":faction"),
      (party_get_slot, ":culture", ":spawn_point", slot_center_culture),
    (try_end),
    
    #find the troop types
    (faction_get_slot, ":ashigaru", ":culture", slot_faction_tier_0_troop),
    (faction_get_slot, ":samurai", ":culture", slot_faction_tier_1_troop),
    
    #determine how many parties spawn
    (store_div, ":chance", ":num_defeated_factions", 4),
    (store_random_in_range, ":parties", 1, ":chance"),
    
    #spawn the parties
    (set_spawn_radius, 15),
    (try_for_range, ":i", 0, ":parties"),
      (spawn_around_party, ":spawn_point", "pt_deserters"),
      (assign, ":new_party", reg0),
      
      (try_begin),
        (eq, ":i", 0), #the first party is huge -- 160 to 298
        (store_random_in_range, ":ashigaru_count", 120, 225),
        (store_random_in_range, ":samurai_count", 40, 75),
      (else_try),
        #the subsequent parties are smaller -- 80 to 138
        (store_random_in_range, ":ashigaru_count", 60, 105),
        (store_random_in_range, ":samurai_count", 20, 35),
      (try_end),
      
      (party_add_members, ":new_party", ":ashigaru", ":ashigaru_count"),
      (party_add_members, ":new_party", ":samurai", ":samurai_count"),
      
      (store_random_in_range, ":seed", 1, 15),
      (try_for_range, ":unused", 0, ":seed"),
        (party_upgrade_with_xp, ":new_party", 200000, 0),
      (try_end),
    (try_end),
    
    (assign, "$gekokujo_rebel_faction", ":faction"),
    (assign, "$gekokujo_rebel_stronghold", ":spawn_point"),
    
    (jump_to_menu, "mnu_rebellion"),
  ]),
  # Process siege ai
   (3,
   [
      ##diplomacy start+
	  (assign, ":save_reg0", reg0),#Save registers
	  (assign, ":save_reg1", reg1),
	  ##diplomacy end+
      (store_current_hours, ":cur_hours"),
      (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
        (party_get_slot, ":besieger_party", ":center_no", slot_center_is_besieged_by),
        (gt, ":besieger_party", 0),
        (party_is_active, ":besieger_party"),
        (store_faction_of_party, ":besieger_faction", ":besieger_party"),
        (party_slot_ge, ":center_no", slot_center_is_besieged_by, 1),
        (party_get_slot, ":siege_begin_hours", ":center_no", slot_center_siege_begin_hours),
        (store_sub, ":siege_begin_hours", ":cur_hours", ":siege_begin_hours"),
        (assign, ":launch_attack", 0),
        (assign, ":call_attack_back", 0),
        (assign, ":attacker_strength", 0),
        (assign, ":marshall_attacking", 0),
        (try_for_range, ":troop_no", active_npcs_begin, active_npcs_end),
          (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
          (neg|troop_slot_ge, ":troop_no", slot_troop_prisoner_of_party, 0),
          (troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
          (gt, ":party_no", 0),
          (party_is_active, ":party_no"),
		  
          (store_troop_faction, ":troop_faction_no", ":troop_no"),
          (eq, ":troop_faction_no", ":besieger_faction"),
          (assign, ":continue", 0),
          (try_begin),
            (party_slot_eq, ":party_no", slot_party_ai_state, spai_besieging_center),
            (party_slot_eq, ":party_no", slot_party_ai_object, ":center_no"),
            (assign, ":continue", 1),
          (else_try),
            (party_slot_eq, ":party_no", slot_party_ai_state, spai_accompanying_army),
            (party_get_slot, ":commander_party", ":party_no", slot_party_ai_object),
            (gt, ":commander_party", 0),
            (party_is_active, ":commander_party"),
            (party_slot_eq, ":commander_party", slot_party_ai_state, spai_besieging_center),
            (party_slot_eq, ":commander_party", slot_party_ai_object, ":center_no"),
            (assign, ":continue", 1),
          (try_end),
          (eq, ":continue", 1),
          (party_get_battle_opponent, ":opponent", ":party_no"),
          (this_or_next|lt, ":opponent", 0),
          (eq, ":opponent", ":center_no"),
          (try_begin),
            (faction_slot_eq, ":besieger_faction", slot_faction_marshall, ":troop_no"),
            (assign, ":marshall_attacking", 1),
          (try_end),
          (call_script, "script_party_calculate_regular_strength", ":party_no"),
		  ##diplomacy start+ terrain advantage
		  (try_begin),
			(ge, "$g_dplmc_terrain_advantage", DPLMC_TERRAIN_ADVANTAGE_ENABLE),
			(call_script, "script_dplmc_party_calculate_strength_in_terrain", ":party_no", dplmc_terrain_code_siege, 0, 0),
          (try_end),
		  ##diplomacy end+
          (val_add, ":attacker_strength", reg0),
        (try_end),
        (try_begin),
          (gt, ":attacker_strength", 0),
          (party_collect_attachments_to_party, ":center_no", "p_collective_enemy"),
          (call_script, "script_party_calculate_regular_strength", "p_collective_enemy"),
		  ##diplomacy start+ terrain advantage
		  (try_begin),
			(ge, "$g_dplmc_terrain_advantage", DPLMC_TERRAIN_ADVANTAGE_ENABLE),
			(call_script, "script_dplmc_party_calculate_strength_in_terrain", "p_collective_enemy", dplmc_terrain_code_siege, 0, 0),
          (try_end),
		  ##diplomacy end+
          (assign, ":defender_strength", reg0),
          (try_begin),
            (eq, "$auto_enter_town", ":center_no"),
            (eq, "$g_player_is_captive", 0),
            (call_script, "script_party_calculate_regular_strength", "p_main_party"),
			##diplomacy start+ terrain advantage
			(try_begin),
				(ge, "$g_dplmc_terrain_advantage", DPLMC_TERRAIN_ADVANTAGE_ENABLE),
				(call_script, "script_dplmc_party_calculate_strength_in_terrain", "p_collective_enemy", dplmc_terrain_code_siege, 0, 0),
			(try_end),
			##diplomacy end+
            (val_add, ":defender_strength", reg0),
            (val_mul, ":attacker_strength", 2), #double the power of attackers if the player is in the campaign
          (try_end),
          (party_get_slot, ":siege_hardness", ":center_no", slot_center_siege_hardness),
          (val_add, ":siege_hardness", 100),
          (val_mul, ":defender_strength", ":siege_hardness"),
          (val_div, ":defender_strength", 100),
          (val_max, ":defender_strength", 1),
          (try_begin),
            (eq, ":marshall_attacking", 1),
            (eq, ":besieger_faction", "$players_kingdom"),
            (check_quest_active, "qst_follow_army"),
            (val_mul, ":attacker_strength", 2), #double the power of attackers if the player is in the campaign
          (try_end),
          (store_mul, ":strength_ratio", ":attacker_strength", 100),
          (val_div, ":strength_ratio", ":defender_strength"),
          (store_sub, ":random_up_limit", ":strength_ratio", 250), #was 300 (1.126)
                    
          (try_begin),
            (gt, ":random_up_limit", -100), #never attack if the strength ratio is less than 150%
            (store_div, ":siege_begin_hours_effect", ":siege_begin_hours", 2), #was 3 (1.126)
            (val_add, ":random_up_limit", ":siege_begin_hours_effect"),
          (try_end),

          (val_div, ":random_up_limit", 5),
          (val_max, ":random_up_limit", 0),
          (store_sub, ":random_down_limit", 175, ":strength_ratio"), #was 200 (1.126)
          (val_max, ":random_down_limit", 0),
          (try_begin),
            (store_random_in_range, ":rand", 0, 100),
            (lt, ":rand", ":random_up_limit"),
            (gt, ":siege_begin_hours", 24),#initial preparation
            (assign, ":launch_attack", 1),
          (else_try),
            (store_random_in_range, ":rand", 0, 100),
            (lt, ":rand", ":random_down_limit"),            
            (assign, ":call_attack_back", 1),
          (try_end),
        (else_try),
          (assign, ":call_attack_back", 1),
        (try_end),

        #Assault the fortress
        (try_begin),
          (eq, ":launch_attack", 1),
          (call_script, "script_begin_assault_on_center", ":center_no"),
        (else_try),
          (eq, ":call_attack_back", 1),
          (try_for_range, ":troop_no", active_npcs_begin, active_npcs_end),
            (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
            (neg|troop_slot_ge, ":troop_no", slot_troop_prisoner_of_party, 0),
            (troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
            (gt, ":party_no", 0),
            (party_is_active, ":party_no"),
			
            (party_slot_eq, ":party_no", slot_party_ai_state, spai_besieging_center),
            (party_slot_eq, ":party_no", slot_party_ai_object, ":center_no"),
            (party_slot_eq, ":party_no", slot_party_ai_substate, 1),
            (call_script, "script_party_set_ai_state", ":party_no", spai_undefined, -1),
            (call_script, "script_party_set_ai_state", ":party_no", spai_besieging_center, ":center_no"),
            #resetting siege begin time if at least 1 party retreats
            (party_set_slot, ":center_no", slot_center_siege_begin_hours, ":cur_hours"),
          (try_end),
        (try_end),
      (try_end),
	  ##diplomacy start+
	  #Revert registers
	  (assign, reg0, ":save_reg0"),
	  (assign, reg1, ":save_reg1"),
	  ##diplomacy end+
    ]),
    # Decide faction ais
    (6, #it was 23
    [
      (assign, "$g_recalculate_ais", 1),
    ]),
	
    
  # Decide faction ai flag check
   (0,
   [
   

    (try_begin),
		(ge, "$cheat_mode", 1),
	
		(try_for_range, ":king", "trp_kingdom_1_lord", "trp_knight_1_1"),		
			(store_add, ":proper_faction", ":king", "fac_kingdom_1"),
			(val_sub, ":proper_faction", "trp_kingdom_1_lord"),
			(store_faction_of_troop, ":actual_faction", ":king"),
			
			(neq, ":proper_faction", ":actual_faction"),
			(neq, ":actual_faction", "fac_commoners"),
			(ge, "$cheat_mode", 2),
			(neq, ":king", "trp_kingdom_2_lord"),
			
			(str_store_troop_name, s4, ":king"),
			(str_store_faction_name, s5, ":actual_faction"),
			(str_store_faction_name, s6, ":proper_faction"),
			(str_store_string, s65, "@{!}DEBUG - {s4} is in {s5}, should be in {s6}, disabling political cheat mode"),
#			(display_message, "@{s65}"),
			(rest_for_hours, 0, 0, 0),
			
			#(assign, "$cheat_mode", 1),
			(jump_to_menu, "mnu_debug_alert_from_s65"),
		(try_end),
	
	
	(try_end),
   
     (eq, "$g_recalculate_ais", 1),
     (assign, "$g_recalculate_ais", 0),
     (call_script, "script_recalculate_ais"),
   ]),
	
    # Count faction armies
    (24,
    [
       (try_for_range, ":faction_no", kingdoms_begin, kingdoms_end),
         (call_script, "script_faction_recalculate_strength", ":faction_no"),
       (try_end),
	   ##diplomacy start+ Add support for promoted kingdom ladies
	   ##OLD:
	   #(try_for_range, ":active_npc", active_npcs_begin, active_npcs_end),
	   ##NEW:
	   (try_for_range, ":active_npc", heroes_begin, heroes_end),
	    (this_or_next|is_between, ":active_npc", active_npcs_begin, active_npcs_end),
	    (troop_slot_eq, ":active_npc", slot_troop_occupation, slto_kingdom_hero),
	   ##diplomacy end+
		(store_faction_of_troop, ":active_npc_faction", ":active_npc"),
		(neg|faction_slot_eq, ":active_npc_faction", slot_faction_ai_state, sfai_default),
		(neg|faction_slot_eq, ":active_npc_faction", slot_faction_ai_state, sfai_feast),
		(neg|faction_slot_eq, ":active_npc_faction", slot_faction_ai_state, sfai_gathering_army),
		
		(troop_get_slot, ":active_npc_party", ":active_npc", slot_troop_leaded_party),
		(party_is_active, ":active_npc_party"),
		
		(val_add, "$total_vassal_days_on_campaign", 1),
		
	    (party_slot_eq, ":active_npc_party", slot_party_ai_state, spai_accompanying_army),
		(val_add, "$total_vassal_days_responding_to_campaign", 1),
		
	   
	   (try_end),
	   
    ]),
#   (7 * 24,
#   [
##       (call_script, "script_get_number_of_unclaimed_centers_by_player"),
##       (assign, ":unclaimed_centers", reg0),
##       (gt, ":unclaimed_centers", 0),
# You are holding an estate without a lord.        
#       (try_for_range, ":troop_no", heroes_begin, heroes_end),
#         (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
#         (troop_get_slot, ":relation", ":troop_no", slot_troop_player_relation),
#         (val_sub, ":relation", 1),
#         (val_max, ":relation", -100),
#         (troop_set_slot, ":troop_no", slot_troop_player_relation, ":relation"),
#       (try_end),
# You relation with all kingdoms other than your own has decreased by 1.     
#       (try_for_range, ":faction_no", kingdoms_begin, kingdoms_end),
#         (neq, ":faction_no", "$players_kingdom"),
#         (store_relation,":faction_relation",":faction_no","fac_player_supporters_faction"),
#         (val_sub, ":faction_relation", 1),
#         (val_max, ":faction_relation", -100),
#		  WARNING: Never use set_relation!
#         (set_relation, ":faction_no", "fac_player_supporters_faction", ":faction_relation"),
#       (try_end),
#    ]),

  
  # Offer player to join faction
  # Only if the player is male -- female characters will be told that they should seek out a faction through NPCs, possibly
   (32,
   [
     (eq, "$players_kingdom", 0),
     (le, "$g_invite_faction", 0),
     (eq, "$g_player_is_captive", 0),
	 ##diplomacy start+ Use script for gender
	 #(troop_get_type, ":type", "trp_player"),
	 (assign, ":type", "$character_gender"),#<-- this should have been set correctly during character creation
	 ##diplomacy end+
	 (try_begin),
	    ##diplomacy start+ In reduced prejudice mode, female players get the same offers.
		(lt, "$g_disable_condescending_comments", 2),
		##diplomacy end+
		(eq, ":type", 1),
		(eq, "$npc_with_sisterly_advice", 0),
		##diplomacy start+  Make the order less predictable (used below)
		(store_random_in_range, ":random", companions_begin, companions_end),
		##diplomacy end+
		(try_for_range, ":npc", companions_begin, companions_end),
			##diplomacy start+ Make the order less predictable
			(val_add, ":npc", ":random"),
			(try_begin),
				(ge, ":npc", companions_end),
				(val_sub, ":npc", companions_end),
				(val_add, ":npc", companions_begin),
			(try_end),
			##diplomacy end+
			(main_party_has_troop, ":npc"),
			##diplmacy start+ Use a script for gender
			##OLD:
			#(troop_get_type, ":npc_type", ":npc"),
			#(eq, ":npc_type", 1),
			##NEW:
			(assign, ":npc_type", 0),
			(try_begin),
				(call_script, "script_cf_dplmc_troop_is_female", ":npc"),
				(assign, ":npc_type", 1),
			(try_end),
			(eq, ":npc_type", ":type"),
			##diplomacy end+
			(troop_slot_ge, "trp_player", slot_troop_renown, 150),
			(troop_slot_ge, ":npc", slot_troop_woman_to_woman_string, 1),
			(assign, "$npc_with_sisterly_advice", ":npc"),
		(try_end),
	 (else_try),
	     (store_random_in_range, ":kingdom_no", npc_kingdoms_begin, npc_kingdoms_end),
	     (assign, ":min_distance", 999999),
	     (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
	       (store_faction_of_party, ":center_faction", ":center_no"),
	       (eq, ":center_faction", ":kingdom_no"),
	       (store_distance_to_party_from_party, ":cur_distance", "p_main_party", ":center_no"),
	       (val_min, ":min_distance", ":cur_distance"),
	     (try_end),
	     (lt, ":min_distance", 30),
	     (store_relation, ":kingdom_relation", ":kingdom_no", "fac_player_supporters_faction"),
	     (faction_get_slot, ":kingdom_lord", ":kingdom_no", slot_faction_leader),
	     (call_script, "script_troop_get_player_relation", ":kingdom_lord"),
	     (assign, ":lord_relation", reg0),
	     #(troop_get_slot, ":lord_relation", ":kingdom_lord", slot_troop_player_relation),
	     (call_script, "script_get_number_of_hero_centers", "trp_player"),
	     (assign, ":num_centers_owned", reg0),
	     (eq, "$g_infinite_camping", 0),
	     	     
	     (assign, ":player_party_size", 0),	     
	     (try_begin),
	       (ge, "p_main_party", 0),
	       (store_party_size_wo_prisoners, ":player_party_size", "p_main_party"),	     
	     (try_end),  
	     
	     (try_begin),	       
	       (eq, ":num_centers_owned", 0),
	       (troop_get_slot, ":player_renown", "trp_player", slot_troop_renown),
	       (ge, ":player_renown", 160),
	       (ge, ":kingdom_relation", 0),
	       (ge, ":lord_relation", 0),
	       (ge, ":player_party_size", 45),
	       (store_random_in_range, ":rand", 0, 100),
	       (lt, ":rand", 50),
	       (call_script, "script_get_poorest_village_of_faction", ":kingdom_no"),
	       (assign, "$g_invite_offered_center", reg0),
	       (ge, "$g_invite_offered_center", 0),
	       (assign, "$g_invite_faction", ":kingdom_no"),
	       (jump_to_menu, "mnu_invite_player_to_faction"),
	     (else_try),
	       (gt, ":num_centers_owned", 0),
	       (neq, "$players_oath_renounced_against_kingdom", ":kingdom_no"),
	       (ge, ":kingdom_relation", -40),
	       (ge, ":lord_relation", -20),
	       (ge, ":player_party_size", 30),
	       (store_random_in_range, ":rand", 0, 100),
	       (lt, ":rand", 20),
	       (assign, "$g_invite_faction", ":kingdom_no"),
	       (assign, "$g_invite_offered_center", -1),
	       (jump_to_menu, "mnu_invite_player_to_faction_without_center"),
	     (try_end),
	 (try_end), 
    ]),
    #recalculate lord random decision seeds once in every week
	(24 * 7, 
	[
	  ##diplomacy start+ Kingdom ladies should also have their decision seeds updated.
	  ##                 Also, use 10000 instead of 9999, since the upper bound for store_random_in_range is exclusive.
	  ##OLD:
      #(try_for_range, ":troop_no", active_npcs_begin, active_npcs_end),
      #  (store_random_in_range, ":random", 0, 9999),
	  ##NEW:
	  (try_for_range, ":troop_no", heroes_begin, heroes_end),
	     (store_random_in_range, ":random", 0, 10000),
	  ##diplomacy end+
        (troop_set_slot, ":troop_no", slot_troop_temp_decision_seed, ":random"),
      (try_end),

	  ##diplomacy start+ Also update the temporary seed for the player
	  (store_random_in_range, ":random", 0, 10000),
	  (troop_set_slot, "trp_player", slot_troop_temp_decision_seed, ":random"),
	  ##diplomacy end+		
	
	#npcs will only change their minds on issues at least 24 hours after speaking to the player
    #(store_current_hours, ":hours"),
    #(try_begin),
    #  (eq, 1, 0), #disabled
    #  (try_for_range, ":npc", active_npcs_begin, active_npcs_end),
    #    (troop_get_slot, ":last_talk", ":npc", slot_troop_last_talk_time),
    #    (val_sub, ":hours", ":last_talk"),
    #    (ge, ":hours", 24),
    #    (store_random_in_range, ":random", 0, 9999),
    #    (troop_set_slot, ":npc", slot_troop_temp_decision_seed, ":random"),
    #  (try_end),
    #(try_end),
	]),
  # Check escape chances of hero prisoners.
  (48,
   [
       (call_script, "script_randomly_make_prisoner_heroes_escape_from_party", "p_main_party", 50),
       (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
##         (party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
         (assign, ":chance", 30),
         (try_begin),
           (party_slot_eq, ":center_no", slot_center_has_prisoner_tower, 1),
           (assign, ":chance", 5),
         (try_end),
         (call_script, "script_randomly_make_prisoner_heroes_escape_from_party", ":center_no", ":chance"),
       (try_end),
	   #gekokujo 3.1 fort prison fix start
	   #smaller escape chance than player, greater than towns/castles
       (try_for_range, ":center_no", forts_begin, forts_end),
	     (call_script, "script_randomly_make_prisoner_heroes_escape_from_party", ":center_no", 40),
       (try_end),
	   #gekokujo 3.1 fort prison fix end
    ]),
  # Asking the ownership of captured centers to the player
#  (3,
#   [
#    (assign, "$g_center_taken_by_player_faction", -1),
#    (try_for_range, ":center_no", centers_begin, centers_end),
#      (eq, "$g_center_taken_by_player_faction", -1),
#      (store_faction_of_party, ":center_faction", ":center_no"),
#      (eq, ":center_faction", "fac_player_supporters_faction"),
#      (this_or_next|party_slot_eq, ":center_no", slot_town_lord, stl_reserved_for_player),
#      (this_or_next|party_slot_eq, ":center_no", slot_town_lord, stl_unassigned),
#      (party_slot_eq, ":center_no", slot_town_lord, stl_rejected_by_player),
#      (assign, "$g_center_taken_by_player_faction", ":center_no"),
#    (try_end),
#    (faction_get_slot, ":leader", "fac_player_supporters_faction", slot_faction_leader),

#	(try_begin),
#		(ge, "$g_center_taken_by_player_faction", 0),
		
#		(eq, "$cheat_mode", 1),
#		(str_store_party_name, s14, "$g_center_taken_by_player_faction"),
#		(display_message, "@{!}{s14} should be assigned to lord"),
#	(try_end),
	
#    ]),


  # Respawn hero party after kingdom hero is released from captivity.
  (48,
   [
	   ##diplomacy start+ Support promoted kingdom ladies
	   ##OLD:
       #(try_for_range, ":troop_no", active_npcs_begin, active_npcs_end),
	   ##NEW:
	    (try_for_range, ":troop_no", heroes_begin, heroes_end),
	   ##diplomacy end+
         (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),

         (str_store_troop_name, s1, ":troop_no"),
       
         (neg|troop_slot_ge, ":troop_no", slot_troop_prisoner_of_party, 0),
         (neg|troop_slot_ge, ":troop_no", slot_troop_leaded_party, 1),

         (store_troop_faction, ":cur_faction", ":troop_no"),
         (try_begin),
           (eq, ":cur_faction", "fac_outlaws"), #Do nothing
         (else_try),         
           (try_begin),
             (eq, "$cheat_mode", 2),
             (str_store_troop_name, s4, ":troop_no"),
             (display_message, "str_debug__attempting_to_spawn_s4"),
           (try_end),
           
           (call_script, "script_cf_select_random_walled_center_with_faction_and_owner_priority_no_siege", ":cur_faction", ":troop_no"),#Can fail
           (assign, ":center_no", reg0),

           (try_begin),
             (eq, "$cheat_mode", 2),             
             (str_store_party_name, s7, ":center_no"),
			 (str_store_troop_name, s0, ":troop_no"),
             (display_message, "str_debug__s0_is_spawning_around_party__s7"),
           (try_end),
       
           (call_script, "script_create_kingdom_hero_party", ":troop_no", ":center_no"),

		   (try_begin),
		     (eq, "$g_there_is_no_avaliable_centers", 0),
             (party_attach_to_party, "$pout_party", ":center_no"),
           (try_end),
           
           #new
           #(troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
		   #(call_script, "script_npc_decision_checklist_party_ai", ":troop_no"), #This handles AI for both marshal and other parties		
		   #(call_script, "script_party_set_ai_state", ":party_no", reg0, reg1),
		   #new end

           (troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
           (call_script, "script_party_set_ai_state", ":party_no", spai_holding_center, ":center_no"),           
           
         (else_try),
           (neg|faction_slot_eq, ":cur_faction", slot_faction_state, sfs_active),
           (try_begin),
             (is_between, ":troop_no", kings_begin, kings_end),
			 # NE dk
			 (eq, ":cur_faction", "fac_dark_knights"), ##Invasion
			 # NE end dk
             (troop_set_slot, ":troop_no", slot_troop_change_to_faction, "fac_commoners"),
           (else_try),
             (store_random_in_range, ":random_no", 0, 100),
             (lt, ":random_no", 10),
             (call_script, "script_cf_get_random_active_faction_except_player_faction_and_faction", ":cur_faction"),
             (troop_set_slot, ":troop_no", slot_troop_change_to_faction, reg0),
           (try_end),
         (try_end),
       (try_end),
    ]),
  #Troop AI: Village farmers thinking
  (8,
   [
       (try_for_parties, ":party_no"),
         (party_slot_eq, ":party_no", slot_party_type, spt_village_farmer),
         (party_is_in_any_town, ":party_no"),
         (party_get_slot, ":home_center", ":party_no", slot_party_home_center),
         (party_get_cur_town, ":cur_center", ":party_no"),

         (assign, ":can_leave", 1),
         (try_begin),
           (is_between, ":cur_center", walled_centers_begin, walled_centers_end),
           (neg|party_slot_eq, ":cur_center", slot_center_is_besieged_by, -1),
           (assign, ":can_leave", 0),
         (try_end),
         (eq, ":can_leave", 1),

         (try_begin),
           (eq, ":cur_center", ":home_center"),
		   
		   #Peasants trade in their home center
		   (call_script, "script_do_party_center_trade", ":party_no", ":home_center", 3), #this needs to be the same as the center		   
		   (store_faction_of_party, ":center_faction", ":cur_center"),
           (party_set_faction, ":party_no", ":center_faction"),           		   
           (party_get_slot, ":market_town", ":home_center", slot_village_market_town),
           (party_set_slot, ":party_no", slot_party_ai_object, ":market_town"),
           (party_set_slot, ":party_no", slot_party_ai_state, spai_trading_with_town),
           (party_set_ai_behavior, ":party_no", ai_bhvr_travel_to_party),
           (party_set_ai_object, ":party_no", ":market_town"),
         (else_try),
           (try_begin),
             (party_get_slot, ":cur_ai_object", ":party_no", slot_party_ai_object),
             (eq, ":cur_center", ":cur_ai_object"),

             (call_script, "script_do_party_center_trade", ":party_no", ":cur_ai_object", 3), #raised from 10
             (assign, ":total_change", reg0),
		     #This is roughly 50% of what a caravan would pay
			 
             #Adding tariffs to the town
             (party_get_slot, ":accumulated_tariffs", ":cur_ai_object", slot_center_accumulated_tariffs),
             (party_get_slot, ":prosperity", ":cur_ai_object", slot_town_prosperity),

			 (assign, ":tariffs_generated", ":total_change"),
			 (val_mul, ":tariffs_generated", ":prosperity"),
			 ##diplomacy start+
			 (val_add, ":tariffs_generated", 50),#round properly
			 ##diplomacy end+
			 (val_div, ":tariffs_generated", 100),
			 ##diplomacy start+
			 (val_div, ":tariffs_generated", 5),#round properly
			 ##diplomacy end+
			 (val_div, ":tariffs_generated", 20), #10 for caravans, 20 for villages
			 (val_add, ":accumulated_tariffs", ":tariffs_generated"),
			 ##diplomacy begin
        (try_begin), #no tariffs for infested villages and towns
          (party_slot_ge, ":cur_ai_object", slot_village_infested_by_bandits, 1),
          (assign,":accumulated_tariffs", 0),
        (try_end),
	     ##diplomacy end
			 (try_begin),
				(ge, "$cheat_mode", 3),
				(assign, reg4, ":tariffs_generated"),
				(str_store_party_name, s4, ":cur_ai_object"),
				(assign, reg5, ":accumulated_tariffs"),
				(display_message, "@{!}New tariffs at {s4} = {reg4}, total = {reg5}"),
			 (try_end),

             (party_set_slot, ":cur_ai_object", slot_center_accumulated_tariffs, ":accumulated_tariffs"),

             #Increasing food stocks of the town
             (party_get_slot, ":town_food_store", ":cur_ai_object", slot_party_food_store),
             (call_script, "script_center_get_food_store_limit", ":cur_ai_object"),
             (assign, ":food_store_limit", reg0),
             (val_add, ":town_food_store", 1000),
             (val_min, ":town_food_store", ":food_store_limit"),
             (party_set_slot, ":cur_ai_object", slot_party_food_store, ":town_food_store"),

             #Adding 1 to village prosperity
             (try_begin),
               (store_random_in_range, ":rand", 0, 100),
               (lt, ":rand", 5), #was 35
               (call_script, "script_change_center_prosperity", ":home_center", 1),
			   (val_add, "$newglob_total_prosperity_from_village_trade", 1),
             (try_end),
           (try_end),

           #Moving farmers to their home village
           (party_set_slot, ":party_no", slot_party_ai_object, ":home_center"),
           (party_set_slot, ":party_no", slot_party_ai_state, spai_trading_with_town),
           (party_set_ai_behavior, ":party_no", ai_bhvr_travel_to_party),
           (party_set_ai_object, ":party_no", ":home_center"),
         (try_end),
       (try_end),
    ]),
  # Centers give alarm if the player is around
  (0.5,
   [
     (store_current_hours, ":cur_hours"),
     (store_mod, ":cur_hours_mod", ":cur_hours", 11),
     (store_sub, ":hour_limit", ":cur_hours", 5),
     (party_get_num_companions, ":num_men", "p_main_party"),
     (party_get_num_prisoners, ":num_prisoners", "p_main_party"),
     (val_add, ":num_men", ":num_prisoners"),
     (convert_to_fixed_point, ":num_men"),
     (store_sqrt, ":num_men_effect", ":num_men"),
     (convert_from_fixed_point, ":num_men_effect"),
     (try_begin),
       (eq, ":cur_hours_mod", 0),
       #Reduce alarm by 2 in every 11 hours.
       (try_for_range, ":cur_faction", kingdoms_begin, kingdoms_end),
         (faction_get_slot, ":player_alarm", ":cur_faction", slot_faction_player_alarm),
         (val_sub, ":player_alarm", 1),
         (val_max, ":player_alarm", 0),
         (faction_set_slot, ":cur_faction", slot_faction_player_alarm, ":player_alarm"),
       (try_end),
     (try_end),
     (eq, "$g_player_is_captive", 0),
     (try_for_range, ":cur_center", centers_begin, centers_end),
       (store_faction_of_party, ":cur_faction", ":cur_center"),
       (store_relation, ":reln", ":cur_faction", "fac_player_supporters_faction"),
       (lt, ":reln", 0),
       (store_distance_to_party_from_party, ":dist", "p_main_party", ":cur_center"),
       (lt, ":dist", 5),
       (store_mul, ":dist_sqr", ":dist", ":dist"),
       (store_sub, ":dist_effect", 20, ":dist_sqr"),
       (store_sub, ":reln_effect", 20, ":reln"),
       (store_mul, ":total_effect", ":dist_effect", ":reln_effect"),
       (val_mul, ":total_effect", ":num_men_effect"),
       (store_div, ":spot_chance", ":total_effect", 10),
       (store_random_in_range, ":random_spot", 0, 1000),
       (lt, ":random_spot", ":spot_chance"),
       (faction_get_slot, ":player_alarm", ":cur_faction", slot_faction_player_alarm),
       (val_add, ":player_alarm", 1),
       (val_min, ":player_alarm", 100),
       (faction_set_slot, ":cur_faction", slot_faction_player_alarm, ":player_alarm"),
       (try_begin),
         (neg|party_slot_ge, ":cur_center", slot_center_last_player_alarm_hour, ":hour_limit"),
         (str_store_party_name_link, s1, ":cur_center"),
         (display_message, "@Your party is spotted by {s1}."),
         (party_set_slot, ":cur_center", slot_center_last_player_alarm_hour, ":cur_hours"),
       (try_end),
     (try_end),
    ]),
  # Assigning lords to centers with no leaders
  (72,
   [
   #(call_script, "script_assign_lords_to_empty_centers"),
    ]),
	#This is a backup script to activate the player faction if it doesn't happen automatically, for whatever reason
  (3,
	[
	(try_for_range, ":center", walled_centers_begin, walled_centers_end),
		(faction_slot_eq, "fac_player_supporters_faction", slot_faction_state, sfs_inactive),
		(store_faction_of_party, ":center_faction", ":center"),
		(eq, ":center_faction", "fac_player_supporters_faction"),
		(call_script, "script_activate_player_faction", "trp_player"),
	(try_end),
	##diplomacy start+
	#Piggyback on this: if the minister somehow gets cleared, or wasn't set
	#automatically, reappoint one.
	(try_begin),
		(is_between, "$players_kingdom", kingdoms_begin, kingdoms_end),
		(le, "$g_player_minister", 0),
		(faction_get_slot, ":faction_leader", "$players_kingdom", slot_faction_leader),
		(ge, ":faction_leader", 0),
		(try_begin),
			(this_or_next|eq, ":faction_leader", "trp_player"),
				(troop_slot_eq, "trp_player", slot_troop_spouse, ":faction_leader"),
			(assign, "$g_player_minister", "trp_temporary_minister"),
			(troop_set_faction, "trp_temporary_minister", "fac_player_supporters_faction"),
		(else_try),
			(is_between, ":faction_leader", heroes_begin, heroes_end),
			(troop_slot_eq, ":faction_leader", slot_troop_spouse, "trp_player"),
			(assign, "$g_player_minister", "trp_temporary_minister"),
			(troop_set_faction, "trp_temporary_minister", "fac_player_supporters_faction"),
		(try_end),
	(try_end),
	##diplomacy end+
	]),
	
  # Checking escape chances of prisoners that joined the party recently.
  (6,
   [(gt, "$g_prisoner_recruit_troop_id", 0),
    (gt, "$g_prisoner_recruit_size", 0),
    (gt, "$g_prisoner_recruit_last_time", 0),
    (is_currently_night),
    (try_begin),
      (store_skill_level, ":leadership", "skl_leadership", "trp_player"),
      (val_mul, ":leadership", 5),
      (store_sub, ":chance", 66, ":leadership"),
      (gt, ":chance", 0),
      (assign, ":num_escaped", 0),
      (try_for_range, ":unused", 0, "$g_prisoner_recruit_size"),
        (store_random_in_range, ":random_no", 0, 100),
        (lt, ":random_no", ":chance"),
        (val_add, ":num_escaped", 1),
      (try_end),
      (party_remove_members, "p_main_party", "$g_prisoner_recruit_troop_id", ":num_escaped"),
      (assign, ":num_escaped", reg0),
      (gt, ":num_escaped", 0),
      (try_begin),
        (gt, ":num_escaped", 1),
        (assign, reg2, 1),
      (else_try),
        (assign, reg2, 0),
      (try_end),
      (assign, reg1, ":num_escaped"),
      (str_store_troop_name_by_count, s1, "$g_prisoner_recruit_troop_id", ":num_escaped"),
      (display_log_message, "@{reg1} {s1} {reg2?have:has} escaped from your party during the night."),
    (try_end),
    (assign, "$g_prisoner_recruit_troop_id", 0),
    (assign, "$g_prisoner_recruit_size", 0),
    ]),
  # Offering ransom fees for player's prisoner heroes
  (24,
   [(neq, "$g_ransom_offer_rejected", 1),
    (call_script, "script_offer_ransom_amount_to_player_for_prisoners_in_party", "p_main_party"),
    (eq, reg0, 0),#no prisoners offered
    (assign, ":end_cond", walled_centers_end),
    (try_for_range, ":center_no", walled_centers_begin, ":end_cond"),
      (party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
      (call_script, "script_offer_ransom_amount_to_player_for_prisoners_in_party", ":center_no"),
      (eq, reg0, 1),#a prisoner is offered
      (assign, ":end_cond", 0),#break
    (try_end),
	#gekokujo 3.1 fort prison fix start
    (assign, ":end_cond", forts_end),
	(try_for_range, ":center_no", forts_begin, ":end_cond"),
      #don't need to check for fort ownership because if there's a prisoner in there, it's player-owned anyway
	  (call_script, "script_offer_ransom_amount_to_player_for_prisoners_in_party", ":center_no"),
      (eq, reg0, 1),#a prisoner is offered
      (assign, ":end_cond", 0),#break
    (try_end),
	#gekokujo 3.1 fort prison fix end
    ]),
 

  # Exchanging hero prisoners between factions and clearing old ransom offers
  (72,
   [(assign, "$g_ransom_offer_rejected", 0),
    (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
      (party_get_slot, ":town_lord", ":center_no", slot_town_lord),
      (gt, ":town_lord", 0),
      (party_get_num_prisoner_stacks, ":num_stacks", ":center_no"),
      (try_for_range_backwards, ":i_stack", 0, ":num_stacks"),
        (party_prisoner_stack_get_troop_id, ":stack_troop", ":center_no", ":i_stack"),
        (troop_is_hero, ":stack_troop"),
        (troop_slot_eq, ":stack_troop", slot_troop_occupation, slto_kingdom_hero),
        (store_random_in_range, ":random_no", 0, 100),
        (try_begin),
          (le, ":random_no", 10),
          (call_script, "script_calculate_ransom_amount_for_troop", ":stack_troop"),
          (assign, ":ransom_amount", reg0),
          ##diplomacy start+ Remove the wealth from the stack troop
          (call_script, "script_dplmc_remove_gold_from_lord_and_holdings", ":ransom_amount", ":stack_troop"),
          ##diplomacy end+
          (troop_get_slot, ":wealth", ":town_lord", slot_troop_wealth),
          (val_add, ":wealth", ":ransom_amount"),
          (troop_set_slot, ":town_lord", slot_troop_wealth, ":wealth"),
          (party_remove_prisoners, ":center_no", ":stack_troop", 1),
          (call_script, "script_remove_troop_from_prison", ":stack_troop"),
          (store_troop_faction, ":faction_no", ":town_lord"),
          (store_troop_faction, ":troop_faction", ":stack_troop"),
          (str_store_troop_name, s1, ":stack_troop"),
          (str_store_faction_name, s2, ":faction_no"),
          (str_store_faction_name, s3, ":troop_faction"),
          (display_log_message, "@{s1} of {s3} has been released from captivity."),
        (try_end),
      (try_end),
    (try_end),
    ]),
	
  # Setting random walker types
  (36,
   [(try_for_range, ":center_no", centers_begin, centers_end),
      (this_or_next|party_slot_eq, ":center_no", slot_party_type, spt_town),
      (             party_slot_eq, ":center_no", slot_party_type, spt_village),
      (call_script, "script_center_remove_walker_type_from_walkers", ":center_no", walkert_needs_money),
      (call_script, "script_center_remove_walker_type_from_walkers", ":center_no", walkert_needs_money_helped),
      (store_random_in_range, ":rand", 0, 100),
      (try_begin),
        (lt, ":rand", 70),
        (neg|party_slot_ge, ":center_no", slot_town_prosperity, 60),
        (call_script, "script_cf_center_get_free_walker", ":center_no"),
        (call_script, "script_center_set_walker_to_type", ":center_no", reg0, walkert_needs_money),
      (try_end),
    (try_end),
    ]),
  # Checking center upgrades
  (12,
   [(try_for_range, ":center_no", centers_begin, centers_end),
      (party_get_slot, ":cur_improvement", ":center_no", slot_center_current_improvement),
      (gt, ":cur_improvement", 0),
      (party_get_slot, ":cur_improvement_end_time", ":center_no", slot_center_improvement_end_hour),
      (store_current_hours, ":cur_hours"),
      (ge, ":cur_hours", ":cur_improvement_end_time"),
      (party_set_slot, ":center_no", ":cur_improvement", 1),
      (party_set_slot, ":center_no", slot_center_current_improvement, 0),
      (call_script, "script_get_improvement_details", ":cur_improvement"),
      (try_begin),
        (party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
        (str_store_party_name, s4, ":center_no"),
        (display_log_message, "@Building of {s0} in {s4} has been completed."),
      (try_end),
      (try_begin),
        (is_between, ":center_no", villages_begin, villages_end),
        (eq, ":cur_improvement", slot_center_has_fish_pond),
        (call_script, "script_change_center_prosperity", ":center_no", 5),
      (try_end),
    (try_end),
    ]),
  


#(0.1,

#	[
#	(try_begin),
#		(troop_slot_ge, "trp_player", slot_troop_spouse, active_npcs_begin),
#		(troop_get_slot, ":spouse", "trp_player", slot_troop_spouse),
#		(store_faction_of_troop, ":spouse_faction", ":spouse"),
#		(neq, ":spouse_faction", "$players_kingdom"),
#		(display_message, "@{!}ERROR! Player and spouse are separate factions"),
#	(try_end),
#	]
#),
	
  # Asking to give center to player
  (8,
   [
#    (assign, ":done", 0),
#    (try_for_range, ":center_no", centers_begin, centers_end),
#      (eq, ":done", 0),
#      (party_slot_eq, ":center_no", slot_town_lord, stl_reserved_for_player),
#      (assign, "$g_center_to_give_to_player", ":center_no"),
 #     (try_begin),
  #      (eq, "$g_center_to_give_to_player", "$g_castle_requested_by_player"),
   #     (assign, "$g_castle_requested_by_player", 0),
	#	(try_begin),
	#		(eq, "$g_castle_requested_for_troop", "trp_player"),
	#		(jump_to_menu, "mnu_requested_castle_granted_to_player"),
	#	(else_try),
	#		(jump_to_menu, "mnu_requested_castle_granted_to_player_husband"),
	#	(try_end),	
    #  (else_try),
    #    (jump_to_menu, "mnu_give_center_to_player"),
    # (try_end),
    #  (assign, ":done", 1),
    #(else_try),
    #  (eq, ":center_no", "$g_castle_requested_by_player"),
    #  (party_slot_ge, ":center_no", slot_town_lord, active_npcs_begin),
    #  (assign, "$g_castle_requested_by_player", 0),
    #  (store_faction_of_party, ":faction", ":center_no"),
    #  (eq, ":faction", "$players_kingdom"),
    #  (assign, "$g_center_to_give_to_player", ":center_no"),
	#  (try_begin),
#		(eq, "$player_has_homage", 1),
#		(jump_to_menu, "mnu_requested_castle_granted_to_another"),
#	  (else_try),	
#		(jump_to_menu, "mnu_requested_castle_granted_to_another_female"),
#	  (try_end),	
 #     (assign, ":done", 1),
  #  (try_end),
    ]),
  
  # Taking mon from player while resting in not owned centers
  (1,
   [(neg|map_free),
    (is_currently_night),
#    (ge, "$g_last_rest_center", 0),
    (is_between, "$g_last_rest_center", centers_begin, centers_end),
    (neg|party_slot_eq, "$g_last_rest_center", slot_town_lord, "trp_player"),
    
##diplomacy begin
    (party_get_slot, ":town_lord", "$g_last_rest_center", slot_town_lord),
    (assign, reg0, 0),
    (try_begin),
      (is_between, ":town_lord", lords_begin, kingdom_ladies_end),
      (call_script, "script_dplmc_is_affiliated_family_member", ":town_lord"),
      (try_begin),
        (neq, reg0, 0),
        (display_message, "@You are within the walls of an affiliated family member and don't have to pay for accommodation."),
      (try_end),
    (try_end),
    (eq, reg0, 0),
##diplomacy end
    
    (store_faction_of_party, ":last_rest_center_faction", "$g_last_rest_center"),
    (neq, ":last_rest_center_faction", "fac_player_supporters_faction"),
    (store_current_hours, ":cur_hours"),
    (ge, ":cur_hours", "$g_last_rest_payment_until"),
    (store_add, "$g_last_rest_payment_until", ":cur_hours", 24),
    (store_troop_gold, ":gold", "trp_player"),
    (party_get_num_companions, ":num_men", "p_main_party"),
    (store_div, ":total_cost", ":num_men", 4),
    (val_add, ":total_cost", 1),
    (try_begin),
      (ge, ":gold", ":total_cost"),
      (display_message, "@You pay for accommodation."),
      (troop_remove_gold, "trp_player", ":total_cost"),
    (else_try),
      (gt, ":gold", 0),
      (troop_remove_gold, "trp_player", ":gold"),
    (try_end),
    ]),
  
  # Check if a faction is defeated every day
  (24,
   [
    (assign, ":num_active_factions", 0),
    (try_for_range, ":cur_kingdom", kingdoms_begin, kingdoms_end),
      (faction_set_slot, ":cur_kingdom", slot_faction_number_of_parties, 0),
    (try_end),
    (try_for_parties, ":cur_party"),
      (store_faction_of_party, ":party_faction", ":cur_party"),
      (is_between, ":party_faction", kingdoms_begin, kingdoms_end),
      (this_or_next|is_between, ":cur_party", centers_begin, centers_end),
	  (party_slot_eq, ":cur_party", slot_party_type, spt_kingdom_hero_party),
      (faction_get_slot, ":kingdom_num_parties", ":party_faction", slot_faction_number_of_parties),
      (val_add, ":kingdom_num_parties", 1),
      (faction_set_slot, ":party_faction", slot_faction_number_of_parties, ":kingdom_num_parties"), 
    (try_end),
    (try_for_range, ":cur_kingdom", kingdoms_begin, kingdoms_end),
      #(try_begin),
        #(eq, "$cheat_mode", 1),
        #(str_store_faction_name, s1, ":cur_kingdom"),
        #(faction_get_slot, reg1, ":cur_kingdom", slot_faction_number_of_parties),        
        #(display_message, "@{!}Number of parties belonging to {s1}: {reg1}"),
      #(try_end),
      (faction_slot_eq, ":cur_kingdom", slot_faction_state, sfs_active),
      (val_add, ":num_active_factions", 1),
      (faction_slot_eq, ":cur_kingdom", slot_faction_number_of_parties, 0),
      (assign, ":faction_removed", 0),
      (try_begin),
        (eq, ":cur_kingdom", "fac_player_supporters_faction"),
        (try_begin),
          (le, "$supported_pretender", 0),
          (faction_set_slot, ":cur_kingdom", slot_faction_state, sfs_inactive),
          (assign, ":faction_removed", 1),
        (try_end),
      (else_try),
        (neq, "$players_kingdom", ":cur_kingdom"),
        (faction_set_slot, ":cur_kingdom", slot_faction_state, sfs_defeated),
        (try_for_parties, ":cur_party"),
          (store_faction_of_party, ":party_faction", ":cur_party"),
          (eq, ":party_faction", ":cur_kingdom"),
          (party_get_slot, ":home_center", ":cur_party", slot_party_home_center),
          (store_faction_of_party, ":home_center_faction", ":home_center"),
          (party_set_faction, ":cur_party", ":home_center_faction"),
        (try_end),
        (assign, ":kingdom_pretender", -1),
        (try_for_range, ":cur_pretender", pretenders_begin, pretenders_end),
          (troop_slot_eq, ":cur_pretender", slot_troop_original_faction, ":cur_kingdom"),
          (assign, ":kingdom_pretender", ":cur_pretender"),
        (try_end),
        (try_begin),
          (is_between, ":kingdom_pretender", pretenders_begin, pretenders_end),
          (neq, ":kingdom_pretender", "$supported_pretender"),
          (troop_set_slot, ":kingdom_pretender", slot_troop_cur_center, 0), #remove pretender from the world
        (try_end),
        (assign, ":faction_removed", 1),
        (try_begin),
          (eq, "$players_oath_renounced_against_kingdom", ":cur_kingdom"),
          (assign, "$players_oath_renounced_against_kingdom", 0),
          (assign, "$players_oath_renounced_given_center", 0),
          (assign, "$players_oath_renounced_begin_time", 0),
          (call_script, "script_add_notification_menu", "mnu_notification_oath_renounced_faction_defeated", ":cur_kingdom", 0),
        (try_end),
        #This menu must be at the end because faction banner will change after this menu if the player's supported pretender's original faction is cur_kingdom
        (call_script, "script_add_notification_menu", "mnu_notification_faction_defeated", ":cur_kingdom", 0),
      (try_end),
      (try_begin),
        (eq, ":faction_removed", 1),
        (val_sub, ":num_active_factions", 1),
        #(call_script, "script_store_average_center_value_per_faction"),
      (try_end),
      (try_for_range, ":cur_kingdom_2", kingdoms_begin, kingdoms_end),
        (call_script, "script_update_faction_notes", ":cur_kingdom_2"),
      (try_end),
    (try_end),
    (try_begin),
      (eq, ":num_active_factions", 1),
      (eq, "$g_one_faction_left_notification_shown", 0),
      (assign, "$g_one_faction_left_notification_shown", 1),
      (try_for_range, ":cur_kingdom", kingdoms_begin, kingdoms_end),
        (faction_slot_eq, ":cur_kingdom", slot_faction_state, sfs_active),
        (call_script, "script_add_notification_menu", "mnu_notification_one_faction_left", ":cur_kingdom", 0),
        (try_begin),
          (eq, ":cur_kingdom", "fac_kingdom_28"),
          (faction_set_slot, "fac_kingdom_28", slot_faction_leader, "trp_kingdom_28_lord2"),
          (call_script, "script_add_notification_menu", "mnu_xinzhengfuchengli", ":cur_kingdom", 0),
        (try_end),
      (try_end),
    (try_end),
    ]),
  (3, #check to see if player's court has been captured
   [
     ##diplomacy start+ The player might be the ruler of another kingdom
     (assign, ":save_reg0", reg0),
	 (assign, ":alt_led_faction", "fac_player_supporters_faction"),
	 (try_begin),
		(is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
		(call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", "$players_kingdom"),
	    (ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
		(assign, ":alt_led_faction", "$players_kingdom"),
	 (try_end),
	 ##diplomacy end+
     (try_begin), #The old court has been lost
     ##diplomacy begin
       (is_between, "$g_player_court", centers_begin, centers_end),
       (party_slot_eq, "$g_player_court", slot_village_infested_by_bandits, "trp_peasant_woman"),
       (call_script, "script_add_notification_menu", "mnu_notification_court_lost", 0, 0),
     (else_try),
     ##diplomacy end
       (is_between, "$g_player_court", centers_begin, centers_end),
       (store_faction_of_party, ":court_faction", "$g_player_court"),
       (neq, ":court_faction", "fac_player_supporters_faction"),
	   ##diplomacy start+ The player might be ruler of a faction other than fac_player_supporters_faction
	   (neq, ":court_faction", ":alt_led_faction"),
	   ##diplomacy end+
       (call_script, "script_add_notification_menu", "mnu_notification_court_lost", 0, 0),
     (else_try),	#At least one new court has been found
       (lt, "$g_player_court", centers_begin),
       #Will by definition not active until a center is taken by the player faction
       #Player minister must have been appointed at some point
       (this_or_next|faction_slot_eq, "fac_player_supporters_faction", slot_faction_leader, "trp_player"),
		(gt, "$g_player_minister", 0),

       (assign, ":center_found", 0),
       (try_for_range, ":walled_center", walled_centers_begin, walled_centers_end),
         (eq, ":center_found", 0),
         (store_faction_of_party, ":court_faction", ":walled_center"),
		   ##diplomacy start+ The player might be ruler of a faction other than fac_player_supporters_faction
		   (this_or_next|eq, ":court_faction", ":alt_led_faction"),
		   ##diplomacy end+
         (eq, ":court_faction", "fac_player_supporters_faction"),
         (assign, ":center_found", ":walled_center"),
       (try_end),
       (ge, ":center_found", 1),
       (call_script, "script_add_notification_menu", "mnu_notification_court_lost", 0, 0),
     (try_end),
     #Also, piggy-backing on this -- having bandits go to lairs and back
     (try_for_parties, ":bandit_party"),
       (gt, ":bandit_party", "p_spawn_points_end"),
       (party_get_template_id, ":bandit_party_template", ":bandit_party"),
       (is_between, ":bandit_party_template", "pt_seto_pirates", "pt_deserters"),
       (party_template_get_slot, ":bandit_lair", ":bandit_party_template", slot_party_template_lair_party),
       (try_begin),#If party is active and bandit is far away, then move to location
         (gt, ":bandit_lair", "p_spawn_points_end"),
         (store_distance_to_party_from_party, ":distance", ":bandit_party", ":bandit_lair"), #this is the cause of the error
         (gt, ":distance", 30),
         #All this needs checking
         (party_set_ai_behavior, ":bandit_party", ai_bhvr_travel_to_point),
         (party_get_position, pos5, ":bandit_lair"),
         (party_set_ai_target_position, ":bandit_party", pos5),
       (else_try), #Otherwise, act freely
         (get_party_ai_behavior, ":behavior", ":bandit_party"),
         (eq, ":behavior", ai_bhvr_travel_to_point),
         (try_begin),
           (gt, ":bandit_lair", "p_spawn_points_end"),
           (store_distance_to_party_from_party, ":distance", ":bandit_party", ":bandit_lair"),
           (lt, ":distance", 3),
           (party_set_ai_behavior, ":bandit_party", ai_bhvr_patrol_party),
           (party_template_get_slot, ":spawnpoint", ":bandit_party_template", slot_party_template_lair_spawnpoint),
           (party_set_ai_object, ":bandit_party", ":spawnpoint"),
           (party_set_ai_patrol_radius, ":bandit_party", 45),
         (else_try),
           (lt, ":bandit_lair", "p_spawn_points_end"),
           (party_set_ai_behavior, ":bandit_party", ai_bhvr_patrol_party),
           (party_template_get_slot, ":spawnpoint", ":bandit_party_template", slot_party_template_lair_spawnpoint),
           (party_set_ai_object, ":bandit_party", ":spawnpoint"),
           (party_set_ai_patrol_radius, ":bandit_party", 45),
         (try_end),
       (try_end),
     (try_end),
     #Piggybacking on trigger:
     (try_begin),
       (troop_get_slot, ":betrothed", "trp_player", slot_troop_betrothed),
       (gt, ":betrothed", 0),
       (neg|check_quest_active, "qst_wed_betrothed"),
       (neg|check_quest_active, "qst_wed_betrothed_female"),
       (str_store_troop_name, s5, ":betrothed"),
       (display_message, "@Betrothal to {s5} expires"),
       (troop_set_slot, "trp_player", slot_troop_betrothed, -1),
       (troop_set_slot, ":betrothed", slot_troop_betrothed, -1),
     (try_end),
	 ##diplomacy start+
	 (assign, reg0, ":save_reg0"),#revert register
	 ##diplomacy end+
     ]),
  
#####!!!!!

# Village upgrade triggers

# School
  (30 * 24,
   [(try_for_range, ":cur_village", villages_begin, villages_end),
      (party_slot_eq, ":cur_village", slot_town_lord, "trp_player"),
      (party_slot_eq, ":cur_village", slot_center_has_school, 1),
      (party_get_slot, ":cur_relation", ":cur_village", slot_center_player_relation),
      (val_add, ":cur_relation", 1),
      (val_min, ":cur_relation", 100),
      (party_set_slot, ":cur_village", slot_center_player_relation, ":cur_relation"),
    (try_end),
    ]),
  (2, [
       (try_for_range, ":troop_no", active_npcs_begin, active_npcs_end),
		 (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
		 (troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
         (ge, ":party_no", 1),
		 (party_is_active, ":party_no"),
         (party_slot_eq, ":party_no", slot_party_following_player, 1),
         (store_current_hours, ":cur_time"),
         (neg|party_slot_ge, ":party_no", slot_party_follow_player_until_time, ":cur_time"),
         (party_set_slot, ":party_no", slot_party_commander_party, -1),
         (party_set_slot, ":party_no", slot_party_following_player, 0),
         (assign,  ":dont_follow_period", 200),
         (store_add, ":dont_follow_time", ":cur_time", ":dont_follow_period"),
         (party_set_slot, ":party_no", slot_party_dont_follow_player_until_time,  ":dont_follow_time"),
       (try_end),
    ]),
#persuade_lords_to_make_peace begin
  (72, [(gt, "$g_force_peace_faction_1", 0),
        (gt, "$g_force_peace_faction_2", 0),
        (try_begin),
          (store_relation, ":relation", "$g_force_peace_faction_1", "$g_force_peace_faction_2"),
          (lt, ":relation", 0),
          (call_script, "script_diplomacy_start_peace_between_kingdoms", "$g_force_peace_faction_1", "$g_force_peace_faction_2", 1),
        (try_end),
        (assign, "$g_force_peace_faction_1", 0),
        (assign, "$g_force_peace_faction_2", 0),
       ]),
  

#NPC changes begin
#Resolve one issue each hour
(1, 
   [           
		(str_store_string, s51, "str_no_trigger_noted"),
		
		# Rejoining party
        (try_begin),
            (gt, "$npc_to_rejoin_party", 0),
            (eq, "$g_infinite_camping", 0),
            (try_begin),
                (neg|main_party_has_troop, "$npc_to_rejoin_party"),
                (neq, "$g_player_is_captive", 1),

				(str_store_string, s51, "str_triggered_by_npc_to_rejoin_party"),
				
                (assign, "$npc_map_talk_context", slot_troop_days_on_mission),
                (start_map_conversation, "$npc_to_rejoin_party", -1),
			(else_try),
				(troop_set_slot, "$npc_to_rejoin_party", slot_troop_current_mission, npc_mission_rejoin_when_possible),
				(assign, "$npc_to_rejoin_party", 0),
            (try_end),			
		# Here do NPC that is quitting
		(else_try),
            (gt, "$npc_is_quitting", 0),
            (eq, "$g_infinite_camping", 0),
            (try_begin),
                (main_party_has_troop, "$npc_is_quitting"),
                (neq, "$g_player_is_captive", 1),
                (neq, "$g_gekokujo_companion_neverquit", 1), #gekokujo 3.0 companion interaction
				##diplomacy start+ disable spouse quitting to avoid problems
				(neg|troop_slot_eq, "trp_player", slot_troop_spouse, "$npc_is_quitting"),
				(neg|troop_slot_eq, "$npc_is_quitting", slot_troop_spouse, "trp_player"),
				##diplomacy end+
				(str_store_string, s51, "str_triggered_by_npc_is_quitting"),
                (start_map_conversation, "$npc_is_quitting", -1),
            (else_try),
                (assign, "$npc_is_quitting", 0),
            (try_end),
		#NPC with grievance	
        (else_try), #### Grievance
            (gt, "$npc_with_grievance", 0),
            (eq, "$g_infinite_camping", 0),
            (eq, "$disable_npc_complaints", 0),
            (try_begin),
                (main_party_has_troop, "$npc_with_grievance"),
                (neq, "$g_player_is_captive", 1),

				(str_store_string, s51, "str_triggered_by_npc_has_grievance"),
				
                (assign, "$npc_map_talk_context", slot_troop_morality_state),
                (start_map_conversation, "$npc_with_grievance", -1),
            (else_try),
                (assign, "$npc_with_grievance", 0),
            (try_end),
        (else_try),
            (gt, "$npc_with_personality_clash", 0),
            (eq, "$g_infinite_camping", 0),
            (eq, "$disable_npc_complaints", 0),
            (troop_get_slot, ":object", "$npc_with_personality_clash", slot_troop_personalityclash_object),
            (try_begin),
                (main_party_has_troop, "$npc_with_personality_clash"),
                (main_party_has_troop, ":object"),
                (neq, "$g_player_is_captive", 1),
				
                (assign, "$npc_map_talk_context", slot_troop_personalityclash_state),
				(str_store_string, s51, "str_triggered_by_npc_has_personality_clash"),
                (start_map_conversation, "$npc_with_personality_clash", -1),
            (else_try),
                (assign, "$npc_with_personality_clash", 0),
            (try_end),
        (else_try), #### Political issue
            (gt, "$npc_with_political_grievance", 0),
            (eq, "$g_infinite_camping", 0),
            (eq, "$disable_npc_complaints", 0),
            (try_begin),
                (main_party_has_troop, "$npc_with_political_grievance"),
                (neq, "$g_player_is_captive", 1),
				
				(str_store_string, s51, "str_triggered_by_npc_has_political_grievance"),
                (assign, "$npc_map_talk_context", slot_troop_kingsupport_objection_state),
                (start_map_conversation, "$npc_with_political_grievance", -1),
			(else_try),
				(assign, "$npc_with_political_grievance", 0),
            (try_end),
		(else_try),	
            (eq, "$disable_sisterly_advice", 0),
            (eq, "$g_infinite_camping", 0),
            (gt, "$npc_with_sisterly_advice", 0),
            (try_begin),
				(main_party_has_troop, "$npc_with_sisterly_advice"),
                (neq, "$g_player_is_captive", 1),

				##diplomacy start+
				(troop_slot_ge, "$npc_with_sisterly_advice", slot_troop_woman_to_woman_string, 1),
				##diplomacy end+
				(assign, "$npc_map_talk_context", slot_troop_woman_to_woman_string), #was npc_with_sisterly advice
	            (start_map_conversation, "$npc_with_sisterly_advice", -1),
			(else_try),
				(assign, "$npc_with_sisterly_advice", 0),
            (try_end),
		(else_try), #check for regional background
            (eq, "$disable_local_histories", 0),
            (eq, "$g_infinite_camping", 0),
            (try_for_range, ":npc", companions_begin, companions_end),
                (main_party_has_troop, ":npc"),           
                (troop_slot_eq, ":npc", slot_troop_home_speech_delivered, 0),
                (troop_get_slot, ":home", ":npc", slot_troop_home),
                (gt, ":home", 0),
                (store_distance_to_party_from_party, ":distance", ":home", "p_main_party"),
                (lt, ":distance", 7),
                (assign, "$npc_map_talk_context", slot_troop_home),
				
				(str_store_string, s51, "str_triggered_by_local_histories"),
				
                (start_map_conversation, ":npc", -1),
            (try_end),
        (try_end),
		
		#add pretender to party if not active
		(try_begin),
			(check_quest_active, "qst_rebel_against_kingdom"),
			(is_between, "$supported_pretender", pretenders_begin, pretenders_end),
			(neg|main_party_has_troop, "$supported_pretender"),
			(neg|troop_slot_eq, "$supported_pretender", slot_troop_occupation, slto_kingdom_hero),
			(party_add_members, "p_main_party", "$supported_pretender", 1),
		(try_end),
		
		#make player marshal of rebel faction
		(try_begin),
			(check_quest_active, "qst_rebel_against_kingdom"),
			(is_between, "$supported_pretender", pretenders_begin, pretenders_end),
			(main_party_has_troop, "$supported_pretender"),
			(neg|faction_slot_eq, "fac_player_supporters_faction", slot_faction_marshall, "trp_player"),
			(call_script, "script_appoint_faction_marshall", "fac_player_supporters_faction", "trp_player"),
		(try_end),
		
		
]),
#NPC changes end

(4,
   ##diplomacy start+ Add support for promoted kingdom ladies
   ##OLD:
   #[(try_for_range, ":troop_no", active_npcs_begin, active_npcs_end),
   ##NEW:
   [(try_for_range, ":troop_no", heroes_begin, heroes_end),
      (this_or_next|is_between, ":troop_no", active_npcs_begin, active_npcs_end),
	  (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
   ##diplomacy end+
      (troop_slot_ge, ":troop_no", slot_troop_change_to_faction, 1),
      (store_troop_faction, ":faction_no", ":troop_no"),
      (troop_get_slot, ":new_faction_no", ":troop_no", slot_troop_change_to_faction),
      (troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
      (assign, ":continue", 0),
      (try_begin),
        (le, ":party_no", 0),
        #(troop_slot_eq, ":troop_no", slot_troop_is_prisoner, 0),
        (neg|troop_slot_ge, ":troop_no", slot_troop_prisoner_of_party, 0),
        (assign, ":continue", 1),
      (else_try),
        (gt, ":party_no", 0),

        #checking if the party is outside the centers
        (party_get_attached_to, ":cur_center_no", ":party_no"),
        (try_begin),
          (lt, ":cur_center_no", 0),
          (party_get_cur_town, ":cur_center_no", ":party_no"),
        (try_end),
        (this_or_next|neg|is_between, ":cur_center_no", centers_begin, centers_end),
        (party_slot_eq, ":cur_center_no", slot_town_lord, ":troop_no"),

        #checking if the party is away from his original faction parties
		##diplomacy start+
		##Add support for promoted kingdom lades.
		##OLD:
        #(assign, ":end_cond", active_npcs_end),
		##NEW:
        (assign, ":end_cond", heroes_end),
		##diplomacy end+
        (try_for_range, ":enemy_troop_no", active_npcs_begin, ":end_cond"),
		  (troop_slot_eq, ":enemy_troop_no", slot_troop_occupation, slto_kingdom_hero),
          (troop_get_slot, ":enemy_party_no", ":enemy_troop_no", slot_troop_leaded_party),
          (party_is_active, ":enemy_party_no"),
          (store_faction_of_party, ":enemy_faction_no", ":enemy_party_no"),
          (eq, ":enemy_faction_no", ":faction_no"),
          (store_distance_to_party_from_party, ":dist", ":party_no", ":enemy_party_no"),
          (lt, ":dist", 4),
          (assign, ":end_cond", 0),
        (try_end),
        (neq, ":end_cond", 0),
        (assign, ":continue", 1),
      (try_end),
	  # NE - don't want DKs defecting unless they have been defeated
	  (try_begin),
	  (eq, ":faction_no", "fac_dark_knights"),
	  (try_begin),
	  (faction_slot_eq, ":faction_no", slot_faction_state, sfs_defeated),
	  (assign, ":continue", 1),
	  (else_try), 
	  (assign, ":continue", 0),
	  (try_end), 
	  (try_end),
	  # NE end 
	  
      (eq, ":continue", 1),

		(try_begin),
			(ge, "$cheat_mode", 1),
			(str_store_troop_name, s4, ":troop_no"),
			(display_message, "@{!}DEBUG - {s4} faction changed from slot_troop_change_to_faction"),
		(try_end),

      (call_script, "script_change_troop_faction", ":troop_no", ":new_faction_no"),
      (troop_set_slot, ":troop_no", slot_troop_change_to_faction, 0),
      (try_begin),
        (is_between, ":new_faction_no", kingdoms_begin, kingdoms_end),
        (str_store_troop_name_link, s1, ":troop_no"),
        (str_store_faction_name_link, s2, ":faction_no"),
        (str_store_faction_name_link, s3, ":new_faction_no"),
        (display_message, "@{s1} has switched from {s2} to {s3}."),
        (try_begin),
          (eq, ":faction_no", "$players_kingdom"),
          (call_script, "script_add_notification_menu", "mnu_notification_troop_left_players_faction", ":troop_no", ":new_faction_no"),
        (else_try),
          (eq, ":new_faction_no", "$players_kingdom"),
          (call_script, "script_add_notification_menu", "mnu_notification_troop_joined_players_faction", ":troop_no", ":faction_no"),
        (try_end),
      (try_end),
    (try_end),
    ]),
(1,
   [
     (eq, "$cheat_mode", 1),
     (try_for_range, ":center_no", centers_begin, centers_end),
       (party_get_battle_opponent, ":besieger_party", ":center_no"),
       (try_begin),
         (gt, ":besieger_party", 0),
         (str_store_party_name, s2, ":center_no"),
         (str_store_party_name, s3, ":besieger_party"),
         (display_message, "@{!}DEBUG : {s2} is besieging by {s3}"),
       (try_end),
     (try_end),    
     ]),
 # reserved for future use. For backward compatibility, we need to use these triggers instead of creating new ones.
  
  (1,
   [
     (call_script, "script_calculate_castle_prosperities_by_using_its_villages"),

     (store_add, ":fac_kingdom_6_plus_one", "fac_kingdom_6", 1),

     (try_for_range, ":faction_1", "fac_kingdom_1", ":fac_kingdom_6_plus_one"),
       (try_for_range, ":faction_2", "fac_kingdom_1", ":fac_kingdom_6_plus_one"),
         (store_relation, ":faction_relation", ":faction_1", ":faction_2"),
         (str_store_faction_name, s7, ":faction_1"),
         (str_store_faction_name, s8, ":faction_2"),
         (neq, ":faction_1", ":faction_2"),
         (assign, reg1, ":faction_relation"),
         #(display_message, "@{s7}-{s8}, relation is {reg1}"),
       (try_end),
     (try_end),          
   ]),
   
  (1,
   [   
     (try_begin),
       (eq, "$g_player_is_captive", 1),
       (neg|party_is_active, "$capturer_party"),
       (rest_for_hours, 0, 0, 0),
     (try_end),            
     
     ##diplomacy begin
      #seems to be a native bug
     (is_between, "$next_center_will_be_fired", villages_begin, villages_end),
     ##diplomacy end
     (assign, ":village_no", "$next_center_will_be_fired"),
     (party_get_slot, ":is_there_already_fire", ":village_no", slot_village_smoke_added),
     (eq, ":is_there_already_fire", 0),
	 
	 
     (try_begin),
       (party_get_slot, ":bound_center", ":village_no", slot_village_bound_center),  
       (party_get_slot, ":last_nearby_fire_time", ":bound_center", slot_town_last_nearby_fire_time),
       (store_current_hours, ":cur_hours"),
	   
	   (try_begin),
		(eq, "$cheat_mode", 1),
		(is_between, ":village_no", centers_begin, centers_end),
		(is_between, ":bound_center", centers_begin, centers_end),
		(str_store_party_name, s4, ":village_no"),
		(str_store_party_name, s5, ":bound_center"),
		(store_current_hours, reg3),
        (party_get_slot, reg4, ":bound_center", slot_town_last_nearby_fire_time),
		(display_message, "@{!}DEBUG - Checking fire at {s4} for {s5} - current time {reg3}, last nearby fire {reg4}"),
	   (try_end),
	   
	   
       (eq, ":cur_hours", ":last_nearby_fire_time"),
       (party_add_particle_system, ":village_no", "psys_map_village_fire"),
       (party_add_particle_system, ":village_no", "psys_map_village_fire_smoke"),       
     (else_try),  
       (store_add, ":last_nearby_fire_finish_time", ":last_nearby_fire_time", fire_duration),
       (eq, ":last_nearby_fire_finish_time", ":cur_hours"),
       (party_clear_particle_systems, ":village_no"),
     (try_end),  
     

   ]),
  ##diplomacy begin
  #Troop AI Spouse: Spouse thinking
  (3,
   [
	(troop_get_slot, ":player_spouse", "trp_player", slot_troop_spouse),
	(ge, ":player_spouse", active_npcs_begin),#<-- skip the rest of the check when there is no spouse
    (try_for_parties, ":spouse_party"),
      (party_slot_eq, ":spouse_party", slot_party_type, dplmc_spt_spouse),

      (party_get_slot, ":spouse_target", ":spouse_party", slot_party_orders_object),
      (party_get_slot, ":home_center", ":spouse_party", slot_party_home_center),
      (store_distance_to_party_from_party, ":distance", ":spouse_party", ":spouse_target"),

      #Moving spouse to home village
      (try_begin),
        (le, ":distance", 1),
        (try_begin),
          (this_or_next|eq, ":spouse_target", "$g_player_court"),
		      (eq, ":spouse_target", ":home_center"),
          (remove_party, ":spouse_party"),
          (troop_set_slot, ":player_spouse", slot_troop_cur_center, ":spouse_target"),
        (else_try),
          (try_begin),
            (is_between, ":spouse_target", villages_begin, villages_end),
            (party_get_slot,":cur_merchant",":spouse_target", slot_town_elder),
          (else_try),
            (party_get_slot,":cur_merchant",":spouse_target", slot_town_merchant),
          (try_end),
          (troop_get_slot, ":amount", ":player_spouse", dplmc_slot_troop_mission_diplomacy),
          (troop_remove_items, ":cur_merchant", "itm_bread", ":amount"),
          (party_set_ai_behavior, ":spouse_party", ai_bhvr_travel_to_party),
          (try_begin),
            (gt, "$g_player_court", 0),
            (party_set_slot, ":spouse_party", slot_party_ai_object, "$g_player_court"),
            (party_set_ai_object, ":spouse_party", "$g_player_court"),
          (else_try),
            (party_set_slot, ":spouse_party", slot_party_ai_object, ":home_center"),
            (party_set_ai_object, ":spouse_party", ":home_center"),
          (try_end),

          (troop_add_items, "trp_household_possessions", "itm_bread", ":amount"),
        (try_end),
      (try_end),
    (try_end),
    ]),
  #create ai patrols
   (24 * 7,
   [
    (try_for_range, ":kingdom", npc_kingdoms_begin, npc_kingdoms_end),

      (assign, ":max_patrols", 0),
      (try_for_range, ":center", towns_begin, towns_end),
        (store_faction_of_party, ":center_faction", ":center"),
        (eq, ":center_faction", ":kingdom"),
        (val_add, ":max_patrols", 1),
      (try_end),

      (assign, ":count", 0),
      (try_for_parties, ":party_no"),
        (party_slot_eq, ":party_no", slot_party_type, spt_patrol),
        (store_faction_of_party, ":party_faction", ":party_no"),
        (eq, ":party_faction", ":kingdom"),
        (neg|party_slot_eq, ":party_no", dplmc_slot_party_mission_diplomacy, "trp_player"), #not player ordered
        (try_begin),
           #Remove patrols above the maximum number allowed.
           (ge, ":count", ":max_patrols"),
           (try_begin),
              (ge, "$cheat_mode", 1),
              (str_store_faction_name, s4, ":kingdom"),
              (str_store_party_name, s5, ":party_no"),
              (display_message, "@{!}DEBUG - Removed {s5} because {s4} cannot support that many patrols"),
           (try_end),
           (remove_party, ":party_no"),
        (else_try),
           (val_add, ":count", 1),
        (try_end),
      (try_end),

      (try_begin),
        (lt, ":count", ":max_patrols"),

        (store_random_in_range, ":random", 0, 10),
        (le, ":random", 3),

        (assign, ":start_center", -1),
        (assign, ":target_center", -1),

        (try_for_range, ":center", towns_begin, towns_end),
          (store_faction_of_party, ":center_faction", ":center"),
          (eq, ":center_faction", ":kingdom"),

          (eq, ":start_center", -1),
          (eq, ":target_center", -1),

          (assign, ":continue", 1),
          (try_for_parties, ":party_no"),
            (party_slot_eq, ":party_no", slot_party_type, spt_patrol),
            (store_faction_of_party, ":party_faction", ":party_no"),
            (eq, ":party_faction", ":kingdom"),
            (party_get_slot, ":target", ":party_no", slot_party_ai_object),
            (eq, ":target", ":center"),
            (assign, ":continue", 0),
          (try_end),
          (eq, ":continue", 1),

          (call_script, "script_cf_select_random_town_with_faction", ":kingdom"),
          (neq, reg0, -1),

          (assign, ":start_center", reg0),
          (assign, ":target_center", ":center"),
        (try_end),

        (try_begin),
          (neq, ":start_center", -1),
          (neq, ":target_center", -1),
          (store_random_in_range, ":random_size", 0, 3),
          (faction_get_slot, ":faction_leader", ":kingdom", slot_faction_leader),
          (call_script, "script_dplmc_send_patrol", ":start_center", ":target_center", ":random_size",":kingdom", ":faction_leader"),
        (try_end),
      (try_end),
    (try_end),
    ]),
  # Patrol ai
   (2,
   [

    (try_for_parties, ":party_no"),
      (party_slot_eq,":party_no", slot_party_type, spt_patrol),

      (call_script, "script_party_remove_all_prisoners", ":party_no"),

      (try_begin),
        (get_party_ai_behavior, ":ai_behavior", ":party_no"),
        (eq, ":ai_behavior", ai_bhvr_travel_to_party),
        (party_get_slot, ":target_party", ":party_no", slot_party_ai_object),

        (try_begin),
          (gt, ":target_party", 0),
          (store_distance_to_party_from_party, ":distance_to_target", ":party_no", ":target_party"),
          (le, ":distance_to_target", 5),
          (try_begin),
            (party_get_slot, ":ai_state", ":party_no", slot_party_ai_state),
            (eq, ":ai_state", spai_retreating_to_center),
            (try_begin),
              (le, ":distance_to_target", 1),
              (call_script, "script_party_add_party", ":target_party", ":party_no"),
              (remove_party, ":party_no"),
            (try_end),
          (else_try),
            (party_get_position, pos1, ":target_party"),
            (party_set_ai_behavior,":party_no", ai_bhvr_patrol_location),
            (party_set_ai_patrol_radius, ":party_no", 1),
            (party_set_ai_target_position, ":party_no", pos1),
          (try_end),
        (else_try),
          #remove party?
        (try_end),

      (try_end),
    (try_end),
    ]),
  # Scout ai
   (0.2,
   [

    (try_for_parties, ":party_no"),
      (party_slot_eq,":party_no", slot_party_type, spt_scout),

      (try_begin),
        (get_party_ai_behavior, ":ai_behavior", ":party_no"),
        (this_or_next|eq, ":ai_behavior", ai_bhvr_travel_to_point),
        (eq, ":ai_behavior", ai_bhvr_travel_to_party),

        (party_get_slot, ":target_party", ":party_no", slot_party_ai_object),
        (store_distance_to_party_from_party, ":distance_to_target", ":party_no", ":target_party"),
        (le, ":distance_to_target", 1),

        (try_begin),
          (eq, ":target_party", "p_main_party"),

          (party_get_slot, ":mission_target", ":party_no", dplmc_slot_party_mission_diplomacy),
          (call_script, "script_add_notification_menu", "mnu_dplmc_scout", ":mission_target", 0),

          (remove_party, ":party_no"),
        (else_try),
          (neq, ":target_party", "p_main_party"),
          (party_get_slot, ":hours", ":party_no", dplmc_slot_party_mission_diplomacy),

          (try_begin),
            (le, ":hours", 100),
            (disable_party, ":party_no"),
            (val_add, ":hours", 1),
            (party_set_slot, ":party_no", dplmc_slot_party_mission_diplomacy, ":hours"),

            (try_begin),
              (store_random_in_range, ":random", 0, 1000),
              (eq, ":random", 0),
              (str_store_party_name, s11, ":target_party"),
              (display_log_message, "@It is rumoured that a spy has been caught in {s11}.", 0xFF0000),
              (remove_party, ":party_no"),
            (try_end),

          (else_try),
            (enable_party, ":party_no"),
            (party_set_ai_behavior, ":party_no", ai_bhvr_travel_to_party),
            (party_set_ai_object, ":party_no", "p_main_party"),
            (party_set_slot, ":party_no", slot_party_ai_object, "p_main_party"),
            (party_set_slot, ":party_no", dplmc_slot_party_mission_diplomacy, ":target_party"),
          (try_end),

        (try_end),
      (try_end),
    (try_end),
    ]),
  # Policy
   (30 * 24,
   [
	##nested diplomacy start+
	##If the player is ruler or co-ruler of an NPC kingdom, make sure the
	#policy matches fac_player_supporters_faction.  (It should be synchronized
	#elsewhere, but do it here in case there has been an error.)
	(assign, ":player_is_coruler_of_npc_faction", 0),
	  (try_begin),
		(neq, "$players_kingdom", "fac_player_supporters_faction"),
		(is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
		(call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", "$players_kingdom"),
		(ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),

		(assign, ":player_is_coruler_of_npc_faction", 1),

		(faction_get_slot, reg0, "$players_kingdom", dplmc_slot_faction_serfdom),
		(faction_set_slot, "fac_player_supporters_faction", dplmc_slot_faction_serfdom,  reg0),

		(faction_get_slot, reg0, "$players_kingdom", dplmc_slot_faction_centralization),
		(faction_set_slot, "fac_player_supporters_faction", dplmc_slot_faction_centralization,  reg0),

		(faction_get_slot, reg0, "$players_kingdom", dplmc_slot_faction_quality),
		(faction_set_slot, "fac_player_supporters_faction", dplmc_slot_faction_quality,  reg0),

		(faction_get_slot, reg0, "$players_kingdom", dplmc_slot_faction_aristocracy),
		(faction_set_slot, "fac_player_supporters_faction", dplmc_slot_faction_aristocracy,  reg0),

		(faction_get_slot, reg0, "$players_kingdom", dplmc_slot_faction_mercantilism),
		(faction_set_slot, "fac_player_supporters_faction", dplmc_slot_faction_mercantilism,  reg0),
	(try_end),
	##nested diplomacy end+
  (try_for_range, ":kingdom", kingdoms_begin, kingdoms_end),
    (faction_slot_eq, ":kingdom", slot_faction_state, sfs_active),

    (faction_get_slot, ":centralization", ":kingdom", dplmc_slot_faction_centralization),
    (faction_get_slot, ":aristocracy", ":kingdom", dplmc_slot_faction_aristocracy),
    (faction_get_slot, ":quality", ":kingdom", dplmc_slot_faction_quality),
    (faction_get_slot, ":serfdom", ":kingdom", dplmc_slot_faction_serfdom),
	 ##nested diplomacy start+
    (faction_get_slot, ":mercantilism", ":kingdom", dplmc_slot_faction_mercantilism),
	 ##nested diplomacy end+

    (try_begin),
      (eq, "$cheat_mode", 1),
      (str_store_faction_name, s9, ":kingdom"),
      (assign, reg1, ":centralization"),
      (display_message, "@{!}DEBUG - centralization {reg1}"),
      (assign, reg1, ":aristocracy"),
      (display_message, "@{!}DEBUG - aristocracy {reg1}"),
      (assign, reg1, ":quality"),
      (display_message, "@{!}DEBUG - quality {reg1}"),
      (assign, reg1, ":serfdom"),
      (display_message, "@{!}DEBUG - serfdom {reg1}"),
		##nested diplomacy start+
      (assign, reg1, ":mercantilism"),
      (display_message, "@{!}DEBUG - mercantilism {reg1}"),
		##nested diplomacy end+
    (try_end),

    (try_begin),
      (is_between, ":kingdom", npc_kingdoms_begin, npc_kingdoms_end),
      ##nested diplomacy start+
      ##Ensure the player isn't the kingdom's ruler or co-ruler
      (this_or_next|neq, ":kingdom", "$players_kingdom"),
		(eq, ":player_is_coruler_of_npc_faction", 0),
	  ##Add the chance to move around mercantilism.
      #(store_random_in_range, ":random", 0, 8),
	  (store_random_in_range, ":random", 0, 10),
      ##nested diplomacy end+

      (try_begin),
		  ##nested diplomacy start+
        #(is_between, ":random", 1, 5),
		  (is_between, ":random", 1, 6),
		  ##nested diplomacy end+
        (store_random_in_range, ":change", -1, 2),

        (try_begin),
          (eq, "$cheat_mode", 1),
          (str_store_faction_name, s12, ":kingdom"),
          (assign, reg1, ":change"),
          (assign, reg2, ":random"),
          (display_message, "@{!}DEBUG - changing {reg1} of {reg2} for {s12}"),
        (try_end),

        (try_begin),
          (eq, ":random", 1),
          (val_add, ":centralization", ":change"),
          (val_max, ":centralization", -3),
          (val_min, ":centralization", 3),
          (faction_set_slot, ":kingdom", dplmc_slot_faction_centralization, ":centralization"),
        (else_try),
          (eq, ":random", 2),
          (val_add, ":aristocracy", ":change"),
          (val_max, ":aristocracy", -3),
          (val_min, ":aristocracy", 3),
          (faction_set_slot, ":kingdom", dplmc_slot_faction_aristocracy, ":aristocracy"),
        (else_try),
          (eq, ":random", 3),
          (val_add, ":quality", ":change"),
          (val_max, ":quality", -3),
          (val_min, ":quality", 3),
          (faction_set_slot, ":kingdom", dplmc_slot_faction_quality, ":quality"),
        (else_try),
          (eq, ":random", 4),
          (val_add, ":serfdom", ":change"),
          (val_max, ":serfdom", -3),
          (val_min, ":serfdom", 3),
          (faction_set_slot, ":kingdom", dplmc_slot_faction_serfdom, ":serfdom"),
		  ##nested diplomacy start+
          (eq, ":random", 5),
          (val_add, ":mercantilism", ":change"),
			 (val_clamp, ":mercantilism", -3, 4),#-3 min, +3 max
          (faction_set_slot, ":kingdom", dplmc_slot_faction_mercantilism, ":mercantilism"),
		  ##nested diplomacy end+
        (try_end),
      (try_end),

    (else_try),

      #only player faction is affected by relation hits
      ##nested diplomacy start+
      ##Don't alter the values of centralization and aristocracy, since that's confusing.
      #(store_mul, ":centralization", ":centralization", -1),
      #(store_mul, ":aristocracy", ":aristocracy", 1),
      #(store_add, ":relation_change", ":centralization", ":aristocracy"),

		(store_sub, ":relation_change", ":aristocracy", ":centralization"),
      ##custodian (merchant) lords like plutocracy, unlike ordinary lords
      (store_mul, ":custodian_change", ":aristocracy", -1),
		(val_sub, ":custodian_change", ":centralization"),
      #benefactor lords like freedom and dislike serfdom
		(store_mul, ":benefactor_change", ":serfdom", -1),
		(val_sub, ":custodian_change", ":centralization"),
      ##nested diplomacy end+
      (try_begin),
        ##nested diplomacy start+
        (this_or_next|neq, ":benefactor_change", 0),
        (this_or_next|neq, ":custodian_change", 0),
        ##nested diplomacy end+
        (neq, ":relation_change", 0),

        (try_begin),
          (eq, "$cheat_mode", 1),
          (str_store_faction_name, s9, ":kingdom"),
          (assign, reg1, ":relation_change"),
          (display_message, "@{!}DEBUG - relation_change =  {reg1} for {s9}"),
        (try_end),

        ##diplomacy start+ also include kingdom ladies who are kingdom heroes
        #(try_for_range, ":troop_no", active_npcs_begin, active_npcs_end),
        (try_for_range, ":troop_no", heroes_begin, heroes_end),
        ##diplomacy end+
          (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
          (store_troop_faction, ":faction_no", ":troop_no"),
          (eq, ":kingdom", ":faction_no"),
          (faction_get_slot, ":faction_leader", ":kingdom", slot_faction_leader),
          ##diplomacy start+
          (neq, ":troop_no", ":faction_leader"),
          (assign, ":change_for_troop", ":relation_change"),
          (try_begin),
             (troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_custodian),
             (assign, ":change_for_troop", ":custodian_change"),
          (else_try),
             (troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_benefactor),
             (assign, ":change_for_troop", ":benefactor_change"),
          (try_end),
          ##Extra penalty for going back on a promise, extra bonus for keeping it
          (assign, ":promise_mod", 0),
          (try_begin),
             ##Following are only relevant for companions
             (is_between, ":troop_no", companions_begin, companions_end),
             (troop_slot_eq, ":troop_no", slot_troop_kingsupport_state, 1),
             (try_begin),
                #Argument: Lords
                (troop_slot_eq, ":troop_no", slot_troop_kingsupport_argument, argument_lords),
                (try_begin),
                  #If more than slightly centralized, or more than slightly balanced against aristocrats
                  (this_or_next|neg|faction_slot_ge, ":faction_no", dplmc_slot_faction_aristocracy, -1),
                     (faction_slot_ge, ":faction_no", dplmc_slot_faction_centralization, 2),
                  (val_sub, ":promise_mod", 1),
                (else_try),
                  #If more than slightly decentralized or more than slightly balanced in favor of aristocrats
                  (this_or_next|faction_slot_ge, ":faction_no", dplmc_slot_faction_aristocracy, 2),
                  (neg|faction_slot_ge, ":faction_no", dplmc_slot_faction_centralization, -2),
                  (faction_slot_ge, ":faction_no", dplmc_slot_faction_aristocracy, -1),#redundant
                  (val_add, ":promise_mod", 1),
                (try_end),
             (else_try),
                  #Argument: Commons
                  (troop_slot_eq, ":troop_no", slot_troop_kingsupport_argument, argument_commons),
                  (try_begin),
                    (faction_slot_ge, ":faction_no", dplmc_slot_faction_serfdom, 2),
                    (val_sub, ":promise_mod", 1),
                  (else_try),
                    (neg|faction_slot_ge, ":faction_no", dplmc_slot_faction_serfdom, 0),
                    (store_add, ":local_temp", ":serfdom", ":aristocracy"),
                    (lt, ":local_temp", 0),
                    (val_add, ":promise_mod", 1),
                  (try_end),
             (try_end),
         (try_end),
         #Check other broken promises
         (try_begin),
             (troop_slot_eq, ":troop_no", slot_lord_recruitment_argument, argument_lords),
             (this_or_next|neg|faction_slot_ge, ":faction_no", dplmc_slot_faction_aristocracy, -1),
                (faction_slot_ge, ":faction_no", dplmc_slot_faction_centralization, 2),
             #Lord must actually have cared about argument
             (neg|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_debauched),
             (neg|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_upstanding),
             (val_sub, ":promise_mod", 1),
         (else_try),
             (troop_slot_eq, ":troop_no", slot_lord_recruitment_argument, argument_commons),
             (faction_slot_ge, ":faction_no", dplmc_slot_faction_serfdom, 2),
             #Lord must actually have cared about argument
             (neg|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_quarrelsome),
             (neg|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_selfrighteous),
             (neg|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_debauched),
             (val_sub, ":promise_mod", 1),
         (try_end),
         (val_clamp, ":promise_mod", -1, 2),#-1, 0, or 1
         (val_add, ":change_for_troop", ":promise_mod"),

		 (neq, ":change_for_troop", 0),
		 (call_script, "script_change_player_relation_with_troop", ":troop_no", ":change_for_troop"),
        ##diplomacy end+
        (try_end),
      (try_end),
    (try_end),
  (try_end),
  ]),
  # affilated family ai
   (24 * 7,
   [
	##nested diplomacy start+ (piggyback on this trigger) allow lords to return from exile
	(assign, ":save_reg0", reg0),
	(assign, ":save_reg1", reg1),
	(assign, ":save_reg4", reg4),
	(try_begin),
		#only proceed if setting is enabled
		(ge, "$g_dplmc_lord_recycling", DPLMC_LORD_RECYCLING_ENABLE),
		#Kings/pretenders do not return in this manner (it should be different if it does happen).
		#Companions have a separate mechanism for return.
		(assign, ":chosen_lord", -1),
		(assign, ":best_score", -101),
		(assign, ":num_exiles", 0),
		#iterate over lords from a random start point, wrapping back to zero
		(store_random_in_range, ":rand_no", lords_begin, lords_end),
		(try_for_range, ":index", lords_begin, lords_end),
		  (store_add, ":troop_no", ":rand_no", ":index"),
		  (try_begin),
			 #wrap back around when you go off the end
			  (ge, ":troop_no", lords_end),
			(val_sub, ":troop_no", lords_end),
			(val_add, ":troop_no", lords_begin),
		  (try_end),
		  #Elsewhere we do the bookkeeping of ensuring that when a lord gets exiled
		  #his occupation changes to dplmc_slto_exile, and when loading a Native
		  #saved gamed with diplomacy we make this change for any lords required.
		  (troop_slot_eq, ":troop_no", slot_troop_occupation, dplmc_slto_exile),

		  (store_troop_faction, ":faction_no", ":troop_no"),
		  (this_or_next|eq, ":faction_no", -1),
		  (this_or_next|eq, ":faction_no", "fac_commoners"),
			 (eq, ":faction_no", "fac_outlaws"),
		  (val_add, ":num_exiles", 1),
		  (try_begin),
		     #Pick the lord with the best relation with his original liege.
			  #In most cases this will be the lord that has been in exile
			  #the longest.
			  (troop_get_slot, ":new_faction", ":troop_no", slot_troop_original_faction),
			  (is_between, ":new_faction", kingdoms_begin, kingdoms_end),
			  (faction_get_slot, ":faction_leader", ":new_faction", slot_faction_leader),
			  (gt, ":faction_leader", 0),
			  (call_script, "script_troop_get_relation_with_troop", ":troop_no", ":faction_leader"),
			  (this_or_next|eq, ":chosen_lord", -1),
			     (gt, reg0, ":best_score"),
			  (assign, ":chosen_lord", ":troop_no"),
			  (assign, ":best_score", reg0),
		  (else_try),
		     (eq, ":chosen_lord", -1),
			 (assign, ":chosen_lord", ":troop_no"),
		  (try_end),
      (try_end),
		#search is done
		(try_begin),
		 #no lord found
		 (eq, ":chosen_lord", -1),
		 (try_begin),
			(ge, "$cheat_mode", 1),
			(display_message, "@{!}DEBUG - no eligible lords in exile"),
		 (try_end),
	    (else_try),
			#If there were fewer than 3 lords in exile, random chance that none will return.
			(lt, ":num_exiles", 3),
			(store_random_in_range, ":random", 0, 256),
			(ge, ":random", 128),
			(try_begin),
				(ge, "$cheat_mode", 1),
				(assign, reg0, ":num_exiles"),
				(display_message, "@{!}DEBUG - {reg0} lords found in exile; randomly decided not to try to return anyone."),
			(try_end),
		(else_try),
		 #found a lord
		 (neq, ":chosen_lord", -1),
		 (try_begin),
			(ge, "$cheat_mode", 1),
			(str_store_troop_name, s4, ":chosen_lord"),
			(assign, reg0, ":best_score"),
			(assign, reg1, ":num_exiles"),
			(display_message, "@{!}DEBUG - {reg1} lords found in exile; {s4} chosen to return, score was {reg0}"),
		 (try_end),
		 #To decrease the displeasing fragmentation of lord cultures, bias towards assigning
		 #the lord back to his original faction if possible.
		 (troop_get_slot, ":new_faction", ":chosen_lord", slot_troop_original_faction),
		 (try_begin),
			 #If the original faction is not active, or the lord's relation is too low, use a different faction
			 (this_or_next|lt, ":best_score", -50),
			 (this_or_next|neg|is_between, ":new_faction", kingdoms_begin, kingdoms_end),
			    (neg|faction_slot_eq, ":new_faction", slot_faction_state, sfs_active),
		    (call_script, "script_lord_find_alternative_faction", ":chosen_lord"),
			(assign, ":new_faction", reg0),
		 (try_end),
		 (try_begin),
		   (neg|is_between, ":new_faction", kingdoms_begin, kingdoms_end),
			(ge, "$cheat_mode", 1),
			(str_store_troop_name, s4, ":chosen_lord"),
			(display_message, "@{!}DEBUG - {s4} found no faction to return to!"),
		 (try_end),
		 (is_between, ":new_faction", kingdoms_begin, kingdoms_end),
		 (assign, ":num_inactive", 0),
		 (try_begin),
			(eq, ":new_faction", "$players_kingdom"),
			(call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", "$players_kingdom"),
			(ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
			(assign, ":num_inactive", 0),
			(try_for_range, ":other_lord", lords_begin, lords_end),
			   (store_troop_faction, ":other_lord_faction", ":other_lord"),
			   (this_or_next|eq, ":other_lord_faction", "fac_player_supporters_faction"),
				(eq, ":other_lord_faction", "$players_kingdom"),
			   (troop_slot_eq, ":other_lord", slot_troop_occupation, slto_inactive),
			   (val_add, ":num_inactive", 1),
			(try_end),
			(gt, ":num_inactive", 1),
			(try_begin),
				(ge, "$cheat_mode", 1),
				(assign, reg0, ":num_inactive"),
				(display_message, "@{!}DEBUG - Not returning a lord to the player's kingdom, since there are already {reg0} lords waiting for their petitions to be heard."),
			(try_end),
		 (else_try),
			(call_script, "script_dplmc_lord_return_from_exile", ":chosen_lord", ":new_faction"),
		 (try_end),
		(try_end),
	(try_end),
	##More piggybacking
	##
	(assign, reg0, ":save_reg0"),
	(assign, reg1, ":save_reg1"),
	(assign, reg4, ":save_reg4"),
	##nested diplomacy end+
    (is_between, "$g_player_affiliated_troop", lords_begin, kingdom_ladies_end),
	##nested diplomacy start+
	(assign, ":best_relation", -101),
	(assign, ":worst_relation", 101),

	(assign, ":num_at_least_20", 0),
	(assign, ":num_below_0", 0),

	(assign, ":good_relation", 0),
	##nested diplomacy end+

    (assign, ":bad_relation", 0),
    (try_for_range, ":family_member", lords_begin, kingdom_ladies_end),
      (call_script, "script_dplmc_is_affiliated_family_member", ":family_member"),
      (gt, reg0, 0),
      (call_script, "script_troop_get_player_relation", ":family_member"),
	  ##nested diplomacy start+
	  #(le, reg0, -20),
	  #(assign, ":bad_relation", ":family_member"),
  	  (try_begin),
		(lt, reg0, 0),
		(val_add, ":num_below_0", 1),
		(le, reg0, ":worst_relation"),
		(assign, ":bad_relation", ":family_member"),
	  (else_try),
		(ge, reg0, 20),
		(val_add, ":num_at_least_20", 1),
		(gt, reg0, ":best_relation"),
		(assign, ":good_relation", ":family_member"),
	  (try_end),

	  (val_max, ":best_relation", reg0),
	  (val_min, ":worst_relation", reg0),
	  ##nested diplomacy end+
    (try_end),
	##nested diplomacy start+
	(try_begin),
		(gt, ":worst_relation", -15),
		(assign, ":bad_relation", 0),#suppress with no message
	(else_try),
		(gt, ":worst_relation", -20),
		(str_store_troop_name, s0, ":bad_relation"),
		(display_message, "@{s0} is grumbling against you.  Your affiliation could be jeopardized if this continues."),
		(str_clear, s0),
	(else_try),
		(neq, ":bad_relation", 0),
		(ge, ":num_at_least_20", ":num_below_0"),
		(store_add, reg0, ":worst_relation", ":best_relation"),
		(ge, reg0, 0),
		(str_store_troop_name, s0, ":bad_relation"),
		(str_store_troop_name, s1, ":good_relation"),
		(display_message, "@{s0} is grumbling against you, but with {s1}'s support you remain affiliated for now."),
		(str_clear, s0),
		(str_clear, s1),
		(assign, ":bad_relation", 0),
	(try_end),
	##nested diplomacy end+
    (try_begin),
      (eq, ":bad_relation", 0),

      (try_for_range, ":family_member", lords_begin, kingdom_ladies_end),
        (call_script, "script_dplmc_is_affiliated_family_member", ":family_member"),
        (gt, reg0, 0),
        (try_begin),
           (troop_slot_ge, ":family_member", slot_troop_prisoner_of_party, 0),
           ##diplomacy start+ skip relationship decay for imprisonment when the player himself is imprisoned or wounded
           (neg|troop_slot_ge, "trp_player", slot_troop_prisoner_of_party, 1),
           (neg|troop_is_wounded, "trp_player"),
           ##diplomacy end+
           (call_script, "script_change_player_relation_with_troop", ":family_member", -1),
        (else_try),
          (call_script, "script_change_player_relation_with_troop", ":family_member", 1),
        (try_end),
      (try_end),
    (else_try),
      (call_script, "script_add_notification_menu", "mnu_dplmc_affiliate_end", ":bad_relation", 0),
      (call_script, "script_dplmc_affiliate_end", 1),
    (try_end),
    ##nested diplomacy start+
 	 (assign, reg0, ":save_reg0"),
	 (assign, reg1, ":save_reg1"),
	 (assign, reg4, ":save_reg4"),
    ##nested diplomacy end+
    ]),
   (2,
   [
    (assign, ":has_walled_center", 0),
    (assign, ":has_fief", 0),
    (try_for_range, ":center_no", centers_begin, centers_end),
      (party_get_slot,  ":lord_troop_id", ":center_no", slot_town_lord),
      (eq, ":lord_troop_id", "trp_player"),
      (try_begin),
        (is_between, ":center_no", walled_centers_begin, walled_centers_end),
        (assign, ":has_walled_center", 1),
      (try_end),
      (assign, ":has_fief", 1),
    (try_end),

    (try_begin),
      (eq, ":has_walled_center", 0),
      (this_or_next|neq, "$g_player_constable", 0),
      (neq, "$g_player_chancellor", 0),
      (assign, "$g_player_constable", 0),
      (assign, "$g_player_chancellor", 0),
    (try_end),

    (try_begin),
      (eq, ":has_fief", 0),
      (neq, "$g_player_chamberlain", 0),
      (assign, "$g_player_chamberlain", 0),

      ##nested diplomacy start+
      #Adjust gold loss by difficulty
      (assign, ":save_reg0", reg0),
      (assign, ":save_reg1", reg1),

      (assign, ":loss_numerator", 2),
      (assign, ":loss_denominator", 3),

      (game_get_reduce_campaign_ai, ":reduce_campaign_ai"),
      (try_begin),
         (eq, ":reduce_campaign_ai", 0), #hard, lose 5/6
	 (assign, ":loss_numerator", 5),
	 (assign, ":loss_denominator", 6),
      (else_try),
         (eq, ":reduce_campaign_ai", 1), #medium, lose 2/3
	 (assign, ":loss_numerator", 2),
	 (assign, ":loss_denominator", 3),
      (else_try),
         (eq, ":reduce_campaign_ai", 2), #easy, lose 1/2
	 (assign, ":loss_numerator", 1),
	 (assign, ":loss_denominator", 2),
      (try_end),

      (store_troop_gold, ":cur_gold", "trp_household_possessions"),
      (try_begin),
        (gt, ":cur_gold", 0),
        #(call_script, "script_dplmc_withdraw_from_treasury", ":cur_gold"),
        #(val_div, ":cur_gold", 3),
        #(call_script, "script_troop_add_gold", "trp_player", ":cur_gold"),
        #(display_message, "@Your last fief was captured and you lost 2/3 of your treasury"),
	(store_mul, ":lost_gold", ":cur_gold", ":loss_numerator"),
	(val_div, ":lost_gold", ":loss_denominator"),
	(val_mul, ":lost_gold", -1),
	(call_script, "script_dplmc_withdraw_from_treasury", ":lost_gold"),
	(assign, reg0, ":loss_numerator"),
	(assign, reg1, ":loss_denominator"),
	(display_message, "@Your last fief was captured and you lost {reg0}/{reg1} of your treasury"),
      (try_end),

      (assign, reg0, ":save_reg0"),
      (assign, reg1, ":save_reg1"),
      ##nested diplomacy end+
    (try_end),
    ]),
   (24,
   [
      (try_for_range, ":faction1", npc_kingdoms_begin, npc_kingdoms_end),
        (assign, ":attitude_change", 2), #positive means good attitude
        (try_for_range, ":faction2", kingdoms_begin, kingdoms_end),
          (neq, ":faction1", ":faction2"),
		  ##diplomacy start+
		  #FIX: Stop the attitude change from carrying over from the previous kingdom!
		  (assign, ":attitude_change", 2),
		  #Handling for fac_player_supporters_faction & players_kingdom
		  (assign, ":alt_faction", ":faction2"),
		  (try_begin),
		     (eq, ":faction2", "fac_player_supporters_faction"),
			 (neq, ":faction1", "$players_kingdom"),
			 (assign, ":alt_faction", "$players_kingdom"),
		  (else_try),
		     (eq, ":faction2", "$players_kingdom"),
			 (assign, ":alt_faction", "fac_player_supporters_faction"),
		  (try_end),
		  ##Make loop less wasteful.
		  ##OLD:
          #(try_for_parties, ":party"),
          #  (is_between, ":party", centers_begin, centers_end),
		  ##NEW:
		  (try_for_range, ":party", centers_begin, centers_end),
		  ##diplomacy end+
            (store_faction_of_party, ":party_faction", ":party"),
			##diplomacy start+
			##FIX broken slot check!
			##ADD support for player's faction
			##OLD:
            #(eq, ":party_faction", ":faction2"),
            #(party_slot_eq, ":faction1", ":party", slot_center_original_faction),
			##NEW:
			(this_or_next|eq, ":party_faction", ":faction2"),
				(eq, ":party_faction", ":alt_faction"),
			(party_slot_eq, ":party", slot_center_original_faction, ":faction1"),
			#Don't subtract relation when it would be nonsensical
			(this_or_next|neq, ":faction1", "$players_kingdom"),
			(this_or_next|neq, ":faction2", "fac_player_supporters_faction"),
				(party_slot_ge, ":party", dplmc_slot_center_original_lord, 1),
			##diplomacy end+
            (val_sub, ":attitude_change", 1), #less attitude
          (try_end),

          (try_for_range, ":faction3", kingdoms_begin, kingdoms_end),
            (call_script, "script_diplomacy_faction_get_diplomatic_status_with_faction", ":faction2", ":faction3"),
            (eq, reg0, -2), #war between 2 and 3
            (call_script, "script_diplomacy_faction_get_diplomatic_status_with_faction", ":faction1", ":faction3"),
            (eq, reg0, -2), #war between 1 and 3
            (val_add, ":attitude_change", 1), #higher attitude
          (try_end),
        (try_end),

        (store_add, ":faction1_to_faction2_slot", ":faction2", dplmc_slot_faction_attitude_begin),
        (party_set_slot, ":faction1", ":faction1_to_faction2_slot", ":attitude_change"),
      (try_end),
    ]),
]
