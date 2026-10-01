# -*- coding: UTF-8 -*-
# split feature file: mission_templates - module
from aheader_operations import *
from header_common import *
from header_operations import *
from header_mission_templates import *
from header_animations import *
from header_sounds import *
from header_music import *
from header_items import *
from module_constants import *
from header_triggers import *
from header_terrain_types import * #gekokujo 3.0 no running away in sea battles
from ym_gatling import *
from header_skills import *
from header_skills import *
from module_mission_templates import af_castle_lord, bodyguard_triggers, caba_order_triggers, common_arena_fight_tab_press, common_battle_check_friendly_kills, common_battle_check_victory_condition, common_battle_init_banner, common_battle_inventory, common_battle_mission_start, common_battle_order_panel, common_battle_order_panel_tick, common_battle_tab_press, common_battle_victory_display, common_custom_battle_question_answered, common_custom_battle_tab_press, common_custom_siege_init, common_fade, common_gekokujo_sabakato_switch_check, common_gekokujo_siege_gate, common_gekokujo_siege_init, common_inventory_not_available, common_music_situation_update, common_siege_ai_trigger_init, common_siege_ai_trigger_init_2, common_siege_ai_trigger_init_after_2_secs, common_siege_assign_men_to_belfry, common_siege_attacker_do_not_stall, common_siege_attacker_reinforcement_check, common_siege_check_defeat_condition, common_siege_defender_reinforcement_archer_reposition, common_siege_defender_reinforcement_check, common_siege_init, common_siege_init_ai_and_belfry, common_siege_move_belfry, common_siege_question_answered, common_siege_refill_ammo, common_siege_rotate_belfry, custom_battle_check_defeat_condition, custom_battle_check_victory_condition, dplmc_battle_mode_triggers, multiplayer_battle_window_opened, multiplayer_once_at_the_first_frame, multiplayer_server_check_belfry_movement, multiplayer_server_check_end_map, multiplayer_server_check_polls, multiplayer_server_manage_bots, multiplayer_server_spawn_bots, pilgrim_disguise, prebattle_orders_triggers, tournament_triggers, trigger_cannon

