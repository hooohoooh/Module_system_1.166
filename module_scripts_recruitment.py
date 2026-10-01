# -*- coding: utf-8 -*-
# module_scripts_recruitment.py -- auto split from module_scripts.py (feature: 招募（村庄/城镇/同伴）)
# entries: 9 (order preserved within this file)
from header_presentations import *
from header_common import *
from header_operations import *
from module_constants import *
from module_constants import *
from header_parties import *
from header_skills import *
from header_mission_templates import *
from header_items import *
from header_triggers import *
from header_terrain_types import *
from header_music import *
from header_map_icons import *
from ID_animations import *
from ym_gatling import *
from ym_gatling_shop import *
from zhenyinghebing import *
from lco_scripts import lco_scripts
from upgrade_scripts import upgrade_scripts
##diplomacy start+
from module_factions import dplmc_factions_begin, dplmc_factions_end, dplmc_non_generic_factions_begin
##diplomacy end+
from header_presentations import tf_left_align
  #### Autoloot improved by rubik begin
from module_items import *


scripts_recruitment = [

  # script_recruit_troop_as_companion
  # Input: arg1 = troop_no,
  # Output: none
  ("recruit_troop_as_companion",
    [
      (store_script_param_1, ":troop_no"),
      ##diplomacy start+
      ##Save civilian clothing of companions (and ladies, etc.)
      (try_begin),
         (troop_is_hero, ":troop_no"),
         (neg|troop_slot_ge, ":troop_no", slot_troop_playerparty_history, 1),#only call this the first time they join
         (call_script, "script_dplmc_save_civilian_clothing", ":troop_no"),#although, redundant calls should be save
      (try_end),
      ##Preserve former occupations enfeoffed companions
      (try_begin),
          (troop_is_hero, ":troop_no"),
          (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
          (neg|troop_slot_eq, ":troop_no", slot_troop_playerparty_history, dplmc_pp_history_nonplayer_entry),
          (troop_set_slot, ":troop_no", slot_troop_playerparty_history, dplmc_pp_history_lord_rejoined),
      (try_end),
      ##diplomacy end+
      (troop_set_slot, ":troop_no", slot_troop_occupation, slto_player_companion),
      (troop_set_slot, ":troop_no", slot_troop_cur_center, -1),
      (troop_set_auto_equip, ":troop_no", 0),
      (party_add_members, "p_main_party", ":troop_no", 1),
      (str_store_troop_name, s6, ":troop_no"),
      (display_message, "@{s6} has joined your party."),
	  (troop_set_note_available, ":troop_no", 1),	
	  
	  (try_begin),  
	    #gekokujo 3.0 microfactions! include fort companions start
	    #(is_between, ":troop_no", companions_begin, companions_end),
		(is_between, ":troop_no", companions_begin, fort_companions_end),
		#gekokujo 3.0 microfactions! include fort companions end
	    (store_sub, ":companion_number", ":troop_no", companions_begin),
	    	    
	    (set_achievement_stat, ACHIEVEMENT_KNIGHTS_OF_THE_ROUND, ":companion_number", 1),
	    
	    (assign, ":number_of_companions_hired", 0),
	    (try_for_range, ":cur_companion", 0, 16),	      
	      (get_achievement_stat, ":is_hired", ACHIEVEMENT_KNIGHTS_OF_THE_ROUND, ":cur_companion"),
	      (eq, ":is_hired", 1),
	      (val_add, ":number_of_companions_hired", 1),
	    (try_end),
	    
	    (try_begin),
	      (ge, ":number_of_companions_hired", 6),
	      (unlock_achievement, ACHIEVEMENT_KNIGHTS_OF_THE_ROUND),
	    (try_end),
	  (try_end),
  ]),
  #script_update_mercenary_units_of_towns
  # INPUT: none
  # OUTPUT: none
  ("update_mercenary_units_of_towns",
    [(try_for_range, ":town_no", towns_begin, towns_end),
      (store_random_in_range, ":troop_no", mercenary_troops_begin, mercenary_troops_end),
      (party_set_slot, ":town_no", slot_center_mercenary_troop_type, ":troop_no"),
      (store_random_in_range, ":amount", 3, 8),
	  ##diplomacy start+
	  #OPTIONAL CHANGE: The same way that lord party sizes increase as the player
	  #progresses, also increase mercenary party sizes to maintain their relevance.
	  (try_begin),
	     (ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_HIGH),
		 (store_character_level, ":level", "trp_player"), #increase limits a little bit as the game progresses.
		 (store_add, ":level_factor", 80, ":level"),
         (val_mul, ":amount", ":level_factor"),
         (val_div, ":amount", 80),
	  (try_end),
	  ##diplomacy end+
      (party_set_slot, ":town_no", slot_center_mercenary_troop_amount, ":amount"),
    (try_end),
     ]),
  #script_update_volunteer_troops_in_village
  # INPUT: arg1 = center_no
  # OUTPUT: none
  ("update_volunteer_troops_in_village",
    [
       (store_script_param, ":center_no", 1),
       (party_get_slot, ":player_relation", ":center_no", slot_center_player_relation),
       (party_get_slot, ":center_culture", ":center_no", slot_center_culture),
	   
	   
##	   (try_begin),
##		(eq, "$cheat_mode", 2),
##	    (str_store_party_name, s4, ":center_no"),
##	    (str_store_faction_name, s5, ":center_culture"),
##	    (display_message, "str_updating_volunteers_for_s4_faction_is_s5"),
##	   (try_end),
	   
	   #gekokujo town/castle/village recruitment differences start
       #(faction_get_slot, ":volunteer_troop", ":center_culture", slot_faction_tier_1_troop),
       (try_begin),
	     #gekokujo 3.0 ikko ikko recruitment start
	     #for toyama castle (p_castle_14) ikko ikki recruit samurai instead
	     (eq, ":center_no", "p_castle_14"),
	     (assign, ":volunteer_troop", "trp_ceshi15_messenger"),
       (else_try),
         (eq, ":center_no", "p_castle_27"),
	     (assign, ":volunteer_troop", "trp_ceshi15_messenger"),
       (else_try),
         (eq, ":center_no", "p_castle_82"),
	     (assign, ":volunteer_troop", "trp_ceshi15_messenger"),
       (else_try),
         (eq, ":center_no", "p_town_25"),
	     (assign, ":volunteer_troop", "trp_ceshi1_messenger"),
       (else_try),
         (eq, ":center_no", "p_castle_34"),
	     (assign, ":volunteer_troop", "trp_ceshi1_messenger"),
       (else_try),
         (eq, ":center_no", "p_castle_35"),
	     (assign, ":volunteer_troop", "trp_ceshi1_messenger"),
       (else_try),
         (eq, ":center_no", "p_castle_64"),
	     (assign, ":volunteer_troop", "trp_ceshi1_messenger"),
      (else_try),
         (eq, ":center_no", "p_town_9"),
	     (assign, ":volunteer_troop", "trp_ceshi13_messenger"),
      (else_try),
         (eq, ":center_no", "p_castle_61"),
	     (assign, ":volunteer_troop", "trp_ceshi13_messenger"),
      (else_try),
         (eq, ":center_no", "p_castle_45"),
	     (assign, ":volunteer_troop", "trp_ceshi13_messenger"),
      (else_try),
         (eq, ":center_no", "p_castle_11"),
	     (assign, ":volunteer_troop", "trp_ceshi13_messenger"),
      (else_try),
         (eq, ":center_no", "p_castle_72"),
	     (assign, ":volunteer_troop", "trp_ceshi13_messenger"),
      (else_try),
         (eq, ":center_no", "p_castle_73"),
	     (assign, ":volunteer_troop", "trp_ceshi13_messenger"),
      (else_try),
         (eq, ":center_no", "p_town_22"),
	     (assign, ":volunteer_troop", "trp_ceshi12_messenger"),
      (else_try),
         (eq, ":center_no", "p_castle_69"),
	     (assign, ":volunteer_troop", "trp_ceshi12_messenger"),
      (else_try),
         (eq, ":center_no", "p_castle_6"),
	     (assign, ":volunteer_troop", "trp_ceshi17_messenger"),
      (else_try),
         (eq, ":center_no", "p_castle_16"),
	     (assign, ":volunteer_troop", "trp_ceshi17_messenger"),
      (else_try),
         (eq, ":center_no", "p_castle_75"),
	     (assign, ":volunteer_troop", "trp_ceshi17_messenger"),
      (else_try),
         (eq, ":center_no", "p_town_33"),
	     (assign, ":volunteer_troop", "trp_ceshi17_messenger"),
      (else_try),
         (eq, ":center_no", "p_town_28"),
	     (assign, ":volunteer_troop", "trp_ceshi14_messenger"),    
      (else_try),
         (eq, ":center_no", "p_castle_5"),
	     (assign, ":volunteer_troop", "trp_ceshi14_messenger"), 
      (else_try),
         (eq, ":center_no", "p_castle_40"),
	     (assign, ":volunteer_troop", "trp_ceshi14_messenger"), 
	     #gekokujo 3.0 ikko ikko recruitment end
	   (else_try),
         (this_or_next|party_slot_eq, ":center_no", slot_party_type, spt_town),
         (party_slot_eq, ":center_no", slot_party_type, spt_castle),
         (faction_get_slot, ":volunteer_troop", ":center_culture", slot_faction_tier_1_troop),
       (else_try),
         (faction_get_slot, ":volunteer_troop", ":center_culture", slot_faction_tier_0_troop),
       (try_end),
	   #gekokujo town/castle/village recruitment differences end
	   
       (assign, ":volunteer_troop_tier", 1),
       (store_div, ":tier_upgrades", ":player_relation", 10),
       (try_for_range, ":unused", 0, ":tier_upgrades"),
         (store_random_in_range, ":random_no", 0, 100),
         (lt, ":random_no", 10),
         (store_random_in_range, ":random_no", 0, 2),
         (troop_get_upgrade_troop, ":upgrade_troop_no", ":volunteer_troop", ":random_no"),
         (try_begin),
           (le, ":upgrade_troop_no", 0),
           (troop_get_upgrade_troop, ":upgrade_troop_no", ":volunteer_troop", 0),
         (try_end),
         (gt, ":upgrade_troop_no", 0),
         (val_add, ":volunteer_troop_tier", 1),
         (assign, ":volunteer_troop", ":upgrade_troop_no"),
       (try_end),
       
       (assign, ":upper_limit", 8),
       (try_begin),
         (ge, ":player_relation", 4),
         (assign, ":upper_limit", ":player_relation"),
         (val_div, ":upper_limit", 2),
         (val_add, ":upper_limit", 6),
       (else_try),
         (lt, ":player_relation", 0),
         (assign, ":upper_limit", 0),
       (try_end),
       
##diplomacy begin
      (assign, ":percent", 100),
      (try_begin), #-30% if not owner
        (neg|party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
        (val_sub, ":percent", 30),
      (try_end),
      (try_begin), #1%/4 renown
        (troop_get_slot, ":player_renown", "trp_player", slot_troop_renown),
        (val_div, ":player_renown", 4),
        (val_add, ":percent", ":player_renown"),
      (try_end),
      (try_begin), #1%/3 honour
        (assign, ":player_honour", "$player_honor"),
        (val_div, ":player_honour", 3),
        (val_add, ":percent", ":player_honour"),
      (try_end),
      (try_begin), #+5% if king
        (faction_get_slot, ":faction_leader", "fac_player_supporters_faction", slot_faction_leader),
        (eq, ":faction_leader", "trp_player"),
        (val_add, ":percent", 5),

        (try_begin), #-5% for each point of serfdom
          (faction_get_slot, ":serfdom", "fac_player_supporters_faction", dplmc_slot_faction_serfdom),
          (neq, ":serfdom", 0),
          (val_mul, ":serfdom", 5),
          (val_sub, ":percent", ":serfdom"),
        (try_end),

        (try_begin),  #+5% if king of village
          (store_faction_of_party, ":faction", ":center_no"),
          (eq, ":faction", "fac_player_supporters_faction"),
          (val_add, ":percent", 5),
        (try_end),
      (try_end),

      (try_begin),
        (gt, ":upper_limit", 0),
        (val_clamp, ":percent", 0, 201),
        (val_mul, ":upper_limit", ":percent"),
        (val_div, ":upper_limit", 100),
      (try_end),

##diplomacy end

       (val_mul, ":upper_limit", 3),   
       (store_add, ":amount_random_divider", 2, ":volunteer_troop_tier"),
       (val_div, ":upper_limit", ":amount_random_divider"),
       
       (store_random_in_range, ":amount", 0, ":upper_limit"),
       (party_set_slot, ":center_no", slot_center_volunteer_troop_type, ":volunteer_troop"),
       (party_set_slot, ":center_no", slot_center_volunteer_troop_amount, ":amount"),
     ]),
  #script_update_npc_volunteer_troops_in_village
  # INPUT: arg1 = center_no
  # OUTPUT: none
  ("update_npc_volunteer_troops_in_village",
    [
       (store_script_param, ":center_no", 1),
       (party_get_slot, ":center_culture", ":center_no", slot_center_culture),
	   
		 ##for ikko ikki castles, recruit samurai instead
		 #(try_begin),
		 #  (eq, ":center_culture", "fac_culture_20"),
		 #  (assign, ":volunteer_troop", "trp_gekokujo_ikko_jizamurai"),
		 #(try_end),
		 
	   #gekokujo town/castle/village recruitment differences start
       #(faction_get_slot, ":volunteer_troop", ":center_culture", slot_faction_tier_1_troop),
	   (try_begin),
	     #gekokujo 3.0 ikko ikko recruitment start
	     #for toyama castle (p_castle_14) ikko ikki recruit samurai instead
	     (eq, ":center_no", "p_castle_14"),
	     (assign, ":volunteer_troop", "trp_gekokujo_ikko_jizamurai"),
	     #gekokujo 3.0 ikko ikko recruitment end
	   (else_try),
         (this_or_next|party_slot_eq, ":center_no", slot_party_type, spt_town),
         (party_slot_eq, ":center_no", slot_party_type, spt_castle),
         (faction_get_slot, ":volunteer_troop", ":center_culture", slot_faction_tier_1_troop),
       (else_try),
         (faction_get_slot, ":volunteer_troop", ":center_culture", slot_faction_tier_0_troop),
       (try_end),
	   #gekokujo town/castle/village recruitment differences end
	   
       (assign, ":volunteer_troop_tier", 1),
       (try_for_range, ":unused", 0, 5),
         (store_random_in_range, ":random_no", 0, 100),
         (lt, ":random_no", 10),
         (store_random_in_range, ":random_no", 0, 2),
         (troop_get_upgrade_troop, ":upgrade_troop_no", ":volunteer_troop", ":random_no"),
         (try_begin),
           (le, ":upgrade_troop_no", 0),
           (troop_get_upgrade_troop, ":upgrade_troop_no", ":volunteer_troop", 0),
         (try_end),
         (gt, ":upgrade_troop_no", 0),
         (val_add, ":volunteer_troop_tier", 1),
         (assign, ":volunteer_troop", ":upgrade_troop_no"),
       (try_end),
       
       (assign, ":upper_limit", 12),
       
       (store_add, ":amount_random_divider", 2, ":volunteer_troop_tier"),
       (val_div, ":upper_limit", ":amount_random_divider"),
       
       (store_random_in_range, ":amount", 0, ":upper_limit"),
       (party_set_slot, ":center_no", slot_center_npc_volunteer_troop_type, ":volunteer_troop"),
       (party_set_slot, ":center_no", slot_center_npc_volunteer_troop_amount, ":amount"),
     ]),
  #script_update_companion_candidates_in_taverns
  # INPUT: none
  # OUTPUT: none
  ("update_companion_candidates_in_taverns",
    [
      (try_begin),
        (eq, "$cheat_mode", 1),
        (display_message, "str_shuffling_companion_locations"),
      (try_end),
      
      (try_for_range, ":troop_no", companions_begin, companions_end),
	    ##diplomacy start+ Move this *after* the checks!
        #  (troop_set_slot, ":troop_no", slot_troop_cur_center, -1),
		##diplomacy end+
        (troop_slot_eq, ":troop_no", slot_troop_days_on_mission, 0),
        (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_inactive),
        
        (neg|troop_slot_ge, ":troop_no", slot_troop_prisoner_of_party, 0),
		##diplomacy start+
		(troop_get_slot, ":town_no", ":troop_no", slot_troop_cur_center),
		(try_begin),
			(is_between, ":town_no", towns_begin, towns_end),
			(party_get_slot, ":town_lord", ":town_no", slot_town_lord),
			##zerilius changes begin
			##bug fix for red text
			(ge, ":town_lord", 0),
			##zerilius changes end
			(this_or_next|eq, ":town_lord", "trp_player"),
			(this_or_next|troop_slot_eq, "trp_player", slot_troop_spouse, ":town_lord"),
				(troop_slot_eq, ":town_lord", slot_troop_spouse, "trp_player"),
		(else_try),
			#Moved from above:
			(troop_set_slot, ":troop_no", slot_troop_cur_center, -1),
		(try_end),
		(neg|troop_slot_ge, ":troop_no", slot_troop_cur_center, 1),
		##diplomacy end+        
        (store_random_in_range, ":town_no", towns_begin, towns_end),
        (try_begin),
		  ##diplomacy start+ Remove the "you can't go home again" condition if the player owns the town
		  (assign, ":veto", 0),
		  (try_begin),
			(store_faction_of_party, ":town_faction", ":town_no"),
			(eq, ":town_faction", "fac_player_supporters_faction"),
		  (else_try),
			(party_get_slot, ":town_lord", ":town_no", slot_town_lord),
			(ge, ":town_lord", 0),
			(this_or_next|eq, ":town_lord", "trp_player"),
			(this_or_next|troop_slot_eq, "trp_player", slot_troop_spouse, ":town_lord"),
				(troop_slot_eq, ":town_lord", slot_troop_spouse, "trp_player"),
		  (else_try),
			#Native veto:
			(this_or_next|troop_slot_eq, ":troop_no", slot_troop_home, ":town_no"),
				(troop_slot_eq, ":troop_no", slot_troop_first_encountered, ":town_no"),
			(assign, ":veto", 1),
		  (try_end),
		  (eq, ":veto", 0),
                  ##diplomacy end+
          (troop_set_slot, ":troop_no", slot_troop_cur_center, ":town_no"),
          (try_begin),
            (eq, "$cheat_mode", 1),
            (str_store_troop_name, 4, ":troop_no"),
            (str_store_party_name, 5, ":town_no"),
            (display_message, "@{!}{s4} is in {s5}"),
          (try_end),
        (try_end),
      (try_end),
     ]),
  #script_cf_village_recruit_volunteers_cond
  # INPUT: none
  # OUTPUT: none
  ("cf_village_recruit_volunteers_cond",
    [
	
	 (try_begin),
		(eq, "$cheat_mode", 1),
		(display_message, "str_checking_volunteer_availability_script"),
	 (try_end),
	 
	 (neg|party_slot_eq, "$current_town", slot_village_state, svs_looted),
     (neg|party_slot_eq, "$current_town", slot_village_state, svs_being_raided),
     (neg|party_slot_ge, "$current_town", slot_village_infested_by_bandits, 1),
     (store_faction_of_party, ":village_faction", "$current_town"),
     (party_get_slot, ":center_relation", "$current_town", slot_center_player_relation),
     (store_relation, ":village_faction_relation", ":village_faction", "fac_player_faction"),
	 
     (ge, ":center_relation", 0),
	 (try_begin),
		(eq, "$cheat_mode", 1),
		(display_message, "str_center_relation_at_least_zero"),
	 (try_end),
	 
	 
	 
	 
     (this_or_next|ge, ":center_relation", 5),
     (this_or_next|eq, ":village_faction", "$players_kingdom"),
     (this_or_next|ge, ":village_faction_relation", 0),
     (this_or_next|eq, ":village_faction", "$supported_pretender_old_faction"),
		(eq, "$players_kingdom", 0),

	 (try_begin),
		(eq, "$cheat_mode", 1),
		(display_message, "str_relationfaction_conditions_met"),
	 (try_end),

		
     (party_slot_ge, "$current_town", slot_center_volunteer_troop_amount, 0),
     (party_slot_ge, "$current_town", slot_center_volunteer_troop_type, 1),
	 
	 (try_begin),
		(eq, "$cheat_mode", 1),
		(display_message, "str_troops_available"),
	 (try_end),
	 
	 
     (party_get_free_companions_capacity, ":free_capacity", "p_main_party"),
     (ge, ":free_capacity", 1),
	 
	 (try_begin),
		(eq, "$cheat_mode", 1),
		(display_message, "str_party_has_capacity"),
	 (try_end),
	 
	 
     ]),
  #Gekokujo town recruitment
  #script_cf_town_castle_recruit_volunteers_cond
  # INPUT: none
  # OUTPUT: none
  ("cf_town_castle_recruit_volunteers_cond",
    [(store_faction_of_party, ":town_faction", "$current_town"),
     (party_get_slot, ":center_relation", "$current_town", slot_center_player_relation),
     (store_relation, ":town_faction_relation", ":town_faction", "fac_player_faction"),
     (ge, ":center_relation", 0),
     (this_or_next|ge, ":center_relation", 5),
     (this_or_next|eq, ":town_faction", "$players_kingdom"),
     (this_or_next|ge, ":town_faction_relation", 0),
     (this_or_next|eq, ":town_faction", "$supported_pretender_old_faction"),
     (             eq, "$players_kingdom", 0),
     (party_slot_ge, "$current_town", slot_center_volunteer_troop_amount, 0),
     (party_slot_ge, "$current_town", slot_center_volunteer_troop_type, 1),
     (party_get_free_companions_capacity, ":free_capacity", "p_main_party"),
     (ge, ":free_capacity", 1),
     ]),
  #script_village_recruit_volunteers_recruit
  # INPUT: none
  # OUTPUT: none
  ("village_recruit_volunteers_recruit",
    [(party_get_slot, ":volunteer_troop", "$current_town", slot_center_volunteer_troop_type),
     (party_get_slot, ":volunteer_amount", "$current_town", slot_center_volunteer_troop_amount),
     (party_get_free_companions_capacity, ":free_capacity", "p_main_party"),
     (val_min, ":volunteer_amount", ":free_capacity"),
     (store_troop_gold, ":gold", "trp_player"),

#     (store_div, ":gold_capacity", ":gold", 10),#10 mon per man
     (try_begin),
       (this_or_next|party_slot_eq, "$current_town", slot_party_type, spt_castle),
       (party_slot_eq, "$current_town", slot_party_type, spt_town),
	   (store_div, ":gold_capacity", ":gold", 300),
     (else_try),
       (store_div, ":gold_capacity", ":gold", 10),
     (try_end),
	 
	 #gekokujo 3.0 ikko ikko recruitment start
	 #kanazawa, ishiyama, nagashima, and joguji all cost 10 because they have monk recruits
     (try_begin),
	   (this_or_next|eq, "$current_town", "p_town_8"),
	   (this_or_next|eq, "$current_town", "p_castle_72"),
	   (this_or_next|eq, "$current_town", "p_castle_74"),
	   (eq, "$current_town", "p_castle_75"),
	   (store_div, ":gold_capacity", ":gold", 10),
     (try_end),
	 #gekokujo 3.0 ikko ikko recruitment end

     (val_min, ":volunteer_amount", ":gold_capacity"),
     (party_add_members, "p_main_party", ":volunteer_troop", ":volunteer_amount"),
     (party_set_slot, "$current_town", slot_center_volunteer_troop_amount, -1),

#     (store_mul, ":cost", ":volunteer_amount", 10),#10 mon per man
     (try_begin),
       (this_or_next|party_slot_eq, "$current_town", slot_party_type, spt_castle),
       (party_slot_eq, "$current_town", slot_party_type, spt_town),
	   (try_begin),
		 (party_slot_eq, "$current_town", slot_center_culture, "fac_culture_20"),
	     (store_mul, ":cost", ":volunteer_amount", 10),
	   (else_try),
	     (store_mul, ":cost", ":volunteer_amount", 300),
	   (try_end),
     (else_try),
       (store_mul, ":cost", ":volunteer_amount", 10),
     (try_end),

     (troop_remove_gold, "trp_player", ":cost"),
     ]),
#gekokujo variable recruitment
  #script_village_recruit_volunteers_recruit
  # INPUT: arg1 = volunteer_troop_amount
  # OUTPUT: none
  ("gekokujo_recruit_volunteers_recruit",
    [(store_script_param, ":volunteer_amount", 1),
	 (party_get_slot, ":volunteer_troop", "$current_town", slot_center_volunteer_troop_type),
	 (party_get_slot, ":volunteer_current", "$current_town", slot_center_volunteer_troop_amount),
     (party_get_free_companions_capacity, ":free_capacity", "p_main_party"),
     (val_min, ":volunteer_amount", ":free_capacity"),
     (store_troop_gold, ":gold", "trp_player"),

#     (store_div, ":gold_capacity", ":gold", 10),#10 mon per man
     (try_begin),
       (this_or_next|party_slot_eq, "$current_town", slot_party_type, spt_castle),
       (party_slot_eq, "$current_town", slot_party_type, spt_town),
	   (store_div, ":gold_capacity", ":gold", 300),
     (else_try),
       (store_div, ":gold_capacity", ":gold", 10),
     (try_end),
	 
	 #gekokujo 3.0 ikko ikko recruitment start
	 #kanazawa, ishiyama, nagashima, and joguji all cost 10 because they have monk recruits
     (try_begin),
	   (this_or_next|eq, "$current_town", "p_town_8"),
	   (this_or_next|eq, "$current_town", "p_castle_72"),
	   (this_or_next|eq, "$current_town", "p_castle_74"),
	   (eq, "$current_town", "p_castle_75"),
	   (store_div, ":gold_capacity", ":gold", 10),
     (try_end),
	 #gekokujo 3.0 ikko ikko recruitment end

     (val_min, ":volunteer_amount", ":gold_capacity"),
     (party_add_members, "p_main_party", ":volunteer_troop", ":volunteer_amount"),
	 (val_sub, ":volunteer_current", ":volunteer_amount"),
	 (try_begin),
	   (gt, ":volunteer_current", 0),
	   (party_set_slot, "$current_town", slot_center_volunteer_troop_amount, ":volunteer_current"),
	 (else_try),
       (party_set_slot, "$current_town", slot_center_volunteer_troop_amount, -1),
	 (end_try),

#     (store_mul, ":cost", ":volunteer_amount", 10),#10 mon per man
     (try_begin),
       (this_or_next|party_slot_eq, "$current_town", slot_party_type, spt_castle),
       (party_slot_eq, "$current_town", slot_party_type, spt_town),
	   (try_begin),
	     #gekokujo 3.1 ikko samurai recruitment fix start
		 #see notes in mnu_recruit_volunteers
		 #(party_slot_eq, "$current_town", slot_center_culture, "fac_culture_20"),
	     (this_or_next|eq, "$current_town", "p_town_8"),
	     (this_or_next|eq, "$current_town", "p_castle_72"),
	     (this_or_next|eq, "$current_town", "p_castle_74"),
	     (eq, "$current_town", "p_castle_75"),
		 #gekokujo 3.1 ikko samurai recruitment fix end
		 (store_mul, ":cost", ":volunteer_amount", 10),
	   (else_try),
		 (store_mul, ":cost", ":volunteer_amount", 300),
	   (try_end),
     (else_try),
       (store_mul, ":cost", ":volunteer_amount", 10),
     (try_end),

     (troop_remove_gold, "trp_player", ":cost"),
     ]),
]
