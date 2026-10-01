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

mission_templates_town_village = [
  (
    "town_default",0,-1,
    "Default town visit",
    [(0,mtef_scene_source|mtef_team_0,af_override_horse,0,1,pilgrim_disguise),
     (1,mtef_scene_source|mtef_team_0,af_override_horse,0,1,[]),
     (2,mtef_scene_source|mtef_team_0,af_override_horse,0,1,[]),
     (3,mtef_scene_source|mtef_team_0,af_override_horse,0,1,[]),
     (4,mtef_scene_source|mtef_team_0,af_override_horse,0,1,[]),
     (5,mtef_scene_source|mtef_team_0,af_override_horse,0,1,[]),
     (6,mtef_scene_source|mtef_team_0,af_override_horse,0,1,[]),
     (7,mtef_scene_source|mtef_team_0,af_override_horse,0,1,[]),
     (8,mtef_scene_source,af_override_horse,0,1,[]),
     (9,mtef_scene_source,af_override_horse,0,1,[]),
     (10,mtef_scene_source,af_override_horse,0,1,[]),
     (11,mtef_scene_source,af_override_horse,0,1,[]),
     (12,mtef_scene_source,af_override_horse,0,1,[]),
     (13,mtef_scene_source,0,0,1,[]),
     (14,mtef_scene_source,0,0,1,[]),
     (15,mtef_scene_source,0,0,1,[]),
     (16,mtef_visitor_source,af_override_horse,0,1,[]),
     (17,mtef_visitor_source,af_override_horse,0,1,[]),
     (18,mtef_visitor_source,af_override_horse,0,1,[]),
     (19,mtef_visitor_source,af_override_horse,0,1,[]),
     (20,mtef_visitor_source,af_override_horse,0,1,[]),
     (21,mtef_visitor_source,af_override_horse,0,1,[]),
     (22,mtef_visitor_source,af_override_horse,0,1,[]),
     (23,mtef_visitor_source,af_override_horse,0,1,[]),
     (24,mtef_visitor_source,af_override_horse,0,1,[]),
     (25,mtef_visitor_source,af_override_horse,0,1,[]),
     (26,mtef_visitor_source,af_override_horse,0,1,[]),
     (27,mtef_visitor_source,af_override_horse,0,1,[]),
     (28,mtef_visitor_source,af_override_horse,0,1,[]),
     (29,mtef_visitor_source,af_override_horse,0,1,[]),
     (30,mtef_visitor_source,af_override_horse,0,1,[]),
     (31,mtef_visitor_source,af_override_horse,0,1,[]),
     ],     
     [
      (1, 0, ti_once, [], 
      [
        (store_current_scene, ":cur_scene"),
        (scene_set_slot, ":cur_scene", slot_scene_visited, 1),
        (try_begin),
          (eq, "$sneaked_into_town", 1),
          (call_script, "script_music_set_situation_with_culture", mtf_sit_town_infiltrate),
        (else_try),
          (eq, "$talk_context", tc_tavern_talk),
          (call_script, "script_music_set_situation_with_culture", mtf_sit_tavern),
        (else_try),
          (call_script, "script_music_set_situation_with_culture", mtf_sit_town),
        (try_end),
      ]),
	  		  	        
      (ti_before_mission_start, 0, 0, [], 
      [
        (call_script, "script_change_banners_and_chest"),
        (call_script, "script_initialize_tavern_variables"),
	  ]),

      (ti_inventory_key_pressed, 0, 0, 
      [
        (set_trigger_result,1)
      ], []),
      
      #tavern - belligerent drunk leaving/fading out
      (1, 0, 0, 
      [
        (gt, "$g_belligerent_drunk_leaving", 0),
        (entry_point_get_position, pos0, 0),
        (agent_get_position, pos1, "$g_belligerent_drunk_leaving"),
        (get_distance_between_positions, ":dist", pos0, pos1),
        (le, ":dist", 150),
      ],
      [
        (agent_fade_out, "$g_belligerent_drunk_leaving"),
        (assign, "$g_belligerent_drunk_leaving", 0),
      ]),
      
      (ti_tab_pressed, 0, 0, 
      [
        (try_begin),
          (eq, "$g_main_attacker_agent", 0),
          (set_trigger_result, 1),
        (try_end),  
      ], []),

	  #tavern brawl triggers - drunk
      (2, 0, 0, 
      [
	    (neg|conversation_screen_is_active),

		(eq, "$talk_context", tc_tavern_talk),
		
		(neg|troop_slot_eq, "trp_hired_assassin", slot_troop_cur_center, "$g_encountered_party"),		
		(troop_slot_eq, "trp_belligerent_drunk", slot_troop_cur_center, "$g_encountered_party"),		
		(eq, "$drunks_dont_pick_fights", 0),		
	  ], 
	  [	  
	    (try_begin),
	      (eq, "$g_start_belligerent_drunk_fight", 0),
	      (assign, "$g_start_belligerent_drunk_fight", 1),
	      
	      (try_for_agents, ":cur_agent"),
	        (agent_get_troop_id, ":cur_agent_troop", ":cur_agent"),
	        (eq, ":cur_agent_troop", "trp_belligerent_drunk"),
	        (assign, "$g_belligerent_drunk", ":cur_agent"),
	      (try_end),
	    (else_try),
	      (eq, "$g_start_belligerent_drunk_fight", 1),	 
	           
	      (agent_is_active, "$g_belligerent_drunk"),
	      (agent_is_alive, "$g_belligerent_drunk"),
	      (get_player_agent_no, ":player_agent"),
	      (agent_get_position, pos0, ":player_agent"),
	      (agent_get_position, pos1, "$g_belligerent_drunk"),
	      (get_distance_between_positions, ":dist", pos0, pos1),
	      (position_get_z, ":pos0_z", pos0),
	      (position_get_z, ":pos1_z", pos1),
	      (store_sub, ":z_difference", ":pos1_z", ":pos0_z"),
	      (try_begin),
	        (le, ":z_difference", 0),
	        (val_mul, ":z_difference", -1),
	      (try_end),
	      (store_mul, ":z_difference_mul_3", ":z_difference", 3),
	      (val_add, ":dist", ":z_difference_mul_3"),
	      (store_random_in_range, ":random_value", 0, 200),
	      (store_add, ":400_plus_random_200", 400, ":random_value"),
	      (le, ":dist", ":400_plus_random_200"),
	      
 		  (call_script, "script_activate_tavern_attackers"),
  		  (start_mission_conversation, "trp_belligerent_drunk"),
  		  (assign, "$g_start_belligerent_drunk_fight", 2),
	    (try_end),  
	  ]),
	  	  
	  #tavern brawl triggers - assassin
      (2, 0, 0, [
	    (neg|conversation_screen_is_active),
		(eq, "$talk_context", tc_tavern_talk),
		(troop_slot_eq, "trp_hired_assassin", slot_troop_cur_center, "$g_encountered_party"),		
	  ], 
	  [
	    (try_begin),
	      (eq, "$g_start_hired_assassin_fight", 0),
	      (assign, "$g_start_hired_assassin_fight", 1),
	      
	      (try_for_agents, ":cur_agent"),
	        (agent_get_troop_id, ":cur_agent_troop", ":cur_agent"),
	        (eq, ":cur_agent_troop", "trp_hired_assassin"),
	        (assign, "$g_hired_assassin", ":cur_agent"),
	      (try_end),	      
	    (else_try),  
	      (eq, "$g_start_hired_assassin_fight", 1),

	      (agent_is_active, "$g_hired_assassin"),
	      (agent_is_alive, "$g_hired_assassin"),
	      (get_player_agent_no, ":player_agent"),
	      (agent_get_position, pos0, ":player_agent"),
	      (agent_get_position, pos1, "$g_hired_assassin"),
	      (get_distance_between_positions, ":dist", pos0, pos1),
	      (position_get_z, ":pos0_z", pos0),
	      (position_get_z, ":pos1_z", pos1),
	      (store_sub, ":z_difference", ":pos1_z", ":pos0_z"),
	      (try_begin),
	        (le, ":z_difference", 0),
	        (val_mul, ":z_difference", -1),
	      (try_end),
	      (store_mul, ":z_difference_mul_3", ":z_difference", 3),
	      (val_add, ":dist", ":z_difference_mul_3"),
	      (store_random_in_range, ":random_value", 0, 200),
	      (store_add, ":400_plus_random_200", 400, ":random_value"),
	      (le, ":dist", ":400_plus_random_200"),

		  (call_script, "script_activate_tavern_attackers"),
		  (assign, "$g_start_hired_assassin_fight", 2),
		(try_end),  
	  ]),
	  	  
	  #Aftermath talks
      (3, 0, ti_once, 
      [
	    (neg|conversation_screen_is_active),
		(eq, "$talk_context", tc_tavern_talk),
		(gt, "$g_main_attacker_agent", 0),
				
		(this_or_next|neg|agent_is_alive, "$g_main_attacker_agent"),
		(agent_is_wounded, "$g_main_attacker_agent"),
      ],
      [
        (mission_enable_talk),
      
		(try_for_agents, ":agent"),
		  (agent_is_alive, ":agent"),
		  (agent_get_position, pos4, ":agent"),
		  (agent_set_scripted_destination, ":agent", pos4),
		(try_end),
		
		(party_get_slot, ":tavernkeeper", "$g_encountered_party", slot_town_tavernkeeper),
		(start_mission_conversation, ":tavernkeeper"),	 
	  ]),

	  
	  #Aftermath talks
      (3, 0, ti_once, 
      [
	    (neg|conversation_screen_is_active),
		(eq, "$talk_context", tc_tavern_talk),
		(gt, "$g_main_attacker_agent", 0),
		(main_hero_fallen),		
      ],
      [
	  (jump_to_menu, "mnu_lost_tavern_duel"),
	  (finish_mission,0)
	  
	  ]),	  
	  
	  #gekokujo SHOOTING ALLOWED IN THE TAVERN
	  #No shooting in the tavern
#      (1, 0, 0, 
#      [
#	    (neg|conversation_screen_is_active),
#		(eq, "$talk_context", tc_tavern_talk),
#		(gt, "$g_main_attacker_agent", 0),
#		
#		(get_player_agent_no, ":player_agent"),
#		(agent_is_alive, ":player_agent"),
#		
#		(agent_get_wielded_item, ":wielded_item", ":player_agent", 0),
#		(is_between, ":wielded_item", "itm_darts", "itm_torch"),
#		(neq, ":wielded_item", "itm_javelin_melee"),
#		(neq, ":wielded_item", "itm_throwing_spear_melee"),
#		(neq, ":wielded_item", "itm_jarid_melee"),
#		(neq, ":wielded_item", "itm_light_throwing_axes_melee"),
#		(neq, ":wielded_item", "itm_throwing_axes_melee"),
#		(neq, ":wielded_item", "itm_heavy_throwing_axes_melee"),
#      ], 
#      [
#		(party_get_slot, ":tavernkeeper", "$g_encountered_party", slot_town_tavernkeeper),
#		##diplomacy start+
#		#Turn of this !@#$%ing obnoxious and totally illogical restriction provided:
#		(try_begin),
#			#1) there is an actual fight
#			(gt, "$g_main_attacker_agent", 0),
#			(agent_is_alive, "$g_main_attacker_agent"),
#			(neg|agent_is_wounded, "$g_main_attacker_agent"),
#			#2) the player is the lord of this town, a mercenary captain in the kingdom's employ, or ruler of this kingdom
#			(store_faction_of_party , ":center_faction", "$g_encountered_party"),
#			(this_or_next|eq, ":center_faction", "$players_kingdom"),
#				(eq, ":center_faction", "fac_player_supporters_faction"),
#		(else_try),
#		#Else, original behavior:
#			(start_mission_conversation, ":tavernkeeper"),
#		(try_end),
#		##diplomacy stop+
#	  ]),
	  	  	  
	  #Check for weapon in hand of attacker, also, everyone gets out of the way
      (1, 0, 0, 
      [
		(gt, "$g_main_attacker_agent", 0),	
      ],
      [
        (agent_get_wielded_item, ":wielded_item", "$g_main_attacker_agent", 0),
        (val_max, "$g_attacker_drawn_weapon", ":wielded_item"),               
        
        (call_script, "script_neutral_behavior_in_fight"),
      ]),	  			
    ] + bodyguard_triggers,
  ),
  
#----------------------------------------------------------------
#mission templates before this point are hardwired into the game.
#-----------------------------------------------------------------

  (
    "town_center",0,-1,
    "Default town visit",
    [(0,mtef_scene_source|mtef_team_0,af_override_horse,0,1,pilgrim_disguise),
     (1,mtef_scene_source|mtef_team_0,0,0,1,[]),
     (2,mtef_scene_source|mtef_team_0,af_override_horse,0,1,pilgrim_disguise),
     (3,mtef_scene_source|mtef_team_0,af_override_horse,0,1,pilgrim_disguise),
     (4,mtef_scene_source|mtef_team_0,af_override_horse,0,1,pilgrim_disguise),
     (5,mtef_scene_source|mtef_team_0,af_override_horse,0,1,pilgrim_disguise),
     (6,mtef_scene_source|mtef_team_0,af_override_horse,0,1,pilgrim_disguise),
     (7,mtef_scene_source|mtef_team_0,af_override_horse,0,1,pilgrim_disguise),     
     (8,mtef_visitor_source,af_override_horse,0,1,[]),
     (9,mtef_visitor_source,af_override_horse,0,1,[]),(10,mtef_visitor_source,af_override_horse,0,1,[]),(11,mtef_visitor_source,af_override_horse,0,1,[]),(12,mtef_visitor_source,af_override_horse,0,1,[]),(13,mtef_visitor_source,0,0,1,[]),(14,mtef_scene_source,0,0,1,[]),(15,mtef_scene_source,0,0,1,[]),
     (16,mtef_visitor_source,af_override_horse,0,1,[]),(17,mtef_visitor_source,af_override_horse,0,1,[]),(18,mtef_visitor_source,af_override_horse,0,1,[]),(19,mtef_visitor_source,af_override_horse,0,1,[]),(20,mtef_visitor_source,af_override_horse,0,1,[]),(21,mtef_visitor_source,af_override_horse,0,1,[]),(22,mtef_visitor_source,af_override_horse,0,1,[]),
	 (23,mtef_visitor_source,af_override_horse,0,1,[]), #guard
     (24,mtef_visitor_source,af_override_horse,0,1,[]), #guard
	 (25,mtef_visitor_source,af_override_horse,0,1,[]), #guard
	 (26,mtef_visitor_source,af_override_horse,0,1,[]), #guard
	 (27,mtef_visitor_source,af_override_horse,0,1,[]), #guard
	 (28,mtef_visitor_source,af_override_horse,0,1,[]), #guard
	 (29,mtef_visitor_source,af_override_horse,0,1,[]),
	 (30,mtef_visitor_source,af_override_horse,0,1,[]),
	 (31,mtef_visitor_source,af_override_horse,0,1,[]),
     (32,mtef_visitor_source,af_override_horse,0,1,[]),
	 (33,mtef_visitor_source,af_override_horse,0,1,[]),
	 (34,mtef_visitor_source,af_override_horse,0,1,[]),
	 (35,mtef_visitor_source,af_override_horse,0,1,[]),
	 (36,mtef_visitor_source,af_override_horse,0,1,[]), #town walker point
	 (37,mtef_visitor_source,af_override_horse,0,1,[]), #town walker point
	 (38,mtef_visitor_source,af_override_horse,0,1,[]),
	 (39,mtef_visitor_source,af_override_horse,0,1,[]),
     (40,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]), #in towns, can be used for guard reinforcements
	 (41,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]), #in towns, can be used for guard reinforcements
	 (42,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]), #in towns, can be used for guard reinforcements
	 (43,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]), #in towns, can be used for guard reinforcements
     (44,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
	 (45,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
	 (46,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
	 (47,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     ],
    [
      (ti_on_agent_spawn, 0, 0, [],
      [
        (store_trigger_param_1, ":agent_no"),
        (call_script, "script_init_town_agent", ":agent_no"),
        (try_begin),
          (this_or_next|eq, "$talk_context", tc_escape),
          (eq, "$talk_context", tc_prison_break),
          (agent_get_troop_id, ":troop_no", ":agent_no"),		  
          (troop_slot_eq, ":troop_no", slot_troop_will_join_prison_break, 1),
          (agent_set_team, ":agent_no", 0),
          (agent_ai_set_aggressiveness, ":agent_no", 5),
          (troop_set_slot, ":troop_no", slot_troop_will_join_prison_break, 0),
          (try_begin),
            (troop_slot_eq, ":troop_no", slot_troop_mission_participation, mp_prison_break_stand_back),
            (agent_get_position, pos1, ":agent_no"),            
            (agent_set_scripted_destination, ":agent_no", pos1),
          (try_end),
        (try_end),         
      ]),

      (ti_before_mission_start, 0, 0, [],
      [
        (assign, "$g_main_attacker_agent", 0),
	  ]),
		 
      (1, 0, ti_once, 
      [],
      [
        (try_begin),
          (eq, "$g_mt_mode", tcm_default),
          (store_current_scene, ":cur_scene"),
          (scene_set_slot, ":cur_scene", slot_scene_visited, 1),
        (try_end),
        (call_script, "script_init_town_walker_agents"),
        (try_begin),
          (eq, "$sneaked_into_town", 1),
          (call_script, "script_music_set_situation_with_culture", mtf_sit_town_infiltrate),
        (else_try),
          (call_script, "script_music_set_situation_with_culture", mtf_sit_town),
        (try_end),
      ]),

      (ti_before_mission_start, 0, 0, 
      [], 
      [
        (call_script, "script_change_banners_and_chest")
      ]),
        
      (ti_inventory_key_pressed, 0, 0,
      [
        (try_begin),
          (eq, "$g_mt_mode", tcm_default),
          (set_trigger_result,1),
        (else_try),
          (eq, "$g_mt_mode", tcm_disguised),
          (display_message,"str_cant_use_inventory_disguised"),
        (else_try),
          (display_message, "str_cant_use_inventory_now"),
        (try_end),
      ], 
      []),
       
      (ti_tab_pressed, 0, 0,
      [
        (try_begin),
          (this_or_next|eq, "$talk_context", tc_escape),
          (eq, "$talk_context", tc_prison_break),
          (display_message, "str_cannot_leave_now"),
        (else_try),
          (this_or_next|eq, "$g_mt_mode", tcm_default),
          (eq, "$g_mt_mode", tcm_disguised),
          (mission_enable_talk),
          (set_trigger_result,1),
        (else_try),
          (display_message, "str_cannot_leave_now"),
        (try_end),
      ], 
      []),

      (ti_on_leave_area, 0, 0,
      [
        (try_begin),
          (eq, "$g_defending_against_siege", 0),
          (assign,"$g_leave_town",1),
        (try_end),			
      ], 
      [
        (try_begin),
          (eq, "$talk_context", tc_escape),
          (call_script, "script_deduct_casualties_from_garrison"),
          (jump_to_menu,"mnu_sneak_into_town_caught_dispersed_guards"),
        (try_end),
        
        (mission_enable_talk),
      ]),            

     (0, 0, ti_once, 
     [], 
     [
       (party_slot_eq, "$current_town", slot_party_type, spt_town),
       (call_script, "script_town_init_doors", 0),
       (try_begin),
         (eq, "$town_nighttime", 0),
         (play_sound, "snd_town_ambiance", sf_looping),
       (try_end),
     ]),

	(3, 0, 0, 
	[
	  (call_script, "script_tick_town_walkers")
	], 
	[]),
	
    (2, 0, 0, 
    [
      (call_script, "script_center_ambiance_sounds")
    ], 
    []),
		
	#JAILBREAK TRIGGERS 
	#Civilians get out of the way
    (1, 0, 0,
	[
	  (this_or_next|eq, "$talk_context", tc_prison_break),
      (eq, "$talk_context", tc_escape),		
	],
	[
	  #(agent_get_team, ":prisoner_agent", 0),
	  (call_script, "script_neutral_behavior_in_fight"),
	  (mission_disable_talk),	  	  
	]),

	#The game begins with the town alerted
    (1, 0, ti_once, 
      [
        #If I set this to 1, 0, ti_once, then the prisoner spawns twice
        (eq, "$talk_context", tc_escape),
	  ],	  
	  [
		(get_player_agent_no, ":player_agent"),
	    (assign, reg6, ":player_agent"),
		(call_script, "script_activate_town_guard"),		
		
		(get_player_agent_no, ":player_agent"),
		(agent_get_position, pos4, ":player_agent"),
		
		(try_for_range, ":prisoner", active_npcs_begin, kingdom_ladies_end),		
		  (troop_slot_ge, ":prisoner", slot_troop_mission_participation, mp_prison_break_fight),

		  (str_store_troop_name, s4, ":prisoner"),
		  (display_message, "str_s4_joins_prison_break"),
			
		  (store_current_scene, ":cur_scene"), #this might be a better option?
		  (modify_visitors_at_site, ":cur_scene"),
			            
          #<entry_no>,<troop_id>,<number_of_troops>, <team_no>, <group_no>), 
          #team no and group no are used in multiplayer mode only. default team in entry is used in single player mode            
          (store_current_scene, ":cur_scene"),
          (modify_visitors_at_site, ":cur_scene"),                      
          (add_visitors_to_current_scene, 24, ":prisoner", 1, 0, 0),
          (troop_set_slot, ":prisoner", slot_troop_will_join_prison_break, 1),					          
        (try_end),
	  ]),
	
   (3, 0, 0, 
   [     
     (main_hero_fallen, 0),
   ],	  
   [
     (try_begin),
       (this_or_next|eq, "$talk_context", tc_prison_break),
       (eq, "$talk_context", tc_escape),
       
       (call_script, "script_deduct_casualties_from_garrison"),
	   (jump_to_menu,"mnu_captivity_start_castle_defeat"), 
	 
	   (assign, ":end_cond", kingdom_ladies_end),
       (try_for_range, ":prisoner", active_npcs_begin, ":end_cond"),
  	     (troop_set_slot, ":prisoner", slot_troop_mission_participation, 0), #new	  
  	   (try_end),  
	 
	   (mission_enable_talk),
	   (finish_mission, 0),
	 (else_try),  
	   (set_trigger_result,1),
	 (try_end),	 	 
   ]),
		
   (3, 0, 0, 
   [
     (eq, "$talk_context", tc_escape),
	 (neg|main_hero_fallen,0),
     (store_mission_timer_a, ":time"),
     (ge, ":time", 10),
		
     (all_enemies_defeated), #1 is default enemy team for in-town battles
   ],	  
   [
     (call_script, "script_deduct_casualties_from_garrison"),
	 (try_for_agents, ":agent"),
	 (agent_get_troop_id, ":troop", ":agent"),
       (troop_slot_ge, ":troop", slot_troop_mission_participation, mp_prison_break_fight),
       (try_begin),
         (agent_is_alive, ":agent"),
         (troop_set_slot, ":troop", slot_troop_mission_participation, mp_prison_break_escaped),
       (else_try),	
         (troop_set_slot, ":troop", slot_troop_mission_participation, mp_prison_break_caught),
       (try_end),
     (try_end),
     (jump_to_menu,"mnu_sneak_into_town_caught_ran_away"),
     
     (mission_enable_talk),
     (finish_mission,0)
   ]),
   
   (ti_on_agent_killed_or_wounded, 0, 0, [],
   [
     (store_trigger_param_1, ":dead_agent_no"),
     (store_trigger_param_2, ":killer_agent_no"),
     #(store_trigger_param_3, ":is_wounded"),
        
     (agent_get_troop_id, ":dead_agent_troop_no", ":dead_agent_no"),
     (agent_get_troop_id, ":killer_agent_troop_no", ":killer_agent_no"),
                
     (try_begin), 
       (this_or_next|eq, ":dead_agent_troop_no", "trp_gekokujo_uesugi_prison_guard"),
       (this_or_next|eq, ":dead_agent_troop_no", "trp_gekokujo_date_prison_guard"),
       (this_or_next|eq, ":dead_agent_troop_no", "trp_gekokujo_oda_prison_guard"),
       (this_or_next|eq, ":dead_agent_troop_no", "trp_gekokujo_mori_prison_guard"),
       (this_or_next|eq, ":dead_agent_troop_no", "trp_gekokujo_takeda_prison_guard"),
       (this_or_next|eq, ":dead_agent_troop_no", "trp_gekokujo_tokugawa_prison_guard"),
       (this_or_next|eq, ":dead_agent_troop_no", "trp_gekokujo_miyoshi_prison_guard"),
       (this_or_next|eq, ":dead_agent_troop_no", "trp_gekokujo_amako_prison_guard"),
       (this_or_next|eq, ":dead_agent_troop_no", "trp_gekokujo_otomo_prison_guard"),
       (this_or_next|eq, ":dead_agent_troop_no", "trp_gekokujo_nanbu_prison_guard"),
       (this_or_next|eq, ":dead_agent_troop_no", "trp_gekokujo_asakura_prison_guard"),
       (this_or_next|eq, ":dead_agent_troop_no", "trp_gekokujo_chosokabe_prison_guard"),
       (this_or_next|eq, ":dead_agent_troop_no", "trp_gekokujo_hojo_prison_guard"),
       (this_or_next|eq, ":dead_agent_troop_no", "trp_gekokujo_mogami_prison_guard"),
       (this_or_next|eq, ":dead_agent_troop_no", "trp_gekokujo_shimazu_prison_guard"),
       (this_or_next|eq, ":dead_agent_troop_no", "trp_gekokujo_ryuzoji_prison_guard"),
       (this_or_next|eq, ":dead_agent_troop_no", "trp_gekokujo_satake_prison_guard"),
       (this_or_next|eq, ":dead_agent_troop_no", "trp_gekokujo_satomi_prison_guard"),
       (this_or_next|eq, ":dead_agent_troop_no", "trp_gekokujo_ukita_prison_guard"),
       (eq, ":dead_agent_troop_no", "trp_gekokujo_ikko_prison_guard"),
          
       (eq, ":killer_agent_troop_no", "trp_player"),
          
       (display_message, "@You got the keys of rhe prison."),
     (try_end),
   ]),     
  ] + bodyguard_triggers),
  (
    "village_center",0,-1,
    "village center",
    [(0,mtef_scene_source|mtef_team_0,0,0,1,[]),
     (1,mtef_scene_source|mtef_team_0,0,0,1,[]),
     (2,mtef_scene_source|mtef_team_0,af_override_horse,0,1,[]),
     (3,mtef_scene_source|mtef_team_0,af_override_horse,0,1,[]),
     (4,mtef_scene_source|mtef_team_0,af_override_horse,0,1,[]),
     (5,mtef_scene_source|mtef_team_0,af_override_horse,0,1,[]),
     (6,mtef_scene_source|mtef_team_0,af_override_horse,0,1,[]),
     (7,mtef_scene_source|mtef_team_0,af_override_horse,0,1,[]),
     
     (8,mtef_visitor_source,af_override_horse,0,1,[]),
     (9,mtef_visitor_source,af_override_horse,0,1,[]),(10,mtef_visitor_source,af_override_horse,0,1,[]),(11,mtef_visitor_source,af_override_horse,0,1,[]),(12,mtef_visitor_source,af_override_horse,0,1,[]),(13,mtef_visitor_source,0,0,1,[]),(14,mtef_visitor_source,0,0,1,[]),(15,mtef_visitor_source,0,0,1,[]),
     (16,mtef_visitor_source,af_override_horse,0,1,[]),(17,mtef_visitor_source,af_override_horse,0,1,[]),(18,mtef_visitor_source,af_override_horse,0,1,[]),(19,mtef_visitor_source,af_override_horse,0,1,[]),(20,mtef_visitor_source,af_override_horse,0,1,[]),(21,mtef_visitor_source,af_override_horse,0,1,[]),(22,mtef_visitor_source,af_override_horse,0,1,[]),(23,mtef_visitor_source,af_override_horse,0,1,[]),
     (24,mtef_visitor_source,af_override_horse,0,1,[]),(25,mtef_visitor_source,af_override_horse,0,1,[]),(26,mtef_visitor_source,af_override_horse,0,1,[]),(27,mtef_visitor_source,af_override_horse,0,1,[]),(28,mtef_visitor_source,af_override_horse,0,1,[]),(29,mtef_visitor_source,af_override_horse,0,1,[]),(30,mtef_visitor_source,af_override_horse,0,1,[]),(31,mtef_visitor_source,af_override_horse,0,1,[]),
     (32,mtef_visitor_source,af_override_horse,0,1,[]),(33,mtef_visitor_source,af_override_horse,0,1,[]),(34,mtef_visitor_source,af_override_horse,0,1,[]),(35,mtef_visitor_source,af_override_horse,0,1,[]),(36,mtef_visitor_source,af_override_horse,0,1,[]),(37,mtef_visitor_source,af_override_horse,0,1,[]),(38,mtef_visitor_source,af_override_horse,0,1,[]),(39,mtef_visitor_source,af_override_horse,0,1,[]),
     (40,mtef_visitor_source,af_override_horse,0,1,[]),(41,mtef_visitor_source,af_override_horse,0,1,[]),(42,mtef_visitor_source,af_override_horse,0,1,[]),(43,mtef_visitor_source,af_override_horse,0,1,[]),(44,mtef_visitor_source,af_override_horse,0,1,[]),(45,mtef_visitor_source,af_override_horse,0,1,[]),(46,mtef_visitor_source,af_override_horse,0,1,[]),(47,mtef_visitor_source,af_override_horse,0,1,[]),
     ],
    [
      (1, 0, ti_once, [], [
          (store_current_scene, ":cur_scene"),
          (scene_set_slot, ":cur_scene", slot_scene_visited, 1),
          (call_script, "script_init_town_walker_agents"),
          (call_script, "script_music_set_situation_with_culture", mtf_sit_travel),
        ]),
	  #gekokujo 3.0 microfactions! start
	  #let's just not trigger this when it's a fort, mmkay?
      #(ti_before_mission_start, 0, 0, [], [(call_script, "script_change_banners_and_chest")]),
      (ti_before_mission_start, 0, 0, [(neg|party_slot_eq, "$current_town", slot_party_type, spt_fort)], [(call_script, "script_change_banners_and_chest")]),
	  #gekokujo 3.0 microfactions! end
      (ti_inventory_key_pressed, 0, 0, [(set_trigger_result,1)], []),
      (ti_tab_pressed, 0, 0, [(try_begin),
                                (check_quest_active, "qst_hunt_down_fugitive"),
                                (neg|check_quest_succeeded, "qst_hunt_down_fugitive"),
                                (neg|check_quest_failed, "qst_hunt_down_fugitive"),
                                (quest_slot_eq, "qst_hunt_down_fugitive", slot_quest_current_state, 1),
                                (try_begin),
                                  (call_script, "script_cf_troop_agent_is_alive", "trp_fugitive"),
                                  (call_script, "script_fail_quest", "qst_hunt_down_fugitive"),
                                (else_try),
                                  (call_script, "script_succeed_quest", "qst_hunt_down_fugitive"),
                                (try_end),
                              (try_end),
                              (set_trigger_result,1)], []),
      (ti_on_leave_area, 0, 0, [
          (try_begin),
            (assign,"$g_leave_town",1),
          (try_end),
          ], []),
      (3, 0, 0, [(call_script, "script_tick_town_walkers")], []),
      (2, 0, 0, [(call_script, "script_center_ambiance_sounds")], []),

      (1, 0, ti_once, [(check_quest_active, "qst_hunt_down_fugitive"),
                       (neg|check_quest_succeeded, "qst_hunt_down_fugitive"),
                       (neg|check_quest_failed, "qst_hunt_down_fugitive"),
                       (quest_slot_eq, "qst_hunt_down_fugitive", slot_quest_current_state, 1),
                       (assign, ":not_alive", 0),
                       (try_begin),
                         (call_script, "script_cf_troop_agent_is_alive", "trp_fugitive"),
                       (else_try),
                         (assign, ":not_alive", 1),
                       (try_end),
                       (this_or_next|main_hero_fallen),
                       (eq, ":not_alive", 1),
                       ],
       [(try_begin),
          (main_hero_fallen),
          (jump_to_menu, "mnu_village_hunt_down_fugitive_defeated"),
          (call_script, "script_fail_quest", "qst_hunt_down_fugitive"),
          (finish_mission, 4),
        (else_try),
          (call_script, "script_change_player_relation_with_center", "$current_town", -2),
          (call_script, "script_succeed_quest", "qst_hunt_down_fugitive"),
        (try_end),
        ]),
	
    ] + bodyguard_triggers,
  ),
  (
    "bandits_at_night",0,-1,
    "Default town visit",
    [(0,mtef_scene_source|mtef_team_0, af_override_horse, aif_start_alarmed, 1, pilgrim_disguise),
     (1,mtef_scene_source|mtef_team_0,0,0,1,[]),
     (2,mtef_scene_source|mtef_team_0,af_override_horse,0,1,[]),
     (3,mtef_scene_source|mtef_team_0,af_override_horse,0,1,[]),
     (4,mtef_visitor_source|mtef_team_0, af_override_horse, aif_start_alarmed, 1, []),
     (5,mtef_scene_source|mtef_team_0,af_override_horse,0,1,[]),
     (6,mtef_scene_source|mtef_team_0,af_override_horse,0,1,[]),
     (7,mtef_scene_source|mtef_team_0,af_override_horse,0,1,[]),
     
     (8,mtef_scene_source,af_override_horse,0,1,[]),
     (9,mtef_visitor_source,af_override_horse,0,1,[]),(10,mtef_visitor_source,af_override_horse,0,1,[]),(11,mtef_visitor_source,af_override_horse,aif_start_alarmed,1,[]),(12,mtef_visitor_source,af_override_horse,0,1,[]),(13,mtef_scene_source,0,0,1,[]),(14,mtef_scene_source,0,0,1,[]),(15,mtef_scene_source,0,0,1,[]),
     (16,mtef_visitor_source,af_override_horse,0,1,[]),(17,mtef_visitor_source,af_override_horse,0,1,[]),(18,mtef_visitor_source,af_override_horse,0,1,[]),(19,mtef_visitor_source,af_override_horse,0,1,[]),(20,mtef_visitor_source,af_override_horse,0,1,[]),(21,mtef_visitor_source,af_override_horse,0,1,[]),(22,mtef_visitor_source,af_override_horse,0,1,[]),(23,mtef_visitor_source,af_override_horse,0,1,[]),
     (24,mtef_visitor_source,af_override_horse,0,1,[]),(25,mtef_visitor_source,af_override_horse,0,1,[]),(26,mtef_visitor_source,af_override_horse,0,1,[]),(27,mtef_visitor_source,af_override_horse,aif_start_alarmed,1,[]),(28,mtef_visitor_source,af_override_horse,aif_start_alarmed,1,[]),(29,mtef_visitor_source,af_override_horse,0,1,[]),(30,mtef_visitor_source,af_override_horse,0,1,[]),(31,mtef_visitor_source,af_override_horse,0,1,[]),
     (32,mtef_visitor_source,af_override_horse,0,1,[]),(33,mtef_visitor_source,af_override_horse,0,1,[]),(34,mtef_visitor_source,af_override_horse,0,1,[]),(35,mtef_visitor_source,af_override_horse,0,1,[]),(36,mtef_visitor_source,af_override_horse,0,1,[]),(37,mtef_visitor_source,af_override_horse,0,1,[]),(38,mtef_visitor_source,af_override_horse,0,1,[]),(39,mtef_visitor_source,af_override_horse,0,1,[]),
     (40,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),(41,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),(42,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),(43,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     (44,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),(45,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),(46,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),(47,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     ],
    [
      (ti_on_agent_spawn, 0, 0, [],
       [
         (store_trigger_param_1, ":agent_no"),
         (agent_get_troop_id, ":troop_no", ":agent_no"),
         (neq, ":troop_no", "trp_player"),
         (agent_set_team, ":agent_no", 1),
         ]),

      (ti_before_mission_start, 0, 0, [], [(call_script, "script_change_banners_and_chest")]),

      common_inventory_not_available,
      
      (ti_tab_pressed, 0, 0,
       [
         (display_message, "str_cannot_leave_now"),
         ], []),
      (ti_on_leave_area, 0, 0,
       [
         (try_begin),
           (eq, "$g_defending_against_siege", 0),
           (assign,"$g_leave_town",1),
         (try_end),
         ], []),

      (0, 0, ti_once, [],
       [
         (call_script, "script_music_set_situation_with_culture", mtf_sit_ambushed),
         (set_party_battle_mode),
         (party_slot_eq, "$current_town", slot_party_type, spt_town),
         (call_script, "script_town_init_doors", 0),
        ]),

      (1, 4, ti_once,
       [
         (store_mission_timer_a,":cur_time"),
         (ge, ":cur_time", 5),
         (this_or_next|main_hero_fallen),
         (num_active_teams_le,1)
         ],
       [
         (try_begin),
           (main_hero_fallen),
           (jump_to_menu, "mnu_town_bandits_failed"),
         (else_try),
           (jump_to_menu, "mnu_town_bandits_succeeded"),
         (try_end),
         (finish_mission),
         ]),
      ] + bodyguard_triggers,
    ),
  
  (
    "village_training", mtf_arena_fight, -1,
    "village_training",
    [(2,mtef_visitor_source|mtef_team_0,af_override_everything,aif_start_alarmed,1,[itm_gekokujo_practice_jo, itm_gekokujo_sandal_2]),
     (4,mtef_visitor_source|mtef_team_1,af_override_everything,aif_start_alarmed,1,[itm_gekokujo_practice_jo, itm_gekokujo_sandal_2]),
     ],
    [
      (ti_before_mission_start, 0, 0, [],
       [
         (assign, "$g_train_peasants_against_bandits_training_succeeded", 0),
         (call_script, "script_change_banners_and_chest"),
         ]),
      
      common_arena_fight_tab_press,
      
      (ti_question_answered, 0, 0, [],
       [
         (store_trigger_param_1,":answer"),
         (eq,":answer",0),
         (finish_mission),
         ]),
      
      common_inventory_not_available,

      (1, 4, ti_once,
       [
         (this_or_next|main_hero_fallen),
         (num_active_teams_le, 1)
         ],
       [
         (try_begin),
           (neg|main_hero_fallen),
           (assign, "$g_train_peasants_against_bandits_training_succeeded", 1),
         (try_end),
         (finish_mission),
         ]),
      ],
    ),
		  
  (
    "back_alley_kill_local_merchant",mtf_battle_mode,-1,
    "You enter the back alley",
    [
      (0,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
      (3,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
    ],
    [
      common_inventory_not_available,
      (ti_tab_pressed, 0, 0, [(display_message,"str_cannot_leave_now")], []),
      (ti_before_mission_start, 0, 0, [], [(call_script, "script_change_banners_and_chest")]),

      (0, 0, ti_once, [],
       [
         (call_script, "script_music_set_situation_with_culture", mtf_sit_ambushed),
         ]),

      (0, 0, ti_once, [
          (store_mission_timer_a,":cur_time"),
          (ge,":cur_time",1), 
          (assign, ":merchant_hp", 0),
          (assign, ":player_hp", 0),
          (assign, ":merchant_hp", 0),
          (assign, ":merchant_agent", -1),
          (assign, ":player_agent", -1),
          (try_for_agents, ":agent_no"),
            (agent_get_troop_id, ":troop_id", ":agent_no"),
            (try_begin),
              (eq, ":troop_id", "trp_local_merchant"),
              (store_agent_hit_points, ":merchant_hp", ":agent_no"),
              (assign, ":merchant_agent", ":agent_no"),
            (else_try),
              (eq, ":troop_id", "trp_player"),
              (store_agent_hit_points, ":player_hp",":agent_no"),
              (assign, ":player_agent", ":agent_no"),
            (try_end),
          (try_end),
          (ge, ":player_agent", 0),
          (ge, ":merchant_agent", 0),
          (agent_is_alive, ":player_agent"),
          (agent_is_alive, ":merchant_agent"),
          (is_between, ":merchant_hp", 1, 30),
          (gt, ":player_hp", 50),
          (start_mission_conversation, "trp_local_merchant"),
          ], []),
      
      (1, 4, ti_once, [(assign, ":not_alive", 0),
                       (try_begin),
                         (call_script, "script_cf_troop_agent_is_alive", "trp_local_merchant"),
                       (else_try),
                         (assign, ":not_alive", 1),
                       (try_end),
                       (this_or_next|main_hero_fallen),
                       (eq, ":not_alive", 1)],
       [
           (try_begin),
             (main_hero_fallen),
             (call_script, "script_fail_quest", "qst_kill_local_merchant"),
           (else_try),
             (call_script, "script_change_player_relation_with_center", "$current_town", -4),
             (call_script, "script_succeed_quest", "qst_kill_local_merchant"),
           (try_end),
           (finish_mission),
           ]),
    ],
  ),
  (
    "back_alley_revolt",mtf_battle_mode,charge,
    "You lead your men to battle.",
    [(0,mtef_team_0|mtef_use_exact_number,af_override_horse|af_override_weapons|af_override_head,aif_start_alarmed,4,[itm_gekokujo_bo]),
     (3,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     ],
    [
      common_inventory_not_available,

      common_battle_init_banner,

      (ti_tab_pressed, 0, 0, [],
       [(question_box,"str_do_you_want_to_retreat"),
        ]),
      (ti_question_answered, 0, 0, [],
       [(store_trigger_param_1,":answer"),
        (eq,":answer",0),
        (jump_to_menu, "mnu_collect_taxes_failed"),
        (finish_mission),]),

      (ti_tab_pressed, 0, 0, [(display_message,"str_cannot_leave_now")], []),
      (ti_before_mission_start, 0, 0, [], [(call_script, "script_change_banners_and_chest")]),

      (0, 0, ti_once, [],
       [
         (call_script, "script_music_set_situation_with_culture", mtf_sit_fight),
         ]),

      (1, 4, ti_once, [(this_or_next|main_hero_fallen),(num_active_teams_le,1)],
       [
           (try_begin),
             (main_hero_fallen),
             (jump_to_menu, "mnu_collect_taxes_failed"),
           (else_try),
             (jump_to_menu, "mnu_collect_taxes_rebels_killed"),
           (try_end),
           (finish_mission),
           ]),
    ],
  ),
  (
    "village_attack_bandits",mtf_battle_mode|mtf_synch_inventory,charge,
    "You lead your men to battle.",
    [
     (3,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
     (1,mtef_team_0|mtef_use_exact_number,0,aif_start_alarmed, 7,[]),
     (1,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
     ],
     trigger_cannon+
    [
      common_battle_tab_press,
      common_battle_init_banner,

      (ti_question_answered, 0, 0, [],
       [(store_trigger_param_1,":answer"),
        (eq,":answer",0),
        (assign, "$pin_player_fallen", 0),
        (str_store_string, s5, "str_retreat"),
        (call_script, "script_simulate_retreat", 10, 20, 1),
        (assign, "$g_battle_result", -1),
        (call_script, "script_count_mission_casualties_from_agents"),
        (finish_mission,0),]),

      (0, 0, ti_once, [], [(assign, "$g_battle_won", 0),
                           (assign, "$defender_reinforcement_stage", 0),
                           (assign, "$attacker_reinforcement_stage", 0),
                           (try_begin),
                             (eq, "$g_mt_mode", vba_after_training),
                             (add_reinforcements_to_entry, 1, 6),
                           (else_try),
                             (add_reinforcements_to_entry, 1, 29),
                           (try_end),
                           (call_script, "script_combat_music_set_situation_with_culture"),
                           ]),

      common_music_situation_update,
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

      common_battle_inventory,      
      common_battle_order_panel,
      common_battle_order_panel_tick,

    ]
    ##diplomacy begin
    + dplmc_battle_mode_triggers,
    ##diplomacy end
  ),
  (
    "village_raid",mtf_battle_mode|mtf_synch_inventory,charge,
    "You lead your men to battle.",
    [
     (3,mtef_defenders|mtef_team_0,af_override_horse,aif_start_alarmed,12,[]),
     (3,mtef_defenders|mtef_team_0,0,aif_start_alarmed,0,[]),
     (1,mtef_attackers|mtef_team_1,0,aif_start_alarmed,12,[]),
     (1,mtef_attackers|mtef_team_1,0,aif_start_alarmed,0,[]),
     ],
     trigger_cannon+
    [
      common_battle_tab_press,
      common_battle_init_banner,

      (ti_question_answered, 0, 0, [],
       [(store_trigger_param_1,":answer"),
        (eq,":answer",0),
        (assign, "$pin_player_fallen", 0),
        (str_store_string, s5, "str_retreat"),
        (call_script, "script_simulate_retreat", 10, 20, 1),
        (call_script, "script_count_mission_casualties_from_agents"),
        (finish_mission,0),]),

      (0, 0, ti_once, [], [(assign,"$g_battle_won",0),
                           (assign,"$defender_reinforcement_stage",0),
                           (assign,"$attacker_reinforcement_stage",0),
                           (call_script, "script_combat_music_set_situation_with_culture"),
                           ]),

      common_music_situation_update,
      common_battle_check_friendly_kills,

      (1, 0, 5, [(lt,"$defender_reinforcement_stage",2),
                 (store_mission_timer_a,":mission_time"),
                 (ge,":mission_time",10),
                 (store_normalized_team_count,":num_defenders", 0),
                 (lt,":num_defenders",6)],
           [(add_reinforcements_to_entry,0,6),(val_add,"$defender_reinforcement_stage",1)]),
      (1, 0, 5, [(lt,"$attacker_reinforcement_stage",2),
                 (store_mission_timer_a,":mission_time"),
                 (ge,":mission_time",10),
                 (store_normalized_team_count,":num_attackers", 1),
                 (lt,":num_attackers",6)],
           [(add_reinforcements_to_entry,3,6),(val_add,"$attacker_reinforcement_stage",1)]),

      (1, 60, ti_once,
       [
         (store_mission_timer_a,reg(1)),
         (ge,reg(1),10),
         (all_enemies_defeated, 5),
         (neg|main_hero_fallen, 0),
         (set_mission_result,1),
         (display_message,"str_msg_battle_won"),
         (assign,"$g_battle_won",1),
         (assign, "$g_battle_result", 1),
         (try_begin),
           (eq, "$g_village_raid_evil", 0),
           (call_script, "script_play_victorious_sound"),
         (else_try),
           (play_track, "track_victorious_evil", 1),
         (try_end),
         ],
       [
         (call_script, "script_count_mission_casualties_from_agents"),
         (finish_mission, 1),
         ]),

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
      common_battle_order_panel,
      common_battle_order_panel_tick,

##      #AI Tiggers
##      (0, 0, ti_once, [
##          (store_mission_timer_a,reg(1)),(ge,reg(1),4),
##          (call_script, "script_select_battle_tactic"),
##          (call_script, "script_battle_tactic_init"),
##          ], []),
##      (1, 0, 0, [
##          (store_mission_timer_a,reg(1)),(ge,reg(1),4),
##          (call_script, "script_battle_tactic_apply"),
##          ], []),
    ]
    ##diplomacy begin
    + dplmc_battle_mode_triggers,
    ##diplomacy end
  ),
  
  (
	"bandit_lair",mtf_battle_mode|mtf_synch_inventory,charge,
    "Ambushing a bandit lair",
    [
      (0,mtef_team_0|mtef_use_exact_number,af_override_horse, aif_start_alarmed, 7,[]),
      (1,mtef_visitor_source|mtef_team_1,af_override_horse, aif_start_alarmed,20,[]),
      (2,mtef_visitor_source|mtef_team_1,af_override_horse, aif_start_alarmed,20,[]),
      (3,mtef_visitor_source|mtef_team_1,af_override_horse, aif_start_alarmed,20,[]),
      (4,mtef_visitor_source|mtef_team_1,af_override_horse, aif_start_alarmed,20,[]),
      (5,mtef_visitor_source|mtef_team_1,af_override_horse, aif_start_alarmed,20,[]),
      (6,mtef_visitor_source|mtef_team_1,af_override_horse, aif_start_alarmed,20,[]),
      (7,mtef_visitor_source|mtef_team_1,af_override_horse, aif_start_alarmed,20,[]),
      (8,mtef_visitor_source|mtef_team_1,af_override_horse, aif_start_alarmed,20,[]),
      (9,mtef_visitor_source|mtef_team_1,af_override_horse, aif_start_alarmed,20,[]),
      (10,mtef_visitor_source|mtef_team_1,af_override_horse, aif_start_alarmed,20,[]),
    ],
    [
      common_battle_init_banner,
    
      common_inventory_not_available,
      
      (ti_on_agent_spawn, 0, 0, [],
      [
        (store_trigger_param_1, ":agent_no"),
        
        (assign, "$relative_of_merchant_is_found", 0),
              
        (try_begin),
          (agent_is_human, ":agent_no"),
          (agent_is_alive, ":agent_no"),
          (agent_get_team, ":agent_team", ":agent_no"),
          (eq, ":agent_team", 1),

          (agent_get_position, pos4, ":agent_no"),
          (agent_set_scripted_destination, ":agent_no", pos4, 1),
        (try_end),  
        
        (try_begin),
          (agent_get_troop_id, ":troop_no", ":agent_no"),
          (is_between, ":troop_no", "trp_relative_of_merchant", "trp_relative_of_merchants_end"),
          (agent_set_team, ":agent_no", 7),
          (team_set_relation, 0, 7, 0),          
        (try_end),                
        ]),
        
	   (0, 0, 0, 
	   [	     
         (party_get_template_id, ":template", "$g_encountered_party"),
         (eq, ":template", "pt_looter_lair"),
         (check_quest_active, "qst_save_relative_of_merchant"),	   
         (eq, "$relative_of_merchant_is_found", 0),
	   ],
	   [
        (get_player_agent_no, ":player_agent"),
        (agent_get_position, pos0, ":player_agent"),

        (try_for_agents, ":agent_no"),
          (agent_get_troop_id, ":troop_no", ":agent_no"),
          (is_between, ":troop_no", "trp_relative_of_merchant", "trp_relative_of_merchants_end"),    
          (agent_set_scripted_destination, ":agent_no", pos0),
          (agent_get_position, pos1, ":agent_no"),
          (get_distance_between_positions, ":dist", pos0, pos1),
          (le, ":dist", 200),
          #(assign, "$g_talk_troop", "trp_relative_of_merchant"),
          (start_mission_conversation, "trp_relative_of_merchant"),
        (try_end),
	   ]),
        
      (ti_tab_pressed, 0, 0,
       [
        (display_message, "str_cannot_leave_now"),
       ], []),
     
      (1, 0, ti_once, [],
       [
        (assign, "$defender_reinforcement_stage", 0),
        (assign, "$bandits_spawned_extra", 0),
	   ]),
	   
	   (1, 0, 0, [],
	   [
        (try_for_agents, ":bandit_id"),
          (agent_is_alive, ":bandit_id"),          
          (agent_get_team, ":agent_team_1", ":bandit_id"),
          (eq, ":agent_team_1", 1),
          (agent_is_in_special_mode, ":bandit_id"),
          (agent_is_human, ":bandit_id"),
          
          (agent_get_position, pos0, ":bandit_id"),
          (try_for_agents, ":player_team_agent_id"),
            (agent_is_alive, ":player_team_agent_id"),
            (agent_get_team, ":agent_team_2", ":player_team_agent_id"),
            (eq, ":agent_team_2", 0),
            (agent_is_human, ":player_team_agent_id"),
                      
            (store_agent_hit_points, ":bandit_hit_points", ":bandit_id"),
            
            (assign, ":continue", 0),
            (try_begin),
              (lt, ":bandit_hit_points", 100),
                            
              (try_for_agents, ":bandit_2_id"),
                (agent_is_alive, ":bandit_2_id"),  
                (agent_get_team, ":bandit_2_team", ":bandit_2_id"),
                (eq, ":bandit_2_team", 1),
                (neq, ":bandit_id", ":bandit_2_id"),
                (agent_is_in_special_mode, ":bandit_2_id"),
                (agent_is_human, ":bandit_2_id"),
                
                (agent_get_position, pos1, ":bandit_id"),
                (agent_get_position, pos2, ":bandit_2_id"),                        
                (get_distance_between_positions, ":distance", pos1, pos2),
                (le, ":distance", 1000),

                (agent_clear_scripted_mode, ":bandit_2_id"),  
              (try_end),                             
              
              (assign, ":continue", 1),
            (else_try),  
              (agent_get_position, pos1, ":bandit_id"),
              (agent_get_position, pos2, ":player_team_agent_id"),                        
              (get_distance_between_positions, ":distance", pos1, pos2),                                                                        
              (le, ":distance", 4000),
              
              (try_for_agents, ":bandit_2_id"),
                (agent_is_alive, ":bandit_2_id"),  
                (agent_get_team, ":bandit_2_team", ":bandit_2_id"),
                (eq, ":bandit_2_team", 1),
                (neq, ":bandit_id", ":bandit_2_id"),
                (agent_is_in_special_mode, ":bandit_2_id"),
                (agent_is_human, ":bandit_2_id"),
                
                (agent_get_position, pos1, ":bandit_id"),
                (agent_get_position, pos2, ":bandit_2_id"),                        
                (get_distance_between_positions, ":distance", pos1, pos2),
                (le, ":distance", 1000),
                
                (agent_clear_scripted_mode, ":bandit_2_id"),  
              (try_end),                

              (assign, ":continue", 1),
            (try_end),  
            
            (eq, ":continue", 1),
            
            (agent_clear_scripted_mode, ":bandit_id"),            
          (try_end),
        (try_end),
	   ]),
	   
	   (30, 0, 0, 
	   [
	     (le, "$defender_reinforcement_stage", 1),
	   ],
	   [          
          (store_character_level, ":player_level", "trp_player"),                   
          (store_add, ":number_of_bandits_will_be_spawned_at_each_period", 5, ":player_level"),
          (val_div, ":number_of_bandits_will_be_spawned_at_each_period", 3),

          (lt, "$bandits_spawned_extra", ":number_of_bandits_will_be_spawned_at_each_period"),
          (val_add, "$bandits_spawned_extra", 1),                   

          (party_get_template_id, ":template", "$g_encountered_party"),
          (store_random_in_range, ":random_value", 0, 2),
          
          (try_begin),
            (eq, ":template", "pt_kinai_rebel_lair"),
            (eq, ":random_value", 0),
            (assign, ":bandit_troop", "trp_kinai_rebel"),
            (assign, ":bandit_troop_2", "trp_kinai_rebel"),
          (else_try),
            (eq, ":template", "pt_shinano_rebel_lair"),
            (eq, ":random_value", 0),
            (assign, ":bandit_troop", "trp_shinano_rebel"),
            (assign, ":bandit_troop_2", "trp_shinano_rebel"),
          (else_try),
            (eq, ":template", "pt_northern_raider_lair"),
            (eq, ":random_value", 0),
            (assign, ":bandit_troop", "trp_northern_raider"),
            (assign, ":bandit_troop_2", "trp_northern_raider"),
          (else_try),
            (eq, ":template", "pt_woku_pirate_lair"),
            (eq, ":random_value", 0),
            (assign, ":bandit_troop", "trp_woku_pirate"),
            (assign, ":bandit_troop_2", "trp_woku_pirate"),
          (else_try),
            (eq, ":template", "pt_kanto_rebel_lair"),
            (eq, ":random_value", 0),
            (assign, ":bandit_troop", "trp_kanto_rebel"),
            (assign, ":bandit_troop_2", "trp_kanto_rebel"),
          (else_try),
            (eq, ":template", "pt_seto_pirate_lair"),
            (eq, ":random_value", 0),
            (assign, ":bandit_troop", "trp_seto_pirate"),
            (assign, ":bandit_troop_2", "trp_seto_pirate"),
		  #gekokujo 3.0 new bandit types start
          (else_try),
            (this_or_next|eq, ":template", "pt_monk_rebel_lair"),
            (neq, ":random_value", 0),
            (assign, ":bandit_troop", "trp_monk_rebel"),
            (assign, ":bandit_troop_2", "trp_monk_rebel"),
		  #gekokujo 3.0 new bandit types end
          (else_try),
            (this_or_next|eq, ":template", "pt_looter_lair"),
            (neq, ":random_value", 0),
            (assign, ":bandit_troop", "trp_generic_ashigaru"),
            (assign, ":bandit_troop_2", "trp_generic_jizamurai"), #gekokujo 3.0 enable enemy samurai in mansion raid
          (try_end),

          (store_current_scene, ":cur_scene"), 
          (modify_visitors_at_site, ":cur_scene"),
          (store_random_in_range, ":random_entry_point", 2, 11),
		  #gekokujo 3.0 enable enemy samurai in mansion raid start
		  #we added a bandit_troop_2 variable and initialized it in all bandit lair types
		  #but it only matters for looters aka the opening quest
		  #this is also applied in the below trigger and module_game_menus
          #(add_visitors_to_current_scene, ":random_entry_point", ":bandit_troop", 1),
		  (store_random_in_range, ":random_bandit_type", 0, 6), #roll 1 to 6 (well, 0 to 5)
		  (try_begin),
		    (eq, ":random_bandit_type", 0), #roll of 1 (so 1/6 chance)
			(add_visitors_to_current_scene, ":random_entry_point", ":bandit_troop_2", 1),
		  (else_try),
		    (add_visitors_to_current_scene, ":random_entry_point", ":bandit_troop", 1),
		  (try_end),
		  #gekokujo 3.0 enable enemy samurai in mansion raid end
       ]),	   	   

      (ti_on_agent_killed_or_wounded, 0, 0, [],
       [
        (store_trigger_param_1, ":dead_agent_no"),
        #(store_trigger_param_2, ":killer_agent_no"),
        (store_trigger_param_3, ":is_wounded"),

        (try_begin),
          (ge, ":dead_agent_no", 0),
          (agent_is_human, ":dead_agent_no"),
          (agent_get_troop_id, ":dead_agent_troop_id", ":dead_agent_no"),
          (str_store_troop_name, s6, ":dead_agent_troop_id"),
          (try_begin),
            (neg|agent_is_ally, ":dead_agent_no"),
            (party_add_members, "p_total_enemy_casualties", ":dead_agent_troop_id", 1), #addition_to_p_total_enemy_casualties            
            (try_begin),
              (eq, ":is_wounded", 1),
              (party_wound_members, "p_total_enemy_casualties", ":dead_agent_troop_id", 1), 
            (try_end),  
          (try_end),  
          
          (party_add_members, "p_temp_casualties", ":dead_agent_troop_id", 1), #addition_to_p_total_enemy_casualties            
          
          (eq, ":is_wounded", 1),
          (party_wound_members, "p_temp_casualties", ":dead_agent_troop_id", 1), 
        (try_end),
        
        (assign, ":number_of_enemies", 0),
        (try_for_agents, ":cur_agent"),
          (agent_is_non_player, ":cur_agent"),
          (agent_is_human, ":cur_agent"),
          (agent_is_alive, ":cur_agent"),
          (neg|agent_is_ally, ":cur_agent"),
          (val_add, ":number_of_enemies", 1),
        (try_end),
        
        (try_begin),
          (le, ":number_of_enemies", 2),
          (le, "$defender_reinforcement_stage", 1),
          (val_add, "$defender_reinforcement_stage", 1),

          (store_character_level, ":player_level", "trp_player"),                   
          (store_add, ":number_of_bandits_will_be_spawned_at_each_period", 5, ":player_level"),
          (val_div, ":number_of_bandits_will_be_spawned_at_each_period", 3),
          (try_begin),
            (ge, "$defender_reinforcement_stage", 2),
            (val_sub, ":number_of_bandits_will_be_spawned_at_each_period", "$bandits_spawned_extra"),
          (try_end),
          
          (party_get_template_id, ":template", "$g_encountered_party"),          
          (store_random_in_range, ":random_value", 0, 2),
          
          (try_begin),
            (eq, ":template", "pt_kinai_rebel_lair"),
            (eq, ":random_value", 0),
            (assign, ":bandit_troop", "trp_kinai_rebel"),
            (assign, ":bandit_troop_2", "trp_kinai_rebel"),
          (else_try),
            (eq, ":template", "pt_shinano_rebel_lair"),
            (eq, ":random_value", 0),
            (assign, ":bandit_troop", "trp_shinano_rebel"),
            (assign, ":bandit_troop_2", "trp_shinano_rebel"),
          (else_try),
            (eq, ":template", "pt_northern_raider_lair"),
            (eq, ":random_value", 0),
            (assign, ":bandit_troop", "trp_northern_raider"),
            (assign, ":bandit_troop_2", "trp_northern_raider"),
          (else_try),
            (eq, ":template", "pt_woku_pirate_lair"),
            (eq, ":random_value", 0),
            (assign, ":bandit_troop", "trp_woku_pirate"),
            (assign, ":bandit_troop_2", "trp_woku_pirate"),
          (else_try),
            (eq, ":template", "pt_kanto_rebel_lair"),
            (eq, ":random_value", 0),
            (assign, ":bandit_troop", "trp_kanto_rebel"),
            (assign, ":bandit_troop_2", "trp_kanto_rebel"),
          (else_try),
            (eq, ":template", "pt_seto_pirate_lair"),
            (eq, ":random_value", 0),
            (assign, ":bandit_troop", "trp_seto_pirate"),
            (assign, ":bandit_troop_2", "trp_seto_pirate"),
		  #gekokujo 3.0 new bandit types start
          (else_try),
            (this_or_next|eq, ":template", "pt_monk_rebel_lair"),
            (neq, ":random_value", 0),
            (assign, ":bandit_troop", "trp_monk_rebel"),
            (assign, ":bandit_troop_2", "trp_monk_rebel"),
		  #gekokujo 3.0 new bandit types end
          (else_try),
            (this_or_next|eq, ":template", "pt_looter_lair"),
            (neq, ":random_value", 0),
            (assign, ":bandit_troop", "trp_generic_ashigaru"),
            (assign, ":bandit_troop_2", "trp_generic_jizamurai"), #gekokujo 3.0 enable enemy samurai in mansion raid
          (try_end),
                                                                       
          (store_current_scene, ":cur_scene"), 
          (modify_visitors_at_site, ":cur_scene"),
          (try_for_range, ":unused", 0, ":number_of_bandits_will_be_spawned_at_each_period"),            
            (store_random_in_range, ":random_entry_point", 2, 11),
		    #gekokujo 3.0 enable enemy samurai in mansion raid start
			#see above trigger for notes
            #(add_visitors_to_current_scene, ":random_entry_point", ":bandit_troop", 1),
			(store_random_in_range, ":random_bandit_type", 0, 6), #roll 1 to 6
			(try_begin),
			  (eq, ":random_bandit_type", 0), #roll of 1 (so 1/6 chance)
			  (add_visitors_to_current_scene, ":random_entry_point", ":bandit_troop_2", 1),
			(else_try),
			  (add_visitors_to_current_scene, ":random_entry_point", ":bandit_troop", 1),
			(try_end),
		    #gekokujo 3.0 enable enemy samurai in mansion raid end
          (try_end),
        (try_end),

        #no need to adjust courage in bandit lair for now
        #(call_script, "script_apply_death_effect_on_courage_scores", ":dead_agent_no", ":killer_agent_no"),
       ]),

      (0, 0, ti_once, [],
       [
         (call_script, "script_music_set_situation_with_culture", mtf_sit_ambushed),
         (set_party_battle_mode),
        ]),

      (2, 0, ti_once, 
       [
         (neg|main_hero_fallen),
         (num_active_teams_le, 1),         
       ],
       [
         (party_get_template_id, ":template", "$g_encountered_party"),
         (try_begin),
           (eq, ":template", "pt_looter_lair"),
           (check_quest_active, "qst_save_relative_of_merchant"),

           (store_faction_of_party, ":starting_town_faction", "$g_starting_town"),
           
           (try_begin),
             (eq, ":starting_town_faction", "fac_kingdom_11"),
             (assign, ":troop_of_merchant", "trp_relative_of_merchant"),
           (else_try),  
             (eq, ":starting_town_faction", "fac_kingdom_10"),
             (assign, ":troop_of_merchant", "trp_relative_of_merchant"),
           (else_try),                   
             (eq, ":starting_town_faction", "fac_kingdom_1"),
             (assign, ":troop_of_merchant", "trp_relative_of_merchant"),
           (else_try),  
             (eq, ":starting_town_faction", "fac_kingdom_13"),
             (assign, ":troop_of_merchant", "trp_relative_of_merchant"),
           (else_try),  
             (eq, ":starting_town_faction", "fac_kingdom_7"),
             (assign, ":troop_of_merchant", "trp_relative_of_merchant"),
           (else_try),  
             (eq, ":starting_town_faction", "fac_kingdom_9"),
             (assign, ":troop_of_merchant", "trp_relative_of_merchant"),
           (try_end),
           
           (get_player_agent_no, ":player_agent"),
           (agent_get_position, pos0, ":player_agent"),
           (assign, ":minimum_distance", 100000),
           (try_for_range, ":entry_no", 1, 10),
             (entry_point_get_position, pos1, ":entry_no"),
             (get_distance_between_positions, ":dist", pos0, pos1),
             (le, ":dist", ":minimum_distance"),
             (ge, ":dist", 1000),
             (assign, ":nearest_entry_point", ":entry_no"),
             (assign, ":minimum_distance", ":dist"),
           (try_end),                     
                          
           (add_visitors_to_current_scene, ":nearest_entry_point", ":troop_of_merchant", 1, 0),                      
         (try_end),
       ]),

       common_battle_order_panel,
       common_battle_order_panel_tick,

       (1, 4, ti_once,
       [
         (assign, ":continue", 0),
       
         (party_get_template_id, ":template", "$g_encountered_party"),
         (try_begin),       
           (eq, ":template", "pt_looter_lair"),
           (check_quest_active, "qst_save_relative_of_merchant"),
           
           (this_or_next|main_hero_fallen),
           (eq, "$relative_of_merchant_is_found", 1),
           
           (assign, ":continue", 1),
         (else_try),
		   #gekokujo 3.0 this looks like a typo (NOT ME) start
           #(this_or_next|neq|eq, ":template", "pt_looter_lair"),
		   (this_or_next|neg|eq, ":template", "pt_looter_lair"),
		   #gekokujo 3.0 this looks like a typo (NOT ME) end
           (neg|check_quest_active, "qst_save_relative_of_merchant"),

           (store_mission_timer_a,":cur_time"),
           (ge, ":cur_time", 5),
           
           (this_or_next|main_hero_fallen),
           (num_active_teams_le, 1),
           
           (assign, ":continue", 1),
         (try_end),  
         
         (eq, ":continue", 1),
       ],
       [
         (try_begin),
           (main_hero_fallen),
         (else_try),
           (party_set_slot, "$g_encountered_party", slot_party_ai_substate, 2),
         (try_end),
         
         (finish_mission),
         ]),
      ]),
        
  (
	"alley_fight", mtf_battle_mode,charge,
    "Alley fight",
    [    
      (0,mtef_team_0|mtef_use_exact_number,af_override_horse,aif_start_alarmed,7,[]),
      (1,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,20,[]),
      (2,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,20,[]),
      (3,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,20,[]),
    ],    
    [
      common_battle_init_banner,
    
      common_inventory_not_available,
      
      (ti_on_agent_spawn, 0, 0, [],
      [              
        (store_trigger_param_1, ":agent_no"),
        (get_player_agent_no, ":player_agent"),
        (neq, ":agent_no", ":player_agent"),
        (assign, "$g_main_attacker_agent", ":agent_no"),
        (agent_ai_set_aggressiveness, ":agent_no", 199),
        
        (try_begin),
          (agent_get_troop_id, ":troop_no", ":agent_no"),
          (is_between, ":troop_no", "trp_tsu_merchant", "trp_startup_merchants_end"),
          (agent_set_team, ":agent_no", 7),          
          (team_set_relation, 0, 7, 0), 
        (try_end),                
      ]),
              
	   (0, 0, 0, 
	   [
	     (eq, "$talked_with_merchant", 0), 
	   ],
	   [
        (get_player_agent_no, ":player_agent"),
        (agent_get_position, pos0, ":player_agent"),

        (try_for_agents, ":agent_no"),
          (agent_get_troop_id, ":troop_no", ":agent_no"),
          (is_between, ":troop_no", "trp_tsu_merchant", "trp_startup_merchants_end"),
          (agent_set_scripted_destination, ":agent_no", pos0),
          (agent_get_position, pos1, ":agent_no"),
          (get_distance_between_positions, ":dist", pos0, pos1),
          (le, ":dist", 200),     
          (assign, "$talk_context", tc_back_alley),     
          (start_mission_conversation, ":troop_no"),
        (try_end),
	   ]),
     
      (1, 0, 0, [], 
      [      
        (get_player_agent_no, ":player_agent"),       
        (ge, "$g_main_attacker_agent", 0),
        (ge, ":player_agent", 0),
        (agent_is_active, "$g_main_attacker_agent"),
        (agent_is_active, ":player_agent"),
        (agent_get_position, pos0, ":player_agent"),
        (agent_get_position, pos1, "$g_main_attacker_agent"),
        (get_distance_between_positions, ":dist", pos0, pos1),
        (ge, ":dist", 5),
        (agent_set_scripted_destination, "$g_main_attacker_agent", pos0),
      ]),

      (ti_tab_pressed, 0, 0, [], 
      [
        (display_message, "str_cannot_leave_now"),
      ]),

      (0, 0, ti_once, [],
       [
         (call_script, "script_music_set_situation_with_culture", mtf_sit_ambushed),
         (set_party_battle_mode),
        ]),

      (0, 0, ti_once, 
       [
         (neg|main_hero_fallen),
         (num_active_teams_le, 1),
       ],
       [
         (store_faction_of_party, ":starting_town_faction", "$g_starting_town"),
           
         (try_begin),
           (eq, ":starting_town_faction", "fac_kingdom_1"),
           (assign, ":troop_of_merchant", "trp_niigata_merchant"),
         (else_try),  
           (eq, ":starting_town_faction", "fac_kingdom_11"),
           (assign, ":troop_of_merchant", "trp_tsu_merchant"),
         (else_try),                   
           (eq, ":starting_town_faction", "fac_kingdom_7"),
           (assign, ":troop_of_merchant", "trp_sakai_merchant"),
         (else_try),  
           (eq, ":starting_town_faction", "fac_kingdom_9"),
           (assign, ":troop_of_merchant", "trp_hakata_merchant"),
         (else_try),  
           (eq, ":starting_town_faction", "fac_kingdom_13"),
           (assign, ":troop_of_merchant", "trp_edo_merchant"),
         (else_try),  
           (eq, ":starting_town_faction", "fac_kingdom_10"),
           (assign, ":troop_of_merchant", "trp_hirosaki_merchant"),
         (try_end),
                                     
         (add_visitors_to_current_scene, 3, ":troop_of_merchant", 1, 0),                      
       ]),
       
      (1, 0, ti_once,
       [        
         (eq, "$talked_with_merchant", 1),         
       ],
       [         
         (try_begin),
           (main_hero_fallen),
           (assign, "$g_killed_first_bandit", 0),
         (else_try),  
           (assign, "$g_killed_first_bandit", 1),
         (try_end),

         (finish_mission),
         (assign, "$g_main_attacker_agent", 0),
         (assign, "$talked_with_merchant", 1),  
         
         (assign, "$current_startup_quest_phase", 1),                  
                  
         (change_screen_return),
         (set_trigger_result, 1),
         
         (get_player_agent_no, ":player_agent"),
         (store_agent_hit_points, ":hit_points", ":player_agent"),
         
         (try_begin),
           (lt, ":hit_points", 90),
           (agent_set_hit_points, ":player_agent", 90),
         (try_end),  
       ]),

      (1, 3, ti_once,
       [        
         (main_hero_fallen),         
       ],
       [         
         (try_begin),
           (main_hero_fallen),
           (assign, "$g_killed_first_bandit", 0),
         (else_try),  
           (assign, "$g_killed_first_bandit", 1),
         (try_end),

         (finish_mission),
         (assign, "$g_main_attacker_agent", 0),
         (assign, "$talked_with_merchant", 1),  
         
         (assign, "$current_startup_quest_phase", 1),                  
                  
         (change_screen_return),
         (set_trigger_result, 1),    
         
         (get_player_agent_no, ":player_agent"),
         (store_agent_hit_points, ":hit_points", ":player_agent"),
         
         (try_begin),
           (lt, ":hit_points", 90),
           (agent_set_hit_points, ":player_agent", 90),
         (try_end),                
       ]),
     ]),
     
  (
    "meeting_merchant",0,-1,
    "Meeting with the merchant",
    [
      (0,mtef_team_0,af_override_horse,0,1,[]),
      (1,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
      (2,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
      (3,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
      (4,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
      (5,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
      (6,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
      (7,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
      (8,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
      (9,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
    ],
    [
      (ti_on_agent_spawn, 0, 0, [],
      [              
        (store_trigger_param_1, ":agent_no"),

        (try_begin),
          (agent_get_troop_id, ":troop_no", ":agent_no"),
          (is_between, ":troop_no", "trp_tsu_merchant", "trp_startup_merchants_end"),
          (agent_set_team, ":agent_no", 7),          
          (team_set_relation, 0, 7, 0), 
        (try_end),                
      ]),

      (1, 0, ti_once, [], 
      [
        (assign, "$dialog_with_merchant_ended", 0),
        (store_current_scene, ":cur_scene"),
        (scene_set_slot, ":cur_scene", slot_scene_visited, 1),
        (try_begin),
          (eq, "$sneaked_into_town", 1),
          (call_script, "script_music_set_situation_with_culture", mtf_sit_town_infiltrate),
        (else_try),
          (eq, "$talk_context", tc_tavern_talk),
          (call_script, "script_music_set_situation_with_culture", mtf_sit_tavern),
        (else_try),
          (call_script, "script_music_set_situation_with_culture", mtf_sit_town),
        (try_end),
      ]),
      
      (1, 0, 0, 
      [        
        (assign, ":continue", 0),
        (try_begin),
          (ge, "$dialog_with_merchant_ended", 6),
          (assign, ":continue", 1),
        (else_try),
          (ge, "$dialog_with_merchant_ended", 1),
		  (neg|conversation_screen_is_active),          

          (try_begin),
            (eq, "$dialog_with_merchant_ended", 1),
            (check_quest_active, "qst_collect_men"),
            (tutorial_box, "str_start_up_first_quest", "@Tutorial"),
          (try_end),  

          (val_add, "$dialog_with_merchant_ended", 1),
          (assign, ":continue", 0),
        (try_end),  
        
        (try_begin),
          (conversation_screen_is_active), 
          (tutorial_message, -1),
          (assign, ":continue", 0),
        (try_end),
        
        (eq, ":continue", 1),                        
      ],
      [
        (tutorial_message_set_size, 17, 17),
        (tutorial_message_set_position, 500, 650),
        (tutorial_message_set_center_justify, 0),
        (tutorial_message_set_background, 1),
        (tutorial_message, "str_press_tab_to_exit_from_town"),
      ]),
      	  	
      (ti_before_mission_start, 0, 0, [], 
      [      
        #(call_script, "script_change_banners_and_chest"),
	  ]),

      (ti_inventory_key_pressed, 0, 0, 
      [
        (set_trigger_result, 1),        
      ], []),           
            
      (ti_tab_pressed, 0, 0, 
      [ 
        (try_begin),          
          (gt, "$dialog_with_merchant_ended", 0),          

          (assign, ":max_dist", 0),
          (party_get_position, pos1, "$current_town"),
          (try_for_range, ":unused", 0, 10),
            (map_get_random_position_around_position, pos0, pos1, 2),
            (get_distance_between_positions, ":dist", pos0, pos1),
            (ge, ":dist", ":max_dist"),
            (assign, ":max_dist", ":dist"),
            (copy_position, pos2, pos0),
          (try_end),  
    
          (party_set_position, "p_main_party", pos2),          
                            
          (finish_mission),
          
          (assign, "$current_startup_quest_phase", 2),
          
          (tutorial_message, -1),
          
          (tutorial_message_set_background, 0),
          
          (change_screen_map),
          
          (try_begin),
            (check_quest_finished, "qst_save_town_from_bandits"),
            (assign, "$g_do_one_more_meeting_with_merchant", 1),
          (else_try),  
            #will do this at first spawning in the map          
            (set_spawn_radius, 50),
            (try_for_range, ":unused", 0, 20),
              (spawn_around_party, "p_main_party", "pt_looters"),
            (try_end),          
          (try_end),  

          (set_trigger_result, 1),
        (else_try),
          (display_message, "str_cannot_leave_now"),
        (try_end),
      ], []),
    ]),
  (
    "town_fight",0,-1,
    "Town Fight",
    [
      (0,mtef_scene_source|mtef_team_0,af_override_horse,0,1,[]),
      (1,mtef_scene_source|mtef_team_0,af_override_horse,0,1,[]),
      (2,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
      (3,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
      (4,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
      (5,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
      (6,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
      (7,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),          
      (8,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
      (9,mtef_visitor_source,af_override_horse,0,1,[]),
      (10,mtef_visitor_source,af_override_horse,0,1,[]),
      (11,mtef_visitor_source|mtef_team_1,af_override_horse,0,1,[]),
      (12,mtef_visitor_source|mtef_team_1,af_override_horse,0,1,[]),
      (13,mtef_visitor_source|mtef_team_1,af_override_horse,0,1,[]),
      (14,mtef_visitor_source,af_override_horse,0,1,[]),
      (15,mtef_visitor_source,af_override_horse,0,1,[]),
      (16,mtef_visitor_source,af_override_horse,0,1,[]),
      (17,mtef_visitor_source,af_override_horse,0,1,[]),
      (18,mtef_visitor_source,af_override_horse,0,1,[]),
      (19,mtef_visitor_source,af_override_horse,0,1,[]),
      (20,mtef_visitor_source,af_override_horse,0,1,[]),
      (21,mtef_visitor_source|mtef_team_1,af_override_horse,0,1,[]),
      (22,mtef_visitor_source|mtef_team_1,af_override_horse,0,1,[]),
	  (23,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]), #guard
      (24,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]), #guard
	  (25,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]), #guard
	  (26,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]), #guard
	  (27,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]), #guard
	  (28,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]), #guard
	  (29,mtef_visitor_source,af_override_horse,0,1,[]),
	  (30,mtef_visitor_source,af_override_horse,0,1,[]), 
	  (31,mtef_visitor_source,af_override_horse,0,1,[]), 
      (32,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]), #town walker point
	  (33,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]), #town walker point
	  (34,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]), #town walker point
	  (35,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]), #town walker point
	  (36,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]), #town walker point
	  (37,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]), #town walker point
	  (38,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]), #town walker point
	  (39,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]), #town walker point
      (40,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]), #in towns, can be used for guard reinforcements
	  (41,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]), #in towns, can be used for guard reinforcements
	  (42,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]), #in towns, can be used for guard reinforcements
	  (43,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]), #in towns, can be used for guard reinforcements
      (44,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
	  (45,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
	  (46,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
	  (47,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
    ],
    [
      common_battle_init_banner,
    
      (ti_on_agent_spawn, 0, 0, [],
      [
        (store_trigger_param_1, ":agent_no"),
        
        (agent_set_team, ":agent_no", 0),
      ]),

      (ti_before_mission_start, 0, 0, [],
      [
        (mission_disable_talk),        
      
        (assign, "$g_main_attacker_agent", 0),
        (set_party_battle_mode),
        
        (assign, "$number_of_bandits_killed_by_player", 0),
        (assign, "$number_of_civilian_loses", 0),
        
        (set_fixed_point_multiplier, 100),
	  ]),
		 
      (1, 0, ti_once, 
      [
        (call_script, "script_init_town_walker_agents"),
      ], 
      []),
      
      (ti_on_agent_killed_or_wounded, 0, 0, [],
      [
        (store_trigger_param_1, ":dead_agent_no"),
        (store_trigger_param_2, ":killer_agent_no"),
        #(store_trigger_param_3, ":is_wounded"),
        
        (try_begin),
          (agent_get_team, ":dead_agent_team_no", ":dead_agent_no"),
          (eq, ":dead_agent_team_no", 1),

          (get_player_agent_no, ":player_agent"),
          (eq, ":player_agent", ":killer_agent_no"),
                
          (val_add, "$number_of_bandits_killed_by_player", 1),
        (else_try),
          (eq, ":dead_agent_team_no", 0),
          
          (val_add, "$number_of_civilian_loses", 1),
        (try_end),  
      ]),
            
      (1, 0, 0, 
      [
        (lt, "$merchant_sign_count", 8),
  	    (val_add, "$merchant_sign_count", 1),
  	    
  	    (try_begin),
  	      (eq, "$merchant_sign_count", 2),
          (get_player_agent_no, ":player_agent"),
  	      (try_for_agents, ":agent_no"),
  	        (agent_get_troop_id, ":agent_troop_id", ":agent_no"),
  	        (ge, ":agent_troop_id", "trp_tsu_merchant"),
  	        (lt, ":agent_troop_id", "trp_startup_merchants_end"),
  	        
  	        (assign, "$g_city_merchant_troop_id", ":agent_troop_id"),
  	        (assign, "$g_city_merchant_agent_id", ":agent_no"),
  	        
  	        (agent_get_position, pos0, ":player_agent"),
  	        (agent_get_position, pos1, ":agent_no"),
  	                    
  	        (assign, ":max_dif", -1000),
            (try_for_range, ":target_entry_point", 0, 64),
              #(neg|entry_point_is_auto_generated, ":target_entry_point"),
              (entry_point_get_position, pos6, ":target_entry_point"),
              (get_distance_between_positions, ":dist_to_player", pos0, pos6),
              (get_distance_between_positions, ":dist_to_merchant", pos1, pos6),
              (store_sub, ":dif", ":dist_to_merchant", ":dist_to_player"),
              (ge, ":dist_to_merchant", 15),
              (ge, ":dif", ":max_dif"),
              (copy_position, pos2, pos6),
              (assign, ":max_dif", ":dif"),
            (try_end),
  	      	    
    	    (agent_set_scripted_destination, ":agent_no", pos2, 0),
            (agent_set_speed_limit, ":agent_no", 10),
          (try_end),
        (else_try),
  	      (eq, "$merchant_sign_count", 5),
  	                 
          (get_player_agent_no, ":player_agent"),
	      (agent_get_position, pos0, ":player_agent"),

  	      (agent_set_scripted_destination, "$g_city_merchant_agent_id", pos0, 0),
          (agent_set_speed_limit, "$g_city_merchant_agent_id", 10),
        (else_try),
  	      (eq, "$merchant_sign_count", 7),
  	      
  	      (agent_clear_scripted_mode, "$g_city_merchant_agent_id"),
  	                 
  	      (assign, "$talk_context", tc_town_talk),
  	      (start_mission_conversation, "$g_city_merchant_troop_id"),  	        	      
  	    (try_end),  	      
  	  ], 
	  []),
	  
	  (1, 0, 0, [],
	  [	  
	    (ge, "$merchant_sign_count", 8),
	   
	    (get_player_agent_no, ":player_agent"),
	    	    
        (try_for_agents, ":agent_no"),
          (neq, ":agent_no", ":player_agent"),
          (agent_is_alive, ":agent_no"),
          (agent_get_team, ":agent_team", ":agent_no"),
          (eq, ":agent_team", 0),
          
          (agent_get_position, pos0, ":agent_no"),
        
          (assign, ":minimum_distance", 10000),  
          (try_for_agents, ":bandit_no"),
            (agent_is_alive, ":bandit_no"),
            (agent_get_team, ":bandit_team", ":bandit_no"),
            (eq, ":bandit_team", 1),
            
            (agent_get_position, pos1, ":bandit_no"),
  
            (get_distance_between_positions, ":dist", pos0, pos1),
            (le, ":dist", ":minimum_distance"),
            (assign, ":minimum_distance", ":dist"),
            (copy_position, pos2, pos1),
          (try_end),
         
          (assign, reg1, ":dist"),
          (try_begin),
            (le, ":minimum_distance", 500),
            (agent_clear_scripted_mode, ":agent_no"),
          (else_try),  
            (lt, ":minimum_distance", 10000),
            (agent_set_scripted_destination, ":agent_no", pos2, 0),
          (try_end),
        (try_end),                  	      
      ]),

      (3, 0, 0, 
      [
        (lt, "$merchant_sign_count", 8),
  	    (call_script, "script_tick_town_walkers")
  	  ], 
	  []),	  	  
	
      (2, 0, 0, 
      [
        (call_script, "script_center_ambiance_sounds")
      ], 
      []),
    
      (ti_before_mission_start, 0, 0, 
      [], 
      [
        (call_script, "script_change_banners_and_chest")
      ]),
        
      (1, 4, ti_once,
       [                  
         (this_or_next|main_hero_fallen),
         (num_active_teams_le, 1),
         
         (ge, "$merchant_sign_count", 8),
       ],
       [         
         (try_begin),
           (main_hero_fallen),
           (assign, "$g_killed_first_bandit", 0),
         (else_try),  
           (assign, "$g_killed_first_bandit", 1),
         (try_end),
         
         (assign, "$current_startup_quest_phase", 4),

         (mission_enable_talk),        

         (finish_mission),         
         
         (unlock_achievement, ACHIEVEMENT_GET_UP_STAND_UP),        
                  
         (change_screen_return),
         (set_trigger_result, 1),         
       ]),

      (ti_inventory_key_pressed, 0, 0,
      [
        (try_begin),
          (eq, "$g_mt_mode", tcm_default),
          (set_trigger_result,1),
        (else_try),
          (eq, "$g_mt_mode", tcm_disguised),
          (display_message,"str_cant_use_inventory_disguised"),
        (else_try),
          (display_message, "str_cant_use_inventory_now"),
        (try_end),
      ], []),
       
      (ti_tab_pressed, 0, 0,
      [
        (display_message, "str_cannot_leave_now"),
      ], []),
  ]),
]
