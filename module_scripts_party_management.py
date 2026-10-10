# -*- coding: utf-8 -*-
# module_scripts_party_management.py -- auto split from module_scripts.py (feature: 队伍管理/战利品/升级)
# entries: 49 (order preserved within this file)
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


scripts_party_management = [

  # script_party_get_ideal_size @used for NPC parties.
  # Input: arg1 = party_no
  # Output: reg0: ideal size 
  ("party_get_ideal_size",
    [
    (store_script_param_1, ":party_no"),
    (assign, ":limit", 30),
    (try_begin),
        (party_slot_eq, ":party_no", slot_party_type, spt_kingdom_hero_party),
        (party_stack_get_troop_id, ":party_leader", ":party_no", 0),
        (store_faction_of_party, ":faction_id", ":party_no"),
        (assign, ":limit", 10),

        (store_skill_level, ":skill", "skl_leadership", ":party_leader"),
        (store_attribute_level, ":charisma", ":party_leader", ca_charisma),
        (val_mul, ":skill", 5),
        (val_add, ":limit", ":skill"),
        (val_add, ":limit", ":charisma"),

        (troop_get_slot, ":troop_renown", ":party_leader", slot_troop_renown),
        (store_div, ":renown_bonus", ":troop_renown", 25),
        (val_add, ":limit", ":renown_bonus"),
        
        ##diplomacy begin
        (assign, ":percent", 100),
        ##diplomacy end

        ##diplomacy start+
        #Limit effects of policies for nascent kingdoms.
        (assign, ":policy_min", -3),
        (assign, ":policy_max", 4),#one greater than the maximum

        (try_begin),
			(this_or_next|eq, ":faction_id", "fac_player_supporters_faction"),
			(faction_slot_eq, ":faction_id", slot_faction_leader, "trp_player"),
		
			(faction_get_slot, ":policy_max", ":faction_id", slot_faction_num_towns),
			(faction_get_slot, reg0, ":faction_id", slot_faction_num_castles),
			(val_add, ":policy_max", reg0),
			(val_clamp, ":policy_max", 0, 4),#0, 1, 2, 3
			(store_mul, ":policy_min", ":policy_max", -1),
			(val_add, ":policy_max", 1),#one greater than the maximum
		(try_end),
		##diplomacy end+

        (try_begin),
          (faction_slot_eq, ":faction_id", slot_faction_leader, ":party_leader"),
		  #gekokujo 3.0 greatly reduce faction leader party size
          #(val_add, ":limit", 100),
		  (val_add, ":limit", 20),
		##diplomacy begin
		(try_begin),
			(faction_get_slot, ":centralization", ":faction_id", dplmc_slot_faction_centralization),
			(neq, ":centralization", 0),
			##diplomacy start+ Apply constraint
			(val_clamp, ":centralization", ":policy_min", ":policy_max"),
			##diplomacy end+
			(val_mul, ":centralization", 10),
			(val_add, ":percent", ":centralization"),
		(try_end),

		(else_try),
		(try_begin),
			(faction_get_slot, ":centralization", ":faction_id", dplmc_slot_faction_centralization),
			(neq, ":centralization", 0),
			##diplomacy start+ Apply constraint
			(val_clamp, ":centralization", ":policy_min", ":policy_max"),
			##diplomacy end+
			(val_mul, ":centralization", -3),
			(val_add, ":percent", ":centralization"),
			(try_end),
			(try_begin),
			(faction_get_slot, ":aristocraty", ":faction_id", dplmc_slot_faction_aristocracy),
			(neq, ":aristocraty", 0),
			##diplomacy start+ Apply constraint
			(val_clamp, ":aristocraty", ":policy_min", ":policy_max"),
			##diplomacy end+
			(val_mul, ":aristocraty", 3),
			(val_add, ":percent", ":aristocraty"),
		(try_end),
		(try_begin),
			(faction_get_slot, ":quality", ":faction_id", dplmc_slot_faction_quality),
			(neq, ":quality", 0),
			##diplomacy start+ Apply constraint
			(val_clamp, ":quality", ":policy_min", ":policy_max"),
			##diplomacy end+
			(val_mul, ":quality", -4),
			(val_add, ":percent", ":quality"),
		(try_end),
		##diplomacy end
        (try_end),
        
        ##diplomacy begin
		(try_begin),
			(faction_get_slot, ":serfdom", ":faction_id", dplmc_slot_faction_serfdom),
			(neq, ":serfdom", 0),
			##diplomacy start+ Apply constraint
			(val_clamp, ":serfdom", ":policy_min", ":policy_max"),
			##diplomacy end+
			(val_mul, ":serfdom", 3),
			(val_add, ":percent", ":serfdom"),
		(try_end),

		(val_mul, ":limit", ":percent"),
		##nested diplomacy start+ Round correctly
		(val_add, ":limit", 50),
		##nested diplomacy end+
		(val_div, ":limit", 100),
		##diplomacy end

        (try_begin),
			(faction_slot_eq, ":faction_id", slot_faction_marshall, ":party_leader"),
			(val_add, ":limit", 20),
        (try_end),        

        (try_for_range, ":cur_center", castles_begin, castles_end),
			(party_slot_eq, ":cur_center", slot_town_lord, ":party_leader"),
			(val_add, ":limit", 20),
        (try_end),        

	##diplomacy start+
	##Extend this script so it will also work with garrisons
    (else_try),
		(party_slot_eq, ":party_no", slot_party_type, spt_town),
		#gekokujo 3.0 new garrison ideal sizes start
		#(assign, ":limit", 380),#average starting town garrison size
        (store_faction_of_party, ":faction_id", ":party_no"),
		(try_begin),
			(eq, ":faction_id", "fac_kingdom_20"),
			(assign, ":limit", 617),
		(else_try),
			(assign, ":limit", 475),
		(try_end),
		#gekokujo 3.0 new garrison ideal sizes end
    (else_try),
		(this_or_next|is_between, ":party_no", walled_centers_begin, walled_centers_end),
		(party_slot_eq, ":party_no", slot_party_type, spt_castle),
		#gekokujo 3.0 new garrison ideal sizes start
		#(assign, ":limit", 142),#average starting castle garrison size
        (store_faction_of_party, ":faction_id", ":party_no"),
		(try_begin),
			(eq, ":faction_id", "fac_kingdom_20"),
			(assign, ":limit", 237),
		(else_try),
			(assign, ":limit", 190),
		(try_end),
		#gekokujo 3.0 new garrison ideal sizes end
    ##diplomacy end+
	  
    (try_end),

		# NE dk ## Invasion
		(try_begin),
          (eq, ":faction_id", "fac_dark_knights"),
          (val_add, ":limit", 100),
        (try_end),
		# NE End dk	  
            
    (store_character_level, ":level", "trp_player"), #increase limits a little bit as the game progresses.
	#gekokujo 3.0 forgot to integrate start
    (val_min, ":level", 80),
	#gekokujo 3.0 forgot to integrate end
    (store_add, ":level_factor", 80, ":level"),
    (val_mul, ":limit", ":level_factor"),
    (val_div, ":limit", 80),
    (assign, reg0, ":limit"),
  ]),
  #script_party_calculate_regular_strength:
  # INPUT:
  # param1: Party-id
  ("party_calculate_regular_strength",
    [
      (store_script_param_1, ":party"), #Party_id
      
      (assign, reg0,0),
      (party_get_num_companion_stacks, ":num_stacks",":party"),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop", ":party", ":i_stack"),
        (neg|troop_is_hero, ":stack_troop"),
        (store_character_level, ":stack_strength", ":stack_troop"),
        (val_add, ":stack_strength", 12),
        (val_mul, ":stack_strength", ":stack_strength"),
        (val_div, ":stack_strength", 100),
        (party_stack_get_size, ":stack_size",":party",":i_stack"),
        (party_stack_get_num_wounded, ":num_wounded",":party",":i_stack"),
        (val_sub, ":stack_size", ":num_wounded"),
        (val_mul, ":stack_strength", ":stack_size"),
        (val_add,reg0, ":stack_strength"),
      (try_end),
  ]),
  ("party_calculate_strength",
    [
      (store_script_param_1, ":party"), #Party_id
      (store_script_param_2, ":exclude_leader"), #Party_id
      
      (assign, reg0,0),
      (party_get_num_companion_stacks, ":num_stacks", ":party"),
      (assign, ":first_stack", 0),
      (try_begin),
        (neq, ":exclude_leader", 0),
        (assign, ":first_stack", 1),
      (try_end),
      (try_for_range, ":i_stack", ":first_stack", ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop",":party", ":i_stack"),
        (store_character_level, ":stack_strength", ":stack_troop"),
        (val_add, ":stack_strength", 4), #new was 12 (patch 1.125)
        (val_mul, ":stack_strength", ":stack_strength"),
        (val_mul, ":stack_strength", 2), #new (patch 1.125)
        (val_div, ":stack_strength", 100),
        (val_max, ":stack_strength", 1), #new (patch 1.125)
        (try_begin),
          (neg|troop_is_hero, ":stack_troop"),
          (party_stack_get_size, ":stack_size",":party",":i_stack"),
          (party_stack_get_num_wounded, ":num_wounded",":party",":i_stack"),                    
          (val_sub, ":stack_size", ":num_wounded"),
          (val_mul, ":stack_strength", ":stack_size"),
        (else_try),
          (troop_is_wounded, ":stack_troop"), #hero & wounded
          (assign, ":stack_strength", 0),
        (try_end),
        (val_add, reg0, ":stack_strength"),
      (try_end),
      (party_set_slot, ":party", slot_party_cached_strength, reg0),
  ]),
  #script_loot_player_items:
  # INPUT: arg1 = enemy_party_no
  # Output: none
  ("loot_player_items",
    [
      (store_script_param, ":enemy_party_no", 1),
	  ##diplomacy start+ some enemy lords will not loot the personal equipment of a player who surrendered
	  (assign, ":save_reg0", reg0),
	  (assign, ":extra_gold", 0),
	  #I am not sure if this is historical or not, but it gives the player a reason to
	  #surrender (rather than fight to the end) even before permanent attribute loss is
	  #a possibility (or even if it is disabled outright).
	  #
	  #This also adds another layer of interaction, and makes different lords feel
	  #different from each other.
	  #
	  #Other changes:
	  # Enemy lords will receive gold they loot from the player,
	  # Books will not be looted from the player (it turns out a bug was responsible for this being possible)
	  # The enemy leader's looting skill will affect the amount of gold lootable.
	  (assign, ":merciful", 0),
	  (assign, ":party_leader", -1),
	  (game_get_reduce_campaign_ai, ":reduce_campaign_ai"),
	  (try_begin),
 	    (ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_LOW),#only use this if it is explicitly enabled
	    #Possibility the player's personal equipment will be untouched if he surrendered
  	    (ge, "$g_player_surrenders", 1),
   	    (gt, ":enemy_party_no", 0),
		(party_stack_get_troop_id, ":party_leader", ":enemy_party_no", 0),
	   #(party_slot_eq, ":enemy_party_no", slot_party_type, spt_kingdom_hero_party),
		(ge, ":party_leader", walkers_end),
		(troop_is_hero, ":party_leader"),
		(call_script, "script_troop_get_player_relation", ":party_leader"),
		(assign, ":relation", reg0),
		(assign, ":probability_modifier", 0),
		(try_begin),
			#Upstanding lords are inclined to honor deals in general, and will automatically
			#do so with honorable lords they do not extremely dislike.  However, this does not
			#extend to commoners.
			(troop_slot_ge, "trp_player", slot_troop_banner_scene_prop, 1),# the player has a coat of arms
			(troop_slot_eq, ":party_leader", slot_lord_reputation_type, lrep_upstanding),
			(val_max, ":probability_modifier", 10),#set to +10 unless already higher
			#They will automatically honor deals with the honorable, if they do not
			#excessively dislike them.
			(ge, "$player_honor", 1),
			(val_add, reg0, 10),
			(val_clamp, reg0, 11, 21),
			(val_max, ":probability_modifier", reg0),#set somewhere from +11 to +20 unless already higher
			(ge, ":relation", -10),
			(assign, ":merciful", 1),
		(else_try),
			#Martial lords are inclined to honor deals with lords who likewise follow the rules of war,
			#and will do so as long as they are neutral or friendly towards them.  This does not extend
			#to commoners.
			(troop_slot_ge, "trp_player", slot_troop_banner_scene_prop, 1),# the player has a coat of arms
			(this_or_next|troop_slot_eq, ":party_leader", slot_lord_reputation_type, lrep_moralist),
			(troop_slot_eq, ":party_leader", slot_lord_reputation_type, lrep_martial),
			(ge, "$player_honor", 1),
			(assign, reg0, "$player_honor"),
			(val_clamp, reg0, 1, 6),
			(val_max, ":probability_modifier", reg0),#set somewhere from +1 to +5 unless already higher
			(ge, ":relation", 0),
			(assign, ":merciful", 1),
		(else_try),
			#Good-natured lords are inclined to honor deals with everyone, commoner or not.
			#They will do so automatically unless they particularly dislike someone.
			#This also goes for Moralist ladies if they someone end up accepting your surrender.
			(this_or_next|troop_slot_eq, ":party_leader", slot_lord_reputation_type, lrep_goodnatured),
			(troop_slot_eq, ":party_leader", slot_lord_reputation_type, lrep_moralist),
			(val_max, ":probability_modifier", 21),#set to +20 unless already higher
			(ge, ":relation", -10),
			(assign, ":merciful", 1),
		(else_try),
			#Honest lords are inclined honor deals with everyone, commoner or not.
			#They will do so automatically unless they particularly dislike someone.
			(call_script, "script_dplmc_get_troop_morality_value", ":party_leader", tmt_honest),
			(assign, ":honest_val", reg0),
			(ge, ":honest_val", 1),
			(store_add, reg0, ":honest_val", 14),
			(val_max, ":probability_modifier", reg0),#set to (14 + honesty ) unless already higher
			(ge, "$player_honor", 1),
			(val_mul, reg0, -1),
			(ge, ":relation", reg0),
			(assign, ":merciful", 1),
		(else_try),
			(try_begin),
				#Penalty instead of bonus for vicious lord personalities, unless they are
				#explicitly set as honest.  (None are by default.)
				(lt, ":honest_val", 1),#Must either be negative or not given
				(this_or_next|lt, ":honest_val", 0),
				(this_or_next|troop_slot_eq, ":party_leader", slot_lord_reputation_type, lrep_debauched),
				(this_or_next|troop_slot_eq, ":party_leader", slot_lord_reputation_type, lrep_selfrighteous),
				(this_or_next|troop_slot_eq, ":party_leader", slot_lord_reputation_type, lrep_cunning),
				(troop_slot_eq, ":party_leader", slot_lord_reputation_type, lrep_quarrelsome),
				(val_min, ":probability_modifier", -10),#set to -10 unless already lower
			(try_end),
			#Now store into reg0 the percent chance of mercy
			(try_begin),
				(le, ":reduce_campaign_ai", 0),#Hard: base chance 25% + relation
				(store_add, reg0, ":relation", 25),
			(else_try),
				(eq, ":reduce_campaign_ai", 1),#Medium: base chance 50% + relation
				(store_add, reg0, ":relation", 50),
			(else_try),
				(ge, ":reduce_campaign_ai", 2),#Easy: base chance 75% + relation
				(store_add, reg0, ":relation", 75),
			(try_end),
			(val_add, reg0, ":probability_modifier"),#modify the chance based on the captor's personality
			(val_max, reg0, ":probability_modifier"),#at least this much of a chance
			(val_max, reg0, 5),#at least a 5% chance
			(store_random_in_range, ":probability_modifier", 1, 101),
			(lt, reg0, ":probability_modifier"),
			(assign, ":merciful", 1),
		(try_end),
	  (else_try),
  	   (ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_LOW),#only use this if it is explicitly enabled
		#Surrendered to a non-hero party
		(gt, ":enemy_party_no", 0),
		(ge, "$g_player_surrenders", 1),
		(store_random_in_range, reg0, 1, 101),
		(this_or_next|lt, reg0, 25),#Hard: 25% chance
			(ge, ":reduce_campaign_ai", 1),
		(this_or_next|lt, reg0, 50),#Medium: 50% chance
			(ge, ":reduce_campaign_ai", 2),
		(lt, reg0, 75),#Easy: 75% chance
		(assign, ":merciful", 1),
	  (try_end),
	  (try_begin),
		(ge, "$cheat_mode", 1),
		(ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_LOW),#don't display when nonapplicable
		(assign, ":save_reg1", reg1),
		(assign, reg0, "$g_player_surrenders"),
		(assign, reg1, ":merciful"),
		(display_message, "@{!} DEBUG loot_player_items: g_player_surrenders = {reg0}, merciful = {reg1}"),
        (assign, reg1, ":save_reg1"),
	  (try_end),
	  ##diplomacy end+      
      (troop_get_inventory_capacity, ":inv_cap", "trp_player"),
      (try_for_range, ":i_slot", 0, ":inv_cap"),
        (troop_get_inventory_slot, ":item_id", "trp_player", ":i_slot"),
        (ge, ":item_id", 0),
		##diplomacy start+ looting changes
		(neg|is_between, ":item_id", books_begin, books_end),#shouldn't be necessary, but just in case
		(assign, ":randomness", 0),#properly initialize variables
		##diplomacy end+
        (troop_get_inventory_slot_modifier, ":item_modifier", "trp_player", ":i_slot"),
        (try_begin),
          (is_between, ":item_id", trade_goods_begin, trade_goods_end),
          (assign, ":randomness", 20),
        (else_try),
          (is_between, ":item_id", horses_begin, horses_end),
          #(this_or_next|is_between, ":item_id", horses_begin, horses_end),
          #(this_or_next|eq, ":item_id", "itm_warhorse_sarranid"),
          #(eq, ":item_id", "itm_warhorse_steppe"),
          (assign, ":randomness", 15),
        (else_try),
          (this_or_next|is_between, ":item_id", weapons_begin, weapons_end),
          (is_between, ":item_id", ranged_weapons_begin, ranged_weapons_end),
          (assign, ":randomness", 5),
        (else_try),
          (this_or_next|is_between, ":item_id", armors_begin, armors_end),
		  #(this_or_next|eq, ":item_id", "itm_plate_boots"), #added to the end because of not breaking the save games
          (is_between, ":item_id", shields_begin, shields_end),
          (assign, ":randomness", 5),
        (try_end),
        (store_random_in_range, ":random_no", 0, 100),
        (lt, ":random_no", ":randomness"),
		##diplomacy start+ changes
		(try_begin),
			#If this option is enabled, personal items may be spared, and instead
			#sligthly more gold is taken (but not as much as the thing's worth).
			(ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_LOW),
			(ge, ":merciful", 1),
			(is_between, ":i_slot", ek_item_0, dplmc_ek_alt_items_end),
			(assign, ":random_no", 101),
			#(store_item_value, reg0, ":item_id"),#don't bother with imods #don't bother with the rest of this
			#(val_div, reg0, 2),
			#(ge, reg0, 1),
			#(val_add, ":extra_gold", reg0),##disable, as it defeats the point!
		(try_end),
		(lt, ":random_no", ":randomness"),
		##diplomacy end+
        (troop_remove_item, "trp_player", ":item_id"),

        (try_begin),
          (gt, ":enemy_party_no", 0),
          (party_get_slot, ":cur_loot_slot", ":enemy_party_no", slot_party_next_looted_item_slot),
          (val_add, ":cur_loot_slot", slot_party_looted_item_1),
          (party_set_slot, ":enemy_party_no", ":cur_loot_slot", ":item_id"),
          (val_sub, ":cur_loot_slot", slot_party_looted_item_1),
          (val_add, ":cur_loot_slot", slot_party_looted_item_1_modifier),
          (party_set_slot, ":enemy_party_no", ":cur_loot_slot", ":item_modifier"),
          (val_sub, ":cur_loot_slot", slot_party_looted_item_1_modifier),
          (val_add, ":cur_loot_slot", 1),
          (val_mod, ":cur_loot_slot", num_party_loot_slots),
          (party_set_slot, ":enemy_party_no", slot_party_next_looted_item_slot, ":cur_loot_slot"),
        (try_end),
      (try_end),
      (store_troop_gold, ":cur_gold", "trp_player"),
	  #gekokujo 3.0 forgot to integrate start
      #(store_div, ":max_lost", ":cur_gold", 4),
	  (store_div, ":max_lost", ":cur_gold", 5),
	  #gekokujo 3.0 forgot to integrate end
      (store_div, ":min_lost", ":cur_gold", 10),
      (store_random_in_range, ":lost_gold", ":min_lost", ":max_lost"),
	  ##diplomacy start+
	  (try_begin),
		#This does nothing unless the option is enabled.
		(ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_MEDIUM),
		#add extra gold from enemy's looting skill
		(gt, ":enemy_party_no", 0),
		(party_get_skill_level, reg0, ":enemy_party_no", "skl_looting"),
		(val_clamp, reg0, 0, 11),#allow range +0 to +10
		(val_add, reg0, 10),
		(val_mul, ":lost_gold", reg0),
		(val_div, ":lost_gold", 10),
		#Add any gold from items not looted.
		(val_add, ":lost_gold", ":extra_gold"),
		#gold looted can't exceed player's actual gold
		(val_min, ":lost_gold", ":cur_gold"),
		(val_max, ":lost_gold", 0),
      (try_end),
	  #diplomacy end+
      (troop_remove_gold, "trp_player", ":lost_gold"),
	  ##diplomacy start+
	  (try_begin),
	    #add looted gold to the enemy, if he's a valid hero
		(is_between, ":party_leader", heroes_begin, heroes_end),
		(troop_is_hero, ":party_leader"),
		(neq, ":party_leader", "trp_player"),
		(neq, ":party_leader", "trp_kingdom_heroes_including_player_begin"),
		(ge, ":lost_gold", 1),
		#(call_script, "script_troop_add_gold", ":party_leader", ":lost_gold"),#add looted gold to enemy
		(troop_get_slot, reg0, ":party_leader", slot_troop_wealth),
		(val_add, reg0, ":lost_gold"),
		(val_max, reg0, 0),
		(troop_set_slot, ":party_leader", slot_troop_wealth, reg0),#add looted gold to enemy
	  (try_end),
	  (assign, reg0, ":save_reg0"),#revert register
	  ##diplomacy end+
      ]),
  #script_party_calculate_loot:
  # INPUT:
  # param1: Party-id
  # Returns num looted items in reg0
  ("party_calculate_loot",
    [
      (store_script_param_1, ":enemy_party"), #Enemy Party_id
            
      (call_script, "script_calculate_main_party_shares"),
      (assign, ":num_player_party_shares", reg0),
            
      (try_for_range, ":i_loot", 0, num_party_loot_slots),
        (store_add, ":cur_loot_slot", ":i_loot", slot_party_looted_item_1),
        (party_get_slot, ":item_no", "$g_enemy_party", ":cur_loot_slot"),
        (gt, ":item_no", 0),
        (party_set_slot, "$g_enemy_party", ":cur_loot_slot", 0),
        (val_sub, ":cur_loot_slot", slot_party_looted_item_1),
        (val_add, ":cur_loot_slot", slot_party_looted_item_1_modifier),
        (party_get_slot, ":item_modifier", "$g_enemy_party", ":cur_loot_slot"),
        (troop_add_item, "trp_temp_troop", ":item_no", ":item_modifier"),
      (try_end),
      (party_set_slot, "$g_enemy_party", slot_party_next_looted_item_slot, 0),
      
      (assign, ":num_looted_items",0),
      (try_begin),
        (this_or_next|party_slot_eq, "$g_enemy_party", slot_party_type, spt_kingdom_caravan),
        (this_or_next|party_slot_eq, "$g_enemy_party", slot_party_type, spt_bandit_lair),
        (party_slot_eq, "$g_enemy_party", slot_party_type, spt_village_farmer),
        (store_mul, ":plunder_amount", player_loot_share, 30),
        (val_mul, ":plunder_amount", "$g_strength_contribution_of_player"),
        (val_div, ":plunder_amount", 100),
        (val_div, ":plunder_amount", ":num_player_party_shares"),
        (try_begin),
          (party_slot_eq, "$g_enemy_party", slot_party_type, spt_kingdom_caravan),
          (reset_item_probabilities, 100),
          (assign, ":range_min", trade_goods_begin),
          (assign, ":range_max", trade_goods_end),
        (else_try),
          (party_slot_eq, "$g_enemy_party", slot_party_type, spt_bandit_lair),
          (val_div, ":plunder_amount", 2),
          (reset_item_probabilities, 1),
          (assign, ":range_min", food_begin),
          (assign, ":range_max", food_end),
        (else_try),
          (val_div, ":plunder_amount", 5),
          (reset_item_probabilities, 1),
          (assign, ":range_min", food_begin),
          (assign, ":range_max", food_end),
        (try_end),
        (store_sub, ":item_to_price_slot", slot_town_trade_good_prices_begin, trade_goods_begin),
        (try_for_range, ":cur_goods", ":range_min", ":range_max"),
          (try_begin),
            (neg|party_slot_eq, "$g_enemy_party", slot_party_type, spt_bandit_lair),
            (store_add, ":cur_price_slot", ":cur_goods", ":item_to_price_slot"),
            (party_get_slot, ":cur_price", "$g_enemy_party", ":cur_price_slot"),                    
          (else_try),
            (assign, ":cur_price", maximum_price_factor),
            (val_add, ":cur_price", average_price_factor),
            (val_div, ":cur_price", 3),
          (try_end),  
                    
          (assign, ":cur_probability", 100),
          (val_mul, ":cur_probability", average_price_factor),
          (val_div, ":cur_probability", ":cur_price"),
          (assign, reg0, ":cur_probability"),
          (set_item_probability_in_merchandise, ":cur_goods", ":cur_probability"),
        (try_end),
        (troop_add_merchandise, "trp_temp_troop", itp_type_goods, ":plunder_amount"),
        (val_add, ":num_looted_items", ":plunder_amount"),
      (try_end),
      
      #Now loot the defeated party
      (store_mul, ":loot_probability", player_loot_share, 3),
      (val_mul, ":loot_probability", "$g_strength_contribution_of_player"),
      (party_get_skill_level, ":player_party_looting", "p_main_party", "skl_looting"),
      (val_add, ":player_party_looting", 10),
      (val_mul, ":loot_probability", ":player_party_looting"),
      (val_div, ":loot_probability", 10),
      (val_div, ":loot_probability", ":num_player_party_shares"),

      (party_get_num_companion_stacks, ":num_stacks",":enemy_party"),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop",":enemy_party",":i_stack"),
        (neg|troop_is_hero, ":stack_troop"),
        (party_stack_get_size, ":stack_size",":enemy_party",":i_stack"),
        (try_for_range, ":unused", 0, ":stack_size"),
          (troop_loot_troop, "trp_temp_troop", ":stack_troop", ":loot_probability"),
        (try_end),
      (try_end),

      #(troop_get_inventory_capacity, ":inv_cap", "trp_temp_troop"),
      #(try_for_range, ":i_slot", 0, ":inv_cap"),
      #  (troop_get_inventory_slot, ":item_id", "trp_temp_troop", ":i_slot"),
      #  (is_between, ":item_id", horses_begin, horses_end),
      #  (troop_set_inventory_slot, "trp_temp_troop", ":i_slot", -1),
      #(try_end),

      (troop_get_inventory_capacity, ":inv_cap", "trp_temp_troop"),
      (try_for_range, ":i_slot", 0, ":inv_cap"),
        (troop_get_inventory_slot, ":item_id", "trp_temp_troop", ":i_slot"),
        (ge, ":item_id", 0),
        (val_add, ":num_looted_items", 1),
      (try_end),

      (assign, reg0, ":num_looted_items"),
  ]),
  #script_calculate_main_party_shares:
  # INPUT:
  # Returns number of player party shares in reg0  
  ("calculate_main_party_shares",
    [
      (assign, ":num_player_party_shares", player_loot_share),
      # Add shares for player's party
      (party_get_num_companion_stacks, ":num_stacks", "p_main_party"),
      (try_for_range, ":i_stack", 1, ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop", "p_main_party", ":i_stack"),
        (try_begin),
          (neg|troop_is_hero, ":stack_troop"),
          (party_stack_get_size, ":stack_size","p_main_party",":i_stack"),
          (val_add, ":num_player_party_shares", ":stack_size"),
        (else_try),
          (val_add, ":num_player_party_shares", hero_loot_share),
        (try_end),
      (try_end),
      
      (assign, reg0, ":num_player_party_shares"),
  ]),
  ("party_give_xp_and_gold",
    [
      (store_script_param_1, ":enemy_party"), #Party_id
      
      (call_script, "script_calculate_main_party_shares"),
      (assign, ":num_player_party_shares", reg0),
            
      (assign, ":total_gain", 0),
      (party_get_num_companion_stacks, ":num_stacks",":enemy_party"),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_troop_id,     ":stack_troop",":enemy_party",":i_stack"),
        (neg|troop_is_hero, ":stack_troop"),
        (party_stack_get_size, ":stack_size",":enemy_party",":i_stack"),
        (store_character_level, ":level", ":stack_troop"),
        (store_add, ":gain", ":level", 10),
        (val_mul, ":gain", ":gain"),
        (val_div, ":gain", 10),
        (store_mul, ":stack_gain", ":gain", ":stack_size"),
        (val_add, ":total_gain", ":stack_gain"),
      (try_end),
      
      (val_mul, ":total_gain", "$g_strength_contribution_of_player"),
      (val_div, ":total_gain", 100),

      (val_min, ":total_gain", 40000), #eliminate negative results
                  
      (assign, ":player_party_xp_gain", ":total_gain"),
      
      (store_random_in_range, ":r", 50, 100),
      (val_mul, ":player_party_xp_gain", ":r"),
      (val_div, ":player_party_xp_gain", 100),
      
      (party_add_xp, "p_main_party", ":player_party_xp_gain"),
      
      (store_mul, ":player_gold_gain", ":total_gain", player_loot_share),
      (val_min, ":player_gold_gain", 60000), #eliminate negative results
      (store_random_in_range, ":r", 50, 100),
      (val_mul, ":player_gold_gain", ":r"),
      (val_div, ":player_gold_gain", 100),
      (val_div, ":player_gold_gain", ":num_player_party_shares"),
      
      #add gold now
      (party_get_num_companion_stacks, ":num_stacks","p_main_party"),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop","p_main_party",":i_stack"),
        (try_begin),
          (troop_is_hero, ":stack_troop"),
          (call_script, "script_troop_add_gold", ":stack_troop", ":player_gold_gain"),
        (try_end),
      (try_end),
  ]),
  ("setup_troop_meeting",
    [
      (store_script_param_1, ":meeting_troop"),
      (store_script_param_2, ":troop_dna"),
      (call_script, "script_get_meeting_scene"), 
      (assign, ":meeting_scene", reg0),
      (modify_visitors_at_site,":meeting_scene"),
      (reset_visitors),
      (set_visitor,0,"trp_player"),
	  (try_begin),
		(gt, ":troop_dna", -1),
        (set_visitor,17,":meeting_troop",":troop_dna"),
	  (else_try),
        (set_visitor,17,":meeting_troop"),
	  (try_end),	
      (set_jump_mission,"mt_conversation_encounter"),
      (jump_to_scene,":meeting_scene"),
      (change_screen_map_conversation, ":meeting_troop"),
  ]),
  ("setup_party_meeting",
    [
      (store_script_param_1, ":meeting_party"),
      (try_begin),
        (lt, "$g_encountered_party_relation", 0), #hostile
#        (call_script, "script_music_set_situation_with_culture", mtf_sit_encounter_hostile),
      (try_end),
      (call_script, "script_get_meeting_scene"), (assign, ":meeting_scene", reg0),
      (modify_visitors_at_site,":meeting_scene"),(reset_visitors),
      (set_visitor,0,"trp_player"),
      (party_stack_get_troop_id, ":meeting_troop",":meeting_party",0),
      (party_stack_get_troop_dna,":troop_dna",":meeting_party",0),
      (try_begin),
        (gt, ":troop_dna", -1),
        (set_visitor,17,":meeting_troop",":troop_dna"),
      (else_try),
        (set_visitor,17,":meeting_troop"),
      (try_end),
      (set_jump_mission,"mt_conversation_encounter"),
      (jump_to_scene,":meeting_scene"),
      (change_screen_map_conversation, ":meeting_troop"),
  ]),
  ("get_meeting_scene",
    [
      (party_get_current_terrain, ":terrain_type", "p_main_party"),
      (assign, ":scene_to_use", "scn_random_scene"),
      (try_begin),
        (eq, ":terrain_type", rt_steppe),
        (assign, ":scene_to_use", "scn_meeting_scene_steppe"),
      (else_try),
        (eq, ":terrain_type", rt_plain),
        (assign, ":scene_to_use", "scn_meeting_scene_plain"),
      (else_try),
        (eq, ":terrain_type", rt_snow),
        (assign, ":scene_to_use", "scn_meeting_scene_snow"),
      (else_try),
        (eq, ":terrain_type", rt_desert),
        (assign, ":scene_to_use", "scn_meeting_scene_desert"),
      (else_try),
        (eq, ":terrain_type", rt_steppe_forest),
        (assign, ":scene_to_use", "scn_meeting_scene_steppe"),
      (else_try),
        (eq, ":terrain_type", rt_forest),
        (assign, ":scene_to_use", "scn_meeting_scene_plain"),
      (else_try),
        (eq, ":terrain_type", rt_snow_forest),
        (assign, ":scene_to_use", "scn_meeting_scene_snow"),
      (else_try),
        (eq, ":terrain_type", rt_desert_forest),
        (assign, ":scene_to_use", "scn_meeting_scene_desert"),
      (else_try),
        (assign, ":scene_to_use", "scn_meeting_scene_plain"),
      (try_end),
      (assign, reg0, ":scene_to_use"),
  ]),
  ("party_remove_all_companions",
    [
      (store_script_param_1, ":party"), #Source Party_id
      (party_get_num_companion_stacks, ":num_companion_stacks",":party"),
      
      #gekokujo 3.1 ninja rescue start
      #let's use $gekokujo_rescue_score but not mess with it yet
      #this script pares down the rescueable contingent of your party
      #but we still have to pare them down even further during the captivity phase
      (assign, ":rescued_companions", "$gekokujo_rescue_score"),
      (val_sub, ":rescued_companions", 1), #the player themselves costs 1 point
      (val_div, ":rescued_companions", 2), #companion heroes cost 2 points each
      (val_max, ":rescued_companions", 0), #don't go below 0
      #gekokujo 3.1 ninja rescue end
      
      (try_for_range_backwards, ":stack_no", 0, ":num_companion_stacks"),
        (party_stack_get_troop_id, ":stack_troop",":party",":stack_no"),
       
        (party_stack_get_size, ":stack_size", ":party", ":stack_no"),
        
        (try_begin),
		##diplomacy start+
		  #To avoid problems with temporarily-rejoined promoted companions and ladies
		  #suddenly forgetting that they're lords, check this.
			#If the troop is a companion or a kingdom lady...
			#gekokujo 3.0 microfactions! include fort companions start
			#(this_or_next|is_between, ":stack_troop", companions_begin, companions_end),
			(this_or_next|is_between, ":stack_troop", companions_begin, fort_companions_end),
			#gekokujo 3.0 microfactions! include fort companions end
				(is_between, ":stack_troop", kingdom_ladies_begin, kingdom_ladies_end),
			#...but has since become a lord
			(this_or_next|troop_slot_eq, ":stack_troop", slot_troop_playerparty_history, dplmc_pp_history_granted_fief),
			(this_or_next|troop_slot_eq, ":stack_troop", slot_troop_playerparty_history, dplmc_pp_history_lord_rejoined),
				(troop_slot_eq, ":stack_troop", slot_troop_occupation, slto_kingdom_hero),
			#...and the troop would be removed
			(this_or_next|eq, "$g_move_heroes", 1),
				(eq, ":party", "p_main_party"),
			#Then set up the troop as if it was a lord that was just defeated but escaped
			(troop_set_slot, ":stack_troop", slot_troop_occupation, slto_kingdom_hero),
			(troop_set_slot, ":stack_troop", slot_troop_leaded_party, -1),
			(troop_set_slot, ":stack_troop", slot_troop_prisoner_of_party, -1),
			(troop_set_slot, ":stack_troop", slot_troop_cur_center, -1),
			(party_remove_members, ":party", ":stack_troop", ":stack_size"),
		#Fall through to standard behavior:
		(else_try),
	    ##diplomacy end+
          (troop_is_hero, ":stack_troop"),
          (neg|is_between, ":stack_troop", pretenders_begin, pretenders_end),
          (neq, ":stack_troop", "trp_player"),
          (eq, "$g_prison_heroes", 1),
          (eq, ":party", "p_main_party"),
		  #gekokujo 3.0 forgot to integrate start
          #(store_random_in_range, ":succeed_escaping", 0, 4),
          #(neq, ":succeed_escaping", 0), #25% chance companion stays with us.
          (store_random_in_range, ":succeed_escaping", 0, 2),
          #gekokujo 3.1 ninja rescue start
          (try_begin),
            (gt, ":rescued_companions", 0),
            (assign, ":succeed_escaping", 0), #guarantee escape, but still give a chance for more to escape naturally
            (val_sub, ":rescued_companions", 1),
          (try_end),
          #gekokujo 3.1 ninja rescue end
          (neq, ":succeed_escaping", 0), #50% chance companion stays with us.
		  #gekokujo 3.0 forgot to integrate end
          (troop_set_health, ":stack_troop", 100), #heal before leaving
          (store_faction_of_party, ":enemy_faction", "$g_enemy_party"),
          (assign, ":minimum_distance", 99999),
          (assign, ":prison_center", -1),
          (try_for_range, ":center", walled_centers_begin, walled_centers_end),
            (store_faction_of_party, ":center_faction", ":center"),
            (eq, ":center_faction", ":enemy_faction"),
            (store_distance_to_party_from_party, ":dist", ":center", "p_main_party"),
            (lt, ":dist", ":minimum_distance"),
            (assign, ":minimum_distance", ":dist"),
            (assign, ":prison_center", ":center"),
          (try_end),          
          (assign, reg1, ":prison_center"),
          #(display_message, "@{!}DEBUG : prison center is {reg1}"),
          (try_begin),
            (ge, ":prison_center", 0),
            (store_random_in_range, ":succeed_escaping", 0, 4),
            (neq, ":succeed_escaping", 0), #25% chance companion escapes to a tavern.
            (party_add_prisoners, ":prison_center", ":stack_troop", ":stack_size"),          
            (troop_set_slot, ":stack_troop", slot_troop_prisoner_of_party, ":prison_center"),
            (troop_set_slot, ":stack_troop", slot_troop_playerparty_history, pp_history_scattered),          
            (troop_set_slot, ":stack_troop", slot_troop_turned_down_twice, 0),
            (troop_set_slot, ":stack_troop", slot_troop_occupation, 0),                                    
            (party_remove_members, ":party", ":stack_troop", ":stack_size"),
            (try_begin),
              (eq, "$cheat_mode", 1),
              (str_store_party_name, s1, ":prison_center"),
              (display_message, "str_your_hero_prisoned_at_s1"),
            (try_end),
          (else_try),
            #bandits or deserters won and captured companion. So place it randomly in a town's tavern.
            (assign, ":end_condition", 1000),
            (try_for_range, ":unused", 0, ":end_condition"),
              (store_random_in_range, ":town_no", towns_begin, towns_end),
			  ##diplomacy start+
			  #OLD (NATIVE) VERSION:
			  #(neg|troop_slot_eq, ":stack_troop", slot_troop_home, ":town_no"),
              #(neg|troop_slot_eq, ":stack_troop", slot_troop_first_encountered, ":town_no"),
			  #
			  #NEW (DIPLOMACY+) VERSION:
			  #If the player owns the town, the companion is no longer in "never return" mode.
			  (party_get_slot, ":town_lord", ":town_no", slot_town_lord),
			  (this_or_next|eq, ":town_lord", "trp_player"),
			  (this_or_next|troop_slot_eq, "trp_player", slot_troop_spouse, ":town_lord"),
				(neg|troop_slot_eq, ":stack_troop", slot_troop_home, ":town_no"),
              (this_or_next|eq, ":town_lord", "trp_player"),
			  (this_or_next|troop_slot_eq, "trp_player", slot_troop_spouse, ":town_lord"),
			     (neg|troop_slot_eq, ":stack_troop", slot_troop_first_encountered, ":town_no"),
			  ##diplomacy end+
              (assign, ":end_condition", -1),
            (try_end),  
            (troop_set_slot, ":stack_troop", slot_troop_cur_center, ":town_no"),
            (troop_set_slot, ":stack_troop", slot_troop_playerparty_history, pp_history_scattered),
            (troop_set_slot, ":stack_troop", slot_troop_turned_down_twice, 0),
            (troop_set_slot, ":stack_troop", slot_troop_occupation, 0),
            (party_remove_members, ":party", ":stack_troop", ":stack_size"),
            (try_begin),
              (eq, "$cheat_mode", 1),
              (str_store_troop_name, 4, ":stack_troop"),
              (str_store_party_name, 5, ":town_no"),
              (display_message, "@{!}{s4} is sent to {s5} after defeat"),
            (try_end),
          (try_end),
        (else_try),        
          (this_or_next|neg|troop_is_hero, ":stack_troop"),
          (eq, "$g_move_heroes", 1),
          (party_remove_members, ":party", ":stack_troop", ":stack_size"),
        (try_end),
      (try_end),
  ]),
  ("party_remove_all_prisoners",
    [
      (store_script_param_1, ":party"), #Source Party_id
      (party_get_num_prisoner_stacks, ":num_prisoner_stacks",":party"),
      (try_for_range_backwards, ":stack_no", 0, ":num_prisoner_stacks"),
        (party_prisoner_stack_get_troop_id, ":stack_troop",":party",":stack_no"),
        (this_or_next|neg|troop_is_hero, ":stack_troop"),
        (eq, "$g_move_heroes", 1),
        (party_prisoner_stack_get_size, ":stack_size",":party",":stack_no"),
        (party_remove_prisoners, ":party", ":stack_troop", ":stack_size"),
      (try_end),
  ]),
  ("party_add_party_companions",
    [
      (store_script_param_1, ":target_party"), #Target Party_id
      (store_script_param_2, ":source_party"), #Source Party_id
      (party_get_num_companion_stacks, ":num_stacks",":source_party"),
      (try_for_range, ":stack_no", 0, ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop",":source_party",":stack_no"),
        (this_or_next|neg|troop_is_hero, ":stack_troop"),
        (eq, "$g_move_heroes", 1),
        (party_stack_get_size, ":stack_size",":source_party",":stack_no"),
        (party_add_members, ":target_party", ":stack_troop", ":stack_size"),
        (party_stack_get_num_wounded, ":num_wounded", ":source_party", ":stack_no"),
        (party_wound_members, ":target_party", ":stack_troop", ":num_wounded"),
      (try_end),
  ]),
  ("party_add_party_prisoners",
    [
      (store_script_param_1, ":target_party"), #Target Party_id
      (store_script_param_2, ":source_party"), #Source Party_id
      (party_get_num_prisoner_stacks, ":num_stacks",":source_party"),
      (try_for_range, ":stack_no", 0, ":num_stacks"),
        (party_prisoner_stack_get_troop_id, ":stack_troop",":source_party",":stack_no"),
        (this_or_next|neg|troop_is_hero, ":stack_troop"),
        (eq, "$g_move_heroes", 1),
        (party_prisoner_stack_get_size, ":stack_size",":source_party",":stack_no"),
        (party_add_members, ":target_party", ":stack_troop", ":stack_size"),
      (try_end),
  ]),
  ("party_prisoners_add_party_companions",
    [
      (store_script_param_1, ":target_party"), #Target Party_id
      (store_script_param_2, ":source_party"), #Source Party_id
      (party_get_num_companion_stacks, ":num_stacks",":source_party"),
      (try_for_range, ":stack_no", 0, ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop",":source_party",":stack_no"),
        (this_or_next|neg|troop_is_hero, ":stack_troop"),
        (eq, "$g_move_heroes", 1),
        (party_stack_get_size, ":stack_size",":source_party",":stack_no"),
        (party_add_prisoners, ":target_party", ":stack_troop", ":stack_size"),
      (try_end),
  ]),
  ("party_prisoners_add_party_prisoners",
    [
      (store_script_param_1, ":target_party"), #Target Party_id
      (store_script_param_2, ":source_party"), #Source Party_id
      (party_get_num_prisoner_stacks, ":num_stacks",":source_party"),
      (try_for_range, ":stack_no", 0, ":num_stacks"),
        (party_prisoner_stack_get_troop_id, ":stack_troop",":source_party",":stack_no"),
        (this_or_next|neg|troop_is_hero, ":stack_troop"),
        (eq, "$g_move_heroes", 1),
        (party_prisoner_stack_get_size, ":stack_size",":source_party",":stack_no"),
        (party_add_prisoners, ":target_party", ":stack_troop", ":stack_size"),
      (try_end),
  ]),
  ("party_add_party",
    [
      (store_script_param_1, ":target_party"), #Target Party_id
      (store_script_param_2, ":source_party"), #Source Party_id
      (call_script, "script_party_add_party_companions",          ":target_party", ":source_party"),
      (call_script, "script_party_prisoners_add_party_prisoners", ":target_party", ":source_party"),
  ]),
  ("party_copy",
    [
      (assign, "$g_move_heroes", 1),
      (store_script_param_1, ":target_party"), #Target Party_id
      (store_script_param_2, ":source_party"), #Source Party_id
      (party_clear, ":target_party"),
      (call_script, "script_party_add_party", ":target_party", ":source_party"),
  ]),
  ("clear_party_group",
    [
      (store_script_param_1, ":root_party"),
	  
      (party_clear, ":root_party"),
      (party_get_num_attached_parties, ":num_attached_parties", ":root_party"),
      (try_for_range, ":attached_party_rank", 0, ":num_attached_parties"),
        (party_get_attached_party_with_rank, ":attached_party", ":root_party", ":attached_party_rank"),
        (call_script, "script_clear_party_group", ":attached_party"),
      (try_end),
  ]),
  ("party_add_wounded_members_as_prisoners",
    [
      (store_script_param_1, ":target_party"), #Target Party_id
      (store_script_param_2, ":source_party"), #Source Party_id
      (party_get_num_companion_stacks, ":num_stacks", ":source_party"),
      (try_for_range, ":stack_no", 0, ":num_stacks"),
        (party_stack_get_num_wounded, ":num_wounded", ":source_party", ":stack_no"),
        (ge, ":num_wounded", 1),
        (party_stack_get_troop_id, ":stack_troop", ":source_party", ":stack_no"),
        (this_or_next|neg|troop_is_hero, ":stack_troop"),
        (eq, "$g_move_heroes", 1),
        #(party_prisoner_stack_get_size, ":stack_size",":source_party",":stack_no"),
        (party_add_prisoners, ":target_party", ":stack_troop", ":num_wounded"),
      (try_end),
  ]),
  ("get_nonempty_party_in_group",
    [
      (store_script_param_1, ":party_no"),
      (party_get_num_companion_stacks, ":num_companion_stacks", ":party_no"),
      (try_begin),
        (gt, ":num_companion_stacks", 0),
        (assign, reg0, ":party_no"),
      (else_try),
        (assign, reg0, -1),
        
        (party_get_num_attached_parties, ":num_attached_parties", ":party_no"),
        (try_for_range, ":attached_party_rank", 0, ":num_attached_parties"),
          (lt, reg0, 0),
          (party_get_attached_party_with_rank, ":attached_party", ":party_no", ":attached_party_rank"),
          (call_script, "script_get_nonempty_party_in_group", ":attached_party"),
        (try_end),
      (try_end),
  ]),
  ("collect_prisoners_from_empty_parties",
    [
      (store_script_param_1, ":party_no"),
      (store_script_param_2, ":collection_party"),
      
      (party_get_num_companions, ":num_companions", ":party_no"),
      (try_begin),
        (eq, ":num_companions", 0), #party is empty (has no companions). Collect its prisoners.
        (party_get_num_prisoner_stacks, ":num_stacks",":party_no"),
        (try_for_range, ":stack_no", 0, ":num_stacks"),
          (party_prisoner_stack_get_troop_id, ":stack_troop", ":party_no", ":stack_no"),
          (troop_is_hero, ":stack_troop"),
          (party_add_members, ":collection_party", ":stack_troop", 1),
        (try_end),
      (try_end),
      (party_get_num_attached_parties, ":num_attached_parties", ":party_no"),
      (try_for_range, ":attached_party_rank", 0, ":num_attached_parties"),
        (party_get_attached_party_with_rank, ":attached_party", ":party_no", ":attached_party_rank"),
        (call_script, "script_collect_prisoners_from_empty_parties", ":attached_party", ":collection_party"),
      (try_end),
  ]),
  ("change_party_morale",
   [
      (store_script_param_1, ":party_no"),
      (store_script_param_2, ":morale_dif"),

      (party_get_morale, ":cur_morale", ":party_no"),
      (store_add, ":new_morale", ":cur_morale", ":morale_dif"),
      (val_clamp, ":new_morale", 0, 100),
      (party_set_morale, ":party_no", ":new_morale"),
      (str_store_party_name, s1, ":party_no"),
      
      (try_begin),
        (lt, ":new_morale", ":cur_morale"),
        (store_sub, reg1, ":cur_morale", ":new_morale"),
      (else_try),
        (gt, ":new_morale", ":cur_morale"),
        (store_sub, reg1, ":new_morale", ":cur_morale"),        
      (try_end),
  ]),
  ("count_casualties_and_adjust_morale",
   [             
    (call_script, "script_calculate_main_party_shares"),
    (assign, ":num_player_party_shares", reg0),
    
    (assign, ":our_loss_score", 0),
    (party_get_num_companion_stacks, ":num_stacks","p_player_casualties"),
    (try_for_range, ":i_stack", 0, ":num_stacks"),
      (party_stack_get_troop_id, ":stack_troop", "p_player_casualties", ":i_stack"),
      (party_stack_get_size, ":stack_size", "p_player_casualties", ":i_stack"),
      
      (party_stack_get_num_wounded, ":num_wounded", "p_player_casualties", ":i_stack"),
      (store_mul, ":stack_size_mul_2", ":stack_size", 2),
      ##diplomacy start+ Fix what appears to be a mistake in Native
      #(store_sub, ":stack_size_mul_2_sub_wounded", ":num_wounded"),##OLD
      (store_sub, ":stack_size_mul_2_sub_wounded", ":stack_size_mul_2", ":num_wounded"),##NEW
      ##diplomacy end+
      
      (store_character_level, ":level", ":stack_troop"),    
      (store_add, ":gain", ":level", 3),
      
      #if died/wounded troop is player troop then give its level +30 while calculating troop die effect on morale
      (try_begin),
        (eq, ":stack_troop", "trp_player"),
        (val_add, ":level", 75),
      (else_try),
        (troop_is_hero, ":stack_troop"),
        (val_add, ":level", 50),
      (try_end),
      
      (val_mul, ":gain", ":gain"),
      (val_div, ":gain", 10),
      (assign, reg0, ":gain"),
      (val_mul, ":gain", ":stack_size"),
      
      (try_begin),
        (neg|troop_is_hero, ":stack_troop"),
        (val_mul, ":gain", ":stack_size_mul_2_sub_wounded"),
        (val_div, ":gain", ":stack_size_mul_2"),
      (try_end),  
      
      (try_begin),
        (eq, "$cheat_mode", 1),
        (assign, reg1, ":stack_size"),
        (assign, reg2, ":gain"),
        (display_message, "str_our_per_person__reg0_num_people__reg1_total_gain__reg2"),
      (try_end),  
      (val_add, ":our_loss_score", ":gain"),
    (try_end),
    
    (assign, ":died_enemy_population", 0),
    (assign, ":enemy_loss_score", 0),
    (party_get_num_companion_stacks, ":num_stacks","p_enemy_casualties"),
    (try_for_range, ":i_stack", 0, ":num_stacks"),
      (party_stack_get_troop_id, ":stack_troop", "p_enemy_casualties", ":i_stack"),
      (party_stack_get_size, ":stack_size", "p_enemy_casualties", ":i_stack"),

      (party_stack_get_num_wounded, ":num_wounded", "p_enemy_casualties", ":i_stack"),
      (store_mul, ":stack_size_mul_2", ":stack_size", 2),
      (store_sub, ":stack_size_mul_2_sub_wounded", ":stack_size_mul_2", ":num_wounded"),

      (store_character_level, ":level", ":stack_troop"),      
      (store_add, ":gain", ":level", 3),

      #if troop is hero give extra +15 level while calculating troop die effect on morale 
      (try_begin),
        (troop_is_hero, ":stack_troop"),
        (val_add, ":level", 50),
      (try_end),

      (val_mul, ":gain", ":gain"),
      (val_div, ":gain", 10),      
      (assign, reg0, ":gain"),
      (val_mul, ":gain", ":stack_size"),
      
      (try_begin),
        (neg|troop_is_hero, ":stack_troop"),
        (val_mul, ":gain", ":stack_size_mul_2_sub_wounded"),
        (val_div, ":gain", ":stack_size_mul_2"),
      (try_end),  

      (try_begin),
        (eq, "$cheat_mode", 1),
        (assign, reg1, ":stack_size"),
        (assign, reg2, ":gain"),
        (display_message, "str_ene_per_person__reg0_num_people__reg1_total_gain__reg2"),
      (try_end),  
      (val_add, ":enemy_loss_score", ":gain"),
      (val_add, ":died_enemy_population", ":stack_size"),
    (try_end),

    (assign, ":ally_loss_score", 0),
    (try_begin),
      (eq, "$any_allies_at_the_last_battle", 1),
      (party_get_num_companion_stacks, ":num_stacks","p_ally_casualties"),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop", "p_ally_casualties", ":i_stack"),
        (party_stack_get_size, ":stack_size", "p_ally_casualties", ":i_stack"),
        
        (party_stack_get_num_wounded, ":num_wounded", "p_ally_casualties", ":i_stack"),
        (store_mul, ":stack_size_mul_2", ":stack_size", 2),
        ##diplomacy start+ Fix what appears to be a mistake in Native
        #(store_sub, ":stack_size_mul_2_sub_wounded", ":num_wounded"),##OLD
        (store_sub, ":stack_size_mul_2_sub_wounded", ":stack_size_mul_2", ":num_wounded"),##NEW
        ##diplomacy end+

        (store_character_level, ":level", ":stack_troop"),    
        (store_add, ":gain", ":level", 3),

        #if troop is hero give extra +15 level while calculating troop die effect on morale 
        (try_begin),
          (troop_is_hero, ":stack_troop"),
          (val_add, ":level", 50),
        (try_end),

        (val_mul, ":gain", ":gain"),
        (val_div, ":gain", 10),      
        (assign, reg0, ":gain"),
        (val_mul, ":gain", ":stack_size"),

        (try_begin),
          (neg|troop_is_hero, ":stack_troop"),
          (val_mul, ":gain", ":stack_size_mul_2_sub_wounded"),
          (val_div, ":gain", ":stack_size_mul_2"),
        (try_end),  

        (try_begin),
          (eq, "$cheat_mode", 1),
          (assign, reg1, ":stack_size"),
          (assign, reg2, ":gain"),
          (display_message, "str_all_per_person__reg0_num_people__reg1_total_gain__reg2"),
        (try_end),  
        (val_add, ":ally_loss_score", ":gain"),
      (try_end),
    (try_end),
    
    (store_add, ":our_losses", ":our_loss_score", ":ally_loss_score"), 
    (assign, ":enemy_losses", ":enemy_loss_score"),
    (val_mul, ":our_losses", 100),
    
    (try_begin), 
      (eq, "$cheat_mode", 1),
      (assign, reg0, ":enemy_losses"),
      (display_message, "@{!}DEBUGS : enemy_loses : {reg0}"),
    (try_end),  
    
    (try_begin),
      (gt, ":enemy_losses", 0),
      (store_div, ":loss_ratio", ":our_losses", ":enemy_losses"),
    (else_try),
      (assign, ":loss_ratio", 1000),
    (try_end),

    (try_begin),
      (eq, "$cheat_mode", 1),
      (assign, reg1, ":loss_ratio"),
      (display_message, "str_loss_ratio_is_reg1"),
    (try_end),
     
    (try_begin),       
      (neg|is_between, "$g_enemy_party", centers_begin, centers_end),
      (store_sub, ":total_gain", 60, ":loss_ratio"),
    (else_try),
      (store_sub, ":total_gain", 100, ":loss_ratio"),
    (try_end),    

    (try_begin),
      (lt, ":total_gain", 0),
      (val_div, ":total_gain", 2),
    (try_end),

    (try_begin), 
      (eq, "$cheat_mode", 1),
      (assign, reg0, ":total_gain"),
      (display_message, "@{!}DEBUGS1 : total_gain : {reg0}"),
    (try_end),

    (val_max, ":total_gain", -60), #total gain changes between -60(1.8+ loss ratio) and 60(0 loss ratio). We assumed average loss ratio is 0.6
    (val_mul, ":total_gain", ":enemy_losses"),
    (val_div, ":total_gain", 100),

    (store_mul, ":total_enemy_morale_gain", ":total_gain", -1), #enemies get totally negative of the morale we get
    (val_mul, ":total_gain", "$g_strength_contribution_of_player"),
    (val_div, ":total_gain", 100),

    (try_begin), 
      (eq, "$cheat_mode", 1),
      (assign, reg0, ":total_gain"),
      (display_message, "@{!}DEBUGS2 : total_gain : {reg0}"),
    (try_end),  

    (try_begin),
      (party_is_active, "$g_enemy_party"), #change enemy morale if and only if there is a valid enemy party
      
      #main enemy party    
      (assign, ":total_enemy_population", 0),        
      (val_add, ":total_enemy_population", 10), #every part effect total population by number of agents they have plus 10
      (party_get_num_companion_stacks, ":num_stacks", "$g_enemy_party"),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop", "$g_enemy_party", ":i_stack"),
        (party_stack_get_size, ":stack_size", "$g_enemy_party", ":i_stack"),
        (val_add, ":total_enemy_population", ":stack_size"),
      (try_end),
      (assign, ":main_enemy_party_population", ":total_enemy_population"),

      #enemy attachers
      (party_get_num_attached_parties, ":num_attached_parties", "$g_enemy_party"),
      (try_for_range, ":attached_party_rank", 0, ":num_attached_parties"),
        (val_add, ":total_enemy_population", 10), #every part effect total population by number of agents they have plus 10
        (party_get_attached_party_with_rank, ":attached_party", "$g_enemy_party", ":attached_party_rank"),
        (party_get_num_companion_stacks, ":num_stacks", ":attached_party"),
        (try_for_range, ":i_stack", 0, ":num_stacks"),
          (party_stack_get_troop_id, ":stack_troop", ":attached_party", ":i_stack"),
          (party_stack_get_size, ":stack_size", ":attached_party", ":i_stack"),
          (val_add, ":total_enemy_population", ":stack_size"),        
        (try_end),
      (try_end),
    
      #(assign, reg3, ":total_enemy_population"),
      #(assign, reg4, ":died_enemy_population"),
      #(store_sub, ":remaining_enemy_population", ":total_enemy_population", ":died_enemy_population"),
      #(val_add, ":remaining_enemy_population", 10),
      #(assign, reg5, ":remaining_enemy_population"),
      #(display_message, "@total : {reg3}, died : {reg4}, remaining : {reg5}"),
    
      #remaining enemy population has 10+remaining soldiers in enemy party
      (assign, ":remaining_enemy_population", ":total_enemy_population"),

      (assign, reg5, ":remaining_enemy_population"),
      (assign, reg6, ":total_enemy_morale_gain"),
    
      (set_fixed_point_multiplier, 100),
      (val_mul, ":remaining_enemy_population", 100),
      (store_sqrt, ":sqrt_remaining_enemy_population", ":remaining_enemy_population"),
      (val_div, ":sqrt_remaining_enemy_population", 100),            
      (val_div, ":total_enemy_morale_gain", ":sqrt_remaining_enemy_population"),
      (val_div, ":total_enemy_morale_gain", 4),

      (try_begin),
        (eq, "$cheat_mode", 1),
        (assign, reg7, ":total_enemy_morale_gain"),
        (display_message, "str_total_enemy_morale_gain__reg6_last_total_enemy_morale_gain__reg7_remaining_enemy_population__reg5"),
      (try_end),

      (store_mul, ":party_morale_gain", ":total_enemy_morale_gain", ":main_enemy_party_population"),
      (val_div, ":party_morale_gain", ":total_enemy_population"),
      
      (try_begin),      
        (party_is_active, "$g_enemy_party"),
        
        (call_script, "script_change_party_morale", "$g_enemy_party", ":party_morale_gain"),

        (party_get_num_attached_parties, ":num_attached_parties", "$g_enemy_party"),
        (try_for_range, ":attached_party_rank", 0, ":num_attached_parties"),
          (party_get_attached_party_with_rank, ":attached_party", "$g_enemy_party", ":attached_party_rank"),
          (party_get_num_companion_stacks, ":num_stacks", ":attached_party"),
          (assign, ":party_population", 0),
          (try_for_range, ":i_stack", 0, ":num_stacks"),
            (party_stack_get_troop_id, ":stack_troop", ":attached_party", ":i_stack"),
            (party_stack_get_size, ":stack_size", ":attached_party", ":i_stack"),
            (val_add, ":party_population", ":stack_size"),        
          (try_end),
          #(store_div, ":party_ratio", ":total_enemy_population_multiplied_by_100", ":party_population"), #party ratio changes between 0..100, shows population ratio of that party among all enemy parties
          (store_mul, ":party_morale_gain", ":total_enemy_morale_gain", ":party_population"),
          (val_div, ":party_morale_gain", ":total_enemy_population"),
          (call_script, "script_change_party_morale", ":attached_party", ":party_morale_gain"),
        (try_end),
      (try_end),  
    (try_end),
    
    #Add morale
    (assign, ":morale_gain", ":total_gain"),
    (val_div, ":morale_gain", ":num_player_party_shares"),#if there are lots of soldiers in my party there will be less morale increase.
    
    (try_begin), 
      (eq, "$cheat_mode", 1),
      (assign, reg0, ":num_player_party_shares"),
      (assign, reg1, ":total_gain"),
      (display_message, "@{!}DEBUGS3 : num_player_party_shares:{reg0}, total_gain:{reg1}"),
    (try_end),  
    
    (call_script, "script_change_player_party_morale", ":morale_gain"),
    
    (store_mul, ":killed_enemies_by_our_soldiers", ":died_enemy_population", "$g_strength_contribution_of_player"),
    (store_div, ":faction_morale_change", ":killed_enemies_by_our_soldiers", 8), #each 8 killed agent with any faction decreases morale of troops belong to that faction in our party by 1.
    (try_begin),
      (gt, ":faction_morale_change", 2000),
      (assign, ":faction_morale_change", 2000),
    (try_end),    
    
    (try_begin), #here we give positive morale to our troops of with same faction of ally party with 2/3x multipication.
      (ge, "$g_ally_party", 0),

      (store_div, ":ally_faction_morale_change", ":faction_morale_change", 3), #2/3x multipication (less than normal)
      (val_mul, ":ally_faction_morale_change", 2),
      (store_faction_of_party, ":ally_faction", "$g_ally_party"),
      (faction_get_slot, ":faction_morale", ":ally_faction",  slot_faction_morale_of_player_troops),
      (val_add, ":faction_morale", ":ally_faction_morale_change"),
      (faction_set_slot, ":ally_faction",  slot_faction_morale_of_player_troops, ":faction_morale"),
    (try_end),
    
    (try_begin), #here we give positive morale to our troops of owner of rescued village's faction after saving village from bandits by x3 bonus.
      (neg|party_is_active, "$g_enemy_party"),
      (ge, "$current_town", 0),
      
      (val_mul, ":faction_morale_change", 2), #2x bonus (more than normal)
      (store_faction_of_party, ":ally_faction", "$current_town"),
      (faction_get_slot, ":faction_morale", ":ally_faction",  slot_faction_morale_of_player_troops),
      (val_add, ":faction_morale", ":faction_morale_change"),
      (faction_set_slot, ":ally_faction",  slot_faction_morale_of_player_troops, ":faction_morale"),
    (else_try),
      (party_is_active, "$g_enemy_party"),
      (assign, ":currently_in_rebellion", 0),    
      (try_begin),
        (eq, "$players_kingdom", "fac_player_supporters_faction"),
        (neg|faction_slot_eq, "fac_player_supporters_faction", slot_faction_leader, "trp_player"),
        (assign, ":currently_in_rebellion", 1),
      (try_end),     
      (eq, ":currently_in_rebellion", 0),

      (store_div, ":faction_morale_change", ":faction_morale_change", 3), #2/3x multipication (less than normal)
      (val_mul, ":faction_morale_change", 2),
      (store_faction_of_party, ":enemy_faction", "$g_enemy_party"),
      (faction_get_slot, ":faction_morale", ":enemy_faction",  slot_faction_morale_of_player_troops),
      (val_sub, ":faction_morale", ":faction_morale_change"),
      (faction_set_slot, ":enemy_faction",  slot_faction_morale_of_player_troops, ":faction_morale"),
    (try_end),
        
  ]),
  ("print_casualties_to_s0",
    [(store_script_param, ":party_no", 1),
     (store_script_param, ":use_comma", 2),
     (str_clear, s0),
     (assign, ":total_reported", 0),
     (assign, ":total_wounded", 0),
     (assign, ":total_killed", 0),
     (assign, ":total_routed", 0),
     (party_get_num_companion_stacks, ":num_stacks",":party_no"),
     (try_for_range, ":i_stack", 0, ":num_stacks"),
       (party_stack_get_troop_id, ":stack_troop_id", ":party_no", ":i_stack"),
       (party_stack_get_size, ":stack_size", ":party_no", ":i_stack"),
       (party_stack_get_num_wounded, ":num_wounded", ":party_no", ":i_stack"),
       #get number of routed agent numbers
       (try_begin),
         (this_or_next|eq, ":party_no", "p_main_party"),
         (eq, ":party_no", "p_player_casualties"),     
         (troop_get_slot, ":num_routed", ":stack_troop_id", slot_troop_player_routed_agents),
         (troop_set_slot, ":stack_troop_id", slot_troop_player_routed_agents, 0),
       (else_try),
         (party_get_attached_to, ":attached_to", ":party_no"),
         (this_or_next|eq, ":party_no", "p_ally_casualties"),     
         (ge, ":attached_to", 0), 
         (this_or_next|eq, ":party_no", "p_ally_casualties"),     
         (eq, ":attached_to", "p_main_party"),
         (troop_get_slot, ":num_routed", ":stack_troop_id", slot_troop_ally_routed_agents),
         (troop_set_slot, ":stack_troop_id", slot_troop_ally_routed_agents, 0),
       (else_try),
         (troop_get_slot, ":num_routed", ":stack_troop_id", slot_troop_enemy_routed_agents),
         (troop_set_slot, ":stack_troop_id", slot_troop_enemy_routed_agents, 0),
       (try_end),                
       (store_sub, ":num_killed", ":stack_size", ":num_wounded"),
       (val_sub, ":num_killed", ":num_routed"),
       (val_add, ":total_killed", ":num_killed"),
       (val_add, ":total_wounded", ":num_wounded"),
       (val_add, ":total_routed", ":num_routed"),     
       (try_begin),
         (this_or_next|gt, ":num_killed", 0),
         (this_or_next|gt, ":num_wounded", 0),
         (gt, ":num_routed", 0),     
         (store_add, reg3, ":num_killed", ":num_wounded"),
         (store_add, reg3, reg3, ":num_routed"),
         (str_store_troop_name_by_count, s1, ":stack_troop_id", reg3),
         (try_begin),
           (troop_is_hero, ":stack_troop_id"),
           (assign, reg3, 0),
         (try_end),
         (try_begin), #there are people who killed, wounded and routed.
           (gt, ":num_killed", 0),
           (gt, ":num_wounded", 0),
           (gt, ":num_routed", 0),
           (assign, reg4, ":num_killed"),
           (assign, reg5, ":num_wounded"),
           (assign, reg6, ":num_routed"),
           (str_store_string, s2, "str_reg4_killed_reg5_wounded_reg6_routed"),
         (else_try), #there are people who killed and routed.
           (gt, ":num_killed", 0),
           (gt, ":num_routed", 0),
           (assign, reg4, ":num_killed"),
           (assign, reg5, ":num_routed"),
           (str_store_string, s2, "str_reg4_killed_reg5_routed"),     
         (else_try), #there are people who killed and wounded.
           (gt, ":num_killed", 0),
           (gt, ":num_wounded", 0),
           (assign, reg4, ":num_killed"),
           (assign, reg5, ":num_wounded"),
           (str_store_string, s2, "str_reg4_killed_reg5_wounded"),     
         (else_try), #there are people who wounded and routed.
           (gt, ":num_wounded", 0),
           (gt, ":num_routed", 0),
           (assign, reg4, ":num_wounded"),
           (assign, reg5, ":num_routed"),
           (str_store_string, s2, "str_reg4_wounded_reg5_routed"),
         (else_try), #there are people who only killed.
           (gt, ":num_killed", 0),
           (assign, reg1, ":num_killed"),
           (str_store_string, s3, "@killed"),
           (str_store_string, s2, "str_reg1_blank_s3"),
         (else_try), #there are people who only wounded.
           (gt, ":num_wounded", 0),
           (assign, reg1, ":num_wounded"),
           (str_store_string, s3, "@wounded"),
           (str_store_string, s2, "str_reg1_blank_s3"),
         (else_try), #there are people who only routed.
           (assign, reg1, ":num_routed"),
           (str_store_string, s3, "str_routed"),
           (str_store_string, s2, "str_reg1_blank_s3"),
         (try_end),
         (try_begin),
           (eq, ":use_comma", 1),
           (try_begin),
             (eq, ":total_reported", 0),
             (str_store_string, s0, "@{!}{reg3?{reg3}:} {s1} ({s2})"),
           (else_try),
             (str_store_string, s0, "@{!}{s0}, {reg3?{reg3}:} {s1} ({s2})"),
           (try_end),
         (else_try),
           (str_store_string, s0, "@{!}{s0}^{reg3?{reg3}:} {s1} ({s2})"),
         (try_end),
         (val_add, ":total_reported", 1),
       (try_end),
     (try_end),
     (try_begin),
       (this_or_next|gt, ":total_killed", 0),
       (this_or_next|gt, ":total_wounded", 0),
       (gt, ":total_routed", 0),
       (store_add, ":total_agents", ":total_killed", ":total_wounded"),
       (val_add, ":total_agents", ":total_routed"),
       (assign, reg3, ":total_agents"),
       (try_begin),
         (gt, ":total_killed", 0),
         (gt, ":total_wounded", 0),
         (gt, ":total_routed", 0),
         (assign, reg4, ":total_killed"),
         (assign, reg5, ":total_wounded"),
         (assign, reg6, ":total_routed"),
         (str_store_string, s2, "str_reg4_killed_reg5_wounded_reg6_routed"),
       (else_try),
         (gt, ":total_killed", 0),
         (gt, ":total_routed", 0),
         (assign, reg4, ":total_killed"),
         (assign, reg5, ":total_routed"),
         (str_store_string, s2, "str_reg4_killed_reg5_routed"),
       (else_try),
         (gt, ":total_killed", 0),
         (gt, ":total_wounded", 0),
         (assign, reg4, ":total_killed"),
         (assign, reg5, ":total_wounded"),
         (str_store_string, s2, "str_reg4_killed_reg5_wounded"),
       (else_try),
         (gt, ":total_wounded", 0),
         (gt, ":total_routed", 0),
         (assign, reg4, ":total_wounded"),
         (assign, reg5, ":total_routed"),
         (str_store_string, s2, "str_reg4_wounded_reg5_routed"),
       (else_try),
         (gt, ":total_killed", 0),
         (str_store_string, s2, "@killed"),
       (else_try),
         (gt, ":total_wounded", 0),
         (str_store_string, s2, "@wounded"),
       (else_try),
         (str_store_string, s2, "str_routed"),
       (else_try),
       (try_end),
       (str_store_string, s0, "@{s0}^TOTAL: {reg3} ({s2})"),
     (else_try),
       (try_begin),
         (eq, ":use_comma", 1),
         (str_store_string, s0, "@None"),
       (else_try),
         (str_store_string, s0, "@^None"),
       (try_end),
     (try_end),
  ]),
  #script_write_fit_party_members_to_stack_selection
  # INPUT:
  # param1: party_no, exclude_leader
  #OUTPUT:
  # trp_stack_selection_amounts slots (slot 0 = number of stacks, 1 = number of men fit, 2..n = stack sizes (fit))
  # trp_stack_selection_ids slots (2..n = stack troops)
  ("write_fit_party_members_to_stack_selection",
   [
     (store_script_param, ":party_no", 1),
     (store_script_param, ":exclude_leader", 2),
     (party_get_num_companion_stacks, ":num_stacks", ":party_no"),
     (assign, ":slot_index", 2),
     (assign, ":total_fit", 0),
     (try_for_range, ":stack_index", 0, ":num_stacks"),
       (party_stack_get_troop_id, ":stack_troop", ":party_no", ":stack_index"),
       (assign, ":num_fit", 0),
       (try_begin),
         (troop_is_hero, ":stack_troop"),
         (try_begin),
           (neg|troop_is_wounded, ":stack_troop"),
           (this_or_next|eq, ":exclude_leader", 0),
           (neq, ":stack_index", 0),
           (assign, ":num_fit",1),
         (try_end),
       (else_try),
         (party_stack_get_size, ":num_fit", ":party_no", ":stack_index"),
         (party_stack_get_num_wounded, ":num_wounded", ":party_no", ":stack_index"),
         (val_sub, ":num_fit", ":num_wounded"),
       (try_end),
       (try_begin),
         (gt, ":num_fit", 0),
         (troop_set_slot, "trp_stack_selection_amounts", ":slot_index", ":num_fit"),
         (troop_set_slot, "trp_stack_selection_ids", ":slot_index", ":stack_troop"),
         (val_add, ":slot_index", 1),
       (try_end),
       (val_add, ":total_fit", ":num_fit"),
     (try_end),
     (val_sub, ":slot_index", 2),
     (troop_set_slot, "trp_stack_selection_amounts", 0, ":slot_index"),
     (troop_set_slot, "trp_stack_selection_amounts", 1, ":total_fit"),
    ]),
  #script_remove_fit_party_member_from_stack_selection
  # INPUT:
  # param1: slot_index
  #OUTPUT:
  # reg0 = troop_no
  # trp_stack_selection_amounts slots (slot 0 = number of stacks, 1 = number of men fit, 2..n = stack sizes (fit))
  # trp_stack_selection_ids slots (2..n = stack troops)
  ("remove_fit_party_member_from_stack_selection",
   [
     (store_script_param, ":slot_index", 1),
     (val_add, ":slot_index", 2),
     (troop_get_slot, ":amount", "trp_stack_selection_amounts", ":slot_index"),
     (troop_get_slot, ":troop_no", "trp_stack_selection_ids", ":slot_index"),
     (val_sub, ":amount", 1),
     (troop_set_slot, "trp_stack_selection_amounts", ":slot_index", ":amount"),
     (troop_get_slot, ":total_amount", "trp_stack_selection_amounts", 1),
     (val_sub, ":total_amount", 1),
     (troop_set_slot, "trp_stack_selection_amounts", 1, ":total_amount"),
     (try_begin),
       (le, ":amount", 0),
       (troop_get_slot, ":num_slots", "trp_stack_selection_amounts", 0),
       (store_add, ":end_cond", ":num_slots", 2),
       (store_add, ":begin_cond", ":slot_index", 1),
       (try_for_range, ":index", ":begin_cond", ":end_cond"),
         (store_sub, ":prev_index", ":index", 1),
         (troop_get_slot, ":value", "trp_stack_selection_amounts", ":index"),
         (troop_set_slot, "trp_stack_selection_amounts", ":prev_index", ":value"),
         (troop_get_slot, ":value", "trp_stack_selection_ids", ":index"),
         (troop_set_slot, "trp_stack_selection_ids", ":prev_index", ":value"),
       (try_end),
       (val_sub, ":num_slots", 1),
       (troop_set_slot, "trp_stack_selection_amounts", 0, ":num_slots"),
     (try_end),
     (assign, reg0, ":troop_no"),
    ]),
  #script_remove_random_fit_party_member_from_stack_selection
  # INPUT:
  # none
  #OUTPUT:
  # reg0 = troop_no
  # trp_stack_selection_amounts slots (slot 0 = number of stacks, 1 = number of men fit, 2..n = stack sizes (fit))
  # trp_stack_selection_ids slots (2..n = stack troops)
  ("remove_random_fit_party_member_from_stack_selection",
   [
     (troop_get_slot, ":total_amount", "trp_stack_selection_amounts", 1),
     (store_random_in_range, ":random_troop", 0, ":total_amount"),
     (troop_get_slot, ":num_slots", "trp_stack_selection_amounts", 0),
     (store_add, ":end_cond", ":num_slots", 2),
     (try_for_range, ":index", 2, ":end_cond"),
       (troop_get_slot, ":amount", "trp_stack_selection_amounts", ":index"),
       (val_sub, ":random_troop", ":amount"),
       (lt, ":random_troop", 0),
       (assign, ":end_cond", 0),
       (store_sub, ":slot_index", ":index", 2),
     (try_end),
     (call_script, "script_remove_fit_party_member_from_stack_selection", ":slot_index"),
    ]),
  #script_add_routed_party
  #INPUT: none
  #OUTPUT: none
  ("add_routed_party",
   [                
     (party_get_num_companion_stacks, ":num_stacks", "p_routed_enemies"), #question, I changed (total_enemy_casualties) with (p_routed_enemies) because this is not prisoner in p_routed_enemies party.        
     (assign, ":num_regulars", 0),
     (assign, ":deleted_stacks", 0),
     (try_for_range, ":stack_no", 0, ":num_stacks"),
       (store_sub, ":difference", ":num_stacks", ":stack_no"),
       (ge, ":difference", ":deleted_stacks"),
       (store_sub, ":stack_no_minus_deleted", ":stack_no", ":deleted_stacks"),
       (party_stack_get_troop_id, ":stack_troop", "p_routed_enemies", ":stack_no_minus_deleted"), 
       (try_begin),
         (troop_is_hero, ":stack_troop"),
         (party_stack_get_size, ":stack_size", "p_routed_enemies", ":stack_no_minus_deleted"),
         (party_remove_members, "p_routed_enemies", ":stack_troop", 1),              
         (try_begin), 
           (le, ":stack_size", 1),
           (val_add, ":deleted_stacks", 1), #if deleted hero is the only one in his troop, now we have one less stacks
         (try_end),
       (else_try),
         (val_add, ":num_regulars", 1),
       (try_end),
     (try_end),

     #add new party to map if there is at least one routed agent. (new party name : routed_party, template : routed_warriors)
     (try_begin),
       (ge, ":num_regulars", 1),
     
       (set_spawn_radius, 2),
       (spawn_around_party, "p_main_party", "pt_routed_warriors"),
       (assign, ":routed_party", reg0),
     
       (party_set_slot, ":routed_party", slot_party_commander_party, -1), #we need this because 0 is player's party!

       (assign, ":max_routed_agents", 0),
       (assign, ":routed_party_faction", "fac_neutral"),
       (try_for_range, ":cur_faction", fac_kingdom_1, fac_kingdoms_end),
         (faction_get_slot, ":num_routed_agents_in_this_faction", ":cur_faction", slot_faction_num_routed_agents),
         (gt, ":num_routed_agents_in_this_faction", ":max_routed_agents"),
         (assign, ":max_routed_agents", ":num_routed_agents_in_this_faction"),
         (assign, ":routed_party_faction", ":cur_faction"),
       (try_end),
       
       (party_set_faction, ":routed_party", ":routed_party_faction"),

       (party_set_ai_behavior, ":routed_party", ai_bhvr_travel_to_party),

       (assign, ":minimum_distance", 1000000),
       (try_for_parties, ":party_no"),
         (party_is_active, ":party_no"),
         (party_get_slot, ":cur_party_type", ":party_no", slot_party_type),
         (this_or_next|eq, ":cur_party_type", spt_town),
         (eq, ":cur_party_type", spt_castle),
         (store_faction_of_party, ":cur_faction", ":party_no"),
         (this_or_next|eq, ":routed_party_faction", "fac_neutral"),
         (eq, ":cur_faction", ":routed_party_faction"),
         (party_get_position, pos1, ":party_no"),
         (store_distance_to_party_from_party, ":dist", ":party_no", "p_main_party"),
         (try_begin),
           (lt, ":dist", ":minimum_distance"),
           (assign, ":minimum_distance", ":dist"),
           (assign, ":nearest_ally_city", ":party_no"),
         (try_end),
       (try_end),     

       (party_get_position, pos1, "p_main_party"), #store position information of main party in pos1
       (party_get_position, pos2, ":nearest_ally_city"), #store position information of target city in pos2

       (assign, ":minimum_distance", 1000000),
       (try_for_range, ":unused", 0, 10),
         (map_get_random_position_around_position, pos3, pos1, 2), #store position of found random position (possible placing position for new routed party) around battle position in pos3
         (get_distance_between_positions, ":dist", pos2, pos3), #store distance between found position and target city in ":dist".
         (try_begin),
           (lt, ":dist", ":minimum_distance"),
           (assign, ":minimum_distance", ":dist"),
           (copy_position, pos63, pos3), 
         (try_end),
       (end_try),
     
       (party_set_position, ":routed_party", pos63),

       (party_set_ai_object, ":routed_party", ":nearest_ally_city"),
       (party_set_flags, ":routed_party", pf_default_behavior, 1),

       #adding party members of p_routed_enemies to routed_party
       (party_clear, ":routed_party"),
       (party_get_num_companion_stacks, ":num_stacks", "p_routed_enemies"), #question, I changed (total_enemy_casualties) with (p_routed_enemies) because this is not prisoner in p_routed_enemies party.
       (try_for_range, ":stack_no", 0, ":num_stacks"),
         (party_stack_get_troop_id, ":stack_troop", "p_routed_enemies", ":stack_no"),          
         (try_begin),
           (neg|troop_is_hero, ":stack_troop"), #do not add routed heroes to (new created) routed party for now.

           (party_stack_get_size, ":stack_size", "p_routed_enemies", ":stack_no"),
           (party_add_members, ":routed_party", ":stack_troop", ":stack_size"),
         (try_end),
       (try_end),
     (try_end),
    ]),
  ("party_count_fit_regulars",
    [
      (store_script_param_1, ":party"), #Party_id
      (party_get_num_companion_stacks, ":num_stacks", ":party"),
      (assign, reg0, 0),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop", ":party", ":i_stack"),
        (neg|troop_is_hero, ":stack_troop"),
        (party_stack_get_size, ":stack_size",":party",":i_stack"),
        (party_stack_get_num_wounded, ":num_wounded",":party",":i_stack"),
        (val_sub, ":stack_size", ":num_wounded"),
        (val_add, reg0, ":stack_size"),
      (try_end),
  ]),
  #script_party_count_fit_for_battle:
  # Returns the number of unwounded companions in a party
  # INPUT:
  # param1: Party-id
  # OUTPUT: reg0 = result
  ("party_count_fit_for_battle",
    [
      (store_script_param_1, ":party"), #Party_id
      (party_get_num_companion_stacks, ":num_stacks",":party"),
      (assign, reg0, 0),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop",":party",":i_stack"),
        (assign, ":num_fit",0),
        (try_begin),
          (troop_is_hero, ":stack_troop"),
          (try_begin),
            (neg|troop_is_wounded, ":stack_troop"),
            (assign, ":num_fit", 1),
          (try_end),
        (else_try),
          (party_stack_get_size, ":num_fit",":party",":i_stack"),
          (party_stack_get_num_wounded, ":num_wounded",":party",":i_stack"),
          (val_sub, ":num_fit", ":num_wounded"),
        (try_end),
        (val_add, reg0, ":num_fit"),
      (try_end),
  ]),
  #script_party_count_members_with_full_health
  # Returns the number of unwounded regulars, and heroes other than player with 100% hitpoints in a party
  # INPUT:
  # param1: Party-id
  # OUTPUT: reg0 = result
  ("party_count_members_with_full_health",
    [
      (store_script_param_1, ":party"), #Party_id
      (party_get_num_companion_stacks, ":num_stacks",":party"),
      (assign, reg0, 0),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop",":party",":i_stack"),
        (neq, ":stack_troop", "trp_player"),
        (assign, ":num_fit",0),
        (try_begin),
          (troop_is_hero, ":stack_troop"),
          (store_troop_health, ":troop_hp", ":stack_troop"),
          (try_begin),
            (ge, ":troop_hp", 80),
            (assign, ":num_fit",1),
          (try_end),
        (else_try),
          (party_stack_get_size, ":num_fit",":party",":i_stack"),
          (party_stack_get_num_wounded, ":num_wounded",":party",":i_stack"),
          (val_sub, ":num_fit", ":num_wounded"),
          (val_max, ":num_fit", 0),
        (try_end),
        (val_add, reg0, ":num_fit"),
      (try_end),
  ]),
  ("get_stack_with_rank",
    [
      (store_script_param_1, ":party"), #Party_id
      (store_script_param_2, ":rank"), #Rank
      (party_get_num_companion_stacks, ":num_stacks",":party"),
      (assign, reg(0), -1),
      (assign, ":num_total", 0),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (eq, reg(0), -1), #continue only if we haven't found the result yet.
        (party_stack_get_troop_id,     ":stack_troop",":party",":i_stack"),
        (neg|troop_is_hero, ":stack_troop"),
        (party_stack_get_size,         ":stack_size",":party",":i_stack"),
        (party_stack_get_num_wounded,  ":num_wounded",":party",":i_stack"),
        (val_sub, ":stack_size", ":num_wounded"),
        (val_add, ":num_total", ":stack_size"),
        (try_begin),
          (lt, ":rank", ":num_total"),
          (assign, reg(0), ":i_stack"),
        (try_end),
      (try_end),
  ]),
  ("inflict_casualties_to_party",
    [
      (party_clear, "p_temp_casualties"),
      (store_script_param_1, ":party"), #Party_id
      (call_script, "script_party_count_fit_regulars", ":party"),
      (assign, ":num_fit", reg(0)), #reg(47) = number of fit regulars.
      (store_script_param_2, ":num_attack_rounds"), #number of attacks
      (try_for_range, ":unused", 0, ":num_attack_rounds"),
        (gt, ":num_fit", 0),
        (store_random_in_range, ":attacked_troop_rank", 0 , ":num_fit"), #attack troop with rank reg(46)
        (assign, reg1, ":attacked_troop_rank"),
        (call_script, "script_get_stack_with_rank", ":party", ":attacked_troop_rank"),
        (assign, ":attacked_stack", reg(0)), #reg(53) = stack no to attack.
        (party_stack_get_troop_id,     ":attacked_troop",":party",":attacked_stack"),
        (store_character_level, ":troop_toughness", ":attacked_troop"),
        (val_add, ":troop_toughness", 5),  #troop-toughness = level + 5
        (assign, ":casualty_chance", 10000),
        (val_div, ":casualty_chance", ":troop_toughness"), #dying chance
        (try_begin),
          (store_random_in_range, ":rand_num", 0 ,10000),
          (lt, ":rand_num", ":casualty_chance"), #check chance to be a casualty
          (store_random_in_range, ":rand_num2", 0, 2), #check if this troop will be wounded or killed
          (try_begin),
            (troop_is_hero,":attacked_troop"), #currently troop can't be a hero, but no harm in keeping this.
            (store_troop_health, ":troop_hp",":attacked_troop"),
            (val_sub, ":troop_hp", 45),
            (val_max, ":troop_hp", 1),
            (troop_set_health, ":attacked_troop", ":troop_hp"),
          (else_try),
            (lt, ":rand_num2", 1), #wounded
            (party_add_members, "p_temp_casualties", ":attacked_troop", 1),
            (party_wound_members, "p_temp_casualties", ":attacked_troop", 1),
            (party_wound_members, ":party", ":attacked_troop", 1),
          (else_try), #killed
            (party_add_members, "p_temp_casualties", ":attacked_troop", 1),
            (party_remove_members, ":party", ":attacked_troop", 1),
          (try_end),
          (val_sub, ":num_fit", 1), #adjust number of fit regulars.
        (try_end),
      (try_end),
  ]),
  #OUTPUT:
  # This script doesn't return a value but moves some of the members of source party to target party according to the given ratio.
  ("move_members_with_ratio",
    [
      (store_script_param_1, ":source_party"), #Source Party_id
      (store_script_param_2, ":target_party"), #Target Party_id
      (party_get_num_prisoner_stacks, ":num_stacks",":source_party"),
      (try_for_range_backwards, ":stack_no", 0, ":num_stacks"),
        (party_prisoner_stack_get_troop_id,     ":stack_troop",":source_party",":stack_no"),
        (party_prisoner_stack_get_size,    ":stack_size",":source_party",":stack_no"),
        (store_mul, ":number_to_move",":stack_size","$pin_number"),
        (val_div, ":number_to_move", 1000),
        (party_remove_prisoners, ":source_party", ":stack_troop", ":number_to_move"),
        (assign, ":number_moved", reg0),
        (party_add_prisoners, ":target_party", ":stack_troop", ":number_moved"),
      (try_end),
      (party_get_num_companion_stacks, ":num_stacks",":source_party"),
      (try_for_range_backwards, ":stack_no", 0, ":num_stacks"),
        (party_stack_get_troop_id,     ":stack_troop",":source_party",":stack_no"),
        (party_stack_get_size,    ":stack_size",":source_party",":stack_no"),
        (store_mul, ":number_to_move",":stack_size","$pin_number"),
        (val_div, ":number_to_move", 1000),
        (party_remove_members, ":source_party", ":stack_troop", ":number_to_move"),
        (assign, ":number_moved", reg0),
        (party_add_members, ":target_party", ":stack_troop", ":number_moved"),
      (try_end),
  ]),
  # script_shuffle_troop_slots:
  # Shuffles a range of slots of a given troop.
  # Used for exploiting a troop as an array.
  # Input: arg1 = troop_no, arg2 = slot_begin, arg3 = slot_end
  ("shuffle_troop_slots",
    [
      (store_script_param, ":troop_no", 1),
      (store_script_param, ":slots_begin", 2),
      (store_script_param, ":slots_end", 3),
      (try_for_range, ":cur_slot_no", ":slots_begin", ":slots_end"),
        (store_random_in_range, ":random_slot_no", ":slots_begin", ":slots_end"), #reg(58) = random slot. Now exchange slots reg(57) and reg(58)
        (troop_get_slot, ":cur_slot_value", ":troop_no", ":cur_slot_no"), #temporarily store the value in slot reg(57) in reg(59)
        (troop_get_slot, ":random_slot_value", ":troop_no", ":random_slot_no"), #temporarily store the value in slot reg(58) in reg(60)
        (troop_set_slot, ":troop_no", ":cur_slot_no", ":random_slot_value"), # Now exchange the two...
        (troop_set_slot, ":troop_no", ":random_slot_no", ":cur_slot_value"),
      (try_end),
  ]),
  # script_print_party_members
  # Input: arg1 = party_no
  # Output: s51 = output string. "noone" if the party is empty
  ("print_party_members",
    [  
      (store_script_param_1, ":party_no"),
      (party_get_num_companion_stacks, ":num_stacks", ":party_no"),
      (assign, reg10, ":num_stacks"),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop",":party_no",":i_stack"),
        (troop_is_hero, ":stack_troop"),
        (try_begin),
          (eq, ":i_stack", 0),
          (str_store_troop_name, s51, ":stack_troop"),
        (try_end),
        (str_store_troop_name, s52, ":stack_troop"),
        (try_begin),
          (eq, ":i_stack", 1),
          (str_store_string, s51, "str_s52_and_s51"),
        (else_try),
          (gt, ":i_stack", 1),
          (str_store_string, s51, "str_s52_comma_s51"),
        (try_end),
      (try_end),
      (try_begin),
        (eq, ":num_stacks", 0),
        (str_store_string, s51, "str_noone"),
      (try_end),
  ]),
  # script_consume_food
  # Input: arg1: order of the food to be consumed
  # Output: none
  ("consume_food",
   [(store_script_param, ":selected_food", 1),
    (troop_get_inventory_capacity, ":capacity", "trp_player"),
    (try_for_range, ":cur_slot", 0, ":capacity"),
      (troop_get_inventory_slot, ":cur_item", "trp_player", ":cur_slot"),
      (is_between, ":cur_item", food_begin, food_end),
      (troop_get_inventory_slot_modifier, ":item_modifier", "trp_player", ":cur_slot"),
      (neq, ":item_modifier", imod_rotten),
      (item_slot_eq, ":cur_item", slot_item_is_checked, 0),
      (item_set_slot, ":cur_item", slot_item_is_checked, 1),
      (val_sub, ":selected_food", 1),
      (lt, ":selected_food", 0),
      (assign, ":capacity", 0),
      (troop_inventory_slot_get_item_amount, ":cur_amount", "trp_player", ":cur_slot"),
      (val_sub, ":cur_amount", 1),
      (troop_inventory_slot_set_item_amount, "trp_player", ":cur_slot", ":cur_amount"),
    (try_end),
    ]),
  #script_upgrade_hero_party
  # INPUT: arg1 = party_id, arg2 = xp_amount
  ("upgrade_hero_party",
    [
      (store_script_param, ":party_no", 1),
      (store_script_param, ":xp_amount", 2),
      ##diplomacy start+
      #Take into account faction quality/quantity settings.  Do not apply this
      #to the player party or to special parties.
      (try_begin),
        (ge, ":party_no", spawn_points_begin),
        (store_faction_of_party, ":var1", ":party_no"),
        (faction_get_slot, ":var1", ":var1", dplmc_slot_faction_quality),
        (val_add, ":var1", 100),
        (val_clamp, ":var1", 97, 104),#100 plus or minus three percent
        (val_mul, ":xp_amount", ":var1"),
        (val_div, ":xp_amount", 100),
      (try_end),
       ##diplomacy end+
      (party_upgrade_with_xp, ":party_no", ":xp_amount", 0),
    ]),
  #script_get_troop_item_amount
  # INPUT: arg1 = troop_no, arg2 = item_no
  # OUTPUT: reg0 = item_amount
  ("get_troop_item_amount",
    [(store_script_param, ":troop_no", 1),
     (store_script_param, ":item_no", 2),
     (troop_get_inventory_capacity, ":inv_cap", ":troop_no"),
     (assign, ":count", 0),
     (try_for_range, ":i_slot", 0, ":inv_cap"),
       (troop_get_inventory_slot, ":cur_item", ":troop_no", ":i_slot"),
       (eq, ":cur_item", ":item_no"),
       (val_add, ":count", 1),
     (try_end),
     (assign, reg0, ":count"),
     ]),
  #script_troop_add_gold
  # INPUT: arg1 = troop_no, arg2 = amount
  # OUTPUT: none
  ("troop_add_gold",
    [
      (store_script_param, ":troop_no", 1),
      (store_script_param, ":amount", 2),
      
      (troop_add_gold, ":troop_no", ":amount"),
      (try_begin),
        (eq, ":troop_no", "trp_player"),
        (play_sound, "snd_money_received"),
      (try_end),
     ]),
	("party_inflict_attrition", #parameters from dialog
	[
	(store_script_param, ":party", 1),
	(store_script_param, ":attrition_rate", 2),
#	(store_script_param, ":attrition_type", 3), #1 = desertion, 2 = sickness
##diplomacy start+
	(store_script_param, ":unused", 3), #1 = desertion, 2 = sickness
##diplomacy end+

    (party_clear, "p_temp_casualties"),

	(party_get_num_companion_stacks, ":num_stacks", ":party"),

	#add to temp casualties
	(try_for_range, ":stack", 0, ":num_stacks"),
		(party_stack_get_troop_id, ":troop_type", ":party", ":stack"),
		(neg|troop_is_hero, ":troop_type"),
		(party_stack_get_size, ":size", ":party", ":stack"),
		(store_mul, ":casualties_x_100", ":attrition_rate", ":size"),
		(store_div, ":casualties", ":casualties_x_100", 100),
		(party_add_members, "p_temp_casualties", ":troop_type", ":casualties"),
		
		(store_mul, ":subtractor", ":casualties", 100),
		(store_sub, ":chance_of_additional_casualty", ":casualties_x_100", ":subtractor"),
	
		(try_begin),
			(gt, ":chance_of_additional_casualty", 0),
			(store_random_in_range, ":random", 0, 100),
			(lt, ":random", ":chance_of_additional_casualty"),
			(party_add_members, "p_temp_casualties", ":troop_type", ":casualties"),
		(try_end),

#		(try_begin),
#			(eq, "$cheat_mode", 1),
#			(str_store_party_name, s7, ":party"),
#           		...
#		(try_end),
	(try_end),
	
	#take temp casualties from main party
	(party_get_num_companion_stacks, ":num_stacks", "p_temp_casualties"),

	#add to temp casualties
	(try_for_range, ":stack", 0, ":num_stacks"),
		(party_stack_get_troop_id, ":troop_type", "p_temp_casualties", ":stack"),
		(party_stack_get_size, ":size", "p_temp_casualties", ":stack"),
		(party_remove_members, ":party", ":troop_type", ":size"),
		
		(eq, "$cheat_mode", 1),
		(assign, reg3, ":size"),
		(str_store_troop_name, s4, ":troop_type"),
		(str_store_party_name, s5, ":party"),
#		(display_message, "str_s5_suffers_attrition_reg3_x_s4"), 
		(str_store_string, s65, "str_s5_suffers_attrition_reg3_x_s4"), 
		(display_message, "str_s65"),
		(try_begin),
			(eq, "$debug_message_in_queue", 0),
			(call_script, "script_add_notification_menu", "mnu_debug_alert_from_s65", 0, 0),
			(assign, "$debug_message_in_queue", 1),
		(try_end),
	(try_end),
	
	]),
# script_game_troop_upgrades_button_clicked
  ("game_troop_upgrades_button_clicked",
  [
      (store_script_param, ":troop_no", 1),
      (assign, reg0, ":troop_no"),
      (start_presentation, "prsnt_upgrade_tree"),
  ]),
   ("troop_tree_recursive_backtracking",
    [
      (store_script_param, ":troop_no", 1),
      (store_script_param, ":cur_x", 2),
      (store_script_param, ":cur_y", 3),
      (store_script_param, ":offset_x", 4),
      
      (store_add, ":next_x", ":cur_x", ":offset_x"),
      # upgrade_troop
      (troop_get_upgrade_troop, ":upgrade_troop_1", ":troop_no", 0),
      (troop_get_upgrade_troop, ":upgrade_troop_2", ":troop_no", 1),
      (try_begin),
        (gt,  ":upgrade_troop_2", 0),
        (call_script, "script_troop_tree_recursive_backtracking", ":upgrade_troop_2", ":next_x", reg2, ":offset_x"),
        (assign, ":upgrade_troop_2_y", reg0),
        (val_add, reg2, 200), # current global y
        (call_script, "script_troop_tree_recursive_backtracking", ":upgrade_troop_1", ":next_x", reg2, ":offset_x"),
        (assign, ":upgrade_troop_1_y", reg0),
      (else_try),
        (gt,  ":upgrade_troop_1", 0),
        (call_script, "script_troop_tree_recursive_backtracking", ":upgrade_troop_1", ":next_x", reg2, ":offset_x"),
        (assign, ":upgrade_troop_1_y", reg0),
      (try_end),
      
      # troop_tree_line
      (try_begin),
        (gt,  ":upgrade_troop_2", 0),
        (store_add, reg0, ":upgrade_troop_1_y", ":upgrade_troop_2_y"),
        (val_div, reg0, 2),
        #               ---- upgrade_troop_1
        #              |
        # troop_no ----
        #              |
        #               ---- upgrade_troop_2
        (store_div, ":half_offset_x", ":offset_x", 2),
        (store_add, ":middle_x", ":cur_x", ":half_offset_x"),
        (call_script, "script_prsnt_line", ":half_offset_x", 4, ":cur_x", reg0, 0),
        (call_script, "script_prsnt_line", ":half_offset_x", 4, ":middle_x", ":upgrade_troop_1_y", 0),
        (call_script, "script_prsnt_line", ":half_offset_x", 4, ":middle_x", ":upgrade_troop_2_y", 0),
        (store_sub, ":size_y", ":upgrade_troop_1_y", ":upgrade_troop_2_y"),
        (val_add, ":size_y", 4),
        (call_script, "script_prsnt_line", 4, ":size_y", ":middle_x", ":upgrade_troop_2_y", 0),
      (else_try),
        (gt,  ":upgrade_troop_1", 0),
        (assign, reg0, ":upgrade_troop_1_y"),
        #
        # troop_no -------- upgrade_troop_1
        #
        (call_script, "script_prsnt_line", ":offset_x", 4, ":cur_x", ":upgrade_troop_1_y", 0),
      (else_try),
        (assign, reg0, ":cur_y"),
      (try_end),
      
      # troop name
      (str_store_troop_name, s1, ":troop_no"),
      (create_text_overlay, reg1, "@{s1}", tf_center_justify|tf_vertical_align_center|tf_double_space|tf_scrollable),
      (store_sub, ":name_x", ":cur_x", 50),
      (store_sub, ":name_y", reg0, 130),
      (position_set_x, pos1, ":name_x"),
      (position_set_y, pos1, ":name_y"),
      (overlay_set_position, reg1, pos1),
      (position_set_x, pos1, 100),
      (position_set_y, pos1, 60),
      (overlay_set_area_size, reg1, pos1),
      (position_set_x, pos1, 800),
      (position_set_y, pos1, 800),
      (overlay_set_size, reg1, pos1),
      
      # troop avatar (clickable button)
      (store_sub, ":avatar_x", ":cur_x", 75),
      (store_sub, ":avatar_y", reg0, 75),
      (store_mul, ":cur_troop", ":troop_no", 2), #with weapons
      (create_image_button_overlay_with_tableau_material, reg1, -1, "tableau_game_party_window", ":cur_troop"),
      (position_set_x, pos1, 450),
      (position_set_y, pos1, 600),
      (overlay_set_size, reg1, pos1),
      (position_set_x, pos1, ":avatar_x"),
      (position_set_y, pos1, ":avatar_y"),
      (overlay_set_position, reg1, pos1),
      
      # Store overlay ID and troop_no mapping for click handling
      (troop_set_slot, "trp_temp_array_c", reg1, ":troop_no"),
    ]),
########################################################
## Easy regulars upgrading kit begin by rubik 
########################################################
("calculate_upgrade_troops", 
  [
    (call_script, "script_party_copy", "p_temp_party", "p_main_party"), ## before
    ## upgrade all troops in first upgrade path with total 1 xp
    ## everyone get 0 xp at last, but they all upgraded
    (party_upgrade_with_xp, "p_main_party", 1, 1),
    (call_script, "script_party_copy", "p_temp_party_2", "p_main_party"), ## after
    
    ## remove prisoners and heroes
    (call_script, "script_party_remove_all_prisoners", "p_temp_party"),
    (call_script, "script_party_remove_all_prisoners", "p_temp_party_2"),
    (call_script, "script_party_remove_heroes", "p_temp_party"),
    (call_script, "script_party_remove_heroes", "p_temp_party_2"),
    
    ## Initialize trp_temp_array_a, trp_temp_array_b, trp_temp_array_c
    (try_for_range, ":slot_no", 0, 32),
      (troop_set_slot, "trp_temp_array_a", ":slot_no", -1),
      (troop_set_slot, "trp_temp_array_b", ":slot_no", 0),
      (troop_set_slot, "trp_temp_array_c", ":slot_no", 0),
    (try_end),
    
    (assign, ":slot_id", 0),
    (assign, ":num_times", 1),
    (try_for_range, ":unused", 0, ":num_times"),
      ## find all current root troops
      (party_get_num_companion_stacks, ":num_stacks", "p_temp_party"),
      (try_for_range, ":cur_stack", 0, ":num_stacks"),
        (party_stack_get_troop_id, ":cur_troop", "p_temp_party", ":cur_stack"),
        (troop_set_slot, ":cur_troop", slot_root_troop, 1),
      (try_end),
      
      (try_for_range, ":cur_stack", 0, ":num_stacks"),
        (party_stack_get_troop_id, ":cur_troop", "p_temp_party", ":cur_stack"),
        (troop_get_upgrade_troop, ":upgrade_troop", ":cur_troop", 0),
        (gt, ":upgrade_troop", 0),
        (call_script, "script_party_has_troop", "p_temp_party", ":upgrade_troop"),
        (eq, reg0, 1),
        (troop_set_slot, ":upgrade_troop", slot_root_troop, 0), ## not a root troop
      (try_end),
      
      ## calculate upgrade troops and upgrade size
      (try_for_range_backwards, ":cur_stack", 0, ":num_stacks"),
        (party_stack_get_troop_id, ":cur_troop", "p_temp_party", ":cur_stack"),
        (gt, ":cur_troop", 0),
        (troop_slot_eq, ":cur_troop", slot_root_troop, 1),
        (party_stack_get_size, ":stack_size", "p_temp_party", ":cur_stack"),
        
        (call_script, "script_party_has_troop", "p_temp_party_2", ":cur_troop"),
        (try_begin),
          (eq, reg0, 0),
          (assign, ":stack_size_2", 0),
        (else_try),
          (party_get_num_companion_stacks, ":num_stacks_2", "p_temp_party_2"),
          (try_for_range, ":cur_stack_2", 0, ":num_stacks_2"),
            (party_stack_get_troop_id, ":cur_troop_2", "p_temp_party_2", ":cur_stack_2"),
            (eq, ":cur_troop_2", ":cur_troop"),
            (party_stack_get_size, ":stack_size_2", "p_temp_party_2", ":cur_stack_2"),
          (try_end),
        (try_end),
        
        (try_begin),
          (val_sub, ":stack_size", ":stack_size_2"),
          (gt, ":stack_size", 0),
          ## reduce the first upgrade path size
          (troop_get_upgrade_troop, ":upgrade_troop", ":cur_troop", 0),
          (party_remove_members, "p_temp_party_2", ":upgrade_troop", ":stack_size"),
          ## reduce the first upgrade path size
          (troop_set_slot, "trp_temp_array_a", ":slot_id", ":cur_troop"), ## troop which can upgrade
          (troop_set_slot, "trp_temp_array_b", ":slot_id", ":stack_size"), ## troop upgrade size
          (troop_set_slot, "trp_temp_array_c", ":slot_id", 0), ## troop upgrade second path size
          (val_add, ":slot_id", 1),
        (try_end),
        
        ## remove current root troop
        (call_script, "script_party_remove_troop", "p_temp_party", ":cur_troop"),
        (call_script, "script_party_remove_troop", "p_temp_party_2", ":cur_troop"),
      (try_end),
      
      ## do the loop once more?
      (try_begin),
        (party_get_num_companion_stacks, ":num_stacks", "p_temp_party"),
        (gt, ":num_stacks", 0),
        (val_add, ":num_times", 1), ## once more
      (try_end),
    (try_end),
  ]),
("party_has_troop", 
  [
    (store_script_param_1, ":party_no"),
    (store_script_param_2, ":troop_no"),
    
    (assign, reg0, 0),
    (party_get_num_companion_stacks, ":num_stacks", ":party_no"),
    (try_for_range, ":cur_stack", 0, ":num_stacks"),
      (party_stack_get_troop_id, ":cur_troop", ":party_no", ":cur_stack"),
      (eq, ":cur_troop", ":troop_no"),
      (assign, reg0, 1),
      (assign, ":num_stacks", 0), #end the loop
    (try_end),
  ]),
("party_remove_troop", 
  [
    (store_script_param_1, ":party_no"),
    (store_script_param_2, ":troop_no"),
    
    (party_get_num_companion_stacks, ":num_stacks", ":party_no"),
    (try_for_range, ":cur_stack", 0, ":num_stacks"),
      (party_stack_get_troop_id, ":cur_troop", ":party_no", ":cur_stack"),
      (eq, ":cur_troop", ":troop_no"),
      (party_stack_get_size, ":stack_size", ":party_no", ":cur_stack"),
      (party_remove_members, ":party_no", ":troop_no", ":stack_size"),
    (try_end),
  ]),
("party_remove_heroes", 
  [
    (store_script_param_1, ":party_no"),
    
    (party_get_num_companion_stacks, ":num_stacks", ":party_no"),
    (try_for_range_backwards, ":cur_stack", 0, ":num_stacks"),
      (party_stack_get_troop_id, ":cur_troop", ":party_no", ":cur_stack"),
      (troop_is_hero, ":cur_troop"),
      (party_remove_members, ":party_no", ":cur_troop", 1),
    (try_end),
  ]),
("has_enough_slot", 
  [
    (party_clear, "p_temp_party"),
    (party_get_num_companion_stacks, ":num_stacks", "p_main_party"),
    (try_for_range, ":stack_no", 0, ":num_stacks"),
      (party_stack_get_troop_id, ":cur_troop", "p_main_party", ":stack_no"),
      (try_begin),
        (troop_get_upgrade_troop, ":upgraded_troop_1", ":cur_troop", 0),
        (gt, ":upgraded_troop_1", 0),
        (neg|main_party_has_troop, ":upgraded_troop_1"),
        (party_add_members, "p_temp_party", ":upgraded_troop_1", 1),
      (else_try),
        (troop_get_upgrade_troop, ":upgraded_troop_2", ":cur_troop", 1),
        (gt, ":upgraded_troop_2", 0),
        (neg|main_party_has_troop, ":upgraded_troop_2"),
        (party_add_members, "p_temp_party", ":upgraded_troop_2", 1),
      (try_end),
    (try_end),
    (store_num_free_stacks, ":free_stacks", "p_main_party"),
    (party_get_num_companion_stacks, ":num_stack_increase", "p_temp_party"),
    
    (try_begin),
      (ge, ":free_stacks", ":num_stack_increase"),
      (assign, reg0, 1),
    (else_try),
      (assign, reg0, 0),
    (try_end),
  ]),
]