mission_templates_siege = [
  (
    "besiege_inner_battle_town_center",mtf_battle_mode,-1,
    "You attack the walls of the castle...",
    [
     (0, mtef_attackers|mtef_use_exact_number|mtef_team_1,af_override_horse,aif_start_alarmed,4,[]),
     (2, mtef_defenders|mtef_use_exact_number|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
     (23, mtef_defenders|mtef_use_exact_number|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
     (24, mtef_defenders|mtef_use_exact_number|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
     (25, mtef_defenders|mtef_use_exact_number|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
     (26, mtef_defenders|mtef_use_exact_number|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
     (27, mtef_defenders|mtef_use_exact_number|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
     (28, mtef_defenders|mtef_use_exact_number|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
     ],
     trigger_cannon+
    [
      (ti_before_mission_start, 0, 0, [], [(call_script, "script_change_banners_and_chest")]),

      common_battle_tab_press,
      common_battle_init_banner,

      (ti_question_answered, 0, 0, [],
       [(store_trigger_param_1,":answer"),
        (eq,":answer",0),
        (assign, "$pin_player_fallen", 0),
        (str_store_string, s5, "str_retreat"),
        (call_script, "script_simulate_retreat", 5, 20, 0),
        (assign, "$g_battle_result", -1),
        (set_mission_result,-1),
        (call_script, "script_count_mission_casualties_from_agents"),
        (finish_mission,0),
        ]),
        
      (0, 0, ti_once, [], [(assign,"$g_battle_won",0),
                           #gekokujo 3.0 diplomacy deathcam deprecated start
                           ###diplomacy begin
                           #(assign, "$g_dplmc_cam_activated", 0),
                           #(assign, "$g_dplmc_charge_when_dead", 1),
                           ###diplomacy end
                           #gekokujo 3.0 diplomacy deathcam deprecated end
                           (call_script, "script_music_set_situation_with_culture", mtf_sit_ambushed),
                           ]),
      
      #AI Tiggers
      (0, 0, ti_once, [
          (assign, "$defender_team", 0),
          (assign, "$attacker_team", 1),
          (assign, "$defender_team_2", 2),
          (assign, "$attacker_team_2", 3),
          ], []),

      common_battle_check_friendly_kills,
      common_battle_check_victory_condition,
      common_battle_victory_display,

	  #gekokujo 3.0 mouselook death cam start
	  (1, 4, ti_once,
        [
            (main_hero_fallen),
            (assign, ":pteam_alive", 0), 
            (try_for_agents, ":agent"), #Check players team is dead
            (neq, ":pteam_alive", 1), #Break loop
            (agent_is_ally, ":agent"),
            (agent_is_alive, ":agent"),
                (assign, ":pteam_alive", 1),
            (try_end),
            (eq, ":pteam_alive", 0),
        ],
        [
            (assign, "$pin_player_fallen", 1),
            (display_message, "@Press TAB to end the battle."),
        ]),
	  #gekokujo 3.0 mouselook death cam end
#gekokujo 3.0 diplomacy deathcam deprecated start
#      (1, 4,
#      ##diplomacy begin
#      0,
#      ##diplomacy end
#      [(main_hero_fallen)],
#          [
#              ##diplomacy begin
#              (try_begin),
#                (eq, "$g_dplmc_battle_continuation", 0),
#                (assign, ":num_allies", 0),
#                (try_for_agents, ":agent"),
#                 (agent_is_ally, ":agent"),
#                 (agent_is_alive, ":agent"),
#                 (val_add, ":num_allies", 1),
#                (try_end),
#                (gt, ":num_allies", 0),
#                (try_begin),
#                  (eq, "$g_dplmc_cam_activated", 0),
#                  #(store_mission_timer_a, "$g_dplmc_main_hero_fallen_seconds"),
#                  (assign, "$g_dplmc_cam_activated", 1),
#                  (display_message, "@You have been knocked out by the enemy. Watch your men continue the fight without you or press Tab to retreat."),
#				  #gekokujo 3.0 mouselook deathcam no more control message
#                  #(display_message, "@To watch the fight you can use 'w, a, s, d, numpad_+/numpad_-' to move and 'numpad_1,2,3,4,6,8' to rotate the cam."),
#                (try_end),
#              (else_try),
#              ##diplomacy end
#              (assign, "$pin_player_fallen", 1),
#              (str_store_string, s5, "str_retreat"),
#              (call_script, "script_simulate_retreat", 10, 20, 1),
#              (assign, "$g_battle_result", -1),
#              (set_mission_result,-1),
#              (call_script, "script_count_mission_casualties_from_agents"),
#              (finish_mission,0),
#              ##diplomacy begin
#              (try_end),
#              ##diplomacy end
#            ]),
#gekokujo 3.0 diplomacy deathcam deprecated end

      common_battle_order_panel,
      common_battle_order_panel_tick,
      common_battle_inventory,
    ]
    ##diplomacy begin
    + dplmc_battle_mode_triggers,
    ##diplomacy end
  ),
  (
    "castle_attack_walls_defenders_sally",mtf_battle_mode|mtf_synch_inventory,-1,
    "You attack the walls of the castle...",
    [
     (0,mtef_attackers|mtef_team_1,af_override_horse,aif_start_alarmed,12,[]),
     (0,mtef_attackers|mtef_team_1,af_override_horse,aif_start_alarmed,0,[]),
     (3,mtef_defenders|mtef_team_0,af_override_horse,aif_start_alarmed,12,[]),
     (3,mtef_defenders|mtef_team_0,af_override_horse,aif_start_alarmed,0,[]),
     ],
     trigger_cannon+
    [
      (ti_on_agent_spawn, 0, 0, [],
       [
         (store_trigger_param_1, ":agent_no"),
         (call_script, "script_agent_reassign_team", ":agent_no"),
         ]),
 (0, 0, 0.1, [],
      [
        (try_for_agents, ":var_0"),
            (agent_is_alive, ":var_0"),
            (agent_is_human, ":var_0"),
            (agent_is_non_player, ":var_0"),
            (agent_get_horse, ":var_1", ":var_0"),
            (neg| ge, ":var_1", 0), # 
            (assign, ":var_2", 0),
            (assign, ":var_3", 0),
            (assign, ":var_4", 0),
            (assign, ":var_5", 0),
            (assign, ":var_6", 0),
            (assign, ":var_7", 0),
            (try_for_range, ":var_8", 0, 4),
                (agent_get_item_slot, ":var_9", ":var_0", ":var_8"),
                (gt, ":var_9", 0),
                (item_get_type, ":var_10", ":var_9"),
                (try_begin),
                    (eq, ":var_10", 4), # 
                    (assign, ":var_2", 1),
                    (assign, ":var_4", ":var_9"),
                (else_try),
                    (eq, ":var_10", 2), # 
                    (assign, ":var_3", 1),
                    (assign, ":var_5", ":var_9"),
                (else_try),
                    (eq, ":var_10", 3), # 
                    (assign, ":var_3", 1),
                    (assign, ":var_6", ":var_9"),
                (try_end),
            (try_end),
            (eq, ":var_2", 1), # 
            (eq, ":var_3", 1),
            (try_begin),
                (gt, ":var_5", 0),
                (eq, ":var_6", 0),
                (assign, ":var_7", ":var_5"),
            (else_try),
                (eq, ":var_5", 0),
                (gt, ":var_6", 0),
                (assign, ":var_7", ":var_6"),
            (else_try),
                (gt, ":var_5", 0),
                (gt, ":var_6", 0),
                (agent_get_troop_id, ":var_11", ":var_0"),
                (store_proficiency_level, ":var_12", ":var_11", wpt_one_handed_weapon),
                (store_proficiency_level, ":var_13", ":var_11", wpt_two_handed_weapon),
                (store_sub, ":var_14", ":var_13", ":var_12"),
                (try_begin),
                    (ge, ":var_14", 0),
                    (assign, ":var_7", ":var_6"),
                (else_try),
                    (assign, ":var_7", ":var_5"),
                (try_end),
            (try_end),
            (agent_get_team, ":var_15", ":var_0"),
            (agent_get_position, pos34, ":var_0"),
            (assign, ":var_16", 3000),
            (try_for_agents, ":var_17"),
                (agent_is_alive, ":var_17"),
                (agent_is_human, ":var_17"),
                (agent_get_team, ":var_18", ":var_17"),
                (teams_are_enemies, ":var_18", ":var_15"),
                (agent_get_position, pos36, ":var_17"),
                (get_distance_between_positions, ":var_19", pos36, pos34),
                (neg| ge, ":var_19", ":var_16"), # 
                (assign, ":var_16", ":var_19"),
            (try_end),
            (set_fixed_point_multiplier, 100),
            (agent_get_speed, pos35, ":var_0"),
            (position_get_y, ":var_20", pos35),
            (convert_from_fixed_point, ":var_20"),
            (agent_get_wielded_item, ":var_21", ":var_0"),
            (gt, ":var_21", 0),
            (item_get_type, ":var_22", ":var_21"),
            (try_begin),
                (neg| ge, ":var_16", 100), #
                (neg| gt, ":var_20", 1), # 
                (eq, ":var_22", 4),
                (agent_set_wielded_item, ":var_0", ":var_7"),
            (else_try),
                (this_or_next| gt, ":var_20", 2), # 
                (gt, ":var_16", 200),
                (this_or_next| eq, ":var_22", 2), # 
                (eq, ":var_22", 3),
                (agent_set_wielded_item, ":var_0", ":var_4"),
            (try_end),
        (try_end),
      ]),     
      (ti_before_mission_start, 0, 0, [],
       [
         (team_set_relation, 0, 2, 1),
         (team_set_relation, 1, 3, 1),
         (call_script, "script_change_banners_and_chest"),
         (call_script, "script_remove_siege_objects"),
		 #gekokujo 3.1 siege improvement start
		 #open the gates in visit mode
		 #(replace_scene_props, "spr_gekokujo_c2_gate_large", "spr_empty"), #this is inelegant, but can replace all of below
		 #(set_fixed_point_multiplier, 100),
		 (scene_prop_get_num_instances, ":num_gates", "spr_gekokujo_c2_gate_large"),  #count number of gates
		 (try_for_range, ":gate_no", 0, ":num_gates"), #go through each gate instance
		   (scene_prop_get_instance, ":gate_id", "spr_gekokujo_c2_gate_large", ":gate_no"), #find the gate instance's id
		   (prop_instance_get_variation_id, ":var1", ":gate_id"), #find the instance's gate number (the var1 set in edit mode)
		   (neq, ":var1", 0), #gates with a var1 of 0 (default) are only decorative and should be ignored
		   
		   #(prop_instance_get_position, pos1, ":gate_id"), #absolute position of gate to pos1
		   #(prop_instance_get_scale, pos2, ":gate_id"), #get scale of gate to pos2
		   #(position_get_scale_x, ":width", pos2), #get scale of x axis to find width
           #(init_position, pos3),
		   #(position_set_x, pos3, ":width"), #move pos3 on x axis by width
		   #(try_begin),
		   #  (gt, ":width", 0), #width was a positive number, it must be the left gate
		   #  (position_set_y, pos3, ":width"), #move pos3 on y axis by width
		   #  (position_rotate_z, pos1, 90), #rotate pos3 on z axis by 90 degrees
		   #(else_try),
		   #  #width was a negative number, it must be the right gate
		   #  (store_sub, ":width", 0, ":width"), #find the negative of width
		   #  (position_set_y, pos3, ":width"), #move pos3 on y axis by the negative of width
		   #  (position_rotate_z, pos1, -90), #rotate pos3 on z axis by -90 degrees
		   #(try_end),
		   #(position_transform_position_to_parent, pos4, pos1, pos3), #get absolute position of pos3 relative from pos1 to pos4
		   #(prop_instance_animate_to_position, ":gate_id", pos4, 1), #start with the gate open
           (call_script, "script_gekokujo_open_gate", ":gate_id", 1), #open instantly
		 (try_end),
		 #gekokujo 3.1 siege improvement end
         ]),

      common_battle_tab_press,
      common_battle_init_banner,

      (ti_on_agent_killed_or_wounded, 0, 0, [], #new
       [
        (store_trigger_param_1, ":dead_agent_no"),
        (store_trigger_param_2, ":killer_agent_no"),
        (store_trigger_param_3, ":is_wounded"),

        (try_begin),
          (ge, ":dead_agent_no", 0),
          (neg|agent_is_ally, ":dead_agent_no"),
          (agent_is_human, ":dead_agent_no"),
          (agent_get_troop_id, ":dead_agent_troop_id", ":dead_agent_no"),
          (str_store_troop_name, s6, ":dead_agent_troop_id"),
          (assign, reg0, ":dead_agent_no"),
          (assign, reg1, ":killer_agent_no"),
          (assign, reg2, ":is_wounded"),
          (agent_get_team, reg3, ":dead_agent_no"),          
          #(display_message, "@{!}dead agent no : {reg0} ; killer agent no : {reg1} ; is_wounded : {reg2} ; dead agent team : {reg3} ; {s6} is added"), 
          (party_add_members, "p_total_enemy_casualties", ":dead_agent_troop_id", 1), #addition_to_p_total_enemy_casualties
          (eq, ":is_wounded", 1),
          (party_wound_members, "p_total_enemy_casualties", ":dead_agent_troop_id", 1), 
        (try_end),
       ]),

      (ti_question_answered, 0, 0, [],
       [(store_trigger_param_1,":answer"),
        (eq,":answer",0),
        (assign, "$pin_player_fallen", 0),
        (str_store_string, s5, "str_retreat"),
        (call_script, "script_simulate_retreat", 5, 20, 0),
        (call_script, "script_count_mission_casualties_from_agents"),
        (finish_mission,0),]),
        
      (0, 0, ti_once, [], [(assign,"$g_battle_won",0),
                           #gekokujo 3.0 diplomacy deathcam deprecated start
                           ###diplomacy begin
                           #(assign, "$g_dplmc_cam_activated", 0),
                           #(assign, "$g_dplmc_charge_when_dead", 1),
                           ###diplomacy end
                           #gekokujo 3.0 diplomacy deathcam deprecated end
                           (call_script, "script_combat_music_set_situation_with_culture"),
                           ]),
      
      common_music_situation_update,
      common_battle_check_friendly_kills,

      (1, 60, ti_once, [(store_mission_timer_a, reg(1)),
                        (ge, reg(1), 10),
                        (all_enemies_defeated, 2),
                        (neg|main_hero_fallen,0),
                        (set_mission_result,1),
                        (display_message,"str_msg_battle_won"),
                        (assign, "$g_battle_won", 1),
                        (assign, "$g_battle_result", 1),
                        (assign, "$g_siege_sallied_out_once", 1),
                        (assign, "$g_siege_method", 1), #reset siege timer
                        (call_script, "script_play_victorious_sound"),
                        ],
           [(call_script, "script_count_mission_casualties_from_agents"),
            (finish_mission,1)]),

      common_battle_victory_display,

	  #gekokujo 3.0 mouselook death cam start
	  (1, 4, ti_once,
        [
            (main_hero_fallen),
            (assign, ":pteam_alive", 0), 
            (try_for_agents, ":agent"), #Check players team is dead
            (neq, ":pteam_alive", 1), #Break loop
            (agent_is_ally, ":agent"),
            (agent_is_alive, ":agent"),
                (assign, ":pteam_alive", 1),
            (try_end),
            (eq, ":pteam_alive", 0),
        ],
        [
            (assign, "$pin_player_fallen", 1),
            (display_message, "@Press TAB to end the battle."),
        ]),
	  #gekokujo 3.0 mouselook death cam end
#gekokujo 3.0 diplomacy deathcam deprecated start
#      (1, 4,
#      ##diplomacy begin
#      0,
#      ##diplomacy end
#      [(main_hero_fallen)],
#          [
#              ##diplomacy begin
#              (try_begin),
#                (eq, "$g_dplmc_battle_continuation", 0),
#                (assign, ":num_allies", 0),
#                (try_for_agents, ":agent"),
#                 (agent_is_ally, ":agent"),
#                 (agent_is_alive, ":agent"),
#                 (val_add, ":num_allies", 1),
#                (try_end),
#                (gt, ":num_allies", 0),
#                (try_begin),
#                  (eq, "$g_dplmc_cam_activated", 0),
#                  #(store_mission_timer_a, "$g_dplmc_main_hero_fallen_seconds"),
#                  (assign, "$g_dplmc_cam_activated", 1),
#                  (display_message, "@You have been knocked out by the enemy. Watch your men continue the fight without you or press Tab to retreat."),
#				  #gekokujo 3.0 mouselook deathcam no more control message
#                  #(display_message, "@To watch the fight you can use 'w, a, s, d, numpad_+/numpad_-' to move and 'numpad_1,2,3,4,6,8' to rotate the cam."),
#                (try_end),
#              (else_try),
#              ##diplomacy end
#              (assign, "$pin_player_fallen", 1),
#              (str_store_string, s5, "str_retreat"),
#              (call_script, "script_simulate_retreat", 10, 20, 1),
#              (assign, "$g_battle_result", -1),
#              (set_mission_result,-1),
#              (call_script, "script_count_mission_casualties_from_agents"),
#              (finish_mission,0),
#              ##diplomacy begin
#              (try_end),
#              ##diplomacy end
#            ]),
#gekokujo 3.0 diplomacy deathcam deprecated end

      common_battle_order_panel,
      common_battle_order_panel_tick,
      common_battle_inventory,
    ]
    ##diplomacy begin
    + dplmc_battle_mode_triggers,
    ##diplomacy end
  ),
  (
    "castle_attack_walls_belfry",mtf_battle_mode|mtf_synch_inventory,-1,
    "You attack the walls of the castle...",
    [
     (0,mtef_attackers|mtef_team_1,af_override_horse,aif_start_alarmed,12,[]),
     (0,mtef_attackers|mtef_team_1,af_override_horse,aif_start_alarmed,0,[]),
     (10,mtef_defenders|mtef_team_0,af_override_horse,aif_start_alarmed,0,[]),
     (11,mtef_defenders|mtef_team_0,af_override_horse,aif_start_alarmed,7,[]),
     (15,mtef_defenders|mtef_team_0,af_override_horse,aif_start_alarmed,0,[]),

     (40,mtef_defenders|mtef_team_0|mtef_archers_first,af_override_horse,aif_start_alarmed,1,[]),
     (41,mtef_defenders|mtef_team_0|mtef_archers_first,af_override_horse,aif_start_alarmed,1,[]),
     (42,mtef_defenders|mtef_team_0|mtef_archers_first,af_override_horse,aif_start_alarmed,1,[]),
     (43,mtef_defenders|mtef_team_0|mtef_archers_first,af_override_horse,aif_start_alarmed,1,[]),
     (44,mtef_defenders|mtef_team_0|mtef_archers_first,af_override_horse,aif_start_alarmed,1,[]),
     (45,mtef_defenders|mtef_team_0|mtef_archers_first,af_override_horse,aif_start_alarmed,1,[]),
     (46,mtef_defenders|mtef_team_0|mtef_archers_first,af_override_horse,aif_start_alarmed,1,[]),
     (47,mtef_defenders|mtef_team_0|mtef_archers_first,af_override_horse,aif_start_alarmed,1,[]),
     ],
     trigger_cannon+
    [
      common_battle_mission_start,
      common_battle_tab_press,
      common_battle_init_banner,
      common_siege_question_answered,
      common_siege_init,
      common_music_situation_update,
      common_siege_ai_trigger_init,
      common_siege_ai_trigger_init_2,

      (0, 0, ti_once,
       [
         (set_show_messages, 0),
         (team_give_order, "$attacker_team", grc_everyone, mordr_spread_out),
         (team_give_order, "$attacker_team", grc_everyone, mordr_spread_out),
         (team_give_order, "$attacker_team", grc_everyone, mordr_spread_out),
         (set_show_messages, 1),
         ], []),
      
      (ti_on_agent_killed_or_wounded, 0, 0, [],
       [
        (store_trigger_param_1, ":dead_agent_no"),
        (store_trigger_param_2, ":killer_agent_no"),
        (store_trigger_param_3, ":is_wounded"),

        (try_begin),
          (ge, ":dead_agent_no", 0),
          (neg|agent_is_ally, ":dead_agent_no"),
          (agent_is_human, ":dead_agent_no"),
          (agent_get_troop_id, ":dead_agent_troop_id", ":dead_agent_no"),
          (str_store_troop_name, s6, ":dead_agent_troop_id"),
          (assign, reg0, ":dead_agent_no"),
          (assign, reg1, ":killer_agent_no"),
          (assign, reg2, ":is_wounded"),
          (agent_get_team, reg3, ":dead_agent_no"),          
          #(display_message, "@{!}dead agent no : {reg0} ; killer agent no : {reg1} ; is_wounded : {reg2} ; dead agent team : {reg3} ; {s6} is added"), 
          (party_add_members, "p_total_enemy_casualties", ":dead_agent_troop_id", 1), #addition_to_p_total_enemy_casualties
          (eq, ":is_wounded", 1),
          (party_wound_members, "p_total_enemy_casualties", ":dead_agent_troop_id", 1), 
        (try_end),
       ]),
 (0, 0, 0.1, [],
      [
        (try_for_agents, ":var_0"),
            (agent_is_alive, ":var_0"),
            (agent_is_human, ":var_0"),
            (agent_is_non_player, ":var_0"),
            (agent_get_horse, ":var_1", ":var_0"),
            (neg| ge, ":var_1", 0), # 
            (assign, ":var_2", 0),
            (assign, ":var_3", 0),
            (assign, ":var_4", 0),
            (assign, ":var_5", 0),
            (assign, ":var_6", 0),
            (assign, ":var_7", 0),
            (try_for_range, ":var_8", 0, 4),
                (agent_get_item_slot, ":var_9", ":var_0", ":var_8"),
                (gt, ":var_9", 0),
                (item_get_type, ":var_10", ":var_9"),
                (try_begin),
                    (eq, ":var_10", 4), # 
                    (assign, ":var_2", 1),
                    (assign, ":var_4", ":var_9"),
                (else_try),
                    (eq, ":var_10", 2), # 
                    (assign, ":var_3", 1),
                    (assign, ":var_5", ":var_9"),
                (else_try),
                    (eq, ":var_10", 3), # 
                    (assign, ":var_3", 1),
                    (assign, ":var_6", ":var_9"),
                (try_end),
            (try_end),
            (eq, ":var_2", 1), # 
            (eq, ":var_3", 1),
            (try_begin),
                (gt, ":var_5", 0),
                (eq, ":var_6", 0),
                (assign, ":var_7", ":var_5"),
            (else_try),
                (eq, ":var_5", 0),
                (gt, ":var_6", 0),
                (assign, ":var_7", ":var_6"),
            (else_try),
                (gt, ":var_5", 0),
                (gt, ":var_6", 0),
                (agent_get_troop_id, ":var_11", ":var_0"),
                (store_proficiency_level, ":var_12", ":var_11", wpt_one_handed_weapon),
                (store_proficiency_level, ":var_13", ":var_11", wpt_two_handed_weapon),
                (store_sub, ":var_14", ":var_13", ":var_12"),
                (try_begin),
                    (ge, ":var_14", 0),
                    (assign, ":var_7", ":var_6"),
                (else_try),
                    (assign, ":var_7", ":var_5"),
                (try_end),
            (try_end),
            (agent_get_team, ":var_15", ":var_0"),
            (agent_get_position, pos34, ":var_0"),
            (assign, ":var_16", 3000),
            (try_for_agents, ":var_17"),
                (agent_is_alive, ":var_17"),
                (agent_is_human, ":var_17"),
                (agent_get_team, ":var_18", ":var_17"),
                (teams_are_enemies, ":var_18", ":var_15"),
                (agent_get_position, pos36, ":var_17"),
                (get_distance_between_positions, ":var_19", pos36, pos34),
                (neg| ge, ":var_19", ":var_16"), # 
                (assign, ":var_16", ":var_19"),
            (try_end),
            (set_fixed_point_multiplier, 100),
            (agent_get_speed, pos35, ":var_0"),
            (position_get_y, ":var_20", pos35),
            (convert_from_fixed_point, ":var_20"),
            (agent_get_wielded_item, ":var_21", ":var_0"),
            (gt, ":var_21", 0),
            (item_get_type, ":var_22", ":var_21"),
            (try_begin),
                (neg| ge, ":var_16", 100), #
                (neg| gt, ":var_20", 1), # 
                (eq, ":var_22", 4),
                (agent_set_wielded_item, ":var_0", ":var_7"),
            (else_try),
                (this_or_next| gt, ":var_20", 2), # 
                (gt, ":var_16", 200),
                (this_or_next| eq, ":var_22", 2), # 
                (eq, ":var_22", 3),
                (agent_set_wielded_item, ":var_0", ":var_4"),
            (try_end),
        (try_end),
      ]),      
  

      common_siege_ai_trigger_init_after_2_secs,
      common_siege_defender_reinforcement_check,
      common_siege_defender_reinforcement_archer_reposition,
      common_siege_attacker_reinforcement_check,
      common_siege_attacker_do_not_stall,
      common_battle_check_friendly_kills,
      common_battle_check_victory_condition,
      common_battle_victory_display,
      common_siege_refill_ammo,
      common_siege_check_defeat_condition,
      common_battle_order_panel,
      common_battle_order_panel_tick,
      common_inventory_not_available,
      common_siege_init_ai_and_belfry,
      common_siege_move_belfry,
      common_siege_rotate_belfry,
      common_siege_assign_men_to_belfry,
    ]
    ##diplomacy begin
    + dplmc_battle_mode_triggers,
    ##diplomacy end
  ),
  (
    "castle_attack_walls_ladder",mtf_battle_mode|mtf_synch_inventory,-1,
    "You attack the walls of the castle...",
    [
     (0,mtef_attackers|mtef_team_1,af_override_horse,aif_start_alarmed,12,[]),
     (0,mtef_attackers|mtef_team_1,af_override_horse,aif_start_alarmed,0,[]),
     (10,mtef_defenders|mtef_team_0,af_override_horse,aif_start_alarmed,0,[]),
     (11,mtef_defenders|mtef_team_0,af_override_horse,aif_start_alarmed,7,[]),
     (15,mtef_defenders|mtef_team_0,af_override_horse,aif_start_alarmed,0,[]),

     (40,mtef_defenders|mtef_team_0|mtef_archers_first,af_override_horse,aif_start_alarmed,1,[]),
     (41,mtef_defenders|mtef_team_0|mtef_archers_first,af_override_horse,aif_start_alarmed,1,[]),
     (42,mtef_defenders|mtef_team_0|mtef_archers_first,af_override_horse,aif_start_alarmed,1,[]),
     (43,mtef_defenders|mtef_team_0|mtef_archers_first,af_override_horse,aif_start_alarmed,1,[]),
     (44,mtef_defenders|mtef_team_0|mtef_archers_first,af_override_horse,aif_start_alarmed,1,[]),
     (45,mtef_defenders|mtef_team_0|mtef_archers_first,af_override_horse,aif_start_alarmed,1,[]),
     (46,mtef_defenders|mtef_team_0|mtef_archers_first,af_override_horse,aif_start_alarmed,1,[]),
     ],
     trigger_cannon+
    [
      common_battle_mission_start,
      common_battle_tab_press,
      common_battle_init_banner,
      common_siege_question_answered,
      common_siege_init,
      common_music_situation_update,
      common_siege_ai_trigger_init,
      common_siege_ai_trigger_init_2,
      common_siege_ai_trigger_init_after_2_secs,
      common_siege_defender_reinforcement_check,
      common_siege_defender_reinforcement_archer_reposition,
      common_siege_attacker_reinforcement_check,
      common_siege_attacker_do_not_stall,
      common_battle_check_friendly_kills,
      common_battle_check_victory_condition,
      common_battle_victory_display,
      common_siege_refill_ammo,
      common_siege_check_defeat_condition,
      common_battle_order_panel,
      common_battle_order_panel_tick,
      common_inventory_not_available,
	  
	  #gekokujo 3.1 siege improvement start
	  common_gekokujo_siege_init,
	  common_gekokujo_siege_gate,
	  #common_gekokujo_siege_aggression,
	  #gekokujo 3.1 siege improvement end

      (ti_on_agent_killed_or_wounded, 0, 0, [],
       [
        (store_trigger_param_1, ":dead_agent_no"),
        (store_trigger_param_2, ":killer_agent_no"),
        (store_trigger_param_3, ":is_wounded"),

        (try_begin),
          (ge, ":dead_agent_no", 0),
          (neg|agent_is_ally, ":dead_agent_no"),
          (agent_is_human, ":dead_agent_no"),
          (agent_get_troop_id, ":dead_agent_troop_id", ":dead_agent_no"),
          (str_store_troop_name, s6, ":dead_agent_troop_id"),
          (assign, reg0, ":dead_agent_no"),
          (assign, reg1, ":killer_agent_no"),
          (assign, reg2, ":is_wounded"),
          (agent_get_team, reg3, ":dead_agent_no"),          
          #(display_message, "@{!}dead agent no : {reg0} ; killer agent no : {reg1} ; is_wounded : {reg2} ; dead agent team : {reg3} ; {s6} is added"), 
          (party_add_members, "p_total_enemy_casualties", ":dead_agent_troop_id", 1), #addition_to_p_total_enemy_casualties
          (eq, ":is_wounded", 1),
          (party_wound_members, "p_total_enemy_casualties", ":dead_agent_troop_id", 1), 
        (try_end),
       ]),
(0, 0, 0.1, [],
      [
        (try_for_agents, ":var_0"),
            (agent_is_alive, ":var_0"),
            (agent_is_human, ":var_0"),
            (agent_is_non_player, ":var_0"),
            (agent_get_horse, ":var_1", ":var_0"),
            (neg| ge, ":var_1", 0), # 
            (assign, ":var_2", 0),
            (assign, ":var_3", 0),
            (assign, ":var_4", 0),
            (assign, ":var_5", 0),
            (assign, ":var_6", 0),
            (assign, ":var_7", 0),
            (try_for_range, ":var_8", 0, 4),
                (agent_get_item_slot, ":var_9", ":var_0", ":var_8"),
                (gt, ":var_9", 0),
                (item_get_type, ":var_10", ":var_9"),
                (try_begin),
                    (eq, ":var_10", 4), # 
                    (assign, ":var_2", 1),
                    (assign, ":var_4", ":var_9"),
                (else_try),
                    (eq, ":var_10", 2), # 
                    (assign, ":var_3", 1),
                    (assign, ":var_5", ":var_9"),
                (else_try),
                    (eq, ":var_10", 3), # 
                    (assign, ":var_3", 1),
                    (assign, ":var_6", ":var_9"),
                (try_end),
            (try_end),
            (eq, ":var_2", 1), # 
            (eq, ":var_3", 1),
            (try_begin),
                (gt, ":var_5", 0),
                (eq, ":var_6", 0),
                (assign, ":var_7", ":var_5"),
            (else_try),
                (eq, ":var_5", 0),
                (gt, ":var_6", 0),
                (assign, ":var_7", ":var_6"),
            (else_try),
                (gt, ":var_5", 0),
                (gt, ":var_6", 0),
                (agent_get_troop_id, ":var_11", ":var_0"),
                (store_proficiency_level, ":var_12", ":var_11", wpt_one_handed_weapon),
                (store_proficiency_level, ":var_13", ":var_11", wpt_two_handed_weapon),
                (store_sub, ":var_14", ":var_13", ":var_12"),
                (try_begin),
                    (ge, ":var_14", 0),
                    (assign, ":var_7", ":var_6"),
                (else_try),
                    (assign, ":var_7", ":var_5"),
                (try_end),
            (try_end),
            (agent_get_team, ":var_15", ":var_0"),
            (agent_get_position, pos34, ":var_0"),
            (assign, ":var_16", 3000),
            (try_for_agents, ":var_17"),
                (agent_is_alive, ":var_17"),
                (agent_is_human, ":var_17"),
                (agent_get_team, ":var_18", ":var_17"),
                (teams_are_enemies, ":var_18", ":var_15"),
                (agent_get_position, pos36, ":var_17"),
                (get_distance_between_positions, ":var_19", pos36, pos34),
                (neg| ge, ":var_19", ":var_16"), # 
                (assign, ":var_16", ":var_19"),
            (try_end),
            (set_fixed_point_multiplier, 100),
            (agent_get_speed, pos35, ":var_0"),
            (position_get_y, ":var_20", pos35),
            (convert_from_fixed_point, ":var_20"),
            (agent_get_wielded_item, ":var_21", ":var_0"),
            (gt, ":var_21", 0),
            (item_get_type, ":var_22", ":var_21"),
            (try_begin),
                (neg| ge, ":var_16", 100), #
                (neg| gt, ":var_20", 1), # 
                (eq, ":var_22", 4),
                (agent_set_wielded_item, ":var_0", ":var_7"),
            (else_try),
                (this_or_next| gt, ":var_20", 2), # 
                (gt, ":var_16", 200),
                (this_or_next| eq, ":var_22", 2), # 
                (eq, ":var_22", 3),
                (agent_set_wielded_item, ":var_0", ":var_4"),
            (try_end),
        (try_end),
      ]),
##      (15, 0, 0,
##       [
##         (get_player_agent_no, ":player_agent"),
##         (agent_get_team, ":agent_team", ":player_agent"),
##         (neq, "$attacker_team", ":agent_team"),
##         (assign, ":non_ranged", 0),
##         (assign, ":ranged", 0),
##         (assign, ":ranged_pos_x", 0),
##         (assign, ":ranged_pos_y", 0),
##         (set_fixed_point_multiplier, 100),
##         (try_for_agents, ":agent_no"),
##           (eq, ":non_ranged", 0),
##           (agent_is_human, ":agent_no"),
##           (agent_is_alive, ":agent_no"),
##           (neg|agent_is_defender, ":agent_no"),
##           (agent_get_class, ":agent_class", ":agent_no"),
##           (try_begin),
##             (neq, ":agent_class", grc_archers),
##             (val_add, ":non_ranged", 1),
##           (else_try),
##             (val_add, ":ranged", 1),
##             (agent_get_position, pos0, ":agent_no"),
##             (position_get_x, ":pos_x", pos0),
##             (position_get_y, ":pos_y", pos0),
##             (val_add, ":ranged_pos_x", ":pos_x"),
##             (val_add, ":ranged_pos_y", ":pos_y"),
##           (try_end),
##         (try_end),
##         (try_begin),
##           (eq, ":non_ranged", 0),
##           (gt, ":ranged", 0),
##           (val_div, ":ranged_pos_x", ":ranged"),
##           (val_div, ":ranged_pos_y", ":ranged"),
##           (entry_point_get_position, pos0, 10),
##           (init_position, pos1),
##           (position_set_x, pos1, ":ranged_pos_x"),
##           (position_set_y, pos1, ":ranged_pos_y"),
##           (position_get_z, ":pos_z", pos0),
##           (position_set_z, pos1, ":pos_z"),
##           (get_distance_between_positions, ":dist", pos0, pos1),
##           (gt, ":dist", 1000), #average position of archers is more than 10 meters far from entry point 10
##           (team_give_order, "$attacker_team", grc_archers, mordr_hold),
##           (team_set_order_position, "$attacker_team", grc_archers, pos0),
##         (else_try),
##           (team_give_order, "$attacker_team", grc_everyone, mordr_charge),
##         (try_end),
##         ],
##       []),
    ]
    ##diplomacy begin
    + dplmc_battle_mode_triggers,
    ##diplomacy end
  ),
  (
    "quick_battle_siege", mtf_battle_mode,-1,
    "You lead your men to battle.",
    [
      (0,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
      (1,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
      (2,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
      (3,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
      (4,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
      (5,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
      (6,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
      (7,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),

      (8,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
      (9,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
      (10,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
      (11,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
      (12,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
      (13,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
      (14,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
      (15,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),

      (16,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
      (17,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
      (18,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
      (19,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
      (20,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
      (21,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
      (22,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
      (23,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),

      (24,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
      (25,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
      (26,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
      (27,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
      (28,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
      (29,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
      (30,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
      (31,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),

      (32,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
      (33,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
      (34,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
      (35,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
      (36,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
      (37,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
      (38,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
      (39,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),

      (40,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
      (41,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
      (42,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
      (43,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
      (44,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
      (45,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
      (46,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
      (47,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
     ],
     trigger_cannon+
    [
	  common_battle_mission_start,
      common_battle_init_banner,

      (0, 0, ti_once,
       [
         (assign, "$defender_team", 0),
         (assign, "$attacker_team", 1),
         (assign, "$defender_team_2", 2),
         (assign, "$attacker_team_2", 3),
         ], []),

      (ti_before_mission_start, 0, 0, [],
       [
         (scene_set_day_time, 15),
         ]),

      common_custom_battle_tab_press,
      common_custom_battle_question_answered,
      common_inventory_not_available,
      common_custom_siege_init,
      common_music_situation_update,
      custom_battle_check_victory_condition,
      common_battle_victory_display,
      custom_battle_check_defeat_condition,
      common_siege_attacker_do_not_stall,
      common_siege_refill_ammo,
      common_siege_init_ai_and_belfry,
      common_siege_move_belfry,
      common_siege_rotate_belfry,
      common_siege_assign_men_to_belfry,
      common_siege_ai_trigger_init_2,
      ],
    ),
##
##  (
##    "quick_battle_siege_offense",mtf_battle_mode,-1,
##    "You lead your men to battle.",
##    [
##      (0,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
##      (1,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
##      (2,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
##      (3,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
##      (4,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
##      (5,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
##      (6,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
##      (7,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
##
##      (8,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
##      (9,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
##      (10,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
##
##      (11,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
##      (12,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
##      (13,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
##      (14,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
##      (15,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
##      (40,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
##      (41,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
##      (42,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
##      (43,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
##      (44,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
##      (45,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
##      (46,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
##      (47,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
##
##     ],
##    [
##      common_custom_battle_tab_press,
##      common_battle_init_banner,
##      common_custom_battle_question_answered,
##      common_custom_siege_init,
##      common_inventory_not_available,
##      common_music_situation_update,
##      custom_battle_check_victory_condition,
##      common_battle_victory_display,
##      custom_battle_check_defeat_condition,
##      
##      (0, 0, ti_once,
##       [
##         (assign, "$defender_team", 0),
##         (assign, "$attacker_team", 1),
##         (assign, "$defender_team_2", 2),
##         (assign, "$attacker_team_2", 3),
##         ], []),
##
##      common_siege_ai_trigger_init_2,
##      common_siege_attacker_do_not_stall,
##      common_siege_refill_ammo,
##      common_siege_init_ai_and_belfry,
##      common_siege_move_belfry,
##      common_siege_rotate_belfry,
##      common_siege_assign_men_to_belfry,
##    ],
##  ),

    (
    "multiplayer_dm",mtf_battle_mode,-1, #deathmatch mode
    "You lead your men to battle.",
    [
      (0,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (1,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (2,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (3,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (4,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (5,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (6,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (7,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),

      (8,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (9,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (10,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (11,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (12,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (13,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (14,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (15,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),

      (16,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (17,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (18,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (19,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (20,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (21,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (22,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (23,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),

      (24,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (25,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (26,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (27,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (28,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (29,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (30,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (31,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),

      (32,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (33,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (34,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (35,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (36,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (37,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (38,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (39,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),

      (40,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (41,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (42,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (43,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (44,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (45,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (46,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (47,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),

      (48,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (49,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (50,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (51,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (52,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (53,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (54,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (55,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),

      (56,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (57,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (58,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (59,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (60,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (61,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (62,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (63,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
     ],
    [
      #multiplayer_server_check_belfry_movement,      
     
      multiplayer_server_check_polls,

      (ti_on_agent_spawn, 0, 0, [],
       [
         (store_trigger_param_1, ":agent_no"),
         (call_script, "script_multiplayer_server_on_agent_spawn_common", ":agent_no"),
         ]),

      (ti_server_player_joined, 0, 0, [],
       [
         (store_trigger_param_1, ":player_no"),
         (call_script, "script_multiplayer_server_player_joined_common", ":player_no"),
         ]),

      (ti_before_mission_start, 0, 0, [],
       [
         (assign, "$g_multiplayer_game_type", multiplayer_game_type_deathmatch),
         (call_script, "script_multiplayer_server_before_mission_start_common"),
         
         (multiplayer_make_everyone_enemy),

         (call_script, "script_multiplayer_init_mission_variables"),
         (call_script, "script_multiplayer_remove_destroy_mod_targets"),
         (call_script, "script_multiplayer_remove_headquarters_flags"), # close this line and open map in deathmatch mod and use all ladders firstly 
         ]),                                                            # to be able to edit maps without damaging any headquarters flags ext. 

      (ti_after_mission_start, 0, 0, [], 
       [
         (set_spawn_effector_scene_prop_kind, 0, -1), #during this mission, agents of "team 0" will try to spawn around scene props with kind equal to -1(no effector for this mod)
         (set_spawn_effector_scene_prop_kind, 1, -1), #during this mission, agents of "team 1" will try to spawn around scene props with kind equal to -1(no effector for this mod)

         (call_script, "script_initialize_all_scene_prop_slots"),
         
         (call_script, "script_multiplayer_move_moveable_objects_initial_positions"),

         (assign, "$g_multiplayer_ready_for_spawning_agent", 1),
         ]),

      (ti_on_multiplayer_mission_end, 0, 0, [],
       [
         #ELITE_WARRIOR achievement
         (try_begin),
           (multiplayer_get_my_player, ":my_player_no"),
           (is_between, ":my_player_no", 0, multiplayer_max_possible_player_id),
           (player_get_team_no, ":my_player_team", ":my_player_no"),
           (lt, ":my_player_team", multi_team_spectator),
           (player_get_kill_count, ":kill_count", ":my_player_no"),
           (player_get_death_count, ":death_count", ":my_player_no"),
           (store_mul, ":my_score_plus_death", ":kill_count", 1000),
           (val_sub, ":my_score_plus_death", ":death_count"),
           (assign, ":continue", 1),
           (get_max_players, ":num_players"),
           (assign, ":end_cond", ":num_players"),
           (try_for_range, ":player_no", 0, ":end_cond"),
             (player_is_active, ":player_no"),
             (player_get_team_no, ":player_team", ":player_no"),
             (this_or_next|eq, ":player_team", 0),
             (eq, ":player_team", 1),
             (player_get_kill_count, ":kill_count", ":player_no"),
             (player_get_death_count, ":death_count", ":player_no"), #get_death_count
             (store_mul, ":player_score_plus_death", ":kill_count", 1000),
             (val_sub, ":player_score_plus_death", ":death_count"),
             (gt, ":player_score_plus_death", ":my_score_plus_death"),
             (assign, ":continue", 0),
             (assign, ":end_cond", 0), #break
           (try_end),
           (eq, ":continue", 1),
           (unlock_achievement, ACHIEVEMENT_ELITE_WARRIOR),
         (try_end),
         #ELITE_WARRIOR achievement end

         (call_script, "script_multiplayer_event_mission_end"),

         (assign, "$g_multiplayer_stats_chart_opened_manually", 0),
         (start_presentation, "prsnt_multiplayer_stats_chart_deathmatch"),
         ]),

      (ti_on_agent_killed_or_wounded, 0, 0, [],
       [
         (store_trigger_param_1, ":dead_agent_no"), 
         (store_trigger_param_2, ":killer_agent_no"),
         (call_script, "script_multiplayer_server_on_agent_killed_or_wounded_common", ":dead_agent_no", ":killer_agent_no"),
         ]),
      
      (1, 0, 0, [],
       [
         (multiplayer_is_server),
         (get_max_players, ":num_players"),
         (try_for_range, ":player_no", 0, ":num_players"),
           (player_is_active, ":player_no"),
           (neg|player_is_busy_with_menus, ":player_no"),

           (player_get_team_no, ":player_team", ":player_no"), #if player is currently spectator do not spawn his agent
           (lt, ":player_team", multi_team_spectator),

           (player_get_troop_id, ":player_troop", ":player_no"), #if troop is not selected do not spawn his agent
           (ge, ":player_troop", 0),

           (player_get_agent_id, ":player_agent", ":player_no"),
           (assign, ":spawn_new", 0),
           (try_begin),
             (player_get_slot, ":player_first_spawn", ":player_no", slot_player_first_spawn),
             (eq, ":player_first_spawn", 1),
             (assign, ":spawn_new", 1),
             (player_set_slot, ":player_no", slot_player_first_spawn, 0),
           (else_try),
             (try_begin),
               (lt, ":player_agent", 0),
               (assign, ":spawn_new", 1),
             (else_try),
               (neg|agent_is_alive, ":player_agent"),
               (agent_get_time_elapsed_since_removed, ":elapsed_time", ":player_agent"),
               (gt, ":elapsed_time", "$g_multiplayer_respawn_period"),
               (assign, ":spawn_new", 1),
             (try_end),             
           (try_end),
           (eq, ":spawn_new", 1),
           (call_script, "script_multiplayer_buy_agent_equipment", ":player_no"),

           (troop_get_inventory_slot, ":has_item", ":player_troop", ek_horse),
           (try_begin),
             (ge, ":has_item", 0),
             (assign, ":is_horseman", 1),
           (else_try),
             (assign, ":is_horseman", 0),
           (try_end),
         
           (call_script, "script_multiplayer_find_spawn_point", ":player_team", 0, ":is_horseman"), 
           (player_spawn_new_agent, ":player_no", reg0),
         (try_end),
         ]),

      (1, 0, 0, [], #do this in every new frame, but not at the same time
       [
         (multiplayer_is_server),
         (store_mission_timer_a, ":mission_timer"),
         (ge, ":mission_timer", 2),
         (assign, ":team_1_count", 0),
         (assign, ":team_2_count", 0),
         (try_for_agents, ":cur_agent"),
           (agent_is_non_player, ":cur_agent"),
           (agent_is_human, ":cur_agent"),
           (assign, ":will_be_counted", 0),
           (try_begin),
             (agent_is_alive, ":cur_agent"),
             (assign, ":will_be_counted", 1), #alive so will be counted
           (else_try),
             (agent_get_time_elapsed_since_removed, ":elapsed_time", ":cur_agent"),
             (le, ":elapsed_time", "$g_multiplayer_respawn_period"),
             (assign, ":will_be_counted", 1), 
           (try_end),
           (eq, ":will_be_counted", 1),
           (agent_get_team, ":cur_team", ":cur_agent"),
           (try_begin),
             (eq, ":cur_team", 0),
             (val_add, ":team_1_count", 1),
           (else_try),
             (eq, ":cur_team", 1),
             (val_add, ":team_2_count", 1),
           (try_end),
         (try_end),
         (store_sub, "$g_multiplayer_num_bots_required_team_1", "$g_multiplayer_num_bots_team_1", ":team_1_count"),
         (store_sub, "$g_multiplayer_num_bots_required_team_2", "$g_multiplayer_num_bots_team_2", ":team_2_count"),
         (val_max, "$g_multiplayer_num_bots_required_team_1", 0),
         (val_max, "$g_multiplayer_num_bots_required_team_2", 0),
         ]),

      (0, 0, 0, [],
       [
         (multiplayer_is_server),
         (eq, "$g_multiplayer_ready_for_spawning_agent", 1),
         (store_add, ":total_req", "$g_multiplayer_num_bots_required_team_1", "$g_multiplayer_num_bots_required_team_2"),
         (try_begin),
           (gt, ":total_req", 0),
           (store_random_in_range, ":random_req", 0, ":total_req"),
           (val_sub, ":random_req", "$g_multiplayer_num_bots_required_team_1"),
           (try_begin),
             (lt, ":random_req", 0),
             #add to team 1
             (assign, ":selected_team", 0),
             (val_sub, "$g_multiplayer_num_bots_required_team_1", 1),
           (else_try),
             #add to team 2
             (assign, ":selected_team", 1),
             (val_sub, "$g_multiplayer_num_bots_required_team_2", 1),
           (try_end),

           (team_get_faction, ":team_faction_no", ":selected_team"),
           (assign, ":available_troops_in_faction", 0),

           (try_for_range, ":troop_no", multiplayer_ai_troops_begin, multiplayer_ai_troops_end),
             (store_troop_faction, ":troop_faction", ":troop_no"),
             (eq, ":troop_faction", ":team_faction_no"),
             (val_add, ":available_troops_in_faction", 1),
           (try_end),

           (store_random_in_range, ":random_troop_index", 0, ":available_troops_in_faction"),
           (assign, ":end_cond", multiplayer_ai_troops_end),
           (try_for_range, ":troop_no", multiplayer_ai_troops_begin, ":end_cond"),
             (store_troop_faction, ":troop_faction", ":troop_no"),
             (eq, ":troop_faction", ":team_faction_no"),
             (val_sub, ":random_troop_index", 1),
             (lt, ":random_troop_index", 0),
             (assign, ":end_cond", 0),
             (assign, ":selected_troop", ":troop_no"),
           (try_end),
         
           (troop_get_inventory_slot, ":has_item", ":selected_troop", ek_horse),
           (try_begin),
             (ge, ":has_item", 0),
             (assign, ":is_horseman", 1),
           (else_try),
             (assign, ":is_horseman", 0),
           (try_end),

           (call_script, "script_multiplayer_find_spawn_point", ":selected_team", 0, ":is_horseman"), 
           (store_current_scene, ":cur_scene"),
           (modify_visitors_at_site, ":cur_scene"),
           (add_visitors_to_current_scene, reg0, ":selected_troop", 1, ":selected_team", -1),
           (assign, "$g_multiplayer_ready_for_spawning_agent", 0),
         (try_end),
         ]),

      (1, 0, 0, [],
       [
         (multiplayer_is_server),
         #checking for restarting the map
         (assign, ":end_map", 0),
         (try_begin),
           (store_mission_timer_a, ":mission_timer"),
           (store_mul, ":game_max_seconds", "$g_multiplayer_game_max_minutes", 60),
           (gt, ":mission_timer", ":game_max_seconds"),
           (assign, ":end_map", 1),
         (try_end),
         (try_begin),
           (eq, ":end_map", 1),
           (call_script, "script_game_multiplayer_get_game_type_mission_template", "$g_multiplayer_game_type"),
           (start_multiplayer_mission, reg0, "$g_multiplayer_selected_map", 0),
           (call_script, "script_game_set_multiplayer_mission_end"),
         (try_end),
         ]),
        
      (ti_tab_pressed, 0, 0, [],
       [
         (try_begin),
           (eq, "$g_multiplayer_mission_end_screen", 0),
           (assign, "$g_multiplayer_stats_chart_opened_manually", 1),
           (start_presentation, "prsnt_multiplayer_stats_chart_deathmatch"),
         (try_end),
         ]),

      multiplayer_once_at_the_first_frame,
      
      (ti_escape_pressed, 0, 0, [],
       [
         (neg|is_presentation_active, "prsnt_multiplayer_escape_menu"),
         (neg|is_presentation_active, "prsnt_multiplayer_stats_chart_deathmatch"),
         (eq, "$g_waiting_for_confirmation_to_terminate", 0),
         (start_presentation, "prsnt_multiplayer_escape_menu"),
         ]),
      ],
  ),
]
