# -*- coding: utf-8 -*-
# module_scripts_core.py -- auto split from module_scripts.py (feature: 游戏核心回调/通用工具)
# entries: 91 (order preserved within this file)
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


scripts_core = [

  #script_game_start:
  # This script is called when a new game is started
  # INPUT: none
  ("game_start",
   [
      (assign, "$gonghe", 0),
      (assign, "$cut_body", 1),
      (assign, "$ym_gatling_purchased", 0),
      (faction_set_slot, "fac_player_supporters_faction", slot_faction_state, sfs_inactive),
      (assign, "$g_player_luck", 200),
      (assign, "$g_player_luck", 200),
      (troop_set_slot, "trp_player", slot_troop_occupation, slto_kingdom_hero),
## Tocan Invasion+ ##	  		  
	  (troop_set_slot, "trp_dark_knight_lord", slot_troop_leaded_party, -1),
      (troop_set_slot, "trp_dark_knight_lord1", slot_troop_leaded_party, -1),
      (troop_set_slot, "trp_dark_knight_lord2", slot_troop_leaded_party, -1),
      (troop_set_slot, "trp_dark_knight_lord3", slot_troop_leaded_party, -1),
      (troop_set_slot, "trp_dark_knight_lord4", slot_troop_leaded_party, -1),
      (troop_set_slot, "trp_dark_knight_lord5", slot_troop_leaded_party, -1),
      (troop_set_slot, "trp_dark_knight_lord6", slot_troop_leaded_party, -1),
      (troop_set_slot, "trp_dark_knight_lord7", slot_troop_leaded_party, -1),
      (troop_set_slot, "trp_dark_knight_lord8", slot_troop_leaded_party, -1),
      (troop_set_slot, "trp_dark_knight_lord9", slot_troop_leaded_party, -1),
      (troop_set_slot, "trp_dark_knight_lord10", slot_troop_leaded_party, -1),
      (troop_set_slot, "trp_dark_knight_lord11", slot_troop_leaded_party, -1),
      (troop_set_slot, "trp_dark_knight_lord12", slot_troop_leaded_party, -1),
      (troop_set_slot, "trp_dark_knight_lord13", slot_troop_leaded_party, -1),
      (troop_set_slot, "trp_dark_knight_lord14", slot_troop_leaded_party, -1),
      (troop_set_slot, "trp_dark_knight_lord15", slot_troop_leaded_party, -1),	
      (troop_set_slot, "trp_dark_knight_lord16", slot_troop_leaded_party, -1),
      (troop_set_slot, "trp_dark_knight_lord17", slot_troop_leaded_party, -1),
      (troop_set_slot, "trp_dark_knight_lord18", slot_troop_leaded_party, -1),
      (troop_set_slot, "trp_dark_knight_lord19", slot_troop_leaded_party, -1),
      (troop_set_slot, "trp_dark_knight_lord20", slot_troop_leaded_party, -1),	 
      (assign,"$invaded",0),
## Dark kinghts Invasion ##
      (store_random_in_range, "$setting_invasion_time", 6800, 14200),
## Dark kinghts Invasion ##
      (faction_set_slot, "fac_dark_knights", slot_faction_state, sfs_inactive),	  
	  (party_set_faction,"p_main_party","fac_player_faction"),
## Tocan Invasion- ##
      (store_random_in_range, ":starting_training_ground", training_grounds_begin, training_grounds_end),
      (party_relocate_near_party, "p_main_party", ":starting_training_ground", 3),
      (str_store_troop_name, s5, "trp_player"),
      (party_set_name, "p_main_party", s5),
      (call_script, "script_update_party_creation_random_limits"),
      (assign, "$g_player_party_icon", -1),	  
	  
	  #Warband changes begin -- set this early 
	  (try_for_range, ":npc", 0, kingdom_ladies_end),
	    (this_or_next|eq, ":npc", "trp_player"),
		(is_between, ":npc", active_npcs_begin, kingdom_ladies_end),
		(troop_set_slot, ":npc", slot_troop_father, -1),
		(troop_set_slot, ":npc", slot_troop_mother, -1),
		(troop_set_slot, ":npc", slot_troop_guardian, -1),
		(troop_set_slot, ":npc", slot_troop_spouse, -1),
		(troop_set_slot, ":npc", slot_troop_betrothed, -1),
        (troop_set_slot, ":npc", slot_troop_prisoner_of_party, -1),		
        (troop_set_slot, ":npc", slot_lady_last_suitor, -1),		
        (troop_set_slot, ":npc", slot_troop_stance_on_faction_issue, -1),		
		
		(store_random_in_range, ":decision_seed", 0, 10000),
        (troop_set_slot, ":npc", slot_troop_set_decision_seed, ":decision_seed"),	#currently not used
        (troop_set_slot, ":npc", slot_troop_temp_decision_seed, ":decision_seed"),	#currently not used, holds for at least 24 hours			
	  (try_end),

	  (assign, "$g_lord_long_term_count", 0),
	  ##diplomacy start+ Clear faction leader/marshall, since 0 is the player
	  (try_for_range, ":faction_no", 0, dplmc_factions_end),
	     (neq, ":faction_no", "fac_player_faction"),
	     (neq, ":faction_no", "fac_player_supporters_faction"),
	     (faction_set_slot, ":faction_no", slot_faction_leader, -1),
	     (faction_set_slot, ":faction_no", slot_faction_marshall, -1),
	  (try_end),
	  ##diplomacy end+

	  (call_script, "script_initialize_banner_info"),
	  (call_script, "script_initialize_item_info"),
	  (call_script, "script_initialize_aristocracy"),
      (call_script, "script_initialize_npcs"),
      (assign, "$disable_npc_complaints", 0),
      #NPC companion changes end
      
      # Setting random feast time
      (try_for_range, ":faction_no", kingdoms_begin, kingdoms_end),
		#gekokujo feasts -- make them more rare
        #(store_random_in_range, ":last_feast_time", 0, 312), #240 + 72
        (store_random_in_range, ":last_feast_time", 0, 1231), #1159 + 72 -- there are 1.45x as many cities and 3.33x as many factions
        (val_mul, ":last_feast_time", -1),
        (faction_set_slot, ":faction_no", slot_faction_last_feast_start_time, ":last_feast_time"),
      (try_end),
      
      # Setting the random town sequence:
      (store_sub, ":num_towns", towns_end, towns_begin),
      (assign, ":num_iterations", ":num_towns"),
      (try_for_range, ":cur_town_no", 0, ":num_towns"),
        (troop_set_slot, "trp_random_town_sequence", ":cur_town_no", -1),
      (try_end),
      (assign, ":cur_town_no", 0),
      (try_for_range, ":unused", 0, ":num_iterations"),
        (store_random_in_range, ":random_no", 0, ":num_towns"),
        (assign, ":is_unique", 1),
        (try_for_range, ":cur_town_no_2", 0, ":num_towns"),
          (troop_slot_eq, "trp_random_town_sequence", ":cur_town_no_2", ":random_no"),
          (assign, ":is_unique", 0),
        (try_end),
        (try_begin),
          (eq, ":is_unique", 1),
          (troop_set_slot, "trp_random_town_sequence", ":cur_town_no", ":random_no"),
          (val_add, ":cur_town_no", 1),
        (else_try),
          (val_add, ":num_iterations", 1),
        (try_end),
      (try_end),
	  
	  # Cultures:
      (faction_set_slot, "fac_culture_1", slot_faction_tier_0_troop, "trp_gekokujo_uesugi_villager"),
      (faction_set_slot, "fac_culture_2", slot_faction_tier_0_troop, "trp_gekokujo_date_villager"),
      (faction_set_slot, "fac_culture_3", slot_faction_tier_0_troop, "trp_gekokujo_oda_villager"),
      (faction_set_slot, "fac_culture_4", slot_faction_tier_0_troop, "trp_gekokujo_mori_villager"),
      (faction_set_slot, "fac_culture_5", slot_faction_tier_0_troop, "trp_gekokujo_takeda_villager"),
      (faction_set_slot, "fac_culture_6", slot_faction_tier_0_troop, "trp_gekokujo_tokugawa_villager"),
      (faction_set_slot, "fac_culture_7", slot_faction_tier_0_troop, "trp_gekokujo_miyoshi_villager"),
      (faction_set_slot, "fac_culture_8", slot_faction_tier_0_troop, "trp_gekokujo_amako_villager"),
      (faction_set_slot, "fac_culture_9", slot_faction_tier_0_troop, "trp_gekokujo_otomo_villager"),
      (faction_set_slot, "fac_culture_10", slot_faction_tier_0_troop, "trp_gekokujo_nanbu_villager"),
      (faction_set_slot, "fac_culture_11", slot_faction_tier_0_troop, "trp_gekokujo_asakura_villager"),
      (faction_set_slot, "fac_culture_12", slot_faction_tier_0_troop, "trp_gekokujo_chosokabe_villager"),
      (faction_set_slot, "fac_culture_13", slot_faction_tier_0_troop, "trp_gekokujo_hojo_villager"),
      (faction_set_slot, "fac_culture_14", slot_faction_tier_0_troop, "trp_gekokujo_mogami_villager"),
      (faction_set_slot, "fac_culture_15", slot_faction_tier_0_troop, "trp_gekokujo_shimazu_villager"),
      (faction_set_slot, "fac_culture_16", slot_faction_tier_0_troop, "trp_gekokujo_ryuzoji_villager"),
      (faction_set_slot, "fac_culture_17", slot_faction_tier_0_troop, "trp_gekokujo_satake_villager"),
      (faction_set_slot, "fac_culture_18", slot_faction_tier_0_troop, "trp_gekokujo_satomi_villager"),
      (faction_set_slot, "fac_culture_19", slot_faction_tier_0_troop, "trp_gekokujo_ukita_villager"),
      (faction_set_slot, "fac_culture_20", slot_faction_tier_0_troop, "trp_gekokujo_ikko_villager"),
      (faction_set_slot, "fac_culture_21", slot_faction_tier_0_troop, "trp_ceshi1"),
      (faction_set_slot, "fac_culture_22", slot_faction_tier_0_troop, "trp_ceshi12"),
      (faction_set_slot, "fac_culture_23", slot_faction_tier_0_troop, "trp_ceshi13"),
      (faction_set_slot, "fac_culture_24", slot_faction_tier_0_troop, "trp_ceshi14"),
      (faction_set_slot, "fac_culture_25", slot_faction_tier_0_troop, "trp_ceshi15"),
      (faction_set_slot, "fac_culture_26", slot_faction_tier_0_troop, "trp_ceshi16"),
      (faction_set_slot, "fac_culture_27", slot_faction_tier_0_troop, "trp_ceshi17"),
      (faction_set_slot, "fac_culture_28", slot_faction_tier_0_troop, "trp_zunwangzhishi"),
      (faction_set_slot, "fac_culture_dark_knights", slot_faction_tier_0_troop, "trp_rus_ally"),
	  #gekokujo 3.0 get rid of player culture start
	  ##gekokujo player culture
      #(faction_set_slot, "fac_culture_player", slot_faction_tier_0_troop, "trp_gekokujo_player_villager"),
	  #gekokujo 3.0 get rid of player culture end

      (faction_set_slot, "fac_culture_1", slot_faction_tier_1_troop, "trp_gekokujo_uesugi_jizamurai"),
      (faction_set_slot, "fac_culture_1", slot_faction_tier_2_troop, "trp_gekokujo_uesugi_retainer"),
      (faction_set_slot, "fac_culture_1", slot_faction_tier_3_troop, "trp_gekokujo_uesugi_veteran_retainer"),
      (faction_set_slot, "fac_culture_1", slot_faction_tier_4_troop, "trp_gekokujo_uesugi_officer"),
      (faction_set_slot, "fac_culture_1", slot_faction_tier_5_troop, "trp_gekokujo_uesugi_mounted_officer"),

      (faction_set_slot, "fac_culture_2", slot_faction_tier_1_troop, "trp_gekokujo_date_jizamurai"),
      (faction_set_slot, "fac_culture_2", slot_faction_tier_2_troop, "trp_gekokujo_date_retainer"),
      (faction_set_slot, "fac_culture_2", slot_faction_tier_3_troop, "trp_gekokujo_date_veteran_retainer"),
      (faction_set_slot, "fac_culture_2", slot_faction_tier_4_troop, "trp_gekokujo_date_officer"),
      (faction_set_slot, "fac_culture_2", slot_faction_tier_5_troop, "trp_gekokujo_date_mounted_officer"),

      (faction_set_slot, "fac_culture_3", slot_faction_tier_1_troop, "trp_gekokujo_oda_jizamurai"),
      (faction_set_slot, "fac_culture_3", slot_faction_tier_2_troop, "trp_gekokujo_oda_retainer"),
      (faction_set_slot, "fac_culture_3", slot_faction_tier_3_troop, "trp_gekokujo_oda_veteran_retainer"),
      (faction_set_slot, "fac_culture_3", slot_faction_tier_4_troop, "trp_gekokujo_oda_officer"),
      (faction_set_slot, "fac_culture_3", slot_faction_tier_5_troop, "trp_gekokujo_oda_mounted_officer"),

      (faction_set_slot, "fac_culture_4", slot_faction_tier_1_troop, "trp_gekokujo_mori_jizamurai"),
      (faction_set_slot, "fac_culture_4", slot_faction_tier_2_troop, "trp_gekokujo_mori_retainer"),
      (faction_set_slot, "fac_culture_4", slot_faction_tier_3_troop, "trp_gekokujo_mori_veteran_retainer"),
      (faction_set_slot, "fac_culture_4", slot_faction_tier_4_troop, "trp_gekokujo_mori_officer"),
      (faction_set_slot, "fac_culture_4", slot_faction_tier_5_troop, "trp_gekokujo_mori_mounted_officer"),

      (faction_set_slot, "fac_culture_5", slot_faction_tier_1_troop, "trp_gekokujo_takeda_jizamurai"),
      (faction_set_slot, "fac_culture_5", slot_faction_tier_2_troop, "trp_gekokujo_takeda_retainer"),
      (faction_set_slot, "fac_culture_5", slot_faction_tier_3_troop, "trp_gekokujo_takeda_veteran_retainer"),
      (faction_set_slot, "fac_culture_5", slot_faction_tier_4_troop, "trp_gekokujo_takeda_officer"),
      (faction_set_slot, "fac_culture_5", slot_faction_tier_5_troop, "trp_gekokujo_takeda_mounted_officer"),

      (faction_set_slot, "fac_culture_6", slot_faction_tier_1_troop, "trp_gekokujo_tokugawa_jizamurai"),
      (faction_set_slot, "fac_culture_6", slot_faction_tier_2_troop, "trp_gekokujo_tokugawa_retainer"),
      (faction_set_slot, "fac_culture_6", slot_faction_tier_3_troop, "trp_gekokujo_tokugawa_veteran_retainer"),
      (faction_set_slot, "fac_culture_6", slot_faction_tier_4_troop, "trp_gekokujo_tokugawa_officer"),
      (faction_set_slot, "fac_culture_6", slot_faction_tier_5_troop, "trp_gekokujo_tokugawa_mounted_officer"),

      (faction_set_slot, "fac_culture_7", slot_faction_tier_1_troop, "trp_gekokujo_miyoshi_jizamurai"),
      (faction_set_slot, "fac_culture_7", slot_faction_tier_2_troop, "trp_gekokujo_miyoshi_retainer"),
      (faction_set_slot, "fac_culture_7", slot_faction_tier_3_troop, "trp_gekokujo_miyoshi_veteran_retainer"),
      (faction_set_slot, "fac_culture_7", slot_faction_tier_4_troop, "trp_gekokujo_miyoshi_officer"),
      (faction_set_slot, "fac_culture_7", slot_faction_tier_5_troop, "trp_gekokujo_miyoshi_mounted_officer"),

      (faction_set_slot, "fac_culture_8", slot_faction_tier_1_troop, "trp_gekokujo_amako_jizamurai"),
      (faction_set_slot, "fac_culture_8", slot_faction_tier_2_troop, "trp_gekokujo_amako_retainer"),
      (faction_set_slot, "fac_culture_8", slot_faction_tier_3_troop, "trp_gekokujo_amako_veteran_retainer"),
      (faction_set_slot, "fac_culture_8", slot_faction_tier_4_troop, "trp_gekokujo_amako_officer"),
      (faction_set_slot, "fac_culture_8", slot_faction_tier_5_troop, "trp_gekokujo_amako_mounted_officer"),

      (faction_set_slot, "fac_culture_9", slot_faction_tier_1_troop, "trp_gekokujo_otomo_jizamurai"),
      (faction_set_slot, "fac_culture_9", slot_faction_tier_2_troop, "trp_gekokujo_otomo_retainer"),
      (faction_set_slot, "fac_culture_9", slot_faction_tier_3_troop, "trp_gekokujo_otomo_veteran_retainer"),
      (faction_set_slot, "fac_culture_9", slot_faction_tier_4_troop, "trp_gekokujo_otomo_officer"),
      (faction_set_slot, "fac_culture_9", slot_faction_tier_5_troop, "trp_gekokujo_otomo_mounted_officer"),

      (faction_set_slot, "fac_culture_10", slot_faction_tier_1_troop, "trp_gekokujo_nanbu_jizamurai"),
      (faction_set_slot, "fac_culture_10", slot_faction_tier_2_troop, "trp_gekokujo_nanbu_retainer"),
      (faction_set_slot, "fac_culture_10", slot_faction_tier_3_troop, "trp_gekokujo_nanbu_veteran_retainer"),
      (faction_set_slot, "fac_culture_10", slot_faction_tier_4_troop, "trp_gekokujo_nanbu_officer"),
      (faction_set_slot, "fac_culture_10", slot_faction_tier_5_troop, "trp_gekokujo_nanbu_mounted_officer"),

      (faction_set_slot, "fac_culture_11", slot_faction_tier_1_troop, "trp_gekokujo_asakura_jizamurai"),
      (faction_set_slot, "fac_culture_11", slot_faction_tier_2_troop, "trp_gekokujo_asakura_retainer"),
      (faction_set_slot, "fac_culture_11", slot_faction_tier_3_troop, "trp_gekokujo_asakura_veteran_retainer"),
      (faction_set_slot, "fac_culture_11", slot_faction_tier_4_troop, "trp_gekokujo_asakura_officer"),
      (faction_set_slot, "fac_culture_11", slot_faction_tier_5_troop, "trp_gekokujo_asakura_mounted_officer"),

      (faction_set_slot, "fac_culture_12", slot_faction_tier_1_troop, "trp_gekokujo_chosokabe_jizamurai"),
      (faction_set_slot, "fac_culture_12", slot_faction_tier_2_troop, "trp_gekokujo_chosokabe_retainer"),
      (faction_set_slot, "fac_culture_12", slot_faction_tier_3_troop, "trp_gekokujo_chosokabe_veteran_retainer"),
      (faction_set_slot, "fac_culture_12", slot_faction_tier_4_troop, "trp_gekokujo_chosokabe_officer"),
      (faction_set_slot, "fac_culture_12", slot_faction_tier_5_troop, "trp_gekokujo_chosokabe_mounted_officer"),

      (faction_set_slot, "fac_culture_13", slot_faction_tier_1_troop, "trp_gekokujo_hojo_jizamurai"),
      (faction_set_slot, "fac_culture_13", slot_faction_tier_2_troop, "trp_gekokujo_hojo_retainer"),
      (faction_set_slot, "fac_culture_13", slot_faction_tier_3_troop, "trp_gekokujo_hojo_veteran_retainer"),
      (faction_set_slot, "fac_culture_13", slot_faction_tier_4_troop, "trp_gekokujo_hojo_officer"),
      (faction_set_slot, "fac_culture_13", slot_faction_tier_5_troop, "trp_gekokujo_hojo_mounted_officer"),

      (faction_set_slot, "fac_culture_14", slot_faction_tier_1_troop, "trp_gekokujo_mogami_jizamurai"),
      (faction_set_slot, "fac_culture_14", slot_faction_tier_2_troop, "trp_gekokujo_mogami_retainer"),
      (faction_set_slot, "fac_culture_14", slot_faction_tier_3_troop, "trp_gekokujo_mogami_veteran_retainer"),
      (faction_set_slot, "fac_culture_14", slot_faction_tier_4_troop, "trp_gekokujo_mogami_officer"),
      (faction_set_slot, "fac_culture_14", slot_faction_tier_5_troop, "trp_gekokujo_mogami_mounted_officer"),

      (faction_set_slot, "fac_culture_15", slot_faction_tier_1_troop, "trp_gekokujo_shimazu_jizamurai"),
      (faction_set_slot, "fac_culture_15", slot_faction_tier_2_troop, "trp_gekokujo_shimazu_retainer"),
      (faction_set_slot, "fac_culture_15", slot_faction_tier_3_troop, "trp_gekokujo_shimazu_veteran_retainer"),
      (faction_set_slot, "fac_culture_15", slot_faction_tier_4_troop, "trp_gekokujo_shimazu_officer"),
      (faction_set_slot, "fac_culture_15", slot_faction_tier_5_troop, "trp_gekokujo_shimazu_mounted_officer"),

      (faction_set_slot, "fac_culture_16", slot_faction_tier_1_troop, "trp_gekokujo_ryuzoji_jizamurai"),
      (faction_set_slot, "fac_culture_16", slot_faction_tier_2_troop, "trp_gekokujo_ryuzoji_retainer"),
      (faction_set_slot, "fac_culture_16", slot_faction_tier_3_troop, "trp_gekokujo_ryuzoji_veteran_retainer"),
      (faction_set_slot, "fac_culture_16", slot_faction_tier_4_troop, "trp_gekokujo_ryuzoji_officer"),
      (faction_set_slot, "fac_culture_16", slot_faction_tier_5_troop, "trp_gekokujo_ryuzoji_mounted_officer"),

      (faction_set_slot, "fac_culture_17", slot_faction_tier_1_troop, "trp_gekokujo_satake_jizamurai"),
      (faction_set_slot, "fac_culture_17", slot_faction_tier_2_troop, "trp_gekokujo_satake_retainer"),
      (faction_set_slot, "fac_culture_17", slot_faction_tier_3_troop, "trp_gekokujo_satake_skirmisher"),
      (faction_set_slot, "fac_culture_17", slot_faction_tier_4_troop, "trp_gekokujo_satake_officer"),
      (faction_set_slot, "fac_culture_17", slot_faction_tier_5_troop, "trp_gekokujo_satake_mounted_officer"),

      (faction_set_slot, "fac_culture_18", slot_faction_tier_1_troop, "trp_gekokujo_satomi_jizamurai"),
      (faction_set_slot, "fac_culture_18", slot_faction_tier_2_troop, "trp_gekokujo_satomi_retainer"),
      (faction_set_slot, "fac_culture_18", slot_faction_tier_3_troop, "trp_gekokujo_satomi_veteran_retainer"),
      (faction_set_slot, "fac_culture_18", slot_faction_tier_4_troop, "trp_gekokujo_satomi_officer"),
      (faction_set_slot, "fac_culture_18", slot_faction_tier_5_troop, "trp_gekokujo_satomi_mounted_officer"),

      (faction_set_slot, "fac_culture_19", slot_faction_tier_1_troop, "trp_gekokujo_ukita_jizamurai"),
      (faction_set_slot, "fac_culture_19", slot_faction_tier_2_troop, "trp_gekokujo_ukita_retainer"),
      (faction_set_slot, "fac_culture_19", slot_faction_tier_3_troop, "trp_gekokujo_ukita_veteran_retainer"),
      (faction_set_slot, "fac_culture_19", slot_faction_tier_4_troop, "trp_gekokujo_ukita_officer"),
      (faction_set_slot, "fac_culture_19", slot_faction_tier_5_troop, "trp_gekokujo_ukita_mounted_officer"),

      (faction_set_slot, "fac_culture_20", slot_faction_tier_1_troop, "trp_gekokujo_ikko_jizamurai"),
      (faction_set_slot, "fac_culture_20", slot_faction_tier_2_troop, "trp_gekokujo_ikko_retainer"),
      (faction_set_slot, "fac_culture_20", slot_faction_tier_3_troop, "trp_gekokujo_ikko_marksman"),
      (faction_set_slot, "fac_culture_20", slot_faction_tier_4_troop, "trp_gekokujo_ikko_veteran_retainer"),
      (faction_set_slot, "fac_culture_20", slot_faction_tier_5_troop, "trp_gekokujo_ikko_mounted_officer"),
      
      (faction_set_slot, "fac_culture_21", slot_faction_tier_1_troop, "trp_gekokujo_xb_veteran_skirmisher"),
      (faction_set_slot, "fac_culture_21", slot_faction_tier_2_troop, "trp_gekokujo_xb_elite_spearman"),
      (faction_set_slot, "fac_culture_21", slot_faction_tier_3_troop, "trp_gekokujo_xb_retainer"),
      (faction_set_slot, "fac_culture_21", slot_faction_tier_4_troop, "trp_gekokujo_xb_marksman"),
      (faction_set_slot, "fac_culture_21", slot_faction_tier_5_troop, "trp_gekokujo_xb_master_gunner"),
      
      (faction_set_slot, "fac_culture_22", slot_faction_tier_1_troop, "trp_gekokujo_ss_officer"),
      (faction_set_slot, "fac_culture_22", slot_faction_tier_2_troop, "trp_gekokujo_ss_mounted_officer"),
      (faction_set_slot, "fac_culture_22", slot_faction_tier_3_troop, "trp_gekokujo_ss_master_archer"),
      (faction_set_slot, "fac_culture_22", slot_faction_tier_4_troop, "trp_gekokujo_ss_veteran_skirmisher"),
      (faction_set_slot, "fac_culture_22", slot_faction_tier_5_troop, "trp_gekokujo_ss_elite_spearman"),
      
      (faction_set_slot, "fac_culture_23", slot_faction_tier_1_troop, "trp_gekokujo_wz_samurai_archer"),
      (faction_set_slot, "fac_culture_23", slot_faction_tier_2_troop, "trp_gekokujo_wz_marksman"),
      (faction_set_slot, "fac_culture_23", slot_faction_tier_3_troop, "trp_gekokujo_wz_master_archer"),
      (faction_set_slot, "fac_culture_23", slot_faction_tier_4_troop, "trp_gekokujo_wz_mounted_retainer"),
      (faction_set_slot, "fac_culture_23", slot_faction_tier_5_troop, "trp_gekokujo_wz_mounted_officer"),
      
      (faction_set_slot, "fac_culture_24", slot_faction_tier_1_troop, "trp_gekokujo_ikko_monk"),
      (faction_set_slot, "fac_culture_24", slot_faction_tier_2_troop, "trp_gekokujo_ikko_yari_monk"),
      (faction_set_slot, "fac_culture_24", slot_faction_tier_3_troop, "trp_gekokujo_ikko_naginata_monk"),
      (faction_set_slot, "fac_culture_24", slot_faction_tier_4_troop, "trp_gekokujo_ikko_veteran_naginata_monk"),
      (faction_set_slot, "fac_culture_24", slot_faction_tier_5_troop, "trp_gekokujo_ikko_elite_naginata_monk"),
      
      (faction_set_slot, "fac_culture_25", slot_faction_tier_1_troop, "trp_gekokujo_dd_master_archer"),
      (faction_set_slot, "fac_culture_25", slot_faction_tier_2_troop, "trp_gekokujo_dd_elite_spearman"),
      (faction_set_slot, "fac_culture_25", slot_faction_tier_3_troop, "trp_gekokujo_dd_samurai_gunner"),
      (faction_set_slot, "fac_culture_25", slot_faction_tier_4_troop, "trp_gekokujo_dd_officer"),
      (faction_set_slot, "fac_culture_25", slot_faction_tier_5_troop, "trp_gekokujo_dd_master_gunner"),
      
      (faction_set_slot, "fac_culture_26", slot_faction_tier_1_troop, "trp_gekokujo_qt_officer"),
      (faction_set_slot, "fac_culture_26", slot_faction_tier_2_troop, "trp_gekokujo_qt_master_gunner"),
      (faction_set_slot, "fac_culture_26", slot_faction_tier_3_troop, "trp_gekokujo_qt_veteran_retainer"),
      (faction_set_slot, "fac_culture_26", slot_faction_tier_4_troop, "trp_gekokujo_qt_marksman"),
      (faction_set_slot, "fac_culture_26", slot_faction_tier_5_troop, "trp_gekokujo_qt_elite_spearman"),
      
      (faction_set_slot, "fac_culture_27", slot_faction_tier_1_troop, "trp_gekokujo_yg_veteran_retainer"),
      (faction_set_slot, "fac_culture_27", slot_faction_tier_2_troop, "trp_gekokujo_yg_mounted_retainer"),
      (faction_set_slot, "fac_culture_27", slot_faction_tier_3_troop, "trp_gekokujo_yg_samurai_gunner"),
      (faction_set_slot, "fac_culture_27", slot_faction_tier_4_troop, "trp_gekokujo_yg_officer"),
      (faction_set_slot, "fac_culture_27", slot_faction_tier_5_troop, "trp_gekokujo_yg_elite_skirmisher"),
      
    
      (faction_set_slot, "fac_culture_28", slot_faction_tier_1_troop, "trp_gekokujo_shimazu_trained_spearman"),
      (faction_set_slot, "fac_culture_28", slot_faction_tier_2_troop, "trp_gekokujo_shimazu_veteran_skirmisher"),
      (faction_set_slot, "fac_culture_28", slot_faction_tier_3_troop, "trp_gekokujo_shimazu_elite_spearman"),
      (faction_set_slot, "fac_culture_28", slot_faction_tier_4_troop, "trp_gekokujo_shimazu_samurai_gunner"),
      (faction_set_slot, "fac_culture_28", slot_faction_tier_5_troop, "trp_gekokujo_shimazu_master_gunner"),

## Tocan Invasion+ ##		  
      (faction_set_slot, "fac_culture_dark_knights", slot_faction_tier_1_troop, "trp_rus_ally"),
      (faction_set_slot, "fac_culture_dark_knights", slot_faction_tier_2_troop, "trp_rus_ally"),
      (faction_set_slot, "fac_culture_dark_knights", slot_faction_tier_3_troop, "trp_rus_ally"),
      (faction_set_slot, "fac_culture_dark_knights", slot_faction_tier_4_troop, "trp_rus_ally"),
      (faction_set_slot, "fac_culture_dark_knights", slot_faction_tier_5_troop, "trp_rus_ally"),	  
## Tocan Invasion- ##	   

	  #gekokujo 3.0 get rid of player culture start
	  ##gekokujo player units
      #(faction_set_slot, "fac_culture_player", slot_faction_tier_1_troop, "trp_gekokujo_player_jizamurai"),
      #(faction_set_slot, "fac_culture_player", slot_faction_tier_2_troop, "trp_gekokujo_player_retainer"),
      #(faction_set_slot, "fac_culture_player", slot_faction_tier_3_troop, "trp_gekokujo_player_veteran_retainer"),
      #(faction_set_slot, "fac_culture_player", slot_faction_tier_4_troop, "trp_gekokujo_player_officer"),
      #(faction_set_slot, "fac_culture_player", slot_faction_tier_5_troop, "trp_gekokujo_player_mounted_officer"),
	  #gekokujo 3.0 get rid of player culture end




      (faction_set_slot, "fac_culture_1", slot_faction_town_walker_male_troop, "trp_town_walker_1"),
      (faction_set_slot, "fac_culture_1", slot_faction_town_walker_female_troop, "trp_town_walker_2"),
      (faction_set_slot, "fac_culture_1", slot_faction_village_walker_male_troop, "trp_village_walker_1"),
      (faction_set_slot, "fac_culture_1", slot_faction_village_walker_female_troop, "trp_village_walker_2"),
      (faction_set_slot, "fac_culture_1", slot_faction_town_spy_male_troop, "trp_spy_walker_1"),
      (faction_set_slot, "fac_culture_1", slot_faction_town_spy_female_troop, "trp_spy_walker_2"),

      (faction_set_slot, "fac_culture_2", slot_faction_town_walker_male_troop, "trp_town_walker_1"),
      (faction_set_slot, "fac_culture_2", slot_faction_town_walker_female_troop, "trp_town_walker_2"),
      (faction_set_slot, "fac_culture_2", slot_faction_village_walker_male_troop, "trp_village_walker_1"),
      (faction_set_slot, "fac_culture_2", slot_faction_village_walker_female_troop, "trp_village_walker_2"),
      (faction_set_slot, "fac_culture_2", slot_faction_town_spy_male_troop, "trp_spy_walker_1"),
      (faction_set_slot, "fac_culture_2", slot_faction_town_spy_female_troop, "trp_spy_walker_2"),

      (faction_set_slot, "fac_culture_3", slot_faction_town_walker_male_troop, "trp_town_walker_1"),
      (faction_set_slot, "fac_culture_3", slot_faction_town_walker_female_troop, "trp_town_walker_2"),
      (faction_set_slot, "fac_culture_3", slot_faction_village_walker_male_troop, "trp_village_walker_1"),
      (faction_set_slot, "fac_culture_3", slot_faction_village_walker_female_troop, "trp_village_walker_2"),
      (faction_set_slot, "fac_culture_3", slot_faction_town_spy_male_troop, "trp_spy_walker_1"),
      (faction_set_slot, "fac_culture_3", slot_faction_town_spy_female_troop, "trp_spy_walker_2"),

      (faction_set_slot, "fac_culture_4", slot_faction_town_walker_male_troop, "trp_town_walker_1"),
      (faction_set_slot, "fac_culture_4", slot_faction_town_walker_female_troop, "trp_town_walker_2"),
      (faction_set_slot, "fac_culture_4", slot_faction_village_walker_male_troop, "trp_village_walker_1"),
      (faction_set_slot, "fac_culture_4", slot_faction_village_walker_female_troop, "trp_village_walker_2"),
      (faction_set_slot, "fac_culture_4", slot_faction_town_spy_male_troop, "trp_spy_walker_1"),
      (faction_set_slot, "fac_culture_4", slot_faction_town_spy_female_troop, "trp_spy_walker_2"),

      (faction_set_slot, "fac_culture_5", slot_faction_town_walker_male_troop, "trp_town_walker_1"),
      (faction_set_slot, "fac_culture_5", slot_faction_town_walker_female_troop, "trp_town_walker_2"),
      (faction_set_slot, "fac_culture_5", slot_faction_village_walker_male_troop, "trp_village_walker_1"),
      (faction_set_slot, "fac_culture_5", slot_faction_village_walker_female_troop, "trp_village_walker_2"),
      (faction_set_slot, "fac_culture_5", slot_faction_town_spy_male_troop, "trp_spy_walker_1"),
      (faction_set_slot, "fac_culture_5", slot_faction_town_spy_female_troop, "trp_spy_walker_2"),

      (faction_set_slot, "fac_culture_6", slot_faction_town_walker_male_troop, "trp_town_walker_1"),
      (faction_set_slot, "fac_culture_6", slot_faction_town_walker_female_troop, "trp_town_walker_2"),
      (faction_set_slot, "fac_culture_6", slot_faction_village_walker_male_troop, "trp_village_walker_1"),
      (faction_set_slot, "fac_culture_6", slot_faction_village_walker_female_troop, "trp_village_walker_2"),
      (faction_set_slot, "fac_culture_6", slot_faction_town_spy_male_troop, "trp_spy_walker_1"),
      (faction_set_slot, "fac_culture_6", slot_faction_town_spy_female_troop, "trp_spy_walker_2"),

      (faction_set_slot, "fac_culture_7", slot_faction_town_walker_male_troop, "trp_town_walker_1"),
      (faction_set_slot, "fac_culture_7", slot_faction_town_walker_female_troop, "trp_town_walker_2"),
      (faction_set_slot, "fac_culture_7", slot_faction_village_walker_male_troop, "trp_village_walker_1"),
      (faction_set_slot, "fac_culture_7", slot_faction_village_walker_female_troop, "trp_village_walker_2"),
      (faction_set_slot, "fac_culture_7", slot_faction_town_spy_male_troop, "trp_spy_walker_1"),
      (faction_set_slot, "fac_culture_7", slot_faction_town_spy_female_troop, "trp_spy_walker_2"),

      (faction_set_slot, "fac_culture_8", slot_faction_town_walker_male_troop, "trp_town_walker_1"),
      (faction_set_slot, "fac_culture_8", slot_faction_town_walker_female_troop, "trp_town_walker_2"),
      (faction_set_slot, "fac_culture_8", slot_faction_village_walker_male_troop, "trp_village_walker_1"),
      (faction_set_slot, "fac_culture_8", slot_faction_village_walker_female_troop, "trp_village_walker_2"),
      (faction_set_slot, "fac_culture_8", slot_faction_town_spy_male_troop, "trp_spy_walker_1"),
      (faction_set_slot, "fac_culture_8", slot_faction_town_spy_female_troop, "trp_spy_walker_2"),

      (faction_set_slot, "fac_culture_9", slot_faction_town_walker_male_troop, "trp_town_walker_1"),
      (faction_set_slot, "fac_culture_9", slot_faction_town_walker_female_troop, "trp_town_walker_2"),
      (faction_set_slot, "fac_culture_9", slot_faction_village_walker_male_troop, "trp_village_walker_1"),
      (faction_set_slot, "fac_culture_9", slot_faction_village_walker_female_troop, "trp_village_walker_2"),
      (faction_set_slot, "fac_culture_9", slot_faction_town_spy_male_troop, "trp_spy_walker_1"),
      (faction_set_slot, "fac_culture_9", slot_faction_town_spy_female_troop, "trp_spy_walker_2"),

      (faction_set_slot, "fac_culture_10", slot_faction_town_walker_male_troop, "trp_town_walker_1"),
      (faction_set_slot, "fac_culture_10", slot_faction_town_walker_female_troop, "trp_town_walker_2"),
      (faction_set_slot, "fac_culture_10", slot_faction_village_walker_male_troop, "trp_village_walker_1"),
      (faction_set_slot, "fac_culture_10", slot_faction_village_walker_female_troop, "trp_village_walker_2"),
      (faction_set_slot, "fac_culture_10", slot_faction_town_spy_male_troop, "trp_spy_walker_1"),
      (faction_set_slot, "fac_culture_10", slot_faction_town_spy_female_troop, "trp_spy_walker_2"),

      (faction_set_slot, "fac_culture_11", slot_faction_town_walker_male_troop, "trp_town_walker_1"),
      (faction_set_slot, "fac_culture_11", slot_faction_town_walker_female_troop, "trp_town_walker_2"),
      (faction_set_slot, "fac_culture_11", slot_faction_village_walker_male_troop, "trp_village_walker_1"),
      (faction_set_slot, "fac_culture_11", slot_faction_village_walker_female_troop, "trp_village_walker_2"),
      (faction_set_slot, "fac_culture_11", slot_faction_town_spy_male_troop, "trp_spy_walker_1"),
      (faction_set_slot, "fac_culture_11", slot_faction_town_spy_female_troop, "trp_spy_walker_2"),

      (faction_set_slot, "fac_culture_12", slot_faction_town_walker_male_troop, "trp_town_walker_1"),
      (faction_set_slot, "fac_culture_12", slot_faction_town_walker_female_troop, "trp_town_walker_2"),
      (faction_set_slot, "fac_culture_12", slot_faction_village_walker_male_troop, "trp_village_walker_1"),
      (faction_set_slot, "fac_culture_12", slot_faction_village_walker_female_troop, "trp_village_walker_2"),
      (faction_set_slot, "fac_culture_12", slot_faction_town_spy_male_troop, "trp_spy_walker_1"),
      (faction_set_slot, "fac_culture_12", slot_faction_town_spy_female_troop, "trp_spy_walker_2"),

      (faction_set_slot, "fac_culture_13", slot_faction_town_walker_male_troop, "trp_town_walker_1"),
      (faction_set_slot, "fac_culture_13", slot_faction_town_walker_female_troop, "trp_town_walker_2"),
      (faction_set_slot, "fac_culture_13", slot_faction_village_walker_male_troop, "trp_village_walker_1"),
      (faction_set_slot, "fac_culture_13", slot_faction_village_walker_female_troop, "trp_village_walker_2"),
      (faction_set_slot, "fac_culture_13", slot_faction_town_spy_male_troop, "trp_spy_walker_1"),
      (faction_set_slot, "fac_culture_13", slot_faction_town_spy_female_troop, "trp_spy_walker_2"),

      (faction_set_slot, "fac_culture_14", slot_faction_town_walker_male_troop, "trp_town_walker_1"),
      (faction_set_slot, "fac_culture_14", slot_faction_town_walker_female_troop, "trp_town_walker_2"),
      (faction_set_slot, "fac_culture_14", slot_faction_village_walker_male_troop, "trp_village_walker_1"),
      (faction_set_slot, "fac_culture_14", slot_faction_village_walker_female_troop, "trp_village_walker_2"),
      (faction_set_slot, "fac_culture_14", slot_faction_town_spy_male_troop, "trp_spy_walker_1"),
      (faction_set_slot, "fac_culture_14", slot_faction_town_spy_female_troop, "trp_spy_walker_2"),

      (faction_set_slot, "fac_culture_15", slot_faction_town_walker_male_troop, "trp_town_walker_1"),
      (faction_set_slot, "fac_culture_15", slot_faction_town_walker_female_troop, "trp_town_walker_2"),
      (faction_set_slot, "fac_culture_15", slot_faction_village_walker_male_troop, "trp_village_walker_1"),
      (faction_set_slot, "fac_culture_15", slot_faction_village_walker_female_troop, "trp_village_walker_2"),
      (faction_set_slot, "fac_culture_15", slot_faction_town_spy_male_troop, "trp_spy_walker_1"),
      (faction_set_slot, "fac_culture_15", slot_faction_town_spy_female_troop, "trp_spy_walker_2"),

      (faction_set_slot, "fac_culture_16", slot_faction_town_walker_male_troop, "trp_town_walker_1"),
      (faction_set_slot, "fac_culture_16", slot_faction_town_walker_female_troop, "trp_town_walker_2"),
      (faction_set_slot, "fac_culture_16", slot_faction_village_walker_male_troop, "trp_village_walker_1"),
      (faction_set_slot, "fac_culture_16", slot_faction_village_walker_female_troop, "trp_village_walker_2"),
      (faction_set_slot, "fac_culture_16", slot_faction_town_spy_male_troop, "trp_spy_walker_1"),
      (faction_set_slot, "fac_culture_16", slot_faction_town_spy_female_troop, "trp_spy_walker_2"),

      (faction_set_slot, "fac_culture_17", slot_faction_town_walker_male_troop, "trp_town_walker_1"),
      (faction_set_slot, "fac_culture_17", slot_faction_town_walker_female_troop, "trp_town_walker_2"),
      (faction_set_slot, "fac_culture_17", slot_faction_village_walker_male_troop, "trp_village_walker_1"),
      (faction_set_slot, "fac_culture_17", slot_faction_village_walker_female_troop, "trp_village_walker_2"),
      (faction_set_slot, "fac_culture_17", slot_faction_town_spy_male_troop, "trp_spy_walker_1"),
      (faction_set_slot, "fac_culture_17", slot_faction_town_spy_female_troop, "trp_spy_walker_2"),

      (faction_set_slot, "fac_culture_18", slot_faction_town_walker_male_troop, "trp_town_walker_1"),
      (faction_set_slot, "fac_culture_18", slot_faction_town_walker_female_troop, "trp_town_walker_2"),
      (faction_set_slot, "fac_culture_18", slot_faction_village_walker_male_troop, "trp_village_walker_1"),
      (faction_set_slot, "fac_culture_18", slot_faction_village_walker_female_troop, "trp_village_walker_2"),
      (faction_set_slot, "fac_culture_18", slot_faction_town_spy_male_troop, "trp_spy_walker_1"),
      (faction_set_slot, "fac_culture_18", slot_faction_town_spy_female_troop, "trp_spy_walker_2"),

      (faction_set_slot, "fac_culture_19", slot_faction_town_walker_male_troop, "trp_town_walker_1"),
      (faction_set_slot, "fac_culture_19", slot_faction_town_walker_female_troop, "trp_town_walker_2"),
      (faction_set_slot, "fac_culture_19", slot_faction_village_walker_male_troop, "trp_village_walker_1"),
      (faction_set_slot, "fac_culture_19", slot_faction_village_walker_female_troop, "trp_village_walker_2"),
      (faction_set_slot, "fac_culture_19", slot_faction_town_spy_male_troop, "trp_spy_walker_1"),
      (faction_set_slot, "fac_culture_19", slot_faction_town_spy_female_troop, "trp_spy_walker_2"),

      (faction_set_slot, "fac_culture_20", slot_faction_town_walker_male_troop, "trp_town_walker_1"),
      (faction_set_slot, "fac_culture_20", slot_faction_town_walker_female_troop, "trp_town_walker_2"),
      (faction_set_slot, "fac_culture_20", slot_faction_village_walker_male_troop, "trp_village_walker_1"),
      (faction_set_slot, "fac_culture_20", slot_faction_village_walker_female_troop, "trp_village_walker_2"),
      (faction_set_slot, "fac_culture_20", slot_faction_town_spy_male_troop, "trp_spy_walker_1"),
      (faction_set_slot, "fac_culture_20", slot_faction_town_spy_female_troop, "trp_spy_walker_2"),
      
      (faction_set_slot, "fac_culture_21", slot_faction_town_walker_male_troop, "trp_town_walker_1"),
      (faction_set_slot, "fac_culture_21", slot_faction_town_walker_female_troop, "trp_town_walker_2"),
      (faction_set_slot, "fac_culture_21", slot_faction_village_walker_male_troop, "trp_village_walker_1"),
      (faction_set_slot, "fac_culture_21", slot_faction_village_walker_female_troop, "trp_village_walker_2"),
      (faction_set_slot, "fac_culture_21", slot_faction_town_spy_male_troop, "trp_spy_walker_1"),
      (faction_set_slot, "fac_culture_21", slot_faction_town_spy_female_troop, "trp_spy_walker_2"),
      
      (faction_set_slot, "fac_culture_22", slot_faction_town_walker_male_troop, "trp_town_walker_1"),
      (faction_set_slot, "fac_culture_22", slot_faction_town_walker_female_troop, "trp_town_walker_2"),
      (faction_set_slot, "fac_culture_22", slot_faction_village_walker_male_troop, "trp_village_walker_1"),
      (faction_set_slot, "fac_culture_22", slot_faction_village_walker_female_troop, "trp_village_walker_2"),
      (faction_set_slot, "fac_culture_22", slot_faction_town_spy_male_troop, "trp_spy_walker_1"),
      (faction_set_slot, "fac_culture_22", slot_faction_town_spy_female_troop, "trp_spy_walker_2"),
      
      (faction_set_slot, "fac_culture_23", slot_faction_town_walker_male_troop, "trp_town_walker_1"),
      (faction_set_slot, "fac_culture_23", slot_faction_town_walker_female_troop, "trp_town_walker_2"),
      (faction_set_slot, "fac_culture_23", slot_faction_village_walker_male_troop, "trp_village_walker_1"),
      (faction_set_slot, "fac_culture_23", slot_faction_village_walker_female_troop, "trp_village_walker_2"),
      (faction_set_slot, "fac_culture_23", slot_faction_town_spy_male_troop, "trp_spy_walker_1"),
      (faction_set_slot, "fac_culture_23", slot_faction_town_spy_female_troop, "trp_spy_walker_2"),
      
      (faction_set_slot, "fac_culture_24", slot_faction_town_walker_male_troop, "trp_town_walker_1"),
      (faction_set_slot, "fac_culture_24", slot_faction_town_walker_female_troop, "trp_town_walker_2"),
      (faction_set_slot, "fac_culture_24", slot_faction_village_walker_male_troop, "trp_village_walker_1"),
      (faction_set_slot, "fac_culture_24", slot_faction_village_walker_female_troop, "trp_village_walker_2"),
      (faction_set_slot, "fac_culture_24", slot_faction_town_spy_male_troop, "trp_spy_walker_1"),
      (faction_set_slot, "fac_culture_24", slot_faction_town_spy_female_troop, "trp_spy_walker_2"),
      
      (faction_set_slot, "fac_culture_25", slot_faction_town_walker_male_troop, "trp_town_walker_1"),
      (faction_set_slot, "fac_culture_25", slot_faction_town_walker_female_troop, "trp_town_walker_2"),
      (faction_set_slot, "fac_culture_25", slot_faction_village_walker_male_troop, "trp_village_walker_1"),
      (faction_set_slot, "fac_culture_25", slot_faction_village_walker_female_troop, "trp_village_walker_2"),
      (faction_set_slot, "fac_culture_25", slot_faction_town_spy_male_troop, "trp_spy_walker_1"),
      (faction_set_slot, "fac_culture_25", slot_faction_town_spy_female_troop, "trp_spy_walker_2"),
      
      (faction_set_slot, "fac_culture_26", slot_faction_town_walker_male_troop, "trp_town_walker_1"),
      (faction_set_slot, "fac_culture_26", slot_faction_town_walker_female_troop, "trp_town_walker_2"),
      (faction_set_slot, "fac_culture_26", slot_faction_village_walker_male_troop, "trp_village_walker_1"),
      (faction_set_slot, "fac_culture_26", slot_faction_village_walker_female_troop, "trp_village_walker_2"),
      (faction_set_slot, "fac_culture_26", slot_faction_town_spy_male_troop, "trp_spy_walker_1"),
      (faction_set_slot, "fac_culture_26", slot_faction_town_spy_female_troop, "trp_spy_walker_2"),
      
      (faction_set_slot, "fac_culture_27", slot_faction_town_walker_male_troop, "trp_town_walker_1"),
      (faction_set_slot, "fac_culture_27", slot_faction_town_walker_female_troop, "trp_town_walker_2"),
      (faction_set_slot, "fac_culture_27", slot_faction_village_walker_male_troop, "trp_village_walker_1"),
      (faction_set_slot, "fac_culture_27", slot_faction_village_walker_female_troop, "trp_village_walker_2"),
      (faction_set_slot, "fac_culture_27", slot_faction_town_spy_male_troop, "trp_spy_walker_1"),
      (faction_set_slot, "fac_culture_27", slot_faction_town_spy_female_troop, "trp_spy_walker_2"),

      (faction_set_slot, "fac_culture_28", slot_faction_town_walker_male_troop, "trp_town_walker_1"),
      (faction_set_slot, "fac_culture_28", slot_faction_town_walker_female_troop, "trp_town_walker_2"),
      (faction_set_slot, "fac_culture_28", slot_faction_village_walker_male_troop, "trp_village_walker_1"),
      (faction_set_slot, "fac_culture_28", slot_faction_village_walker_female_troop, "trp_village_walker_2"),
      (faction_set_slot, "fac_culture_28", slot_faction_town_spy_male_troop, "trp_spy_walker_1"),
      (faction_set_slot, "fac_culture_28", slot_faction_town_spy_female_troop, "trp_spy_walker_2"),
## Tocan Invasion+ ##
      (faction_set_slot, "fac_culture_dark_knights", slot_faction_town_walker_male_troop, "trp_town_walker_1"),
      (faction_set_slot, "fac_culture_dark_knights", slot_faction_town_walker_female_troop, "trp_town_walker_2"),
      (faction_set_slot, "fac_culture_dark_knights", slot_faction_village_walker_male_troop, "trp_village_walker_1"),
      (faction_set_slot, "fac_culture_dark_knights", slot_faction_village_walker_female_troop, "trp_village_walker_2"),
      (faction_set_slot, "fac_culture_dark_knights", slot_faction_town_spy_male_troop, "trp_spy_walker_1"),
      (faction_set_slot, "fac_culture_dark_knights", slot_faction_town_spy_female_troop, "trp_spy_walker_2"),
## Tocan Invasion- ##

	  #gekokujo 3.0 get rid of player culture start
      #(faction_set_slot, "fac_culture_player", slot_faction_town_walker_male_troop, "trp_town_walker_1"),
      #(faction_set_slot, "fac_culture_player", slot_faction_town_walker_female_troop, "trp_town_walker_2"),
      #(faction_set_slot, "fac_culture_player", slot_faction_village_walker_male_troop, "trp_village_walker_1"),
      #(faction_set_slot, "fac_culture_player", slot_faction_village_walker_female_troop, "trp_village_walker_2"),
      #(faction_set_slot, "fac_culture_player", slot_faction_town_spy_male_troop, "trp_spy_walker_1"),
      #(faction_set_slot, "fac_culture_player", slot_faction_town_spy_female_troop, "trp_spy_walker_2"),
	  #gekokujo 3.0 get rid of player culture end

      (try_begin),
        (eq, "$cheat_mode", 1),
        (assign, reg3, "$cheat_mode"),
        (display_message, "@{!}DEBUG : Completed faction troop assignments, cheat mode: {reg3}"),
      (try_end),
      
# Factions:
      (faction_set_slot, "fac_kingdom_1",  slot_faction_culture, "fac_culture_1"),
      (faction_set_slot, "fac_kingdom_1",  slot_faction_leader, "trp_kingdom_1_lord"),
	  (troop_set_slot, "trp_kingdom_1_lord", slot_troop_renown, 1500),
	  
      (faction_set_slot, "fac_kingdom_2",  slot_faction_culture, "fac_culture_2"),
      (faction_set_slot, "fac_kingdom_2",  slot_faction_leader, "trp_kingdom_2_lord"),
	  (troop_set_slot, "trp_kingdom_2_lord", slot_troop_renown, 1500),

      (faction_set_slot, "fac_kingdom_3",  slot_faction_culture, "fac_culture_3"),
      (faction_set_slot, "fac_kingdom_3",  slot_faction_leader, "trp_kingdom_3_lord"),
	  (troop_set_slot, "trp_kingdom_3_lord", slot_troop_renown, 1500),

      (faction_set_slot, "fac_kingdom_4",  slot_faction_culture, "fac_culture_4"),
      (faction_set_slot, "fac_kingdom_4",  slot_faction_leader, "trp_kingdom_4_lord"),
	  (troop_set_slot, "trp_kingdom_4_lord", slot_troop_renown, 1500),

      (faction_set_slot, "fac_kingdom_5",  slot_faction_culture, "fac_culture_5"),
      (faction_set_slot, "fac_kingdom_5",  slot_faction_leader, "trp_kingdom_5_lord"),
	  (troop_set_slot, "trp_kingdom_5_lord", slot_troop_renown, 1500),

      (faction_set_slot, "fac_kingdom_6",  slot_faction_culture, "fac_culture_6"),
      (faction_set_slot, "fac_kingdom_6",  slot_faction_leader, "trp_kingdom_6_lord"),
	  (troop_set_slot, "trp_kingdom_6_lord", slot_troop_renown, 1500),

      (faction_set_slot, "fac_kingdom_7",  slot_faction_culture, "fac_culture_7"),
      (faction_set_slot, "fac_kingdom_7",  slot_faction_leader, "trp_kingdom_7_lord"),
	  (troop_set_slot, "trp_kingdom_7_lord", slot_troop_renown, 1200),

      (faction_set_slot, "fac_kingdom_8",  slot_faction_culture, "fac_culture_8"),
      (faction_set_slot, "fac_kingdom_8",  slot_faction_leader, "trp_kingdom_8_lord"),
	  (troop_set_slot, "trp_kingdom_8_lord", slot_troop_renown, 1200),

      (faction_set_slot, "fac_kingdom_9",  slot_faction_culture, "fac_culture_9"),
      (faction_set_slot, "fac_kingdom_9",  slot_faction_leader, "trp_kingdom_9_lord"),
	  (troop_set_slot, "trp_kingdom_9_lord", slot_troop_renown, 1200),

      (faction_set_slot, "fac_kingdom_10",  slot_faction_culture, "fac_culture_10"),
      (faction_set_slot, "fac_kingdom_10",  slot_faction_leader, "trp_kingdom_10_lord"),
	  (troop_set_slot, "trp_kingdom_10_lord", slot_troop_renown, 1200),

      (faction_set_slot, "fac_kingdom_11",  slot_faction_culture, "fac_culture_11"),
      (faction_set_slot, "fac_kingdom_11",  slot_faction_leader, "trp_kingdom_11_lord"),
	  (troop_set_slot, "trp_kingdom_11_lord", slot_troop_renown, 1200),

      (faction_set_slot, "fac_kingdom_12",  slot_faction_culture, "fac_culture_12"),
      (faction_set_slot, "fac_kingdom_12",  slot_faction_leader, "trp_kingdom_12_lord"),
	  (troop_set_slot, "trp_kingdom_12_lord", slot_troop_renown, 1200),

      (faction_set_slot, "fac_kingdom_13",  slot_faction_culture, "fac_culture_13"),
      (faction_set_slot, "fac_kingdom_13",  slot_faction_leader, "trp_kingdom_13_lord"),
	  (troop_set_slot, "trp_kingdom_13_lord", slot_troop_renown, 1200),

      (faction_set_slot, "fac_kingdom_14",  slot_faction_culture, "fac_culture_14"),
      (faction_set_slot, "fac_kingdom_14",  slot_faction_leader, "trp_kingdom_14_lord"),
	  (troop_set_slot, "trp_kingdom_14_lord", slot_troop_renown, 1200),

      (faction_set_slot, "fac_kingdom_15",  slot_faction_culture, "fac_culture_15"),
      (faction_set_slot, "fac_kingdom_15",  slot_faction_leader, "trp_kingdom_15_lord"),
	  (troop_set_slot, "trp_kingdom_15_lord", slot_troop_renown, 1200),

      (faction_set_slot, "fac_kingdom_16",  slot_faction_culture, "fac_culture_16"),
      (faction_set_slot, "fac_kingdom_16",  slot_faction_leader, "trp_kingdom_16_lord"),
	  (troop_set_slot, "trp_kingdom_16_lord", slot_troop_renown, 1200),

      (faction_set_slot, "fac_kingdom_17",  slot_faction_culture, "fac_culture_17"),
      (faction_set_slot, "fac_kingdom_17",  slot_faction_leader, "trp_kingdom_17_lord"),
	  (troop_set_slot, "trp_kingdom_17_lord", slot_troop_renown, 1000),

      (faction_set_slot, "fac_kingdom_18",  slot_faction_culture, "fac_culture_18"),
      (faction_set_slot, "fac_kingdom_18",  slot_faction_leader, "trp_kingdom_18_lord"),
	  (troop_set_slot, "trp_kingdom_18_lord", slot_troop_renown, 1000),
	  
      (faction_set_slot, "fac_kingdom_19",  slot_faction_culture, "fac_culture_19"),
      (faction_set_slot, "fac_kingdom_19",  slot_faction_leader, "trp_kingdom_19_lord"),
	  (troop_set_slot, "trp_kingdom_19_lord", slot_troop_renown, 1000),

      (faction_set_slot, "fac_kingdom_20",  slot_faction_culture, "fac_culture_20"),
      (faction_set_slot, "fac_kingdom_20",  slot_faction_leader, "trp_kingdom_20_lord"),
	  (troop_set_slot, "trp_kingdom_20_lord", slot_troop_renown, 1000),
      
      (faction_set_slot, "fac_kingdom_21",  slot_faction_culture, "fac_culture_21"),
      (faction_set_slot, "fac_kingdom_21",  slot_faction_leader, "trp_kingdom_21_lord"),
	  (troop_set_slot, "trp_kingdom_21_lord", slot_troop_renown, 1000),
      
      (faction_set_slot, "fac_kingdom_22",  slot_faction_culture, "fac_culture_22"),
      (faction_set_slot, "fac_kingdom_22",  slot_faction_leader, "trp_kingdom_22_lord"),
	  (troop_set_slot, "trp_kingdom_22_lord", slot_troop_renown, 1000),
      
      (faction_set_slot, "fac_kingdom_23",  slot_faction_culture, "fac_culture_23"),
      (faction_set_slot, "fac_kingdom_23",  slot_faction_leader, "trp_kingdom_23_lord"),
	  (troop_set_slot, "trp_kingdom_23_lord", slot_troop_renown, 1000),
      
      (faction_set_slot, "fac_kingdom_24",  slot_faction_culture, "fac_culture_24"),
      (faction_set_slot, "fac_kingdom_24",  slot_faction_leader, "trp_kingdom_24_lord"),
	  (troop_set_slot, "trp_kingdom_24_lord", slot_troop_renown, 1000),
      
      (faction_set_slot, "fac_kingdom_25",  slot_faction_culture, "fac_culture_25"),
      (faction_set_slot, "fac_kingdom_25",  slot_faction_leader, "trp_kingdom_25_lord"),
	  (troop_set_slot, "trp_kingdom_25_lord", slot_troop_renown, 1000),
      
      (faction_set_slot, "fac_kingdom_26",  slot_faction_culture, "fac_culture_26"),
      (faction_set_slot, "fac_kingdom_26",  slot_faction_leader, "trp_kingdom_26_lord"),
	  (troop_set_slot, "trp_kingdom_26_lord", slot_troop_renown, 1000),
      
      (faction_set_slot, "fac_kingdom_27",  slot_faction_culture, "fac_culture_27"),
      (faction_set_slot, "fac_kingdom_27",  slot_faction_leader, "trp_kingdom_27_lord"),
	  (troop_set_slot, "trp_kingdom_27_lord", slot_troop_renown, 1000),
      
      
      (faction_set_slot, "fac_kingdom_28",  slot_faction_culture, "fac_culture_28"),
      (faction_set_slot, "fac_kingdom_28",  slot_faction_leader, "trp_kingdom_28_lord"),
      (faction_set_slot, "fac_kingdom_28",  slot_faction_state, sfs_defeated),
	  (troop_set_slot, "trp_kingdom_28_lord", slot_troop_renown, 1000),
      
## Tocan Invasion+ ##	  	  
      (faction_set_slot, "fac_dark_knights",  slot_faction_culture, "fac_culture_dark_knights"),
      (faction_set_slot, "fac_dark_knights",  slot_faction_leader, "trp_dark_knight_lord"),
	  (troop_set_slot, "trp_dark_knight_lord", slot_troop_renown, 1500),
## Tocan Invasion- ##	  	
      
	  
	  #gekokujo player culture
      (assign, ":player_faction_culture", "fac_culture_player"),
      (faction_set_slot, "fac_player_supporters_faction",  slot_faction_culture, ":player_faction_culture"),
      (faction_set_slot, "fac_player_faction",  slot_faction_culture, ":player_faction_culture"),
	  
      (try_for_range, ":faction_no", kingdoms_begin, kingdoms_end),
        (faction_set_slot, ":faction_no", slot_faction_marshall, -1),
      (try_end), 
      (faction_set_slot, "fac_player_supporters_faction", slot_faction_marshall, "trp_player"),
      (call_script, "script_initialize_faction_troop_types"),
      ##diplomacy begin
      (call_script, "script_dplmc_init_domestic_policy"),
      ##diplomacy end


# Towns:
      (try_for_range, ":item_no", trade_goods_begin, trade_goods_end),
        (store_sub, ":offset", ":item_no", trade_goods_begin),
        (val_add, ":offset", slot_town_trade_good_prices_begin),
        (try_for_range, ":center_no", centers_begin, centers_end),
          (party_set_slot, ":center_no", ":offset", average_price_factor), #1000
        (try_end),
      (try_end),

	  (call_script, "script_initialize_trade_routes"),
	  (call_script, "script_initialize_town_arena_info"),
      #start some tournaments
      (try_for_range, ":town_no", towns_begin, towns_end),
        (store_random_in_range, ":rand", 0, 100),
		#gekokujo tournaments 1/4 chance of tourneys?
        (lt, ":rand", 5),
        #(lt, ":rand", 20),
        (store_random_in_range, ":random_days", 12, 15),
        (party_set_slot, ":town_no", slot_town_has_tournament, ":random_days"),
      (try_end),

      #village products -- at some point we might make it so that the villages supply raw materials to towns, and the towns produce manufactured goods
	  #village products designate the raw materials produced in the vicinity
	  #right now, just doing a test for grain produced in the swadian heartland
	  

	  # fill_village_bound_centers
    #pass 1: Give one village to each castle
      (try_for_range, ":cur_center", castles_begin, castles_end),
        (assign, ":min_dist", 999999),
        (assign, ":min_dist_village", -1),
        (try_for_range, ":cur_village", villages_begin, villages_end),
          (neg|party_slot_ge, ":cur_village", slot_village_bound_center, 1), #skip villages which are already bound.
          (store_distance_to_party_from_party, ":cur_dist", ":cur_village", ":cur_center"),
          (lt, ":cur_dist", ":min_dist"),
          (assign, ":min_dist", ":cur_dist"),
          (assign, ":min_dist_village", ":cur_village"),
        (try_end),
        (party_set_slot, ":min_dist_village", slot_village_bound_center, ":cur_center"),
        (store_faction_of_party, ":town_faction", ":cur_center"),
        (call_script, "script_give_center_to_faction_aux", ":min_dist_village", ":town_faction"),
      (try_end),

      
    #pass 2: Give other villages to closest town.
      (try_for_range, ":cur_village", villages_begin, villages_end),
        (neg|party_slot_ge, ":cur_village", slot_village_bound_center, 1), #skip villages which are already bound.
        (assign, ":min_dist", 999999),
        (assign, ":min_dist_town", -1),
        (try_for_range, ":cur_town", towns_begin, towns_end),
          (store_distance_to_party_from_party, ":cur_dist", ":cur_village", ":cur_town"),
          (lt, ":cur_dist", ":min_dist"),
          (assign, ":min_dist", ":cur_dist"),
          (assign, ":min_dist_town", ":cur_town"),
        (try_end),
        (party_set_slot, ":cur_village", slot_village_bound_center, ":min_dist_town"),
        (store_faction_of_party, ":town_faction", ":min_dist_town"),
        (call_script, "script_give_center_to_faction_aux", ":cur_village", ":town_faction"),
      (try_end),

      		  	  
	# Towns (loop)
      (try_for_range, ":town_no", towns_begin, towns_end),
        (store_sub, ":offset", ":town_no", towns_begin),
        (party_set_slot,":town_no", slot_party_type, spt_town),
        #(store_add, ":cur_object_no", "trp_town_1_seneschal", ":offset"),
        #(party_set_slot,":town_no", slot_town_seneschal, ":cur_object_no"),
        (store_add, ":cur_object_no", "scn_town_1_center", ":offset"),
        (party_set_slot,":town_no", slot_town_center, ":cur_object_no"),
        (store_add, ":cur_object_no", "scn_town_1_castle", ":offset"),
        (party_set_slot,":town_no", slot_town_castle, ":cur_object_no"),
        (store_add, ":cur_object_no", "scn_town_1_prison", ":offset"),
        (party_set_slot,":town_no", slot_town_prison, ":cur_object_no"),
        (store_add, ":cur_object_no", "scn_town_1_walls", ":offset"),
        (party_set_slot,":town_no", slot_town_walls, ":cur_object_no"),
        (store_add, ":cur_object_no", "scn_town_1_tavern", ":offset"),
        (party_set_slot,":town_no", slot_town_tavern, ":cur_object_no"),
        (store_add, ":cur_object_no", "scn_town_1_store", ":offset"),
        (party_set_slot,":town_no", slot_town_store, ":cur_object_no"),
        (store_add, ":cur_object_no", "scn_town_1_arena", ":offset"),
        (party_set_slot,":town_no", slot_town_arena, ":cur_object_no"),
        (store_add, ":cur_object_no", "scn_town_1_alley", ":offset"),
        (party_set_slot,":town_no", slot_town_alley, ":cur_object_no"),
        (store_add, ":cur_object_no", "trp_town_1_mayor", ":offset"),
        (party_set_slot,":town_no", slot_town_elder, ":cur_object_no"),
        (store_add, ":cur_object_no", "trp_town_1_tavernkeeper", ":offset"),
        (party_set_slot,":town_no", slot_town_tavernkeeper, ":cur_object_no"),
        (store_add, ":cur_object_no", "trp_town_1_weaponsmith", ":offset"),
        (party_set_slot,":town_no", slot_town_weaponsmith, ":cur_object_no"),
        (store_add, ":cur_object_no", "trp_town_1_armorer", ":offset"),
        (party_set_slot,":town_no", slot_town_armorer, ":cur_object_no"),
        (store_add, ":cur_object_no", "trp_town_1_merchant", ":offset"),
        (party_set_slot,":town_no", slot_town_merchant, ":cur_object_no"),
        (store_add, ":cur_object_no", "trp_town_1_horse_merchant", ":offset"),
        (party_set_slot,":town_no", slot_town_horse_merchant, ":cur_object_no"),
        (store_add, ":cur_object_no", "scn_town_1_center", ":offset"),
        (party_set_slot,":town_no", slot_town_center, ":cur_object_no"),
        (party_set_slot,":town_no", slot_town_reinforcement_party_template, "pt_center_reinforcements"),
      (try_end),
	  	  
# Castles
      (try_for_range, ":castle_no", castles_begin, castles_end),
        (store_sub, ":offset", ":castle_no", castles_begin),
        (val_mul, ":offset", 3),

#        (store_add, ":senechal_troop_no", "trp_castle_1_seneschal", ":offset"),
#        (party_set_slot,":castle_no", slot_town_seneschal, ":senechal_troop_no"),
        (store_add, ":exterior_scene_no", "scn_castle_1_exterior", ":offset"),
        (party_set_slot,":castle_no", slot_castle_exterior, ":exterior_scene_no"),
        (store_add, ":interior_scene_no", "scn_castle_1_interior", ":offset"),
        (party_set_slot,":castle_no", slot_town_castle, ":interior_scene_no"),
        (store_add, ":interior_scene_no", "scn_castle_1_prison", ":offset"),
        (party_set_slot,":castle_no", slot_town_prison, ":interior_scene_no"),
        
        (party_set_slot,":castle_no", slot_town_reinforcement_party_template, "pt_center_reinforcements"),
        (party_set_slot,":castle_no", slot_party_type, spt_castle),
        (party_set_slot,":castle_no", slot_center_is_besieged_by, -1),
      (try_end),

# Set which castles need to be attacked with siege towers.
      #(party_set_slot,"p_town_13", slot_center_siege_with_belfry, 1),
      #(party_set_slot,"p_town_16", slot_center_siege_with_belfry, 1),

      #(party_set_slot,"p_castle_1", slot_center_siege_with_belfry, 1),
      #(party_set_slot,"p_castle_2", slot_center_siege_with_belfry, 1),
      #(party_set_slot,"p_castle_4", slot_center_siege_with_belfry, 1), #sakasai castle
      #(party_set_slot,"p_castle_7", slot_center_siege_with_belfry, 1),
      #(party_set_slot,"p_castle_8", slot_center_siege_with_belfry, 1),
      #(party_set_slot,"p_castle_9", slot_center_siege_with_belfry, 1),
      #(party_set_slot,"p_castle_11", slot_center_siege_with_belfry, 1),
      #(party_set_slot,"p_castle_13", slot_center_siege_with_belfry, 1),
      #(party_set_slot,"p_castle_21", slot_center_siege_with_belfry, 1),
      #(party_set_slot,"p_castle_25", slot_center_siege_with_belfry, 1),
      #(party_set_slot,"p_castle_34", slot_center_siege_with_belfry, 1),
      #(party_set_slot,"p_castle_35", slot_center_siege_with_belfry, 1),
      #(party_set_slot,"p_castle_38", slot_center_siege_with_belfry, 1),
      #(party_set_slot,"p_castle_40", slot_center_siege_with_belfry, 1),
      #(party_set_slot,"p_castle_41", slot_center_siege_with_belfry, 1),
      #(party_set_slot,"p_castle_42", slot_center_siege_with_belfry, 1),
      #(party_set_slot,"p_castle_43", slot_center_siege_with_belfry, 1),

	  # Villages characters
      (try_for_range, ":village_no", villages_begin, villages_end),
        (store_sub, ":offset", ":village_no", villages_begin),

        (store_add, ":exterior_scene_no", "scn_village_1", ":offset"),
        (party_set_slot,":village_no", slot_castle_exterior, ":exterior_scene_no"),
      
        (store_add, ":store_troop_no", "trp_village_1_elder", ":offset"),
        (party_set_slot,":village_no", slot_town_elder, ":store_troop_no"),
        
        (party_set_slot,":village_no", slot_party_type, spt_village),
        (party_set_slot,":village_no", slot_village_raided_by, -1),
      
        (call_script, "script_refresh_village_defenders", ":village_no"),
        (call_script, "script_refresh_village_defenders", ":village_no"),
        (call_script, "script_refresh_village_defenders", ":village_no"),
        (call_script, "script_refresh_village_defenders", ":village_no"),
      (try_end),
	  
	  #gekokujo 3.0 microfactions! start
	  #this is where we initialize the forts 
	  (assign, "$num_forts_captured", 0),
	  
	  (party_set_slot, "p_fort_1", slot_fort_type, sft_mansion), #sado island has a mansion
	  (party_set_slot, "p_fort_2", slot_fort_type, sft_mansion), #tsushima island has a mansion
	  (party_set_slot, "p_fort_3", slot_fort_type, sft_temple), #kokawa-dera is a temple
	  (party_set_slot, "p_fort_4", slot_fort_type, sft_temple), #mii-dera is a temple
	  (party_set_slot, "p_fort_5", slot_fort_type, sft_village), #niputay is an ainu village
	  (party_set_slot, "p_fort_6", slot_fort_type, sft_village), #otasut is an ainu village
	  
	  (party_set_slot, "p_fort_1", slot_fort_bandit_type, "trp_fort_troop_1_2"), #sado island gets looters (placeholder)
	  (party_set_slot, "p_fort_2", slot_fort_bandit_type, "trp_woku_pirate"), #tsushima island gets pirates
	  (party_set_slot, "p_fort_3", slot_fort_bandit_type, "trp_fort_troop_3_2"), #kokawa-dera gets monk rebels
	  (party_set_slot, "p_fort_4", slot_fort_bandit_type, "trp_fort_troop_4_2"), #mii-dera gets monk rebels
	  (party_set_slot, "p_fort_5", slot_fort_bandit_type, "trp_northern_raider"), #niputay gets ezo warriors
	  (party_set_slot, "p_fort_6", slot_fort_bandit_type, "trp_northern_raider"), #otasut gets ezo warriors
	  
	  #let's iterate!
      (try_for_range, ":center_no", forts_begin, forts_end),
	    (party_set_slot, ":center_no", slot_party_type, spt_fort),
	    (party_set_slot, ":center_no", slot_fort_timer, 0),
	    (party_set_slot, ":center_no", slot_fort_fire, 0),
	    (party_set_slot, ":center_no", slot_fort_captured, 0),
		(store_random_in_range, ":rand", 15, 31),
        (party_set_slot, ":center_no", slot_fort_recruit_amount, ":rand"),
		
		#here begin the offsets
	    (store_sub, ":offset", ":center_no", forts_begin),

        (store_add, ":store_no", "scn_fort_1", ":offset"),
        (party_set_slot, ":center_no", slot_fort_exterior, ":store_no"),
		
        (store_add, ":store_no", "trp_fort_npc_1_1", ":offset"), 
        (party_set_slot, ":center_no", slot_fort_npc_1, ":store_no"),
		
        (store_add, ":store_no", "trp_fort_npc_1_2", ":offset"), 
        (party_set_slot, ":center_no", slot_fort_npc_2, ":store_no"),
        (party_set_slot, ":center_no", slot_fort_npc_2_state, 0),
		
        (store_add, ":store_no", "trp_fort_troop_1_1", ":offset"),
        (party_set_slot, ":center_no", slot_fort_recruit_type, ":store_no"),
		
		#let's form the garrison. 76 troops is 40% the size of castles (190), which are 40% the size of towns (475)
		#50 will be a split between the recruit and bandit types, the final 26 will be mercenaries
		(try_begin),
		  (party_slot_eq, ":center_no", slot_fort_type, sft_village), #ainu villages don't get mercenaries
		  
		  (store_random_in_range, ":rand", 15, 62), #10 to 40, so that there will always at least 10 of each
		  (party_add_members, ":center_no", ":store_no", ":rand"), #recruits
		  
		  (party_get_slot, ":store_no", ":center_no", slot_fort_bandit_type),
		  (store_sub, ":rand", 76, ":rand"),
		  (party_add_members, ":center_no", ":store_no", ":rand"), #bandits
		(else_try),
		  (store_random_in_range, ":rand", 10, 41), #10 to 40, so that there will always at least 10 of each
		  (party_add_members, ":center_no", ":store_no", ":rand"), #recruits
		  
		  (party_get_slot, ":store_no", ":center_no", slot_fort_bandit_type),
		  (store_sub, ":rand", 50, ":rand"),
		  (party_add_members, ":center_no", ":store_no", ":rand"), #bandits
		
		  (store_random_in_range, ":rand", 5, 22), #5 to 21, so that there will always be at least 5 of each
		  (party_add_members, ":center_no", "trp_hired_warrior", ":rand"), #mercenary melee
		  
		  (store_sub, ":rand", 26, ":rand"),
		  (party_add_members, ":center_no", "trp_hired_gunner", ":rand"), #mercenary ranged
		(try_end),
		#note: unlike castles and towns, fort garrisons don't change
		#keep it simple, stupid (i'm stupid)
		
		#let's initialize the walkers (unlike towns and villages, they never have to be refreshed again)
		(try_for_range, ":walker_no", 0, num_town_walkers),
		  (store_add, ":slot_no", slot_center_walker_0_type, ":walker_no"),
		  (party_set_slot, ":center_no", ":slot_no", walkert_default),
		  
		  (try_begin),
		    (this_or_next|eq, ":center_no", "p_fort_5"),
		    (eq, ":center_no", "p_fort_6"),
			(assign, ":store_no", "trp_ainu_walker_1"),
		  (else_try),
			(assign, ":store_no", "trp_village_walker_1"),
		  (try_end),
		  (store_random_in_range, ":rand", 0, 2), #random gender
		  (val_add, ":store_no", ":rand"),
		  
		  (store_add, ":slot_no", slot_center_walker_0_troop, ":walker_no"),
		  (party_set_slot, ":center_no", ":slot_no", ":store_no"),
		  
		  (store_random_in_range, ":store_no", 0, 1000000),
		  (store_add, ":slot_no", slot_center_walker_0_dna, ":walker_no"),
		  (party_set_slot, ":center_no", ":slot_no", ":store_no"),
		(try_end),
		#initializing fort walkers end
      (try_end),
	  
	  #let us also initialize the companion NPCs
	  (troop_set_slot, "trp_fort_npc_1_2", slot_troop_home, "p_fort_1"), #momo
	  (troop_set_slot, "trp_fort_npc_2_2", slot_troop_home, "p_fort_2"), #jungeun
	  (troop_set_slot, "trp_fort_npc_3_2", slot_troop_home, "p_fort_3"), #genko
	  (troop_set_slot, "trp_fort_npc_4_2", slot_troop_home, "p_fort_4"), #jukeini
	  (troop_set_slot, "trp_fort_npc_5_2", slot_troop_home, "p_fort_5"), #chufsanma
	  (troop_set_slot, "trp_fort_npc_6_2", slot_troop_home, "p_fort_6"), #bafunkei

	  (troop_set_slot, "trp_fort_npc_1_2", slot_troop_town_with_contacts, "p_town_20"), #Kagoshima
	  (troop_set_slot, "trp_fort_npc_2_2", slot_troop_town_with_contacts, "p_town_28"), #Izumo
	  (troop_set_slot, "trp_fort_npc_3_2", slot_troop_town_with_contacts, "p_town_24"), #Nara
	  (troop_set_slot, "trp_fort_npc_4_2", slot_troop_town_with_contacts, "p_town_26"), #Imahama
	  (troop_set_slot, "trp_fort_npc_5_2", slot_troop_town_with_contacts, "p_town_22"), #Matsuyama
	  (troop_set_slot, "trp_fort_npc_6_2", slot_troop_town_with_contacts, "p_town_29"), #Funai

	  (troop_set_slot, "trp_fort_npc_1_2", slot_troop_original_faction, 0),
	  (troop_set_slot, "trp_fort_npc_2_2", slot_troop_original_faction, 0),
	  (troop_set_slot, "trp_fort_npc_3_2", slot_troop_original_faction, 0),
	  (troop_set_slot, "trp_fort_npc_4_2", slot_troop_original_faction, 0),
	  (troop_set_slot, "trp_fort_npc_5_2", slot_troop_original_faction, 0),
	  (troop_set_slot, "trp_fort_npc_6_2", slot_troop_original_faction, 0),
	  
	  (troop_set_slot, "trp_fort_npc_1_2", slot_troop_kingsupport_argument, argument_none),
	  (troop_set_slot, "trp_fort_npc_2_2", slot_troop_kingsupport_argument, argument_none),
	  (troop_set_slot, "trp_fort_npc_3_2", slot_troop_kingsupport_argument, argument_none),
	  (troop_set_slot, "trp_fort_npc_4_2", slot_troop_kingsupport_argument, argument_none),
	  (troop_set_slot, "trp_fort_npc_5_2", slot_troop_kingsupport_argument, argument_none),
	  (troop_set_slot, "trp_fort_npc_6_2", slot_troop_kingsupport_argument, argument_none),

	  (troop_set_slot, "trp_fort_npc_1_2", slot_lord_reputation_type, lrep_benefactor),
	  (troop_set_slot, "trp_fort_npc_2_2", slot_lord_reputation_type, lrep_custodian),
	  (troop_set_slot, "trp_fort_npc_3_2", slot_lord_reputation_type, lrep_roguish),
	  (troop_set_slot, "trp_fort_npc_4_2", slot_lord_reputation_type, lrep_cunning), #imagawa yoshimoto's mother jukeini was called "onna daimyo"
	  (troop_set_slot, "trp_fort_npc_5_2", slot_lord_reputation_type, lrep_custodian),
	  (troop_set_slot, "trp_fort_npc_6_2", slot_lord_reputation_type, lrep_roguish),
	  
	  #gekokujo 3.0 microfactions! end
      
      (try_for_range, ":center_no", centers_begin, centers_end),
        (party_set_slot, ":center_no", slot_center_last_spotted_enemy, -1),
        (party_set_slot, ":center_no", slot_center_is_besieged_by, -1),
        (party_set_slot, ":center_no", slot_center_last_taken_by_troop, -1),
        ##diplomacy start+ Set the home slots for town merchants, elders, etc. for reverse-lookup
        (try_for_range, ":offset", dplmc_slot_town_merchants_begin, dplmc_slot_town_merchants_end),
           (party_get_slot, ":npc", ":center_no", ":offset"),
           (gt, ":npc", 0),
           (neg|troop_slot_ge, ":npc", slot_troop_home, 1),#If the startup script wasn't altered by another mod, we don't have to worry about this condition.
           (troop_set_slot, ":npc", slot_troop_home, ":center_no"),
        (try_end),
        ##diplomacy end+
      (try_end),

# Troops:

# Assign banners and renown.
# We assume there are enough banners for all kingdom heroes.

      #faction banners
      (faction_set_slot, "fac_kingdom_1", slot_faction_banner, "mesh_banner_c01"), #uesugi
      (faction_set_slot, "fac_kingdom_2", slot_faction_banner, "mesh_banner_b19"), #date
      (faction_set_slot, "fac_kingdom_3", slot_faction_banner, "mesh_banner_b20"), #oda
      (faction_set_slot, "fac_kingdom_4", slot_faction_banner, "mesh_banner_b04"), #mori
      (faction_set_slot, "fac_kingdom_5", slot_faction_banner, "mesh_banner_g11"), #takeda
      (faction_set_slot, "fac_kingdom_6", slot_faction_banner, "mesh_banner_a13"), #tokugawa
      (faction_set_slot, "fac_kingdom_7", slot_faction_banner, "mesh_banner_a11"), #miyoshi
      (faction_set_slot, "fac_kingdom_8", slot_faction_banner, "mesh_banner_a19"), #amako
      (faction_set_slot, "fac_kingdom_9", slot_faction_banner, "mesh_banner_c03"), #otomo
      (faction_set_slot, "fac_kingdom_10", slot_faction_banner, "mesh_banner_b14"), #nanbu
      (faction_set_slot, "fac_kingdom_11", slot_faction_banner, "mesh_banner_c04"), #asakura
      (faction_set_slot, "fac_kingdom_12", slot_faction_banner, "mesh_banner_d20"), #chosokabe
      (faction_set_slot, "fac_kingdom_13", slot_faction_banner, "mesh_banner_a20"), #hojo
      (faction_set_slot, "fac_kingdom_14", slot_faction_banner, "mesh_banner_b12"), #mogami
      (faction_set_slot, "fac_kingdom_15", slot_faction_banner, "mesh_banner_c05"), #shimazu
      (faction_set_slot, "fac_kingdom_16", slot_faction_banner, "mesh_banner_c06"), #ryuzoji
      (faction_set_slot, "fac_kingdom_17", slot_faction_banner, "mesh_banner_c07"), #satake
      (faction_set_slot, "fac_kingdom_18", slot_faction_banner, "mesh_banner_c08"), #satomi
      (faction_set_slot, "fac_kingdom_19", slot_faction_banner, "mesh_banner_a02"), #ukita
      (faction_set_slot, "fac_kingdom_20", slot_faction_banner, "mesh_banner_f02"), #ikko-ikki
#Gekokujo todo?
      (faction_set_slot, "fac_dark_knights", slot_faction_banner, "mesh_banner_c01"), ## Tocan Invasion ##

      (try_for_range, ":cur_faction", npc_kingdoms_begin, npc_kingdoms_end),
        (faction_get_slot, ":cur_faction_king", ":cur_faction", slot_faction_leader),
        (faction_get_slot, ":cur_faction_banner", ":cur_faction", slot_faction_banner),
        (val_sub, ":cur_faction_banner", banner_meshes_begin),
        (val_add, ":cur_faction_banner", banner_scene_props_begin),
        (troop_set_slot, ":cur_faction_king", slot_troop_banner_scene_prop, ":cur_faction_banner"),
      (try_end),
	  #gekokujo no offsets required
      #(assign, ":num_khergit_lords_assigned", 0),
      #(assign, ":num_sarranid_lords_assigned", 0),
      (assign, ":num_other_lords_assigned", 0),
            
      (try_for_range, ":kingdom_hero", active_npcs_begin, active_npcs_end),
        (this_or_next|troop_slot_eq, ":kingdom_hero", slot_troop_occupation, slto_kingdom_hero),
        (troop_slot_eq, ":kingdom_hero", slot_troop_occupation, slto_inactive_pretender),
        
        (store_troop_faction, ":kingdom_hero_faction", ":kingdom_hero"),
        (neg|faction_slot_eq, ":kingdom_hero_faction", slot_faction_leader, ":kingdom_hero"),
        #(try_begin), 
        #  (eq, ":kingdom_hero_faction", "fac_kingdom_3"), #Khergit Khanate
        #  (store_add, ":kingdom_3_banners_begin", banner_scene_props_begin, khergit_banners_begin_offset),
        #  (store_add, ":banner_id", ":kingdom_3_banners_begin", ":num_khergit_lords_assigned"),
        #  (troop_set_slot, ":kingdom_hero", slot_troop_banner_scene_prop, ":banner_id"),
        #  (val_add, ":num_khergit_lords_assigned", 1),
        #(else_try),
        #  (eq, ":kingdom_hero_faction", "fac_kingdom_6"), #Sarranid Sultanate
        #  (store_add, ":kingdom_6_banners_begin", banner_scene_props_begin, sarranid_banners_begin_offset),
        #  (store_add, ":banner_id", ":kingdom_6_banners_begin", ":num_sarranid_lords_assigned"),
        #  (troop_set_slot, ":kingdom_hero", slot_troop_banner_scene_prop, ":banner_id"),
        #  (val_add, ":num_sarranid_lords_assigned", 1),
        #(else_try),
          (assign, ":hero_offset", ":num_other_lords_assigned"),
          #(try_begin),
          #  (gt, ":hero_offset", khergit_banners_begin_offset),#Do not add khergit banners to other lords
          #  (val_add, ":hero_offset", khergit_banners_end_offset),
          #  (val_sub, ":hero_offset", khergit_banners_begin_offset),
          #(try_end),
          #(try_begin),
          #  (gt, ":hero_offset", sarranid_banners_begin_offset),#Do not add sarranid banners to other lords
          #  (val_add, ":hero_offset", sarranid_banners_end_offset),
          #  (val_sub, ":hero_offset", sarranid_banners_begin_offset),
          #(try_end),
          (store_add, ":banner_id", banner_scene_props_begin, ":hero_offset"),
          (troop_set_slot, ":kingdom_hero", slot_troop_banner_scene_prop, ":banner_id"),
          (val_add, ":num_other_lords_assigned", 1),
        #(try_end),
        (try_begin),
          (this_or_next|lt, ":banner_id", banner_scene_props_begin),
          (gt, ":banner_id", banner_scene_props_end_minus_one),
          (display_message, "@{!}ERROR: Not enough banners for heroes!"),
        (try_end),

        (store_character_level, ":level", ":kingdom_hero"),
        (store_mul, ":renown", ":level", ":level"),
        (val_div, ":renown", 4), #for top lord, is about 400

		(troop_get_slot, ":age", ":kingdom_hero", slot_troop_age),
        (store_mul, ":age_addition", ":age", ":age"),
        (val_div, ":age_addition", 8), #for top lord, is about 400
		(val_add, ":renown", ":age_addition"),
			
        (try_begin),
          (faction_slot_eq, ":kingdom_hero_faction", slot_faction_leader, ":kingdom_hero"),
          (store_random_in_range, ":random_renown", 250, 400),
        (else_try),
          (store_random_in_range, ":random_renown", 0, 100),
        (try_end),
        (val_add, ":renown", ":random_renown"),

        (troop_set_slot, ":kingdom_hero", slot_troop_renown, ":renown"),				
      (try_end),

      (try_for_range, ":troop_no", "trp_player", "trp_merchants_end"),
        (add_troop_note_tableau_mesh, ":troop_no", "tableau_troop_note_mesh"),
      (try_end),
	  
      (try_for_range, ":center_no", centers_begin, centers_end),
        (add_party_note_tableau_mesh, ":center_no", "tableau_center_note_mesh"),
      (try_end),

      (try_for_range, ":faction_no", kingdoms_begin, kingdoms_end),
        (is_between, ":faction_no", "fac_kingdom_1", kingdoms_end), #Excluding player kingdom
        (add_faction_note_tableau_mesh, ":faction_no", "tableau_faction_note_mesh"),
      (else_try),
        (add_faction_note_tableau_mesh, ":faction_no", "tableau_faction_note_mesh_banner"),
      (try_end),
	  
      

   
	  #gekokujo 2.1 manual banner exchanges
   
	    #(troop_set_slot, "trp_knight_1_2", slot_troop_banner_scene_prop, "spr_banner_g01"), #honjo shigenaga gets the 'dragon' banner
      #(troop_set_slot, "trp_knight_1_6", slot_troop_banner_scene_prop, "spr_banner_g07"), #naoe kagetsuna gets 'love' even though it's kanetsugu's helmet date
      #(troop_set_slot, "trp_knight_1_7", slot_troop_banner_scene_prop, "spr_banner_h18"), #suda chikamitsu gets his irl swastika *gulp* (not mon)
      #(troop_set_slot, "trp_knight_1_8", slot_troop_banner_scene_prop, "spr_banner_h17"), #murakami yoshikiyo gets his 'mura' banner
      #(troop_set_slot, "trp_knight_1_9", slot_troop_banner_scene_prop, "spr_banner_g02"), #kitajo kagehiro gets the 'bishamonten' banner
      #(troop_set_slot, "trp_knight_1_10", slot_troop_banner_scene_prop, "spr_banner_i06"), #nagao masakage gets his irl banner
      #(troop_set_slot, "trp_knight_3_2", slot_troop_banner_scene_prop, "spr_banner_f03"), #shibata katsuie gets his irl banner
      #(troop_set_slot, "trp_knight_3_4", slot_troop_banner_scene_prop, "spr_banner_i01"), #HASHIBA hideyoshi gets his TOYOTOMI banner from when he became kampaku
      #(troop_set_slot, "trp_knight_3_5", slot_troop_banner_scene_prop, "spr_banner_n"), #akechi mitsuhide gets his irl banner
      #(troop_set_slot, "trp_knight_3_7", slot_troop_banner_scene_prop, "spr_banner_ck"), #ikeda nobuteru gets his irl banner
      #(troop_set_slot, "trp_knight_3_9", slot_troop_banner_scene_prop, "spr_banner_da"), #sakuma morimasa gets his irl banner
      #(troop_set_slot, "trp_knight_4_2", slot_troop_banner_scene_prop, "spr_banner_ek"), #kobayakawa takakage gets his irl banner
      #(troop_set_slot, "trp_knight_5_1", slot_troop_banner_scene_prop, "spr_banner_g03"), #baba nobuharu gets 'wind'
      #(troop_set_slot, "trp_knight_5_2", slot_troop_banner_scene_prop, "spr_banner_i07"), #sanada yukitaka gets his irl banner
      #(troop_set_slot, "trp_knight_5_4", slot_troop_banner_scene_prop, "spr_banner_g06"), #yamamoto kansuke gets 'mountain'
      #(troop_set_slot, "trp_knight_5_6", slot_troop_banner_scene_prop, "spr_banner_g08"), #kosaka masanobu gets takeda blue
      #(troop_set_slot, "trp_knight_5_7", slot_troop_banner_scene_prop, "spr_banner_g04"), #naito masatoyo gets 'forest'
      #(troop_set_slot, "trp_knight_5_8", slot_troop_banner_scene_prop, "spr_banner_g09"), #tsuchiya masatsugu gets takeda green
      #(troop_set_slot, "trp_knight_5_9", slot_troop_banner_scene_prop, "spr_banner_g05"), #yamagata masakage gets 'fire'
      #(troop_set_slot, "trp_knight_5_11", slot_troop_banner_scene_prop, "spr_banner_g10"), #komai masatake gets takeda red
      #(troop_set_slot, "trp_knight_6_2", slot_troop_banner_scene_prop, "spr_banner_f"), #honda tadakatsu gets his 'hon' rather than aoi banner
      #(troop_set_slot, "trp_knight_6_6", slot_troop_banner_scene_prop, "spr_banner_ba"), #ii naomasa gets his irl banner
	    #(troop_set_slot, "trp_knight_6_7", slot_troop_banner_scene_prop, "spr_banner_i04"), #torii mototada gets his irl banner
      #(troop_set_slot, "trp_knight_9_8", slot_troop_banner_scene_prop, "spr_banner_o"), #ito yoshisuke gets his irl banner
      #(troop_set_slot, "trp_knight_11_3", slot_troop_banner_scene_prop, "spr_banner_i"), #ishida masatsugu gets his irl banner
	    #(troop_set_slot, "trp_knight_19_6", slot_troop_banner_scene_prop, "spr_banner_ci"), #urakami munekage gets his irl banner
      #(troop_set_slot, "trp_kingdom_5_pretender", slot_troop_banner_scene_prop, "spr_banner_g13"), #takeda yoshinobu gets the head of takeda's irl mon
	    #(troop_set_slot, "trp_kingdom_6_pretender", slot_troop_banner_scene_prop, "spr_banner_g12"), #this fake jukeini gets the imagawa banner        
	  #the following lords get their auto-assigned banners taken away in exchange with the lords and factions above
	  #i could have just ordered the banners correctly, but i didn't. no take-backs. R.I.P.
  	  #(troop_set_slot, "trp_knight_2_1", slot_troop_banner_scene_prop, "spr_banner_g"), #endo exchanges away his banner
  	  #(troop_set_slot, "trp_knight_2_3", slot_troop_banner_scene_prop, "spr_banner_h"), #inawashiro exchanges away his banner
  	  #(troop_set_slot, "trp_knight_2_4", slot_troop_banner_scene_prop, "spr_banner_j"), #oniniwa exchanges away his banner
  	  #(troop_set_slot, "trp_knight_2_5", slot_troop_banner_scene_prop, "spr_banner_bb"), #kakeda exchanges away his banner
  	  #(troop_set_slot, "trp_knight_3_1", slot_troop_banner_scene_prop, "spr_banner_bf"), #maeda exchanges away his banner
  	  #(troop_set_slot, "trp_knight_4_5", slot_troop_banner_scene_prop, "spr_banner_bi"), #fukubara exchanges away his banner
  	  #(troop_set_slot, "trp_knight_4_7", slot_troop_banner_scene_prop, "spr_banner_br"), #kunishi exchanges away his banner
  	  #(troop_set_slot, "trp_knight_5_3", slot_troop_banner_scene_prop, "spr_banner_bu"), #oyamada exchanges away his banner
  	  #(troop_set_slot, "trp_knight_5_5", slot_troop_banner_scene_prop, "spr_banner_cb"), #obata exchanges away his banner
  	  #(troop_set_slot, "trp_knight_5_10", slot_troop_banner_scene_prop, "spr_banner_cj"), #hara exchanges away his banner
  	  #(troop_set_slot, "trp_knight_5_12", slot_troop_banner_scene_prop, "spr_banner_cn"), #aiki exchanges away his banner
  	  #(troop_set_slot, "trp_knight_6_1", slot_troop_banner_scene_prop, "spr_banner_co"), #okudaira exchanges away his banner
  	  #(troop_set_slot, "trp_knight_6_3", slot_troop_banner_scene_prop, "spr_banner_dq"), #hattori exchanges away his banner
  	  #(troop_set_slot, "trp_knight_7_6", slot_troop_banner_scene_prop, "spr_banner_ee"), #atagi exchanges away his banner
  	  #(troop_set_slot, "trp_knight_10_3", slot_troop_banner_scene_prop, "spr_banner_g19"), #ishikawa exchanges away his banner
  	  #(troop_set_slot, "trp_knight_12_3", slot_troop_banner_scene_prop, "spr_banner_h10"), #yoshida exchanges away his banner
  	  #(troop_set_slot, "trp_knight_14_1", slot_troop_banner_scene_prop, "spr_banner_h11"), #tateoka exchanges away his banner
  	  #(troop_set_slot, "trp_knight_14_2", slot_troop_banner_scene_prop, "spr_banner_h12"), #buei exchanges away his banner
  	  #(troop_set_slot, "trp_knight_16_6", slot_troop_banner_scene_prop, "spr_banner_h13"), #nabeshima exchanges away his banner
  	  #(troop_set_slot, "trp_knight_17_1", slot_troop_banner_scene_prop, "spr_banner_h14"), #umezu exchanges away his banner
  	  #(troop_set_slot, "trp_knight_17_2", slot_troop_banner_scene_prop, "spr_banner_h15"), #okamoto exchanges away his banner
  	  #(troop_set_slot, "trp_knight_17_3", slot_troop_banner_scene_prop, "spr_banner_h16"), #kuruma exchanges away his banner
  	  #(troop_set_slot, "trp_knight_17_4", slot_troop_banner_scene_prop, "spr_banner_h19"), #onuki exchanges away his banner
  	  #(troop_set_slot, "trp_knight_17_5", slot_troop_banner_scene_prop, "spr_banner_h20"), #oba exchanges away his banner
  	  #(troop_set_slot, "trp_knight_17_6", slot_troop_banner_scene_prop, "spr_banner_h21"), #wada exchanges away his banner
  	  #(troop_set_slot, "trp_knight_18_1", slot_troop_banner_scene_prop, "spr_banner_i02"), #masaki exchanges away his banner
  	  #(troop_set_slot, "trp_knight_18_2", slot_troop_banner_scene_prop, "spr_banner_i03"), #toki exchanges away his banner
  	  #(troop_set_slot, "trp_knight_18_3", slot_troop_banner_scene_prop, "spr_banner_i05"), #mikogami exchanges away his banner
  	  #(troop_set_slot, "trp_knight_18_4", slot_troop_banner_scene_prop, "spr_banner_i08"), #yuki exchanges away his banner
  	  #(troop_set_slot, "trp_knight_18_5", slot_troop_banner_scene_prop, "spr_banner_i09"), #chiba exchanges away his banner
  	  #(troop_set_slot, "trp_knight_18_6", slot_troop_banner_scene_prop, "spr_banner_i10"), #takagi exchanges away his banner  
      
     (troop_set_slot, "trp_kingdom_1_lord", slot_troop_banner_scene_prop, "spr_banner_g07"),
     (troop_set_slot, "trp_knight_1_1", slot_troop_banner_scene_prop, "spr_banner_g07"),
     (troop_set_slot, "trp_knight_1_2", slot_troop_banner_scene_prop, "spr_banner_g07"),
     (troop_set_slot, "trp_knight_1_3", slot_troop_banner_scene_prop, "spr_banner_g07"),
     (troop_set_slot, "trp_knight_1_4", slot_troop_banner_scene_prop, "spr_banner_g07"),
     (troop_set_slot, "trp_knight_1_5", slot_troop_banner_scene_prop, "spr_banner_g07"),
     (troop_set_slot, "trp_knight_1_6", slot_troop_banner_scene_prop, "spr_banner_g07"),
     (troop_set_slot, "trp_knight_1_7", slot_troop_banner_scene_prop, "spr_banner_g07"),
     (troop_set_slot, "trp_knight_1_8", slot_troop_banner_scene_prop, "spr_banner_g07"),
     (troop_set_slot, "trp_knight_1_9", slot_troop_banner_scene_prop, "spr_banner_g07"),
     (troop_set_slot, "trp_knight_1_10", slot_troop_banner_scene_prop, "spr_banner_g07"),
     
     (troop_set_slot, "trp_kingdom_2_lord", slot_troop_banner_scene_prop, "spr_banner_bs"),
     (troop_set_slot, "trp_knight_2_1", slot_troop_banner_scene_prop, "spr_banner_bs"),
     (troop_set_slot, "trp_knight_2_2", slot_troop_banner_scene_prop, "spr_banner_bs"),
     (troop_set_slot, "trp_knight_2_3", slot_troop_banner_scene_prop, "spr_banner_bs"),
     (troop_set_slot, "trp_knight_2_4", slot_troop_banner_scene_prop, "spr_banner_bs"),
     (troop_set_slot, "trp_knight_2_5", slot_troop_banner_scene_prop, "spr_banner_bs"),

     (troop_set_slot, "trp_kingdom_3_lord", slot_troop_banner_scene_prop, "spr_banner_f04"),
     (troop_set_slot, "trp_knight_3_1", slot_troop_banner_scene_prop, "spr_banner_f04"),
     (troop_set_slot, "trp_knight_3_2", slot_troop_banner_scene_prop, "spr_banner_f04"),
     (troop_set_slot, "trp_knight_3_3", slot_troop_banner_scene_prop, "spr_banner_f04"),
     (troop_set_slot, "trp_knight_3_4", slot_troop_banner_scene_prop, "spr_banner_f04"),
     (troop_set_slot, "trp_knight_3_5", slot_troop_banner_scene_prop, "spr_banner_f04"),
     
     (troop_set_slot, "trp_kingdom_4_lord", slot_troop_banner_scene_prop, "spr_banner_bd"),
     (troop_set_slot, "trp_knight_4_1", slot_troop_banner_scene_prop, "spr_banner_bd"),
     (troop_set_slot, "trp_knight_4_2", slot_troop_banner_scene_prop, "spr_banner_bd"),
     (troop_set_slot, "trp_knight_4_3", slot_troop_banner_scene_prop, "spr_banner_bd"),
     (troop_set_slot, "trp_knight_4_4", slot_troop_banner_scene_prop, "spr_banner_bd"),
     (troop_set_slot, "trp_knight_4_5", slot_troop_banner_scene_prop, "spr_banner_bd"),
     (troop_set_slot, "trp_knight_4_6", slot_troop_banner_scene_prop, "spr_banner_bd"),
     (troop_set_slot, "trp_knight_4_7", slot_troop_banner_scene_prop, "spr_banner_bd"),
     (troop_set_slot, "trp_knight_4_8", slot_troop_banner_scene_prop, "spr_banner_bd"),
     (troop_set_slot, "trp_knight_4_9", slot_troop_banner_scene_prop, "spr_banner_bd"),
     (troop_set_slot, "trp_knight_4_10", slot_troop_banner_scene_prop, "spr_banner_bd"),
     
     (troop_set_slot, "trp_kingdom_5_lord", slot_troop_banner_scene_prop, "spr_banner_h08"),
     (troop_set_slot, "trp_knight_5_1", slot_troop_banner_scene_prop, "spr_banner_h08"),
     (troop_set_slot, "trp_knight_5_2", slot_troop_banner_scene_prop, "spr_banner_h08"),
     (troop_set_slot, "trp_knight_5_3", slot_troop_banner_scene_prop, "spr_banner_h08"),
     (troop_set_slot, "trp_knight_5_4", slot_troop_banner_scene_prop, "spr_banner_h08"),
     (troop_set_slot, "trp_knight_5_5", slot_troop_banner_scene_prop, "spr_banner_h08"),
     
     (troop_set_slot, "trp_kingdom_6_lord", slot_troop_banner_scene_prop, "spr_banner_m"),
     (troop_set_slot, "trp_knight_6_1", slot_troop_banner_scene_prop, "spr_banner_m"),
     (troop_set_slot, "trp_knight_6_2", slot_troop_banner_scene_prop, "spr_banner_m"),
     (troop_set_slot, "trp_knight_6_3", slot_troop_banner_scene_prop, "spr_banner_m"),
     (troop_set_slot, "trp_knight_6_4", slot_troop_banner_scene_prop, "spr_banner_m"),
     (troop_set_slot, "trp_knight_6_5", slot_troop_banner_scene_prop, "spr_banner_m"),
     (troop_set_slot, "trp_knight_6_6", slot_troop_banner_scene_prop, "spr_banner_m"),
     (troop_set_slot, "trp_knight_6_7", slot_troop_banner_scene_prop, "spr_banner_m"),
     (troop_set_slot, "trp_knight_6_8", slot_troop_banner_scene_prop, "spr_banner_m"),
     (troop_set_slot, "trp_knight_6_9", slot_troop_banner_scene_prop, "spr_banner_m"),
     (troop_set_slot, "trp_knight_6_10", slot_troop_banner_scene_prop, "spr_banner_m"),
     (troop_set_slot, "trp_knight_6_11", slot_troop_banner_scene_prop, "spr_banner_m"),
     (troop_set_slot, "trp_knight_6_12", slot_troop_banner_scene_prop, "spr_banner_m"),
     (troop_set_slot, "trp_knight_6_13", slot_troop_banner_scene_prop, "spr_banner_m"),
     (troop_set_slot, "trp_knight_6_14", slot_troop_banner_scene_prop, "spr_banner_m"),
     (troop_set_slot, "trp_knight_6_15", slot_troop_banner_scene_prop, "spr_banner_m"), 
     (troop_set_slot, "trp_knight_6_16", slot_troop_banner_scene_prop, "spr_banner_m"),
     (troop_set_slot, "trp_knight_6_17", slot_troop_banner_scene_prop, "spr_banner_m"),
     (troop_set_slot, "trp_knight_6_18", slot_troop_banner_scene_prop, "spr_banner_m"),
     (troop_set_slot, "trp_knight_6_19", slot_troop_banner_scene_prop, "spr_banner_m"),

     (troop_set_slot, "trp_kingdom_7_lord", slot_troop_banner_scene_prop, "spr_banner_h11"),
     (troop_set_slot, "trp_knight_7_1", slot_troop_banner_scene_prop, "spr_banner_h11"),
     (troop_set_slot, "trp_knight_7_2", slot_troop_banner_scene_prop, "spr_banner_h11"),
     (troop_set_slot, "trp_knight_7_3", slot_troop_banner_scene_prop, "spr_banner_h11"),
     (troop_set_slot, "trp_knight_7_4", slot_troop_banner_scene_prop, "spr_banner_h11"),
     (troop_set_slot, "trp_knight_7_5", slot_troop_banner_scene_prop, "spr_banner_h11"),
     
     (troop_set_slot, "trp_kingdom_8_lord", slot_troop_banner_scene_prop, "spr_banner_ck"),
     (troop_set_slot, "trp_knight_8_1", slot_troop_banner_scene_prop, "spr_banner_ck"),
     (troop_set_slot, "trp_knight_8_2", slot_troop_banner_scene_prop, "spr_banner_ck"),
     (troop_set_slot, "trp_knight_8_3", slot_troop_banner_scene_prop, "spr_banner_ck"),
     (troop_set_slot, "trp_knight_8_4", slot_troop_banner_scene_prop, "spr_banner_ck"),
     (troop_set_slot, "trp_knight_8_5", slot_troop_banner_scene_prop, "spr_banner_ck"),
   
     (troop_set_slot, "trp_kingdom_9_lord", slot_troop_banner_scene_prop, "spr_banner_f14"),
     (troop_set_slot, "trp_knight_9_1", slot_troop_banner_scene_prop, "spr_banner_f14"),
     (troop_set_slot, "trp_knight_9_2", slot_troop_banner_scene_prop, "spr_banner_f14"),
     (troop_set_slot, "trp_knight_9_3", slot_troop_banner_scene_prop, "spr_banner_f14"),
     (troop_set_slot, "trp_knight_9_4", slot_troop_banner_scene_prop, "spr_banner_f14"),
     (troop_set_slot, "trp_knight_9_5", slot_troop_banner_scene_prop, "spr_banner_f14"),
     
     (troop_set_slot, "trp_kingdom_10_lord", slot_troop_banner_scene_prop, "spr_banner_o"),
     (troop_set_slot, "trp_knight_10_1", slot_troop_banner_scene_prop, "spr_banner_o"),
     (troop_set_slot, "trp_knight_10_2", slot_troop_banner_scene_prop, "spr_banner_o"),
     (troop_set_slot, "trp_knight_10_3", slot_troop_banner_scene_prop, "spr_banner_o"),
     (troop_set_slot, "trp_knight_10_4", slot_troop_banner_scene_prop, "spr_banner_o"),
     (troop_set_slot, "trp_knight_10_5", slot_troop_banner_scene_prop, "spr_banner_o"),
     
     (troop_set_slot, "trp_kingdom_11_lord", slot_troop_banner_scene_prop, "spr_banner_bu"),
     (troop_set_slot, "trp_knight_11_1", slot_troop_banner_scene_prop, "spr_banner_bu"),
     (troop_set_slot, "trp_knight_11_2", slot_troop_banner_scene_prop, "spr_banner_bu"),
     
     (troop_set_slot, "trp_kingdom_12_lord", slot_troop_banner_scene_prop, "spr_banner_bm"),
     (troop_set_slot, "trp_knight_12_1", slot_troop_banner_scene_prop, "spr_banner_bm"),
     (troop_set_slot, "trp_knight_12_2", slot_troop_banner_scene_prop, "spr_banner_bm"),
     (troop_set_slot, "trp_knight_12_3", slot_troop_banner_scene_prop, "spr_banner_bm"),
     (troop_set_slot, "trp_knight_12_4", slot_troop_banner_scene_prop, "spr_banner_bm"),
     (troop_set_slot, "trp_knight_12_5", slot_troop_banner_scene_prop, "spr_banner_bm"),
     (troop_set_slot, "trp_knight_12_6", slot_troop_banner_scene_prop, "spr_banner_bm"),
     (troop_set_slot, "trp_knight_12_7", slot_troop_banner_scene_prop, "spr_banner_bm"),
     (troop_set_slot, "trp_knight_12_8", slot_troop_banner_scene_prop, "spr_banner_bm"),
     (troop_set_slot, "trp_knight_12_9", slot_troop_banner_scene_prop, "spr_banner_bm"),
     (troop_set_slot, "trp_knight_12_10", slot_troop_banner_scene_prop, "spr_banner_bm"),
     
     (troop_set_slot, "trp_kingdom_13_lord", slot_troop_banner_scene_prop, "spr_banner_bi"),
     (troop_set_slot, "trp_knight_13_1", slot_troop_banner_scene_prop, "spr_banner_bi"),
     (troop_set_slot, "trp_knight_13_2", slot_troop_banner_scene_prop, "spr_banner_bi"),
     (troop_set_slot, "trp_knight_13_3", slot_troop_banner_scene_prop, "spr_banner_bi"),
     (troop_set_slot, "trp_knight_13_4", slot_troop_banner_scene_prop, "spr_banner_bi"),
     (troop_set_slot, "trp_knight_13_5", slot_troop_banner_scene_prop, "spr_banner_bi"),
     (troop_set_slot, "trp_knight_13_6", slot_troop_banner_scene_prop, "spr_banner_bi"),
     
     (troop_set_slot, "trp_kingdom_14_lord", slot_troop_banner_scene_prop, "spr_banner_h06"),
     (troop_set_slot, "trp_knight_14_1", slot_troop_banner_scene_prop, "spr_banner_h06"),
     (troop_set_slot, "trp_knight_14_2", slot_troop_banner_scene_prop, "spr_banner_h06"),
     (troop_set_slot, "trp_knight_14_3", slot_troop_banner_scene_prop, "spr_banner_h06"),
     (troop_set_slot, "trp_knight_14_4", slot_troop_banner_scene_prop, "spr_banner_h06"),
     (troop_set_slot, "trp_knight_14_5", slot_troop_banner_scene_prop, "spr_banner_h06"),
     (troop_set_slot, "trp_knight_14_6", slot_troop_banner_scene_prop, "spr_banner_h06"),
     
     (troop_set_slot, "trp_kingdom_15_lord", slot_troop_banner_scene_prop, "spr_banner_ce"),
     (troop_set_slot, "trp_knight_15_1", slot_troop_banner_scene_prop, "spr_banner_ce"),
     (troop_set_slot, "trp_knight_15_2", slot_troop_banner_scene_prop, "spr_banner_ce"),
     (troop_set_slot, "trp_knight_15_3", slot_troop_banner_scene_prop, "spr_banner_ce"),
     (troop_set_slot, "trp_knight_15_4", slot_troop_banner_scene_prop, "spr_banner_ce"),
     (troop_set_slot, "trp_knight_15_5", slot_troop_banner_scene_prop, "spr_banner_ce"),
     (troop_set_slot, "trp_knight_15_6", slot_troop_banner_scene_prop, "spr_banner_ce"),
     (troop_set_slot, "trp_knight_15_7", slot_troop_banner_scene_prop, "spr_banner_ce"),
     (troop_set_slot, "trp_knight_15_8", slot_troop_banner_scene_prop, "spr_banner_ce"),
     (troop_set_slot, "trp_knight_15_9", slot_troop_banner_scene_prop, "spr_banner_ce"),
     (troop_set_slot, "trp_knight_15_10", slot_troop_banner_scene_prop, "spr_banner_ce"),
     (troop_set_slot, "trp_knight_15_11", slot_troop_banner_scene_prop, "spr_banner_ce"),
     (troop_set_slot, "trp_knight_15_12", slot_troop_banner_scene_prop, "spr_banner_ce"),
     
     (troop_set_slot, "trp_kingdom_16_lord", slot_troop_banner_scene_prop, "spr_banner_cc"),
     (troop_set_slot, "trp_knight_16_1", slot_troop_banner_scene_prop, "spr_banner_cc"),
     (troop_set_slot, "trp_knight_16_2", slot_troop_banner_scene_prop, "spr_banner_cc"),
     (troop_set_slot, "trp_knight_16_3", slot_troop_banner_scene_prop, "spr_banner_cc"),
     (troop_set_slot, "trp_knight_16_4", slot_troop_banner_scene_prop, "spr_banner_cc"),
     (troop_set_slot, "trp_knight_16_5", slot_troop_banner_scene_prop, "spr_banner_cc"),
     (troop_set_slot, "trp_knight_16_6", slot_troop_banner_scene_prop, "spr_banner_cc"),
     (troop_set_slot, "trp_knight_16_7", slot_troop_banner_scene_prop, "spr_banner_cc"),
     (troop_set_slot, "trp_knight_16_8", slot_troop_banner_scene_prop, "spr_banner_cc"),
     
     (troop_set_slot, "trp_kingdom_17_lord", slot_troop_banner_scene_prop, "spr_banner_j06"),
     (troop_set_slot, "trp_knight_17_1", slot_troop_banner_scene_prop, "spr_banner_j06"),
     (troop_set_slot, "trp_knight_17_2", slot_troop_banner_scene_prop, "spr_banner_j06"),
     (troop_set_slot, "trp_knight_17_3", slot_troop_banner_scene_prop, "spr_banner_j06"),
     (troop_set_slot, "trp_knight_17_4", slot_troop_banner_scene_prop, "spr_banner_j06"),
     (troop_set_slot, "trp_knight_17_5", slot_troop_banner_scene_prop, "spr_banner_j06"),
     
     (troop_set_slot, "trp_kingdom_18_lord", slot_troop_banner_scene_prop, "spr_banner_bf"),
     (troop_set_slot, "trp_knight_18_1", slot_troop_banner_scene_prop, "spr_banner_bf"),
     (troop_set_slot, "trp_knight_18_2", slot_troop_banner_scene_prop, "spr_banner_bf"),
     
    (troop_set_slot, "trp_kingdom_19_lord", slot_troop_banner_scene_prop, "spr_banner_do"),
     (troop_set_slot, "trp_knight_19_1", slot_troop_banner_scene_prop, "spr_banner_do"),
     (troop_set_slot, "trp_knight_19_2", slot_troop_banner_scene_prop, "spr_banner_do"),
     (troop_set_slot, "trp_knight_19_3", slot_troop_banner_scene_prop, "spr_banner_do"),
     (troop_set_slot, "trp_knight_19_4", slot_troop_banner_scene_prop, "spr_banner_do"),
     (troop_set_slot, "trp_knight_19_5", slot_troop_banner_scene_prop, "spr_banner_do"),
     (troop_set_slot, "trp_knight_19_6", slot_troop_banner_scene_prop, "spr_banner_do"),
     
     (troop_set_slot, "trp_kingdom_20_lord", slot_troop_banner_scene_prop, "spr_banner_dj"),
     (troop_set_slot, "trp_knight_20_1", slot_troop_banner_scene_prop, "spr_banner_dj"),
     (troop_set_slot, "trp_knight_20_2", slot_troop_banner_scene_prop, "spr_banner_dj"),
     (troop_set_slot, "trp_knight_20_3", slot_troop_banner_scene_prop, "spr_banner_dj"),
     (troop_set_slot, "trp_knight_20_4", slot_troop_banner_scene_prop, "spr_banner_dj"),
     (troop_set_slot, "trp_knight_20_5", slot_troop_banner_scene_prop, "spr_banner_dj"),
     (troop_set_slot, "trp_knight_20_6", slot_troop_banner_scene_prop, "spr_banner_dj"),
     
     (troop_set_slot, "trp_kingdom_21_lord", slot_troop_banner_scene_prop, "spr_banner_o"),
     (troop_set_slot, "trp_knight_21_1", slot_troop_banner_scene_prop, "spr_banner_o"),
     (troop_set_slot, "trp_knight_21_2", slot_troop_banner_scene_prop, "spr_banner_o"),
     (troop_set_slot, "trp_knight_21_3", slot_troop_banner_scene_prop, "spr_banner_o"),
     (troop_set_slot, "trp_knight_21_4", slot_troop_banner_scene_prop, "spr_banner_o"),
     (troop_set_slot, "trp_knight_21_5", slot_troop_banner_scene_prop, "spr_banner_o"),
     (troop_set_slot, "trp_knight_21_6", slot_troop_banner_scene_prop, "spr_banner_o"),
     
     (troop_set_slot, "trp_kingdom_22_lord", slot_troop_banner_scene_prop, "spr_banner_h08"),
     (troop_set_slot, "trp_knight_22_1", slot_troop_banner_scene_prop, "spr_banner_h08"),
     (troop_set_slot, "trp_knight_22_2", slot_troop_banner_scene_prop, "spr_banner_h08"),
     (troop_set_slot, "trp_knight_22_3", slot_troop_banner_scene_prop, "spr_banner_h08"),
     (troop_set_slot, "trp_knight_22_4", slot_troop_banner_scene_prop, "spr_banner_h08"),
     
     (troop_set_slot, "trp_kingdom_23_lord", slot_troop_banner_scene_prop, "spr_banner_h08"),
     (troop_set_slot, "trp_knight_23_1", slot_troop_banner_scene_prop, "spr_banner_h08"),
     (troop_set_slot, "trp_knight_23_2", slot_troop_banner_scene_prop, "spr_banner_h08"),
     (troop_set_slot, "trp_knight_23_3", slot_troop_banner_scene_prop, "spr_banner_h08"),
     (troop_set_slot, "trp_knight_23_4", slot_troop_banner_scene_prop, "spr_banner_h08"),
     (troop_set_slot, "trp_knight_23_5", slot_troop_banner_scene_prop, "spr_banner_h08"),
     (troop_set_slot, "trp_knight_23_6", slot_troop_banner_scene_prop, "spr_banner_h08"),
     
     (troop_set_slot, "trp_kingdom_24_lord", slot_troop_banner_scene_prop, "spr_banner_d"),
     (troop_set_slot, "trp_knight_24_1", slot_troop_banner_scene_prop, "spr_banner_d"),
     (troop_set_slot, "trp_knight_24_2", slot_troop_banner_scene_prop, "spr_banner_d"),
     (troop_set_slot, "trp_knight_24_3", slot_troop_banner_scene_prop, "spr_banner_d"),
     (troop_set_slot, "trp_knight_24_4", slot_troop_banner_scene_prop, "spr_banner_d"),
     
     (troop_set_slot, "trp_kingdom_25_lord", slot_troop_banner_scene_prop, "spr_banner_j"),
     (troop_set_slot, "trp_knight_25_1", slot_troop_banner_scene_prop, "spr_banner_j"),
     (troop_set_slot, "trp_knight_25_2", slot_troop_banner_scene_prop, "spr_banner_j"),
     (troop_set_slot, "trp_knight_25_3", slot_troop_banner_scene_prop, "spr_banner_j"),
     
     (troop_set_slot, "trp_kingdom_26_lord", slot_troop_banner_scene_prop, "spr_banner_cg"),
     (troop_set_slot, "trp_knight_26_1", slot_troop_banner_scene_prop, "spr_banner_cg"),
     (troop_set_slot, "trp_knight_26_2", slot_troop_banner_scene_prop, "spr_banner_cg"),
     (troop_set_slot, "trp_knight_26_3", slot_troop_banner_scene_prop, "spr_banner_cg"),
     (troop_set_slot, "trp_knight_26_4", slot_troop_banner_scene_prop, "spr_banner_cg"),
     
     (troop_set_slot, "trp_kingdom_27_lord", slot_troop_banner_scene_prop, "spr_banner_ba"),
     (troop_set_slot, "trp_knight_27_1", slot_troop_banner_scene_prop, "spr_banner_ba"),
     (troop_set_slot, "trp_knight_27_2", slot_troop_banner_scene_prop, "spr_banner_ba"),
     (troop_set_slot, "trp_knight_27_3", slot_troop_banner_scene_prop, "spr_banner_ba"),
     (troop_set_slot, "trp_knight_27_4", slot_troop_banner_scene_prop, "spr_banner_ba"),
     
     (troop_set_slot, "trp_kingdom_28_lord", slot_troop_banner_scene_prop, "spr_banner_g01"),
     (troop_set_slot, "trp_knight_28_1", slot_troop_banner_scene_prop, "spr_banner_g01"),
     (troop_set_slot, "trp_knight_28_2", slot_troop_banner_scene_prop, "spr_banner_g01"),
     (troop_set_slot, "trp_knight_28_3", slot_troop_banner_scene_prop, "spr_banner_g01"),

	  #Give centers to factions first, to ensure more equal distributions
    # Generated from CSV data
    (call_script, "script_give_center_to_faction_aux", "p_town_1", "fac_kingdom_6"),
    (call_script, "script_give_center_to_lord", "p_town_1", "trp_kingdom_6_lord", 0),
    (call_script, "script_give_center_to_faction_aux", "p_town_2", "fac_kingdom_17"),
    (call_script, "script_give_center_to_lord", "p_town_2", "trp_kingdom_17_lord", 0),
    (call_script, "script_give_center_to_faction_aux", "p_town_3", "fac_kingdom_6"),
    (call_script, "script_give_center_to_lord", "p_town_3", "trp_knight_6_4", 0),
    (call_script, "script_give_center_to_faction_aux", "p_town_4", "fac_commoners"),
    (call_script, "script_give_center_to_faction_aux", "p_town_5", "fac_kingdom_6"),
    (call_script, "script_give_center_to_lord", "p_town_5", "trp_knight_6_2", 0),
    (call_script, "script_give_center_to_faction_aux", "p_town_6", "fac_kingdom_3"),
    (call_script, "script_give_center_to_lord", "p_town_6", "trp_kingdom_3_lord", 0),
    (call_script, "script_give_center_to_faction_aux", "p_town_7", "fac_kingdom_19"),
    (call_script, "script_give_center_to_lord", "p_town_7", "trp_knight_19_3", 0),
    (call_script, "script_give_center_to_faction_aux", "p_town_8", "fac_kingdom_20"),
    (call_script, "script_give_center_to_lord", "p_town_8", "trp_kingdom_20_lord", 0),
    (call_script, "script_give_center_to_faction_aux", "p_town_9", "fac_kingdom_23"),
    (call_script, "script_give_center_to_lord", "p_town_9", "trp_kingdom_23_lord", 0),
    (call_script, "script_give_center_to_faction_aux", "p_town_10", "fac_kingdom_6"),
    (call_script, "script_give_center_to_lord", "p_town_10", "trp_kingdom_6_lord", 0),
    (call_script, "script_give_center_to_faction_aux", "p_town_11", "fac_kingdom_4"),
    (call_script, "script_give_center_to_lord", "p_town_11", "trp_knight_4_1", 0),
    (call_script, "script_give_center_to_faction_aux", "p_town_12", "fac_kingdom_16"),
    (call_script, "script_give_center_to_lord", "p_town_12", "trp_kingdom_16_lord", 0),
    (call_script, "script_give_center_to_faction_aux", "p_town_13", "fac_kingdom_13"),
    (call_script, "script_give_center_to_lord", "p_town_13", "trp_kingdom_13_lord", 0),
    (call_script, "script_give_center_to_faction_aux", "p_town_14", "fac_kingdom_19"),
    (call_script, "script_give_center_to_lord", "p_town_14", "trp_kingdom_19_lord", 0),
    (call_script, "script_give_center_to_faction_aux", "p_town_15", "fac_kingdom_2"),
    (call_script, "script_give_center_to_lord", "p_town_15", "trp_kingdom_2_lord", 0),
    (call_script, "script_give_center_to_faction_aux", "p_town_16", "fac_kingdom_1"),
    (call_script, "script_give_center_to_lord", "p_town_16", "trp_kingdom_1_lord", 0),
    (call_script, "script_give_center_to_faction_aux", "p_town_17", "fac_kingdom_26"),
    (call_script, "script_give_center_to_lord", "p_town_17", "trp_kingdom_26_lord", 0),
    (call_script, "script_give_center_to_faction_aux", "p_town_18", "fac_kingdom_10"),
    (call_script, "script_give_center_to_lord", "p_town_18", "trp_kingdom_10_lord", 0),
    (call_script, "script_give_center_to_faction_aux", "p_town_19", "fac_kingdom_9"),
    (call_script, "script_give_center_to_lord", "p_town_19", "trp_kingdom_9_lord", 0),
    (call_script, "script_give_center_to_faction_aux", "p_town_20", "fac_kingdom_15"),
    (call_script, "script_give_center_to_lord", "p_town_20", "trp_kingdom_15_lord", 0),
    (call_script, "script_give_center_to_lord", "p_town_4", "trp_kingdom_28_lord", 0),
    (call_script, "script_give_center_to_faction_aux", "p_town_21", "fac_kingdom_6"),
    (call_script, "script_give_center_to_lord", "p_town_21", "trp_knight_6_19", 0),
    (call_script, "script_give_center_to_faction_aux", "p_town_22", "fac_kingdom_22"),
    (call_script, "script_give_center_to_lord", "p_town_22", "trp_kingdom_22_lord", 0),
    (call_script, "script_give_center_to_faction_aux", "p_town_23", "fac_kingdom_6"),
    (call_script, "script_give_center_to_lord", "p_town_23", "trp_kingdom_6_lord", 0),
    (call_script, "script_give_center_to_faction_aux", "p_town_24", "fac_kingdom_5"),
    (call_script, "script_give_center_to_lord", "p_town_24", "trp_kingdom_5_lord", 0),
    (call_script, "script_give_center_to_faction_aux", "p_town_25", "fac_kingdom_21"),
    (call_script, "script_give_center_to_lord", "p_town_25", "trp_kingdom_21_lord", 0),
    (call_script, "script_give_center_to_faction_aux", "p_town_26", "fac_kingdom_12"),
    (call_script, "script_give_center_to_lord", "p_town_26", "trp_kingdom_12_lord", 0),
    (call_script, "script_give_center_to_faction_aux", "p_town_27", "fac_kingdom_8"),
    (call_script, "script_give_center_to_lord", "p_town_27", "trp_kingdom_8_lord", 0),
    (call_script, "script_give_center_to_faction_aux", "p_town_28", "fac_kingdom_24"),
    (call_script, "script_give_center_to_lord", "p_town_28", "trp_kingdom_24_lord", 0),
    (call_script, "script_give_center_to_faction_aux", "p_town_29", "fac_kingdom_7"),
    (call_script, "script_give_center_to_lord", "p_town_29", "trp_kingdom_7_lord", 0),
    (call_script, "script_give_center_to_faction_aux", "p_town_30", "fac_kingdom_6"),
    (call_script, "script_give_center_to_lord", "p_town_30", "trp_kingdom_6_lord", 0),
    (call_script, "script_give_center_to_faction_aux", "p_town_31", "fac_kingdom_6"),
    (call_script, "script_give_center_to_lord", "p_town_31", "trp_kingdom_6_lord", 0),
    (call_script, "script_give_center_to_faction_aux", "p_town_32", "fac_kingdom_6"),
    (call_script, "script_give_center_to_lord", "p_town_32", "trp_kingdom_6_lord", 0),
    (call_script, "script_give_center_to_faction_aux", "p_town_33", "fac_kingdom_27"),
    (call_script, "script_give_center_to_lord", "p_town_33", "trp_kingdom_27_lord", 0),
    (call_script, "script_give_center_to_faction_aux", "p_castle_1", "fac_kingdom_6"),
    (call_script, "script_give_center_to_faction_aux", "p_castle_2", "fac_kingdom_6"),
    (call_script, "script_give_center_to_faction_aux", "p_castle_3", "fac_kingdom_6"),
    (call_script, "script_give_center_to_faction_aux", "p_castle_4", "fac_kingdom_6"),
    (call_script, "script_give_center_to_faction_aux", "p_castle_5", "fac_kingdom_24"),
    (call_script, "script_give_center_to_lord", "p_castle_5", "trp_knight_24_2", 0),
    (call_script, "script_give_center_to_faction_aux", "p_castle_6", "fac_kingdom_27"),
    (call_script, "script_give_center_to_lord", "p_castle_6", "trp_knight_27_1", 0),
    (call_script, "script_give_center_to_faction_aux", "p_castle_7", "fac_kingdom_3"),
    (call_script, "script_give_center_to_lord", "p_castle_7", "trp_kingdom_3_lord", 0),
    (call_script, "script_give_center_to_faction_aux", "p_castle_8", "fac_kingdom_1"),
    (call_script, "script_give_center_to_lord", "p_castle_8", "trp_knight_1_1", 0),
    (call_script, "script_give_center_to_faction_aux", "p_castle_9", "fac_kingdom_7"),
    (call_script, "script_give_center_to_lord", "p_castle_9", "trp_knight_7_2", 0),
    (call_script, "script_give_center_to_faction_aux", "p_castle_10", "fac_kingdom_7"),
    (call_script, "script_give_center_to_lord", "p_castle_10", "trp_kingdom_7_lord", 0),
    (call_script, "script_give_center_to_faction_aux", "p_castle_11", "fac_kingdom_23"),
    (call_script, "script_give_center_to_lord", "p_castle_11", "trp_knight_23_3", 0),
    (call_script, "script_give_center_to_faction_aux", "p_castle_12", "fac_kingdom_20"),
    (call_script, "script_give_center_to_lord", "p_castle_12", "trp_knight_20_3", 0),
    (call_script, "script_give_center_to_faction_aux", "p_castle_13", "fac_kingdom_6"),
    (call_script, "script_give_center_to_faction_aux", "p_castle_14", "fac_kingdom_25"),
    (call_script, "script_give_center_to_lord", "p_castle_14", "trp_knight_25_1", 0),
    (call_script, "script_give_center_to_faction_aux", "p_castle_15", "fac_kingdom_6"),
    (call_script, "script_give_center_to_faction_aux", "p_castle_16", "fac_kingdom_27"),
    (call_script, "script_give_center_to_lord", "p_castle_16", "trp_knight_27_3", 0),
    (call_script, "script_give_center_to_faction_aux", "p_castle_17", "fac_kingdom_6"),
    (call_script, "script_give_center_to_lord", "p_castle_17", "trp_knight_6_2", 0),
    (call_script, "script_give_center_to_faction_aux", "p_castle_18", "fac_kingdom_6"),
    (call_script, "script_give_center_to_faction_aux", "p_castle_19", "fac_kingdom_4"),
    (call_script, "script_give_center_to_lord", "p_castle_19", "trp_knight_4_2", 0),
    (call_script, "script_give_center_to_faction_aux", "p_castle_20", "fac_kingdom_4"),
    (call_script, "script_give_center_to_lord", "p_castle_20", "trp_kingdom_4_lord", 0),
    (call_script, "script_give_center_to_faction_aux", "p_castle_21", "fac_kingdom_13"),
    (call_script, "script_give_center_to_lord", "p_castle_21", "trp_knight_13_1", 0),
    (call_script, "script_give_center_to_faction_aux", "p_castle_22", "fac_kingdom_8"),
    (call_script, "script_give_center_to_lord", "p_castle_22", "trp_knight_8_2", 0),
    (call_script, "script_give_center_to_faction_aux", "p_castle_23", "fac_kingdom_4"),
    (call_script, "script_give_center_to_lord", "p_castle_23", "trp_knight_4_3", 0),
    (call_script, "script_give_center_to_faction_aux", "p_castle_24", "fac_kingdom_10"),
    (call_script, "script_give_center_to_lord", "p_castle_24", "trp_knight_10_2", 0),
    (call_script, "script_give_center_to_faction_aux", "p_castle_25", "fac_kingdom_14"),
    (call_script, "script_give_center_to_lord", "p_castle_25", "trp_knight_14_1", 0),
    (call_script, "script_give_center_to_faction_aux", "p_castle_26", "fac_kingdom_6"),
    (call_script, "script_give_center_to_faction_aux", "p_castle_27", "fac_kingdom_25"),
    (call_script, "script_give_center_to_lord", "p_castle_27", "trp_kingdom_25_lord", 0),
    (call_script, "script_give_center_to_faction_aux", "p_castle_28", "fac_kingdom_2"),
    (call_script, "script_give_center_to_lord", "p_castle_28", "trp_knight_2_2", 0),
    (call_script, "script_give_center_to_faction_aux", "p_castle_29", "fac_kingdom_26"),
    (call_script, "script_give_center_to_lord", "p_castle_29", "trp_knight_26_1", 0),
    (call_script, "script_give_center_to_faction_aux", "p_castle_30", "fac_kingdom_16"),
    (call_script, "script_give_center_to_lord", "p_castle_30", "trp_knight_16_1", 0),
    (call_script, "script_give_center_to_faction_aux", "p_castle_31", "fac_kingdom_4"),
    (call_script, "script_give_center_to_lord", "p_castle_31", "trp_kingdom_4_lord", 0),
    (call_script, "script_give_center_to_faction_aux", "p_castle_32", "fac_kingdom_20"),
    (call_script, "script_give_center_to_lord", "p_castle_32", "trp_knight_20_1", 0),
    (call_script, "script_give_center_to_faction_aux", "p_castle_33", "fac_kingdom_15"),
    (call_script, "script_give_center_to_lord", "p_castle_33", "trp_knight_15_4", 0),
    (call_script, "script_give_center_to_faction_aux", "p_castle_34", "fac_kingdom_21"),
    (call_script, "script_give_center_to_lord", "p_castle_34", "trp_knight_21_1", 0),
    (call_script, "script_give_center_to_faction_aux", "p_castle_35", "fac_kingdom_21"),
    (call_script, "script_give_center_to_lord", "p_castle_35", "trp_knight_21_3", 0),
    (call_script, "script_give_center_to_faction_aux", "p_castle_36", "fac_kingdom_15"),
    (call_script, "script_give_center_to_lord", "p_castle_36", "trp_knight_15_1", 0),
    (call_script, "script_give_center_to_faction_aux", "p_castle_37", "fac_kingdom_12"),
    (call_script, "script_give_center_to_lord", "p_castle_37", "trp_knight_12_2", 0),
    (call_script, "script_give_center_to_faction_aux", "p_castle_38", "fac_kingdom_12"),
    (call_script, "script_give_center_to_lord", "p_castle_38", "trp_knight_12_1", 0),
    (call_script, "script_give_center_to_faction_aux", "p_castle_39", "fac_kingdom_19"),
    (call_script, "script_give_center_to_lord", "p_castle_39", "trp_knight_19_2", 0),
    (call_script, "script_give_center_to_faction_aux", "p_castle_40", "fac_kingdom_24"),
    (call_script, "script_give_center_to_lord", "p_castle_40", "trp_knight_24_1", 0),
    (call_script, "script_give_center_to_faction_aux", "p_castle_41", "fac_kingdom_6"),
    (call_script, "script_give_center_to_faction_aux", "p_castle_42", "fac_kingdom_17"),
    (call_script, "script_give_center_to_lord", "p_castle_42", "trp_knight_17_1", 0),
    (call_script, "script_give_center_to_faction_aux", "p_castle_43", "fac_kingdom_19"),
    (call_script, "script_give_center_to_lord", "p_castle_43", "trp_knight_19_4", 0),
    (call_script, "script_give_center_to_faction_aux", "p_castle_44", "fac_kingdom_8"),
    (call_script, "script_give_center_to_lord", "p_castle_44", "trp_knight_8_3", 0),
    (call_script, "script_give_center_to_faction_aux", "p_castle_45", "fac_kingdom_23"),
    (call_script, "script_give_center_to_lord", "p_castle_45", "trp_knight_23_2", 0),
    (call_script, "script_give_center_to_faction_aux", "p_castle_46", "fac_kingdom_6"),
    (call_script, "script_give_center_to_faction_aux", "p_castle_47", "fac_kingdom_6"),
    (call_script, "script_give_center_to_faction_aux", "p_castle_48", "fac_kingdom_18"),
    (call_script, "script_give_center_to_lord", "p_castle_48", "trp_kingdom_18_lord", 0),
    (call_script, "script_give_center_to_faction_aux", "p_castle_49", "fac_kingdom_19"),
    (call_script, "script_give_center_to_lord", "p_castle_49", "trp_knight_19_1", 0),
    (call_script, "script_give_center_to_faction_aux", "p_castle_50", "fac_kingdom_14"),
    (call_script, "script_give_center_to_lord", "p_castle_50", "trp_kingdom_14_lord", 0),
    (call_script, "script_give_center_to_faction_aux", "p_castle_51", "fac_kingdom_1"),
    (call_script, "script_give_center_to_lord", "p_castle_51", "trp_knight_1_2", 0),
    (call_script, "script_give_center_to_faction_aux", "p_castle_52", "fac_kingdom_15"),
    (call_script, "script_give_center_to_lord", "p_castle_52", "trp_knight_15_3", 0),
    (call_script, "script_give_center_to_faction_aux", "p_castle_53", "fac_kingdom_9"),
    (call_script, "script_give_center_to_lord", "p_castle_53", "trp_knight_9_2", 0),
    (call_script, "script_give_center_to_faction_aux", "p_castle_54", "fac_kingdom_7"),
    (call_script, "script_give_center_to_lord", "p_castle_54", "trp_knight_7_1", 0),
    (call_script, "script_give_center_to_faction_aux", "p_castle_55", "fac_kingdom_12"),
    (call_script, "script_give_center_to_lord", "p_castle_55", "trp_knight_12_2", 0),
    (call_script, "script_give_center_to_faction_aux", "p_castle_56", "fac_kingdom_6"),
    (call_script, "script_give_center_to_faction_aux", "p_castle_57", "fac_kingdom_6"),
    (call_script, "script_give_center_to_faction_aux", "p_castle_58", "fac_kingdom_6"),
    (call_script, "script_give_center_to_faction_aux", "p_castle_59", "fac_kingdom_11"),
    (call_script, "script_give_center_to_lord", "p_castle_59", "trp_kingdom_11_lord", 0),
    (call_script, "script_give_center_to_faction_aux", "p_castle_60", "fac_kingdom_10"),
    (call_script, "script_give_center_to_lord", "p_castle_60", "trp_knight_10_1", 0),
    (call_script, "script_give_center_to_faction_aux", "p_castle_61", "fac_kingdom_23"),
    (call_script, "script_give_center_to_lord", "p_castle_61", "trp_knight_23_1", 0),
    (call_script, "script_give_center_to_faction_aux", "p_castle_62", "fac_kingdom_9"),
    (call_script, "script_give_center_to_lord", "p_castle_62", "trp_knight_9_1", 0),
    (call_script, "script_give_center_to_faction_aux", "p_castle_63", "fac_kingdom_15"),
    (call_script, "script_give_center_to_lord", "p_castle_63", "trp_knight_15_2", 0),
    (call_script, "script_give_center_to_faction_aux", "p_castle_64", "fac_kingdom_21"),
    (call_script, "script_give_center_to_lord", "p_castle_64", "trp_knight_21_2", 0),
    (call_script, "script_give_center_to_faction_aux", "p_castle_65", "fac_kingdom_6"),
    (call_script, "script_give_center_to_faction_aux", "p_castle_66", "fac_kingdom_7"),
    (call_script, "script_give_center_to_lord", "p_castle_66", "trp_knight_7_3", 0),
    (call_script, "script_give_center_to_faction_aux", "p_castle_67", "fac_kingdom_14"),
    (call_script, "script_give_center_to_lord", "p_castle_67", "trp_knight_14_2", 0),
    (call_script, "script_give_center_to_faction_aux", "p_castle_68", "fac_kingdom_16"),
    (call_script, "script_give_center_to_lord", "p_castle_68", "trp_knight_16_2", 0),
    (call_script, "script_give_center_to_faction_aux", "p_castle_69", "fac_kingdom_22"),
    (call_script, "script_give_center_to_lord", "p_castle_69", "trp_knight_22_1", 0),
    (call_script, "script_give_center_to_faction_aux", "p_castle_70", "fac_kingdom_8"),
    (call_script, "script_give_center_to_lord", "p_castle_70", "trp_knight_8_1", 0),
    (call_script, "script_give_center_to_faction_aux", "p_castle_71", "fac_kingdom_6"),
    (call_script, "script_give_center_to_faction_aux", "p_castle_72", "fac_kingdom_23"),
    (call_script, "script_give_center_to_lord", "p_castle_72", "trp_knight_23_4", 0),
    (call_script, "script_give_center_to_faction_aux", "p_castle_73", "fac_kingdom_23"),
    (call_script, "script_give_center_to_lord", "p_castle_73", "trp_knight_23_5", 0),
    (call_script, "script_give_center_to_faction_aux", "p_castle_74", "fac_kingdom_3"),
    (call_script, "script_give_center_to_lord", "p_castle_74", "trp_knight_3_1", 0),
    (call_script, "script_give_center_to_faction_aux", "p_castle_75", "fac_kingdom_27"),
    (call_script, "script_give_center_to_lord", "p_castle_75", "trp_knight_27_2", 0),
    (call_script, "script_give_center_to_faction_aux", "p_castle_76", "fac_kingdom_20"),
    (call_script, "script_give_center_to_lord", "p_castle_76", "trp_knight_20_2", 0),
    (call_script, "script_give_center_to_faction_aux", "p_castle_77", "fac_kingdom_5"),
    (call_script, "script_give_center_to_lord", "p_castle_77", "trp_knight_5_1", 0),
    (call_script, "script_give_center_to_faction_aux", "p_castle_78", "fac_kingdom_17"),
    (call_script, "script_give_center_to_lord", "p_castle_78", "trp_knight_17_2", 0),
    (call_script, "script_give_center_to_faction_aux", "p_castle_79", "fac_kingdom_6"),
    (call_script, "script_give_center_to_faction_aux", "p_castle_80", "fac_kingdom_1"),
    (call_script, "script_give_center_to_lord", "p_castle_80", "trp_knight_1_3", 0),
    (call_script, "script_give_center_to_faction_aux", "p_castle_81", "fac_kingdom_2"),
    (call_script, "script_give_center_to_lord", "p_castle_81", "trp_knight_2_1", 0),
    (call_script, "script_give_center_to_faction_aux", "p_castle_82", "fac_kingdom_25"),
    (call_script, "script_give_center_to_lord", "p_castle_82", "trp_knight_25_2", 0),
    (call_script, "script_give_center_to_faction_aux", "p_castle_83", "fac_kingdom_26"),
    (call_script, "script_give_center_to_lord", "p_castle_83", "trp_knight_26_2", 0),
    (call_script, "script_give_center_to_faction_aux", "p_castle_84", "fac_kingdom_8"),
    (call_script, "script_give_center_to_lord", "p_castle_84", "trp_knight_8_4", 0),
    (call_script, "script_give_center_to_faction_aux", "p_castle_85", "fac_kingdom_5"),
    (call_script, "script_give_center_to_lord", "p_castle_85", "trp_knight_5_2", 0),
    (call_script, "script_give_center_to_faction_aux", "p_castle_86", "fac_kingdom_6"),
    (call_script, "script_give_center_to_lord", "p_castle_86", "trp_knight_6_3", 0),

    ##diplomacy start+
    #Add home centers for claimants
      (troop_set_slot, "trp_kingdom_1_pretender", slot_troop_home, "p_town_10"),#Lady Yamanouchi - Niigata
      (troop_set_slot, "trp_kingdom_2_pretender", slot_troop_home, "p_town_16"),#Lord Tamura - Yonezawa
      (troop_set_slot, "trp_kingdom_3_pretender", slot_troop_home, "p_town_9"),#Lord Saito - Kiyosu
      (troop_set_slot, "trp_kingdom_4_pretender", slot_troop_home, "p_town_27"),#Lord Ouchi - Yamaguchi
      (troop_set_slot, "trp_kingdom_5_pretender", slot_troop_home, "p_town_11"),#Lord Takeda - Kofu
      (troop_set_slot, "trp_kingdom_6_pretender", slot_troop_home, "p_town_4"),#Lady Imagawa - Hamamatsu
    #Also the primary six towns:
      #(troop_set_slot, "trp_kingdom_1_lord", slot_troop_home, "p_town_12"),#Kenshin to #Kasugayama
      #(troop_set_slot, "trp_kingdom_2_lord", slot_troop_home, "p_town_15"),#Masamune to Sendai
      #(troop_set_slot, "trp_kingdom_3_lord", slot_troop_home, "p_town_9"),#Nobunaga to Kiyosu
      #(troop_set_slot, "trp_kingdom_4_lord", slot_troop_home, "p_town_13"),#Motonari to #Hiroshima
      #(troop_set_slot, "trp_kingdom_5_lord", slot_troop_home, "p_town_11"),#Shingen to Kofu
      #(troop_set_slot, "trp_kingdom_6_lord", slot_troop_home, "p_town_25"),#Ieyasu to Hamamatsu
    
    ##Also set home slots for starting quest merchants (merchant of praven, merchant of reyvadin, etc.)
    (try_for_range, ":npc", major_kings_begin, major_kings_end),
       (troop_get_slot, ":center_no", ":npc", slot_troop_home),
       (val_sub, ":npc", major_kings_begin),
       (val_add, ":npc", startup_merchants_begin),
       (is_between, ":npc", startup_merchants_begin, startup_merchants_end),#Right now there's a startup merchant for each faction.  Verify this hasn't unexpectedly changed.
       (neg|troop_slot_ge, ":npc", slot_troop_home, 1),#Verify that the home slot is not already set
       (troop_set_slot, ":npc", slot_troop_home, ":center_no"),
    (try_end),
    ##diplomacy end+
	  
    #  (call_script, "script_assign_lords_to_empty_centers"),
	  	  
	  #set original factions
      (try_for_range, ":center_no", centers_begin, centers_end),
        (store_faction_of_party, ":original_faction", ":center_no"),
        (faction_get_slot, ":culture", ":original_faction", slot_faction_culture),
        (party_set_slot, ":center_no", slot_center_culture,  ":culture"),
        (party_set_slot, ":center_no", slot_center_original_faction,  ":original_faction"),
        (party_set_slot, ":center_no", slot_center_ex_faction,  ":original_faction"),
		##diplomacy start+ set additional slots
		(party_get_slot, ":town_lord", ":center_no", slot_town_lord),

		(try_begin),
			(eq, ":town_lord", "trp_player"),
			#Use trp_kingdom_heroes_including_player_begin instead of trp_player as a workaround for
			#old saved games (since uninitialized memory is 0).
			(party_set_slot, ":center_no", dplmc_slot_center_ex_lord, "trp_kingdom_heroes_including_player_begin"),
			(troop_slot_eq, "trp_player", slot_troop_home, ":center_no"),
			(neg|party_slot_ge, ":center_no", dplmc_slot_center_original_lord, 1),
			(party_set_slot, ":center_no", dplmc_slot_center_original_lord, "trp_kingdom_heroes_including_player_begin"),
		(else_try),
			(party_set_slot, ":center_no", dplmc_slot_center_ex_lord, ":town_lord"),
			(ge, ":town_lord", 0),
			(troop_slot_eq, ":town_lord", slot_troop_home, ":center_no"),
			(neg|party_slot_ge, ":center_no", dplmc_slot_center_original_lord, 1),
			(party_set_slot, ":center_no", dplmc_slot_center_original_lord, ":town_lord"),
		(try_end),
		##diplomacy end+
      (try_end),

	  #gekokujo 2.1 new, balanced territorial issues
	  ##set territorial disputes/outstanding border issues 
	  #(party_set_slot, "p_castle_19", slot_center_ex_faction, "fac_kingdom_1"), #uesugi claims takeda-held kaizu castle
	  #(party_set_slot, "p_castle_32", slot_center_ex_faction, "fac_kingdom_2"), #date claims nanbu-held ichinoseki castle
	  #(party_set_slot, "p_castle_8", slot_center_ex_faction, "fac_kingdom_3"), #oda claims asakura-held kannonji castle
	  #(party_set_slot, "p_town_4", slot_center_ex_faction, "fac_kingdom_3"), #oda claims miyoshi-held kyoto
	  #(party_set_slot, "p_town_28", slot_center_ex_faction, "fac_kingdom_4"), #mori claims yamana-held izumo
	  #(party_set_slot, "p_castle_56", slot_center_ex_faction, "fac_kingdom_5"), #takeda claims oda-held iwamura castle
	  #(party_set_slot, "p_castle_55", slot_center_ex_faction, "fac_kingdom_5"), #takeda claims tokugawa-held nagashino castle
	  #(party_set_slot, "p_castle_53", slot_center_ex_faction, "fac_kingdom_6"), #tokugawa claims takeda-held sunpu castle
	  #(party_set_slot, "p_castle_67", slot_center_ex_faction, "fac_kingdom_7"), #miyoshi claims chosokabe-held muroto castle
	  #(party_set_slot, "p_castle_6", slot_center_ex_faction, "fac_kingdom_8"), #amako claims miyoshi-held kobe castle
	  #(party_set_slot, "p_castle_29", slot_center_ex_faction, "fac_kingdom_9"), #otomo claims mori-held kushizake castle
	  #(party_set_slot, "p_town_29", slot_center_ex_faction, "fac_kingdom_15"), #shimazu claims otomo-held funai
	  #(party_set_slot, "p_town_17", slot_center_ex_faction, "fac_kingdom_10"), #nanbu claims mogami-held kubota
	  #(party_set_slot, "p_castle_68", slot_center_ex_faction, "fac_kingdom_12"), #chosokabe claims miyoshi-held kawanoe castle
	  #(party_set_slot, "p_castle_50", slot_center_ex_faction, "fac_kingdom_13"), #hojo claims satomi-held konodai castle
	  #(party_set_slot, "p_castle_18", slot_center_ex_faction, "fac_kingdom_14"), #mogami claims uesugi-held shibata castle
	  #(party_set_slot, "p_town_30", slot_center_ex_faction, "fac_kingdom_9"), #otomo claims shimazu-held kumamoto
	  #(party_set_slot, "p_castle_34", slot_center_ex_faction, "fac_kingdom_17"), #satake claims date-held shirakawa castle
	  #(party_set_slot, "p_town_2", slot_center_ex_faction, "fac_kingdom_18"), #satomi claims satake-held mito  	  	  	  
	  ##ikko, ryuzoji, and asakura try to mind their own business
	  (party_set_slot, "p_castle_3", slot_center_ex_faction, "fac_kingdom_1"), #uesugi claims hojo-held takasaki castle
	  (party_set_slot, "p_castle_62", slot_center_ex_faction, "fac_kingdom_1"), #uesugi claims date-held kurokawa castle
	  (party_set_slot, "p_castle_33", slot_center_ex_faction, "fac_kingdom_2"), #date claims mogami-held yamagata castle
	  (party_set_slot, "p_town_4", slot_center_ex_faction, "fac_kingdom_3"), #oda claims miyoshi-held kyoto
	  #(party_set_slot, "p_castle_10", slot_center_ex_faction, "fac_kingdom_3"), #oda claims asakura-held odani castle #gekokujo 3.0 excessive
	  (party_set_slot, "p_castle_12", slot_center_ex_faction, "fac_kingdom_3"), #oda claims asakura-held tsu castle #gekokujo 3.0 excessive
	  (party_set_slot, "p_castle_27", slot_center_ex_faction, "fac_kingdom_4"), #mori claims ukita-held mihara castle
	  (party_set_slot, "p_castle_69", slot_center_ex_faction, "fac_kingdom_5"), #takeda claims uesugi-held otari castle
	  (party_set_slot, "p_castle_56", slot_center_ex_faction, "fac_kingdom_5"), #takeda claims oda-held iwamura castle
	  (party_set_slot, "p_castle_55", slot_center_ex_faction, "fac_kingdom_5"), #takeda claims tokugawa-held nagashino castle
	  (party_set_slot, "p_castle_53", slot_center_ex_faction, "fac_kingdom_6"), #tokugawa claims takeda-held sunpu castle
	  #(party_set_slot, "p_castle_12", slot_center_ex_faction, "fac_kingdom_7"), #miyoshi claims asakura-held tsu castle #gekokujo 3.0 excessive
	  (party_set_slot, "p_castle_8", slot_center_ex_faction, "fac_kingdom_7"), #miyoshi claims asakura-held kannonji castle
	  (party_set_slot, "p_castle_67", slot_center_ex_faction, "fac_kingdom_7"), #miyoshi claims chosokabe-held muroto caslte
	  (party_set_slot, "p_castle_51", slot_center_ex_faction, "fac_kingdom_7"), #miyoshi claims ukita-held akashi-castle
	  (party_set_slot, "p_castle_25", slot_center_ex_faction, "fac_kingdom_8"), #amako claims mori-held hamada castle
	  (party_set_slot, "p_castle_29", slot_center_ex_faction, "fac_kingdom_9"), #otomo claims mori-held kushizaki castle
	  (party_set_slot, "p_castle_32", slot_center_ex_faction, "fac_kingdom_10"), #nanbu claims date-held ichinoseki castle
	  (party_set_slot, "p_castle_68", slot_center_ex_faction, "fac_kingdom_12"), #chosokabe claims miyoshi-held kawanoe castle
	  (party_set_slot, "p_castle_24", slot_center_ex_faction, "fac_kingdom_13"), #hojo claims takeda-held yoshiwara castle
	  (party_set_slot, "p_castle_2", slot_center_ex_faction, "fac_kingdom_13"), #hojo claims satake-held utsunomiya castle
	  (party_set_slot, "p_castle_50", slot_center_ex_faction, "fac_kingdom_13"), #hojo claims satomi-held konodai castle
	  (party_set_slot, "p_castle_18", slot_center_ex_faction, "fac_kingdom_14"), #mogami claims uesugi-held shibata castle
	  (party_set_slot, "p_town_18", slot_center_ex_faction, "fac_kingdom_14"), #mogami claims nanbu-held hirosaki
	  (party_set_slot, "p_town_29", slot_center_ex_faction, "fac_kingdom_15"), #shimazu claims otomo-held funai
	  (party_set_slot, "p_town_21", slot_center_ex_faction, "fac_kingdom_15"), #shimazu claims ryuzoji-held nagasaki
	  (party_set_slot, "p_castle_44", slot_center_ex_faction, "fac_kingdom_16"), #ryuzoji claims otomo-held yanagawa castle
	  (party_set_slot, "p_castle_34", slot_center_ex_faction, "fac_kingdom_17"), #satake claims date-held shirakawa castle
	  (party_set_slot, "p_town_2", slot_center_ex_faction, "fac_kingdom_18"), #satomi claims satake-held mito
	  (party_set_slot, "p_castle_52", slot_center_ex_faction, "fac_kingdom_19"), #ukita claims amako-held fukuchiyama castle
	  
	  (party_set_slot, "p_castle_72", slot_center_ex_faction, "fac_kingdom_3"), #oda claims ikko-held nagashima	fortress
	  (party_set_slot, "p_castle_74", slot_center_ex_faction, "fac_kingdom_6"), #tokugawa claims ikko-held ishiyama	fortress
	  (party_set_slot, "p_castle_75", slot_center_ex_faction, "fac_kingdom_7"), #miyoshi claims ikko-held jogu-ji fortress
	  
	  
      (call_script, "script_update_village_market_towns"),	  

	  ##diplomacy start+
	  #(1) Assign plausible ancestral homes to some of the lords (not all of them) who didn't have
      #one set before.  Among other things, this is used for a sense of possessiveness.
      #(2) Assign last-transfer-times to the contested centers.
      (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
		 (try_begin),
			#Assign last-transfer-times to the contested centers.
			(party_get_slot, ":original_faction", ":center_no", slot_center_original_faction),
			(neg|party_slot_eq, ":center_no", slot_center_ex_faction, ":original_faction"),
			(store_random_in_range, ":transfer_time", 1, 181),#some time in the last 180 days (the length of a short game)
			(val_mul, ":transfer_time", -24),
			(party_set_slot, ":center_no", dplmc_slot_center_last_transfer_time, ":transfer_time"),
		 (else_try),
			#For non-contested centers, possibly set the lord's home slot.  Note that because
			#we're iterating in order, lords will get set to towns they own before they get
			#set to cities.
			(party_get_slot, ":town_lord", ":center_no", slot_town_lord),
			(ge, ":town_lord", 1),#only NPCs
			(neg|party_slot_ge, ":center_no", dplmc_slot_center_original_lord, 1),#If there is an original owner who is dispossessed, such as a claimant
			(neg|troop_slot_ge, ":town_lord", slot_troop_home, 1),
			(troop_set_slot, ":town_lord", slot_troop_home, ":center_no"),
		 (try_end),
      (try_end),

	  (try_for_range, ":troop_id", heroes_begin, heroes_end),
	  (try_end),
      #
      #etc.
      (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
		 #If the original owner of the lord is set, don't apply this
		 (neg|party_slot_ge, ":center_no", dplmc_slot_center_original_lord, 1),
		 #Don't apply this to contested centers.
		 (party_get_slot, ":original_faction", ":center_no", slot_center_original_faction),
		 (party_slot_eq, ":center_no", slot_center_ex_faction, ":original_faction"),
		 #If the owner already has his "home" slot set, don't overwrite it
         (party_get_slot, ":town_lord", ":center_no", slot_town_lord),
         (ge, ":town_lord", 1),#only NPCs
		 (neg|troop_slot_ge, ":town_lord", slot_troop_home, 1),
		 #No objections, so go ahead
		 (troop_set_slot, ":town_lord", slot_troop_home, ":center_no"),
      (try_end),
      ##diplomacy end+

	  #this should come after assignment of territorial grievances
      (try_for_range, ":unused", 0, 70),
        (try_begin),
          (eq, "$cheat_mode", 1),
          (display_message, "@{!}DEBUG -- initial war/peace check begins"),
        (try_end),
        (call_script, "script_randomly_start_war_peace_new", 0),
      (try_end),

	  
      #Initialize walkers
      (try_for_range, ":center_no", centers_begin, centers_end),
        (this_or_next|party_slot_eq, ":center_no", slot_party_type, spt_town),
                     (party_slot_eq, ":center_no", slot_party_type, spt_village),
        (try_for_range, ":walker_no", 0, num_town_walkers),
          (call_script, "script_center_set_walker_to_type", ":center_no", ":walker_no", walkert_default),
        (try_end),
      (try_end),

	  	  
	  #This needs to be after market towns
	  (call_script, "script_initialize_economic_information"),

	  (try_for_range, ":village_no", villages_begin, villages_end),	        
        (call_script, "script_refresh_village_merchant_inventory", ":village_no"),
      (try_end),	  
	  	  	  	 
      (try_for_range, ":troop_id", original_kingdom_heroes_begin, active_npcs_end),
        (try_begin),
          (store_troop_faction, ":faction_id", ":troop_id"),
          (is_between, ":faction_id", kingdoms_begin, kingdoms_end),
          (troop_set_slot, ":troop_id", slot_troop_original_faction, ":faction_id"),
          (try_begin),
            (is_between, ":troop_id", pretenders_begin, pretenders_end),
            (faction_set_slot, ":faction_id", slot_faction_has_rebellion_chance, 1),			
          (try_end),
        (try_end),
        (assign, ":initial_wealth", 6000),
        (try_begin),
          (store_troop_faction, ":faction", ":troop_id"),
          (faction_slot_eq, ":faction", slot_faction_leader, ":troop_id"),
          (assign, ":initial_wealth", 20000),
        (try_end),
        (troop_set_slot, ":troop_id", slot_troop_wealth, ":initial_wealth"),
      (try_end),

      (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),#add town garrisons
        #Add initial center wealth
        (assign, ":initial_wealth", 2000),
        (try_begin),
          (is_between, ":center_no", towns_begin, towns_end),
          (val_mul, ":initial_wealth", 2),
        (try_end),
        (party_set_slot, ":center_no", slot_town_wealth, ":initial_wealth"),
      
		#gekokujo 3.0 garrison increase
        #(assign, ":garrison_strength", 15),
        (assign, ":garrison_strength", 20),
		
        (try_begin),
          (party_slot_eq, ":center_no", slot_party_type, spt_town),
		  #gekokujo 3.0 garrison increase
          #(assign, ":garrison_strength", 40), 
          (assign, ":garrison_strength", 50), 
        (try_end),
		
		#gekokujo 3.0 ikko increased garrisons start
		(store_faction_of_party, ":garrison_faction", ":center_no"),
		(try_begin),
		  (eq, ":garrison_faction", "fac_kingdom_20"),
          (try_begin),
            (party_slot_eq, ":center_no", slot_party_type, spt_town),
            (assign, ":garrison_strength", 65),
		  (else_try),
            (assign, ":garrison_strength", 25),
          (try_end),
        (try_end),
		#gekokujo 3.0 ikko increased garrisons end
		
        (try_for_range, ":unused", 0, ":garrison_strength"),
          (call_script, "script_cf_reinforce_party", ":center_no"),
        (try_end),
        ## ADD some XP initially
        (store_div, ":xp_rounds", ":garrison_strength", 5),
        (val_add, ":xp_rounds", 2),
        
        (game_get_reduce_campaign_ai, ":reduce_campaign_ai"),                
        
        (try_begin), #hard
          (eq, ":reduce_campaign_ai", 0),
          (assign, ":xp_addition_for_centers", 7500),
        (else_try), #moderate
          (eq, ":reduce_campaign_ai", 1),
          (assign, ":xp_addition_for_centers", 5000),
        (else_try), #easy
          (eq, ":reduce_campaign_ai", 2),
          (assign, ":xp_addition_for_centers", 2500),
        (try_end),
        
        (try_for_range, ":unused", 0, ":xp_rounds"),          
          (party_upgrade_with_xp, ":center_no", ":xp_addition_for_centers", 0),
        (try_end),

        #Fill town food stores upto half the limit
        (call_script, "script_center_get_food_store_limit", ":center_no"),
        (assign, ":food_store_limit", reg0),
        (val_div, ":food_store_limit", 2),
        (party_set_slot, ":center_no", slot_party_food_store, ":food_store_limit"),

        #create lord parties
        (party_get_slot, ":center_lord", ":center_no", slot_town_lord),
        (ge, ":center_lord", 1),
        (troop_slot_eq, ":center_lord", slot_troop_leaded_party, 0),
		(assign, "$g_there_is_no_avaliable_centers", 0),
        (call_script, "script_create_kingdom_hero_party", ":center_lord", ":center_no"),
        (assign, ":lords_party", "$pout_party"),
        (party_attach_to_party, ":lords_party", ":center_no"),
        (party_set_slot, ":center_no", slot_town_player_odds, 1000),
      (try_end),
		
	#More pre-Warband family structures removed here

	  #Warband changes begin - set companions relations
	  #gekokujo 3.0 microfactions! include fort companions start
	  #(try_for_range, ":companion", companions_begin, companions_end),
		#(try_for_range, ":other_companion", companions_begin, companions_end),
	  (try_for_range, ":companion", companions_begin, fort_companions_end),
		(try_for_range, ":other_companion", companions_begin, fort_companions_end),
	  #gekokujo 3.0 microfactions! include fort companions end
			(neq, ":other_companion", ":companion"),
			(neg|troop_slot_eq, ":companion", slot_troop_personalityclash_object, ":other_companion"),
			(neg|troop_slot_eq, ":companion", slot_troop_personalityclash2_object, ":other_companion"),
			(call_script, "script_troop_change_relation_with_troop", ":companion", ":other_companion", 7), #companions have a starting relation of 14, unless they are rivals
		(try_end),
	  (try_end),	
	
	  #Warband changes continue -  sets relations in the same faction
      (try_for_range, ":lord", original_kingdom_heroes_begin, active_npcs_end),
		(troop_slot_eq, ":lord", slot_troop_occupation, slto_kingdom_hero),
		(troop_get_slot, ":lord_faction", ":lord", slot_troop_original_faction),
				
		(try_for_range, ":other_hero", original_kingdom_heroes_begin, active_npcs_end),
			(this_or_next|troop_slot_eq, ":other_hero", slot_troop_occupation, slto_kingdom_hero),
				(troop_slot_eq, ":other_hero", slot_troop_occupation, slto_inactive_pretender),
			(troop_get_slot, ":other_hero_faction", ":other_hero", slot_troop_original_faction),
			(eq, ":other_hero_faction", ":lord_faction"),
			(call_script, "script_troop_get_family_relation_to_troop", ":lord", ":other_hero"),
			(call_script, "script_troop_change_relation_with_troop", ":lord", ":other_hero", reg0),
			
			(store_random_in_range, ":random", 0, 11), #this will be scored twice between two kingdom heroes, so starting relation will average 10. Between lords and pretenders it will average 7.5
			(call_script, "script_troop_change_relation_with_troop", ":lord", ":other_hero", ":random"),
		(try_end),		
	  (try_end),
	  
	  ##diplomacy start+
     ##Initialize town "last caravan arrived" times randomly
	  (try_for_range, ":cur_town", towns_begin, towns_end),
	     (try_for_range, ":cur_slot", dplmc_slot_town_trade_route_last_arrivals_begin, dplmc_slot_town_trade_route_last_arrivals_end),
		    (party_slot_eq, ":cur_town", ":cur_slot", 0),
		    (store_random_in_range, ":last_arrived", 1, (24 * 7 * 5) + 1),#some time in the last five weeks
			(val_mul, ":last_arrived", -1),
			(party_get_slot, ":prosperity_factor", ":cur_town", slot_town_prosperity),#modify plus or minus 40% based on prosperity
			(val_clamp, ":prosperity_factor", 0, 101),
			(val_add, ":prosperity_factor", 75),
			(val_mul, ":last_arrived", 125),
			(val_div, ":last_arrived", ":prosperity_factor"),#last arrival some time in the last five weeks, plus or minus 40%
			(party_set_slot, ":cur_town", ":cur_slot", ":last_arrived"),
		 (try_end),
	  (try_end),
      (try_for_range, ":cur_village", villages_begin, villages_end),
          (party_get_slot, ":prosperity_factor", ":cur_town", slot_town_prosperity),#modify plus or minus 40% based on prosperity
          (val_clamp, ":prosperity_factor", 0, 101),
          (val_add, ":prosperity_factor", 75),#average 125, min 75, max 175
          (store_random_in_range, ":last_arrived", 1, (24 * 7) + 1),
          (val_mul, ":last_arrived", -1),#some time in the last 7 days, plus or minus 40%
          (val_mul, ":last_arrived", 125),
          (val_div, ":last_arrived", ":prosperity_factor"),
          (party_set_slot, ":cur_village", dplmc_slot_village_trade_last_returned_from_market, ":last_arrived"),
          (store_random_in_range, ":last_arrived", 1, (24 * 7) + 1),
          (val_mul, ":last_arrived", -1),#some time in the last 7 days
          (val_mul, ":last_arrived", 125),
          (val_div, ":last_arrived", ":prosperity_factor"),
          (party_set_slot, ":cur_village", dplmc_slot_village_trade_last_arrived_to_market, ":last_arrived"),
      (try_end),
      ##diplomacy end+

	  #do about 5 years' worth of political history (assuming 3 random checks a day)
	  (try_for_range, ":unused", 0, 5000),
		(call_script, "script_cf_random_political_event"),
	  (try_end),
#	  #gekokujo 3.0 new random political event script start
#	  #do about 3 years' worth of political history (assuming 2 random checks a day)
#	  (try_for_range, ":unused", 0, 2000),
#		(call_script, "script_cf_random_political_event"),
#	  (try_end),
#	  #gekokujo 3.0 new random political event script end
	  (assign, "$total_random_quarrel_changes", 0),
	  (assign, "$total_relation_adds", 0),
	  (assign, "$total_relation_subs", 0),
	  
	  #gekokujo 3.0 oda and tokugawa start as allies
      (set_show_messages, 0), #gekokujo 3.1 oda and tokugawa alliance no longer shows a message at game start
	  (call_script, "script_dplmc_start_alliance_between_kingdoms", "fac_kingdom_3", "fac_kingdom_6", 0),
      (set_show_messages, 1), #gekokujo 3.1 oda and tokugawa alliance no longer shows a message at game start
	  
	  (try_for_range, ":kingdom", kingdoms_begin, kingdoms_end),
		(call_script, "script_evaluate_realm_stability", ":kingdom"),
		#(faction_set_slot, ":kingdom", slot_faction_last_feast_time, -264),
	  (try_end),
	  #Warband changes end
	  
	  (try_begin),
	    (eq, "$cheat_mode", 1),
	    (assign, reg3, "$cheat_mode"),
	    (display_message, "@{!}DEBUG : Completed political events, cheat mode: {reg3}"),
	  (try_end),

	  #assign love interests to unmarried male lords
	  (try_for_range, ":cur_troop", lords_begin, lords_end),
	    (troop_slot_eq, ":cur_troop", slot_troop_spouse, -1),
	    ##diplomacy start+ Also bypass this for characters that start with manually-assigned fiancees
	    (troop_slot_eq, ":cur_troop", slot_troop_betrothed, -1),
	    ##diplomacy end+
		(neg|is_between, ":cur_troop", kings_begin, kings_end),
		(neg|is_between, ":cur_troop", pretenders_begin, pretenders_end),
		
		(call_script, "script_assign_troop_love_interests", ":cur_troop"),
	  (try_end),

	  (store_random_in_range, "$romantic_attraction_seed", 0, 5),
	  
	  (try_begin),
	    (eq, "$cheat_mode", 1),
	    (assign, reg3, "$romantic_attraction_seed"),
	    (display_message, "@{!}DEBUG : Assigned love interests. Attraction seed: {reg3}"),
	  (try_end),
	  
	  #we need to spawn more bandits in warband, because map is bigger.
      #(try_for_range, ":unused", 0, 7),
      #  (call_script, "script_spawn_bandits"),
      #(try_end),

      #(set_spawn_radius, 50),
      #(try_for_range, ":unused", 0, 25),
      #  (spawn_around_party, "p_main_party", "pt_looters"),
      #(try_end),
	  	  
      (try_for_range, ":unused", 0, 10),
        (call_script, "script_spawn_bandits"),
      (try_end),

      #we are adding looter parties around each village with 1/5 probability.
      (set_spawn_radius, 5),
      (try_for_range, ":cur_village", villages_begin, villages_end),
        (store_random_in_range, ":random_value", 0, 5),               
        (eq, ":random_value", 0),
        (spawn_around_party, ":cur_village", "pt_looters"),
      (try_end),

      (call_script, "script_update_mercenary_units_of_towns"),
      (call_script, "script_update_companion_candidates_in_taverns"),
      (call_script, "script_update_ransom_brokers"),
      (call_script, "script_update_tavern_travellers"),
      (call_script, "script_update_tavern_minstrels"),
      (call_script, "script_update_booksellers"),

	  #Gekokujo Update Cities for Recruitment
      #(try_for_range, ":village_no", villages_begin, villages_end),
      (try_for_range, ":center_no", centers_begin, centers_end),
        (call_script, "script_update_volunteer_troops_in_village", ":center_no"),
      (try_end),
	  
      (try_for_range, ":cur_kingdom", kingdoms_begin, kingdoms_end),
        (call_script, "script_update_faction_notes", ":cur_kingdom"),
        (store_random_in_range, ":random_no", -60, 0),
        ##diplomacy start+
        #The above is a random time in the last 60 hours, but that's probably a mistake.
        #Change to a time within the last 60 days.
        (val_mul, ":random_no", 24),
        ##diplomacy end+
        (faction_set_slot, ":faction_no", slot_faction_last_offensive_concluded, ":random_no"),
      (try_end),
	  
      (try_for_range, ":cur_troop", original_kingdom_heroes_begin, active_npcs_end),
        (call_script, "script_update_troop_notes", ":cur_troop"),
      (try_end),

      (try_for_range, ":cur_center", centers_begin, centers_end),
        ##diplomacy start+
        (party_get_slot, ":original_faction", ":center_no", slot_center_original_faction),
        (try_begin),
           #Assign plausible last-transfer-times to the contested centers based
           #on the "last offensive concluded" slot of the controlling faction.
           (is_between, ":original_faction", kingdoms_begin, kingdoms_end),
           (neg|party_slot_eq, ":center_no", slot_center_ex_faction, ":original_faction"),
           (faction_get_slot, reg0, ":original_faction", slot_faction_last_offensive_concluded),
           (party_set_slot, ":center_no", dplmc_slot_center_last_transfer_time, reg0),
        (try_end),
        ##diplomacy end+
        (call_script, "script_update_center_notes", ":cur_center"),
      (try_end),
	  
      (call_script, "script_update_troop_notes", "trp_player"),

	  #Place kingdom ladies
      (try_for_range, ":troop_id", kingdom_ladies_begin, kingdom_ladies_end),
		(call_script, "script_get_kingdom_lady_social_determinants", ":troop_id"),
		(troop_set_slot, ":troop_id", slot_troop_cur_center, reg1),
		##diplomacy start+
		#Set their original faction.
		(ge, reg0, 0),
		(troop_get_slot, ":original_faction", reg0, slot_troop_original_faction),
		(troop_set_slot, ":troop_id", slot_troop_original_faction, ":original_faction"),
		##diplomacy end+
	  (try_end),
	  
	  ##diplomacy start+
	  ##Set initial relations between kingdom ladies and their relatives.
	  ##Do *not* initialize their relations with anyone they aren't related to:
	  ##that is used for courtship.
	  ##  The purpose of this initialization is so if a kingdom lady gets promoted,
	  ##her relations aren't a featureless slate.  Also, it would be interesting to
	  ##further develop the idea of ladies as pursuing agendas even if they aren't
	  ##leading warbands, which would benefit from giving them relations with other
	  ##people.
     (try_for_range, ":lady", kingdom_ladies_begin, kingdom_ladies_end),
		(troop_slot_eq, ":lady", slot_troop_occupation, slto_kingdom_lady),
		(troop_get_slot, ":lady_faction", ":lady", slot_troop_original_faction),

		(try_for_range, ":other_hero", heroes_begin, heroes_end),
		   (this_or_next|troop_slot_eq, ":other_hero", slot_troop_occupation, slto_kingdom_lady),
			(this_or_next|troop_slot_eq, ":other_hero", slot_troop_occupation, slto_kingdom_hero),
				(troop_slot_eq, ":other_hero", slot_troop_occupation, slto_inactive_pretender),
			(troop_slot_eq, ":other_hero", slot_troop_original_faction, ":lady_faction"),

			(neq, ":other_hero", ":lady"),
			(try_begin),
			   (this_or_next|troop_slot_eq, ":lady", slot_troop_spouse, ":other_hero"),
				   (troop_slot_eq, ":other_hero", slot_troop_spouse, ":lady"),
				(store_random_in_range, reg0, 0, 11),
			(else_try),
			   (call_script, "script_troop_get_family_relation_to_troop", ":lady", ":other_hero"),
			(try_end),
			(call_script, "script_troop_change_relation_with_troop", ":lady", ":other_hero", reg0),

			#This relation change only applies between kingdom ladies.
			(troop_slot_eq, ":other_hero", slot_troop_occupation, slto_kingdom_lady),
			(is_between, ":other_hero", kingdom_ladies_begin, kingdom_ladies_end),

			(store_random_in_range, ":random", 0, 11),
			(call_script, "script_troop_change_relation_with_troop", ":lady", ":other_hero", ":random"),
		(try_end),
	  (try_end),
	  ##diplomacy end+
	  
	  
	  (try_begin),
	    (eq, "$cheat_mode", 1),
	    (assign, reg3, "$cheat_mode"),
	    (display_message, "@{!}DEBUG : Located kingdom ladies, cheat mode: {reg3}"),
	  (try_end),
	  
      (try_for_range, ":faction_no", kingdoms_begin, kingdoms_end),
        (call_script, "script_faction_recalculate_strength", ":faction_no"),
      (try_end),

	  (faction_set_slot, "fac_kingdom_1", slot_faction_adjective, "str_kingdom_1_adjective"),
	  (faction_set_slot, "fac_kingdom_2", slot_faction_adjective, "str_kingdom_2_adjective"),
	  (faction_set_slot, "fac_kingdom_3", slot_faction_adjective, "str_kingdom_3_adjective"),
	  (faction_set_slot, "fac_kingdom_4", slot_faction_adjective, "str_kingdom_4_adjective"),
	  (faction_set_slot, "fac_kingdom_5", slot_faction_adjective, "str_kingdom_5_adjective"),
	  (faction_set_slot, "fac_kingdom_6", slot_faction_adjective, "str_kingdom_6_adjective"),
	  (faction_set_slot, "fac_kingdom_7", slot_faction_adjective, "str_kingdom_7_adjective"),
	  (faction_set_slot, "fac_kingdom_8", slot_faction_adjective, "str_kingdom_8_adjective"),
	  (faction_set_slot, "fac_kingdom_9", slot_faction_adjective, "str_kingdom_9_adjective"),
	  (faction_set_slot, "fac_kingdom_10", slot_faction_adjective, "str_kingdom_10_adjective"),
	  (faction_set_slot, "fac_kingdom_11", slot_faction_adjective, "str_kingdom_11_adjective"),
	  (faction_set_slot, "fac_kingdom_12", slot_faction_adjective, "str_kingdom_12_adjective"),
	  (faction_set_slot, "fac_kingdom_13", slot_faction_adjective, "str_kingdom_13_adjective"),
	  (faction_set_slot, "fac_kingdom_14", slot_faction_adjective, "str_kingdom_14_adjective"),
	  (faction_set_slot, "fac_kingdom_15", slot_faction_adjective, "str_kingdom_15_adjective"),
	  (faction_set_slot, "fac_kingdom_16", slot_faction_adjective, "str_kingdom_16_adjective"),
	  (faction_set_slot, "fac_kingdom_17", slot_faction_adjective, "str_kingdom_17_adjective"),
	  (faction_set_slot, "fac_kingdom_18", slot_faction_adjective, "str_kingdom_18_adjective"),
	  
	  (faction_set_slot, "fac_dark_knights", slot_faction_adjective, "str_kingdom_dk_adjective"), ## Tocan Invasion ##

## Tocan Invasion+ ##
      (faction_set_slot, "fac_dark_knights", slot_faction_state, sfs_inactive),	  
      (party_set_faction,"p_main_party","fac_player_faction"),
## Tocan Invasion- ##
	  
##      (assign, "$players_kingdom", "fac_kingdom_1"),
##      (call_script, "script_give_center_to_lord", "p_town_7", "trp_player", 0),
##      (call_script, "script_give_center_to_lord", "p_town_16", "trp_player", 0),
####      (call_script, "script_give_center_to_lord", "p_castle_10", "trp_player", 0),
##      (assign, "$g_castle_requested_by_player", "p_castle_10"),
      (call_script, "script_get_player_party_morale_values"),
      (party_set_morale, "p_main_party", reg0),

      (troop_set_note_available, "trp_player", 1),

      (try_for_range, ":troop_no", kings_begin, kings_end),
        (troop_set_note_available, ":troop_no", 1),
      (try_end),
	  
      (try_for_range, ":troop_no", lords_begin, lords_end),
        (troop_set_note_available, ":troop_no", 1),
      (try_end),

	  (try_for_range, ":troop_no", kingdom_ladies_begin, kingdom_ladies_end),
        (troop_set_note_available, ":troop_no", 1),
      (try_end),
	  (troop_set_note_available, "trp_knight_1_1_wife", 0),

      (try_for_range, ":troop_no", pretenders_begin, pretenders_end),
        (troop_set_note_available, ":troop_no", 1),
      (try_end),
	  
	  #Lady and companion notes become available as you meet/recruit them
	  
      (try_for_range, ":faction_no", npc_kingdoms_begin, npc_kingdoms_end),
        (faction_set_note_available, ":faction_no", 1),
      (try_end),
      (faction_set_note_available, "fac_neutral", 0),
	  
      (try_for_range, ":party_no", centers_begin, centers_end),
        (party_set_note_available, ":party_no", 1),
      (try_end),
      
	  ## Tocan Invasion
	(try_begin),	  
	  (troop_set_note_available, "trp_dark_knight_lord", 0),
	  (troop_set_note_available, "trp_dark_knight_lord1", 0),
	  (troop_set_note_available, "trp_dark_knight_lord2", 0),
	  (troop_set_note_available, "trp_dark_knight_lord3", 0),
	  (troop_set_note_available, "trp_dark_knight_lord4", 0),
	  (troop_set_note_available, "trp_dark_knight_lord5", 0),
	  (troop_set_note_available, "trp_dark_knight_lord6", 0),
	  (troop_set_note_available, "trp_dark_knight_lord7", 0),
	  (troop_set_note_available, "trp_dark_knight_lord8", 0),
	  (troop_set_note_available, "trp_dark_knight_lord9", 0),
	  (troop_set_note_available, "trp_dark_knight_lord10", 0),
	  (troop_set_note_available, "trp_dark_knight_lord11", 0),
	  (troop_set_note_available, "trp_dark_knight_lord12", 0),
	  (troop_set_note_available, "trp_dark_knight_lord13", 0),
	  (troop_set_note_available, "trp_dark_knight_lord14", 0),
	  (troop_set_note_available, "trp_dark_knight_lord15", 0),
	  (troop_set_note_available, "trp_dark_knight_lord16", 0),
	  (troop_set_note_available, "trp_dark_knight_lord17", 0),
	  (troop_set_note_available, "trp_dark_knight_lord18", 0),
	  (troop_set_note_available, "trp_dark_knight_lord19", 0),
	  (troop_set_note_available, "trp_dark_knight_lord20", 0),
	  (faction_set_note_available, "fac_dark_knights", 0), 
	(try_end),	  
	
	##diplomacy start+
    #Perform initialization for autoloot / autosell.
	(call_script, "script_dplmc_initialize_autoloot", 1),#argument "1" forces this to make changes
	#Set the version number (this slot on this troop should never be used for anything else)
	#The lowest 7 bits of the slot are a verification code.  They should always be equal to 68,
	#  unless there is no version number set.  The rest of the slot is the version number.
    (troop_set_slot, "trp_dplmc_chamberlain", dplmc_slot_troop_affiliated, (DPLMC_CURRENT_VERSION_CODE * 128) + DPLMC_VERSION_LOW_7_BITS),#Version number 1
	##diplomacy end+
    ]),
  #script_game_get_use_string
  # This script is called from the game engine for getting using information text
  # INPUT: used_scene_prop_id  
  # OUTPUT: s0
  ("game_get_use_string",
   [
     (store_script_param, ":instance_id", 1),

     (prop_instance_get_scene_prop_kind, ":scene_prop_id", ":instance_id"),
     
     (try_begin),
       (this_or_next|eq, ":scene_prop_id", "spr_winch_b"),
       (eq, ":scene_prop_id", "spr_winch"),
       (assign, ":effected_object", "spr_portcullis"),
     (else_try),
       (this_or_next|eq, ":scene_prop_id", "spr_door_destructible"),
       (this_or_next|eq, ":scene_prop_id", "spr_castle_f_door_b"),
       (this_or_next|eq, ":scene_prop_id", "spr_castle_e_sally_door_a"),
       (this_or_next|eq, ":scene_prop_id", "spr_castle_f_sally_door_a"),
       (this_or_next|eq, ":scene_prop_id", "spr_earth_sally_gate_left"),
       (this_or_next|eq, ":scene_prop_id", "spr_earth_sally_gate_right"),
       (this_or_next|eq, ":scene_prop_id", "spr_viking_keep_destroy_sally_door_left"),
       (this_or_next|eq, ":scene_prop_id", "spr_viking_keep_destroy_sally_door_right"),
       (this_or_next|eq, ":scene_prop_id", "spr_castle_f_door_a"),
       (this_or_next|eq, ":scene_prop_id", "spr_siege_ladder_move_6m"),
       (this_or_next|eq, ":scene_prop_id", "spr_siege_ladder_move_8m"),
       (this_or_next|eq, ":scene_prop_id", "spr_siege_ladder_move_10m"),
       (this_or_next|eq, ":scene_prop_id", "spr_siege_ladder_move_12m"),
       (eq, ":scene_prop_id", "spr_siege_ladder_move_14m"),
       (assign, ":effected_object", ":scene_prop_id"),
     (try_end),   

     (scene_prop_get_slot, ":item_situation", ":instance_id", scene_prop_open_or_close_slot),
   
     (try_begin), #opening/closing portcullis
       (eq, ":effected_object", "spr_portcullis"),

       (try_begin),
         (eq, ":item_situation", 0),
         (str_store_string, s0, "str_open_gate"),
       (else_try), 
         (str_store_string, s0, "str_close_gate"),
       (try_end),
     (else_try), #opening/closing door
       (this_or_next|eq, ":effected_object", "spr_door_destructible"),
       (this_or_next|eq, ":effected_object", "spr_castle_f_door_b"),
       (this_or_next|eq, ":effected_object", "spr_castle_e_sally_door_a"),
       (this_or_next|eq, ":effected_object", "spr_castle_f_sally_door_a"),
       (this_or_next|eq, ":effected_object", "spr_earth_sally_gate_left"),
       (this_or_next|eq, ":effected_object", "spr_earth_sally_gate_right"),
       (this_or_next|eq, ":effected_object", "spr_viking_keep_destroy_sally_door_left"),
       (this_or_next|eq, ":effected_object", "spr_viking_keep_destroy_sally_door_right"),
       (eq, ":effected_object", "spr_castle_f_door_a"),

       (try_begin),
         (eq, ":item_situation", 0),
         (str_store_string, s0, "str_open_door"),
       (else_try),
         (str_store_string, s0, "str_close_door"),
       (try_end),
     (else_try), #raising/dropping ladder
       (try_begin),
         (eq, ":item_situation", 0),
         (str_store_string, s0, "str_raise_ladder"),
       (else_try),
         (str_store_string, s0, "str_drop_ladder"),
       (try_end),
     (try_end),
   ]),
  #script_game_quick_start
  # This script is called from the game engine for initializing the global variables for tutorial, multiplayer and custom battle modes.
  # INPUT:
  # none
  # OUTPUT:
  # none
  ("game_quick_start",
    [
      #for quick battle mode
      (assign, "$g_is_quick_battle", 0),
      (assign, "$g_quick_battle_game_type", 0),
      (assign, "$g_quick_battle_troop", quick_battle_troops_begin),
      (assign, "$g_quick_battle_map", quick_battle_scenes_begin),
      (assign, "$g_quick_battle_team_1_faction", "fac_kingdom_1"),
      (assign, "$g_quick_battle_team_2_faction", "fac_kingdom_2"),
      (assign, "$g_quick_battle_army_1_size", 25),
      (assign, "$g_quick_battle_army_2_size", 25),

      (faction_set_slot, "fac_outlaws", slot_faction_quick_battle_tier_1_infantry, "trp_woku_pirate"),
      (faction_set_slot, "fac_outlaws", slot_faction_quick_battle_tier_2_infantry, "trp_kinai_rebel"),
      (faction_set_slot, "fac_outlaws", slot_faction_quick_battle_tier_1_archer, "trp_shinano_rebel"),
      (faction_set_slot, "fac_outlaws", slot_faction_quick_battle_tier_2_archer, "trp_kanto_rebel"),
      (faction_set_slot, "fac_outlaws", slot_faction_quick_battle_tier_1_cavalry, "trp_seto_pirate"),
      (faction_set_slot, "fac_outlaws", slot_faction_quick_battle_tier_2_cavalry, "trp_northern_raider"),
      (faction_set_slot, "fac_kingdom_1", slot_faction_quick_battle_tier_1_infantry, "trp_gekokujo_uesugi_retainer"),
      (faction_set_slot, "fac_kingdom_1", slot_faction_quick_battle_tier_2_infantry, "trp_gekokujo_uesugi_veteran_retainer"),
      (faction_set_slot, "fac_kingdom_1", slot_faction_quick_battle_tier_1_archer, "trp_gekokujo_uesugi_skirmisher"),
      (faction_set_slot, "fac_kingdom_1", slot_faction_quick_battle_tier_2_archer, "trp_gekokujo_uesugi_samurai_archer"),
      (faction_set_slot, "fac_kingdom_1", slot_faction_quick_battle_tier_1_cavalry, "trp_gekokujo_uesugi_mounted_retainer"),
      (faction_set_slot, "fac_kingdom_1", slot_faction_quick_battle_tier_2_cavalry, "trp_gekokujo_uesugi_mounted_officer"),
      (faction_set_slot, "fac_kingdom_2", slot_faction_quick_battle_tier_1_infantry, "trp_gekokujo_date_retainer"),
      (faction_set_slot, "fac_kingdom_2", slot_faction_quick_battle_tier_2_infantry, "trp_gekokujo_date_veteran_retainer"),
      (faction_set_slot, "fac_kingdom_2", slot_faction_quick_battle_tier_1_archer, "trp_gekokujo_date_skirmisher"),
      (faction_set_slot, "fac_kingdom_2", slot_faction_quick_battle_tier_2_archer, "trp_gekokujo_date_samurai_archer"),
      (faction_set_slot, "fac_kingdom_2", slot_faction_quick_battle_tier_1_cavalry, "trp_gekokujo_date_mounted_retainer"),
      (faction_set_slot, "fac_kingdom_2", slot_faction_quick_battle_tier_2_cavalry, "trp_gekokujo_date_mounted_officer"),
      (faction_set_slot, "fac_kingdom_3", slot_faction_quick_battle_tier_1_infantry, "trp_gekokujo_oda_retainer"),
      (faction_set_slot, "fac_kingdom_3", slot_faction_quick_battle_tier_2_infantry, "trp_gekokujo_oda_veteran_retainer"),
      (faction_set_slot, "fac_kingdom_3", slot_faction_quick_battle_tier_1_archer, "trp_gekokujo_oda_skirmisher"),
      (faction_set_slot, "fac_kingdom_3", slot_faction_quick_battle_tier_2_archer, "trp_gekokujo_oda_samurai_gunner"),
      (faction_set_slot, "fac_kingdom_3", slot_faction_quick_battle_tier_1_cavalry, "trp_gekokujo_oda_mounted_retainer"),
      (faction_set_slot, "fac_kingdom_3", slot_faction_quick_battle_tier_2_cavalry, "trp_gekokujo_oda_mounted_officer"),
      (faction_set_slot, "fac_kingdom_4", slot_faction_quick_battle_tier_1_infantry, "trp_gekokujo_mori_retainer"),
      (faction_set_slot, "fac_kingdom_4", slot_faction_quick_battle_tier_2_infantry, "trp_gekokujo_mori_veteran_retainer"),
      (faction_set_slot, "fac_kingdom_4", slot_faction_quick_battle_tier_1_archer, "trp_gekokujo_mori_skirmisher"),
      (faction_set_slot, "fac_kingdom_4", slot_faction_quick_battle_tier_2_archer, "trp_gekokujo_mori_samurai_archer"),
      (faction_set_slot, "fac_kingdom_4", slot_faction_quick_battle_tier_1_cavalry, "trp_gekokujo_mori_mounted_retainer"),
      (faction_set_slot, "fac_kingdom_4", slot_faction_quick_battle_tier_2_cavalry, "trp_gekokujo_mori_mounted_officer"),
      (faction_set_slot, "fac_kingdom_5", slot_faction_quick_battle_tier_1_infantry, "trp_gekokujo_takeda_retainer"),
      (faction_set_slot, "fac_kingdom_5", slot_faction_quick_battle_tier_2_infantry, "trp_gekokujo_takeda_veteran_retainer"),
      (faction_set_slot, "fac_kingdom_5", slot_faction_quick_battle_tier_1_archer, "trp_gekokujo_takeda_skirmisher"),
      (faction_set_slot, "fac_kingdom_5", slot_faction_quick_battle_tier_2_archer, "trp_gekokujo_takeda_samurai_archer"),
      (faction_set_slot, "fac_kingdom_5", slot_faction_quick_battle_tier_1_cavalry, "trp_gekokujo_takeda_mounted_retainer"),
      (faction_set_slot, "fac_kingdom_5", slot_faction_quick_battle_tier_2_cavalry, "trp_gekokujo_takeda_mounted_officer"),
      (faction_set_slot, "fac_kingdom_6", slot_faction_quick_battle_tier_1_infantry, "trp_gekokujo_tokugawa_retainer"),
      (faction_set_slot, "fac_kingdom_6", slot_faction_quick_battle_tier_2_infantry, "trp_gekokujo_tokugawa_veteran_retainer"),
      (faction_set_slot, "fac_kingdom_6", slot_faction_quick_battle_tier_1_archer, "trp_gekokujo_tokugawa_skirmisher"),
      (faction_set_slot, "fac_kingdom_6", slot_faction_quick_battle_tier_2_archer, "trp_gekokujo_tokugawa_samurai_gunner"),
      (faction_set_slot, "fac_kingdom_6", slot_faction_quick_battle_tier_1_cavalry, "trp_gekokujo_tokugawa_mounted_retainer"),
      (faction_set_slot, "fac_kingdom_6", slot_faction_quick_battle_tier_2_cavalry, "trp_gekokujo_tokugawa_mounted_officer"),

      #for multiplayer mode
      (assign, "$g_multiplayer_selected_map", multiplayer_scenes_begin),
      (assign, "$g_multiplayer_respawn_period", 5),
      (assign, "$g_multiplayer_round_max_seconds", 300),
      (assign, "$g_multiplayer_game_max_minutes", 30),
      (assign, "$g_multiplayer_game_max_points", 300),

      (server_get_renaming_server_allowed, "$g_multiplayer_renaming_server_allowed"),
      (server_get_changing_game_type_allowed, "$g_multiplayer_changing_game_type_allowed"),
      (assign, "$g_multiplayer_point_gained_from_flags", 100),
      (assign, "$g_multiplayer_point_gained_from_capturing_flag", 5),
      (assign, "$g_multiplayer_game_type", 0),
      (assign, "$g_multiplayer_team_1_faction", "fac_kingdom_1"),
      (assign, "$g_multiplayer_team_2_faction", "fac_kingdom_2"),
      (assign, "$g_multiplayer_next_team_1_faction", "$g_multiplayer_team_1_faction"),
      (assign, "$g_multiplayer_next_team_2_faction", "$g_multiplayer_team_2_faction"),
      (assign, "$g_multiplayer_num_bots_team_1", 0),
      (assign, "$g_multiplayer_num_bots_team_2", 0),
      (assign, "$g_multiplayer_number_of_respawn_count", 0),
      (assign, "$g_multiplayer_num_bots_voteable", 50),
      (assign, "$g_multiplayer_max_num_bots", 101),
      (assign, "$g_multiplayer_factions_voteable", 1),
      (assign, "$g_multiplayer_maps_voteable", 1),
      (assign, "$g_multiplayer_kick_voteable", 1),
      (assign, "$g_multiplayer_ban_voteable", 1),
      (assign, "$g_multiplayer_valid_vote_ratio", 51), #more than 50 percent
      (assign, "$g_multiplayer_auto_team_balance_limit", 3), #auto balance when difference is more than 2
      (assign, "$g_multiplayer_player_respawn_as_bot", 1),
      (assign, "$g_multiplayer_stats_chart_opened_manually", 0),
      (assign, "$g_multiplayer_mission_end_screen", 0),
      (assign, "$g_multiplayer_ready_for_spawning_agent", 1),
      (assign, "$g_multiplayer_welcome_message_shown", 0),
      (assign, "$g_multiplayer_allow_player_banners", 1),
      (assign, "$g_multiplayer_force_default_armor", 1),
      (assign, "$g_multiplayer_disallow_ranged_weapons", 0),
      
      (assign, "$g_multiplayer_initial_gold_multiplier", 100),
      (assign, "$g_multiplayer_battle_earnings_multiplier", 100),
      (assign, "$g_multiplayer_round_earnings_multiplier", 100),
  
      #faction banners
      #(faction_set_slot, "fac_kingdom_1", slot_faction_banner, "mesh_banner_kingdom_f"),
      #(faction_set_slot, "fac_kingdom_2", slot_faction_banner, "mesh_banner_kingdom_b"),
      #(faction_set_slot, "fac_kingdom_3", slot_faction_banner, "mesh_banner_kingdom_c"),
      #(faction_set_slot, "fac_kingdom_4", slot_faction_banner, "mesh_banner_kingdom_a"),
      #(faction_set_slot, "fac_kingdom_5", slot_faction_banner, "mesh_banner_kingdom_d"),
      #(faction_set_slot, "fac_kingdom_6", slot_faction_banner, "mesh_banner_kingdom_e"),

      (faction_set_slot, "fac_kingdom_1", slot_faction_banner, "mesh_banner_c01"),
      (faction_set_slot, "fac_kingdom_2", slot_faction_banner, "mesh_banner_b19"),
      (faction_set_slot, "fac_kingdom_3", slot_faction_banner, "mesh_banner_b20"),
      (faction_set_slot, "fac_kingdom_4", slot_faction_banner, "mesh_banner_b04"),
      (faction_set_slot, "fac_kingdom_5", slot_faction_banner, "mesh_banner_g11"),
      (faction_set_slot, "fac_kingdom_6", slot_faction_banner, "mesh_banner_a13"),
      (faction_set_slot, "fac_kingdom_7", slot_faction_banner, "mesh_banner_a11"),
      (faction_set_slot, "fac_kingdom_8", slot_faction_banner, "mesh_banner_c02"),
      (faction_set_slot, "fac_kingdom_9", slot_faction_banner, "mesh_banner_c03"),
      (faction_set_slot, "fac_kingdom_10", slot_faction_banner, "mesh_banner_b14"),
      (faction_set_slot, "fac_kingdom_11", slot_faction_banner, "mesh_banner_c04"),
      (faction_set_slot, "fac_kingdom_12", slot_faction_banner, "mesh_banner_b03"),
      (faction_set_slot, "fac_kingdom_13", slot_faction_banner, "mesh_banner_a20"),
      (faction_set_slot, "fac_kingdom_14", slot_faction_banner, "mesh_banner_b12"),
      (faction_set_slot, "fac_kingdom_15", slot_faction_banner, "mesh_banner_c05"),
      (faction_set_slot, "fac_kingdom_16", slot_faction_banner, "mesh_banner_c06"),
      (faction_set_slot, "fac_kingdom_17", slot_faction_banner, "mesh_banner_c07"),
      (faction_set_slot, "fac_kingdom_18", slot_faction_banner, "mesh_banner_c08"),
      (faction_set_slot, "fac_kingdom_19", slot_faction_banner, "mesh_banner_c09"),
      (faction_set_slot, "fac_kingdom_20", slot_faction_banner, "mesh_banner_f02"),
	  
      (try_for_range, ":cur_item", all_items_begin, all_items_end),
        (try_for_range, ":cur_faction", npc_kingdoms_begin, npc_kingdoms_end),
          (store_sub, ":faction_index", ":cur_faction", npc_kingdoms_begin),
          (val_add, ":faction_index", slot_item_multiplayer_faction_price_multipliers_begin),
          (item_set_slot, ":cur_item", ":faction_index", 100), #100 is the default price multiplier
        (try_end),
      (try_end),
      (store_sub, ":swadian_price_slot", "fac_kingdom_1", npc_kingdoms_begin),
      (val_add, ":swadian_price_slot", slot_item_multiplayer_faction_price_multipliers_begin),
      (store_sub, ":vaegir_price_slot", "fac_kingdom_2", npc_kingdoms_begin),
      (val_add, ":vaegir_price_slot", slot_item_multiplayer_faction_price_multipliers_begin),
      (store_sub, ":khergit_price_slot", "fac_kingdom_3", npc_kingdoms_begin),
      (val_add, ":khergit_price_slot", slot_item_multiplayer_faction_price_multipliers_begin),
      (store_sub, ":nord_price_slot", "fac_kingdom_4", npc_kingdoms_begin),
      (val_add, ":nord_price_slot", slot_item_multiplayer_faction_price_multipliers_begin),
      (store_sub, ":rhodok_price_slot", "fac_kingdom_5", npc_kingdoms_begin),
      (val_add, ":rhodok_price_slot", slot_item_multiplayer_faction_price_multipliers_begin),
      (store_sub, ":sarranid_price_slot", "fac_kingdom_6", npc_kingdoms_begin),
      (val_add, ":sarranid_price_slot", slot_item_multiplayer_faction_price_multipliers_begin),

      #arrows
      (item_set_slot, "itm_gekokujo_arrows_1", slot_item_multiplayer_item_class, multi_item_class_type_arrow),      
      (item_set_slot, "itm_gekokujo_arrows_2", slot_item_multiplayer_item_class, multi_item_class_type_arrow),       
      (item_set_slot, "itm_gekokujo_arrows_3", slot_item_multiplayer_item_class, multi_item_class_type_arrow),     
      (item_set_slot, "itm_gekokujo_arrows_4", slot_item_multiplayer_item_class, multi_item_class_type_arrow),   
      (item_set_slot, "itm_gekokujo_bullets_1", slot_item_multiplayer_item_class, multi_item_class_type_bolt),
      (item_set_slot, "itm_gekokujo_bullets_2", slot_item_multiplayer_item_class, multi_item_class_type_bolt),
      #bows
      (item_set_slot, "itm_gekokujo_yumi_1", slot_item_multiplayer_item_class, multi_item_class_type_bow),
      (item_set_slot, "itm_gekokujo_yumi_2", slot_item_multiplayer_item_class, multi_item_class_type_bow),    
      (item_set_slot, "itm_gekokujo_yumi_3", slot_item_multiplayer_item_class, multi_item_class_type_bow),    
      (item_set_slot, "itm_gekokujo_yumi_4", slot_item_multiplayer_item_class, multi_item_class_type_bow),    
      (item_set_slot, "itm_gekokujo_yumi_5", slot_item_multiplayer_item_class, multi_item_class_type_bow),    
      (item_set_slot, "itm_gekokujo_yumi_6", slot_item_multiplayer_item_class, multi_item_class_type_bow),    
      (item_set_slot, "itm_gekokujo_yumi_7", slot_item_multiplayer_item_class, multi_item_class_type_bow),    
      (item_set_slot, "itm_gekokujo_yumi_8", slot_item_multiplayer_item_class, multi_item_class_type_bow),    
      (item_set_slot, "itm_gekokujo_yumi_9", slot_item_multiplayer_item_class, multi_item_class_type_bow),    
      (item_set_slot, "itm_gekokujo_arquebus_1", slot_item_multiplayer_item_class, multi_item_class_type_bow), 
      (item_set_slot, "itm_gekokujo_arquebus_2", slot_item_multiplayer_item_class, multi_item_class_type_bow), 
      (item_set_slot, "itm_gekokujo_arquebus_3", slot_item_multiplayer_item_class, multi_item_class_type_bow),    
      (item_set_slot, "itm_gekokujo_arquebus_4", slot_item_multiplayer_item_class, multi_item_class_type_bow), 
      (item_set_slot, "itm_gekokujo_arquebus_5", slot_item_multiplayer_item_class, multi_item_class_type_bow),    
      #swords
      (item_set_slot, "itm_gekokujo_katana_1", slot_item_multiplayer_item_class, multi_item_class_type_sword),
      (item_set_slot, "itm_gekokujo_katana_2", slot_item_multiplayer_item_class, multi_item_class_type_sword),
      (item_set_slot, "itm_gekokujo_katana_3", slot_item_multiplayer_item_class, multi_item_class_type_sword),
      (item_set_slot, "itm_gekokujo_katana_4", slot_item_multiplayer_item_class, multi_item_class_type_sword),
      (item_set_slot, "itm_gekokujo_katana_5", slot_item_multiplayer_item_class, multi_item_class_type_sword),
      (item_set_slot, "itm_gekokujo_katana_6", slot_item_multiplayer_item_class, multi_item_class_type_sword),
      (item_set_slot, "itm_gekokujo_katana_7", slot_item_multiplayer_item_class, multi_item_class_type_sword),
      (item_set_slot, "itm_gekokujo_katana_8", slot_item_multiplayer_item_class, multi_item_class_type_sword),
      (item_set_slot, "itm_gekokujo_katana_9", slot_item_multiplayer_item_class, multi_item_class_type_sword),
      (item_set_slot, "itm_gekokujo_katana_10", slot_item_multiplayer_item_class, multi_item_class_type_sword),
      (item_set_slot, "itm_gekokujo_tachi_1", slot_item_multiplayer_item_class, multi_item_class_type_sword),
      (item_set_slot, "itm_gekokujo_tachi_2", slot_item_multiplayer_item_class, multi_item_class_type_sword),
      (item_set_slot, "itm_gekokujo_tachi_3", slot_item_multiplayer_item_class, multi_item_class_type_sword),
      (item_set_slot, "itm_gekokujo_tachi_4", slot_item_multiplayer_item_class, multi_item_class_type_sword),
      (item_set_slot, "itm_gekokujo_tachi_5", slot_item_multiplayer_item_class, multi_item_class_type_sword),
      (item_set_slot, "itm_gekokujo_tachi_6", slot_item_multiplayer_item_class, multi_item_class_type_sword),
      (item_set_slot, "itm_gekokujo_tachi_7", slot_item_multiplayer_item_class, multi_item_class_type_sword),
      (item_set_slot, "itm_gekokujo_tachi_8", slot_item_multiplayer_item_class, multi_item_class_type_sword),
      (item_set_slot, "itm_gekokujo_tachi_9", slot_item_multiplayer_item_class, multi_item_class_type_sword),
      (item_set_slot, "itm_gekokujo_tachi_10", slot_item_multiplayer_item_class, multi_item_class_type_sword),
      (item_set_slot, "itm_gekokujo_nodachi_1", slot_item_multiplayer_item_class, multi_item_class_type_sword),
      (item_set_slot, "itm_gekokujo_nodachi_2", slot_item_multiplayer_item_class, multi_item_class_type_sword),
      (item_set_slot, "itm_gekokujo_nodachi_3", slot_item_multiplayer_item_class, multi_item_class_type_sword),
      (item_set_slot, "itm_gekokujo_nodachi_4", slot_item_multiplayer_item_class, multi_item_class_type_sword),
      (item_set_slot, "itm_gekokujo_nodachi_5", slot_item_multiplayer_item_class, multi_item_class_type_sword),
      (item_set_slot, "itm_gekokujo_nodachi_6", slot_item_multiplayer_item_class, multi_item_class_type_sword),
      (item_set_slot, "itm_gekokujo_nodachi_7", slot_item_multiplayer_item_class, multi_item_class_type_sword),
      (item_set_slot, "itm_gekokujo_nodachi_8", slot_item_multiplayer_item_class, multi_item_class_type_sword),
      (item_set_slot, "itm_gekokujo_nodachi_9", slot_item_multiplayer_item_class, multi_item_class_type_sword),
      (item_set_slot, "itm_gekokujo_nodachi_10", slot_item_multiplayer_item_class, multi_item_class_type_sword),
      (item_set_slot, "itm_gekokujo_chinese_1", slot_item_multiplayer_item_class, multi_item_class_type_sword),
      (item_set_slot, "itm_gekokujo_chinese_2", slot_item_multiplayer_item_class, multi_item_class_type_sword),
      (item_set_slot, "itm_gekokujo_chinese_3", slot_item_multiplayer_item_class, multi_item_class_type_sword),
      (item_set_slot, "itm_gekokujo_chinese_4", slot_item_multiplayer_item_class, multi_item_class_type_sword),
      (item_set_slot, "itm_gekokujo_chinese_5", slot_item_multiplayer_item_class, multi_item_class_type_sword),
      (item_set_slot, "itm_gekokujo_wakizashi_1", slot_item_multiplayer_item_class, multi_item_class_type_sword),
      (item_set_slot, "itm_gekokujo_wakizashi_2", slot_item_multiplayer_item_class, multi_item_class_type_sword),
      (item_set_slot, "itm_gekokujo_wakizashi_3", slot_item_multiplayer_item_class, multi_item_class_type_sword),
      (item_set_slot, "itm_gekokujo_wakizashi_4", slot_item_multiplayer_item_class, multi_item_class_type_sword),
      (item_set_slot, "itm_gekokujo_wakizashi_5", slot_item_multiplayer_item_class, multi_item_class_type_sword),
      (item_set_slot, "itm_gekokujo_wakizashi_6", slot_item_multiplayer_item_class, multi_item_class_type_sword),
      (item_set_slot, "itm_gekokujo_wakizashi_7", slot_item_multiplayer_item_class, multi_item_class_type_sword),
      (item_set_slot, "itm_gekokujo_wakizashi_8", slot_item_multiplayer_item_class, multi_item_class_type_sword),
      (item_set_slot, "itm_gekokujo_wakizashi_9", slot_item_multiplayer_item_class, multi_item_class_type_sword),
      (item_set_slot, "itm_gekokujo_wakizashi_10", slot_item_multiplayer_item_class, multi_item_class_type_sword),
	  
      #axe
      (item_set_slot, "itm_gekokujo_kama_1", slot_item_multiplayer_item_class, multi_item_class_type_axe),
	  
      #blunt
      (item_set_slot, "itm_gekokujo_jo", slot_item_multiplayer_item_class, multi_item_class_type_blunt),
      (item_set_slot, "itm_gekokujo_bo", slot_item_multiplayer_item_class, multi_item_class_type_blunt),
      (item_set_slot, "itm_gekokujo_bo_iron", slot_item_multiplayer_item_class, multi_item_class_type_blunt),
      (item_set_slot, "itm_gekokujo_otsuchi", slot_item_multiplayer_item_class, multi_item_class_type_blunt),
      (item_set_slot, "itm_gekokujo_konsaibo_1", slot_item_multiplayer_item_class, multi_item_class_type_blunt),
      (item_set_slot, "itm_gekokujo_konsaibo_2", slot_item_multiplayer_item_class, multi_item_class_type_blunt),
      (item_set_slot, "itm_gekokujo_tetsubo_1", slot_item_multiplayer_item_class, multi_item_class_type_blunt),
      (item_set_slot, "itm_gekokujo_tetsubo_2", slot_item_multiplayer_item_class, multi_item_class_type_blunt),
      #picks
      (item_set_slot, "itm_gekokujo_kama_2", slot_item_multiplayer_item_class, multi_item_class_type_war_picks),
	  
	  #Cleavers
      (item_set_slot, "itm_gekokujo_mongol_1", slot_item_multiplayer_item_class, multi_item_class_type_cleavers),
      (item_set_slot, "itm_gekokujo_naginata_1", slot_item_multiplayer_item_class, multi_item_class_type_cleavers),
      (item_set_slot, "itm_gekokujo_naginata_2", slot_item_multiplayer_item_class, multi_item_class_type_cleavers),
      (item_set_slot, "itm_gekokujo_naginata_3", slot_item_multiplayer_item_class, multi_item_class_type_cleavers),
      (item_set_slot, "itm_gekokujo_naginata_4", slot_item_multiplayer_item_class, multi_item_class_type_cleavers),
      (item_set_slot, "itm_gekokujo_naginata_5", slot_item_multiplayer_item_class, multi_item_class_type_cleavers),
      (item_set_slot, "itm_gekokujo_naginata_6", slot_item_multiplayer_item_class, multi_item_class_type_cleavers),
      (item_set_slot, "itm_gekokujo_naginata_7", slot_item_multiplayer_item_class, multi_item_class_type_cleavers),
      (item_set_slot, "itm_gekokujo_naginata_8", slot_item_multiplayer_item_class, multi_item_class_type_cleavers),
      (item_set_slot, "itm_gekokujo_naginata_9", slot_item_multiplayer_item_class, multi_item_class_type_cleavers),
      (item_set_slot, "itm_gekokujo_naginata_10", slot_item_multiplayer_item_class, multi_item_class_type_cleavers),
      (item_set_slot, "itm_gekokujo_guandao_1", slot_item_multiplayer_item_class, multi_item_class_type_cleavers),
	  
      #spears
      (item_set_slot, "itm_gekokujo_yari_bamboo_1", slot_item_multiplayer_item_class, multi_item_class_type_spear),
      (item_set_slot, "itm_gekokujo_fukuro_yari_1", slot_item_multiplayer_item_class, multi_item_class_type_spear),
      (item_set_slot, "itm_gekokujo_fukuro_yari_2", slot_item_multiplayer_item_class, multi_item_class_type_spear),
      (item_set_slot, "itm_gekokujo_fukuro_yari_3", slot_item_multiplayer_item_class, multi_item_class_type_spear),
      (item_set_slot, "itm_gekokujo_fukuro_yari_4", slot_item_multiplayer_item_class, multi_item_class_type_spear),
      (item_set_slot, "itm_gekokujo_yari_1", slot_item_multiplayer_item_class, multi_item_class_type_spear),
      (item_set_slot, "itm_gekokujo_yari_2", slot_item_multiplayer_item_class, multi_item_class_type_spear),
      (item_set_slot, "itm_gekokujo_yari_3", slot_item_multiplayer_item_class, multi_item_class_type_spear),
      (item_set_slot, "itm_gekokujo_yari_4", slot_item_multiplayer_item_class, multi_item_class_type_spear),
      (item_set_slot, "itm_gekokujo_yari_5", slot_item_multiplayer_item_class, multi_item_class_type_spear),
      (item_set_slot, "itm_gekokujo_yari_6", slot_item_multiplayer_item_class, multi_item_class_type_spear),
      (item_set_slot, "itm_gekokujo_omi_yari_1", slot_item_multiplayer_item_class, multi_item_class_type_spear),
      (item_set_slot, "itm_gekokujo_omi_yari_2", slot_item_multiplayer_item_class, multi_item_class_type_spear),
      (item_set_slot, "itm_gekokujo_omi_yari_3", slot_item_multiplayer_item_class, multi_item_class_type_spear),
      (item_set_slot, "itm_gekokujo_jumonji_yari_1", slot_item_multiplayer_item_class, multi_item_class_type_spear),
      (item_set_slot, "itm_gekokujo_jumonji_yari_2", slot_item_multiplayer_item_class, multi_item_class_type_spear),
      (item_set_slot, "itm_gekokujo_jumonji_yari_3", slot_item_multiplayer_item_class, multi_item_class_type_spear),
      (item_set_slot, "itm_gekokujo_jumonji_yari_4", slot_item_multiplayer_item_class, multi_item_class_type_spear),
      (item_set_slot, "itm_gekokujo_jumonji_yari_5", slot_item_multiplayer_item_class, multi_item_class_type_spear),
      (item_set_slot, "itm_gekokujo_katakama_yari_1", slot_item_multiplayer_item_class, multi_item_class_type_spear),
      (item_set_slot, "itm_gekokujo_katakama_yari_2", slot_item_multiplayer_item_class, multi_item_class_type_spear),
      (item_set_slot, "itm_gekokujo_katakama_yari_3", slot_item_multiplayer_item_class, multi_item_class_type_spear),
      #throwing
      (item_set_slot, "itm_gekokujo_kunai", slot_item_multiplayer_item_class, multi_item_class_type_throwing),
       #armors
      (item_set_slot, "itm_gekokujo_hakama_1", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_gekokujo_hakama_2", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_gekokujo_hakama_3", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_gekokujo_hakama_4", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_gekokujo_hakama_5", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_gekokujo_hakama_6", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_gekokujo_haori_1", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_gekokujo_haori_2", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_gekokujo_haori_3", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_gekokujo_haori_4", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_gekokujo_haori_5", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_gekokujo_haori_6", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_gekokujo_tatami_half_1", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_gekokujo_tatami_half_2", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_gekokujo_tatami_half_3", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_gekokujo_okegawa_half_1", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_gekokujo_okegawa_half_2", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_gekokujo_okegawa_half_3", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_gekokujo_okegawa_half_4", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_gekokujo_okegawa_half_5", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_gekokujo_okegawa_half_6", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_gekokujo_mogami_half_1", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_gekokujo_mogami_half_2", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_gekokujo_mogami_half_3", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_gekokujo_okegawa_half_uesugi", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_gekokujo_okegawa_half_oda", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_gekokujo_okegawa_half_mori", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_gekokujo_okegawa_half_takeda", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_gekokujo_okegawa_half_tokugawa", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_gekokujo_tatami_short_1", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_gekokujo_tatami_short_2", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_gekokujo_tatami_short_3", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_gekokujo_tatami_short_4", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_gekokujo_tatami_short_5", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_gekokujo_tatami_short_6", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_gekokujo_okegawa_short_1", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_gekokujo_okegawa_short_2", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_gekokujo_okegawa_short_3", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_gekokujo_okegawa_short_4", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_gekokujo_okegawa_short_5", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_gekokujo_okegawa_short_6", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_gekokujo_okegawa_short_7", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_gekokujo_okegawa_short_8", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_gekokujo_okegawa_short_9", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_gekokujo_okegawa_short_10", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_gekokujo_okegawa_short_11", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_gekokujo_okegawa_short_12", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_gekokujo_mogami_short_1", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_gekokujo_mogami_short_2", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_gekokujo_mogami_short_3", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_gekokujo_mogami_short_4", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_gekokujo_mogami_short_5", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_gekokujo_mogami_short_6", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_gekokujo_okegawa_short_uesugi", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_gekokujo_okegawa_short_oda", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_gekokujo_okegawa_short_mori", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_gekokujo_okegawa_short_takeda", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_gekokujo_okegawa_short_tokugawa", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_gekokujo_yukinoshita_short_1", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_gekokujo_yukinoshita_short_2", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_gekokujo_yukinoshita_short_3", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_gekokujo_yukinoshita_short_date", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_gekokujo_okegawa_long_1", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_gekokujo_okegawa_long_2", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_gekokujo_okegawa_long_3", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_gekokujo_okegawa_long_4", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_gekokujo_okegawa_long_5", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_gekokujo_okegawa_long_6", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_gekokujo_mogami_long_1", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_gekokujo_mogami_long_2", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_gekokujo_mogami_long_3", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_gekokujo_nuinobe_long_1", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_gekokujo_nuinobe_long_2", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_gekokujo_nuinobe_long_3", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_gekokujo_kebiki_1", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_gekokujo_kebiki_2", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_gekokujo_kebiki_3", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_gekokujo_kebiki_4", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_gekokujo_kebiki_5", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_gekokujo_kebiki_6", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_gekokujo_kebiki_7", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_gekokujo_kebiki_8", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_gekokujo_kebiki_9", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_gekokujo_kebiki_10", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_gekokujo_kebiki_11", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_gekokujo_kebiki_12", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_gekokujo_kebiki_13", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_gekokujo_kebiki_14", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_gekokujo_kebiki_15", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_gekokujo_kebiki_16", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_gekokujo_kebiki_17", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_gekokujo_kebiki_18", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_gekokujo_kebiki_19", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_gekokujo_kebiki_20", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_gekokujo_kebiki_21", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),

	  
	  

  
      #boots
      (item_set_slot, "itm_gekokujo_sandal_1", slot_item_multiplayer_item_class, multi_item_class_type_light_foot),
      (item_set_slot, "itm_gekokujo_sandal_2", slot_item_multiplayer_item_class, multi_item_class_type_light_foot),
      (item_set_slot, "itm_gekokujo_sandal_3", slot_item_multiplayer_item_class, multi_item_class_type_light_foot),
      (item_set_slot, "itm_gekokujo_light_suneate_1", slot_item_multiplayer_item_class, multi_item_class_type_light_foot),
      (item_set_slot, "itm_gekokujo_light_suneate_2", slot_item_multiplayer_item_class, multi_item_class_type_light_foot),
      (item_set_slot, "itm_gekokujo_light_suneate_3", slot_item_multiplayer_item_class, multi_item_class_type_light_foot),
      (item_set_slot, "itm_gekokujo_shino_suneate_1", slot_item_multiplayer_item_class, multi_item_class_type_light_foot),
      (item_set_slot, "itm_gekokujo_shino_suneate_2", slot_item_multiplayer_item_class, multi_item_class_type_light_foot),
      (item_set_slot, "itm_gekokujo_shino_suneate_3", slot_item_multiplayer_item_class, multi_item_class_type_light_foot),
      (item_set_slot, "itm_gekokujo_tsubo_suneate_1", slot_item_multiplayer_item_class, multi_item_class_type_light_foot),
      (item_set_slot, "itm_gekokujo_tsubo_suneate_2", slot_item_multiplayer_item_class, multi_item_class_type_light_foot),
      (item_set_slot, "itm_gekokujo_tsubo_suneate_3", slot_item_multiplayer_item_class, multi_item_class_type_light_foot),
      (item_set_slot, "itm_gekokujo_jinbaori_1", slot_item_multiplayer_item_class, multi_item_class_type_light_foot),
      (item_set_slot, "itm_gekokujo_jinbaori_2", slot_item_multiplayer_item_class, multi_item_class_type_light_foot),
      (item_set_slot, "itm_gekokujo_jinbaori_3", slot_item_multiplayer_item_class, multi_item_class_type_light_foot),
      (item_set_slot, "itm_gekokujo_jinbaori_4", slot_item_multiplayer_item_class, multi_item_class_type_light_foot),
      (item_set_slot, "itm_gekokujo_jinbaori_5", slot_item_multiplayer_item_class, multi_item_class_type_light_foot),
      (item_set_slot, "itm_gekokujo_jinbaori_6", slot_item_multiplayer_item_class, multi_item_class_type_light_foot),
      (item_set_slot, "itm_gekokujo_jinbaori_7", slot_item_multiplayer_item_class, multi_item_class_type_light_foot),
      (item_set_slot, "itm_gekokujo_jinbaori_8", slot_item_multiplayer_item_class, multi_item_class_type_light_foot),
      (item_set_slot, "itm_gekokujo_jinbaori_9", slot_item_multiplayer_item_class, multi_item_class_type_light_foot),

	  
      #helmets
      (item_set_slot, "itm_gekokujo_sugegasa_1", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_gekokujo_monk_headwrap", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_gekokujo_jingasa_1", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_gekokujo_jingasa_2", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_gekokujo_jingasa_3", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_gekokujo_jingasa_4", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_gekokujo_jingasa_5", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_gekokujo_jingasa_6", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_gekokujo_jingasa_7", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_gekokujo_jingasa_8", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_gekokujo_jingasa_9", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_gekokujo_shinomi_o_1", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_gekokujo_shinomi_o_2", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_gekokujo_shinomi_o_3", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_gekokujo_shinomi_o_h_1", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_gekokujo_shinomi_o_h_2", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_gekokujo_shinomi_o_h_3", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_gekokujo_zunari_o_1", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_gekokujo_zunari_o_2", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_gekokujo_zunari_o_3", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_gekokujo_zunari_o_h_1", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_gekokujo_zunari_o_h_2", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_gekokujo_zunari_o_h_3", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_gekokujo_eboshi_h_1", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_gekokujo_eboshi_h_2", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_gekokujo_eboshi_h_3", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_gekokujo_shinomi_h_1", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_gekokujo_shinomi_h_2", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_gekokujo_shinomi_h_3", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_gekokujo_zunari_h_1", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_gekokujo_zunari_h_2", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_gekokujo_zunari_h_3", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_gekokujo_eboshi_m_1", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_gekokujo_eboshi_m_2", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_gekokujo_eboshi_m_3", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_gekokujo_shinomi_m_1", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_gekokujo_shinomi_m_2", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_gekokujo_shinomi_m_3", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_gekokujo_zunari_m_1", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_gekokujo_zunari_m_2", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_gekokujo_zunari_m_3", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_gekokujo_hari_o_1", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_gekokujo_hari_o_2", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_gekokujo_hari_o_3", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_gekokujo_suji_o_1", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_gekokujo_suji_o_2", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_gekokujo_suji_o_3", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_gekokujo_kabuto1_h_1", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_gekokujo_kabuto1_h_2", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_gekokujo_kabuto1_h_3", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_gekokujo_kabuto2_h_1", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_gekokujo_kabuto2_h_2", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_gekokujo_kabuto2_h_3", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_gekokujo_kabuto3_h_1", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_gekokujo_kabuto3_h_2", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_gekokujo_kabuto3_h_3", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_gekokujo_kabuto_nanban_h_1", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_gekokujo_kabuto_nanban_h_2", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_gekokujo_kabuto_nanban_h_3", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_gekokujo_kabuto_nanban_h_4", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_gekokujo_kabuto_nanban_h_5", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_gekokujo_kabuto_nanban_h_6", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_gekokujo_kabuto1_m_1", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_gekokujo_kabuto1_m_2", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_gekokujo_kabuto1_m_3", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_gekokujo_kabuto2_m_1", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_gekokujo_kabuto2_m_2", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_gekokujo_kabuto2_m_3", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_gekokujo_kabuto3_m_1", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_gekokujo_kabuto3_m_2", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_gekokujo_kabuto3_m_3", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_gekokujo_kabuto_nanban_m_1", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_gekokujo_kabuto_nanban_m_2", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_gekokujo_kabuto_nanban_m_3", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_gekokujo_kabuto_nanban_m_4", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_gekokujo_kabuto_nanban_m_5", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_gekokujo_kabuto_nanban_m_6", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_gekokujo_kabuto_unique_1", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_gekokujo_kabuto_unique_2", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_gekokujo_kabuto_unique_3", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_gekokujo_kabuto_unique_4", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_gekokujo_kabuto_unique_5", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_gekokujo_kabuto_unique_6", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_gekokujo_kabuto_unique_7", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_gekokujo_kabuto_unique_8", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_gekokujo_kabuto_unique_9", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_gekokujo_kabuto_unique_10", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_gekokujo_kabuto_unique_11", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_gekokujo_kabuto_unique_12", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_gekokujo_kabuto_unique_13", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_gekokujo_kabuto_unique_14", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_gekokujo_kabuto_unique_15", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_gekokujo_kabuto_unique_16", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_gekokujo_kabuto_unique_17", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_gekokujo_kabuto_unique_18", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_gekokujo_kabuto_unique_19", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_gekokujo_kabuto_unique_20", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_gekokujo_kabuto_unique_21", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_gekokujo_kabuto_unique_22", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_gekokujo_kabuto_unique_23", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_gekokujo_kabuto_unique_24", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_gekokujo_kabuto_unique_25", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_gekokujo_kabuto_unique_26", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_gekokujo_kabuto_unique_27", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_gekokujo_kabuto_unique_28", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_gekokujo_kabuto_unique_29", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_gekokujo_kabuto_unique_30", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),

	  #gloves
      (item_set_slot, "itm_gekokujo_tekko_1", slot_item_multiplayer_item_class, multi_item_class_type_glove),           
      (item_set_slot, "itm_gekokujo_tekko_2", slot_item_multiplayer_item_class, multi_item_class_type_glove),           
      (item_set_slot, "itm_gekokujo_tekko_3_1", slot_item_multiplayer_item_class, multi_item_class_type_glove),           
      (item_set_slot, "itm_gekokujo_tekko_3_2", slot_item_multiplayer_item_class, multi_item_class_type_glove),         
      (item_set_slot, "itm_gekokujo_tekko_3_3", slot_item_multiplayer_item_class, multi_item_class_type_glove),     
	  (item_set_slot, "itm_gekokujo_tekko_4_1", slot_item_multiplayer_item_class, multi_item_class_type_glove),	
	  (item_set_slot, "itm_gekokujo_tekko_4_2", slot_item_multiplayer_item_class, multi_item_class_type_glove),	
	  (item_set_slot, "itm_gekokujo_tekko_4_3", slot_item_multiplayer_item_class, multi_item_class_type_glove),	
	  
      #horses
      (item_set_slot, "itm_saddle_horse", slot_item_multiplayer_item_class, multi_item_class_type_horse),
      (item_set_slot, "itm_courser", slot_item_multiplayer_item_class, multi_item_class_type_horse),
      (item_set_slot, "itm_steppe_horse", slot_item_multiplayer_item_class, multi_item_class_type_horse),
      (item_set_slot, "itm_arabian_horse_a", slot_item_multiplayer_item_class, multi_item_class_type_horse),
      (item_set_slot, "itm_arabian_horse_b", slot_item_multiplayer_item_class, multi_item_class_type_horse),
      (item_set_slot, "itm_hunter", slot_item_multiplayer_item_class, multi_item_class_type_horse),
	  

      #1-Swadian Warriors
      #1a-Swadian Crossbowman
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_gekokujo_sandal_1", "trp_swadian_crossbowman_multiplayer"),

      #1b-Swadian Infantry
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_gekokujo_sandal_1", "trp_swadian_infantry_multiplayer"),

      #1c-Swadian Man At Arms
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_gekokujo_sandal_1", "trp_swadian_man_at_arms_multiplayer"),

      #2-Vaegir Warriors
      #2a-Vaegir Archer
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_gekokujo_sandal_1", "trp_vaegir_archer_multiplayer"),

      #2b-Vaegir Spearman
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_gekokujo_sandal_1", "trp_vaegir_spearman_multiplayer"),

      #2c-Vaegir Horseman
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_gekokujo_sandal_1", "trp_vaegir_horseman_multiplayer"),

      #3-Khergit Warriors
      #3a-Khergit Veteran Horse Archer
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_gekokujo_sandal_1", "trp_khergit_veteran_horse_archer_multiplayer"),

      #3a-Khergit Lancer
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_gekokujo_sandal_1", "trp_khergit_lancer_multiplayer"),

      #Nord Warriors 

      #4c-Nord Archer
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_gekokujo_sandal_1", "trp_nord_archer_multiplayer"),

      #4a-Nord Veteran      
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_gekokujo_sandal_1", "trp_nord_veteran_multiplayer"),

      #4b-Nord Scout
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_gekokujo_sandal_1", "trp_nord_scout_multiplayer"),

      #5-Rhodok Warriors         
      #5a-Rhodok Veteran Crossbowman
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_gekokujo_sandal_1", "trp_rhodok_veteran_crossbowman_multiplayer"),

	  #5b-Rhodok Sergeant
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_gekokujo_sandal_1", "trp_rhodok_sergeant_multiplayer"),

	  #5c-Rhodok Horseman
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_gekokujo_sandal_1", "trp_rhodok_horseman_multiplayer"),

      #6-Sarranid Warriors         
      #5a-Sarranid archer
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_gekokujo_sandal_1", "trp_sarranid_archer_multiplayer"),   

	  #Sarranid footman
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_gekokujo_sandal_1", "trp_sarranid_footman_multiplayer"),

	  #Sarranid mamluke
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_gekokujo_sandal_1", "trp_sarranid_mamluke_multiplayer")


      ]),
  #script_get_army_size_from_slider_value
  # INPUT: arg1 = slider_value
  # OUTPUT: reg0 = army_size
  ("get_army_size_from_slider_value",
    [
     (store_script_param, ":slider_value", 1),
     (assign, ":army_size", ":slider_value"),
     (try_begin),
       (gt, ":slider_value", 25),
       (store_sub, ":adder_value", ":slider_value", 25),
       (val_add, ":army_size", ":adder_value"),
       (try_begin),
         (gt, ":slider_value", 50),
         (store_sub, ":adder_value", ":slider_value", 50),
         (val_mul, ":adder_value", 3),
         (val_add, ":army_size", ":adder_value"),
       (try_end),
     (try_end),
     (assign, reg0, ":army_size"),
  ]),
  #script_spawn_quick_battle_army
  # INPUT: arg1 = initial_entry_point, arg2 = faction_no, arg3 = infantry_ratio, arg4 = archers_ratio, arg5 = cavalry_ratio, arg6 = divide_archer_entry_points, arg7 = player_team
  # OUTPUT: none
  ("spawn_quick_battle_army",
   [
     (store_script_param, ":cur_entry_point", 1),
     (store_script_param, ":faction_no", 2),
     (store_script_param, ":infantry_ratio", 3),
     (store_script_param, ":archers_ratio", 4),
     (store_script_param, ":cavalry_ratio", 5),
     (store_script_param, ":divide_archer_entry_points", 6),
     (store_script_param, ":player_team", 7),

     (try_begin),
       (eq, ":player_team", 1),
       (call_script, "script_get_army_size_from_slider_value", "$g_quick_battle_army_1_size"),
       (assign, ":army_size", reg0),
       (set_player_troop, "$g_quick_battle_troop"),
       (set_visitor, ":cur_entry_point", "$g_quick_battle_troop"),
       (try_begin),
         (eq, ":cur_entry_point", 0),
         (try_begin),
           (is_between, ":faction_no", npc_kingdoms_begin, npc_kingdoms_end),
           (faction_get_slot, "$g_quick_battle_team_0_banner", ":faction_no", slot_faction_banner),
         (else_try),
           (assign, "$g_quick_battle_team_0_banner", "mesh_banners_default_b"),
         (try_end),
       (else_try),
         (try_begin),
           (is_between, ":faction_no", npc_kingdoms_begin, npc_kingdoms_end),
           (faction_get_slot, "$g_quick_battle_team_1_banner", ":faction_no", slot_faction_banner),
         (else_try),
           (assign, "$g_quick_battle_team_1_banner", "mesh_banners_default_b"),
         (try_end),
       (try_end),
       (val_add, ":cur_entry_point", 1),

     (else_try),
       (call_script, "script_get_army_size_from_slider_value", "$g_quick_battle_army_2_size"),
       (assign, ":army_size", reg0),
       (try_begin),
         (eq, ":cur_entry_point", 0),
         (assign, "$g_quick_battle_team_0_banner", "mesh_banners_default_a"),
       (else_try),
         (assign, "$g_quick_battle_team_1_banner", "mesh_banners_default_a"),
       (try_end),
       (val_add, ":cur_entry_point", 1),
     (try_end),

     (store_mul, ":num_infantry", ":infantry_ratio", ":army_size"),
     (val_div, ":num_infantry", 100),
     (store_mul, ":num_archers", ":archers_ratio", ":army_size"),
     (val_div, ":num_archers", 100),
     (store_mul, ":num_cavalry", ":cavalry_ratio", ":army_size"),
     (val_div, ":num_cavalry", 100),

     (try_begin),
       (store_add, ":num_total", ":num_infantry", ":num_archers"),
       (val_add, ":num_total", ":num_cavalry"),
       (neq, ":num_total", ":army_size"),
       (store_sub, ":leftover", ":army_size", ":num_total"),
       (try_begin),
         (gt, ":infantry_ratio", ":archers_ratio"),
         (gt, ":infantry_ratio", ":cavalry_ratio"),
         (val_add, ":num_infantry", ":leftover"),
       (else_try),
         (gt, ":archers_ratio", ":cavalry_ratio"),
         (val_add, ":num_archers", ":leftover"),
       (else_try),
         (val_add, ":num_cavalry", ":leftover"),
       (try_end),
     (try_end),

     (store_mul, ":rand_min", ":num_infantry", 15),
     (val_div, ":rand_min", 100),
     (store_mul, ":rand_max", ":num_infantry", 45),
     (val_div, ":rand_max", 100),
     (store_random_in_range, ":num_tier_2_infantry", ":rand_min", ":rand_max"),
     (store_sub, ":num_tier_1_infantry", ":num_infantry", ":num_tier_2_infantry"),
     (store_mul, ":rand_min", ":num_archers", 15),
     (val_div, ":rand_min", 100),
     (store_mul, ":rand_max", ":num_archers", 45),
     (val_div, ":rand_max", 100),
     (store_random_in_range, ":num_tier_2_archers", ":rand_min", ":rand_max"),
     (store_sub, ":num_tier_1_archers", ":num_archers", ":num_tier_2_archers"),
     (store_mul, ":rand_min", ":num_cavalry", 15),
     (val_div, ":rand_min", 100),
     (store_mul, ":rand_max", ":num_cavalry", 45),
     (val_div, ":rand_max", 100),
     (store_random_in_range, ":num_tier_2_cavalry", ":rand_min", ":rand_max"),
     (store_sub, ":num_tier_1_cavalry", ":num_cavalry", ":num_tier_2_cavalry"),

     (faction_get_slot, ":cur_troop", ":faction_no", slot_faction_quick_battle_tier_2_infantry),
     (set_visitors, ":cur_entry_point", ":cur_troop", ":num_tier_2_infantry"),
     (val_add, ":cur_entry_point", 1),
     (faction_get_slot, ":cur_troop", ":faction_no", slot_faction_quick_battle_tier_1_infantry),
     (set_visitors, ":cur_entry_point", ":cur_troop", ":num_tier_1_infantry"),
     (val_add, ":cur_entry_point", 1),
     (faction_get_slot, ":cur_troop", ":faction_no", slot_faction_quick_battle_tier_2_cavalry),
     (set_visitors, ":cur_entry_point", ":cur_troop", ":num_tier_2_cavalry"),
     (val_add, ":cur_entry_point", 1),
     (faction_get_slot, ":cur_troop", ":faction_no", slot_faction_quick_battle_tier_1_cavalry),
     (set_visitors, ":cur_entry_point", ":cur_troop", ":num_tier_1_cavalry"),
     (val_add, ":cur_entry_point", 1),

     (try_begin),
       (eq, ":divide_archer_entry_points", 0),
       (faction_get_slot, ":cur_troop", ":faction_no", slot_faction_quick_battle_tier_2_archer),
       (set_visitors, ":cur_entry_point", ":cur_troop", ":num_tier_2_archers"),
       (val_add, ":cur_entry_point", 1),
       (faction_get_slot, ":cur_troop", ":faction_no", slot_faction_quick_battle_tier_1_archer),
       (set_visitors, ":cur_entry_point", ":cur_troop", ":num_tier_1_archers"),
       (val_add, ":cur_entry_point", 1),
     (else_try),
       (assign, ":cur_entry_point", 40), #archer positions begin point
       (store_div, ":num_tier_1_archers_ceil_8", ":num_tier_1_archers", 8),
       (val_mul, ":num_tier_1_archers_ceil_8", 8),
       (try_begin),
         (neq, ":num_tier_1_archers_ceil_8", ":num_tier_1_archers"),
         (val_div, ":num_tier_1_archers_ceil_8", 8),
         (val_add, ":num_tier_1_archers_ceil_8", 1),
         (val_mul, ":num_tier_1_archers_ceil_8", 8),
       (try_end),
       (store_div, ":num_tier_2_archers_ceil_8", ":num_tier_2_archers", 8),
       (val_mul, ":num_tier_2_archers_ceil_8", 8),
       (try_begin),
         (neq, ":num_tier_2_archers_ceil_8", ":num_tier_2_archers"),
         (val_div, ":num_tier_2_archers_ceil_8", 8),
         (val_add, ":num_tier_2_archers_ceil_8", 1),
         (val_mul, ":num_tier_2_archers_ceil_8", 8),
       (try_end),
       (store_add, ":num_archers_ceil_8", ":num_tier_1_archers_ceil_8", ":num_tier_2_archers_ceil_8"),
       (store_div, ":num_archers_per_entry_point", ":num_archers_ceil_8", 8),
       (assign, ":left_tier_1_archers", ":num_tier_1_archers"),
       (assign, ":left_tier_2_archers", ":num_tier_2_archers"),
       (assign, ":end_cond", 1000),
       (try_for_range, ":unused", 0, ":end_cond"),
         (try_begin),
           (gt, ":left_tier_2_archers", 0),
           (assign, ":used_tier_2_archers", ":num_archers_per_entry_point"),
           (val_min, ":used_tier_2_archers", ":left_tier_2_archers"),
           (faction_get_slot, ":cur_troop", ":faction_no", slot_faction_quick_battle_tier_2_archer),
           (set_visitors, ":cur_entry_point", ":cur_troop", ":used_tier_2_archers"),
           (val_add, ":cur_entry_point", 1),
           (val_sub, ":left_tier_2_archers", ":used_tier_2_archers"),
         (else_try),
           (gt, ":left_tier_1_archers", 0),
           (assign, ":used_tier_1_archers", ":num_archers_per_entry_point"),
           (val_min, ":used_tier_1_archers", ":left_tier_1_archers"),
           (faction_get_slot, ":cur_troop", ":faction_no", slot_faction_quick_battle_tier_1_archer),
           (set_visitors, ":cur_entry_point", ":cur_troop", ":used_tier_1_archers"),
           (val_add, ":cur_entry_point", 1),
           (val_sub, ":left_tier_1_archers", ":used_tier_1_archers"),
         (else_try),
           (assign, ":end_cond", 0),
         (try_end),
       (try_end),
     (try_end),
     ]),
  ("player_arrived",
   [
      (assign, ":player_faction_culture", "fac_culture_1"),
	  #gekokujo 3.0 get rid of player culture
      #(assign, ":player_faction_culture", "fac_culture_player"),
      (faction_set_slot, "fac_player_supporters_faction",  slot_faction_culture, ":player_faction_culture"),
      (faction_set_slot, "fac_player_faction",  slot_faction_culture, ":player_faction_culture"),
	]),
  #script_game_enable_cheat_menu
  # This script is called from the game engine when user enters "cheatmenu from command console (ctrl+~).
  # INPUT:
  # none
  # OUTPUT:
  # none
  ("game_enable_cheat_menu",
    [
      (store_script_param, ":input", 1),
      (try_begin),
        (eq, ":input", 0),
        (assign, "$cheat_mode", 0),
      (else_try),
        (eq, ":input", 1),
        (assign, "$cheat_mode", 1),
      (try_end),
      ]),
  #script_game_get_console_command
  # This script is called from the game engine when a console command is entered from the dedicated server.
  # INPUT: anything
  # OUTPUT: s0 = result text
  ("game_get_console_command",
   [
     (store_script_param, ":input", 1),
     (store_script_param, ":val1", 2),
     (try_begin),
       #getting val2 for some commands
       (eq, ":input", 2),
       (store_script_param, ":val2", 3),
     (end_try),
     (try_begin),
       (eq, ":input", 1),
       (assign, reg0, ":val1"),
       (try_begin),
         (eq, ":val1", 1),
         (assign, reg1, "$g_multiplayer_num_bots_team_1"),
         (str_store_string, s0, "str_team_reg0_bot_count_is_reg1"),
       (else_try),
         (eq, ":val1", 2),
         (assign, reg1, "$g_multiplayer_num_bots_team_2"),
         (str_store_string, s0, "str_team_reg0_bot_count_is_reg1"),
       (else_try),
         (str_store_string, s0, "str_input_is_not_correct_for_the_command_type_help_for_more_information"),
       (try_end),
     (else_try),
       (eq, ":input", 2),
       (assign, reg0, ":val1"),
       (assign, reg1, ":val2"),
       (try_begin),
         (eq, ":val1", 1),
         (ge, ":val2", 0),
         (assign, "$g_multiplayer_num_bots_team_1", ":val2"),
         (str_store_string, s0, "str_team_reg0_bot_count_is_reg1"),
       (else_try),
         (eq, ":val1", 2),
         (ge, ":val2", 0),
         (assign, "$g_multiplayer_num_bots_team_2", ":val2"),
         (str_store_string, s0, "str_team_reg0_bot_count_is_reg1"),
       (else_try),
         (str_store_string, s0, "str_input_is_not_correct_for_the_command_type_help_for_more_information"),
       (try_end),
     (else_try),
       (eq, ":input", 3),
       (assign, reg0, "$g_multiplayer_round_max_seconds"),
       (str_store_string, s0, "str_maximum_seconds_for_round_is_reg0"),
     (else_try),
       (eq, ":input", 4),
       (assign, reg0, ":val1"),
       (try_begin),
         (is_between, ":val1", multiplayer_round_max_seconds_min, multiplayer_round_max_seconds_max),
         (assign, "$g_multiplayer_round_max_seconds", ":val1"),
         (str_store_string, s0, "str_maximum_seconds_for_round_is_reg0"),
         (get_max_players, ":num_players"),
         (try_for_range, ":cur_player", 1, ":num_players"),
           (player_is_active, ":cur_player"),
           (multiplayer_send_int_to_player, ":cur_player", multiplayer_event_return_round_max_seconds, ":val1"),
         (try_end),            
       (else_try),
         (str_store_string, s0, "str_input_is_not_correct_for_the_command_type_help_for_more_information"),
       (try_end),
     (else_try),
       (eq, ":input", 5),
       (assign, reg0, "$g_multiplayer_respawn_period"),
       (str_store_string, s0, "str_respawn_period_is_reg0_seconds"),
     (else_try),
       (eq, ":input", 6),
       (assign, reg0, ":val1"),
       (try_begin),
         (is_between, ":val1", multiplayer_respawn_period_min, multiplayer_respawn_period_max),
         (assign, "$g_multiplayer_respawn_period", ":val1"),
         (str_store_string, s0, "str_respawn_period_is_reg0_seconds"),
       (else_try),
         (str_store_string, s0, "str_input_is_not_correct_for_the_command_type_help_for_more_information"),
       (try_end),
     (else_try),
       (eq, ":input", 7),
       (assign, reg0, "$g_multiplayer_num_bots_voteable"),
       (str_store_string, s0, "str_bots_upper_limit_for_votes_is_reg0"),
     (else_try),
       (eq, ":input", 8),
       (try_begin),
         (is_between, ":val1", 0, 51),
         (assign, "$g_multiplayer_num_bots_voteable", ":val1"),
         (store_add, "$g_multiplayer_max_num_bots", ":val1", 1),
         (assign, reg0, "$g_multiplayer_num_bots_voteable"),
         (str_store_string, s0, "str_bots_upper_limit_for_votes_is_reg0"),
         (get_max_players, ":num_players"),
         (try_for_range, ":cur_player", 1, ":num_players"),
           (player_is_active, ":cur_player"),
           (multiplayer_send_int_to_player, ":cur_player", multiplayer_event_return_num_bots_voteable, ":val1"),
         (try_end),
       (else_try),
         (str_store_string, s0, "str_input_is_not_correct_for_the_command_type_help_for_more_information"),
       (try_end),
     (else_try),
       (eq, ":input", 9),
       (try_begin),
         (eq, "$g_multiplayer_maps_voteable", 1),
         (str_store_string, s0, "str_map_is_voteable"),
       (else_try),
         (str_store_string, s0, "str_map_is_not_voteable"),
       (try_end),
     (else_try),
       (eq, ":input", 10),
       (try_begin),
         (is_between, ":val1", 0, 2),
         (assign, "$g_multiplayer_maps_voteable", ":val1"),
         (try_begin),
           (eq, ":val1", 1),
           (str_store_string, s0, "str_map_is_voteable"),
         (else_try),
           (str_store_string, s0, "str_map_is_not_voteable"),
         (try_end),
         (get_max_players, ":num_players"),
         (try_for_range, ":cur_player", 1, ":num_players"),
           (player_is_active, ":cur_player"),
           (multiplayer_send_int_to_player, ":cur_player", multiplayer_event_return_maps_voteable, ":val1"),
         (try_end),
       (else_try),
         (str_store_string, s0, "str_input_is_not_correct_for_the_command_type_help_for_more_information"),
       (try_end),
     (else_try),
       (eq, ":input", 11),
       (try_begin),
         (eq, "$g_multiplayer_factions_voteable", 1),
         (str_store_string, s0, "str_factions_are_voteable"),
       (else_try),
         (str_store_string, s0, "str_factions_are_not_voteable"),
       (try_end),
     (else_try),
       (eq, ":input", 12),
       (try_begin),
         (is_between, ":val1", 0, 2),
         (assign, "$g_multiplayer_factions_voteable", ":val1"),
         (try_begin),
           (eq, ":val1", 1),
           (str_store_string, s0, "str_factions_are_voteable"),
         (else_try),
           (str_store_string, s0, "str_factions_are_not_voteable"),
         (try_end),
         (get_max_players, ":num_players"),
         (try_for_range, ":cur_player", 1, ":num_players"),
           (player_is_active, ":cur_player"),
           (multiplayer_send_int_to_player, ":cur_player", multiplayer_event_return_factions_voteable, ":val1"),
         (try_end),
       (else_try),
         (str_store_string, s0, "str_input_is_not_correct_for_the_command_type_help_for_more_information"),
       (try_end),
     (else_try),
       (eq, ":input", 13),
       (try_begin),
         (eq, "$g_multiplayer_player_respawn_as_bot", 1),
         (str_store_string, s0, "str_players_respawn_as_bot"),
       (else_try),
         (str_store_string, s0, "str_players_do_not_respawn_as_bot"),
       (try_end),
     (else_try),
       (eq, ":input", 14),
       (try_begin),
         (is_between, ":val1", 0, 2),
         (assign, "$g_multiplayer_player_respawn_as_bot", ":val1"),
         (try_begin),
           (eq, ":val1", 1),
           (str_store_string, s0, "str_players_respawn_as_bot"),
         (else_try),
           (str_store_string, s0, "str_players_do_not_respawn_as_bot"),
         (try_end),
         (get_max_players, ":num_players"),
         (try_for_range, ":cur_player", 1, ":num_players"),
           (player_is_active, ":cur_player"),
           (multiplayer_send_int_to_player, ":cur_player", multiplayer_event_return_player_respawn_as_bot, ":val1"),
         (try_end),            
       (else_try),
         (str_store_string, s0, "str_input_is_not_correct_for_the_command_type_help_for_more_information"),
       (try_end),
     (else_try),
       (eq, ":input", 15),
       (try_begin),
         (eq, "$g_multiplayer_kick_voteable", 1),
         (str_store_string, s0, "str_kicking_a_player_is_voteable"),
       (else_try),
         (str_store_string, s0, "str_kicking_a_player_is_not_voteable"),
       (try_end),
     (else_try),
       (eq, ":input", 16),
       (try_begin),
         (is_between, ":val1", 0, 2),
         (assign, "$g_multiplayer_kick_voteable", ":val1"),
         (try_begin),
           (eq, ":val1", 1),
           (str_store_string, s0, "str_kicking_a_player_is_voteable"),
         (else_try),
           (str_store_string, s0, "str_kicking_a_player_is_not_voteable"),
         (try_end),
         (get_max_players, ":num_players"),
         (try_for_range, ":cur_player", 1, ":num_players"),
           (player_is_active, ":cur_player"),
           (multiplayer_send_int_to_player, ":cur_player", multiplayer_event_return_kick_voteable, ":val1"),
         (try_end),
       (else_try),
         (str_store_string, s0, "str_input_is_not_correct_for_the_command_type_help_for_more_information"),
       (try_end),
     (else_try),
       (eq, ":input", 17),
       (try_begin),
         (eq, "$g_multiplayer_ban_voteable", 1),
         (str_store_string, s0, "str_banning_a_player_is_voteable"),
       (else_try),
         (str_store_string, s0, "str_banning_a_player_is_not_voteable"),
       (try_end),
     (else_try),
       (eq, ":input", 18),
       (try_begin),
         (is_between, ":val1", 0, 2),
         (assign, "$g_multiplayer_ban_voteable", ":val1"),
         (try_begin),
           (eq, ":val1", 1),
           (str_store_string, s0, "str_banning_a_player_is_voteable"),
         (else_try),
           (str_store_string, s0, "str_banning_a_player_is_not_voteable"),
         (try_end),
         (get_max_players, ":num_players"),
         (try_for_range, ":cur_player", 1, ":num_players"),
           (player_is_active, ":cur_player"),
           (multiplayer_send_int_to_player, ":cur_player", multiplayer_event_return_ban_voteable, ":val1"),
         (try_end),
       (else_try),
         (str_store_string, s0, "str_input_is_not_correct_for_the_command_type_help_for_more_information"),
       (try_end),
     (else_try),
       (eq, ":input", 19),
       (assign, reg0, "$g_multiplayer_valid_vote_ratio"),
       (str_store_string, s0, "str_percentage_of_yes_votes_required_for_a_poll_to_get_accepted_is_reg0"),
     (else_try),
       (eq, ":input", 20),
       (try_begin),
         (is_between, ":val1", 50, 101),
         (assign, "$g_multiplayer_valid_vote_ratio", ":val1"),
         (assign, reg0, ":val1"),
         (str_store_string, s0, "str_percentage_of_yes_votes_required_for_a_poll_to_get_accepted_is_reg0"),
       (else_try),
         (str_store_string, s0, "str_input_is_not_correct_for_the_command_type_help_for_more_information"),
       (try_end),
     (else_try),
       (eq, ":input", 21),
       (assign, reg0, "$g_multiplayer_auto_team_balance_limit"),
       (str_store_string, s0, "str_auto_team_balance_threshold_is_reg0"),
     (else_try),
       (eq, ":input", 22),
       (try_begin),
         (is_between, ":val1", 2, 7),
         (assign, "$g_multiplayer_auto_team_balance_limit", ":val1"),
         (assign, reg0, "$g_multiplayer_auto_team_balance_limit"),
         (str_store_string, s0, "str_auto_team_balance_threshold_is_reg0"),
         (get_max_players, ":num_players"),
         (try_for_range, ":cur_player", 1, ":num_players"),
           (player_is_active, ":cur_player"),
           (multiplayer_send_int_to_player, ":cur_player", multiplayer_event_return_auto_team_balance_limit, ":val1"),
         (try_end),
       (else_try),
         (ge, ":val1", 7),
         (assign, "$g_multiplayer_auto_team_balance_limit", 1000),
         (assign, reg0, "$g_multiplayer_auto_team_balance_limit"),
         (str_store_string, s0, "str_auto_team_balance_threshold_is_reg0"),
         (get_max_players, ":num_players"),
         (try_for_range, ":cur_player", 1, ":num_players"),
           (player_is_active, ":cur_player"),
           (multiplayer_send_int_to_player, ":cur_player", multiplayer_event_return_auto_team_balance_limit, ":val1"),
         (try_end),
       (else_try),
         (str_store_string, s0, "str_input_is_not_correct_for_the_command_type_help_for_more_information"),
       (try_end),
     (else_try),
       (eq, ":input", 23),
       (assign, reg0, "$g_multiplayer_initial_gold_multiplier"),
       (str_store_string, s0, "str_starting_gold_ratio_is_reg0"),
     (else_try),
       (eq, ":input", 24),
       (try_begin),
         (is_between, ":val1", 0, 1001),
         (assign, "$g_multiplayer_initial_gold_multiplier", ":val1"),
         (assign, reg0, "$g_multiplayer_initial_gold_multiplier"),
         (str_store_string, s0, "str_starting_gold_ratio_is_reg0"),
       (else_try),
         (str_store_string, s0, "str_input_is_not_correct_for_the_command_type_help_for_more_information"),
       (try_end),
     (else_try),
       (eq, ":input", 25),
       (assign, reg0, "$g_multiplayer_battle_earnings_multiplier"),
       (str_store_string, s0, "str_combat_gold_bonus_ratio_is_reg0"),
     (else_try),
       (eq, ":input", 26),
       (try_begin),
         (is_between, ":val1", 0, 1001),
         (assign, "$g_multiplayer_battle_earnings_multiplier", ":val1"),
         (assign, reg0, "$g_multiplayer_battle_earnings_multiplier"),
         (str_store_string, s0, "str_combat_gold_bonus_ratio_is_reg0"),
       (else_try),
         (str_store_string, s0, "str_input_is_not_correct_for_the_command_type_help_for_more_information"),
       (try_end),
     (else_try),
       (eq, ":input", 27),
       (assign, reg0, "$g_multiplayer_round_earnings_multiplier"),
       (str_store_string, s0, "str_round_gold_bonus_ratio_is_reg0"),
     (else_try),
       (eq, ":input", 28),
       (try_begin),
         (is_between, ":val1", 0, 1001),
         (assign, "$g_multiplayer_round_earnings_multiplier", ":val1"),
         (assign, reg0, "$g_multiplayer_round_earnings_multiplier"),
         (str_store_string, s0, "str_round_gold_bonus_ratio_is_reg0"),
       (else_try),
         (str_store_string, s0, "str_input_is_not_correct_for_the_command_type_help_for_more_information"),
       (try_end),
     (else_try),
       (eq, ":input", 29),
       (try_begin),
         (eq, "$g_multiplayer_allow_player_banners", 1),
         (str_store_string, s0, "str_player_banners_are_allowed"),
       (else_try),
         (str_store_string, s0, "str_player_banners_are_not_allowed"),
       (try_end),
     (else_try),
       (eq, ":input", 30),
       (try_begin),
         (is_between, ":val1", 0, 2),
         (assign, "$g_multiplayer_allow_player_banners", ":val1"),
         (try_begin),
           (eq, ":val1", 1),
           (str_store_string, s0, "str_player_banners_are_allowed"),
         (else_try),
           (str_store_string, s0, "str_player_banners_are_not_allowed"),
         (try_end),
       (else_try),
         (str_store_string, s0, "str_input_is_not_correct_for_the_command_type_help_for_more_information"),
       (try_end),
     (else_try),
       (eq, ":input", 31),
       (try_begin),
         (eq, "$g_multiplayer_force_default_armor", 1),
         (str_store_string, s0, "str_default_armor_is_forced"),
       (else_try),
         (str_store_string, s0, "str_default_armor_is_not_forced"),
       (try_end),
     (else_try),
       (eq, ":input", 32),
       (try_begin),
         (is_between, ":val1", 0, 2),
         (assign, "$g_multiplayer_force_default_armor", ":val1"),
         (try_begin),
           (eq, ":val1", 1),
           (str_store_string, s0, "str_default_armor_is_forced"),
         (else_try),
           (str_store_string, s0, "str_default_armor_is_not_forced"),
         (try_end),
       (else_try),
         (str_store_string, s0, "str_input_is_not_correct_for_the_command_type_help_for_more_information"),
       (try_end),
     (else_try),
       (eq, ":input", 33),
       (assign, reg0, "$g_multiplayer_point_gained_from_flags"),
       (str_store_string, s0, "str_point_gained_from_flags_is_reg0"),
     (else_try),
       (eq, ":input", 34),
       (try_begin),
         (is_between, ":val1", 25, 401),
         (assign, "$g_multiplayer_point_gained_from_flags", ":val1"),
         (assign, reg0, "$g_multiplayer_point_gained_from_flags"),
         (str_store_string, s0, "str_point_gained_from_flags_is_reg0"),
       (else_try),
         (str_store_string, s0, "str_input_is_not_correct_for_the_command_type_help_for_more_information"),
       (try_end),
     (else_try),
       (eq, ":input", 35),
       (assign, reg0, "$g_multiplayer_point_gained_from_capturing_flag"),
       (str_store_string, s0, "str_point_gained_from_capturing_flag_is_reg0"),
     (else_try),
       (eq, ":input", 36),
       (try_begin),
         (is_between, ":val1", 0, 11),
         (assign, "$g_multiplayer_point_gained_from_capturing_flag", ":val1"),
         (assign, reg0, "$g_multiplayer_point_gained_from_capturing_flag"),
         (str_store_string, s0, "str_point_gained_from_capturing_flag_is_reg0"),
       (else_try),
         (str_store_string, s0, "str_input_is_not_correct_for_the_command_type_help_for_more_information"),
       (try_end),
     (else_try),
       (eq, ":input", 37),
       (assign, reg0, "$g_multiplayer_game_max_minutes"),
       (str_store_string, s0, "str_map_time_limit_is_reg0"),
     (else_try),
       (eq, ":input", 38),
       (try_begin),
         (is_between, ":val1", 5, 121),
         (assign, "$g_multiplayer_game_max_minutes", ":val1"),
         (assign, reg0, "$g_multiplayer_game_max_minutes"),
         (str_store_string, s0, "str_map_time_limit_is_reg0"),
       (else_try),
         (str_store_string, s0, "str_input_is_not_correct_for_the_command_type_help_for_more_information"),
       (try_end),
     (else_try),
       (eq, ":input", 39),
       (assign, reg0, "$g_multiplayer_game_max_points"),
       (str_store_string, s0, "str_team_points_limit_is_reg0"),
     (else_try),
       (eq, ":input", 40),
       (try_begin),
         (is_between, ":val1", 3, 1001),
         (assign, "$g_multiplayer_game_max_points", ":val1"),
         (assign, reg0, "$g_multiplayer_game_max_points"),
         (str_store_string, s0, "str_team_points_limit_is_reg0"),
       (else_try),
         (str_store_string, s0, "str_input_is_not_correct_for_the_command_type_help_for_more_information"),
       (try_end),
     (else_try),
       (eq, ":input", 41),
       (assign, reg0, "$g_multiplayer_number_of_respawn_count"),
       (try_begin),
         (eq, reg0, 0),
         (str_store_string, s1, "str_unlimited"),
       (else_try),
         (str_store_string, s1, "str_reg0"),
       (try_end),
       (str_store_string, s0, "str_defender_spawn_count_limit_is_s1"),
     (else_try),
       (eq, ":input", 42),
       (try_begin),
         (is_between, ":val1", 0, 6),
         (assign, "$g_multiplayer_number_of_respawn_count", ":val1"),
         (assign, reg0, "$g_multiplayer_number_of_respawn_count"),
         (try_begin),
           (eq, reg0, 0),
           (str_store_string, s1, "str_unlimited"),
         (else_try),
           (str_store_string, s1, "str_reg0"),
         (try_end),
         (str_store_string, s0, "str_defender_spawn_count_limit_is_s1"),
         (get_max_players, ":num_players"),
         (try_for_range, ":cur_player", 1, ":num_players"),
           (player_is_active, ":cur_player"),
           (multiplayer_send_int_to_player, ":cur_player", multiplayer_event_return_respawn_count, ":val1"),
         (try_end),                  
       (else_try),
         (str_store_string, s0, "str_input_is_not_correct_for_the_command_type_help_for_more_information"),
       (try_end),
     (else_try),
       (eq, ":input", 43),
       (try_begin),
         (eq, "$g_multiplayer_disallow_ranged_weapons", 1),
         (str_store_string, s0, "str_ranged_weapons_are_disallowed"),
       (else_try),
         (str_store_string, s0, "str_ranged_weapons_are_allowed"),
       (try_end),
     (else_try),
       (eq, ":input", 44),
       (try_begin),
         (is_between, ":val1", 0, 2),
         (assign, "$g_multiplayer_disallow_ranged_weapons", ":val1"),
         (try_begin),
           (eq, ":val1", 1),
           (str_store_string, s0, "str_ranged_weapons_are_disallowed"),
         (else_try),
           (str_store_string, s0, "str_ranged_weapons_are_allowed"),
         (try_end),
       (else_try),
         (str_store_string, s0, "str_input_is_not_correct_for_the_command_type_help_for_more_information"),
       (try_end),
     (else_try),
       (str_store_string, s0, "@{!}DEBUG : SYSTEM ERROR!"),
     (try_end),
  ]),
  # script_game_event_party_encounter:
  # This script is called from the game engine whenever player party encounters another party or a battle on the world map
  # INPUT:
  # param1: encountered_party
  # param2: second encountered_party (if this was a battle
  ("game_event_party_encounter",
   [
       (store_script_param_1, "$g_encountered_party"),
       (store_script_param_2, "$g_encountered_party_2"),# encountered_party2 is set when we come across a battle or siege, otherwise it's a negative value
#       (store_encountered_party, "$g_encountered_party"),
#       (store_encountered_party2,"$g_encountered_party_2"), # encountered_party2 is set when we come across a battle or siege, otherwise it's a minus value
       (store_faction_of_party, "$g_encountered_party_faction","$g_encountered_party"),
       (store_relation, "$g_encountered_party_relation", "$g_encountered_party_faction", "fac_player_faction"),
              
       (party_get_slot, "$g_encountered_party_type", "$g_encountered_party", slot_party_type),
       (party_get_template_id,"$g_encountered_party_template","$g_encountered_party"),
#       (try_begin),
#         (gt, "$g_encountered_party_2", 0),
#         (store_faction_of_party, "$g_encountered_party_2_faction","$g_encountered_party_2"),
#         (store_relation, "$g_encountered_party_2_relation", "$g_encountered_party_2_faction", "fac_player_faction"),
#         (party_get_template_id,"$g_encountered_party_2_template","$g_encountered_party_2"),
#       (else_try),
#         (assign, "$g_encountered_party_2_faction",-1),
#         (assign, "$g_encountered_party_2_relation", 0),
#         (assign,"$g_encountered_party_2_template", -1),
#       (try_end),

#NPC companion changes begin
       (call_script, "script_party_count_fit_regulars", "p_main_party"),
       (assign, "$playerparty_prebattle_regulars", reg0),

#        (try_begin),
#            (assign, "$player_party__regulars", 0),
#            (call_script, "script_party_count_fit_regulars", "p_main_party"),
#            (gt, reg0, 0),
#            (assign, "$player_party_contains_regulars", 1),
#        (try_end),
#NPC companion changes end


       (assign, "$g_last_rest_center", -1),
       (assign, "$talk_context", 0),
       (assign,"$g_player_surrenders",0),
       (assign,"$g_enemy_surrenders",0),
       (assign, "$g_leave_encounter",0),
       (assign, "$g_engaged_enemy", 0),
#       (assign,"$waiting_for_arena_fight_result", 0),
#       (assign,"$arena_bet_amount",0),
#       (assign,"$g_player_raiding_village",0),
       (try_begin),
         (neg|is_between, "$g_encountered_party", centers_begin, centers_end),
         (rest_for_hours, 0), #stop waiting
         (assign, "$g_infinite_camping", 0),
       (try_end),
#       (assign, "$g_permitted_to_center",0),
       (assign, "$new_encounter", 1), #check this in the menu.
       (try_begin),
         (lt, "$g_encountered_party_2",0), #Normal encounter. Not battle or siege.
         (try_begin),
           (party_slot_eq, "$g_encountered_party", slot_party_type, spt_town),
           (jump_to_menu, "mnu_castle_outside"),
         (else_try),
           (party_slot_eq, "$g_encountered_party", slot_party_type, spt_castle),
           (jump_to_menu, "mnu_castle_outside"),
         (else_try),
           (party_slot_eq, "$g_encountered_party", slot_party_type, spt_ship),
           (jump_to_menu, "mnu_ship_reembark"),
         (else_try),
           (party_slot_eq, "$g_encountered_party", slot_party_type, spt_village),
           (jump_to_menu, "mnu_village"),
		 #gekokujo 3.0 microfactions! start
		 #this is how we bring up the menu, of course
         (else_try),
           (party_slot_eq, "$g_encountered_party", slot_party_type, spt_fort),
           (jump_to_menu, "mnu_fort"),
		 #gekokujo 3.0 microfactions! end
         (else_try),
           (party_slot_eq, "$g_encountered_party", slot_party_type, spt_cattle_herd),
           (jump_to_menu, "mnu_cattle_herd"),
         (else_try),
           (is_between, "$g_encountered_party", training_grounds_begin, training_grounds_end),
           (jump_to_menu, "mnu_training_ground"),
		 (else_try),  
		   (party_get_template_id, ":template", "$g_encountered_party"),
		   (ge, ":template", "pt_seto_pirate_lair"),
		   (lt, ":template", "pt_bandit_lair_templates_end"),
		   (assign, "$loot_screen_shown", 0),
#		   (call_script, "script_encounter_init_variables"),
		   (jump_to_menu, "mnu_bandit_lair"),
         (else_try),
           (eq, "$g_encountered_party", "p_zendar"),
           (jump_to_menu, "mnu_zendar"),
         (else_try),
           (eq, "$g_encountered_party", "p_salt_mine"),
           (jump_to_menu, "mnu_salt_mine"),
         (else_try),
           (eq, "$g_encountered_party", "p_four_ways_inn"),
           (jump_to_menu, "mnu_four_ways_inn"),
         (else_try),
           (eq, "$g_encountered_party", "p_test_scene"),
           (jump_to_menu, "mnu_test_scene"),
         (else_try),
           (eq, "$g_encountered_party", "p_battlefields"),
           (jump_to_menu, "mnu_battlefields"),
         (else_try),
           (eq, "$g_encountered_party", "p_training_ground"),
           (jump_to_menu, "mnu_tutorial"),
         (else_try),
           (eq, "$g_encountered_party", "p_camp_bandits"),           
           (jump_to_menu, "mnu_camp"),
         #gekokujo 3.1 bogmir's quests start
         (else_try),
           (eq, "$g_encountered_party", "p_hidden_village"),
           (jump_to_menu, "mnu_hidden_village"),
         #gekokujo 3.1 bogmir's quest end
         (else_try),
           (jump_to_menu, "mnu_simple_encounter"),
         (try_end),
       (else_try), #Battle or siege
         (try_begin),
           (this_or_next|party_slot_eq, "$g_encountered_party", slot_party_type, spt_town),
           (party_slot_eq, "$g_encountered_party", slot_party_type, spt_castle),
           (try_begin),
             (eq, "$auto_enter_town", "$g_encountered_party"),
             (jump_to_menu, "mnu_town"),
           (else_try),
             (eq, "$auto_besiege_town", "$g_encountered_party"),
             (jump_to_menu, "mnu_besiegers_camp_with_allies"),
           (else_try),
             (jump_to_menu, "mnu_join_siege_outside"),
           (try_end),
         (else_try),
           (jump_to_menu, "mnu_pre_join"),
         (try_end),
       (try_end),
       (assign,"$auto_enter_town",0),
       (assign,"$auto_besiege_town",0),
      ]),
  #script_game_event_simulate_battle:
  # This script is called whenever the game simulates the battle between two parties on the map.
  # INPUT:
  # param1: Defender Party
  # param2: Attacker Party
  ("game_event_simulate_battle",
    [
      (store_script_param_1, ":root_defender_party"),
      (store_script_param_2, ":root_attacker_party"),

      (assign, "$marshall_defeated_in_battle", -1),

      (store_current_hours, ":hours"),
      
      ##diplomacy start+ Get campaign AI, used below
      (game_get_reduce_campaign_ai, ":reduce_campaign_ai"),
      ##diplomacy end+
      
      (try_for_parties, ":party"),
        (party_get_battle_opponent, ":opponent", ":party"),
        (gt, ":opponent", 0),
        (party_set_slot, ":party", slot_party_last_in_combat, ":hours"),
      (try_end),

      (assign, ":trigger_result", 1),
      (try_begin),
        (ge, ":root_defender_party", 0),
        (ge, ":root_attacker_party", 0),
        (party_is_active, ":root_defender_party"),
        (party_is_active, ":root_attacker_party"),
        (store_faction_of_party, ":defender_faction", ":root_defender_party"),
        (store_faction_of_party, ":attacker_faction", ":root_attacker_party"),
        #(neq, ":defender_faction", "fac_player_faction"),
        #(neq, ":attacker_faction", "fac_player_faction"),		
        (store_relation, ":reln", ":defender_faction", ":attacker_faction"),
        (lt, ":reln", 0),
        (assign, ":trigger_result", 0),

        (try_begin),
          (this_or_next|eq, "$g_battle_simulation_cancel_for_party", ":root_defender_party"),
          (eq, "$g_battle_simulation_cancel_for_party", ":root_attacker_party"),
          (assign, "$g_battle_simulation_cancel_for_party", -1),
          (assign, "$auto_enter_town", "$g_battle_simulation_auto_enter_town_after_battle"),		  
          (assign, ":trigger_result", 1),
        (else_try),
          (try_begin),
            (this_or_next|party_slot_eq, ":root_defender_party", slot_party_retreat_flag, 1),
            (party_slot_eq, ":root_attacker_party", slot_party_retreat_flag, 1),
            (assign, ":trigger_result", 1), #End battle!
          (try_end),
          (party_set_slot, ":root_attacker_party", slot_party_retreat_flag, 0),		  

          #(assign, ":cancel_attack", 0),

          (party_collect_attachments_to_party, ":root_defender_party", "p_collective_ally"),
          (party_collect_attachments_to_party, ":root_attacker_party", "p_collective_enemy"),

	      ##diplomacy start+
 		  (assign, ":terrain_code", dplmc_terrain_code_none),#defined in header_terrain.py
          (try_begin),
              (eq, "$g_dplmc_terrain_advantage", DPLMC_TERRAIN_ADVANTAGE_ENABLE),
			  (call_script, "script_dplmc_get_terrain_code_for_battle", ":root_attacker_party", ":root_defender_party"),
			  (assign, ":terrain_code", reg0),
			  #
              (call_script, "script_dplmc_party_calculate_strength_in_terrain", "p_collective_ally", ":terrain_code", 0, 1),
              (assign, ":defender_strength", reg0),
              (call_script, "script_dplmc_party_calculate_strength_in_terrain", "p_collective_enemy", ":terrain_code", 0, 1),
              (assign, ":attacker_strength", reg0),
          (else_try),
              (call_script, "script_party_calculate_strength", "p_collective_ally", 0),
              (assign, ":defender_strength", reg0),
          #(call_script, "script_party_count_fit_for_battle", "p_collective_enemy"),
              (call_script, "script_party_calculate_strength", "p_collective_enemy", 0),
              (assign, ":attacker_strength", reg0),
          (try_end),
          ##diplomacy end+

          (store_div, ":defender_strength", ":defender_strength", 20),
          (val_min, ":defender_strength", 50),
          (val_max, ":defender_strength", 1),
          (store_div, ":attacker_strength", ":attacker_strength", 20),
          (val_min, ":attacker_strength", 50),
          (val_add, ":attacker_strength", 1),
          (try_begin),
            #For sieges increase attacker casualties and reduce defender casualties.
            (this_or_next|party_slot_eq, ":root_defender_party", slot_party_type, spt_castle),
            (party_slot_eq, ":root_defender_party", slot_party_type, spt_town),
            (val_mul, ":defender_strength", 123), #it was 1.5 in old version, now it is only 1.23
            (val_div, ":defender_strength", 100),
      
            (val_mul, ":attacker_strength", 100), #it was 0.5 in old version, now it is only 1 / 1.23
            (val_div, ":attacker_strength", 123),
          (try_end),		  
          
          ##diplomacy begin
          (assign, ":defender_percent", 100),
          (try_begin),
            (faction_get_slot, ":serfdom", ":defender_faction", dplmc_slot_faction_serfdom),
            (neq, ":serfdom", 0),
            (val_mul, ":serfdom", -2),
            (val_add, ":defender_percent", ":serfdom"),
          (try_end),
          (try_begin),
            (faction_get_slot, ":quality", ":defender_faction", dplmc_slot_faction_quality),
            (neq, ":quality", 0),
            (val_mul, ":quality", 4),
            (val_add, ":defender_percent", ":quality"),
          (try_end),
          (val_mul, ":defender_strength", ":defender_percent"),
          (val_div, ":defender_strength", 100),

          (assign, ":attacker_percent", 100),
          (try_begin),
            (faction_get_slot, ":serfdom", ":attacker_faction", dplmc_slot_faction_serfdom),
            (neq, ":serfdom", 0),
            (val_mul, ":serfdom", -2),
            (val_add, ":attacker_percent", ":serfdom"),
          (try_end),
          (try_begin),
            (faction_get_slot, ":quality", ":attacker_faction", dplmc_slot_faction_quality),
            (neq, ":quality", 0),
            (val_mul, ":quality", 4),
            (val_add, ":attacker_percent", ":quality"),
          (try_end),
          (val_mul, ":attacker_strength", ":attacker_percent"),
          (val_div, ":attacker_strength", 100),
          ##diplomacy end	

          (call_script, "script_party_count_fit_for_battle", "p_collective_ally", 0),
          (assign, ":old_defender_strength", reg0),

          (try_begin),
            (neg|is_currently_night), #Don't fight at night
            (inflict_casualties_to_party_group, ":root_attacker_party", ":defender_strength", "p_temp_casualties"),
            (party_collect_attachments_to_party, ":root_attacker_party", "p_collective_enemy"),
          (try_end),
          (call_script, "script_party_count_fit_for_battle", "p_collective_enemy", 0),
          (assign, ":new_attacker_strength", reg0),

          (try_begin),
            (gt, ":new_attacker_strength", 0),
            (neg|is_currently_night), #Don't fight at night
            (inflict_casualties_to_party_group, ":root_defender_party", ":attacker_strength", "p_temp_casualties"),
            (party_collect_attachments_to_party, ":root_defender_party", "p_collective_ally"),
          (try_end),
          (call_script, "script_party_count_fit_for_battle", "p_collective_ally", 0),
          (assign, ":new_defender_strength", reg0),		  

          (try_begin),
            (this_or_next|eq, ":new_attacker_strength", 0),
            (eq, ":new_defender_strength", 0),
            # Battle concluded! determine winner			
            
            (assign, ":do_not_end_battle", 0),
            (try_begin),
              (neg|troop_is_wounded, "trp_player"),
              (eq, ":new_defender_strength", 0),              
              (eq, "$auto_enter_town", "$g_encountered_party"),
              (eq, ":old_defender_strength", ":new_defender_strength"),
              (assign, ":do_not_end_battle", 1),
            (try_end),            
            (eq, ":do_not_end_battle", 0),

            (try_begin),
              (eq, ":new_attacker_strength", 0),
              (eq, ":new_defender_strength", 0),
              (assign, ":root_winner_party", -1),
              (assign, ":root_defeated_party", -1),
              (assign, ":collective_casualties", -1),
            (else_try),
              (eq, ":new_attacker_strength", 0),
              (assign, ":root_winner_party", ":root_defender_party"),
              (assign, ":root_defeated_party", ":root_attacker_party"),
              (assign, ":collective_casualties", "p_collective_enemy"),
            (else_try),
              (assign, ":root_winner_party", ":root_attacker_party"),
              (assign, ":root_defeated_party", ":root_defender_party"),
              (assign, ":collective_casualties", "p_collective_ally"),
            (try_end),

##diplomacy begin
        (try_begin),
          (gt, ":root_defeated_party", -1),
# Recruiter kit begin
 # This little fella just shows a message when a recruiter is defeated.

         (assign, ":minimum_distance", 1000000),
         (try_for_range, ":center", centers_begin, centers_end),
           (store_distance_to_party_from_party, ":dist", ":root_defeated_party", ":center"),
           (try_begin),
             (lt, ":dist", ":minimum_distance"),
             (assign, ":minimum_distance", ":dist"),
             (assign, ":nearest_center", ":center"),
           (try_end),
         (try_end),

        (str_clear, s10),
        (try_begin),
          (gt, ":nearest_center", 0),
          (str_store_party_name, s10, ":nearest_center"),
          (str_store_string, s10, "@ near {s10}"),
        (try_end),

         (try_begin),
            (party_slot_eq, ":root_defeated_party", slot_party_type, dplmc_spt_recruiter),
            (party_get_slot, reg10, ":root_defeated_party", dplmc_slot_party_recruiter_needed_recruits),
            (party_get_slot, ":party_origin", ":root_defeated_party", dplmc_slot_party_recruiter_origin),
            (str_store_party_name_link, s13, ":party_origin"),
            (display_log_message, "@Your recruiter who was commissioned to recruit {reg10} recruits to {s13} has been defeated{s10}!", 0xFF0000),
         (try_end),
# Recruiter kit end

        (try_begin),
          (party_slot_eq,":root_defeated_party", slot_party_type, dplmc_spt_gift_caravan),

          (party_get_slot, ":target_troop", ":root_defeated_party", slot_party_orders_object),
          (party_get_slot, ":target_party", ":root_defeated_party", slot_party_ai_object),
          (try_begin),
            (gt, ":target_troop", 0),
            (str_store_troop_name, s13, ":target_troop"),
          (else_try),
            (str_store_party_name, s13, ":target_party"),
          (end_try),
          (party_get_slot, ":gift", ":root_defeated_party", dplmc_slot_party_mission_diplomacy),
          (str_store_item_name, s12, ":gift"),
          (display_log_message, "@Your caravan sending {s12} to {s13} has been defeated{s10}!", 0xFF0000),
        (try_end),

        (try_begin),
          (party_slot_eq,":root_defeated_party", slot_party_type, spt_messenger),
          (party_get_slot, ":target_party", ":root_defeated_party", slot_party_orders_object),
          (party_stack_get_troop_id, ":party_leader", ":target_party", 0),
          (str_store_troop_name, s13, ":party_leader"),
          (display_log_message, "@Your messenger on the way to {s13} has been defeated{s10}!", 0xFF0000),
        (try_end),

        (try_begin),
          (party_slot_eq,":root_defeated_party", slot_party_type, spt_patrol),
          (party_slot_eq, ":root_defeated_party", dplmc_slot_party_mission_diplomacy, "trp_player"),
          (party_get_slot, ":target_party", ":root_defeated_party", slot_party_ai_object),
          (str_store_party_name, s13, ":target_party"),
          (display_log_message, "@Your soldiers patrolling {s13} have been defeated{s10}!", 0xFF0000),
        (try_end),

        (try_begin),
          (party_slot_eq,":root_defeated_party", slot_party_type, spt_scout),
          (store_faction_of_party, ":party_faction", ":root_defeated_party"),
          (eq, ":party_faction", "$players_kingdom"),
          (party_get_slot, ":target_party", ":root_defeated_party", slot_party_orders_object),
          (str_store_party_name, s13, ":target_party"),
          (display_log_message, "@A scout trying to gather information about {s13} has been slain{s10}!", 0xFF0000),
        (try_end),
      (try_end),
##diplomacy end

            (try_begin),
              (ge, ":root_winner_party", 0),
              (call_script, "script_get_nonempty_party_in_group", ":root_winner_party"),
              (assign, ":nonempty_winner_party", reg0),
              (store_faction_of_party, ":faction_receiving_prisoners", ":nonempty_winner_party"),
              (store_faction_of_party, ":defeated_faction", ":root_defeated_party"),
            (else_try),
              (assign, ":nonempty_winner_party", -1),
            (try_end),

            (try_begin),
              (ge, ":collective_casualties", 0),
              (party_get_num_companion_stacks, ":num_stacks", ":collective_casualties"),
            (else_try),
              (assign, ":num_stacks", 0),
            (try_end),
                                                                         
            (try_for_range, ":troop_iterator", 0, ":num_stacks"),
              (party_stack_get_troop_id, ":cur_troop_id", ":collective_casualties", ":troop_iterator"),
              (troop_is_hero, ":cur_troop_id"),
              
              (try_begin),
                #abort quest if troop loses a battle during rest time
                (check_quest_active, "qst_lend_surgeon"),
                (quest_slot_eq, "qst_lend_surgeon", slot_quest_giver_troop, ":cur_troop_id"),
                (call_script, "script_abort_quest", "qst_lend_surgeon", 0),
              (try_end),
              
              (call_script, "script_remove_troop_from_prison", ":cur_troop_id"),
                              
              (troop_set_slot, ":cur_troop_id", slot_troop_leaded_party, -1),
               
              (store_random_in_range, ":rand", 0, 100),
              (str_store_troop_name_link, s1, ":cur_troop_id"),
              (str_store_faction_name_link, s2, ":faction_receiving_prisoners"),
              (store_troop_faction, ":defeated_troop_faction", ":cur_troop_id"),
              (str_store_faction_name_link, s3, ":defeated_troop_faction"),
              (try_begin),
                (ge, ":rand", hero_escape_after_defeat_chance),
                (party_stack_get_troop_id, ":leader_troop_id", ":nonempty_winner_party", 0),
                ##diplomacy start+ kingdom ladies might lead kingdom parties
                (this_or_next|is_between,":leader_troop_id", kingdom_ladies_begin, kingdom_ladies_end),
                   (is_between, ":leader_troop_id", active_npcs_begin, active_npcs_end),

                (this_or_next|troop_slot_eq, ":leader_troop_id", slot_troop_occupation, slto_kingdom_hero),
                ##diplomacy end+
                (is_between, ":leader_troop_id", active_npcs_begin, active_npcs_end), #disable non-kingdom parties capturing enemy lords
                (party_add_prisoners, ":nonempty_winner_party", ":cur_troop_id", 1),
                (gt, reg0, 0),
                #(troop_set_slot, ":cur_troop_id", slot_troop_is_prisoner, 1),
                (troop_set_slot, ":cur_troop_id", slot_troop_prisoner_of_party, ":nonempty_winner_party"),
                (display_log_message, "str_hero_taken_prisoner"),
				 
                (try_begin),
                  (call_script, "script_cf_prisoner_offered_parole", ":cur_troop_id"),

                  (try_begin),
                    (eq, "$cheat_mode", 1),
                    (display_message, "@{!}DEBUG : Prisoner granted parole"),
                  (try_end),

                  (call_script, "script_troop_change_relation_with_troop", ":leader_troop_id", ":cur_troop_id", 3),
				  (val_add, "$total_battle_enemy_changes", 3),
                (else_try),			 
                  (try_begin),
                    (eq, "$cheat_mode", 1),
                    (display_message, "@{!}DEBUG : Prisoner not offered parole"),
		          (try_end),

		          (call_script, "script_troop_change_relation_with_troop", ":leader_troop_id", ":cur_troop_id", -5),
				  (val_add, "$total_battle_enemy_changes", -5),
		        (try_end),
				 				 				 				 			
				(store_faction_of_party, ":capturer_faction", ":nonempty_winner_party"),
                (call_script, "script_update_troop_location_notes_prisoned", ":cur_troop_id", ":capturer_faction"),
              (else_try),
                (display_message,"@{s1} of {s3} was defeated in battle but managed to escape."),
              (try_end),
              
              (try_begin),
                (store_troop_faction, ":cur_troop_faction", ":cur_troop_id"),
                (is_between, ":cur_troop_faction", kingdoms_begin, kingdoms_end),
                (faction_slot_eq, ":cur_troop_faction", slot_faction_marshall, ":cur_troop_id"),
                (is_between, ":cur_troop_faction", kingdoms_begin, kingdoms_end),
                (assign, "$marshall_defeated_in_battle", ":cur_troop_id"),
                #Marshall is defeated, refresh ai.
                (assign, "$g_recalculate_ais", 1),
              (try_end),
              ##diplomacy begin
              (try_begin),
                (call_script, "script_dplmc_is_affiliated_family_member", ":cur_troop_id"),
                (eq, reg0, 1),
                ##diplomacy start+ skip relationship decay for defeat when the player himself is imprisoned or wounded
					 (eq, "$g_player_is_captive", 0),
                (neg|troop_slot_ge, "trp_player", slot_troop_prisoner_of_party, 1),
                (neg|troop_is_wounded, "trp_player"),
                ##diplomacy end+
					 (assign, ":mitigating_factors", 0),
					 (try_begin),
					    #Being at war with the troop's faction is a mitigating factor, unless the player leads his faction.
						 (store_relation, reg0, "$players_kingdom", ":cur_troop_faction"),
						 (lt, reg0, 0),
						 (neq, "$players_kingdom", "fac_player_supporters_faction"),
						 (neg|faction_slot_eq, "$players_kingdom", slot_faction_leader, "trp_player"),
						 (assign, ":mitigating_factors", 1),
					 (try_end),

                (try_for_range, ":family_member", lords_begin, kingdom_ladies_end),
					   ##diplomacy start+
						#The dead, exiled, and retired don't participate in this
						(neg|troop_slot_ge, ":family_member", slot_troop_occupation, slto_retirement),
						#Members of factions at war with the defeated affiliate's faction don't have
						#any relation loss either: it would be nonsensical for them to be willing to
						#battle him themselves, but become enraged at his defeat.
						(store_troop_faction, ":family_member_faction", ":family_member"),
						(store_relation, reg0, ":family_member_faction", ":cur_troop_faction"),
						(this_or_next|eq, ":family_member_faction", ":cur_troop_faction"),
							(ge, reg0, 0),
                  ##(call_script, "script_troop_get_family_relation_to_troop", ":family_member", "$g_player_affiliated_troop"),
                  (call_script, "script_dplmc_is_affiliated_family_member", ":family_member"),
                  (gt, reg0, 0),
						(assign, reg0, -2),
                        (try_begin),
                        	(eq, ":reduce_campaign_ai", 0),#hard: -1
                        	(assign, reg0, -1),
                        (else_try),
                        	(eq, ":reduce_campaign_ai", 1),#medium: -1 or 0
                        	(store_random_in_range, reg0, -1, 1),
                        (else_try),
                        	(eq, ":reduce_campaign_ai", 2),#easy: 0
                        	(assign, reg0, 0),
                        (try_end),
						(val_add, reg0, ":mitigating_factors"),
						(lt, reg0, 0),
                  (call_script, "script_change_player_relation_with_troop", ":family_member", reg0),
                  ##diplomacy end+
                (try_end),
              (try_end),
              ##diplomacy end
            (try_end),
			 
             (try_begin),
               (ge, ":collective_casualties", 0),
               (party_get_num_prisoner_stacks, ":num_stacks", ":collective_casualties"),
             (else_try),
               (assign, ":num_stacks", 0),
             (try_end),
             (try_for_range, ":troop_iterator", 0, ":num_stacks"),
               (party_prisoner_stack_get_troop_id, ":cur_troop_id", ":collective_casualties", ":troop_iterator"),
               (troop_is_hero, ":cur_troop_id"),
               (call_script, "script_remove_troop_from_prison", ":cur_troop_id"),
               (store_troop_faction, ":cur_troop_faction", ":cur_troop_id"),
               (str_store_troop_name_link, s1, ":cur_troop_id"),
               (str_store_faction_name_link, s2, ":faction_receiving_prisoners"),
               (str_store_faction_name_link, s3, ":cur_troop_faction"),
               (display_log_message,"str_hero_freed"),
             (try_end),

             (try_begin),
               (ge, ":collective_casualties", 0),
               (party_clear, "p_temp_party"),
               (assign, "$g_move_heroes", 0), #heroes are already processed above. Skip them here.
               (call_script, "script_party_add_party_prisoners", "p_temp_party", ":collective_casualties"),
               (call_script, "script_party_prisoners_add_party_companions", "p_temp_party", ":collective_casualties"),
               (distribute_party_among_party_group, "p_temp_party", ":root_winner_party"),
			   
               (call_script, "script_battle_political_consequences", ":root_defeated_party", ":root_winner_party"),
			
               (call_script, "script_clear_party_group", ":root_defeated_party"),
             (try_end),
             (assign, ":trigger_result", 1), #End battle!

             #Center captured
             (try_begin),
               (ge, ":collective_casualties", 0),
               (party_get_slot, ":cur_party_type", ":root_defeated_party", slot_party_type),
               (this_or_next|eq, ":cur_party_type", spt_town),
               (eq, ":cur_party_type", spt_castle),

               (assign, "$g_recalculate_ais", 1),

               (store_faction_of_party, ":winner_faction", ":root_winner_party"),
               (store_faction_of_party, ":defeated_faction", ":root_defeated_party"),

               (str_store_party_name, s1, ":root_defeated_party"),
               (str_store_faction_name, s2, ":winner_faction"),
               (str_store_faction_name, s3, ":defeated_faction"),
               (display_log_message, "str_center_captured"),
			
			   (store_current_hours, ":hours"),
			   (faction_set_slot, ":winner_faction", slot_faction_ai_last_decisive_event, ":hours"),
			
               (try_begin),
                 (eq, "$g_encountered_party", ":root_defeated_party"),
                 (call_script, "script_add_log_entry", logent_player_participated_in_siege, "trp_player",  "$g_encountered_party", 0, "$g_encountered_party_faction"),
               (try_end),

               (try_begin),
                 (party_get_num_companion_stacks, ":num_stacks", ":root_winner_party"),
                 (gt, ":num_stacks", 0),
                 (party_stack_get_troop_id, ":leader_troop_no", ":root_winner_party", 0),
		##diplomacy start+ support for promoted kingdom ladies
                 (is_between, ":leader_troop_no", heroes_begin, heroes_end),#<- dplmc+ added
                 (this_or_next|troop_slot_eq, ":leader_troop_no", slot_troop_occupation, slto_kingdom_hero),#<- dplmc+ addded
                     (is_between, ":leader_troop_no", active_npcs_begin, active_npcs_end),
		##diplomacy end+
                 (party_set_slot, ":root_defeated_party", slot_center_last_taken_by_troop, ":leader_troop_no"),
               (else_try),
                 (party_set_slot, ":root_defeated_party", slot_center_last_taken_by_troop, -1),
               (try_end),

               (call_script, "script_lift_siege", ":root_defeated_party", 0),
			   (store_faction_of_party, ":fortress_faction", ":root_defeated_party"),			   
			   (try_begin),
			     (is_between, ":root_defeated_party", towns_begin, towns_end),
			     (assign, ":damage", 40),
			   (else_try),
			     (assign, ":damage", 20),
			   (try_end),
			   (call_script, "script_faction_inflict_war_damage_on_faction", ":winner_faction", ":fortress_faction", ":damage"),
			   
			   #gekokujo 3.0 imahama-nagahama rename start
			   #town 26 gets renamed to nagahama when oda take it
			   #it gets renamed back to imahama if asakura retake it
			   #everyone else keeps whatever name they took it over with
			   (try_begin),
			     (eq, ":root_defeated_party", "p_town_26"),
				 (try_begin),
				   (eq, ":winner_faction", "fac_kingdom_3"),
				   (party_set_name, "p_town_26", "@Nagahama"),
				 (else_try),
				   (eq, ":winner_faction", "fac_kingdom_11"),
				   (party_set_name, "p_town_26", "@Imahama"),
				 (try_end),
			   (try_end),
			   #gekokujo 3.0 imahama-nagahama rename end
			   
               (call_script, "script_give_center_to_faction", ":root_defeated_party", ":winner_faction"),
               (try_begin),
			     ##diplomacy start+ Handle player is co-ruler of faction
			     (assign, ":is_defeated_faction_coruler", 0),
            	 (try_begin),
            		##zerilius changes begin
            		(eq, ":defeated_faction", "$players_kingdom"),
            		# (eq, ":is_defeated_faction_coruler", "$players_kingdom"),
            		##zerilius changes end
            		(is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
            		(call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", "$players_kingdom"),
            		(ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
            		(assign, ":is_defeated_faction_coruler", 1),
            	 (try_end),
				 (this_or_next|eq, ":is_defeated_faction_coruler", 1),
	  		     ##diplomacy end+
                 (eq, ":defeated_faction", "fac_player_supporters_faction"),
                 (call_script, "script_add_notification_menu", "mnu_notification_center_lost", ":root_defeated_party", ":winner_faction"),
               (try_end),
               
               (party_get_num_attached_parties, ":num_attached_parties",  ":root_attacker_party"),
                 (try_for_range, ":attached_party_rank", 0, ":num_attached_parties"),
                 (party_get_attached_party_with_rank, ":attached_party", ":root_attacker_party", ":attached_party_rank"),
                                                                                                       
                 (party_get_num_companion_stacks, ":num_stacks", ":attached_party"),                 
                 (assign, ":total_size", 0),
                 (try_for_range, ":i_stack", 0, ":num_stacks"),
                   (party_stack_get_size, ":stack_size", ":attached_party", ":i_stack"),
                   (val_add, ":total_size", ":stack_size"),
                 (try_end),  
                 
                 (try_begin),
                   (ge, ":total_size", 10),
                   
                   (assign, ":stacks_added", 0),
                   (assign, ":last_random_stack", -1),
                   
                   (assign, ":end_condition", 10),
                   (try_for_range, ":unused", 0, ":end_condition"),
                     (store_random_in_range, ":random_stack", 1, ":num_stacks"),
                     (party_stack_get_troop_id, ":random_stack_troop", ":attached_party", ":random_stack"),
                     (party_stack_get_size, ":stack_size", ":attached_party", ":random_stack"),
                     (ge, ":stack_size", 4),
                     (neq, ":random_stack", ":last_random_stack"),
                   
                     (store_mul, ":total_size_mul_2", ":total_size", 2),
                     (assign, ":percentage", ":total_size_mul_2"),
                     (val_min, ":percentage", 100),                   
                   
                     (val_mul, ":stack_size", ":percentage"),
                     (val_div, ":stack_size", 100),
                   
                     (party_stack_get_troop_id, ":party_leader", ":attached_party", 0),

                     (try_begin),
                       ##diplomacy start+ add lady personality
                       (this_or_next|troop_slot_eq, ":party_leader", slot_lord_reputation_type, lrep_conventional),
                       (this_or_next|troop_slot_eq, ":party_leader", slot_lord_reputation_type, lrep_otherworldly),
                       (this_or_next|troop_slot_eq, ":party_leader", slot_lord_reputation_type, lrep_adventurous),
                       ##diplomacy end+
                       (this_or_next|troop_slot_eq, ":party_leader", slot_lord_reputation_type, lrep_goodnatured),
                       (this_or_next|troop_slot_eq, ":party_leader", slot_lord_reputation_type, lrep_upstanding),
                       (troop_slot_eq, ":party_leader", slot_lord_reputation_type, lrep_martial),
                       (assign, reg2, 0),
                       (store_random_in_range, ":random_percentage", 40, 50), #average 45%
                     (else_try),  
                       ##diplomacy start+ add lady personality
                       (this_or_next|troop_slot_eq, ":party_leader", slot_lord_reputation_type, lrep_ambitious),
                       ##diplmoacy end+
                       (this_or_next|troop_slot_eq, ":party_leader", slot_lord_reputation_type, lrep_quarrelsome),
                       (troop_slot_eq, ":party_leader", slot_lord_reputation_type, lrep_cunning),
                       (assign, reg2, 1),
                       (store_random_in_range, ":random_percentage", 30, 40), #average 35%
                     (else_try),  
                       (this_or_next|troop_slot_eq, ":party_leader", slot_lord_reputation_type, lrep_selfrighteous),
                       (this_or_next|troop_slot_eq, ":party_leader", slot_lord_reputation_type, lrep_roguish),
                       (troop_slot_eq, ":party_leader", slot_lord_reputation_type, lrep_debauched),
                       (assign, reg2, 2),
                       (store_random_in_range, ":random_percentage", 20, 30), #average 25%
                     (else_try),  
                       ##diplomacy start+ add lady personality
                       (this_or_next|troop_slot_eq, ":party_leader", slot_lord_reputation_type, lrep_moralist),
                       ##diplomacy end+
                       (this_or_next|troop_slot_eq, ":party_leader", slot_lord_reputation_type, lrep_benefactor),
                       (troop_slot_eq, ":party_leader", slot_lord_reputation_type, lrep_custodian),
                       (assign, reg2, 3),
                       (store_random_in_range, ":random_percentage", 50, 60), #average 55%
                     (try_end),                   
                   
                     (val_min, ":random_percentage", 100),                   
                     (val_mul, ":stack_size", ":random_percentage"),
                     (val_div, ":stack_size", 100),
                                                    
                     (party_add_members, ":root_defender_party", ":random_stack_troop", ":stack_size"),
                     (party_remove_members, ":attached_party", ":random_stack_troop", ":stack_size"),
                     
                     (val_add, ":stacks_added", 1),
                     (assign, ":last_random_stack", ":random_stack"),
                     
                     (try_begin),
                       #if troops from three different stack is already added then break
                       (eq, ":stacks_added", 3),
                       (assign, ":end_condition", 0),
                     (try_end),
                   (try_end),  
                 (try_end),  
               (try_end),
               
               #Reduce prosperity of the center by 5
			   (try_begin),
			     (neg|is_between, ":root_defeated_party", castles_begin, castles_end),
			     (call_script, "script_change_center_prosperity", ":root_defeated_party", -5),
			     (val_add, "$newglob_total_prosperity_from_townloot", -5),
			   (try_end),
               (call_script, "script_order_best_besieger_party_to_guard_center", ":root_defeated_party", ":winner_faction"),
               (call_script, "script_cf_reinforce_party", ":root_defeated_party"),
               (call_script, "script_cf_reinforce_party", ":root_defeated_party"),			   
             (try_end),
           (try_end),

           #ADD XP
           (try_begin),
             (party_slot_eq, ":root_attacker_party", slot_party_type, spt_kingdom_hero_party),
                          
             (assign, ":xp_gained_attacker", 200),
             (game_get_reduce_campaign_ai, ":reduce_campaign_ai"),
             (store_faction_of_party, ":root_attacker_party_faction", ":root_attacker_party"),
             (try_begin),
               (this_or_next|eq, ":root_attacker_party", "p_main_party"),
               (this_or_next|eq, ":root_attacker_party_faction", "fac_player_supporters_faction"),
               (eq, ":root_attacker_party_faction", "$players_kingdom"),               
               #same
             (else_try),
               (eq, ":reduce_campaign_ai", 0), #hard (1.5x)
               (val_mul, ":xp_gained_attacker", 3),
               (val_div, ":xp_gained_attacker", 2),
             (else_try),
               (eq, ":reduce_campaign_ai", 1), #moderate (1.0x)
               #same
             (else_try),                        
               (eq, ":reduce_campaign_ai", 2), #easy (0.5x)
               (val_div, ":xp_gained_attacker", 2),
             (try_end),           
             
             (gt, ":new_attacker_strength", 0),             
             (call_script, "script_upgrade_hero_party", ":root_attacker_party", ":xp_gained_attacker"),
           (try_end),
           (try_begin),
             (party_slot_eq, ":root_defender_party", slot_party_type, spt_kingdom_hero_party),
                          
             (assign, ":xp_gained_defender", 200),
             (store_faction_of_party, ":root_defender_party_faction", ":root_defender_party"),             
             (game_get_reduce_campaign_ai, ":reduce_campaign_ai"),
             (try_begin),
               (this_or_next|eq, ":root_defender_party", "p_main_party"),
               (this_or_next|eq, ":root_defender_party_faction", "fac_player_supporters_faction"),
               (eq, ":root_defender_party_faction", "$players_kingdom"),               
               #same
             (else_try),
               (eq, ":reduce_campaign_ai", 0), #hard (1.5x)
               (val_mul, ":xp_gained_defender", 3),
               (val_div, ":xp_gained_defender", 2),
             (else_try),
               (eq, ":reduce_campaign_ai", 1), #moderate (1.0x)
               #same
             (else_try),         
               (eq, ":reduce_campaign_ai", 2), #easy (0.5x)
               (val_div, ":xp_gained_defender", 2),
             (try_end),           

             (gt, ":new_defender_strength", 0),
             (call_script, "script_upgrade_hero_party", ":root_defender_party", ":xp_gained_defender"),
           (try_end),

           (try_begin),         
             #ozan - do not randomly end battles aganist towns or castles.
             (neg|party_slot_eq, ":root_defender_party", slot_party_type, spt_castle), #added by ozan
             (neg|party_slot_eq, ":root_defender_party", slot_party_type, spt_town),   #added by ozan        
             #end ozan
                          
             (party_get_slot, ":attacker_root_strength", ":root_attacker_party", slot_party_cached_strength),
             (party_get_slot, ":attacker_nearby_friend_strength", ":root_attacker_party", slot_party_nearby_friend_strength),
             (party_get_slot, ":strength_of_attacker_followers", ":root_attacker_party", slot_party_follower_strength),
             (store_add, ":total_attacker_strength", ":attacker_root_strength", ":attacker_nearby_friend_strength"),
             (val_add, ":total_attacker_strength", ":strength_of_attacker_followers"),

             (party_get_slot, ":defender_root_strength", ":root_defender_party", slot_party_cached_strength),
             (party_get_slot, ":defender_nearby_friend_strength", ":root_defender_party", slot_party_nearby_friend_strength),
             (party_get_slot, ":strength_of_defender_followers", ":root_defender_party", slot_party_follower_strength),
             (store_add, ":total_defender_strength", ":defender_root_strength", ":defender_nearby_friend_strength"),
             (val_add, ":total_attacker_strength", ":strength_of_defender_followers"),

             #Players can make save loads and change history because these random values are not determined from random_slots of troops
             (store_random_in_range, ":random_num", 0, 100),
                          
             (try_begin),
               (lt, ":random_num", 10),
               (assign, ":trigger_result", 1), #End battle!
             (try_end),
           (else_try),
             (party_get_slot, ":attacker_root_strength", ":root_attacker_party", slot_party_cached_strength),
             (party_get_slot, ":attacker_nearby_friend_strength", ":root_attacker_party", slot_party_nearby_friend_strength),
             (party_get_slot, ":strength_of_followers", ":root_attacker_party", slot_party_follower_strength),
             (store_add, ":total_attacker_strength", ":attacker_root_strength", ":attacker_nearby_friend_strength"),
             (val_add, ":total_attacker_strength", ":strength_of_followers"),

             (party_get_slot, ":defender_root_strength", ":root_defender_party", slot_party_cached_strength),
             (party_get_slot, ":defender_nearby_friend_strength", ":root_defender_party", slot_party_nearby_friend_strength),
             (store_add, ":total_defender_strength", ":defender_root_strength", ":defender_nearby_friend_strength"),

             (val_mul, ":total_defender_strength", 13), #multiply defender strength with 1.3
             (val_div, ":total_defender_strength", 10),

             (gt, ":total_defender_strength", ":total_attacker_strength"),
             (gt, ":total_defender_strength", 3),

             #Players can make save loads and change history because these random values are not determined from random_slots of troops
             (store_random_in_range, ":random_num", 0, 100),

             (try_begin),
               (lt, ":random_num", 15), #15% is a bit higher than 10% (which is open area escape probability)
               (assign, ":trigger_result", 1), #End battle!
                                             
               (assign, "$g_recalculate_ais", 1), #added new
                              
               (try_begin),
                 (eq, "$cheat_mode", 1),
                 (display_message, "@{!}DEBUG : Siege attackers are running away"),
               (try_end),
             (try_end),      
           (try_end),
         (try_end),  
       (try_end),
       (set_trigger_result, ":trigger_result"),
  ]),
  #script_game_event_battle_end:
  # This script is called whenever the game ends the battle between two parties on the map.
  # INPUT:
  # param1: Defender Party
  # param2: Attacker Party
  ("game_event_battle_end",
    [
##       (store_script_param_1, ":root_defender_party"),
##       (store_script_param_2, ":root_attacker_party"),
        
      #Fixing deleted heroes
      ##diplomacy start+ kingdom ladies may also potentially lead parties
      (try_for_range, ":cur_troop", heroes_begin, heroes_end),#<- changed active_npcs to heroes
      #diplomacy end+
		(troop_slot_eq, ":cur_troop", slot_troop_occupation, slto_kingdom_hero),
        (troop_get_slot, ":cur_party", ":cur_troop", slot_troop_leaded_party),
        (troop_get_slot, ":cur_prisoner_of_party", ":cur_troop", slot_troop_prisoner_of_party),
        (try_begin),
          (ge, ":cur_party", 0),
          (assign, ":continue", 0),
          (try_begin),
            (neg|party_is_active, ":cur_party"),
            (assign, ":continue", 1),
          (else_try),
            (party_count_companions_of_type, ":amount", ":cur_party", ":cur_troop"),
            (le, ":amount", 0),
            (assign, ":continue", 1),
          (try_end),
          (eq, ":continue", 1),
          (try_begin),
            (eq, "$cheat_mode", 1),
            (str_store_troop_name, s1, ":cur_troop"),
            (display_message, "@{!}DEBUG: {s1} no longer leads a party."),
          (try_end),
         
          (troop_set_slot, ":cur_troop", slot_troop_leaded_party, -1),
          #(str_store_troop_name, s5, ":cur_troop"),
          #(display_message, "@{!}DEBUG : {s5}'s troop_leaded_party set to -1"),
        (try_end),
        (try_begin),
          (ge, ":cur_prisoner_of_party", 0),
          (assign, ":continue", 0),
          (try_begin),
            (neg|party_is_active, ":cur_prisoner_of_party"),
            (assign, ":continue", 1),
          (else_try),
            (party_count_prisoners_of_type, ":amount", ":cur_prisoner_of_party", ":cur_troop"),
            (le, ":amount", 0),
            (assign, ":continue", 1),
          (try_end),
          (eq, ":continue", 1),
          (try_begin),
            (eq, "$cheat_mode", 1),
            (str_store_troop_name, s1, ":cur_troop"),
            (display_message, "@{!}DEBUG: {s1} is no longer a prisoner."),
          (try_end),
          (call_script, "script_remove_troop_from_prison", ":cur_troop"),
          #searching player
          (try_begin),
            (party_count_prisoners_of_type, ":amount", "p_main_party", ":cur_troop"),
            (gt, ":amount", 0),
            (troop_set_slot, ":cur_troop", slot_troop_prisoner_of_party, "p_main_party"),
            (assign, ":continue", 0),
            (try_begin),
              (eq, "$cheat_mode", 1),
              (str_store_troop_name, s1, ":cur_troop"),
              (display_message, "@{!}DEBUG: {s1} is now a prisoner of player."),                         
            (try_end),
          (try_end),
          (eq, ":continue", 1),
		  ##diplomacy start+
		  #Add increased information for affiliates.
		  (call_script, "script_dplmc_store_troop_is_eligible_for_affiliate_messages", ":cur_troop"),
		  (assign, ":is_affiliated", reg0),
		  ##diplomacy end+
          #searching kingdom heroes
	  ##diplomacy start+ support for promoted kingdom ladies
          (try_for_range, ":cur_troop_2", heroes_begin, heroes_end),#<-- changed active_npcs to heroes
          ##diplomacy end+
			(troop_slot_eq, ":cur_troop_2", slot_troop_occupation, slto_kingdom_hero),
			(eq, ":continue", 1),
            (troop_get_slot, ":cur_prisoner_of_party_2", ":cur_troop_2", slot_troop_leaded_party),
            (party_is_active, ":cur_prisoner_of_party_2"),
            (party_count_prisoners_of_type, ":amount", ":cur_prisoner_of_party_2", ":cur_troop"),
            (gt, ":amount", 0),
            (troop_set_slot, ":cur_troop", slot_troop_prisoner_of_party, ":cur_prisoner_of_party_2"),
            (assign, ":continue", 0),
            (try_begin),
			##diplomacy start+ Show for affiliates
			  (ge, ":is_affiliated", 1),
			  (str_store_troop_name, s1, ":cur_troop"),
			  (str_store_party_name, s2, ":cur_prisoner_of_party_2"),
			  (display_message, "@{s1} is now a prisoner of {s2}."),
			(else_try),
			##diplomacy end+
              (eq, "$cheat_mode", 1),
              (str_store_troop_name, s1, ":cur_troop"),
              (str_store_party_name, s2, ":cur_prisoner_of_party_2"),
              (display_message, "@{!}DEBUG: {s1} is now a prisoner of {s2}."),
            (try_end),
          (try_end),
          #searching walled centers
          (try_for_range, ":cur_prisoner_of_party_2", walled_centers_begin, walled_centers_end),
            (eq, ":continue", 1),
            (party_count_prisoners_of_type, ":amount", ":cur_prisoner_of_party_2", ":cur_troop"),
            (gt, ":amount", 0),
            (troop_set_slot, ":cur_troop", slot_troop_prisoner_of_party, ":cur_prisoner_of_party_2"),
            (assign, ":continue", 0),
            (try_begin),
			##diplomacy start+ Show for affiliates
			  (ge, ":is_affiliated", 1),
			  (str_store_troop_name, s1, ":cur_troop"),
			  (str_store_party_name, s2, ":cur_prisoner_of_party_2"),
			  (display_message, "@{s1} is now a prisoner of {s2}."),
			(else_try),
			##diplomacy end+
              (eq, "$cheat_mode", 1),
              (str_store_troop_name, s1, ":cur_troop"),
              (str_store_party_name, s2, ":cur_prisoner_of_party_2"),
              (display_message, "@{!}DEBUG: {s1} is now a prisoner of {s2}."),
            (try_end),
          (try_end),
        (try_end),
      (try_end),
  ]),
  #script_game_get_item_buy_price_factor:
  # This script is called from the game engine for calculating the buying price of any item.
  # INPUT:
  # param1: item_kind_id
  # OUTPUT:
  # trigger_result and reg0 = price_factor
  ("game_get_item_buy_price_factor",
    [
      (store_script_param_1, ":item_kind_id"),
      (assign, ":price_factor", 100),

      (call_script, "script_get_trade_penalty", ":item_kind_id"),
      (assign, ":trade_penalty", reg0),

      (try_begin),
        (is_between, "$g_encountered_party", centers_begin, centers_end),
        (is_between, ":item_kind_id", trade_goods_begin, trade_goods_end),
        (store_sub, ":item_slot_no", ":item_kind_id", trade_goods_begin),
        (val_add, ":item_slot_no", slot_town_trade_good_prices_begin),
        (party_get_slot, ":price_factor", "$g_encountered_party", ":item_slot_no"),
		
		#new
		#(try_begin),
		#	(is_between, "$g_encountered_party", villages_begin, villages_end),
		#	(party_get_slot, ":market_town", "$g_encountered_party", slot_village_market_town),
		#	(party_get_slot, ":price_in_market_town", ":market_town", ":item_slot_no"),
		#	(val_max, ":price_factor", ":price_in_market_town"),
		#(try_end),
		
		#For villages, the good will be sold no cheaper than in the market town
		#This represents the absence of a permanent market -- ie, the peasants retain goods to sell on their journeys to town, and are not about to do giveaway deals with passing adventurers
				
        (val_mul, ":price_factor", 100), #normalize price factor to range 0..100
        (val_div, ":price_factor", average_price_factor),
      (try_end),
      
      (store_add, ":penalty_factor", 100, ":trade_penalty"),
      
      (val_mul, ":price_factor", ":penalty_factor"),
      (val_div, ":price_factor", 100),

      (assign, reg0, ":price_factor"),
      (set_trigger_result, reg0),
  ]),
  #script_game_get_item_sell_price_factor:
  # This script is called from the game engine for calculating the selling price of any item.
  # INPUT:
  # param1: item_kind_id
  # OUTPUT:
  # trigger_result and reg0 = price_factor
  ("game_get_item_sell_price_factor",
    [
      (store_script_param_1, ":item_kind_id"),
      (assign, ":price_factor", 100),

      (call_script, "script_get_trade_penalty", ":item_kind_id"),
      (assign, ":trade_penalty", reg0),

      (try_begin),
        (is_between, "$g_encountered_party", centers_begin, centers_end),
        (is_between, ":item_kind_id", trade_goods_begin, trade_goods_end),
        (store_sub, ":item_slot_no", ":item_kind_id", trade_goods_begin),
        (val_add, ":item_slot_no", slot_town_trade_good_prices_begin),
        (party_get_slot, ":price_factor", "$g_encountered_party", ":item_slot_no"),
        (val_mul, ":price_factor", 100),#normalize price factor to range 0..100
        (val_div, ":price_factor", average_price_factor),
      (else_try),
        #increase trade penalty while selling weapons, armor, and horses
        (val_mul, ":trade_penalty", 4),
      (try_end),

	  ##diplomacy start+
	  #If economic changes are enabled, use a lesser trade penalty when selling
 	  #to the correct merchant in town.
	  (try_begin),
		(ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_LOW),
		(is_between, "$g_encountered_party", towns_begin, towns_end),
		(gt, "$g_talk_troop", "trp_player"),
		(try_begin),
			#Selling weapons to the weaponsmith
			(party_slot_eq, "$g_encountered_party", slot_town_weaponsmith, "$g_talk_troop"),
			(this_or_next|is_between, ":item_kind_id", weapons_begin, weapons_end),
			(this_or_next|is_between, ":item_kind_id", shields_begin, shields_end),
				(is_between, ":item_kind_id", ranged_weapons_begin, ranged_weapons_end),
			(val_mul, ":trade_penalty", 9),
			(val_div, ":trade_penalty", 10),
		(else_try),
			#Selling armor to the armorer
			(party_slot_eq, "$g_encountered_party", slot_town_armorer, "$g_talk_troop"),
			(is_between, ":item_kind_id", armors_begin, armors_end),
			(val_mul, ":trade_penalty", 9),
			(val_div, ":trade_penalty", 10),
		(else_try),
			#Selling horses to the horse merchant
			(party_slot_eq, "$g_encountered_party", slot_town_horse_merchant, "$g_talk_troop"),
			(is_between, ":item_kind_id", horses_begin, horses_end),
			(val_mul, ":trade_penalty", 9),
			(val_div, ":trade_penalty", 10),
		(try_end),
	  (try_end),

	  #If economic changes are enabled, increase food prices in a town under siege.
	  (try_begin),
		(ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_LOW),
		(is_between, "$g_encountered_party", centers_begin, centers_end),
		#Check selling food
		(is_between, ":item_kind_id", food_begin, food_end),
		#Check at a town or castle under siege for at least 48 hours
		(this_or_next|party_slot_eq, "$g_encountered_party", slot_party_type, spt_town),
			(party_slot_eq, "$g_encountered_party", slot_party_type, spt_castle),
		(party_slot_eq, "$g_encountered_party", slot_village_state, svs_under_siege),

		(party_slot_ge, "$g_encountered_party", slot_center_is_besieged_by, 1),
		(party_get_slot, ":siege_start", "$g_encountered_party", slot_center_siege_begin_hours),
		(store_current_hours, ":cur_hours"),
		(store_sub, reg0, ":cur_hours", ":siege_start"),
		(ge, reg0, 48),
		#Check last caravan or village trading party arrival (default to eight weeks ago)
		(store_sub, ":last_arrival", ":cur_hours", 8 * 7 * 24),
		(val_min, ":last_arrival", ":siege_start"),
		(try_for_range, ":village_no", villages_begin, villages_end),
			(party_slot_eq, ":village_no", slot_village_market_town, "$g_encountered_party"),
			(party_get_slot, reg0, ":village_no", dplmc_slot_village_trade_last_arrived_to_market),
			(val_min, reg0, ":cur_hours"),
			(val_max, ":last_arrival", reg0),
		(try_end),
		(try_for_range, ":slot_no", dplmc_slot_town_trade_route_last_arrivals_begin, dplmc_slot_town_trade_route_last_arrivals_end),
			#Not all of these slots correspond to towns, but that doesn't
			#matter since their arrival times won't update after the start
			#of the game.
			(party_get_slot, reg0, "$g_encountered_party", ":slot_no"),
			(val_min, reg0, ":cur_hours"),
			(val_max, ":last_arrival", reg0),
		(try_end),
		##Increase food prices by 10% for every 3 days the siege has been going on,
		#or a minimum of 5%.
		#TODO: Make use of the last caravan arrival time.
		(store_sub, ":hours_since", ":cur_hours", ":siege_start"),
		(store_mul, ":siege_percent", ":hours_since", 10),
		(val_add, ":siege_percent", (3 * 24) // 2),
		(val_div, ":siege_percent", 3 * 24),
		(val_max, ":siege_percent", 5),
		(val_add, ":siege_percent", 100),
		(val_mul, ":price_factor", ":siege_percent"),
		(val_add, ":price_factor", 50),
		(val_div, ":price_factor", 100),
	  (try_end),
	  ##diplomacy end+
            
      (store_add, ":penalty_divisor", 100, ":trade_penalty"),
      
      (val_mul, ":price_factor", 100),
	  ##diplomacy start+
	  (try_begin),
		(gt, ":penalty_divisor", 0),
		(store_div, reg0, ":penalty_divisor", 2),
		(val_add, ":price_factor", reg0),#round correctly
	  (try_end),
	  ##diplomacy end+
      (val_div, ":price_factor", ":penalty_divisor"),
      
      (assign, reg0, ":price_factor"),
      (set_trigger_result, reg0),
  ]),
  #script_game_event_buy_item:
  # This script is called from the game engine when player buys an item.
  # INPUT:
  # param1: item_kind_id
  ("game_event_buy_item",
    [
      (store_script_param_1, ":item_kind_id"),
      (store_script_param_2, ":reclaim_mode"),
      (try_begin),
        (is_between, ":item_kind_id", trade_goods_begin, trade_goods_end),
        (store_sub, ":item_slot_no", ":item_kind_id", trade_goods_begin),
        (val_add, ":item_slot_no", slot_town_trade_good_prices_begin),
        (party_get_slot, ":multiplier", "$g_encountered_party", ":item_slot_no"),
        (try_begin),
          (eq, ":reclaim_mode", 0),
          (val_add, ":multiplier", 20),
        (else_try),
          (val_add, ":multiplier", 30),
        (try_end),

		(store_item_value, ":item_value", ":item_kind_id"),
		(try_begin),
		  (ge, ":item_value", 100),
		  (store_sub, ":item_value_sub_100", ":item_value", 100),
		  (store_div, ":item_value_sub_100_div_8", ":item_value_sub_100", 8),
		  (val_add, ":multiplier", ":item_value_sub_100_div_8"),
		(try_end),

        (val_min, ":multiplier", maximum_price_factor),
        
		(party_set_slot, "$g_encountered_party", ":item_slot_no", ":multiplier"),
      (try_end),
  ]),
  #script_game_event_sell_item:
  # This script is called from the game engine when player sells an item.
  # INPUT:
  # param1: item_kind_id
  ("game_event_sell_item",
    [
      (store_script_param_1, ":item_kind_id"),
      (store_script_param_2, ":return_mode"),
      (try_begin),
        (is_between, ":item_kind_id", trade_goods_begin, trade_goods_end),
        (store_sub, ":item_slot_no", ":item_kind_id", trade_goods_begin),
        (val_add, ":item_slot_no", slot_town_trade_good_prices_begin),
        (party_get_slot, ":multiplier", "$g_encountered_party", ":item_slot_no"),
        (try_begin),
          (eq, ":return_mode", 0),
          (val_sub, ":multiplier", 30),
        (else_try),
          (val_sub, ":multiplier", 20),
        (try_end),

		(store_item_value, ":item_value", ":item_kind_id"),
		(try_begin),
		  (ge, ":item_value", 100),
		  (store_sub, ":item_value_sub_100", ":item_value", 100),
		  (store_div, ":item_value_sub_100_div_8", ":item_value_sub_100", 8),
		  (val_sub, ":multiplier", ":item_value_sub_100_div_8"),
		(try_end),

        (val_max, ":multiplier", minimum_price_factor),
        
		(party_set_slot, "$g_encountered_party", ":item_slot_no", ":multiplier"),
      (try_end),
  ]),
  ("game_get_troop_wage",
    [
      (store_script_param_1, ":troop_id"),
      (store_script_param_2, ":unused"), #party id
      
      (assign,":wage", 0),
      (try_begin),
        (this_or_next|eq, ":troop_id", "trp_player"),
        (eq, ":troop_id", "trp_kidnapped_girl"),
      (else_try),
        (is_between, ":troop_id", pretenders_begin, pretenders_end),
      ##diplomacy start+
      (else_try),
      #Temporarily joined lords and ladies don't require wages.
        (is_between, ":troop_id", heroes_begin, heroes_end),
        (this_or_next|troop_slot_eq, ":troop_id", slot_troop_playerparty_history,dplmc_pp_history_lord_rejoined),
        (this_or_next|troop_slot_eq, ":troop_id", slot_troop_occupation, slto_kingdom_hero),
           (troop_slot_eq, ":troop_id",slot_troop_occupation, slto_kingdom_lady),
      ##diplomacy end+
      (else_try),
        (store_character_level, ":troop_level", ":troop_id"),
        (assign, ":wage", ":troop_level"),
        (val_add, ":wage", 3),
        (val_mul, ":wage", ":wage"),
        (val_div, ":wage", 25),
      (try_end),

      (try_begin), #mounted troops cost 65% more than the normal cost
		#gekokujo 3.0 microfactions! include fort companions start
        #(neg|is_between, ":troop_id", companions_begin, companions_end),
        (neg|is_between, ":troop_id", companions_begin, fort_companions_end),
		#gekokujo 3.0 microfactions! include fort companions end
        (troop_is_mounted, ":troop_id"),
        (val_mul, ":wage", 5),
        (val_div, ":wage", 3),
      (try_end),

      (try_begin), #mercenaries cost %50 more than the normal cost
        (is_between, ":troop_id", mercenary_troops_begin, mercenary_troops_end),
        (val_mul, ":wage", 3),
        (val_div, ":wage", 2),
      (try_end),
	  
      (try_begin), #gekokujo 3.0 samurai troops cost 33% more than the normal cost
        (is_between, ":troop_id", samurai_troops_begin, samurai_troops_end),
        (val_mul, ":wage", 4),
        (val_div, ":wage", 3),
      (try_end),

      (try_begin),
		#gekokujo 3.0 microfactions! include fort companions start
        #(is_between, ":troop_id", companions_begin, companions_end),
        (is_between, ":troop_id", companions_begin, fort_companions_end),
		#gekokujo 3.0 microfactions! include fort companions end
        (val_mul, ":wage", 2),
      (try_end),
      
      (store_skill_level, ":leadership_level", "skl_leadership", "trp_player"),
      (store_mul, ":leadership_bonus", 5, ":leadership_level"),
      (store_sub, ":leadership_factor", 100, ":leadership_bonus"), 
      (val_mul, ":wage", ":leadership_factor"),  #wage = wage * (100 - 5*leadership)/100
      (val_div, ":wage", 100),

      (try_begin),
        (neq, ":troop_id", "trp_player"),
        (neq, ":troop_id", "trp_kidnapped_girl"),
        (neg|is_between, ":troop_id", pretenders_begin, pretenders_end),
	##diplomacy start+ For temporarily rejoined lords, and temporarily joined ladies
        (neg|troop_slot_eq, ":troop_id", slot_troop_playerparty_history,dplmc_pp_history_lord_rejoined),
        (neg|troop_slot_eq, ":troop_id", slot_troop_occupation, slto_kingdom_hero),
        (neg|is_between, ":troop_id", kingdom_ladies_begin, kingdom_ladies_end),
	##diplomacy end+
        (val_max, ":wage", 1),
      (try_end),
       
      (assign, reg0, ":wage"),
      (set_trigger_result, reg0),
  ]),
  ("game_get_total_wage",
    [
      (assign, ":total_wage", 0),
      (party_get_num_companion_stacks, ":num_stacks", "p_main_party"),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop", "p_main_party", ":i_stack"),
        (party_stack_get_size, ":stack_size", "p_main_party", ":i_stack"),
        (call_script, "script_game_get_troop_wage", ":stack_troop", 0),
        (val_mul, reg0, ":stack_size"),
        (val_add, ":total_wage", reg0),
      (try_end),
	  ##diplomacy start+
	  #If the player leads a kingdom, take into account centralization.
	  (faction_get_slot, ":centralization", "$players_kingdom", dplmc_slot_faction_centralization),
	  (try_begin),
		  (neq, ":centralization", 0),

		  (assign, reg0, 0),
	     (try_begin),
		     (is_between, "$players_kingdom", kingdoms_begin, kingdoms_end),
		     (faction_get_slot, ":faction_leader", "$players_kingdom", slot_faction_leader),
		     (ge, ":faction_leader", 0),
		     (this_or_next|eq, ":faction_leader", "trp_player"),
		     (this_or_next|troop_slot_eq, ":faction_leader", slot_troop_spouse, "trp_player"),
              (troop_slot_eq, "trp_player", slot_troop_spouse, reg0),
           (assign, reg0, 1),
        (try_end),

		  (this_or_next|eq, reg0, 1),
		     (eq, "$players_kingdom", "fac_player_supporters_faction"),
		  (faction_slot_eq, "$players_kingdom", slot_faction_state, sfs_active),

		  #Apply centralization, but limit it for nascent kingdoms
        (val_clamp, ":centralization", -3, 4),
	     (faction_get_slot, ":policy_limit", "$players_kingdom", slot_faction_num_towns),
	     (faction_get_slot, reg0, "$players_kingdom", slot_faction_num_castles),
	     (val_add, ":policy_limit", reg0),

	     (val_max, ":policy_limit", 0),
	     (val_min, ":centralization", ":policy_limit"),
	     (val_mul, ":policy_limit", -1),
	     (val_max, ":centralization", ":policy_limit"),

		  #Now reg0 is going to be the result again
		  (store_mul, reg0, ":centralization", -5),
		  (val_add, reg0, 100),
		  (val_mul, reg0, ":total_wage"),
		  (val_add, reg0, 50),#rounding
		  (val_div, reg0, 100),
	  (try_end),
    ##diplomacy end+
      (assign, reg0, ":total_wage"),
      (set_trigger_result, reg0),
  ]),
  ("game_get_join_cost",
    [
      (store_script_param_1, ":troop_id"),
      
      (assign,":join_cost", 0),
      (try_begin),
        (troop_is_hero, ":troop_id"),
      (else_try),
        (store_character_level, ":troop_level", ":troop_id"),
        (assign, ":join_cost", ":troop_level"),
        (val_add, ":join_cost", 5),
        (val_mul, ":join_cost", ":join_cost"),
        (val_add, ":join_cost", 40),
        (val_div, ":join_cost", 5),
        (try_begin), #mounted troops cost %100 more than the normal cost
          (troop_is_mounted, ":troop_id"),
          (val_mul, ":join_cost", 2),
        (try_end),
      (try_end),
      (assign, reg0, ":join_cost"),
      (set_trigger_result, reg0),
  ]),
  # script_game_get_upgrade_xp
  # This script is called from game engine for calculating needed troop upgrade exp
  # Input:
  # param1: troop_id,
  # Output: reg0 = needed exp for upgrade 
  ("game_get_upgrade_xp",
    [
      (store_script_param_1, ":troop_id"),
      
      (assign, ":needed_upgrade_xp", 0),
      #formula : int needed_upgrade_xp = 2 * (30 + 0.006f * level_boundaries[troops[troop_id].level + 3]);
      (store_character_level, ":troop_level", ":troop_id"),
      (store_add, ":needed_upgrade_xp", ":troop_level", 3),
      (get_level_boundary, reg0, ":needed_upgrade_xp"),        
      (val_mul, reg0, 6),
      (val_div, reg0, 1000),
      (val_add, reg0, 30),

      (try_begin),               
        (ge, ":troop_id", bandits_begin),
        (lt, ":troop_id", bandits_end),
        (val_mul, reg0, 2),
      (try_end),

      (set_trigger_result, reg0),
  ]),
  # script_game_get_upgrade_cost
  # This script is called from game engine for calculating needed troop upgrade exp
  # Input:
  # param1: troop_id,
  # Output: reg0 = needed cost for upgrade
  ("game_get_upgrade_cost",
    [
      (store_script_param_1, ":troop_id"),
      
      (store_character_level, ":troop_level", ":troop_id"),
      
      (try_begin),
        (is_between, ":troop_level", 0, 6),
        (assign, reg0, 10),
      (else_try),  
        (is_between, ":troop_level", 6, 11),
        (assign, reg0, 20),
      (else_try),  
        (is_between, ":troop_level", 11, 16),
        (assign, reg0, 40),
      (else_try),  
        (is_between, ":troop_level", 16, 21),
        (assign, reg0, 80),
      (else_try),  
        (is_between, ":troop_level", 21, 26),
        (assign, reg0, 120),
      (else_try),  
        (is_between, ":troop_level", 26, 31),
        (assign, reg0, 160),
      (else_try),  
        (assign, reg0, 200),
      (try_end),  
        
      (set_trigger_result, reg0),
  ]),
  # script_game_get_prisoner_price
  # This script is called from the game engine for calculating prisoner price
  # Input:
  # param1: troop_id,
  # Output: reg0  
  ("game_get_prisoner_price",
    [
      (store_script_param_1, ":troop_id"),
            
      (try_begin),
        (is_between, "$g_talk_troop", ransom_brokers_begin, ransom_brokers_end),
        (store_character_level, ":troop_level", ":troop_id"),
        (assign, ":ransom_amount", ":troop_level"),
        (val_add, ":ransom_amount", 10), 
        (val_mul, ":ransom_amount", ":ransom_amount"),
        (val_div, ":ransom_amount", 6),
      (else_try),  
        (assign, ":ransom_amount", 50),
      (try_end),
      
      (assign, reg0, ":ransom_amount"),
      
      (set_trigger_result, reg0),
  ]),
  ("game_check_prisoner_can_be_sold",
    [
      (store_script_param_1, ":troop_id"),
      (assign, reg0, 0),
      (try_begin),
        (neg|troop_is_hero, ":troop_id"),
        (assign, reg0, 1),
      (try_end),
      (set_trigger_result, reg0),
  ]),
  ("game_get_morale_of_troops_from_faction",
    [
      (store_script_param_1, ":troop_no"),            
      
      (store_troop_faction, ":faction_no", ":troop_no"),
      
      (try_begin),
        (ge, ":faction_no", npc_kingdoms_begin),
        (lt, ":faction_no", npc_kingdoms_end),
        
        (faction_get_slot, reg0, ":faction_no",  slot_faction_morale_of_player_troops),

        #(assign, reg1, ":faction_no"),
        #(assign, reg2, ":troop_no"),
        #(assign, reg3, reg0),
        #(display_message, "@extra morale for troop {reg2} of faction {reg1} is {reg3}"),
      (else_try),
        (assign, reg0, 0),
      (try_end),
      ##diplomacy start+
      #If there is no current morale penalty, then there will be a minor morale bonus
		#if the player has his own faction and his culture matches the source kingdom.
		(try_begin),
		   (eq, reg0, 0),
			(is_between,"$g_player_culture", npc_kingdoms_begin, npc_kingdoms_end),
			(eq, "$g_player_culture", ":faction_no"),
			#xxx TODO: pick a number less arbitrarily
			(assign, reg0, 100),
		(try_end),
      ##diplomacy end+            
      (val_div, reg0, 100),
      
      (party_get_morale, reg1, "p_main_party"),
      
      (val_add, reg0, reg1),
      
      (set_trigger_result, reg0),
  ]),
  #script_game_event_detect_party:
  # This script is called from the game engine when player party inspects another party.
  # INPUT:
  # param1: Party-id
  ("game_event_detect_party",
    [
        (store_script_param_1, ":party_id"),
        (try_begin),
          (party_slot_eq, ":party_id", slot_party_type, spt_kingdom_hero_party),
          (party_stack_get_troop_id, ":leader", ":party_id", 0),
          ##diplomacy start+ support for promoted kingdom ladies
          (is_between, ":leader", heroes_begin, heroes_end),
          (this_or_next|troop_slot_eq, ":leader", slot_troop_occupation, slto_kingdom_hero),
          ##diplomacy end+
          (is_between, ":leader", active_npcs_begin, active_npcs_end),
          (call_script, "script_update_troop_location_notes", ":leader", 0),
        (else_try),
          (is_between, ":party_id", walled_centers_begin, walled_centers_end),
          (party_get_num_attached_parties, ":num_attached_parties",  ":party_id"),
          (try_for_range, ":attached_party_rank", 0, ":num_attached_parties"),
            (party_get_attached_party_with_rank, ":attached_party", ":party_id", ":attached_party_rank"),
            (party_stack_get_troop_id, ":leader", ":attached_party", 0),
			##diplomacy start+ support for promoted kingdom ladies
			(is_between, ":leader", heroes_begin, heroes_end),
			(this_or_next|troop_slot_eq, ":leader", slot_troop_occupation, slto_kingdom_hero),
			##diplomacy end+
            (is_between, ":leader", active_npcs_begin, active_npcs_end),
            (call_script, "script_update_troop_location_notes", ":leader", 0),
          (try_end),
        (try_end),
  ]),
  #script_game_event_undetect_party:
  # This script is called from the game engine when player party inspects another party.
  # INPUT:
  # param1: Party-id
  ("game_event_undetect_party",
    [
        (store_script_param_1, ":party_id"),
        (try_begin),
          (party_slot_eq, ":party_id", slot_party_type, spt_kingdom_hero_party),
          (party_stack_get_troop_id, ":leader", ":party_id", 0),
          ##diplomacy start+ support for promoted kingdom ladies
          (is_between, ":leader", heroes_begin, heroes_end),
          (this_or_next|troop_slot_eq, ":leader", slot_troop_occupation, slto_kingdom_hero),
          ##diplomacy end+
          (is_between, ":leader", active_npcs_begin, active_npcs_end),
          (call_script, "script_update_troop_location_notes", ":leader", 0),
        (try_end),
  ]),
  #script_game_get_statistics_line:
  # This script is called from the game engine when statistics page is opened.
  # INPUT:
  # param1: line_no
  ("game_get_statistics_line",
    [
      (store_script_param_1, ":line_no"),
      (try_begin),
        (eq, ":line_no", 0),
        (get_player_agent_kill_count, reg1),
        (str_store_string, s1, "str_number_of_troops_killed_reg1"),
        (set_result_string, s1),
      (else_try),
        (eq, ":line_no", 1),
        (get_player_agent_kill_count, reg1, 1),
        (str_store_string, s1, "str_number_of_troops_wounded_reg1"),
        (set_result_string, s1),
      (else_try),
        (eq, ":line_no", 2),
        (get_player_agent_own_troop_kill_count, reg1),
        (str_store_string, s1, "str_number_of_own_troops_killed_reg1"),
        (set_result_string, s1),
      (else_try),
        (eq, ":line_no", 3),
        (get_player_agent_own_troop_kill_count, reg1, 1),
        (str_store_string, s1, "str_number_of_own_troops_wounded_reg1"),
        (set_result_string, s1),
      (try_end),
  ]),
  #script_game_get_date_text:
  # This script is called from the game engine when the date needs to be displayed.
  # INPUT: arg1 = number of days passed since the beginning of the game
  # OUTPUT: result string = date
  ("game_get_date_text",
    [
      (store_script_param_2, ":num_hours"),
      (store_div, ":num_days", ":num_hours", 24),
      (store_add, ":cur_day", ":num_days", 1),
      (assign, ":cur_month", 1),
      (assign, ":cur_year", 1868),
      (assign, ":try_range", 99999),
      (try_for_range, ":unused", 0, ":try_range"),
        (try_begin),
          (this_or_next|eq, ":cur_month", 1),
          (this_or_next|eq, ":cur_month", 3),
          (this_or_next|eq, ":cur_month", 5),
          (this_or_next|eq, ":cur_month", 7),
          (this_or_next|eq, ":cur_month", 8),
          (this_or_next|eq, ":cur_month", 10),
          (eq, ":cur_month", 12),
          (assign, ":month_day_limit", 31),
        (else_try),
          (this_or_next|eq, ":cur_month", 4),
          (this_or_next|eq, ":cur_month", 6),
          (this_or_next|eq, ":cur_month", 9),
          (eq, ":cur_month", 11),
          (assign, ":month_day_limit", 30),
        (else_try),
          (try_begin),
            (store_div, ":cur_year_div_4", ":cur_year", 4),
            (val_mul, ":cur_year_div_4", 4),
            (eq, ":cur_year_div_4", ":cur_year"),
            (assign, ":month_day_limit", 29),
          (else_try),
            (assign, ":month_day_limit", 28),      
          (try_end),
        (try_end),
        (try_begin),
          (gt, ":cur_day", ":month_day_limit"),
          (val_sub, ":cur_day", ":month_day_limit"),
          (val_add, ":cur_month", 1),
          (try_begin),
            (gt, ":cur_month", 12),
            (val_sub, ":cur_month", 12),
            (val_add, ":cur_year", 1),
          (try_end),
        (else_try),
          (assign, ":try_range", 0),
        (try_end),
      (try_end),
      (assign, reg1, ":cur_day"),
      (assign, reg2, ":cur_year"),
      (try_begin),
        (eq, ":cur_month", 1),
        (str_store_string, s1, "str_january_reg1_reg2"),
      (else_try),
        (eq, ":cur_month", 2),
        (str_store_string, s1, "str_february_reg1_reg2"),
      (else_try),
        (eq, ":cur_month", 3),
        (str_store_string, s1, "str_march_reg1_reg2"),
      (else_try),
        (eq, ":cur_month", 4),
        (str_store_string, s1, "str_april_reg1_reg2"),
      (else_try),
        (eq, ":cur_month", 5),
        (str_store_string, s1, "str_may_reg1_reg2"),
      (else_try),
        (eq, ":cur_month", 6),
        (str_store_string, s1, "str_june_reg1_reg2"),
      (else_try),
        (eq, ":cur_month", 7),
        (str_store_string, s1, "str_july_reg1_reg2"),
      (else_try),
        (eq, ":cur_month", 8),
        (str_store_string, s1, "str_august_reg1_reg2"),
      (else_try),
        (eq, ":cur_month", 9),
        (str_store_string, s1, "str_september_reg1_reg2"),
      (else_try),
        (eq, ":cur_month", 10),
        (str_store_string, s1, "str_october_reg1_reg2"),
      (else_try),
        (eq, ":cur_month", 11),
        (str_store_string, s1, "str_november_reg1_reg2"),
      (else_try),
        (eq, ":cur_month", 12),
        (str_store_string, s1, "str_december_reg1_reg2"),
      (try_end),
      (set_result_string, s1),
	  #
	  (assign, "$c_year", ":cur_year"),
      (assign, "$c_month", ":cur_month"),
      (assign, "$c_day", ":cur_day"),
    ]),
  #script_game_get_money_text:
  # This script is called from the game engine when an amount of money needs to be displayed.
  # INPUT: arg1 = amount in units
  # OUTPUT: result string = money in text
  ("game_get_money_text",
    [
      (store_script_param_1, ":amount"),
      (try_begin),
        (eq, ":amount", 1),
        (str_store_string, s1, "str_1_denar"),
      (else_try),
        (assign, reg1, ":amount"),
        (str_store_string, s1, "str_reg1_denars"),
      (try_end),
      (set_result_string, s1),
  ]),
  #script_game_get_party_companion_limit:
  # This script is called from the game engine when the companion limit is needed for a party.
  # INPUT: arg1 = none
  # OUTPUT: reg0 = companion_limit
  ("game_get_party_companion_limit",
    [
      (assign, ":troop_no", "trp_player"),

      (assign, ":limit", 20),
      (store_skill_level, ":skill", "skl_leadership", ":troop_no"),
      (store_attribute_level, ":charisma", ":troop_no", ca_charisma),
      (val_mul, ":skill", 5),
      (val_add, ":limit", ":skill"),
      (val_add, ":limit", ":charisma"),

      (troop_get_slot, ":troop_renown", ":troop_no", slot_troop_renown),
	  #gekokujo 3.0 increased renown bonus to party size
      #(store_div, ":renown_bonus", ":troop_renown", 25),
	  (store_div, ":renown_bonus", ":troop_renown", 10),
      (val_add, ":limit", ":renown_bonus"),

	  #gekokujo 3.0 player party size bonuses start
      (store_faction_of_party, ":faction_id", ":troop_no"),
	  
      (try_begin),
	    (is_between, ":faction_id", kingdoms_begin, kingdoms_end),
		(faction_slot_eq, ":faction_id", slot_faction_state, sfs_active),
        (faction_slot_eq, ":faction_id", slot_faction_leader, ":troop_no"),
        (val_add, ":limit", 20), #+20 for being the leader of your own faction
      (try_end),

      (try_begin),
	    (is_between, ":faction_id", kingdoms_begin, kingdoms_end),
		(faction_slot_eq, ":faction_id", slot_faction_state, sfs_active),
        (faction_slot_eq, ":faction_id", slot_faction_marshall, ":troop_no"),
        (val_add, ":limit", 20), #+20 for being the strategist
      (try_end),        

      (try_for_range, ":cur_center", walled_centers_begin, walled_centers_end),
        (party_slot_eq, ":cur_center", slot_town_lord, ":troop_no"),
        (val_add, ":limit", 10), #+10 for each walled center
      (try_end),
	  #gekokujo 3.0 player party size bonuses end

	  #gekokujo 3.1 samurai party penalty start
	  #in this option (off by default), every samurai takes up 2 slots rather than 1
	  #since you can't actually change how many slots a unit takes up, this is a penalty to party size instaed
	  #the slots taken up represent off-screen servants and attendants that are useless in battle
      (try_begin),
	    (eq, "$g_gekokujo_samurai_penalty", 1),
	    (assign, ":samurai_penalty", 0),
		(party_get_num_companion_stacks, ":num_stacks", "p_main_party"),
	    (try_for_range, ":i_stack", 0, ":num_stacks"),
		  (party_stack_get_troop_id, ":stack_troop", "p_main_party", ":i_stack"),
		  (is_between, ":stack_troop", samurai_troops_begin, samurai_troops_end),
		  (party_stack_get_size, ":stack_size", "p_main_party", ":i_stack"),
		  (val_add, ":samurai_penalty", ":stack_size"),
		(try_end),
	    (val_sub, ":limit", ":samurai_penalty"),
	  (try_end),
	  #gekokujo 3.1 samurai party penalty end
	  
      (assign, reg0, ":limit"),
      (set_trigger_result, reg0),
  ]),
  #script_game_reset_player_party_name:
  # This script is called from the game engine when the player name is changed.
  # INPUT: none
  # OUTPUT: none
  ("game_reset_player_party_name",
    [(str_store_troop_name, s5, "trp_player"),
     (party_set_name, "p_main_party", s5),
     ]),
  #script_game_get_troop_note
  # This script is called from the game engine when the notes of a troop is needed.
  # INPUT: arg1 = troop_no, arg2 = note_index
  # OUTPUT: s0 = note
  ("game_get_troop_note",
    [
      (store_script_param_1, ":troop_no"),
      (store_script_param_2, ":note_index"),
      (set_trigger_result, 0),

      (str_store_troop_name, s54, ":troop_no"),
      (try_begin),
        (eq, ":troop_no", "trp_player"),
        (this_or_next|eq, "$player_has_homage", 1),
        (eq, "$players_kingdom", "fac_player_supporters_faction"),
        (assign, ":troop_faction", "$players_kingdom"),
      (else_try),
        (store_troop_faction, ":troop_faction", ":troop_no"),
		

		
      (try_end),
      (str_clear, s49),
	  
	  #Family notes
      (try_begin),
	    ##diplomacy start+ add support for displaying relations with kings and claimants
		#(this_or_next|is_between, ":troop_no", lords_begin, kingdom_ladies_end),
        #(eq, ":troop_no", "trp_player"),
        #(neg|is_between, ":troop_no", pretenders_begin, pretenders_end),

		(this_or_next|eq, ":troop_no", "trp_player"),
		(this_or_next|is_between, ":troop_no", lords_begin, kingdom_ladies_end),#includes pretenders
			(is_between, ":troop_no", kings_begin, kings_end),

		##The following would only show relations for kings and claimants if they are married.
        #(this_or_next|troop_slot_ge, ":troop_no", slot_troop_spouse, 0),
		#	(neg|is_between, ":troop_no", pretenders_begin, pretenders_end),
		#(this_or_next|troop_slot_ge, ":troop_no", slot_troop_spouse, 0),
		#	(neg|is_between, ":troop_no", kings_begin, kings_end),

		##diplomacy end+
        (assign, ":num_relations", 0),

        (try_begin),
          (call_script, "script_troop_get_family_relation_to_troop", "trp_player", ":troop_no"),
          (gt, reg0, 0),
          (val_add, ":num_relations", 1),
        (try_end),
		##diplomacy start+
        #(try_for_range, ":aristocrat", lords_begin, kingdom_ladies_end),
		#Display relations with kings and claimants
		(try_for_range, ":aristocrat", heroes_begin, heroes_end),
		  (this_or_next|is_between, ":aristocrat", lords_begin, kingdom_ladies_end),#includes pretenders
			  (is_between, ":aristocrat", kings_begin, kings_end),
		##diplomacy end+
          (call_script, "script_troop_get_family_relation_to_troop", ":aristocrat", ":troop_no"),
          (gt, reg0, 0),
          (val_add, ":num_relations", 1),
        (try_end),
        (try_begin),
          (gt, ":num_relations", 0),
          (try_begin),
            (eq, ":troop_no", "trp_player"),
            (str_store_string, s49, "str__family_"),
          (else_try),
            (troop_get_slot, reg1, ":troop_no", slot_troop_age),
            (str_store_string, s49, "str__age_reg1_family_"),
          (try_end),
          (try_begin),
            (call_script, "script_troop_get_family_relation_to_troop", "trp_player", ":troop_no"),
            (gt, reg0, 0),
            (str_store_troop_name_link, s12, "trp_player"),
            (val_sub, ":num_relations", 1),
            (try_begin),
              (eq, ":num_relations", 0),
              (str_store_string, s49, "str_s49_s12_s11_end"),
            (else_try),
              (str_store_string, s49, "str_s49_s12_s11"),
            (try_end),
          (try_end),
		  ##diplomacy start+
          #(try_for_range, ":aristocrat", lords_begin, kingdom_ladies_end),
		  #Display relations with kings and claimants
		  (try_for_range, ":aristocrat", heroes_begin, heroes_end),
		    (this_or_next|is_between, ":aristocrat", lords_begin, kingdom_ladies_end),#includes pretenders
			   (is_between, ":aristocrat", kings_begin, kings_end),
		  ##diplomacy end+
            (call_script, "script_troop_get_family_relation_to_troop", ":aristocrat", ":troop_no"),
            (gt, reg0, 0),
            (try_begin),
              (neg|is_between, ":aristocrat", kingdom_ladies_begin, kingdom_ladies_end),
              (eq, "$cheat_mode", 1),
              (str_store_troop_name_link, s12, ":aristocrat"),
              (call_script, "script_troop_get_relation_with_troop", ":aristocrat", ":troop_no"),
              (str_store_string, s49, "str_s49_s12_s11_rel_reg0"),
            (else_try),
              (str_store_troop_name_link, s12, ":aristocrat"),
              (val_sub, ":num_relations", 1),
              (try_begin),
                (eq, ":num_relations", 0),
                (str_store_string, s49, "str_s49_s12_s11_end"),
              (else_try),
                (str_store_string, s49, "str_s49_s12_s11"),
              (try_end),
            (try_end),
          (try_end),
        (try_end),
      (try_end),
      
      (try_begin),
        (neq, ":troop_no", "trp_player"),
        (neg|is_between, ":troop_faction", kingdoms_begin, kingdoms_end),
		#gekokujo 3.0 microfactions! include fort companions start
        #(neg|is_between, ":troop_no", companions_begin, companions_end),
        (neg|is_between, ":troop_no", companions_begin, fort_companions_end),
		#gekokujo 3.0 microfactions! include fort companions end
        (neg|is_between, ":troop_no", pretenders_begin, pretenders_end),

        (try_begin),
          (eq, ":note_index", 0),
          (str_store_string, s0, "str_s54_has_left_the_realm"),
          ##diplomacy start+
          #Check for "deceased" instead
          (try_begin),
             (troop_slot_eq, ":troop_no", slot_troop_occupation, dplmc_slto_dead),
             (str_store_string, s0, "str_s54_is_deceased"),
          (try_end),
          ##diplomacy end+
          (set_trigger_result, 1),
        (else_try),
          (str_clear, s0),
          (this_or_next|eq, ":note_index", 1),
          (eq, ":note_index", 2),
          (set_trigger_result, 1),
        (try_end),

      (else_try),
		#gekokujo 3.0 microfactions! include fort companions start
        #(is_between, ":troop_no", companions_begin, companions_end),
        (is_between, ":troop_no", companions_begin, fort_companions_end),
		#gekokujo 3.0 microfactions! include fort companions end
        (neg|troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
        (eq, ":note_index", 0),
        (set_trigger_result, 1),
        (str_clear, s0),
        (assign, ":companion", ":troop_no"),
        (str_store_troop_name, s4, ":companion"),
        (try_begin),
			(troop_get_slot, ":days_left", ":companion", slot_troop_days_on_mission),

			(this_or_next|main_party_has_troop, ":companion"),
			(this_or_next|troop_slot_ge, ":companion", slot_troop_current_mission, 1),
				(eq, "$g_player_minister", ":companion"),

			(try_begin),
				(troop_slot_eq, ":companion", slot_troop_current_mission, npc_mission_kingsupport),
				(str_store_string, s8, "str_gathering_support"),
				(try_begin),
					(eq, ":days_left", 1),
					(str_store_string, s5, "str_expected_back_imminently"),
				(else_try),	
					(assign, reg3, ":days_left"),
					(str_store_string, s5, "str_expected_back_in_approximately_reg3_days"),
				(try_end),
			(else_try),
				(troop_slot_eq, ":companion", slot_troop_current_mission, npc_mission_gather_intel),
				(troop_get_slot, ":town_with_contacts", ":companion", slot_troop_town_with_contacts),
				(str_store_party_name, s11, ":town_with_contacts"),
				
				(str_store_string, s8, "str_gathering_intelligence"),
				(try_begin),
					(eq, ":days_left", 1),
					(str_store_string, s5, "str_expected_back_imminently"),
				(else_try),	
					(assign, reg3, ":days_left"),
					(str_store_string, s5, "str_expected_back_in_approximately_reg3_days"),
				(try_end),
			(else_try),	
				
				(troop_slot_ge, ":companion", slot_troop_current_mission, npc_mission_peace_request),
				(neg|troop_slot_ge, ":companion", slot_troop_current_mission, 8),

				(troop_get_slot, ":faction", ":companion", slot_troop_mission_object),
				(str_store_faction_name, s9, ":faction"),
				(str_store_string, s8, "str_diplomatic_embassy_to_s9"),
				(try_begin),
					(eq, ":days_left", 1),
					(str_store_string, s5, "str_expected_back_imminently"),
				(else_try),	
					(assign, reg3, ":days_left"),
					(str_store_string, s5, "str_expected_back_in_approximately_reg3_days"),
				(try_end),
			(else_try),
				(eq, ":companion", "$g_player_minister"),
				(str_store_string, s8, "str_serving_as_minister"),
				(str_store_party_name, s9, "$g_player_court"),
				(is_between, "$g_player_court", centers_begin, centers_end),
				(str_store_string, s5, "str_in_your_court_at_s9"),
			(else_try),
				(eq, ":companion", "$g_player_minister"),
				(str_store_string, s8, "str_serving_as_minister"),
				(str_store_string, s5, "str_awaiting_the_capture_of_a_fortress_which_can_serve_as_your_court"),
			(else_try),
				(main_party_has_troop, ":companion"),
				(str_store_string, s8, "str_under_arms"),
				(str_store_string, s5, "str_in_your_party"),
			(try_end),	
			
			(str_store_string, s0, "str_s4_s8_s5"),
		##diplomacy start+
		#Check for explicit "exiled" and "dead" settings
		(else_try),
			(troop_slot_eq, ":troop_no", slot_troop_occupation, dplmc_slto_dead),
			(str_store_string, s0, "str_s54_is_deceased"),
		(else_try),
			(troop_slot_eq, ":troop_no", slot_troop_occupation, dplmc_slto_exile),
			(str_store_string, s0, "str_s54_has_left_the_realm"),
		##diplomacy end+			
		(else_try),
			(str_store_string, s0, "str_whereabouts_unknown"),
		(try_end),
		
	  
	  (else_try),
        (is_between, ":troop_no", pretenders_begin, pretenders_end),
        (neg|troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
        (neq, ":troop_no", "$supported_pretender"),

		
        (troop_get_slot, ":orig_faction", ":troop_no", slot_troop_original_faction),
        (try_begin),
          (faction_slot_eq, ":orig_faction", slot_faction_state, sfs_active),
          (faction_slot_eq, ":orig_faction", slot_faction_has_rebellion_chance, 1),
          (try_begin),
            (eq, ":note_index", 0),
            (str_store_faction_name_link, s56, ":orig_faction"),
            ##diplomacy start+ xxx Removed third argument (was it doing anything?)
            #(str_store_string, s0, "@{s54} is a claimant to the throne of {s56}.", 0),
            (str_store_string, s0, "@{s54} is a claimant to the overlordship of {s56}."),
            ##diplomacy end+
            (set_trigger_result, 1),
          (try_end),
        (else_try),
          (try_begin),
            (str_clear, s0),
            (this_or_next|eq, ":note_index", 0),
            (this_or_next|eq, ":note_index", 1),
            (eq, ":note_index", 2),
            (set_trigger_result, 1),
          (try_end),
        (try_end),
		
      (else_try),
        (try_begin),
          (eq, ":note_index", 0),
          (faction_get_slot, ":faction_leader", ":troop_faction", slot_faction_leader),
          (str_store_troop_name_link, s55, ":faction_leader"),
          (str_store_faction_name_link, s56, ":troop_faction"),
          (assign, ":troop_is_player_faction", 0),
          (assign, ":troop_is_faction_leader", 0),
          (try_begin),
            (eq, ":troop_faction", "fac_player_faction"),
            (assign, ":troop_is_player_faction", 1),
          (else_try),
            (eq, ":faction_leader", ":troop_no"),
            (assign, ":troop_is_faction_leader", 1),
          (try_end),
          (assign, ":num_centers", 0),
          (str_store_string, s58, "@nowhere"),
          (try_for_range_backwards, ":cur_center", centers_begin, centers_end),                     
            (party_slot_eq, ":cur_center", slot_town_lord, ":troop_no"),
            (try_begin),
              (eq, ":num_centers", 0),
              (str_store_party_name_link, s58, ":cur_center"),
            (else_try),
              (eq, ":num_centers", 1),
              (str_store_party_name_link, s57, ":cur_center"),
              (str_store_string, s58, "@{s57} and {s58}"),
            (else_try),
              (str_store_party_name_link, s57, ":cur_center"),
              (str_store_string, s58, "@{!}{s57}, {s58}"),
            (try_end),
            (val_add, ":num_centers", 1),
          (try_end),
		  ##diplomacy start+ use script for gender
          #(troop_get_type, reg3, ":troop_no"),
        (call_script, "script_dplmc_store_troop_is_female_reg", ":troop_no", 3),
		  #(assign, reg3, reg0),
		  ##diplomacy end+
          (troop_get_type, reg3, ":troop_no"),
          (troop_get_slot, reg5, ":troop_no", slot_troop_renown),
          (troop_get_slot, reg15, ":troop_no", slot_troop_controversy),
		  
          (str_clear, s59),
          (try_begin),   
            (call_script, "script_troop_get_player_relation", ":troop_no"),
            (assign, ":relation", reg0),
            (store_add, ":normalized_relation", ":relation", 100),
            (val_add, ":normalized_relation", 5),
            (store_div, ":str_offset", ":normalized_relation", 10),
            (val_clamp, ":str_offset", 0, 20),
            (store_add, ":str_id", "str_relation_mnus_100_ns",  ":str_offset"),
            (neq, ":str_id", "str_relation_plus_0_ns"),
            (str_store_string, s60, "@{reg3?She:He}"),
            (str_store_string, s59, ":str_id"),
            (str_store_string, s59, "@{!}^{s59}"),
          (try_end),
          #lord recruitment changes begin
          #This sends a bunch of political information to s47.
    
          #refresh registers
          (assign, reg9, ":num_centers"),
		  ##diplomacy start+ use script for gender
          #(troop_get_type, reg3, ":troop_no"),
		  (call_script, "script_dplmc_store_troop_is_female_reg", ":troop_no", 3),
		  ##diplomacy end+
          (troop_get_slot, reg5, ":troop_no", slot_troop_renown),
          (assign, reg4, ":troop_is_faction_leader"),
          (assign, reg6, ":troop_is_player_faction"),
          
          (troop_get_slot, reg17, ":troop_no", slot_troop_wealth), #DEBUGS
          ##diplomacy start+ xxx remove third argument (was it doing anything?)
          #(str_store_string, s0, "str_lord_info_string", 0),
          (str_store_string, s0, "str_lord_info_string"),
          ##diplomacy end+
          #lord recruitment changes end
          (add_troop_note_tableau_mesh, ":troop_no", "tableau_troop_note_mesh"),
          (set_trigger_result, 1),
        (try_end),
      (try_end),
     ]),
  #script_game_get_center_note
  # This script is called from the game engine when the notes of a center is needed.
  # INPUT: arg1 = center_no, arg2 = note_index
  # OUTPUT: s0 = note
  ("game_get_center_note",
    [
      (store_script_param_1, ":center_no"),
      (store_script_param_2, ":note_index"),

      (set_trigger_result, 0),
      (try_begin),
        (eq, ":note_index", 0),
        (party_get_slot, ":lord_troop", ":center_no", slot_town_lord),
        (try_begin),
          (ge, ":lord_troop", 0),
          (store_troop_faction, ":lord_faction", ":lord_troop"),
          (str_store_troop_name_link, s1, ":lord_troop"),
          (try_begin),
            (eq, ":lord_troop", "trp_player"),
            (gt, "$players_kingdom", 0),
            (str_store_faction_name_link, s2, "$players_kingdom"),
          (else_try),
            (str_store_faction_name_link, s2, ":lord_faction"),
          (try_end),
          (str_store_party_name, s50, ":center_no"),
          (try_begin),
            (party_slot_eq, ":center_no", slot_party_type, spt_town),
            (str_store_string, s51, "@The town of {s50}"),
          (else_try),
            (party_slot_eq, ":center_no", slot_party_type, spt_village),
            (party_get_slot, ":bound_center", ":center_no", slot_village_bound_center),
            (str_store_party_name_link, s52, ":bound_center"),
            (str_store_string, s51, "@The village of {s50} near {s52}"),
          (else_try),
            (str_store_string, s51, "@{!}{s50}"),
          (try_end),
          ##diplomacy start+ Show when the city is the home of a lord or is a court
          (assign, ":bound_center", reg0),#Save reg0 to avoid having it randomly change
          (try_begin),
             (eq, "$g_player_court", ":center_no"),
             (str_store_string, s2, "@{s51} belongs to {s1} of {s2}, and is where you make your court.^"),
          (else_try),
             (neq, ":lord_troop", "trp_player"),
             (neg|is_between, ":center_no", villages_begin, villages_end),
             (call_script, "script_lord_get_home_center", ":lord_troop"),
             (eq, reg0, ":center_no"),
             (call_script, "script_dplmc_get_troop_standing_in_faction", ":lord_troop", ":lord_faction"),
             (try_begin),
                (ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
                (call_script, "script_dplmc_store_troop_is_female", ":lord_troop"),
                (str_store_string, s2, "@{s51} belongs to {s1} of {s2}, and is where {reg0?she:he} makes {reg0?her:his} court.^"),
             (else_try),
                (call_script, "script_dplmc_store_troop_is_female", ":lord_troop"),
                (str_store_string, s2, "@{s51} belongs to {s1} of {s2}, and is where {reg0?she:he} makes {reg0?her:his} home.^"),
             (try_end),
          (else_try),#Fall through to normal behavior
          ##diplomacy end+
          (str_store_string, s2, "@{s51} belongs to {s1} of {s2}.^"),
          ##diplomacy start+
          (try_end),
          (assign, reg0, ":bound_center"),#Revert reg0 to avoid having it randomly change
          ##diplomacy end+
        (else_try),
          (str_clear, s2),
          ##diplomacy start+ Don't hide notes for centers with no lords.
          (store_faction_of_party, ":lord_faction", ":center_no"),
          (str_store_string, s1, "str_noone"),
          (try_begin),
             (ge, ":lord_faction", 1),
             (str_store_faction_name_link, s2, ":lord_faction"),
          (else_try),
             (str_store_string, s2, "str_noone"),
          (try_end),
          (str_store_party_name, s50, ":center_no"),
          (try_begin),
            (party_slot_eq, ":center_no", slot_party_type, spt_town),
            (str_store_string, s51, "@The town of {s50}"),
          (else_try),
            (party_slot_eq, ":center_no", slot_party_type, spt_village),
            (party_get_slot, ":bound_center", ":center_no", slot_village_bound_center),
            (str_store_party_name_link, s52, ":bound_center"),
            (str_store_string, s51, "@The village of {s50} near {s52}"),
          (else_try),
            (str_store_string, s51, "@{!}{s50}"),
          (try_end),
          (try_begin),
             (is_between, ":lord_faction", kingdoms_begin, kingdoms_end),
             (faction_slot_eq, ":lord_faction", slot_faction_state, sfs_active),
             (str_store_string, s2, "@{s51} belongs to {s2} but has not yet been granted to a lord.^"),
          (else_try),
             (str_store_string, s2, "@{s51} belongs to {s2}.^"),
          (try_end),
          ##diplomacy end+
        (try_end),
        (try_begin),
          (is_between, ":center_no", villages_begin, villages_end),
          ##diplomacy start+ Show market town if it differs from the bound center
          (party_get_slot, ":market_center", ":center_no", slot_village_market_town),
          (try_begin),
             (is_between, ":market_center", centers_begin, centers_end),
             (neq, ":market_center", ":center_no"),
             (neg|party_slot_eq, ":center_no", slot_village_bound_center, ":market_center"),
             (str_store_party_name_link, s8, ":market_center"),
             (str_store_string, s2, "@{s2}Its market town is {s8}.^"),
          (try_end),
          ##diplomacy end+
        (else_try),
          (assign, ":num_villages", 0),
          (try_for_range_backwards, ":village_no", villages_begin, villages_end),
            (party_slot_eq, ":village_no", slot_village_bound_center, ":center_no"),
            (try_begin),
              (eq, ":num_villages", 0),
              (str_store_party_name_link, s8, ":village_no"),
            (else_try),
              (eq, ":num_villages", 1),
              (str_store_party_name_link, s7, ":village_no"),
              (str_store_string, s8, "@{s7} and {s8}"),
            (else_try),
              (str_store_party_name_link, s7, ":village_no"),
              (str_store_string, s8, "@{!}{s7}, {s8}"),
            (try_end),
            (val_add, ":num_villages", 1),
          (try_end),
          (try_begin),
            (eq, ":num_villages", 0),
            (str_store_string, s2, "@{s2}It has no villages.^"),
          (else_try),
            (store_sub, reg0, ":num_villages", 1),
            (str_store_string, s2, "@{s2}{reg0?Its villages are:Its village is} {s8}.^"),
          (try_end),
        (try_end),
        (call_script, "script_get_prosperity_text_to_s50", ":center_no"),
        (str_store_string, s0, "@{s2}Its prosperity is: {s50}", 0),
        (set_trigger_result, 1),
      (try_end),
     ]),
  #script_game_get_faction_note
  # This script is called from the game engine when the notes of a faction is needed.
  # INPUT: arg1 = faction_no, arg2 = note_index
  # OUTPUT: s0 = note
  ("game_get_faction_note",
    [
      (store_script_param_1, ":faction_no"),
      (store_script_param_2, ":note_index"),
      (set_trigger_result, 0),
      
##      (try_begin),
##        (eq, 2, 1),
##        (str_store_faction_name, s14, ":faction_no"),
##        (assign, reg4, "$temp"),
##        (display_message, "str_updating_faction_notes_for_s14_temp_=_reg4"),
##      (try_end),

      (try_begin),
        (is_between, ":faction_no", kingdoms_begin, kingdoms_end),
        (faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
        #conditions end
        (try_begin),
            (eq, ":note_index", 0),
          (faction_get_slot, ":faction_leader", ":faction_no", slot_faction_leader),
          (str_store_faction_name, s5, ":faction_no"),
          ##diplomacy start+
          ##OLD:
          #(str_store_troop_name_link, s6, ":faction_leader"),
          ##NEW:
          (try_begin),
             (lt, ":faction_leader", 0),
             #(le, ":faction_leader", 0),
             #(this_or_next|lt, ":faction_leader", 0),
             #   (neg|is_between, ":faction_no", kingdoms_begin, kingdoms_end),
             (str_store_string, s6, "str_noone"),
          (else_try),
             (eq, ":faction_leader", "trp_kingdom_heroes_including_player_begin"),
             (assign, ":faction_leader", "trp_player"),
          (str_store_troop_name_link, s6, ":faction_leader"),
          (else_try),
             (str_store_troop_name_link, s6, ":faction_leader"),
          (try_end),
			 ##diplomacy end+
          (assign, ":num_centers", 0),
          (str_store_string, s8, "@nowhere"),
          (try_for_range_backwards, ":cur_center", centers_begin, centers_end),
            (store_faction_of_party, ":center_faction", ":cur_center"),
            (eq, ":center_faction", ":faction_no"),
            (try_begin),
              (eq, ":num_centers", 0),
              (str_store_party_name_link, s8, ":cur_center"),
            (else_try),
              (eq, ":num_centers", 1),
              (str_store_party_name_link, s7, ":cur_center"),
              (str_store_string, s8, "@{s7} and {s8}"),
            (else_try),
              (str_store_party_name_link, s7, ":cur_center"),
              (str_store_string, s8, "@{!}{s7}, {s8}"),
            (try_end),
            (val_add, ":num_centers", 1),
          (try_end),
          (assign, ":num_members", 0),
          (str_store_string, s10, "@noone"),
          ##diplomacy start+ support for promoted kingdom ladies
          (try_for_range_backwards, ":loop_var", "trp_kingdom_heroes_including_player_begin", heroes_end),#<- changed active_npcs_end to heroes_end
          ##diplomacy end+
            (assign, ":cur_troop", ":loop_var"),
            (try_begin),
              (eq, ":loop_var", "trp_kingdom_heroes_including_player_begin"),
              (assign, ":cur_troop", "trp_player"),
              (assign, ":troop_faction", "$players_kingdom"),
            (else_try),
              (store_troop_faction, ":troop_faction", ":cur_troop"),
            (try_end),
            (eq, ":troop_faction", ":faction_no"),
            (neq, ":cur_troop", ":faction_leader"),
            (troop_slot_eq, ":cur_troop", slot_troop_occupation, slto_kingdom_hero),
            (try_begin),
              (eq, ":num_members", 0),
              (str_store_troop_name_link, s10, ":cur_troop"),
            (else_try),
              (eq, ":num_members", 1),
              (str_store_troop_name_link, s9, ":cur_troop"),
              (str_store_string, s10, "@{s9} and {s10}"),
            (else_try),
              (str_store_troop_name_link, s9, ":cur_troop"),
              (str_store_string, s10, "@{!}{s9}, {s10}"),
            (try_end),
            (val_add, ":num_members", 1),
          (try_end),
              
              #wars
          (str_store_string, s12, "@noone"),
   #       (assign, ":num_enemies", 0),
   #       (try_for_range_backwards, ":cur_faction", kingdoms_begin, kingdoms_end),
   #         (faction_slot_eq, ":cur_faction", slot_faction_state, sfs_active),
   #         (store_relation, ":cur_relation", ":cur_faction", ":faction_no"),
   #         (lt, ":cur_relation", 0),
   #         (try_begin),
   #           (eq, ":num_enemies", 0),
   #           (str_store_faction_name_link, s12, ":cur_faction"),
   #         (else_try),
   #           (eq, ":num_enemies", 1),
   #           (str_store_faction_name_link, s11, ":cur_faction"),
   #           (str_store_string, s12, "@the {s11} and the {s12}"),
   #         (else_try),
   #           (str_store_faction_name_link, s11, ":cur_faction"),
   #           (str_store_string, s12, "@the {s11}, the {s12}"),
   #         (try_end),
   #         (val_add, ":num_enemies", 1),
   #       (try_end),
              
          (str_store_string, s21, "str_foreign_relations__"),
              
              #other foreign relations
          (try_for_range, ":cur_faction", kingdoms_begin, kingdoms_end),
            (faction_slot_eq, ":cur_faction", slot_faction_state, sfs_active),
            (neq, ":faction_no", ":cur_faction"),
            (str_store_faction_name_link, s14, ":cur_faction"),
            (call_script, "script_diplomacy_faction_get_diplomatic_status_with_faction", ":faction_no", ":cur_faction"),
            (assign, ":diplomatic_status", reg0),
			(assign, ":duration_of_status", reg1),
			
            (call_script, "script_diplomacy_faction_get_diplomatic_status_with_faction", ":cur_faction", ":faction_no"),
            (assign, ":reverse_diplomatic_status", reg0),
#			(assign, ":reverse_diplomatic_duration", reg1),

            (try_begin),
              (eq, ":diplomatic_status", -2),
              (str_store_string, s21, "str_s21__the_s5_is_at_war_with_the_s14"),
              (store_add, ":slot_war_damage_inflicted", ":cur_faction", slot_faction_war_damage_inflicted_on_factions_begin),
              (val_sub, ":slot_war_damage_inflicted", kingdoms_begin),
              (faction_get_slot, ":war_damage_inflicted", ":faction_no", ":slot_war_damage_inflicted"),
              (store_mul, ":war_damage_inflicted_x_2", ":war_damage_inflicted", 2),

              (store_add, ":slot_war_damage_suffered", ":faction_no", slot_faction_war_damage_inflicted_on_factions_begin),
              (val_sub, ":slot_war_damage_suffered", kingdoms_begin),
              (faction_get_slot, ":war_damage_suffered", ":cur_faction", ":slot_war_damage_suffered"),
              (store_mul, ":war_damage_suffered_x_2", ":war_damage_suffered", 2),
			  
			  
			  (assign, ":war_cause", 0),
			  (assign, ":attacker", 0),
			  (try_for_range, ":log_entry", 0, "$num_log_entries"),
				(troop_get_slot, ":type", "trp_log_array_entry_type", ":log_entry"),
				(is_between, ":type", logent_faction_declares_war_out_of_personal_enmity, logent_war_declaration_types_end),
				(troop_get_slot, ":actor", "trp_log_array_actor", ":log_entry"),
				(troop_get_slot, ":object", "trp_log_array_faction_object", ":log_entry"),

				(try_begin),
					(eq, ":actor", ":cur_faction"),
					(eq, ":object", ":faction_no"),
					(assign, ":war_cause", ":type"),
					(assign, ":attacker", ":actor"),
				(else_try),	
					(eq, ":actor", ":faction_no"),
					(eq, ":object", ":cur_faction"),
					(assign, ":war_cause", ":type"),
					(assign, ":attacker", ":actor"),
				(try_end),
			  (try_end),	

			  #bug fix! backing up s8 to somewhere else
                          (str_store_string, s25, s8),
			  (try_begin),
			    (gt, ":war_cause", 0),
				(str_store_faction_name, s8, ":attacker"),
				(try_begin),
					(eq, ":war_cause", logent_faction_declares_war_out_of_personal_enmity),
					(str_store_string, s21, "str_s21_the_s8_declared_war_out_of_personal_enmity"),
				(else_try),			
					(eq, ":war_cause", logent_faction_declares_war_to_respond_to_provocation),
					(str_store_string, s21, "str_s21_the_s8_declared_war_in_response_to_border_provocations"),
				(else_try),			
					(eq, ":war_cause", logent_faction_declares_war_to_curb_power),
					(str_store_string, s21, "str_s21_the_s8_declared_war_to_curb_the_other_realms_power"),
				(else_try),	
					(eq, ":war_cause", logent_faction_declares_war_to_regain_territory),
					(str_store_string, s21, "str_s21_the_s8_declared_war_to_regain_lost_territory"),
				##diplomacy begin
				(else_try),
					(eq, ":war_cause", logent_faction_declares_war_to_fulfil_pact),
					(str_store_string, s21, "str_dplmc_s21_the_s8_declared_war_to_fulfil_pact"),
				##diplomacy end
				(else_try),
					(eq, ":war_cause", logent_player_faction_declares_war),
					(neq, ":attacker", "fac_player_supporters_faction"),
					(str_store_string, s21, "str_s21_the_s8_declared_war_as_part_of_a_bid_to_conquer_all_calradia"),
				(try_end),
			  (try_end),
			  #bug fix! restoring the back up to s8
                          (str_store_string, s8, s25),

              (try_begin),
                (gt, ":war_damage_inflicted", ":war_damage_suffered_x_2"),
                (str_store_string, s21, "str_s21_the_s5_has_had_the_upper_hand_in_the_fighting"),
              (else_try),
                (gt, ":war_damage_suffered", ":war_damage_inflicted_x_2"),
                (str_store_string, s21, "str_s21_the_s5_has_gotten_the_worst_of_the_fighting"),
              (else_try),
			    #gekokujo 3.0 new strategic ai start
                (gt, ":war_damage_inflicted", 150),
                #(gt, ":war_damage_inflicted", 100),
                #(gt, ":war_damage_inflicted", 100),
			    #gekokujo 3.0 new strategic ai end
                (str_store_string, s21, "str_s21_the_fighting_has_gone_on_for_some_time_and_the_war_may_end_soon_with_a_truce"),
              (else_try),
                (str_store_string, s21, "str_s21_the_fighting_has_begun_relatively_recently_and_the_war_may_continue_for_some_time"),
              (try_end),
              (try_begin),
                (eq, "$cheat_mode", 1),
                (assign, reg4, ":war_damage_inflicted"),
                (assign, reg5, ":war_damage_suffered"),
                (str_store_string, s21, "str_s21_reg4reg5"),
              (try_end),
            (else_try),
              (eq, ":diplomatic_status", 1),
              (str_clear, s18),
              (try_begin),
                (neq, ":reverse_diplomatic_status", 1),
                (str_store_string, s18, "str__however_the_truce_is_no_longer_binding_on_the_s14"),
              (try_end),
			  (assign, reg1, ":duration_of_status"),
			  ##diplomacy begin
              (try_begin),
			    ##nested diplomacy start+ Use named variables for truce lengths
                #(is_between, ":duration_of_status", 1, 21),
				(is_between, ":duration_of_status", dplmc_treaty_truce_days_expire + 1, dplmc_treaty_truce_days_initial + 1),
				##nested diplomacy end+
              ##diplomacy end
              (str_store_string, s21, "str_s21__the_s5_is_bound_by_truce_not_to_attack_the_s14s18_the_truce_will_expire_in_reg1_days"),
              ##diplomacy begin
			  ##nested diplomacy start+ Use named variables for truce lengths
              (else_try),
                #(is_between, ":duration_of_status", 21, 41),
                #(val_sub, reg1, 20),
                (is_between, ":duration_of_status", dplmc_treaty_trade_days_expire + 1, dplmc_treaty_trade_days_initial + 1),
                (val_sub, reg1, dplmc_treaty_trade_days_expire),
                (str_store_string, s21, "str_dplmc_s21__the_s5_is_bound_by_trade_not_to_attack_the_s14s18_it_will_expire_in_reg1_days"),
              (else_try),
                #(is_between, ":duration_of_status", 41, 61),
                #(val_sub, reg1, 40),
                (is_between, ":duration_of_status", dplmc_treaty_defense_days_expire + 1, dplmc_treaty_defense_days_initial + 1),
                (val_sub, reg1, dplmc_treaty_defense_days_expire),
                (str_store_string, s21, "str_dplmc_s21__the_s5_is_bound_by_defensive_not_to_attack_the_s14s18_it_will_expire_in_reg1_days"),
              (else_try),
                #(is_between, ":duration_of_status", 61, 81),
                #(val_sub, reg1, 60),
                (is_between, ":duration_of_status", dplmc_treaty_alliance_days_expire + 1, dplmc_treaty_alliance_days_initial + 1),
                (val_sub, reg1, dplmc_treaty_alliance_days_expire),
                (str_store_string, s21, "str_dplmc_s21__the_s5_is_bound_by_alliance_not_to_attack_the_s14s18_it_will_expire_in_reg1_days"),
              (try_end),
			  ##nested diplomacy end+ (Use named variables for truce lengths)
               ##diplomacy end
            (else_try),
              (eq, ":diplomatic_status", -1),
              (str_store_string, s21, "str_s21__the_s5_has_recently_suffered_provocation_by_subjects_of_the_s14_and_there_is_a_risk_of_war"),
            (else_try),
              (eq, ":diplomatic_status", 0),
              (str_store_string, s21, "str_s21__the_s5_has_no_outstanding_issues_with_the_s14"),
            (try_end),
            (try_begin),
              (eq, ":reverse_diplomatic_status", -1),
              (str_store_string, s21, "str_s21_the_s14_was_recently_provoked_by_subjects_of_the_s5_and_there_is_a_risk_of_war_"),
            (try_end),
            (try_begin),
              (eq, "$cheat_mode", 1),
              (call_script, "script_npc_decision_checklist_peace_or_war", ":faction_no", ":cur_faction", -1),
			  (str_store_string, s21, "@{!}DEBUG : {s21}.^CHEAT MODE ASSESSMENT: {s14}^"), 
            (try_end),
          (try_end),
          (str_store_string, s0, "str_the_s5_is_ruled_by_s6_it_occupies_s8_its_vassals_are_s10__s21", 0),
          (set_trigger_result, 1),
        (try_end),
      (else_try),
        (is_between, ":faction_no", kingdoms_begin, kingdoms_end),
        (faction_slot_eq, ":faction_no", slot_faction_state, sfs_defeated),
        (try_begin),
          (eq, ":note_index", 0),
          (str_store_faction_name, s5, ":faction_no"),
          (str_store_string, s0, "@{s5} has been defeated!", 0),
          (set_trigger_result, 1),
        (else_try),
          (eq, ":note_index", 1),
          (str_clear, s0),
          (set_trigger_result, 1),
        (try_end),
      (else_try),
        (try_begin),
          (this_or_next|eq, ":note_index", 0),
          (eq, ":note_index", 1),
          (str_clear, s0),
          (set_trigger_result, 1),
        (try_end),
      (try_end),
     ]),
  #script_game_get_quest_note
  # This script is called from the game engine when the notes of a quest is needed.
  # INPUT: arg1 = quest_no, arg2 = note_index
  # OUTPUT: s0 = note
  ("game_get_quest_note",
    [
##      (store_script_param_1, ":quest_no"),
##      (store_script_param_2, ":note_index"),
      (set_trigger_result, 0), # set it to 1 if this script is wanted to be used rather than static notes
     ]),
  #script_game_get_info_page_note
  # This script is called from the game engine when the notes of a info_page is needed.
  # INPUT: arg1 = info_page_no, arg2 = note_index
  # OUTPUT: s0 = note
  ("game_get_info_page_note",
    [
##      (store_script_param_1, ":info_page_no"),
##      (store_script_param_2, ":note_index"),
      (set_trigger_result, 0), # set it to 1 if this script is wanted to be used rather than static notes
     ]),
  #script_game_get_scene_name
  # This script is called from the game engine when a name for the scene is needed.
  # INPUT: arg1 = scene_no
  # OUTPUT: s0 = name
  ("game_get_scene_name",
    [
      (store_script_param, ":scene_no", 1),
      (try_begin),
        (is_between, ":scene_no", multiplayer_scenes_begin, multiplayer_scenes_end),
        (store_sub, ":string_id", ":scene_no", multiplayer_scenes_begin),
        (val_add, ":string_id", multiplayer_scene_names_begin),
        (str_store_string, s0, ":string_id"),
      (try_end),
     ]),
  #script_game_get_mission_template_name
  # This script is called from the game engine when a name for the mission template is needed.
  # INPUT: arg1 = mission_template_no
  # OUTPUT: s0 = name
  ("game_get_mission_template_name",
    [
      (store_script_param, ":mission_template_no", 1),
      (call_script, "script_multiplayer_get_mission_template_game_type", ":mission_template_no"),
      (assign, ":game_type", reg0),
      (try_begin),
        (is_between, ":game_type", 0, multiplayer_num_game_types),
        (store_add, ":string_id", ":game_type", multiplayer_game_type_names_begin),
        (str_store_string, s0, ":string_id"),
      (try_end),
     ]),
  #script_add_kill_death_counts
  # INPUT: arg1 = killer_agent_no, arg2 = dead_agent_no
  # OUTPUT: none
  ("add_kill_death_counts",
   [
      (store_script_param, ":killer_agent_no", 1),
      (store_script_param, ":dead_agent_no", 2),
      
      (try_begin),
        (ge, ":killer_agent_no", 0),
        (agent_get_team, ":killer_agent_team", ":killer_agent_no"),
      (else_try),
        (assign, ":killer_agent_team", -1),
      (try_end),

      (try_begin),
        (ge, ":dead_agent_no", 0),
        (agent_get_team, ":dead_agent_team", ":dead_agent_no"),
      (else_try),
        (assign, ":dead_agent_team", -1),
      (try_end),
      
      #adjusting kill counts of players/bots
      (try_begin), 
        (try_begin), 
          (ge, ":killer_agent_no", 0),
          (ge, ":dead_agent_no", 0),
          (agent_is_human, ":killer_agent_no"),
          (agent_is_human, ":dead_agent_no"),
          (neq, ":killer_agent_no", ":dead_agent_no"),
          
          (this_or_next|neq, ":killer_agent_team", ":dead_agent_team"),
          (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_deathmatch),
          (eq, "$g_multiplayer_game_type", multiplayer_game_type_duel),
          
          (agent_get_player_id, ":killer_agent_player", ":killer_agent_no"),
          (try_begin),
            (agent_is_non_player, ":killer_agent_no"), #if killer agent is bot then increase bot kill counts of killer agent's team by one.
            (agent_get_team, ":killer_agent_team", ":killer_agent_no"),
            (team_get_bot_kill_count, ":killer_agent_team_bot_kill_count", ":killer_agent_team"),
            (val_add, ":killer_agent_team_bot_kill_count", 1),
            (team_set_bot_kill_count, ":killer_agent_team", ":killer_agent_team_bot_kill_count"),            
          (else_try), #if killer agent is not bot then increase kill counts of killer agent's player by one.
            (player_is_active, ":killer_agent_player"),
            (player_get_kill_count, ":killer_agent_player_kill_count", ":killer_agent_player"),
            (val_add, ":killer_agent_player_kill_count", 1),
            (player_set_kill_count, ":killer_agent_player", ":killer_agent_player_kill_count"),
          (try_end),
        (try_end),           

        (try_begin), 
          (ge, ":dead_agent_no", 0),
          (agent_is_human, ":dead_agent_no"),
          (try_begin),
            (agent_is_non_player, ":dead_agent_no"), #if dead agent is bot then increase bot kill counts of dead agent's team by one.
            (agent_get_team, ":dead_agent_team", ":dead_agent_no"),
            (team_get_bot_death_count, ":dead_agent_team_bot_death_count", ":dead_agent_team"),
            (val_add, ":dead_agent_team_bot_death_count", 1),
            (team_set_bot_death_count, ":dead_agent_team", ":dead_agent_team_bot_death_count"),
          (else_try), #if dead agent is not bot then increase death counts of dead agent's player by one.
            (agent_get_player_id, ":dead_agent_player", ":dead_agent_no"),
            (player_is_active, ":dead_agent_player"),
            (player_get_death_count, ":dead_agent_player_death_count", ":dead_agent_player"),
            (val_add, ":dead_agent_player_death_count", 1),
            (player_set_death_count, ":dead_agent_player", ":dead_agent_player_death_count"),
          (try_end),

          (try_begin),
            (assign, ":continue", 0),
      
            (try_begin),
              (this_or_next|lt, ":killer_agent_no", 0), #if he killed himself (1a(team change) or 1b(self kill)) then decrease kill counts of killer player by one.
              (eq, ":killer_agent_no", ":dead_agent_no"),
              (assign, ":continue", 1),
            (try_end),

            (try_begin),
              (eq, ":killer_agent_team", ":dead_agent_team"), #if he killed a teammate and game mod is not deathmatch then decrease kill counts of killer player by one.
              (neq, "$g_multiplayer_game_type", multiplayer_game_type_deathmatch),
              (neq, "$g_multiplayer_game_type", multiplayer_game_type_duel),
              (assign, ":continue", 1),
            (try_end),

            (eq, ":continue", 1),
                    
            (try_begin),
              (ge, ":killer_agent_no", 0),
              (assign, ":responsible_agent", ":killer_agent_no"),                
            (else_try),
              (assign, ":responsible_agent", ":dead_agent_no"),
            (try_end),

            (try_begin),
              (ge, ":responsible_agent", 0),
              (neg|agent_is_non_player, ":responsible_agent"),
              (agent_get_player_id, ":responsible_player", ":responsible_agent"),
              (ge, ":responsible_player", 0),
              (player_get_kill_count, ":dead_agent_player_kill_count", ":responsible_player"),
              (val_add, ":dead_agent_player_kill_count", -1),
              (player_set_kill_count, ":responsible_player", ":dead_agent_player_kill_count"),
            (try_end),
          (try_end),               
        (try_end),
      (try_end),
    ]),
  #script_warn_player_about_auto_team_balance
  # INPUT: none
  # OUTPUT: none
  ("warn_player_about_auto_team_balance",
   [
     (assign, "$g_multiplayer_message_type", multiplayer_message_type_auto_team_balance_next),
     (start_presentation, "prsnt_multiplayer_message_2"),
     ]),
  #script_check_team_balance
  # INPUT: none
  # OUTPUT: none
  ("check_team_balance",
   [
     (try_begin),
       (multiplayer_is_server),
  
       (assign, ":number_of_players_at_team_1", 0),
       (assign, ":number_of_players_at_team_2", 0),
       (get_max_players, ":num_players"),
       (try_for_range, ":cur_player", 0, ":num_players"),
         (player_is_active, ":cur_player"),
         (player_get_team_no, ":player_team", ":cur_player"),
         (try_begin),
           (eq, ":player_team", 0),
           (val_add, ":number_of_players_at_team_1", 1),
         (else_try),
           (eq, ":player_team", 1),
           (val_add, ":number_of_players_at_team_2", 1),
         (try_end),         
       (try_end),
 
       (store_sub, ":difference_of_number_of_players", ":number_of_players_at_team_1", ":number_of_players_at_team_2"),
       (assign, ":number_of_players_will_be_moved", 0),
       (try_begin),
         (try_begin),
           (store_mul, ":checked_value", "$g_multiplayer_auto_team_balance_limit", -1),
           (le, ":difference_of_number_of_players", ":checked_value"),
           (store_div, ":number_of_players_will_be_moved", ":difference_of_number_of_players", -2),
           (assign, ":team_with_more_players", 1),
           (assign, ":team_with_less_players", 0),
         (else_try),
           (ge, ":difference_of_number_of_players", "$g_multiplayer_auto_team_balance_limit"),
           (store_div, ":number_of_players_will_be_moved", ":difference_of_number_of_players", 2),
           (assign, ":team_with_more_players", 0),
           (assign, ":team_with_less_players", 1),
         (try_end),          
       (try_end),         
       #team balance checks are done
       (try_begin),
         (gt, ":number_of_players_will_be_moved", 0),
         (try_begin),
           (eq, "$g_team_balance_next_round", 1), #if warning is given
           
           #auto team balance starts
           (try_for_range, ":unused", 0, ":number_of_players_will_be_moved"), 
             (assign, ":max_player_join_time", 0),
             (assign, ":latest_joined_player_no", -1),
             (get_max_players, ":num_players"),                               
             (try_for_range, ":player_no", 0, ":num_players"),
               (player_is_active, ":player_no"),
               (player_get_team_no, ":player_team", ":player_no"),
               (eq, ":player_team", ":team_with_more_players"),
               (player_get_slot, ":player_join_time", ":player_no", slot_player_join_time),
               (try_begin),
                 (gt, ":player_join_time", ":max_player_join_time"),
                 (assign, ":max_player_join_time", ":player_join_time"),
                 (assign, ":latest_joined_player_no", ":player_no"),
               (try_end),
             (try_end),
             (try_begin),
               (ge, ":latest_joined_player_no", 0),
               (try_begin),
                 #if player is living add +1 to his kill count because he will get -1 because of team change while living.
                 (player_get_agent_id, ":latest_joined_agent_id", ":latest_joined_player_no"), 
                 (ge, ":latest_joined_agent_id", 0),
                 (agent_is_alive, ":latest_joined_agent_id"),

                 (player_get_kill_count, ":player_kill_count", ":latest_joined_player_no"), #adding 1 to his kill count, because he will lose 1 undeserved kill count for dying during team change
                 (val_add, ":player_kill_count", 1),
                 (player_set_kill_count, ":latest_joined_player_no", ":player_kill_count"),

                 (player_get_death_count, ":player_death_count", ":latest_joined_player_no"), #subtracting 1 to his death count, because he will gain 1 undeserved death count for dying during team change
                 (val_sub, ":player_death_count", 1),
                 (player_set_death_count, ":latest_joined_player_no", ":player_death_count"),

                 (player_get_score, ":player_score", ":latest_joined_player_no"), #adding 1 to his score count, because he will lose 1 undeserved score for dying during team change
                 (val_add, ":player_score", 1),
                 (player_set_score, ":latest_joined_player_no", ":player_score"),

                 (try_for_range, ":player_no", 1, ":num_players"), #0 is server so starting from 1
                   (player_is_active, ":player_no"),
                   (multiplayer_send_4_int_to_player, ":player_no", multiplayer_event_set_player_score_kill_death, ":latest_joined_player_no", ":player_score", ":player_kill_count", ":player_death_count"),
                 (try_end),

                 (player_get_value_of_original_items, ":old_items_value", ":latest_joined_player_no"),
                 (player_get_gold, ":player_gold", ":latest_joined_player_no"),
                 (val_add, ":player_gold", ":old_items_value"),
                 (player_set_gold, ":latest_joined_player_no", ":player_gold", multi_max_gold_that_can_be_stored),
               (end_try),

               (player_set_troop_id, ":latest_joined_player_no", -1),
               (player_set_team_no, ":latest_joined_player_no", ":team_with_less_players"),
               (multiplayer_send_message_to_player, ":latest_joined_player_no", multiplayer_event_force_start_team_selection),
             (try_end),
           (try_end),
     
           #for only server itself-----------------------------------------------------------------------------------------------
           (call_script, "script_show_multiplayer_message", multiplayer_message_type_auto_team_balance_done, 0), #0 is useless here
           #for only server itself-----------------------------------------------------------------------------------------------     
           (get_max_players, ":num_players"),                               
           (try_for_range, ":player_no", 1, ":num_players"),
             (player_is_active, ":player_no"),
             (multiplayer_send_int_to_player, ":player_no", multiplayer_event_show_multiplayer_message, multiplayer_message_type_auto_team_balance_done), 
           (try_end),
           (assign, "$g_team_balance_next_round", 0),
           #auto team balance done
         (else_try),
           #tutorial message (next round there will be auto team balance)
           (assign, "$g_team_balance_next_round", 1),
     
           #for only server itself-----------------------------------------------------------------------------------------------
           (call_script, "script_show_multiplayer_message", multiplayer_message_type_auto_team_balance_next, 0), #0 is useless here
           #for only server itself-----------------------------------------------------------------------------------------------     
           (get_max_players, ":num_players"),                               
           (try_for_range, ":player_no", 1, ":num_players"),
             (player_is_active, ":player_no"),
             (multiplayer_send_int_to_player, ":player_no", multiplayer_event_show_multiplayer_message, multiplayer_message_type_auto_team_balance_next), 
           (try_end),
         (try_end),
       (else_try),
         (assign, "$g_team_balance_next_round", 0),
       (try_end),
     (try_end),
   ]),
  #script_check_creating_ladder_dust_effect
  # INPUT: arg1 = instance_id, arg2 = remaining_time
  # OUTPUT: none
  ("check_creating_ladder_dust_effect",
   [
      (store_trigger_param_1, ":instance_id"),
      (store_trigger_param_2, ":remaining_time"),

      (try_begin),
        (lt, ":remaining_time", 15), #less then 0.15 seconds
        (gt, ":remaining_time", 3), #more than 0.03 seconds
      
        (scene_prop_get_slot, ":smoke_effect_done", ":instance_id", scene_prop_smoke_effect_done),
        (scene_prop_get_slot, ":opened_or_closed", ":instance_id", scene_prop_open_or_close_slot),

        (try_begin),
          (eq, ":smoke_effect_done", 0),
          (eq, ":opened_or_closed", 0),
      
          (prop_instance_get_position, pos0, ":instance_id"),

          (assign, ":smallest_dist", -1),
          (try_for_range, ":entry_point_no", multi_entry_points_for_usable_items_start, multi_entry_points_for_usable_items_end),
            (entry_point_get_position, pos1, ":entry_point_no"),
            (get_sq_distance_between_positions, ":dist", pos0, pos1),
            (this_or_next|eq, ":smallest_dist", -1),
            (lt, ":dist", ":smallest_dist"),
            (assign, ":smallest_dist", ":dist"),
            (assign, ":nearest_entry_point", ":entry_point_no"),
          (try_end),

          (try_begin),
            (set_fixed_point_multiplier, 100),

            (ge, ":smallest_dist", 0),
            (lt, ":smallest_dist", 22500), #max 15m distance
      
            (entry_point_get_position, pos1, ":nearest_entry_point"),
            (position_rotate_x, pos1, -90),

            (prop_instance_get_scene_prop_kind, ":scene_prop_kind", ":instance_id"),
            (try_begin),
              (eq, ":scene_prop_kind", "spr_siege_ladder_move_6m"),              
              (init_position, pos2),
              (position_set_z, pos2, 300),
              (position_transform_position_to_parent, pos3, pos1, pos2),
              (particle_system_burst, "psys_ladder_dust_6m", pos3, 100),
              (particle_system_burst, "psys_ladder_straw_6m", pos3, 100),
            (else_try),
              (eq, ":scene_prop_kind", "spr_siege_ladder_move_8m"),
              (init_position, pos2),
              (position_set_z, pos2, 400),
              (position_transform_position_to_parent, pos3, pos1, pos2),
              (particle_system_burst, "psys_ladder_dust_8m", pos3, 100),
              (particle_system_burst, "psys_ladder_straw_8m", pos3, 100),
            (else_try),
              (eq, ":scene_prop_kind", "spr_siege_ladder_move_10m"),
              (init_position, pos2),
              (position_set_z, pos2, 500),
              (position_transform_position_to_parent, pos3, pos1, pos2),
              (particle_system_burst, "psys_ladder_dust_10m", pos3, 100),
              (particle_system_burst, "psys_ladder_straw_10m", pos3, 100),
            (else_try),
              (eq, ":scene_prop_kind", "spr_siege_ladder_move_12m"),
              (init_position, pos2),
              (position_set_z, pos2, 600),
              (position_transform_position_to_parent, pos3, pos1, pos2),
              (particle_system_burst, "psys_ladder_dust_12m", pos3, 100),
              (particle_system_burst, "psys_ladder_straw_12m", pos3, 100),
            (else_try),
              (eq, ":scene_prop_kind", "spr_siege_ladder_move_14m"),
              (init_position, pos2),
              (position_set_z, pos2, 700),
              (position_transform_position_to_parent, pos3, pos1, pos2),
              (particle_system_burst, "psys_ladder_dust_14m", pos3, 100),
              (particle_system_burst, "psys_ladder_straw_14m", pos3, 100),
            (try_end),

            (scene_prop_set_slot, ":instance_id", scene_prop_smoke_effect_done, 1),
          (try_end),
        (try_end),
      (try_end),
      ]),
  #script_money_management_after_agent_death
  # INPUT: arg1 = killer_agent_no, arg2 = dead_agent_no
  # OUTPUT: none
  ("money_management_after_agent_death",
   [
     (store_script_param, ":killer_agent_no", 1),
     (store_script_param, ":dead_agent_no", 2),

     (assign, ":dead_agent_player_id", -1),

     (try_begin),
       (multiplayer_is_server),
       (ge, ":killer_agent_no", 0),
       (ge, ":dead_agent_no", 0),
       (agent_is_human, ":dead_agent_no"), #if dead agent is not horse
       (agent_is_human, ":killer_agent_no"), #if killer agent is not horse
       (agent_get_team, ":killer_agent_team", ":killer_agent_no"),
       (agent_get_team, ":dead_agent_team", ":dead_agent_no"),
     
       (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_deathmatch),
       (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_duel),
       (neq, ":killer_agent_team", ":dead_agent_team"), #if these agents are enemies

       (neq, ":dead_agent_no", ":killer_agent_no"), #if agents are different, do not remove it is needed because in deathmatch mod, self killing passes here because of this or next.
     
       (try_begin),
         (neg|agent_is_non_player, ":dead_agent_no"), 
         (agent_get_player_id, ":dead_player_no", ":dead_agent_no"),
         (player_get_slot, ":dead_agent_equipment_value", ":dead_player_no", slot_player_total_equipment_value),             
       (else_try),
         (assign, ":dead_agent_equipment_value", 0),
       (try_end),

       (assign, ":dead_agent_team_human_players_count", 0),
       (get_max_players, ":num_players"),
       (try_for_range, ":player_no", 0, ":num_players"),
         (player_is_active, ":player_no"),
         (player_get_team_no, ":player_team", ":player_no"),
         (eq, ":player_team", ":dead_agent_team"),
         (val_add, ":dead_agent_team_human_players_count", 1),
       (try_end),
         
       (try_for_range, ":player_no", 0, ":num_players"),
         (player_is_active, ":player_no"),
          
         (try_begin), 
           (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_battle),
           (eq, "$g_multiplayer_game_type", multiplayer_game_type_destroy),
           (assign, ":one_spawn_per_round_game_type", 1),            
         (else_try),
           (assign, ":one_spawn_per_round_game_type", 0),
         (try_end),
         
         (this_or_next|eq, ":one_spawn_per_round_game_type", 0),
         (this_or_next|player_slot_eq, ":player_no", slot_player_spawned_this_round, 0),
         (player_slot_eq, ":player_no", slot_player_spawned_this_round, 1),
         
         (player_get_agent_id, ":agent_no", ":player_no"),
         (try_begin),
           (eq, ":agent_no", ":dead_agent_no"), #if this agent is dead agent then get share from total loot. (20% of total equipment value)                 
           (player_get_gold, ":player_gold", ":player_no"),

           (assign, ":dead_agent_player_id", ":player_no"),
          
           #dead agent loot share (32%-48%-64%, norm : 48%)
           (store_mul, ":share_of_dead_agent", ":dead_agent_equipment_value", multi_dead_agent_loot_percentage_share),
           (val_div, ":share_of_dead_agent", 100),
           (val_mul, ":share_of_dead_agent", "$g_multiplayer_battle_earnings_multiplier"),
           (val_div, ":share_of_dead_agent", 100),
           (try_begin),
             (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_deathmatch), #(4/3x) share if current mod is deathmatch
             (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_duel), #(4/3x) share if current mod is duel
             (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_team_deathmatch), #(4/3x) share if current mod is team_deathmatch
             (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_capture_the_flag), #(4/3x) share if current mod is capture the flag
             (eq, "$g_multiplayer_game_type", multiplayer_game_type_headquarters), #(4/3x) share if current mod is headquarters
             (val_mul, ":share_of_dead_agent", 4),
             (val_div, ":share_of_dead_agent", 3),
             (val_add, ":player_gold", ":share_of_dead_agent"), 
           (else_try),
             (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_battle), #(2/3x) share if current mod is battle 
             (eq, "$g_multiplayer_game_type", multiplayer_game_type_destroy), #(2/3x) share if current mod is fight and destroy
             (val_mul, ":share_of_dead_agent", 2),
             (val_div, ":share_of_dead_agent", 3),
             (val_add, ":player_gold", ":share_of_dead_agent"),
           (else_try),
             (val_add, ":player_gold", ":share_of_dead_agent"), #(3/3x) share if current mod is siege
           (try_end),
           (player_set_gold, ":player_no", ":player_gold", multi_max_gold_that_can_be_stored),
         (else_try),
           (eq, ":agent_no", ":killer_agent_no"), #if this agent is killer agent then get share from total loot. (10% of total equipment value)
           (player_get_gold, ":player_gold", ":player_no"),           

           #killer agent standart money (100-150-200, norm : 150)
           (assign, ":killer_agent_standard_money_addition", multi_killer_agent_standard_money_add),
           (val_mul, ":killer_agent_standard_money_addition", "$g_multiplayer_battle_earnings_multiplier"),
           (val_div, ":killer_agent_standard_money_addition", 100),
           (try_begin),
             (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_deathmatch), #(4/3x) share if current mod is deathmatch
             (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_duel), #(4/3x) share if current mod is duel
             (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_team_deathmatch), #(4/3x) share if current mod is team_deathmatch
             (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_capture_the_flag), #(4/3x) share if current mod is capture the flag
             (eq, "$g_multiplayer_game_type", multiplayer_game_type_headquarters), #(4/3x) share if current mod is headquarters
             (val_mul, ":killer_agent_standard_money_addition", 4),
             (val_div, ":killer_agent_standard_money_addition", 3),
             (val_add, ":player_gold", ":killer_agent_standard_money_addition"), 
           (else_try),
             (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_battle), #(2/3x) share if current mod is battle 
             (eq, "$g_multiplayer_game_type", multiplayer_game_type_destroy), #(2/3x) share if current mod is fight and destroy
             (val_mul, ":killer_agent_standard_money_addition", 2),
             (val_div, ":killer_agent_standard_money_addition", 3),
             (val_add, ":player_gold", ":killer_agent_standard_money_addition"),
           (else_try),
             (val_add, ":player_gold", ":killer_agent_standard_money_addition"), #(3/3x) share if current mod is siege
           (try_end),

           #killer agent loot share (8%-12%-16%, norm : 12%)
           (store_mul, ":share_of_killer_agent", ":dead_agent_equipment_value", multi_killer_agent_loot_percentage_share),
           (val_div, ":share_of_killer_agent", 100),
           (val_mul, ":share_of_killer_agent", "$g_multiplayer_battle_earnings_multiplier"),
           (val_div, ":share_of_killer_agent", 100),
           (try_begin),
             (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_deathmatch), #(4/3x) share if current mod is deathmatch
             (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_duel), #(4/3x) share if current mod is duel
             (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_team_deathmatch), #(4/3x) share if current mod is team_deathmatch
             (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_capture_the_flag), #(4/3x) share if current mod is capture the flag
             (eq, "$g_multiplayer_game_type", multiplayer_game_type_headquarters), #(4/3x) share if current mod is headquarters
             (val_mul, ":share_of_killer_agent", 4),
             (val_div, ":share_of_killer_agent", 3),
             (val_add, ":player_gold", ":share_of_killer_agent"), 
           (else_try),
             (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_battle), #(2/3x) share if current mod is battle 
             (eq, "$g_multiplayer_game_type", multiplayer_game_type_destroy), #(2/3x) share if current mod is fight and destroy
             (val_mul, ":share_of_killer_agent", 2),
             (val_div, ":share_of_killer_agent", 3),
             (val_add, ":player_gold", ":share_of_killer_agent"),
           (else_try),
             (val_add, ":player_gold", ":share_of_killer_agent"), #(3/3x) share if current mod is siege
           (try_end),
           (player_set_gold, ":player_no", ":player_gold", multi_max_gold_that_can_be_stored),
         (try_end),
       (try_end),
     (try_end),

     #(below lines added new at 25.11.09 after Armagan decided new money system)
     (try_begin),
       (multiplayer_is_server),
       (neq, "$g_multiplayer_game_type", multiplayer_game_type_battle),
       (neq, "$g_multiplayer_game_type", multiplayer_game_type_destroy),

       (ge, ":dead_agent_no", 0),
       (agent_is_human, ":dead_agent_no"), #if dead agent is not horse
       (agent_get_player_id, ":dead_agent_player_id", ":dead_agent_no"),
       (ge, ":dead_agent_player_id", 0),
     
       (player_get_gold, ":player_gold", ":dead_agent_player_id"),
       (try_begin),
         (store_mul, ":minimum_gold", "$g_multiplayer_initial_gold_multiplier", 10),
         (lt, ":player_gold", ":minimum_gold"),
         (assign, ":player_gold", ":minimum_gold"),
       (try_end),
       (player_set_gold, ":dead_agent_player_id", ":player_gold"),
     (try_end),
     #new money system addition end          
     ]),
	("initialize_aristocracy",
	[
	  #LORD OCCUPATIONS, BLOOD RELATIONSHIPS, RENOWN AND REPUTATIONS
	  
	  #King ages
	  (try_for_range, ":cur_troop", kings_begin, kings_end),
		(troop_set_slot, ":cur_troop", slot_troop_occupation, slto_kingdom_hero),
		#(store_random_in_range, ":age", 18, 64),
		#(troop_set_slot, ":cur_troop", slot_troop_age, ":age"),
		
		#gekokujo 3.0 some lords have fixed ages
		(try_begin),
      (eq, ":cur_troop", "trp_kingdom_1_lord"),
      (assign, ":age", 32),
    (else_try),
      (eq, ":cur_troop", "trp_kingdom_2_lord"),
      (assign, ":age", 43),
    (else_try),
      (eq, ":cur_troop", "trp_kingdom_3_lord"),
      (assign, ":age", 55),
    (else_try),
      (eq, ":cur_troop", "trp_kingdom_4_lord"),
      (assign, ":age", 49),
    (else_try),
      (eq, ":cur_troop", "trp_kingdom_5_lord"),
      (assign, ":age", 32),
    (else_try),
      (eq, ":cur_troop", "trp_kingdom_6_lord"),
      (assign, ":age", 31),
    (else_try),
      (eq, ":cur_troop", "trp_kingdom_7_lord"),
      (assign, ":age", 24),
    (else_try),
      (eq, ":cur_troop", "trp_kingdom_8_lord"),
      (assign, ":age", 31),
    (else_try),
      (eq, ":cur_troop", "trp_kingdom_9_lord"),
      (assign, ":age", 57),
    (else_try),
      (eq, ":cur_troop", "trp_kingdom_10_lord"),
      (assign, ":age", 41),
    (else_try),
      (eq, ":cur_troop", "trp_kingdom_11_lord"),
      (assign, ":age", 11),
    (else_try),
      (eq, ":cur_troop", "trp_kingdom_12_lord"),
      (assign, ":age", 41),
    (else_try),
      (eq, ":cur_troop", "trp_kingdom_13_lord"),
      (assign, ":age", 56),
    (else_try),
      (eq, ":cur_troop", "trp_kingdom_14_lord"),
      (assign, ":age", 48),
    (else_try),
      (eq, ":cur_troop", "trp_kingdom_15_lord"),
      (assign, ":age", 28),
    (else_try),
      (eq, ":cur_troop", "trp_kingdom_16_lord"),
      (assign, ":age", 22),
    (else_try),
      (eq, ":cur_troop", "trp_kingdom_17_lord"),
      (assign, ":age", 36),
    (else_try),
      (eq, ":cur_troop", "trp_kingdom_18_lord"),
      (assign, ":age", 24),
    (else_try),
      (eq, ":cur_troop", "trp_kingdom_19_lord"),
      (assign, ":age", 29),
    (else_try),
      (eq, ":cur_troop", "trp_kingdom_20_lord"),
      (assign, ":age", 38),
    (else_try),
      (eq, ":cur_troop", "trp_kingdom_21_lord"),
      (assign, ":age", 33),
    (else_try),
      (eq, ":cur_troop", "trp_kingdom_22_lord"),
      (assign, ":age", 23),
    (else_try),
      (eq, ":cur_troop", "trp_kingdom_23_lord"),
      (assign, ":age", 44),
    (else_try),
      (eq, ":cur_troop", "trp_kingdom_24_lord"),
      (assign, ":age", 22),
    (else_try),
      (eq, ":cur_troop", "trp_kingdom_25_lord"),
      (assign, ":age", 15),
    (else_try),
      (eq, ":cur_troop", "trp_kingdom_26_lord"),
      (assign, ":age", 43),
    (else_try),
      (eq, ":cur_troop", "trp_kingdom_27_lord"),
      (assign, ":age", 20),
    (else_try),
      (eq, ":cur_troop", "trp_kingdom_28_lord"),
      (assign, ":age", 33),
    (else_try),
      (store_random_in_range, ":age", 18, 64),
		(try_end),
		(call_script, "script_init_troop_age", ":cur_troop", ":age"),
		#gekokujo kingdom_5_lord age not set
		#(eq, ":cur_troop", "trp_kingdom_5_lord"),
		#(troop_set_slot, ":cur_troop", slot_troop_age, 47),	
	  (try_end),
	  	  
	  #The first thing - family structure
	  #lords 1 to 8 are patriarchs with one live-at-home son and one daughter. They come from one of six possible ancestors, thus making it likely that there will be two sets of siblings
	  #lords 9 to 12 are unmarried landowners with sisters
	  #lords 13 to 20 are sons who still live in their fathers' houses
	  #For the sake of simplicity, we can assume that all male aristocrats in prior generations either married commoners or procured their brides from the Old Country, thus discounting intermarriage 
	  
	  #Gekokujo 1.x family structure
	  #father, son, then single sequence (max 8 -- 3 fathers, 3 sons, 2 singles, 3 wives, 3 daughters, 2 sisters)
	  #"fathers" might not have sons or daughters
	  
	  #Gekokujo 2.x family structure
	  #random age for everyone
	  #lord/lady pairs are close in age
	  #wife/sister possible
	  
	  (try_for_range, ":cur_troop", kingdom_ladies_begin, kingdom_ladies_end),
		(troop_set_slot, ":cur_troop", slot_troop_occupation, slto_kingdom_lady),
	  (try_end),
	  
	  (assign, ":cur_lady", "trp_kingdom_1_lady_1"),

	  (try_for_range, ":cur_troop", lords_begin, lords_end),  
		(troop_set_slot, ":cur_troop", slot_troop_occupation, slto_kingdom_hero),
		
#		(store_random_in_range, ":father_age_at_birth", 23, 26),
#		(store_random_in_range, ":mother_age_at_birth", 19, 22),

		#Gekokujo - added :max_troops variable to help count eligible 'child' slots for 'father' lords
		#:max_troops is 1 less than real maximum number of troops (is compared to npc_seed)
		
		# (try_begin), #uesugi clan
		# 	(is_between, ":cur_troop", "trp_knight_1_1", "trp_knight_2_1"),
		# 	#(store_sub, ":npc_seed", ":cur_troop", "trp_knight_1_1"),
		# 	#(assign, ":max_troops", 9),
		# 	(assign, ":ancestor_seed", 1),

		# (else_try), #date clan
		# 	(is_between, ":cur_troop", "trp_knight_2_1", "trp_knight_3_1"),
		# 	#(store_sub, ":npc_seed", ":cur_troop", "trp_knight_2_1"),
		# 	#(assign, ":max_troops", 7),
		# 	(assign, ":ancestor_seed", 11),
			
		# (else_try), #oda clan
		# 	(is_between, ":cur_troop", "trp_knight_3_1", "trp_knight_4_1"),
		# 	#(store_sub, ":npc_seed", ":cur_troop", "trp_knight_3_1"),
		# 	#(assign, ":max_troops", 9),
		# 	(assign, ":ancestor_seed", 21),
			
		# (else_try), #mori clan
		# 	(is_between, ":cur_troop", "trp_knight_4_1", "trp_knight_5_1"),
		# 	#(store_sub, ":npc_seed", ":cur_troop", "trp_knight_4_1"),
		# 	#(assign, ":max_troops", 7),
		# 	(assign, ":ancestor_seed", 31),

		# (else_try), #takeda clan
		# 	(is_between, ":cur_troop", "trp_knight_5_1", "trp_knight_6_1"),
		# 	#(store_sub, ":npc_seed", ":cur_troop", "trp_knight_5_1"),
		# 	#(assign, ":max_troops", 9),
		# 	(assign, ":ancestor_seed", 41),
			
		# (else_try), #tokugawa clan
		# 	(is_between, ":cur_troop", "trp_knight_6_1", "trp_knight_7_1"),
		# 	#(store_sub, ":npc_seed", ":cur_troop", "trp_knight_6_1"),
		# 	#(assign, ":max_troops", 7),
		# 	(assign, ":ancestor_seed", 51),
		
		# (else_try), #miyoshi clan
		# 	(is_between, ":cur_troop", "trp_knight_7_1", "trp_knight_8_1"),
		# 	#(store_sub, ":npc_seed", ":cur_troop", "trp_knight_7_1"),
		# 	#(assign, ":max_troops", 7),
		# 	(assign, ":ancestor_seed", 61),
		
		# (else_try), #amako clan
		# 	(is_between, ":cur_troop", "trp_knight_8_1", "trp_knight_9_1"),
		# 	#(store_sub, ":npc_seed", ":cur_troop", "trp_knight_8_1"),
		# 	#(assign, ":max_troops", 9),
		# 	(assign, ":ancestor_seed", 71),
		
		# (else_try), #otomo clan
		# 	(is_between, ":cur_troop", "trp_knight_9_1", "trp_knight_10_1"),
		# 	#(store_sub, ":npc_seed", ":cur_troop", "trp_knight_9_1"),
		# 	#(assign, ":max_troops", 7),
		# 	(assign, ":ancestor_seed", 81),
		
		# (else_try), #nanbu clan
		# 	(is_between, ":cur_troop", "trp_knight_10_1", "trp_knight_11_1"),
		# 	#(store_sub, ":npc_seed", ":cur_troop", "trp_knight_10_1"),
		# 	#(assign, ":max_troops", 5),
		# 	(assign, ":ancestor_seed", 91),
		
		# (else_try), #asakura clan
		# 	(is_between, ":cur_troop", "trp_knight_11_1", "trp_knight_12_1"),
		# 	#(store_sub, ":npc_seed", ":cur_troop", "trp_knight_11_1"),
		# 	#(assign, ":max_troops", 5),
		# 	(assign, ":ancestor_seed", 101),
		
		# (else_try), #chosokabe clan
		# 	(is_between, ":cur_troop", "trp_knight_12_1", "trp_knight_13_1"),
		# 	#(store_sub, ":npc_seed", ":cur_troop", "trp_knight_12_1"),
		# 	#(assign, ":max_troops", 5),
		# 	(assign, ":ancestor_seed", 111),
		
		# (else_try), #hojo clan
		# 	(is_between, ":cur_troop", "trp_knight_13_1", "trp_knight_14_1"),
		# 	#(store_sub, ":npc_seed", ":cur_troop", "trp_knight_13_1"),
		# 	#(assign, ":max_troops", 7),
		# 	(assign, ":ancestor_seed", 121),
		
		# (else_try), #mogami clan
		# 	(is_between, ":cur_troop", "trp_knight_14_1", "trp_knight_15_1"),
		# 	#(store_sub, ":npc_seed", ":cur_troop", "trp_knight_14_1"),
		# 	#(assign, ":max_troops", 6),
		# 	(assign, ":ancestor_seed", 131),
		
		# (else_try), #shimazu clan
		# 	(is_between, ":cur_troop", "trp_knight_15_1", "trp_knight_16_1"),
		# 	#(store_sub, ":npc_seed", ":cur_troop", "trp_knight_15_1"),
		# 	#(assign, ":max_troops", 7),
		# 	(assign, ":ancestor_seed", 141),
		
		# (else_try), #ryuzoji clan
		# 	(is_between, ":cur_troop", "trp_knight_16_1", "trp_knight_17_1"),
		# 	#(store_sub, ":npc_seed", ":cur_troop", "trp_knight_16_1"),
		# 	#(assign, ":max_troops", 5),
		# 	(assign, ":ancestor_seed", 151),
		
		# (else_try), #satake clan
		# 	(is_between, ":cur_troop", "trp_knight_17_1", "trp_knight_18_1"),
		# 	#(store_sub, ":npc_seed", ":cur_troop", "trp_knight_17_1"),
		# 	#(assign, ":max_troops", 5),
		# 	(assign, ":ancestor_seed", 161),
		
		# (else_try), #satomi clan
		# 	(is_between, ":cur_troop", "trp_knight_18_1", "trp_knight_19_1"),
		# 	#(store_sub, ":npc_seed", ":cur_troop", "trp_knight_18_1"),
		# 	#(assign, ":max_troops", 5),
		# 	(assign, ":ancestor_seed", 171),
		
		# (else_try), #ukita clan
		# 	(is_between, ":cur_troop", "trp_knight_19_1", "trp_knight_20_1"),
		# 	#(store_sub, ":npc_seed", ":cur_troop", "trp_knight_18_1"),
		# 	#(assign, ":max_troops", 5),
		# 	(assign, ":ancestor_seed", 181),
		
		# (else_try), #ikko ikki
		# 	(is_between, ":cur_troop", "trp_knight_20_1", "trp_kingdom_1_pretender"),
		# 	#(store_sub, ":npc_seed", ":cur_troop", "trp_knight_19_1"),
		# 	#(assign, ":max_troops", 5),
		# 	(assign, ":ancestor_seed", 191),
			
		# (try_end),
		
		#gekokujo new lord initialization
		#gekokujo 3.0 some lords have fixed ages and reputations
		(try_begin),
      (eq, ":cur_troop", "trp_knight_1_1"),
      (assign, ":age", 34),
    (else_try),
      (eq, ":cur_troop", "trp_knight_1_2"),
      (assign, ":age", 18),
    (else_try),
      (eq, ":cur_troop", "trp_knight_1_3"),
      (assign, ":age", 50),
    (else_try),
      (eq, ":cur_troop", "trp_knight_1_4"),
      (assign, ":age", 23),
    (else_try),
      (eq, ":cur_troop", "trp_knight_1_5"),
      (assign, ":age", 37),
    (else_try),
      (eq, ":cur_troop", "trp_knight_1_6"),
      (assign, ":age", 48),
    (else_try),
      (eq, ":cur_troop", "trp_knight_1_7"),
      (assign, ":age", 41),
    (else_try),
      (eq, ":cur_troop", "trp_knight_1_8"),
      (assign, ":age", 21),
    (else_try),
      (eq, ":cur_troop", "trp_knight_1_9"),
      (assign, ":age", 26),
    (else_try),
      (eq, ":cur_troop", "trp_knight_1_10"),
      (assign, ":age", 38),
    (else_try),
      (eq, ":cur_troop", "trp_knight_2_1"),
      (assign, ":age", 16),
    (else_try),
      (eq, ":cur_troop", "trp_knight_2_2"),
      (assign, ":age", 19),
    (else_try),
      (eq, ":cur_troop", "trp_knight_2_3"),
      (assign, ":age", 27),
    (else_try),
      (eq, ":cur_troop", "trp_knight_2_4"),
      (assign, ":age", 34),
    (else_try),
      (eq, ":cur_troop", "trp_knight_2_5"),
      (assign, ":age", 24),
    (else_try),
      (eq, ":cur_troop", "trp_knight_3_1"),
      (assign, ":age", 13),
    (else_try),
      (eq, ":cur_troop", "trp_knight_3_2"),
      (assign, ":age", 22),
    (else_try),
      (eq, ":cur_troop", "trp_knight_3_3"),
      (assign, ":age", 31),
    (else_try),
      (eq, ":cur_troop", "trp_knight_3_4"),
      (assign, ":age", 17),
    (else_try),
      (eq, ":cur_troop", "trp_knight_3_5"),
      (assign, ":age", 17),
    (else_try),
      (eq, ":cur_troop", "trp_knight_4_1"),
      (assign, ":age", 41),
    (else_try),
      (eq, ":cur_troop", "trp_knight_4_2"),
      (assign, ":age", 26),
    (else_try),
      (eq, ":cur_troop", "trp_knight_4_3"),
      (assign, ":age", 43),
    (else_try),
      (eq, ":cur_troop", "trp_knight_4_4"),
      (assign, ":age", 30),
    (else_try),
      (eq, ":cur_troop", "trp_knight_4_5"),
      (assign, ":age", 24),
    (else_try),
      (eq, ":cur_troop", "trp_knight_4_6"),
      (assign, ":age", 27),
    (else_try),
      (eq, ":cur_troop", "trp_knight_4_7"),
      (assign, ":age", 28),
    (else_try),
      (eq, ":cur_troop", "trp_knight_4_8"),
      (assign, ":age", 35),
    (else_try),
      (eq, ":cur_troop", "trp_knight_4_9"),
      (assign, ":age", 32),
    (else_try),
      (eq, ":cur_troop", "trp_knight_4_10"),
      (assign, ":age", 34),
    (else_try),
      (eq, ":cur_troop", "trp_knight_5_1"),
      (assign, ":age", 31),
    (else_try),
      (eq, ":cur_troop", "trp_knight_5_2"),
      (assign, ":age", 34),
    (else_try),
      (eq, ":cur_troop", "trp_knight_5_3"),
      (assign, ":age", 40),
    (else_try),
      (eq, ":cur_troop", "trp_knight_5_4"),
      (assign, ":age", 61),
    (else_try),
      (eq, ":cur_troop", "trp_knight_5_5"),
      (assign, ":age", 39),
    (else_try),
      (eq, ":cur_troop", "trp_knight_6_1"),
      (assign, ":age", 21),
    (else_try),
      (eq, ":cur_troop", "trp_knight_6_2"),
      (assign, ":age", 37),
    (else_try),
      (eq, ":cur_troop", "trp_knight_6_3"),
      (assign, ":age", 45),
    (else_try),
      (eq, ":cur_troop", "trp_knight_6_4"),
      (assign, ":age", 32),
    (else_try),
      (eq, ":cur_troop", "trp_knight_6_5"),
      (assign, ":age", 35),
    (else_try),
      (eq, ":cur_troop", "trp_knight_6_6"),
      (assign, ":age", 34),
    (else_try),
      (eq, ":cur_troop", "trp_knight_6_7"),
      (assign, ":age", 33),
    (else_try),
      (eq, ":cur_troop", "trp_knight_6_8"),
      (assign, ":age", 40),
    (else_try),
      (eq, ":cur_troop", "trp_knight_6_9"),
      (assign, ":age", 23),
    (else_try),
      (eq, ":cur_troop", "trp_knight_6_10"),
      (assign, ":age", 45),
    (else_try),
      (eq, ":cur_troop", "trp_knight_6_11"),
      (assign, ":age", 37),
    (else_try),
      (eq, ":cur_troop", "trp_knight_6_12"),
      (assign, ":age", 30),
    (else_try),
      (eq, ":cur_troop", "trp_knight_6_13"),
      (assign, ":age", 32),
    (else_try),
      (eq, ":cur_troop", "trp_knight_6_14"),
      (assign, ":age", 32),
    (else_try),
      (eq, ":cur_troop", "trp_knight_6_15"),
      (assign, ":age", 29),
    (else_try),
      (eq, ":cur_troop", "trp_knight_6_16"),
      (assign, ":age", 52),
    (else_try),
      (eq, ":cur_troop", "trp_knight_6_17"),
      (assign, ":age", 24),
    (else_try),
      (eq, ":cur_troop", "trp_knight_6_18"),
      (assign, ":age", 28),
    (else_try),
      (eq, ":cur_troop", "trp_knight_6_19"),
      (assign, ":age", 47),
    (else_try),
      (eq, ":cur_troop", "trp_knight_7_1"),
      (assign, ":age", 34),
    (else_try),
      (eq, ":cur_troop", "trp_knight_7_2"),
      (assign, ":age", 34),
    (else_try),
      (eq, ":cur_troop", "trp_knight_7_3"),
      (assign, ":age", 59),
    (else_try),
      (eq, ":cur_troop", "trp_knight_7_4"),
      (assign, ":age", 29),
    (else_try),
      (eq, ":cur_troop", "trp_knight_7_5"),
      (assign, ":age", 47),
    (else_try),
      (eq, ":cur_troop", "trp_knight_8_1"),
      (assign, ":age", 33),
    (else_try),
      (eq, ":cur_troop", "trp_knight_8_2"),
      (assign, ":age", 41),
    (else_try),
      (eq, ":cur_troop", "trp_knight_8_3"),
      (assign, ":age", 22),
    (else_try),
      (eq, ":cur_troop", "trp_knight_8_4"),
      (assign, ":age", 53),
    (else_try),
      (eq, ":cur_troop", "trp_knight_8_5"),
      (assign, ":age", 53),
    (else_try),
      (eq, ":cur_troop", "trp_knight_9_1"),
      (assign, ":age", 56),
    (else_try),
      (eq, ":cur_troop", "trp_knight_9_2"),
      (assign, ":age", 37),
    (else_try),
      (eq, ":cur_troop", "trp_knight_9_3"),
      (assign, ":age", 23),
    (else_try),
      (eq, ":cur_troop", "trp_knight_9_4"),
      (assign, ":age", 50),
    (else_try),
      (eq, ":cur_troop", "trp_knight_9_5"),
      (assign, ":age", 20),
    (else_try),
      (eq, ":cur_troop", "trp_knight_10_1"),
      (assign, ":age", 40),
    (else_try),
      (eq, ":cur_troop", "trp_knight_10_2"),
      (assign, ":age", 28),
    (else_try),
      (eq, ":cur_troop", "trp_knight_10_3"),
      (assign, ":age", 35),
    (else_try),
      (eq, ":cur_troop", "trp_knight_10_4"),
      (assign, ":age", 55),
    (else_try),
      (eq, ":cur_troop", "trp_knight_10_5"),
      (assign, ":age", 44),
    (else_try),
      (eq, ":cur_troop", "trp_knight_11_1"),
      (assign, ":age", 25),
    (else_try),
      (eq, ":cur_troop", "trp_knight_11_2"),
      (assign, ":age", 23),
    (else_try),
      (eq, ":cur_troop", "trp_knight_12_1"),
      (assign, ":age", 22),
    (else_try),
      (eq, ":cur_troop", "trp_knight_12_2"),
      (assign, ":age", 38),
    (else_try),
      (eq, ":cur_troop", "trp_knight_12_3"),
      (assign, ":age", 40),
    (else_try),
      (eq, ":cur_troop", "trp_knight_12_4"),
      (assign, ":age", 31),
    (else_try),
      (eq, ":cur_troop", "trp_knight_12_5"),
      (assign, ":age", 30),
    (else_try),
      (eq, ":cur_troop", "trp_knight_12_6"),
      (assign, ":age", 26),
    (else_try),
      (eq, ":cur_troop", "trp_knight_12_7"),
      (assign, ":age", 27),
    (else_try),
      (eq, ":cur_troop", "trp_knight_12_8"),
      (assign, ":age", 31),
    (else_try),
      (eq, ":cur_troop", "trp_knight_12_9"),
      (assign, ":age", 33),
    (else_try),
      (eq, ":cur_troop", "trp_knight_12_10"),
      (assign, ":age", 26),
    (else_try),
      (eq, ":cur_troop", "trp_knight_13_1"),
      (assign, ":age", 49),
    (else_try),
      (eq, ":cur_troop", "trp_knight_13_2"),
      (assign, ":age", 45),
    (else_try),
      (eq, ":cur_troop", "trp_knight_13_3"),
      (assign, ":age", 26),
    (else_try),
      (eq, ":cur_troop", "trp_knight_13_4"),
      (assign, ":age", 28),
    (else_try),
      (eq, ":cur_troop", "trp_knight_13_5"),
      (assign, ":age", 31),
    (else_try),
      (eq, ":cur_troop", "trp_knight_13_6"),
      (assign, ":age", 25),
    (else_try),
      (eq, ":cur_troop", "trp_knight_14_1"),
      (assign, ":age", 35),
    (else_try),
      (eq, ":cur_troop", "trp_knight_14_2"),
      (assign, ":age", 49),
    (else_try),
      (eq, ":cur_troop", "trp_knight_14_3"),
      (assign, ":age", 24),
    (else_try),
      (eq, ":cur_troop", "trp_knight_14_4"),
      (assign, ":age", 24),
    (else_try),
      (eq, ":cur_troop", "trp_knight_14_5"),
      (assign, ":age", 42),
    (else_try),
      (eq, ":cur_troop", "trp_knight_14_6"),
      (assign, ":age", 27),
    (else_try),
      (eq, ":cur_troop", "trp_knight_15_1"),
      (assign, ":age", 40),
    (else_try),
      (eq, ":cur_troop", "trp_knight_15_2"),
      (assign, ":age", 25),
    (else_try),
      (eq, ":cur_troop", "trp_knight_15_3"),
      (assign, ":age", 16),
    (else_try),
      (eq, ":cur_troop", "trp_knight_15_4"),
      (assign, ":age", 56),
    (else_try),
      (eq, ":cur_troop", "trp_knight_15_5"),
      (assign, ":age", 24),
    (else_try),
      (eq, ":cur_troop", "trp_knight_15_6"),
      (assign, ":age", 29),
    (else_try),
      (eq, ":cur_troop", "trp_knight_15_7"),
      (assign, ":age", 40),
    (else_try),
      (eq, ":cur_troop", "trp_knight_15_8"),
      (assign, ":age", 51),
    (else_try),
      (eq, ":cur_troop", "trp_knight_15_9"),
      (assign, ":age", 33),
    (else_try),
      (eq, ":cur_troop", "trp_knight_15_10"),
      (assign, ":age", 38),
    (else_try),
      (eq, ":cur_troop", "trp_knight_15_11"),
      (assign, ":age", 28),
    (else_try),
      (eq, ":cur_troop", "trp_knight_15_12"),
      (assign, ":age", 40),
    (else_try),
      (eq, ":cur_troop", "trp_knight_16_1"),
      (assign, ":age", 28),
    (else_try),
      (eq, ":cur_troop", "trp_knight_16_2"),
      (assign, ":age", 17),
    (else_try),
      (eq, ":cur_troop", "trp_knight_16_3"),
      (assign, ":age", 53),
    (else_try),
      (eq, ":cur_troop", "trp_knight_16_4"),
      (assign, ":age", 30),
    (else_try),
      (eq, ":cur_troop", "trp_knight_16_5"),
      (assign, ":age", 34),
    (else_try),
      (eq, ":cur_troop", "trp_knight_16_6"),
      (assign, ":age", 40),
    (else_try),
      (eq, ":cur_troop", "trp_knight_16_7"),
      (assign, ":age", 36),
    (else_try),
      (eq, ":cur_troop", "trp_knight_16_8"),
      (assign, ":age", 46),
    (else_try),
      (eq, ":cur_troop", "trp_knight_17_1"),
      (assign, ":age", 17),
    (else_try),
      (eq, ":cur_troop", "trp_knight_17_2"),
      (assign, ":age", 48),
    (else_try),
      (eq, ":cur_troop", "trp_knight_17_3"),
      (assign, ":age", 15),
    (else_try),
      (eq, ":cur_troop", "trp_knight_17_4"),
      (assign, ":age", 52),
    (else_try),
      (eq, ":cur_troop", "trp_knight_17_5"),
      (assign, ":age", 36),
    (else_try),
      (eq, ":cur_troop", "trp_knight_18_1"),
      (assign, ":age", 41),
    (else_try),
      (eq, ":cur_troop", "trp_knight_18_2"),
      (assign, ":age", 23),
    (else_try),
      (eq, ":cur_troop", "trp_knight_19_1"),
      (assign, ":age", 16),
    (else_try),
      (eq, ":cur_troop", "trp_knight_19_2"),
      (assign, ":age", 28),
    (else_try),
      (eq, ":cur_troop", "trp_knight_19_3"),
      (assign, ":age", 29),
    (else_try),
      (eq, ":cur_troop", "trp_knight_19_4"),
      (assign, ":age", 42),
    (else_try),
      (eq, ":cur_troop", "trp_knight_19_5"),
      (assign, ":age", 32),
    (else_try),
      (eq, ":cur_troop", "trp_knight_19_6"),
      (assign, ":age", 32),
    (else_try),
      (eq, ":cur_troop", "trp_knight_20_1"),
      (assign, ":age", 27),
    (else_try),
      (eq, ":cur_troop", "trp_knight_20_2"),
      (assign, ":age", 34),
    (else_try),
      (eq, ":cur_troop", "trp_knight_20_3"),
      (assign, ":age", 33),
    (else_try),
      (eq, ":cur_troop", "trp_knight_20_4"),
      (assign, ":age", 30),
    (else_try),
      (eq, ":cur_troop", "trp_knight_20_5"),
      (assign, ":age", 32),
    (else_try),
      (eq, ":cur_troop", "trp_knight_20_6"),
      (assign, ":age", 20),
    (else_try),
      (eq, ":cur_troop", "trp_knight_21_1"),
      (assign, ":age", 39),
    (else_try),
      (eq, ":cur_troop", "trp_knight_21_2"),
      (assign, ":age", 48),
    (else_try),
      (eq, ":cur_troop", "trp_knight_21_3"),
      (assign, ":age", 25),
    (else_try),
      (eq, ":cur_troop", "trp_knight_21_4"),
      (assign, ":age", 29),
    (else_try),
      (eq, ":cur_troop", "trp_knight_21_5"),
      (assign, ":age", 26),
    (else_try),
      (eq, ":cur_troop", "trp_knight_21_6"),
      (assign, ":age", 29),
    (else_try),
      (eq, ":cur_troop", "trp_knight_22_1"),
      (assign, ":age", 33),
    (else_try),
      (eq, ":cur_troop", "trp_knight_22_2"),
      (assign, ":age", 36),
    (else_try),
      (eq, ":cur_troop", "trp_knight_22_3"),
      (assign, ":age", 46),
    (else_try),
      (eq, ":cur_troop", "trp_knight_22_4"),
      (assign, ":age", 25),
    (else_try),
      (eq, ":cur_troop", "trp_knight_23_1"),
      (assign, ":age", 24),
    (else_try),
      (eq, ":cur_troop", "trp_knight_23_2"),
      (assign, ":age", 29),
    (else_try),
      (eq, ":cur_troop", "trp_knight_23_3"),
      (assign, ":age", 39),
    (else_try),
      (eq, ":cur_troop", "trp_knight_23_4"),
      (assign, ":age", 31),
    (else_try),
      (eq, ":cur_troop", "trp_knight_23_5"),
      (assign, ":age", 14),
    (else_try),
      (eq, ":cur_troop", "trp_knight_23_6"),
      (assign, ":age", 37),
    (else_try),
      (eq, ":cur_troop", "trp_knight_24_1"),
      (assign, ":age", 34),
    (else_try),
      (eq, ":cur_troop", "trp_knight_24_2"),
      (assign, ":age", 13),
    (else_try),
      (eq, ":cur_troop", "trp_knight_24_3"),
      (assign, ":age", 51),
    (else_try),
      (eq, ":cur_troop", "trp_knight_24_4"),
      (assign, ":age", 46),
    (else_try),
      (eq, ":cur_troop", "trp_knight_25_1"),
      (assign, ":age", 55),
    (else_try),
      (eq, ":cur_troop", "trp_knight_25_2"),
      (assign, ":age", 35),
    (else_try),
      (eq, ":cur_troop", "trp_knight_25_3"),
      (assign, ":age", 25),
    (else_try),
      (eq, ":cur_troop", "trp_knight_26_1"),
      (assign, ":age", 19),
    (else_try),
      (eq, ":cur_troop", "trp_knight_26_2"),
      (assign, ":age", 30),
    (else_try),
      (eq, ":cur_troop", "trp_knight_26_3"),
      (assign, ":age", 24),
    (else_try),
      (eq, ":cur_troop", "trp_knight_26_4"),
      (assign, ":age", 19),
    (else_try),
      (eq, ":cur_troop", "trp_knight_27_1"),
      (assign, ":age", 33),
    (else_try),
      (eq, ":cur_troop", "trp_knight_27_2"),
      (assign, ":age", 32),
    (else_try),
      (eq, ":cur_troop", "trp_knight_27_3"),
      (assign, ":age", 14),
    (else_try),
      (eq, ":cur_troop", "trp_knight_27_4"),
      (assign, ":age", 26),
    (else_try),
      (eq, ":cur_troop", "trp_knight_28_1"),
      (assign, ":age", 22),
    (else_try),
      (eq, ":cur_troop", "trp_knight_28_2"),
      (assign, ":age", 43),
    (else_try),
      (eq, ":cur_troop", "trp_knight_28_3"),
      (assign, ":age", 31),
		(else_try),
			(store_random_in_range, ":age", 18, 64), #gekokujo also means sons toppling fathers
			(store_random_in_range, ":reputation", 0, 7), #randomize traits
		(try_end),
		
		#(store_random_in_range, ":father", 0, 9), #ten possible fathers
		#(val_add, ":father", ":ancestor_seed"),
		#(troop_set_slot, ":cur_troop", slot_troop_father, ":father"),
		
		#gekokujo 3.0 fixed lady types and reputations
		(try_begin),
			(eq, ":cur_lady", "trp_kingdom_3_lady_1"), #Matsu
			(assign, ":lady_type", 4),
			(assign, ":lady_reputation", 24),
		(else_try),
			(eq, ":cur_lady", "trp_kingdom_3_lady_4"), #Nene
			(assign, ":lady_type", 4),
			(assign, ":lady_reputation", 25),
		(else_try),
			(eq, ":cur_lady", "trp_kingdom_3_lady_5"), #Gracia
			(assign, ":lady_type", 1),
			(assign, ":lady_reputation", 23),
		(else_try),
			(eq, ":cur_lady", "trp_kingdom_9_lady_7"), #Ginchiyo
			(assign, ":lady_type", 1),
			(assign, ":lady_reputation", 22),
		(else_try),
			(eq, ":cur_lady", "trp_kingdom_13_lady_1"), #Kaihime
			(assign, ":lady_type", 1),
			(assign, ":lady_reputation", 22),
		(else_try),
			(store_random_in_range, ":lady_reputation", 21, 25),
			#gekokujo 3.0 daughters and sisters twice as likely
			##find lady type: 1 - daughter, 2 - wife, 3 - sister
			#find lady type: 1/2/3 - daughter, 4/5 - wife, 6/7/8 - sister
			(try_begin),
				(is_between, ":age", 35, 55), #daughter, sister, or wife possible
				(store_random_in_range, ":lady_type", 1, 8),
			(else_try),
				(gt, ":age", 35), #daughter or wife possible
				(store_random_in_range, ":lady_type", 1, 5),
			(else_try),
				(lt, ":age", 55), #sister or wife possible
				(store_random_in_range, ":lady_type", 4, 8),
			(else_try),
				(eq, 1, 1), #only wife possible
				(assign, ":lady_type", 4),
			(try_end),
		(try_end),
		
		(troop_set_slot, ":cur_lady", slot_lord_reputation_type, ":lady_reputation"),
		
		#set lady age and type
		(try_begin),
			(this_or_next|eq, ":lady_type", 1), #daughter
			(this_or_next|eq, ":lady_type", 2),
			(eq, ":lady_type", 3),
			
			(troop_set_slot, ":cur_lady", slot_troop_father, ":cur_troop"),
			
			(store_sub, ":daughter_max_age", ":age", 18),
			(try_begin),
				(gt, ":daughter_max_age", 31),
				(assign, ":daughter_max_age", 31),
			(try_end),
			(store_random_in_range, ":lady_age", 18, ":daughter_max_age"),
		(else_try),
			(this_or_next|eq, ":lady_type", 4), #wife
			(eq, ":lady_type", 5), #wife
			
			(troop_set_slot, ":cur_troop", slot_troop_spouse, ":cur_lady"),
			(troop_set_slot, ":cur_lady", slot_troop_spouse, ":cur_troop"),
			
			(store_sub, ":wife_min_age", ":age", 10),
			(try_begin),
				(lt, ":wife_min_age", 18),
				(assign, ":wife_min_age", 18),
			(try_end),
			(store_random_in_range, ":lady_age", ":wife_min_age", ":age"),
		(else_try),
			(this_or_next|eq, ":lady_type", 6), #sister
			(this_or_next|eq, ":lady_type", 7),
			(eq, ":lady_type", 8), #sister
			
			(troop_set_slot, ":cur_lady", slot_troop_guardian, ":cur_troop"),
			
			(store_sub, ":sister_min_age", ":age", 30),
			(try_begin),
				(lt, ":sister_min_age", 18),
				(assign, ":sister_min_age", 18),
			(try_end),
			(store_add, ":sister_max_age", ":age", 30),
			(try_begin),
				(gt, ":sister_max_age", 31),
				(assign, ":sister_max_age", 31),
			(try_end),
			(store_random_in_range, ":lady_age", ":sister_min_age", ":sister_max_age"),
		(try_end),
		
		#gekokujo 3.0 fixed lady ages
		(try_begin),
			(eq, ":cur_lady", "trp_kingdom_3_lady_1"), #Matsu
			(assign, ":lady_age", 21),
		(else_try),
			(eq, ":cur_lady", "trp_kingdom_3_lady_4"), #Nene
			(assign, ":lady_age", 19),
		(else_try),
			(eq, ":cur_lady", "trp_kingdom_3_lady_5"), #Gracia
			(assign, ":lady_age", 18),
		(else_try),
			(eq, ":cur_lady", "trp_kingdom_9_lady_7"), #Ginchiyo
			(assign, ":lady_age", 19),
		(else_try),
			(eq, ":cur_lady", "trp_kingdom_13_lady_1"), #Kaihime
			(assign, ":lady_age", 18),
		(try_end),
		
		(call_script, "script_init_troop_age", ":cur_lady", ":lady_age"),
		#gekokujo 3.0 script has been long deprecated
		#(call_script, "script_add_lady_items", ":cur_lady"),
		(val_add, ":cur_lady", 1),
		
#		(try_begin),
##			(lt, ":npc_seed", 8), #NPC seed is the order in the faction #Gekokujo, old 'father' conditional
#			(this_or_next|eq, ":npc_seed", 0), #Gekokujo, new alternating 'father' conditional
#			(this_or_next|eq, ":npc_seed", 3),
#			(eq, ":npc_seed", 6),
#			
##			(assign, ":reputation", ":npc_seed"), #Gekokujo remove fixed "father" traits
#			(store_random_in_range, ":reputation", 0, 8), #randomize "father traits"
#			(store_random_in_range, ":age", 45, 64),
#			
#			(store_random_in_range, ":father", 0, 6), #six possible fathers
#			(val_add, ":father", ":ancestor_seed"),
#			(troop_set_slot, ":cur_troop", slot_troop_father, ":father"),
#		
#			#wife
#			(troop_set_slot, ":cur_troop", slot_troop_spouse, ":cur_lady"),
#			(troop_set_slot, ":cur_lady", slot_troop_spouse, ":cur_troop"),
#			(store_random_in_range, ":wife_reputation", 20, 26),
#			(try_begin),
#				(eq, ":wife_reputation", 20),
#				(assign, ":wife_reputation", lrep_conventional),
#			(try_end),
#			(troop_set_slot, ":cur_lady", slot_lord_reputation_type, ":wife_reputation"),
#		
#			#gekokujo random wife age gap
#			(store_random_in_range, ":wife_age_gap", 0, 10),
#			(store_sub, ":wife_age", ":age", ":wife_age_gap"),
#			(call_script, "script_init_troop_age", ":cur_lady", ":wife_age"),
#			#(call_script, "script_init_troop_age", ":cur_lady", 49),
#			(call_script, "script_add_lady_items", ":cur_lady"),
#		
#			(val_add, ":cur_lady", 1),
#
#			#daughter
#			#Gekokujo - first check to see if there are available daughters
#			(try_begin),
#				(gt, ":max_troops", ":npc_seed"), #if max_troops > npc_seed, the next slot is a guaranteed a child
#				
#				(troop_set_slot, ":cur_lady", slot_troop_father, ":cur_troop"),
#				(store_sub, ":mother", ":cur_lady", 1),
#				#gekokujo random daughter ages
#				(store_random_in_range, ":daughter_age", 19, 29),
#				(call_script, "script_init_troop_age", ":cur_lady", ":daughter_age"),
#				#(call_script, "script_init_troop_age", ":cur_lady", 19),
#				(troop_set_slot, ":cur_lady", slot_troop_mother, ":cur_lady"),
#				(store_random_in_range, ":lady_reputation", lrep_conventional, 34), #33% chance of father-derived
#				(try_begin),
#					(le, ":lady_reputation", 25),
#					(troop_set_slot, ":cur_lady", slot_lord_reputation_type, ":lady_reputation"),
#				(else_try),	
#					(eq, ":lady_reputation", 26),
#					(troop_set_slot, ":cur_lady", slot_lord_reputation_type, lrep_conventional),
#				(else_try),	
#					(eq, ":lady_reputation", 27),
#					(troop_set_slot, ":cur_lady", slot_lord_reputation_type, lrep_moralist),
#				(else_try),
#					(assign, ":guardian_reputation", ":reputation"),
#					(try_begin),
#						(this_or_next|eq, ":guardian_reputation", lrep_martial),
#						(eq, ":guardian_reputation", 0),
#						(troop_set_slot, ":cur_lady", slot_lord_reputation_type, lrep_conventional),
#					(else_try),		
#						(eq, ":guardian_reputation", lrep_quarrelsome),
#						(troop_set_slot, ":cur_lady", slot_lord_reputation_type, lrep_otherworldly),
#					(else_try),		
#						(eq, ":guardian_reputation", lrep_selfrighteous),
#						(troop_set_slot, ":cur_lady", slot_lord_reputation_type, lrep_ambitious),
#					(else_try),		
#						(eq, ":guardian_reputation", lrep_cunning),
#						(troop_set_slot, ":cur_lady", slot_lord_reputation_type, lrep_adventurous),
#					(else_try),		
#						(eq, ":guardian_reputation", lrep_goodnatured),
#						(troop_set_slot, ":cur_lady", slot_lord_reputation_type, lrep_adventurous),
#					(else_try),		
#						(eq, ":guardian_reputation", lrep_debauched),
#						(troop_set_slot, ":cur_lady", slot_lord_reputation_type, lrep_ambitious),
#					(else_try),		
#						(eq, ":guardian_reputation", lrep_upstanding),
#						(troop_set_slot, ":cur_lady", slot_lord_reputation_type, lrep_moralist),
#					(try_end),
#				(try_end),
#			
#				(call_script, "script_add_lady_items", ":cur_lady"),
#				(val_add, ":cur_lady", 1),
#				#high renown
#			(try_end),
#			
#		(else_try),	#Younger unmarried lords 
#			#age is father's minus 20 to 25
#			(this_or_next|eq, ":npc_seed", 1), #Gekokujo new alternating son conditionals
#			(this_or_next|eq, ":npc_seed", 4), 
#			(eq, ":npc_seed", 7),
#			(store_sub, ":father", ":cur_troop", 1), #Gekokujo -- the father is always 1 slot before the son
#			
#			(troop_set_slot, ":cur_troop", slot_troop_father, ":father"),
#			(troop_get_slot, ":mother", ":father", slot_troop_spouse),
#			(troop_set_slot, ":cur_troop", slot_troop_mother, ":mother"),
#			
#			(troop_get_slot, ":father_age", ":father", slot_troop_age),
#			(store_sub, ":age", ":father_age", ":father_age_at_birth"),
#
#			(try_begin), #50% chance of having father's rep
#				(store_random_in_range, ":reputation", 0, 16),
#
#				(gt, ":reputation", 7),
#				(troop_get_slot, ":reputation", ":father", slot_lord_reputation_type),
#			(try_end),
#			
#		(else_try),	#Older unmarried lords
#			(is_between, ":npc_seed", 8, 12), #Gekokujo old 'single' conditionals
#			(this_or_next|eq, ":npc_seed", 2), #Gekokujo new alternating 'single' lords conditionals
#			(this_or_next|eq, ":npc_seed", 5), #Gekokujo new alternating 'single' lords conditionals
#			(this_or_next|eq, ":npc_seed", 8), #Gekokujo new alternating 'single' lords conditionals
#			(eq, ":npc_seed", 9),
#			
#			#(store_sub, ":father", ":cur_troop", 2), #Gekokujo -- the father is always 2 slots before the 'single'
#			
#			(store_random_in_range, ":age", 25, 36),			
#			(store_random_in_range, ":reputation", 0, 8),			
#			
#			(store_random_in_range, ":sister_reputation", 20, 26),
#			(try_begin),
#				(eq, ":sister_reputation", 20),
#				(assign, ":sister_reputation", lrep_conventional),
#			(try_end),
#			(troop_set_slot, ":cur_lady", slot_lord_reputation_type, ":sister_reputation"),
#			
#			(troop_set_slot, ":cur_lady", slot_troop_guardian, ":cur_troop"),
#	
#			#gekokujo random sister age
#			(store_random_in_range, ":sister_age", 21, 31),
#			(call_script, "script_init_troop_age", ":cur_lady", ":sister_age"),
#			#(call_script, "script_init_troop_age", ":cur_lady", 21),
#			(call_script, "script_add_lady_items", ":cur_lady"),
#			
#			(val_add, ":cur_lady", 1),
#			
#		(try_end),
		
		(try_begin),
			(eq, ":reputation", 0),
			(assign, ":reputation", 1),
		(try_end),
		
    (troop_set_slot, ":cur_troop", slot_lord_reputation_type, ":reputation"),

		(call_script, "script_init_troop_age", ":cur_troop", ":age"),
	  (try_end),
	  
	  (try_begin),
	    (eq, "$cheat_mode", 1),
	    (assign, reg3, "$cheat_mode"),
	    (display_message, "@{!}DEBUG -- Assigned lord reputation and relations"),
		
#	    (display_message, "str_assigned_lord_reputation_and_relations_cheat_mode_reg3"), #This string can be removed
	  (try_end),
	  
	  (try_for_range, ":cur_troop", pretenders_begin, pretenders_end),
		(troop_set_slot, ":cur_troop", slot_troop_occupation, slto_inactive_pretender),
		(store_random_in_range, ":age", 25, 30),
		(troop_set_slot, ":cur_troop", slot_troop_age, ":age"),
		(eq, ":cur_troop", "trp_kingdom_5_pretender"),
		(troop_set_slot, ":cur_troop", slot_troop_age, 45),		
	  (try_end),
	]),
    ("initialize_faction_troop_types",
    [

      (try_for_range, ":faction_no", kingdoms_begin, kingdoms_end),
        (faction_get_slot, ":culture", ":faction_no", slot_faction_culture),
	  
	    #gekokujo ashigaru recruitment start
        (faction_get_slot, ":troop", ":culture",  slot_faction_tier_0_troop),
        (faction_set_slot, ":faction_no",  slot_faction_tier_0_troop, ":troop"),
		#gekokujo ashigaru recruitment end
        (faction_get_slot, ":troop", ":culture",  slot_faction_tier_1_troop),
        (faction_set_slot, ":faction_no",  slot_faction_tier_1_troop, ":troop"),
        (faction_get_slot, ":troop", ":culture",  slot_faction_tier_2_troop),
        (faction_set_slot, ":faction_no",  slot_faction_tier_2_troop, ":troop"),
        (faction_get_slot, ":troop", ":culture",  slot_faction_tier_3_troop),
        (faction_set_slot, ":faction_no",  slot_faction_tier_3_troop, ":troop"),
        (faction_get_slot, ":troop", ":culture",  slot_faction_tier_4_troop),
        (faction_set_slot, ":faction_no",  slot_faction_tier_4_troop, ":troop"),
        (faction_get_slot, ":troop", ":culture",  slot_faction_tier_5_troop),
        (faction_set_slot, ":faction_no",  slot_faction_tier_5_troop, ":troop"),
      
        (try_begin),
          (faction_slot_eq, ":faction_no", slot_faction_culture, "fac_culture_1"),
      
          (faction_set_slot, ":faction_no", slot_faction_deserter_troop, "trp_gekokujo_uesugi_deserter"),
          (faction_set_slot, ":faction_no", slot_faction_guard_troop, "trp_gekokujo_uesugi_veteran_retainer"),
          (faction_set_slot, ":faction_no", slot_faction_messenger_troop, "trp_gekokujo_uesugi_messenger"),
          (faction_set_slot, ":faction_no", slot_faction_prison_guard_troop, "trp_gekokujo_uesugi_prison_guard"),
          (faction_set_slot, ":faction_no", slot_faction_castle_guard_troop, "trp_gekokujo_uesugi_castle_guard"),
          (faction_set_slot, ":faction_no", slot_faction_reinforcements_a, "pt_kingdom_1_reinforcements_a"),
          (faction_set_slot, ":faction_no", slot_faction_reinforcements_b, "pt_kingdom_1_reinforcements_b"),
          (faction_set_slot, ":faction_no", slot_faction_reinforcements_c, "pt_kingdom_1_reinforcements_c"),
        (else_try),
          (faction_slot_eq, ":faction_no", slot_faction_culture, "fac_culture_2"),
      
          (faction_set_slot, ":faction_no", slot_faction_deserter_troop, "trp_gekokujo_date_deserter"),
          (faction_set_slot, ":faction_no", slot_faction_guard_troop, "trp_gekokujo_date_veteran_retainer"),
          (faction_set_slot, ":faction_no", slot_faction_messenger_troop, "trp_gekokujo_date_messenger"),
          (faction_set_slot, ":faction_no", slot_faction_prison_guard_troop, "trp_gekokujo_date_prison_guard"),
          (faction_set_slot, ":faction_no", slot_faction_castle_guard_troop, "trp_gekokujo_date_castle_guard"),
          (faction_set_slot, ":faction_no", slot_faction_reinforcements_a, "pt_kingdom_2_reinforcements_a"),
          (faction_set_slot, ":faction_no", slot_faction_reinforcements_b, "pt_kingdom_2_reinforcements_b"),
          (faction_set_slot, ":faction_no", slot_faction_reinforcements_c, "pt_kingdom_2_reinforcements_c"),
        (else_try),
          (faction_slot_eq, ":faction_no", slot_faction_culture, "fac_culture_3"),
      
          (faction_set_slot, ":faction_no", slot_faction_deserter_troop, "trp_gekokujo_oda_deserter"),
          (faction_set_slot, ":faction_no", slot_faction_guard_troop, "trp_gekokujo_oda_veteran_retainer"),
          (faction_set_slot, ":faction_no", slot_faction_messenger_troop, "trp_gekokujo_oda_messenger"),
          (faction_set_slot, ":faction_no", slot_faction_prison_guard_troop, "trp_gekokujo_oda_prison_guard"),
          (faction_set_slot, ":faction_no", slot_faction_castle_guard_troop, "trp_gekokujo_oda_castle_guard"),
          (faction_set_slot, ":faction_no", slot_faction_reinforcements_a, "pt_kingdom_3_reinforcements_a"),
          (faction_set_slot, ":faction_no", slot_faction_reinforcements_b, "pt_kingdom_3_reinforcements_b"),
          (faction_set_slot, ":faction_no", slot_faction_reinforcements_c, "pt_kingdom_3_reinforcements_c"),
        (else_try),
          (faction_slot_eq, ":faction_no", slot_faction_culture, "fac_culture_4"),
      
          (faction_set_slot, ":faction_no", slot_faction_deserter_troop, "trp_gekokujo_mori_deserter"),
          (faction_set_slot, ":faction_no", slot_faction_guard_troop, "trp_gekokujo_mori_veteran_retainer"),
          (faction_set_slot, ":faction_no", slot_faction_messenger_troop, "trp_gekokujo_mori_messenger"),
          (faction_set_slot, ":faction_no", slot_faction_prison_guard_troop, "trp_gekokujo_mori_prison_guard"),
          (faction_set_slot, ":faction_no", slot_faction_castle_guard_troop, "trp_gekokujo_mori_castle_guard"),
          (faction_set_slot, ":faction_no", slot_faction_reinforcements_a, "pt_kingdom_4_reinforcements_a"),
          (faction_set_slot, ":faction_no", slot_faction_reinforcements_b, "pt_kingdom_4_reinforcements_b"),
          (faction_set_slot, ":faction_no", slot_faction_reinforcements_c, "pt_kingdom_4_reinforcements_c"),
        (else_try),
          (faction_slot_eq, ":faction_no", slot_faction_culture, "fac_culture_5"),
      
          (faction_set_slot, ":faction_no", slot_faction_deserter_troop, "trp_gekokujo_takeda_deserter"),
          (faction_set_slot, ":faction_no", slot_faction_guard_troop, "trp_gekokujo_takeda_veteran_retainer"),
          (faction_set_slot, ":faction_no", slot_faction_messenger_troop, "trp_gekokujo_takeda_messenger"),
          (faction_set_slot, ":faction_no", slot_faction_prison_guard_troop, "trp_gekokujo_takeda_prison_guard"),
          (faction_set_slot, ":faction_no", slot_faction_castle_guard_troop, "trp_gekokujo_takeda_castle_guard"),
          (faction_set_slot, ":faction_no", slot_faction_reinforcements_a, "pt_kingdom_5_reinforcements_a"),
          (faction_set_slot, ":faction_no", slot_faction_reinforcements_b, "pt_kingdom_5_reinforcements_b"),
          (faction_set_slot, ":faction_no", slot_faction_reinforcements_c, "pt_kingdom_5_reinforcements_c"),
        (else_try),
          (faction_slot_eq, ":faction_no", slot_faction_culture, "fac_culture_6"),
      
          (faction_set_slot, ":faction_no", slot_faction_deserter_troop, "trp_gekokujo_tokugawa_deserter"),
          (faction_set_slot, ":faction_no", slot_faction_guard_troop, "trp_gekokujo_tokugawa_veteran_retainer"),
          (faction_set_slot, ":faction_no", slot_faction_messenger_troop, "trp_gekokujo_tokugawa_messenger"),
          (faction_set_slot, ":faction_no", slot_faction_prison_guard_troop, "trp_gekokujo_tokugawa_prison_guard"),
          (faction_set_slot, ":faction_no", slot_faction_castle_guard_troop, "trp_gekokujo_tokugawa_castle_guard"),
          (faction_set_slot, ":faction_no", slot_faction_reinforcements_a, "pt_kingdom_6_reinforcements_a"),
          (faction_set_slot, ":faction_no", slot_faction_reinforcements_b, "pt_kingdom_6_reinforcements_b"),
          (faction_set_slot, ":faction_no", slot_faction_reinforcements_c, "pt_kingdom_6_reinforcements_c"),
        (else_try),
          (faction_slot_eq, ":faction_no", slot_faction_culture, "fac_culture_7"),
      
          (faction_set_slot, ":faction_no", slot_faction_deserter_troop, "trp_gekokujo_miyoshi_deserter"),
          (faction_set_slot, ":faction_no", slot_faction_guard_troop, "trp_gekokujo_miyoshi_veteran_retainer"),
          (faction_set_slot, ":faction_no", slot_faction_messenger_troop, "trp_gekokujo_miyoshi_messenger"),
          (faction_set_slot, ":faction_no", slot_faction_prison_guard_troop, "trp_gekokujo_miyoshi_prison_guard"),
          (faction_set_slot, ":faction_no", slot_faction_castle_guard_troop, "trp_gekokujo_miyoshi_castle_guard"),
          (faction_set_slot, ":faction_no", slot_faction_reinforcements_a, "pt_kingdom_7_reinforcements_a"),
          (faction_set_slot, ":faction_no", slot_faction_reinforcements_b, "pt_kingdom_7_reinforcements_b"),
          (faction_set_slot, ":faction_no", slot_faction_reinforcements_c, "pt_kingdom_7_reinforcements_c"),
        (else_try),
          (faction_slot_eq, ":faction_no", slot_faction_culture, "fac_culture_8"),
      
          (faction_set_slot, ":faction_no", slot_faction_deserter_troop, "trp_gekokujo_amako_deserter"),
          (faction_set_slot, ":faction_no", slot_faction_guard_troop, "trp_gekokujo_amako_veteran_retainer"),
          (faction_set_slot, ":faction_no", slot_faction_messenger_troop, "trp_gekokujo_amako_messenger"),
          (faction_set_slot, ":faction_no", slot_faction_prison_guard_troop, "trp_gekokujo_amako_prison_guard"),
          (faction_set_slot, ":faction_no", slot_faction_castle_guard_troop, "trp_gekokujo_amako_castle_guard"),
          (faction_set_slot, ":faction_no", slot_faction_reinforcements_a, "pt_kingdom_8_reinforcements_a"),
          (faction_set_slot, ":faction_no", slot_faction_reinforcements_b, "pt_kingdom_8_reinforcements_b"),
          (faction_set_slot, ":faction_no", slot_faction_reinforcements_c, "pt_kingdom_8_reinforcements_c"),
        (else_try),
          (faction_slot_eq, ":faction_no", slot_faction_culture, "fac_culture_9"),
      
          (faction_set_slot, ":faction_no", slot_faction_deserter_troop, "trp_gekokujo_otomo_deserter"),
          (faction_set_slot, ":faction_no", slot_faction_guard_troop, "trp_gekokujo_otomo_veteran_retainer"),
          (faction_set_slot, ":faction_no", slot_faction_messenger_troop, "trp_gekokujo_otomo_messenger"),
          (faction_set_slot, ":faction_no", slot_faction_prison_guard_troop, "trp_gekokujo_otomo_prison_guard"),
          (faction_set_slot, ":faction_no", slot_faction_castle_guard_troop, "trp_gekokujo_otomo_castle_guard"),
          (faction_set_slot, ":faction_no", slot_faction_reinforcements_a, "pt_kingdom_9_reinforcements_a"),
          (faction_set_slot, ":faction_no", slot_faction_reinforcements_b, "pt_kingdom_9_reinforcements_b"),
          (faction_set_slot, ":faction_no", slot_faction_reinforcements_c, "pt_kingdom_9_reinforcements_c"),
        (else_try),
          (faction_slot_eq, ":faction_no", slot_faction_culture, "fac_culture_10"),
      
          (faction_set_slot, ":faction_no", slot_faction_deserter_troop, "trp_gekokujo_nanbu_deserter"),
          (faction_set_slot, ":faction_no", slot_faction_guard_troop, "trp_gekokujo_nanbu_veteran_retainer"),
          (faction_set_slot, ":faction_no", slot_faction_messenger_troop, "trp_gekokujo_nanbu_messenger"),
          (faction_set_slot, ":faction_no", slot_faction_prison_guard_troop, "trp_gekokujo_nanbu_prison_guard"),
          (faction_set_slot, ":faction_no", slot_faction_castle_guard_troop, "trp_gekokujo_nanbu_castle_guard"),
          (faction_set_slot, ":faction_no", slot_faction_reinforcements_a, "pt_kingdom_10_reinforcements_a"),
          (faction_set_slot, ":faction_no", slot_faction_reinforcements_b, "pt_kingdom_10_reinforcements_b"),
          (faction_set_slot, ":faction_no", slot_faction_reinforcements_c, "pt_kingdom_10_reinforcements_c"),
        (else_try),
          (faction_slot_eq, ":faction_no", slot_faction_culture, "fac_culture_11"),
      
          (faction_set_slot, ":faction_no", slot_faction_deserter_troop, "trp_gekokujo_asakura_deserter"),
          (faction_set_slot, ":faction_no", slot_faction_guard_troop, "trp_gekokujo_asakura_veteran_retainer"),
          (faction_set_slot, ":faction_no", slot_faction_messenger_troop, "trp_gekokujo_asakura_messenger"),
          (faction_set_slot, ":faction_no", slot_faction_prison_guard_troop, "trp_gekokujo_asakura_prison_guard"),
          (faction_set_slot, ":faction_no", slot_faction_castle_guard_troop, "trp_gekokujo_asakura_castle_guard"),
          (faction_set_slot, ":faction_no", slot_faction_reinforcements_a, "pt_kingdom_11_reinforcements_a"),
          (faction_set_slot, ":faction_no", slot_faction_reinforcements_b, "pt_kingdom_11_reinforcements_b"),
          (faction_set_slot, ":faction_no", slot_faction_reinforcements_c, "pt_kingdom_11_reinforcements_c"),
        (else_try),
          (faction_slot_eq, ":faction_no", slot_faction_culture, "fac_culture_12"),
      
          (faction_set_slot, ":faction_no", slot_faction_deserter_troop, "trp_gekokujo_chosokabe_deserter"),
          (faction_set_slot, ":faction_no", slot_faction_guard_troop, "trp_gekokujo_chosokabe_veteran_retainer"),
          (faction_set_slot, ":faction_no", slot_faction_messenger_troop, "trp_gekokujo_chosokabe_messenger"),
          (faction_set_slot, ":faction_no", slot_faction_prison_guard_troop, "trp_gekokujo_chosokabe_prison_guard"),
          (faction_set_slot, ":faction_no", slot_faction_castle_guard_troop, "trp_gekokujo_chosokabe_castle_guard"),
          (faction_set_slot, ":faction_no", slot_faction_reinforcements_a, "pt_kingdom_12_reinforcements_a"),
          (faction_set_slot, ":faction_no", slot_faction_reinforcements_b, "pt_kingdom_12_reinforcements_b"),
          (faction_set_slot, ":faction_no", slot_faction_reinforcements_c, "pt_kingdom_12_reinforcements_c"),
        (else_try),
          (faction_slot_eq, ":faction_no", slot_faction_culture, "fac_culture_13"),
      
          (faction_set_slot, ":faction_no", slot_faction_deserter_troop, "trp_gekokujo_hojo_deserter"),
          (faction_set_slot, ":faction_no", slot_faction_guard_troop, "trp_gekokujo_hojo_veteran_retainer"),
          (faction_set_slot, ":faction_no", slot_faction_messenger_troop, "trp_gekokujo_hojo_messenger"),
          (faction_set_slot, ":faction_no", slot_faction_prison_guard_troop, "trp_gekokujo_hojo_prison_guard"),
          (faction_set_slot, ":faction_no", slot_faction_castle_guard_troop, "trp_gekokujo_hojo_castle_guard"),
          (faction_set_slot, ":faction_no", slot_faction_reinforcements_a, "pt_kingdom_13_reinforcements_a"),
          (faction_set_slot, ":faction_no", slot_faction_reinforcements_b, "pt_kingdom_13_reinforcements_b"),
          (faction_set_slot, ":faction_no", slot_faction_reinforcements_c, "pt_kingdom_13_reinforcements_c"),
        (else_try),
          (faction_slot_eq, ":faction_no", slot_faction_culture, "fac_culture_14"),
      
          (faction_set_slot, ":faction_no", slot_faction_deserter_troop, "trp_gekokujo_mogami_deserter"),
          (faction_set_slot, ":faction_no", slot_faction_guard_troop, "trp_gekokujo_mogami_veteran_retainer"),
          (faction_set_slot, ":faction_no", slot_faction_messenger_troop, "trp_gekokujo_mogami_messenger"),
          (faction_set_slot, ":faction_no", slot_faction_prison_guard_troop, "trp_gekokujo_mogami_prison_guard"),
          (faction_set_slot, ":faction_no", slot_faction_castle_guard_troop, "trp_gekokujo_mogami_castle_guard"),
          (faction_set_slot, ":faction_no", slot_faction_reinforcements_a, "pt_kingdom_14_reinforcements_a"),
          (faction_set_slot, ":faction_no", slot_faction_reinforcements_b, "pt_kingdom_14_reinforcements_b"),
          (faction_set_slot, ":faction_no", slot_faction_reinforcements_c, "pt_kingdom_14_reinforcements_c"),
        (else_try),
          (faction_slot_eq, ":faction_no", slot_faction_culture, "fac_culture_15"),
      
          (faction_set_slot, ":faction_no", slot_faction_deserter_troop, "trp_gekokujo_shimazu_deserter"),
          (faction_set_slot, ":faction_no", slot_faction_guard_troop, "trp_gekokujo_shimazu_veteran_retainer"),
          (faction_set_slot, ":faction_no", slot_faction_messenger_troop, "trp_gekokujo_shimazu_messenger"),
          (faction_set_slot, ":faction_no", slot_faction_prison_guard_troop, "trp_gekokujo_shimazu_prison_guard"),
          (faction_set_slot, ":faction_no", slot_faction_castle_guard_troop, "trp_gekokujo_shimazu_castle_guard"),
          (faction_set_slot, ":faction_no", slot_faction_reinforcements_a, "pt_kingdom_15_reinforcements_a"),
          (faction_set_slot, ":faction_no", slot_faction_reinforcements_b, "pt_kingdom_15_reinforcements_b"),
          (faction_set_slot, ":faction_no", slot_faction_reinforcements_c, "pt_kingdom_15_reinforcements_c"),
        (else_try),
          (faction_slot_eq, ":faction_no", slot_faction_culture, "fac_culture_16"),
      
          (faction_set_slot, ":faction_no", slot_faction_deserter_troop, "trp_gekokujo_ryuzoji_deserter"),
          (faction_set_slot, ":faction_no", slot_faction_guard_troop, "trp_gekokujo_ryuzoji_veteran_retainer"),
          (faction_set_slot, ":faction_no", slot_faction_messenger_troop, "trp_gekokujo_ryuzoji_messenger"),
          (faction_set_slot, ":faction_no", slot_faction_prison_guard_troop, "trp_gekokujo_ryuzoji_prison_guard"),
          (faction_set_slot, ":faction_no", slot_faction_castle_guard_troop, "trp_gekokujo_ryuzoji_castle_guard"),
          (faction_set_slot, ":faction_no", slot_faction_reinforcements_a, "pt_kingdom_16_reinforcements_a"),
          (faction_set_slot, ":faction_no", slot_faction_reinforcements_b, "pt_kingdom_16_reinforcements_b"),
          (faction_set_slot, ":faction_no", slot_faction_reinforcements_c, "pt_kingdom_16_reinforcements_c"),
        (else_try),
          (faction_slot_eq, ":faction_no", slot_faction_culture, "fac_culture_17"),
      
          (faction_set_slot, ":faction_no", slot_faction_deserter_troop, "trp_gekokujo_satake_deserter"),
          (faction_set_slot, ":faction_no", slot_faction_guard_troop, "trp_gekokujo_satake_veteran_retainer"),
          (faction_set_slot, ":faction_no", slot_faction_messenger_troop, "trp_gekokujo_satake_messenger"),
          (faction_set_slot, ":faction_no", slot_faction_prison_guard_troop, "trp_gekokujo_satake_prison_guard"),
          (faction_set_slot, ":faction_no", slot_faction_castle_guard_troop, "trp_gekokujo_satake_castle_guard"),
          (faction_set_slot, ":faction_no", slot_faction_reinforcements_a, "pt_kingdom_17_reinforcements_a"),
          (faction_set_slot, ":faction_no", slot_faction_reinforcements_b, "pt_kingdom_17_reinforcements_b"),
          (faction_set_slot, ":faction_no", slot_faction_reinforcements_c, "pt_kingdom_17_reinforcements_c"),
        (else_try),
          (faction_slot_eq, ":faction_no", slot_faction_culture, "fac_culture_18"),
      
          (faction_set_slot, ":faction_no", slot_faction_deserter_troop, "trp_gekokujo_satomi_deserter"),
          (faction_set_slot, ":faction_no", slot_faction_guard_troop, "trp_gekokujo_satomi_veteran_retainer"),
          (faction_set_slot, ":faction_no", slot_faction_messenger_troop, "trp_gekokujo_satomi_messenger"),
          (faction_set_slot, ":faction_no", slot_faction_prison_guard_troop, "trp_gekokujo_satomi_prison_guard"),
          (faction_set_slot, ":faction_no", slot_faction_castle_guard_troop, "trp_gekokujo_satomi_castle_guard"),
          (faction_set_slot, ":faction_no", slot_faction_reinforcements_a, "pt_kingdom_18_reinforcements_a"),
          (faction_set_slot, ":faction_no", slot_faction_reinforcements_b, "pt_kingdom_18_reinforcements_b"),
          (faction_set_slot, ":faction_no", slot_faction_reinforcements_c, "pt_kingdom_18_reinforcements_c"),
        (else_try),
          (faction_slot_eq, ":faction_no", slot_faction_culture, "fac_culture_19"),
      
          (faction_set_slot, ":faction_no", slot_faction_deserter_troop, "trp_gekokujo_ukita_deserter"),
          (faction_set_slot, ":faction_no", slot_faction_guard_troop, "trp_gekokujo_ukita_veteran_retainer"),
          (faction_set_slot, ":faction_no", slot_faction_messenger_troop, "trp_gekokujo_ukita_messenger"),
          (faction_set_slot, ":faction_no", slot_faction_prison_guard_troop, "trp_gekokujo_ukita_prison_guard"),
          (faction_set_slot, ":faction_no", slot_faction_castle_guard_troop, "trp_gekokujo_ukita_castle_guard"),
          (faction_set_slot, ":faction_no", slot_faction_reinforcements_a, "pt_kingdom_19_reinforcements_a"),
          (faction_set_slot, ":faction_no", slot_faction_reinforcements_b, "pt_kingdom_19_reinforcements_b"),
          (faction_set_slot, ":faction_no", slot_faction_reinforcements_c, "pt_kingdom_19_reinforcements_c"),
        (else_try),
          (faction_slot_eq, ":faction_no", slot_faction_culture, "fac_culture_20"),
      
          (faction_set_slot, ":faction_no", slot_faction_deserter_troop, "trp_gekokujo_ikko_jizamurai"),
          (faction_set_slot, ":faction_no", slot_faction_guard_troop, "trp_gekokujo_ikko_retainer"),
          (faction_set_slot, ":faction_no", slot_faction_messenger_troop, "trp_gekokujo_ikko_mounted_retainer"),
          (faction_set_slot, ":faction_no", slot_faction_prison_guard_troop, "trp_gekokujo_ikko_master_gunner"),
          (faction_set_slot, ":faction_no", slot_faction_castle_guard_troop, "trp_gekokujo_ikko_mounted_officer"),
          (faction_set_slot, ":faction_no", slot_faction_reinforcements_a, "pt_kingdom_20_reinforcements_a"),
          (faction_set_slot, ":faction_no", slot_faction_reinforcements_b, "pt_kingdom_20_reinforcements_b"),
          (faction_set_slot, ":faction_no", slot_faction_reinforcements_c, "pt_kingdom_20_reinforcements_c"),
          
       (else_try),
          (faction_slot_eq, ":faction_no", slot_faction_culture, "fac_culture_21"),
      
          (faction_set_slot, ":faction_no", slot_faction_deserter_troop, "trp_gekokujo_xb_deserter"),
          (faction_set_slot, ":faction_no", slot_faction_guard_troop, "trp_gekokujo_xb_hatamoto_archer"),
          (faction_set_slot, ":faction_no", slot_faction_messenger_troop, "trp_gekokujo_xb_messenger"),
          (faction_set_slot, ":faction_no", slot_faction_prison_guard_troop, "trp_gekokujo_xb_prison_guard"),
          (faction_set_slot, ":faction_no", slot_faction_castle_guard_troop, "trp_gekokujo_xb_castle_guard"),
          (faction_set_slot, ":faction_no", slot_faction_reinforcements_a, "pt_kingdom_21_reinforcements_a"),
          (faction_set_slot, ":faction_no", slot_faction_reinforcements_b, "pt_kingdom_21_reinforcements_b"),
          (faction_set_slot, ":faction_no", slot_faction_reinforcements_c, "pt_kingdom_21_reinforcements_c"),
          
       (else_try),
          (faction_slot_eq, ":faction_no", slot_faction_culture, "fac_culture_22"),
      
          (faction_set_slot, ":faction_no", slot_faction_deserter_troop, "trp_gekokujo_ss_elite_spearman"),
          (faction_set_slot, ":faction_no", slot_faction_guard_troop, "trp_gekokujo_ss_veteran_spearman"),
          (faction_set_slot, ":faction_no", slot_faction_messenger_troop, "trp_gekokujo_ss_master_gunner"),
          (faction_set_slot, ":faction_no", slot_faction_prison_guard_troop, "trp_gekokujo_ss_officer"),
          (faction_set_slot, ":faction_no", slot_faction_castle_guard_troop, "trp_gekokujo_ss_mounted_officer"),
          (faction_set_slot, ":faction_no", slot_faction_reinforcements_a, "pt_kingdom_22_reinforcements_a"),
          (faction_set_slot, ":faction_no", slot_faction_reinforcements_b, "pt_kingdom_22_reinforcements_b"),
          (faction_set_slot, ":faction_no", slot_faction_reinforcements_c, "pt_kingdom_22_reinforcements_c"),
          
       (else_try),
          (faction_slot_eq, ":faction_no", slot_faction_culture, "fac_culture_23"),
      
          (faction_set_slot, ":faction_no", slot_faction_deserter_troop, "trp_gekokujo_wz_retainer"),
          (faction_set_slot, ":faction_no", slot_faction_guard_troop, "trp_gekokujo_wz_mounted_retainer"),
          (faction_set_slot, ":faction_no", slot_faction_messenger_troop, "trp_gekokujo_wz_samurai_archer"),
          (faction_set_slot, ":faction_no", slot_faction_prison_guard_troop, "trp_gekokujo_wz_samurai_archer"),
          (faction_set_slot, ":faction_no", slot_faction_castle_guard_troop, "trp_gekokujo_wz_mounted_officer"),
          (faction_set_slot, ":faction_no", slot_faction_reinforcements_a, "pt_kingdom_23_reinforcements_a"),
          (faction_set_slot, ":faction_no", slot_faction_reinforcements_b, "pt_kingdom_23_reinforcements_b"),
          (faction_set_slot, ":faction_no", slot_faction_reinforcements_c, "pt_kingdom_23_reinforcements_c"),
          
        (else_try),
          (faction_slot_eq, ":faction_no", slot_faction_culture, "fac_culture_24"),
      
          (faction_set_slot, ":faction_no", slot_faction_deserter_troop, "trp_gekokujo_dd_marksman"),
          (faction_set_slot, ":faction_no", slot_faction_guard_troop, "trp_gekokujo_dd_officer"),
          (faction_set_slot, ":faction_no", slot_faction_messenger_troop, "trp_gekokujo_dd_mounted_officer"),
          (faction_set_slot, ":faction_no", slot_faction_prison_guard_troop, "trp_gekokujo_dd_veteran_retainer"),
          (faction_set_slot, ":faction_no", slot_faction_castle_guard_troop, "trp_gekokujo_dd_officer"),
          (faction_set_slot, ":faction_no", slot_faction_reinforcements_a, "pt_kingdom_24_reinforcements_a"),
          (faction_set_slot, ":faction_no", slot_faction_reinforcements_b, "pt_kingdom_24_reinforcements_b"),
          (faction_set_slot, ":faction_no", slot_faction_reinforcements_c, "pt_kingdom_24_reinforcements_c"),
          
       (else_try),
          (faction_slot_eq, ":faction_no", slot_faction_culture, "fac_culture_25"),
      
          (faction_set_slot, ":faction_no", slot_faction_deserter_troop, "trp_gekokujo_zhuangnei_deserter"),
          (faction_set_slot, ":faction_no", slot_faction_guard_troop, "trp_gekokujo_zhuangnei_hatamoto_cavalry"),
          (faction_set_slot, ":faction_no", slot_faction_messenger_troop, "trp_gekokujo_zhuangnei_mounted_officer"),
          (faction_set_slot, ":faction_no", slot_faction_prison_guard_troop, "trp_gekokujo_zhuangnei_prison_guard"),
          (faction_set_slot, ":faction_no", slot_faction_castle_guard_troop, "trp_gekokujo_zhuangnei_castle_guard"),
          (faction_set_slot, ":faction_no", slot_faction_reinforcements_a, "pt_kingdom_25_reinforcements_a"),
          (faction_set_slot, ":faction_no", slot_faction_reinforcements_b, "pt_kingdom_25_reinforcements_b"),
          (faction_set_slot, ":faction_no", slot_faction_reinforcements_c, "pt_kingdom_25_reinforcements_c"),
          
        (else_try),
          (faction_slot_eq, ":faction_no", slot_faction_culture, "fac_culture_26"),
      
          (faction_set_slot, ":faction_no", slot_faction_deserter_troop, "trp_gekokujo_qt_samurai_archer"),
          (faction_set_slot, ":faction_no", slot_faction_guard_troop, "trp_gekokujo_qt_officer"),
          (faction_set_slot, ":faction_no", slot_faction_messenger_troop, "trp_gekokujo_qt_monk"),
          (faction_set_slot, ":faction_no", slot_faction_prison_guard_troop, "trp_gekokujo_qt_master_archer"),
          (faction_set_slot, ":faction_no", slot_faction_castle_guard_troop, "trp_gekokujo_qt_elite_spearman"),
          (faction_set_slot, ":faction_no", slot_faction_reinforcements_a, "pt_kingdom_26_reinforcements_a"),
          (faction_set_slot, ":faction_no", slot_faction_reinforcements_b, "pt_kingdom_26_reinforcements_b"),
          (faction_set_slot, ":faction_no", slot_faction_reinforcements_c, "pt_kingdom_26_reinforcements_c"),
          
       (else_try),
          (faction_slot_eq, ":faction_no", slot_faction_culture, "fac_culture_27"),
      
          (faction_set_slot, ":faction_no", slot_faction_deserter_troop, "trp_gekokujo_yg_deserter"),
          (faction_set_slot, ":faction_no", slot_faction_guard_troop, "trp_gekokujo_yg_hatamoto_cavalry"),
          (faction_set_slot, ":faction_no", slot_faction_messenger_troop, "trp_gekokujo_yg_messenger"),
          (faction_set_slot, ":faction_no", slot_faction_prison_guard_troop, "trp_gekokujo_yg_prison_guard"),
          (faction_set_slot, ":faction_no", slot_faction_castle_guard_troop, "trp_gekokujo_yg_castle_guard"),
          (faction_set_slot, ":faction_no", slot_faction_reinforcements_a, "pt_kingdom_27_reinforcements_a"),
          (faction_set_slot, ":faction_no", slot_faction_reinforcements_b, "pt_kingdom_27_reinforcements_b"),
          (faction_set_slot, ":faction_no", slot_faction_reinforcements_c, "pt_kingdom_27_reinforcements_c"),
          
          
       (else_try),
          (faction_slot_eq, ":faction_no", slot_faction_culture, "fac_culture_28"),
      
          (faction_set_slot, ":faction_no", slot_faction_deserter_troop, "trp_gekokujo_shimazu_deserter"),
          (faction_set_slot, ":faction_no", slot_faction_guard_troop, "trp_gekokujo_shimazu_hatamoto_gunner"),
          (faction_set_slot, ":faction_no", slot_faction_messenger_troop, "trp_gekokujo_shimazu_hatamoto_guard"),
          (faction_set_slot, ":faction_no", slot_faction_prison_guard_troop, "trp_gekokujo_shimazu_elite_spearman"),
          (faction_set_slot, ":faction_no", slot_faction_castle_guard_troop, "trp_gekokujo_shimazu_samurai_gunner"),
          (faction_set_slot, ":faction_no", slot_faction_reinforcements_a, "pt_kingdom_28_reinforcements_a"),
          (faction_set_slot, ":faction_no", slot_faction_reinforcements_b, "pt_kingdom_28_reinforcements_b"),
          (faction_set_slot, ":faction_no", slot_faction_reinforcements_c, "pt_kingdom_28_reinforcements_c"),
          
        # NE dk
        (else_try),
          (faction_slot_eq, ":faction_no", slot_faction_culture, "fac_culture_dark_knights"),
      
          (faction_set_slot, ":faction_no", slot_faction_deserter_troop, "trp_gekokujo_yg_deserter"),
          (faction_set_slot, ":faction_no", slot_faction_guard_troop, "trp_gekokujo_yg_hatamoto_cavalry"),
          (faction_set_slot, ":faction_no", slot_faction_messenger_troop, "trp_gekokujo_yg_messenger"),
          (faction_set_slot, ":faction_no", slot_faction_prison_guard_troop, "trp_gekokujo_yg_prison_guard"),
          (faction_set_slot, ":faction_no", slot_faction_castle_guard_troop, "trp_gekokujo_yg_castle_guard"),
          (faction_set_slot, ":faction_no",  slot_faction_reinforcements_a, "pt_dark_knights_reinforcements_a"),
          (faction_set_slot, ":faction_no",  slot_faction_reinforcements_b, "pt_dark_knights_reinforcements_b"),
          (faction_set_slot, ":faction_no",  slot_faction_reinforcements_c, "pt_dark_knights_reinforcements_c"),	
        # NE end dk		
#gekokujo 3.0 get rid of player culture start
#		 #gekokujo player culture units
#        (else_try),
#          (faction_slot_eq, ":faction_no", slot_faction_culture, "fac_culture_player"),
#      
#          (faction_set_slot, ":faction_no", slot_faction_deserter_troop, "trp_gekokujo_player_deserter"),
#          (faction_set_slot, ":faction_no", slot_faction_guard_troop, "trp_gekokujo_player_veteran_retainer"),
#          (faction_set_slot, ":faction_no", slot_faction_messenger_troop, "trp_gekokujo_player_messenger"),
#          (faction_set_slot, ":faction_no", slot_faction_prison_guard_troop, "trp_gekokujo_player_prison_guard"),
#          (faction_set_slot, ":faction_no", slot_faction_castle_guard_troop, "trp_gekokujo_player_castle_guard"),
#          (faction_set_slot, ":faction_no", slot_faction_reinforcements_a, "pt_kingdom_player_reinforcements_a"),
#          (faction_set_slot, ":faction_no", slot_faction_reinforcements_b, "pt_kingdom_player_reinforcements_b"),
#          (faction_set_slot, ":faction_no", slot_faction_reinforcements_c, "pt_kingdom_player_reinforcements_c"),
#gekokujo 3.0 get rid of player culture end
        (try_end),
      (try_end),
	]),
    ("initialize_item_info",
    [	 
	  # Setting food bonuses - these have been changed to incentivize using historical rations. Bread is the most cost-efficient
	  #Staples
      (item_set_slot, "itm_bread", slot_item_food_bonus, 8), #brought up from 4
      (item_set_slot, "itm_grain", slot_item_food_bonus, 2), #new - can be boiled as porridge
	  
	  #Fat sources - preserved
      (item_set_slot, "itm_smoked_fish", slot_item_food_bonus, 4),
      (item_set_slot, "itm_dried_meat", slot_item_food_bonus, 5),
      (item_set_slot, "itm_cheese", slot_item_food_bonus, 5),
      (item_set_slot, "itm_sausages", slot_item_food_bonus, 5),
      (item_set_slot, "itm_butter", slot_item_food_bonus, 4), #brought down from 8

	  #Fat sources - perishable
      (item_set_slot, "itm_chicken", slot_item_food_bonus, 8), #brought up from 7
      (item_set_slot, "itm_cattle_meat", slot_item_food_bonus, 7), #brought down from 7
      (item_set_slot, "itm_pork", slot_item_food_bonus, 6), #brought down from 6
	  
	  #Produce
      (item_set_slot, "itm_raw_olives", slot_item_food_bonus, 1),
      (item_set_slot, "itm_cabbages", slot_item_food_bonus, 2),
      (item_set_slot, "itm_raw_grapes", slot_item_food_bonus, 3),
      (item_set_slot, "itm_apples", slot_item_food_bonus, 4), #brought down from 5

	  #Sweet items
      (item_set_slot, "itm_raw_date_fruit", slot_item_food_bonus, 4), #brought down from 8
      (item_set_slot, "itm_honey", slot_item_food_bonus, 6), #brought down from 12
      
      (item_set_slot, "itm_wine", slot_item_food_bonus, 5),
      (item_set_slot, "itm_ale", slot_item_food_bonus, 4),

	  #Item economic settings	  
	  (item_set_slot, "itm_grain", slot_item_urban_demand, 20),
      (item_set_slot, "itm_grain", slot_item_rural_demand, 20),
      (item_set_slot, "itm_grain", slot_item_desert_demand, 20),
      (item_set_slot, "itm_grain", slot_item_production_slot, slot_center_acres_grain),
      (item_set_slot, "itm_grain", slot_item_production_string, "str_acres_grain"),
      (item_set_slot, "itm_grain", slot_item_base_price, 30),
	  
      (item_set_slot, "itm_bread", slot_item_urban_demand, 30),
      (item_set_slot, "itm_bread", slot_item_rural_demand, 30),
      (item_set_slot, "itm_bread", slot_item_desert_demand, 30),
      (item_set_slot, "itm_bread", slot_item_production_slot, slot_center_mills),
      (item_set_slot, "itm_bread", slot_item_production_string, "str_mills"),
      (item_set_slot, "itm_bread", slot_item_primary_raw_material, "itm_grain"),
      (item_set_slot, "itm_bread", slot_item_input_number, 6),
      (item_set_slot, "itm_bread", slot_item_output_per_run, 6),
      (item_set_slot, "itm_bread", slot_item_overhead_per_run, 30),
      (item_set_slot, "itm_bread", slot_item_base_price, 50),
      (item_set_slot, "itm_bread", slot_item_enterprise_building_cost, 1500),
	  	  
	  (item_set_slot, "itm_ale", slot_item_urban_demand, 10),
	  (item_set_slot, "itm_ale", slot_item_rural_demand, 15),
      (item_set_slot, "itm_ale", slot_item_desert_demand, 0),
      (item_set_slot, "itm_ale", slot_item_production_slot, slot_center_breweries),
      (item_set_slot, "itm_ale", slot_item_production_string, "str_breweries"),
      (item_set_slot, "itm_ale", slot_item_base_price, 120),
      (item_set_slot, "itm_ale", slot_item_primary_raw_material, "itm_grain"),
	  (item_set_slot, "itm_ale", slot_item_input_number, 1),
      (item_set_slot, "itm_ale", slot_item_output_per_run, 2),
      (item_set_slot, "itm_ale", slot_item_overhead_per_run, 50),
      (item_set_slot, "itm_ale", slot_item_base_price, 120),
      (item_set_slot, "itm_ale", slot_item_enterprise_building_cost, 2500),
	  	  
	  (item_set_slot, "itm_wine", slot_item_urban_demand, 15),
	  (item_set_slot, "itm_wine", slot_item_rural_demand, 10),
      (item_set_slot, "itm_wine", slot_item_desert_demand, 25),
      (item_set_slot, "itm_wine", slot_item_production_slot, slot_center_wine_presses),
      (item_set_slot, "itm_wine", slot_item_production_string, "str_presses"),
      (item_set_slot, "itm_wine", slot_item_primary_raw_material, "itm_raw_grapes"),
      (item_set_slot, "itm_wine", slot_item_input_number, 4),
      (item_set_slot, "itm_wine", slot_item_output_per_run, 2),
	  (item_set_slot, "itm_wine", slot_item_overhead_per_run, 60),
      (item_set_slot, "itm_wine", slot_item_base_price, 220),
      (item_set_slot, "itm_wine", slot_item_enterprise_building_cost, 5000),

	  (item_set_slot, "itm_raw_grapes", slot_item_urban_demand, 0),
	  (item_set_slot, "itm_raw_grapes", slot_item_rural_demand, 0),
      (item_set_slot, "itm_raw_grapes", slot_item_desert_demand, 0),
      (item_set_slot, "itm_raw_grapes", slot_item_production_slot, slot_center_acres_vineyard),
      (item_set_slot, "itm_raw_grapes", slot_item_production_string, "str_acres_orchard"),
      (item_set_slot, "itm_raw_grapes", slot_item_is_raw_material_only_for, "itm_wine"),
      (item_set_slot, "itm_raw_grapes", slot_item_base_price, 75),
	
	  (item_set_slot, "itm_apples", slot_item_urban_demand, 4),
	  (item_set_slot, "itm_apples", slot_item_rural_demand, 4),
	  (item_set_slot, "itm_apples", slot_item_desert_demand, 0),
      #(item_set_slot, "itm_apples", slot_item_production_slot, slot_center_acres_vineyard),
      #(item_set_slot, "itm_apples", slot_item_production_string, "str_acres_orchard"),
      (item_set_slot, "itm_apples", slot_item_production_slot, slot_center_household_gardens),
      (item_set_slot, "itm_apples", slot_item_production_string, "str_gardens"),
      (item_set_slot, "itm_apples", slot_item_base_price, 44),
	  
      (item_set_slot, "itm_smoked_fish", slot_item_urban_demand, 16),
      (item_set_slot, "itm_smoked_fish", slot_item_rural_demand, 16),
      (item_set_slot, "itm_smoked_fish", slot_item_desert_demand, 16),
      (item_set_slot, "itm_smoked_fish", slot_item_production_slot, slot_center_fishing_fleet),
      (item_set_slot, "itm_smoked_fish", slot_item_production_string, "str_boats"),

      (item_set_slot, "itm_salt", slot_item_urban_demand, 5),
      (item_set_slot, "itm_salt", slot_item_rural_demand, 3),
      (item_set_slot, "itm_salt", slot_item_desert_demand, -1),
      (item_set_slot, "itm_salt", slot_item_production_slot, slot_center_salt_pans),
      (item_set_slot, "itm_salt", slot_item_production_string, "str_pans"),
	  
      (item_set_slot, "itm_dried_meat", slot_item_urban_demand, 20),
      (item_set_slot, "itm_dried_meat", slot_item_rural_demand, 5),
      (item_set_slot, "itm_dried_meat", slot_item_desert_demand, -1),
      #(item_set_slot, "itm_dried_meat", slot_item_production_slot, slot_center_head_cattle),
      #(item_set_slot, "itm_dried_meat", slot_item_production_string, "str_head_cattle"),
      (item_set_slot, "itm_sausages", slot_item_production_slot, slot_center_head_sheep),
      (item_set_slot, "itm_sausages", slot_item_production_string, "str_head_sheep"),

	  #Gekokujo reduce demand by 1/5 overall
      #(item_set_slot, "itm_cattle_meat", slot_item_urban_demand, 12),
      #(item_set_slot, "itm_cattle_meat", slot_item_rural_demand, 3),
      (item_set_slot, "itm_cattle_meat", slot_item_urban_demand, 5),
      (item_set_slot, "itm_cattle_meat", slot_item_rural_demand, 0),
      (item_set_slot, "itm_cattle_meat", slot_item_desert_demand, -1),
      (item_set_slot, "itm_cattle_meat", slot_item_production_slot, slot_center_head_cattle),
      (item_set_slot, "itm_cattle_meat", slot_item_production_string, "str_head_cattle"),
	  (item_set_slot, "itm_cattle_meat", slot_item_production_slot, slot_center_fur_traps),
	  (item_set_slot, "itm_cattle_meat", slot_item_production_string, "str_traps"),

      (item_set_slot, "itm_cheese", slot_item_urban_demand, 10),
      (item_set_slot, "itm_cheese", slot_item_rural_demand, 10),
      (item_set_slot, "itm_cheese", slot_item_desert_demand, 10),
      #(item_set_slot, "itm_cheese", slot_item_production_slot, slot_center_head_cattle),
      #(item_set_slot, "itm_cheese", slot_item_production_string, "str_head_cattle"),
      (item_set_slot, "itm_cheese", slot_item_production_slot, slot_center_acres_vineyard),
      (item_set_slot, "itm_cheese", slot_item_production_string, "str_acres_orchard"),

      (item_set_slot, "itm_butter", slot_item_urban_demand, 2),
      (item_set_slot, "itm_butter", slot_item_rural_demand, 2),
      (item_set_slot, "itm_butter", slot_item_desert_demand, 2),
      #(item_set_slot, "itm_butter", slot_item_production_slot, slot_center_head_cattle),
      #(item_set_slot, "itm_butter", slot_item_production_string, "str_head_cattle"),
      (item_set_slot, "itm_butter", slot_item_production_slot, slot_center_acres_vineyard),
      (item_set_slot, "itm_butter", slot_item_production_string, "str_acres_orchard"),

	  #Gekokujo get leatherwork demand down to match new supply
      #(item_set_slot, "itm_leatherwork", slot_item_urban_demand, 10),
      #(item_set_slot, "itm_leatherwork", slot_item_rural_demand, 10),
      #(item_set_slot, "itm_leatherwork", slot_item_desert_demand, 10),
      (item_set_slot, "itm_leatherwork", slot_item_urban_demand, 2),
      (item_set_slot, "itm_leatherwork", slot_item_rural_demand, 2),
      (item_set_slot, "itm_leatherwork", slot_item_desert_demand, 2),
      (item_set_slot, "itm_leatherwork", slot_item_production_slot, slot_center_tanneries),
      (item_set_slot, "itm_leatherwork", slot_item_production_string, "str_tanneries"),
      (item_set_slot, "itm_leatherwork", slot_item_primary_raw_material, "itm_raw_leather"),
      (item_set_slot, "itm_leatherwork", slot_item_input_number, 3),
      (item_set_slot, "itm_leatherwork", slot_item_output_per_run, 3),
      (item_set_slot, "itm_leatherwork", slot_item_overhead_per_run, 50),
	  (item_set_slot, "itm_leatherwork", slot_item_base_price, 220),
	  (item_set_slot, "itm_leatherwork", slot_item_enterprise_building_cost, 8000),

      (item_set_slot, "itm_raw_leather", slot_item_urban_demand, 0),
      (item_set_slot, "itm_raw_leather", slot_item_rural_demand, 0),
      (item_set_slot, "itm_raw_leather", slot_item_desert_demand, 0),
      (item_set_slot, "itm_raw_leather", slot_item_production_slot, slot_center_head_cattle),
      (item_set_slot, "itm_raw_leather", slot_item_production_string, "str_head_cattle"),
      (item_set_slot, "itm_raw_leather", slot_item_is_raw_material_only_for, "itm_leatherwork"),
	  (item_set_slot, "itm_raw_leather", slot_item_base_price, 120),
	  	  
  	  (item_set_slot, "itm_sausages", slot_item_urban_demand, 12),
	  (item_set_slot, "itm_sausages", slot_item_rural_demand, 3),
	  (item_set_slot, "itm_sausages", slot_item_desert_demand, -1),
      (item_set_slot, "itm_sausages", slot_item_production_slot, slot_center_head_sheep),
      (item_set_slot, "itm_sausages", slot_item_production_string, "str_head_sheep"),
	  
	  (item_set_slot, "itm_wool", slot_item_urban_demand, 0),
	  (item_set_slot, "itm_wool", slot_item_rural_demand, 0),
	  (item_set_slot, "itm_wool", slot_item_desert_demand, 0),
      #(item_set_slot, "itm_wool", slot_item_production_slot, slot_center_head_sheep),
      #(item_set_slot, "itm_wool", slot_item_production_string, "str_head_sheep"),
      (item_set_slot, "itm_wool", slot_item_production_slot, slot_center_acres_olives),
      (item_set_slot, "itm_wool", slot_item_production_string, "str_olive_groves"),
	  (item_set_slot, "itm_wool", slot_item_is_raw_material_only_for, "itm_wool_cloth"),
	  (item_set_slot, "itm_wool", slot_item_base_price,130),

	  (item_set_slot, "itm_wool_cloth", slot_item_urban_demand, 15),
	  (item_set_slot, "itm_wool_cloth", slot_item_rural_demand, 20),
	  (item_set_slot, "itm_wool_cloth", slot_item_desert_demand, 5),
      (item_set_slot, "itm_wool_cloth", slot_item_production_slot, slot_center_wool_looms),
      (item_set_slot, "itm_wool_cloth", slot_item_production_string, "str_looms"),
	  (item_set_slot, "itm_wool_cloth", slot_item_primary_raw_material, "itm_wool"),
      (item_set_slot, "itm_wool_cloth", slot_item_input_number, 2),
      (item_set_slot, "itm_wool_cloth", slot_item_output_per_run, 2),
      (item_set_slot, "itm_wool_cloth", slot_item_overhead_per_run, 120),
	  (item_set_slot, "itm_wool_cloth", slot_item_base_price, 250),
	  (item_set_slot, "itm_wool_cloth", slot_item_enterprise_building_cost, 6000),
	  
	  (item_set_slot, "itm_raw_flax", slot_item_urban_demand, 0),
	  (item_set_slot, "itm_raw_flax", slot_item_rural_demand, 0),
	  (item_set_slot, "itm_raw_flax", slot_item_desert_demand, 0),
      (item_set_slot, "itm_raw_flax", slot_item_production_slot, slot_center_acres_flax),
      (item_set_slot, "itm_raw_flax", slot_item_production_string, "str_acres_flax"),
      (item_set_slot, "itm_raw_flax", slot_item_is_raw_material_only_for, "itm_linen"),
	  (item_set_slot, "itm_raw_flax", slot_item_base_price, 150),

	  (item_set_slot, "itm_linen", slot_item_urban_demand, 7),
	  (item_set_slot, "itm_linen", slot_item_rural_demand, 3),
	  (item_set_slot, "itm_linen", slot_item_desert_demand, 15),
      (item_set_slot, "itm_linen", slot_item_production_slot, slot_center_linen_looms),
      (item_set_slot, "itm_linen", slot_item_production_string, "str_looms"),
      (item_set_slot, "itm_linen", slot_item_primary_raw_material, "itm_raw_flax"),
      (item_set_slot, "itm_linen", slot_item_input_number, 2),
      (item_set_slot, "itm_linen", slot_item_output_per_run, 2),
      (item_set_slot, "itm_linen", slot_item_overhead_per_run, 120),
	  (item_set_slot, "itm_linen", slot_item_base_price, 250),
	  (item_set_slot, "itm_linen", slot_item_enterprise_building_cost, 6000),
	  
	  (item_set_slot, "itm_iron", slot_item_urban_demand, 0),
	  (item_set_slot, "itm_iron", slot_item_rural_demand, 0),
	  (item_set_slot, "itm_iron", slot_item_desert_demand, 0),
      (item_set_slot, "itm_iron", slot_item_production_slot, slot_center_iron_deposits),
      (item_set_slot, "itm_iron", slot_item_production_string, "str_deposits"),
      (item_set_slot, "itm_iron", slot_item_is_raw_material_only_for, "itm_tools"),
	  (item_set_slot, "itm_iron", slot_item_base_price, 264),
	  
	  (item_set_slot, "itm_tools", slot_item_urban_demand, 7),
	  (item_set_slot, "itm_tools", slot_item_rural_demand, 7),
	  (item_set_slot, "itm_tools", slot_item_desert_demand, 7),
      (item_set_slot, "itm_tools", slot_item_production_slot, slot_center_smithies),
      (item_set_slot, "itm_tools", slot_item_production_string, "str_smithies"),
      (item_set_slot, "itm_tools", slot_item_primary_raw_material, "itm_iron"),
      (item_set_slot, "itm_tools", slot_item_input_number, 2),
      (item_set_slot, "itm_tools", slot_item_output_per_run, 2),
      (item_set_slot, "itm_tools", slot_item_overhead_per_run, 60),
	  (item_set_slot, "itm_tools", slot_item_base_price, 410),
	  (item_set_slot, "itm_tools", slot_item_enterprise_building_cost, 3500),
	  	  
	  (item_set_slot, "itm_pottery", slot_item_urban_demand, 15),
	  (item_set_slot, "itm_pottery", slot_item_rural_demand, 5),
	  (item_set_slot, "itm_pottery", slot_item_desert_demand, -1),
      (item_set_slot, "itm_pottery", slot_item_production_slot, slot_center_pottery_kilns),
      (item_set_slot, "itm_pottery", slot_item_production_string, "str_kilns"),
	  	  
	  (item_set_slot, "itm_oil", slot_item_urban_demand, 10),
	  (item_set_slot, "itm_oil", slot_item_rural_demand, 5),
	  (item_set_slot, "itm_oil", slot_item_desert_demand, -1),
      (item_set_slot, "itm_oil", slot_item_production_slot, slot_center_olive_presses),
      (item_set_slot, "itm_oil", slot_item_production_string, "str_presses"),
      (item_set_slot, "itm_oil", slot_item_primary_raw_material, "itm_raw_olives"),	
      (item_set_slot, "itm_oil", slot_item_input_number, 6),
      (item_set_slot, "itm_oil", slot_item_output_per_run, 2),
      (item_set_slot, "itm_oil", slot_item_overhead_per_run, 80),
	  (item_set_slot, "itm_oil", slot_item_base_price, 450),
	  (item_set_slot, "itm_oil", slot_item_enterprise_building_cost, 4500),
	
	  (item_set_slot, "itm_raw_olives", slot_item_urban_demand, 0),
	  (item_set_slot, "itm_raw_olives", slot_item_rural_demand, 0),
	  (item_set_slot, "itm_raw_olives", slot_item_desert_demand, 0),
      #(item_set_slot, "itm_raw_olives", slot_item_production_slot, slot_center_acres_olives),
      #(item_set_slot, "itm_raw_olives", slot_item_production_string, "str_olive_groves"),
      (item_set_slot, "itm_raw_olives", slot_item_production_slot, slot_center_apiaries),
      (item_set_slot, "itm_raw_olives", slot_item_production_string, "str_hives"),
      (item_set_slot, "itm_raw_olives", slot_item_is_raw_material_only_for, "itm_oil"),
	  (item_set_slot, "itm_raw_olives", slot_item_base_price, 100),
	 
	  (item_set_slot, "itm_velvet", slot_item_urban_demand, 5),
	  (item_set_slot, "itm_velvet", slot_item_rural_demand, 0),
	  (item_set_slot, "itm_velvet", slot_item_desert_demand, -1),
      (item_set_slot, "itm_velvet", slot_item_production_slot, slot_center_silk_looms),
      (item_set_slot, "itm_velvet", slot_item_production_string, "str_looms"),
	  (item_set_slot, "itm_velvet", slot_item_primary_raw_material, "itm_raw_silk"),
      (item_set_slot, "itm_velvet", slot_item_input_number, 2),
      (item_set_slot, "itm_velvet", slot_item_output_per_run, 2),
	  #gekokujo 3.0 dyeworks rebalance, 2x overhead increase
      #(item_set_slot, "itm_velvet", slot_item_overhead_per_run, 160),
      (item_set_slot, "itm_velvet", slot_item_overhead_per_run, 320),
	  (item_set_slot, "itm_velvet", slot_item_base_price, 1025),
	  (item_set_slot, "itm_velvet", slot_item_secondary_raw_material, "itm_raw_dyes"),
	  #gekokujo 3.0 dyeworks rebalance, 1.6x building cost
	  #(item_set_slot, "itm_velvet", slot_item_enterprise_building_cost, 10000),
	  (item_set_slot, "itm_velvet", slot_item_enterprise_building_cost, 16000),
	
	  (item_set_slot, "itm_raw_silk", slot_item_urban_demand, 0),
	  (item_set_slot, "itm_raw_silk", slot_item_rural_demand, 0),
      (item_set_slot, "itm_raw_silk", slot_item_production_slot, slot_center_silk_farms),
      (item_set_slot, "itm_raw_silk", slot_item_production_string, "str_mulberry_groves"),
      (item_set_slot, "itm_raw_silk", slot_item_is_raw_material_only_for, "itm_velvet"),
      (item_set_slot, "itm_raw_silk", slot_item_base_price, 600),

	  (item_set_slot, "itm_raw_dyes", slot_item_urban_demand, 3),
	  (item_set_slot, "itm_raw_dyes", slot_item_rural_demand, 0),
	  (item_set_slot, "itm_raw_dyes", slot_item_desert_demand, -1),
	  (item_set_slot, "itm_raw_dyes", slot_item_production_string, "str_caravans"),
	  (item_set_slot, "itm_raw_dyes", slot_item_base_price, 200),
	  
	  (item_set_slot, "itm_spice", slot_item_urban_demand, 5),
	  (item_set_slot, "itm_spice", slot_item_rural_demand, 0),
	  (item_set_slot, "itm_spice", slot_item_desert_demand, 5),
	  (item_set_slot, "itm_spice", slot_item_production_string, "str_caravans"),
	  
	  (item_set_slot, "itm_furs", slot_item_urban_demand, 5),
	  (item_set_slot, "itm_furs", slot_item_rural_demand, 0),
	  (item_set_slot, "itm_furs", slot_item_desert_demand, -1),
	  (item_set_slot, "itm_furs", slot_item_production_slot, slot_center_fur_traps),
	  (item_set_slot, "itm_furs", slot_item_production_string, "str_traps"),

      (item_set_slot, "itm_honey", slot_item_urban_demand, 12),
      (item_set_slot, "itm_honey", slot_item_rural_demand, 3),
      (item_set_slot, "itm_honey", slot_item_desert_demand, -1),
      #(item_set_slot, "itm_honey", slot_item_production_slot, slot_center_apiaries),
      #(item_set_slot, "itm_honey", slot_item_production_string, "str_hives"),
      (item_set_slot, "itm_honey", slot_item_production_slot, slot_center_acres_vineyard),
      (item_set_slot, "itm_honey", slot_item_production_string, "str_acres_orchard"),
	  
      (item_set_slot, "itm_cabbages", slot_item_urban_demand, 7),
      (item_set_slot, "itm_cabbages", slot_item_rural_demand, 7),
      (item_set_slot, "itm_cabbages", slot_item_desert_demand, 7),
      (item_set_slot, "itm_cabbages", slot_item_production_slot, slot_center_household_gardens),
      (item_set_slot, "itm_cabbages", slot_item_production_string, "str_gardens"),

      (item_set_slot, "itm_raw_date_fruit", slot_item_urban_demand, 7),
      (item_set_slot, "itm_raw_date_fruit", slot_item_rural_demand, 7),
      (item_set_slot, "itm_raw_date_fruit", slot_item_desert_demand, 7),
      (item_set_slot, "itm_raw_date_fruit", slot_item_production_slot, slot_center_household_gardens),
      (item_set_slot, "itm_raw_date_fruit", slot_item_production_string, "str_acres_oasis"),
	  	  
      #(item_set_slot, "itm_chicken", slot_item_urban_demand, 40),
      (item_set_slot, "itm_chicken", slot_item_urban_demand, 10),
      (item_set_slot, "itm_chicken", slot_item_rural_demand, 10),
      (item_set_slot, "itm_chicken", slot_item_desert_demand, -1),

      #(item_set_slot, "itm_pork", slot_item_urban_demand, 40),
      (item_set_slot, "itm_pork", slot_item_urban_demand, 10),
      (item_set_slot, "itm_pork", slot_item_rural_demand, 10),
      (item_set_slot, "itm_pork", slot_item_desert_demand, -1),

      # Setting book intelligence requirements
      (item_set_slot, "itm_book_tactics", slot_item_intelligence_requirement, 9),
      (item_set_slot, "itm_book_persuasion", slot_item_intelligence_requirement, 8),
      (item_set_slot, "itm_book_leadership", slot_item_intelligence_requirement, 7),
      (item_set_slot, "itm_book_intelligence", slot_item_intelligence_requirement, 10),
      (item_set_slot, "itm_book_trade", slot_item_intelligence_requirement, 11),
      (item_set_slot, "itm_book_weapon_mastery", slot_item_intelligence_requirement, 9),
      (item_set_slot, "itm_book_engineering", slot_item_intelligence_requirement, 12),

      (item_set_slot, "itm_book_wound_treatment_reference", slot_item_intelligence_requirement, 10),
      (item_set_slot, "itm_book_training_reference", slot_item_intelligence_requirement, 10),
      (item_set_slot, "itm_book_surgery_reference", slot_item_intelligence_requirement, 10),	 
	 ]),
    ("initialize_town_arena_info",
    [
      (try_for_range, ":town_no", towns_begin, towns_end),
		#gekokujo 3.0 tournaments ought to be smaller affairs
        #(party_set_slot, ":town_no", slot_town_tournament_max_teams, 4),
        #(party_set_slot, ":town_no", slot_town_tournament_max_team_size, 8),
        (party_set_slot, ":town_no", slot_town_tournament_max_teams, 2),
        (party_set_slot, ":town_no", slot_town_tournament_max_team_size, 4),
      (try_end),
      (party_set_slot, "p_town_6", slot_town_tournament_max_team_size, 2),

      (party_set_slot,"p_town_1", slot_town_arena_melee_1_num_teams,   2),
      (party_set_slot,"p_town_1", slot_town_arena_melee_1_team_size,   1),
      (party_set_slot,"p_town_1", slot_town_arena_melee_2_num_teams,   4),
      (party_set_slot,"p_town_1", slot_town_arena_melee_2_team_size,   1),
      (party_set_slot,"p_town_1", slot_town_arena_melee_3_num_teams,   4),
      (party_set_slot,"p_town_1", slot_town_arena_melee_3_team_size,   1),
	  
      (party_set_slot,"p_town_2", slot_town_arena_melee_1_num_teams,   4),
      (party_set_slot,"p_town_2", slot_town_arena_melee_1_team_size,   4),
      (party_set_slot,"p_town_2", slot_town_arena_melee_2_num_teams,   4),
      (party_set_slot,"p_town_2", slot_town_arena_melee_2_team_size,   6),
      (party_set_slot,"p_town_2", slot_town_arena_melee_3_num_teams,   4),
      (party_set_slot,"p_town_2", slot_town_arena_melee_3_team_size,   8),

      (party_set_slot,"p_town_3", slot_town_arena_melee_1_num_teams,   2),
      (party_set_slot,"p_town_3", slot_town_arena_melee_1_team_size,   8),
      (party_set_slot,"p_town_3", slot_town_arena_melee_2_num_teams,   2),
      (party_set_slot,"p_town_3", slot_town_arena_melee_2_team_size,   8),
      (party_set_slot,"p_town_3", slot_town_arena_melee_3_num_teams,   2),
      (party_set_slot,"p_town_3", slot_town_arena_melee_3_team_size,   8),

      (party_set_slot,"p_town_4", slot_town_arena_melee_1_num_teams,   2),
      (party_set_slot,"p_town_4", slot_town_arena_melee_1_team_size,   8),
      (party_set_slot,"p_town_4", slot_town_arena_melee_2_num_teams,   3),
      (party_set_slot,"p_town_4", slot_town_arena_melee_2_team_size,   8),
      (party_set_slot,"p_town_4", slot_town_arena_melee_3_num_teams,   2),
      (party_set_slot,"p_town_4", slot_town_arena_melee_3_team_size,   5),
      
      (party_set_slot,"p_town_5", slot_town_arena_melee_1_num_teams,   2),
      (party_set_slot,"p_town_5", slot_town_arena_melee_1_team_size,   3),
      (party_set_slot,"p_town_5", slot_town_arena_melee_2_num_teams,   2),
      (party_set_slot,"p_town_5", slot_town_arena_melee_2_team_size,   5),
      (party_set_slot,"p_town_5", slot_town_arena_melee_3_num_teams,   2),
      (party_set_slot,"p_town_5", slot_town_arena_melee_3_team_size,   8),

      (party_set_slot,"p_town_6", slot_town_arena_melee_1_num_teams,   2),
      (party_set_slot,"p_town_6", slot_town_arena_melee_1_team_size,   4),
      (party_set_slot,"p_town_6", slot_town_arena_melee_2_num_teams,   3),
      (party_set_slot,"p_town_6", slot_town_arena_melee_2_team_size,   4),
      (party_set_slot,"p_town_6", slot_town_arena_melee_3_num_teams,   3),
      (party_set_slot,"p_town_6", slot_town_arena_melee_3_team_size,   6),

      (party_set_slot,"p_town_7", slot_town_arena_melee_1_num_teams,   4),
      (party_set_slot,"p_town_7", slot_town_arena_melee_1_team_size,   4),
      (party_set_slot,"p_town_7", slot_town_arena_melee_2_num_teams,   4),
      (party_set_slot,"p_town_7", slot_town_arena_melee_2_team_size,   6),
      (party_set_slot,"p_town_7", slot_town_arena_melee_3_num_teams,   4),
      (party_set_slot,"p_town_7", slot_town_arena_melee_3_team_size,   8),

      (party_set_slot,"p_town_8", slot_town_arena_melee_1_num_teams,   3),
      (party_set_slot,"p_town_8", slot_town_arena_melee_1_team_size,   1),
      (party_set_slot,"p_town_8", slot_town_arena_melee_2_num_teams,   3),
      (party_set_slot,"p_town_8", slot_town_arena_melee_2_team_size,   3),
      (party_set_slot,"p_town_8", slot_town_arena_melee_3_num_teams,   3),
      (party_set_slot,"p_town_8", slot_town_arena_melee_3_team_size,   7),

      (party_set_slot,"p_town_9", slot_town_arena_melee_1_num_teams,   2),
      (party_set_slot,"p_town_9", slot_town_arena_melee_1_team_size,   2),
      (party_set_slot,"p_town_9", slot_town_arena_melee_2_num_teams,   2),
      (party_set_slot,"p_town_9", slot_town_arena_melee_2_team_size,   5),
      (party_set_slot,"p_town_9", slot_town_arena_melee_3_num_teams,   2),
      (party_set_slot,"p_town_9", slot_town_arena_melee_3_team_size,   8),

      (party_set_slot,"p_town_10", slot_town_arena_melee_1_num_teams,   2),
      (party_set_slot,"p_town_10", slot_town_arena_melee_1_team_size,   3),
      (party_set_slot,"p_town_10", slot_town_arena_melee_2_num_teams,   2),
      (party_set_slot,"p_town_10", slot_town_arena_melee_2_team_size,   5),
      (party_set_slot,"p_town_10", slot_town_arena_melee_3_num_teams,   2),
      (party_set_slot,"p_town_10", slot_town_arena_melee_3_team_size,   8),

      (party_set_slot,"p_town_11", slot_town_arena_melee_1_num_teams,   2),
      (party_set_slot,"p_town_11", slot_town_arena_melee_1_team_size,   8),
      (party_set_slot,"p_town_11", slot_town_arena_melee_2_num_teams,   3),
      (party_set_slot,"p_town_11", slot_town_arena_melee_2_team_size,   4),
      (party_set_slot,"p_town_11", slot_town_arena_melee_3_num_teams,   3),
      (party_set_slot,"p_town_11", slot_town_arena_melee_3_team_size,   6),

      (party_set_slot,"p_town_12", slot_town_arena_melee_1_num_teams,   3),
      (party_set_slot,"p_town_12", slot_town_arena_melee_1_team_size,   8),
      (party_set_slot,"p_town_12", slot_town_arena_melee_2_num_teams,   4),
      (party_set_slot,"p_town_12", slot_town_arena_melee_2_team_size,   6),
      (party_set_slot,"p_town_12", slot_town_arena_melee_3_num_teams,   4),
      (party_set_slot,"p_town_12", slot_town_arena_melee_3_team_size,   5),

      (party_set_slot,"p_town_13", slot_town_arena_melee_1_num_teams,   2),
      (party_set_slot,"p_town_13", slot_town_arena_melee_1_team_size,   8),
      (party_set_slot,"p_town_13", slot_town_arena_melee_2_num_teams,   4),
      (party_set_slot,"p_town_13", slot_town_arena_melee_2_team_size,   5),
      (party_set_slot,"p_town_13", slot_town_arena_melee_3_num_teams,   4),
      (party_set_slot,"p_town_13", slot_town_arena_melee_3_team_size,   7),

      (party_set_slot,"p_town_14", slot_town_arena_melee_1_num_teams,   2),
      (party_set_slot,"p_town_14", slot_town_arena_melee_1_team_size,   4),
      (party_set_slot,"p_town_14", slot_town_arena_melee_2_num_teams,   2),
      (party_set_slot,"p_town_14", slot_town_arena_melee_2_team_size,   5),
      (party_set_slot,"p_town_14", slot_town_arena_melee_3_num_teams,   2),
      (party_set_slot,"p_town_14", slot_town_arena_melee_3_team_size,   6),

      (party_set_slot,"p_town_15", slot_town_arena_melee_1_num_teams,   2),
      (party_set_slot,"p_town_15", slot_town_arena_melee_1_team_size,   8),
      (party_set_slot,"p_town_15", slot_town_arena_melee_2_num_teams,   3),
      (party_set_slot,"p_town_15", slot_town_arena_melee_2_team_size,   4),
      (party_set_slot,"p_town_15", slot_town_arena_melee_3_num_teams,   3),
      (party_set_slot,"p_town_15", slot_town_arena_melee_3_team_size,   6),

      (party_set_slot,"p_town_16", slot_town_arena_melee_1_num_teams,   3),
      (party_set_slot,"p_town_16", slot_town_arena_melee_1_team_size,   8),
      (party_set_slot,"p_town_16", slot_town_arena_melee_2_num_teams,   4),
      (party_set_slot,"p_town_16", slot_town_arena_melee_2_team_size,   6),
      (party_set_slot,"p_town_16", slot_town_arena_melee_3_num_teams,   4),
      (party_set_slot,"p_town_16", slot_town_arena_melee_3_team_size,   5),

      (party_set_slot,"p_town_17", slot_town_arena_melee_1_num_teams,   2),
      (party_set_slot,"p_town_17", slot_town_arena_melee_1_team_size,   8),
      (party_set_slot,"p_town_17", slot_town_arena_melee_2_num_teams,   4),
      (party_set_slot,"p_town_17", slot_town_arena_melee_2_team_size,   5),
      (party_set_slot,"p_town_17", slot_town_arena_melee_3_num_teams,   4),
      (party_set_slot,"p_town_17", slot_town_arena_melee_3_team_size,   7),

      (party_set_slot,"p_town_18", slot_town_arena_melee_1_num_teams,   2),
      (party_set_slot,"p_town_18", slot_town_arena_melee_1_team_size,   4),
      (party_set_slot,"p_town_18", slot_town_arena_melee_2_num_teams,   2),
      (party_set_slot,"p_town_18", slot_town_arena_melee_2_team_size,   5),
      (party_set_slot,"p_town_18", slot_town_arena_melee_3_num_teams,   2),
      (party_set_slot,"p_town_18", slot_town_arena_melee_3_team_size,   6),

      (party_set_slot,"p_town_19", slot_town_arena_melee_1_num_teams,   2),
      (party_set_slot,"p_town_19", slot_town_arena_melee_1_team_size,   8),
      (party_set_slot,"p_town_19", slot_town_arena_melee_2_num_teams,   4),
      (party_set_slot,"p_town_19", slot_town_arena_melee_2_team_size,   4),
      (party_set_slot,"p_town_19", slot_town_arena_melee_3_num_teams,   4),
      (party_set_slot,"p_town_19", slot_town_arena_melee_3_team_size,   6),

      (party_set_slot,"p_town_20", slot_town_arena_melee_1_num_teams,   4),
      (party_set_slot,"p_town_20", slot_town_arena_melee_1_team_size,   2),
      (party_set_slot,"p_town_20", slot_town_arena_melee_2_num_teams,   4),
      (party_set_slot,"p_town_20", slot_town_arena_melee_2_team_size,   4),
      (party_set_slot,"p_town_20", slot_town_arena_melee_3_num_teams,   4),
      (party_set_slot,"p_town_20", slot_town_arena_melee_3_team_size,   6),

      (party_set_slot,"p_town_21", slot_town_arena_melee_1_num_teams,   3),
      (party_set_slot,"p_town_21", slot_town_arena_melee_1_team_size,   3),
      (party_set_slot,"p_town_21", slot_town_arena_melee_2_num_teams,   2),
      (party_set_slot,"p_town_21", slot_town_arena_melee_2_team_size,   6),
      (party_set_slot,"p_town_21", slot_town_arena_melee_3_num_teams,   2),
      (party_set_slot,"p_town_21", slot_town_arena_melee_3_team_size,   8),

      (party_set_slot,"p_town_22", slot_town_arena_melee_1_num_teams,   4),
      (party_set_slot,"p_town_22", slot_town_arena_melee_1_team_size,   3),
      (party_set_slot,"p_town_22", slot_town_arena_melee_2_num_teams,   3),
      (party_set_slot,"p_town_22", slot_town_arena_melee_2_team_size,   4),
      (party_set_slot,"p_town_22", slot_town_arena_melee_3_num_teams,   2),
      (party_set_slot,"p_town_22", slot_town_arena_melee_3_team_size,   6),
	  
#gekokujo arena info
      (party_set_slot,"p_town_23", slot_town_arena_melee_1_num_teams,   2),
      (party_set_slot,"p_town_23", slot_town_arena_melee_1_team_size,   8),
      (party_set_slot,"p_town_23", slot_town_arena_melee_2_num_teams,   2),
      (party_set_slot,"p_town_23", slot_town_arena_melee_2_team_size,   8),
      (party_set_slot,"p_town_23", slot_town_arena_melee_3_num_teams,   2),
      (party_set_slot,"p_town_23", slot_town_arena_melee_3_team_size,   8),

      (party_set_slot,"p_town_24", slot_town_arena_melee_1_num_teams,   2),
      (party_set_slot,"p_town_24", slot_town_arena_melee_1_team_size,   8),
      (party_set_slot,"p_town_24", slot_town_arena_melee_2_num_teams,   3),
      (party_set_slot,"p_town_24", slot_town_arena_melee_2_team_size,   8),
      (party_set_slot,"p_town_24", slot_town_arena_melee_3_num_teams,   2),
      (party_set_slot,"p_town_24", slot_town_arena_melee_3_team_size,   5),
      
      (party_set_slot,"p_town_25", slot_town_arena_melee_1_num_teams,   2),
      (party_set_slot,"p_town_25", slot_town_arena_melee_1_team_size,   3),
      (party_set_slot,"p_town_25", slot_town_arena_melee_2_num_teams,   2),
      (party_set_slot,"p_town_25", slot_town_arena_melee_2_team_size,   5),
      (party_set_slot,"p_town_25", slot_town_arena_melee_3_num_teams,   2),
      (party_set_slot,"p_town_25", slot_town_arena_melee_3_team_size,   8),

      (party_set_slot,"p_town_26", slot_town_arena_melee_1_num_teams,   2),
      (party_set_slot,"p_town_26", slot_town_arena_melee_1_team_size,   4),
      (party_set_slot,"p_town_26", slot_town_arena_melee_2_num_teams,   3),
      (party_set_slot,"p_town_26", slot_town_arena_melee_2_team_size,   4),
      (party_set_slot,"p_town_26", slot_town_arena_melee_3_num_teams,   3),
      (party_set_slot,"p_town_26", slot_town_arena_melee_3_team_size,   6),

      (party_set_slot,"p_town_27", slot_town_arena_melee_1_num_teams,   4),
      (party_set_slot,"p_town_27", slot_town_arena_melee_1_team_size,   4),
      (party_set_slot,"p_town_27", slot_town_arena_melee_2_num_teams,   4),
      (party_set_slot,"p_town_27", slot_town_arena_melee_2_team_size,   6),
      (party_set_slot,"p_town_27", slot_town_arena_melee_3_num_teams,   4),
      (party_set_slot,"p_town_27", slot_town_arena_melee_3_team_size,   8),

      (party_set_slot,"p_town_28", slot_town_arena_melee_1_num_teams,   3),
      (party_set_slot,"p_town_28", slot_town_arena_melee_1_team_size,   1),
      (party_set_slot,"p_town_28", slot_town_arena_melee_2_num_teams,   3),
      (party_set_slot,"p_town_28", slot_town_arena_melee_2_team_size,   3),
      (party_set_slot,"p_town_28", slot_town_arena_melee_3_num_teams,   3),
      (party_set_slot,"p_town_28", slot_town_arena_melee_3_team_size,   7),

      (party_set_slot,"p_town_29", slot_town_arena_melee_1_num_teams,   2),
      (party_set_slot,"p_town_29", slot_town_arena_melee_1_team_size,   2),
      (party_set_slot,"p_town_29", slot_town_arena_melee_2_num_teams,   2),
      (party_set_slot,"p_town_29", slot_town_arena_melee_2_team_size,   5),
      (party_set_slot,"p_town_29", slot_town_arena_melee_3_num_teams,   2),
      (party_set_slot,"p_town_29", slot_town_arena_melee_3_team_size,   8),

      (party_set_slot,"p_town_30", slot_town_arena_melee_1_num_teams,   2),
      (party_set_slot,"p_town_30", slot_town_arena_melee_1_team_size,   3),
      (party_set_slot,"p_town_30", slot_town_arena_melee_2_num_teams,   2),
      (party_set_slot,"p_town_30", slot_town_arena_melee_2_team_size,   5),
      (party_set_slot,"p_town_30", slot_town_arena_melee_3_num_teams,   2),
      (party_set_slot,"p_town_30", slot_town_arena_melee_3_team_size,   8),

      (party_set_slot,"p_town_31", slot_town_arena_melee_1_num_teams,   2),
      (party_set_slot,"p_town_31", slot_town_arena_melee_1_team_size,   8),
      (party_set_slot,"p_town_31", slot_town_arena_melee_2_num_teams,   3),
      (party_set_slot,"p_town_31", slot_town_arena_melee_2_team_size,   4),
      (party_set_slot,"p_town_31", slot_town_arena_melee_3_num_teams,   3),
      (party_set_slot,"p_town_31", slot_town_arena_melee_3_team_size,   6),

      (party_set_slot,"p_town_32", slot_town_arena_melee_1_num_teams,   2),
      (party_set_slot,"p_town_32", slot_town_arena_melee_1_team_size,   8),
      (party_set_slot,"p_town_32", slot_town_arena_melee_2_num_teams,   3),
      (party_set_slot,"p_town_32", slot_town_arena_melee_2_team_size,   4),
      (party_set_slot,"p_town_32", slot_town_arena_melee_3_num_teams,   3),
      (party_set_slot,"p_town_32", slot_town_arena_melee_3_team_size,   6),

      (party_set_slot,"p_town_33", slot_town_arena_melee_1_num_teams,   2),
      (party_set_slot,"p_town_33", slot_town_arena_melee_1_team_size,   8),
      (party_set_slot,"p_town_33", slot_town_arena_melee_2_num_teams,   3),
      (party_set_slot,"p_town_33", slot_town_arena_melee_2_team_size,   4),
      (party_set_slot,"p_town_33", slot_town_arena_melee_3_num_teams,   3),
      (party_set_slot,"p_town_33", slot_town_arena_melee_3_team_size,   6),

	]),
	("initialize_banner_info",	
	[	
	  #Banners
      (try_for_range, ":cur_troop", active_npcs_begin, kingdom_ladies_end),
        (troop_set_slot, ":cur_troop", slot_troop_custom_banner_flag_type, -1),
        (troop_set_slot, ":cur_troop", slot_troop_custom_banner_map_flag_type, -1),
      (try_end),
      (troop_set_slot, "trp_player", slot_troop_custom_banner_flag_type, -1),
      (troop_set_slot, "trp_player", slot_troop_custom_banner_map_flag_type, -1),
      (store_random_in_range, "$g_election_date", 0, 45), #setting a random election date
      #Assigning global constant
      #(call_script, "script_store_average_center_value_per_faction"),

      (troop_set_slot, "trp_player", slot_troop_custom_banner_bg_color_1, 0xFFFFFFFF),
      (troop_set_slot, "trp_player", slot_troop_custom_banner_bg_color_2, 0xFFFFFFFF),
      (troop_set_slot, "trp_player", slot_troop_custom_banner_charge_color_1, 0xFFFFFFFF),
      (troop_set_slot, "trp_player", slot_troop_custom_banner_charge_color_2, 0xFFFFFFFF),
      (troop_set_slot, "trp_player", slot_troop_custom_banner_charge_color_3, 0xFFFFFFFF),
      (troop_set_slot, "trp_player", slot_troop_custom_banner_charge_color_4, 0xFFFFFFFF),

      #Setting background colors for banners
      (troop_set_slot, "trp_banner_background_color_array", 0, 0xFF8f4531),
      (troop_set_slot, "trp_banner_background_color_array", 1, 0xFFd9d7d1),
      (troop_set_slot, "trp_banner_background_color_array", 2, 0xFF373736),
      (troop_set_slot, "trp_banner_background_color_array", 3, 0xFFa48b28),
      (troop_set_slot, "trp_banner_background_color_array", 4, 0xFF497735),
      (troop_set_slot, "trp_banner_background_color_array", 5, 0xFF82362d),
      (troop_set_slot, "trp_banner_background_color_array", 6, 0xFF793329),
      (troop_set_slot, "trp_banner_background_color_array", 7, 0xFF262521),
      (troop_set_slot, "trp_banner_background_color_array", 8, 0xFFd9dad1),
      (troop_set_slot, "trp_banner_background_color_array", 9, 0xFF524563),
      (troop_set_slot, "trp_banner_background_color_array", 10, 0xFF91312c),
      (troop_set_slot, "trp_banner_background_color_array", 11, 0xFFafa231),
      (troop_set_slot, "trp_banner_background_color_array", 12, 0xFF706d3c),
      (troop_set_slot, "trp_banner_background_color_array", 13, 0xFFd6d3ce),
      (troop_set_slot, "trp_banner_background_color_array", 14, 0xFF521c08),
      (troop_set_slot, "trp_banner_background_color_array", 15, 0xFF394584),
      (troop_set_slot, "trp_banner_background_color_array", 16, 0xFF42662e),
      (troop_set_slot, "trp_banner_background_color_array", 17, 0xFFdfded6),
      (troop_set_slot, "trp_banner_background_color_array", 18, 0xFF292724),
      (troop_set_slot, "trp_banner_background_color_array", 19, 0xFF58611b),
      (troop_set_slot, "trp_banner_background_color_array", 20, 0xFF313a67),
      (troop_set_slot, "trp_banner_background_color_array", 21, 0xFF9c924a),
      (troop_set_slot, "trp_banner_background_color_array", 22, 0xFF998b39),
      (troop_set_slot, "trp_banner_background_color_array", 23, 0xFF365168),
      (troop_set_slot, "trp_banner_background_color_array", 24, 0xFFd6d3ce),
      (troop_set_slot, "trp_banner_background_color_array", 25, 0xFF94a642),
      (troop_set_slot, "trp_banner_background_color_array", 26, 0xFF944131),
      (troop_set_slot, "trp_banner_background_color_array", 27, 0xFF893b34),
      (troop_set_slot, "trp_banner_background_color_array", 28, 0xFF425510),
      (troop_set_slot, "trp_banner_background_color_array", 29, 0xFF94452e),
      (troop_set_slot, "trp_banner_background_color_array", 30, 0xFF475a94),
      (troop_set_slot, "trp_banner_background_color_array", 31, 0xFFd1b231),
      (troop_set_slot, "trp_banner_background_color_array", 32, 0xFFe1e2df),
      (troop_set_slot, "trp_banner_background_color_array", 33, 0xFF997c1e),
      (troop_set_slot, "trp_banner_background_color_array", 34, 0xFFc6b74d),
      (troop_set_slot, "trp_banner_background_color_array", 35, 0xFFad9a18),
      (troop_set_slot, "trp_banner_background_color_array", 36, 0xFF212421),
      (troop_set_slot, "trp_banner_background_color_array", 37, 0xFF8c2021),
      (troop_set_slot, "trp_banner_background_color_array", 38, 0xFF4d7136),
      (troop_set_slot, "trp_banner_background_color_array", 39, 0xFF395d84),
      (troop_set_slot, "trp_banner_background_color_array", 40, 0xFF527539),
      (troop_set_slot, "trp_banner_background_color_array", 41, 0xFF9c3c39),
      (troop_set_slot, "trp_banner_background_color_array", 42, 0xFF42518c),
      (troop_set_slot, "trp_banner_background_color_array", 43, 0xFFa46a2c),
      (troop_set_slot, "trp_banner_background_color_array", 44, 0xFF9f5141),
      (troop_set_slot, "trp_banner_background_color_array", 45, 0xFF2c6189),
      (troop_set_slot, "trp_banner_background_color_array", 46, 0xFF556421),
      (troop_set_slot, "trp_banner_background_color_array", 47, 0xFF9d621e),
      (troop_set_slot, "trp_banner_background_color_array", 48, 0xFFdeded6),
      (troop_set_slot, "trp_banner_background_color_array", 49, 0xFF6e4891),
      (troop_set_slot, "trp_banner_background_color_array", 50, 0xFF865a29),
      (troop_set_slot, "trp_banner_background_color_array", 51, 0xFFdedfd9),
      (troop_set_slot, "trp_banner_background_color_array", 52, 0xFF524273),
      (troop_set_slot, "trp_banner_background_color_array", 53, 0xFF8c3821),
      (troop_set_slot, "trp_banner_background_color_array", 54, 0xFFd1cec6),
      (troop_set_slot, "trp_banner_background_color_array", 55, 0xFF313031),
      (troop_set_slot, "trp_banner_background_color_array", 56, 0xFF47620d),
      (troop_set_slot, "trp_banner_background_color_array", 57, 0xFF6b4139),
      (troop_set_slot, "trp_banner_background_color_array", 58, 0xFFd6d7d6),
      (troop_set_slot, "trp_banner_background_color_array", 59, 0xFF2e2f2c),
      (troop_set_slot, "trp_banner_background_color_array", 60, 0xFF604283),
      (troop_set_slot, "trp_banner_background_color_array", 61, 0xFF395584),
      (troop_set_slot, "trp_banner_background_color_array", 62, 0xFF313031),
      (troop_set_slot, "trp_banner_background_color_array", 63, 0xFF7e3f2e),
      (troop_set_slot, "trp_banner_background_color_array", 64, 0xFF343434),
      (troop_set_slot, "trp_banner_background_color_array", 65, 0xFF3c496b),
      (troop_set_slot, "trp_banner_background_color_array", 66, 0xFFd9d8d1),
      (troop_set_slot, "trp_banner_background_color_array", 67, 0xFF99823c),
      (troop_set_slot, "trp_banner_background_color_array", 68, 0xFF9f822e),
      (troop_set_slot, "trp_banner_background_color_array", 69, 0xFF393839),
      (troop_set_slot, "trp_banner_background_color_array", 70, 0xFFa54931),
      (troop_set_slot, "trp_banner_background_color_array", 71, 0xFFdfdcd6),
      (troop_set_slot, "trp_banner_background_color_array", 72, 0xFF9f4a36),
      (troop_set_slot, "trp_banner_background_color_array", 73, 0xFF8c7521),
      (troop_set_slot, "trp_banner_background_color_array", 74, 0xFF9f4631),
      (troop_set_slot, "trp_banner_background_color_array", 75, 0xFF793324),
      (troop_set_slot, "trp_banner_background_color_array", 76, 0xFF395076),
      (troop_set_slot, "trp_banner_background_color_array", 77, 0xFF2c2b2c),
      (troop_set_slot, "trp_banner_background_color_array", 78, 0xFF657121),
      (troop_set_slot, "trp_banner_background_color_array", 79, 0xFF7e3121),
      (troop_set_slot, "trp_banner_background_color_array", 80, 0xFF76512e),
      (troop_set_slot, "trp_banner_background_color_array", 81, 0xFFe7e3de),
      (troop_set_slot, "trp_banner_background_color_array", 82, 0xFF947921),
      (troop_set_slot, "trp_banner_background_color_array", 83, 0xFF4d7b7c),
      (troop_set_slot, "trp_banner_background_color_array", 84, 0xFF343331),
      (troop_set_slot, "trp_banner_background_color_array", 85, 0xFFa74d36),
      (troop_set_slot, "trp_banner_background_color_array", 86, 0xFFe7e3de),
      (troop_set_slot, "trp_banner_background_color_array", 87, 0xFFd6d8ce),
      (troop_set_slot, "trp_banner_background_color_array", 88, 0xFF3e4d67),
      (troop_set_slot, "trp_banner_background_color_array", 89, 0xFF9f842e),
      (troop_set_slot, "trp_banner_background_color_array", 90, 0xFF4d6994),
      (troop_set_slot, "trp_banner_background_color_array", 91, 0xFF4a6118),
      (troop_set_slot, "trp_banner_background_color_array", 92, 0xFF943c29),
      (troop_set_slot, "trp_banner_background_color_array", 93, 0xFF394479),
      (troop_set_slot, "trp_banner_background_color_array", 94, 0xFF343331),
      (troop_set_slot, "trp_banner_background_color_array", 95, 0xFF3f4d5d),
      (troop_set_slot, "trp_banner_background_color_array", 96, 0xFF4a6489),
      (troop_set_slot, "trp_banner_background_color_array", 97, 0xFF313031),
      (troop_set_slot, "trp_banner_background_color_array", 98, 0xFFd6d7ce),
      (troop_set_slot, "trp_banner_background_color_array", 99, 0xFFc69e00),
      (troop_set_slot, "trp_banner_background_color_array", 100, 0xFF638e52),
      (troop_set_slot, "trp_banner_background_color_array", 101, 0xFFdcdbd3),
      (troop_set_slot, "trp_banner_background_color_array", 102, 0xFFdbdcd3),
      (troop_set_slot, "trp_banner_background_color_array", 103, 0xFF843831),
      (troop_set_slot, "trp_banner_background_color_array", 104, 0xFFcecfc6),
      (troop_set_slot, "trp_banner_background_color_array", 105, 0xFFc39d31),
      (troop_set_slot, "trp_banner_background_color_array", 106, 0xFFcbb670),
      (troop_set_slot, "trp_banner_background_color_array", 107, 0xFF394a18),
      (troop_set_slot, "trp_banner_background_color_array", 108, 0xFF372708),
      (troop_set_slot, "trp_banner_background_color_array", 109, 0xFF9a6810),
      (troop_set_slot, "trp_banner_background_color_array", 110, 0xFFb27910),
      (troop_set_slot, "trp_banner_background_color_array", 111, 0xFF8c8621),
      (troop_set_slot, "trp_banner_background_color_array", 112, 0xFF975a03),
      (troop_set_slot, "trp_banner_background_color_array", 113, 0xFF2c2924),
      (troop_set_slot, "trp_banner_background_color_array", 114, 0xFFaa962c),
      (troop_set_slot, "trp_banner_background_color_array", 115, 0xFFa2822e),
      (troop_set_slot, "trp_banner_background_color_array", 116, 0xFF7b8a8c),
      (troop_set_slot, "trp_banner_background_color_array", 117, 0xFF3c0908),
      (troop_set_slot, "trp_banner_background_color_array", 118, 0xFFFF00FF),
      (troop_set_slot, "trp_banner_background_color_array", 119, 0xFF671e14),
      (troop_set_slot, "trp_banner_background_color_array", 120, 0xFF103042),
      (troop_set_slot, "trp_banner_background_color_array", 121, 0xFF4a4500),
      (troop_set_slot, "trp_banner_background_color_array", 122, 0xFF703324),
      (troop_set_slot, "trp_banner_background_color_array", 123, 0xFF24293c),
      (troop_set_slot, "trp_banner_background_color_array", 124, 0xFF5d6966),
      (troop_set_slot, "trp_banner_background_color_array", 125, 0xFFbd9631),
      (troop_set_slot, "trp_banner_background_color_array", 126, 0xFFc6b26b),
      (troop_set_slot, "trp_banner_background_color_array", 127, 0xFF394918),
	  
	  #gekokujo 3.0 banner background colors. i literally do not give a shit, this is all made up
      (troop_set_slot, "trp_banner_background_color_array", 128, 0xFF425510),
      (troop_set_slot, "trp_banner_background_color_array", 129, 0xFF94452e),
      (troop_set_slot, "trp_banner_background_color_array", 130, 0xFF475a94),
      (troop_set_slot, "trp_banner_background_color_array", 131, 0xFFd1b231),
      (troop_set_slot, "trp_banner_background_color_array", 132, 0xFFe1e2df),
      (troop_set_slot, "trp_banner_background_color_array", 133, 0xFF997c1e),
      (troop_set_slot, "trp_banner_background_color_array", 134, 0xFFc6b74d),
      (troop_set_slot, "trp_banner_background_color_array", 135, 0xFFad9a18),
      (troop_set_slot, "trp_banner_background_color_array", 136, 0xFF212421),
      (troop_set_slot, "trp_banner_background_color_array", 137, 0xFF8c2021),
      (troop_set_slot, "trp_banner_background_color_array", 138, 0xFF4d7136),
      (troop_set_slot, "trp_banner_background_color_array", 139, 0xFF395d84),
      (troop_set_slot, "trp_banner_background_color_array", 140, 0xFF527539),
      (troop_set_slot, "trp_banner_background_color_array", 141, 0xFF9c3c39),
      (troop_set_slot, "trp_banner_background_color_array", 142, 0xFF42518c),
      (troop_set_slot, "trp_banner_background_color_array", 143, 0xFFa46a2c),
      (troop_set_slot, "trp_banner_background_color_array", 144, 0xFF9f5141),
      (troop_set_slot, "trp_banner_background_color_array", 145, 0xFF2c6189),
      (troop_set_slot, "trp_banner_background_color_array", 146, 0xFF556421),
      (troop_set_slot, "trp_banner_background_color_array", 147, 0xFF9d621e),
      (troop_set_slot, "trp_banner_background_color_array", 148, 0xFFdeded6),
      (troop_set_slot, "trp_banner_background_color_array", 149, 0xFF6e4891),
      (troop_set_slot, "trp_banner_background_color_array", 150, 0xFF865a29),
      (troop_set_slot, "trp_banner_background_color_array", 151, 0xFFdedfd9),
      (troop_set_slot, "trp_banner_background_color_array", 152, 0xFF524273),
      (troop_set_slot, "trp_banner_background_color_array", 153, 0xFF8c3821),
      (troop_set_slot, "trp_banner_background_color_array", 154, 0xFFd1cec6),
      (troop_set_slot, "trp_banner_background_color_array", 155, 0xFF313031),
      (troop_set_slot, "trp_banner_background_color_array", 156, 0xFF47620d),
      (troop_set_slot, "trp_banner_background_color_array", 157, 0xFF6b4139),
      (troop_set_slot, "trp_banner_background_color_array", 158, 0xFFd6d7d6),
      (troop_set_slot, "trp_banner_background_color_array", 159, 0xFF2e2f2c),
      (troop_set_slot, "trp_banner_background_color_array", 160, 0xFF604283),
      (troop_set_slot, "trp_banner_background_color_array", 161, 0xFF395584),
      (troop_set_slot, "trp_banner_background_color_array", 162, 0xFF313031),
      (troop_set_slot, "trp_banner_background_color_array", 163, 0xFF7e3f2e),
      (troop_set_slot, "trp_banner_background_color_array", 164, 0xFF343434),
      (troop_set_slot, "trp_banner_background_color_array", 165, 0xFF3c496b),
      (troop_set_slot, "trp_banner_background_color_array", 166, 0xFFd9d8d1),
      (troop_set_slot, "trp_banner_background_color_array", 167, 0xFF99823c),
      (troop_set_slot, "trp_banner_background_color_array", 168, 0xFF9f822e),
      (troop_set_slot, "trp_banner_background_color_array", 169, 0xFF393839),
      (troop_set_slot, "trp_banner_background_color_array", 170, 0xFFa54931),
      (troop_set_slot, "trp_banner_background_color_array", 171, 0xFFdfdcd6),
      (troop_set_slot, "trp_banner_background_color_array", 172, 0xFF9f4a36),
      (troop_set_slot, "trp_banner_background_color_array", 173, 0xFF8c7521),
      (troop_set_slot, "trp_banner_background_color_array", 174, 0xFF9f4631),
      (troop_set_slot, "trp_banner_background_color_array", 175, 0xFF793324),
      (troop_set_slot, "trp_banner_background_color_array", 176, 0xFF395076),
      (troop_set_slot, "trp_banner_background_color_array", 177, 0xFF2c2b2c),
      (troop_set_slot, "trp_banner_background_color_array", 178, 0xFF657121),
      (troop_set_slot, "trp_banner_background_color_array", 179, 0xFF7e3121),
      (troop_set_slot, "trp_banner_background_color_array", 180, 0xFF76512e),
      (troop_set_slot, "trp_banner_background_color_array", 181, 0xFFe7e3de),
      (troop_set_slot, "trp_banner_background_color_array", 182, 0xFF947921),
      (troop_set_slot, "trp_banner_background_color_array", 183, 0xFF4d7b7c),
      (troop_set_slot, "trp_banner_background_color_array", 184, 0xFF343331),
      (troop_set_slot, "trp_banner_background_color_array", 185, 0xFFa74d36),
      (troop_set_slot, "trp_banner_background_color_array", 186, 0xFFe7e3de),
      (troop_set_slot, "trp_banner_background_color_array", 187, 0xFFd6d8ce),
      (troop_set_slot, "trp_banner_background_color_array", 188, 0xFF3e4d67),
      (troop_set_slot, "trp_banner_background_color_array", 189, 0xFF9f842e),
      (troop_set_slot, "trp_banner_background_color_array", 190, 0xFF4d6994),
      (troop_set_slot, "trp_banner_background_color_array", 191, 0xFF4a6118),
      (troop_set_slot, "trp_banner_background_color_array", 192, 0xFF943c29),
      (troop_set_slot, "trp_banner_background_color_array", 193, 0xFF394479),
      (troop_set_slot, "trp_banner_background_color_array", 194, 0xFF343331),
      (troop_set_slot, "trp_banner_background_color_array", 195, 0xFF3f4d5d),

      #Default banners
      (troop_set_slot, "trp_banner_background_color_array", 196, 0xFF212221),
      (troop_set_slot, "trp_banner_background_color_array", 197, 0xFF212221),
      (troop_set_slot, "trp_banner_background_color_array", 198, 0xFF2E3B10),
      (troop_set_slot, "trp_banner_background_color_array", 199, 0xFF425D7B),
      (troop_set_slot, "trp_banner_background_color_array", 200, 0xFF394608),
	  ]),
    ("initialize_economic_information",
    [   	     
	#Gekokujo completely changed code and made neater for understanding (see backup for reference)
	#All towns produce tools, pottery, and wool cloth for sale in countryside
	(try_for_range, ":town_no", towns_begin, towns_end),	
		#gekokujo hemp cloth
		(store_random_in_range, ":random_average_20_variation_10", 10, 31), #10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29 or 30
		(party_set_slot, ":town_no", slot_center_wool_looms, ":random_average_20_variation_10"),

		#gekokujo sake
		#(store_random_in_range, ":random_average_2_variation_1", 1, 4), #1,2 or 3
		(store_random_in_range, ":random_average_2_variation_1", 0, 7), #0, 1, 2, 3, 4, 5 or 6
		(party_set_slot, ":town_no", slot_center_breweries, ":random_average_2_variation_1"),

		#gekokujo pottery
		(store_random_in_range, ":random_average_5_variation_3", 3, 9), #2,3,4,5,6,7 or 8
		(party_set_slot, ":town_no", slot_center_pottery_kilns, ":random_average_5_variation_3"),

		#gekokujo tools
		(store_random_in_range, ":random_average_15_variation_9", 6, 25), #6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23 or 24
		(party_set_slot, ":town_no", slot_center_smithies, ":random_average_15_variation_9"),

		#gekokujo white rice
		(store_random_in_range, ":random_average_5_variation_3", 3, 9), #2,3,4,5,6,7 or 8
		(party_set_slot, ":town_no", slot_center_mills, ":random_average_5_variation_3"),

		#gekokujo leatherworks (reduced production by 1/5 thereabouts)
		#(store_random_in_range, ":random_average_2_variation_1", 1, 4), #1,2 or 3
		(store_random_in_range, ":random_average_2_variation_1", 0, 2), #0 or 1
		(party_set_slot, ":town_no", slot_center_tanneries, ":random_average_2_variation_1"),

		#gekokujo soy sauce
		(store_random_in_range, ":random_average_1_variation_1", 0, 3), #0,1 or 2
		(party_set_slot, ":town_no", slot_center_wine_presses, ":random_average_1_variation_1"),

		#gekokujo fish sauce
		(store_random_in_range, ":random_average_2_variation_1", 1, 4), #1,2 or 3
		(party_set_slot, ":town_no", slot_center_olive_presses, ":random_average_2_variation_1"),
		
		#gekokujo brown rice
		(store_random_in_range, ":random_average_1000_variation_1000", 0, 2001), #0..2000
		(party_set_slot, ":town_no", slot_center_acres_grain, ":random_average_1000_variation_1000"), #0..2000

		#gekokujo soybeans
		(store_random_in_range, ":random_average_1000_variation_1000", 0, 2001), #0..2000
		(party_set_slot, ":town_no", slot_center_acres_vineyard, ":random_average_1000_variation_1000"), #0..2000
	  
	    #gekokujo raw silk
        (store_random_in_range, ":random_value_between_0_and_2000", 0, 2000),
	    (store_random_in_range, ":random_value_between_0_and_average_1000", 0, ":random_value_between_0_and_2000"),
	    (party_set_slot, ":town_no", slot_center_silk_farms, ":random_value_between_0_and_average_1000"), #average : 500, min : 0, max : 2000
	
	#Gekokujo Town Production
	
	#Coastal (Sea Fish, Salt, Offal)
        (try_begin),
          (this_or_next|eq, ":town_no", "p_town_1"), 
          (this_or_next|eq, ":town_no", "p_town_2"), 
          (this_or_next|eq, ":town_no", "p_town_3"), 
          (this_or_next|eq, ":town_no", "p_town_4"), 
          (this_or_next|eq, ":town_no", "p_town_5"), 
          (this_or_next|eq, ":town_no", "p_town_6"), 
          (this_or_next|eq, ":town_no", "p_town_7"), 
          (this_or_next|eq, ":town_no", "p_town_8"), 
          (this_or_next|eq, ":town_no", "p_town_9"),
          (this_or_next|eq, ":town_no", "p_town_10"), 
          (this_or_next|eq, ":town_no", "p_town_11"), 
          (this_or_next|eq, ":town_no", "p_town_12"), 
          (this_or_next|eq, ":town_no", "p_town_13"), 
          (this_or_next|eq, ":town_no", "p_town_14"), 
          (this_or_next|eq, ":town_no", "p_town_15"), 
          (this_or_next|eq, ":town_no", "p_town_16"), 
          (this_or_next|eq, ":town_no", "p_town_17"), 
          (this_or_next|eq, ":town_no", "p_town_18"), 
          (this_or_next|eq, ":town_no", "p_town_19"),
          (this_or_next|eq, ":town_no", "p_town_20"), 
          (this_or_next|eq, ":town_no", "p_town_21"), 
          (this_or_next|eq, ":town_no", "p_town_22"), 
          (this_or_next|eq, ":town_no", "p_town_23"), 
          (this_or_next|eq, ":town_no", "p_town_24"), 
          (this_or_next|eq, ":town_no", "p_town_25"), 
          (this_or_next|eq, ":town_no", "p_town_26"), 
          (this_or_next|eq, ":town_no", "p_town_27"), 
          (this_or_next|eq, ":town_no", "p_town_28"), 
          (this_or_next|eq, ":town_no", "p_town_29"),
          (this_or_next|eq, ":town_no", "p_town_30"), 
          (this_or_next|eq, ":town_no", "p_town_31"), 
          (eq, ":town_no", "p_town_32"), 
	  
	      (store_random_in_range, ":random_value_between_5_and_30", 5, 30),
	      (party_set_slot, ":town_no", slot_center_fishing_fleet, ":random_value_between_5_and_30"),
	      (party_set_slot, ":town_no", slot_center_apiaries, ":random_value_between_5_and_30"),
	  
	      (store_random_in_range, ":random_value_between_0_and_1", 0, 1),
	      (party_set_slot, ":town_no", slot_center_salt_pans, ":random_value_between_0_and_1"),
	    (try_end),	  
	
	#Cultural Centers (Linen and Silk Looms)
        (try_begin),
          (this_or_next|eq, ":town_no", "p_town_1"), #Edo
          (this_or_next|eq, ":town_no", "p_town_4"), #Kyoto
          (eq, ":town_no", "p_town_5"), #Osaka
	  
	      (store_random_in_range, ":random_average_25_variation_5", 5, 31),
	      (party_set_slot, ":town_no", slot_center_silk_looms, ":random_average_25_variation_5"),
	  
	      (store_random_in_range, ":random_average_25_variation_5", 5, 31),
	      (party_set_slot, ":town_no", slot_center_linen_looms, ":random_average_25_variation_5"),
	    (try_end),	  

    (try_end),
	
	
    (try_for_range, ":village_no", villages_begin, villages_end),
	  #gekokujo cattle (reduced by 1/5)
    # (store_random_in_range, ":random_cattle", 20, 100),
      (store_random_in_range, ":random_cattle", 4, 20),
      (party_set_slot, ":village_no", slot_center_head_cattle, ":random_cattle"),
	  #average : 10, min : 5, max : 15

	  #gekokujo brown rice
      (store_random_in_range, ":random_value_between_0_and_40000", 0, 40000),
	  (store_random_in_range, ":random_value_between_0_and_average_20000", 0, ":random_value_between_0_and_40000"),
	  (party_set_slot, ":village_no", slot_center_acres_grain, ":random_value_between_0_and_average_20000"),
	  #average : 10000, min : 0, max : 40000

      #gekokujo soybeans
	  (store_random_in_range, ":random_value_between_0_and_2000", 0, 2000),
	  (store_random_in_range, ":random_value_between_0_and_average_1000", 0, ":random_value_between_0_and_2000"),
	  (party_set_slot, ":village_no", slot_center_acres_vineyard, ":random_value_between_0_and_average_1000"), #average : 500, min : 0, max : 2000
	  
	  #gekokujo hemp
      (store_random_in_range, ":random_value_between_0_and_2000", 0, 2000),
	  (store_random_in_range, ":random_value_between_0_and_average_1000", 0, ":random_value_between_0_and_2000"),
	  (party_set_slot, ":village_no", slot_center_acres_olives, ":random_value_between_0_and_average_1000"),
	  #average : 500, min : 0, max : 2000
	  
	  #gekokujo cabbage and fruit
	  (store_random_in_range, ":random_value_between_0_and_5", 0, 5),
	  (party_set_slot, ":village_no", slot_center_household_gardens, ":random_value_between_0_and_5"), 

	  #gekokujo white rice
      (store_random_in_range, ":random_value_between_0_and_3", 0, 3),
	  (party_set_slot, ":village_no", slot_center_mills, ":random_value_between_0_and_3"),
	  
	  #gekokujo pottery
	  (store_random_in_range, ":random_value_between_0_and_5", 0, 5),
	  (party_set_slot, ":village_no", slot_center_pottery_kilns, ":random_value_between_0_and_5"),
	
	  #gekokujo flax
      (store_random_in_range, ":random_value_between_0_and_2000", 0, 2000),
	  (store_random_in_range, ":random_value_between_0_and_average_1000", 0, ":random_value_between_0_and_2000"),
	  (party_set_slot, ":village_no", slot_center_acres_flax, ":random_value_between_0_and_average_1000"),
	  #average : 500, min : 0, max : 2000
	  
	  #Gekokujo Village Production
	
	  #Coastal (Sea Fish)
	  (try_begin),
        (this_or_next|eq, ":village_no", "p_village_1"),
        (this_or_next|eq, ":village_no", "p_village_2"),
        (this_or_next|eq, ":village_no", "p_village_3"),
        (this_or_next|eq, ":village_no", "p_village_4"),
        (this_or_next|eq, ":village_no", "p_village_5"),
        (this_or_next|eq, ":village_no", "p_village_6"),
        (this_or_next|eq, ":village_no", "p_village_7"),
        (this_or_next|eq, ":village_no", "p_village_8"),
        (this_or_next|eq, ":village_no", "p_village_9"),
        (this_or_next|eq, ":village_no", "p_village_10"),
        (this_or_next|eq, ":village_no", "p_village_11"),
        (this_or_next|eq, ":village_no", "p_village_12"),
        (this_or_next|eq, ":village_no", "p_village_13"),
        (this_or_next|eq, ":village_no", "p_village_14"),
        (this_or_next|eq, ":village_no", "p_village_15"),
        (this_or_next|eq, ":village_no", "p_village_16"),
        (this_or_next|eq, ":village_no", "p_village_17"),
        (this_or_next|eq, ":village_no", "p_village_18"),
        (this_or_next|eq, ":village_no", "p_village_19"),
        (this_or_next|eq, ":village_no", "p_village_20"),
        (this_or_next|eq, ":village_no", "p_village_21"),
        (this_or_next|eq, ":village_no", "p_village_22"),
        (this_or_next|eq, ":village_no", "p_village_23"),
        (this_or_next|eq, ":village_no", "p_village_24"),
        (this_or_next|eq, ":village_no", "p_village_25"),
        (this_or_next|eq, ":village_no", "p_village_26"),
        (this_or_next|eq, ":village_no", "p_village_27"),
        (this_or_next|eq, ":village_no", "p_village_28"),
        (this_or_next|eq, ":village_no", "p_village_29"),
        (this_or_next|eq, ":village_no", "p_village_30"),
        (this_or_next|eq, ":village_no", "p_village_31"),
        (this_or_next|eq, ":village_no", "p_village_32"),
        (this_or_next|eq, ":village_no", "p_village_33"),
        (this_or_next|eq, ":village_no", "p_village_34"),
        (this_or_next|eq, ":village_no", "p_village_35"),
        (this_or_next|eq, ":village_no", "p_village_36"),
        (this_or_next|eq, ":village_no", "p_village_37"),
        (this_or_next|eq, ":village_no", "p_village_38"),
        (this_or_next|eq, ":village_no", "p_village_39"),
        (this_or_next|eq, ":village_no", "p_village_40"),
        (this_or_next|eq, ":village_no", "p_village_41"),
        (this_or_next|eq, ":village_no", "p_village_42"),
        (this_or_next|eq, ":village_no", "p_village_43"),
        (this_or_next|eq, ":village_no", "p_village_44"),
        (this_or_next|eq, ":village_no", "p_village_45"),
        (this_or_next|eq, ":village_no", "p_village_46"),
        (this_or_next|eq, ":village_no", "p_village_47"),
        (this_or_next|eq, ":village_no", "p_village_48"),
        (this_or_next|eq, ":village_no", "p_village_49"),
        (this_or_next|eq, ":village_no", "p_village_50"),
        (this_or_next|eq, ":village_no", "p_village_51"),
        (this_or_next|eq, ":village_no", "p_village_52"),
        (this_or_next|eq, ":village_no", "p_village_53"),
        (this_or_next|eq, ":village_no", "p_village_54"),
        (this_or_next|eq, ":village_no", "p_village_56"),
        (this_or_next|eq, ":village_no", "p_village_57"),
        (this_or_next|eq, ":village_no", "p_village_59"),
        (this_or_next|eq, ":village_no", "p_village_60"),
        (this_or_next|eq, ":village_no", "p_village_61"),
        (this_or_next|eq, ":village_no", "p_village_62"),
        (this_or_next|eq, ":village_no", "p_village_64"),
        (this_or_next|eq, ":village_no", "p_village_65"),
        (this_or_next|eq, ":village_no", "p_village_66"),
        (this_or_next|eq, ":village_no", "p_village_67"),
        (this_or_next|eq, ":village_no", "p_village_68"),
        (this_or_next|eq, ":village_no", "p_village_69"),
        (this_or_next|eq, ":village_no", "p_village_70"),
        (this_or_next|eq, ":village_no", "p_village_71"),
        (this_or_next|eq, ":village_no", "p_village_72"),
        (this_or_next|eq, ":village_no", "p_village_73"),
        (this_or_next|eq, ":village_no", "p_village_74"),
        (this_or_next|eq, ":village_no", "p_village_75"),
        (this_or_next|eq, ":village_no", "p_village_76"),
        (this_or_next|eq, ":village_no", "p_village_77"),
        (this_or_next|eq, ":village_no", "p_village_78"),
        (this_or_next|eq, ":village_no", "p_village_79"),
        (this_or_next|eq, ":village_no", "p_village_80"),
        (this_or_next|eq, ":village_no", "p_village_81"),
        (this_or_next|eq, ":village_no", "p_village_82"),
        (this_or_next|eq, ":village_no", "p_village_83"),
        (this_or_next|eq, ":village_no", "p_village_84"),
        (this_or_next|eq, ":village_no", "p_village_85"),
        (this_or_next|eq, ":village_no", "p_village_86"),
        (this_or_next|eq, ":village_no", "p_village_87"),
        (this_or_next|eq, ":village_no", "p_village_88"),
        (this_or_next|eq, ":village_no", "p_village_89"),
        (this_or_next|eq, ":village_no", "p_village_90"),
        (this_or_next|eq, ":village_no", "p_village_91"),
        (this_or_next|eq, ":village_no", "p_village_92"),
        (this_or_next|eq, ":village_no", "p_village_93"),
        (this_or_next|eq, ":village_no", "p_village_94"),
        (this_or_next|eq, ":village_no", "p_village_95"),
        (this_or_next|eq, ":village_no", "p_village_96"),
        (this_or_next|eq, ":village_no", "p_village_97"),
        (this_or_next|eq, ":village_no", "p_village_98"),
        (this_or_next|eq, ":village_no", "p_village_99"),
        (this_or_next|eq, ":village_no", "p_village_100"),
        (this_or_next|eq, ":village_no", "p_village_101"),
        (this_or_next|eq, ":village_no", "p_village_102"),
        (this_or_next|eq, ":village_no", "p_village_103"),
        (this_or_next|eq, ":village_no", "p_village_104"),
        (this_or_next|eq, ":village_no", "p_village_105"),
        (this_or_next|eq, ":village_no", "p_village_106"),
        (this_or_next|eq, ":village_no", "p_village_107"),
        (this_or_next|eq, ":village_no", "p_village_108"),
        (this_or_next|eq, ":village_no", "p_village_109"),
        (this_or_next|eq, ":village_no", "p_village_110"),
        (this_or_next|eq, ":village_no", "p_village_111"),
        (this_or_next|eq, ":village_no", "p_village_112"),
        (this_or_next|eq, ":village_no", "p_village_113"),
        (this_or_next|eq, ":village_no", "p_village_114"),
        (this_or_next|eq, ":village_no", "p_village_115"),
        (this_or_next|eq, ":village_no", "p_village_116"),
        (this_or_next|eq, ":village_no", "p_village_117"),
        (this_or_next|eq, ":village_no", "p_village_118"),
        (this_or_next|eq, ":village_no", "p_village_119"),
        (this_or_next|eq, ":village_no", "p_village_120"),
        (this_or_next|eq, ":village_no", "p_village_121"),
        (this_or_next|eq, ":village_no", "p_village_122"),
        (this_or_next|eq, ":village_no", "p_village_123"),
        (this_or_next|eq, ":village_no", "p_village_124"),
        (this_or_next|eq, ":village_no", "p_village_125"),
        (this_or_next|eq, ":village_no", "p_village_126"),
        (this_or_next|eq, ":village_no", "p_village_128"),
        (this_or_next|eq, ":village_no", "p_village_130"),
        (this_or_next|eq, ":village_no", "p_village_131"),
        (this_or_next|eq, ":village_no", "p_village_132"),
        (this_or_next|eq, ":village_no", "p_village_133"),
        (this_or_next|eq, ":village_no", "p_village_134"),
        (this_or_next|eq, ":village_no", "p_village_135"),
        (this_or_next|eq, ":village_no", "p_village_136"),
        (this_or_next|eq, ":village_no", "p_village_137"),
        (this_or_next|eq, ":village_no", "p_village_138"),
        (this_or_next|eq, ":village_no", "p_village_140"),
        (this_or_next|eq, ":village_no", "p_village_141"),
        (this_or_next|eq, ":village_no", "p_village_145"),
        (this_or_next|eq, ":village_no", "p_village_146"),
        (this_or_next|eq, ":village_no", "p_village_148"),
        (this_or_next|eq, ":village_no", "p_village_149"),
        (this_or_next|eq, ":village_no", "p_village_151"),
        (this_or_next|eq, ":village_no", "p_village_153"),
        (this_or_next|eq, ":village_no", "p_village_154"),
        (this_or_next|eq, ":village_no", "p_village_155"),
        (this_or_next|eq, ":village_no", "p_village_156"),
        (this_or_next|eq, ":village_no", "p_village_157"),
        (this_or_next|eq, ":village_no", "p_village_158"),
        (this_or_next|eq, ":village_no", "p_village_159"),
        (this_or_next|eq, ":village_no", "p_village_160"),
        (this_or_next|eq, ":village_no", "p_village_162"),
        (this_or_next|eq, ":village_no", "p_village_163"),
        (this_or_next|eq, ":village_no", "p_village_164"),
        (this_or_next|eq, ":village_no", "p_village_167"),
        (this_or_next|eq, ":village_no", "p_village_169"),
        (this_or_next|eq, ":village_no", "p_village_171"),
        (this_or_next|eq, ":village_no", "p_village_172"),
        (this_or_next|eq, ":village_no", "p_village_173"),
        (this_or_next|eq, ":village_no", "p_village_174"),
        (this_or_next|eq, ":village_no", "p_village_175"),
        (this_or_next|eq, ":village_no", "p_village_178"),
        (this_or_next|eq, ":village_no", "p_village_183"),
        (this_or_next|eq, ":village_no", "p_village_184"),
        (eq, ":village_no", "p_village_185"), 
	  
	    (store_random_in_range, ":random_value_between_15_and_20", 15, 20),
	    (party_set_slot, ":village_no", slot_center_fishing_fleet, ":random_value_between_15_and_20"),
	  (try_end),
	
	  #Riverine (River Fish, Eels)
	  (try_begin),
        (this_or_next|eq, ":village_no", "p_village_1"),
        (this_or_next|eq, ":village_no", "p_village_2"),
        (this_or_next|eq, ":village_no", "p_village_3"),
        (this_or_next|eq, ":village_no", "p_village_4"),
        (this_or_next|eq, ":village_no", "p_village_5"),
        (this_or_next|eq, ":village_no", "p_village_6"),
        (this_or_next|eq, ":village_no", "p_village_7"),
        (this_or_next|eq, ":village_no", "p_village_8"),
        (this_or_next|eq, ":village_no", "p_village_9"),
        (this_or_next|eq, ":village_no", "p_village_10"),
        (this_or_next|eq, ":village_no", "p_village_11"),
        (this_or_next|eq, ":village_no", "p_village_12"),
        (this_or_next|eq, ":village_no", "p_village_13"),
        (this_or_next|eq, ":village_no", "p_village_14"),
        (this_or_next|eq, ":village_no", "p_village_15"),
        (this_or_next|eq, ":village_no", "p_village_16"),
        (this_or_next|eq, ":village_no", "p_village_17"),
        (this_or_next|eq, ":village_no", "p_village_18"),
        (this_or_next|eq, ":village_no", "p_village_19"),
        (this_or_next|eq, ":village_no", "p_village_20"),
        (this_or_next|eq, ":village_no", "p_village_21"),
        (this_or_next|eq, ":village_no", "p_village_22"),
        (this_or_next|eq, ":village_no", "p_village_23"),
        (this_or_next|eq, ":village_no", "p_village_24"),
        (this_or_next|eq, ":village_no", "p_village_25"),
        (this_or_next|eq, ":village_no", "p_village_26"),
        (this_or_next|eq, ":village_no", "p_village_27"),
        (this_or_next|eq, ":village_no", "p_village_28"),
        (this_or_next|eq, ":village_no", "p_village_29"),
        (this_or_next|eq, ":village_no", "p_village_30"),
        (this_or_next|eq, ":village_no", "p_village_31"),
        (this_or_next|eq, ":village_no", "p_village_32"),
        (this_or_next|eq, ":village_no", "p_village_33"),
        (this_or_next|eq, ":village_no", "p_village_34"),
        (this_or_next|eq, ":village_no", "p_village_35"),
        (this_or_next|eq, ":village_no", "p_village_36"),
        (this_or_next|eq, ":village_no", "p_village_37"),
        (this_or_next|eq, ":village_no", "p_village_38"),
        (this_or_next|eq, ":village_no", "p_village_39"),
        (this_or_next|eq, ":village_no", "p_village_40"),
        (this_or_next|eq, ":village_no", "p_village_41"),
        (this_or_next|eq, ":village_no", "p_village_42"),
        (this_or_next|eq, ":village_no", "p_village_43"),
        (this_or_next|eq, ":village_no", "p_village_44"),
        (this_or_next|eq, ":village_no", "p_village_45"),
        (this_or_next|eq, ":village_no", "p_village_46"),
        (this_or_next|eq, ":village_no", "p_village_47"),
        (this_or_next|eq, ":village_no", "p_village_48"),
        (this_or_next|eq, ":village_no", "p_village_49"),
        (this_or_next|eq, ":village_no", "p_village_50"),
        (this_or_next|eq, ":village_no", "p_village_51"),
        (this_or_next|eq, ":village_no", "p_village_52"),
        (this_or_next|eq, ":village_no", "p_village_53"),
        (this_or_next|eq, ":village_no", "p_village_54"),
        (this_or_next|eq, ":village_no", "p_village_56"),
        (this_or_next|eq, ":village_no", "p_village_57"),
        (this_or_next|eq, ":village_no", "p_village_59"),
        (this_or_next|eq, ":village_no", "p_village_60"),
        (this_or_next|eq, ":village_no", "p_village_61"),
        (this_or_next|eq, ":village_no", "p_village_62"),
        (this_or_next|eq, ":village_no", "p_village_64"),
        (this_or_next|eq, ":village_no", "p_village_65"),
        (this_or_next|eq, ":village_no", "p_village_66"),
        (this_or_next|eq, ":village_no", "p_village_67"),
        (this_or_next|eq, ":village_no", "p_village_68"),
        (this_or_next|eq, ":village_no", "p_village_69"),
        (this_or_next|eq, ":village_no", "p_village_70"),
        (this_or_next|eq, ":village_no", "p_village_71"),
        (this_or_next|eq, ":village_no", "p_village_72"),
        (this_or_next|eq, ":village_no", "p_village_73"),
        (this_or_next|eq, ":village_no", "p_village_74"),
        (this_or_next|eq, ":village_no", "p_village_75"),
        (this_or_next|eq, ":village_no", "p_village_76"),
        (this_or_next|eq, ":village_no", "p_village_77"),
        (this_or_next|eq, ":village_no", "p_village_78"),
        (this_or_next|eq, ":village_no", "p_village_79"),
        (this_or_next|eq, ":village_no", "p_village_80"),
        (this_or_next|eq, ":village_no", "p_village_81"),
        (this_or_next|eq, ":village_no", "p_village_82"),
        (this_or_next|eq, ":village_no", "p_village_83"),
        (this_or_next|eq, ":village_no", "p_village_84"),
        (this_or_next|eq, ":village_no", "p_village_85"),
        (this_or_next|eq, ":village_no", "p_village_86"),
        (this_or_next|eq, ":village_no", "p_village_87"),
        (this_or_next|eq, ":village_no", "p_village_88"),
        (this_or_next|eq, ":village_no", "p_village_89"),
        (this_or_next|eq, ":village_no", "p_village_90"),
        (this_or_next|eq, ":village_no", "p_village_91"),
        (this_or_next|eq, ":village_no", "p_village_92"),
        (this_or_next|eq, ":village_no", "p_village_93"),
        (this_or_next|eq, ":village_no", "p_village_94"),
        (this_or_next|eq, ":village_no", "p_village_95"),
        (this_or_next|eq, ":village_no", "p_village_96"),
        (this_or_next|eq, ":village_no", "p_village_97"),
        (this_or_next|eq, ":village_no", "p_village_98"),
        (this_or_next|eq, ":village_no", "p_village_99"),
        (this_or_next|eq, ":village_no", "p_village_100"),
        (this_or_next|eq, ":village_no", "p_village_101"),
        (this_or_next|eq, ":village_no", "p_village_102"),
        (this_or_next|eq, ":village_no", "p_village_103"),
        (this_or_next|eq, ":village_no", "p_village_104"),
        (this_or_next|eq, ":village_no", "p_village_105"),
        (this_or_next|eq, ":village_no", "p_village_106"),
        (this_or_next|eq, ":village_no", "p_village_107"),
        (this_or_next|eq, ":village_no", "p_village_108"),
        (this_or_next|eq, ":village_no", "p_village_109"),
        (this_or_next|eq, ":village_no", "p_village_110"),
        (this_or_next|eq, ":village_no", "p_village_111"),
        (this_or_next|eq, ":village_no", "p_village_112"),
        (this_or_next|eq, ":village_no", "p_village_113"),
        (this_or_next|eq, ":village_no", "p_village_114"),
        (this_or_next|eq, ":village_no", "p_village_115"),
        (this_or_next|eq, ":village_no", "p_village_116"),
        (this_or_next|eq, ":village_no", "p_village_117"),
        (this_or_next|eq, ":village_no", "p_village_118"),
        (this_or_next|eq, ":village_no", "p_village_119"),
        (this_or_next|eq, ":village_no", "p_village_120"),
        (this_or_next|eq, ":village_no", "p_village_121"),
        (this_or_next|eq, ":village_no", "p_village_122"),
        (this_or_next|eq, ":village_no", "p_village_123"),
        (this_or_next|eq, ":village_no", "p_village_124"),
        (this_or_next|eq, ":village_no", "p_village_125"),
        (this_or_next|eq, ":village_no", "p_village_126"),
        (this_or_next|eq, ":village_no", "p_village_128"),
        (this_or_next|eq, ":village_no", "p_village_130"),
        (this_or_next|eq, ":village_no", "p_village_131"),
        (this_or_next|eq, ":village_no", "p_village_132"),
        (this_or_next|eq, ":village_no", "p_village_133"),
        (this_or_next|eq, ":village_no", "p_village_134"),
        (this_or_next|eq, ":village_no", "p_village_135"),
        (this_or_next|eq, ":village_no", "p_village_136"),
        (this_or_next|eq, ":village_no", "p_village_137"),
        (this_or_next|eq, ":village_no", "p_village_138"),
        (this_or_next|eq, ":village_no", "p_village_140"),
        (this_or_next|eq, ":village_no", "p_village_141"),
        (this_or_next|eq, ":village_no", "p_village_145"),
        (this_or_next|eq, ":village_no", "p_village_146"),
        (this_or_next|eq, ":village_no", "p_village_148"),
        (this_or_next|eq, ":village_no", "p_village_149"),
        (this_or_next|eq, ":village_no", "p_village_151"),
        (this_or_next|eq, ":village_no", "p_village_153"),
        (this_or_next|eq, ":village_no", "p_village_154"),
        (this_or_next|eq, ":village_no", "p_village_155"),
        (this_or_next|eq, ":village_no", "p_village_156"),
        (this_or_next|eq, ":village_no", "p_village_157"),
        (this_or_next|eq, ":village_no", "p_village_158"),
        (this_or_next|eq, ":village_no", "p_village_159"),
        (this_or_next|eq, ":village_no", "p_village_160"),
        (this_or_next|eq, ":village_no", "p_village_162"),
        (this_or_next|eq, ":village_no", "p_village_163"),
        (this_or_next|eq, ":village_no", "p_village_164"),
        (this_or_next|eq, ":village_no", "p_village_167"),
        (this_or_next|eq, ":village_no", "p_village_169"),
        (this_or_next|eq, ":village_no", "p_village_171"),
        (this_or_next|eq, ":village_no", "p_village_172"),
        (this_or_next|eq, ":village_no", "p_village_173"),
        (this_or_next|eq, ":village_no", "p_village_174"),
        (this_or_next|eq, ":village_no", "p_village_175"),
        (this_or_next|eq, ":village_no", "p_village_178"),
        (this_or_next|eq, ":village_no", "p_village_183"),
        (this_or_next|eq, ":village_no", "p_village_184"),
        (eq, ":village_no", "p_village_185"), 
	  
	    (store_random_in_range, ":random_value_between_15_and_20", 15, 20),
	    (party_set_slot, ":village_no", slot_center_head_sheep, ":random_value_between_15_and_20"),
	  (try_end),
	
	#Frontier (Furs)
	  (try_begin),
        (this_or_next|eq, ":village_no", "p_village_40"), 
        (this_or_next|eq, ":village_no", "p_village_41"), 
        (this_or_next|eq, ":village_no", "p_village_126"), 
        (this_or_next|eq, ":village_no", "p_village_78"), 
        (this_or_next|eq, ":village_no", "p_village_77"), 
        (this_or_next|eq, ":village_no", "p_village_82"), 
        (this_or_next|eq, ":village_no", "p_village_83"), 
        (this_or_next|eq, ":village_no", "p_village_88"), 
        (this_or_next|eq, ":village_no", "p_village_86"), 
        (this_or_next|eq, ":village_no", "p_village_84"), 
        (this_or_next|eq, ":village_no", "p_village_71"), 
        (this_or_next|eq, ":village_no", "p_village_75"), 
        (this_or_next|eq, ":village_no", "p_village_74"), 
        (this_or_next|eq, ":village_no", "p_village_52"), 
        (this_or_next|eq, ":village_no", "p_village_73"), 
        (this_or_next|eq, ":village_no", "p_village_70"), 
        (this_or_next|eq, ":village_no", "p_village_162"), 
        (eq, ":village_no", "p_village_70"),
	  
	    (store_random_in_range, ":random_value_between_1_and_5", 1, 5),
	    (party_set_slot, ":village_no", slot_center_fur_traps, ":random_value_between_1_and_5"),
	  (try_end),
	
	#Iron (Iron)
	  (try_begin),
        (this_or_next|eq, ":village_no", "p_village_126"),
        (this_or_next|eq, ":village_no", "p_village_81"),
        (this_or_next|eq, ":village_no", "p_village_14"),
        (eq, ":village_no", "p_village_67"), 
	  
	    (store_random_in_range, ":random_value_between_10_and_20", 10, 20),
	    (party_set_slot, ":village_no", slot_center_iron_deposits, ":random_value_between_10_and_20"),
	  (try_end),
	
	#Offal (from Sea and River Fish)
      (try_for_range, ":village_no", villages_begin, villages_end),
	    (party_get_slot, ":saltwater_fisheries", ":village_no", slot_center_fishing_fleet),
	    (party_get_slot, ":freshwater_fisheries", ":village_no", slot_center_head_sheep),
	    (store_add, ":total_fisheries", ":saltwater_fisheries", ":freshwater_fisheries"),
	  
	    (party_set_slot, ":village_no", slot_center_apiaries, ":total_fisheries"),
	  (try_end),
	(try_end),
	
	#gekokujo 3.0 forgot to integrate start
	#determining village productions which are bounded by castle by nearby village productions which are bounded by a town.
	(try_for_range, ":village_no", villages_begin, villages_end),
	  (party_get_slot, ":bound_center", ":village_no", slot_village_bound_center),
	  (is_between, ":bound_center", castles_begin, castles_end),

	  (try_for_range, ":cur_production_source", slot_production_sources_begin, slot_production_sources_end),

		(assign, ":total_averaged_production", 0),
		(try_for_range, ":effected_village_no", villages_begin, villages_end),
		  (party_get_slot, ":bound_center", ":effected_village_no", slot_village_bound_center),
	      (is_between, ":bound_center", towns_begin, towns_end),

		  (store_distance_to_party_from_party, ":dist", ":village_no", ":effected_village_no"),
		  (le, ":dist", 72),
		  
		  (party_get_slot, ":production", ":village_no", ":cur_production_source"),
		  
		  (store_add, ":dist_plus_24", ":dist", 24),
		  (store_mul, ":production_mul_12", ":production", 12),
		  (store_div, ":averaged_production", ":production_mul_12", ":dist_plus_24"), #if close (12/24=1/2) else (12/96=1/8)		  
		  (val_div, ":averaged_production", 2), #if close (1/4) else (1/16)
		  (val_add, ":total_averaged_production", ":averaged_production"),
		(try_end),
		
		(party_set_slot, ":village_no", ":cur_production_source", ":total_averaged_production"),
      (try_end),
	(try_end),
	#gekokujo 3.0 forgot to integrate end
	
	#Initialize pastureland
	(try_for_range, ":center", centers_begin, centers_end),
		(party_get_slot, ":head_cattle", ":center", slot_center_head_cattle),
		#(party_get_slot, ":head_sheep", ":center", slot_center_head_sheep),
		(store_mul, ":num_acres", ":head_cattle", 4),
		#(val_add, ":num_acres", ":head_sheep"), 
		#(val_add, ":num_acres", ":head_sheep"), 
		(val_mul, ":num_acres", 6),
		(val_div, ":num_acres", 5),

		(store_random_in_range, ":random", 60, 150),
		(val_mul, ":num_acres", ":random"),
		(val_div, ":num_acres", 100),

		(party_set_slot, ":center", slot_center_acres_pasture, ":num_acres"),		
	(try_end),
	  
	#Initialize prices based on production, etc
    (try_for_range, ":unused", 0, 3), #15 cycles = 45 days. For a village with -20 production, this should lead to approximate +1000, modified	    
        (call_script, "script_update_trade_good_prices"), #changes prices based on production
    (try_end),
	  
	#Initialize prosperity based on final prices
    (try_for_range, ":center_no", centers_begin, centers_end),
      (neg|is_between, ":center_no", castles_begin, castles_end),
      (store_random_in_range, ":random_prosperity_adder", -10, 10),
      (call_script, "script_get_center_ideal_prosperity", ":center_no"),
      (assign, ":prosperity", reg0),
      (val_add, ":prosperity", ":random_prosperity_adder"),
      (val_clamp, ":prosperity", 0, 100),
      (party_set_slot, ":center_no", slot_town_prosperity, ":prosperity"),                
	(try_end),
	
	(call_script, "script_calculate_castle_prosperities_by_using_its_villages"),
    ]),
  #script_initialize_all_scene_prop_slots
  # INPUT: arg1 = scene_prop_no
  # OUTPUT: none
  ("initialize_all_scene_prop_slots",
   [
     (call_script, "script_initialize_scene_prop_slots", "spr_siege_ladder_move_6m"),
     (call_script, "script_initialize_scene_prop_slots", "spr_siege_ladder_move_8m"),
     (call_script, "script_initialize_scene_prop_slots", "spr_siege_ladder_move_10m"),
     (call_script, "script_initialize_scene_prop_slots", "spr_siege_ladder_move_12m"),
     (call_script, "script_initialize_scene_prop_slots", "spr_siege_ladder_move_14m"),
     (call_script, "script_initialize_scene_prop_slots", "spr_castle_e_sally_door_a"),
     (call_script, "script_initialize_scene_prop_slots", "spr_castle_f_sally_door_a"),
     (call_script, "script_initialize_scene_prop_slots", "spr_earth_sally_gate_left"),
     (call_script, "script_initialize_scene_prop_slots", "spr_earth_sally_gate_right"),
     (call_script, "script_initialize_scene_prop_slots", "spr_viking_keep_destroy_sally_door_left"),
     (call_script, "script_initialize_scene_prop_slots", "spr_viking_keep_destroy_sally_door_right"),
     (call_script, "script_initialize_scene_prop_slots", "spr_castle_f_door_a"),
     (call_script, "script_initialize_scene_prop_slots", "spr_belfry_a"),
     (call_script, "script_initialize_scene_prop_slots", "spr_belfry_b"),
     (call_script, "script_initialize_scene_prop_slots", "spr_winch_b"),
    ]),
  #script_initialize_scene_prop_slots
  # INPUT: arg1 = scene_prop_no
  # OUTPUT: none
  ("initialize_scene_prop_slots",
   [
     (store_script_param, ":scene_prop_no", 1),

     (scene_prop_get_num_instances, ":num_instances_of_scene_prop", ":scene_prop_no"),     
     (try_for_range, ":cur_instance", 0, ":num_instances_of_scene_prop"),
       (scene_prop_get_instance, ":cur_instance_id", ":scene_prop_no", ":cur_instance"),
       (try_for_range, ":cur_slot", 0, scene_prop_slots_end),
         (scene_prop_set_slot, ":cur_instance_id", ":cur_slot", 0),
       (try_end),
     (try_end),
     ]),
  #script_use_item
  # INPUT: arg1 = agent_id, arg2 = instance_id
  # OUTPUT: none
  ("use_item",
   [
     (store_script_param, ":instance_id", 1),
     (store_script_param, ":user_id", 2),

     (try_begin),
       (game_in_multiplayer_mode),
       (prop_instance_get_scene_prop_kind, ":scene_prop_id", ":instance_id"),
       (eq, ":scene_prop_id", "spr_winch_b"),
                      
       (multiplayer_get_my_player, ":my_player_no"),

       (this_or_next|gt, ":my_player_no", 0),
       (neg|multiplayer_is_dedicated_server),

       (ge, ":my_player_no", 0),
       (player_get_agent_id, ":my_agent_id", ":my_player_no"),
       (ge, ":my_agent_id", 0),
       (agent_is_active, ":my_agent_id"),
       (agent_get_team, ":my_team_no", ":my_agent_id"),
       (eq, ":my_team_no", 0),
                             
       (scene_prop_get_slot, ":opened_or_closed", ":instance_id", scene_prop_open_or_close_slot),
       (ge, ":user_id", 0),
       (agent_is_active, ":user_id"),
       (agent_get_player_id, ":user_player", ":user_id"),
       (str_store_player_username, s7, ":user_player"),
            
       (try_begin),
         (eq, ":opened_or_closed", 0),
         (display_message, "@{s7} opened the gate"),
       (else_try),  
         (display_message, "@{s7} closed the gate"),
       (try_end),
     (try_end),  

     (prop_instance_get_scene_prop_kind, ":scene_prop_id", ":instance_id"),
     
     (try_begin),
       (this_or_next|eq, ":scene_prop_id", "spr_winch_b"),
       (eq, ":scene_prop_id", "spr_winch"),
       (assign, ":effected_object", "spr_portcullis"),
     (else_try),
       (this_or_next|eq, ":scene_prop_id", "spr_door_destructible"),
       (this_or_next|eq, ":scene_prop_id", "spr_castle_f_door_b"),
       (this_or_next|eq, ":scene_prop_id", "spr_castle_e_sally_door_a"),
       (this_or_next|eq, ":scene_prop_id", "spr_castle_f_sally_door_a"),
       (this_or_next|eq, ":scene_prop_id", "spr_earth_sally_gate_left"),
       (this_or_next|eq, ":scene_prop_id", "spr_earth_sally_gate_right"),
       (this_or_next|eq, ":scene_prop_id", "spr_viking_keep_destroy_sally_door_left"),
       (this_or_next|eq, ":scene_prop_id", "spr_viking_keep_destroy_sally_door_right"),
       (this_or_next|eq, ":scene_prop_id", "spr_castle_f_door_a"),
       (this_or_next|eq, ":scene_prop_id", "spr_siege_ladder_move_6m"),
       (this_or_next|eq, ":scene_prop_id", "spr_siege_ladder_move_8m"),
       (this_or_next|eq, ":scene_prop_id", "spr_siege_ladder_move_10m"),
       (this_or_next|eq, ":scene_prop_id", "spr_siege_ladder_move_12m"),
       (eq, ":scene_prop_id", "spr_siege_ladder_move_14m"),
       (assign, ":effected_object", ":scene_prop_id"),
     (try_end),

     (assign, ":smallest_dist", -1),
     (prop_instance_get_position, pos0, ":instance_id"),
     (scene_prop_get_num_instances, ":num_instances_of_effected_object", ":effected_object"),     
     (try_for_range, ":cur_instance", 0, ":num_instances_of_effected_object"),
       (scene_prop_get_instance, ":cur_instance_id", ":effected_object", ":cur_instance"),
       (prop_instance_get_position, pos1, ":cur_instance_id"),
       (get_sq_distance_between_positions, ":dist", pos0, pos1),
       (this_or_next|eq, ":smallest_dist", -1),
       (lt, ":dist", ":smallest_dist"),
       (assign, ":smallest_dist", ":dist"),
       (assign, ":effected_object_instance_id", ":cur_instance_id"),
     (try_end),

     (try_begin),
       (ge, ":instance_id", 0),
       (ge, ":smallest_dist", 0),

       (try_begin),     
         (eq, ":effected_object", "spr_portcullis"),
         (scene_prop_get_slot, ":opened_or_closed", ":instance_id", scene_prop_open_or_close_slot),

         (try_begin),
           (eq, ":opened_or_closed", 0), #open gate
     
           (scene_prop_enable_after_time, ":instance_id", 400), #4 seconds
           (try_begin),
             (this_or_next|multiplayer_is_server),
             (neg|game_in_multiplayer_mode),
             (prop_instance_get_position, pos0, ":effected_object_instance_id"),
             (position_move_z, pos0, 375),
             (prop_instance_animate_to_position, ":effected_object_instance_id", pos0, 400),
           (try_end),
           (scene_prop_set_slot, ":instance_id", scene_prop_open_or_close_slot, 1),

           (try_begin),
             (eq, ":scene_prop_id", "spr_winch_b"),
             (this_or_next|multiplayer_is_server),
             (neg|game_in_multiplayer_mode),
             (prop_instance_get_position, pos1, ":instance_id"),
             (prop_instance_rotate_to_position, ":instance_id", pos1, 400, 72000),
           (try_end),
         (else_try), #close gate     
           (scene_prop_enable_after_time, ":instance_id", 400), #4 seconds
           (try_begin),
             (this_or_next|multiplayer_is_server),
             (neg|game_in_multiplayer_mode),
             (prop_instance_get_position, pos0, ":effected_object_instance_id"),
             (position_move_z, pos0, -375),
             (prop_instance_animate_to_position, ":effected_object_instance_id", pos0, 400),
           (try_end),
           (scene_prop_set_slot, ":instance_id", scene_prop_open_or_close_slot, 0),

           (try_begin),
             (eq, ":scene_prop_id", "spr_winch_b"),
             (this_or_next|multiplayer_is_server),
             (neg|game_in_multiplayer_mode),
             (prop_instance_get_position, pos1, ":instance_id"),
             (prop_instance_rotate_to_position, ":instance_id", pos1, 400, -72000),
           (try_end),
         (try_end),
       (else_try),
         (this_or_next|eq, ":effected_object", "spr_siege_ladder_move_6m"),
         (this_or_next|eq, ":effected_object", "spr_siege_ladder_move_8m"),
         (this_or_next|eq, ":effected_object", "spr_siege_ladder_move_10m"),
         (this_or_next|eq, ":effected_object", "spr_siege_ladder_move_12m"),
         (eq, ":effected_object", "spr_siege_ladder_move_14m"),

         (try_begin),
           (eq, ":effected_object", "spr_siege_ladder_move_6m"),
           (assign, ":animation_time_drop", 120),
           (assign, ":animation_time_elevate", 240),
         (else_try),
           (eq, ":effected_object", "spr_siege_ladder_move_8m"),
           (assign, ":animation_time_drop", 140),
           (assign, ":animation_time_elevate", 280),
         (else_try),
           (eq, ":effected_object", "spr_siege_ladder_move_10m"),
           (assign, ":animation_time_drop", 160),
           (assign, ":animation_time_elevate", 320),
         (else_try),
           (eq, ":effected_object", "spr_siege_ladder_move_12m"),
           (assign, ":animation_time_drop", 190),
           (assign, ":animation_time_elevate", 360),
         (else_try),
           (eq, ":effected_object", "spr_siege_ladder_move_14m"),
           (assign, ":animation_time_drop", 230),
           (assign, ":animation_time_elevate", 400),
         (try_end),
     
         (scene_prop_get_slot, ":opened_or_closed", ":instance_id", scene_prop_open_or_close_slot),

         (try_begin),
           (scene_prop_enable_after_time, ":effected_object_instance_id", ":animation_time_elevate"), #3 seconds in average
           (eq, ":opened_or_closed", 0), #ladder at ground           
           (prop_instance_get_starting_position, pos0, ":effected_object_instance_id"),
           (prop_instance_enable_physics, ":effected_object_instance_id", 0),
           (prop_instance_animate_to_position, ":effected_object_instance_id", pos0, 300),
           (scene_prop_set_slot, ":effected_object_instance_id", scene_prop_open_or_close_slot, 1), 
         (else_try), #ladder at wall
           (scene_prop_enable_after_time, ":effected_object_instance_id", ":animation_time_drop"), #1.5 seconds in average
           (prop_instance_get_position, pos0, ":instance_id"),

           (assign, ":smallest_dist", -1),
           (try_for_range, ":entry_point_no", multi_entry_points_for_usable_items_start, multi_entry_points_for_usable_items_end),
             (entry_point_get_position, pos1, ":entry_point_no"),
             (get_sq_distance_between_positions, ":dist", pos0, pos1),
             (this_or_next|eq, ":smallest_dist", -1),
             (lt, ":dist", ":smallest_dist"),
             (assign, ":smallest_dist", ":dist"),
             (assign, ":nearest_entry_point", ":entry_point_no"),
           (try_end),

           (try_begin),
             (ge, ":smallest_dist", 0),
             (lt, ":smallest_dist", 22500), #max 15m distance
             (entry_point_get_position, pos1, ":nearest_entry_point"),
             (position_rotate_x, pos1, -90),
             (scene_prop_set_slot, ":effected_object_instance_id", scene_prop_smoke_effect_done, 0),
             (prop_instance_enable_physics, ":effected_object_instance_id", 0),
             (prop_instance_animate_to_position, ":effected_object_instance_id", pos1, 130),
           (try_end),

           (scene_prop_set_slot, ":effected_object_instance_id", scene_prop_open_or_close_slot, 0),
         (try_end),
       (else_try),
         (this_or_next|eq, ":effected_object", "spr_door_destructible"),
         (this_or_next|eq, ":effected_object", "spr_castle_f_door_b"),
         (this_or_next|eq, ":scene_prop_id", "spr_castle_e_sally_door_a"),     
         (this_or_next|eq, ":scene_prop_id", "spr_castle_f_sally_door_a"),     
         (this_or_next|eq, ":scene_prop_id", "spr_earth_sally_gate_left"),     
         (this_or_next|eq, ":scene_prop_id", "spr_earth_sally_gate_right"),     
         (this_or_next|eq, ":scene_prop_id", "spr_viking_keep_destroy_sally_door_left"),     
         (this_or_next|eq, ":scene_prop_id", "spr_viking_keep_destroy_sally_door_right"),     
         (eq, ":scene_prop_id", "spr_castle_f_door_a"),
     
         (assign, ":effected_object_instance_id", ":instance_id"),
         (scene_prop_get_slot, ":opened_or_closed", ":effected_object_instance_id", scene_prop_open_or_close_slot),

         (try_begin),
           (eq, ":opened_or_closed", 0),

           (prop_instance_get_starting_position, pos0, ":effected_object_instance_id"),

           (scene_prop_enable_after_time, ":effected_object_instance_id", 100),

           (try_begin),
             (neg|eq, ":scene_prop_id", "spr_viking_keep_destroy_sally_door_left"),
             (neg|eq, ":scene_prop_id", "spr_earth_sally_gate_left"),
             
             (position_rotate_z, pos0, -85),
           (else_try),  
             (position_rotate_z, pos0, 85),
           (try_end),
           
           (prop_instance_animate_to_position, ":effected_object_instance_id", pos0, 100),
          
           (scene_prop_set_slot, ":effected_object_instance_id", scene_prop_open_or_close_slot, 1),
         (else_try),          
           (prop_instance_get_starting_position, pos0, ":effected_object_instance_id"),

           (scene_prop_enable_after_time, ":effected_object_instance_id", 100),

           (prop_instance_animate_to_position, ":effected_object_instance_id", pos0, 100),

           (scene_prop_set_slot, ":effected_object_instance_id", scene_prop_open_or_close_slot, 0),
         (try_end),
       (try_end),
     (try_end),
     ]),
  #script_game_get_party_prisoner_limit:
  # This script is called from the game engine when the prisoner limit is needed for a party.
  # INPUT: arg1 = party_no
  # OUTPUT: reg0 = prisoner_limit
  ("game_get_party_prisoner_limit",
    [
#		(store_script_param_1, ":party_no"),
		(assign, ":troop_no", "trp_player"),
		
		(assign, ":limit", 0),
		(store_skill_level, ":skill", "skl_prisoner_management", ":troop_no"),
		(store_mul, ":limit", ":skill", 5),
		
		#gekokujo 3.0 party size bonus to prisoner limit start
		#(assign, reg0, ":limit"),
		(call_script, "script_party_count_fit_regulars", "p_main_party"),
		(assign, ":party_size", reg0),
		(val_div, ":party_size", 10),
		
		(store_add, reg0, ":limit", ":party_size"),
		#gekokujo 3.0 party size bonus to prisoner limit end
		
		(set_trigger_result, reg0),
  ]),
  #script_game_get_item_extra_text:
  # This script is called from the game engine when an item's properties are displayed.
  # INPUT: arg1 = item_no, arg2 = extra_text_id (this can be between 0-7 (7 included)), arg3 = item_modifier
  # OUTPUT: result_string = item extra text, trigger_result = text color (0 for default)
  ("game_get_item_extra_text",
    [
      (store_script_param, ":item_no", 1),
      (store_script_param, ":extra_text_id", 2),
      (store_script_param, ":item_modifier", 3),
      (try_begin),
        (is_between, ":item_no", food_begin, food_end),
        (try_begin),
          (eq, ":extra_text_id", 0),
          (assign, ":continue", 1),
          (try_begin),
            (this_or_next|eq, ":item_no", "itm_cattle_meat"),
            (this_or_next|eq, ":item_no", "itm_pork"),
				(eq, ":item_no", "itm_chicken"),
				
            (eq, ":item_modifier", imod_rotten),
            (assign, ":continue", 0),
          (try_end),
          (eq, ":continue", 1),
          (item_get_slot, ":food_bonus", ":item_no", slot_item_food_bonus),
          (assign, reg1, ":food_bonus"),
          (set_result_string, "@+{reg1} to party morale"),
          (set_trigger_result, 0x4444FF),
        (try_end),
      (else_try),
        (is_between, ":item_no", readable_books_begin, readable_books_end),
        (try_begin),
          (eq, ":extra_text_id", 0),
          (item_get_slot, reg1, ":item_no", slot_item_intelligence_requirement),
          (set_result_string, "@Requires {reg1} intelligence to read"),
          (set_trigger_result, 0xFFEEDD),
        (else_try),
          (eq, ":extra_text_id", 1),
          (item_get_slot, ":progress", ":item_no", slot_item_book_reading_progress),
          (val_div, ":progress", 10),
          (assign, reg1, ":progress"),
          (set_result_string, "@Reading Progress: {reg1}%"),
          (set_trigger_result, 0xFFEEDD),
        (try_end),
      (else_try),
        (is_between, ":item_no", reference_books_begin, reference_books_end),
        (try_begin),
          (eq, ":extra_text_id", 0),
          (try_begin),
            (eq, ":item_no", "itm_book_wound_treatment_reference"),
            (str_store_string, s1, "@wound treament"),
          (else_try),
            (eq, ":item_no", "itm_book_training_reference"),
            (str_store_string, s1, "@trainer"),
          (else_try),
            (eq, ":item_no", "itm_book_surgery_reference"),
            (str_store_string, s1, "@surgery"),
          (try_end),
          (set_result_string, "@+1 to {s1} while in inventory"),
          (set_trigger_result, 0xFFEEDD),
        (try_end),
      (try_end),
  ]),
  #script_game_on_disembark:
  # This script is called from the game engine when the player reaches the shore with a ship.
  # INPUT: pos0 = disembark position
  # OUTPUT: none
  ("game_on_disembark",
   [(jump_to_menu, "mnu_disembark"),
  ]),
  #script_game_context_menu_get_buttons:
  # This script is called from the game engine when the player clicks the right mouse button over a party on the map.
  # INPUT: arg1 = party_no
  # OUTPUT: none, fills the menu buttons
  ("game_context_menu_get_buttons",
   [
     (store_script_param, ":party_no", 1),
     (try_begin),
       (neq, ":party_no", "p_main_party"),
       (context_menu_add_item, "@Move here", cmenu_move),
     (try_end),
        
     (try_begin),
       (is_between, ":party_no", centers_begin, centers_end),
       (context_menu_add_item, "@View notes", 1),
     (else_try),
       (party_get_num_companion_stacks, ":num_stacks", ":party_no"),
       (gt, ":num_stacks", 0),
       (party_stack_get_troop_id, ":troop_no", ":party_no", 0),
       ##diplomacy start+ support for promoted kingdom ladies
       (is_between, ":troop_no", heroes_begin, heroes_end),
       (this_or_next|troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
       ##diplomacy end+
       (is_between, ":troop_no", active_npcs_begin, active_npcs_end),
       (context_menu_add_item, "@View notes", 2),
     (try_end),
    
     (try_begin),
       (neq, ":party_no", "p_main_party"),       
       (store_faction_of_party, ":party_faction", ":party_no"),
                     
       (this_or_next|eq, ":party_faction", "$players_kingdom"),
       (this_or_next|eq, ":party_faction", "fac_player_supporters_faction"),
       (party_slot_eq, ":party_no", slot_party_type, spt_kingdom_caravan),
       
       (neg|is_between, ":party_no", centers_begin, centers_end),
       
       (context_menu_add_item, "@Accompany", cmenu_follow), 
     (try_end),    
  ]),
  #script_game_event_context_menu_button_clicked:
  # This script is called from the game engine when the player clicks on a button at the right mouse menu.
  # INPUT: arg1 = party_no, arg2 = button_value
  # OUTPUT: none
  ("game_event_context_menu_button_clicked",
   [(store_script_param, ":party_no", 1),
    (store_script_param, ":button_value", 2),
    (try_begin),
      (eq, ":button_value", 1),
      (change_screen_notes, 3, ":party_no"),
    (else_try),
      (eq, ":button_value", 2),
      (party_stack_get_troop_id, ":troop_no", ":party_no", 0),
      (change_screen_notes, 1, ":troop_no"),
    (try_end),
  ]),
  #script_game_get_skill_modifier_for_troop
  # This script is called from the game engine when a skill's modifiers are needed
  # INPUT: arg1 = troop_no, arg2 = skill_no
  # OUTPUT: trigger_result = modifier_value
  ("game_get_skill_modifier_for_troop",
   [(store_script_param, ":troop_no", 1),
    (store_script_param, ":skill_no", 2),
    (assign, ":modifier_value", 0),
    (try_begin),
      (eq, ":skill_no", "skl_wound_treatment"),
      (call_script, "script_get_troop_item_amount", ":troop_no", "itm_book_wound_treatment_reference"),
      (gt, reg0, 0),
      (val_add, ":modifier_value", 1),
    (else_try),
      (eq, ":skill_no", "skl_trainer"),
      (call_script, "script_get_troop_item_amount", ":troop_no", "itm_book_training_reference"),
      (gt, reg0, 0),
      (val_add, ":modifier_value", 1),
    (else_try),
      (eq, ":skill_no", "skl_surgery"),
      (call_script, "script_get_troop_item_amount", ":troop_no", "itm_book_surgery_reference"),
      (gt, reg0, 0),
      (val_add, ":modifier_value", 1),
    (try_end),
    (set_trigger_result, ":modifier_value"),
    ]),
#script_game_check_party_sees_party
# This script is called from the game engine when a party is inside the range of another party
# INPUT: arg1 = party_no_seer, arg2 = party_no_seen
# OUTPUT: trigger_result = true or false (1 = true, 0 = false)
	("game_check_party_sees_party",
	[
	(store_script_param_1, ":party_no_seer"),
	(store_script_param_2, ":party_no_seen"),

	(assign, ":trigger_result", 1),
	(assign, ":save_reg0", reg0),

	#Lords who dislike raiding caravans should not attack village_farmer or kingdom_caravan
	#parties.  Achieve this by stopping them from seeing them.
	(try_begin),
		(gt, ":party_no_seer", spawn_points_end),
		(gt, ":party_no_seen", spawn_points_end),

		#Only apply this when the "seer" is a kingdom hero party
		(party_slot_eq, ":party_no_seer", slot_party_type, spt_kingdom_hero_party),

		#Only needed if the seen party is of a hostile faction
		(call_script, "script_get_relation_between_parties", ":party_no_seer", ":party_no_seen"),
		(lt, reg0, 0),

		#Only apply this when the seen party is a merchant caravan or villagers
		#(party_get_template_id, ":template", ":party_no_seen"),
		(this_or_next|party_slot_eq, ":party_no_seen", slot_party_type, spt_kingdom_caravan),
		(this_or_next|party_slot_eq,":party_no_seen", slot_party_type, dplmc_spt_gift_caravan),#custom diplomacy caravan
			(party_slot_eq, ":party_no_seen", slot_party_type, spt_village_farmer),

		#Never apply this when the seen party is engaging in hostile actions
		(party_get_battle_opponent, reg0, ":party_no_seen"),
		(lt, reg0, 0),
		(neg|party_slot_eq, ":party_no_seen", slot_party_ai_state, spai_besieging_center),
		(neg|party_slot_eq, ":party_no_seen", slot_party_ai_state, spai_raiding_around_center),
		(neg|party_slot_eq, ":party_no_seen", slot_party_ai_state, spai_engaging_army),
		(neg|party_slot_eq, ":party_no_seen", slot_party_ai_state, spai_accompanying_army),
		(neg|party_slot_eq, ":party_no_seen", slot_party_ai_state, spai_screening_army),


		#Only apply this when the leader is tmt_humanitarian, lrep_benefactor, or lrep_moralist
		(party_get_num_companion_stacks, ":num_stacks", ":party_no_seer"),
		(ge, ":num_stacks", 1),
		(party_stack_get_troop_id, ":leader", ":party_no_seer", 0),
		(ge, ":leader", 1),
		(troop_is_hero, ":leader"),
		(call_script, "script_dplmc_get_troop_morality_value", ":leader", tmt_humanitarian),
		(ge, reg0, 0),# (never apply for leaders who like raiding caravans and attacking villagers)
		(this_or_next|ge, reg0, 1),
		(this_or_next|troop_slot_eq, ":leader", slot_lord_reputation_type, lrep_benefactor),
			(troop_slot_eq, ":leader", slot_lord_reputation_type, lrep_moralist),
		(assign, ":trigger_result", 0),
	(try_end),

	(assign, reg0, ":save_reg0"),
	(set_trigger_result, ":trigger_result"),
	]),
##diplomacy begin
  #script_game_get_party_speed_multiplier
  # This script is called from the game engine when a skill's modifiers are needed
  # INPUT: arg1 = party_no
  # OUTPUT: trigger_result = multiplier (scaled by 100, meaning that giving 100 as the trigger result does not change the party speed)
("game_get_party_speed_multiplier",
  [
    (store_script_param_1, ":party_no"),

    (assign,":speed_multiplier",100),

    (try_begin),
      (this_or_next|eq,":party_no","p_main_party"),
      (party_slot_eq, ":party_no", slot_party_type, spt_kingdom_hero_party),
      (party_get_skill_level, ":pathfinding_skill", ":party_no", skl_pathfinding),
      (val_mul,":pathfinding_skill",3),
      (val_add,":speed_multiplier",":pathfinding_skill"),
    (try_end),

    (try_begin),
      (eq,":party_no","p_main_party"),
      (eq,"$g_move_fast", 1),
      (val_mul,":speed_multiplier",2),
    (try_end),

    (val_max, ":speed_multiplier", 0),
    (set_trigger_result, ":speed_multiplier"),
   ]),
  #script_setup_talk_info
  # INPUT: $g_talk_troop, $g_talk_troop_relation
  ("setup_talk_info",
    [
      ##diplomacy start+ Ensure $character_gender is set correctly (it should have been set during character creation)
      (try_begin),
         (call_script, "script_cf_dplmc_troop_is_female", "trp_player"),
	     (assign, "$character_gender", 1),
      (else_try),
	     (assign, "$character_gender", 0),
      (try_end),
	  ##diplomacy end+
      (talk_info_set_relation_bar, "$g_talk_troop_relation"),
      (str_store_troop_name, s61, "$g_talk_troop"),
      (str_store_string, s61, "@{!} {s61}"),
      (assign, reg1, "$g_talk_troop_relation"),
      (str_store_string, s62, "str_relation_reg1"),
      (talk_info_set_line, 0, s61),
      (talk_info_set_line, 1, s62),
      (call_script, "script_describe_relation_to_s63", "$g_talk_troop_relation"),
      (talk_info_set_line, 3, s63),
  ]),
#NPC companion changes begin
  #script_setup_talk_info_companions
  ("setup_talk_info_companions",
    [
      ##diplomacy start+ Ensure $character_gender is set correctly (it should have been set during character creation)
      (try_begin),
         (call_script, "script_cf_dplmc_troop_is_female", "trp_player"),
	     (assign, "$character_gender", 1),
      (else_try),
	     (assign, "$character_gender", 0),
      (try_end),
	  ##diplomacy end+
      (call_script, "script_npc_morale", "$g_talk_troop"),
      (assign, ":troop_morale", reg0),

      (talk_info_set_relation_bar, ":troop_morale"),

      (str_store_troop_name, s61, "$g_talk_troop"),
      (str_store_string, s61, "@{!} {s61}"),
      (assign, reg1, ":troop_morale"),
      (str_store_string, s62, "str_morale_reg1"),
      (talk_info_set_line, 0, s61),
      (talk_info_set_line, 1, s62),
      (talk_info_set_line, 3, s63),
  ]),
  #script_cf_training_ground_sub_routine_1_for_melee_details
  # INPUT:
  # value
  #OUTPUT:
  # none
  ("cf_training_ground_sub_routine_1_for_melee_details",
   [
     (store_script_param, ":value", 1),
     (ge, "$temp_3", ":value"),
     (val_add, ":value", 1),
     (troop_get_slot, ":troop_id", "trp_stack_selection_ids", ":value"),
     (str_store_troop_name, s0, ":troop_id"),
     ]),
  #script_training_ground_sub_routine_2_for_melee_details
  # INPUT:
  # value
  #OUTPUT:
  # none
  ("training_ground_sub_routine_2_for_melee_details",
   [
     (store_script_param, ":value", 1),
     (val_sub, ":value", 1),
     (try_begin),
       (lt, ":value", 0),
       (call_script, "script_remove_random_fit_party_member_from_stack_selection"),
     (else_try),
       (call_script, "script_remove_fit_party_member_from_stack_selection", ":value"),
     (try_end),
     (assign, ":troop_id", reg0),
     (store_sub, ":slot_index", "$temp_2", 1),
     (troop_set_slot, "trp_temp_array_a", ":slot_index", ":troop_id"),
     (try_begin),
       (eq, "$temp", "$temp_2"),
       (call_script, "script_start_training_at_training_ground", -1, "$temp"),
     (else_try),
       (val_add, "$temp_2", 1),
       (jump_to_menu, "mnu_training_ground_selection_details_melee_2"),
     (try_end),
     ]),
  #script_cf_training_ground_sub_routine_for_training_result
  # INPUT:
  # arg1: troop_id, arg2: stack_no, arg3: troop_count, arg4: xp_ratio_to_add
  #OUTPUT:
  # none
  ("cf_training_ground_sub_routine_for_training_result",
   [
     (store_script_param, ":troop_id", 1),
     (store_script_param, ":stack_no", 2),
     (store_script_param, ":amount", 3),
     (store_script_param, ":xp_ratio_to_add", 4),

     (store_character_level, ":level", ":troop_id"),
     (store_add, ":level_added", ":level", 5),
     (store_mul, ":min_hardness", ":level_added", 3),
     (val_min, ":min_hardness", 100),
     (store_sub, ":hardness_dif", ":min_hardness", "$g_training_ground_training_hardness"),
     (val_max, ":hardness_dif", 0),
     (store_sub, ":hardness_dif", 100, ":hardness_dif"),
     (val_mul, ":hardness_dif", ":hardness_dif"),
     (val_div, ":hardness_dif", 10), # value over 1000
##     (assign, reg0, ":hardness_dif"),
##     (display_message, "@Hardness difference: {reg0}/1000"),
     (store_mul, ":xp_ratio_to_add_for_stack", ":xp_ratio_to_add", ":hardness_dif"),
     (val_div, ":xp_ratio_to_add_for_stack", 1000),
     (try_begin),
       (eq, ":troop_id", "trp_player"),
       (val_mul, ":xp_ratio_to_add_for_stack", 1),
     (else_try),
       (try_begin),
         (eq, "$g_mt_mode", ctm_melee),
         (try_begin),
           (this_or_next|troop_is_guarantee_ranged, ":troop_id"),
           (troop_is_guarantee_horse, ":troop_id"),
           (val_div, ":xp_ratio_to_add_for_stack", 4),
         (try_end),
       (else_try),
         (eq, "$g_mt_mode", ctm_mounted),
         (try_begin),
           (neg|troop_is_guarantee_horse, ":troop_id"),
           (assign, ":xp_ratio_to_add_for_stack", 0),
         (try_end),
       (else_try),
         (neg|troop_is_guarantee_ranged, ":troop_id"),
         (assign, ":xp_ratio_to_add_for_stack", 0),
       (try_end),
     (try_end),
     (val_add,  ":level", 1),
     (store_mul, ":xp_to_add", 100, ":level"),
     (val_mul, ":xp_to_add", ":amount"),
     (val_div, ":xp_to_add", 20),
     (val_mul, ":xp_to_add", ":xp_ratio_to_add_for_stack"),
     (val_div, ":xp_to_add", 1000),
     (store_mul, ":max_xp_to_add", ":xp_to_add", 3),
     (val_div, ":max_xp_to_add", 2),
     (store_div, ":min_xp_to_add", ":xp_to_add", 2),
     (store_random_in_range, ":random_xp_to_add", ":min_xp_to_add", ":max_xp_to_add"),
     (gt, ":random_xp_to_add", 0),
     (try_begin),
       (troop_is_hero, ":troop_id"),
       (add_xp_to_troop, ":random_xp_to_add", ":troop_id"),
       (store_div, ":proficiency_to_add", ":random_xp_to_add", 50),
       (try_begin),
         (gt, ":proficiency_to_add", 0),
         (troop_raise_proficiency, ":troop_id", "$g_training_ground_used_weapon_proficiency", ":proficiency_to_add"),
       (try_end),
     (else_try),
       (party_add_xp_to_stack, "p_main_party", ":stack_no", ":random_xp_to_add"),
     (try_end),
     (assign, reg0, ":random_xp_to_add"),
     ]),
  #script_print_troop_owned_centers_in_numbers_to_s0
  # INPUT:
  # param1: troop_no
  #OUTPUT:
  # string register 0.
  ("print_troop_owned_centers_in_numbers_to_s0",
   [
     (store_script_param_1, ":troop_no"),
     (str_store_string, s0, "@nothing"),
     (assign, ":owned_towns", 0),
     (assign, ":owned_castles", 0),
     (assign, ":owned_villages", 0),
     (try_for_range_backwards, ":cur_center", centers_begin, centers_end),
       (party_slot_eq, ":cur_center", slot_town_lord, ":troop_no"),
       (try_begin),
         (party_slot_eq, ":cur_center", slot_party_type, spt_town),
         (val_add, ":owned_towns", 1),
       (else_try),
         (party_slot_eq, ":cur_center", slot_party_type, spt_castle),
         (val_add, ":owned_castles", 1),
       (else_try),
         (val_add, ":owned_villages", 1),
       (try_end),
     (try_end),
     (assign, ":num_types", 0),
     (try_begin),
       (gt, ":owned_villages", 0),
       (assign, reg0, ":owned_villages"),
       (store_sub, reg1, reg0, 1),
       (str_store_string, s0, "@{reg0} village{reg1?s:}"),
       (val_add, ":num_types", 1),
     (try_end),
     (try_begin),
       (gt, ":owned_castles", 0),
       (assign, reg0, ":owned_castles"),
       (store_sub, reg1, reg0, 1),
       (try_begin),
         (eq, ":num_types", 0),
         (str_store_string, s0, "@{reg0} castle{reg1?s:}"),
       (else_try),
         (str_store_string, s0, "@{reg0} castle{reg1?s:} and {s0}"),
       (try_end),
       (val_add, ":num_types", 1),
     (try_end),
     (try_begin),
       (gt, ":owned_towns", 0),
       (assign, reg0, ":owned_towns"),
       (store_sub, reg1, reg0, 1),
       (try_begin),
         (eq, ":num_types", 0),
         (str_store_string, s0, "@{reg0} town{reg1?s:}"),
       (else_try),
         (eq, ":num_types", 1),
         (str_store_string, s0, "@{reg0} town{reg1?s:} and {s0}"),
       (else_try),
         (str_store_string, s0, "@{reg0} town{reg1?s:}, {s0}"),
       (try_end),
     (try_end),
     (store_add, reg0, ":owned_villages", ":owned_castles"),
     (val_add, reg0, ":owned_towns"),
     ]),
  #script_get_random_melee_training_weapon
  # INPUT: none
  # OUTPUT: reg0 = weapon_1, reg1 = weapon_2
  ("get_random_melee_training_weapon",
   [
     (assign, ":weapon_1", -1),
     (assign, ":weapon_2", -1),
     (store_random_in_range, ":random_no", 0, 3),
     (try_begin),
       (eq, ":random_no", 0),
       (assign, ":weapon_1", "itm_gekokujo_practice_jo"),
     (else_try),
       (eq, ":random_no", 1),
       (assign, ":weapon_1", "itm_gekokujo_practice_katana"),
       (assign, ":weapon_2", "itm_gekokujo_practice_wakizashi"),
     (else_try),
       (assign, ":weapon_1", "itm_gekokujo_practice_nodachi"),
     (try_end),
     (assign, reg0, ":weapon_1"),
     (assign, reg1, ":weapon_2"),
     ]),
  #script_start_training_at_training_ground
  # INPUT:
  # param1: training_weapon_type, param2: training_param
  ("start_training_at_training_ground",
   [
     (val_add, "$g_training_ground_training_count", 1),
     (store_script_param, ":mission_weapon_type", 1),
     (store_script_param, ":training_param", 2),

     (set_jump_mission, "mt_training_ground_training"),

     (assign, ":training_default_weapon_1", -1),
     (assign, ":training_default_weapon_2", -1),
     (assign, ":training_default_weapon_3", -1),
     (assign, "$scene_num_total_gourds_destroyed", 0),
     (try_begin),
       (eq, ":mission_weapon_type", itp_type_bow),
       (assign, "$g_training_ground_used_weapon_proficiency", wpt_archery),
       (assign, ":training_default_weapon_1", "itm_gekokujo_practice_yumi"),
       (try_begin),
         (eq, "$g_mt_mode", ctm_mounted),
         (assign, ":training_default_weapon_2", "itm_gekokujo_arrows_2"),
       (else_try),
         (assign, ":training_default_weapon_2", "itm_gekokujo_arrows_1"),
       (try_end),
     (else_try),
       (eq, ":mission_weapon_type", itp_type_crossbow),
       (assign, "$g_training_ground_used_weapon_proficiency", wpt_archery),
       (assign, ":training_default_weapon_1", "itm_gekokujo_practice_yumi"),
       (assign, ":training_default_weapon_2", "itm_gekokujo_arrows_1"),
     (else_try),
       (eq, ":mission_weapon_type", itp_type_thrown),
       (assign, "$g_training_ground_used_weapon_proficiency", wpt_throwing),
       (try_begin),
         (eq, "$g_mt_mode", ctm_mounted),
         (assign, ":training_default_weapon_2", "itm_gekokujo_practice_kunai"),
       (else_try),
         (assign, ":training_default_weapon_2", "itm_gekokujo_practice_kunai"),
       (try_end),
     (else_try),
       (eq, ":mission_weapon_type", itp_type_one_handed_wpn),
       (assign, "$g_training_ground_used_weapon_proficiency", wpt_one_handed_weapon),
       (assign, ":training_default_weapon_1", "itm_gekokujo_practice_katana"),
     (else_try),
       (eq, ":mission_weapon_type", itp_type_polearm),
       (assign, "$g_training_ground_used_weapon_proficiency", wpt_polearm),
       (assign, ":training_default_weapon_1", "itm_gekokujo_practice_yari"),
     (else_try),
       #weapon_type comes as -1 when melee training is selected
       (assign, "$g_training_ground_used_weapon_proficiency", wpt_one_handed_weapon),
       (call_script, "script_get_random_melee_training_weapon"),
       (assign, ":training_default_weapon_1", reg0),
       (assign, ":training_default_weapon_2", reg1),
     (try_end),
     
##     (assign, "$g_training_ground_training_troop_stack_index", ":stack_index"),
     (try_begin),
       (eq, "$g_mt_mode", ctm_mounted),
       (assign, ":training_default_weapon_3", "itm_practice_horse"),
       (store_add, "$g_training_ground_training_scene", "scn_training_ground_horse_track_1", "$g_encountered_party"),
       (val_sub, "$g_training_ground_training_scene", training_grounds_begin),
     (else_try),
       (store_add, "$g_training_ground_training_scene", "scn_training_ground_ranged_melee_1", "$g_encountered_party"),
       (val_sub, "$g_training_ground_training_scene", training_grounds_begin),
     (try_end),

     (modify_visitors_at_site, "$g_training_ground_training_scene"),
     (reset_visitors),
     (set_visitor, 0, "trp_player"),

     (assign, ":selected_weapon", -1),
     (try_for_range, ":cur_slot", 0, 4),#equipment slots
       (troop_get_inventory_slot, ":cur_item", "trp_player", ":cur_slot"),
       (ge, ":cur_item", 0),
       (item_get_type, ":item_type", ":cur_item"),
       (try_begin),
         (eq, ":item_type", ":mission_weapon_type"),
         (eq, ":selected_weapon", -1),
         (assign, ":selected_weapon", ":cur_item"),
       (try_end),
     (try_end),
     (mission_tpl_entry_clear_override_items, "mt_training_ground_training", 0),
     (mission_tpl_entry_add_override_item, "mt_training_ground_training", 0, "itm_gekokujo_sandal_2"),
     (try_begin),
       (ge, ":training_default_weapon_1", 0),
       (try_begin),
         (ge, ":selected_weapon", 0),
         (mission_tpl_entry_add_override_item, "mt_training_ground_training", 0, ":selected_weapon"),
       (else_try),
         (mission_tpl_entry_add_override_item, "mt_training_ground_training", 0, ":training_default_weapon_1"),
       (try_end),
     (try_end),
     (try_begin),
       (ge, ":training_default_weapon_2", 0),
       (mission_tpl_entry_add_override_item, "mt_training_ground_training", 0, ":training_default_weapon_2"),
     (try_end),
     (try_begin),
       (ge, ":training_default_weapon_3", 0),
       (mission_tpl_entry_add_override_item, "mt_training_ground_training", 0, ":training_default_weapon_3"),
     (try_end),

     (assign, ":cur_visitor_point", 5),
     (troop_get_slot, ":num_fit", "trp_stack_selection_amounts", 1),
     (store_add, ":end_cond", 5, ":num_fit"),
     (val_min, ":end_cond", 13),
     (try_for_range, ":cur_visitor_point", 5, ":end_cond"),
       (call_script, "script_remove_random_fit_party_member_from_stack_selection"),
       (set_visitor, ":cur_visitor_point", reg0),
       (val_add, ":cur_visitor_point", 1),
     (try_end),
     (try_begin),
       (eq, "$g_mt_mode", ctm_melee),
       (assign, ":total_difficulty", 0),
       (try_for_range, ":i", 0, ":training_param"),
         (troop_get_slot, ":cur_troop", "trp_temp_array_a", ":i"),
         (store_add, ":cur_entry_point", ":i", 1),
         (set_visitor, ":cur_entry_point", ":cur_troop"),
         (mission_tpl_entry_clear_override_items, "mt_training_ground_training", ":cur_entry_point"),
         (mission_tpl_entry_add_override_item, "mt_training_ground_training", ":cur_entry_point", "itm_gekokujo_sandal_1"),
         (call_script, "script_get_random_melee_training_weapon"),
         (mission_tpl_entry_add_override_item, "mt_training_ground_training", ":cur_entry_point", reg0),
         (try_begin),
           (ge, reg1, 0),
           (mission_tpl_entry_add_override_item, "mt_training_ground_training", ":cur_entry_point", reg1),
         (try_end),
         (store_character_level, ":cur_troop_level", ":cur_troop"),
         (val_add, ":cur_troop_level", 10),
         (val_mul, ":cur_troop_level", ":cur_troop_level"),
         (val_add, ":total_difficulty", ":cur_troop_level"),
       (try_end),

       (assign, "$g_training_ground_training_num_enemies", ":training_param"),
       (assign, "$g_training_ground_training_hardness",  ":total_difficulty"),
       (store_add, ":number_multiplier", "$g_training_ground_training_num_enemies", 4),
       (val_mul, "$g_training_ground_training_hardness", ":number_multiplier"),
       (val_div, "$g_training_ground_training_hardness", 2400),
       (str_store_string, s0, "@Your opponents are ready for the fight."),
     (else_try),
       (eq, "$g_mt_mode", ctm_mounted),
       (try_begin),
         (eq, ":mission_weapon_type", itp_type_bow),
         (assign, "$g_training_ground_training_hardness", 350),
         (assign, "$g_training_ground_training_num_gourds_to_destroy", 30),
       (else_try),
         (eq, ":mission_weapon_type", itp_type_thrown),
         (assign, "$g_training_ground_training_hardness", 400),
         (assign, "$g_training_ground_training_num_gourds_to_destroy", 30),
       (else_try),
         (eq, ":mission_weapon_type", itp_type_one_handed_wpn),
         (assign, "$g_training_ground_training_hardness", 200),
         (assign, "$g_training_ground_training_num_gourds_to_destroy", 45),
       (else_try),
         (eq, ":mission_weapon_type", itp_type_polearm),
         (assign, "$g_training_ground_training_hardness", 280),
         (assign, "$g_training_ground_training_num_gourds_to_destroy", 35),
       (try_end),
       (str_store_string, s0, "@Try to destroy as many targets as you can. You have two and a half minutes to clear the track."),
     (else_try),
       (eq, "$g_mt_mode", ctm_ranged),
       (store_mul, "$g_training_ground_ranged_distance", ":training_param", 100),
       (assign, ":hardness_modifier", ":training_param"),
       (val_mul, ":hardness_modifier", ":hardness_modifier"),
       (try_begin),
         (eq, ":mission_weapon_type", itp_type_bow),
         (val_mul, ":hardness_modifier", 3),
         (val_div, ":hardness_modifier", 2),
       (else_try),
         (eq, ":mission_weapon_type", itp_type_thrown),
         (val_mul, ":hardness_modifier", 5),
         (val_div, ":hardness_modifier", 2),
         (val_mul, ":hardness_modifier", ":training_param"),
         (val_div, ":hardness_modifier", 2),
       (try_end),
       (store_mul, "$g_training_ground_training_hardness", 100, ":hardness_modifier"),
       (val_div, "$g_training_ground_training_hardness", 6000),
       (str_store_string, s0, "@Stay behind the line on the ground and shoot the targets. Try not to waste any shots."),
     (try_end),
     (jump_to_menu, "mnu_training_ground_description"),
     ]),
  # script_get_percentage_with_randomized_round
  # Input: arg1 = value, arg2 = percentage
  # Output: none
  ("get_percentage_with_randomized_round",
    [
      (store_script_param, ":value", 1),
      (store_script_param, ":percentage", 2),

      (store_mul, ":result", ":value", ":percentage"),
      (val_div, ":result", 100),
      (store_mul, ":used_amount", ":result", 100),
      (val_div, ":used_amount", ":percentage"),
      (store_sub, ":left_amount", ":value", ":used_amount"),
      (try_begin),
        (gt, ":left_amount", 0),
        (store_mul, ":chance", ":left_amount", ":percentage"),
        (store_random_in_range, ":random_no", 0, 100),
        (lt, ":random_no", ":chance"),
        (val_add, ":result", 1),
      (try_end),
      (assign, reg0, ":result"),
      ]),
  # script_setup_random_scene
  # Input: arg1 = center_no, arg2 = mission_template_no
  # Output: none
  ("setup_random_scene",
    [
      (party_get_current_terrain, ":terrain_type", "p_main_party"),
      (assign, ":scene_to_use", "scn_random_scene"),
      (try_begin),
        (eq, ":terrain_type", rt_steppe),
		#gekokujo 3.0 road battles start
        ##(assign, ":scene_to_use", "scn_random_scene_steppe"),
		#(store_random_in_range, ":scene_seed", 0, 3),
		#(try_begin),
		#  (eq, ":scene_seed", 0),
        #  (assign, ":scene_to_use", "scn_gekokujo_road_1"),
		#(else_try),
		#  (eq, ":scene_seed", 1),
        #  (assign, ":scene_to_use", "scn_gekokujo_road_2"),
		#(else_try),
        #  (assign, ":scene_to_use", "scn_gekokujo_road_3"),
		#(try_end),
		#gekokujo 3.0 road battles end

        (eq, ":terrain_type", rt_plain),
        (assign, ":scene_to_use", "scn_random_scene_plain"),
      (else_try),
        (eq, ":terrain_type", rt_snow),
        (assign, ":scene_to_use", "scn_random_scene_snow"),
      (else_try),
        (eq, ":terrain_type", rt_desert),
		#gekokujo 3.0 bridge battles start
        ##(assign, ":scene_to_use", "scn_random_scene_desert"),
		#(store_random_in_range, ":scene_seed", 0, 3),
		#(try_begin),
		#  (eq, ":scene_seed", 0),
        #  (assign, ":scene_to_use", "scn_gekokujo_bridge_1"),
		#(else_try),
		#  (eq, ":scene_seed", 1),
        #  (assign, ":scene_to_use", "scn_gekokujo_bridge_2"),
		#(else_try),
        #  (assign, ":scene_to_use", "scn_gekokujo_bridge_3"),
		#(try_end),
		(assign, ":scene_to_use", "scn_random_scene_plain_small"), #gosh dang it
		#gekokujo 3.0 bridge battles end
      (else_try),
        (eq, ":terrain_type", rt_steppe_forest),
        (assign, ":scene_to_use", "scn_random_scene_steppe_forest"),
      (else_try),
        (eq, ":terrain_type", rt_forest),
        (assign, ":scene_to_use", "scn_random_scene_plain_forest"),
      (else_try),
        (eq, ":terrain_type", rt_snow_forest),
        (assign, ":scene_to_use", "scn_random_scene_snow_forest"),
      (else_try),
        (eq, ":terrain_type", rt_desert_forest),
        (assign, ":scene_to_use", "scn_random_scene_desert_forest"),
      (else_try),
        (eq, ":terrain_type", rt_water),
        (assign, ":scene_to_use", "scn_water"),
      (else_try),
        (eq, ":terrain_type", rt_bridge),
        #(assign, ":scene_to_use", "scn_random_scene_plain"),
		#gekokujo 3.0 sea battles start
		
		#first, count how many are on the player's side
		(party_get_num_companions, ":player_count", "p_main_party"),
		(try_begin),
		  (gt, "$g_ally_party", 0),
		  (party_get_num_companions, ":ally_count", "$g_ally_party"),
		  (val_add, ":player_count", ":ally_count"),
		(try_end),
		(assign, reg9, ":player_count"),
		#(display_log_message, "@there are {reg9} allies"),
		
		#second, count the enemy
		(try_begin),
		  (gt, "$g_enemy_party", 0),
		  (party_get_num_companions, ":enemy_count", "$g_enemy_party"),
		(else_try),
		  (party_get_num_companions, ":enemy_count", "$g_encountered_party"),
		(try_end),
		(assign, reg9, ":enemy_count"),
		#(display_log_message, "@there are {reg9} enemies"),
		
		#third, determine the attacker and defender
		(try_begin), #the enemy is the attacker
		  (encountered_party_is_attacker),
		  (assign, ":attacker", ":enemy_count"),
		  (assign, ":defender", ":player_count"),
		  #(display_log_message, "@the enemy is the attacker"),
		(else_try), #the player is the attacker
		  (assign, ":attacker", ":player_count"),
		  (assign, ":defender", ":enemy_count"),
		  #(display_log_message, "@you are the attacker"),
		(try_end),
		
		#now, assign the correct scene
		(try_begin), #small (attacker) vs small (defender)
		  (lt, ":attacker", 10),
		  (lt, ":defender", 10),
		  (assign, ":scene_to_use", "scn_gekokujo_sea_1"),
		  #(display_log_message, "@small vs small"),
		(else_try), #small vs medium
		  (lt, ":attacker", 10),
		  (is_between, ":defender", 10, 30),
		  (assign, ":scene_to_use", "scn_gekokujo_sea_2"),
		  #(display_log_message, "@small vs medium"),
		(else_try), #medium vs small
		  (is_between, ":attacker", 10, 30),
		  (lt, ":defender", 10),
		  (assign, ":scene_to_use", "scn_gekokujo_sea_3"),
		  #(display_log_message, "@medium vs small"),
		(else_try), #medium vs medium
		  (is_between, ":attacker", 10, 30),
		  (is_between, ":defender", 10, 30),
		  (assign, ":scene_to_use", "scn_gekokujo_sea_4"),
		  #(display_log_message, "@medium vs medium"),
		(else_try), #small vs large
		  (lt, ":attacker", 10),
		  (ge, ":defender", 30),
		  (assign, ":scene_to_use", "scn_gekokujo_island_1"),
		  #(display_log_message, "@small vs large"),
		(else_try), #medium vs large
		  (is_between, ":attacker", 10, 30),
		  (ge, ":defender", 30),
		  (assign, ":scene_to_use", "scn_gekokujo_island_2"),
		  #(display_log_message, "@medium vs large"),
		(else_try), #large vs small
		  (ge, ":attacker", 30),
		  (lt, ":defender", 10),
		  (assign, ":scene_to_use", "scn_gekokujo_island_3"),
		  #(display_log_message, "@large vs small"),
		(else_try), #large vs medium
		  (ge, ":attacker", 30),
		  (is_between, ":defender", 10, 30),
		  (assign, ":scene_to_use", "scn_gekokujo_island_4"),
		  #(display_log_message, "@large vs medium"),
		(else_try), #large vs large
		  (assign, ":scene_to_use", "scn_gekokujo_island_5"),
		  #(display_log_message, "@large vs large"),
		(try_end),
		#gekokujo 3.0 sea battles end
      (try_end),
      ## CC
      (party_get_battle_opponent, ":opponent", "p_main_party"),
      (try_begin),
        (le, ":opponent", 0), # do nothing
      (else_try),
        (val_add, ":scene_to_use", "$g_random_scene_size"),
        (val_sub, ":scene_to_use", 1),
      (try_end),
      ## CC
      (jump_to_scene,":scene_to_use"),
  ]),
  # script_enter_dungeon
  # Input: arg1 = center_no, arg2 = mission_template_no
  # Output: none
  ("enter_dungeon",
    [
      (store_script_param_1, ":center_no"),
      (store_script_param_2, ":mission_template_no"),
      
      (set_jump_mission,":mission_template_no"),
      #new added...
      (mission_tpl_entry_set_override_flags, ":mission_template_no", 0, af_override_horse),
      (try_begin),
        (eq, "$sneaked_into_town", 1),
        (mission_tpl_entry_set_override_flags, ":mission_template_no", 0, af_override_all),                
        
        (mission_tpl_entry_clear_override_items, ":mission_template_no", 0),
        (mission_tpl_entry_add_override_item, ":mission_template_no", 0, "itm_gekokujo_monk_headwrap"),
        (mission_tpl_entry_add_override_item, ":mission_template_no", 0, "itm_gekokujo_kimono_2_monk"),
        (mission_tpl_entry_add_override_item, ":mission_template_no", 0, "itm_gekokujo_katana_1"),
        (mission_tpl_entry_add_override_item, ":mission_template_no", 0, "itm_gekokujo_shuriken"),
      (try_end),   
      #new added end              

      (party_get_slot, ":dungeon_scene", ":center_no", slot_town_prison),
      
      (modify_visitors_at_site,":dungeon_scene"),
      (reset_visitors),
      (assign, ":cur_pos", 16),
	  
	  
      (call_script, "script_get_heroes_attached_to_center_as_prisoner", ":center_no", "p_temp_party"),
      (party_get_num_companion_stacks, ":num_stacks","p_temp_party"),
	  ##diplomacy start+ Allow some variation in which prisoners appear,
      #when there are too many to all fit in the jail at once.
      (try_begin),
         	(gt, ":num_stacks", 15),
            (store_random_in_range, ":offset", 0, ":num_stacks"),
      (else_try),
           	(assign, ":offset", 0),
      (try_end),
      ##diplomacy end+
      (try_for_range, ":i_stack", 0, ":num_stacks"),
      ##diplomacy start+
        (val_add, ":i_stack", ":offset"),
        (try_begin),
           (ge, ":i_stack", ":num_stacks"),
           (val_sub, ":i_stack", ":num_stacks"),
        (try_end),
      ##diplomacy end+
        (party_stack_get_troop_id, ":stack_troop","p_temp_party",":i_stack"),

		(assign, ":prisoner_offered_parole", 0),
		(try_begin),
			(party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
		(else_try),
			(call_script, "script_cf_prisoner_offered_parole", ":stack_troop"),
			(assign, ":prisoner_offered_parole", 1),
		(else_try),
			(assign, ":prisoner_offered_parole", 0),
		(try_end),
		(eq, ":prisoner_offered_parole", 0),
		
        (lt, ":cur_pos", 32), # spawn up to entry point 32
        (set_visitor, ":cur_pos", ":stack_troop"),
        (val_add,":cur_pos", 1),
      (try_end),
      	 
#	  (set_visitor, ":cur_pos", "trp_npc3"),
#	  (troop_set_slot, "trp_npc3", slot_troop_prisoner_of_party, "$g_encountered_party"),	  
	  
      (set_jump_entry, 0),
      (jump_to_scene,":dungeon_scene"),
      (scene_set_slot, ":dungeon_scene", slot_scene_visited, 1),
      (change_screen_mission),
  ]),
  # script_find_high_ground_around_pos1
  # Input: pos1 should hold center_position_no
  #        arg1: team_no
  #        arg2: search_radius (in meters)
  # Output: pos52 contains highest ground within <search_radius> meters of team leader
  # Destroys position registers: pos10, pos11, pos15
  ("find_high_ground_around_pos1",
    [
      (store_script_param, ":team_no", 1),
      (store_script_param, ":search_radius", 2),
      (val_mul, ":search_radius", 100),
      (get_scene_boundaries, pos10,pos11),
      (team_get_leader, ":ai_leader", ":team_no"),
      (agent_get_position, pos1, ":ai_leader"),
      (set_fixed_point_multiplier, 100),
      (position_get_x, ":o_x", pos1),
      (position_get_y, ":o_y", pos1),
      (store_sub, ":min_x", ":o_x", ":search_radius"),
      (store_sub, ":min_y", ":o_y", ":search_radius"),
      (store_add, ":max_x", ":o_x", ":search_radius"),
      (store_add, ":max_y", ":o_y", ":search_radius"),
      (position_get_x, ":scene_min_x", pos10),
      (position_get_x, ":scene_max_x", pos11),
      (position_get_y, ":scene_min_y", pos10),
      (position_get_y, ":scene_max_y", pos11),
      #do not find positions close to borders (20 m)
      (val_add, ":scene_min_x", 2000),
      (val_sub, ":scene_max_x", 2000),
      (val_add, ":scene_min_y", 2000),
      (val_sub, ":scene_max_y", 2000),
      (val_max, ":min_x", ":scene_min_x"),
      (val_max, ":min_y", ":scene_min_y"),
      (val_min, ":max_x", ":scene_max_x"),
      (val_min, ":max_y", ":scene_max_y"),
      
      (store_div, ":min_x_meters", ":min_x", 100),
      (store_div, ":min_y_meters", ":min_y", 100),
      (store_div, ":max_x_meters", ":max_x", 100),
      (store_div, ":max_y_meters", ":max_y", 100),
      
      (assign, ":highest_pos_z", -10000),
      (copy_position, pos52, pos1),
      (init_position, pos15),
      
      (try_for_range, ":i_x", ":min_x_meters", ":max_x_meters"),
        (store_mul, ":i_x_cm", ":i_x", 100),
        (try_for_range, ":i_y", ":min_y_meters", ":max_y_meters"),
          (store_mul, ":i_y_cm", ":i_y", 100),
          (position_set_x, pos15, ":i_x_cm"),
          (position_set_y, pos15, ":i_y_cm"),
          (position_set_z, pos15, 10000),
          (position_set_z_to_ground_level, pos15),
          (position_get_z, ":cur_pos_z", pos15),
          (try_begin),
            (gt, ":cur_pos_z", ":highest_pos_z"),
            (copy_position, pos52, pos15),
            (assign, ":highest_pos_z", ":cur_pos_z"),
          (try_end),
        (try_end),
      (try_end),
  ]),
  # script_round_value
  # Input: arg1 = value
  # Output: reg0 = rounded_value
  ("round_value",
    [
      (store_script_param_1, ":value"),
      (try_begin),
        (lt, ":value", 100),
        (neq, ":value", 0),
        (val_add, ":value", 5),
        (val_div, ":value", 10),
        (val_mul, ":value", 10),
        (try_begin),
          (eq, ":value", 0),
          (assign, ":value", 5),
        (try_end),
      (else_try),
        (lt, ":value", 300),
        (val_add, ":value", 25),
        (val_div, ":value", 50),
        (val_mul, ":value", 50),
      (else_try),
        (val_add, ":value", 50),
        (val_div, ":value", 100),
        (val_mul, ":value", 100),
      (try_end),
      (assign, reg0, ":value"),
  ]),
  #script_get_max_skill_of_player_party
  # INPUT: arg1 = skill_no
  # OUTPUT: reg0 = max_skill, reg1 = skill_owner_troop_no
  ("get_max_skill_of_player_party",
    [(store_script_param, ":skill_no", 1),
     (party_get_num_companion_stacks, ":num_stacks","p_main_party"),
     (store_skill_level, ":max_skill", ":skill_no", "trp_player"),
     (assign, ":skill_owner", "trp_player"),
     (try_for_range, ":i_stack", 0, ":num_stacks"),
       (party_stack_get_troop_id, ":stack_troop","p_main_party",":i_stack"),
       (troop_is_hero, ":stack_troop"),
       (neg|troop_is_wounded, ":stack_troop"),
       (store_skill_level, ":cur_skill", ":skill_no", ":stack_troop"),
       (gt, ":cur_skill", ":max_skill"),
       (assign, ":max_skill", ":cur_skill"),
       (assign, ":skill_owner", ":stack_troop"),
     (try_end),
     (party_get_skill_level, reg0, "p_main_party", ":skill_no"),
##     (assign, reg0, ":max_skill"),
     (assign, reg1, ":skill_owner"),
     ]),
  #script_get_improvement_details
  # INPUT: arg1 = improvement
  # OUTPUT: reg0 = base_cost
  ("get_improvement_details",
    [(store_script_param, ":improvement_no", 1),
     (try_begin),
       (eq, ":improvement_no", slot_center_has_manor),
       (str_store_string, s0, "@Manor"),
       (str_store_string, s1, "@A manor lets you rest at the village and pay your troops half wages while you rest."),
       (assign, reg0, 8000),
     (else_try),
       (eq, ":improvement_no", slot_center_has_fish_pond),
       (str_store_string, s0, "@Mill"),
       (str_store_string, s1, "@A mill increases village prosperity by 5%."),
       (assign, reg0, 6000),
     (else_try),
       (eq, ":improvement_no", slot_center_has_watch_tower),
       (str_store_string, s0, "@Watch Tower"),
       (str_store_string, s1, "@A watch tower lets the villagers raise alarm earlier. The time it takes for enemies to loot the village increases by 50%."),
       (assign, reg0, 5000),
     (else_try),
       (eq, ":improvement_no", slot_center_has_school),
       (str_store_string, s0, "@Shrine"),
       (str_store_string, s1, "@A Shinto shrine increases the loyality of the villagers to you by +1 every month."),
       (assign, reg0, 9000),
     (else_try),
       (eq, ":improvement_no", slot_center_has_messenger_post),
       (str_store_string, s0, "@Messenger Post"),
       (str_store_string, s1, "@A messenger post lets the inhabitants send you a message whenever enemies are nearby, even if you are far away from here."),
       (assign, reg0, 4000),
     (else_try),
       (eq, ":improvement_no", slot_center_has_prisoner_tower),
       (str_store_string, s0, "@Prison Tower"),
       (str_store_string, s1, "@A prison tower reduces the chance of captives held here running away successfully."),
       (assign, reg0, 7000),
     (try_end),
     ]),
  #script_cf_troop_agent_is_alive
  # INPUT: arg1 = troop_id
  ("cf_troop_agent_is_alive",
    [(store_script_param, ":troop_no", 1),
     (assign, ":alive_count", 0),
     (try_for_agents, ":cur_agent"),
       (agent_get_troop_id, ":cur_agent_troop", ":cur_agent"),
       (eq, ":troop_no", ":cur_agent_troop"),
       (agent_is_alive, ":cur_agent"),
       (val_add, ":alive_count", 1),
     (try_end),
     (gt, ":alive_count", 0),
     ]),
  # script_debug_variables
  # Input: two variables which will be examined by coder, this script is only for debugging.
  # Output: none
  ("debug_variables",
    [
      (store_script_param, ":unused", 1),
      (store_script_param, ":unused_2", 2),
    ]),
  # script_cf_is_melee_weapon_for_tutorial
  # Input: arg1 = item_no
  # Output: none (can fail)
  ("cf_is_melee_weapon_for_tutorial",
    [
      (store_script_param, ":item_no", 1),
      (assign, ":result", 0),
      (try_begin),
        (this_or_next|eq, ":item_no", "itm_gekokujo_practice_jo"),
        (eq, ":item_no", "itm_gekokujo_practice_katana"),
        (assign, ":result", 1),
      (try_end),
      (eq, ":result", 1),
     ]),
  # script_iterate_pointer_arrow
  # Input: none
  # Output: none
  ("iterate_pointer_arrow",
    [
      (store_mission_timer_a_msec, ":cur_time"),
      (try_begin),
        (assign, ":up_down", ":cur_time"),
        (assign, ":turn_around", ":cur_time"),
        (val_mod, ":up_down", 1080),
        (val_div, ":up_down", 3),
        (scene_prop_get_instance, ":prop_instance", "spr_pointer_arrow", 0),
        (prop_instance_get_position, pos0, ":prop_instance"),
        (position_set_z_to_ground_level, pos0),
        (position_move_z, pos0, "$g_pointer_arrow_height_adder", 1),
        (set_fixed_point_multiplier, 100),
        (val_mul, ":up_down", 100),
        (store_sin, ":up_down_sin", ":up_down"),
        (position_move_z, pos0, ":up_down_sin", 1),
        (position_move_z, pos0, 100, 1),
        (val_mod, ":turn_around", 2880),
        (val_div, ":turn_around", 8),
        (init_position, pos1),
        (position_rotate_z, pos1, ":turn_around"),
        (position_copy_rotation, pos0, pos1),
        (prop_instance_set_position, ":prop_instance", pos0),
      (try_end),
     ]),
  # script_check_concilio_calradi_achievement  
  ("check_concilio_calradi_achievement",
  [
   (try_begin),
     (eq, "$players_kingdom", "fac_player_supporters_faction"),
     (faction_get_slot, ":player_faction_king", "fac_player_supporters_faction", slot_faction_leader),
     (eq, ":player_faction_king", "trp_player"),
     (assign, ":number_of_vassals", 0),
     (try_for_range, ":cur_troop", active_npcs_begin, active_npcs_end),
       (troop_slot_eq, ":cur_troop", slot_troop_occupation, slto_kingdom_hero),
       (store_faction_of_troop, ":cur_faction", ":cur_troop"),
       (eq, ":cur_faction", "fac_player_supporters_faction"),
       (val_add, ":number_of_vassals", 1),
     (try_end),
     (ge, ":number_of_vassals", 3),
     (unlock_achievement, ACHIEVEMENT_CONCILIO_CALRADI),
   (try_end),  
  ]),
#gekokujo 3.0 foraging skill start
  ## FORAGING v1.0 #######################################################################
  ## Script food_consumption_display_message
  ## display food consumption
  ## use reg1 and reg2 and reg4 from forage
  ## hooked in simple trigger for food consumption every 14 hours
  ("food_consumption_display_message",
   [
    (store_script_param, ":num_men", 1),

    (assign, reg1, ":num_men"),
    # Display day of food left with current amount and party size
    (assign, ":available_food", 0),
    (troop_get_inventory_capacity, ":capacity", "trp_player"),
    (try_for_range, ":cur_slot", 0, ":capacity"),
      (troop_get_inventory_slot, ":cur_item", "trp_player", ":cur_slot"),
      (try_begin),
        (is_between, ":cur_item", food_begin, food_end),
        (troop_get_inventory_slot_modifier, ":item_modifier", "trp_player", ":cur_slot"),
        (neq, ":item_modifier", imod_rotten),
        (troop_inventory_slot_get_item_amount, ":cur_amount", "trp_player", ":cur_slot"),
        (val_add, ":available_food", ":cur_amount"),
      (try_end),
    (try_end),
    
    (assign, ":num_food_hours", ":available_food"),
    (val_mul, ":num_food_hours", 14),
    (val_div, ":num_food_hours", 24),
    (val_div, ":num_food_hours", ":num_men"),
    (assign, ":num_food_days", ":num_food_hours"),
    (assign, reg2, ":num_food_days"),
    
    (try_begin),
      (lt, reg2, 4),
      (display_message, "@Your party consumed {reg1} units of food{reg4?, {reg4} from foraging : }({reg2} days left).", 0xFF0000),
    (else_try),
      (display_message, "@Your party consumed {reg1} units of food{reg4?, {reg4} from foraging : }({reg2} days left)."),
    (try_end),
   ]),
  # Script forage_for_food
  # Compute foraging amount
  # use s2, reg0, reg1 and reg10
  # for DEBUG, use s1 and reg11
  # use reg4 for return value
  ("forage_for_food",
   [
        # Get max skill in party for foraging
        (call_script, "script_get_max_skill_of_player_party", "skl_shield"),
        (assign, ":max_foraging_in_party", reg0),
        (assign, ":max_skill_owner", reg1),

        # Initialize foraged food amount and register
        (assign, ":foraged_food", 0),
        (assign, reg4, 0),
        
        (try_begin),
          # stop if no-one has foraging skill
          (gt, ":max_foraging_in_party", 0),

          (try_begin),
            # set limits and range for foraging
            (assign,  ":foraging_limit", ":max_foraging_in_party"),
            (val_mul, ":foraging_limit", 5),
            (assign,  ":foraging_distance", ":max_foraging_in_party"),
            (val_mul, ":foraging_distance", 2),

            # Check distance from village or town
            (try_for_parties,":foraging_site"),
              (assign, ":foraged_food_at_site", 0),
              (this_or_next|party_slot_eq, ":foraging_site", slot_party_type, spt_town),
              (party_slot_eq, ":foraging_site", slot_party_type, spt_village),
              (neg|party_slot_eq, ":foraging_site", slot_village_state, svs_looted), # no foraging from looted village

              # Compute center distance to party
              (store_distance_to_party_from_party, ":distance", ":foraging_site", "p_main_party"),
              (try_begin),
                (le,":distance",":foraging_distance"), # we can forage from this center

                # Forage from fields
                (party_get_slot, ":temp_forage", ":foraging_site", slot_center_acres_grain),
                (val_div, ":temp_forage", 1000), # 500 was too low, try 1000
                (val_add, ":foraged_food_at_site", ":temp_forage"),

                (party_get_slot, ":temp_forage", ":foraging_site", slot_center_acres_vineyard),
                (val_div, ":temp_forage", 800), # 400 was too low, try 800
                (val_add, ":foraged_food_at_site", ":temp_forage"),

                (party_get_slot, ":temp_forage", ":foraging_site", slot_center_acres_vineyard), # second time for fruits
                (val_div, ":temp_forage", 1000), # 500 was too low, try 1000
                (val_add, ":foraged_food_at_site", ":temp_forage"),

                (party_get_slot, ":temp_forage", ":foraging_site", slot_center_acres_olives),
                (val_div, ":temp_forage", 1200), # 600 was too low, try 1200
                (val_add, ":foraged_food_at_site", ":temp_forage"),

                (party_get_slot, ":temp_forage", ":foraging_site", slot_center_acres_dates),
                (val_div, ":temp_forage", 960), # 480 was to low, try 960
                (val_add, ":foraged_food_at_site", ":temp_forage"),

                # Forage from herds
                (party_get_slot, ":temp_forage", ":foraging_site", slot_center_head_cattle),
                (val_div, ":temp_forage", 36),
                (val_add, ":foraged_food_at_site", ":temp_forage"),

                (party_get_slot, ":temp_forage", ":foraging_site", slot_center_head_sheep),
                (val_div, ":temp_forage", 60),
                (val_add, ":foraged_food_at_site", ":temp_forage"),

                # Forage from gardens and apiaries
                (party_get_slot, ":temp_forage", ":foraging_site", slot_center_household_gardens),
                (val_add, ":foraged_food_at_site", 2),

                (party_get_slot, ":temp_forage", ":foraging_site", slot_center_apiaries),
                (val_add, ":foraged_food_at_site", 1),
 
                # Forage game in traps
                (party_get_slot, ":temp_forage", ":foraging_site", slot_center_fur_traps),
                (val_add, ":foraged_food_at_site", ":temp_forage"),

                # Add amount foraged off the center to the total
                (val_add, ":foraged_food", ":foraged_food_at_site"),

                # DEBUG message to tweak values, uncomment to display
                #(str_store_party_name, s1, ":foraging_site"),
                #(assign, reg11, ":foraged_food_at_site"),
                #(display_message, "@DEBUG foraging: foraged {reg11} units from {s1}.", 0xFF00FF),
              (try_end),
            (try_end), # end of centers loop

            # Check terrain for foraging from the countryside
            (party_get_current_terrain, ":cur_terrain", "p_main_party"),
            (try_begin),
              (is_between, ":cur_terrain", rt_bridge, rt_desert_forest),
              (assign, reg10, 4),
            (else_try),
              (is_between, ":cur_terrain", rt_steppe, rt_plain),
              (assign, reg10, 2),
            (else_try),
              (assign, reg10, 0),
            (try_end),

            # Add foraged amount from countryside to total amount
            (val_add, ":foraged_food", reg10),

            # DEBUG message to tweak values, uncomment to display
            #(display_message, "@DEBUG foraging: foraged {reg10} units from countryside.", 0xFF00FF),

            # Tier Multiplier, foraging value multiplied by foraging skill tier bonus
            # Represent experience, less time to find forage means more food foraged
            (try_begin), 
              # between 2-4, x1.5 bonus
              (gt, ":max_foraging_in_party", 1),
              (lt, ":max_foraging_in_party", 5),
              (val_mul, ":foraged_food", 3), 
              (val_div, ":foraged_food", 2), 
            (else_try), 
              # between 5-7, x2 bonus
              (gt, ":max_foraging_in_party", 4),
              (lt, ":max_foraging_in_party", 8),
              (val_mul, ":foraged_food", 2), 
            (else_try), 
              # between 8-9, x2.5 bonus
              (gt, ":max_foraging_in_party", 7),
              (lt, ":max_foraging_in_party", 10),
              (val_mul, ":foraged_food", 5), 
              (val_div, ":foraged_food", 2), 
            (else_try), 
              # 10 and more, x3 bonus
              (ge, ":max_foraging_in_party", 10),
              (val_mul, ":foraged_food", 3), 
            (try_end),

            # Apply Camp bonus x1.5 (represent more time to forage)
            (try_begin),
              #(this_or_next|ge, "$current_camp_party", -1), # uncomment if using Entrenchment
              (this_or_next|eq, "$g_camp_mode", 1), 
              (eq, "$g_siege_force_wait", 1),
              (val_mul, ":foraged_food", 3),
              (val_div, ":foraged_food", 2),        
            (try_end),

            # Apply foraging limit according to skill level (modified by party bonus)
            (try_begin),
              (gt, ":foraged_food", ":foraging_limit"),
              (assign, ":foraged_food", ":foraging_limit"),
            (try_end),

            # assign amount foraged to register to deduct from party consumption
            (assign, reg4, ":foraged_food"),

            # End of foraging message
            (try_begin),
              (gt, ":foraged_food", 0),
              (str_store_troop_name, s2, ":max_skill_owner"),
              (display_message, "@{s2} managed to forage {reg4} units of food to complement supplies.", 0x00FF00),
            (try_end),
          (try_end),
        (try_end),
   ]),
#gekokujo 3.1 integrating 1.166 change start
  #Equipment cost fix
   ("player_get_value_of_original_items",
    [
      (store_script_param, ":player_no", 1),  
      (store_script_param, ":agent_no", 2),
      (store_script_param, ":troop_id", 3),
      (assign, ":total_equipment_cost", 0),
      (try_for_range, ":i_item_slot", 0, 8), 
          (neg|player_item_slot_is_picked_up, ":player_no", ":i_item_slot"),
          (agent_get_item_slot, ":item_id", ":agent_no", ":i_item_slot"), #value between 0-7, order is weapon1, weapon2, weapon3, weapon4, head_armor, body_armor, leg_armor, hand_armor
          #(player_get_item_id, ":item_id", ":player_no", ":i_item_slot"), #only for server
          (neq, ":item_id", -1),
          (call_script, "script_multiplayer_get_item_value_for_troop", ":item_id", ":troop_id"),
          (val_add, ":total_equipment_cost", reg0),

          #Debugging
          #(assign, reg1, ":total_equipment_cost"),
          #(str_store_item_name, s0, ":item_id"),
          #(multiplayer_send_string_to_player, ":player_no", multiplayer_event_show_server_message, "@{s0} for {reg0}g added to total equipment cost, which is now: {reg1}g"),
          ##
      (try_end),
      (try_for_agents, ":cur_horse"),
         #Check all horses in the scene and see if one of them is agent_no's bought horse. Won't be enough to just do (agent_get_horse, ":horse", ":agent_no"), 
         #since you get money back for a bought horse, even if you have dismounted it, if the horse is still alive and has no other rider.
         (agent_is_alive, ":cur_horse"),
         (neg|agent_is_human, ":cur_horse"),  #Spawned agent is horse
         (agent_get_slot, ":agent_no_bought_horse", ":agent_no", slot_agent_bought_horse),
         (eq, ":agent_no_bought_horse", ":cur_horse"),
         (assign, ":add_horse_cost_to_equipment_value", 0),
         (try_begin),
             (agent_get_rider, ":rider_agent_id", ":cur_horse"),
             (try_begin),
                 (neq, ":rider_agent_id", -1),
                 (neg|agent_is_non_player, ":rider_agent_id"),
                 (agent_get_slot, ":agent_no_bought_horse", ":rider_agent_id", slot_agent_bought_horse),          
                 (eq, ":agent_no_bought_horse", ":cur_horse"), #agent_no is mounted on the same horse he bought
                 (assign, ":add_horse_cost_to_equipment_value", 1),

                 #Debugging
                 #(agent_get_item_id, ":mount_type", ":cur_horse"), #(works only for horses, returns -1 otherwise)
                 #(str_store_item_name, s0, ":mount_type"),
                 #(multiplayer_send_string_to_player, ":player_no", multiplayer_event_show_server_message, "@You are mounted on your bought {s0} and will get money for it"),
                 ##
             (else_try),
                 (eq, ":rider_agent_id", -1), #If cur_horse doesn't have a rider
                 (agent_get_horse, ":agent_no_mount", ":agent_no"),
                 (eq, ":agent_no_mount", -1), #If agent_no is not mounted on another horse
                 (agent_get_slot, ":agent_no_bought_horse", ":agent_no", slot_agent_bought_horse),
                 (eq, ":agent_no_bought_horse", ":cur_horse"),
                 (assign, ":add_horse_cost_to_equipment_value", 1),

                 #Debugging
                 #(agent_get_item_id, ":mount_type", ":cur_horse"), #(works only for horses, returns -1 otherwise)
                 #(str_store_item_name, s0, ":mount_type"),
                 #(multiplayer_send_string_to_player, ":player_no", multiplayer_event_show_server_message, "@Your bought {s0} is alive so you get money for it"),
                 ##
            (try_end),
            (eq, ":add_horse_cost_to_equipment_value", 1),
            (agent_get_item_id, ":cur_mount_type", ":cur_horse"), #Checks which type the horse is
            (call_script, "script_multiplayer_get_item_value_for_troop", ":cur_mount_type", ":troop_id"),
            (val_add, ":total_equipment_cost", reg0),
            (multiplayer_send_string_to_player, ":player_no", multiplayer_event_show_server_message, "@Added money for your old horse"),
         (try_end),
      (try_end),
      (agent_set_slot, ":agent_no", slot_agent_bought_horse, -1),
      (assign, reg0, ":total_equipment_cost"),
     ]),
#gekokujo 3.1 siege improvement end
#llf
#parabola
  # script_cf_quadratic_roots
  # Input:  <a_fixed_point>, <b_fixed_point>, <c_fixed_point> : ax^2+bx+c=0
  # Output: <reg0> - number of roots, <reg1_fixed_point> - first root, <reg2_fixed_point> - second root
  # Note:   Fixed_point_multiplier can be any. It will be converted for precise calculation.
("cf_quadratic_roots", [
    (store_script_param, ":a", 1),
    (store_script_param, ":b", 2),
    (store_script_param, ":c", 3),
    (try_begin),
      (eq, ":a", 0),
      (assign, reg0, 0),
      (assign, reg1, -1),
      (assign, reg2, -1),
    (else_try),
      (assign, ":save_fpm", 1),
      (convert_to_fixed_point, ":save_fpm"),
      (set_fixed_point_multiplier, 100000), # precise calculation
      (convert_to_fixed_point, ":a"),
      (convert_to_fixed_point, ":b"),
      (convert_to_fixed_point, ":c"),
      (val_div, ":a", ":save_fpm"),
      (val_div, ":b", ":save_fpm"),
      (val_div, ":c", ":save_fpm"),
      (store_mul, ":b2", ":b", ":b"),
      (convert_from_fixed_point, ":b2"),
      (val_mul, ":c", ":a"),
      (convert_from_fixed_point, ":c"),
      (val_mul, ":c", 4),
      (val_sub, ":b2", ":c"),
      (try_begin),
        (lt, ":b2", 0),
        (assign, reg0, 0),
        (assign, reg1, -1),
        (assign, reg2, -1),
      (else_try),
        (eq, ":b2", 0),
        (assign, reg0, 1),
        (assign, reg2, -1),
        (store_mul, reg1, ":b", -1),
        (val_mul, ":a", 2),
        (convert_to_fixed_point, reg1),
        (val_div, reg1, ":a"),
        (val_mul, reg1, ":save_fpm"),
        (convert_from_fixed_point, reg1),
      (else_try),
        (assign, reg0, 2),
        (store_sqrt, reg1, ":b2"),
        (store_mul, reg2, reg1, -1),
        (val_sub, reg1, ":b"),
        (val_sub, reg2, ":b"),
        (val_mul, ":a", 2),
        (convert_to_fixed_point, reg1),
        (convert_to_fixed_point, reg2),
        (val_div, reg1, ":a"),
        (val_div, reg2, ":a"),
        (val_mul, reg1, ":save_fpm"),
        (val_mul, reg2, ":save_fpm"),
        (convert_from_fixed_point, reg1),
        (convert_from_fixed_point, reg2),
      (try_end),
      (set_fixed_point_multiplier, ":save_fpm"),
    (try_end),

    (gt, reg0, 0), # There are no roots
  ]),
  # script_point_missile_position
  # Input:  <missile_pos>, <target_pos>, <speed_fixed_point>
  # Output: <missile_pos>
  ("point_missile_position", [
    (store_script_param, ":missile_pos", 1),
    (store_script_param, ":target_pos", 2),
    (store_script_param, ":speed", 3),

    (assign, ":save_fpm", 1),
    (convert_to_fixed_point, ":save_fpm"),
    (set_fixed_point_multiplier, 1000), # precise calculation
    (assign, ":g", 9807),
    (convert_to_fixed_point, ":speed"),
    (val_div, ":speed", ":save_fpm"),

    #remove current rotation
    (position_get_x, ":from_x", ":missile_pos"),
    (position_get_y, ":from_y", ":missile_pos"),
    (position_get_z, ":from_z", ":missile_pos"),
    (init_position, ":missile_pos"),
    (position_set_x, ":missile_pos", ":from_x"),
    (position_set_y, ":missile_pos", ":from_y"),
    (position_set_z, ":missile_pos", ":from_z"),
   
    #horizontal rotation - Yaw
    (position_get_x, ":change_in_x", ":target_pos"),
    (val_sub, ":change_in_x", ":from_x"),
    (position_get_y, ":change_in_y", ":target_pos"),
    (val_sub, ":change_in_y", ":from_y"),
   
    (try_begin),
      (this_or_next|neq, ":change_in_y", 0),
      (neq, ":change_in_x", 0),
      (store_atan2, ":theta", ":change_in_y", ":change_in_x"),
      (assign, ":ninety", 90),
      (convert_to_fixed_point, ":ninety"),
      (val_sub, ":theta", ":ninety"), #point Y axis at to position
      (position_rotate_z_floating, ":missile_pos", ":theta"),
    (try_end),

    #vertical rotation - Roll
    (get_distance_between_positions, ":distance_between", ":missile_pos", ":target_pos"),
    (try_begin),
      (gt, ":distance_between", 0),
      (position_get_z, ":z_distance", ":target_pos"),
      (position_get_z, ":z_missile", ":missile_pos"),
      (val_sub, ":z_distance", ":z_missile"),
      # Get plane distance
      (val_mul, ":change_in_x", ":change_in_x"),
      (convert_from_fixed_point, ":change_in_x"),
      (val_mul, ":change_in_y", ":change_in_y"),
      (convert_from_fixed_point, ":change_in_y"),
      (store_add, ":plane_distance", ":change_in_x", ":change_in_y"),
      (store_sqrt, ":plane_distance", ":plane_distance"),
      # A
      (store_mul, ":a", ":g", -1),
      (val_mul, ":a", ":plane_distance"),
      (convert_from_fixed_point, ":a"),
      (store_mul, ":divisor", ":speed", ":speed"),
      (convert_from_fixed_point, ":divisor"),
      (val_mul, ":divisor", 2),
      (convert_to_fixed_point, ":a"),
      (val_div, ":a", ":divisor"),
      # B
      (assign, ":b", 1),
      (convert_to_fixed_point, ":b"),
      # C
      (store_mul, ":c", ":z_distance", -1),
      (convert_to_fixed_point, ":c"),
      (val_div, ":c", ":plane_distance"),
      (val_add, ":c", ":a"),

      (try_begin),
        (call_script, "script_cf_quadratic_roots", ":a", ":b", ":c"),
        (try_begin),
          (eq, reg0, 1),
          (store_atan, ":theta", reg1),
        (else_try),
          (eq, reg0, 2),
          (store_atan, ":theta", reg1),
          (store_atan, ":theta2", reg2),
          (try_begin),
            (lt, ":theta2", ":theta"),
            (assign, ":theta", ":theta2"),
          (try_end),
        (try_end),
        (position_rotate_x_floating, ":missile_pos", ":theta"),
      (else_try),
        (gt, "$cheat_mode", 0),
        (display_message, "@Error: script_point_missile_position invalid roots"),
      (try_end),
    (try_end),

    (set_fixed_point_multiplier, ":save_fpm"),
  ]),
  ("game_get_skill_modifier_for_troop",
  [
    (store_script_param, ":var0", 1),
    (store_script_param, ":var1", 2),
    (assign, ":var2", 0),
    (try_begin),
      (eq, ":var1", "skl_wound_treatment"),
      (call_script, "script_get_troop_item_amount", ":var0", "itm_book_wound_treatment_reference"),
      (gt, reg0, 0),
      (val_add, ":var2", 1),
    (else_try),
      (eq, ":var1", "skl_trainer"),
      (call_script, "script_get_troop_item_amount", ":var0", "itm_book_training_reference"),
      (gt, reg0, 0),
      (val_add, ":var2", 1),
    (else_try),
      (eq, ":var1", "skl_surgery"),
      (call_script, "script_get_troop_item_amount", ":var0", "itm_book_surgery_reference"),
      (gt, reg0, 0),
      (val_add, ":var2", 1),
    (else_try),
      (eq, ":var1", "skl_riding"),
      (store_attribute_level, ":var3", ":var0", ca_agility),
      (call_script, "script_get_total_equipment_weight", ":var0"),
      (assign, ":var4", reg0),
      (val_sub, ":var4", ":var3"),
      (val_sub, ":var4", 10),
      (val_div, ":var4", 10),
      (store_sub, ":var2", 0, ":var4"),
      (val_min, ":var2", 0),
    (else_try),
      (eq, ":var1", "skl_athletics"),
      (store_attribute_level, ":var5", ":var0", ca_strength),
      (call_script, "script_get_total_equipment_weight", ":var0"),
      (assign, ":var4", reg0),
      (call_script, "script_get_total_shield_weight", ":var0"),
      (assign, ":var6", reg0),
      (val_add, ":var4", ":var6"),
      (val_sub, ":var4", ":var5"),
      (val_sub, ":var4", 10),
      (val_div, ":var4", 10),
      (store_sub, ":var2", 0, ":var4"),
      (val_min, ":var2", 0),
    (else_try),
      (eq, ":var1", "skl_power_draw"),
      (troop_is_hero, ":var0"),
      (store_attribute_level, ":var5", ":var0", ca_strength),
      (call_script, "script_get_total_equipment_weight", ":var0"),
      (assign, ":var4", reg0),
      (val_div, ":var5", 2),
      (val_sub, ":var4", ":var5"),
      (val_sub, ":var4", 10),
      (val_div, ":var4", 10),
      (call_script, "script_get_total_shield_weight", ":var0"),
      (assign, ":var6", reg0),
      (store_sub, ":var2", 0, ":var4"),
      (try_begin),
        (gt, ":var6", 3),
        (val_div, ":var6", 3),
        (store_sub, ":var2", 0, ":var6"),
      (end_try),
      (assign, ":var7", 0),
      (try_for_range, ":var8", 0, 8),
        (troop_get_inventory_slot, ":var9", ":var0", ":var8"),
        (ge, ":var9", 0),
        (item_get_type, ":var10", ":var9"),
        (try_begin),
          (eq, ":var10", 15),
          (item_get_weight, ":var11", ":var9"),
          (val_add, ":var7", ":var11"),
        (end_try),
      (end_try),
      (try_begin),
        (ge, ":var7", 500),
        (assign, ":var2", -3),
      (end_try),
      (val_min, ":var2", 0),
    (else_try),
      (eq, ":var1", "skl_horse_archery"),
      (store_attribute_level, ":var3", ":var0", ca_agility),
      (store_attribute_level, ":var5", ":var0", ca_strength),
      (call_script, "script_get_total_equipment_weight", ":var0"),
      (assign, ":var4", reg0),
      (val_mul, ":var4", 2),
      (val_sub, ":var4", 20),
      (val_sub, ":var4", ":var3"),
      (val_sub, ":var4", ":var5"),
      (val_div, ":var4", 10),
      (store_sub, ":var2", 0, ":var4"),
      (val_min, ":var2", 0),
    (end_try),
    (set_trigger_result, ":var2"),
  ]),
  ("get_total_equipment_weight",
  [
    (store_script_param_1, ":var0"),
    (set_fixed_point_multiplier, 1000),
    (assign, ":var1", 0),
    (try_for_range, ":var2", 0, 8),
      (troop_get_inventory_slot, ":var3", ":var0", ":var2"),
      (ge, ":var3", 0),
      (item_get_weight, ":var4", ":var3"),
      (val_add, ":var1", ":var4"),
    (end_try),
    (val_div, ":var1", 1000),
    (assign, reg0, ":var1"),
  ]),
  ("get_troop_total_equipment_weight",
  [
    (store_script_param_1, ":var0"),
    (assign, ":var1", 0),
    (set_fixed_point_multiplier, 1000),
    (troop_get_inventory_capacity, ":var2", ":var0"),
    (assign, ":var3", 0),
    (assign, ":var4", 0),
    (assign, ":var5", 0),
    (assign, ":var6", 0),
    (assign, ":var7", 0),
    (assign, ":var8", 0),
    (assign, ":var9", 0),
    (assign, ":var10", 0),
    (try_for_range, ":var11", 0, ":var2"),
      (troop_get_inventory_slot, ":var12", ":var0", ":var11"),
      (ge, ":var12", 0),
      (item_get_type, ":var13", ":var12"),
      (try_begin),
        (eq, ":var13", 13),
        (val_add, ":var3", 1),
        (item_get_weight, ":var14", ":var12"),
        (val_add, ":var4", ":var14"),
      (else_try),
        (eq, ":var13", 12),
        (val_add, ":var5", 1),
        (item_get_weight, ":var15", ":var12"),
        (val_add, ":var6", ":var15"),
      (else_try),
        (eq, ":var13", 14),
        (val_add, ":var7", 1),
        (item_get_weight, ":var16", ":var12"),
        (val_add, ":var8", ":var16"),
      (else_try),
        (eq, ":var13", 15),
        (val_add, ":var9", 1),
        (item_get_weight, ":var17", ":var12"),
        (val_add, ":var10", ":var17"),
      (end_try),
    (end_try),
    (val_max, ":var3", 1),
    (val_div, ":var4", ":var3"),
    (val_max, ":var5", 1),
    (val_div, ":var6", ":var5"),
    (val_max, ":var7", 1),
    (val_div, ":var8", ":var7"),
    (val_max, ":var9", 1),
    (val_div, ":var10", ":var9"),
    (val_add, ":var1", ":var4"),
    (val_add, ":var1", ":var6"),
    (val_add, ":var1", ":var8"),
    (val_add, ":var1", ":var10"),
    (val_div, ":var1", 1000),
    (assign, reg0, ":var1"),
  ]),
  ("get_total_shield_weight",
  [
    (store_script_param_1, ":var0"),
    (set_fixed_point_multiplier, 1000),
    (assign, ":var1", 0),
    (try_for_range, ":var2", 0, 8),
      (troop_get_inventory_slot, ":var3", ":var0", ":var2"),
      (ge, ":var3", 0),
      (item_get_type, ":var4", ":var3"),
      (eq, ":var4", 7),
      (item_get_weight, ":var5", ":var3"),
      (val_add, ":var1", ":var5"),
    (end_try),
    (val_div, ":var1", 1000),
    (assign, reg0, ":var1"),
  ]),
#Town Merchant Interactions
  ("start_town_conversation",
  [
    (store_script_param, ":troop_slot_no", 1),
    (store_script_param, ":entry_no", 2),

    (try_begin),
      (eq, ":troop_slot_no", slot_town_merchant),
      (assign, ":scene_slot_no", slot_town_store),
    (else_try),
      (eq, ":troop_slot_no", slot_town_tavernkeeper),
      (assign, ":scene_slot_no", slot_town_tavern),
    (else_try),
      (assign, ":scene_slot_no", slot_town_center),
    (try_end),

    (party_get_slot, ":conversation_scene", "$current_town", ":scene_slot_no"),
    (modify_visitors_at_site, ":conversation_scene"),
    (reset_visitors),
    (set_visitor, 0, "trp_player"),

    (try_begin),
      (eq, "$sneaked_into_town", 1),
      (mission_tpl_entry_set_override_flags, "mt_conversation_encounter", 0, af_override_all),
      (mission_tpl_entry_add_override_item, "mt_conversation_encounter", 0, "itm_pilgrim_disguise"),
    (else_try),
      (mission_tpl_entry_set_override_flags, "mt_conversation_encounter", 0, af_override_horse),
      (mission_tpl_entry_clear_override_items, "mt_conversation_encounter", 0),
    (try_end),
    (party_get_slot, ":conversation_troop", "$current_town", ":troop_slot_no"),
    (set_visitor, ":entry_no", ":conversation_troop"),
    (set_jump_mission,"mt_conversation_encounter"),
    (jump_to_scene, ":conversation_scene"),
    (change_screen_map_conversation, ":conversation_troop"),
  ]),
  #MORDACHAI - update whether the specified prisoner would like to join the player's party
  # script_determine_prisoner_agreed
  # Input: arg1 = troop, arg2 = troop faction relation
  # Output: slot_prisoner_agreed is set to 1 if they agreed, or 0 if not
  #         reg0 = agreed or not
  ("determine_prisoner_agreed",
    [
      (store_script_param, ":troop", 1),
      (store_script_param, ":relation", 2),

      # upper bound = Persuasion*3 + Charisma + Leadership*3 + Honor/2 + Renown/100
      (store_attribute_level, ":charisma", "trp_player", ca_charisma),
      (store_skill_level, ":persuasion", "skl_persuasion", "trp_player"),
      (store_skill_level, ":leadership", "skl_leadership", "trp_player"),
      (val_mul, ":persuasion", 3),
      (val_mul, ":leadership", 3),
      (store_div, ":half_honor", "$player_honor", 2),
      (troop_get_slot, ":renown_factor", slot_troop_renown),
      (val_div, ":renown_factor", 100),
      (assign, ":upper_bound", ":persuasion"),
      (val_add, ":upper_bound", ":leadership"),
      (val_add, ":upper_bound", ":charisma"),
      (val_add, ":upper_bound", ":half_honor"),
      (val_add, ":upper_bound", ":renown_factor"),
      (val_min, ":relation", ":upper_bound"),

      # determine their reaction (relation...upper_bound)
      (store_random_in_range, ":reaction", ":relation", ":upper_bound"),
      (assign, reg1, ":reaction"),
      (assign, reg2, ":relation"),
      (assign, reg3, ":upper_bound"),
      #(display_message, "@Prisoner Agrees Check: rolled a {reg1} out of a possible {reg2}-{reg3}"),#diagnostic only

      # record whether they agree or not
      (try_begin),
        (ge, ":reaction", 0),
        (troop_set_slot, ":troop", slot_prisoner_agreed, 1),
      (else_try),
        (troop_set_slot, ":troop", slot_prisoner_agreed, 0),
      (try_end),

      # return the results
      (troop_get_slot, reg0, ":troop", slot_prisoner_agreed),
      #(display_message, "@Prisoner Agrees Check: slot_prisoner_agreed = {reg0?yes:no}"),#diagnostic only
    ]
  ),
  ("get_item_value_with_imod",
    [# returns the sell price based on the item's money value and its imod
      (store_script_param, ":item", 1),
      (store_script_param, ":imod", 2),

      (store_item_value, ":score", ":item"),
      (try_begin),
        (eq, ":imod", imod_plain),
        (assign, ":imod_multiplier", 100),
      (else_try),
        (eq, ":imod", imod_cracked),
        (assign, ":imod_multiplier", 50),
      (else_try),
        (eq, ":imod", imod_rusty),
        (assign, ":imod_multiplier", 55),
      (else_try),
        (eq, ":imod", imod_bent),
        (assign, ":imod_multiplier", 65),
      (else_try),
        (eq, ":imod", imod_chipped),
        (assign, ":imod_multiplier", 72),
      (else_try),
        (eq, ":imod", imod_battered),
        (assign, ":imod_multiplier", 75),
      (else_try),
        (eq, ":imod", imod_poor),
        (assign, ":imod_multiplier", 80),
      (else_try),
        (eq, ":imod", imod_crude),
        (assign, ":imod_multiplier", 83),
      (else_try),
        (eq, ":imod", imod_old),
        (assign, ":imod_multiplier", 86),
      (else_try),
        (eq, ":imod", imod_cheap),
        (assign, ":imod_multiplier", 90),
      (else_try),
        (eq, ":imod", imod_fine),
        (assign, ":imod_multiplier", 190),
      (else_try),
        (eq, ":imod", imod_well_made),
        (assign, ":imod_multiplier", 250),
      (else_try),
        (eq, ":imod", imod_sharp),
        (assign, ":imod_multiplier", 160),
      (else_try),
        (eq, ":imod", imod_balanced),
        (assign, ":imod_multiplier", 350),
      (else_try),
        (eq, ":imod", imod_tempered),
        (assign, ":imod_multiplier", 670),
      (else_try),
        (eq, ":imod", imod_deadly),
        (assign, ":imod_multiplier", 850),
      (else_try),
        (eq, ":imod", imod_exquisite),
        (assign, ":imod_multiplier", 1450),
      (else_try),
        (eq, ":imod", imod_masterwork),
        (assign, ":imod_multiplier", 1750),
      (else_try),
        (eq, ":imod", imod_heavy),
        (assign, ":imod_multiplier", 190),
      (else_try),
        (eq, ":imod", imod_strong),
        (assign, ":imod_multiplier", 490),
      (else_try),
        (eq, ":imod", imod_powerful),
        (assign, ":imod_multiplier", 320),
      (else_try),
        (eq, ":imod", imod_tattered),
        (assign, ":imod_multiplier", 50),
      (else_try),
        (eq, ":imod", imod_ragged),
        (assign, ":imod_multiplier", 70),
      (else_try),
        (eq, ":imod", imod_rough),
        (assign, ":imod_multiplier", 60),
      (else_try),
        (eq, ":imod", imod_sturdy),
        (assign, ":imod_multiplier", 170),
      (else_try),
        (eq, ":imod", imod_thick),
        (assign, ":imod_multiplier", 260),
      (else_try),
        (eq, ":imod", imod_hardened),
        (assign, ":imod_multiplier", 390),
      (else_try),
        (eq, ":imod", imod_reinforced),
        (assign, ":imod_multiplier", 650),
      (else_try),
        (eq, ":imod", imod_superb),
        (assign, ":imod_multiplier", 250),
      (else_try),
        (eq, ":imod", imod_lordly),
        (assign, ":imod_multiplier", 1150),
      (else_try),
        (eq, ":imod", imod_lame),
        (assign, ":imod_multiplier", 40),
      (else_try),
        (eq, ":imod", imod_swaybacked),
        (assign, ":imod_multiplier", 60),
      (else_try),
        (eq, ":imod", imod_stubborn),
        (assign, ":imod_multiplier", 90),
      (else_try),
        (eq, ":imod", imod_timid),
        (assign, ":imod_multiplier", 180),
      (else_try),
        (eq, ":imod", imod_meek),
        (assign, ":imod_multiplier", 180),
      (else_try),
        (eq, ":imod", imod_spirited),
        (assign, ":imod_multiplier", 650),
      (else_try),
        (eq, ":imod", imod_champion),
        (assign, ":imod_multiplier", 1450),
      (else_try),
        (eq, ":imod", imod_fresh),
        (assign, ":imod_multiplier", 100),
      (else_try),
        (eq, ":imod", imod_day_old),
        (assign, ":imod_multiplier", 100),
      (else_try),
        (eq, ":imod", imod_two_day_old),
        (assign, ":imod_multiplier", 90),
      (else_try),
        (eq, ":imod", imod_smelling),
        (assign, ":imod_multiplier", 40),
      (else_try),
        (eq, ":imod", imod_rotten),
        (assign, ":imod_multiplier", 5),
      (else_try),
        (eq, ":imod", imod_large_bag),
        (assign, ":imod_multiplier", 190),
      (try_end),
      (val_mul, ":score", ":imod_multiplier"),
      (assign, reg0, ":score"),
    ]),
]
