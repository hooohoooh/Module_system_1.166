# -*- coding: utf-8 -*-
# module_scripts_trade_economy.py -- auto split from module_scripts.py (feature: 经济贸易/商队/物价)
# entries: 33 (order preserved within this file)
from header_presentations import *
from header_common import *
from header_operations import *
from module_constants import *
from module_constants import *
from header_parties import *
from header_skills import *
from header_mission_templates import *
from header_items import *
from header_triggers import *
from header_terrain_types import *
from header_music import *
from header_map_icons import *
from ID_animations import *
from ym_gatling import *
from ym_gatling_shop import *
from zhenyinghebing import *
from lco_scripts import lco_scripts
from upgrade_scripts import upgrade_scripts
##diplomacy start+
from module_factions import dplmc_factions_begin, dplmc_factions_end, dplmc_non_generic_factions_begin
##diplomacy end+
from header_presentations import tf_left_align
  #### Autoloot improved by rubik begin
from module_items import *


scripts_trade_economy = [

  ("get_trade_penalty",
    [
	##diplomacy start+
	##Changed to fall back to parameterized version
	##NEW:
      (store_script_param_1, ":item_kind_id"),
	  (call_script, "script_dplmc_get_trade_penalty", ":item_kind_id", "$g_encountered_party", "trp_player", "$g_talk_troop"),

	##OLD:
#      (store_script_param_1, ":item_kind_id"),
#      (assign, ":penalty",0),
#      
#      (party_get_skill_level, ":trade_skill", "p_main_party", skl_trade),
#      (try_begin),
#        (is_between, ":item_kind_id", trade_goods_begin, trade_goods_end),
#        (assign, ":penalty", 12), #reduced slightly 20-15-12
#        (store_mul, ":skill_bonus", ":trade_skill", 1),
#        (val_sub, ":penalty", ":skill_bonus"),
#		(val_max, ":penalty", 3),		
#      (else_try),
#        (assign, ":penalty",100),
#        (store_mul, ":skill_bonus", ":trade_skill", 5),
#        (val_sub, ":penalty", ":skill_bonus"),
#      (try_end),
#
#      (assign, ":penalty_multiplier", 1000),
###       # Apply penalty if player is hostile to merchants faction
###      (store_relation, ":merchants_reln", "fac_merchants", "fac_player_supporters_faction"),
###      (try_begin),
###        (lt, ":merchants_reln", 0),
###        (store_sub, ":merchants_reln_dif", 10, ":merchants_reln"),
###        (store_mul, ":merchants_relation_penalty", ":merchants_reln_dif", 20),
###        (val_add, ":penalty_multiplier", ":merchants_relation_penalty"),
###      (try_end),
#
#       # Apply penalty if player is on bad terms with the town
#      (try_begin),
#        (is_between, "$g_encountered_party", centers_begin, centers_end),
#        (party_get_slot, ":center_relation", "$g_encountered_party", slot_center_player_relation),
#        (store_mul, ":center_relation_penalty", ":center_relation", -3),
#        (val_add, ":penalty_multiplier", ":center_relation_penalty"),
#        (try_begin),
#          (lt, ":center_relation", 0),
#          (store_sub, ":center_penalty_multiplier", 100, ":center_relation"),
#          (val_mul, ":penalty_multiplier", ":center_penalty_multiplier"),
#          (val_div, ":penalty_multiplier", 100),
#        (try_end),
#      (try_end),
#
#       # Apply penalty if player is on bad terms with the merchant (not currently used)
#      (call_script, "script_troop_get_player_relation", "$g_talk_troop"),
#      (assign, ":troop_reln", reg0),
#      #(troop_get_slot, ":troop_reln", "$g_talk_troop", slot_troop_player_relation),
#      (try_begin),
#        (lt, ":troop_reln", 0),
#        (store_sub, ":troop_reln_dif", 0, ":troop_reln"),
#        (store_mul, ":troop_relation_penalty", ":troop_reln_dif", 20),
#        (val_add, ":penalty_multiplier", ":troop_relation_penalty"),
#      (try_end),
#      
#	  
#	  (try_begin),
#		(is_between, "$g_encountered_party", villages_begin, villages_end),
#	    (val_mul, ":penalty", 5), #1.25x trade penalty in villages.
#		(val_div, ":penalty", 4),
#	  (try_end),
#	  
#	  #(try_begin),
#            #(is_between, "$g_encountered_party", centers_begin, centers_end),
#	    ##Double trade penalty if no local production or consumption
#	    #(is_between, ":item_kind_id", trade_goods_begin, trade_goods_end),
#	    #(call_script, "script_center_get_production", "$g_encountered_party", ":item_kind_id"),
#	    #(eq, reg0, 0),
#	    #(call_script, "script_center_get_consumption", "$g_encountered_party", ":item_kind_id"),
#	    #(eq, reg0, 0),
#	    #(val_mul, ":penalty", 2),
#	  #(try_end),
#	  
#      (val_mul, ":penalty",  ":penalty_multiplier"),
#      (val_div, ":penalty", 1000),
#      (val_max, ":penalty", 1),
#      (assign, reg0, ":penalty"),
  ]),
	("initialize_trade_routes",
	[
	  #Gekokujo trade routes
	  
	  #EDO - 6 routes
	  (call_script, "script_set_trade_route_between_centers", "p_town_1", "p_town_2"), #Edo - Mito
	  (call_script, "script_set_trade_route_between_centers", "p_town_1", "p_town_3"), #Edo - Choshi
	  (call_script, "script_set_trade_route_between_centers", "p_town_1", "p_town_10"), #Edo - Niigata
	  (call_script, "script_set_trade_route_between_centers", "p_town_1", "p_town_11"), #Edo - Kofu
	  (call_script, "script_set_trade_route_between_centers", "p_town_1", "p_town_12"), #Edo - Takada
	  (call_script, "script_set_trade_route_between_centers", "p_town_1", "p_town_15"), #Edo - Sendai
	  (call_script, "script_set_trade_route_between_centers", "p_town_1", "p_town_23"), #Edo - Odawara
	  
	  #MITO - 3 routes
	  #Edo
	  (call_script, "script_set_trade_route_between_centers", "p_town_2", "p_town_3"), #Mito - Choshi
	  (call_script, "script_set_trade_route_between_centers", "p_town_2", "p_town_15"), #Mito - Sendai
	  
	  #CHOSHI - 2 routes
	  #Edo, Mito
	  
	  #KYOTO - 7 routes
	  (call_script, "script_set_trade_route_between_centers", "p_town_4", "p_town_5"), #Kyoto - Osaka
	  (call_script, "script_set_trade_route_between_centers", "p_town_4", "p_town_6"), #Kyoto - Tsu
	  (call_script, "script_set_trade_route_between_centers", "p_town_4", "p_town_7"), #Kyoto - Himeji
	  (call_script, "script_set_trade_route_between_centers", "p_town_4", "p_town_9"), #Kyoto - Kiyosu
	  (call_script, "script_set_trade_route_between_centers", "p_town_4", "p_town_24"), #Kyoto - Nara
	  (call_script, "script_set_trade_route_between_centers", "p_town_4", "p_town_26"), #Kyoto - Imahama
	  (call_script, "script_set_trade_route_between_centers", "p_town_4", "p_town_32"), #Kyoto - Tottori
	  
	  #OSAKA - 6 routes
	  #Kyoto
	  (call_script, "script_set_trade_route_between_centers", "p_town_5", "p_town_7"), #Osaka - Himeji
	  (call_script, "script_set_trade_route_between_centers", "p_town_5", "p_town_22"), #Osaka - Matsuyama
	  (call_script, "script_set_trade_route_between_centers", "p_town_5", "p_town_24"), #Osaka - Nara
	  (call_script, "script_set_trade_route_between_centers", "p_town_5", "p_town_32"), #Osaka - Tottori
	  (call_script, "script_set_trade_route_between_centers", "p_town_5", "p_town_31"), #Osaka - Kochi
	  
	  #TSU - 2 routes
	  (call_script, "script_set_trade_route_between_centers", "p_town_6", "p_town_9"), #Tsu - Kiyosu
	  (call_script, "script_set_trade_route_between_centers", "p_town_6", "p_town_24"), #Tsu - Nara
	  
	  #HIMEJI - 6 routes
	  #Kyoto, Osaka
	  (call_script, "script_set_trade_route_between_centers", "p_town_7", "p_town_14"), #Himeji - Okayama
	  (call_script, "script_set_trade_route_between_centers", "p_town_7", "p_town_26"), #Himeji - Ichijodani
	  (call_script, "script_set_trade_route_between_centers", "p_town_7", "p_town_28"), #Himeji - Izumo
	  (call_script, "script_set_trade_route_between_centers", "p_town_7", "p_town_32"), #Himeji - Tottori
	  
	  #KANAZAWA - 4 routes
	  (call_script, "script_set_trade_route_between_centers", "p_town_8", "p_town_9"), #Kanazawa - Kiyosu
	  (call_script, "script_set_trade_route_between_centers", "p_town_8", "p_town_11"), #Kanazawa - Kofu
	  (call_script, "script_set_trade_route_between_centers", "p_town_8", "p_town_12"), #Kanazawa - Takada
	  (call_script, "script_set_trade_route_between_centers", "p_town_8", "p_town_26"), #Kanazawa - Ichijodani
	  
	  #KIYOSU - 5 routes
	  #Kanazawa, Tsu
	  (call_script, "script_set_trade_route_between_centers", "p_town_9", "p_town_11"), #Kiyosu - Kofu
	  (call_script, "script_set_trade_route_between_centers", "p_town_9", "p_town_12"), #Kiyosu - Takada
	  (call_script, "script_set_trade_route_between_centers", "p_town_9", "p_town_26"), #Kiyosu - Ichijodani
	  (call_script, "script_set_trade_route_between_centers", "p_town_9", "p_town_24"), #Kiyosu - Nara
	  (call_script, "script_set_trade_route_between_centers", "p_town_9", "p_town_25"), #Kiyosu - Hamamatsu
	  
	  #NIIGATA - 4 routes
	  #Edo
	  (call_script, "script_set_trade_route_between_centers", "p_town_10", "p_town_12"), #Niigata - Takada
	  (call_script, "script_set_trade_route_between_centers", "p_town_10", "p_town_16"), #Niigata - Yonezawa
	  (call_script, "script_set_trade_route_between_centers", "p_town_10", "p_town_17"), #Niigata - Kubota
	  
	  #KOFU - 6 routes
	  #Edo, Kanazawa, Kiyosu
	  (call_script, "script_set_trade_route_between_centers", "p_town_11", "p_town_12"), #Kofu - Takada
	  (call_script, "script_set_trade_route_between_centers", "p_town_11", "p_town_23"), #Kofu - Odawara
	  (call_script, "script_set_trade_route_between_centers", "p_town_11", "p_town_25"), #Kofu - Hamamatsu
	  
	  #TAKADA - 6 routes
	  #Edo, Kanazawa, Kiyosu, Niigata, Kofu
	  (call_script, "script_set_trade_route_between_centers", "p_town_12", "p_town_23"), #Takada - Odawara
	  
	  #HIROSHIMA - 4 routes
	  (call_script, "script_set_trade_route_between_centers", "p_town_13", "p_town_14"), #Hiroshima - Okayama
	  (call_script, "script_set_trade_route_between_centers", "p_town_13", "p_town_22"), #Hiroshima - Matsuyama
	  (call_script, "script_set_trade_route_between_centers", "p_town_13", "p_town_27"), #Hiroshima - Yamaguchi
	  (call_script, "script_set_trade_route_between_centers", "p_town_13", "p_town_28"), #Hiroshima - Izumo
	  
	  #OKAYAMA - 5 routes
	  #Himeji, Hiroshima
	  (call_script, "script_set_trade_route_between_centers", "p_town_14", "p_town_22"), #Okayama - Matsuyama
	  (call_script, "script_set_trade_route_between_centers", "p_town_14", "p_town_28"), #Okayama - Izumo
	  (call_script, "script_set_trade_route_between_centers", "p_town_14", "p_town_32"), #Okayama - Tottori
	  
	  #SENDAI - 5 routes
	  #Edo, Mito
	  (call_script, "script_set_trade_route_between_centers", "p_town_15", "p_town_16"), #Sendai - Yonezawa
	  (call_script, "script_set_trade_route_between_centers", "p_town_15", "p_town_17"), #Sendai - Kubota
	  (call_script, "script_set_trade_route_between_centers", "p_town_15", "p_town_18"), #Sendai - Hirosaki
	  
	  #YONEZAWA - 3 routes
	  #Niigata, Sendai
	  (call_script, "script_set_trade_route_between_centers", "p_town_16", "p_town_17"), #Yonezawa - Kubota
	  
	  #KUBOTA - 3 routes
	  #Sendai, Yonezawa
	  (call_script, "script_set_trade_route_between_centers", "p_town_17", "p_town_18"), #Kubota - Hirosaki
	  
	  #HIROSAKI - 2 routes
	  #Sendai, Kubota
	  
	  #HAKATA - 5 routes
	  (call_script, "script_set_trade_route_between_centers", "p_town_19", "p_town_21"), #Hakata - Nagasaki
	  (call_script, "script_set_trade_route_between_centers", "p_town_19", "p_town_27"), #Hakata - Yamaguchi
	  (call_script, "script_set_trade_route_between_centers", "p_town_19", "p_town_28"), #Hakata - Izumo
	  (call_script, "script_set_trade_route_between_centers", "p_town_19", "p_town_29"), #Hakata - Funai
	  (call_script, "script_set_trade_route_between_centers", "p_town_19", "p_town_30"), #Hakata - Kumamoto
	  
	  #KAGOSHIMA - 3 routes
	  (call_script, "script_set_trade_route_between_centers", "p_town_20", "p_town_21"), #Kagoshima - Nagasaki
	  (call_script, "script_set_trade_route_between_centers", "p_town_20", "p_town_29"), #Kagoshima - Funai
	  (call_script, "script_set_trade_route_between_centers", "p_town_20", "p_town_30"), #Kagoshima - Kumamoto
	  
	  #NAGASAKI - 3 routes
	  #Hakata, Kagoshima
	  (call_script, "script_set_trade_route_between_centers", "p_town_21", "p_town_30"), #Kagoshima - Kumamoto
	  
	  #MATSUYAMA - 5 routes
	  #Osaka, Hiroshima, Okayama
	  (call_script, "script_set_trade_route_between_centers", "p_town_22", "p_town_29"), #Kagoshima - Funai
	  (call_script, "script_set_trade_route_between_centers", "p_town_22", "p_town_31"), #Kagoshima - Kochi
	  
	  #ODAWARA - 4 routes
	  #Edo, Kofu, Takada
	  (call_script, "script_set_trade_route_between_centers", "p_town_23", "p_town_25"), #Odawara - Hamamatsu
	  
	  #NARA - 5 routes
	  #Kyoto, Osaka, Tsu, Kiyosu
	  (call_script, "script_set_trade_route_between_centers", "p_town_24", "p_town_26"), #Nara - Imahama
	  
	  #HAMAMATSU - 3 routes
	  #Kiyosu, Kofu, Odawara
	  
	  #ICHIJODANI - 6 routes
	  #Kanazawa, Kyoto, Kiyosu, Himeji, Nara
	  (call_script, "script_set_trade_route_between_centers", "p_town_26", "p_town_32"), #Imahama - Tottori
	  
	  #YAMAGUCHI - 3 routes
	  #Hiroshima, Hakata
	  (call_script, "script_set_trade_route_between_centers", "p_town_27", "p_town_28"), #Yamaguchi - Izumo
	  
	  #IZUMO - 6 routes
	  #Himeji, Okayama, Hiroshima, Hakata, Yamaguchi
	  (call_script, "script_set_trade_route_between_centers", "p_town_28", "p_town_32"), #Izumo - Tottori
	  
	  #FUNAI - 4 routes
	  #Hakata, Kagoshima, Matsuyama
	  (call_script, "script_set_trade_route_between_centers", "p_town_29", "p_town_30"), #Funai - Kumamoto
	  
	  #KUMAMOTO
	  #Hakata, Kagoshima, Nagasaki, Funai
	  
	  #KOCHI - 2 routes
	  #Osaka, Matsuyama
	  
	  #TOTTORI - 6 routes
	  #Kyoto, Osaka, Himeji, Okayama, Ichijodani, Izumo
	  
	  #SARGOTH - 10 routes
      #(call_script, "script_set_trade_route_between_centers", "p_town_1", "p_town_2"), #Sargoth - Tihr
      #(call_script, "script_set_trade_route_between_centers", "p_town_1", "p_town_4"), #Sargoth - Suno
      #(call_script, "script_set_trade_route_between_centers", "p_town_1", "p_town_12"), #Sargoth - Wercheg
      #(call_script, "script_set_trade_route_between_centers", "p_town_1", "p_town_11"), #Sargoth - Curaw
      #(call_script, "script_set_trade_route_between_centers", "p_town_1", "p_town_8"), #Sargoth - Reyvadin
      #(call_script, "script_set_trade_route_between_centers", "p_town_1", "p_town_13"), #Sargoth - Rivacheg
      #(call_script, "script_set_trade_route_between_centers", "p_town_1", "p_town_7"), #Sargoth - Uxkhal
      #(call_script, "script_set_trade_route_between_centers", "p_town_1", "p_town_9"), #Sargoth - Khudan
      #(call_script, "script_set_trade_route_between_centers", "p_town_1", "p_town_6"), #Sargoth - Praven
      #(call_script, "script_set_trade_route_between_centers", "p_town_1", "p_town_15"), #Sargoth - Yalen      
      #(call_script, "script_set_trade_route_between_centers", "p_town_1", "p_town_16"), #Sargoth - Dhirim
	 
	  #TIHR- 8 Routes
      #(call_script, "script_set_trade_route_between_centers", "p_town_2", "p_town_4"), #Tihr- Suno
      #(call_script, "script_set_trade_route_between_centers", "p_town_2", "p_town_6"), #Tihr - Praven
      #(call_script, "script_set_trade_route_between_centers", "p_town_2", "p_town_7"), #Tihr - Uxkhal
      #(call_script, "script_set_trade_route_between_centers", "p_town_2", "p_town_15"), #Tihr - Yalen
      #(call_script, "script_set_trade_route_between_centers", "p_town_2", "p_town_12"), #Tihr - Wercheg
      #(call_script, "script_set_trade_route_between_centers", "p_town_2", "p_town_8"), #Tihr - Reyvadin
      #(call_script, "script_set_trade_route_between_centers", "p_town_2", "p_town_11"), #Tihr - Curaw      
      #(call_script, "script_set_trade_route_between_centers", "p_town_2", "p_town_16"), #Thir - Dhirim

	  #VELUCA - 8 Routes
      #(call_script, "script_set_trade_route_between_centers", "p_town_3", "p_town_7"), #Veluca- Uxkhal
      #(call_script, "script_set_trade_route_between_centers", "p_town_3", "p_town_5"), #Veluca - Jelkala
      #(call_script, "script_set_trade_route_between_centers", "p_town_3", "p_town_15"), #Veluca - Yalen
      #(call_script, "script_set_trade_route_between_centers", "p_town_3", "p_town_16"), #Veluca - Dhirim
      #(call_script, "script_set_trade_route_between_centers", "p_town_3", "p_town_14"), #Veluca - Halmar
      #(call_script, "script_set_trade_route_between_centers", "p_town_3", "p_town_4"), #Veluca - Suno
      #(call_script, "script_set_trade_route_between_centers", "p_town_3", "p_town_19"), #Veluca - Shariz
      #(call_script, "script_set_trade_route_between_centers", "p_town_3", "p_town_6"), #Veluca - Praven

	  #SUNO - 11 routes
	  #Sargoth, Tihr, Veluca
      #(call_script, "script_set_trade_route_between_centers", "p_town_4", "p_town_12"), #Suno - Wercheg
      #(call_script, "script_set_trade_route_between_centers", "p_town_4", "p_town_8"), #Suno - Reyvadin
      #(call_script, "script_set_trade_route_between_centers", "p_town_4", "p_town_11"), #Suno - Curaw
      #(call_script, "script_set_trade_route_between_centers", "p_town_4", "p_town_6"), #Suno - Praven
      #(call_script, "script_set_trade_route_between_centers", "p_town_4", "p_town_7"), #Suno - Uxkhal
      #(call_script, "script_set_trade_route_between_centers", "p_town_4", "p_town_16"), #Suno - Dhirim
      #(call_script, "script_set_trade_route_between_centers", "p_town_4", "p_town_5"), #Suno - Jelkala
      #(call_script, "script_set_trade_route_between_centers", "p_town_4", "p_town_15"), #Suno - Yalen

	  #JELKALA - 6 ROUTES
      #Veluca, Suno
      #(call_script, "script_set_trade_route_between_centers", "p_town_5", "p_town_15"), #Jelkala - Yalen
      #(call_script, "script_set_trade_route_between_centers", "p_town_5", "p_town_6"), #Jelkala - Praven
      #(call_script, "script_set_trade_route_between_centers", "p_town_5", "p_town_7"), #Jelkala - Uxkhal
      #(call_script, "script_set_trade_route_between_centers", "p_town_5", "p_town_19"), #Jelkala - Shariz
	  
	  #PRAVEN - 7 ROUTES
	  #Tihr, Veluca, Suno, Jelkala
      #(call_script, "script_set_trade_route_between_centers", "p_town_6", "p_town_7"), #Praven - Uxkhal
      #(call_script, "script_set_trade_route_between_centers", "p_town_6", "p_town_15"), #Praven - Yalen
      #(call_script, "script_set_trade_route_between_centers", "p_town_6", "p_town_16"), #Praven - Dhirim

	  #UXKHAL - 9 Routes
	  #Sargoth, Tihr, Suno, Jelkala, Praven 
      #(call_script, "script_set_trade_route_between_centers", "p_town_7", "p_town_15"), #Yalen
      #(call_script, "script_set_trade_route_between_centers", "p_town_7", "p_town_16"), #Dhirim
      #(call_script, "script_set_trade_route_between_centers", "p_town_7", "p_town_19"), #Shariz
      #(call_script, "script_set_trade_route_between_centers", "p_town_7", "p_town_14"), #Halmar

	  #REYVADIN - 9 Routes
	  #Suno, Sargoth
      #(call_script, "script_set_trade_route_between_centers", "p_town_8", "p_town_9"), #Khudan 
      #(call_script, "script_set_trade_route_between_centers", "p_town_8", "p_town_11"), #Curaw
      #(call_script, "script_set_trade_route_between_centers", "p_town_8", "p_town_12"), #Wercheg
      #(call_script, "script_set_trade_route_between_centers", "p_town_8", "p_town_13"), #Rivacheg
      #(call_script, "script_set_trade_route_between_centers", "p_town_8", "p_town_16"), #Dhirim
      #(call_script, "script_set_trade_route_between_centers", "p_town_8", "p_town_18"), #Narra
      #(call_script, "script_set_trade_route_between_centers", "p_town_8", "p_town_17"), #Ichamur

	  #KHUDAN - 9 Routes
	  #Sargoth, Reyvadin
      #(call_script, "script_set_trade_route_between_centers", "p_town_9", "p_town_11"), #Curaw
      #(call_script, "script_set_trade_route_between_centers", "p_town_9", "p_town_13"), #Rivacheg
      #(call_script, "script_set_trade_route_between_centers", "p_town_9", "p_town_12"), #Wercheg
      #(call_script, "script_set_trade_route_between_centers", "p_town_9", "p_town_17"), #Ichamur
      #(call_script, "script_set_trade_route_between_centers", "p_town_9", "p_town_10"), #Tulga
      #(call_script, "script_set_trade_route_between_centers", "p_town_9", "p_town_16"), #Dhirim
      #(call_script, "script_set_trade_route_between_centers", "p_town_9", "p_town_18"), #Narra

	  #TULGA - 7 Routes
	  #Khudan
      #(call_script, "script_set_trade_route_between_centers", "p_town_10", "p_town_17"), #Ichamur
      #(call_script, "script_set_trade_route_between_centers", "p_town_10", "p_town_18"), #Narra
      #(call_script, "script_set_trade_route_between_centers", "p_town_10", "p_town_22"), #Bariyye
      #(call_script, "script_set_trade_route_between_centers", "p_town_10", "p_town_21"), #Ahmerrad
      #(call_script, "script_set_trade_route_between_centers", "p_town_10", "p_town_14"), #Halmar
      #(call_script, "script_set_trade_route_between_centers", "p_town_10", "p_town_20"), #Durquba

	  #CURAW - 9 Routes
	  #Khudan, Reyvadin, Sargoth, Suno
      #(call_script, "script_set_trade_route_between_centers", "p_town_11", "p_town_12"), #Wercheg
      #(call_script, "script_set_trade_route_between_centers", "p_town_11", "p_town_13"), #Rivacheg
      #(call_script, "script_set_trade_route_between_centers", "p_town_11", "p_town_14"), #Halmar
      #(call_script, "script_set_trade_route_between_centers", "p_town_11", "p_town_16"), #Dhirim
      #(call_script, "script_set_trade_route_between_centers", "p_town_11", "p_town_17"), #Ichamur
      
	  #WERCHEG - 7 Routes
	  #Sargoth, Suno, Reyvadin, Khudan, Curaw, Tihr
      #(call_script, "script_set_trade_route_between_centers", "p_town_12", "p_town_13"), #Rivacheg
	  
	  #RIVACHEG - 6 Routes
	  #Sargoth, Reyvadin, Khudan, Curaw, Wercheg
      #(call_script, "script_set_trade_route_between_centers", "p_town_13", "p_town_17"), #Ichamur

	  #HALMAR- 11 Routes 
	  #Veluca, Uxkhal, Tulga, Curaw
      #(call_script, "script_set_trade_route_between_centers", "p_town_14", "p_town_17"), #Ichamur
      #(call_script, "script_set_trade_route_between_centers", "p_town_14", "p_town_18"), #Narra
      #(call_script, "script_set_trade_route_between_centers", "p_town_14", "p_town_21"), #Ahmerrad
      #(call_script, "script_set_trade_route_between_centers", "p_town_14", "p_town_22"), #Bariyye
      #(call_script, "script_set_trade_route_between_centers", "p_town_14", "p_town_20"), #Durquba
      #(call_script, "script_set_trade_route_between_centers", "p_town_14", "p_town_19"), #Shariz
      #(call_script, "script_set_trade_route_between_centers", "p_town_14", "p_town_16"), #Dhirim

	  #YALEN - 7 Routes
	  #Sargoth, Tihr, Veluca, Suno, Jelkala, Praven, Uxkhal
	  
	  #DHIRIM - 13 Routes
	  #Sargoth, Thir, Veluca, Suno, Praven, Uxkhal, Reyvadin, Khudan, Curaw, Halmar
      #(call_script, "script_set_trade_route_between_centers", "p_town_16", "p_town_18"), #Narra
      #(call_script, "script_set_trade_route_between_centers", "p_town_16", "p_town_20"), #Durquba
      #(call_script, "script_set_trade_route_between_centers", "p_town_16", "p_town_19"), #Shariz
	  
	  #ICHAMUR - 7 Routes
      #Reyvadin, Khudan, Tulga, Curaw, Rivacheg, Halmar
      #(call_script, "script_set_trade_route_between_centers", "p_town_17", "p_town_18"), #Narra

	  #NARRA - 9 Routes
      #Reyvadin, Khudan, Tulga, Halmar, Dhirim, Ichamur
      #(call_script, "script_set_trade_route_between_centers", "p_town_18", "p_town_20"), #Durquba
      #(call_script, "script_set_trade_route_between_centers", "p_town_18", "p_town_21"), #Ahmerrad
      #(call_script, "script_set_trade_route_between_centers", "p_town_18", "p_town_22"), #Bariyye
	  
	  #SHARIZ - 8 Routes
      #Veluca, Jelkala, Uxkhal, Halmar, Dhirim
      #(call_script, "script_set_trade_route_between_centers", "p_town_19", "p_town_20"), #Durquba
      #(call_script, "script_set_trade_route_between_centers", "p_town_19", "p_town_21"), #Ahmerrad
      #(call_script, "script_set_trade_route_between_centers", "p_town_19", "p_town_22"), #Bariyye
	  
	  #DURQUBA - 7 Routes
      #Tulga, Halmar, Dhirim, Narra, Shariz
      #(call_script, "script_set_trade_route_between_centers", "p_town_20", "p_town_21"), #Ahmerrad
      #(call_script, "script_set_trade_route_between_centers", "p_town_20", "p_town_22"), #Bariyye

	  #AHMERRAD - 6 Routes
      #Tulga, Halmar, Narra, Shariz, Durquba
      #(call_script, "script_set_trade_route_between_centers", "p_town_21", "p_town_22"), #Bariyye

	  #BARIYYE - 6 Routes
      #Tulga, Halmar, Narra, Shariz, Durquba, Ahmerrad
	]),
  #script_update_party_creation_random_limits
  # INPUT: none
  ("update_party_creation_random_limits",
    [
      (store_character_level, ":player_level", "trp_player"),
      (store_mul, ":upper_limit", ":player_level", 3),
      (val_add, ":upper_limit", 25),
      (val_min, ":upper_limit", 100),
      (set_party_creation_random_limits, 0, ":upper_limit"),
      (assign, reg0, ":upper_limit"),
  ]),
  #script_set_trade_route_between_centers
  # INPUT:
  # param1: center_no_1
  # param1: center_no_2
  ("set_trade_route_between_centers",
    [(store_script_param, ":center_no_1", 1),
     (store_script_param, ":center_no_2", 2),
     (assign, ":center_1_added", 0),
     (assign, ":center_2_added", 0),
     (try_for_range, ":cur_slot", slot_town_trade_routes_begin, slot_town_trade_routes_end),
       (try_begin),
         (eq, ":center_1_added", 0),
         (party_slot_eq, ":center_no_1", ":cur_slot", 0),
         (party_set_slot, ":center_no_1", ":cur_slot", ":center_no_2"),
         (assign, ":center_1_added", 1),
       (try_end),
       (try_begin),
         (eq, ":center_2_added", 0),
         (party_slot_eq, ":center_no_2", ":cur_slot", 0),
         (party_set_slot, ":center_no_2", ":cur_slot", ":center_no_1"),
         (assign, ":center_2_added", 1),
       (try_end),
     (try_end),
     (try_begin),
       (eq, ":center_1_added", 0),
       (str_store_party_name, s1, ":center_no_1"),
       (display_message, "@{!}DEBUG -- ERROR: More than 15 trade routes are given for {s1}."),
     (try_end),
     (try_begin),
       (eq, ":center_2_added", 0),
       (str_store_party_name, s1, ":center_no_2"),
       (display_message, "@{!}DEBUG -- ERROR: More than 15 trade routes are given for {s1}."),
     (try_end),
     ]),
  ("average_trade_good_prices", #Called from start
    [	
	#This should be done by route rather than distance
      (store_sub, ":item_to_slot", slot_town_trade_good_prices_begin, trade_goods_begin),

      (try_for_range, ":center_no", towns_begin, towns_end),
        (this_or_next|is_between, ":center_no", towns_begin, towns_end),
		(is_between, ":center_no", villages_begin, villages_end),
		
        (try_for_range, ":other_center", centers_begin, centers_end),
          (this_or_next|is_between, ":center_no", towns_begin, towns_end),
		  (is_between, ":center_no", villages_begin, villages_end),
 			
          (neq, ":other_center", ":center_no"),
          (store_distance_to_party_from_party, ":cur_distance", ":center_no", ":other_center"),
          (lt, ":cur_distance", 50), #Reduced from 110
          (store_sub, ":dist_factor", 50, ":cur_distance"),
		  
          (try_for_range, ":cur_good", trade_goods_begin, trade_goods_end),
            (store_add, ":cur_good_slot", ":cur_good", ":item_to_slot"),
            (party_get_slot, ":center_price", ":center_no", ":cur_good_slot"),
            (party_get_slot, ":other_center_price", ":other_center", ":cur_good_slot"),
            (store_sub, ":price_dif", ":center_price", ":other_center_price"),
			
            (assign, ":price_dif_change", ":price_dif"),

            (val_mul ,":price_dif_change", ":dist_factor"),
            (val_div ,":price_dif_change", 1000), #Maximum of 1/20 per center
            (val_add, ":other_center_price", ":price_dif_change"),
            (party_set_slot, ":other_center", ":cur_good_slot", ":other_center_price"),
			
            (val_sub, ":center_price", ":price_dif_change"),
            (party_set_slot, ":center_no", ":cur_good_slot", ":center_price"),			
          (try_end),
        (try_end),
      (try_end),
  ]),
  ("average_trade_good_prices_2", #Called from start
    [
	
	#This should be done by route rather than distance
      (store_sub, ":item_to_slot", slot_town_trade_good_prices_begin, trade_goods_begin),

      (try_for_range, ":center_no", towns_begin, towns_end),       		
        (try_for_range, ":other_center", centers_begin, centers_end),
          (this_or_next|is_between, ":other_center", towns_begin, towns_end),
			(is_between, ":other_center", villages_begin, villages_end),

		  (this_or_next|party_slot_eq, ":other_center", slot_village_market_town, ":center_no"),
		  (this_or_next|party_slot_eq, ":center_no", slot_town_trade_route_1, ":other_center"),
		  (this_or_next|party_slot_eq, ":center_no", slot_town_trade_route_2, ":other_center"),
		  (this_or_next|party_slot_eq, ":center_no", slot_town_trade_route_3, ":other_center"),
		  (this_or_next|party_slot_eq, ":center_no", slot_town_trade_route_4, ":other_center"),
		  (this_or_next|party_slot_eq, ":center_no", slot_town_trade_route_5, ":other_center"),
		  (this_or_next|party_slot_eq, ":center_no", slot_town_trade_route_6, ":other_center"),
		  (this_or_next|party_slot_eq, ":center_no", slot_town_trade_route_7, ":other_center"),
		  (this_or_next|party_slot_eq, ":center_no", slot_town_trade_route_8, ":other_center"),
		  (this_or_next|party_slot_eq, ":center_no", slot_town_trade_route_9, ":other_center"),
		  (this_or_next|party_slot_eq, ":center_no", slot_town_trade_route_10, ":other_center"),
		  (this_or_next|party_slot_eq, ":center_no", slot_town_trade_route_11, ":other_center"),
		  (this_or_next|party_slot_eq, ":center_no", slot_town_trade_route_12, ":other_center"),
		  (this_or_next|party_slot_eq, ":center_no", slot_town_trade_route_13, ":other_center"),
		  (this_or_next|party_slot_eq, ":center_no", slot_town_trade_route_14, ":other_center"),
			(party_slot_eq, ":center_no", slot_town_trade_route_15, ":other_center"),

#          (neq, ":other_center", ":center_no"),
#          (store_distance_to_party_from_party, ":cur_distance", ":center_no", ":other_center"),
#          (lt, ":cur_distance", 50), #Reduced from 110
#          (store_sub, ":dist_factor", 50, ":cur_distance"),
		  
          (try_for_range, ":cur_good", trade_goods_begin, trade_goods_end),
            (store_add, ":cur_good_slot", ":cur_good", ":item_to_slot"),
            (party_get_slot, ":center_price", ":center_no", ":cur_good_slot"),
            (party_get_slot, ":other_center_price", ":other_center", ":cur_good_slot"),
            (store_sub, ":price_dif", ":center_price", ":other_center_price"),
			
			(store_div, ":price_dif_change", ":price_dif", 5), #this is done twice, reduced from 4
#            (assign, ":price_dif_change", ":price_dif"),

#            (val_mul ,":price_dif_change", ":dist_factor"),
#            (val_div ,":price_dif_change", 500), #Maximum of 1/10 per center
            (val_add, ":other_center_price", ":price_dif_change"),
            (party_set_slot, ":other_center", ":cur_good_slot", ":other_center_price"),
			
            (val_sub, ":center_price", ":price_dif_change"),
            (party_set_slot, ":center_no", ":cur_good_slot", ":center_price"),
			
          (try_end),
        (try_end),
      (try_end),
  ]),
  #script_average_trade_good_productions
  # INPUT: none (called only from game start?)
  #This is currently deprecated, as I was going to try to fine-tune production
  ("average_trade_good_productions",
    [	  
      (store_sub, ":item_to_slot", slot_town_trade_good_productions_begin, trade_goods_begin),
      (try_for_range, ":center_no", towns_begin, towns_end),
        (this_or_next|is_between, ":center_no", towns_begin, towns_end),
        (is_between, ":center_no", villages_begin, villages_end),
        (try_for_range, ":other_center", centers_begin, centers_end),
          (this_or_next|is_between, ":center_no", towns_begin, towns_end),
          (is_between, ":center_no", villages_begin, villages_end),
          (neq, ":other_center", ":center_no"),
          (store_distance_to_party_from_party, ":cur_distance", ":center_no", ":other_center"),
          (lt, ":cur_distance", 110),
          (store_sub, ":dist_factor", 110, ":cur_distance"),
          (try_for_range, ":cur_good", trade_goods_begin, trade_goods_end),
            (store_add, ":cur_good_slot", ":cur_good", ":item_to_slot"),
            (party_get_slot, ":center_production", ":center_no", ":cur_good_slot"),
            (party_get_slot, ":other_center_production", ":other_center", ":cur_good_slot"),
            (store_sub, ":prod_dif", ":center_production", ":other_center_production"),
            (gt, ":prod_dif", 0),
            (store_mul, ":prod_dif_change", ":prod_dif", 1),
##            (try_begin),
##              (is_between, ":center_no", towns_begin, towns_end),
##              (is_between, ":other_center", towns_begin, towns_end),
##              (val_mul, ":cur_distance", 2),
##            (try_end),
            (val_mul ,":prod_dif_change", ":dist_factor"),
            (val_div ,":prod_dif_change", 110),
            (val_add, ":other_center_production", ":prod_dif_change"),
            (party_set_slot, ":other_center", ":cur_good_slot", ":other_center_production"),
          (try_end),
        (try_end),
      (try_end),
  ]),
  #script_normalize_trade_good_productions 
  #Adjusts productions according to the amount of the item produced
  # INPUT: none
  # This currently deprecated, as I was going to try to fine-tune productions
  ("normalize_trade_good_productions",
    [	  
      (store_sub, ":item_to_slot", slot_town_trade_good_productions_begin, trade_goods_begin),
      (try_for_range, ":cur_good", trade_goods_begin, trade_goods_end),
        (assign, ":total_production", 0),
        (assign, ":num_centers", 0),
        (store_add, ":cur_good_slot", ":cur_good", ":item_to_slot"),
        (try_for_range, ":center_no", centers_begin, centers_end),
          (val_add, ":num_centers", 1),
          (try_begin),
            (is_between, ":center_no", towns_begin, towns_end), #each town is weighted as 5 villages...
            (val_add, ":num_centers", 4), 
          (try_end),
          (party_get_slot, ":center_production", ":center_no", ":cur_good_slot"),
          (val_add, ":total_production", ":center_production"),
        (try_end),
        (store_div, ":new_production_difference", ":total_production", ":num_centers"),
        (neq, ":new_production_difference", 0),
        (try_for_range, ":center_no", centers_begin, centers_end),
          (this_or_next|is_between, ":center_no", towns_begin, towns_end),
          (is_between, ":center_no", villages_begin, villages_end),
          (party_get_slot, ":center_production", ":center_no", ":cur_good_slot"),
          (val_sub, ":center_production", ":new_production_difference"),
          (party_set_slot, ":center_no", ":cur_good_slot", ":center_production"),
        (try_end),
      (try_end),
  ]),
  #script_update_trade_good_prices
  # INPUT: none
  ("update_trade_good_prices",
    [
      (try_for_range, ":center_no", centers_begin, centers_end),
        (this_or_next|is_between, ":center_no", towns_begin, towns_end),
        (is_between, ":center_no", villages_begin, villages_end),
        (call_script, "script_update_trade_good_price_for_party", ":center_no"),
      (try_end),

      (try_for_range, ":cur_good", trade_goods_begin, trade_goods_end),
	    (assign, ":total_price", 0),
		(assign, ":total_constants", 0),

	    (try_for_range, ":center_no", centers_begin, centers_end),
          (this_or_next|is_between, ":center_no", towns_begin, towns_end),
          (is_between, ":center_no", villages_begin, villages_end),

          (store_sub, ":cur_good_price_slot", ":cur_good", trade_goods_begin),
          (val_add, ":cur_good_price_slot", slot_town_trade_good_prices_begin),
          (party_get_slot, ":cur_price", ":center_no", ":cur_good_price_slot"),

		  (try_begin),
		    (is_between, ":center_no", towns_begin, towns_end),
			(assign, ":constant", 5),
          (else_try),
		    (assign, ":constant", 1),
		  (try_end),

		  (val_mul, ":cur_price", ":constant"),

		  (val_add, ":total_price", ":cur_price"),
		  (val_add, ":total_constants", ":constant"),
		(try_end),

		(try_for_range, ":center_no", centers_begin, centers_end),
          (this_or_next|is_between, ":center_no", towns_begin, towns_end),
          (is_between, ":center_no", villages_begin, villages_end),

          (store_sub, ":cur_good_price_slot", ":cur_good", trade_goods_begin),
          (val_add, ":cur_good_price_slot", slot_town_trade_good_prices_begin),
          (party_get_slot, ":cur_price", ":center_no", ":cur_good_price_slot"),

		  (val_mul, ":cur_price", 1000),
		  (val_mul, ":cur_price", ":total_constants"),
		  (val_div, ":cur_price", ":total_price"),		  

		  (val_clamp, ":cur_price", minimum_price_factor, maximum_price_factor),
		  (party_set_slot, ":center_no", ":cur_good_price_slot", ":cur_price"),
		(try_end),
      (try_end),
  ]),
  #script_update_trade_good_price_for_party
  # INPUT: arg1 = party_no
  #Called once every 72 hours
  ("update_trade_good_price_for_party",
    [
      (store_script_param, ":center_no", 1),
      (try_for_range, ":cur_good", trade_goods_begin, trade_goods_end),
        (store_sub, ":cur_good_price_slot", ":cur_good", trade_goods_begin),
        (val_add, ":cur_good_price_slot", slot_town_trade_good_prices_begin),
		(party_get_slot, ":cur_price", ":center_no", ":cur_good_price_slot"),
		
        (call_script, "script_center_get_production", ":center_no", ":cur_good"),
		(assign, ":production", reg0),
		
        (call_script, "script_center_get_consumption", ":center_no", ":cur_good"),
		(assign, ":consumption", reg0),

		(val_sub, ":production", ":consumption"),
		
		#Change averages production x 2(1+random(2)) (was 4, random(8)) for excess demand
        (try_begin),
		  #supply is greater than demand
          (gt, ":production", 0), 
		  (store_mul, ":change_factor", ":production", 1), #price will be decreased by his factor
		  (store_random_in_range, ":random_change", 0, ":change_factor"),
		  (val_add, ":random_change", ":change_factor"),
		  (val_add, ":random_change", ":change_factor"),		  

		  #simulation starts
          (store_sub, ":final_price", ":cur_price", ":random_change"),
		  (val_clamp, ":final_price", minimum_price_factor, maximum_price_factor),		  		  		  
		  (try_begin), #Excess of supply decelerates over time, as low price reduces output
		    #if expected final price is 100 then it will multiply random_change by 0.308x ((100+300)/(1300) = 400/1300).
			(lt, ":final_price", 1000),
			(store_add, ":final_price_plus_300", ":final_price", 300),
			(val_mul, ":random_change", ":final_price_plus_300"),
			(val_div, ":random_change", 1300),
          (try_end),
          (val_sub, ":cur_price", ":random_change"),
        (else_try),
          (lt, ":production", 0), 
		  (store_sub, ":change_factor", 0, ":production"), #price will be increased by his factor
		  (val_mul, ":change_factor", 1), 
		  (store_random_in_range, ":random_change", 0, ":change_factor"),
		  (val_add, ":random_change", ":change_factor"),
		  (val_add, ":random_change", ":change_factor"),
          (val_add, ":cur_price", ":random_change"),
        (try_end),
			
        #Move price towards average by 3%...
		#Equilibrium is 33 cycles, or 100 days
		#Change per cycle is Production x 4
		#Thus, max differential = -5 x 4 x 33 = -660 for -5
		(try_begin),
		  (is_between, ":center_no", villages_begin, villages_end),
          (store_sub, ":price_difference", ":cur_price", average_price_factor),
          (val_mul, ":price_difference", 96),
          (val_div, ":price_difference", 100),
          (store_add, ":new_price", average_price_factor, ":price_difference"),
        (else_try),
          (store_sub, ":price_difference", ":cur_price", average_price_factor),
          (val_mul, ":price_difference", 96),
          (val_div, ":price_difference", 100),
          (store_add, ":new_price", average_price_factor, ":price_difference"),
        (try_end),
		
		#Price of manufactured goods drift towards primary raw material 
		(try_begin),
			(item_get_slot, ":raw_material", ":cur_good", slot_item_primary_raw_material),
            (neq, ":raw_material", 0),
	        (store_sub, ":raw_material_price_slot", ":raw_material", trade_goods_begin),
	        (val_add, ":raw_material_price_slot", slot_town_trade_good_prices_begin),

			(party_get_slot, ":total_raw_material_price", ":center_no", ":raw_material_price_slot"),
			(val_mul, ":total_raw_material_price", 3),
            (assign, ":number_of_centers", 3),

			(try_for_range, ":village_no", villages_begin, villages_end),
			  (party_slot_eq, ":village_no", slot_village_bound_center, ":center_no"),
			  (party_get_slot, ":raw_material_price", ":village_no", ":raw_material_price_slot"),
			  (val_add, ":total_raw_material_price", ":raw_material_price"),
			  (val_add, ":number_of_centers", 1),
            (try_end),

			(store_div, ":average_raw_material_price", ":total_raw_material_price", ":number_of_centers"),					

			(gt, ":average_raw_material_price", ":new_price"),
			(store_sub, ":raw_material_boost", ":average_raw_material_price", ":new_price"),
			(val_div, ":raw_material_boost", 10), 
			(val_add, ":new_price", ":raw_material_boost"),
		(try_end),
		
        (val_clamp, ":new_price", minimum_price_factor, maximum_price_factor),
        (party_set_slot, ":center_no", ":cur_good_price_slot", ":new_price"),

		#(assign, reg3, ":new_price"),
		#(str_store_item_name, s2, ":cur_good"),
		#(display_log_message, "@DEBUG : {s1}-{s2}, prod:{reg1}, cons:{reg2}, price:{reg3}"),
      (try_end),
  ]),
  ("center_get_production",
    [
	#Actually, this could be reset somewhat to yield supply and demand as raw numbers
	#Demand could be set values for rural and urban
	#Supply could be based on capital goods -- head of cattle, head of sheep, fish ponds, fishing fleets, acres of grain fields, olive orchards, olive presses, wine presses, mills, smithies, salt pans, potters' kilns, etc
	#Prosperity would increase both demand and supply
		(store_script_param_1, ":center_no"),
		(store_script_param_2, ":cur_good"),
  
		(assign, ":base_production", 0),
		
		#Grain products
		(try_begin),
			(eq, ":cur_good", "itm_bread"), #Demand = 3000 across Japan
			(party_get_slot, ":base_production", ":center_no", slot_center_mills),
			(val_mul, ":base_production", 20), #one mills per village, five mills per town = 160 mills 
		(else_try),
			(eq, ":cur_good", "itm_grain"), #Demand =  3200+, 1600 to mills, 1500 on its own, extra to breweries
			(party_get_slot, ":base_production", ":center_no", slot_center_acres_grain),
			(val_div, ":base_production", 125), #10000 acres is the average across Japan, extra in Swadia, less in snows and steppes, a bit from towns 
		(else_try),
			(eq, ":cur_good", "itm_ale"), #
			(party_get_slot, ":base_production", ":center_no", slot_center_breweries),
			(val_mul, ":base_production", 25), 

		(else_try),
			(eq, ":cur_good", "itm_smoked_fish"), #Demand = 20
			(party_get_slot, ":base_production", ":center_no", slot_center_fishing_fleet),
			(val_mul, ":base_production", 4), #was originally 5
		(else_try),
			(eq, ":cur_good", "itm_salt"), 
			(party_get_slot, ":base_production", ":center_no", slot_center_salt_pans),
			(val_mul, ":base_production", 35),

		#Cattle products	
		(else_try),
			(eq, ":cur_good", "itm_cattle_meat"), #Demand = 5
			(party_get_slot, ":base_production", ":center_no", slot_center_head_cattle),
			(val_div, ":base_production", 4), #was 9
		(else_try),
			(eq, ":cur_good", "itm_dried_meat"), #Demand = 15
			#(party_get_slot, ":base_production", ":center_no", slot_center_head_cattle),
			#(val_div, ":base_production", 2), #was 3
			#gekokujo dried river fish
			(party_get_slot, ":base_production", ":center_no", slot_center_head_sheep),
			(val_mul, ":base_production", 2), #last 2 for eel
		(else_try),
			(eq, ":cur_good", "itm_cheese"), 	 #Demand = 10
			#(party_get_slot, ":base_production", ":center_no", slot_center_head_cattle),
			#(val_div, ":base_production", 3), #was 4
			#gekokujo tofu
			(party_get_slot, ":base_production", ":center_no", slot_center_acres_vineyard),
			(val_div, ":base_production", 100),
		(else_try),
			(eq, ":cur_good", "itm_butter"), 	 #Demand = 2
			#(party_get_slot, ":base_production", ":center_no", slot_center_head_cattle),
			#(val_div, ":base_production", 8), #was 20
			#gekokujo miso
			(party_get_slot, ":base_production", ":center_no", slot_center_acres_vineyard),
			(val_div, ":base_production", 300),
			
		(else_try),
			(eq, ":cur_good", "itm_raw_leather"), 	 #Demand = ??
			(party_get_slot, ":base_production", ":center_no", slot_center_head_cattle),
			(val_div, ":base_production", 6),
			#(party_get_slot, ":sheep_addition", ":center_no", slot_center_head_sheep),
			#(val_div, ":sheep_addition", 12),
			#(val_add, ":base_production", ":sheep_addition"),
			
		(else_try),
			(eq, ":cur_good", "itm_leatherwork"), 	 #Demand = ??
			(party_get_slot, ":base_production", ":center_no", slot_center_tanneries),
			(val_mul, ":base_production", 20),
			
		(else_try),
			(eq, ":cur_good", "itm_honey"), 	 #Demand = 5
			#(party_get_slot, ":base_production", ":center_no", slot_center_apiaries),
			#(val_mul, ":base_production", 6),
			#gekokujo miso
			(party_get_slot, ":base_production", ":center_no", slot_center_acres_vineyard),
			(val_div, ":base_production", 150),
		(else_try),
			(eq, ":cur_good", "itm_cabbages"), 	 #Demand = 7
			(party_get_slot, ":base_production", ":center_no", slot_center_household_gardens),
			(val_mul, ":base_production", 10),
		(else_try),
			(eq, ":cur_good", "itm_apples"), 	 #Demand = 7
			(party_get_slot, ":base_production", ":center_no", slot_center_household_gardens),
			(val_mul, ":base_production", 10),
			
		#Sheep products	
		(else_try),
			(eq, ":cur_good", "itm_sausages"), 	 #Demand = 5
			(party_get_slot, ":base_production", ":center_no", slot_center_head_sheep), #average of 90 sheep
			#(val_div, ":base_production", 15),
			#gekokujo dried eel
			(val_mul, ":base_production", 2),
		(else_try),
			(eq, ":cur_good", "itm_wool"), 	 #(Demand = 0, but 15 averaged out perhaps)
			#(party_get_slot, ":base_production", ":center_no", slot_center_head_sheep), #average of 90 sheep
			#gekokujo hemp fiber
			(party_get_slot, ":base_production", ":center_no", slot_center_acres_olives),
			(val_div, ":base_production", 50),
		(else_try),
			(eq, ":cur_good", "itm_wool_cloth"), 	 #(Demand = 1500 across Japan)
			(party_get_slot, ":base_production", ":center_no", slot_center_wool_looms),
			(val_mul, ":base_production", 5), #300 across Japan
		
		(else_try),
			(this_or_next|eq, ":cur_good", "itm_pork"), 	 
			(eq, ":cur_good", "itm_chicken"), 	 
			(try_begin),
			  (is_between, ":center_no", villages_begin, villages_end),
			  (assign, ":base_production", 30), 
			(else_try),
			  (assign, ":base_production", 0), 
			(try_end),

		(else_try),
			(eq, ":cur_good", "itm_iron"), 	 #Demand = 5, one supplies three smithies
			(party_get_slot, ":base_production", ":center_no", slot_center_iron_deposits),
			(val_mul, ":base_production", 10),
		(else_try),
			(eq, ":cur_good", "itm_tools"), 	 #Demand = 560 across Japan
			(party_get_slot, ":base_production", ":center_no", slot_center_smithies),
			(val_mul, ":base_production", 3),

		#Other artisanal goods	
		(else_try),
			(eq, ":cur_good", "itm_pottery"), #560 is total demand	 
			(party_get_slot, ":base_production", ":center_no", slot_center_pottery_kilns),
			(val_mul, ":base_production", 5),

		(else_try),
			(eq, ":cur_good", "itm_raw_grapes"), 	 
			(party_get_slot, ":base_production", ":center_no", slot_center_acres_vineyard),
			(val_div, ":base_production", 100),
		(else_try),
			(eq, ":cur_good", "itm_wine"), 	 
			(party_get_slot, ":base_production", ":center_no", slot_center_wine_presses),
			(val_mul, ":base_production", 25),						
		(else_try),
			(eq, ":cur_good", "itm_raw_olives"), 	 
			#(party_get_slot, ":base_production", ":center_no", slot_center_acres_olives),
			#(val_div, ":base_production", 150),
			(party_get_slot, ":base_production", ":center_no", slot_center_apiaries),
			(val_div, ":base_production", 4),
		(else_try),
			(eq, ":cur_good", "itm_oil"), 	 
			(party_get_slot, ":base_production", ":center_no", slot_center_olive_presses),
			(val_mul, ":base_production", 12),
			
		#Flax and linen	
		(else_try),
			(eq, ":cur_good", "itm_linen"), 	 
			(party_get_slot, ":base_production", ":center_no", slot_center_linen_looms),
			(val_mul, ":base_production", 5),
		(else_try),
			(eq, ":cur_good", "itm_raw_flax"), 	 
			(party_get_slot, ":base_production", ":center_no", slot_center_acres_flax),
			(val_div, ":base_production", 80),			
		(else_try),
			(eq, ":cur_good", "itm_velvet"), 	 
			(party_get_slot, ":base_production", ":center_no", slot_center_silk_looms),
			(val_mul, ":base_production", 5),
		(else_try),
			(eq, ":cur_good", "itm_raw_silk"), 	 
			(party_get_slot, ":base_production", ":center_no", slot_center_silk_farms),
			(val_div, ":base_production", 20),
		(else_try),
			(eq, ":cur_good", "itm_raw_dyes"), 	 
			#(party_get_slot, ":base_production", ":center_no", slot_center_kirmiz_farms),
			#(val_div, ":base_production", 20),
			(try_begin),
				(eq, ":center_no", "p_town_19"), #Hakata
				(assign, ":base_production", 250),
			(else_try),
				(eq, ":center_no", "p_town_20"), #Kagoshima
				(assign, ":base_production", 200),
			(else_try),
				(eq, ":center_no", "p_town_21"), #Nagasaki
				(assign, ":base_production", 150),
			(try_end),	
		(else_try),
			(eq, ":cur_good", "itm_raw_date_fruit"), 	 
			(party_get_slot, ":base_production", ":center_no", slot_center_acres_dates),
			(val_div, ":base_production", 120),
		(else_try),
			(eq, ":cur_good", "itm_furs"), 	 #Demand = 90 across Japan
			(party_get_slot, ":base_production", ":center_no", slot_center_fur_traps),
			(val_mul, ":base_production", 25),
		(else_try),
			(eq, ":cur_good", "itm_spice"),
			(try_begin),
				(eq, ":center_no", "p_town_19"), #Hakata
				(assign, ":base_production", 50),
			(else_try),
				(eq, ":center_no", "p_town_20"), #Kagoshima
				(assign, ":base_production", 100),
			(else_try),
				(eq, ":center_no", "p_town_21"), #Nagasaki
				(assign, ":base_production", 100),
			(try_end),	
		(try_end),
							
		#Modify production by other goods
		(assign, ":modified_production", ":base_production"),
		(try_begin),
			(eq, ":cur_good", "itm_bread"),
			(call_script, "script_good_price_affects_good_production", ":center_no", "itm_grain", ":base_production", 1),
			(assign, ":modified_production", reg0),
		(else_try),
			(eq, ":cur_good", "itm_ale"),
			(call_script, "script_good_price_affects_good_production", ":center_no", "itm_grain", ":base_production", 2),
			(assign, ":modified_production", reg0),
		(else_try),
			(eq, ":cur_good", "itm_dried_meat"),
			(call_script, "script_good_price_affects_good_production", ":center_no", "itm_salt", ":base_production", 2),
			(assign, ":modified_production", reg0),
		(else_try),
			(eq, ":cur_good", "itm_smoked_fish"),
			(call_script, "script_good_price_affects_good_production", ":center_no", "itm_salt", ":base_production", 2),
			(assign, ":modified_production", reg0),
		(else_try),	
			(eq, ":cur_good", "itm_tools"),
			(call_script, "script_good_price_affects_good_production", ":center_no", "itm_iron", ":base_production", 1),
			(assign, ":modified_production", reg0),
		(else_try),	
			(eq, ":cur_good", "itm_wool_cloth"),
			(call_script, "script_good_price_affects_good_production", ":center_no", "itm_wool", ":base_production", 1),
			(assign, ":modified_production", reg0),
		(else_try),	
			(eq, ":cur_good", "itm_wine"),
			(call_script, "script_good_price_affects_good_production", ":center_no", "itm_raw_grapes", ":base_production", 1),
			(assign, ":modified_production", reg0),
		(else_try),	
			(eq, ":cur_good", "itm_oil"),
			(call_script, "script_good_price_affects_good_production", ":center_no", "itm_raw_olives", ":base_production", 1),
			(assign, ":modified_production", reg0),
		(else_try),	
			(eq, ":cur_good", "itm_velvet"),
			(call_script, "script_good_price_affects_good_production", ":center_no", "itm_raw_silk", ":base_production", 1),
			(assign, ":initially_modified_production", reg0),			
			(call_script, "script_good_price_affects_good_production", ":center_no", "itm_raw_dyes", ":initially_modified_production", 2),
			(assign, ":modified_production", reg0),
		(else_try),	
			(eq, ":cur_good", "itm_leatherwork"),
			(call_script, "script_good_price_affects_good_production", ":center_no", "itm_raw_leather", ":base_production", 1),
			(assign, ":modified_production", reg0),
		(else_try),	
			(eq, ":cur_good", "itm_linen"),
			(call_script, "script_good_price_affects_good_production", ":center_no", "itm_raw_flax", ":base_production", 1),
			(assign, ":modified_production", reg0),
		(try_end),
		
		(assign, ":base_production_modded_by_raw_materials", ":modified_production"), #this is just logged for the report screen

	    #Increase both positive and negative production by the center's prosperity
		#Richer towns have more people and consume more, but also produce more 
		(try_begin),
			(party_get_slot, ":prosperity_plus_75", ":center_no", slot_town_prosperity),
			(val_add, ":prosperity_plus_75", 75),
			(val_mul, ":modified_production", ":prosperity_plus_75"),
			(val_div, ":modified_production", 125),
		(try_end),
  
		(try_begin),
		    (this_or_next|party_slot_eq, ":center_no", slot_village_state, svs_being_raided),
		        (party_slot_eq, ":center_no", slot_village_state, svs_looted),
		    (assign, ":modified_production", 0),	
		(try_end),
 
	    (assign, reg0, ":modified_production"), #modded by prosperity
	    (assign, reg1, ":base_production_modded_by_raw_materials"),
	    (assign, reg2, ":base_production"),	  
	]),
  ("center_get_consumption",
    [
		(store_script_param_1, ":center_no"),
		(store_script_param_2, ":cur_good"),

		(assign, ":consumer_consumption", 0),
		(try_begin),
##diplomacy start+ To determine if a center should be counted as a desert center or not,
#instead of using a fixed range (which is brittle to map changes) check if the terrain
#at the center is rt_desert or rt_desert_forest.
			(ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_LOW),
			(is_between, ":center_no", centers_begin, centers_end),
			(party_get_current_terrain, reg0, ":center_no"),
			(this_or_next|eq, reg0, rt_desert),
			(eq, reg0, rt_desert_forest),
			(item_slot_ge, ":cur_good", slot_item_desert_demand, 0), #Otherwise use rural or urban
			(item_get_slot, ":consumer_consumption", ":cur_good", slot_item_desert_demand),
		(else_try),
			(lt, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_LOW),
#If economic changes are disabled, use the Native desert-check logic.
##diplomacy end+
			(this_or_next|is_between, ":center_no", "p_town_19", "p_castle_1"),		
				(ge, ":center_no", "p_village_91"),
			(item_slot_ge, ":cur_good", slot_item_desert_demand, 0), #Otherwise use rural or urban
			(item_get_slot, ":consumer_consumption", ":cur_good", slot_item_desert_demand),
		(else_try),
			(is_between, ":center_no", villages_begin, villages_end),
			(item_get_slot, ":consumer_consumption", ":cur_good", slot_item_rural_demand),
		(else_try),
			(is_between, ":center_no", towns_begin, towns_end),
			(item_get_slot, ":consumer_consumption", ":cur_good", slot_item_urban_demand),
		(try_end),
				
		(assign, ":raw_material_consumption", 0),
		(try_begin),
			(eq, ":cur_good", "itm_grain"),
			(party_get_slot, ":grain_for_bread", ":center_no", slot_center_mills),
			(val_mul, ":grain_for_bread", 20),
			
			(party_get_slot, ":grain_for_ale", ":center_no", slot_center_breweries),
			(val_mul, ":grain_for_ale", 5),
			
			(store_add, ":raw_material_consumption", ":grain_for_bread", ":grain_for_ale"),
			
		(else_try),	
			(eq, ":cur_good", "itm_iron"),
			(party_get_slot, ":raw_material_consumption", ":center_no", slot_center_smithies),
			(val_mul, ":raw_material_consumption", 3),
			
		(else_try),	
			(eq, ":cur_good", "itm_wool"),
			(party_get_slot, ":raw_material_consumption", ":center_no", slot_center_wool_looms),
			(val_mul, ":raw_material_consumption", 5),

		(else_try),	
			(eq, ":cur_good", "itm_raw_flax"),
			(party_get_slot, ":raw_material_consumption", ":center_no", slot_center_linen_looms),
			(val_mul, ":raw_material_consumption", 5),

		(else_try),	
			(eq, ":cur_good", "itm_raw_leather"),
			(party_get_slot, ":raw_material_consumption", ":center_no", slot_center_tanneries),
			(val_mul, ":raw_material_consumption", 20),

		(else_try),	
			(eq, ":cur_good", "itm_raw_grapes"),
			(party_get_slot, ":raw_material_consumption", ":center_no", slot_center_wine_presses),
			(val_mul, ":raw_material_consumption", 30),

		(else_try),	
			(eq, ":cur_good", "itm_raw_olives"),
			(party_get_slot, ":raw_material_consumption", ":center_no", slot_center_olive_presses),
			(val_mul, ":raw_material_consumption", 12),
			
		(else_try),	
			(eq, ":cur_good", "itm_raw_dyes"),
			(party_get_slot, ":raw_material_consumption", ":center_no", slot_center_silk_looms),
			(val_mul, ":raw_material_consumption", 1),

		(else_try),	
			(eq, ":cur_good", "itm_raw_silk"),
			(party_get_slot, ":raw_material_consumption", ":center_no", slot_center_silk_looms),
			(val_mul, ":raw_material_consumption", 5),
			
		(else_try),	
			(eq, ":cur_good", "itm_salt"),
			(party_get_slot, ":salt_for_beef", ":center_no", slot_center_head_cattle),
			(val_div, ":salt_for_beef", 10),
			
			(party_get_slot, ":salt_for_fish", ":center_no", slot_center_fishing_fleet),
			(val_div, ":salt_for_fish", 5),
			
			(store_add, ":raw_material_consumption", ":salt_for_beef", ":salt_for_fish"),
		(try_end),
		
		(try_begin), #Reduce consumption of raw materials if their cost is high
			(gt, ":raw_material_consumption", 0),
			(store_sub, ":item_to_price_slot", slot_town_trade_good_prices_begin, trade_goods_begin),
	        (store_add, ":cur_good_price_slot", ":cur_good", ":item_to_price_slot"),
	        (party_get_slot, ":cur_center_price", ":center_no", ":cur_good_price_slot"),
			##diplomacy start+
			(gt, ":cur_center_price", average_price_factor),#replace the hardcoded constant 1000 with average_price_factor
			(val_mul, ":raw_material_consumption", average_price_factor),#again replace the hardcoded constant 1000 with average_price_factor
			##diplomacy end+
			(val_div, ":raw_material_consumption", ":cur_center_price"),
		(try_end),
				
		(store_add, ":modified_consumption", ":consumer_consumption", ":raw_material_consumption"),
		(try_begin),
			(party_get_slot, ":prosperity_plus_75", ":center_no", slot_town_prosperity),
			(val_add, ":prosperity_plus_75", 75),
			(val_mul, ":modified_consumption", ":prosperity_plus_75"),
			(val_div, ":modified_consumption", 125),
		(try_end),
		

	    (assign, reg0, ":modified_consumption"), #modded by prosperity
	    (assign, reg1, ":raw_material_consumption"),
	    (assign, reg2, ":consumer_consumption"),				
	]),
  #script_get_enterprise_name
  # INPUT: arg1 = item_no
  # Output: reg0: production string
  ("get_enterprise_name",
    [
		(store_script_param_1, ":item_produced"),
		(assign, ":enterprise_name", "str_bread_site"),
		(try_begin),
			(eq, ":item_produced", "itm_bread"),
			(assign, ":enterprise_name", "str_bread_site"),
		(else_try),
			(eq, ":item_produced", "itm_ale"),
			(assign, ":enterprise_name", "str_ale_site"),
		(else_try),
			(eq, ":item_produced", "itm_oil"),
			(assign, ":enterprise_name", "str_oil_site"),
		(else_try),
			(eq, ":item_produced", "itm_wine"),
			(assign, ":enterprise_name", "str_wine_site"),
		(else_try),
			(eq, ":item_produced", "itm_leatherwork"),
			(assign, ":enterprise_name", "str_leather_site"),
		(else_try),
			(eq, ":item_produced", "itm_wool_cloth"),
			(assign, ":enterprise_name", "str_wool_cloth_site"),
		(else_try),
			(eq, ":item_produced", "itm_linen"),
			(assign, ":enterprise_name", "str_linen_site"),
		(else_try),
			(eq, ":item_produced", "itm_velvet"),
			(assign, ":enterprise_name", "str_velvet_site"),
		(else_try),
			(eq, ":item_produced", "itm_tools"),
			(assign, ":enterprise_name", "str_tool_site"),
		(try_end),
		(assign, reg0, ":enterprise_name"),
	]),
  #script_do_merchant_town_trade
  # INPUT: arg1 = party_no (of the merchant), arg2 = center_no
  ##diplomacy start+
  # If optional economic changes are enabled, the benefits are applied to both
  # the town of origin and the destination, instead of just the latter.
  ##diplomacy end+
  ("do_merchant_town_trade",
    [
      (store_script_param_1, ":party_no"),
      (store_script_param_2, ":center_no"),

	  (party_get_slot, ":origin", ":party_no", slot_party_last_traded_center),
	  
	  (try_begin),
		(eq, "$cheat_mode", 2),
		(str_store_party_name, s4, ":center_no"),
		(str_store_party_name, s5, ":origin"),
		(display_message, "@{!}DEBUG -- Caravan trades in {s4}, originally from {s5}"),
	  (try_end),
	  
	  (call_script, "script_add_log_entry", logent_party_traded, ":party_no", ":origin", ":center_no", -1),

      (call_script, "script_do_party_center_trade", ":party_no", ":center_no", 4), #it was first 10 then increased 20 then increased 30, now I decrease it to back 6. Because otherwise prices do not differiate much. Trade become useless in game.
      
      (assign, ":total_change", reg0),
      #Adding the earnings to the wealth (maximum changed price is the earning)
      (val_div, ":total_change", 2),
      (str_store_party_name, s1, ":party_no"),
      (str_store_party_name, s2, ":center_no"),
      (assign, reg1, ":total_change"),

      #Adding tariffs to the town
      (party_get_slot, ":accumulated_tariffs", ":center_no", slot_center_accumulated_tariffs),
      (party_get_slot, ":prosperity", ":center_no", slot_town_prosperity),
	  
	  (assign, ":tariffs_generated", ":total_change"),
      (val_mul, ":tariffs_generated", ":prosperity"),
	  ##diplomacy start+
	  #Move the next two lines further down to reduce rounding error
	  #(val_div, ":tariffs_generated", 100),
	  #(val_div, ":tariffs_generated", 10), #10 for caravans, 20 for villages

	  #Re-wrote the "diplomacy" section here for greater clarity.
	  (assign, ":percent", 100),
      (try_begin), # trade agreement
        (store_faction_of_party, ":party_faction", ":party_no"),
        (store_faction_of_party, ":center_faction", ":center_no"),

        (store_add, ":truce_slot", ":party_faction", slot_faction_truce_days_with_factions_begin),
        (val_sub, ":truce_slot", kingdoms_begin),
  	    (faction_get_slot, ":truce_days", ":center_faction", ":truce_slot"),
  	    ##nested diplomacy start+ replace "20" with a named constant
  	    #(gt, ":truce_days", 20),
  	    (gt, ":truce_days", dplmc_treaty_trade_days_expire),
  	    ##nested diplomacy end+
  	    (val_add, ":percent", 30),
      (try_end),

	  #If economic changes are enabled, divide the tariffs between the source and destination.
	  (assign, ":origin_tariffs_generated", 0),#we will need this variable later, if it is set
	  (try_begin),
	    #Economic changes must be enabled
		(ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_LOW),
		#verify the origin is a real town or village and not a placeholder value
		(ge, ":origin", 0),
		(this_or_next|is_between, ":origin", towns_begin, towns_end),
		(this_or_next|is_between, ":origin", villages_begin, villages_end),
		(this_or_next|party_slot_eq, ":origin", slot_party_type, spt_town),
			(party_slot_eq, ":origin", slot_party_type, spt_village),
		#give half the tariffs to the origin
		(ge, ":tariffs_generated", 0),
		(party_get_slot, ":origin_accumulated_tariffs", ":origin", slot_center_accumulated_tariffs),
		(store_div, ":origin_tariffs_generated", ":tariffs_generated", 2),
		(val_sub, ":tariffs_generated", ":origin_tariffs_generated"),
		#apply plutocracy/aristocracy modifier, and any modifier from a trade treaty
		(store_faction_of_party, ":origin_faction", ":center_no"),
		(faction_get_slot, ":aristocracy", ":origin_faction", dplmc_slot_faction_aristocracy),
        (val_mul, ":aristocracy", -5),
        (store_add, ":origin_percent", ":percent", ":aristocracy"),
		(val_mul, ":origin_tariffs_generated", ":origin_percent"),
		(val_add, ":origin_tariffs_generated", 50),#for rounding
		(val_div, ":origin_tariffs_generated", 100),
		#apply the delayed division from before (leaving the steps separated for clarity)
		(val_add, ":origin_tariffs_generated", 50),
		(val_div, ":origin_tariffs_generated", 100),#adjust for having been multiplied by prosperity
		(val_add, ":tariffs_generated", 5),
		(val_div, ":tariffs_generated", 10), #10 for caravans, 20 for villages
		#now we have the final value of origin_tariffs_generated
		(val_add, ":origin_accumulated_tariffs", ":origin_tariffs_generated"),
		(party_set_slot, ":origin", slot_center_accumulated_tariffs, ":origin_accumulated_tariffs"),
		#print economic debug message if enabled
		(ge, "$cheat_mode", 3),
		(assign, reg4, ":origin_tariffs_generated"),
		(str_store_party_name, s4, ":origin"),
		(assign, reg5, ":origin_accumulated_tariffs"),
		(display_message, "@{!}New tariffs at {s4} = {reg4}, total = {reg5}"),
	  (try_end),

	  #For this town: apply the faction plutocracy/aristocracy modifier
      (faction_get_slot, ":aristocracy", ":center_faction", dplmc_slot_faction_aristocracy),
      (val_mul, ":aristocracy", -5),
      (val_add, ":percent", ":aristocracy"),
      (val_mul, ":tariffs_generated", ":percent"),
   	  (val_add, ":tariffs_generated", 50),
      (val_div, ":tariffs_generated", 100),
	  #apply the delayed division from before (leaving the steps separated for clarity)
   	  (val_add, ":tariffs_generated", 50),
 	  (val_div, ":tariffs_generated", 100),#adjust for having been multiplied by prosperity
	  (val_add, ":tariffs_generated", 5),
	  (val_div, ":tariffs_generated", 10), #10 for caravans, 20 for villages
	  ##diplomacy end+
	  (val_add, ":accumulated_tariffs", ":tariffs_generated"),
	  
	  (try_begin),
		(ge, "$cheat_mode", 3),
		(assign, reg4, ":tariffs_generated"),
		(str_store_party_name, s4, ":center_no"),
		(assign, reg5, ":accumulated_tariffs"),
		(display_message, "@{!}New tariffs at {s4} = {reg4}, total = {reg5}"),
	  (try_end),
	  
      (party_set_slot, ":center_no", slot_center_accumulated_tariffs, ":accumulated_tariffs"),
      ##diplomacy start+
	  #If economic changes are enabled, 50% chance that the origin rather than
	  #the destination will receive the chance for prosperity increase.
	  (assign, ":benefit_center", ":center_no"),
	  (try_begin),
		#Economic changes must be enabled
		(ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_LOW),
		#verify the origin is a real town or village and not a placeholder value
		(ge, ":origin", 0),
		(this_or_next|is_between, ":origin", towns_begin, towns_end),
		(this_or_next|is_between, ":origin", villages_begin, villages_end),
		(this_or_next|party_slot_eq, ":origin", slot_party_type, spt_town),
			(party_slot_eq, ":origin", slot_party_type, spt_village),
		(ge, ":tariffs_generated", 0),
		#50% chance
		(store_random_in_range, ":rand", 0, 64),
		(lt, ":rand", 32),
		(assign, ":benefit_center", ":origin"),
	  (try_end),
	  ##diplomacy end+	  
      #Adding 1 to center prosperity in many circumstances
      (try_begin),
        (store_random_in_range, ":rand", 0, 80),
		##diplomacy start+ in next line, changed center_no to benefit_center
        (call_script, "script_center_get_goods_availability", ":benefit_center"),
		##diplomacy end+
		(assign, ":hardship_index", reg0),
		(gt, ":rand", ":hardship_index"),
	    ##diplomacy start+ in next line, changed center_no to benefit_center
        (call_script, "script_change_center_prosperity", ":benefit_center", 1),
		##diplomacy end+
		(val_add, "$newglob_total_prosperity_from_caravan_trade", 1),
      (try_end),
      #Repeat, but harder
      (try_begin),
        (store_random_in_range, ":rand", -20, 40),
		##diplomacy start+ in next line, changed center_no to benefit_center
        (call_script, "script_center_get_goods_availability", ":benefit_center"),
		##diplomacy end+
		(assign, ":hardship_index", reg0),
		(gt, ":rand", ":hardship_index"),
        ##diplomacy start+ in next line, changed center_no to benefit_center
        (call_script, "script_change_center_prosperity", ":benefit_center", 1),
		##diplomacy end+
		(val_add, "$newglob_total_prosperity_from_caravan_trade", 1),
      (try_end),
      
  ]),
  #OUTPUT:
  # This script may return false if there is no matching town.
  # reg0 = town_no
  ("cf_select_random_town_at_peace_with_faction_in_trade_route",
    [
      (store_script_param, ":town_no", 1),
      (store_script_param, ":faction_no", 2),
      (assign, ":result", -1),
      (assign, ":no_towns", 0),
      (try_for_range, ":cur_slot", slot_town_trade_routes_begin, slot_town_trade_routes_end),
        (party_get_slot, ":cur_town", ":town_no", ":cur_slot"),
        (gt, ":cur_town", 0),
        (store_faction_of_party, ":cur_faction", ":cur_town"),
        (store_relation, ":reln", ":cur_faction", ":faction_no"),
        (ge, ":reln", 0),
        (val_add, ":no_towns", 1),
      (try_end),
      (gt, ":no_towns", 0), #Fail if there are no towns
      (store_random_in_range, ":random_town", 0, ":no_towns"),
      (try_for_range, ":cur_slot", slot_town_trade_routes_begin, slot_town_trade_routes_end),
        (eq, ":result", -1),
        (party_get_slot, ":cur_town", ":town_no", ":cur_slot"),
        (gt, ":cur_town", 0),
        (store_faction_of_party, ":cur_faction", ":cur_town"),
        (store_relation, ":reln", ":cur_faction", ":faction_no"),
        (ge, ":reln", 0),
        (val_sub, ":random_town", 1),
        (lt, ":random_town", 0),
        (assign, ":result", ":cur_town"),
      (try_end),
      (assign, reg0, ":result"),
  ]),
	#the following is a very simple adjustment - it measures the difference in prices between two towns
	#all goods are weighted equally except for luxuries
	#it does not take into account the prices of the goods, nor cargo capacity
	#to do that properly, a merchant would have to virtually fill his baggage, slot by slot, for each town
	#i also found that one needed to introduce demand inelasticity -- prices should vary a lot for grain,  relatively little for iron
    ##diplomacy start+
	#
    #Added a third parameter, the caravan party, for use in distance calculations and perhaps
	#other things in the future.  This may be -1, in which case the script attempts to find a
	#general answer without referring to any specific attributes.  It may also be a town,
	#in which case its position is used for distance calculations.
	##diplomacy end+
  ("cf_select_most_profitable_town_at_peace_with_faction_in_trade_route",
    [
      (store_script_param, ":town_no", 1),
      (store_script_param, ":faction_no", 2),
	  ##diplomacy start+
	  (store_script_param, ":perspective_party", 3),
	  ##diplomacy end+

      (assign, ":result", -1),
	  (assign, ":best_town_score", 0),
      (store_sub, ":item_to_price_slot", slot_town_trade_good_prices_begin, trade_goods_begin),

	  ##diplomacy start+
	  # If economics changes are enabled, the caravan may also take into account the distance
	  # to the destination or bias towards towns of its town faction.
	  (store_random_in_range, ":consider_distance", 0, 2),
	  (store_random_in_range, ":faction_bias", 0, 2),
	  (try_begin),
		(lt, ":perspective_party", 0),
		(assign, ":perspective_party", ":town_no"),
	  (try_end),
      ##diplomacy end+

      (try_for_range, ":cur_slot", slot_town_trade_routes_begin, slot_town_trade_routes_end),
        (party_get_slot, ":cur_town", ":town_no", ":cur_slot"),
        (gt, ":cur_town", 0),
		
        (store_faction_of_party, ":cur_faction", ":cur_town"),
        (store_relation, ":reln", ":cur_faction", ":faction_no"),
        (ge, ":reln", 0),

		(assign, ":cur_town_score", 0),
		(try_for_range, ":cur_goods", trade_goods_begin, trade_goods_end),
			(neq, ":cur_goods", "itm_butter"), #Don't count perishables
			(neq, ":cur_goods", "itm_cattle_meat"),
			(neq, ":cur_goods", "itm_chicken"),
			(neq, ":cur_goods", "itm_pork"),
			
            (store_add, ":cur_goods_price_slot", ":cur_goods", ":item_to_price_slot"),
			(party_get_slot, ":origin_price", ":town_no", ":cur_goods_price_slot"),
			(party_get_slot, ":destination_price", ":cur_town", ":cur_goods_price_slot"),
						
			(gt, ":destination_price", ":origin_price"),
			(store_sub, ":price_dif", ":destination_price", ":origin_price"),
			
			(try_begin), #weight luxury goods double
				(this_or_next|eq, ":cur_goods", "itm_spice"),
					(eq, ":cur_goods", "itm_velvet"),
				(val_mul, ":price_dif", 2),
			(try_end),
			(val_add, ":cur_town_score", ":price_dif"),
		(try_end),
		
##		(try_begin),
##			(eq, "$cheat_mode", 1),
##			(str_store_party_name, s10, ":town_no"),
##			(str_store_party_name, s11, ":cur_town"),
##			(assign, reg3, ":cur_town_score"),
##			(display_message, "str_caravan_in_s10_considers_s11_total_price_dif_=_reg3"),
##		(try_end),

        ##diplomacy start+
		(try_begin),
			#Economic changes must be enabled, or the player must have decided
			#to use mercantilism settings (which expresses a desire to see changes
			#related to that setting applied), or a trade treaty must be in effect.
			(this_or_next|neg|faction_slot_eq, "fac_player_supporters_faction", dplmc_slot_faction_mercantilism, 0),
			(ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_LOW),
			#Take into account distance, or treat factions preferentially
			(try_begin),
				#Bias towards own faction
				(ge, ":faction_bias", 1),
				(neq, ":faction_no", ":cur_faction"),

				##The penalty is based on the source faction's mercantilism rating, as well as
				##the other faction's mercantilism rating.
				(faction_get_slot, ":source_mercantilism", ":faction_no", dplmc_slot_faction_mercantilism),
				(val_clamp, ":source_mercantilism", -3, 4),
				(faction_get_slot, ":dest_mercantilism", ":cur_faction", dplmc_slot_faction_mercantilism),
				(val_clamp, ":dest_mercantilism", -3, 4),
				##Default (if both factions have mercantilism 0) is a 6% reduction.  Possible range is 0% (least) to 12% (most).
				(store_sub, ":percent", 94, ":source_mercantilism"),
				(val_sub, ":percent", ":dest_mercantilism"),

				(val_mul, ":cur_town_score", ":percent"),
				(val_add, ":cur_town_score", 50),
				(val_div, ":cur_town_score", 100),
			(try_end),
			(try_begin),
				(ge, ":consider_distance", 1),#consider distance
				(store_distance_to_party_from_party, ":dist", ":perspective_party",":cur_town"),
				#Avoid asymptotic effects and undue weighting.
				#Further explanation: What we really care about is time, not distance.
				#It will take time to buy and sell once reaching our destination: halving
				#the distance doesn't double the expected profit per month.
				(val_max, ":dist", 0),
				(val_add, ":dist", 12),
				#Avoid possible problems trying to compare distant towns
				(val_mul, ":cur_town_score", 100),
				(val_div, ":cur_town_score", ":dist"),
			(try_end),
		(try_end),
		##diplomacy end+
		
		(gt, ":cur_town_score", ":best_town_score"),
		(assign, ":best_town_score", ":cur_town_score"),
		(assign, ":result", ":cur_town"),
		
	  (try_end),

      (gt, ":result", -1), #Fail if there are no towns

      (assign, reg0, ":result"),

#	  (store_current_hours, ":hour"),
#	  (party_set_slot, ":result", slot_town_caravan_last_visit, ":hour"),

##	  (try_begin),
##		(eq, "$cheat_mode", 1),
##	    (assign, reg3, ":best_town_score"),
##	    (str_store_party_name, s3, ":town_no"),
##	    (str_store_party_name, s4, ":result"),
##	    (display_message, "str_test__caravan_in_s3_selects_for_s4_trade_score_reg3"),
##	  (try_end),
	  
  ]),
  # script_center_get_food_consumption
  # Input: arg1 = center_no
  # Output: reg0: food consumption (1 food item counts as 100 units)
  ("center_get_food_consumption",
    [
      (store_script_param_1, ":center_no"),
      (assign, ":food_consumption", 0),
      (try_begin),
        (party_slot_eq, ":center_no", slot_party_type, spt_town),
        (assign, ":food_consumption", 500),
      (else_try),
        (party_slot_eq, ":center_no", slot_party_type, spt_castle),
        (assign, ":food_consumption", 50),
      (try_end),
      ##diplomacy start+
      (try_begin),
         (ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_MEDIUM),
		 #Optional change: increase food consumption with garrison size
		 #The rationale goes like this:
		 #The average reinforcement size for a town or castle is 9.5 per round.
		 #At the start of the game:
		 #
		 #  Castles get 15 reinforcement rounds, for around 142.5 troops
		 #  Towns   get 40 reinforcement rounds, for around 380 troops
		 #
		 #Of course both the castles and the towns have other people living
		 #there as well.
		 (party_get_num_companions, ":garrison_size", ":center_no"),
		 (try_begin),
			(party_slot_eq, ":center_no", slot_party_type, spt_castle),
			#gekokujo 3.0 increased garrison sizes start
			#(gt, ":garrison_size", 150),
			##Assume that the garrison accounts for most of the food consumption.
			#(store_div, ":food_consumption", ":garrison_size", 3),
			(store_faction_of_party, ":faction_id", ":center_no"),
			(try_begin),
				(eq, ":faction_id", "fac_kingdom_20"),
				(gt, ":garrison_size", 237),
				(store_div, ":food_consumption", ":garrison_size", 3),
			(else_try),
				(gt, ":garrison_size", 190),
				(store_div, ":food_consumption", ":garrison_size", 3),
			(try_end),
			#gekokujo 3.0 increased garrison sizes end
		 (else_try),
			(party_slot_eq, ":center_no", slot_party_type, spt_town),
			#gekokujo 3.0 increased garrison sizes start
			##Assume that the garrison accounts for most of the food consumption.
			#(gt, ":garrison_size", 380),
			##Assume that the garrison makes the same contribution to size for towns.
			#(store_div, ":food_consumption", ":garrison_size", 3),#for 381, equals 127
			#(val_add, ":food_consumption", 500 - 127),
			(store_faction_of_party, ":faction_id", ":center_no"),
			(try_begin),
				(eq, ":faction_id", "fac_kingdom_20"),
				(gt, ":garrison_size", 475),
				(store_div, ":food_consumption", ":garrison_size", 3),#for 475, equals 158
				(val_add, ":food_consumption", 500 - 158),
			(else_try),
				(gt, ":garrison_size", 617),
				(store_div, ":food_consumption", ":garrison_size", 3),#for 617, equals 206
				(val_add, ":food_consumption", 500 - 206),
			(try_end),
			#gekokujo 3.0 increased garrison sizes end
		 (try_end),

		 #Optional change: increase food consumption with prosperity
		 (party_slot_eq, ":center_no", slot_party_type, spt_town),
         (party_get_slot, reg0, ":center_no", slot_town_prosperity),
			(gt, reg0, 50),#<- increase only
         (val_add, reg0, 75),
         (val_mul, ":food_consumption", reg0),
         (val_add, ":food_consumption", 62),
         (val_div, ":food_consumption", 125),
      (try_end),
      ##diplomacy+
      (assign, reg0, ":food_consumption"),
  ]),
  # script_center_get_food_store_limit
  # Input: arg1 = center_no
  # Output: reg0: food consumption (1 food item counts as 100 units)
  ("center_get_food_store_limit",
    [
      (store_script_param_1, ":center_no"),
      (assign, ":food_store_limit", 0),
      (try_begin),
        (party_slot_eq, ":center_no", slot_party_type, spt_town),
        (assign, ":food_store_limit", 50000),
      (else_try),
        (party_slot_eq, ":center_no", slot_party_type, spt_castle),
        (assign, ":food_store_limit", 1500),
      (try_end),
      (assign, reg0, ":food_store_limit"),
  ]),
  # script_refresh_village_merchant_inventory
  # Input: arg1 = village_no
  # Output: none
  ("refresh_village_merchant_inventory",
    [
      (store_script_param_1, ":village_no"),
      (party_get_slot, ":merchant_troop", ":village_no", slot_town_elder),
      (reset_item_probabilities,0),
	  
	  #gekokujo 3.0 forgot to integrate start
	  (party_get_slot, ":bound_center", ":village_no", slot_village_bound_center),
	  #gekokujo 3.0 forgot to integrate end

	  (assign, ":total_probability", 0),
      (try_for_range, ":cur_goods", trade_goods_begin, trade_goods_end),
	    (call_script, "script_center_get_production", ":village_no", ":cur_goods"),
		(assign, ":cur_probability", reg0),

		#gekokujo 3.0 forgot to integrate start
		(call_script, "script_center_get_production", ":bound_center", ":cur_goods"),
		(val_div, reg0, 5), #also add 1/5 of bound center production to village's inventory.
		(val_add, ":cur_probability", reg0),  
		#gekokujo 3.0 forgot to integrate end
		
		(val_max, ":cur_probability", 5),	  	
		(val_add, ":total_probability", ":cur_probability"),
      (try_end),
	  
	  (try_begin),
		(party_get_slot, ":prosperity", ":village_no", slot_town_prosperity),
		(val_div, ":prosperity", 15), #up to 6
		(store_add, ":number_of_items_in_village", ":prosperity", 1),
	  (try_end),

      (try_for_range, ":cur_goods", trade_goods_begin, trade_goods_end),
	    (call_script, "script_center_get_production", ":village_no", ":cur_goods"),
		(assign, ":cur_probability", reg0),
		
		#gekokujo 3.0 forgot to integrate start
		(call_script, "script_center_get_production", ":bound_center", ":cur_goods"),
		(val_div, reg0, 5), #also add 1/5 of bound center production to village's inventory.
		(val_add, ":cur_probability", reg0),
		#gekokujo 3.0 forgot to integrate end

		(val_max, ":cur_probability", 5),

        (val_mul, ":cur_probability", ":number_of_items_in_village"),
		(val_mul, ":cur_probability", 100),
		(val_div, ":cur_probability", ":total_probability"),

        (set_item_probability_in_merchandise, ":cur_goods", ":cur_probability"),
      (try_end),

      (troop_clear_inventory, ":merchant_troop"),
      (troop_add_merchandise, ":merchant_troop", itp_type_goods, ":number_of_items_in_village"),
      (troop_ensure_inventory_space, ":merchant_troop", 80),

      #Adding 1 prosperity to the village while reducing each 3000 gold from the elder
      (store_troop_gold, ":gold",":merchant_troop"),
      (try_begin),
        (gt, ":gold", 3500),
        (store_div, ":prosperity_added", ":gold", 3000),
        (store_mul, ":gold_removed", ":prosperity_added", 3000),
        (troop_remove_gold, ":merchant_troop", ":gold_removed"),
        (call_script, "script_change_center_prosperity", ":village_no", ":prosperity_added"),
      (try_end),
  ]),
  #script_do_party_center_trade
  # INPUT: arg1 = party_no, arg2 = center_no, arg3 = percentage_change_in_center
  # OUTPUT: reg0 = total_change
  ("do_party_center_trade",
    [	  
      (store_script_param, ":party_no", 1),
      (store_script_param, ":center_no", 2),

      (try_begin),
	    (eq, "$cheat_mode", 3),
	    (str_store_party_name, s1, ":center_no"),
	    (display_message, "@{!}DEBUG : {s1} is trading with villagers"),
      (try_end),

      (store_script_param, ":percentage_change", 3), #this should probably always be a constant. Currently it is 25.


	  ##diplomacy start+
	  (party_get_slot, ":origin", ":party_no", slot_party_last_traded_center),
	  #If optional economic changes are enabled, reduce the percentage change in order
	  #to make prices feel less static.
	  (try_begin),
		(ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_LOW),
		#Only apply lessened price movements to towns.
		(this_or_next|party_slot_eq, ":center_no", slot_party_type, spt_town),
			(is_between, ":center_no", towns_begin, towns_end),
		#This halves the average impact as well as making it more variable.
		(val_add, ":percentage_change", 1),
		(store_random_in_range, ":percentage_change", 0, ":percentage_change"),
		#Display economics diagnostic
		(ge, "$cheat_mode", 3),
		(str_store_party_name, s3, ":origin"),
		(str_store_party_name, s4, ":center_no"),
		(assign, reg4, ":percentage_change"),
		(display_message, "@{!}DEBUG -- Trade from {s3} to {s4}: rolled random impact of {reg4}"),
	  (try_end),
	  ##diplomacy end+

	  (party_get_slot, ":origin", ":party_no", slot_party_last_traded_center),
	  (party_set_slot, ":party_no", slot_party_last_traded_center, ":center_no"),
	  ##diplomacy start+
	  #Update the record of trade route arrival times
      (try_begin),
         (ge, ":origin", centers_begin),
    	 ##zerilius changes begin
    	 # (this_or_next|party_slot_eq, ":origin", villages_begin, villages_end),
    	 (this_or_next|party_slot_eq, ":origin", slot_party_type, spt_village),
    	 ##zerilius changes end
         (is_between, ":origin", villages_begin, villages_end),
         (store_current_hours, ":cur_hours"),
         (party_set_slot, ":origin", dplmc_slot_village_trade_last_arrived_to_market, ":cur_hours"),
      (try_end),
      (try_begin),
	     (ge, ":origin", centers_begin),
		 (this_or_next|party_slot_eq, ":center_no", slot_party_type, spt_town),
			(is_between, ":center_no", towns_begin, towns_end),
		 (store_current_hours, ":cur_hours"),
		 (try_for_range, ":trade_route_slot", slot_town_trade_routes_begin, slot_town_trade_routes_end),
            (party_slot_eq,  ":center_no", ":trade_route_slot", ":origin"),
			(store_sub, ":trade_route_arrival_slot", ":trade_route_slot", slot_town_trade_routes_begin),
			(val_add, ":trade_route_arrival_slot", dplmc_slot_town_trade_route_last_arrivals_begin),
			(is_between, ":trade_route_arrival_slot", dplmc_slot_town_trade_route_last_arrivals_begin, dplmc_slot_town_trade_route_last_arrivals_end),#this will always be true unless a modder increased the number of trade route slots without increasing the number of last arrival slots
			(party_set_slot, ":center_no", ":trade_route_arrival_slot", ":cur_hours"),
         (try_end),
         (else_try),
            (this_or_next|party_slot_eq, ":center_no", slot_party_type, spt_village),
               (is_between, ":center_no", villages_begin, villages_end),
         (store_current_hours, ":cur_hours"),
         (party_set_slot, ":center_no", dplmc_slot_village_trade_last_returned_from_market, ":cur_hours"),
	  (try_end),
	  ##diplomacy end+
	  
      (assign, ":total_change", 0),
      (store_sub, ":item_to_price_slot", slot_town_trade_good_prices_begin, trade_goods_begin),
      (try_for_range, ":cur_good", trade_goods_begin, trade_goods_end),
        (store_add, ":cur_good_price_slot", ":cur_good", ":item_to_price_slot"),
        (party_get_slot, ":cur_merchant_price", ":party_no", ":cur_good_price_slot"),
        (party_get_slot, ":cur_center_price", ":center_no", ":cur_good_price_slot"),
        (store_sub, ":price_dif", ":cur_merchant_price", ":cur_center_price"),
        (assign, ":cur_change", ":price_dif"),
        (val_abs, ":cur_change"),
        (val_add, ":total_change", ":cur_change"),
        (val_mul, ":cur_change", ":percentage_change"),
        (val_div, ":cur_change", 100),
		
		#This is to reconvert from absolute value
        (try_begin),
          (lt, ":price_dif", 0),
          (val_mul, ":cur_change", -1),
        (try_end),

		(assign, ":initial_price", ":cur_center_price"),

		#The new price for the caravan or peasant is set before the change, so the prices in the trading town have full effect on the next center         
		(party_set_slot, ":party_no", ":cur_good_price_slot", ":cur_center_price"),
		
        (val_add, ":cur_center_price", ":cur_change"),       
		(party_set_slot, ":center_no", ":cur_good_price_slot", ":cur_center_price"),
				
		(try_begin),
			(eq, "$cheat_mode", 3),
			(str_store_party_name, s3, ":origin"),
			(str_store_party_name, s4, ":center_no"),
			(str_store_item_name, s5, ":cur_good"),
			(assign, reg4, ":initial_price"),
			(assign, reg5, ":cur_center_price"),
			(display_log_message, "@{!}DEBUG -- Trade of {s5} from {s3} to {s4} brings price from {reg4} to {reg5}"),
		(try_end),
		
      (try_end),
      (assign, reg0, ":total_change"),
  ]),
  #script_update_village_market_towns
  # INPUT: none
  # OUTPUT: none
  ("update_village_market_towns",
    [(try_for_range, ":cur_village", villages_begin, villages_end),
       (store_faction_of_party, ":village_faction", ":cur_village"),
       (assign, ":min_dist", 999999),
       (assign, ":min_dist_town", -1),
       (try_for_range, ":cur_town", towns_begin, towns_end),
         (store_faction_of_party, ":town_faction", ":cur_town"),
         (eq, ":town_faction", ":village_faction"),
         (store_distance_to_party_from_party, ":cur_dist", ":cur_village", ":cur_town"),
         (lt, ":cur_dist", ":min_dist"),
         (assign, ":min_dist", ":cur_dist"),
         (assign, ":min_dist_town", ":cur_town"),
       (try_end),
	   
	   (try_begin),
		(gt, ":min_dist_town", -1),
		(party_set_slot, ":cur_village", slot_village_market_town, ":min_dist_town"),
	   (else_try),
		(assign, ":min_dist", 999999),
		(assign, ":min_dist_town", -1),
		(try_for_range, ":cur_town", towns_begin, towns_end),
			(store_faction_of_party, ":town_faction", ":cur_town"),
			(store_relation, ":relation", ":town_faction", ":village_faction"),
			(ge, ":relation", 0),
			(store_distance_to_party_from_party, ":cur_dist", ":cur_village", ":cur_town"),
			(lt, ":cur_dist", ":min_dist"),
			(assign, ":min_dist", ":cur_dist"),
			(assign, ":min_dist_town", ":cur_town"),
		(try_end),
		(gt, ":min_dist_town", -1),
		(party_set_slot, ":cur_village", slot_village_market_town, ":min_dist_town"),
	   (try_end),
     (try_end),
     ]),
  #script_change_center_prosperity
  # INPUT: arg1 = center_no, arg2 = difference
  # OUTPUT: none
  ("change_center_prosperity",
    [(store_script_param, ":center_no", 1),
     (store_script_param, ":difference", 2),
     (party_get_slot, ":old_prosperity", ":center_no", slot_town_prosperity),
     (store_add, ":new_prosperity", ":old_prosperity", ":difference"),
     (val_clamp, ":new_prosperity", 0, 100),
     (store_div, ":old_state", ":old_prosperity", 20),
     (store_div, ":new_state", ":new_prosperity", 20),
	 
     (try_begin),
       (neq, ":old_state", ":new_state"),
	   (neg|is_between, ":center_no", castles_begin, castles_end),
	   
       (str_store_party_name_link, s2, ":center_no"),
       (call_script, "script_get_prosperity_text_to_s50", ":center_no"),
       (str_store_string, s3, s50),
       (party_set_slot, ":center_no", slot_town_prosperity, ":new_prosperity"),
       (call_script, "script_get_prosperity_text_to_s50", ":center_no"),
       (str_store_string, s4, s50),
       (try_begin),
         (party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
         (display_message, "@Prosperity of {s2} has changed from {s3} to {s4}."),
       (try_end),
       (call_script, "script_update_center_notes", ":center_no"),
     (else_try),
       (party_set_slot, ":center_no", slot_town_prosperity, ":new_prosperity"),
     (try_end),
	 
	 (try_begin),
		(store_current_hours, ":hours"),
		(gt, ":hours", 1),
		(store_sub, ":actual_difference", ":new_prosperity", ":old_prosperity"),
		(try_begin),
			(lt, ":actual_difference", 0),
			(val_add, "$newglob_total_prosperity_losses", ":actual_difference"),
	    (else_try),
			(gt, ":actual_difference", 0),
			(val_add, "$newglob_total_prosperity_gains", ":actual_difference"),
		(try_end),
	 (try_end),
	 
	 #This will add up all non-trade prosperity
	 (try_begin),
		(eq, "$cheat_mode", 3),
		(assign, reg4, "$newglob_total_prosperity_from_bandits"), 
		(assign, reg5, "$newglob_total_prosperity_from_caravan_trade"),	 
	    (assign, reg7, "$newglob_total_prosperity_from_villageloot"), 
	    (assign, reg8, "$newglob_total_prosperity_from_townloot"),	 
	    (assign, reg9, "$newglob_total_prosperity_from_village_trade"),
	    (assign, reg10, "$newglob_total_prosperity_from_convergence"),
	    (assign, reg11, "$newglob_total_prosperity_losses"),
	    (assign, reg12, "$newglob_total_prosperity_gains"),
		(display_message, "@{!}DEBUG: Total prosperity actual losses: {reg11}"),
		(display_message, "@{!}DEBUG: Total prosperity actual gains: {reg12}"),
		
		(display_message, "@{!}DEBUG: Prosperity changes from random bandits: {reg4}"),
		(display_message, "@{!}DEBUG: Prosperity changes from caravan trades: {reg5}"),
		(display_message, "@{!}DEBUG: Prosperity changes from farmer trades: {reg9}"),
		(display_message, "@{!}DEBUG: Prosperity changes from looted villages: {reg7}"),
		(display_message, "@{!}DEBUG: Prosperity changes from sieges: {reg8}"),
		(display_message, "@{!}DEBUG: Theoretical prosperity changes from convergence: {reg10}"),
	 (try_end),
	 
     ]),
  #script_get_center_ideal_prosperity
  # INPUT: arg1 = center_no
  # OUTPUT: reg0 = ideal_prosperity
  ("get_center_ideal_prosperity",
    [(store_script_param, ":center_no", 1),
     (assign, ":ideal", 65),

     (call_script, "script_center_get_goods_availability", ":center_no"),
     (store_mul, ":hardship_index", reg0, 2),
     (val_sub, ":ideal", ":hardship_index"),	 

     (try_begin),
       (is_between, ":center_no", villages_begin, villages_end),
       (party_slot_eq, ":center_no", slot_center_has_fish_pond, 1),
       (val_add, ":ideal", 5),
     (try_end),

     (val_max, ":ideal", 0),
	
     (assign, reg0, ":ideal"),
     ]),
  ("good_price_affects_good_production",
	[
	(store_script_param, ":center", 1),	 
	(store_script_param, ":input_item_no", 2),	 
	(store_script_param, ":production", 3),	 
	(store_script_param, ":impact_divisor", 4),	 

	(assign, reg4, ":production"),
	
	(try_begin),
		(gt, ":production", 0), #let's take -20 as the zero production rate, although in actuality production can go lower, representing increased demand
	
		(store_sub, ":input_good_price_slot", ":input_item_no", trade_goods_begin),
		(val_add, ":input_good_price_slot", slot_town_trade_good_prices_begin),
		(party_get_slot, ":input_price", ":center", ":input_good_price_slot"),

		(try_begin),
		  (is_between, ":center", towns_begin, towns_end),

		  (val_mul, ":input_price", 4),
		  (assign, ":number_of_villages", 4),
		  (try_for_range, ":village_no", villages_begin, villages_end),
		    (party_slot_eq, ":village_no", slot_village_bound_center, ":center"),
		    (party_get_slot, ":input_price_at_village", ":village_no", ":input_good_price_slot"),
			(val_add, ":input_price", ":input_price_at_village"),
			(val_add, ":number_of_villages", 1),
		  (try_end),		  

		  (val_div, ":input_price", ":number_of_villages"),
		(try_end),
		
		(try_begin), #1/2 impact for low prices
			##diplomacy start+
			(lt, ":input_price", average_price_factor),#Replace 1000 with average_price_factor
			##diplomacy end+
			(val_mul, ":impact_divisor", 2),
		(try_end),
		
		(try_begin),
			(gt, ":impact_divisor", 1),
			##diplomacy start+
			(val_sub, ":input_price", average_price_factor),#Replace 1000 with average_price_factor
			(val_div, ":input_price", ":impact_divisor"),#<- unchanged
			(val_add, ":input_price", average_price_factor),#Replace 1000 with average_price_factor
			##diplomacy end+
		(try_end),

		##diplomacy start+
		(val_mul, ":production", average_price_factor),#Replace 1000 with average_price_factor
		##diplomacy end+
		(val_div, ":production", ":input_price"),
	
		#(assign, reg5, ":production"),
		#(assign, reg3, ":input_price"),
		#(str_store_item_name, s4, ":input_item_no"),
		#(display_message, "@{s4} price of {reg3} reduces production from {reg4} to {reg5}"),		
	(try_end),
				
	(assign, reg0, ":production"),	
	]),
  #script_get_poorest_village_of_faction
  # INPUT: arg1 = center_no
  # OUTPUT: reg0 = ideal_prosperity
  ("get_poorest_village_of_faction",
    [(store_script_param, ":faction_no", 1),
     (assign, ":min_prosperity_village", -1),
     (assign, ":min_prosperity", 101),
     (try_for_range, ":village_no", villages_begin, villages_end),
       (store_faction_of_party, ":village_faction", ":village_no"),
       (eq, ":village_faction", ":faction_no"),
       (party_get_slot, ":prosperity", ":village_no", slot_town_prosperity),
       (lt, ":prosperity", ":min_prosperity"),
       (assign, ":min_prosperity", ":prosperity"),
       (assign, ":min_prosperity_village", ":village_no"),
     (try_end),
     (assign, reg0, ":min_prosperity_village"),
     ]),
	#it might be easier to monitor whether prices are following an intuitive pattern if we separate production from consumption
	#the current system still works very well, however
	("center_get_item_consumption",
    [
	]),
	("center_get_goods_availability", 
	[
	(store_script_param, ":center_no", 1),

	(str_store_party_name, s4, ":center_no"),
	##diplomacy start+ Determine whether the center should use "desert" consumption values.
  	#Native uses the following logic:
	#  (this_or_next|is_between, ":center_no", "p_town_19", "p_castle_1"),
	#  (ge, ":center_no", "p_village_91"),
	##This is very vulnerable to map changes, though, so I would prefer to check the terrain type.
	(party_get_current_terrain, ":terrain_type", ":center_no"),
	(try_begin),
	   (eq, reg0, rt_desert_forest),
	   (assign, ":terrain_type", rt_desert),
	(try_end),
	(try_begin),
	   (lt, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_LOW),
	   #To be consistent with script_center_get_consumption and script_initialize_economic_information
	   #use the Native desert-determination scheme when economic changes are disabled.
	   (assign, ":terrain_type", rt_plain),
  	   (this_or_next|is_between, ":center_no", "p_town_19", "p_castle_1"),
	   (ge, ":center_no", "p_village_91"),
	   (assign, ":terrain_type", rt_desert),
	(try_end),
	##diplomacy end+

	(assign, ":hardship_index", 0),
	(try_for_range, ":cur_good", trade_goods_begin, trade_goods_end),		
		#Must have consumption of at least 4 to be relevant
		#This prevents perishables and raw materials from having a major impact
		(try_begin),
		##diplomacy start+ Use the "desert" slot when applicable
			(ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_LOW),
			(eq, ":terrain_type", rt_desert),
			(item_slot_ge, ":cur_good", slot_item_desert_demand, 0), #Otherwise use rural or urban
			(item_get_slot, ":consumer_consumption", ":cur_good", slot_item_desert_demand),
		(else_try),
		##diplomacy end+
			(is_between, ":center_no", villages_begin, villages_end),
			(item_get_slot, ":consumer_consumption", ":cur_good", slot_item_rural_demand),
		(else_try),
			(item_get_slot, ":consumer_consumption", ":cur_good", slot_item_urban_demand),
		(try_end),
		(gt, ":consumer_consumption", 2),
				
		(store_div, ":max_impact", ":consumer_consumption", 4), #was 4, dropped 3 again 4 now
		
		#High-demand items like grain tend to have much more dramatic price differentiation, so they yield substantially higher results than low-demand items
		
        (store_sub, ":cur_good_price_slot", ":cur_good", trade_goods_begin),
        (val_add, ":cur_good_price_slot", slot_town_trade_good_prices_begin),
        (party_get_slot, ":price", ":center_no", ":cur_good_price_slot"),
		
		(store_sub, ":price_differential", ":price", 1000),
		(gt, ":price_differential", 200), #was 100

		(val_div, ":price_differential", 200),
		(val_min, ":price_differential", ":max_impact"),
		
		(val_add, ":hardship_index", ":price_differential"),
	(try_end),
	
	(assign, reg0, ":hardship_index"),

	(try_begin),
		(eq, "$cheat_mode", 1),
		(display_message, "@{!}DEBUG -- hardship index for {s4} = {reg0}"),
	(try_end),	
	]),
	("process_player_enterprise",
    #reg0: Profit per cycle
	##diplomacy start+
	#Actual documentation of original parameters and outputs.
	# INPUTS:
	#   arg1: item_type
	#   arg2: center
	# OUTPUTS:
    #   reg0:  profit_per_cycle"),
	#   reg1:  final_price_for_total_produced_goods"),
	#   reg2:  final_price_for_total_inputs"),
	#   reg3:  price_of_labor"),
	#   reg4:  final_price_for_single_produced_good"),
	#   reg5:  final_price_for_single_input"),
	#	reg10: final_price_for_secondary_input"),
	#
	# Further, if experimental changes are enabled, modify the price.
	##diplomacy end+
	[
	  (store_script_param, ":item_type", 1),
	  (store_script_param, ":center", 2),
	  
	  (item_get_slot, ":price_of_labor", ":item_type", slot_item_overhead_per_run),
	  
	  (item_get_slot, ":base_price", ":item_type", slot_item_base_price),
	  (store_sub, ":cur_good_price_slot", ":item_type", trade_goods_begin),
	  (val_add, ":cur_good_price_slot", slot_town_trade_good_prices_begin),
	  (party_get_slot, ":cur_price_modifier", ":center", ":cur_good_price_slot"),
	  ##diplomacy start+
	  (val_clamp, ":cur_price_modifier", minimum_price_factor, maximum_price_factor + 1),#Added enforcement of minimum/maximum
	  (store_mul, ":final_price_for_single_produced_good", ":base_price", ":cur_price_modifier"),#<- (Unchanged)
	  (val_div, ":final_price_for_single_produced_good", average_price_factor),#Replaced "1000" with "average_price_factor"
	  ##diplomacy end+
	  (item_get_slot, ":number_of_outputs_produced", ":item_type", slot_item_output_per_run),
	  (store_mul, ":final_price_for_total_produced_goods", ":number_of_outputs_produced", ":final_price_for_single_produced_good"),
	  
	  (item_get_slot, ":primary_raw_material", ":item_type", slot_item_primary_raw_material),
	  (item_get_slot, ":base_price", ":primary_raw_material", slot_item_base_price),
	  (store_sub, ":cur_good_price_slot", ":primary_raw_material", trade_goods_begin),
	  (val_add, ":cur_good_price_slot", slot_town_trade_good_prices_begin),
	  (party_get_slot, ":cur_price_modifier", ":center", ":cur_good_price_slot"),
	  ##diplomacy start+
	  (try_begin),
	     (ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_MEDIUM),#<-- experimental changes must be enabled
		 (call_script, "script_dplmc_assess_ability_to_purchase_good_from_center", ":primary_raw_material", ":center"),
		 (val_max, ":cur_price_modifier", reg0),
	  (try_end),
	  (val_clamp, ":cur_price_modifier", minimum_price_factor, maximum_price_factor + 1),#Added enforcement of minimum/maximum
	  (store_mul, ":final_price_for_single_input", ":base_price", ":cur_price_modifier"),#<- (Unchanged)
	  (val_div, ":final_price_for_single_input", average_price_factor),#Replaced "1000" with "average_price_factor"
	  ##diplomacy end+
	  (item_get_slot, ":number_of_inputs_required", ":item_type", slot_item_input_number),
	  (try_begin),
	    (lt, ":number_of_inputs_required", 0),
	    (store_div, ":final_price_for_total_inputs", ":final_price_for_single_input", 2),
	  (else_try),
	    (store_mul, ":final_price_for_total_inputs", ":final_price_for_single_input", ":number_of_inputs_required"),
	  (try_end),
	  
	  (try_begin),
	    (item_slot_ge, ":item_type", slot_item_secondary_raw_material, 1),
	    (item_get_slot, ":secondary_raw_material", ":item_type", slot_item_secondary_raw_material),	  	  
	    (item_get_slot, ":base_price", ":secondary_raw_material", slot_item_base_price),
	    (store_sub, ":cur_good_price_slot", ":secondary_raw_material", trade_goods_begin),
	    (val_add, ":cur_good_price_slot", slot_town_trade_good_prices_begin),
	    (party_get_slot, ":cur_price_modifier", ":center", ":cur_good_price_slot"),
		##diplomacy start+
		(try_begin),
	      (ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_MEDIUM),#<-- experimental changes must be enabled
		  (call_script, "script_dplmc_assess_ability_to_purchase_good_from_center", ":secondary_raw_material", ":center"),
		  (val_max, ":cur_price_modifier", reg0),
	    (try_end),
	    (val_clamp, ":cur_price_modifier", minimum_price_factor, maximum_price_factor + 1),#Added enforcement of minimum/maximum
		##diplomacy end+

	    (try_begin),
	      (lt, ":number_of_inputs_required", 0),
	      (store_div, ":final_price_for_secondary_input", ":final_price_for_secondary_input", 2),
	    (else_try),
	      (store_mul, ":final_price_for_secondary_input", ":final_price_for_secondary_input", ":number_of_inputs_required"),
	    (try_end),

	    (store_mul, ":final_price_for_secondary_input", ":base_price", ":cur_price_modifier"),
		##diplomacy start+
	    (val_div, ":final_price_for_secondary_input", average_price_factor),#Replaced "1000" with "average_price_factor"
		##diplomacy end+
	  (else_try),
	    (assign, ":final_price_for_secondary_input", 0),
	  (try_end),
	  
	  (store_sub, ":profit_per_cycle", ":final_price_for_total_produced_goods", ":final_price_for_total_inputs"),
	  (val_sub, ":profit_per_cycle", ":price_of_labor"),
	  (val_sub, ":profit_per_cycle", ":final_price_for_secondary_input"),
	  
	  (assign, reg0, ":profit_per_cycle"),
	  (assign, reg1, ":final_price_for_total_produced_goods"),
	  (assign, reg2, ":final_price_for_total_inputs"),
	  (assign, reg3, ":price_of_labor"),
	  (assign, reg4, ":final_price_for_single_produced_good"),
	  (assign, reg5, ":final_price_for_single_input"),
	  (assign, reg10, ":final_price_for_secondary_input"),
	]),
  # script_refresh_center_inventories
  ("refresh_center_inventories",
  [   	
    (set_merchandise_modifier_quality,150),
    (reset_item_probabilities,100),	    

    # Add trade goods to merchant inventories
    (try_for_range,":cur_center",towns_begin, towns_end),
      (party_get_slot,":cur_merchant",":cur_center",slot_town_merchant),
      (reset_item_probabilities,100),
      (assign, ":total_production", 0),
      (try_for_range, ":cur_goods", trade_goods_begin, trade_goods_end),
        (call_script, "script_center_get_production", ":cur_center", ":cur_goods"),
		(assign, ":cur_production", reg0),

        (try_for_range, ":cur_village", villages_begin, villages_end),
		  (party_slot_eq, ":cur_village", slot_village_bound_center, ":cur_center"),
          (call_script, "script_center_get_production", ":cur_village", ":cur_goods"),
		  (val_div, reg0, 3),
		  (val_add, ":cur_production", reg0),
		(try_end),		

		(val_max, ":cur_production", 1),
		(val_mul, ":cur_production", 4),

		(val_add, ":total_production", ":cur_production"),
      (try_end),

	  (party_get_slot, ":town_prosperity", ":cur_center", slot_town_prosperity),
	  (assign, ":number_of_items_in_town", 25),

	  (try_begin), #1.0x - 2.0x (50 - 100 prosperity)
	    (ge, ":town_prosperity", 50),
		(store_sub, ":ratio", ":town_prosperity", 50),
		(val_mul, ":ratio", 2),
		(val_add, ":ratio", 100),
		(val_mul, ":number_of_items_in_town", ":ratio"),
		(val_div, ":number_of_items_in_town", 100),
	  (else_try), #0.5x - 1.0x (0 - 50 prosperity)
		(store_sub, ":ratio", ":town_prosperity", 50),
		(val_add, ":ratio", 100),
		(val_mul, ":number_of_items_in_town", ":ratio"),
		(val_div, ":number_of_items_in_town", 100),
	  (try_end),

	  (val_clamp, ":number_of_items_in_town", 10, 40),	

	  (try_begin),
	    (is_between, ":cur_center", castles_begin, castles_end),
	    (val_div, ":number_of_items_in_town", 2),
      (try_end),

      (try_for_range, ":cur_goods", trade_goods_begin, trade_goods_end),
        (call_script, "script_center_get_production", ":cur_center", ":cur_goods"),
		(assign, ":cur_production", reg0),

        (try_for_range, ":cur_village", villages_begin, villages_end),
		  (party_slot_eq, ":cur_village", slot_village_bound_center, ":cur_center"),
          (call_script, "script_center_get_production", ":cur_village", ":cur_goods"),
		  (val_div, reg0, 3),
		  (val_add, ":cur_production", reg0),
		(try_end),		

		(val_max, ":cur_production", 1),
		(val_mul, ":cur_production", 4),

        (val_mul, ":cur_production", ":number_of_items_in_town"),
		(val_mul, ":cur_production", 100),
		(val_div, ":cur_production", ":total_production"),
        (set_item_probability_in_merchandise, ":cur_goods", ":cur_production"),						  
      (try_end),

	  (troop_clear_inventory, ":cur_merchant"),
      (troop_add_merchandise, ":cur_merchant", itp_type_goods, ":number_of_items_in_town"),

      (troop_ensure_inventory_space, ":cur_merchant", 20),
      (troop_sort_inventory, ":cur_merchant"),
      (store_troop_gold, ":cur_gold",":cur_merchant"),
    ##diplomacy start+
	#Option: scaling gold additions by the prosperity of the town.
	(try_begin),
		(ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_LOW),#this must be explicitly enabled
	    (party_get_slot, ":prosperity_75", ":cur_center", slot_town_prosperity),
		(val_add, ":prosperity_75", 75),
		(store_mul, ":target_gold", ":prosperity_75", 1500),
		(val_add, ":target_gold", 62),
		(val_div, ":target_gold", 125),#average 1500
		(lt, ":cur_gold", ":target_gold"),
		(store_random_in_range,":new_gold",500,1000),
		(val_mul, ":new_gold", ":prosperity_75"),
		(val_add, ":new_gold", 62),
		(val_div, ":new_gold", 125),
		(call_script, "script_troop_add_gold", ":cur_merchant", ":new_gold"),
	(else_try),
		(lt, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_LOW),
	    #fall through to default behavior
	    ##diplomacy end+
      (lt,":cur_gold",1500),
      (store_random_in_range,":new_gold",500,1000),
      (call_script, "script_troop_add_gold", ":cur_merchant", ":new_gold"),
    ##diplomacy start+
    (try_end),
	##diplomacy end+
    (try_end), 	
  ]),
  # script_refresh_center_armories
  ("refresh_center_armories",
  [
    (reset_item_probabilities, 100),
	(set_merchandise_modifier_quality, 150),    
	(try_for_range, ":cur_merchant", armor_merchants_begin, armor_merchants_end),    
	  (store_sub, ":cur_town", ":cur_merchant", armor_merchants_begin),
	  (val_add, ":cur_town", towns_begin),
	  (troop_clear_inventory, ":cur_merchant"),
	  (party_get_slot, ":cur_faction", ":cur_town", slot_center_original_faction),    
	  (troop_add_merchandise_with_faction, ":cur_merchant", ":cur_faction", itp_type_body_armor, 16),
	  (troop_add_merchandise_with_faction, ":cur_merchant", ":cur_faction", itp_type_head_armor, 16),
	  (troop_add_merchandise_with_faction, ":cur_merchant", ":cur_faction", itp_type_foot_armor, 8),
	  (troop_add_merchandise_with_faction, ":cur_merchant", ":cur_faction", itp_type_hand_armor, 4),
	  (troop_ensure_inventory_space, ":cur_merchant", merchant_inventory_space),
	  (troop_sort_inventory, ":cur_merchant"),
	  (store_troop_gold, reg6, ":cur_merchant"),

	    ##diplomacy start+
		#Option: scaling gold additions by the prosperity of the town.
		(try_begin),
			(ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_LOW),#this must be explicitly enabled
		    (party_get_slot, ":prosperity_75", ":cur_town", slot_town_prosperity),
			(val_add, ":prosperity_75", 75),
			(store_mul, ":target_gold", ":prosperity_75", 900),
			(val_add, ":target_gold", 62),
			(val_div, ":target_gold", 125),#average 900
			(lt, reg(6), ":target_gold"),
			(store_random_in_range,":new_gold",200,400),
			(val_mul, ":new_gold", ":prosperity_75"),
			(val_add, ":new_gold", 62),
			(val_div, ":new_gold", 125),
			(call_script, "script_troop_add_gold", ":cur_merchant", ":new_gold"),
		(else_try),
			(lt, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_LOW),
		    #fall through to default behavior
		    ##diplomacy end+
	    (lt,reg6,1000),
	    (store_random_in_range,":new_gold",250,500),
	    (call_script, "script_troop_add_gold", ":cur_merchant", ":new_gold"),
		##diplomacy start+
		(try_end),
		##diplomacy end+
    (end_try),
  ]),
  # script_refresh_center_weaponsmiths
  ("refresh_center_weaponsmiths",
  [
    (reset_item_probabilities, 100),
    (set_merchandise_modifier_quality, 150),
    (try_for_range, ":cur_merchant", weapon_merchants_begin, weapon_merchants_end),
	  (store_sub, ":cur_town", ":cur_merchant", weapon_merchants_begin),
      (val_add, ":cur_town", towns_begin), 
	  (troop_clear_inventory, ":cur_merchant"),
      (party_get_slot, ":cur_faction", ":cur_town", slot_center_original_faction),
	  #gekokujo add new types of merchandise
      #(troop_add_merchandise_with_faction, ":cur_merchant", ":cur_faction", itp_type_one_handed_wpn, 5),
      #(troop_add_merchandise_with_faction, ":cur_merchant", ":cur_faction", itp_type_two_handed_wpn, 5),
      #(troop_add_merchandise_with_faction, ":cur_merchant", ":cur_faction", itp_type_polearm, 5),
      #(troop_add_merchandise_with_faction, ":cur_merchant", ":cur_faction", itp_type_shield, 6),
      #(troop_add_merchandise_with_faction, ":cur_merchant", ":cur_faction", itp_type_bow, 4),
      #(troop_add_merchandise_with_faction, ":cur_merchant", ":cur_faction", itp_type_crossbow, 3),
      #(troop_add_merchandise_with_faction, ":cur_merchant", ":cur_faction", itp_type_thrown, 5),
      #(troop_add_merchandise_with_faction, ":cur_merchant", ":cur_faction", itp_type_arrows, 2),
      #(troop_add_merchandise_with_faction, ":cur_merchant", ":cur_faction", itp_type_bolts, 2),
      (troop_add_merchandise_with_faction, ":cur_merchant", ":cur_faction", itp_type_one_handed_wpn, 4),
      (troop_add_merchandise_with_faction, ":cur_merchant", ":cur_faction", itp_type_two_handed_wpn, 8),
      (troop_add_merchandise_with_faction, ":cur_merchant", ":cur_faction", itp_type_polearm, 8),
      (troop_add_merchandise_with_faction, ":cur_merchant", ":cur_faction", itp_type_thrown, 3),
      (troop_add_merchandise_with_faction, ":cur_merchant", ":cur_faction", itp_type_bow, 5),
      (troop_add_merchandise_with_faction, ":cur_merchant", ":cur_faction", itp_type_musket, 5),
      (troop_add_merchandise_with_faction, ":cur_merchant", ":cur_faction", itp_type_arrows, 2),
      (troop_add_merchandise_with_faction, ":cur_merchant", ":cur_faction", itp_type_bullets, 2),
      (troop_ensure_inventory_space, ":cur_merchant", merchant_inventory_space),
      (troop_sort_inventory, ":cur_merchant"), 
      (store_troop_gold, reg6, ":cur_merchant"),

	    ##diplomacy start+
		#Option: scaling gold additions by the prosperity of the town.
		(try_begin),
			(ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_LOW),#this must be explicitly enabled
		    (party_get_slot, ":prosperity_75", ":cur_town", slot_town_prosperity),
			(val_add, ":prosperity_75", 75),
			(store_mul, ":target_gold", ":prosperity_75", 900),
			(val_add, ":target_gold", 62),
			(val_div, ":target_gold", 125),#average 900
			(lt, reg6, ":target_gold"),
			(store_random_in_range,":new_gold",200,400),
			(val_mul, ":new_gold", ":prosperity_75"),
			(val_add, ":new_gold", 62),
			(val_div, ":new_gold", 125),
			(call_script, "script_troop_add_gold", ":cur_merchant", ":new_gold"),
		(else_try),
			(lt, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_LOW),
		    #fall through to default behavior
		    ##diplomacy end+
      (lt, reg6, 1000),
      (store_random_in_range, ":new_gold", 250, 500),
      (call_script, "script_troop_add_gold", ":cur_merchant", ":new_gold"),
	  ##diplomacy start+
	  (try_end),
	  ##diplomacy end+
    (try_end),
  ]),
  # script_refresh_center_stables
  ("refresh_center_stables",
  [
    (reset_item_probabilities, 100),
    (set_merchandise_modifier_quality, 150),
    (try_for_range, ":cur_merchant", horse_merchants_begin, horse_merchants_end),
	  (troop_clear_inventory, ":cur_merchant"),
      (store_sub, ":cur_town", ":cur_merchant", horse_merchants_begin),
      (val_add, ":cur_town", towns_begin),
      (party_get_slot, ":cur_faction", ":cur_town", slot_center_original_faction),
      (troop_add_merchandise_with_faction, ":cur_merchant", ":cur_faction", itp_type_horse, 5),
      (troop_ensure_inventory_space, ":cur_merchant", 65),
      (troop_sort_inventory, ":cur_merchant"),
      (store_troop_gold, ":cur_gold", ":cur_merchant"),
	##diplomacy start+
	#Option: scaling gold additions by the prosperity of the town.
	(try_begin),
		(ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_LOW),#this must be explicitly enabled
	    (party_get_slot, ":prosperity_75", ":cur_town", slot_town_prosperity),
		(val_add, ":prosperity_75", 75),
		(store_mul, ":target_gold", ":prosperity_75", 600),
		(val_add, ":target_gold", 62),
		(val_div, ":target_gold", 125),#average 600
		(lt, ":cur_gold", ":target_gold"),
		(store_random_in_range,":new_gold",200,400),
		(val_mul, ":new_gold", ":prosperity_75"),
		(val_add, ":new_gold", 62),
		(val_div, ":new_gold", 125),
		(call_script, "script_troop_add_gold", ":cur_merchant", ":new_gold"),
	(else_try),
		(lt, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_LOW),
	    #fall through to default behavior
	    ##diplomacy end+
      (lt, ":cur_gold", 600),
      (store_random_in_range, ":new_gold", 250, 500),
      (call_script, "script_troop_add_gold", ":cur_merchant", ":new_gold"),
    ##diplomacy start+
    (try_end),
    ##diplomacy end+
    (try_end),
  ]),
## Gambling System by rubik 
## CC gambling begin
  ("refresh_mystic_merchant_items",
    [
      (store_script_param_1, ":troop_no"),
     
      (troop_get_inventory_capacity, ":inv_cap", ":troop_no"),
      (try_for_range, ":i_slot", 10, ":inv_cap"),
        (troop_set_inventory_slot, ":troop_no", ":i_slot", -1),
        (troop_set_slot, ":troop_no", ":i_slot", 0), # 0 = not_hidden , 1 = hidden
      (try_end),
      (reset_item_probabilities, 100),
      (set_merchandise_modifier_quality, 120),
      (troop_add_merchandise, ":troop_no", itp_type_horse,15),
      (troop_add_merchandise, ":troop_no", itp_type_body_armor,16),
      (troop_add_merchandise, ":troop_no", itp_type_head_armor,8),
      (troop_add_merchandise, ":troop_no", itp_type_foot_armor,8),
      (troop_add_merchandise, ":troop_no", itp_type_hand_armor,4),
      (troop_add_merchandise, ":troop_no", itp_type_one_handed_wpn,5),
      (troop_add_merchandise, ":troop_no", itp_type_two_handed_wpn,5),
      (troop_add_merchandise, ":troop_no", itp_type_polearm,5),
      (troop_add_merchandise, ":troop_no", itp_type_shield,6),
      (troop_add_merchandise, ":troop_no", itp_type_bow,4),
      (troop_add_merchandise, ":troop_no", itp_type_crossbow,3),
      (troop_add_merchandise, ":troop_no", itp_type_thrown,5),
      (try_for_range, ":i_slot", 10, ":inv_cap"),
        (troop_get_inventory_slot, ":item", ":troop_no", ":i_slot"),
        (gt, ":item", -1),
        (troop_set_slot, ":troop_no", ":i_slot", 1), # 0 = not_hidden , 1 = hidden
      (try_end),
   ]),
]
