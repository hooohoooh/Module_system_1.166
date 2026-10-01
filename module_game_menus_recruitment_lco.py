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

game_menus_recruitment_lco = [
  
  ("zhaobing",mnf_disable_all_keys,
    "欢 迎 来 到 招 募 界 面",
    "none",   
    [(eq, "$current_town", "p_town_1", "p_town_5", "p_town_4", "p_town_10", "p_town_21"),],
    [
     ("buy_cannon",[
		(store_troop_gold,":gold","trp_player"),
		(party_get_slot,":num_cannons","p_main_party",slot_party_cannons),
		(try_begin),
			(ge,":gold",15000),
			(lt,":num_cannons",10),
		(else_try),
			(disable_menu_option),
		(try_end),
	 ],"购 买 一 门 火 炮 ，花 费 一 万 五 （ 炮 兵 随 炮 自 动 配 备 ）",
       [
		(troop_remove_gold,"trp_player",15000),
		(party_get_slot,":num_cannons","p_main_party",slot_party_cannons),
		(val_add,":num_cannons",1),
		(party_set_slot,"p_main_party",slot_party_cannons,":num_cannons"),
		(assign,reg0,":num_cannons"),
		(display_message,"@你购买了一门火炮，当前共有{reg0}门火炮。"),
       ]),

     ("view_cannon_info",[],
       "查 看 当 前 火 炮 数 量",
       [
		(party_get_slot,":num_cannons","p_main_party",slot_party_cannons),
		(assign,reg0,":num_cannons"),
		(display_message,"@当前火炮：{reg0}门。"),
       ]),
       
     ("go_back",[],"Go back",
       [
        (jump_to_menu, "mnu_town"),
       ]),
    ]
  ),
  
  ("zhaobing2",mnf_disable_all_keys,
    "民 主 人 士，欢 迎 来 到 招 募 界 面",
    "none",   
    [],
    [
     ("buy_munitions1",[
		(store_free_inventory_capacity,":num","trp_player"),
		(store_troop_gold,":gold","trp_player"),
		(try_begin),
			(ge,":num",1),
			(ge,":gold",30),
		(else_try),
			(disable_menu_option),
		(try_end),
	 ],"购 买 一 个 共 和 国 卫 队 ，花 费 三 十 ",
       [
		(troop_remove_gold,"trp_player",30),
		(party_add_members, "p_main_party", "trp_republic_citizen", 1),
       ]),
       
     ("buy_munitions2",[
		(store_free_inventory_capacity,":num","trp_player"),
		(store_troop_gold,":gold","trp_player"),
		(try_begin),
			(ge,":num",1),
			(ge,":gold",300),
		(else_try),
			(disable_menu_option),
		(try_end),
	 ],"购 买 十 个 共 和 国 卫 队 ，花 费 三 百",
       [
		(troop_remove_gold,"trp_player",301),
		(party_add_members, "p_main_party", "trp_republic_citizen", 10),
       ]),
       
     ("buy_munitions3",[
		(store_free_inventory_capacity,":num","trp_player"),
		(store_troop_gold,":gold","trp_player"),
		(try_begin),
			(ge,":num",1),
			(ge,":gold",3000),
		(else_try),
			(disable_menu_option),
		(try_end),
	 ],"购 买 一百 个 共 和 国 卫 队 ，花 费 三 千",
       [
		(troop_remove_gold,"trp_player",3000),
		(party_add_members, "p_main_party", "trp_republic_citizen", 100),
       ]),
     ("go_back",[],"Go back",
       [
        (jump_to_menu, "mnu_town"),
       ]),
    ]

  ),
  ("zhaobing3",mnf_disable_all_keys,
    "倒 幕 志 士，欢 迎 来 到 招 募 界 面",
    "none",   
    [],
    [
     ("buy_munitions4",[
		(store_free_inventory_capacity,":num","trp_player"),
		(store_troop_gold,":gold","trp_player"),
		(try_begin),
			(ge,":num",1),
			(ge,":gold",100),
		(else_try),
			(disable_menu_option),
		(try_end),
	 ],"招 募 一 个 倒 幕 志 士 ，花 费 一 百",
       [
		(troop_remove_gold,"trp_player",100),
		(party_add_members, "p_main_party", "trp_zunwangzhishi", 1),
       ]),
       
     ("buy_munitions5",[
		(store_free_inventory_capacity,":num","trp_player"),
		(store_troop_gold,":gold","trp_player"),
		(try_begin),
			(ge,":num",1),
			(ge,":gold",1000),
		(else_try),
			(disable_menu_option),
		(try_end),
	 ],"招 募 十 个 倒 幕 志 士 ，花 费 一 千",
       [
		(troop_remove_gold,"trp_player",1001),
		(party_add_members, "p_main_party", "trp_zunwangzhishi", 10),
       ]),
       
     ("buy_munitions6",[
		(store_free_inventory_capacity,":num","trp_player"),
		(store_troop_gold,":gold","trp_player"),
		(try_begin),
			(ge,":num",1),
			(ge,":gold",10000),
		(else_try),
			(disable_menu_option),
		(try_end),
	 ],"招 募 一 百 个 倒 幕 志 士 ，花 费 一 万",
       [
		(troop_remove_gold,"trp_player",10000),
		(party_add_members, "p_main_party", "trp_zunwangzhishi", 100),
       ]),
     ("go_back",[],"Go back",
       [
        (jump_to_menu, "mnu_town"),
       ]),
    ]
    ),
    
    ("zhaobing4",mnf_disable_all_keys,
    "佐 幕 志 士，欢 迎 来 到 招 募 界 面",
    "none",   
    [],
    [
     ("buy_munitions6",[
		(store_free_inventory_capacity,":num","trp_player"),
		(store_troop_gold,":gold","trp_player"),
		(try_begin),
			(ge,":num",1),
			(ge,":gold",100),
		(else_try),
			(disable_menu_option),
		(try_end),
	 ],"招 募 一 个 佐 幕 志 士 ，花 费 一 百",
       [
		(troop_remove_gold,"trp_player",100),
		(party_add_members, "p_main_party", "trp_zuomuzhishi", 1),
       ]),
       
     ("buy_munitions6",[
		(store_free_inventory_capacity,":num","trp_player"),
		(store_troop_gold,":gold","trp_player"),
		(try_begin),
			(ge,":num",1),
			(ge,":gold",1000),
		(else_try),
			(disable_menu_option),
		(try_end),
	 ],"招 募 十 个 佐 幕 志 士 ，花 费 一 千",
       [
		(troop_remove_gold,"trp_player",1001),
		(party_add_members, "p_main_party", "trp_zuomuzhishi", 10),
       ]),
       
     ("buy_munitions6",[
		(store_free_inventory_capacity,":num","trp_player"),
		(store_troop_gold,":gold","trp_player"),
		(try_begin),
			(ge,":num",1),
			(ge,":gold",10000),
		(else_try),
			(disable_menu_option),
		(try_end),
	 ],"招 募 一 百 个 佐 幕 志 士 ，花 费 一 万",
       [
		(troop_remove_gold,"trp_player",10000),
		(party_add_members, "p_main_party", "trp_zuomuzhishi", 100),
       ]),
     ("go_back",[],"Go back",
       [
        (jump_to_menu, "mnu_town"),
       ]),
    ]
    ),
  
  ## Tocan Invasion+ ##
  (
    "dk_invasion_start_warning",mnf_scale_picture,
    "A frightened and exhausted messenger boy rides up to you, his face red and hair soaked with sweat. '{s1}!' he cries, running up to you. 'Wait, you must hear me out!'^^\
\
After catching his breath, the messenger hands you a slip of paper. 'War has come! Conquerors from another land have stepped on Japan ground, bent on domination! Escape, \
{s1}, while you still can! I have seen them myself, their armor as black as night, their eyes cold as steel!'^^\
\
With that, the boy rides off, shouting to any who will listen.",
    "none",
    [
		(set_background_mesh, "mesh_rus_army"),
                (try_begin),
                   (troop_get_type, ":is_female", "trp_player"),
                   (eq, ":is_female", 1),
                   (str_store_string, s1, "@Milady"), 
                (else_try),
                   (str_store_string, s1, "@Milord"),
                (try_end),
   ],
    [
		("continue",[],"Continue...",
			[
			(change_screen_return),
			],
		),
	]
),
  ("set_invasion",0,
   "Are the Great Ming army (Dark Knights) allowed to invade?^This feature is on a early development stage and not really tested. If you play a good save make please a copy of them before you let them invade!^The Diplomacy option 'terrain advantage in Autocalc battles' will be disabled.^^Currently, they {s1}",
   "none",
   [
     (try_begin),
       (eq,"$setting_invasion_time",0),
       (str_store_string,s1,"@are not allowed to invade."),
     (else_try),
       (ge,"$setting_invasion_time",1),
       (str_store_string,s1,"@are set to invade at an unknown date."),
     #(else_try),
     #  (eq,"$setting_invasion_time",1200),
     #  (str_store_string,s1,"@50 days after start"),
     #(else_try),
     #  (eq,"$setting_invasion_time",1800),
     #  (str_store_string,s1,"@75 days after start"),
     #(else_try),
     #  (eq,"$setting_invasion_time",2400),
     #  (str_store_string,s1,"@100 days after start"),
     #(else_try),
     #  (eq,"$setting_invasion_time",3600),
     #  (str_store_string,s1,"@150 days after start"),
     #(else_try),
     #  (eq,"$setting_invasion_time",4800),
     #  (str_store_string,s1,"@200 days after start"),
     #(else_try),
     #  (str_store_string,s1,"@ERROR - NOT SET - BAD SAVE?"),
     #(try_end),
     (try_begin),
       (gt,"$invaded",0),
       (str_store_string,s1,"@have already invaded."),
     (try_end),
     ],
    [
      ("never",[(eq, "$invaded", 0)],"Never let them invade.",
       [(assign,"$setting_invasion_time",0),
        (display_message,"@The the Great Ming army will never invade."),
        (jump_to_menu, "mnu_dplmc_preferences"),
       ]),
      ("now",[],"Immediately.",
       [(assign,"$setting_invasion_time",1),
        (display_message,"@The the Great Ming army will shortly begin their invasion."),
        (jump_to_menu, "mnu_dplmc_preferences"),
       ]),
      ("unknown",[],"An unknown date in the future.",
       [(store_random_in_range, "$setting_invasion_time", 1, 4800),
        (display_message,"@The the Great Ming army will invade sometime in the future."),
        (jump_to_menu, "mnu_dplmc_preferences"),
       ]),
      ("return",[],"Leave the setting as it is.",
       [
        (jump_to_menu, "mnu_dplmc_preferences"),
       ]),
   ]),
     
## Tocan- ##  

##diplomacy end+

####################################################################################################################
# LAV MODIFICATIONS START (COMPANIONS OVERSEER MOD)

    ("lco_presentation",0,"Hidden Text","none",
        [
            (jump_to_menu, "mnu_lco_presentation"), # Self-reference
            (try_begin),
                (eq, "$g_lco_page", 2),
                (start_presentation, "prsnt_equipment_overview"),
            (else_try),
                (start_presentation, "prsnt_companions_overview"),
            (try_end),
        ],
        [("lco_go_back",[],"{!}Return",[])]
    ),
    ("lco_view_character",0,"Hidden Text","none",
        [
            (assign, "$g_lco_operation", 0),  # Reset operation flag before conversation
            (modify_visitors_at_site,"scn_conversation_scene"),
            (reset_visitors),
            (set_visitor,0,"trp_player"),
            (set_visitor,17,"$g_lco_target"),
            (set_jump_mission,"mt_conversation_encounter"),
            (jump_to_scene,"scn_conversation_scene"),
            (change_screen_map_conversation, "$g_lco_target"),
        ],
        [("lco_go_back",[],"{!}Return",[])]
    ),
    ("lco_auto_return",0,"Hidden Text","none",
        [
            (try_begin),
                (gt, "$g_lco_auto_menu", 0),
                (jump_to_menu, "$g_lco_auto_menu"),
                (assign, "$g_lco_auto_menu", 0),
            (else_try),
                (change_screen_return),
            (try_end),
        ],
        [("lco_go_back",[],"{!}Return",[])]
    ),
    ("upgrade_template",0,"Hidden Text","none",
        [
            (start_presentation, "prsnt_upgrade_template"),
        ],
        [("upgrade_template_back",[],"{!}Return",[])]
    ),
# LAV MODIFICATIONS END (COMPANIONS OVERSEER MOD)
####################################################################################################################

####################################################################################################################
# TROOPS OVERVIEW MOD - P key for regular troops upgrade
    ("troops_overview",0,"Hidden Text","none",
        [
            (start_presentation, "prsnt_troops_overview"),
        ],
        [("troops_overview_back",[],"{!}Return",[])]
    ),
]
