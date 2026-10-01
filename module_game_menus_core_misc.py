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

game_menus_core_misc = [
  (
    "custom_battle_scene",menu_text_color(0xFF000000)|mnf_disable_all_keys,
    "(NO_TRANS)",
	
    "none",
    [],
    [

      ("quick_battle_scene_1",[],"{!}quick_battle_scene_1",
       [
           (set_jump_mission,"mt_ai_training"),
           (jump_to_scene,"scn_quick_battle_scene_1"),(change_screen_mission)        
		]
       ),
      ("quick_battle_scene_2",[],"{!}quick_battle_scene_2",
       [
           (set_jump_mission,"mt_ai_training"),
           (jump_to_scene,"scn_quick_battle_scene_2"),(change_screen_mission)        
		]
       ),
      ("quick_battle_scene_3",[],"{!}quick_battle_scene_3",
       [
           (set_jump_mission,"mt_ai_training"),
           (jump_to_scene,"scn_quick_battle_scene_3"),(change_screen_mission)        
		]
       ),
      ("quick_battle_scene_4",[],"{!}quick_battle_scene_4",
       [
           (set_jump_mission,"mt_ai_training"),
           (jump_to_scene,"scn_quick_battle_scene_4"),(change_screen_mission)        
		]
       ),
      ("quick_battle_scene_5",[],"{!}quick_battle_scene_5",
       [
           (set_jump_mission,"mt_ai_training"),
           (jump_to_scene,"scn_quick_battle_scene_5"),(change_screen_mission)        
		]
       ),
	   
      ("go_back",[],"{!}Go back",
       [(change_screen_quit),
        ]
       ),
      ]
  ),
  
  #deprecated
##  (
##    "custom_battle_2",mnf_disable_all_keys,
##    "{s16}",
##    "none",
##    [
##     (assign, "$g_battle_result", 0),
##     (set_show_messages, 0),
##
##     (troop_clear_inventory, "trp_player"),
##     (troop_raise_attribute, "trp_player", ca_strength, -1000),
##     (troop_raise_attribute, "trp_player", ca_agility, -1000),
##     (troop_raise_attribute, "trp_player", ca_charisma, -1000),
##     (troop_raise_attribute, "trp_player", ca_intelligence, -1000),
##     (troop_raise_skill, "trp_player", skl_shield, -1000),
##     (troop_raise_skill, "trp_player", skl_athletics, -1000),
##     (troop_raise_skill, "trp_player", skl_riding, -1000),
##     (troop_raise_skill, "trp_player", skl_power_strike, -1000),
##     (troop_raise_skill, "trp_player", skl_power_throw, -1000),
##     (troop_raise_skill, "trp_player", skl_weapon_master, -1000),
##     (troop_raise_skill, "trp_player", skl_horse_archery, -1000),
##     (troop_raise_skill, "trp_player", skl_ironflesh, -1000),
##     (troop_raise_proficiency_linear, "trp_player", wpt_one_handed_weapon, -10000),
##     (troop_raise_proficiency_linear, "trp_player", wpt_two_handed_weapon, -10000),
##     (troop_raise_proficiency_linear, "trp_player", wpt_polearm, -10000),
##     (troop_raise_proficiency_linear, "trp_player", wpt_archery, -10000),
##     (troop_raise_proficiency_linear, "trp_player", wpt_crossbow, -10000),
##     (troop_raise_proficiency_linear, "trp_player", wpt_throwing, -10000),
##
##     (reset_visitors),
####   Scene 1 Start "Shalow Lake War"
##     (try_begin),
##       (eq, "$g_custom_battle_scenario", 0),
##       (assign, "$g_player_troop", "trp_knight_1_15"),
##       (set_player_troop, "$g_player_troop"),
##     
##       (assign, "$g_custom_battle_scene", "scn_quick_battle_1"),
##       (modify_visitors_at_site, "$g_custom_battle_scene"),
##       (set_visitor, 0, "$g_player_troop"),
##
###       (troop_add_item, "trp_player","itm_bascinet",0),
###       (troop_add_item, "trp_player","itm_mail_with_surcoat",0),
###       (troop_add_item, "trp_player","itm_bastard_sword_a",0),
###       (troop_add_item, "trp_player","itm_war_bow",0),
###       (troop_add_item, "trp_player","itm_khergit_arrows",0),
###       (troop_add_item, "trp_player","itm_kite_shield",0),
###       (troop_add_item, "trp_player","itm_hunter",0),
###       (troop_add_item, "trp_player","itm_mail_chausses",0),
###       (troop_equip_items, "trp_player"),
##     
##       (set_visitors, 1, "trp_farmer", 13),
##       (set_visitors, 2, "trp_swadian_sergeant", 5),
##       (set_visitors, 3, "trp_swadian_sharpshooter", 4),
##       (set_visitors, 4, "trp_swadian_man_at_arms", 8),
##       (set_visitors, 5, "trp_swadian_knight", 3),
##       (set_visitors, 6, "trp_peasant_woman", 7),
##     
####     Enemy
##       (set_visitors, 16, "trp_vaegir_infantry", 6),
##       (set_visitors, 17, "trp_vaegir_archer", 6),
##       (set_visitors, 18, "trp_vaegir_horseman", 4),
##       (set_visitors, 19, "trp_vaegir_knight", 10),
##       (set_visitors, 20, "trp_vaegir_guard", 6),
##       (str_store_string, s16, "str_custom_battle_1"),
##
####   SCENE 3 Start "Mountain Bandit Hunt"
##     (else_try),
##       (eq, "$g_custom_battle_scenario", 1),
##       (assign, "$g_player_troop", "trp_knight_2_5"),
##       (set_player_troop, "$g_player_troop"),
##     
##       (assign, "$g_custom_battle_scene", "scn_quick_battle_3"),
##       (modify_visitors_at_site, "$g_custom_battle_scene"),
##       (set_visitor, 0, "$g_player_troop"),
##     
##       (set_visitors, 1, "trp_vaegir_archer", 4),
##       (set_visitors, 2, "trp_vaegir_archer", 5),
##       (set_visitors, 3, "trp_vaegir_veteran", 4),
##       (set_visitors, 4, "trp_vaegir_horseman", 4),
##       (set_visitors, 5, "trp_vaegir_footman", 2),
##       (set_visitors, 6, "trp_vaegir_knight", 4),
#### ENEMY
##     
##       (set_visitors, 16, "trp_woku_pirate", 4),
##       (set_visitors, 17, "trp_bandit", 8),
##       (set_visitors, 18, "trp_woku_pirate", 8),
##       (set_visitors, 19, "trp_woku_pirate", 6),
##       (set_visitors, 20, "trp_kinai_rebel", 5),
##       (set_visitors, 21, "trp_woku_pirate", 4),
##       (set_visitors, 22, "trp_brigand", 6),
##       (set_visitors, 23, "trp_kinai_rebel", 8),
##       (set_visitors, 25, "trp_brigand", 10),
##       (str_store_string, s16, "str_custom_battle_2"),
##
####   SCENE 4 Start "Grand Stand"
##     (else_try),
##       (eq, "$g_custom_battle_scenario", 2),
##       (assign, "$g_player_troop", "trp_kingdom_5_lady_1"),
##       (set_player_troop, "$g_player_troop"),
##     
##       (troop_raise_attribute, "$g_player_troop", ca_strength, 12),
##       (troop_raise_attribute, "$g_player_troop", ca_agility, 9),
##       (troop_raise_attribute, "$g_player_troop", ca_charisma, 5),
##       (troop_raise_attribute, "$g_player_troop", ca_intelligence, 5),
##       (troop_raise_skill, "$g_player_troop", skl_shield, 3),
##       (troop_raise_skill, "$g_player_troop", skl_athletics, 2),
##       (troop_raise_skill, "$g_player_troop", skl_riding, 3),
##       (troop_raise_skill, "$g_player_troop", skl_power_strike, 4),
##       (troop_raise_skill, "$g_player_troop", skl_power_draw, 5),
##       (troop_raise_skill, "$g_player_troop", skl_weapon_master, 4),    
##       (troop_raise_skill, "$g_player_troop", skl_ironflesh, 6),
##       (troop_raise_proficiency_linear, "$g_player_troop", wpt_one_handed_weapon, 100),
##       (troop_raise_proficiency_linear, "$g_player_troop", wpt_two_handed_weapon, 30),
##       (troop_raise_proficiency_linear, "$g_player_troop", wpt_polearm, 20),
##       (troop_raise_proficiency_linear, "$g_player_troop", wpt_crossbow, 110),
##       (troop_raise_proficiency_linear, "$g_player_troop", wpt_throwing, 10),
##     
##       (assign, "$g_custom_battle_scene", "scn_quick_battle_4"),
##       (modify_visitors_at_site, "$g_custom_battle_scene"),
##       (set_visitor, 0, "$g_player_troop"),
##     
##       (troop_clear_inventory, "$g_player_troop"),
##       (troop_add_item, "$g_player_troop","itm_helmet_with_neckguard",0),
##       (troop_add_item, "$g_player_troop","itm_plate_armor",0),
##       (troop_add_item, "$g_player_troop","itm_iron_greaves",0),
##       (troop_add_item, "$g_player_troop","itm_mail_chausses",0),
##       (troop_add_item, "$g_player_troop","itm_tab_shield_small_round_c",0),
##       (troop_add_item, "$g_player_troop","itm_heavy_crossbow",0),
##       (troop_add_item, "$g_player_troop","itm_bolts",0),
##       (troop_add_item, "$g_player_troop","itm_sword_medieval_b_small",0),
##       (troop_equip_items, "$g_player_troop"),
#### US     
##       (set_visitors, 1, "trp_vaegir_infantry", 4),
##       (set_visitors, 2, "trp_vaegir_archer", 3),
##       (set_visitors, 3, "trp_vaegir_infantry", 4),
##       (set_visitors, 4, "trp_vaegir_archer", 3),
##       (set_visitors, 5, "trp_vaegir_infantry", 3),
##       (set_visitors, 6, "trp_vaegir_footman", 5),
##       (set_visitors, 7, "trp_vaegir_footman", 4),
##       (set_visitors, 8, "trp_vaegir_archer", 3),
##
#### ENEMY
##       (set_visitors, 16, "trp_swadian_footman", 8),
##       (set_visitors, 17, "trp_swadian_crossbowman", 9),
##       (set_visitors, 18, "trp_swadian_sergeant", 7),
##       (set_visitors, 19, "trp_swadian_sharpshooter", 8),
##       (set_visitors, 20, "trp_swadian_militia", 13),
##       (str_store_string, s16, "str_custom_battle_3"),
##     
####   Scene 5 START
##     (else_try),
##       (eq, "$g_custom_battle_scenario", 3),
##       (assign, "$g_player_troop", "trp_knight_1_10"),
##       (set_player_troop, "$g_player_troop"),
##
##       (assign, "$g_custom_battle_scene", "scn_quick_battle_5"),
##       (modify_visitors_at_site, "$g_custom_battle_scene"),
##       (set_visitor, 0, "$g_player_troop"),
##     
#### US     
##       (set_visitors, 1, "trp_swadian_knight", 3),
##       (set_visitors, 2, "trp_swadian_sergeant", 4),
##       (set_visitors, 3, "trp_swadian_sharpshooter", 8),
##       (set_visitors, 4, "trp_swadian_man_at_arms", 8),
##       (set_visitors, 5, "trp_swadian_knight", 2),
##     
####     enemy
##       (set_visitors, 16, "trp_vaegir_infantry", 8),
##       (set_visitors, 17, "trp_vaegir_archer", 10),
##       (set_visitors, 18, "trp_vaegir_horseman", 4),
##       (set_visitors, 19, "trp_vaegir_knight", 10),
##       (set_visitors, 20, "trp_vaegir_guard", 7),
##       (str_store_string, s16, "str_custom_battle_4"),
##     
##     (else_try),
##       (eq, "$g_custom_battle_scenario", 4),
##
####       (assign, "$g_custom_battle_scene", "scn_quick_battle_6"),
##       (assign, "$g_custom_battle_scene", "scn_quick_battle_7"),
##     
###   Player Wear
##       (assign, "$g_player_troop", "trp_knight_4_9"),
##       (set_player_troop, "$g_player_troop"),
##     
##       (modify_visitors_at_site, "$g_custom_battle_scene"),
##       (set_visitor, 0, "$g_player_troop"),
##
##       (set_visitors, 1, "trp_nord_archer", 4),
##       (set_visitors, 2, "trp_nord_archer", 4),
##       (set_visitors, 3, "trp_nord_champion", 4),
##       (set_visitors, 4, "trp_nord_veteran", 5),
##       (set_visitors, 5, "trp_nord_warrior", 5),
##       (set_visitors, 6, "trp_nord_trained_footman", 8),
##
#### ENEMY
##       (set_visitors, 11, "trp_vaegir_knight", 2),
##       (set_visitors, 12, "trp_vaegir_guard", 6),
##       (set_visitors, 13, "trp_vaegir_infantry", 8),
##       (set_visitors, 14, "trp_vaegir_veteran", 10),
##       (set_visitors, 16, "trp_vaegir_skirmisher", 5),
##       (set_visitors, 17, "trp_vaegir_archer", 4),
##       (set_visitors, 18, "trp_vaegir_marksman", 2),
##       (set_visitors, 19, "trp_vaegir_skirmisher", 4),
##       (set_visitors, 20, "trp_vaegir_skirmisher", 3),
##       (set_visitors, 21, "trp_vaegir_skirmisher", 3),
##       (set_visitors, 22, "trp_vaegir_skirmisher", 3),
##       (set_visitors, 23, "trp_vaegir_archer", 2),
##       (str_store_string, s16, "str_custom_battle_5"),
##     (try_end),
##     (set_show_messages, 1),
##     ],
##    
##    [
##      ("custom_battle_go",[],"Start.",
##       [(try_begin),
##          (eq, "$g_custom_battle_scenario", 2),
####          (set_jump_mission,"mt_custom_battle_siege"),
##        (else_try),
##          (eq, "$g_custom_battle_scenario", 4),
####          (set_jump_mission,"mt_custom_battle_5"),
##        (else_try),
####          (set_jump_mission,"mt_custom_battle"),
##        (try_end),
##        (jump_to_menu, "mnu_custom_battle_end"),
##        (jump_to_scene,"$g_custom_battle_scene"),
##        (change_screen_mission),
##        ]
##       ),
##      ("leave_custom_battle_2",[],"Cancel.",
##       [(jump_to_menu, "mnu_start_game_3"),
##        ]
##       ),
##    ]
##  ),


  (
    "custom_battle_end",mnf_disable_all_keys,
    "The battle is over. {s1} Your side killed {reg5} enemies and lost {reg6} troops over the battle. You personally slew {reg7} men in the fighting.",
    "none",
    [(music_set_situation, 0),
     (assign, reg5, "$g_custom_battle_team2_death_count"),
     (assign, reg6, "$g_custom_battle_team1_death_count"),
     (get_player_agent_kill_count, ":kill_count"),
     (get_player_agent_kill_count, ":wound_count", 1),
     (store_add, reg7, ":kill_count", ":wound_count"),
     (try_begin),
       (eq, "$g_battle_result", 1),
       (str_store_string, s1, "str_battle_won"),
     (else_try),
       (str_store_string, s1, "str_battle_lost"),
     (try_end),
     
     (try_begin),
       (ge, "$g_custom_battle_team2_death_count", 100),
       (unlock_achievement, ACHIEVEMENT_LOOK_AT_THE_BONES),
     (try_end),
     ],
    [
      ("continue",[],"Continue.",
       [(change_screen_quit),
        ]
       ),
    ]
  ),
  (
    "auto_return",0,
    "{!}This menu automatically returns to caller.",
    "none",
    [(change_screen_return, 0)],
    [
    ]
  ),
  ("camp",mnf_scale_picture,
   "You set up camp. What do you want to do?",
   "none",
   [
     (assign, "$g_player_icon_state", pis_normal),
     (set_background_mesh, "mesh_pic_camp"),
     #(set_background_mesh, "mesh_gekokujo_pic_camp"), #gekokujo 3.1 change camp picture
    ],
    [
      ("camp_action_1",[(eq,"$cheat_mode",1)],"{!}Cheat: Walk around.",
       [(set_jump_mission,"mt_ai_training"),
        (call_script, "script_setup_random_scene"),
        (change_screen_mission),
        ]
       ),
	   
	  #gekokujo 3.0 cheat menu consolidation start
      ("camp_gekokujo",[], "Gekokujo options...",
       [
         (jump_to_menu, "mnu_camp_gekokujo"),
	   ]
       ),	   
	  #gekokujo 3.0 cheat menu consolidation end
	  
       ##diplomacy begin
###################################################################################
# Autoloot: Allow item management from camp
###################################################################################
##nested diplomacy start+
#Made some changes to autoloot conditions
	("dplmc_camp_manage_inventory",
		[
	  #OLD:
	  #(eq, "$g_autoloot", 1),
      #(store_skill_level, ":inv_skill", "skl_inventory_management", "trp_player"),
      #(gt, "$g_player_chamberlain", 0),
      #(ge, ":inv_skill", 3),
	  #NEW:
	  #1. Must have companions
	  #2. Either a hero in the party must have inventory management 3 or higher, or the player must have inventory management of 2 or higher, or the player or a hero in the party must have a looting skill of 2 or higher
	  (call_script, "script_cf_dplmc_player_party_meets_autoloot_conditions"),
	    ],
	  #"Manage your party's inventory.",
	  "Auto-loot settings...",
		[
			(try_begin),
				#dplmc+ Add check if autoloot has not been initialized yet
				(call_script, "script_dplmc_initialize_autoloot", 0),#argument "0" means this does nothing if deemed unnecessary
			(try_end),
			(troop_clear_inventory, "trp_temp_troop"),
			##diplomacy start+
			(assign, "$pool_troop", "trp_temp_troop"),
			(assign, "$dplmc_return_menu", "mnu_camp"),
			##diplomacy end+
			(assign, "$inventory_menu_offset", 0),
			(jump_to_menu, "mnu_dplmc_manage_loot_pool")
		]
	),

#Alternate display: make it clear why autoloot isn't appearing
	("dplmc_camp_manage_inventory_disabled",
		[
	  #Print this when the player has companions but doesn't meet
	  #the minimum skill levels.
		(try_begin),
			(call_script, "script_cf_dplmc_player_party_meets_autoloot_conditions"),
		(try_end),
		(eq, reg0, 0),
		(disable_menu_option),
	    ],
	  "Auto-loot requires Inventory Management or Looting at rank 2.",
		[
		]
	),
##nested diplomacy end+ Finished changes to autoloot conditions
###################################################################################
# End Autoloot
###################################################################################
	("dplmc_camp_preferences",
		[
		],
		"Diplomacy options...",
		[
			(jump_to_menu, "mnu_dplmc_preferences")
		]
	),

##diplomacy end
      ("camp_action",[],"Take an action.",
       [(jump_to_menu, "mnu_camp_action"),
        ]
       ),
      ("camp_wait_here",[],"Wait here for some time.",
       [
           (assign,"$g_camp_mode", 1),
           (assign, "$g_infinite_camping", 0),
           (assign, "$g_player_icon_state", pis_camping),
           
           (try_begin),
             (party_is_active, "p_main_party"),
             (party_get_current_terrain, ":cur_terrain", "p_main_party"),
             (try_begin),
               (eq, ":cur_terrain", rt_desert),
               (unlock_achievement, ACHIEVEMENT_SARRANIDIAN_NIGHTS),
             (try_end),  
           (try_end),  

           (rest_for_hours_interactive, 24 * 365, 5, 1), #rest while attackable
                      
           (change_screen_return),
        ]
       ),
	   
      ("camp_cheat",
       [(ge, "$cheat_mode", 1)
        ], "CHEAT MENU!",
       [(jump_to_menu, "mnu_camp_cheat"),
        ],
       ),
	  
      ("resume_travelling",[],"Resume travelling.",
       [
           (change_screen_return),
        ]
       ),
      ]
  ),
  ("retirement_verify",0,
   "You are at day {reg0}. Your current luck is {reg1}. Are you sure you want to retire?",
   "none",
   [
     (store_current_day, reg0),
     (assign, reg1, "$g_player_luck"),
     ],
    [
      ("retire_yes",[],"Yes.",
       [
         (start_presentation, "prsnt_retirement"),
        ]
       ),
      ("retire_no",[],"No.",
       [
         (jump_to_menu, "mnu_camp"),
        ]
       ),
      ]
  ),
  ("end_game",0,
   "The decision is made, and you resolve to give up your adventurer's\
 life and settle down. You sell off your weapons and armour, gather up\
 all your money, and ride off into the sunset....",
   "none",
   [],
    [
      ("end_game_bye",[],"Farewell.",
       [
         (change_screen_quit),
        ]
       ),
      ]
  ),
  ("cattle_herd",mnf_scale_picture,
   "You encounter a herd of cattle.",
   "none",
   [(play_sound, "snd_cow_moo"),
    (set_background_mesh, "mesh_pic_cattle"),
   ],
    [
      ("cattle_drive_away",[],"Drive the cattle onward.",
       [
        (party_set_slot, "$g_encountered_party", slot_cattle_driven_by_player, 1),
		#gekokujo cattle herding
		(party_set_ai_behavior, "$g_encountered_party", ai_bhvr_escort_party),
        #(party_set_ai_behavior, "$g_encountered_party", ai_bhvr_driven_by_party),
        (party_set_ai_object,"$g_encountered_party", "p_main_party"),
        (change_screen_return),
        ]
       ),
      ("cattle_stop",[],"Bring the herd to a stop.",
       [
        (party_set_slot, "$g_encountered_party", slot_cattle_driven_by_player, 0),
        (party_set_ai_behavior, "$g_encountered_party", ai_bhvr_hold),
        (change_screen_return),
        ]
       ),
      ("cattle_kill",[(assign, ":continue", 1),
                      (try_begin),
                        (check_quest_active, "qst_move_cattle_herd"),
                        (quest_slot_eq, "qst_move_cattle_herd", slot_quest_target_party, "$g_encountered_party"),
                        (assign, ":continue", 0),
                      (try_end),
                      (eq, ":continue", 1)],"Slaughter some of the animals.",
       [(jump_to_menu, "mnu_cattle_herd_kill"),
        ]
       ),
      ("leave",[],"Leave.",
       [(change_screen_return),
        ]
       ),
      ]
  ),
  ("cattle_herd_kill",0,
   "How many animals do you want to slaughter?",
   "none",
   [(party_get_num_companions, reg5, "$g_encountered_party")],
    [
      ("cattle_kill_1",[(ge, reg5, 1),],"One.",
       [(call_script, "script_kill_cattle_from_herd", "$g_encountered_party", 1),
        (jump_to_menu, "mnu_cattle_herd_kill_end"),
        (change_screen_loot, "trp_temp_troop"),
        (play_sound, "snd_cow_slaughter"),
        ]
       ),
      ("cattle_kill_2",[(ge, reg5, 2),],"Two.",
       [(call_script, "script_kill_cattle_from_herd", "$g_encountered_party", 2),
        (jump_to_menu, "mnu_cattle_herd_kill_end"),
        (change_screen_loot, "trp_temp_troop"),
        (play_sound, "snd_cow_slaughter"),
        ]
       ),
      ("cattle_kill_3",[(ge, reg5, 3),],"Three.",
       [(call_script, "script_kill_cattle_from_herd", "$g_encountered_party", 3),
        (jump_to_menu, "mnu_cattle_herd_kill_end"),
        (change_screen_loot, "trp_temp_troop"),
        (play_sound, "snd_cow_slaughter"),
        ]
       ),
      ("cattle_kill_4",[(ge, reg5, 4),],"Four.",
       [(call_script, "script_kill_cattle_from_herd", "$g_encountered_party", 4),
        (jump_to_menu, "mnu_cattle_herd_kill_end"),
        (change_screen_loot, "trp_temp_troop"),
        (play_sound, "snd_cow_slaughter"),
        ]
       ),
      ("cattle_kill_5",[(ge, reg5, 5),],"Five.",
       [(call_script, "script_kill_cattle_from_herd", "$g_encountered_party", 5),
        (jump_to_menu, "mnu_cattle_herd_kill_end"),
        (change_screen_loot, "trp_temp_troop"),
        (play_sound, "snd_cow_slaughter"),
        ]
       ),
      ("go_back_dot",[],"Go back.",
       [(jump_to_menu, "mnu_cattle_herd"),
        ]
       ),
      ]
  ),
  ("cattle_herd_kill_end",0,
   "{!}You shouldn't be reading this.",
   "none",
   [(change_screen_return)],
    [
      ]
  ),
  #gekokujo 3.1 bogmir's quests end

  (
    "village",mnf_enable_hot_keys,
    "{s10} {s12}^{s11}^{s6}{s7}",
    "none",
    [
        (assign, "$current_town", "$g_encountered_party"),
        (call_script, "script_update_center_recon_notes", "$current_town"),

        (assign, "$g_defending_against_siege", 0), #required for bandit check
        (assign, "$g_battle_result", 0),
        (assign, "$qst_collect_taxes_currently_collecting", 0),
        (assign, "$qst_train_peasants_against_bandits_currently_training", 0),

        (try_begin),
          (gt, "$auto_enter_menu_in_center", 0),
          (jump_to_menu, "$auto_enter_menu_in_center"),
          (assign, "$auto_enter_menu_in_center", 0),
        (try_end),

        (try_begin),
          (neq, "$g_player_raiding_village",  "$current_town"),
          (assign, "$g_player_raiding_village", 0),
        (else_try),
          (jump_to_menu, "mnu_village_loot_continue"),
        (try_end),

        (try_begin),#Fix for collecting taxes
          (eq, "$g_town_visit_after_rest", 1),
          (assign, "$g_town_visit_after_rest", 0),
        (try_end),

        (str_store_party_name,s2, "$current_town"),
        (party_get_slot, ":center_lord", "$current_town", slot_town_lord),
        (store_faction_of_party, ":center_faction", "$current_town"),
        (str_store_faction_name,s9,":center_faction"),
        (try_begin),
          (ge, ":center_lord", 0),
          (str_store_troop_name,s8,":center_lord"),
          (str_store_string,s7,"@{s8} of {s9}"),
        (try_end),

        (str_clear, s10),
        (str_clear, s12),
		
        (try_begin),
          (neg|party_slot_eq, "$current_town", slot_village_state, svs_looted),
          (str_store_string, s60, s2),
		  		  
          (party_get_slot, ":prosperity", "$current_town", slot_town_prosperity),
		  (try_begin),
			(eq, "$cheat_mode", 1),
			(assign, reg4, ":prosperity",),
			(display_message, "@{!}Prosperity: {reg4}"),
		  (try_end),
		  
		  #(val_add, ":prosperity", 5),
          (store_div, ":str_id", ":prosperity", 10),
		  (val_min, ":str_id", 9),
		  (val_add, ":str_id", "str_village_prosperity_0"),
          (str_store_string, s10, ":str_id"),


          (store_div, ":str_id", ":prosperity", 20),
		  (val_min, ":str_id", 4),
		  #gekokujo 3.0 there are no freakin oasis villages in gekokujo start
		  #(try_begin),
		  #  (is_between, "$current_town", "p_village_91", villages_end),
		  #  (val_add, ":str_id", "str_oasis_village_alt_prosperity_0"),
		  #(else_try),
		  #  (val_add, ":str_id", "str_village_alt_prosperity_0"),
		  #(try_end),
		  (val_add, ":str_id", "str_village_alt_prosperity_0"),
		  #gekokujo 3.0 there are no freakin oasis villages in gekokujo end
		  
          (str_store_string, s12, ":str_id"),		  		 		  
        (try_end),

        (str_clear, s11),
        ##diplomacy start+
		(assign, ":save_reg0", reg0),#save variables
		(assign, ":save_reg4", reg4),
		(assign, reg0, 0),
		(assign, reg4, 0),
		(try_begin),#If there's a relation of some kind, write it to s11 (which we'll overwrite below)
			(lt, ":center_lord", 1),
		(else_try),
			#your relative
			(call_script, "script_troop_get_family_relation_to_troop", ":center_lord", "trp_player"),#outputs to s11, reg0, and reg4
			(ge, reg0, 1),#Fall through if this not a relative
		(else_try),
			#your current liege
			(eq, ":center_faction", "$players_kingdom"),
			(is_between, ":center_faction", kingdoms_begin, kingdoms_end),#include fac_player_supporters_faction for claimant quest
			(faction_slot_eq, ":center_faction", slot_faction_leader, ":center_lord"),
			(str_store_string, s11, "@liege"),
			(assign, reg0, 1),
		(else_try),
			#your former liege if you renounced a kingdom
			(eq, ":center_faction", "$players_oath_renounced_against_kingdom"),
			(is_between, ":center_faction", npc_kingdoms_begin, npc_kingdoms_end),
			(faction_slot_eq, ":center_faction", slot_faction_leader, ":center_lord"),
			(str_store_string, s11, "@former liege"),
			(assign, reg0, 1),
		(else_try),
			#stop here for lords you haven't met, or non-hero troops
			(this_or_next|neg|troop_is_hero, ":center_lord"),
			(troop_slot_eq, ":center_lord", slot_troop_met, 0),
		(else_try),
			#check for affiliates
			(call_script, "script_dplmc_is_affiliated_family_member", ":center_lord"),
			(ge, reg0, 1),
			(try_begin),
				(ge, "$g_encountered_party_relation", 0),#don't say "ally" when you might fight them, as that's confusing
				(str_store_string, s11, "str_dplmc_ally"),
			(else_try),
				(str_store_string, s11, "@affiliate"),
			(try_end),
		(else_try),
			#check for former companions
			(call_script, "script_troop_get_player_relation", ":center_lord"),
			#gekokujo 3.0 microfactions! include fort companions start
			#(is_between, ":center_lord", companions_begin, companions_end),
			(is_between, ":center_lord", companions_begin, fort_companions_end),
			#gekokujo 3.0 microfactions! include fort companions end
			(neg|troop_slot_eq, ":center_lord", slot_troop_playerparty_history, dplmc_pp_history_nonplayer_entry),
			(try_begin),
			   (ge, "$g_encountered_party_relation", 0),#don't say "ally" when you might fight them, as that's confusing
			   (ge, reg0, 50),
			   (str_store_string, s11, "str_dplmc_ally"),
			(else_try),
				(ge, "$g_encountered_party_relation", 0),
				(ge, reg0, 20),
				(str_store_string, s11, "str_dplmc_friend"),
			(else_try),
				(str_store_string, s11, "@former companion"),
			(try_end),
			(assign, reg0, 1),
		(else_try),
			#don't print "friend" if you might fight them
			(lt, "$g_encountered_party_relation", 0),
			(assign, reg0, 0),
		(else_try),
			#check for friends
			(val_div, reg0, 50),#right now reg0 holds the relation with the player
			(ge, reg0, 1),
			(str_store_string, s11, "str_dplmc_friend"),
		(else_try),
			#check for marshall
			(eq, ":center_faction", "$players_kingdom"),
			(faction_slot_eq, ":center_faction", slot_faction_marshall, ":center_lord"),
			(str_store_string, s11, "@marshall"),
		(else_try),
			#check for vassal of player if nothing else to say
			(call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", ":center_faction"),
			(val_add, reg0, 1),
			(val_sub, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
			(ge, reg0, 1),
			(str_store_string, s11, "@vassal"),
		(else_try),
			(assign, reg0, 0),
		(try_end),
		##diplomacy end+
        (try_begin),
          (party_slot_eq, "$current_town", slot_village_state, svs_looted),
        (else_try),
          (eq, ":center_lord", "trp_player"),
          (str_store_string,s11,"@ This village and the surrounding lands belong to you."),
		##diplomacy start+ If reg0 > 0, a relation string has been written into s11
		(else_try),
		  (ge, reg0, 1),
		  (str_store_string,s11,"@ You remember that this village and the surrounding lands belong to your {s11} {s7}."),
		##diplomacy end+
        (else_try),
          (ge, ":center_lord", 0),
          (str_store_string,s11,"@ You remember that this village and the surrounding lands belong to {s7}."),
        (else_try),
          (str_store_string,s11,"@ These lands belong to no one."),
        (try_end),
		##diplomacy start+
		(assign, reg0, ":save_reg0"),#revert registers
		(assign, reg4, ":save_reg4"),
		##diplomacy end+

        (str_clear, s7),
        (try_begin),
          (neg|party_slot_eq, "$current_town", slot_village_state, svs_looted),
          (party_get_slot, ":center_relation", "$current_town", slot_center_player_relation),
          (call_script, "script_describe_center_relation_to_s3", ":center_relation"),
          (assign, reg9, ":center_relation"),
          (str_store_string, s7, "@{!} {s3} ({reg9})."),
        (try_end),
        (str_clear, s6),
        (try_begin),
          (party_slot_ge, "$current_town", slot_village_infested_by_bandits, 1),
          (party_get_slot, ":bandit_troop", "$current_town", slot_village_infested_by_bandits),
          (store_character_level, ":player_level", "trp_player"),
          (store_add, "$qst_eliminate_bandits_infesting_village_num_bandits", ":player_level", 10),
          (val_mul, "$qst_eliminate_bandits_infesting_village_num_bandits", 12),
          (val_div, "$qst_eliminate_bandits_infesting_village_num_bandits", 10),
          (store_random_in_range, "$qst_eliminate_bandits_infesting_village_num_villagers", 25, 30),
          (assign, reg8, "$qst_eliminate_bandits_infesting_village_num_bandits"),
          (str_store_troop_name_by_count, s35, ":bandit_troop", "$qst_eliminate_bandits_infesting_village_num_bandits"),
          (str_store_string, s6, "@ The village is infested by {reg8} {s35}."),
          
          (assign, "$g_enemy_party", -1), #new, no known enemy party while saving village from bandits dfdf
          (assign, "$g_ally_party", -1), #new, no known enemy party while saving village from bandits dfdf
          
          (try_begin),
            (eq, ":bandit_troop", "trp_shinano_rebel"),
            (set_background_mesh, "mesh_pic_forest_bandits"),
          (else_try),
            (eq, ":bandit_troop", "trp_seto_pirate"),
            (set_background_mesh, "mesh_pic_steppe_bandits"),
          (else_try),
            (eq, ":bandit_troop", "trp_kanto_rebel"),
            (set_background_mesh, "mesh_pic_steppe_bandits"),
          (else_try),
            (eq, ":bandit_troop", "trp_woku_pirate"),
            (set_background_mesh, "mesh_pic_mountain_bandits"),
          (else_try),
            (eq, ":bandit_troop", "trp_kinai_rebel"),
            (set_background_mesh, "mesh_pic_sea_raiders"),
          (else_try),
           ##diplomacy begin
            (eq, ":bandit_troop", "trp_peasant_woman"),
            (str_store_string, s6, "@ The peasants hired mercenaries and are rebelling against you."),
            (set_background_mesh, "mesh_pic_villageriot"),
          (else_try),
           ##diplomacy end
            (set_background_mesh, "mesh_pic_bandits"),
          (try_end),
        (else_try),
          (party_slot_eq, "$current_town", slot_village_state, svs_looted),
          (str_store_string, s6, "@ The village has been looted. A handful of souls scatter as you pass through the burnt out houses."),
          (try_begin),
            (neq, "$g_player_raid_complete", 1),
            (play_track, "track_empty_village", 1),
          (try_end),
          (set_background_mesh, "mesh_pic_looted_village"),
        (else_try),
          (party_slot_eq, "$current_town", slot_village_state, svs_being_raided),
          (str_store_string, s6, "@ The village is being raided."),
        (else_try),
		  #gekokujo only one village picture type
          #(party_get_current_terrain, ":cur_terrain", "$current_town"),
          #(try_begin),
          #  (this_or_next|eq, ":cur_terrain", rt_steppe),
          #  (this_or_next|eq, ":cur_terrain", rt_steppe_forest),
          #  (this_or_next|eq, ":cur_terrain", rt_desert),
          #  (             eq, ":cur_terrain", rt_desert_forest),
          #  (set_background_mesh, "mesh_pic_village_s"),
          #(else_try),
          #  (this_or_next|eq, ":cur_terrain", rt_snow),
          #  (             eq, ":cur_terrain", rt_snow_forest),
          #  (set_background_mesh, "mesh_pic_village_w"),
          #(else_try),
          #  (set_background_mesh, "mesh_pic_village_p"),
          #(try_end),
		  (set_background_mesh, "mesh_gekokujo_pic_village"),
        (try_end),

        (try_begin),
          (eq, "$g_player_raid_complete", 1),
          (assign, "$g_player_raid_complete", 0),
          (jump_to_menu, "mnu_village_loot_complete"),
        (else_try),
          (party_get_slot, ":raider_party", "$current_town", slot_village_raided_by),
          (gt, ":raider_party", 0),
        # Process here...
        (try_end),

        (try_begin),
          (eq,"$g_leave_town",1),
          (assign,"$g_leave_town",0),
          (change_screen_return),
        (try_end),

        (try_begin), 
          (store_time_of_day, ":cur_hour"),
          (ge, ":cur_hour", 5),
          (lt, ":cur_hour", 21),
          (assign, "$town_nighttime", 0),
        (else_try),
          (assign, "$town_nighttime", 1),
        (try_end),
    ],
    [
      ("village_manage",
      [
        (neg|party_slot_eq, "$current_town", slot_village_state, svs_looted),
        (neg|party_slot_eq, "$current_town", slot_village_state, svs_being_raided),
        (neg|party_slot_ge, "$current_town", slot_village_infested_by_bandits, 1),
        (party_slot_eq, "$current_town", slot_town_lord, "trp_player")
        ]
       ,"Manage this village.",
       [
           (assign, "$g_next_menu", "mnu_village"),
           (jump_to_menu, "mnu_center_manage"),
        ]),
#deprecated
#	#Gekokujo - Talk to village elder START      
#      ("village_elder_talk",[(neg|party_slot_eq, "$current_town", slot_village_state, svs_looted),
#                         (neg|party_slot_eq, "$current_town", slot_village_state, svs_being_raided),
#                         (neg|party_slot_ge, "$current_town", slot_village_infested_by_bandits, 1),]
#       ,"Speak with the Village Elder.",
#       [
#         (try_begin),
#           (call_script, "script_cf_enter_center_location_bandit_check"),
#         (else_try),
#           (party_get_slot, ":village_scene", "$current_town", slot_castle_exterior),
#           (modify_visitors_at_site,":village_scene"),
#           (reset_visitors),
#           (party_get_slot, ":village_elder_troop", "$current_town",slot_town_elder),
#           (set_visitor, 11, ":village_elder_troop"),

#           (call_script, "script_init_town_walkers"),

#           (try_begin),
#             (check_quest_active, "qst_hunt_down_fugitive"),
#             (neg|is_currently_night),
#             (quest_slot_eq, "qst_hunt_down_fugitive", slot_quest_target_center, "$current_town"),
#             (neg|check_quest_succeeded, "qst_hunt_down_fugitive"),
#             (neg|check_quest_failed, "qst_hunt_down_fugitive"),
#             (set_visitor, 45, "trp_fugitive"),
#           (try_end),

#           (set_jump_mission,"mt_village_center"),
#           (jump_to_scene,":village_scene"),

#           (change_screen_map_conversation, ":village_elder_troop"),
#         (try_end),
#        ],"Door to the village center."),
#	#Gekokujo - Talk to village elder END
#	#From HokieBT
      ("recruit_volunteers",
      [
        (call_script, "script_cf_village_recruit_volunteers_cond"),
       ]
       ,"Recruit Volunteers.",
       [
         (try_begin),
           (call_script, "script_cf_enter_center_location_bandit_check"),
         (else_try),
           (jump_to_menu, "mnu_recruit_volunteers"),
         (try_end),
        ]),
      ("village_center",[(neg|party_slot_eq, "$current_town", slot_village_state, svs_looted),
                         (neg|party_slot_eq, "$current_town", slot_village_state, svs_being_raided),
                         (neg|party_slot_ge, "$current_town", slot_village_infested_by_bandits, 1),]
       ,"Go to the village center.",
       [
         (try_begin),
           (call_script, "script_cf_enter_center_location_bandit_check"),
         (else_try),
           (party_get_slot, ":village_scene", "$current_town", slot_castle_exterior),
           (modify_visitors_at_site,":village_scene"),
           (reset_visitors),
           (party_get_slot, ":village_elder_troop", "$current_town",slot_town_elder),
           (set_visitor, 11, ":village_elder_troop"),
           ##diplomacy begin
           (try_begin),
             (gt, "$g_player_chamberlain", 0),
             (call_script, "script_dplmc_appoint_chamberlain"),  #fix for wrong troops after update
             (party_get_slot, ":town_lord", "$current_town", slot_town_lord),
             (eq, ":town_lord", "trp_player"),
             (set_visitor, 9, "$g_player_chamberlain"),
           (try_end),
           ##diplomacy end

           (call_script, "script_init_town_walkers"),

           (try_begin),
             (check_quest_active, "qst_hunt_down_fugitive"),
             (neg|is_currently_night),
             (quest_slot_eq, "qst_hunt_down_fugitive", slot_quest_target_center, "$current_town"),
             (neg|check_quest_succeeded, "qst_hunt_down_fugitive"),
             (neg|check_quest_failed, "qst_hunt_down_fugitive"),
             (set_visitor, 45, "trp_fugitive"),
           (try_end),

           (set_jump_mission,"mt_village_center"),
           (jump_to_scene,":village_scene"),
           (change_screen_mission),
         (try_end),
        ],"Door to the village center."),
       ##diplomacy begin
      ("dplmc_village_elder_meeting",[
         (neg|party_slot_eq, "$current_town", slot_village_state, svs_looted),
         (neg|party_slot_eq, "$current_town", slot_village_state, svs_being_raided),
         (neg|party_slot_ge, "$current_town", slot_village_infested_by_bandits, 1),
	   ##diplomacy start+
		#rubik had a good idea: only enable this after having met the village elder
		(party_get_slot, ":village_elder_troop", "$current_town",slot_town_elder),
		(gt, ":village_elder_troop", 0),
		(this_or_next|eq, "$cheat_mode", 1),#Always can jump to village elder in cheat mode
		    (troop_slot_ge,":village_elder_troop", slot_troop_met, 1),
		##diplomacy end+
       ]
       ,"Meet the village headman.",
       [
         (try_begin),
           (call_script, "script_cf_enter_center_location_bandit_check"),
         (else_try),
           (party_get_slot, ":village_scene", "$current_town", slot_castle_exterior),
           (modify_visitors_at_site,":village_scene"),
           (reset_visitors),
           (party_get_slot, ":village_elder_troop", "$current_town",slot_town_elder),
           (set_visitor, 11, ":village_elder_troop"),

           (set_jump_mission,"mt_village_center"),
           (jump_to_scene,":village_scene"),
           (change_screen_map_conversation, ":village_elder_troop"),
         (try_end),
        ]),
      ##diplomacy end
	##diplomacy start+
	#If you can't jump to the village elder, explain why
    ("dplmc_village_elder_meeting_denied",
	[
		#Only show this when the player would get the rest of the village menus
        (neg|party_slot_eq, "$current_town", slot_village_state, svs_looted),
        (neg|party_slot_eq, "$current_town", slot_village_state, svs_being_raided),
        (neg|party_slot_ge, "$current_town", slot_village_infested_by_bandits, 1),
	    #There is a valid village elder, and you haven't met him,
		#and there isn't another condition that enables the jump.
		(party_get_slot, ":village_elder_troop", "$current_town",slot_town_elder),
		(gt, ":village_elder_troop", 0),
		(eq, "$cheat_mode", 0),
		(troop_slot_eq, ":village_elder_troop", slot_troop_met, 0),
		(disable_menu_option),
		],
       "You have not met the village headman yet.",
       [
     ]),
     
      #gekokujo 3.1 labor start
      ("gekokujo_labor",
	    [
		  #Only show this when the player would get the rest of the village menus
          (neg|party_slot_eq, "$current_town", slot_village_state, svs_looted),
          (neg|party_slot_eq, "$current_town", slot_village_state, svs_being_raided),
          (neg|party_slot_ge, "$current_town", slot_village_infested_by_bandits, 1),
		],
        "Find work in the village.",
        [
          (jump_to_menu, "mnu_labor"),
        ]),
      #gekokujo 3.1 labor end
     
	 ##diplomacy end+
      ("village_buy_food",[(party_slot_eq, "$current_town", slot_village_state, 0),
                           (neg|party_slot_ge, "$current_town", slot_village_infested_by_bandits, 1),
                           ],"Buy supplies from the peasants.",
       [
         (try_begin),
           (call_script, "script_cf_enter_center_location_bandit_check"),
         (else_try),
           (party_get_slot, ":merchant_troop", "$current_town", slot_town_elder),

      #(try_for_range, ":cur_goods", trade_goods_begin, trade_goods_end),
        #(store_sub, ":cur_good_price_slot", ":cur_goods", trade_goods_begin),
        #(val_add, ":cur_good_price_slot", slot_town_trade_good_prices_begin),
		#(party_get_slot, ":cur_price", "$current_town", ":cur_good_price_slot"),
	    #(call_script, "script_center_get_production", "$current_town", ":cur_goods"),
        #(assign, reg13, reg0),
	    #(call_script, "script_center_get_consumption", "$current_town", ":cur_goods"),
        #(str_store_party_name, s1, "$current_town"),
        #(str_store_item_name, s2, ":cur_goods"),
		#(assign, reg16, ":cur_price"),
        #(display_log_message, "@DEBUG:{s1}-{s2}, prd: {reg13}, con: {reg0}, raw: {reg1}, cns: {reg2}, fee: {reg16}"),
	  #(try_end),

           (change_screen_trade, ":merchant_troop"),
         (try_end),
         ]),
##diplomacy start+
#Import rubik's Auto-Sell options from Custom Commander
      ("dplmc_village_auto_sell",
        [
         (party_slot_eq, "$current_town", slot_village_state, 0),
         (neg|party_slot_ge, "$current_town", slot_village_infested_by_bandits, 1),
			(party_get_slot, ":village_elder_troop", "$current_town",slot_town_elder),
			(ge, ":village_elder_troop", 0),
        ],
       "Automatically sell items.",
       [
          (assign, "$g_next_menu", "mnu_village"),
          (jump_to_menu,"mnu_dplmc_trade_auto_sell_begin"),
        ]),

      ("dplmc_village_auto_buy_food",
        [
          (party_slot_eq, "$current_town", slot_village_state, 0),
			 (party_get_slot, ":village_elder_troop", "$current_town",slot_town_elder),
			 (ge, ":village_elder_troop", 0),
          (neg|party_slot_ge, "$current_town", slot_village_infested_by_bandits, 1),
        ],
       "Automatically buy food.",
       [
          (assign, "$g_next_menu", "mnu_village"),
          (jump_to_menu,"mnu_dplmc_trade_auto_buy_food_begin"),
        ]),
##diplomacy end+
      ("village_attack_bandits",[(party_slot_ge, "$current_town", slot_village_infested_by_bandits, 1),],
       "Attack the bandits.",
       [(party_get_slot, ":bandit_troop", "$current_town", slot_village_infested_by_bandits),
        (party_get_slot, ":scene_to_use", "$current_town", slot_castle_exterior),
        (modify_visitors_at_site,":scene_to_use"),
        (reset_visitors),
        (set_visitors, 0, ":bandit_troop", "$qst_eliminate_bandits_infesting_village_num_bandits"),
        (set_visitors, 2, "trp_farmer", "$qst_eliminate_bandits_infesting_village_num_villagers"),
        (set_party_battle_mode),
        (set_battle_advantage, 0),
        (assign, "$g_battle_result", 0),
        (set_jump_mission,"mt_village_attack_bandits"),
        (jump_to_scene, ":scene_to_use"),
        (assign, "$g_next_menu", "mnu_village_infest_bandits_result"),
        (jump_to_menu, "mnu_battle_debrief"),
        (assign, "$g_mt_mode", vba_normal),
        (change_screen_mission),
        ]),

      ("village_wait",
       [(party_slot_eq, "$current_town", slot_center_has_manor, 1),
        (party_slot_eq, "$current_town", slot_town_lord, "trp_player"),
        ],
         "Wait here for some time.",
         [
           (assign,"$auto_enter_town","$current_town"),
           (assign, "$g_last_rest_center", "$current_town"),

           (try_begin),
             (party_is_active, "p_main_party"),
             (party_get_current_terrain, ":cur_terrain", "p_main_party"),
             (try_begin),
               (eq, ":cur_terrain", rt_desert),
               (unlock_achievement, ACHIEVEMENT_SARRANIDIAN_NIGHTS),
             (try_end),  
           (try_end),  

           (rest_for_hours_interactive, 24 * 7, 5, 1), #rest while attackable

           (change_screen_return),
          ]),
      
       ##diplomacy begin
      ("dplmc_village_counter_insurgency",[
        (party_slot_eq, "$current_town", slot_village_infested_by_bandits, "trp_peasant_woman"),
        ],
       "Counter the insurgency.",
       [
          (store_random_in_range, ":enmity", -10, -5),
          (call_script, "script_change_player_relation_with_center", "$current_town", ":enmity"),
          (call_script, "script_calculate_battle_advantage"),
          (set_battle_advantage, reg0),
          (set_party_battle_mode),
          (assign, "$g_battle_result", 0),
          (assign, "$g_village_raid_evil", 1), #check
          (set_jump_mission,"mt_village_raid"),
          (party_get_slot, ":scene_to_use", "$current_town", slot_castle_exterior),
          (jump_to_scene, ":scene_to_use"),
          (assign, "$g_next_menu", "mnu_dplmc_village_riot_result"),

          (call_script, "script_objectionable_action", tmt_humanitarian, "str_loot_village"),
          (jump_to_menu, "mnu_battle_debrief"),
          (change_screen_mission),
        ]),

      ("dplmc_village_negotiate",[
        (party_slot_eq, "$current_town", slot_village_infested_by_bandits, "trp_peasant_woman"),
        ],
       "Begin negotiations.",
       [
          (jump_to_menu, "mnu_dplmc_riot_negotiate"),
        ]),
        ##diplomacy end      
      
      ("collect_taxes_qst",[(party_slot_eq, "$current_town", slot_village_state, 0),
                            (neg|party_slot_ge, "$current_town", slot_village_infested_by_bandits, 1),
                            (check_quest_active, "qst_collect_taxes"),
                            (quest_get_slot, ":quest_giver_troop", "qst_collect_taxes", slot_quest_giver_troop),
                            (quest_slot_eq, "qst_collect_taxes", slot_quest_target_center, "$current_town"),
                            (neg|quest_slot_eq, "qst_collect_taxes", slot_quest_current_state, 4),
                            (str_store_troop_name, s1, ":quest_giver_troop"),
                            (quest_get_slot, reg5, "qst_collect_taxes", slot_quest_current_state),
                            ], "{reg5?Continue collecting taxes:Collect taxes} due to {s1}.",
       [(jump_to_menu, "mnu_collect_taxes"),]),

      ("train_peasants_against_bandits_qst",
       [
         (party_slot_eq, "$current_town", slot_village_state, 0),
         (check_quest_active, "qst_train_peasants_against_bandits"),
         (neg|check_quest_concluded, "qst_train_peasants_against_bandits"),
         (quest_slot_eq, "qst_train_peasants_against_bandits", slot_quest_target_center, "$current_town"),
         ], "Train the peasants.",
       [(jump_to_menu, "mnu_train_peasants_against_bandits"),]),

      ("village_hostile_action",[(party_slot_eq, "$current_town", slot_village_state, 0),
                                 (neg|party_slot_ge, "$current_town", slot_village_infested_by_bandits, 1),
								 (neq, "$players_kingdom", "$g_encountered_party_faction"),
								 ], "Take a hostile action.",
       [(jump_to_menu,"mnu_village_hostile_action"),
           ]),
      
      ("village_reports",[(eq, "$cheat_mode", 1),], "{!}CHEAT! Show reports.",
       [(jump_to_menu,"mnu_center_reports"),
           ]),
	  #gekokujo scene editing - villages
      ("village_cheat_exterior",[(eq, "$cheat_mode", 1)], "{!}CHEAT! Exterior.",[
#                                                       (set_jump_mission,"mt_town_default"),
                                                       (set_jump_mission,"mt_ai_training"),
                                                       (party_get_slot, ":village_scene", "$current_town", slot_castle_exterior),
                                                       (jump_to_scene,":village_scene"),
                                                       (change_screen_mission)]),
      ("village_leave",[],"Leave...",[(change_screen_return,0),
	  ##diplomacy start+
	  ##Importing auto-purchase of food from rubik's Custom Commander
	  (try_begin),
		 (party_slot_eq, "$current_town", slot_village_state, 0),
		 (neg|party_slot_ge, "$current_town", slot_village_infested_by_bandits, 1),
		 (party_get_slot, ":merchant_troop", "$current_town",slot_town_elder),
		 (gt, ":merchant_troop", 0),
		 (call_script, "script_dplmc_initialize_autoloot", 0),#argument "0" means this does nothing if deemed unnecessary
		 (try_begin),
			(eq, "$g_dplmc_buy_food_when_leaving", 1),
			(call_script, "script_dplmc_auto_buy_food", "trp_player", ":merchant_troop"),
		 (try_end),
		 (try_begin),
			(eq, "$g_dplmc_sell_items_when_leaving", 1),
			(call_script, "script_dplmc_auto_sell", "trp_player", ":merchant_troop", "$g_dplmc_auto_sell_price_limit", all_items_begin, all_items_end, 2),
		 (try_end),
	  (try_end),
	  ##diplomacy end+
	  ]),
      
    ],
  ),
  
  (
    "close",0,
    "Nothing.",
    "none",
    [
        (change_screen_return),
      ],
    [],
  ),
# They must learn field discipline and the steadiness to follow orders in combat before they can be thought to use arms.",
  (
    "train_peasants_against_bandits",0,
    "As the party member with the highest training skill ({reg2}), {reg3?you expect:{s1} expects} that getting some peasants ready for practice will take {reg4} hours.",
    "none",
    [(call_script, "script_get_max_skill_of_player_party", "skl_trainer"),
     (assign, ":max_skill", reg0),
     (assign, reg2, reg0),
     (assign, ":max_skill_owner", reg1),
     (try_begin),
       (eq, ":max_skill_owner", "trp_player"),
       (assign, reg3, 1),
     (else_try),
       (assign, reg3, 0),
       (str_store_troop_name, s1, ":max_skill_owner"),
     (try_end),
     (store_sub, ":needed_hours", 20, ":max_skill"),
     (val_mul, ":needed_hours", 3),
     (val_div, ":needed_hours", 5),
     (store_sub, reg4, ":needed_hours", "$qst_train_peasants_against_bandits_num_hours_trained"),
     ],
    [
      ("make_preparation", [], "Train them.",
       [
         (assign, "$qst_train_peasants_against_bandits_currently_training", 1),
         (rest_for_hours_interactive, 1000, 5, 0), #rest while not attackable
         (assign, "$auto_enter_town", "$current_town"),
         (assign, "$g_town_visit_after_rest", 1),
         (change_screen_return),
         ]),
      ("train_later", [], "Put it off until later.",
       [
         (jump_to_menu, "mnu_village"),
        ]),
    ]
  ),
  (
    "center_reports",0,
    "Town Name: {s1}^Rent Income: {reg1} mon^Tariff Income: {reg2} mon^Food Stock: for {reg3} days",
    "none",
    [(party_get_slot, ":town_food_store", "$g_encountered_party", slot_party_food_store),
     (call_script, "script_center_get_food_consumption", "$g_encountered_party"),
     (assign, ":food_consumption", reg0),
     (try_begin),
       (gt, ":food_consumption", 0),
       (store_div, reg3, ":town_food_store", ":food_consumption"),
     (else_try),
       (assign, reg3, 9999),
     (try_end),
     (str_store_party_name, s1, "$g_encountered_party"),
     (party_get_slot, reg1, "$g_encountered_party", slot_center_accumulated_rents),
     (party_get_slot, reg2, "$g_encountered_party", slot_center_accumulated_tariffs),
     ],
    [
      ("to_price_and_productions", [], "Show prices and productions.",
       [(jump_to_menu, "mnu_price_and_production"),
        ]),
      
      ("go_back_dot",[],"Go back.",
       [(try_begin),
          (party_slot_eq, "$g_encountered_party", slot_party_type, spt_village),
          (jump_to_menu, "mnu_village"),
        (else_try),
          (jump_to_menu, "mnu_town"),
        (try_end),
        ]),
    ]
  ),
##diplomacy start+
##Begin auto-sell credit rubik (Custom Commander)
##Altered to only sell items from the player's inventory, not his companions'.
#
#Uses global variable $g_auto_sell_price_limit changed to $g_dplmc_auto_sell_price_limit
## CC
  (
    "dplmc_trade_auto_sell_begin",0,
    "Items in your inventory whose type is marked as sellable and whose prices \
are below {reg1} mon will be sold to the {reg2?appropriate merchants:elder} \
in the current {reg2?town:village} automatically.  Specifically food, trade \
goods, and books will never be sold. ^^You can change some settings here freely.",
    "none",
  [
	##dplmc+ added section begin
    (this_or_next|is_between, "$current_town", towns_begin, towns_end),
	    (is_between, "$current_town", villages_begin, villages_end),
	(call_script, "script_dplmc_initialize_autoloot", 0),#argument "0" means this does nothing if deemed unnecessary
	##dplmc+ added section end
    (assign, reg1, "$g_dplmc_auto_sell_price_limit"),
	 (assign, reg2, 0),
    (try_begin),
      (is_between, "$current_town", towns_begin, towns_end),
      (assign, reg2, 1),
    (try_end),
  ],
  [
    ("continue",[],"Continue...",
    [
      #(call_script, "script_auto_sell_all"),
	  (call_script, "script_dplmc_player_auto_sell_at_center", "$current_town"),
      (jump_to_menu, "$g_next_menu"),
      ]),
    ("change_settings",[],"Change settings.",[(start_presentation, "prsnt_dplmc_auto_sell_options"),]),
    ("go_back",[],"Go back",[(jump_to_menu, "$g_next_menu")]),
  ]
  ),
  
    (
    "debug_alert_from_s65",0,
    "DEBUG ALERT: {s65}",
    "none",
    [
    ],
    [
      ("continue",[],"Continue...",
       [
		(assign, "$debug_message_in_queue", 0),
        (change_screen_return),
        ]),
     ]
  ),
      
  (
    "auto_return_to_map",0,
    "stub",
    "none",
    [(change_screen_map)],
    []
  ),
 

  ("lost_tavern_duel",mnf_disable_all_keys,
    "{s11}",
    "none",
    [
	(try_begin),
		(agent_get_troop_id, ":type", "$g_main_attacker_agent"),
		(eq, ":type", "trp_belligerent_drunk"),
		(str_store_string, s11, "str_lost_tavern_duel_ordinary"),
	(else_try),
		(agent_get_troop_id, ":type", "$g_main_attacker_agent"),
		(eq, ":type", "trp_hired_assassin"),
		(str_store_string, s11, "str_lost_tavern_duel_assassin"),
	(try_end),
	(troop_set_slot, "trp_hired_assassin", slot_troop_cur_center, -1),
    ],
    [
      ("continue",[],"Continue...",
       [         
         (jump_to_menu, "mnu_town"),         
       ]),       
    ]
  ),
]
