# -*- coding: UTF-8 -*-
# split feature file: game_menus - module
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from module_constants import *
from ym_gatling_shop import *

game_menus_encounter_battle = [
  
    
  (
    "simple_encounter",mnf_enable_hot_keys|mnf_scale_picture,
    "{s2} You have {reg10} troops fit for battle against their {reg11}.",
    "none",
    [      
        (assign, "$g_enemy_party", "$g_encountered_party"),
        (assign, "$g_ally_party", -1),
        (call_script, "script_encounter_calculate_fit"),
        
        #gekokujo 3.1 ninja rescue start
        #tally the number of ninjas to figure out rescue potential
        #do this before the battle because outcome is irrelevant to ninja score (dead ninjas did their work before the battle)
        (party_count_companions_of_type, "$gekokujo_rescue_score", "p_main_party", "trp_hired_agent"),
        
        (party_count_companions_of_type, ":additional_agents", "p_main_party", "trp_female_agent"),
        (val_add, "$gekokujo_rescue_score", ":additional_agents"),
        
        (party_count_companions_of_type, ":additional_agents", "p_main_party", "trp_hired_agent_experienced"),
        (val_mul, ":additional_agents", 2), #experienced agents are worth 2 points
        (val_add, "$gekokujo_rescue_score", ":additional_agents"),
        
        (party_count_companions_of_type, ":additional_agents", "p_main_party", "trp_female_agent_experienced"),
        (val_mul, ":additional_agents", 2), #experienced agents are worth 2 points
        (val_add, "$gekokujo_rescue_score", ":additional_agents"),
        #gekokujo 3.1 ninja rescue end
        
        (try_begin),
          (eq, "$new_encounter", 1),
          (assign, "$new_encounter", 0),
          (assign, "$g_encounter_is_in_village", 0),
          (assign, "$g_encounter_type", 0),
          (try_begin),
            (party_slot_eq, "$g_enemy_party", slot_party_ai_state, spai_raiding_around_center),        
            (party_get_slot, ":village_no", "$g_enemy_party", slot_party_ai_object),
        
            (store_distance_to_party_from_party, ":dist", ":village_no", "$g_enemy_party"),

            (try_begin),
              (lt, ":dist", raid_distance),
              (assign, "$g_encounter_is_in_village", ":village_no"),
              (assign, "$g_encounter_type", enctype_fighting_against_village_raid),
            (try_end),
          (try_end),
          (try_begin),
            (gt, "$g_player_raiding_village", 0),
            (assign, "$g_encounter_is_in_village", "$g_player_raiding_village"),
            (assign, "$g_encounter_type", enctype_catched_during_village_raid),
            (party_quick_attach_to_current_battle, "$g_encounter_is_in_village", 1), #attach as enemy
            (str_store_string, s1, "@Villagers"),
            (display_message, "str_s1_joined_battle_enemy"),
          (else_try),
            (eq, "$g_encounter_type", enctype_fighting_against_village_raid),
            (party_quick_attach_to_current_battle, "$g_encounter_is_in_village", 0), #attach as friend
            (str_store_string, s1, "@Villagers"),
            (display_message, "str_s1_joined_battle_friend"),
            # Let village party join battle at your side
          (try_end),
                    
          (call_script, "script_let_nearby_parties_join_current_battle", 0, 0),
          (call_script, "script_encounter_init_variables"),
          (assign, "$encountered_party_hostile", 0),
          (assign, "$encountered_party_friendly", 0),
          (try_begin),
            (gt, "$g_encountered_party_relation", 0),
            (assign, "$encountered_party_friendly", 1),
          (try_end),
          (try_begin),
            (lt, "$g_encountered_party_relation", 0),
            (assign, "$encountered_party_hostile", 1),
            (try_begin),
              (encountered_party_is_attacker),
              (assign, "$cant_leave_encounter", 1),
            (try_end),
          (try_end),
          (assign, "$talk_context", tc_party_encounter),
          (call_script, "script_setup_party_meeting", "$g_encountered_party"),
        (else_try), #second or more turn
#          (try_begin),
#            (call_script, "script_encounter_calculate_morale_change"),
#          (try_end),
          (try_begin),
            # We can leave battle only after some troops have been killed. 
            (eq, "$cant_leave_encounter", 1),
            (call_script, "script_party_count_members_with_full_health", "p_main_party_backup"),
            (assign, ":org_total_party_counts", reg0),
            (call_script, "script_party_count_members_with_full_health", "p_encountered_party_backup"),
            (val_add, ":org_total_party_counts", reg0),

            (call_script, "script_party_count_members_with_full_health", "p_main_party"),
            (assign, ":cur_total_party_counts", reg0),
            (call_script, "script_party_count_members_with_full_health", "p_collective_enemy"),
            (val_add, ":cur_total_party_counts", reg0),

            (store_sub, ":leave_encounter_limit", ":org_total_party_counts", 10),
            (lt, ":cur_total_party_counts", ":leave_encounter_limit"),
            (assign, "$cant_leave_encounter", 0),
          (try_end),
          (eq, "$g_leave_encounter",1),
          (change_screen_return),
        (try_end),

        #setup s2
        (try_begin),
          (party_is_active, "$g_encountered_party"),
          (str_store_party_name, s1,"$g_encountered_party"),
          (try_begin),
            (eq, "$g_encounter_type", 0),
            (str_store_string, s2,"@You have encountered {s1}."),
          (else_try),
            (eq, "$g_encounter_type", enctype_fighting_against_village_raid),
            (str_store_party_name, s3, "$g_encounter_is_in_village"),
            (str_store_string, s2,"@You have engaged {s1} while they were raiding {s3}."),
          (else_try),
            (eq, "$g_encounter_type", enctype_catched_during_village_raid),
            (str_store_party_name, s3, "$g_encounter_is_in_village"),
            (str_store_string, s2,"@You were caught by {s1} while your forces were raiding {s3}."),
          (try_end),
        (try_end),
        (try_begin),
          (call_script, "script_party_count_members_with_full_health", "p_collective_enemy"),
          (assign, ":num_enemy_regulars_remaining", reg0),
          (assign, ":enemy_finished", 0),
          (try_begin),
            (eq, "$g_battle_result", 1), #battle won
                        
            (this_or_next|le, ":num_enemy_regulars_remaining", 0), #battle won
            (le, ":num_enemy_regulars_remaining",  "$num_routed_enemies"), #replaced for above line because we do not want routed agents to spawn again in next turn of battle.

            (assign, ":enemy_finished",1),
          (else_try),
            (eq, "$g_engaged_enemy", 1), 
            
            (this_or_next|le, ":num_enemy_regulars_remaining", 0), 
            (le, "$g_enemy_fit_for_battle", "$num_routed_enemies"),  #replaced for above line because we do not want routed agents to spawn again in next turn of battle.
            
            (ge, "$g_friend_fit_for_battle",1),
            (assign, ":enemy_finished",1),
          (try_end),
                
          (this_or_next|eq, ":enemy_finished",1),
          (eq,"$g_enemy_surrenders",1),
          (assign, "$g_next_menu", -1),
          (jump_to_menu, "mnu_total_victory"),
        (else_try),       
          (call_script, "script_party_count_members_with_full_health", "p_main_party"),        
          (assign, ":num_our_regulars_remaining", reg0),
          (assign, ":friends_finished",0),
          (try_begin),
            (eq, "$g_battle_result", -1),

            #(eq, ":num_our_regulars_remaining", 0), #battle lost
            (le, ":num_our_regulars_remaining",  "$num_routed_us"), #replaced for above line because we do not want routed agents to spawn again in next turn of battle.

            (assign,  ":friends_finished", 1),
          (else_try),
            (eq, "$g_engaged_enemy", 1),
            (ge, "$g_enemy_fit_for_battle",1),
            (le, "$g_friend_fit_for_battle",0),
            (assign,  ":friends_finished",1),
          (try_end),
          
          (this_or_next|eq,  ":friends_finished",1),
          (eq,"$g_player_surrenders",1),
          (assign, "$g_next_menu", "mnu_captivity_start_wilderness"),
          (jump_to_menu, "mnu_total_defeat"),
        (try_end),

       
        (try_begin),
          (eq, "$g_encountered_party_template", "pt_looters"),
          (set_background_mesh, "mesh_gekokujo_pic_bandits_2"),
        (else_try),
          (eq, "$g_encountered_party_template", "pt_woku_pirates"),
          (set_background_mesh, "mesh_gekokujo_pic_bandits_2"),
        (else_try),
          (eq, "$g_encountered_party_template", "pt_seto_pirates"),
          (set_background_mesh, "mesh_gekokujo_pic_bandits_2"),
        (else_try),
          (eq, "$g_encountered_party_template", "pt_kanto_rebels"),
          (set_background_mesh, "mesh_gekokujo_pic_bandits_3"),
        (else_try),
          (eq, "$g_encountered_party_template", "pt_kinai_rebels"),
          (set_background_mesh, "mesh_gekokujo_pic_bandits_1"),
		#gekokujo 3.0 new bandit types start
        (else_try),
          (eq, "$g_encountered_party_template", "pt_monk_rebels"),
          (set_background_mesh, "mesh_gekokujo_pic_bandits_1"),
		#gekokujo 3.0 new bandit types end
        (else_try),
          (eq, "$g_encountered_party_template", "pt_shinano_rebels"),
          (set_background_mesh, "mesh_gekokujo_pic_bandits_2"),
        (else_try),
          (eq, "$g_encountered_party_template", "pt_deserters"),
          (set_background_mesh, "mesh_gekokujo_pic_bandits_3"),
        (else_try),
          (eq, "$g_encountered_party_template", "pt_kingdom_hero_party"),
		  (party_stack_get_troop_id, ":leader_troop", "$g_encountered_party", 0),
		  (ge, ":leader_troop", 1),
		  (troop_get_slot, ":leader_troop_faction", ":leader_troop", slot_troop_original_faction),
		  (try_begin),
			(eq, ":leader_troop_faction", fac_kingdom_1),
            (set_background_mesh, "mesh_gekokujo_pic_arms_uesugi"),
		  (else_try),
			(eq, ":leader_troop_faction", fac_kingdom_2),
            (set_background_mesh, "mesh_gekokujo_pic_arms_date"),
		  (else_try),
			(eq, ":leader_troop_faction", fac_kingdom_3),
            (set_background_mesh, "mesh_gekokujo_pic_arms_oda"),
		  (else_try),
			(eq, ":leader_troop_faction", fac_kingdom_4),
            (set_background_mesh, "mesh_gekokujo_pic_arms_mori"),
		  (else_try),
			(eq, ":leader_troop_faction", fac_kingdom_5),
            (set_background_mesh, "mesh_gekokujo_pic_arms_takeda"),
		  (else_try),
			(eq, ":leader_troop_faction", fac_kingdom_6),
            (set_background_mesh, "mesh_gekokujo_pic_arms_tokugawa"),
		  (else_try),
			(eq, ":leader_troop_faction", fac_kingdom_7),
            (set_background_mesh, "mesh_gekokujo_pic_arms_miyoshi"),
		  (else_try),
			(eq, ":leader_troop_faction", fac_kingdom_8),
            (set_background_mesh, "mesh_gekokujo_pic_arms_amako"),
		  (else_try),
			(eq, ":leader_troop_faction", fac_kingdom_9),
            (set_background_mesh, "mesh_gekokujo_pic_arms_otomo"),
		  (else_try),
			(eq, ":leader_troop_faction", fac_kingdom_10),
            (set_background_mesh, "mesh_gekokujo_pic_arms_nanbu"),
		  (else_try),
			(eq, ":leader_troop_faction", fac_kingdom_11),
            (set_background_mesh, "mesh_gekokujo_pic_arms_asakura"),
		  (else_try),
			(eq, ":leader_troop_faction", fac_kingdom_12),
            (set_background_mesh, "mesh_gekokujo_pic_arms_chosokabe"),
		  (else_try),
			(eq, ":leader_troop_faction", fac_kingdom_13),
            (set_background_mesh, "mesh_gekokujo_pic_arms_hojo"),
		  (else_try),
			(eq, ":leader_troop_faction", fac_kingdom_14),
            (set_background_mesh, "mesh_gekokujo_pic_arms_mogami"),
		  (else_try),
			(eq, ":leader_troop_faction", fac_kingdom_15),
            (set_background_mesh, "mesh_gekokujo_pic_arms_shimazu"),
		  (else_try),
			(eq, ":leader_troop_faction", fac_kingdom_16),
            (set_background_mesh, "mesh_gekokujo_pic_arms_ryuzoji"),
		  (else_try),
			(eq, ":leader_troop_faction", fac_kingdom_17),
            (set_background_mesh, "mesh_gekokujo_pic_arms_satake"),
		  (else_try),
			(eq, ":leader_troop_faction", fac_kingdom_18),
            (set_background_mesh, "mesh_gekokujo_pic_arms_satomi"),
		  (else_try),
			(eq, ":leader_troop_faction", fac_kingdom_19),
            (set_background_mesh, "mesh_gekokujo_pic_arms_ukita"),
		  (else_try),
			(eq, ":leader_troop_faction", fac_kingdom_20),
            (set_background_mesh, "mesh_gekokujo_pic_arms_ikko"),
          (else_try),
			(eq, ":leader_troop_faction", fac_kingdom_21),
            (set_background_mesh, "mesh_gekokujo_pic_arms_xb"),
          (else_try),
			(eq, ":leader_troop_faction", fac_kingdom_22),
            (set_background_mesh, "mesh_gekokujo_pic_arms_ss"),
          (else_try),
			(eq, ":leader_troop_faction", fac_kingdom_23),
            (set_background_mesh, "mesh_gekokujo_pic_arms_wz"),
          (else_try),
			(eq, ":leader_troop_faction", fac_kingdom_24),
            (set_background_mesh, "mesh_gekokujo_pic_arms_dedao"),
          (else_try),
			(eq, ":leader_troop_faction", fac_kingdom_25),
            (set_background_mesh, "mesh_gekokujo_pic_arms_zhuangnei"),
          (else_try),
			(eq, ":leader_troop_faction", fac_kingdom_26),
            (set_background_mesh, "mesh_gekokujo_pic_arms_jiubaotian"), 
          (else_try),
			(eq, ":leader_troop_faction", fac_kingdom_27),
            (set_background_mesh, "mesh_gekokujo_pic_arms_yangen"), 
          (else_try),
			(eq, ":leader_troop_faction", fac_kingdom_28),
            (set_background_mesh, "mesh_gekokujo_pic_arms_xinzhengfu"), 
          (else_try),
			(eq, ":leader_troop_faction", fac_dark_knights),
            (set_background_mesh, "mesh_gekokujo_pic_arms_rus"), 
		  (else_try),
            (set_background_mesh, "mesh_gekokujo_pic_arms_other"),
		  (try_end),
        (try_end),
    ],
    [
	
#gekokujo 2.1 PBO
## PreBattle Orders Begin
	  # ("encounter_attack_plan",
      # [
        # (eq, "$encountered_party_friendly", 0),
        # (neg|troop_is_wounded, "trp_player"),
		# (neq, "$g_encounter_type", enctype_fighting_against_village_raid),
		# (neq, "$g_encounter_type", enctype_catched_during_village_raid),
		# (party_get_skill_level, ":tactics", "p_main_party", skl_tactics),
		# (ge, ":tactics", 2),
      # ],
      # "Plan your battle with the enemy.",
      # [
  		# (assign, "$g_next_menu", "mnu_simple_encounter"),		
		# (start_presentation, "prsnt_prebattle_orders"),
      # ]),
	  
	  ("encounter_attack_do_plan",
      [
         (party_slot_eq, "p_main_party", slot_party_prebattle_plan, 1),
      ],
      "Enough planning. To battle!",
      [
	    (party_set_slot, "p_main_party", slot_party_prebattle_plan, 0),
	  
        (assign, "$g_battle_result", 0),
        (assign, "$g_engaged_enemy", 1),
        
        (party_get_template_id, ":encountered_party_template", "$g_encountered_party"),		
        (try_begin),
		  (eq, ":encountered_party_template", "pt_village_farmers"),
		  (unlock_achievement, ACHIEVEMENT_HELP_HELP_IM_BEING_REPRESSED),
		(try_end),     
     
        (call_script, "script_calculate_renown_value"),
        (call_script, "script_calculate_battle_advantage"),
        (set_battle_advantage, reg0),
        (set_party_battle_mode),
		
        (set_jump_mission,"mt_lead_charge"),
		
        #gekokujo 3.0 disable horses in sea battles start
        (party_get_current_terrain, ":terrain_type", "p_main_party"),
        (try_begin),
          (eq, ":terrain_type", rt_bridge),
          (mission_tpl_entry_set_override_flags, "mt_lead_charge", 0, af_override_horse),
          (mission_tpl_entry_set_override_flags, "mt_lead_charge", 1, af_override_horse),
          (mission_tpl_entry_set_override_flags, "mt_lead_charge", 2, af_override_horse),
          (mission_tpl_entry_set_override_flags, "mt_lead_charge", 3, af_override_horse),
        (try_end),
        #gekokujo 3.0 disable horses in sea battles end
		
        (call_script, "script_setup_random_scene"),
        (assign, "$g_next_menu", "mnu_simple_encounter"),
        (jump_to_menu, "mnu_battle_debrief"),
		(change_screen_mission),
      ]),
	  
	  ("encounter_attack_clear_plan",
      [
         (party_slot_eq, "p_main_party", slot_party_prebattle_plan, 1),
      ],
      "Re-assess the situation.",
      [
        (party_set_slot, "p_main_party", slot_party_prebattle_plan, 0),
		(party_set_slot, "p_main_party", slot_party_prebattle_num_orders, 0),
		
        (jump_to_menu, "mnu_simple_encounter"),
      ]),
	  
	  # ("encounter_attack_hold",
      # [
        # (eq, "$encountered_party_friendly", 0),
        # (neg|troop_is_wounded, "trp_player"),
		# (neq, "$g_encounter_type", enctype_fighting_against_village_raid),
		# (neq, "$g_encounter_type", enctype_catched_during_village_raid),
		# (party_get_skill_level, ":tactics", "p_main_party", skl_tactics),
		# (ge, ":tactics", 1),
      # ],
      # "Take the field.",
      # [
        # (assign, "$g_battle_result", 0),
        # (assign, "$g_engaged_enemy", 1),
        
        # (party_get_template_id, ":encountered_party_template", "$g_encountered_party"),		
        # (try_begin),
		  # (eq, ":encountered_party_template", "pt_village_farmers"),
		  # (unlock_achievement, ACHIEVEMENT_HELP_HELP_IM_BEING_REPRESSED),
		# (try_end),     
         
        # (party_set_slot, "p_main_party", slot_party_prebattle_num_orders, 1),
	    # (party_get_slot, ":first_order", "p_main_party", slot_party_prebattle_order_array_begin),
		# (try_begin),
		    # (gt, ":first_order", 0),
			# (party_set_slot, "p_main_party_backup", slot_party_prebattle_order_array_begin, ":first_order"),
        # (try_end),
		# (party_set_slot, "p_main_party", slot_party_prebattle_order_array_begin, 910),		
        
        # (call_script, "script_calculate_renown_value"),
        # (call_script, "script_calculate_battle_advantage"),
        # (set_battle_advantage, reg0),
        # (set_party_battle_mode),
		
        # (set_jump_mission,"mt_lead_charge"),
		
        # #gekokujo 3.0 disable horses in sea battles start
        # (party_get_current_terrain, ":terrain_type", "p_main_party"),
        # (try_begin),
          # (eq, ":terrain_type", rt_bridge),
          # (mission_tpl_entry_set_override_flags, "mt_lead_charge", 0, af_override_horse),
          # (mission_tpl_entry_set_override_flags, "mt_lead_charge", 1, af_override_horse),
          # (mission_tpl_entry_set_override_flags, "mt_lead_charge", 2, af_override_horse),
          # (mission_tpl_entry_set_override_flags, "mt_lead_charge", 3, af_override_horse),
        # (try_end),
        # #gekokujo 3.0 disable horses in sea battles end
		
        # (call_script, "script_setup_random_scene"),
        # (assign, "$g_next_menu", "mnu_simple_encounter"),
        # (jump_to_menu, "mnu_battle_debrief"),
        # (change_screen_mission),
      # ]),
	  
	  # ("encounter_attack_follow",
      # [
        # (eq, "$encountered_party_friendly", 0),
        # (neg|troop_is_wounded, "trp_player"),
		# (neq, "$g_encounter_type", enctype_fighting_against_village_raid),
		# (neq, "$g_encounter_type", enctype_catched_during_village_raid),
		# (party_get_skill_level, ":tactics", "p_main_party", skl_tactics),
		# (ge, ":tactics", 1),
      # ],
      # "Lead your troops.",
      # [
        # (assign, "$g_battle_result", 0),
        # (assign, "$g_engaged_enemy", 1),
        
        # (party_get_template_id, ":encountered_party_template", "$g_encountered_party"),		
        # (try_begin),
		  # (eq, ":encountered_party_template", "pt_village_farmers"),
		  # (unlock_achievement, ACHIEVEMENT_HELP_HELP_IM_BEING_REPRESSED),
		# (try_end),     
         
        # (party_set_slot, "p_main_party", slot_party_prebattle_num_orders, 1),
		# (party_get_slot, ":first_order", "p_main_party", slot_party_prebattle_order_array_begin),
		# (try_begin),
		    # (gt, ":first_order", 0),
			# (party_set_slot, "p_main_party_backup", slot_party_prebattle_order_array_begin, ":first_order"),
        # (try_end),
        # (party_set_slot, "p_main_party", slot_party_prebattle_order_array_begin, 911),		
        
        # (call_script, "script_calculate_renown_value"),
        # (call_script, "script_calculate_battle_advantage"),
        # (set_battle_advantage, reg0),
        # (set_party_battle_mode),
		
        # (set_jump_mission,"mt_lead_charge"),
		
        # #gekokujo 3.0 disable horses in sea battles start
        # (party_get_current_terrain, ":terrain_type", "p_main_party"),
        # (try_begin),
          # (eq, ":terrain_type", rt_bridge),
          # (mission_tpl_entry_set_override_flags, "mt_lead_charge", 0, af_override_horse),
          # (mission_tpl_entry_set_override_flags, "mt_lead_charge", 1, af_override_horse),
          # (mission_tpl_entry_set_override_flags, "mt_lead_charge", 2, af_override_horse),
          # (mission_tpl_entry_set_override_flags, "mt_lead_charge", 3, af_override_horse),
        # (try_end),
        # #gekokujo 3.0 disable horses in sea battles end
		
        # (call_script, "script_setup_random_scene"),
        # (assign, "$g_next_menu", "mnu_simple_encounter"),
        # (jump_to_menu, "mnu_battle_debrief"),
        # (change_screen_mission),
      # ]),
## PreBattle Orders End
    ("change_battlefield_size",
        [
          (eq, "$g_encounter_type", 0),
          (eq, "$encountered_party_friendly", 0),
          (neg|troop_is_wounded, "trp_player"),
          (store_add, ":dest_string", "str_battlefield_small", "$g_random_scene_size"),
          (str_store_string, s3, ":dest_string"),
         ],
        "改 变 你 的 战 场 规 模 ，他 会 是 一 个({s3}).",
        [
        (val_add, "$g_random_scene_size", 1),
        (val_mod, "$g_random_scene_size", 3),
        (jump_to_menu, "mnu_simple_encounter"),
        ]),

      ("encounter_attack",
      [
        (eq, "$encountered_party_friendly", 0),
        (neg|troop_is_wounded, "trp_player"),
	    #gekokujo 2.1 PBO
		## PreBattle Orders Begin
		(party_slot_eq, "p_main_party", slot_party_prebattle_plan, 0),
		## PreBattle Orders End
      ],
      "Charge the enemy.",
      [
        (assign, "$g_battle_result", 0),
        (assign, "$g_engaged_enemy", 1),
        
        (party_get_template_id, ":encountered_party_template", "$g_encountered_party"),		
        (try_begin),
		  (eq, ":encountered_party_template", "pt_village_farmers"),
		  (unlock_achievement, ACHIEVEMENT_HELP_HELP_IM_BEING_REPRESSED),
		(try_end),          
        
        (call_script, "script_calculate_renown_value"),
		##diplomacy start+
		(try_begin),
			#Call this to properly set cached values for strength
			(eq, "$g_dplmc_terrain_advantage", DPLMC_TERRAIN_ADVANTAGE_ENABLE),
			(assign, ":terrain_code", dplmc_terrain_code_none),#defined in header_terrain_types.py
			(try_begin),
				(this_or_next|eq, "$g_encounter_type", enctype_fighting_against_village_raid),
					(eq, "$g_encounter_type", enctype_catched_during_village_raid),
				(assign, ":terrain_code", dplmc_terrain_code_village),#defined in header_terrain_types.py
			(else_try),
				(encountered_party_is_attacker),
				(call_script, "script_dplmc_get_terrain_code_for_battle", "$g_encountered_party", "p_main_party"),
				(assign, ":terrain_code", reg0),
			(else_try),
				(call_script, "script_dplmc_get_terrain_code_for_battle", "p_main_party", "$g_encountered_party"),
				(assign, ":terrain_code", reg0),
			(try_end),
			(neq, ":terrain_code", dplmc_terrain_code_none),
			(call_script, "script_dplmc_party_calculate_strength_in_terrain", "p_main_party", ":terrain_code", 0, 1),
			(call_script, "script_dplmc_party_calculate_strength_in_terrain", "$g_encountered_party", ":terrain_code", 0, 1),
		(try_end),
		##diplomacy end+
        (call_script, "script_calculate_battle_advantage"),
        (set_battle_advantage, reg0),
        (set_party_battle_mode),
        (try_begin),
          (eq, "$g_encounter_type", enctype_fighting_against_village_raid),
          (assign, "$g_village_raid_evil", 0),
          (set_jump_mission,"mt_village_raid"),
          (party_get_slot, ":scene_to_use", "$g_encounter_is_in_village", slot_castle_exterior),
          (jump_to_scene, ":scene_to_use"),
        (else_try),
          (eq, "$g_encounter_type", enctype_catched_during_village_raid),
          (assign, "$g_village_raid_evil", 0),
          (set_jump_mission,"mt_village_raid"),
          (party_get_slot, ":scene_to_use", "$g_encounter_is_in_village", slot_castle_exterior),
          (jump_to_scene, ":scene_to_use"),
        (else_try),
          (set_jump_mission,"mt_lead_charge"),
		
          #gekokujo 3.0 disable horses in sea battles start
          (party_get_current_terrain, ":terrain_type", "p_main_party"),
          (try_begin),
            (eq, ":terrain_type", rt_bridge),
            (mission_tpl_entry_set_override_flags, "mt_lead_charge", 0, af_override_horse),
            (mission_tpl_entry_set_override_flags, "mt_lead_charge", 1, af_override_horse),
            (mission_tpl_entry_set_override_flags, "mt_lead_charge", 2, af_override_horse),
            (mission_tpl_entry_set_override_flags, "mt_lead_charge", 3, af_override_horse),
          (try_end),
          #gekokujo 3.0 disable horses in sea battles end
		
          (call_script, "script_setup_random_scene"),
        (try_end),
        (assign, "$g_next_menu", "mnu_simple_encounter"),
        (jump_to_menu, "mnu_battle_debrief"),
        (change_screen_mission),
      ]),
      
      ("encounter_order_attack",
      [
        (eq, "$encountered_party_friendly", 0),
        (call_script, "script_party_count_members_with_full_health", "p_main_party"),(ge, reg0, 4),
	    #gekokujo 2.1 PBO
		## PreBattle Orders Begin
		(party_slot_eq, "p_main_party", slot_party_prebattle_plan, 0),
		## PreBattle Orders End
      ],
      "Order your troops to attack without you.",
      [
        (jump_to_menu, "mnu_order_attack_begin"),
        #(simulate_battle,3),
      ]),
      
      ("encounter_leave",[
          (eq,"$cant_leave_encounter", 0),
	      #gekokujo 2.1 PBO
		  ## PreBattle Orders Begin
		  (party_slot_eq, "p_main_party", slot_party_prebattle_plan, 0),
		  ## PreBattle Orders End
          ],"Leave.",[

###NPC companion changes begin
              (try_begin),
                  (eq, "$encountered_party_friendly", 0),
                  (encountered_party_is_attacker),
                  (call_script, "script_objectionable_action", tmt_aristocratic, "str_flee_battle"),
              (try_end),
###NPC companion changes end
#Troop commentary changes begin
              (try_begin),
                  (eq, "$encountered_party_friendly", 0),
#                  (encountered_party_is_attacker),
                  (party_get_num_companion_stacks, ":num_stacks", "p_encountered_party_backup"),
                  (try_for_range, ":stack_no", 0, ":num_stacks"),
                    (party_stack_get_troop_id,   ":stack_troop","p_encountered_party_backup",":stack_no"),
                    (is_between, ":stack_troop", active_npcs_begin, active_npcs_end),
					(troop_slot_eq, ":stack_troop", slot_troop_occupation, slto_kingdom_hero),
                    (store_troop_faction, ":victorious_faction", ":stack_troop"),
#					(store_relation, ":relation_with_stack_troop", ":victorious_faction", "fac_player_faction"),
#					(lt, ":relation_with_stack_troop", 0),
                    (call_script, "script_add_log_entry", logent_player_retreated_from_lord, "trp_player",  -1, ":stack_troop", ":victorious_faction"),
                  (try_end),
              (try_end),
#Troop commentary changes end
          (leave_encounter),(change_screen_return),
          ##diplomacy begin
          (assign, "$g_move_fast", 1),
          ##diplomacy end
          ]),
      ("encounter_retreat",[
	     #gekokujo 2.1 PBO
		 ## PreBattle Orders Begin
		 (party_slot_eq, "p_main_party", slot_party_prebattle_plan, 0),
		 ## PreBattle Orders End
         (eq,"$cant_leave_encounter", 1),
         (call_script, "script_get_max_skill_of_player_party", "skl_tactics"),
         (assign, ":max_skill", reg0),
         (val_add, ":max_skill", 4),

         (call_script, "script_party_count_members_with_full_health", "p_collective_enemy", 0),
         (assign, ":enemy_party_strength", reg0),
         (val_div, ":enemy_party_strength", 2),

         (val_div, ":enemy_party_strength", ":max_skill"),
         (val_max, ":enemy_party_strength", 1),

         (call_script, "script_party_count_fit_regulars", "p_main_party"),
         (assign, ":player_count", reg0),
         (ge, ":player_count", ":enemy_party_strength"),
         ],"Pull back, leaving some soldiers behind to cover your retreat.",[(jump_to_menu, "mnu_encounter_retreat_confirm"),]),
         
      ("encounter_surrender",[
	     #gekokujo 2.1 PBO
		 ## PreBattle Orders Begin
		 (party_slot_eq, "p_main_party", slot_party_prebattle_plan, 0),
		 ## PreBattle Orders End
         (eq,"$cant_leave_encounter", 1),
          ],"Surrender.",[(assign,"$g_player_surrenders",1)]),
    ]
  ),
  (
    "encounter_retreat_confirm",0,
    "As the party member with the highest tactics skill,\
 ({reg2}), {reg3?you devise:{s3} devises} a plan that will allow you and your men to escape with your lives,\
 but you'll have to leave {reg4} soldiers behind to stop the enemy from giving chase.",
    "none",
    [(call_script, "script_get_max_skill_of_player_party", "skl_tactics"),
     (assign, ":max_skill", reg0),
     (assign, ":max_skill_owner", reg1),
     (assign, reg2, ":max_skill"),
     (val_add, ":max_skill", 4),

     (call_script, "script_party_count_members_with_full_health", "p_collective_enemy", 0),
     (assign, ":enemy_party_strength", reg0),
     (val_div, ":enemy_party_strength", 2),

     (store_div, reg4, ":enemy_party_strength", ":max_skill"),
     (val_max, reg4, 1),
     
     (try_begin),
       (eq, ":max_skill_owner", "trp_player"),
       (assign, reg3, 1),
     (else_try),
       (assign, reg3, 0),
       (str_store_troop_name, s3, ":max_skill_owner"),
     (try_end),
     ],
    [
      ("leave_behind",[],"Go on. The sacrifice of these men will save the rest.",[
          (assign, ":num_casualties", reg4),
          (try_for_range, ":unused", 0, ":num_casualties"),
            (call_script, "script_cf_party_remove_random_regular_troop", "p_main_party"),
            (assign, ":lost_troop", reg0),
            (store_random_in_range, ":random_no", 0, 100),
            (ge, ":random_no", 30),
            (party_add_prisoners, "$g_encountered_party", ":lost_troop", 1),
           (try_end),
           (call_script, "script_change_player_party_morale", -20),
           (jump_to_menu, "mnu_encounter_retreat"),
          ]),
      ("dont_leave_behind",[],"No. We leave no one behind.",[(jump_to_menu, "mnu_simple_encounter"),]),
    ]
  ),
  (
    "encounter_retreat",0,
    "You tell {reg4} of your troops to hold the enemy while you retreat with the rest of your party.",
    "none",
    [
     ],
    [
      ("continue",[],"Continue...",[
###Troop commentary changes begin
          (call_script, "script_objectionable_action", tmt_aristocratic, "str_flee_battle"),
          (party_get_num_companion_stacks, ":num_stacks", "p_encountered_party_backup"),
          (try_for_range, ":stack_no", 0, ":num_stacks"),
              (party_stack_get_troop_id,   ":stack_troop","p_encountered_party_backup",":stack_no"),
              (is_between, ":stack_troop", active_npcs_begin, active_npcs_end),
              (troop_slot_eq, ":stack_troop", slot_troop_occupation, slto_kingdom_hero),

              (store_troop_faction, ":victorious_faction", ":stack_troop"),
              (call_script, "script_add_log_entry", logent_player_retreated_from_lord_cowardly, "trp_player",  -1, ":stack_troop", ":victorious_faction"),
          (try_end),
###Troop commentary changes end
          (party_ignore_player, "$g_encountered_party", 1),
          (leave_encounter),(change_screen_return)]),
    ]
  ),
  (
    "order_attack_begin",0,
    "Your troops prepare to attack the enemy.",
    "none",
    [],
    [
      ("order_attack_begin",[],"Order the attack to begin.", 
      [
        (party_get_template_id, ":encountered_party_template", "$g_encountered_party"),		
        (try_begin),
		  (eq, ":encountered_party_template", "pt_village_farmers"),
		  (unlock_achievement, ACHIEVEMENT_HELP_HELP_IM_BEING_REPRESSED),
		(try_end),                
        
        (assign, "$g_engaged_enemy", 1),
        (jump_to_menu,"mnu_order_attack_2"),
      ]),
      ("call_back",[],"Call them back.",[(jump_to_menu,"mnu_simple_encounter")]),
    ]
  ),
  (
    "order_attack_2",mnf_disable_all_keys,
    "{s4}^^Your casualties: {s8}^^Enemy casualties: {s9}",
    "none",
    [
      (set_background_mesh, "mesh_pic_charge"),

      (call_script, "script_party_calculate_strength", "p_main_party", 1), #exclude player
      (assign, ":player_party_strength", reg0),

      (call_script, "script_party_calculate_strength", "p_collective_enemy", 0),
      (assign, ":enemy_party_strength", reg0),
      
      (party_collect_attachments_to_party, "p_main_party", "p_collective_ally"),
      (call_script, "script_party_calculate_strength", "p_collective_ally", 1), #exclude player
      (assign, ":total_player_and_followers_strength", reg0),
                                    
      (try_begin),
        (le, ":total_player_and_followers_strength", ":enemy_party_strength"),
        (assign, ":minimum_power", ":total_player_and_followers_strength"),
      (else_try),
        (assign, ":minimum_power", ":enemy_party_strength"),
      (try_end),
      
      (try_begin),
        (le, ":minimum_power", 25),
        (assign, ":division_constant", 1),
      (else_try),
        (le, ":minimum_power", 50),
        (assign, ":division_constant", 2),
      (else_try),
        (le, ":minimum_power", 75),
        (assign, ":division_constant", 3),
      (else_try),
        (le, ":minimum_power", 125),
        (assign, ":division_constant", 4),
      (else_try),
        (le, ":minimum_power", 200),
        (assign, ":division_constant", 5),
      (else_try),
        (le, ":minimum_power", 400),
        (assign, ":division_constant", 6),
      (else_try),
        (le, ":minimum_power", 800),
        (assign, ":division_constant", 7),
      (else_try),
        (le, ":minimum_power", 1600),
        (assign, ":division_constant", 8),
      (else_try),
        (le, ":minimum_power", 3200),
        (assign, ":division_constant", 9),
      (else_try),
        (le, ":minimum_power", 6400),
        (assign, ":division_constant", 10),
      (else_try),
        (le, ":minimum_power", 12800),
        (assign, ":division_constant", 11),
      (else_try),
        (le, ":minimum_power", 25600),
        (assign, ":division_constant", 12),
      (else_try),
        (le, ":minimum_power", 51200),
        (assign, ":division_constant", 13),
      (else_try),
        (le, ":minimum_power", 102400),
        (assign, ":division_constant", 14),
      (else_try),  
        (assign, ":division_constant", 15),
      (try_end),  
                                                                              
      (val_div, ":player_party_strength", ":division_constant"), #1.126, ":division_constant" was 5 before
      (val_max, ":player_party_strength", 1), #1.126
      (val_div, ":enemy_party_strength", ":division_constant"), #1.126, ":division_constant" was 5 before
      (val_max, ":enemy_party_strength", 1), #1.126
      (val_div, ":total_player_and_followers_strength", ":division_constant"), #1.126, ":division_constant" was 5 before
      (val_max, ":total_player_and_followers_strength", 1), #1.126

      (store_mul, "$g_strength_contribution_of_player", ":player_party_strength", 100),
      (val_div, "$g_strength_contribution_of_player", ":total_player_and_followers_strength"),

      (inflict_casualties_to_party_group, "p_main_party", ":enemy_party_strength", "p_temp_casualties"),
      (call_script, "script_print_casualties_to_s0", "p_temp_casualties", 0),
      (str_store_string_reg, s8, s0),

      (try_begin),
        (ge, "$g_ally_party", 0),
        (inflict_casualties_to_party_group, "$g_ally_party", ":enemy_party_strength", "p_temp_casualties"),
        (str_store_string_reg, s8, s0),
      (try_end),  
                                  
      (inflict_casualties_to_party_group, "$g_encountered_party", ":total_player_and_followers_strength", "p_temp_casualties"),

      #ozan begin
      (party_get_num_companion_stacks, ":num_stacks", "p_temp_casualties"), 
      (try_for_range, ":stack_no", 0, ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop", "p_temp_casualties", ":stack_no"), 
        (try_begin),
          (party_stack_get_size, ":stack_size", "p_temp_casualties", ":stack_no"),
          (gt, ":stack_size", 0),
          (party_add_members, "p_total_enemy_casualties", ":stack_troop", ":stack_size"), #addition_to_p_total_enemy_casualties
          (party_stack_get_num_wounded, ":stack_wounded_size", "p_temp_casualties", ":stack_no"),                                    
          (gt, ":stack_wounded_size", 0),
          (party_wound_members, "p_total_enemy_casualties", ":stack_troop", ":stack_wounded_size"),
        (try_end),
      (try_end),
      #ozan end
                                                                        
      (call_script, "script_print_casualties_to_s0", "p_temp_casualties", 0),
      (str_store_string_reg, s9, s0),

      (party_collect_attachments_to_party, "$g_encountered_party", "p_collective_enemy"),
      (assign, "$no_soldiers_left", 0),
      (try_begin),
        (call_script, "script_party_count_members_with_full_health", "p_main_party"),
        (assign, ":num_our_regulars_remaining", reg0),
        (store_add, ":num_routed_us_plus_one", "$num_routed_us", 1),
        (le, ":num_our_regulars_remaining", ":num_routed_us_plus_one"), #replaced for above line because we do not want routed agents to spawn again in next turn of battle.
        (assign, "$no_soldiers_left", 1),
        (str_store_string, s4, "str_order_attack_failure"),
      (else_try),
        (call_script, "script_party_count_members_with_full_health", "p_collective_enemy"),
        (assign, ":num_enemy_regulars_remaining", reg0),
        (this_or_next|le, ":num_enemy_regulars_remaining", 0),
        (le, ":num_enemy_regulars_remaining", "$num_routed_enemies"), #replaced for above line because we do not want routed agents to spawn again in next turn of battle.
        (assign, ":continue", 0),
        (party_get_num_companion_stacks, ":party_num_stacks", "p_collective_enemy"),
        (try_begin),
          (eq, ":party_num_stacks", 0),
          (assign, ":continue", 1),
        (else_try),
          (party_stack_get_troop_id, ":party_leader", "p_collective_enemy", 0),
          (try_begin),
            (neg|troop_is_hero, ":party_leader"),
            (assign, ":continue", 1),
          (else_try),
            (troop_is_wounded, ":party_leader"),
            (assign, ":continue", 1),
          (try_end),
        (try_end),
        (eq, ":continue", 1),
        (assign, "$g_battle_result", 1),
        (assign, "$no_soldiers_left", 1),
        (str_store_string, s4, "str_order_attack_success"),
      (else_try),
      (str_store_string, s4, "str_order_attack_continue"),
    (try_end),
    ],
    [
      ("order_attack_continue",[(eq, "$no_soldiers_left", 0)],"Order your soldiers to continue the attack.",[
          (jump_to_menu,"mnu_order_attack_2"),
          ]),
      ("order_retreat",[(eq, "$no_soldiers_left", 0)],"Call your soldiers back.",[
          (jump_to_menu,"mnu_simple_encounter"),
          ]),
      ("continue",[(eq, "$no_soldiers_left", 1)],"Continue...",[
          (jump_to_menu,"mnu_simple_encounter"),
          ]),
    ]
  ),
  (
    "battle_debrief",mnf_scale_picture|mnf_disable_all_keys,
    "{s11}^^Your Casualties:{s8}{s10}^^Enemy Casualties:{s9}",
    "none",
    [
     (try_begin),
       (eq, "$g_battle_result", 1),
       (call_script, "script_change_troop_renown", "trp_player", "$battle_renown_value"),

       (try_begin),  
         (ge, "$g_encountered_party", 0),
         (party_is_active, "$g_encountered_party"),
         (party_get_template_id, ":encountered_party_template", "$g_encountered_party"),
         (eq, ":encountered_party_template", "pt_kingdom_caravan_party"),                  
         
         (get_achievement_stat, ":number_of_village_raids", ACHIEVEMENT_THE_BANDIT, 0),
         (get_achievement_stat, ":number_of_caravan_raids", ACHIEVEMENT_THE_BANDIT, 1),
         (val_add, ":number_of_caravan_raids", 1),
         (set_achievement_stat, ACHIEVEMENT_THE_BANDIT, 1, ":number_of_caravan_raids"),
        
         (try_begin),
           (ge, ":number_of_village_raids", 3),
           (ge, ":number_of_caravan_raids", 3),
           (unlock_achievement, ACHIEVEMENT_THE_BANDIT),
         (try_end),
       (try_end),  

       (try_begin),
         (party_get_current_terrain, ":cur_terrain", "p_main_party"),
         (eq, ":cur_terrain", rt_snow),
         (get_achievement_stat, ":number_of_victories_at_snowy_lands", ACHIEVEMENT_BEST_SERVED_COLD, 0),
         (val_add, ":number_of_victories_at_snowy_lands", 1),
         (set_achievement_stat, ACHIEVEMENT_BEST_SERVED_COLD, 0, ":number_of_victories_at_snowy_lands"),
         
         (try_begin),
           (eq, ":number_of_victories_at_snowy_lands", 10),
           (unlock_achievement, ACHIEVEMENT_BEST_SERVED_COLD),
         (try_end),
       (try_end),              
       
	   #gekokujo 3.0 deactivate mountain blade achievement start
       #(try_begin),
       #  (ge, "$g_enemy_party", 0),
       #  (party_is_active, "$g_enemy_party"),
       #  (party_stack_get_troop_id, ":stack_troop", "$g_enemy_party", 0),          
       #  (eq, ":stack_troop", "trp_woku_pirate"),
       #   
       #  (get_achievement_stat, ":number_of_victories_aganist_woku_pirates", ACHIEVEMENT_MOUNTAIN_BLADE, 0),
       #  (val_add, ":number_of_victories_aganist_woku_pirates", 1),
       #  (set_achievement_stat, ACHIEVEMENT_MOUNTAIN_BLADE, 0, ":number_of_victories_aganist_woku_pirates"),
       #  
       #  (try_begin),
       #    (eq, ":number_of_victories_aganist_woku_pirates", 10),
       #    (unlock_achievement, ACHIEVEMENT_MOUNTAIN_BLADE),
       #  (try_end),
       #(try_end),  
	   #gekokujo 3.0 deactivate mountain blade achievement end

       (try_begin),
         (is_between, "$g_ally_party", walled_centers_begin, walled_centers_end),
         (unlock_achievement, ACHIEVEMENT_NONE_SHALL_PASS),
       (try_end),

       (try_begin),  
         (eq, "$g_joined_battle_to_help", 1), 
         (unlock_achievement, ACHIEVEMENT_GOOD_SAMARITAN),
       (try_end),
     (try_end),
          
     (assign, "$g_joined_battle_to_help", 0), 
     (call_script, "script_count_casualties_and_adjust_morale"),#new
     (call_script, "script_encounter_calculate_fit"),               

     (call_script, "script_party_count_fit_regulars", "p_main_party"),
     (assign, "$playerparty_postbattle_regulars", reg0),
     
     (try_begin),
       (eq, "$g_battle_result", 1),
       (eq, "$g_enemy_fit_for_battle", 0),
       (str_store_string, s11, "@You were victorious!"),
#       (play_track, "track_bogus"), #clear current track.
#       (call_script, "script_music_set_situation_with_culture", mtf_sit_victorious),
       (try_begin),
         (gt, "$g_friend_fit_for_battle", 1),
         (set_background_mesh, "mesh_pic_victory"),
       (try_end),
     (else_try),
       (eq, "$g_battle_result", -1),
       (ge, "$g_enemy_fit_for_battle",1),
       (this_or_next|le, "$g_friend_fit_for_battle",0),
       (le, "$playerparty_postbattle_regulars", 0),
       (str_store_string, s11, "@Battle was lost. Your forces were utterly crushed."),
       (set_background_mesh, "mesh_pic_defeat"),
     (else_try),
       (eq, "$g_battle_result", -1),
       (str_store_string, s11, "@Your companions carry you away from the fighting."),
	   ##diplomacy start+ Test gender with script
       #(troop_get_type, ":is_female", "trp_player"),#<- replaced
       (try_begin),
         #(eq, ":is_female", 1),#<- replaced
		 (eq, 1, "$character_gender"),#<- added
         (set_background_mesh, "mesh_pic_wounded_fem"),
       (else_try),
         (set_background_mesh, "mesh_pic_wounded"),
       (try_end),
		 ##diplomacy end+
     (else_try),
       (eq, "$g_battle_result", 1),
       (str_store_string, s11, "@You have defeated the enemy."),
       (try_begin),
         (gt, "$g_friend_fit_for_battle", 1),
         (set_background_mesh, "mesh_pic_victory"),
       (try_end),
     (else_try),
       (eq, "$g_battle_result", 0),
       (str_store_string, s11, "@You have retreated from the fight."),
     (try_end),
#NPC companion changes begin
##check for excessive casualties, more forgiving if battle result is good
     (try_begin),
        (gt, "$playerparty_prebattle_regulars", 9),
        (store_add, ":divisor", 3, "$g_battle_result"), 
        (store_div, ":half_of_prebattle_regulars", "$playerparty_prebattle_regulars", ":divisor"),
        (lt, "$playerparty_postbattle_regulars", ":half_of_prebattle_regulars"),
        (call_script, "script_objectionable_action", tmt_egalitarian, "str_excessive_casualties"),
     (try_end),
#NPC companion changes end

     (call_script, "script_print_casualties_to_s0", "p_player_casualties", 0),
     (str_store_string_reg, s8, s0),
     (call_script, "script_print_casualties_to_s0", "p_enemy_casualties", 0),
     (str_store_string_reg, s9, s0),
     (str_clear, s10),
     (try_begin),
       (eq, "$any_allies_at_the_last_battle", 1),
       (call_script, "script_print_casualties_to_s0", "p_ally_casualties", 0),
       (str_store_string, s10, "@^^Ally Casualties:{s0}"),
     (try_end),
     ],
    [
      ("continue",[],"Continue...",[(jump_to_menu, "$g_next_menu"),]),
    ]
  ),
  
  (
    "total_victory", 0,
    "You shouldn't be reading this... {s9}",
    "none",
    [
        # We exploit the menu condition system below.
        # The conditions should make sure that always another screen or menu is called.
        (assign, ":break", 0),
        (try_begin),
          (eq, "$routed_party_added", 0), #new
          (assign, "$routed_party_added", 1),
          
           #add new party to map (routed_warriors)
          (call_script, "script_add_routed_party"),
        (end_try),
        		
		(try_begin),
			(check_quest_active, "qst_track_down_bandits"),
			(neg|check_quest_succeeded, "qst_track_down_bandits"),
			(neg|check_quest_failed, "qst_track_down_bandits"),
			
			(quest_get_slot, ":quest_party", "qst_track_down_bandits", slot_quest_target_party),
			(party_is_active, ":quest_party"),
			(party_get_attached_to, ":quest_party_attached"),
			(this_or_next|eq, ":quest_party", "$g_enemy_party"),
				(eq, ":quest_party_attached", "$g_enemy_party"),
			(call_script, "script_succeed_quest", "qst_track_down_bandits"),	
		(try_end),
				
		(try_begin),
			(gt, "$g_private_battle_with_troop", 0),
			(troop_slot_eq, "$g_private_battle_with_troop", slot_troop_leaded_party, "$g_encountered_party"),
			(assign, "$g_private_battle_with_troop", 0),
			##diplomacy start+
			#g_disable_condescending_comments is also used to track the "enhanced/diminished prejudice" setting
			(try_begin),
				(eq, "$g_disable_condescending_comments", 0),
				(assign, "$g_disable_condescending_comments", 1),
			(else_try),
				(eq, "$g_disable_condescending_comments", 2),
				(assign, "$g_disable_condescending_comments", 3),
			(try_end),
			##diplomacy end+
		(try_end),
		
		#new - begin
        (party_get_num_companion_stacks, ":num_stacks", "p_collective_enemy"),          
        (try_for_range, ":i_stack", 0, ":num_stacks"),
          (party_stack_get_troop_id, ":stack_troop", "p_collective_enemy", ":i_stack"),
          (is_between, ":stack_troop", lords_begin, lords_end),
          (troop_is_wounded, ":stack_troop"),
          (party_add_members, "p_total_enemy_casualties", ":stack_troop", 1),
        (try_end),                      
        #new - end
          
        (try_begin),
          # Talk to ally leader          
          (eq, "$thanked_by_ally_leader", 0),
          (assign, "$thanked_by_ally_leader", 1),

          (gt, "$g_ally_party", 0),          
          #(store_add, ":total_str_without_player", "$g_starting_strength_ally_party", "$g_starting_strength_enemy_party"),                    
          
          (store_add, ":total_str_without_player", "$g_starting_strength_friends", "$g_starting_strength_enemy_party"),
          (val_sub, ":total_str_without_player", "$g_starting_strength_main_party"),

          (store_sub, ":ally_strength_without_player", "$g_starting_strength_friends", "$g_starting_strength_main_party"),
        
          (store_mul, ":ally_advantage", ":ally_strength_without_player", 100),
          (val_add, ":total_str_without_player", 1),
          (val_div, ":ally_advantage", ":total_str_without_player"),
          #Ally advantage=50  means battle was evenly matched

          (store_sub, ":enemy_advantage", 100, ":ally_advantage"),
        
          (store_mul, ":faction_reln_boost", ":enemy_advantage", "$g_starting_strength_enemy_party"),
          (val_div, ":faction_reln_boost", 3000),
          (val_min, ":faction_reln_boost", 4),

          (store_mul, "$g_relation_boost", ":enemy_advantage", ":enemy_advantage"),
          (val_div, "$g_relation_boost", 700),
          (val_clamp, "$g_relation_boost", 0, 20),
        
          (party_get_num_companion_stacks, ":num_ally_stacks", "$g_ally_party"),
          (gt, ":num_ally_stacks", 0),
          (store_faction_of_party, ":ally_faction","$g_ally_party"),
		  #gekokujo 3.1 fix bandit swarm start
		  #do not give a faction relation boost if you fought on the side of the bandits
          #(call_script, "script_change_player_relation_with_faction", ":ally_faction", ":faction_reln_boost"),
		  (party_get_template_id, ":cur_template_id", "$g_ally_party"),
		  (try_begin),
		    (this_or_next|neq, ":cur_template_id", "pt_looters"),
			(this_or_next|neq, ":cur_template_id", "pt_seto_pirates"),
			(this_or_next|neq, ":cur_template_id", "pt_kanto_rebels"),
			(this_or_next|neq, ":cur_template_id", "pt_northern_raiders"),
			(this_or_next|neq, ":cur_template_id", "pt_shinano_rebels"),
			(this_or_next|neq, ":cur_template_id", "pt_kinai_rebels"),
			(this_or_next|neq, ":cur_template_id", "pt_woku_pirates"),
			(this_or_next|neq, ":cur_template_id", "pt_monk_rebels"),
			(this_or_next|neq, ":cur_template_id", "pt_troublesome_bandits"),
			(this_or_next|neq, ":cur_template_id", "pt_bandits_awaiting_ransom"),
			(neq, ":cur_template_id", "pt_deserters"),
			(call_script, "script_change_player_relation_with_faction", ":ally_faction", ":faction_reln_boost"),
		  (try_end),
		  #gekokujo 3.1 fix bandit swarm end
          (party_stack_get_troop_id, ":ally_leader", "$g_ally_party"),
          (party_stack_get_troop_dna, ":ally_leader_dna", "$g_ally_party", 0),
          (try_begin),
            (troop_is_hero, ":ally_leader"),
            (troop_get_slot, ":hero_relation", ":ally_leader", slot_troop_player_relation),
            (assign, ":rel_boost", "$g_relation_boost"),
            (try_begin),
              (lt, ":hero_relation", -5),
              (val_div, ":rel_boost", 3),
            (try_end),
            (call_script,"script_change_player_relation_with_troop", ":ally_leader", ":rel_boost"),
          (try_end),
          (assign, "$talk_context", tc_ally_thanks),
          (call_script, "script_setup_troop_meeting", ":ally_leader", ":ally_leader_dna"),
        (else_try),
          # Talk to enemy leaders                                        
          (assign, ":break", 0),
          
          (party_get_num_companion_stacks, ":num_stacks", "p_total_enemy_casualties"), #p_encountered changed to total_enemy_casualties			        
          (try_for_range, ":stack_no", "$last_defeated_hero", ":num_stacks"), #May 31 bug note -- this now returns some heroes in victorious party as well as in the other party
            (eq, ":break", 0),
            (party_stack_get_troop_id, ":stack_troop", "p_total_enemy_casualties", ":stack_no"),
            (party_stack_get_troop_dna, ":stack_troop_dna", "p_total_enemy_casualties", ":stack_no"),
            
            (troop_is_hero, ":stack_troop"),
                                    
            (store_troop_faction, ":defeated_faction", ":stack_troop"),
            #steve post 0912 changes begin - removed, this is duplicated elsewhere in game menus
            #(call_script, "script_add_log_entry", logent_lord_defeated_by_player, "trp_player",  -1, ":stack_troop", ":defeated_faction"),
            (try_begin),
   			  (store_relation, ":relation", ":defeated_faction", "fac_player_faction"),
			  (ge, ":relation", 0),
			  (str_store_troop_name, s4, ":stack_troop"),

			  (try_begin),
				(eq, "$cheat_mode", 1),
				(display_message, "@{!}{s4} skipped in p_total_enemy_casualties capture queue because is friendly"),
			  (try_end),			
			(else_try),
              (try_begin),
                (party_stack_get_troop_id, ":party_leader", "$g_encountered_party", 0),
                (is_between, ":party_leader", active_npcs_begin, active_npcs_end),                
                (troop_slot_eq, ":party_leader", slot_troop_occupation, slto_kingdom_hero),
                (store_sub, ":kingdom_hero_id", ":party_leader", active_npcs_begin),
                (get_achievement_stat, ":was_he_defeated_player_before", ACHIEVEMENT_BARON_GOT_BACK, ":kingdom_hero_id"),                
                (eq, ":was_he_defeated_player_before", 1),
                
                (unlock_achievement, ACHIEVEMENT_BARON_GOT_BACK),
              (try_end),

              (store_add, "$last_defeated_hero", ":stack_no", 1),                    
              (call_script, "script_remove_troop_from_prison", ":stack_troop"),
              (troop_set_slot, ":stack_troop", slot_troop_leaded_party, -1),

              (call_script, "script_cf_check_hero_can_escape_from_player", ":stack_troop"),
                            
              (str_store_troop_name, s1, ":stack_troop"),
              (str_store_faction_name, s3, ":defeated_faction"),
              (str_store_string, s17, "@{s1} of {s3} managed to escape."),
              (display_log_message, "@{!}{s17}"),
              (jump_to_menu, "mnu_enemy_slipped_away"),
              (assign, ":break", 1),			  
			(else_try),
              (store_add, "$last_defeated_hero", ":stack_no", 1),                    
              (call_script, "script_remove_troop_from_prison", ":stack_troop"),
              (troop_set_slot, ":stack_troop", slot_troop_leaded_party, -1),

              (assign, "$talk_context", tc_hero_defeated),                            
			  
              (call_script, "script_setup_troop_meeting", ":stack_troop", ":stack_troop_dna"),
              (assign, ":break", 1),
            (try_end),
          (try_end),          
                  
          (eq, ":break", 1),          
        (else_try),
          # Talk to freed heroes
          (assign, ":break", 0),
          (party_get_num_prisoner_stacks, ":num_prisoner_stacks", "p_collective_enemy"),
          (try_for_range, ":stack_no", "$last_freed_hero", ":num_prisoner_stacks"),
            (eq, ":break", 0),
            (party_prisoner_stack_get_troop_id, ":stack_troop", "p_collective_enemy", ":stack_no"),
            (troop_is_hero, ":stack_troop"),
            (party_prisoner_stack_get_troop_dna, ":stack_troop_dna", "p_collective_enemy", ":stack_no"),
            (store_add, "$last_freed_hero", ":stack_no", 1),
            (assign, "$talk_context", tc_hero_freed),
            (call_script, "script_setup_troop_meeting", ":stack_troop", ":stack_troop_dna"),
            (assign, ":break", 1),
          (try_end),          
          (eq, ":break", 1),          
        (else_try),                 
          (eq, "$capture_screen_shown", 0),
          (assign, "$capture_screen_shown", 1),
          (party_clear, "p_temp_party"),
          (assign, "$g_move_heroes", 0),          
          #(call_script, "script_party_prisoners_add_party_companions", "p_temp_party", "p_collective_enemy"),
        
          #p_total_enemy_casualties deki yarali askerler p_temp_party'e prisoner olarak eklenecek.
          (call_script, "script_party_add_wounded_members_as_prisoners", "p_temp_party", "p_total_enemy_casualties"),
        
          (call_script, "script_party_add_party_prisoners", "p_temp_party", "p_collective_enemy"),          
          (try_begin),
            (call_script, "script_party_calculate_strength", "p_collective_friends_backup",0),
            (assign,":total_initial_strength", reg(0)),
            (gt, ":total_initial_strength", 0),
            #(gt, "$g_ally_party", 0),
            (call_script, "script_party_calculate_strength", "p_main_party_backup",0),
            (assign,":player_party_initial_strength", reg(0)),
            # move ally_party_initial_strength/(player_party_initial_strength + ally_party_initial_strength) prisoners to ally party.
            # First we collect the share of prisoners of the ally party and distribute those among the allies.
            (store_sub, ":ally_party_initial_strength", ":total_initial_strength", ":player_party_initial_strength"),

            #(call_script, "script_party_calculate_strength", "p_ally_party_backup"),
            #(assign,":ally_party_initial_strength", reg(0)),
            #(store_add, ":total_initial_strength", ":player_party_initial_strength", ":ally_party_initial_strength"),
            (store_mul, ":ally_share", ":ally_party_initial_strength", 1000),
            (val_div, ":ally_share", ":total_initial_strength"),
            (assign, "$pin_number", ":ally_share"), #we send this as a parameter to the script.
            (party_clear, "p_temp_party_2"),
            (call_script, "script_move_members_with_ratio", "p_temp_party", "p_temp_party_2"),
        
            #TODO: This doesn't handle prisoners if our allies joined battle after us.
            (try_begin),
              (gt, "$g_ally_party", 0),
              (distribute_party_among_party_group, "p_temp_party_2", "$g_ally_party"),
            (try_end),
            #next if there's anything left, we'll open up the party exchange screen and offer them to the player.
          (try_end),
          (party_get_num_companions, ":num_rescued_prisoners", "p_temp_party"),
          (party_get_num_prisoners,  ":num_captured_enemies", "p_temp_party"),

          (store_add, ":total_capture_size", ":num_rescued_prisoners", ":num_captured_enemies"),
          
          (gt, ":total_capture_size", 0),          
          (change_screen_exchange_with_party, "p_temp_party"),
        (else_try),          
          (eq, "$loot_screen_shown", 0),
          (assign, "$loot_screen_shown", 1),
#gekokujo 3.0 integrating 1.158 change start
#          (try_begin),
#            (gt, "$g_ally_party", 0),
#            (call_script, "script_party_add_party", "$g_ally_party", "p_temp_party"), #Add remaining prisoners to ally TODO: FIX it.
#          (else_try),
#            (party_get_num_attached_parties, ":num_quick_attachments", "p_main_party"),
#            (gt, ":num_quick_attachments", 0),
#            (party_get_attached_party_with_rank, ":helper_party", "p_main_party", 0),
#            (call_script, "script_party_add_party", ":helper_party", "p_temp_party"), #Add remaining prisoners to our reinforcements
#          (try_end),     
#gekokujo 3.0 integrating 1.158 change end
          (troop_clear_inventory, "trp_temp_troop"),
          (call_script, "script_party_calculate_loot", "p_total_enemy_casualties"), #p_encountered_party_backup changed to total_enemy_casualties
          (gt, reg0, 0),          
          (troop_sort_inventory, "trp_temp_troop"),
		  ##diplomacy start+
		  #Here: we jump to rubik's autoloot from CC if applicable instead of using the standard loot screen
		  (try_begin),
			(call_script, "script_cf_dplmc_player_party_meets_autoloot_conditions"),
			(assign, "$dplmc_return_menu", "mnu_total_victory"),
            (jump_to_menu, "mnu_dplmc_manage_loot_pool"),
		  (else_try),
			#Old behavior:
			(change_screen_loot, "trp_temp_troop"),
		  (try_end),
		  ##diplomacy end+
        (else_try),
          #finished all
          (try_begin),
            (le, "$g_ally_party", 0),
            (end_current_battle),
          (try_end),
          (call_script, "script_party_give_xp_and_gold", "p_total_enemy_casualties"), #p_encountered_party_backup changed to total_enemy_casualties
          (try_begin),
            (eq, "$g_enemy_party", 0),
            (display_message,"str_error_string"),
          (try_end),

		  (try_begin),
		    (party_is_active, "$g_ally_party"),
			(call_script, "script_battle_political_consequences", "$g_enemy_party", "$g_ally_party"),
		  (else_try),
			(call_script, "script_battle_political_consequences", "$g_enemy_party", "p_main_party"),
		  (try_end),
		  
          (call_script, "script_event_player_defeated_enemy_party", "$g_enemy_party"),
          (call_script, "script_clear_party_group", "$g_enemy_party"),
          (try_begin),
            (eq, "$g_next_menu", -1),

            #NPC companion changes begin
            (call_script, "script_post_battle_personality_clash_check"),
            #NPC companion changes end

            #Post 0907 changes begin
            (party_stack_get_troop_id, ":enemy_leader", "p_encountered_party_backup",0),
            (try_begin),
              (is_between, ":enemy_leader", active_npcs_begin, active_npcs_end),
              (neg|is_between, "$g_encountered_party", centers_begin, centers_end),
              (store_troop_faction, ":enemy_leader_faction", ":enemy_leader"),

              (try_begin),
                (eq, "$g_ally_party", 0),
                (call_script, "script_add_log_entry", logent_lord_defeated_by_player, "trp_player",  -1, ":enemy_leader", ":enemy_leader_faction"),
                (try_begin),
                  (eq, "$cheat_mode", 1),
                  (display_message, "@{!}Victory comment. Player was alone"),
                (try_end),
              (else_try),
                (ge, "$g_strength_contribution_of_player", 40), 
                (call_script, "script_add_log_entry", logent_lord_defeated_by_player, "trp_player",  -1, ":enemy_leader", ":enemy_leader_faction"),
                (try_begin),
                  (eq, "$cheat_mode", 1),
                  (display_message, "@{!}Ordinary victory comment. The player provided at least 40 percent forces."),
                (try_end),
              (else_try),
                (gt, "$g_starting_strength_enemy_party", 1000),
                (call_script, "script_get_closest_center", "p_main_party"),
                (assign, ":battle_of_where", reg0),
                (call_script, "script_add_log_entry", logent_player_participated_in_major_battle, "trp_player",  ":battle_of_where", -1, ":enemy_leader_faction"),
                (try_begin),
                  (eq, "$cheat_mode", 1),
                  (display_message, "@{!}Player participation comment. The enemy had at least 1k starting strength."),
                (try_end),
              (else_try),
                (eq, "$cheat_mode", 1),
                (display_message, "@{!}No victory comment. The battle was small, and the player provided less than 40 percent of allied strength"),
              (try_end),
            (try_end),
            #Post 0907 changes end
            (val_add, "$g_total_victories", 1),
            (leave_encounter),
            (change_screen_return),
          (else_try),            
            (try_begin), #my kingdom
            ##diplomacy begin
			  (this_or_next|eq, "$g_next_menu", "mnu_fort_taken"), #gekokujo 3.0 microfactions! fort was taken (duh)
              (eq, "$g_next_menu", "mnu_dplmc_town_riot_removed"),
              (jump_to_menu, "$g_next_menu"),
            (else_try),
            ##diplomacy end
              #(change_screen_return),              
              (eq, "$g_next_menu", "mnu_castle_taken"),
              
              (call_script, "script_add_log_entry", logent_castle_captured_by_player, "trp_player", "$g_encountered_party", -1, "$g_encountered_party_faction"),
              (store_current_hours, ":hours"),
			  (faction_set_slot, "$players_kingdom", slot_faction_ai_last_decisive_event, ":hours"),
			  
              (try_begin), #player took a walled center while he is a vassal of npc kingdom.
			  ##diplomacy start+ Handle player is co-ruler of NPC faction
				(assign, ":is_coruler", 0),
                (is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
                (call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", "$players_kingdom"),
                (ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
				(assign, ":is_coruler", 1),

				(assign, "$g_center_taken_by_player_faction", "$g_encountered_party"),
				(faction_get_slot, ":faction_leader", "fac_player_supporters_faction", slot_faction_leader),
				(try_begin),
					(eq, ":faction_leader", "trp_player"),
					(assign, ":faction_leader", heroes_end),
					(try_for_range, ":troop_no", heroes_begin, ":faction_leader"),
						(this_or_next|troop_slot_eq, slot_troop_spouse, "trp_player"),
							(troop_slot_eq, "trp_player", slot_troop_spouse, ":troop_no"),
						(neg|troop_slot_ge, ":faction_leader", slot_troop_prisoner_of_party, 0),#Not a prisoner
						(neg|troop_slot_ge, ":faction_leader", slot_troop_occupation, slto_retirement),#Not retired, exiled, dead
						(assign, ":faction_leader", ":troop_no"),#assign and break the loop
					(try_end),
				(try_end),

				(is_between, ":faction_leader", heroes_begin, heroes_end),#Not the player, and not a bogus value
				(neg|troop_slot_ge, ":faction_leader", slot_troop_prisoner_of_party, 0),#Not a prisoner
				(neg|troop_slot_ge, ":faction_leader", slot_troop_occupation, slto_retirement),#Not retired, exiled, dead

				(change_screen_return),
				(start_map_conversation, ":faction_leader", -1),
			  (else_try),
			  #player took a walled center while he is a vassal of npc kingdom.
			    (neq, ":is_coruler", 1),
			  ##diplomacy end+
                (is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
                (jump_to_menu, "$g_next_menu"),
              (else_try), #player took a walled center while he is a vassal of rebels.
                (eq, "$players_kingdom", "fac_player_supporters_faction"), 
                (assign, "$g_center_taken_by_player_faction", "$g_encountered_party"),                
                (neg|faction_slot_eq, "fac_player_supporters_faction", slot_faction_leader, "trp_player"),
                (faction_get_slot, ":faction_leader", "fac_player_supporters_faction", slot_faction_leader),
                (change_screen_return),              
                (start_map_conversation, ":faction_leader", -1),
              (else_try), #player took a walled center for player's kingdom
			    ##diplomacy start+ Handle player is co-ruler of faction
				(this_or_next|eq, ":is_coruler", 1),
				##diplomacy end+
                (neg|is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),                
                (assign, "$g_center_taken_by_player_faction", "$g_encountered_party"),
                (assign, "$talk_context", tc_give_center_to_fief),
                (change_screen_return),              
                
                (assign, ":best_troop", "trp_gekokujo_uesugi_mounted_officer"),
				##diplomacy start+
				#Trivial aesthetic change, change the default troop to be appropriate to the
				#culture of the player kingdom (instead of defaulting always to a Swadian troop).
				(assign, ":players_culture", "$players_kingdom"),
				(try_begin),
					#If not the co-ruler of an NPC kingdom, use the player faction culture.
				   (neg|is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
				   (assign, ":best_troop", "trp_hired_gunner"),#<- while we're at it, use a mercenary default
				   (assign, ":players_culture", "$g_player_culture"),
				   (this_or_next|is_between, ":players_culture", npc_kingdoms_begin, npc_kingdoms_end),
					(is_between, ":players_culture", cultures_begin, cultures_end),
				(else_try),
					#If not the co-ruler of an NPC kingdom, and there wasn't a valid player faction
					#culture, try to use the faction of the player's court.
					(neg|is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
					(is_between, "$g_player_court", centers_begin, centers_end),
					(party_slot_ge, "$g_player_court", slot_center_original_faction, 1),
					(party_get_slot, ":players_culture", "$g_player_court", slot_center_original_faction),
				(try_end),
				(try_begin),
					#Resolve from kingdom to culture if necessary
				   (is_between, ":players_culture", kingdoms_begin, kingdoms_end),
				   (faction_get_slot, ":players_culture", ":players_culture", slot_faction_culture),
				(try_end),
				(try_begin),
					#If the final result is a culture, get the best troop if valid
				   (is_between, ":players_culture", cultures_begin, cultures_end),
				   (neq, ":players_culture", "fac_culture_1"),
				   (faction_get_slot, reg0, ":players_culture", slot_faction_guard_troop),
				   (ge, reg0, soldiers_begin),
				   (assign, ":best_troop", reg0),
				(try_end),
				##diplomacy end+
                (assign, ":maximum_troop_score", 0),
                
                (party_get_num_companion_stacks, ":num_stacks", "p_main_party"),
                (try_for_range, ":stack_no", 0, ":num_stacks"),
                  (party_stack_get_troop_id, ":stack_troop", "p_main_party", ":stack_no"),
                  (neq, ":stack_troop", "trp_player"),

                  (party_stack_get_size, ":stack_size", "p_main_party", ":stack_no"),
                  (party_stack_get_num_wounded, ":num_wounded", "p_main_party", ":stack_no"),
                  (troop_get_slot, ":num_routed", "p_main_party", slot_troop_player_routed_agents),
                                    
                  (assign, ":continue", 0),                  
                  (try_begin),
                    (neg|troop_is_hero, ":stack_troop"),
                    (store_add, ":agents_which_cannot_speak", ":num_wounded", ":num_routed"),
                    (gt, ":stack_size", ":agents_which_cannot_speak"),
                    (assign, ":continue", 1),
                  (else_try),
                    (troop_is_hero, ":stack_troop"),
                    (neg|troop_is_wounded, ":stack_troop"),
                    (assign, ":continue", 1),
                  (try_end),                  
                  (eq, ":continue", 1),

                  (try_begin),
                    (troop_is_hero, ":stack_troop"),
                    (troop_get_slot, ":troop_renown", ":stack_troop", slot_troop_renown),
                    (store_mul, ":troop_score", ":troop_renown", 100),
                    (val_add, ":troop_score", 1000),
                  (else_try),                  
                    (store_character_level, ":troop_level", ":stack_troop"),
                    (assign, ":troop_score", ":troop_level"),
                  (try_end),
                                    
                  (try_begin),
                    (gt, ":troop_score", ":maximum_troop_score"),
                    (assign, ":maximum_troop_score", ":troop_score"),
                    (assign, ":best_troop", ":stack_troop"),                    
                    (party_stack_get_troop_dna, ":best_troop_dna", "p_main_party", ":stack_no"),
                  (try_end),
                (try_end),                                                                
                                
                (start_map_conversation, ":best_troop", ":best_troop_dna"),
              (try_end),
            (try_end),
          (try_end),
        (try_end),
      ],
    [
      ("continue",[],"Continue...",[]),
        ]
  ),
  (
    "enemy_slipped_away",0,
    "{s17}",
    "none",
    [],
    [
      ("continue",[],"Continue...",[(jump_to_menu,"mnu_total_victory")]),
    ]
  ),
  (
    "total_defeat",0,
    "{!}You shouldn't be reading this...",
    "none",
    [
        (play_track, "track_captured", 1),
           # Free prisoners
          (party_get_num_prisoner_stacks, ":num_prisoner_stacks","p_main_party"),
          (try_for_range, ":stack_no", 0, ":num_prisoner_stacks"),
            (party_prisoner_stack_get_troop_id, ":stack_troop","p_main_party",":stack_no"),
            (troop_is_hero, ":stack_troop"),
            (call_script, "script_remove_troop_from_prison", ":stack_troop"),
          (try_end),

		  (try_begin),
		    (party_is_active, "$g_ally_party"),
			(call_script, "script_battle_political_consequences", "$g_ally_party", "$g_enemy_party"),
		  (else_try),
			(call_script, "script_battle_political_consequences", "p_main_party", "$g_enemy_party"),
		  (try_end),
		  
          (call_script, "script_loot_player_items", "$g_enemy_party"),

          (assign, "$g_move_heroes", 0),
          (party_clear, "p_temp_party"),
          (call_script, "script_party_add_party_prisoners", "p_temp_party", "p_main_party"),
          (call_script, "script_party_prisoners_add_party_companions", "p_temp_party", "p_main_party"),
          (distribute_party_among_party_group, "p_temp_party", "$g_enemy_party"),
        
          (assign, "$g_prison_heroes", 1),
          (call_script, "script_party_remove_all_companions", "p_main_party"),
          (assign, "$g_prison_heroes", 0),
          (assign, "$g_move_heroes", 1),
          (call_script, "script_party_remove_all_prisoners", "p_main_party"),

          (val_add, "$g_total_defeats", 1),

          (try_begin),
            (neq, "$g_player_surrenders", 1),
            (store_random_in_range, ":random_no", 0, 100),
            (ge, ":random_no", "$g_player_luck"),
            (jump_to_menu, "mnu_permanent_damage"),
          (else_try),
            (try_begin),
              (eq, "$g_next_menu", -1),
              (leave_encounter),
              (change_screen_return),
            (else_try),
              (jump_to_menu, "$g_next_menu"),
            (try_end),
          (try_end),
          (try_begin),
            (gt, "$g_ally_party", 0),
            (call_script, "script_party_wound_all_members", "$g_ally_party"),
          (try_end),

#Troop commentary changes begin
          (party_get_num_companion_stacks, ":num_stacks", "p_encountered_party_backup"),
          (try_for_range, ":stack_no", 0, ":num_stacks"),
            (party_stack_get_troop_id,   ":stack_troop","p_encountered_party_backup",":stack_no"),
            (is_between, ":stack_troop", active_npcs_begin, active_npcs_end),
			(troop_slot_eq, ":stack_troop", slot_troop_occupation, slto_kingdom_hero),
            (store_troop_faction, ":victorious_faction", ":stack_troop"),
            (call_script, "script_add_log_entry", logent_player_defeated_by_lord, "trp_player",  -1, ":stack_troop", ":victorious_faction"),
          (try_end),
#Troop commentary changes end

      ],
    []
  ),
  (
    "permanent_damage",mnf_disable_all_keys,
    "{s0}",
    "none",
    [
      (assign, ":end_cond", 1),
      (try_for_range, ":unused", 0, ":end_cond"),
        (store_random_in_range, ":random_attribute", 0, 4),
        (store_attribute_level, ":attr_level", "trp_player", ":random_attribute"),
        (try_begin),
          (gt, ":attr_level", 3),
          (neq, ":random_attribute", ca_charisma),
          (try_begin),
            (eq, ":random_attribute", ca_strength),
            (str_store_string, s0, "@Some of your tendons have been damaged in the battle. You lose 1 strength."),
          (else_try),
            (eq, ":random_attribute", ca_agility),
            (str_store_string, s0, "@You took a nasty wound which will cause you to limp slightly even after it heals. You lose 1 agility."),
##          (else_try),
##            (eq, ":random_attribute", ca_charisma),
##            (str_store_string, s0, "@After the battle you are aghast to find that one of the terrible blows you suffered has left a deep, disfiguring scar on your face, horrifying those around you. Your charisma is reduced by 1."),
          (else_try),
##            (eq, ":random_attribute", ca_intelligence),
            (str_store_string, s0, "@You have trouble thinking straight after the battle, perhaps from a particularly hard hit to your head, and frequent headaches now plague your existence. Your intelligence is reduced by 1."),
          (try_end),
        (else_try),
          (lt, ":end_cond", 200),
          (val_add, ":end_cond", 1),
        (try_end),
      (try_end),
      (try_begin),
        (eq, ":end_cond", 200),
        (try_begin),
          (eq, "$g_next_menu", -1),
          (leave_encounter),
          (change_screen_return),
        (else_try),
          (jump_to_menu, "$g_next_menu"),
        (try_end),
      (else_try),
        (troop_raise_attribute, "trp_player", ":random_attribute", -1),
      (try_end),
      ],
    [
      ("s0",
       [
         (store_random_in_range, ":random_no", 0, 4),
         (try_begin),
           (eq, ":random_no", 0),
           (str_store_string, s0, "@Perhaps I'm getting unlucky..."),
         (else_try),
           (eq, ":random_no", 1),
           (str_store_string, s0, "@Retirement is starting to sound better and better."),
         (else_try),
           (eq, ":random_no", 2),
           (str_store_string, s0, "@No matter! I will persevere!"),
         (else_try),
           (eq, ":random_no", 3),
		   ##diplomacy start+ Don't use troop_get_type for gender
           #(troop_get_type, ":is_female", "trp_player"),#<- replaced
           (try_begin),
             #(eq, ":is_female", 1),#<- replaced
			 (eq, 1, "$character_gender"),#<- added
             (str_store_string, s0, "@What did I do to deserve this?"),
           (else_try),
             (str_store_string, s0, "@I suppose it'll make for a good story, at least..."),
           (try_end),
			  ##diplomacy end+
         (try_end),
         ],
       "{s0}",
       [
         (try_begin),
           (eq, "$g_next_menu", -1),
           (leave_encounter),
           (change_screen_return),
         (else_try),
           (jump_to_menu, "$g_next_menu"),
         (try_end),
         ]),
      ]
  ),
  
  (
    "pre_join",0,
    "You come across a battle between {s2} and {s1}. You decide to...",
    "none",
    [
        (str_store_party_name, 1,"$g_encountered_party"),
        (str_store_party_name, 2,"$g_encountered_party_2"),
      ],
    [
      ("pre_join_help_attackers",[
          #gekokujo 3.0 join any side during battle
          #(store_faction_of_party, ":attacker_faction", "$g_encountered_party_2"),
          #(store_relation, ":attacker_relation", ":attacker_faction", "fac_player_supporters_faction"),
          #(store_faction_of_party, ":defender_faction", "$g_encountered_party"),
          #(store_relation, ":defender_relation", ":defender_faction", "fac_player_supporters_faction"),
          #(ge, ":attacker_relation", 0),
          #(lt, ":defender_relation", 0),
          ],
          "Move in to help the {s2}.",[
              (select_enemy,0),
              (assign,"$g_enemy_party","$g_encountered_party"),
              (assign,"$g_ally_party","$g_encountered_party_2"),
              (jump_to_menu,"mnu_join_battle")]),
      ("pre_join_help_defenders",[
          #gekokujo 3.0 join any side during battle
		  #(store_faction_of_party, ":attacker_faction", "$g_encountered_party_2"),
          #(store_relation, ":attacker_relation", ":attacker_faction", "fac_player_supporters_faction"),
          #(store_faction_of_party, ":defender_faction", "$g_encountered_party"),
          #(store_relation, ":defender_relation", ":defender_faction", "fac_player_supporters_faction"),
          #(ge, ":defender_relation", 0),
          #(lt, ":attacker_relation", 0),
          ],
          "Rush to the aid of the {s1}.",[
              (select_enemy,1),
              (assign,"$g_enemy_party","$g_encountered_party_2"),
              (assign,"$g_ally_party","$g_encountered_party"),
              (jump_to_menu,"mnu_join_battle")]),
      ("pre_join_leave",[],"Don't get involved.",[(leave_encounter),(change_screen_return)]),
    ]
  ),
  
  (
    "join_battle",0,
    "You are helping the {s2} against the {s1}. You have {reg10} troops fit for battle against the enemy's {reg11}.",
    "none",
    [                
        (str_store_party_name, 1,"$g_enemy_party"),
        (str_store_party_name, 2,"$g_ally_party"),

        (call_script, "script_encounter_calculate_fit"),                

        (try_begin),
          (eq, "$new_encounter", 1),
          (assign, "$new_encounter", 0),
          (call_script, "script_encounter_init_variables"),
        (else_try), #second or more turn
          (eq, "$g_leave_encounter",1),
          (change_screen_return),
        (try_end),

        (try_begin),
          (call_script, "script_party_count_members_with_full_health", "p_collective_enemy"),
          (assign, ":num_enemy_regulars_remaining", reg0),
          (assign, ":enemy_finished",0),
          (try_begin),
            (eq, "$g_battle_result", 1), 
            
            (this_or_next|le, ":num_enemy_regulars_remaining", 0), #battle won
            (le, ":num_enemy_regulars_remaining", "$num_routed_enemies"), #replaced for above line because we do not want routed agents to spawn again in next turn of battle.
            
            (assign, ":enemy_finished",1),
          (else_try),
            (eq, "$g_engaged_enemy", 1),
            (le, "$g_enemy_fit_for_battle",0),
            (ge, "$g_friend_fit_for_battle",1),
            (assign, ":enemy_finished",1),
          (try_end),
          
          (this_or_next|eq, ":enemy_finished",1),
          (eq,"$g_enemy_surrenders",1),
          (assign, "$g_next_menu", -1),
          (jump_to_menu, "mnu_total_victory"),
        (else_try),
          (call_script, "script_party_count_members_with_full_health", "p_collective_friends"),
          (assign, ":num_ally_regulars_remaining", reg0),
          (assign, ":battle_lost", 0),
          (try_begin),
            (eq, "$g_battle_result", -1),
            
            #(eq, ":num_ally_regulars_remaining", 0), #battle lost
            (le, ":num_ally_regulars_remaining",  "$num_routed_allies"), #replaced for above line because we do not want routed agents to spawn again in next turn of battle.
            
            (assign, ":battle_lost",1),
          (try_end),
          
          (this_or_next|eq, ":battle_lost",1),
          (eq,"$g_player_surrenders",1),
          (leave_encounter),
          (change_screen_return),
        (try_end),
      ],
    [

#gekokujo 2.1 PBO
## PreBattle Orders Begin
	  ("join_attack_plan",
      [
        (neg|troop_is_wounded, "trp_player"),
		(party_get_skill_level, ":tactics", "p_main_party", skl_tactics),
		(ge, ":tactics", 2),
      ],
	   "Plan your attack on the enemy.",
      [
  		(assign, "$g_next_menu", "mnu_join_battle"),	
		(start_presentation, "prsnt_prebattle_orders"),
      ]),
	  
	  ("join_attack_do_plan",
      [
         (party_slot_eq, "p_main_party", slot_party_prebattle_plan, 1),
      ],
      "Enough planning. To battle!",
      [
	    (party_set_slot, "p_main_party", slot_party_prebattle_plan, 0),
	  
        (assign, "$g_joined_battle_to_help", 1),
        (party_set_next_battle_simulation_time, "$g_encountered_party", -1),
        (assign, "$g_battle_result", 0),
        (call_script, "script_calculate_renown_value"),
        (call_script, "script_calculate_battle_advantage"),
        (set_battle_advantage, reg0),
        (set_party_battle_mode),
        (set_jump_mission,"mt_lead_charge"),
		
        #gekokujo 3.0 disable horses in sea battles start
        (party_get_current_terrain, ":terrain_type", "p_main_party"),
        (try_begin),
          (eq, ":terrain_type", rt_bridge),
          (mission_tpl_entry_set_override_flags, "mt_lead_charge", 0, af_override_horse),
          (mission_tpl_entry_set_override_flags, "mt_lead_charge", 1, af_override_horse),
          (mission_tpl_entry_set_override_flags, "mt_lead_charge", 2, af_override_horse),
          (mission_tpl_entry_set_override_flags, "mt_lead_charge", 3, af_override_horse),
        (try_end),
        #gekokujo 3.0 disable horses in sea battles end
		
        (call_script, "script_setup_random_scene"),
        (assign, "$g_next_menu", "mnu_join_battle"),
        (jump_to_menu, "mnu_battle_debrief"),
        (change_screen_mission),
      ]),
	  
	  ("join_attack_clear_plan",
      [
         (party_slot_eq, "p_main_party", slot_party_prebattle_plan, 1),
      ],
      "Re-assess the situation.",
      [
        (party_set_slot, "p_main_party", slot_party_prebattle_plan, 0),
		(party_set_slot, "p_main_party", slot_party_prebattle_num_orders, 0),
		
        (jump_to_menu, "mnu_join_battle"),
      ]),
	  	  
	  ("join_attack_hold",
      [
        (neg|troop_is_wounded, "trp_player"),
		(party_get_skill_level, ":tactics", "p_main_party", skl_tactics),
		(ge, ":tactics", 1),
		(party_slot_eq, "p_main_party", slot_party_prebattle_plan, 0),
      ],
      "Take the field.",
      [
        (party_set_slot, "p_main_party", slot_party_prebattle_num_orders, 1),
		(party_get_slot, ":first_order", "p_main_party", slot_party_prebattle_order_array_begin),
		(try_begin),
		    (gt, ":first_order", 0),
			(party_set_slot, "p_main_party_backup", slot_party_prebattle_order_array_begin, ":first_order"),
        (try_end),
        (party_set_slot, "p_main_party", slot_party_prebattle_order_array_begin, 910),	
	  
        (assign, "$g_joined_battle_to_help", 1),
        (party_set_next_battle_simulation_time, "$g_encountered_party", -1),
        (assign, "$g_battle_result", 0),
        (call_script, "script_calculate_renown_value"),
        (call_script, "script_calculate_battle_advantage"),
        (set_battle_advantage, reg0),
        (set_party_battle_mode),
        (set_jump_mission,"mt_lead_charge"),
		
        #gekokujo 3.0 disable horses in sea battles start
        (party_get_current_terrain, ":terrain_type", "p_main_party"),
        (try_begin),
          (eq, ":terrain_type", rt_bridge),
          (mission_tpl_entry_set_override_flags, "mt_lead_charge", 0, af_override_horse),
          (mission_tpl_entry_set_override_flags, "mt_lead_charge", 1, af_override_horse),
          (mission_tpl_entry_set_override_flags, "mt_lead_charge", 2, af_override_horse),
          (mission_tpl_entry_set_override_flags, "mt_lead_charge", 3, af_override_horse),
        (try_end),
        #gekokujo 3.0 disable horses in sea battles end
		
        (call_script, "script_setup_random_scene"),
        (assign, "$g_next_menu", "mnu_join_battle"),
        (jump_to_menu, "mnu_battle_debrief"),
        (change_screen_mission),
      ]),
	  
	  ("join_attack_follow",
      [
        (neg|troop_is_wounded, "trp_player"),
		(party_get_skill_level, ":tactics", "p_main_party", skl_tactics),
		(ge, ":tactics", 1),
		(party_slot_eq, "p_main_party", slot_party_prebattle_plan, 0),
      ],
      "Lead your troops.",
      [
        (party_set_slot, "p_main_party", slot_party_prebattle_num_orders, 1),
		(party_get_slot, ":first_order", "p_main_party", slot_party_prebattle_order_array_begin),
		(try_begin),
		    (gt, ":first_order", 0),
			(party_set_slot, "p_main_party_backup", slot_party_prebattle_order_array_begin, ":first_order"),
        (try_end),
        (party_set_slot, "p_main_party", slot_party_prebattle_order_array_begin, 911),	
	  
        (assign, "$g_joined_battle_to_help", 1),
        (party_set_next_battle_simulation_time, "$g_encountered_party", -1),
        (assign, "$g_battle_result", 0),
        (call_script, "script_calculate_renown_value"),
        (call_script, "script_calculate_battle_advantage"),
        (set_battle_advantage, reg0),
        (set_party_battle_mode),
        (set_jump_mission,"mt_lead_charge"),
		
        #gekokujo 3.0 disable horses in sea battles start
        (party_get_current_terrain, ":terrain_type", "p_main_party"),
        (try_begin),
          (eq, ":terrain_type", rt_bridge),
          (mission_tpl_entry_set_override_flags, "mt_lead_charge", 0, af_override_horse),
          (mission_tpl_entry_set_override_flags, "mt_lead_charge", 1, af_override_horse),
          (mission_tpl_entry_set_override_flags, "mt_lead_charge", 2, af_override_horse),
          (mission_tpl_entry_set_override_flags, "mt_lead_charge", 3, af_override_horse),
        (try_end),
        #gekokujo 3.0 disable horses in sea battles end
		
        (call_script, "script_setup_random_scene"),
        (assign, "$g_next_menu", "mnu_join_battle"),
        (jump_to_menu, "mnu_battle_debrief"),
        (change_screen_mission),
      ]),
## PreBattle Orders End
 
      ("change_battlefield_size",
        [
          (neg|troop_is_wounded, "trp_player"),
          (store_add, ":dest_string", "str_battlefield_small", "$g_random_scene_size"),
          (str_store_string, s3, ":dest_string"),
         ],
        "Change battlefield size({s3}).",
        [
        (val_add, "$g_random_scene_size", 1),
        (val_mod, "$g_random_scene_size", 4),
        (jump_to_menu, "mnu_join_battle"),]),

      ("join_attack",
      [
        (neg|troop_is_wounded, "trp_player"),
		#gekokujo 2.1 PBO
		## PreBattle Orders Begin
		(party_slot_eq, "p_main_party", slot_party_prebattle_plan, 0),
		## PreBattle Orders End
      ],
      "Charge the enemy.",
      [
        (assign, "$g_joined_battle_to_help", 1),
        (party_set_next_battle_simulation_time, "$g_encountered_party", -1),
        (assign, "$g_battle_result", 0),
        (call_script, "script_calculate_renown_value"),
        (call_script, "script_calculate_battle_advantage"),
        (set_battle_advantage, reg0),
        (set_party_battle_mode),
        (set_jump_mission,"mt_lead_charge"),
		
        #gekokujo 3.0 disable horses in sea battles start
        (party_get_current_terrain, ":terrain_type", "p_main_party"),
        (try_begin),
          (eq, ":terrain_type", rt_bridge),
          (mission_tpl_entry_set_override_flags, "mt_lead_charge", 0, af_override_horse),
          (mission_tpl_entry_set_override_flags, "mt_lead_charge", 1, af_override_horse),
          (mission_tpl_entry_set_override_flags, "mt_lead_charge", 2, af_override_horse),
          (mission_tpl_entry_set_override_flags, "mt_lead_charge", 3, af_override_horse),
        (try_end),
        #gekokujo 3.0 disable horses in sea battles end
		
        (call_script, "script_setup_random_scene"),
        (assign, "$g_next_menu", "mnu_join_battle"),
        (jump_to_menu, "mnu_battle_debrief"),
        (change_screen_mission),
      ]),

      ("join_order_attack",
      [
        (call_script, "script_party_count_members_with_full_health", "p_main_party"),
        (ge, reg0, 3),
		#gekokujo 2.1 PBO
		## PreBattle Orders Begin
		(party_slot_eq, "p_main_party", slot_party_prebattle_plan, 0),
		## PreBattle Orders End
      ],
      "Order your troops to attack with your allies while you stay back.",
      [
        (assign, "$g_joined_battle_to_help", 1),
        (party_set_next_battle_simulation_time, "$g_encountered_party", -1),
        (jump_to_menu,"mnu_join_order_attack"),
      ]),
      
      ("join_leave",[
		#gekokujo 2.1 PBO
		## PreBattle Orders Begin
		(party_slot_eq, "p_main_party", slot_party_prebattle_plan, 0),
		## PreBattle Orders End
		],"Leave.",
      [
        (try_begin),
           (neg|troop_is_wounded, "trp_player"),
           (call_script, "script_objectionable_action", tmt_aristocratic, "str_flee_battle"),
           (party_stack_get_troop_id, ":enemy_leader","$g_enemy_party",0),
		   (is_between, ":enemy_leader", active_npcs_begin, active_npcs_end),
           (call_script, "script_add_log_entry", logent_player_retreated_from_lord, "trp_player",  -1, ":enemy_leader", -1),
        (try_end),
        
        (leave_encounter),(change_screen_return)]),
      ]),
  (
    "join_order_attack",mnf_disable_all_keys,
    "{s4}^^Your casualties: {s8}^^Allies' casualties: {s9}^^Enemy casualties: {s10}",
    "none",
    [
      (call_script, "script_party_calculate_strength", "p_main_party", 1), #skip player
      (assign, ":player_party_strength", reg0),
      (val_div, ":player_party_strength", 5),
      (call_script, "script_party_calculate_strength", "p_collective_friends", 0),
      (assign, ":friend_party_strength", reg0),
      (val_div, ":friend_party_strength", 5),
                                    
      (call_script, "script_party_calculate_strength", "p_collective_enemy", 0),
      (assign, ":enemy_party_strength", reg0),
      (val_div, ":enemy_party_strength", 5),

      (try_begin),
        (eq, ":friend_party_strength", 0),
        (store_div, ":enemy_party_strength_for_p", ":enemy_party_strength", 2),
      (else_try),
        (assign, ":enemy_party_strength_for_p", ":enemy_party_strength"),
        (val_mul, ":enemy_party_strength_for_p", ":player_party_strength"),
        (val_div, ":enemy_party_strength_for_p", ":friend_party_strength"),
      (try_end),

      (val_sub, ":enemy_party_strength", ":enemy_party_strength_for_p"),
      (inflict_casualties_to_party_group, "p_main_party", ":enemy_party_strength_for_p", "p_temp_casualties"),
      (call_script, "script_print_casualties_to_s0", "p_temp_casualties", 0),
      (str_store_string_reg, s8, s0),
                                    
      (inflict_casualties_to_party_group, "$g_enemy_party", ":friend_party_strength", "p_temp_casualties"),
                                    
      #ozan begin
      (party_get_num_companion_stacks, ":num_stacks", "p_temp_casualties"), 
      (try_for_range, ":stack_no", 0, ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop", "p_temp_casualties", ":stack_no"), 
        (try_begin),
          (party_stack_get_size, ":stack_size", "p_temp_casualties", ":stack_no"),
          (gt, ":stack_size", 0),
          (party_add_members, "p_total_enemy_casualties", ":stack_troop", ":stack_size"), #addition_to_p_total_enemy_casualties
          (party_stack_get_num_wounded, ":stack_wounded_size", "p_temp_casualties", ":stack_no"),                                    
          (gt, ":stack_wounded_size", 0),
          (party_wound_members, "p_total_enemy_casualties", ":stack_troop", ":stack_wounded_size"),
        (try_end),
      (try_end),
      #ozan end

      (call_script, "script_print_casualties_to_s0", "p_temp_casualties", 0),
      (str_store_string_reg, s10, s0),
                                    
      (call_script, "script_collect_friendly_parties"),
      #(party_collect_attachments_to_party, "$g_ally_party", "p_collective_ally"),

      (inflict_casualties_to_party_group, "$g_ally_party", ":enemy_party_strength", "p_temp_casualties"),
      (call_script, "script_print_casualties_to_s0", "p_temp_casualties", 0),
      (str_store_string_reg, s9, s0),
      (party_collect_attachments_to_party, "$g_enemy_party", "p_collective_enemy"),

       #(assign, "$cant_leave_encounter", 0),
       (assign, "$no_soldiers_left", 0),
       (try_begin),
         (call_script, "script_party_count_members_with_full_health","p_main_party"),
         (assign, ":num_our_regulars_remaining", reg0),
                                      
         #(le, ":num_our_regulars_remaining", 0),
         (le, ":num_our_regulars_remaining", "$num_routed_us"), #replaced for above line because we do not want routed agents to spawn again in next turn of battle.
                                      
         (assign, "$no_soldiers_left", 1),
         (str_store_string, s4, "str_join_order_attack_failure"),
       (else_try),
         (call_script, "script_party_count_members_with_full_health","p_collective_enemy"),
         (assign, ":num_enemy_regulars_remaining", reg0),

         (this_or_next|le, ":num_enemy_regulars_remaining", 0),
         (le, ":num_enemy_regulars_remaining", "$num_routed_enemies"), #replaced for above line because we do not want routed agents to spawn again in next turn of battle.

         (assign, "$g_battle_result", 1),
         (assign, "$no_soldiers_left", 1),
         (str_store_string, s4, "str_join_order_attack_success"),
       (else_try),
         (str_store_string, s4, "str_join_order_attack_continue"),
       (try_end),
    ],
    [
      ("continue",[],"Continue...",
      [
        (jump_to_menu,"mnu_join_battle"),
      ]),
    ]
  ),
  #gekokujo 3.0 microfactions! end
  
  #gekokujo 3.1 random encounters start
  
  #mnu_encounter is the intro and setup
  #use for both friendly and hostile encounter
  (
    "encounter",0,
    "{s8}",
    "none",
    [
      (try_begin),
        (eq, "$gekokujo_encounter_accepted", 1),
        #the description is the version of the encounter menu if you choose to proceed
        (set_background_mesh, "mesh_gekokujo_pic_recruits"),
        
        #find = variations on the opening of the sentence, for no good reason
        (store_random_in_range, ":offset", 0, 4),
        (val_add, ":offset", "str_gekokujo_encounter_description_find_1"),
        (str_store_string, s8, ":offset"),
        
        #boss = the boss troop, the one you talk with in dialogue
        (store_random_in_range, ":offset", 0, 12),
        (try_begin),
          (eq, ":offset", 0),
          (assign, "$gekokujo_encounter_boss", "trp_generic_jizamurai"),
          (str_store_string, s8, "@{s8} a"), #"a" jizamurai
        (else_try),
          (eq, ":offset", 1),
          (assign, "$gekokujo_encounter_boss", "trp_monk_rebel"),
          (str_store_string, s8, "@{s8} a"), #"a" monk rebel
        (else_try),
          (eq, ":offset", 2),
          (assign, "$gekokujo_encounter_boss", "trp_shinano_rebel"),
          (str_store_string, s8, "@{s8} a"), #"a" shinano rebel
        (else_try),
          (eq, ":offset", 3),
          (assign, "$gekokujo_encounter_boss", "trp_kinai_rebel"),
          (str_store_string, s8, "@{s8} a"), #"a" kinai rebel
        (else_try),
          (eq, ":offset", 4),
          (assign, "$gekokujo_encounter_boss", "trp_kanto_rebel"),
          (str_store_string, s8, "@{s8} a"), #"a" kanto rebel
        (else_try),
          (eq, ":offset", 5),
          (assign, "$gekokujo_encounter_boss", "trp_ronin_adventurer"),
          (str_store_string, s8, "@{s8} a"), #"a" ronin adventurer
        (else_try),
          (eq, ":offset", 6),
          (assign, "$gekokujo_encounter_boss", "trp_ronin_protector"),
          (str_store_string, s8, "@{s8} a"), #"a" ronin protector
        (else_try),
          (eq, ":offset", 7),
          (assign, "$gekokujo_encounter_boss", "trp_ronin_hero"),
          (str_store_string, s8, "@{s8} a"), #"a" ronin hero
        (else_try),
          (eq, ":offset", 8),
          (assign, "$gekokujo_encounter_boss", "trp_onnabushi_veteran"),
          (str_store_string, s8, "@{s8} an"), #"an" onnabushi veteran
        (else_try),
          (eq, ":offset", 9),
          (assign, "$gekokujo_encounter_boss", "trp_onnabushi_elite"),
          (str_store_string, s8, "@{s8} an"), #"an" onnabushi elite
        (else_try),
          (eq, ":offset", 10),
          (assign, "$gekokujo_encounter_boss", "trp_hired_agent_experienced"),
          (str_store_string, s8, "@{s8} an"), #"an" experienced agent
        (else_try),
          #offset = 11
          (assign, "$gekokujo_encounter_boss", "trp_female_agent_experienced"),
          (str_store_string, s8, "@{s8} an"), #"an" experienced agent
        (try_end),
        (str_store_troop_name, s18, "$gekokujo_encounter_boss"),
        (str_store_string, s8, "@{s8} {s18}"),
        
        #circumstance = what the boss is doing
        (store_random_in_range, ":offset", 0, 20),
        (val_add, ":offset", "str_gekokujo_encounter_description_circumstance_1"),
        (str_store_string, s18, ":offset"),
        (str_store_string, s8, "@{s8} {s18}"),
        
        #mook_count = random 1 to 4
        (store_random_in_range, "$gekokujo_encounter_mook_count", 1, 5),
        (try_begin),
          (eq, "$gekokujo_encounter_mook_count", 1),
          (str_store_string, s8, "@{s8} a single"),
        (else_try),
          (str_store_string, s8, "@{s8} some"),
        (try_end),
        
        #mook = the mook troop that accompany the boss
        (store_random_in_range, ":offset", 0, 20),
        (try_begin),
          (eq, ":offset", 0),
          (assign, "$gekokujo_encounter_mook", "trp_looter"),
        (else_try),
          (eq, ":offset", 1),
          (assign, "$gekokujo_encounter_mook", "trp_bandit"),
        (else_try),
          (eq, ":offset", 2),
          (assign, "$gekokujo_encounter_mook", "trp_brigand"),
        (else_try),
          (eq, ":offset", 3),
          (assign, "$gekokujo_encounter_mook", "trp_woku_pirate"),
        (else_try),
          (eq, ":offset", 4),
          (assign, "$gekokujo_encounter_mook", "trp_seto_pirate"),
        (else_try),
          (eq, ":offset", 5),
          (assign, "$gekokujo_encounter_mook", "trp_northern_raider"),
        (else_try),
          (eq, ":offset", 6),
          (assign, "$gekokujo_encounter_mook", "trp_generic_ashigaru"),
        (else_try),
          (eq, ":offset", 7),
          (assign, "$gekokujo_encounter_mook", "trp_ronin"),
        (else_try),
          (eq, ":offset", 8),
          (assign, "$gekokujo_encounter_mook", "trp_ronin_wanderer"),
        (else_try),
          (eq, ":offset", 9),
          (assign, "$gekokujo_encounter_mook", "trp_onnabushi"),
        (else_try),
          (eq, ":offset", 10),
          (assign, "$gekokujo_encounter_mook", "trp_onnabushi_trained"),
        (else_try),
          (eq, ":offset", 11),
          (assign, "$gekokujo_encounter_mook", "trp_hired_agent"),
        (else_try),
          (eq, ":offset", 12),
          (assign, "$gekokujo_encounter_mook", "trp_female_agent"),
        (else_try),
          (eq, ":offset", 13),
          (assign, "$gekokujo_encounter_mook", "trp_farmer"),
        (else_try),
          (eq, ":offset", 14),
          (assign, "$gekokujo_encounter_mook", "trp_townsman"),
        (else_try),
          (eq, ":offset", 15),
          (assign, "$gekokujo_encounter_mook", "trp_peasant_woman"),
        (else_try),
          (eq, ":offset", 16),
          (assign, "$gekokujo_encounter_mook", "trp_yojimbo"),
        (else_try),
          (eq, ":offset", 17),
          (assign, "$gekokujo_encounter_mook", "trp_hired_warrior"),
        (else_try),
          (eq, ":offset", 18),
          (assign, "$gekokujo_encounter_mook", "trp_hired_warrior_veteran"),
        (else_try),
          #offset = 19
          (assign, "$gekokujo_encounter_mook", "trp_hired_gunner"),
        (try_end),
        (try_begin),
          (eq, "$gekokujo_encounter_mook_count", 1),
          (str_store_troop_name, s18, "$gekokujo_encounter_mook"),
        (else_try),
          (str_store_troop_name_plural, s18, "$gekokujo_encounter_mook"),
        (try_end),
        (str_store_string, s8, "@{s8} {s18}."),
        
      (else_try),
        #The intro is the first version of the menu and you can choose to proceed or cancel the encounter
        (set_background_mesh, "mesh_pic_camp"),
        
        #intro1 = what player is doing
        (store_random_in_range, ":offset", 0, 4),
        (party_get_num_companions, ":num_companions", "p_main_party"), #party count also determines offset
        (try_begin),
          (gt, ":num_companions", 30), #player has an army
          (val_add, ":offset", 8),
        (else_try),
          (gt, ":num_companions", 1), #player has a party
          (val_add, ":offset", 4),
        (try_end),
        (val_add, ":offset", "str_gekokujo_encounter_intro1_single_1"),
        (str_store_string, s8, ":offset"),
      
        #intro2 = transition
        (store_random_in_range, ":offset", 0, 4),
        (val_add, ":offset", "str_gekokujo_encounter_intro2_1"),
        (str_store_string, s18, ":offset"),
        (str_store_string, s8, "@{s8} {s18}"),
      
        #intro3 = what the player noticed
        (store_random_in_range, ":offset", 0, 12),
        (val_add, ":offset", "str_gekokujo_encounter_intro3_1"),
        (str_store_string, s18, ":offset"),
        (str_store_string, s8, "@{s8} {s18}"),
      (try_end),
    ],
    [
      ("encounter_accept", 
        [
          (eq, "$gekokujo_encounter_accepted", 0), #only show if it's an intro
          
          (store_random_in_range, ":offset", 0, 6),
          (val_add, ":offset", "str_gekokujo_encounter_intro_accept_1"),
          (str_store_string, s9, ":offset"),
        ],
        "{s9}", 
        [
          (assign, "$gekokujo_encounter_accepted", 1), #set acceptance to 1 for description mode
          (jump_to_menu, "mnu_encounter"), #iterate this menu
        ]),
      
      ("encounter_reject", 
        [
          (eq, "$gekokujo_encounter_accepted", 0), #only show if it's an intro
          
          (store_random_in_range, ":offset", 0, 6),
          (val_add, ":offset", "str_gekokujo_encounter_intro_reject_1"),
          (str_store_string, s10, ":offset"),
        ], 
        "{s10}", 
        [
          (assign, "$gekokujo_encounter_accepted", 0), #reset acceptance to 0 for intro mode
          (change_screen_return), #exit to the world
        ]),
      
      ("encounter_continue", 
        [
          (eq, "$gekokujo_encounter_accepted", 1), #only show if it's a description
        ], 
        "Continue...", 
        [          
          (assign, "$gekokujo_encounter_accepted", 0), #reset acceptance to 0 for intro mode
          #go into dialogue with the boss of friendly or hostile encounter
          
          (assign, "$npc_map_talk_context", tc_gekokujo_encounter),
          (change_screen_return),
          (start_map_conversation, "$gekokujo_encounter_boss"),
        ]),
    ],
  ),
  
  (
    "encounter_setup",mnf_disable_all_keys,
    "You get ready to fight the {s2} and {s3}.",
    "none",
    [
      (str_store_troop_name, s2, "$gekokujo_encounter_boss"),
      (try_begin),
        (eq, "$gekokujo_encounter_mook_count", 1),
        (str_store_troop_name, s3, "$gekokujo_encounter_mook"),
      (else_try),
        (str_store_troop_name_plural, s3, "$gekokujo_encounter_mook"),
      (try_end),
    ],
    [
      ("continue",[],"Continue...",
        [
          (assign, "$gekokujo_encounter_mode", 1), #1 = encounter
          (set_jump_mission, "mt_gekokujo_encounter"),
          
          (party_get_current_terrain, ":terrain_type", "p_main_party"),
          (try_begin),
            (eq, ":terrain_type", rt_snow_forest),
            (assign, ":scene", "scn_random_scene_snow_forest"),
          (else_try),
            (eq, ":terrain_type", rt_forest),
            (assign, ":scene", "scn_random_scene_plain_forest"),
          (else_try),
            (eq, ":terrain_type", rt_snow),
            (assign, ":scene", "scn_random_scene_snow"),
          (else_try),
            (assign, ":scene", "scn_random_scene_plain"),
          (try_end),
          
          (modify_visitors_at_site, ":scene"),
          (reset_visitors),
          
          (set_visitor, 2, "trp_player"),
          (set_visitors, 0, "$gekokujo_encounter_boss", 1),
          (set_visitors, 1, "$gekokujo_encounter_mook", "$gekokujo_encounter_mook_count"),
          
          #fixed x shift (so it doesn't recalculate at every ti_on_agent_spawn trigger)
          (store_random_in_range, "$gekokujo_encounter_x", 1200, 2500),
          (store_random_in_range, ":shift_sign", 0, 2),
          (try_begin),
            (eq, ":shift_sign", 0),
            (val_mul, "$gekokujo_encounter_x", -1),
          (try_end),
          
          #fixed y shift (so it doesn't recalculate at every ti_on_agent_spawn trigger)
          (store_random_in_range, "$gekokujo_encounter_y", 1200, 2500),
          (store_random_in_range, ":shift_sign", 0, 2),
          (try_begin),
            (eq, ":shift_sign", 0),
            (val_mul, "$gekokujo_encounter_y", -1),
          (try_end),
          
          (jump_to_scene, ":scene"),
          (change_screen_mission),
        ]),
    ],
  ),
  
  #mnu_encounter_won is the win screen with loot and mon rewarded
  (
    "encounter_won",mnf_disable_all_keys,
    "{s3}",
    "none",
    [
      (set_background_mesh, "mesh_gekokujo_pic_escape"),
      
      (store_random_in_range, ":offset", 0, 10),
      (val_add, ":offset", "str_gekokujo_encounter_win1_1"),
      (str_store_string, s3, ":offset"),
      
      #determine the item quality
      #12% item 1 (best), 25% item 2 (medium), 63% item 3 (worst)
      (store_random_in_range, ":item", 0, 100),
      (try_begin),
        (le, ":item", 12),
        (assign, ":item", 0), #best
      (else_try),
        (le, ":item", 37), #12 + 25
        (assign, ":item", 1), #medium
      (else_try),
        (assign, ":item", 2), #worst
      (try_end),
      
      #determine the actual item, mon, and renown reward from the boss
      #it's going to be nested 2 levels deep because i'm an idiot
      (try_begin),
        (eq, "$gekokujo_encounter_boss", "trp_generic_jizamurai"),
        (store_random_in_range, ":mon_reward", 25, 100),
        (store_random_in_range, ":renown_reward", 0, 2),
        (try_begin),
          (eq, ":item", 0), #best
          (assign, ":item_id", "itm_gekokujo_katana_3"),
          (assign, ":imod", imod_rusty),
        (else_try),
          (eq, ":item", 1), #medium
          (assign, ":item_id", "itm_gekokujo_okegawa_short_7"),
          (assign, ":imod", imod_battered),
        (else_try),
          #worst
          (assign, ":item_id", "itm_gekokujo_haori_1"),
          (assign, ":imod", imod_thick),
        (try_end),
      (else_try),
        (eq, "$gekokujo_encounter_boss", "trp_monk_rebel"),
        (store_random_in_range, ":mon_reward", 25, 100),
        (store_random_in_range, ":renown_reward", 1, 4),
        (try_begin),
          (eq, ":item", 0), #best
          (assign, ":item_id", "itm_gekokujo_arquebus_3"),
          (assign, ":imod", imod_cracked),
        (else_try),
          (eq, ":item", 1), #medium
          (assign, ":item_id", "itm_gekokujo_monk_headwrap"),
          (assign, ":imod", imod_ragged),
        (else_try),
          #worst
          (assign, ":item_id", "itm_gekokujo_kimono_2_monk"),
          (assign, ":imod", imod_thick),
        (try_end),
      (else_try),
        (eq, "$gekokujo_encounter_boss", "trp_shinano_rebel"),
        (store_random_in_range, ":mon_reward", 25, 100),
        (store_random_in_range, ":renown_reward", 0, 2),
        (try_begin),
          (eq, ":item", 0), #best
          (assign, ":item_id", "itm_hunter"),
          (assign, ":imod", imod_swaybacked),
        (else_try),
          (eq, ":item", 1), #medium
          (assign, ":item_id", "itm_gekokujo_yumi_5"),
          (assign, ":imod", imod_cracked),
        (else_try),
          #worst
          (assign, ":item_id", "itm_gekokujo_haori_2"),
          (assign, ":imod", imod_thick),
        (try_end),
      (else_try),
        (eq, "$gekokujo_encounter_boss", "trp_kinai_rebel"),
        (store_random_in_range, ":mon_reward", 25, 100),
        (store_random_in_range, ":renown_reward", 1, 4),
        (try_begin),
          (eq, ":item", 0), #best
          (assign, ":item_id", "itm_gekokujo_katana_2"),
          (assign, ":imod", imod_rusty),
        (else_try),
          (eq, ":item", 1), #medium
          (assign, ":item_id", "itm_gekokujo_okegawa_short_7"),
          (assign, ":imod", imod_battered),
        (else_try),
          #worst
          (assign, ":item_id", "itm_gekokujo_haori_3"),
          (assign, ":imod", imod_thick),
        (try_end),
      (else_try),
        (eq, "$gekokujo_encounter_boss", "trp_kanto_rebel"),
        (store_random_in_range, ":mon_reward", 25, 100),
        (store_random_in_range, ":renown_reward", 0, 2),
        (try_begin),
          (eq, ":item", 0), #best
          (assign, ":item_id", "itm_gekokujo_tachi_2"),
          (assign, ":imod", imod_rusty),
        (else_try),
          (eq, ":item", 1), #medium
          (assign, ":item_id", "itm_gekokujo_mogami_short_1"),
          (assign, ":imod", imod_battered),
        (else_try),
          #worst
          (assign, ":item_id", "itm_gekokujo_haori_4"),
          (assign, ":imod", imod_thick),
        (try_end),
      (else_try),
        (eq, "$gekokujo_encounter_boss", "trp_ronin_adventurer"),
        (store_random_in_range, ":mon_reward", 5, 20),
        (store_random_in_range, ":renown_reward", 1, 4),
        (try_begin),
          (eq, ":item", 0), #best
          (assign, ":item_id", "itm_gekokujo_nagamaki_2"),
          (assign, ":imod", imod_rusty),
        (else_try),
          (eq, ":item", 1), #medium
          (assign, ":item_id", "itm_gekokujo_hari_o_1"),
          (assign, ":imod", imod_rusty),
        (else_try),
          #worst
          (assign, ":item_id", "itm_gekokujo_hakama_6"),
          (assign, ":imod", imod_hardened),
        (try_end),
      (else_try),
        (eq, "$gekokujo_encounter_boss", "trp_ronin_protector"),
        (store_random_in_range, ":mon_reward", 50, 200),
        (store_random_in_range, ":renown_reward", 1, 5),
        (try_begin),
          (eq, ":item", 0), #best
          (assign, ":item_id", "itm_gekokujo_nagamaki_5"),
          (assign, ":imod", imod_chipped),
        (else_try),
          (eq, ":item", 1), #medium
          (assign, ":item_id", "itm_gekokujo_kabuto3_h_2"),
          (assign, ":imod", imod_battered),
        (else_try),
          #worst
          (assign, ":item_id", "itm_gekokujo_hakama_1"),
          (assign, ":imod", imod_hardened),
        (try_end),
      (else_try),
        (eq, "$gekokujo_encounter_boss", "trp_ronin_hero"),
        (store_random_in_range, ":mon_reward", 125, 500),
        (store_random_in_range, ":renown_reward", 2, 7),
        (try_begin),
          (eq, ":item", 0), #best
          (assign, ":item_id", "itm_gekokujo_nagamaki_9"),
          (assign, ":imod", 0),
        (else_try),
          (eq, ":item", 1), #medium
          (assign, ":item_id", "itm_gekokujo_zunari_m_2"),
          (assign, ":imod", imod_crude),
        (else_try),
          #worst
          (assign, ":item_id", "itm_gekokujo_hakama_2"),
          (assign, ":imod", imod_hardened),
        (try_end),
      (else_try),
        (eq, "$gekokujo_encounter_boss", "trp_onnabushi_veteran"),
        (store_random_in_range, ":mon_reward", 25, 100),
        (store_random_in_range, ":renown_reward", 1, 5),
        (try_begin),
          (eq, ":item", 0), #best
          (assign, ":item_id", "itm_gekokujo_naginata_2"),
          (assign, ":imod", imod_chipped),
        (else_try),
          (eq, ":item", 1), #medium
          (assign, ":item_id", "itm_gekokujo_yukinoshita_short_3"),
          (assign, ":imod", imod_battered),
        (else_try),
          #worst
          (assign, ":item_id", "itm_gekokujo_hakama_3"),
          (assign, ":imod", imod_hardened),
        (try_end),
      (else_try),
        (eq, "$gekokujo_encounter_boss", "trp_onnabushi_elite"),
        (store_random_in_range, ":mon_reward", 75, 300),
        (store_random_in_range, ":renown_reward", 2, 7),
        (try_begin),
          (eq, ":item", 0), #best
          (assign, ":item_id", "itm_gekokujo_naginata_4"),
          (assign, ":imod", 0),
        (else_try),
          (eq, ":item", 1), #medium
          (assign, ":item_id", "itm_gekokujo_hishinui_long_3"),
          (assign, ":imod", imod_crude),
        (else_try),
          #worst
          (assign, ":item_id", "itm_gekokujo_hakama_4"),
          (assign, ":imod", imod_hardened),
        (try_end),
      (else_try),
        (eq, "$gekokujo_encounter_boss", "trp_hired_agent_experienced"),
        (store_random_in_range, ":mon_reward", 50, 200),
        (store_random_in_range, ":renown_reward", 1, 5),
        (try_begin),
          (eq, ":item", 0), #best
          (assign, ":item_id", "itm_gekokujo_ninjato_3"),
          (assign, ":imod", 0),
        (else_try),
          (eq, ":item", 1), #medium
          (assign, ":item_id", "itm_gekokujo_tatami_short_4"),
          (assign, ":imod", imod_reinforced),
        (else_try),
          #worst
          (assign, ":item_id", "itm_gekokujo_kunai"),
          (assign, ":imod", 0),
        (try_end),
      (else_try),
        #trp_female_agent_experienced
        (store_random_in_range, ":mon_reward", 100, 400),
        (store_random_in_range, ":renown_reward", 1, 5),
        (try_begin),
          (eq, ":item", 0), #best
          (assign, ":item_id", "itm_gekokujo_ninjato_1"),
          (assign, ":imod", 0),
        (else_try),
          (eq, ":item", 1), #medium
          (assign, ":item_id", "itm_gekokujo_ninja_headwrap"),
          (assign, ":imod", imod_thick),
        (else_try),
          #worst
          (assign, ":item_id", "itm_gekokujo_shuriken"),
          (assign, ":imod", 0),
        (try_end),
      (try_end),
      
      #give the items
      (troop_add_item, "trp_player", ":item_id", ":imod"),
      (str_store_item_name, s11, ":item_id"),
      
      #give the money
      (call_script, "script_troop_add_gold", "trp_player", ":mon_reward"),
      (assign, reg32, ":mon_reward"),
      
      #50% to get the full (random) renown reward, 50% to get half (minimum 1)
      (try_begin),
        (gt, ":renown_reward", 0),
        (store_random_in_range, ":offset", 0, 2),
        (try_begin),
          (eq, ":offset", 0),
          (val_div, ":renown_reward", 2),
          (val_max, ":renown_reward", 1),
        (try_end),
        (call_script, "script_change_troop_renown", "trp_player", ":renown_reward"),
      (try_end),
      
      (store_random_in_range, ":offset", 0, 6),
      (val_add, ":offset", "str_gekokujo_encounter_win2_1"),
      (str_store_string, s4, ":offset"),
      (str_store_string, s3, "@{s3}^^{s4}"),
    ],
    [
      ("continue",[],"Continue...",
        [
          #(change_screen_return),
          (change_screen_map),
        ]),
    ],
  ),
  
  #mnu_encounter_lost is the lose screen with the amount of mon removed
  (
    "encounter_lost",mnf_disable_all_keys,
    "{s3}",
    "none",
    [
      (set_background_mesh, "mesh_gekokujo_pic_bandits_2"),
      
      (store_random_in_range, ":offset", 0, 10),
      (val_add, ":offset", "str_gekokujo_encounter_lose1_1"),
      (str_store_string, s3, ":offset"),
      
      #take 10% of player's gold
      (store_troop_gold, reg12, "trp_player"),
      (val_div, reg12, 10),
      (try_begin),
        (gt, reg12, 0),
        (troop_remove_gold, "trp_player", reg12),
        (str_store_string, s11, "@{reg12} mon"),
      (else_try),
        (str_store_string, s11, "@nothing"), #just in case there's nothing to take
      (try_end),
      
      (store_random_in_range, ":offset", 0, 6),
      (val_add, ":offset", "str_gekokujo_encounter_lose2_1"),
      (str_store_string, s4, ":offset"),
      (str_store_string, s3, "@{s3}^^{s4}"),
    ],
    [
      ("continue",[],"Continue...",
        [
          #(change_screen_return),
          (change_screen_map),
        ]),
    ],
  ),
  
  #mnu_encounter_end is the summary of a friendly encounter
  
  #gekokujo 3.1 random encounters end
  
  #gekokojo 3.1 begging start
  (
    "beg",0,
    "{s6}",
    "none",
    [
      (set_background_mesh, "mesh_pic_camp"),
      
      (try_begin),
        (eq, "$gekokujo_beg_result", 1), #the player succeeded
        
        (store_random_in_range, reg10, 0, 5), #begging from peasants usually gives poor yields
        (try_begin),
          (eq, reg10, 0),
          (store_random_in_range, reg10, 5, 50), #but there is a chance for a jackpot
        (try_end),
        (troop_add_gold, "trp_player", reg10),
        
        (str_store_string, s6, "str_gekokujo_beg_success"),
      (else_try),
        #(call_script, "script_change_player_relation_with_center", "$current_town", -1),
        (str_store_string, s6, "str_gekokujo_beg_fail"),
      (try_end),        
    ],
    [
      ("beg_continue", [], "Continue...", 
        [
          (rest_for_hours, 2, 2, 0),
          (change_screen_return),
        ]),
    ],
  ),
]
