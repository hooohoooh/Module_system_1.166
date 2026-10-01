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

simple_triggers_dplmc = [
#Recruiter kit begin
## This trigger keeps the recruiters moving by assigning them targets.
 (0.5,
   [
   (try_for_parties, ":party_no"),
      (party_slot_eq,":party_no", slot_party_type, dplmc_spt_recruiter),

      (party_get_slot, ":needed", ":party_no", dplmc_slot_party_recruiter_needed_recruits),

      (party_get_num_companion_stacks, ":stacks", ":party_no"),
      (assign, ":destruction", 1),
      (assign, ":quit", 0),

      (try_for_range, ":stack_no", 0, ":stacks"),
         (party_stack_get_troop_id, ":troop_id", ":party_no", ":stack_no"),
         (eq, ":troop_id", "trp_dplmc_recruiter"),
         (assign, ":destruction",0),
      (try_end),
      (try_begin),
         (party_get_battle_opponent, ":opponent", ":party_no"),
         (lt, ":opponent", 0),
         (eq, ":destruction", 1),
         (party_get_slot, ":party_origin", ":party_no", dplmc_slot_party_recruiter_origin),
         (str_store_party_name_link, s13, ":party_origin"),
         (assign, reg10, ":needed"),
         (display_log_message, "@Your recruiter who was commissioned to recruit {reg10} recruits to {s13} has been defeated!", 0xFF0000),
         (remove_party, ":party_no"),
         (assign, ":quit", 1),
      (try_end),

      #waihti
      (try_begin),
        (eq, ":quit", 0),
        (party_get_slot, ":party_origin", ":party_no", dplmc_slot_party_recruiter_origin),
        (store_faction_of_party, ":origin_faction", ":party_origin"),
        (neq, ":origin_faction", "$players_kingdom"),
        (str_store_party_name_link, s13, ":party_origin"),
        (assign, reg10, ":needed"),
        (display_log_message, "@{s13} has been taken by the enemy and your recruiter who was commissioned to recruit {reg10} recruits vanished  without a trace!", 0xFF0000),
        (remove_party, ":party_no"),
        (assign, ":quit", 1),
      (try_end),
      #waihti

      (eq, ":quit", 0),

      (party_get_num_companions, ":amount", ":party_no"),
      (val_sub, ":amount", 1),   #the recruiter himself doesn't count.

   #daedalus begin
      (party_get_slot, ":recruit_faction", ":party_no", dplmc_slot_party_recruiter_needed_recruits_faction),
   #daedalus end
      (lt, ":amount", ":needed"),  #If the recruiter has less troops than player ordered, new village will be set as target.
      (try_begin),
         #(get_party_ai_current_behavior, ":ai_bhvr", ":party_no"),
         #(eq, ":ai_bhvr", ai_bhvr_hold),
         (get_party_ai_object, ":previous_target", ":party_no"),
         (get_party_ai_behavior, ":previous_behavior", ":party_no"),
         (try_begin),
            (neq, ":previous_behavior", ai_bhvr_hold),
            (neq, ":previous_target", -1),
            (party_set_slot, ":previous_target", dplmc_slot_village_reserved_by_recruiter, 0),
         (try_end),
         (assign, ":min_distance", 999999),
         (assign, ":closest_village", -1),
         (try_for_range, ":village", villages_begin, villages_end),
            (store_distance_to_party_from_party, ":distance", ":party_no", ":village"),
            (lt, ":distance", ":min_distance"),
            (try_begin),
               (store_faction_of_party, ":village_current_faction", ":village"),
               (assign, ":faction_relation", 100),
               (try_begin),
                  (neq, ":village_current_faction", "$players_kingdom"),    # faction relation will be checked only if the village doesn't belong to the player's current faction
                  (store_relation, ":faction_relation", "$players_kingdom", ":village_current_faction"),
               (try_end),
               (ge, ":faction_relation", 0),
               (party_get_slot, ":village_relation", ":village", slot_center_player_relation),
               (ge, ":village_relation", 0),
               (party_get_slot, ":volunteers_in_village", ":village", slot_center_volunteer_troop_amount),
               (gt, ":volunteers_in_village", 0),
            #daedalus begin
               (party_get_slot, ":village_faction", ":village", slot_center_original_faction),
               (assign,":stop",1),
               (try_begin),
                  (eq,":recruit_faction",-1),
                  (assign,":stop",0),
               (else_try),
                  (eq, ":village_faction", ":recruit_faction"),
                  (assign,":stop",0),
               (try_end),
               (neq,":stop",1),
            #daedalus end
               (neg|party_slot_eq, ":village", slot_village_state, svs_looted),
               (neg|party_slot_eq, ":village", slot_village_state, svs_being_raided),
               (neg|party_slot_ge, ":village", slot_village_infested_by_bandits, 1),
               (neg|party_slot_eq, ":village", dplmc_slot_village_reserved_by_recruiter, 1),
               (assign, ":min_distance", ":distance"),
               (assign, ":closest_village", ":village"),
            (try_end),
         (try_end),
         (gt, ":closest_village", -1),
         (party_set_ai_behavior, ":party_no", ai_bhvr_travel_to_party),
         (party_set_ai_object, ":party_no", ":closest_village"),
         (party_set_slot, ":party_no", slot_party_ai_object, ":closest_village"),
         (party_set_slot, ":closest_village", dplmc_slot_village_reserved_by_recruiter, 1),
      (try_end),
      (party_get_slot, ":target", ":party_no", slot_party_ai_object),
      (gt, ":target", -1),
      (store_distance_to_party_from_party, ":distance_from_target", ":party_no", ":target"),
      (try_begin),
         (store_faction_of_party, ":target_current_faction", ":target"),
         (assign, ":faction_relation", 100),
         (try_begin),
            (neq, ":target_current_faction", "$players_kingdom"),    # faction relation will be checked only if the target doesn't belong to the player's current faction
            (store_relation, ":faction_relation", "$players_kingdom", ":target_current_faction"),
         (try_end),
         (ge, ":faction_relation", 0),
         (party_get_slot, ":target_relation", ":target", slot_center_player_relation),
         (ge, ":target_relation", 0),
      #daedalus begin
            (party_get_slot, ":target_faction", ":target", slot_center_original_faction),
            (assign,":stop",1),
            (try_begin),
            (eq,":recruit_faction",-1),
            (assign,":stop",0),
        (else_try),
            (eq, ":target_faction", ":recruit_faction"),
            (assign,":stop",0),
            (try_end),
            (neq,":stop",1),
      #daedalus end
         (neg|party_slot_eq, ":target", slot_village_state, svs_looted),
            (neg|party_slot_eq, ":target", slot_village_state, svs_being_raided),
            (neg|party_slot_ge, ":target", slot_village_infested_by_bandits, 1),
         (le, ":distance_from_target", 0),
         (party_get_slot, ":volunteers_in_target", ":target", slot_center_volunteer_troop_amount),
         (party_get_slot, ":target_volunteer_type", ":target", slot_center_volunteer_troop_type),
         (assign, ":still_needed", ":needed"),
         (val_sub, ":still_needed", ":amount"),
         (try_begin),
            (gt, ":volunteers_in_target", ":still_needed"),
            (assign, ":santas_little_helper", ":volunteers_in_target"),
            (val_sub, ":santas_little_helper", ":still_needed"),
            (assign, ":amount_to_recruit", ":volunteers_in_target"),
            (val_sub, ":amount_to_recruit", ":santas_little_helper"),
            (assign, ":new_target_volunteer_amount", ":volunteers_in_target"),
            (val_sub, ":new_target_volunteer_amount", ":amount_to_recruit"),
            (party_set_slot, ":target", slot_center_volunteer_troop_amount, ":new_target_volunteer_amount"),
            (party_add_members, ":party_no", ":target_volunteer_type", ":amount_to_recruit"),
            (party_set_ai_behavior, ":party_no", ai_bhvr_hold),
            (party_set_slot, ":target", dplmc_slot_village_reserved_by_recruiter, 0),
         (else_try),
            (le, ":volunteers_in_target", ":still_needed"),
            (gt, ":volunteers_in_target", 0),
            (party_set_slot, ":target", slot_center_volunteer_troop_amount, -1),
            (party_add_members, ":party_no", ":target_volunteer_type", ":volunteers_in_target"),
            (party_set_ai_behavior, ":party_no", ai_bhvr_hold),
            (party_set_slot, ":target", dplmc_slot_village_reserved_by_recruiter, 0),
         (else_try),
            (le, ":volunteers_in_target", 0),
            (party_set_ai_behavior, ":party_no", ai_bhvr_hold),
            (party_set_slot, ":target", dplmc_slot_village_reserved_by_recruiter, 0),
         (else_try),
            (display_message, "@ERROR IN THE RECRUITER KIT SIMPLE TRIGGERS!",0xFF2222),
            (party_set_slot, ":target", dplmc_slot_village_reserved_by_recruiter, 0),
         (try_end),
      (try_end),
   (try_end),

   (try_for_parties, ":party_no"),
      (party_slot_eq,":party_no", slot_party_type, dplmc_spt_recruiter),
      (party_get_num_companions, ":amount", ":party_no"),
      (val_sub, ":amount", 1),   #the recruiter himself doesn't count
      (party_get_slot, ":needed", ":party_no", dplmc_slot_party_recruiter_needed_recruits),
      (eq, ":amount", ":needed"),
      (party_get_slot, ":party_origin", ":party_no", dplmc_slot_party_recruiter_origin),
      (try_begin),
         (neg|party_slot_eq, ":party_no", slot_party_ai_object, ":party_origin"),
         (party_set_slot, ":party_no", slot_party_ai_object, ":party_origin"),
         (party_set_ai_behavior, ":party_no", ai_bhvr_travel_to_party),
         (party_set_ai_object, ":party_no", ":party_origin"),
      (try_end),
      (store_distance_to_party_from_party, ":distance_from_origin", ":party_no", ":party_origin"),
      (try_begin),
         (le, ":distance_from_origin", 0),
         (party_get_num_companion_stacks, ":stacks", ":party_no"),
         (try_for_range, ":stack_no", 1, ":stacks"),
            (party_stack_get_size, ":size", ":party_no", ":stack_no"),
            (party_stack_get_troop_id, ":troop_id", ":party_no", ":stack_no"),
            (party_add_members, ":party_origin", ":troop_id", ":size"),
         (try_end),
         (str_store_party_name_link, s13, ":party_origin"),
         (assign, reg10, ":amount"),
         (display_log_message, "@A recruiter has brought {reg10} recruits to {s13}.", 0x00FF00),
         (remove_party, ":party_no"),
      (try_end),
   (try_end),
   ]),
#This trigger makes sure that no village is left reserved forever.
(12,
   [
   (try_for_range, ":village", villages_begin, villages_end),
      (party_set_slot, ":village", dplmc_slot_village_reserved_by_recruiter, 0),
   (try_end),
   ]),
#Recruiter kit end

 #process gift_carvans
 (0.5,
 [
  (eq, "$g_player_chancellor", "trp_dplmc_chancellor"),
  ##nested diplomacy start+
  #These gifts are far too efficient.  To be balanced with Native, they
  #should not (at the best case) exceed an efficiency of 1000 gold per point.
  (assign, ":save_reg0", reg0),
  (assign, ":save_reg1", reg1),
  (game_get_reduce_campaign_ai, ":reduce_campaign_ai"),#store for use below
  ##nested diplomacy end+
  (try_for_parties, ":party_no"),
    (party_slot_eq,":party_no", slot_party_type, dplmc_spt_gift_caravan),
    (party_is_active, ":party_no"),
    (party_get_slot, ":target_party", ":party_no", slot_party_ai_object),
    (party_get_slot, ":target_troop", ":party_no", slot_party_orders_object),

    (try_begin),
      (party_is_active, ":target_party"),

      (store_distance_to_party_from_party, ":distance_to_target", ":party_no", ":target_party"),
      (str_store_party_name, s14, ":party_no"),
      (str_store_party_name, s15,":target_party"),

      (try_begin), #debug
        (eq, "$cheat_mode", 1),
        (assign, reg0, ":distance_to_target"),
        (display_message, "@Distance between {s14} and {s15}: {reg0}"),
      (try_end),

      (try_begin),
        (le, ":distance_to_target", 1),

        (party_get_slot, ":gift", ":party_no", dplmc_slot_party_mission_diplomacy),
        (str_store_item_name, s12, ":gift"),

        (try_begin),
          (gt, ":target_troop", 0),
          (str_store_troop_name, s13, ":target_troop"),
        (else_try),
          (str_store_party_name, s13, ":target_party"),
        (end_try),
        (display_log_message, "@Your caravan has brought {s12} to {s13}.", 0x00FF00),

        (assign, ":relation_boost", 0),
        (store_faction_of_party, ":target_faction", ":target_party"),

        (try_begin),
          (gt, ":target_troop", 0),
          (faction_slot_eq,":target_faction",slot_faction_leader,":target_troop"),
          (try_begin),
            (eq, ":gift", "itm_wine"),
            (assign, ":relation_boost", 1),
          (else_try),
            (eq, ":gift", "itm_oil"),
            (assign, ":relation_boost", 2),
          (try_end),
        (else_try),
          (store_random_in_range, ":random", 1, 3),
          (try_begin),
            (eq, ":gift", "itm_ale"),
            (val_add, ":relation_boost", ":random"),
          (else_try),
            (eq, ":gift", "itm_wine"),
            (store_add, ":relation_boost", 1, ":random"),
          (else_try),
            (eq, ":gift", "itm_oil"),
            (store_add, ":relation_boost", 2, ":random"),
          (else_try),
            (eq, ":gift", "itm_raw_dyes"),
            (val_add, ":relation_boost", 1),
          (else_try),
            (eq, ":gift", "itm_raw_silk"),
            (val_add, ":relation_boost", 2),
          (else_try),
            (eq, ":gift", "itm_velvet"),
            (val_add, ":relation_boost", 4),
          (else_try),
            (eq, ":gift", "itm_smoked_fish"),
            (try_begin),
              (party_slot_eq, ":target_party", slot_party_type, spt_village),
              (val_add, ":relation_boost", 1),
            (try_end),
          (else_try),
            (eq, ":gift", "itm_cheese"),
            (val_add, ":relation_boost", 1),
            (try_begin),
              (party_slot_eq, ":target_party", slot_party_type, spt_village),
              (val_add, ":relation_boost", 1),
            (try_end),
          (else_try),
            (eq, ":gift", "itm_honey"),
            (val_add, ":relation_boost", 2),
            (try_begin),
              (party_slot_eq, ":target_party", slot_party_type, spt_village),
              (val_add, ":relation_boost", 2),
            (try_end),
          (try_end),
        (try_end),

        (try_begin),
          (this_or_next|eq, ":target_faction", "fac_player_supporters_faction"),
          (eq, ":target_faction", "$players_kingdom"),
          (val_add, ":relation_boost", 1),
        (try_end),

		##nested diplomacy start+
		#Determine the gold cost of the gifts.
		(store_item_value, ":gift_value", ":gift"),
		#Determine how many copies of the gift are used
		(party_get_slot, ":gift_value_factor", ":party_no", dplmc_slot_party_mission_parameter_1),
		(try_begin),
			#This should only fail if the game was saved using an old version while
			#a caravan was en route.
			(gt, ":gift_value_factor", 0),
			(val_mul, ":gift_value", ":gift_value_factor"),
		(else_try),
			#Gifts to ladies had no multiplier.
			#Also, don't do anything for non-trade-goods.
			(this_or_next|is_between, ":target_troop", kingdom_ladies_begin, kingdom_ladies_end),
			(neg|is_between, ":gift", trade_goods_begin, trade_goods_end),
		(else_try),
			 #Gifts to lords used 150 copies of an item
			(is_between, ":target_troop", active_npcs_begin, active_npcs_end),
			(val_mul, ":gift_value", 150),
		(else_try),
			#Gifts to centers used 300 copies of an item
			(is_between, ":target_party", centers_begin, centers_end),
			(val_mul, ":gift_value", 300),
		(try_end),
		(assign, ":gift_value_factor", 100),

		#(store_sub, ":gift_slot_no", ":gift", trade_goods_begin),
		#(val_add, ":gift_slot_no", slot_town_trade_good_prices_begin),

		(try_begin),
			#Gift isn't a trade good: this should never happen
			(neg|is_between, ":gift", trade_goods_begin, trade_goods_end),
			(try_begin),
				(this_or_next|gt, ":target_troop", 0),
					(party_slot_eq, ":target_party", slot_party_type, spt_town),
				(assign, ":gift_value_factor", 115),
			(else_try),
				(assign, ":gift_value_factor", 130),
			(try_end),
		(else_try),
			#Given to a lord.
			(gt, ":target_troop", 0),

			(assign, ":global_price_factor", 0),
			(assign, ":faction_price_factor", 0),
			(assign, ":faction_markets", 0),
			(assign, ":personal_price_factor", 0),
			(assign, ":personal_markets", 0),

			(try_for_range, ":center_no", towns_begin, towns_end),
				(call_script, "script_dplmc_get_item_buy_price_factor", ":gift", ":center_no", -2, -2),
				(val_add, ":global_price_factor", reg0),

				(store_faction_of_party, ":center_faction", ":center_no"),
				(eq, ":center_faction", ":target_faction"),
				(val_add, ":faction_price_factor", reg0),
				(val_add, ":faction_markets", 1),

				(party_slot_eq, ":center_no", slot_town_lord, ":target_troop"),
				(val_add, ":personal_price_factor", reg0),
				(val_add, ":personal_markets", 1),
			(try_end),

			(try_begin),
				(eq, ":personal_markets", 0),
				(try_for_range, ":center_no", villages_begin, villages_end),
					(try_begin),
						(party_slot_eq, ":center_no", slot_town_lord, ":target_troop"),
						(call_script, "script_dplmc_get_item_buy_price_factor", ":gift", ":center_no", -2, -2),
						(val_add, ":faction_markets", reg0),
						(val_add, ":personal_markets", 1),
					(try_end),
					#Check for castles (deliberately allow multiple-counting)
					(try_begin),
						(party_get_slot, reg1, ":center_no", slot_village_bound_center),
						(gt, reg1, 0),
						(party_slot_eq, reg1, slot_party_type, spt_castle),
						(party_slot_eq, reg1, slot_town_lord, ":target_troop"),
						(call_script, "script_dplmc_get_item_buy_price_factor", ":gift", ":center_no", -2, -2),
						(val_add, ":faction_markets", reg0),
						(val_add, ":personal_markets", 1),
					(try_end),
				(try_end),
			(try_end),

			(try_begin),
				#First use any markets at or near the target's fiefs
				(gt, ":personal_markets", 0),
				(store_div, ":gift_value_factor", ":personal_price_factor", ":personal_markets"),
			(else_try),
				#Alternately use any faction markets
				(gt, ":faction_markets", 0),
				(val_mul, ":faction_price_factor", 130),#Convert trade penalty from 115% to 130%
				(val_div, ":faction_price_factor", 115),
				(store_div, ":gift_value_factor", ":faction_price_factor", ":faction_markets"),
			(else_try),
				#As a final option use the global average price
				(gt, towns_end, towns_begin),#should always be true (if not, then the gift price factor stays average)
				(store_sub, reg1, towns_end, towns_begin),
				(val_mul, ":global_price_factor", 130),#Convert trade penalty from 115% to 130%
				(val_div, ":global_price_factor", 115),
				(store_div, ":gift_value_factor", ":global_price_factor", reg1),
			(try_end),
		(else_try),
			#Given to a town or village
			(gt, ":target_party", 0),
			(call_script, "script_dplmc_get_item_buy_price_factor", ":gift", ":center_no", -2, -2),
			(assign, ":gift_value_factor", reg0),
		(else_try),
			#This should never happen
			(assign, ":gift_value_factor", 115),
		(try_end),

		(try_begin),
			(ge, "$cheat_mode", 1),
			(assign, reg0, ":gift_value_factor"),
			(store_mul, reg1, ":gift_value", ":gift_value_factor"),
			(val_add, reg1, 50),
			(val_div, reg1, 100),
			(val_add, reg1, 50),
			(display_message, "@{!} Gift price factor {reg0}/100, effective value {reg1}"),
		(try_end),

		(val_mul, ":gift_value", ":gift_value_factor"),
		(val_add, ":gift_value", 50),
		(val_div, ":gift_value", 100),

		(val_add, ":gift_value", 50),#the cost of the messenger
	    (store_random_in_range, ":random", 0, 1000),#randomly round up or down later, when dividing by 1000
		(assign, reg0, ":gift_value"),#<-- see (1) below, store gold value of gift
		(val_add, ":gift_value", ":random"),
		(val_div, ":gift_value", 1000),

		(try_begin),
		   (eq, ":reduce_campaign_ai", 0), #hard: do not exceed 1/1000 efficiency
		   (val_min, ":relation_boost", ":gift_value"),
		   (try_begin),
			  (eq, ":relation_boost", 0),
			  (store_random_in_range, ":random", 0, 1000),
			  (lt, ":random", reg0),#<-- (1) see above, has gold value of gift
			  (assign, ":relation_boost", 1),
		   (try_end),
		(else_try),
		   (eq, ":reduce_campaign_ai", 1), #medium: use a blend of the two
		   (lt, ":gift_value", ":relation_boost"),
		   (val_add, ":relation_boost", ":gift_value"),
		   (val_add, ":relation_boost", 1),
		   (val_div, ":relation_boost", 2),
	    (else_try),
		   (eq, ":reduce_campaign_ai", 2), #easy: do not use
		(try_end),

		(val_max, ":gift_value", 1),
		(val_min, ":relation_boost", ":gift_value"),
		##nested diplomacy end+

        (try_begin),
		##nested diplomacy start+
		#Write a message so the player doesn't think the lack of relation gain is an error.
			(lt, ":relation_boost", 1),
			(try_begin),
				(gt, ":target_troop", 0),
				(display_message, "@{s13} is unimpressed by your paltry gift."),
			(else_try),
				(display_message, "@The people of {s13} are unimpressed by your paltry gift."),
			(try_end),
		(else_try),
		##nested diplomacy+
          (gt, ":target_troop", 0),
		  (call_script, "script_change_player_relation_with_troop", ":target_troop", ":relation_boost"),
        (else_try),
          (call_script, "script_change_player_relation_with_center", ":target_party", ":relation_boost"),
        (try_end),
        (remove_party, ":party_no"),
      (try_end),
    (else_try),
      (display_log_message, "@Your caravan has lost it's way and gave up your mission!", 0xFF0000),
      (remove_party, ":party_no"),
    (try_end),
  (try_end),
  ##nested diplomacy start+
  (assign, reg0, ":save_reg0"),
  (assign, reg1, ":save_reg1"),
  ##nested diplomacy start+
 ]),
 #process messengers
 (0.5,
 [
  (try_for_parties, ":party_no"),
    (party_slot_eq,":party_no", slot_party_type, spt_messenger),

    (party_get_slot, ":target_party", ":party_no", slot_party_ai_object),
    (party_get_slot, ":orders_object", ":party_no", slot_party_orders_object),

    (try_begin),
      (party_is_active, ":target_party"),
      (store_distance_to_party_from_party, ":distance_to_target", ":party_no", ":target_party"),
      (str_store_party_name, s14, ":party_no"),
      (str_store_party_name, s15,":target_party"),

      (try_begin), #debug
        (eq, "$cheat_mode", 1),
        (assign, reg0, ":distance_to_target"),
        (display_message, "@Distance between {s14} and {s15}: {reg0}"),
      (try_end),

      (try_begin),
        (le, ":distance_to_target", 1),

        (try_begin), # returning to p_main_party
          (eq, ":target_party", "p_main_party"),
          (party_get_slot, ":party_leader", ":party_no", slot_party_orders_object),
          (party_get_slot, ":success", ":party_no", dplmc_slot_party_mission_diplomacy),
          (call_script, "script_add_notification_menu", "mnu_dplmc_messenger", ":party_leader", ":success"),
          (remove_party, ":party_no"),
        (else_try), # patrols
          (party_slot_eq, ":target_party", slot_party_type, spt_patrol),
          (party_get_slot, ":message", ":party_no", dplmc_slot_party_mission_diplomacy),

          (try_begin),
            (eq, ":message", spai_undefined),
            (remove_party, ":target_party"),
          (else_try),
            (eq, ":message", spai_retreating_to_center),
            (str_store_party_name, s6, ":orders_object"),
            (party_set_name, ":target_party", "@Transfer to {s6}"),
            (party_set_ai_behavior, ":target_party", ai_bhvr_travel_to_party),
            (party_set_ai_object, ":target_party", ":orders_object"),
            (party_set_slot, ":target_party", slot_party_ai_object, ":orders_object"),
            (party_set_slot, ":target_party", slot_party_ai_state, spai_retreating_to_center),
            (party_set_aggressiveness, ":target_party", 0),
            (party_set_courage, ":target_party", 3),
            (party_set_ai_initiative, ":target_party", 100),
          (else_try),
            (str_store_party_name, s6, ":orders_object"),
            (party_set_name, ":target_party", "@{s6} patrol"),
            (party_set_ai_behavior, ":target_party", ai_bhvr_travel_to_party),
            (party_set_ai_object, ":target_party", ":orders_object"),
            (party_set_slot, ":target_party", slot_party_ai_object, ":orders_object"),
            (party_set_slot, ":target_party", slot_party_orders_type, ":message"),
          (try_end),

          (remove_party, ":party_no"),
        (else_try), # reached any other target
          (party_stack_get_troop_id, ":party_leader", ":target_party", 0),
          (str_store_troop_name, s13, ":party_leader"),

          (try_begin), #debug
            (eq, "$cheat_mode", 1),
            (display_log_message, "@Your messenger reached {s13}.", 0x00FF00),
            (assign, "$g_talk_troop", ":party_leader"), #debug
          (try_end),

          (party_get_slot, ":message", ":party_no", dplmc_slot_party_mission_diplomacy),
          (assign, ":success", 0),
          (try_begin),
            (party_set_slot, ":target_party", slot_party_commander_party, "p_main_party"),
          	(store_current_hours, ":hours"),
          	(party_set_slot, ":target_party", slot_party_following_orders_of_troop, "trp_kingdom_heroes_including_player_begin"),
          	(party_set_slot, ":target_party", slot_party_orders_object, ":orders_object"),
          	(party_set_slot, ":target_party", slot_party_orders_type, ":message"),

          	(party_set_slot, ":target_party", slot_party_orders_time, ":hours"),
            (call_script, "script_npc_decision_checklist_party_ai", ":party_leader"), #This handles AI for both marshal and other parties


            (try_begin), #debug
              (eq, "$cheat_mode", 1),
              (display_message, "@{s14}"), #debug
            (try_end),

            (try_begin),
              (eq, reg0, ":message"),
              (eq, reg1, ":orders_object"),
              (assign, ":success", 1),
            (try_end),
            (call_script, "script_party_set_ai_state", ":target_party", reg0, reg1),
          (try_end),

          (party_set_ai_behavior, ":party_no", ai_bhvr_travel_to_party),
          (party_set_ai_object, ":party_no", "p_main_party"),
          (party_set_slot, ":party_no", slot_party_ai_object, "p_main_party"),
          (party_set_slot, ":party_no", slot_party_orders_object, ":party_leader"),
          (party_set_slot, ":party_no", dplmc_slot_party_mission_diplomacy, ":success"),
        (try_end),
      (try_end),
    (else_try),
      (display_log_message, "@Your messenger has lost it's way and gave up your mission!", 0xFF0000),
      (remove_party, ":party_no"),
    (try_end),
  (try_end),
 ]),
]
