# -*- coding: UTF-8 -*-
# split feature file: presentations - module
from header_common import *
from header_presentations import *
from header_mission_templates import *
from ID_meshes import *
from header_operations import *
from header_triggers import *
from module_constants import *
from module_meshes import *
import string
from header_terrain_types import *
from module_items import *

presentations_politics_reports = [
  ("name_kingdom",0,mesh_load_window,[
      (ti_on_presentation_load,
       [(set_fixed_point_multiplier, 1000),
        (str_store_string, s1, "str_name_kingdom_text"),
        (create_text_overlay, reg1, s1, tf_center_justify),
        (position_set_x, pos1, 500),
        (position_set_y, pos1, 500),
        (overlay_set_position, reg1, pos1),
        (overlay_set_text, reg1, s1),
        (create_simple_text_box_overlay, "$g_presentation_obj_name_kingdom_1"),
        (position_set_x, pos1, 400),
        (position_set_y, pos1, 400),
        (overlay_set_position, "$g_presentation_obj_name_kingdom_1", pos1),
        (try_begin),
          (eq, "$players_kingdom_name_set", 1),
          (str_store_faction_name, s7, "fac_player_supporters_faction"),
          (overlay_set_text, "$g_presentation_obj_name_kingdom_1", s7),
        (else_try),
          (str_store_troop_name, s0, "trp_player"),
          (overlay_set_text, "$g_presentation_obj_name_kingdom_1", "str_default_kingdom_name"),
          (str_store_string, s7, "str_default_kingdom_name"),
        (try_end),
        
        (create_button_overlay, "$g_presentation_obj_name_kingdom_2", "@Continue...", tf_center_justify),
        (position_set_x, pos1, 500),
        (position_set_y, pos1, 300),
        (overlay_set_position, "$g_presentation_obj_name_kingdom_2", pos1),
        (presentation_set_duration, 999999),
        ]),
      (ti_on_presentation_event_state_change,
       [(store_trigger_param_1, ":object"),
        (try_begin),
          (eq, ":object", "$g_presentation_obj_name_kingdom_1"),
          (str_store_string, s7, s0),
        (else_try),
          (eq, ":object", "$g_presentation_obj_name_kingdom_2"),
          (faction_set_name, "fac_player_supporters_faction", s7),
          (faction_set_color, "fac_player_supporters_faction", 0xFF0000),
          (assign, "$players_kingdom_name_set", 1),
          (presentation_set_duration, 0),
        (try_end),
        ]),
      ]),
  ("marshall_selection", 0, mesh_load_window,
   [
     (ti_on_presentation_load,
      [
        (assign, "$g_presentation_obj_marshall_selection_1", -1),
        (assign, "$g_presentation_obj_marshall_selection_2", -1),
        (assign, "$g_presentation_obj_marshall_selection_3", -1),
        (set_fixed_point_multiplier, 1000),
        (assign, "$g_presentation_next_presentation", -1),
        (assign, "$g_presentation_marshall_selection_1_vote", 0),
        (assign, "$g_presentation_marshall_selection_2_vote", 0),
        (assign, "$g_presentation_marshall_selection_max_renown_1", -10000),
        (assign, "$g_presentation_marshall_selection_max_renown_2", -10000),
        (assign, "$g_presentation_marshall_selection_max_renown_1_troop", -1),
        (assign, "$g_presentation_marshall_selection_max_renown_2_troop", -1),
        (assign, "$g_presentation_marshall_selection_ended", 0),

        (store_add, ":total_renown", "$g_presentation_marshall_selection_max_renown_1", "$g_presentation_marshall_selection_max_renown_2"),
        (faction_get_slot, ":king", "$players_kingdom", slot_faction_leader),

        (str_store_troop_name, s1, "$g_presentation_marshall_selection_max_renown_1_troop"),
        (create_text_overlay, reg1, "@Candidate #1: {s1}", tf_center_justify),
        (position_set_x, pos1, 200),
        (position_set_y, pos1, 600),
        (overlay_set_position, reg1, pos1),
        (str_store_troop_name, s1, "$g_presentation_marshall_selection_max_renown_2_troop"),
        (create_text_overlay, reg1, "@Candidate #2: {s1}", tf_center_justify),
        (position_set_x, pos1, 800),
        (position_set_y, pos1, 600),
        (overlay_set_position, reg1, pos1),
        (create_mesh_overlay_with_tableau_material, reg1, -1, "tableau_troop_note_mesh", "$g_presentation_marshall_selection_max_renown_1_troop"),
        (position_set_x, pos1, 500),
        (position_set_y, pos1, 500),
        (overlay_set_size, reg1, pos1),
        (position_set_x, pos1, 100),
        (position_set_y, pos1, 300),
        (overlay_set_position, reg1, pos1),
        (create_mesh_overlay_with_tableau_material, reg1, -1, "tableau_troop_note_mesh", "$g_presentation_marshall_selection_max_renown_2_troop"),
        (position_set_x, pos1, 500),
        (position_set_y, pos1, 500),
        (overlay_set_size, reg1, pos1),
        (position_set_x, pos1, 700),
        (position_set_y, pos1, 300),
        (overlay_set_position, reg1, pos1),

        (assign, ":lord_index", "$g_presentation_input"),
        (val_add, "$g_presentation_input", 1),

        (try_begin),
          (lt, ":lord_index", 0),
          (str_store_troop_name, s1, "$g_presentation_marshall_selection_max_renown_1_troop"),
          (str_store_troop_name, s2, "$g_presentation_marshall_selection_max_renown_2_troop"),
          (str_store_troop_name, s3, ":king"),
          (str_store_faction_name, s4, "$players_kingdom"),
          (create_text_overlay, reg1, "@{s3} of {s4} wishes to select a new strategist and invites his vassals for a counsel. {s1} and {s2} are the likely candidates.", tf_center_justify),
          (position_set_x, pos1, 500),
          (position_set_y, pos1, 200),
          (overlay_set_position, reg1, pos1),

          (create_button_overlay, "$g_presentation_obj_marshall_selection_1", "@Continue...", tf_center_justify),
          (position_set_x, pos1, 500),
          (position_set_y, pos1, 100),
          (overlay_set_position, "$g_presentation_obj_marshall_selection_1", pos1),
          (assign, "$g_presentation_next_presentation", "prsnt_marshall_selection"),
        (else_try),
          (assign, ":cur_index", ":lord_index"),
          (try_for_range_backwards, ":loop_var", "trp_kingdom_heroes_including_player_begin", active_npcs_end),
            (ge, ":cur_index", 0),
            (assign, ":cur_troop", ":loop_var"),
            (assign, ":continue", 0),
            (try_begin),
              (eq, ":loop_var", "trp_kingdom_heroes_including_player_begin"),
              (assign, ":cur_troop", "trp_player"),
              (try_begin),
                (eq, "$g_player_is_captive", 0),
                (assign, ":continue", 1),
              (try_end),
            (else_try),
              (store_troop_faction, ":cur_troop_faction", ":cur_troop"),
              (eq, "$players_kingdom", ":cur_troop_faction"),
              #(troop_slot_eq, ":cur_troop", slot_troop_is_prisoner, 0),
              (neg|troop_slot_ge, ":cur_troop", slot_troop_prisoner_of_party, 0),
              (troop_slot_ge, ":cur_troop", slot_troop_leaded_party, 1),
              (troop_slot_eq, ":cur_troop", slot_troop_occupation, slto_kingdom_hero),
              (neg|faction_slot_eq, ":cur_troop_faction", slot_faction_leader, ":cur_troop"),
              (assign, ":continue", 1),
            (try_end),
            (eq, ":continue", 1),

            (neq, "$g_presentation_marshall_selection_max_renown_1_troop", ":cur_troop"),
            (neq, "$g_presentation_marshall_selection_max_renown_2_troop", ":cur_troop"),

            (val_sub, ":cur_index", 1),
            (lt, ":cur_index", 0),

            (assign, "$g_presentation_next_presentation", "prsnt_marshall_selection"),

            (create_mesh_overlay_with_tableau_material, reg1, -1, "tableau_troop_note_mesh", ":cur_troop"),
            (position_set_x, pos1, 300),
            (position_set_y, pos1, 300),
            (overlay_set_size, reg1, pos1),
            (position_set_x, pos1, 440),
            (position_set_y, pos1, 400),
            (overlay_set_position, reg1, pos1),

            (try_begin),
              (eq, ":cur_troop", "trp_player"),
              (create_text_overlay, reg1, "@Who do you wish to support?", tf_center_justify),
              (position_set_x, pos1, 500),
              (position_set_y, pos1, 200),
              (overlay_set_position, reg1, pos1),
              (str_store_troop_name, s1, "$g_presentation_marshall_selection_max_renown_1_troop"),
              (create_button_overlay, "$g_presentation_obj_marshall_selection_2", "@{!}{s1}", tf_center_justify),
              (position_set_x, pos1, 300),
              (position_set_y, pos1, 100),
              (overlay_set_position, "$g_presentation_obj_marshall_selection_2", pos1),
              (str_store_troop_name, s1, "$g_presentation_marshall_selection_max_renown_2_troop"),
              (create_button_overlay, "$g_presentation_obj_marshall_selection_3", "@{!}{s1}", tf_center_justify),
              (position_set_x, pos1, 700),
              (position_set_y, pos1, 100),
              (overlay_set_position, "$g_presentation_obj_marshall_selection_3", pos1),
            (else_try),
              (str_store_troop_name, s1, ":cur_troop"),
              (store_random_in_range, ":random_renown", 0, ":total_renown"),
              (val_sub, ":random_renown", "$g_presentation_marshall_selection_max_renown_1"),
              (try_begin),
                (lt, ":random_renown", 0),
                (val_add, "$g_presentation_marshall_selection_1_vote", 1),
                (str_store_troop_name, s2, "$g_presentation_marshall_selection_max_renown_1_troop"),
              (else_try),
                (val_add, "$g_presentation_marshall_selection_2_vote", 1),
                (str_store_troop_name, s2, "$g_presentation_marshall_selection_max_renown_2_troop"),
              (try_end),
              (create_text_overlay, reg1, "@{s1} gives his support to {s2}.", tf_center_justify),
              (position_set_x, pos1, 500),
              (position_set_y, pos1, 200),
              (overlay_set_position, reg1, pos1),

              (create_button_overlay, "$g_presentation_obj_marshall_selection_1", "@Continue...", tf_center_justify),
              (position_set_x, pos1, 500),
              (position_set_y, pos1, 100),
              (overlay_set_position, "$g_presentation_obj_marshall_selection_1", pos1),
            (try_end),
          (try_end),
        (try_end),

        (assign, reg0, "$g_presentation_marshall_selection_1_vote"),
        (create_text_overlay, reg1, "@Number of Supporters: {reg0}", tf_center_justify),
        (position_set_x, pos1, 200),
        (position_set_y, pos1, 550),
        (overlay_set_position, reg1, pos1),
        (assign, reg0, "$g_presentation_marshall_selection_2_vote"),
        (create_text_overlay, reg1, "@Number of Supporters: {reg0}", tf_center_justify),
        (position_set_x, pos1, 800),
        (position_set_y, pos1, 550),
        (overlay_set_position, reg1, pos1),

        (try_begin),
          (lt, "$g_presentation_next_presentation", 0),
          (try_begin),
            (gt, "$g_presentation_marshall_selection_2_vote", "$g_presentation_marshall_selection_1_vote"),
            (assign, ":local_temp", "$g_presentation_marshall_selection_max_renown_1_troop"),
            (assign, "$g_presentation_marshall_selection_max_renown_1_troop", "$g_presentation_marshall_selection_max_renown_2_troop"),
            (assign, "$g_presentation_marshall_selection_max_renown_2_troop", ":local_temp"),
          (try_end),
          #Winner is set to g_presentation_marshall_selection_max_renown_1_troop
          (str_store_troop_name, s1, "$g_presentation_marshall_selection_max_renown_1_troop"),
          (str_store_troop_name, s2, ":king"),
          (str_store_faction_name, s3, "$players_kingdom"),
          (create_text_overlay, reg1, "@{s2} has heard his vassals' counsel. He selects {s1} as the strategist of {s3}.", tf_center_justify),
          (position_set_x, pos1, 500),
          (position_set_y, pos1, 200),
          (overlay_set_position, reg1, pos1),
          (create_button_overlay, "$g_presentation_obj_marshall_selection_1", "@Continue...", tf_center_justify),
          (position_set_x, pos1, 500),
          (position_set_y, pos1, 100),
          (overlay_set_position, "$g_presentation_obj_marshall_selection_1", pos1),
        (try_end),

        (presentation_set_duration, 999999),
        ]),
     (ti_on_presentation_event_state_change,
      [
        (store_trigger_param_1, ":object"),
        (try_begin),
          (eq, ":object", "$g_presentation_obj_marshall_selection_2"),
          (val_add, "$g_presentation_marshall_selection_1_vote", 1),
          (call_script, "script_change_player_relation_with_troop", "$g_presentation_marshall_selection_max_renown_1_troop", 2),
          (call_script, "script_change_player_relation_with_troop", "$g_presentation_marshall_selection_max_renown_2_troop", -2),
        (else_try),
          (eq, ":object", "$g_presentation_obj_marshall_selection_3"),
          (val_add, "$g_presentation_marshall_selection_2_vote", 1),
          (call_script, "script_change_player_relation_with_troop", "$g_presentation_marshall_selection_max_renown_1_troop", -2),
          (call_script, "script_change_player_relation_with_troop", "$g_presentation_marshall_selection_max_renown_2_troop", 2),
        (try_end),
        (try_begin),
          (this_or_next|eq, ":object", "$g_presentation_obj_marshall_selection_1"),
          (this_or_next|eq, ":object", "$g_presentation_obj_marshall_selection_2"),
          (eq, ":object", "$g_presentation_obj_marshall_selection_3"),
          (try_begin),
            (ge, "$g_presentation_next_presentation", 0),
            (start_presentation, "$g_presentation_next_presentation"),
          (else_try),
            (try_begin),
              (neg|faction_slot_eq, "$players_kingdom", slot_faction_marshall, "$g_presentation_marshall_selection_max_renown_1_troop"),
              (call_script, "script_check_and_finish_active_army_quests_for_faction", "$players_kingdom"),
            (try_end),

           (faction_get_slot, ":old_marshall", "$players_kingdom", slot_faction_marshall),
           (try_begin),
             (ge, ":old_marshall", 0),
             (party_is_active, ":old_marshall"),
             (party_set_marshall, ":old_marshall", 0),
           (try_end),  

            (faction_set_slot, "$players_kingdom", slot_faction_marshall, "$g_presentation_marshall_selection_max_renown_1_troop"),
            (try_begin),
              (eq, "$g_presentation_marshall_selection_max_renown_1_troop", "trp_player"),
              (call_script, "script_change_player_relation_with_troop", "$g_presentation_marshall_selection_max_renown_2_troop", -3),
            (try_end),
            (assign, "$g_recalculate_ais", 1),
            (assign, "$g_presentation_marshall_selection_ended", 1),
            (presentation_set_duration, 0),
          (try_end),
        (try_end),
        ]),
     ]),
  ("budget_report", 0, mesh_load_window,
   [(ti_on_presentation_load,
     [(presentation_set_duration, 999999),
      (set_fixed_point_multiplier, 1000),
      
      (create_mesh_overlay, reg1, "mesh_pic_payment"),
      (position_set_x, pos1, 800),
      (position_set_y, pos1, 800),
      (overlay_set_size, reg1, pos1),
      (position_set_x, pos1, 170),
      (position_set_y, pos1, 0),
      (overlay_set_position, reg1, pos1),
      
      (create_text_overlay, reg1, "str_weekly_budget", tf_center_justify),
      (position_set_x, pos1, 1500),
      (position_set_y, pos1, 1500),
      (overlay_set_size, reg1, pos1),
      (position_set_x, pos1, 260),
      (position_set_y, pos1, 650),
      (overlay_set_position, reg1, pos1),

      (str_clear, s0),
      (create_text_overlay, "$g_presentation_obj_bugdet_report_container", s0, tf_scrollable_style_2),
      (position_set_x, pos1, 0),
      (position_set_y, pos1, 100),
      (overlay_set_position, "$g_presentation_obj_bugdet_report_container", pos1),
      (position_set_x, pos1, 505),
      (position_set_y, pos1, 500),
      (overlay_set_area_size, "$g_presentation_obj_bugdet_report_container", pos1),
      (set_container_overlay, "$g_presentation_obj_bugdet_report_container"),

      (game_get_reduce_campaign_ai, ":reduce_campaign_ai"),      
      (try_begin),
        (eq, ":reduce_campaign_ai", 0), #hard
        (assign, ":num_centers_needed_for_efficiency_loss", 2),
        (assign, ":tax_efficiency_loss_ratio_per_center", 5),
      (else_try),  
        (eq, ":reduce_campaign_ai", 1), #medium
        (assign, ":num_centers_needed_for_efficiency_loss", 4),
        (assign, ":tax_efficiency_loss_ratio_per_center", 4),
      (else_try),  
        (eq, ":reduce_campaign_ai", 2), #easy
        (assign, ":num_centers_needed_for_efficiency_loss", 6),
        (assign, ":tax_efficiency_loss_ratio_per_center", 3),
      (try_end),  
	  ##diplomacy start+ Handle player is co-ruler of NPC kingdom
	  (assign, ":alt_rule_faction", "fac_player_supporters_faction"),
	  (try_begin),
		 (is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
		 (call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", "$players_kingdom"),
		 (ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
	 	 (assign, ":alt_rule_faction", "$players_kingdom"),
	  (try_end),
	  ##diplomacy end+

      (assign, ":num_lines", 0),
      (assign, ":num_owned_center_values_for_tax_efficiency", 0),
      (assign, ":all_centers_accumulated_total", 0),
      (assign, ":all_centers_accumulated_taxes_and_rents", 0),
      (try_for_range, ":center_no", centers_begin, centers_end),	  
	    (try_begin),
		  (party_slot_ge, ":center_no", slot_center_player_enterprise, 1),		  
		  (val_add, ":num_lines", 1),
	    (try_end),	  
	  
        (party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
        (val_add, ":num_lines", 1),
        (val_add, ":num_owned_center_values_for_tax_efficiency", 1),
        (try_begin),
          (is_between, ":center_no", towns_begin, towns_end),
          (val_add, ":num_lines", 1),
          (val_add, ":num_owned_center_values_for_tax_efficiency", 1),
        (try_end),
      (try_end),
      (try_begin),
        (gt, "$players_kingdom", 0),
        (neq, "$players_kingdom", "fac_player_supporters_faction"),
        (neq, "$players_kingdom", "fac_player_faction"),
        (eq, "$player_has_homage", 0),
        (val_add, ":num_lines", 1),
      (try_end),
	  
      (try_begin),      
        (gt, ":num_owned_center_values_for_tax_efficiency", ":num_centers_needed_for_efficiency_loss"),
      #gt accumulated total is ignored
        (val_add, ":num_lines", 1),
      (try_end),
	  
      (try_for_parties, ":party_no"),
        (assign, ":garrison_troop", 0),
        (try_begin),
          (this_or_next|party_slot_eq, ":party_no", slot_party_type, spt_town),
          (party_slot_eq, ":party_no", slot_party_type, spt_castle),
          (party_slot_eq, ":party_no", slot_town_lord, "trp_player"),
          (assign, ":garrison_troop", 1),
        (else_try),
          (this_or_next|party_slot_eq, ":party_no", slot_party_type, spt_town),
          (party_slot_eq, ":party_no", slot_party_type, spt_castle),
          (neg|party_slot_ge, ":party_no", slot_town_lord, 1), #unassigned
          (store_faction_of_party, ":center_faction", ":party_no"),
		  ##diplomacy start+
          (this_or_next|eq, ":alt_rule_faction", ":center_faction"),#co-ruler of an NPC kingdom ##fixed typo 2011-06-07
		  ##diplomacy end+
          (eq, ":center_faction", "fac_player_supporters_faction"),
		  ##diplomacy start+
          (this_or_next|is_between, ":alt_rule_faction", npc_kingdoms_begin, npc_kingdoms_end),#co-ruler of an NPC kingdom
		  ##diplomacy end+
          (faction_slot_eq, "fac_player_supporters_faction", slot_faction_leader, "trp_player"),
          (assign, ":garrison_troop", 1),		  
        (try_end),

        (this_or_next|eq, ":party_no", "p_main_party"),
        ##diplomacy begin
        (assign, ":patrol_troop", 0),
        (try_begin),
          (party_slot_eq, ":party_no",slot_party_type, spt_patrol),
          (party_slot_eq, ":party_no", dplmc_slot_party_mission_diplomacy, "trp_player"),
          (assign, ":patrol_troop", 1),
        (try_end),
        (this_or_next|eq, ":patrol_troop", 1),
        ##diplomacy end
        (eq, ":garrison_troop", 1),
        (val_add, ":num_lines", 1), #include empty towns/castles
      (try_end),
	  
      (try_begin),
        (gt, "$g_player_debt_to_party_members", 0),
        (val_add, ":num_lines", 2), #include new debt line
      (try_end),
	  
      ##diplomacy begin
      (try_begin),
        (this_or_next|gt, "$g_player_minister", 0),
        (this_or_next|troop_slot_ge, "trp_player", slot_troop_spouse, 0),
        (this_or_next|gt, "$g_player_chamberlain", 0),
        (gt, "$g_player_constable", 0),
        (val_add, ":num_lines", 1), # staff salary
      (try_end),

      (try_begin),
        (gt, "$g_player_chamberlain", 0),
        (val_add, ":num_lines", 2), #earlier cash, new cash
      (try_end),
      ##diplomacy end
	  
      (val_add, ":num_lines", 3),
      (store_mul, ":cur_y", 27, ":num_lines"),
      (assign, ":net_change", 0), #this is the amount added
      (try_for_range, ":center_no", centers_begin, centers_end),		
		#Enterprise
        (try_begin),
		  (party_get_slot, ":enterprise_output", ":center_no", slot_center_player_enterprise),
		  (gt, ":enterprise_output", 1),
		  (neg|party_slot_ge, ":center_no", slot_center_player_enterprise_days_until_complete, 1),
		  
          (str_store_party_name, s0, ":center_no"),
		  
		  (call_script, "script_process_player_enterprise", ":enterprise_output", ":center_no"),
		  (assign, ":net_profit", reg0),
		  (assign, ":price_of_single_output", reg4),
		  (assign, ":price_of_single_input", reg5),
		  (assign, ":price_of_secondary_input", reg10),
		  
		  (store_sub, ":town_order", ":center_no", towns_begin),
		  (store_add, ":craftsman_troop", ":town_order", "trp_town_1_master_craftsman"),

		  (item_get_slot, ":outputs_added_to_market", ":enterprise_output", slot_item_output_per_run),
		  (assign, ":outputs_added_to_warehouse", 0),
		  
		  #Enterprise impact of outputs
		  (try_begin),
		    #output placed in inventory: deduct selling price and add one good
			(party_slot_eq, ":center_no", slot_center_player_enterprise_production_order, 1),
			
			#Count empty slots
			(assign, ":empty_slots", 0),
			(troop_get_inventory_capacity, ":total_capacity", ":craftsman_troop"),
			(try_for_range, ":capacity_iterator", 0, ":total_capacity"),
				(troop_get_inventory_slot, ":slot", ":craftsman_troop", ":capacity_iterator"),
				(lt, ":slot", 1),
				(val_add, ":empty_slots", 1),
			(try_end),
			
			(assign, ":outputs_added_to_warehouse", ":outputs_added_to_market"),
			(val_min, ":outputs_added_to_warehouse",  ":empty_slots"),
			(gt, ":outputs_added_to_warehouse", 0),
			
			(store_mul, ":cancelled_sales", ":price_of_single_output", ":outputs_added_to_warehouse"),
			(val_sub, ":net_profit", ":cancelled_sales"),
			(val_sub, ":outputs_added_to_market", ":outputs_added_to_warehouse"),
		  (try_end),
		  
		  #If the transaction is for real, and not just a budget check
		  (try_begin),
		    (eq, "$g_apply_budget_report_to_gold", 1),
			(troop_add_items, ":craftsman_troop", ":enterprise_output", ":outputs_added_to_warehouse"),

			#Affect prices by outputs added to market
			(store_sub, ":item_slot_no", ":enterprise_output", trade_goods_begin),
			(val_add, ":item_slot_no", slot_town_trade_good_prices_begin),
			(party_get_slot, ":current_index", ":center_no", ":item_slot_no"),			
			(store_mul, ":impact_on_price", ":outputs_added_to_market", 15),
			(val_sub, ":current_index", ":impact_on_price"),
			(party_set_slot, ":center_no", ":item_slot_no",":current_index"),			
						
			(gt, "$cheat_mode", 0),
			(str_store_troop_name, s3, ":craftsman_troop"),
			(assign, reg3, ":outputs_added_to_warehouse"),
			(display_message, "@{!}DEBUG -- Adding {reg3} items to {s3}"),
		  (try_end),
		  
		  #Enterprise impact of outputs
		  (item_get_slot, ":inputs_taken_from_market", ":enterprise_output", slot_item_input_number),		  
		  (try_begin),
			(item_slot_ge, ":enterprise_output", slot_item_secondary_raw_material, 1),
		    (assign, ":2ary_inputs_taken_from_market", ":inputs_taken_from_market"),
		  (else_try),
		    (assign, ":2ary_inputs_taken_from_market", 0),
		  (try_end),
		  
		  (assign, ":inputs_taken_from_warehouse", 0),
		  (assign, ":2ary_inputs_taken_from_warehouse", 0),
		  
		  (try_begin),
		    #input present in inventory: reimburse for input cost and remove one good
			(troop_get_inventory_capacity, ":total_capacity", ":craftsman_troop"),
			(try_for_range, ":capacity_iterator", 0, ":total_capacity"),
				(troop_get_inventory_slot, ":item_in_slot", ":craftsman_troop", ":capacity_iterator"),
			
				(lt, ":inputs_taken_from_warehouse", ":inputs_taken_from_market"),
				(item_slot_eq, ":enterprise_output", slot_item_primary_raw_material, ":item_in_slot"),
                #(troop_inventory_slot_get_item_amount, ":item_ammo", ":craftsman_troop", ":capacity_iterator"),
                #(troop_inventory_slot_get_item_max_amount, ":item_max_ammo", ":craftsman_troop", ":capacity_iterator"),
                #(eq, ":item_ammo", ":item_max_ammo"),
				
				(val_add, ":inputs_taken_from_warehouse", 1),
			(else_try),	
				(lt, ":2ary_inputs_taken_from_warehouse", ":2ary_inputs_taken_from_market"),
				(item_slot_eq, ":enterprise_output", slot_item_secondary_raw_material, ":item_in_slot"),
                #(troop_inventory_slot_get_item_amount, ":item_ammo", ":craftsman_troop", ":capacity_iterator"),
                #(troop_inventory_slot_get_item_max_amount, ":item_max_ammo", ":craftsman_troop", ":capacity_iterator"),
                #(eq, ":item_ammo", ":item_max_ammo"),

				(val_add, ":2ary_inputs_taken_from_warehouse", 1),
			(try_end),
		  
		    (try_begin),
				(gt, ":inputs_taken_from_warehouse", 0),
				(val_sub, ":inputs_taken_from_market", ":inputs_taken_from_warehouse"),
				(store_mul, ":savings_from_warehoused_inputs",	":price_of_single_input", ":inputs_taken_from_warehouse"),
				(val_add, ":net_profit", ":savings_from_warehoused_inputs"),
			(try_end),	
		    (try_begin),
				(gt, ":2ary_inputs_taken_from_warehouse", 0),
				(val_sub, ":2ary_inputs_taken_from_market", ":2ary_inputs_taken_from_warehouse"),
				(assign, ":savings_from_warehoused_inputs",	":price_of_secondary_input"),
				(val_add, ":net_profit", ":savings_from_warehoused_inputs"),
			(try_end),					
		  (try_end),
		  
		  #If the transaction is for real, and not just a budget check
		  (try_begin),
		    (eq, "$g_apply_budget_report_to_gold", 1),
			(item_get_slot, ":raw_material", ":enterprise_output", slot_item_primary_raw_material),
			(troop_remove_items, ":craftsman_troop", ":raw_material", ":inputs_taken_from_warehouse"),
			(item_get_slot, ":secondary_raw_material", ":enterprise_output", slot_item_secondary_raw_material),
			(troop_remove_items, ":craftsman_troop", ":secondary_raw_material", ":2ary_inputs_taken_from_warehouse"),
			
			#Affect prices by intputs added to market
			(store_sub, ":item_slot_no", ":raw_material", trade_goods_begin),
			(val_add, ":item_slot_no", slot_town_trade_good_prices_begin),
			(party_get_slot, ":current_index", ":center_no", ":item_slot_no"),			
			(store_mul, ":impact_on_price", ":outputs_added_to_market", 15),
			(val_add, ":current_index", ":impact_on_price"),
			(party_set_slot, ":center_no", ":item_slot_no",":current_index"),			
			
			(try_begin),
				(gt, ":2ary_inputs_taken_from_market", 0),
				(store_sub, ":item_slot_no", ":secondary_raw_material", trade_goods_begin),
				(val_add, ":item_slot_no", slot_town_trade_good_prices_begin),
				(party_get_slot, ":current_index", ":center_no", ":item_slot_no"),			
				(val_add, ":current_index", 15),
				(party_set_slot, ":center_no", ":item_slot_no",":current_index"),			
			(try_end),
		  (try_end),		  
		  		  
		  (call_script, "script_get_enterprise_name", ":enterprise_output"),
		  (str_store_string, s5, reg0),
		  
          (create_text_overlay, reg1, "str_enterprise_s5_at_s0", 0),
          (position_set_x, pos1, 900),
          (position_set_y, pos1, 900),
          (overlay_set_size, reg1, pos1),
          (position_set_x, pos1, 25),
          (position_set_y, pos1, ":cur_y"),
          (overlay_set_position, reg1, pos1),
		  
          (assign, reg0, ":net_profit"),
		  
		  #Enterprise revenue strings
          (try_begin),
     	    (store_faction_of_party, ":faction_no", ":center_no"),
		    (store_relation, ":relation", ":faction_no", "$players_kingdom"),
		    (lt, ":relation", 0),
		    (assign, reg0, 0), 
		    (assign, ":net_profit", 0), 
		  
            (create_text_overlay, reg1, "str_under_sequestration", tf_right_align|tf_single_line),
            (overlay_set_color, reg1, 0xFF0000),		  
		  (else_try),
		    (ge, reg0, 0), 
            (create_text_overlay, reg1, "@{!}{reg0}", tf_right_align|tf_single_line),
            (overlay_set_color, reg1, 0x00AA00),
          (else_try),
            (create_text_overlay, reg1, "@{!}{reg0}", tf_right_align|tf_single_line),
            (overlay_set_color, reg1, 0xFF0000),
          (try_end),
		  
          (val_add, ":all_centers_accumulated_total", ":net_profit"),
          (val_add, ":net_change", ":net_profit"),		  
		  
          (position_set_x, pos1, 900),
          (position_set_y, pos1, 900),
          (overlay_set_size, reg1, pos1),
          (position_set_x, pos1, 500),
          (position_set_y, pos1, ":cur_y"),
          (overlay_set_position, reg1, pos1),
          (val_sub, ":cur_y", 27),
        (try_end),

		#Enterprise ends, taxes begin
        (party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
        (party_get_slot, ":accumulated_rents", ":center_no", slot_center_accumulated_rents),
        (party_get_slot, ":accumulated_tariffs", ":center_no", slot_center_accumulated_tariffs),
		
        (store_add, ":accumulated_total", ":accumulated_rents", ":accumulated_tariffs"),
        (val_add, ":all_centers_accumulated_total", ":accumulated_total"),
        (val_add, ":all_centers_accumulated_taxes_and_rents", ":accumulated_total"),
        (val_add, ":net_change", ":accumulated_total"),
        (str_store_party_name, s0, ":center_no"),
        ##diplomacy begin
        (try_begin),
          (neg|is_between, ":center_no", castles_begin, castles_end),
          (party_get_slot, ":tax_rate", ":center_no", dplmc_slot_center_taxation),
          (neq, ":tax_rate", 0),
          (call_script, "script_dplmc_describe_tax_rate_to_s50", ":tax_rate"),
          (str_store_string, s0, "@{s0} ({s50})"),
        (try_end),
        ##diplomacy end
        (create_text_overlay, reg1, "str_rents_from_s0", 0),
        ##diplomacy begin
        (str_store_party_name, s0, ":center_no"),
        ##diplomacy end
        (position_set_x, pos1, 900),
        (position_set_y, pos1, 900),
        (overlay_set_size, reg1, pos1),
        (position_set_x, pos1, 25),
        (position_set_y, pos1, ":cur_y"),
        (overlay_set_position, reg1, pos1),
        (try_begin),
          (gt, ":accumulated_rents", 0),
          (assign, reg0, ":accumulated_rents"),
          (create_text_overlay, reg1, "@{!}{reg0}", tf_right_align|tf_single_line),
          (overlay_set_color, reg1, 0x00AA00),
        (else_try),
          (create_text_overlay, reg1, "@None", tf_right_align|tf_single_line),
        (try_end),
        (position_set_x, pos1, 900),
        (position_set_y, pos1, 900),
        (overlay_set_size, reg1, pos1),
        (position_set_x, pos1, 500),
        (position_set_y, pos1, ":cur_y"),
        (overlay_set_position, reg1, pos1),
        (val_sub, ":cur_y", 27),
		
        (try_begin),
          (is_between, ":center_no", towns_begin, towns_end),
          (create_text_overlay, reg1, "str_tariffs_from_s0", 0),
          (position_set_x, pos1, 900),
          (position_set_y, pos1, 900),
          (overlay_set_size, reg1, pos1),
          (position_set_x, pos1, 25),
          (position_set_y, pos1, ":cur_y"),
          (overlay_set_position, reg1, pos1),
          (try_begin),
            (gt, ":accumulated_tariffs", 0),
            (assign, reg0, ":accumulated_tariffs"),
            (create_text_overlay, reg1, "@{!}{reg0}", tf_right_align|tf_single_line),
            (overlay_set_color, reg1, 0x00AA00),
          (else_try),
            (create_text_overlay, reg1, "@None", tf_right_align|tf_single_line),
          (try_end),
          (position_set_x, pos1, 900),
          (position_set_y, pos1, 900),
          (overlay_set_size, reg1, pos1),
          (position_set_x, pos1, 500),
          (position_set_y, pos1, ":cur_y"),
          (overlay_set_position, reg1, pos1),
          (val_sub, ":cur_y", 27),
        (try_end),								
      (try_end),

      (try_begin),
        (gt, "$players_kingdom", 0),
        (neq, "$players_kingdom", "fac_player_supporters_faction"),
        (neq, "$players_kingdom", "fac_player_faction"),
        (eq, "$player_has_homage", 0),
        (str_store_faction_name, s0, "$players_kingdom"),
        (create_text_overlay, reg1, "str_mercenary_payment_from_s0", 0),
        (position_set_x, pos1, 900),
        (position_set_y, pos1, 900),
        (overlay_set_size, reg1, pos1),
        (position_set_x, pos1, 25),
        (position_set_y, pos1, ":cur_y"),
        (overlay_set_position, reg1, pos1),
        (call_script, "script_party_calculate_strength", "p_main_party", 0),
        (assign, ":offer_value", reg0),
        (val_div, ":offer_value", 2),
        (val_add, ":offer_value", 30),
        (call_script, "script_round_value", ":offer_value"),
        (val_add, ":net_change", reg0),
        (create_text_overlay, reg1, "@{!}{reg0}", tf_right_align|tf_single_line),
        (position_set_x, pos1, 900),
        (position_set_y, pos1, 900),
        (overlay_set_size, reg1, pos1),
        (overlay_set_color, reg1, 0x00AA00),
        (position_set_x, pos1, 500),
        (position_set_y, pos1, ":cur_y"),
        (overlay_set_position, reg1, pos1),
        (val_sub, ":cur_y", 27),
      (try_end),
      
      (try_begin),
        (gt, ":num_owned_center_values_for_tax_efficiency", ":num_centers_needed_for_efficiency_loss"),
        (gt, ":all_centers_accumulated_total", 0),
        (store_sub, ":ratio_lost", ":num_owned_center_values_for_tax_efficiency", ":num_centers_needed_for_efficiency_loss"),
        (val_mul, ":ratio_lost", ":tax_efficiency_loss_ratio_per_center"),
        (val_min, ":ratio_lost", 65),
                
        #(store_mul, ":tax_lost", ":all_centers_accumulated_total", ":ratio_lost"),
        (store_mul, ":tax_lost", ":all_centers_accumulated_taxes_and_rents", ":ratio_lost"),
        (val_div, ":tax_lost", 100),
        ##diplomacy begin
        (assign, ":percent", 0),
        (try_begin),
          (gt, "$g_player_chamberlain", 0),
          (val_add, ":percent", 10),
        (try_end),
        (try_begin),
		  ##diplomacy start+ Handle player is co-ruler of NPC kingdom
		  (try_begin),
			#Copy slot values
		    (is_between, ":alt_rule_faction", npc_kingdoms_begin, npc_kingdoms_end),
			(neg|faction_slot_eq, "fac_player_supporters_faction", slot_faction_state, sfs_active),

			(faction_get_slot, reg0, ":alt_rule_faction", dplmc_slot_faction_serfdom),
			(faction_set_slot, "fac_player_supporters_faction", dplmc_slot_faction_serfdom,  reg0),

			(faction_get_slot, reg0, ":alt_rule_faction", dplmc_slot_faction_centralization),
			(faction_set_slot, "fac_player_supporters_faction", dplmc_slot_faction_centralization,  reg0),

			(faction_get_slot, reg0, ":alt_rule_faction", dplmc_slot_faction_quality),
			(faction_set_slot, "fac_player_supporters_faction", dplmc_slot_faction_quality,  reg0),

			(faction_get_slot, reg0, ":alt_rule_faction", dplmc_slot_faction_aristocracy),
			(faction_set_slot, "fac_player_supporters_faction", dplmc_slot_faction_aristocracy,  reg0),

			(faction_get_slot, reg0, ":alt_rule_faction", dplmc_slot_faction_mercantilism),
			(faction_set_slot, "fac_player_supporters_faction", dplmc_slot_faction_mercantilism,  reg0),
		  (try_end),

		  (this_or_next|is_between, ":alt_rule_faction", npc_kingdoms_begin, npc_kingdoms_end),
		  ##diplomacy end+
          (faction_slot_eq, "fac_player_supporters_faction", slot_faction_state, sfs_active),
          (try_begin),
            (faction_get_slot, ":centralization", "fac_player_supporters_faction", dplmc_slot_faction_centralization),
            (neq, ":centralization", 0),
            (val_mul, ":centralization", 5),
            (val_add, ":percent", ":centralization"),
          (try_end),
          (try_begin),
            (faction_get_slot, ":serfdom", "fac_player_supporters_faction", dplmc_slot_faction_serfdom),
            (neq, ":serfdom", 0),
            (val_mul, ":serfdom", 3),
            (val_add, ":percent", ":serfdom"),
          (try_end),
        (else_try),
          (gt, "$players_kingdom", 0),
          (faction_get_slot, ":centralization", "$players_kingdom", dplmc_slot_faction_centralization),
          (neq, ":centralization", 0),
          (val_mul, ":centralization", -5),
          (val_add, ":percent", ":centralization"),
        (try_end),
        (try_begin),
          (gt, ":tax_lost", 0),
          (store_mul, ":save", ":tax_lost", ":percent"),
          (val_div, ":save", 100),
          (store_mul, ":percent", ":save", 100),
          (val_div, ":percent", ":tax_lost"),
          (val_sub, ":tax_lost", ":save"),
        (try_end),
         ##diplomacy end
        (val_sub, ":net_change", ":tax_lost"),
        ##diplomacy begin
        (try_begin),
          (gt, "$g_player_chamberlain", 0),
          (str_store_string, s55, "str_loss_due_to_tax_inefficiency"),
          (assign, reg0, ":percent"),
          (val_mul, reg0, -1),
	        (str_store_string, s55, "@{s55} ({reg0}%)"),
          (create_text_overlay, reg1, "@{s55}", 0),
        (else_try),
        ##diplomacy end
          (create_text_overlay, reg1, "str_loss_due_to_tax_inefficiency", 0),
        ##diplomacy begin
        (try_end),
        ##diplomacy end
        (position_set_x, pos1, 25),
        (position_set_y, pos1, ":cur_y"),
        (overlay_set_position, reg1, pos1),
        (position_set_x, pos1, 900),
        (position_set_y, pos1, 900),
        (overlay_set_size, reg1, pos1),
        (store_mul, reg0, ":tax_lost", -1),
        (create_text_overlay, reg1, "@{!}{reg0}", tf_right_align|tf_single_line),
        (position_set_x, pos1, 900),
        (position_set_y, pos1, 900),
        (overlay_set_size, reg1, pos1),
        (overlay_set_color, reg1, 0xFF0000),
        (position_set_x, pos1, 500),
        (position_set_y, pos1, ":cur_y"),
        (overlay_set_position, reg1, pos1),
        (val_sub, ":cur_y", 27),
      (try_end),

      (try_for_parties, ":party_no"),
        (assign, ":garrison_troop", 0),
        (try_begin),
		  #gekokujo 3.0 microfactions! start
		  #let's include fort garrisons in budget
          (party_slot_eq, ":party_no", slot_party_type, spt_fort),
		  (party_slot_eq, ":party_no", slot_fort_captured, 1),
		  (assign, ":garrison_troop", 1),
		  #gekokujo 3.0 microfactions! end
		(else_try),  
          (this_or_next|party_slot_eq, ":party_no", slot_party_type, spt_town),
          (party_slot_eq, ":party_no", slot_party_type, spt_castle),
          (party_slot_eq, ":party_no", slot_town_lord, "trp_player"),
          ##diplomacy begin
          (neg|party_slot_eq, ":party_no", slot_village_infested_by_bandits, "trp_peasant_woman"),
          ##diplomacy end
          (assign, ":garrison_troop", 1),
		(else_try),  
          (this_or_next|party_slot_eq, ":party_no", slot_party_type, spt_town),
			(party_slot_eq, ":party_no", slot_party_type, spt_castle),
          (neg|party_slot_ge, ":party_no", slot_town_lord, 1), #unassigned
		  (store_faction_of_party, ":center_faction", ":party_no"),
		  ##diplomacy start+ Either player is co-ruler of faction, or this is fac_player_supporters_faction
		  (this_or_next|eq, ":alt_rule_faction", ":center_faction"),
		  ##diplomacy end+
		  (eq, ":center_faction", "fac_player_supporters_faction"),
		  ##diplomacy start+
		  (this_or_next|is_between, ":alt_rule_faction", npc_kingdoms_begin, npc_kingdoms_end),#Player is co-ruler of NPC faction
		  ##diplomacy end+
		  (faction_slot_eq, "fac_player_supporters_faction", slot_faction_leader, "trp_player"),
          (assign, ":garrison_troop", 1),			  
        (try_end),
		
        ##diplomacy begin
        (assign, ":patrol_troop", 0),
        (try_begin),
          (party_slot_eq, ":party_no",slot_party_type, spt_patrol),
          (party_slot_eq, ":party_no", dplmc_slot_party_mission_diplomacy, "trp_player"),
          (assign, ":patrol_troop", 1),
        (try_end),
        (this_or_next|eq, ":patrol_troop", 1),
        ##diplomacy end
        (this_or_next|eq, ":party_no", "p_main_party"),
        (eq, ":garrison_troop", 1),
		
        (assign, ":total_wage", 0),
        (party_get_num_companion_stacks, ":num_stacks", ":party_no"),
        (try_for_range, ":i_stack", 0, ":num_stacks"),
          (party_stack_get_troop_id, ":stack_troop", ":party_no", ":i_stack"),
          (party_stack_get_size, ":stack_size", ":party_no", ":i_stack"),
          (call_script, "script_game_get_troop_wage", ":stack_troop", ":party_no"),
          (assign, ":cur_wage", reg0),
          (val_mul, ":cur_wage", ":stack_size"),
          (val_add, ":total_wage", ":cur_wage"),
        (try_end),
		
        (try_begin),
          (eq, ":garrison_troop", 1),
          (val_div, ":total_wage", 2), #Half payment for garrisons
        (else_try),
          (eq, ":party_no", "p_main_party"),
          (store_sub, ":total_payment_ratio", 14, "$g_cur_week_half_daily_wage_payments"), #between 0 and 7
          (val_mul, ":total_wage", ":total_payment_ratio"),
          (val_div, ":total_wage", 14),
        (try_end),
		
##        (gt, ":total_wage", 0),
        (val_mul, ":total_wage", -1),
        (val_add, ":net_change", ":total_wage"),
        (str_store_party_name, s0, ":party_no"),
		
        (try_begin),
          (eq, ":party_no", "p_main_party"),
          (str_store_string, s0, "str_s0s_party"),
        (try_end),
		
        (create_text_overlay, reg1, "str_wages_for_s0", 0),
        (position_set_x, pos1, 900),
        (position_set_y, pos1, 900),
        (overlay_set_size, reg1, pos1),
        (position_set_x, pos1, 25),
        (position_set_y, pos1, ":cur_y"),
        (overlay_set_position, reg1, pos1),
		
        (try_begin),
          (lt, ":total_wage", 0),
          (assign, reg0, ":total_wage"),
          (create_text_overlay, reg1, "@{!}{reg0}", tf_right_align|tf_single_line),
          (overlay_set_color, reg1, 0xFF0000),
        (else_try),
          (create_text_overlay, reg1, "@None", tf_right_align|tf_single_line),
        (try_end),
		
        (position_set_x, pos1, 900),
        (position_set_y, pos1, 900),
        (overlay_set_size, reg1, pos1),
        (position_set_x, pos1, 500),
        (position_set_y, pos1, ":cur_y"),
        (overlay_set_position, reg1, pos1),
        (val_sub, ":cur_y", 27),
      (try_end),

      (try_begin),
        (gt, "$g_player_debt_to_party_members", 0),
        (val_sub, ":net_change", "$g_player_debt_to_party_members"),
        (create_text_overlay, reg1, "str_earlier_debts", 0),
        (position_set_x, pos1, 900),
        (position_set_y, pos1, 900),
        (overlay_set_size, reg1, pos1),
        (position_set_x, pos1, 25),
        (position_set_y, pos1, ":cur_y"),
        (overlay_set_position, reg1, pos1),
        (store_mul, reg0, "$g_player_debt_to_party_members", -1),
        (create_text_overlay, reg1, "@{!}{reg0}", tf_right_align|tf_single_line),
        (position_set_x, pos1, 900),
        (position_set_y, pos1, 900),
        (overlay_set_size, reg1, pos1),
        (overlay_set_color, reg1, 0xFF0000),
        (position_set_x, pos1, 500),
        (position_set_y, pos1, ":cur_y"),
        (overlay_set_position, reg1, pos1),
        (val_sub, ":cur_y", 27),
      (try_end),
      ##diplomacy begin
      (assign, ":staff_salary", 0),
      (try_begin),
        (gt, "$g_player_minister", 0),
        (val_add, ":staff_salary", 15),
      (try_end),
      (try_begin),
        (troop_slot_ge, "trp_player", slot_troop_spouse, 0),
        (val_add, ":staff_salary", 10),
      (try_end),
      (try_begin),
        (gt, "$g_player_chamberlain", 0),
        (val_add, ":staff_salary", 15),
      (try_end),
      (try_begin),
        (gt, "$g_player_constable", 0),
        (val_add, ":staff_salary", 15),
      (try_end),
      (try_begin),
        (gt, "$g_player_chancellor", 0),
        (val_add, ":staff_salary", 20),
      (try_end),

      (try_begin),
        (gt, ":staff_salary", 0),
        (val_sub, ":net_change", ":staff_salary"),
        (create_text_overlay, reg1, "@Staff:", 0),
        (position_set_x, pos1, 900),
        (position_set_y, pos1, 900),
        (overlay_set_size, reg1, pos1),
        (position_set_x, pos1, 25),
        (position_set_y, pos1, ":cur_y"),
        (overlay_set_position, reg1, pos1),
        (store_mul, reg0, ":staff_salary", -1),
        (create_text_overlay, reg1, "@{!}{reg0}", tf_right_align|tf_single_line),
        (position_set_x, pos1, 900),
        (position_set_y, pos1, 900),
        (overlay_set_size, reg1, pos1),
        (overlay_set_color, reg1, 0xFF0000),
        (position_set_x, pos1, 500),
        (position_set_y, pos1, ":cur_y"),
        (overlay_set_position, reg1, pos1),
        (val_sub, ":cur_y", 27),
      (try_end),
      ##diplomacy end
      (create_mesh_overlay, reg1, "mesh_white_plane"),
      (overlay_set_color, reg1, 0x000000),
      (position_set_x, pos1, 24000),
      (position_set_y, pos1, 50),
      (overlay_set_size, reg1, pos1),
      (position_set_x, pos1, 25),
      (store_add, ":line_y", ":cur_y", 25),
      (position_set_y, pos1, ":line_y"),
      (overlay_set_position, reg1, pos1),
      (create_text_overlay, reg1, "str_net_change", 0),
      (position_set_x, pos1, 900),
      (position_set_y, pos1, 900),
      (overlay_set_size, reg1, pos1),
      (position_set_x, pos1, 25),
      (position_set_y, pos1, ":cur_y"),
      (overlay_set_position, reg1, pos1),
      (assign, reg0, ":net_change"),
      (create_text_overlay, reg1, "@{!}{reg0}", tf_right_align|tf_single_line),
      (position_set_x, pos1, 900),
      (position_set_y, pos1, 900),
      (overlay_set_size, reg1, pos1),
      (try_begin),
        (gt, reg0, 0),
        (overlay_set_color, reg1, 0x00AA00),
      (else_try),
        (lt, reg0, 0),
        (overlay_set_color, reg1, 0xFF0000),
      (try_end),
      (position_set_x, pos1, 500),
      (position_set_y, pos1, ":cur_y"),
      (overlay_set_position, reg1, pos1),
      (val_sub, ":cur_y", 27),
      (create_text_overlay, reg1, "str_earlier_wealth", 0),
      (position_set_x, pos1, 900),
      (position_set_y, pos1, 900),
      (overlay_set_size, reg1, pos1),
      (position_set_x, pos1, 25),
      (position_set_y, pos1, ":cur_y"),
      (overlay_set_position, reg1, pos1),
      ##diplomacy begin
      (try_begin),
        (gt, "$g_player_chamberlain", 0),
        (store_troop_gold, ":player_wealth", "trp_household_possessions"),
      (else_try),
      ##diplomacy end
      (store_troop_gold, ":player_wealth", "trp_player"),
      ##diplomacy begin
      (try_end),
      ##diplomacy end
      (assign, reg0, ":player_wealth"),
      (create_text_overlay, reg1, "@{!}{reg0}", tf_right_align|tf_single_line),
      (position_set_x, pos1, 900),
      (position_set_y, pos1, 900),
      (overlay_set_size, reg1, pos1),
      (position_set_x, pos1, 500),
      (position_set_y, pos1, ":cur_y"),
      (overlay_set_position, reg1, pos1),
      (val_sub, ":cur_y", 27),
      (val_mul, ":net_change", -1),
      ##diplomacy begin
      (assign, ":cash_to_pay", 0),
      ##diplomacy end
      (try_begin),
        (ge, ":player_wealth", ":net_change"),
        (assign, ":player_wealth_dif", ":net_change"),
        (assign, ":player_new_debt_to_party_members", 0),
      (else_try),
        (assign, ":player_wealth_dif", ":player_wealth"),
        (store_sub, ":player_new_debt_to_party_members", ":net_change", ":player_wealth"),
        ##diplomacy begin
        (try_begin),
          (gt, "$g_player_chamberlain", 0),
          (store_troop_gold, ":player_inv_wealth", "trp_player"),

          (try_begin), #drawing debts from personal money
            (ge, ":player_inv_wealth", ":player_new_debt_to_party_members"),
            (assign, ":cash_to_pay", ":player_new_debt_to_party_members"),
            (assign, ":player_new_debt_to_party_members", 0),
          (else_try),
            (assign, ":cash_to_pay", ":player_inv_wealth"),
            (val_sub, ":player_new_debt_to_party_members",":player_inv_wealth"),
          (try_end),

          (try_begin),
            (eq, "$g_apply_budget_report_to_gold", 1),
            (troop_remove_gold, "trp_player", ":cash_to_pay"),
            (assign, reg0, ":cash_to_pay"),
            (display_message, "@You paid {reg0} cash to liquidate a debt"),
          (try_end),
        (try_end),
        ##diplomacy end
      (try_end),
      (create_text_overlay, reg1, "str_new_wealth", 0),
      (position_set_x, pos1, 900),
      (position_set_y, pos1, 900),
      (overlay_set_size, reg1, pos1),
      (position_set_x, pos1, 25),
      (position_set_y, pos1, ":cur_y"),
      (overlay_set_position, reg1, pos1),
      (store_sub, reg0, ":player_wealth", ":player_wealth_dif"),
      (create_text_overlay, reg1, "@{!}{reg0}", tf_right_align|tf_single_line),
      (position_set_x, pos1, 900),
      (position_set_y, pos1, 900),
      (overlay_set_size, reg1, pos1),
      (position_set_x, pos1, 500),
      (position_set_y, pos1, ":cur_y"),
      (overlay_set_position, reg1, pos1),
      (val_sub, ":cur_y", 27),
      ##diplomacy begin
      (try_begin),
        (gt, "$g_player_chamberlain", 0),
        (gt, ":cash_to_pay", 0),
        (create_text_overlay, reg1, "@Earlier cash:", 0),
        (position_set_x, pos1, 900),
        (position_set_y, pos1, 900),
        (overlay_set_size, reg1, pos1),
        (position_set_x, pos1, 25),
        (position_set_y, pos1, ":cur_y"),
        (overlay_set_position, reg1, pos1),
        (assign, reg0, ":player_inv_wealth"),
        (create_text_overlay, reg1, "@{!}{reg0}", tf_right_align|tf_single_line),
        (position_set_x, pos1, 900),
        (position_set_y, pos1, 900),
        (overlay_set_size, reg1, pos1),
        (position_set_x, pos1, 500),
        (position_set_y, pos1, ":cur_y"),
        (overlay_set_position, reg1, pos1),
        (val_sub, ":cur_y", 27),

        (create_text_overlay, reg1, "@New cash:", 0),
        (position_set_x, pos1, 900),
        (position_set_y, pos1, 900),
        (overlay_set_size, reg1, pos1),
        (position_set_x, pos1, 25),
        (position_set_y, pos1, ":cur_y"),
        (overlay_set_position, reg1, pos1),
        (store_sub, reg0, ":player_inv_wealth", ":cash_to_pay"),
        (create_text_overlay, reg1, "@{!}{reg0}", tf_right_align|tf_single_line),
        (position_set_x, pos1, 900),
        (position_set_y, pos1, 900),
        (overlay_set_size, reg1, pos1),
        (position_set_x, pos1, 500),
        (position_set_y, pos1, ":cur_y"),
        (overlay_set_position, reg1, pos1),
        (val_sub, ":cur_y", 27),
      (try_end),
      ##diplomacy end

      (try_begin),
        (gt, ":player_new_debt_to_party_members", 0),
        (create_text_overlay, reg1, "str_new_debts", 0),
        (position_set_x, pos1, 900),
        (position_set_y, pos1, 900),
        (overlay_set_size, reg1, pos1),
        (position_set_x, pos1, 25),
        (position_set_y, pos1, ":cur_y"),
        (overlay_set_position, reg1, pos1),
        (assign, reg0, ":player_new_debt_to_party_members"),
        (create_text_overlay, reg1, "@{!}{reg0}", tf_right_align|tf_single_line),
        (position_set_x, pos1, 900),
        (position_set_y, pos1, 900),
        (overlay_set_size, reg1, pos1),
        (position_set_x, pos1, 500),
        (position_set_y, pos1, ":cur_y"),
        (overlay_set_position, reg1, pos1),
        (val_sub, ":cur_y", 27),
        (neq, "$g_apply_budget_report_to_gold", 0),
        (call_script, "script_objectionable_action", tmt_egalitarian, "str_men_unpaid"),
      (try_end),

      (set_container_overlay, -1),

      (create_button_overlay, "$g_presentation_obj_budget_report_1", "@Continue..."),
      (position_set_x, pos1, 225),
      (position_set_y, pos1, 60),
      (overlay_set_position, "$g_presentation_obj_budget_report_1", pos1),

      (try_begin),
        (eq, "$g_apply_budget_report_to_gold", 1),
        (assign, "$g_player_debt_to_party_members", ":player_new_debt_to_party_members"),
        (try_begin),
          (gt, ":player_wealth_dif", 0),
          ##diplomacy begin
          (try_begin),
            (gt, "$g_player_chamberlain", 0),
            (call_script, "script_dplmc_withdraw_from_treasury", ":player_wealth_dif"),
          (else_try),
          ##diplomacy end
            (troop_remove_gold, "trp_player", ":player_wealth_dif"),
          ##diplomacy begin
          (try_end),
          ##diplomacy end
        (else_try),
          (val_mul, ":player_wealth_dif", -1),
          ##diplomacy begin
          (try_begin),
            (gt, "$g_player_chamberlain", 0),
            (call_script, "script_dplmc_pay_into_treasury", ":player_wealth_dif"),
          (else_try),
          ##diplomacy end
            (troop_add_gold, "trp_player", ":player_wealth_dif"),
          ##diplomacy begin
          (try_end),
          ##diplomacy end
        (try_end),
        (try_for_range, ":center_no", centers_begin, centers_end),
          (party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
          (party_set_slot, ":center_no", slot_center_accumulated_rents, 0),
          (party_set_slot, ":center_no", slot_center_accumulated_tariffs, 0),
        (try_end),
        (assign, "$g_cur_week_half_daily_wage_payments", 0),#Reseting the weekly half wage payments
      (try_end),
      ]),
    (ti_on_presentation_event_state_change,
     [(store_trigger_param_1, ":object"),
      (try_begin),
        (eq, ":object", "$g_presentation_obj_budget_report_1"),
        (presentation_set_duration, 0),
      (try_end),
      ]),
    ]),
  #gekokujo world map end

##diplomacy begin
  ("dplmc_autoloot_upgrade_management", 0, mesh_load_window, [
    (ti_on_presentation_load,
     [
      (set_fixed_point_multiplier, 1000),
      (presentation_set_duration, 999999),

      # done
      (create_game_button_overlay, "$g_presentation_obj_10", "@Done"),
      (position_set_x, pos1, 900),
      (position_set_y, pos1, 25),
      (overlay_set_position, "$g_presentation_obj_10", pos1),

      ## current hero
      # character picture
      (create_mesh_overlay_with_tableau_material, reg0, -1, "tableau_troop_note_mesh", "$temp"),
      (position_set_x, pos1, 500),
      (position_set_y, pos1, 500),
      (overlay_set_size, reg0, pos1),
      (position_set_x, pos1, 200),
      (position_set_y, pos1, 560),
      (overlay_set_position, reg0, pos1),

      (str_store_troop_name, s1, "$temp"),
      (store_character_level, ":troop_level", "$temp"),
      (assign, reg1, ":troop_level"),
      (str_store_string, s1, "@Name: {s1}^Level: {reg1}"),

      (store_troop_health, ":cur_hp", "$temp", 1),
      (call_script, "script_dplmc_get_troop_max_hp", "$temp"),
      (assign, reg1, ":cur_hp"),
      (assign, reg2, reg0),
      (str_store_string, s1, "@{s1}^HP: {reg1}/{reg2}"),

      (create_text_overlay, reg1, "@{s1}", tf_double_space),
      (position_set_x, pos1, 380),
      (position_set_y, pos1, 560),
      (overlay_set_position, reg1, pos1),

      # title
      (create_text_overlay, reg1, "@Weapon upgrade settings:", tf_center_justify|tf_vertical_align_center),
      (position_set_x, pos1, 445),
      (position_set_y, pos1, 530),
      (overlay_set_position, reg1, pos1),

      # init trp_temp_array_c
      (assign, ":sub_overlay_id", 0),
      (try_for_range_backwards, ":item_type", 0, itp_type_animal),
        (this_or_next|is_between, ":item_type", itp_type_one_handed_wpn, itp_type_goods),
        (this_or_next|is_between, ":item_type", itp_type_pistol, itp_type_animal),
        (eq, ":item_type", 0),
        (troop_set_slot, "trp_temp_array_c", ":sub_overlay_id", ":item_type"),
        (val_add, ":sub_overlay_id", 1),
      (try_end),

      # settings 1
      # set 1: wpn slot button
      (position_set_x, pos1, 270),
      (position_set_y, pos1, 450),
      (create_combo_button_overlay, "$g_presentation_obj_1"),
      (overlay_set_position, "$g_presentation_obj_1", pos1),
      (assign, ":sub_overlay_id", 0),
      (call_script, "script_dplmc_get_current_item_for_autoloot", 0),
      (try_for_range_backwards, ":item_type", 0, itp_type_animal),
        (this_or_next|is_between, ":item_type", itp_type_one_handed_wpn, itp_type_goods),
        (this_or_next|is_between, ":item_type", itp_type_pistol, itp_type_animal),
        (eq, ":item_type", 0),
        (store_add, ":out_string", "str_dplmc_hero_wpn_slot_none", ":item_type"),
        (str_store_string, s0, ":out_string"),
        (overlay_add_item, "$g_presentation_obj_1", s0),
        (try_begin),
          (troop_slot_eq, "$temp", dplmc_slot_upgrade_wpn_0, ":item_type"),
          (overlay_set_val, "$g_presentation_obj_1", ":sub_overlay_id"),
        (try_end),
        (val_add, ":sub_overlay_id", 1),
      (try_end),

      (position_set_y, pos1, 420),
      (create_combo_button_overlay, "$g_presentation_obj_2"),
      (overlay_set_position, "$g_presentation_obj_2", pos1),
      (assign, ":sub_overlay_id", 0),
      (call_script, "script_dplmc_get_current_item_for_autoloot", 1),
      (try_for_range_backwards, ":item_type", 0, itp_type_animal),
        (this_or_next|is_between, ":item_type", itp_type_one_handed_wpn, itp_type_goods),
        (this_or_next|is_between, ":item_type", itp_type_pistol, itp_type_animal),
        (eq, ":item_type", 0),
        (store_add, ":out_string", "str_dplmc_hero_wpn_slot_none", ":item_type"),
        (str_store_string, s0, ":out_string"),
        (overlay_add_item, "$g_presentation_obj_2", s0),
        (try_begin),
          (troop_slot_eq, "$temp", dplmc_slot_upgrade_wpn_1, ":item_type"),
          (overlay_set_val, "$g_presentation_obj_2", ":sub_overlay_id"),
        (try_end),
        (val_add, ":sub_overlay_id", 1),
      (try_end),

      (position_set_y, pos1, 390),
      (create_combo_button_overlay, "$g_presentation_obj_3"),
      (overlay_set_position, "$g_presentation_obj_3", pos1),
      (assign, ":sub_overlay_id", 0),
      (call_script, "script_dplmc_get_current_item_for_autoloot", 2),
      (try_for_range_backwards, ":item_type", 0, itp_type_animal),
        (this_or_next|is_between, ":item_type", itp_type_one_handed_wpn, itp_type_goods),
        (this_or_next|is_between, ":item_type", itp_type_pistol, itp_type_animal),
        (eq, ":item_type", 0),
        (store_add, ":out_string", "str_dplmc_hero_wpn_slot_none", ":item_type"),
        (str_store_string, s0, ":out_string"),
        (overlay_add_item, "$g_presentation_obj_3", s0),
        (try_begin),
          (troop_slot_eq, "$temp", dplmc_slot_upgrade_wpn_2, ":item_type"),
          (overlay_set_val, "$g_presentation_obj_3", ":sub_overlay_id"),
        (try_end),
        (val_add, ":sub_overlay_id", 1),
      (try_end),

      (position_set_y, pos1, 360),
      (create_combo_button_overlay, "$g_presentation_obj_4"),
      (overlay_set_position, "$g_presentation_obj_4", pos1),
      (assign, ":sub_overlay_id", 0),
      (call_script, "script_dplmc_get_current_item_for_autoloot", 3),
      (try_for_range_backwards, ":item_type", 0, itp_type_animal),
        (this_or_next|is_between, ":item_type", itp_type_one_handed_wpn, itp_type_goods),
        (this_or_next|is_between, ":item_type", itp_type_pistol, itp_type_animal),
        (eq, ":item_type", 0),
        (store_add, ":out_string", "str_dplmc_hero_wpn_slot_none", ":item_type"),
        (str_store_string, s0, ":out_string"),
        (overlay_add_item, "$g_presentation_obj_4", s0),
        (try_begin),
          (troop_slot_eq, "$temp", dplmc_slot_upgrade_wpn_3, ":item_type"),
          (overlay_set_val, "$g_presentation_obj_4", ":sub_overlay_id"),
        (try_end),
        (val_add, ":sub_overlay_id", 1),
      (try_end),

      (position_set_x, pos1, 1000),
      (position_set_y, pos1, 800),
      (overlay_set_size, "$g_presentation_obj_1", pos1),
      (overlay_set_size, "$g_presentation_obj_2", pos1),
      (overlay_set_size, "$g_presentation_obj_3", pos1),
      (overlay_set_size, "$g_presentation_obj_4", pos1),
      # set 1: apply to all
      (position_set_x, pos1, 128),
      (position_set_y, pos1, 310),
      (create_image_button_overlay, "$g_presentation_obj_11", "mesh_longer_button", "mesh_longer_button_down"),
      (overlay_set_position, "$g_presentation_obj_11", pos1),
      (position_set_x, pos1, 270),
      (position_set_y, pos1, 325),
      (create_text_overlay, reg1, "@Apply to everyone", tf_center_justify|tf_vertical_align_center),
      (overlay_set_position, reg1, pos1),

      # upgrade armor and horse
      # text
      (position_set_x, pos1, 300),
      (position_set_y, pos1, 155),
      (create_text_overlay, reg1, "@Upgrade armor ", tf_center_justify|tf_vertical_align_center),
      (overlay_set_position, reg1, pos1),
      (position_set_y, pos1, 105),
      (create_text_overlay, reg1, "@Upgrade horse ", tf_center_justify|tf_vertical_align_center),
      (overlay_set_position, reg1, pos1),
      # checkbox
      (position_set_x, pos1, 180),
      (position_set_y, pos1, 148),
      (create_check_box_overlay, "$g_presentation_obj_13", "mesh_checkbox_off", "mesh_checkbox_on"),
      (overlay_set_position, "$g_presentation_obj_13", pos1),
      (troop_get_slot,":upg_armor", "$temp",dplmc_slot_upgrade_armor),
      (overlay_set_val, "$g_presentation_obj_13", ":upg_armor"),
      (position_set_y, pos1, 98),
      (create_check_box_overlay, "$g_presentation_obj_14", "mesh_checkbox_off", "mesh_checkbox_on"),
      (overlay_set_position, "$g_presentation_obj_14", pos1),
      (troop_get_slot,":upg_horse", "$temp",dplmc_slot_upgrade_horse),
      (overlay_set_val, "$g_presentation_obj_14", ":upg_horse"),
      # long button
      (position_set_x, pos1, 418),
      (position_set_y, pos1, 140),
      (create_image_button_overlay, "$g_presentation_obj_15", "mesh_longer_button", "mesh_longer_button_down"),
      (overlay_set_position, "$g_presentation_obj_15", pos1),
      (position_set_y, pos1, 90),
      (create_image_button_overlay, "$g_presentation_obj_16", "mesh_longer_button", "mesh_longer_button_down"),
      (overlay_set_position, "$g_presentation_obj_16", pos1),
      (position_set_x, pos1, 560),
      (position_set_y, pos1, 155),
      (create_text_overlay, reg1, "@Apply to everyone", tf_center_justify|tf_vertical_align_center),
      (overlay_set_position, reg1, pos1),
      (position_set_y, pos1, 105),
      (create_text_overlay, reg1, "@Apply to everyone", tf_center_justify|tf_vertical_align_center),
      (overlay_set_position, reg1, pos1),

      # hero list
      (assign, ":pos_x", 900),
      (assign, ":pos_y", 600),
      (assign, ":num_of_heros", 0),
      (party_get_num_companion_stacks, ":num_stacks","p_main_party"),
      (try_for_range, ":i_stack", 1, ":num_stacks"),
        (party_stack_get_troop_id,":stack_troop","p_main_party",":i_stack"),
		#gekokujo 3.0 microfactions! include fort companions start
        #(is_between, ":stack_troop", companions_begin, companions_end),
        (is_between, ":stack_troop", companions_begin, fort_companions_end),
		#gekokujo 3.0 microfactions! include fort companions end
        (str_store_troop_name, s1, ":stack_troop"),
        (position_set_x, pos1, ":pos_x"),
        (position_set_y, pos1, ":pos_y"),
        (val_sub, ":pos_y", 30),
        (create_button_overlay, reg0, "@{s1}", tf_center_justify|tf_vertical_align_center),
        (overlay_set_position, reg0, pos1),

        (assign, ":trp_slot_prsnt_no", ":num_of_heros"),
        (troop_set_slot, "trp_temp_array_a", ":trp_slot_prsnt_no", reg0),
        (troop_set_slot, "trp_temp_array_b", ":trp_slot_prsnt_no", ":stack_troop"),
        (val_add, ":num_of_heros", 1),
      (try_end),
#      ####### mouse fix pos system #######
#      (call_script, "script_mouse_fix_pos_ready"),
#      ####### mouse fix pos system #######
     ]),

#    (ti_on_presentation_run,
#      [
#      ####### mouse fix pos system #######
#      (call_script, "script_mouse_fix_pos_run"),
#      ####### mouse fix pos system #######
#    ]),

    (ti_on_presentation_event_state_change,
     [
        (store_trigger_param_1, ":object"),
        (store_trigger_param_2, ":value"),

        (try_begin),
          (eq, ":object", "$g_presentation_obj_1"),
          (troop_get_slot, ":item_type", "trp_temp_array_c", ":value"),
          (troop_set_slot, "$temp", dplmc_slot_upgrade_wpn_0, ":item_type"),
          (start_presentation, "prsnt_dplmc_autoloot_upgrade_management"),
        (else_try),
          (eq, ":object", "$g_presentation_obj_2"),
          (troop_get_slot, ":item_type", "trp_temp_array_c", ":value"),
          (troop_set_slot, "$temp", dplmc_slot_upgrade_wpn_1, ":item_type"),
          (start_presentation, "prsnt_dplmc_autoloot_upgrade_management"),
        (else_try),
          (eq, ":object", "$g_presentation_obj_3"),
          (troop_get_slot, ":item_type", "trp_temp_array_c", ":value"),
          (troop_set_slot, "$temp", dplmc_slot_upgrade_wpn_2, ":item_type"),
          (start_presentation, "prsnt_dplmc_autoloot_upgrade_management"),
        (else_try),
          (eq, ":object", "$g_presentation_obj_4"),
          (troop_get_slot, ":item_type", "trp_temp_array_c", ":value"),
          (troop_set_slot, "$temp", dplmc_slot_upgrade_wpn_3, ":item_type"),
          (start_presentation, "prsnt_dplmc_autoloot_upgrade_management"),
        (else_try),
          (eq, ":object", "$g_presentation_obj_10"),
          (presentation_set_duration, 0),
        (else_try),
          (eq, ":object", "$g_presentation_obj_11"),
          (call_script, "script_dplmc_copy_upgrade_to_all_heroes", "$temp", dplmc_wpn_setting_1),
        (else_try),
          (eq, ":object", "$g_presentation_obj_13"),
          (troop_set_slot, "$temp", dplmc_slot_upgrade_armor, ":value"),
        (else_try),
          (eq, ":object", "$g_presentation_obj_14"),
          (troop_set_slot, "$temp", dplmc_slot_upgrade_horse, ":value"),
        (else_try),
          (eq, ":object", "$g_presentation_obj_15"),
          (call_script, "script_dplmc_copy_upgrade_to_all_heroes", "$temp", dplmc_armor_setting),
        (else_try),
          (eq, ":object", "$g_presentation_obj_16"),
          (call_script, "script_dplmc_copy_upgrade_to_all_heroes", "$temp", dplmc_horse_setting),
        (try_end),

        (assign, ":num_of_heros", 0),
        (party_get_num_companion_stacks, ":num_stacks","p_main_party"),
        (try_for_range, ":i_stack", 0, ":num_stacks"),
          (party_stack_get_troop_id,":stack_troop","p_main_party",":i_stack"),
		  #gekokujo 3.0 microfactions! include fort companions start
          #(is_between, ":stack_troop", companions_begin, companions_end),
          (is_between, ":stack_troop", companions_begin, fort_companions_end),
		  #gekokujo 3.0 microfactions! include fort companions end
          (assign, ":trp_slot_prsnt_no", ":num_of_heros"),
          (val_add, ":num_of_heros", 1),
          (troop_slot_eq, "trp_temp_array_a", ":trp_slot_prsnt_no", ":object"),
          (troop_get_slot, ":cur_troop", "trp_temp_array_b", ":trp_slot_prsnt_no"),
          (assign, "$temp", ":cur_troop"),
          (start_presentation, "prsnt_dplmc_autoloot_upgrade_management"),
        (try_end),
    ]),
  ]),
    ("dplmc_policy_management",0,mesh_load_window,[
      (ti_on_presentation_load,
       [
        (set_fixed_point_multiplier, 1000),
        (presentation_set_duration, 999999),
		##nested diplomacy start+ insert g_presentation_obj_5, g_presentation_obj_6 and increment others

		##Moved up here from below
        (faction_get_slot, ":centralization", "fac_player_supporters_faction", dplmc_slot_faction_centralization),
        (faction_get_slot, ":aristocratcy", "fac_player_supporters_faction", dplmc_slot_faction_aristocracy),
        (faction_get_slot, ":serfdom", "fac_player_supporters_faction", dplmc_slot_faction_serfdom),
        (faction_get_slot, ":quality", "fac_player_supporters_faction", dplmc_slot_faction_quality),
		(faction_get_slot, ":mercantilism", "fac_player_supporters_faction", dplmc_slot_faction_quality),#<- dplmc+ added

        # done
        (create_game_button_overlay, "$g_presentation_obj_12", "@Done"),#<- dplmc+ changed obj_10 to obj_12
        (position_set_x, pos1, 900),
        (position_set_y, pos1, 25),
        (overlay_set_position, "$g_presentation_obj_12", pos1),#<- dplmc_ changed obj_10 to obj_12

        # title
        (create_text_overlay, reg1, "@Select your domestic policy", tf_center_justify|tf_vertical_align_center),
        (position_set_x, pos1, 445),
        (position_set_y, pos1, 700),
        (overlay_set_position, reg1, pos1),

        (create_slider_overlay, "$g_presentation_obj_sliders_1", -3, 3),
        (create_slider_overlay, "$g_presentation_obj_sliders_2", -3, 3),
        (create_slider_overlay, "$g_presentation_obj_sliders_3", -3, 3),
        (create_slider_overlay, "$g_presentation_obj_sliders_4", -3, 3),
		(create_slider_overlay, "$g_presentation_obj_sliders_5", -3, 3),#<-dplmc+ added
        (assign, reg1, 25),
		##dplmc+ start incremented sliders by 1... (and changed since things might not be at their initial values)
		(store_add, ":text", "str_dplmc_neither_centralize_nor_decentralized", ":centralization"),
        (create_text_overlay, "$g_presentation_obj_sliders_6", ":text"),
		(store_add, ":text", "str_dplmc_neither_aristocratic_nor_plutocratic", ":aristocratcy"),
        (create_text_overlay, "$g_presentation_obj_sliders_7", ":text"),
		(store_add, ":text", "str_dplmc_mixture_serfs", ":serfdom"),
        (create_text_overlay, "$g_presentation_obj_sliders_8", ":text"),
		(store_add, ":text", "str_dplmc_mediocre_quality", ":quality"),
        (create_text_overlay, "$g_presentation_obj_sliders_9", ":text"),
		##dplmc+ end incremented sliders by 1
		(store_add, ":text", "str_dplmc_neither_mercantilist_nor_laissez_faire", ":mercantilism"),
		(create_text_overlay, "$g_presentation_obj_sliders_10", ":text"),#<- dplmc+ added

        (create_text_overlay, "$g_presentation_obj_1", "@Centralization:"),
        (create_text_overlay, "$g_presentation_obj_2", "@Aristocracy:"),
        (create_text_overlay, "$g_presentation_obj_3", "@Serfdom:"),
        (create_text_overlay, "$g_presentation_obj_4", "@Troop quality:"),
		(create_text_overlay, "$g_presentation_obj_5", "@Mercantilism:"),#<-- dplmc+ added
		#dplmc+ start incremented obj by 1...
        (create_text_overlay, "$g_presentation_obj_6", "@High centralization reduces tax inefficiency for the daimyo and raises it for vassals. This will interfere  the relations between ruler and vassals."),
        (create_text_overlay, "$g_presentation_obj_7", "@High aristocracy will improve the relations between the daimyo and his vassals who will be able to raise bigger armies but it will decreased trade."),
        (create_text_overlay, "$g_presentation_obj_8", "@High serfdom reduces tax inefficiency for the daimyo and his vassals and vassals can maintain bigger armies but troops loose moral."),
        (create_text_overlay, "$g_presentation_obj_9", "@High troop quality increases the strength of troops but decreases army size."),
		#dplmc+ end incremented obj by 1
		(create_text_overlay, "$g_presentation_obj_10", "@Mercantilistic policies maximize exports while minimizing imports, and increase government regulation of industry."),#<-dplmc+ added

		##Moved earlier
        #(faction_get_slot, ":centralization", "fac_player_supporters_faction", dplmc_slot_faction_centralization),
        #(faction_get_slot, ":aristocratcy", "fac_player_supporters_faction", dplmc_slot_faction_aristocracy),
        #(faction_get_slot, ":serfdom", "fac_player_supporters_faction", dplmc_slot_faction_serfdom),
        #(faction_get_slot, ":quality", "fac_player_supporters_faction", dplmc_slot_faction_quality),
		#(faction_get_slot, ":mercantilism", "fac_player_supporters_faction", dplmc_slot_faction_quality),#<- dplmc+ added

        (overlay_set_val, "$g_presentation_obj_sliders_1", ":centralization"),
        (overlay_set_val, "$g_presentation_obj_sliders_2", ":aristocratcy"),
        (overlay_set_val, "$g_presentation_obj_sliders_3", ":serfdom"),
        (overlay_set_val, "$g_presentation_obj_sliders_4", ":quality"),
		(overlay_set_val, "$g_presentation_obj_sliders_5", ":mercantilism"),#<- dplmc+ added
        (position_set_x, pos1, 200),

		##SLIDERS
		#dplmc start+ pushed all items by 150, then dropped all items by 75, then decreased the spacing from 150 to 100
        (position_set_y, pos1, 575),#750),
        (overlay_set_position, "$g_presentation_obj_sliders_1", pos1),
        (position_set_y, pos1, 450),#600),
        (overlay_set_position, "$g_presentation_obj_sliders_2", pos1),
        (position_set_y, pos1, 325),#450),
        (overlay_set_position, "$g_presentation_obj_sliders_3", pos1),
        (position_set_y, pos1, 200),#300),
        (overlay_set_position, "$g_presentation_obj_sliders_4", pos1),
		#dplmc end+ end pushed all items by 150
        (position_set_y, pos1, 75),#150), #<- dplmc+ added
        (overlay_set_position, "$g_presentation_obj_sliders_5", pos1),#<- dplmc+ added


		##HEADERS
        (position_set_x, pos1, 100),
		#dplmc+ start pushed all items by 150, then dropped all items by 75, then changed the spacing to 100
        (position_set_y, pos1, 625),#800),
        (overlay_set_position, "$g_presentation_obj_1", pos1),
        (position_set_y, pos1, 500),#650),
        (overlay_set_position, "$g_presentation_obj_2", pos1),
        (position_set_y, pos1, 375),#500),
        (overlay_set_position, "$g_presentation_obj_3", pos1),
        (position_set_y, pos1, 250),#350),
        (overlay_set_position, "$g_presentation_obj_4", pos1),
		#dplmc+ end pushed all items by 150
		(position_set_y, pos1, 125),#200), #<- dplmc+ added
        (overlay_set_position, "$g_presentation_obj_5", pos1), #<- dplmc+ added

		##SLIDER DESCRIPTIONS
        (position_set_x, pos1, 50),
		#dplmc+ start pushed all items by 150, and incremented obj by 1, then dropped all items by 75, then raised it 10, then changed the spacing to 100
        (position_set_y, pos1, 550),#700),
        (overlay_set_position, "$g_presentation_obj_6", pos1),
        (position_set_y, pos1, 425),#550),
        (overlay_set_position, "$g_presentation_obj_7", pos1),
        (position_set_y, pos1, 300),#400),
        (overlay_set_position, "$g_presentation_obj_8", pos1),
        (position_set_y, pos1, 175),#250),
        (overlay_set_position, "$g_presentation_obj_9", pos1),
		#dplmc+ end pushed all items by 150, and incremented obj by 1
		(position_set_y, pos1, 50),#100), #<- dplmc+ added
        (overlay_set_position, "$g_presentation_obj_10", pos1), #<- dplmc+ added

        (position_set_x, pos1, 775),
        (position_set_y, pos1, 775),
		#dplmc+ start increment obj by 1
        (overlay_set_size, "$g_presentation_obj_6", pos1),
        (overlay_set_size, "$g_presentation_obj_7", pos1),
        (overlay_set_size, "$g_presentation_obj_8", pos1),
        (overlay_set_size, "$g_presentation_obj_9", pos1),
		#dplmc+ end increment obj by 1
		(overlay_set_size, "$g_presentation_obj_10", pos1),#<- dplmc+ added

		##SLIDER LEVEL TEXT
        (position_set_x, pos1, 400),#400),
		#dplmc+ start pushed all items by 150, and incremented sliders by 1, then dropped all items by 75, then changed the spacing to 100
        (position_set_y, pos1, 575),#750),
        (overlay_set_position, "$g_presentation_obj_sliders_6", pos1),
        (position_set_y, pos1, 450),#600),
        (overlay_set_position, "$g_presentation_obj_sliders_7", pos1),
        (position_set_y, pos1, 325),#450),
        (overlay_set_position, "$g_presentation_obj_sliders_8", pos1),
        (position_set_y, pos1, 200),#300),
        (overlay_set_position, "$g_presentation_obj_sliders_9", pos1),
		#dplmc+ end pushed all items by 150, and incremented sliders by 1
		(position_set_y, pos1, 75),#150),#<- dplmc+ added
        (overlay_set_position, "$g_presentation_obj_sliders_10", pos1),#<- dplmc+ added

        (position_set_x, pos1, 925),
        (position_set_y, pos1, 925),
		#dplmc+ start incremented sliders by 1
        (overlay_set_size, "$g_presentation_obj_sliders_6", pos1),
        (overlay_set_size, "$g_presentation_obj_sliders_7", pos1),
        (overlay_set_size, "$g_presentation_obj_sliders_8", pos1),
        (overlay_set_size, "$g_presentation_obj_sliders_9", pos1),
		#dplmc+ end incremented sliders by 1
		(overlay_set_size, "$g_presentation_obj_sliders_10", pos1),#<- dplmc+ added
        ]),
      (ti_on_presentation_run,
       [
        ]),
      (ti_on_presentation_event_state_change,
       [(store_trigger_param_1, ":object"),
        (store_trigger_param_2, ":value"),
        ##nested diplomacy start+
		#Added new option, so had to increment some sliders
        (try_begin),
          (eq, ":object", "$g_presentation_obj_sliders_1"),
          (faction_set_slot,  "fac_player_supporters_faction", dplmc_slot_faction_centralization, ":value"),
          (val_add, ":value", "str_dplmc_neither_centralize_nor_decentralized"),
          (overlay_set_text, "$g_presentation_obj_sliders_6", ":value"),#dplmc+ incremented "sliders"
        (else_try),
          (eq, ":object", "$g_presentation_obj_sliders_2"),
          (faction_set_slot,  "fac_player_supporters_faction", dplmc_slot_faction_aristocracy, ":value"),
          (val_add, ":value", "str_dplmc_neither_aristocratic_nor_plutocratic"),
          (overlay_set_text, "$g_presentation_obj_sliders_7", ":value"),#dplmc+ incremented "sliders"
        (else_try),
          (eq, ":object", "$g_presentation_obj_sliders_3"),
          (faction_set_slot,  "fac_player_supporters_faction", dplmc_slot_faction_serfdom, ":value"),
          (val_add, ":value", "str_dplmc_mixture_serfs"),
          (overlay_set_text, "$g_presentation_obj_sliders_8", ":value"),#dplmc+ incremented "sliders"
        (else_try),
          (eq, ":object", "$g_presentation_obj_sliders_4"),
          (faction_set_slot,  "fac_player_supporters_faction", dplmc_slot_faction_quality, ":value"),
          (val_add, ":value", "str_dplmc_mediocre_quality"),
          (overlay_set_text, "$g_presentation_obj_sliders_9", ":value"),#dplmc+ incremented "sliders"
		#Finished incremented sliders.
		(else_try),
		  #dplmc+ new option: mercantilism
		  (eq, ":object", "$g_presentation_obj_sliders_5"),
          (faction_set_slot,  "fac_player_supporters_faction", dplmc_slot_faction_mercantilism, ":value"),
          (val_add, ":value", "str_dplmc_neither_mercantilist_nor_laissez_faire"),
          (overlay_set_text, "$g_presentation_obj_sliders_10", ":value"),
		#Change variable associated with "Done" button.
        (else_try),
          (eq, ":object", "$g_presentation_obj_12"),#dplmc+ changed 10 to 12
          (assign, "$g_players_policy_set", 1),
          (presentation_set_duration, 0),
        (try_end),
		##nested diplomacy end+
    ]),
  ]),
  ##nested diplomacy start+
  #
  #Make it slightly harder to abuse the AI.
  #For example, some players report randomly starting wars with a faction and
  #demanding a hard-to-take castle until the AI concedes.
  #
  #See changes in logic below for specifics.
  #
  ##nested diplomacy end+
    ("dplmc_peace_terms",0,mesh_load_window,[
      (ti_on_presentation_load,
       [
        (set_fixed_point_multiplier, 1000),
        (presentation_set_duration, 999999),

        # done
        (create_game_button_overlay, "$g_presentation_obj_10", "@Done"),
        (position_set_x, pos1, 900),
        (position_set_y, pos1, 25),
        (overlay_set_position, "$g_presentation_obj_10", pos1),

        #cancel
        (create_game_button_overlay, "$g_presentation_obj_9", "@Cancel"),
        (position_set_x, pos1, 100),
        (overlay_set_position, "$g_presentation_obj_9", pos1),

        # title
        (create_text_overlay, reg1, "@Dictate the peace terms", tf_center_justify|tf_vertical_align_center),
        (position_set_x, pos1, 445),
        (position_set_y, pos1, 700),
        (overlay_set_position, reg1, pos1),

        (position_set_y, pos1, 550),
        (create_text_overlay, "$g_presentation_obj_2", "@Select the castle and the amount of money and check the boxes to activate the demand. The demands are combined if both boxes are checked."),
        (position_set_x, pos1, 50),
        (overlay_set_position, "$g_presentation_obj_2", pos1),

        (create_slider_overlay, "$g_presentation_obj_sliders_1", 1, 10),
        (overlay_set_val, "$g_presentation_obj_sliders_1", 1),
        (position_set_x, pos1, 300),
        (position_set_y, pos1, 350),
        (overlay_set_position, "$g_presentation_obj_sliders_1", pos1),
        (assign, "$demanded_money", 1000),
        (assign, "$diplomacy_var", 1),

        (create_text_overlay, "$g_presentation_obj_sliders_2", "@1000 mon"),
        (position_set_x, pos1, 500),
        (overlay_set_position, "$g_presentation_obj_sliders_2", pos1),

        (create_check_box_overlay, "$g_presentation_obj_battle_check0", "mesh_checkbox_off", "mesh_checkbox_on"),
        (position_set_x, pos1, 700),
        (overlay_set_position, "$g_presentation_obj_battle_check0", pos1),
        (overlay_set_val, "$g_presentation_obj_battle_check0", 1),

        (assign, "$demanded_castle", 0),
        (assign, ":castle_count", 0),
        (create_combo_button_overlay, "$g_presentation_obj_1"),
        (try_for_range, ":castle", castles_begin, castles_end),
		  ##diplomacy start+
		  (party_slot_eq, ":castle", slot_party_type, spt_castle),
		  ##diplomacy end+
          (store_faction_of_party, ":castle_faction", ":castle"),
          (eq, ":castle_faction", "$g_notification_menu_var1"),
          (str_store_party_name, s2, ":castle"),
          (overlay_add_item, "$g_presentation_obj_1", s2),
          (assign, "$demanded_castle", ":castle"),
          (val_add, ":castle_count", 1),
        (end_try),
        (assign, "$diplomacy_var2", 0),
        (position_set_x, pos1, 300),
        (position_set_y, pos1, 250),
        (overlay_set_position, "$g_presentation_obj_1", pos1),
        (overlay_set_val, "$g_presentation_obj_1", ":castle_count"),

        (create_check_box_overlay, "$g_presentation_obj_battle_check1", "mesh_checkbox_off", "mesh_checkbox_on"),
        (position_set_x, pos1, 700),
        (overlay_set_position, "$g_presentation_obj_battle_check1", pos1),

        ]),
      (ti_on_presentation_run,
       [
        ]),
      (ti_on_presentation_event_state_change,
       [(store_trigger_param_1, ":object"),
        (store_trigger_param_2, ":value"),

        (try_begin),
          (eq, ":object", "$g_presentation_obj_1"),

          (assign, ":cur", 0),
          (try_for_range, ":castle", castles_begin, castles_end),
            (store_faction_of_party, ":castle_faction", ":castle"),
            (eq, ":castle_faction", "$g_notification_menu_var1"),
            (try_begin),
              (eq, ":cur", ":value"),
              (assign, "$demanded_castle", ":castle"),
            (try_end),
            (val_add, ":cur", 1),
          (try_end),

        (else_try),
          (eq, ":object", "$g_presentation_obj_battle_check0"),
          (assign, "$diplomacy_var", ":value"),

        (else_try),
          (eq, ":object", "$g_presentation_obj_battle_check1"),
          (assign, "$diplomacy_var2", ":value"),

        (else_try),
          (eq, ":object", "$g_presentation_obj_sliders_1"),
          (store_mul, "$demanded_money",":value", 1000),
		  ##diplomacy start+
		  ##OLD:
          #(assign, reg0, "$demanded_money"),
          #(overlay_set_text, "$g_presentation_obj_sliders_2", "@{reg0} mon"),
		  ##NEW:
		  (assign, reg1, "$demanded_money"),
		  (overlay_set_text, "$g_presentation_obj_sliders_2", "str_reg1_denars"),
		  ##diplomacy end+

        (else_try),
          (eq, ":object", "$g_presentation_obj_9"),
          (presentation_set_duration, 0),
        (else_try),
          (eq, ":object", "$g_presentation_obj_10"),
          (presentation_set_duration, 0),

          (try_begin),
            (eq, "$diplomacy_var", 0),
            (assign, "$demanded_money", 0),
          (try_end),

          (try_begin),
            (eq, "$diplomacy_var2", 0),
            (assign, "$demanded_castle", 0),
          (try_end),

          (assign, ":demand", 0),
          (try_begin),
            (gt, "$demanded_money", 0),
            (store_div, ":demand", "$demanded_money", 1000),
          (try_end),
		  ##nested diplomacy start+
		  #OLD:
		  #(try_begin),
          #   (is_between, "$demanded_castle", castles_begin, castles_end),
          #   (val_add, ":demand", 12),
          #(try_end),
		  #NEW:
		  #
		  #Not all castles are created equal.
		  (assign, ":npc_faction", "$g_notification_menu_var1"),

		  (assign, ":player_faction", "fac_player_supporters_faction"),
		  (try_begin),
		     (neg|faction_slot_eq, ":player_faction", slot_faction_state, sfs_active),
			 (is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
			 (assign, ":player_faction", "$players_kingdom"),
		  (try_end),

		  #(assign, ":castle_value", 0),
		  (assign, ":was_taken_recently", 0),
		  (assign, ":would_make_lord_fiefless", 0),
		  (assign, ":distance_factor", 100),#If positive, 100 times the ratio of distance of closest friendly center to closest enemy center; if negative, 100 times the ratio of the distance of the closest enemy center to the closest friendly center.
		  (try_begin),
			(is_between, "$demanded_castle", castles_begin, castles_end),
			## (1) Determine whether or not the demanded castle was taken recently.
			(try_begin),
				#This version of Diplomacy+ saves transfer times, so we can check directly.
				(neg|party_slot_eq, "$demanded_castle", dplmc_slot_center_last_transfer_time, 0),
				(store_current_hours, ":hours_since_capture"),
				(party_get_slot, reg0, "$demanded_castle", dplmc_slot_center_last_transfer_time),
				(val_sub, ":hours_since_capture", reg0),
				(try_begin),
					#In the last month (i.e. about a war)
					(lt, ":hours_since_capture", 31 * 24),
					(assign, ":was_taken_recently", 1),
				(else_try),
					#For non-core castles, extend the definition of recent to the last three months
					(neg|party_slot_eq, "$demanded_castle", slot_center_original_faction, ":npc_faction"),
					(lt, ":hours_since_capture", 91 * 24),
					(assign, ":was_taken_recently", 1),
				(else_try),
					(assign, ":was_taken_recently", 0),
				(try_end),
			(else_try),
				#This is an old saved game, so use some rules of thumb.
				#If the player faction is the original or previous owner, it might have been taken recently.
				(this_or_next|party_slot_eq, "$demanded_castle", slot_center_original_faction, "$players_kingdom"),
				(this_or_next|party_slot_eq, "$demanded_castle", slot_center_ex_faction, "$players_kingdom"),
					(party_slot_eq, "$demanded_castle", slot_center_ex_faction, "fac_player_supporters_faction"),
				(assign, ":was_taken_recently", 1),
			(else_try),
				#If the original owner is at war with the current owner, it might have been taken recently.
				(neg|party_slot_eq, "$demanded_castle", slot_center_original_faction, ":npc_faction"),
				(party_get_slot, ":third_faction", "$demanded_castle", slot_center_original_faction),
				(is_between, ":third_faction", kingdoms_begin, kingdoms_end),
				(faction_slot_eq, ":third_faction", slot_faction_state, sfs_active),
				(store_relation, reg0, ":npc_faction", ":third_faction"),
				(lt, reg0, 0),
				(assign, ":was_taken_recently", 1),
			(else_try),
				#If the ex-owner is at war with the current owner, it might have been taken recently.
				(neg|party_slot_eq, "$demanded_castle", slot_center_ex_faction, ":npc_faction"),
				(party_get_slot, ":third_faction", "$demanded_castle", slot_center_ex_faction),
				(is_between, ":third_faction", kingdoms_begin, kingdoms_end),
				(faction_slot_eq, ":third_faction", slot_faction_state, sfs_active),
				(store_relation, reg0, ":npc_faction", ":third_faction"),
				(lt, reg0, 0),
				(assign, ":was_taken_recently", 1),
			(else_try),
				#If there is no assigned lord, it was taken recently.
				(neg|party_slot_ge, "$demanded_castle", slot_town_lord, 0),
				(assign, ":was_taken_recently", 1),
			(try_end),##End "Was taken recently?"
			## (2) Determine whether handing over the demanded castle would cost any lord his last fief.
			## (2a: At the same time, calculate the closest friendly & enemy walled centers)
			(party_slot_ge, "$demanded_castle", slot_town_lord, 1),
			(party_get_slot, ":lord_a", "$demanded_castle", slot_town_lord),
			(assign, ":lord_b", -1),
			(assign, ":would_make_lord_fiefless", 1),
			(assign, ":distance_to_friendly_fortress", 10000),
			(assign, ":distance_to_enemy_fortress", 10000),
			(try_for_range, ":center_no", centers_begin, centers_end),
				(neq, ":center_no", "$demanded_castle"),
				#Check for fieflessness
				(try_begin),
					(party_slot_eq, ":center_no", slot_village_bound_center, "$demanded_castle"),
					(neg|party_slot_eq, ":center_no", slot_town_lord, ":lord_a"),
					(party_slot_ge, ":center_no", slot_town_lord, 1),
					(party_get_slot, ":lord_b", ":center_no", slot_town_lord),
				(else_try),
					(party_slot_eq, ":center_no", slot_town_lord, ":lord_a"),
					(neg|party_slot_eq, ":center_no", slot_village_bound_center, "$demanded_castle"),
					(assign, ":would_make_lord_fiefless", 0),
				(try_end),
				#For walled centers check distance
				(this_or_next|party_slot_eq, ":center_no", slot_party_type, spt_town),
					(this_or_next|party_slot_eq, ":center_no", slot_party_type, spt_castle),

				(store_faction_of_party, ":center_faction", ":center_no"),
				(store_distance_to_party_from_party, ":cur_distance", ":center_no", "$demanded_castle"),

				(call_script, "script_dplmc_get_faction_truce_length_with_faction", ":center_faction", ":npc_faction"),
				(try_begin),
					(this_or_next|gt, reg0, dplmc_treaty_defense_days_expire),
					(eq, ":center_faction", ":npc_faction"),
					(val_min, ":distance_to_friendly_fortress", ":cur_distance"),
				(else_try),
					(store_relation, reg0, ":center_faction", ":npc_faction"),
					(val_min, ":distance_to_enemy_fortress", ":cur_distance"),
				(try_end),
			(try_end),
			#(2a, set distance factor based on closest other fortress)
			(assign, ":distance_factor", 100),
			(try_begin),
				(this_or_next|ge, ":distance_to_friendly_fortress", 10000),
					(ge, ":distance_to_enemy_fortress", 10000),
				#No fortress found for one or both
			(else_try),
				#Friendly is closer
				(lt, ":distance_to_friendly_fortress", ":distance_to_enemy_fortress"),
				(gt, ":distance_to_enemy_fortress", 25),#Within 25 ignore differences
				(val_max, ":distance_to_friendly_fortress", 1),
				(store_mul, ":distance_factor", ":distance_to_enemy_fortress", 100),
				(val_div, ":distance_factor", ":distance_to_friendly_fortress"),
				(try_begin),
					(le, ":distance_to_enemy_fortress", 50),
					(val_min, ":distance_factor", 200),
				(try_end),
			(else_try),
				#Enemy is closer
				(lt, ":distance_to_enemy_fortress", ":distance_to_friendly_fortress"),
				(gt, ":distance_to_friendly_fortress", 25),#Within 25 ignore differences
				(val_max, ":distance_to_enemy_fortress", 1),
				(store_mul, ":distance_factor", ":distance_to_friendly_fortress", 100),
				(val_div, ":distance_factor", ":distance_to_enemy_fortress"),
				(try_begin),
					(le, ":distance_to_friendly_fortress", 50),
					(val_min, ":distance_factor", 200),
				(try_end),
				(val_mul, ":distance_factor", -1),
			(try_end),##end 2a: distance factor

			(neq, ":would_make_lord_fiefless", 1),#If we already know it would make the castle owner fiefless, stop.
			(ge, ":lord_b", 1),
			(assign, ":would_make_lord_fiefless", 1),
			(try_for_range, ":center_no", centers_begin, centers_end),
				(party_slot_eq, ":center_no", slot_town_lord, ":lord_b"),
				(this_or_next|neg|is_between, ":center_no", villages_begin, villages_end),
					(neg|party_slot_eq, ":center_no", slot_village_bound_center, "$demanded_castle"),
					(assign, ":would_make_lord_fiefless", 0),
			(try_end),
		  (try_end),##end 2: would make lord fiefless?
		  (assign, ":castle_strength_ratio", 100),
		  (assign, ":high_ratio", 150),
		  (try_begin),
			(is_between, "$demanded_castle", castles_begin, castles_end),
			#(3) Determine typical castle strength
			(assign, ":typical_strength", 0),
			(assign, ":high_ratio", 0),#<- for now, store max strength seen
			(try_for_range, ":center_no", castles_begin, castles_end),
				(try_begin),
					(eq, "$g_dplmc_terrain_advantage", DPLMC_TERRAIN_ADVANTAGE_ENABLE),
					(call_script, "script_dplmc_party_calculate_strength_in_terrain", ":center_no", dplmc_terrain_code_siege, 0, 1),
					#Outputs to reg0 (using terrain) and reg1 (not using terrain).  We'll be using reg1,
					#but the function will be updating the cached strength using the terrain version (as I want).
					(assign, reg0, reg1),
				(else_try),
					#Use the non-terrain-modified strength script.
					(call_script, "script_party_calculate_strength", ":center_no", dplmc_terrain_code_siege, 0),
				(try_end),

				(val_max, reg0, 250),#A certain minimum scale is assumed
				(val_add, ":typical_strength", reg0),
				(val_max, ":high_ratio", reg0),#keep track of max
				(eq, ":center_no", "$demanded_castle"),
				(assign, ":castle_strength_ratio", reg0),
			(try_end),
			(try_begin),
				(gt, castles_end, castles_begin),
				(store_sub, reg0, castles_end, castles_begin),
				(val_div, ":typical_strength", reg0),
			(try_end),
			(val_max, ":typical_strength", 300),#<- A certain minimum scale is assumed
			(val_mul, ":castle_strength_ratio", 100),
			(val_mul, ":high_ratio", 100),

			(store_div, reg0, ":typical_strength", 2),

			(val_add, ":castle_strength_ratio", reg0),
			(val_add, ":high_ratio", reg0),

			(val_div, ":castle_strength_ratio", ":typical_strength"),
			(val_div, ":high_ratio", ":typical_strength"),

			(assign, reg0, ":castle_strength_ratio"),
			(val_max, reg0, 100),
			(val_mul, reg0, 12),#Scale so that 100 is 12, 200 is 24, etc.
			(val_add, reg0, 50),
			(val_div, reg0, 100),
			(val_add, ":demand", reg0),

			(val_sub, ":high_ratio", 100),
			(val_div, ":high_ratio", 2),
			(val_add, ":high_ratio", 100),
			(val_clamp, ":high_ratio", 110, 400),
		  (try_end),##end (3) determine typical castle strength

		  ##Next line: replace fac_player_supporters_faction with :player_faction
          (call_script, "script_npc_decision_checklist_peace_or_war", "$g_notification_menu_var1", ":player_faction", -1),

		  ##Save the unmodified numbers for later
		  (assign, ":check_peace_war_result", reg0),
		  #(assign, ":original_demand", ":demand"),
		  ##diplomacy end+
          (assign, ":goodwill", reg0),
          (val_mul, ":goodwill", 2),
          (store_random_in_range, ":random", 0, ":demand"),

          (val_div, ":demand", -2),

          (call_script, "script_change_player_relation_with_faction", "$g_notification_menu_var1", ":demand"),
		  ##diplomacy start+
		  #Count "third party" kingdoms: kingdoms that aren't either the player's kingdom
		  #or the other kingdom in the negotiations, and that aren't allied to either.
		  #(faction_get_slot, ":npc_faction_leader", ":npc_faction", slot_faction_leader),
		  (assign, ":other_players", 0),
		  (try_for_range, ":third_faction", kingdoms_begin, kingdoms_end),
			 #Active faction
		     (faction_slot_eq, ":third_faction", slot_faction_state, sfs_active),
			 (neq, ":third_faction", ":npc_faction"),
			 (neq, ":third_faction", "fac_player_supporters_faction"),
			 (neq, ":third_faction", "$players_kingdom"),
			 #Not allied (full alliance or defensive alliance) to either faction
			 (call_script, "script_dplmc_get_faction_truce_length_with_faction", ":third_faction", ":npc_faction"),
			 (le, reg0, dplmc_treaty_defense_days_expire),
			 (call_script, "script_dplmc_get_faction_truce_length_with_faction", ":third_faction", "$players_kingdom"),
			 (le, reg0, dplmc_treaty_defense_days_expire),
			 (val_add, ":other_players", 1),
		  (try_end),
		  #Improve the AI's decision-making somewhat.
		  (game_get_reduce_campaign_ai, ":reduce_campaign_ai"),
		  (val_clamp, ":reduce_campaign_ai", 0, 3),#0 is hard, 1 is medium, 2 is easy
		  (try_begin),
            #This should never be reached.
				(lt, ":check_peace_war_result", 0),
            (this_or_next|is_between, "$demanded_castle", castles_begin, castles_end),
               (gt, "$demanded_money", 0),
			(jump_to_menu,"mnu_dplmc_deny_terms"),
        (else_try),
            (is_between, "$demanded_castle", castles_begin, castles_end),
				(lt, ":check_peace_war_result", 2),
            #Don't enable "fishing" for fiefs, hoping to get a lucky
            #result.  Make the chance of giving a fief zero.
            (this_or_next|party_slot_eq,"$demanded_castle",slot_center_original_faction,":npc_faction"),
            (this_or_next|eq, ":would_make_lord_fiefless", 1),
            (this_or_next|ge, ":castle_strength_ratio", ":high_ratio"),
				(this_or_next|eq, ":was_taken_recently", 0),
               (eq, ":other_players", 0),
			(jump_to_menu,"mnu_dplmc_deny_terms"),
        (else_try),
            (is_between, "$demanded_castle", castles_begin, castles_end),
            #Some things will just never be agreed to.
				#If three or more of the following are true, reject:
				#- The demanded castle was not taken recently
				#- The demanded castle is one of the faction's original castles
				#- Giving the castle would make some lords fiefless
				#- The castle has an especially large garrison
				#- Aside from the player's faction and the NPC faction (and their allies),
				#  there are no other kingdoms.
				#- The demanded castle is significantly deeper within the NPC kingdom's territory
				#  than it is close to enemy territory
            (assign, reg0, 1),
			(val_sub, reg0, ":was_taken_recently"),
			(val_max, reg0, 0),
            (try_begin),#Check: is the castle part of the faction's original territory?
               (party_slot_eq,"$demanded_castle",slot_center_original_faction,":npc_faction"),
			   (val_add, reg0, 1),
            (try_end),
			(val_max, ":would_make_lord_fiefless", 0),
			(val_add, reg0, ":would_make_lord_fiefless"),
			(try_begin),#Check: castle has high strength compared to average?
				 (ge, ":castle_strength_ratio", ":high_ratio"),
				 (val_add, reg0, 1),
			(try_end),
			(try_begin),#Check: no one else remaining?
				 (eq, ":other_players", 0),
				 (val_add, reg0, 1),
			(try_end),
			(try_begin),#Check: is it much closer to friendly centers than enemy centers?
				(ge, ":distance_factor", 190),
				(val_add, reg0, 1),
			(try_end),
			(val_add, ":random", reg0),#Even if less than 3 are met, other factors will still decrease likelihood of acceptance.

			(ge, reg0, 3),
			(jump_to_menu,"mnu_dplmc_deny_terms"),
        (else_try),
			#SPECIAL CASE: Two Kingdoms Remain
			(eq, ":other_players", 0),
			(this_or_next|is_between, "$demanded_castle", castles_begin, castles_end),
				(gt, "$demanded_money", 0),
			(is_between, ":npc_faction", kingdoms_begin, kingdoms_end),
			(assign, ":minimum_peace_war_result", 2),
			(try_begin),
				#Hard: never accept.
				(eq, ":reduce_campaign_ai", 0),
				(store_add, ":minimum_peace_war_result", ":check_peace_war_result", 1),
				(val_max, ":minimum_peace_war_result", 4),
			(else_try),
				#Medium: never give up fiefs, sometimes accept other deals.
				(eq, ":reduce_campaign_ai", 1),
				(is_between, "$demanded_castle", castles_begin, castles_end),
				(store_add, ":minimum_peace_war_result", ":check_peace_war_result", 1),
				(val_max, ":minimum_peace_war_result", 4),
			(else_try),
				#Easy: sometimes accept.
				(eq, ":reduce_campaign_ai", 2),
			(try_end),
			(lt, ":check_peace_war_result", ":minimum_peace_war_result"),
			(jump_to_menu,"mnu_dplmc_deny_terms"),
		  (else_try),
		  #fall through to other behavior
		  ##diplomacy end+
            (le, ":random", ":goodwill"),
            (try_begin),
              (is_between, "$demanded_castle", castles_begin, castles_end),
				  ##diplomacy start+
				  #Relation hit with the owner of the surrendered castle and its village,
				  #if there was a valid owner.
				  (try_begin),
					(party_slot_ge, "$demanded_castle", slot_town_lord, 1),
					(party_get_slot, reg0, ":center_no", slot_town_lord),
					(call_script, "script_change_player_relation_with_troop", reg0, -1),
				  (try_end),
				  (try_for_range, ":center_no", villages_begin, villages_end),
					(party_slot_eq, ":center_no", slot_village_bound_center, "$demanded_castle"),
					(party_slot_ge, ":center_no", slot_town_lord, 1),
					(party_get_slot, reg0, ":center_no", slot_town_lord),
					(call_script, "script_change_player_relation_with_troop", reg0, -1),
				  (try_end),
			  ##Change next to use :player_faction instead of fac_player_supporters_faction
              (call_script, "script_give_center_to_faction", "$demanded_castle", ":player_faction"),
			  ##diplomacy end+
            (try_end),
            (try_begin),
              (gt, "$demanded_money", 0),
              (call_script, "script_dplmc_pay_into_treasury", "$demanded_money"),
			  ##diplomacy start+ other faction loses money
			  #Since setting terms for surrender is a non-native feature, there is no need to make this optional.
			  (faction_get_slot, ":faction_leader", "$g_notification_menu_var1", slot_faction_leader),
			  (try_begin),
				(ge, ":faction_leader", 1),
				(neq, "$g_notification_menu_var1", "$players_kingdom"),
				(neq, "$g_notification_menu_var1", "fac_player_supporters_faction"),
				(ge, "$demanded_money", 1),
				(assign, ":cost_to_leader", "$demanded_money"),
				#(try_begin),
				#	 (faction_get_slot, ":marshall", "$g_notification_menu_var1", slot_faction_marshall),
				#	 (neq, ":marshall", "trp_player"),
				#	 (neq, ":marshall", ":faction_leader"),
				#	 (ge, ":marshall", 0),
				#	 (store_troop_gold, reg0, ":marshall"),
				#	 (store_troop_gold, reg1, ":faction_leader"),
				#	 (val_add, reg1, reg0),
				#	 (gt, reg1, 0),
				#	 (store_mul, ":cost_to_marshall", "$demanded_money", reg0),
				#	 (val_div, ":cost_to_marshall", reg1),
				#	 (store_div, reg0, "$demanded_money", 2),
				#	 (val_min, ":cost_to_marshall", reg0),#no more than 1/2
				#	 (store_mul, reg0, "$demanded_money", 3),
				#	 (val_div, reg0, 13),#no less than 3/13 (6/26 marshall, 20/26 leader)
				#	 (val_max, ":cost_to_marshall", reg0),
				#	 (gt, ":cost_to_marshall", 0),
				#	 (call_script, "script_dplmc_remove_gold_from_lord_and_holdings", ":cost_to_marshall", ":marshall"),
				#	 (val_sub, ":cost_to_leader", ":cost_to_marshall"),
				#	 (store_random_in_range, reg0, 0, 1000),
				#	 (val_add, reg0, ":cost_to_marshall"),
				#	 (val_div, reg0, 1000),
				#	 (ge, reg0, 1),
				#	 (val_mul, reg0, -1),
				#	 (call_script, "script_change_player_relation_with_troop", ":marshall", reg0),
				#(try_end),
				(ge, ":cost_to_leader", 1),
				(call_script, "script_dplmc_remove_gold_from_lord_and_holdings", ":cost_to_leader", ":faction_leader"),
				(store_random_in_range, reg0, 0, 1000),
				(val_add, reg0, ":cost_to_leader"),
				(val_div, reg0, 1000),
				(ge, reg0, 1),
				(val_mul, reg0, -1),
				(call_script, "script_change_player_relation_with_troop", ":faction_leader", reg0),
			  (try_end),
			  ##diplomacy end+
            (try_end),
			##diplomacy start+
            (call_script, "script_diplomacy_start_peace_between_kingdoms", "$g_notification_menu_var1", ":player_faction", 1),
			##diplomacy end+
            (presentation_set_duration, 0),
            (change_screen_return),
          (else_try),
            (jump_to_menu,"mnu_dplmc_deny_terms"),
          (try_end),

        (try_end),
    ]),
  ]),
  # Jrider +
  # REPORTS PRESENTATIONS 1.2 :
  # Factions relations presentation report
  ("jrider_faction_relations_report", 0,
   mesh_message_window,
   [
     (ti_on_presentation_load,
      [
    (presentation_set_duration, 999999),
        (set_fixed_point_multiplier, 1000),

        # Embed picture upper right
		#gekokujo reports presentation - use the new castle mesh
        #(create_mesh_overlay, reg1, "mesh_pic_castledes"),
        (create_mesh_overlay, reg1, "mesh_gekokujo_pic_castle"),
        (position_set_x, pos1, 180),
        (position_set_y, pos1, 180),
        (overlay_set_size, reg1, pos1),
        (position_set_x, pos1, 795),
        (position_set_y, pos1, 600),
        (overlay_set_position, reg1, pos1),

        # Embed picture upper left
        (create_mesh_overlay, reg1, "mesh_pic_looted_village"),
        (position_set_x, pos1, 170),
        (position_set_y, pos1, 170),
        (overlay_set_size, reg1, pos1),
        (position_set_x, pos1, -15),
        (position_set_y, pos1, 600),
        (overlay_set_position, reg1, pos1),

    # Presentation title, centered at the top
        (create_text_overlay, reg1, "@_Faction Relations Report_", tf_center_justify),
    (position_set_x, pos1, 500), # Higher, means more toward the right
        (position_set_y, pos1, 670), # Higher, means more toward the top
        (overlay_set_position, reg1, pos1),
    (position_set_x, pos1, 1500),
        (position_set_y, pos1, 1500),
    (overlay_set_size, reg1, pos1),
    
    #gekokujo 3.1 faction relations report start
    #find the first faction
    (assign, ":fac_first", 0),
    (try_for_range, ":faction", kingdoms_begin, kingdoms_end),
      (eq, ":fac_first", 0),
      (faction_slot_eq, ":faction", slot_faction_state, sfs_active),
      (assign, ":fac_first", ":faction"),
    (try_end),
    
    #add the offset to find the active faction
    (val_add, ":fac_first", "$gekokujo_fac_report_offset"),
    
    #count 6 active factions after our first active faction
    (assign, ":fac_last", 0),
    (assign, ":fac_count", 0),
    (try_for_range, ":faction", ":fac_first", kingdoms_end),
      (lt, ":fac_count", 6), #stop at 6
      (faction_slot_eq, ":faction", slot_faction_state, sfs_active),
      (assign, ":fac_last", ":faction"),
      (val_add, ":fac_count", 1),
    (try_end),
    (val_add, ":fac_last", 1),
    
    #add a previous button
    (create_game_button_overlay, reg1, "@_Prev_"),
    (position_set_x, pos1, 250),
    (position_set_y, pos1, 23),
    (overlay_set_position, reg1, pos1),
    (assign, "$gekokujo_fac_report_prev", reg1),
    
    #add a next button
    (create_game_button_overlay, reg1, "@_Next_"),
    (position_set_x, pos1, 750),
    (position_set_y, pos1, 23),
    (overlay_set_position, reg1, pos1),
    (assign, "$gekokujo_fac_report_next", reg1),
    #gekokujo 3.1 faction relations report end
    
    # Back to menu - graphical button
    (create_game_button_overlay, reg1, "@_Return to menu_"),
    (position_set_x, pos1, 500),
        (position_set_y, pos1, 23),
        (overlay_set_position, reg1, pos1),
        (assign, "$g_jrider_faction_report_Return_to_menu", reg1),

    # Set Headlines
#set column title
          (assign, ":x_poshl", 250),
          (assign, ":y_pos", 620),
          (position_set_y, pos1, ":y_pos"),
    #gekokujo 3.1 faction relations report start
    #(try_for_range, ":faction", kingdoms_begin, kingdoms_end),
    (try_for_range, ":faction", ":fac_first", ":fac_last"), 
    #gekokujo 3.1 faction relations report end
            (faction_slot_eq, ":faction", slot_faction_state, sfs_active), # continue if active
            (try_begin),
              (is_between, ":faction", npc_kingdoms_begin, npc_kingdoms_end),
              (store_sub, ":offset", ":faction", "fac_kingdom_1"),
			  #gekokujo not the freaking swadians
              #(val_add, ":offset", "str_swadians"),
			  (val_add, ":offset", "str_uesugi"),
              (str_store_string, s1, ":offset"),
            (else_try),
              (str_store_string, s1, "@Your kingdom"),
            (try_end),

            (str_store_string, s11, ":offset"),
            (create_text_overlay, reg10, s1, tf_left_align|tf_with_outline),
            (faction_get_color, ":faction_color", ":faction"),
            (overlay_set_color, reg10, ":faction_color"),

            (position_set_x, pos3, 650),
            (position_set_y, pos3, 800),
            (overlay_set_size, reg10, pos3),

            (position_set_x, pos1, ":x_poshl"),
            (overlay_set_position, reg10, pos1),
            (val_add, ":x_poshl", 90),
    (try_end),


    (assign, ":x_poshl", 215),
     (assign, ":y_pos", 597),
     (assign, ":headline_size", 0),
    (position_set_x, ":headline_size", 720),
        (position_set_y, ":headline_size", 775),

        (assign, ":hl_columnsep_size", 50),
        (position_set_x, ":hl_columnsep_size", 60),
        (position_set_y, ":hl_columnsep_size", 28000),

        (create_text_overlay, reg2, "@Player^Relation", tf_center_justify),
        (overlay_set_size, reg2, ":headline_size"),
        (position_set_x, pos1, ":x_poshl"),
        (position_set_y, pos1, ":y_pos"),
        (overlay_set_position, reg2, pos1),

        (val_add, ":x_poshl", 45),
        (try_for_range, ":count", 0, 7),
          # create a separator column
          (create_mesh_overlay, reg1, "mesh_white_plane"),
          (overlay_set_color, reg1, 0x000000),
          (overlay_set_size, reg1, ":hl_columnsep_size"),
          (store_sub, ":line_x", ":x_poshl", 15), # set it 21 pix left of current column start
          (store_sub, ":y_pos2", ":y_pos", 500), # set it 21 pix left of current column start
          (position_set_x, pos2, ":line_x"),
          (position_set_y, pos2, ":y_pos2"),
          (overlay_set_position, reg1, pos2),
          (val_add, ":x_poshl", 90),

          (try_begin),
            (eq, "$cheat_mode", 1),
            (assign, reg20, ":count"),
            (display_message, "@{!}DEBUG - Drawing line {reg20}"),
          (try_end),
        (try_end),

        # clear the string globals that we'll use
         (str_clear, s9),
    (str_clear, s8),
    (str_clear, s3),
    (str_clear, s60),
    (str_clear, s61),
    (str_clear, s0),

        # Scrollable area (all the next overlay will be contained in this, s0 sets the scrollbar)
        (create_text_overlay, reg1, s0, tf_scrollable_style_2),
        (position_set_x, pos1, 50),
        (position_set_y, pos1, 70),
        (overlay_set_position, reg1, pos1),
        (position_set_x, pos1, 860),
        (position_set_y, pos1, 527),
        (overlay_set_area_size, reg1, pos1),
        (set_container_overlay, reg1),

        # set base position and size for lines
        (assign, ":line_size", 0),
        (assign, ":y_pos", 0),

        # set base color for line
    (assign, ":line_color", 0x000000),

        # Line faction loop begins here - fetching corresponding informations and printing the line title
        (try_for_range_backwards, ":faction_line", kingdoms_begin, kingdoms_end),
            (faction_slot_eq, ":faction_line", slot_faction_state, sfs_active), # continue if active

            # Base position for subheaders
            (assign, ":x_posfhl", 220),

            # Loop other factions (columns)
            #gekokujo 3.1 faction relations report start
            #(try_for_range, ":faction_column", kingdoms_begin, kingdoms_end),
            (try_for_range, ":faction_column", ":fac_first", ":fac_last"),
            #gekokujo 3.1 faction relations report end
                (faction_slot_eq, ":faction_column", slot_faction_state, sfs_active), # continue if active

                (try_begin), # not same faction
                  (neq, ":faction_column", ":faction_line"),

                  (str_store_faction_name, s8, ":faction_column"),

                  # sub-faction excluding current faction line
                  (try_begin),
                      # different from faction line, display status and relation with faction line
                      (neq, ":faction_column", ":faction_line"),
                      (call_script, "script_diplomacy_faction_get_diplomatic_status_with_faction", ":faction_line", ":faction_column"),
                      (assign, ":global_diplomatic_status", reg0),
                      (assign, ":extended_diplomatic_status", reg1),

                      (try_begin), # War
                          (eq, ":global_diplomatic_status", -2),
                          (str_store_string, s60, "@War"),
                          (assign, reg60, 0xDD0000),
                          (assign, reg59, 0),
                      (else_try), # Border incident
                          (eq, ":global_diplomatic_status", -1),
                          (str_store_string, s60, "@Casus Belli"),
                          (assign, reg60, 0xDD8000),
                          (assign, reg59, ":extended_diplomatic_status"),
                      (else_try), # Peace
                          (eq, ":global_diplomatic_status", 0),
                          (str_store_string, s60, "@Peace"),
                          (assign, reg60, 0xFFFFFF),
                          (assign, reg59, 0),
                      (else_try), # Truce (non aggression)
                          (eq, ":global_diplomatic_status", 1),
                          (str_store_string, s60, "@Truce"),
                          (assign, reg60, 0xDDDDDD),
                          (assign, reg59, ":extended_diplomatic_status"),

                          # for Diplomacy, comment if not using
                          (try_begin),
                              (ge, ":extended_diplomatic_status", 61),
                              (str_store_string, s60, "@Alliance"),
                              (assign, reg60, 0x00FF00),
                              (store_sub, reg59, ":extended_diplomatic_status", 60),
                          (else_try),
                              (ge, ":extended_diplomatic_status", 41),
                              (str_store_string, s60, "@Defense"),
                              (assign, reg60, 0x00FFAA),
                              (store_sub, reg59, ":extended_diplomatic_status", 40),
                          (else_try),
                              (ge, ":extended_diplomatic_status", 21),
                              (str_store_string, s60, "@Trade"),
                              (assign, reg60, 0x00FFCC),
                              (store_sub, reg59, ":extended_diplomatic_status", 20),
                          (try_end),
                      (try_end),

                      (val_add, ":x_poshl", 50),

                      # diplomatic status and duration block (set at current line)
                      (create_text_overlay, reg10, s60, tf_left_align|tf_with_outline),
                      (overlay_set_size, reg10, ":line_size"),
                      (overlay_set_color, reg10, reg60),
                      (store_sub, ":line_x", ":x_posfhl", 20),
                      (store_add, ":line_y", ":y_pos", 54),
                      (position_set_x, pos3, ":line_x"),
                      (position_set_y, pos3, ":line_y"),
                      (overlay_set_position, reg10, pos3),

                      (create_text_overlay, reg10, "@{reg59?{reg59} days:}", tf_center_justify),
                      (overlay_set_size, reg10, ":line_size"),
                      (store_add, ":line_y", ":y_pos", 36),
                      (store_add, ":line_x", ":x_posfhl", 10),
                      (position_set_x, pos3, ":line_x"),
                      (position_set_y, pos3, ":line_y"),
                      (overlay_set_position, reg10, pos3),


                      # add diplomatic status
                      (store_relation, ":kingdom_relation", ":faction_line", ":faction_column"),

                      # kingdom relation (same line as faction name)
                      (assign, reg61, ":kingdom_relation"),
                      (create_text_overlay, reg10, "@{reg61}", tf_center_justify),
                      (overlay_set_size, reg10, ":line_size"),

                      (store_add, ":line_y", ":y_pos", 18),
                      (store_add, ":line_x", ":x_posfhl", 10),
                      (position_set_x, pos3, ":line_x"),
                      (position_set_y, pos3, ":line_y"),
                      (overlay_set_position, reg10, pos3),
                  (try_end), # end select alternate display
                (try_end),

                # increase column x position
                (val_add, ":x_posfhl", 90), # valid values 220, 385, 550, 715
            (try_end), # end of column faction loop

            # Faction line information, this is a 4 line block
            # reset x postion for next beginning column and decrease y position according to line count
            (assign, ":x_poshl", 165),

            (val_add, ":y_pos", 54), # linebreak

            # create a separator for faction line
            (create_mesh_overlay, reg1, "mesh_white_plane"),
            (overlay_set_color, reg1, 0x000000),
            (position_set_x, pos1, 42000),
            (position_set_y, pos1, 60),
            (overlay_set_size, reg1, pos1),
            (position_set_x, pos1, 17),
            (store_add, ":line_y", ":y_pos", 20), # set it 20 pix above current line
            (position_set_y, pos1, ":line_y"),
            (overlay_set_position, reg1, pos1),

            # Set line title
            (str_store_faction_name, s9, ":faction_line"),
            (str_store_string, s1, "@{s9}"),
            (create_text_overlay, reg10, s1, tf_left_align|tf_with_outline),
            (faction_get_color, ":faction_color", ":faction_line"),
            (overlay_set_color, reg10, ":faction_color"),

            (position_set_x, pos3, 750),
            (position_set_y, pos3, 850),
            (overlay_set_size, reg10, pos3),

            (position_set_x, pos3, 10),
            (position_set_y, pos3, ":y_pos"),
            (overlay_set_position, reg10, pos3),

            # set position for columns
            (assign, ":x_poshl", 165),
            (assign, ":line_size", 0),
            (position_set_x, ":line_size", 700),
            (position_set_y, ":line_size", 800),

            ## Player relation (first column)
            (store_relation, reg1, "fac_player_supporters_faction", ":faction_line"),

            # no clean strings existing, doing it the same way it's done in game_menu
            (try_begin),
                (ge, reg1, 90),
                (str_store_string, s3, "@Loyal"),
            (else_try),
                (ge, reg1, 80),
                (str_store_string, s3, "@Devoted"),
            (else_try),
                (ge, reg1, 70),
                (str_store_string, s3, "@Fond"),
            (else_try),
                (ge, reg1, 60),
                (str_store_string, s3, "@Gracious"),
            (else_try),
                (ge, reg1, 50),
                (str_store_string, s3, "@Friendly"),
            (else_try),
                (ge, reg1, 40),
                (str_store_string, s3, "@Supportive"),
            (else_try),
                (ge, reg1, 30),
                (str_store_string, s3, "@Favorable"),
            (else_try),
                (ge, reg1, 20),
                (str_store_string, s3, "@Cooperative"),
            (else_try),
                (ge, reg1, 10),
                (str_store_string, s3, "@Accepting"),
            (else_try),
                (ge, reg1, 0),
                (str_store_string, s3, "@Indifferent"),
            (else_try),
                (ge, reg1, -10),
                (str_store_string, s3, "@Suspicious"),
            (else_try),
                (ge, reg1, -20),
                (str_store_string, s3, "@Grumbling"),
            (else_try),
                (ge, reg1, -30),
                (str_store_string, s3, "@Hostile"),
            (else_try),
                (ge, reg1, -40),
                (str_store_string, s3, "@Resentful"),
            (else_try),
                (ge, reg1, -50),
                (str_store_string, s3, "@Angry"),
            (else_try),
                (ge, reg1, -60),
                (str_store_string, s3, "@Hateful"),
            (else_try),
                (ge, reg1, -70),
                (str_store_string, s3, "@Revengeful"),
            (else_try),
                (str_store_string, s3, "@Vengeful"),
            (try_end),

            # Set relation to player numerical value (same line)
            (create_text_overlay, reg10, "@{reg1}", tf_right_align),
            (overlay_set_size, reg10, ":line_size"),
            (store_add, ":line_x", ":x_poshl", 20),
            (position_set_x, pos1, ":line_x"),
            (position_set_y, pos1, ":y_pos"),
            (overlay_set_position, reg10, pos1),
            (overlay_set_color, reg10, ":line_color"),

            # Set relation to player string value (second line)
            (create_text_overlay, reg10, "@{s3}", tf_right_align),
            (overlay_set_size, reg10, ":line_size"),
            (position_set_x, pos1, ":line_x"),
            (store_sub, ":line_y", ":y_pos", 20),
            (position_set_y, pos1, ":line_y"),
            (overlay_set_position, reg10, pos1),
            (overlay_set_color, reg10, ":line_color"),

            # Set Faction Coat of Arm for standard faction (left of relation string)
            (try_begin),
                (neq, ":faction_line", "fac_player_supporters_faction"),
                (store_sub, ":mesh_index", ":faction_line", kingdoms_begin),
                (val_add, ":mesh_index", "mesh_pic_recruits"),
                (create_mesh_overlay, reg10, ":mesh_index"),
                (position_set_x, pos1, 75),
                (position_set_y, pos1, 75),
                (overlay_set_size, reg10, pos1),
                (position_set_x, pos1, 165),
                (store_sub, ":line_y", ":y_pos", 37),
                (position_set_y, pos1, ":line_y"),
                (overlay_set_position, reg10, pos1),
            (try_end),

            # for current line_faction count lords and centers
            (assign, ":num_lords", 0),
            (assign, ":num_caravans", 0),
            (assign, ":num_centers", 0),
            (assign, ":unassigned_centers", 0),
            (try_for_parties, ":cur_party"),
                (store_faction_of_party, ":cur_faction", ":cur_party"),
                (eq, ":cur_faction", ":faction_line"),

                (try_begin),
                    (party_slot_eq, ":cur_party", slot_party_type, spt_kingdom_hero_party),
                    (val_add, ":num_lords", 1),
                (else_try),
                    (party_slot_eq, ":cur_party", slot_party_type, spt_kingdom_caravan),
                    (val_add, ":num_caravans", 1),
                (else_try),
                    (this_or_next|party_slot_eq, ":cur_party", slot_party_type, spt_town),
                    (this_or_next|party_slot_eq, ":cur_party", slot_party_type, spt_castle),
                    (party_slot_eq, ":cur_party", slot_party_type, spt_village),
                    (val_add, ":num_centers", 1),

                    (try_begin),
                        (party_slot_eq, ":cur_party", slot_town_lord, stl_unassigned),
                        (val_add, ":unassigned_centers", 1),
                    (try_end),
                (try_end),
            (try_end), # end of parties loop

            # Count prisoners
            (assign, ":prisoners", 0),
            (try_for_range, ":lord_id", active_npcs_begin, active_npcs_end),
                (troop_slot_eq, ":lord_id", slot_troop_occupation, slto_kingdom_hero),
                (troop_slot_ge, ":lord_id", slot_troop_prisoner_of_party, 0),
                (store_troop_faction, ":lord_faction", ":lord_id"),
                (eq, ":lord_faction", ":faction_line"),
                (val_add, ":prisoners", 1),
            (try_end),

            # add count to last line for faction line report (second, third and fourth line)
            (assign, reg61, ":num_centers"),
            (assign, reg58, ":unassigned_centers"),
            (create_text_overlay, reg10, "@{reg61} {reg58?({reg58} U) :}Centers", tf_left_align),
            (overlay_set_size, reg10, ":line_size"),
            (position_set_x, pos1, 15),
            (store_sub, ":line_y", ":y_pos", 17),
            (position_set_y, pos1, ":line_y"),
            (overlay_set_position, reg10, pos1),
            (overlay_set_color, reg10, 0x000000),

            (assign, reg62, ":num_caravans"),
            (create_text_overlay, reg10, "@{reg62} Caravans", tf_left_align),
            (overlay_set_size, reg10, ":line_size"),
            (position_set_x, pos1, 15),
            (val_sub, ":line_y", 17),
            (position_set_y, pos1, ":line_y"),
            (overlay_set_position, reg10, pos1),
            (overlay_set_color, reg10, 0x000000),

            (assign, reg60, ":num_lords"),
            (assign, reg59, ":prisoners"),
            (create_text_overlay, reg10, "@{reg60} {reg59?({reg59} P) :}Lords", tf_left_align),
            (overlay_set_size, reg10, ":line_size"),
            (position_set_x, pos1, 15),
            (val_sub, ":line_y", 17),
            (position_set_y, pos1, ":line_y"),
            (overlay_set_position, reg10, pos1),
            (overlay_set_color, reg10, 0x000000),

            # increase line for next faction block
            (val_add, ":y_pos", 18),#linebreak

        (try_end), # end of faction loop
        (set_container_overlay, -1),
   ]),
   ## END on load trigger

   ## Check for buttonpress
  (ti_on_presentation_event_state_change,
    [
      (store_trigger_param_1, ":button_pressed_id"),
      (try_begin),
        (eq, ":button_pressed_id", "$g_jrider_faction_report_Return_to_menu"), # pressed  (Return to menu)
        (presentation_set_duration, 0),
      #gekokujo 3.1 faction relations report start
      (else_try),
        (eq, ":button_pressed_id", "$gekokujo_fac_report_next"), # pressed Next
    
        #count total number of factions so the button never adds over
        (assign, ":fac_count", 0),
        (try_for_range, ":faction", kingdoms_begin, kingdoms_end),
          (faction_slot_eq, ":faction", slot_faction_state, sfs_active),
          (val_add, ":fac_count", 1),
        (try_end),
        (val_sub, ":fac_count", 6), #last faction is last displayed
        (lt, "$gekokujo_fac_report_offset", ":fac_count"),
        
        (val_add, "$gekokujo_fac_report_offset", 1),
        (start_presentation, "prsnt_jrider_faction_relations_report"),
      (else_try),
        (eq, ":button_pressed_id", "$gekokujo_fac_report_prev"), # pressed Prev
        (gt, "$gekokujo_fac_report_offset", 0),
        (val_sub, "$gekokujo_fac_report_offset", 1),
        (start_presentation, "prsnt_jrider_faction_relations_report"),
      #gekokujo 3.1 faction relations report end
      (try_end),
    ]),
   ## END presentation event state change trigger

   ## Event to process when running the presentation
   (ti_on_presentation_run,
    [
        (try_begin),
      (this_or_next|key_clicked, key_escape),
      (key_clicked, key_right_mouse_button),
      (presentation_set_duration, 0),
      (jump_to_menu, "mnu_reports"),
        (try_end),

        ]),
   ]),
  # END presentation run trigger
  # END Faction relation presentation
  # Jrider -

##diplomacy end
##diplomacy start+
##Custom player kingdom vassal titles, credit Caba`drin start
#(Updated 2011-04-24, to use Caba`drin's 2011-04-20 bug-fix and update)
# See http://forums.taleworlds.com/index.php/topic,148259.0.html
("dplmc_set_vassal_title",0,mesh_load_window,[
      (ti_on_presentation_load,
       [(set_fixed_point_multiplier, 1000),
        (str_clear, s1),
        (str_clear, s2),

        (create_text_overlay, reg0, "@How will your male vassals be known?", tf_center_justify),
        (position_set_x, pos1, 500),
        (position_set_y, pos1, 600),
        (overlay_set_position, reg0, pos1),
        (create_text_overlay, reg0, "@How will your female vassals be known?", tf_center_justify),
        (position_set_x, pos1, 500),
        (position_set_y, pos1, 400),
        (overlay_set_position, reg0, pos1),

        (create_simple_text_box_overlay, "$g_presentation_obj_name_kingdom_1"),
        (position_set_x, pos1, 400),
        (position_set_y, pos1, 500),
        (overlay_set_position, "$g_presentation_obj_name_kingdom_1", pos1),
        (try_begin),
          (troop_slot_eq, "trp_heroes_end", 0, 1), #Pick a slot
          (str_store_troop_name, s0, "trp_heroes_end"),
        (else_try),
          (str_store_string, s0, "@{!}"),
          (str_store_string, s0, "str_faction_title_male_player"),
        (try_end),
        (overlay_set_text, "$g_presentation_obj_name_kingdom_1", s0),

        (create_simple_text_box_overlay, reg0),
        (position_set_x, pos1, 400),
        (position_set_y, pos1, 300),
        (overlay_set_position, reg0, pos1),
        (try_begin),
          (troop_slot_eq, "trp_heroes_end", 1, 1), #Pick a slot
          (str_store_troop_name_plural, s0, "trp_heroes_end"),
        (else_try),
          (str_store_string, s0, "@{!}"),
          (str_store_string, s0, "str_faction_title_female_player"),
        (try_end),
        (overlay_set_text, reg0, s0),

        (create_button_overlay, reg0, "@Use the Titles Entered Above.", tf_center_justify),
        (position_set_x, pos1, 600),
        (position_set_y, pos1, 150),
        (overlay_set_position, reg0, pos1),

        (create_button_overlay, reg0, "@Use Default Titles (Lord/Lady).", tf_center_justify),
        (position_set_x, pos1, 600),
        (position_set_y, pos1, 100),
        (overlay_set_position, reg0, pos1),

        (presentation_set_duration, 999999),
        ]),
      (ti_on_presentation_event_state_change,
       [(store_trigger_param_1, ":object"),
        (try_begin),
          (eq, ":object", "$g_presentation_obj_name_kingdom_1"),
          (str_store_string, s1, s0), #Male Title
        (else_try),
          (store_add, ":overlay", "$g_presentation_obj_name_kingdom_1", 1),
          (eq, ":object", ":overlay"),
          (str_store_string, s2, s0), ##Female Title
        (else_try),
          (val_add, ":overlay", 1),
          (eq, ":object", ":overlay"), #Custom
          (try_begin),
            (neg|str_is_empty, s1),
            (troop_set_name, "trp_heroes_end", s1),
            (troop_set_slot, "trp_heroes_end", 0, 1),
            (try_for_range, ":lord_lady", lords_begin, lords_end),
                (store_troop_faction, ":faction", ":lord_lady"),
                (eq, ":faction", "fac_player_supporters_faction"),
                (call_script, "script_troop_set_title_according_to_faction", ":lord_lady", ":faction"),
            (try_end),
          (try_end),
          (try_begin),
            (neg|str_is_empty, s2),
            (troop_set_plural_name, "trp_heroes_end", s2),
            (troop_set_slot, "trp_heroes_end", 1, 1),
            (try_for_range, ":lord_lady", kingdom_ladies_begin, kingdom_ladies_end),
                (store_troop_faction, ":faction", ":lord_lady"),
                (eq, ":faction", "fac_player_supporters_faction"),
                (call_script, "script_troop_set_title_according_to_faction", ":lord_lady", ":faction"),
            (try_end),
          (try_end),
          (try_begin),
            (this_or_next|neg|str_is_empty, s1),
            (neg|str_is_empty, s2),
			#gekokujo 3.0 microfactions! include fort companions start
            #(try_for_range, ":lord_lady", companions_begin, companions_end),
            (try_for_range, ":lord_lady", companions_begin, fort_companions_end),
			#gekokujo 3.0 microfactions! include fort companions end
                (store_troop_faction, ":faction", ":lord_lady"),
                (eq, ":faction", "fac_player_supporters_faction"),
                (troop_slot_eq, ":lord_lady", slot_troop_occupation, slto_kingdom_hero),
                (call_script, "script_troop_set_title_according_to_faction", ":lord_lady", ":faction"),
            (try_end),
          (try_end),
          (presentation_set_duration, 0),
        (else_try),
          (val_add, ":overlay", 1),
          (eq, ":object", ":overlay"), #Default
          (troop_set_slot, "trp_heroes_end", 0, 0),
          (troop_set_slot, "trp_heroes_end", 1, 0),
          (try_for_range, ":lord_lady", lords_begin, kingdom_ladies_end),
            (neg|is_between, ":lord_lady", pretenders_begin, pretenders_end),
            (store_troop_faction, ":faction", ":lord_lady"),
            (eq, ":faction", "fac_player_supporters_faction"),
            (call_script, "script_troop_set_title_according_to_faction", ":lord_lady", ":faction"),
          (try_end),
		  #gekokujo 3.0 microfactions! include fort companions start
          #(try_for_range, ":lord_lady", companions_begin, companions_end),
          (try_for_range, ":lord_lady", companions_begin, fort_companions_end),
		  #gekokujo 3.0 microfactions! include fort companions end
            (store_troop_faction, ":faction", ":lord_lady"),
            (eq, ":faction", "fac_player_supporters_faction"),
            (troop_slot_eq, ":lord_lady", slot_troop_occupation, slto_kingdom_hero),
            (call_script, "script_troop_set_title_according_to_faction", ":lord_lady", ":faction"),
          (try_end),
          (presentation_set_duration, 0),
        (try_end),
        ]),
      ]),
##Custom player kingdom vassal titles, credit Caba`drin end

##Auto-Sell, credit rubik (Custom Commander) begin
##Adds global variables:
#  $g_sell_items_when_leaving, renamed to g_dplmc_sell_items_when_leaving
#  $g_auto_sell_price_limit, renamed to g_dplmc_auto_sell_price_limit
##Adds slot:
#  slot_item_type_not_for_sell, renamed to dplmc_slot_item_type_not_for_sell
  ("dplmc_auto_sell_options", 0, mesh_load_window, [
    (ti_on_presentation_load,
      [
        (presentation_set_duration, 999999),
        (set_fixed_point_multiplier, 1000),

        ## do auto-sell automaticly when leaving
        (create_text_overlay, reg0, "@Sell items automatically when leaving:", tf_vertical_align_center),
        (position_set_x, pos1, 170),
        (position_set_y, pos1, 660),
        (overlay_set_position, reg0, pos1),

        (create_check_box_overlay, "$g_presentation_obj_1", "mesh_checkbox_off", "mesh_checkbox_on"),
        (position_set_x, pos1, 150),
        (position_set_y, pos1, 652),
        (overlay_set_position, "$g_presentation_obj_1", pos1),
        (overlay_set_val, "$g_presentation_obj_1", "$g_dplmc_sell_items_when_leaving"),

        ## price_limit
        (create_text_overlay, reg0, "@Price limit for auto-sell:", tf_vertical_align_center),
        (position_set_x, pos1, 150),
        (position_set_y, pos1, 610),
        (overlay_set_position, reg0, pos1),

        (create_number_box_overlay, "$g_presentation_obj_2", 10, 10000),
        (position_set_x, pos1, 600),
        (position_set_y, pos1, 596),
        (overlay_set_val, "$g_presentation_obj_2", "$g_dplmc_auto_sell_price_limit"),
        (overlay_set_position, "$g_presentation_obj_2", pos1),

        # done
        (create_game_button_overlay, "$g_presentation_obj_3", "@Done"),
        (position_set_x, pos1, 900),
        (position_set_y, pos1, 25),
        (overlay_set_position, "$g_presentation_obj_3", pos1),

        ## Item types
        (create_text_overlay, reg0, "@Item types for auto-sell:", tf_vertical_align_center),
        (position_set_x, pos1, 150),
        (position_set_y, pos1, 578),
        (overlay_set_position, reg0, pos1),

        # select all
        (create_image_button_overlay, "$g_presentation_obj_5", "mesh_drop_button_child", "mesh_drop_button_child_down"),
        (position_set_x, pos1, 160),
        (position_set_y, pos1, 528),
        (overlay_set_position, "$g_presentation_obj_5", pos1),
        (create_text_overlay, reg1, "@Select all", tf_center_justify|tf_vertical_align_center),
        (position_set_x, pos1, 265),
        (position_set_y, pos1, 538),
        (overlay_set_position, reg1, pos1),

        # select invert
        (create_image_button_overlay, "$g_presentation_obj_6", "mesh_drop_button_child", "mesh_drop_button_child_down"),
        (position_set_x, pos1, 385),
        (position_set_y, pos1, 528),
        (overlay_set_position, "$g_presentation_obj_6", pos1),
        (create_text_overlay, reg1, "@Select invert", tf_center_justify|tf_vertical_align_center),
        (position_set_x, pos1, 490),
        (position_set_y, pos1, 538),
        (overlay_set_position, reg1, pos1),

        (assign, ":pos_x", 160),
        (assign, ":pos_y", 500),
        (try_for_range, ":cur_type", 0, 20),
          (store_add, ":cur_item_type", itp_type_horse, ":cur_type"),
          (neq, ":cur_item_type", itp_type_goods),
          (neq, ":cur_item_type", itp_type_animal),
          (neq, ":cur_item_type", itp_type_book),
          # button
          (position_set_x, pos1, ":pos_x"),
          (position_set_y, pos1, ":pos_y"),
          (create_mesh_overlay, reg1, "mesh_drop_button_child"),
          (overlay_set_position, reg1, pos1),
          # text
          (store_add, ":text_pos_x", ":pos_x", 120),
          (store_add, ":text_pos_y", ":pos_y", 10),
          (position_set_x, pos1, ":text_pos_x"),
          (position_set_y, pos1, ":text_pos_y"),
          (store_add, ":out_string", "str_dplmc_hero_wpn_slot_horse", ":cur_type"),#<- dplmc+ added "dplmc" prefix
          (str_store_string, s1, ":out_string"),
          (create_text_overlay, reg1, "@{s1}", tf_center_justify|tf_vertical_align_center),
          (overlay_set_position, reg1, pos1),
          # checkbox
          (store_add, ":checkbox_pos_x", ":pos_x", 0),
          (store_add, ":checkbox_pos_y", ":pos_y", 4),
          (position_set_x, pos1, ":checkbox_pos_x"),
          (position_set_y, pos1, ":checkbox_pos_y"),
          (create_check_box_overlay, reg1, "mesh_checkbox_off", "mesh_checkbox_on"),
          (overlay_set_position, reg1, pos1),
          (store_add, ":item_type", itp_type_horse, ":cur_type"),
          (item_get_slot, ":for_sell", ":item_type", dplmc_slot_item_type_not_for_sell),
          (store_sub, ":for_sell", 1, ":for_sell"),
          (overlay_set_val, reg1, ":for_sell"),
          (troop_set_slot, "trp_temp_array_b", ":cur_type", reg1),
          # focous
          (val_add, ":pos_x", 225),
          (try_begin),
            (eq, ":pos_x", 835),
            (assign, ":pos_x", 160),
            (val_sub, ":pos_y", 28),
          (try_end),
        (try_end),

        ####### mouse fix pos system #######
        #(call_script, "script_mouse_fix_pos_ready"),
        ####### mouse fix pos system #######
      ]),

      #(ti_on_presentation_run,
        #[
        ####### mouse fix pos system #######
        #(call_script, "script_mouse_fix_pos_run"),
        ####### mouse fix pos system #######
      #]),

    (ti_on_presentation_event_state_change,
      [
        (store_trigger_param_1, ":object"),
        (store_trigger_param_2, ":value"),

        (try_begin),
          (eq, ":object", "$g_presentation_obj_1"),
          (assign, "$g_dplmc_sell_items_when_leaving", ":value"),
        (else_try),
          (eq, ":object", "$g_presentation_obj_2"),
          (assign, "$g_dplmc_auto_sell_price_limit", ":value"),
        (else_try),
          (eq, ":object", "$g_presentation_obj_3"),
          (presentation_set_duration, 0),
        (else_try),
          ## select all
          (eq, ":object", "$g_presentation_obj_5"),
          (try_for_range, ":cur_type", 0, 20),
            (store_add, ":cur_item_type", itp_type_horse, ":cur_type"),
            (neq, ":cur_item_type", itp_type_goods),
            (neq, ":cur_item_type", itp_type_animal),
            (neq, ":cur_item_type", itp_type_book),
            (item_set_slot, ":cur_item_type", dplmc_slot_item_type_not_for_sell, 0),
            (troop_get_slot, ":dest_checkbox", "trp_temp_array_b", ":cur_type"),
            (overlay_set_val, ":dest_checkbox", 1),
          (try_end),
        (else_try),
          ## select invert
          (eq, ":object", "$g_presentation_obj_6"),
          (try_for_range, ":cur_type", 0, 20),
            (store_add, ":cur_item_type", itp_type_horse, ":cur_type"),
            (neq, ":cur_item_type", itp_type_goods),
            (neq, ":cur_item_type", itp_type_animal),
            (neq, ":cur_item_type", itp_type_book),
            (item_get_slot, ":for_sell", ":cur_item_type", dplmc_slot_item_type_not_for_sell),
            (val_add, ":for_sell", 1),
            (val_mod, ":for_sell", 2),
            (item_set_slot, ":cur_item_type", dplmc_slot_item_type_not_for_sell, ":for_sell"),
            (troop_get_slot, ":dest_checkbox", "trp_temp_array_b", ":cur_type"),
            (store_sub, ":dest_val", 1, ":for_sell"),
            (overlay_set_val, ":dest_checkbox", ":dest_val"),
          (try_end),
        (try_end),

        ## checkboxes
        (try_for_range, ":slot_item_type_checkbox", 0, 20),
          (troop_slot_eq, "trp_temp_array_b", ":slot_item_type_checkbox", ":object"),
          (store_add, ":item_type", itp_type_horse, ":slot_item_type_checkbox"),
          (store_sub, ":for_sell", 1, ":value"),
          (item_set_slot, ":item_type", dplmc_slot_item_type_not_for_sell, ":for_sell"),
        (try_end),
      ]),
    ]),
##auto-sell, credit rubik (Custom Commander) end

##Auto-Buy-Food shopping list management credit rubik (Custom Commander), end
##
##Global variables used:
##   $g_buy_foods_when_leaving changed to $g_dplmc_buy_food_when_leaving
##
##Slots used:
##   slot_item_food_portion, renamed to dplmc_slot_item_food_portion
  ("dplmc_shopping_list_of_food", 0, mesh_load_window, [
    (ti_on_presentation_load,
      [
        (presentation_set_duration, 999999),
        (set_fixed_point_multiplier, 1000),

        ## back
        (create_game_button_overlay, "$g_presentation_obj_1", "@Done"),
        (position_set_x, pos1, 900),
        (position_set_y, pos1, 25),
        (overlay_set_position, "$g_presentation_obj_1", pos1),

        ## buy food automatically when leaving
        (create_text_overlay, reg0, "@Buy food automatically when leaving:", tf_vertical_align_center),
        (position_set_x, pos1, 170),
        (position_set_y, pos1, 690),
        (overlay_set_position, reg0, pos1),

        (create_check_box_overlay, "$g_presentation_obj_2", "mesh_checkbox_off", "mesh_checkbox_on"),
        (position_set_x, pos1, 150),
        (position_set_y, pos1, 682),
        (overlay_set_position, "$g_presentation_obj_2", pos1),
        (overlay_set_val, "$g_presentation_obj_2", "$g_dplmc_buy_food_when_leaving"),

        (assign, ":pos_x", 60),
        (assign, ":pos_y", 550),
        (try_for_range, ":cur_food", food_begin, food_end),
          # frame
          (create_mesh_overlay, reg1, "mesh_inv_slot"),
          (position_set_x, pos1, 800),
          (position_set_y, pos1, 800),
          (overlay_set_size, reg1, pos1),
          (position_set_x, pos1, ":pos_x"),
          (position_set_y, pos1, ":pos_y"),
          (overlay_set_position, reg1, pos1),
          # back ground
          (create_mesh_overlay, reg1, "mesh_mp_inventory_choose"),
          (position_set_x, pos1, 640),
          (position_set_y, pos1, 640),
          (overlay_set_size, reg1, pos1),
          (position_set_x, pos1, ":pos_x"),
          (position_set_y, pos1, ":pos_y"),
          (overlay_set_position, reg1, pos1),
          # item overlay
          (troop_set_slot, "trp_temp_array_a", ":cur_food", reg1),
          (create_mesh_overlay_with_item_id, reg1, ":cur_food"),
          (position_set_x, pos1, 800),
          (position_set_y, pos1, 800),
          (overlay_set_size, reg1, pos1),
          (store_add, ":item_x", ":pos_x", 40),
          (store_add, ":item_y", ":pos_y", 40),
          (position_set_x, pos1, ":item_x"),
          (position_set_y, pos1, ":item_y"),
          (overlay_set_position, reg1, pos1),
          (troop_set_slot, "trp_temp_array_b", ":cur_food", reg1),
          # text *
          (create_text_overlay, reg1, "@*", tf_center_justify|tf_vertical_align_center),
          (store_add, ":text_x", ":pos_x", 100),
          (store_add, ":text_y", ":pos_y", 40),
          (position_set_x, pos1, ":text_x"),
          (position_set_y, pos1, ":text_y"),
          (overlay_set_position, reg1, pos1),
          # number_box
          (create_number_box_overlay, reg1, 0, 5),
          (store_add, ":number_box_x", ":pos_x", 115),
          (store_add, ":number_box_y", ":pos_y", 30),
          (position_set_x, pos1, ":number_box_x"),
          (position_set_y, pos1, ":number_box_y"),
          (overlay_set_position, reg1, pos1),
          (item_get_slot, ":food_portion", ":cur_food", dplmc_slot_item_food_portion),
          (overlay_set_val, reg1, ":food_portion"),
          (troop_set_slot, "trp_temp_array_c", ":cur_food", reg1),
          # next
          (val_add, ":pos_x", 240),
          (try_begin),
            (eq, ":pos_x", 1020),
            (assign, ":pos_x", 60),
            (val_sub, ":pos_y", 120),
          (try_end),
        (try_end),

        ####### mouse fix pos system #######
        #(call_script, "script_mouse_fix_pos_ready"),
        ####### mouse fix pos system #######
      ]),

    #(ti_on_presentation_run,
      #[
        ####### mouse fix pos system #######
        #(call_script, "script_mouse_fix_pos_run"),
        ####### mouse fix pos system #######
    #]),

    (ti_on_presentation_mouse_enter_leave,
      [
      (store_trigger_param_1, ":object"),
      (store_trigger_param_2, ":enter_leave"),

      (try_begin),
        (eq, ":enter_leave", 0),
        (try_for_range, ":cur_food", food_begin, food_end),
          (troop_slot_eq, "trp_temp_array_a", ":cur_food", ":object"),
          (troop_get_slot, ":target_obj", "trp_temp_array_b", ":cur_food"),
          (overlay_get_position, pos0, ":target_obj"),
          (show_item_details, ":cur_food", pos0, 100),
          (assign, "$g_current_opened_item_details", ":cur_food"),
        (try_end),
      (else_try),
        (try_for_range, ":cur_food", food_begin, food_end),
          (troop_slot_eq, "trp_temp_array_a", ":cur_food", ":object"),
          (try_begin),
            (eq, "$g_current_opened_item_details", ":cur_food"),
            (close_item_details),
          (try_end),
        (try_end),
      (try_end),
    ]),

    (ti_on_presentation_event_state_change,
      [
        (store_trigger_param_1, ":object"),
        (store_trigger_param_2, ":value"),

        (try_for_range, ":cur_food", food_begin, food_end),
          (troop_slot_eq, "trp_temp_array_c", ":cur_food", ":object"),
          (item_set_slot, ":cur_food", dplmc_slot_item_food_portion, ":value"),
        (try_end),

        (try_begin),
          (eq, ":object", "$g_presentation_obj_2"),
          (assign, "$g_dplmc_buy_food_when_leaving", ":value"),
        (else_try),
          (eq, ":object", "$g_presentation_obj_1"),
          (presentation_set_duration, 0),
        (try_end),
    ]),
  ]),
##Auto-Buy-Food shopping list management credit rubik (Custom Commander), end

# Jrider +
  ##############################################################################
  # REPORT PRESENTATIONS v1.2
  ## Character relations report
  ("jrider_character_relation_report", 0,
   mesh_message_window,
   [
     ## Load Presentation
     (ti_on_presentation_load,
      # generic_ti_on_load +
      [
    (presentation_set_duration, 999999),
        (set_fixed_point_multiplier, 1000),

        (str_clear, s0),
        (str_clear, s1),

        # Character presentation type variations
        (try_begin),
            ###############################
            ## Courtship Relations presentation
            (eq, "$g_character_presentation_type", 0),

            # Set presentation title string
            (str_store_string, s0, "@_Courtships in progress_"),

            # Set size of listbox
            (assign, ":base_scroll_y", 160),
            (assign, ":base_scroll_size_y", 480),
            (assign, ":base_candidates_y", 0), # scrollable area size minus (one line size + 2) 430

            # Set storage index
            (assign, "$g_base_character_presentation_storage_index", 1000),

            # presentation specific extra overlays
            (call_script, "script_generate_knonwn_poems_string"),

            # Extra text area for knowns poems (filling once so we use a register), filled from s1 generated in script call
            (create_text_overlay, reg1, s1, tf_left_align),
            (position_set_x, pos1, 590), # position
            (position_set_y, pos1, 55),
            (overlay_set_position, reg1, pos1),
            (position_set_x, pos1, 750), # size
            (position_set_y, pos1, 850),
            (overlay_set_size, reg1, pos1),
            (overlay_set_color, reg1, 0xFF66CC), # color
        (else_try),
            ###############################
            ## Lord Relations presentation
            (eq, "$g_character_presentation_type", 1),

            # Set presentation title string
            (str_store_string, s0, "@_Known Lords by Relation_"),

            # Set size of listbox
            (assign, ":base_scroll_y", 110),
            (assign, ":base_scroll_size_y", 550),
            (assign, ":base_candidates_y", 0), # scrollable area size minus 530

            # Set storage index
            (assign, "$g_base_character_presentation_storage_index", 2000),
        (else_try),
            ###############################
            ## Player and Companions presentation
            (eq, "$g_character_presentation_type", 2),

            # Set presentation title string
            (str_store_string, s0, "@_Character & Companions_"),

            # Set size of listbox
            (assign, ":base_scroll_y", 110),
            (assign, ":base_scroll_size_y", 550),
            (assign, ":base_candidates_y", 0), # scrollable area size minus (one line size + 2) 530

            # Set storage index
            (assign, "$g_base_character_presentation_storage_index", 3000),

            # Extra area for equipment display
            (assign, ":inv_bar_size", 0),
            (position_set_x, ":inv_bar_size", 400),
            (position_set_y, ":inv_bar_size", 400),

            (create_mesh_overlay, reg1, "mesh_mp_inventory_left"),
            (position_set_x, pos1, 67),
            (position_set_y, pos1, 300),
            (overlay_set_position, reg1, pos1),
            (overlay_set_size, reg1, ":inv_bar_size"),

            (create_mesh_overlay, reg1, "mesh_mp_inventory_right"),
            (position_set_x, pos1, 450),
            (position_set_y, pos1, 330),
            (overlay_set_position, reg1, pos1),
            (overlay_set_size, reg1, ":inv_bar_size"),
        (try_end),
        # END of presentation type specific init and static overlay

        ###############################
        # Create common overlays
        # set foreground mesh overlay (has some transparency in it, so can't use it directly)
        (create_mesh_overlay, reg1, "mesh_face_gen_window"),
        (position_set_x, pos1, 0),
        (position_set_y, pos1, 0),
        (overlay_set_position, reg1, pos1),
    (position_set_x, pos1, 1000),
        (position_set_y, pos1, 1000),
    (overlay_set_size, reg1, pos1),

    # Presentation title overlay, centered at the top of right pane (from s0, presentation type specific)
        (create_text_overlay, reg1, s0, tf_center_justify),
        (overlay_set_color, reg1, 0xDDDDDD),
    (position_set_x, pos1, 740), # Higher, means more toward the right
        (position_set_y, pos1, 680), # Higher, means more toward the top
        (overlay_set_position, reg1, pos1),
    (position_set_x, pos1, 1200),
        (position_set_y, pos1, 1200),
    (overlay_set_size, reg1, pos1),

    # Done button
        (create_game_button_overlay, "$g_jrider_character_report_Return_to_menu", "@_Done_"),
        (position_set_x, pos1, 290),
        (position_set_y, pos1, 10),
        (overlay_set_position, "$g_jrider_character_report_Return_to_menu", pos1),

        # Character Information text to fill when an entry is clicked in the list
        (create_text_overlay, "$g_jrider_character_information_text", "str_space", tf_left_align),
        (overlay_set_color, "$g_jrider_character_information_text", 0xFFFFFF),
        (position_set_x, pos1, 55), # Higher, means more toward the right
        (position_set_y, pos1, 60), # Higher, means more toward the top
        (overlay_set_position, "$g_jrider_character_information_text", pos1),
        (position_set_x, pos1, 700), # smaller means smaller font
        (position_set_y, pos1, 800),
        (overlay_set_size, "$g_jrider_character_information_text", pos1),

        # Character selection listbox overlay
        # use scrollable text area with global reference so objects can be put inside using overlay_set_container
        (create_text_overlay, "$g_jrider_character_relation_listbox", "str_empty_string", tf_scrollable_style_2),
        (position_set_x, pos1, 590),
        (position_set_y, pos1, ":base_scroll_y"),
        (overlay_set_position, "$g_jrider_character_relation_listbox", pos1),
        (position_set_x, pos1, 335),
        (position_set_y, pos1, ":base_scroll_size_y"),
        (overlay_set_area_size, "$g_jrider_character_relation_listbox", pos1),

        # Faction filter
        (create_combo_button_overlay, "$g_jrider_character_faction_filter", "str_empty_string",0),
        (position_set_x, pos1, 507),
        (position_set_y, pos1, 709),
        (overlay_set_position, "$g_jrider_character_faction_filter", pos1),
        (position_set_x, pos1, 550),
        (position_set_y, pos1, 650),
        (overlay_set_size, "$g_jrider_character_faction_filter", pos1),

        # add elements to filter button
        (overlay_add_item, "$g_jrider_character_faction_filter", "@Your supporters"),
		#gekokujo 3.0 name changes and additional factions
        #(overlay_add_item, "$g_jrider_character_faction_filter", "@Swadians"),
        #(overlay_add_item, "$g_jrider_character_faction_filter", "@Vaegirs"),
        #(overlay_add_item, "$g_jrider_character_faction_filter", "@Khergits"),
        #(overlay_add_item, "$g_jrider_character_faction_filter", "@Nords"),
        #(overlay_add_item, "$g_jrider_character_faction_filter", "@Rhodoks"),
        #(overlay_add_item, "$g_jrider_character_faction_filter", "@Sarranids"),
        (overlay_add_item, "$g_jrider_character_faction_filter", "@Uesugi"),
        (overlay_add_item, "$g_jrider_character_faction_filter", "@Date"),
        (overlay_add_item, "$g_jrider_character_faction_filter", "@Oda"),
        (overlay_add_item, "$g_jrider_character_faction_filter", "@Mori"),
        (overlay_add_item, "$g_jrider_character_faction_filter", "@Takeda"),
        (overlay_add_item, "$g_jrider_character_faction_filter", "@Tokugawa"),
        (overlay_add_item, "$g_jrider_character_faction_filter", "@Miyoshi"),
        (overlay_add_item, "$g_jrider_character_faction_filter", "@Amako"),
        (overlay_add_item, "$g_jrider_character_faction_filter", "@Otomo"),
        (overlay_add_item, "$g_jrider_character_faction_filter", "@Nanbu"),
        (overlay_add_item, "$g_jrider_character_faction_filter", "@Asakura"),
        (overlay_add_item, "$g_jrider_character_faction_filter", "@Chosokabe"),
        (overlay_add_item, "$g_jrider_character_faction_filter", "@Hojo"),
        (overlay_add_item, "$g_jrider_character_faction_filter", "@Mogami"),
        (overlay_add_item, "$g_jrider_character_faction_filter", "@Shimazu"),
        (overlay_add_item, "$g_jrider_character_faction_filter", "@Ryuzoji"),
        (overlay_add_item, "$g_jrider_character_faction_filter", "@Satake"),
        (overlay_add_item, "$g_jrider_character_faction_filter", "@Satomi"),
        (overlay_add_item, "$g_jrider_character_faction_filter", "@Ukita"),
        (overlay_add_item, "$g_jrider_character_faction_filter", "@Ikko Ikki"),
        (overlay_add_item, "$g_jrider_character_faction_filter", "@All Factions"),

        # Set initial value for selection box
        (try_begin),
            (this_or_next|eq, "$g_jrider_pres_called_from_menu", 1),
            (eq, "$g_jrider_faction_filter", -1),

            (assign, "$g_jrider_faction_filter", -1),
			#gekokujo 3.0 "all factions" is now index 21
            #(overlay_set_val, "$g_jrider_character_faction_filter", 7),
            (overlay_set_val, "$g_jrider_character_faction_filter", 21),
        (else_try),
            (overlay_set_val, "$g_jrider_character_faction_filter", "$g_jrider_faction_filter"),
        (try_end),

        ###############################
        # Populate lists
        # Init presentation common global variables
        (assign, "$num_charinfo_candidates", 0),

        # Fill listbox (overlay_add_item and extra storage)
        (call_script, "script_fill_relation_canditate_list_for_presentation", "$g_character_presentation_type", ":base_candidates_y"),
        (assign, "$g_jrider_reset_selected_on_faction", 0),
        # stop if there's no candidate
        (gt, "$num_charinfo_candidates", 0),

        # get extra information from storage
        (store_add, ":current_storage_index", "$g_base_character_presentation_storage_index", "$g_latest_character_relation_entry"),
        (troop_get_slot, "$character_info_id", "trp_temp_array_c", ":current_storage_index"),

        # Fill text information for current entry and update text information overlay
        (call_script, "script_generate_extended_troop_relation_information_string", "$character_info_id"),
        (overlay_set_text, "$g_jrider_character_information_text", s1),

        # color selected entry
        (overlay_set_color, "$g_jrider_last_checked_indicator", 0xFF6666FF),
        (overlay_set_alpha, "$g_jrider_last_checked_indicator", 0x44),

        # Begin common dynamic overlay
        # mesh Overlay for character portrait (global not needed)
        (create_image_button_overlay_with_tableau_material, "$g_jrider_character_portrait", -1, "tableau_troop_note_mesh", "$character_info_id"),
        (position_set_x, pos2, 100),
        (position_set_y, pos2, 280),
        (overlay_set_position, "$g_jrider_character_portrait", pos2),
        (position_set_x, pos2, 1100), #1150
        (position_set_y, pos2, 1100), #1150
        (overlay_set_size, "$g_jrider_character_portrait", pos2),

        # mesh Overlay for faction coat of arms
        (try_begin),
            (store_troop_faction, ":troop_faction", "$character_info_id"),
            (neq, ":troop_faction", "fac_player_supporters_faction"),
            (is_between, ":troop_faction", kingdoms_begin, kingdoms_end),
            (store_sub, ":faction_mesh_index", ":troop_faction", kingdoms_begin),
            (val_add, ":faction_mesh_index", "mesh_pic_recruits"),

            (create_mesh_overlay, "$g_jrider_faction_coat_of_arms", ":faction_mesh_index"),
            (position_set_x, pos3, 150),
            (position_set_y, pos3, 600),
            (overlay_set_position, "$g_jrider_faction_coat_of_arms", pos3),
            (position_set_x, pos3, 250),
            (position_set_y, pos3, 250),
            (overlay_set_size, "$g_jrider_faction_coat_of_arms", pos3),
        (try_end),

        # Begin presentation type specific dynamic overlay
        # equipement meshes for character/companions
        (try_begin),
            (eq, "$g_character_presentation_type", 2),

            (assign, ":base_inv_slot_x", 452),
            (assign, ":base_inv_slot_y", 536),

            (try_for_range, ":item_eq", 0, 9),
            # loop equipment slots
                (troop_get_inventory_slot, reg1, "$character_info_id", ":item_eq"),

                (try_begin),
                    (eq, ":item_eq", 4),
                    (assign, ":base_inv_slot_x", 68),
                    (assign, ":base_inv_slot_y", 557),
                (try_end),
                (try_begin),
                    (lt, reg1, 1),
                    # empty... assign default mesh
                   (try_begin),
                       (lt, ":item_eq", 4),
                       (assign, ":mesh_id", "mesh_mp_inventory_slot_equip"),
                   (else_try),
                       (eq, ":item_eq", 4),
                       (assign, ":mesh_id", "mesh_mp_inventory_slot_helmet"),
                   (else_try),
                       (eq, ":item_eq", 5),
                       (assign, ":mesh_id", "mesh_mp_inventory_slot_armor"),
                   (else_try),
                       (eq, ":item_eq", 6),
                       (assign, ":mesh_id", "mesh_mp_inventory_slot_boot"),
                   (else_try),
                       (eq, ":item_eq", 7),
                       (assign, ":mesh_id", "mesh_mp_inventory_slot_glove"),
                   (else_try),
                       (eq, ":item_eq", 8),
                       (assign, ":mesh_id", "mesh_mp_inventory_slot_horse"),
                   (try_end),

                   (create_mesh_overlay, reg11, ":mesh_id"),
                   (overlay_set_size, reg11, ":inv_bar_size"),

                   (position_set_x, pos1, ":base_inv_slot_x"),
                   (position_set_y, pos1, ":base_inv_slot_y"),
                   (overlay_set_position, reg11, pos1),

                   (troop_set_slot, "trp_temp_array_a", ":item_eq", -1),
                   (store_add, ":item_eq_id", ":item_eq", 10),
                   (troop_set_slot, "trp_temp_array_a", ":item_eq_id", -1),
                # end missing item
                (else_try),
                    (create_mesh_overlay_with_item_id, reg10, reg1),
                    (position_set_x, pos1, 450),
                    (position_set_y, pos1, 450),
                    (overlay_set_size, reg10, pos1),

                    (store_add, ":item_inv_slot_x", ":base_inv_slot_x", 25),
                    (store_add, ":item_inv_slot_y", ":base_inv_slot_y", 25),

                    (position_set_x, pos1, ":item_inv_slot_x"),
                    (position_set_y, pos1, ":item_inv_slot_y"),
                    (overlay_set_position, reg10, pos1),

                    # save id for reuse
                    (troop_set_slot, "trp_temp_array_a", ":item_eq", reg10),
                    (store_add, ":item_eq_id", ":item_eq", 10),
                    (troop_set_slot, "trp_temp_array_a", ":item_eq_id", reg1),
                # real items
                (try_end),
                (val_sub, ":base_inv_slot_y", 51),
            (try_end),
            # end loop equipments slots
        (try_end),

        # do an update if called from menu and reset init variable
        (try_begin),
            (eq, "$g_jrider_pres_called_from_menu", 1),
            (assign, "$g_jrider_pres_called_from_menu", 0),
        (try_end),
    ]),
    # end presentation load

    ## Mouse-over
    (ti_on_presentation_mouse_enter_leave,
      [
      (store_trigger_param_1, ":object"),
      (store_trigger_param_2, ":enter_leave"),

      (try_begin),
          (eq, "$g_character_presentation_type", 2),
          (try_begin),
              (eq, ":enter_leave", 0),
              (try_for_range, ":slot_no", 0, 9),
                  (troop_slot_eq, "trp_temp_array_a", ":slot_no", ":object"),
                  (store_add, ":slot_no_eq", ":slot_no", 10),
                  (troop_get_slot, ":item_no", "trp_temp_array_a", ":slot_no_eq"),

                  (set_fixed_point_multiplier, 1000),

                  (position_set_x,pos0,740),
                  (position_set_y,pos0,235),
                  (show_item_details, ":item_no", pos0, 100),
              (try_end),
          (else_try),
              (try_for_range, ":slot_no", 0, 9),
                (troop_slot_eq, "trp_temp_array_a", ":slot_no", ":object"),
                (close_item_details),
              (try_end),
          (try_end),
      (try_end),
    ]),
    # end mouseover

    ## Check for buttonpress
    (ti_on_presentation_event_state_change,
     [
        (store_trigger_param_1, ":object"), # object
        (store_trigger_param_2, ":value"),  # value

        (try_begin),
            # pressed  (Return to menu)
            (eq, ":object", "$g_jrider_character_report_Return_to_menu"),

            (try_begin),
                (neq, "$num_charinfo_candidates", 0),
                (overlay_set_text, "$g_jrider_character_information_text", "str_empty_string"),
                (overlay_set_alpha, "$g_jrider_last_checked_indicator", 0),
            (try_end),
            (presentation_set_duration, 0),

        (else_try),
            # Faction filter
            (eq, ":object", "$g_jrider_character_faction_filter"),
            (try_begin),
				#gekokujo 3.0 "all factions" is now index 21
                #(eq, ":value", 7),
                (eq, ":value", 21),
                (assign, "$g_jrider_faction_filter", -1),
            (else_try),
                (assign, "$g_jrider_faction_filter", ":value"),
            (try_end),

            # reset selected to first
            (assign, "$g_jrider_reset_selected_on_faction", 1000),

            # restart presentation to take filters into account
            (start_presentation, "prsnt_jrider_character_relation_report"),

        (else_try),
            (neq, ":object", "$g_jrider_character_information_text"),
            (neq, ":object", "$g_jrider_character_portrait"),
            (neq, ":object", "$g_jrider_character_relation_listbox"),
            #(neq, ":object", "$g_jrider_faction_coat_of_arms"),
            # clicked on list entry
            # get storage index + base storage index
            (store_add, ":storage_button_id", ":object", "$g_base_character_presentation_storage_index"),
            (troop_get_slot, ":character_number", "trp_temp_array_b", ":storage_button_id"),

            (overlay_set_alpha, "$g_jrider_last_checked_indicator", 0),
            (overlay_set_color, "$g_jrider_last_checked_indicator", 0xDDDDDD),

            # update last entry and check variables
            (assign, "$g_latest_character_relation_entry", ":character_number"),
            (assign, "$g_jrider_last_checked_indicator", ":object"),

            # color selected entry
            (overlay_set_color, "$g_jrider_last_checked_indicator", 0xFF6666FF),
            (overlay_set_alpha, "$g_jrider_last_checked_indicator", 0x44),

            # get troop information from storage to update text
            (val_add, ":character_number", "$g_base_character_presentation_storage_index"),
            (troop_get_slot, "$character_info_id", "trp_temp_array_c", ":character_number"),

            # restart presentation to update picture and text
            (start_presentation, "prsnt_jrider_character_relation_report"),
    (try_end),
     ] # + generic_ti_on_presentation_event_state_change
     ),
     # end event state change

    ## Event to process when running the presentation
    (ti_on_presentation_run,
     # generic_ti_on_presentation_run +
     [
        (try_begin),
      (this_or_next|key_clicked, key_escape),
      (key_clicked, key_right_mouse_button),
      (presentation_set_duration, 0),
      (jump_to_menu, "mnu_reports"),
        (try_end),

        ]),
     # end presentation run
     ]),
    ###################################
    # Character relation presentation end
# Jrider -


##diplomacy end+

#gekokujo 2.1 PBO
## Prebattle Orders Begin
 ("caba_order_display", prsntf_read_only,0,[
      (ti_on_presentation_load,
       [(set_fixed_point_multiplier, 1000),
		(try_for_range, ":i", 0, 9),
			(store_add, ":slot", ":i", slot_party_cabadrin_order_d0),
			(party_set_slot, "p_main_party_backup", ":slot", -1),
		(try_end),
		
		(assign, ":y_position", 560),
		(try_begin), #Figure out which orders to display, set strings
			(party_slot_eq, "p_main_party", slot_party_gk_order, 0),
			(str_store_string, s1, "@F5 - Weapon orders"),
            (str_store_string, s2, "@F6 - Shield orders"),
			(str_store_string, s3, "@F7 - Skirmish orders"),
			
            (assign, ":num_orders", 3),
			(assign, ":y_position", 470),
		(else_try),
			(party_slot_eq, "p_main_party", slot_party_gk_order, gk_order_5),
			(str_store_string, s1, "@F5 - One Handers"),
			(str_store_string, s2, "@F6 - Two Handers"),
            (str_store_string, s3, "@F7 - Polearms"),
			(str_store_string, s4, "@F8 - Ranged"),
			(str_store_string, s5, "@F9 - Escape Menu"),

            (assign, ":num_orders", 5),
		(else_try),
			(party_slot_eq, "p_main_party", slot_party_gk_order, gk_order_6),
			(str_store_string, s1, "@F5 - Use Shields"),
			(str_store_string, s2, "@F6 - No Shields"),
			(str_store_string, s3, "@F7 - Free"),
			(str_store_string, s4, "@F9 - Escape Menu"),
			
            (assign, ":num_orders", 4),
		(else_try),
			(party_slot_eq, "p_main_party", slot_party_gk_order, k_order_7),
			(str_store_string, s1, "@F5 - Skirmish"),
			(str_store_string, s2, "@F6 - Melee"),
			(str_store_string, s3, "@F9 - Escape Menu"),
			
            (assign, ":num_orders", 3),
		(try_end),
		(party_get_slot, ":starting_order", "p_main_party", slot_party_gk_order),
		(party_set_slot, "p_main_party_backup", slot_party_gk_order, ":starting_order"),

		(try_for_range, ":i", 0, ":num_orders"),
			(try_begin),
			    (eq, ":i", 0),
				(str_store_string_reg, s0, s1),
			(else_try),
				(eq, ":i", 1),
				(str_store_string_reg, s0, s2),
			(else_try),
				(eq, ":i", 2),
				(str_store_string_reg, s0, s3),
			(else_try),
				(eq, ":i", 3),
				(str_store_string_reg, s0, s4),
			(else_try),
				(eq, ":i", 4),
				(str_store_string_reg, s0, s5),
			(try_end),
		    (create_text_overlay, ":overlay", s0),
			(overlay_set_color, ":overlay", 0xFFFFFF),
			(position_set_x, pos1, 1000),
			(position_set_y, pos1, 1000),
			(overlay_set_size, ":overlay", pos1),
			(position_set_x, pos1, 0),
			(position_set_y, pos1, ":y_position"),
			(overlay_set_position, ":overlay", pos1),
			
			(store_add, ":slot", ":i", slot_party_cabadrin_order_d0),
			(party_set_slot, "p_main_party_backup", ":slot", ":overlay"),
			
			(val_sub, ":y_position", 30),
		(try_end),
		(store_mul, ":add_back", 30, ":num_orders"),
		(val_add, ":y_position", ":add_back"),
		(try_for_range, ":i", 0, ":num_orders"),
		    (create_mesh_overlay, ":overlay", "mesh_white_plane"),
			(overlay_set_color, ":overlay", 0),
			(overlay_set_alpha, ":overlay", 0x60),
			(position_set_x, pos1, 13900),
			(position_set_y, pos1, 1300),
			(overlay_set_size, ":overlay", pos1),
						
			(position_set_x, pos1, 1),
			(position_set_y, pos1, ":y_position"),
			(overlay_set_position, ":overlay", pos1),
			
			(val_sub, ":y_position", 30),
		(try_end),
		(store_mul, ":add_back", 30, ":num_orders"),
		(val_add, ":y_position", ":add_back"),
		(val_sub, ":y_position", 2),
		# (try_for_range, ":i", 0, ":num_orders"),
		    # (create_mesh_overlay, ":overlay", "mesh_order_frame"),
			##(overlay_set_color, ":overlay", 0xFFCC00),
			##(overlay_set_alpha, ":overlay", 0x60),
			# (position_set_x, pos1, 712),
			# (position_set_y, pos1, 780),
			# (overlay_set_size, ":overlay", pos1),
			
			# (position_set_x, pos1, 0),
			# (position_set_y, pos1, ":y_position"),
			# (overlay_set_position, ":overlay", pos1),
			
			# (val_sub, ":y_position", 30),
		# (try_end),
		
		(try_begin),
			(neg|party_slot_eq, "p_main_party", slot_party_gk_order, 0),
			(create_mesh_overlay, ":overlay", "mesh_white_plane"),
			(overlay_set_color, ":overlay", 0),
			(overlay_set_alpha, ":overlay", 0x10),
			(position_set_x, pos1, 14000),
			(position_set_y, pos1, 4500),
			(overlay_set_size, ":overlay", pos1),
			
			(position_set_x, pos1, 0),
			(position_set_y, pos1, 498),
			(overlay_set_position, ":overlay", pos1),
		(try_end),    

		(presentation_set_duration, 999999),
	   ]),
	(ti_on_presentation_run,
       [(store_trigger_param_1, ":cur_time"),
        (gt, ":cur_time", 250), #0.25 Second after Pres. Start
        (try_begin),
          (this_or_next|game_key_clicked, gk_group0_hear),
          (this_or_next|game_key_clicked, gk_group1_hear),
          (this_or_next|game_key_clicked, gk_group2_hear),
          (this_or_next|game_key_clicked, gk_group3_hear),
          (this_or_next|game_key_clicked, gk_group4_hear),
          (this_or_next|game_key_clicked, gk_group5_hear),
          (this_or_next|game_key_clicked, gk_group6_hear),
          (this_or_next|game_key_clicked, gk_group7_hear),
          (this_or_next|game_key_clicked, gk_group8_hear),
          (this_or_next|game_key_clicked, gk_everyone_hear),
          (game_key_clicked, gk_reverse_order_group),
		  (presentation_set_duration, 0),
        (try_end),
        (try_begin),
          (this_or_next|game_key_clicked, gk_order_1),
          (this_or_next|game_key_clicked, gk_order_2),
          (this_or_next|game_key_clicked, gk_order_3), #Order Keys not used by Expanded Orders
		  #(this_or_next|game_key_clicked, gk_order_4),
		  (game_key_clicked, gk_view_orders),
		  (presentation_set_duration, 0),
        (try_end),
		(try_begin),
			(key_clicked, key_escape),
			(omit_key_once, key_escape),
		    (presentation_set_duration, 0),
		(try_end),
		(try_begin),
			(assign, ":key", -1),
		    (try_begin),
 			    (game_key_clicked, gk_order_5),
			    (assign, ":key", 5),
		    (else_try),
      			(game_key_clicked, gk_order_6),
		    	(assign, ":key", 6),
			(else_try),
			    (key_clicked, k_order_7),
				(assign, ":key", 7),
		    (else_try),
			    (key_clicked, k_order_8),
				(assign, ":key", 8),
			(try_end),
			(neq, ":key", -1),
			(try_begin),
			    (party_slot_eq, "p_main_party_backup", slot_party_gk_order, 0),
		        (presentation_set_duration, 0),
			(else_try),
			    (try_begin),
					(party_slot_eq, "p_main_party_backup", slot_party_gk_order, gk_order_5),
					(assign, ":min_key", 5),
					(assign, ":max_key", 8),
				(else_try),
				    (party_slot_eq, "p_main_party_backup", slot_party_gk_order, gk_order_6),
					(assign, ":min_key", 5),
					(assign, ":max_key", 7),
				(else_try),
				    (party_slot_eq, "p_main_party_backup", slot_party_gk_order, k_order_7),
					(assign, ":min_key", 5),
					(assign, ":max_key", 6),
				(try_end),
				(store_sub, ":num_orders", ":max_key", ":min_key"),
				(val_add, ":num_orders", 1),
				(store_sub, ":key_pressed", ":key", ":min_key"),
				(is_between, ":key_pressed", 0, ":num_orders"),
				(val_add, ":num_orders", 1), #For the cancel box
				(try_for_range, ":i", 0, ":num_orders"),
					(store_add, ":slot", ":i", slot_party_cabadrin_order_d0),
				    (party_get_slot, ":overlay", "p_main_party_backup", ":slot"), 
					(try_begin),
					    (neq, ":i", ":key_pressed"),
				        (overlay_animate_to_alpha, ":overlay", 400, 0x00),
						(val_add, ":overlay", ":num_orders"),
				        (overlay_animate_to_alpha, ":overlay", 400, 0x00),
						# (val_add, ":overlay", ":num_orders"),
				        # (overlay_animate_to_alpha, ":overlay", 400, 0x00),
					(else_try),				
				        (overlay_animate_to_alpha, ":overlay", 1100, 0x00),
						(val_add, ":overlay", ":num_orders"),
						(overlay_animate_to_alpha, ":overlay", 1100, 0x00),
						# (val_add, ":overlay", ":num_orders"),
						# (overlay_animate_to_alpha, ":overlay", 1100, 0x00),
					(try_end),
				(try_end),			
				(presentation_set_duration, 200), #100
			(try_end),
        (try_end),
        ]),
	]),
]
