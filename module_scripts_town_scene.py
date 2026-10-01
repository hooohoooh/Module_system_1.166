# -*- coding: utf-8 -*-
# module_scripts_town_scene.py -- auto split from module_scripts.py (feature: 城镇场景/NPC 行走者)
# entries: 19 (order preserved within this file)
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


scripts_town_scene = [

  # script_cf_turn_windmill_fans
  # Input: arg1 = instance_no (none = 0)
  # Output: none
  ("cf_turn_windmill_fans",
    [(store_script_param_1, ":instance_no"),
      (scene_prop_get_instance, ":windmill_fan_object", "spr_windmill_fan_turning", ":instance_no"),
      (ge, ":windmill_fan_object", 0),
      (prop_instance_get_position, pos1, ":windmill_fan_object"),
      (position_rotate_y, pos1, 10),
      (prop_instance_animate_to_position, ":windmill_fan_object", pos1, 100),
      (val_add, ":instance_no", 1),
      (call_script, "script_cf_turn_windmill_fans", ":instance_no"),
  ]),
  # script_center_ambiance_sounds
  # Input: none
  # Output: none
  # to be called every two seconds
  ("center_ambiance_sounds",
    [
        (assign, ":sound_1", -1),
        (assign, ":sound_2", -1),
        (assign, ":sound_3", -1),
        (assign, ":sound_4", -1),
        (assign, ":sound_5", -1),
        (try_begin),
          (party_slot_eq, "$g_encountered_party", slot_party_type, spt_village),
          (try_begin),
            (neg|is_currently_night),
            (assign, ":sound_3", "snd_distant_dog_bark"),
            (assign, ":sound_3", "snd_distant_chicken"),
          (else_try),
            (assign, ":sound_1", "snd_distant_dog_bark"),
            (assign, ":sound_2", "snd_distant_owl"),
          (try_end),
        (else_try),
          (party_slot_eq, "$g_encountered_party", slot_party_type, spt_town),
          (try_begin),
            (neg|is_currently_night),
            (assign, ":sound_1", "snd_distant_carpenter"),
            (assign, ":sound_2", "snd_distant_blacksmith"),
            (assign, ":sound_3", "snd_distant_dog_bark"),
          (else_try),
            (assign, ":sound_1", "snd_distant_dog_bark"),
          (try_end),
        (try_end),
        (try_begin),
          (store_random_in_range, ":r", 0, 7),
          (try_begin),
            (eq, ":r", 1),
            (ge, ":sound_1", 0),
            (play_sound, ":sound_1"),
          (else_try),
            (eq, ":r", 2),
            (ge, ":sound_2", 0),
            (play_sound, ":sound_2"),
          (else_try),
            (eq, ":r", 3),
            (ge, ":sound_3", 0),
            (play_sound, ":sound_3"),
          (else_try),
            (eq, ":r", 4),
            (ge, ":sound_4", 0),
            (play_sound, ":sound_4"),
          (else_try),
            (eq, ":r", 5),
            (ge, ":sound_5", 0),
            (play_sound, ":sound_5"),
          (try_end),
        (try_end),
  ]),
  # script_center_set_walker_to_type
  # Input: arg1 = center_no, arg2 = walker_no, arg3 = walker_type, 
  # Output: none
  ("center_set_walker_to_type",
   [
       (store_script_param, ":center_no", 1),
       (store_script_param, ":walker_no", 2),
       (store_script_param, ":walker_type", 3),
       (store_add, ":type_slot", slot_center_walker_0_type, ":walker_no"),
       (party_set_slot, ":center_no", ":type_slot", ":walker_type"),
       (party_get_slot, ":center_faction", ":center_no", slot_center_original_faction),
       (faction_get_slot, ":center_culture", ":center_faction", slot_faction_culture),
       (store_random_in_range, ":walker_troop_slot", 0, 2),
       (try_begin),
         (party_slot_eq, ":center_no", slot_party_type, spt_village),
         (val_add, ":walker_troop_slot", slot_faction_village_walker_male_troop),
       (else_try),
         (val_add, ":walker_troop_slot", slot_faction_town_walker_male_troop),
       (try_end),
       (try_begin),
         (eq,":walker_type", walkert_spy),
         (assign,":original_walker_slot",":walker_troop_slot"),
         (val_add,":walker_troop_slot",4), # select spy troop id slot
       (try_end),
       (faction_get_slot, ":walker_troop_id", ":center_culture", ":walker_troop_slot"),
       (try_begin),
         (eq,":walker_type", walkert_spy),
         (faction_get_slot, ":original_walker", ":center_culture", ":original_walker_slot"),
         # restore spy inventory
         (try_for_range,":item_no","itm_horse_meat","itm_wooden_stick"),
            (store_item_kind_count,":num_items",":item_no",":original_walker"),
            (ge,":num_items",1),
            (store_item_kind_count,":num_items",":item_no",":walker_troop_id"),
            (lt,":num_items",1),
            (troop_add_items,":walker_troop_id",":item_no",1),
         (try_end),
         # determine spy recognition item
         (store_random_in_range,":spy_item_type",itp_type_head_armor,itp_type_hand_armor),
         (assign,":num",0),
         (try_for_range,":item_no","itm_horse_meat","itm_wooden_stick"),
            (store_item_kind_count,":num_items",":item_no",":walker_troop_id"),
            (ge,":num_items",1),
            (item_get_type, ":itp", ":item_no"),
            (eq,":itp",":spy_item_type"),
            (val_add,":num",1),
            (troop_remove_items,":walker_troop_id",":item_no",":num_items"),
         (try_end),
         (store_random_in_range,":random_item",0,":num"),
         (assign,":num",-1),
         (try_for_range,":item_no","itm_horse_meat","itm_wooden_stick"),
            (store_item_kind_count,":num_items",":item_no",":original_walker"),
            (ge,":num_items",1),
            (item_get_type, ":itp", ":item_no"),
            (eq,":itp",":spy_item_type"),
            (val_add,":num",1),
            (eq,":num",":random_item"),
            (troop_add_items,":walker_troop_id",":item_no",1),
            (assign,":spy_item",":item_no"),
         (try_end),
         (assign,"$spy_item_worn",":spy_item"),
         (assign,"$spy_quest_troop",":walker_troop_id"),
         (troop_equip_items,":walker_troop_id"),
       (try_end),
       (store_add, ":troop_slot", slot_center_walker_0_troop, ":walker_no"),
       (party_set_slot, ":center_no", ":troop_slot", ":walker_troop_id"),
       (store_random_in_range, ":walker_dna", 0, 1000000),
       (store_add, ":dna_slot", slot_center_walker_0_dna, ":walker_no"),
       (party_set_slot, ":center_no", ":dna_slot", ":walker_dna"),
     ]),
  # script_cf_center_get_free_walker
  # Input: arg1 = center_no
  # Output: reg0 = walker no (can fail)
  ("cf_center_get_free_walker",
   [
       (store_script_param, ":center_no", 1),
       (assign, ":num_free_walkers", 0),
       (try_for_range, ":walker_no", 0, num_town_walkers),
         (store_add, ":type_slot", slot_center_walker_0_type, ":walker_no"),
         (party_slot_eq, ":center_no", ":type_slot", walkert_default),
         (val_add, ":num_free_walkers", 1),
       (try_end),
       (gt, ":num_free_walkers", 0),
       (assign, reg0, -1),
       (store_random_in_range, ":random_rank", 0, ":num_free_walkers"),
       (try_for_range, ":walker_no", 0, num_town_walkers),
         (store_add, ":type_slot", slot_center_walker_0_type, ":walker_no"),
         (party_slot_eq, ":center_no", ":type_slot", walkert_default),
         (val_sub, ":num_free_walkers", 1),
         (eq, ":num_free_walkers", ":random_rank"),
         (assign, reg0, ":walker_no"),
       (try_end),
     ]),
  # script_center_remove_walker_type_from_walkers
  # Input: arg1 = center_no, arg2 = walker_type, 
  # Output: reg0 = 1 if comment found, 0 otherwise; s61 will contain comment string if found
  ("center_remove_walker_type_from_walkers",
   [
       (store_script_param, ":center_no", 1),
       (store_script_param, ":walker_type", 2),
       (try_for_range, ":walker_no", 0, num_town_walkers),
         (store_add, ":type_slot", slot_center_walker_0_type, ":walker_no"),
         (party_slot_eq, ":center_no", ":type_slot", ":walker_type"),
         (call_script, "script_center_set_walker_to_type", ":center_no", ":walker_no", walkert_default),
       (try_end),
     ]),
  # script_init_town_walkers
  # Input: none
  # Output: none
  ("init_town_walkers",
  [
    (try_begin),
      (eq, "$town_nighttime", 0),
      (try_for_range, ":walker_no", 0, num_town_walkers),
        (store_add, ":troop_slot", slot_center_walker_0_troop, ":walker_no"),
        (party_get_slot, ":walker_troop_id", "$current_town", ":troop_slot"),
        (gt, ":walker_troop_id", 0),
        (store_add, ":entry_no", town_walker_entries_start, ":walker_no"),
        #gekokujo 3.1 kyoto has up to three times as many town walkers start
        #(set_visitor, ":entry_no", ":walker_troop_id"),
        (try_begin),
          (eq, "$current_town", "p_town_4",),
          (store_random_in_range, ":random", 1, 4), #1 to 3
          (set_visitors, ":entry_no", ":walker_troop_id", ":random"),
        (else_try),
          (set_visitor, ":entry_no", ":walker_troop_id"),
        #gekokujo 3.1 kyoto has up to three times as many town walkers end
      (try_end),  
    (try_end),  
  ]),
  # script_cf_enter_center_location_bandit_check
  # Input: none
  # Output: none
  ("cf_enter_center_location_bandit_check",
    [
      (neq, "$town_nighttime", 0),
      (party_slot_ge, "$current_town", slot_center_has_bandits, 1),
      (eq, "$g_defending_against_siege", 0),#Skip if the center is under siege (because of resting)
      (eq, "$sneaked_into_town", 0),#Skip if sneaked
      (try_begin),
        (party_slot_eq, "$current_town", slot_party_type, spt_village),
        (party_get_slot, ":cur_scene", "$current_town", slot_castle_exterior),
      (else_try),
        (party_get_slot, ":cur_scene", "$current_town", slot_town_center),
      (try_end),
      (modify_visitors_at_site, ":cur_scene"),
      (reset_visitors),
      (party_get_slot, ":bandit_troop", "$current_town", slot_center_has_bandits),
      (store_character_level, ":level", "trp_player"),

      (set_jump_mission, "mt_bandits_at_night"),
      (try_begin),
        (party_slot_eq, "$current_town", slot_party_type, spt_village),
        (assign, ":spawn_amount", 2),
        (store_div, ":level_fac",  ":level", 10),
        (val_add, ":spawn_amount", ":level_fac"),
        (try_for_range, ":unused", 0, 3),
          (gt, ":level", 10),
          (store_random_in_range, ":random_no", 0, 100),
          (lt, ":random_no", ":level"),
          (val_add, ":spawn_amount", 1),
        (try_end),
        (set_visitors, 4, ":bandit_troop", ":spawn_amount"),
        (assign, "$num_center_bandits", ":spawn_amount"),
        (set_jump_entry, 2),
      (else_try),
        (assign, ":spawn_amount", 1),
        (assign, "$num_center_bandits", 0),
        (try_begin),
          (gt, ":level", 15),
          (store_random_in_range, ":random_no", 0, 100),
          (lt, ":random_no", ":level"),
          (assign, ":spawn_amount", 2),
        (try_end),
        (val_add, "$num_center_bandits",  ":spawn_amount"),
        (set_visitors, 11, ":bandit_troop", ":spawn_amount"),
        (assign, ":spawn_amount", 1),
        (try_begin),
          (gt, ":level", 20),
          (store_random_in_range, ":random_no", 0, 100),
          (lt, ":random_no", ":level"),
          (assign, ":spawn_amount", 2),
        (try_end),
        (set_visitors, 27, ":bandit_troop", ":spawn_amount"),
        (val_add, "$num_center_bandits",  ":spawn_amount"),
        (try_begin),
          (gt, ":level", 9),
          (assign, ":spawn_amount", 1),
          (try_begin),
            (gt, ":level", 25),
            (store_random_in_range, ":random_no", 0, 100),
            (lt, ":random_no", ":level"),
            (assign, ":spawn_amount", 2),
          (try_end),
          (set_visitors, 28, ":bandit_troop", ":spawn_amount"),
          (val_add, "$num_center_bandits",  ":spawn_amount"),
        (try_end),
        (assign, "$town_entered", 1),
        (assign, "$all_doors_locked", 1),
      (try_end),

      (display_message, "@You have run into a trap!", 0xFFFF2222),
      (display_message, "@You are attacked by a group of bandits!", 0xFFFF2222),

      (jump_to_scene, ":cur_scene"),
      (change_screen_mission),
      ]),
  # script_init_town_agent
  # Input: none
  # Output: none
  ("init_town_agent",
    [
      (store_script_param, ":agent_no", 1),
      (agent_get_troop_id, ":troop_no", ":agent_no"),
      (set_fixed_point_multiplier, 100),
      (assign, ":stand_animation", -1),
      (try_begin),
        (this_or_next|is_between, ":troop_no", armor_merchants_begin, armor_merchants_end),
        (is_between, ":troop_no", weapon_merchants_begin, weapon_merchants_end),
        (try_begin),
          (troop_get_type, ":cur_troop_gender", ":troop_no"),
          (eq, ":cur_troop_gender", 0),
          (agent_set_animation, ":agent_no", "anim_stand_townguard"),
        (else_try),
          (agent_set_animation, ":agent_no", "anim_stand_townguard"),
        (end_try),
      (else_try),
        (is_between, ":troop_no", kingdom_ladies_begin, kingdom_ladies_end),
        (assign, ":stand_animation", "anim_stand_lady"),
      (else_try),
        (is_between, ":troop_no", active_npcs_begin, active_npcs_end),
        (assign, ":stand_animation", "anim_stand_lord"),
      (else_try),
        (is_between, ":troop_no", soldiers_begin, soldiers_end),
        (assign, ":stand_animation", "anim_stand_townguard"),
      (try_end),
      (try_begin),
        (ge, ":stand_animation", 0),
        (agent_set_stand_animation, ":agent_no", ":stand_animation"),
        (agent_set_animation, ":agent_no", ":stand_animation"),
        (store_random_in_range, ":random_no", 0, 100),
        (agent_set_animation_progress, ":agent_no", ":random_no"),
      (try_end),
      ]),
  # script_init_town_walker_agents
  # Input: none
  # Output: none
  ("init_town_walker_agents",
    [(assign, ":num_walkers", 0),
     (try_for_agents, ":cur_agent"),
       (agent_get_troop_id, ":cur_troop", ":cur_agent"),
       (is_between, ":cur_troop", walkers_begin, walkers_end),
       (val_add, ":num_walkers", 1),
       (agent_get_position, pos1, ":cur_agent"),
       (try_for_range, ":i_e_p", 9, 40),#Entry points
         (entry_point_get_position, pos2, ":i_e_p"),
         (get_distance_between_positions, ":distance", pos1, pos2),
         (lt, ":distance", 200),
         (agent_set_slot, ":cur_agent", 0, ":i_e_p"),
       (try_end),
       (call_script, "script_set_town_walker_destination", ":cur_agent"),
     (try_end),
  ]),
  # script_agent_get_town_walker_details
  # This script assumes this is one of town walkers. 
  # Input: agent_id
  # Output: reg0: town_walker_type, reg1: town_walker_dna
  ("agent_get_town_walker_details",
    [(store_script_param, ":agent_no", 1),
     (agent_get_entry_no, ":entry_no", ":agent_no"),
     (store_sub, ":walker_no", ":entry_no", town_walker_entries_start),

     (store_add, ":type_slot", slot_center_walker_0_type, ":walker_no"),
     (party_get_slot, ":walker_type", "$current_town", ":type_slot"),
     (store_add, ":dna_slot", slot_center_walker_0_dna,  ":walker_no"),
     (party_get_slot, ":walker_dna", "$current_town", ":dna_slot"),
     (assign, reg0, ":walker_type"),
     (assign, reg1, ":walker_dna"),
     (assign, reg2, ":walker_no"),
  ]),
  ##diplomacy start+
  ##WARNING: this will also clobber s0 now
  ##diplomacy end+
  ("town_walker_occupation_string_to_s14",
    [	
	(store_script_param, ":agent_no", 1),
	
	#Cairo, approx 1799:
	#adult males = 114,000
	#military, 10,400
	#civil, including religious 5,000
	#commerce 3,500
	#merchants 4,500
	#coffee shops, 1,500 (maybe broaden to inns and taverns)
	#artisans 21,800
	#workmen 4,300
	#itinerants 8,600
	#servants (inc water carriers) 26,400
	(assign, ":check_for_good_price", 0),
    ##diplomacy start+ escalate "sir/madame" to "my lord/lady" or "your highness" if appropriate
    (call_script, "script_dplmc_print_subordinate_says_sir_madame_to_s0"),
    ##diplomacy end+
	(str_store_string, s14, "str_i_take_what_work_i_can_sirmadame_i_carry_water_or_help_the_merchants_with_their_loads_or_help_build_things_if_theres_things_to_be_built"),
	
	(call_script, "script_agent_get_town_walker_details", ":agent_no"),	
	(assign, ":type", reg0),
	(assign, ":walker_dna", reg1),
	
	(assign, ":item", -1),
	(assign, ":total_item_production", 0),
	(try_for_range, ":trade_good", trade_goods_begin, trade_goods_end),
		(call_script, "script_center_get_production", "$g_encountered_party", ":trade_good"),
		(val_add, ":total_item_production", reg0),
	(try_end),

	(val_max, ":total_item_production", 1),
	
	(store_mod, ":semi_random_number", ":walker_dna", ":total_item_production"),
	
	
	(try_begin),
		(eq, "$cheat_mode", 1),
		(assign, reg4, ":walker_dna"),
		(assign, reg5, ":total_item_production"),
		(assign, reg7, ":semi_random_number"), 
		(display_message, "str_dna_reg4_total_production_reg5_modula_reg7"),
	(try_end),
	
	(try_for_range, ":trade_good", trade_goods_begin, trade_goods_end),
		(gt, ":semi_random_number", -1),
		(call_script, "script_center_get_production", "$g_encountered_party", ":trade_good"),
		(val_sub, ":semi_random_number", reg0),
		(lt, ":semi_random_number", 0),
                (try_begin),
                  (eq, "$cheat_mode", 1),
		  (str_store_item_name, s9, ":trade_good"),
		  (display_message, "str_agent_produces_s9"),
                (try_end),
		(assign, ":item", ":trade_good"),
	(try_end),	
	
	
	(try_begin),
		(eq, ":type", walkert_needs_money),
		(is_between, "$g_encountered_party", towns_begin, towns_end),
		(str_store_string, s14, "str_im_not_doing_anything_sirmadame_theres_no_work_to_be_had_around_here_these_days"),
	(else_try),	
		(eq, ":type", walkert_needs_money),
		(str_store_string, s14, "str_im_not_doing_anything_sirmadame_i_have_no_land_of_my_own_and_theres_no_work_to_be_had_around_here_these_days"),
	(else_try),	
		(eq, ":type", walkert_needs_money_helped),
		(str_store_string, s14, "str_why_im_still_living_off_of_your_kindness_and_goodness_sirmadame_hopefully_there_will_be_work_shortly"),
	(else_try),
		(eq, ":item", "itm_grain"),
		(is_between, "$g_encountered_party", towns_begin, towns_end),
		(str_store_string, s14, "str_i_work_in_the_fields_just_outside_the_walls_where_they_grow_grain_we_dont_quite_grow_enough_to_meet_our_needs_though_and_have_to_import_grain_from_the_surrounding_countryside"),
		(assign, ":check_for_good_price", 1),
		
	(else_try),
		(eq, ":item", "itm_grain"),
		(str_store_string, s14, "str_i_work_mostly_in_the_fields_growing_grain_in_the_town_they_grind_it_to_make_bread_or_ale_and_we_can_also_boil_it_as_a_porridge"),
		(assign, ":check_for_good_price", 1),
		
	(else_try),	
		(eq, ":item", "itm_ale"),
		(str_store_string, s14, "str_i_work_in_the_breweries_making_ale_the_poor_folk_drink_a_lot_of_it_as_its_cheaper_than_wine_we_make_it_with_grain_brought_in_from_the_countryside"),
		(assign, ":check_for_good_price", 1),
		
	(else_try),	
		(eq, ":item", "itm_bread"),
		(str_store_string, s14, "str_i_work_in_a_mill_grinding_flour_to_make_bread_bread_is_cheap_keeps_well_and_fills_the_stomach"),
		(assign, ":check_for_good_price", 1),
		
	(else_try),	
		(eq, ":item", "itm_dried_meat"),
		(str_store_string, s14, "str_i_tend_cattle_we_dry_and_salt_meat_to_preserve_it_and_make_cheese_from_the_milk"),
		(assign, ":check_for_good_price", 1),
		
	(else_try),	
		(eq, ":item", "itm_cheese"),
		(str_store_string, s14, "str_i_tend_cattle_we_dry_and_salt_meat_to_preserve_it_and_make_cheese_from_the_milk_so_it_doesnt_spoil"),
		(assign, ":check_for_good_price", 1),
		
	(else_try),	
		(eq, ":item", "itm_butter"),
		(str_store_string, s14, "str_i_tend_cattle_we_dry_and_salt_meat_to_preserve_it_and_make_cheese_from_the_milk_so_it_doesnt_spoil"),
		(assign, ":check_for_good_price", 1),
		
	(else_try),	
		(eq, ":item", "itm_wool"),
		(str_store_string, s14, "str_i_tend_sheep_we_send_the_wool_to_the_cities_to_be_woven_into_cloth_and_make_mutton_sausage_when_we_cull_the_herds"),
		(assign, ":check_for_good_price", 1),
		
	(else_try),	
		(eq, ":item", "itm_sausages"),
		(str_store_string, s14, "str_i_tend_sheep_we_send_the_wool_to_the_cities_to_be_woven_into_cloth_and_make_mutton_sausage_when_we_cull_the_herds"),
		(assign, ":check_for_good_price", 1),
		
	(else_try),	
		(eq, ":item", "itm_wool_cloth"),
		(str_store_string, s14, "str_i_work_at_a_loom_spinning_cloth_from_wool_wool_is_some_of_the_cheapest_cloth_you_can_buy_but_it_will_still_keep_you_warm"),
		(assign, ":check_for_good_price", 1),
		
	(else_try),	
		(eq, ":item", "itm_smoked_fish"),
		(str_store_string, s14, "str_i_crew_a_fishing_boat_we_salt_and_smoke_the_flesh_to_sell_it_far_inland"),
		(assign, ":check_for_good_price", 1),
		
	(else_try),	
		(eq, ":item", "itm_salt"),
		(str_store_string, s14, "str_i_sift_salt_from_a_nearby_flat_they_need_salt_everywhere_to_preserve_meat_and_fish"),
		(assign, ":check_for_good_price", 1),
		
	(else_try),	
		(eq, ":item", "itm_iron"),
		(str_store_string, s14, "str_i_mine_iron_from_a_vein_in_a_nearby_cliffside_they_use_it_to_make_tools_arms_and_other_goods"),
		(assign, ":check_for_good_price", 1),
		
	(else_try),	
		(eq, ":item", "itm_pottery"),
		(str_store_string, s14, "str_i_make_pottery_which_people_use_to_store_grain_and_carry_water"),
		(assign, ":check_for_good_price", 1),
		
	(else_try),	
		(eq, ":item", "itm_tools"),
		(str_store_string, s14, "str_trade_explanation_tools"),
		(assign, ":check_for_good_price", 1),
		
	(else_try),	
		(eq, ":item", "itm_oil"),
		(str_store_string, s14, "str_trade_explanation_oil"),
		(assign, ":check_for_good_price", 1),
		
	(else_try),	
		(eq, ":item", "itm_linen"),
		(str_store_string, s14, "str_trade_explanation_linen"),
		(assign, ":check_for_good_price", 1),
		
	(else_try),	
		(eq, ":item", "itm_velvet"),
		(str_store_string, s14, "str_trade_explanation_velvet"),
		(assign, ":check_for_good_price", 1),
		
	(else_try),	
		(eq, ":item", "itm_spice"),
		(str_store_string, s14, "str_trade_explanation_spice"),
		(assign, ":check_for_good_price", 1),
		
	(else_try),	
		(eq, ":item", "itm_apples"),
		(str_store_string, s14, "str_trade_explanation_apples"),
		(assign, ":check_for_good_price", 1),
		
	(try_end),
	
	
	(try_begin),
		(eq, ":check_for_good_price", 1),
	
		(assign, ":trade_destination", -1),
		(store_skill_level, ":trade_skill", "skl_trade", "trp_player"),
	
		(try_begin),
			(is_between, "$g_encountered_party", villages_begin, villages_end),
			(party_get_slot, ":trade_town", "$g_encountered_party", slot_village_market_town),
		(else_try),	
			(assign, ":trade_town", "$g_encountered_party"),
		(try_end),
		
		(store_sub, ":item_to_price_slot", slot_town_trade_good_prices_begin, trade_goods_begin),
		(store_add, ":cur_good_price_slot", ":item", ":item_to_price_slot"),
		(party_get_slot, ":score_to_beat", ":trade_town", ":cur_good_price_slot"),
		(val_add, ":score_to_beat", 400),
		(store_mul, ":deduction_for_trade_skill", ":trade_skill", 35),
		(try_begin),
			(is_between, "$g_encountered_party", villages_begin, villages_end),
			(val_add, ":score_to_beat", 200),
		(try_end),
		(val_sub, ":score_to_beat", ":deduction_for_trade_skill"),
		
		(try_for_range, ":trade_route_slot", slot_town_trade_routes_begin, slot_town_trade_routes_end),
			(party_get_slot, ":other_town", ":trade_town", ":trade_route_slot"),
			(party_get_slot, ":price_in_other_town", ":other_town", ":cur_good_price_slot"),
			
			
			(try_begin),
				(eq, "$cheat_mode", 1),
				(assign, reg4, ":price_in_other_town"),
				(assign, reg5, ":score_to_beat"),
				(str_store_party_name, s10, ":other_town"),
				(display_message, "str_s10_has_reg4_needs_reg5"),
			(try_end),
			
			(gt, ":price_in_other_town", ":score_to_beat"),
		
			(assign, ":trade_destination", ":other_town"),
			(assign, ":score_to_beat", ":price_in_other_town"),
		(try_end),
		
		(is_between, ":trade_destination", centers_begin, centers_end),
		
		(str_store_party_name, s15, ":trade_destination"),
		(str_store_string, s14, "str_s14_i_hear_that_you_can_find_a_good_price_for_it_in_s15"),
		
		#Reasons -- raw material
		#Reason -- road cut
		#Reason -- villages looted
		
	(try_end),
	
	
	]),
  # script_tick_town_walkers
  # Input: none
  # Output: none
  ("tick_town_walkers",
    [(try_for_agents, ":cur_agent"),
       (agent_get_troop_id, ":cur_troop", ":cur_agent"),
       (is_between, ":cur_troop", walkers_begin, walkers_end),
       (agent_get_slot, ":target_entry_point", ":cur_agent", 0),
       (entry_point_get_position, pos1, ":target_entry_point"),
       (try_begin),
         (lt, ":target_entry_point", 32),
         (init_position, pos2),
         (position_set_y, pos2, 250),
         (position_transform_position_to_parent, pos1, pos1, pos2),
       (try_end),
       (agent_get_position, pos2, ":cur_agent"),
       (get_distance_between_positions, ":distance", pos1, pos2),
       (lt, ":distance", 400),
       (assign, ":random_no", 0),
       (try_begin),
         (lt, ":target_entry_point", 32),
         (store_random_in_range, ":random_no", 0, 100),
       (try_end),
       #gekokujo 3.1 kyoto has up to three times as many town walkers start
       #(lt, ":random_no", 20),
       (lt, ":random_no", 60), #more moving, less standing?
       #gekokujo 3.1 kyoto has up to three times as many town walkers end
       (call_script, "script_set_town_walker_destination", ":cur_agent"),
     (try_end),
  ]),
  # script_set_town_walker_destination
  # Input: arg1 = agent_no
  # Output: none
  ("set_town_walker_destination",
    [(store_script_param_1, ":agent_no"),
     (assign, reg0, 9),
     (assign, reg1, 10),
     (assign, reg2, 12),
     (assign, reg3, 32),
     (assign, reg4, 33),
     (assign, reg5, 34),
     (assign, reg6, 35),
     (assign, reg7, 36),
     (assign, reg8, 37),
     (assign, reg9, 38),
     (assign, reg10, 39),
     (try_for_agents, ":cur_agent"),
       (agent_get_troop_id, ":cur_troop", ":cur_agent"),
       (is_between, ":cur_troop", walkers_begin, walkers_end),
       (agent_get_slot, ":target_entry_point", ":cur_agent", 0),
       (try_begin),
         (eq, ":target_entry_point", 9),
         (assign, reg0, 0),
       (else_try),
         (eq, ":target_entry_point", 10),
         (assign, reg1, 0),
       (else_try),
         (eq, ":target_entry_point", 12),
         (assign, reg2, 0),
       (else_try),
         (eq, ":target_entry_point", 32),
         (assign, reg3, 0),
       (else_try),
         (eq, ":target_entry_point", 33),
         (assign, reg4, 0),
       (else_try),
         (eq, ":target_entry_point", 34),
         (assign, reg5, 0),
       (else_try),
         (eq, ":target_entry_point", 35),
         (assign, reg6, 0),
       (else_try),
         (eq, ":target_entry_point", 36),
         (assign, reg7, 0),
       (else_try),
         (eq, ":target_entry_point", 37),
         (assign, reg8, 0),
       (else_try),
         (eq, ":target_entry_point", 38),
         (assign, reg9, 0),
       (else_try),
         (eq, ":target_entry_point", 39),
         (assign, reg10, 0),
       (try_end),
     (try_end),
     (assign, ":try_limit", 100),
     (assign, ":target_entry_point", 0),
     (try_for_range, ":unused", 0, ":try_limit"),
       (shuffle_range, 0, 11),
       (gt, reg0, 0),
       (assign, ":target_entry_point", reg0),
       (assign, ":try_limit", 0),
     (try_end),
     (try_begin),
       (gt, ":target_entry_point", 0),
       (agent_set_slot, ":agent_no", 0, ":target_entry_point"),
       (entry_point_get_position, pos1, ":target_entry_point"),
       (try_begin),
         (lt, ":target_entry_point", 32),
         (init_position, pos2),
         (position_set_y, pos2, 250),
         (position_transform_position_to_parent, pos1, pos1, pos2),
       (try_end),
       (agent_set_scripted_destination, ":agent_no", pos1, 0),
       (agent_set_speed_limit, ":agent_no", 5),
     (try_end),
  ]),
  # script_town_init_doors
  # Input: door_state (-1 = closed, 1 = open, 0 = use $town_nighttime)
  # Output: none (required for siege mission templates)
  ("town_init_doors",
   [(store_script_param, ":door_state", 1),
    (try_begin),
      (assign, ":continue", 0),
      (try_begin),
        (eq, ":door_state", 1),
        (assign, ":continue", 1),
      (else_try),
        (eq, ":door_state", 0),
        (eq, "$town_nighttime", 0),
        (assign, ":continue", 1),
      (try_end),
      (eq, ":continue", 1),# open doors
      (assign, ":end_cond", 1),
      (try_for_range, ":i_instance", 0, ":end_cond"),
        (scene_prop_get_instance, ":object", "spr_towngate_door_left", ":i_instance"),
        (ge, ":object", 0),
        (val_add, ":end_cond", 1),
        (prop_instance_get_position, pos1, ":object"),
        (position_rotate_z, pos1, -100),
        (prop_instance_animate_to_position, ":object", pos1, 1),
      (try_end),
      (assign, ":end_cond", 1),
      (try_for_range, ":i_instance", 0, ":end_cond"),
        (scene_prop_get_instance, ":object", "spr_towngate_rectangle_door_left", ":i_instance"),
        (ge, ":object", 0),
        (val_add, ":end_cond", 1),
        (prop_instance_get_position, pos1, ":object"),
        (position_rotate_z, pos1, -80),
        (prop_instance_animate_to_position, ":object", pos1, 1),
      (try_end),
      (assign, ":end_cond", 1),
      (try_for_range, ":i_instance", 0, ":end_cond"),
        (scene_prop_get_instance, ":object", "spr_towngate_door_right", ":i_instance"),
        (ge, ":object", 0),
        (val_add, ":end_cond", 1),
        (prop_instance_get_position, pos1, ":object"),
        (position_rotate_z, pos1, 100),
        (prop_instance_animate_to_position, ":object", pos1, 1),
      (try_end),
      (assign, ":end_cond", 1),
      (try_for_range, ":i_instance", 0, ":end_cond"),
        (scene_prop_get_instance, ":object", "spr_towngate_rectangle_door_right", ":i_instance"),
        (ge, ":object", 0),
        (val_add, ":end_cond", 1),
        (prop_instance_get_position, pos1, ":object"),
        (position_rotate_z, pos1, 80),
        (prop_instance_animate_to_position, ":object", pos1, 1),
      (try_end),
    (try_end),
  ]),
 # script_set_town_picture
  # Input: none
  # Output: none
  ("set_town_picture",
   [
        (try_begin),
		  #gekokujo use only one type of town pic
          #(party_get_current_terrain, ":cur_terrain", "$current_town"),
          (party_slot_eq,"$current_town",slot_party_type, spt_town),
          #(try_begin),
          #  (this_or_next|eq, ":cur_terrain", rt_steppe),
          #  (this_or_next|eq, ":cur_terrain", rt_steppe_forest),
          #  (this_or_next|eq, ":cur_terrain", rt_desert),
          #  (             eq, ":cur_terrain", rt_desert_forest),
          #  (set_background_mesh, "mesh_pic_towndes"),
          #(else_try),
          #  (this_or_next|eq, ":cur_terrain", rt_snow),
          #  (             eq, ":cur_terrain", rt_snow_forest),
          #  (set_background_mesh, "mesh_pic_townsnow"),
          #(else_try),
          #  (set_background_mesh, "mesh_pic_town1"),
          #(try_end),
		  (set_background_mesh, "mesh_gekokujo_pic_town"),
        (else_try),
		  #gekokujo use only one type of castle pic
		  (set_background_mesh, "mesh_gekokujo_pic_castle"),
          #(try_begin),
          #  (this_or_next|eq, ":cur_terrain", rt_steppe),
          #  (this_or_next|eq, ":cur_terrain", rt_steppe_forest),
          #  (this_or_next|eq, ":cur_terrain", rt_desert),
          #  (             eq, ":cur_terrain", rt_desert_forest),
          #  (set_background_mesh, "mesh_pic_castledes"),
          #(else_try),
          #  (this_or_next|eq, ":cur_terrain", rt_snow),
          #  (             eq, ":cur_terrain", rt_snow_forest),
          #  (set_background_mesh, "mesh_pic_castlesnow"),
          #(else_try),
          #  (set_background_mesh, "mesh_pic_castle1"),
          #(try_end),
        (try_end),
    ]),
  #script_update_tavern_travellers
  # INPUT: none
  # OUTPUT: none
  ("update_tavern_travellers",
    [(try_for_range, ":town_no", towns_begin, towns_end),
       (party_set_slot, ":town_no", slot_center_tavern_traveler, 0),
     (try_end),
     
     (try_for_range, ":troop_no", tavern_travelers_begin, tavern_travelers_end),
       (store_random_in_range, ":town_no", towns_begin, towns_end),
       (party_set_slot, ":town_no", slot_center_tavern_traveler, ":troop_no"),
       (assign, ":end_cond", 15),
       (try_for_range, ":unused", 0, ":end_cond"),
         (store_random_in_range, ":info_faction", kingdoms_begin, kingdoms_end),
         (faction_slot_eq, ":info_faction", slot_faction_state, sfs_active),
         (neq, ":info_faction", "$players_kingdom"),
         (neq, ":info_faction", "fac_player_supporters_faction"),
         (party_set_slot, ":town_no", slot_center_traveler_info_faction, ":info_faction"),
         (assign, ":end_cond", 0),
       (try_end),
     (try_end),
	 
	 (troop_set_slot, "trp_belligerent_drunk", slot_troop_cur_center, "p_town_1"),
     ]),
  #script_update_booksellers
  # INPUT: none
  # OUTPUT: none
  ("update_booksellers",
    [(try_for_range, ":town_no", towns_begin, towns_end),
       (party_set_slot, ":town_no", slot_center_tavern_bookseller, 0),
     (try_end),
     
     (try_for_range, ":troop_no", tavern_booksellers_begin, tavern_booksellers_end),
       (store_random_in_range, ":town_no", towns_begin, towns_end),
       (party_set_slot, ":town_no", slot_center_tavern_bookseller, ":troop_no"),
     (try_end),
	 

	 
     ]),
  #script_update_tavern_minstels
  # INPUT: none
  # OUTPUT: none
  ("update_tavern_minstrels",
    [(try_for_range, ":town_no", towns_begin, towns_end),
       (party_set_slot, ":town_no", slot_center_tavern_minstrel, 0),
     (try_end),
     
     (try_for_range, ":troop_no", tavern_minstrels_begin, tavern_minstrels_end),
       (store_random_in_range, ":town_no", towns_begin, towns_end),
       (party_set_slot, ":town_no", slot_center_tavern_minstrel, ":troop_no"),
	   (try_begin),
		(eq, "$cheat_mode", 1),
		(str_store_troop_name, s4, ":troop_no"),
		(str_store_party_name, s5, ":town_no"),
		
	    (display_message, "str_s4_is_at_s5"),
	   (try_end),	
     (try_end),
	 
	 
     ]),
  ("update_other_taverngoers", 
  [
	(store_random_in_range, ":fight_promoter_tavern", towns_begin, towns_end),
	(troop_set_slot, "trp_fight_promoter", slot_troop_cur_center, ":fight_promoter_tavern"),
	
	(store_random_in_range, ":belligerent_drunk_tavern", towns_begin, towns_end),
	(troop_set_slot, "trp_belligerent_drunk", slot_troop_cur_center, ":belligerent_drunk_tavern"),	
	]),
]
