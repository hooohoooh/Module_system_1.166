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

game_menus_camp_cheat = [
  
  ("camp_cheat",0,
   "Select a cheat:",
   "none",
   [
     ],
    [
	   
      ("camp_cheat_find_item",[], "Find an item...",
       [
         (jump_to_menu, "mnu_cheat_find_item"),
	   ]
       ),	   

      #("camp_cheat_find_item",[], "Change weather..",
      ("camp_cheat_change_weather",[], "Change weather..",
       [
         (jump_to_menu, "mnu_cheat_change_weather"),
	   ]
       ),	   
	   
      ("camp_cheat_1",[],"{!}Increase player renown.",
       [
         (str_store_string, s1, "@Player renown is increased by 100. "),
         (call_script, "script_change_troop_renown", "trp_player", 100),
         (jump_to_menu, "mnu_camp_cheat"),
        ]
       ),
	   
      ("camp_cheat_2",[],"{!}Increase player honor.",      
       [
         (assign, reg7, "$player_honor"),
         (val_add, reg7, 1),
         (display_message, "@Player honor is increased by 1 and it is now {reg7}."),
         (val_add, "$player_honor", 1),
         (jump_to_menu, "mnu_camp_cheat"),
        ]
       ),

      ("camp_cheat_3",[],"{!}Update political notes.",
       [
         (try_for_range, ":hero", active_npcs_begin, active_npcs_end),
           (troop_slot_eq, ":hero", slot_troop_occupation, slto_kingdom_hero),
           (call_script, "script_update_troop_political_notes", ":hero"),
         (try_end),
         
         (try_for_range, ":kingdom", kingdoms_begin, kingdoms_end),
           (call_script, "script_update_faction_political_notes", ":kingdom"),
         (try_end),		
        ]
       ),	   
	   
      ("camp_cheat_4",[],"{!}Update troop notes.",
       [
         (try_for_range, ":hero", active_npcs_begin, active_npcs_end),
           (troop_slot_eq, ":hero", slot_troop_occupation, slto_kingdom_hero),
           (call_script, "script_update_troop_notes", ":hero"),
         (try_end),
         
         (try_for_range, ":lady", kingdom_ladies_begin, kingdom_ladies_end),
           (call_script, "script_update_troop_notes", ":lady"),
           (call_script, "script_update_troop_political_notes", ":lady"),
           (call_script, "script_update_troop_location_notes", ":lady", 0),
         (try_end),		
        ]
       ),	   
	   
      ("camp_cheat_5",[],"{!}Scramble minstrels.",
       [
         (call_script, "script_update_tavern_minstrels"),
        ]
       ),	   
	   
      ("camp_cheat_6",[],"{!}Infinite camp",
       [
         (assign,"$g_camp_mode", 1),
         (assign, "$g_infinite_camping", 1),
         (assign, "$g_player_icon_state", pis_camping),
         (rest_for_hours_interactive, 10 * 24 * 365, 20), #10 year rest while not attackable with 20x speed
         (change_screen_return),
        ]
       ),	   
       
	   ##nested diplomacy start+
	  ("camp_cheat_7",[(troop_slot_ge, "trp_player", slot_troop_spouse, 1),],"{!}Divorce player spouse",
       [
	 	 (troop_get_slot, ":spouse", "trp_player", slot_troop_spouse),
        #set this before the loop below, to avoid potential wierdness in the family relation check
		 (troop_set_slot, ":spouse", slot_troop_spouse, -1),
	     (troop_set_slot, "trp_player", slot_troop_spouse, -1),

		#apply relation loss with the spouse
		 (call_script, "script_change_player_relation_with_troop", ":spouse", -40),
	    #change relations with family - inverse of gain from marriage
		(try_for_range, ":family_member", heroes_begin, heroes_end),
		    (neq, ":family_member", ":spouse"),
			(call_script, "script_dplmc_troop_get_family_relation_to_troop", ":spouse", ":family_member"),
			(gt, reg0, 0),
			(val_mul, reg0, -2),
			(val_div, reg0, 3),
			(val_min, reg0, -1),
			(call_script, "script_change_player_relation_with_troop", ":family_member", reg0),
		(try_end),
        ]
       ),
	   ##nested diplomacy end+       

      ("cheat_faction_orders",[(ge,"$cheat_mode",1)],
	  "{!}Cheat: Set Debug messages to All.",
       [(assign,"$cheat_mode",1),
         (jump_to_menu, "mnu_camp_cheat"),
        ]
       ),
      ("cheat_faction_orders",[
	  (ge, "$cheat_mode", 1),
	  (neq,"$cheat_mode",3)],"{!}Cheat: Set Debug messages to Econ Only.",
       [(assign,"$cheat_mode",3),
         (jump_to_menu, "mnu_camp_cheat"),
        ]
       ),
      ("cheat_faction_orders",[
	  (ge, "$cheat_mode", 1),
	  (neq,"$cheat_mode",4)],"{!}Cheat: Set Debug messages to Political Only.",
       [(assign,"$cheat_mode",4),
         (jump_to_menu, "mnu_camp_cheat"),
        ]
       ),
	   
	   
      ("back_to_camp_menu",[],"{!}Back to camp menu.",
       [
         (jump_to_menu, "mnu_camp"),
        ]
       ),
      ]
  ),
  
  #gekokujo 3.0 cheat menu consolidation start
  ("camp_gekokujo",0,
   "Current Difficulty: +{reg14}%^^Select an option:",
   "none",
    [
      #gekokujo 3.1 difficulty calculation start
	  (assign, reg14, 0),
	  
      (try_begin),
	    (eq, "$g_gekokujo_encounter_rate", 1), #reduced encounter rate = +3%
	    (val_add, reg14, 3),
	  (try_end),
	  
      (try_begin),
		(eq, "$g_gekokujo_encounter_rate", 0), #normal encounter rate = +7%
		(val_add, reg14, 7),
	  (try_end),
      
      (try_begin),
		(eq, "$g_gekokujo_bandit_reduction", 0), #normal bandit spawn = +13%
		(val_add, reg14, 13),
	  (try_end),
	  
      (try_begin),
		(eq, "$g_gekokujo_companion_neverquit", 0), #companions can quit = +20%
		(val_add, reg14, 20),
	  (try_end),
	  
      (try_begin),
		(eq, "$g_gekokujo_old_siege", 0), #new siege style = +27%
		(val_add, reg14, 27),
	  (try_end),
	  
      (try_begin),
		(eq, "$g_gekokujo_samurai_penalty", 1), #samurai penalty = +33%
		(val_add, reg14, 33),
	  (try_end),
      #gekokujo 3.1 difficulty calculation end
    ],
    [
	#gekokujo 3.1 biography page start
      ("gekokujo_bio",[],"Read {playername}'s biography...",[
	      (jump_to_menu, "mnu_gekokujo_bio"),
        ]),
	#gekokujo 3.1 biography page end
	
	#gekokujo 3.1 random encounters start (menu option to disable/disable)
      ("gekokujo_encounter_rate_0",[(eq, "$g_gekokujo_encounter_rate", 0),],"Random Encounters Enabled",[
	      (assign, "$g_gekokujo_encounter_rate", 1),
	      (jump_to_menu, "mnu_camp_gekokujo"),
        ]),
      ("gekokujo_encounter_rate_1",[(eq, "$g_gekokujo_encounter_rate", 1),],"Random Encounters Reduced",[
	      (assign, "$g_gekokujo_encounter_rate", 2),
	      (jump_to_menu, "mnu_camp_gekokujo"),
        ]),
      ("gekokujo_encounter_rate_2",[(eq, "$g_gekokujo_encounter_rate", 2),],"Random Encounters Disabled",[
	      (assign, "$g_gekokujo_encounter_rate", 0),
	      (jump_to_menu, "mnu_camp_gekokujo"),
        ]),
      #("gekokujo_encounter_test",[],"Test Random Encounter",[
	  #    (assign, "$gekokujo_encounter_accepted", 0),
      #    (jump_to_menu, "mnu_encounter"),
      #  ]),
	#gekokujo 3.1 random encounters end
    
	#gekokujo 3.0 bandit rate option start (menu option to disable/disable)
      ("gekokujo_reduce_bandits",[(eq, "$g_gekokujo_bandit_reduction", 0),],"Bandit Count Normal",[
	      (assign, "$g_gekokujo_bandit_reduction", 1),
	      (jump_to_menu, "mnu_camp_gekokujo"),
        ]),
      ("gekokujo_increase_bandits",[(eq, "$g_gekokujo_bandit_reduction", 1),],"Bandit Count Reduced",[
	      (assign, "$g_gekokujo_bandit_reduction", 0),
	      (jump_to_menu, "mnu_camp_gekokujo"),
        ]),
	#gekokujo 3.0 bandit rate option end
	
	#gekokujo 3.0 companion interaction start (menu option to disable/disable)
      ("gekokujo_disable_companion_quit",[(eq, "$g_gekokujo_companion_neverquit", 0),],"Companions Can Quit",[
	      (assign, "$g_gekokujo_companion_neverquit", 1),
	      (jump_to_menu, "mnu_camp_gekokujo"),
        ]),
      ("gekokujo_enable_companion_quit",[(eq, "$g_gekokujo_companion_neverquit", 1),],"Companions Cannot Quit",[
	      (assign, "$g_gekokujo_companion_neverquit", 0),
	      (jump_to_menu, "mnu_camp_gekokujo"),
        ]),
	#gekokujo 3.0 companion interaction end
	
	#gekokujo 3.1 siege improvement start (menu option to disable/disable)
      ("gekokujo_disable_new_sieges",[(eq, "$g_gekokujo_old_siege", 0),],"Sieges Have Gates",[
	      (assign, "$g_gekokujo_old_siege", 1),
	      (jump_to_menu, "mnu_camp_gekokujo"),
        ]),
      ("gekokujo_enable_new_sieges",[(eq, "$g_gekokujo_old_siege", 1),],"Old-Style Sieges",[
	      (assign, "$g_gekokujo_old_siege", 0),
	      (jump_to_menu, "mnu_camp_gekokujo"),
        ]),
	#gekokujo 3.1 siege improvement end
	
	#gekokujo 3.1 samurai slots start (menu option to disable/disable)
      ("gekokujo_enable_samurai_penalty",[(eq, "$g_gekokujo_samurai_penalty", 0),],"Samurai Use 1 Party Slot",[
	      (assign, "$g_gekokujo_samurai_penalty", 1),
	      (jump_to_menu, "mnu_camp_gekokujo"),
        ]),
      ("gekokujo_disable_samurai_penalty",[(eq, "$g_gekokujo_samurai_penalty", 1),],"Samurai Use 2 Party Slots",[
	      (assign, "$g_gekokujo_samurai_penalty", 0),
	      (jump_to_menu, "mnu_camp_gekokujo"),
        ]),
	#gekokujo 3.1 samurai slots end
	
	#gekokujo 3.0 cheat menu start
      ("gekokujo_disable_cheat",[(eq, "$cheat_mode", 0),],"Cheat Mode Disabled",[
	      (assign, "$cheat_mode", 1),
	      (jump_to_menu, "mnu_camp_gekokujo"),
        ]),
		
      ("gekokujo_enable_cheat",[(eq, "$cheat_mode", 1),],"Cheat Mode Enabled",[
	      (assign, "$cheat_mode", 0),
	      (jump_to_menu, "mnu_camp_gekokujo"),
        ]),
	#gekokujo 3.0 cheat menu end
	   
	#gekokujo 3.1 separate cheat menu start
      ("gekokujo_cheat_menu",[(ge, "$cheat_mode", 1)], "GEKOKUJO CHEAT MENU!",
        [
          (jump_to_menu, "mnu_cheat_gekokujo"),
	    ]
	    ),
	   
      ("gekokujo_back_to_camp_menu",[],"{!}Back to camp menu.",
        [
          (jump_to_menu, "mnu_camp"),
          ]
        ),
      ]
  ),
  
  ("cheat_gekokujo",0,
   "Select a cheat:",
   "none",
   [],
    [
	#gekokujo 3.1 separate cheat menu end
	
      ("gekokujo_companions",[(ge, "$cheat_mode", 1)], "Find all companions...",
        [
          (jump_to_menu, "mnu_gekokujo_companions"),
	    ]
        ),
	   
      ("gekokujo_enter_scene",[(ge, "$cheat_mode", 1)], "Enter a special scene to edit...",
        [
          (jump_to_menu, "mnu_cheat_enter_scene"),
	    ]
	    ),
	   
      ("gekokujo_instant_army",[(ge, "$cheat_mode", 1)], "Form an army...",
        [
          (party_add_members, "p_main_party", "trp_gekokujo_oda_veteran_spearman", 15),
          (party_add_members, "p_main_party", "trp_gekokujo_oda_veteran_skirmisher", 15),
          (party_add_members, "p_main_party", "trp_gekokujo_oda_retainer", 10),
          (party_add_members, "p_main_party", "trp_gekokujo_oda_veteran_retainer", 8),
          (party_add_members, "p_main_party", "trp_gekokujo_oda_officer", 2),
		  (troop_add_gold, "trp_player", 10000),
		  (troop_add_item, "trp_player", "itm_bread"),
		  (troop_add_item, "trp_player", "itm_bread"),
		  (troop_add_item, "trp_player", "itm_bread"),
		  (troop_add_item, "trp_player", "itm_bread"),
		  (troop_add_item, "trp_player", "itm_gekokujo_katana_7"),
		  (troop_add_item, "trp_player", "itm_gekokujo_wakizashi_7"),
		  (troop_add_item, "trp_player", "itm_gekokujo_naginata_7"),
		  (troop_add_item, "trp_player", "itm_gekokujo_kabuto3_h_1"),
		  (troop_add_item, "trp_player", "itm_gekokujo_tekko_3_1"),
		  (troop_add_item, "trp_player", "itm_gekokujo_yukinoshita_long_1"),
		  (troop_add_item, "trp_player", "itm_gekokujo_shino_suneate_1"),
		  (troop_equip_items, "trp_player"),
          (change_screen_return),
	    ]
        ),	   
	   
	#gekokujo 3.1 separate cheat menu start
      ("gekokujo_back_to_gekokujo_menu",[],"{!}Back to Gekokujo options.",
        [
          (jump_to_menu, "mnu_camp_gekokujo"),
          ]
        ),
	#gekokujo 3.1 separate cheat menu end
      ]
  ),
  #gekokujo 3.0 all companion report end
  
  #gekokujo 3.0 edit scene menu start
  ("cheat_enter_scene",0,
    "Select a scene:",
    "none",
    [],
    [
      ("scene_next_page",[],"{!}Next Page", [
         (jump_to_menu, "mnu_cheat_enter_scene_p2"),
      ]),
	  
      ("camp_cheat_enter_scene_1", [], "Enter Scene: Bridge 1", [
       (set_jump_mission,"mt_ai_training"),
       (jump_to_scene,"scn_gekokujo_bridge_1"),
       (change_screen_mission)
	  ]),
	  
	  #screw it, we'll do it live
      #("camp_cheat_enter_scene_2", [], "Enter Scene: Bridge 2", [
      # (set_jump_mission,"mt_ai_training"),
      # (jump_to_scene,"scn_gekokujo_bridge_2"),
      # (change_screen_mission)
	  #]),
	  #
      #("camp_cheat_enter_scene_3", [], "Enter Scene: Bridge 3", [
      # (set_jump_mission,"mt_ai_training"),
      # (jump_to_scene,"scn_gekokujo_bridge_3"),
      # (change_screen_mission)
	  #]),
	  
      ("camp_cheat_enter_scene_4", [], "Enter Scene: Road 1", [
       (set_jump_mission,"mt_ai_training"),
       (jump_to_scene,"scn_gekokujo_road_1"),
       (change_screen_mission)
	  ]),
	  
      #("camp_cheat_enter_scene_5", [], "Enter Scene: Road 2", [
      # (set_jump_mission,"mt_ai_training"),
      # (jump_to_scene,"scn_gekokujo_road_2"),
      # (change_screen_mission)
	  #]),
	  #
      #("camp_cheat_enter_scene_6", [], "Enter Scene: Road 3", [
      # (set_jump_mission,"mt_ai_training"),
      # (jump_to_scene,"scn_gekokujo_road_3"),
      # (change_screen_mission)
	  #]),
	  
      ("camp_cheat_enter_scene_7", [], "Enter Scene: Sea 1 (Small vs Small)", [
       (set_jump_mission,"mt_ai_training"),
       (jump_to_scene,"scn_gekokujo_sea_1"),
       (change_screen_mission)
	  ]),
      ("camp_cheat_enter_scene_8", [], "Enter Scene: Sea 2 (Small vs Medium)", [
       (set_jump_mission,"mt_ai_training"),
       (jump_to_scene,"scn_gekokujo_sea_2"),
       (change_screen_mission)
	  ]),
      ("camp_cheat_enter_scene_9", [], "Enter Scene: Sea 3 (Medium vs Small)", [
       (set_jump_mission,"mt_ai_training"),
       (jump_to_scene,"scn_gekokujo_sea_3"),
       (change_screen_mission)
	  ]),
      ("camp_cheat_enter_scene_10", [], "Enter Scene: Sea 4 (Medium vs Medium)", [
       (set_jump_mission,"mt_ai_training"),
       (jump_to_scene,"scn_gekokujo_sea_4"),
       (change_screen_mission)
	  ]),
      ("camp_cheat_enter_scene_11", [], "Enter Scene: Island 1 (Small vs Large)", [
       (set_jump_mission,"mt_ai_training"),
       (jump_to_scene,"scn_gekokujo_island_1"),
       (change_screen_mission)
	  ]),
      ("camp_cheat_enter_scene_12", [], "Enter Scene: Island 2 (Medium vs Large)", [
       (set_jump_mission,"mt_ai_training"),
       (jump_to_scene,"scn_gekokujo_island_2"),
       (change_screen_mission)
	  ]),
      ("camp_cheat_enter_scene_13", [], "Enter Scene: Island 3 (Large vs Small)", [
       (set_jump_mission,"mt_ai_training"),
       (jump_to_scene,"scn_gekokujo_island_3"),
       (change_screen_mission)
	  ]),
      ("camp_cheat_enter_scene_14", [], "Enter Scene: Island 4 (Large vs Medium)", [
       (set_jump_mission,"mt_ai_training"),
       (jump_to_scene,"scn_gekokujo_island_4"),
       (change_screen_mission)
	  ]),
      ("camp_cheat_enter_scene_15", [], "Enter Scene: Island 5 (Large vs Large)", [
       (set_jump_mission,"mt_ai_training"),
       (jump_to_scene,"scn_gekokujo_island_5"),
       (change_screen_mission)
	  ]),
	  
      ("scene_back_to_cheat_menu",[],"{!}Back to Gekokujo cheat menu.", [
         (jump_to_menu, "mnu_cheat_gekokujo"),
      ]),
    ]
  ),
  
  ("cheat_enter_scene_p2",0,
    "Select a scene:",
    "none",
    [],
    [
      ("scene_p2_next_page",[],"{!}Next Page", [
         (jump_to_menu, "mnu_cheat_enter_scene_p3"),
      ]),
	  
      ("camp_cheat_enter_scene_16", [], "Enter Scene: Wedding Scene", [
       (set_jump_mission,"mt_ai_training"),
       (jump_to_scene,"scn_wedding"),
       (change_screen_mission)
	  ]),
      ("camp_cheat_enter_scene_17", [], "Enter Scene: Seto Pirate Lair", [
       (set_jump_mission,"mt_ai_training"),
       (jump_to_scene,"scn_lair_seto_pirates"),
       (change_screen_mission)
	  ]),
      ("camp_cheat_enter_scene_18", [], "Enter Scene: Kanto Rebel Lair", [
       (set_jump_mission,"mt_ai_training"),
       (jump_to_scene,"scn_lair_kanto_rebels"),
       (change_screen_mission)
	  ]),
      ("camp_cheat_enter_scene_19", [], "Enter Scene: Ezo Warrior Lair", [
       (set_jump_mission,"mt_ai_training"),
       (jump_to_scene,"scn_lair_northern_raiders"),
       (change_screen_mission)
	  ]),
      ("camp_cheat_enter_scene_20", [], "Enter Scene: Shinano Rebel Lair", [
       (set_jump_mission,"mt_ai_training"),
       (jump_to_scene,"scn_lair_shinano_rebels"),
       (change_screen_mission)
	  ]),
      ("camp_cheat_enter_scene_21", [], "Enter Scene: Woku Pirate Lair", [
       (set_jump_mission,"mt_ai_training"),
       (jump_to_scene,"scn_lair_woku_pirates"),
       (change_screen_mission)
	  ]),
      ("camp_cheat_enter_scene_22", [], "Enter Scene: Kinai Rebel Lair", [
       (set_jump_mission,"mt_ai_training"),
       (jump_to_scene,"scn_lair_kinai_rebels"),
       (change_screen_mission)
	  ]),
      ("camp_cheat_enter_scene_23", [], "Enter Scene: Monk Rebel Lair", [
       (set_jump_mission,"mt_ai_training"),
       (jump_to_scene,"scn_lair_monk_rebels"),
       (change_screen_mission)
	  ]),
      ("camp_cheat_enter_scene_24", [], "Enter Scene: Mansion Lair", [
       (set_jump_mission,"mt_ai_training"),
       (jump_to_scene,"scn_lair_mansion"),
       (change_screen_mission)
	  ]),
	  
      ("scene_p2_back_to_cheat_menu",[],"{!}Back to Gekokujo cheat menu.", [
         (jump_to_menu, "mnu_cheat_gekokujo"),
      ]),
    ]
  ),
  #gekokujo 3.0 edit scene menu end
  
  #gekokujo 3.1 new scenes start
  ("cheat_enter_scene_p3",0,
    "Select a scene:",
    "none",
    [],
    [
      ("scene_p3_next_page",[],"{!}Next Page", [
         (jump_to_menu, "mnu_cheat_enter_scene"),
      ]),
	  
      ("camp_cheat_enter_scene_25", [], "Enter Scene: Enterprise", [
       (set_jump_mission,"mt_ai_training"),
	   #only 1 type of enterprise interior from now on
	   (jump_to_scene,"scn_enterprise"),
	   #former enterprises:
       #(jump_to_scene,"scn_enterprise_tannery"), #lacquerworks
       #(jump_to_scene,"scn_enterprise_winery"), #soy sauce
       #(jump_to_scene,"scn_enterprise_smithy"), #smithy
       #(jump_to_scene,"scn_enterprise_dyeworks"), #silk weavery
       #(jump_to_scene,"scn_enterprise_linen_weavery"), #linen weavery
       #(jump_to_scene,"scn_enterprise_wool_weavery"), #hemp weavery
       #(jump_to_scene,"scn_enterprise_brewery"), #sake brewery
       #(jump_to_scene,"scn_enterprise_oil_press"), #fish press
       (change_screen_mission)
	  ]),
      ("camp_cheat_enter_scene_26", [], "Enter Scene: Alley Encounter", [
       (set_jump_mission,"mt_ai_training"),
       (jump_to_scene,"scn_encounter_alley"),
       (change_screen_mission)
	  ]),
      ("camp_cheat_enter_scene_27", [], "Enter Scene: Shop Encounter", [
       (set_jump_mission,"mt_ai_training"),
       (jump_to_scene,"scn_encounter_shop"),
       (change_screen_mission)
	  ]),
      ("camp_cheat_enter_scene_28", [], "Enter Scene: Mansion Encounter", [
       (set_jump_mission,"mt_ai_training"),
       (jump_to_scene,"scn_encounter_mansion"),
       (change_screen_mission)
	  ]),
      ("camp_cheat_enter_scene_29", [], "Enter Scene: Farm Encounter", [
       (set_jump_mission,"mt_ai_training"),
       (jump_to_scene,"scn_encounter_farm"),
       (change_screen_mission)
	  ]),
      ("camp_cheat_enter_scene_30", [], "Enter Scene: Road Encounter", [
       (set_jump_mission,"mt_ai_training"),
       (jump_to_scene,"scn_encounter_road"),
       (change_screen_mission)
	  ]),
      ("camp_cheat_enter_scene_31", [], "Enter Scene: Forest Encounter", [
       (set_jump_mission,"mt_ai_training"),
       (jump_to_scene,"scn_encounter_forest"), 
       (change_screen_mission)
	  ]),
      ("camp_cheat_enter_scene_32", [], "Enter Scene: Riverside Encounter", [
       (set_jump_mission,"mt_ai_training"),
       (jump_to_scene,"scn_encounter_river"), 
       (change_screen_mission)
	  ]),
      #("camp_cheat_enter_scene_33", [], "Enter Scene: House Encounter", [
      # (set_jump_mission,"mt_ai_training"),
      # (jump_to_scene,"scn_encounter_house"),
      # (change_screen_mission)
	  #]),
	  
      ("scene_p3_back_to_cheat_menu",[],"{!}Back to Gekokujo cheat menu.", [
         (jump_to_menu, "mnu_cheat_gekokujo"),
      ]),
    ]
  ),
  #gekokujo 3.1 biography page end
  
  ("cheat_find_item",0,
   "{!}Current item range: {reg5} to {reg6}",
   "none",
   [
     (assign, reg5, "$cheat_find_item_range_begin"),
     (store_add, reg6, "$cheat_find_item_range_begin", max_inventory_items),
	 (val_min, reg6, "itm_items_end"),
	 (val_sub, reg6, 1),
     ],
    [
      ("cheat_find_item_next_range",[], "{!}Move to next item range.",
       [
	    (val_add, "$cheat_find_item_range_begin", max_inventory_items),
	    (try_begin),
	      (ge, "$cheat_find_item_range_begin", "itm_items_end"),
		  (assign, "$cheat_find_item_range_begin", 0),
	    (try_end),
	    (jump_to_menu, "mnu_cheat_find_item"),
	   ]
       ),	   

	   ("cheat_find_item_choose_this",[], "{!}Choose from this range.",
       [
        (troop_clear_inventory, "trp_find_item_cheat"),
        (store_add, ":max_item", "$cheat_find_item_range_begin", max_inventory_items),
	    (val_min, ":max_item", "itm_items_end"),
		(store_sub, ":num_items_to_add", ":max_item", "$cheat_find_item_range_begin"),
		(try_for_range, ":i_slot", 0, ":num_items_to_add"),
		  (store_add, ":item_id", "$cheat_find_item_range_begin", ":i_slot"),
          (troop_add_items, "trp_find_item_cheat", ":item_id", 1),
        (try_end),
        (change_screen_trade, "trp_find_item_cheat"),
	   ]
       ),	   
	   
      ("camp_action_4",[],"{!}Back to camp menu.",
       [(jump_to_menu, "mnu_camp"),
        ]
       ),
      ]
  ),
   ("cheat_change_weather",0,
   "{!}Current cloud amount: {reg5}^Current Fog Strength: {reg6}",
   "none",
   [
     (get_global_cloud_amount, reg5),
     (get_global_haze_amount, reg6),
     ],
    [
      ("cheat_increase_cloud",[], "{!}Increase Cloud Amount.",
       [
	    (get_global_cloud_amount, ":cur_cloud_amount"),
		(val_add, ":cur_cloud_amount", 5),
		(val_min, ":cur_cloud_amount", 100),
	    (set_global_cloud_amount, ":cur_cloud_amount"),
	   ]
       ),
      ("cheat_decrease_cloud",[], "{!}Decrease Cloud Amount.",
       [
	    (get_global_cloud_amount, ":cur_cloud_amount"),
		(val_sub, ":cur_cloud_amount", 5),
		(val_max, ":cur_cloud_amount", 0),
	    (set_global_cloud_amount, ":cur_cloud_amount"),
	   ]
       ),
      ("cheat_increase_fog",[], "{!}Increase Fog Amount.",
       [
	    (get_global_haze_amount, ":cur_fog_amount"),
		(val_add, ":cur_fog_amount", 5),
		(val_min, ":cur_fog_amount", 100),
	    (set_global_haze_amount, ":cur_fog_amount"),
	   ]
       ),
      ("cheat_decrease_fog",[], "{!}Decrease Fog Amount.",
       [
	    (get_global_haze_amount, ":cur_fog_amount"),
		(val_sub, ":cur_fog_amount", 5),
		(val_max, ":cur_fog_amount", 0),
	    (set_global_haze_amount, ":cur_fog_amount"),
	   ]
       ),

      ("camp_action_4",[],"{!}Back to camp menu.",
       [(jump_to_menu, "mnu_camp"),
        ]
       ),
      ]
  ),
  ("camp_action",0,
   "Choose an action:",
   "none",
   [
     ],
    [
	

      ("camp_recruit_prisoners",
       [(troops_can_join, 1),
        (store_current_hours, ":cur_time"),
        (val_sub, ":cur_time", 24),
        (gt, ":cur_time", "$g_prisoner_recruit_last_time"),
        (try_begin),
          (gt, "$g_prisoner_recruit_last_time", 0),
          (assign, "$g_prisoner_recruit_troop_id", 0),
          (assign, "$g_prisoner_recruit_size", 0),
          (assign, "$g_prisoner_recruit_last_time", 0),
        (try_end),
        ], "Recruit some of your prisoners to your party.",
       [(jump_to_menu, "mnu_camp_recruit_prisoners"),
        ],
       ),
       
      ("action_read_book",[],"Select a book to read.",
       [(jump_to_menu, "mnu_camp_action_read_book"),
        ]
       ),
      ("action_rename_kingdom",
       [
         (eq, "$players_kingdom_name_set", 1),
         (faction_slot_eq, "fac_player_supporters_faction", slot_faction_state, sfs_active),
         (faction_slot_eq, "fac_player_supporters_faction", slot_faction_leader, "trp_player"),
         ],"Rename your domain.",
       [(start_presentation, "prsnt_name_kingdom"),
        ]
       ),

      ##diplomacy begin+
      ##Custom player kingdom vassal titles, credit Caba'drin start
       ("action_change_vassal_title",
        [
            (eq, "$players_kingdom_name_set", 1),
            (faction_slot_eq, "fac_player_supporters_faction", slot_faction_state, sfs_active),
            (faction_slot_eq, "fac_player_supporters_faction", slot_faction_leader, "trp_player"),
        ],"Change your vassals' title of nobility.",
        [(start_presentation, "prsnt_dplmc_set_vassal_title"),
        ]
       ),
       ("action_change_policies",
        [
            (gt, "$cheat_mode", 0),
            (eq, "$players_kingdom_name_set", 1),
            (faction_slot_eq, "fac_player_supporters_faction", slot_faction_state, sfs_active),
            (faction_slot_eq, "fac_player_supporters_faction", slot_faction_leader, "trp_player"),
        ],"{!}Cheat: Change domain policies",
        [(start_presentation, "prsnt_dplmc_policy_management"),

        ]
       ),
      ##Custom player kingdom vassal titles, credit Caba'drin end
      ##diplomacy end+

      ("action_modify_banner",[(eq, "$cheat_mode", 1)],"{!}Cheat: Modify your banner.",
       [
           (start_presentation, "prsnt_banner_selection"),
           #(start_presentation, "prsnt_custom_banner"),
        ]
       ),
      ("action_retire",[],"Retire from adventuring.",
       [(jump_to_menu, "mnu_retirement_verify"),
        ]
       ),
      ("camp_action_4",[],"Back to camp menu.",
       [(jump_to_menu, "mnu_camp"),
        ]
       ),
      ]
  ),
  ("camp_recruit_prisoners",0,
   "You offer your prisoners freedom if they agree to join you as soldiers. {s18}",
   "none",
   [(assign, ":num_regular_prisoner_slots", 0),
    (party_get_num_prisoner_stacks, ":num_stacks", "p_main_party"),
    (try_for_range, ":cur_stack", 0, ":num_stacks"),
      (party_prisoner_stack_get_troop_id, ":cur_troop_id", "p_main_party", ":cur_stack"),
      (neg|troop_is_hero, ":cur_troop_id"),
      (val_add, ":num_regular_prisoner_slots", 1),
    (try_end),
    (try_begin),
      (eq, ":num_regular_prisoner_slots", 0),
      (jump_to_menu, "mnu_camp_no_prisoners"),
    (else_try),
      (eq, "$g_prisoner_recruit_troop_id", 0),
      (store_current_hours, "$g_prisoner_recruit_last_time"),
      (store_random_in_range, ":rand", 0, 100),
      (store_skill_level, ":persuasion_level", "skl_persuasion", "trp_player"),
      (store_sub, ":reject_chance", 15, ":persuasion_level"),
      (val_mul, ":reject_chance", 4),
      (try_begin),
        (lt, ":rand", ":reject_chance"),
        (assign, "$g_prisoner_recruit_troop_id", -7),
      (else_try),
        (assign, ":num_regular_prisoner_slots", 0),
        (party_get_num_prisoner_stacks, ":num_stacks", "p_main_party"),
        (try_for_range, ":cur_stack", 0, ":num_stacks"),
          (party_prisoner_stack_get_troop_id, ":cur_troop_id", "p_main_party", ":cur_stack"),
          (neg|troop_is_hero, ":cur_troop_id"),
          (val_add, ":num_regular_prisoner_slots", 1),
        (try_end),
        (store_random_in_range, ":random_prisoner_slot", 0, ":num_regular_prisoner_slots"),
        (try_for_range, ":cur_stack", 0, ":num_stacks"),
          (party_prisoner_stack_get_troop_id, ":cur_troop_id", "p_main_party", ":cur_stack"),
          (neg|troop_is_hero, ":cur_troop_id"),
          (val_sub, ":random_prisoner_slot", 1),
          (lt, ":random_prisoner_slot", 0),
          (assign, ":num_stacks", 0),
          (assign, "$g_prisoner_recruit_troop_id", ":cur_troop_id"),
          (party_prisoner_stack_get_size, "$g_prisoner_recruit_size", "p_main_party", ":cur_stack"),
        (try_end),
      (try_end),

      (try_begin),
        (gt, "$g_prisoner_recruit_troop_id", 0),
        (party_get_free_companions_capacity, ":capacity", "p_main_party"),
        (val_min, "$g_prisoner_recruit_size", ":capacity"),
        (assign, reg1, "$g_prisoner_recruit_size"),
        (gt, "$g_prisoner_recruit_size", 0),
        (try_begin),
          (gt, "$g_prisoner_recruit_size", 1),
          (assign, reg2, 1),
        (else_try),
          (assign, reg2, 0),
        (try_end),
        (str_store_troop_name_by_count, s1, "$g_prisoner_recruit_troop_id", "$g_prisoner_recruit_size"),
        (str_store_string, s18, "@{reg1} {s1} {reg2?accept:accepts} the offer."),
      (else_try),
        (str_store_string, s18, "@No one accepts the offer."),
      (try_end),
    (try_end),
    ],
    [
      ("camp_recruit_prisoners_accept",[(gt, "$g_prisoner_recruit_troop_id", 0)],"Take them.",
       [(remove_troops_from_prisoners, "$g_prisoner_recruit_troop_id", "$g_prisoner_recruit_size"),
        (party_add_members, "p_main_party", "$g_prisoner_recruit_troop_id", "$g_prisoner_recruit_size"),
        (store_mul, ":morale_change", -3, "$g_prisoner_recruit_size"),
        (call_script, "script_change_player_party_morale", ":morale_change"),
        (jump_to_menu, "mnu_camp"),
        ]
       ),
      ("camp_recruit_prisoners_reject",[(gt, "$g_prisoner_recruit_troop_id", 0)],"Reject them.",
       [(jump_to_menu, "mnu_camp"),
        (assign, "$g_prisoner_recruit_troop_id", 0),
        (assign, "$g_prisoner_recruit_size", 0),
        ]
       ),
      ("continue",[(le, "$g_prisoner_recruit_troop_id", 0)],"Go back.",
       [(jump_to_menu, "mnu_camp"),
        ]
       ),
      ]
  ),
  
  ("camp_no_prisoners",0,
   "You have no prisoners to recruit from.",
   "none",
   [],
    [
      ("continue",[],"Continue...",
       [(jump_to_menu, "mnu_camp"),
        ]
       ),
      ]
  ),
  ("camp_action_read_book",0,
   "Choose a book to read:",
   "none",
   [],
    [
      ("action_read_book_1",[(player_has_item, "itm_book_tactics"),
                             (item_slot_eq, "itm_book_tactics", slot_item_book_read, 0),
                             (str_store_item_name, s1, "itm_book_tactics"),
                             ],"{s1}.",
       [(assign, "$temp", "itm_book_tactics"),
        (jump_to_menu, "mnu_camp_action_read_book_start"),
        ]
       ),
      ("action_read_book_2",[(player_has_item, "itm_book_persuasion"),
                             (item_slot_eq, "itm_book_persuasion", slot_item_book_read, 0),
                             (str_store_item_name, s1, "itm_book_persuasion"),
                             ],"{s1}.",
       [(assign, "$temp", "itm_book_persuasion"),
        (jump_to_menu, "mnu_camp_action_read_book_start"),
        ]
       ),
      ("action_read_book_3",[(player_has_item, "itm_book_leadership"),
                             (item_slot_eq, "itm_book_leadership", slot_item_book_read, 0),
                             (str_store_item_name, s1, "itm_book_leadership"),
                             ],"{s1}.",
       [(assign, "$temp", "itm_book_leadership"),
        (jump_to_menu, "mnu_camp_action_read_book_start"),
        ]
       ),
      ("action_read_book_4",[(player_has_item, "itm_book_intelligence"),
                             (item_slot_eq, "itm_book_intelligence", slot_item_book_read, 0),
                             (str_store_item_name, s1, "itm_book_intelligence"),
                             ],"{s1}.",
       [(assign, "$temp", "itm_book_intelligence"),
        (jump_to_menu, "mnu_camp_action_read_book_start"),
        ]
       ),
      ("action_read_book_5",[(player_has_item, "itm_book_trade"),
                             (item_slot_eq, "itm_book_trade", slot_item_book_read, 0),
                             (str_store_item_name, s1, "itm_book_trade"),
                             ],"{s1}.",
       [(assign, "$temp", "itm_book_trade"),
        (jump_to_menu, "mnu_camp_action_read_book_start"),
        ]
       ),
      ("action_read_book_6",[(player_has_item, "itm_book_weapon_mastery"),
                             (item_slot_eq, "itm_book_weapon_mastery", slot_item_book_read, 0),
                             (str_store_item_name, s1, "itm_book_weapon_mastery"),
                             ],"{s1}.",
       [(assign, "$temp", "itm_book_weapon_mastery"),
        (jump_to_menu, "mnu_camp_action_read_book_start"),
        ]
       ),
      ("action_read_book_7",[(player_has_item, "itm_book_engineering"),
                             (item_slot_eq, "itm_book_engineering", slot_item_book_read, 0),
                             (str_store_item_name, s1, "itm_book_engineering"),
                             ],"{s1}.",
       [(assign, "$temp", "itm_book_engineering"),
        (jump_to_menu, "mnu_camp_action_read_book_start"),
        ]
       ),
      ("camp_action_4",[],"Back to camp menu.",
       [(jump_to_menu, "mnu_camp"),
        ]
       ),
      ]
  ),
  ("camp_action_read_book_start",0,
   "{s1}",
   "none",
   [(assign, ":new_book", "$temp"),
    (str_store_item_name, s2, ":new_book"),
    (try_begin),
      (store_attribute_level, ":int", "trp_player", ca_intelligence),
      (item_get_slot, ":int_req", ":new_book", slot_item_intelligence_requirement),
      (le, ":int_req", ":int"),
      (str_store_string, s1, "@You start reading {s2}. After a few pages,\
 you feel you could learn a lot from this book. You decide to keep it close by and read whenever you have the time."),
      (assign, "$g_player_reading_book", ":new_book"),
    (else_try),
      (str_store_string, s1, "@You flip through the pages of {s2}, but you find the text confusing and difficult to follow.\
 Try as you might, it soon gives you a headache, and you're forced to give up the attempt."),
    (try_end),],
    [
      ("continue",[],"Continue...",
       [(jump_to_menu, "mnu_camp"),
        ]
       ),
      ]
  ),
]
