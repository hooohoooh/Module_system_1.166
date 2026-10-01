# -*- coding: utf-8 -*-
# module_scripts_faction_politics.py -- auto split from module_scripts.py (feature: 领主/派系/政治/围城/婚姻)
# entries: 192 (order preserved within this file)
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


scripts_faction_politics = [

  #script_start_wedding_cutscene
  # INPUT: arg1 = groom_troop, arg2 = bride_troop
  # OUTPUT: none
  ("start_wedding_cutscene",
   [
     (store_script_param, "$g_wedding_groom_troop", 1),
     (store_script_param, "$g_wedding_bride_troop", 2),
     ##diplomacy start+
	 (assign, ":save_reg0", reg0),
	 (assign, ":save_reg1", reg1),


     #To prevent a ridiculous cutscene, reverse genders if the bride is male.
	 (call_script, "script_dplmc_store_is_female_troop_1_troop_2", "$g_wedding_groom_troop", "$g_wedding_bride_troop"),
	 (assign, ":groom_is_woman", reg0),
	 (assign, ":bride_is_woman", reg1),

     (try_begin),
       (eq, ":bride_is_woman", 0),
       (neq, ":groom_is_woman", 0),#Don't bother reversing if both are male
       (assign, reg0, "$g_wedding_bride_troop"),
       (assign, "$g_wedding_bride_troop", "$g_wedding_groom_troop"),
       (assign, "$g_wedding_groom_troop", reg0),
	 (else_try),
	   #If it's a same-sex wedding, put the player in the role of the groom.
	   (eq, ":bride_is_woman", ":groom_is_woman"),
	   (eq, "$g_wedding_bride_troop", "trp_player"),
	   (assign, "$g_wedding_bride_troop", "$g_wedding_groom_troop"),
	   (assign, "$g_wedding_groom_troop", "trp_player"),
     (try_end),
     #diplomacy end+
     (assign, "$g_wedding_bishop_troop", "trp_temporary_minister"),
     (try_begin),
       (is_between, "$players_kingdom", kingdoms_begin, kingdoms_end),
       (neg|faction_slot_eq, "$players_kingdom", slot_faction_leader, "$g_wedding_groom_troop"),
       (neg|faction_slot_eq, "$players_kingdom", slot_faction_leader, "$g_wedding_bride_troop"),
       (faction_get_slot, ":players_king", "$players_kingdom", slot_faction_leader),
	   ##diplomacy start+
	   (neq, ":players_king", "$g_wedding_bride_troop"),#necessary now that marrying monarchs can occur
	   (neq, ":players_king", "$g_wedding_groom_troop"),
	   #Changed the gender requirement (used to be required male)
       #(troop_get_type, ":troop_type", ":players_king"),
       #(eq, ":troop_type", 0), #male
	   (call_script, "script_dplmc_store_troop_is_female", ":players_king"),
	   (this_or_next|eq, reg0, 0),
	   (this_or_next|eq, ":groom_is_woman", ":bride_is_woman"),
	      (ge, "$g_disable_condescending_comments", 2),
       (neq, ":players_king", "$g_wedding_bride_troop"),
       (neg|troop_slot_eq, "$g_wedding_bride_troop", slot_troop_father, ":players_king"),
	   (neg|troop_slot_eq, "$g_wedding_bride_troop", slot_troop_mother, ":players_king"),
       ##diplomacy end+
       (neq, ":players_king", "$g_wedding_groom_troop"),
       (assign, "$g_wedding_bishop_troop", ":players_king"),
     (else_try),
       (eq, "$players_kingdom", "fac_player_supporters_faction"),
       (faction_slot_eq, "$players_kingdom", slot_faction_leader, "trp_player"),
       (gt, "$g_player_minister", 0),
	   ##diplomacy start+
       #(troop_get_type, ":troop_type", "$g_player_minister"),
	   #(eq, ":troop_type", 0), #male
	   (call_script, "script_dplmc_store_troop_is_female", "$g_player_minister"),
	   (this_or_next|eq, reg0, 0),
	   (this_or_next|eq, ":groom_is_woman", ":bride_is_woman"),
	      (ge, "$g_disable_condescending_comments", 2),
	   ##diplomacy end+
       (neq, "$g_player_minister", "$g_wedding_groom_troop"),
       (assign, "$g_wedding_bishop_troop", "$g_player_minister"),
     (try_end),

     (assign, "$g_wedding_brides_dad_troop", "trp_temporary_minister"),
     (try_begin),
       (neq, "$g_wedding_bride_troop", "trp_player"),
       (try_begin),
         (troop_get_slot, ":father", "$g_wedding_bride_troop", slot_troop_father),
         (gt, ":father", 0),
         ##diplomacy start+
         (neg|troop_slot_ge, ":father", slot_troop_occupation, slto_retirement),
         #(troop_get_type, ":troop_type", ":father"), #just to make sure #<- dplmc+ replaced
		 (call_script, "script_dplmc_store_troop_is_female", ":father"),
		 (this_or_next|eq, ":bride_is_woman", 0),
			(eq, reg0, 0), #male
		 ##diplomacy end+
         (neq, ":father", "$g_wedding_groom_troop"), #this might be 0 due to an error
         (neq, ":father", "$g_wedding_bishop_troop"),
         (assign, "$g_wedding_brides_dad_troop", ":father"),
       (else_try),
         (troop_get_slot, ":guardian", "$g_wedding_bride_troop", slot_troop_guardian),
         (gt, ":guardian", 0),
         ##diplomacy start+
         (neg|troop_slot_ge, ":guardian", slot_troop_occupation, slto_retirement),
         #(troop_get_type, ":troop_type", ":guardian"), #just to make sure #<- dplmc+ replaced
		 (call_script, "script_dplmc_store_troop_is_female", ":guardian"),
		 (this_or_next|eq, ":bride_is_woman", 0),
			(eq, reg0, 0), #male
		 (call_script, "script_dplmc_store_troop_is_female", ":guardian"),
		 ##diplomacy end+
         (neq, ":guardian", "$g_wedding_groom_troop"), #this might be 0 due to an error
         (neq, ":guardian", "$g_wedding_bishop_troop"),
         (assign, "$g_wedding_brides_dad_troop", ":guardian"),
       ##diplomacy start+
	   #mother might be appropriate
	   (else_try),
		  (troop_get_slot, ":mother", "$g_wedding_bride_troop", slot_troop_mother),
	      (gt, ":mother", 0),
	      (neg|troop_slot_ge, ":mother", slot_troop_occupation, slto_retirement),

		  (neq, ":mother", "$g_wedding_groom_troop"),
		  (neq, ":mother", "$g_wedding_bride_troop"),
		  (neq, ":mother", "$g_wedding_bishop_troop"),

	      (assign, "$g_wedding_brides_dad_troop", ":mother"),
	   #we can get here, since male players can marry female lords
       (else_try),
          (is_between, "$g_wedding_bride_troop", companions_begin, companions_end),
          (troop_get_slot, ":cur_npc", "$g_wedding_bride_troop", slot_troop_personalitymatch_object),
          (ge, ":cur_npc", heroes_begin),
          (troop_slot_ge, ":cur_npc", slot_troop_met, 1),
		  (neg|troop_slot_ge, ":cur_npc", slot_troop_occupation, slto_retirement),
		  (this_or_next|troop_slot_eq, ":cur_npc", slot_troop_occupation, slto_kingdom_hero),
		  (this_or_next|troop_slot_eq, ":cur_npc", slot_troop_occupation, slto_player_companion),
		  (this_or_next|troop_slot_eq, ":cur_npc", slot_troop_occupation, slto_kingdom_seneschal),
		     (troop_slot_eq, ":cur_npc", slot_troop_occupation, slto_kingdom_lady),

		  (neg|troop_slot_ge, ":cur_npc", slot_troop_occupation, slto_retirement),
		  (neq, ":cur_npc", "$g_wedding_groom_troop"),
	      (neq, ":cur_npc", "$g_wedding_bride_troop"),
	      (neq, ":cur_npc", "$g_wedding_bishop_troop"),

		  (this_or_next|neg|troop_slot_ge, ":cur_npc", slot_lord_reputation_type, lrep_roguish),
		  (this_or_next|troop_slot_ge, ":cur_npc", slot_lord_reputation_type, lrep_conventional),

          (assign, "$g_wedding_brides_dad_troop", ":cur_npc"),
	   (else_try),
	      #any other companion or lord that is favorable
		  (assign, ":best_score", 0),#must be at least positive
		  (try_for_range, ":cur_npc", heroes_begin, heroes_end),
			(neq, ":cur_npc", "$g_wedding_groom_troop"),
	        (neq, ":cur_npc", "$g_wedding_bride_troop"),
	        (neq, ":cur_npc", "$g_wedding_bishop_troop"),
			(neq, ":cur_npc", "trp_knight_1_1_wife"),
			(neq, ":cur_npc", "trp_kingdom_heroes_including_player_begin"),

			(neg|troop_slot_ge, ":cur_npc", slot_troop_occupation, slto_retirement),

			(call_script, "script_troop_get_relation_with_troop", ":cur_npc", "$g_wedding_bride_troop"),
			(assign, ":relation", reg0),
			#(call_script, "script_troop_get_family_relation_to_troop", ":cur_npc", "$g_wedding_bride_troop"),
			(call_script, "script_dplmc_troop_get_family_relation_to_troop", ":cur_npc",  "$g_wedding_bride_troop"),
			(assign, ":family_relation", reg0),

			(store_add, ":score", ":relation", ":family_relation"),

			(gt, ":score", ":best_score"),#score better than current best
			(assign, ":best_score", ":score"),
			(assign, "$g_wedding_brides_dad_troop", ":cur_npc"),
		  (try_end),
       ##diplomacy end+
       (try_end),
     (else_try),
	   #gekokujo 3.0 microfactions! include fort companions start
       #(try_for_range, ":cur_companion", companions_begin, companions_end),
       (try_for_range, ":cur_companion", companions_begin, fort_companions_end),
	   #gekokujo 3.0 microfactions! include fort companions end
         (this_or_next|troop_slot_eq, ":cur_companion", slot_troop_occupation, slto_player_companion),
         (troop_slot_eq, ":cur_companion", slot_troop_occupation, slto_kingdom_hero),
		 ##diplomacy start+
         #(troop_get_type, ":troop_type", ":cur_companion"), #just to make sure
         #(eq, ":troop_type", 0), #male
		 (call_script, "script_dplmc_store_troop_is_female", ":cur_companion"),
		 (this_or_next|eq, reg0, 0),
			(eq, ":bride_is_woman", 0),
		 ##diplomacy end+
         (neq, ":cur_companion", "$g_wedding_groom_troop"),
         (neq, ":cur_companion", "$g_wedding_bishop_troop"),
         (assign, "$g_wedding_brides_dad_troop", ":cur_companion"),
       (try_end),
       ##diplomacy start+ try again with female companions if no male companions available
       (eq, "$g_wedding_brides_dad_troop", "trp_temporary_minister"),
	   #gekokujo 3.0 microfactions! include fort companions start
       #(try_for_range, ":cur_companion", companions_begin, companions_end),
       (try_for_range, ":cur_companion", companions_begin, fort_companions_end),
	   #gekokujo 3.0 microfactions! include fort companions end
         (this_or_next|troop_slot_eq, ":cur_companion", slot_troop_occupation, slto_player_companion),
			(troop_slot_eq, ":cur_companion", slot_troop_occupation, slto_kingdom_hero),
         (neq, ":cur_companion", "$g_wedding_groom_troop"),
         (neq, ":cur_companion", "$g_wedding_bishop_troop"),
         (assign, "$g_wedding_brides_dad_troop", ":cur_companion"),
       (try_end),
	   #try again with all lords if no female companions available
	   (eq, "$g_wedding_brides_dad_troop", "trp_temporary_minister"),
	   (assign, ":best_score", -100),#best score
       (try_for_range, ":cur_npc", heroes_begin, heroes_end),
	     (neg|troop_slot_eq, ":cur_npc", slot_troop_met, 0),

 	     (this_or_next|troop_slot_eq, ":cur_npc", slot_troop_occupation, slto_kingdom_seneschal),
         (this_or_next|troop_slot_eq, ":cur_npc", slot_troop_occupation, slto_player_companion),
		 (this_or_next|troop_slot_eq, ":cur_npc", slot_troop_occupation, slto_kingdom_lady),
			(troop_slot_eq, ":cur_npc", slot_troop_occupation, slto_kingdom_hero),

         (neq, ":cur_npc", "$g_wedding_groom_troop"),
         (neq, ":cur_npc", "$g_wedding_bishop_troop"),
		 (neq, ":cur_npc", "trp_knight_1_1_wife"),
	 	 (neq, ":cur_npc", "trp_kingdom_heroes_including_player_begin"),

		 (call_script, "script_troop_get_player_relation", ":cur_npc"),
		 (assign, ":score", reg0),
		 (ge, ":score", 0),
		 (call_script, "script_dplmc_is_affiliated_family_member", ":cur_npc"),
		 (this_or_next|ge, ":score", 20),
			(ge, reg0, 1),
		 (gt, ":score", ":best_score"),
		 (assign, ":best_score", ":score"),
         (assign, "$g_wedding_brides_dad_troop", ":cur_npc"),
       (try_end),
       ##diplomacy end+
     (try_end),

     (modify_visitors_at_site,"scn_wedding"),
     (reset_visitors,0),
     (set_visitor, 0, "$g_wedding_groom_troop"),
     (set_visitor, 1, "$g_wedding_bride_troop"),
     (set_visitor, 2, "$g_wedding_brides_dad_troop"),
     (set_visitor, 3, "$g_wedding_bishop_troop"),
     (assign, ":num_visitors", 4),
     (assign, ":num_male_visitors", 0),
	 ##diplomacy start+
	 (store_troop_faction, ":groom_faction", "$g_wedding_groom_troop"),
	 (store_troop_faction, ":bride_faction", "$g_wedding_bride_troop"),
	 ##diplomacy end+
     (try_for_range, ":cur_npc", active_npcs_begin, kingdom_ladies_end),
       (lt, ":num_visitors", 32),
       (neq, ":cur_npc", "$g_wedding_groom_troop"),
       (neq, ":cur_npc", "$g_wedding_bride_troop"),
       (neq, ":cur_npc", "$g_wedding_brides_dad_troop"),
       (neq, ":cur_npc", "$g_wedding_bishop_troop"),
       (store_troop_faction, ":npc_faction", ":cur_npc"),
	   ##diplomacy start+
       #(is_between, ":npc_faction", kingdoms_begin, kingdoms_end),
       #(eq, ":npc_faction", "$players_kingdom"),
	   (this_or_next|eq, ":groom_faction", ":npc_faction"),
	      (eq, ":bride_faction", ":npc_faction"),
       ##diplomacy end+
       (this_or_next|troop_slot_eq, ":cur_npc", slot_troop_occupation, slto_player_companion),
       (this_or_next|troop_slot_eq, ":cur_npc", slot_troop_occupation, slto_kingdom_hero),
       (troop_slot_eq, ":cur_npc", slot_troop_occupation, slto_kingdom_lady),
	   ##diplomacy start+
       #(troop_get_type, ":troop_type", ":cur_npc"),
	   (call_script, "script_dplmc_store_troop_is_female", ":cur_npc"),
	   (assign, ":troop_type", reg0),
	   ##diplomacy end+
       (assign, ":continue_adding", 1),
       (try_begin),
         (eq, ":troop_type", 0),
         (assign, ":continue_adding", 0),
         (lt, ":num_male_visitors", 16), #limit number of male visitors
         (assign, ":continue_adding", 1),
         (val_add, ":num_male_visitors", 1),
       (try_end),
       (eq, ":continue_adding", 1),
       (set_visitor, ":num_visitors", ":cur_npc"),
       (val_add, ":num_visitors", 1),
     (try_end),
	 ##diplomacy start+
	 (assign, reg0, ":save_reg0"),
	 (assign, reg1, ":save_reg1"),
	 ##diplomacy end+
     (set_jump_mission,"mt_wedding"),
     (jump_to_scene,"scn_wedding"),
     (change_screen_mission),
    ]),
  ("count_parties_of_faction_and_party_type",
    [
      (store_script_param_1, ":faction_no"),
      (store_script_param_2, ":party_type"),
      (assign, reg0, 0),
      (try_for_parties, ":party_no"),
        (party_is_active, ":party_no"),
        (party_get_slot, ":cur_party_type", ":party_no", slot_party_type),
        (store_faction_of_party, ":cur_faction", ":party_no"),
        (eq, ":cur_party_type", ":party_type"),
        (eq, ":cur_faction", ":faction_no"),
        (val_add, reg0, 1),
      (try_end),
  ]),
# script_faction_get_number_of_armies
# Input: arg1 = faction_no
# Output: reg0 = number_of_armies
  ("faction_get_number_of_armies",
   [
      (store_script_param_1, ":faction_no"),
      (assign, ":num_armies", 0),
      ##diplomacy start+ support for promoted kingdom ladies
      (try_for_range, ":troop_no", heroes_begin, heroes_end),#<- changed from active_npcs to heroes
      ##diplomacy end+
		(troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
    	(store_troop_faction, ":hero_faction_no", ":troop_no"),
        (eq, ":hero_faction_no", ":faction_no"),
        (troop_get_slot, ":hero_party", ":troop_no", slot_troop_leaded_party),
        (ge, ":hero_party", 0),
        (party_is_active, ":hero_party"),
        (call_script, "script_party_count_fit_regulars", ":hero_party"),
        (assign, ":party_size", reg0),
        (call_script, "script_party_get_ideal_size", ":hero_party"),
        (assign, ":ideal_size", reg0),
        (val_mul, ":ideal_size", 60),
        (val_div, ":ideal_size", 100),
        (gt, ":party_size", ":ideal_size"),
        (val_add, ":num_armies", 1),
      (try_end),
      (assign, reg0, ":num_armies"),
    ]),
# script_faction_recalculate_strength
# Input: arg1 = faction_no
# Output: reg0 = strength
  ("faction_recalculate_strength",
   [
      (store_script_param_1, ":faction_no"),

      (call_script, "script_faction_get_number_of_armies", ":faction_no"),
      (assign, ":num_armies", reg0),
      (assign, ":num_castles", 0),
      (assign, ":num_towns", 0),

      (try_for_range, ":center_no", centers_begin, centers_end),
        (store_faction_of_party, ":center_faction", ":center_no"),
        (eq, ":center_faction", ":faction_no"),
        (try_begin),
          (party_slot_eq, ":center_no", slot_party_type, spt_castle),
          (val_add, ":num_castles", 1),
        (else_try),
          (party_slot_eq, ":center_no", slot_party_type, spt_town),
          (val_add, ":num_towns", 1),
        (try_end),
      (try_end),

      (faction_set_slot, ":faction_no", slot_faction_num_armies, ":num_armies"),
      (faction_set_slot, ":faction_no", slot_faction_num_castles, ":num_castles"),
      (faction_set_slot, ":faction_no", slot_faction_num_towns, ":num_towns"),

    ]),
  #OUTPUT:
  # This script may return false if there is no matching town.
  # reg0 = town_no
  ("cf_select_random_town_with_faction",
    [
      (store_script_param_1, ":faction_no"),
      (assign, ":result", -1),
      # First count num matching spawn points
      (assign, ":no_towns", 0),
      (try_for_range,":cur_town", towns_begin, towns_end),
        (store_faction_of_party, ":cur_faction", ":cur_town"),
        (eq, ":cur_faction", ":faction_no"),
        (val_add, ":no_towns", 1),
      (try_end),
      (gt, ":no_towns", 0), #Fail if there are no towns
      (store_random_in_range, ":random_town", 0, ":no_towns"),
      (assign, ":no_towns", 0),
      (try_for_range,":cur_town", towns_begin, towns_end),
        (eq, ":result", -1),
        (store_faction_of_party, ":cur_faction", ":cur_town"),
        (eq, ":cur_faction", ":faction_no"),
        (val_add, ":no_towns", 1),
        (gt, ":no_towns", ":random_town"),
        (assign, ":result", ":cur_town"),
      (try_end),
      (assign, reg0, ":result"),
  ]),
  #OUTPUT:
  # This script may return false if there is no matching village.
  # reg0 = village_no
  ("cf_select_random_village_with_faction",
    [
      (store_script_param_1, ":faction_no"),
      (assign, ":result", -1),
      # First count num matching spawn points
      (assign, ":no_villages", 0),
      (try_for_range,":cur_village", villages_begin, villages_end),
        (store_faction_of_party, ":cur_faction", ":cur_village"),
        (eq, ":cur_faction", ":faction_no"),
        (val_add, ":no_villages", 1),
      (try_end),
      (gt, ":no_villages", 0), #Fail if there are no villages
      (store_random_in_range, ":random_village", 0, ":no_villages"),
      (assign, ":no_villages", 0),
      (try_for_range,":cur_village", villages_begin, villages_end),
        (eq, ":result", -1),
        (store_faction_of_party, ":cur_faction", ":cur_village"),
        (eq, ":cur_faction", ":faction_no"),
        (val_add, ":no_villages", 1),
        (gt, ":no_villages", ":random_village"),
        (assign, ":result", ":cur_village"),
      (try_end),
      (assign, reg0, ":result"),
  ]),
  #OUTPUT:
  # This script may return false if there is no matching town.
  # reg0 = town_no (Can fail)
  ("cf_select_random_walled_center_with_faction",
    [
      (store_script_param, ":faction_no", 1),
      (store_script_param, ":preferred_center_no", 2),
      (assign, ":result", -1),
      # First count num matching spawn points
      (assign, ":no_centers", 0),
      (try_for_range,":cur_center", walled_centers_begin, walled_centers_end),
        (store_faction_of_party, ":cur_faction", ":cur_center"),
        (eq, ":cur_faction", ":faction_no"),
        (val_add, ":no_centers", 1),
        (eq, ":cur_center", ":preferred_center_no"),
        (val_add, ":no_centers", 99),
      (try_end),
      (gt, ":no_centers", 0), #Fail if there are no centers
      (store_random_in_range, ":random_center", 0, ":no_centers"),
      (try_for_range,":cur_center", walled_centers_begin, walled_centers_end),
        (eq, ":result", -1),
        (store_faction_of_party, ":cur_faction", ":cur_center"),
        (eq, ":cur_faction", ":faction_no"),
        (val_sub, ":random_center", 1),
        (try_begin),
          (eq, ":cur_center", ":preferred_center_no"),
          (val_sub, ":random_center", 99),
        (try_end),
        (lt, ":random_center", 0),
        (assign, ":result", ":cur_center"),
      (try_end),
      (assign, reg0, ":result"),
  ]),
  #script_cf_select_random_walled_center_with_faction_and_owner_priority_no_siege:
  # INPUT:
  # arg1 = faction_no
  # arg2 = owner_troop_no
  #OUTPUT:
  # This script may return false if there is no matching town.
  # reg0 = center_no (Can fail)
  ("cf_select_random_walled_center_with_faction_and_owner_priority_no_siege",
    [
      (store_script_param, ":faction_no", 1),
      (store_script_param, ":troop_no", 2),
      (assign, ":result", -1),
      (assign, ":no_centers", 0),
      
      (call_script, "script_lord_get_home_center", ":troop_no"),
      (assign, ":home_center", reg0),
      
      (try_for_range,":cur_center", walled_centers_begin, walled_centers_end),
        (store_faction_of_party, ":cur_faction", ":cur_center"),
        (eq, ":cur_faction", ":faction_no"),
        (party_slot_eq, ":cur_center", slot_center_is_besieged_by, -1),
        (val_add, ":no_centers", 1),
        
        #(party_slot_eq, ":cur_center", slot_town_lord, ":troop_no"),
        (eq, ":home_center", ":cur_center"), #I changed it with above line, now if lord is owner of any village its bound walled center is counted as 1000. Better this way. ozan-18.01.09
        
        (val_add, ":no_centers", 1000),
      (try_end),
     ##diplomacy start+
     ##Add Caba`drin's fix for a lord respawning bug caused by an inane change in Warband 1.142
     (gt, ":no_centers", 0),#Cause the script to fail when there weren't any eligible centers.
     (assign, "$g_there_is_no_avaliable_centers", 0),
     ##Not logically necessary, but for clarity comment out the following lines:
#	  #if no center is available count all centers not besieged do not care its faction.
#	  (try_begin),
#        (le, ":no_centers", 0),
#
#		(assign, "$g_there_is_no_avaliable_centers", 1),
#
#        (try_for_range,":cur_center", walled_centers_begin, walled_centers_end),
#	      (party_slot_eq, ":cur_center", slot_center_is_besieged_by, -1),
#          (val_add, ":no_centers", 1),
#        (try_end),
#	  (else_try),
#	    (assign, "$g_there_is_no_avaliable_centers", 0),
#	  (try_end),
     ##end of Caba`drin's fix for the lord respawning bug
     ##diplomacy end+

      (faction_get_slot, ":faction_leader", ":faction_no", slot_faction_leader),
	  (this_or_next|eq, "$g_there_is_no_avaliable_centers", 0),
      (neq, ":troop_no", ":faction_leader"), #faction leaders cannot spawn if they have no centers.

      (store_random_in_range, ":random_center", 0, ":no_centers"),
      (try_for_range,":cur_center", walled_centers_begin, walled_centers_end),
        (eq, ":result", -1),
        (store_faction_of_party, ":cur_faction", ":cur_center"),
##diplomacy start+ Not logically necessary, but for clarity comment out the following line:
#		(this_or_next|eq, "$g_there_is_no_avaliable_centers", 1),
##diplomacy end+
        (eq, ":cur_faction", ":faction_no"),
        (party_slot_eq, ":cur_center", slot_center_is_besieged_by, -1),
        (val_sub, ":random_center", 1),
        (try_begin),
          #(party_slot_eq, ":cur_center", slot_town_lord, ":troop_no"),
          (eq, ":home_center", ":cur_center"), #I changed it with above line, now if lord is owner of any village its bound walled center is counted as 1000. Better this way. ozan-18.01.09
		  (eq, "$g_there_is_no_avaliable_centers", 0),

          (val_sub, ":random_center", 1000),
        (try_end),
        (lt, ":random_center", 0),
        (assign, ":result", ":cur_center"),
      (try_end),
      (assign, reg0, ":result"),
  ]),
  #OUTPUT:
  # This script may return false if there is no matching town.
  # reg0 = town_no (Can fail)
  ("cf_select_random_walled_center_with_faction_and_less_strength_priority",
    [
      (store_script_param, ":faction_no", 1),
      (store_script_param, ":preferred_center_no", 2),
      (assign, ":result", -1),
      # First count num matching spawn points
      (assign, ":no_centers", 0),
      (try_for_range, ":cur_center", walled_centers_begin, walled_centers_end),
        (store_faction_of_party, ":cur_faction", ":cur_center"),
        (eq, ":cur_faction", ":faction_no"),
        (party_slot_eq, ":cur_center", slot_center_is_besieged_by, -1),
        (val_add, ":no_centers", 1),
        (try_begin),
          (eq, ":cur_center", ":preferred_center_no"),
          (val_add, ":no_centers", 99),
        (try_end),
##        (call_script, "script_party_calculate_regular_strength", ":cur_center"),
##        (assign, ":strength", reg0),
##        (lt, ":strength", 80),
##        (store_sub, ":strength", 100, ":strength"),
##        (val_div, ":strength", 20),
##        (val_add, ":no_centers", ":strength"),
      (try_end),
      (gt, ":no_centers", 0), #Fail if there are no centers
      (store_random_in_range, ":random_center", 0, ":no_centers"),
      (try_for_range, ":cur_center", walled_centers_begin, walled_centers_end),
        (eq, ":result", -1),
        (store_faction_of_party, ":cur_faction", ":cur_center"),
        (eq, ":cur_faction", ":faction_no"),
        (party_slot_eq, ":cur_center", slot_center_is_besieged_by, -1),
        (val_sub, ":random_center", 1),
        (try_begin),
          (eq, ":cur_center", ":preferred_center_no"),
          (val_sub, ":random_center", 99),
        (try_end),
##        (try_begin),
##          (call_script, "script_party_calculate_regular_strength", ":cur_center"),
##          (assign, ":strength", reg0),
##          (lt, ":strength", 80),
##          (store_sub, ":strength", 100, ":strength"),
##          (val_div, ":strength", 20),
##          (val_sub, ":random_center", ":strength"),
##        (try_end),
        (lt, ":random_center", 0),
        (assign, ":result", ":cur_center"),
      (try_end),
      (assign, reg0, ":result"),
  ]),
  #OUTPUT:
  # This script may return false if there is no matching town.
  # reg0 = town_no
  ("cf_select_random_town_at_peace_with_faction",
    [
      (store_script_param_1, ":faction_no"),
      (assign, ":result", -1),
      # First count num matching towns
      (assign, ":no_towns", 0),
      (try_for_range,":cur_town", towns_begin, towns_end),
        (store_faction_of_party, ":cur_faction", ":cur_town"),
        (store_relation,":reln", ":cur_faction", ":faction_no"),
        (ge, ":reln", 0),
        (val_add, ":no_towns", 1),
      (try_end),
      (gt, ":no_towns", 0), #Fail if there are no towns
      (store_random_in_range, ":random_town", 0, ":no_towns"),
      (assign, ":no_towns", 0),
      (try_for_range,":cur_town", towns_begin, towns_end),
        (eq, ":result", -1),
        (store_faction_of_party, ":cur_faction", ":cur_town"),
        (store_relation,":reln", ":cur_faction", ":faction_no"),
        (ge, ":reln", 0),
        (val_add, ":no_towns", 1),
        (gt, ":no_towns", ":random_town"),
        (assign, ":result", ":cur_town"),
      (try_end),
      (assign, reg0, ":result"),
  ]),
  # script_cf_get_random_enemy_center_within_range
  # Input: arg1 = party_no, arg2 = range (in kms)
  # Output: reg0 = center_no
  ("cf_get_random_enemy_center_within_range",
    [
      (store_script_param, ":party_no", 1),
      (store_script_param, ":range", 2),

      (assign, ":num_centers", 0),
      (store_faction_of_party, ":faction_no", ":party_no"),
      (try_for_range, ":cur_center", centers_begin, centers_end),
        (store_faction_of_party, ":cur_faction", ":cur_center"),
        (store_relation, ":cur_relation", ":faction_no", ":cur_faction"),
        (lt, ":cur_relation", 0),
        (store_distance_to_party_from_party, ":dist", ":party_no", ":cur_center"),
        (le, ":dist", ":range"),
        (val_add, ":num_centers", 1),
      (try_end),
      (gt, ":num_centers", 0),
      (store_random_in_range, ":random_center", 0, ":num_centers"),
      (assign, ":end_cond", centers_end),
      (try_for_range, ":cur_center", centers_begin, ":end_cond"),
        (store_faction_of_party, ":cur_faction", ":cur_center"),
        (store_relation, ":cur_relation", ":faction_no", ":cur_faction"),
        (lt, ":cur_relation", 0),
        (store_distance_to_party_from_party, ":dist", ":party_no", ":cur_center"),
        (le, ":dist", ":range"),
        (val_sub, ":random_center", 1),
        (lt, ":random_center", 0),
        (assign, ":result", ":cur_center"),
        (assign, ":end_cond", 0),#break
      (try_end),
      (assign, reg0, ":result"),
  ]),
  # script_cf_faction_get_random_enemy_faction
  # Input: arg1 = faction_no
  # Output: reg0 = faction_no (Can fail)
  ("cf_faction_get_random_enemy_faction",
    [
      (store_script_param_1, ":faction_no"),
      
      (assign, ":result", -1),
      (assign, ":count_factions", 0),
      (try_for_range, ":cur_faction", kingdoms_begin, kingdoms_end),
        (faction_slot_eq, ":cur_faction", slot_faction_state, sfs_active),
        (store_relation, ":cur_relation", ":faction_no", ":cur_faction"),
        (le, ":cur_relation", -1),
        (val_add, ":count_factions", 1),
      (try_end),
      (store_random_in_range,":random_faction",0,":count_factions"),
      (assign, ":count_factions", 0),
      (try_for_range, ":cur_faction", kingdoms_begin, kingdoms_end),
        (eq, ":result", -1),
        (faction_slot_eq, ":cur_faction", slot_faction_state, sfs_active),
        (store_relation, ":cur_relation", ":faction_no", ":cur_faction"),
        (le, ":cur_relation", -1),
        (val_add, ":count_factions", 1),
        (gt, ":count_factions", ":random_faction"),
        (assign, ":result", ":cur_faction"),
      (try_end),
      
      (neq, ":result", -1),
      (assign, reg0, ":result"),
  ]),
  # script_cf_faction_get_random_friendly_faction
  # Input: arg1 = faction_no
  # Output: reg0 = faction_no (Can fail)
  ("cf_faction_get_random_friendly_faction",
    [
      (store_script_param_1, ":faction_no"),
      
      (assign, ":result", -1),
      (assign, ":count_factions", 0),
      (try_for_range, ":cur_faction", kingdoms_begin, kingdoms_end),
        (faction_slot_eq, ":cur_faction", slot_faction_state, sfs_active),
        (neq, ":cur_faction", ":faction_no"),
        (store_relation, ":cur_relation", ":faction_no", ":cur_faction"),
        (ge, ":cur_relation", 0),
        (val_add, ":count_factions", 1),
      (try_end),
      (store_random_in_range,":random_faction",0,":count_factions"),
      (assign, ":count_factions", 0),
      (try_for_range, ":cur_faction", kingdoms_begin, kingdoms_end),
        (eq, ":result", -1),
        (faction_slot_eq, ":cur_faction", slot_faction_state, sfs_active),
        (neq, ":cur_faction", ":faction_no"),
        (store_relation, ":cur_relation", ":faction_no", ":cur_faction"),
        (ge, ":cur_relation", 0),
        (val_add, ":count_factions", 1),
        (gt, ":count_factions", ":random_faction"),
        (assign, ":result", ":cur_faction"),
      (try_end),
      
      (neq, ":result", -1),
      (assign, reg0, ":result"),
  ]),
  # script_cf_troop_get_random_enemy_troop_with_occupation
  # Input: arg1 = troop_no,
  # Output: reg0 = enemy_troop_no (Can fail)
  ("cf_troop_get_random_enemy_troop_with_occupation",
    [
      (store_script_param_1, ":troop_no"),
      (store_script_param_2, ":occupation"),
      
      (assign, ":result", -1),
      (assign, ":count_enemies", 0),
      (try_for_range, ":enemy_troop_no", active_npcs_begin, active_npcs_end),
        (troop_slot_eq, ":enemy_troop_no", slot_troop_occupation, ":occupation"),
        (call_script, "script_troop_get_relation_with_troop", ":troop_no", ":enemy_troop_no"),         
        (lt, reg0, -10), 
        (val_add, ":count_enemies", 1),
      (try_end),
      
      (gt, ":count_enemies", 0),
      (store_random_in_range,":random_enemy",0,":count_enemies"),
      
      (assign, ":count_enemies", 0),
      (try_for_range, ":enemy_troop_no", active_npcs_begin, active_npcs_end),
        (troop_slot_eq, ":enemy_troop_no", slot_troop_occupation, ":occupation"),
        (call_script, "script_troop_get_relation_with_troop", ":troop_no", ":enemy_troop_no"), 
        (lt, reg0, -10),
        (val_add, ":count_enemies", 1),
        (eq, ":random_enemy", ":count_enemies"),
        (assign, ":result", ":enemy_troop_no"),
      (try_end),
      
      (neq, ":result", -1),
      (assign, reg0, ":result"),
  ]),
  # script_cf_get_random_lord_in_a_center_with_faction
  # Input: arg1 = faction_no
  # Output: reg0 = troop_no, Can Fail!
  ("cf_get_random_lord_in_a_center_with_faction",
    [
      (store_script_param_1, ":faction_no"),
      (assign, ":result", -1),
      (assign, ":count_lords", 0),
      (try_for_range, ":lord_no", heroes_begin, heroes_end),
        (store_troop_faction, ":lord_faction_no", ":lord_no"),
        (eq, ":faction_no", ":lord_faction_no"),
        (troop_slot_eq, ":lord_no", slot_troop_occupation, slto_kingdom_hero),
        #(troop_slot_eq, ":lord_no", slot_troop_is_prisoner, 0),
        (neg|troop_slot_ge, ":lord_no", slot_troop_prisoner_of_party, 0),
        (troop_get_slot, ":lord_party", ":lord_no", slot_troop_leaded_party),
        (ge, ":lord_party", 0),
        (party_get_attached_to, ":lord_attachment", ":lord_party"),
        (is_between, ":lord_attachment", centers_begin, centers_end), #is troop in a center?
        (val_add, ":count_lords", 1),
      (try_end),
      (store_random_in_range, ":random_lord", 0, ":count_lords"),
      (assign, ":count_lords", 0),
      (try_for_range, ":lord_no", heroes_begin, heroes_end),
        (eq, ":result", -1),
        (store_troop_faction, ":lord_faction_no", ":lord_no"),
        (eq, ":faction_no", ":lord_faction_no"),
        (troop_slot_eq, ":lord_no", slot_troop_occupation, slto_kingdom_hero),
        #(troop_slot_eq, ":lord_no", slot_troop_is_prisoner, 0),
        (neg|troop_slot_ge, ":lord_no", slot_troop_prisoner_of_party, 0),
        (troop_get_slot, ":lord_party", ":lord_no", slot_troop_leaded_party),
        (ge, ":lord_party", 0),
        (party_get_attached_to, ":lord_attachment", ":lord_party"),
        (is_between, ":lord_attachment", centers_begin, centers_end), #is troop in a center?
        (val_add, ":count_lords", 1),
        (lt, ":random_lord", ":count_lords"),
        (assign, ":result", ":lord_no"),
      (try_end),
      (neq, ":result", -1),
      (assign, reg0, ":result"),
  ]),
  # script_cf_get_random_lord_except_king_with_faction
  # Input: arg1 = faction_no
  # Output: reg0 = troop_no, Can Fail!
  ("cf_get_random_lord_except_king_with_faction",
    [
      (store_script_param_1, ":faction_no"),
      (assign, ":result", -1),
      (assign, ":count_lords", 0),
      (try_for_range, ":lord_no", heroes_begin, heroes_end),
        (store_troop_faction, ":lord_faction_no", ":lord_no"),
        (eq, ":faction_no", ":lord_faction_no"),
        (neg|faction_slot_eq, ":faction_no", slot_faction_leader, ":lord_no"),
        (troop_slot_eq, ":lord_no", slot_troop_occupation, slto_kingdom_hero),
        #(troop_slot_eq, ":lord_no", slot_troop_is_prisoner, 0),
        (neg|troop_slot_ge, ":lord_no", slot_troop_prisoner_of_party, 0),
        (troop_get_slot, ":lord_party", ":lord_no", slot_troop_leaded_party),
        (ge, ":lord_party", 0),
        (val_add, ":count_lords", 1),
      (try_end),
      (store_random_in_range, ":random_lord", 0, ":count_lords"),
      (assign, ":count_lords", 0),
      (try_for_range, ":lord_no", heroes_begin, heroes_end),
        (eq, ":result", -1),
        (store_troop_faction, ":lord_faction_no", ":lord_no"),
        (eq, ":faction_no", ":lord_faction_no"),
        (neg|faction_slot_eq, ":faction_no", slot_faction_leader, ":lord_no"),
        (troop_slot_eq, ":lord_no", slot_troop_occupation, slto_kingdom_hero),
        #(troop_slot_eq, ":lord_no", slot_troop_is_prisoner, 0),
        (neg|troop_slot_ge, ":lord_no", slot_troop_prisoner_of_party, 0),
        (troop_get_slot, ":lord_party", ":lord_no", slot_troop_leaded_party),
        (ge, ":lord_party", 0),
        (val_add, ":count_lords", 1),
        (lt, ":random_lord", ":count_lords"),
        (assign, ":result", ":lord_no"),
      (try_end),
      (neq, ":result", -1),
      (assign, reg0, ":result"),
  ]),
  # script_cf_get_random_lord_from_another_faction_in_a_center
  # Input: arg1 = faction_no
  # Output: reg0 = troop_no, Can Fail!
  ("cf_get_random_lord_from_another_faction_in_a_center",
    [
      (store_script_param_1, ":faction_no"),
      (assign, ":result", -1),
      (assign, ":count_lords", 0),
      (try_for_range, ":lord_no", heroes_begin, heroes_end),
        (store_troop_faction, ":lord_faction_no", ":lord_no"),
        (neq, ":lord_faction_no", ":faction_no"),
        (store_relation, ":our_relation", ":lord_faction_no", "fac_player_supporters_faction"),
        (store_relation, ":lord_relation", ":lord_faction_no", ":faction_no"),
        (lt, ":lord_relation", 0),
        (ge, ":our_relation", 0),
        (troop_slot_eq, ":lord_no", slot_troop_occupation, slto_kingdom_hero),
        #(troop_slot_eq, ":lord_no", slot_troop_is_prisoner, 0),
        (neg|troop_slot_ge, ":lord_no", slot_troop_prisoner_of_party, 0),
        (troop_get_slot, ":lord_party", ":lord_no", slot_troop_leaded_party),
        (ge, ":lord_party", 0),
        (party_get_attached_to, ":lord_attachment", ":lord_party"),
        (is_between, ":lord_attachment", centers_begin, centers_end), #is troop in a center?
        (val_add, ":count_lords", 1),
      (try_end),
      (store_random_in_range, ":random_lord", 0, ":count_lords"),
      (assign, ":count_lords", 0),
      (try_for_range, ":lord_no", heroes_begin, heroes_end),
        (eq, ":result", -1),
        (store_troop_faction, ":lord_faction_no", ":lord_no"),
        (neq, ":lord_faction_no", ":faction_no"),
        (store_relation, ":our_relation", ":lord_faction_no", "fac_player_supporters_faction"),
        (store_relation, ":lord_relation", ":lord_faction_no", ":faction_no"),
        (lt, ":lord_relation", 0),
        (ge, ":our_relation", 0),
        (troop_slot_eq, ":lord_no", slot_troop_occupation, slto_kingdom_hero),
        #(troop_slot_eq, ":lord_no", slot_troop_is_prisoner, 0),
        (neg|troop_slot_ge, ":lord_no", slot_troop_prisoner_of_party, 0),
        (troop_get_slot, ":lord_party", ":lord_no", slot_troop_leaded_party),
        (ge, ":lord_party", 0),
        (party_get_attached_to, ":lord_attachment", ":lord_party"),
        (is_between, ":lord_attachment", centers_begin, centers_end), #is troop in a center?
        (val_add, ":count_lords", 1),
        (lt, ":random_lord", ":count_lords"),
        (assign, ":result", ":lord_no"),
      (try_end),
      (neq, ":result", -1),
      (assign, reg0, ":result"),
  ]),
  # script_get_closest_walled_center
  # Input: arg1 = party_no
  # Output: reg0 = center_no (closest)
  ("get_closest_walled_center",
    [
      (store_script_param_1, ":party_no"),
      (assign, ":min_distance", 9999999),
      (assign, reg0, -1),
      (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
        (store_distance_to_party_from_party, ":party_distance", ":party_no", ":center_no"),
        (lt, ":party_distance", ":min_distance"),
        (assign, ":min_distance", ":party_distance"),
        (assign, reg0, ":center_no"),
      (try_end),
  ]),
  # script_get_closest_center
  # Input: arg1 = party_no
  # Output: reg0 = center_no (closest)
  ("get_closest_center",
    [
      (store_script_param_1, ":party_no"),
      (assign, ":min_distance", 9999999),
      (assign, reg0, -1),
      (try_for_range, ":center_no", centers_begin, centers_end),
        (store_distance_to_party_from_party, ":party_distance", ":party_no", ":center_no"),
        (lt, ":party_distance", ":min_distance"),
        (assign, ":min_distance", ":party_distance"),
        (assign, reg0, ":center_no"),
      (try_end),
  ]),
  # script_get_closest_center_of_faction
  # Input: arg1 = party_no, arg2 = kingdom_no
  # Output: reg0 = center_no (closest)
  ("get_closest_center_of_faction",
    [
      (store_script_param_1, ":party_no"),
      (store_script_param_2, ":kingdom_no"),
      (assign, ":min_distance", 99999),
      (assign, ":result", -1),
      (try_for_range, ":center_no", centers_begin, centers_end),
        (store_faction_of_party, ":faction_no", ":center_no"),
        (eq, ":faction_no", ":kingdom_no"),
        (store_distance_to_party_from_party, ":party_distance", ":party_no", ":center_no"),
        (lt, ":party_distance", ":min_distance"),
        (assign, ":min_distance", ":party_distance"),
        (assign, ":result", ":center_no"),
      (try_end),
      (assign, reg0, ":result"),
  ]),
  # script_get_closest_walled_center_of_faction
  # Input: arg1 = party_no, arg2 = kingdom_no
  # Output: reg0 = center_no (closest)
  ("get_closest_walled_center_of_faction",
    [
      (store_script_param_1, ":party_no"),
      (store_script_param_2, ":kingdom_no"),
      (assign, ":min_distance", 99999),
      (assign, ":result", -1),
      (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
        (store_faction_of_party, ":faction_no", ":center_no"),
        (eq, ":faction_no", ":kingdom_no"),
        (store_distance_to_party_from_party, ":party_distance", ":party_no", ":center_no"),
        (lt, ":party_distance", ":min_distance"),
        (assign, ":min_distance", ":party_distance"),
        (assign, ":result", ":center_no"),
      (try_end),
      (assign, reg0, ":result"),
  ]),
  # script_get_heroes_attached_to_center_aux
  # For internal use only
  ("get_heroes_attached_to_center_aux",
    [
      (store_script_param_1, ":center_no"),
      (store_script_param_2, ":party_no_to_collect_heroes"),
      (party_get_num_companion_stacks, ":num_stacks",":center_no"),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop",":center_no",":i_stack"),
        (troop_is_hero, ":stack_troop"),
        (party_add_members, ":party_no_to_collect_heroes", ":stack_troop", 1),
      (try_end),
      (party_get_num_attached_parties, ":num_attached_parties", ":center_no"),
      (try_for_range, ":attached_party_rank", 0, ":num_attached_parties"),
        (party_get_attached_party_with_rank, ":attached_party", ":center_no", ":attached_party_rank"),
        (call_script, "script_get_heroes_attached_to_center_aux", ":attached_party", ":party_no_to_collect_heroes"),
      (try_end),
  ]),
  # script_get_heroes_attached_to_center
  # Input: arg1 = center_no, arg2 = party_no_to_collect_heroes
  # Output: none, adds heroes to the party_no_to_collect_heroes party
  ("get_heroes_attached_to_center",
    [
      (store_script_param_1, ":center_no"),
      (store_script_param_2, ":party_no_to_collect_heroes"),
      (party_clear, ":party_no_to_collect_heroes"),
      (call_script, "script_get_heroes_attached_to_center_aux", ":center_no", ":party_no_to_collect_heroes"),

#rebellion changes begin -Arma
     (try_for_range, ":pretender", pretenders_begin, pretenders_end),
        (neq, ":pretender", "$supported_pretender"),
        (troop_slot_eq, ":pretender", slot_troop_cur_center, ":center_no"),
        (party_add_members, ":party_no_to_collect_heroes", ":pretender", 1),
     (try_end),

#     (try_for_range, ":rebel_faction", rebel_factions_begin, rebel_factions_end),
#        (faction_slot_eq, ":rebel_faction", slot_faction_state, sfs_inactive_rebellion),
#        (faction_slot_eq, ":rebel_faction", slot_faction_inactive_leader_location, ":center_no"),
#        (faction_get_slot, ":pretender", ":rebel_faction", slot_faction_leader),
#        (party_add_members, ":party_no_to_collect_heroes", ":pretender", 1),
#     (try_end),
#rebellion changes end


  ]),
  # script_get_heroes_attached_to_center_as_prisoner_aux
  # For internal use only
  ("get_heroes_attached_to_center_as_prisoner_aux",
    [
      (store_script_param_1, ":center_no"),
      (store_script_param_2, ":party_no_to_collect_heroes"),
      (party_get_num_prisoner_stacks, ":num_stacks",":center_no"),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_prisoner_stack_get_troop_id, ":stack_troop",":center_no",":i_stack"),
        (troop_is_hero, ":stack_troop"),
        (party_add_members, ":party_no_to_collect_heroes", ":stack_troop", 1),
      (try_end),
      (party_get_num_attached_parties, ":num_attached_parties", ":center_no"),
      (try_for_range, ":attached_party_rank", 0, ":num_attached_parties"),
        (party_get_attached_party_with_rank, ":attached_party", ":center_no", ":attached_party_rank"),
        (call_script, "script_get_heroes_attached_to_center_as_prisoner_aux", ":attached_party", ":party_no_to_collect_heroes"),
      (try_end),
  ]),
  # script_get_heroes_attached_to_center_as_prisoner
  # Input: arg1 = center_no, arg2 = party_no_to_collect_heroes
  # Output: none, adds heroes to the party_no_to_collect_heroes party
  ("get_heroes_attached_to_center_as_prisoner",
    [
      (store_script_param_1, ":center_no"),
      (store_script_param_2, ":party_no_to_collect_heroes"),
      (party_clear, ":party_no_to_collect_heroes"),
      (call_script, "script_get_heroes_attached_to_center_as_prisoner_aux", ":center_no", ":party_no_to_collect_heroes"),
  ]),
  # script_give_center_to_faction
  # Input: arg1 = center_no, arg2 = faction
  ("give_center_to_faction",
    [
      (store_script_param_1, ":center_no"),
      (store_script_param_2, ":faction_no"),

      ##diplomacy begin
      (party_set_slot, ":center_no", dplmc_slot_center_taxation, 0),
      (try_begin),
        (party_slot_eq, ":center_no", slot_village_infested_by_bandits, "trp_peasant_woman"),
        (party_set_slot, ":center_no", slot_village_infested_by_bandits, 0),
      (try_end),
      (try_begin),
        (eq, "$g_constable_training_center", ":center_no"),
        (assign, "$g_constable_training_center", -1),
      (try_end),
      ##diplomacy end      
      (try_begin),
        (eq, ":faction_no", "fac_player_supporters_faction"),        
        (faction_get_slot, ":player_faction_king", "fac_player_supporters_faction", slot_faction_leader),
        (eq, ":player_faction_king", "trp_player"),
        
        (try_begin),
          (is_between, ":center_no", walled_centers_begin, walled_centers_end),
          (assign, ":number_of_walled_centers_players_kingdom_has", 1),
        (else_try),
          (assign, ":number_of_walled_centers_players_kingdom_has", 0),
        (try_end),
        
        (try_for_range, ":walled_center", walled_centers_begin, walled_centers_end),
          (store_faction_of_party, ":owner_faction_no", ":walled_center"),
          (eq, ":owner_faction_no", "fac_player_supporters_faction"),          
          (val_add, ":number_of_walled_centers_players_kingdom_has", 1),
        (try_end),
        
        (ge, ":number_of_walled_centers_players_kingdom_has", 10),
        (unlock_achievement, ACHIEVEMENT_VICTUM_SEQUENS),
      (try_end),  
      
      (try_begin),
        (check_quest_active, "qst_join_siege_with_army"),
        (quest_slot_eq, "qst_join_siege_with_army", slot_quest_target_center, ":center_no"),
        (call_script, "script_abort_quest", "qst_join_siege_with_army", 0),
        #Reactivating follow army quest
        (faction_get_slot, ":faction_marshall", "$players_kingdom", slot_faction_marshall),
        (str_store_troop_name_link, s9, ":faction_marshall"),
        (setup_quest_text, "qst_follow_army"),
        (str_store_string, s2, "@{s9} wants you to resume following his army until further notice."),
        (call_script, "script_start_quest", "qst_follow_army", ":faction_marshall"),
        (assign, "$g_player_follow_army_warnings", 0),
      (try_end),

      #(store_faction_of_party, ":old_faction", ":center_no"),
      (call_script, "script_give_center_to_faction_aux", ":center_no", ":faction_no"),
      (call_script, "script_update_village_market_towns"),

      (try_for_range, ":cur_faction", kingdoms_begin, kingdoms_end),
        (call_script, "script_faction_recalculate_strength", ":cur_faction"),
      (try_end),
      (assign, "$g_recalculate_ais", 1),
	  
	  (try_begin),
        (eq, ":faction_no", "fac_player_supporters_faction"),
		(faction_slot_eq, "fac_player_supporters_faction", slot_faction_state, sfs_inactive),
		(call_script, "script_activate_player_faction", "trp_player"),
	  (try_end),
	  	  
      #(call_script, "script_activate_deactivate_player_faction", ":old_faction"),
      #(try_begin),
      #(eq, ":faction_no", "fac_player_supporters_faction"),
      #(faction_slot_eq, "fac_player_supporters_faction", slot_faction_leader, "trp_player"),
      #(call_script, "script_give_center_to_lord", ":center_no", "trp_player", 0),
	
      #check with Armagan -- what is this here for?
      #(try_for_range, ":cur_village", villages_begin, villages_end),
      #(store_faction_of_party, ":cur_village_faction", ":cur_village"),
      #(eq, ":cur_village_faction", "fac_player_supporters_faction"),
      #(neg|party_slot_eq, ":cur_village", slot_town_lord, "trp_player"),
      #(call_script, "script_give_center_to_lord", ":cur_village", "trp_player", 0),
      #(try_end),
      #(try_end),
    ]),
  # script_give_center_to_faction_aux
  # Input: arg1 = center_no, arg2 = faction
  ("give_center_to_faction_aux",
    [
      (store_script_param_1, ":center_no"),
      (store_script_param_2, ":faction_no"),

      (store_faction_of_party, ":old_faction", ":center_no"),
      (party_set_faction, ":center_no", ":faction_no"),

      (try_begin),
        (party_slot_eq, ":center_no", slot_party_type, spt_village),
        (party_get_slot, ":farmer_party", ":center_no", slot_village_farmer_party),
        (gt, ":farmer_party", 0),
        (party_is_active, ":farmer_party"),
        (party_set_faction, ":farmer_party", ":faction_no"),
      (try_end),

      (try_begin),
	    #This bit of seemingly redundant code (the neq condition) is designed to prevent a bug that occurs when a player first conquers a center -- apparently this script is called again AFTER it is handed to a lord
		#Without this line, then the player's dialog selection does not have any affect, because town_lord is set again to stl_unassigned after the player makes his or her choice
	    (neq, ":faction_no", ":old_faction"),
		##diplomacy start+
		(party_get_slot, ":old_ex_faction", ":center_no", slot_center_ex_faction),
		##diplomacy end+		
        (party_set_slot, ":center_no", slot_center_ex_faction, ":old_faction"),
        (party_get_slot, ":old_town_lord", ":center_no", slot_town_lord),
		##diplomacy start+
		(store_current_hours, ":hours"),
		(party_get_slot, ":old_ex_lord", ":center_no", dplmc_slot_center_ex_lord),
		#(party_get_slot, ":old_last_transfer", ":center_no", dplmc_slot_center_last_transfer_time),
		(try_begin),
			#When a faction regains a lost fief, if the ex-lord is a member of that faction,
			#don't erase that information.
			(this_or_next|party_slot_eq, ":center_no", slot_center_original_faction, ":faction_no"),#Handle several rapid sequential transfers
				(eq, ":old_ex_faction", ":faction_no"),
			(is_between, ":old_ex_lord", heroes_begin, heroes_end),
			(store_faction_of_troop, ":old_ex_lord_faction", ":old_ex_lord"),
			(eq, ":old_ex_lord_faction", ":faction_no"),
		(else_try),
			#Otherwise, if the center had a lord before this transfer, set the
			#ex-lord to the lord losing this.
			(neq, ":old_town_lord", stl_unassigned),
			(ge, ":old_town_lord", 0),
			(this_or_next|ge, ":old_town_lord", 1),#Don't apply to the player at the start of the game
				(gt, ":hours", 0),

			#Don't apply to fiefs lost by the faction leader, except for his "home",
			#and any fiefs with him marked as the original lord.
			(call_script, "script_dplmc_get_troop_standing_in_faction", ":old_town_lord", ":old_faction"),
			(this_or_next|lt, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
			(this_or_next|troop_slot_eq, ":old_faction", slot_troop_home, ":center_no"),
				(party_slot_eq, ":center_no", dplmc_slot_center_original_lord, ":old_town_lord"),

			(party_set_slot, ":center_no", dplmc_slot_center_ex_lord, ":old_town_lord"),
		(try_end),
        (party_set_slot, ":center_no", dplmc_slot_center_last_transfer_time, ":hours"),
        (party_set_slot, ":center_no", slot_town_lord, stl_unassigned),
        (party_set_banner_icon, ":center_no", 0),#Removing banner
        (call_script, "script_update_faction_notes", ":old_faction"),
        #Invalidate old lord's cached center points
        (gt, ":old_town_lord", -1),
        (troop_set_slot, ":old_town_lord", dplmc_slot_troop_center_points_plus_one, 0),
      (try_end),  
      
      (call_script, "script_update_faction_notes", ":faction_no"),
      (call_script, "script_update_center_notes", ":center_no"),
      
      (try_begin),
        (ge, ":old_town_lord", 0),
        (neq, ":faction_no", "fac_player_supporters_faction"),
        (call_script, "script_update_troop_notes", ":old_town_lord"),
      (try_end),

      (try_for_range, ":other_center", centers_begin, centers_end),
        (party_slot_eq, ":other_center", slot_village_bound_center, ":center_no"),
        ##diplomacy start+ Avoid infinite recursion even if some foolish modder (such as myself)
        #has set up bizarre cyclic dependencies
        (store_faction_of_party, ":other_center_faction", ":other_center"),
        ##The "this or next" is so that any weird uses of this function
        ##in Native (to change something to its own faction) will be
        ##replicated.  The reason this works is that all villages have
        ##higher ID numbers than castles or towns.
        (this_or_next|gt, ":other_center", ":center_no"),
        (neq, ":other_center_faction", ":old_faction"),
        ##diplomacy end+
        (call_script, "script_give_center_to_faction_aux", ":other_center", ":faction_no"),
      (try_end),
  ]),
  # script_change_troop_faction
  # Input: arg1 = troop_no, arg2 = faction
  ("change_troop_faction",
    [
      (store_script_param_1, ":troop_no"),
      (store_script_param_2, ":faction_no"),
      (try_begin),
        #Reactivating inactive or defeated faction
        (is_between, ":faction_no", kingdoms_begin, kingdoms_end),
        (neg|faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
        (faction_set_slot, ":faction_no", slot_faction_state, sfs_active),
        #(call_script, "script_store_average_center_value_per_faction"),
      (try_end),

	  #Political ramifications
	  (store_faction_of_troop, ":orig_faction", ":troop_no"),
	  ##diplomacy start+ save these for reference
	  #(faction_get_slot, ":orig_faction_leader", ":orig_faction", slot_faction_leader),
	  (faction_get_slot, ":new_faction_leader", ":faction_no", slot_faction_leader),
	  (try_begin),
		  #Avoid letting heroes get stuck as slto_inactive if petitioners switch away from the player's faction
		  (eq, ":orig_faction", "fac_player_supporters_faction"),
	     (gt, ":troop_no", 0),
	     (troop_is_hero, ":troop_no"),
		  (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_inactive),
		  (this_or_next|is_between, ":troop_no", lords_begin, lords_end),
		  (this_or_next|is_between, ":troop_no", kings_begin, kings_end),
		  (this_or_next|is_between, ":troop_no", pretenders_begin, pretenders_end),
		  (this_or_next|troop_slot_eq, ":troop_no", slot_troop_playerparty_history, dplmc_pp_history_granted_fief),
		     (troop_slot_eq, ":troop_no", slot_troop_playerparty_history, dplmc_pp_history_lord_rejoined),
		  (troop_set_slot, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
	  (try_end),
	  ##diplomacy end+
	  
	  #remove if he is marshal
	  (try_begin),
		(faction_slot_eq, ":orig_faction", slot_faction_marshall, ":troop_no"),
        (call_script, "script_check_and_finish_active_army_quests_for_faction", ":orig_faction"),       

		#No current issue on the agenda
		(try_begin),
			(faction_slot_eq, ":orig_faction", slot_faction_political_issue, 0),
		
			(faction_set_slot, ":orig_faction", slot_faction_political_issue, 1), #Appointment of marshal
			(store_current_hours, ":hours"),
			(val_max, ":hours", 0),
			(faction_set_slot, ":orig_faction", slot_faction_political_issue_time, ":hours"), #Appointment of marshal
			##diplomacy start+ Reset political stance for kingdom ladies as well
			#(try_for_range, ":active_npc", active_npcs_begin, active_npcs_end),##OLD
			(try_for_range, ":active_npc", heroes_begin, heroes_end),##NEW
			##diplomacy end+
				(store_faction_of_troop, ":active_npc_faction", ":active_npc"),
				(eq, ":active_npc_faction", ":orig_faction"),
				(troop_set_slot, ":active_npc", slot_troop_stance_on_faction_issue, -1),
			(try_end),		
			(try_begin),
				(eq, "$players_kingdom", ":orig_faction"),
				(troop_set_slot, "trp_player", slot_troop_stance_on_faction_issue, -1),
			(try_end),		
		(try_end),
		
        (try_begin),
		  (troop_get_slot, ":old_marshall_party", ":troop_no", slot_troop_leaded_party),
          (party_is_active, ":old_marshall_party"),
          (party_set_marshall, ":old_marshall_party", 0),
        (try_end),  

		(faction_set_slot, ":orig_faction", slot_faction_marshall, -1),
	  (try_end),
	  #Removal as marshal ends
	  
	  #Other political ramifications
	  (troop_set_slot, ":troop_no", slot_troop_stance_on_faction_issue, -1),
	  ##diplomacy start+ Support promoted kingdom ladies
	  #(try_for_range, ":active_npc", active_npcs_begin, active_npcs_end),
	  (try_for_range, ":active_npc", heroes_begin, heroes_end),
	  ##diplomacy end+
		(troop_slot_eq, ":active_npc", slot_troop_stance_on_faction_issue, ":troop_no"),
		(troop_set_slot, ":active_npc", slot_troop_stance_on_faction_issue, -1),
	  (try_end),
	  #Political ramifications end
	  
	  
		(try_begin),
			(ge, "$cheat_mode", 1),
			(str_store_troop_name, s4, ":troop_no"),
			(display_message, "@{!}DEBUG - {s4} faction changed in normal faction change"), 
		(try_end),
	  
      (troop_set_faction, ":troop_no", ":faction_no"),
	  ##diplomacy start+
	  ##Don't give lords amnesia about what the player said to recruit them.
	  ##OLD:
      #(troop_set_slot, ":troop_no", slot_troop_recruitment_random, 0),
      #(troop_set_slot, ":troop_no", slot_lord_recruitment_argument, 0),
      #(troop_set_slot, ":troop_no", slot_lord_recruitment_candidate, 0),
      #(troop_set_slot, ":troop_no", slot_troop_promised_fief, 0),
	  ##NEW
	  (try_begin),
		 (eq, ":troop_no", "trp_player"),
		 #Don't change of this for the player.
	  (else_try),
	    (is_between, ":faction_no", kingdoms_begin, kingdoms_end),
		 (this_or_next|eq, ":faction_no", "fac_player_supporters_faction"),
			(eq, ":faction_no", "$players_kingdom"),
		 (ge, ":new_faction_leader", 0),
		 (this_or_next|eq, ":faction_no", "fac_player_supporters_faction"),
		 (this_or_next|eq, ":new_faction_leader", "trp_player"),
		 (this_or_next|troop_slot_eq, ":new_faction_leader", slot_troop_spouse, "trp_player"),
			(troop_slot_eq, "trp_player", slot_troop_spouse, ":new_faction_leader"),
		 #Joined faction that player is ruler or co-ruler of.  Don't forget
		 #any promises received.
		 (troop_set_slot, ":troop_no", slot_troop_recruitment_random, 0),
	  (else_try),
	     #Joined a new faction.  Previous promises moot.
		 (troop_set_slot, ":troop_no", slot_troop_recruitment_random, 0),
		 (troop_set_slot, ":troop_no", slot_lord_recruitment_argument, 0),
		 (troop_set_slot, ":troop_no", slot_lord_recruitment_candidate, 0),
		 (troop_set_slot, ":troop_no", slot_troop_promised_fief, 0),
	  (try_end),
	  ##diplomacy end+

      #Give new title
      (call_script, "script_troop_set_title_according_to_faction", ":troop_no", ":faction_no"),
      
      (try_begin),
        (this_or_next|eq, ":faction_no", "$players_kingdom"),
        (eq, ":faction_no", "fac_player_supporters_faction"),
        (call_script, "script_check_concilio_calradi_achievement"),
      (try_end),

	  #Takes walled centers and dependent villages with him
      (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
        (party_slot_eq, ":center_no", slot_town_lord, ":troop_no"),
        (party_set_faction, ":center_no", ":faction_no"),
        (try_for_range, ":village_no", villages_begin, villages_end),
          (party_slot_eq, ":village_no", slot_village_bound_center, ":center_no"),
          (party_set_faction, ":village_no", ":faction_no"),
          (party_get_slot, ":farmer_party_no", ":village_no", slot_village_farmer_party),
          (try_begin),
            (gt, ":farmer_party_no", 0),
            (party_is_active, ":farmer_party_no"),
            (party_set_faction, ":farmer_party_no", ":faction_no"),
          (try_end),
          (try_begin),
            (party_get_slot, ":old_town_lord", ":village_no", slot_town_lord),
            (neq, ":old_town_lord", ":troop_no"),
            (party_set_slot, ":village_no", slot_town_lord, stl_unassigned),
            ##diplomacy start+ Invalidate old lord's cached center points
            (gt, ":old_town_lord", -1),
            (troop_set_slot, ":old_town_lord", dplmc_slot_troop_center_points_plus_one, 0),
            ##diplomacy end+
          (try_end),
        (try_end),
      (try_end),
	  
	  #Dependant kingdom ladies switch faction
	  (try_for_range, ":kingdom_lady", kingdom_ladies_begin, kingdom_ladies_end),
		##diplomacy start+ This is required if kingdom ladies can be promoted to other roles
        (this_or_next|troop_slot_eq, ":kingdom_lady", slot_troop_occupation, 0),#for prisoners
		   (troop_slot_eq, ":kingdom_lady", slot_troop_occupation, slto_kingdom_lady),
		(store_faction_of_troop, reg0, ":kingdom_lady"),
		(this_or_next|eq, reg0, ":orig_faction"),
		(neg|faction_slot_eq, reg0, slot_faction_state, sfs_active),
		##diplomacy end+
		(call_script, "script_get_kingdom_lady_social_determinants", ":kingdom_lady"),
		(assign, ":closest_male_relative", reg0),
		(assign, ":new_center", reg1),
		
		(eq, ":closest_male_relative", ":troop_no"),
		
		(try_begin),
			(ge, "$cheat_mode", 1),
			(str_store_troop_name, s4, ":kingdom_lady"),
			(display_message, "@{!}DEBUG - {s4} faction changed by guardian moving"), 
		(try_end),
		
		(troop_set_faction, ":kingdom_lady", ":faction_no"),
		(troop_slot_eq, ":kingdom_lady", slot_troop_prisoner_of_party, -1),
		(troop_set_slot, ":kingdom_lady", slot_troop_cur_center, ":new_center"),
	  (try_end),
	  
	  #Remove his control over villages under another fortress
      (try_for_range, ":village_no", villages_begin, villages_end),
        (party_slot_eq, ":village_no", slot_town_lord, ":troop_no"),
        (store_faction_of_party, ":village_faction", ":village_no"),
        (try_begin),
          (neq, ":village_faction", ":faction_no"),
          (party_set_slot, ":village_no", slot_town_lord, stl_unassigned),
          ##diplomacy start+ invalidate cached center points
          (gt, ":old_town_lord", -1),
          (troop_set_slot, ":troop_no", dplmc_slot_troop_center_points_plus_one, 0),
          ##diplomacy end+
        (try_end),
      (try_end),
	  
	  #Free prisoners
      (try_begin),
        (troop_get_slot, ":leaded_party", ":troop_no", slot_troop_leaded_party),
        (gt, ":leaded_party", 0),
        (party_set_faction, ":leaded_party", ":faction_no"),
        (party_get_num_prisoner_stacks, ":num_stacks", ":leaded_party"),
        (try_for_range_backwards, ":troop_iterator", 0, ":num_stacks"),
          (party_prisoner_stack_get_troop_id, ":cur_troop_id", ":leaded_party", ":troop_iterator"),
          (store_troop_faction, ":cur_faction", ":cur_troop_id"),
          (troop_is_hero, ":cur_troop_id"),
          (eq, ":cur_faction", ":faction_no"),
          (call_script, "script_remove_troop_from_prison", ":cur_troop_id"),
          (party_remove_prisoners, ":leaded_party", ":cur_troop_id", 1),
        (try_end),
      (try_end),
	  
	  #Annull all quests of which the lord is giver
	  (try_for_range, ":quest", all_quests_begin, all_quests_end),
		(check_quest_active, ":quest"),
		(quest_slot_eq, ":quest", slot_quest_giver_troop, ":troop_no"),
		
		(str_store_troop_name, s4, ":troop_no"),
		(try_begin),
		  (eq, "$cheat_mode", 1),
  		  (display_message, "str_s4_changing_sides_aborts_quest"),
        (try_end),
		(call_script, "script_abort_quest", ":quest", 0),
	  (try_end),
	  
	  #Boot all lords out of centers whose faction has changed
	  ##diplomacy start+ add check for promoted kingdom ladies
	  #(try_for_range, ":lord_to_move", active_npcs_begin, active_npcs_end),
	  (try_for_range, ":lord_to_move", heroes_begin, heroes_end),
		 (troop_slot_ge, ":lord_to_move", slot_troop_leaded_party, 1),
	  ##diplomacy end+
		(troop_get_slot, ":lord_led_party", ":lord_to_move", slot_troop_leaded_party),
	    (party_is_active, ":lord_led_party"),
		(party_get_attached_to, ":led_party_attached", ":lord_led_party"),
		(is_between, ":led_party_attached", walled_centers_begin, walled_centers_end),
		(store_faction_of_party, ":led_party_faction", ":lord_led_party"),
		(store_faction_of_party, ":attached_party_faction", ":led_party_attached"),
		(neq, ":led_party_faction", ":attached_party_faction"),
		
		(party_detach, ":lord_led_party"),
	  (try_end),
	  
	  #Increase relation with lord in new faction by 5
	  #Or, if player kingdom, make inactive pending confirmation
	  (faction_get_slot, ":faction_liege", ":faction_no", slot_faction_leader),
	  (try_begin),
		(eq, ":faction_liege", "trp_player"),
		(neq, ":troop_no", "$g_talk_troop"),
	    (troop_set_slot, ":troop_no", slot_troop_occupation, slto_inactive), #POSSIBLE REASON 1
	  (else_try),
	   ##diplomacy start+ Add support for promoted ladies
		##OLD:
		#(is_between, ":faction_liege", active_npcs_begin, active_npcs_end),
		#(is_between, ":troop_no", active_npcs_begin, active_npcs_end),
		##NEW:
		(is_between, ":faction_liege", heroes_begin, heroes_end),
		(is_between, ":troop_no", heroes_begin, heroes_end),
		##diplomacy end+
		(call_script, "script_troop_change_relation_with_troop", ":faction_liege", ":troop_no", 5),
		(val_add, "$total_indictment_changes", 5),
	  (try_end),
	  
	  #Break courtship relations
	  (try_begin),
	  	(troop_slot_ge, ":troop_no", slot_troop_spouse, 0),
		#Already married, do nothing
	  (else_try),
		(is_between, ":troop_no", active_npcs_begin, active_npcs_end),
		##diplomacy start+
		#Bug fix: don't do this for pretenders.
		(neg|is_between, ":troop_no", kings_begin, kings_end),
		(neg|is_between, ":troop_no", pretenders_begin, pretenders_end),
		##diplomacy end+
	    (try_for_range, ":love_interest_slot", slot_troop_love_interest_1, slot_troop_love_interests_end),
			(troop_get_slot, ":courted_lady", ":troop_no", ":love_interest_slot"),
            ##diplomacy start+ don't call this for bad values
            (is_between, ":courted_lady", kingdom_ladies_begin, kingdom_ladies_end),
            ##diplomacy end+
			(call_script, "script_courtship_event_lady_break_relation_with_suitor", ":courted_lady", ":troop_no"),
	    (try_end),
		##diplomacy start+
		# Don't call this script for married troops / rulers
		#(call_script, "script_assign_troop_love_interests", ":troop_no"),
		(try_begin),
			(neg|troop_slot_ge, ":troop_no", slot_troop_spouse, 0),
			(neg|is_between, ":troop_no", kings_begin, kings_end),
			(neg|is_between, ":troop_no", pretenders_begin, pretenders_end),
			(call_script, "script_assign_troop_love_interests", ":troop_no"),
		(try_end),
		##diplomacy end+
	  (else_try),	
		(is_between, ":troop_no", kingdom_ladies_begin, kingdom_ladies_end),
		(try_for_range, ":active_npc", active_npcs_begin, active_npcs_end),
			(try_for_range, ":love_interest_slot", slot_troop_love_interest_1, slot_troop_love_interests_end),
				(troop_slot_eq, ":active_npc", ":love_interest_slot", ":troop_no"),
				(call_script, "script_courtship_event_lady_break_relation_with_suitor", ":troop_no", ":active_npc"),
			(try_end),
		(try_end),
	  (try_end),
	  
	  #Stop raidings/sieges of new faction's fief if there is any
	  (troop_get_slot, ":troop_party", ":troop_no", slot_troop_leaded_party),
	  (try_for_range, ":center_no", centers_begin, centers_end),
	    (party_slot_eq, ":center_no", slot_party_type, spt_village),
	    (party_get_slot, ":raided_by", ":center_no", slot_village_raided_by),	    
	    (eq, ":raided_by", ":troop_party"),
	    (party_set_slot, ":center_no", slot_village_raided_by, -1),
	    (try_begin),
	      (party_slot_eq, ":center_no", slot_village_state, svs_being_raided),	      
	      (party_set_slot, ":center_no", slot_village_state, svs_normal),
	      (party_set_extra_text, ":center_no", "str_empty_string"),
	    (try_end),
	  (else_try),  	    
	    (party_get_slot, ":besieged_by", ":center_no", slot_center_is_besieged_by),
	    (eq, ":besieged_by", ":troop_party"),
	    (party_set_slot, ":center_no", slot_center_is_besieged_by, -1),
	    (try_begin),	    
	      (party_slot_eq, ":center_no", slot_village_state, svs_under_siege),	      
	      (party_set_slot, ":center_no", slot_village_state, svs_normal),
	      (party_set_extra_text, ":center_no", "str_empty_string"),
	    (try_end),
	  (try_end),
	  	  
      (call_script, "script_update_all_notes"),

      (call_script, "script_update_village_market_towns"),
      (assign, "$g_recalculate_ais", 1),
      ]),
  # script_troop_set_title_according_to_faction
  # Input: arg1 = troop_no, arg2 = faction_no
  # EDITED FROM NATIVE TO ALLOW CUSTOM PLAYER KINGDOM TITLES
  ("troop_set_title_according_to_faction",
    [
      (store_script_param, ":troop_no", 1),
      (store_script_param, ":faction_no", 2),
      ##diplomacy start+
	  # OLD CODE:
      #(try_begin),
      #  (is_between, ":faction_no", kingdoms_begin, kingdoms_end),
      #  (str_store_troop_name_plural, s0, ":troop_no"),
      #  (troop_get_type, ":gender", ":troop_no"),
      #  (store_sub, ":title_index", ":faction_no", kingdoms_begin),
      #  (try_begin),
      #    (eq, ":gender", 0), #male
      #    (val_add, ":title_index", kingdom_titles_male_begin),
      #  (else_try),
      #    (val_add, ":title_index", kingdom_titles_female_begin),
      #  (try_end),
      #  (str_store_string, s1, ":title_index"),
      #  (troop_set_name, ":troop_no", s1),
      #  (troop_get_slot, ":troop_party", ":troop_no", slot_troop_leaded_party),
      #  (gt, ":troop_party", 0),
      #  (str_store_troop_name, s5, ":troop_no"),
      #  (party_set_name, ":troop_party", "str_s5_s_party"),
      #(try_end),
	  #
	  # NEW CODE:
	  (assign, ":save_reg0", 0),
	  (assign, ":custom_name", 0),
      (try_begin),
	    #Don't do anything when given a bad value.
		 #
		 #We could restrict this further, checking whether the troop is a hero,
		 #or whether it's between heroes_begin and heroes_end, but there are
		 #legitimate reasons a coder may want to run this to get a temporary value,
		 #or use this with temporary heroes, or so forth.
		 #
		 #However, some things are unambiguously errors:
		 (this_or_next|lt, ":troop_no", 0),# At best, the rename operation would fail.
		 (this_or_next|eq, ":troop_no", "trp_heroes_end"),# This is used to store custom titles, so applying a title to this will mess them up.
		 (this_or_next|eq, ":troop_no", "trp_kingdom_heroes_including_player_begin"),#This could easily end up changed due to carelessness
		 #There is also no legitimate reason to try to give the titles to generic soldiers.
		 (is_between, ":troop_no", soldiers_begin, soldiers_end),
	  ##Custom player kingdom vassal titles, credit Caba`drin start
	  #(Updated 2011-04-24, to use Caba`drin's 2011-04-20 bug-fix and update)
	  # See http://forums.taleworlds.com/index.php/topic,148259.0.html
      (else_try),
		(call_script, "script_dplmc_store_troop_is_female", ":troop_no"),#<- dplmc+ altered
		(assign, ":troop_is_female", reg0),
		##Additional alteration start
		#All Rhodok benefactor / custodian NPCs insist on the name "Tribune"
		#Currently this is just Bunduk, but others could be added.
		(try_begin),
			(str_store_troop_name, s1, ":troop_no"),#s1 is overwritten below
			#For dialogue reasons, this should be enabled even when the player
			#is co-ruler of an NPC kingdom.
			(this_or_next|eq, ":faction_no", "fac_player_supporters_faction"),
				(eq, ":faction_no", "$players_kingdom"),
			(this_or_next|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_benefactor),
				(troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_custodian),
			(troop_slot_eq, ":troop_no", slot_troop_original_faction, "fac_kingdom_5"),
			(assign, ":is_coruler", 0),
			(try_begin),
				(is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
				(faction_get_slot, ":faction_leader", ":faction_no", slot_faction_leader),
				(gt, ":faction_leader", -1),
				(this_or_next|eq, ":faction_leader", "trp_player"),
				(this_or_next|troop_slot_eq, "trp_player", slot_troop_spouse, ":faction_leader"),
					(troop_slot_eq, ":faction_leader", slot_troop_spouse, "trp_player"),
				(assign, ":is_coruler", 1),
			(try_end),
			(this_or_next|eq, ":is_coruler", 1),
				(eq, ":faction_no", "fac_player_supporters_faction"),
			(str_store_string, s0, "@Tribune"),
			(str_store_troop_name_plural, s1, ":troop_no"),
			(str_store_string, s1, "str_s0_s1"),
		##Additional alteration end
		(else_try),
            (eq, ":faction_no", "fac_player_supporters_faction"),
            #(troop_get_type, ":gender", ":troop_no"),#<- dplmc+ altered (use script for gender instead)
            (try_begin),
              (eq, ":troop_is_female", 0), #male #<- dplmc+ altered
              (troop_slot_eq, "trp_heroes_end", 0, 1),
              (str_store_troop_name, s0, "trp_heroes_end"),
              (str_store_troop_name_plural, s1, ":troop_no"),
              (str_store_string, s1, "str_s0_s1"),
              (assign, ":custom_name", 1),
            (else_try),
              (troop_slot_eq, "trp_heroes_end", 1, 1),
              (str_store_troop_name_plural, s0, "trp_heroes_end"),
              (str_store_troop_name_plural, s1, ":troop_no"),
              (str_store_string, s1, "str_s0_s1"),
              (assign, ":custom_name", 1),
            (try_end),
            (eq, ":custom_name", 1), #So if it fails, will rename normally
        (else_try),
            (is_between, ":faction_no", kingdoms_begin, kingdoms_end),
			##Additional section begin: add support for player kingdom culture
			(try_begin),
				(eq, ":faction_no", "fac_player_supporters_faction"),
				(is_between, "$g_player_culture", npc_kingdoms_begin, npc_kingdoms_end),
				(assign, ":faction_no", "$g_player_culture"),#<- Use title from culture if one is set, and not using custom titles
			(try_end),
			##Additional section end
            (str_store_troop_name_plural, s0, ":troop_no"),
            #(troop_get_type, ":gender", ":troop_no"),#<- dplmc+ altered
            (store_sub, ":title_index", ":faction_no", kingdoms_begin),
            (try_begin),
              (eq, ":troop_is_female", 0), #<- dplmc+ altered
              (val_add, ":title_index", kingdom_titles_male_begin),
            (else_try),
              (val_add, ":title_index", kingdom_titles_female_begin),
            (try_end),
            (str_store_string, s1, ":title_index"),
        (try_end),
        (troop_set_name, ":troop_no", s1),
        (troop_get_slot, ":troop_party", ":troop_no", slot_troop_leaded_party),
        (gt, ":troop_party", 0),
        (str_store_troop_name, s5, ":troop_no"),
        (party_set_name, ":troop_party", "str_s5_s_party"),
      (try_end),
      ##Custom player kingdom vassal titles, credit Caba'drin end
	  (assign, reg0, ":save_reg0"),
      ##diplomacy end+
      ]),
  # script_give_center_to_lord
  # Input: arg1 = center_no, arg2 = lord_troop, arg3 = add_garrison_to_center
  ("give_center_to_lord",
    [
      (store_script_param, ":center_no", 1),
      (store_script_param, ":lord_troop_id", 2), #-1 only in the case of a player deferring ownership of a center
      (store_script_param, ":add_garrison", 3),
      ##diplomacy begin
      (party_set_slot, ":center_no", dplmc_slot_center_taxation, 0),
      (try_begin),
        (party_slot_eq, ":center_no", slot_village_infested_by_bandits, "trp_peasant_woman"),
        (party_set_slot, ":center_no", slot_village_infested_by_bandits, 0),
      (try_end),
      ##diplomacy end

	  ##diplomacy start+
	  #For relation changes below, store all heroes' center points and closest fiefs.
	  (call_script, "script_dplmc_prepare_hero_center_points_ignoring_center", ":center_no"),

	  #(assign, ":player_declines_honor", 0),
	  #(try_begin),
	  #	  (gt, "$g_dont_give_fief_to_player_days", 1),
	  #	  (assign, ":player_declines_honor", 1),
	  #(try_end),
	  ##diplomacy end+

	  (try_begin),
	  ##diplomacy start+ notable events like this should be logged by default
      (store_current_hours, ":hours"),
      (ge, ":hours", 1),#Don't spam the game log during world setup
	   (ge, ":lord_troop_id", 0),
		(str_store_party_name_link, s4, ":center_no"),
		(str_store_troop_name_link, s5, ":lord_troop_id"),
		(store_troop_faction, ":msg_faction_no", ":lord_troop_id"),
		(str_store_faction_name_link, s7, ":msg_faction_no"),
		(try_begin),
		   (faction_slot_eq, ":msg_faction_no", slot_faction_leader, ":lord_troop_id"),
		   (display_log_message, "@{s5} of the {s7} has taken ownership of {s4}."),
		(else_try),
		   (display_log_message, "@{s4} has been awarded to {s5} of the {s7}."),
		(try_end),
	  (else_try),
	  ##diplomacy end+
	    (eq, "$cheat_mode", 1),
		(ge, ":lord_troop_id", 0),
		(str_store_party_name, s4, ":center_no"),
		(str_store_troop_name, s5, ":lord_troop_id"),
		(display_message, "@{!}DEBUG -- {s4} awarded to {s5}"),
	  (try_end),
	  
	  (try_begin),
	    (eq, ":lord_troop_id", "trp_player"),
	    (unlock_achievement, ACHIEVEMENT_ROYALITY_PAYMENT),
	    
	    (assign, ":number_of_fiefs_player_have", 1),
	    (try_for_range, ":cur_center", centers_begin, centers_end),
	      (neq, ":cur_center", ":center_no"),
	      (party_slot_eq, ":cur_center", slot_town_lord, "trp_player"),
	      (val_add, ":number_of_fiefs_player_have", 1),
	    (try_end),
	    
	    (ge, ":number_of_fiefs_player_have", 5),
	    (unlock_achievement, ACHIEVEMENT_MEDIEVAL_EMLAK),	    
	  (try_end),
	  
      (party_get_slot, ":old_lord_troop_id", ":center_no", slot_town_lord),
      
	  (try_begin), #This script is ONLY called with lord_troop_id = -1 when it is the player faction 
	  ##diplomacy start+
	  #The player can now also be co-ruler of a NPC kingdom.
         (eq, ":lord_troop_id", -1),

		 (is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
		 (faction_get_slot, ":players_kingdom_liege", "$players_kingdom", slot_faction_leader),
		 (gt, ":players_kingdom_liege", -1),
		 (this_or_next|eq, ":players_kingdom_liege", "trp_player"),
		 (this_or_next|troop_slot_eq, ":players_kingdom_liege", slot_troop_spouse, "trp_player"),
			(troop_slot_eq, "trp_player", slot_troop_spouse, ":players_kingdom_liege"),

		(assign, ":lord_troop_faction", "$players_kingdom"),
		(party_set_banner_icon, ":center_no", 0),#Removing banner
	  (else_try),
	  ##diplomacy end+
	    (eq, ":lord_troop_id", -1),
	    (assign, ":lord_troop_faction", "fac_player_supporters_faction"),
        (party_set_banner_icon, ":center_no", 0),#Removing banner
		
      (else_try),	
	    (eq, ":lord_troop_id", "trp_player"),
	    (assign, ":lord_troop_faction", "$players_kingdom"), #was changed on Apr 27 from fac_plyr_sup_fac

      (else_try),	  
		(store_troop_faction, ":lord_troop_faction", ":lord_troop_id"),
	  (try_end),	
	  (faction_get_slot, ":faction_leader", ":lord_troop_faction", slot_faction_leader),

	  (try_begin),
	    (eq, ":faction_leader", "trp_player"),

        (try_begin),
            (troop_get_type, ":is_female", "trp_player"),
            (eq, ":is_female", 1),
            (unlock_achievement, ACHIEVEMENT_QUEEN),
        (try_end),
	  (try_end),
	  
	  (try_begin),
		(eq, ":faction_leader", ":old_lord_troop_id"),
		(call_script, "script_add_log_entry", logent_liege_grants_fief_to_vassal, ":faction_leader", ":center_no", ":lord_troop_id", ":lord_troop_faction"),
        (troop_set_slot, ":lord_troop_id", slot_troop_promised_fief, 0),		
	  (try_end),

      (try_begin),
	    (eq, ":lord_troop_id", -1), #Lord troop ID -1 is only used when a player is deferring assignment of a fief
        (party_set_faction, ":center_no", "$players_kingdom"),
	  (else_try),
        (eq, ":lord_troop_id", "trp_player"),
        (gt, "$players_kingdom", 0),
        (party_set_faction, ":center_no", "$players_kingdom"),
      (else_try),
        (eq, ":lord_troop_id", "trp_player"),
        (neg|is_between, "$players_kingdom", kingdoms_begin, kingdoms_end),
        (party_set_faction, ":center_no", "fac_player_supporters_faction"),
      (else_try),
        (party_set_faction, ":center_no", ":lord_troop_faction"),
      (try_end),
      (party_set_slot, ":center_no", slot_town_lord, ":lord_troop_id"),

      (try_begin),
        (party_slot_eq, ":center_no", slot_party_type, spt_village),
        (party_get_slot, ":farmer_party_no", ":center_no", slot_village_farmer_party),
        (gt, ":farmer_party_no", 0),
        (party_is_active, ":farmer_party_no"),
        (store_faction_of_party, ":center_faction", ":center_no"),
        (party_set_faction, ":farmer_party_no", ":center_faction"),
      (try_end),

    (try_begin),
        (this_or_next|party_slot_eq, ":center_no", slot_party_type, spt_town),
			(party_slot_eq, ":center_no", slot_party_type, spt_castle),
		(gt, ":lord_troop_id", -1),
		
#normal_banner_begin
        (troop_get_slot, ":cur_banner", ":lord_troop_id", slot_troop_banner_scene_prop),
        (try_begin),
       (gt, ":cur_banner", 0),
      (val_sub, ":cur_banner", banner_scene_props_begin),
       (ge, ":cur_banner", 0),
      (val_add, ":cur_banner", banner_map_icons_begin),
       (party_set_banner_icon, ":center_no", ":cur_banner"),
        (else_try),
       (party_set_banner_icon, ":center_no", 0),
      (try_end),
# custom_banner_begin
#        (troop_get_slot, ":flag_icon", ":lord_troop_id", slot_troop_custom_banner_map_flag_type),
#        (ge, ":flag_icon", 0),
#        (val_add, ":flag_icon", custom_banner_map_icons_begin),
#        (party_set_banner_icon, ":center_no", ":flag_icon"),
    (try_end),

#    (try_begin),
#		(eq, 1, 0),
 #       (eq, ":lord_troop_id", "trp_player"),
 #       (neq, ":old_lord_troop_id", "trp_player"),
 #       (party_get_slot, ":center_relation", ":center_no", slot_center_player_relation),
 #       (is_between, ":center_relation", -4, 5),
 #       (call_script, "script_change_player_relation_with_center", ":center_no", 5),
 #       (gt, ":old_lord_troop_id", 0),
 #       (call_script, "script_change_player_relation_with_troop", ":old_lord_troop_id", -25),
 #   (try_end),
	(try_begin),
		(gt, ":lord_troop_id", -1),
		(call_script, "script_update_troop_notes", ":lord_troop_id"),
	(try_end),
	
    (call_script, "script_update_center_notes", ":center_no"),
    
    (try_begin),
      (gt, ":lord_troop_faction", 0),
      (call_script, "script_update_faction_notes", ":lord_troop_faction"),
    (try_end),  
    
    (try_begin),
        (ge, ":old_lord_troop_id", 0),
        (call_script, "script_update_troop_notes", ":old_lord_troop_id"),
        (store_troop_faction, ":old_lord_troop_faction", ":old_lord_troop_id"),
        (call_script, "script_update_faction_notes", ":old_lord_troop_faction"),
    (try_end),

    (try_begin),
        (eq, ":add_garrison", 1),
        (this_or_next|party_slot_eq, ":center_no", slot_party_type, spt_town),
			(party_slot_eq, ":center_no", slot_party_type, spt_castle),
        (assign, ":garrison_strength", 3), 
        (try_begin),
          (party_slot_eq, ":center_no", slot_party_type, spt_town),
          (assign, ":garrison_strength", 9),
        (try_end),
        (try_for_range, ":unused", 0, ":garrison_strength"),
          (call_script, "script_cf_reinforce_party", ":center_no"),
        (try_end),
        ## ADD some XP initially
        (try_for_range, ":unused", 0, 7),
          (store_mul, ":xp_range_min", 150, ":garrison_strength"),
          (store_mul, ":xp_range_max", 200, ":garrison_strength"),
          (store_random_in_range, ":xp", ":xp_range_min", ":xp_range_max"),
          (party_upgrade_with_xp, ":center_no", ":xp", 0),
        (try_end),
    (try_end),

	(faction_get_slot, ":faction_leader", ":lord_troop_faction", slot_faction_leader),
	(store_current_hours, ":hours"),
	
	#the next block handles gratitude, objections and jealousies
	(try_begin),
	  	(gt, ":hours", 0),
		(gt, ":lord_troop_id", 0),
		
    	(call_script, "script_troop_change_relation_with_troop", ":lord_troop_id", ":faction_leader", 10),
		(val_add, "$total_promotion_changes", 10),
		
		#smaller factions are more dramatically influenced by internal jealousies
		#Disabled as of NOV 2010
#		(try_begin),
#			(neg|faction_slot_ge, ":lord_troop_faction", slot_faction_number_of_parties, 4),
#			(assign, ":faction_size_multiplier", 6),
#		(else_try),
#			(neg|faction_slot_ge, ":lord_troop_faction", slot_faction_number_of_parties, 8),
#			(assign, ":faction_size_multiplier", 5),
#		(else_try),
#			(neg|faction_slot_ge, ":lord_troop_faction", slot_faction_number_of_parties, 16),
#			(assign, ":faction_size_multiplier", 4),
#		(else_try),
#			(neg|faction_slot_ge, ":lord_troop_faction", slot_faction_number_of_parties, 32),
#			(assign, ":faction_size_multiplier", 3),
#		(else_try),	
#			(assign, ":faction_size_multiplier", 2),
#		(try_end),
		
		#factional politics -- each lord in the faction adjusts his relation according to the relation with the lord receiving the faction
		##diplomacy start+ add support for kingdom ladies
		#(try_for_range, ":other_lord", active_npcs_begin, active_npcs_end),
		(try_for_range, ":other_lord", heroes_begin, heroes_end),
		##diplomacy end+
			(troop_slot_eq, ":other_lord", slot_troop_occupation, slto_kingdom_hero),
			(neq, ":other_lord", ":lord_troop_id"),
			
		    (store_troop_faction, ":other_troop_faction", ":other_lord"),
		    (eq, ":lord_troop_faction", ":other_troop_faction"),

		    (neq, ":other_lord", ":faction_leader"),
			
	        (call_script, "script_troop_get_relation_with_troop", ":other_lord", ":lord_troop_id"),
			(assign, ":relation_with_troop", reg0),

			#relation reduction = relation/10 minus 2. So,0 = -2, 8 = -1, 16+ = no change or bonus, 24+ gain one point
		    (store_div, ":relation_with_liege_change", ":relation_with_troop", 8), #changed from 16
		    (val_sub, ":relation_with_liege_change", 2),

		    (val_clamp, ":relation_with_liege_change", -5, 3),
			
			(try_begin),
				#upstanding and goodnatured lords will not lose relation unless they actively dislike the other lord
				(this_or_next|troop_slot_eq, ":other_lord", slot_lord_reputation_type, lrep_upstanding),
				 ##diplomacy start+ add companion/lady personality types
				 (this_or_next|troop_slot_eq, ":other_lord", slot_lord_reputation_type, lrep_benefactor),
				 (this_or_next|troop_slot_eq, ":other_lord", slot_lord_reputation_type, lrep_conventional),
				 (this_or_next|troop_slot_eq, ":other_lord", slot_lord_reputation_type, lrep_moralist),
				 (this_or_next|troop_slot_eq, ":other_lord", slot_lord_reputation_type, lrep_otherworldly),
				 ##diplomacy end+
					(troop_slot_eq, ":other_lord", slot_lord_reputation_type, lrep_goodnatured),
				(ge, ":relation_with_troop", 0),
				(val_max, ":relation_with_liege_change", 0),
			(else_try),
				#penalty is increased for lords who have the more unpleasant reputation types
				(this_or_next|troop_slot_eq, ":other_lord", slot_lord_reputation_type, lrep_selfrighteous),
				(this_or_next|troop_slot_eq, ":other_lord", slot_lord_reputation_type, lrep_debauched),
					(troop_slot_eq, ":other_lord", slot_lord_reputation_type, lrep_quarrelsome),
				(lt, ":relation_with_liege_change", 0),
				(val_mul, ":relation_with_liege_change", 3),
				(val_div, ":relation_with_liege_change", 2),
			(try_end),
			##diplomacy start+

			#TODO (idea for "high"): instead of being absolute, the sliding score system should be used.
			#(So you can use a score instead of using relations.)  The greater the
			#difference in score, the greater the relation loss -- so if the lord
			#was nearly indifferent between two candidates, the difference would be
			#lesser.
			(try_begin),
				(ge, "$g_dplmc_ai_changes", DPLMC_AI_CHANGES_MEDIUM),
				(try_begin),
					#Optional change: Non-jerkish lords will not object to giving a village to
					#someone fiefless, unless they dislike him.
					(neg|troop_slot_eq, ":other_lord", slot_lord_reputation_type, lrep_debauched),
					(neg|troop_slot_eq, ":other_lord", slot_lord_reputation_type, lrep_selfrighteous),
					(neg|troop_slot_eq, ":other_lord", slot_lord_reputation_type, lrep_quarrelsome),
					(lt, ":relation_with_liege_change", 0),
					(is_between, ":center_no", villages_begin, villages_end),
					(troop_slot_eq, ":lord_troop_id", slot_troop_temp_slot, 0),
					(ge, ":relation_with_troop", 0),
					(val_max, ":relation_with_liege_change", 0),
				(try_end),
				(try_begin),
					#Optional change: because taking a penalty for 'thrashing' the same fief
					#back and forth is silly, if you're giving the fief back to the lord who
					#last had it, reduce any penalty.
					(lt, ":relation_with_liege_change", 0),
					(party_slot_eq, ":center_no", dplmc_slot_center_ex_lord, ":lord_troop_id"),
					(neq, ":lord_troop_id", 0),
					(val_add, ":relation_with_liege_change", 1),

					#If the other lord doesn't have any claim of his own on the center,
					#attenuate the penalty more.
					(lt, ":relation_with_liege_change", 0),
					(ge, ":relation_with_troop", 0),
					(neg|party_slot_eq, ":center_no", dplmc_slot_center_original_lord, ":other_lord"),
					(neg|troop_slot_eq, ":other_lord", slot_troop_home, ":center_no"),
					(this_or_next|neg|troop_slot_ge, ":other_lord", slot_troop_stance_on_faction_issue, 0),
						(neg|party_slot_eq, ":center_no", slot_center_last_taken_by_troop, ":other_lord"),
					(val_add, ":relation_with_liege_change", 1),
				(else_try),
					#Similar logic, but for "original lord" instead of most recent lord
					(lt, ":relation_with_liege_change", 0),
					(neg|party_slot_eq, ":center_no", dplmc_slot_center_ex_lord, ":lord_troop_id"),#don't apply this if the above "ex-center" check was applied
					(this_or_next|party_slot_eq, ":center_no", dplmc_slot_center_original_lord, ":lord_troop_id"),
						(troop_slot_eq, ":lord_troop_id", slot_troop_home, ":center_no"),

					#Only attenuate the panelty if the other lord doesn't have any claim of his own on the center
					(ge, ":relation_with_troop", 0),
					(neg|troop_slot_eq, ":other_lord", slot_troop_home, ":center_no"),
					(neg|party_slot_eq, ":center_no", dplmc_slot_center_original_lord, ":other_lord"),
					(neg|party_slot_eq, ":center_no", dplmc_slot_center_ex_lord, ":other_lord"),
					(this_or_next|neg|troop_slot_ge, ":other_lord", slot_troop_stance_on_faction_issue, 0),
						(neg|party_slot_eq, ":center_no", slot_center_last_taken_by_troop, ":other_lord"),

					(val_add, ":relation_with_liege_change", 1),
				(try_end),
				(try_begin),
					#On the minus side, lords whose homes and/or original fiefs are not
					#disposed according to their wishes are that much more cross.
					(lt, ":relation_with_liege_change", 1),
					(this_or_next|party_slot_eq, ":center_no", dplmc_slot_center_ex_lord, ":other_lord"),
					(this_or_next|party_slot_eq, ":center_no", dplmc_slot_center_original_lord, ":other_lord"),
					   (troop_slot_eq, ":other_lord", slot_troop_home, ":center_no"),
					(val_sub, ":relation_with_liege_change", 1),
				(else_try),
					#Optional change: martial lords are less displeased by awarding a fief to
					#the one who conquered it.
					(lt, ":relation_with_liege_change", 0),
					(party_slot_eq, ":center_no", slot_center_last_taken_by_troop, ":lord_troop_id"),
					(this_or_next|troop_slot_eq, ":other_lord", slot_lord_reputation_type, lrep_upstanding),
					(troop_slot_eq, ":other_lord", slot_lord_reputation_type, lrep_martial),
					(val_add, ":relation_with_liege_change", 1),
				(try_end),
			(try_end),
			##diplomacy end+
			
		    (neq, ":relation_with_liege_change", 0),
			#removed Nov 2010
#		  	(val_mul, ":relation_reduction", ":faction_size_multiplier"),
#		  	(val_div, ":relation_reduction", 2),
			#removed Nov 2010
			
			(try_begin),
				(troop_slot_eq, ":other_lord", slot_troop_stance_on_faction_issue, ":lord_troop_id"),
				(val_add, ":relation_with_liege_change", 1),
				(val_max, ":relation_with_liege_change", 1),
			(try_end),
			
 	        (call_script, "script_troop_change_relation_with_troop", ":other_lord", ":faction_leader", ":relation_with_liege_change"),
			(val_add, "$total_promotion_changes", ":relation_with_liege_change"),
			
		    (try_begin),
				(this_or_next|le, ":relation_with_liege_change", -4), #Nov 2010 - changed from -8
				(this_or_next|troop_slot_eq, ":other_lord", slot_troop_promised_fief, 1), #1 is any fief
					(troop_slot_eq, ":other_lord", slot_troop_promised_fief, ":center_no"),
				(call_script, "script_add_log_entry", logent_troop_feels_cheated_by_troop_over_land, ":other_lord", ":center_no", ":lord_troop_id", ":lord_troop_faction"),
		    (try_end),
		  
		(try_end),
	(try_end),
	
	##diplomacy start+ invalidate cached center points
	(try_begin),
		(neq, ":old_lord_troop_id", ":lord_troop_id"),
		(try_begin),
			(gt, ":old_lord_troop_id", -1),
			(troop_set_slot, ":old_lord_troop_id", dplmc_slot_troop_center_points_plus_one, 0),
		(try_end),
		(try_begin),
			(gt, ":lord_troop_id", -1),
			(troop_set_slot, ":lord_troop_id", dplmc_slot_troop_center_points_plus_one, 0),
		(try_end),
	(try_end),
	##diplomacy end+
	
	#Villages from another faction will also be transferred along with a fortress
    (try_begin),
		(is_between, ":center_no", walled_centers_begin, walled_centers_end),
        (try_for_range, ":cur_village", villages_begin, villages_end),
			(party_slot_eq, ":cur_village", slot_village_bound_center, ":center_no"),
			(store_faction_of_party, ":cur_village_faction", ":cur_village"),
			(neq, ":cur_village_faction", ":lord_troop_faction"),
			
			(call_script, "script_give_center_to_lord", ":cur_village", ":lord_troop_id", 0),
        (try_end),
    (try_end),       
  ]),
  # script_get_number_of_hero_centers
  # Input: arg1 = troop_no
  # Output: reg0 = number of centers that are ruled by the hero
  ("get_number_of_hero_centers",
    [
      (store_script_param_1, ":troop_no"),
      (assign, ":result", 0),
      (try_for_range, ":center_no", centers_begin, centers_end),
        (party_slot_eq, ":center_no", slot_town_lord, ":troop_no"),
        (val_add, ":result", 1),
      (try_end),
      (assign, reg0, ":result"),
  ]),
  # script_cf_get_random_enemy_center
  # Input: arg1 = party_no
  # Output: reg0 = center_no
  ("cf_get_random_enemy_center",
    [
      (store_script_param_1, ":party_no"),
      
      (assign, ":result", -1),
      (assign, ":total_enemy_centers", 0),
      (store_faction_of_party, ":party_faction", ":party_no"),
      
      (try_for_range, ":center_no", centers_begin, centers_end),
        (store_faction_of_party, ":center_faction", ":center_no"),
        (store_relation, ":party_relation", ":center_faction", ":party_faction"),
        (lt, ":party_relation", 0),
        (val_add, ":total_enemy_centers", 1),
      (try_end),

      (gt, ":total_enemy_centers", 0),
      (store_random_in_range, ":random_center", 0, ":total_enemy_centers"),
      (assign, ":total_enemy_centers", 0),
      (try_for_range, ":center_no", centers_begin, centers_end),
        (eq, ":result", -1),
        (store_faction_of_party, ":center_faction", ":center_no"),
        (store_relation, ":party_relation", ":center_faction", ":party_faction"),
        (lt, ":party_relation", 0),
        (val_sub, ":random_center", 1),
        (lt, ":random_center", 0),
        (assign, ":result", ":center_no"),
      (try_end),
      (assign, reg0, ":result"),
  ]),
  # script_find_travel_location
  # Input: arg1 = center_no
  # Output: reg0 = new_center_no (to travel within the same faction)
  ("find_travel_location",
    [
      (store_script_param_1, ":center_no"),
      (store_faction_of_party, ":faction_no", ":center_no"),
      (assign, ":total_weight", 0),
      (try_for_range, ":cur_center_no", centers_begin, centers_end),
        (neq, ":center_no", ":cur_center_no"),
        (store_faction_of_party, ":center_faction_no", ":cur_center_no"),
        (eq, ":faction_no", ":center_faction_no"),
        
        (store_distance_to_party_from_party, ":cur_distance", ":center_no", ":cur_center_no"),
        (val_add, ":cur_distance", 1),
        
        (assign, ":new_weight", 100000),
        (val_div, ":new_weight", ":cur_distance"),
        (val_add, ":total_weight", ":new_weight"),
      (try_end),
      
      (assign, reg0, -1),
      
      (try_begin),
        (eq, ":total_weight", 0),
      (else_try),
        (store_random_in_range, ":random_weight", 0 , ":total_weight"),
        (assign, ":total_weight", 0),
        (assign, ":done", 0),
        (try_for_range, ":cur_center_no", centers_begin, centers_end),
          (eq, ":done", 0),
          (neq, ":center_no", ":cur_center_no"),
          (store_faction_of_party, ":center_faction_no", ":cur_center_no"),
          (eq, ":faction_no", ":center_faction_no"),
          
          (store_distance_to_party_from_party, ":cur_distance", ":center_no", ":cur_center_no"),
          (val_add, ":cur_distance", 1),
          
          (assign, ":new_weight", 100000),
          (val_div, ":new_weight", ":cur_distance"),
          (val_add, ":total_weight", ":new_weight"),
          (lt, ":random_weight", ":total_weight"),
          (assign, reg0, ":cur_center_no"),
          (assign, ":done", 1),
        (try_end),
      (try_end),
  ]),
  # script_get_relation_between_parties
  # Input: arg1 = party_no_1, arg2 = party_no_2
  # Output: reg0 = relation between parties
  ("get_relation_between_parties",
    [
      (store_script_param_1, ":party_no_1"),
      (store_script_param_2, ":party_no_2"),
      
      (store_faction_of_party, ":party_no_1_faction", ":party_no_1"),
      (store_faction_of_party, ":party_no_2_faction", ":party_no_2"),
      (try_begin),
        (eq, ":party_no_1_faction", ":party_no_2_faction"),
        (assign, reg0, 100),
      (else_try),
        (store_relation, ":relation", ":party_no_1_faction", ":party_no_2_faction"),
        (assign, reg0, ":relation"),
      (try_end),
  ]),
  # script_calculate_weekly_party_wage
  # Input: arg1 = party_no
  # Output: reg0 = weekly wage
  ("calculate_weekly_party_wage",
    [
      (store_script_param_1, ":party_no"),
      
      (assign, ":result", 0),
      (party_get_num_companion_stacks, ":num_stacks",":party_no"),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop",":party_no",":i_stack"),
        (party_stack_get_size, ":stack_size",":party_no",":i_stack"),
        (call_script, "script_npc_get_troop_wage", ":stack_troop", ":party_no"),
        (assign, ":cur_wage", reg0),
        (val_mul, ":cur_wage", ":stack_size"),
        (val_add, ":result", ":cur_wage"),
      (try_end),
      (assign, reg0, ":result"),
  ]),
  # script_calculate_player_faction_wage
  # Input: arg1 = party_no
  # Output: reg0 = weekly wage
  ("calculate_player_faction_wage",
    [(assign, ":nongarrison_wages", 0),
     (assign, ":garrison_wages", 0),
     (try_for_parties, ":party_no"),
       (assign, ":garrison_troop", 0),
       (try_begin),
         (this_or_next|party_slot_eq, ":party_no", slot_party_type, spt_town),
         (party_slot_eq, ":party_no", slot_party_type, spt_castle),
         (party_slot_eq, ":party_no", slot_town_lord, "trp_player"),
         (assign, ":garrison_troop", 1),
       (else_try),
	     #gekokujo 3.0 microfactions! start
		 #let's include fort garrisons in the budget
		 (party_slot_eq, ":party_no", slot_party_type, spt_fort),
		 (party_slot_eq, ":party_no", slot_fort_captured, 1),
         (assign, ":garrison_troop", 1),
		 #gekokujo 3.0 microfactions! end
       (try_end),
       (this_or_next|eq, ":party_no", "p_main_party"),
       (eq, ":garrison_troop", 1),
       (party_get_num_companion_stacks, ":num_stacks",":party_no"),
       (try_for_range, ":i_stack", 0, ":num_stacks"),
         (party_stack_get_troop_id, ":stack_troop",":party_no",":i_stack"),
         (party_stack_get_size, ":stack_size",":party_no",":i_stack"),
         (call_script, "script_game_get_troop_wage", ":stack_troop", ":party_no"),
         (assign, ":cur_wage", reg0),
         (val_mul, ":cur_wage", ":stack_size"),
         (try_begin),
           (eq, ":garrison_troop", 1),
           (val_add, ":garrison_wages", ":cur_wage"),
         (else_try),
           (val_add, ":nongarrison_wages", ":cur_wage"),
         (try_end),
       (try_end),
     (try_end),
     (val_div, ":garrison_wages", 2),#Half payment for garrisons
     (store_sub, ":total_payment", 14, "$g_cur_week_half_daily_wage_payments"), #between 0 and 7
     (val_mul, ":nongarrison_wages", ":total_payment"),
     (val_div, ":nongarrison_wages", 14),
     ##diplomacy start+ centralization affects this in the player's kingdom
###xxx TODO: This appears to be missing.
     ##diplomacy end+
     (store_add, reg0, ":nongarrison_wages", ":garrison_wages"),
    ]),
  # script_calculate_hero_weekly_net_income_and_add_to_wealth
  # Input: arg1 = troop_no
  # Output: none
  ("calculate_hero_weekly_net_income_and_add_to_wealth",
    [
      (store_script_param_1, ":troop_no"),
      
      (troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
      (troop_get_slot, ":cur_wealth", ":troop_no", slot_troop_wealth),
      
      (assign, ":weekly_income", 750), #let every hero receive 750 mon by default
      
      (store_character_level, ":troop_level", ":troop_no"),
      (store_mul, ":level_income", ":troop_level", 10),
      (val_add, ":weekly_income", ":level_income"),
      
      (store_troop_faction,":faction_no", ":troop_no"),

	  ##diplomacy start+
	  #Bonus for marshall and/or faction leader (is 1000 in native)
	  (assign, ":leader_bonus_gold", 1000),
	  (assign, ":bonus_applied", 0),
	  (try_begin),
		   #OPTIONAL CHANGE (HIGH)
		   (ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_HIGH),
 		   #Scale marshall and king bonus gold by number of remaining kingdoms,
           #so the total amount paid out remains the same even as kingdoms disappear.
           #This is only enabled if changes are on "HIGH".
           (is_between, ":faction_no", kingdoms_begin, kingdoms_end),
           (store_sub, ":original_kingdoms", npc_kingdoms_end, npc_kingdoms_begin),#deliberately excludes player kingdom
           (ge, ":original_kingdoms", 2),
           (assign, ":current_kingdoms", 0),
           (try_for_range, ":other_fac", kingdoms_begin, kingdoms_end),#deliberately include player kingdom
             (faction_slot_eq, ":other_fac", slot_faction_state, sfs_active),
             (val_add, ":current_kingdoms", 1),
           (try_end),
           (ge, ":current_kingdoms", 1),
           (lt, ":current_kingdoms", ":original_kingdoms"),
           (val_mul, ":leader_bonus_gold", ":original_kingdoms"),
           (val_div, ":leader_bonus_gold", ":current_kingdoms"),
		   #Examples, assuming 6 starting kingdoms and no player kingdom:
		   #6 kingdoms: 1000 each, 1000 * 6 = 6000 total
		   #5 kingdoms: 1200 each, 1200 * 5 = 6000 total
		   #4 kingdoms: 1500 each, 1500 * 4 = 6000 total
		   #3 kingdoms: 2000 each, 2000 * 3 = 6000 total
		   #2 kingdoms: 3000 each, 3000 * 2 = 6000 total
		   #1 kingdom:  6000 each, 6000 * 1 = 6000 total
      (try_end),
	  ##diplomacy end+
	  
      (try_begin), #check if troop is kingdom leader
        (faction_slot_eq, ":faction_no", slot_faction_leader, ":troop_no"),
        ##diplomacy start+
		#OLD BEHAVIOR:
        #(val_add, ":weekly_income", 1000),
		#NEW BEHAVIOR:
		(val_add, ":weekly_income", ":leader_bonus_gold"),
		(val_add, ":bonus_applied", 1),
        ##diplomacy end+
      (try_end),
      
      (try_begin), #check if troop is marshall
        (faction_slot_eq, ":faction_no", slot_faction_marshall, ":troop_no"),
        ##diplomacy start+
		#OLD BEHAVIOR:
        #(val_add, ":weekly_income", 1000),
		#NEW BEHAVIOR:
	    (val_add, ":weekly_income", ":leader_bonus_gold"),
		(val_add, ":bonus_applied", 1),
        ##diplomacy end+
      (try_end),

	  ##diplomacy start+
	  (try_begin),
	  	  #OPTIONAL CHANGE (MEDIUM)
		  (ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_MEDIUM),
		  #If the lord is the spouse of the faction leader and no better bonus
		  #applied, the lord gets half of the bonus if either (1) there is no
		  #marshall, or (2) the faction leader is the player.
		  (eq, ":bonus_applied", 0),
		  (is_between, ":faction_no", kingdoms_begin, kingdoms_end),
  		  #Don't do the usual polygamy check: the bonus only applies to
		  #one of the spouses.
		  (faction_get_slot, ":faction_leader", ":faction_no", slot_faction_leader),
		  (ge, ":faction_leader", 0),
		  (troop_slot_eq, ":faction_leader", slot_troop_spouse, ":troop_no"),
		  #Don't apply the bonus unless the faction leader bonus is going
		  #all/partially uncollected, or the marshal bonus is going uncollected.
		  (this_or_next|neg|faction_slot_ge, ":faction_no", slot_faction_marshall, 0),
			(eq, ":faction_leader", "trp_player"),
		  #Apply bonus
		  (val_add, ":bonus_applied", 1),
		  (store_div, reg0, ":leader_bonus_gold", 2),
		  (val_add, ":weekly_income", reg0),
	  (try_end),
	  ##diplomacy end+
      
      (assign, ":cur_weekly_wage", 0),
      (try_begin),
        (gt, ":party_no",0),
        (call_script, "script_calculate_weekly_party_wage", ":party_no"),
        (assign, ":cur_weekly_wage", reg0),
      (try_end),
      ##diplomacy start+
      (try_begin),
	     #take into account leader's leadership skill, like in CC
	     #economics changes must be enabled
         (ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_HIGH),
         (store_skill_level, ":leadership_level", "skl_leadership", ":troop_no"),
         (val_clamp, ":leadership_level", 0, 11),
         (store_mul, ":leadership_bonus", 5, ":leadership_level"),
         (store_sub, ":leadership_factor", 100, ":leadership_bonus"),
         (val_mul, ":cur_weekly_wage", ":leadership_factor"),  #wage = wage * (100 - 5*leadership)/100
         (val_div, ":cur_weekly_wage", 100),
      (try_end),

	  #Store the change in income for use below
	  (store_sub, ":net_income", ":weekly_income", ":cur_weekly_wage"),
      ##diplomacy end+
      (val_sub, ":weekly_income", ":cur_weekly_wage"),
      
      (val_add, ":cur_wealth", ":weekly_income"),
	  
	  (try_begin),
		(lt, ":cur_wealth", 0),
		(store_sub, ":percent_under", 0, ":cur_wealth"),
		(val_mul, ":percent_under", 100),
		(val_div, ":percent_under", ":cur_weekly_wage"),
		(val_div, ":percent_under", 5), #Max 20 percent
		##diplomacy start+
		#The above assumption could be violated if the lord entered this
		#script with a negative wealth.  Add a failsafe.
		(val_clamp, ":percent_under", 0, 21),
		##diplomacy end+		
		(call_script, "script_party_inflict_attrition", ":party_no", ":percent_under", 1),
	  (try_end),

	  ##diplomacy start+
	  #Apply gold change
	  (try_begin),
	     #If the wealth change was positive, some of it may go to the lord's holdings.
	     (ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_HIGH),
	     (ge, ":net_income", 1),
		 (call_script, "script_dplmc_distribute_gold_to_lord_and_holdings", ":net_income", ":troop_no"),
	  (else_try),
	     #Fall through to old version:
		 #OLD VERSION:
         (val_max, ":cur_wealth", 0),
         (troop_set_slot, ":troop_no", slot_troop_wealth, ":cur_wealth"),
	  (try_end),
	  ##diplomacy end+
  ]),
  # script_cf_reinforce_party
  # Input: arg1 = party_no,
  # Output: none
  # Adds reinforcement to party according to its type and faction
  # Called from several places, simple_triggers for centers, script_hire_men_to_kingdom_hero_party for hero parties
  ("cf_reinforce_party",
    [
      (store_script_param_1, ":party_no"),
      
      (store_faction_of_party, ":party_faction", ":party_no"),
	  ##diplomacy start+ The party faction may be changed for culture, but we still need the original
	  (assign, ":real_party_faction", ":party_faction"),
	  ##diplomacy end+
      (party_get_slot, ":party_type",":party_no", slot_party_type),

#Rebellion changes begin: 
      (try_begin),
        (eq, ":party_type", spt_kingdom_hero_party),
        (party_stack_get_troop_id, ":leader", ":party_no"),
        (troop_get_slot, ":party_faction",  ":leader", slot_troop_original_faction),
		##diplomacy start+ Use player culture for companions and spouse (and any hypothetical non-hero mercenaries)
		(eq, ":real_party_faction", "fac_player_supporters_faction"),
		(is_between, "$g_player_culture", npc_kingdoms_begin, npc_kingdoms_end),
		#gekokujo 3.0 microfactions! include fort companions start
		#(this_or_next|is_between, ":leader", companions_begin, companions_end),
		(this_or_next|is_between, ":leader", companions_begin, fort_companions_end),
		#gekokujo 3.0 microfactions! include fort companions end
		(this_or_next|troop_slot_eq, "trp_player", slot_troop_spouse, ":leader"),
		   (neg|is_between, ":leader", heroes_begin, heroes_end),
		(assign, ":party_faction", "$g_player_culture"),
		##diplomacy end+
      (try_end),
#Rebellion changes end

      (try_begin),
        (eq, ":party_faction", "fac_player_supporters_faction"),
        (party_get_slot, ":town_lord", ":party_no", slot_town_lord),
        (try_begin),
        ##diplomacy begin
          (is_between, "$g_player_culture", npc_kingdoms_begin, npc_kingdoms_end),
          (assign, ":party_faction", "$g_player_culture"),

          (try_begin), #debug
            (eq, "$cheat_mode", 1),
            (str_store_party_name, s11, ":party_no"),
            (display_message, "@pt in {s11}"),
          (try_end),

        (else_try),
        ##diplomacy end
          (gt, ":town_lord", 0),
          (troop_get_slot, ":party_faction", ":town_lord", slot_troop_original_faction),
        (else_try),
          (party_get_slot, ":party_faction", ":party_no", slot_center_original_faction),
        (try_end),
      (try_end),
	  ##diplomacy start+ Player culture cleanup (do this once here, instead of separately for each type)
	  (try_begin),
	     (gt, ":real_party_faction", "fac_commoners"),
	     (this_or_next|eq, ":real_party_faction", "fac_player_faction"),
	     (this_or_next|eq, ":real_party_faction", "fac_player_supporters_faction"),
		 (eq, ":real_party_faction", "$players_kingdom"),
		 (neg|is_between, ":party_faction", npc_kingdoms_begin, npc_kingdoms_end),
		 (is_between, "$g_player_culture", npc_kingdoms_begin, npc_kingdoms_end),
		 (assign, ":party_faction", "$g_player_culture"),
	  (try_end),
	  ##diplomacy end+
      
      (faction_get_slot, ":party_template_a", ":party_faction", slot_faction_reinforcements_a),
      (faction_get_slot, ":party_template_b", ":party_faction", slot_faction_reinforcements_b),
      (faction_get_slot, ":party_template_c", ":party_faction", slot_faction_reinforcements_c),

      (assign, ":party_template", 0),
      (store_random_in_range, ":rand", 0, 100),
  	  ##diplomacy start+
	  #Implement "quality vs. quantity" in a way that is visible in player battles
	  #(previously, quantity increased party size, but quality only had an effect
	  #in autocalc battles)
	  (try_begin),
		(is_between, ":real_party_faction", kingdoms_begin, kingdoms_end),
		(faction_get_slot, ":dplmc_quality", ":real_party_faction", dplmc_slot_faction_quality),
		(val_clamp, ":dplmc_quality", -3, 4),
		(val_add, ":rand", ":dplmc_quality"),
		(val_clamp, ":rand", 0, 101),
	  (try_end),
	  ##diplomacy end+
      (try_begin),
        (this_or_next|eq, ":party_type", spt_town),
        (eq, ":party_type", spt_castle),  #CASTLE OR TOWN
        (try_begin),
          (lt, ":rand", 65),
          (assign, ":party_template", ":party_template_a"),
        (else_try),
          (assign, ":party_template", ":party_template_b"),
        (try_end),
      (else_try),
        (eq, ":party_type", spt_kingdom_hero_party),
        (try_begin),
          (lt, ":rand", 50),
          (assign, ":party_template", ":party_template_a"),
        (else_try),
          (lt, ":rand", 75),
          (assign, ":party_template", ":party_template_b"),
        (else_try),
          (assign, ":party_template", ":party_template_c"),
        (try_end),
      (else_try),
	  ##diplomacy start+ Reinforcements for patrols
	    (eq, ":party_type", spt_patrol),
		(try_begin),
		   (lt, ":rand", 65),
		   (assign, ":party_template", ":party_template_a"),
		(else_try),
		   (assign, ":party_template", ":party_template_b"),
		(try_end),
	  ##diplomacy end+
      (try_end),

      (try_begin),
        (gt, ":party_template", 0),
        (party_add_template, ":party_no", ":party_template"),
      (try_end),
  ]),
  # script_hire_men_to_kingdom_hero_party
  # Input: arg1 = troop_no (hero of the party)
  # Output: none
  ("hire_men_to_kingdom_hero_party",
    [
      (store_script_param_1, ":troop_no"),
      
      (troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
      (troop_get_slot, ":cur_wealth", ":troop_no", slot_troop_wealth),
      
      #while hiring reinforcements party leaders can only use 3/4 of their budget. This value is holding in ":hiring budget".
      (assign, ":hiring_budget", ":cur_wealth"),
      (val_mul, ":hiring_budget", 3),
      (val_div, ":hiring_budget", 4),            
    
      (call_script, "script_party_get_ideal_size", ":party_no"),
      (assign, ":ideal_size", reg0),
      (store_mul, ":ideal_top_size", ":ideal_size", 3),
      (val_div, ":ideal_top_size", 2),

	  #(try_begin),
	  #	(ge, "$cheat_mode", 1),
      #  (str_store_troop_name, s7, ":troop_no"),
      #  (assign, reg9, ":cur_wealth"),
      #  (display_message, "@{!}DEBUGS : {s7} total budget is {reg9}"),
      #  (assign, reg6, ":ideal_size"),
      #  (assign, reg7, ":ideal_top_size"),
      #  (assign, reg8, ":hiring_budget"),
      #  (display_message, "str_debug__hiring_men_to_s7_ideal_size__reg6_ideal_top_size__reg7_hiring_budget__reg8"),
      #(try_end),
	  	  
      (party_get_num_companions, ":party_size", ":party_no"),
      
      (store_faction_of_party, ":party_faction", ":party_no"),
      (try_begin),
        (this_or_next|eq, ":party_faction", "fac_player_supporters_faction"),
        (eq, ":party_faction", "$players_kingdom"),        
        (assign, ":reinforcement_cost", reinforcement_cost_moderate),
      (else_try),
        (game_get_reduce_campaign_ai, ":reduce_campaign_ai"),
        (assign, ":reinforcement_cost", reinforcement_cost_moderate),
        (try_begin), 
          (eq, ":reduce_campaign_ai", 0), #hard
          (assign, ":reinforcement_cost", reinforcement_cost_hard),
        (else_try), 
          (eq, ":reduce_campaign_ai", 1), #moderate
          (assign, ":reinforcement_cost", reinforcement_cost_moderate),
        (else_try), 
          (eq, ":reduce_campaign_ai", 2), #easy
          (assign, ":reinforcement_cost", reinforcement_cost_easy),
        (try_end),           
      (try_end),  
      
      (assign, ":num_rounds", 1),            
      (try_for_range, ":unused", 0 , ":num_rounds"),
        (try_begin),
          (lt, ":party_size", ":ideal_size"),
          (gt, ":hiring_budget", ":reinforcement_cost"),
          (gt, ":party_no", 0), 
          (call_script, "script_cf_reinforce_party", ":party_no"),
          (val_sub, ":cur_wealth", ":reinforcement_cost"),
          (troop_set_slot, ":troop_no", slot_troop_wealth, ":cur_wealth"),
        (else_try),
          (gt, ":party_size", ":ideal_top_size"),
          (store_troop_faction, ":troop_faction", ":troop_no"),
          (party_get_num_companion_stacks, ":num_stacks", ":party_no"),
          (assign, ":total_regulars", 0),
          (assign, ":total_regular_levels", 0),
          (try_for_range_backwards, ":i_stack", 0, ":num_stacks"),
            (party_stack_get_troop_id, ":stack_troop", ":party_no", ":i_stack"),
            (neg|troop_is_hero, ":stack_troop"),
            (party_stack_get_size, ":stack_size", ":party_no", ":i_stack"),
            (store_character_level, ":stack_level", ":stack_troop"),
            (store_troop_faction, ":stack_faction", ":stack_troop"),
            (try_begin),
              (eq, ":troop_faction", ":stack_faction"),
              (val_mul, ":stack_level", 3), #reducing the chance of the faction troops' removal
            (try_end),
            (val_mul, ":stack_level", ":stack_size"),
            (val_add, ":total_regulars", ":stack_size"),
            (val_add, ":total_regular_levels", ":stack_level"),
          (try_end),
          (gt, ":total_regulars", 0),
          (store_div, ":average_level", ":total_regular_levels", ":total_regulars"),
          (try_for_range_backwards, ":i_stack", 0, ":num_stacks"),
            (party_stack_get_troop_id, ":stack_troop", ":party_no", ":i_stack"),
            (neg|troop_is_hero, ":stack_troop"),
            (party_stack_get_size, ":stack_size", ":party_no", ":i_stack"),
            (store_character_level, ":stack_level", ":stack_troop"),
            (store_troop_faction, ":stack_faction", ":stack_troop"),
            (try_begin),
              (eq, ":troop_faction", ":stack_faction"),
              (val_mul, ":stack_level", 3),
            (try_end),
            (store_sub, ":level_dif", ":average_level", ":stack_level"),
            (val_div, ":level_dif", 3),
            (store_add, ":prune_chance", 10, ":level_dif"),
            (gt, ":prune_chance", 0),
            (call_script, "script_get_percentage_with_randomized_round", ":stack_size", ":prune_chance"),
            (gt, reg0, 0),
            (party_remove_members, ":party_no", ":stack_troop", reg0),
          (try_end),
        (try_end),
      (try_end),
  ]),
  # script_create_cattle_herd
  # Input: arg1 = center_no, arg2 = amount (0 = default)
  # Output: reg0 = party_no
  ("create_cattle_herd",
    [
      (store_script_param_1, ":center_no"),
      (store_script_param_2, ":amount"),
      
      (assign, ":herd_party", -1),
      (set_spawn_radius,1),

      (spawn_around_party,":center_no", "pt_cattle_herd"),
      (assign, ":herd_party", reg0),
      (party_get_position, pos1, ":center_no"),
      (call_script, "script_map_get_random_position_around_position_within_range", 1, 2),
      (party_set_position, ":herd_party", pos2),

      (party_set_slot, ":herd_party", slot_party_type, spt_cattle_herd),
      (party_set_slot, ":herd_party", slot_party_ai_state, spai_undefined),
      (party_set_ai_behavior, ":herd_party", ai_bhvr_hold),

      (party_set_slot, ":herd_party", slot_party_commander_party, -1), #we need this because 0 is player's party!

      (try_begin),
        (gt, ":amount", 0),
        (party_clear, ":herd_party"),
        (party_add_members, ":herd_party", "trp_cattle", ":amount"),
      (try_end),
       
      (assign, reg0, ":herd_party"),
  ]),
  #script_buy_cattle_from_village
  # Input: arg1 = village_no, arg2 = amount, arg3 = single_cost
  # Output: reg0 = party_no
  ("buy_cattle_from_village",
    [
      (store_script_param, ":village_no", 1),
      (store_script_param, ":amount", 2),
      (store_script_param, ":single_cost", 3),

      #Changing price of the cattle
      (try_for_range, ":unused", 0, ":amount"),
        (call_script, "script_game_event_buy_item", "itm_cattle_meat", 0),
        (call_script, "script_game_event_buy_item", "itm_cattle_meat", 0),
      (try_end),

      (party_get_slot, ":num_cattle", ":village_no", slot_village_number_of_cattle),
      (val_sub, ":num_cattle", ":amount"),
      (party_set_slot, ":village_no", slot_village_number_of_cattle, ":num_cattle"),
      (store_mul, ":cost", ":single_cost", ":amount"),
      (troop_remove_gold, "trp_player", ":cost"),

      (assign, ":continue", 1),
      (try_for_parties, ":cur_party"),
        (eq, ":continue", 1),
        (party_slot_eq, ":cur_party", slot_party_type, spt_cattle_herd),
        (store_distance_to_party_from_party, ":dist", ":village_no", ":cur_party"),
        (lt, ":dist", 6),
        (assign, ":subcontinue", 1),
        (try_begin),
          (check_quest_active, "qst_move_cattle_herd"),
          (quest_slot_eq, "qst_move_cattle_herd", slot_quest_target_party, ":cur_party"),
          (assign, ":subcontinue", 0),
        (try_end),
        (eq, ":subcontinue", 1),
        (party_add_members, ":cur_party", "trp_cattle", ":amount"),
        (assign, ":continue", 0),
        (assign, reg0, ":cur_party"),
      (try_end),
      (try_begin),
        (eq, ":continue", 1),
        (call_script, "script_create_cattle_herd", ":village_no", ":amount"),
      (try_end),
  ]),
  #script_kill_cattle_from_herd
  # Input: arg1 = party_no, arg2 = amount
  # Output: none (fills trp_temp_troop's inventory)
  ("kill_cattle_from_herd",
    [
      (store_script_param_1, ":party_no"),
      (store_script_param_2, ":amount"),

      (troop_clear_inventory, "trp_temp_troop"),
      (store_mul, ":meat_amount", ":amount", 2),
      (troop_add_items, "trp_temp_troop", "itm_cattle_meat", ":meat_amount"),

      (troop_get_inventory_capacity, ":inv_size", "trp_temp_troop"),
      (try_for_range, ":i_slot", 0, ":inv_size"),
        (troop_get_inventory_slot, ":item_id", "trp_temp_troop", ":i_slot"),
        (eq, ":item_id", "itm_cattle_meat"),
        (troop_set_inventory_slot_modifier, "trp_temp_troop", ":i_slot", imod_fresh),
      (try_end),

      (party_get_num_companions, ":num_cattle", ":party_no"),
      (try_begin),
        (ge, ":amount", ":num_cattle"),
        (remove_party, ":party_no"),
      (else_try),
        (party_remove_members, ":party_no", "trp_cattle", ":amount"),
      (try_end),
      ]),
  # script_create_kingdom_hero_party
  # Input: arg1 = troop_no, arg2 = center_no
  # Output: $pout_party = party_no
  ("create_kingdom_hero_party",
    [
      (store_script_param, ":troop_no", 1),
      (store_script_param, ":center_no", 2),
     
      (store_troop_faction, ":troop_faction_no", ":troop_no"),
      
      (assign, "$pout_party", -1),
      (try_begin),
        (eq, "$g_there_is_no_avaliable_centers", 0),
        (set_spawn_radius, 0),
	  (else_try),
        (set_spawn_radius, 15),
      (try_end),
      (spawn_around_party, ":center_no", "pt_kingdom_hero_party"),
      
      (assign, "$pout_party", reg0),
      
      (party_set_faction, "$pout_party", ":troop_faction_no"),
      (party_set_slot, "$pout_party", slot_party_type, spt_kingdom_hero_party),
      (call_script, "script_party_set_ai_state", "$pout_party", spai_undefined, -1),
      (troop_set_slot, ":troop_no", slot_troop_leaded_party, "$pout_party"),
      (party_add_leader, "$pout_party", ":troop_no"),
      (str_store_troop_name, s5, ":troop_no"),
      (party_set_name, "$pout_party", "str_s5_s_party"),
      
      (party_set_slot, "$pout_party", slot_party_commander_party, -1), #we need this because 0 is player's party!

      #Setting the flag icon
      #normal_banner_begin
      (troop_get_slot, ":cur_banner", ":troop_no", slot_troop_banner_scene_prop),
      (try_begin),
        (gt, ":cur_banner", 0),
        (val_sub, ":cur_banner", banner_scene_props_begin),
        (val_add, ":cur_banner", banner_map_icons_begin),
      #custom_banner_begin
      #(troop_get_slot, ":flag_icon", ":troop_no", slot_troop_custom_banner_map_flag_type),
      #(try_begin),
      #  (ge, ":flag_icon", 0),
      #  (val_add, ":flag_icon", custom_banner_map_icons_begin),
      #  (party_set_banner_icon, "$pout_party", ":flag_icon"),
      (try_end),

      (try_begin),
        #because of below two lines, lords can only hire more than one party_template(stack) at game start once a time during all game.
        (troop_slot_eq, ":troop_no", slot_troop_spawned_before, 0),
        (troop_set_slot, ":troop_no", slot_troop_spawned_before, 1),
        (assign, ":num_tries", 20),
        (try_begin),
          (store_troop_faction, ":troop_kingdom", ":troop_no"),
          (faction_slot_eq, ":troop_kingdom", slot_faction_leader, ":troop_no"),
          (assign, ":num_tries", 50),
        (try_end),

        #(str_store_troop_name, s0, ":troop_no"),
        #(display_message, "{!}str_debug__hiring_men_to_party_for_s0"),

        (try_for_range, ":unused", 0, ":num_tries"),
          (call_script, "script_hire_men_to_kingdom_hero_party", ":troop_no"),
        (try_end),
        
        (assign, ":xp_rounds", 0),

        (game_get_reduce_campaign_ai, ":reduce_campaign_ai"),
        (try_begin),
          (this_or_next|eq, ":troop_faction_no", "$players_kingdom"),
          (eq, ":troop_faction_no", "fac_player_supporters_faction"),
          (assign, ":xp_rounds", 0),
        (else_try),
          (eq, ":reduce_campaign_ai", 0), #hard
          (assign, ":xp_rounds", 2),
        (else_try),
          (eq, ":reduce_campaign_ai", 1), #moderate
          (assign, ":xp_rounds", 1),
        (else_try),                        
          (eq, ":reduce_campaign_ai", 2), #easy
          (assign, ":xp_rounds", 0),
        (try_end),           

        (troop_get_slot, ":renown", ":troop_no", slot_troop_renown),
        (store_div, ":renown_xp_rounds", ":renown", 100),
        (val_add, ":xp_rounds", ":renown_xp_rounds"),
        (try_for_range, ":unused", 0, ":xp_rounds"),
          (call_script, "script_upgrade_hero_party", "$pout_party", 4000),
        (try_end),
      (try_end),      
  ]),
  # script_create_kingdom_party_if_below_limit
  # Input: arg1 = faction_no, arg2 = party_type (variables beginning with spt_)
  # Output: reg0 = party_no
  ("create_kingdom_party_if_below_limit",
    [
      (store_script_param_1, ":faction_no"),
      (store_script_param_2, ":party_type"),

      (call_script, "script_count_parties_of_faction_and_party_type", ":faction_no", ":party_type"),
      (assign, ":party_count", reg0),
      
      (assign, ":party_count_limit", 0),

      (faction_get_slot, ":num_towns", ":faction_no", slot_faction_num_towns),

      (try_begin),
##        (eq, ":party_type", spt_forager),
##        (assign, ":party_count_limit", 1),
##      (else_try),
##        (eq, ":party_type", spt_scout),
##        (assign, ":party_count_limit", 1),
##      (else_try),
##        (eq, ":party_type", spt_patrol),
##        (assign, ":party_count_limit", 1),
##      (else_try),
##        (eq, ":party_type", spt_messenger),
##        (assign, ":party_count_limit", 1),
##      (else_try),
        (eq, ":party_type", spt_kingdom_caravan),
        (try_begin),
          (eq, ":num_towns", 0),
          (assign, ":party_count_limit", 0),
        (else_try),
          (eq, ":num_towns", 1),
          (assign, ":party_count_limit", 1),
        (else_try),
          (eq, ":num_towns", 2),
          (assign, ":party_count_limit", 3),
        (else_try),
          (assign, ":party_count_limit", 5),
        (try_end),
        ##diplomacy begin
          #overwriting party count limit MAX(2 * X - 1, 0)
        (store_mul, ":party_count_limit", ":num_towns", 2),
        (val_sub, ":party_count_limit", 1),
        (val_max, ":party_count_limit", 0),
        ##diplomacy end

##      (else_try),
##        (eq, ":party_type", spt_prisoner_train),
##        (assign, ":party_count_limit", 1),
      (try_end),
      
      (assign, reg0, -1),
      (try_begin),
        (lt, ":party_count", ":party_count_limit"),
        (call_script,"script_cf_create_kingdom_party", ":faction_no", ":party_type"),
      (try_end),
  ]),
  # script_cf_create_kingdom_party
  # Input: arg1 = faction_no, arg2 = party_type (variables beginning with spt_)
  # Output: reg0 = party_no
  ("cf_create_kingdom_party",
    [
      (store_script_param_1, ":faction_no"),
      (store_script_param_2, ":party_type"),
      
      (str_store_faction_name, s7, ":faction_no"),
      (assign, ":party_name_str", "str_no_string"),
      
##      (faction_get_slot, ":reinforcements_a", ":faction_no", slot_faction_reinforcements_a),
      (faction_get_slot, ":reinforcements_b", ":faction_no", slot_faction_reinforcements_b),
##      (faction_get_slot, ":reinforcements_c", ":faction_no", slot_faction_reinforcements_c),
      
      (try_begin),
##        (eq, ":party_type", spt_forager),
##        (assign, ":party_template", "pt_forager_party"),
#        (assign, ":party_name_str", "str_s7_foragers"),
##      (else_try),
##        (eq, ":party_type", spt_scout),
##        (assign, ":party_template", "pt_scout_party"),
#        (assign, ":party_name_str", "str_s7_scouts"),
##      (else_try),
##        (eq, ":party_type", spt_patrol),
##        (assign, ":party_template", "pt_patrol_party"),
#        (assign, ":party_name_str", "str_s7_patrol"),
##      (else_try),
        (eq, ":party_type", spt_kingdom_caravan),
        (assign, ":party_template", "pt_kingdom_caravan_party"),
#        (assign, ":party_name_str", "str_s7_caravan"),
##      (else_try),
##        (eq, ":party_type", spt_messenger),
##        (assign, ":party_template", "pt_messenger_party"),
#        (assign, ":party_name_str", "str_s7_messenger"),
##      (else_try),
##        (eq, ":party_type", spt_raider),
##        (assign, ":party_template", "pt_raider_party"),
##        (assign, ":party_name_str", "str_s7_raiders"),
##      (else_try),
##        (eq, ":party_type", spt_prisoner_train),
##        (assign, ":party_template", "pt_prisoner_train_party"),
#        (assign, ":party_name_str", "str_s7_prisoner_train"),
      (try_end),
      
      (assign, ":result", -1),
      (try_begin),
        (try_begin),
          (eq, ":party_type", spt_kingdom_caravan),
          (call_script,"script_cf_select_random_town_with_faction", ":faction_no", -1),
          (set_spawn_radius, 0),
        (else_try), #not used at the moment
          (call_script,"script_cf_select_random_walled_center_with_faction", ":faction_no", -1),
          (set_spawn_radius, 1),
        (try_end),
        (assign, ":spawn_center", reg0),
        (is_between, ":spawn_center", centers_begin, centers_end),
        (spawn_around_party,":spawn_center",":party_template"),
        (assign, ":result", reg0),
        (party_set_faction, ":result", ":faction_no"),
        (try_begin),
          (eq, ":party_type", spt_kingdom_caravan),
          (party_set_slot, ":result", slot_party_home_center, ":spawn_center"),
          (party_set_slot, ":result", slot_party_last_traded_center, ":spawn_center"),
		(try_end),
        (party_set_slot, ":result", slot_party_type, ":party_type"),
        (party_set_slot, ":result", slot_party_ai_state, spai_undefined),
        (try_begin),
          (neq, ":party_name_str", "str_no_string"),
          (party_set_name, ":result", ":party_name_str"),
        (try_end),
        
        (try_begin),
##          (eq, ":party_type", spt_forager),
##          (party_add_template, ":result", ":reinforcements_a"),
##        (else_try),
##          (eq, ":party_type", spt_scout),
##          (party_add_template, ":result", ":reinforcements_c"),
##        (else_try),
##          (eq, ":party_type", spt_patrol),
##          (party_add_template, ":result", ":reinforcements_a"),
##          (party_add_template, ":result", ":reinforcements_b"),
##        (else_try),
          (eq, ":party_type", spt_kingdom_caravan),
          (try_begin),
            (eq, ":faction_no", "fac_player_supporters_faction"),
            (party_get_slot, ":reinforcement_faction", ":spawn_center", slot_center_original_faction),
            (faction_get_slot, ":reinforcements_b", ":reinforcement_faction", slot_faction_reinforcements_b),
          (try_end),
          (party_add_template, ":result", ":reinforcements_b"),
          (party_add_template, ":result", ":reinforcements_b"),
          (party_set_ai_behavior,":result",ai_bhvr_travel_to_party),
          (party_set_ai_object,":result",":spawn_center"),
          (party_set_flags, ":result", pf_default_behavior, 1),
          (store_sub, ":item_to_price_slot", slot_town_trade_good_prices_begin, trade_goods_begin),
          (try_for_range, ":cur_goods", trade_goods_begin, trade_goods_end),
            (store_add, ":cur_goods_price_slot", ":cur_goods", ":item_to_price_slot"),
            (party_set_slot, ":result", ":cur_goods_price_slot", average_price_factor),
          (try_end),
##        (else_try),
##          (eq, ":party_type", spt_messenger),
##          (faction_get_slot, ":messenger_troop", ":faction_no", slot_faction_messenger_troop),
##          (party_add_leader, ":result", ":messenger_troop"),
##          (party_set_ai_behavior,":result",ai_bhvr_travel_to_party),
##          (party_set_ai_object,":result",":spawn_center"),
##          (party_set_flags, ":result", pf_default_behavior, 0),
##        (else_try),
##          (eq, ":party_type", spt_raider),
##          (party_add_template, ":result", ":reinforcements_c"),
##          (party_add_template, ":result", ":reinforcements_b"),
##          (party_add_template, ":result", "pt_raider_captives"),
##        (else_try),
##          (eq, ":party_type", spt_prisoner_train),
##          (party_add_template, ":result", ":reinforcements_b"),
##          (party_add_template, ":result", ":reinforcements_a"),
##          (try_begin),
##            (call_script,"script_cf_faction_get_random_enemy_faction",":faction_no"),
##            (store_random_in_range,":r",0,3),
##            (try_begin),
##              (lt, ":r", 1),
##              (faction_get_slot, ":captive_reinforcements", reg0, slot_faction_reinforcements_b),
##            (else_try),
##              (faction_get_slot, ":captive_reinforcements", reg0, slot_faction_reinforcements_a),
##            (try_end),
##            (party_add_template, ":result", ":captive_reinforcements",1),
##          (else_try),
##            (party_add_template, ":result", "pt_default_prisoners"),
##          (try_end),
        (try_end),
      (try_end),
      (ge, ":result", 0),
      (assign, reg0, ":result"),
  ]),
  # script_get_troop_attached_party
  # Input: arg1 = troop_no
  # Output: reg0 = party_no (-1 if troop's party is not attached to a party)
  ("get_troop_attached_party",
    [
      (store_script_param_1, ":troop_no"),
      
      (troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
      (assign, ":attached_party_no", -1),
      (try_begin),
        (ge, ":party_no", 0),
        (party_get_attached_to, ":attached_party_no", ":party_no"),
      (try_end),
      (assign, reg0, ":attached_party_no"),
  ]),
  # script_refresh_village_defenders
  # Input: arg1 = village_no
  # Output: none
  ("refresh_village_defenders",
    [
      (store_script_param_1, ":village_no"),

      (assign, ":ideal_size", 50),
      (try_begin),
        (party_get_num_companions, ":party_size", ":village_no"),
        (lt, ":party_size", ":ideal_size"),
        (party_add_template, ":village_no", "pt_village_defenders"),
      (try_end),
  ]),
  # script_village_set_state
  # Input: arg1 = center_no arg2:new_state
  # Output: reg0: food consumption (1 food item counts as 100 units)
  ("village_set_state",
    [
      (store_script_param_1, ":village_no"),
      (store_script_param_2, ":new_state"),

	  ##diplomacy start+
	  (store_current_hours, ":hours"),
	  (party_get_slot, ":attacker_party", ":village_no", slot_village_raided_by),
	  (try_begin),
		(ge, ":attacker_party", 0),
		(party_is_active, ":attacker_party"),#added 2011-06-07
		(party_stack_get_troop_id, ":attack_leader", ":attacker_party", 0),
		(ge, ":attack_leader", 0),
		(party_set_slot, ":village_no", dplmc_slot_center_last_attacked_time, ":hours"),
		(party_set_slot, ":village_no", dplmc_slot_center_last_attacker, ":attack_leader"),
	  (try_end),
	  ##diplomacy end+
	  
      (try_begin),
        (eq, ":new_state", 0),
        (party_set_extra_text, ":village_no", "str_empty_string"),
        (party_set_slot, ":village_no", slot_village_raided_by, -1),
      (else_try),
        (eq, ":new_state", svs_being_raided),
        (party_set_extra_text, ":village_no", "@(Being Raided)"),
      (else_try),
        (eq, ":new_state", svs_looted),
        (party_set_extra_text, ":village_no", "@(Looted)"),
				
        (party_set_slot, ":village_no", slot_village_raided_by, -1),
        (call_script, "script_change_center_prosperity", ":village_no", -60),
		(val_add, "$newglob_total_prosperity_from_villageloot", -60),

		(try_begin), #optional - lowers the relationship between a lord and his liege if his fief is looted
			(eq, 5, 0),
			(party_get_slot, ":town_lord", ":village_no", slot_town_lord),
			(is_between, ":town_lord", active_npcs_begin, active_npcs_end),
			(store_faction_of_troop, ":town_lord_faction", ":town_lord"),
			(faction_get_slot, ":faction_leader", ":town_lord_faction", slot_faction_leader),
			(call_script, "script_troop_change_relation_with_troop", ":town_lord", ":faction_leader", -1),
			(val_add, "$total_battle_ally_changes", -1),
		(try_end),
      (else_try),
        (eq, ":new_state", svs_under_siege),
        (party_set_extra_text, ":village_no", "@(Under Siege)"),
				
		#Divert all caravans heading to the center
		#Note that occasionally, no alternative center will be found. In that case, the caravan will try to run the blockade
		(try_for_parties, ":party_no"), 
			(gt, ":party_no", "p_spawn_points_end"),
			(party_slot_eq, ":party_no", slot_party_type, spt_kingdom_caravan),
            (party_slot_eq, ":party_no", slot_party_ai_object, ":village_no"),

			(party_get_slot, ":origin", ":party_no", slot_party_last_traded_center),
			(store_faction_of_party, ":merchant_faction", ":party_no"),
            ##diplomacy start+ added new third parameter, the caravan party itself
            (call_script, "script_cf_select_most_profitable_town_at_peace_with_faction_in_trade_route", ":origin", ":merchant_faction",
				":party_no"),
			##diplomacy end+
            (assign, ":target_center", reg0),
			(is_between, ":target_center", centers_begin, centers_end),
			
            (party_set_ai_behavior, ":party_no", ai_bhvr_travel_to_party),
            (party_set_ai_object, ":party_no", ":target_center"),
            (party_set_flags, ":party_no", pf_default_behavior, 0),
            (party_set_slot, ":party_no", slot_party_ai_state, spai_trading_with_town),
            (party_set_slot, ":party_no", slot_party_ai_object, ":target_center"),
		(try_end),		
      (try_end),
      (party_set_slot, ":village_no", slot_village_state, ":new_state"),
  ]),
  # script_process_village_raids
  # Input: none
  # Output: none
  # called from triggers every two hours
  ("process_village_raids",
    [
	   ##diplomacy start+
	   (store_current_hours, ":hours"),
	   ##diplomacy end+
       (try_for_range, ":village_no", villages_begin, villages_end),
        ##CABA Fix 
        #(try_begin), 
        #  (this_or_next|is_between, ":village_no", "p_village_16", "p_village_23"), #Shapeshte through Shulus (up to Ilvia) 
        #  (this_or_next|is_between, ":village_no", "p_village_49", "p_village_51"), #Tismirr and Karindi 
        #  (this_or_next|eq, ":village_no", "p_village_75"), #Bhulaban 
        #  (is_between, ":village_no", "p_village_85", "p_village_87"), #Ismirala and Slezkh 
        #  (assign, ":normal_village_icon", "icon_village_snow_a"),  
        #  (assign, ":burnt_village_icon", "icon_village_snow_burnt_a"), 
        #  (assign, ":deserted_village_icon", "icon_village_snow_deserted_a"), 
        #(else_try), 
        #  (is_between, ":village_no", "p_village_91", "p_salt_mine"), #Ayn Assuadi through Rushdigh 
        #  (assign, ":normal_village_icon", "icon_village_c"),  
        #  (assign, ":burnt_village_icon", "icon_village_burnt_c"), 
        #  (assign, ":deserted_village_icon", "icon_village_deserted_c"), 
        #(else_try), 
        #  (assign, ":normal_village_icon", "icon_village_a"), 
        #  (assign, ":burnt_village_icon", "icon_village_burnt_a"), 
        #  (assign, ":deserted_village_icon", "icon_village_deserted_a"), 
        #(try_end), 
        ##CABA Fix        
		
		#gekokujo default village icons
         (assign, ":normal_village_icon", "icon_village_a"), 
         (assign, ":burnt_village_icon", "icon_village_burnt_a"), 
         (assign, ":deserted_village_icon", "icon_village_deserted_a"), 
		 
         (party_get_slot, ":village_raid_progress", ":village_no", slot_village_raid_progress),
         (try_begin),                
           (party_slot_eq, ":village_no", slot_village_state, 0), #village is normal
           (val_sub, ":village_raid_progress", 5),
           (val_max, ":village_raid_progress", 0),
           (party_set_slot, ":village_no", slot_village_raid_progress, ":village_raid_progress"),
           (try_begin),
             (lt, ":village_raid_progress", 50),
             
             (try_begin),
               (party_get_icon, ":village_icon", ":village_no"),
              (neq, ":village_icon", ":normal_village_icon"), ##CABA FIX 
              (party_set_icon, ":village_no", ":normal_village_icon"), ##CABA FIX 
             (try_end),
             
             (party_slot_ge, ":village_no", slot_village_smoke_added, 1),
             (party_set_slot, ":village_no", slot_village_smoke_added, 0),             
             (party_clear_particle_systems, ":village_no"),
           (try_end),
         (else_try),
           (party_slot_eq, ":village_no", slot_village_state, svs_being_raided), #village is being raided
           #End raid unless there is an enemy party nearby
           (assign, ":raid_ended", 1),
           (party_get_slot, ":raider_party", ":village_no", slot_village_raided_by),
           
           (try_begin),
             (ge, ":raider_party", 0),
             (party_is_active, ":raider_party"),
             (this_or_next|neq, ":raider_party", "p_main_party"),
             (eq, "$g_player_is_captive", 0),
             (store_distance_to_party_from_party, ":distance", ":village_no", ":raider_party"),
             (lt, ":distance", raid_distance),
             (assign, ":raid_ended", 0),
           (try_end),
           
           (try_begin),           
             (eq, ":raid_ended", 1),
             (call_script, "script_village_set_state", ":village_no", svs_normal), #clear raid flag
             (party_set_slot, ":village_no", slot_village_smoke_added, 0),
             (party_clear_particle_systems, ":village_no"),                          
           (else_try),
             (assign, ":raid_progress_increase", 11),
             (party_get_slot, ":looter_party", ":village_no", slot_village_raided_by),
             (try_begin),
               (party_get_skill_level, ":looting_skill", ":looter_party", "skl_looting"),
               (val_add, ":raid_progress_increase", ":looting_skill"),
             (try_end),
             (try_begin),
               (party_slot_eq, ":village_no", slot_center_has_watch_tower, 1),
               (val_mul, ":raid_progress_increase", 2),
               (val_div, ":raid_progress_increase", 3),
             (try_end),
             (val_add, ":village_raid_progress", ":raid_progress_increase"),
             (party_set_slot, ":village_no", slot_village_raid_progress, ":village_raid_progress"),
             (try_begin),
               (ge, ":village_raid_progress", 50),
               (party_slot_eq, ":village_no", slot_village_smoke_added, 0),
               (party_add_particle_system, ":village_no", "psys_map_village_fire"),
               (party_add_particle_system, ":village_no", "psys_map_village_fire_smoke"),
              (party_set_icon, ":village_no", ":burnt_village_icon"), ##CABA FIX 
               (party_set_slot, ":village_no", slot_village_smoke_added, 1),
             (try_end),
			 ##diplomacy start+ set values of slots
			 (try_begin),
				(ge, ":looter_party", 0),
				(party_stack_get_troop_id, ":raid_leader", ":looter_party", 0),
				(ge, ":raid_leader", 0),
				(party_set_slot, ":village_no", dplmc_slot_center_last_attacked_time, ":hours"),
				(party_set_slot, ":village_no", dplmc_slot_center_last_attacker, ":raid_leader"),
			 (try_end),
			 ##diplomacy end+
             (try_begin),
               (gt, ":village_raid_progress", 100),
               (str_store_party_name_link, s1, ":village_no"),
               (party_stack_get_troop_id, ":raid_leader", ":looter_party", 0),
               (ge, ":raid_leader", 0),
               (str_store_party_name, s2, ":looter_party"),
               (display_log_message, "@The village of {s1} has been looted by {s2}."),

               (try_begin),
                 (party_get_slot, ":village_lord", ":village_no", slot_town_lord),
                 (is_between, ":village_lord", active_npcs_begin, active_npcs_end),
                 (call_script, "script_troop_change_relation_with_troop", ":raid_leader", ":village_lord", -1),
                 (val_add, "$total_battle_enemy_changes", -1),
               (try_end),

               #give loot gold to raid leader
               (troop_get_slot, ":raid_leader_gold", ":raid_leader", slot_troop_wealth),
			   ##diplomacy start+
			   #How did the next line ever work?  isn't it missing a slot number?!
               #  (party_get_slot, ":village_prosperity", ":village_no"),
			   #Replace it with the following:
			   (party_get_slot, ":village_prosperity", ":village_no", slot_town_prosperity),
			   ##diplomacy end+
               (store_mul, ":value_of_loot", ":village_prosperity", 60), #average is 3000
               (val_add, ":raid_leader_gold", ":value_of_loot"),
               (troop_set_slot, ":raid_leader", slot_troop_wealth, ":raid_leader_gold"),			   			   
               
               #take loot gold from village lord #new 1.126
			   ##diplomacy start+
			   #With economic changes enabled, this will first withdraw from accumulated taxes at center
               (try_begin),
				 #To support the possibility of kingdom_ladies becoming enfeoffed, changed the
				 #below line from active_npcs_begin/active_npcs_end to heroes_begin/heroes_end
                 (is_between, ":village_lord", heroes_begin, heroes_end),
				 (neq, ":village_lord", "trp_kingdom_heroes_including_player_begin"),
                 (troop_get_slot, ":village_lord_gold", ":village_lord", slot_troop_wealth),
				 (try_begin),
					#Optional behavior: subtract the looted wealth from the village's uncollected
					#rents and tariffs
					(ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_HIGH),#<-- check experimental changes are enabled
					(assign, ":gold_lost_by_lord", ":value_of_loot"),
					#Accumulated rents & tariffs get zeroed further down, so we don't need to worry
					#about modifying the slot's value to reflect the loss.
					(party_get_slot, ":x", ":village_no", slot_center_accumulated_rents),
					(val_max, ":x", 0),
					(val_sub, ":gold_lost_by_lord", ":x"),
					(party_get_slot, ":x", ":village_no", slot_center_accumulated_tariffs),
					(val_max, ":x", 0),
					(val_sub, ":gold_lost_by_lord", ":x"),
					#Only then subtract the remainder from the lord
					(val_max, ":gold_lost_by_lord", 0),
					(val_sub, ":village_lord_gold", ":gold_lost_by_lord"),
				 (else_try),
					#Unaltered behavior
					(val_sub, ":village_lord_gold", ":value_of_loot"),
				 (try_end),
				 #Apply the gold change
                 (val_max, ":village_lord_gold", 0),
                 (troop_set_slot, ":village_lord", slot_troop_wealth, ":village_lord_gold"),
			   (else_try),
			      #Option: player loses gold when his fiefs are raided, just as an NPC does
				  #(default behavior in Native is the player loses no gold).  The gold is
				  #lost from the treasury, and is reduced by uncollected taxes.
				  #
				  #Only do this if the option is explicitly enabled and the player has
				  # a chamberlain.
				  (eq, ":village_lord", "trp_player"),
				  (gt, "$g_player_chamberlain", 0),#check the player has a chamberlain
			      (ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_MEDIUM),#<-- check experimental changes are enabled
				  (party_slot_eq, ":village_no", slot_town_lord, "trp_player"),
				  #Do some double-checking, to avoid potential erroneous gold loss
				  #if some careless code has improperly left the "slot_town_lord"
				  #slot of the village initialized to zero.
				  (store_faction_of_party, ":village_faction", ":village_no"),
				 ##diplomacy start+ Handle player is co-ruler of faction
				 (assign, ":is_coruler", 0),
 				 (try_begin),
				    (eq, ":village_faction", "$players_kingdom"),
					(is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
					(call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", "$players_kingdom"),
					(ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
					(assign, ":is_coruler", 1),
				 (try_end),
				 (this_or_next|eq, ":is_coruler", 1),
				 ##diplomacy end+
				  (this_or_next|eq, "fac_player_supporters_faction", ":village_faction"),
				     (eq, "$players_kingdom", ":village_faction"),
				  #Adjust the amount lost by difficulty setting.
				  (assign, ":gold_lost_by_lord", ":value_of_loot"),
				  (game_get_reduce_campaign_ai, ":reduce_campaign_ai"),
				  (try_begin),
				    (eq, ":reduce_campaign_ai", 0),#hard, 125% loss
					(val_mul, ":gold_lost_by_lord", 5),
					(val_div, ":gold_lost_by_lord", 4),
				  (else_try),
					(eq, ":reduce_campaign_ai", 1),#medium, 100% loss
				  (else_try),
					(eq, ":reduce_campaign_ai", 2),#easy, 50% loss
					(val_div, ":gold_lost_by_lord", 2),
				  (try_end),

				  #First defray the lost gold with rents and tarriffs from the village
				  (party_get_slot, ":x", ":village_no", slot_center_accumulated_rents),
				  (val_max, ":x", 0),
				  (val_sub, ":gold_lost_by_lord", ":x"),
				  (party_get_slot, ":x", ":village_no", slot_center_accumulated_tariffs),
				  (val_max, ":x", 0),
				  (val_sub, ":gold_lost_by_lord", ":x"),
				  (val_max, ":gold_lost_by_lord", 0),
				  #Remove the remainder (if any) from the player's treasury
				  (store_troop_gold, ":x", "trp_household_possessions"),
				  (val_min, ":gold_lost_by_lord", ":x"),
				  (ge, ":gold_lost_by_lord", 1),
				  (call_script, "script_dplmc_withdraw_from_treasury", ":gold_lost_by_lord"),
               (try_end),
			   ##diplomacy end+
			   
               (call_script, "script_village_set_state",  ":village_no", svs_looted),
               (party_set_slot, ":village_no", slot_center_accumulated_rents, 0), #new 1.126
               (party_set_slot, ":village_no", slot_center_accumulated_tariffs, 0), #new 1.126

               (party_set_slot, ":village_no", slot_village_raid_progress, 0),
               (party_set_slot, ":village_no", slot_village_recover_progress, 0),
               (try_begin),
                 (store_faction_of_party, ":village_faction", ":village_no"),
				 ##diplomacy start+ Handle player is co-ruler of faction
				 (assign, ":is_coruler", 0),
 				 (try_begin),
				    (eq, ":village_faction", "$players_kingdom"),
					(is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
					(call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", "$players_kingdom"),
					(ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
					(assign, ":is_coruler", 1),
				 (try_end),
				 (this_or_next|eq, ":is_coruler", 1),
				 ##diplomacy end+
                 (this_or_next|party_slot_eq, ":village_no", slot_town_lord, "trp_player"),
                 (eq, ":village_faction", "fac_player_supporters_faction"),
                 (call_script, "script_add_notification_menu", "mnu_notification_village_raided", ":village_no", ":raid_leader"),
               (try_end),
               (call_script, "script_add_log_entry", logent_village_raided, ":raid_leader",  ":village_no", -1, -1),
               (store_faction_of_party, ":looter_faction", ":looter_party"),
               (call_script, "script_faction_inflict_war_damage_on_faction", ":looter_faction", ":village_faction", 5),			   
             (try_end),
           (try_end),
         (else_try),
           (party_slot_eq, ":village_no", slot_village_state, svs_looted), #village is looted
           (party_get_slot, ":recover_progress", ":village_no", slot_village_recover_progress),
           (val_add, ":recover_progress", 1),
           (party_set_slot, ":village_no", slot_village_recover_progress, ":recover_progress"), #village looted
           (try_begin),
             (ge, ":recover_progress", 10),
             (party_slot_eq, ":village_no", slot_village_smoke_added, 1),
             (party_clear_particle_systems, ":village_no"),
             (party_add_particle_system, ":village_no", "psys_map_village_looted_smoke"),
             (party_set_slot, ":village_no", slot_village_smoke_added, 2),
           (try_end),
           (try_begin),
             (gt, ":recover_progress", 50),
             (party_slot_eq, ":village_no", slot_village_smoke_added, 2),
             (party_clear_particle_systems, ":village_no"),
             (party_set_slot, ":village_no", slot_village_smoke_added, 3),
            (party_set_icon, ":village_no", ":deserted_village_icon"), ##CABA FIX 
           (try_end),
           (try_begin),
             (gt, ":recover_progress", 100),
             (call_script, "script_village_set_state",  ":village_no", 0),#village back to normal
             (party_set_slot, ":village_no", slot_village_recover_progress, 0),
             (party_clear_particle_systems, ":village_no"),
             (party_set_slot, ":village_no", slot_village_smoke_added, 0),
            (party_set_icon, ":village_no", ":normal_village_icon"), ##CABA FIX 
           (try_end),
         (try_end),
       (try_end),
  ]),
  # script_process_sieges
  # Input: none
  # Output: none
  #called from triggers
  ("process_sieges",
    [
       (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
         #Reducing siege hardness every day by 20
         (party_get_slot, ":siege_hardness", ":center_no", slot_center_siege_hardness),
         (val_sub, ":siege_hardness", 20),
         (val_max, ":siege_hardness", 0),
         (party_set_slot, ":center_no", slot_center_siege_hardness, ":siege_hardness"),
       
         (party_get_slot, ":town_food_store", ":center_no", slot_party_food_store),
         (call_script, "script_center_get_food_store_limit", ":center_no"),
         (assign, ":food_store_limit", reg0),
         (try_begin),
           (party_get_slot, ":besieger_party", ":center_no", slot_center_is_besieged_by),
           (ge, ":besieger_party", 0), #town is under siege
       
           #Reduce prosperity of besieged castle/town by -0.33/-4 every day.
           (try_begin),
             (try_begin),
               (is_between, ":center_no", castles_begin, castles_end),
               (store_random_in_range, ":random_value", 0, 3),
               (try_begin),
                 (eq, ":random_value", 0),
                 (assign, ":daily_siege_effect_on_prosperity", -1),
               (else_try),
                 (assign, ":daily_siege_effect_on_prosperity", 0),
               (try_end),
             (else_try),
               (assign, ":daily_siege_effect_on_prosperity", -4),
             (try_end),
       
             (call_script, "script_change_center_prosperity", ":center_no", ":daily_siege_effect_on_prosperity"),
             (val_add, "$newglob_total_prosperity_from_townloot", ":daily_siege_effect_on_prosperity"),
           (try_end),

           (store_faction_of_party, ":center_faction", ":center_no"),
        # Lift siege unless there is an enemy party nearby
           (assign, ":siege_lifted", 0),
           (try_begin),
             (try_begin),
               (neg|party_is_active, ":besieger_party"),
               (assign, ":siege_lifted", 1),
             (else_try),
               (store_distance_to_party_from_party, ":besieger_distance", ":center_no", ":besieger_party"),
               (gt, ":besieger_distance", 5),
               (assign, ":siege_lifted", 1),
			 (else_try),  
  			 ##diplomacy begin
         (neg|party_slot_eq, ":center_no", slot_village_infested_by_bandits, "trp_peasant_woman"),
         ##diplomacy end
			   (store_faction_of_party, ":besieger_faction", ":besieger_party"),
               (store_relation, ":reln", ":besieger_faction", ":center_faction"),
               (ge, ":reln", 0),
               (assign, ":siege_lifted", 1),
             (try_end),
			 
			 
             (eq, ":siege_lifted", 1),
			 #If another lord can take over the siege, it isn't lifted
             ##diplomacy start+ Support promoted kingdom ladies
             #(try_for_range, ":enemy_hero", active_npcs_begin, active_npcs_end),
             (try_for_range, ":enemy_hero", heroes_begin, heroes_end),
             ##diplomacy end+
               (troop_slot_eq, ":enemy_hero", slot_troop_occupation, slto_kingdom_hero),
               (troop_get_slot, ":enemy_party", ":enemy_hero", slot_troop_leaded_party),
               (ge, ":enemy_party", 0),
               (party_is_active, ":enemy_party"),
               (store_faction_of_party, ":party_faction", ":enemy_party"),
               (store_relation, ":reln", ":party_faction", ":center_faction"),
               (lt, ":reln", 0),
               (store_distance_to_party_from_party, ":distance", ":center_no", ":enemy_party"),
               (lt, ":distance", 4),
               (assign, ":besieger_party", ":enemy_party"),
               (party_set_slot, ":center_no", slot_center_is_besieged_by, ":enemy_party"),
               (assign, ":siege_lifted", 0),
             (try_end),
           (try_end),
           (try_begin),
             (eq, ":siege_lifted", 1),
             (call_script, "script_lift_siege", ":center_no", 1),
           (else_try),
             (call_script, "script_center_get_food_consumption", ":center_no"),
             (assign, ":food_consumption", reg0),
             (val_sub, ":town_food_store", ":food_consumption"), # reduce food only under siege???
             (try_begin),
               (le, ":town_food_store", 0), #town is starving
               (store_random_in_range, ":r", 0, 100),
               (lt, ":r", 10), 
               (call_script, "script_party_wound_all_members", ":center_no"), # town falls with 10% chance if starving
             (try_end),
           (try_end),
         (else_try),
           #town is not under siege...
           (val_add, ":town_food_store", 30), #add 30 food (significant for castles only.
         (try_end),

         (val_min, ":town_food_store", ":food_store_limit"),
         (val_max, ":town_food_store", 0),
         (party_set_slot, ":center_no", slot_party_food_store, ":town_food_store"),
       (try_end),
  ]),
  # script_lift_siege
  # Input: arg1 = center_no, arg2 = display_message
  # Output: none
  #called from triggers
  ("lift_siege",
    [
      (store_script_param, ":center_no", 1),
      (store_script_param, ":display_message", 2),
      (party_set_slot, ":center_no", slot_center_is_besieged_by, -1), #clear siege
      (call_script, "script_village_set_state",  ":center_no", 0), #clear siege flag
      (try_begin),
        (eq, ":center_no", "$g_player_besiege_town"),
        (assign, "$g_siege_method", 0), #remove siege progress
      (try_end),
      (try_begin),
        (eq, ":display_message", 1),
        (str_store_party_name_link, s3, ":center_no"),
        (display_message, "@{s3} is no longer under siege."),
      (try_end),
      ]),
  # script_process_alarms
  # Input: none
  # Output: none
  #called from triggers
  ("process_alarms",
    [	
      (assign, ":current_modula", "$g_alarm_modula"),
      (val_add, "$g_alarm_modula", 1),
      (try_begin),
        (eq, "$g_alarm_modula", 3),
        (assign, "$g_alarm_modula", 0),
      (try_end),
      
      (try_for_range, ":center_no", centers_begin, centers_end),
        (store_mod, ":center_modula", ":center_no", 3),
        (eq, ":center_modula", ":current_modula"),
        
        (party_set_slot, ":center_no", slot_center_last_spotted_enemy, -1),
        (party_set_slot, ":center_no", slot_center_sortie_strength, 0),
        (party_set_slot, ":center_no", slot_center_sortie_enemy_strength, 0),
        
        (assign, ":spotting_range", 3),
        (try_begin),
          (is_currently_night),
          (assign, ":spotting_range", 2),
        (try_end),
        
        (try_begin),
          (party_slot_eq, ":center_no", slot_center_has_watch_tower, 1),
          (val_mul, ":spotting_range", 2),
        (else_try),
          (neg|is_between, ":center_no", villages_begin, villages_end),
          (val_add, ":spotting_range", 1),
          (val_mul, ":spotting_range", 2),
        (try_end),

        (store_faction_of_party, ":center_faction", ":center_no"),
		
        (try_for_parties, ":party_no"),
          (this_or_next|party_slot_eq, ":party_no", slot_party_type, spt_kingdom_hero_party),
          (eq, ":party_no", "p_main_party"),
          
          (store_faction_of_party, ":party_faction", ":party_no"),
          
          (try_begin),
            (eq, ":party_no", "p_main_party"),
            (assign, ":party_faction", "$players_kingdom"),
          (try_end),
          
          (try_begin),          
            (eq, ":party_faction", ":center_faction"),
            
            (store_distance_to_party_from_party, ":distance", ":party_no", ":center_no"),
            (le, ":distance", ":spotting_range"),
            
            (party_get_slot, ":cached_strength", ":party_no", slot_party_cached_strength),
            (party_get_slot, ":sortie_strength", ":center_no", slot_center_sortie_strength),
            (val_add, ":sortie_strength", ":cached_strength"),
            (party_set_slot, ":center_no", slot_center_sortie_strength, ":sortie_strength"),		 
          (else_try),
            (neq, ":party_faction", ":center_faction"),
		  
            (store_distance_to_party_from_party, ":distance", ":party_no", ":center_no"),

			(try_begin),
				(lt, ":distance", 10),
				(store_current_hours, ":hours"),
				(store_sub, ":faction_recce_slot", ":party_faction", kingdoms_begin),
				(val_add, ":faction_recce_slot", slot_center_last_reconnoitered_by_faction_time),
				(party_set_slot, ":center_no", ":faction_recce_slot", ":hours"),
				
				#(eq, "$cheat_mode", 1),
				#(str_store_faction_name, s4, ":party_faction"),
				#(str_store_party_name, s5, ":center_no"),
				#(display_message, "@{!}DEBUG -- {s4} reconnoiters {s5}"),
			(try_end),

		    (store_relation, ":reln", ":center_faction", ":party_faction"),
            (lt, ":reln", 0),
			(try_begin),
	            (le, ":distance", ":spotting_range"),
	            
	            (party_get_slot, ":cached_strength", ":party_no", slot_party_cached_strength),
	            (party_get_slot, ":enemy_strength", ":center_no", slot_center_sortie_enemy_strength),
	            (val_add, ":enemy_strength", ":cached_strength"),
	            (party_set_slot, ":center_no", slot_center_sortie_enemy_strength, ":enemy_strength"),
	            (party_set_slot, ":center_no", slot_center_last_spotted_enemy, ":party_no"),
			(try_end),
			
          (try_end),		  		  		  		  		  
        (try_end),
      (try_end),
      
      (try_for_range, ":center_no", centers_begin, centers_end),
        (store_mod, ":center_modula", ":center_no", 3),
        (eq, ":center_modula", ":current_modula"),
        
        (try_begin), #eligible units sortie out of castle
          (is_between, ":center_no", walled_centers_begin, walled_centers_end),
          (party_slot_ge, ":center_no", slot_center_last_spotted_enemy, 0),
          
          (party_get_slot, ":sortie_strength", ":center_no", slot_center_sortie_strength),
          (party_get_slot, ":enemy_strength", ":center_no", slot_center_sortie_enemy_strength),
          
          #Below two lines are new added by ozan. While AI want to drive nearby besieging enemy parties by making sortie them, they give up current battle if they are already joining one.
          #Lets assume there is a battle inside the castle, because enemies are inside castle and they are so close to castle they will be also added to slot_center_sortie_enemy_strength
          #But in this scenario, they are not outside the castle, so searching/patrolling enemy outside the castle is useless at this point. 
          #So if there is already a battle inside the center, do not sortie and search enemy outside.
          (party_get_battle_opponent, ":center_battle_opponent", ":center_no"),
          (try_begin),
		    (ge, "$cheat_mode", 1),
            (ge, ":center_battle_opponent", 0),
            (str_store_party_name, s7, ":center_no"),
            (str_store_party_name, s6, ":center_battle_opponent"),
            (display_message, "@{!}DEBUG : There are already enemies ({s6}) inside {s7}."),
          (try_end),
          (lt, ":center_battle_opponent", 0), 
          #New added by ozan ended.
                                        
          (try_begin),
            (eq, "$cheat_mode", 1),
            (str_store_party_name, s4, ":center_no"),
            (assign, reg3, ":sortie_strength"),
            (assign, reg4, ":enemy_strength"),
            (display_message, "@{!}DEBUG -- Calculating_sortie for {s4} strength of {reg3} vs {reg4} enemies"),
          (try_end),
          
          (store_mul, ":enemy_strength_mul_14_div_10", ":enemy_strength", 14),
          (val_div, ":enemy_strength_mul_14_div_10", 10),
          (gt, ":sortie_strength", ":enemy_strength_mul_14_div_10"),
          
          (assign, ":at_least_one_party_sorties", 0),
          (try_for_parties, ":sortie_party"),
            (party_get_attached_to, ":town", ":sortie_party"),
            (eq, ":town", ":center_no"),
            
            (party_slot_eq, ":sortie_party", slot_party_type, spt_kingdom_hero_party),
            
            (party_get_slot, ":cached_strength", ":sortie_party", slot_party_cached_strength),
            (ge, ":cached_strength", 100),
            
            (party_detach, ":sortie_party"),
            (call_script, "script_party_set_ai_state", ":sortie_party",  spai_patrolling_around_center, ":center_no"),
            
            (try_begin),          
              (eq, "$cheat_mode", 1),
              (str_store_party_name, s4, ":sortie_party"),
              (display_message, "str_s4_sorties"),
            (try_end),
            
            (eq, ":at_least_one_party_sorties", 0),
            (assign, ":at_least_one_party_sorties", ":sortie_party"),
          (try_end),
          
          (try_begin),
            (party_is_in_town, "p_main_party", ":center_no"),
			(eq, "$g_player_is_captive", 0),
            (gt, ":at_least_one_party_sorties", 0),
            (call_script, "script_add_notification_menu", "mnu_notification_sortie_possible", ":center_no", ":sortie_party"),	
          (try_end),
		(try_end),
		
		(store_faction_of_party, ":center_faction", ":center_no"),
		
		#Send message
		(this_or_next|eq, "$cheat_mode", 1), #this is message
		(this_or_next|party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
		(eq, ":center_faction", "$players_kingdom"),
		
		(party_get_slot, ":enemy_party", ":center_no", slot_center_last_spotted_enemy),
		(ge, ":enemy_party", 0),
		(store_distance_to_party_from_party, ":dist", "p_main_party", ":center_no"),
		(assign, ":has_messenger", 0),
		(try_begin),
		 ##diplomacy start+ Handle player is co-ruler of faction
		 (assign, ":is_coruler", 0),
		 (try_begin),
			(eq, ":center_faction", "$players_kingdom"),
			(is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
			(call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", "$players_kingdom"),
			(ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
			(assign, ":is_coruler", 1),
		 (try_end),
		 (this_or_next|eq, ":is_coruler", 1),
		 ##diplomacy end+
		  (this_or_next|party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
		  (eq, ":center_faction", "fac_player_supporters_faction"),
		  (party_slot_eq, ":center_no", slot_center_has_messenger_post, 1),
		  (assign, ":has_messenger", 1),
		(try_end),
		
		(this_or_next|eq, "$cheat_mode", 1),
		(this_or_next|lt, ":dist", 30),
			(eq, ":has_messenger", 1),
		
		(str_store_party_name_link, s1, ":center_no"),
        (party_get_slot, ":exact_enemy_strength", ":center_no", slot_center_sortie_enemy_strength),
		
		(try_begin),
			(lt, ":exact_enemy_strength", 500),
			(display_message, "@Small bands of enemies spotted near {s1}."),
		(else_try),
			(lt, ":exact_enemy_strength", 1000),
			(display_message, "@Enemy patrols spotted near {s1}."),
		(else_try),
			(lt, ":exact_enemy_strength", 2000),
			(display_message, "@Medium-sized group of enemies spotted near {s1}."),
		(else_try),
			(lt, ":exact_enemy_strength", 4000),
			(display_message, "@Significant group of enemies spotted near {s1}."),
		(else_try),
			(lt, ":exact_enemy_strength", 8000),
			(display_message, "@Army of enemies spotted near {s1}."),
		(else_try),
			(lt, ":exact_enemy_strength", 16000),
			(display_message, "@Large army of enemies spotted near {s1}."),
		(else_try),
			(display_message, "@Great host of enemies spotted near {s1}."),
		(try_end),
		#maybe do audio sound?
		
      (try_end),
     ]),
  # script_allow_vassals_to_join_indoor_battle
  # Input: none
  # Output: none 
  ("allow_vassals_to_join_indoor_battle",
    [
     #if our commander attacks an enemy army
     ##diplomacy start+ Support promoted kingdom ladies
     #(try_for_range, ":troop_no", active_npcs_begin, active_npcs_end),
     (try_for_range, ":troop_no", heroes_begin, heroes_end),
     ##diplomacy end+
       (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
       (neg|troop_slot_ge, ":troop_no", slot_troop_prisoner_of_party, 0),
       (troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
       (gt, ":party_no", 0),
       (party_is_active, ":party_no"),
                
       (party_get_attached_to, ":party_is_attached_to", ":party_no"),
       (lt, ":party_is_attached_to", 0),

       (store_troop_faction, ":faction_no", ":troop_no"),

       (try_begin),
         #(faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_attacking_enemies_around_center),
         (party_slot_eq, ":party_no", slot_party_ai_state, spai_accompanying_army),
         (party_get_slot, ":commander_party", ":party_no", slot_party_ai_object),
         (gt, ":commander_party", 0),
         (party_is_active, ":commander_party"),
               
         (assign, ":besieged_center", -1),          
         (try_begin),
           (party_slot_eq, ":commander_party", slot_party_ai_state, spai_holding_center), #if commander is holding a center
           (party_get_slot, ":commander_object", ":commander_party", slot_party_ai_object), #get commander's ai object (center they are holding)
           (party_get_battle_opponent, ":besieger_enemy", ":commander_object"), #get this object's battle opponent
           (party_is_active, ":besieger_enemy"),
           (assign, ":besieged_center", ":commander_object"),
           (assign, ":commander_object", ":besieger_enemy"),
         (else_try),
           (party_slot_eq, ":commander_party", slot_party_ai_state, spai_engaging_army), #if commander is engaging an army          
           (party_get_slot, ":commander_object", ":commander_party", slot_party_ai_object), #get commander's ai object (army which they engaded)
           (ge, ":commander_object", 0), #if commander has an object
           (neg|is_between, ":commander_object", centers_begin, centers_end), #if this object is not a center, so it is a party
           (party_is_active, ":commander_object"),
           (party_get_battle_opponent, ":besieged_center", ":commander_object"), #get this object's battle opponent
         (else_try),
           (assign, ":besieged_center", -1),
         (try_end),
         
         (is_between, ":besieged_center", walled_centers_begin, walled_centers_end), #if battle opponent of our commander's ai object is a walled center

         (party_get_attached_to, ":attached_to_party", ":commander_party"), #if commander is attached to besieged center already.
         (eq, ":attached_to_party", ":besieged_center"),

         (store_faction_of_party, ":besieged_center_faction", ":besieged_center"),#get (battle opponent of our commander's ai object)'s faction
         (eq, ":besieged_center_faction", ":faction_no"), #if battle opponent of our commander's ai object is from same faction with current party
         (party_is_active, ":commander_object"),
         #make also follow_or_not check if needed

         (call_script, "script_party_set_ai_state", ":party_no", spai_engaging_army, ":commander_object"), #go and help commander

         (try_begin),
           (eq, "$cheat_mode", 1),
           (str_store_party_name, s7, ":party_no"),
           (str_store_party_name, s6, ":commander_object"),         
           (display_message, "@{!}DEBUG : {s7} is helping his commander by fighting with {s6}."),
         (try_end),
       (else_try),
         #(faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_attacking_center),

         (party_slot_eq, ":party_no", slot_party_ai_state, spai_accompanying_army),
         (party_get_slot, ":commander_party", ":party_no", slot_party_ai_object),
         (gt, ":commander_party", 0),
         (party_is_active, ":commander_party"),
                
         (party_get_battle_opponent, ":besieged_center", ":commander_party"), #get this object's battle opponent

         #make also follow_or_not check if needed
                  
         (is_between, ":besieged_center", walled_centers_begin, walled_centers_end), #if this object is a center
         (party_get_attached_to, ":attached_to_party", ":party_no"),
         (neq, ":attached_to_party", ":besieged_center"),
         (party_is_active, ":besieged_center"),

         (call_script, "script_party_set_ai_state", ":party_no", spai_engaging_army, ":besieged_center"), #go and help commander         
                  
         #(try_begin),
         #  (eq, "$cheat_mode", 1),
         #  (str_store_party_name, s7, ":party_no"),
         #  (str_store_party_name, s6, ":besieged_center"),         
         #  (display_message, "@{!}DEBUG : {s7} is helping his commander by attacking {s6}."),
         #(try_end),  

         #(party_set_ai_behavior, ":party_no", ai_bhvr_attack_party),
         #(party_set_ai_object, ":party_no", ":besieged_center"),
         #(party_set_flags, ":party_no", pf_default_behavior, 1), #is these needed?
         #(party_set_slot, ":party_no", slot_party_ai_substate, 1), #is these needed?
       (try_end),
     (try_end),       
     ]),
  ("party_set_ai_state",
    [
      (store_script_param, ":party_no", 1),
      (store_script_param, ":new_ai_state", 2),
      (store_script_param, ":new_ai_object", 3),
            
      (party_get_slot, ":old_ai_state", ":party_no", slot_party_ai_state),
      (party_get_slot, ":old_ai_object", ":party_no", slot_party_ai_object),
      (party_get_attached_to, ":attached_to_party", ":party_no"),
      (assign, ":party_is_in_town", 0),
      (try_begin),
        (is_between, ":attached_to_party", centers_begin, centers_end),
        (assign, ":party_is_in_town", ":attached_to_party"),
      (try_end),
          
      (assign, ":commander", -1),          
      (try_begin),
        (party_is_active, ":party_no"),
	    (party_stack_get_troop_id, ":commander", ":party_no", 0),	
	    (store_faction_of_party, ":faction_no", ":party_no"),
	  (try_end),  
	  
	  (try_begin),
	    (lt, ":commander", 0),
        #sometimes 0 sized parties enter "party_set_ai_state" script. So only discard them	    
	    #(try_begin),
        #  (eq, "$cheat_mode", 1),        
	    #  (str_store_troop_name, s6, ":party_no"),      
        #  (party_get_num_companions, reg6, ":party_no"),
        #  (display_message, "@{!}DEBUGS : party name is : {s6}, party size is : {reg6}, new ai discarded."),
        #(try_end),  
	  (else_try),
	    #Party does any business in town
	    (try_begin),
	      (is_between, ":party_is_in_town", walled_centers_begin, walled_centers_end),
	      (party_slot_eq, ":party_is_in_town", slot_center_is_besieged_by, -1),
	      (call_script, "script_troop_does_business_in_center", ":commander", ":party_is_in_town"),
	    (else_try),	      
	      (party_slot_eq, ":party_no", slot_party_ai_state, spai_visiting_village),
	      (party_get_slot, ":party_is_in_village", ":party_no", slot_party_ai_object),	     
	      (is_between, ":party_is_in_village", villages_begin, villages_end),
	      #(party_slot_eq, ":party_is_in_village", slot_center_is_looted_by, -1),
		  (neg|party_slot_eq, ":party_is_in_village", slot_village_state, svs_being_raided),
		  (neg|party_slot_eq, ":party_is_in_village", slot_village_state, svs_looted),
	      (store_distance_to_party_from_party, ":distance", ":party_no", ":party_is_in_village"),
	      (lt, ":distance", 3),
	      (call_script, "script_troop_does_business_in_center", ":commander", ":party_is_in_village"),
	    (try_end),
	    
	    (party_set_slot, ":party_no", slot_party_follow_me, 0),
	    
	    (try_begin),
	      (eq, ":old_ai_state", ":new_ai_state"),
	      (eq, ":old_ai_object", ":new_ai_object"),
          #do nothing. Nothing is changed.
        (else_try),
		  #gekokujo 3.0 integrating motomataru's campaign AI start
          #(assign, ":initiative", 100),
          #(assign, ":aggressiveness", 8),
          #(assign, ":courage", 8),
          (assign, ":initiative", 80),
          (assign, ":aggressiveness", 5),
          (assign, ":courage", 5),
		  #gekokujo 3.0 integrating motomataru's campaign AI end
          
          (try_begin),
            (this_or_next|eq, ":new_ai_state", spai_accompanying_army),
            (eq, ":new_ai_state", spai_screening_army),
            
            (party_set_ai_behavior, ":party_no", ai_bhvr_escort_party),
            (party_set_ai_object, ":party_no", ":new_ai_object"),
            (party_set_flags, ":party_no", pf_default_behavior, 0),
            
            (try_begin),
              (gt, ":party_is_in_town", 0),
              (party_detach, ":party_no"),
            (try_end),
			
            #gekokujo 3.0 integrating motomataru's campaign AI start
            #(try_begin),
            #  (eq, ":new_ai_state", spai_screening_army),
            #  (assign, ":aggressiveness", 9),
            #  (assign, ":courage", 9),
            #  (assign, ":initiative", 80),
            #(else_try),
            #  (assign, ":aggressiveness", 6),
            #  (assign, ":courage", 9),
            #  (assign, ":initiative", 10),
            #(try_end),
            (try_begin),
              (eq, ":new_ai_state", spai_screening_army),
              (assign, ":aggressiveness", 8),
              (assign, ":courage", 8),
              (assign, ":initiative", 100),
			  (assign, ":new_ai_state", spai_accompanying_army),
			  (party_set_slot, ":party_no", slot_party_ai_substate, 1),
            (else_try),
              (assign, ":aggressiveness", 3),
              (assign, ":courage", 8),
              (assign, ":initiative", 50),
			  (party_set_slot, ":party_no", slot_party_ai_substate, 0),
            (try_end),
            #gekokujo 3.0 integrating motomataru's campaign AI end
          (else_try),
            (eq, ":new_ai_state", spai_besieging_center),
            
            (party_get_position, pos1, ":new_ai_object"),
            (map_get_random_position_around_position, pos2, pos1, 2),
            (party_set_ai_behavior, ":party_no", ai_bhvr_travel_to_point),
            (party_set_ai_target_position, ":party_no", pos2),
            (party_set_ai_object, ":party_no", ":new_ai_object"),
            (party_set_flags, ":party_no", pf_default_behavior, 0),
            (party_set_slot, ":party_no", slot_party_follow_me, 1),
            (party_set_slot, ":party_no", slot_party_ai_substate, 0),
            
            (try_begin),
              (gt, ":party_is_in_town", 0),
              (neq, ":party_is_in_town", ":new_ai_object"),
              (party_detach, ":party_no"),
            (try_end),
            
			#gekokujo 3.0 integrating motomataru's campaign AI start
            #(assign, ":aggressiveness", 1),
            #(assign, ":courage", 9),
            #(assign, ":initiative", 20),
            ##(assign, ":initiative", 100),
            (assign, ":aggressiveness", 3),
            (assign, ":courage", 5),
            (assign, ":initiative", 100),
			#gekokujo 3.0 integrating motomataru's campaign AI end
          (else_try),
            (eq, ":new_ai_state", spai_holding_center),
            
            (party_set_ai_behavior, ":party_no", ai_bhvr_travel_to_party),
            (party_set_ai_object, ":party_no", ":new_ai_object"),
            (party_set_flags, ":party_no", pf_default_behavior, 0),
            
            (try_begin),
              (gt, ":party_is_in_town", 0),
              (neq, ":party_is_in_town", ":new_ai_object"),
              (party_detach, ":party_no"),
            (try_end),
            
			#gekokujo 3.0 integrating motomataru's campaign AI start
            #(assign, ":aggressiveness", 7),
            #(assign, ":courage", 9),
            #(assign, ":initiative", 100),
            (assign, ":aggressiveness", 3),
            (assign, ":courage", 8),
            (assign, ":initiative", 80),
			#gekokujo 3.0 integrating motomataru's campaign AI end
            #(party_set_ai_initiative, ":party_no", 99),
          (else_try),
            (eq, ":new_ai_state", spai_patrolling_around_center),
			
			#gekokujo 3.0 integrating motomataru's campaign AI start
			(try_begin),
			  (neg|is_between, ":new_ai_object", villages_begin, villages_end),
			  (party_get_battle_opponent, ":besieger_party", ":new_ai_object"),
			(else_try),
			  (party_slot_eq, ":new_ai_object", slot_village_state, svs_being_raided),
			  (party_get_slot, ":besieger_party", ":new_ai_object", slot_village_raided_by),
			(else_try),
			  (assign, ":besieger_party", -1),
			(try_end),
			  
			(try_begin),
			  (gt, ":besieger_party", 0),
			  (party_is_active, ":besieger_party"),
				
			  (assign, ":new_ai_state", spai_engaging_army),
			  (assign, ":new_ai_object", ":besieger_party"),
			(try_end),
			
            (eq, ":new_ai_state", spai_patrolling_around_center),
			#gekokujo 3.0 integrating motomataru's campaign AI end
			
            (party_get_position, pos1, ":new_ai_object"),
            (map_get_random_position_around_position, pos2, pos1, 1),
            (party_set_ai_behavior, ":party_no", ai_bhvr_travel_to_point),
            (party_set_ai_target_position, ":party_no", pos2),
            (party_set_ai_object, ":party_no", ":new_ai_object"),
            
			#gekokujo 3.0 integrating motomataru's campaign AI start
            #(try_begin),
            #  (faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_attacking_enemies_around_center),
            #  (party_set_ai_patrol_radius, ":party_no", 1), #line 100
            #(else_try),  
            #  (party_set_ai_patrol_radius, ":party_no", 5), #line 100
            #(try_end),
			#gekokujo 3.0 integrating motomataru's campaign AI end
            
            (party_set_flags, ":party_no", pf_default_behavior, 0),
            (party_set_slot, ":party_no", slot_party_follow_me, 1),
            (party_set_slot, ":party_no", slot_party_ai_substate, 0),
            
            (try_begin),
              (gt, ":party_is_in_town", 0),
              (party_detach, ":party_no"),
            (try_end),
            
			#gekokujo 3.0 integrating motomataru's campaign AI start
            #(try_begin),
            #  #new to avoid losing time of marshal with attacking unimportant targets while there is a threat in our centers.
            #  (ge, ":commander", 0),
            #  (faction_slot_eq, ":faction_no", slot_faction_marshall, ":commander"),
	        #  (faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_attacking_enemies_around_center),	        	  
	        #  
	        #  (party_get_position, pos3, ":party_no"),
	        #  (get_distance_between_positions, ":distance_to_center", pos1, pos3),
	        #  	          	      
	        #  (try_begin),    
	        #    (ge, ":distance_to_center", 800), #added new (1.122)
            #    (assign, ":initiative", 10), 
            #    (assign, ":aggressiveness", 1),
            #    (assign, ":courage", 8), 
            #  (else_try), #below added new (1.122)
            #    (assign, ":initiative", 100), 
            #    (assign, ":aggressiveness", 8),
            #    (assign, ":courage", 8),              
            #  (try_end),
            #(else_try),              
            #  (assign, ":aggressiveness", 8),
            #  (assign, ":courage", 8),
            #  (assign, ":initiative", 100),
            #(try_end),  
			(assign, ":courage", 8),
			#gekokujo 3.0 integrating motomataru's campaign AI end
          (else_try),
            (eq, ":new_ai_state", spai_visiting_village),
            (party_get_position, pos1, ":new_ai_object"),
            (map_get_random_position_around_position, pos2, pos1, 2),
            (party_set_ai_behavior, ":party_no", ai_bhvr_travel_to_point),
            (party_set_ai_target_position, ":party_no", pos2),
            (party_set_ai_object, ":party_no", ":new_ai_object"),
            (party_set_flags, ":party_no", pf_default_behavior, 0),
            (party_set_slot, ":party_no", slot_party_ai_substate, 0),
            (try_begin),
              (gt, ":party_is_in_town", 0),
              (neq, ":party_is_in_town", ":new_ai_object"),
              (party_detach, ":party_no"),
            (try_end),
            
			#gekokujo 3.0 integrating motomataru's campaign AI start
            #(assign, ":aggressiveness", 8),
            #(assign, ":courage", 8),
            #(assign, ":initiative", 100),
            (assign, ":aggressiveness", 3),
            (assign, ":courage", 8),
            (assign, ":initiative", 80),
			#gekokujo 3.0 integrating motomataru's campaign AI end
          (else_try), #0.660: this is where the 1625/1640 bugs happen with an improper ai_object
            (eq, ":new_ai_state", spai_raiding_around_center),
            (party_get_position, pos1, ":new_ai_object"),
            (map_get_random_position_around_position, pos2, pos1, 1),
            (party_set_ai_behavior, ":party_no", ai_bhvr_patrol_location),
			
			#gekokujo 3.0 integrating motomataru's campaign AI
            #(party_set_ai_patrol_radius, ":party_no", 10),
			(party_set_ai_patrol_radius, ":party_no", 2),
			
            (party_set_ai_target_position, ":party_no", pos2),
            (party_set_ai_object, ":party_no", ":new_ai_object"),
            (party_set_flags, ":party_no", pf_default_behavior, 0),
	        (party_set_slot, ":party_no", slot_party_follow_me, 1),
	        (party_set_slot, ":party_no", slot_party_ai_substate, 0),
	        (try_begin),
	          (gt, ":party_is_in_town", 0),
	          (neq, ":party_is_in_town", ":new_ai_object"),
	          (party_detach, ":party_no"),
	        (try_end),
	        
			#gekokujo 3.0 integrating motomataru's campaign AI start
	        #(try_begin),
	        #  (ge, ":commander", 0),
	        #  (faction_slot_eq, ":faction_no", slot_faction_marshall, ":commander"),
	        #  (assign, ":aggressiveness", 1),
	        #  (assign, ":courage", 8),
	        #  (assign, ":initiative", 20),
	        #(else_try),
	        #  (assign, ":aggressiveness", 7),
	        #  (assign, ":courage", 8),
	        #  (assign, ":initiative", 100),
	        #(try_end),
	        (assign, ":aggressiveness", 7),
	        (assign, ":courage", 5),
	        (assign, ":initiative", 100),
			#gekokujo 3.0 integrating motomataru's campaign AI end
	      (else_try),
	        (eq, ":new_ai_state", spai_engaging_army),
	        
	        (party_set_ai_behavior, ":party_no", ai_bhvr_attack_party),
	        (party_set_ai_object, ":party_no", ":new_ai_object"),
	        (party_set_flags, ":party_no", pf_default_behavior, 0),
	        (try_begin),
	          (gt, ":party_is_in_town", 0),
	          (party_detach, ":party_no"),
	        (try_end),
	        
			#gekokujo 3.0 integrating motomataru's campaign AI start
            #(try_begin),
            #  #new to avoid losing time of marshal with attacking unimportant targets while there is a threat in our centers.
            #  (ge, ":commander", 0),
            #  (faction_slot_eq, ":faction_no", slot_faction_marshall, ":commander"),
	        #  (faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_attacking_enemies_around_center),	        	  
            #  (assign, ":initiative", 10), 
            #  (assign, ":aggressiveness", 1),
            #  (assign, ":courage", 8),
            #(else_try),              
            #  (assign, ":aggressiveness", 8),
	        #  (assign, ":courage", 8),
	        #  (assign, ":initiative", 100),
	        #(try_end),  
            (assign, ":aggressiveness", 8),
	        (assign, ":courage", 5),
	        (assign, ":initiative", 100),
			#gekokujo 3.0 integrating motomataru's campaign AI end
	      (else_try),
	        (eq, ":new_ai_state", spai_retreating_to_center),
	        (party_set_ai_behavior, ":party_no", ai_bhvr_travel_to_party),
	        (party_set_ai_object, ":party_no", ":new_ai_object"),
	        (party_set_flags, ":party_no", pf_default_behavior, 1),
	        (party_set_slot, ":party_no", slot_party_commander_party, -1),
	        (try_begin),
	          (gt, ":party_is_in_town", 0),
	          (neq, ":party_is_in_town", ":new_ai_object"),
	          (party_detach, ":party_no"),
	        (try_end),
	        
	        (assign, ":aggressiveness", 3),
	        (assign, ":courage", 4),
			#gekokujo 3.0 integrating motomataru's campaign AI
	        #(assign, ":initiative", 100),
	        (assign, ":initiative", 80),
	      (else_try),
	        (eq, ":new_ai_state", spai_undefined),
	        (party_set_ai_behavior, ":party_no", ai_bhvr_hold),
	        (party_set_flags, ":party_no", pf_default_behavior, 0),
	      (try_end),
		  
		  #gekokujo 3.0 integrating motomataru's campaign AI start
		  (try_begin),
			(faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_attacking_enemies_around_center),
			
            (this_or_next|eq, ":new_ai_state", spai_holding_center),
	        (this_or_next|eq, ":new_ai_state", spai_engaging_army),
            (eq, ":new_ai_state", spai_patrolling_around_center),

            (party_get_position, pos1, ":new_ai_object"),
	        (party_get_position, pos3, ":party_no"),
	        (get_distance_between_positions, ":distance", pos1, pos3),

	        (try_begin),    
	          # (ge, ":distance_to_center", 800), #added new (1.122)
              (ge, ":distance", 1500),    #1.5 x patrol radius, see script_process_hero_ai below
              (assign, ":initiative", 80),	#MOTO change to 80 from 10, army is in high state of mobilization but scrambling
              (assign, ":aggressiveness", 1),
              (assign, ":courage", 8), 
            (else_try), #below added new (1.122)
              (assign, ":initiative", 100), 
              (assign, ":aggressiveness", 8),
              (assign, ":courage", 8),              
            (try_end),
          (try_end),
		  #gekokujo 3.0 integrating motomataru's campaign AI end
	      
	      (try_begin),
	        (troop_slot_eq, ":commander", slot_lord_reputation_type, lrep_martial),	
	        (val_add, ":aggressiveness", 2),
	        (val_add, ":courage", 2),
	      (else_try),
			  ##diplomacy start+ support lady personality types
			  (neg|troop_slot_eq, ":commander", slot_lord_reputation_type, lrep_adventurous),
			  (this_or_next|troop_slot_ge, ":commander", slot_lord_reputation_type, dplmc_lrep_ladies_begin),
			  ##diplomacy end+
	        (troop_slot_eq, ":commander", slot_lord_reputation_type, lrep_debauched),
	        (val_sub, ":aggressiveness", 1),
	        (val_sub, ":courage", 1),
	      (try_end),
	      
	      (party_set_slot, ":party_no", slot_party_ai_state, ":new_ai_state"),
	      (party_set_slot, ":party_no", slot_party_ai_object, ":new_ai_object"),
	      (party_set_aggressiveness, ":party_no", ":aggressiveness"),
	      (party_set_courage, ":party_no", ":courage"),
	      (party_set_ai_initiative, ":party_no", ":initiative"),
	    (try_end),
	  (try_end),

	  #Helpfulness
	  (try_begin),
	    (ge, ":commander", 0),
	  
	    (party_set_helpfulness, ":party_no", 101),
	    (try_begin),
  	      (troop_slot_eq, ":commander", slot_lord_reputation_type, lrep_martial),
 	      (party_set_helpfulness, ":party_no", 200),
	    (else_try),
  	      (troop_slot_eq, ":commander", slot_lord_reputation_type, lrep_upstanding),
	      (party_set_helpfulness, ":party_no", 150),
	    (else_try),
	      (party_slot_eq, ":party_no", slot_party_ai_state, spai_accompanying_army),
	      (party_set_helpfulness, ":party_no", 110),
	    (else_try),
	      (troop_slot_eq, ":commander", slot_lord_reputation_type, lrep_quarrelsome),
	      (party_set_helpfulness, ":party_no", 90),	  
	    (else_try),
	      (troop_slot_eq, ":commander", slot_lord_reputation_type, lrep_selfrighteous),
	      (party_set_helpfulness, ":party_no", 80),	  
	    (else_try),
	      (troop_slot_eq, ":commander", slot_lord_reputation_type, lrep_debauched),
	      (party_set_helpfulness, ":party_no", 50),
	    (try_end),	  
	  (try_end),  
  ]),
  ("cf_party_under_player_suggestion",
    [
    (store_script_param, ":party_no", 1),
	
	(party_slot_eq, ":party_no", slot_party_following_orders_of_troop, "trp_kingdom_heroes_including_player_begin"),
	
	(party_get_slot, ":ai_state", ":party_no", slot_party_ai_state),
	(party_slot_eq, ":party_no", slot_party_orders_type, ":ai_state"),

	(party_get_slot, ":ai_object", ":party_no", slot_party_ai_object),
	(party_slot_eq, ":party_no", slot_party_orders_object, ":ai_object"),
	
	(store_current_hours, ":hours_since_orders_given"),
	(party_get_slot, ":orders_time", ":party_no", slot_party_orders_time),
	
	(val_sub, ":hours_since_orders_given", ":orders_time"),
	(lt, ":hours_since_orders_given", 12),  
	]),
  #Currently called from process_ai_state, could be called from elsewhere
  #It is used for lord to (1)Court ladies (2)Collect rents (3)Look for volunteers
  ("troop_does_business_in_center", 
  [
    (store_script_param, ":troop_no", 1),
    (store_script_param, ":center_no", 2),
	##diplomacy start+
	#Call this once and reuse below.
	(call_script, "script_dplmc_is_affiliated_family_member", ":troop_no"),
	(assign, ":is_affiliated", reg0),
	#Also enable for the spouse, unless you're on bad terms
	(try_begin),
		(lt, ":is_affiliated", 0),
		(this_or_next|troop_slot_eq,":troop_no",slot_troop_spouse, "trp_player"),
			(troop_slot_eq,"trp_player",slot_troop_spouse, ":troop_no"),
		(call_script, "script_troop_get_player_relation", ":troop_no"),
		(store_skill_level, ":persuasion", "skl_persuasion", "trp_player"),
		(val_add, reg0, ":persuasion"),
		#reduce magnitude, since >= 0 succeeds
		(store_sub, ":persuasion_modifier", 20, ":persuasion"),
		(val_mul, reg0, ":persuasion_modifier"),
		(val_div, reg0, 20),
		#final number must be >= -5
		(ge, reg0, -5),
		(assign, ":is_affiliated", 1),
	(try_end),
	##diplomacy end+
    
    (troop_get_slot, ":led_party", ":troop_no", slot_troop_leaded_party),
    
    (store_current_hours, ":current_time"),
    (try_begin),
#      (party_slot_eq, ":center_no", slot_town_lord, ":troop_no"), #this was added to get lords in centers out and visiting their fiefs, but I've adjusted the decision checklist
      (is_between, ":center_no", walled_centers_begin, walled_centers_end),
      (party_set_slot, ":led_party", slot_party_last_in_any_center, ":current_time"),
      (try_begin),
        (call_script, "script_lord_get_home_center", ":troop_no"),
        (eq, ":center_no", reg0),
        (party_set_slot, ":led_party", slot_party_last_in_home_center, ":current_time"),
      (try_end),
    (try_end),
    
    #Collect the rents
    (try_begin),
      (party_slot_eq, ":center_no", slot_town_lord, ":troop_no"),
      
      (party_get_slot, ":accumulated_rents", ":center_no", slot_center_accumulated_rents),
      (party_get_slot, ":accumulated_tariffs", ":center_no", slot_center_accumulated_tariffs),
      (troop_get_slot, ":troop_wealth", ":troop_no", slot_troop_wealth),
      (val_add, ":troop_wealth", ":accumulated_rents"),
      (val_add, ":troop_wealth", ":accumulated_tariffs"),
      
      (troop_set_slot, ":troop_no", slot_troop_wealth, ":troop_wealth"),
      (party_set_slot, ":center_no", slot_center_accumulated_rents, 0),
      (party_set_slot, ":center_no", slot_center_accumulated_tariffs, 0),

	  ##diplomacy start+
	  #Modify the next block to display for affiliates
      (try_begin),
		(this_or_next|ge, ":is_affiliated", 1),#<-- dplmc+ added
        (this_or_next|eq, "$cheat_mode", 1),
        (eq, "$cheat_mode", 3),
        (assign, reg1, ":troop_wealth"),
        (str_store_party_name, s4, ":center_no"),
        (add_troop_note_from_sreg, ":troop_no", 1, "str_current_wealth_reg1_taxes_last_collected_from_s4", 0),
		#New section, print a message for affiliates:
		(ge, ":is_affiliated", 1),
		(store_add, reg0, ":accumulated_rents", ":accumulated_tariffs"),
		(str_store_troop_name, s0, ":troop_no"),
        (try_begin),
           (gt, reg0, 0),
		   (display_message, "@{s0} collects {reg0} mon from {s4}, current wealth: {reg1} mon"),
        (try_end),
      (try_end),
	  ##diplomacy end+
    (try_end),
	
	#Recruit volunteers
    (try_begin),
		#gekokujo lord recruitment start
		#(is_between, ":center_no", villages_begin, villages_end),
		(is_between, ":center_no", centers_begin, centers_end),
		#gekokujo lord recruitment end
	
        (party_get_slot, ":troop_type", ":center_no", slot_center_npc_volunteer_troop_type),
        (party_get_slot, ":troop_amount", ":center_no", slot_center_npc_volunteer_troop_amount),
        (party_set_slot, ":center_no", slot_center_npc_volunteer_troop_amount, -1),
        ##diplomacy begin
        (try_begin),
          (store_faction_of_party, ":party_faction", ":led_party"),
          (eq, ":party_faction", "fac_player_supporters_faction"),
          (is_between, "$g_player_culture", npc_kingdoms_begin, npc_kingdoms_end),
          (faction_get_slot, ":troop_type", "$g_player_culture", slot_faction_tier_1_troop),
        (try_end),

        (try_begin), #debug
          (eq, "$cheat_mode", 1),
		  ##nested diplomacy start+
		  (this_or_next|ge, ":is_affiliated", 1),#<- Show for affiliates
		  ##nested diplomacy end+
          (assign, reg2, ":troop_amount"),
          (str_store_string, s11, "@{reg2}"),
          (str_store_troop_name, s12, ":troop_type"),
          (str_store_faction_name, s13, ":party_faction"),
          (str_store_party_name, s14, ":center_no"),
          (str_store_party_name, s10, ":led_party"),
          (display_message, "@ {s10} of {s13} recruits {s11} {s12} in {s14}"),
        (try_end),
        ##diplomacy end
        (party_add_members, ":led_party", ":troop_type", ":troop_amount"),
    (try_end),
   
    #Courtship
    (try_begin),
		(party_get_slot, ":time_of_last_courtship", ":led_party", slot_party_leader_last_courted),
		(store_sub, ":hours_since_last_courtship", ":current_time", ":time_of_last_courtship"),
		(gt, ":hours_since_last_courtship", 72),

		(troop_slot_eq, ":troop_no", slot_troop_spouse, -1),
		##diplomacy start+ Disable this for inappropriate types
		(neg|is_between, ":troop_no", kingdom_ladies_begin, kingdom_ladies_end),#They use the last visited slots for other purposes
		(neg|is_between, ":troop_no", kings_begin, kings_end),#They should not be participating in this system
		(neg|is_between, ":troop_no", pretenders_begin, pretenders_end),#They should not be participating in this system
		##diplomacy end+
		(try_for_range, ":love_interest_slot", slot_troop_love_interest_1, slot_troop_love_interests_end),
			(troop_get_slot, ":love_interest", ":troop_no", ":love_interest_slot"),
			(gt, ":love_interest", 0),
			(troop_get_slot, ":love_interest_town", ":love_interest", slot_troop_cur_center),
			(eq, ":center_no", ":love_interest_town"),
			
			(call_script, "script_courtship_event_troop_court_lady", ":troop_no", ":love_interest"),
			(party_set_slot, ":led_party", slot_party_leader_last_courted, ":current_time"),
		(try_end),   
    (try_end),	
    ]),
  # script_process_kingdom_parties_ai
  # This is called more frequently than decide_kingdom_parties_ai
  # Input: none
  # Output: none
  #called from triggers
  ("process_kingdom_parties_ai",
    [
		##diplomacy start+ add support for promoted kingdom ladies
       (try_for_range, ":troop_no", heroes_begin, heroes_end),#<- change active_npcs to heroes
	   ##diplomacy end+
         (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
         (neg|troop_slot_ge, ":troop_no", slot_troop_prisoner_of_party, 0),
         (troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
         (gt, ":party_no", 0),
         (call_script, "script_process_hero_ai", ":troop_no"),
       (try_end),
  ]),
  # script_process_hero_ai
  # This is called more frequently than script_decide_kingdom_party_ais
  #Handles sieges, raids, etc -- does not change the party's basic mission.
  # Input: none
  # Output: none
  #called from triggers
  ("process_hero_ai",
    [
      (store_script_param_1, ":troop_no"),
      (troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
      (try_begin),
        (party_is_active, ":party_no"),
        (store_faction_of_party, ":faction_no", ":party_no"),
        (party_get_slot, ":ai_state", ":party_no", slot_party_ai_state),
        (party_get_slot, ":ai_object", ":party_no", slot_party_ai_object),
        (try_begin),
          (eq, ":ai_state", spai_besieging_center),
          (try_begin),
            (party_slot_eq, ":ai_object", slot_center_is_besieged_by, -1),
            (store_distance_to_party_from_party, ":distance", ":party_no", ":ai_object"),
            (lt, ":distance", 3),
            (try_begin),
              (party_slot_eq, ":party_no", slot_party_ai_state, spai_accompanying_army),
              (party_get_slot, ":commander_party", ":party_no", slot_party_ai_object),
              (party_set_slot, ":ai_object", slot_center_is_besieged_by, ":commander_party"),
            (else_try),
              (party_set_slot, ":ai_object", slot_center_is_besieged_by, ":party_no"),
            (try_end),
            (store_current_hours, ":cur_hours"),
            (party_set_slot, ":ai_object", slot_center_siege_begin_hours, ":cur_hours"),

            (str_store_party_name_link, s1, ":ai_object"),
            (str_store_troop_name_link, s2, ":troop_no"),
            (str_store_faction_name_link, s3, ":faction_no"),
            (display_log_message, "@{s1} has been besieged by {s2} of {s3}."),
            (try_begin),
              (store_faction_of_party, ":ai_object_faction", ":ai_object"),
				 ##diplomacy start+ Handle player is co-ruler of faction
				 (assign, ":is_coruler", 0),
				 (try_begin),
					(eq, ":ai_object_faction", "$players_kingdom"),
					(is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
					(call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", "$players_kingdom"),
					(ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
					(assign, ":is_coruler", 1),
				 (try_end),
				 (this_or_next|eq, ":is_coruler", 1),
				 ##diplomacy end+
              (this_or_next|party_slot_eq, ":ai_object", slot_town_lord, "trp_player"),
              (eq, ":ai_object_faction", "fac_player_supporters_faction"),
              (call_script, "script_add_notification_menu", "mnu_notification_center_under_siege", ":ai_object", ":troop_no"),
            (try_end),
            (call_script, "script_village_set_state", ":ai_object", svs_under_siege),
            (assign, "$g_recalculate_ais", 1),
          (try_end),
        (else_try),
          (eq, ":ai_state", spai_raiding_around_center),
          (party_slot_eq, ":party_no", slot_party_ai_substate, 0),
          (assign, ":selected_village", 0),
          (try_for_range, ":enemy_village_no", villages_begin, villages_end),
            (eq, ":selected_village", 0),
            (store_faction_of_party, ":enemy_village_faction", ":enemy_village_no"),
            (try_begin),
              (party_slot_eq, ":enemy_village_no", slot_town_lord, "trp_player"),
              (store_relation, ":reln", "fac_player_supporters_faction", ":faction_no"),
            (else_try),
              (store_relation, ":reln", ":enemy_village_faction", ":faction_no"),
            (try_end),
            (lt, ":reln", 0),
            (store_distance_to_party_from_party, ":dist", ":enemy_village_no", ":party_no"),
            (lt, ":dist", 15),
            (party_slot_eq, ":enemy_village_no", slot_village_state, 0), #village is not already raided
            #CHANGE STATE TO RAID THIS VILLAGE
            (assign, ":selected_village", ":enemy_village_no"),
          (try_end),
          (try_begin),
            (eq, ":selected_village", 0),
            (is_between, ":ai_object", villages_begin, villages_end),
            (assign, ":selected_village", ":ai_object"),
          (try_end),
          (try_begin),
            (gt, ":selected_village", 0),
            (call_script, "script_party_set_ai_state", ":party_no", spai_raiding_around_center, ":selected_village"),
            (try_begin),
              (faction_slot_eq, ":faction_no", slot_faction_marshall, ":troop_no"),
              (faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_raiding_village),
              (faction_set_slot, ":faction_no", slot_faction_ai_object, ":selected_village"),
            (try_end),
            (party_get_position, pos1, ":selected_village"),
            (map_get_random_position_around_position, pos2, pos1, 1),
            (party_set_ai_behavior, ":party_no", ai_bhvr_travel_to_point),
            (party_set_ai_target_position, ":party_no", pos2),
            (party_set_ai_object, ":party_no", ":selected_village"),
            (party_set_slot, ":party_no", slot_party_ai_substate, 1),
          (try_end),
        (else_try),
          (eq, ":ai_state", spai_raiding_around_center),#substate is 1
          (try_begin),                                
            (store_distance_to_party_from_party, ":distance", ":party_no", ":ai_object"),
            (lt, ":distance", 2),
            (try_begin),
              (party_slot_eq, ":ai_object", slot_village_state, 0),
              (call_script, "script_village_set_state", ":ai_object", svs_being_raided),
              (party_set_slot, ":ai_object", slot_village_raided_by, ":party_no"),
              (try_begin),
                (store_faction_of_party, ":village_faction", ":ai_object"),
				 ##diplomacy start+ Handle player is co-ruler of faction
				 (assign, ":is_coruler", 0),
				 (try_begin),
					(eq, ":village_faction", "$players_kingdom"),
					(is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
					(call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", "$players_kingdom"),
					(ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
					(assign, ":is_coruler", 1),
				 (try_end),
				 (this_or_next|eq, ":is_coruler", 1),
				 ##diplomacy end+
                (this_or_next|party_slot_eq, ":ai_object", slot_town_lord, "trp_player"),
                (eq, ":village_faction", "fac_player_supporters_faction"),
                (store_distance_to_party_from_party, ":dist", "p_main_party", ":ai_object"),
                (this_or_next|lt, ":dist", 30),
                (party_slot_eq, ":ai_object", slot_center_has_messenger_post, 1),
                (call_script, "script_add_notification_menu", "mnu_notification_village_raid_started", ":ai_object", ":troop_no"),
              (try_end),
            (else_try),
              (party_slot_eq, ":ai_object", slot_village_state, svs_being_raided),
            (else_try),
              #if anything other than being_raided leave
              (party_set_slot, ":party_no", slot_party_ai_substate, 0),
            (try_end),
          (try_end),
        (else_try),
          (eq, ":ai_state", spai_retreating_to_center),
          (try_begin),
            (party_get_battle_opponent, ":enemy_party", ":party_no"),
            (ge, ":enemy_party", 0), #we are in a battle! we may be caught in a loop!
            (call_script, "script_party_set_ai_state", ":party_no", spai_undefined, -1),
            (party_set_flags, ":party_no", pf_default_behavior, 0),
            (party_set_slot, ":party_no", slot_party_commander_party, -1),
          (try_end),
		#gekokujo 3.0 integrating motomataru's campaign AI start
        #(else_try),
        #  (eq, ":ai_state", spai_patrolling_around_center),
        #            
        #  (try_begin),
        #    (party_slot_eq, ":party_no", slot_party_ai_substate, 0),
        #    (store_distance_to_party_from_party, ":distance", ":party_no", ":ai_object"),
        #    (lt, ":distance", 6),
        #    (party_set_slot, ":party_no", slot_party_ai_substate, 1),
        #            
	    #    (party_set_aggressiveness, ":party_no", 8),
	    #    (party_set_courage, ":party_no", 8),
	    #    (party_set_ai_initiative, ":party_no", 100),
	    #                
        #    (party_set_ai_behavior, ":party_no", ai_bhvr_patrol_party),
        #    (party_set_ai_object, ":party_no", ":ai_object"),
        #  (try_end),
        #(else_try),
        #  (eq, ":ai_state", spai_holding_center),
        #(try_end),
		#gekokujo 3.0 integrating motomataru's campaign AI end
      (try_end),
	  
	  #gekokujo 3.0 integrating motomataru's campaign AI start
	  (try_begin),
		  (ge, ":ai_object", 0),
		  (neg|party_is_active, ":ai_object"),	#object was eliminated
		  (call_script, "script_npc_decision_checklist_party_ai", ":troop_no"),
		  (assign, ":ai_state", reg0),
		  (assign, ":ai_object", reg1),
		  (call_script, "script_party_set_ai_state", ":party_no", ":ai_state", ":ai_object"),
		(try_end),
		
		#state changes
		(assign, ":initiative", 0),	#test variable
		
		#start fights between passing armies
		(try_begin),
		  (faction_slot_eq, ":faction_no", slot_faction_marshall, ":troop_no"),
		  (assign, ":enemy_distance", 1000),
		  
		  (try_for_range, ":enemy_faction", kingdoms_begin, kingdoms_end),
			(store_relation, ":reln", ":faction_no", ":enemy_faction"),
			(lt, ":reln", 0),
			(faction_get_slot, ":enemy_marshal", ":enemy_faction", slot_faction_marshall),
			(ge, ":enemy_marshal", 0),
			(troop_get_slot, ":enemy_marshal_party", ":enemy_marshal", slot_troop_leaded_party),
			(party_is_active, ":enemy_marshal_party"),
			(store_distance_to_party_from_party, ":distance", ":party_no", ":enemy_marshal_party"),
			(gt, ":enemy_distance", ":distance"),
			(assign, ":enemy_distance", ":distance"),
		  (try_end),
		  
		  (lt, ":distance", 25),
		  
		  (try_begin),
			(faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_attacking_enemies_around_center),
			(assign, ":aggressiveness", 8),
			(assign, ":courage", 8),
			(assign, ":initiative", 100),
		  (else_try),
			(assign, ":aggressiveness", 8),
			(assign, ":courage", 5),	#in enemy territory
			(assign, ":initiative", 100),
		  (try_end),

		(else_try),
		  (ge, ":ai_object", 0),
		  (party_is_active, ":ai_object"),
		  
		  (try_begin),
			(eq, ":ai_state", spai_accompanying_army),
			(party_get_battle_opponent, ":commander_opponent", ":ai_object"),
			(lt, ":commander_opponent", 0),	#commander not in a fight?
			(party_get_slot, ":commander_ai_object", ":ai_object", slot_party_ai_object),
			(try_begin),
			  (party_is_active, ":commander_ai_object"),
			  (store_distance_to_party_from_party, ":distance", ":party_no", ":commander_ai_object"),
			(else_try),
			  (assign, ":distance", 1000),
			(try_end),
		  (else_try),
			(store_distance_to_party_from_party, ":distance", ":party_no", ":ai_object"),
		  (try_end),
		  
		  #defensive emergency
		  (try_begin),
			(faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_attacking_enemies_around_center),
			(try_begin),
			  (le, ":distance", 15),	#1.5 x patrol radius
			  
			  (try_begin),
				(this_or_next|eq, ":ai_state", spai_engaging_army),
				(eq, ":ai_state", spai_patrolling_around_center),
				(assign, ":aggressiveness", 8),
				(assign, ":courage", 8),
				(assign, ":initiative", 100),
				(try_begin),
				  (eq, ":ai_state", spai_patrolling_around_center),
				  (party_slot_eq, ":party_no", slot_party_ai_substate, 0),
				  (party_set_slot, ":party_no", slot_party_ai_substate, 1),
				  (party_set_ai_behavior, ":party_no", ai_bhvr_patrol_party),
				  (party_set_ai_object, ":party_no", ":ai_object"),
				  (party_set_ai_patrol_radius, ":party_no", 1),
				(try_end),
				
			  (else_try),
				(eq, ":ai_state", spai_accompanying_army),
				(party_get_slot, ":commander_ai_state", ":ai_object", slot_party_ai_state),
				(this_or_next|ge, ":commander_opponent", 0),	#commander in a fight?
				(this_or_next|eq, ":commander_ai_state", spai_engaging_army),
				(eq, ":commander_ai_state", spai_patrolling_around_center),
				(assign, ":aggressiveness", 8),
				(assign, ":courage", 8),
				(assign, ":initiative", 100),
			  (try_end),
			(try_end),
			
		  #reach objective
		  (else_try),
			(eq, ":ai_state", spai_holding_center),
			(party_is_in_any_town, ":party_no"),
			(assign, ":aggressiveness", 5),
			(assign, ":courage", 8),
			(assign, ":initiative", 50),
			
		  (else_try),
			(eq, ":ai_state", spai_besieging_center),
			(le, ":distance", 3),
			(assign, ":aggressiveness", 1),
			(assign, ":courage", 5),
			(assign, ":initiative", 20),
			
		  (else_try),
			(eq, ":ai_state", spai_visiting_village),
			(le, ":distance", 3),
			(assign, ":aggressiveness", 5),
			(assign, ":courage", 8),
			(assign, ":initiative", 50),

		  (else_try),
			(eq, ":ai_state", spai_patrolling_around_center),
			(le, ":distance", 15),	#1.5 x patrol radius
			(party_slot_eq, ":party_no", slot_party_ai_substate, 0),
			(party_set_slot, ":party_no", slot_party_ai_substate, 1),
			(assign, ":aggressiveness", 8),
			(assign, ":courage", 8),
			(assign, ":initiative", 80),
			(party_set_ai_behavior, ":party_no", ai_bhvr_patrol_party),
			(party_set_ai_object, ":party_no", ":ai_object"),
			(party_set_ai_patrol_radius, ":party_no", 1),
			
		  (else_try),
			(eq, ":ai_state", spai_accompanying_army),
			(party_get_slot, ":commander_ai_state", ":ai_object", slot_party_ai_state),
			(this_or_next|ge, ":commander_opponent", 0),	#commander in a fight?
			(this_or_next|eq, ":commander_ai_state", spai_engaging_army),
			(eq, ":commander_ai_state", spai_raiding_around_center),
			(le, ":distance", 15),	#1.5 x patrol radius
			(assign, ":aggressiveness", 8),
			(assign, ":courage", 5),
			(assign, ":initiative", 100),
		  (try_end),
		(try_end),
		  
		#set new values
		(try_begin),
		  (gt, ":initiative", 0),
			
		  (try_begin),
			(troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_martial),
			(val_add, ":aggressiveness", 2),
			(val_add, ":courage", 2),
		  (else_try),
			(troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_debauched),
			(val_sub, ":aggressiveness", 1),
			(val_sub, ":courage", 1),
		  (try_end),

		  (party_set_aggressiveness, ":party_no", ":aggressiveness"),
		  (party_set_courage, ":party_no", ":courage"),
		  (party_set_ai_initiative, ":party_no", ":initiative"),
		(try_end),
		#MOTO end rewrite to update ALL states from script_party_set_ai_state when objective reached or eliminated
	  (try_end),
	  #gekokujo 3.0 integrating motomataru's campaign AI end
  ]),
  # script_begin_assault_on_center
  # Input: arg1: faction_no
  # Output: none
  #called from triggers
  ("begin_assault_on_center",
   [
     (store_script_param, ":center_no", 1),
	 ##diplomacy start+ add support for promoted kingdom ladies
     (try_for_range, ":troop_no", heroes_begin, heroes_end),#<- change active_npcs to heroes
	 ##diplomacy end+
       (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
       (neg|troop_slot_ge, ":troop_no", slot_troop_prisoner_of_party, 0),
       (troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
       (gt, ":party_no", 0),
       (party_is_active, ":party_no"),

       (assign, ":continue", 0),
       (try_begin),
         (party_slot_eq, ":party_no", slot_party_ai_state, spai_besieging_center),
         (party_slot_eq, ":party_no", slot_party_ai_object, ":center_no"),
         (party_slot_eq, ":party_no", slot_party_ai_substate, 0),
         (assign, ":continue", 1),
       (else_try),
         (party_slot_eq, ":party_no", slot_party_ai_state, spai_accompanying_army),
         (party_get_slot, ":commander_party", ":party_no", slot_party_ai_object),
         (gt, ":commander_party", 0),
         (party_is_active, ":commander_party"),
         (party_slot_eq, ":commander_party", slot_party_ai_state, spai_besieging_center),
         (party_slot_eq, ":commander_party", slot_party_ai_object, ":center_no"),
         (call_script, "script_party_set_ai_state", ":party_no", spai_besieging_center, ":center_no"),
         (assign, ":continue", 1),
       (try_end),

       (eq, ":continue", 1),

       (party_set_ai_behavior, ":party_no", ai_bhvr_attack_party),
       (party_set_ai_object, ":party_no", ":center_no"),
       (party_set_flags, ":party_no", pf_default_behavior, 1),
       (party_set_slot, ":party_no", slot_party_ai_substate, 1),
     (try_end),
   ]),
  #DEPRECATED - Using new political issue system instead
  ("select_faction_marshall",
   [
#     (store_script_param_1, ":faction_no"),
 #    (faction_get_slot, ":faction_leader", ":faction_no", slot_faction_leader),
  #   (faction_get_slot, ":old_faction_marshall", ":faction_no", slot_faction_marshall),
     
   #  (assign, ":old_marshal_is_avaliable", 0),
    # (try_begin),
     #  (gt, ":old_faction_marshall", 0),
      # (troop_get_slot, ":old_marshal_party", ":old_faction_marshall", slot_troop_leaded_party),
     #  (party_is_active, ":old_marshal_party"),
    #   (assign, ":old_marshal_is_avaliable", 1),
   #  (try_end),
     
     #Ozan : I am adding some codes here because sometimes armies demobilize during last seconds of an 
	 #important event like taking a castle, ext because of marshal change. When marshal changes during 
	 #an important event occurs new marshal's followers become 0 and continueing siege attack seems less 
	 #valuable then armies demobilize, faction ai become "do nothing", "I cannot think anything to do" ext.
		
   #  (assign, ":there_is_an_important_situation", 0),
   #  (faction_get_slot, ":current_ai_object", ":faction_no", slot_faction_ai_object),            
     
   #  (try_begin), #do not demobilize during taking a castle/town (fighting in the castle)
   #    (is_between, ":current_ai_object", walled_centers_begin, walled_centers_end),
   #    (party_get_battle_opponent, ":besieger_party", ":current_ai_object"),
   #    (ge, ":besieger_party", 0),
   #    (party_is_active, ":besieger_party"),
   #    (store_faction_of_party, ":besieger_faction", ":besieger_party"),
   #    (this_or_next|eq, ":besieger_faction", ":faction_no"),
   #    (eq, ":besieger_faction", "fac_player_faction"),
   #    (assign, ":there_is_an_important_situation", 1),
   #  (try_end),

   #  (try_begin), #do not demobilize during raiding a village (holding around village)
   #    (is_between, ":current_ai_object", centers_begin, centers_end),
   #    (neg|is_between, ":current_ai_object", walled_centers_begin, walled_centers_end),		  
   #    (party_slot_eq, ":current_ai_object", slot_village_state, svs_being_raided),
   #    (assign, ":there_is_an_important_situation", 1),
   #  (try_end),

   #  (try_begin), #do not demobilize during besigning a siege (holding around castle)
   #    (is_between, ":current_ai_object", walled_centers_begin, walled_centers_end),
   #    #(str_store_party_name, s7, ":current_ai_object"),
   #    (party_get_slot, ":besieger_party", ":current_ai_object", slot_center_is_besieged_by),
   #    (ge, ":besieger_party", 0),
   #    (party_is_active, ":besieger_party"),
   #    #(str_store_party_name, s7, ":besieger_party"),
   #    (store_faction_of_party, ":besieger_faction", ":besieger_party"),
   #    (this_or_next|eq, ":besieger_faction", ":faction_no"),
   #    (eq, ":besieger_faction", "fac_player_faction"),		  
   #    (assign, ":there_is_an_important_situation", 1),
   #  (try_end),
     
   #  (try_begin),   
   #    (this_or_next|eq, ":there_is_an_important_situation", 0),
   #    (eq, ":old_marshal_is_avaliable", 0),
       #end addition ozan
   
   
    #   (assign, ":total_renown", 0),
    #   (try_for_range, ":loop_var", active_npcs_including_player_begin, active_npcs_end),
    #     (assign, ":cur_troop", ":loop_var"),
    #     (assign, ":continue", 0),
    #     (try_begin),
    #       (eq, ":loop_var", "trp_kingdom_heroes_including_player_begin"),
    #       (assign, ":cur_troop", "trp_player"),
    #       (try_begin),
    #         (eq, ":faction_no", "$players_kingdom"),
    #         (assign, ":continue", 1),
    #       (try_end),
    #     (else_try),
    #       (troop_slot_eq, ":cur_troop", slot_troop_occupation, slto_kingdom_hero),
    #       (store_troop_faction, ":cur_faction", ":cur_troop"),
    #       (eq, ":cur_faction", ":faction_no"),
    #       (troop_get_slot, ":cur_party", ":cur_troop", slot_troop_leaded_party),
    #       (gt, ":cur_party", 0),
    #       (party_is_active, ":cur_party"),
    #       (call_script, "script_party_count_fit_for_battle", ":cur_party"),
    #       (assign, ":party_fit_for_battle", reg0),
    #       (call_script, "script_party_get_ideal_size", ":cur_party"),
    #       (assign, ":ideal_size", reg0),
    #       (store_mul, ":relative_strength", ":party_fit_for_battle", 100),
    #       (val_div, ":relative_strength", ":ideal_size"),
    #       (ge, ":relative_strength", 25),
    #       (assign, ":continue", 1),
    #     (try_end),
         
     #    (eq, ":continue", 1),
	   
    #     (troop_get_slot, ":renown", ":cur_troop", slot_troop_renown),
	#     (call_script, "script_troop_get_relation_with_troop", ":cur_troop", ":faction_leader"),
	#     (store_mul, ":relation_modifier", reg0, 15),
	#     (val_add, ":renown", ":relation_modifier"),
	#     (val_max, ":renown", 1),
	#   
    #     (try_begin),
    #       (eq, ":cur_troop", "trp_player"),
    #       (neq, ":old_faction_marshall", "trp_player"),
    #       (assign, ":renown", 0),
   #      (try_end),
    #     (try_begin),
    #       (eq, ":cur_troop", ":faction_leader"),
    #       (val_mul, ":renown", 3),
    #       (val_div, ":renown", 4),
    #     (try_end),
    #     (try_begin),
    #       (eq, ":cur_troop", ":old_faction_marshall"),
    #       (val_mul, ":renown", 1000),
    #     (try_end),
    #     (val_add, ":total_renown", ":renown"),
    #   (try_end),
    #   (assign, ":result", -1),
    #   (try_begin),
    #     (gt, ":total_renown", 0),
    #     (store_random_in_range, ":random_renown", 0, ":total_renown"),
    #     (try_for_range, ":loop_var", active_npcs_including_player_begin, active_npcs_end),
    #       (eq, ":result", -1),
    #       (assign, ":cur_troop", ":loop_var"),
    #       (assign, ":continue", 0),
    #       (try_begin),
    #         (eq, ":loop_var", "trp_kingdom_heroes_including_player_begin"),
    #         (assign, ":cur_troop", "trp_player"),
   #          (try_begin),
   #            (eq, ":faction_no", "$players_kingdom"),
   #            (assign, ":continue", 1),
   #          (try_end),
   #        (else_try),
   #          (troop_slot_eq, ":cur_troop", slot_troop_occupation, slto_kingdom_hero),
   #          (store_troop_faction, ":cur_faction", ":cur_troop"),
   #          (eq, ":cur_faction", ":faction_no"),
   #          (troop_get_slot, ":cur_party", ":cur_troop", slot_troop_leaded_party),
   #          (gt, ":cur_party", 0),
   #          (party_is_active, ":cur_party"),
   #          (call_script, "script_party_count_fit_for_battle", ":cur_party"),
   #          (assign, ":party_fit_for_battle", reg0),
      #       (call_script, "script_party_get_ideal_size", ":cur_party"),
      #       (assign, ":ideal_size", reg0),
      #       (store_mul, ":relative_strength", ":party_fit_for_battle", 100),
      #       (val_div, ":relative_strength", ":ideal_size"),
      #       (ge, ":relative_strength", 25),
      #       (assign, ":continue", 1),
      #     (try_end),
      #     (eq, ":continue", 1),

		#   (troop_get_slot, ":renown", ":cur_troop", slot_troop_renown),
	    #   (call_script, "script_troop_get_relation_with_troop", ":cur_troop", ":faction_leader"),
	    #   (store_mul, ":relation_modifier", reg0, 15),
	    #   (val_add, ":renown", ":relation_modifier"),
	    #   (val_max, ":renown", 1),
		# 
        #   (try_begin),
        #     (eq, ":cur_troop", "trp_player"),
        #     (neq, ":old_faction_marshall", "trp_player"),
        #     (assign, ":renown", 0),
        #   (try_end),
        #   (try_begin),
        #     (eq, ":cur_troop", ":faction_leader"),
        #     (val_mul, ":renown", 3),
         #    (val_div, ":renown", 4),
         #  (try_end),
         #  (try_begin),
       #      (eq, ":cur_troop", ":old_faction_marshall"),
       #      (val_mul, ":renown", 1000),
       #    (try_end),
       #    (val_sub, ":random_renown", ":renown"),
       #    (lt, ":random_renown", 0),
       #    (assign, ":result", ":cur_troop"),
       #  (try_end),
      # (try_end),
      # (try_begin),
         #(eq, "$cheat_mode", 1),
        # (ge, ":result", 0),
       #  (str_store_troop_name, s1, ":result"),
      #   (str_store_faction_name, s2, ":faction_no"),
     #    (display_message, "@{!}{s1} is chosen as the marshall of {s2}."),
    #   (try_end),
   #  (else_try),
   #    (faction_get_slot, ":old_faction_marshall", ":faction_no", slot_faction_marshall),
   #    (assign, ":result", ":old_faction_marshall"),
   #  (try_end),
     
   #  (assign, reg0, ":result"),
     ]),
  # script_get_center_faction_relation_including_player
  # Input: arg1: center_no, arg2: target_faction_no
  # Output: reg0: relation
  #called from triggers
  ("get_center_faction_relation_including_player",
   [
     (store_script_param, ":center_no", 1),
     (store_script_param, ":target_faction_no", 2),
     (store_faction_of_party, ":center_faction", ":center_no"),
     (store_relation, ":relation", ":center_faction", ":target_faction_no"),
     (try_begin),
       (party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
       (store_relation, ":relation", "fac_player_supporters_faction", ":target_faction_no"),
     (try_end),
     (assign, reg0, ":relation"),
     ]),
  # script_decide_faction_ai
  # Input: arg1: faction_no
  # Output: none
  #called from triggers
  ("decide_faction_ai",
  #This handles political issues and faction issues
   [
    (store_script_param_1, ":faction_no"),
	   
	   
    (faction_get_slot, ":old_faction_ai_state", ":faction_no", slot_faction_ai_state),
    (faction_get_slot, ":old_faction_ai_object", ":faction_no", slot_faction_ai_object),
	(faction_get_slot, ":faction_marshal", ":faction_no", slot_faction_marshall),

	 
	#Remove marshal if he has become too controversial,, or he has defected, or has been taken prisoner
	(try_begin),
        (faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
		(neq, ":faction_no", "fac_player_supporters_faction"),
		(ge, ":faction_marshal", "trp_player"),
		
		(store_faction_of_troop, ":marshal_faction", ":faction_marshal"),
		(try_begin),
			(eq, ":faction_marshal", "trp_player"),
			(assign, ":marshal_faction", "$players_kingdom"),
		(try_end),
		
		
		(assign, ":player_marshal_is_prisoner", 0),
		(try_begin),
			(eq, ":faction_marshal", "trp_player"),
			(eq, "$g_player_is_captive", 1),
			(assign, ":player_marshal_is_prisoner", 1),
		(try_end),
		
		
		#High controversy level, or marshal has defected, or is prisoner
		(this_or_next|neq, ":marshal_faction", ":faction_no"),		
		(this_or_next|troop_slot_ge, ":faction_marshal", slot_troop_controversy, 80),
		(this_or_next|eq, ":player_marshal_is_prisoner", 1),
			(troop_slot_ge, ":faction_marshal", slot_troop_prisoner_of_party, 0),
		
		(assign, ":few_following_player_campaign", 0),
		(try_begin),
			(eq, ":faction_marshal", "trp_player"),
			(assign, ":vassals_following_player_campaign", 0),
			(gt, "$g_player_days_as_marshal", 1),
			(try_for_range, ":vassal", active_npcs_begin, active_npcs_end),
				(troop_slot_eq, ":vassal", slot_troop_occupation, slto_kingdom_hero),
				(store_faction_of_troop, ":vassal_faction", ":vassal"),
				(eq, ":vassal_faction", ":faction_no"),
				(call_script, "script_npc_decision_checklist_troop_follow_or_not", ":vassal"),
				(eq, reg0, 1),
				(val_add, ":vassals_following_player_campaign", 1),
			(try_end),
			(lt, ":vassals_following_player_campaign", 4),
			(assign, ":few_following_player_campaign", 1),
		(try_end),
		
		#Only remove marshal for controversy if offensive campaign in progress
		(this_or_next|eq, ":old_faction_ai_state", sfai_default),
		(this_or_next|eq, ":old_faction_ai_state", sfai_feast),		
		(this_or_next|neq, ":marshal_faction", ":faction_no"),
		(this_or_next|eq, ":few_following_player_campaign", 1),
		(this_or_next|eq, ":player_marshal_is_prisoner", 1),
			(troop_slot_ge, ":faction_marshal", slot_troop_prisoner_of_party, 0),
		
		#No current issue on the agenda
		(this_or_next|faction_slot_eq, ":faction_no", slot_faction_political_issue, 0),
		(this_or_next|eq, ":player_marshal_is_prisoner", 1),
			(troop_slot_ge, ":faction_marshal", slot_troop_prisoner_of_party, 0),
		
		(faction_set_slot, ":faction_no", slot_faction_political_issue, 1), #Appointment of marshal
		(store_current_hours, ":hours"),
		(val_max, ":hours", 0),
		(faction_set_slot, ":faction_no", slot_faction_political_issue_time, ":hours"), #Appointment of marshal
		
        (faction_get_slot, ":old_marshall", ":faction_no", slot_faction_marshall),
        (try_begin),
		  (ge, ":old_marshall", 0),
		  (troop_get_slot, ":old_marshall_party", ":old_marshall", slot_troop_leaded_party),
          (party_is_active, ":old_marshall_party"),
          (party_set_marshall, ":old_marshall_party", 0),
        (try_end),  

		(try_begin),
			(eq, "$players_kingdom", ":faction_no"),
			(faction_slot_eq, "$players_kingdom", slot_faction_marshall, "trp_player"),
			(call_script, "script_add_notification_menu", "mnu_notification_relieved_as_marshal", 0, 0),
		(else_try),
			(neq, ":old_marshall", "trp_player"),
			(call_script, "script_change_troop_renown", ":old_marshall", 15),
		(try_end),
		(faction_set_slot, ":faction_no", slot_faction_marshall, -1),
		(assign, ":faction_marshal", -1),
		
		
		##diplomacy start+ add support for promoted kingdom ladies
		(try_for_range, ":active_npc", heroes_begin, heroes_end),#<- change active_npcs to heroes
		##diplomacy end+
			(store_faction_of_troop, ":active_npc_faction", ":active_npc"),
			(eq, ":active_npc_faction", ":faction_no"),
			(troop_set_slot, ":active_npc", slot_troop_stance_on_faction_issue, -1),
		(try_end),		
		(try_begin),
			(eq, "$players_kingdom", ":faction_no"),
			(troop_set_slot, "trp_player", slot_troop_stance_on_faction_issue, -1),
		(try_end),
		
	(else_try),	 #If marshal not present, and not already on agenda, make political issue
		(eq, ":faction_marshal", -1),
		(neg|faction_slot_ge, ":faction_no", slot_faction_political_issue, 1), #This to avoid resetting votes every time
	
        (faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
		(neq, ":faction_no", "fac_player_supporters_faction"),
		
		(faction_set_slot, ":faction_no", slot_faction_political_issue, 1), #Appointment of marshal
		(store_current_hours, ":hours"),
		(val_max, ":hours", 0),
		(faction_set_slot, ":faction_no", slot_faction_political_issue_time, ":hours"), #Appointment of marshal
		
		##diplomacy start+ add support for promoted kingdom ladies
		(try_for_range, ":active_npc", heroes_begin, heroes_end),#<- change active_npcs to heroes
		##diplomacy end+
			(store_faction_of_troop, ":active_npc_faction", ":active_npc"),
			(eq, ":active_npc_faction", ":faction_no"),
			(troop_set_slot, ":active_npc", slot_troop_stance_on_faction_issue, -1),
		(try_end),		
		(try_begin),
			(eq, "$players_kingdom", ":faction_no"),
			(troop_set_slot, "trp_player", slot_troop_stance_on_faction_issue, -1),
		(try_end),
		
		
	(else_try),	#If player is marshal, but not part of faction
		(eq, ":faction_marshal", "trp_player"),
		(neq, "$players_kingdom", ":faction_no"),

                (faction_set_slot, ":faction_no", slot_faction_political_issue, 1), #Appointment of marshal
		(store_current_hours, ":hours"),
		(val_max, ":hours", 0),
		(faction_set_slot, ":faction_no", slot_faction_political_issue_time, ":hours"), #Appointment of marshal

        (faction_get_slot, ":old_marshall", ":faction_no", slot_faction_marshall),
        (try_begin),
		  (ge, ":old_marshall", 0),
		  (troop_get_slot, ":old_marshall_party", ":old_marshall", slot_troop_leaded_party),
          (party_is_active, ":old_marshall_party"),
          (party_set_marshall, ":old_marshall_party", 0),
        (try_end),  

		(faction_set_slot, ":faction_no", slot_faction_marshall, -1),
		(assign, ":faction_marshal", -1),
		
		##diplomacy start+ add support for promoted kingdom ladies
		(try_for_range, ":active_npc", heroes_begin, heroes_end),#<- change active_npcs to heroes
		##diplomacy end+
			(store_faction_of_troop, ":active_npc_faction", ":active_npc"),
			(eq, ":active_npc_faction", ":faction_no"),
			(troop_set_slot, ":active_npc", slot_troop_stance_on_faction_issue, -1),
		(try_end),		
		(try_begin),
			(eq, "$players_kingdom", ":faction_no"),
			(troop_set_slot, "trp_player", slot_troop_stance_on_faction_issue, -1),
		(try_end),
		
	(try_end),
	 
	#If the faction issue is a center no longer under faction control, remove and reset 
	(try_begin), 
		(faction_get_slot, ":faction_political_issue", ":faction_no", slot_faction_political_issue),
		(is_between, ":faction_political_issue", centers_begin, centers_end),
		(store_faction_of_party, ":disputed_center_faction", ":faction_political_issue"),
		(neq, ":disputed_center_faction", ":faction_no"),
		
		(try_begin),
			(eq, "$cheat_mode", 1),
			(str_store_faction_name, s4, ":faction_no"),
			(str_store_party_name, s5, ":disputed_center_faction"),
			(display_message, "@{!}DEBUG -- {s4} drops {s5} as issue as it has changed hands"),
		(try_end),
		
		#Reset political issue
		(faction_set_slot, ":faction_no", slot_faction_political_issue, 0),
		##diplomacy start+ add support for promoted kingdom ladies
		(try_for_range, ":active_npc", heroes_begin, heroes_end),#<- change active_npcs to heroes
		##diplomacy end+
			(store_faction_of_troop, ":active_npc_faction", ":active_npc"),
			(eq, ":active_npc_faction", ":faction_no"),
			(troop_set_slot, ":active_npc", slot_troop_stance_on_faction_issue, -1),
		(try_end),		
		(try_begin),
			(eq, "$players_kingdom", ":faction_no"),
			(troop_set_slot, "trp_player", slot_troop_stance_on_faction_issue, -1),
		(try_end),
		
	(try_end),
	
	
	#Resolve the political issue on the agenda
	(try_begin),
		(faction_slot_ge, ":faction_no", slot_faction_political_issue, 1),
		(neq, ":faction_no", "fac_player_supporters_faction"),
		
		#Do not switch marshals during a campaign
		(this_or_next|faction_slot_ge, ":faction_no", slot_faction_political_issue, centers_begin),
		(this_or_next|faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_default),
			(faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_feast),
		
		
		(faction_get_slot, ":faction_leader", ":faction_no", slot_faction_leader),
		
		(assign, ":total_lords", 0),
		(assign, ":lords_who_have_voted", 0),
		(assign, ":popular_favorite", -1),
	
		#Reset number of votes
		(troop_set_slot, "trp_player", slot_troop_temp_slot, 0),
		##diplomacy start+ add support for promoted kingdom ladies
		(try_for_range, ":active_npc", heroes_begin, heroes_end),#<- change active_npcs to heroes
		##diplomacy end+
			(troop_set_slot, ":active_npc", slot_troop_temp_slot, 0),
		(try_end),

		#Tabulate votes

		##diplomacy start+
		(try_begin),#count the player's vote
			(eq, "$players_kingdom", ":faction_no"),
			(ge, "$player_has_homage", 1),
			(troop_get_slot, ":lord_chosen_candidate", "trp_player", slot_troop_stance_on_faction_issue),
      			(gt, ":lord_chosen_candidate", -1),
			#You may notice that I don't count the player for "total_lords" if he was undecided.
			#This is so faction behavior will not be changed from Native if the player did not
			#support anyone.
			(val_add, ":total_lords", 1),
			(val_add, ":lords_who_have_voted", 1),
			(troop_set_slot, ":lord_chosen_candidate", slot_troop_temp_slot, 1),
			(assign, ":popular_favorite", ":lord_chosen_candidate"),
		(try_end),
		#add support for promoted kingdom ladies
		(try_for_range, ":voting_lord", heroes_begin, heroes_end),#<- changed active_npcs_begin/end to heroes_begin/end
			(this_or_next|troop_slot_eq, ":voting_lord", slot_troop_occupation, slto_kingdom_hero),
				(is_between, ":voting_lord", active_npcs_begin, active_npcs_end),
		       	#the dead / retired / exiled do not vote
			(neg|troop_slot_ge, ":voting_lord", slot_troop_occupation, slto_retirement),
		##diplomacy end+
			(store_faction_of_troop, ":voting_lord_faction", ":voting_lord"),
			(eq, ":voting_lord_faction", ":faction_no"),
			(val_add, ":total_lords", 1),
			(troop_get_slot, ":lord_chosen_candidate", ":voting_lord", slot_troop_stance_on_faction_issue),								
			(gt, ":lord_chosen_candidate", -1),									
			(val_add, ":lords_who_have_voted", 1),			
			(troop_get_slot, ":total_votes", ":lord_chosen_candidate", slot_troop_temp_slot),
			(val_add, ":total_votes", 1),
			(troop_set_slot, ":lord_chosen_candidate", slot_troop_temp_slot, ":total_votes"),			
			(try_begin),
				(gt, ":popular_favorite", -1),
				(troop_get_slot, ":current_winner_votes", ":popular_favorite", slot_troop_temp_slot),
				(gt, ":total_votes", ":current_winner_votes"),
				(assign, ":popular_favorite", ":lord_chosen_candidate"),
			(else_try),	
				(eq, ":popular_favorite", -1),
				(assign, ":popular_favorite", ":lord_chosen_candidate"),
			(try_end),
		(try_end),	

		#Check to see if enough lords have voted
		(store_div, ":number_required_for_quorum", ":total_lords", 5),
		(val_mul, ":number_required_for_quorum", 4),
		##diplomacy start+
		#Replace number required for quorum, altering it based on the centralization
		#value.  Do the same for the minimum time left on the agenda.
		(faction_get_slot, ":centralization", ":faction_no", dplmc_slot_faction_centralization),
		(val_clamp, ":centralization", -3, 4),
		(try_begin),
			#Disable this for now, since NPC kingdoms set their policies randomly.
			(eq, 0, 1),
			(neq, ":centralization", 0),
			(store_sub, ":number_required_for_quorum", 15, ":centralization"),#fully centralized = 12/20 , fully decentralized = 18/20
			(try_begin),
				#If the plutocracy/aristocracy slider is negative, allow it to offset
				#a negative centralization value for the purpose of quorum, on the
				#assumption that part of the "quorum" is accounted for by the influence
				#of merchants.  They do not vote currently, although integrating guild masters
				#and/or village elders into the faction issue system is something to consider
				#for the future.
				(ge, ":number_required_for_quorum", 16),
				(faction_get_slot, ":aristocracy", ":faction_no", dplmc_slot_faction_aristocracy),
				(lt, ":aristocracy", 0),
				(val_clamp, ":aristocracy", -3, 4),
				(val_add, ":number_required_for_quorum", ":aristocracy"),
				(val_max, ":number_required_for_quorum", 15),
			(try_end),
			(val_mul, ":number_required_for_quorum", ":total_lords"),
			(val_div, ":number_required_for_quorum", 20),
		(try_end),
		##diplomacy end+		
		
#		(gt, ":lords_who_have_voted", ":number_required_for_quorum"),

		(store_current_hours, ":hours_on_agenda"),
		(faction_get_slot, ":hours_when_put_on_agenda", ":faction_no", slot_faction_political_issue_time), #Appointment of marshal
		(val_sub, ":hours_on_agenda", ":hours_when_put_on_agenda"),

		##diplomacy start+
		#Before, the maximum number of hours on the agenda for an issue before it became
		#eligible for resolution regardless of quorum was fixed at 120 (five days).
		#Modify this by 16 hours for every point of centralization, for a minimum
		#of 3 days and a maximum of 7 days.
		(assign, ":hours_on_agenda_threshold", 120),
		(try_begin),
			#Disable this for now, since arguably all of the NPC kingdoms are
			#supposed to have fairly similar structures.  From a gameplay perspective,
			#they choose their kingdom policy at random, so enabling this is  probably
			#not going to have good effects, unless more thought is given to balancing
			#centralization/decentralization for NPC kingdoms.
			(eq, 0, 1),
			(store_mul, ":hours_on_agenda_threshold", ":centralization", 16),
			(val_add, ":hours_on_agenda_threshold", 120),
			(try_begin),
				(neq, ":centralization", 0),
			(try_end),
		(try_end),

		#(this_or_next|gt, ":lords_who_have_voted", ":number_required_for_quorum"),
		#	(ge, ":hours_on_agenda", 120),

		(this_or_next|gt, ":lords_who_have_voted", ":number_required_for_quorum"),
			(ge, ":hours_on_agenda", ":hours_on_agenda_threshold"),
		##diplomacy end+

		(try_begin),
			(eq, "$cheat_mode", 1),
			(assign, reg4, ":lords_who_have_voted"),
			(assign, reg5, ":number_required_for_quorum"),
			(assign, reg7, ":hours_on_agenda"),
			(str_store_faction_name, s4, ":faction_no"),
			(display_message, "@{!}DEBUG -- Issue resolution for {s4}: {reg4} votes for a quorum of {reg5}, {reg7} hours on agenda"),
		(try_end),


		(try_begin),
		  (eq, "$cheat_mode", 1),
		  (display_message, "@{!}DEBUG -- Faction resolves political issue"),
		(try_end),

	
		#Resolve faction political issue
		(assign, ":winning_candidate", -1),

		##diplomacy start+
		#Change "liege overrules lords" check.  The version in Native caused relation death spirals:
		#a lord who has no fiefs becomes unhappy, and since relation is symmetrical, this can result
		#in the liege never granting him fiefs.
		#
		#OLD BEHAVIOR:
#		(try_begin),
#                        (call_script, "script_troop_get_relation_with_troop", ":faction_leader", ":popular_favorite"),
#			
#			(this_or_next|ge, reg0, 10),
#			(this_or_next|troop_slot_eq, ":faction_leader", slot_troop_stance_on_faction_issue, ":popular_favorite"),
#				(troop_slot_eq, ":faction_leader", slot_troop_stance_on_faction_issue, -1),
#						
#			(assign, ":winning_candidate", ":popular_favorite"),
#		(else_try),#Lord overrules lords' opinion		
#			(gt, ":faction_leader", -1), #not sure why this is necessary
#			(troop_get_slot, ":liege_choice", ":faction_leader", slot_troop_stance_on_faction_issue),
#			(ge, ":liege_choice", -1),
#							
#			(assign, ":winning_candidate", ":liege_choice"),
#		(try_end),
#
#      NEW BEHAVIOR
        (troop_get_slot, ":liege_choice", ":faction_leader", slot_troop_stance_on_faction_issue),
		(assign, ":min_liege_relation", 10),#<-- Same as in default
		(faction_get_slot, ":issue_on_table", ":faction_no", slot_faction_political_issue),
		(try_begin),
		  (ge, "$g_dplmc_ai_changes", DPLMC_AI_CHANGES_LOW),
		  #Alter the minimum for villages and castles, but not towns or the marshall.
		  (this_or_next|is_between, ":issue_on_table", villages_begin, villages_end),
		     (is_between, ":issue_on_table", castles_begin, castles_end),
		  (store_random_in_range, ":min_liege_relation", 0, 16),
		  (val_sub, ":min_liege_relation", 5),#-5 to 10
		(try_end),
		#New override check
		(try_begin),
			#When the player is co-ruler of the kingdom, his/her support for the popular
			#candidate can be sufficient to guarantee success over the opposition of the
			#king/queen.
			(ge, ":faction_leader", 1),
			(eq, "$players_kingdom", ":faction_no"),
			(this_or_next|troop_slot_eq, ":faction_leader", slot_troop_spouse, "trp_player"),
				(troop_slot_eq, "trp_player", slot_troop_spouse, ":faction_leader"),
			(troop_slot_eq, "trp_player", slot_troop_stance_on_faction_issue, ":popular_favorite"),
			(assign, ":winning_candidate", ":popular_favorite"),
            (else_try),
            	#The leader may overrule a choice he disagrees with, if he dislikes the candidate
            	#sufficiently and has someone else in mind.
            	(ge, ":faction_leader", 1),
			(neq, ":liege_choice", ":popular_favorite"),
			(gt, ":liege_choice", -1),
			(call_script, "script_troop_get_relation_with_troop", ":faction_leader", ":liege_choice"),
			(val_min, ":min_liege_relation", reg0),
            	(call_script, "script_troop_get_relation_with_troop", ":faction_leader", ":popular_favorite"),
			(gt, ":min_liege_relation", reg0),
			(assign, reg0, 0),
            	(try_begin),
			   (troop_slot_ge, ":faction_leader", slot_troop_prisoner_of_party, 0),
			   (store_random_in_range, reg0, 0, 2),
			(try_end),
			(try_begin),
			    #The leader would have overruled the choice, but cannot because he is a prisoner.
            		#Print a message letting people know when this happens.
				(eq, reg0, 1),
				(gt, ":popular_favorite", -1),
            		(this_or_next|eq, "$players_kingdom", ":faction_no"),
            		(ge, "$cheat_mode", 1),
            		(str_store_faction_name, s4, ":faction_no"),
            		(str_store_troop_name, s5, ":popular_favorite"),
            		(str_store_troop_name, s0, ":faction_leader"),
            		(try_begin),
            			(eq, ":issue_on_table", 1),
					(display_message, "@{s5} has the greatest support among the lords of the {s4} to be the next strategist.  {s0} is indisposed and cannot overrule their choice."),
            		(else_try),
            			(is_between, ":issue_on_table", centers_begin, centers_end),
            			(str_store_party_name, s1, ":issue_on_table"),
					(display_message, "@{s5} has the greatest support among the lords of the {s4} to receive {s1}.  {s0} is indisposed and cannot overrule their choice."),
            		(try_end),
            	(try_end),
			(eq, reg0, 0),
			(assign, ":winning_candidate", ":liege_choice"),
			(try_begin),
				#Print a message letting people know when this happens.
				(gt, ":popular_favorite", -1),
				(this_or_next|eq, "$players_kingdom", ":faction_no"),
					(ge, "$cheat_mode", 1),
				(str_store_faction_name, s4, ":faction_no"),
				(str_store_troop_name, s5, ":popular_favorite"),
				(str_store_troop_name, s0, ":faction_leader"),
				(try_begin),
					(eq, ":issue_on_table", 1),
					(display_message, "@{s5} has the greatest support among the lords of the {s4} to be the next strategist, but {s0} overrules their choice."),
				(else_try),
					(is_between, ":issue_on_table", centers_begin, centers_end),
					(str_store_party_name, s1, ":issue_on_table"),
					(display_message, "@{s5} has the greatest support among the lords of the {s4} to receive {s1}, but {s0} overrules their choice."),
				(try_end),
			(try_end),
		(else_try),
			#No override: use popular candidate
			(assign, ":winning_candidate", ":popular_favorite"),
		(try_end),
		##diplomacy end+

		#Carry out faction decision
		(try_begin), #Nothing happens
			(eq, ":winning_candidate", -1),
			
		(else_try), #For player, create a menu to accept or refuse
			(eq, ":winning_candidate", "trp_player"),
			(eq, "$players_kingdom", ":faction_no"),
			(call_script, "script_add_notification_menu", "mnu_notification_player_faction_political_issue_resolved_for_player", 0, 0),
		(else_try),
			(eq, ":winning_candidate", "trp_player"),
			(neq, "$players_kingdom", ":faction_no"),

			(try_begin),
				(eq, "$cheat_mode", 1),
				(str_store_faction_name, s4, ":faction_no"),
				(str_store_party_name, s5, ":winning_candidate"),
				(display_message, "@{!}DEBUG -- {s4} drops {s5} as winner, for having changed sides"),
			(try_end),

			##diplomacy start+ add support for promoted kingdom ladies
			(try_for_range, ":active_npc", heroes_begin, heroes_end),#<- change active_npcs to heroes
				(this_or_next|troop_slot_eq, ":active_npc", slot_troop_occupation, slto_kingdom_hero),
					(is_between, ":active_npc", active_npcs_begin, active_npcs_end),
			##diplomacy end+
				(store_faction_of_troop, ":active_npc_faction", ":active_npc"),
				(eq, ":active_npc_faction", ":faction_no"),
				(troop_set_slot, ":active_npc", slot_troop_stance_on_faction_issue, -1),
			(try_end),		
			(try_begin),
				(eq, "$players_kingdom", ":faction_no"),
				(troop_set_slot, "trp_player", slot_troop_stance_on_faction_issue, -1),
			(try_end),
			
		(else_try),	#If candidate is not of winning faction, reset lrod votes
			(store_faction_of_troop, ":winning_candidate_faction", ":winning_candidate"),
			(neq, ":winning_candidate_faction", ":faction_no"),
			
			(try_begin),
				(eq, "$cheat_mode", 1),
				(str_store_faction_name, s4, ":faction_no"),
				(str_store_party_name, s5, ":winning_candidate"),
				(display_message, "@{!}DEBUG -- {s4} drops {s5} as winner, for having changed sides"),
			(try_end),
			##diplomacy start+ add support for promoted kingdom ladies
			(try_for_range, ":active_npc", heroes_begin, heroes_end),#<- change active_npcs to heroes
				(this_or_next|troop_slot_eq, ":active_npc", slot_troop_occupation, slto_kingdom_hero),
					(is_between, ":active_npc", active_npcs_begin, active_npcs_end),
			##diplomacy end+
				(store_faction_of_troop, ":active_npc_faction", ":active_npc"),
				(eq, ":active_npc_faction", ":faction_no"),
				(troop_set_slot, ":active_npc", slot_troop_stance_on_faction_issue, -1),
			(try_end),		
			(try_begin),
                                (eq, "$players_kingdom", ":faction_no"),
				(troop_set_slot, "trp_player", slot_troop_stance_on_faction_issue, -1),
			(try_end),
			
		(else_try), #Honor awarded to another
			(faction_get_slot, ":issue_on_table", ":faction_no", slot_faction_political_issue),
			(try_begin), #A marshalship awarded to another
				(eq, ":issue_on_table", 1),
				(is_between, ":winning_candidate", active_npcs_begin, active_npcs_end),

				##diplomacy start+ add support for promoted kingdom ladies
				(this_or_next|is_between, ":winning_candidate", heroes_begin, heroes_end),
					(eq, "$players_kingdom", ":faction_no"),
				(this_or_next|troop_slot_eq, ":winning_candidate", slot_troop_occupation, slto_kingdom_hero),
				##diplomacy end+				
				(this_or_next|is_between, ":winning_candidate", active_npcs_begin, active_npcs_end), #Prevents bug in which player given marshaldom of kingdom of which he/she is not a member
					(eq, "$players_kingdom", ":faction_no"),
				
				(assign, ":faction_marshal", ":winning_candidate"),
			(else_try), #A fief awarded to another
				(is_between, ":issue_on_table", centers_begin, centers_end),
				
				#If given to the player, resolved above
				(call_script, "script_give_center_to_lord", ":issue_on_table", ":winning_candidate", 0), #Zero means don't add garrison
				
				#If the player had requested a captured castle
				(try_begin),
					(eq, ":issue_on_table", "$g_castle_requested_by_player"),
					(party_slot_ge, ":issue_on_table", slot_town_lord, active_npcs_begin),
					(store_faction_of_party, ":faction_of_issue", ":issue_on_table"),
					(eq, ":faction_of_issue", "$players_kingdom"),
					(assign, "$g_center_to_give_to_player", ":issue_on_table"),
					(try_begin),
						(troop_get_slot, ":husband", "trp_player", slot_troop_spouse),
						##diplomacy start+ add support for promotede kingdom ladies
						(is_between, ":husband", heroes_begin, heroes_end),
						(this_or_next|troop_slot_eq, ":winning_candidate", slot_troop_occupation, slto_kingdom_hero),
						##diplomacy end+
						(is_between, ":husband", active_npcs_begin, active_npcs_end),
						(eq, "$g_castle_requested_for_troop", ":husband"),
						(neq, ":winning_candidate", ":husband"),
						(jump_to_menu, "mnu_requested_castle_granted_to_another_female"),
					(else_try),
						(jump_to_menu, "mnu_requested_castle_granted_to_another"),
					(try_end),	
				(try_end),
				
			(try_end),
		
			(try_begin),
				(eq, ":faction_no", "$players_kingdom"),
				(call_script, "script_add_notification_menu", "mnu_notification_player_faction_political_issue_resolved", ":issue_on_table", ":winning_candidate"),
			(try_end),
		
		#Reset political issue
			(faction_set_slot, ":faction_no", slot_faction_political_issue, 0),
			##diplomacy start+ add support for promoted kingdom ladies
			(try_for_range, ":active_npc", heroes_begin, heroes_end),#<- change active_npcs to heroes
			##diplomacy end+
				(store_faction_of_troop, ":active_npc_faction", ":active_npc"),
				(eq, ":active_npc_faction", ":faction_no"),
				(troop_set_slot, ":active_npc", slot_troop_stance_on_faction_issue, -1),
			(try_end),
			(try_begin),
				(eq, "$players_kingdom", ":faction_no"),
				(troop_set_slot, "trp_player", slot_troop_stance_on_faction_issue, -1),
			(try_end),			
		(try_end),
	(try_end),

	#Add fief to faction issues
	(try_begin),
		(faction_get_slot, ":faction_issue", ":faction_no", slot_faction_political_issue),
		(le, ":faction_issue", 0),

                (assign, ":landless_lords", 0),
		(assign, ":unassigned_centers", 0),
		(assign, ":first_unassigned_center_found", 0),
		
		(troop_set_slot, "trp_player", slot_troop_temp_slot, 0),
		##diplomacy start+ add support for promoted kingdom ladies
		(try_for_range, ":active_npc", heroes_begin, heroes_end),#<- change active_npcs to heroes
		##diplomacy end+
			(troop_set_slot, ":active_npc", slot_troop_temp_slot, 0),
		(try_end),
		
		
		(try_for_range, ":center", centers_begin, centers_end),
			(store_faction_of_party, ":center_faction", ":center"),
			(eq, ":center_faction", ":faction_no"),
			
			(party_get_slot, ":town_lord", ":center", slot_town_lord),
			
			(try_begin),
				(lt, ":town_lord", 0),
				(val_add, ":unassigned_centers", 1),
				(try_begin),
					(eq, ":first_unassigned_center_found", 0),
					(assign, ":first_unassigned_center_found", ":center"),
				(try_end),
			(else_try),
				(troop_set_slot, ":town_lord", slot_troop_temp_slot, 1),			
			(try_end),
		(try_end),
		
		(store_add, ":landless_lords_plus_unassigned_centers", ":landless_lords", ":unassigned_centers"),
		(ge, ":landless_lords_plus_unassigned_centers", 2),		
			
		(faction_set_slot, ":faction_no", slot_faction_political_issue, ":first_unassigned_center_found"),	
		(store_current_hours, ":hours"),
		(faction_set_slot, ":faction_no", slot_faction_political_issue_time, ":hours"), #Fief put on agenda
		
		##diplomacy start+ add support for promoted kingdom ladies
		(try_for_range, ":active_npc", heroes_begin, heroes_end),#<- change active_npcs to heroes
		##diplomacy end+
			(store_faction_of_troop, ":active_npc_faction", ":active_npc"),
			(eq, ":active_npc_faction", ":faction_no"),
			(troop_set_slot, ":active_npc", slot_troop_stance_on_faction_issue, -1),
		(try_end),
		(try_begin),
			(eq, "$players_kingdom", ":faction_no"),
			(troop_set_slot, "trp_player", slot_troop_stance_on_faction_issue, -1),
		(try_end),				
	(try_end),
	 
	 
    (try_begin), #If the marshal is changed
       (neg|faction_slot_eq, ":faction_no", slot_faction_marshall, ":faction_marshal"),
       #(assign, ":marshall_changed", 1),
       (eq, "$players_kingdom", ":faction_no"),
       (str_store_troop_name_link, s1, ":faction_marshal"),
       (str_store_faction_name_link, s2, ":faction_no"),
       (display_message, "@{s1} is the new strategist of {s2}."),
       (call_script, "script_check_and_finish_active_army_quests_for_faction", ":faction_no"),       
    (try_end),	 
	 
    (try_begin), #If the marshal is changed
       (neg|faction_slot_eq, ":faction_no", slot_faction_marshall, ":faction_marshal"),
	   (gt, ":faction_marshal", -1),
       (call_script, "script_appoint_faction_marshall", ":faction_no", ":faction_marshal"),   
    (try_end),	 
		 
	#DO FACTION AI HERE
    (try_begin),
		(eq, ":faction_no", "$players_kingdom"),
		(eq, ":faction_marshal", "trp_player"),
	    (assign, ":faction_ai_decider", "trp_player"),
	(else_try),
		##diplomacy start+ add support for promoted kingdom ladies
		(is_between, ":faction_marshal", heroes_begin, heroes_end),
		#(this_or_next|troop_slot_eq, ":faction_marshal", slot_troop_occupation, slto_kingdom_hero),
		#(is_between, ":faction_marshal", active_npcs_begin, active_npcs_end),
		##diplomacy end+
		(assign, ":faction_ai_decider", ":faction_marshal"),
	(else_try),
		(faction_get_slot, ":faction_ai_decider", ":faction_no", slot_faction_leader),
	(try_end),
	 
    (call_script, "script_npc_decision_checklist_faction_ai_alt",  ":faction_ai_decider"),
    (assign, ":new_strategy", reg0),
    (assign, ":new_object", reg1),
    	   
    #new ozan
    (try_begin),
       (neq, ":new_strategy", ":old_faction_ai_state"),
       (eq, ":new_strategy", sfai_gathering_army),
       (faction_get_slot, ":faction_marshal", ":faction_no", slot_faction_marshall),
       ##diplomacy begin
       #native script error bug fix when no marshal
       (gt, ":faction_marshal", -1),
       ##diplomacy end
       (troop_get_slot, ":marshal_party", ":faction_marshal", slot_troop_leaded_party),
       (party_set_slot, ":marshal_party", slot_party_ai_object, -1),
       (assign, "$g_gathering_new_started", 1),
       (call_script, "script_npc_decision_checklist_party_ai", ":faction_marshal"), #This handles AI for both marshal and other parties		
       (call_script, "script_party_set_ai_state", ":marshal_party", reg0, reg1),
       (assign, "$g_gathering_new_started", 0),
    (else_try),      
       #check if marshal arrived his target city during active gathering
       
       #for now i disabled below lines because after always/active gathering armies become very large.
       #in current style marshal makes active gathering only at first, it travels to a city and waits there.
       
       (eq, ":new_strategy", ":old_faction_ai_state"),
       (eq, ":new_strategy", sfai_gathering_army),
       (faction_get_slot, ":faction_marshal", ":faction_no", slot_faction_marshall),
       ##diplomacy begin
       #native script error bug fix when no marshal
       (gt, ":faction_marshal", -1),
       ##diplomacy end
       (troop_get_slot, ":marshal_party", ":faction_marshal", slot_troop_leaded_party),
	   ##diplomacy start+ 2011-06-08 Fix bug when the marshall leaded party is set negative!
	   (gt, ":marshal_party", -1),
	   ##diplomacy end+
       (party_get_slot, ":party_ai_object", ":marshal_party", slot_party_ai_object),

       (ge, ":party_ai_object", 0),
       (ge, ":marshal_party", 0),
       (party_is_active, ":marshal_party"),
       (party_is_active, ":party_ai_object"),    
       (store_distance_to_party_from_party, ":dist", ":marshal_party", ":party_ai_object"),
       (le, ":dist", 5),

       (party_set_slot, ":marshal_party", slot_party_ai_object, -1),
    (try_end),
     #end ozan
	   	   	   
     #The following logic is mostly transplanted to the new decision_checklist 
     #Decision_checklist is used because I want to be able to reproduce the logic for strings
     #(call_script, "script_old_faction_ai"), 
     #ozan - I collected all comment-out lines in here (faction ai script) and placed most bottom of scripts.py to avoid confusing.	   		 	
     
    (faction_set_slot, ":faction_no", slot_faction_ai_state, ":new_strategy"),
    (faction_set_slot, ":faction_no", slot_faction_ai_object, ":new_object"),

    (call_script, "script_update_report_to_army_quest_note", ":faction_no", ":new_strategy", ":old_faction_ai_state"),

    (try_begin),
       (eq, ":new_strategy", sfai_feast),
       
       (store_current_hours, ":hours"),
       (faction_set_slot, ":faction_no", slot_faction_last_feast_start_time, ":hours"), #new
       
       (try_begin),
         (eq, "$g_player_eligible_feast_center_no", ":new_object"),
         (assign, "$g_player_eligible_feast_center_no", -1), #reset needed
       (try_end),
       (try_begin),
         (is_between, ":new_object", towns_begin, towns_end),
         (party_set_slot, ":new_object", slot_town_has_tournament, 2),
       (try_end),
    (try_end),	
	
     #Change of strategy
    (try_begin),
       (neq, ":new_strategy", ":old_faction_ai_state"),
		
       (try_begin),
         (ge, "$cheat_mode", 1),
         (str_store_faction_name, s5, ":faction_no"),
         (display_message, "str_s5_decides_s14"),
       (try_end),
		
       (store_current_hours, ":hours"),
       (faction_set_slot, ":faction_no", slot_faction_ai_current_state_started, ":hours"),

       #Feast ends
       (try_begin),
         (eq, ":old_faction_ai_state", sfai_feast),
         (call_script, "script_faction_conclude_feast", ":faction_no", ":old_faction_ai_object"),
       (try_end),

	   
       #Feast begins
       (try_begin),
         (eq, ":new_strategy", sfai_feast),
         (faction_get_slot, ":faction_object", ":faction_no", slot_faction_ai_object),
		 
##         (str_store_faction_name, s1, ":faction_no"),
##         (str_store_party_name, s2, ":faction_object"),
##         (display_message, "str_lords_of_the_s1_gather_for_a_feast_at_s2"),
		
         (party_get_slot, ":feast_host", ":faction_object", slot_town_lord),

         (try_begin),
           (check_quest_active, "qst_wed_betrothed"),
		   
           (quest_slot_eq, "qst_wed_betrothed", slot_quest_giver_troop, ":feast_host"),
           (neg|quest_slot_ge, "qst_wed_betrothed", slot_quest_expiration_days, 362),
           (call_script, "script_add_notification_menu", "mnu_notification_player_wedding_day", ":feast_host", ":faction_object"),
		 (else_try),
           (check_quest_active, "qst_wed_betrothed_female"),
		   
           (quest_get_slot, ":player_betrothed", "qst_wed_betrothed", slot_quest_giver_troop),
		   (store_faction_of_troop, ":player_betrothed_faction", ":player_betrothed"),
		   (eq, ":player_betrothed_faction", ":faction_no"),
           (neg|quest_slot_ge, "qst_wed_betrothed", slot_quest_expiration_days, 362),
           (call_script, "script_add_notification_menu", "mnu_notification_player_kingdom_holds_feast", ":feast_host", ":faction_object"),
         (else_try),
           (eq, "$players_kingdom", ":faction_no"),
           (troop_slot_ge, "trp_player", slot_troop_renown, 150),
		   
		   
           (party_get_slot, ":feast_host", ":faction_object", slot_town_lord),
           (call_script, "script_add_notification_menu", "mnu_notification_player_kingdom_holds_feast", ":feast_host", ":faction_object"),
         (try_end),
       (try_end),
		

       #Offensive begins
       (try_begin),
         (eq, ":old_faction_ai_state", sfai_gathering_army),
         (is_between, ":new_strategy", sfai_attacking_center, sfai_feast),
		 (try_begin),
			(eq, "$cheat_mode", 1),
			(str_store_faction_name, s5, ":faction_no"),
			(display_message, "str_s5_begins_offensive"),
		 (try_end),
			
		 #gekokujo 3.0 integrating motomataru's campaign AI start
         ##Appoint screening party
         #(try_begin),
         #  (assign, ":total_lords_participating", 0),
         #  (assign, ":best_screening_party", -1),
         #  (assign, ":score_to_beat", 30), #closest in size to 50
         #  (troop_get_slot, ":faction_marshal_party", ":faction_marshal", slot_troop_leaded_party),
         #  (party_is_active, ":faction_marshal_party"),	
		 #
		 #  ##diplomacy start+
         #  #(try_for_range, ":screen_leader", active_npcs_begin, active_npcs_end),##OLD
         #  (try_for_range, ":screen_leader", heroes_begin, heroes_end),##NEW
		 #  ##diplomacy end+
         #    (store_faction_of_troop, ":screen_leader_faction", ":screen_leader"),
         #    (eq, ":screen_leader_faction", ":faction_no"),
         #
         #    #gekokujo 3.0 forgot to integrate start
         #    #(troop_get_slot, ":screening_party", ":screen_leader_faction", slot_troop_leaded_party), 
         #    (troop_get_slot, ":screening_party", ":screen_leader", slot_troop_leaded_party), 
         #    #gekokujo 3.0 forgot to integrate end
         #    ##diplomacy start+ Guard against things such as the party being 0 (p_main_party)
         #    (gt, ":screening_party", 0),
         #    ##diplomacy end+
         #    (party_is_active, ":screening_party"),			
         #    (party_slot_eq, ":screening_party", slot_party_ai_state, spai_accompanying_army),
         #    (party_slot_eq, ":screening_party", slot_party_ai_object, ":faction_marshal_party"),
         #    (val_add, ":total_lords_participating", 1),
         #
		 #    (try_begin),
		 #     (ge, "$cheat_mode", 1),
		 #     (str_store_party_name, s4, ":screening_party"),
		 #     (display_message, "@{!}DEBUG -- {s4} participates in offensive"),
		 #    (try_end),
         #
         # 
         #    (store_party_size_wo_prisoners, ":screening_party_score", ":screening_party"),
         #    (val_sub, ":screening_party_score", 50),
		 #	  (val_abs, ":screening_party_score"),
         #
         #
         #    (lt, ":screening_party_score", ":score_to_beat"),
         #
         #    #set party and score
         #    (assign, ":best_screening_party", ":screening_party"),
         #    (assign, ":score_to_beat", ":screening_party_score"),
         #  (try_end),	
         #
         #  (gt, ":total_lords_participating", 2),
         #  (party_is_active, ":best_screening_party"),
         #  (party_is_active, ":faction_marshal_party"),
         #  (call_script, "script_party_set_ai_state", ":best_screening_party", spai_screening_army, ":faction_marshal_party"),
		 #  (try_begin),
		 #   (ge, "$cheat_mode", 1),
		 #   (str_store_party_name, s4, ":best_screening_party"),
		 #   (display_message, "@{!}DEBUG -- {s4} chosen as screen"),
		 #  (try_end),
         #  #after this - dialogs on what doing, npc_decision_checklist
         #(try_end),	
		 #gekokujo 3.0 integrating motomataru's campaign AI end
		 
       #Offensive concludes
       (else_try),
	     (store_current_hours, ":hours"),
         (this_or_next|eq, ":old_faction_ai_state", sfai_gathering_army),
         (this_or_next|eq, ":old_faction_ai_state", sfai_attacking_center),
         (this_or_next|eq, ":old_faction_ai_state", sfai_raiding_village),
		 #(this_or_next|eq, ":old_faction_ai_state", sfai_attacking_enemies_around_center),
			(eq, ":old_faction_ai_state", sfai_attacking_enemy_army),
		 
         (this_or_next|eq, ":new_strategy", sfai_default),
			(eq, ":new_strategy", sfai_feast),				
						
         (call_script, "script_check_and_finish_active_army_quests_for_faction", ":faction_no"),       		 
         (faction_set_slot, ":faction_no", slot_faction_last_offensive_concluded, ":hours"),
        (try_end),
    (try_end),
	
    (try_begin),
       (eq, "$players_kingdom", ":faction_no"),
       (neg|faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_attacking_center),
       (check_quest_active, "qst_join_siege_with_army"),
       (call_script, "script_abort_quest", "qst_join_siege_with_army", 0),
    (try_end),

    (try_begin),
       #old condition to rest, I changed below part - ozan, to rest (a faction's old strategy should be feast or default) and (a faction's new strategy should be feast or default)
       #(this_or_next|eq, ":new_strategy", sfai_default),
       #(this_or_next|eq, ":new_strategy", sfai_feast),
       #(this_or_next|eq, ":old_faction_ai_state", sfai_default),
       #(eq, ":old_faction_ai_state", sfai_feast),
       
       #new condition to rest, (a faction's new strategy should be feast or default) and (":hours_at_current_state" > 20)
       (this_or_next|eq, ":new_strategy", sfai_default),
		(eq, ":new_strategy", sfai_feast),                            
              
       (store_current_hours, ":hours_at_current_state"),
       (faction_get_slot, ":current_state_started", ":faction_no", slot_faction_ai_current_state_started), 
       (val_sub, ":hours_at_current_state", ":current_state_started"),
       (ge, ":hours_at_current_state", 18), #Must have at least 18 hours to reset
              
       (store_current_hours, ":hours"),       
       (faction_set_slot, ":faction_no", slot_faction_ai_last_rest_time, ":hours"),		
    (try_end),     
  ]),
    # script_troop_get_player_relation
    # Input: arg1 = troop_no
    # Output: reg0 = effective relation (modified by troop reputation, honor, etc.)
    ("troop_get_player_relation",
      [
        (store_script_param_1, ":troop_no"),
        (troop_get_slot, ":reputation", ":troop_no", slot_lord_reputation_type),
        (troop_get_slot, ":effective_relation", ":troop_no", slot_troop_player_relation),
        (assign, ":honor_bonus", 0),
        (try_begin),
          (eq,  ":reputation", lrep_quarrelsome),
          (val_add, ":effective_relation", -3),
        (try_end),
        (try_begin),
          (ge, "$player_honor", 0),
          (try_begin),
            (this_or_next|eq,  ":reputation", lrep_upstanding),
            (             eq,  ":reputation", lrep_goodnatured),
            (store_div, ":honor_bonus", "$player_honor", 3),
		  ##diplomacy start+
		  (else_try),
			#In general this should not apply to ladies, as they operate by different
			#reputation rules, but if a "kingdom lady" has become a "kingdom hero" instead,
			#it should apply.
		     (eq,  ":reputation", lrep_moralist),#-- verify that the lady is effectively a lord:
		     (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
			 (store_div, ":honor_bonus", "$player_honor", 3),
		  (else_try),
			 #Personality type that values keeping your word
			 (call_script, "script_dplmc_get_troop_morality_value", ":troop_no", tmt_honest),
			 (ge, reg0, 1),
			 (store_div, ":honor_bonus", "$player_honor", 3),
		  ##diplomacy end+
          (try_end),
        (try_end),
        (try_begin),
          (lt, "$player_honor", 0),
          (try_begin),
            (this_or_next|eq,  ":reputation", lrep_upstanding),
            (             eq,  ":reputation", lrep_goodnatured),
            (store_div, ":honor_bonus", "$player_honor", 3),
          ##diplomacy start+
		  (else_try),
			(call_script, "script_dplmc_get_troop_morality_value", ":troop_no", tmt_honest),
			(ge, reg0, 1),#Personality type that values keeping your word
			(store_div, ":honor_bonus", "$player_honor", 3),
		  (else_try),
		  	 #"My kind of scum" - a few rare individuals might actively approve.
		  	 (lt, reg0, 0),#<-- must have negative value for tmt_honest; by default this is only Rolf.
		  	 (this_or_next|eq, ":reputation", lrep_roguish),
		  	 (this_or_next|eq, ":reputation", lrep_custodian),
		  	 (this_or_next|eq, ":reputation", lrep_debauched),
		  	 (this_or_next|eq, ":reputation", lrep_ambitious),
		  		(eq, ":reputation", lrep_cunning),
		  	 (store_div, ":honor_bonus", "$player_honor", -5),
		  	 (val_clamp, ":honor_bonus", 1, 6),
          (else_try),
			#"Honorable" lords can be awful people, so no bonus with benefactors,
			#but dishonorable lords are *guaranteed* to be awful.
            (eq, ":reputation", lrep_benefactor),
            (store_div, ":honor_bonus", "$player_honor", 5),
		  (else_try),
			#Self-righteous lords are moralizing but hypocritical.
			(eq, ":reputation", lrep_selfrighteous),
			(store_div, ":honor_bonus", "$player_honor", 5),
		  (else_try),
			 #In general this should not apply to ladies, as they operate by different
			 #reputation rules, but if a "kingdom lady" has become a "kingdom hero" instead,
			 #it should apply.
			 (eq,  ":reputation", lrep_moralist),#-- verify that the lady is effectively a lord:
		     (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
			 (store_div, ":honor_bonus", "$player_honor", 3),
		  (else_try),
			 (eq,  ":reputation", lrep_conventional),#-- verify that the lady is effectively a lord:
		     (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
			 (store_div, ":honor_bonus", "$player_honor", 5),
          ##diplomacy end+
          (else_try),
            (eq,  ":reputation", lrep_martial),
            (store_div, ":honor_bonus", "$player_honor", 5),
          (try_end),
        (try_end),
        (val_add, ":effective_relation", ":honor_bonus"),
        (val_clamp, ":effective_relation", -100, 101),
        (assign, reg0, ":effective_relation"),
    ]),
  # script_change_troop_renown
  # Input: arg1 = troop_no, arg2 = relation difference
  # Output: none
  ("change_troop_renown",
    [
      (store_script_param_1, ":troop_no"),
      (store_script_param_2, ":renown_change"),
      
      (troop_get_slot, ":old_renown", ":troop_no", slot_troop_renown),

	  (try_begin),
		(gt, ":renown_change", 0),
		(assign, reg4, ":renown_change"),
		
		(store_div, ":subtraction", ":old_renown", 200), 
	    (val_sub, ":renown_change", ":subtraction"),
	    (val_max, ":renown_change", 0),
		
	    (eq, ":troop_no", "trp_player"), 

	    (assign, reg5, ":renown_change"),
		
		(eq, "$cheat_mode", 1),
	    (display_message, "str_renown_change_of_reg4_reduced_to_reg5_because_of_high_existing_renown"),
	  (try_end),

      (store_add, ":new_renown", ":old_renown", ":renown_change"),
      (val_max, ":new_renown", 0),
      (troop_set_slot, ":troop_no", slot_troop_renown, ":new_renown"),
	  
      (try_begin),
        (eq, ":troop_no", "trp_player"),

		(try_begin),
		  (ge, ":new_renown", 50),

          (try_begin),
            (troop_get_type, ":is_female", "trp_player"),
            (eq, ":is_female", 1),
            (unlock_achievement, ACHIEVEMENT_TALK_OF_THE_TOWN),
          (try_end),
		(try_end),

        (str_store_troop_name, s1, ":troop_no"),
        (assign, reg12, ":renown_change"),
        (val_abs, reg12),
        (try_begin),
         (gt, ":renown_change", 0),
         (display_message, "@You gained {reg12} renown."),
        (else_try),
          (lt, ":renown_change", 0),
          (display_message, "@You lose {reg12} renown."),
        (try_end),
      (try_end),
      (call_script, "script_update_troop_notes", ":troop_no"),
  ]),
  # script_change_player_relation_with_troop
  # Input: arg1 = troop_no, arg2 = relation difference
  # Output: none
  ("change_player_relation_with_troop",
    [
      (store_script_param_1, ":troop_no"),
      (store_script_param_2, ":difference"),

      (try_begin),
        (neq, ":troop_no", "trp_player"),
        (neg|is_between, ":troop_no", soldiers_begin, soldiers_end),
        ##diplomacy start+
		  (neq, ":troop_no", "trp_kingdom_heroes_including_player_begin"),
		  #(neq, ":troop_no", -1),#OLD
		  (ge, ":troop_no", 1),#NEW
        ##diplomacy end+
        (neq, ":difference", 0),
        (call_script, "script_troop_get_player_relation", ":troop_no"),
        (assign, ":old_effective_relation", reg0),
        (troop_get_slot, ":player_relation", ":troop_no", slot_troop_player_relation),
        (val_add, ":player_relation", ":difference"),
        (val_clamp, ":player_relation", -100, 101),
        (try_begin),
          (troop_set_slot, ":troop_no", slot_troop_player_relation, ":player_relation"),
          
          (try_begin),
            (le, ":player_relation", -50),
            (unlock_achievement, ACHIEVEMENT_OLD_DIRTY_SCOUNDREL),
          (try_end),
          
          (str_store_troop_name_link, s1, ":troop_no"),
          (call_script, "script_troop_get_player_relation", ":troop_no"),
          (assign, ":new_effective_relation", reg0),
          (neq, ":old_effective_relation", ":new_effective_relation"),
          (assign, reg1, ":old_effective_relation"),
          (assign, reg2, ":new_effective_relation"),
          (try_begin),
			##diplomacy start+ Suppress this message for dead people except in cheat mode
            (lt, "$cheat_mode", 1),
			(troop_slot_eq, ":troop_no", slot_troop_occupation, dplmc_slto_dead),
			(neq, ":troop_no", "$g_talk_troop"),
		  (else_try),
		  ##diplomacy end+
            (gt, ":difference", 0),
            (display_message, "str_troop_relation_increased"),
          (else_try),
            (lt, ":difference", 0),
            (display_message, "str_troop_relation_detoriated"),
          (try_end),
          (try_begin),
            (eq, ":troop_no", "$g_talk_troop"),
            (assign, "$g_talk_troop_relation", ":new_effective_relation"),
            (call_script, "script_setup_talk_info"),
          (try_end),
          (call_script, "script_update_troop_notes", ":troop_no"),
        (try_end),
      (try_end),
  ]),
  # script_change_player_relation_with_center
  # Input: arg1 = party_no, arg2 = relation difference
  # Output: none
  ("change_player_relation_with_center",
    [
      (store_script_param_1, ":center_no"),
      (store_script_param_2, ":difference"),
      
      (party_get_slot, ":player_relation", ":center_no", slot_center_player_relation),
      (assign, reg1, ":player_relation"),
      (val_add, ":player_relation", ":difference"),
      (val_clamp, ":player_relation", -100, 100),
      (assign, reg2, ":player_relation"),
      (party_set_slot, ":center_no", slot_center_player_relation, ":player_relation"),

      (try_begin),
        (le, ":player_relation", -50),
        (unlock_achievement, ACHIEVEMENT_OLD_DIRTY_SCOUNDREL),
      (try_end),

      
      (str_store_party_name_link, s1, ":center_no"),
      (try_begin),
        (gt, ":difference", 0),
        (display_message, "@Your relation with {s1} has improved."),
      (else_try),
        (lt, ":difference", 0),
        (display_message, "@Your relation with {s1} has deteriorated."),
      (try_end),
      (try_begin),
        (party_slot_eq, ":center_no", slot_party_type, spt_village),
        (call_script, "script_update_volunteer_troops_in_village", ":center_no"),
      (try_end),
      
      (try_begin),
        (this_or_next|is_between, "$g_talk_troop", village_elders_begin, village_elders_end),
        (is_between, "$g_talk_troop", mayors_begin, mayors_end),
        ##diplomacy start+
		  #Fix potential bug: don't adjust relations except with *that* center's
		  #mayor.
		  (party_slot_eq, ":center_no", slot_town_elder, "$g_talk_troop"),
	    ##diplomacy end+
        (assign, "$g_talk_troop_relation", ":player_relation"),
        (call_script, "script_setup_talk_info"),
      (try_end),
  ]),
  # script_change_player_relation_with_faction
  # Input: arg1 = faction_no, arg2 = relation difference
  # Output: none
  ("change_player_relation_with_faction",
    [
      (store_script_param_1, ":faction_no"),
      (store_script_param_2, ":difference"),
      
      (store_relation, ":player_relation", ":faction_no", "fac_player_supporters_faction"),
      (assign, reg1, ":player_relation"),
      (val_add, ":player_relation", ":difference"),
      (assign, reg2, ":player_relation"),
      (set_relation, ":faction_no", "fac_player_faction", ":player_relation"),
      (set_relation, ":faction_no", "fac_player_supporters_faction", ":player_relation"),
      
      (try_begin),
        (le, ":player_relation", -50),
        (unlock_achievement, ACHIEVEMENT_OLD_DIRTY_SCOUNDREL),
      (try_end),

      
      (str_store_faction_name_link, s1, ":faction_no"),
      (try_begin),
        (gt, ":difference", 0),
        (display_message, "str_faction_relation_increased"),
      (else_try),
        (lt, ":difference", 0),
        (display_message, "str_faction_relation_detoriated"),
      (try_end),
      (call_script, "script_update_all_notes"),
      ]),
  # script_set_player_relation_with_faction
  # Input: arg1 = faction_no, arg2 = relation
  # Output: none
  ("set_player_relation_with_faction",
    [
      (store_script_param_1, ":faction_no"),
      (store_script_param_2, ":relation"),
      
      (store_relation, ":player_relation", ":faction_no", "fac_player_supporters_faction"),
      (store_sub, ":reln_dif", ":relation", ":player_relation"),
      (call_script, "script_change_player_relation_with_faction", ":faction_no", ":reln_dif"),
      ]),
  # script_change_player_relation_with_faction_ex
  # changes relations with other factions also (according to their relations between each other)
  # Input: arg1 = faction_no, arg2 = relation difference
  # Output: none
  ("change_player_relation_with_faction_ex",
    [
      (store_script_param_1, ":faction_no"),
      (store_script_param_2, ":difference"),
      
      (store_relation, ":player_relation", ":faction_no", "fac_player_supporters_faction"),
      (assign, reg1, ":player_relation"),
      (val_add, ":player_relation", ":difference"),
      (assign, reg2, ":player_relation"),
      (set_relation, ":faction_no", "fac_player_faction", ":player_relation"),
      (set_relation, ":faction_no", "fac_player_supporters_faction", ":player_relation"),
      
      (str_store_faction_name_link, s1, ":faction_no"),
      (try_begin),
        (gt, ":difference", 0),
        (display_message, "str_faction_relation_increased"),
      (else_try),
        (lt, ":difference", 0),
        (display_message, "str_faction_relation_detoriated"),
      (try_end),
      
      (try_for_range, ":other_faction", kingdoms_begin, kingdoms_end),
        (faction_slot_eq, ":other_faction", slot_faction_state, sfs_active),
        (neq, ":faction_no", ":other_faction"),
        (store_relation, ":other_faction_relation", ":faction_no", ":other_faction"),
        (store_relation, ":player_relation", ":other_faction", "fac_player_supporters_faction"),
        (store_mul, ":relation_change", ":difference", ":other_faction_relation"),
        (val_div, ":relation_change", 100),
        (val_add, ":player_relation", ":relation_change"),
        ##diplomacy start
        (try_begin),
            (store_add, ":truce_slot", "fac_player_supporters_faction", slot_faction_truce_days_with_factions_begin),
  		    (val_sub, ":truce_slot", kingdoms_begin),
  		    (faction_get_slot, ":truce_days", ":other_faction", ":truce_slot"),
			##nested diplomacy start+ Changed "eq 0", to "le 0", since now negative truce days track war length
            (this_or_next|le, ":truce_days", 0), #other faction only affected if no truce
			##nested diplomacy end+
            (gt, ":difference", 0), #or change > 0
            (store_relation, ":cur_relation", ":other_faction", "fac_player_supporters_faction"),

            #display relation change message
            (store_sub,  ":relation_change", ":player_relation", ":cur_relation"),
            (str_store_faction_name_link, s1, ":other_faction"),
            (assign, reg1, ":cur_relation"),
            (assign, reg2, ":player_relation"),
            (try_begin),
              (gt, ":relation_change", 0),
              (display_message, "str_faction_relation_increased"),
            (else_try),
              (lt, ":relation_change", 0),
              (display_message, "str_faction_relation_detoriated"),
            (try_end),

            #display war declaration
            (try_begin),
                (ge, ":cur_relation", 0), #old relation > 0 -> peace
                (lt, ":player_relation", 0), #new relation < 0 -> war
                ##nested diplomacy start+
                #This is the source of the "fake war" bug.  I think this should get rid of it:
                (try_begin),
                    (this_or_next|eq, "$players_kingdom", "fac_player_faction"),
                       (eq, "$players_kingdom", "fac_player_supporters_faction"),
                ##nested diplomacy end+
                (call_script, "script_add_notification_menu", "mnu_notification_war_declared", ":other_faction", "$players_kingdom"),
                ##nested diplomacy start+
				(else_try),
					(is_between, "$players_kingdom", kingdoms_begin, kingdoms_end),
					(store_relation, ":players_kingdom_relation", ":other_faction", "$players_kingdom"),
					(lt, ":players_kingdom_relation", 0),
					(call_script, "script_add_notification_menu", "mnu_notification_war_declared", ":other_faction", "$players_kingdom"),
				(else_try),
					#Display some sort of message so you know something happened
				    (display_message, "@{!} There is widespread ill-will towards you in the {s1}."),
                (try_end),
                ##nested diplomacy end+
            (try_end),
        ##diplomacy end
        (set_relation, ":other_faction", "fac_player_faction", ":player_relation"),
        (set_relation, ":other_faction", "fac_player_supporters_faction", ":player_relation"),
        ##diplomacy begin
        (try_end),
        ##diplomacy end
      (try_end),
      (try_begin),
        (faction_slot_eq, "fac_player_supporters_faction", slot_faction_state, sfs_active),
        (try_for_range, ":kingdom_no", kingdoms_begin, kingdoms_end),
          (faction_slot_eq, ":kingdom_no", slot_faction_state, sfs_active),
          (call_script, "script_update_faction_notes", ":kingdom_no"),
        (try_end),
      (try_end),
  ]),
  # script_cf_get_random_active_faction_except_player_faction_and_faction
  # Input: arg1 = except_faction_no
  # Output: reg0 = random_faction
  ("cf_get_random_active_faction_except_player_faction_and_faction",
    [
      (store_script_param_1, ":except_faction_no"),
      (assign, ":num_factions", 0),
      (try_for_range, ":faction_no", kingdoms_begin, kingdoms_end),
        (neq, ":faction_no", "fac_player_supporters_faction"),
        (neq, ":faction_no", ":except_faction_no"),
        (faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
        (val_add, ":num_factions", 1),
      (try_end),
      (gt, ":num_factions", 0),
      (assign, ":selected_faction", -1),
      (store_random_in_range, ":random_faction", 0, ":num_factions"),
      (try_for_range, ":faction_no", kingdoms_begin, kingdoms_end),
        (ge, ":random_faction", 0),
        (neq, ":faction_no", "fac_player_supporters_faction"),
        (neq, ":faction_no", ":except_faction_no"),
        (faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
        (val_sub, ":random_faction", 1),
        (lt, ":random_faction", 0),
        (assign, ":selected_faction", ":faction_no"),
      (try_end),
      (assign, reg0, ":selected_faction"),
  ]),
  # script_make_kingdom_hostile_to_player
  # Input: arg1 = faction_no, arg2 = relation difference
  # Output: none
  ("make_kingdom_hostile_to_player",
    [
      (store_script_param_1, ":kingdom_no"),
      (store_script_param_2, ":difference"),

      (try_begin),
        (lt, ":difference", 0),
        (store_relation, ":player_relation", ":kingdom_no", "fac_player_supporters_faction"),
        (val_min, ":player_relation", 0),
        (val_add, ":player_relation", ":difference"),
        (call_script, "script_set_player_relation_with_faction", ":kingdom_no", ":player_relation"),
      (try_end),
  ]),
  # script_change_player_honor
  # Input: arg1 = honor difference
  # Output: none
  ("change_player_honor",
    [
      (store_script_param_1, ":honor_dif"),
      ##diplomacy start+
      #Exacerbate the effect of honor losses as the player's honor increases
      (try_begin),
         (ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_HIGH),#<-- experimental settings must be enabled
		 (ge, "$player_honor", 10),
         (lt, ":honor_dif", 0),
         (store_add, ":honor_multiplier", "$player_honor", 100),
         (val_mul, ":honor_dif", ":honor_multiplier"),
         (val_sub, ":honor_dif", 50),
         (val_div, ":honor_dif", 100),
      (try_end),
      ##diplomacy end+
      (val_add, "$player_honor", ":honor_dif"),
      (try_begin),
        (gt, ":honor_dif", 0),
        (display_message, "@You gain honour."),
      (else_try),
        (lt, ":honor_dif", 0),
        (display_message, "@You lose honour."),
      (try_end),

##      (val_mul, ":honor_dif", 1000),
##      (assign, ":temp_honor", 0),
##      (assign, ":num_nonlinear_steps", 10),
##      (try_begin),
##        (gt, "$player_honor", 0),
##        (lt, ":honor_dif", 0),
##        (assign, ":num_nonlinear_steps", 0),
##      (else_try),
##        (lt, "$player_honor", 0),
##        (gt, ":honor_dif", 0),
##        (assign, ":num_nonlinear_steps", 3),
##      (try_end),
##      
##      (try_begin),
##        (ge, "$player_honor", 0),
##        (assign, ":temp_honor", "$player_honor"),
##      (else_try),
##        (val_sub, ":temp_honor", "$player_honor"),
##      (try_end),
##      (try_for_range, ":unused",0,":num_nonlinear_steps"),
##        (ge, ":temp_honor", 10000),
##        (val_div, ":temp_honor", 2),
##        (val_div, ":honor_dif", 2),
##      (try_end),
##      (val_add, "$player_honor", ":honor_dif"),
  ]),
  # script_change_player_party_morale
  # Input: arg1 = morale difference
  # Output: none
  ("change_player_party_morale",
    [
      (store_script_param_1, ":morale_dif"),
      (party_get_morale, ":cur_morale", "p_main_party"),
      (val_clamp, ":cur_morale", 0, 100),
            
      (store_add, ":new_morale", ":cur_morale", ":morale_dif"),
      (val_clamp, ":new_morale", 0, 100),
      
      (party_set_morale, "p_main_party", ":new_morale"),
      (try_begin),
        (lt, ":new_morale", ":cur_morale"),
        (store_sub, reg1, ":cur_morale", ":new_morale"),
        (display_message, "str_party_lost_morale"),
      (else_try),
        (gt, ":new_morale", ":cur_morale"),
        (store_sub, reg1, ":new_morale", ":cur_morale"),
        (display_message, "str_party_gained_morale"),
      (try_end),
  ]),
  # script_cf_player_has_item_without_modifier
  # Input: arg1 = item_id, arg2 = modifier
  # Output: none (can_fail)
  ("cf_player_has_item_without_modifier",
    [
      (store_script_param, ":item_id", 1),
      (store_script_param, ":modifier", 2),
      (player_has_item, ":item_id"),
      #checking if any of the meat is not rotten
      (assign, ":has_without_modifier", 0),
      (troop_get_inventory_capacity, ":inv_size", "trp_player"),
      (try_for_range, ":i_slot", 0, ":inv_size"),
        (troop_get_inventory_slot, ":cur_item", "trp_player", ":i_slot"),
        (eq, ":cur_item", ":item_id"),
        (troop_get_inventory_slot_modifier, ":cur_modifier", "trp_player", ":i_slot"),
        (neq, ":cur_modifier", ":modifier"),
        (assign, ":has_without_modifier", 1),
        (assign, ":inv_size", 0), #break
      (try_end),
      (eq, ":has_without_modifier", 1),
  ]),
  # script_get_player_party_morale_values
  # Output: reg0 = player_party_morale_target
  ("get_player_party_morale_values",
    [
      (party_get_num_companion_stacks, ":num_stacks","p_main_party"),
      (assign, ":num_men", 0),
      (try_for_range, ":i_stack", 1, ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop","p_main_party",":i_stack"),
        (try_begin),
          (troop_is_hero, ":stack_troop"),
          (val_add, ":num_men", 1), #it was 3 in "Mount&Blade", now it is 1 in Warband
        (else_try),
          (party_stack_get_size, ":stack_size","p_main_party",":i_stack"),
          (val_add, ":num_men", ":stack_size"),
        (try_end),
      (try_end),
      (assign, "$g_player_party_morale_modifier_party_size", ":num_men"),
    
      (store_skill_level, ":player_leadership", "skl_leadership", "trp_player"),
	  #gekokujo 3.1 increased morale from leadership start
	  (store_attribute_level, ":player_cha", "$map_talk_troop", ca_charisma), 
	  (store_attribute_level, ":player_int", "$map_talk_troop", ca_intelligence), 
	  #gekokujo 3.1 increased morale from leadership end
      
      (try_begin),
        (eq, "$players_kingdom", "fac_player_supporters_faction"),
        (faction_get_slot, ":cur_faction_king", "$players_kingdom", slot_faction_leader),
        (eq, ":cur_faction_king", "trp_player"),
		#gekokujo 3.1 increased morale from leadership start
        #(store_mul, "$g_player_party_morale_modifier_leadership", ":player_leadership", 15),
        (store_mul, "$g_player_party_morale_modifier_leadership", ":player_leadership", 20),
		
		(val_mul, ":player_cha", 3),
		(val_add, "$g_player_party_morale_modifier_leadership", ":player_cha"),
		
		(val_mul, ":player_int", 2),
		(val_add, "$g_player_party_morale_modifier_leadership", ":player_int"),
		#gekokujo 3.1 increased morale from leadership end
      (else_try),  
		#gekokujo 3.1 increased morale from leadership start
        #(store_mul, "$g_player_party_morale_modifier_leadership", ":player_leadership", 12),
        (store_mul, "$g_player_party_morale_modifier_leadership", ":player_leadership", 16),
		
		(val_mul, ":player_cha", 2),
		(val_add, "$g_player_party_morale_modifier_leadership", ":player_cha"),
		
		(val_mul, ":player_int", 1),
		(val_add, "$g_player_party_morale_modifier_leadership", ":player_int"),
		#gekokujo 3.1 increased morale from leadership end
      (try_end),  
      
      (assign, ":new_morale", "$g_player_party_morale_modifier_leadership"),
      (val_sub, ":new_morale", "$g_player_party_morale_modifier_party_size"),
      
      (val_add, ":new_morale", 50),
      
      (assign, "$g_player_party_morale_modifier_food", 0),
      (try_for_range, ":cur_edible", food_begin, food_end),      
        (call_script, "script_cf_player_has_item_without_modifier", ":cur_edible", imod_rotten),
        (item_get_slot, ":food_bonus", ":cur_edible", slot_item_food_bonus),
        
        (val_mul, ":food_bonus", 3),
        (val_div, ":food_bonus", 2),
        
        (val_add, "$g_player_party_morale_modifier_food", ":food_bonus"),
      (try_end),
      (val_add, ":new_morale", "$g_player_party_morale_modifier_food"),

      (try_begin),
        (eq, "$g_player_party_morale_modifier_food", 0),
        (assign, "$g_player_party_morale_modifier_no_food", 30),
        (val_sub, ":new_morale", "$g_player_party_morale_modifier_no_food"),
      (else_try),
        (assign, "$g_player_party_morale_modifier_no_food", 0),
      (try_end),

      (assign, "$g_player_party_morale_modifier_debt", 0),
      (try_begin),
        (gt, "$g_player_debt_to_party_members", 0),
        (call_script, "script_calculate_player_faction_wage"),
        (assign, ":total_wages", reg0),
        (store_mul, "$g_player_party_morale_modifier_debt", "$g_player_debt_to_party_members", 10),
		(val_max, ":total_wages", 1),
        (val_div, "$g_player_party_morale_modifier_debt", ":total_wages"),
        (val_clamp, "$g_player_party_morale_modifier_debt", 1, 31),
        (val_sub, ":new_morale", "$g_player_party_morale_modifier_debt"),
      (try_end),

      (val_clamp, ":new_morale", 0, 100),
      (assign, reg0, ":new_morale"),
      ]),
  # script_diplomacy_start_war_between_kingdoms
  # Input: arg1 = kingdom_1, arg2 = kingdom_2, arg3 = initializing_war_peace_cond
  # Output: none
  ("diplomacy_start_war_between_kingdoms", #sets relations between two kingdoms and their vassals.
    [
      (store_script_param, ":kingdom_a", 1),
      (store_script_param, ":kingdom_b", 2),
      (store_script_param, ":initializing_war_peace_cond", 3), #1 = after start of game

	  (call_script, "script_npc_decision_checklist_peace_or_war", ":kingdom_a", ":kingdom_b", -1),
	  (assign, ":explainer_string", reg1),
	  
	  #
    ##diplomacy begin
    (try_begin),
      (lt, ":initializing_war_peace_cond", 2),
    ##diplomacy end
	  (try_begin),
	    (eq, ":kingdom_a", "fac_player_supporters_faction"),
		(assign, ":war_event", logent_player_faction_declares_war),
	  (else_try),	
		(eq, ":explainer_string", "str_s12s15_declared_war_to_control_calradia"),
		(assign, ":war_event", logent_player_faction_declares_war), #for savegame compatibility, this event stands in for the attempt to declare war on all of Japan
	  (else_try),
		(eq, ":explainer_string", "str_s12s15_considers_s16_to_be_dangerous_and_untrustworthy_and_shehe_wants_to_bring_s16_down"),
		(assign, ":war_event", logent_faction_declares_war_out_of_personal_enmity),
	  (else_try),	
		(eq, ":explainer_string", "str_s12s15_is_anxious_to_reclaim_old_lands_such_as_s18_now_held_by_s16"),
		(assign, ":war_event", logent_faction_declares_war_to_regain_territory),
	  (else_try),	
		(eq, ":explainer_string", "str_s12s15_faces_too_much_internal_discontent_to_feel_comfortable_ignoring_recent_provocations_by_s16s_subjects"),
		(assign, ":war_event", logent_faction_declares_war_to_respond_to_provocation),
	  (else_try),	
		(eq, ":explainer_string", "str_s12s15_is_alarmed_by_the_growing_power_of_s16"),
		(assign, ":war_event", logent_faction_declares_war_to_curb_power),
	  (try_end),
	  (call_script, "script_add_log_entry", ":war_event", ":kingdom_a", 0, 0, ":kingdom_b"),
	  
	  
	  
	  (call_script, "script_diplomacy_faction_get_diplomatic_status_with_faction", ":kingdom_a", ":kingdom_b"),
	  (assign, ":current_diplomatic_status", reg0),
	  (try_begin), #effects of policy only after the start of the game
	    (eq, ":initializing_war_peace_cond", 1),
		(eq, ":current_diplomatic_status", -1),
		(call_script, "script_faction_follows_controversial_policy", ":kingdom_a", logent_policy_ruler_declares_war_with_justification),
	  (else_try),
	    (eq, ":initializing_war_peace_cond", 1),	  
		(eq, ":current_diplomatic_status", 0),
		(call_script, "script_faction_follows_controversial_policy", ":kingdom_a", logent_policy_ruler_attacks_without_provocation),
	  (else_try),
		(eq, ":current_diplomatic_status", 1),
		(call_script, "script_faction_follows_controversial_policy", ":kingdom_a", logent_policy_ruler_breaks_truce),
	  (try_end),
	  ##diplomacy begin
    (else_try),
      (assign, ":war_event", logent_faction_declares_war_to_fulfil_pact),
      (call_script, "script_faction_follows_controversial_policy", ":kingdom_a", logent_policy_ruler_declares_war_with_justification),
      (assign, ":initializing_war_peace_cond", 1),
	  (try_end),
	  ##diplomacy end
      
      (store_relation, ":relation", ":kingdom_a", ":kingdom_b"),
      (val_min, ":relation", -10),
      (val_add, ":relation", -30),
      (set_relation, ":kingdom_a", ":kingdom_b", ":relation"),

      (try_begin),
        (eq, "$players_kingdom", ":kingdom_a"),
        (store_relation, ":relation", "fac_player_supporters_faction", ":kingdom_b"),
        (val_min, ":relation", -30),
        (call_script, "script_set_player_relation_with_faction", ":kingdom_b", ":relation"),
      (else_try),
        (eq, "$players_kingdom", ":kingdom_b"),
        (store_relation, ":relation", "fac_player_supporters_faction", ":kingdom_a"),
        (val_min, ":relation", -30),
        (call_script, "script_set_player_relation_with_faction", ":kingdom_a", ":relation"),
      (try_end),

      (try_begin),
        (eq, ":initializing_war_peace_cond", 1),
		
		#Remove this -- this scrambles who declares war on whom
#        (try_begin),
 #         (store_random_in_range, ":random_no", 0, 2),
  #        (this_or_next|eq, ":kingdom_a", "fac_player_supporters_faction"),
	#		(eq, ":random_no", 0),
     #     (assign, ":local_temp", ":kingdom_a"),
      #    (assign, ":kingdom_a", ":kingdom_b"),
       #   (assign, ":kingdom_b", ":local_temp"),
        #(try_end),
		
        (str_store_faction_name_link, s1, ":kingdom_a"),
        (str_store_faction_name_link, s2, ":kingdom_b"),
        (display_log_message, "@{s1} has declared war against {s2}."),

		(store_current_hours, ":hours"),
		(faction_set_slot, ":kingdom_a", slot_faction_ai_last_decisive_event, ":hours"),
		(faction_set_slot, ":kingdom_b", slot_faction_ai_last_decisive_event, ":hours"),
		
		#set provocation and truce days
		(store_add, ":truce_slot", ":kingdom_b", slot_faction_truce_days_with_factions_begin),
		(store_add, ":provocation_slot", ":kingdom_b", slot_faction_provocation_days_with_factions_begin),
		(val_sub, ":truce_slot", kingdoms_begin),
		(val_sub, ":provocation_slot", kingdoms_begin),
		(faction_set_slot, ":kingdom_a", ":truce_slot", 0),
		(faction_set_slot, ":kingdom_a", ":provocation_slot", 0),

		(store_add, ":truce_slot", ":kingdom_a", slot_faction_truce_days_with_factions_begin),
		(store_add, ":provocation_slot", ":kingdom_a", slot_faction_provocation_days_with_factions_begin),
		(val_sub, ":truce_slot", kingdoms_begin),
		(val_sub, ":provocation_slot", kingdoms_begin),
		(faction_set_slot, ":kingdom_b", ":truce_slot", 0),
		(faction_set_slot, ":kingdom_b", ":provocation_slot", 0),
		
		#gekokujo diplomacy - less notification menus the better
		(try_begin),
		  (this_or_next|eq, "$players_kingdom", ":kingdom_a"),
		  (eq, "$players_kingdom", ":kingdom_b"),
		  (call_script, "script_add_notification_menu", "mnu_notification_war_declared", ":kingdom_a", ":kingdom_b"),
		  #gekokujo 3.0 once again re-disabled notification menus
		#(else_try),
		  ##gekokujo 3.0 temporarily re-enable notification menus since it is no longer insane
		  #(call_script, "script_add_notification_menu", "mnu_notification_war_declared", ":kingdom_a", ":kingdom_b"),
		(try_end),
		
        (call_script, "script_update_faction_notes", ":kingdom_a"),
        (call_script, "script_update_faction_notes", ":kingdom_b"),
        (assign, "$g_recalculate_ais", 1),
      (try_end),
	  
	  (try_begin),
		(check_quest_active, "qst_cause_provocation"),
	    (neg|check_quest_succeeded, "qst_cause_provocation"),
		(this_or_next|eq, "$players_kingdom", ":kingdom_a"),
			(eq, "$players_kingdom", ":kingdom_b"),
		(call_script, "script_abort_quest", "qst_cause_provocation", 0),
	  (try_end),
    ##diplomacy begin
    #check for defensive
    (try_for_range, ":cur_kingdom", kingdoms_begin, kingdoms_end),
      (neq, ":cur_kingdom", ":kingdom_a"),
      (neq, ":cur_kingdom", ":kingdom_b"),

      (store_relation, ":cur_relation", ":cur_kingdom", ":kingdom_a"),
			(ge, ":cur_relation", 0), #AT PEACE

      (store_add, ":truce_slot", ":kingdom_b", slot_faction_truce_days_with_factions_begin),
  		(val_sub, ":truce_slot", kingdoms_begin),
  		(faction_get_slot, ":truce_days", ":cur_kingdom", ":truce_slot"),
  		##nested diplomacy start+ replace "40" with a named constant
  		#(gt, ":truce_days", 40),
  		(gt, ":truce_days", dplmc_treaty_defense_days_expire),
  		##nested diplomacy end+
  		(try_begin),
  		  (lt, ":initializing_war_peace_cond", 2), #only if war was not caused by defensive or alliance pact
  		  (call_script, "script_diplomacy_start_war_between_kingdoms", ":cur_kingdom", ":kingdom_a", 2),
  		(try_end),
    (try_end),

    #check for alliance
    (try_for_range, ":cur_kingdom", kingdoms_begin, kingdoms_end),
      (neq, ":cur_kingdom", ":kingdom_a"),
      (neq, ":cur_kingdom", ":kingdom_b"),

      (store_relation, ":cur_relation", ":cur_kingdom", ":kingdom_b"),
			(ge, ":cur_relation", 0), #AT PEACE

  		(store_add, ":truce_slot", ":kingdom_a", slot_faction_truce_days_with_factions_begin),
  		(val_sub, ":truce_slot", kingdoms_begin),
  		(faction_get_slot, ":truce_days", ":cur_kingdom", ":truce_slot"),
  		##nested diplomacy start+ replace "60" with a named constant
  		#(gt, ":truce_days", 60),
  		(gt, ":truce_days", dplmc_treaty_alliance_days_expire),
  		##nested diplomacy end+
  		(call_script, "script_diplomacy_start_war_between_kingdoms", ":cur_kingdom", ":kingdom_b", 3),
    (try_end),
    ##diplomacy end
  ]),
  ("diplomacy_party_attacks_neutral", #called from game_menus (plundering a village, raiding a village),  from dialogs: surprise attacking a neutral lord, any attack on caravan or villagers
#Has no effect if factions are already at war  
    [
      (store_script_param, ":attacker_party", 1),
      (store_script_param, ":defender_party", 2),
	  
	  (store_faction_of_party, ":attacker_faction", ":attacker_party"),
	  (store_faction_of_party, ":defender_faction", ":defender_party"),
	  
	  (party_stack_get_troop_id, ":attacker_leader", ":attacker_party", 0),
	  
	  (try_begin),
		(eq, ":attacker_party", "p_main_party"),
		(neq, ":attacker_faction", "fac_player_supporters_faction"),
		(assign, ":attacker_faction", "$players_kingdom"),
	  (else_try),	
		(eq, ":attacker_party", "p_main_party"),
		(eq, ":attacker_faction", "fac_player_supporters_faction"),
	  (try_end),
	  
	  (try_begin),
	    (eq, ":attacker_party", "p_main_party"),
		(store_relation, ":relation", ":attacker_faction", ":defender_faction"),
	    (ge, ":relation", 0),
		(call_script, "script_change_player_honor", -2),
	  (try_end),
	  
	  
	  (try_begin),
		(check_quest_active, "qst_cause_provocation"),
		(quest_slot_eq, "qst_cause_provocation", slot_quest_target_faction, ":defender_faction"),
		(quest_get_slot, ":giver_troop", "qst_cause_provocation", slot_quest_giver_troop),
		(store_faction_of_troop, ":attacker_faction", ":giver_troop"),
		(call_script, "script_succeed_quest", "qst_cause_provocation"),		
	  (try_end),
	  
	  (call_script, "script_diplomacy_faction_get_diplomatic_status_with_faction", ":attacker_faction", ":defender_faction"),
	  (assign, ":diplomatic_status", reg0),
	  
	  (try_begin),
	    (eq, ":attacker_faction", "fac_player_supporters_faction"),
		(neg|faction_slot_eq, "fac_player_supporters_faction", slot_faction_state, sfs_active),
		#player faction inactive, no effect
	  (else_try),
		(eq, ":diplomatic_status", -2),
	    #war, no effect
	  (else_try),
	  
	    (eq, ":attacker_faction", "fac_player_supporters_faction"),
		(faction_slot_eq, ":attacker_faction", slot_faction_leader, "trp_player"),
		(call_script, "script_faction_follows_controversial_policy", "fac_player_supporters_faction",logent_policy_ruler_attacks_without_provocation),
	  (else_try),	
		(eq, ":diplomatic_status", 1),
		#truce
		(party_stack_get_troop_id, ":defender_party_leader", ":defender_party", 0),
		(try_begin),
			##diplomacy start+ add support for promoted kingdom ladies
			#(i.e. verify not a promoted kingdom lady, since they exist)
			(this_or_next|neg|is_between, ":defender_party_leader", kingdom_ladies_begin, kingdom_ladies_end),
				(neg|troop_slot_eq, ":defender_party_leader", slot_troop_occupation, slto_kingdom_hero),
			##diplomacy end+
			(neg|is_between, ":defender_party_leader", active_npcs_begin, active_npcs_end),
			(store_faction_of_party, ":defender_party_faction", ":defender_party"),
			(faction_get_slot, ":defender_party_leader", ":defender_party_faction", slot_faction_leader),
		(try_end),
		
		(call_script, "script_add_log_entry", logent_border_incident_troop_breaks_truce, ":attacker_leader", -1, ":defender_party_leader", ":attacker_faction"),
	  (else_try),	
		#truce
		(call_script, "script_add_log_entry", logent_border_incident_troop_attacks_neutral, ":attacker_leader", -1, ":defender_party_leader", ":attacker_faction"),
	  (try_end),
	  	  
	  (try_begin),
	    (is_between, ":defender_party", villages_begin, villages_end),
	    (call_script, "script_add_log_entry", logent_village_raided, ":attacker_leader",  ":defender_party", -1, ":defender_faction"),
	  (else_try),
	    (party_get_template_id, ":template", ":defender_party"),
	    (neq, ":template", "pt_kingdom_hero_party"),
		(try_begin),
			(ge, "$cheat_mode", 1),
			(str_store_faction_name, s5, ":defender_faction"),
			(display_message, "@{!}DEbug - {s5} caravan attacked"),
		(try_end),
		
	    (call_script, "script_add_log_entry", logent_caravan_accosted, ":attacker_leader",  -1, -1, ":defender_faction"),
	  (try_end),

	  (store_add, ":slot_truce_days", ":attacker_faction", slot_faction_provocation_days_with_factions_begin),
	  (val_sub, ":slot_truce_days", kingdoms_begin),
	  (faction_set_slot, ":defender_faction", ":slot_truce_days", 0),
	  
	  (store_add, ":slot_provocation_days", ":attacker_faction", slot_faction_provocation_days_with_factions_begin),
	  (val_sub, ":slot_provocation_days", kingdoms_begin),
	  (try_begin),
	    (neq, ":diplomatic_status", -2),
		(faction_slot_eq, ":defender_faction", ":slot_provocation_days", 0),
		#gekokujo 3.0 provocation days increase start
		(faction_set_slot, ":defender_faction", ":slot_provocation_days", 60),
		#(faction_set_slot, ":defender_faction", ":slot_provocation_days", 30),
		#gekokujo 3.0 provocation days increase end
	  (try_end),	  
	]),
  # script_party_calculate_and_set_nearby_friend_enemy_follower_strengths
  # Input: party_no
  # Output: none
  ("party_calculate_and_set_nearby_friend_enemy_follower_strengths",
    [
      (store_script_param, ":party_no", 1),
      (assign, ":follower_strength", 0),
      (assign, ":friend_strength", 0),
      (assign, ":enemy_strength", 0),
      (store_faction_of_party, ":party_faction", ":party_no"),
	  ##diplomacy start+ add support for promoted kingdom ladies
      (store_add, ":end_cond", heroes_end, 1),#<- changed active_npcs to heroes
      (try_for_range, ":iteration", heroes_begin, ":end_cond"),#<- changed active_npcs to heroes
        (try_begin),
          (eq, ":iteration", heroes_end),#<- changed active_npcs to heroes
          (assign, ":cur_troop", "trp_player"),
        (else_try),
          (assign, ":cur_troop", ":iteration"),
        (try_end),
		##diplomacy end+

        (troop_slot_eq, ":cur_troop", slot_troop_occupation, slto_kingdom_hero),
        (troop_get_slot, ":cur_troop_party", ":cur_troop", slot_troop_leaded_party),
        (ge, ":cur_troop_party", 0),
        (party_is_active, ":cur_troop_party"),

         
        #I moved these lines here from (*1) to faster process, ozan.
        (store_troop_faction, ":army_faction", ":cur_troop"),
        (store_relation, ":relation", ":army_faction", ":party_faction"),        
        (this_or_next|neq, ":relation", 0),
        (eq, ":army_faction", ":party_faction"),
        #ozan end


        (neq, ":party_no", ":cur_troop_party"),
        (party_get_slot, ":str", ":cur_troop_party", slot_party_cached_strength),
        (try_begin),
          (neg|is_between, ":party_no", centers_begin, centers_end),
          (party_slot_eq, ":cur_troop_party", slot_party_ai_state, spai_accompanying_army),
          (party_get_slot, ":commander_party", ":cur_troop_party", slot_party_ai_object),
          (eq, ":commander_party", ":party_no"),
          (val_add, ":follower_strength", ":str"),
        (else_try),
          (store_distance_to_party_from_party, ":distance", ":cur_troop_party", ":party_no"),
          (lt, ":distance", 20),
        
          #(*1)
          
          (try_begin),
            (lt, ":distance", 5),
            (assign, ":str_divided", ":str"),
          (else_try),
            (lt, ":distance", 10),
            (store_div, ":str_divided", ":str", 2),
          (else_try),
            (lt, ":distance", 15),
            (store_div, ":str_divided", ":str", 4),
          (else_try),
            (store_div, ":str_divided", ":str", 8),
          (try_end),
        
          (try_begin),
            (this_or_next|eq, ":army_faction", ":party_faction"),
            (gt, ":relation", 0),
            (val_add, ":friend_strength", ":str_divided"),
          (else_try),
            (lt, ":relation", 0),
            (val_add, ":enemy_strength", ":str_divided"),
          (try_end),
        (try_end),
      (try_end),
      
      (party_set_slot, ":party_no", slot_party_follower_strength, ":follower_strength"),
      (party_set_slot, ":party_no", slot_party_nearby_friend_strength, ":friend_strength"),
      (party_set_slot, ":party_no", slot_party_nearby_enemy_strength, ":enemy_strength"),
      ]),
  # script_init_ai_calculation
  # Input: none
  # Output: none
  ("init_ai_calculation",
    [
      ##diplomacy start+
	  #(assign, ":real_party_strength"),
	  ##If terrain advantage is enabled, use it to calculate troop strengths.
      (try_begin),
         (eq, "$g_dplmc_terrain_advantage", DPLMC_TERRAIN_ADVANTAGE_ENABLE),

		 #First update all lords
		 (try_for_range, ":cur_troop", heroes_begin, heroes_end),
            (troop_slot_eq, ":cur_troop", slot_troop_occupation, slto_kingdom_hero),
            (troop_get_slot, ":cur_party", ":cur_troop", slot_troop_leaded_party),
			(gt, ":cur_party", 0),
            (party_is_active, ":cur_party"),

		    (party_get_current_terrain, ":terrain_code", ":cur_party"),

			(party_get_attached_to, ":attachment", ":cur_party"),
			(try_begin),
				(ge, ":attachment", 0),
				(is_between, ":attachment", centers_begin, centers_end),
				(assign, ":terrain_code", dplmc_terrain_code_siege),#siege constant defined in header_terrain_types.py
			(try_end),

            (call_script, "script_dplmc_party_calculate_strength_in_terrain", ":cur_party", ":terrain_code", 0, 1), #will update slot_party_cached_strength
         (try_end),

		 #Then update player
		 (party_get_current_terrain, ":terrain_code", "p_main_party"),

		 (party_get_attached_to, ":attachment", "p_main_party"),
			(try_begin),
				(ge, ":attachment", 0),
				(is_between, ":attachment", centers_begin, centers_end),
				(assign, ":terrain_code", dplmc_terrain_code_siege),#siege constant defined in header_terrain_types.py
			(try_end),

		 (call_script, "script_dplmc_party_calculate_strength_in_terrain", "p_main_party", ":terrain_code", 0, 1), #will update slot_party_cached_strength

         (try_for_range, ":cur_center", walled_centers_begin, walled_centers_end),
		    #Update with walled center alterations
            (call_script, "script_dplmc_party_calculate_strength_in_terrain", ":cur_center", -2, 0, 1),
         (try_end),
      (else_try),
	   #The old behavior, unchanged:
         (try_for_range, ":cur_troop", heroes_begin, heroes_end),
            (troop_slot_eq, ":cur_troop", slot_troop_occupation, slto_kingdom_hero),
            (troop_get_slot, ":cur_party", ":cur_troop", slot_troop_leaded_party),
            (party_is_active, ":cur_party"),
            (call_script, "script_party_calculate_strength", ":cur_party", 0), #will update slot_party_cached_strength
         (try_end),
         (call_script, "script_party_calculate_strength", "p_main_party", 0), #will update slot_party_cached_strength
         (try_for_range, ":cur_center", walled_centers_begin, walled_centers_end),
            (call_script, "script_party_calculate_strength", ":cur_center", 0), #will update slot_party_cached_strength
         (try_end),
      (try_end),
      ##diplomacy end+

	  #gekokujo 3.0 integrating motomataru's campaign AI
      #(try_for_range, ":cur_center", walled_centers_begin, walled_centers_end),
	  (try_for_range, ":cur_center", centers_begin, centers_end),
        (call_script, "script_party_calculate_and_set_nearby_friend_enemy_follower_strengths", ":cur_center"),
      (try_end),

      (try_for_range, ":cur_troop", heroes_begin, heroes_end),
        (troop_get_slot, ":cur_troop_party", ":cur_troop", slot_troop_leaded_party),
        (gt, ":cur_troop_party", 0),
        (party_is_active, ":cur_troop_party"),
        (call_script, "script_party_calculate_and_set_nearby_friend_enemy_follower_strengths", ":cur_troop_party"),
      (try_end),
      (call_script, "script_party_calculate_and_set_nearby_friend_enemy_follower_strengths", "p_main_party"),
      ]),
  #When a lord changes factions
  #When a center changes factions
  #When a center is captured
  #When a marshal is defeated
  #Every 23 hours
    ("recalculate_ais",
    [
      (call_script, "script_init_ai_calculation"),
            
      (try_for_range, ":faction_no", kingdoms_begin, kingdoms_end),
      (assign, reg8, ":faction_no"),
        (faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
        #(neg|faction_slot_eq, ":faction_no",  slot_faction_marshall, "trp_player"),
		# NE dk
		(try_begin), 
		(neq, ":faction_no", "fac_dark_knights"),
		(call_script, "script_decide_faction_ai", ":faction_no"),
		(else_try),
	    (call_script, "script_decide_faction_ai_dk2", ":faction_no"),
		(try_end),
		# NE end dk
      (try_end),

	  ##diplomacy start+ add support for promoted kingdom ladies
	  (try_for_range, ":troop_no", heroes_begin, heroes_end),#<- change active_npcs to heroes
	  ##diplomacy end+
        (store_troop_faction, ":faction_no", ":troop_no"),        
        (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
        (call_script, "script_calculate_troop_ai", ":troop_no"),
      (try_end),	  
    ]),
  # script_calculate_troop_ai
  # Input: troop_no
  # Output: none
  #Now called directly from scripts
  ("calculate_troop_ai",
    [
      (store_script_param, ":troop_no", 1),

      (try_begin),
        (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
        (neg|troop_slot_ge, ":troop_no", slot_troop_prisoner_of_party, 0),
        (troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
        (gt, ":party_no", 0),
		(party_is_active, ":party_no"),
		##diplomacy start+
		#Testing notifications
		(party_get_slot, ":old_ai_state", ":party_no", slot_party_ai_state),
		#(party_get_slot, ":old_ai_object", ":party_no", slot_party_ai_object),
		##diplomacy end+
		(call_script, "script_npc_decision_checklist_party_ai", ":troop_no"), #This handles AI for both marshal and other parties		
		(call_script, "script_party_set_ai_state", ":party_no", reg0, reg1),
		##diplomacy start+
		#Notify the player of changes to spouse and affiliates
		(party_get_slot, ":new_ai_state", ":party_no", slot_party_ai_state),
		(party_get_slot, ":new_ai_object", ":party_no", slot_party_ai_object),

		##(this_or_next|neq, ":old_ai_object", ":new_ai_object",
		(neq, ":old_ai_state", ":new_ai_state"),
		(ge, "$g_dplmc_ai_changes", DPLMC_AI_CHANGES_LOW),
		#(assign, reg0, 0),
		#(try_begin),
		#	(this_or_next|troop_slot_eq, ":troop_no", slot_troop_spouse, "trp_player"),
		#	(troop_slot_eq, "trp_player", slot_troop_spouse, ":troop_no"),
		#	(assign, reg0, 1),
		##(else_try),
		##	(store_faction_of_troop, ":troop_faction", ":troop_no"),
		##	(is_between,
		##(else_try),
		#	(call_script, "script_dplmc_is_affiliated_family_member", ":troop_no"),
		#(try_end),
		(call_script, "script_dplmc_store_troop_is_eligible_for_affiliate_messages", ":troop_no"),
		(gt, reg0, 0),


		#Some of these have non-obvious secondary uses.
		#xxx TODO: Later, I should go and verify all of them.
		(str_store_troop_name, s0, ":troop_no"),

		(try_begin),
			(eq, ":new_ai_state", spai_besieging_center),
			(is_between, ":new_ai_object", centers_begin, centers_end),
			(str_store_party_name, s1, ":new_ai_object"),
			(display_message, "@{s0} is laying siege to {s1}."),
		(else_try),
			(eq, ":new_ai_state", spai_patrolling_around_center),
			(is_between, ":new_ai_object", centers_begin, centers_end),
			(str_store_party_name, s1, ":new_ai_object"),
			(display_message, "@{s0} is patrolling around {s1}."),
		(else_try),
			(eq, ":new_ai_state", spai_raiding_around_center),
			(is_between, ":new_ai_object", centers_begin, centers_end),
			(str_store_party_name, s1, ":new_ai_object"),
			(display_message, "@{s0} is raiding around {s1}."),
		(else_try),
			(eq, ":new_ai_state", spai_engaging_army),
			(gt, ":new_ai_object", -1),
			(party_is_active, ":new_ai_object"),
			(str_store_party_name, s1, ":new_ai_object"),
			(display_message, "@{s0} is engaging {s1}."),
		(else_try),
			(eq, ":new_ai_state", spai_accompanying_army),
			(gt, ":new_ai_object", -1),
			(party_is_active, ":new_ai_object"),
			(str_store_party_name, s1, ":new_ai_object"),
			(display_message, "@{s0} is accompanying {s1}."),
		(else_try),
			(eq, ":new_ai_state", spai_screening_army),
			(gt, ":new_ai_object", -1),
			(party_is_active, ":new_ai_object"),
			(str_store_party_name, s1, ":new_ai_object"),
			(display_message, "@{s0} is screening the advance of {s1}."),
		(else_try),
			(eq, ":new_ai_state", spai_trading_with_town),
			(is_between, ":new_ai_object", centers_begin, centers_end),
			(str_store_party_name, s1, ":new_ai_object"),
			(display_message, "@{s0} is trading with {s1}."),
		(else_try),
			(eq, ":new_ai_state", spai_retreating_to_center),
			(is_between, ":new_ai_object", centers_begin, centers_end),
			(str_store_party_name, s1, ":new_ai_object"),
			(display_message, "@{s0} is retreating to {s1}."),
		(else_try),
			(eq, ":new_ai_state", spai_visiting_village),
			(is_between, ":new_ai_object", centers_begin, centers_end),
			(str_store_party_name, s1, ":new_ai_object"),
			(display_message, "@{s0} is visiting {s1}."),
		(try_end),
		#Make it obvious that something went wrong if something tries to use the registers
		(str_store_string, s0, "str_ERROR_string"),
		(str_store_string, s1, "str_ERROR_string"),
		##diplomacy end+
      (try_end),			
    ]),
  # script_diplomacy_start_peace_between_kingdoms
  # Input: arg1 = kingdom_1, arg2 = kingdom_2, arg3 = initializing_war_peace_cond
  # Output: none
  ("diplomacy_start_peace_between_kingdoms", #sets relations between two kingdoms
    [
      (store_script_param, ":kingdom_a", 1),
      (store_script_param, ":kingdom_b", 2),
      (store_script_param, ":initializing_war_peace_cond", 3), #set to 1 if not the start of the game

      (store_relation, ":relation", ":kingdom_a", ":kingdom_b"),
      (val_max, ":relation", 0),
      (set_relation, ":kingdom_a", ":kingdom_b", ":relation"),
      (call_script, "script_exchange_prisoners_between_factions", ":kingdom_a", ":kingdom_b"),

      (try_begin),
        (eq, "$players_kingdom", ":kingdom_a"),
        (store_relation, ":relation", "fac_player_supporters_faction", ":kingdom_b"),
        (val_max, ":relation", 0),
        (call_script, "script_set_player_relation_with_faction", ":kingdom_b", ":relation"),
        (call_script, "script_event_kingdom_make_peace_with_kingdom", ":kingdom_b", "fac_player_supporters_faction"), #event cancels certain quests
      (else_try),
        (eq, "$players_kingdom", ":kingdom_b"),
        (store_relation, ":relation", "fac_player_supporters_faction", ":kingdom_a"),
        (val_max, ":relation", 0),
        (call_script, "script_set_player_relation_with_faction", ":kingdom_a", ":relation"),
        (call_script, "script_event_kingdom_make_peace_with_kingdom", ":kingdom_a", "fac_player_supporters_faction"), #event cancels certain quests
      (try_end),
      
      (try_for_range, ":cur_center", centers_begin, centers_end),
        (store_faction_of_party, ":faction_no", ":cur_center"),
        (this_or_next|eq, ":faction_no", ":kingdom_a"),
        (eq, ":faction_no", ":kingdom_b"),        
        (party_get_slot, ":besieger_party", ":cur_center", slot_center_is_besieged_by),
        (ge, ":besieger_party", 0), #town is under siege
        (party_is_active, ":besieger_party"),        
        (store_faction_of_party, ":besieger_party_faction_no", ":besieger_party"),
        (this_or_next|eq, ":besieger_party_faction_no", ":kingdom_a"),
        (eq, ":besieger_party_faction_no", ":kingdom_b"),
        (call_script, "script_lift_siege", ":cur_center", 0),
      (try_end),
      
      (try_begin),
        (this_or_next|eq, "$players_kingdom", ":kingdom_a"),
        (eq, "$players_kingdom", ":kingdom_b"),

        (ge, "$g_player_besiege_town", 0),
        (party_is_active, "$g_player_besiege_town"),        
        
        (store_faction_of_party, ":besieged_center_faction_no", "$g_player_besiege_town"),
        
        (this_or_next|eq, ":besieged_center_faction_no", ":kingdom_a"),
        (eq, ":besieged_center_faction_no", ":kingdom_b"),

        (call_script, "script_lift_siege", "$g_player_besiege_town", 0),
        (assign, "$g_player_besiege_town", -1),
      (try_end),

      (try_begin),
        (eq, ":initializing_war_peace_cond", 1),
        (str_store_faction_name_link, s1, ":kingdom_a"),
        (str_store_faction_name_link, s2, ":kingdom_b"),
        (display_log_message, "@{s1} and {s2} have made peace with each other."),
		#gekokujo diplomacy - less notification menus the better
		(try_begin),
		  (this_or_next|eq, "$players_kingdom", ":kingdom_a"),
		  (eq, "$players_kingdom", ":kingdom_b"),
		  (call_script, "script_add_notification_menu", "mnu_notification_peace_declared", ":kingdom_a", ":kingdom_b"), #stability penalty for early peace is in the menu		
		(try_end),
        (call_script, "script_event_kingdom_make_peace_with_kingdom", ":kingdom_a", ":kingdom_b"), #cancels quests
        (call_script, "script_event_kingdom_make_peace_with_kingdom", ":kingdom_b", ":kingdom_a"), #cancels quests
        (assign, "$g_recalculate_ais", 1),				
      (try_end),
	  
	  (try_begin), #add truce
		(store_add, ":truce_slot", ":kingdom_a", slot_faction_truce_days_with_factions_begin),
		(val_sub, ":truce_slot", kingdoms_begin),
		##diplomacy begin
	    #(faction_set_slot, ":kingdom_b", ":truce_slot", 40),
        ##nested diplomacy start+ replace "20" with constant for truce length
#        (faction_set_slot, ":kingdom_b", ":truce_slot", 20),
        (faction_set_slot, ":kingdom_b", ":truce_slot", dplmc_treaty_truce_days_initial),
        ##nested diplomacy end+
	    ##diplomacy end		
		(store_add, ":truce_slot", ":kingdom_b", slot_faction_truce_days_with_factions_begin),
		(val_sub, ":truce_slot", kingdoms_begin),
	    ##diplomacy begin
	    #(faction_set_slot, ":kingdom_a", ":truce_slot", 40),
        ##nested diplomacy start+ replace "20" with constant for truce length
        #(faction_set_slot, ":kingdom_a", ":truce_slot", 20),
        (faction_set_slot, ":kingdom_a", ":truce_slot", dplmc_treaty_truce_days_initial),
        ##nested diplomacy end+
        ##diplomacy end
		(store_add, ":slot_war_damage_inflicted_on_b", ":kingdom_b", slot_faction_war_damage_inflicted_on_factions_begin),
		(val_sub, ":slot_war_damage_inflicted_on_b", kingdoms_begin),
		#(faction_get_slot, ":damage_inflicted_by_a", ":kingdom_a", ":slot_war_damage_inflicted_on_b"),
		(faction_set_slot, ":kingdom_a", ":slot_war_damage_inflicted_on_b", 0),		
		(store_add, ":slot_war_damage_inflicted_on_a", ":kingdom_a", slot_faction_war_damage_inflicted_on_factions_begin),
		(val_sub, ":slot_war_damage_inflicted_on_a", kingdoms_begin),
		#(faction_get_slot, ":damage_inflicted_by_b", ":kingdom_b", ":slot_war_damage_inflicted_on_a"),
		(faction_set_slot, ":kingdom_b", ":slot_war_damage_inflicted_on_a", 0),		
	  (try_end),
  ]),
  ("event_kingdom_make_peace_with_kingdom",
    [
      (store_script_param_1, ":source_kingdom"),
      (store_script_param_2, ":target_kingdom"),
      (try_begin),
        (check_quest_active, "qst_capture_prisoners"),
        (try_begin),
          (eq, "$players_kingdom", ":source_kingdom"),
          (quest_slot_eq, "qst_capture_prisoners", slot_quest_target_faction, ":target_kingdom"),
          (call_script, "script_cancel_quest", "qst_capture_prisoners"),
        (else_try),
          (eq, "$players_kingdom", ":target_kingdom"),
          (quest_slot_eq, "qst_capture_prisoners", slot_quest_target_faction, ":source_kingdom"),
          (call_script, "script_cancel_quest", "qst_capture_prisoners"),
        (try_end),
      (try_end),
	  
      (try_begin),
        (check_quest_active, "qst_capture_enemy_hero"),
        (try_begin),
          (eq, "$players_kingdom", ":source_kingdom"),
          (quest_slot_eq, "qst_capture_enemy_hero", slot_quest_target_faction, ":target_kingdom"),
          (call_script, "script_cancel_quest", "qst_capture_enemy_hero"),
        (else_try),
          (eq, "$players_kingdom", ":target_kingdom"),
          (quest_slot_eq, "qst_capture_enemy_hero", slot_quest_target_faction, ":source_kingdom"),
          (call_script, "script_cancel_quest", "qst_capture_enemy_hero"),
        (try_end),
      (try_end),
	  
	  
	  
      (try_begin),
        (check_quest_active, "qst_persuade_lords_to_make_peace"),
	    (quest_get_slot, ":lord_1", "qst_persuade_lords_to_make_peace", slot_quest_target_troop),
	    (quest_get_slot, ":lord_2", "qst_persuade_lords_to_make_peace", slot_quest_object_troop),
		
		(try_begin),
			(lt, ":lord_1", 0),
			(val_mul, ":lord_1", -1),
		(try_end),
		(try_begin),
			(lt, ":lord_2", 0),
			(val_mul, ":lord_2", -1),
		(try_end),
		
		
	    (store_faction_of_troop, ":lord_1_faction", ":lord_1"),
	    (store_faction_of_troop, ":lord_2_faction", ":lord_2"),	  
	  
	    (this_or_next|eq, ":lord_1_faction", ":source_kingdom"),
			(eq, ":lord_2_faction", ":source_kingdom"),

	    (this_or_next|eq, ":lord_1_faction", ":target_kingdom"),
			(eq, ":lord_2_faction", ":target_kingdom"),

        (call_script, "script_cancel_quest", "qst_persuade_lords_to_make_peace"),
			
	  (try_end),
	  
	  #Rescue prisoners cancelled in simple_triggers
	  
	  (try_begin),
		(this_or_next|faction_slot_eq, ":target_kingdom", slot_faction_leader, "trp_player"),
		(faction_slot_eq, ":source_kingdom", slot_faction_leader, "trp_player"),
	  
		#gekokujo 3.0 reduced RTR rewards start
	    #(call_script, "script_change_player_right_to_rule", 3),
	    (call_script, "script_change_player_right_to_rule", 1),
		#gekokujo 3.0 reduced RTR rewards end
	  (try_end),
	  
  ]),
  #Aims to introduce a slightly simpler system in which the AI kings' reasoning could be made more  transparent to the player. At the start of the game, this may lead to less variation in outcomes, though
  ("randomly_start_war_peace_new",
    [
    (store_script_param_1, ":initializing_war_peace_cond"),
	
	(assign, ":players_kingdom_at_peace", 0), #if the player kingdom is at peace, then create an enmity
	(try_begin),
		(is_between, "$players_kingdom", "fac_kingdom_1", kingdoms_end),
		(assign, ":players_kingdom_at_peace", 1),
	(try_end),
	
    (try_for_range, ":cur_kingdom", "fac_kingdom_1", kingdoms_end),
        (faction_slot_eq, ":cur_kingdom", slot_faction_state, sfs_active),
	  
		(try_for_range, ":cur_kingdom_2", kingdoms_begin, kingdoms_end),
			(neq, ":cur_kingdom", ":cur_kingdom_2"),
			(faction_slot_eq, ":cur_kingdom_2", slot_faction_state, sfs_active),
            
            (assign,":jixu",1),
            (try_begin),
                (this_or_next|eq,":cur_kingdom","fac_kingdom_1"),
                (this_or_next|eq,":cur_kingdom","fac_kingdom_2"),
                (this_or_next|eq,":cur_kingdom","fac_kingdom_6"),
                (this_or_next|eq,":cur_kingdom","fac_kingdom_10"),
                (this_or_next|eq,":cur_kingdom","fac_kingdom_11"),
                (this_or_next|eq,":cur_kingdom","fac_kingdom_18"),
                (this_or_next|eq,":cur_kingdom","fac_kingdom_25"),
                (eq,":cur_kingdom","fac_kingdom_27"),
                (assign,":jixu",0),
            (else_try),
                (this_or_next|eq,":cur_kingdom","fac_kingdom_4"),
                (this_or_next|eq,":cur_kingdom","fac_kingdom_12"),
                (eq,":cur_kingdom","fac_kingdom_15"),
                (assign,":jixu",0),
            (try_end),
            (eq,":jixu",1),
            	
			(call_script, "script_npc_decision_checklist_peace_or_war", ":cur_kingdom", ":cur_kingdom_2", -1),
			(assign, ":kingdom_1_to_kingdom_2", reg0),
			
			(store_relation, ":cur_relation", ":cur_kingdom", ":cur_kingdom_2"),
			(try_begin),
				(lt, ":cur_relation", 0), #AT WAR
				
				(try_begin),
					(eq, ":cur_kingdom", "$players_kingdom"),
					(assign, ":players_kingdom_at_peace", 0),
				(try_end),
				
				(ge, ":kingdom_1_to_kingdom_2", 1),
								
	            (try_begin),
	                (eq, ":cur_kingdom_2", "fac_player_supporters_faction"),
					
					(store_mul, ":goodwill_level", ":kingdom_1_to_kingdom_2", 2),
					(store_random_in_range, ":random", 0, 20),
					(try_begin),
					(lt, ":random", ":goodwill_level"),
	                (call_script, "script_add_notification_menu", "mnu_question_peace_offer", ":cur_kingdom", 0),
					(try_end),
	            (else_try),
					(call_script, "script_npc_decision_checklist_peace_or_war", ":cur_kingdom_2", ":cur_kingdom", -1),
					(assign, ":kingdom_2_to_kingdom_1", reg0),
					(ge, ":kingdom_2_to_kingdom_1", 1),

					(store_mul, ":goodwill_level", ":kingdom_1_to_kingdom_2", ":kingdom_2_to_kingdom_1"),
					(store_random_in_range, ":random", 0, 20),
					(lt, ":random", ":goodwill_level"),

					(try_begin),
						(eq, "$g_include_diplo_explanation", 0),
						(assign, "$g_include_diplo_explanation", ":cur_kingdom"),
						(str_store_string, s57, "str_s14"),
					(try_end),	

	                (call_script, "script_diplomacy_start_peace_between_kingdoms", ":cur_kingdom", ":cur_kingdom_2", ":initializing_war_peace_cond"),
	            (try_end),
			# (else_try),
				# (ge, ":cur_relation", 0), #AT PEACE
			
			    # (call_script, "script_npc_decision_checklist_peace_or_war", ":cur_kingdom", ":cur_kingdom_2", -1),
				
				# #negative, leans towards war/positive, leans towards peace
				# (le, reg0, 0), #still no chance of war unless provocation, or at start of game
			 
			    # (assign, ":hostility", reg0),

			    # (call_script, "script_diplomacy_faction_get_diplomatic_status_with_faction", ":cur_kingdom", ":cur_kingdom_2"),
			    # (le, reg0, 0), #no truce

				# (val_add, ":hostility", reg0), #increase hostility if there is a provocation

				# (val_sub, ":hostility", 1), #greater chance at start of game
				# (val_add, ":hostility", ":initializing_war_peace_cond"), #this variable = 1 after the start
				
				# (store_mul, ":hostility_squared", ":hostility", ":hostility"),
				# (store_random_in_range, ":random", 0, 50),
			    # (lt, ":random", ":hostility_squared"),
				
				# (try_begin),
					# (eq, "$g_include_diplo_explanation", 0),
					# (assign, "$g_include_diplo_explanation", ":cur_kingdom"),
					# (str_store_string, s57, "str_s14"),
				# (try_end),	
                # (call_script, "script_diplomacy_start_war_between_kingdoms", ":cur_kingdom", ":cur_kingdom_2", ":initializing_war_peace_cond"),
				
				# (try_begin), #do some war damage for 
					# (eq, ":initializing_war_peace_cond", 0),
					# (store_random_in_range, ":war_damage_inflicted", 10, 120),			
					# (store_add, ":slot_war_damage_inflicted", ":cur_kingdom", slot_faction_war_damage_inflicted_on_factions_begin),
					# (val_sub, ":slot_war_damage_inflicted", kingdoms_begin),
					# (faction_set_slot, ":cur_kingdom_2",  ":slot_war_damage_inflicted", ":war_damage_inflicted"),
			
					# (store_add, ":slot_war_damage_inflicted", ":cur_kingdom_2", slot_faction_war_damage_inflicted_on_factions_begin),
					# (val_sub, ":slot_war_damage_inflicted", kingdoms_begin),
					# (faction_set_slot, ":cur_kingdom", ":slot_war_damage_inflicted", ":war_damage_inflicted"),
				# (try_end),
            # (try_end),
		# (try_end),
	# (try_end),	
	
	(try_begin),
		(eq, ":players_kingdom_at_peace", 1),
		(val_add, "$players_kingdom_days_at_peace", 1),
		(try_begin),
			(eq, "$cheat_mode", 1),
			(assign, reg3, "$players_kingdom_days_at_peace"),
			(display_message, "@{!}DEBUG -- Player's kingdom has had {reg3} days of peace"),
		(try_end),
	(else_try),	
		(assign, "$players_kingdom_days_at_peace", 0),
	(try_end),
	
     ]),
# script_exchange_prisoners_between_factions
# Input: arg1 = faction_no_1, arg2 = faction_no_2
  ("exchange_prisoners_between_factions",
   [
       (store_script_param_1, ":faction_no_1"),
       (store_script_param_2, ":faction_no_2"),
       (assign, ":faction_no_3", -1),
       (assign, ":faction_no_4", -1),
       (assign, ":free_companions_too", 0),
       (try_begin),
         (this_or_next|eq, "$players_kingdom", ":faction_no_1"),
         (eq, "$players_kingdom", ":faction_no_2"),
         (assign, ":faction_no_3", "fac_player_faction"),
         (assign, ":faction_no_4", "fac_player_supporters_faction"),
         (assign, ":free_companions_too", 1),
       (try_end),
	   
       (try_for_parties, ":party_no"),
         (store_faction_of_party, ":party_faction", ":party_no"),
         (this_or_next|eq, ":party_faction", ":faction_no_1"),
         (this_or_next|eq, ":party_faction", ":faction_no_2"),
         (this_or_next|eq, ":party_faction", ":faction_no_3"),
         (eq, ":party_faction", ":faction_no_4"),
         (party_get_num_prisoner_stacks, ":num_stacks", ":party_no"),
         (try_for_range_backwards, ":troop_iterator", 0, ":num_stacks"),
           (party_prisoner_stack_get_troop_id, ":cur_troop_id", ":party_no", ":troop_iterator"),                                                                             
           
           (assign, ":continue", 0),
           (try_begin),
			 #gekokujo 3.0 microfactions! include fort companions start
             #(is_between, ":cur_troop_id", companions_begin, companions_end),
             (is_between, ":cur_troop_id", companions_begin, fort_companions_end),
			 #gekokujo 3.0 microfactions! include fort companions end
             (eq, ":free_companions_too", 1),
             (assign, ":continue", 1),
           (else_try),                        
			 #gekokujo 3.0 microfactions! include fort companions start
             #(neg|is_between, ":cur_troop_id", companions_begin, companions_end),             
             (neg|is_between, ":cur_troop_id", companions_begin, fort_companions_end),
			 #gekokujo 3.0 microfactions! include fort companions end
             (store_troop_faction, ":cur_faction", ":cur_troop_id"),
             (this_or_next|eq, ":cur_faction", ":faction_no_1"),
             (this_or_next|eq, ":cur_faction", ":faction_no_2"),
             (this_or_next|eq, ":cur_faction", ":faction_no_3"),
             (eq, ":cur_faction", ":faction_no_4"),
             (assign, ":continue", 1),
           (try_end),                        
           (eq, ":continue", 1),
           
           (try_begin),
             (troop_is_hero, ":cur_troop_id"),
             (call_script, "script_remove_troop_from_prison", ":cur_troop_id"),
           (try_end),
           (party_prisoner_stack_get_size, ":stack_size", ":party_no", ":troop_iterator"),
           (party_remove_prisoners, ":party_no", ":cur_troop_id", ":stack_size"),
         (try_end),
       (try_end),
	   
    ]),
  # script_add_notification_menu
  # Input: arg1 = menu_no, arg2 = menu_var_1, arg3 = menu_var_2
  # Output: none
  ("add_notification_menu",
    [
      (try_begin),        
        (eq, "$g_infinite_camping", 0),
        (store_script_param, ":menu_no", 1),
        (store_script_param, ":menu_var_1", 2),
        (store_script_param, ":menu_var_2", 3),
        (assign, ":end_cond", 1),      
        (try_for_range, ":cur_slot", 0, ":end_cond"),
          (try_begin),
            (troop_slot_ge, "trp_notification_menu_types", ":cur_slot", 1),
            (val_add, ":end_cond", 1),
          (else_try),
            (troop_set_slot, "trp_notification_menu_types", ":cur_slot", ":menu_no"),
            (troop_set_slot, "trp_notification_menu_var1", ":cur_slot", ":menu_var_1"),
            (troop_set_slot, "trp_notification_menu_var2", ":cur_slot", ":menu_var_2"),
          (try_end),
        (try_end),
      (try_end),
      ]),
  # script_enter_court
  # Input: arg1 = center_no
  # Output: none
  #other search term: setup_court
  ("enter_court",
    [
      (store_script_param_1, ":center_no"),
      
      (assign, "$talk_context", tc_court_talk),

      (set_jump_mission,"mt_visit_town_castle"),
         
      (mission_tpl_entry_clear_override_items, "mt_visit_town_castle", 0),
      #(mission_tpl_entry_set_override_flags, "mt_visit_town_castle", 0, af_override_all),
      
      (party_get_slot, ":castle_scene", ":center_no", slot_town_castle),
      (modify_visitors_at_site,":castle_scene"),
      (reset_visitors),
      #Adding guards
      (store_faction_of_party, ":center_faction", ":center_no"),
      (faction_get_slot, ":guard_troop", ":center_faction", slot_faction_guard_troop),
      ##diplomacy begin
      (try_begin),
         (eq, ":center_faction", "$players_kingdom"),
         (is_between, "$g_player_culture", npc_kingdoms_begin, npc_kingdoms_end),
         (faction_get_slot, ":guard_troop", "$g_player_culture", slot_faction_guard_troop),
	  ##nested diplomacy start+
	  (else_try),
	     #Reflect multicultural empires.
		 (party_get_slot, ":town_lord", ":center_no", slot_town_lord),
		 (gt, ":town_lord", "trp_player"),
		 (troop_get_slot, ":lord_original_faction", ":town_lord", slot_troop_original_faction),
		 (neq, ":lord_original_faction", ":center_faction"),
		 (is_between, ":lord_original_faction", npc_kingdoms_begin, npc_kingdoms_end),
		 (this_or_next|party_slot_eq, ":center_no", slot_center_original_faction, ":lord_original_faction"),
			(troop_slot_eq, ":town_lord", slot_troop_home, ":center_no"),
		 (faction_get_slot, ":guard_troop", ":lord_original_faction", slot_faction_guard_troop),
	  ##nested diplomacy end+
      (try_end),
      ##diplomacy end
      (try_begin),
        (le, ":guard_troop", 0),
		#diplomacy start+
		#rubik changes this in Custom Commander, and I agree: the "generic" guard
		#should be non-faction-specific.
		##OLD:
        #(assign, ":guard_troop", "trp_gekokujo_uesugi_veteran_retainer"),
		##NEW:
		(assign, ":guard_troop", "trp_hired_warrior_veteran"),
		##diplomacy end+
      (try_end),
      (set_visitor, 6, ":guard_troop"),
      (set_visitor, 7, ":guard_troop"),

      (assign, ":cur_pos", 16),

	  (try_begin),
		(troop_get_slot, ":player_spouse", "trp_player", slot_troop_spouse),
	    (gt, ":player_spouse", 0),
		(troop_slot_eq, ":player_spouse", slot_troop_cur_center, ":center_no"),
        (set_visitor, ":cur_pos", ":player_spouse"),
        (val_add,":cur_pos", 1),
	  (else_try),	
		(troop_get_slot, ":player_betrothed", "trp_player", slot_troop_betrothed),
	    (gt, ":player_betrothed", 0),
		(troop_slot_eq, ":player_betrothed", slot_troop_cur_center, ":center_no"),
        (set_visitor, ":cur_pos", ":player_betrothed"),
        (val_add,":cur_pos", 1),
	  (try_end),
	  
	  (try_begin),
		(eq, "$g_player_court", ":center_no"),
		(gt, "$g_player_minister", 0),
		(neg|troop_slot_eq, "trp_player", slot_troop_spouse, "$g_player_minister"),
        (set_visitor, ":cur_pos", "$g_player_minister"),
        (val_add,":cur_pos", 1),
	  (try_end),	  
    ##diplomacy begin
    (try_begin),
      (gt, "$g_player_chamberlain", 0),
      (call_script, "script_dplmc_appoint_chamberlain"),  #fix for wrong troops after update
      (party_get_slot, ":town_lord", ":center_no", slot_town_lord),
      (eq, ":town_lord", "trp_player"),
      (set_visitor, ":cur_pos", "$g_player_chamberlain"),
      (val_add,":cur_pos", 1),
    (try_end),

    (try_begin),
      (gt, "$g_player_constable", 0),
      (call_script, "script_dplmc_appoint_constable"),  #fix for wrong troops after update
      (party_get_slot, ":town_lord", ":center_no", slot_town_lord),
      (eq, ":town_lord", "trp_player"),
      (set_visitor, ":cur_pos", "$g_player_constable"),
      (val_add,":cur_pos", 1),
    (try_end),

    (try_begin),
      (gt, "$g_player_chancellor", 0),
      (call_script, "script_dplmc_appoint_chancellor"), #fix for wrong troops after update
      (party_get_slot, ":town_lord", ":center_no", slot_town_lord),
      (eq, ":town_lord", "trp_player"),
      (set_visitor, ":cur_pos", "$g_player_chancellor"),
      (val_add,":cur_pos", 1),
    (try_end),
    ##diplomacy end
	  
	  #Lords wishing to pledge allegiance - inactive, but part of player faction
	  (try_begin),
		(eq, "$g_player_court", ":center_no"),
	    (faction_slot_eq, ":center_faction", slot_faction_leader, "trp_player"),
		##diplomacy start+
		#It's not exactly clear if this would work for kingdom ladies.  If they
		#can go from slto_kingdom_lady to slto_inactive, this could take them
		#from there to slto_kingdom_hero unintentionally.
		#
		#Because of this, don't enable this for now.  Elsewhere (where defections
		#occur) add alternate behavior for promoted kingdom ladies.
		#
		#TODO: Later, make sure that kingdom ladies are never inactive normally,
		#so this loop can be expanded to work with them.
		##diplomacy end+
	    (try_for_range, ":active_npc", active_npcs_begin, active_npcs_end),
	      (store_faction_of_troop, ":active_npc_faction", ":active_npc"),
	      (eq, ":active_npc_faction", "fac_player_supporters_faction"),
	      (troop_slot_eq, ":active_npc", slot_troop_occupation, slto_inactive),
	      (neg|troop_slot_ge, ":active_npc", slot_troop_prisoner_of_party, 0), #if he/she is not prisoner in any center.
	      (neq, ":active_npc", "$g_player_minister"),
	      (set_visitor, ":cur_pos", ":active_npc"),	      
	      (val_add,":cur_pos", 1),
		(try_end),
	  (try_end),	  

      ##diplomacy start+
      #Show heroes you haven't seen recently first, to deal with crowded feast halls
      #(call_script, "script_get_heroes_attached_to_center", ":center_no", "p_temp_party"),
      (call_script, "script_dplmc_time_sorted_heroes_for_center", ":center_no", "p_temp_party"),
	  #Reserve a certain number of feast positions for ladies, both for practical
	  #reasons of courtship and for visual variety.
	  (try_begin),
		#If the player is unmarried, reserve zero to 8 slots for women
		(lt, ":player_spouse", 1),
		(store_random_in_range, ":reserved", 0, 9),
	  (else_try),
		#If the player is married, reserve zero to four slots for women
		(store_random_in_range, ":reserved", 0, 5),
	  (try_end),
	  (store_sub, ":non_lady_max", 32, ":reserved"),
      #diplomacy end+
      (party_get_num_companion_stacks, ":num_stacks","p_temp_party"),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop","p_temp_party",":i_stack"),
		##diplomacy start+
        #(lt, ":cur_pos", 32), # spawn up to entry point 32 - is it possible to add another 10 spots?
		(lt, ":cur_pos", ":non_lady_max"),#Leave some room for ladies in huge feasts
		##diplomacy end+
        (set_visitor, ":cur_pos", ":stack_troop"),
        (val_add,":cur_pos", 1),
      (try_end),
      (try_for_range, ":cur_troop", kingdom_ladies_begin, kingdom_ladies_end),
	    (neq, ":cur_troop", "trp_knight_1_1_wife"), #The one who should not appear in game
        #(troop_slot_eq, ":cur_troop", slot_troop_occupation, slto_kingdom_lady),
        (troop_slot_eq, ":cur_troop", slot_troop_cur_center, ":center_no"),
		
		(assign, ":lady_meets_visitors", 0),
		(try_begin),
			(this_or_next|troop_slot_eq, "trp_player", slot_troop_spouse, ":cur_troop"), #player spouse goes in position of honor
			(this_or_next|troop_slot_eq, "trp_player", slot_troop_betrothed, ":cur_troop"), #player spouse goes in position of honor
			(this_or_next|troop_slot_eq, ":cur_troop", slot_troop_spouse, "trp_player"), #player spouse goes in position of honor
				(troop_slot_eq, ":cur_troop", slot_troop_betrothed, "trp_player"),
				
			(assign, ":lady_meets_visitors", 0), #She is already in the place of honor
		
			(try_begin),
				(eq, "$cheat_mode", 1),
				(str_store_troop_name, s4, ":cur_troop"),
				(display_message, "str_s4_is_present_at_the_center_and_in_place_of_honor"),
			(try_end),
		
		(else_try), #lady is troop
			(store_faction_of_troop, ":lady_faction", ":cur_troop"),
			(neq, ":lady_faction", ":center_faction"),
			
			(assign, ":lady_meets_visitors", 1),
			
			
			(try_begin),
				(eq, "$cheat_mode", 1),
				(str_store_troop_name, s4, ":cur_troop"),
				(display_message, "str_s4_is_present_at_the_center_as_a_refugee"),
			(try_end),

		(else_try),
			(troop_slot_ge, ":cur_troop", slot_troop_spouse, 1),
			
			(try_begin),
			 #married ladies at a feast will not mingle - this is ahistorical, as married women and widows probably had much more freedom than unmarried ones, at least in the West, but the game needs to leave slots for them to show off their unmarried daughters
				(faction_slot_eq, ":center_faction", slot_faction_ai_state, sfai_feast),
				(faction_slot_eq, ":center_faction", slot_faction_ai_object, ":center_no"),
				(assign, ":lady_meets_visitors", 0),
				
				(try_begin),
					(eq, "$cheat_mode", 1),
					(str_store_troop_name, s4, ":cur_troop"),
					(display_message, "str_s4_is_present_at_the_center_and_not_attending_the_feast"),
				(try_end),				
			(else_try),
				(assign, ":lady_meets_visitors", 1),
				
				(try_begin),
					(eq, "$cheat_mode", 1),
					(str_store_troop_name, s4, ":cur_troop"),
					(display_message, "str_s4_is_present_at_the_center_and_is_married"),
				(try_end),				
			(try_end),
			
		(else_try), #feast is in progress			
			(faction_slot_eq, ":center_faction", slot_faction_ai_state, sfai_feast),
			(faction_slot_eq, ":center_faction", slot_faction_ai_object, ":center_no"),
			(assign, ":lady_meets_visitors", 1),
			
			(try_begin),
				(eq, "$cheat_mode", 1),
				(str_store_troop_name, s4, ":cur_troop"),
				(display_message, "@{!}DEBUG -- {s4} is present at the center and is attending the feast"),
			(try_end),
						
		(else_try), #already met - awaits in private
			(troop_slot_ge, ":cur_troop", slot_troop_met, 2),
			(assign, ":lady_meets_visitors", 0),
			
			(try_begin),
				(eq, "$cheat_mode", 1),
				(str_store_troop_name, s4, ":cur_troop"),
				(display_message, "@{!}DEBUG -- {s4} is present at the center and is awaiting the player in private"),
			(try_end),
			
		(else_try),	
			(call_script, "script_get_kingdom_lady_social_determinants", ":cur_troop"),
			(call_script, "script_npc_decision_checklist_male_guardian_assess_suitor", reg0, "trp_player"),
			(gt, reg0, 0),
			(assign, ":lady_meets_visitors", 1),
			
			(try_begin),
				(eq, "$cheat_mode", 1),
				(str_store_troop_name, s4, ":cur_troop"),
				(display_message, "@{!}DEBUG -- {s4} is_present_at_the_center_and_is_allowed_to_meet_the_player"),
			(try_end),
			
		(else_try),	
			(try_begin),
				(eq, "$cheat_mode", 1),
				(str_store_troop_name, s4, ":cur_troop"),
				(display_message, "@{!}DEBUG -- {s4}is_present_at_the_center_and_is_not_allowed_to_meet_the_player"),
			(try_end),
		
		(try_end),				

		(eq, ":lady_meets_visitors", 1),
		
        (lt, ":cur_pos", 32), # spawn up to entry point 32
        (set_visitor, ":cur_pos", ":cur_troop"),
        (val_add,":cur_pos", 1),
      (try_end),
      
      (set_jump_entry, 0),
      
      (jump_to_scene,":castle_scene"),
      (scene_set_slot, ":castle_scene", slot_scene_visited, 1),
      (change_screen_mission),
  ]),
   ("setup_meet_lady",
    [
      (store_script_param_1, ":lady_no"), 
      (store_script_param_2, ":center_no"), 
    
      #(mission_tpl_entry_set_override_flags, "mt_visit_town_castle", 0, af_override_horse),
      (troop_set_slot, ":lady_no", slot_lady_last_suitor, "trp_player"),
	  
      (set_jump_mission,"mt_visit_town_castle"),
      (party_get_slot, ":castle_scene", ":center_no", slot_town_castle),
      (modify_visitors_at_site,":castle_scene"),
      (reset_visitors),

	  (troop_set_age, "trp_nurse_for_lady", 100),
      (set_visitor, 7, "trp_nurse_for_lady"),

      (assign, ":cur_pos", 16),
	  (set_visitor, ":cur_pos", ":lady_no"),

      (assign, "$talk_context", tc_garden),
	  
      (jump_to_scene,":castle_scene"),
      (scene_set_slot, ":castle_scene", slot_scene_visited, 1),
      (change_screen_mission),	  
	]),
  # script_change_debt_to_troop
  # Input: arg1 = troop_no, arg2 = new debt amount
  # Output: none
  ("change_debt_to_troop",
    [
      (store_script_param_1, ":troop_no"),
      (store_script_param_2, ":new_debt"),
      
      (troop_get_slot, ":cur_debt", ":troop_no", slot_troop_player_debt),
      (assign, reg1, ":cur_debt"),
      (val_add, ":cur_debt", ":new_debt"),
      (assign, reg2, ":cur_debt"),
      (troop_set_slot, ":troop_no", slot_troop_player_debt, ":cur_debt"),
      (str_store_troop_name_link, s1, ":troop_no"),
      (display_message, "@You now owe {reg2} mon to {s1}."),
  ]),
  # script_map_get_random_position_around_position_within_range
  # Input: arg1 = minimum_distance in km, arg2 = maximum_distance in km, pos1 = origin position
  # Output: pos2 = result position
  ("map_get_random_position_around_position_within_range",
    [
      (store_script_param_1, ":min_distance"),
      (store_script_param_2, ":max_distance"),
      (val_mul, ":min_distance", 100),
      (assign, ":continue", 1),
      (try_for_range, ":unused", 0, 20),
        (eq, ":continue", 1),
        (map_get_random_position_around_position, pos2, pos1, ":max_distance"),
        (get_distance_between_positions, ":distance", pos2, pos1),
        (ge, ":distance", ":min_distance"),
        (assign, ":continue", 0),
      (try_end),
  ]),
  # script_get_number_of_unclaimed_centers_by_player
  # Input: none
  # Output: reg0 = number of unclaimed centers, reg1 = last unclaimed center_no
  ("get_number_of_unclaimed_centers_by_player",
    [
      (assign, ":unclaimed_centers", 0),
      (assign, reg1, -1),
      (try_for_range, ":center_no", centers_begin, centers_end),
        (store_faction_of_party, ":faction_no", ":center_no"),
        (eq, ":faction_no", "fac_player_supporters_faction"),
        (party_slot_eq, ":center_no", slot_town_claimed_by_player, 0),
        (party_get_num_companion_stacks, ":num_stacks", ":center_no"),
        (ge, ":num_stacks", 1), #castle is garrisoned
        (assign, reg1, ":center_no"),
        (val_add, ":unclaimed_centers", 1),
      (try_end),
      (assign, reg0, ":unclaimed_centers"),
  ]),
  # script_cf_troop_check_troop_is_enemy
  # Input: arg1 = troop_no, arg2 = checked_troop_no
  # Output: none (Can fail)
  ("cf_troop_check_troop_is_enemy",
    [
      (store_script_param_1, ":troop_no"),
      (store_script_param_2, ":checked_troop_no"),
	  (call_script, "script_troop_get_relation_with_troop", ":troop_no", ":checked_troop_no"),
	  (lt, reg0, -10),
 ]),
  # script_troop_get_leaded_center_with_index
  # Input: arg1 = troop_no, arg2 = center index within range between zero and the number of centers that troop owns
  # Output: reg0 = center_no
  ("troop_get_leaded_center_with_index",
    [
      (store_script_param_1, ":troop_no"),
      (store_script_param_2, ":random_center"),
      (assign, ":result", -1),
      (assign, ":center_count", 0),
      (try_for_range, ":center_no", centers_begin, centers_end),
        (eq, ":result", -1),
        (party_slot_eq, ":center_no", slot_town_lord, ":troop_no"),
        (val_add, ":center_count", 1),
        (gt, ":center_count", ":random_center"),
        (assign, ":result", ":center_no"),
      (try_end),
      (assign, reg0, ":result"),
  ]),
  # script_cf_troop_get_random_leaded_walled_center_with_less_strength_priority
  # Input: arg1 = troop_no, arg2 = preferred_center_no
  # Output: reg0 = center_no (Can fail)
  ("cf_troop_get_random_leaded_walled_center_with_less_strength_priority",
    [
      (store_script_param, ":troop_no", 1),
      (store_script_param, ":preferred_center_no", 2),

      (assign, ":num_centers", 0),
      (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
        (party_slot_eq, ":center_no", slot_town_lord, ":troop_no"),
        (party_slot_eq, ":center_no", slot_center_is_besieged_by, -1),
        (val_add, ":num_centers", 1),
        (try_begin),
          (eq, ":center_no", ":preferred_center_no"),
          (val_add, ":num_centers", 99),
        (try_end),
##        (call_script, "script_party_calculate_regular_strength", ":center_no"),
##        (assign, ":strength", reg0),
##        (lt, ":strength", 80),
##        (store_sub, ":strength", 100, ":strength"),
##        (val_div, ":strength", 20),
##        (val_add, ":num_centers", ":strength"),
      (try_end),
      (gt, ":num_centers", 0),
      (store_random_in_range, ":random_center", 0, ":num_centers"),
      (assign, ":result", -1),
      (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
        (eq, ":result", -1),
        (party_slot_eq, ":center_no", slot_town_lord, ":troop_no"),
        (party_slot_eq, ":center_no", slot_center_is_besieged_by, -1),
        (val_sub, ":random_center", 1),
        (try_begin),
          (eq, ":center_no", ":preferred_center_no"),
          (val_sub, ":random_center", 99),
        (try_end),
##        (try_begin),
##          (call_script, "script_party_calculate_regular_strength", ":center_no"),
##          (assign, ":strength", reg0),
##          (lt, ":strength", 80),
##          (store_sub, ":strength", 100, ":strength"),
##          (val_div, ":strength", 20),
##          (val_sub, ":random_center", ":strength"),
##        (try_end),
        (lt, ":random_center", 0),
        (assign, ":result", ":center_no"),
      (try_end),
      (assign, reg0, ":result"),
  ]),
  # script_cf_troop_get_random_leaded_town_or_village_except_center
  # Input: arg1 = troop_no, arg2 = except_center_no
  # Output: reg0 = center_no (Can fail)
  ("cf_troop_get_random_leaded_town_or_village_except_center",
    [
      (store_script_param_1, ":troop_no"),
      (store_script_param_2, ":except_center_no"),

      (assign, ":num_centers", 0),
      (try_for_range, ":center_no", centers_begin, centers_end),
        (neg|party_slot_eq, ":center_no", slot_party_type, spt_castle),
        (party_slot_eq, ":center_no", slot_town_lord, ":troop_no"),
        (neq, ":center_no", ":except_center_no"),
        (val_add, ":num_centers", 1),
      (try_end),

      (gt, ":num_centers", 0),
      (store_random_in_range, ":random_center", 0, ":num_centers"),
      (assign, ":end_cond", centers_end),
      (try_for_range, ":center_no", centers_begin, ":end_cond"),
        (neg|party_slot_eq, ":center_no", slot_party_type, spt_castle),
        (party_slot_eq, ":center_no", slot_town_lord, ":troop_no"),
        (neq, ":center_no", ":except_center_no"),
        (val_sub, ":random_center", 1),
        (lt, ":random_center", 0),
        (assign, ":target_center", ":center_no"),
        (assign, ":end_cond", 0),
      (try_end),
      (assign, reg0, ":target_center"),
  ]),
  # script_troop_write_owned_centers_to_s2
  # Input: arg1 = troop_no
  # Output: none
  ("troop_write_owned_centers_to_s2",
    [
      (store_script_param_1, ":troop_no"),
      
      (call_script, "script_get_number_of_hero_centers", ":troop_no"),
      (assign, ":no_centers", reg0),
      
      (str_store_troop_name, s5, ":troop_no"),
      
      (try_begin),
        (gt, ":no_centers", 1),
        (try_for_range, ":i_center", 1, ":no_centers"),
          (call_script, "script_troop_get_leaded_center_with_index", ":troop_no", ":i_center"),
          (str_store_party_name_link, s50, reg0),
          (try_begin),
            (eq, ":i_center", 1),
            (call_script, "script_troop_get_leaded_center_with_index", ":troop_no", 0),
            (str_store_party_name_link, s51, reg0),
            (str_store_string, s51, "str_s50_and_s51"),
          (else_try),
            (str_store_string, s51, "str_s50_comma_s51"),
          (try_end),
        (try_end),
        (str_store_string, s2, "str_s5_is_the_ruler_of_s51"),
      (else_try),
        (eq, ":no_centers", 1),
        (call_script, "script_troop_get_leaded_center_with_index", ":troop_no", 0),
        (str_store_party_name_link, s51, reg0),
        (str_store_string, s2, "str_s5_is_the_ruler_of_s51"),
      (else_try),
        (store_troop_faction, ":faction_no", ":troop_no"),
        (str_store_faction_name_link, s6, ":faction_no"),
        ##diplomacy start+ make gender-correct
		#(troop_get_type, reg4, ":troop_no"),
        (assign, ":save_reg4", reg4),
      (call_script, "script_dplmc_store_troop_is_female_reg", ":troop_no", 4),
        (str_store_string, s2, "str_s5_is_a_nobleman_of_s6"),
        (assign, reg4, ":save_reg4"),
        ##diplomacy end+
      (try_end),
  ]),
  ("troop_write_family_relations_to_s1", 
    [
	(str_clear, s1),
	#redo, possibly using base from update_troop_notes
	
]),
  ("troop_get_family_relation_to_troop", 
    [
    (store_script_param_1, ":troop_1"),
    (store_script_param_2, ":troop_2"),

    ##diplomacy start+ use gender script
    #(troop_get_type, ":gender_1", ":troop_1"),
	(call_script, "script_dplmc_store_troop_is_female", ":troop_1"),
	(assign, ":gender_1", reg0),
	##diplomacy end+
	(assign, ":relation_strength", 0),
	
    (troop_get_slot, ":spouse_of_1", ":troop_1", slot_troop_spouse),
    (troop_get_slot, ":spouse_of_2", ":troop_2", slot_troop_spouse),
	
	(try_begin),
		(gt, ":spouse_of_1", -1),
		(troop_get_slot, ":father_of_spouse_of_1", ":spouse_of_1", slot_troop_father),
	(else_try),
		(assign, ":father_of_spouse_of_1", -1),
	(try_end),
	
	(try_begin),
		(gt, ":spouse_of_2", -1),
		(troop_get_slot, ":father_of_spouse_of_2", ":spouse_of_2", slot_troop_father),
	(else_try),
		(assign, ":father_of_spouse_of_2", -1),
	(try_end),

	(try_begin),
		(gt, ":spouse_of_2", -1),
		(troop_get_slot, ":mother_of_spouse_of_2", ":spouse_of_2", slot_troop_mother),
	(else_try),
		(assign, ":mother_of_spouse_of_2", -1),
	(try_end),
	
    (troop_get_slot, ":father_of_1", ":troop_1", slot_troop_father),
    (troop_get_slot, ":father_of_2", ":troop_2", slot_troop_father),

	#For the sake of simplicity, we can assume that all male aristocrats in prior generations either married commoners or procured their brides from the Old Country, thus discounting intermarriage 
    (troop_get_slot, ":mother_of_1", ":troop_1", slot_troop_mother),
    (troop_get_slot, ":mother_of_2", ":troop_2", slot_troop_mother),

    ##diplomacy start+
	#Fix a native bug where daughters are their own mothers
        #(fixed in this mod, but still affects old saved games)
        #REMOVED - Instead this occurs once in simple triggers

	##Adding paternal grandmother (begin mostly-unaltered section)
	(try_begin),
		(this_or_next|eq, ":father_of_1", "trp_player"),#dplmc+ added
		(is_between, ":father_of_1", companions_begin, kingdom_ladies_end),
		(troop_get_slot, ":paternal_grandfather_of_1", ":father_of_1", slot_troop_father),
		(troop_get_slot, ":paternal_grandmother_of_1", ":father_of_1", slot_troop_mother),#added
	(else_try),
		(assign, ":paternal_grandfather_of_1", -1),
		(assign, ":paternal_grandmother_of_1", -1),#added
	(try_end),

	(try_begin),
		(this_or_next|eq, ":father_of_2", "trp_player"),#dplmc+ added
		(is_between, ":father_of_2", companions_begin, kingdom_ladies_end),
		(troop_get_slot, ":paternal_grandfather_of_2", ":father_of_2", slot_troop_father),
		(troop_get_slot, ":paternal_grandmother_of_2", ":father_of_2", slot_troop_mother),#added
	(else_try),
		(assign, ":paternal_grandfather_of_2", -1),
		(assign, ":paternal_grandmother_of_2", -1),#added
	(try_end),
	#(end mostly-unaltered section)

	##Adding maternal grandfather and maternal grandmother
	(try_begin),
		(this_or_next|eq, ":mother_of_1", "trp_player"),#dplmc+ added
		(is_between, ":mother_of_1", companions_begin, kingdom_ladies_end),
		(troop_get_slot, ":maternal_grandfather_of_1", ":mother_of_1", slot_troop_father),
		(troop_get_slot, ":maternal_grandmother_of_1", ":mother_of_1", slot_troop_mother),
	(else_try),
		(assign, ":maternal_grandfather_of_1", -1),
		(assign, ":maternal_grandmother_of_1", -1),
	(try_end),

	(try_begin),
		(this_or_next|eq, ":mother_of_2", "trp_player"),#dplmc+ added
		(is_between, ":mother_of_2", companions_begin, kingdom_ladies_end),
		(troop_get_slot, ":maternal_grandfather_of_2", ":mother_of_2", slot_troop_father),
		(troop_get_slot, ":maternal_grandmother_of_2", ":mother_of_2", slot_troop_mother),
	(else_try),
		(assign, ":maternal_grandfather_of_2", -1),
		(assign, ":maternal_grandmother_of_2", -1),
	(try_end),
	##diplomacy end+
		
    (troop_get_slot, ":guardian_of_1", ":troop_1", slot_troop_guardian),
    (troop_get_slot, ":guardian_of_2", ":troop_2", slot_troop_guardian),

	(str_store_string, s11, "str_no_relation"),
	
	(try_begin),
	  (eq, ":troop_1", ":troop_2"),
	  #self
	(else_try),
	  ##diplomacy start+
      (this_or_next|eq, ":spouse_of_2", ":troop_1"),#polygamy helper
	  ##diplomacy end+
	  (eq, ":spouse_of_1", ":troop_2"),
	  (assign, ":relation_strength", 20),
	  (try_begin),
	    (eq, ":gender_1", 1),
	    (str_store_string, s11, "str_wife"),
	  (else_try),
	    (str_store_string, s11, "str_husband"),
	  (try_end),
	(else_try),
	  (eq, ":father_of_2", ":troop_1"),
	  (assign, ":relation_strength", 15),
	  (str_store_string, s11, "str_father"),
	(else_try),
	  (eq, ":mother_of_2", ":troop_1"),
	  (assign, ":relation_strength", 15),
	  (str_store_string, s11, "str_mother"),
	(else_try),
	  (this_or_next|eq, ":father_of_1", ":troop_2"),
	  (eq, ":mother_of_1", ":troop_2"),
	  (assign, ":relation_strength", 15),	  
	  (try_begin),
	    (eq, ":gender_1", 1),
	    (str_store_string, s11, "str_daughter"),
	  (else_try),
	    (str_store_string, s11, "str_son"),
	  (try_end),
	##diplomacy start+
	(else_try),
	   #Check for half-siblings: sharing a father
	   (neq, ":father_of_1", -1),
	   (eq, ":father_of_1", ":father_of_2"),
	   (neq, ":mother_of_1", ":mother_of_2"),
	   (assign, ":relation_strength", 10),
	   (try_begin),
	     (eq, ":gender_1", 1),
	     (str_store_string, s11, "str_dplmc_half_sister"),
	   (else_try),
	     (str_store_string, s11, "str_dplmc_half_brother"),
	   (try_end),
   (else_try),
	   #Check for half-siblings: sharing a mother
	   (neq, ":mother_of_1", -1),
	   (eq, ":mother_of_1", ":mother_of_2"),
	   (neq, ":father_of_1", ":father_of_2"),
	   (assign, ":relation_strength", 10),
	   (try_begin),
	     (eq, ":gender_1", 1),
	     (str_store_string, s11, "str_dplmc_half_sister"),
	   (else_try),
	     (str_store_string, s11, "str_dplmc_half_brother"),
	   (try_end),
	(else_try),
	  #(gt, ":father_of_1", -1), #necessary, as some lords do not have the father registered #dplmc+ replaced
	  (neq, ":father_of_1", -1), #dplmc+ added
	##diplomacy end+
	  (eq, ":father_of_1", ":father_of_2"),
	  (assign, ":relation_strength", 10),
	  (try_begin),
	    (eq, ":gender_1", 1),
	    (str_store_string, s11, "str_sister"),
	  (else_try),	
	    (str_store_string, s11, "str_brother"),
	  (try_end),
	(else_try),
	  (eq, ":guardian_of_2", ":troop_1"),
	  (assign, ":relation_strength", 10),
	  (try_begin),
	    (eq, ":gender_1", 1),
	    (str_store_string, s11, "str_sister"),
	  (else_try),	
	    (str_store_string, s11, "str_brother"),
	  (try_end),
	(else_try),
	  (eq, ":guardian_of_1", ":troop_2"),
	  (assign, ":relation_strength", 10),
	  (try_begin),
	    (eq, ":gender_1", 1),
	    (str_store_string, s11, "str_sister"),
	  (else_try),	
	    (str_store_string, s11, "str_brother"),
	  (try_end),		
	##diplomacy start+
    (else_try),#polygamy, between two people married to the same person
	   (neq, ":spouse_of_1", -1),
	   (eq, ":spouse_of_2", ":spouse_of_1"),
	   (assign, ":relation_strength", 10),
	   (try_begin),
	      (eq, ":gender_1", 1),
	      (str_store_string, s11, "str_dplmc_sister_wife"),
	   (else_try),
	      (str_store_string, s11, "str_dplmc_co_husband"),
	   (try_end),
	##diplomacy end+
	(else_try),
	  #(gt, ":paternal_grandfather_of_1", -1),#dplmc+ replaced
	  (neq, ":father_of_2", -1),#dplmc+ added
	  (this_or_next|eq, ":maternal_grandfather_of_1", ":father_of_2"),#dplmc+ added
	  (eq, ":paternal_grandfather_of_1", ":father_of_2"),
	  (assign, ":relation_strength", 4),
	  (try_begin),
	    (eq, ":gender_1", 1),
	    (str_store_string, s11, "str_niece"),
	  (else_try),
	    (str_store_string, s11, "str_nephew"),
	  (try_end),		
	##diplomacy start+: add niece/nephew through mother
	(else_try),
	  (neq, ":mother_of_2", -1),
  	  (this_or_next|eq, ":maternal_grandmother_of_1", ":mother_of_2"),
	  (eq, ":paternal_grandmother_of_1", ":mother_of_2"),
	  (assign, ":relation_strength", 4),
	  (try_begin),
	    (eq, ":gender_1", tf_female),
	    (str_store_string, s11, "str_niece"),
	  (else_try),
	    (str_store_string, s11, "str_nephew"),
	  (try_end),
	##diplomacy end+
	(else_try), #specifically aunt and uncle by blood -- i assume that in a medieval society with lots of internal family conflicts, they would not include aunts and uncles by marriage
	  #(gt, ":paternal_grandfather_of_2", -1),#dplmc+ replaced
	  (neq, ":father_of_1", -1),#dplmc+ added
	  (this_or_next|eq, ":maternal_grandfather_of_2", ":father_of_1"),#dplmc+ added
	  (eq, ":paternal_grandfather_of_2", ":father_of_1"),	  
	  (assign, ":relation_strength", 4),	  
	  (try_begin),
	    (eq, ":gender_1", 1),
	    (str_store_string, s11, "str_aunt"),
	  (else_try),	
	    (str_store_string, s11, "str_uncle"),
	  (try_end),	
	##diplomacy start+
	#blood uncles & blood aunts, continued (via mother)
	(else_try),
	  (neq, ":mother_of_1", -1),
	  (this_or_next|eq, ":maternal_grandmother_of_2", ":mother_of_1"),
	  (eq, ":paternal_grandmother_of_2", ":mother_of_1"),
	  (assign, ":relation_strength", 4),
	  (try_begin),
	    (eq, ":gender_1", tf_female),
	    (str_store_string, s11, "str_aunt"),
	  (else_try),
	    (str_store_string, s11, "str_uncle"),
	  (try_end),
	##diplomacy end+
	(else_try),
	  #(gt, ":paternal_grandfather_of_1", 0),#dplmc+ replaced (why was this one "gt 0" but the previous "gt -1"?)
	  (neq, ":paternal_grandfather_of_1", -1),#dplmc+ added
	  (this_or_next|eq, ":maternal_grandfather_of_2", ":paternal_grandfather_of_1"),#dplmc+ added
	  (eq, ":paternal_grandfather_of_2", ":paternal_grandfather_of_1"),
	  (assign, ":relation_strength", 2),
	  (str_store_string, s11, "str_cousin"),
	##diplomacy start+
	#Add cousin via paternal grandmother or maternal grandparents
	(else_try),
	  (neq, ":maternal_grandfather_of_1", -1),
	  (this_or_next|eq, ":maternal_grandfather_of_2", ":maternal_grandfather_of_1"),
	  (eq, ":paternal_grandfather_of_2", ":maternal_grandfather_of_1"),
	  (assign, ":relation_strength", 2),
	  (str_store_string, s11, "str_cousin"),
	(else_try),
	  (neq, ":paternal_grandmother_of_1", -1),
	  (this_or_next|eq, ":maternal_grandmother_of_2", ":paternal_grandmother_of_1"),
	  (eq, ":paternal_grandmother_of_2", ":paternal_grandmother_of_1"),
	  (assign, ":relation_strength", 2),
	  (str_store_string, s11, "str_cousin"),
	(else_try),
	  (neq, ":maternal_grandmother_of_1", -1),
	  (this_or_next|eq, ":maternal_grandmother_of_2", ":maternal_grandmother_of_1"),
	  (eq, ":paternal_grandmother_of_2", ":maternal_grandmother_of_1"),
	  (assign, ":relation_strength", 2),
	  (str_store_string, s11, "str_cousin"),
	##diplomacy end+
   	(else_try),
   	  (eq, ":father_of_spouse_of_1", ":troop_2"),
   	  (assign, ":relation_strength", 5),
   	  (try_begin),
   	    (eq, ":gender_1", 1),
   	    (str_store_string, s11, "str_daughterinlaw"),
   	  (else_try),	
   	    (str_store_string, s11, "str_soninlaw"),
   	  (try_end),
	(else_try),
	  (eq, ":father_of_spouse_of_2", ":troop_1"),
	  (assign, ":relation_strength", 5),
	  (str_store_string, s11, "str_fatherinlaw"),
	(else_try),  
	  (eq, ":mother_of_spouse_of_2", ":troop_1"),
	  (neq, ":mother_of_spouse_of_2", "trp_player"), #May be necessary if mother for troops not set to -1
	  (assign, ":relation_strength", 5),
	  (str_store_string, s11, "str_motherinlaw"),

	(else_try),
	  #(gt, ":father_of_spouse_of_1", -1), #necessary #dplmc+ replaced
	  (neq, ":father_of_spouse_of_1", -1), #dplmc+ added
	  (eq, ":father_of_spouse_of_1", ":father_of_2"),
	  (assign, ":relation_strength", 5),
	  (try_begin),
	    (eq, ":gender_1", 1),
	    (str_store_string, s11, "str_sisterinlaw"),
	  (else_try),	
	    (str_store_string, s11, "str_brotherinlaw"),	       
	  (try_end), 
	(else_try),
	  #(gt, ":father_of_spouse_of_2", -1), #necessary #dplmc+ replaced
	  (neq, ":father_of_spouse_of_2", -1), #dplmc+ added
	  (eq, ":father_of_spouse_of_2", ":father_of_1"),
	  (assign, ":relation_strength", 5),
	  (try_begin),
	    (eq, ":gender_1", 1),
	    (str_store_string, s11, "str_sisterinlaw"),
	  (else_try),
	    (str_store_string, s11, "str_brotherinlaw"),
	  (try_end),
	(else_try),
	  #(gt, ":spouse_of_2", -1), #necessary to avoid bug #dplmc+ replaced
	  (neq, ":spouse_of_2", -1), #dplmc+ added
	  (troop_slot_eq, ":spouse_of_2", slot_troop_guardian, ":troop_1"),
	  (assign, ":relation_strength", 5),
	  (try_begin),
	    #(eq, ":gender_1", 1),#dplmc+ replaced
	    (eq, ":gender_1", tf_female),#dplmc+ added
	    (str_store_string, s11, "str_sisterinlaw"),
	  (else_try),	
	    (str_store_string, s11, "str_brotherinlaw"),
	  (try_end),
	(else_try),
	  #(gt, ":spouse_of_1", -1), #necessary to avoid bug #dplmc+ replaced
	  (neq, ":spouse_of_1", -1), #dplmc+ added
	  (troop_slot_eq, ":spouse_of_1", slot_troop_guardian, ":troop_2"),
	  (assign, ":relation_strength", 5),
	  (try_begin),
	    (eq, ":gender_1", 1),
	    (str_store_string, s11, "str_sisterinlaw"),
	  (else_try),	
	    (str_store_string, s11, "str_brotherinlaw"),
	  (try_end),		
	(else_try),
	  #grandchild
	  (neq, ":troop_2", -1),
	   (this_or_next|eq, ":paternal_grandfather_of_1", ":troop_2"),
	   (this_or_next|eq, ":maternal_grandfather_of_1", ":troop_2"),
	   (this_or_next|eq, ":paternal_grandmother_of_1", ":troop_2"),
		   (eq, ":maternal_grandmother_of_1", ":troop_2"),
	   (assign, ":relation_strength", 4),
	  (try_begin),
	    (eq, ":gender_1", tf_female),
	    (str_store_string, s11, "str_dplmc_granddaughter"),
	  (else_try),
	    (str_store_string, s11, "str_dplmc_grandson"),
	  (try_end),
	(else_try),
	   #grandparent
	   (neq, ":troop_1", -1),
	   (this_or_next|eq, ":paternal_grandfather_of_2", ":troop_1"),
	   (this_or_next|eq, ":maternal_grandfather_of_2", ":troop_1"),
	   (this_or_next|eq, ":paternal_grandmother_of_2", ":troop_1"),
		   (eq, ":maternal_grandmother_of_2", ":troop_1"),
	  (assign, ":relation_strength", 4),
	  (try_begin),
	    (eq, ":gender_1", tf_female),
	    (str_store_string, s11, "str_dplmc_grandmother"),
	  (else_try),
	    (str_store_string, s11, "str_dplmc_grandfather"),
	  (try_end),
	(try_end),
	
	##diplomacy start+
	##Add uncles and aunts by marriage.
	##In Native, the relation strength for blood uncles/aunts is 4, and for cousins is 2.
	##In light of this I've decided to set the relation strength for aunts/uncles by marriage to 2.
	(try_begin),
		(lt, ":relation_strength", 2),#Skip this check if a stronger relation has been found.
		#Test if troop_1 is married to a sibling of one of troop_2's parents, pt. 1
		(ge, ":spouse_of_1", 0),
		(neg|troop_slot_eq, ":spouse_of_1", slot_troop_father, -1),
		(this_or_next|troop_slot_eq, ":spouse_of_1", slot_troop_father, ":paternal_grandfather_of_2"),
			(troop_slot_eq, ":spouse_of_1", slot_troop_father, ":maternal_grandfather_of_2"),
		(assign, ":relation_strength", 2),
		(try_begin),
			(eq, ":gender_1", tf_female),
			(str_store_string, s11, "str_aunt"),
		(else_try),
			(str_store_string, s11, "str_uncle"),
		(try_end),
	(else_try),
		(lt, ":relation_strength", 2),#Skip this check if a stronger relation has been found.
		#Test if troop_1 is married to a sibling of one of troop_2's parents, pt. 2
		(ge, ":spouse_of_1", 0),
		(neg|troop_slot_eq, ":spouse_of_1", slot_troop_mother, -1),
		(this_or_next|troop_slot_eq, ":spouse_of_1", slot_troop_mother, ":paternal_grandmother_of_2"),
			(troop_slot_eq, ":spouse_of_1", slot_troop_mother, ":maternal_grandmother_of_2"),
		(assign, ":relation_strength", 2),
		(try_begin),
			(eq, ":gender_1", tf_female),
			(str_store_string, s11, "str_aunt"),
		(else_try),
			(str_store_string, s11, "str_uncle"),
		(try_end),
	(else_try),
		(lt, ":relation_strength", 2),#Skip this check if a stronger relation has been found.
		#Test if troop_2 is married to a sibling of one of troop_1's parents, pt. 1
		(ge, ":spouse_of_2", 0),
		(neg|troop_slot_eq, ":spouse_of_2", slot_troop_father, -1),
		(this_or_next|troop_slot_eq, ":spouse_of_2", slot_troop_father, ":paternal_grandfather_of_1"),
			(troop_slot_eq, ":spouse_of_2", slot_troop_father, ":maternal_grandfather_of_1"),
		(assign, ":relation_strength", 2),
		(try_begin),
			(eq, ":gender_1", tf_female),
			(str_store_string, s11, "str_niece"),
		(else_try),
			(str_store_string, s11, "str_nephew"),
		(try_end),
	(else_try),
		(lt, ":relation_strength", 2),#Skip this check if a stronger relation has been found.
		#Test if troop_2 is married to a sibling of one of troop_1's parents, pt. 2
		(ge, ":spouse_of_2", 0),
		(neg|troop_slot_eq, ":spouse_of_2", slot_troop_mother, -1),
		(this_or_next|troop_slot_eq, ":spouse_of_2", slot_troop_mother, ":paternal_grandmother_of_1"),
			(troop_slot_eq, ":spouse_of_2", slot_troop_mother, ":maternal_grandmother_of_1"),
		(assign, ":relation_strength", 2),
		(try_begin),
			(eq, ":gender_1", tf_female),
			(str_store_string, s11, "str_niece"),
		(else_try),
			(str_store_string, s11, "str_nephew"),
		(try_end),
	(try_end),
	##diplomacy end+
    (assign, reg4, ":gender_1"),
	(assign, reg0, ":relation_strength"),
	]),
  # script_collect_friendly_parties
  # Fills the party p_collective_friends with the members of parties attached to main_party and ally_party_no
  ("collect_friendly_parties",
    [
      (party_collect_attachments_to_party, "p_main_party", "p_collective_friends"),
      (try_begin),
        (gt, "$g_ally_party", 0),
        (party_collect_attachments_to_party, "$g_ally_party", "p_temp_party"),
        (assign, "$g_move_heroes", 1),
        (call_script, "script_party_add_party", "p_collective_friends", "p_temp_party"),
      (try_end),
  ]),
  # script_calculate_renown_value
  # Input: arg1 = troop_no
  # Output: fills $battle_renown_value
  ("calculate_renown_value",
   [
      ##diplomacy start+
	  #If terrain advantage is enabled, use it to avoid messing up cached
	  #strength values, but do not take it into consideration for renown
	  #granted.
	  (assign, ":main_party_strength", 1),
	  (assign, ":enemy_strength", 1),
	  (assign, ":friends_strength", 1),
	  (assign, ":terrain_code", -1),
	  (try_begin),
	     (eq, "$g_dplmc_terrain_advantage", DPLMC_TERRAIN_ADVANTAGE_ENABLE),
	     (try_begin),
	        (encountered_party_is_attacker),
		    (call_script, "script_dplmc_get_terrain_code_for_battle", "$g_encountered_party", "p_main_party"),
	     (else_try),
	        (call_script, "script_dplmc_get_terrain_code_for_battle", "p_main_party", "$g_encountered_party"),
		 (try_end),
		 (assign, ":terrain_code", reg0),
		 ##Alternate option: calculate with terrain, but don't use it for renown
		 #(but do use it to update the cached strength for the party)
		 (call_script, "script_dplmc_party_calculate_strength_in_terrain", "p_main_party", ":terrain_code",0,1),
		 (assign, ":main_party_strength", reg1),#use non-terrain version!
		 (call_script, "script_dplmc_party_calculate_strength_in_terrain", "p_collective_enemy", ":terrain_code",0,1),
		 (assign, ":enemy_strength", reg1),#use non-terrain version!
		 (call_script, "script_dplmc_party_calculate_strength_in_terrain", "p_collective_friends", ":terrain_code",0,1),
		 (assign, ":friends_strength", reg1),#use non-terrain version!
	  (else_try),
	      ##Original option: calculate without terrain
		  (call_script, "script_party_calculate_strength", "p_main_party", 0),
		  (assign, ":main_party_strength", reg0),
		  (call_script, "script_party_calculate_strength", "p_collective_enemy", 0),
		  (assign, ":enemy_strength", reg0),
		  (call_script, "script_party_calculate_strength", "p_collective_friends", 0),
		  (assign, ":friends_strength", reg0),
	  (try_end),
	  ##diplomacy end+

      (val_add, ":friends_strength", 1),
      (store_mul, ":enemy_strength_ratio", ":enemy_strength", 100),
      (val_div, ":enemy_strength_ratio", ":friends_strength"),

      (assign, ":renown_val", ":enemy_strength"),
      (val_mul, ":renown_val", ":enemy_strength_ratio"),
      (val_div, ":renown_val", 100),

      (val_mul, ":renown_val", ":main_party_strength"),
      (val_div, ":renown_val",":friends_strength"),

      (store_div, "$battle_renown_value", ":renown_val", 5),
      (val_min, "$battle_renown_value", 2500),
      (convert_to_fixed_point, "$battle_renown_value"),
      (store_sqrt, "$battle_renown_value", "$battle_renown_value"),
      (convert_from_fixed_point, "$battle_renown_value"),
      (assign, reg8, "$battle_renown_value"),
      (display_message, "@Renown value for this battle is {reg8}.",0xFFFFFFFF),
  ]),
  # script_change_banners_and_chest
  # Input: none
  # Output: none
  ("change_banners_and_chest",
    [(party_get_slot, ":cur_leader", "$g_encountered_party", slot_town_lord),
     (try_begin),
       (ge, ":cur_leader", 0),
#normal_banner_begin
       (troop_get_slot, ":troop_banner_object", ":cur_leader", slot_troop_banner_scene_prop),
       (gt, ":troop_banner_object", 0),
       (replace_scene_props, banner_scene_props_begin, ":troop_banner_object"),
     (else_try),
       (replace_scene_props, banner_scene_props_begin, "spr_empty"),
#custom_banner_begin
#       (troop_get_slot, ":flag_spr", ":cur_leader", slot_troop_custom_banner_flag_type),
#       (ge, ":flag_spr", 0),
#       (val_add, ":flag_spr", custom_banner_flag_scene_props_begin),
#       (replace_scene_props, banner_scene_props_begin, ":flag_spr"),
#     (else_try),
#       (replace_scene_props, banner_scene_props_begin, "spr_empty"),
     (try_end),
     (try_begin),
       (neq, ":cur_leader", "trp_player"),
       (replace_scene_props, "spr_player_chest", "spr_locked_player_chest"),
     (try_end),
     ]),
  # script_remove_siege_objects
  # Input: none
  # Output: none
  ("remove_siege_objects",
    [
      (replace_scene_props, "spr_battlement_a_destroyed", "spr_battlement_a"),
      (replace_scene_props, "spr_snowy_castle_battlement_a_destroyed", "spr_snowy_castle_battlement_a"),
      (replace_scene_props, "spr_castle_e_battlement_a_destroyed", "spr_castle_e_battlement_a"),
      (replace_scene_props, "spr_castle_battlement_a_destroyed", "spr_castle_battlement_a"),
      (replace_scene_props, "spr_castle_battlement_b_destroyed", "spr_castle_battlement_b"),
      (replace_scene_props, "spr_earth_wall_a2", "spr_earth_wall_a"),
      (replace_scene_props, "spr_earth_wall_b2", "spr_earth_wall_b"),
      (replace_scene_props, "spr_belfry_platform_b", "spr_empty"),
      (replace_scene_props, "spr_belfry_platform_a", "spr_empty"),
      (replace_scene_props, "spr_belfry_a", "spr_empty"),
      (replace_scene_props, "spr_belfry_wheel", "spr_empty"),
      (replace_scene_props, "spr_siege_ladder_move_6m", "spr_empty"),
      (replace_scene_props, "spr_siege_ladder_move_8m", "spr_empty"),
      (replace_scene_props, "spr_siege_ladder_move_10m", "spr_empty"),
      (replace_scene_props, "spr_siege_ladder_move_12m", "spr_empty"),
      (replace_scene_props, "spr_siege_ladder_move_14m", "spr_empty"),
      (replace_scene_props, "spr_siege_ladder_12m", "spr_empty"),
      (replace_scene_props, "spr_siege_ladder_14m", "spr_empty"),
      (replace_scene_props, "spr_mangonel", "spr_empty"),
      (replace_scene_props, "spr_trebuchet_old", "spr_empty"),
      (replace_scene_props, "spr_trebuchet_new", "spr_empty"),
      (replace_scene_props, "spr_stone_ball", "spr_empty"),
      (replace_scene_props, "spr_Village_fire_big", "spr_empty"),
      ]),
  # script_describe_relation_to_s63
  # Input: arg1 = relation (-100 .. 100)
  # Output: none
  ("describe_relation_to_s63",
    [(store_script_param_1, ":relation"),
      (store_add, ":normalized_relation", ":relation", 100),
      (val_add, ":normalized_relation", 5),
      (store_div, ":str_offset", ":normalized_relation", 10),
      (val_clamp, ":str_offset", 0, 20),
      (store_add, ":str_id", "str_relation_mnus_100",  ":str_offset"),
      (str_store_string, s63, ":str_id"),
  ]),
  # script_describe_center_relation_to_s3
  # Input: arg1 = relation (-100 .. 100)
  # Output: none
  ("describe_center_relation_to_s3",
    [(store_script_param_1, ":relation"),
      (store_add, ":normalized_relation", ":relation", 100),
      (val_add, ":normalized_relation", 5),
      (store_div, ":str_offset", ":normalized_relation", 10),
      (val_clamp, ":str_offset", 0, 20),
      (store_add, ":str_id", "str_center_relation_mnus_100",  ":str_offset"),
      (str_store_string, s3, ":str_id"),
  ]),
  # script_calculate_troop_score_for_center
  # Input: arg1 = troop_no, arg2 = center_no
  # Output: reg0 = score
  ("calculate_troop_score_for_center",
   [(store_script_param, ":troop_no", 1),
    (store_script_param, ":center_no", 2),
    (assign, ":num_center_points", 1),
    (try_for_range, ":cur_center", centers_begin, centers_end),
      (assign, ":center_owned", 0),
      (try_begin),
        (eq, ":troop_no", "trp_player"),
        (party_slot_eq, ":cur_center", slot_town_lord, stl_reserved_for_player),
        (assign, ":center_owned", 1),
      (try_end),
      (this_or_next|party_slot_eq, ":cur_center", slot_town_lord, ":troop_no"),
		(eq, ":center_owned", 1),
      (try_begin),
        (party_slot_eq, ":cur_center", slot_party_type, spt_town),
        (val_add, ":num_center_points", 4),
      (else_try),
        (party_slot_eq, ":cur_center", slot_party_type, spt_castle),
        (val_add, ":num_center_points", 2),
      (else_try),
        (val_add, ":num_center_points", 1),
      (try_end),
    (try_end),
    (troop_get_slot, ":troop_renown", ":troop_no", slot_troop_renown),
    (store_add, ":score", 500, ":troop_renown"),
    (val_div, ":score", ":num_center_points"),
    (store_random_in_range, ":random", 50, 100),
    (val_mul, ":score", ":random"),
    (try_begin),
      (party_slot_eq, ":center_no", slot_center_last_taken_by_troop, ":troop_no"),
      (val_mul, ":score", 3),
      (val_div, ":score", 2),
  	##diplomacy start+
	#Take into account original/most-recent lord and home slots.
	#Fief allocations during rebellions are an example of when this would apply.
	(else_try),
	#Bonus for original owner
 		(ge, "$g_dplmc_ai_changes", DPLMC_AI_CHANGES_LOW),
		(party_slot_ge, ":center_no", dplmc_slot_center_original_lord, 1),
		(party_slot_eq, ":center_no", dplmc_slot_center_original_lord, ":troop_no"),
		(val_mul, ":score", 3),
		(val_div, ":score", 2),
	(else_try),
	#Bonus for previous owner
 		(ge, "$g_dplmc_ai_changes", DPLMC_AI_CHANGES_LOW),
		(party_slot_ge, ":center_no", dplmc_slot_center_ex_lord, 1),
		(party_slot_eq, ":center_no", dplmc_slot_center_ex_lord, ":troop_no"),
		(val_mul, ":score", 3),
		(val_div, ":score", 2),
	(else_try),
	#Bonus for lord claiming the center as home
 		(ge, "$g_dplmc_ai_changes", DPLMC_AI_CHANGES_LOW),
		(troop_slot_eq, ":troop_no", slot_troop_home, ":center_no"),
		(val_mul, ":score", 3),
		(val_div, ":score", 2),
	##diplomacy end+
    (try_end),
    (try_begin),
      (eq, ":troop_no", "trp_player"),
       ##diplomacy start+ xxx Replaced next line (slot 0 is not the faction leader slot):
      #(faction_get_slot, ":faction_leader", "$players_kingdom"),
      (faction_get_slot, ":faction_leader", "$players_kingdom", slot_faction_leader),
      ##diplomacy end+
      (call_script, "script_troop_get_player_relation", ":faction_leader"),
      (assign, ":leader_relation", reg0),
      #(troop_get_slot, ":leader_relation", ":faction_leader", slot_troop_player_relation),
      (val_mul, ":leader_relation", 2),
      (val_add, ":score", ":leader_relation"),
    (try_end),
    (assign, reg0, ":score"),
    ]),
  # script_assign_lords_to_empty_centers
  # Input: none
  # Output: none
  #Now ONLY called from the start
  ("assign_lords_to_empty_centers",
   [
   
    (try_begin),
		(eq, "$cheat_mode", 1),		
		(display_message, "str_assigning_lords_to_empty_centers"),
		(str_store_string, s65, "str_assign_lords_to_empty_centers_just_happened"),
		(call_script, "script_add_notification_menu", "mnu_debug_alert_from_s65", 0, 0),
    (try_end),
   
	(try_for_range, ":faction", kingdoms_begin, kingdoms_end),
		(faction_set_slot, ":faction", slot_faction_temp_slot, 0),
    (try_end),

	(try_for_range, ":active_npc", 0, active_npcs_end),
		(troop_set_slot, ":active_npc", slot_troop_temp_slot, 0),
    (try_end),
   
    #Factions will keep one unassigned center in reserve, unless they have landless lords
    (try_for_range, ":cur_center", centers_begin, centers_end),
	    (party_get_slot, ":center_lord", ":cur_center", slot_town_lord),
		(try_begin),
			(this_or_next|eq, ":center_lord", stl_unassigned),
				(eq, ":center_lord", stl_rejected_by_player),
			(store_faction_of_party, ":center_faction", ":cur_center"),
			
			(try_begin),
				(eq, "$cheat_mode", 1),
				(str_store_party_name, s4, ":cur_center"),
				(str_store_faction_name, s5, ":center_faction"),
				(display_message, "str_s4_of_the_s5_is_unassigned"),
			(try_end),
		
			(faction_get_slot, ":number_of_unassigned_centers_plus_landless_lords", ":center_faction", slot_faction_temp_slot),
			(val_add, ":number_of_unassigned_centers_plus_landless_lords", 1),
			(faction_set_slot,  ":center_faction", slot_faction_temp_slot, ":number_of_unassigned_centers_plus_landless_lords"),
		(else_try),
			(eq, ":center_lord", stl_reserved_for_player),

			(try_begin),
				(eq, "$cheat_mode", 1),
				(str_store_party_name, s4, ":cur_center"),
				(str_store_faction_name, s5, ":center_faction"),
				(display_message, "str_s4_of_the_s5_is_reserved_for_player"),
			(try_end),
			
		(else_try),
			(ge, ":center_lord", 0),
			(troop_set_slot, ":center_lord", slot_troop_temp_slot, 1),
		(try_end),	
	(try_end),
   
	(try_for_range, ":active_npc", 0, active_npcs_end),
		(troop_slot_eq, ":active_npc", slot_troop_occupation, slto_kingdom_hero),
		(this_or_next|gt, ":active_npc", "trp_player"),
			(eq, "$player_has_homage", 1),
			
		(troop_slot_eq, ":active_npc", slot_troop_temp_slot, 0),
		(store_faction_of_troop, ":npc_faction", ":active_npc"),

		(is_between, ":npc_faction", npc_kingdoms_begin, npc_kingdoms_end),
	
		(try_begin),
			(eq, "$cheat_mode", 1),
			(str_store_troop_name, s4, ":active_npc"),
			(str_store_faction_name, s5, ":npc_faction"),
			(display_message, "str_s4_of_the_s5_has_no_fiefs"),
		(try_end),
	
		(faction_get_slot, ":number_of_unassigned_centers_plus_landless_lords", ":npc_faction", slot_faction_temp_slot),
		(val_add, ":number_of_unassigned_centers_plus_landless_lords", 1),
		(faction_set_slot,  ":npc_faction", slot_faction_temp_slot, ":number_of_unassigned_centers_plus_landless_lords"),
	(try_end),
   
   	(try_begin),
	  (eq, "$cheat_mode", 1),
 	  (try_for_range, ":faction", kingdoms_begin, kingdoms_end),
		(faction_get_slot, reg4, ":faction", slot_faction_temp_slot),
		(str_store_faction_name, s4, ":faction"),
		(display_message, "str_s4_unassigned_centers_plus_landless_lords_=_reg4"),
	  (try_end),
    (try_end),
   
	(try_for_range, ":cur_center", centers_begin, centers_end),
		(party_get_slot, ":center_lord", ":cur_center", slot_town_lord),
        (this_or_next|eq, ":center_lord", stl_unassigned),
			(eq, ":center_lord", stl_rejected_by_player),
    
        (store_faction_of_party, ":center_faction", ":cur_center"),
        (is_between, ":center_faction", kingdoms_begin, kingdoms_end),
        (neg|faction_slot_eq, ":center_faction", slot_faction_leader, "trp_player"),
        
        (try_begin),
	      (eq, "$cheat_mode", 1),
		  (str_store_party_name, s5, ":cur_center"),
	      (try_begin),
			(neg|faction_slot_ge, ":center_faction", slot_faction_temp_slot, 2),
			(str_store_faction_name, s4, ":center_faction"),
			(display_message, "str_s4_holds_s5_in_reserve"),
		  (try_end),
        (try_end),
	  
		(faction_slot_ge, ":center_faction", slot_faction_temp_slot, 2),
		
		#(display_message, "@Considering grant of {s5}"),

		(assign, ":best_lord", -1),
		(assign, ":best_lord_score", -1),
		(try_begin),
			(eq, ":center_lord", stl_unassigned),
			(try_begin),
				(eq, "$players_kingdom", ":center_faction"),
				(eq, "$player_has_homage", 1),
				(assign, ":best_lord", stl_reserved_for_player),
				(call_script, "script_calculate_troop_score_for_center", "trp_player", ":cur_center"),
				(assign, ":best_lord_score", reg0),
			(try_end),
		(try_end),
    
		(try_for_range, ":cur_troop", active_npcs_begin, active_npcs_end),
			(troop_slot_eq, ":cur_troop", slot_troop_occupation, slto_kingdom_hero),
			(store_troop_faction, ":troop_faction", ":cur_troop"),
			(eq, ":troop_faction", ":center_faction"),

			(call_script, "script_calculate_troop_score_for_center", ":cur_troop", ":cur_center"),
			(assign, ":score", reg0),

			#This prioritizes granting of centers for troops which do not already have one
			(try_begin),
				(troop_slot_eq, ":cur_troop", slot_troop_temp_slot, 0),
				(is_between, ":cur_center", villages_begin, villages_end),
				(val_mul, ":score", 10),
			(try_end),
			
			(gt, ":score", ":best_lord_score"),
			(assign, ":best_lord_score", ":score"),
			(assign, ":best_lord", ":cur_troop"),
		(try_end),
	  
	    #Adjust count of centers and lords
 		(try_begin),
			(this_or_next|ge, ":best_lord", 0),
				(eq, ":best_lord", stl_reserved_for_player),
				
			(faction_get_slot, ":landless_lords_plus_unassigned_centers", ":center_faction", slot_faction_temp_slot),
			(val_sub, ":landless_lords_plus_unassigned_centers", 1),
			
			(try_begin),
				(eq, ":best_lord", stl_reserved_for_player),
				(troop_slot_eq, "trp_player", slot_troop_temp_slot, 0),
				(troop_set_slot, "trp_player", slot_troop_temp_slot, 1),
				(val_sub, ":landless_lords_plus_unassigned_centers", 1), 			
			(else_try),
				(troop_slot_eq, ":best_lord", slot_troop_temp_slot, 0),
				(troop_set_slot, ":best_lord", slot_troop_temp_slot, 1),
				(val_sub, ":landless_lords_plus_unassigned_centers", 1), 			
			(try_end),
			
			(faction_set_slot, ":center_faction", slot_faction_temp_slot, ":landless_lords_plus_unassigned_centers"),
		(try_end),
	  
	    #Give the center to the lord
		(try_begin),
			(ge, ":best_lord", 0),
			(call_script, "script_give_center_to_lord", ":cur_center", ":best_lord", 1),
		(else_try),
			(eq, ":best_lord", stl_reserved_for_player),
			(party_set_slot, ":cur_center", slot_town_lord, stl_reserved_for_player),
			(try_begin), #grant bound villages to player, if granting a castle
				(party_slot_eq, ":cur_center", slot_party_type, spt_castle),
#				(assign, ":give_at_least_one_village", 0),
				(try_for_range, ":cur_village", villages_begin, villages_end),
#					(eq, ":give_at_least_one_village", 0),
					(party_slot_eq, ":cur_village", slot_village_bound_center, ":cur_center"),
					(party_slot_eq, ":cur_village", slot_town_lord, stl_unassigned),
					(party_set_slot, ":cur_village", slot_town_lord, stl_reserved_for_player),
#					(assign, ":give_at_least_one_village", 1),
				(try_end),
			(try_end),
		(try_end),
    (try_end),
    ]),
  # script_create_village_farmer_party
  # Input: arg1 = village_no
  # Output: reg0 = party_no
  ("create_village_farmer_party",
   [(store_script_param, ":village_no", 1),
    (party_get_slot, ":town_no", ":village_no", slot_village_market_town),
    (store_faction_of_party, ":party_faction", ":town_no"),

	
#    (store_faction_of_party, ":town_faction", ":town_no"),
#    (try_begin),
#		(neq, ":town_faction", ":party_faction"),
#		(assign, ":town_no", -1),
#		(assign, ":score_to_beat", 9999),
#		(try_for_range, ":other_town", towns_begin, towns_end),
#			(store_faction_of_party, ":other_town_faction", ":town_no"),
#			(store_relation, ":relation", ":other_town_faction", ":party_faction"),
#			(ge, ":relation", 0),
			
#			(store_distance_to_party_from_party, ":distance", ":village_no", ":other_town"),
#			(lt, ":distance", ":score_to_beat"),
#			(assign, ":town_no", ":other_town"),
#			(assign, ":score_to_beat", ":distance"),
#		(try_end),
#	(try_end),
	
	(try_begin),
		(is_between, ":town_no", towns_begin, towns_end),
	    (set_spawn_radius, 0),
	    (spawn_around_party, ":village_no", "pt_village_farmers"),
	    (assign, ":new_party", reg0),
	      
	    (party_set_faction, ":new_party", ":party_faction"),
	    (party_set_slot, ":new_party", slot_party_home_center, ":village_no"),
	    (party_set_slot, ":new_party", slot_party_last_traded_center, ":village_no"),

	    (party_set_slot, ":new_party", slot_party_type, spt_village_farmer),
	    (party_set_slot, ":new_party", slot_party_ai_state, spai_trading_with_town),
	    (party_set_slot, ":new_party", slot_party_ai_object, ":town_no"),
	    (party_set_ai_behavior, ":new_party", ai_bhvr_travel_to_party),
	    (party_set_ai_object, ":new_party", ":town_no"),
	    (party_set_flags, ":new_party", pf_default_behavior, 0),
	    (store_sub, ":item_to_price_slot", slot_town_trade_good_prices_begin, trade_goods_begin),
	    (try_for_range, ":cur_goods", trade_goods_begin, trade_goods_end),
	      (store_add, ":cur_good_price_slot", ":cur_goods", ":item_to_price_slot"),
	      (party_get_slot, ":cur_village_price", ":village_no", ":cur_good_price_slot"),
	      (party_set_slot, ":new_party", ":cur_good_price_slot", ":cur_village_price"),
	    (try_end),
	    (assign, reg0, ":new_party"),
	(try_end),
	
    ]),
  #script_player_join_faction
  # INPUT: arg1 = faction_no
  # OUTPUT: none
  ("player_join_faction",
    [
      (store_script_param, ":faction_no", 1),
      (assign,"$players_kingdom",":faction_no"),
      (faction_set_slot, "fac_player_supporters_faction", slot_faction_ai_state, sfai_default),
      (assign, "$players_oath_renounced_against_kingdom", 0),
      (assign, "$players_oath_renounced_given_center", 0),
      (assign, "$players_oath_renounced_begin_time", 0),
      
      (try_for_range,":other_kingdom",kingdoms_begin,kingdoms_end),
        (faction_slot_eq, ":other_kingdom", slot_faction_state, sfs_active),
        (neq, ":other_kingdom", "fac_player_supporters_faction"),
        (try_begin),
          (neq, ":other_kingdom", ":faction_no"),
          (store_relation, ":other_kingdom_reln", ":other_kingdom", ":faction_no"),
        (else_try),
          (store_relation, ":other_kingdom_reln", "fac_player_supporters_faction", ":other_kingdom"),
          (val_max, ":other_kingdom_reln", 12),
        (try_end),
        (call_script, "script_set_player_relation_with_faction", ":other_kingdom", ":other_kingdom_reln"),
      (try_end),
      
      (try_for_range, ":cur_center", centers_begin, centers_end),
        #Give center to kingdom if player is the owner
        (party_slot_eq, ":cur_center", slot_town_lord, "trp_player"),
        (call_script, "script_give_center_to_faction_while_maintaining_lord", ":cur_center", ":faction_no"),
	  (else_try),
        #Give center to kingdom if part of player faction
     	(store_faction_of_party, ":cur_center_faction", ":cur_center"),
		(eq, ":cur_center_faction", "fac_player_supporters_faction"),
        (call_script, "script_give_center_to_faction_while_maintaining_lord", ":cur_center", ":faction_no"),
      (try_end),
      
      (try_for_range, ":quest_no", lord_quests_begin, lord_quests_end),
        (check_quest_active, ":quest_no"),
        (quest_get_slot, ":quest_giver_troop", ":quest_no", slot_quest_giver_troop),
        (store_troop_faction, ":quest_giver_faction", ":quest_giver_troop"),
        (store_relation, ":quest_giver_faction_relation", "fac_player_supporters_faction", ":quest_giver_faction"),
        (lt, ":quest_giver_faction_relation", 0),
        (call_script, "script_abort_quest", ":quest_no", 0),
      (try_end),
      (try_for_range, ":quest_no", lord_quests_begin_2, lord_quests_end_2),
        (check_quest_active, ":quest_no"),
        (quest_get_slot, ":quest_giver_troop", ":quest_no", slot_quest_giver_troop),
        (store_troop_faction, ":quest_giver_faction", ":quest_giver_troop"),
        (store_relation, ":quest_giver_faction_relation", "fac_player_supporters_faction", ":quest_giver_faction"),
        (lt, ":quest_giver_faction_relation", 0),
        (call_script, "script_abort_quest", ":quest_no", 0),
      (try_end),
      (try_begin),
        (neq, ":faction_no", "fac_player_supporters_faction"),
        (faction_set_slot, "fac_player_supporters_faction", slot_faction_state, sfs_inactive),
        (faction_set_slot, "fac_player_supporters_faction", slot_faction_leader, "trp_player"),
      (try_end),
	  
	  (try_begin),
		(troop_get_slot, ":spouse", "trp_player", slot_troop_spouse),
	    (is_between, ":spouse", kingdom_ladies_begin, kingdom_ladies_end),
		
		(try_begin),
			(ge, "$cheat_mode", 1),
			(str_store_troop_name, s4, ":spouse"),
			(display_message, "@{!}DEBUG - {s4} faction changed by marriage, case 1"), 
		(try_end),
		
	    (troop_set_faction, ":spouse", "$players_kingdom"),
	  (try_end),
	  ##diplomacy start+
	  #Make other vassals follow the player.
	  ##(There are other possibilities that we might want to explore, but
	  ##what happens now is that they remain members of the defunct faction.)
	  (try_begin),
		(neq, ":faction_no", "fac_player_supporters_faction"),
		  (try_for_range, ":troop_no", heroes_begin, heroes_end),
			 (store_troop_faction, ":other_troop_faction", ":troop_no"),
			 (eq, ":other_troop_faction", "fac_player_supporters_faction"),

			 #gekokujo 3.0 microfactions! include fort companions start
			 #(this_or_next|neg|is_between, ":troop_no", companions_begin, companions_end),
			 (this_or_next|neg|is_between, ":troop_no", companions_begin, fort_companions_end),
			 #gekokujo 3.0 microfactions! include fort companions end
			 (this_or_next|troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
			 (this_or_next|troop_slot_eq, ":troop_no", slot_troop_playerparty_history, dplmc_pp_history_granted_fief),
				(troop_slot_eq, ":troop_no", slot_troop_playerparty_history, dplmc_pp_history_lord_rejoined),
			 (this_or_next|neq, ":troop_no", ":spouse"),
				(neg|is_between, ":spouse", kingdom_ladies_begin, kingdom_ladies_end),
			(try_begin),
				(ge, "$cheat_mode", 1),
				(str_store_troop_name, s4, ":troop_no"),
				(display_message, "@{!} DEBUG - {s4} changed by player's defection"),
			(try_end),
			(troop_set_faction, ":troop_no", "$players_kingdom"),
			#Clear troop slots
			(troop_set_slot, ":troop_no", slot_troop_stance_on_faction_issue, -1),
			(troop_set_slot, ":troop_no", slot_troop_recruitment_random, 0),
			(troop_set_slot, ":troop_no", slot_lord_recruitment_argument, 0),
			(troop_set_slot, ":troop_no", slot_lord_recruitment_candidate, 0),
			(troop_set_slot, ":troop_no", slot_troop_promised_fief, 0),
			#Give new title
			(try_begin),
				(this_or_next|neg|is_between,":troop_no", kingdom_ladies_begin, kingdom_ladies_end),
					(troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
				(call_script, "script_troop_set_title_according_to_faction", ":troop_no", ":faction_no"),
			(try_end),
			#Change led party
			(try_begin),
				(troop_get_slot, ":troop_leaded_party", ":troop_no", slot_troop_leaded_party),
				(gt, ":troop_leaded_party", 0),
				(party_is_active, ":troop_leaded_party"),
				(party_set_faction, ":troop_leaded_party", ":faction_no"),
			(try_end),
		  (try_end),
	  (try_end),
	  ##diplomacy end+
	  	  
	  (try_for_range, ":center", centers_begin, centers_end),
	    (store_faction_of_party, ":center_faction", ":faction_no"),
		(neq, ":center_faction", "$players_kingdom"),
		(party_slot_eq, ":center", slot_town_lord, stl_reserved_for_player),
#		(party_set_slot, ":center", slot_town_lord, stl_unassigned),
	  (try_end),
	  
	  (troop_set_slot, "trp_player", slot_troop_stance_on_faction_issue, -1),
	  
	  #remove prisoners of player's faction if he was member of his own faction. And free companions which is prisoned in that faction.
      (try_for_parties, ":party_no"),
        (store_faction_of_party, ":party_faction", ":party_no"),
        (eq, ":party_faction", ":faction_no"),
        
        (party_get_num_prisoner_stacks, ":num_stacks", ":party_no"),
        (try_for_range_backwards, ":troop_iterator", 0, ":num_stacks"),
          (party_prisoner_stack_get_troop_id, ":cur_troop_id", ":party_no", ":troop_iterator"),                                 
          (store_troop_faction, ":cur_faction", ":cur_troop_id"),
                      
          (this_or_next|eq, ":cur_faction", "fac_player_supporters_faction"),
          (this_or_next|eq, ":cur_faction", ":faction_no"),
		  #gekokujo 3.0 microfactions! include fort companions start
          #(is_between, ":cur_troop_id", companions_begin, companions_end),
          (is_between, ":cur_troop_id", companions_begin, fort_companions_end),
		  #gekokujo 3.0 microfactions! include fort companions end
            
          (try_begin),
            (troop_is_hero, ":cur_troop_id"),
            (call_script, "script_remove_troop_from_prison", ":cur_troop_id"),
          (try_end),
          
          (party_prisoner_stack_get_size, ":stack_size", ":party_no", ":troop_iterator"),
          (party_remove_prisoners, ":party_no", ":cur_troop_id", ":stack_size"),
          
          (try_begin),
			#gekokujo 3.0 microfactions! include fort companions start
            #(is_between, ":cur_troop_id", companions_begin, companions_end),
            (is_between, ":cur_troop_id", companions_begin, fort_companions_end),
			#gekokujo 3.0 microfactions! include fort companions end
            
            (try_begin),
              (is_between, ":party_no", towns_begin, towns_end),
              (troop_set_slot, ":cur_troop_id", slot_troop_cur_center, ":party_no"),
            (else_try),
              (store_random_in_range, ":random_town_no", towns_begin, towns_end),       
              (troop_set_slot, ":cur_troop_id", slot_troop_cur_center, ":random_town_no"),
            (try_end),  
          (try_end),
        (try_end),
      (try_end),
      #remove prisoners end.

      #(call_script, "script_store_average_center_value_per_faction"),
      (call_script, "script_update_all_notes"),
      (assign, "$g_recalculate_ais", 1),
      ]),
  #script_player_leave_faction
  # INPUT: arg1 = give_back_fiefs
  # OUTPUT: none
  ("player_leave_faction",
    [
      (store_script_param, ":give_back_fiefs", 1),
	  
      (call_script, "script_check_and_finish_active_army_quests_for_faction", "$players_kingdom"),
      (assign, ":old_kingdom", "$players_kingdom"),
      (assign, ":old_has_homage", "$player_has_homage"),
      (assign, "$players_kingdom", 0),
      (assign, "$player_has_homage", 0),
	  
      (try_begin),
        (neq, ":give_back_fiefs", 0), #ie, give back fiefs = 1, thereby do it
        (try_for_range, ":cur_center", centers_begin, centers_end),
          (party_slot_eq, ":cur_center", slot_town_lord, "trp_player"),
          ##diplomacy begin
          #native bug fix when giving back fiefs
          (call_script, "script_give_center_to_faction", ":cur_center", "fac_neutral"),
          ##diplomacy end
          (call_script, "script_give_center_to_faction", ":cur_center", ":old_kingdom"),
		  
		  #The following line also occurs when a lord is stripped of his fiefs by an indictment
		  (party_set_slot, ":cur_center", slot_town_lord, stl_unassigned),
        (try_end),		
      (else_try),
	    #If you retain the fiefs
        (try_for_range, ":cur_center", centers_begin, centers_end),
          (party_slot_eq, ":cur_center", slot_town_lord, "trp_player"),
          (call_script, "script_give_center_to_faction", ":cur_center", "fac_player_supporters_faction"),
		  (party_set_slot, ":cur_center", slot_town_lord, "trp_player"),
          (troop_get_slot, ":cur_banner", "trp_player", slot_troop_banner_scene_prop),
          (gt, ":cur_banner", 0),
          (val_sub, ":cur_banner", banner_scene_props_begin),
          (val_add, ":cur_banner", banner_map_icons_begin),
          (party_set_banner_icon, ":cur_center", ":cur_banner"),		  		  
        (try_end),
        
        (try_for_range, ":cur_center", villages_begin, villages_end),
          (party_get_slot, ":cur_bound_center", ":cur_center", slot_village_bound_center),
          (party_slot_eq, ":cur_center", slot_town_lord, "trp_player"),
          (neg|party_slot_eq, ":cur_bound_center", slot_town_lord, "trp_player"),
          (call_script, "script_give_center_to_faction", ":cur_center", ":old_kingdom"),
        (try_end),
	  
		(is_between, ":old_kingdom", kingdoms_begin, kingdoms_end),
		(neq, ":old_kingdom", "fac_player_supporters_faction"),		
        (store_relation, ":reln", "fac_player_supporters_faction", ":old_kingdom"),
        (store_sub, ":req_dif", -40, ":reln"),
        (call_script, "script_change_player_relation_with_faction", ":old_kingdom", ":req_dif"),
      (try_end),
	  
      (try_begin),
        (eq, ":old_has_homage", 1),
        (faction_get_slot, ":faction_leader", ":old_kingdom", slot_faction_leader),
        (call_script, "script_change_player_relation_with_troop", ":faction_leader", -20),
      (try_end),
	  
	  (try_begin),
		(troop_get_slot, ":spouse", "trp_player", slot_troop_spouse),
	    (is_between, ":spouse", kingdom_ladies_begin, kingdom_ladies_end),
		
		(try_begin),
			(ge, "$cheat_mode", 1),
			(str_store_troop_name, s4, ":spouse"),
			(display_message, "@{!}DEBUG - {s4} faction changed by marriage, case 3"), 
		(try_end),
		
		
	    (troop_set_faction, ":spouse", "fac_player_supporters_faction"),
	  (try_end),
	  
	  #Change relations with players_kingdom when player changes factions
	  (try_for_range, ":kingdom", kingdoms_begin, kingdoms_end),
	    (neq, ":kingdom", "fac_player_supporters_faction"),
	    (store_relation, ":relation_with_old_faction", ":old_kingdom", ":kingdom"),
	    (store_relation, ":relation_with_player_faction", "fac_player_faction", ":kingdom"),
	    
	    (try_begin),
	      (eq, ":old_kingdom", ":kingdom"),
	      (val_min, ":relation_with_player_faction", 0),
	    (else_try),	
	      (lt, ":relation_with_old_faction", 0),
	      (val_max, ":relation_with_player_faction", 0),
       ##diplomacy start+ do not retain allies of former kingdom
       (else_try),
         (gt, ":relation_with_old_faction", 0),
         (val_min, ":relation_with_player_faction", 0),
       ##diplomacy end+
	    (try_end),
	    (set_relation, "fac_player_faction", ":kingdom", ":relation_with_player_faction"),
	    (set_relation, "fac_player_supporters_faction", ":kingdom", ":relation_with_player_faction"),
	  (try_end),
	  
	  (call_script, "script_update_all_notes"),
	  (assign, "$g_recalculate_ais", 1),

        ##diplomacy begin
        ##disband player patrols
      (try_for_parties, ":party_no"),
        (party_slot_eq,":party_no", slot_party_type, spt_patrol),
		(party_slot_eq, ":party_no", dplmc_slot_party_mission_diplomacy, "trp_player"),
        (party_get_slot, ":target_party", ":party_no", slot_party_ai_object),
        (str_store_party_name, s6, ":target_party"),
        (display_log_message, "@Your soldiers patrolling {s6} disbanded because you left the faction!", 0xFF0000),
        (remove_party, ":party_no"),
      (try_end),
        ##diplomacy end
    ]),
    ("deactivate_player_faction",
    [
	(faction_set_slot, "fac_player_supporters_faction", slot_faction_state, sfs_inactive),
    (faction_set_slot, "fac_player_supporters_faction", slot_faction_leader, "trp_player"),
    (assign, "$players_kingdom", 0),
    (assign, "$players_oath_renounced_against_kingdom", 0),
    (assign, "$players_oath_renounced_given_center", 0),
    (assign, "$players_oath_renounced_begin_time", 0),
    #(call_script, "script_store_average_center_value_per_faction"),
    (call_script, "script_update_all_notes"),
	
	(try_begin),
		#gekokujo 3.0 microfactions! include fort companions start
		#(is_between, "$g_player_minister", companions_begin, companions_end),
		(is_between, "$g_player_minister", companions_begin, fort_companions_end),
		#gekokujo 3.0 microfactions! include fort companions end
		(assign, "$npc_to_rejoin_party", "$g_player_minister"),
	(try_end),
	(assign, "$g_player_minister", -1),
	
    (call_script, "script_add_notification_menu", "mnu_notification_player_faction_deactive", 0, 0),
    ]),
  #When a player convinces her husband to rebel
  #When a player proclaims herself queen
  #When a player seizes control of a center  
  #When a player recruits a lord through intrigue
  #When a player 
    ("activate_player_faction",
    [
    (store_script_param, ":liege", 1),

	#This moved to top, so that mnu_notification does not occur twice
	(try_begin),
		(faction_slot_eq, "fac_player_supporters_faction", slot_faction_state, sfs_inactive),
		(neg|is_between, ":liege", pretenders_begin, pretenders_end),
		(call_script, "script_add_notification_menu", "mnu_notification_player_faction_active", 0, 0),
		##diplomacy begin
		(call_script, "script_add_notification_menu", "mnu_dplmc_domestic_policy", 0, 0),
		##diplomacy end
	(try_end),

	
    (faction_set_slot, "fac_player_supporters_faction", slot_faction_state, sfs_active),
    (faction_set_slot, "fac_player_supporters_faction", slot_faction_leader, ":liege"),

	(assign, ":original_kingdom", "$players_kingdom"),
	
	(try_begin),
		(is_between, ":original_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
		(call_script, "script_player_leave_faction", 0), #Ends quests, transfers control of centers
	(try_end),
	
	#Name faction
	(try_begin),
		(is_between, ":liege", active_npcs_begin, active_npcs_end),
		(store_faction_of_troop, ":liege_faction"),
		(is_between, ":liege_faction", npc_kingdoms_begin, npc_kingdoms_end),
		(faction_get_slot, ":adjective_string", ":liege_faction", slot_faction_adjective),
		(str_store_string, s1, ":adjective_string"),
		(faction_set_name, "fac_player_supporters_faction", "@{s1} Rebels"),
	(else_try),
		(str_store_troop_name, s2, ":liege"),
        (str_store_string, s1, "str_s2s_rebellion"),
	(try_end),	
    (faction_set_color, "fac_player_supporters_faction", 0xFF0000),
	
    (assign, "$players_kingdom", "fac_player_supporters_faction"),
    (assign, "$g_player_banner_granted", 1),
	
	
	
	#Any oaths renounced?
	(try_begin),
		(is_between, ":original_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
		
        (faction_get_slot, ":old_leader", ":original_kingdom", slot_faction_leader),
        (call_script, "script_add_log_entry", logent_renounced_allegiance,   "trp_player",  -1, ":old_leader", "$players_kingdom"),

        #Initializing renounce war variables
        (assign, "$players_oath_renounced_against_kingdom", ":original_kingdom"),
        (assign, "$players_oath_renounced_given_center", 0),
        (store_current_hours, "$players_oath_renounced_begin_time"),
        
        (try_for_range, ":cur_center", walled_centers_begin, walled_centers_end),
          (store_faction_of_party, ":cur_center_faction", ":cur_center"),
          (party_set_slot, ":cur_center", slot_center_faction_when_oath_renounced, ":cur_center_faction"),
        (try_end),
        (party_set_slot, "$g_center_to_give_to_player", slot_center_faction_when_oath_renounced, "$players_oath_renounced_against_kingdom"),
		
		(store_relation, ":relation", ":original_kingdom", "fac_player_supporters_faction"),
		(ge, ":relation", 0),
		(call_script, "script_diplomacy_start_war_between_kingdoms", ":original_kingdom", "fac_player_supporters_faction", 1),
	(try_end),
	
	
	(try_begin),
		(troop_get_slot, ":spouse", "trp_player", slot_troop_spouse),
	    (is_between, ":spouse", kingdom_ladies_begin, kingdom_ladies_end),
		
		
		(try_begin),
			(ge, "$cheat_mode", 1),
			(str_store_troop_name, s4, ":spouse"),
			(display_message, "@{!}DEBUG - {s4} faction changed by marriage, case 2"), 
		(try_end),
		
	    (troop_set_faction, ":spouse", "fac_player_supporters_faction"),
	(try_end),
		 	
	
    #(call_script, "script_store_average_center_value_per_faction"),
    (call_script, "script_update_all_notes"),
	(assign, "$g_recalculate_ais", 1),
	
    ]),
  #script_update_villages_infested_by_bandits
  # INPUT: none
  # OUTPUT: none
  ("update_villages_infested_by_bandits",
    [(try_for_range, ":village_no", villages_begin, villages_end),
       (try_begin),
         (check_quest_active, "qst_eliminate_bandits_infesting_village"),
         (quest_slot_eq, "qst_eliminate_bandits_infesting_village", slot_quest_target_center, ":village_no"),
         (quest_get_slot, ":cur_state", "qst_eliminate_bandits_infesting_village", slot_quest_current_state),
         (val_add, ":cur_state", 1),
         (try_begin),
           (lt, ":cur_state", 3),
           (quest_set_slot, "qst_eliminate_bandits_infesting_village", slot_quest_current_state, ":cur_state"),
         (else_try),
           (party_set_slot, ":village_no", slot_village_infested_by_bandits, 0),
           (call_script, "script_abort_quest", "qst_eliminate_bandits_infesting_village", 2),
         (try_end),
       (else_try),
         (check_quest_active, "qst_deal_with_bandits_at_lords_village"),
         (quest_slot_eq, "qst_deal_with_bandits_at_lords_village", slot_quest_target_center, ":village_no"),
         (quest_get_slot, ":cur_state", "qst_deal_with_bandits_at_lords_village", slot_quest_current_state),
         (val_add, ":cur_state", 1),
         (try_begin),
           (lt, ":cur_state", 3),
           (quest_set_slot, "qst_deal_with_bandits_at_lords_village", slot_quest_current_state, ":cur_state"),
         (else_try),
           (party_set_slot, ":village_no", slot_village_infested_by_bandits, 0),
           (call_script, "script_abort_quest", "qst_deal_with_bandits_at_lords_village", 2),
         (try_end),
       (else_try),
         (party_set_slot, ":village_no", slot_village_infested_by_bandits, 0),
         (store_random_in_range, ":random_no", 0, 100),
         (assign, ":continue", 1),
         (try_begin),
           (check_quest_active, "qst_collect_taxes"),
           (quest_slot_eq, "qst_collect_taxes", slot_quest_target_center, ":village_no"),
           (assign, ":continue", 0),
         (else_try),
           (check_quest_active, "qst_train_peasants_against_bandits"),
           (quest_slot_eq, "qst_train_peasants_against_bandits", slot_quest_target_center, ":village_no"),
           (assign, ":continue", 0),
         (try_end),
         (eq, ":continue", 1),
         (lt, ":random_no", 3),
         (store_random_in_range, ":random_no", 0, 3),
         (try_begin),
           (eq, ":random_no", 0),
           (assign, ":bandit_troop", "trp_bandit"),
         (else_try),
           (eq, ":random_no", 1),
           (assign, ":bandit_troop", "trp_woku_pirate"),
         (else_try),
           (assign, ":bandit_troop", "trp_shinano_rebel"),
         (try_end),
         (party_set_slot, ":village_no", slot_village_infested_by_bandits, ":bandit_troop"),
         #Reduce prosperity of the village by 3: reduce to -1
         (call_script, "script_change_center_prosperity", ":village_no", -1),
		 (val_add, "$newglob_total_prosperity_from_bandits", -1),
         (try_begin),
           (eq, "$cheat_mode", 2),
           (str_store_party_name, s1, ":village_no"),
           (display_message, "@{!}DEBUG --{s1} is infested by bandits."),
         (try_end),
       (try_end),
     (try_end),
     ]),
  #script_update_faction_notes
  # INPUT: faction_no
  # OUTPUT: none
  ("update_faction_notes",
    [
      (store_script_param, ":faction_no", 1),
            
      (try_begin),
        (this_or_next|faction_slot_eq, ":faction_no", slot_faction_state, sfs_inactive),
        (eq, ":faction_no", "fac_player_faction"),
        (faction_set_note_available, ":faction_no", 0),
      (else_try),
        (faction_set_note_available, ":faction_no", 1),
      (try_end),
##
##	(try_begin),
##		(eq, 2, 1),
##		(str_store_faction_name, s14, ":faction_no"),
##		(assign, reg4, "$temp"),
##		(display_message, "str_updating_faction_notes_for_s14_temp_=_reg4"),
##	(try_end),
##		
##    (try_begin),
##       (is_between, ":faction_no", kingdoms_begin, kingdoms_end),
##       (faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
##       (faction_get_slot, ":faction_leader", ":faction_no", slot_faction_leader),
##       (str_store_faction_name, s5, ":faction_no"),
##       (str_store_troop_name_link, s6, ":faction_leader"),
##       (assign, ":num_centers", 0),
##       (str_store_string, s8, "@nowhere"),
##       (try_for_range_backwards, ":cur_center", centers_begin, centers_end),
##         (store_faction_of_party, ":center_faction", ":cur_center"),
##         (eq, ":center_faction", ":faction_no"),
##         (try_begin),
##           (eq, ":num_centers", 0),
##           (str_store_party_name_link, s8, ":cur_center"),
##         (else_try),
##           (eq, ":num_centers", 1),
##           (str_store_party_name_link, s7, ":cur_center"),
##           (str_store_string, s8, "@{s7} and {s8}"),
##         (else_try),
##           (str_store_party_name_link, s7, ":cur_center"),
##           (str_store_string, s8, "@{!}{s7}, {s8}"),
##         (try_end),
##         (val_add, ":num_centers", 1),
##       (try_end),
##       (assign, ":num_members", 0),
##       (str_store_string, s10, "@noone"),
##       (try_for_range_backwards, ":loop_var", "trp_kingdom_heroes_including_player_begin", active_npcs_end),
##         (assign, ":cur_troop", ":loop_var"),
##         (try_begin),
##           (eq, ":loop_var", "trp_kingdom_heroes_including_player_begin"),
##           (assign, ":cur_troop", "trp_player"),
##           (assign, ":troop_faction", "$players_kingdom"),
##         (else_try),
##           (store_troop_faction, ":troop_faction", ":cur_troop"),
##         (try_end),
##         (eq, ":troop_faction", ":faction_no"),
##         (neq, ":cur_troop", ":faction_leader"),
##         (troop_slot_eq, ":cur_troop", slot_troop_occupation, slto_kingdom_hero),
##         (try_begin),
##           (eq, ":num_members", 0),
##           (str_store_troop_name_link, s10, ":cur_troop"),
##         (else_try),
##           (eq, ":num_members", 1),
##           (str_store_troop_name_link, s9, ":cur_troop"),
##           (str_store_string, s10, "@{s9} and {s10}"),
##         (else_try),
##           (str_store_troop_name_link, s9, ":cur_troop"),
##           (str_store_string, s10, "@{!}{s9}, {s10}"),
##         (try_end),
##         (val_add, ":num_members", 1),
##       (try_end),
##	   
##	   #wars
##       (str_store_string, s12, "@noone"),
###       (assign, ":num_enemies", 0),
###       (try_for_range_backwards, ":cur_faction", kingdoms_begin, kingdoms_end),
###         (faction_slot_eq, ":cur_faction", slot_faction_state, sfs_active),
###         (store_relation, ":cur_relation", ":cur_faction", ":faction_no"),
###         (lt, ":cur_relation", 0),
###         (try_begin),
###           (eq, ":num_enemies", 0),
###           (str_store_faction_name_link, s12, ":cur_faction"),
###         (else_try),
###           (eq, ":num_enemies", 1),
###           (str_store_faction_name_link, s11, ":cur_faction"),
###           (str_store_string, s12, "@the {s11} and the {s12}"),
###         (else_try),
###           (str_store_faction_name_link, s11, ":cur_faction"),
###           (str_store_string, s12, "@the {s11}, the {s12}"),
###         (try_end),
###         (val_add, ":num_enemies", 1),
###       (try_end),
##	   
##       (str_store_string, s21, "str_foreign_relations__"),
##	   
##	   #other foreign relations
##       (try_for_range, ":cur_faction", kingdoms_begin, kingdoms_end),
##         (faction_slot_eq, ":cur_faction", slot_faction_state, sfs_active),
##		 (neq, ":faction_no", ":cur_faction"),
##		 (str_store_faction_name_link, s14, ":cur_faction"),
##         (call_script, "script_diplomacy_faction_get_diplomatic_status_with_faction", ":faction_no", ":cur_faction"),
##		 (assign, ":diplomatic_status", reg0),
##		 (assign, reg2, reg1), #length of events
##		 (call_script, "script_diplomacy_faction_get_diplomatic_status_with_faction", ":cur_faction", ":faction_no"),
##		 (assign, ":reverse_diplomatic_status", reg0),
##		 
##		 
##		 (try_begin),
##			(eq, ":diplomatic_status", -2),
##			(str_store_string, s21, "str_s21__the_s5_is_at_war_with_the_s14"), 
##		 
##			(store_add, ":slot_war_damage_inflicted", ":cur_faction", slot_faction_war_damage_inflicted_on_factions_begin),
##			(val_sub, ":slot_war_damage_inflicted", kingdoms_begin),
##			(faction_get_slot, ":war_damage_inflicted", ":faction_no", ":slot_war_damage_inflicted"),
##			(store_mul, ":war_damage_inflicted_x_2", ":war_damage_inflicted", 2),
##			
##			(store_add, ":slot_war_damage_suffered", ":faction_no", slot_faction_war_damage_inflicted_on_factions_begin),
##			(val_sub, ":slot_war_damage_suffered", kingdoms_begin),
##			(faction_get_slot, ":war_damage_suffered", ":cur_faction", ":slot_war_damage_suffered"),
##			(store_mul, ":war_damage_suffered_x_2", ":war_damage_suffered", 2),
##			
##			(try_begin),
##				(gt, ":war_damage_inflicted", ":war_damage_suffered_x_2"),
##				(str_store_string, s21, "str_s21_the_s5_has_had_the_upper_hand_in_the_fighting"),
##			(else_try),
##				(gt, ":war_damage_suffered", ":war_damage_inflicted_x_2"),
##				(str_store_string, s21, "@{s21}. The {s14} has gotten the worst of the fighting."),
##			(else_try),
##				(gt, ":war_damage_inflicted", 100),
##				(gt, ":war_damage_inflicted", 100),
##				(str_store_string, s21, "str_s21_the_fighting_has_gone_on_for_some_time_and_the_war_may_end_soon_with_a_truce"),
##			(else_try),
##				(str_store_string, s21, "str_s21_the_fighting_has_begun_relatively_recently_and_the_war_may_continue_for_some_time"),
##			(try_end),
##			
##			(try_begin),
##				(eq, "$cheat_mode", 1),
##				(assign, reg4, ":war_damage_inflicted"),
##				(assign, reg5, ":war_damage_suffered"),
##				(str_store_string, s21, "str_s21_reg4reg5"),
##			(try_end),
##		 (else_try),
##			(eq, ":diplomatic_status", 1),
##			(str_clear, s18),
##
##			(try_begin),
##				(neq, reg0, 1),
##				(str_store_string, s18, "str__however_the_truce_is_no_longer_binding_on_the_s14"),
##			(try_end),
##			(str_store_string, s21, "str_s21__the_s5_is_bound_by_truce_not_to_attack_the_s14s18_the_truce_will_expire_in_reg1_days"),
##			
##		 (else_try), 
##			(eq, ":diplomatic_status", -1),
##			(str_store_string, s21, "str_s21__the_s5_has_recently_suffered_provocation_by_subjects_of_the_s14_and_there_is_a_risk_of_war"),
##		 (else_try),
##			(eq, ":diplomatic_status", 0),
##			(str_store_string, s21, "str_s21__the_s5_has_no_outstanding_issues_with_the_s14"),
##		 (try_end),
##			 
##			 
##		 (try_begin),
##			(eq, ":reverse_diplomatic_status", -1),
##			(str_store_string, s21, "str_s21_the_s14_was_recently_provoked_by_subjects_of_the_s5_and_there_is_a_risk_of_war_"), 
##		 (try_end),
##		 
##		 (try_begin),
##			(eq, "$cheat_mode", 1),
##			(call_script, "script_diplomacy_faction_assess_faction_to_s14", ":faction_no", ":cur_faction", -1),
##			(str_store_string, s21, "str_s21_cheat_mode_assessment_s14_"), 
##	     (try_end),
##	  (try_end),	 
##
##	  
##	  (add_faction_note_from_sreg, ":faction_no", 0, "str_the_s5_is_ruled_by_s6_it_occupies_s8_its_vassals_are_s10__s21", 0),
##
##
##	   
##    (else_try),
##       (is_between, ":faction_no", kingdoms_begin, kingdoms_end),
##       (faction_slot_eq, ":faction_no", slot_faction_state, sfs_defeated),
##       (str_store_faction_name, s5, ":faction_no"),
##       (add_faction_note_from_sreg, ":faction_no", 0, "@{s5} has been defeated!", 0),
##       (str_clear, s1),
##       (add_faction_note_from_sreg, ":faction_no", 1, s1, 0),
##    (else_try),
##       (str_clear, s1),
##       (add_faction_note_from_sreg, ":faction_no", 0, s1, 0),
##       (add_faction_note_from_sreg, ":faction_no", 1, s1, 0),
##    (try_end),
##	
##    (try_begin),
##       (is_between, ":faction_no", "fac_kingdom_1", kingdoms_end), #Excluding player kingdom
##       (add_faction_note_tableau_mesh, ":faction_no", "tableau_faction_note_mesh"),
##    (else_try),
##       (add_faction_note_tableau_mesh, ":faction_no", "tableau_faction_note_mesh_banner"),
##    (try_end),
     ]),
  ("update_faction_political_notes",
    [(store_script_param, ":faction_no", 1),
	 
	(call_script, "script_evaluate_realm_stability", ":faction_no"),
    (add_faction_note_from_sreg, ":faction_no", 2, "str_instability_reg0_of_lords_are_disgruntled_reg1_are_restless", 0),
	]),
  #script_update_faction_traveler_notes
  # INPUT: faction_no
  # OUTPUT: none
  ("update_faction_traveler_notes",
    [(store_script_param, ":faction_no", 1),
     (assign, ":total_men", 0),
     (try_for_parties, ":cur_party"),
       (store_faction_of_party, ":center_faction", ":cur_party"),
       (eq, ":center_faction", ":faction_no"),
       (party_get_num_companions, ":num_men", ":cur_party"),
       (val_add, ":total_men", ":num_men"),
     (try_end),
     (str_store_faction_name, s5, ":faction_no"),
     (assign, reg1, ":total_men"),
     (add_faction_note_from_sreg, ":faction_no", 1, "@{s5} has a strength of {reg1} men in total.", 1),
     ]),
  #script_update_troop_notes
  # INPUT: troop_no
  # OUTPUT: none
  ("update_troop_notes",
    [
##      (store_script_param, ":troop_no", 1),
##     (str_store_troop_name, s54, ":troop_no"),
##     (try_begin),
##       (eq, ":troop_no", "trp_player"),
##       (this_or_next|eq, "$player_has_homage", 1),
##		(eq, "$players_kingdom", "fac_player_supporters_faction"),
##       (assign, ":troop_faction", "$players_kingdom"),
##     (else_try),
##       (store_troop_faction, ":troop_faction", ":troop_no"),
##     (try_end),
##	 
##	 (str_clear, s49),
##	 (try_begin),
##		(is_between, ":troop_no", lords_begin, kingdom_ladies_end),
##		(troop_get_slot, reg1, ":troop_no", slot_troop_age),
##		(str_store_string, s49, "str__age_reg1_family_"),
##		
##		(try_for_range, ":aristocrat", lords_begin, kingdom_ladies_end),
##			(call_script, "script_troop_get_family_relation_to_troop", ":aristocrat", ":troop_no"),
##			(gt, reg0, 0),
##
##			(try_begin),
##				(neg|is_between, ":aristocrat", kingdom_ladies_begin, kingdom_ladies_end),
##				(str_store_troop_name_link, s12, ":aristocrat"),
##				(call_script, "script_troop_get_relation_with_troop", ":aristocrat", ":troop_no"),
##				(str_store_string, s49, "str_s49_s12_s11_rel_reg0"),
##			(else_try),	
##				(str_store_troop_name, s12, ":aristocrat"),
##				(str_store_string, s49, "str_s49_s12_s11"),
##			(try_end),	
##			
##		(try_end),
##	 (try_end),
##	 
##     (try_begin),
##       (neq, ":troop_no", "trp_player"),
##       (neg|is_between, ":troop_faction", kingdoms_begin, kingdoms_end),
##       (str_clear, s54),
##       (add_troop_note_from_sreg, ":troop_no", 0, s54, 0),
##       (add_troop_note_from_sreg, ":troop_no", 1, s54, 0),
##       (add_troop_note_from_sreg, ":troop_no", 2, s54, 0),
###     (else_try),
###       (is_between, ":troop_no", kingdom_ladies_begin, kingdom_ladies_end),
###       (str_clear, s54),
###       (add_troop_note_from_sreg, ":troop_no", 0, s54, 0),
###       (add_troop_note_from_sreg, ":troop_no", 1, s54, 0),
###       (add_troop_note_from_sreg, ":troop_no", 2, s54, 0),
##     (else_try),
##       (is_between, ":troop_no", pretenders_begin, pretenders_end),
##       (neg|troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
##       (neq, ":troop_no", "$supported_pretender"),
##       (troop_get_slot, ":orig_faction", ":troop_no", slot_troop_original_faction),
##       (try_begin),
##         (faction_slot_eq, ":orig_faction", slot_faction_state, sfs_active),
##         (faction_slot_eq, ":orig_faction", slot_faction_has_rebellion_chance, 1),
##         (str_store_faction_name_link, s56, ":orig_faction"),
##         (add_troop_note_from_sreg, ":troop_no", 0, "@{s54} is a claimant to the throne of {s56}.", 0),
##         (add_troop_note_tableau_mesh, ":troop_no", "tableau_troop_note_mesh"),
##       (else_try),
##         (str_clear, s54),
##         (add_troop_note_from_sreg, ":troop_no", 0, s54, 0),
##         (add_troop_note_from_sreg, ":troop_no", 1, s54, 0),
##         (add_troop_note_from_sreg, ":troop_no", 2, s54, 0),
##       (try_end),
##     (else_try),
##       (faction_get_slot, ":faction_leader", ":troop_faction", slot_faction_leader),
##       (str_store_troop_name_link, s55, ":faction_leader"),
##       (str_store_faction_name_link, s56, ":troop_faction"),
##       (assign, ":troop_is_player_faction", 0),
##       (assign, ":troop_is_faction_leader", 0),
##       (try_begin),
##         (eq, ":troop_faction", "fac_player_faction"),
##         (assign, ":troop_is_player_faction", 1),
##       (else_try),
##         (eq, ":faction_leader", ":troop_no"),
##         (assign, ":troop_is_faction_leader", 1),
##       (try_end),
##       (assign, ":num_centers", 0),
##       (str_store_string, s58, "@nowhere"),
##       (try_for_range_backwards, ":cur_center", centers_begin, centers_end),
##         (party_slot_eq, ":cur_center", slot_town_lord, ":troop_no"),
##         (try_begin),
##           (eq, ":num_centers", 0),
##           (str_store_party_name_link, s58, ":cur_center"),
##         (else_try),
##           (eq, ":num_centers", 1),
##           (str_store_party_name_link, s57, ":cur_center"),
##           (str_store_string, s58, "@{s57} and {s58}"),
##         (else_try),
##           (str_store_party_name_link, s57, ":cur_center"),
##           (str_store_string, s58, "@{!}{s57}, {s58}"),
##         (try_end),
##         (val_add, ":num_centers", 1),
##       (try_end),
##       (troop_get_type, reg3, ":troop_no"),
##       (troop_get_slot, reg5, ":troop_no", slot_troop_renown),
##       (str_clear, s59),
##       (try_begin),
###         (troop_get_slot, ":relation", ":troop_no", slot_troop_player_relation),
##         (call_script, "script_troop_get_player_relation", ":troop_no"),
##         (assign, ":relation", reg0),
##         (store_add, ":normalized_relation", ":relation", 100),
##         (val_add, ":normalized_relation", 5),
##         (store_div, ":str_offset", ":normalized_relation", 10),
##         (val_clamp, ":str_offset", 0, 20),
##         (store_add, ":str_id", "str_relation_mnus_100_ns",  ":str_offset"),
##         (neq, ":str_id", "str_relation_plus_0_ns"),
##         (str_store_string, s60, "@{reg3?She:He}"),
##         (str_store_string, s59, ":str_id"),
##         (str_store_string, s59, "@{!}^{s59}"),
##       (try_end),
##
##	#lord recruitment changes begin
##	#This sends a bunch of political information to s47. 
##	
##
##
##	   
##	    #refresh registers
##        (assign, reg9, ":num_centers"),
##        (troop_get_type, reg3, ":troop_no"),
##        (troop_get_slot, reg5, ":troop_no", slot_troop_renown),
##		(assign, reg4, ":troop_is_faction_leader"),
##		(assign, reg6, ":troop_is_player_faction"),
##		
##        (add_troop_note_from_sreg, ":troop_no", 0, "str_reg6reg4s54_is_the_ruler_of_s56_s54_is_a_vassal_of_s55_of_s56_renown_reg5_reg9reg3shehe_is_the_reg3ladylord_of_s58reg3shehe_has_no_fiefss59_s49", 0),
##	#lord recruitment changes end
##
##        (add_troop_note_tableau_mesh, ":troop_no", "tableau_troop_note_mesh"),
##     (try_end),
     ]),
  #script_update_troop_location_notes
  # INPUT: troop_no
  # OUTPUT: none
  ("update_troop_location_notes",
    [
      (store_script_param, ":troop_no", 1),
      (store_script_param, ":see_or_hear", 2),      
      (try_begin),
        (call_script, "script_get_information_about_troops_position", ":troop_no", 1),
        (neq, reg0, 0),       
        
        (call_script, "script_search_troop_prisoner_of_party", ":troop_no"),
        (eq, reg0, -1),
        ##diplomacy start+ use gender script
	    #(troop_get_type, reg1, ":troop_no"),
		(call_script, "script_dplmc_store_troop_is_female", ":troop_no"),
		(assign, reg1, reg0),
		##diplomacy end+    
        (try_begin),
          (eq, ":see_or_hear", 0),
          (add_troop_note_from_sreg, ":troop_no", 2, "@The last time you saw {reg1?her:him}, {s1}", 1),
        (else_try),
          (add_troop_note_from_sreg, ":troop_no", 2, "@The last time you heard about {reg1?her:him}, {s1}", 1),
        (try_end),
      (try_end),
     ]),
  #script_update_troop_location_notes_prisoned
  # INPUT: troop_no
  # OUTPUT: none
  ("update_troop_location_notes_prisoned",
    [
      (store_script_param, ":troop_no", 1),
      (store_script_param, ":capturer_faction_no", 2),
      ##diplomacy start+ use gender script
      #(troop_get_type, reg1, ":troop_no"),
	  (call_script, "script_dplmc_store_troop_is_female", ":troop_no"),
      (assign, reg1, reg0),
	  ##diplomacy end+  
      (str_store_faction_name_link, s1, ":capturer_faction_no"),
       
      (add_troop_note_from_sreg, ":troop_no", 2, "str_reg1shehe_is_prisoner_of_s1", 1),
    ]),
  ("update_troop_political_notes",
      [
		(store_script_param, ":troop_no", 1),
		(try_begin),
		    (str_clear, s47),

			(store_faction_of_troop, ":troop_faction", ":troop_no"),

		    (faction_get_slot, ":faction_leader", ":troop_faction", slot_faction_leader),

		    (str_clear, s40),
		    (assign, ":logged_a_rivalry", 0),
		    (try_for_range, ":kingdom_hero", active_npcs_begin, active_npcs_end),
				(call_script, "script_troop_get_relation_with_troop", ":troop_no", ":kingdom_hero"),
				(lt, reg0, -10),
				
		   		(str_store_troop_name_link, s39, ":kingdom_hero"),
				(try_begin),
					(eq, ":logged_a_rivalry", 0),
					(str_store_string, s40, "str_s39_rival"),
					(assign, ":logged_a_rivalry", 1),
				(else_try),
					(str_store_string, s41, "str_s40"),
					(str_store_string, s40, "str_s41_s39_rival"),
				(try_end),
		   
		    (try_end),

		    (str_clear, s46),
		    (try_begin),
				(ge, "$cheat_mode", 1),
				(try_begin),
					(troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_martial),
					(str_store_string, s46, "str_reputation_cheat_mode_only_martial_"),
				(else_try),	
					(troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_debauched),
					(str_store_string, s46, "str_reputation_cheat_mode_only_debauched_"),
				(else_try),	
					(troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_selfrighteous),
					(str_store_string, s46, "str_reputation_cheat_mode_only_pitiless_"),
				(else_try),	
					(troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_cunning),
					(str_store_string, s46, "str_reputation_cheat_mode_only_calculating_"),
				(else_try),	
					(troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_quarrelsome),
					(str_store_string, s46, "str_reputation_cheat_mode_only_quarrelsome_"),
				(else_try),	
					(troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_goodnatured),
					(str_store_string, s46, "str_reputation_cheat_mode_only_goodnatured_"),
				(else_try),	
					(troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_upstanding),
					(str_store_string, s46, "str_reputation_cheat_mode_only_upstanding_"),
				(else_try),
					(troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_conventional),
					(str_store_string, s46, "str_reputation_cheat_mode_only_conventional_"),
				(else_try),
					(troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_adventurous),
					(str_store_string, s46, "str_reputation_cheat_mode_only_adventurous_"),
				(else_try),
					(troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_otherworldly),
					(str_store_string, s46, "str_reputation_cheat_mode_only_romantic_"),
				(else_try),
					(troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_moralist),
					(str_store_string, s46, "str_reputation_cheat_mode_only_moralist_"),
				(else_try),
					(troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_ambitious),
					(str_store_string, s46, "str_reputation_cheat_mode_only_ambitious_"),
				(else_try),	
					(troop_get_slot, reg11, ":troop_no", slot_lord_reputation_type),
					(str_store_string, s46, "str_reputation_cheat_mode_only_reg11_"),
				(try_end),

				(try_begin),
					(eq, "$cheat_mode", 1),
					(try_for_range, ":love_interest_slot", slot_troop_love_interest_1, slot_troop_love_interests_end),
						(troop_get_slot, ":love_interest", ":troop_no", ":love_interest_slot"),
						(is_between, ":love_interest", kingdom_ladies_begin, kingdom_ladies_end),
						(str_store_troop_name_link, s39, ":love_interest"),
						(call_script, "script_troop_get_relation_with_troop", ":troop_no", ":love_interest"),
						(str_store_string, s2, "str_love_interest"),
						(try_begin),
							(troop_slot_eq, ":troop_no", slot_troop_betrothed, ":love_interest"),
							(str_store_string, s2, "str_betrothed"),
						(try_end),
						(str_store_string, s40, "str_s40_s39_s2_reg0"),
					(try_end),
				(try_end),
				
		    (try_end),
			
		    (str_store_string, s45, "str_other_relations_s40_"),

		    (str_clear, s44),
		    (try_begin),
				(neq, ":troop_no", ":faction_leader"),
				(call_script, "script_troop_get_relation_with_troop", ":troop_no", ":faction_leader"),
				(str_store_string, s44, "str_relation_with_liege_reg0_"),
		    (try_end),

			(str_clear, s48),

		    (try_begin),
				(eq, "$cheat_mode", 1),
				(store_current_hours, ":hours"),
				(gt, ":hours", 0),
#				(display_message, "@{!}Updating political factors"),
				(call_script, "script_calculate_troop_political_factors_for_liege", ":troop_no", ":faction_leader"),
				(str_store_string, s48, "str_sense_of_security_military_reg1_court_position_reg3_"),
			(try_end),
			(str_store_string, s47, "str_s46s45s44s48"),

			(add_troop_note_from_sreg, ":troop_no", 3, "str_political_details_s47_", 1),

		(try_end),	 
    ]),
  #script_update_center_notes
  # INPUT: center_no
  # OUTPUT: none
  ("update_center_notes",
    [
##      (store_script_param, ":center_no", 1),
##
##     (party_get_slot, ":lord_troop", ":center_no", slot_town_lord),
##     (try_begin),
##       (ge, ":lord_troop", 0),
##       (store_troop_faction, ":lord_faction", ":lord_troop"),
##       (str_store_troop_name_link, s1, ":lord_troop"),
##       (try_begin),
##         (eq, ":lord_troop", "trp_player"),
##         (gt, "$players_kingdom", 0),
##         (str_store_faction_name_link, s2, "$players_kingdom"),
##       (else_try),
##         (str_store_faction_name_link, s2, ":lord_faction"),
##       (try_end),
##       (str_store_party_name, s50, ":center_no"),
##       (try_begin),
##         (party_slot_eq, ":center_no", slot_party_type, spt_town),
##         (str_store_string, s51, "@The town of {s50}"),
##       (else_try),
##         (party_slot_eq, ":center_no", slot_party_type, spt_village),
##         (party_get_slot, ":bound_center", ":center_no", slot_village_bound_center),
##         (str_store_party_name_link, s52, ":bound_center"),
##         (str_store_string, s51, "@The village of {s50} near {s52}"),
##       (else_try),
##         (str_store_string, s51, "@{!}{s50}"),
##       (try_end),
##       (str_store_string, s2, "@{s51} belongs to {s1} of {s2}.^"),
##     (else_try),
##       (str_clear, s2),
##     (try_end),
##     (try_begin),
##       (is_between, ":center_no", villages_begin, villages_end),
##     (else_try),
##       (assign, ":num_villages", 0),
##       (try_for_range_backwards, ":village_no", villages_begin, villages_end),
##         (party_slot_eq, ":village_no", slot_village_bound_center, ":center_no"),
##         (try_begin),
##           (eq, ":num_villages", 0),
##           (str_store_party_name_link, s8, ":village_no"),
##         (else_try),
##           (eq, ":num_villages", 1),
##           (str_store_party_name_link, s7, ":village_no"),
##           (str_store_string, s8, "@{s7} and {s8}"),
##         (else_try),
##           (str_store_party_name_link, s7, ":village_no"),
##           (str_store_string, s8, "@{!}{s7}, {s8}"),
##         (try_end),
##         (val_add, ":num_villages", 1),
##       (try_end),
##       (try_begin),
##         (eq, ":num_villages", 0),
##         (str_store_string, s2, "@{s2}It has no villages.^"),
##       (else_try),
##         (store_sub, reg0, ":num_villages", 1),
##         (str_store_string, s2, "@{s2}{reg0?Its villages are:Its village is} {s8}.^"),
##       (try_end),
##     (try_end),
##     (call_script, "script_get_prosperity_text_to_s50", ":center_no"),
##     (add_party_note_from_sreg, ":center_no", 0, "@{s2}Its prosperity is: {s50}", 0),
##     (add_party_note_tableau_mesh, ":center_no", "tableau_center_note_mesh"),
     ]),
  #script_update_center_recon_notes
  # INPUT: center_no
  # OUTPUT: none
  ("update_center_recon_notes",
    [(store_script_param, ":center_no", 1),
     (try_begin),
       (this_or_next|is_between, ":center_no", towns_begin, towns_end),
       (is_between, ":center_no", castles_begin, castles_end),
       (party_get_slot, ":center_food_store", ":center_no", slot_party_food_store),
       (call_script, "script_center_get_food_consumption", ":center_no"),
       (assign, ":food_consumption", reg0),
       (store_div, reg6, ":center_food_store", ":food_consumption"),
       (party_collect_attachments_to_party, ":center_no", "p_collective_ally"),
       (party_get_num_companions, reg5, "p_collective_ally"),
       (add_party_note_from_sreg, ":center_no", 1, "@Current garrison consists of {reg5} men.^Has food stock for {reg6} days.", 1),
     (try_end),
     ]),
  #script_update_all_notes
  # INPUT: none
  # OUTPUT: none
  ("update_all_notes",
    [
      (call_script, "script_update_troop_notes", "trp_player"),
      (try_for_range, ":troop_no", active_npcs_begin, active_npcs_end),
	    (this_or_next|troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
	    (this_or_next|troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_lady),
			(troop_slot_eq, ":troop_no", slot_troop_occupation, slto_inactive_pretender),
        (call_script, "script_update_troop_notes", ":troop_no"),
      (try_end),
      (try_for_range, ":center_no", centers_begin, centers_end),
        (call_script, "script_update_center_notes", ":center_no"),
      (try_end),
      (try_for_range, ":faction_no", kingdoms_begin, kingdoms_end),
        (call_script, "script_update_faction_notes", ":faction_no"),
      (try_end),
    ]),
  #script_spawn_bandits
  # INPUT: none
  # OUTPUT: none
  ("spawn_bandits",
    [
     (set_spawn_radius,1),
	
	 (try_begin),
		(eq, "$cheat_mode", 1),
		(display_message, "@{!}DEBUG : Doing spawn bandit script"),
	 (try_end),
	 
	 (party_template_set_slot, "pt_seto_pirates", slot_party_template_lair_type, "pt_seto_pirate_lair"),
	 (party_template_set_slot, "pt_kanto_rebels", slot_party_template_lair_type, "pt_kanto_rebel_lair"),
	 (party_template_set_slot, "pt_woku_pirates", slot_party_template_lair_type, "pt_woku_pirate_lair"),
	 (party_template_set_slot, "pt_shinano_rebels", slot_party_template_lair_type, "pt_shinano_rebel_lair"),
	 (party_template_set_slot, "pt_kinai_rebels", slot_party_template_lair_type, "pt_kinai_rebel_lair"),
	 (party_template_set_slot, "pt_northern_raiders", slot_party_template_lair_type, "pt_kinai_rebel_lair"),
	 #gekokujo 3.0 new bandit types
     (party_template_set_slot, "pt_manhunters", slot_party_template_lair_type, "pt_kinai_rebel_lair"),
	 (party_template_set_slot, "pt_monk_rebels", slot_party_template_lair_type, "pt_monk_rebel_lair"),
     (party_template_set_slot, "pt_manhunters", slot_party_template_lair_spawnpoint, "p_kinai_osaka_spawn_point"),
	 (party_template_set_slot, "pt_seto_pirates", slot_party_template_lair_spawnpoint, "p_kinai_osaka_spawn_point"),
	 (party_template_set_slot, "pt_kanto_rebels", slot_party_template_lair_spawnpoint, "p_kanto_rebel_spawn_point"),
     (party_template_set_slot, "pt_woku_pirates", slot_party_template_lair_spawnpoint, "p_monk_rebel_spawn_point"),
	 (party_template_set_slot, "pt_shinano_rebels", slot_party_template_lair_spawnpoint, "p_kinai_rebel_spawn_point"),
     (party_template_set_slot, "pt_shinano_rebels", slot_party_template_lair_spawnpoint, "p_kinai_osaka_spawn_point"),
	 (party_template_set_slot, "pt_kinai_rebels", slot_party_template_lair_spawnpoint, "p_kinai_rebel_spawn_point"),
	 (party_template_set_slot, "pt_northern_raiders", slot_party_template_lair_spawnpoint, "p_northern_raider_spawn_point"),

	 #gekokujo 3.0 new bandit types
	 (party_template_set_slot, "pt_monk_rebels", slot_party_template_lair_spawnpoint, "p_monk_rebel_spawn_point"),
     
     #gekokujo 3.1 bandits spawn proportionally to factions start
     #get a count of how many factions are active and base all spawn numbers on it
     (assign, ":num_active_factions", 0),
     (try_for_range, ":cur_kingdom", kingdoms_begin, kingdoms_end),
       (faction_slot_eq, ":cur_kingdom", slot_faction_state, sfs_active),
       (val_add, ":num_active_factions", 1),
     (try_end),
     
     (store_add, ":bandit_count", ":num_active_factions", 4), #normal bandits have 5-24 each
     (try_begin),
       (eq, "$g_gekokujo_bandit_reduction", 1),
       (val_div, ":bandit_count", 2), #2-12 with bandit reduction
     (try_end),
     
     (store_mul, ":looter_count", ":num_active_factions", 2), #looters have 25-63
     (val_add, ":looter_count", 23),
     (try_begin),
       (eq, "$g_gekokujo_bandit_reduction", 1),
       (val_div, ":looter_count", 2), #12-32 with bandit reduction
     (try_end),
     #gekokujo 3.1 bandits spawn proportionally to factions end
     
     (try_begin),
       (store_num_parties_of_template, ":num_parties", "pt_woku_pirates"),
	   #gekokujo 3.0 increase bandit count
       #(lt,":num_parties",16), #was 14 at mount&blade, 18 in warband, 16 last decision
       #(lt,":num_parties",24),
       (lt,":num_parties", ":bandit_count"), #gekokuko 3.1 bandits spawn proportionately to factions
       (store_random,":spawn_point",num_woku_pirate_spawn_points),
       (val_add,":spawn_point","p_woku_pirate_spawn_point"),
	   #gekokujo 3.0 increase bandit spawn area
       #(set_spawn_radius, 25),
       (set_spawn_radius, 35),
       (spawn_around_party,":spawn_point","pt_woku_pirates"),
	   #gekokujo 3.0 microfactions! start
	   #let's piggyback and spawn some woku pirates in tsushima (if it's not captured and is active)
	   (try_begin),
	     (party_slot_eq, "p_fort_2", slot_fort_captured, 0), #not captured
	     (party_slot_eq, "p_fort_2", slot_fort_timer, 0), #not disabled
         (set_spawn_radius, 16),
         (spawn_around_party,"p_fort_2","pt_woku_pirates"),
	   (try_end),
	   #gekokujo 3.0 microfactions! end
     (try_end),
     (try_begin),
       (store_num_parties_of_template, ":num_parties", "pt_shinano_rebels"),
	   #gekokujo 3.0 increase bandit count
       #(lt,":num_parties",16), #was 14 at mount&blade, 18 in warband, 16 last decision
       #(lt,":num_parties",24),
       (lt,":num_parties", ":bandit_count"), #gekokuko 3.1 bandits spawn proportionately to factions
       (store_random,":spawn_point",num_shinano_rebel_spawn_points),
       (val_add,":spawn_point","p_shinano_rebel_spawn_point"),
	   #gekokujo 3.0 increase bandit spawn area
       #(set_spawn_radius, 25),
       (set_spawn_radius, 35),
       (spawn_around_party,":spawn_point","pt_shinano_rebels"),
     (try_end),
     (try_begin),
       (store_num_parties_of_template, ":num_parties", "pt_kinai_rebels"),
	   #gekokujo 3.0 increase bandit count
       #(lt,":num_parties",16), #was 14 at mount&blade, 18 in warband, 16 last decision
       #(lt,":num_parties",24),
       (lt,":num_parties", ":bandit_count"), #gekokuko 3.1 bandits spawn proportionately to factions
       (store_random,":spawn_point",num_kinai_rebel_spawn_points),
       (val_add,":spawn_point","p_kinai_rebel_spawn_point"),
	   #gekokujo 3.0 increase bandit spawn area
       #(set_spawn_radius, 25),
       (set_spawn_radius, 35),
       (spawn_around_party,":spawn_point","pt_kinai_rebels"),
     (try_end),
     (try_begin),
       (store_num_parties_of_template, ":num_parties", "pt_seto_pirates"),
	   #gekokujo 3.0 increase bandit count
       #(lt,":num_parties",16), #was 14 at mount&blade, 18 in warband, 16 last decision
       #(lt,":num_parties",24),
       (lt,":num_parties", ":bandit_count"), #gekokuko 3.1 bandits spawn proportionately to factions
       (store_random,":spawn_point",num_seto_pirate_spawn_points),
       (val_add,":spawn_point","p_seto_pirate_spawn_point"),
	   #gekokujo 3.0 increase bandit spawn area
       #(set_spawn_radius, 25),
       (set_spawn_radius, 35),
       (spawn_around_party,":spawn_point","pt_seto_pirates"),
     (try_end),
     (try_begin),
       (store_num_parties_of_template, ":num_parties", "pt_kanto_rebels"),
	   #gekokujo 3.0 increase bandit count
       #(lt,":num_parties",16), #was 14 at mount&blade, 18 in warband, 16 last decision
       #(lt,":num_parties",24),
       (lt,":num_parties", ":bandit_count"), #gekokuko 3.1 bandits spawn proportionately to factions
       (store_random,":spawn_point",num_kanto_rebel_spawn_points),
       (val_add,":spawn_point","p_kanto_rebel_spawn_point"),
	   #gekokujo 3.0 increase bandit spawn area
       #(set_spawn_radius, 25),
       (set_spawn_radius, 35),
       (spawn_around_party,":spawn_point","pt_kanto_rebels"),
     (try_end),
     (try_begin),
       (store_num_parties_of_template, ":num_parties", "pt_northern_raiders"),
	   #gekokujo 3.0 increase bandit count
       #(lt,":num_parties",16), #was 14 at mount&blade, 18 in warband, 16 last decision
       #(lt,":num_parties",24),
       (lt,":num_parties", ":bandit_count"), #gekokuko 3.1 bandits spawn proportionately to factions
       #(store_random,":spawn_point",num_northern_raider_spawn_points), #gekokujo 3.0 microfactions! let's disable northern raiders outside of hideouts and forts entirely
       #(val_add,":spawn_point","p_northern_raider_spawn_point"), #gekokujo 3.0 microfactions! let's disable northern raiders outside of hideouts and forts entirely
	   #gekokujo 3.0 increase bandit spawn area
       #(set_spawn_radius, 25),
       #(set_spawn_radius, 50), #gekokujo 3.0 microfactions! let's disable northern raiders outside of hideouts and forts entirely
       #(spawn_around_party,":spawn_point","pt_northern_raiders"), #gekokujo 3.0 microfactions! let's disable northern raiders outside of hideouts and forts entirely
	   #gekokujo 3.0 microfactions! start
	   #let's piggyback and spawn some ezo warriors in niputay and otasut separately
	   (try_begin),
	     (party_slot_eq, "p_fort_5", slot_fort_captured, 0), #not captured
	     (party_slot_eq, "p_fort_5", slot_fort_timer, 0), #not disabled
         (set_spawn_radius, 24),
         (spawn_around_party,"p_fort_5","pt_northern_raiders"),
	   (try_end),
	   (try_begin),
	     (party_slot_eq, "p_fort_6", slot_fort_captured, 0), #not captured
	     (party_slot_eq, "p_fort_6", slot_fort_timer, 0), #not disabled
         (set_spawn_radius, 24),
         (spawn_around_party,"p_fort_6","pt_northern_raiders"),
	   (try_end),
	   #gekokujo 3.0 microfactions! end
     (try_end),
	 #gekokujo 3.0 new bandit types start
     (try_begin),
       (store_num_parties_of_template, ":num_parties", "pt_monk_rebels"),
       #(lt,":num_parties",24), #was 14 at mount&blade, 18 in warband, 16 last decision
       (lt,":num_parties", ":bandit_count"), #gekokuko 3.1 bandits spawn proportionately to factions
       (store_random,":spawn_point",num_monk_rebel_spawn_points),
       (val_add,":spawn_point","p_monk_rebel_spawn_point"),
       (set_spawn_radius, 35),
       (spawn_around_party,":spawn_point","pt_monk_rebels"),
	   #gekokujo 3.0 microfactions! start
	   #let's piggyback and spawn some monk rebels in kokawa-dera and mii-dera separately
	   (try_begin),
	     (party_slot_eq, "p_fort_3", slot_fort_captured, 0), #not captured
	     (party_slot_eq, "p_fort_3", slot_fort_timer, 0), #not disabled
         (set_spawn_radius, 12),
         (spawn_around_party,"p_fort_3","pt_monk_rebels"),
	   (try_end),
	   (try_begin),
	     (party_slot_eq, "p_fort_4", slot_fort_captured, 0), #not captured
	     (party_slot_eq, "p_fort_4", slot_fort_timer, 0), #not disabled
         (set_spawn_radius, 12),
         (spawn_around_party,"p_fort_4","pt_monk_rebels"),
	   (try_end),
	   #gekokujo 3.0 microfactions! end
     (try_end),
	 #gekokujo 3.0 new bandit types end
     (try_begin),
       (store_num_parties_of_template, ":num_parties", "pt_looters"),
	   #gekokujo 3.0 increase looter spawns proportionally to new village count
       #(lt,":num_parties",42), #was 33 at mount&blade, 50 in warband, 42 last decision
	   #(lt,":num_parties",63),
       (lt,":num_parties", ":looter_count"), #gekokuko 3.1 bandits spawn proportionately to factions
       (store_random_in_range,":spawn_point",villages_begin,villages_end), #spawn looters twice to have lots of them at the beginning       
	   #gekokujo 3.0 increase bandit spawn area
       #(set_spawn_radius, 25),
       (set_spawn_radius, 35),
       (spawn_around_party,":spawn_point","pt_looters"),
       (assign, ":spawned_party_id", reg0),
       (try_begin),
         (check_quest_active, "qst_deal_with_looters"),
         (party_set_flags, ":spawned_party_id", pf_quest_party, 1),
       (else_try),
         (party_set_flags, ":spawned_party_id", pf_quest_party, 0),
       (try_end),
	   #gekokujo 3.0 microfactions! start
	   #let's piggyback and spawn some looters in sado (if it's not captured and is active)
	   (try_begin),
	     (party_slot_eq, "p_fort_1", slot_fort_captured, 0), #not captured
	     (party_slot_eq, "p_fort_1", slot_fort_timer, 0), #not disabled
         (set_spawn_radius, 16),
         (spawn_around_party,"p_fort_1","pt_looters"),
         (assign, ":spawned_party_id", reg0),
		 (party_set_flags, ":spawned_party_id", pf_quest_party, 0),
	   (try_end),
	   #gekokujo 3.0 microfactions! end
     (try_end),
     (try_begin),
       (store_num_parties_of_template, ":num_parties", "pt_deserters"),
	   #gekokujo 3.0 increase deserter spawns proportionally to new castle & faction count
       #(lt,":num_parties",15),
	   #(lt,":num_parties",24),
       (lt,":num_parties", ":bandit_count"), #gekokuko 3.1 bandits spawn proportionately to factions
	   #gekokujo 3.0 increase bandit spawn area
       #(set_spawn_radius, 4),
       (set_spawn_radius, 8),
       (try_for_range, ":troop_no", active_npcs_begin, active_npcs_end),
	     (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
         (store_random_in_range, ":random_no", 0, 100),
         (lt, ":random_no", 5),
         (troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
         (store_troop_faction, ":troop_faction", ":troop_no"),
         (neq, ":troop_faction", "fac_player_supporters_faction"),
         (gt, ":party_no", 0),
         (neg|party_is_in_any_town, ":party_no"),
##         (party_get_attached_to, ":attached_party_no", ":party_no"),
##         (lt, ":attached_party_no", 0),#in wilderness
         (spawn_around_party, ":party_no", "pt_deserters"),
         (assign, ":new_party", reg0),
         (store_troop_faction, ":faction_no", ":troop_no"),
		 #gekokujo 3.0 allow ashigaru deserters to spawn (2/3 chance) start
         #(faction_get_slot, ":tier_1_troop", ":faction_no", slot_faction_tier_1_troop),
		 (store_random_in_range, ":deserter_seed", 0, 6),
		 (try_begin),
		   (eq, ":deserter_seed", 0),
		   (faction_get_slot, ":tier_1_troop", ":faction_no", slot_faction_tier_1_troop),
		 (else_try),
		   (eq, ":deserter_seed", 1),
		   (try_begin),
		     #for ikko ikki troops, have samurai deserters instead
		     (eq, ":faction_no", "fac_kingdom_20"),
			 (assign, ":tier_1_troop", "trp_gekokujo_ikko_jizamurai"),
		   (else_try),
		     (faction_get_slot, ":tier_1_troop", ":faction_no", slot_faction_tier_1_troop),
		   (try_end),
		 (else_try),
		   (faction_get_slot, ":tier_1_troop", ":faction_no", slot_faction_tier_0_troop),
		 (try_end),
		 #gekokujo 3.0 allow ashigaru deserters to spawn (2/3 chance) end
         (store_character_level, ":level", "trp_player"),
         (store_mul, ":max_number_to_add", ":level", 2),
         (val_add, ":max_number_to_add", 11),
         (store_random_in_range, ":number_to_add", 10, ":max_number_to_add"),
         (party_add_members, ":new_party", ":tier_1_troop", ":number_to_add"),
         (store_random_in_range, ":random_no", 1, 4),
         (try_for_range, ":unused", 0, ":random_no"),
           (party_upgrade_with_xp, ":new_party", 1000000, 0),
         (try_end),
##         (str_store_party_name, s1, ":party_no"),
##         (call_script, "script_get_closest_center", ":party_no"),
##         (try_begin),
##           (gt, reg0, 0),
##           (str_store_party_name, s2, reg0),
##         (else_try),
##           (str_store_string, s2, "@unknown place"),
##         (try_end),
##         (assign, reg1, ":number_to_add"),
##         (display_message, "@{reg1} Deserters spawned from {s1}, near {s2}."),
       (try_end),
     (try_end), #deserters ends
	 
	 
	 #Spawn bandit lairs
	(try_for_range, ":bandit_template", "pt_seto_pirates", "pt_deserters"),
		(party_template_get_slot, ":bandit_lair_party", ":bandit_template", slot_party_template_lair_party),
		(le, ":bandit_lair_party", 1),
		
		(party_template_get_slot, ":bandit_lair_template", ":bandit_template", slot_party_template_lair_type),
		(party_template_get_slot, ":bandit_lair_template_spawnpoint", ":bandit_template", slot_party_template_lair_spawnpoint),
	 
		#(set_spawn_radius, 20), #gekokujo 3.0 increase bandit camp spawn area
		(set_spawn_radius, 30),
	 
        (spawn_around_party, ":bandit_lair_template_spawnpoint", ":bandit_lair_template"),
		(assign, ":new_camp", reg0),
		
		(party_set_slot, ":new_camp", slot_party_type, spt_bandit_lair),
		
		(str_store_party_name, s4, ":new_camp"),
		
		(party_get_position, pos4, ":new_camp"),
        #(party_set_flags, ":new_camp", pf_icon_mask, 1),
		
		(party_get_current_terrain, ":new_camp_terrain", ":new_camp"),
		#(position_get_z, ":elevation", pos4), #gekokujo 3.0 deprecated
		#(position_get_y, ":lair_y", pos4), #gekokujo 3.0 deprecated
								
		(assign, ":center_too_close", 0),
		(try_for_range, ":center", centers_begin, centers_end),
			(eq, ":center_too_close", 0),
			(store_distance_to_party_from_party, ":distance", ":new_camp", ":center"),
			(lt, ":distance", 3),
			(assign, ":center_too_close", 1),
		(try_end),
						
		(try_begin),
			(eq, ":center_too_close", 1),
			(party_is_active, ":new_camp"),
			(remove_party, ":new_camp"),
			(party_template_set_slot, ":bandit_template", slot_party_template_lair_party, 0),
	    #gekokujo 3.0 allow all bandit camps to spawn everywhere start
		#(else_try),
		#	(eq, ":bandit_template", "pt_kinai_rebels"),
		#	(eq, ":new_camp_terrain", 3),
		#	(map_get_water_position_around_position, pos5, pos4, 4),			
		#	(party_template_set_slot, ":bandit_template", slot_party_template_lair_party, ":new_camp"),
		#	(party_set_flags, ":new_camp", pf_disabled, 1),			
		#(else_try),	
		#	(eq, ":bandit_template", "pt_woku_pirates"),
		#	(eq, ":new_camp_terrain", 3),
		#	(gt, ":elevation", 250),			
		#	(party_template_set_slot, ":bandit_template", slot_party_template_lair_party, ":new_camp"),
		#	(party_set_flags, ":new_camp", pf_disabled, 1),			
		#(else_try),
		#	(eq, ":bandit_template", "pt_northern_raiders"),
		#	(eq, ":new_camp_terrain", 5),
		#	(gt, ":lair_y", -9000),
		#	(gt, ":elevation", 125),
		#	(party_template_set_slot, ":bandit_template", slot_party_template_lair_party, ":new_camp"),
		#	(party_set_flags, ":new_camp", pf_disabled, 1),			
		#(else_try),	
		#	(eq, ":bandit_template", "pt_seto_pirates"),
		#	(this_or_next|eq, ":new_camp_terrain", 2),
		#	(eq, ":new_camp_terrain", 10),
		#	(this_or_next|eq, ":new_camp_terrain", 10),
		#	(gt, ":elevation", 200),
		#	(party_template_set_slot, ":bandit_template", slot_party_template_lair_party, ":new_camp"),
		#	(party_set_flags, ":new_camp", pf_disabled, 1),			
		#(else_try),	
		#	(eq, ":bandit_template", "pt_kanto_rebels"),
		#	(eq, ":new_camp_terrain", 12),				
		#	(party_template_set_slot, ":bandit_template", slot_party_template_lair_party, ":new_camp"),
		#	(party_set_flags, ":new_camp", pf_disabled, 1),
		#(else_try),	
		#	(eq, ":bandit_template", "pt_shinano_rebels"),
		#	(eq, ":new_camp_terrain", 11),			
		#	(party_template_set_slot, ":bandit_template", slot_party_template_lair_party, ":new_camp"),
		#	(party_set_flags, ":new_camp", pf_disabled, 1),		
		(else_try),	
			(this_or_next|eq, ":bandit_template", "pt_kinai_rebels"),
			(this_or_next|eq, ":bandit_template", "pt_woku_pirates"),
			(this_or_next|eq, ":bandit_template", "pt_northern_raiders"),
			(this_or_next|eq, ":bandit_template", "pt_seto_pirates"),
			(this_or_next|eq, ":bandit_template", "pt_kanto_rebels"),
			(this_or_next|eq, ":bandit_template", "pt_shinano_rebels"),
			(this_or_next|eq, ":bandit_template", "pt_monk_rebels"),
			(this_or_next|eq, ":bandit_template", "pt_jianhuizu"),
			(this_or_next|eq, ":new_camp_terrain", 3), #plains		
			(this_or_next|eq, ":new_camp_terrain", 4), #snow
			(this_or_next|eq, ":new_camp_terrain", 11), #forest
			(eq, ":new_camp_terrain", 12), #snow forest
			
			(party_template_set_slot, ":bandit_template", slot_party_template_lair_party, ":new_camp"),
			(party_set_flags, ":new_camp", pf_disabled, 1),		
	    #gekokujo 3.0 allow all bandit camps to spawn everywhere end
		(else_try),
			(party_is_active, ":new_camp"),
			(str_store_party_name, s4, ":new_camp"),
			(remove_party, ":new_camp"),
			(party_template_set_slot, ":bandit_template", slot_party_template_lair_party, 0),
		(else_try),
		(try_end),	 	 
	(try_end),
     ]),
  # script_calculate_amount_of_cattle_can_be_stolen
  # Input: arg1 = village_no
  # Output: reg0 = max_amount
  ("calculate_amount_of_cattle_can_be_stolen",
    [
      (store_script_param, ":village_no", 1),
      (call_script, "script_get_max_skill_of_player_party", "skl_looting"),
      (assign, ":max_skill", reg0),
      (store_mul, ":can_steal", ":max_skill", 2),
      (call_script, "script_party_count_fit_for_battle", "p_main_party"),
      (store_add, ":num_men_effect", reg0, 10),
      (val_div, ":num_men_effect", 10),
      (val_add, ":can_steal", ":num_men_effect"),
      (party_get_slot, ":num_cattle", ":village_no", slot_village_number_of_cattle),
      (val_min, ":can_steal", ":num_cattle"),
      (assign, reg0, ":can_steal"),
     ]),
  # script_get_next_active_kingdom
  # Input: arg1 = faction_no
  # Output: reg0 = faction_no (does not choose player faction)
  ("get_next_active_kingdom",
    [
      (store_script_param, ":faction_no", 1),
      (assign, ":end_cond", kingdoms_end),
      (try_for_range, ":unused", kingdoms_begin, ":end_cond"),
        (val_add, ":faction_no", 1),
        (try_begin),
          (ge, ":faction_no", kingdoms_end),
          (assign, ":faction_no", kingdoms_begin),
        (try_end),
        (faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
        (neq, ":faction_no", "fac_player_supporters_faction"),
        (assign, ":end_cond", 0),
      (try_end),
      (assign, reg0, ":faction_no"),
     ]),
  # script_remove_cattles_if_herd_is_close_to_party
  # Input: arg1 = party_no, arg2 = maximum_number_of_cattles_required
  # Output: reg0 = number_of_cattles_removed
  ("remove_cattles_if_herd_is_close_to_party",
    [
      (store_script_param, ":party_no", 1),
      (store_script_param, ":max_req", 2),
      (assign, ":cur_req", ":max_req"),
      (try_for_parties, ":cur_party"),
        (gt, ":cur_req", 0),
        (party_slot_eq, ":cur_party", slot_party_type, spt_cattle_herd),
        (store_distance_to_party_from_party, ":dist", ":cur_party", ":party_no"),
        (lt, ":dist", 3),
		
        #Do not use the quest herd for "move cattle herd"
        (assign, ":subcontinue", 1),
        (try_begin),
          (check_quest_active, "qst_move_cattle_herd"),
          (quest_slot_eq, "qst_move_cattle_herd", slot_quest_target_party, ":cur_party"),
          (assign, ":subcontinue", 0),
        (try_end),
        (eq, ":subcontinue", 1),
        #Do not use the quest herd for "move cattle herd" ends
		
        (party_count_companions_of_type, ":num_cattle", ":cur_party", "trp_cattle"),
        (try_begin),
          (le, ":num_cattle", ":cur_req"),
          (assign, ":num_added", ":num_cattle"),
          (remove_party, ":cur_party"),
        (else_try),
          (assign, ":num_added", ":cur_req"),
          (party_remove_members, ":cur_party", "trp_cattle", ":cur_req"),
        (try_end),
        (val_sub, ":cur_req", ":num_added"),
		
		
        (try_begin),
          (party_slot_eq, ":party_no", slot_party_type, spt_village),
          (party_get_slot, ":village_cattle_amount", ":party_no", slot_village_number_of_cattle),
          (val_add, ":village_cattle_amount", ":num_added"),
          (party_set_slot, ":party_no", slot_village_number_of_cattle, ":village_cattle_amount"),
        (try_end),
		
        (assign, reg3, ":num_added"),
        (str_store_party_name_link, s1, ":party_no"),
        (display_message, "@You brought {reg3} heads of cattle to {s1}."),
		(try_begin),
			(gt, "$cheat_mode", 0),
			(assign, reg4, ":village_cattle_amount"),
			(display_message, "@{!}Village now has {reg4}"),
		(try_end),
      (try_end),
      (store_sub, reg0, ":max_req", ":cur_req"),
     ]),
  # script_get_rumor_to_s61
  # Input: rumor_id
  # Output: reg0 = 1 if rumor found, 0 otherwise; s61 will contain rumor string if found
  ("get_rumor_to_s61",
    [
     (store_script_param, ":base_rumor_id", 1), # the script returns the same rumor for the same rumor id, so that one cannot hear all rumors by
                                                # speaking to a single person.
     ##diplomacy start+ save reg4 in order to revert it at the end of the script
	 (assign, ":save_reg4", reg4),
	 ##diplomacy end+
     (store_current_hours, ":cur_hours"),
     (store_div, ":cur_day", ":cur_hours", 24),
     (assign, ":rumor_found", 0),
     (assign, ":num_tries", 3),
     (try_for_range, ":try_no", 0, ":num_tries"),
       (store_mul, ":rumor_id", ":try_no", 6781),
       (val_add, ":rumor_id", ":base_rumor_id"),
       (store_mod, ":rumor_type", ":rumor_id", 7),
       (val_add, ":rumor_id", ":cur_hours"),
       (try_begin),
         (eq,  ":rumor_type", 0),
         (try_begin),
           (store_sub, ":range", towns_end, towns_begin),
           (store_mod, ":random_center", ":rumor_id", ":range"),
           (val_add, ":random_center", towns_begin),
           (party_slot_ge, ":random_center", slot_town_has_tournament, 1),
           (neq, ":random_center", "$current_town"),
           (str_store_party_name, s62, ":random_center"),
           (str_store_string, s61, "@I heard that there will be a tournament in {s62} soon."),
           (assign, ":rumor_found", 1),
         (try_end),
       (else_try),
         (eq,  ":rumor_type", 1),
         (try_begin),
           (store_sub, ":range", active_npcs_end, original_kingdom_heroes_begin), #was reversed
           (store_mod, ":random_hero", ":rumor_id", ":range"),
           (val_add, ":random_hero", original_kingdom_heroes_begin),
		   (is_between, ":random_hero", active_npcs_begin, active_npcs_end),
           (troop_get_slot, ":personality", ":random_hero", slot_lord_reputation_type),
		   ##diplomacy start+ give rumors for non-noble personalities, and make pronouns gender-correct
		   (try_begin),
		      (ge, ":personality", lrep_roguish),
			  (try_begin),
			    (eq, ":personality", lrep_benefactor),#Ymira, Bunduk, Jeremus
				(assign, ":personality", lrep_goodnatured),#treats people living in his lands decently
			  (else_try),
			    (eq, ":personality", lrep_custodian),#Marnid, Artimenner, Deshavi, Katrin
				(assign, ":personality", lrep_goodnatured),#good to his followers, and rewards them if they work well
			  (else_try),
			    (call_script, "script_dplmc_get_troop_morality_value", ":random_hero", tmt_humanitarian),
				(lt, reg0, 0),#Klethi
				(assign, ":personality", lrep_debauched),#likes to torture his enemies
			  (try_end),
			  (ge, ":personality", lrep_roguish),
			  (assign, ":personality", 0),#zero out to avoid jumping to a nonsensical string
		   (try_end),
		   (call_script, "script_dplmc_store_troop_is_female_reg", ":random_hero", 4),#store gender to reg4 to make pronouns gender-correct
		   ##diplomacy end+
           (gt, ":personality", 0),
           (store_add, ":rumor_string", ":personality", "str_gossip_about_character_default"),
           (str_store_troop_name, s6, ":random_hero"),
           (str_store_string, s61, ":rumor_string"),
           (assign, ":rumor_found", 1),
         (try_end),
         ##diplomacy start+ Change the rumor string in some circumstances to avoid implying the hero is currently ruling a fief
         (try_begin),
           (neg|is_between, ":random_hero", heroes_begin, heroes_end),
         (else_try),
           #Dead
           (troop_slot_eq, ":random_hero", slot_troop_occupation, dplmc_slto_dead),
           (str_store_troop_name, s6, ":random_hero"),
           (str_store_string, s61, "@I heard some people say they don't believe {s6} is really dead."),#The doubters are wrong, like with Tupac or Elvis.
           (assign, ":rumor_found", 1),
         (else_try),
           #In exile
           (this_or_next|troop_slot_eq, ":random_hero", slot_troop_occupation, slto_retirement),
           (troop_slot_eq, ":random_hero", slot_troop_occupation, dplmc_slto_exile),
           (str_store_troop_name, s6, ":random_hero"),
           (str_store_string, s61, "@I heard a traveller say that he came across {s6} while journeying outside these lands."),
           (assign, ":rumor_found", 1),
         (else_try),
           #Inactive pretender
           (troop_slot_eq, ":random_hero", slot_troop_occupation, slto_inactive_pretender),
           (neq, ":random_hero", "$supported_pretender"),
           (troop_get_slot, reg4, ":random_hero", slot_troop_original_faction),
           (is_between, reg4, npc_kingdoms_begin, npc_kingdoms_end),
           (faction_slot_eq, reg4, slot_faction_state, sfs_active),
           (faction_get_slot, reg4, reg4, slot_faction_leader),
           (gt, reg4, -1),
           (str_store_troop_name, s61, reg4),
           (str_store_string, s6, ":random_hero"),
           (str_store_string, s61, "@I heard that {s6} intends to raise an army and seize the overlordship from {s61}."),
           (assign, ":rumor_found", 1),
         (try_end),
         ##diplomacy end+
       (else_try),
         (eq,  ":rumor_type", 2),
         (try_begin),
           (store_sub, ":range", trade_goods_end, trade_goods_begin),
           (store_add, ":random_trade_good", ":rumor_id", ":cur_day"),
           (store_mod, ":random_trade_good", ":random_trade_good", ":range"),
           (store_add, ":random_trade_good_slot", ":random_trade_good", slot_town_trade_good_prices_begin),
           (val_add, ":random_trade_good", trade_goods_begin),
           (store_mul, ":min_price", average_price_factor, 3),
           (val_div, ":min_price", 4),
           (assign, ":min_price_center", -1),
           (try_for_range, ":sub_try_no", 0, 10),
             (store_sub, ":range", towns_end, towns_begin),
             (store_add, ":center_rumor_id", ":rumor_id", ":sub_try_no"),
             (store_mod, ":random_center", ":center_rumor_id", ":range"),
             (val_add, ":random_center", towns_begin),
             (neq, ":random_center", "$g_encountered_party"),
             (party_get_slot, ":cur_price", ":random_center", ":random_trade_good_slot"),
             (lt, ":cur_price", ":min_price"),
             (assign, ":min_price", ":cur_price"),
             (assign, ":min_price_center", ":random_center"),
           (try_end),
           (ge, ":min_price_center", 0),
           (str_store_item_name, s62, ":random_trade_good"),
           (str_store_party_name, s63, ":min_price_center"),
           (str_store_string, s61, "@I heard that one can buy {s62} very cheap at {s63}."),
           (assign, ":rumor_found", 1),
         (try_end),
       (else_try),
         (eq,  ":rumor_type", 3),
         (try_begin),
           (store_sub, ":range", trade_goods_end, trade_goods_begin),
           (store_add, ":random_trade_good", ":rumor_id", ":cur_day"),
           (store_mod, ":random_trade_good", ":random_trade_good", ":range"),
           (store_add, ":random_trade_good_slot", ":random_trade_good", slot_town_trade_good_prices_begin),
           (val_add, ":random_trade_good", trade_goods_begin),
           (store_mul, ":max_price", average_price_factor, 5),
           (val_div, ":max_price", 4),
           (assign, ":max_price_center", -1),
           (try_for_range, ":sub_try_no", 0, 10),
             (store_sub, ":range", towns_end, towns_begin),
             (store_add, ":center_rumor_id", ":rumor_id", ":sub_try_no"),
             (store_mod, ":random_center", ":center_rumor_id", ":range"),
             (val_add, ":random_center", towns_begin),
             (neq, ":random_center", "$g_encountered_party"),
             (party_get_slot, ":cur_price", ":random_center", ":random_trade_good_slot"),
             (gt, ":cur_price", ":max_price"),
             (assign, ":max_price", ":cur_price"),
             (assign, ":max_price_center", ":random_center"),
           (try_end),
           (ge, ":max_price_center", 0),
           (str_store_item_name, s62, ":random_trade_good"),
           (str_store_party_name, s63, ":max_price_center"),
           (str_store_string, s61, "@I heard that they pay a very high price for {s62} at {s63}."),
           (assign, ":rumor_found", 1),
         (try_end),
       (try_end),
       (try_begin),
         (gt, ":rumor_found", 0),
         (assign, ":num_tries", 0),
       (try_end),
     (try_end),
     (assign, reg0, ":rumor_found"),
	 ##diplomacy start+ revert reg4
	 (assign, reg4, ":save_reg4"),
	 ##diplomacy end+
     ]),
  ("lord_comment_to_s43",
    [(store_script_param, ":lord", 1),
     (store_script_param, ":default_string", 2),

    (troop_get_slot,":reputation", ":lord", slot_lord_reputation_type),

	(try_begin),
		#some default strings will have added comments for the added commons reputation types
		##diplomacy start+
		(try_begin),
		#Don't reassign personalities of lords
			(is_between, ":reputation", lrep_none, lrep_upstanding + 1),
       		(else_try),
		#Special case for anti-humanitarians (Klethi in Native)
		    (neg|is_between, ":reputation", lrep_none, lrep_upstanding + 1),
	            (neq, ":reputation", lrep_benefactor),
	            (neq, ":reputation", lrep_moralist),
	            (neq, ":reputation", lrep_conventional),
		    (call_script, "script_dplmc_get_troop_morality_value", ":lord", tmt_humanitarian),
	      	    (lt, reg0, 0),#<- In Native, this only applies to Klethi
		    #Use lrep_debauched by default, and refine further below.
		    (assign, ":reputation", lrep_debauched),
		    (try_begin),
			#If pious, anti-humanitarians use lrep_selfrighteous
		    	(call_script, "script_dplmc_get_troop_morality_value", ":lord", tmt_pious),
			(ge, reg0, 1),#<- Describes no one in Native
			(assign, ":reputation", lrep_selfrighteous),
		    (else_try),
			#If aggressive, anti-humanitarians use lrep_quarrelsome
		    	(call_script, "script_dplmc_get_troop_morality_value", ":lord", tmt_aristocratic),
			(this_or_next|eq, ":reputation", lrep_adventurous),
				(ge, reg0, 1),#<- In Native describes Alayen, Matheld, Rolf, Nizar, Lezalit, Klethi (but only Klethi can even reach here)
			(assign, ":reputation", lrep_quarrelsome),
		    (try_end),
		(else_try),
		#Special case for "pious" characters (no one in Native)
			(call_script, "script_dplmc_get_troop_morality_value", ":lord", tmt_pious),
			(ge, reg0, 1),
			(try_begin),
				#Handle these separately to prevent inappropriate reassignment
				(this_or_next|eq, ":reputation", lrep_benefactor),
					(eq, ":reputation", lrep_moralist),
				(assign, ":reputation", lrep_upstanding),
			(else_try),
				#Ordinarily upstanding
				(call_script, "script_dplmc_get_troop_morality_value", ":lord", tmt_humanitarian),
				(ge, reg0, 0),#<- In Native describes all but Klethi
				(call_script, "script_dplmc_get_troop_morality_value", ":lord", tmt_egalitarian),
				(ge, reg0, 0),#<- In Native describes all but Lezalit
				(call_script, "script_dplmc_get_troop_morality_value", ":lord", tmt_honest),
				(ge, reg0, 0),#<- In Native describes all but Rolf
				(assign, ":reputation", lrep_upstanding),
		    	(else_try),
				#If vicious, self-righteous is also a possibility
			        (assign, ":reputation", lrep_selfrighteous),
		     	(try_end),
		(else_try),
		#Special case for dishonest commoners.
		#Pragmatic-style amoral: lrep_cunning
		#Jerk-style amoral: lrep_debauched
	 	 	(neg|is_between, ":reputation", lrep_none, lrep_upstanding + 1),
	            	(neq, ":reputation", lrep_moralist),
	            	(neq, ":reputation", lrep_benefactor),
			(call_script, "script_dplmc_get_troop_morality_value", ":lord", tmt_honest),
			(lt, reg0, 0),#<- In Native only describes Rolf (who wouldn't reach here, since he is lrep_cunning)
			(try_begin),
				(call_script, "script_dplmc_get_troop_morality_value", ":lord", tmt_egalitarian),
				(lt, reg0, 1),
				(assign, ":egalitarian", reg0),
				(call_script, "script_dplmc_get_troop_morality_value", ":lord", tmt_humanitarian),
				(lt, reg0, 1),
				(this_or_next|lt, reg0, 0),
					(lt, ":egalitarian", 0),
				(assign, ":reputation", lrep_debauched),
			(else_try),
				(assign, ":reputation", lrep_cunning),
			(try_end),
		(else_try),
			(eq, ":reputation", lrep_roguish),
			(assign, ":reputation", lrep_goodnatured),
		(else_try),
			(eq, ":reputation", lrep_custodian),
			(assign, ":reputation", lrep_cunning),
		(else_try),
			(eq, ":reputation", lrep_benefactor),
			(assign, ":reputation", lrep_goodnatured),
        #add support for lady personalities
        (else_try),
            (eq, ":reputation", lrep_ambitious),
            (assign, ":reputation", lrep_cunning),
	(else_try),
	    (this_or_next|eq, ":reputation", lrep_conventional),
	    	(eq, ":reputation", lrep_otherworldly),
	    (assign, ":reputation", lrep_goodnatured),
	(else_try),
	    (eq, ":reputation", lrep_adventurous),
   	    (assign, ":reputation", lrep_martial),
  	    (call_script, "script_dplmc_get_troop_morality_value", ":lord", tmt_egalitarian),
	    (try_begin),
		    (lt, reg0, 0),#<- In Native describes no one
		    (assign, ":reputation", lrep_quarrelsome),
	    (try_end),
	(else_try),
	    (eq, ":reputation", lrep_moralist),
	    (assign, ":reputation", lrep_upstanding),
	(try_end),
	##diplomacy end+

	##diplomacy start+ Add some variability
	#For non-companion, non-monarchs who don't have any tmt_* morality values, this
	# just amounts to a 5% chance to use lrep_none instead of their real reputation
	# (except where that would cause problems).
	#Otherwise,
	# 16,17:
	#   tmt_pious > 0, with lrep_debauched or lrep_quarrelsome or lrep_selfrighteous: lrep_selfrighteous
	#   tmt_pious > 0, with one of (tmt_egalitarian, tmt_honest, tmt_humanitarian) < 0 and none > 0: lrep_selfrighteous
	#   (tmt_pious >= 0 and tmt_honest >= 0) and (tmt_pious > 0 or tmt_honest > 0): lrep_upstanding
	#   tmt_honest < 0: lrep_cunning
	#   lrep_none and is a king or pretender: lrep_cunning
	#
	# 18,19:
	#   tmt_aristocratic > 0, with lrep_debauched or lrep_quarrelsome: lrep_quarrelsome
	#   lrep_martial, with (tmt_honest, tmt_egalitarian, tmt_humanitarian) all non-positive and
	#      at least one negative, and tmt_pious < 1 (so not to overlap with 16,17): lrep_quarrelsome
	#   tmt_aristocratic > 0: lrep_martial
	#   lrep_none and is a king or pretender: lrep_martial
	(store_random_in_range, ":random_chance", 0, 20),
	(assign, ":new_reputation", ":reputation"),
	(try_begin),
		(eq, 1, 1),#Disable this feature for now.
	(else_try),
		#Disable the first time you're talking to someone, or if you haven't
		#spoken to this NPC recently.
		(store_current_hours, ":recently"),
		(val_sub, ":recently", 24),
		(this_or_next|neq, "$g_talk_troop_met", 1),
		(this_or_next|neg|troop_slot_ge, ":lord", slot_troop_met, 1),
		(this_or_next|neg|troop_slot_ge, ":lord", slot_troop_last_talk_time, ":recently"),
		#Disable for things that come in sequences
		(this_or_next|eq, ":default_string", "str_rebellion_dilemma_default"),
			(eq, ":default_string", "str_rebellion_dilemma_2_default"),
		#Set this value to signal to the debug message at the end
		(assign, ":random_chance", -1),
	(else_try),
		#10% chance of lrep_martial or lrep_quarrelsome if appropriate...
		#if already lrep_martial, check separately here for possible conversion
		#to lrep_quarrelsome
		(is_between, ":random_chance", 18, 20),
		(eq, ":reputation", lrep_martial),
		(call_script, "script_dplmc_get_troop_morality_value", ":lord", tmt_egalitarian),
		(lt, reg0, 1),
		(assign, ":bad_sum", reg0),
		(call_script, "script_dplmc_get_troop_morality_value", ":lord", tmt_humanitarian),
		(lt, reg0, 1),
		(val_add, ":bad_sum", reg0),
		(call_script, "script_dplmc_get_troop_morality_value", ":lord", tmt_honest),
		(lt, reg0, 1),
		(val_add, ":bad_sum", reg0),
		#at least one of tmt_egalitarian, tmt_humanitarian, and tmt_honest were negative (and none were positive)
		(lt, ":bad_sum", 0),
		#disable for positive tmt_pious, since that's handled separately as an alternative to lrep_upstanding for [16,17]
		(call_script, "script_dplmc_get_troop_morality_value", ":lord", tmt_honest),
		(lt, reg0, 1),
		(assign, ":new_reputation", lrep_quarrelsome),
     	(else_try),
		#10% chance of lrep_martial or lrep_quarrelsome if appropriate
		#Applies to: Rolf, Nizar, Lezalit, Klethi
		#(Also Alayen and Matheld, but they are already lrep_martial)
		(is_between, ":random_chance", 18, 20),
		(call_script, "script_dplmc_get_troop_morality_value", ":lord", tmt_aristocratic),
		(ge, reg0, 1),
		(try_begin),
			#some personalities use lrep_quarrelsome (only Klethi in Native)
			(this_or_next|eq, ":reputation", lrep_debauched),
				(eq, ":reputation", lrep_quarrelsome),#<-- i.e. no change
			(assign, ":new_reputation", lrep_quarrelsome),
		(else_try),
			#other personalities use lrep_martial
	      		(assign, ":new_reputation", lrep_martial),
		(try_end),
	(else_try),
		#10% chance of lrep_upstanding or lrep_selfrighteous if appropriate
		#Applies to: Marnid, Alayen, Artimenner
		#(Also Firentis, but he is already lrep_upstanding)
		(is_between, ":random_chance", 16, 18),
		(call_script, "script_dplmc_get_troop_morality_value", ":lord", tmt_honest),
		(assign, ":honest", reg0),
		(call_script, "script_dplmc_get_troop_morality_value", ":lord", tmt_pious),
		(assign, ":pious", reg0),
		(this_or_next|ge, ":honest", 1),#one or the other must be greater than zero
			(ge, ":pious", 1),
		(call_script, "script_dplmc_get_troop_morality_value", ":lord", tmt_egalitarian),
		(assign, ":egalitarian", reg0),
		(call_script, "script_dplmc_get_troop_morality_value", ":lord", tmt_humanitarian),
		(assign, ":humanitarian", reg0),
		(try_begin),
			#Unpleasant personalities use "selfrighteous" instead
			#(Applies to no one in Native)
			(this_or_next|eq, ":reputation", lrep_debauched),
			(this_or_next|eq, ":reputation", lrep_quarrelsome),
			(this_or_next|eq, ":reputation", lrep_selfrighteous),#<- i.e. no change
			(this_or_next|lt, ":honest", 0),
			(this_or_next|lt, ":egalitarian", 0),
				(lt, ":humanitarian", 0),
			(assign, ":new_reputation", lrep_selfrighteous),
		(else_try),
		   	#Other personalities use upstanding
			(assign, ":new_reputation", lrep_upstanding),
		(try_end),
	(else_try),
		#10% chance of lrep_cunning if appropriate
		(is_between, ":random_chance", 16, 18),
		(lt, ":honest", 0),#<- In Native only Rolf satisfies this, but he is already lrep_cunning
		(assign, ":reputation", lrep_cunning),
	(else_try),
		#Ruler, if personality triggers not met: 10% cunning, 10% martial
		(is_between, ":random_chance", 16, 20),
		(eq, ":reputation", lrep_none),
		(this_or_next|is_between, ":lord", kings_begin, kings_end),
			(is_between, ":lord", pretenders_begin, pretenders_end),
		(try_begin),
			(is_between, ":random_chance", 16, 18),
			(assign, ":new_reputation", lrep_cunning),
		(else_try),
			(is_between, ":random_chance", 18, 20),
			(call_script, "script_dplmc_get_troop_morality_value", ":lord", tmt_aristocratic),
			(ge, reg0, 0),#Won't reach here if positive, so you could just check if it equals zero
			(assign, ":new_reputation", lrep_martial),
		(try_end),
	(else_try),
		#Others, if personality triggers not met: 5% chance of null
		(is_between, ":random_chance", 16, 20),#base 20%
		(store_mod, ":rand_mod", ":random_chance",4),
		(troop_get_slot, reg0, ":lord", slot_troop_temp_decision_seed),
		(val_mod, reg0, 4),
		(eq, ":rand_mod", reg0),#1/4 of the time, 5%
		#disable for things that don't have a "lrep_none" version defined
		(neq, ":default_string", "str_rebellion_dilemma_default"),
		(neq, ":default_string", "str_rebellion_dilemma_2_default"),
		(neq, ":default_string", "str_changed_my_mind_default"),
		(neq, ":default_string", "str_political_philosophy_default"),
		(neq, ":default_string", "str_rebellion_rival_default"),
		(neq, ":default_string", "str_rebellion_agree_default"),
		(neq, ":default_string", "str_rebellion_refuse_default"),
		(neq, ":default_string", "str_talk_later_default"),
		(neq, ":default_string", "str_npc_claim_throne_liege"),
		#use lrep_none
		(assign, ":new_reputation", lrep_none),
	(try_end),
	(try_begin),
		(eq, 1, 0),#Disable this feature for now.
		(ge, "$cheat_mode", 1),
		(assign, ":save_reg1", reg1),
		(assign, ":save_reg2", reg2),
		(assign, reg0, ":random_chance"),
		(assign, reg1, ":reputation"),
		(assign, reg2, ":new_reputation"),
		(try_begin),
			(neq, ":reputation", ":new_reputation"),
			(display_message, "@{!} DEBUG - random {reg0} (0 to 20), used reputation {reg2} instead of {reg1}"),
		(else_try),
			(lt, ":random_chance", 0),
			(display_message, "@{!} DEBUG - variable responses disabled, kept reputation {reg2}"),
		(else_try),
			(display_message, "@{!} DEBUG - random {reg0} (0 to 20), kept reputation {reg2}"),
		(try_end),
		(assign, reg1, ":save_reg1"),
		(assign, reg2, ":save_reg2"),
	(try_end),
	(assign, ":reputation", ":new_reputation"),
	##diplomacy end+

    (store_add, ":result", ":reputation", ":default_string"),

    (str_store_string, 43, ":result"),
	(assign, reg0, ":result"),


	]),
  # script_add_log_entry
  # Input: arg1 = entry_type, arg2 = event_actor, arg3 = center_object, arg4 = troop_object, arg5 = faction_object
  # Output: none
  ("add_log_entry",
    [(store_script_param, ":entry_type", 1),
     (store_script_param, ":actor", 2),
     (store_script_param, ":center_object", 3),
     (store_script_param, ":troop_object", 4),
     (store_script_param, ":faction_object", 5),
     (assign, ":center_object_lord", -1),
     (assign, ":center_object_faction", -1),
     (assign, ":troop_object_faction", -1),
     
     (try_begin),
       (party_is_active, ":center_object", 0),
       (party_get_slot, ":center_object_lord", ":center_object", slot_town_lord),
       (store_faction_of_party, ":center_object_faction", ":center_object"),
	 (else_try),
	   (assign, ":center_object_lord", 0),	 
       (assign, ":center_object_faction", 0),	 
     (try_end),
     
     (try_begin),
       (is_between, ":troop_object", 0, "trp_local_merchant"),
       (store_troop_faction, ":troop_object_faction", ":troop_object"),
	 (else_try),
	   (assign, ":troop_object_faction", 0),
     (try_end),

     (val_add, "$num_log_entries", 1),
     
     (store_current_hours, ":entry_time"),
     (troop_set_slot, "trp_log_array_entry_type",            "$num_log_entries", ":entry_type"),
     (troop_set_slot, "trp_log_array_entry_time",            "$num_log_entries", ":entry_time"),
     (troop_set_slot, "trp_log_array_actor",                 "$num_log_entries", ":actor"),
     (troop_set_slot, "trp_log_array_center_object",         "$num_log_entries", ":center_object"),
     (troop_set_slot, "trp_log_array_center_object_lord",    "$num_log_entries", ":center_object_lord"),
     (troop_set_slot, "trp_log_array_center_object_faction", "$num_log_entries", ":center_object_faction"),
     (troop_set_slot, "trp_log_array_troop_object",          "$num_log_entries", ":troop_object"),
     (troop_set_slot, "trp_log_array_troop_object_faction",  "$num_log_entries", ":troop_object_faction"),
     (troop_set_slot, "trp_log_array_faction_object",        "$num_log_entries", ":faction_object"),

     (try_begin),
       (eq, "$cheat_mode", 1),
       (assign, reg3, "$num_log_entries"), 
       (assign, reg4, ":entry_type"),
       (display_message, "@{!}Log entry {reg3}: type {reg4}"), 
       (try_begin),
          (gt, ":center_object", 0),
		  (neq, ":entry_type", logent_traveller_attacked),
		  (neq, ":entry_type", logent_party_traded),
		  (party_is_active, ":center_object"), #sometimes is a troop
		  
          (str_store_party_name, s4, ":center_object"),
          (display_message, "@{!}Center: {s4}"), 
       (try_end),      
       (try_begin),
          (gt, ":troop_object", 0),
		  (neq, ":entry_type", logent_traveller_attacked),
		  (neq, ":entry_type", logent_party_traded),
		  
		  (str_store_troop_name, s4, ":troop_object"),
		  (display_message, "@{!}Troop: {s4}"), 
       (try_end),      
       (try_begin),
          (gt, ":center_object_lord", 0),
		  (neq, ":entry_type", logent_traveller_attacked),
		  (neq, ":entry_type", logent_party_traded),
		  
		  (str_store_troop_name, s4, ":center_object_lord"),
          (display_message, "@{!}Lord: {s4}"), 
       (try_end),
     (try_end),


     (try_begin),
	   (this_or_next|eq, ":entry_type", logent_lord_defeated_by_player),
       (this_or_next|eq, ":entry_type", logent_player_participated_in_major_battle),
		(eq, ":entry_type", logent_player_participated_in_siege),
		
       (try_begin),
         (eq, "$cheat_mode", 1),
         (display_message, "@{!}Ally party is present"),
       (try_end),
	   ##diplomacy start+ support kingdom ladies as well
       #(try_for_range, ":hero", active_npcs_begin, active_npcs_end),
	   (try_for_range, ":hero", heroes_begin, heroes_end),
	     (this_or_next|is_between, ":hero", active_npcs_begin, active_npcs_end),
	     (this_or_next|troop_slot_eq, ":hero", slot_troop_occupation, slto_kingdom_hero),
		 (this_or_next|troop_slot_eq, ":hero", slot_troop_occupation, slto_player_companion),
		    (troop_slot_eq, ":hero", slot_troop_occupation, slto_kingdom_seneschal),
	   ##diplomacy end+
         (party_count_companions_of_type, ":hero_present", "p_collective_friends", ":hero"),
         (gt, ":hero_present", 0),
         (troop_set_slot, ":hero", slot_troop_present_at_event, "$num_log_entries"),
#         (store_sub, ":skip_up_to_here", "$num_log_entries", 1),
#         (troop_set_slot, ":hero", slot_troop_last_comment_slot, ":skip_up_to_here"),
         (try_begin),
           (eq, "$cheat_mode", 1),
           (str_store_troop_name, s4, ":hero"),
           (display_message, "@{!}{s4} is present at event"),
         (try_end),
       (try_end),
     (try_end),
     ]),
  # script_get_relevant_comment_for_log_entry
  # Input: arg1 = log_entry_no, 
  # Output: reg0 = comment_id; reg1 = relevance
  # Notes: 50 is the default relevance.
  # A comment with relevance less than 30 will always be skipped.
  # A comment with relevance 75 or more will never be skipped.
  # A comment with relevance 50 has about 50% chance to be skipped.
  # If there is more than one comment that is not skipped, the system will randomize their relevance values, and then choose the highest one.
  # Also note that the relevance of events decreases as time passes. After three months, relevance reduces to 50%, after 6 months, 25%, etc...
  ##diplomacy start+
  ##May also set reg4 or reg3 to correspond to gender
  ##diplomac end+
  ("get_relevant_comment_for_log_entry",
    [(store_script_param, ":log_entry_no", 1),
     
     (troop_get_slot, ":entry_type",            "trp_log_array_entry_type",            ":log_entry_no"),
     (troop_get_slot, ":entry_time",            "trp_log_array_entry_time",            ":log_entry_no"),
     (troop_get_slot, ":actor",                 "trp_log_array_actor",                 ":log_entry_no"),
     (troop_get_slot, ":center_object",         "trp_log_array_center_object",         ":log_entry_no"),
     (troop_get_slot, ":center_object_lord",    "trp_log_array_center_object_lord",    ":log_entry_no"),
     (troop_get_slot, ":center_object_faction", "trp_log_array_center_object_faction", ":log_entry_no"),
     (troop_get_slot, ":troop_object",          "trp_log_array_troop_object",          ":log_entry_no"),
     (troop_get_slot, ":troop_object_faction",  "trp_log_array_troop_object_faction",  ":log_entry_no"),
     (troop_get_slot, ":faction_object",        "trp_log_array_faction_object",        ":log_entry_no"),

     (assign, ":relevance", 0),
     (assign, ":comment", -1), 
     (assign, ":rejoinder", -1), 
     (assign, ":suggested_relation_change", 0),

     (troop_get_slot, ":reputation", "$g_talk_troop", slot_lord_reputation_type),
	 ##diplomacy start+
	 (assign, ":return_reg4", reg4),
	 #Set an initial value for ":return_reg4", although further down
	 #some specific log types override this.
	 (try_begin),
		(is_between, ":troop_object", heroes_begin, heroes_end),
		(neq, ":troop_object", "$g_talk_troop"),
		(assign, ":return_reg4", 0),
		(try_begin),
			(call_script, "script_cf_dplmc_troop_is_female", ":troop_object"),
			(assign, ":return_reg4", 1),
		(try_end),
	 (else_try),
		(is_between, ":actor", heroes_begin, heroes_end),
		(neq, ":actor", "$g_talk_troop"),
		(assign, ":return_reg4", 0),
		(try_begin),
			(call_script, "script_cf_dplmc_troop_is_female", ":actor"),
			(assign, ":return_reg4", 1),
		(try_end),
	 (try_end),


	 #add support for commoner/lady reputations
     (troop_get_slot, ":true_reputation", "$g_talk_troop", slot_lord_reputation_type),#unmodified value
	 #(troop_get_type, ":talk_troop_gender",  "$g_talk_troop"),
	 (call_script, "script_dplmc_store_troop_is_female", "$g_talk_troop"),
	 (assign, ":talk_troop_gender", reg0),
	 (try_begin),
	    (neg|is_between, ":reputation", lrep_none, lrep_upstanding + 1),#<-- no changes are required for standard lord personalities
		(try_begin),
			(eq, ":true_reputation", lrep_ambitious),
			(assign, ":reputation", lrep_cunning),
		(else_try),
			(eq, ":true_reputation", lrep_moralist),
			(assign, ":reputation", lrep_upstanding),
		(else_try),
			(this_or_next|eq, ":true_reputation", lrep_conventional),
			   (this_or_next|eq, ":true_reputation", lrep_otherworldly),
			   (eq, ":true_reputation", lrep_benefactor),
			(assign, ":reputation", lrep_goodnatured),
		(try_end),
	 (try_end),
	 ##diplomacy end+
     (store_current_hours, ":current_time"),
     (store_sub, ":entry_hours_elapsed", ":current_time", ":entry_time"),

#Post 0907 changes begin
     (assign, ":players_kingdom_relation", 0), ##the below is so that lords will not congratulate player on attacking neutrals
	 (try_begin),
        (gt, "$players_kingdom", 0),
		(store_relation, ":players_kingdom_relation", "$players_kingdom", ":troop_object_faction"),
	 (try_end),
	 
     (try_begin),
       (eq, "$cheat_mode", -1), #temporarily disabled
       (try_begin),
         (assign, reg5, ":log_entry_no"),
         (assign, reg6, ":entry_type"),
         (assign, reg8, ":entry_time"),

         (gt, "$players_kingdom", 0),
         (try_begin),
            (gt, ":troop_object_faction", 0),
            (assign, reg7, ":players_kingdom_relation"),
            (display_message, "@{!}Event #{reg5}, type {reg6}, time {reg8}: player's domain relation to troop object = {reg7}"),
         (else_try),
            (gt, ":center_object_faction", 0),
            (assign, reg7, ":players_kingdom_relation"),
            (display_message, "@{!}Event #{reg5}, type {reg6}, time {reg8}: player's domain relation to center object faction = {reg7}"),
         (else_try),
            (gt, ":faction_object", 0),
            (assign, reg7, ":players_kingdom_relation"),
            (display_message, "@{!}Event #{reg5}, type {reg6}, time {reg8}: player's domain relation to faction object = {reg7}"),
         (else_try),
            (display_message, "@{!}Event #{reg5}, type {reg6}, time {reg8}. No relevant domain relation"),
         (try_end),
       (else_try),
         (display_message, "@{!}Event #{reg5}, type {reg6}, time {reg8}. Player unaffiliated"),
       (try_end),
     (try_end),

     ##diplomacy start+
	 #In Native, it's assumed that anyone with lrep_none is a liege, but that isn't alwasys true.
	 #(For example, it's possible in a Native game for a defeated pretender to end up as the vassal
	 #of an NPC lord (!), but still talk as if they're ruling a kingdom.)
	 #  Instead of just relying on personality for this, explicily check if they're a liege.
	 (call_script, "script_dplmc_get_troop_standing_in_faction", "$g_talk_troop", "$g_talk_troop_faction"),
	 (try_begin),
		 (ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
		 (assign, ":speaker_is_a_liege", 1),
	 (else_try),
	     (assign, ":speaker_is_a_liege", 0),
	 (try_end),
	 ##diplomacy end+
     (try_begin),
       (eq, ":entry_type", logent_game_start),
       (eq, "$g_talk_troop_met", 0),
       (is_between, "$g_talk_troop_faction_relation", -5, 5),
       (is_between, "$g_talk_troop_relation", -5, 5),

       (assign, ":relevance", 25),
       (troop_get_slot, ":plyr_renown", "trp_player", slot_troop_renown),
		##diplomacy start+
		(try_begin),
			(lt, "$g_disable_condescending_comments", 0),#prejudice mode: high
			(call_script, "script_cf_dplmc_faction_has_bias_against_gender", "$g_talk_troop_faction", "$character_gender"),#bias against gender
			#80% renown
			(val_mul, ":plyr_renown", 4),
			(val_add, ":plyr_renown", 3),
			(val_div, ":plyr_renown", 5),
		(try_end),
		##diplomacy end+
#normal_banner_begin
       (troop_get_slot, ":banner", "trp_player", slot_troop_banner_scene_prop),
#custom_banner_begin
#       (troop_get_slot, ":banner", "trp_player", slot_troop_custom_banner_flag_type),
       (store_random_in_range, ":renown_check", 100, 200),
       (try_begin),
	     ##diplomacy start+
		 (gt, ":speaker_is_a_liege", 0),#Explicitly check if the speaker is a liege rather than relying solely on reputation
		 ##diplomacy end+
         (eq, ":reputation", lrep_none),
         (gt, "$players_kingdom", 0),
         (assign, ":comment", "str_comment_intro_liege_affiliated"),
         (try_begin),
	       (faction_slot_eq, "$players_kingdom", slot_faction_leader, "trp_player"),
	       (assign, ":comment", "str_comment_intro_liege_affiliated_to_player"),
	     (try_end),
	   (else_try),
	      ##diplomacy start+
		  ##OLD:
		  #(eq, "$character_gender",tf_female),
		  ##NEW:
		  #Instead of assuming there's anti-female bias in all settings, check on a kingdom-by-kingdom basis.
		  (call_script, "script_cf_dplmc_faction_has_bias_against_gender", "$g_talk_troop_faction", "$character_gender"),
		  ##diplomacy end+
		  
         (call_script, "script_troop_get_romantic_chemistry_with_troop", "$g_talk_troop", "trp_player"),
	 (assign, ":attraction", reg0),
	 (store_random_in_range, ":random", 0, 2),
	 (this_or_next|eq, ":random", 0),
	 (gt, ":attraction", 10),
          ##diplomacy start+ disable remarks about women if the speaker is a woman (or visa versa, for settings with biases against men)
		  (this_or_next|gt, ":attraction", 10),
			(neq, ":talk_troop_gender", "$character_gender"),
		  ##diplomacy end+
	 (try_begin),
            (this_or_next|gt, ":plyr_renown", ":renown_check"),
			##diplomacy start+
			#	(eq, "$g_disable_condescending_comments", 1),
			    (ge, "$g_disable_condescending_comments", 1),
			##diplomacy end+
            (assign, ":comment", "str_comment_intro_female_famous_liege"),
            (val_add, ":comment", ":reputation"),
	 (else_try),
	   (ge, ":attraction", 9),
	   (assign, ":comment", "str_comment_intro_female_admiring_liege"),
	   (val_add, ":comment", ":reputation"),
	 (else_try),	
           (gt, ":banner", 0), 
	   (assign, ":comment", "str_comment_intro_female_noble_liege"),
	   (val_add, ":comment", ":reputation"),
	 (else_try),
	   (assign, ":comment", "str_comment_intro_female_common_liege"),
	   (val_add, ":comment", ":reputation"),
	 (try_end),		  
           #Rejoinders for comments

         (try_begin),
	   (eq, ":comment", "str_comment_intro_female_common_badtempered"),
	   (assign, ":rejoinder", "str_rejoinder_intro_female_common_badtempered"),
	 (else_try),
	   (eq, ":comment", "str_comment_intro_female_noble_pitiless"),
	   (assign, ":rejoinder", "str_rejoinder_intro_female_noble_pitiless"),
	 (else_try),
	   (eq, ":comment", "str_comment_intro_female_common_pitiless"),
	   (assign, ":rejoinder", "str_rejoinder_intro_female_common_pitiless"),
	 (else_try),
	   (eq, ":comment", "str_comment_intro_female_noble_sadistic"),
	   (assign, ":rejoinder", "str_rejoinder_intro_female_noble_sadistic"),
	 (else_try),
	   (eq, ":comment", "str_comment_intro_female_common_sadistic"),
	   (assign, ":rejoinder", "str_rejoinder_intro_female_common_sadistic"),			
	 (else_try),
	   (eq, ":comment", "str_comment_intro_female_common_upstanding"),
	   (assign, ":rejoinder", "str_rejoinder_intro_female_common_upstanding"),
	 (else_try),
           (eq, ":comment", "str_comment_intro_female_noble_upstanding"),
	   (assign, ":rejoinder", "str_rejoinder_intro_female_noble_upstanding"),
	 (else_try),
	   (eq, ":comment", "str_comment_intro_female_common_martial"),
	   (assign, ":rejoinder", "str_rejoinder_intro_female_common_martial"),
	 (else_try),
	   (eq, ":comment", "str_comment_intro_female_sadistic_admiring"),
	   (assign, ":rejoinder", "str_rejoinder_intro_female_sadistic_admiring"),
	 (else_try),
	   (eq, ":comment", "str_comment_intro_female_badtempered_admiring"),
	   (assign, ":rejoinder", "str_rejoinder_intro_female_badtempered_admiring"),
	 (else_try),
	   (eq, ":comment", "str_comment_intro_female_pitiless_admiring"),
	   (assign, ":rejoinder", "str_rejoinder_intro_female_pitiless_admiring"),
	 (try_end),
       (else_try),
       #Male character or non-gendered comment
         (try_begin),
           (gt, ":plyr_renown", ":renown_check"),
           (assign, ":comment", "str_comment_intro_famous_liege"),
           (val_add, ":comment", ":reputation"),
         (else_try),	
           (gt, ":banner", 0), 
           (assign, ":comment", "str_comment_intro_noble_liege"),
  	   (val_add, ":comment", ":reputation"),			
           (try_begin),
             (eq, ":comment", "str_comment_intro_noble_sadistic"),
             (assign, ":rejoinder", "str_rejoinder_intro_noble_sadistic"),
           (try_end),			
         (else_try),
           (assign, ":comment", "str_comment_intro_common_liege"),
           (val_add, ":comment", ":reputation"),									
         (try_end),
       (try_end),
#Post 0907 changes end

     (else_try),
       (eq, ":entry_type", logent_village_raided),
       (eq, ":actor", "trp_player"),
       (try_begin),
         (eq, ":center_object_lord", "$g_talk_troop"),
         (assign, ":relevance", 200),
         (assign, ":suggested_relation_change", -1),
         (assign, ":comment", "str_comment_you_raided_my_village_default"),
         (try_begin),
            (lt, "$g_talk_troop_faction_relation", -5),
            (this_or_next|eq, ":reputation", lrep_goodnatured),
                (eq, ":reputation", lrep_upstanding),
            (assign, ":comment", "str_comment_you_raided_my_village_enemy_benevolent"),
         (else_try),
            (lt, "$g_talk_troop_faction_relation", -5),
            (this_or_next|eq, ":reputation", lrep_cunning),
                (eq, ":reputation", lrep_selfrighteous),
            (assign, ":comment", "str_comment_you_raided_my_village_enemy_coldblooded"),
         (else_try),
            (lt, "$g_talk_troop_faction_relation", -5),
            (this_or_next|eq, ":reputation", lrep_quarrelsome),
                (eq, ":reputation", lrep_debauched),
            (assign, ":comment", "str_comment_you_raided_my_village_enemy_spiteful"),
         (else_try),
            (lt, "$g_talk_troop_faction_relation", -5),
            (assign, ":comment", "str_comment_you_raided_my_village_enemy"),
         (else_try),
            (lt, "$g_talk_troop_relation", -5),
            (this_or_next|eq, ":reputation", lrep_quarrelsome),
                (eq, ":reputation", lrep_debauched),
            (assign, ":comment", "str_comment_you_raided_my_village_unfriendly_spiteful"),
         (else_try),
            (gt, "$g_talk_troop_relation", 5),
            (assign, ":comment", "str_comment_you_raided_my_village_friendly"),
         (try_end),
       (try_end),

     (else_try),
       (eq, ":entry_type", logent_village_extorted),
       (eq, ":actor", "trp_player"),
       (try_begin),
         (eq, ":center_object_lord", "$g_talk_troop"),
         (assign, ":relevance", 30),
         (assign, ":suggested_relation_change", -1),
         (assign, ":comment", "str_comment_you_robbed_my_village_default"),
         (try_begin),
            (lt, "$g_talk_troop_faction_relation", -5),
            (this_or_next|eq, ":reputation", lrep_cunning),
                (eq, ":reputation", lrep_selfrighteous),
            (assign, ":comment", "str_comment_you_robbed_my_village_enemy_coldblooded"),
         (else_try),
            (lt, "$g_talk_troop_faction_relation", -5),
            (assign, ":comment", "str_comment_you_robbed_my_village_enemy"),
         (else_try),
            (gt, "$g_talk_troop_relation", 5),
            (this_or_next|eq, ":reputation", lrep_quarrelsome),
                (eq, ":reputation", lrep_debauched),
            (assign, ":comment", "str_comment_you_robbed_my_village_friendly_spiteful"),
         (else_try),
            (gt, "$g_talk_troop_relation", 5),
            (assign, ":comment", "str_comment_you_robbed_my_village_friendly"),
         (try_end),
       (try_end),

     (else_try),
       (eq, ":entry_type", logent_caravan_accosted),
       (eq, ":actor", "trp_player"),
       (eq, ":faction_object", "$g_talk_troop_faction"),
	   (eq, ":center_object", -1),
	   (eq, ":troop_object", -1),
	   

	   
       (faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, "$g_talk_troop"),
       (assign, ":relevance", 30),
       (assign, ":suggested_relation_change", -1),
       (assign, ":comment", "str_comment_you_accosted_my_caravan_default"),
       (try_begin),
            (lt, "$g_talk_troop_faction_relation", -5),
            (assign, ":comment", "str_comment_you_accosted_my_caravan_enemy"),
       (try_end),

     (else_try),
       (eq, ":entry_type", logent_helped_peasants),
       (eq, ":actor", "trp_player"),
       (try_begin),
         (eq, ":center_object_lord", "$g_talk_troop"),
         (assign, ":relevance", 40),
         (assign, ":suggested_relation_change", 0),
         (try_begin),
            (this_or_next|eq, ":reputation", lrep_goodnatured),
                (eq, ":reputation", lrep_upstanding),
            (assign, ":comment", "str_comment_you_helped_villagers_benevolent"),
            (assign, ":suggested_relation_change", 1),
         (else_try),
            (gt, "$g_talk_troop_relation", 5),
            (this_or_next|eq, ":reputation", lrep_quarrelsome),
                (eq, ":reputation", lrep_debauched),
            (assign, ":comment", "str_comment_you_helped_villagers_friendly_cruel"),
            (assign, ":suggested_relation_change", -1),
         (else_try),
            (lt, "$g_talk_troop_relation", -5),
            (this_or_next|eq, ":reputation", lrep_quarrelsome),
                (eq, ":reputation", lrep_debauched),
            (assign, ":comment", "str_comment_you_helped_villagers_unfriendly_spiteful"),
            (assign, ":suggested_relation_change", -1),
         (else_try),
            (gt, "$g_talk_troop_relation", 5),
            (assign, ":comment", "str_comment_you_helped_villagers_friendly"),
         (else_try),
            (this_or_next|eq, ":reputation", lrep_selfrighteous),
                (eq, ":reputation", lrep_debauched),
            (assign, ":comment", "str_comment_you_helped_villagers_cruel"),
            (assign, ":suggested_relation_change", -1),
         (else_try),
             (assign, ":comment", "str_comment_you_helped_villagers_default"),
         (try_end),
       (try_end),

###Combat events
     (else_try),
       (eq, ":entry_type", logent_castle_captured_by_player),
       
       (try_begin),
         (eq, ":center_object_lord", "$g_talk_troop"),
		 (store_faction_of_party, ":current_center_faction", ":center_object"),
		 (eq, ":current_center_faction", "$players_kingdom"),
		 (neq, "$g_talk_troop_faction", "$players_kingdom"),
		 
         (this_or_next|eq, ":reputation", lrep_quarrelsome),
			(eq, ":reputation", lrep_debauched),
		 
         (assign, ":comment", "str_comment_you_captured_my_castle_enemy_spiteful"),
         (assign, ":relevance", 200),
       (else_try),
         (eq, ":center_object_lord", "$g_talk_troop"),
		 (store_faction_of_party, ":current_center_faction", ":center_object"),
		 (eq, ":current_center_faction", "$players_kingdom"),
		 (neq, "$g_talk_troop_faction", "$players_kingdom"),
		 
         (this_or_next|eq, ":reputation", lrep_martial),
			(eq, ":reputation", lrep_goodnatured),
			
         (assign, ":comment", "str_comment_you_captured_my_castle_enemy_chivalrous"),
         (assign, ":relevance", 200),
       (else_try),
         (eq, ":center_object_lord", "$g_talk_troop"),
		 (store_faction_of_party, ":current_center_faction", ":center_object"),
		 (eq, ":current_center_faction", "$players_kingdom"),
		 (neq, "$g_talk_troop_faction", "$players_kingdom"),
		 
         (assign, ":comment", "str_comment_you_captured_my_castle_enemy"),
         (assign, ":relevance", 200),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (lt, ":players_kingdom_relation", 0),
         (this_or_next|eq, ":reputation", lrep_quarrelsome),
         (eq, ":reputation", lrep_debauched),
         (assign, ":comment", "str_comment_you_captured_a_castle_allied_spiteful"),
         (assign, ":relevance", 75),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (lt, ":players_kingdom_relation", 0),
         (gt, "$g_talk_troop_relation", 5),
         (assign, ":comment", "str_comment_you_captured_a_castle_allied_friendly"),
         (assign, ":relevance", 75),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (lt, ":players_kingdom_relation", 0),
         (lt, "$g_talk_troop_relation", -5),
         (this_or_next|eq, ":reputation", lrep_quarrelsome),
         (eq, ":reputation", lrep_debauched),
         (assign, ":comment", "str_comment_you_captured_a_castle_allied_unfriendly_spiteful"),
         (assign, ":relevance", 75),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (lt, ":players_kingdom_relation", 0),
         (lt, "$g_talk_troop_relation", -5),
         (assign, ":comment", "str_comment_you_captured_a_castle_allied_unfriendly"),
         (assign, ":relevance", 75),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (lt, ":players_kingdom_relation", 0),
         (assign, ":comment", "str_comment_you_captured_a_castle_allied"),
         (assign, ":relevance", 75),
       (try_end),
       
     (else_try),
       (eq, ":entry_type", logent_player_claims_throne_1),
       (eq, "$players_kingdom", "$g_talk_troop_faction"),
	   (faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, "$g_talk_troop"),
       (assign, ":comment", "str_comment_you_claimed_the_throne_1_player_liege"),
       (assign, ":relevance", 500),
       (lt, "$g_talk_troop_relation", -10),
	   
     (else_try),
       (eq, ":entry_type", logent_player_claims_throne_2),
       (eq, "$players_kingdom", "$g_talk_troop_faction"),
	   (faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, "$g_talk_troop"),
       (assign, ":comment", "str_comment_you_claimed_the_throne_2_player_liege"),
       (assign, ":relevance", 500),
       (lt, "$g_talk_troop_relation", -10),

     (else_try), #player appointed a commoner
       (eq, ":entry_type", logent_liege_grants_fief_to_vassal),
	   (eq, ":actor", "trp_player"),
           (troop_slot_ge, ":troop_object", slot_lord_reputation_type, lrep_roguish),
           ##diplomacy start+
           (neq, ":troop_object", "trp_npc13"),#Nizar isn't a commoner
		   (neg|troop_slot_ge, ":troop_object", slot_lord_reputation_type, lrep_conventional),#ladies aren't commoners
		   (assign, ":return_reg4", 0),
		   (try_begin),
			  (call_script, "script_cf_dplmc_troop_is_female", ":troop_object"),
			  (assign, ":return_reg4", 1),
		   (try_end),
           ##diplomacy end+
       (try_begin),
	   ##diplomacy start+
	      #Companions: make a supportive remark if the person is compatible with you
		  #gekokujo 3.0 microfactions! include fort companions start
	      #(is_between, "$g_talk_troop", companions_begin, companions_end),
	      (is_between, "$g_talk_troop", companions_begin, fort_companions_end),
		  #gekokujo 3.0 microfactions! include fort companions end
	      (troop_slot_eq, "$g_talk_troop", slot_troop_personalitymatch_object, ":troop_object"),
	      (assign, ":comment", "str_dplmc_comment_you_enfiefed_a_commoner_supportive"),
	      (assign, ":relevance", 100),
	      (assign, ":suggested_relation_change", 0),
	   (else_try),
		   #Make a supportive remark if you like the person a lot (overrides objections)
		   (call_script, "script_troop_get_relation_with_troop", ":troop_object", "$g_talk_troop"),
 	       (ge, reg0, 50),
		   (assign, ":comment", "str_dplmc_comment_you_enfiefed_a_commoner_supportive"),
		   (assign, ":relevance", 100),
		   (assign, ":suggested_relation_change", 0),
	   (else_try),
	       #Make a supportive remark if you like the person and wouldn't ordinarily object
		   (ge, reg0, 20),
		   (this_or_next|is_between, ":true_reputation", lrep_roguish, lrep_conventional),
		   (this_or_next|eq, ":reputation", lrep_cunning),
		   (eq, ":reputation", lrep_goodnatured),
		   (assign, ":comment", "str_dplmc_comment_you_enfiefed_a_commoner_supportive"),
		   (assign, ":relevance", 100),
		   (assign, ":suggested_relation_change", 0),
	   (else_try),
	       #Don't complain about your own spouse.
		   (troop_slot_eq, "$g_talk_troop", ":troop_object", slot_troop_spouse),
	   (else_try),
		   #Don't complain if you aren't actually a lord.
		   (is_between, ":true_reputation", lrep_roguish, lrep_conventional),
	   (else_try),
	   ##diplomacy end+
           (this_or_next|eq, ":reputation", lrep_quarrelsome),
               (eq, ":reputation", lrep_debauched),        
           (assign, ":comment", "str_comment_you_enfiefed_a_commoner_nasty"),##diplomacy start+ note: this line uses reg4 from above for gender-correct pronoun ##diplomacy end+
           (assign, ":relevance", 100),
		   (assign, ":suggested_relation_change", -3),

       (else_try),
		   (eq, ":reputation", lrep_upstanding),
           (assign, ":comment", "str_comment_you_enfiefed_a_commoner_hesitant"),##diplomacy start+ note: next line uses reg4 from above for gender-correct pronoun ##diplomacy en
           (assign, ":relevance", 100),
		   (assign, ":suggested_relation_change", -2),
		   
       (else_try),
           (this_or_next|eq, ":reputation", lrep_selfrighteous),
			   (eq, ":reputation", lrep_martial),
           (assign, ":comment", "str_comment_you_enfiefed_a_commoner_derisive"),##diplomacy start+ note: next line uses reg4 from above for gender-correct pronoun ##diplomacy en
           (assign, ":relevance", 100),
		   (assign, ":suggested_relation_change", -4),
		   
       (try_end),
   	   	   
#Post 0907 changes begin
     (else_try),
       (this_or_next|eq, ":entry_type", logent_lord_defeated_by_player),
            (eq, ":entry_type", logent_lord_helped_by_player),
       (troop_slot_eq, "$g_talk_troop", slot_troop_present_at_event, ":log_entry_no"),
       (try_begin),
           (lt, "$g_talk_troop_relation", -5),
           (this_or_next|eq, ":reputation", lrep_quarrelsome),
               (eq, ":reputation", lrep_debauched),        
           (assign, ":comment", "str_comment_we_defeated_a_lord_unfriendly_spiteful"),
           (assign, ":relevance", 150),
       (else_try),
           (lt, "$g_talk_troop_relation", -5),
           (assign, ":comment", "str_comment_we_defeated_a_lord_unfriendly"),
           (assign, ":relevance", 150),
       (else_try),
           (this_or_next|eq, ":reputation", lrep_selfrighteous),
               (eq, ":reputation", lrep_debauched),        
           (assign, ":comment", "str_comment_we_defeated_a_lord_cruel"),
           (assign, ":relevance", 150),
       (else_try),
           (eq, ":reputation", lrep_quarrelsome),        
           (assign, ":comment", "str_comment_we_defeated_a_lord_cruel"),
           (assign, ":relevance", 150),
       (else_try),
           (eq, ":reputation", lrep_upstanding),
           (assign, ":comment", "str_comment_we_defeated_a_lord_upstanding"),
           (assign, ":relevance", 150),
       (else_try),
           (assign, ":comment", "str_comment_we_defeated_a_lord_default"),
           (assign, ":relevance", 150),
       (try_end),

     (else_try),
       (this_or_next|eq, ":entry_type", logent_castle_captured_by_player),
       (eq, ":entry_type", logent_player_participated_in_siege),       
    
       (troop_slot_eq, "$g_talk_troop", slot_troop_present_at_event, ":log_entry_no"),
       
       (try_begin),
           (lt, "$g_talk_troop_relation", -5),
           (this_or_next|eq, ":reputation", lrep_quarrelsome),
           (eq, ":reputation", lrep_debauched),        
           (assign, ":comment", "str_comment_we_fought_in_siege_unfriendly_spiteful"),
           (assign, ":relevance", 150),
       (else_try),
           (lt, "$g_talk_troop_relation", -5),
           (assign, ":comment", "str_comment_we_fought_in_siege_unfriendly"),
           (assign, ":relevance", 150),
       (else_try),
           (this_or_next|eq, ":reputation", lrep_selfrighteous),
           (eq, ":reputation", lrep_debauched),        
           (assign, ":comment", "str_comment_we_fought_in_siege_cruel"),
           (assign, ":relevance", 150),
		   (assign, ":suggested_relation_change", 1),		   
       (else_try),
           (eq, ":reputation", lrep_quarrelsome),        
           (assign, ":comment", "str_comment_we_fought_in_siege_quarrelsome"),
           (assign, ":relevance", 150),
		   (assign, ":suggested_relation_change", 1),		   
       (else_try),
           (eq, ":reputation", lrep_upstanding),
           (assign, ":comment", "str_comment_we_fought_in_siege_upstanding"),
           (assign, ":relevance", 150),
		   (assign, ":suggested_relation_change", 1),		   
       (else_try),
           (eq, ":reputation", lrep_martial),
           (assign, ":comment", "str_comment_we_fought_in_siege_default"),
           (assign, ":relevance", 150),
		   (assign, ":suggested_relation_change", 2),
       (else_try),
           (faction_slot_eq, "$players_kingdom", slot_faction_leader, "$g_talk_troop"),
           (assign, ":comment", "str_comment_we_fought_in_siege_default"),
           (assign, ":relevance", 150),
		   (assign, ":suggested_relation_change", 1),
		(else_try),
           (assign, ":comment", "str_comment_we_fought_in_siege_default"),
           (assign, ":relevance", 150),
		   (assign, ":suggested_relation_change", 1),
       (try_end),
       
     (else_try),     
       (eq, ":entry_type", logent_castle_given_to_lord_by_player),
            
       (try_begin),
         (eq, ":troop_object", "$g_talk_troop"),         
         (this_or_next|eq, ":reputation", lrep_quarrelsome),
         (eq, ":reputation", lrep_debauched),         
         (assign, ":comment", "str_comment_you_give_castle_in_my_control"),
         (assign, ":relevance", 200),
       (else_try),
         (eq, ":troop_object", "$g_talk_troop"),         
         (this_or_next|eq, ":reputation", lrep_martial),
         (eq, ":reputation", lrep_goodnatured),         
         (assign, ":comment", "str_comment_you_give_castle_in_my_control"),
         (assign, ":relevance", 200),
       (else_try),
         (eq, ":troop_object", "$g_talk_troop"),
         (assign, ":comment", "str_comment_you_give_castle_in_my_control"),
         (assign, ":relevance", 200),
       (try_end),

     (else_try),
       (eq, ":entry_type", logent_player_participated_in_major_battle),
       (troop_slot_eq, "$g_talk_troop", slot_troop_present_at_event, ":log_entry_no"),
       (try_begin),
           (lt, "$g_talk_troop_relation", -5),
           (this_or_next|eq, ":reputation", lrep_quarrelsome),
               (eq, ":reputation", lrep_debauched),        
           (assign, ":comment", "str_comment_we_fought_in_major_battle_unfriendly_spiteful"),
           (assign, ":relevance", 150),
       (else_try),
           (lt, "$g_talk_troop_relation", -5),
           (assign, ":comment", "str_comment_we_fought_in_major_battle_unfriendly"),
           (assign, ":relevance", 150),
       (else_try),
           (this_or_next|eq, ":reputation", lrep_selfrighteous),
               (eq, ":reputation", lrep_debauched),        
           (assign, ":comment", "str_comment_we_fought_in_major_battle_cruel"),
           (assign, ":relevance", 150),
		   (assign, ":suggested_relation_change", 1),		   
       (else_try),
           (eq, ":reputation", lrep_quarrelsome),        
           (assign, ":comment", "str_comment_we_fought_in_major_battle_cruel"),
           (assign, ":relevance", 150),
		   (assign, ":suggested_relation_change", 1),		   
       (else_try),
           (eq, ":reputation", lrep_upstanding),
           (assign, ":comment", "str_comment_we_fought_in_major_battle_upstanding"),
           (assign, ":relevance", 150),
		   (assign, ":suggested_relation_change", 1),		   
       (else_try),
           (faction_slot_eq, "$players_kingdom", slot_faction_leader, "$g_talk_troop"),
           (assign, ":comment", "str_comment_we_fought_in_major_battle_default"),
           (assign, ":relevance", 150),
		   (assign, ":suggested_relation_change", 1),
       (else_try),
           (eq, ":reputation", lrep_martial),
           (assign, ":comment", "str_comment_we_fought_in_major_battle_default"),
           (assign, ":relevance", 150),
		   (assign, ":suggested_relation_change", 2),
	   (else_try),
           (assign, ":comment", "str_comment_we_fought_in_major_battle_default"),
           (assign, ":relevance", 150),
		   (assign, ":suggested_relation_change", 1),		   
       (try_end),

     (else_try),
       (eq, ":entry_type", logent_player_suggestion_succeeded),
       (try_begin),
         (eq, ":troop_object", "$g_talk_troop"),
         (assign, ":comment", "str_comment_player_suggestion_succeeded"),
         (assign, ":relevance", 200),
		 (assign, ":suggested_relation_change", 3),

	   (try_end),
     (else_try),
       (eq, ":entry_type", logent_player_suggestion_failed),
       (try_begin),
         (eq, ":troop_object", "$g_talk_troop"),
         (assign, ":comment", "str_comment_player_suggestion_failed"),
         (assign, ":relevance", 200),
		 (assign, ":suggested_relation_change", -5),

	   (try_end),
	   
#Post 0907 changes end

     (else_try),
       (eq, ":entry_type", logent_lord_defeated_by_player),
	   ##diplomacy start+  Set reg4 for calling scripts
	   (try_begin),
		  (neq, ":troop_object", "$g_talk_troop"),
		  (assign, ":return_reg4", 0),
		  (call_script, "script_cf_dplmc_troop_is_female", ":troop_object"),
		  (assign, ":return_reg4", 1),
	   (try_end),
	   ##diplomacy end+
       (try_begin),
         (eq, ":troop_object", "$g_talk_troop"),
         (this_or_next|eq, ":reputation", lrep_martial),
             (eq, ":reputation", lrep_goodnatured),
         (assign, ":comment", "str_comment_you_defeated_me_enemy_chivalrous"),
         (assign, ":relevance", 200),
       (else_try),
         (eq, ":troop_object", "$g_talk_troop"),
         (this_or_next|eq, ":reputation", lrep_debauched),
             (eq, ":reputation", lrep_quarrelsome),
         (assign, ":comment", "str_comment_you_defeated_me_enemy_spiteful"),
         (assign, ":relevance", 200),
       (else_try),
         (eq, ":troop_object", "$g_talk_troop"),
         (assign, ":comment", "str_comment_you_defeated_me_enemy"),
         (assign, ":relevance", 200),
       (else_try),
         (eq, ":troop_object_faction", "$g_talk_troop_faction"),
         (this_or_next|eq, ":reputation", lrep_upstanding),
             (eq, ":reputation", lrep_cunning),
         (assign, ":comment", "str_comment_you_defeated_my_friend_enemy_pragmatic"),
         (assign, ":relevance", 85),
       (else_try),
         (eq, ":troop_object_faction", "$g_talk_troop_faction"),
         (this_or_next|eq, ":reputation", lrep_martial),
             (eq, ":reputation", lrep_goodnatured),
         (assign, ":comment", "str_comment_you_defeated_my_friend_enemy_chivalrous"),
         (assign, ":relevance", 85),
       (else_try),
         (eq, ":troop_object_faction", "$g_talk_troop_faction"),
         (this_or_next|eq, ":reputation", lrep_quarrelsome),
             (eq, ":reputation", lrep_debauched),
         (assign, ":comment", "str_comment_you_defeated_my_friend_enemy_spiteful"),
         (assign, ":relevance", 85),
       (else_try),
         (eq, ":troop_object_faction", "$g_talk_troop_faction"),
         (assign, ":comment", "str_comment_you_defeated_my_friend_enemy"),
         (assign, ":relevance", 85),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (lt, ":players_kingdom_relation", 0),
         (faction_slot_eq, "$players_kingdom", slot_faction_leader, "$g_talk_troop"),
         (assign, ":comment", "str_comment_you_defeated_a_lord_allied_liege"),
         (assign, ":relevance", 150),
		 (assign, ":suggested_relation_change", 1),
		 
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (lt, ":players_kingdom_relation", 0),
         (lt, "$g_talk_troop_relation", -5),
         (this_or_next|eq, ":reputation", lrep_quarrelsome),
             (eq, ":reputation", lrep_debauched),
         (assign, ":comment", "str_comment_you_defeated_a_lord_allied_unfriendly_spiteful"),
         (assign, ":relevance", 65),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (lt, ":players_kingdom_relation", 0),
         (this_or_next|eq, ":reputation", lrep_quarrelsome),
             (eq, ":reputation", lrep_debauched),
         (assign, ":comment", "str_comment_you_defeated_a_lord_allied_spiteful"),
         (assign, ":relevance", 65),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (lt, ":players_kingdom_relation", 0),
         (lt, "$g_talk_troop_relation", -5),
         (this_or_next|eq, ":reputation", lrep_upstanding),
             (eq, ":reputation", lrep_martial),
         (assign, ":comment", "str_comment_you_defeated_a_lord_allied_unfriendly_chivalrous"),
         (assign, ":relevance", 65),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (lt, ":players_kingdom_relation", 0),
         (assign, ":comment", "str_comment_you_defeated_a_lord_allied"),
         (assign, ":relevance", 65),
       (try_end),

     (else_try),
       (eq, ":entry_type", logent_lord_defeated_by_player),
	   ##diplomacy start+  Set reg4 for calling scripts
	   (try_begin),
		  (neq, ":troop_object", "$g_talk_troop"),
		  (assign, ":return_reg4", 0),
		  (call_script, "script_cf_dplmc_troop_is_female", ":troop_object"),
		  (assign, ":return_reg4", 1),
	   (try_end),
	   ##diplomacy end+
       (try_begin),
         (eq, ":troop_object", "$g_talk_troop"),
         (this_or_next|eq, ":reputation", lrep_martial),
             (eq, ":reputation", lrep_goodnatured),
         (assign, ":comment", "str_comment_you_defeated_me_enemy_chivalrous"),
         (assign, ":relevance", 200),
       (else_try),
         (eq, ":troop_object", "$g_talk_troop"),
         (this_or_next|eq, ":reputation", lrep_debauched),
             (eq, ":reputation", lrep_quarrelsome),
         (assign, ":comment", "str_comment_you_defeated_me_enemy_spiteful"),
         (assign, ":relevance", 200),
       (else_try),
         (eq, ":troop_object", "$g_talk_troop"),
         (assign, ":comment", "str_comment_you_defeated_me_enemy"),
         (assign, ":relevance", 200),
       (else_try),
         (eq, ":troop_object_faction", "$g_talk_troop_faction"),
         (this_or_next|eq, ":reputation", lrep_upstanding),
             (eq, ":reputation", lrep_cunning),
         (assign, ":comment", "str_comment_you_defeated_my_friend_enemy_pragmatic"),
         (assign, ":relevance", 85),
       (else_try),
         (eq, ":troop_object_faction", "$g_talk_troop_faction"),
         (this_or_next|eq, ":reputation", lrep_martial),
             (eq, ":reputation", lrep_goodnatured),
         (assign, ":comment", "str_comment_you_defeated_my_friend_enemy_chivalrous"),
         (assign, ":relevance", 85),
       (else_try),
         (eq, ":troop_object_faction", "$g_talk_troop_faction"),
         (this_or_next|eq, ":reputation", lrep_quarrelsome),
             (eq, ":reputation", lrep_debauched),
         (assign, ":comment", "str_comment_you_defeated_my_friend_enemy_spiteful"),
         (assign, ":relevance", 85),
       (else_try),
         (eq, ":troop_object_faction", "$g_talk_troop_faction"),
         (assign, ":comment", "str_comment_you_defeated_my_friend_enemy"),
         (assign, ":relevance", 85),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (lt, ":players_kingdom_relation", 0),
         (faction_slot_eq, "$players_kingdom", slot_faction_leader, "$g_talk_troop"),
         (assign, ":comment", "str_comment_you_defeated_a_lord_allied_liege"),
         (assign, ":relevance", 70),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (lt, ":players_kingdom_relation", 0),
         (lt, "$g_talk_troop_relation", -5),
         (this_or_next|eq, ":reputation", lrep_quarrelsome),
             (eq, ":reputation", lrep_debauched),
         (assign, ":comment", "str_comment_you_defeated_a_lord_allied_unfriendly_spiteful"),
         (assign, ":relevance", 65),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (lt, ":players_kingdom_relation", 0),
         (this_or_next|eq, ":reputation", lrep_quarrelsome),
             (eq, ":reputation", lrep_debauched),
         (assign, ":comment", "str_comment_you_defeated_a_lord_allied_spiteful"),
         (assign, ":relevance", 65),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (lt, ":players_kingdom_relation", 0),
         (lt, "$g_talk_troop_relation", -5),
         (this_or_next|eq, ":reputation", lrep_upstanding),
             (eq, ":reputation", lrep_martial),
         (assign, ":comment", "str_comment_you_defeated_a_lord_allied_unfriendly_chivalrous"),
         (assign, ":relevance", 65),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (lt, ":players_kingdom_relation", 0),
         (assign, ":comment", "str_comment_you_defeated_a_lord_allied"),
         (assign, ":relevance", 65),
       (try_end),

#Post 0907 changes begin
     (else_try),
       (eq, ":entry_type", logent_lord_helped_by_player),
       (neq, ":troop_object", "$g_talk_troop"),
       (eq, ":troop_object_faction", "$g_talk_troop_faction"),
	   ##diplomacy start+  Set reg4 for calling scripts
	   (assign, ":return_reg4", 0),
	   (try_begin),
		  (call_script, "script_cf_dplmc_troop_is_female", ":troop_object"),
		  (assign, ":return_reg4", 1),
	   (try_end),
	   ##diplomacy end+
       (try_begin),
         (lt, "$g_talk_troop_relation", -5),
         (this_or_next|eq, ":reputation", lrep_upstanding),
             (eq, ":reputation", lrep_martial),
         (assign, ":comment", "str_comment_you_helped_my_ally_unfriendly_chivalrous"),
         (assign, ":relevance", 65),
         (assign, ":suggested_relation_change", 2),
       (else_try),
         (lt, "$g_talk_troop_relation", -5),
         (assign, ":comment", "str_comment_you_helped_my_ally_unfriendly"),
         (assign, ":relevance", 0),
       (else_try),
	      ##diplomacy start+
		  (gt, ":speaker_is_a_liege", 0),#Explicitly check if the speaker is a liege rather than relying solely on reputation
		  ##diplomacy end+
         (eq, ":reputation", lrep_none),
         (assign, ":comment", "str_comment_you_helped_my_ally_liege"),
         (assign, ":relevance", 65),
         (assign, ":suggested_relation_change", 3),
       (else_try),
         (lt, "$g_talk_troop_relation", -5),
         (this_or_next|eq, ":reputation", lrep_quarrelsome),
             (eq, ":reputation", lrep_debauched),
         (assign, ":comment", "str_comment_you_helped_my_ally_unfriendly_spiteful"),
         (assign, ":relevance", 65),
       (else_try),
         (this_or_next|eq, ":reputation", lrep_quarrelsome),
             (eq, ":reputation", lrep_debauched),
         (assign, ":comment", "str_comment_you_helped_my_ally_spiteful"),
         (assign, ":relevance", 65),
       (else_try),
         (this_or_next|eq, ":reputation", lrep_martial),
             (eq, ":reputation", lrep_upstanding),
         (assign, ":comment", "str_comment_you_helped_my_ally_chivalrous"),
         (assign, ":relevance", 65),
         (assign, ":suggested_relation_change", 2),
       (else_try),
         (eq, ":troop_object", "$g_talk_troop"),
         (assign, ":comment", "str_comment_you_helped_my_ally_default"),
       (try_end),

#Post 0907 changes begin
     (else_try),
       (eq, ":entry_type", logent_player_defeated_by_lord),
	   ##diplomacy start+  Set reg4 for calling scripts
	   (try_begin),
		  (neq, ":troop_object", "$g_talk_troop"),
		  (assign, ":return_reg4", 0),
		  (call_script, "script_cf_dplmc_troop_is_female", ":troop_object"),
		  (assign, ":return_reg4", 1),
	   (try_end),
	   ##diplomacy end+
       (troop_slot_eq, "$g_talk_troop", slot_troop_present_at_event, ":log_entry_no"),
       (try_begin),
           (lt, "$g_talk_troop_relation", -5),
           (this_or_next|eq, ":reputation", lrep_quarrelsome),
               (eq, ":reputation", lrep_debauched),
           (assign, ":comment", "str_comment_we_were_defeated_unfriendly_spiteful"),
           (assign, ":relevance", 150),
       (else_try),
           (lt, "$g_talk_troop_relation", -5),
           (assign, ":comment", "str_comment_we_were_defeated_unfriendly"),
           (assign, ":relevance", 150),
       (else_try),
           (this_or_next|eq, ":reputation", lrep_selfrighteous),
               (eq, ":reputation", lrep_debauched),        
           (assign, ":comment", "str_comment_we_were_defeated_cruel"),
           (assign, ":relevance", 150),
       (else_try),
           (assign, ":comment", "str_comment_we_were_defeated_default"),
           (assign, ":relevance", 150),
       (try_end),

     (else_try),
       (eq, ":entry_type", logent_player_defeated_by_lord),
  	   ##diplomacy start+  Set reg4 for calling scripts
	   (try_begin),
		  (neq, ":troop_object", "$g_talk_troop"),
		  (assign, ":return_reg4", 0),
		  (call_script, "script_cf_dplmc_troop_is_female", ":troop_object"),
		  (assign, ":return_reg4", 1),
	   (try_end),
	   ##diplomacy end+
       (try_begin),
         (eq, ":troop_object", "$g_talk_troop"),
         (this_or_next|eq, ":reputation", lrep_quarrelsome),
                (eq, ":reputation", lrep_debauched),
         (assign, ":comment", "str_comment_I_defeated_you_enemy_spiteful"),
         (assign, ":relevance", 200),
       (else_try),
         (eq, ":troop_object", "$g_talk_troop"),
         (eq, ":reputation", lrep_martial),
         (assign, ":comment", "str_comment_I_defeated_you_enemy_chivalrous"),
         (assign, ":relevance", 200),
       (else_try),
         (eq, ":troop_object", "$g_talk_troop"),
         (this_or_next|eq, ":reputation", lrep_goodnatured),
                (eq, ":reputation", lrep_upstanding),
         (assign, ":comment", "str_comment_I_defeated_you_enemy_benevolent"),
         (assign, ":relevance", 200),
       (else_try),
         (eq, ":troop_object", "$g_talk_troop"),
         (this_or_next|eq, ":reputation", lrep_selfrighteous),
             (eq, ":reputation", lrep_cunning),
         (assign, ":comment", "str_comment_I_defeated_you_enemy_coldblooded"),
         (assign, ":relevance", 200),
       (else_try),
         (eq, ":troop_object", "$g_talk_troop"),
         (assign, ":comment", "str_comment_I_defeated_you_enemy"),
         (assign, ":relevance", 200),
       (else_try),
         (eq, ":troop_object", "$g_talk_troop"),
         (assign, ":comment", "str_comment_I_defeated_you_enemy"),
         (assign, ":relevance", 200),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (this_or_next|eq, ":reputation", lrep_quarrelsome),
                (eq, ":reputation", lrep_debauched),
         (gt, "$g_talk_troop_relation", 5),
         (assign, ":comment", "str_comment_you_were_defeated_allied_friendly_spiteful"),
         (assign, ":relevance", 80),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (this_or_next|eq, ":reputation", lrep_selfrighteous),
                (eq, ":reputation", lrep_debauched),
         (lt, "$g_talk_troop_relation", -5),
         (assign, ":comment", "str_comment_you_were_defeated_allied_unfriendly_cruel"),
         (assign, ":relevance", 80),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (this_or_next|eq, ":reputation", lrep_quarrelsome),
                (eq, ":reputation", lrep_debauched),
         (le, "$g_talk_troop_relation", 5),
         (assign, ":comment", "str_comment_you_were_defeated_allied_spiteful"),
         (assign, ":relevance", 80),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (eq, ":reputation", lrep_selfrighteous),
         (assign, ":comment", "str_comment_you_were_defeated_allied_pitiless"),
         (assign, ":relevance", 65),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (eq, ":reputation", lrep_upstanding),
         (lt, "$g_talk_troop_relation", -15),
         (assign, ":comment", "str_comment_you_were_defeated_allied_unfriendly_upstanding"),
         (assign, ":relevance", 65),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (lt, "$g_talk_troop_relation", -10),
         (assign, ":comment", "str_comment_you_were_defeated_allied_unfriendly"),
         (assign, ":relevance", 65),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (assign, ":comment", "str_comment_you_were_defeated_allied"),
         (assign, ":relevance", 65),
       (try_end),
#Post 0907 changes end

#Post 0907 changes begin
     (else_try),
       (eq, ":entry_type", logent_player_retreated_from_lord),
       (troop_slot_eq, "$g_talk_troop", slot_troop_present_at_event, ":log_entry_no"),
   	   ##diplomacy start+  Set reg4 for calling scripts
	   (try_begin),
		  (neq, ":troop_object", "$g_talk_troop"),
		  (assign, ":return_reg4", 0),
		  (call_script, "script_cf_dplmc_troop_is_female", ":troop_object"),
		  (assign, ":return_reg4", 1),
	   (try_end),
	   ##diplomacy end+
       (try_begin),
           (lt, "$g_talk_troop_relation", -5),
           (this_or_next|eq, ":reputation", lrep_quarrelsome),
               (eq, ":reputation", lrep_debauched),
           (assign, ":comment", "str_comment_you_abandoned_us_unfriendly_spiteful"),
           (assign, ":relevance", 150),
           (assign, ":suggested_relation_change", -5),
       (else_try),
           (lt, "$g_talk_troop_relation", -5),
           (eq, ":reputation", lrep_selfrighteous),        
           (assign, ":comment", "str_comment_you_abandoned_us_unfriendly_pitiless"),
           (assign, ":relevance", 150),
           (assign, ":suggested_relation_change", -5),
       (else_try),
           (lt, "$g_talk_troop_relation", -5),
           (this_or_next|eq, ":reputation", lrep_quarrelsome),
               (eq, ":reputation", lrep_debauched),        
           (assign, ":comment", "str_comment_you_abandoned_us_spiteful"),
           (assign, ":suggested_relation_change", -5),
       (else_try),
           (eq, ":reputation", lrep_martial),
           (assign, ":comment", "str_comment_you_abandoned_us_chivalrous"),
           (assign, ":relevance", 150),
           (assign, ":suggested_relation_change", -2),
       (else_try),
           (this_or_next|eq, ":reputation", lrep_upstanding),
               (eq, ":reputation", lrep_goodnatured),        
           (assign, ":comment", "str_comment_you_abandoned_us_benefitofdoubt"),
           (assign, ":relevance", 150),
           (assign, ":suggested_relation_change", -1),
       (else_try),
           (assign, ":comment", "str_comment_you_abandoned_us_default"),
           (assign, ":relevance", 150),
           (assign, ":suggested_relation_change", -2),
       (try_end),


#Post 0907 changes end

     (else_try),
       (this_or_next|eq, ":entry_type", logent_player_retreated_from_lord),
            (eq, ":entry_type", logent_player_retreated_from_lord_cowardly),
			
       (eq, ":troop_object", "$g_talk_troop"),
       (try_begin),
         (eq, "$cheat_mode", 1),
         (assign, reg7, ":entry_hours_elapsed"),
         (display_message, "@{!}Elapsed hours: {reg7}"),
       (try_end),
       (gt, ":entry_hours_elapsed", 2),
       (try_begin),
         (this_or_next|eq, ":reputation", lrep_selfrighteous),
                (eq, ":reputation", lrep_debauched),
         (assign, ":comment", "str_comment_you_ran_from_me_enemy_spiteful"),
         (assign, ":relevance", 25),
       (else_try),
         (eq, ":reputation", lrep_martial),
         (assign, ":comment", "str_comment_you_ran_from_me_enemy_chivalrous"),
         (assign, ":relevance", 25),
       (else_try),
         (this_or_next|eq, ":reputation", lrep_goodnatured),
                (eq, ":reputation", lrep_upstanding),
         (assign, ":comment", "str_comment_you_ran_from_me_enemy_benevolent"),
         (assign, ":relevance", 25),
       (else_try),
         (eq, ":reputation", lrep_cunning),
         (assign, ":comment", "str_comment_you_ran_from_me_enemy_coldblooded"),
         (assign, ":relevance", 25),
       (else_try),
         (assign, ":comment", "str_comment_you_ran_from_me_enemy"),
         (assign, ":relevance", 25),
       (try_end),

     (else_try),
       (eq, ":entry_type", logent_player_retreated_from_lord_cowardly),
   	   ##diplomacy start+  Set reg4 for calling scripts
	   (try_begin),
		  (neq, ":troop_object", "$g_talk_troop"),
		  (assign, ":return_reg4", 0),
		  (call_script, "script_cf_dplmc_troop_is_female", ":troop_object"),
		  (assign, ":return_reg4", 1),
	   (try_end),
	   ##diplomacy end+
       (try_begin),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (neq, ":troop_object", "$g_talk_troop"),
         (lt, "$g_talk_troop_relation", 5),
         (eq, ":reputation", lrep_martial),
         (assign, ":comment", "str_comment_you_ran_from_foe_allied_chivalrous"),
         (assign, ":relevance", 80),
         (assign, ":suggested_relation_change", -3),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (neq, ":troop_object", "$g_talk_troop"),
         (eq, ":reputation", lrep_upstanding),
         (assign, ":comment", "str_comment_you_ran_from_foe_allied_upstanding"),
         (assign, ":relevance", 80),
         (assign, ":suggested_relation_change", -1),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (neq, ":troop_object", "$g_talk_troop"),
         (lt, "$g_talk_troop_relation", 5),
         (this_or_next|eq, ":reputation", lrep_quarrelsome),
             (eq, ":reputation", lrep_debauched),
         (assign, ":comment", "str_comment_you_ran_from_foe_allied_spiteful"),
         (assign, ":relevance", 80),
       (try_end),

     (else_try),
       (eq, ":entry_type", logent_lord_defeated_but_let_go_by_player),
   	   ##diplomacy start+  Set reg4 for calling scripts
	   (try_begin),
		  (neq, ":troop_object", "$g_talk_troop"),
		  (assign, ":return_reg4", 0),
		  (call_script, "script_cf_dplmc_troop_is_female", ":troop_object"),
		  (assign, ":return_reg4", 1),
	   (try_end),
	   ##diplomacy end+
       (try_begin),
         (eq, ":troop_object", "$g_talk_troop"),
         (this_or_next|eq, ":reputation", lrep_quarrelsome),
             (eq, ":reputation", lrep_debauched),
         (assign, ":comment", "str_comment_you_let_me_go_spiteful"),
         (assign, ":relevance", 300),
         (assign, ":suggested_relation_change", -15),
       (else_try),
         (eq, ":troop_object", "$g_talk_troop"),
         (ge, "$g_talk_troop_faction_relation", 0),
         (assign, ":comment", "str_comment_you_let_me_go_default"),
         (assign, ":relevance", 300),
         (assign, ":suggested_relation_change", 2),
       (else_try),
         (eq, ":troop_object", "$g_talk_troop"),
         (lt, "$g_talk_troop_faction_relation", 0),
         (this_or_next|eq, ":reputation", lrep_martial),
             (eq, ":reputation", lrep_upstanding),
         (assign, ":suggested_relation_change", 5),
         (assign, ":relevance", 300),
         (assign, ":comment", "str_comment_you_let_me_go_enemy_chivalrous"),
       (else_try),
         (eq, ":troop_object", "$g_talk_troop"),
         (lt, "$g_talk_troop_faction_relation", 0),
         (this_or_next|eq, ":reputation", lrep_selfrighteous),
             (eq, ":reputation", lrep_cunning),
         (assign, ":relevance", 300),
         (assign, ":comment", "str_comment_you_let_me_go_enemy_coldblooded"),
       (else_try),
         (eq, ":troop_object", "$g_talk_troop"),
         (lt, "$g_talk_troop_faction_relation", 0),
         (assign, ":relevance", 300),
         (assign, ":comment", "str_comment_you_let_me_go_enemy"),
         (assign, ":suggested_relation_change", 1),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (lt, ":players_kingdom_relation", 0),
         (neq, ":troop_object", "$g_talk_troop"),
         (this_or_next|eq, ":reputation", lrep_martial),
             (eq, ":reputation", lrep_goodnatured),
         (assign, ":comment", "str_comment_you_let_go_a_lord_allied_chivalrous"),
         (assign, ":relevance", 80),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (lt, ":players_kingdom_relation", 0),
         (neq, ":troop_object", "$g_talk_troop"),
         (eq, ":reputation", lrep_upstanding),
         (assign, ":comment", "str_comment_you_let_go_a_lord_allied_upstanding"),
         (assign, ":relevance", 80),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (lt, ":players_kingdom_relation", 0),
         (neq, ":troop_object", "$g_talk_troop"),
         (this_or_next|eq, ":reputation", lrep_cunning),
             (eq, ":reputation", lrep_selfrighteous),
         (assign, ":comment", "str_comment_you_let_go_a_lord_allied_coldblooded"),
         (assign, ":relevance", 80),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (lt, ":players_kingdom_relation", 0),
         (neq, ":troop_object", "$g_talk_troop"),
         (lt, "$g_talk_troop_relation", -5),
         (this_or_next|eq, ":reputation", lrep_quarrelsome),
             (eq, ":reputation", lrep_debauched),
         (assign, ":comment", "str_comment_you_let_go_a_lord_allied_unfriendly_spiteful"),
         (assign, ":relevance", 80),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (lt, ":players_kingdom_relation", 0),
         (neq, ":troop_object", "$g_talk_troop"),
         (assign, ":comment", "str_comment_you_let_go_a_lord_allied"),
         (assign, ":relevance", 80),
       (try_end),

#Internal faction relations

     (else_try),
       (eq, ":entry_type", logent_pledged_allegiance),
       (eq, ":actor", "trp_player"),
       (try_begin),
         (eq, ":faction_object", "$g_talk_troop_faction"),
         (neq, ":troop_object", "$g_talk_troop"),
		 (eq, ":faction_object", "$players_kingdom"), #Ie, no switch of kingdoms
         (assign, ":relevance", 200),
         (try_begin),
            (lt, "$g_talk_troop_relation", -5),
            (eq, ":reputation", lrep_martial),
            (assign, ":comment", "str_comment_pledged_allegiance_allied_martial_unfriendly"),
         (else_try),
            (eq, ":reputation", lrep_martial),
            (assign, ":comment", "str_comment_pledged_allegiance_allied_martial"),
         (else_try),
            (lt, "$g_talk_troop_relation", -5),
            (eq, ":reputation", lrep_quarrelsome),
            (assign, ":comment", "str_comment_pledged_allegiance_allied_quarrelsome_unfriendly"),
         (else_try),
            (eq, ":reputation", lrep_quarrelsome),
            (assign, ":comment", "str_comment_pledged_allegiance_allied_quarrelsome"),
         (else_try),
            (lt, "$g_talk_troop_relation", -5),
            (eq, ":reputation", lrep_selfrighteous),
            (assign, ":comment", "str_comment_pledged_allegiance_allied_selfrighteous_unfriendly"),
         (else_try),
            (eq, ":reputation", lrep_selfrighteous),
            (assign, ":comment", "str_comment_pledged_allegiance_allied_selfrighteous"),
         (else_try),
            (lt, "$g_talk_troop_relation", -5),
            (eq, ":reputation", lrep_cunning),
            (assign, ":comment", "str_comment_pledged_allegiance_allied_cunning_unfriendly"),
         (else_try),
            (eq, ":reputation", lrep_cunning),
            (assign, ":comment", "str_comment_pledged_allegiance_allied_cunning"),
         (else_try),
            (lt, "$g_talk_troop_relation", -5),
            (eq, ":reputation", lrep_debauched),
            (assign, ":comment", "str_comment_pledged_allegiance_allied_debauched_unfriendly"),
         (else_try),
            (eq, ":reputation", lrep_debauched),
            (assign, ":comment", "str_comment_pledged_allegiance_allied_debauched"),
         (else_try),
            (lt, "$g_talk_troop_relation", -5),
            (eq, ":reputation", lrep_goodnatured),
            (assign, ":comment", "str_comment_pledged_allegiance_allied_goodnatured_unfriendly"),
         (else_try),
            (eq, ":reputation", lrep_goodnatured),
            (assign, ":comment", "str_comment_pledged_allegiance_allied_goodnatured"),
         (else_try),
            (lt, "$g_talk_troop_relation", -5),
            (eq, ":reputation", lrep_upstanding),
            (assign, ":comment", "str_comment_pledged_allegiance_allied_upstanding_unfriendly"),
         (else_try),
            (eq, ":reputation", lrep_upstanding),
            (assign, ":comment", "str_comment_pledged_allegiance_allied_upstanding"),
         (try_end),
       (try_end),


     (else_try),
       (eq, ":entry_type", logent_liege_grants_fief_to_vassal),
       (eq, ":troop_object", "trp_player"),
       (try_begin),
         (eq, ":faction_object", "$g_talk_troop_faction"),
         (neq, ":actor", "$g_talk_troop"),
         (eq, ":faction_object", "$players_kingdom"),
         (assign, ":relevance", 110),
         (try_begin),
            (gt, "$g_talk_troop_relation", 5),
            (this_or_next|eq, ":reputation", lrep_selfrighteous),
                (eq, ":reputation", lrep_debauched),
            (assign, ":comment", "str_comment_our_king_granted_you_a_fief_allied_friendly_cruel"),
         (else_try),
            (gt, "$g_talk_troop_relation", 5),
            (this_or_next|eq, ":reputation", lrep_quarrelsome),
                (eq, ":reputation", lrep_cunning),
            (assign, ":comment", "str_comment_our_king_granted_you_a_fief_allied_friendly_cynical"),
         (else_try),
            (gt, "$g_talk_troop_relation", 5),
            (assign, ":comment", "str_comment_our_king_granted_you_a_fief_allied_friendly"),
         (else_try),
            (is_between, "$g_talk_troop_relation", -5, 5),
            (this_or_next|eq, ":reputation", lrep_quarrelsome),
                (eq, ":reputation", lrep_debauched),
            (assign, ":comment", "str_comment_our_king_granted_you_a_fief_allied_spiteful"),
            (assign, ":suggested_relation_change", -2),
         (else_try),
            (lt, "$g_talk_troop_relation", -5),
            (eq, ":reputation", lrep_upstanding),
            (assign, ":comment", "str_comment_our_king_granted_you_a_fief_allied_unfriendly_upstanding"),
         (else_try),
            (lt, "$g_talk_troop_relation", -5),
            (this_or_next|eq, ":reputation", lrep_quarrelsome),
                (eq, ":reputation", lrep_debauched),
            (assign, ":comment", "str_comment_our_king_granted_you_a_fief_allied_unfriendly_spiteful"),
         (else_try),
            (assign, ":comment", "str_comment_our_king_granted_you_a_fief_allied"),
         (try_end),
       (try_end),

     (else_try),
       (eq, ":entry_type", logent_renounced_allegiance),
       (eq, ":actor", "trp_player"),
       (try_begin),
         (eq, ":faction_object", "$g_talk_troop_faction"),
         (neq, ":troop_object", "$g_talk_troop"),
         (try_begin),
           (ge, "$g_talk_troop_faction_relation", 0),
           (neq, "$g_talk_troop_faction", "$players_kingdom"),
           (assign, ":relevance", 180),
           (try_begin),
             (gt, "$g_talk_troop_relation", 5),
             (assign, ":comment", "str_comment_you_renounced_your_alliegance_friendly"),
           (else_try),
             (ge, "$g_talk_troop_relation", 0),
             (eq, ":reputation", lrep_goodnatured),
             (assign, ":comment", "str_comment_you_renounced_your_alliegance_friendly"),
		   (else_try),
		     (assign, ":comment", "str_comment_you_renounced_your_alliegance_default"),
           (try_end),
         (else_try),
           (lt, "$g_talk_troop_faction_relation", 0),
           (assign, ":relevance", 300),
           (try_begin),
              (ge, "$g_talk_troop_relation", 0),
              (this_or_next|eq, ":reputation", lrep_selfrighteous),
                  (eq, ":reputation", lrep_debauched),
              (assign, ":comment", "str_comment_you_renounced_your_alliegance_unfriendly_moralizing"),
           (else_try),
              (gt, "$g_talk_troop_relation", 5),
              (this_or_next|eq, ":reputation", lrep_goodnatured),
                (eq, ":reputation", lrep_upstanding),
              (assign, ":comment", "str_comment_you_renounced_your_alliegance_enemy_friendly"),
           (else_try),
              (gt, "$g_talk_troop_relation", 5),
              (assign, ":comment", "str_comment_you_renounced_your_alliegance_enemy"),
           (else_try),
              (is_between, "$g_talk_troop_relation", -5, 5),
              (this_or_next|eq, ":reputation", lrep_quarrelsome),
                  (eq, ":reputation", lrep_debauched),
              (assign, ":comment", "str_comment_you_renounced_your_alliegance_unfriendly_spiteful"),
              (assign, ":suggested_relation_change", -2),
           (else_try),
              (lt, "$g_talk_troop_relation", -5),
              (this_or_next|eq, ":reputation", lrep_quarrelsome),
              (this_or_next|eq, ":reputation", lrep_selfrighteous),
                (eq, ":reputation", lrep_debauched),
              (assign, ":comment", "str_comment_you_renounced_your_alliegance_unfriendly_spiteful"),
           (else_try),
              (assign, ":comment", "str_comment_you_renounced_your_alliegance_default"),
           (try_end),
         (try_end),
       (try_end),

     (else_try),
       (eq, ":entry_type", logent_lady_marries_lord),
	   (eq, ":troop_object", "trp_player"),
   	   ##diplomacy start+  Set reg4 for calling scripts
	   (try_begin),
		  (neq, ":actor", "$g_talk_troop"),
		  (assign, ":return_reg4", 0),
		  (call_script, "script_cf_dplmc_troop_is_female", ":actor"),
		  (assign, ":return_reg4", 1),
	   (try_end),
	   ##diplomacy end+
	   (try_begin),
		  (this_or_next|eq, ":reputation", lrep_quarrelsome),
			(eq, ":reputation", lrep_debauched),
		  (lt, "$g_talk_troop_relation", -5),
          (assign, ":relevance", 200),
		  (assign, ":comment", "str_comment_marriage_normal_nasty"),
	   (else_try),
		  (call_script, "script_troop_get_family_relation_to_troop", ":actor", "$g_talk_troop"),
		  (ge, reg0, 5),
		  (assign, ":comment", "str_comment_marriage_normal_family"),
          (assign, ":relevance", 300),
		  (assign, ":suggested_relation_change", reg0),
		  (val_div, ":suggested_relation_change", 3),
	   (else_try),
		  (store_faction_of_troop, ":bride_faction", ":actor"),
		  (eq, ":bride_faction", "$g_talk_troop_faction"),
		  (assign, ":comment", "str_comment_marriage_normal"),
          (assign, ":relevance", 100),
	   (try_end),
     (else_try),
       (eq, ":entry_type", logent_lady_elopes_with_lord),
	   (eq, ":troop_object", "trp_player"),
  	   ##diplomacy start+  Set reg4 for calling scripts
	   (try_begin),
		  (neq, ":actor", "$g_talk_troop"),
		  (assign, ":return_reg4", 0),
		  (call_script, "script_cf_dplmc_troop_is_female", ":troop_object"),
		  (assign, ":return_reg4", 1),
	   (try_end),
	   ##diplomacy end+
	   (try_begin),
		  (call_script, "script_troop_get_family_relation_to_troop", ":actor", "$g_talk_troop"),
		  (ge, reg0, 5),
		  (assign, ":comment", "str_comment_marriage_elopement_family"),
          (assign, ":relevance", 300),
		  (store_sub, ":suggested_relation_change", 0, reg0),
		  (val_div, ":suggested_relation_change", 3),
	   (else_try),
		  (store_faction_of_troop, ":bride_faction", ":actor"),
		  (eq, ":bride_faction", "$g_talk_troop_faction"),
		  (faction_slot_eq, ":bride_faction", slot_faction_leader, "$g_talk_troop"),
		  (assign, ":comment", "str_comment_marriage_elopement_liege"),
          (assign, ":relevance", 300),
		  (assign, ":suggested_relation_change", -10),
	   (try_end),
     (else_try), #this is specific to quarrels with the player 
       (eq, ":entry_type", logent_lords_quarrel_over_woman),
 	   (eq, ":actor", "$g_talk_troop"),
 	   (eq, ":center_object", "trp_player"),

	   (neg|troop_slot_ge, ":troop_object", slot_troop_spouse, "trp_player"),

	   (str_store_troop_name, s54, ":troop_object"),
   	   ##diplomacy start+  Set reg4 for calling scripts
	   (assign, ":return_reg4", 0),
	   (try_begin),
		  (call_script, "script_cf_dplmc_troop_is_female", ":troop_object"),
		  (assign, ":return_reg4", 1),
	   (try_end),
	   ##diplomacy end+
	   (try_begin),
	       (this_or_next|eq, ":reputation", lrep_selfrighteous),
	       (this_or_next|eq, ":reputation", lrep_quarrelsome),
				(eq, ":reputation", lrep_debauched),
		   
	       (assign, ":comment", "str_comment_i_quarreled_with_you_over_woman_derisive"),
		   (assign, ":relevance", 200),
	       (assign, ":suggested_relation_change", -20),
	   (else_try),
	       (assign, ":comment", "str_comment_i_quarreled_with_you_over_woman_default"),
		   (assign, ":relevance", 200),
	       (assign, ":suggested_relation_change", -20),
	   (try_end),
	 
     (else_try), 
       (eq, ":entry_type", logent_border_incident_troop_breaks_truce),
 	   (eq, ":actor", "trp_player"),
 	   (faction_slot_eq, ":faction_object", slot_faction_leader, "$g_talk_troop"),
	   (eq, "$players_kingdom", ":faction_object"),
	   
	   (assign, ":suggested_relation_change", -10),
	   (assign, ":comment", "str_comment_you_broke_truce_as_my_vassal"),
	   (assign, ":relevance", 300),

     (else_try), 
       (eq, ":entry_type", logent_border_incident_troop_attacks_neutral),
 	   (eq, ":actor", "trp_player"),
 	   (faction_slot_eq, ":faction_object", slot_faction_leader, "$g_talk_troop"),
	   (eq, "$players_kingdom", ":faction_object"),

	   (assign, ":suggested_relation_change", -3),
	   (assign, ":comment", "str_comment_you_attacked_neutral_as_my_vassal"),
	   (assign, ":relevance", 200),

	 #THE FOLLOWING ARE ALL COMPLAINTS SPOKEN BY LORDS WITHIN CONVERATIONS, RATHER THAN COMMENTS WHEN THE PLAYER FIRST SPEAKS TO A LORD
	 (else_try), #these need to have the actor and object strings added because they are used outside of "script_get_relevant_comment_to_s42"
       (eq, ":entry_type", logent_ruler_intervenes_in_quarrel),
 	   (eq, ":center_object", "$g_talk_troop"), #actor is liege lord, center object is loser lord, troop object is winner lord
	   (str_store_troop_name, s50, ":actor"), 
	   (str_store_troop_name, s51, ":center_object"), #s50 is actor, s51 is center object, s54 is troop object
	   (str_store_troop_name, s54, ":troop_object"), #s50 is actor, s51 is center object, s54 is troop object
       (assign, ":comment", "str_comment_lord_intervened_against_me"),
	   (assign, ":relevance", -1),

	 (else_try),
       (eq, ":entry_type", logent_lord_protests_marshall_appointment),
 	   (eq, ":actor", "$g_talk_troop"),

	   (str_store_troop_name, s51, ":center_object"), #s51 is center object (marshall), s54 is troop object (liege lord), 
	   (str_store_troop_name, s54, ":troop_object"), 

       (assign, ":comment", "str_comment_i_protested_marshall_appointment"),
	   (assign, ":relevance", -1),
	   
	 (else_try),
       (eq, ":entry_type", logent_lord_blames_defeat),
 	   (eq, ":actor", "$g_talk_troop"),

	   (str_store_troop_name, s51, ":center_object"), #s51 is center object (marshall), s54 is troop object (liege lord), 
	   (str_store_troop_name, s54, ":troop_object"),  
	   (str_store_troop_name, s56, ":faction_object"), #faction object is unusual in this circumstance
	   
       (assign, ":comment", "str_comment_i_blamed_defeat"),
	   (assign, ":relevance", -1),

	 (else_try),
       (eq, ":entry_type", logent_troop_feels_cheated_by_troop_over_land),
 	   (eq, ":actor", "$g_talk_troop"),

	   ##diplomacy start+ fix fief quarrel comment bug (where the name of a random troop replaces the name of the center)
	   (str_store_party_name, s51, ":center_object"),#str_store_troop_name -> str_store_party_name
	   ##diplomacy end+
	   (str_store_troop_name, s54, ":troop_object"),
	   (str_store_troop_name, s56, ":faction_object"), #faction object is unusual in this circumstance
	   
       (assign, ":comment", "str_comment_i_was_entitled_to_fief"),
	   (assign, ":relevance", -1),
	   
	 (else_try),
       (eq, ":entry_type", logent_lords_quarrel_over_woman),
 	   (eq, ":actor", "$g_talk_troop"),

	   (str_store_troop_name, s51, ":center_object"),
	   (str_store_troop_name, s54, ":troop_object"),
	   ##diplomacy start+  Set reg4 and reg3 for calling scripts
	   #(assign, reg3, 0),# #Exclude reg3, since it is used for output anyway
	   #(try_begin),
	   #  (call_script, "script_cf_dplmc_troop_is_female", ":center_object"),
	   #  (assign, reg3, 1),
	   #(try_end),
	   (assign, ":return_reg4", 0),
	   (try_begin),
		  (call_script, "script_cf_dplmc_troop_is_female", ":troop_object"),
		  (assign, ":return_reg4", 1),
	   (try_end),
	   ##diplomacy end+

       (assign, ":comment", "str_comment_i_quarreled_with_troop_over_woman"),
	   (assign, ":relevance", -1),

	 (else_try),
       (eq, ":entry_type", logent_lords_quarrel_over_woman),
 	   (eq, ":center_object", "$g_talk_troop"),

	   (str_store_troop_name, s51, ":actor"),
	   (str_store_troop_name, s54, ":troop_object"),
	   ##diplomacy start+  Set reg4 and reg3 for calling scripts
	   #(assign, reg3, 0),#Exclude reg3, since it is used for output anyway
	   #(try_begin),
	   #  (call_script, "script_cf_dplmc_troop_is_female", ":actor"),
	   #  (assign, reg3, 1),
	   #(try_end),
	   (assign, ":return_reg4", 0),
	   (try_begin),
		  (call_script, "script_cf_dplmc_troop_is_female", ":troop_object"),
		  (assign, ":return_reg4", 1),
	   (try_end),
	   ##diplomacy end+

       (assign, ":comment", "str_comment_i_quarreled_with_troop_over_woman"),
	   (assign, ":relevance", -1),
	   
	 (else_try),	 
       (eq, ":entry_type", logent_player_stole_cattles_from_village),
       
       (eq, ":actor", "trp_player"),
       (try_begin),
         (eq, ":center_object_lord", "$g_talk_troop"),
         (assign, ":relevance", 200),
         (assign, ":suggested_relation_change", -1),
         (assign, ":comment", "str_comment_you_stole_cattles_from_my_village_default"),
         (try_begin),
            (lt, "$g_talk_troop_faction_relation", -3),
            (this_or_next|eq, ":reputation", lrep_goodnatured),
            (eq, ":reputation", lrep_upstanding),
            (assign, ":comment", "str_comment_you_stole_cattles_from_my_village_enemy_benevolent"),
         (else_try),
            (lt, "$g_talk_troop_faction_relation", -3),
            (this_or_next|eq, ":reputation", lrep_cunning),
                (eq, ":reputation", lrep_selfrighteous),
            (assign, ":comment", "str_comment_you_stole_cattles_from_my_village_enemy_coldblooded"),
         (else_try),
            (lt, "$g_talk_troop_faction_relation", -3),
            (this_or_next|eq, ":reputation", lrep_quarrelsome),
                (eq, ":reputation", lrep_debauched),
            (assign, ":comment", "str_comment_you_stole_cattles_from_my_village_enemy_spiteful"),
         (else_try),
            (lt, "$g_talk_troop_faction_relation", -3),
            (assign, ":comment", "str_comment_you_stole_cattles_from_my_village_enemy"),
         (else_try),
            (lt, "$g_talk_troop_relation", -3),
            (this_or_next|eq, ":reputation", lrep_quarrelsome),
                (eq, ":reputation", lrep_debauched),
            (assign, ":comment", "str_comment_you_stole_cattles_from_my_village_unfriendly_spiteful"),
         (else_try),
            (gt, "$g_talk_troop_relation", 6),
            (assign, ":comment", "str_comment_you_stole_cattles_from_my_village_friendly"),
         (try_end),
       (try_end),
             	   
     (try_end),

     (assign, reg0, ":comment"),
	 (assign, reg1, ":relevance"),
     (assign, reg2, ":suggested_relation_change"),
     (assign, reg3, ":rejoinder"),
	 ##diplomacy start+
	 (assign, reg4, ":return_reg4"),
	 ##diplomacy end+
	]),
  # script_get_relevant_comment_to_s42
  # Input: none
  # Output: reg0 = 1 if comment found, 0 otherwise; s61 will contain comment string if found
  ("get_relevant_comment_to_s42",
    [

	 (troop_get_slot, ":reputation", "$g_talk_troop", slot_lord_reputation_type),
     (try_begin),
	   (eq, "$cheat_mode", 1),
       (store_add, ":rep_string", ":reputation", "str_personality_archetypes"),
       (str_store_string, s15, ":rep_string"),
       (display_message, "@{!}Reputation type: {s15}"),
     (try_end),

	 
     (assign, ":highest_score_so_far", 50),
     (assign, ":best_comment_so_far", -1),
     (assign, ":rejoinder_to_best_comment_so_far", -1),
     (assign, ":comment_found", 0),
     (assign, ":best_log_entry", -1),
     (assign, ":comment_relation_change", 0),
     (store_current_hours, ":current_time"),
	 ##diplomacy start+
	 (assign, ":best_comment_reg4", 0),
	 ##diplomacy end+

#prevents multiple comments in conversations in same hour

#     (troop_get_slot, ":talk_troop_last_comment_time", "$g_talk_troop", slot_troop_last_comment_time),
#"$num_log_entries should also be set to one, not zero. This is included in the initialize npcs script, although could be moved to game_start
     (troop_get_slot, ":talk_troop_last_comment_slot", "$g_talk_troop", slot_troop_last_comment_slot),
     (troop_set_slot, "$g_talk_troop", slot_troop_last_comment_slot, "$num_log_entries"),

     (store_add, ":log_entries_plus_one", "$num_log_entries", 1),
     (try_for_range, ":log_entry_no", 1, ":log_entries_plus_one"),
#      It should be log entries plus one, so that the try_ sequence does not stop short of the last log entry
#      $Num_log_entries is now the number of the last log entry, which begins at "1" rather than "0"
#      This is so that (le, ":log_entry_no", ":talk_troop_last_comment_slot") works properly
     
       (troop_get_slot, ":entry_time",           "trp_log_array_entry_time",           ":log_entry_no"),
#      (val_max, ":entry_time", 1), #This is needed for pre-game events to be commented upon, if hours are used rather than the order of events
       (store_sub, ":entry_hours_elapsed", ":current_time", ":entry_time"),
       (try_begin),
         (le, ":log_entry_no", ":talk_troop_last_comment_slot"),
#         (le, ":entry_time", ":talk_troop_last_comment_time"),
         (try_begin),
           (eq, ":log_entry_no", ":talk_troop_last_comment_slot"),
           (eq, "$cheat_mode", 1),
           (assign, reg5, ":log_entry_no"),
           (display_message, "@{!}Entries up to #{reg5} skipped"),
         (try_end),
#       I suggest using the log entry number as opposed to time so that events in the same hour can be commented upon
#       This feels more natural, for example, if there are other lords in the court when the player pledges allegiance     
       (else_try),
#         (le, ":entry_hours_elapsed", 3), #don't comment on really fresh events 
#       (else_try),
         (call_script, "script_get_relevant_comment_for_log_entry", ":log_entry_no"),
         (gt, reg1, 10),
         (assign, ":score", reg1),
         (assign, ":comment", reg0),
		 #reg2 is what
		 (assign, ":rejoinder", reg3),
		 
         (store_random_in_range, ":rand", 70, 140),
         (val_mul, ":score", ":rand"),
         (store_add, ":entry_time_score", ":entry_hours_elapsed", 500), #approx. one month 
         (val_mul, ":score", 1000),
         (val_div, ":score", ":entry_time_score"), ###Relevance decreases over time - halved after one month, one-third after two, etc
         (try_begin),
           (gt, ":score", ":highest_score_so_far"),
           (assign, ":highest_score_so_far", ":score"),
           (assign, ":best_comment_so_far",  ":comment"),
           (assign, ":rejoinder_to_best_comment_so_far",  ":rejoinder"),
           (assign, ":best_log_entry", ":log_entry_no"),
           (assign, ":comment_relation_change", reg2),
		   ##diplomacy start+
		   (assign, ":best_comment_reg4", reg4),
		   ##diplomacy end+
         (try_end),
       (try_end),
     (try_end),

     (try_begin),
       (gt, ":best_comment_so_far", 0),
       (assign, ":comment_found", 1), #comment found print it to s61 now. 
       (troop_get_slot, ":actor",                 "trp_log_array_actor",                 ":best_log_entry"),
       (troop_get_slot, ":center_object",         "trp_log_array_center_object",         ":best_log_entry"),
       (troop_get_slot, ":center_object_lord",    "trp_log_array_center_object_lord",    ":best_log_entry"),
       (troop_get_slot, ":center_object_faction", "trp_log_array_center_object_faction", ":best_log_entry"),
       (troop_get_slot, ":troop_object",          "trp_log_array_troop_object",          ":best_log_entry"),
       (troop_get_slot, ":troop_object_faction",  "trp_log_array_troop_object_faction",  ":best_log_entry"),
       (troop_get_slot, ":faction_object",        "trp_log_array_faction_object",        ":best_log_entry"),
	   ##diplomacy start+
	   (assign, reg4, ":best_comment_reg4"),
	   ##diplomacy end+
       (try_begin),
         (ge, ":actor", 0),
         (str_store_troop_name,   s50, ":actor"),
		 ##diplomacy start+
		 (eq, ":best_comment_so_far", "str_comment_i_quarreled_with_troop_over_woman"),
		 (neq, ":actor", "$g_talk_troop"),
		 (neq, ":actor", "trp_player"),
		 (assign, reg3, 0),
		 (try_begin),
			(call_script, "script_cf_dplmc_troop_is_female", ":actor"),
			(assign, reg3, 1),
		 (try_end),
		 ##diplomacy end+
       (try_end),
       (try_begin),
         (ge, ":center_object", 0),
		 ##diplomacy start+
		 ##OLD:
         #(str_store_party_name,   s51, ":center_object"),
		 ##NEW:
		 #Alternate meaning (not usually called from this script, but just in case)
		 #In this case, s51 is actually a troop.  Use reg3 for the gender.
		 (try_begin),
			(eq, ":best_comment_so_far", "str_comment_i_quarreled_with_troop_over_woman"),
			(str_store_troop_name, s51, ":center_object"),
			(neq, ":center_object", "$g_talk_troop"),
			(neq, ":center_object", "trp_player"),
			(call_script, "script_dplmc_store_troop_is_female_reg", ":center_object", 3),
		 (else_try),
		   (neq, ":best_comment_so_far", "str_comment_i_quarreled_with_troop_over_woman"),
 		   (str_store_party_name,   s51, ":center_object"),#<- old behavior
  	    (try_end),
		##diplomacy end+
       (try_end),
       (try_begin),
         (ge, ":center_object_lord", 0),
         (str_store_troop_name,   s52, ":center_object_lord"),
       (try_end),
       (try_begin),
         (ge, ":center_object_faction", 0),
         (str_store_faction_name, s53, ":center_object_faction"),
       (try_end),
       (try_begin),
         (ge, ":troop_object", 0),
         (str_store_troop_name,   s54, ":troop_object"),
       (try_end),
       (try_begin),
         (is_between, ":troop_object_faction", kingdoms_begin, kingdoms_end),
         (str_store_faction_name, s55, ":troop_object_faction"),
         (str_store_string, s55, "str_the_s55"),
	   (else_try), 
		 (is_between, ":troop_object", bandits_begin, bandits_end),
         (str_store_string, s55, "str_bandits"),
	   (else_try),
	     (eq, ":troop_object_faction", "fac_deserters"),
         (str_store_string, s55, "str_deserters"),
       (else_try),
         (str_store_string, s55, "str_travellers_on_the_road"),
	   (else_try),
	   
       (try_end),
	   
       (try_begin),
         (ge, ":faction_object", 0),
         (str_store_faction_name, s56, ":faction_object"),
       (try_end),
	   (assign, "$g_last_comment_copied_to_s42", ":best_comment_so_far"), #maybe deprecate
	   (assign, "$g_rejoinder_to_last_comment", ":rejoinder_to_best_comment_so_far"),
	   
       (str_store_string, s42, ":best_comment_so_far"),
     (try_end),
     
     (assign, reg0, ":comment_found"),
	 
     (assign, "$log_comment_relation_change", ":comment_relation_change"),
     ]),
#	 
  ("merchant_road_info_to_s42", #also does itemss to s32
    [
	(store_script_param, ":center", 1),
	
	(assign, ":last_bandit_party_found", -1),
	(assign, ":last_bandit_party_origin", -1),
	(assign, ":last_bandit_party_destination", -1),
	(assign, ":last_bandit_party_hours_ago", -1),
	
	(str_clear, s32),
	
	(str_clear, s42), 
	(str_clear, s47), #safe roads
	
	(try_for_range, ":center_to_reset", centers_begin, centers_end),
		(party_set_slot, ":center_to_reset", slot_party_temp_slot_1, 0),
	(try_end),

	(assign, ":road_attacks", 0),
	(assign, ":trades", 0),
	
#first mention all attacks	
    (try_for_range, ":log_entry_iterator", 0, "$num_log_entries"),
		(store_sub, ":log_entry_no", "$num_log_entries", ":log_entry_iterator"),
#how long ago?
        (this_or_next|troop_slot_eq, "trp_log_array_entry_type", ":log_entry_no", logent_traveller_attacked),
			(troop_slot_eq, "trp_log_array_entry_type", ":log_entry_no", logent_party_traded),

#       reference - (call_script, "script_add_log_entry", logent_traveller_attacked, ":winner_party" (actor),  ":origin" (center object), ":destination" (troop_object), ":winner_faction"),
			
        (troop_get_slot, ":origin",         "trp_log_array_center_object",         ":log_entry_no"),
        (troop_get_slot, ":destination",    "trp_log_array_troop_object",          ":log_entry_no"),
		
		(this_or_next|eq, ":origin", ":center"),
			(eq, ":destination", ":center"),
		
	
        (troop_get_slot, ":event_time",            "trp_log_array_entry_time",              ":log_entry_no"),
		(store_current_hours, ":cur_hour"),
		(store_sub, ":hours_ago", ":cur_hour", ":event_time"),
		(assign, reg3, ":hours_ago"),

		(lt, ":hours_ago", 672), #four weeks
		
		(try_begin),
			(eq, "$cheat_mode", 1),
			(troop_slot_eq, "trp_log_array_entry_type", ":log_entry_no", logent_traveller_attacked),
			(display_message, "str_attack_on_travellers_found_reg3_hours_ago"),
		(else_try),	
			(eq, "$cheat_mode", 1),
			(troop_slot_eq, "trp_log_array_entry_type", ":log_entry_no", logent_party_traded),
			(display_message, "str_trade_event_found_reg3_hours_ago"),
		(try_end),

		(try_begin), #possibly make script -- get_colloquial_for_time
			(lt, ":hours_ago", 24),
			(str_store_string, s46, "str_a_short_while_ago"),
		(else_try),
			(lt, ":hours_ago", 48),
			(str_store_string, s46, "str_one_day_ago"),
		(else_try),	
			(lt, ":hours_ago", 72),
			(str_store_string, s46, "@two days ago"),
		(else_try),	
			(lt, ":hours_ago", 154),
			(str_store_string, s46, "str_earlier_this_week"),
		(else_try),
			(lt, ":hours_ago", 240),
			(str_store_string, s46, "str_about_a_week_ago"),
		(else_try),
			(lt, ":hours_ago", 480),
			(str_store_string, s46, "str_about_two_weeks_ago"),
		(else_try),
			(str_store_string, s46, "str_several_weeks_ago"),
		(try_end),


			
        (troop_get_slot, ":actor", "trp_log_array_actor", ":log_entry_no"),
        (troop_get_slot, ":faction_object", "trp_log_array_faction_object", ":log_entry_no"),
	 
		(str_store_string, s39, "str_unknown_assailants"),
		(assign, ":assailants_known", -1),
		(try_begin),
			(party_is_active, ":actor"),
			(store_faction_of_party, ":actor_faction", ":actor"),
			(eq, ":faction_object", ":actor_faction"),
			(assign, ":assailants_known", ":actor"),
			(str_store_party_name, s39, ":assailants_known"),
			(assign, "$g_bandit_party_for_bounty", -1),
			(try_begin), #possibly make script -- get_colloquial_for_faction
				(eq, ":faction_object", "fac_kingdom_1"),
				(str_store_string, s39, "str_uesugi"),
			(else_try),	
				(eq, ":faction_object", "fac_kingdom_2"),
				(str_store_string, s39, "str_date"),
			(else_try),	
				(eq, ":faction_object", "fac_kingdom_3"),
				(str_store_string, s39, "str_oda"),
			(else_try),	
				(eq, ":faction_object", "fac_kingdom_4"),
				(str_store_string, s39, "str_mori"),
			(else_try),	
				(eq, ":faction_object", "fac_kingdom_5"),
				(str_store_string, s39, "str_takeda"),
			(else_try),	
				(eq, ":faction_object", "fac_kingdom_6"),
				(str_store_string, s39, "str_tokugawa"),
			(else_try),	
				(eq, ":faction_object", "fac_kingdom_7"),
				(str_store_string, s39, "str_miyoshi"),
			(else_try),	
				(eq, ":faction_object", "fac_kingdom_8"),
				(str_store_string, s39, "str_amako"),
			(else_try),	
				(eq, ":faction_object", "fac_kingdom_9"),
				(str_store_string, s39, "str_otomo"),
			(else_try),	
				(eq, ":faction_object", "fac_kingdom_10"),
				(str_store_string, s39, "str_nanbu"),
			(else_try),	
				(eq, ":faction_object", "fac_kingdom_11"),
				(str_store_string, s39, "str_asakura"),
			(else_try),	
				(eq, ":faction_object", "fac_kingdom_12"),
				(str_store_string, s39, "str_chosokabe"),
			(else_try),	
				(eq, ":faction_object", "fac_kingdom_13"),
				(str_store_string, s39, "str_hojo"),
			(else_try),	
				(eq, ":faction_object", "fac_kingdom_14"),
				(str_store_string, s39, "str_mogami"),
			(else_try),	
				(eq, ":faction_object", "fac_kingdom_15"),
				(str_store_string, s39, "str_shimazu"),
			(else_try),	
				(eq, ":faction_object", "fac_kingdom_16"),
				(str_store_string, s39, "str_ryuzoji"),
			(else_try),	
				(eq, ":faction_object", "fac_kingdom_17"),
				(str_store_string, s39, "str_satake"),
			(else_try),	
				(eq, ":faction_object", "fac_kingdom_18"),
				(str_store_string, s39, "str_satomi"),
			(else_try),	
				(eq, ":faction_object", "fac_kingdom_19"),
				(str_store_string, s39, "str_ukita"),
			(else_try),	
				(eq, ":faction_object", "fac_kingdom_20"),
				(str_store_string, s39, "str_ikko"),
			(else_try),
				(eq, ":faction_object", "fac_player_supporters_faction"),
				(str_store_string, s39, "str_your_followers"),
			(else_try), #bandits	
				(assign, ":last_bandit_party_found", ":assailants_known"),
				(assign, ":last_bandit_party_origin", ":origin"),
				(assign, ":last_bandit_party_destination", ":destination"),
				(assign, ":last_bandit_party_hours_ago", ":hours_ago"),
			(try_end),
		(try_end),
	 
		(try_begin),
			(eq, ":origin", ":center"),
			(troop_slot_eq, "trp_log_array_entry_type", ":log_entry_no", logent_traveller_attacked),
			(party_slot_eq, ":destination", slot_party_temp_slot_1, 0),

			(party_set_slot, ":destination", slot_party_temp_slot_1, 1),
			(str_store_party_name, s40, ":destination"),
			(str_store_string, s44, "str_we_have_heard_that_travellers_heading_to_s40_were_attacked_on_the_road_s46_by_s39"),
			(str_store_string, s43, "str_s42"),
			(str_store_string, s42, "str_s43_s44"),

			(val_add, ":road_attacks", 1),
			#travellers were attacked on the road to...			
		(else_try),
			(eq, ":destination", ":center"),
			(troop_slot_eq, "trp_log_array_entry_type", ":log_entry_no", logent_traveller_attacked),
			(party_slot_eq, ":origin", slot_party_temp_slot_1, 0),

			(party_set_slot, ":origin", slot_party_temp_slot_1, 1),
			(str_store_party_name, s40, ":origin"),
			(str_store_string, s44, "str_we_have_heard_that_travellers_coming_from_s40_were_attacked_on_the_road_s46_by_s39"),

			(str_store_string, s43, "str_s42"),
			(str_store_string, s42, "str_s43_s44"),

			(val_add, ":road_attacks", 1),

		#travellers from here traded at...
#		(else_try),
#			(eq, ":origin", ":center"),
#			(troop_slot_eq, "trp_log_array_entry_type", ":log_entry_no", logent_party_traded),
#			(party_slot_eq, ":destination", slot_party_temp_slot_1, 0),

#			(party_set_slot, ":destination", slot_party_temp_slot_1, 1),
#			(str_store_party_name, s40, ":destination"),
#			(str_store_string, s44, "@Travellers headed to {s40} traded there {s46}"),
#			(str_store_string, s43, "@{s42"),
#			(str_store_string, s42, "str_s43_s44"),

			#caravan from traded at...
		(else_try),
			(eq, ":destination", ":center"),
			(troop_slot_eq, "trp_log_array_entry_type", ":log_entry_no", logent_party_traded),
			(party_slot_eq, ":origin", slot_party_temp_slot_1, 0),

			(party_set_slot, ":origin", slot_party_temp_slot_1, 1),
			(str_store_party_name, s40, ":origin"),
			(str_store_string, s44, "str_travellers_coming_from_s40_traded_here_s46"),
			(str_store_string, s43, "str_s42"),
			(str_store_string, s42, "str_s43_s44"),

			(val_add, ":trades", 1),

			#caravan from traded at...
		(try_end),
		
	(try_end),

	
	(try_begin),
		(le, ":trades", 2),
		(eq, ":road_attacks", 0),
		(store_current_hours, ":hours"),
		(lt, ":hours", 168),
		(str_store_string, s42, "str_it_is_still_early_in_the_caravan_season_so_we_have_seen_little_tradings42"),
	(else_try),
		(eq, ":trades", 0),
		(eq, ":road_attacks", 0),
		(str_store_string, s42, "str_there_has_been_very_little_trading_activity_here_recentlys42"),
	(else_try),
		(le, ":trades", 2),
		(eq, ":road_attacks", 0),
		(str_store_string, s42, "str_there_has_some_trading_activity_here_recently_but_not_enoughs42"),
	(else_try),	
		(le, ":trades", 2),
		(le, ":road_attacks", 2),
		(str_store_string, s42, "str_there_has_some_trading_activity_here_recently_but_the_roads_are_dangerouss42"),
	(else_try),	
		(ge, ":road_attacks", 3),
		(str_store_string, s42, "str_the_roads_around_here_are_very_dangerouss42"),
	(else_try),	
		(ge, ":road_attacks", 1),
		(str_store_string, s42, "str_we_have_received_many_traders_in_town_here_although_there_is_some_danger_on_the_roadss42"),
	(else_try),
		(str_store_string, s42, "str_we_have_received_many_traders_in_town_heres42"),
	(try_end),
	
#do safe roads
	(assign, ":unused_trade_route_found", 0),
	(try_for_range, ":trade_route_slot", slot_town_trade_routes_begin, slot_town_trade_routes_end),
		(party_get_slot, ":trade_center", ":center", ":trade_route_slot"),
		(is_between, ":trade_center", centers_begin, centers_end),

		(party_slot_eq, ":trade_center", slot_party_temp_slot_1, 0),

#		(party_get_slot, ":town_lord", ":trade_center", slot_town_lord),
				
		(str_store_party_name, s41, ":trade_center"),
		(try_begin),
			(eq, ":unused_trade_route_found", 1),
			(str_store_string, s44, "str_s44_s41"),
		(else_try),
			(str_store_string, s44, "str_s41"),
		(try_end),
		(assign, ":unused_trade_route_found", 1),
	(try_end),
	(try_begin),
		(eq, ":unused_trade_route_found", 1),
		(str_store_string, s47, "str_there_is_little_news_about_the_caravan_routes_to_the_towns_of_s44_and_nearby_parts_but_no_news_is_good_news_and_those_are_therefore_considered_safe"),
	(try_end),

	(assign, ":safe_village_road_found", 0),
	(try_for_range, ":village", villages_begin, villages_end),
		(party_slot_eq, ":village", slot_village_market_town, ":center"),
		(party_slot_eq, ":village", slot_party_temp_slot_1, 0),

#		(party_get_slot, ":town_lord", ":village", slot_town_lord),
		(str_store_party_name, s41, ":village"),
		(try_begin),
			(eq, ":safe_village_road_found", 1),
			(str_store_string, s44, "str_s44_s41"),
		(else_try),
			(str_store_string, s44, "str_s41"),
		(try_end),
		(assign, ":safe_village_road_found", 1),
	(try_end),

	(try_begin),
		(eq, ":safe_village_road_found", 1),
		(eq, ":unused_trade_route_found", 1),
		(str_store_string, s47, "str_s47_also_the_roads_to_the_villages_of_s44_and_other_outlying_hamlets_are_considered_safe"),
	(else_try),	
		(eq, ":safe_village_road_found", 1),
		(str_store_string, s47, "str_however_the_roads_to_the_villages_of_s44_and_other_outlying_hamlets_are_considered_safe"),
	(try_end),

	(str_store_string, s33, "str_we_have_shortages_of"),
	(assign, ":some_shortages_found", 0),
	(try_for_range, ":cur_good", trade_goods_begin, trade_goods_end),
        (store_sub, ":cur_good_price_slot", ":cur_good", trade_goods_begin),
        (val_add, ":cur_good_price_slot", slot_town_trade_good_prices_begin),
        (party_get_slot, ":price", ":center", ":cur_good_price_slot"),
		(gt, ":price", 1100),

        (str_store_item_name, s34, ":cur_good"),
        (assign, reg1, ":price"),
        (str_store_string, s33, "str_s33_s34_reg1"),

		(assign, ":some_shortages_found", 1),	
	(try_end),

	(try_begin),
		(eq, ":some_shortages_found", 0),
		(str_store_string, s32, "str_we_have_adequate_stores_of_all_commodities"),
	(else_try),
		(str_store_string, s32, "str_s33_and_some_other_commodities"),
	(try_end),

	(assign, reg0, ":last_bandit_party_found"),
	(assign, reg1, ":last_bandit_party_origin"),
	(assign, reg2, ":last_bandit_party_destination"),
	(assign, reg3, ":last_bandit_party_hours_ago"),
	
	
	] 
	),
  ("rebellion_arguments", #Right now, called only in one place. This is only used when for player overtures, and will need some changes if this script is called when NPCs try to suborn lords
    [
     (store_script_param, ":lord", 1),
     (store_script_param, ":argument", 2),
     (store_script_param, ":candidate", 3),

     (assign, ":argument_appeal", 0),
     (assign, ":argument_strength", 0),

     (troop_get_slot, ":reputation", ":lord", slot_lord_reputation_type),

	 (store_faction_of_troop, ":lord_faction", ":candidate"),
	 (store_faction_of_troop, ":candidate_faction", ":candidate"),
	 
	 (try_begin),
		(eq, ":candidate", "trp_player"),
		(assign, ":right_to_rule", "$player_right_to_rule"),
	 (else_try), #default right to rule of 75 for pretenders claiming throne
		(is_between, ":candidate", pretenders_begin, pretenders_end),
		(troop_slot_eq, ":candidate", slot_troop_original_faction, ":lord_faction"),
		(assign, ":right_to_rule", 75),
	 (else_try), #default right to rule of 60 for all other lords
		(assign, ":right_to_rule", 60),
	 (try_end),
	 
	 (try_begin),
		(eq, ":argument", argument_claim),					
		(store_sub, ":argument_strength", ":right_to_rule", 30),				
	 (else_try),
		(eq, ":argument", argument_ruler),		
		(store_sub, ":argument_strength", "$player_honor", 20),
	 (else_try),
		(eq, ":argument", argument_lords),		
		(store_sub, ":argument_strength", "$player_honor", 20),		
	 (else_try),
	    #argument_strength is ((5 * number of centers player have) - 40) if argument type is argument_victory
		(eq, ":argument", argument_victory),		
		(assign, ":argument_strength", 0),
		(try_for_range, ":center", centers_begin, centers_end),
			(store_faction_of_party, ":center_faction", ":center"),
			(assign, ":argument_strength", -40),
			(try_begin),
				(eq, "$players_kingdom", ":candidate_faction"),
				##diplomacy start+
				(this_or_next|eq, ":center_faction", "$players_kingdom"),
				##diplomacy end+
				(this_or_next|eq, ":center_faction", "fac_player_faction"),
				(eq, ":center_faction", "fac_player_supporters_faction"),
				(val_add, ":argument_strength", 5),
			(else_try),
				(eq, ":center_faction", ":candidate_faction"),
				(val_add, ":argument_strength", 5),
			(try_end),
		(try_end),		
	 (else_try),
	    #argument_strength is (20 - 20 * (number of lords in player's faction which not awareded fief by player although there is a fief awarding in future promise))
		(eq, ":argument", argument_benefit),
		(assign, ":argument_strength", 20),
		(try_for_range, ":lord_promised_fief", active_npcs_begin, active_npcs_end),
			(store_faction_of_troop, ":other_faction", ":lord_promised_fief"),
			(neq, ":lord", "$g_talk_troop"),
			(this_or_next|eq, ":other_faction", "fac_player_supporters_faction"),
			(eq, ":other_faction", "$players_kingdom"),
			(troop_slot_eq, ":lord_promised_fief", slot_troop_promised_fief, 1),
			(val_sub, ":argument_strength", 20),
		(try_end),
	 (try_end),
	 (val_clamp, ":argument_strength", -40, 41),
	 	 
     (try_begin),
         (eq, ":reputation", lrep_martial),
         (try_begin),
             (eq, ":argument", argument_claim),
             (assign, ":argument_appeal", 30),			 
			 (try_begin),
				(gt, ":argument_strength", 0),
				(str_store_string, s15, "str_you_speak_of_claims_to_the_throne_good_there_is_nothing_id_rather_do_than_fight_for_a_good_cause"),
			 (else_try),
				(str_store_string, s15, "str_you_speak_of_claims_to_the_throne_well_there_is_nothing_id_rather_do_than_fight_for_a_good_cause_but_the_claim_you_make_seems_somewhat_weak"),
		     (try_end),
         (else_try),
             (eq, ":argument", argument_lords),
             (assign, ":argument_appeal", 10),			 
			 (try_begin),
				(gt, ":argument_strength", 0),
				(str_store_string, s15, "str_i_am_pleased_that_you_speak_of_upholding_my_ancient_rights_which_are_sometimes_trod_upon_in_these_sorry_days"),
			 (else_try),
			    ##diplomacy start+ use culturally-approrpriate term
				(call_script, "script_dplmc_print_cultural_word_to_sreg", ":lord", DPLMC_CULTURAL_TERM_KING, 14),
				##diplomacy end+
				(str_store_string, s15, "str_i_am_pleased_that_you_speak_of_upholding_my_ancient_rights_but_sometimes_men_make_pledges_before_they_are_king_which_they_cannot_keep_once_they_take_the_throne"),
			 (try_end),
         (else_try),
             (eq, ":argument", argument_ruler),
             (assign, ":argument_appeal", 0),			 
			 (try_begin),
				##diplomacy start+: use culturally-approrpriate term
				(call_script, "script_dplmc_print_cultural_word_to_sreg", ":lord", DPLMC_CULTURAL_TERM_USE_MY_WEAPON, s14),
				##diplomacy end+
				(str_store_string, s15, "str_you_speak_of_protecting_the_commons_well_i_supposed_thats_good_but_sometimes_the_commons_overstep_their_boundaries_im_more_concerned_that_your_claim_be_legal_so_i_can_swing_my_sword_with_a_good_conscience"),
			 (try_end),			 
         (else_try),
             (eq, ":argument", argument_benefit),
             (assign, ":argument_appeal", -10),			 
			 (try_begin),
				(gt, ":argument_strength", 0),
				(str_store_string, s15, "str_you_speak_of_giving_me_land_good_i_ask_for_no_more_than_my_due"),
			 (else_try),
				(str_store_string, s15, "str_you_speak_of_giving_me_land_unfortunately_you_are_not_wellknown_for_rewarding_those_to_whom_you_have_made_such_offers"),
			 (try_end),
         (else_try),
             (eq, ":argument", argument_victory),
             (assign, ":argument_appeal", -30),			 
			 (str_store_string, s15, "str_you_speak_of_unifying_calradia_well_i_believe_that_well_always_be_fighting__its_important_that_we_fight_for_a_rightful_cause"),
         (try_end),
     (else_try),
        (eq, ":reputation", lrep_quarrelsome),
        (try_begin),
             (eq, ":argument", argument_claim),
             (assign, ":argument_appeal", -20),
 			 (str_store_string, s15, "str_you_talk_of_claims_to_the_throne_but_i_leave_bickering_about_legalities_to_the_lawyers_and_clerks"),
		(else_try),
             (eq, ":argument", argument_ruler),
             (assign, ":argument_appeal", -30),
			  ##diplomacy start+ use culturally-approrpriate term
			  (call_script, "script_dplmc_print_cultural_word_to_sreg", ":lord", DPLMC_CULTURAL_TERM_KING, 14),
			  ##diplomacy end+
			 (str_store_string, s15, "str_you_speak_of_ruling_justly_hah_ill_believe_theres_such_a_thing_as_a_just_king_when_i_see_one"),
		(else_try),
             (eq, ":argument", argument_lords),
             (assign, ":argument_appeal", 0),
			 ##diplomacy start+ use culturally-approrpriate term
			  (call_script, "script_dplmc_print_cultural_word_to_sreg", ":lord", DPLMC_CULTURAL_TERM_KING, 14),
			  ##diplomacy end+
			 (str_store_string, s15, "str_you_spoke_of_protecting_the_rights_of_the_nobles_if_you_did_youd_be_the_first_king_to_do_so_in_a_very_long_time"),
		(else_try),
             (eq, ":argument", argument_benefit),
             (assign, ":argument_appeal", 30),
			 (try_begin),
				(gt, ":argument_strength", 0),
				(str_store_string, s15, "str_you_speak_of_giving_me_land_ay_well_lets_see_if_you_deliver"),
			 (else_try),
				(str_store_string, s15, "str_you_speak_of_giving_me_land_bah_youre_not_known_for_delivering_on_your_pledges"),
			 (try_end),
	    (else_try),
             (eq, ":argument", argument_victory),
             (assign, ":argument_appeal", 10),			 
			 (try_begin),
				(gt, ":argument_strength", 0),
				(str_store_string, s15, "str_you_speak_of_unifying_calradia_well_youve_done_a_good_job_at_making_calradia_bend_its_knee_to_you_so_maybe_thats_not_just_talk"),
			 (else_try),
				(str_store_string, s15, "str_you_speak_of_unifying_calradia_id_be_impressed_if_i_thought_you_could_do_it_but_unfortunately_you_dont"),
			 (try_end),
		(try_end),
     (else_try),
         (eq, ":reputation", lrep_selfrighteous),
         (try_begin),
             (eq, ":argument", argument_claim),
             (assign, ":argument_appeal", -20),
			 (str_store_string, s15, "str_you_speak_of_claims_to_the_throne_well_any_peasant_can_claim_to_be_a_kings_bastard"),
		 (else_try),
             (eq, ":argument", argument_ruler),
             (assign, ":argument_appeal", -30),			 
			 (str_store_string, s15, "str_well_its_a_fine_thing_to_court_the_commons_with_promises_but_what_do_you_have_to_offer_me"),
		 (else_try),
             (eq, ":argument", argument_lords),
             (assign, ":argument_appeal", 0),		
			 ##diplomacy start+ use culturally-approrpriate term
			 (call_script, "script_dplmc_print_cultural_word_to_sreg", ":lord", DPLMC_CULTURAL_TERM_LORD_PLURAL, 15),
			 (call_script, "script_dplmc_print_cultural_word_to_sreg", ":lord", DPLMC_CULTURAL_TERM_LORD, 14),
			 ##diplomacy end+	 
			 (try_begin),
				(gt, ":argument_strength", 0),
				(str_store_string, s15, "str_you_speak_of_protecting_the_rights_of_lords_that_would_make_a_fine_change_if_my_rights_as_lord_would_be_respected"),
			 (else_try),
				(str_store_string, s15, "str_you_speak_of_protecting_the_rights_of_lords_that_would_make_a_fine_change_if_my_rights_as_lord_would_be_respected_however_it_is_easy_for_you_to_make_promises_while_you_are_weak_that_you_have_no_intention_of_keeping_when_you_are_strong"),
			 (try_end),			 
         (else_try),
             (eq, ":argument", argument_benefit),
             (assign, ":argument_appeal", 20),
			 (try_begin),
				(gt, ":argument_strength", 0),
				(str_store_string, s15, "str_you_speak_of_giving_me_land_well_my_family_is_of_ancient_and_noble_lineage_so_you_promise_me_no_more_than_my_due_still_your_gesture_is_appreciated"),
			 (else_try),
				(str_store_string, s15, "str_you_speak_of_giving_me_land_well_you_make_that_pledge_but_i_am_not_impressed"),
			 (try_end),
		 (else_try),
             (eq, ":argument", argument_victory),
             (assign, ":argument_appeal", 20),			 
			 (try_begin),
				(gt, ":argument_strength", 0),
				(str_store_string, s15, "str_you_speak_of_unifying_calradia_well_much_of_this_land_now_bends_its_knee_to_you_so_perhaps_that_is_not_just_talk"),
			 (else_try),
				(str_store_string, s15, "str_you_speak_of_unifying_calradia_but_right_now_yours_is_just_one_squabbling_faction_among_many"),
			 (try_end),			 			 
         (try_end),
     (else_try),
         (eq, ":reputation", lrep_cunning),
         (try_begin),
             (eq, ":argument", argument_claim),
             (assign, ":argument_appeal", -30),
			 (str_store_string, s15, "str_you_speak_of_claims_well_no_offense_but_a_claim_unsupported_by_might_rarely_prospers"),			 			 
         (else_try),
             (eq, ":argument", argument_ruler),
             (assign, ":argument_appeal", 10),			 
			 (try_begin),
				(gt, ":argument_strength", 0),
				(str_store_string, s15, "str_you_speak_of_protecting_the_commons_well_i_suppose_that_will_make_for_a_more_prosperous_realm_ive_always_tried_to_treat_my_peasants_decently_saves_going_to_bed_worrying_about_whether_youll_wake_up_with_the_roof_on_fire"),
			 (else_try),
				(str_store_string, s15, "str_you_speak_of_protecting_the_commons_very_well_but_remember_that_peasants_are_more_likely_to_cause_trouble_if_you_make_promises_then_dont_deliver_than_if_you_never_made_the_promise_in_the_first_place"),
			 (try_end),
         (else_try),
             (eq, ":argument", argument_lords),
             (assign, ":argument_appeal", 15),		
 			 ##diplomacy start+ use culturally-approrpriate term
			 (call_script, "script_dplmc_print_cultural_word_to_sreg", ":lord", DPLMC_CULTURAL_TERM_KING, 15),
			 (call_script, "script_dplmc_print_cultural_word_to_sreg", ":lord", DPLMC_CULTURAL_TERM_LORD_PLURAL, 14),
			 ##diplomacy end+	 
			 (try_begin),
				(gt, ":argument_strength", 0),
				(str_store_string, s15, "str_you_speak_of_protecting_the_rights_of_lords_good_youd_be_well_advised_to_do_that__men_fight_better_for_a_king_wholl_respect_their_rights"),
			 (else_try),
				(str_store_string, s15, "str_you_speak_of_protecting_the_rights_of_lords_very_well_but_remember__failing_to_keep_promises_which_you_made_while_scrambling_up_the_throne_is_the_quickest_way_to_topple_off_of_it_once_you_get_there"),
			 (try_end),			 			 			 			 
         (else_try),
             (eq, ":argument", argument_benefit),
             (assign, ":argument_appeal", -20),			 
			 (str_store_string, s15, "str_you_speak_of_giving_me_land_very_good_but_often_i_find_that_when_a_man_makes_too_many_promises_trying_to_get_to_the_top_he_has_trouble_keeping_them_once_he_reaches_it"),
         (else_try),
             (eq, ":argument", argument_victory),
             (assign, ":argument_appeal", 20),			 
			 (try_begin),
				(gt, ":argument_strength", 0),
				(str_store_string, s15, "str_you_speak_of_unifying_calradia_well_many_have_said_that_you_might_very_well_be_the_one_to_do_it"),
			 (else_try),
				(str_store_string, s15, "str_you_speak_of_unifying_calradia_well_all_the_kings_say_that_im_not_sure_that_you_will_succeed_while_they_fail"),
			 (try_end),			 			 
         (try_end),
     (else_try),
         (eq, ":reputation", lrep_debauched),
         (try_begin),
             (eq, ":argument", argument_claim),
             (assign, ":argument_appeal", -20),			 
			 (str_store_string, s15, "str_you_speak_of_claims_do_you_think_i_care_for_the_nattering_of_lawyers"),			 
         (else_try),
             (eq, ":argument", argument_ruler),
             (assign, ":argument_appeal", -20),			 
             ##diplomacy start+ replace "swineherd" with culturally-appropriate term
             (call_script, "script_dplmc_print_cultural_word_to_sreg", ":lord", DPLMC_CULTURAL_TERM_SWINEHERD, 14),
             ##diplomacy end+
			 (str_store_string, s15, "str_you_speak_of_protecting_the_commons_how_kind_of_you_i_shall_tell_my_swineherd_all_about_your_sweet_promises_no_doubt_he_will_become_your_most_faithful_vassal"),
         (else_try),
             (eq, ":argument", argument_lords),
             (assign, ":argument_appeal", -10),		
             ##diplomacy start+ replace "lords" with culturally-appropriate term
             (call_script, "script_dplmc_print_cultural_word_to_sreg", ":lord", DPLMC_CULTURAL_TERM_LORD_PLURAL, 14),
             ##diplomacy end+	 
			 (str_store_string, s15, "str_you_speak_of_protecing_the_rights_of_lords_such_sweet_words_but_ill_tell_you_this__the_only_rights_that_are_respected_in_this_world_are_the_rights_to_dominate_whoever_is_weaker_and_to_submit_to_whoever_is_stronger"),			 
         (else_try),
             (eq, ":argument", argument_benefit),
             (assign, ":argument_appeal", 20),			 
			 (try_begin),
				(gt, ":argument_strength", 0),
				(str_store_string, s15, "str_you_speak_of_giving_me_land_yes_very_good__but_you_had_best_deliver"),
			 (else_try),
				(str_store_string, s15, "str_you_speak_of_giving_me_land_hah_perhaps_all_those_others_to_whom_you_promised_lands_will_simply_step_aside"),
			 (try_end),			 			 
         (else_try),
             (eq, ":argument", argument_victory),
             (assign, ":argument_appeal", 10),			 
			 (try_begin),
				(gt, ":argument_strength", 0),
				(str_store_string, s15, "str_you_speak_of_unifying_calradia_you_may_indeed_humble_the_other_kings_of_this_land_and_in_that_case_i_would_hope_that_you_would_remember_me_as_your_faithful_servant"),
			 (else_try),
				(str_store_string, s15, "str_you_speak_of_unifying_calradia_but_you_are_weak_and_i_think_that_you_will_remain_weak"),
			 (try_end),			 
         (try_end),
	 (else_try),
         (eq, ":reputation", lrep_goodnatured),
         (try_begin),
             (eq, ":argument", argument_claim),
             (assign, ":argument_appeal", 10),
			 ##diplomacy start+ replace "king" with culturally-appropriate term
             (call_script, "script_dplmc_print_cultural_word_to_sreg", ":lord", DPLMC_CULTURAL_TERM_KING, 14),
			 ##diplomacy end+
			 (try_begin),
				(gt, ":argument_strength", 0),
				(str_store_string, s15, "str_you_speak_of_claims_its_good_for_a_king_to_have_a_strong_claim_although_admittedly_im_more_concerned_that_he_rules_just_ly_than_with_legalities_anyway_your_claim_seems_wellfounded_to_me"),
			 (else_try),
				(str_store_string, s15, "str_you_speak_of_claims_but_your_claim_seems_a_bit_weak_to_me"),
			 (try_end),
         (else_try),
             (eq, ":argument", argument_ruler),
             (assign, ":argument_appeal", 20),
			 (try_begin),
				(gt, ":argument_strength", 0),
				(str_store_string, s15, "str_you_speak_of_protecting_the_commons_i_like_that_my_tenants_are_a_happy_lot_i_think_but_i_hear_of_others_in_other_estates_that_arent_so_fortunate"),
			 (else_try),
				(str_store_string, s15, "str_you_speak_of_protecting_the_commons_im_glad_to_hear_you_say_that_but_do_me_a_favor__dont_promise_the_commons_anything_you_cant_deliver_thats_a_sure_way_to_get_them_to_rebel_and_it_breaks_my_heart_to_have_to_put_them_down"),
			 (try_end),
         (else_try),
             (eq, ":argument", argument_lords),
			 (assign, ":argument_appeal", 0),
			 ##diplomacy start+ use culturally-approrpriate term
			 (call_script, "script_dplmc_print_cultural_word_to_sreg", ":lord", DPLMC_CULTURAL_TERM_KING, 15),
			 (call_script, "script_dplmc_print_cultural_word_to_sreg", ":lord", DPLMC_CULTURAL_TERM_LORD_PLURAL, 14),
			 ##diplomacy end+
			 (str_store_string, s15, "str_you_speak_of_protecting_the_rights_of_lords_well_very_good_i_suppose_but_you_know__we_lords_can_take_of_ourselves_its_the_common_folk_who_need_a_strong_king_to_look_out_for_them_to_my_mind"),			 
         (else_try),
             (eq, ":argument", argument_benefit),
             (assign, ":argument_appeal", -15),
			 (str_store_string, s15, "str_you_speak_of_giving_me_land_its_kind_of_you_really_though_that_is_not_necessary"),			 			 
         (else_try),
             (eq, ":argument", argument_victory),
             (assign, ":argument_appeal", -25),
             ##diplomacy start+
             #Save culturally-appropriate variant of "sword" (as in "by the sword") to s14
			 (call_script, "script_dplmc_print_cultural_word_to_sreg", ":lord", DPLMC_CULTURAL_TERM_WEAPON, 14),
			 ##diplomacy end+
			 (str_store_string, s15, "str_you_speak_of_unifying_calradia_well_maybe_you_can_unite_this_land_by_the_sword_but_im_not_sure_that_this_will_make_you_a_good_ruler"),			 			 
         (try_end),
     (else_try),
         (eq, ":reputation", lrep_upstanding),
         (try_begin),
             (eq, ":argument", argument_claim),
             (assign, ":argument_appeal", 10),
			 ##diplomacy start+ use culturally-approrpriate term
			 (call_script, "script_dplmc_print_cultural_word_to_sreg", ":lord", DPLMC_CULTURAL_TERM_KING, 14),
			 ##diplomacy end+
			 (try_begin),
				(gt, ":argument_strength", 0),
				(str_store_string, s15, "str_you_speak_of_claims_a_king_must_have_a_strong_legal_claim_for_there_not_to_be_chaos_in_the_realm_and_yours_is_wellestablished"),
			 (else_try),
				(str_store_string, s15, "str_you_speak_of_claims_a_king_must_have_a_strong_legal_claim_for_there_not_to_be_chaos_in_the_realm_but_your_claim_is_not_so_strong"),
			 (try_end),
		 (else_try),
             (eq, ":argument", argument_lords),
             (assign, ":argument_appeal", -5),
			 ##diplomacy start+ use culturally-approrpriate term
			 (call_script, "script_dplmc_print_cultural_word_to_sreg", ":lord", DPLMC_CULTURAL_TERM_KING, 14),
			 (call_script, "script_dplmc_print_cultural_word_to_sreg", ":lord", DPLMC_CULTURAL_TERM_LORD_PLURAL, 15),
			 ##diplomacy end+
			 (try_begin),
				(gt, ":argument_strength", 0),
				(str_store_string, s15, "str_you_speak_of_protecting_the_rights_of_lords_it_is_of_course_important_that_a_king_respect_the_rights_of_his_vassals_although_i_worry_that_a_king_who_took_a_throne_without_proper_cause_would_not_rule_with_justice"),
			 (else_try),
				(str_store_string, s15, "str_you_speak_of_protecting_the_rights_of_lords_it_is_of_course_important_that_a_king_respect_the_rights_of_his_vassals_however_i_would_like_to_know_that_you_would_indeed_deliver_on_your_promises"),
			 (try_end),
		 (else_try),
             (eq, ":argument", argument_ruler),
             (assign, ":argument_appeal", 5),	
			 ##diplomacy start+ use culturally-approrpriate term
			 (call_script, "script_dplmc_print_cultural_word_to_sreg", ":lord", DPLMC_CULTURAL_TERM_KING, 14),
			 ##diplomacy end+		 
			 (try_begin),
				(gt, ":argument_strength", 0),
				(str_store_string, s15, "str_you_speak_of_protecting_the_commons_i_would_be_pleased_to_serve_a_king_who_respected_the_rights_of_his_subjects_although_i_worry_that_a_king_who_took_a_throne_without_proper_cause_would_not_rule_with_justice"),
			 (else_try),
				(str_store_string, s15, "str_you_speak_of_protecting_the_commons_i_would_be_pleased_to_serve_a_king_who_respected_the_rights_of_his_subjects_however_i_would_like_to_know_that_you_would_indeed_deliver_on_your_promises"),
			 (try_end),			 
         (else_try),
             (eq, ":argument", argument_benefit),
             (assign, ":argument_appeal", -40),
			 (str_store_string, s15, "str_i_am_not_swayed_by_promises_of_reward"),
		 (else_try),
             (eq, ":argument", argument_victory),
             (assign, ":argument_appeal", 10),			 
			 (try_begin),
				(gt, ":argument_strength", 0),
				(str_store_string, s15, "str_you_speak_of_unifying_calradia_it_would_be_good_to_bring_peace_to_the_realm_and_i_believe_that_you_are_strong_enough_to_do_so"),
			 (else_try),
				(str_store_string, s15, "str_you_speak_of_unifying_calradia_it_would_be_good_to_bring_peace_the_realm_but_with_your_kingdom_in_its_current_state_i_worry_that_you_are_just_bringing_more_discord"),
			 (try_end),			 			 
         (try_end),
     (try_end),
	 
	 (str_store_string, s14, "str_s15"),
	 	 
     (assign, reg0, ":argument_appeal"),
     (assign, reg1, ":argument_strength"),     
]),
  # script_get_culture_with_party_faction_for_music
  # Input: arg1 = party_no
  # Output: reg0 = culture
  ("get_culture_with_party_faction_for_music",
    [
      (store_script_param, ":party_no", 1),
      (store_faction_of_party, ":faction_no", ":party_no"),
      (try_begin),
        (this_or_next|eq, ":faction_no", "fac_player_faction"),
        (eq, ":faction_no", "fac_player_supporters_faction"),
        (assign, ":faction_no", "$players_kingdom"),
      (try_end),
      (try_begin),
        (is_between, ":party_no", centers_begin, centers_end),
        (this_or_next|eq, ":faction_no", "fac_player_supporters_faction"),
        (neg|is_between, ":faction_no", kingdoms_begin, kingdoms_end),
        (party_get_slot, ":faction_no", ":party_no", slot_center_original_faction),
      (try_end),
      (call_script, "script_get_culture_with_faction_for_music", ":faction_no"),
     ]),
  # script_get_culture_with_faction_for_music
  # Input: arg1 = party_no
  # Output: reg0 = culture
  ("get_culture_with_faction_for_music",
    [
      (store_script_param, ":faction_no", 1),
      (try_begin),
        (this_or_next|eq, ":faction_no", "fac_kingdom_1"),
        (this_or_next|eq, ":faction_no", "fac_kingdom_7"),
        (this_or_next|eq, ":faction_no", "fac_kingdom_13"),
        (eq, ":faction_no", "fac_kingdom_19"),
        (assign, ":result", mtf_culture_1),
      (else_try),
        (this_or_next|eq, ":faction_no", "fac_kingdom_2"),
        (this_or_next|eq, ":faction_no", "fac_kingdom_8"),
        (eq, ":faction_no", "fac_kingdom_14"),
        (assign, ":result", mtf_culture_2),
      (else_try),
        (this_or_next|eq, ":faction_no", "fac_kingdom_3"),
        (this_or_next|eq, ":faction_no", "fac_kingdom_9"),
        (eq, ":faction_no", "fac_kingdom_15"),
        (assign, ":result", mtf_culture_3),
      (else_try),
        (this_or_next|eq, ":faction_no", "fac_kingdom_4"),
        (this_or_next|eq, ":faction_no", "fac_kingdom_10"),
        (eq, ":faction_no", "fac_kingdom_16"),
        (assign, ":result", mtf_culture_4),
      (else_try),
        (this_or_next|eq, ":faction_no", "fac_kingdom_5"),
        (this_or_next|eq, ":faction_no", "fac_kingdom_11"),
        (eq, ":faction_no", "fac_kingdom_17"),
        (assign, ":result", mtf_culture_5),
      (else_try),
        (this_or_next|eq, ":faction_no", "fac_kingdom_6"),
        (this_or_next|eq, ":faction_no", "fac_kingdom_12"),
        (eq, ":faction_no", "fac_kingdom_18"),
        (assign, ":result", mtf_culture_6),
      (else_try),
        (this_or_next|eq, ":faction_no", "fac_outlaws"),
        (this_or_next|eq, ":faction_no", "fac_shinano_rebels"),
        (this_or_next|eq, ":faction_no", "fac_deserters"),
        (eq, ":faction_no", "fac_woku_pirates"),
        (eq, ":faction_no", "fac_shinano_rebels"),
        (assign, ":result", mtf_culture_6),
      (else_try),
        (assign, ":result", 0), #no culture, including player with no bindings to another kingdom
      (try_end),
      (assign, reg0, ":result"),
     ]),
  # script_music_set_situation_with_culture
  # Input: arg1 = music_situation
  # Output: none
  ("music_set_situation_with_culture",
    [
      (store_script_param, ":situation", 1),
      (assign, ":culture", 0), #no culture
      (try_begin),
        (this_or_next|eq, ":situation", mtf_sit_town),
        (this_or_next|eq, ":situation", mtf_sit_day),
        (this_or_next|eq, ":situation", mtf_sit_night),
        (this_or_next|eq, ":situation", mtf_sit_town_infiltrate),
        (eq, ":situation", mtf_sit_encounter_hostile),
        (call_script, "script_get_culture_with_party_faction_for_music", "$g_encountered_party"),
        (val_or, ":culture", reg0),
      (else_try),
        (this_or_next|eq, ":situation", mtf_sit_ambushed),
        (eq, ":situation", mtf_sit_fight),
        (call_script, "script_get_culture_with_party_faction_for_music", "$g_encountered_party"),
        (val_or, ":culture", reg0),
        (call_script, "script_get_culture_with_party_faction_for_music", "p_main_party"),
        (val_or, ":culture", reg0),
        (call_script, "script_get_closest_center", "p_main_party"),
        (call_script, "script_get_culture_with_party_faction_for_music", reg0),
        (val_or, ":culture", reg0),
      (else_try),
        (eq, ":situation", mtf_sit_multiplayer_fight),
        (call_script, "script_get_culture_with_faction_for_music", "$g_multiplayer_team_1_faction"),
        (val_or, ":culture", reg0),
        (call_script, "script_get_culture_with_faction_for_music", "$g_multiplayer_team_2_faction"),
        (val_or, ":culture", reg0),
      (else_try),
        (eq, ":situation", mtf_sit_travel),
        (call_script, "script_get_culture_with_party_faction_for_music", "p_main_party"),
        (val_or, ":culture", reg0),
        (call_script, "script_get_closest_center", "p_main_party"),
        (call_script, "script_get_culture_with_party_faction_for_music", reg0),
        (val_or, ":culture", reg0),
      (else_try),
        (eq, ":situation", mtf_sit_victorious),
        (call_script, "script_get_culture_with_party_faction_for_music", "p_main_party"),
        (val_or, ":culture", reg0),
      (else_try),
        (eq, ":situation", mtf_sit_killed),
        (call_script, "script_get_culture_with_party_faction_for_music", "$g_encountered_party"),
        (val_or, ":culture", reg0),
      (try_end),
      (try_begin),
        (this_or_next|eq, ":situation", mtf_sit_town),
        (eq, ":situation", mtf_sit_day),
        (try_begin),
          (is_currently_night),
          (assign, ":situation", mtf_sit_night),
        (try_end),
      (try_end),
      (music_set_situation, ":situation"),
      (music_set_culture, ":culture"),
     ]),
  # script_combat_music_set_situation_with_culture
  # Input: none
  # Output: none
  ("combat_music_set_situation_with_culture",
    [
      (assign, ":situation", mtf_sit_fight),
      (assign, ":num_allies", 0),
      (assign, ":num_enemies", 0),
      (try_for_agents, ":agent_no"),
        (agent_is_alive, ":agent_no"),
        (agent_is_human, ":agent_no"),
        (agent_get_troop_id, ":agent_troop_id", ":agent_no"),
        (store_character_level, ":troop_level", ":agent_troop_id"),
        (val_add,  ":troop_level", 10),
        (val_mul, ":troop_level", ":troop_level"),
        (try_begin),
          (agent_is_ally, ":agent_no"),
          (val_add, ":num_allies", ":troop_level"),
        (else_try),
          (val_add, ":num_enemies", ":troop_level"),
        (try_end),
      (try_end),
      (val_mul, ":num_allies", 4), #play ambushed music if we are 2 times outnumbered.
      (val_div, ":num_allies", 3),
      (try_begin),
        (lt, ":num_allies", ":num_enemies"),
        (assign, ":situation", mtf_sit_ambushed),
      (try_end),
      (call_script, "script_music_set_situation_with_culture", ":situation"),
     ]),
  # script_play_victorious_sound
  # Input: none
  # Output: none
  ("play_victorious_sound",
   [
     (call_script, "script_music_set_situation_with_culture", mtf_sit_victorious),
#      (play_cue_track, "track_victorious_neutral_1"),
#      (play_track, "track_victorious_neutral_1", 1),
     ]),
#lord recruitment scripts begin	  
  ("troop_describes_troop_to_s15",
  [
	(store_script_param, ":troop_1", 1),
	(store_script_param, ":troop_2", 2),

	
	(str_store_troop_name, s15, ":troop_2"),
	
	(try_begin),
		(eq, ":troop_2", "trp_player"),
		(str_store_string, s15, "str_you"),
	(else_try),	
		(eq, ":troop_2", ":troop_1"),
		(str_store_string, s15, "str_myself"),
	(else_try),
		(call_script, "script_troop_get_family_relation_to_troop", ":troop_2", ":troop_1"),
		(gt, reg0, 0),
		(str_store_string, s15, "str_my_s11_s15"),
	(else_try),	
		(call_script, "script_troop_get_relation_with_troop", ":troop_2", ":troop_1"),
		(ge, reg0, 20),
		(str_store_string, s15, "str_my_friend_s15"),
	(try_end),	
	
	]),
  ("troop_describes_quarrel_with_troop_to_s14",
  #perhaps replace this with get_relevant_comment at a later date
    [
	(store_script_param, ":troop", 1),
	(store_script_param, ":troop_2", 2),

	(str_store_troop_name, s15, ":troop"),
	(str_store_troop_name, s16, ":troop_2"),

	(str_store_string, s14, "str_stop_gap__s15_is_the_rival_of_s16"),
	
	(try_begin),
		(eq, ":troop", "$g_talk_troop"),
		(call_script, "script_cf_test_lord_incompatibility_to_s17", ":troop", ":troop_2"),
		(str_store_string, s14, s17),
	(else_try),	
		(eq, ":troop_2", "$g_talk_troop"),
		(call_script, "script_cf_test_lord_incompatibility_to_s17", ":troop_2", ":troop"),
		(str_store_string, s14, s17),
	(else_try),
		(str_store_string, s14, "str_general_quarrel"),
	(try_end),
	
]),
  ("cf_test_lord_incompatibility_to_s17", #writes rivalry chance to reg0
    [

	(store_script_param, ":source_lord", 1),
	(store_script_param, ":target_lord", 2),
	
	
	(assign, ":chance_of_rivalry", 0),
	
	(troop_get_slot, ":source_reputation", ":source_lord", slot_lord_reputation_type),
	(troop_get_slot, ":target_reputation", ":target_lord", slot_lord_reputation_type),

	##diplomacy start+ Note: the next line is in native, but as far as I can discern the register value wasn't actually used.
	(troop_get_type, reg15, ":target_lord"),
	##diplomacy end+
	
	(str_store_troop_name, s18, ":target_lord"),
	
	(assign, ":divisor", 1),
	
	(call_script, "script_troop_get_family_relation_to_troop", ":target_lord", ":source_lord"),
	(assign, ":family_relationship", reg0),
	
	(try_begin),
		(gt, ":family_relationship", 0),
		(store_div, ":family_divisor", reg0, 5),
		(val_add, ":divisor", ":family_divisor"),
		(str_store_string, s18, "str_my_s11_s18"),
	(else_try),
		(gt, ":target_reputation", lrep_upstanding),
		(this_or_next|eq, ":source_reputation", lrep_debauched),
			(eq, ":source_reputation", lrep_selfrighteous),
		(str_store_string, s18, "str_the_socalled_s11_s18"),
	(try_end),	

   ##diplomacy start+ get gender types
	(assign, ":save_reg65", reg65),#save register values to revert at end of script
	(assign, ":save_reg3", reg3),
	(call_script, "script_dplmc_store_troop_is_female_reg", ":target_lord", 3),#reg3 used below for gender-correct pronouns
	(call_script, "script_dplmc_store_troop_is_female", ":source_lord"),
   (assign, reg65, reg0),#used below in some situations for speaker
   (assign, reg0, ":family_relationship"),#revert register to value before this section
	##diplomacy end+	
	(try_begin), #test if reps are compatible
        (eq, ":source_reputation", lrep_martial),
		(is_between, ":family_relationship", 1, 5), #uncles and cousins
		
		(assign, ":chance_of_rivalry", 100),
        (str_store_string, s17, "str_s18_would_cheat_me_of_my_inheritance_by_heaven_i_know_my_rights_and_im_not_going_to_back_down"), 
	(else_try),
        (eq, ":source_reputation", lrep_martial),
        (eq, ":target_reputation", lrep_quarrelsome),
        (str_store_string, s17, "str_s18_once_questioned_my_honour_and_my_bravery_i_long_for_the_day_when_i_can_meet_him_in_battle_and_make_him_retract_his_statement"),
		(assign, ":chance_of_rivalry", 50),

	(else_try),
        (eq, ":source_reputation", lrep_martial),
        (eq, ":target_reputation", lrep_upstanding),
        (str_store_string, s17, "str_s18_once_questioned_my_judgment_in_battle_by_heaven_would_he_have_us_shirk_our_duty_to_smite_our_sovereigns_foes"),
		(assign, ":chance_of_rivalry", 50),

	(else_try),
        (eq, ":target_reputation", lrep_martial),
		(is_between, ":family_relationship", 1, 5),
		
		(assign, ":chance_of_rivalry", 100),
        (str_store_string, s17, "str_s18_seems_to_think_he_has_the_right_to_some_of_my_property_well_he_does_not"), 
		
	(else_try),
        (eq, ":source_reputation", lrep_quarrelsome),
        (eq, ":target_reputation", lrep_martial),
        (str_store_string, s17, "str_s18_once_took_something_i_said_amiss_stubborn_bastard_wont_give_it_up_and_keeps_trying_to_get_me_to_recant_my_words"), 
		(assign, ":chance_of_rivalry", 50),

	(else_try),
        (eq, ":source_reputation", lrep_quarrelsome),
        (eq, ":target_reputation", lrep_cunning),
        (str_store_string, s17, "str_s18_is_a_crafty_weasel_and_i_dont_trust_him_one_bit"), 
		(assign, ":chance_of_rivalry", 100),

		
    (else_try),
        (eq, ":source_reputation", lrep_debauched),
        (eq, ":target_reputation", lrep_upstanding),
		(str_store_string, s17, "str_s18_i_despite_him_he_puts_on_such_a_nauseating_display_of_virtue_and_thinks_nothing_of_insulting_his_betters"),
		(assign, ":chance_of_rivalry", 100),

        #debauched insults upstanding

    (else_try),
        (eq, ":source_reputation", lrep_debauched),
        (eq, ":target_reputation", lrep_selfrighteous),
		(str_store_string, s17, "str_s18_entered_into_a_little_deal_with_me_and_is_now_trying_to_wriggle_out_of_it"),
		(assign, ":chance_of_rivalry", 100),

        #debauched insults selfrighteous

		
		
    (else_try),
        (eq, ":source_reputation", lrep_selfrighteous),
        (eq, ":target_reputation", lrep_debauched),
		(str_store_string, s17, "str_s18_once_ran_an_errand_for_me_and_now_thinks_i_owe_him_something_i_owe_his_ilk_nothing"),
		(assign, ":chance_of_rivalry", 100),
        #selfrighteous dismisses debauched
		
    (else_try),
        (eq, ":source_reputation", lrep_selfrighteous),
        (eq, ":target_reputation", lrep_goodnatured),
		(str_store_string, s17, "str_s18_is_soft_and_weak_and_not_fit_to_govern_a_fief_and_i_have_always_detested_him"),
		(assign, ":chance_of_rivalry", 100),
             

			 
	(else_try),
        (eq, ":source_reputation", lrep_cunning),
        (eq, ":target_reputation", lrep_quarrelsome),
        (str_store_string, s17, "str_s18_is_a_quarrelsome_oaf_and_a_liability_in_my_opinion_and_ive_let_him_know_as_much"), 
		(assign, ":chance_of_rivalry", 100),
        #cunning insults quarrelsome

	(else_try),
        (eq, ":source_reputation", lrep_cunning),
        (eq, ":target_reputation", lrep_goodnatured),
        (str_store_string, s17, "str_s18_i_am_sorry_to_say_is_far_too_softhearted_a_man_to_be_given_any_kind_of_responsibility_his_chivalry_will_allow_the_enemy_to_flee_to_fight_another_day_and_will_cost_the_lives_of_my_own_faithful_men"), 
		(assign, ":chance_of_rivalry", 100),
		

	(else_try),
        (eq, ":source_reputation", lrep_goodnatured),
        (eq, ":target_reputation", lrep_cunning),
        (str_store_string, s17, "str_s18_seems_to_have_something_against_me_for_some_reason_i_dont_like_to_talk_ill_of_people_but_i_think_hes_can_be_a_bit_of_a_cad_sometimes"), 
		(assign, ":chance_of_rivalry", 100),
		
	(else_try),
        (eq, ":source_reputation", lrep_goodnatured),
        (eq, ":target_reputation", lrep_selfrighteous),
        (str_store_string, s17, "str_s18_has_always_treated_me_contemptuously_although_i_have_done_him_no_wrong"), 
		(assign, ":chance_of_rivalry", 100),
		
		

	(else_try),
        (eq, ":source_reputation", lrep_upstanding),
        (eq, ":target_reputation", lrep_debauched),
        (str_store_string, s17, "str_s18_is_thoroughly_dishonorable_and_a_compulsive_spinner_of_intrigues_which_i_fear_will_drag_us_into_wars_or_incite_rebellions"), 
		(assign, ":chance_of_rivalry", 50),

	(else_try),
        (eq, ":source_reputation", lrep_upstanding),
        (eq, ":target_reputation", lrep_martial),
        (str_store_string, s17, "str_s18_disappoints_me_i_once_scolded_for_his_rashness_in_battle_and_he_took_offense_i_do_not_care_to_apologize_for_my_efforts_to_save_his_life_and_the_lives_of_his_men"), 
		(assign, ":chance_of_rivalry", 50),

	#for commons	
	(else_try),
        (this_or_next|eq, ":source_reputation", lrep_upstanding),
		(this_or_next|eq, ":source_reputation", lrep_martial),
			(eq, ":source_reputation", lrep_selfrighteous),
        (eq, ":target_reputation", lrep_roguish),
        (str_store_string, s17, "str_s18_squanders_money_and_carouses_in_a_way_most_unbefitting_a_noble_by_doing_so_he_disgraces_us_all"), 
		(assign, ":chance_of_rivalry", 100),

		
	(else_try),
        (eq, ":source_reputation", lrep_roguish),
        (this_or_next|eq, ":target_reputation", lrep_upstanding),
		(this_or_next|eq, ":target_reputation", lrep_martial),
			(eq, ":target_reputation", lrep_selfrighteous),
        (str_store_string, s17, "str_s18_has_been_speaking_ill_of_me_behind_my_back_or_so_they_say"), 
		(assign, ":chance_of_rivalry", 100),


	(else_try),
        (this_or_next|eq, ":source_reputation", lrep_quarrelsome),
		(this_or_next|eq, ":source_reputation", lrep_martial),
			(eq, ":source_reputation", lrep_selfrighteous),
        (eq, ":target_reputation", lrep_custodian),
        (str_store_string, s17, "str_s18_is_a_disgrace_reg3shehe_consorts_with_merchants_lends_money_at_interest_uses_coarse_language_and_shows_no_attempt_to_uphold_the_dignity_of_the_honor_bestowed_upon_reg3herhim"), 
		(assign, ":chance_of_rivalry", 100),

	(else_try),
        (eq, ":source_reputation", lrep_custodian),
		(this_or_next|eq, ":target_reputation", lrep_quarrelsome),
		(this_or_next|eq, ":target_reputation", lrep_martial),
			(eq, ":target_reputation", lrep_selfrighteous),
        (str_store_string, s17, "str_s18_has_condemned_me_for_engaging_in_commerce_what_could_possibly_be_wrong_with_that"), 
		(assign, ":chance_of_rivalry", 100),

		
	(else_try),
        (this_or_next|eq, ":source_reputation", lrep_debauched),
		(this_or_next|eq, ":source_reputation", lrep_martial),
			(eq, ":source_reputation", lrep_selfrighteous),
        (eq, ":target_reputation", lrep_benefactor),
        (str_store_string, s17, "str_s18_i_have_heard_has_been_encouraging_seditious_ideas_among_the_peasantry__a_foolish_move_which_endangers_us_all"), 
		(assign, ":chance_of_rivalry", 100),
		
		
	(else_try),
        (eq, ":source_reputation", lrep_benefactor),
		(this_or_next|eq, ":target_reputation", lrep_debauched),
		(this_or_next|eq, ":target_reputation", lrep_martial),
			(eq, ":target_reputation", lrep_selfrighteous),
        (str_store_string, s17, "str_s18_has_called_me_out_for_the_way_i_deal_with_my_tenants_well_so_be_it_if_i_teach_them_that_they_are_the_equal_of_anyone_with_socalled_gentle_blood_what_is_it_to_reg3herhim"), 
		(assign, ":chance_of_rivalry", 100),


	#lady incompatibilities	
	(else_try),	
		(eq, ":source_reputation", lrep_conventional),
		(this_or_next|eq, ":target_reputation", lrep_martial),
			(eq, ":target_reputation", lrep_selfrighteous),
        (str_store_string, s17, "str_a_most_gallant_gentleman_who_knows_how_to_treat_a_lady"), 
		(assign, ":chance_of_rivalry", -50),

	(else_try),	
		(eq, ":source_reputation", lrep_conventional),
		(eq, ":target_reputation", lrep_quarrelsome),
        (str_store_string, s17, "str_a_base_cad"), 
		(assign, ":chance_of_rivalry", 50),
	
		
	(else_try),	
		(eq, ":source_reputation", lrep_adventurous),
		(eq, ":target_reputation", lrep_cunning),
        (str_store_string, s17, "str_a_man_who_treats_me_as_his_equal_which_is_rare"), 
		(assign, ":chance_of_rivalry", -50),

	(else_try),	
		(eq, ":source_reputation", lrep_adventurous),
		(this_or_next|eq, ":target_reputation", lrep_martial),
			(eq, ":target_reputation", lrep_debauched),
		(str_store_string, s17, "str_appears_to_value_me_with_his_estate_and_his_horse_as_prizes_worth_having"), 
		(assign, ":chance_of_rivalry", 50),

	(else_try),	
		(eq, ":source_reputation", lrep_adventurous),
		(neq, ":target_reputation", lrep_goodnatured),
		
        (str_store_string, s17, "str_a_bit_dull_but_what_can_you_expect"), 
		(assign, ":chance_of_rivalry", 10),

	(else_try),	
		(eq, ":source_reputation", lrep_otherworldly),
		(call_script, "script_troop_get_romantic_chemistry_with_troop", ":source_lord", ":target_lord"),
		(ge, reg0, 10),
        (str_store_string, s17, "str_the_man_whom_destiny_intends_for_me"), 
		(assign, ":chance_of_rivalry", -50),

	(else_try),	
		(eq, ":source_reputation", lrep_otherworldly),
		(lt, reg0, 0),
		
        (str_store_string, s17, "str_is_not_right_for_me__i_cannot_say_why_but_he_makes_my_skin_crawl"), 
		(assign, ":chance_of_rivalry", 50),

		
	(else_try),	
		(eq, ":source_reputation", lrep_ambitious),
		(this_or_next|eq, ":target_reputation", lrep_selfrighteous),
			(eq, ":target_reputation", lrep_cunning),
        (str_store_string, s17, "str_is_a_man_who_clearly_intends_to_make_his_mark_in_the_world"), 
		(assign, ":chance_of_rivalry", -20),

	(else_try),	
		(eq, ":source_reputation", lrep_ambitious),
		(eq, ":target_reputation", lrep_goodnatured),
		
        (str_store_string, s17, "str_is_a_layabout_a_naif_prey_for_others_who_are_cleverer_than_he"), 
		(assign, ":chance_of_rivalry", 30),

				
	(else_try),	
		(eq, ":source_reputation", lrep_moralist),
		(eq, ":target_reputation", lrep_upstanding),
		
        (str_store_string, s17, "str_is_a_man_of_stalwart_character"), 
		(assign, ":chance_of_rivalry", -50),

	(else_try),	
		(eq, ":source_reputation", lrep_moralist),
		(this_or_next|eq, ":target_reputation", lrep_debauched),
			(eq, ":target_reputation", lrep_cunning),
			
        (str_store_string, s17, "str_appears_to_be_a_man_of_low_morals"), 
		(assign, ":chance_of_rivalry", 50),

	(else_try),	
		(eq, ":source_reputation", lrep_moralist),
		(eq, ":target_reputation", lrep_quarrelsome),
		
        (str_store_string, s17, "str_appears_to_be_a_man_who_lacks_selfdiscipline"), 
		(assign, ":chance_of_rivalry", 50),
##diplomacy start+ Support for promoted ladies:
   (else_try),
       #Ambitious vs otherworldly
       (eq, ":source_reputation", lrep_ambitious),
       (troop_slot_eq, ":source_lord", slot_troop_occupation, slto_kingdom_hero),
       (eq, ":target_reputation", lrep_otherworldly),
       (troop_slot_eq, ":target_lord", slot_troop_occupation, slto_kingdom_hero),
       (str_store_string, s17, "str_s18_is_soft_and_weak_and_not_fit_to_govern_a_fief_and_i_have_always_detested_him"),
       (str_store_string, s17, "str_s18_has_always_treated_me_contemptuously_although_i_have_done_him_no_wrong"),
		(assign, ":chance_of_rivalry", 100),
   (else_try),
       #Otherworldly vs ambitious
       (eq, ":source_reputation", lrep_otherworldly),
       (troop_slot_eq, ":source_lord", slot_troop_occupation, slto_kingdom_hero),
       (eq, ":target_reputation", lrep_ambitious),
       (troop_slot_eq, ":target_lord", slot_troop_occupation, slto_kingdom_hero),
       (str_store_string, s17, "str_s18_has_always_treated_me_contemptuously_although_i_have_done_him_no_wrong"),
		(assign, ":chance_of_rivalry", 100),
   (else_try),
       #Quarrelsome quarrels with conventional and moralist
       (eq, ":source_reputation", lrep_quarrelsome),
       (troop_slot_eq, ":target_lord", slot_troop_occupation, slto_kingdom_hero),
       (this_or_next|eq, ":target_reputation", lrep_moralist),
          (eq, ":target_reputation", lrep_conventional),
       (str_store_string, s17, "str_s18_once_took_something_i_said_amiss_stubborn_bastard_wont_give_it_up_and_keeps_trying_to_get_me_to_recant_my_words"),
		(assign, ":chance_of_rivalry", 50),
   (else_try),
        #Cunning conflicts with moralist
        (eq, ":source_reputation", lrep_cunning),
        (eq, ":target_reputation", lrep_moralist),
        (troop_slot_eq, ":target_lord", slot_troop_occupation, slto_kingdom_hero),
        (str_store_string, s17, "str_s18_i_am_sorry_to_say_is_far_too_softhearted_a_man_to_be_given_any_kind_of_responsibility_his_chivalry_will_allow_the_enemy_to_flee_to_fight_another_day_and_will_cost_the_lives_of_my_own_faithful_men"),
		(assign, ":chance_of_rivalry", 50),
    (else_try),
        #Debauched conflicts with moralist
        (eq, ":source_reputation", lrep_debauched),
        (troop_slot_eq, ":target_lord", slot_troop_occupation, slto_kingdom_hero),
        (eq, ":target_reputation", lrep_moralist),
		(str_store_string, s17, "str_s18_i_despite_him_he_puts_on_such_a_nauseating_display_of_virtue_and_thinks_nothing_of_insulting_his_betters"),
		(assign, ":chance_of_rivalry", 50),
    (else_try),
        #Martial or debauched conflicts with adventurous
	   (this_or_next|eq, ":source_reputation", lrep_martial),
	   (eq, ":source_reputation", lrep_debauched),
      (troop_slot_eq, ":target_lord", slot_troop_occupation, slto_kingdom_hero),
      (eq, ":target_reputation", lrep_adventurous),
      (str_store_string, s17, "str_s18_once_took_something_i_said_amiss_stubborn_bastard_wont_give_it_up_and_keeps_trying_to_get_me_to_recant_my_words"),
		(assign, ":chance_of_rivalry", 50),
	(else_try),
        (eq, ":source_reputation", lrep_goodnatured),
        (troop_slot_eq, ":target_lord", slot_troop_occupation, slto_kingdom_hero),
        (eq, ":target_reputation", lrep_ambitious),
        (str_store_string, s17, "str_s18_seems_to_have_something_against_me_for_some_reason_i_dont_like_to_talk_ill_of_people_but_i_think_hes_can_be_a_bit_of_a_cad_sometimes"),
		  (assign, ":chance_of_rivalry", 30),
##Add support for secondary morality types
	(else_try),
		(call_script, "script_dplmc_get_troop_morality_value", ":target_lord", tmt_honest),
		(ge, reg0, 1),#This would apply (if no previous condition was reached) to Marnid, Rolf, Firentis, Alayan, and Jeremus.
		(eq, ":source_reputation", lrep_moralist),
		(str_store_string, s17, "str_is_a_man_of_stalwart_character"),#<- (does not apply to Rolf, since he is Cunning)
		(assign, ":chance_of_rivalry", -50),
	(else_try),
		(call_script, "script_dplmc_get_troop_morality_value", ":target_lord", tmt_pious),
		(ge, reg0, 1),#This doesn't apply to anyone at the moment.
		(eq, ":source_reputation", lrep_moralist),
		(str_store_string, s17, "str_is_a_man_of_stalwart_character"),
		(assign, ":chance_of_rivalry", -50),
	(try_end),

##diplomacy end+

	(val_div, ":chance_of_rivalry", ":divisor"),
##diplomacy start+ for companions, use compatability information
    (try_begin),
	   #gekokujo 3.0 microfactions! include fort companions start
	   #(is_between, ":source_lord", companions_begin, companions_end),
	   (is_between, ":source_lord", companions_begin, fort_companions_end),
	   #gekokujo 3.0 microfactions! include fort companions end
	   (troop_slot_eq, ":source_lord", slot_troop_personalitymatch_object, ":target_lord"),
	   (val_min, ":chance_of_rivalry", -100),
	(else_try),
	   #gekokujo 3.0 microfactions! include fort companions start
	   #(is_between, ":source_lord", companions_begin, companions_end),
	   (is_between, ":source_lord", companions_begin, fort_companions_end),
	   #gekokujo 3.0 microfactions! include fort companions end
	   (this_or_next|troop_slot_eq, ":source_lord", slot_troop_personalityclash_object, ":target_lord"),
	   (troop_slot_eq, ":source_lord", slot_troop_personalityclash2_object, ":target_lord"),
	   (try_begin),
	      (le, ":chance_of_rivalry", 0),
		  (str_store_string, s17, "str_general_quarrel"),
	   (try_end),
	   (val_max, ":chance_of_rivalry", 100),
	(try_end),
	(assign, reg3, ":save_reg3"),#revert reg3
	(assign, reg65, ":save_reg65"),#revert reg65
##diplomacy end+
	(assign, reg0, ":chance_of_rivalry"),

	(neq, ":chance_of_rivalry", 0),
#	(eq, ":incompatibility_found", 1), #cf can be removed with this
	
	]),
  ("troop_get_romantic_chemistry_with_troop", #source is lady, target is man
    [
      ##diplomacy start+ (players of either gender may marry opposite-gender lords)
      #Note: the above is misleading even in Native, since when target_lord is the player,
      #target_lord can be female and source_lady can be male.
	  (assign, ":save_reg1", reg1),
      ##diplomacy end+
      (store_script_param, ":source_lady", 1),
      (store_script_param, ":target_lord", 2),
      
      (store_add, ":chemistry_sum", ":source_lady", ":target_lord"),
      (val_add, ":chemistry_sum", "$romantic_attraction_seed"),      
      
      #This calculates (modula ^ 2) * 3
      (store_mod, ":chemistry_remainder", ":chemistry_sum", 5),
      (val_mul, ":chemistry_remainder", ":chemistry_remainder"), #0, 1, 4, 9, 16
      (val_mul, ":chemistry_remainder", 3), #0, 3, 12, 27, 48

      (store_attribute_level, ":romantic_chemistry", ":target_lord", ca_charisma),
      (val_sub, ":romantic_chemistry", ":chemistry_remainder"),

      (val_mul, ":romantic_chemistry", 2),
      ##diplomacy start+ ensure companion compatability
      (try_begin),
  	     #gekokujo 3.0 microfactions! include fort companions start
         #(is_between, ":source_lady", companions_begin, companions_end),
         (is_between, ":source_lady", companions_begin, fort_companions_end),
  	     #gekokujo 3.0 microfactions! include fort companions end
         (troop_slot_eq, ":source_lady", slot_troop_personalitymatch_object, ":target_lord"),
         (val_max, ":romantic_chemistry", 15),
      (else_try),
  	     #gekokujo 3.0 microfactions! include fort companions start
         #(is_between, ":target_lord", companions_begin, companions_end),
         (is_between, ":target_lord", companions_begin, fort_companions_end),
  	     #gekokujo 3.0 microfactions! include fort companions end
         (troop_slot_eq, ":target_lord", slot_troop_personalitymatch_object, ":source_lady"),
         (val_max, ":romantic_chemistry", 15),
	  #...and companion incompatibility.
	  (else_try),
  	     #gekokujo 3.0 microfactions! include fort companions start
  	     #(is_between, ":source_lady", companions_begin, companions_end),
  	     (is_between, ":source_lady", companions_begin, fort_companions_end),
  	     #gekokujo 3.0 microfactions! include fort companions end
		 (this_or_next|troop_slot_eq, ":source_lady", slot_troop_personalityclash_object, ":target_lord"),
			(troop_slot_eq, ":source_lady", slot_troop_personalityclash2_object, ":target_lord"),
		 (val_min, ":romantic_chemistry", -15),
  	  (else_try),
  	     #gekokujo 3.0 microfactions! include fort companions start
  	     #(is_between, ":target_lord", companions_begin, companions_end),
  	     (is_between, ":target_lord", companions_begin, fort_companions_end),
  	     #gekokujo 3.0 microfactions! include fort companions end
		 (this_or_next|troop_slot_eq, ":target_lord", slot_troop_personalityclash_object, ":source_lady"),
			(troop_slot_eq, ":target_lord", slot_troop_personalityclash2_object, ":source_lady"),
		(val_min, ":romantic_chemistry", -15),
	  #Prevent glitches.  This can be enabled explicitly if intentional.
      (else_try),
	     (call_script, "script_dplmc_store_is_female_troop_1_troop_2", ":source_lady", ":target_lord"),
         (eq, reg0, reg1),#different genders
         (val_min, ":romantic_chemistry", -15),
      (try_end),
	  (assign, reg1, ":save_reg1"),
      ##diplomacy end+
      (assign, reg0, ":romantic_chemistry"),

      #examples :
      #For a charisma of 18, yields (18 - 0) * 2 = 36, (18 - 3) * 2 = 30, (18 - 12) * 2 = 12, (18 - 27) * 2 = -18, (18 - 48) * 2 = -60
      #For a charisma of 10, yields (10 - 0) * 2 = 20, (10 - 3) * 2 = 14, (10 - 12) * 2 = -4, (10 - 27) * 2 = -34, (10 - 48) * 2 = -76
      #For a charisma of 7, yields  (7 - 0) * 2 = 14,  (7 - 3) * 2 = 8,   (7 - 12) * 2 = -10, (7 - 27) * 2 = -40,  (7 - 48) * 2 = -82

      #15 is high attraction, 0 is moderate attraction, -76 is lowest attraction
	]),
  ("cf_troop_get_romantic_attraction_to_troop", #source is lady, target is man
    [	

	(store_script_param, ":source_lady", 1),
	(store_script_param, ":target_lord", 2),

	(assign, ":weighted_romantic_assessment", 0),
    ##diplomacy start+
	(assign, ":save_reg1", reg1),
	#Use gender script
	#(troop_get_type, ":source_is_female", ":source_lady"),
	#(eq, ":source_is_female", 1),
	#(troop_get_type, ":target_is_female", ":target_lord"),
	#(eq, ":target_is_female", 0),
	(call_script, "script_dplmc_store_is_female_troop_1_troop_2", ":source_lady", ":target_lord"),
	(assign, ":source_is_female", reg0),
	(assign, ":target_is_female", reg1),
	(assign, reg1, ":save_reg1"),
   (assign, reg0, -15),
	(neq, ":source_is_female", ":target_is_female"),
	##diplomacy end+

	(call_script, "script_troop_get_romantic_chemistry_with_troop", ":source_lady", ":target_lord"),
	(assign, ":romantic_chemistry", reg0),

	
	#objective attraction - average renown
	(troop_get_slot, ":modified_renown", ":target_lord", slot_troop_renown),
	(assign, ":lady_status", 60),
   ##diplomacy start+ adjust status based on who they are
	(try_begin),
      #The renown bonus is decreased the more important the lady's relatives are.
      (ge, "$g_dplmc_ai_changes", DPLMC_AI_CHANGES_HIGH),
      (troop_get_slot, ":best_renown", ":source_lady", slot_troop_renown),
      (try_begin),
        (troop_get_slot, ":relative", ":source_lady", slot_troop_father),
        (ge, ":relative", 0),
        (troop_get_slot, ":other_renown", ":relative", slot_troop_renown),
        (val_max, ":best_renown", ":other_renown"),
   	(try_end),
   	(try_begin),
		  (troop_get_slot, ":relative", ":source_lady", slot_troop_guardian),
        (ge, ":relative", 0),
        (troop_get_slot, ":other_renown", ":relative", slot_troop_renown),
        (val_max, ":best_renown", ":other_renown"),
   	(try_end),
   	(try_begin),
		  (troop_get_slot, ":relative", ":source_lady", slot_troop_mother),
        (ge, ":relative", 0),
        (troop_get_slot, ":other_renown", ":relative", slot_troop_renown),
        (val_max, ":best_renown", ":other_renown"),
   	(try_end),
   	(try_begin),
		  (ge, ":best_renown", 600),
        (store_div, ":lady_status", ":best_renown", 10),
   	(else_try),
		  (lt, ":best_renown", 400),
        (store_div, ":lady_status", ":best_renown", 10),
		  (val_add, ":lady_status", 20),
   	(try_end),
   	(val_clamp, ":lady_status", 30, 90),
   (try_end),
   ##diplomacy end+
	(val_div, ":modified_renown", 5),
	(val_sub, ":modified_renown", ":lady_status"),
	(val_min, ":modified_renown", 60),


	
	#weight values
	(try_begin),
		(assign, ":personality_match", 0),
		(call_script, "script_cf_test_lord_incompatibility_to_s17", ":source_lady", ":target_lord"),
		(store_sub, ":personality_match", 0, reg0),
	(try_end),
	
	(troop_get_slot, ":lady_reputation", ":source_lady", slot_lord_reputation_type),
	(try_begin),
		(eq, ":lady_reputation", lrep_ambitious),
		(val_mul, ":modified_renown", 2),
		(val_div, ":romantic_chemistry", 2),
	(else_try),
		(eq, ":lady_reputation", lrep_otherworldly),
		(val_div, ":modified_renown", 2),
		(val_mul, ":romantic_chemistry", 2),
	(else_try),
		(eq, ":lady_reputation", lrep_adventurous),
		(val_div, ":modified_renown", 2),
	(else_try),
		(eq, ":lady_reputation", lrep_moralist),
		(val_div, ":modified_renown", 2),
		(val_div, ":romantic_chemistry", 2),
	(try_end),

	(val_add, ":weighted_romantic_assessment", ":romantic_chemistry"),
	(val_add, ":weighted_romantic_assessment", ":personality_match"),
	(val_add, ":weighted_romantic_assessment", ":modified_renown"),
	
	(assign, reg0, ":weighted_romantic_assessment"),
	
	]),
  ("cf_random_political_event", #right now, just enmities
    [

	##diplomacy start+ Lay more groundwork for heroes other than active-npcs being lords
	##OLD:
	#(store_random_in_range, ":lord_1", active_npcs_begin, active_npcs_end),
	#(store_random_in_range, ":lord_2", active_npcs_begin, active_npcs_end),
	##NEW:
	(store_random_in_range, ":lord_1", heroes_begin, heroes_end),
	(try_begin),
	   (neg|is_between, ":lord_1", active_npcs_begin, active_npcs_end),
	   (neg|troop_slot_eq, ":lord_1", slot_troop_occupation, slto_kingdom_hero),
	   (store_random_in_range, ":lord_1", active_npcs_begin, active_npcs_end),
	(try_end),
	(store_random_in_range, ":lord_2", heroes_begin, heroes_end),
	(try_begin),
	   (neg|is_between, ":lord_2", active_npcs_begin, active_npcs_end),
	   (neg|troop_slot_eq, ":lord_2", slot_troop_occupation, slto_kingdom_hero),
	   (store_random_in_range, ":lord_2", active_npcs_begin, active_npcs_end),
	(try_end),
	##diplomacy end+

	(troop_slot_eq, ":lord_1", slot_troop_occupation, slto_kingdom_hero),
	(troop_slot_eq, ":lord_2", slot_troop_occupation, slto_kingdom_hero),

	(neq, ":lord_1", ":lord_2"),
	
	(val_add, "$total_political_events", 1),
					
	(store_troop_faction, ":lord_1_faction", ":lord_1"),
	(store_troop_faction, ":lord_2_faction", ":lord_2"),
	
	(assign, reg8, "$total_political_events"),
	
	
	(faction_get_slot, ":faction_1_leader", ":lord_1_faction", slot_faction_leader),
	(faction_get_slot, ":faction_2_leader", ":lord_2_faction", slot_faction_leader),
	
	(this_or_next|eq, ":lord_1_faction", ":lord_2_faction"),
	(this_or_next|eq, ":lord_1", ":faction_1_leader"),
		(eq, ":lord_2", ":faction_2_leader"),
	
	
	(call_script, "script_troop_get_relation_with_troop", ":lord_1", ":lord_2"),
	(assign, ":relation", reg0),
	

	(store_random_in_range, ":random", 0, 100),
		
	(try_begin),
		#reconciliation
		#The chance of a liege reconciling two quarreling vassals is equal to (relationship with lord 1 x relationship with lord 2) / 4
		
		(eq, ":lord_1_faction", ":lord_2_faction"),
		(neq, ":faction_1_leader", "trp_player"),
		
		(le, ":relation", -10),
		
#		(ge, "$total_political_events", 5000),

		(call_script, "script_troop_get_relation_with_troop", ":lord_1", ":faction_1_leader"),
		(gt, reg0, 0),
		(assign, ":lord_1_leader_rel", reg0),
		
		(call_script, "script_troop_get_relation_with_troop", ":lord_2", ":faction_1_leader"),
		(gt, reg0, 0),
		(store_mul, ":reconciliation_chance", ":lord_1_leader_rel", reg0),		
		(val_div, ":reconciliation_chance", 4),	#was 2 before	
				
		(le, ":random", ":reconciliation_chance"), 
		
		(str_store_troop_name, s4, ":faction_1_leader"),
		(str_store_troop_name, s5, ":lord_1"),
		(str_store_troop_name, s6, ":lord_2"),
		(try_begin),
			(eq, "$cheat_mode", 1),
			(display_message, "str_check_reg8_s4_reconciles_s5_and_s6_"),
		(try_end),
		
		(call_script, "script_troop_change_relation_with_troop", ":lord_1", ":lord_2", 20),
		(val_add, "$total_random_quarrel_changes", 20),
	(else_try),	#lord intervenes in quarrel
		(eq, ":lord_1_faction", ":lord_2_faction"),

		(le, ":relation", -10),
#		(ge, ":random", 50),
		(try_begin),
			(eq, ":faction_1_leader", "trp_player"),
			(try_begin),
				(eq, "$cheat_mode", 1),
				(display_message, "str_diagnostic__player_should_receive_consultation_quest_here_if_not_already_active"),
			(try_end),
			(neg|check_quest_active, "qst_consult_with_minister"),
			(neg|check_quest_active, "qst_resolve_dispute"),
			(eq, "$g_minister_notification_quest", 0),
			(assign, "$g_minister_notification_quest", "qst_resolve_dispute"),
			(quest_set_slot, "qst_resolve_dispute", slot_quest_target_troop, ":lord_1"),
			(quest_set_slot, "qst_resolve_dispute", slot_quest_object_troop, ":lord_2"),
			
			(call_script, "script_add_notification_menu", "mnu_notification_player_should_consult", 0, 0),
			
			
		(else_try),
			(call_script, "script_troop_get_relation_with_troop", ":lord_1", ":faction_1_leader"),
			(assign, ":lord_1_rel_w_leader", reg0),
			
			(call_script, "script_troop_get_relation_with_troop", ":lord_2", ":faction_1_leader"),
			(assign, ":lord_2_rel_w_leader", reg0),
			
			(store_random_in_range, ":another_random", -5, 5),

			(val_add, ":lord_1_rel_w_leader", ":another_random"),
			
			(try_begin),
				(ge, ":lord_1_rel_w_leader", ":lord_2_rel_w_leader"),
				(assign, ":winner_lord", ":lord_1"),
				(assign, ":loser_lord", ":lord_2"),
			(else_try),
				(assign, ":loser_lord", ":lord_1"),
				(assign, ":winner_lord", ":lord_2"),
			(try_end),
			
			(str_store_troop_name, s4, ":faction_1_leader"),
			(str_store_troop_name, s5, ":winner_lord"),
			(str_store_troop_name, s6, ":loser_lord"),

			(try_begin),
				(eq, "$cheat_mode", 1),
				(display_message, "str_check_reg8_s4_rules_in_s5s_favor_in_quarrel_with_s6_"),
			(try_end), 
			 
			(call_script, "script_add_log_entry", logent_ruler_intervenes_in_quarrel, ":faction_1_leader",  ":loser_lord", ":winner_lord", ":lord_1_faction"), #faction leader is actor, loser lord is center object, winner lord is troop_object
			
			(call_script, "script_troop_change_relation_with_troop", ":winner_lord", ":faction_1_leader", 10),
			(call_script, "script_troop_change_relation_with_troop", ":loser_lord", ":faction_1_leader", -20),
			(val_add, "$total_random_quarrel_changes", -10),

		(try_end),

		
	(else_try), #new quarrel - companions
		#gekokujo 3.0 microfactions! include fort companions start
		#(is_between, ":lord_1", companions_begin, companions_end),
		#(is_between, ":lord_2", companions_begin, companions_end),
		(is_between, ":lord_1", companions_begin, fort_companions_end),
		(is_between, ":lord_2", companions_begin, fort_companions_end),
		#gekokujo 3.0 microfactions! include fort companions end
		
		(ge, ":relation", -10), 		
		(this_or_next|troop_slot_eq, ":lord_1", slot_troop_personalityclash_object, ":lord_2"),
			(troop_slot_eq, ":lord_1", slot_troop_personalityclash2_object, ":lord_2"),
		
		(str_store_troop_name, s5, ":lord_1"),
		(str_store_troop_name, s6, ":lord_2"),
		
		(try_begin),
			(eq, "$cheat_mode", 1),
			(display_message, "str_check_reg8_new_rivalry_generated_between_s5_and_s6"),
		(try_end),
		
		(call_script, "script_troop_change_relation_with_troop", ":lord_1", ":lord_2", -30),
		(val_add, "$total_random_quarrel_changes", -30),
				
		
	(else_try), #new quarrel - others
		(eq, ":lord_1_faction", ":lord_2_faction"),

		(ge, ":relation", -10), #can have two quarrels

		(call_script, "script_cf_test_lord_incompatibility_to_s17", ":lord_1", ":lord_2"),
		(assign, ":chance_of_enmity", reg0),
		(gt, ":chance_of_enmity", 0),
	
	
		(lt, ":random", ":chance_of_enmity"), #50 or 100 percent, usually
	
	
		(str_store_troop_name, s5, ":lord_1"),
		(str_store_troop_name, s6, ":lord_2"),
		(try_begin),
			(eq, "$cheat_mode", 1),
			(display_message, "str_check_reg8_new_rivalry_generated_between_s5_and_s6"),
		(try_end),
		
		(call_script, "script_troop_change_relation_with_troop", ":lord_1", ":lord_2", -30),
		(val_add, "$total_random_quarrel_changes", -30),

#		(call_script, "script_update_troop_notes", ":lord_1"),
#		(call_script, "script_update_troop_notes", ":lord_2"),
	(else_try), #a lord attempts to suborn a character
		(store_current_hours, ":hours"),
		(ge, ":hours", 24),
	
		(neq, ":lord_1_faction", ":lord_2_faction"),
#		(eq, ":lord_1", ":faction_1_leader"),
		(is_between, ":lord_1_faction", kingdoms_begin, kingdoms_end),
		
		(call_script, "script_cf_troop_can_intrigue", ":lord_2", 0),
		(neq, ":lord_2", ":faction_2_leader"),
		(neq, ":lord_2", ":faction_1_leader"),
		
		(str_store_troop_name, s5, ":faction_1_leader"),
		(str_store_troop_name, s6, ":lord_2"),		

		(try_begin),
			(ge, "$cheat_mode", 1),
			(display_message, "str_check_reg8_s5_attempts_to_win_over_s6"),
		(try_end),
			
		(call_script, "script_calculate_troop_political_factors_for_liege", ":lord_2", ":faction_1_leader"),
		(assign, ":lord_1_score", reg0),

		(call_script, "script_calculate_troop_political_factors_for_liege", ":lord_2", ":faction_2_leader"),
		(assign, ":faction_2_leader_score", reg0),

		(try_begin),
			(gt, ":lord_1_score", ":faction_2_leader_score"),
			
			
			(try_begin),
				(ge, "$cheat_mode", 1),
				(str_store_troop_name, s4, ":lord_2"),
				(display_message, "@{!}DEBUG - {s4} faction changed in subornment"), 
			(try_end),
			
			(call_script, "script_change_troop_faction", ":lord_2", ":lord_1_faction"),		
		(try_end),
	(try_end),
	
	
	
]),
#this calculates the average number of rivalries per lord, giving a rough indication of how easily a faction may be divided
#fairly expensive in terms of CPU
  ("evaluate_realm_stability",
 
    [
	(store_script_param, ":realm", 1),

	(assign, ":total_lords", 0),
	(assign, ":total_restless_lords", 0),
	(assign, ":total_disgruntled_lords", 0),
	
	(faction_get_slot, ":liege", ":realm", slot_faction_leader),
	
	(try_for_range, ":lord", active_npcs_begin, active_npcs_end),
		(troop_slot_eq, ":lord", slot_troop_occupation, slto_kingdom_hero),
		(store_troop_faction, ":lord_faction", ":lord"),
		(eq, ":lord_faction", ":realm"),
		(val_add, ":total_lords", 1),

		(call_script, "script_calculate_troop_political_factors_for_liege", ":lord", ":liege"),
		(try_begin),
			(le, reg3, -10),
			(val_add, ":total_disgruntled_lords", 1),
		(else_try),
			(le, reg3, 10),
			(val_add, ":total_restless_lords", 1),
		(try_end),
	(try_end),
	
	(try_begin),
		(gt, ":total_lords", 0),
		(store_mul, ":instability_quotient", ":total_disgruntled_lords", 100),
		(val_div, ":instability_quotient", ":total_lords"),

		(store_mul, ":restless_quotient", ":total_restless_lords", 100),
		(val_div, ":restless_quotient", ":total_lords"),

		(store_mul, ":combined_quotient", ":instability_quotient", 2),
		(val_add, ":combined_quotient", ":restless_quotient"),
		(faction_set_slot, ":realm", slot_faction_instability, ":combined_quotient"),
	
		(assign, reg0, ":instability_quotient"),
		(assign, reg1, ":restless_quotient"),
		(assign, reg1, ":restless_quotient"),
	(else_try),
		(try_begin),
			(eq, "$cheat_mode", 1),
			(str_store_faction_name, s1, ":realm"),
			(display_message, "str_s1_has_no_lords"),
		(try_end),
		(assign, reg0, 0),
		(assign, reg1, 0),
	(try_end),
	
	]),
#called from game_event_simulate_battle
#Includes a number of consequences that follow on battles, mostly affecting relations between different NPCs
#This only fires from complete victories
  ("battle_political_consequences",
    [
	(store_script_param, ":defeated_party", 1),
	(store_script_param, ":winner_party", 2),

	(try_begin),
		(eq, "$cheat_mode", 1),
		(str_store_party_name, s4, ":winner_party"),
		(str_store_party_name, s5, ":defeated_party"),
		(display_message, "str_do_political_consequences_for_s4_victory_over_s5"),
	(try_end),
	
	(store_faction_of_party, ":winner_faction", ":winner_party"),
	(try_begin),
		(eq, ":winner_party", "p_main_party"),
		(assign, ":winner_faction", "$players_kingdom"),
	(try_end),
		
	(party_get_template_id, ":defeated_party_template", ":defeated_party"),
		
	#did the battle involve travellers?	
	(try_begin),
		(this_or_next|eq, ":defeated_party_template", "pt_village_farmers"),
			(eq, ":defeated_party_template", "pt_kingdom_caravan_party"),

			
		(party_get_slot, ":destination", ":defeated_party", slot_party_ai_object),
		(party_get_slot, ":origin", ":defeated_party", slot_party_last_traded_center),
		
        (call_script, "script_add_log_entry", logent_traveller_attacked, ":winner_party",  ":origin", ":destination", ":winner_faction"),
		
		(try_begin),
			(eq, "$cheat_mode", 2),
			(neg|is_between, ":winner_faction", kingdoms_begin, kingdoms_end),
			(str_store_string, s65, "str_bandits_attacked_a_party_on_the_roads_so_a_bounty_is_probably_available"),
			(call_script, "script_add_notification_menu", "mnu_debug_alert_from_s65", 0, 0),

			(str_store_party_name, s15, ":origin"),
			(str_store_party_name, s16, ":destination"),
			(display_message, "str_travellers_attacked_on_road_from_s15_to_s16"),
		(try_end),
		
		
		#by logging the faction and the party, we can verify that the party number is unlikely to have been reassigned - or at any rate, that the factions have not changed 
	(try_end),
	
	#winner consequences:
	#1)   leader improves relations with other leaders
	#2)  Player given credit for victory if the victorious party is following the player's advice
	(try_begin),
		(party_get_template_id, ":winner_party_template", ":winner_party"),
		(eq, ":winner_party_template", "pt_kingdom_hero_party"),
		(neq, ":winner_party", "p_main_party"),
		#Do not do for player party, as is included in post-battle dialogs

		(party_stack_get_troop_id, ":winner_leader", ":winner_party", 0),
		##diplomacy start+ Support additional types
		(troop_is_hero, ":winner_leader"),
		(this_or_next|troop_slot_eq, ":winner_leader", slot_troop_occupation, slto_kingdom_hero),
		##diplomacy end+
		(is_between, ":winner_leader", active_npcs_begin, active_npcs_end),

		(store_faction_of_party, ":winner_faction", ":winner_party"),

		(party_collect_attachments_to_party, ":winner_party", "p_temp_party_2"),
        (party_get_num_companion_stacks, ":num_stacks", "p_temp_party_2"),
		(try_for_range, ":troop_iterator", 0, ":num_stacks"),
            (party_stack_get_troop_id, ":cur_troop_id", "p_temp_party_2", ":troop_iterator"),
	    ##diplomacy start+ support promoted kingdom ladies
	    (is_between, ":cur_troop_id", heroes_begin, heroes_end),
	    (this_or_next|troop_slot_eq, ":cur_troop_id", slot_troop_occupation, slto_kingdom_hero),
	    ##diplomacy end+
            (is_between, ":cur_troop_id", active_npcs_begin, active_npcs_end),
			
			(try_begin),
				(troop_get_slot, ":winner_lord_party", ":cur_troop_id", slot_troop_leaded_party),
				(party_is_active, ":winner_lord_party"),				
				(call_script, "script_cf_party_under_player_suggestion", ":winner_lord_party"),
				(call_script, "script_add_log_entry", logent_player_suggestion_succeeded, "trp_player", -1, ":cur_troop_id", -1),
			(try_end),

			
			(store_faction_of_troop, ":troop_faction", ":cur_troop_id"),
			(eq, ":troop_faction", ":winner_faction"),
			(neq, ":cur_troop_id", ":winner_leader"),

			(try_begin),
				(eq, "$cheat_mode", 4),
				(str_store_troop_name, s15, ":cur_troop_id"),
				(str_store_troop_name, s16, ":winner_leader"),
				(display_message, "str_s15_shares_joy_of_victory_with_s16"),
			(try_end),
			
			(call_script, "script_troop_change_relation_with_troop", ":cur_troop_id", ":winner_leader", 3),
			(val_add, "$total_battle_ally_changes", 3),

		(try_end),
		(party_clear, "p_temp_party_2"),
	(try_end),
	
	#consequences of defeat,
	#1) -1 relation with lord per lord, plus -15 if there is an incompatible marshal
	#2)  losers under player suggestion blame the player
	#3) Some losers resent the victor lord
	#4) Possible quarrels over defeat
	(try_begin),
		(party_collect_attachments_to_party, ":defeated_party", "p_temp_party_2"),
        (party_get_num_companion_stacks, ":num_stacks", "p_temp_party_2"),

		(try_begin),
			(gt, "$marshall_defeated_in_battle", 0),
			(str_store_troop_name, s15, "$marshall_defeated_in_battle"),
			(store_faction_of_troop, ":defeated_marshall_faction", "$marshall_defeated_in_battle"),
            (try_begin),
                (eq, "$cheat_mode", 1),
			    (display_message, "str_faction_marshall_s15_involved_in_defeat"),
            (try_end),
		(else_try),
			(eq, "$marshall_defeated_in_battle", "trp_player"),
			(eq, ":defeated_party", "p_main_party"),
			(faction_slot_eq, "fac_player_supporters_faction", slot_faction_state, sfs_active),
            (try_begin),
                (eq, "$cheat_mode", 1),
			    (display_message, "str_player_faction_marshall_involved_in_defeat"),
            (try_end),
		(else_try),	
			(assign, "$marshall_defeated_in_battle", -1),
		(try_end),
		
		(try_for_range, ":troop_iterator", 0, ":num_stacks"),
            (party_stack_get_troop_id, ":cur_troop_id", "p_temp_party_2", ":troop_iterator"),
            (troop_slot_eq, ":cur_troop_id", slot_troop_occupation, slto_kingdom_hero),					
		
			(try_begin), #is party under suggestion?
				(troop_get_slot, ":defeated_lord_party", ":cur_troop_id", slot_troop_leaded_party),
				(party_is_active, ":defeated_lord_party"),

				#is party under suggestion?
				(call_script, "script_cf_party_under_player_suggestion", ":defeated_lord_party"),
				(call_script, "script_add_log_entry", logent_player_suggestion_failed, "trp_player", -1, ":cur_troop_id", -1),		
			(try_end),

			
			(store_faction_of_troop, ":troop_faction", ":cur_troop_id"),
			
			(faction_get_slot, ":faction_leader", ":troop_faction", slot_faction_leader),
			(neq, ":cur_troop_id", ":faction_leader"),
			
			#Lose one point relation with liege
			(try_begin),
				(eq, "$cheat_mode", 1),
				(str_store_troop_name, s14, ":cur_troop_id"),
				(str_store_faction_name, s15, ":troop_faction"),
				
				(display_message, "str_s14_of_s15_defeated_in_battle_loses_one_point_relation_with_liege"),
			(try_end),
			
			(try_begin),
				(this_or_next|neq, ":faction_leader", "trp_player"), #if leader is zero at beginning of game. I'm not entirely sure how this could happen...
					(eq, "$players_kingdom", ":troop_faction"),
				
				(call_script, "script_troop_change_relation_with_troop", ":cur_troop_id", ":faction_leader", -1),
				(val_add, "$total_battle_ally_changes", -1),
			(try_end),
			
	
			(call_script, "script_faction_inflict_war_damage_on_faction", ":winner_faction", ":troop_faction", 10),
		
			
			(try_begin),
				(this_or_next|is_between, ":winner_leader", active_npcs_begin, active_npcs_end),
					(eq, ":winner_leader", "trp_player"),
					
				(this_or_next|neq, ":winner_leader", "trp_player"), #prevents winner leader being zero, for whatever reason
					(eq, ":winner_party", "p_main_party"),
				
				(this_or_next|troop_slot_eq, ":cur_troop_id", slot_lord_reputation_type, lrep_quarrelsome),
				(this_or_next|troop_slot_eq, ":cur_troop_id", slot_lord_reputation_type, lrep_selfrighteous),
					(troop_slot_eq, ":cur_troop_id", slot_lord_reputation_type, lrep_debauched),
			
				(call_script, "script_troop_change_relation_with_troop", ":cur_troop_id", ":winner_leader", -1),
				(val_add, "$total_battle_enemy_changes", -1),
				
				(try_begin),
					(eq, "$cheat_mode", 1),
					(str_store_troop_name, s14, ":cur_troop_id"),
					(str_store_troop_name, s15, ":winner_leader"),
				
					(display_message, "str_s14_defeated_in_battle_by_s15_loses_one_point_relation"),
				(try_end),

				
			(try_end),
			
			(gt, "$marshall_defeated_in_battle", -1),
			(eq, ":troop_faction", ":defeated_marshall_faction"),
			(str_store_troop_name, s14, ":cur_troop_id"),
			
			(call_script, "script_cf_test_lord_incompatibility_to_s17", ":cur_troop_id", "$marshall_defeated_in_battle"),
            (try_begin),
                (eq, "$cheat_mode", 1),
			    (display_message, "str_s14_blames_s15_for_defeat"),
            (try_end),
			
			(call_script, "script_add_log_entry", logent_lord_blames_defeat, ":cur_troop_id", "$marshall_defeated_in_battle", ":faction_leader", ":winner_faction"),

			(call_script, "script_troop_change_relation_with_troop", ":cur_troop_id", ":faction_leader", -15),
			(val_add, "$total_battle_ally_changes", -15),
			
			(neq, "$marshall_defeated_in_battle", ":faction_leader"),
			(call_script, "script_troop_change_relation_with_troop", ":cur_troop_id", "$marshall_defeated_in_battle", -15),
			(val_add, "$total_battle_ally_changes", -15),
			
		(try_end),
		
		(party_clear, "p_temp_party_2"),
	(try_end),
	]),
    ("faction_inflict_war_damage_on_faction",
    [
	(store_script_param, ":actor_faction", 1),
	(store_script_param, ":target_faction", 2),
	(store_script_param, ":amount", 3),
	
	
	(store_add, ":slot_war_damage", ":target_faction", slot_faction_war_damage_inflicted_on_factions_begin),
	(val_sub, ":slot_war_damage", kingdoms_begin),
	##diplomacy start+ Due to aberrant behavior, non-standard kingdoms
	##like fac_commoners can end up with parties on the map, and possibly
	##could end up inflicting or receiving war damage.  Guard against this.
	(try_begin),
	(is_between, ":slot_war_damage", slot_faction_war_damage_inflicted_on_factions_begin, slot_faction_war_damage_inflicted_on_factions_end),
	(gt, ":actor_faction", 0),
	##diplomacy end+
	(faction_get_slot, ":cur_war_damage", ":actor_faction", ":slot_war_damage"),

	(val_add, ":cur_war_damage", ":amount"),
	(faction_set_slot, ":actor_faction", ":slot_war_damage", ":cur_war_damage"),
	##diplomacy start+ Close added if-statement
	(else_try),
	   #For use in cheat-mode below
	   (assign, ":cur_war_damage", 0),
	(try_end),
	##diplomacy end+


	(try_begin),
	  (ge, "$cheat_mode", 1),
	  (str_store_faction_name, s4, ":actor_faction"),
	  (str_store_faction_name, s5, ":target_faction"),
	  (assign, reg3, ":cur_war_damage"),
	  (assign, reg4, ":amount"),
	  (display_message, "@{!}{s4} inflicts {reg4} damage on {s5}, raising total inflicted to {reg3}"),
	(try_end),

	
	(faction_get_slot, ":faction_marshal", ":target_faction", slot_faction_marshall),
	(try_begin),
		(ge, ":faction_marshal", 0),
		(gt, ":amount", 0),
		
		(troop_get_slot, ":controversy", ":faction_marshal", slot_troop_controversy),
		(val_add, ":controversy", ":amount"),
		(val_min, ":controversy", 100),
		(troop_set_slot, ":faction_marshal", slot_troop_controversy, ":controversy"),
		
		(try_begin),
			(ge, "$cheat_mode", 1),
			(str_store_troop_name, s4, ":faction_marshal"),
			(assign, reg4, ":amount"),
			(assign, reg5, ":controversy"),
			(display_message, "@{!}War damage raises {s4}'s controversy by {reg4} to {reg5}"),
		(try_end),
	(try_end),

	(faction_get_slot, ":faction_marshal", ":actor_faction", slot_faction_marshall),
	(try_begin),
		(ge, ":faction_marshal", 0),
		(val_div, ":amount", 3),
		(gt, ":amount", 0),
		
		
		(troop_get_slot, ":controversy", ":faction_marshal", slot_troop_controversy),
		(val_sub, ":controversy", ":amount"),
		(val_max, ":controversy", 0),
		(troop_set_slot, ":faction_marshal", slot_troop_controversy, ":controversy"),
		
		(try_begin),
			(ge, "$cheat_mode", 1),
			(str_store_troop_name, s4, ":faction_marshal"),
			(assign, reg4, ":amount"),
			(assign, reg5, ":controversy"),
			(display_message, "@{!}War damage lowers {s4}'s controversy by {reg4} to {reg5}"),
		(try_end),
	(try_end),


	
	]),
    ("calculate_troop_political_factors_for_liege",
    [
	(store_script_param, ":troop", 1),
	(store_script_param, ":liege", 2),

	(troop_get_slot, ":lord_reputation", ":troop", slot_lord_reputation_type),
	
	##diplomacy start+ Work correctly in certain situations where this can be called w/o a liege.
	##OLD:
	#(store_faction_of_troop, ":faction", ":liege"),
	##NEW:
	(try_begin),
	   (eq, ":liege", "trp_player"),
	   (assign, ":faction", "fac_player_supporters_faction"),
	   (try_begin),
	     #Handle "player is co-ruler of NPC faction"
	     (is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
	     (call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", "$players_kingdom"),
	     (ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
	     (assign, ":faction", "$players_kingdom"),
	     (faction_get_slot, reg0, ":faction", slot_faction_leader),
	     (gt, reg0, 0),
	     (assign, ":liege", reg0),
	   (try_end),
	(else_try),
	   #Ordinary case
	   (ge, ":liege", 0),
	   (store_faction_of_troop, ":faction", ":liege"),
	(else_try),
	   (store_faction_of_troop, reg0, ":troop"),
	   (faction_slot_eq, reg0, slot_faction_leader, ":liege"),
	   (assign, ":faction", reg0),
	(else_try),
	   (assign, ":faction", kingdoms_end),
	   (try_for_range, reg0, kingdoms_begin, ":faction"),
	      (faction_slot_eq, reg0, slot_faction_leader, ":liege"),
	      (assign, ":faction", reg0),
	   (try_end),
	   (neg|is_between, ":faction", kingdoms_begin, kingdoms_end),
	   (assign, ":faction", "fac_no_faction"),
	(try_end),
	##diplomacy end+

	
	(try_begin),
		(eq, ":faction", "fac_player_faction"),
		(assign, ":faction", "fac_player_supporters_faction"),
	(try_end),

	(assign, ":liege_is_undeclared_rebel", 0),
	(try_begin),
		(neg|faction_slot_eq, ":faction", slot_faction_leader, ":liege"),
		#the liege is a rebel
		(assign, ":liege_is_undeclared_rebel", 1),
		(try_begin),
			(eq, "$cheat_mode", 1),
                        ##diplomacy start+ Guard against bad liege
                        (ge, ":liege", 0),
                        ##diplomacy end+
			(str_store_troop_name, s32, ":liege"),
			(display_message, "str_s32_is_undeclared_rebel"),
		(try_end),
	(try_end),	
	
	(assign, ":result_for_material", 0),
	(assign, ":penalty_for_changing_sides", 0),

	

	#FACTOR 1 - MILITARY SECURITY
	(assign, ":result_for_security", 0),

	#find the lord's home
	(assign, ":base_center", -1),
	(try_begin),
		##diplomacy start+ add support for promoted kingdom ladies
		(is_between, ":troop", heroes_begin, heroes_end),
		(this_or_next|troop_slot_eq, ":troop", slot_troop_occupation, slto_kingdom_hero),
		##diplomacy end+
		(is_between, ":troop", active_npcs_begin, active_npcs_end),
		(try_for_range, ":center", centers_begin, centers_end),
			(eq, ":base_center", -1),
			(party_slot_eq, ":center", slot_town_lord, ":troop"),
			(assign, ":base_center", ":center"),
		(try_end),
	(try_end),
	
	(assign, ":faction_has_base", 0),
	
	#add up all other centers for the security value
	(try_for_range, ":center", centers_begin, centers_end),
		(neq, ":center", ":base_center"),
		(gt, ":base_center", 0),
	
		(try_begin),
			(is_between, ":center", towns_begin, towns_end),
			(assign, ":weight", 9000),
		(else_try),
			(is_between, ":center", castles_begin, castles_end),
			(assign, ":weight", 6000),
		(else_try),
			(assign, ":weight", 1000),	
		(try_end),

		(store_distance_to_party_from_party, ":distance", ":base_center", ":center"),
		(val_add, ":distance", 10),
		(val_div, ":weight", ":distance"),
		(val_div, ":weight", ":distance"),
		
		(store_faction_of_party, ":center_faction", ":center"),

		(try_begin),
			(eq, ":center_faction", ":faction"),

			(assign, ":faction_has_base", 1),
			(val_add, ":result_for_security", ":weight"),
		(else_try),
			(neq, ":center_faction", ":faction"),
			(store_relation, ":center_relation", ":center_faction", ":faction"),
		
			(try_begin), #potentially hostile center
				(this_or_next|eq, ":liege_is_undeclared_rebel", 1),
					(lt, ":center_relation", 0),
				(val_div, ":weight", 2),
			(else_try), #neutral center
				(val_div, ":weight", 4),
			(try_end),
		
			(val_sub, ":result_for_security", ":weight"),		
		(try_end),
	(try_end),
	
	
	#if a faction controls no other centers, then there is a small bonus
	(try_begin),
		(eq, ":faction_has_base", 0),
		(val_add, ":result_for_security", 20),
		(try_begin),
			(eq, "$cheat_mode", 2),
			(display_message, "str_small_bonus_for_no_base"),
		(try_end),
	(try_end),
	(val_clamp, ":result_for_security", -100, 100),


	(assign, ":result_for_security_weighted", ":result_for_security"),
	##diplomacy start+
   #ADDED TO THIS, SEE BELOW
	#(try_begin),
	#	(eq, ":lord_reputation", lrep_cunning),
	#	(val_mul, ":result_for_security_weighted", 2),
	#(else_try),
	#	(eq, ":lord_reputation", lrep_martial),
	#	(val_div, ":result_for_security_weighted", 2),
	#(try_end),
	#
    ##Use companion morality type "tmt_aristocratic" as a synonym/antonym for bold
	(call_script, "script_dplmc_get_troop_morality_value", ":troop", tmt_aristocratic),
	(assign, ":lord_tmt_aristocratic", reg0),
	(try_begin),
		(lt, ":lord_tmt_aristocratic", 1),
		(this_or_next|lt, ":lord_tmt_aristocratic", 0),
		(eq, ":lord_reputation", lrep_cunning),
		(val_mul, ":result_for_security_weighted", 2),
	(else_try),
		(ge, ":lord_tmt_aristocratic", 0),
		(this_or_next|ge, ":lord_tmt_aristocratic", 1),
		(eq, ":lord_reputation", lrep_martial),
		(val_div, ":result_for_security_weighted", 2),
	(try_end),
	##diplomacy end+

	#FACTOR 2 - INTERNAL FACTION POLITICS
	#this is a calculation of how much influence the lord believes he will have in each faction
	(assign, ":result_for_political", 0),

    (try_for_range, ":loop_var", "trp_kingdom_heroes_including_player_begin", active_npcs_end),
        (assign, ":kingdom_hero", ":loop_var"),
	##diplomacy start+ Skip what follows when there is no liege
	(ge, ":liege", 0),
	##diplomacy end+

		(this_or_next|troop_slot_eq, ":kingdom_hero", slot_troop_occupation, slto_kingdom_hero),
		(this_or_next|eq, ":kingdom_hero", "trp_kingdom_heroes_including_player_begin"),
			(is_between, ":kingdom_hero", pretenders_begin, pretenders_end),

		(store_faction_of_troop, ":kingdom_hero_faction", ":kingdom_hero"),

        (try_begin),
            (eq, ":loop_var", "trp_kingdom_heroes_including_player_begin"),
            (assign, ":kingdom_hero", "trp_player"),
			(assign, ":kingdom_hero_faction", "$players_kingdom"),
			(try_begin), #do not count player relation if the player is trying to suborn the character. this has the slight potential for a miscalculation, if the script is called from outside dialogs and $g_talk_troop has not been reset
				(eq, "$g_talk_troop", ":troop"),
				(store_faction_of_troop, ":cur_faction", ":troop"),
				(eq, ":cur_faction", ":faction"),
				(assign, ":kingdom_hero_faction", 0),
			(try_end),	
		(try_end),
		
		(eq, ":kingdom_hero_faction", ":faction"),
		(neg|faction_slot_eq, ":kingdom_hero_faction", slot_faction_leader, ":kingdom_hero"),
		(neq, ":liege_is_undeclared_rebel", 1),
		(neg|is_between, ":kingdom_hero", pretenders_begin, pretenders_end),
		
						
		(call_script, "script_troop_get_relation_with_troop", ":troop", ":kingdom_hero"),
		(assign, ":troop_rel_w_hero", reg0),

		(call_script, "script_troop_get_relation_with_troop", ":kingdom_hero", ":liege"),
		(assign, ":hero_rel_w_liege", reg0),

		(store_mul, ":lord_political_weight", ":troop_rel_w_hero", ":hero_rel_w_liege"),
		(val_div, ":lord_political_weight", 100),

		(try_begin),
			(eq, "$cheat_mode", 2), #disabled
			(eq, "$g_talk_troop", ":troop"),
			(str_store_faction_name, s20, ":kingdom_hero_faction"),
			(str_store_troop_name, s15, ":kingdom_hero"),
			(assign, reg15, ":lord_political_weight"),
			(display_message, "str_s15_considered_member_of_faction_s20_weight_of_reg15"),
		(try_end),
		
		(val_add, ":result_for_political", ":lord_political_weight"),
	(try_end),			

	(val_clamp, ":result_for_political", -100, 101), #lords portion represents half
	
	(try_begin),
		##diplomacy start+ When there isn't a liege, use 0
		(assign, ":liege_relation", 0),
		(ge, ":liege", 0),
		##diplomacy end+
		(call_script, "script_troop_get_relation_with_troop", ":troop", ":liege"),
		(assign, ":liege_relation", reg0),
		(val_add, ":result_for_political", ":liege_relation"),
	(try_end),

	(val_div, ":result_for_political", 2),
	
	(val_clamp, ":result_for_political", -100, 101), #liege portion represents half
	
	(assign, ":result_for_political_weighted", ":result_for_political"),
	
	(try_begin),
		(this_or_next|eq, ":lord_reputation", lrep_goodnatured),
			(eq, ":lord_reputation", lrep_quarrelsome),
		(val_mul, ":result_for_political_weighted", 2),
	(try_end),

	#FACTOR 3 - PROMISES AND OTHER ANTICIPATED GAINS
	#lord's calculation of anticipated gains
	(assign, ":result_for_material", 0),
	(assign, ":result_for_material_weighted", ":result_for_material"),

	
	#FACTOR 4 - IDEOLOGY
	#lord's calculation of ideological comfort
	(try_begin),
		#Originally, the argument section was not used for a non-player liege. Actually, it can be used
		(eq, 1, 0),
		(neq, ":liege", "trp_player"),
		(neq, ":liege", "$supported_pretender"), #player is advocate for pretender
		(assign, ":argument_strength", 0),
		(assign, ":argument_appeal", 0),
		(assign, ":result_for_argument", 0),
	(else_try),	#only if the recruitment candidate is either the player, or a supported pretender
		(troop_get_slot, ":recruitment_argument", ":troop", slot_lord_recruitment_argument),

		(call_script, "script_rebellion_arguments", ":troop", ":recruitment_argument", ":liege"),
		(assign, ":argument_appeal", reg0),
		(assign, ":argument_strength", reg1),
		
		(store_add, ":result_for_argument", ":argument_appeal", ":argument_strength"),

		(store_skill_level, ":player_persuasion_skill", "skl_persuasion", "trp_player"),
		(try_begin),
			(gt, ":result_for_argument", 0),
			#make sure player is the one making the overture
			
			#if player has 0 persuasion, ":result_for_argument" will be multiplied by 3/10.
			(store_add, ":player_persuasion_skill_plus_5_mul_066", ":player_persuasion_skill", 5),
			(val_mul, ":player_persuasion_skill_plus_5_mul_066", 2),
			(val_div, ":player_persuasion_skill_plus_5_mul_066", 3),
			
			(val_mul, ":result_for_argument", ":player_persuasion_skill_plus_5_mul_066"),
			(val_div, ":result_for_argument", 10),
		(else_try),
			(lt, ":result_for_argument", 0),
			(store_sub, ":ten_minus_player_persuasion_skill", 10, ":player_persuasion_skill"),
			(val_mul, ":result_for_argument", ":ten_minus_player_persuasion_skill"),
			(val_div, ":result_for_argument", 10),
		(try_end),
		
		(try_begin),
			(neq, ":liege", "trp_player"),
			(neq, ":liege", "$supported_pretender"), #player is advocate for pretender
			(val_div, ":argument_strength", 2),
			(val_div, ":argument_appeal", 2),
			(val_div, ":result_for_argument", 2),		
		(try_end),
		
	(try_end),
	
#	(try_begin),
#		(eq, ":lord_reputation", lrep_cunning),
#		(val_div, ":result_for_ideological_weighted", 2),
#	(else_try),
#		(eq, ":lord_reputation", lrep_upstanding),
#		(val_mul, ":result_for_ideological_weighted", 2),
#	(try_end),


	#FACTOR 5 - PENALTY FOR CHANGING SIDES
	(try_begin), #no penalty for the incumbent
		(store_faction_of_troop, ":cur_faction", ":troop"),
		(eq, ":cur_faction", ":faction"),
		(assign, ":penalty_for_changing_sides", 0),
	(else_try), #penalty for the player
		(eq, ":liege", "trp_player"),
		(store_sub, ":penalty_for_changing_sides", 60, "$player_right_to_rule"),
	(else_try), #same culture, such as a pretender
		##diplomacy start+ skip when there is no liege
		(ge, ":liege", 0),
		##diplomacy end+
		(troop_get_slot, ":orig_faction_of_lord", ":troop", slot_troop_original_faction),
		(troop_get_slot, ":orig_faction_of_liege", ":liege", slot_troop_original_faction),
		(eq, ":orig_faction_of_lord", ":orig_faction_of_liege"),
		(assign, ":penalty_for_changing_sides", 10),
	##diplomacy start+
	#"same culture, such as a pretender" pt. 2
	(else_try),
		(troop_slot_eq, ":troop", slot_troop_original_faction, ":faction"),
		(assign, ":penalty_for_changing_sides", 10),	
	##diplomacy end+
	(else_try), #a liege from a different culture
		(assign, ":penalty_for_changing_sides", 50),
	(try_end),
	(val_clamp, ":penalty_for_changing_sides", 0, 101),

	(assign, ":penalty_for_changing_sides_weighted", ":penalty_for_changing_sides"),
	##diplomacy start+
	#(try_begin),
	#	(eq, ":lord_reputation", lrep_debauched),
	#	(val_div, ":penalty_for_changing_sides_weighted", 2),
	#(else_try),
	#	(eq, ":lord_reputation", lrep_upstanding),
	#	(val_mul, ":penalty_for_changing_sides_weighted", 2),
	#(try_end),
	#
	##Use companion morality type "tmt_honest" as a synonym/antonym for deal-keeping
	(call_script, "script_dplmc_get_troop_morality_value", ":troop", tmt_honest),
	(assign, ":lord_tmt_honest", reg0),
	(try_begin),
		(this_or_next|lt, ":lord_tmt_honest", 0),
		(eq, ":lord_reputation", lrep_debauched),
		(val_div, ":penalty_for_changing_sides_weighted", 2),
	(else_try),
		(this_or_next|ge, ":lord_tmt_honest", 1),
		(eq, ":lord_reputation", lrep_upstanding),
		(val_mul, ":penalty_for_changing_sides_weighted", 2),
	(try_end),
	##diplomacy end+

	
	
	(assign, reg1, ":result_for_security"),
	(assign, reg2, ":result_for_security_weighted"),
	(assign, reg3, ":result_for_political"),
	(assign, reg4, ":result_for_political_weighted"),
	(assign, reg5, ":result_for_material"),
	(assign, reg6, ":result_for_material_weighted"),
	(assign, reg7, ":argument_strength"),
	(assign, reg17, ":argument_appeal"),

	(assign, reg8, ":result_for_argument"),
	(assign, reg9, ":penalty_for_changing_sides"),
	(assign, reg10, ":penalty_for_changing_sides_weighted"),

	
	(try_begin),
		(eq, "$cheat_mode", 1),
		(eq, "$g_talk_troop", ":troop"),
		(str_store_troop_name, s20, ":troop"),
		(str_store_faction_name, s21, ":faction"),
		##diplomacy start+
		##OLD:
		#(str_store_troop_name, s22, ":liege"),
		##NEW:
		(try_begin),
		  (gt, ":liege", -1),
		  (str_store_troop_name, s22, ":liege"),
		(else_try),
		  (str_store_string, s22, "str_noone"),
		(try_end),
		##diplomacy end+

		(display_message, "@{!}G_talk_troop {s20} evaluates being vassal to {s22} of {s21}"),

		(display_message, "str_base_result_for_security_reg1"),
		(display_message, "str_result_for_security_weighted_by_personality_reg2"),
		(display_message, "str_base_result_for_political_connections_reg3"),	
		(display_message, "str_result_for_political_connections_weighted_by_personality_reg4"),	
#		(display_message, "@{!}Result for anticipated_gains: {reg5}"),	
#		(display_message, "@{!}Result for anticipated_gains weighted by personality: {reg6}"),	

		(try_begin),
			(this_or_next|eq, ":liege", "trp_player"),
				(eq, ":liege", "$supported_pretender"), #player is advocate for pretender
			(display_message, "str_result_for_argument_strength_reg7"),	
			(display_message, "str_result_for_argument_appeal_reg17"),	
			(display_message, "str_combined_result_for_argument_modified_by_persuasion_reg8"),
		(try_end),			
		(display_message, "str_base_changing_sides_penalty_reg9"),	
		(display_message, "str_changing_sides_penalty_weighted_by_personality_reg10"),	
	(try_end),
		
	(store_add, ":total", ":result_for_security_weighted", ":result_for_political_weighted"),
	(val_add, ":total", ":result_for_material_weighted"),
	(val_add, ":total", ":result_for_argument"),
	(val_sub, ":total", ":penalty_for_changing_sides_weighted"),


	(assign, reg0, ":total"),

	(try_begin),
		(eq, "$cheat_mode", 2),
		(display_message, "@{!}DEBUG -- Analyzing lord allegiances, combined bonuses and penalties = {reg0}"),
		#(display_message, "str_combined_bonuses_and_penalties_=_reg0"),
	(try_end),
	]),
    ("cf_troop_can_intrigue",
	#This script should be called from dialogs, and also prior to any event which might result in a lord changing sides
    [
      (store_script_param, ":troop", 1),
      (store_script_param, ":skip_player_party", 2),

		##diplomacy start+
		#Use this to filter out lords who are supposed to be "off the board"
		(assign, ":bad_occupation", 0),
		(try_begin),
		   (gt, ":troop", 0),
			(troop_is_hero, ":troop"),
		   (troop_slot_eq, ":troop", slot_lord_reputation_type, dplmc_slto_dead),
		   (assign, ":bad_occupation", 1),#altered 2011-06-08
		(try_end),
		(eq, ":bad_occupation", 0),
		##diplomacy end+

      (troop_get_slot, ":led_party_1", ":troop", slot_troop_leaded_party),
      (party_is_active, ":led_party_1"),
      
      (try_begin),
        (eq, "$cheat_mode", 1),
        (eq, ":troop", "$g_talk_troop"),
        (display_message, "str_intrigue_test_troop_party_is_active"),
      (try_end),
      
      (party_get_battle_opponent, ":battle_opponent", ":led_party_1"),
      (le, ":battle_opponent", 0), #battle opponent can be 0 for an attached party?
      
      (try_begin),
        (eq, "$cheat_mode", 1),
        (eq, ":troop", "$g_talk_troop"),
        (display_message, "str_intrigue_test_troop_party_is_not_in_battle"),
      (try_end),
      
      (troop_slot_eq, ":troop", slot_troop_prisoner_of_party, -1),
      
      (try_begin),
        (eq, "$cheat_mode", 1),
        (eq, ":troop", "$g_talk_troop"),
        (display_message, "str_intrigue_test_troop_is_not_prisoner"),
      (try_end),
      
      (party_get_attached_to, ":led_party_1_attached", ":led_party_1"),
      
      (store_faction_of_party, ":led_party_1_faction", ":led_party_1"),
      
      (assign, ":other_lords_nearby", 0),
      (try_for_range, ":troop_2", active_npcs_begin, active_npcs_end),
        (neq, ":troop", ":troop_2"),
        (eq, ":other_lords_nearby", 0),
        
        (troop_slot_eq, ":troop_2", slot_troop_occupation, slto_kingdom_hero),
        
        (troop_get_slot, ":led_party_2", ":troop_2", slot_troop_leaded_party),
        (party_is_active, ":led_party_2"),
        (neq, ":led_party_1", ":led_party_2"),
        
        (store_faction_of_party, ":led_party_2_faction", ":led_party_2"),
        (eq, ":led_party_1_faction", ":led_party_2_faction"),
        
        (try_begin),
          (eq, ":led_party_1_attached", -1),
          (store_distance_to_party_from_party, ":distance", ":led_party_1", ":led_party_2"),
          (lt, ":distance", 3),
          (assign, ":other_lords_nearby", 1),
        (else_try),
          (is_between, ":led_party_1_attached", walled_centers_begin, walled_centers_end),
          (party_get_attached_to, ":led_party_2_attached", ":led_party_2"),
          (eq, ":led_party_1_attached", ":led_party_2_attached"),
          (assign, ":other_lords_nearby", 1),
        (try_end),
      (try_end),
      
      (try_begin),
        (eq, "$cheat_mode", 1),
        (eq, ":troop", "$g_talk_troop"),
        (display_message, "str_intrigue_test_troop_is_nearby"),
      (try_end),
      
      (try_begin),
        (eq, ":skip_player_party", 0),
        #temporary spot
      (try_end),
      
      (eq, ":other_lords_nearby", 0),	
	]),
    ("troop_change_relation_with_troop",
    [
	(store_script_param, ":troop1", 1),
	(store_script_param, ":troop2", 2),
	(store_script_param, ":amount", 3),

	(try_begin),
		(eq, ":troop1", "trp_player"),
		(call_script, "script_change_player_relation_with_troop", ":troop2", ":amount"),
	(else_try),	
		(eq, ":troop2", "trp_player"),
		(call_script, "script_change_player_relation_with_troop", ":troop1", ":amount"),
	(else_try),
		##diplomacy start+ Cancel the result for bad troop values
		(this_or_next|lt, ":troop1", 0),
		(this_or_next|lt, ":troop2", 0),
		##diplomacy end+
		(eq, ":troop1", ":troop2"),
		##diplomacy start+ Do this to avoid the controversy check further below
		(assign, ":amount", 0),
		##diplomacy end+
	(else_try),
		(call_script, "script_troop_get_relation_with_troop", ":troop1", ":troop2"),
		(store_add, ":new_relation", reg0, ":amount"),

		(val_clamp, ":new_relation", -100, 101),

		(try_begin),
			(eq, ":new_relation", 0),
			(assign, ":new_relation", 1), #this removes the need for a separate "met" slot - any non-zero relation will be a met
		(try_end),
		
		(store_add, ":troop1_slot_for_troop2", ":troop2", slot_troop_relations_begin),
		(troop_set_slot, ":troop1", ":troop1_slot_for_troop2", ":new_relation"),
	
		(store_add, ":troop2_slot_for_troop1", ":troop1", slot_troop_relations_begin),
		(troop_set_slot, ":troop2", ":troop2_slot_for_troop1", ":new_relation"),
	(try_end),
	
	
	(try_begin), #generate controversy if troops are in the same faciton
		(lt, ":amount", -5),
		(try_begin),
			(eq, ":troop1", "trp_player"),
			(assign, ":faction1", "$players_kingdom"),
		(else_try),	
			(store_faction_of_troop, ":faction1", ":troop1"),
		(try_end),
		(try_begin),
			(eq, ":troop2", "trp_player"),
			(assign, ":faction2", "$players_kingdom"),
		(else_try),	
			(store_faction_of_troop, ":faction2", ":troop2"),
		(try_end),
		(eq, ":faction1", ":faction2"),
		(is_between, ":faction1", kingdoms_begin, kingdoms_end),
		
		(store_mul, ":controversy_generated", ":amount", -1),
	
		(troop_get_slot, ":controversy1", ":troop1", slot_troop_controversy),
		(val_add, ":controversy1", ":controversy_generated"),
		(val_min, ":controversy1", 100),
		(troop_set_slot, ":troop1", slot_troop_controversy, ":controversy1"),

		(troop_get_slot, ":controversy2", ":troop2", slot_troop_controversy),
		(val_add, ":controversy2", ":controversy_generated"),
		(val_min, ":controversy2", 100),
		(troop_set_slot, ":troop2", slot_troop_controversy, ":controversy2"),
		
	(try_end),
	
	(try_begin),
		##diplomacy start+ Also enable messages for promoted kingdom ladies
		#OLD:
		#(is_between, ":troop1", active_npcs_begin, active_npcs_end),
		#(is_between, ":troop2", active_npcs_begin, active_npcs_end),
		#
		#NEW:
		(is_between, ":troop1", heroes_begin, heroes_end),
		(this_or_next|troop_slot_eq, ":troop1", slot_troop_occupation, slto_kingdom_hero),
			(is_between, ":troop1", active_npcs_begin, active_npcs_end),

		(is_between, ":troop2", heroes_begin, heroes_end),
		(this_or_next|troop_slot_eq, ":troop2", slot_troop_occupation, slto_kingdom_hero),
			(is_between, ":troop2", active_npcs_begin, active_npcs_end),
		##diplomacy end+
		(neq, ":troop1", ":troop2"),

		(try_begin),
			(gt, ":amount", 0),
			(val_add, "$total_relation_adds", ":amount"),
		(else_try),
			(val_sub, "$total_relation_subs", ":amount"),
		(try_end),
	(try_end),
	
	(try_begin),
		(eq, "$cheat_mode", 4), #change back to 4
		##diplomacy start+ Also enable messages for promoted kingdom ladies
		#OLD:
		# (is_between, ":troop1", active_npcs_begin, active_npcs_end),
		# (is_between, ":troop2", active_npcs_begin, active_npcs_end),
		#
		#NEW:
		(is_between, ":troop1", heroes_begin, heroes_end),
		(this_or_next|troop_slot_eq, ":troop1", slot_troop_occupation, slto_kingdom_hero),
			(is_between, ":troop1", active_npcs_begin, active_npcs_end),

		(is_between, ":troop2", heroes_begin, heroes_end),
		(this_or_next|troop_slot_eq, ":troop2", slot_troop_occupation, slto_kingdom_hero),
			(is_between, ":troop2", active_npcs_begin, active_npcs_end),
		##diplomacy end+
		(neq, ":troop1", ":troop2"),

		(str_store_troop_name, s20, ":troop1"),
		(str_store_troop_name, s15, ":troop2"),
		(assign, reg4, ":amount"),
		(assign, reg14, ":new_relation"),
		(display_message, "str_s20_relation_with_s15_changed_by_reg4_to_reg14"),
		
		(assign, reg4, "$total_relation_adds"),
		(display_message, "str_total_additions_reg4"),
		(assign, reg4, "$total_relation_subs"),
		(display_message, "str_total_subtractions_reg4"),
		
		(assign, reg4, "$total_courtship_quarrel_changes"),
		(display_message, "@{!}DEBUG -- Total courtship quarrel changes: {reg4}"),

		(assign, reg4, "$total_random_quarrel_changes"),
		(display_message, "@{!}DEBUG -- Total random quarrel changes: {reg4}"),
		
		(assign, reg4, "$total_battle_ally_changes"),
		(display_message, "@{!}DEBUG -- Total battle changes for allies: {reg4}"),

		(assign, reg4, "$total_battle_enemy_changes"),
		(display_message, "@{!}DEBUG -- Total battle changes for enemies: {reg4}"),

		(assign, reg4, "$total_promotion_changes"),
		(display_message, "@{!}DEBUG -- Total promotion changes: {reg4}"),
		
		(assign, reg4, "$total_feast_changes"),
		(display_message, "@{!}DEBUG -- Total feast changes: {reg4}"),
		
		(assign, reg4, "$total_policy_dispute_changes"),
		(assign, reg5, "$number_of_controversial_policy_decisions"),		
		(display_message, "@{!}DEBUG -- Total policy dispute changes: {reg4} from {reg5} decisions"),

		(assign, reg4, "$total_indictment_changes"),
		(display_message, "@{!}DEBUG -- Total faction switch changes: {reg4}"),

		(assign, reg4, "$total_no_fief_changes"),
		(display_message, "@{!}DEBUG -- Total no fief changes: {reg4}"),

		(assign, reg4, "$total_relation_changes_through_convergence"),
		(display_message, "@{!}DEBUG -- Total changes through convergence: {reg4}"),
		
		(assign, reg4, "$total_vassal_days_responding_to_campaign"),
		(display_message, "@{!}DEBUG -- Total vassal responses to campaign: {reg4}"),
		
		(assign, reg4, "$total_vassal_days_on_campaign"),
		(display_message, "@{!}DEBUG -- Total vassal campaign days: {reg4}"),
		
		(val_max, "$total_vassal_days_on_campaign", 1),
		(store_mul, ":response_rate", "$total_vassal_days_responding_to_campaign", 100),
		(val_div, ":response_rate", "$total_vassal_days_on_campaign"),
		(assign, reg4, ":response_rate"),
		(display_message, "@{!}DEBUG -- Vassal response rate: {reg4}"),
		
		
		
#		(assign, reg4, "$total_joy_battle_changes"),
#		(display_message, "@{!}DEBUG -- Total joy of battle changes"),
		
	(try_end),

	]),
    ("troop_get_relation_with_troop",
    [
	(store_script_param, ":troop1", 1),
	(store_script_param, ":troop2", 2),

	(assign, ":relation", 0),
	(try_begin),
		##diplomacy start+
		#Change "eq -1", to "lt 0"
		(this_or_next|lt, ":troop1", 0),
			(lt, ":troop2", 0),
		##diplomacy end+

		#Possibly switch to relation with liege
		(assign, ":relation", 0),
	(else_try),
		(eq, ":troop1", "trp_player"),
		(call_script, "script_troop_get_player_relation", ":troop2"),
		(assign, ":relation", reg0),
	(else_try),
		(eq, ":troop2", "trp_player"),
		(call_script, "script_troop_get_player_relation", ":troop1"),
		(assign, ":relation", reg0),
	(else_try),
		(store_add, ":troop1_slot_for_troop2", ":troop2", slot_troop_relations_begin),
		(troop_get_slot, ":relation", ":troop1", ":troop1_slot_for_troop2"),
	(try_end),
	
	
	(val_clamp, ":relation", -100, 101),
	(assign, reg0, ":relation"),
	
	]),
	("appoint_faction_marshall",
    [
	(store_script_param, ":faction_no", 1),
	(store_script_param, ":faction_marshall", 2),


    (faction_get_slot, ":faction_leader", ":faction_no", slot_faction_leader),
    (faction_get_slot, ":old_marshall", ":faction_no", slot_faction_marshall),

    (faction_set_slot, ":faction_no", slot_faction_marshall, ":faction_marshall"),
    
    (try_begin),
		(ge, ":old_marshall", 0),
		(troop_get_slot, ":old_marshall_party", ":old_marshall", slot_troop_leaded_party),
        (party_is_active, ":old_marshall_party"),
        (party_set_marshall, ":old_marshall_party", 0),
    (try_end),  

    
    (try_begin),
      (ge, ":faction_marshall", 0),
	  (troop_get_slot, ":new_marshall_party", ":faction_marshall", slot_troop_leaded_party),
      (party_is_active, ":new_marshall_party"),
      (party_set_marshall,":new_marshall_party", 1),
    (try_end),  
	
	
	(try_begin),
		(neq, ":faction_marshall", ":faction_leader"),
		(neq, ":faction_marshall", ":old_marshall"),
		##diplomacy start+ Support promoted kingdom ladies
		(this_or_next|eq, ":faction_marshall", "trp_player"),
			(is_between, ":faction_marshall", heroes_begin, heroes_end),
		(this_or_next|troop_slot_eq, ":faction_marshall", slot_troop_occupation, slto_kingdom_hero),
		##diplomacy end+
		(this_or_next|eq, ":faction_marshall", "trp_player"),
			(is_between, ":faction_marshall", active_npcs_begin, active_npcs_end),
		
		(this_or_next|neq, ":faction_no", "fac_player_supporters_faction"),
			(neg|check_quest_active, "qst_rebel_against_kingdom"),
		
		(try_begin),
			(eq, "$cheat_mode", 1),
			(str_store_faction_name, s15, ":faction_no"),
			(display_message, "str_checking_lord_reactions_in_s15"),
		(try_end),

		
		(call_script, "script_troop_change_relation_with_troop", ":faction_marshall", ":faction_leader", 5),
		(val_add, "$total_promotion_changes", 5),

		##diplomacy start+
		(call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", ":faction_no"),
		(assign, ":player_standing_in_faction", reg0),
		#(ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),

		#Support promoted kingdom ladies
		##OLD:
		#(try_for_range, ":lord", active_npcs_begin, active_npcs_end),
		##NEW:
		(try_for_range, ":lord", heroes_begin, heroes_end),
		##diplomacy end+
			(troop_slot_eq, ":lord", slot_troop_occupation, slto_kingdom_hero),
			(store_faction_of_troop, ":lord_faction", ":lord"),
			(eq, ":lord_faction", ":faction_no"),

			(neq, ":lord", ":faction_marshall"),
			(neq, ":lord", ":faction_leader"),

			(call_script, "script_troop_get_relation_with_troop", ":faction_marshall", ":lord"),
#			(try_begin),
#				(eq, "$cheat_mode", 1),
#				(str_store_troop_name, s14, ":lord"),
#				(str_store_troop_name, s17, ":faction_marshall"),
#				(display_message, "@{!}{s14}'s relation with {s17} is {reg0}"),
#			(try_end),
			(store_sub, ":adjust_relations", reg0, 10),
			(val_div, ":adjust_relations", 15),
			##diplomacy start+
			#In some situtations the player can set the marshall freely even though he isn't the faction leader.
			(try_begin),
				(eq, ":faction_marshall", "trp_player"),
				(ge, ":player_standing_in_faction", DPLMC_FACTION_STANDING_LEADER_SPOUSE),
				#Still allow a relation gain below if the lord had actively supported the player
				#(which doesn't happen now if the player is the ruler, but could).
				(val_min, ":adjust_relations", 0),
			(try_end),
			##diplomacy end+
			(neq, ":adjust_relations", 0),

			#Not negatively affected if they favored the lord
			(try_begin),
				(troop_slot_eq, ":lord", slot_troop_stance_on_faction_issue, ":faction_marshall"),
				(val_add, ":adjust_relations", 1),
				(val_max, ":adjust_relations", 0),
			(try_end),

			(call_script, "script_troop_change_relation_with_troop", ":faction_leader", ":lord", ":adjust_relations"),
			(val_add, "$total_promotion_changes", ":adjust_relations"),
			
			(lt, ":adjust_relations", -2),
			(store_random_in_range, ":random", 1, 10),
			
			(val_add, ":adjust_relations", ":random"),
			
			(lt, ":adjust_relations", 0),
			
			(str_store_troop_name, s14, ":lord"),
			(str_store_troop_name, s15, ":faction_marshall"),

			(try_begin),
			##diplomacy start+ Show protest information for your own kingdom if you have a chancellor or are the ruler
				(ge, ":player_standing_in_faction", DPLMC_FACTION_STANDING_MEMBER),
				(this_or_next|ge, ":player_standing_in_faction", DPLMC_FACTION_STANDING_LEADER_SPOUSE),#<- via the minister, or just hearing about it
					(gt, "$g_player_chancellor", 0),#<- via your chancellor
				(neg|troop_slot_eq, ":lord", slot_troop_met, 0),
				(display_message, "str_s14_protests_the_appointment_of_s15_as_marshall"),
			(else_try),
				(call_script, "script_dplmc_store_troop_is_eligible_for_affiliate_messages", ":lord"),
				(this_or_next|gt, reg0, 0),
			##diplomacy end+
                (eq, "$cheat_mode", 1),
                (display_message, "str_s14_protests_the_appointment_of_s15_as_marshall"),
            (try_end),

			(call_script, "script_troop_change_relation_with_troop", ":faction_leader", ":lord", -10),
			(call_script, "script_troop_change_relation_with_troop", ":faction_marshall", ":lord", -5),
			(val_add, "$total_promotion_changes", -15),
			
			(call_script, "script_add_log_entry", logent_lord_protests_marshall_appointment, ":lord",  ":faction_marshall", ":faction_leader", "$g_encountered_party_faction"),

		(try_end),
	(try_end),
	
		]),
	("locate_player_minister", #maybe deprecate this
    [
	##diplomacy start+ Handle player is co-ruler of NPC faction
	(assign, ":alt_faction", "fac_player_supporters_faction"),
	(try_begin),
		(is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
		(call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", "$players_kingdom"),
		(ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
		(assign, ":alt_faction", "$players_kingdom"),
	(try_end),
	##diplomacy end+
	(assign, ":walled_center_found", 0),
	(try_for_range, ":walled_center", walled_centers_begin, walled_centers_end),
		(lt, ":walled_center_found", centers_begin),
		(store_faction_of_party, ":walled_center_faction", ":walled_center"),
		##diplomacy start+
		(this_or_next|eq, ":walled_center_faction", ":alt_faction"),
		##diplomacy end+
		(eq, ":walled_center_faction", "fac_player_supporters_faction"),
		(neg|party_slot_ge, ":walled_center", slot_town_lord, active_npcs_begin), #ie, player or a reserved slot
		(assign, ":walled_center_found", ":walled_center"),
	(try_end),

	(troop_get_slot, ":old_location", "$g_player_minister", slot_troop_cur_center),
	(troop_set_slot, "$g_player_minister", slot_troop_cur_center, ":walled_center_found"),
	
	(try_begin),
		(neq, ":old_location", ":walled_center"),
		(str_store_party_name, s10, ":walled_center"),
		(str_store_troop_name, s11, "$g_player_minister"),
		(display_message, "str_s11_relocates_to_s10"),
	(try_end),
	
	]),
	("lord_get_home_center",
	[
      (store_script_param, ":troop_no", 1),
      (assign, ":result", -1),

	  ##diplomacy start+
	  (assign, ":best_score", -1),
	  (troop_get_slot, ":troop_original_faction", ":troop_no", slot_troop_original_faction),
	  #The default script prefers towns to castles, but aside from that is
	  #fairly arbitrary.  Add scores that take into account original faction
	  #and so forth.
      (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
        (party_slot_eq, ":center_no", slot_town_lord, ":troop_no"),
		  (assign, ":center_score", 10),#10 for castles, 20 for towns
		  (try_begin),
		     (is_between, ":center_no", towns_begin, towns_end),
			  (assign, ":center_score", 20),
		  (try_end),
		  (try_begin),
		     (troop_slot_eq, ":troop_no", slot_troop_home, ":center_no"),
			  (val_add, ":center_score", 6),
		  (else_try),
			  (party_slot_eq, ":center_no", dplmc_slot_center_original_lord, ":troop_no"),
			  (val_add, ":center_score", 5),
		  (else_try),
		     (is_between, ":troop_original_faction", kingdoms_begin, kingdoms_end),
			  (party_slot_eq, ":center_no", slot_center_original_faction, ":troop_original_faction"),
			  (val_add, ":center_score", 4),
		  (try_end),
		  (gt, ":center_score", ":best_score"),
        (assign, ":result", ":center_no"),
		  (assign, ":best_score", ":center_score"),
      (try_end),
		##diplomacy end+

      (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
        (eq, ":result", -1),
        (party_slot_eq, ":center_no", slot_town_lord, ":troop_no"),
        (assign, ":result", ":center_no"),
      (try_end),

      #NOTE : In old code if a lord has no walled center then home city of this lord is assigning to
      #faction leader's home city. Now I changed this to assign home cities more logical and homogeneous.
      #In new code if a lord has no walled center then his home city becomes his village's border_city.
      #This means his home city becomes owner city of his village. If he has no village then as last change
      #his home city become faction leader's home city.
      (try_begin),
        (eq, ":result", -1),
        (try_for_range, ":center_no", centers_begin, centers_end),
          (eq, ":result", -1),
          (party_slot_eq, ":center_no", slot_town_lord, ":troop_no"),
          
          (try_begin),
            (neg|is_between, ":center_no", walled_centers_begin, walled_centers_end),
            (party_get_slot, ":bound_center", ":center_no", slot_village_bound_center),            
            (assign, ":result", ":bound_center"),
          (try_end),
        (try_end),      
      (try_end),

      #If lord has no walled center and is player faction, then assign player court
      (try_begin),
        (eq, ":result", -1),
        (store_faction_of_troop, ":faction_no", ":troop_no"),
        (eq, ":faction_no", "fac_player_supporters_faction"),
		(is_between, "$g_player_court", walled_centers_begin, walled_centers_end),
		(store_faction_of_party, ":player_court_faction", "$g_player_court"),
		(eq, ":player_court_faction", "fac_player_supporters_faction"),
		
        (assign, ":result", "$g_player_court"),
      (try_end),
      
      #If lord has no walled center and any not walled village then assign faction capital
      (try_begin),
        (eq, ":result", -1),
        (store_faction_of_troop, ":faction_no", ":troop_no"),
        (faction_get_slot, ":faction_leader", ":faction_no", slot_faction_leader),
        (neq, ":troop_no", ":faction_leader"),
		#gekokujo 3.0 ARGH lord_get_home_center_error fix
		(ge, ":faction_leader", 0),#<- Fix for ticket 36.
        (call_script, "script_lord_get_home_center", ":faction_leader"),
        (gt, reg0, -1),
        (assign, ":result", reg0),
      (try_end),
      
	  #Any center of the faction
      (try_begin),
        (eq, ":result", -1),
		(store_faction_of_troop, ":faction_no", ":troop_no"),
		
		(try_for_range, ":walled_center", walled_centers_begin, walled_centers_end),
		    (eq, ":result", -1),

			(store_faction_of_party, ":center_faction", ":walled_center"),
			(eq, ":faction_no", ":center_faction"),
			(assign, ":result", ":walled_center"),
		(try_end),
      (try_end),
	  
	  
	  
      (assign, reg0, ":result"),	
	]),
	("get_kingdom_lady_social_determinants", #Calradian society is rather patriarchal, at least among the upper classes
    [
	(store_script_param, ":kingdom_lady", 1),
	
	(store_faction_of_troop, ":faction_of_lady", ":kingdom_lady"),
	(assign, ":center", -1),
	(assign, ":closest_male_relative", -1),
	(assign, ":best_center_score", 0),
	
	##diplomacy start+
	##TODO: Re-implement, disabled for now.  "Don't get stuck attached to a MIA relative"
	(try_begin),
		(troop_slot_ge, ":kingdom_lady", slot_troop_spouse, 0),
		(troop_get_slot, ":closest_male_relative", ":kingdom_lady", slot_troop_spouse),
		#gekokujo 3.0 patriarch start
		(troop_slot_eq, ":closest_male_relative", slot_troop_occupation, slto_kingdom_hero),
		#gekokujo 3.0 patriarch end
		#(neg|troop_slot_ge, ":closest_male_relative", slot_troop_occupation, slto_retirement),#added: has not been removed from play
	(else_try),
		(troop_slot_ge, ":kingdom_lady", slot_troop_father, 0),
		(troop_get_slot, ":closest_male_relative", ":kingdom_lady", slot_troop_father),
		#gekokujo 3.0 patriarch start
		(troop_slot_eq, ":closest_male_relative", slot_troop_occupation, slto_kingdom_hero),
		#gekokujo 3.0 patriarch end
		#(neg|troop_slot_ge, ":closest_male_relative", slot_troop_occupation, slto_retirement),#added: has not been removed from play
	(else_try),
		#added
		(troop_slot_ge, ":kingdom_lady", slot_troop_mother, 0),
		(troop_get_slot, ":closest_male_relative", ":kingdom_lady", slot_troop_mother),
		(troop_slot_eq, ":closest_male_relative", slot_troop_occupation, slto_kingdom_hero),
	(else_try),
		(troop_slot_ge, ":kingdom_lady", slot_troop_guardian, 0),
		(troop_get_slot, ":closest_male_relative", ":kingdom_lady", slot_troop_guardian),
		#(neg|troop_slot_ge, ":closest_male_relative", slot_troop_occupation, slto_retirement),#added: has not been removed from play
	(try_end),
	##diplomacy end+

	##diplomacy start+
    #Avoid strange problems if the argument is not a kingdom lady.
	(try_begin),
		(this_or_next|is_between, ":kingdom_lady", kingdom_ladies_begin, kingdom_ladies_end),
			(troop_slot_eq, ":kingdom_lady", slot_troop_occupation, slto_kingdom_lady),
		(neg|troop_slot_eq, ":kingdom_lady", slot_troop_occupation, slto_kingdom_hero),
		(assign, ":is_lady", 1),
	(else_try),
		(assign, ":is_lady", 0),
		(assign, ":closest_male_relative", ":kingdom_lady"),# is doing this useful for the way this script is used, or should we just set it to -1?
	(try_end),

	##OLD:
	#(try_begin), #if ongoing social event (maybe add if not besieged)
	##NEW:
	(try_begin),
		(eq, ":is_lady", 0),
		(call_script, "script_lord_get_home_center", ":kingdom_lady"),
		(assign, ":center", reg0),
		(is_between, ":center", walled_centers_begin, walled_centers_end),
	(else_try), #if ongoing social event (maybe add if not besieged)
	##diplomacy end+
		(faction_slot_eq, ":faction_of_lady", slot_faction_ai_state, sfai_feast),
		(faction_get_slot, ":feast_center", ":faction_of_lady", slot_faction_ai_object),

		(gt, ":closest_male_relative", -1),
		(troop_get_slot, ":closest_male_party", ":closest_male_relative", slot_troop_leaded_party),
		(party_is_active, ":closest_male_party"),
		(party_get_attached_to, ":closest_male_cur_location", ":closest_male_party"),
		
		(eq, ":closest_male_cur_location", ":feast_center"),
		(is_between, ":feast_center", walled_centers_begin, walled_centers_end),
		
		(assign, ":center", ":feast_center"),
		
	(else_try),
		(troop_slot_eq, "trp_player", slot_troop_spouse, ":kingdom_lady"),
		###diplomacy begin
    (try_begin),
    ##diplomacy end
		(is_between, "$g_player_court", walled_centers_begin, walled_centers_end),
		(assign, ":center", "$g_player_court"),
		##diplomacy begin
    (else_try),
      (troop_get_slot, ":cur_residence", ":kingdom_lady", slot_troop_cur_center),
      (is_between, ":cur_residence", walled_centers_begin, walled_centers_end),
      (party_slot_eq, ":cur_residence", slot_town_lord, "trp_player"),
      (assign, ":center", ":cur_residence"),
    (try_end),
    (is_between, ":center",  walled_centers_begin, walled_centers_end),
    ##diplomacy end		
	(else_try),
		(try_for_range, ":walled_center", walled_centers_begin, walled_centers_end),
			(store_faction_of_party, ":walled_center_faction", ":walled_center"),
			(this_or_next|eq, ":faction_of_lady", ":walled_center_faction"),
				(neg|is_between, ":faction_of_lady", kingdoms_begin, kingdoms_end), #lady married to a player without a faction
				
			(party_get_slot, ":castle_lord", ":walled_center", slot_town_lord),
		
			(gt, ":castle_lord", -1),
			
			(call_script, "script_troop_get_family_relation_to_troop", ":kingdom_lady", ":castle_lord"),
			##diplomacy start+
			(try_begin),
				(eq, ":is_lady", 0),
				(eq, ":castle_lord", ":kingdom_lady"),
				(val_max, reg0, 16),
			(try_end),
			##diplomacy end+

			(try_begin),
				(this_or_next|is_between, ":faction_of_lady", kingdoms_begin, kingdoms_end),
					(troop_slot_eq, "trp_player", slot_troop_spouse, ":kingdom_lady"),
					
				(faction_slot_eq, ":faction_of_lady", slot_faction_leader, ":castle_lord"),
				(val_max, reg0, 1),
			(try_end),
			
			(try_begin),
				(eq, "$cheat_mode", 2),
				(str_store_troop_name, s3, ":kingdom_lady"),
				(str_store_troop_name, s4, ":castle_lord"),
				(str_store_party_name, s5, ":walled_center"),
				(display_message, "str_checking_s3_at_s5_with_s11_relationship_with_s4_score_reg0"),
				(str_clear, s11),
			(try_end),

			(gt, reg0, ":best_center_score"),
		
			(assign, ":best_center_score", reg0),
			(assign, ":center", ":walled_center"),
			
			
	    (try_end),
	(try_end),

	(assign, reg0, ":closest_male_relative"),
	(assign, reg1, ":center"),
	
	
	]),
	#This is probably unnecessarily complicated, but can support a multi-generational mod
	("age_troop_one_year",
    [
	(store_script_param, ":troop_no", 1),
    ##diplomacy start+ use gender script
	#(troop_get_type, ":is_female", ":troop_no"),
	(assign, ":save_reg0", reg0),
	(call_script, "script_dplmc_store_troop_is_female", ":troop_no"),
	(assign, ":is_female", reg0),
	(assign, reg0, ":save_reg0"),
	##diplomacy end+

	(troop_get_slot, ":age", ":troop_no", slot_troop_age),
	(troop_get_slot, ":appearance", ":troop_no", slot_troop_age_appearance),
	
	(val_add, ":age", 1),
	(store_random_in_range, ":addition", 1, 5),

	(try_begin),
		(eq, ":is_female", 1),
#		(val_add, ":addition", 2), #the women's age slider seems to produce less change than the male one - commented out: makes women look too old.
	(try_end),
	
	(val_add, ":appearance", ":addition"),
	(try_begin),
		(gt, ":age", 45),
		(store_attribute_level, ":strength", ":troop_no", ca_strength),
		(store_attribute_level, ":agility", ":troop_no", ca_agility),
		(store_random_in_range, ":random", 0, 50), #2% loss brings it down to about 36% by age 90, but of course can be counteracted by new level gain
		(try_begin),
			(lt, ":random", ":strength"),
			(troop_raise_attribute, ":troop_no", ca_strength, -1),
		(try_end),
		(try_begin),
			(lt, ":random", ":agility"),
			(troop_raise_attribute, ":troop_no", ca_agility, -1),
		(try_end),
	(try_end),

	(val_clamp, ":appearance", 1, 100),
	
	(troop_set_slot, ":troop_no", slot_troop_age, ":age"), 
	(troop_set_slot, ":troop_no", slot_troop_age_appearance, ":appearance"), 
	(troop_set_age, ":troop_no", ":appearance"),
	]),
	#gekokujo 3.0 add_lady_items is long deprecated start
	("add_lady_items",
	[
	(store_script_param, ":lady_no", 1),
	(troop_equip_items, ":lady_no"),
	
	(store_faction_of_troop, ":faction_no", ":lady_no"),
	
	(store_random_in_range, ":random", 0, 6),
	
	(try_begin), #assign clothes
		(this_or_next|troop_slot_eq, ":lady_no", slot_lord_reputation_type, lrep_adventurous),
			(troop_slot_eq, ":lady_no", slot_lord_reputation_type, lrep_ambitious),
	
		(this_or_next|troop_slot_eq, ":lady_no", slot_lord_reputation_type, lrep_adventurous),
			(lt, ":random", 2),
			
		(neg|troop_slot_ge, ":lady_no", slot_troop_age, 40),
		(try_begin),
			(eq, ":faction_no", "fac_kingdom_2"),
			(lt, ":random", 4),
			(troop_add_item, ":lady_no", "itm_gekokujo_kimono_3_1", 0),
		(else_try),
			(eq, ":faction_no", "fac_kingdom_3"),
			(lt, ":random", 3),
			(troop_add_item, ":lady_no", "itm_gekokujo_kimono_3_2", 0),
		(else_try),	
			(troop_add_item, ":lady_no", "itm_gekokujo_kimono_3_3", 0),
		(try_end),
	(else_try),
		(eq, ":faction_no", "fac_kingdom_1"),
		(try_begin),
			(lt, ":random", 2),
#			(troop_add_item, ":lady_no", "itm_lady_dress_ruby", 0),
		(else_try),
			(lt, ":random", 4),
#			(troop_add_item, ":lady_no", "itm_lady_dress_green", 0),
		(else_try),
#			(troop_add_item, ":lady_no", "itm_lady_dress_blue", 0),
		(try_end),
	(else_try),
		(eq, ":faction_no", "fac_kingdom_2"),
		(try_begin),
			(eq, ":random", 0),
#			(troop_add_item, ":lady_no", "itm_blue_dress", 0),
		(else_try),
			(eq, ":random", 1),
#			(troop_add_item, ":lady_no", "itm_lady_dress_green", 0),
		(else_try),
			(eq, ":random", 2),
#			(troop_add_item, ":lady_no", "itm_lady_dress_blue", 0),
		(else_try),
			(lt, ":random", 5),
			(neg|troop_slot_eq, ":lady_no", slot_lord_reputation_type, lrep_conventional),
			(neg|troop_slot_eq, ":lady_no", slot_lord_reputation_type, lrep_ambitious),
#			(troop_add_item, ":lady_no", "itm_peasant_dress", 0),
		(else_try),
			(lt, ":random", 5),
#			(troop_add_item, ":lady_no", "itm_lady_dress_ruby", 0),
		(else_try),
#			(troop_add_item, ":lady_no", "itm_court_dress", 0),
		(try_end),
	
	(else_try),
		(eq, ":faction_no", "fac_kingdom_3"),
#		(troop_add_item, ":lady_no", "itm_khergit_lady_dress", 0),
	
	(else_try),
		(eq, ":faction_no", "fac_kingdom_4"),

	(else_try),
		(eq, ":faction_no", "fac_kingdom_5"),

		
	(try_end),
	(troop_equip_items, ":lady_no"),

	#also available:
	#itm_blue_dress
	#itm_court_dress	
	
	#to add for khergits -- salwar/shalvar?
	#western tang costume (p105, china's golden age)
	#kipchak woman from russia book
	
	(try_begin), #assign headguear matched to item
		(this_or_next|troop_has_item_equipped, ":lady_no", "itm_gekokujo_kimono_3_1"),
		(this_or_next|troop_has_item_equipped, ":lady_no", "itm_gekokujo_kimono_3_2"),
			(troop_has_item_equipped, ":lady_no", "itm_gekokujo_kimono_3_3"),
		
		#assign no headgear
	(else_try),
		(this_or_next|troop_slot_eq, ":lady_no", slot_lord_reputation_type, lrep_moralist),
		(this_or_next|troop_slot_eq, ":lady_no", slot_lord_reputation_type, lrep_conventional),
			(lt, ":random", 2),
			
		
		(try_begin),
			(troop_has_item_equipped, ":lady_no", "itm_gekokujo_kimono_3_1"),
#			(troop_add_item, ":lady_no", "itm_khergit_lady_hat", 0),
		
		(else_try),
			(troop_has_item_equipped, ":lady_no", "itm_gekokujo_kimono_3_2"),
#			(troop_add_item, ":lady_no", "itm_turret_hat_ruby", 0),

			(str_store_troop_name, s4, ":lady_no"),
#			(display_message, "@Giving ruby turret hat to {s4}"),
		(else_try),
			(troop_has_item_equipped, ":lady_no", "itm_gekokujo_kimono_3_3"),
#			(troop_add_item, ":lady_no", "itm_turret_hat_blue", 0),
		
			(str_store_troop_name, s4, ":lady_no"),
#			(display_message, "@Giving blue turret hat to {s4}"),
		(else_try),
			(troop_has_item_equipped, ":lady_no", "itm_gekokujo_kimono_3_1"),
#			(troop_add_item, ":lady_no", "itm_turret_hat_green", 0),
		
			(str_store_troop_name, s4, ":lady_no"),
#			(display_message, "@Giving green turret hat to {s4}"),
		(else_try),	
			(troop_has_item_equipped, ":lady_no", "itm_gekokujo_kimono_3_2"),
#			(troop_add_item, ":lady_no", "itm_wimple_with_veil", 0),

			(str_store_troop_name, s4, ":lady_no"),
#			(display_message, "@Giving green-lined wimple to {s4}"),
		(else_try),
			(neq, ":faction_no", "fac_kingdom_3"),
			(neq, ":faction_no", "fac_kingdom_6"),
#			(troop_add_item, ":lady_no", "itm_wimple_a", 0),

			(str_store_troop_name, s4, ":lady_no"),
#			(display_message, "@Giving red-lined wimple to {s4}"),
		(else_try),
			(eq, ":faction_no", "fac_kingdom_6"),
			(try_begin),
				(troop_has_item_equipped, ":lady_no", "itm_gekokujo_kimono_3_3"),
#				(troop_add_item, ":lady_no", "itm_sarranid_head_cloth", 0),
			(else_try),
#				(troop_add_item, ":lady_no", "itm_sarranid_head_cloth_b", 0),
			(try_end),
		(try_end),
	(try_end),
	(troop_equip_items, ":lady_no"),
	##diplomacy start+
	##Save personal items of kingdom ladies
	(call_script, "script_dplmc_save_civilian_clothing", ":lady_no"),
	##diplomacy end+	
	]
	),
	("init_troop_age",
	[
	(store_script_param, ":troop_no", 1),
	(store_script_param, ":age", 2), #minimum 20
	#gekokujo 3.0 new minimum age 18
	
	(try_begin),
		(gt, ":age", 18),
		(troop_set_slot, ":troop_no", slot_troop_age, 18),
	(else_try),
		(troop_set_slot, ":troop_no", slot_troop_age, ":age"),
	(try_end),
	
	(store_sub, ":years_to_age", ":age", 18),
    (troop_set_age, ":troop_no", 0),
	
	(try_begin),
		(gt, ":years_to_age", 0),
		(try_for_range, ":unused", 0, ":years_to_age"),
			(call_script, "script_age_troop_one_year", ":troop_no"),
		(try_end),
	(try_end),	
		
	]),
	("assign_troop_love_interests", #Called at the beginning, or whenever a lord is spurned
    [
	(store_script_param, ":cur_troop", 1),
    ##diplomacy start+
	#wrap the entire thing in a try-statement: do nothing when called erroneously
	(assign, ":save_reg0", reg0),
	(assign, ":save_reg1", reg1),
	(try_begin),
	(this_or_next|is_between, ":cur_troop", lords_begin, lords_end),
	#gekokujo 3.0 microfactions! include fort companions start
	#(this_or_next|is_between, ":cur_troop", companions_begin, companions_end),
	(this_or_next|is_between, ":cur_troop", companions_begin, fort_companions_end),
	#gekokujo 3.0 microfactions! include fort companions end
	(troop_slot_eq, ":cur_troop", slot_troop_occupation, slto_kingdom_hero),#kingdom heroes only
	(troop_slot_eq, ":cur_troop", slot_troop_spouse, -1),#not married, engaged
	(troop_slot_eq, ":cur_troop", slot_troop_betrothed, -1),

	#avoid unintentional erroneous pairings (intentional exceptions can be added)
	#(troop_get_type, ":troop_type", ":cur_troop"),
	(call_script, "script_dplmc_store_troop_is_female", ":cur_troop"),
	(assign, ":troop_type", reg0),

	(try_begin),
	    #Certain personality types don't care about flouting convention.
		(this_or_next|troop_slot_eq, ":cur_troop", slot_lord_reputation_type, lrep_debauched),
        (this_or_next|troop_slot_eq, ":cur_troop", slot_lord_reputation_type, lrep_roguish),
        (troop_slot_eq, ":cur_troop", slot_lord_reputation_type, lrep_adventurous),
		(assign, ":troop_type", abs(tf_male) + abs(tf_female) + 1),#guaranteed not to equal tf_male or tf_female
	(try_end),
	(store_faction_of_troop, ":troop_faction", ":cur_troop"),
	#assign default initial courtships for companions
	(try_begin),
		#gekokujo 3.0 microfactions! include fort companions start
		#(is_between, ":cur_troop", companions_begin, companions_end),
		(is_between, ":cur_troop", companions_begin, fort_companions_end),
		#gekokujo 3.0 microfactions! include fort companions end
        (troop_get_slot, ":cur_lady", ":cur_troop", slot_troop_personalitymatch_object),
        (is_between, ":cur_lady", heroes_begin, heroes_end),

		(store_faction_of_troop, ":lady_faction", ":cur_lady"),
		(eq, ":troop_faction", ":lady_faction"),
		#(call_script, "script_troop_get_family_relation_to_troop", ":cur_troop", ":cur_lady"),
		(call_script, "script_dplmc_troop_get_family_relation_to_troop", ":cur_troop", ":cur_lady"),
		(lt, reg0, 2),#check not a close relative
        #(troop_get_type, reg0, ":cur_lady"),
		(call_script, "script_dplmc_store_troop_is_female", ":cur_lady"),
        (neq, ":troop_type", reg0),#check gender compatability
		(neq, ":cur_lady", ":cur_troop"),#check not yourself
		(neg|troop_slot_ge, ":cur_lady", slot_troop_occupation, slto_retirement),#check in the game and not retired, exiled, dead, etc.
		(troop_slot_ge, ":cur_lady", slot_troop_occupation, slto_kingdom_hero),
		(call_script, "script_troop_get_relation_with_troop", ":cur_troop", ":cur_lady"),
		(ge, reg0, 0), #do not develop love interest if already spurned (but DO allow re-courting)

		(neg|troop_slot_eq, ":cur_troop", slot_troop_love_interest_1, ":cur_lady"),
		(neg|troop_slot_eq, ":cur_troop", slot_troop_love_interest_2, ":cur_lady"),
		(neg|troop_slot_eq, ":cur_troop", slot_troop_love_interest_3, ":cur_lady"),
		(try_begin),
		    (this_or_next|troop_slot_eq, ":cur_troop", slot_troop_love_interest_1, -1),
			(troop_slot_eq, ":cur_troop", slot_troop_love_interest_1, 0),
			(troop_set_slot, ":cur_troop", slot_troop_love_interest_1, ":cur_lady"),
		(else_try),
		    (this_or_next|troop_slot_eq, ":cur_troop", slot_troop_love_interest_2, -1),
			(troop_slot_eq, ":cur_troop", slot_troop_love_interest_2, 0),
			(troop_set_slot, ":cur_troop", slot_troop_love_interest_2, ":cur_lady"),
		(else_try),
		    (this_or_next|troop_slot_eq, ":cur_troop", slot_troop_love_interest_3, -1),
			(troop_slot_eq, ":cur_troop", slot_troop_love_interest_3, 0),
			(troop_set_slot, ":cur_troop", slot_troop_love_interest_3, ":cur_lady"),
		(try_end),
    (try_end),
    ##diplomacy end+
	(try_for_range, ":unused", 0, 50),
		(store_random_in_range, ":cur_lady", kingdom_ladies_begin, kingdom_ladies_end),
		(troop_slot_eq, ":cur_lady", slot_troop_spouse, -1),
		(store_faction_of_troop, ":lady_faction", ":cur_lady"),
		(eq, ":troop_faction", ":lady_faction"),
		##diplomacy start+
		##(call_script, "script_troop_get_family_relation_to_troop", ":cur_troop", ":cur_lady"),
        (call_script, "script_dplmc_troop_get_family_relation_to_troop", ":cur_troop", ":cur_lady"),
		#(eq, reg0, 0),
		#right now nothing gives a value of 1, but change this check in case more distant relations are reported
		(lt, reg0, 2),#check not a close relative
		#(troop_get_type, reg0, ":cur_lady"),
		(call_script, "script_dplmc_store_troop_is_female", ":cur_lady"),
        (neq, ":troop_type", reg0),#check gender compatability
		(neq, ":cur_lady", ":cur_troop"),#check not yourself
		(neg|troop_slot_ge, ":cur_lady", slot_troop_occupation, slto_retirement),#check in the game and not retired, exiled, dead, etc.
		(troop_slot_ge, ":cur_lady", slot_troop_occupation, slto_kingdom_hero),
        ##diplomacy end+
		(call_script, "script_troop_get_relation_with_troop", ":cur_troop", ":cur_lady"),

		(eq, reg0, 0), #do not develop love interest if already spurned or courted

		(neg|troop_slot_eq, ":cur_troop", slot_troop_love_interest_1, ":cur_lady"),
		(neg|troop_slot_eq, ":cur_troop", slot_troop_love_interest_2, ":cur_lady"),
		(neg|troop_slot_eq, ":cur_troop", slot_troop_love_interest_3, ":cur_lady"),
	##diplomacy start+ also allow -1 to signify no-one courted
		(try_begin),
			(this_or_next|troop_slot_eq, ":cur_troop", slot_troop_love_interest_1, -1),#< added
			(troop_slot_eq, ":cur_troop", slot_troop_love_interest_1, 0),
			(troop_set_slot, ":cur_troop", slot_troop_love_interest_1, ":cur_lady"),
		(else_try),
			(this_or_next|troop_slot_eq, ":cur_troop", slot_troop_love_interest_2, -1),#< added
			(troop_slot_eq, ":cur_troop", slot_troop_love_interest_2, 0),
			(troop_set_slot, ":cur_troop", slot_troop_love_interest_2, ":cur_lady"),
		(else_try),
			(this_or_next|troop_slot_eq, ":cur_troop", slot_troop_love_interest_3, -1),#< added
			(troop_slot_eq, ":cur_troop", slot_troop_love_interest_3, 0),
			(troop_set_slot, ":cur_troop", slot_troop_love_interest_3, ":cur_lady"),
		(try_end),
	(try_end),
        (try_end),
	(assign, reg1, ":save_reg1"),
	(assign, reg0, ":save_reg0"),#revert register
	##diplomacy end+
	]),
	("faction_conclude_feast", 
	[
	(store_script_param, ":faction_no", 1),
	(store_script_param, ":venue", 2),
	
	(str_store_faction_name, s3, ":faction_no"),
	(str_store_party_name, s4, ":venue"),

    (try_begin),
        (eq, "$cheat_mode", 1),
	    (display_message, "str_s3_feast_concludes_at_s4"),
    (try_end),

	(try_begin),
		(eq, ":faction_no", "fac_player_faction"),
		(assign, ":faction_no", "$players_kingdom"),
	(try_end),
	
	(party_set_slot, ":venue", slot_town_has_tournament, 0),
	
	#markspot
	
	(assign, ":nobility_in_faction", 0),
	(assign, ":nobility_in_attendance", 0),

	(try_for_range, ":troop_no", active_npcs_begin, kingdom_ladies_end),
		(store_faction_of_troop, ":troop_faction", ":troop_no"),
		(eq, ":faction_no", ":troop_faction"),
		
		(val_add, ":nobility_in_faction", 1),

		#CHECK -- is the troop there?
		(troop_slot_eq, ":troop_no", slot_troop_cur_center, ":venue"),
		(val_add, ":nobility_in_attendance", 1),

		#check for marriages
		##diplomacy start+ enable marriages for non-kingdom ladies (for example, between two companions)
		(this_or_next|troop_slot_eq, ":troop_no", slot_troop_occupation, slto_robber_knight),
		(this_or_next|troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
		(this_or_next|troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_seneschal),
		(this_or_next|troop_slot_eq, ":troop_no", slot_troop_occupation, slto_player_companion),
		##diplomacy end+
		(troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_lady),
		(troop_get_slot, ":groom", ":troop_no", slot_troop_betrothed),
		(gt, ":groom", 0),

		(troop_get_slot, ":groom_party", ":groom", slot_troop_leaded_party),
		(party_is_active, ":groom_party"),
		(party_get_attached_to, ":groom_party_attached", ":groom_party"),
		(eq, ":groom_party_attached", ":venue"),
		
		(store_faction_of_troop, ":lady_faction", ":troop_no"),
		(store_faction_of_troop, ":groom_faction", ":groom"),

		(eq, ":groom_faction", ":lady_faction"),
		(eq, ":lady_faction", ":faction_no"),
		(store_current_hours, ":hours_since_betrothal"),
		(troop_get_slot, ":betrothal_time", ":troop_no", slot_troop_betrothal_time),
		(val_sub, ":hours_since_betrothal", ":betrothal_time"),
		(ge, ":hours_since_betrothal", 144), #6 days, should perhaps eventually be 29 days, or 696 yours

		(call_script, "script_get_kingdom_lady_social_determinants", ":troop_no"),
		(assign, ":wedding_venue", reg1),
        ##diplomacy start+ be less picky about where to hold the feast as time goes on
		#(eq, ":venue", ":wedding_venue"),
		(neq, ":troop_no", "trp_player"),
		(neq, ":groom", "trp_player"),
		(party_get_slot, ":town_lord", ":venue", slot_town_lord),
		(assign, ":hold_the_wedding", 0),
		(try_begin),
			#after 6 days, will be held if the venue is the ideal one
			(eq, ":venue", ":wedding_venue"),
			(assign, ":hold_the_wedding", 1),
		(else_try),
			#after 6 days, will be held if the bride's father/guardian holds a feast
			(ge, ":town_lord", 0),
			(this_or_next|troop_slot_eq, ":troop_no", slot_troop_father, ":town_lord"),
			(this_or_next|troop_slot_eq, ":troop_no", slot_troop_mother, ":town_lord"),
			   (troop_slot_eq, ":troop_no", slot_troop_guardian, ":town_lord"),
			(assign, ":hold_the_wedding", 1),
		(else_try),
			#after 20 days, will be held if the bride, the groom, or either of their
			#parents hold a feast
			(ge, ":hours_since_betrothal", 24 * 20),
			(ge, ":town_lord", 0),
			(this_or_next|eq, ":troop_no", ":town_lord"),
			(this_or_next|eq, ":groom", ":town_lord"),
			(this_or_next|troop_slot_eq, ":groom", slot_troop_father, ":town_lord"),
			   (troop_slot_eq, ":groom", slot_troop_mother, ":town_lord"),
			(assign, ":hold_the_wedding", 1),
		(else_try),
			#after 60 days, if against all odds the engagement hasn't been called off,
			#the faction leader qualifies, as does any relative
			(ge, ":hours_since_betrothal", 24 * 60),
			(ge, ":town_lord", 0),
			#(call_script, "script_troop_get_family_relation_to_troop", ":town_lord", ":troop_no"),
			(call_script, "script_dplmc_troop_get_family_relation_to_troop",  ":town_lord", ":troop_no"),
			(assign, ":bride_relation", reg0),
			#(call_script, "script_troop_get_family_relation_to_troop", ":town_lord", ":groom"),
			(call_script, "script_dplmc_troop_get_family_relation_to_troop", ":town_lord", ":groom"),
			(this_or_next|faction_slot_eq, ":troop_faction", slot_faction_leader, ":town_lord"),
			(this_or_next|ge, reg0, 1),
				(ge, ":bride_relation", 1),
			(assign, ":hold_the_wedding", 1),
		(try_end),
		(eq, ":hold_the_wedding", 1),
		##diplomacy end+
		(call_script, "script_courtship_event_bride_marry_groom", ":troop_no", ":groom", 0), #parameters from dialog
	(try_end),


#ssss	(assign, ":placeholder_reminder_to_calculate_effect_for_player_feast", 1),
	
	
	
	(party_get_slot, ":feast_host", ":venue", slot_town_lord),
	(assign, ":quality_of_feast", 0),
	
	(try_begin),
		(check_quest_active, "qst_organize_feast"),
		(quest_slot_eq, "qst_organize_feast", slot_quest_target_center, ":venue"),
		(assign, ":feast_host", "trp_player"),
		
		(assign, ":total_guests", 400),
		
		(call_script, "script_succeed_quest", "qst_organize_feast"),
		(call_script, "script_end_quest", "qst_organize_feast"),
		
		(call_script, "script_internal_politics_rate_feast_to_s9", "trp_household_possessions", ":total_guests", "$players_kingdom", 1),
		(assign, ":quality_of_feast", reg0),
	(else_try),
		(assign, ":quality_of_feast", 60),
	(try_end),
	
	
	(try_begin),
		(ge, "$cheat_mode", 1),
		(str_store_troop_name, s4, ":feast_host"),
		(assign, reg4, ":quality_of_feast"),
		(display_message, "@{!}DEBUG - {s4}'s feast has rating of {reg4}"),
	(try_end),
	
	
	(try_begin),
	  (ge, ":feast_host", 0),
	  (store_div, ":renown_boost", ":quality_of_feast", 3),
	  (call_script, "script_change_troop_renown", ":feast_host", ":renown_boost"),

	  (try_for_range, ":troop_no", active_npcs_begin, active_npcs_end),
		(troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
		(troop_get_slot, ":leaded_party", ":troop_no", slot_troop_leaded_party),
		(party_is_active, ":leaded_party"),
		(party_get_attached_to, ":leaded_party_attached", ":leaded_party"),
		(eq, ":leaded_party_attached", ":venue"),
		
		(assign, ":relation_booster", ":quality_of_feast"),
		(val_div, ":relation_booster", 20),
		
		(try_begin),
			(eq, ":feast_host", "trp_player"),
			(val_sub, ":relation_booster", 1),
			(val_max, ":relation_booster", 0),
		(try_end),
		(call_script, "script_troop_change_relation_with_troop", ":feast_host", ":troop_no", ":relation_booster"),
		(val_add, "$total_feast_changes", ":relation_booster"),
	  (try_end),
	(try_end),
	

	(assign, reg3, ":nobility_in_attendance"),
	(assign, reg4, ":nobility_in_faction"),
	
	(try_begin),
		(eq, "$cheat_mode", 1),
		(display_message, "str_attendance_reg3_nobles_out_of_reg4"),
	(try_end),	
	]),
	("lady_evaluate_troop_as_suitor", 
	[
	(store_script_param, ":lady", 1),
	(store_script_param, ":suitor", 2),
	
	(call_script, "script_troop_get_romantic_chemistry_with_troop", ":lady", ":suitor"),
	(assign, ":romantic_chemistry", reg0),
	
	(try_begin),
      (call_script, "script_cf_test_lord_incompatibility_to_s17", ":lady", ":suitor"),		
    (try_end),
	
	(store_sub, ":personality_modifier", 0, reg0),
	(assign, reg2, ":personality_modifier"),
		
	(try_begin),
		(troop_get_slot, ":renown_modifier", ":suitor", slot_troop_renown),
		(val_div, ":renown_modifier", 20),
		(try_begin),
			(this_or_next|troop_slot_eq, ":lady", slot_lord_reputation_type, lrep_conventional),
				(troop_slot_eq, ":lady", slot_lord_reputation_type, lrep_ambitious),
			(val_mul, ":renown_modifier", 2),
			(val_sub, ":renown_modifier", 15),
		(try_end),
	(try_end),
	
	(store_add, ":final_score", ":renown_modifier", ":personality_modifier"),
	(val_add, ":final_score", ":romantic_chemistry"),
	(assign, reg0, ":final_score"),	
	]),
	("courtship_event_troop_court_lady", 
	[
	(store_script_param, ":suitor", 1),
	(store_script_param, ":lady", 2),

	
	#(try_begin),
	  #(eq, "$cheat_mode", 1),
	  #(str_store_troop_name, s4, ":suitor"),
	  #(str_store_troop_name, s5, ":lady"),
	  #(troop_get_slot, ":lady_location", ":lady", slot_troop_cur_center),
	  #(str_store_party_name, s7, ":lady_location"),
	  #(display_message, "str_s4_pursues_suit_with_s5_in_s7"),
	#(try_end),
	
	(troop_get_slot, ":previous_suitor", ":lady", slot_lady_last_suitor),
	(troop_set_slot, ":lady", slot_lady_last_suitor, ":suitor"), #can determine quarrels
	
	(try_begin),
		(eq, ":previous_suitor", "trp_player"),
		
		(troop_slot_ge, ":lady", slot_troop_met, 2),
		(call_script, "script_troop_get_relation_with_troop", ":suitor", "trp_player"), #add this to list of quarrels
		(assign, ":suitor_relation_w_player", reg0),
		
		(try_begin),
			(this_or_next|troop_slot_eq, ":suitor", slot_lord_reputation_type, lrep_selfrighteous),
			(this_or_next|troop_slot_eq, ":suitor", slot_lord_reputation_type, lrep_quarrelsome),
				(troop_slot_eq, ":suitor", slot_lord_reputation_type, lrep_debauched),
			(gt, ":suitor_relation_w_player", -20),
			(call_script, "script_add_log_entry", logent_lords_quarrel_over_woman, ":suitor", "trp_player", ":lady", 0),
		(else_try),
			(is_between, ":suitor_relation_w_player", -5, -25),
			(call_script, "script_add_log_entry", logent_lords_quarrel_over_woman, ":suitor", "trp_player", ":lady", 0),
		(try_end),
	(else_try),
		(neq, ":previous_suitor", "trp_player"), #not the player
	
		(neq, ":suitor", ":previous_suitor"),
		(ge, ":previous_suitor", active_npcs_begin),
		
		(call_script, "script_cf_test_lord_incompatibility_to_s17", ":suitor", ":previous_suitor"),
		(call_script, "script_add_log_entry", logent_lords_quarrel_over_woman, ":suitor", ":previous_suitor", ":lady", 0),
		
		(call_script, "script_troop_get_relation_with_troop", ":suitor", ":previous_suitor"), #add this to list of quarrels
		(ge, reg0, 0),
		(call_script, "script_troop_change_relation_with_troop", ":suitor", ":previous_suitor", -20),
		(val_add, "$total_courtship_quarrel_changes", -20),
	(else_try),	 #quarrelsome lords quarrel anyway
		(troop_slot_eq, ":suitor", slot_lord_reputation_type, lrep_quarrelsome),
		(neq, ":suitor", ":previous_suitor"),
		(ge, ":previous_suitor", active_npcs_begin),
		
#		(neq, ":previous_suitor", "trp_player"),
		
		(call_script, "script_troop_get_relation_with_troop", ":suitor", ":previous_suitor"), #add this to list of quarrels
		(lt, reg0, 10),
		(call_script, "script_add_log_entry", logent_lords_quarrel_over_woman, ":suitor", ":previous_suitor", ":lady", 0),
		(ge, reg0, 0),
		(call_script, "script_troop_change_relation_with_troop", ":suitor", ":previous_suitor", -20),
		(val_add, "$total_courtship_quarrel_changes", -20),
		
	(try_end),
	
	
#	(call_script, "script_troop_get_relation_with_troop", ":lady", ":suitor"),
#	(assign, ":orig_relation", reg0),

    (call_script, "script_lady_evaluate_troop_as_suitor", ":lady", ":suitor"),
	
	(store_random_in_range, ":random", 5, 16),
	(store_div, ":relationship_change", reg0, ":random"),
	
	(call_script, "script_troop_get_relation_with_troop", ":lady", ":suitor"),
	(assign, ":orig_relation", reg0),

	(call_script, "script_troop_change_relation_with_troop", ":lady", ":suitor", ":relationship_change"),
	
	(call_script, "script_troop_get_relation_with_troop", ":lady", ":suitor"),
	(assign, ":lady_suitor_relation", reg0),
		
	(try_begin),
		(ge, ":lady_suitor_relation", 10),
		(lt, ":orig_relation", 10),
		(call_script, "script_add_log_entry", logent_lady_favors_suitor, ":lady", 0, ":suitor", 0),
		
		(try_begin),
			(eq, "$cheat_mode", 1),
			(display_message, "str_note__favor_event_logged"),
		(try_end),
		
	(else_try),
		(this_or_next|lt, ":lady_suitor_relation", -20),
			(ge, ":lady_suitor_relation", 20),

		(call_script, "script_get_kingdom_lady_social_determinants", ":lady"),
		(assign, ":guardian", reg0),
		(call_script, "script_troop_get_relation_with_troop", ":suitor", ":guardian"),
		(assign, ":suitor_guardian_relation", reg0),
		#things come to a head, one way or another
		
		(assign, ":highest_competitor_lady_score", -1),
		(assign, ":competitor_preferred_by_lady", -1),
		
		(assign, ":highest_competitor_guardian_score", ":suitor_guardian_relation"),
		(assign, ":competitor_preferred_by_guardian", -1),
		
		#log potential competitors
		(try_for_range, ":possible_competitor", lords_begin, lords_end),
			(neq, ":possible_competitor", ":suitor"),
		
			(this_or_next|troop_slot_eq, ":possible_competitor", slot_troop_love_interest_1, ":lady"),
			(this_or_next|troop_slot_eq, ":possible_competitor", slot_troop_love_interest_2, ":lady"),
				(troop_slot_eq, ":possible_competitor", slot_troop_love_interest_3, ":lady"),
			
			(try_begin),
				(call_script, "script_troop_get_relation_with_troop", ":possible_competitor", ":lady"),
				(gt, reg0, ":highest_competitor_lady_score"),
				(assign, ":competitor_preferred_by_lady", ":possible_competitor"),
				(assign, ":highest_competitor_lady_score", reg0),
			(try_end),	

			(try_begin),
				(call_script, "script_troop_get_relation_with_troop", ":possible_competitor", ":guardian"),
				(gt, reg0, ":highest_competitor_guardian_score"),
				(assign, ":competitor_preferred_by_guardian", ":possible_competitor"),
				(assign, ":highest_competitor_guardian_score", reg0),
			(try_end),	
		(try_end),

		#RESULTS
		#Guardian forces lady to be betrothed to suitor now		
		(try_begin), 
			(lt, ":lady_suitor_relation", -20),
			(this_or_next|troop_slot_eq, ":guardian", slot_lord_reputation_type, lrep_selfrighteous),
			(this_or_next|troop_slot_eq, ":guardian", slot_lord_reputation_type, lrep_debauched),
				(troop_slot_eq, ":guardian", slot_lord_reputation_type, lrep_quarrelsome),
			(eq, ":competitor_preferred_by_guardian", -1),

			(this_or_next|troop_slot_eq, ":suitor", slot_lord_reputation_type, lrep_selfrighteous),
			(this_or_next|troop_slot_eq, ":suitor", slot_lord_reputation_type, lrep_debauched),
				(troop_slot_eq, ":suitor", slot_lord_reputation_type, lrep_quarrelsome),

			(troop_slot_eq, ":suitor", slot_troop_betrothed, -1),
			(troop_slot_eq, ":lady", slot_troop_betrothed, -1),
				
			(call_script, "script_add_log_entry", logent_lady_betrothed_to_suitor_by_family, ":lady", 0, ":suitor", 0),
			(troop_set_slot, ":suitor", slot_troop_betrothed, ":lady"),
			(troop_set_slot, ":lady", slot_troop_betrothed, ":suitor"),
			(store_current_hours, ":hours"),
			(troop_set_slot, ":lady", slot_troop_betrothal_time, ":hours"),
			(troop_set_slot, ":suitor", slot_troop_betrothal_time, ":hours"),
			(try_begin),
				(eq, "$cheat_mode", 1),
				(display_message, "str_result_lady_forced_to_agree_to_engagement"),
			(try_end),

		#Lady rejects the suitor			
		(else_try),
			(lt, ":lady_suitor_relation", -20),
			
			(call_script, "script_add_log_entry", logent_lady_rejects_suitor, ":lady", 0, ":suitor", 0),
			(call_script, "script_courtship_event_lady_break_relation_with_suitor", ":lady", ":suitor"),
			(try_begin),
				(eq, "$cheat_mode", 1),
				(display_message, "str_result_lady_rejects_suitor"),
			(try_end),

		#A happy engagement, with parental blessing
		(else_try),	
			(gt, ":lady_suitor_relation", 20),
			(gt, ":suitor_guardian_relation", 0),
			(eq, ":competitor_preferred_by_lady", -1),

			(troop_slot_eq, ":suitor", slot_troop_betrothed, -1),
			(troop_slot_eq, ":lady", slot_troop_betrothed, -1),
			
			(call_script, "script_add_log_entry", logent_lady_betrothed_to_suitor_by_choice, ":lady", 0, ":suitor", 0),
			(troop_set_slot, ":suitor", slot_troop_betrothed, ":lady"),
			(troop_set_slot, ":lady", slot_troop_betrothed, ":suitor"),
			(store_current_hours, ":hours"),
			(troop_set_slot, ":lady", slot_troop_betrothal_time, ":hours"),
			(troop_set_slot, ":suitor", slot_troop_betrothal_time, ":hours"),
			
			(try_begin),
				(eq, "$cheat_mode", 1),
				(str_store_troop_name, s4, ":lady"),
				(str_store_troop_name, s5, ":suitor"),
				(display_message, "str_result_happy_engagement_between_s4_and_s5"),
			(try_end),
			
		#Lady elopes
		(else_try), 
			(gt, ":lady_suitor_relation", 20),
			
			(eq, ":competitor_preferred_by_lady", -1),
			##diplomacy start+
			##Fix Native bug, the following line should be checking ":lady", not ":guardian"
			##OLD:
			#(this_or_next|troop_slot_eq, ":guardian", slot_lord_reputation_type, lrep_adventurous),
			#	(troop_slot_eq, ":guardian", slot_lord_reputation_type, lrep_ambitious),
			##NEW:
			(this_or_next|troop_slot_eq, ":lady", slot_lord_reputation_type, lrep_adventurous),
				(troop_slot_eq, ":lady", slot_lord_reputation_type, lrep_ambitious),
			##diplomacy end+
				
			(troop_slot_eq, ":suitor", slot_troop_betrothed, -1),
			(troop_slot_eq, ":lady", slot_troop_betrothed, -1),
				
			#lady elopes
			(call_script, "script_courtship_event_bride_marry_groom", ":lady", ":suitor", 1),
			#add elopements to quarrel descriptions
					
			(try_begin),
				(eq, "$cheat_mode", 1),
				(str_store_troop_name, s4, ":lady"),
				(str_store_troop_name, s5, ":suitor"),
				(display_message, "str_result_s4_elopes_with_s5"),
			(try_end),
			
		#Lady reluctantly agrees to marry under pressure from family			
		(else_try),	
			(troop_slot_eq, ":lady", slot_lord_reputation_type, lrep_conventional),
			(eq, ":competitor_preferred_by_guardian", -1),
			(gt, ":suitor_guardian_relation", 4),
			
			(store_random_in_range, ":random", 0, 5),
			(eq, ":random", 0),
			
			(troop_slot_eq, ":suitor", slot_troop_betrothed, -1),
			(troop_slot_eq, ":lady", slot_troop_betrothed, -1),

			(call_script, "script_add_log_entry", logent_lady_betrothed_to_suitor_by_pressure, ":lady", 0, ":suitor", 0),
			(troop_set_slot, ":suitor", slot_troop_betrothed, ":lady"),
			(troop_set_slot, ":lady", slot_troop_betrothed, ":suitor"),
			(store_current_hours, ":hours"),
			(troop_set_slot, ":lady", slot_troop_betrothal_time, ":hours"),
			(troop_set_slot, ":suitor", slot_troop_betrothal_time, ":hours"),
			(try_begin),
				(eq, "$cheat_mode", 1),
				(str_store_troop_name, s4, ":lady"),
				(str_store_troop_name, s5, ":suitor"),				
				(display_message, "str_result_s4_reluctantly_agrees_to_engagement_with_s5"),
			(try_end),

		#Stalemate -- make patience roll
		(else_try), 
			(gt, ":lady_suitor_relation", 20),

			(store_random_in_range, reg3, 0, 3),
			(try_begin),
				(eq, "$cheat_mode", 1),
				(display_message, "str_result_stalemate_patience_roll_=_reg3"),
			(try_end),

			(eq, reg3, 0),
			(call_script, "script_add_log_entry", logent_lady_rejected_by_suitor, ":lady", 0, ":suitor", 0),
			(call_script, "script_courtship_event_lady_break_relation_with_suitor", ":lady", ":suitor"),
		(try_end),
		
	(try_end),
	
	]),
	("courtship_event_lady_break_relation_with_suitor", #parameters from dialog
	[
	(store_script_param, ":lady", 1),
	(store_script_param, ":suitor", 2),
	
	(try_for_range, ":love_interest_slot", slot_troop_love_interest_1, slot_troop_love_interests_end),
		(troop_slot_eq, ":suitor", ":love_interest_slot", ":lady"),
		##diplomacy start+ set to -1 instead, since 0 is the player (how annoying)
		#(troop_set_slot, ":suitor", ":love_interest_slot", 0),
		(troop_set_slot, ":suitor", ":love_interest_slot", -1),
		##diplomacy end+
	(try_end),
	(call_script, "script_assign_troop_love_interests", ":suitor"),
	
	(try_begin),
		(troop_slot_eq, ":lady", slot_troop_betrothed, ":suitor"),


		(troop_set_slot, ":lady", slot_troop_betrothed, -1),
	##diplomacy start+ perform the same check for the suitor that was done,
	#for the lady, so this script has no unfortunate consequences even if
	#called inappropriately.
	(try_end),
	(try_begin),
		(troop_slot_eq, ":suitor", slot_troop_betrothed, ":lady"),
		(troop_set_slot, ":suitor", slot_troop_betrothed, -1),
	##diplomacy end+
	(try_end),


	]),
	("courtship_event_bride_marry_groom", #parameters from dialog or scripts
	[
	(store_script_param, ":bride", 1),
	(store_script_param, ":groom", 2),
	(store_script_param, ":elopement", 3),

	(try_begin),
		(eq, ":bride", "trp_player"),
		(assign, ":venue", "$g_encountered_party"),
	(else_try),
		(troop_get_slot, ":venue", ":bride", slot_troop_cur_center),
		##diplomacy start+
		#Ensure there is a venue.
		(lt, ":venue", 1),
		(troop_get_slot, ":venue", ":groom", slot_troop_cur_center),
		##diplomacy end+
	(try_end),

	(store_faction_of_troop, ":groom_faction", ":groom"),
	
	
	(try_begin),
		(eq, ":elopement", 0),
		(call_script, "script_add_log_entry", logent_lady_marries_suitor, ":bride", ":venue", ":groom", 0),
	(else_try),
		(call_script, "script_add_log_entry", logent_lady_elopes_with_lord, ":bride", ":venue", ":groom", 0),
	(try_end),
	
	(str_store_troop_name, s3, ":bride"),
	(str_store_troop_name, s4, ":groom"),
	(str_store_party_name, s5, ":venue"),

	(try_begin),
	##diplomacy start+ this should be globally-visible for notable personages
	#    (this_or_next|is_between, ":groom_faction", kingdoms_begin, kingdoms_end),
	#    (this_or_next|troop_slot_ge, ":groom", slot_troop_met, 1),
	#    (troop_slot_ge, ":bride", slot_troop_met, 1),
		(display_log_message, "str_s3_marries_s4_at_s5"),
	#(else_try),
    #    (eq, "$cheat_mode", 1),
	#    (display_message, "str_s3_marries_s4_at_s5"),
	##diplomacy end+
    (try_end),

	(troop_set_slot, ":bride", slot_troop_spouse, ":groom"),
	(troop_set_slot, ":groom", slot_troop_spouse, ":bride"),

	#Break groom's romantic relations
	(try_for_range, ":love_interest_slot", slot_troop_love_interest_1, slot_troop_love_interests_end),
		(troop_set_slot, ":groom", ":love_interest_slot", 0),
	(try_end),

	#Break bride's romantic relations
	(try_for_range, ":active_npc", active_npcs_begin, active_npcs_end),
		(try_for_range, ":love_interest_slot", slot_troop_love_interest_1, slot_troop_love_interests_end),
			(troop_slot_eq, ":active_npc", ":love_interest_slot", ":bride"),
			(call_script, "script_courtship_event_lady_break_relation_with_suitor", ":bride", ":active_npc"),
		(try_end),
	(try_end),
	
	
	
	(troop_set_slot, ":bride", slot_troop_betrothed, -1),
	(troop_set_slot, ":groom", slot_troop_betrothed, -1),
	
	
	
    #change relations with family
	##diplomacy start+ Include kingdom ladies
	#(try_for_range, ":family_member", lords_begin, lords_end),
	(try_for_range, ":family_member", heroes_begin, heroes_end),
		(neq, ":family_member", ":bride"),
		(neq, ":family_member", ":groom"),
	##diplomacy end+
		(call_script, "script_troop_get_family_relation_to_troop", ":bride", ":family_member"),
		(gt, reg0, 0),
		(store_div, ":family_relation_boost", reg0, 3),
		(try_begin),
			(eq, ":elopement", 1),
			(val_mul, ":family_relation_boost", -2),
		(try_end),
		##diplomacy start+ Fix error!  Change relation between groom and family member, not groom and bride.
		#(call_script, "script_troop_change_relation_with_troop", ":groom", ":bride", ":family_relation_boost"),
		(call_script, "script_troop_change_relation_with_troop", ":groom", ":family_member", ":family_relation_boost"),
		##diplomacy end+
		(val_add, "$total_courtship_quarrel_changes", ":family_relation_boost"),
	(try_end),

	(try_begin),
		(this_or_next|eq, ":groom", "trp_player"),
			(eq, ":bride", "trp_player"),
		##diplomacy start+ fix bug where player didn't get right to rule
		#gekokujo 3.0 reduced RTR rewards start
		#(call_script, "script_change_player_right_to_rule", 15),##one argument, not two
		(call_script, "script_change_player_right_to_rule", 5),##one argument, not two
		#gekokujo 3.0 reduced RTR rewards end
		##diplomacy end+
	(try_end),


	(try_begin),
		(eq, ":groom", "trp_player"),
		(check_quest_active, "qst_wed_betrothed"),
		(call_script, "script_succeed_quest", "qst_wed_betrothed"),
		(call_script, "script_end_quest", "qst_wed_betrothed"),
	(try_end),

	
	(try_begin),
		(check_quest_active, "qst_visit_lady"),
		(quest_slot_eq, "qst_visit_lady", slot_quest_giver_troop, ":bride"),
		(call_script, "script_abort_quest", "qst_visit_lady", 0),
	(try_end),

	
	(try_begin),
		(eq, ":groom", "trp_player"),
		(check_quest_active, "qst_visit_lady"),
		(call_script, "script_abort_quest", "qst_visit_lady", 0),
	(try_end),	
	(try_begin),
		(eq, ":groom", "trp_player"),
		(check_quest_active, "qst_duel_courtship_rival"),
		(call_script, "script_abort_quest", "qst_duel_courtship_rival", 0),
	(try_end),	
	
	
	(try_begin),
		(eq, ":bride", "trp_player"),
	    (call_script, "script_player_join_faction", ":groom_faction"),
		(assign, "$player_has_homage", 1),
	(else_try),
		(eq, ":groom", "trp_player"),
		
		(try_begin),
			(ge, "$cheat_mode", 1),
			(str_store_troop_name, s4, ":bride"),
			(display_message, "@{!} DEBUG - {s4} faction change in marriage case 5"),
		(try_end),
		(troop_set_faction, ":bride", "$players_kingdom"),
	(else_try),
	
		(try_begin),
			(ge, "$cheat_mode", 1),
			(str_store_troop_name, s4, ":bride"),
			(display_message, "@{!}DEBUG - {s4} faction changed by marriage, case 6"), 
		(try_end),
	
		(troop_set_faction, ":bride", ":groom_faction"),
	(try_end),

    (try_begin),
        (this_or_next|eq, ":groom", "trp_player"),
           (eq, ":bride", "trp_player"),   
        (unlock_achievement, ACHIEVEMENT_HAPPILY_EVER_AFTER),
		(try_begin),
			(eq, ":elopement", 1),
			(unlock_achievement, ACHIEVEMENT_HEART_BREAKER),
		(try_end),
    (try_end),
	
	
	
    (try_begin),
        (this_or_next|eq, ":groom", "trp_player"),
           (eq, ":bride", "trp_player"),
		#(eq, ":elopement", 0),    
        (call_script, "script_start_wedding_cutscene", ":groom", ":bride"),
    (try_end),
	]),
	#script_find_total_prosperity_score
    # INPUT: center_no
    # OUTPUT: reg0 = total_prosperity_score
	(
	"find_total_prosperity_score",
	[
	  (store_script_param, ":center_no", 1),
	  
      (try_begin), #":total_prosperity_score" changes between 10..100
        (is_between, ":center_no", walled_centers_begin, walled_centers_end),
            
        (party_get_slot, ":center_prosperity", ":center_no", slot_town_prosperity),
        (store_add, ":center_prosperity_add_200_div_10", ":center_prosperity", 200),
        (val_div, ":center_prosperity_add_200_div_10", 10),
        (try_begin),
          (is_between, ":center_no", towns_begin, towns_end),            
          (store_mul, ":this_center_score", ":center_prosperity_add_200_div_10", 15),
        (else_try),
          (store_mul, ":this_center_score", ":center_prosperity_add_200_div_10", 5),
        (try_end),
        (assign, ":total_prosperity_score", ":this_center_score"), 
                        
        (try_for_range_backwards, ":village_no", villages_begin, villages_end),
          (party_slot_eq, ":village_no", slot_village_bound_center, ":center_no"),

          (party_get_slot, ":village_prosperity", ":village_no", slot_town_prosperity),
          (store_add, ":village_prosperity_add_200_div_10", ":village_prosperity", 200),
          (val_div, ":village_prosperity_add_200_div_10", 10),
          (store_mul, ":this_village_score", ":village_prosperity_add_200_div_10", 5),
                    
          (val_add, ":total_prosperity_score", ":this_village_score"), 
        (try_end),
      (else_try),
        (party_get_slot, ":center_prosperity", ":center_no", slot_town_prosperity),
        (store_add, ":center_prosperity_add_200_div_10", ":center_prosperity", 200),
        (val_div, ":center_prosperity_add_200_div_10", 10),
        (store_mul, ":this_center_score", ":center_prosperity_add_200_div_10", 5),
        (assign, ":total_prosperity_score", ":this_center_score"), 
      (try_end),
      (val_div, ":total_prosperity_score", 10),
      
      (assign, reg0, ":total_prosperity_score"),
	]),
    #script_calculate_center_assailability_score
    # INPUT: faction_no
    # param1: faction_no 
    # param2: all_vassals_included, (becomes 1 if we want to find attackable center if we collected 20% of vassals during gathering army phase)
    # OUTPUT: 
    # reg0 = center_to_attack (-1 if none is logical)
    # reg1 = maximum_attack_score
    (
    "calculate_center_assailability_score", 
    [		
      (store_script_param, ":troop_no", 1),
      (store_script_param, ":potential_target", 2),
      (store_script_param, ":all_vassals_included", 3),
      
      (assign, ":target_score", -1),
      
      (store_faction_of_troop, ":faction_no", ":troop_no"),
  
      (store_current_hours, ":hours_since_last_offensive"),
      (faction_get_slot, ":last_offensive_time", ":faction_no", slot_faction_last_offensive_concluded),
      (val_sub, ":hours_since_last_offensive", ":last_offensive_time"),
      
      (store_div, ":last_offensive_time_score", ":hours_since_last_offensive", 12), #30..50
      (val_add, ":last_offensive_time_score", 30),
      (val_min, ":last_offensive_time_score", 100),

      (faction_get_slot, ":faction_marshal", ":faction_no", slot_faction_marshall),
    
      (assign, ":marshal_party", -1),
      (assign, ":marshal_strength", 0),
      #(assign, ":strength_of_nearby_friend", 0),
      
      (try_begin),
        (gt, ":faction_marshal", 0),
        (troop_get_slot, ":marshal_party", ":faction_marshal", slot_troop_leaded_party),
        (party_is_active, ":marshal_party"),
        (party_get_slot, ":marshal_strength", ":marshal_party", slot_party_cached_strength),
        #(eq, ":all_vassals_included", 0),
        (party_get_slot, ":strength_of_current_followers", ":marshal_party", slot_party_follower_strength),
        #(party_get_slot, ":strength_of_nearby_friend", ":marshal_party", slot_party_nearby_friend_strength),
      (try_end),
  
      #(try_begin),
      #  (eq, ":all_vassals_included", 0),
      #    
      #  (try_begin),
      #    (gt, ":faction_marshal", 0),
      #    (troop_get_slot, ":marshal_party", ":faction_marshal", slot_troop_leaded_party),
      #    (party_is_active, ":marshal_party"),
      #    (party_get_slot, ":strength_of_potential_followers", ":marshal_party", slot_party_follower_strength),
      #  (try_end),                
      #(else_try),
      #  (eq, ":all_vassals_included", 1),
      #      
      #  (assign, ":strength_of_potential_followers", 0),
      #          
      #  (try_for_parties, ":party_no"),
      #    (store_faction_of_party, ":party_faction", ":party_no"),
      #    (eq, ":party_faction", ":faction_no"),
      #    (neq, ":party_no", ":marshal_party"),          
      #    (party_slot_eq, ":party_no", slot_party_type, spt_kingdom_hero_party),
      #    (call_script, "script_party_calculate_strength", ":party_no", 0),
      #    (val_add, ":strength_of_potential_followers", reg0),
      #  (try_end),    
      #  
      #  (val_div, ":strength_of_potential_followers", 2), #Ozan - Think about this, will you divide strength_of_potential_followers to 3 or 2.5 or 2
      #(else_try),
      #  (assign, ":strength_of_potential_followers", 0),      
      #(try_end),
      
      (faction_get_slot, ":last_attacked_center", ":faction_no", slot_faction_last_attacked_center),
      (faction_get_slot, ":last_attacked_hours", ":faction_no", slot_faction_last_attacked_hours),
            
      (try_begin),
        (store_current_hours, ":hours"),
        (store_add, ":last_attacked_hours_plus_24", ":last_attacked_hours", 24),
        (gt, ":hours", ":last_attacked_hours_plus_24"),
        (faction_set_slot, ":faction_no", slot_faction_last_attacked_center, 0),
        (assign, ":last_attacked_center", 0),
      (try_end),
                
      (try_begin),        
        (this_or_next|eq, ":last_attacked_center", 0),
        (this_or_next|eq, ":last_attacked_center", ":potential_target"),
        (this_or_next|eq, "$g_do_not_skip_other_than_current_ai_object", 1),
        (neg|faction_slot_eq, ":faction_no", slot_faction_marshall, ":troop_no"),
        
        (party_is_active, ":potential_target"),
        (store_faction_of_party, ":potential_target_faction", ":potential_target"),
          
        (store_relation, ":relation", ":potential_target_faction", ":faction_no"),	      
        (lt, ":relation", 0),
        
        #attack if and only if we are already besieging that center or anybody do not making besiege.
        (assign, ":faction_of_besieger_party", -1),
        (try_begin),        
          (is_between, ":potential_target", walled_centers_begin, walled_centers_end),      
          (neg|party_slot_eq, ":potential_target", slot_center_is_besieged_by, -1), 
          (party_get_slot, ":besieger_party", ":potential_target", slot_center_is_besieged_by),
          (party_is_active, ":besieger_party"),
          (store_faction_of_party, ":faction_of_besieger_party", ":besieger_party"),
        (try_end),	
        			     
        (this_or_next|eq, ":faction_of_besieger_party", -1), 
        (eq, ":faction_of_besieger_party", ":faction_no"),
        
        #attack if and only if this center is not a village or if it is village it should not be raided or looted
        (assign, ":village_is_looted_or_raided_already", 0),
        (try_begin),
          (is_between, ":potential_target", villages_begin, villages_end),
          (try_begin),
            (party_slot_eq, ":potential_target", slot_village_state, svs_being_raided),
            (party_get_slot, ":raider_party", ":potential_target", slot_village_raided_by),
			(party_is_active, ":raider_party"),
			
            (store_faction_of_party, ":raider_faction", ":raider_party"),
            (neq, ":raider_faction", ":faction_no"),
            (assign, ":raiding_by_one_other_faction", 1),
          (else_try),
            (assign, ":raiding_by_one_other_faction", 0),
          (try_end),  
          (this_or_next|party_slot_eq, ":potential_target", slot_village_state, svs_looted),
          (eq, ":raiding_by_one_other_faction", 1),
          (assign, ":village_is_looted_or_raided_already", 1),
        (try_end),        
        (eq, ":village_is_looted_or_raided_already", 0),

        #if ":potential_target" is faction object of some other faction which is enemy to owner of 
        #":potential_target" then this target cannot be new target we are looking for.
        (assign, ":this_potantial_target_is_target_of_some_other_faction", 0),
        (try_for_range, ":cur_faction", kingdoms_begin, kingdoms_end),
          (is_between, ":cur_faction", "fac_kingdom_1", kingdoms_end), #Excluding player kingdom
          (neq, ":cur_faction", ":faction_no"),
          (faction_get_slot, ":faction_object", ":cur_faction", slot_faction_ai_object),
          (eq, ":faction_object", ":potential_target"),
          (store_relation, ":rel", ":potential_target_faction", ":cur_faction"),
          (lt, ":rel", 0),
          (assign, ":this_potantial_target_is_target_of_some_other_faction", 1),          
        (try_end),      
        (eq, ":this_potantial_target_is_target_of_some_other_faction", 0),                                            
    		  				
        (try_begin),
          (is_between, ":potential_target", walled_centers_begin, walled_centers_end),      
          (party_get_slot, ":potential_target_inside_strength", ":potential_target", slot_party_cached_strength),
          (party_get_slot, ":potential_target_nearby_enemy_strength", ":potential_target", slot_party_nearby_friend_strength),    
          (val_div, ":potential_target_nearby_enemy_strength", 2),        
          (store_add, ":potential_target_strength", ":potential_target_inside_strength", ":potential_target_nearby_enemy_strength"),

          #(try_begin),
            #(eq, ":faction_no", "fac_kingdom_4"),
            #(assign, reg0, ":potential_target_inside_strength"),
            #(assign, reg1, ":potential_target_nearby_enemy_strength"),
            #(assign, reg2, ":marshal_strength"),
            #(assign, reg3, ":strength_of_potential_followers"),
            #(assign, reg4, ":strength_of_nearby_friend"),
            #(assign, reg6, ":marshal_party"),
            #(str_store_party_name, s8, ":potential_target"),
            #(eq, ":all_vassals_included", 0),
            #(display_message, "@DEBUG : {s8}:{reg0}, neare {reg1}, our {reg2}, follow {reg3}, nearf {reg4}"),
          #(try_end),
                    
          (val_mul, ":potential_target_strength", 4), #in walled centers defenders have advantage.
          (val_div, ":potential_target_strength", 3),
                              
          #(store_add, ":army_strength", ":marshal_strength", ":strength_of_potential_followers"),
          (assign, ":army_strength", ":marshal_strength"),
          (val_add, ":army_strength", ":strength_of_current_followers"),
          (store_mul, ":power_ratio", ":army_strength", 100),
          
          #this ratio ":power_ratio" shows (our total army power) / (their total army power)
          (try_begin),
            (gt, ":potential_target_strength", 0),
            (val_div, ":power_ratio", ":potential_target_strength"),
          (else_try),
            (assign, ":power_ratio", 1000),
          (try_end),  
        (else_try),        
          #(party_get_slot, ":potential_target_nearby_enemy_strength", ":potential_target", slot_party_nearby_friend_strength), #gekokujo 3.0 integrating motomataru's campaign AI start
          (assign, ":potential_target_strength", 1000),
                    
          #(store_add, ":army_strength", ":marshal_strength", ":strength_of_potential_followers"),
          (assign, ":army_strength", ":marshal_strength"),
          (val_add, ":army_strength", ":strength_of_current_followers"),
          (store_mul, ":power_ratio", ":army_strength", 100),
                                                            
          (try_begin),
            (gt, ":potential_target_strength", 0),
            (val_div, ":power_ratio", ":potential_target_strength"),
          (else_try),
            (assign, ":power_ratio", 1000),
          (try_end),            
        (try_end),
                            
        (ge, ":power_ratio", 120), #attack if and only if our army is at least 1.2 times powerfull				
        (store_sub, ":power_ratio_sub_120", ":power_ratio", 120),
        
        (try_begin),
          (lt, ":power_ratio_sub_120", 100), #changes between 20..120
          (store_add, ":power_ratio_score", ":power_ratio_sub_120", 20),
        (else_try),
          (lt, ":power_ratio_sub_120", 200), #changes between 120..170
          (store_sub, ":power_ratio_score", ":power_ratio_sub_120", 100),
          (val_div, ":power_ratio_score", 2),
          (val_add, ":power_ratio_score", 120),
        (else_try),
          (lt, ":power_ratio_sub_120", 400), #changes between 170..210
          (store_sub, ":power_ratio_score", ":power_ratio_sub_120", 200),
          (val_div, ":power_ratio_score", 5),
          (val_add, ":power_ratio_score", 170),
        (else_try),
          (lt, ":power_ratio_sub_120", 800), #changes between 210..250
          (store_sub, ":power_ratio_score", ":power_ratio_sub_120", 400),
          (val_div, ":power_ratio_score", 10),
          (val_add, ":power_ratio_score", 210),
        (else_try),
          (assign, ":power_ratio_score", 250),
        (try_end),
          
        (assign, ":number_of_walled_centers", 0),
        (assign, ":total_distance", 0),
        (try_for_range, ":walled_center", walled_centers_begin, walled_centers_end),
          (store_faction_of_party, ":walled_center_faction", ":walled_center"),
          (eq, ":walled_center_faction", ":faction_no"),
                
          (store_distance_to_party_from_party, ":dist", ":walled_center", ":potential_target"),            
          (val_add, ":total_distance", ":dist"),
                
          (val_add, ":number_of_walled_centers", 1),
        (try_end),
                
        (try_begin),
          (gt, ":number_of_walled_centers", 0),
          (store_div, ":average_distance", ":total_distance", ":number_of_walled_centers"),
          #(assign, reg0, ":average_distance"),                    
          #(str_store_faction_name, s7, ":faction_no"),
          #(str_store_party_name, s8, ":potential_target"),
          #(display_message, "@average distance for {s7} for {s8} is {reg0}"),
          
          (try_begin),
            (ge, ":marshal_party", 0),
            (party_is_active, ":marshal_party"),
            (store_distance_to_party_from_party, ":marshal_dist_to_potential_target", ":marshal_party", ":potential_target"),
          (else_try),
            (assign, ":marshal_dist_to_potential_target", 100),
          (try_end),
                      
          (try_begin),  
            #if currently main aim of our faction is attacking to an enemy center and that center is already besieged/raided by one of 
            #our parties then divide marshal_dist_to_potential_target_div_x score for current center to "3/2" instead of "3" and this
            #result in decrease at distance_score, and also decrease some scores from power_ratio_score in order to avoid frequently 
            #changes at main aimed target city of our faction during sieges.
              
            (faction_get_slot, ":current_ai_state", ":faction_no", slot_faction_ai_state),
            (eq, ":current_ai_state", sfai_attacking_center),
            (faction_get_slot, ":current_ai_object", ":faction_no", slot_faction_ai_object),
            
            (ge, ":current_ai_object", 0),
            (neq, ":current_ai_object", ":potential_target"),
              
            (try_begin),
              (ge, ":power_ratio_score", 300), #200 max
              (assign, ":power_ratio_score", 200),
            (else_try),
              (ge, ":power_ratio_score", 100), #100..200
              (val_sub, ":power_ratio_score", 100),
              (val_div, ":power_ratio_score", 2),
              (val_add, ":power_ratio_score", 100),
            (try_end),  
            
            (try_begin),
              (faction_slot_eq, ":faction_no", slot_faction_marshall, ":troop_no"),
              (eq, "$g_do_not_skip_other_than_current_ai_object", 0),
              (assign, ":power_ratio_score", 0), #lets completely forget all other choices if we are already besieging one center.
            (try_end),  
            
            (faction_set_slot, ":faction_no", slot_faction_last_attacked_center, ":current_ai_object"),
            (store_current_hours, ":hours"),
            (faction_set_slot, ":faction_no", slot_faction_last_attacked_hours, ":hours"),

            (eq, ":all_vassals_included", 0),

            (store_mul, ":marshal_dist_to_potential_target_div_x", ":marshal_dist_to_potential_target", 2),
            (val_div, ":marshal_dist_to_potential_target_div_x", 3),
          (else_try),
            (store_div, ":marshal_dist_to_potential_target_div_x", ":marshal_dist_to_potential_target", 3),
          (try_end),
            
          (store_add, ":total_distance", ":average_distance", ":marshal_dist_to_potential_target_div_x"), #in average ":total_distance" is about 150, min : 0, max : 1000
        (else_try),
          (assign, ":total_distance", 100),
        (try_end),                

        (try_begin),
          #according to cautious troop distance is more important
          ##diplomacy start+ Take into account lady & companion personality types
		  ##OLD:
	      #(this_or_next|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_upstanding),
	      #(this_or_next|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_debauched),
	      #(this_or_next|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_goodnatured),
	      #(troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_cunning),	      	      
		  #
		  ##NEW:
		  (call_script, "script_dplmc_store_troop_personality_caution_level", ":troop_no"),
		  (assign, ":troop_caution", reg0),
		  (gt, ":troop_caution", 0),
		  ##diplomacy end+

          (try_begin),
            (lt, ":total_distance", 30), #very close (100p)
            (assign, ":distance_score", 100),
          (else_try),
            (lt, ":total_distance", 80), #close (50p-100p)
            (store_sub, ":distance_score", ":total_distance", 30),
            (val_div, ":distance_score", 1),
            (store_sub, ":distance_score", 100, ":distance_score"),
          (else_try),  
            (lt, ":total_distance", 160), #far (10p-50p)
            (store_sub, ":distance_score", ":total_distance", 80),
            (val_div, ":distance_score", 2),
            (store_sub, ":distance_score", 50, ":distance_score"),
          (else_try),
            (assign, ":distance_score", 10), #very far
          (try_end),
        (else_try),  
          #according to agressive troop distance is less important
          
          (try_begin),
            (lt, ":total_distance", 40), #very close (100p)
            (assign, ":distance_score", 100),
          (else_try),
            (lt, ":total_distance", 140), #close (50p-100p)
            (store_sub, ":distance_score", ":total_distance", 40),
            (val_div, ":distance_score", 2),
            (store_sub, ":distance_score", 100, ":distance_score"),
          (else_try),  
            (lt, ":total_distance", 300), #far (10p-50p)
            (store_sub, ":distance_score", ":total_distance", 140),
            (val_div, ":distance_score", 4),
            (store_sub, ":distance_score", 50, ":distance_score"),
          (else_try),
            (assign, ":distance_score", 10), #very far
          (try_end),
        (try_end),
		##diplomacy start+ If AI changes are enabled, reduce distance penalty (increase score)
		##for recently-lost fiefs.
		(try_begin),
			(lt, ":distance_score", 100),
			(ge, "$g_dplmc_ai_changes", DPLMC_AI_CHANGES_LOW),
			(party_slot_eq, ":potential_target", slot_center_ex_faction, ":faction_no"),
			(party_get_slot, reg0, ":potential_target", dplmc_slot_center_last_transfer_time),
			(gt, reg0, 0),#0 means the slot was uninitialized.  A negative number would be before the start of the game.
			(store_current_hours, ":hours_since_transfer"),
			(val_sub, ":hours_since_transfer", reg0),
			(try_begin),
				(ge, "$g_dplmc_ai_changes", DPLMC_AI_CHANGES_HIGH),
				(assign, reg0, 24 * 21),#within last three weeks
			(else_try),
				(ge, "$g_dplmc_ai_changes", DPLMC_AI_CHANGES_MEDIUM),
				(assign, reg0, 24 * 14),#within last two weeks
			(else_try),
				(assign, reg0, 24 * 7),#within last week
			(try_end),
			(lt, ":hours_since_transfer", reg0),
			(val_add, ":distance_score", 100),
			(val_div, ":distance_score", 2),
		(try_end),
		##diplomacy end+

        (store_mul, ":target_score", ":distance_score", ":power_ratio_score"),
        (val_mul, ":target_score", ":last_offensive_time_score"),
        (val_div, ":target_score", 100), #target score is between 0..10000 generally here

        (call_script, "script_find_total_prosperity_score", ":potential_target"),                
        (assign, ":total_prosperity_score", reg0),
            
        #(try_begin), #new for increase attackability of villages by ai
          #(is_between, ":potential_target", villages_begin, villages_end), 
          (val_mul, ":total_prosperity_score", 3),
          (val_div, ":total_prosperity_score", 2),
        #(try_end),

        (val_mul, ":target_score", ":total_prosperity_score"),
          
        #gekokujo 3.0 integrating motomataru's campaign AI start
		#(try_begin), #if both that center was our (original center) and (ex center) than bonus is 1.2x
        #  (party_slot_eq, ":potential_target", slot_center_ex_faction, ":faction_no"),
        #  (party_slot_eq, ":potential_target", slot_center_original_faction, ":faction_no"),
        #  (val_mul, ":target_score", 12),
        #  (val_div, ":target_score", 10),
        #(else_try), #if either that center was our (original center) or (ex center) than bonus is 1.1x
        #  (this_or_next|party_slot_eq, ":potential_target", slot_center_ex_faction, ":faction_no"),
        #  (party_slot_eq, ":potential_target", slot_center_original_faction, ":faction_no"),
        #  (val_mul, ":target_score", 11),
        #  (val_div, ":target_score", 10),
        #(try_end),
		(try_begin),
          (is_between, ":potential_target", walled_centers_begin, walled_centers_end),      
		  (try_begin),
            (party_slot_eq, ":potential_target", slot_center_original_faction, ":faction_no"),
            (val_mul, ":target_score", 14),
            (val_div, ":target_score", 10),
		  (try_end),
		  (try_begin),
            (party_slot_eq, ":potential_target", slot_center_ex_faction, ":faction_no"),
            (val_mul, ":target_score", 11),
            (val_div, ":target_score", 10),
		  (try_end),
        (try_end),
		#gekokujo 3.0 integrating motomataru's campaign AI start
            
        (val_div, ":target_score", 1000), #target score is between 0..1000 generally here
        
        (try_begin),
          (eq, ":potential_target_faction", "fac_player_supporters_faction"),
          (game_get_reduce_campaign_ai, ":reduce_campaign_ai"),
          
          (assign, ":number_of_walled_centers_player_have", 0),
          (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
            (store_faction_of_party, ":center_faction", ":center_no"),
            (eq, ":center_faction", "fac_player_supporters_faction"),
            (val_add, ":number_of_walled_centers_player_have", 1),
          (try_end),
          
          (try_begin),
            (eq, ":reduce_campaign_ai", 2), #easy
            
            (try_begin),
              (le, ":number_of_walled_centers_player_have", 2),
              (assign, ":hardness_score", 0),              
            (else_try),
              (eq, ":number_of_walled_centers_player_have", 3),
              (assign, ":hardness_score", 20),
            (else_try),
              (eq, ":number_of_walled_centers_player_have", 4),
              (assign, ":hardness_score", 40),
            (else_try),
              (eq, ":number_of_walled_centers_player_have", 5),
              (eq, ":number_of_walled_centers_player_have", 6),
              (assign, ":hardness_score", 55),
            (else_try),
              (eq, ":number_of_walled_centers_player_have", 7),
              (eq, ":number_of_walled_centers_player_have", 8),
              (eq, ":number_of_walled_centers_player_have", 9),
              (assign, ":hardness_score", 70),
            (else_try),
              (assign, ":hardness_score", 85),
            (try_end),
          (else_try),  
            (eq, ":reduce_campaign_ai", 1), #medium

            (try_begin),
              (le, ":number_of_walled_centers_player_have", 1),
              (assign, ":hardness_score", 25),
            (else_try),
              (eq, ":number_of_walled_centers_player_have", 2),
              (assign, ":hardness_score", 45),
            (else_try),
              (eq, ":number_of_walled_centers_player_have", 3),
              (assign, ":hardness_score", 60),
            (else_try),
              (eq, ":number_of_walled_centers_player_have", 4),
              (eq, ":number_of_walled_centers_player_have", 5),
              (assign, ":hardness_score", 75),
            (else_try),
              (eq, ":number_of_walled_centers_player_have", 6),
              (eq, ":number_of_walled_centers_player_have", 7),
              (eq, ":number_of_walled_centers_player_have", 8),
              (assign, ":hardness_score", 85),
            (else_try),
              (assign, ":hardness_score", 92),
            (try_end),
          (else_try), #hard
            (assign, ":hardness_score", 100), 
          (try_end),
          
          (val_mul, ":target_score", ":hardness_score"),
          (val_div, ":target_score", 100),
        (try_end),

        (try_begin),
          (ge, "$cheat_mode", 1),
          (eq, ":faction_no", "fac_kingdom_4"),
          (ge, ":target_score", -1),
          (assign, reg0, ":target_score"),
          (assign, reg7, ":total_prosperity_score"),
          (assign, reg8, ":power_ratio_score"),
          (assign, reg9, ":distance_score"),
          (assign, reg10, ":last_offensive_time_score"),
          (str_store_party_name, s8, ":potential_target"),
          #(eq, ":all_vassals_included", 0),
          (assign, reg11, ":all_vassals_included"),          
          #(display_message, "@DEBUG : attack of {s8} is {reg0}({reg11}), prs:{reg7}, pow:{reg8}, dis:{reg9}, lst:{reg10}"),
        (try_end),  
      (try_end),
                                                     
      (assign, reg0, ":target_score"),
      (assign, reg1, ":power_ratio"),
      (assign, reg2, ":distance_score"),
      (assign, reg3, ":total_prosperity_score"),
    ]),
    #script_find_center_to_defend
    # INPUT: 
    # param1: faction_no 
    # OUTPUT: 
    # reg0 = center_to_defend (-1 if none is logical)
    # reg1 = maximum_defend_score
    # reg3 = enemy_strength_near_most_threatened_center
    (
    "find_center_to_defend",
    [
      (store_script_param, ":troop_no", 1),
	  
	  (store_faction_of_troop, ":faction_no", ":troop_no"),
	  
      (faction_get_slot, ":faction_marshal", ":faction_no", slot_faction_marshall),
      (faction_get_slot, ":current_ai_state", ":faction_no", slot_faction_ai_state),
      (assign, ":marshal_party", -1),  
      (try_begin),
        (gt, ":faction_marshal", 0),
        (troop_get_slot, ":marshal_party", ":faction_marshal", slot_troop_leaded_party),
      (try_end),

      (assign, ":most_threatened_center", -1),
      (assign, ":maximum_threat_score", 0),
	  #gekokujo 3.0 integrating motomataru's campaign AI start	
	  (assign, ":num_walled_centers", 0),	#MOTO count
	  (assign, ":num_villages", 0),	#MOTO count
	  (assign, ":num_idle_villages", 0),	#MOTO count
	  #gekokujo 3.0 integrating motomataru's campaign AI end
      (try_for_range, ":cur_center", centers_begin, centers_end),
        (store_faction_of_party, ":center_faction", ":cur_center"),
        (eq, ":center_faction", ":faction_no"),
	 	    
        (party_get_slot, ":exact_enemy_strength", ":cur_center", slot_center_sortie_enemy_strength),
		#Distort this to account for questionable intelligence
		#(call_script, "script_reduce_exact_number_to_estimate", ":exact_enemy_strength"),
		#(assign, ":enemy_strength_nearby", reg0),
		(assign, ":enemy_strength_nearby", ":exact_enemy_strength"),		
		
        (assign, ":threat_importance", 0),
        (try_begin),          
          (is_between, ":cur_center", walled_centers_begin, walled_centers_end),
		  (val_add, ":num_walled_centers", 1), #gekokujo 3.0 integrating motomataru's campaign AI
          (party_slot_ge, ":cur_center", slot_center_is_besieged_by, 0),
          
          (call_script, "script_find_total_prosperity_score", ":cur_center"),
          (assign, ":total_prosperity_score", reg0),          
                              
          (party_get_slot, ":cur_center_strength", ":cur_center", slot_party_cached_strength),
          (val_mul, ":cur_center_strength", 4),
          (val_div, ":cur_center_strength", 3), #give 33% bonus to insiders because they are inside a castle
          
          #I removed below line and assigned ":cur_center_nearby_strength" to 0, because if not when defender army comes to help
          #threat become less because of high defence power but not yet enemy cleared.
          #(party_get_slot, ":cur_center_nearby_strength", ":cur_center", slot_party_nearby_friend_strength),
          (assign, ":cur_center_nearby_strength", 0),
          
          (val_add, ":cur_center_strength", ":cur_center_nearby_strength"), #add nearby friends and find ":cur_center_strength"
          
          (store_mul, ":power_ratio", ":enemy_strength_nearby", 100),
          (val_add, ":cur_center_strength", 1),
		  (val_max, ":cur_center_strength", 1),
          (val_div, ":power_ratio", ":cur_center_strength"),
         
          (assign, ":player_is_attacking", 0),
          (party_get_slot, ":besieger_party", ":cur_center", slot_center_is_besieged_by),
          (try_begin),
            (party_is_active, ":besieger_party"),
            (try_begin),
              (eq, ":besieger_party", "p_main_party"),
              (assign, ":player_is_attacking", 1),
              #(display_message, "@{!}DEBUG : player is attacking a center (1)"),
            (else_try),
              (store_faction_of_party, ":besieger_faction", ":besieger_party"),
              (eq, ":besieger_faction", "fac_player_faction"),
              (assign, ":player_is_attacking", 1),
              #(display_message, "@{!}DEBUG : player is attacking a center (2)"),
            (else_try), 
              (party_get_attached_to, ":player_is_attached_to", "p_main_party"),
              (ge, ":player_is_attached_to", 0),
              (eq, ":player_is_attached_to", ":besieger_party"),
              (assign, ":player_is_attacking", 1),
              #(display_message, "@{!}DEBUG : player is attacking a center (3)"),
            (try_end),
          (try_end),
          
          (try_begin),
            (eq, ":player_is_attacking", 0),                       
            
            (try_begin),
              (lt, ":power_ratio", 40), #changes between 1..1
              (assign, ":threat_importance", 1),
            (else_try),  
              (lt, ":power_ratio", 80), #changes between 1..7
              (store_sub, ":threat_importance", ":power_ratio", 40),
              (val_div, ":threat_importance", 5),
              (val_add, ":threat_importance", 1), #1
            (else_try),  
              (lt, ":power_ratio", 120), #changes between 7..17
              (store_sub, ":threat_importance", ":power_ratio", 80),
              (val_div, ":threat_importance", 4),
              (val_add, ":threat_importance", 7), #1 + 6
            (else_try),  
              (lt, ":power_ratio", 200),
              (store_sub, ":threat_importance", ":power_ratio", 120),
              (val_div, ":threat_importance", 10),
              (val_add, ":threat_importance", 17), #1 + 6 + 10
            (else_try),  
              (assign, ":threat_importance", 25),
            (try_end),  
          (else_try),
            (try_begin),
              (lt, ":power_ratio", 200), #changes between 5..25
			  #gekokujo 3.0 forgot to integrate start
              #(val_div, ":threat_importance", 10),
			  (store_div, ":threat_importance", ":power_ratio", 10),    #MOTO correction (thanks MOTO:) (mexxico))
			  #gekokujo 3.0 forgot to integrate end
              (val_add, ":threat_importance", 6 ),
            (else_try),  
              (assign, ":threat_importance", 26),
            (try_end),             
          (try_end),          
        (else_try),        
          (is_between, ":cur_center", villages_begin, villages_end),
		  #gekokujo 3.0 integrating motomataru's campaign AI start
          #(party_slot_eq, ":cur_center", slot_village_state, svs_being_raided),
		  #MOTO village defense rewrite
          # (party_slot_eq, ":cur_center", slot_village_state, svs_being_raided),
          (neg|party_slot_eq, ":cur_center", slot_village_state, svs_looted),
		  
	      (val_add, ":num_villages", 1),
		  (try_begin),
            (neg|party_slot_eq, ":cur_center", slot_village_state, svs_normal),
	        (val_add, ":num_idle_villages", 1),
		  (try_end),
		  #gekokujo 3.0 integrating motomataru's campaign AI end
          
          (gt, ":enemy_strength_nearby", 0),
          
          (call_script, "script_find_total_prosperity_score", ":cur_center"),
          #(assign, ":power_ratio", 100), #useless #gekokujo 3.0 integrating motomataru's campaign AI
          (assign, ":total_prosperity_score", reg0),
          (assign, ":threat_importance", 10), #if faction village is looted they lose money for shorter time period. So importance is something low (6-8).
        (try_end),
        
        (gt, ":threat_importance", 0),
        
		#gekokujo 3.0 integrating motomataru's campaign AI start
        #(try_begin),
        #  (is_between, ":cur_center", walled_centers_begin, walled_centers_end),
        #  (assign, ":enemy_strength_nearby_score", 120), 
          (store_add, ":enemy_strength_nearby_score", ":enemy_strength_nearby", 20000), 
          (val_div, ":enemy_strength_nearby_score", 200),
		#gekokujo 3.0 integrating motomataru's campaign AI end
          
          (try_begin),          
            (ge, ":marshal_party", 0),
            (party_is_active, ":marshal_party"),
            (store_distance_to_party_from_party, ":marshal_dist_to_cur_center", ":marshal_party", ":cur_center"),
          (else_try),
            (assign, ":marshal_dist_to_cur_center", 100),
          (try_end),
                              
          (try_begin),  
            #if currently our target is ride to break a siege then
            #divide marshal_distance for other center's to "2" instead of "4" and add some small more distance to avoid easily 
            #changing mind during siege because of small score differences.
            
	        #(faction_get_slot, ":current_ai_state", ":faction_no", slot_faction_ai_state),
            (eq, ":current_ai_state", sfai_attacking_enemies_around_center),                                   
            (faction_get_slot, ":current_ai_object", ":faction_no", slot_faction_ai_object),            
            (is_between, ":current_ai_object", walled_centers_begin, walled_centers_end),            
            (neq, ":current_ai_object", ":cur_center"),
            (val_mul, ":marshal_dist_to_cur_center", 2),
            (val_add, ":marshal_dist_to_cur_center", 20),
          (try_end),
          
          (val_mul, ":marshal_dist_to_cur_center", 2), #standard multipication (1.5x) to adjust distance scoring same with formula at find_center_to_attack
          #(val_div, ":marshal_dist_to_cur_center", 2),
                    
          (try_begin),
            (lt, ":marshal_dist_to_cur_center", 10), #very close (100p)
            (assign, ":distance_score", 100),
          (else_try),
            (lt, ":marshal_dist_to_cur_center", 160), #close (50p-100p)
            (store_sub, ":distance_score", ":marshal_dist_to_cur_center", 10),
            (val_div, ":distance_score", 3),
            (store_sub, ":distance_score", 100, ":distance_score"),
          (else_try),  
            (lt, ":marshal_dist_to_cur_center", 360), #far (10p-50p)
            (store_sub, ":distance_score", ":marshal_dist_to_cur_center", 250),
            (val_div, ":distance_score", 5),
            (store_sub, ":distance_score", 50, ":distance_score"),
          (else_try),
            (assign, ":distance_score", 10), #very far
          (try_end),
		#gekokujo 3.0 integrating motomataru's campaign AI start
        #(else_try),
        #  (store_add, ":enemy_strength_nearby_score", ":enemy_strength_nearby", 20000), 
        #  (val_div, ":enemy_strength_nearby_score", 200),
        #  (assign, ":distance_score", 70), #not related to marshal's position, because everybody is going same place (no gathering in most village raids)
        #(try_end),         
		#gekokujo 3.0 integrating motomataru's campaign AI end

		##diplomacy start+
		(try_begin),
			#AI changes LOW: Give priority to defending centers with lords
			(le, DPLMC_AI_CHANGES_LOW, "$g_dplmc_ai_changes"),
			(party_slot_ge, ":cur_center", slot_town_lord, 0),
			(val_mul, ":threat_importance", 120),
			(val_div, ":threat_importance", 100),
		(try_end),
		##diplomacy end+        
        (store_mul, ":threat_score", ":enemy_strength_nearby_score", ":total_prosperity_score"), 
        (val_mul, ":threat_score", ":threat_importance"), 
        (val_mul, ":threat_score", ":distance_score"),
        (val_div, ":threat_score", 10000),
        
        (try_begin),
		  (ge, "$cheat_mode", 1),
          (gt, ":threat_score", 0),
          (eq, ":faction_no", "fac_kingdom_6"),
          (assign, reg0, ":threat_score"),
          (str_store_party_name, s32, ":cur_center"),
          (assign, reg1,  ":total_prosperity_score"),
          (assign, reg2, ":enemy_strength_nearby_score"),
          (assign, reg3, ":threat_importance"),
          (assign, reg4, ":distance_score"),
          #(display_message, "@{!}DEBUG : defend of {s32} is {reg0}, prosperity:{reg1}, enemy nearby:{reg2}, threat importance:{reg3}, distance: {reg4}"),
        (try_end),

        (gt, ":threat_score", ":maximum_threat_score"),
        		
        (assign, ":most_threatened_center", ":cur_center"),
        (assign, ":maximum_threat_score", ":threat_score"),
        (assign, ":enemy_strength_near_most_threatened_center", ":enemy_strength_nearby"),
      (try_end),
      
      (val_mul, ":maximum_threat_score", 3),
      (val_div, ":maximum_threat_score", 2),

	  #gekokujo 3.0 integrating motomataru's campaign AI start
	  #MOTO importance decreases with more centers
      (val_mul, ":maximum_threat_score", 2),
      (try_begin),	#last walled center is all-important
        (is_between, ":most_threatened_center", walled_centers_begin, walled_centers_end),
		(val_div, ":maximum_threat_score", ":num_walled_centers"),
      (else_try),	#villages start becoming important after half of them have been trash
	    (gt, ":num_villages", 0),
		(val_mul, ":maximum_threat_score", ":num_idle_villages"),
		(val_div, ":maximum_threat_score", ":num_villages"),
	  (try_end),
	  #MOTO end importance decreases with more centers
	  #gekokujo 3.0 integrating motomataru's campaign AI end
	  
      (assign, reg0, ":most_threatened_center"),
      (assign, reg1, ":maximum_threat_score"),
      (assign, reg2, ":enemy_strength_near_most_threatened_center"),
    ]),
	("courtship_poem_reactions", #parameters from dialog
	[
	(store_script_param, ":lady", 1),
	(store_script_param, ":poem", 2),	
	
	(troop_get_slot, ":lady_reputation", ":lady", slot_lord_reputation_type),

	(try_begin),
		(eq, "$cheat_mode", 1),
		(assign, reg4, ":poem"),
		(assign, reg5, ":lady_reputation"),
		(display_message, "str_poem_choice_reg4_lady_rep_reg5"),
	(try_end),
	
	(try_begin), #conventional ++, ambitious -, adventurous -
		(eq, ":poem", courtship_poem_tragic),
		(eq, ":lady_reputation", lrep_conventional),
		(str_store_string, s11, "str_ah__kais_and_layali__such_a_sad_tale_many_a_time_has_it_been_recounted_for_my_family_by_the_wandering_poets_who_come_to_our_home_and_it_has_never_failed_to_bring_tears_to_our_eyes"),
		(assign, ":result", 5),
	(else_try),
		(eq, ":poem", courtship_poem_tragic),
		(eq, ":lady_reputation", lrep_ambitious),
		(str_store_string, s11, "str_kais_and_layali_three_hundred_stanzas_of_pathetic_sniveling_if_you_ask_me_if_kais_wanted_to_escape_heartbreak_he_should_have_learned_to_live_within_his_station_and_not_yearn_for_what_he_cannot_have"),
		(assign, ":result", 0),
	(else_try),
		(eq, ":poem", courtship_poem_tragic),
		(eq, ":lady_reputation", lrep_otherworldly),
		(str_store_string, s11, "str_kais_and_layali_no_one_should_ever_have_written_such_a_sad_poem_if_it_was_the_destiny_of_kais_and_layali_to_be_together_than_their_love_should_have_conquered_all_obstacles"),
		(assign, ":result", 1),
	(else_try),
		(eq, ":poem", courtship_poem_tragic),
#		moralizing and adventurous
		(str_store_string, s11, "str_ah_kais_and_layali_a_very_old_standby_but_moving_in_its_way"),
		(assign, ":result", 3),
	#Heroic	
	(else_try), #adventurous ++, conventional -1, moralizing -1
		(eq, ":poem", courtship_poem_heroic),
		(eq, ":lady_reputation", lrep_adventurous),
		(str_store_string, s11, "str_the_saga_of_helgered_and_kara_such_happy_times_in_which_our_ancestors_lived_women_like_kara_could_venture_out_into_the_world_like_men_win_a_name_for_themselves_and_not_linger_in_their_husbands_shadow"),
		(assign, ":result", 5),
	(else_try), #adventurous ++, conventional -1, moralizing -1
		(eq, ":poem", courtship_poem_heroic),
		(eq, ":lady_reputation", lrep_ambitious),
		(str_store_string, s11, "str_ah_the_saga_of_helgered_and_kara_now_there_was_a_lady_who_knew_what_she_wanted_and_was_not_afraid_to_obtain_it"),
		(assign, ":result", 2),
	(else_try), #adventurous ++, conventional -1, moralizing -1
		(eq, ":poem", courtship_poem_heroic),
		(eq, ":lady_reputation", lrep_otherworldly),
		(str_store_string, s11, "str_the_saga_of_helgered_and_kara_a_terrible_tale__but_it_speaks_of_a_very_great_love_if_she_were_willing_to_make_war_on_her_own_family"),
		(assign, ":result", 2),
	(else_try), #adventurous ++, conventional -1, moralizing -1
		(eq, ":poem", courtship_poem_heroic),
		(eq, ":lady_reputation", lrep_moralist),
		(str_store_string, s11, "str_the_saga_of_helgered_and_kara_as_i_recall_kara_valued_her_own_base_passions_over_duty_to_her_family_that_she_made_war_on_her_own_father_i_have_no_time_for_a_poem_which_praises_such_a_woman"),
		(assign, ":result", 0),
	(else_try), #adventurous ++, conventional -1, moralizing -1
		(eq, ":poem", courtship_poem_heroic),
		(eq, ":lady_reputation", lrep_conventional),
		(str_store_string, s11, "str_the_saga_of_helgered_and_kara_how_could_a_woman_don_armor_and_carry_a_sword_how_could_a_man_love_so_ungentle_a_creature"),
		(assign, ":result", 0),
	#Comic
	(else_try), #ambitious ++, romantic -, moralizing 0
		(eq, ":poem", courtship_poem_comic),
		(eq, ":lady_reputation", lrep_otherworldly),
		(str_store_string, s11, "str_a_conversation_in_the_garden_i_cannot_understand_the_lady_in_that_poem_if_she_loves_the_man_why_does_she_tease_him_so"),
		(assign, ":result", 0),
	(else_try), #ambitious ++, romantic -, moralizing 0
		(eq, ":poem", courtship_poem_comic),
		(eq, ":lady_reputation", lrep_moralist),
		(str_store_string, s11, "str_a_conversation_in_the_garden_let_us_see__it_is_morally_unedifying_it_exalts_deception_it_ends_with_a_maiden_surrendering_to_her_base_passions_and_yet_i_cannot_help_but_find_it_charming_perhaps_because_it_tells_us_that_love_need_not_be_tragic_to_be_memorable"),
		(assign, ":result", 1),
	(else_try), #ambitious ++, romantic -, moralizing 0
		(eq, ":poem", courtship_poem_comic),
		(eq, ":lady_reputation", lrep_ambitious),
		(str_store_string, s11, "str_a_conversation_in_the_garden_now_that_is_a_tale_every_lady_should_know_by_heart_to_learn_the_subtleties_of_the_politics_she_must_practice"),
		(assign, ":result", 5),
	(else_try), #ambitious ++, romantic -, moralizing 0
		(eq, ":poem", courtship_poem_comic),
		#adventurous, conventional 
		(str_store_string, s11, "str_a_conversation_in_the_garden_it_is_droll_i_suppose__although_there_is_nothing_there_that_truly_stirs_my_soul"),
		(assign, ":result", 3),

	#Allegoric	
	(else_try), #moralizing ++, adventurous -, romantic -
		(eq, ":poem", courtship_poem_allegoric),
		(eq, ":lady_reputation", lrep_adventurous),
		(str_store_string, s11, "str_storming_the_fortress_of_love_ah_yes_the_lady_sits_within_doing_nothing_while_the_man_is_the_one_who_strives_and_achieves_i_have_enough_of_that_in_my_daily_life_why_listen_to_poems_about_it"),
		(assign, ":result", 0),
	(else_try), #moralizing ++, adventurous -, romantic -
		(eq, ":poem", courtship_poem_allegoric),
		(this_or_next|eq, ":lady_reputation", lrep_conventional),
			(eq, ":lady_reputation", lrep_moralist),
		(str_store_string, s11, "str_storming_the_fortress_of_love_ah_yes_an_uplifting_tribute_to_the_separate_virtues_of_man_and_woman"),
		(assign, ":result", 3),
	(else_try), #moralizing ++, adventurous -, romantic -
		(eq, ":poem", courtship_poem_allegoric),
		(eq, ":lady_reputation", lrep_otherworldly),
		(str_store_string, s11, "str_storming_the_fortress_of_love_ah_yes_but_although_it_is_a_fine_tale_of_virtues_it_speaks_nothing_of_passion"),
		(assign, ":result", 1),
	(else_try), #moralizing ++, adventurous -, romantic -
		(eq, ":poem", courtship_poem_allegoric),
		(eq, ":lady_reputation", lrep_ambitious),
		(str_store_string, s11, "str_storming_the_fortress_of_love_ah_a_sermon_dressed_up_as_a_love_poem_if_you_ask_me"),
		(assign, ":result", 1),

	(else_try), #romantic ++, moralizing 0, ambitious -
		(eq, ":poem", courtship_poem_mystic),
		(eq, ":lady_reputation", lrep_otherworldly),
		(str_store_string, s11, "str_a_hearts_desire_ah_such_a_beautiful_account_of_the_perfect_perfect_love_to_love_like_that_must_be_to_truly_know_rapture"),
		(assign, ":result", 4),		

	(else_try), #romantic ++, moralizing 0, ambitious -
		(eq, ":poem", courtship_poem_mystic),
		(eq, ":lady_reputation", lrep_ambitious),
		(str_store_string, s11, "str_a_hearts_desire_silly_if_you_ask_me_if_the_poet_desires_a_lady_then_he_should_endeavor_to_win_her__and_not_dress_up_his_desire_with_a_pretense_of_piety"),
		(assign, ":result", 0),		

	(else_try), #romantic ++, moralizing 0, ambitious -
		(eq, ":poem", courtship_poem_mystic),
		(eq, ":lady_reputation", lrep_moralist),
		(str_store_string, s11, "str_a_hearts_desire_hmm__it_is_an_interesting_exploration_of_earthly_and_divine_love_it_does_speak_of_the_spiritual_quest_which_brings_out_the_best_in_man_but_i_wonder_if_the_poet_has_not_confused_his_yearning_for_higher_things_with_his_baser_passions"),
		(assign, ":result", 2),		

	(else_try), #romantic ++, moralizing 0, ambitious -
		(eq, ":poem", courtship_poem_mystic),
		(str_store_string, s11, "str_a_hearts_desire_oh_yes__it_is_very_worthy_and_philosophical_but_if_i_am_to_listen_to_a_bard_strum_a_lute_for_three_hours_i_personally_prefer_there_to_be_a_bit_of_a_story"),
		(assign, ":result", 1),		
	(try_end),

	
	(try_begin),
		(eq, "$cheat_mode", 1),
		(assign, reg4, ":result"),
		(display_message, "str_result_reg4_string_s11"),
	(try_end),	
	
	
	(assign, reg0, ":result"),
	
	]),
	(
	"diplomacy_faction_get_diplomatic_status_with_faction", 
	#result: -1 faction_1 has a casus belli against faction_2. 1, faction_1 has a truce with faction_2, -2, the two factions are at war
	[
	(store_script_param, ":actor_faction", 1),
	(store_script_param, ":target_faction", 2),
	##diplomacy start+
	#Since "fac_player_supporters_faction" is used as a shorthand for the faction
	#run by the player, intercept that here instead of the various places this is
	#called from.
	(call_script, "script_dplmc_translate_inactive_player_supporter_faction_2", ":actor_faction", ":target_faction"),
	(assign, ":actor_faction", reg0),
	(assign, ":target_faction", reg1),
	##diplomacy end+

	(store_add, ":truce_slot", ":target_faction", slot_faction_truce_days_with_factions_begin),
	(store_add, ":provocation_slot", ":target_faction", slot_faction_provocation_days_with_factions_begin),
	(val_sub, ":truce_slot", kingdoms_begin),
	(val_sub, ":provocation_slot", kingdoms_begin),
	
	(assign, ":result", 0),
	(assign, ":duration", 0),
	
	(try_begin),
		(store_relation, ":relation", ":actor_faction", ":target_faction"),
		(lt, ":relation", 0),
		(assign, ":result", -2),
	(else_try),
		(faction_slot_ge, ":actor_faction", ":truce_slot", 1),
		(assign, ":result", 1),

		(faction_get_slot, ":duration", ":actor_faction", ":truce_slot"),
	(else_try),
		(faction_slot_ge, ":actor_faction", ":provocation_slot", 1),
		(assign, ":result", -1),
		
		(faction_get_slot, ":duration", ":actor_faction", ":provocation_slot"),
	(try_end),
	
	(assign, reg0, ":result"),
	(assign, reg1, ":duration"),
	]),
	("faction_follows_controversial_policy",
	[
	(store_script_param, ":faction_no", 1),
	(store_script_param, ":policy_type", 2),
	
	(faction_get_slot, ":faction_leader", ":faction_no", slot_faction_leader),

	(try_begin),
		(ge, "$cheat_mode", 1),
		(str_store_faction_name, s3, ":faction_no"),
		(display_message, "str_calculating_effect_for_policy_for_s3"),
		
		(val_add, "$number_of_controversial_policy_decisions", 1),
	(try_end),
	
	(try_begin),
		(eq, ":policy_type", logent_policy_ruler_attacks_without_provocation),
		(assign, ":hawk_relation_effect", 0),
		(assign, ":honorable_relation_effect", -2),
		(assign, ":honor_change", -1),
		
	(else_try),
		(eq, ":policy_type", logent_policy_ruler_ignores_provocation),
		(assign, ":hawk_relation_effect", -3),
		(assign, ":honorable_relation_effect", 0),
		(assign, ":honor_change", 0),
	
	(else_try),
		(eq, ":policy_type", logent_policy_ruler_declares_war_with_justification),
		(assign, ":hawk_relation_effect", 3),
		(assign, ":honorable_relation_effect", 1),
		(assign, ":honor_change", 0),

	(else_try),
		(eq, ":policy_type", logent_policy_ruler_breaks_truce),
		(assign, ":hawk_relation_effect", 0),
		(assign, ":honorable_relation_effect", -3),
		(assign, ":honor_change", -5),

	(else_try),
		(eq, ":policy_type", logent_policy_ruler_makes_peace_too_soon),
		(assign, ":hawk_relation_effect", -5),
		(assign, ":honorable_relation_effect", 0),
		(assign, ":honor_change", 0),

	##diplomacy start+ If none of the preceeding match, don't use random memory
	(else_try),
		(assign, ":hawk_relation_effect", 0),
		(assign, ":honorable_relation_effect", 0),
		(assign, ":honor_change", 0),
	##diplomacy end+
	(try_end),

	(try_begin),
		(eq, ":faction_leader", "trp_player"),
		(call_script, "script_change_player_honor", ":honor_change"),
	(try_end),

   ##diplomacy start+ add support for promoted kingdom ladies
	#(try_for_range, ":lord", active_npcs_begin, active_npcs_end),
	(try_for_range, ":lord", heroes_begin, heroes_end),
	##diplomacy end+
		(troop_slot_eq, ":lord", slot_troop_occupation, slto_kingdom_hero),
		(store_faction_of_troop, ":lord_faction", ":lord"),
		(eq, ":lord_faction", ":faction_no"),
		(neq, ":lord", ":faction_leader"),

		(try_begin),
		   ##diplomacy start+ Add support for lady personality type
			(this_or_next|troop_slot_eq, ":lord", slot_lord_reputation_type, lrep_adventurous),
			##diplomacy end+
			(this_or_next|troop_slot_eq, ":lord", slot_lord_reputation_type, lrep_martial),
			(this_or_next|troop_slot_eq, ":lord", slot_lord_reputation_type, lrep_quarrelsome),
			(this_or_next|troop_slot_eq, ":lord", slot_lord_reputation_type, lrep_selfrighteous),
				(troop_slot_eq, ":lord", slot_lord_reputation_type, lrep_debauched),
			(call_script, "script_troop_change_relation_with_troop", ":faction_leader", ":lord", ":hawk_relation_effect"),
			(val_add, "$total_policy_dispute_changes", ":hawk_relation_effect"),
		(try_end),

		(try_begin),
		   ##diplomacy start+ Add support for lady personality type
			(this_or_next|troop_slot_eq, ":lord", slot_lord_reputation_type, lrep_moralist),
			##diplomacy end+
			(this_or_next|troop_slot_eq, ":lord", slot_lord_reputation_type, lrep_martial),
			(this_or_next|troop_slot_eq, ":lord", slot_lord_reputation_type, lrep_goodnatured),
			(this_or_next|troop_slot_eq, ":lord", slot_lord_reputation_type, lrep_selfrighteous),
			(this_or_next|troop_slot_eq, ":lord", slot_lord_reputation_type, lrep_benefactor), #new for enfiefed commoners
			(this_or_next|troop_slot_eq, ":lord", slot_lord_reputation_type, lrep_custodian), #new for enfiefed commoners
				(troop_slot_eq, ":lord", slot_lord_reputation_type, lrep_upstanding),
			(call_script, "script_troop_change_relation_with_troop", ":faction_leader", ":lord", ":honorable_relation_effect"),
			(val_add, "$total_policy_dispute_changes", ":honorable_relation_effect"),

		(try_end),

	(try_end),

	]),
	("internal_politics_rate_feast_to_s9",
	[
	(store_script_param, ":householder", 1),
	(store_script_param, ":num_servings", 2),	
#	(store_script_param, ":faction", 3),	
	(store_script_param, ":consume_items", 4),	

	(val_max, ":num_servings", 1),
	
	(try_for_range, ":item", trade_goods_begin, trade_goods_end), 
		(item_set_slot, ":item", slot_item_amount_available, 0), #had no "item"
	(try_end),
	
	(troop_get_inventory_capacity, ":capacity", ":householder"),
	(try_for_range, ":inventory_slot", 0, ":capacity"),
		(troop_get_inventory_slot, ":item", ":householder", ":inventory_slot"),
		(is_between, ":item", trade_goods_begin, trade_goods_end),
	    (troop_inventory_slot_get_item_amount, ":slot_amount", ":householder", ":inventory_slot"),
		(item_get_slot, ":item_amount", ":item", slot_item_amount_available),
		(val_add, ":item_amount", ":slot_amount"),
		(item_set_slot, ":item", slot_item_amount_available, ":item_amount"),
	(try_end),
	#food
	(assign, ":food_amount", 0),
	(assign, ":food_variety", 0),
	
	(store_div, ":servings_div_by_12", ":num_servings", 12),
	(try_for_range, ":food_item", food_begin, food_end),
		(item_get_slot, ":food_in_slot", ":food_item", slot_item_amount_available),
		(val_add, ":food_amount", ":food_in_slot"),


##		(str_store_item_name, s4, ":food_item"),
##		(assign, reg3, ":food_in_slot"),
##		(assign, reg5, ":servings_div_by_12"),
##		(display_message, "str_reg3_units_of_s4_for_reg5_guests_and_retinue"),

		
		(ge, ":food_in_slot", ":servings_div_by_12"),
		(val_add, ":food_variety", 1),
	(try_end),
	
	(val_mul, ":food_amount", 100),
	(val_div, ":food_amount", ":num_servings"), #1 to 100 for each
	(val_min, ":food_amount", 100),
	
	(val_mul, ":food_variety", 85), #1 to 100 for each
	(val_div, ":food_variety", 10), 
	(val_min, ":food_variety", 100),
	
	#drink
	(assign, ":drink_amount", 0),
	(assign, ":drink_variety", 0),
	(store_div, ":servings_div_by_4", ":num_servings", 4),
	(try_for_range, ":drink_iterator", "itm_wine", "itm_smoked_fish"),
		(assign, ":drink_item", ":drink_iterator"),
		(item_get_slot, ":drink_in_slot", ":drink_item", slot_item_amount_available),
		
		(val_add, ":drink_amount", ":drink_in_slot"),
	
		(ge, ":drink_in_slot", ":servings_div_by_4"),
		(val_add, ":drink_variety", 1),
	(try_end),
	
	(val_mul, ":drink_amount", 200), #amount needed is 50% of the number of guests
	(val_max, ":num_servings", 1),
	
	(val_div, ":drink_amount", ":num_servings"), #1 to 100 for each
	(val_min, ":drink_amount", 100),
	(val_mul, ":drink_variety", 50), #1 to 100 for each

	#in the future, it might be worthwhile to add different varieties of spices
	(item_get_slot, ":spice_amount", "itm_spice", slot_item_amount_available),
	(store_mul, ":spice_percentage", ":spice_amount", 100),
	(val_max, ":servings_div_by_12", 1),
	(val_div, ":spice_amount", ":servings_div_by_12"),
	(val_min, ":spice_percentage", 100),
##	(assign, reg3, ":spice_amount"),
##	(assign, reg5, ":servings_div_by_12"),
##	(assign, reg6, ":spice_percentage"),
##	(display_message, "str_reg3_units_of_spice_of_reg5_to_be_consumed"),
	
	#oil availability. In the future, this may become an "atmospherics" category, including incenses
	(item_get_slot, ":oil_amount", "itm_oil", slot_item_amount_available),
	(store_mul, ":oil_percentage", ":oil_amount", 100),
	(val_max, ":servings_div_by_12", 1),
	(val_div, ":oil_amount", ":servings_div_by_12"),
	(val_min, ":oil_percentage", 100),
##	(assign, reg3, ":oil_amount"),
##	(assign, reg5, ":servings_div_by_12"),
##	(assign, reg6, ":oil_percentage"),
##	(display_message, "str_reg3_units_of_oil_of_reg5_to_be_consumed"),

	(store_div, ":food_amount_string", ":food_amount", 20),
	(val_add, ":food_amount_string", "str_feast_description"),
	(str_store_string, s8, ":food_amount_string"),
	(str_store_string, s9, "str_of_food_which_must_come_before_everything_else_the_amount_is_s8"),
	
	(store_div, ":food_variety_string", ":food_variety", 20),
	(val_add, ":food_variety_string", "str_feast_description"),
	(str_store_string, s8, ":food_variety_string"),
	(str_store_string, s9, "str_s9_and_the_variety_is_s8_"),

	(store_div, ":drink_amount_string", ":drink_amount", 20),
	(val_add, ":drink_amount_string", "str_feast_description"),
	(str_store_string, s8, ":drink_amount_string"),
	(str_store_string, s9, "str_s9_of_drink_which_guests_will_expect_in_great_abundance_the_amount_is_s8"),
	
	(store_div, ":drink_variety_string", ":drink_variety", 20),
	(val_add, ":drink_variety_string", "str_feast_description"),
	(str_store_string, s8, ":drink_variety_string"),
	(str_store_string, s9, "str_s9_and_the_variety_is_s8_"),
	
	(store_div, ":spice_string", ":spice_percentage", 20),
	(val_add, ":spice_string", "str_feast_description"),
	(str_store_string, s8, ":spice_string"),
	(str_store_string, s9, "str_s9_of_spice_which_is_essential_to_demonstrate_that_we_spare_no_expense_as_hosts_the_amount_is_s8_"),
	
	(store_div, ":oil_string", ":oil_percentage", 20),
	(val_add, ":oil_string", "str_feast_description"),
	(str_store_string, s8, ":oil_string"),
	(str_store_string, s9, "str_s9_of_oil_which_we_shall_require_to_light_the_lamps_the_amount_is_s8"),
	
	(store_mul, ":food_amount_cap", ":food_amount", 8),
	(store_add, ":total", ":food_amount", ":food_variety"),
	(val_mul, ":total", 2), #x4
	(val_add, ":total", ":drink_variety"),
	(val_add, ":total", ":drink_amount"), #x6
	(val_add, ":total", ":spice_amount"), #x7
	(val_add, ":total", ":oil_amount"), #x8
	(val_min, ":total", ":food_amount_cap"),
	(val_div, ":total", 8),
	(val_clamp, ":total", 1, 101),
	(store_div, ":total_string", ":total", 20),
	(val_add, ":total_string", "str_feast_description"),
	(str_store_string, s8, ":total_string"),
	(str_store_string, s9, "str_s9_overall_our_table_will_be_considered_s8"),
	
	(assign, reg0, ":total"), #zero to 100
	
	
	
	(try_begin),
		(eq, ":consume_items", 1),
		
		(assign, ":num_of_servings_to_serve", ":num_servings"),
		(try_for_range, ":unused", 0, 1999),
			(gt, ":num_of_servings_to_serve", 0),
			
			(try_for_range, ":item", trade_goods_begin, trade_goods_end),
				(item_set_slot, ":item", slot_item_is_checked, 0),
			(try_end),
			
			(troop_get_inventory_capacity, ":inv_size", ":householder"),
			(try_for_range, ":i_slot", 0, ":inv_size"),
				(troop_get_inventory_slot, ":item", ":householder", ":i_slot"),
				(this_or_next|eq, ":item", "itm_spice"),
				(this_or_next|eq, ":item", "itm_oil"),
				(this_or_next|eq, ":item", "itm_wine"),
				(this_or_next|eq, ":item", "itm_ale"),
					(is_between, ":item",  food_begin, food_end),
				(item_slot_eq, ":item", slot_item_is_checked, 0),
				(troop_inventory_slot_get_item_amount, ":cur_amount", ":householder", ":i_slot"),
				(gt, ":cur_amount", 0),
				
				(val_sub, ":cur_amount", 1),
				(troop_inventory_slot_set_item_amount, ":householder", ":i_slot", ":cur_amount"),
				(val_sub, ":num_of_servings_to_serve", 1),
				(item_set_slot, ":item", slot_item_is_checked, 1),
			(try_end),
		(try_end),
	(try_end),
	]),
	("faction_get_adjective_to_s10", 
	[
	(store_script_param, ":faction_no", 1),

	(try_begin),
		(eq, ":faction_no", "fac_player_faction"),
		(assign, ":faction_no", "$players_kingdom"),
	(try_end),
	
	
	(try_begin),
		(eq, ":faction_no", "fac_player_supporters_faction"),
		(str_store_string, s10, "str_rebel"),
	(else_try),	
		(this_or_next|eq, ":faction_no", "fac_outlaws"),
		(this_or_next|eq, ":faction_no", "fac_woku_pirates"),
		(this_or_next|eq, ":faction_no", "fac_shinano_rebels"),
			(eq, ":faction_no", "fac_deserters"),
		(str_store_string, s10, "str_bandit"),	
	(else_try),
		(faction_get_slot, ":adjective_string", ":faction_no", slot_faction_adjective),
		(str_store_string, s10, ":adjective_string"),
	(try_end),			
	]),
	("setup_tavern_attacker", 
	[
	  (store_script_param, ":cur_entry", 1),
	  	  
	  (try_begin),
	    (neg|troop_slot_eq, "trp_hired_assassin", slot_troop_cur_center, "$g_encountered_party"),
	    (troop_slot_eq, "trp_belligerent_drunk", slot_troop_cur_center, "$g_encountered_party"),
	    (set_visitor, ":cur_entry", "trp_belligerent_drunk"),
	  (try_end),
	  
	  (try_begin),
	    (troop_slot_eq, "trp_hired_assassin", slot_troop_cur_center, "$g_encountered_party"),
	    (set_visitor, ":cur_entry", "trp_hired_assassin"),
	  (try_end),
	]),
	("activate_tavern_attackers", 
	[
	  (set_party_battle_mode),
	  (try_for_agents, ":cur_agent"),
	    (agent_get_troop_id, ":cur_agent_troop", ":cur_agent"),
	    (this_or_next|eq, ":cur_agent_troop", "trp_fugitive"),
	    (this_or_next|eq, ":cur_agent_troop", "trp_belligerent_drunk"),
	    (eq, ":cur_agent_troop", "trp_hired_assassin"),
	    (agent_set_team, ":cur_agent", 1),
	    (assign, "$g_main_attacker_agent", ":cur_agent"),
	    (agent_ai_set_aggressiveness, ":cur_agent", 199),
	  (try_end),
	]),
	("deactivate_tavern_attackers", 
	[
	  (finish_party_battle_mode),
	  (try_for_agents, ":cur_agent"),
	    (agent_get_troop_id, ":cur_agent_troop", ":cur_agent"),
	    (this_or_next|eq, ":cur_agent_troop", "trp_fugitive"),
	    (this_or_next|eq, ":cur_agent_troop", "trp_belligerent_drunk"),
	    (eq, ":cur_agent_troop", "trp_hired_assassin"),
	    (agent_set_team, ":cur_agent", 0),
	    (agent_ai_set_aggressiveness, ":cur_agent", 0),
	  (try_end),
	]),
	("activate_town_guard", 
	[
	  (set_party_battle_mode),
	  #(get_player_agent_no, ":player_agent"),
	  #(agent_get_team, ":player_team", ":player_agent"),
	  
	  (try_for_agents, ":cur_agent"), 
	    (agent_get_troop_id, ":troop_type", ":cur_agent"),
	    (is_between, ":troop_type", "trp_gekokujo_uesugi_villager", "trp_looter"),
        (agent_set_team, ":cur_agent", 1),
        #(team_give_order, 1, grc_everyone, mordr_charge), - for some reason, this freezes everyone if the player is not yet spawned
		#(try_begin),
		#	(eq, "$g_main_attacker_agent", 0),
		#	(assign, "$g_main_attacker_agent", ":cur_agent"),
		#(try_end),
	(else_try),	
		(this_or_next|is_between, ":cur_agent", walkers_begin, walkers_end),
		(is_between, ":cur_agent", armor_merchants_begin, mayors_end),
		
		(agent_clear_scripted_mode, ":cur_agent"),
		(agent_set_team, ":cur_agent", 2),
	(try_end),
	]),
	#this determines whether or not a lord is thrown into a dungeon by his captor, or is kept out on parole
	#Not currently used (ie, it always fails)
	("cf_prisoner_offered_parole", 
	[
	  (store_script_param, ":prisoner", 1),
	  
	  (eq, 1, 0), #disabled, this will always return false
	  
	  (troop_get_slot, ":captor_party", ":prisoner", slot_troop_prisoner_of_party),
	  (party_is_active, ":captor_party"),
	  (is_between, ":captor_party", walled_centers_begin, walled_centers_end),
	  (party_get_slot, ":captor", ":captor_party", slot_town_lord),
	  
	  (troop_get_slot, ":prisoner_rep", ":prisoner", slot_lord_reputation_type),
	  (troop_get_slot, ":captor_rep", ":captor", slot_lord_reputation_type),
	  
	  (neq, ":prisoner_rep", lrep_debauched),
	  (neq, ":captor_rep", lrep_debauched),
	  (neq, ":captor_rep", lrep_quarrelsome),
	
     #Prisoner is a noble, or lord is goodnatured
    (this_or_next|eq, ":captor_rep", lrep_goodnatured),
    (this_or_next|troop_slot_eq, ":prisoner", slot_troop_occupation, slto_kingdom_hero),
    (troop_slot_eq, ":prisoner", slot_troop_occupation, slto_kingdom_lady),
	
	(call_script, "script_troop_get_relation_with_troop", ":captor", ":prisoner"),
##	(display_message, "str_relation_of_prisoner_with_captor_is_reg0"),
	(ge, reg0, -10),		
	]),
##diplomacy start+ (documentation only)
#
# Registers changed:
#   reg4 - (sometimes, cheat only) current troop rumor of :object_1 or :object_2
#
# String registers changed:
#    s10 - speaker name
#    s11 - the third argument
#     s1 - the date
#     s5 - str_s10_said_on_s1_s11__
#     s3 - (sometimes, cheat only) the troop name of :object_1 or :object_2
#
#
# Diplomacy+ mod change:
# - Use reg4 to contain the gender of the subject of a rumor string
##diplomacy end+ (documentation only)
	("add_rumor_string_to_troop_notes", #parameters from dialog
	[
      (store_script_param, ":object_1", 1),
      (store_script_param, ":object_2", 2),	
      (store_script_param, ":string", 3),	
	
      (str_store_troop_name, s10, "$g_talk_troop"),
      (str_store_string_reg, s11, ":string"),
	
      (store_current_hours, ":hours"),
      (call_script, "script_game_get_date_text", 0, ":hours"),
	
      (str_store_string, s5, "str_s10_said_on_s1_s11__"),

      (try_begin),
        (is_between, ":object_1", active_npcs_begin, kingdom_ladies_end),
        (troop_get_slot, ":current_rumor_note", ":object_1", slot_troop_current_rumor),
        (val_add, ":current_rumor_note", 1),
        (try_begin),
          (neg|is_between, ":current_rumor_note", 3, 16),
          (assign, ":current_rumor_note", 3),
        (try_end),
        (troop_set_slot, ":object_1", slot_troop_current_rumor, ":current_rumor_note"),
		
        (add_troop_note_from_sreg, ":object_1", ":current_rumor_note", s5, 0), #troop, note slot, string, show       
		
        (try_begin),
          (eq, "$cheat_mode", 1),
          (str_store_troop_name, s3, ":object_1"),
          (assign, reg4, ":current_rumor_note"),
          (display_message, "str_rumor_note_to_s3s_slot_reg4_s5"),
        (try_end),
      (try_end),
      
      (try_begin),
        (is_between, ":object_2", active_npcs_begin, kingdom_ladies_end),
        (troop_get_slot, ":current_rumor_note", ":object_2", slot_troop_current_rumor),
        (val_add, ":current_rumor_note", 1),
        (try_begin),
          (neg|is_between, ":current_rumor_note", 3, 16),
          (assign, ":current_rumor_note", 3),
        (try_end),
        (troop_set_slot, ":object_2", slot_troop_current_rumor, ":current_rumor_note"),
        
        (add_troop_note_from_sreg, ":object_2", ":current_rumor_note", s5, 0), #troop, note slot, string, show        
        
        (try_begin),
          (eq, "$cheat_mode", 1),
          (str_store_troop_name, s3, ":object_2"),
          (assign, reg4, ":current_rumor_note"),
          (display_message, "str_rumor_note_to_s3s_slot_reg4_s5"),
        (try_end),
      (try_end),	
	]),
	("character_can_wed_character", #empty now, but might want to add mid-game
	[
	]),
	("troop_change_career", #empty now, but might want to add mid-game
	[
	]),
	("lord_find_alternative_faction", #Also, make it so that lords will try to keep at least one center unassigned
	[
	  (store_script_param, ":troop_no", 1),
	  (store_faction_of_troop, ":orig_faction", ":troop_no"),

	  (assign, ":new_faction", -1),
	  (assign, ":score_to_beat", -5),
	  ##diplomacy start+
	  (troop_get_slot, ":true_original_faction", ":troop_no", slot_troop_original_faction),#not necessarily ":orig_faction"
	  (try_begin),
	     (neg|is_between, ":true_original_faction", kingdoms_begin, kingdoms_end),
	     (troop_get_slot, reg0, ":troop_no", slot_troop_home),
	     (is_between, reg0, centers_begin, centers_end),
	     (party_get_slot, reg0, reg0, slot_center_original_faction),
	     (gt, reg0, 0),
	     (assign, ":true_original_faction", reg0),
	  (try_end),
	  (assign, ":original_culture", -2),
	  (try_begin),
	     (gt, ":true_original_faction", 0),
		 (faction_get_slot, ":original_culture", ":true_original_faction", slot_faction_culture),
		 (lt, ":original_culture", 1),
		 (assign, ":original_culture", ":true_original_faction"),
	  (try_end),
	  ##diplomacy end+

	  #Factions with an available center
	  (try_for_range, ":center_no", centers_begin, centers_end),
	    (this_or_next|party_slot_eq, ":center_no", slot_town_lord, stl_unassigned),
	    (party_slot_eq, ":center_no", slot_town_lord, stl_rejected_by_player),
	    (store_faction_of_party, ":center_faction", ":center_no"),
	    ##diplomacy start+ In Warband 1.142 / 1.143, this variable was added.
	    #To make certain kinds of mistakes or saved-game issues less likely,
	    #instead of checking for value 1 I'll check if the value matches the troop.
	    (this_or_next|eq, "$g_give_advantage_to_original_faction", ":troop_no"),
	    ##diplomacy end+
	    (neq, ":center_faction", ":orig_faction"),
	    (faction_get_slot, ":liege", ":center_faction", slot_faction_leader),
	    (this_or_next|neq, ":liege", "trp_player"),
	    (ge, "$player_right_to_rule", 25),
	    (call_script, "script_troop_get_relation_with_troop", ":troop_no", ":liege"),
	    (assign, ":liege_relation", reg0),

		##diplomacy start+
		(try_begin),
			(ge, "$g_dplmc_ai_changes", DPLMC_AI_CHANGES_LOW),
			#If behavioral changes are enabled, bias heavily towards joining the
			#faction that contains your home (if you have one), or that has the
			#greatest cultural similarity.
			(ge, reg0, 0),
			(try_begin),
				(this_or_next|troop_slot_eq, ":troop_no", slot_troop_original_faction, ":center_faction"),
				(this_or_next|party_slot_eq, ":center_no", dplmc_slot_center_original_lord, ":troop_no"),
					(troop_slot_eq, ":troop_no", slot_troop_home, ":center_no"),
				(val_add, ":liege_relation", 20),
			(else_try),
				(gt, ":true_original_faction", 0),
				(party_slot_eq, ":center_no", slot_center_original_faction, ":true_original_faction"),
				(val_add, ":liege_relation", 5),
			(else_try),
				(gt, ":original_culture", 0),
				(faction_slot_eq, ":center_faction", slot_faction_culture, ":original_culture"),
				(val_add, ":liege_relation", 5),
			(try_end),
		(try_end),
		##diplomacy end+

	    (gt, ":liege_relation", ":score_to_beat"),
	    (assign, ":new_faction", ":center_faction"),
	    (assign, ":score_to_beat", ":liege_relation"),
	  (try_end),

	  #Factions without an available center
	  (try_begin),
	    (eq, ":new_faction", -1),
	    (assign, ":score_to_beat", 0),
	     #diplomacy start+
	     #If AI changes are explicitly enabled, slightly ease the requirements for entry.
	     (try_begin),
		    (ge, "$g_dplmc_ai_changes", DPLMC_AI_CHANGES_MEDIUM),
	        (assign, ":score_to_beat", -5),
	     (try_end),
		 (store_add, ":min_acceptable_score", ":score_to_beat", 1),#used below
	     ##diplomacy end+

	    (try_for_range, ":kingdom", kingdoms_begin, kingdoms_end),
	      (faction_slot_eq, ":kingdom", slot_faction_state, sfs_active),
	      (faction_get_slot, ":liege", ":kingdom", slot_faction_leader),
	      (call_script, "script_troop_get_relation_with_troop", ":troop_no", ":liege"),
	      (assign, ":liege_relation", reg0),

		  ##diplomacy start+
		  (try_begin),
				#In Warband 1.142 / 1.143, this variable was added.
				#To make certain kinds of mistakes or saved-game issues less likely,
				#instead of checking for value 1 I'll check if the value matches the troop.
				(this_or_next|eq, "$g_give_advantage_to_original_faction", ":troop_no"),
				(neq, ":kingdom", ":orig_faction"),
				(ge, "$g_dplmc_ai_changes", DPLMC_AI_CHANGES_LOW),
				#If behavioral changes are enabled, base your decision in part
				#on how many friends you have in the faction.
				(ge, reg0, ":min_acceptable_score"),
				(try_for_range, ":lord", heroes_begin, heroes_end),
					(troop_slot_eq, ":lord", slot_troop_occupation, slto_kingdom_hero),
					(neq, ":lord", ":troop_no"),
					(neq, ":lord", ":liege"),
					(store_faction_of_troop, ":lord_faction", ":lord"),
					(eq, ":lord_faction", ":kingdom"),
					(call_script, "script_troop_get_relation_with_troop", ":troop_no", ":lord"),
					(try_begin),
						(ge, reg0, 20),
						(val_add, ":liege_relation", 1),
					(else_try),
						(lt, reg0, -19),
						(val_sub, ":liege_relation", 1),
					(try_end),
				(try_end),
				#Also give a bonus towards rejoining the lord's original faction.
				#if it isn't the one the lord has just left.
				(try_begin),
					(eq, ":true_original_faction", ":kingdom"),
					(val_add, ":liege_relation", 5),
				(else_try),
					#Not the same but similar
					(gt, ":original_culture", 0),
					(faction_slot_eq, ":kingdom", slot_faction_culture, ":original_culture"),
					(val_add, ":liege_relation", 2),
				(try_end),
				#The next bit is to prevent this change from increasing the number of
				#lords who find all kingdoms unacceptable.
				(val_max, ":liege_relation", ":min_acceptable_score"),
		  (try_end),
		  ##diplomacy end+

	      (gt, ":liege_relation", ":score_to_beat"),

	      (assign, ":new_faction", ":kingdom"),
	      (assign, ":score_to_beat", ":liege_relation"),
	    (try_end),
	  (try_end),

	  (assign, reg0, ":new_faction"),
	]),
	("set_up_duel_with_troop", #now the setup is handled through the menu
	[
	  (store_script_param, "$g_duel_troop", 1),	
	  (assign, "$g_start_arena_fight_at_nearest_town", 1),
	  (try_begin),
	    (eq, "$g_start_arena_fight_at_nearest_town", 1),
	  (try_end),  
	  (unlock_achievement, ACHIEVEMENT_PUGNACIOUS_D),
      (jump_to_menu, "mnu_arena_duel_fight"),
	  (finish_mission),

	]),
	("test_player_for_career_and_marriage_incompatability", #empty now, but might want to add mid-game
	[
	#Married to a lord of one faction, while fighting for another
	#Married to one lord while holding a stipend from the king	
	]),
 	(
	"faction_last_reconnoitered_center", #This is called from within decide_faction_ai, or from 
	[
		(store_script_param, ":faction_no", 1), 
		(store_script_param, ":center_no", 2), 
		
		(store_sub, ":faction_recce_slot", ":faction_no", kingdoms_begin),
		(val_add, ":faction_recce_slot", slot_center_last_reconnoitered_by_faction_time),
		(store_current_hours, ":hours_since_last_recon"),
		(party_get_slot, ":last_recon_time", ":center_no", ":faction_recce_slot"), 
		
		(try_begin),
			(lt, ":last_recon_time", 1),
			(assign, ":hours_since_last_recon", 1000),
		(else_try),	
			(val_sub, ":hours_since_last_recon", ":last_recon_time"),
		(try_end),
 
		(assign, reg0, ":hours_since_last_recon"),
		(assign, reg1, ":last_recon_time"),		
	]),
 	(
	"reduce_exact_number_to_estimate",
	#This is used to simulate limited intelligence
	#It is roughly analogous to the descriptive strings which the player will receive from alarms
	#Information is presumed to be accurate for four days
	#This is obviously cheating for the AI, as the AI will have exact info for four days, and no info at all after that.
	#It would be fairly easy to log the strength at a center when it is scouted, if we want, but I have not done that at this point,
	#The AI also has a hive mind -- ie, each party knows what its allies are thinking. In this, AI factions have an advantage over the player
	#It would be a simple matter to create a set of arrays in which each party's knowledge is individually updated, but that would also take up a lot of data space
	
	[
		(store_script_param, ":exact_number", 1), 
		
		(try_begin),
			(lt, ":exact_number", 500),
			(assign, ":estimate", 0),
		(else_try),
			(lt, ":exact_number", 1000),
			(assign, ":estimate", 750),
		(else_try),
			(lt, ":exact_number", 2000),
			(assign, ":estimate", 1500),
		(else_try),
			(lt, ":exact_number", 4000),
			(assign, ":estimate", 3000),
		(else_try),
			(lt, ":exact_number", 8000),
			(assign, ":estimate", 6000),
		(else_try),
			(lt, ":exact_number", 16000),
			(assign, ":estimate", 12000),
		(else_try),
			(assign, ":estimate", 24000),
		(try_end),
		##diplomacy start+
		#This currently isn't used anywhere, but modify it if we're thinking about changing that.
		#Take into account campaign AI difficulty -- assume that the difference is either a good
		#spy network or intelligent inference.
		(game_get_reduce_campaign_ai, reg0),
		(try_begin),
			(lt, reg0, 1),#Hard mode
			(assign, ":estimate", ":exact_number"),
		(else_try),
			(eq, reg0, 1),#Medium Mode
			(val_add, ":estimate", ":exact_number"),
			(val_div, ":estimate", 2),
		(try_end),
		##diplomacy end+

		(assign, reg0, ":estimate"),		
	]),
   #script_calculate_castle_prosperities_by_using_its_villages
 	(
	"calculate_castle_prosperities_by_using_its_villages", #This is called from within decide_faction_ai, or from 
	[	  	
	  (try_for_range, ":cur_castle", castles_begin, castles_end),	  
	    (assign, ":total_prosperity", 0),
	    (assign, ":total_villages", 0),
	    
	    (try_for_range, ":cur_village", villages_begin, villages_end),	  
	      (party_get_slot, ":bound_center", ":cur_village", slot_village_bound_center),
	      (eq, ":cur_castle", ":bound_center"),
	      
	      (party_get_slot, ":village_prosperity", ":cur_village", slot_town_prosperity),
	      
	      (val_add, ":total_prosperity", ":village_prosperity"),
	      (val_add, ":total_villages", 1),
	    (try_end),
	    
	    (try_begin),
	      (store_div, ":castle_prosperity", ":total_prosperity", ":total_villages"),
	    (else_try),  
	      (assign, ":castle_prosperity", 50),
	    (try_end),
	    
	    (party_set_slot, ":cur_castle", slot_town_prosperity, ":castle_prosperity"),
	  (try_end),
	]),
   #script_initialize_tavern_variables
   (
   "initialize_tavern_variables",
   [
     (assign, "$g_main_attacker_agent", 0),
     (assign, "$g_attacker_drawn_weapon", 0),
     (assign, "$g_start_belligerent_drunk_fight", 0),
     (assign, "$g_start_hired_assassin_fight", 0),
     (assign, "$g_belligerent_drunk_leaving", 0),   
   ]),
   #script_prepare_alley_to_fight
   (
   "prepare_alley_to_fight",
   [
     (party_get_slot, ":scene_no", "$current_town", slot_town_alley),
     
     #(store_faction_of_party, ":faction_no", "$current_town"),     
     
     (modify_visitors_at_site, ":scene_no"),
     
     (reset_visitors),
     (set_visitor, 0, "trp_player"),
     
     #(try_begin),
     #  (eq, ":faction_no", "fac_kingdom_1"), #swadian
     #  (assign, ":bandit_troop", "trp_seto_pirate"),
     #(else_try),
     #  (eq, ":faction_no", "fac_kingdom_2"), #vaegir
     #  (assign, ":bandit_troop", "trp_kanto_rebel"),
     #(else_try),
     #  (eq, ":faction_no", "fac_kingdom_3"), #khergit
     #  (assign, ":bandit_troop", "trp_woku_pirate"),
     #(else_try),
     #  (eq, ":faction_no", "fac_kingdom_4"), #nord
     #  (assign, ":bandit_troop", "trp_kinai_rebel"),
     #(else_try),
     #  (eq, ":faction_no", "fac_kingdom_5"), #rhodok
     #  (assign, ":bandit_troop", "trp_shinano_rebel"),
     #(else_try),
     #  (eq, ":faction_no", "fac_kingdom_6"), #sarradin
     #  (assign, ":bandit_troop", "trp_northern_raider"),
     #(try_end),  
               
     #(set_visitor, 3, ":bandit_troop"),
     (set_visitor, 3, "trp_bandit"),

     (assign, "$talked_with_merchant", 0),
     (set_jump_mission, "mt_alley_fight"),
     (jump_to_scene, ":scene_no"),
     (change_screen_mission),         
   ]),
   #script_prepare_town_to_fight
   (
   "prepare_town_to_fight",
   [
     (str_store_party_name_link, s9, "$g_starting_town"),
     (str_store_string, s2, "str_save_town_from_bandits"),        
     (call_script, "script_start_quest", "qst_save_town_from_bandits", "$g_talk_troop"),
  
     (assign, "$g_mt_mode", tcm_default),
     #(store_faction_of_party, ":town_faction", "$current_town"),
     #(faction_get_slot, ":tier_2_troop", ":town_faction", slot_faction_tier_3_troop),
     #(faction_get_slot, ":tier_3_troop", ":town_faction", slot_faction_tier_3_troop),
     #(faction_get_slot, ":tier_4_troop", ":town_faction", slot_faction_tier_4_troop),
     
     (party_get_slot, ":town_scene", "$current_town", slot_town_center),
     (modify_visitors_at_site, ":town_scene"),
     (reset_visitors),
    
     #people spawned at #32, #33, #34, #35, #36, #37, #38 and #39 are town walkers.
     (try_begin),
       #(eq, "$town_nighttime", 0),
       (try_for_range, ":walker_no", 0, num_town_walkers),
         (store_add, ":troop_slot", slot_center_walker_0_troop, ":walker_no"),
         (party_get_slot, ":walker_troop_id", "$current_town", ":troop_slot"),
         (gt, ":walker_troop_id", 0),                        
         (store_add, ":entry_no", town_walker_entries_start, ":walker_no"),
         (set_visitor, ":entry_no", ":walker_troop_id"),
       (try_end),  
     (try_end),  

     #guards will be spawned at #25, #26 and #27 
	 #gekokujo 3.0 starting quest give horenbo some weapons and armor
	 (troop_add_item,"trp_relative_of_merchant","itm_gekokujo_naginata_2"),
	 (troop_add_item,"trp_relative_of_merchant","itm_gekokujo_kebiki_1"),
	 (troop_add_item,"trp_relative_of_merchant","itm_gekokujo_shino_suneate_1"),
	 (troop_equip_items,"trp_relative_of_merchant"),
	 
	 #gekokujo 3.0 starting quest make horenbo and ikko-ikki spawn as reinforcements
	 #change the ikko-ikki spawns 23, 25, and 26 rather than 25, 26, 27
     (set_visitors, 23, "trp_relative_of_merchant", 1),
     (set_visitors, 25, "trp_gekokujo_ikko_naginata_monk", 1),
     (set_visitors, 26, "trp_gekokujo_ikko_veteran_naginata_monk", 1),

     (store_faction_of_party, ":starting_town_faction", "$g_starting_town"),    
     (try_begin),
       (eq, ":starting_town_faction", "fac_kingdom_11"),
       (assign, ":troop_of_merchant", "trp_tsu_merchant"),
       (assign, ":troop_of_bandit_1", "trp_generic_ashigaru"),
       (assign, ":troop_of_bandit_2", "trp_generic_jizamurai"),
     (else_try),  
       (eq, ":starting_town_faction", "fac_kingdom_10"),
       (assign, ":troop_of_merchant", "trp_hirosaki_merchant"),
       (assign, ":troop_of_bandit_1", "trp_generic_ashigaru"),
       (assign, ":troop_of_bandit_2", "trp_generic_jizamurai"),
     (else_try),                   
       (eq, ":starting_town_faction", "fac_kingdom_1"),
       (assign, ":troop_of_merchant", "trp_niigata_merchant"),
       (assign, ":troop_of_bandit_1", "trp_generic_ashigaru"),
       (assign, ":troop_of_bandit_2", "trp_generic_jizamurai"),
     (else_try),  
       (eq, ":starting_town_faction", "fac_kingdom_13"),
       (assign, ":troop_of_merchant", "trp_edo_merchant"),
       (assign, ":troop_of_bandit_1", "trp_generic_ashigaru"),
       (assign, ":troop_of_bandit_2", "trp_generic_jizamurai"),
     (else_try),  
       (eq, ":starting_town_faction", "fac_kingdom_7"),
       (assign, ":troop_of_merchant", "trp_sakai_merchant"),
       (assign, ":troop_of_bandit_1", "trp_generic_ashigaru"),
       (assign, ":troop_of_bandit_2", "trp_generic_jizamurai"),
     (else_try),  
       (eq, ":starting_town_faction", "fac_kingdom_9"),
       (assign, ":troop_of_merchant", "trp_hakata_merchant"),
       (assign, ":troop_of_bandit_1", "trp_generic_ashigaru"),
       (assign, ":troop_of_bandit_2", "trp_generic_jizamurai"),
     (try_end),
     (str_store_troop_name, s10, ":troop_of_merchant"),
    
     (set_visitors, 10, ":troop_of_bandit_2", 1),
     #(set_visitors, 11, ":troop_of_bandit_2", 1),
     (set_visitors, 12, ":troop_of_bandit_2", 1),
    
     #(set_visitors, 24, ":troop_of_bandit_1", 1),
     (set_visitors, 2, ":troop_of_bandit_1", 2),
     (set_visitors, 4, ":troop_of_bandit_1", 1),
     #(set_visitors, 5, ":troop_of_bandit_1", 2),
     (set_visitors, 6, ":troop_of_bandit_1", 1),
     #(set_visitors, 7, ":troop_of_bandit_1", 1),
	 
     (set_visitors, 3, ":troop_of_merchant", 1),    
    
     (set_jump_mission,"mt_town_fight"),
     (jump_to_scene, ":town_scene"),
     (change_screen_mission),   
   ]),
   (
   "change_player_right_to_rule",
   [
     (store_script_param_1, ":right_to_rule_dif"),
     (val_add, "$player_right_to_rule", ":right_to_rule_dif"),
     (val_clamp, "$player_right_to_rule", 0, 100),
     (try_begin),
       (gt, ":right_to_rule_dif", 0),
       (display_message, "@You gain right to rule."),
     (else_try),
       (lt, ":right_to_rule_dif", 0),
       (display_message, "@You lose right to rule."),
     (try_end),
   ]),
   ("indict_lord_for_treason",#originally included in simple_triggers. Needed to be moved here to allow player to indict
   [
    (store_script_param, ":troop_no", 1),
    (store_script_param, ":faction", 2),
	
	##diplomacy start+ use gender script
	#(troop_get_type, reg4, ":troop_no"),
	(assign, ":save_reg0", reg0),
	(assign, ":save_reg3", reg3),
	(assign, ":save_reg4", reg4),
	##diplomacy end+
	  
	(try_for_range, ":center", centers_begin, centers_end), #transfer properties to liege
		(party_slot_eq, ":center", slot_town_lord, ":troop_no"),
		(party_set_slot, ":center", slot_town_lord, stl_unassigned), 
	(try_end),
	
	(faction_get_slot, ":faction_leader", ":faction", slot_faction_leader),
	(call_script, "script_troop_get_relation_with_troop", ":troop_no", ":faction_leader"),
	(assign, ":liege_to_lord_relation", reg0),
	(store_sub, ":base_relation_modifier", -150, ":liege_to_lord_relation"), 
	(val_div, ":base_relation_modifier", 40),#-1 at -100, -2 at -70, -3 at -30,etc. 
	(val_min, ":base_relation_modifier", -1),

	#Indictments, cont: Influence relations
	##diplomacy start+ Alter to include promoted ladies
	##OLD:
	#(try_for_range, ":active_npc", active_npcs_begin, active_npcs_end), #this effects all lords in all factions
	##NEW:
	(try_for_range, ":active_npc", heroes_begin, heroes_end), #this effects all lords in all factions
		(this_or_next|is_between, ":active_npc", active_npcs_begin, active_npcs_end),
			(troop_slot_eq, ":active_npc", slot_troop_occupation, slto_kingdom_hero),
	##diplomacy end+
		(store_faction_of_troop, ":active_npc_faction", ":active_npc"),
		(eq, ":faction", ":active_npc_faction"),

		(call_script, "script_troop_get_family_relation_to_troop", ":troop_no", ":active_npc"),
		(assign, ":family_relation", reg0),

		##diplomacy start+
		(val_max, ":family_relation", 0),
		#Take into account friendship or enmity
		(call_script, "script_troop_get_relation_with_troop", ":troop_no", ":faction_leader"),
		(assign, ":liking_relation", reg0),
		(try_begin),
			(ge, ":liking_relation", 20),
			(store_div, reg0, ":liking_relation", 20),
			(val_add, ":family_relation", reg0),
		(else_try),
			(lt, ":liking_relation", 0),
			(store_div, reg0, ":liking_relation", 20),
			(val_sub, reg0, 1),
			(val_add, ":family_relation", reg0),
		(try_end),
		(store_random_in_range, reg0, 0, 3),#+0, +1, or +2 (because below we divide by three...)
		(val_add, ":family_relation", reg0),
		(assign, reg0, ":family_relation"),
		##diplomacy end+
		(assign, ":relation_modifier", ":base_relation_modifier"),
		(try_begin),
			##diplomacy start+
			#(gt, ":family_relation", 1),##OLD
			(neq, ":family_relation", 0),##NEW (allow lessening penalty for hated characters)
			##diplomacy end+
			(store_div, ":family_multiplier", reg0, 3),
			(val_sub, ":relation_modifier", ":family_multiplier"),
		(try_end),

		(lt, ":relation_modifier", 0),
		
		(call_script, "script_troop_change_relation_with_troop", ":faction_leader", ":active_npc", ":relation_modifier"),
		(val_add, "$total_indictment_changes", ":relation_modifier"),
		(try_begin),
			(eq, "$cheat_mode", 1),
			(str_store_troop_name, s17, ":active_npc"),
			(str_store_troop_name, s18, ":faction_leader"),

			(assign, reg3, ":relation_modifier"),
			(display_message, "str_trial_influences_s17s_relation_with_s18_by_reg3"),
		(try_end),
	(try_end),

	#Indictments, cont: Check for other factions
	(assign, ":new_faction", "fac_outlaws"),
	(try_begin),
		(eq, ":troop_no", "trp_player"),
		(assign, ":new_faction", 0), #kicked out of faction
	(else_try),	
		(call_script, "script_lord_find_alternative_faction", ":troop_no"),		
		(assign, ":new_faction", reg0),
	(try_end),
	  
	#Indictments, cont: Finalize where the lord goes
	(try_begin),
		(is_between, ":new_faction", kingdoms_begin, kingdoms_end),
				
		(try_begin),
			(ge, "$cheat_mode", 1),
			(str_store_troop_name, s4, ":troop_no"),
			(display_message, "@{!}DEBUG - {s4} faction changed in indictment"), 
		(try_end),		
		
		(call_script, "script_change_troop_faction", ":troop_no", ":new_faction"),
		(try_begin), #new-begin
		  (neq, ":new_faction", "fac_player_supporters_faction"),
		  (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_inactive), 
		  (troop_set_slot, ":troop_no", slot_troop_occupation, slto_kingdom_hero), 
		(try_end), #new-end
		(str_store_faction_name, s10, ":new_faction"),
		(str_store_string, s11, "str_with_the_s10"),
	(else_try),
		(neq, ":troop_no", "trp_player"),
		##diplomacy start+
		#Set "exile" occupation to differentiate between someone outside of Calradia
		#and an outlaw lord leading a party of bandits.
		(troop_set_slot, ":troop_no", slot_troop_occupation, dplmc_slto_exile),
		##diplomacy end+
		(call_script, "script_change_troop_faction", ":troop_no", "fac_outlaws"),
		(str_store_string, s11, "str_outside_calradia"),
	(else_try),
		(eq, ":troop_no", "trp_player"),
		(call_script, "script_player_leave_faction", 1),
	(try_end),

	#Indictments, cont: Set up string
	(try_begin),
		(eq, ":troop_no", "trp_player"),
		(str_store_string, s9, "str_you_have_been_indicted_for_treason_to_s7_your_properties_have_been_confiscated_and_you_would_be_well_advised_to_flee_for_your_life"),
	(else_try),	
		(str_store_troop_name, s4, ":troop_no"),
		(str_store_faction_name, s5, ":faction"),
		(str_store_troop_name, s6, ":faction_leader"),

		##diplomacy start+
		#(troop_get_type, reg4, ":troop_no"),
		(call_script, "script_dplmc_store_troop_is_female", ":troop_no"),
		(assign, reg4, reg0),
		##diplomacy end+
		(str_store_string, s9, "str_by_order_of_s6_s4_of_the_s5_has_been_indicted_for_treason_the_lord_has_been_stripped_of_all_reg4herhis_properties_and_has_fled_for_reg4herhis_life_he_is_rumored_to_have_gone_into_exile_s11"),
	(try_end),
	##diplomacy start+ important political events should be in the log
	(display_log_message, "@{!}{s9}"),#display_message changed to display_log_message
	##diplomacy end+

	#Indictments, cont: Remove party
	(troop_get_slot, ":led_party", ":troop_no", slot_troop_leaded_party),
	(try_begin),
		(party_is_active, ":led_party"),
		(neq, ":led_party", "p_main_party"),
		(remove_party, ":led_party"),
		(troop_set_slot, ":troop_no", slot_troop_leaded_party, -1),
	(try_end),
				
	(try_begin),
		(eq, "$cheat_mode", 1),
		##diplomacy start+
		(this_or_next|eq, ":faction", "fac_player_supporters_faction"),
		(this_or_next|eq, ":new_faction", "fac_player_supporters_faction"),
		##diplomacy end+
		(this_or_next|eq, ":faction", "$players_kingdom"),
			(eq, ":new_faction", "$players_kingdom"),
		(call_script, "script_add_notification_menu", "mnu_notification_treason_indictment", ":troop_no", ":faction"),
	(try_end),
	##diplomacy start+
	(assign, reg0, ":save_reg0"),
	(assign, reg3, ":save_reg3"),
	(assign, reg4, ":save_reg4"),
	##diplomacy end+
   ]),
  # script_give_center_to_faction_aux
  # Input: arg1 = center_no, arg2 = faction
  ("give_center_to_faction_while_maintaining_lord",
    [
      (store_script_param_1, ":center_no"),
      (store_script_param_2, ":faction_no"),

      (store_faction_of_party, ":old_faction", ":center_no"),
	  ##diplomacy start+
	  #If the player, previously the head of his own faction, is now joining
	  #an NPC faction, don't reset the "last taken" time or the "ex faction"
	  #slots.
	  (try_begin),
		#Friendly transfer: don't update transfer time or ex-faction
		(eq, ":old_faction", "fac_player_supporters_faction"),
		(eq, ":faction_no", "$players_kingdom"),
	  (else_try),
		#Defection: update transfer time and ex-faction
		(party_set_slot, ":center_no", slot_center_ex_faction, ":old_faction"),
		(store_current_hours, ":cur_hours"),
		(party_set_slot, ":center_no", dplmc_slot_center_last_transfer_time, ":cur_hours"),
	  (try_end),
	  ##diplomacy end+
      (party_set_faction, ":center_no", ":faction_no"),

      (try_begin),
        (party_slot_eq, ":center_no", slot_party_type, spt_village),
        (party_get_slot, ":farmer_party", ":center_no", slot_village_farmer_party),
        (gt, ":farmer_party", 0),
        (party_is_active, ":farmer_party"),
        (party_set_faction, ":farmer_party", ":faction_no"),
      (try_end),

      (call_script, "script_update_faction_notes", ":faction_no"),
      (call_script, "script_update_center_notes", ":center_no"),

      (try_for_range, ":other_center", centers_begin, centers_end),
        (party_slot_eq, ":other_center", slot_village_bound_center, ":center_no"),
        (call_script, "script_give_center_to_faction_while_maintaining_lord", ":other_center", ":faction_no"),
      (try_end),
  ]),
]
