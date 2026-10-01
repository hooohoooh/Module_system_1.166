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

game_menus_village_quests = [
  #gekokujo 3.1 rebellions end
  
  #gekokujo 3.1 bogmir's quests start
  (
    "hidden_village",0,
    "You enter the Hidden Village",
    "none",
    [],
    [
      ("hidden_village_enter",[],"Enter.", [
          (set_jump_mission,"mt_town_default"),
          (jump_to_scene,"scn_bogmir_hidden_village"),
          (change_screen_mission)
        ], "Door to the village."),
        
      ("hidden_village_smithy",[],"Smithy.", [
	      (set_jump_mission,"mt_town_default"),
          (jump_to_scene,"scn_bogmir_hidden_village_smithy"),
          (change_screen_mission)
        ], "Door to the smithy."),
        
      ("hidden_village_wait_here",[],"Wait here for some time.", [
          (rest_for_hours_interactive, 24 * 7, 5, 0), #rest while not attackable
          (change_screen_return),
        ]),
        
      ("hidden_village_leave",[],"Leave.", [
          (leave_encounter),
          (change_screen_return)
        ]),
    ],
  ),
  (
    "village_hostile_action",0,
    "What action do you have in mind?",
    "none",
    [],
    [
      ("village_take_food",[
          (party_slot_eq, "$current_town", slot_village_state, 0),
          (neg|party_slot_ge, "$current_town", slot_village_infested_by_bandits, 1),
          (party_get_slot, ":merchant_troop", "$current_town", slot_town_elder),
          (assign, ":town_stores_not_empty", 0),
          (try_for_range, ":slot_no", num_equipment_kinds, max_inventory_items + num_equipment_kinds),
            (troop_get_inventory_slot, ":slot_item", ":merchant_troop", ":slot_no"),
            (ge, ":slot_item", 0),
            (assign, ":town_stores_not_empty", 1),
          (try_end),
          (eq, ":town_stores_not_empty", 1),
          ],"Force the peasants to give you supplies.",
       [
           (jump_to_menu, "mnu_village_take_food_confirm")
        ]),
      ("village_steal_cattle",
       [
          (party_slot_eq, "$current_town", slot_village_state, 0),
          (party_slot_eq, "$current_town", slot_village_player_can_not_steal_cattle, 0),
          (neg|party_slot_ge, "$current_town", slot_village_infested_by_bandits, 1),
          (party_get_slot, ":num_cattle", "$current_town", slot_village_number_of_cattle),
          (neg|party_slot_eq, "$current_town", slot_town_lord, "trp_player"),
          (gt, ":num_cattle", 0),
          ],"Steal cattle.",
       [
           (jump_to_menu, "mnu_village_steal_cattle_confirm")
        ]),
      ("village_loot",[(party_slot_eq, "$current_town", slot_village_state, 0),
                       (neg|party_slot_ge, "$current_town", slot_village_infested_by_bandits, 1),
                       (store_faction_of_party, ":center_faction", "$current_town"),
                       (store_relation, ":reln", "fac_player_supporters_faction", ":center_faction"),
                       (lt, ":reln", 0),
                       ],
       "Loot and burn this village.",
       [
#           (party_clear, "$current_town"),
#           (party_add_template, "$current_town", "pt_villagers_in_raid"),
           (jump_to_menu, "mnu_village_start_attack"),
           ]),
      ("forget_it",[],
      "Forget it.",[(jump_to_menu,"mnu_village")]),
    ],
  ),
  
  (
    "recruit_volunteers",0,
    "{s18}",
    "none",
    [(party_get_slot, ":volunteer_troop", "$current_town", slot_center_volunteer_troop_type),
     (party_get_slot, ":volunteer_amount", "$current_town", slot_center_volunteer_troop_amount),
     (party_get_free_companions_capacity, ":free_capacity", "p_main_party"),
     (store_troop_gold, ":gold", "trp_player"),

#     (store_div, ":gold_capacity", ":gold", 10),#10 mon per man
     (try_begin),
       (this_or_next|party_slot_eq, "$current_town", slot_party_type, spt_castle),
       (party_slot_eq, "$current_town", slot_party_type, spt_town),
       (store_div, ":gold_capacity", ":gold", 300),
     (else_try),
       (store_div, ":gold_capacity", ":gold", 10),
     (try_end),
	 
	 #gekokujo 3.0 ikko ikko recruitment start
	 #kanazawa, ishiyama, nagashima, and joguji all cost 10 because they have monk recruits
     #(try_begin),
	 #  (this_or_next|eq, "$current_town", "p_town_8"),
	 #  (this_or_next|eq, "$current_town", "p_castle_72"),
	 #  (this_or_next|eq, "$current_town", "p_castle_74"),
	 #  (eq, "$current_town", "p_castle_75"),
	 #  (store_div, ":gold_capacity", ":gold", 10),
     #(try_end),
	 #gekokujo 3.0 ikko ikko recruitment end

     (assign, ":party_capacity", ":free_capacity"),
     (val_min, ":party_capacity", ":gold_capacity"),
     (try_begin),
       (gt, ":party_capacity", 0),
	   #gekokujo 3.1 samurai party penalty start
	   #halve party capacity if samurai are being recruited
	   (try_begin),
	     (eq, "$g_gekokujo_samurai_penalty", 1),
         (this_or_next|party_slot_eq, "$current_town", slot_party_type, spt_castle),
         (party_slot_eq, "$current_town", slot_party_type, spt_town),
		 #(neq, "$current_town", "p_town_8"), #not kanazawa (monks)
	     #(neq, "$current_town", "p_castle_72"), #not nagashima fortress (monks)
	     #(neq, "$current_town", "p_castle_74"), #not ishiyama fortress (monks)
	     #(neq, "$current_town", "p_castle_75"), #not joguji fortress (monks)
		 
		 (val_div, ":party_capacity", 2),
	   (try_end),
	   #gekokujo 3.1 samurai party penalty end
       (val_min, ":volunteer_amount", ":party_capacity"),
     (try_end),
     (assign, reg5, ":volunteer_amount"),
     (assign, reg7, 0),
     (try_begin),
       (gt, ":volunteer_amount", ":gold_capacity"),
       (assign, reg7, 1), #not enough money
     (try_end),
     (try_begin),
       (eq, ":volunteer_amount", 0),
       (str_store_string, s18, "@No one here seems to be willing to join your party."),
     (else_try),

#       (store_mul, reg6, ":volunteer_amount", 10),#10 mon per man
        (try_begin),
          (this_or_next|party_slot_eq, "$current_town", slot_party_type, spt_castle),
          (party_slot_eq, "$current_town", slot_party_type, spt_town),
		  (try_begin),
		    #gekokujo 3.1 ikko samurai recruitment fix start
			#dangit i left in outdated code. it was still checking for culture rather than specific party
			#culture was used from 1.x and 2.x because ikko only had 2 troop trees rather than 3
			#now it should be by town so only kanazawa + the 3 fortresses have modified costs (10)
			#toyama castle (p_castle_14) is now treated normally again
			#(party_slot_eq, "$current_town", slot_center_culture, "fac_culture_20"),
			#(this_or_next|eq, "$current_town", "p_town_8"),
			#(this_or_next|eq, "$current_town", "p_castle_72"),
			#(this_or_next|eq, "$current_town", "p_castle_74"),
			#(eq, "$current_town", "p_castle_75"),
		    #gekokujo 3.1 ikko samurai recruitment fix end
			(store_mul, reg6, ":volunteer_amount", 10),
			(assign, reg8, 10), #gekokujo -- display cost when recruiting only a single monk
			(assign, reg9, 20), #gekokujo -- display cost when recruiting only two
			(assign, reg10, 30), #gekokujo -- display cost when recruiting only three
			(assign, reg11, 40), #gekokujo -- display cost when recruiting only four
			(assign, reg12, 50), #gekokujo -- display cost when recruiting only five
		  (else_try),
		    (store_mul, reg6, ":volunteer_amount", 300),
			(assign, reg8, 300), #gekokujo -- display cost when recruiting only a single ji-samurai
			(assign, reg9, 600), #gekokujo -- display cost when recruiting only two
			(assign, reg10, 900), #gekokujo -- display cost when recruiting only three
			(assign, reg11, 1200), #gekokujo -- display cost when recruiting only four
			(assign, reg12, 1500), #gekokujo -- display cost when recruiting only five
		  (try_end),
        (else_try),
          (store_mul, reg6, ":volunteer_amount", 10),
		  (assign, reg8, 10), #gekokujo -- display cost when recruiting only a single village recruit
		  (assign, reg9, 20), #gekokujo -- display cost when recruiting only two
		  (assign, reg10, 30), #gekokujo -- display cost when recruiting only three
		  (assign, reg11, 40), #gekokujo -- display cost when recruiting only four
		  (assign, reg12, 50), #gekokujo -- display cost when recruiting only five
        (try_end),

       (str_store_troop_name_by_count, s3, ":volunteer_troop", ":volunteer_amount"),
       (try_begin),
         (eq, reg5, 1),
         (str_store_string, s18, "@One {s3} volunteers to follow you."),
       (else_try),
         (str_store_string, s18, "@{reg5} {s3} volunteer to follow you."),
       (try_end),
	   #gekokujo new pic_recruits
       #(set_background_mesh, "mesh_pic_recruits"),
       (set_background_mesh, "mesh_gekokujo_pic_recruits"),
     (try_end),
    ],
    [
      ("continue_not_enough_gold",
      [
        (eq, reg7, 1),
      ],
      "I don't have enough money...",
      [
        (try_begin),
          (this_or_next|party_slot_eq, "$current_town", slot_party_type, spt_castle),
          (party_slot_eq, "$current_town", slot_party_type, spt_town),
          (jump_to_menu, "mnu_town"),
        (else_try),
          (jump_to_menu, "mnu_village"),
        (try_end),
      ]),
       
      ("continue",
      [
        (eq, reg7, 0),
        (eq, reg5, 0),
      ], #noone willing to join                   
      "Continue...",
      [
        (party_set_slot, "$current_town", slot_center_volunteer_troop_amount, -1),
        (try_begin),
          (this_or_next|party_slot_eq, "$current_town", slot_party_type, spt_castle),
          (party_slot_eq, "$current_town", slot_party_type, spt_town),
          (jump_to_menu, "mnu_town"),
        (else_try),
          (jump_to_menu, "mnu_village"),
        (try_end),
      ]),
       
	  ("recruit_one",
      [
        (eq, reg7, 0),
        (gt, reg5, 1),
        (store_troop_gold, ":gold", "trp_player"),
		(ge, ":gold", reg8),
      ],
      "Recruit one ({reg8} mon).",
      [
        (call_script, "script_gekokujo_recruit_volunteers_recruit", 1),
                        
        (try_begin),
          (this_or_next|party_slot_eq, "$current_town", slot_party_type, spt_castle),
          (party_slot_eq, "$current_town", slot_party_type, spt_town),
          (jump_to_menu, "mnu_town"),
        (else_try),
          (jump_to_menu, "mnu_village"),
        (try_end),
      ]),
	  
	  ("recruit_two",
      [
        (eq, reg7, 0),
        (gt, reg5, 2),
        (store_troop_gold, ":gold", "trp_player"),
		(ge, ":gold", reg9),
      ],	  
      "Recruit two ({reg9} mon).",
      [
        (call_script, "script_gekokujo_recruit_volunteers_recruit", 2),
                        
        (try_begin),
          (this_or_next|party_slot_eq, "$current_town", slot_party_type, spt_castle),
          (party_slot_eq, "$current_town", slot_party_type, spt_town),
          (jump_to_menu, "mnu_town"),
        (else_try),
          (jump_to_menu, "mnu_village"),
        (try_end),
      ]),
	  
	  ("recruit_three",
      [
        (eq, reg7, 0),
        (gt, reg5, 3),
        (store_troop_gold, ":gold", "trp_player"),
		(ge, ":gold", reg10),
      ],	  
      "Recruit three ({reg10} mon).",
      [
        (call_script, "script_gekokujo_recruit_volunteers_recruit", 3),
                        
        (try_begin),
          (this_or_next|party_slot_eq, "$current_town", slot_party_type, spt_castle),
          (party_slot_eq, "$current_town", slot_party_type, spt_town),
          (jump_to_menu, "mnu_town"),
        (else_try),
          (jump_to_menu, "mnu_village"),
        (try_end),
      ]),
	  
	  ("recruit_four",
      [
        (eq, reg7, 0),
        (gt, reg5, 4),
        (store_troop_gold, ":gold", "trp_player"),
		(ge, ":gold", reg11),
      ],	  
      "Recruit four ({reg11} mon).",
      [
        (call_script, "script_gekokujo_recruit_volunteers_recruit", 4),
                        
        (try_begin),
          (this_or_next|party_slot_eq, "$current_town", slot_party_type, spt_castle),
          (party_slot_eq, "$current_town", slot_party_type, spt_town),
          (jump_to_menu, "mnu_town"),
        (else_try),
          (jump_to_menu, "mnu_village"),
        (try_end),
      ]),
	  
	  ("recruit_five",
      [
        (eq, reg7, 0),
        (gt, reg5, 5),
        (store_troop_gold, ":gold", "trp_player"),
		(ge, ":gold", reg12),
      ],	  
      "Recruit five ({reg12} mon).",
      [
        (call_script, "script_gekokujo_recruit_volunteers_recruit", 5),
                        
        (try_begin),
          (this_or_next|party_slot_eq, "$current_town", slot_party_type, spt_castle),
          (party_slot_eq, "$current_town", slot_party_type, spt_town),
          (jump_to_menu, "mnu_town"),
        (else_try),
          (jump_to_menu, "mnu_village"),
        (try_end),
      ]),
	  
      ("recruit_them",
      [
        (eq, reg7, 0),
        (gt, reg5, 0),
      ],
      "Recruit them all ({reg6} mon).",
      [
        (call_script, "script_village_recruit_volunteers_recruit"),
                        
        (try_begin),
          (this_or_next|party_slot_eq, "$current_town", slot_party_type, spt_castle),
          (party_slot_eq, "$current_town", slot_party_type, spt_town),
          (jump_to_menu, "mnu_town"),
        (else_try),
          (jump_to_menu, "mnu_village"),
        (try_end),
      ]),
      
      ("forget_it",
      [
        (eq, reg7, 0),
        (gt, reg5, 0),
      ],
      "Forget it.",
      [
        (try_begin),
          (this_or_next|party_slot_eq, "$current_town", slot_party_type, spt_castle),
          (party_slot_eq, "$current_town", slot_party_type, spt_town),
          (jump_to_menu, "mnu_town"),
        (else_try),
          (jump_to_menu, "mnu_village"),
        (try_end),
      ]),
    ],
  ),
  (
    "village_hunt_down_fugitive_defeated",0,
    "A heavy blow from the fugitive sends you to the ground, and your vision spins and goes dark.\
 Time passes. When you open your eyes again you find yourself battered and bloody,\
 but luckily none of the wounds appear to be lethal.",
    "none",
    [],
    [
      ("continue",[],"Continue...",[(jump_to_menu, "mnu_village"),]),
    ],
  ),
  (
    "village_infest_bandits_result",mnf_scale_picture,
    "{s9}",
    "none",
    [(try_begin),
       (eq, "$g_battle_result", 1),
       (jump_to_menu, "mnu_village_infestation_removed"),
     (else_try),
       (str_store_string, s9, "@Try as you might, you could not defeat the bandits.\
 Infuriated, they raze the village to the ground to punish the peasants,\
 and then leave the burning wasteland behind to find greener pastures to plunder."),
       (set_background_mesh, "mesh_pic_looted_village"),
     (try_end),
    ],
    [
      ("continue",[],"Continue...",
       [(party_set_slot, "$g_encountered_party", slot_village_infested_by_bandits, 0),
        (call_script, "script_village_set_state",  "$current_town", svs_looted),
        (party_set_slot, "$current_town", slot_village_raid_progress, 0),
        (party_set_slot, "$current_town", slot_village_recover_progress, 0),
        (try_begin),
          (check_quest_active, "qst_eliminate_bandits_infesting_village"),
          (quest_slot_eq, "qst_eliminate_bandits_infesting_village", slot_quest_target_center, "$g_encountered_party"),
          (call_script, "script_change_player_relation_with_center", "$g_encountered_party", -5),
          (call_script, "script_fail_quest", "qst_eliminate_bandits_infesting_village"),
          (call_script, "script_end_quest", "qst_eliminate_bandits_infesting_village"),
        (else_try),
          (check_quest_active, "qst_deal_with_bandits_at_lords_village"),
          (quest_slot_eq, "qst_deal_with_bandits_at_lords_village", slot_quest_target_center, "$g_encountered_party"),
          (call_script, "script_change_player_relation_with_center", "$g_encountered_party", -4),
          (call_script, "script_fail_quest", "qst_deal_with_bandits_at_lords_village"),
          (call_script, "script_end_quest", "qst_deal_with_bandits_at_lords_village"),
        (else_try),
          (call_script, "script_change_player_relation_with_center", "$g_encountered_party", -3),
        (try_end),
        (jump_to_menu, "mnu_village"),]),
    ],
  ),
  (
    "village_infestation_removed",mnf_disable_all_keys,
    "In a battle worthy of song, you and your men drive the bandits out of the village, making it safe once more.\
 The villagers have little left in the way of wealth after their ordeal,\
 but they offer you all they can find.",
    "none",
    [(party_get_slot, ":bandit_troop", "$g_encountered_party", slot_village_infested_by_bandits),
     (party_set_slot, "$g_encountered_party", slot_village_infested_by_bandits, 0),
     (party_clear, "p_temp_party"),
     (party_add_members, "p_temp_party", ":bandit_troop", "$qst_eliminate_bandits_infesting_village_num_bandits"),
     (assign, "$g_strength_contribution_of_player", 50),
     (call_script, "script_party_give_xp_and_gold", "p_temp_party"),
     (try_begin),
       (check_quest_active, "qst_eliminate_bandits_infesting_village"),
       (quest_slot_eq, "qst_eliminate_bandits_infesting_village", slot_quest_target_center, "$g_encountered_party"),
       (call_script, "script_end_quest", "qst_eliminate_bandits_infesting_village"),
       #Add quest reward
       (call_script, "script_change_player_relation_with_center", "$g_encountered_party", 5),
     (else_try),
       (check_quest_active, "qst_deal_with_bandits_at_lords_village"),
       (quest_slot_eq, "qst_deal_with_bandits_at_lords_village", slot_quest_target_center, "$g_encountered_party"),
       (call_script, "script_succeed_quest", "qst_deal_with_bandits_at_lords_village"),
       (call_script, "script_change_player_relation_with_center", "$g_encountered_party", 3),
     (else_try),
     #Add normal reward
       (call_script, "script_change_player_relation_with_center", "$g_encountered_party", 4),
     (try_end),
   
     (party_get_slot, ":merchant_troop", "$current_town", slot_town_elder),
     (try_for_range, ":slot_no", num_equipment_kinds ,max_inventory_items + num_equipment_kinds),
        (store_random_in_range, ":rand", 0, 100),
        (lt, ":rand", 70),
        (troop_set_inventory_slot, ":merchant_troop", ":slot_no", -1),
     (try_end),
    ],
    [
      ("village_bandits_defeated_accept",[],"Take it as your just due.",[(jump_to_menu, "mnu_village"),
                                                                         (party_get_slot, ":merchant_troop", "$current_town", slot_town_elder),
                                                                         (troop_sort_inventory, ":merchant_troop"),
                                                                         (change_screen_loot, ":merchant_troop"),
                                                                       ]),
																	   
      ("village_bandits_defeated_cont",[],  "Refuse, stating that they need these items more than you do.",
	  [	(call_script, "script_change_player_relation_with_center", "$g_encountered_party", 3),
		(call_script, "script_change_player_honor", 1),	  
		(jump_to_menu, "mnu_village")]),
    ],
  ),
  
   (
    "village_steal_cattle_confirm",0,
    "As the party member with the highest looting skill ({reg2}), {reg3?you reckon:{s1} reckons} that you can steal as many as {reg4} heads of village's cattle.",
    "none",
    [
      (call_script, "script_get_max_skill_of_player_party", "skl_looting"),
      (assign, reg2, reg0),
      (assign, ":max_skill_owner", reg1),
      (try_begin),
        (eq, ":max_skill_owner", "trp_player"),
        (assign, reg3, 1),
      (else_try),
        (assign, reg3, 0),
        (str_store_troop_name, s1, ":max_skill_owner"),
      (try_end),
      (call_script, "script_calculate_amount_of_cattle_can_be_stolen", "$current_town"),
      (assign, reg4, reg0),
      ],
    [
      ("village_steal_cattle_confirm",[],"Go on.",
       [
         (rest_for_hours_interactive, 3, 5, 1), #rest while attackable
         (assign, "$auto_menu", "mnu_village_steal_cattle"),
         (change_screen_return),
       ]),
      ("forget_it",[],"Forget it.",[(change_screen_return)]),
    ],
  ),
  (
    "village_steal_cattle",mnf_disable_all_keys,
    "{s1}",
    "none",
    [
      (call_script, "script_calculate_amount_of_cattle_can_be_stolen", "$current_town"),
      (assign, ":max_value", reg0),
      (val_add, ":max_value", 1),
      (store_random_in_range, ":random_value", 0, ":max_value"),
      (party_set_slot, "$current_town", slot_village_player_can_not_steal_cattle, 1),
      (party_get_slot, ":lord", "$current_town", slot_town_lord),
      (try_begin),
        (le, ":random_value", 0),
        (call_script, "script_change_player_relation_with_center", "$current_town", -3),
        (str_store_string, s1, "@You fail to steal any cattle."),
      (else_try),
        (assign, reg17, ":random_value"),
        (store_sub, reg12, ":random_value", 1),
        (try_begin),
          (gt, ":lord", 0),
          (call_script, "script_change_player_relation_with_troop", ":lord", -3),
          (call_script, "script_add_log_entry", logent_player_stole_cattles_from_village, "trp_player",  "$current_town", ":lord", "$g_encountered_party_faction"),
        (try_end),
        (call_script, "script_change_player_relation_with_center", "$current_town", -5),
        (str_store_string, s1, "@You drive away {reg17} {reg12?heads:head} of cattle from the village's herd."),
        
        (try_begin),
          (eq, ":random_value", 3),
          (unlock_achievement, ACHIEVEMENT_GOT_MILK),
        (try_end),
        
        (call_script, "script_create_cattle_herd", "$current_town", ":random_value"),
        (party_get_slot, ":num_cattle", "$current_town", slot_village_number_of_cattle),
        (val_sub, ":num_cattle", ":random_value"),
        (party_set_slot, "$current_town", slot_village_number_of_cattle, ":num_cattle"),
      (try_end),
    ],
    [
      ("continue",[],"Continue...",
       [
         (change_screen_return),
         ]),
    ],
  ),
  

   (
    "village_take_food_confirm",0,
    "It will be difficult to force and threaten the peasants into giving their precious supplies. You think you will need at least one hour.",
    #TODO: mention looting skill?
    "none",
    [],
    [
      ("village_take_food_confirm",[],"Go ahead.",
       [
         (rest_for_hours_interactive, 1, 5, 0), #rest while not attackable
         (assign, "$auto_enter_town", "$current_town"),
         (assign, "$g_town_visit_after_rest", 1),
         (assign, "$auto_enter_menu_in_center", "mnu_village_take_food"),
         (change_screen_return),
         ]),
      ("forget_it",[],"Forget it.",[(jump_to_menu, "mnu_village_hostile_action")]),
    ],
  ),
  (
    "village_take_food",0,
    "The villagers grudgingly bring out what they have for you.",
    "none",
    [
       (call_script, "script_party_count_members_with_full_health","p_main_party"),
       (assign, ":player_party_size", reg0),
       (call_script, "script_party_count_members_with_full_health","$current_town"),
       (assign, ":villagers_party_size", reg0),
       (try_begin),
         (lt, ":player_party_size", 6),
         (ge, ":villagers_party_size", 40),
         (neg|party_slot_eq, "$current_town", slot_town_lord, "trp_player"),
         (jump_to_menu, "mnu_village_start_attack"),
       (try_end),
    ],
    [
      ("take_supplies",[],"Take the supplies.",
       [
         (try_begin),
           (party_slot_ge, "$current_town", slot_center_player_relation, -55),
           (try_begin),
             (party_slot_eq, "$current_town", slot_town_lord, "trp_player"),
             (call_script, "script_change_player_relation_with_center", "$current_town", -1),
           (else_try),
             (call_script, "script_change_player_relation_with_center", "$current_town", -3),
           (try_end),
         (try_end),
         (party_get_slot, ":village_lord", "$current_town", slot_town_lord),
         (try_begin),
           (gt,  ":village_lord", 1),
          (call_script, "script_change_player_relation_with_troop", ":village_lord", -1),
          (try_end),
         (party_get_slot, ":merchant_troop", "$current_town", slot_town_elder),
         (party_get_skill_level, ":player_party_looting", "p_main_party", "skl_looting"),
         (val_mul, ":player_party_looting", 3),
         (store_sub, ":random_chance", 70, ":player_party_looting"), #Increases the chance of looting by 3% per skill level
         (try_for_range, ":slot_no", num_equipment_kinds ,max_inventory_items + num_equipment_kinds),
           (store_random_in_range, ":rand", 0, 100), 
           (lt, ":rand", ":random_chance"),
           (troop_set_inventory_slot, ":merchant_troop", ":slot_no", -1),
         (try_end),

###NPC companion changes begin
         (call_script, "script_objectionable_action", tmt_humanitarian, "str_steal_from_villagers"),
#NPC companion changes end
#Troop commentary changes begin
          (call_script, "script_add_log_entry", logent_village_extorted, "trp_player",  "$current_town", -1, -1),
          (store_faction_of_party,":village_faction",  "$current_town"),
		  (call_script, "script_faction_inflict_war_damage_on_faction", "$players_kingdom", ":village_faction", 5),
#Troop commentary changes end          

         (jump_to_menu, "mnu_village"),
         (troop_sort_inventory, ":merchant_troop"),
         (change_screen_loot, ":merchant_troop"),       
         ]),
      ("let_them_keep_it",[],"Let them keep it.",[(jump_to_menu, "mnu_village")]),
    ],
  ),
  (
    "village_start_attack",mnf_disable_all_keys|mnf_scale_picture,
    "Some of the angry villagers grab their tools and prepare to resist you.\
 It looks like you'll have a fight on your hands if you continue.",
    "none",
    [
       (set_background_mesh, "mesh_pic_villageriot"),
       (call_script, "script_party_count_members_with_full_health","p_main_party"),
       (assign, ":player_party_size", reg0),
       (call_script, "script_party_count_members_with_full_health","$current_town"),
       (assign, ":villagers_party_size", reg0),
       
       (try_begin),
         (gt, ":player_party_size", 25),
         (jump_to_menu, "mnu_village_loot_no_resist"),
       (else_try),
         (this_or_next|eq, ":villagers_party_size", 0),
         (eq, "$g_battle_result", 1),
         (try_begin),
           (eq, "$g_battle_result", 1),
           (store_random_in_range, ":enmity", -30, -15),
           (call_script, "script_change_player_relation_with_center", "$current_town", ":enmity"),
           (party_get_slot, ":town_lord", "$current_town", slot_town_lord),
           (gt, ":town_lord", 0),
           (call_script, "script_change_player_relation_with_troop", ":town_lord", -3),
         (try_end),
         (jump_to_menu, "mnu_village_loot_no_resist"),
       (else_try),
         (eq, "$g_battle_result", -1),
         (jump_to_menu, "mnu_village_loot_defeat"),
       (try_end),
    ],
    [
      ("village_raid_attack",[],"Charge them.",[
          (store_random_in_range, ":enmity", -10, -5),
          (call_script, "script_change_player_relation_with_center", "$current_town", ":enmity"),
          (try_begin),
            (party_get_slot, ":town_lord", "$current_town", slot_town_lord),
            (gt, ":town_lord", 0),
            (call_script, "script_change_player_relation_with_troop", ":town_lord", -3),
          (try_end),
          (call_script, "script_calculate_battle_advantage"),
          (set_battle_advantage, reg0),
          (set_party_battle_mode),
          (assign, "$g_battle_result", 0),
          (assign, "$g_village_raid_evil", 1),
          (set_jump_mission,"mt_village_raid"),
          (party_get_slot, ":scene_to_use", "$current_town", slot_castle_exterior),
          (jump_to_scene, ":scene_to_use"),
          (assign, "$g_next_menu", "mnu_village_start_attack"),

		  (call_script, "script_diplomacy_party_attacks_neutral", "p_main_party", "$g_encountered_party"),
###NPC companion changes begin
          (call_script, "script_objectionable_action", tmt_humanitarian, "str_loot_village"),
#NPC companion changes end

          (jump_to_menu, "mnu_battle_debrief"),
          (change_screen_mission),
          ]),
      ("village_raid_leave",[],"Leave this village alone.",[(change_screen_return)]),
    ],
  ),
  
  (
    "village_loot_no_resist",0,
    "The villagers here are few and frightened, and they quickly scatter and run before you.\
 The village is at your mercy.",
    "none",
    [],
    [
      ("village_loot",[], "Plunder the village, then raze it.",
       [
          (call_script, "script_village_set_state", "$current_town", svs_being_raided),
          (party_set_slot, "$current_town", slot_village_raided_by, "p_main_party"),
          (assign,"$g_player_raiding_village","$current_town"),
		  
		  (try_begin),
		    (store_faction_of_party, ":village_faction", "$current_town"),
			(store_relation, ":relation", "$players_kingdom", ":village_faction"),
			(ge, ":relation", 0),
			(call_script, "script_diplomacy_party_attacks_neutral", "p_main_party", "$current_town"),
		  (try_end),	
		  
          (rest_for_hours, 3, 5, 1), #rest while attackable (3 hours will be extended by the trigger)
          (change_screen_return),
           ]),
      ("village_raid_leave",[],"Leave this village alone.",[(change_screen_return)]),
    ],
  ),
  (
    "village_loot_complete",mnf_disable_all_keys,
    "On your orders your troops sack the village, pillaging everything of any value,\
 and then put the buildings to the torch. From the coins and valuables that are found, you get your share of {reg1} mon.",
    "none",
    [
        (get_achievement_stat, ":number_of_village_raids", ACHIEVEMENT_THE_BANDIT, 0),
        (get_achievement_stat, ":number_of_caravan_raids", ACHIEVEMENT_THE_BANDIT, 1),
        (val_add, ":number_of_village_raids", 1),
        (set_achievement_stat, ACHIEVEMENT_THE_BANDIT, 0, ":number_of_village_raids"),
                
        (try_begin),
          (ge, ":number_of_village_raids", 3),
          (ge, ":number_of_caravan_raids", 3),
          (unlock_achievement, ACHIEVEMENT_THE_BANDIT),
        (try_end),
    
        (party_get_slot, ":village_lord", "$current_town", slot_town_lord),
        (try_begin),
          (gt,  ":village_lord", 0),
          (call_script, "script_change_player_relation_with_troop", ":village_lord", -5),
        (try_end),
        (store_random_in_range, ":enmity", -35, -25),
        (call_script, "script_change_player_relation_with_center", "$current_town", ":enmity"),

        (store_faction_of_party, ":village_faction", "$current_town"),
        (store_relation, ":relation", ":village_faction", "fac_player_supporters_faction"),
        (try_begin),
          (lt, ":relation", 0),
          (call_script, "script_change_player_relation_with_faction", ":village_faction", -3),
        (try_end),
                
        (assign, ":money_gained", 50),
        (party_get_slot, ":prosperity", "$current_town", slot_town_prosperity),
        (store_mul, ":prosperity_of_village_mul_5", ":prosperity", 5),
        (val_add, ":money_gained", ":prosperity_of_village_mul_5"),
        (call_script, "script_troop_add_gold", "trp_player", ":money_gained"),
		
        (assign, ":morale_increase", 3),
        (store_div, ":money_gained_div_100", ":money_gained", 100),
        (val_add, ":morale_increase", ":money_gained_div_100"),
        (call_script, "script_change_player_party_morale", ":morale_increase"),
        
                
        (faction_get_slot, ":faction_morale", ":village_faction",  slot_faction_morale_of_player_troops),
        (store_mul, ":morale_increase_mul_2", ":morale_increase", 200),
        (val_sub, ":faction_morale", ":morale_increase_mul_2"),           
        (faction_set_slot, ":village_faction",  slot_faction_morale_of_player_troops, ":faction_morale"),
        

		
#NPC companion changes begin
        (call_script, "script_objectionable_action", tmt_humanitarian, "str_loot_village"),
#NPC companion changes end
        (assign, reg1, ":money_gained"),
      ],
    [
      ("continue",[], "Continue...",
       [
          (jump_to_menu, "mnu_close"),
          (call_script, "script_calculate_amount_of_cattle_can_be_stolen", "$current_town"),
          (assign, ":max_cattle", reg0),
          (val_mul, ":max_cattle", 3),
          (val_div, ":max_cattle", 2),
          (party_get_slot, ":num_cattle", "$current_town", slot_village_number_of_cattle),
          (val_min, ":max_cattle", ":num_cattle"),
          (val_add, ":max_cattle", 1),
          (store_random_in_range, ":random_value", 0, ":max_cattle"),
          (try_begin),
            (gt, ":random_value", 0),
            (call_script, "script_create_cattle_herd", "$current_town", ":random_value"),
            (val_sub, ":num_cattle", ":random_value"),
            (party_set_slot, "$current_town", slot_village_number_of_cattle, ":num_cattle"),
          (try_end),
          (troop_clear_inventory, "trp_temp_troop"),

		  #below line changed with below lines to make plunder result more realistic. Now only items produced in bound town can be stolen after raid.
          #(reset_item_probabilities,100),

		  #begin of changes
		  (party_get_slot, ":bound_town", slot_village_bound_center, "$current_town"),
          (store_sub, ":item_to_price_slot", slot_town_trade_good_prices_begin, trade_goods_begin),
          (reset_item_probabilities,100),
          (assign, ":total_probability", 0),
          (try_for_range, ":cur_goods", trade_goods_begin, trade_goods_end),
            (store_add, ":cur_price_slot", ":cur_goods", ":item_to_price_slot"),
            (party_get_slot, ":cur_price", ":bound_town", ":cur_price_slot"),
            (call_script, "script_center_get_production", ":bound_town", ":cur_goods"),
            (assign, ":cur_probability", reg0),
            (call_script, "script_center_get_consumption", ":bound_town", ":cur_goods"),
            (val_div, reg0, 3),
            (val_add, ":cur_probability", reg0),
            (val_mul, ":cur_probability", 4),
            (val_mul, ":cur_probability", average_price_factor),
            (val_div, ":cur_probability", ":cur_price"),
			#first only simulation
            #(set_item_probability_in_merchandise,":cur_goods",":cur_probability"),						  
			(val_add, ":total_probability", ":cur_probability"),
          (try_end),

          (try_for_range, ":cur_goods", trade_goods_begin, trade_goods_end),
            (store_add, ":cur_price_slot", ":cur_goods", ":item_to_price_slot"),
            (party_get_slot, ":cur_price", ":bound_town", ":cur_price_slot"),
            (call_script, "script_center_get_production", ":bound_town", ":cur_goods"),
            (assign, ":cur_probability", reg0),
            (call_script, "script_center_get_consumption", ":bound_town", ":cur_goods"),
            (val_div, reg0, 3),
            (val_add, ":cur_probability", reg0),
            (val_mul, ":cur_probability", 4),
            (val_mul, ":cur_probability", average_price_factor),
            (val_div, ":cur_probability", ":cur_price"),

			(val_mul, ":cur_probability", num_merchandise_goods),
			(val_mul, ":cur_probability", 100),
			(val_div, ":cur_probability", ":total_probability"),

            (set_item_probability_in_merchandise,":cur_goods",":cur_probability"),						  
          (try_end),
		  #end of changes

          (troop_add_merchandise,"trp_temp_troop",itp_type_goods,30),
          (troop_sort_inventory, "trp_temp_troop"),
          (change_screen_loot, "trp_temp_troop"),
        ]),
    ],
  ),
  (
    "village_loot_defeat",mnf_scale_picture,
    "Fighting with courage and determination, the villagers manage to hold together and drive off your forces.",
    "none",
    [
        (set_background_mesh, "mesh_pic_villageriot"),
	],
    [
      ("continue",[],"Continue...",[(change_screen_return)]),
    ],
  ),
  
  (
    "village_loot_continue",0,
    "Do you wish to continue looting this village?",
    "none",
    [],
    [
      ("disembark_yes",[],"Yes.",[ (rest_for_hours, 3, 5, 1), #rest while attackable (3 hours will be extended by the trigger)
                              (change_screen_return),
                              ]),
      ("disembark_no",[],"No.",[(call_script, "script_village_set_state", "$current_town", 0),
                            (party_set_slot, "$current_town", slot_village_raided_by, -1),
                            (assign, "$g_player_raiding_village", 0),
                            (change_screen_return)]),
    ],
  ),
  (
    "collect_taxes",mnf_disable_all_keys,
    "As the party member with the highest trade skill ({reg2}), {reg3?you expect:{s1} expects} that collecting taxes from here will take {reg4} days...",
    "none",
    [(call_script, "script_get_max_skill_of_player_party", "skl_trade"),
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
     (assign, ":tax_quest_expected_revenue", 3000),
     (try_begin),
       (party_slot_eq, "$current_town", slot_party_type, spt_town),
       (assign, ":tax_quest_expected_revenue", 6000),
     (try_end),

     (try_begin),
       (quest_slot_eq, "qst_collect_taxes", slot_quest_current_state, 0),
       (store_add, ":max_skill_plus_thirty", ":max_skill", 30),
       (try_begin),
         (party_slot_eq, "$current_town", slot_party_type, spt_town),
         (store_div, "$qst_collect_taxes_total_hours", 24* 7 * 30, ":max_skill_plus_thirty"),
       (else_try),
         #Village
         (store_div, "$qst_collect_taxes_total_hours", 24 * 3 * 30, ":max_skill_plus_thirty"),
       (try_end),

       (call_script, "script_party_count_fit_for_battle", "p_main_party"),
       (val_add, reg0, 20),
       (val_mul, "$qst_collect_taxes_total_hours", 20),
       (val_div, "$qst_collect_taxes_total_hours", reg0),

     
       (quest_set_slot, "qst_collect_taxes", slot_quest_target_amount, "$qst_collect_taxes_total_hours"),
       (store_div, ":menu_begin_time", "$qst_collect_taxes_total_hours", 20),#between %5-%25
       (store_div, ":menu_end_time", "$qst_collect_taxes_total_hours", 4),
       (assign, ":unrest_begin_time", ":menu_end_time"),#between %25-%75
       (store_mul, ":unrest_end_time", "$qst_collect_taxes_total_hours", 3),
       (val_div, ":unrest_end_time", 4),

       (val_mul, ":tax_quest_expected_revenue", 2),
       (store_div, "$qst_collect_taxes_hourly_income", ":tax_quest_expected_revenue", "$qst_collect_taxes_total_hours"),
     
       (store_random_in_range, "$qst_collect_taxes_menu_counter", ":menu_begin_time", ":menu_end_time"),
       (store_random_in_range, "$qst_collect_taxes_unrest_counter", ":unrest_begin_time", ":unrest_end_time"),
       (assign, "$qst_collect_taxes_halve_taxes", 0),
     (try_end),
     (quest_get_slot, ":target_hours", "qst_collect_taxes", slot_quest_target_amount),
     (store_div, ":target_days", ":target_hours", 24),
     (val_mul, ":target_days", 24),
     (try_begin),
       (lt, ":target_days", ":target_hours"),
       (val_add, ":target_days", 24),
     (try_end),
     (val_div, ":target_days", 24),
     (assign, reg4, ":target_days"),
     ],
    [
      ("start_collecting", [], "Start collecting.",
       [(assign, "$qst_collect_taxes_currently_collecting", 1),
        (try_begin),
          (quest_slot_eq, "qst_collect_taxes", slot_quest_current_state, 0),
          (quest_set_slot, "qst_collect_taxes", slot_quest_current_state, 1),
        (try_end),
        (rest_for_hours_interactive, 1000, 5, 0), #rest while not attackable
        (assign,"$auto_enter_town","$current_town"),
        (assign, "$g_town_visit_after_rest", 1),
        (change_screen_return),
        ]),
      ("collect_later", [], "Put it off until later.",
       [(try_begin),
          (party_slot_eq, "$current_town", slot_party_type, spt_town),
          (jump_to_menu, "mnu_town"),
        (else_try),
          (jump_to_menu, "mnu_village"),
        (try_end),
        ]),
    ]
  ),
  (
    "collect_taxes_complete",mnf_disable_all_keys,
	##diplomacy start+
	##Replace "him" with "{reg4?her:him}"
    "You've collected {reg3} mon in taxes from {s3}. {s19} will be expecting you to take the money to {reg4?her:him}.",
	##diplomacy end+
    "none",
    [(str_store_party_name, s3, "$current_town"),
     (quest_get_slot, ":quest_giver", "qst_collect_taxes", slot_quest_giver_troop),
     (str_store_troop_name, s19, ":quest_giver"),
	 ##diplomacy start+
	 ##Store quest giver gender to reg4
	 (assign, reg4, 0),
	 (try_begin),
		(call_script, "script_cf_dplmc_troop_is_female", ":quest_giver"),
		(assign, reg4, 1),
	 (try_end),
	 ##diplomacy end+
     (quest_get_slot, reg3, "qst_collect_taxes", slot_quest_gold_reward),
     (try_begin),
       (eq, "$qst_collect_taxes_halve_taxes", 0),
       (call_script, "script_change_player_relation_with_center", "$current_town", -2),   
     (try_end),
     (call_script, "script_succeed_quest", "qst_collect_taxes"),
     ],
    [
      ("continue", [], "Continue...",
       [(change_screen_return),
        ]),
    ]
  ),
  (
    "collect_taxes_rebels_killed",0,
    "Your quick action and strong arm have successfully put down the revolt.\
 Surely, anyone with a mind to rebel against you will think better of it after this.",
    "none",
    [
    ],
    [
      ("continue", [], "Continue...",
       [(change_screen_map),
        ]),
    ]
  ),
  (
    "collect_taxes_failed",mnf_disable_all_keys,
##diplomacy start+ fix gender of pronoun
    "You could collect only {reg3} mon as tax from {s3} before the revolt broke out.\
 {s1} won't be happy, but some silver will placate {reg4?her:him} better than nothing at all...",
##diplomacy end+
    "none",
    [(str_store_party_name, s3, "$current_town"),
     (quest_get_slot, ":quest_giver", "qst_collect_taxes", slot_quest_giver_troop),
     ##diplomacy start+ store gender of quest giver in reg4
     (call_script, "script_dplmc_store_troop_is_female", ":quest_giver"),
     (assign, reg4, reg0),
     ##diplomacy end+
     (str_store_troop_name, s1, ":quest_giver"),
     (quest_get_slot, reg3, "qst_collect_taxes", slot_quest_gold_reward),
     (call_script, "script_fail_quest", "qst_collect_taxes"),
     (quest_set_slot, "qst_collect_taxes", slot_quest_current_state, 4),
     (rest_for_hours, 0, 0, 0), #stop resting
     ],
    [
      ("continue", [], "Continue...",
       [(change_screen_map),
        ]),
    ]
  ),
  (
    "collect_taxes_revolt_warning",0,
    "The people of {s3} are outraged at your demands and decry it as nothing more than extortion.\
 They're getting very restless, and they may react badly if you keep pressing them.",
    "none",
    [(str_store_party_name, s3, "$current_town"),
     ],
    [
      ("continue_collecting_taxes", [], "Ignore them and continue.",
       [(change_screen_return),]),
      ("halve_taxes", [(quest_get_slot, ":quest_giver_troop", "qst_collect_taxes", slot_quest_giver_troop),
                       (str_store_troop_name, s1, ":quest_giver_troop"),],
       "Agree to reduce your collection by half. ({s1} may be upset)",
       [(assign, "$qst_collect_taxes_halve_taxes", 1),
        (change_screen_return),
        ]),
    ]
  ),
  (
    "collect_taxes_revolt",0,
    "You are interrupted while collecting the taxes at {s3}. A large band of angry {reg9?peasants:townsmen} is marching nearer,\
 shouting about the exorbitant taxes and waving torches and weapons. It looks like they aim to fight you!",
    "none",
    [(str_store_party_name, s3, "$current_town"),
     (assign, reg9, 0),
     (try_begin),
       (party_slot_eq, "$current_town", slot_party_type, spt_village),
       (assign, reg9, 1),
     (try_end),
     ],
    [
      ("continue", [], "Continue...",
       [(set_jump_mission,"mt_back_alley_revolt"),
        (quest_get_slot, ":target_center", "qst_collect_taxes", slot_quest_target_center),
        (try_begin),
          (party_slot_eq, ":target_center", slot_party_type, spt_town),
          (party_get_slot, ":town_alley", ":target_center", slot_town_alley),
        (else_try),
          (party_get_slot, ":town_alley", ":target_center", slot_castle_exterior),
        (try_end),
        (modify_visitors_at_site,":town_alley"),
        (reset_visitors),
        (assign, ":num_rebels", 6),
        (store_character_level, ":level", "trp_player"),
        (val_div, ":level", 5),
        (val_add, ":num_rebels", ":level"),
        (set_visitors, 1, "trp_tax_rebel", ":num_rebels"),
        (jump_to_scene,":town_alley"),
        (change_screen_mission),
        ]),
    ]
  ),
 

  (
    "train_peasants_against_bandits_ready",0,
    "You put the peasants through the basics of soldiering, discipline and obedience.\
 You think {reg0} of them {reg1?have:has} fully grasped the training and {reg1?are:is} ready for some practice.",
    "none",
    [
      (store_character_level, ":level", "trp_player"),
      (val_div, ":level", 10),
      (val_add, ":level", 1),
      (quest_get_slot, ":quest_target_amount", "qst_train_peasants_against_bandits", slot_quest_target_amount),
      (quest_get_slot, ":quest_current_state", "qst_train_peasants_against_bandits", slot_quest_current_state),
      (val_sub, ":quest_target_amount", ":quest_current_state"),
      (assign, ":max_random", ":level"),
      (val_min, ":max_random", ":quest_target_amount"),
      (val_add, ":max_random", 1),
      (store_random_in_range, ":random_number", 1, ":max_random"),
      (assign, "$g_train_peasants_against_bandits_num_peasants", ":random_number"),
      (assign, reg0, ":random_number"),
      (store_sub, reg1, ":random_number", 1),
      (str_store_troop_name_by_count, s0, "trp_trainee_peasant", ":random_number"),
     ],
    [
      ("peasant_start_practice", [], "Start the practice fight.",
       [
         (set_jump_mission,"mt_village_training"),
         (quest_get_slot, ":target_center", "qst_train_peasants_against_bandits", slot_quest_target_center),
         (party_get_slot, ":village_scene", ":target_center", slot_castle_exterior),
         (modify_visitors_at_site, ":village_scene"),
         (reset_visitors),
         (set_visitor, 0, "trp_player"),
         (set_visitors, 1, "trp_trainee_peasant", "$g_train_peasants_against_bandits_num_peasants"),
         (set_jump_entry, 11),
         (jump_to_scene, ":village_scene"),
         (jump_to_menu, "mnu_train_peasants_against_bandits_training_result"),
         (music_set_situation, 0),
         (change_screen_mission),
         ]),
      ]
    ),
  (
    "train_peasants_against_bandits_training_result",mnf_disable_all_keys,
    "{s0}",
    "none",
    [
      (assign, reg5, "$g_train_peasants_against_bandits_num_peasants"),
      (str_store_troop_name_by_count, s0, "trp_trainee_peasant", "$g_train_peasants_against_bandits_num_peasants"),
      (try_begin),
        (eq, "$g_train_peasants_against_bandits_training_succeeded", 0),
        (str_store_string, s0, "@You were beaten. The peasants are heartened by their success, but the lesson you wanted to teach them probably didn't get through..."),
      (else_try),
        (str_store_string, s0, "@After beating your last opponent, you explain to the peasants how to better defend themselves against such an attack. Hopefully they'll take the experience on board and will be prepared next time."),
        (quest_get_slot, ":quest_current_state", "qst_train_peasants_against_bandits", slot_quest_current_state),
        (val_add, ":quest_current_state", "$g_train_peasants_against_bandits_num_peasants"),
        (quest_set_slot, "qst_train_peasants_against_bandits", slot_quest_current_state, ":quest_current_state"),
      (try_end),
     ],
    [
      ("continue", [], "Continue...",
       [
         (try_begin),
           (quest_get_slot, ":quest_current_state", "qst_train_peasants_against_bandits", slot_quest_current_state),
           (quest_slot_eq, "qst_train_peasants_against_bandits", slot_quest_target_amount, ":quest_current_state"),
           (jump_to_menu, "mnu_train_peasants_against_bandits_attack"),
         (else_try),
           (change_screen_map),
         (try_end),
         ]),
      ]
    ),
  (
    "train_peasants_against_bandits_attack",0,
    "As you get ready to continue the training, a sentry from the village runs up to you, shouting alarums.\
 The bandits have been spotted on the horizon, riding hard for {s3}.\
 The elder begs that you organize your newly-trained militia and face them.",
    "none",
    [
	(str_store_party_name, s3, "$current_town"),
     ],
    [
      ("peasants_against_bandits_attack_resist", [], "Prepare for a fight!",
       [
        (store_random_in_range, ":random_no", 0, 3),
        (try_begin),
          (eq, ":random_no", 0),
          (assign, ":bandit_troop", "trp_bandit"),
        (else_try),
          (eq, ":random_no", 1),
          (assign, ":bandit_troop", "trp_woku_pirate"),
        (else_try),
          (assign, ":bandit_troop", "trp_shinano_rebel"),
        (try_end),
        (party_get_slot, ":scene_to_use", "$g_encountered_party", slot_castle_exterior),
        (modify_visitors_at_site, ":scene_to_use"),
        (reset_visitors),
        (store_character_level, ":level", "trp_player"),
        (val_div, ":level", 2),
        (store_add, ":min_bandits", ":level", 16),
        (store_add, ":max_bandits", ":min_bandits", 6),
        (store_random_in_range, ":random_no", ":min_bandits", ":max_bandits"),
        (set_visitors, 0, ":bandit_troop", ":random_no"),
        (assign, ":num_villagers", ":max_bandits"),
        (set_visitors, 2, "trp_trainee_peasant", ":num_villagers"),
        (set_party_battle_mode),
        (set_battle_advantage, 0),
        (assign, "$g_battle_result", 0),
        (set_jump_mission,"mt_village_attack_bandits"),
        (jump_to_scene, ":scene_to_use"),
        (assign, "$g_next_menu", "mnu_train_peasants_against_bandits_attack_result"),
        (jump_to_menu, "mnu_battle_debrief"),
        (assign, "$g_mt_mode", vba_after_training),
        (change_screen_mission),
        ]),
      ]
    ),
  (
    "train_peasants_against_bandits_attack_result",mnf_scale_picture|mnf_disable_all_keys,
    "{s9}",
    "none",
    [
      (try_begin),
        (eq, "$g_battle_result", 1),
        (str_store_string, s9, "@The bandits are broken!\
 Those few who remain alive and conscious run off with their tails between their legs,\
 terrified of the peasants and their new champion."),
	(call_script, "script_succeed_quest", "qst_train_peasants_against_bandits"),
        (jump_to_menu, "mnu_train_peasants_against_bandits_success"),
      (else_try),
        (call_script, "script_fail_quest", "qst_train_peasants_against_bandits"),
        (str_store_string, s9, "@Try as you might, you could not defeat the bandits.\
 Infuriated, they raze the village to the ground to punish the peasants,\
 and then leave the burning wasteland behind to find greener pastures to plunder."),
        (set_background_mesh, "mesh_pic_looted_village"),
      (try_end),
     ],
    [
      ("continue", [], "Continue...",
       [(try_begin),
          (call_script, "script_village_set_state",  "$current_town", svs_looted),
          (party_set_slot, "$current_town", slot_village_raid_progress, 0),
          (party_set_slot, "$current_town", slot_village_recover_progress, 0),
          (call_script, "script_change_player_relation_with_center", "$g_encountered_party", -3),
          (call_script, "script_end_quest", "qst_train_peasants_against_bandits"),
        (try_end),
        (change_screen_map),
	 ]),
      ]
    ),
   (
    "train_peasants_against_bandits_success",mnf_disable_all_keys,
    "The bandits are broken!\
 Those few who remain run off with their tails between their legs,\
 terrified of the peasants and their new champion.\
 The villagers have little left in the way of wealth after their ordeal,\
 but they offer you all they can find to show their gratitude.",
    "none",
    [(party_clear, "p_temp_party"),
     (call_script, "script_end_quest", "qst_train_peasants_against_bandits"),
     (call_script, "script_change_player_relation_with_center", "$g_encountered_party", 4),

     (party_get_slot, ":merchant_troop", "$current_town", slot_town_elder),
     (try_for_range, ":slot_no", num_equipment_kinds ,max_inventory_items + num_equipment_kinds),
        (store_random_in_range, ":rand", 0, 100),
        (lt, ":rand", 50),
        (troop_set_inventory_slot, ":merchant_troop", ":slot_no", -1),
     (try_end),
     (call_script, "script_add_log_entry", logent_helped_peasants, "trp_player",  "$current_town", -1, -1),
    ],
    [
      ("village_bandits_defeated_accept",[],"Take it as your just due.",[(jump_to_menu, "mnu_auto_return_to_map"),
                                                                         (party_get_slot, ":merchant_troop", "$current_town", slot_town_elder),
                                                                         (troop_sort_inventory, ":merchant_troop"),
                                                                         (change_screen_loot, ":merchant_troop"),
                                                                       ]),
      ("village_bandits_defeated_cont",[],  "Refuse, stating that they need these items more than you do.",[
	  (call_script, "script_change_player_relation_with_center", "$g_encountered_party", 3),
      (call_script, "script_change_player_honor", 1),
      (change_screen_map)]),
    ],
  ),
  (
    "enemy_offer_ransom_for_prisoner",0,
##diplomacy start+ Since s2 is the name of a kingdom rather than a person, change "sell him" to "sell them"
    "{s2} offers you a sum of {reg12} mon in silver if you are willing to sell them {s1}.",
##diplomacy end+
    "none",
    [(call_script, "script_calculate_ransom_amount_for_troop", "$g_ransom_offer_troop"),
     (assign, reg12, reg0),
     (str_store_troop_name, s1, "$g_ransom_offer_troop"),
     (store_troop_faction, ":faction_no", "$g_ransom_offer_troop"),
     (str_store_faction_name, s2, ":faction_no"),
     ],
    [
      ("ransom_accept",[],"Accept the offer.",
       [ ##diplomacy begin
        (try_begin),
          (gt, "$g_player_chamberlain", 0),
          (call_script, "script_dplmc_pay_into_treasury", reg12),
        (else_try),
        ##diplomacy end
		  (troop_add_gold, "trp_player", reg12),
        ##diplomacy begin
        (try_end),
        ##diplomacy end
		##diplomacy start+
		#The enemy actually loses the gold paid.
		(assign, ":gold_paid", reg12),
		(assign, ":lord_who_pays", "$g_ransom_offer_troop"),
		(store_troop_faction, ":faction_no", "$g_ransom_offer_troop"),
		#For kingdom ladies, someone else might pay.
		(try_begin),
			(is_between, "$g_ransom_offer_troop", kingdom_ladies_begin, kingdom_ladies_end),
			(neg|troop_slot_eq, "$g_ransom_offer_troop", slot_troop_occupation, slto_kingdom_hero),#I think at this step even for heroes it's 0
			(neg|troop_slot_ge, "$g_ransom_offer_troop", slot_troop_wealth, 1),
			(try_begin),
				#Check spouse pays
				(troop_get_slot, ":lord", "$g_ransom_offer_troop", slot_troop_spouse),
				(this_or_next|is_between, ":lord", active_npcs_begin, active_npcs_end),
					(troop_slot_eq, ":lord", slot_troop_occupation, slto_kingdom_hero),
				(store_troop_faction, ":lord_faction", ":lord"),
				(eq, ":faction_no", ":lord_faction"),
				(neg|troop_slot_ge, ":lord", slot_troop_occupation, slto_retirement),
				(assign, ":lord_who_pays", ":lord"),
			(else_try),
				#Check father pays
				(troop_get_slot, ":lord", "$g_ransom_offer_troop", slot_troop_father),
				(this_or_next|is_between, ":lord", active_npcs_begin, active_npcs_end),
					(troop_slot_eq, ":lord", slot_troop_occupation, slto_kingdom_hero),
				(store_troop_faction, ":lord_faction", ":lord"),
				(eq, ":faction_no", ":lord_faction"),
				(neg|troop_slot_ge, ":lord", slot_troop_occupation, slto_retirement),
				(assign, ":lord_who_pays", ":lord"),
			(else_try),
				#Check guardian pays
				(troop_get_slot, ":lord", "$g_ransom_offer_troop", slot_troop_guardian),
				(this_or_next|is_between, ":lord", active_npcs_begin, active_npcs_end),
					(troop_slot_eq, ":lord", slot_troop_occupation, slto_kingdom_hero),
				(store_troop_faction, ":lord_faction", ":lord"),
				(eq, ":faction_no", ":lord_faction"),
				(neg|troop_slot_ge, ":lord", slot_troop_occupation, slto_retirement),
				(assign, ":lord_who_pays", ":lord"),
			(else_try),
				#Check mother pays
				(troop_get_slot, ":lord", "$g_ransom_offer_troop", slot_troop_mother),
				(this_or_next|is_between, ":lord", active_npcs_begin, active_npcs_end),
					(troop_slot_eq, ":lord", slot_troop_occupation, slto_kingdom_hero),
				(store_troop_faction, ":lord_faction", ":lord"),
				(eq, ":faction_no", ":lord_faction"),
				(neg|troop_slot_ge, ":lord", slot_troop_occupation, slto_retirement),
				(assign, ":lord_who_pays", ":lord"),
			(try_end),
		(try_end),
		(try_begin),
			(ge, ":gold_paid", 0),
			(ge, ":lord_who_pays", 1),
			(troop_is_hero, ":lord_who_pays"),
			#Remove the gold.  The lady has her own funds (e.g. from her dower)
			#that will partially defray the expense to the lord, depending on
			#the campaign difficulty.
		    (game_get_reduce_campaign_ai, ":reduce_campaign_ai"),
		    (try_begin),
			   (eq, ":reduce_campaign_ai", 0), #hard: lord pays 50%, lady's resources pay for 50%
			   (val_div, ":gold_paid", 2),
		    (else_try),
			   (eq, ":reduce_campaign_ai", 1), #medium: lord pays 75%, lady's resources pay for 25%
			   (val_mul, ":gold_paid", 3),
			   (val_div, ":gold_paid", 4),
		    (try_end),#easy: lord pays 100%, lady pays nothing
			(call_script, "script_dplmc_remove_gold_from_lord_and_holdings", ":gold_paid", ":lord_who_pays"),
		(try_end),
		##diplomacy end+
        (party_remove_prisoners, "$g_ransom_offer_party", "$g_ransom_offer_troop", 1),
        #(troop_set_slot, "$g_ransom_offer_troop", slot_troop_is_prisoner, 0),
        (call_script, "script_remove_troop_from_prison", "$g_ransom_offer_troop"),

        (try_begin),
            (troop_get_type, ":is_female", "trp_player"),
            (eq, ":is_female", 1),

            (get_achievement_stat, ":number_of_lords_sold", ACHIEVEMENT_MAN_HANDLER, 1),
            (val_add, ":number_of_lords_sold", 1),
            (set_achievement_stat, ACHIEVEMENT_MAN_HANDLER, 1, ":number_of_lords_sold"),

            (eq, ":number_of_lords_sold", 3),
            (unlock_achievement, ACHIEVEMENT_MAN_HANDLER),
        (try_end),

        (change_screen_return),
        ]),
      ("ransom_reject",[],"Reject the offer.",
       [
	    ##diplomacy start+
		#Relation loss altered by lord personality type.
		#OLD:
        #(call_script, "script_change_player_relation_with_troop", "$g_ransom_offer_troop", -4),
		#NEW:
		(try_begin),
			(troop_slot_eq, "$g_ransom_offer_troop", slot_lord_reputation_type, lrep_quarrelsome),
			(call_script, "script_change_player_relation_with_troop", "$g_ransom_offer_troop", -6),
		(else_try),
			(troop_slot_eq, "$g_ransom_offer_troop", slot_lord_reputation_type, lrep_debauched),
			(call_script, "script_change_player_relation_with_troop", "$g_ransom_offer_troop", -5),
		(else_try),
			(call_script, "script_change_player_relation_with_troop", "$g_ransom_offer_troop", -4),
		(try_end),
		##diplomacy end+
        (call_script, "script_change_player_honor", -1),
        (assign, "$g_ransom_offer_rejected", 1),
		##diplomacy start+
		#TODO: Review this, it was partway through a redesign when I stopped.
		#Also apply a negative reaction modifier to other lords
		(assign, ":save_reg0", reg0),

		(store_faction_of_troop, ":captive_faction", "$g_ransom_offer_troop"),
		#For kingdom ladies:
		(try_begin),
			(is_between, "$g_ransom_offer_troop", kingdom_ladies_begin, kingdom_ladies_end),
			#(troop_slot_eq, "$g_ransom_offer_troop", slot_troop_occupation, slto_kingdom_lady),
			(call_script, "script_get_kingdom_lady_social_determinants", "$g_talk_troop"),
			(assign, ":guardian", reg0),
			(store_faction_of_troop, ":captive_faction", ":guardian"),

			(try_for_range, ":troop_no", heroes_begin, heroes_end),
				(troop_slot_ge, ":troop_no", slot_troop_occupation, slto_kingdom_hero),#lowest valid
				(neg|troop_slot_ge, ":troop_no", slot_troop_occupation, slto_inactive_pretender),#end of valid range
				(neq, "$g_ransom_offer_troop", ":troop_no"),
				(store_faction_of_troop, ":troop_faction", ":troop_no"),

				(assign, ":disapproval_threshold", 20),
				(try_begin),
					(neq, ":troop_faction", ":captive_faction"),
					(neg|is_between, ":troop_no", kingdom_ladies_begin, kingdom_ladies_end),
					(assign, ":disapproval_threshold", 40),
				(try_end),
				#(this_or_next|is_between, ":troop_no", kingdom_ladies_begin, kingdom_ladies_end),
				#	(eq, ":troop_faction", ":captive_faction"),
				(assign, ":relation_change", 0),

				#family
				(try_begin),
					(this_or_next|troop_slot_eq, ":troop_no", slot_troop_spouse, "$g_ransom_offer_troop"),
					(this_or_next|troop_slot_eq, "$g_ransom_offer_troop", slot_troop_spouse, ":troop_no"),
					(eq, ":guardian", ":troop_no"),
					(assign, ":relation_change", -4),
				(else_try),
					(eq, ":troop_no", slot_troop_betrothed, "$g_ransom_offer_troop"),
					(assign, ":relation_change", -4),
				(else_try),
					(call_script, "script_troop_get_family_relation_to_troop", "$g_ransom_offer_troop", ":troop_no"),
					(ge, reg0, 14),
					(assign, ":relation_change", -3),
				(else_try),
					(ge, reg0, 10),
					(assign, ":relation_change", -2),
				(else_try),
					(ge, reg0, 2),
					(assign, ":relation_change", -1),
				(else_try),
					(call_script, "script_troop_get_relation_with_troop", ":troop_no", "$g_ransom_offer_troop"),
					(ge, reg0, ":disapproval_threshold"),
					(this_or_next|is_between, ":troop_no", kingdom_ladies_begin, kingdom_ladies_end),
						(eq, ":troop_faction", ":captive_faction"),
					(assign, ":relation_change", -1),
				(else_try),
					(ge, ":guardian", 1),
					(call_script, "script_troop_get_relation_with_troop", ":troop_no", ":guardian"),
					(ge, reg0, ":disapproval_threshold"),
					(assign, ":relation_change", -1),
				(try_end),

				(lt, ":relation_change", 0),
				(try_begin),
					(troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_quarrelsome),
					(val_mul, ":relation_change", 3),#-1 to -2, -2 to -3, -3 to -5, -4 to -6
					(val_sub, ":relation_change", 1),
					(val_div, ":relation_change", 2),
				(try_end),
				(call_script, "script_change_player_relation_with_troop", ":troop_no", ":relation_change"),
			(try_end),
		(else_try),
		#For others:
			(is_between, "$g_ransom_offer_troop", active_npcs_begin, active_npcs_end),
			(try_for_range, ":hero", heroes_begin, heroes_end),
				(this_or_next|is_between, ":hero", active_npcs_begin, active_npcs_end),
					(troop_slot_eq, ":hero", slot_troop_occupation, slto_kingdom_hero),
				(neg|troop_slot_eq, ":hero", slot_troop_occupation, dplmc_slto_dead),
				(neg|troop_slot_ge, ":hero", slot_troop_occupation, slto_retirement),

				(neq, ":hero", "$g_ransom_offer_troop"),

				(store_faction_of_troop, ":troop_faction", ":hero"),

				(assign, ":relation_change", 0),

				(call_script, "script_troop_get_family_relation_to_troop", "$g_ransom_offer_troop", ":hero"),
				(try_begin),
					(ge, reg0, 10),
					(assign, ":relation_change", -1),
				(try_end),

				(call_script, "script_troop_get_relation_with_troop", ":hero", "$g_ransom_offer_troop"),
				(try_begin),
					(ge, reg0, 20),
					(eq, ":troop_faction", ":captive_faction"),
					(val_sub, ":relation_change", 1),
				(else_try),
					(ge, reg0, 40),
					(val_sub, ":relation_change", 1),
				(else_try),
					(lt, reg0, 0),
					(assign, ":relation_change", 0),
				(try_end),

				(lt, ":relation_change", 0),
				(try_begin),
					(troop_slot_eq, ":hero", slot_lord_reputation_type, lrep_quarrelsome),
					(val_mul, ":relation_change", 3),#-1 to -2, -2 to -3, -3 to -5, -4 to -6
					(val_sub, ":relation_change", 1),
					(val_div, ":relation_change", 2),
				(try_end),
				(call_script, "script_change_player_relation_with_troop", ":hero", ":relation_change"),
			(try_end),

			(try_for_range, ":lady", kingdom_ladies_begin, kingdom_ladies_end),
				(neg|troop_slot_eq, ":lady", slot_troop_occupation, slto_kingdom_hero),
				(neg|troop_slot_eq, ":lady", slot_troop_occupation, dplmc_slto_dead),
				(neg|troop_slot_ge, ":lady", slot_troop_occupation, slto_retirement),

				(neq, ":lady", "$g_ransom_offer_troop"),

				(assign, ":relation_change", 0),
				(call_script, "script_troop_get_family_relation_to_troop", ":lady", "$g_ransom_offer_troop"),
				(try_begin),
					(ge, reg0, 14),
					(assign, ":relation_change", -3),
				(else_try),
					(ge, reg0, 10),
					(assign, ":relation_change", -2),
				(else_try),
					(ge, reg0, 2),
					(assign, ":relation_change", -1),
				(else_try),
					(call_script, "script_troop_get_relation_with_troop", ":lady", "$g_ransom_offer_troop"),
					(ge, reg0, 20),
					(assign, ":relation_change", -1),
				(try_end),

				(lt, ":relation_change", 0),
				(call_script, "script_change_player_relation_with_troop", ":lady", ":relation_change"),
			(try_end),
		(try_end),

		(assign, reg0, ":save_reg0"),
		##diplomacy end+
        (change_screen_return),
        ]),
    ]
  ),
  (
##diplomacy end+ fix gender of pronoun
    "kingdom_army_quest_report_to_army",mnf_scale_picture,
    "{s8} sends word that {reg4?she:he} wishes you to join {reg4?her:his} new military campaign.\
 You need to bring at least {reg13} troops to the army,\
 and are instructed to raise more men with all due haste if you do not have enough.",
##diplomacy end+
    "none",
    [
        (set_background_mesh, "mesh_pic_messenger"),
        (quest_get_slot, ":quest_target_troop", "qst_report_to_army", slot_quest_target_troop),
        (quest_get_slot, ":quest_target_amount", "qst_report_to_army", slot_quest_target_amount),
        (call_script, "script_get_information_about_troops_position", ":quest_target_troop", 0),
        (str_clear, s9),
        (try_begin),
          (eq, reg0, 1), #troop is found and text is correct
          (str_store_string, s9, s1),
        (try_end),
        (str_store_troop_name, s8, ":quest_target_troop"),
        (assign, reg13, ":quest_target_amount"),
		##diplomacy start+
        #Set gender with script
		#(troop_get_type, reg4, ":quest_target_troop"), #<- OLD
		(call_script, "script_dplmc_store_troop_is_female_reg", ":quest_target_troop", 4),
		##diplomacy end+
      ],
    [
      ("continue",[],"Continue...",
       [
           (quest_get_slot, ":quest_target_troop", "qst_report_to_army", slot_quest_target_troop),
           (quest_get_slot, ":quest_target_amount", "qst_report_to_army", slot_quest_target_amount),
           (str_store_troop_name_link, s13, ":quest_target_troop"),
           (assign, reg13, ":quest_target_amount"),
           (setup_quest_text, "qst_report_to_army"),
           ##diplomacy start+ fix gender of pronoun
           (str_store_string, s2, "@{s13} asked you to report to {reg4?her:him} with at least {reg13} troops."),
           ##diplomacy end+
           (call_script, "script_start_quest", "qst_report_to_army", ":quest_target_troop"),
           (call_script, "script_report_quest_troop_positions", "qst_report_to_army", ":quest_target_troop", 3),
           (change_screen_return),
        ]),
     ]
  ),
  (
##diplomacy start+ fix gender of pronouns
    "kingdom_army_quest_messenger",mnf_scale_picture,
    "{s8} sends word that {reg4?she:he} wishes to speak with you about a task {reg4?she:he} needs performed.\
 {reg4?She:He} requests you to come and see him as soon as possible.",
##diplomacy end+
    "none",
    [
        (set_background_mesh, "mesh_pic_messenger"),
        (faction_get_slot, ":faction_marshall", "$players_kingdom", slot_faction_marshall),
        ##diplomacy start+ put marshall's gender in reg4
        (call_script, "script_dplmc_store_troop_is_female", ":faction_marshall"),
        (assign, reg4, reg0),
        ##diplomacy end+
        (str_store_troop_name, s8, ":faction_marshall"),
      ],
    [
      ("continue",[],"Continue...",
       [(change_screen_return),
        ]),
     ]
  ),
  (
    "kingdom_army_quest_join_siege_order",mnf_scale_picture,
    "{s8} sends word that you are to join the siege of {s9} in preparation for a full assault.\
 Your troops are to take {s9} at all costs.",
    "none",
    [
		(set_background_mesh, "mesh_pic_messenger"),
        (faction_get_slot, ":faction_marshall", "$players_kingdom", slot_faction_marshall),
        (quest_get_slot, ":quest_target_center", "qst_join_siege_with_army", slot_quest_target_center),
        (str_store_troop_name, s8, ":faction_marshall"),
        (str_store_party_name, s9, ":quest_target_center"),
      ],
    [
      ("continue",[],"Continue...",
       [
           (call_script, "script_end_quest", "qst_follow_army"),
           (quest_get_slot, ":quest_target_center", "qst_join_siege_with_army", slot_quest_target_center),
           (faction_get_slot, ":faction_marshall", "$players_kingdom", slot_faction_marshall),
           (str_store_troop_name_link, s13, ":faction_marshall"),
           (str_store_party_name_link, s14, ":quest_target_center"),
           (setup_quest_text, "qst_join_siege_with_army"),
           (str_store_string, s2, "@{s13} ordered you to join the assault against {s14}."),
           (call_script, "script_start_quest", "qst_join_siege_with_army", ":faction_marshall"),
           (change_screen_return),
        ]),
     ]
  ),
  (
    "kingdom_army_follow_failed",mnf_scale_picture,
    "You have failed to follow {s8}. The strategist assumes that you were otherwise engaged, but would have appreciated your support.",
    "none",
    [
        (set_background_mesh, "mesh_pic_messenger"),
        (faction_get_slot, ":faction_marshall", "$players_kingdom", slot_faction_marshall),
        (str_store_troop_name, s8, ":faction_marshall"),
        (call_script, "script_abort_quest", "qst_follow_army", 1),
#        (call_script, "script_change_player_relation_with_troop", ":faction_marshall", -3),
      ],
    [
      ("continue",[],"Continue...",
       [(change_screen_return),
        ]),
     ]
  ),
  
  
    (
    "kill_local_merchant_begin",0,
    "You spot your victim and follow him, observing as he turns a corner into a dark alley.\
 This will surely be your best opportunity to attack him.",
    "none",
    [
    ],
    [
      ("continue",[],"Continue...",
       [(set_jump_mission,"mt_back_alley_kill_local_merchant"),
        (party_get_slot, ":town_alley", "$qst_kill_local_merchant_center", slot_town_alley),
        (modify_visitors_at_site,":town_alley"),
        (reset_visitors),
        (set_visitor, 0, "trp_player"),
        (set_visitor, 1, "trp_local_merchant"),
        (jump_to_menu, "mnu_town"),
        (jump_to_scene,":town_alley"),
        (change_screen_mission),
        ]),
     ]
  ),
    (
    "bandit_lair",0,
    "{s3}",
    "none",
    [
      (try_begin),
        (eq, "$loot_screen_shown", 1),
		
        (try_for_range, ":bandit_template", "pt_seto_pirates", "pt_deserters"),
          (party_template_slot_eq, ":bandit_template", slot_party_template_lair_party, "$g_encountered_party"),
          (party_template_set_slot, ":bandit_template", slot_party_template_lair_party, 0),
        (try_end),
        
        (try_begin),
          (ge, "$g_encountered_party", 0),
          (party_is_active, "$g_encountered_party"),
          (party_get_template_id, ":template", "$g_encountered_party"),	    
	      (neq, ":template", "pt_looter_lair"),
          (remove_party, "$g_encountered_party"),
        (try_end),  
		
        (assign, "$g_leave_encounter", 0),
        (change_screen_return),
		
      (else_try),        
        (party_stack_get_troop_id, ":bandit_type", "$g_encountered_party", 0),
        (str_store_troop_name_plural, s4, ":bandit_type"),
        (str_store_string, s5, "str_bandit_approach_defile"),
		
        (try_begin),
          (eq, ":bandit_type", "trp_northern_raider"),
          (str_store_string, s5, "str_bandit_approach_defile"),
        (else_try),
          (eq, ":bandit_type", "trp_woku_pirate"),
          (str_store_string, s5, "str_bandit_approach_cliffs"),
        (else_try),
          (eq, ":bandit_type", "trp_shinano_rebel"),
          (str_store_string, s5, "str_bandit_approach_swamp"),
        (else_try),
          (eq, ":bandit_type", "trp_kanto_rebel"),
          (str_store_string, s5, "str_bandit_approach_swamp"),
        (else_try),
          (eq, ":bandit_type", "trp_seto_pirate"),
          (str_store_string, s5, "str_bandit_approach_thickets"),
        (else_try),
          (eq, ":bandit_type", "trp_kinai_rebel"),
          (str_store_string, s5, "str_bandit_approach_cove"),
		#gekokujo 3.0 new bandit types start
        (else_try),
          (eq, ":bandit_type", "trp_monk_rebel"),
          (str_store_string, s5, "str_bandit_approach_cove"),
		#gekokujo 3.0 new bandit types end
        (try_end),
      
        (try_begin),
          (party_slot_eq, "$g_encountered_party", slot_party_ai_substate, 0), #used in place of global variable
          (str_store_string, s3, "str_bandit_hideout_preattack"),
        (else_try),
          (party_get_template_id, ":template", "$g_encountered_party"),	    
	      (eq, ":template", "pt_looter_lair"),
          (party_slot_eq, "$g_encountered_party", slot_party_ai_substate, 1), #used in place of global variable
          (str_store_string, s3, "str_lost_startup_hideout_attack"),
		(else_try),
          (party_slot_eq, "$g_encountered_party", slot_party_ai_substate, 1), #used in place of global variable
          (str_store_string, s3, "str_bandit_hideout_failure"),
        (else_try),
          (party_slot_eq, "$g_encountered_party", slot_party_ai_substate, 2), #used in place of global variable
          (str_store_string, s3, "str_bandit_hideout_success"),
        (try_end),	
      (try_end),      
    ],
    [
      ("continue_1",
      [
        (party_slot_eq, "$g_encountered_party", slot_party_ai_substate, 0), #used in place of global variable
	  ],
	  "Attack the hideout...",
	  
	  [
	    (party_set_slot, "$g_encountered_party", slot_party_ai_substate, 1),
	    (party_get_template_id, ":template", "$g_encountered_party"),
	    (assign, "$g_enemy_party", "$g_encountered_party"),
	    	    
	    (try_begin),
	      (eq, ":template", "pt_kinai_rebel_lair"),
	      (assign, ":bandit_troop", "trp_kinai_rebel"),
	      (assign, ":bandit_troop_2", "trp_kinai_rebel"),
	      (assign, ":scene_to_use", "scn_lair_kinai_rebels"),
	    (else_try),	
	      (eq, ":template", "pt_shinano_rebel_lair"),
	      (assign, ":bandit_troop", "trp_shinano_rebel"),
	      (assign, ":bandit_troop_2", "trp_shinano_rebel"),
	      (assign, ":scene_to_use", "scn_lair_shinano_rebels"),
	    (else_try),
	      (eq, ":template", "pt_northern_raider_lair"),
	      (assign, ":bandit_troop", "trp_northern_raider"),
	      (assign, ":bandit_troop_2", "trp_northern_raider"),
	      (assign, ":scene_to_use", "scn_lair_northern_raiders"),
	    (else_try),
	      (eq, ":template", "pt_woku_pirate_lair"),
	      (assign, ":bandit_troop", "trp_woku_pirate"),
	      (assign, ":bandit_troop_2", "trp_woku_pirate"),
	      (assign, ":scene_to_use", "scn_lair_woku_pirates"),
	    (else_try),
	      (eq, ":template", "pt_kanto_rebel_lair"),
	      (assign, ":bandit_troop", "trp_kanto_rebel"),
	      (assign, ":bandit_troop_2", "trp_kanto_rebel"),
	      (assign, ":scene_to_use", "scn_lair_kanto_rebels"),
	    (else_try),
	      (eq, ":template", "pt_seto_pirate_lair"),
	      (assign, ":bandit_troop", "trp_seto_pirate"),
	      (assign, ":bandit_troop_2", "trp_seto_pirate"),
	      (assign, ":scene_to_use", "scn_lair_seto_pirates"),
		#gekokujo 3.0 new bandit types start
	    (else_try),
	      (eq, ":template", "pt_monk_rebel_lair"),
	      (assign, ":bandit_troop", "trp_monk_rebel"),
	      (assign, ":bandit_troop_2", "trp_monk_rebel"),
	      (assign, ":scene_to_use", "scn_lair_monk_rebels"),
		#gekokujo 3.0 new bandit types end
	    (else_try),
	      (eq, ":template", "pt_looter_lair"),
	      (assign, ":bandit_troop", "trp_generic_ashigaru"),
	      (assign, ":bandit_troop_2", "trp_generic_jizamurai"), #gekokujo 3.0 enable enemy samurai in mansion raid
	      (assign, ":scene_to_use", "scn_lair_mansion"),	   
	      
		  ##gekokujo 3.0 starting quest placeholder (change scene)
	      #(store_faction_of_party, ":starting_town_faction", "$g_starting_town"),
		  #(try_begin),
	      #  (eq, ":starting_town_faction", "fac_kingdom_11"), #player selected asakura city (tsu) as starting town.
	      #  (assign, ":scene_to_use", "scn_lair_shinano_rebels"),	    
	      #(else_try),
	      #  (eq, ":starting_town_faction", "fac_kingdom_10"), #player selected nanbu city (hirosaki) as starting town.
	      #  (assign, ":scene_to_use", "scn_lair_kanto_rebels"),	    
	      #(else_try),
	      #  (eq, ":starting_town_faction", "fac_kingdom_1"), #player selected uesugi city (niigata) as starting town.
	      #  (assign, ":scene_to_use", "scn_lair_seto_pirates"),	    
	      #(else_try),
	      #  (eq, ":starting_town_faction", "fac_kingdom_13"), #player selected hojo city (edo) as starting town.
	      #  (assign, ":scene_to_use", "scn_lair_kinai_rebels"),
	      #(else_try),
	      #  (eq, ":starting_town_faction", "fac_kingdom_7"), #player selected miyoshi city (osaka) as starting town.
	      #  (assign, ":scene_to_use", "scn_lair_woku_pirates"),
	      #(else_try),
	      #  (eq, ":starting_town_faction", "fac_kingdom_9"), #player selected otomo city (hakata) as starting town.
	      #  (assign, ":scene_to_use", "scn_lair_northern_raiders"),	    
	      #(try_end),  
	    (try_end),
	    
	    (modify_visitors_at_site,":scene_to_use"),
	    (reset_visitors),	    

        (store_character_level, ":player_level", "trp_player"),                   
        (store_add, ":number_of_bandits_will_be_spawned_at_each_period", 5, ":player_level"),
        (val_div, ":number_of_bandits_will_be_spawned_at_each_period", 3),
	    
	    (try_for_range, ":unused", 0, ":number_of_bandits_will_be_spawned_at_each_period"),
	      (store_random_in_range, ":random_entry_point", 2, 11),	      
		  #gekokujo 3.0 enable enemy samurai in mansion raid start
		  #we added a bandit_troop_2 variable and initialized it in all bandit lair types
		  #but it only matters for looters aka the opening quest
		  #this is also applied in the mission template reinforcement triggers
	      #(set_visitor, ":random_entry_point", ":bandit_troop", 1),	   
		  (store_random_in_range, ":random_bandit_type", 0, 6), #roll 1 to 6
		  (try_begin),
		    (eq, ":random_bandit_type", 0), #roll of 1 (so 1/6 chance)
			(set_visitor, ":random_entry_point", ":bandit_troop_2", 1),
		  (else_try),
	        (set_visitor, ":random_entry_point", ":bandit_troop", 1),
		  (try_end),
		  #gekokujo 3.0 enable enemy samurai in mansion raid end
	    (try_end),
	    
	    (party_clear, "p_temp_casualties"),
	    
	    (set_party_battle_mode),
        (set_battle_advantage, 0),
        (assign, "$g_battle_result", 0),
        (set_jump_mission,"mt_bandit_lair"),
        
        (jump_to_scene, ":scene_to_use"),        
        (change_screen_mission),        
	  ]),
		
      ("leave_no_attack",
      [
	    (party_slot_eq, "$g_encountered_party", slot_party_ai_substate, 0),
	  ],
	  "Leave...",
      [
        (change_screen_return),
      ]),            
		
	  ("leave_victory",
	  [
	    (party_slot_eq, "$g_encountered_party", slot_party_ai_substate, 2),
	  ],
	  "Continue...",
      [      
        (try_for_range, ":bandit_template", "pt_seto_pirates", "pt_deserters"),
          (party_template_slot_eq, ":bandit_template", slot_party_template_lair_party, "$g_encountered_party"),
          (party_template_set_slot, ":bandit_template", slot_party_template_lair_party, 0),
        (try_end),
         
        (party_get_template_id, ":template", "$g_encountered_party"),
        (try_begin),
          (neq, ":template", "pt_looter_lair"),
          (check_quest_active, "qst_destroy_bandit_lair"),
          (quest_slot_eq, "qst_destroy_bandit_lair", slot_quest_target_party, "$g_encountered_party"),
          (call_script, "script_succeed_quest", "qst_destroy_bandit_lair"),
        (try_end),
                 
        (assign, "$g_leave_encounter", 0),
        (change_screen_return),

        (try_begin),
          (eq, "$loot_screen_shown", 0),
          (assign, "$loot_screen_shown", 1),
#gekokujo 3.0 integrating 1.158 start
#          (try_begin),
#            (gt, "$g_ally_party", 0),
#            (call_script, "script_party_add_party", "$g_ally_party", "p_temp_party"), #Add remaining prisoners to ally TODO: FIX it.
#          (else_try),
#            (party_get_num_attached_parties, ":num_quick_attachments", "p_main_party"),
#            (gt, ":num_quick_attachments", 0),
#            (party_get_attached_party_with_rank, ":helper_party", "p_main_party", 0),
#            (call_script, "script_party_add_party", ":helper_party", "p_temp_party"), #Add remaining prisoners to our reinforcements
#          (try_end),
#gekokujo 3.0 integrating 1.158 end
          (troop_clear_inventory, "trp_temp_troop"),
          
          (party_get_num_companion_stacks, ":num_stacks", "p_temp_casualties"), 
          (try_for_range, ":stack_no", 0, ":num_stacks"),
            (party_stack_get_troop_id, ":stack_troop", "p_temp_casualties", ":stack_no"), 
            (try_begin),              
              (party_stack_get_size, ":stack_size", "p_temp_casualties", ":stack_no"),
              (party_stack_get_troop_id, ":stack_troop", "p_temp_casualties", ":stack_no"),
              (gt, ":stack_size", 0),              
              (party_add_members, "p_total_enemy_casualties", ":stack_troop", ":stack_size"), #addition_to_p_total_enemy_casualties
              (party_stack_get_num_wounded, ":stack_wounded_size", "p_temp_casualties", ":stack_no"),
              (gt, ":stack_wounded_size", 0),
              (party_wound_members, "p_total_enemy_casualties", ":stack_troop", ":stack_wounded_size"),
            (try_end),
          (try_end),
                    
          (call_script, "script_party_calculate_loot", "p_total_enemy_casualties"), #p_encountered_party_backup changed to total_enemy_casualties          
          (gt, reg0, 0),          
          (troop_sort_inventory, "trp_temp_troop"),
		  ##diplomacy start+
		  ##OLD:
          #(change_screen_loot, "trp_temp_troop"),
		  ##NEW:
		  ##jump to rubik's CC autoloot
		  (try_begin),
			(call_script, "script_party_calculate_loot", "p_total_enemy_casualties"),
			(assign, "$dplmc_return_menu", "mnu_bandit_lair"),
            (jump_to_menu, "mnu_dplmc_manage_loot_pool"),
		  (else_try),
		     #Fall back to old behavior
			(change_screen_loot, "trp_temp_troop"),
		  (try_end),
		  ##diplomacy end+
        (try_end),
        
        (try_begin),
          (ge, "$g_encountered_party", 0),
          (party_is_active, "$g_encountered_party"),
          (party_get_template_id, ":template", "$g_encountered_party"),	    
	      (eq, ":template", "pt_looter_lair"),
          (remove_party, "$g_encountered_party"),
        (try_end),          
      ]),
		
	  ("leave_defeat",
	  [
	    (party_slot_eq, "$g_encountered_party", slot_party_ai_substate, 1),
	  ],
	  "Continue...",
      [
        (try_for_range, ":bandit_template", "pt_seto_pirates", "pt_deserters"),
          (party_template_slot_eq, ":bandit_template", slot_party_template_lair_party, "$g_encountered_party"),
          (party_template_set_slot, ":bandit_template", slot_party_template_lair_party, 0),
        (try_end),
        
        (try_begin),
          (party_get_template_id, ":template", "$g_encountered_party"),
          (neq, ":template", "pt_looter_lair"),
          (check_quest_active, "qst_destroy_bandit_lair"),
          (quest_slot_eq, "qst_destroy_bandit_lair", slot_quest_target_party, "$g_encountered_party"),
          (call_script, "script_fail_quest", "qst_destroy_bandit_lair"),
        (try_end),
        
        (try_begin),
          (ge, "$g_encountered_party", 0),
          (party_is_active, "$g_encountered_party"),
          (party_get_template_id, ":template", "$g_encountered_party"),	    
	      (neq, ":template", "pt_looter_lair"),
          (remove_party, "$g_encountered_party"),
        (try_end),  

        (assign, "$g_leave_encounter", 0),
        
		(try_begin),
			(party_is_active, "$g_encountered_party"),
			(party_set_slot, "$g_encountered_party", slot_party_ai_substate, 0),
        (try_end),
		
        (change_screen_return),
        ]),
		
     ]
  ),
]
