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

mission_templates_field_battle = [
# This template is used in party encounters and such.
# 
  (
    "conversation_encounter",0,-1,
    "Conversation_encounter",
    [( 0,mtef_visitor_source,af_override_fullhelm,0,1,[]),( 1,mtef_visitor_source,af_override_fullhelm,0,1,[]),
     ( 2,mtef_visitor_source,af_override_fullhelm,0,1,[]),( 3,mtef_visitor_source,af_override_fullhelm,0,1,[]),( 4,mtef_visitor_source,af_override_fullhelm,0,1,[]),( 5,mtef_visitor_source,af_override_fullhelm,0,1,[]),( 6,mtef_visitor_source,af_override_fullhelm,0,1,[]),
     ( 7,mtef_visitor_source,af_override_fullhelm,0,1,[]),( 8,mtef_visitor_source,af_override_fullhelm,0,1,[]),( 9,mtef_visitor_source,af_override_fullhelm,0,1,[]),(10,mtef_visitor_source,af_override_fullhelm,0,1,[]),(11,mtef_visitor_source,af_override_fullhelm,0,1,[]),
    #prisoners now...
     (12,mtef_visitor_source,af_override_fullhelm,0,1,[]),(13,mtef_visitor_source,af_override_fullhelm,0,1,[]),(14,mtef_visitor_source,af_override_fullhelm,0,1,[]),(15,mtef_visitor_source,af_override_fullhelm,0,1,[]),(16,mtef_visitor_source,af_override_fullhelm,0,1,[]),
    #Other party
     (17,mtef_visitor_source,af_override_fullhelm,0,1,[]),(18,mtef_visitor_source,af_override_fullhelm,0,1,[]),(19,mtef_visitor_source,af_override_fullhelm,0,1,[]),(20,mtef_visitor_source,af_override_fullhelm,0,1,[]),(21,mtef_visitor_source,af_override_fullhelm,0,1,[]),
     (22,mtef_visitor_source,af_override_fullhelm,0,1,[]),(23,mtef_visitor_source,af_override_fullhelm,0,1,[]),(24,mtef_visitor_source,af_override_fullhelm,0,1,[]),(25,mtef_visitor_source,af_override_fullhelm,0,1,[]),(26,mtef_visitor_source,af_override_fullhelm,0,1,[]),
     (27,mtef_visitor_source,af_override_fullhelm,0,1,[]),(28,mtef_visitor_source,af_override_fullhelm,0,1,[]),(29,mtef_visitor_source,af_override_fullhelm,0,1,[]),(30,mtef_visitor_source,af_override_fullhelm,0,1,[]),(31,mtef_visitor_source,af_override_fullhelm,0,1,[]),
     ],
    [],
  ),
  
  #gekokujo 3.1 encounters framework start
  #this is pretty much a copy of mt_back_alley_revolt, with different entry points and bodyguards
  #also used by gekokujo 3.1 crimes
  (
    "gekokujo_encounter",mtf_battle_mode|mtf_synch_inventory,charge,
    "You lead your men to battle.",
    [
      (0,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
      (1,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
      (2,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
      (3,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
    ],
    [
      common_inventory_not_available,
      common_battle_init_banner,
      
      (ti_tab_pressed, 0, 0, [(display_message,"str_cannot_leave_now")], []),
      (ti_before_mission_start, 0, 0, [], [(call_script, "script_change_banners_and_chest")]),
      (0, 0, ti_once, [],[(call_script, "script_music_set_situation_with_culture", mtf_sit_fight)]),
      
      #spawn the enemy closer in field encounters
      (ti_on_agent_spawn, 0, 0, [], 
        [
          (eq, "$gekokujo_encounter_mode", 1), #1 = encounter
          
          (store_trigger_param_1, ":agent"),
          (agent_get_troop_id, ":troop", ":agent"),
          (neq, ":troop", "trp_player"),
          
          (assign, ":is_enemy", 0),
          (try_begin),
            (eq, ":troop", "$gekokujo_encounter_boss"),
            (assign, ":is_enemy", 1),
          (else_try),
            (eq, ":troop", "$gekokujo_encounter_mook"),
            (assign, ":is_enemy", 1),
          (try_end),
          
          (eq, ":is_enemy", 1),
          
          (entry_point_get_position, pos3, 2), #player position
          
          #let's do the main shift calculated in mnu_encounter_setup
          (position_move_x, pos3, "$gekokujo_encounter_x"),
          (position_move_y, pos3, "$gekokujo_encounter_y"),
          
          #let's also spread the enemies out a little
          (store_random_in_range, ":shift", -100, 100),
          (position_move_x, pos3, ":shift"),
          (store_random_in_range, ":shift", -100, 100),
          (position_move_y, pos3, ":shift"),
          
          (agent_set_position, ":agent", pos3),
        ]),
      
      #check if lethal weapons were used (crime getaway)
      (ti_on_agent_killed_or_wounded, 0, 0, [],
        [
          (store_trigger_param_1, ":dead_agent"),
          (store_trigger_param_3, ":is_wounded"),
          
          (agent_get_troop_id, ":troop", ":dead_agent"),
          (neq, ":troop", "trp_player"),
          
          (try_begin),
            (neg|agent_is_ally, ":dead_agent"),
            (eq, ":is_wounded", 0),
            (assign, "$gekokujo_crime_getaway_lethal", 1),
          (try_end),
        ]),
      
      #check if the battle is over
      (1, 4, ti_once, 
        [
          #(this_or_next|main_hero_fallen),
          (num_active_teams_le, 1),
        ],
        [
          (try_begin),
            #2 = burglary
            (eq, "$gekokujo_encounter_mode", 3), #3 = getaway
            (assign, ":fail_menu", "mnu_getaway_failed"),
            (assign, ":success_menu", "mnu_getaway_succeeded"),
          (else_try),
            #1 = encounter
            (assign, ":fail_menu", "mnu_encounter_lost"),
            (assign, ":success_menu", "mnu_encounter_won"),
          (try_end),
          
          (try_begin),
            #(main_hero_fallen),
            (neg|all_enemies_defeated),
            (jump_to_menu, ":fail_menu"),
          (else_try),
            (jump_to_menu, ":success_menu"),
          (try_end),
          
          (finish_mission),
        ]),
        
      
      common_gekokujo_sabakato_switch_check,
      
    ] + bodyguard_triggers,
  ),
  #gekokujo 3.1 encounters framework end

  (
    "lead_charge",mtf_battle_mode|mtf_synch_inventory,charge,
    "You lead your men to battle.",
    [
     (1,mtef_defenders|mtef_team_0,0,aif_start_alarmed,12,[]),
     (0,mtef_defenders|mtef_team_0,0,aif_start_alarmed,0,[]),
     (4,mtef_attackers|mtef_team_1,0,aif_start_alarmed,12,[]),
     (4,mtef_attackers|mtef_team_1,0,aif_start_alarmed,0,[]),
     ],
	 trigger_cannon+
    [
      (ti_on_agent_spawn, 0, 0, [],
       [
         (store_trigger_param_1, ":agent_no"),
         (call_script, "script_agent_reassign_team", ":agent_no"),

         (assign, ":initial_courage_score", 5000),
                  
         (agent_get_troop_id, ":troop_id", ":agent_no"),
         (store_character_level, ":troop_level", ":troop_id"),
         (val_mul, ":troop_level", 35),
         (val_add, ":initial_courage_score", ":troop_level"), #average : 20 * 35 = 700
         
         (store_random_in_range, ":randomized_addition_courage", 0, 3000), #average : 1500
         (val_add, ":initial_courage_score", ":randomized_addition_courage"), 
         #llf
		 (neq,":troop_id","trp_assistant_gunner"),
		 #llf end
         (agent_get_party_id, ":agent_party", ":agent_no"),         
         (party_get_morale, ":cur_morale", ":agent_party"),
         
         (store_sub, ":morale_effect_on_courage", ":cur_morale", 70),
         (val_mul, ":morale_effect_on_courage", 30), #this can effect morale with -2100..900
         (val_add, ":initial_courage_score", ":morale_effect_on_courage"), 
         
         #average = 5000 + 700 + 1500 = 7200; min : 5700, max : 8700
         #morale effect = min : -2100(party morale is 0), average : 0(party morale is 70), max : 900(party morale is 100)
         #min starting : 3600, max starting  : 9600, average starting : 7200
         (agent_set_slot, ":agent_no", slot_agent_courage_score, ":initial_courage_score"), 
         ]),
         
       (ti_on_agent_hit, 0, 0, 
    [
      (eq, "$cut_body", 1),
    ],
    [
      (store_trigger_param_1, ":var0"),
      (store_trigger_param_2, ":var1"),
      (store_trigger_param_3, ":var2"),
      (store_trigger_param, ":var3", 4),
      (copy_position, pos1, pos0),
      (assign, ":var4", reg0),
      (agent_is_human, ":var0"),
      (try_begin),
        (eq, ":var3", 9),
        (try_begin),
          (agent_is_non_player, ":var0"),
          (ge, ":var2", 25),
          (neq, ":var4", "itm_mace_1"),
          (agent_get_action_dir, ":var5", ":var1"),
          (this_or_next|eq, ":var5", 1),
          (eq, ":var5", 2),
          (store_agent_hit_points, ":var6", ":var0", 1),
          (val_add, ":var6", 10),
          (ge, ":var2", ":var6"),
          (agent_get_item_slot, ":var7", ":var0", ek_head),
          (try_begin),
            (ge, ":var7", 1),
            (agent_unequip_item, ":var0", ":var7"),
            (try_begin),
              (assign, ":var8", 360),
              (spawn_item, ":var7", imod_plain, ":var8"),
            (end_try),
          (end_try),
          (agent_equip_item, ":var0", "itm_invisible_head"),
          (agent_get_position, pos4, ":var0"),
          (agent_get_horse, ":var9", ":var0"),
          (try_begin),
            (ge, ":var9", 0),
            (assign, ":var10", 240),
          (else_try),
            (assign, ":var10", 160),
          (end_try),
          (position_move_z, pos4, ":var10"),
          (store_random_in_range, ":var11", 0, 360),
          (store_random_in_range, ":var12", -60, 60),
          (store_random_in_range, ":var13", -90, 90),
          (store_random_in_range, ":var14", -90, 90),
          (position_rotate_z, pos4, ":var11"),
          (position_rotate_y, pos4, ":var12"),
          (position_move_x, pos4, ":var13"),
          (position_move_y, pos4, ":var14"),
          (position_set_z_to_ground_level, pos4),
          (position_move_z, pos4, 5),
          (set_spawn_position, pos4),
          (particle_system_burst, "psys_game_blood", pos4, 10),
          (particle_system_burst, "psys_game_blood_2", pos4, 10),
          (assign, ":var15", "spr_head_dynamic_male"),
          (agent_get_troop_id, ":var16", ":var0"),
          (try_begin),
            (ge, ":var16", 0),
            (troop_get_type, ":var17", ":var16"),
            (eq, ":var17", 1),
            (assign, ":var15", "spr_head_dynamic_female"),
          (end_try),
          (position_move_z, pos4, 20),
          (set_spawn_position, pos4),
          (spawn_scene_prop, ":var15"),
        (end_try),
        (val_mul, ":var2", 0),
      (else_try),
        (is_between, ":var3", 10, 19),
        (val_mul, ":var2", 0),
      (else_try),
        (is_between, ":var3", 1, 7),
        (store_agent_hit_points, ":var6", ":var0", 1),
        (store_agent_hit_points, ":var18", ":var0", 0),
        (try_begin),
          (gt, ":var18", 0),
          (store_div, ":var19", ":var2", ":var18"),
          (try_begin),
            (this_or_next|gt, ":var19", 0),
            (lt, ":var6", 41),
            (agent_set_speed_modifier, ":var0", ":var6"),
          (end_try),
          (val_mul, ":var2", 0),
        (end_try),
      (end_try),
      (store_agent_hit_points, ":var20", ":var0", 1),
      (val_sub, ":var20", ":var2"),
      (agent_set_hit_points, ":var0", ":var20", 1),
    ]),
         
         (ti_on_agent_spawn, 0, 0, 
    [],
    [
      (store_trigger_param_1, ":var0"),
      (agent_is_alive, ":var0"),
      (agent_is_human, ":var0"),
      (agent_get_item_slot, ":var1", ":var0", ek_body),
      (try_begin),
        (this_or_next|is_between, ":var1", "itm_ceshi", "itm_ceshi"),
        (this_or_next|eq, ":var1", "itm_ceshi"),
        (is_between, ":var1", "itm_ceshi", "itm_ceshi"),
        (agent_set_footstep_sound, ":var0", 2, "snd_footstep_wood"),
      (end_try),
    ]),
         
      #gekokujo 3.1 samurai use primary weapons start
      #no more relying on katanas during field battles
            (0, 0, ti_once, [], [(assign,"$g_battle_won",0),
                           ## CC
                           (try_begin),
                             # not normal size
                             (neq, "$g_random_scene_size", 1),
                             # inventory
                             (get_player_agent_no, ":player_agent"),
                             (agent_get_look_position, pos1, ":player_agent"),
                             (position_move_y, pos1, -300),
                             (position_rotate_z, pos1, 180),
                             (position_set_z_to_ground_level, pos1),
                             (set_spawn_position, pos1),
                             (spawn_scene_prop, "spr_inventory", 0),
                             # banner
                             (troop_get_slot, ":troop_banner_object", "trp_player", slot_troop_banner_scene_prop),
                             (try_begin),
                               (gt, ":troop_banner_object", 0),
                               # banner pole
                               (position_move_y, pos1, -200),
                               (position_set_z_to_ground_level, pos1),
                               (set_spawn_position, pos1),
                               (spawn_scene_prop, "spr_banner_pole", 0),
                               # banner
                               (position_move_z, pos1, 320),
                               (set_spawn_position, pos1),
                               (spawn_scene_prop, ":troop_banner_object", 0),
                             (try_end),
                           (try_end),
                           ## CC
                           (assign,"$defender_reinforcement_stage",0),
                           (assign,"$attacker_reinforcement_stage",0),
                           (call_script, "script_place_player_banner_near_inventory"),
                           (call_script, "script_combat_music_set_situation_with_culture"),
                           (assign, "$g_defender_reinforcement_limit", 2),
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
      #gekokujo 3.1 samurai use primary weapons end

      common_battle_init_banner,common_fade,
		 
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
##          (str_store_troop_name, s6, ":dead_agent_troop_id"),
##          (assign, reg0, ":dead_agent_no"),
##          (assign, reg1, ":killer_agent_no"),
##          (assign, reg2, ":is_wounded"),
##          (agent_get_team, reg3, ":dead_agent_no"),          
          #(display_message, "@{!}dead agent no : {reg0} ; killer agent no : {reg1} ; is_wounded : {reg2} ; dead agent team : {reg3} ; {s6} is added"), 
          (party_add_members, "p_total_enemy_casualties", ":dead_agent_troop_id", 1), #addition_to_p_total_enemy_casualties
          (eq, ":is_wounded", 1),
          (party_wound_members, "p_total_enemy_casualties", ":dead_agent_troop_id", 1), 
        (try_end),

        (call_script, "script_apply_death_effect_on_courage_scores", ":dead_agent_no", ":killer_agent_no"),
       ]),

      common_battle_tab_press,

      (ti_question_answered, 0, 0, [],
       [(store_trigger_param_1,":answer"),
        (eq,":answer",0),
        (assign, "$pin_player_fallen", 0),
        (try_begin),
          (store_mission_timer_a, ":elapsed_time"),
          (gt, ":elapsed_time", 20),
          (str_store_string, s5, "str_retreat"),
          (call_script, "script_simulate_retreat", 10, 20, 1),
        (try_end),
        (call_script, "script_count_mission_casualties_from_agents"),
        (finish_mission,0),]),

      (ti_before_mission_start, 0, 0, [],
       [
         (team_set_relation, 0, 2, 1),
         (team_set_relation, 1, 3, 1),
         (call_script, "script_place_player_banner_near_inventory_bms"),

         (party_clear, "p_routed_enemies"),

         (assign, "$g_latest_order_1", 1), 
         (assign, "$g_latest_order_2", 1), 
         (assign, "$g_latest_order_3", 1), 
         (assign, "$g_latest_order_4", 1), 
         ]),

      
      (0, 0, ti_once, [], [(assign,"$g_battle_won",0),
                           (assign,"$defender_reinforcement_stage",0),
                           (assign,"$attacker_reinforcement_stage",0),
                           (call_script, "script_place_player_banner_near_inventory"),
                           (call_script, "script_combat_music_set_situation_with_culture"),
                           (assign, "$g_defender_reinforcement_limit", 2),
                           #gekokujo 3.0 diplomacy deathcam deprecated start
                           ###diplomacy begin
                           #(assign, "$g_dplmc_cam_activated", 0),
                           #(assign, "$g_dplmc_charge_when_dead", 0),
                           ###diplomacy end
                           #gekokujo 3.0 diplomacy deathcam deprecated end
                           ]),

      common_music_situation_update,
      common_battle_check_friendly_kills,

      (1, 0, 5, [
                              
      #new (25.11.09) starts (sdsd = TODO : make a similar code to also helping ally encounters)
      #count all total (not dead) enemy soldiers (in battle area + not currently placed in battle area)
      (call_script, "script_party_count_members_with_full_health", "p_collective_enemy"),
      (assign, ":total_enemy_soldiers", reg0),
      
      #decrease number of agents already in battle area to find all number of reinforcement enemies
      (assign, ":enemy_soldiers_in_battle_area", 0),
      (try_for_agents,":cur_agent"),
        (agent_is_human, ":cur_agent"),
        (agent_get_party_id, ":agent_party", ":cur_agent"),
        (try_begin),
          (neq, ":agent_party", "p_main_party"),
          (neg|agent_is_ally, ":cur_agent"),
          (val_add, ":enemy_soldiers_in_battle_area", 1),
        (try_end),
      (try_end),
      (store_sub, ":total_enemy_reinforcements", ":total_enemy_soldiers", ":enemy_soldiers_in_battle_area"),

      (try_begin),
        (lt, ":total_enemy_reinforcements", 15),
        (ge, "$defender_reinforcement_stage", 2),
        (eq, "$defender_reinforcement_limit_increased", 0),
        (val_add, "$g_defender_reinforcement_limit", 1),                    
        (assign, "$defender_reinforcement_limit_increased", 1),
      (try_end),    
      #new (25.11.09) ends
      
      
      
      
      
      
      (lt,"$defender_reinforcement_stage","$g_defender_reinforcement_limit"),
                 (store_mission_timer_a,":mission_time"),
                 (ge,":mission_time",10),
                 (store_normalized_team_count,":num_defenders", 0),
                 (lt,":num_defenders",6)],
           [(add_reinforcements_to_entry,0,7),(assign, "$defender_reinforcement_limit_increased", 0),(val_add,"$defender_reinforcement_stage",1)]),
      
      (1, 0, 5, [(lt,"$attacker_reinforcement_stage",2),
                 (store_mission_timer_a,":mission_time"),
                 (ge,":mission_time",10),
                 (store_normalized_team_count,":num_attackers", 1),
                 (lt,":num_attackers",6)],
           [(add_reinforcements_to_entry,3,7),(val_add,"$attacker_reinforcement_stage",1)]),

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

      common_battle_inventory,

      #AI Triggers
      (0, 0, ti_once, [
          (store_mission_timer_a,":mission_time"),(ge,":mission_time",2),
          ],
       [(call_script, "script_select_battle_tactic"),
        (call_script, "script_battle_tactic_init"),
        #(call_script, "script_battle_calculate_initial_powers"), #deciding run away method changed and that line is erased
        ]),
      
      #gekokujo 3.1 jacobhinds overhauled morale and routing start
      #(3, 0, 0, [
      #    (call_script, "script_apply_effect_of_other_people_on_courage_scores"),
      #        ], []), #calculating and applying effect of people on others courage scores
      (3, 0, 0, 
        [
          #controlling courage score and if needed deciding to run away for each agent
          (try_for_agents, ":agent_no"),
            (agent_is_human, ":agent_no"),
            (agent_is_alive, ":agent_no"),
            (store_mission_timer_a,":mission_time"),
            (ge,":mission_time",3),
            (call_script, "script_decide_run_away_or_not", ":agent_no", ":mission_time"),
          (try_end),
          
          #routing soldiers recover morale by 30 every 3 seconds.
          (try_for_agents, ":agent"),
            (agent_is_alive, ":agent"),
            (agent_is_human, ":agent"),
            (agent_get_slot, ":routing", ":agent", slot_agent_is_running_away),
            (eq, ":routing", 1),
            (agent_get_slot, ":courage", ":agent", slot_agent_courage_score),
            (val_add, ":courage", 100),
            (agent_set_slot, ":agent", slot_agent_courage_score, ":courage"),
          (try_end),
        ], []), 
      #gekokujo 3.1 jacobhinds overhauled morale and routing end

      (3, 0, 0, [
		  #gekokujo 3.0 no running away in sea battles start
		  (party_get_current_terrain, ":terrain", "$g_encountered_party"),
		  (neq, ":terrain", rt_bridge),
		  #gekokujo 3.0 no running away in sea battles end
          (try_for_agents, ":agent_no"),
            (agent_is_human, ":agent_no"),
            (agent_is_alive, ":agent_no"),          
            (store_mission_timer_a,":mission_time"),
            (ge,":mission_time",3),          
            (call_script, "script_decide_run_away_or_not", ":agent_no", ":mission_time"),
          (try_end),          
              ], []), #controlling courage score and if needed deciding to run away for each agent

      (5, 0, 0, [
          (store_mission_timer_a,":mission_time"),

          (ge,":mission_time",3),
          
          (call_script, "script_battle_tactic_apply"),
          ], []), #applying battle tactic

      common_battle_order_panel,
      common_battle_order_panel_tick,

    ]
    ##diplomacy begin + #gekokujo 2.1 PBO
    + dplmc_battle_mode_triggers + prebattle_orders_triggers + caba_order_triggers,
    ##diplomacy end
  ),
##  (
##    "charge_with_allies",mtf_battle_mode,charge_with_ally,
##    "Taking a handful of fighters with you, you set off to patrol the area.",
##    [
##     (1,mtef_defenders,0,0|aif_start_alarmed,8,[]),
##     (0,mtef_defenders,0,0|aif_start_alarmed,0,[]),
##     (4,mtef_attackers,0,aif_start_alarmed,8,[]),
##     (4,mtef_attackers,0,aif_start_alarmed,0,[]),
##     ],
##    [
##      (ti_tab_pressed, 0, 0, [],
##       [
##           (try_begin),
##             (eq, "$battle_won", 1),
##             (finish_mission,0),
##           (else_try),
##             (call_script, "script_cf_check_enemies_nearby"),
##             (question_box,"str_do_you_want_to_retreat"),
##           (else_try),
##             (display_message,"str_can_not_retreat"),
##           (try_end),
##        ]),
##      (ti_question_answered, 0, 0, [],
##       [(store_trigger_param_1,":answer"),
##        (eq,":answer",0),
##        (assign, "$pin_player_fallen", 0),
##        (str_store_string, s5, "str_retreat"),
##        (call_script, "script_simulate_retreat", 10, 30),
##        (finish_mission,0),]),
##
##      (0, 0, ti_once, [], [(assign,"$battle_won",0),(assign,"$defender_reinforcement_stage",0),(assign,"$attacker_reinforcement_stage",0)]),
##      (1, 0, 5, [(lt,"$defender_reinforcement_stage",2),(store_mission_timer_a,reg(1)),(ge,reg(1),10),(store_defender_count,reg(2)),(lt,reg(2),3)],
##           [(add_reinforcements_to_entry,0,4),(val_add,"$defender_reinforcement_stage",1)]),
##      (1, 0, 5, [(lt,"$attacker_reinforcement_stage",2),(store_mission_timer_a,reg(1)),(ge,reg(1),10),(store_attacker_count,reg(2)),(lt,reg(2),3)],
##           [(add_reinforcements_to_entry,3,4),(val_add,"$attacker_reinforcement_stage",1)]),
##      (1, 60, ti_once, [(store_mission_timer_a,reg(1)),
##                        (ge,reg(1),10),(all_enemies_defeated,2),
##                        (neg|main_hero_fallen,0),
##                        (set_mission_result,1),
##                        (assign, "$g_battle_result", 1),
##                        (display_message,"str_msg_battle_won"),
##                        (assign,"$battle_won",1)],
##           [(finish_mission,1)]),
##      (10, 0, 0, [], [(eq,"$battle_won",1),(display_message,"str_msg_battle_won")]),
##
##      (1, 4, ti_once, [(main_hero_fallen)],
##          [
##              (assign, "$pin_player_fallen", 1),
##              (str_store_string, s5, "str_retreat"),
##              (call_script, "script_simulate_retreat", 20, 30),
##              (assign, "$g_battle_result", -1),
##              (set_mission_result,-1),(finish_mission,0)]),
##      (ti_inventory_key_pressed, 0, 0, [(display_message,"str_use_baggage_for_inventory")], []),
##    ],
##  ),

##  (
##    "charge_with_allies_old",mtf_battle_mode,charge_with_ally,
##    "Taking a handful of fighters with you, you set off to patrol the area.",
##    [(1,mtef_leader_only,0,0,1,[]),
##     (1,mtef_no_leader,0,0|aif_start_alarmed,2,[]),
##     (1,mtef_reverse_order|mtef_ally_party,0,0|aif_start_alarmed,3,[]),
##     (0,mtef_no_leader,0,0|aif_start_alarmed,0,[]),
##     (0,mtef_reverse_order|mtef_ally_party,0,0|aif_start_alarmed,0,[]),
##     (3,mtef_reverse_order|mtef_enemy_party,0,aif_start_alarmed,6,[]),
##     (4,mtef_reverse_order|mtef_enemy_party,0,aif_start_alarmed,0,[])],
##    [
##      (ti_tab_pressed, 0, 0, [],
##       [
##           (try_begin),
##             (eq, "$battle_won", 1),
##             (finish_mission,0),
##           (else_try),
##             (call_script, "script_cf_check_enemies_nearby"),
##             (question_box,"str_do_you_want_to_retreat"),
##           (else_try),
##             (display_message,"str_can_not_retreat"),
##           (try_end),
##        ]),
##      (ti_question_answered, 0, 0, [],
##       [(store_trigger_param_1,":answer"),(eq,":answer",0),(finish_mission,0),]),
##
##      (0, 0, ti_once, [], [(assign,"$battle_won",0),(assign,"$enemy_reinforcement_stage",0),(assign,"$friend_reinforcement_stage",0),(assign,"$ally_reinforcement_stage",0)]),
##      
##      (1, 0, 5, [(lt,"$enemy_reinforcement_stage",2),(store_mission_timer_a,reg(1)),(ge,reg(1),10),(store_enemy_count,reg(2)),(lt,reg(2),3)],
##       [(add_reinforcements_to_entry,6,3),(val_add,"$enemy_reinforcement_stage",1)]),
##      (1, 0, 5, [(lt,"$friend_reinforcement_stage",2),(store_mission_timer_a,reg(1)),(ge,reg(1),10),(store_friend_count,reg(2)),(lt,reg(2),2)],
##       [(add_reinforcements_to_entry,3,1),(val_add,"$friend_reinforcement_stage",1)]),
##      (1, 0, 5, [(lt,"$ally_reinforcement_stage",2),(store_mission_timer_a,reg(1)),(ge,reg(1),10),(store_ally_count,reg(2)),  (lt,reg(2),2)],
##       [(add_reinforcements_to_entry,4,2),(val_add,"$ally_reinforcement_stage",1)]),
##      (1, 60, ti_once, [(store_mission_timer_a,reg(1)),
##                        (ge,reg(1),10),
##                        (all_enemies_defeated,2),
##                        (neg|main_hero_fallen,0),
##                        (set_mission_result,1),
##                        (assign, "$g_battle_result", 1),
##                        (display_message,"str_msg_battle_won"),
##                        (assign,"$battle_won",1),
##                        ],
##       [(finish_mission,1)]),
##      (10, 0, 0, [], [(eq,"$battle_won",1),(display_message,"str_msg_battle_won")]),
##      (1, 4, ti_once, [(main_hero_fallen,0)],
##       [(set_mission_result,-1),(finish_mission,1)]),
##      (ti_inventory_key_pressed, 0, 0, [(display_message,"str_use_baggage_for_inventory")], []),
##    ],
##  ),
##  (
##    "lead_charge_old",mtf_battle_mode,charge,
##    "You lead your men to battle.",
##    [
##     (1,mtef_leader_only,0,0,1,[]),
##     (1,mtef_no_leader,0,0|aif_start_alarmed,5,[]),
##     (0,mtef_no_leader,0,0|aif_start_alarmed,0,[]),
##     (3,mtef_enemy_party|mtef_reverse_order,0,aif_start_alarmed,6,[]),
##     (4,mtef_enemy_party|mtef_reverse_order,0,aif_start_alarmed,0,[]),
##     ],
##    [
##      (ti_tab_pressed, 0, 0, [],
##       [
##           (try_begin),
##             (eq, "$battle_won", 1),
##             (finish_mission,0),
##           (else_try),
##             (call_script, "script_cf_check_enemies_nearby"),
##             (question_box,"str_do_you_want_to_retreat"),
##           (else_try),
##             (display_message,"str_can_not_retreat"),
##           (try_end),
##        ]),
##      (ti_question_answered, 0, 0, [],
##       [(store_trigger_param_1,":answer"),(eq,":answer",0),(finish_mission,0),]),
##
##      (0, 0, ti_once, [], [(assign,"$battle_won",0),(assign,"$enemy_reinforcement_stage",0),(assign,"$friend_reinforcement_stage",0)]),
##      (1, 0, 5, [(lt,"$enemy_reinforcement_stage",2),(store_mission_timer_a,reg(1)),(ge,reg(1),10),(store_enemy_count,reg(2)),(lt,reg(2),3)],
##           [(add_reinforcements_to_entry,4,3),(val_add,"$enemy_reinforcement_stage",1)]),
##      (1, 0, 5, [(lt,"$friend_reinforcement_stage",2),(store_mission_timer_a,reg(1)),(ge,reg(1),10),(store_friend_count,reg(2)),(lt,reg(2),3)],
##           [(add_reinforcements_to_entry,2,3),(val_add,"$friend_reinforcement_stage",1)]),
##      (1, 60, ti_once, [(store_mission_timer_a,reg(1)),
##                        (ge,reg(1),10),(all_enemies_defeated,2),
##                        (neg|main_hero_fallen,0),
##                        (set_mission_result,1),
##                        (assign, "$g_battle_result", 1),
##                        (display_message,"str_msg_battle_won"),
##                        (assign,"$battle_won",1)],
##           [(finish_mission,1)]),
##      (10, 0, 0, [], [(eq,"$battle_won",1),(display_message,"str_msg_battle_won")]),
##      (1, 4, ti_once, [(main_hero_fallen)],
##          [
##              (assign, "$g_battle_result", -1),
##              (set_mission_result,-1),(finish_mission,1)]),
##      (ti_inventory_key_pressed, 0, 0, [(display_message,"str_use_baggage_for_inventory")], []),
##    ],
##  ),



  (
    "besiege_inner_battle_castle",mtf_battle_mode,-1,
    "You attack the walls of the castle...",
    [
     (0, mtef_attackers|mtef_use_exact_number|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     (6, mtef_attackers|mtef_use_exact_number|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     (7, mtef_attackers|mtef_use_exact_number|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     (16, mtef_defenders|mtef_use_exact_number|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
     (17, mtef_defenders|mtef_use_exact_number|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
     (18, mtef_defenders|mtef_use_exact_number|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
     (19, mtef_defenders|mtef_use_exact_number|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
     (20, mtef_defenders|mtef_use_exact_number|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
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
]
