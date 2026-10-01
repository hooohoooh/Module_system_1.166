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

game_menus_town_castle_siege = [
  
# Towns
  (
    "zendar",mnf_auto_enter,
    "You enter the town of Zendar.",
    "none",
    [(reset_price_rates,0),(set_price_rate_for_item,"itm_tools",70),(set_price_rate_for_item,"itm_salt",140)],
    [
      ("zendar_enter",[],"_",[(set_jump_mission,"mt_town_default"),(jump_to_scene,"scn_zendar_center"),(change_screen_mission)],"Door to the town center."),
      ("zendar_tavern",[],"_",[(set_jump_mission,"mt_town_default"),
                                                   (jump_to_scene,"scn_the_happy_boar"),
                                                   (change_screen_mission)],"Door to the tavern."),
      ("zendar_merchant",[],"_",[(set_jump_mission,"mt_town_default"),
                                                   (jump_to_scene,"scn_zendar_merchant"),
                                                   (change_screen_mission)],"Door to the merchant."),
      ("zendar_arena",[],"_",[(set_jump_mission,"mt_town_default"),
                                                   (jump_to_scene,"scn_zendar_arena"),
                                                   (change_screen_mission)],"Door to the arena."),
#      ("zendar_leave",[],"Leave town.",[[leave_encounter],[change_screen_return]]),
      ("town_1_leave",[],"_",[(leave_encounter),(change_screen_return)]),
    ]
  ),
  (
    "salt_mine",mnf_auto_enter,
    "You enter the salt mine.",
    "none",
    [(reset_price_rates,0),(set_price_rate_for_item,"itm_salt",55)],
    [
      ("enter",[],"Enter.",[(set_jump_mission,"mt_town_center"),(jump_to_scene,"scn_salt_mine"),(change_screen_mission)]),
      ("leave",[],"Leave.",[(leave_encounter),(change_screen_return)]),
    ]
  ),
  (
    "four_ways_inn",mnf_auto_enter,
    "You arrive at the Four Ways Inn.",
    "none",
    [],
    [

#      ("enter",[],"Enter.",[[set_jump_mission,"mt_town_default"],[jump_to_scene,"scn_conversation_scene"],[change_screen_mission]]),
      ("enter",[],"Enter.",[(set_jump_mission,"mt_ai_training"),(jump_to_scene,"scn_four_ways_inn"),(change_screen_mission)]),
      ("leave",[],"Leave.",[(leave_encounter),(change_screen_return)]),
    ]
  ),
  (
    "test_scene",0,
    "You enter the test scene.",
    "none",
    [],
    [

      ("enter",[],"Enter 1.",[[set_jump_mission,"mt_ai_training"],[jump_to_scene,"scn_multi_scene_1"],[change_screen_mission]]),
      ("enter",[],"Enter 2.",[[set_jump_mission,"mt_ai_training"],[jump_to_scene,"scn_multi_scene_2"],[change_screen_mission]]),
      ("enter",[],"Enter 3.",[[set_jump_mission,"mt_ai_training"],[jump_to_scene,"scn_multi_scene_3"],[change_screen_mission]]),
      ("enter",[],"Enter 4.",[[set_jump_mission,"mt_ai_training"],[jump_to_scene,"scn_multi_scene_4"],[change_screen_mission]]),
      ("enter",[],"Enter 5.",[[set_jump_mission,"mt_ai_training"],[jump_to_scene,"scn_multi_scene_5"],[change_screen_mission]]),
      ("enter",[],"Enter 6.",[[set_jump_mission,"mt_ai_training"],[jump_to_scene,"scn_multi_scene_6"],[change_screen_mission]]),
      ("enter",[],"Enter 7.",[[set_jump_mission,"mt_ai_training"],[jump_to_scene,"scn_test2"],[change_screen_mission]]),
      ("enter",[],"Enter 8.",[[set_jump_mission,"mt_ai_training"],[jump_to_scene,"scn_test3"],[change_screen_mission]]),
      ("enter",[],"Enter 9.",[[set_jump_mission,"mt_ai_training"],[jump_to_scene,"scn_multi_scene_13"],[change_screen_mission]]),
      ("leave",[],"Leave.",[(leave_encounter),(change_screen_return)]),
    ]
  ),
  (
    "battlefields",0,
    "{!}Select a field...",
    "none",
    [],
    [

      ("enter_f1",[],"{!}Field 1",[[set_jump_mission,"mt_ai_training"],[jump_to_scene,"scn_field_1"],[change_screen_mission]]),
      ("enter_f2",[],"{!}Field 2",[[set_jump_mission,"mt_ai_training"],[jump_to_scene,"scn_field_2"],[change_screen_mission]]),
      ("enter_f3",[],"{!}Field 3",[[set_jump_mission,"mt_ai_training"],[jump_to_scene,"scn_field_3"],[change_screen_mission]]),
      ("enter_f4",[],"{!}Field 4",[[set_jump_mission,"mt_ai_training"],[jump_to_scene,"scn_field_4"],[change_screen_mission]]),
      ("enter_f5",[],"{!}Field 5",[[set_jump_mission,"mt_ai_training"],[jump_to_scene,"scn_field_5"],[change_screen_mission]]),
      ("leave",[],"Leave.",[(leave_encounter),(change_screen_return)]),
    ]
  ),
  (
    "dhorak_keep",0,
#    "Dhorak Keep, the stronghold of the bandits stands overlooking the barren wilderness.",
    "You enter the Dhorak Keep",
    "none",
    [],
    [
      ("enter",[],"Enter.",[(set_jump_mission,"mt_town_center"),(jump_to_scene,"scn_dhorak_keep"),(change_screen_mission)]),
      ("leave",[],"Leave.",[(leave_encounter),(change_screen_return)]),
    ]
  ),
  
##  (
##    "center_under_attack_while_resting",0,
##    "{s1} has been besieged by {s2}, and the enemy seems to be preparing for an assault!\
## What will you do?",
##    "none",
##    [
##        (party_get_battle_opponent, ":besieger_party", "$auto_enter_town"),
##        (str_store_party_name, s1, "$auto_enter_town"),
##        (str_store_party_name, s2, ":besieger_party"),
##    ],
##    [
##      ("defend_against_siege", [],"Help the defenders of {s1}!",
##       [
##           (assign, "$g_last_player_do_nothing_against_siege_next_check", 0),
##           (rest_for_hours, 0, 0, 0),
##           (change_screen_return),
##           (start_encounter, "$auto_enter_town"),
##           ]),
##      ("do_not_defend_against_siege",[],"Find a secure place and wait there.",
##       [
##           (change_screen_return),
##           ]),
##    ]
##  ),

  (
    "join_siege_outside",mnf_scale_picture,
    "{s1} has come under siege by {s2}.",
    "none",
    [
        (str_store_party_name, s1, "$g_encountered_party"),
        (str_store_party_name, s2, "$g_encountered_party_2"),
		#gekokujo only one type of siege sighted pic
		(set_background_mesh, "mesh_gekokujo_pic_siege_sighted"),
	#	##diplomacy start+ Get gender from script
    #    #(troop_get_type, ":is_female", "trp_player"),#<- replaced
    #    (try_begin),
    #      #(eq, ":is_female", 1),#<- replaced
	#	  (eq, 1, "$character_gender"),#<- added
    #      (set_background_mesh, "mesh_pic_siege_sighted_fem"),
    #    (else_try),
    #      (set_background_mesh, "mesh_pic_siege_sighted"),
    #    (try_end),
	#	##diplomacy end+
    ],
    [
      ("approach_besiegers",[(store_faction_of_party, ":faction_no", "$g_encountered_party_2"),
                             (store_relation, ":relation", ":faction_no", "fac_player_supporters_faction"),
                             (ge, ":relation", 0),
                             (store_faction_of_party, ":faction_no", "$g_encountered_party"),
                             (store_relation, ":relation", ":faction_no", "fac_player_supporters_faction"),
                             (lt, ":relation", 0),
                             ],"Approach the siege camp.",[
          (jump_to_menu, "mnu_besiegers_camp_with_allies"),
                                ]),
      ("pass_through_siege",[(store_faction_of_party, ":faction_no", "$g_encountered_party"),
                             (store_relation, ":relation", ":faction_no", "fac_player_supporters_faction"),
                             (ge, ":relation", 0),
                             ],"Pass through the siege lines and enter {s1}.",
       [
            (jump_to_menu,"mnu_cut_siege_without_fight"),
          ]),
      ("leave",[],"Leave.",[(leave_encounter),
                            (change_screen_return)]),
    ]
  ),
  (
    "cut_siege_without_fight",0,
    "The besiegers let you approach the gates without challenge.",
    "none",
    [],
    [
      ("continue",[],"Continue...",[(try_begin),
                                   (this_or_next|eq, "$g_encountered_party_faction", "fac_player_supporters_faction"),
                                   (eq, "$g_encountered_party_faction", "$players_kingdom"),
                                   (jump_to_menu, "mnu_town"),
                                 (else_try),
                                   (jump_to_menu, "mnu_castle_outside"),
                                 (try_end)]),
      ]
  ),
  (
    "besiegers_camp_with_allies",0,
    "{s1} remains under siege. The banners of {s2} fly above the camp of the besiegers,\
 where you and your men are welcomed.",
    "none",
    [        
        (str_store_party_name, s1, "$g_encountered_party"),
        (str_store_party_name, s2, "$g_encountered_party_2"),
        (assign, "$g_enemy_party", "$g_encountered_party"),
        (assign, "$g_ally_party", "$g_encountered_party_2"),
        (select_enemy, 0),
        (call_script, "script_encounter_calculate_fit"),
        (try_begin),
          (eq, "$new_encounter", 1),
          (assign, "$new_encounter", 0),
		  ###diplomacy start+
		  ##If terrain advantage is on, use siege settings
          #(assign, ":save_dplmc_terrain_advantage", "$g_dplmc_terrain_advantage"),
		  ##(assign, "$g_dplmc_terrain_advantage", ":save_dplmc_terrain_advantage"),
		  #(try_begin),
		  #   (eq, "$g_dplmc_terrain_advantage", TERRAIN_ADVANTAGE_ENABLE),
		  #   (assign, "$g_dplmc_terrain_advantage", TERRAIN_ADVANTAGE_FORCE_SIEGE),
		  #(try_end),
		  ###diplomacy end+
          (call_script, "script_encounter_init_variables"),
		  ###diplomacy start+
		  ##Revert terrain advantage setting
		  #(assign, "$g_dplmc_terrain_advantage", ":save_dplmc_terrain_advantage"),
		  ###diplomacy end+
        (try_end),

        (try_begin),
          (eq, "$g_leave_encounter",1),
          (change_screen_return),
        (else_try),
          (assign, ":enemy_finished", 0),
          (try_begin),
            (eq, "$g_battle_result", 1),
            (assign, ":enemy_finished", 1),
          (else_try),
            (le, "$g_enemy_fit_for_battle", 0),
            (ge, "$g_friend_fit_for_battle", 1),
            (assign, ":enemy_finished", 1),
          (try_end),
          (this_or_next|eq, ":enemy_finished", 1),
          (eq, "$g_enemy_surrenders", 1),
##          (assign, "$g_next_menu", -1),#"mnu_castle_taken_by_friends"),
##          (jump_to_menu, "mnu_total_victory"),
          (call_script, "script_party_wound_all_members", "$g_enemy_party"),
          (leave_encounter),
          (change_screen_return),
        (else_try),
          (call_script, "script_party_count_members_with_full_health", "p_collective_friends"),          
          (assign, ":ally_num_soldiers", reg0),
          (eq, "$g_battle_result", -1),
          (eq, ":ally_num_soldiers", 0), #battle lost (TODO : also compare this with routed allies too like in other parts)
          (leave_encounter),
          (change_screen_return),
        (try_end),
        ],
    [
      ("talk_to_siege_commander",[],"Request a meeting with the commander.",[
                                (call_script, "script_get_meeting_scene"), (assign, ":meeting_scene", reg0),
                                (modify_visitors_at_site,":meeting_scene"),(reset_visitors),
                                (set_visitor,0,"trp_player"),
                                (party_stack_get_troop_id, ":siege_leader_id","$g_encountered_party_2",0),
                                (party_stack_get_troop_dna,":siege_leader_dna","$g_encountered_party_2",0),
                                (set_visitor,17,":siege_leader_id",":siege_leader_dna"),
                                (set_jump_mission,"mt_conversation_encounter"),
                                (jump_to_scene,":meeting_scene"),
                                (assign, "$talk_context", tc_siege_commander),
                                (change_screen_map_conversation, ":siege_leader_id")]),
      ("join_siege_with_allies",[(neg|troop_is_wounded, "trp_player")], "Join the next assault.",
       [
           (assign, "$g_joined_battle_to_help", 1), 
           (party_set_next_battle_simulation_time, "$g_encountered_party", -1),
           (try_begin),
             (check_quest_active, "qst_join_siege_with_army"),
             (quest_slot_eq, "qst_join_siege_with_army", slot_quest_target_center, "$g_encountered_party"),
             (add_xp_as_reward, 250),
             (call_script, "script_end_quest", "qst_join_siege_with_army"),
             #Reactivating follow army quest
             (faction_get_slot, ":faction_marshall", "$players_kingdom", slot_faction_marshall),
             (str_store_troop_name_link, s9, ":faction_marshall"),
             (setup_quest_text, "qst_follow_army"),
             ##diplomacy start+ fix pronoun
             (call_script, "script_dplmc_store_troop_is_female", ":faction_marshall"),
             (str_store_string, s2, "@{s9} wants you to follow {reg0?her:his} army until further notice."),
             ##diplomacy end+
             (call_script, "script_start_quest", "qst_follow_army", ":faction_marshall"),
             (assign, "$g_player_follow_army_warnings", 0),
           (try_end),
           (try_begin),
             (party_slot_eq, "$g_encountered_party", slot_party_type, spt_town),
             (party_get_slot, ":battle_scene", "$g_encountered_party", slot_town_walls),
           (else_try),
             (party_get_slot, ":battle_scene", "$g_encountered_party", slot_castle_exterior),
           (try_end),
           (call_script, "script_calculate_battle_advantage"),
           (val_mul, reg0, 2),
           (val_div, reg0, 3), #scale down the advantage a bit in sieges.
           (set_battle_advantage, reg0),
           (set_party_battle_mode),
           (try_begin),
             (party_slot_eq, "$g_encountered_party", slot_center_siege_with_belfry, 1),
			 #gekokujo revise belfry attack mission sometime
             #(set_jump_mission,"mt_castle_attack_walls_belfry"),
			 (set_jump_mission,"mt_castle_attack_walls_ladder"),
           (else_try),
             (set_jump_mission,"mt_castle_attack_walls_ladder"),
           (try_end),
           (jump_to_scene,":battle_scene"),
           (assign, "$g_siege_final_menu", "mnu_besiegers_camp_with_allies"),
           (assign, "$g_siege_battle_state", 1),
           (assign, "$g_next_menu", "mnu_castle_besiege_inner_battle"),
           (jump_to_menu, "mnu_battle_debrief"),
           (change_screen_mission),
          ]),
      ("join_siege_stay_back", [(call_script, "script_party_count_members_with_full_health", "p_main_party"),
                                (ge, reg0, 3),
                                ],
       "Order your soldiers to join the next assault without you.",
       [
         (assign, "$g_joined_battle_to_help", 1), 
         (party_set_next_battle_simulation_time, "$g_encountered_party", -1),
         (try_begin),
           (check_quest_active, "qst_join_siege_with_army"),
           (quest_slot_eq, "qst_join_siege_with_army", slot_quest_target_center, "$g_encountered_party"),
           (add_xp_as_reward, 100),
           (call_script, "script_end_quest", "qst_join_siege_with_army"),
           #Reactivating follow army quest
           (faction_get_slot, ":faction_marshall", "$players_kingdom", slot_faction_marshall),
           (str_store_troop_name_link, s9, ":faction_marshall"),
           (setup_quest_text, "qst_follow_army"),
           ##diplomacy start+ fix pronoun
           (call_script, "script_dplmc_store_troop_is_female", ":faction_marshall"),
           (str_store_string, s2, "@{s9} wants you to follow {reg0?her:his} army until further notice."),
           ##diplomacy end+
           (call_script, "script_start_quest", "qst_follow_army", ":faction_marshall"),
           (assign, "$g_player_follow_army_warnings", 0),
         (try_end),
         (jump_to_menu,"mnu_castle_attack_walls_with_allies_simulate")]),
      ("leave",[],"Leave.",[(leave_encounter),(change_screen_return)]),
    ]
  ),
  (
    "castle_outside",mnf_scale_picture,
    "You are outside {s2}.{s11} {s3} {s4}",
    "none",
    [
        (assign, "$g_enemy_party", "$g_encountered_party"),
        (assign, "$g_ally_party", -1),
        (str_store_party_name, s2,"$g_encountered_party"),
        (call_script, "script_encounter_calculate_fit"),
        (assign,"$all_doors_locked",1),
        (assign, "$current_town","$g_encountered_party"),
                
        (try_begin),
          (eq, "$new_encounter", 1),
          (assign, "$new_encounter", 0),
          (call_script, "script_let_nearby_parties_join_current_battle", 1, 0),
		  ###diplomacy start+
		  ##If terrain advantage is on, use siege settings for estimating strength
          #(assign, ":save_dplmc_terrain_advantage", "$g_dplmc_terrain_advantage"),
		  #(try_begin),
		  #   (eq, "$g_dplmc_terrain_advantage", TERRAIN_ADVANTAGE_ENABLE),
		  #   (assign, "$g_dplmc_terrain_advantage", TERRAIN_ADVANTAGE_FORCE_SIEGE),
		  #(try_end),
		  ###diplomacy end+
          (call_script, "script_encounter_init_variables"),
		  ###diplomacy start+
		  ##Revert terrain advantage settings
		  #(assign, "$g_dplmc_terrain_advantage", ":save_dplmc_terrain_advantage"),
		  ###diplomacy end+
          (assign, "$entry_to_town_forbidden",0),
          (assign, "$sneaked_into_town",0),
          (assign, "$town_entered", 0),
#          (assign, "$waiting_for_arena_fight_result", 0),
          (assign, "$encountered_party_hostile", 0),
          (assign, "$encountered_party_friendly", 0),
          (try_begin),
            (gt, "$g_player_besiege_town", 0),
            (neq,"$g_player_besiege_town","$g_encountered_party"),
            (party_slot_eq, "$g_player_besiege_town", slot_center_is_besieged_by, "p_main_party"),
            (call_script, "script_lift_siege", "$g_player_besiege_town", 0),
            (assign,"$g_player_besiege_town",-1),
          (try_end),
          (try_begin),
            (lt, "$g_encountered_party_relation", 0),
            (assign, "$encountered_party_hostile", 1),
            (assign,"$entry_to_town_forbidden",1),
          (try_end),

          ##diplomacy begin
          (try_begin),
            (party_slot_eq, "$g_encountered_party", slot_village_infested_by_bandits, "trp_peasant_woman"),
            (assign, "$encountered_party_hostile", 1),
            (assign,"$entry_to_town_forbidden",1),
          (try_end),
          ##diplomacy end

          (assign,"$cant_sneak_into_town",0),
          (try_begin),
            (eq,"$current_town","$last_sneak_attempt_town"),
            (store_current_hours,reg(2)),
            (val_sub,reg(2),"$last_sneak_attempt_time"),
            (lt,reg(2),12),
            (assign,"$cant_sneak_into_town",1),
          (try_end),
        (else_try), #second or more turn
          (eq, "$g_leave_encounter",1),
          (change_screen_return),
        (try_end),

        (str_clear,s4),
        (try_begin), 
          (eq,"$entry_to_town_forbidden",1),
          (try_begin),
            (eq,"$cant_sneak_into_town",1),
            (str_store_string,s4,"str_sneaking_to_town_impossible"),
          (else_try),
            (str_store_string,s4,"str_entrance_to_town_forbidden"),
          (try_end),
        (try_end),

        (party_get_slot, ":center_lord", "$current_town", slot_town_lord),
        (store_faction_of_party, ":center_faction", "$current_town"),
        (str_store_faction_name,s9,":center_faction"),
        (try_begin),
          (ge, ":center_lord", 0),
          (str_store_troop_name,s8,":center_lord"),
          (str_store_string,s7,"@{s8} of {s9}"),
        (try_end),

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
			(str_store_string, s11, "@former overlord"),
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
			#check for friends (former companions)
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

        (try_begin), # same mnu_town
          (party_slot_eq,"$current_town",slot_party_type, spt_castle),
          (try_begin),
            (eq, ":center_lord", "trp_player"),
            (str_store_string,s11,"@ Your own banner flies over the castle gate."),
		  ##diplomacy start+ If reg0 > 0, a relation string was written to {s11} above
		  (else_try),
			(ge, reg0, 1),
			(str_store_string, s11, "@ You see the banner of your {s11} {s7} over the castle gate."),
		  ##diplomacy end+
          (else_try),
            (ge, ":center_lord", 0),
            (str_store_string,s11,"@ You see the banner of {s7} over the castle gate."),
          (else_try),
		    (is_between, ":center_faction", kingdoms_begin, kingdoms_end),
            (str_store_string,s11,"str__this_castle_is_temporarily_under_royal_control"),
		  (else_try),
            (str_store_string,s11,"str__this_castle_does_not_seem_to_be_under_anyones_control"),
          (try_end),
        (else_try),
          (try_begin),
            (eq, ":center_lord", "trp_player"),
            (str_store_string,s11,"@ Your own banner flies over the town gates."),
		  ##diplomacy start+ If reg0 > 0, a relation string was written to {s11} above
		  (else_try),
			(ge, reg0, 1),
			(str_store_string, s11, "@ You see the banner of your {s11} {s7} over the town gates."),
		  ##diplomacy end+
          (else_try),
            (ge, ":center_lord", 0),
            (str_store_string,s11,"@ You see the banner of {s7} over the town gates."),
          (else_try),
		    (is_between, ":center_faction", kingdoms_begin, kingdoms_end),
            (str_store_string,s11,"str__this_town_is_temporarily_under_royal_control"),
		  (else_try),	
            (str_store_string,s11,"str__the_townspeople_seem_to_have_declared_their_independence"),
          (try_end),
        (try_end),

        (party_get_num_companions, reg(7),"p_collective_enemy"),
        (assign,"$castle_undefended",0),
        (str_clear, s3),
        (try_begin),
          (eq,reg(7),0),
          (assign,"$castle_undefended",1),
#          (party_set_faction,"$g_encountered_party","fac_neutral"),
#          (party_set_slot, "$g_encountered_party", slot_town_lord, stl_unassigned),
          (str_store_string, s3, "str_castle_is_abondened"),
        (else_try),
        ##diplomacy begin
          (party_slot_eq, "$g_encountered_party", slot_village_infested_by_bandits, "trp_peasant_woman"),
          (str_store_string, s3, "str_dplmc_place_is_occupied_by_insurgents"),
        (else_try),
        ##diplomacy end
		##diplomacy start+ Handle player is co-ruler of kingdom
		  (assign, ":is_coruler", 0),
		  (try_begin),
			(eq, "$g_encountered_party_faction", "$players_kingdom"),
			(is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
			(call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", "$players_kingdom"),
			(ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
			(assign, ":is_coruler", 1),
		  (try_end),
		  (this_or_next|eq, ":is_coruler", 1),
		##diplomacy end+
          (eq,"$g_encountered_party_faction","fac_player_supporters_faction"),
          (str_store_string, s3, "str_place_is_occupied_by_player"),
        (else_try),
          (lt, "$g_encountered_party_relation", 0),
          (str_store_string, s3, "str_place_is_occupied_by_enemy"),
        (else_try),
#          (str_store_string, s3, "str_place_is_occupied_by_friendly"),
        (try_end),
		##diplomacy start+
		(assign, reg0, ":save_reg0"),#revert variables
		(assign, reg4, ":save_reg4"),
		##diplomacy end+

        (try_begin),
          (eq, "$g_leave_town_outside",1),
          (assign, "$g_leave_town_outside",0),
          (assign, "$g_permitted_to_center", 0),
          (change_screen_return),
        (else_try),
          (check_quest_active, "qst_escort_lady"),
          (quest_slot_eq, "qst_escort_lady", slot_quest_target_center, "$g_encountered_party"),
          (quest_get_slot, ":quest_object_troop", "qst_escort_lady", slot_quest_object_troop),
          (call_script, "script_get_meeting_scene"), (assign, ":meeting_scene", reg0),
          (modify_visitors_at_site,":meeting_scene"),
          (reset_visitors),
          (set_visitor,0, "trp_player"),
          (set_visitor,17, ":quest_object_troop"),
          (set_jump_mission, "mt_conversation_encounter"),
          (jump_to_scene, ":meeting_scene"),
          (assign, "$talk_context", tc_entering_center_quest_talk),
          (change_screen_map_conversation, ":quest_object_troop"),
        (else_try),
          (check_quest_active, "qst_kidnapped_girl"),
          (quest_slot_eq, "qst_kidnapped_girl", slot_quest_giver_center, "$g_encountered_party"),
          (quest_slot_eq, "qst_kidnapped_girl", slot_quest_current_state, 3),
          (call_script, "script_get_meeting_scene"), (assign, ":meeting_scene", reg0),
          (modify_visitors_at_site,":meeting_scene"),
          (reset_visitors),
          (set_visitor,0, "trp_player"),
          (set_visitor,17, "trp_kidnapped_girl"),
          (set_jump_mission, "mt_conversation_encounter"),
          (jump_to_scene, ":meeting_scene"),
          (assign, "$talk_context", tc_entering_center_quest_talk),
          (change_screen_map_conversation, "trp_kidnapped_girl"),
##        (else_try),
##          (gt, "$lord_requested_to_talk_to", 0),
##          (store_current_hours, ":cur_hours"),
##          (neq, ":cur_hours", "$quest_given_time"),
##          (modify_visitors_at_site,"scn_conversation_scene"),
##          (reset_visitors),
##          (assign, ":cur_lord", "$lord_requested_to_talk_to"),
##          (assign, "$lord_requested_to_talk_to", 0),
##          (set_visitor,0,"trp_player"),
##          (set_visitor,17,":cur_lord"),
##          (set_jump_mission,"mt_conversation_encounter"),
##          (jump_to_scene,"scn_conversation_scene"),
##          (assign, "$talk_context", tc_castle_gate_lord),
##          (change_screen_map_conversation, ":cur_lord"),
        (else_try),
          (eq, "$g_town_visit_after_rest", 1),
          (assign, "$g_town_visit_after_rest", 0),
          (jump_to_menu,"mnu_town"),
        ##diplomacy begin
        (else_try),
          (party_slot_eq, "$g_encountered_party", slot_village_infested_by_bandits, "trp_peasant_woman"),
          (try_begin),
            (eq, "$g_player_besiege_town", "$g_encountered_party"),
            (jump_to_menu, "mnu_castle_besiege"),
          (try_end),
        ##diplomacy end
        (else_try),
          (party_slot_eq, "$g_encountered_party", slot_party_type, spt_castle),   
		  ##diplomacy start+ Handle player is co-ruler of kingdom
		  (assign, ":is_coruler",0),
	  	  (try_begin),
			(eq, "$g_encountered_party_faction", "$players_kingdom"),
			(is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
			(call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", "$players_kingdom"),
			(ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
			(assign, ":is_coruler", 1),
		  (try_end),
		  (this_or_next|eq, ":is_coruler", 1),
		  ##diplomacy end+                 
          (this_or_next|party_slot_eq, "$g_encountered_party", slot_town_lord, "trp_player"),
          (faction_slot_eq, "$g_encountered_party_faction", slot_faction_leader, "trp_player"),          
          (jump_to_menu, "mnu_enter_your_own_castle"),
        (else_try),
          (party_slot_eq,"$g_encountered_party", slot_party_type,spt_castle),
          (ge, "$g_encountered_party_relation", 0),
          (this_or_next|eq,"$castle_undefended", 1),
          (this_or_next|eq, "$g_permitted_to_center", 1),
          (eq, "$g_encountered_party_faction", "$players_kingdom"),          
          (jump_to_menu, "mnu_town"),
        (else_try),
          (party_slot_eq,"$g_encountered_party", slot_party_type,spt_town),
          (ge, "$g_encountered_party_relation", 0),
          (jump_to_menu, "mnu_town"),
        (else_try),
          (eq, "$g_player_besiege_town", "$g_encountered_party"),
          (jump_to_menu, "mnu_castle_besiege"),
        (try_end),

        ##diplomacy begin
        (try_begin),
          (party_slot_eq, "$g_encountered_party", slot_village_infested_by_bandits, "trp_peasant_woman"),
          (set_background_mesh, "mesh_pic_townriot"),
        (else_try),
        ##diplomacy end		
		  (call_script, "script_set_town_picture"),
		##diplomacy begin
        (try_end),
        ##diplomacy end
        ],
    [
#        ("talk_to_castle_commander",[
#            (party_get_num_companions, ":no_companions", "$g_encountered_party"),
#            (ge, ":no_companions", 1),
#            (eq,"$ruler_meeting_denied",0), #this variable is removed
#            ],
#         "Request a meeting with the lord of the castle.",[
#             (modify_visitors_at_site,"scn_conversation_scene"),(reset_visitors),
#             (set_visitor,0,"trp_player"),
#             (party_stack_get_troop_id, reg(6),"$g_encountered_party",0),
#             (party_stack_get_troop_dna,reg(7),"$g_encountered_party",0),
#             (set_visitor,17,reg(6),reg(7)),
#             (set_jump_mission,"mt_conversation_encounter"),
#             (jump_to_scene,"scn_conversation_scene"),
#             (assign, "$talk_context", tc_castle_commander),
#             (change_screen_map_conversation, reg(6))
#             ]),
      ("approach_gates",[(this_or_next|eq,"$entry_to_town_forbidden",1),
                          (party_slot_eq,"$g_encountered_party", slot_party_type,spt_castle)],
       "Approach the gates and hail the guard.",[
                                                  (jump_to_menu, "mnu_castle_guard"),
##                                                   (modify_visitors_at_site,"scn_conversation_scene"),(reset_visitors),
##                                                   (set_visitor,0,"trp_player"),
##                                                   (store_faction_of_party, ":cur_faction", "$g_encountered_party"),
##                                                   (faction_get_slot, ":cur_guard", ":cur_faction", slot_faction_guard_troop),
##                                                   (set_visitor,17,":cur_guard"),
##                                                   (set_jump_mission,"mt_conversation_encounter"),
##                                                   (jump_to_scene,"scn_conversation_scene"),
##                                                   (assign, "$talk_context", tc_castle_gate),
##                                                   (change_screen_map_conversation, ":cur_guard")
                                                   ]),
      
      ("town_sneak",
        [
          (try_begin),
            (party_slot_eq, "$g_encountered_party", slot_party_type,spt_town),
            (str_store_string, s7, "str_town"),
          (else_try),  
            (str_store_string, s7, "str_castle"),
          (try_end),  
          
          #gekokujo 3.1 ninja infiltration start
          #if you have an agent or more, mention that they will help
          (party_count_companions_of_type, ":total_agents", "p_main_party", "trp_hired_agent"),
          (party_count_companions_of_type, ":female_agents", "p_main_party", "trp_female_agent"),
          (party_count_companions_of_type, ":experienced_agents", "p_main_party", "trp_hired_agent_experienced"),
          (party_count_companions_of_type, ":experienced_female_agents", "p_main_party", "trp_female_agent_experienced"),
          (val_add, ":total_agents", ":female_agents",),
          (val_add, ":total_agents", ":experienced_agents",),
          (val_add, ":total_agents", ":experienced_female_agents",),
          
          (try_begin),
            (eq, ":total_agents", 1),
            (str_store_string, s7, "@{s7} with your agent"),
          (else_try),
            (gt, ":total_agents", 1),
            (str_store_string, s7, "@{s7} with your agents"),
          (try_end),
          #gekokujo 3.1 ninja infiltration end
          
          (eq, "$entry_to_town_forbidden", 1),
          (eq, "$cant_sneak_into_town", 0)
        ],
       "Disguise yourself and sneak into the {s7}.",
       [
         (faction_get_slot, ":player_alarm", "$g_encountered_party_faction", slot_faction_player_alarm),
         (party_get_num_companions, ":num_men", "p_main_party"),
         (party_get_num_prisoners, ":num_prisoners", "p_main_party"),
         (val_add, ":num_men", ":num_prisoners"),
         (val_mul, ":num_men", 2),
         (val_div, ":num_men", 3),
         (store_add, ":get_caught_chance", ":player_alarm", ":num_men"),
         (store_random_in_range, ":random_chance", 0, 100),
         
         #gekokujo 3.1 ninja infiltration start
         (party_count_companions_of_type, ":total_agents", "p_main_party", "trp_hired_agent"),
         (party_count_companions_of_type, ":female_agents", "p_main_party", "trp_female_agent"),
         (val_add, ":total_agents", ":female_agents"),
         
         (party_count_companions_of_type, ":experienced_agents", "p_main_party", "trp_hired_agent_experienced"),
         (party_count_companions_of_type, ":experienced_female_agents", "p_main_party", "trp_female_agent_experienced"),
         (val_add, ":experienced_agents", ":experienced_female_agents"),
         
         (val_add, ":total_agents", ":experienced_agents"),
         (val_add, ":total_agents", ":experienced_agents"), #experienced agents count for twice
         
         (val_mul, ":total_agents", 2), #each agent cancels out 1 hour of alarm or 3 party members
         (val_add, ":random_chance", ":total_agents"),
         
         #(val_min, ":random_chance", 100),
         #gekokujo 3.1 ninja infiltration end
         
         (try_begin),
           (this_or_next|ge, ":random_chance", ":get_caught_chance"),
           (eq, "$g_last_defeated_bandits_town", "$g_encountered_party"),
           (assign, "$g_last_defeated_bandits_town", 0),
           (assign, "$sneaked_into_town",1),
           (assign, "$town_entered", 1),
           (jump_to_menu,"mnu_sneak_into_town_suceeded"),
           (assign, "$g_mt_mode", tcm_disguised),
         (else_try),
           (jump_to_menu,"mnu_sneak_into_town_caught"),
         (try_end)
         ]),
      ##diplomacy begin
      ("dplmc_riot_start_siege",
       [
           ##diplomacy begin
           (neg|party_slot_eq, "$g_encountered_party", slot_village_infested_by_bandits, "trp_peasant_woman"),
           ##diplomacy end
           (party_slot_eq, "$g_encountered_party", slot_center_is_besieged_by, -1),
           (party_slot_eq, "$g_encountered_party", slot_village_infested_by_bandits, "trp_peasant_woman"),
           (lt, "$g_encountered_party_2", 1),
           (call_script, "script_party_count_fit_for_battle","p_main_party"),
           (gt, reg(0), 5),
           (try_begin),
             (party_slot_eq, "$g_encountered_party", slot_party_type, spt_town),
             (assign, reg6, 1),
           (else_try),
             (assign, reg6, 0),
           (try_end),
           ],
       "Besiege the {reg6?town:castle} to counter the insurgency.",
       [
         (assign,"$g_player_besiege_town","$g_encountered_party"),
         (jump_to_menu, "mnu_castle_besiege"),
         ]),
       ("dplmc_riot_negotiate",
       [
           (party_slot_eq, "$g_encountered_party", slot_center_is_besieged_by, -1),
           (party_slot_eq, "$g_encountered_party", slot_village_infested_by_bandits, "trp_peasant_woman"),
           (lt, "$g_encountered_party_2", 1),
           (call_script, "script_party_count_fit_for_battle","p_main_party"),
           (gt, reg(0), 5),
           (try_begin),
             (party_slot_eq, "$g_encountered_party", slot_party_type, spt_town),
             (assign, reg6, 1),
           (else_try),
             (assign, reg6, 0),
           (try_end),
           ],
       "Begin negotiations.",
       [
          (jump_to_menu, "mnu_dplmc_riot_negotiate"),
        ]),

     ##diplomacy end
      ("castle_start_siege",
       [
           (this_or_next|party_slot_eq, "$g_encountered_party", slot_center_is_besieged_by, -1),
           (             party_slot_eq, "$g_encountered_party", slot_center_is_besieged_by, "p_main_party"),
           (store_relation, ":reln", "$g_encountered_party_faction", "fac_player_supporters_faction"),
           (lt, ":reln", 0),
           (lt, "$g_encountered_party_2", 1),
           (call_script, "script_party_count_fit_for_battle","p_main_party"),
           (gt, reg(0), 5),
           (try_begin),
             (party_slot_eq, "$g_encountered_party", slot_party_type, spt_town),
             (assign, reg6, 1),
           (else_try),
             (assign, reg6, 0),
           (try_end),
           ],
       "Besiege the {reg6?town:castle}.",
       [
         (assign,"$g_player_besiege_town","$g_encountered_party"),
         (store_relation, ":relation", "fac_player_supporters_faction", "$g_encountered_party_faction"),
         (val_min, ":relation", -40),
         (call_script, "script_set_player_relation_with_faction", "$g_encountered_party_faction", ":relation"),
         (call_script, "script_update_all_notes"),
         (jump_to_menu, "mnu_castle_besiege"),
         ]),

      ("cheat_castle_start_siege",
       [
         (eq, "$cheat_mode", 1),
         (this_or_next|party_slot_eq, "$g_encountered_party", slot_center_is_besieged_by, -1),
         (             party_slot_eq, "$g_encountered_party", slot_center_is_besieged_by, "p_main_party"),
         (store_relation, ":reln", "$g_encountered_party_faction", "fac_player_supporters_faction"),
         (ge, ":reln", 0),
         (lt, "$g_encountered_party_2", 1),
         (call_script, "script_party_count_fit_for_battle","p_main_party"),
         (gt, reg(0), 1),
         (try_begin),
           (party_slot_eq, "$g_encountered_party", slot_party_type, spt_town),
           (assign, reg6, 1),
         (else_try),
           (assign, reg6, 0),
         (try_end),
           ],
       "{!}CHEAT: Besiege the {reg6?town:castle}...",
       [
           (assign,"$g_player_besiege_town","$g_encountered_party"),
           (jump_to_menu, "mnu_castle_besiege"),
           ]),

      ("castle_leave",[],"Leave.",[(change_screen_return,0)]),
      ("castle_cheat_interior",[(eq, "$cheat_mode", 1)], "{!}CHEAT! Interior.",[(set_jump_mission,"mt_ai_training"),
                                                       (party_get_slot, ":castle_scene", "$current_town", slot_town_castle),
                                                       (jump_to_scene,":castle_scene"),
                                                       (change_screen_mission)]),
      ("castle_cheat_exterior",[(eq, "$cheat_mode", 1)], "{!}CHEAT! Exterior.",[
#                                                       (set_jump_mission,"mt_town_default"),
                                                       (set_jump_mission,"mt_ai_training"),
                                                       (party_get_slot, ":castle_scene", "$current_town", slot_castle_exterior),
                                                       (jump_to_scene,":castle_scene"),
                                                       (change_screen_mission)]),
      ("castle_cheat_town_walls",[(eq, "$cheat_mode", 1),(party_slot_eq,"$current_town",slot_party_type, spt_town),], "{!}CHEAT! Town Walls.",
       [
         (party_get_slot, ":scene", "$current_town", slot_town_walls),
         (set_jump_mission,"mt_ai_training"),
         (jump_to_scene,":scene"),
         (change_screen_mission)]),

    ]
  ),
   (
    "castle_guard",mnf_scale_picture,
    "You approach the gate. The men on the walls watch you closely.",
    "none",
    [
		(call_script, "script_set_town_picture"),
    ],
    [
      ("request_shelter",[(party_slot_eq, "$g_encountered_party",slot_party_type, spt_castle),
                          (ge, "$g_encountered_party_relation", 0)],
       "Request entry to the castle.",
       [(party_get_slot, ":castle_lord", "$g_encountered_party", slot_town_lord),
        (try_begin),
          (lt, ":castle_lord", 0),
          (jump_to_menu, "mnu_castle_entry_granted"),
        (else_try),
          (call_script, "script_troop_get_player_relation", ":castle_lord"),
          (assign, ":castle_lord_relation", reg0),
          #(troop_get_slot, ":castle_lord_relation", ":castle_lord", slot_troop_player_relation),
          (try_begin),
            (gt, ":castle_lord_relation", -15),
            (jump_to_menu, "mnu_castle_entry_granted"),
          (else_try),
            (jump_to_menu, "mnu_castle_entry_denied"),
          (try_end),
        (try_end),
       ]),
      ("request_meeting_commander",[],
       "Request a meeting with someone.",
       [
          (jump_to_menu, "mnu_castle_meeting"),
       ]),
      ("guard_leave",[],
       "Leave.",
       [(change_screen_return,0)]),
    ]
  ),
  (
    "castle_entry_granted",mnf_scale_picture,
    "After a brief wait, the guards open the gates for you and allow your party inside.",
    "none",
    [
		(call_script, "script_set_town_picture"),
    ],
    [
      ("continue",[],
       "Continue...",
       [(jump_to_menu,"mnu_town")]),
    ]
  ),
  (
    "castle_entry_denied",mnf_scale_picture,
    "The lord of this castle has forbidden you from coming inside these walls,\
 and the guard sergeant informs you that his men will fire if you attempt to come any closer.",
    "none",
    [
		(call_script, "script_set_town_picture"),
    ],
    [
      ("continue",[],
       "Continue...",
       [(jump_to_menu,"mnu_castle_guard")]),
    ]
  ),
  (
    "castle_meeting",mnf_scale_picture,
    "With whom do you want to meet?",
    "none",
    [
        (assign, "$num_castle_meeting_troops", 0),
        (try_for_range, ":troop_no", active_npcs_begin, active_npcs_end),
          (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
          (call_script, "script_get_troop_attached_party", ":troop_no"),
          (eq, "$g_encountered_party", reg0),
          (troop_set_slot, "trp_temp_array_a", "$num_castle_meeting_troops", ":troop_no"),
          (val_add, "$num_castle_meeting_troops", 1),
        (try_end),
		(call_script, "script_set_town_picture"),
    ],
    [
      ("guard_meet_s5",[(gt, "$num_castle_meeting_troops", 0),(troop_get_slot, ":troop_no", "trp_temp_array_a", 0),(str_store_troop_name, s5, ":troop_no")],
       "{s5}.",[(troop_get_slot, "$castle_meeting_selected_troop", "trp_temp_array_a", 0),(jump_to_menu,"mnu_castle_meeting_selected")]),
      ("guard_meet_s5",[(gt, "$num_castle_meeting_troops", 1),(troop_get_slot, ":troop_no", "trp_temp_array_a", 1),(str_store_troop_name, s5, ":troop_no")],
       "{s5}.",[(troop_get_slot, "$castle_meeting_selected_troop", "trp_temp_array_a", 1),(jump_to_menu,"mnu_castle_meeting_selected")]),
      ("guard_meet_s5",[(gt, "$num_castle_meeting_troops", 2),(troop_get_slot, ":troop_no", "trp_temp_array_a", 2),(str_store_troop_name, s5, ":troop_no")],
       "{s5}.",[(troop_get_slot, "$castle_meeting_selected_troop", "trp_temp_array_a", 2),(jump_to_menu,"mnu_castle_meeting_selected")]),
      ("guard_meet_s5",[(gt, "$num_castle_meeting_troops", 3),(troop_get_slot, ":troop_no", "trp_temp_array_a", 3),(str_store_troop_name, s5, ":troop_no")],
       "{s5}.",[(troop_get_slot, "$castle_meeting_selected_troop", "trp_temp_array_a", 3),(jump_to_menu,"mnu_castle_meeting_selected")]),
      ("guard_meet_s5",[(gt, "$num_castle_meeting_troops", 4),(troop_get_slot, ":troop_no", "trp_temp_array_a", 4),(str_store_troop_name, s5, ":troop_no")],
       "{s5}.",[(troop_get_slot, "$castle_meeting_selected_troop", "trp_temp_array_a", 4),(jump_to_menu,"mnu_castle_meeting_selected")]),
      ("guard_meet_s5",[(gt, "$num_castle_meeting_troops", 5),(troop_get_slot, ":troop_no", "trp_temp_array_a", 5),(str_store_troop_name, s5, ":troop_no")],
       "{s5}.",[(troop_get_slot, "$castle_meeting_selected_troop", "trp_temp_array_a", 5),(jump_to_menu,"mnu_castle_meeting_selected")]),
      ("guard_meet_s5",[(gt, "$num_castle_meeting_troops", 6),(troop_get_slot, ":troop_no", "trp_temp_array_a", 6),(str_store_troop_name, s5, ":troop_no")],
       "{s5}.",[(troop_get_slot, "$castle_meeting_selected_troop", "trp_temp_array_a", 6),(jump_to_menu,"mnu_castle_meeting_selected")]),
      ("guard_meet_s5",[(gt, "$num_castle_meeting_troops", 7),(troop_get_slot, ":troop_no", "trp_temp_array_a", 7),(str_store_troop_name, s5, ":troop_no")],
       "{s5}.",[(troop_get_slot, "$castle_meeting_selected_troop", "trp_temp_array_a", 7),(jump_to_menu,"mnu_castle_meeting_selected")]),
      ("guard_meet_s5",[(gt, "$num_castle_meeting_troops", 8),(troop_get_slot, ":troop_no", "trp_temp_array_a", 8),(str_store_troop_name, s5, ":troop_no")],
       "{s5}.",[(troop_get_slot, "$castle_meeting_selected_troop", "trp_temp_array_a", 8),(jump_to_menu,"mnu_castle_meeting_selected")]),
      ("guard_meet_s5",[(gt, "$num_castle_meeting_troops", 9),(troop_get_slot, ":troop_no", "trp_temp_array_a", 9),(str_store_troop_name, s5, ":troop_no")],
       "{s5}.",[(troop_get_slot, "$castle_meeting_selected_troop", "trp_temp_array_a", 9),(jump_to_menu,"mnu_castle_meeting_selected")]),
      
      ("forget_it",[],
       "Forget it.",
       [(jump_to_menu,"mnu_castle_guard")]),
    ]
  ),
  (
    "castle_meeting_selected",0,
    "Your request for a meeting is relayed inside, and finally {s6} appears in the courtyard to speak with you.",
    "none",
    [(str_store_troop_name, s6, "$castle_meeting_selected_troop")],
    [
      ("continue",[],
       "Continue...",
       [(jump_to_menu, "mnu_castle_outside"),
        (modify_visitors_at_site,"scn_conversation_scene"),(reset_visitors),
        (set_visitor,0,"trp_player"),
        (set_visitor,17,"$castle_meeting_selected_troop"),
        (set_jump_mission,"mt_conversation_encounter"),
        (jump_to_scene,"scn_conversation_scene"),
        (assign, "$talk_context", tc_castle_gate),
        (change_screen_map_conversation, "$castle_meeting_selected_troop"),
        ]),
    ]
  ),
   (
    "castle_besiege",mnf_scale_picture,
    "You are laying siege to {s1}. {s2} {s3}",
    "none",
    [
		#gekokujo only one type of siege sighted pic
		(set_background_mesh, "mesh_gekokujo_pic_siege_sighted"),
	#	##diplomacy start+ test gender with script
    #    #(troop_get_type, ":is_female", "trp_player"),#<- replaced
    #    (try_begin),
    #      #(eq, ":is_female", 1),#<- replaced
	#      (eq, 1, "$character_gender"),#<- added
    #      (set_background_mesh, "mesh_pic_siege_sighted_fem"),
    #    (else_try),
    #      (set_background_mesh, "mesh_pic_siege_sighted"),
    #    (try_end),
	#	##diplomacy end+
        (assign, "$g_siege_force_wait", 0),
        (try_begin),
          (party_slot_eq, "$g_encountered_party", slot_center_is_besieged_by, -1),
          (party_set_slot, "$g_encountered_party", slot_center_is_besieged_by, "p_main_party"),
          (store_current_hours, ":cur_hours"),
          (party_set_slot, "$g_encountered_party", slot_center_siege_begin_hours, ":cur_hours"),
          (assign, "$g_siege_method", 0),
          (assign, "$g_siege_sallied_out_once", 0),
        (try_end),

        (party_get_slot, ":town_food_store", "$g_encountered_party", slot_party_food_store),
        (call_script, "script_center_get_food_consumption", "$g_encountered_party"),
        (assign, ":food_consumption", reg0),
        (assign, reg7, ":food_consumption"),
        (assign, reg8, ":town_food_store"),
        (store_div, reg3, ":town_food_store", ":food_consumption"),
        
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
          (party_slot_eq, "$g_encountered_party", slot_party_type, spt_town),
          (assign, reg6, 1),
        (else_try),
          (assign, reg6, 0),
        (try_end),
        
        (try_begin),
          (gt, reg3, 0),
          (str_store_string, s2, "@The {reg6?town's:castle's} food stores should last for {reg3} more days."),
        (else_try),
          (str_store_string, s2, "@The {reg6?town's:castle's} food stores have run out and the defenders are starving."),
        (try_end),

        (str_store_string, s3, "str_empty_string"),
        (try_begin),
          (ge, "$g_siege_method", 1),
          (store_current_hours, ":cur_hours"),
          (try_begin),
            (lt, ":cur_hours",  "$g_siege_method_finish_hours"),
            (store_sub, reg9, "$g_siege_method_finish_hours", ":cur_hours"),
            (try_begin),
              (eq, "$g_siege_method", 1),
              (str_store_string, s3, "@You're preparing to attack the gates, the work should finish in {reg9} hours."),
            (else_try),
              (eq, "$g_siege_method", 2),
			  #gekokujo 3.0 siege towers are deprecated
              #(str_store_string, s3, "@Your forces are building a siege tower. They estimate another {reg9} hours to complete the build."),
			  #gekokujo 3.0 ninja infiltration
			  (str_store_string, s3, "@Your agents are inside, attempting to weaken the gates at first opportunity. They expect good news {reg9} hours from now."),
            #gekokujo 3.1 kyoto siege start
            (else_try),
              (eq, "$g_siege_method", 3),
              (str_store_string, s3, "@Your commanders are conferring with each other to plan the upcoming fight in the streets. They expect a solid report {reg9} hours from now."),
            #gekokujo 3.1 kyoto siege end
            (try_end),
          (else_try),
            (try_begin),
              (eq, "$g_siege_method", 1),
              (str_store_string, s3, "@Your sappers have knocked down the first gate from afar! You are ready to attack the castle at any time."),
            (else_try),
              (eq, "$g_siege_method", 2),
			  #gekokujo 3.0 siege towers are deprecated
              #(str_store_string, s3, "@The siege tower is built and ready to make an assault."),
			  #gekokujo 3.0 ninja infiltration
              (str_store_string, s3, "@Your agents have weakened the enemy gates from the inside! You are ready to attack the castle at any time."),
            #gekokujo 3.1 kyoto siege start
            (else_try),
              (eq, "$g_siege_method", 3),
              (str_store_string, s3, "@Your commanders have pinpointed the weaknesses in the defense! You are ready to attack the enemy at any time."),
            #gekokujo 3.1 kyoto siege end
            (try_end),
          (try_end),
        (try_end),
        
        #Check if enemy leaves the castle to us...
        (try_begin),
          (eq, "$g_castle_left_to_player",1), #we come here after dialog. Empty the castle and send parties away.
          (assign, "$g_castle_left_to_player",0),
          (store_faction_of_party, ":castle_faction", "$g_encountered_party"),
          (party_set_faction,"$g_encountered_party","fac_neutral"), #temporarily erase faction so that it is not the closest town
          (party_get_num_attached_parties, ":num_attached_parties_to_castle","$g_encountered_party"),
          (try_for_range_backwards, ":iap", 0, ":num_attached_parties_to_castle"),
            (party_get_attached_party_with_rank, ":attached_party", "$g_encountered_party", ":iap"),
            (party_detach, ":attached_party"),
            (party_get_slot, ":attached_party_type", ":attached_party", slot_party_type),
            (eq, ":attached_party_type", spt_kingdom_hero_party),
            (store_faction_of_party, ":attached_party_faction", ":attached_party"),
            (call_script, "script_get_closest_walled_center_of_faction", ":attached_party", ":attached_party_faction"),
            (try_begin),
              (gt, reg0, 0),
              (call_script, "script_party_set_ai_state", ":attached_party", spai_holding_center, reg0),
            (else_try),
              (call_script, "script_party_set_ai_state", ":attached_party", spai_patrolling_around_center, "$g_encountered_party"),
            (try_end),
          (try_end),
          (call_script, "script_party_remove_all_companions", "$g_encountered_party"),
          (change_screen_return),
          (party_collect_attachments_to_party, "$g_encountered_party", "p_collective_enemy"), #recalculate so that
          (call_script, "script_party_copy", "p_encountered_party_backup", "p_collective_enemy"), #leaving troops will not be considered as captured
          (party_set_faction,"$g_encountered_party",":castle_faction"), 
        (try_end),

        #Check for victory or defeat....
        (assign, "$g_enemy_party", "$g_encountered_party"),
        (assign, "$g_ally_party", -1),
        (str_store_party_name, 1,"$g_encountered_party"),
        (call_script, "script_encounter_calculate_fit"),
        
        (assign, reg11, "$g_enemy_fit_for_battle"),
        (assign, reg10, "$g_friend_fit_for_battle"),


        (try_begin),
          (eq, "$g_leave_encounter",1),
          (change_screen_return),
        ##diplomacy begin
        (else_try),
          (party_slot_eq, "$g_encountered_party", slot_village_infested_by_bandits, "trp_peasant_woman"),
          (call_script, "script_party_count_fit_regulars","p_collective_enemy"),
          (assign, ":enemy_finished", 0),
          (try_begin),
            (eq, "$g_battle_result", 1),
            (assign, ":enemy_finished", 1),
          (else_try),
            (le, "$g_enemy_fit_for_battle", 0),
            (ge, "$g_friend_fit_for_battle", 1),
            (assign, ":enemy_finished", 1),
          (try_end),
          (this_or_next|eq, ":enemy_finished", 1),
          (eq, "$g_enemy_surrenders", 1),
          (assign, "$g_next_menu", "mnu_dplmc_town_riot_removed"),
          (jump_to_menu, "mnu_total_victory"),
        ##diplomacy end
        (else_try),
          (call_script, "script_party_count_fit_regulars","p_collective_enemy"),
          (assign, ":enemy_finished", 0),
          (try_begin),
            (eq, "$g_battle_result", 1),
            (assign, ":enemy_finished", 1),
          (else_try),
            (le, "$g_enemy_fit_for_battle", 0),
            (ge, "$g_friend_fit_for_battle", 1),
            (assign, ":enemy_finished", 1),
          (try_end),
          (this_or_next|eq, ":enemy_finished", 1),
          (eq, "$g_enemy_surrenders", 1),

          (assign, "$g_next_menu", "mnu_castle_taken"), 
          (jump_to_menu, "mnu_total_victory"),
        (else_try),
          (call_script, "script_party_count_members_with_full_health", "p_main_party"),
          (assign, ":main_party_fit_regulars", reg0),
          (eq, "$g_battle_result", -1),
          (eq, ":main_party_fit_regulars", 0), #all lost (TODO : )
          (assign, "$g_next_menu", "mnu_captivity_start_castle_defeat"),
          (jump_to_menu, "mnu_total_defeat"),
        (try_end),
    ],
    [
      ("siege_request_meeting",[(eq, "$cant_talk_to_enemy", 0)],"Call for a meeting with the castle commander.", [
          (assign, "$cant_talk_to_enemy", 1),
          (assign, "$g_enemy_surrenders",0),
          (assign, "$g_castle_left_to_player",0),
          (assign, "$talk_context", tc_castle_commander),
          (party_get_num_attached_parties, ":num_attached_parties_to_castle","$g_encountered_party"),
          (try_begin),
            (gt, ":num_attached_parties_to_castle", 0),
            (party_get_attached_party_with_rank, ":leader_attached_party", "$g_encountered_party", 0),
            (call_script, "script_setup_party_meeting", ":leader_attached_party"),
          (else_try),
            (call_script, "script_setup_party_meeting", "$g_encountered_party"),
          (try_end),
           ]),
        
      ("wait_24_hours",[],"Wait until tomorrow.", [
          (assign,"$auto_besiege_town","$g_encountered_party"),
          (assign, "$g_siege_force_wait", 1),
          (store_time_of_day,":cur_time_of_day"),
          (val_add, ":cur_time_of_day", 1),
          (assign, ":time_to_wait", 31),
          (val_sub,":time_to_wait",":cur_time_of_day"),
          (val_mod,":time_to_wait",24),
          (val_add, ":time_to_wait", 1),
          (rest_for_hours_interactive, ":time_to_wait", 5, 1), #rest while attackable
          (assign, "$cant_talk_to_enemy", 0),
          (change_screen_return),
          ]),

      
      ("castle_lead_attack",
       [
         (neg|troop_is_wounded, "trp_player"),
         (ge, "$g_siege_method", 1),
         (gt, "$g_friend_fit_for_battle", 3),
         (store_current_hours, ":cur_hours"),
         (ge, ":cur_hours", "$g_siege_method_finish_hours"),
       ],
       "Lead your men in an assault.", 
       [
           (try_begin),
             (party_slot_eq, "$g_encountered_party", slot_party_type, spt_town),
             (party_get_slot, ":battle_scene", "$g_encountered_party", slot_town_walls),
           (else_try),
             (party_get_slot, ":battle_scene", "$g_encountered_party", slot_castle_exterior),
           (try_end),

           (call_script, "script_calculate_renown_value"),            
           (call_script, "script_calculate_battle_advantage"),
           (assign, ":battle_advantage", reg0),
           (val_mul, ":battle_advantage", 2),
           (val_div, ":battle_advantage", 3), #scale down the advantage a bit in sieges.
           (set_battle_advantage, ":battle_advantage"),
           (set_party_battle_mode),
           (assign, "$g_siege_battle_state", 1),
           (assign, ":siege_sally", 0),
           (try_begin),
             (le, ":battle_advantage", -4), #we are outnumbered, defenders sally out
             (eq, "$g_siege_sallied_out_once", 0),
             (set_jump_mission,"mt_castle_attack_walls_defenders_sally"),
             (assign, "$g_siege_battle_state", 0),
             (assign, ":siege_sally", 1),
           (else_try),
             (party_slot_eq, "$current_town", slot_center_siege_with_belfry, 1),
			 #gekokujo revise belfry attack mission sometime
             (set_jump_mission,"mt_castle_attack_walls_ladder"),
             #(set_jump_mission,"mt_castle_attack_walls_belfry"),
           (else_try),
             (set_jump_mission,"mt_castle_attack_walls_ladder"),
           (try_end),
           (assign, "$cant_talk_to_enemy", 0),           
           (assign, "$g_siege_final_menu", "mnu_castle_besiege"),
           (assign, "$g_next_menu", "mnu_castle_besiege_inner_battle"),
           (assign, "$g_siege_method", 0), #reset siege timer
           (jump_to_scene,":battle_scene"),
           (try_begin),
             (eq, ":siege_sally", 1),
             (jump_to_menu, "mnu_siege_attack_meets_sally"),
           (else_try),
             (jump_to_menu, "mnu_battle_debrief"),
             (change_screen_mission),
           (try_end),
       ]),
      ("attack_stay_back",
       [
         (ge, "$g_siege_method", 1),
         (gt, "$g_friend_fit_for_battle", 3),
         (store_current_hours, ":cur_hours"),
         (ge, ":cur_hours",  "$g_siege_method_finish_hours"),
         ],
       "Order your soldiers to attack while you stay back...", [(assign, "$cant_talk_to_enemy", 0),(jump_to_menu,"mnu_castle_attack_walls_simulate")]),

      #gekokujo 3.0 ninja infiltration start
      ("use_agents",
        [
          (neq, "$current_town", "p_town_4"), #gekokujo 3.1 kyoto siege -- no gates to destroy
          (party_count_companions_of_type, ":agents", "p_main_party", "trp_hired_agent"),
          (party_count_companions_of_type, ":female_agents", "p_main_party", "trp_female_agent"),
          (val_add, ":agents", ":female_agents"),
          (party_count_companions_of_type, ":experienced_agents", "p_main_party", "trp_hired_agent_experienced"),
          (party_count_companions_of_type, ":female_experienced_agents", "p_main_party", "trp_female_agent_experienced"),
          (val_add, ":experienced_agents", ":female_experienced_agents"),
          
          (this_or_next|gt, ":agents", 0),
          (gt, ":experienced_agents", 0),
          (eq, "$g_siege_method", 0)
		],
       "Send in agents to weaken the gates from inside!", 
        [
          (jump_to_menu,"mnu_send_agents")
        ]),
      #gekokujo 3.0 ninja infiltration end
	   
      ("build_ladders",
        [
          (neq, "$current_town", "p_town_4"), #gekokujo 3.1 kyoto siege -- no gates to destroy
          (party_slot_eq, "$current_town", slot_center_siege_with_belfry, 0),
          (eq, "$g_siege_method", 0)],
       "Batter down the gates and storm the castle!", 
        [
          (jump_to_menu,"mnu_construct_ladders")
        ]),
        
       #gekokujo 3.1 kyoto siege start
      ("kyoto_siege",
        [
          (eq, "$current_town", "p_town_4"),
          (eq, "$g_siege_method", 0)],
       "Plan the fight in the streets!", 
        [
          (jump_to_menu,"mnu_besiege_kyoto")
        ]),
       #gekokujo 3.1 kyoto siege end

	  #gekokujo 3.0 siege towers are deprecated start
      #("build_siege_tower",[(party_slot_eq, "$current_town", slot_center_siege_with_belfry, 1),(eq, "$g_siege_method", 0)],
	  ##gekokujo revise belfry attack mission sometime
      # #"Build a siege tower.", [(jump_to_menu,"mnu_construct_siege_tower")]),
      # "Batter down the gates and storm the castle!", [(jump_to_menu,"mnu_construct_ladders")]),
	  #gekokujo 3.0 siege towers are deprecated end

      ("cheat_castle_lead_attack",[(eq, "$cheat_mode", 1),
                                   (eq, "$g_siege_method", 0)],
       "{!}CHEAT: Instant build equipments.",
       [
         (assign, "$g_siege_method", 1),
         (assign, "$gekokujo_siege_type", 0), #engineering-based #gekokujo 3.1 siege improvement
         (assign, "$g_siege_method_finish_hours", 0),
         (jump_to_menu, "mnu_castle_besiege"),
       ]),
       
      ("cheat_castle_lead_attack_2",[(eq, "$cheat_mode", 1),
                                   (eq, "$g_siege_method", 0)],
       "{!}CHEAT: Instant ninja infiltration.",
       [
         (assign, "$g_siege_method", 1),
         (assign, "$gekokujo_siege_type", 1), #agent-based #gekokujo 3.1 siege improvement
         (assign, "$g_siege_method_finish_hours", 0),
         (jump_to_menu, "mnu_castle_besiege"),
       ]),

      ("cheat_conquer_castle",[(eq, "$cheat_mode", 1),
                                   ],
       "{!}CHEAT: Instant conquer castle.",
       [
        (assign, "$g_next_menu", "mnu_castle_taken"),
        (jump_to_menu, "mnu_total_victory"),
       ]),
	   
      ("lift_siege",[],"Abandon the siege.",
       [
         (call_script, "script_lift_siege", "$g_player_besiege_town", 0),
         (assign,"$g_player_besiege_town", -1),
         (change_screen_return)]),
    ]
  ),
  
  (
    "siege_attack_meets_sally",mnf_scale_picture,
    "The defenders sally out to meet your assault.",
    "none",
    [
        #(set_background_mesh, "mesh_pic_sally_out"),
		#gekokujo new sally pic
		(set_background_mesh, "mesh_gekokujo_pic_sally_out"),
    ],
    [
      ("continue",[],
       "Continue...",
       [
             (jump_to_menu, "mnu_battle_debrief"),
             (change_screen_mission),
       ]),
    ]
  ),
   (
    "castle_besiege_inner_battle",mnf_scale_picture,
    "{s1}",
    "none",
    [
		#gekokujo only one type of siege sighted pic
		(set_background_mesh, "mesh_gekokujo_pic_siege_sighted"),
	#	##diplomacy start+ test gender with script
    #    #(troop_get_type, ":is_female", "trp_player"),#<- replaced
    #    (try_begin),
    #      #(eq, ":is_female", 1),#<- replaced
	#	  (eq, 1, "$character_gender"),#<- added
    #      (set_background_mesh, "mesh_pic_siege_sighted_fem"),
    #    (else_try),
    #      (set_background_mesh, "mesh_pic_siege_sighted"),
    #    (try_end),
	#	##diplomacy end+
        (assign, ":result", "$g_battle_result"),#will be reset at script_encounter_calculate_fit
        (call_script, "script_encounter_calculate_fit"),
        
# TODO: To use for the future:
            (str_store_string, s1, "@As a last defensive effort, you retreat to the main hall of the keep.\
 You and your remaining soldiers will put up a desperate fight here. If you are defeated, there's no other place to fall back to."),
            (str_store_string, s1, "@You've been driven away from the walls.\
 Now the attackers are pouring into the streets. IF you can defeat them, you can perhaps turn the tide and save the day."),
        (try_begin),
          (this_or_next|neq, ":result", 1),
          (this_or_next|le, "$g_friend_fit_for_battle", 0),
          (le, "$g_enemy_fit_for_battle", 0),
          (jump_to_menu, "$g_siege_final_menu"),
        (else_try),
          (call_script, "script_encounter_calculate_fit"),
          (party_slot_eq, "$g_encountered_party", slot_party_type, spt_town),
          (try_begin),
            (eq, "$g_siege_battle_state", 0),
            (eq, ":result", 1),
            (assign, "$g_battle_result", 0),
            (jump_to_menu, "$g_siege_final_menu"),
          (else_try),
            (eq, "$g_siege_battle_state", 1),
            (eq, ":result", 1),
            (str_store_string, s1, "@You've breached the town walls,\
 but the stubborn defenders continue to resist you in the streets!\
 You'll have to deal with them before you can attack the keep at the heart of the town."),
          (else_try),
            (eq, "$g_siege_battle_state", 2),
            (eq, ":result", 1),
            (str_store_string, s1, "@The town centre is yours,\
 but the remaining defenders have retreated to the castle.\
 It must fall before you can complete your victory."),
          (else_try),
            (jump_to_menu, "$g_siege_final_menu"),
          (try_end),
        (else_try),
          (try_begin),
            (eq, "$g_siege_battle_state", 0),
            (eq, ":result", 1),
            (assign, "$g_battle_result", 0),
            (jump_to_menu, "$g_siege_final_menu"),
          (else_try),
            (eq, "$g_siege_battle_state", 1),
            (eq, ":result", 1),
            (str_store_string, s1, "@The remaining defenders have retreated to the castle as a last defense. You must go in and crush any remaining resistance."),
          (else_try),
            (jump_to_menu, "$g_siege_final_menu"),
          (try_end),
        (try_end),
    ],
    [
      ("continue",[],
       "Continue...",
       [
           (try_begin),
             (party_slot_eq, "$g_encountered_party", slot_party_type, spt_town),
             (try_begin),
               (eq, "$g_siege_battle_state", 1),
               (party_get_slot, ":battle_scene", "$g_encountered_party", slot_town_center),
               (set_jump_mission, "mt_besiege_inner_battle_town_center"),
             (else_try),
               (party_get_slot, ":battle_scene", "$g_encountered_party", slot_town_castle),
               (set_jump_mission, "mt_besiege_inner_battle_castle"),
             (try_end),
           (else_try),
             (party_get_slot, ":battle_scene", "$g_encountered_party", slot_town_castle),
             (set_jump_mission, "mt_besiege_inner_battle_castle"),
           (try_end),
##           (call_script, "script_calculate_battle_advantage"),
##           (set_battle_advantage, reg0),
           (set_party_battle_mode),
           (jump_to_scene, ":battle_scene"),
           (val_add, "$g_siege_battle_state", 1),
           (assign, "$g_next_menu", "mnu_castle_besiege_inner_battle"),
           (jump_to_menu, "mnu_battle_debrief"),
           (change_screen_mission),
       ]),
    ]
  ),
  
  (
    "construct_ladders",0,
    "As the party member with the highest Engineer skill ({reg2}), {reg3?you estimate:{s3} estimates} that it will take\
 {reg4} hours to sap the first gate and get ready for the assault.",
    "none",
    [(call_script, "script_get_max_skill_of_player_party", "skl_engineer"),
     (assign, ":max_skill", reg0),
     (assign, ":max_skill_owner", reg1),
     (assign, reg2, ":max_skill"),

	 #gekokujo 3.0 make sieges halfway between old ladders and siege towers start
     #(store_sub, reg4, 14, ":max_skill"),
     #(val_mul, reg4, 2),
     #(val_div, reg4, 3),
     (store_sub, reg4, 12, ":max_skill"),
     (val_mul, reg4, 3),
	 #gekokujo 3.0 make sieges halfway between old ladders and siege towers end
     
     (try_begin),
       (eq, ":max_skill_owner", "trp_player"),
       (assign, reg3, 1),
     (else_try),
       (assign, reg3, 0),
       (str_store_troop_name, s3, ":max_skill_owner"),
     (try_end),
    ],
    [
      ("build_ladders_cont",[],
       "Do it.", [
           (assign, "$g_siege_method", 1),
           (store_current_hours, ":cur_hours"),
           (call_script, "script_get_max_skill_of_player_party", "skl_engineer"),
		   #gekokujo 3.0 make sieges halfway between old ladders and siege towers start
           #(store_sub, ":hours_takes", 14, reg0),
           #(val_mul, ":hours_takes", 2),
           #(val_div, ":hours_takes", 3),
           (store_sub, ":hours_takes", 12, reg0),
           (val_mul, ":hours_takes", 3),
		   #gekokujo 3.0 make sieges halfway between old ladders and siege towers end
           (store_add, "$g_siege_method_finish_hours",":cur_hours", ":hours_takes"),
           (assign,"$auto_besiege_town","$current_town"),
           (assign, "$gekokujo_siege_type", 0), #engineering-based #gekokujo 3.1 siege improvement
           (rest_for_hours_interactive, 96, 5, 1), #rest while attackable. A trigger will divert control when attack is ready.
           (change_screen_return),
           ]),
      ("go_back",[],
       "Go back.", [(jump_to_menu,"mnu_castle_besiege")]),
        ],
  ),
  

  #gekokujo 3.0 ninja infiltration start
  (
    "send_agents",0,
    "Your party contains {reg0} agents in total, with {reg1} of them having a great wealth of fieldcraft experience. \
 They expect to take {reg2} hours getting inside and sabotaging the gates.",
    "none",
    [(party_count_companions_of_type, reg0, "p_main_party", "trp_hired_agent"),
	 (party_count_companions_of_type, ":female_agents", "p_main_party", "trp_female_agent"),
     (val_add, reg0, ":female_agents"),
	 
	 (party_count_companions_of_type, reg1, "p_main_party", "trp_hired_agent_experienced"),
	 (party_count_companions_of_type, ":female_experienced_agents", "p_main_party", "trp_female_agent_experienced"),
     (val_add, reg1, ":female_experienced_agents"),
	 
     (val_add, reg0, reg1),

     (store_sub, reg2, 36, reg0), #subtract total agents
     (val_sub, reg2, reg1), #subtract experienced agents (they count for twice)
	 (val_clamp, reg2, 6, 36), #only up to 30 agents or 15 experienced agents will make a difference
    ],
    [
      ("send_agents_cont",[],
       "Do it.", [
           (assign, "$g_siege_method", 2),
           (store_current_hours, ":cur_hours"),
		   
           (party_count_companions_of_type, ":total_agents", "p_main_party", "trp_hired_agent"),
           (party_count_companions_of_type, ":female_agents", "p_main_party", "trp_female_agent"),
		   (val_add, ":total_agents", ":female_agents"),
		   
		   (party_count_companions_of_type, ":experienced_agents", "p_main_party", "trp_hired_agent_experienced"),
		   (party_count_companions_of_type, ":experienced_female_agents", "p_main_party", "trp_female_agent_experienced"),
		   (val_add, ":experienced_agents", ":experienced_female_agents"),
		   
		   (val_add, ":total_agents", ":experienced_agents"),
		   
		   (store_sub, ":hours_takes", 36, ":total_agents"),
		   (val_sub, ":hours_takes", ":experienced_agents"),
		   (val_clamp, ":hours_takes", 6, 36),
		   
           (store_add, "$g_siege_method_finish_hours",":cur_hours", ":hours_takes"),
           (assign,"$auto_besiege_town","$current_town"),
           (assign, "$gekokujo_siege_type", 1), #agent-based #gekokujo 3.1 siege improvement
           (rest_for_hours_interactive, 96, 5, 1), #rest while attackable. A trigger will divert control when attack is ready.
           (change_screen_return),
           ]),
      ("go_back",[],
       "Go back.", [(jump_to_menu,"mnu_castle_besiege")]),
        ],
  ),
  #gekokujo 3.0 ninja infiltration end

  #gekokujo 3.1 kyoto siege start
  (
    "besiege_kyoto",0,
    "As the party member with the highest Tactics skill ({reg2}), {reg3?you estimate:{s3} estimates} that it will take\
 {reg4} hours to plan the assault through Kyoto's streets.",
    "none",
    [(call_script, "script_get_max_skill_of_player_party", "skl_tactics"),
     (assign, ":max_skill", reg0),
     (assign, ":max_skill_owner", reg1),
     (assign, reg2, ":max_skill"),

     (store_sub, reg4, 12, ":max_skill"),
     (val_mul, reg4, 3),
     
     (try_begin),
       (eq, ":max_skill_owner", "trp_player"),
       (assign, reg3, 1),
     (else_try),
       (assign, reg3, 0),
       (str_store_troop_name, s3, ":max_skill_owner"),
     (try_end),
    ],
    [
      ("besiege_kyoto_cont",[],
       "Do it.", [
           (assign, "$g_siege_method", 3),
           (store_current_hours, ":cur_hours"),
           (call_script, "script_get_max_skill_of_player_party", "skl_tactics"),
           (store_sub, ":hours_takes", 12, reg0),
           (val_mul, ":hours_takes", 3),
           (store_add, "$g_siege_method_finish_hours",":cur_hours", ":hours_takes"),
           (assign,"$auto_besiege_town","$current_town"),
           (assign, "$gekokujo_siege_type", 2), #kyoto siege, doesn't actually do anything
           (rest_for_hours_interactive, 96, 5, 1), #rest while attackable. A trigger will divert control when attack is ready.
           (change_screen_return),
           ]),
      ("go_back",[],
       "Go back.", [(jump_to_menu,"mnu_castle_besiege")]),
        ],
  ),
  #gekokujo 3.1 kyoto siege end
  
  #gekokujo 3.0 siege towers are deprecated start
  #(
  #  "construct_siege_tower",0,
  #  "As the party member with the highest Engineer skill ({reg2}), {reg3?you estimate:{s3} estimates} that building a siege tower will take\
# {reg4} hours.",
  #  "none",
  #  [(call_script, "script_get_max_skill_of_player_party", "skl_engineer"),
  #   (assign, ":max_skill", reg0),
  #   (assign, ":max_skill_owner", reg1),
  #   (assign, reg2, ":max_skill"),
  #
  #   (store_sub, reg4, 15, ":max_skill"),
  #   (val_mul, reg4, 6),
  #   
  #   (try_begin),
  #     (eq, ":max_skill_owner", "trp_player"),
  #     (assign, reg3, 1),
  #   (else_try),
  #     (assign, reg3, 0),
  #     (str_store_troop_name, s3, ":max_skill_owner"),
  #   (try_end),
  #  ],
  #  [
  #    ("build_siege_tower_cont",[],
  #     "Start building.", [
  #         (assign, "$g_siege_method", 2),
  #         (store_current_hours, ":cur_hours"),
  #         (call_script, "script_get_max_skill_of_player_party", "skl_engineer"),
  #         (store_sub, ":hours_takes", 15, reg0),
  #         (val_mul, ":hours_takes", 6),
  #         (store_add, "$g_siege_method_finish_hours",":cur_hours", ":hours_takes"),
  #         (assign,"$auto_besiege_town","$current_town"),
  #         (rest_for_hours_interactive, 240, 5, 1), #rest while attackable. A trigger will divert control when attack is ready.
  #         (change_screen_return),
  #         ]),
  #    ("go_back",[],
  #     "Go back.", [(jump_to_menu,"mnu_castle_besiege")]),
  #      ],
  #),
  #gekokujo 3.0 siege towers are deprecated end

   (
    "castle_attack_walls_simulate",mnf_scale_picture|mnf_disable_all_keys,
    "{s4}^^Your casualties:{s8}^^Enemy casualties were: {s9}",
    "none",
    [
        (try_begin),
		  #gekokujo new siege attack pic
          #(set_background_mesh, "mesh_pic_siege_attack"),
          (set_background_mesh, "mesh_gekokujo_pic_siege_attack"),
        (try_end),
        ###diplomacy start+
		##If terrain advantage is on, use siege settings
        #(assign, ":save_dplmc_terrain_advantage", "$g_dplmc_terrain_advantage"),
		##(assign, "$g_dplmc_terrain_advantage", ":save_dplmc_terrain_advantage"),
		#(try_begin),
		#   (eq, "$g_dplmc_terrain_advantage", TERRAIN_ADVANTAGE_ENABLE),
		#   (assign, "$g_dplmc_terrain_advantage", TERRAIN_ADVANTAGE_FORCE_SIEGE),
		#(try_end),
		###diplomacy end+        
        (call_script, "script_party_calculate_strength", "p_main_party", 1), #skip player
        (assign, ":player_party_strength", reg0),
        (val_div, ":player_party_strength", 10),

        (call_script, "script_party_calculate_strength", "$g_encountered_party", 0),
        (assign, ":enemy_party_strength", reg0),
        (val_div, ":enemy_party_strength", 4),

        (inflict_casualties_to_party_group, "p_main_party", ":enemy_party_strength", "p_temp_casualties"),
        (call_script, "script_print_casualties_to_s0", "p_temp_casualties", 0),
        (str_store_string_reg, s8, s0),

        (inflict_casualties_to_party_group, "$g_encountered_party", ":player_party_strength", "p_temp_casualties"),
        (call_script, "script_print_casualties_to_s0", "p_temp_casualties", 0),
        (str_store_string_reg, s9, s0),

        (assign, "$no_soldiers_left", 0),
        (try_begin),
          (call_script, "script_party_count_members_with_full_health","p_main_party"),
          (le, reg0, 0), #(TODO : compare with num_routed_us)
          (assign, "$no_soldiers_left", 1),
          (str_store_string, s4, "str_attack_walls_failure"),
        (else_try),
          (call_script, "script_party_count_members_with_full_health","$g_encountered_party"),
          (le, reg0, 0), #(TODO : compare with num_routed_enemies)
          (assign, "$no_soldiers_left", 1),
          (assign, "$g_battle_result", 1),
          (str_store_string, s4, "str_attack_walls_success"),
        (else_try),
          (str_store_string, s4, "str_attack_walls_continue"),
        (try_end),
		##diplomacy start+
		#Revert terrain advantage settings
		#(assign, "$g_dplmc_terrain_advantage", ":save_dplmc_terrain_advantage"),
		##diplomacy end+
     ],
    [
##      ("lead_next_wave",[(eq, "$no_soldiers_left", 0)],"Lead the next wave of attack personally.", [
##           (party_get_slot, ":battle_scene", "$g_encountered_party", slot_castle_exterior),
##           (set_party_battle_mode),
##           (set_jump_mission,"mt_castle_attack_walls"),
##           (jump_to_scene,":battle_scene"),
##           (jump_to_menu,"mnu_castle_outside"),
##           (change_screen_mission),
##       ]),
##      ("continue_attacking",[(eq, "$no_soldiers_left", 0)],"Order your soldiers to keep attacking...", [
##                                    (jump_to_menu,"mnu_castle_attack_walls_3"),
##                                    ]),
##      ("call_soldiers_back",[(eq, "$no_soldiers_left", 0)],"Call your soldiers back.",[(jump_to_menu,"mnu_castle_outside")]),
      ("continue",[],"Continue...",[(jump_to_menu,"mnu_castle_besiege")]),
    ]
  ),
  
   (
    "castle_attack_walls_with_allies_simulate",mnf_scale_picture|mnf_disable_all_keys,
    "{s4}^^Your casualties: {s8}^^Allies' casualties: {s9}^^Enemy casualties: {s10}",
    "none",
    [
        (try_begin),
		  #gekokujo new siege attack pic
          #(set_background_mesh, "mesh_pic_siege_attack"),
          (set_background_mesh, "mesh_gekokujo_pic_siege_attack"),
        (try_end),
        ###diplomacy start+
		##If terrain advantage is on, use siege settings
        #(assign, ":save_dplmc_terrain_advantage", "$g_dplmc_terrain_advantage"),
		#(try_begin),
		#   (eq, "$g_dplmc_terrain_advantage", TERRAIN_ADVANTAGE_ENABLE),
		#   (assign, "$g_dplmc_terrain_advantage", TERRAIN_ADVANTAGE_FORCE_SIEGE),
		#(try_end),
		###diplomacy end+

        (call_script, "script_party_calculate_strength", "p_main_party", 1), #skip player
        (assign, ":player_party_strength", reg0),
        (val_div, ":player_party_strength", 10),
        (call_script, "script_party_calculate_strength", "p_collective_friends", 0),
        (assign, ":friend_party_strength", reg0),
        (val_div, ":friend_party_strength", 10),

        (val_max, ":friend_party_strength", 1),

        (call_script, "script_party_calculate_strength", "p_collective_enemy", 0),
        (assign, ":enemy_party_strength", reg0),
        (val_div, ":enemy_party_strength", 4),

##        (assign, reg0, ":player_party_strength"),
##        (assign, reg1, ":friend_party_strength"),
##        (assign, reg2, ":enemy_party_strength"),
##        (assign, reg3, "$g_enemy_party"),
##        (assign, reg4, "$g_ally_party"),
##        (display_message, "@{!}player_str={reg0} friend_str={reg1} enemy_str={reg2}"),
##        (display_message, "@{!}enemy_party={reg3} ally_party={reg4}"),

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
        (call_script, "script_print_casualties_to_s0", "p_temp_casualties", 0),
        (str_store_string_reg, s10, s0),

        (call_script, "script_collect_friendly_parties"),

        (inflict_casualties_to_party_group, "$g_ally_party", ":enemy_party_strength", "p_temp_casualties"),
        (call_script, "script_print_casualties_to_s0", "p_temp_casualties", 0),
        (str_store_string_reg, s9, s0),

        (party_collect_attachments_to_party, "$g_enemy_party", "p_collective_enemy"),

        (assign, "$no_soldiers_left", 0),
        (try_begin),
          (call_script, "script_party_count_members_with_full_health", "p_main_party"),
          (le, reg0, 0), #(TODO : compare with num_routed_us)
          (assign, "$no_soldiers_left", 1),
          (str_store_string, s4, "str_attack_walls_failure"),
        (else_try),
          (call_script, "script_party_count_members_with_full_health", "p_collective_enemy"),
          (le, reg0, 0), #(TODO : compare with num_routed_enemies)
          (assign, "$no_soldiers_left", 1),
          (assign, "$g_battle_result", 1),
          (str_store_string, s4, "str_attack_walls_success"),
        (else_try),
          (str_store_string, s4, "str_attack_walls_continue"),
        (try_end),
		###diplomacy start+
		##Revert terrain advantage settings
		#(assign, "$g_dplmc_terrain_advantage", ":save_dplmc_terrain_advantage"),
		###diplomacy end+
     ],
    [
      ("continue",[],"Continue...",[(jump_to_menu,"mnu_besiegers_camp_with_allies")]),
    ]
  ),
  (
    "castle_taken_by_friends",0,
    "Nothing to see here.",
    "none",
    [
        (party_clear, "$g_encountered_party"),
        (party_stack_get_troop_id, ":leader", "$g_encountered_party_2", 0),
        (party_set_slot, "$g_encountered_party", slot_center_last_taken_by_troop, ":leader"),
        (store_troop_faction, ":faction_no", ":leader"),
        #Reduce prosperity of the center by 5
        (call_script, "script_change_center_prosperity", "$g_encountered_party", -5),
		(try_begin),
			(assign, ":damage", 20),
			(is_between, "$g_encountered_party", towns_begin, towns_end),
			(assign, ":damage", 40),
		(try_end),
		(try_begin),
			(neq, ":faction_no", "$g_encountered_party_faction"),
			(call_script, "script_faction_inflict_war_damage_on_faction", ":faction_no", "$g_encountered_party_faction", ":damage"),
		(try_end),
		
        (call_script, "script_give_center_to_faction", "$g_encountered_party", ":faction_no"),
        (call_script, "script_add_log_entry", logent_player_participated_in_siege, "trp_player",  "$g_encountered_party", 0, "$g_encountered_party_faction"),
##        (call_script, "script_change_troop_renown", "trp_player", 1),
        (change_screen_return),
    ],
    [
    ],
  ),
  (
    "castle_taken",mnf_disable_all_keys,
	##diplomacy begin
    "{s3} has fallen to your troops, and you now have full control of the {reg2?town:castle}. You can plunder spoils of war worth {reg3} mon.\
{reg1? You may station troops here to defend it against enemies who may try to recapture it. Also, you should select now whether you will hold the {reg2?town:castle} yourself or give it to a faithful vassal...:}",# Only visible when castle is taken without being a vassal of a kingdom.
  ##diplomacy end
    "none",
    [
        (party_clear, "$g_encountered_party"),
		##diplomacy start+ Handle player is co-ruler of kingdom
		(assign, ":is_coruler", 0),
		(try_begin),
			(is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
			(call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", "$players_kingdom"),
			(ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
			(assign, ":is_coruler", 1),
		(try_end),
		##diplomacy end+
        (try_begin),        
		  ##diplomacy start+
		  (this_or_next|eq, ":is_coruler", 1),
		  ##diplomacy end+
          (eq, "$players_kingdom", "fac_player_supporters_faction"),
          (party_get_slot, ":new_owner", "$g_encountered_party", slot_town_lord),
          (neq, ":new_owner", "trp_player"),
          
          (try_for_range, ":unused", 0, 4),
            (call_script, "script_cf_reinforce_party", "$g_encountered_party"),
          (try_end),  
        (try_end),
        
        (call_script, "script_lift_siege", "$g_encountered_party", 0),
        (assign, "$g_player_besiege_town", -1),
                        
        (party_set_slot, "$g_encountered_party", slot_center_last_taken_by_troop, "trp_player"),
		##diplomacy start+ Set last taken time
		(store_current_hours, ":cur_hours"),
		(party_set_slot, "$g_encountered_party", dplmc_slot_center_last_transfer_time, ":cur_hours"),
		##diplomacy end+
        ##diplomacy begin
        #Reduce prosperity of the center by 5
        #(call_script, "script_change_center_prosperity", "$g_encountered_party", -5),
  		(try_begin),
  			(is_between, "$g_encountered_party", towns_begin, towns_end),
  			(store_random_in_range, ":random", 4000, 10000),
  		(else_try),
  		    (store_random_in_range, ":random", 1000, 8000),
  		(try_end),
  		(val_div, ":random", 100),
  		(val_mul, ":random", 100),
  		(assign, "$diplomacy_var", ":random"),
  		(assign, reg3, "$diplomacy_var"),
        ##diplomacy end

        (call_script, "script_change_troop_renown", "trp_player", 5),		

		(assign, ":damage", 20),
		(try_begin),
			(is_between, "$g_encountered_party", towns_begin, towns_end),
			(assign, ":damage", 40),
		(try_end),
		(call_script, "script_faction_inflict_war_damage_on_faction", "$players_kingdom", "$g_encountered_party_faction", ":damage"),
		
		#removed, is it duplicate (useless)? See 20 lines above.
        #(call_script, "script_add_log_entry", logent_castle_captured_by_player, "trp_player", "$g_encountered_party", -1, "$g_encountered_party_faction"),
        
        (try_begin),
          (is_between, "$players_kingdom", kingdoms_begin, kingdoms_end),
          (neq, "$players_kingdom", "fac_player_supporters_faction"),
          (call_script, "script_give_center_to_faction", "$g_encountered_party", "$players_kingdom"),
          (call_script, "script_order_best_besieger_party_to_guard_center", "$g_encountered_party", "$players_kingdom"),
          (jump_to_menu, "mnu_castle_taken_2"),
        (else_try),
          (call_script, "script_give_center_to_faction", "$g_encountered_party", "fac_player_supporters_faction"),          
          (call_script, "script_order_best_besieger_party_to_guard_center", "$g_encountered_party", "fac_player_supporters_faction"),
          (str_store_party_name, s3, "$g_encountered_party"),
          (assign, reg1, 0),
          (try_begin),
            (faction_slot_eq, "fac_player_supporters_faction", slot_faction_leader, "trp_player"),
            (assign, reg1, 1),
          (try_end),          
		  #(party_set_slot, "$g_encountered_party", slot_town_lord, stl_unassigned),		  
        (try_end),
        (assign, reg2, 0),
        (try_begin),
          (is_between, "$g_encountered_party", towns_begin, towns_end),
          (assign, reg2, 1),
        (try_end),
    ],
    [
##diplomacy begin
      ("dplmc_spoils_yourself",[],"Plunder it and keep the spoils all for yourself.",
       [
         (call_script, "script_change_center_prosperity", "$g_encountered_party", -8),
		 ##diplomacy start+
		 (assign, ":is_kingdom_leader", 0),
		 (try_begin),
			(is_between, "$players_kingdom", kingdoms_begin, kingdoms_end),
			(faction_get_slot, ":faction_leader", "$players_kingdom", slot_faction_leader),
			(ge, ":faction_leader", 0),
			(this_or_next|eq, ":faction_leader", "trp_player"),
			(this_or_next|troop_slot_eq, ":faction_leader", slot_troop_spouse, "trp_player"),
				(troop_slot_eq, "trp_player", slot_troop_spouse, ":faction_leader"),
			(assign, ":is_kingdom_leader", 1),
		 (else_try),
			(eq, "$players_kingdom", "fac_player_supporters_faction"),
			(assign, ":is_kingdom_leader", 1),
		 (try_end),
		 #Add support for promoted ladies
         #(try_for_range, ":troop_no", active_npcs_begin, active_npcs_end),
         (try_for_range, ":troop_no", heroes_begin, heroes_end),
		 ##diplomacy end+
           (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
           (store_troop_faction, ":troop_faction_no", ":troop_no"),
		   ##diplomacy start+
		   (this_or_next|eq, "$players_kingdom", ":troop_faction_no"),
			  (eq, "fac_player_supporters_faction", ":troop_faction_no"),
		   (this_or_next|eq, ":is_kingdom_leader", 1),
		   ##diplomacy end+
           (eq, "fac_player_supporters_faction", ":troop_faction_no"),
           (call_script, "script_change_player_relation_with_troop", ":troop_no", -2),
         (try_end),
         (try_begin),
           (gt, "$g_player_chamberlain", 0),
           (call_script, "script_dplmc_pay_into_treasury", "$diplomacy_var"),
         (else_try),
           (troop_add_gold, "trp_player", "$diplomacy_var"),
         (try_end),
         (call_script, "script_change_player_honor", -3),
         (assign, "$auto_enter_town", "$g_encountered_party"),
         (change_screen_return),
        ]),
      ("dplmc_spoils_accompanying_vassals",
      [
		##nested diplomacy start+
		#Add support for being the ruler or co-ruler of an original kingdom
          (is_between, "$players_kingdom", kingdoms_begin, kingdoms_end),
		  (faction_get_slot, ":faction_leader", "$players_kingdom", slot_faction_leader),
		  (this_or_next|eq, ":faction_leader", "trp_player"),
		  (this_or_next|troop_slot_eq, ":faction_leader", slot_troop_spouse, "trp_player"),
  		##nested diplomacy end+
          (eq, "$players_kingdom", "fac_player_supporters_faction"),
         (assign, ":vassal_count", 0),
		##nested diplomacy start+ add support for kingdom ladies, and the other faction options
        # (try_for_range, ":troop_no", active_npcs_begin, active_npcs_end),
		 (try_for_range, ":troop_no", heroes_begin, heroes_end),
  	    ##nested diplmacy end+
           (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
           (store_troop_faction, ":troop_faction_no", ":troop_no"),
		   ##nested diplomacy start+
		   (this_or_next|eq, "$players_kingdom", ":troop_faction_no"),
		   ##nested diplomacy end+
           (eq, "fac_player_supporters_faction", ":troop_faction_no"),
           (troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
           (ge, ":party_no", 1),
           (store_distance_to_party_from_party, ":distance","p_main_party", ":party_no"),
           (le, ":distance", 25),
           (val_add, ":vassal_count", 1),
         (try_end),
		 (gt, ":vassal_count", 0),
      ],"Plunder it and share the spoils equally between the vassals accompanying you and yourself.",
       [
         (assign, ":vassal_count", 1),
		 ##nested diplomacy start+
		 ##OLD:
         #(try_for_range, ":troop_no", active_npcs_begin, active_npcs_end),
         #  (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
         #  (store_troop_faction, ":troop_faction_no", ":troop_no"),
         #  (eq, "fac_player_supporters_faction", ":troop_faction_no"),
         #  (troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
         #  (ge, ":party_no", 1),
         #  (store_distance_to_party_from_party, ":distance","p_main_party", ":party_no"),
         #  (le, ":distance", 25),
         #  (val_add, ":vassal_count", 1),
         #  (call_script, "script_change_player_relation_with_troop", ":troop_no", 3),
         #(try_end),
		 #
		 #NEW:
		 #first loop through to count
		 (try_for_range, ":troop_no", heroes_begin, heroes_end),#promoted lady support
			(troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
			(store_troop_faction, ":troop_faction_no", ":troop_no"),
			(this_or_next|eq, "$players_kingdom", ":troop_faction_no"),#support for other faction arrangements
				(eq, "fac_player_supporters_faction", ":troop_faction_no"),
			(troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
			(ge, ":party_no", 1),
			(store_distance_to_party_from_party, ":distance","p_main_party", ":party_no"),
			(le, ":distance", 25),
			(val_add, ":vassal_count", 1),
		 (try_end),
		 (store_div, ":gold_per_lord", "$diplomacy_var", ":vassal_count"),
		 #now loop through to add gold/relation
		 (try_for_range, ":troop_no", heroes_begin, heroes_end),#promoted lady support
			(troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
			(store_troop_faction, ":troop_faction_no", ":troop_no"),
			(this_or_next|eq, "$players_kingdom", ":troop_faction_no"),#support for other faction arrangements
				(eq, "fac_player_supporters_faction", ":troop_faction_no"),
			(troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
			(ge, ":party_no", 1),
			(store_distance_to_party_from_party, ":distance","p_main_party", ":party_no"),
			(le, ":distance", 25),
			#add gold
			(call_script, "script_dplmc_distribute_gold_to_lord_and_holdings", ":gold_per_lord", ":troop_no"),
			#Relation adjustment
			(store_random_in_range, reg0, 0, 1000),
			(val_add, reg0, ":gold_per_lord"),
			(val_div, reg0, 1000),
			(gt, reg0, 0),
			(val_min, reg0, 4),
			(assign, ":relation_change", reg0),
			#Modify for personality
			(try_begin),
				#Lords who dislike raiding will be displeased by looting a town (but not a castle)
				(party_slot_eq, "$g_encountered_party", slot_party_type, spt_town),
				(call_script, "script_dplmc_get_troop_morality_value", ":troop_no", tmt_humanitarian),
				(try_begin),
					(gt, reg0, 0),#Some lords like raiding settlements less than others
					(val_sub, ":relation_change", reg0),
					(val_min, ":relation_change", -1),
				(else_try),
					(lt, reg0, 0),#Some lords like raiding settlements more than others
					(val_sub, ":relation_change", reg0),
					(val_min, ":relation_change", 5),
				(else_try),
					(this_or_next|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_custodian),
					(this_or_next|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_benefactor),
						(troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_moralist),
					(val_sub, ":relation_change", 1),
			    (try_end),
			(try_end),
			(call_script, "script_change_player_relation_with_troop", ":troop_no", ":relation_change"),
		 (try_end),
		 ##nested diplomacy end+
         (val_div, "$diplomacy_var", ":vassal_count"),
         (try_begin),
           (gt, "$g_player_chamberlain", 0),
           (call_script, "script_dplmc_pay_into_treasury", "$diplomacy_var"),
         (else_try),
           (troop_add_gold, "trp_player", "$diplomacy_var"),
         (try_end),
         (call_script, "script_change_center_prosperity", "$g_encountered_party", -8),
         (call_script, "script_change_player_honor", -1),
         (assign, "$auto_enter_town", "$g_encountered_party"),
         (change_screen_return),
        ]),
      ("dplmc_spoils_all_vassals",
      [
          (is_between, "$players_kingdom", kingdoms_begin, kingdoms_end),
		  ##nested diplomacy start+
		  #Support for being co-ruler of an original kingdom
		  (faction_get_slot, ":faction_leader", "$players_kingdom", slot_faction_leader),
		  (this_or_next|eq, ":faction_leader", "trp_player"),
		  (this_or_next|troop_slot_eq, ":faction_leader", slot_troop_spouse, "trp_player"),
		  ##nested diplomacy end+
          (eq, "$players_kingdom", "fac_player_supporters_faction"),
      ],"Plunder it and share the spoils equally between your vassals and yourself.",
       [
         (assign, ":vassal_count", 1),
		 ##nested diplomacy start+
		 #OLD:
         #(try_for_range, ":troop_no", active_npcs_begin, active_npcs_end),
         #  (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
         #  (store_troop_faction, ":troop_faction_no", ":troop_no"),
         #  (eq, "fac_player_supporters_faction", ":troop_faction_no"),
         #  (val_add, ":vassal_count", 1),
         #  (call_script, "script_change_player_relation_with_troop", ":troop_no", 2),
         #(try_end),
		 #
		 #NEW:
		 #  1. Actually give the gold to your vassals;
		 #  2. Support kingdom ladies as vassals
		 #  3. Support being the ruler or co-ruler of an original kingdom
		 #  4. The relationship gain should not exceed 1 per 1000 gold pieces.
		 (try_for_range, ":troop_no", heroes_begin, heroes_end),
			(troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
			(store_troop_faction, ":troop_faction_no", ":troop_no"),
			(this_or_next|eq, ":troop_faction_no", "fac_player_supporters_faction"),
				(eq, ":troop_faction_no", "$players_kingdom"),
			(val_add, ":vassal_count", 1),
		 (try_end),

		 (store_div, ":gold_per_lord", "$diplomacy_var", ":vassal_count"),
		 (try_for_range, ":troop_no", heroes_begin, heroes_end),
			(troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
			(store_troop_faction, ":troop_faction_no", ":troop_no"),
			(this_or_next|eq, ":troop_faction_no", "fac_player_supporters_faction"),
				(eq, ":troop_faction_no", "$players_kingdom"),
			(call_script, "script_dplmc_distribute_gold_to_lord_and_holdings", ":gold_per_lord", ":troop_no"),
			#Relation adjustment
			(store_random_in_range, reg0, 0, 1000),
			(val_add, reg0, ":gold_per_lord"),
			(val_div, reg0, 1000),
			(gt, reg0, 0),
			(val_min, reg0, 3),
			(assign, ":relation_change", reg0),
			#Modify for personality
			(try_begin),
				#Lords who dislike raiding will be displeased by looting a town (but not a castle)
				(party_slot_eq, "$g_encountered_party", slot_party_type, spt_town),
				(call_script, "script_dplmc_get_troop_morality_value", ":troop_no", tmt_humanitarian),
				(try_begin),
					(gt, reg0, 0),#Some lords like raiding settlements less than others
					(val_sub, ":relation_change", reg0),
					(val_min, ":relation_change", -1),
				(else_try),
					(lt, reg0, 0),#Some lords like raiding settlements more than others
					(val_sub, ":relation_change", reg0),
					(val_min, ":relation_change", 4),
				(else_try),
					(this_or_next|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_custodian),
					(this_or_next|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_benefactor),
						(troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_moralist),
					(val_sub, ":relation_change", 1),
			    (try_end),
			(call_script, "script_change_player_relation_with_troop", ":troop_no", ":relation_change"),
 		    (try_end),
		 (try_end),
		 ##nested diplomacy end+
         (val_div, "$diplomacy_var", ":vassal_count"),
         (try_begin),
           (gt, "$g_player_chamberlain", 0),
           (call_script, "script_dplmc_pay_into_treasury", "$diplomacy_var"),
         (else_try),
           (troop_add_gold, "trp_player", "$diplomacy_var"),
         (try_end),
         (call_script, "script_change_center_prosperity", "$g_encountered_party", -8),
         (assign, "$auto_enter_town", "$g_encountered_party"),
         (change_screen_return),
        ]),
##diplomacy end
      ("continue",[],"Continue...",
       [         
         (assign, "$auto_enter_town", "$g_encountered_party"),                  
         (change_screen_return),
        ]),
    ],        
  ),
  (
    "castle_taken_2",mnf_disable_all_keys,
    "{s3} has fallen to your troops, and you now have full control of the castle.\
 It is time to send word to {s9} about your victory. {s5}",
    "none",
    [
        (str_store_party_name, s3, "$g_encountered_party"),
        (str_clear, s5),
        (faction_get_slot, ":faction_leader", "$players_kingdom", slot_faction_leader),
        (str_store_troop_name, s9, ":faction_leader"),
        (try_begin),
          (eq, "$player_has_homage", 0),
          (assign, reg8, 0),
          (try_begin),
		    ##diplomacy start+ FIX: Inserted missing argument
            #(party_slot_eq, "$g_encountered_party", spt_town),
			(party_slot_eq, "$g_encountered_party", slot_party_type, spt_town),
			##diplomacy end+
            (assign, reg8, 1),
          (try_end),
          ##diplomacy start+ fix gender of pronoun
          (call_script, "script_dplmc_store_troop_is_female", ":faction_leader"),
          (str_store_string, s5, "@However, since you are not a sworn {man/follower} of {s9}, there is no chance {reg0?she:he} would recognize you as the {lord/lady} of this {reg8?town:castle}."),
          ##diplomacy end+
        (try_end),
    ],
    [
        ("castle_taken_claim",[(eq, "$player_has_homage", 1)],
		"Request that {s3} be awarded to you.",
        [
        (party_set_slot, "$g_encountered_party", slot_center_last_taken_by_troop, "trp_player"),
        (assign, "$g_castle_requested_by_player", "$current_town"),
		(assign, "$g_castle_requested_for_troop", "trp_player"),
        (assign, "$auto_enter_town", "$g_encountered_party"),
        (change_screen_return),
        ]),

		("castle_taken_claim_2",[
		(troop_get_slot, ":spouse", "trp_player", slot_troop_spouse),
		(is_between, ":spouse", active_npcs_begin, active_npcs_end),
		(troop_slot_eq, ":spouse", slot_troop_occupation, slto_kingdom_hero),
		(store_faction_of_troop, ":spouse_faction", ":spouse"),
		(eq, ":spouse_faction", "$players_kingdom"),
		],
		"Request that {s3} be awarded to your {wife/husband}.",
        [
        (party_set_slot, "$g_encountered_party", slot_center_last_taken_by_troop, "trp_player"),
        (assign, "$g_castle_requested_by_player", "$current_town"),
		(troop_get_slot, ":spouse", "trp_player", slot_troop_spouse),
		(assign, "$g_castle_requested_for_troop", ":spouse"),
        (assign, "$auto_enter_town", "$g_encountered_party"),
        (change_screen_return),
        ]),
		
		
		
      ("castle_taken_no_claim",[],"Ask no rewards.",
       [
        (party_set_slot, "$g_encountered_party", slot_center_last_taken_by_troop, -1),
        (assign, "$auto_enter_town", "$g_encountered_party"),
        (change_screen_return),
#        (jump_to_menu, "mnu_town"),
        ]),
    ],
  ),
(
    "requested_castle_granted_to_player",mnf_scale_picture,
    "You receive a message from your overlord, {s3}.^^\
 {reg4?She:He} has decided to grant {s2}{reg3? and the nearby village of {s4}:} to you, with all due incomes and titles, to hold in {reg4?her:his} name for as long as you maintain your oath of loyalty..",
    "none",
    [
		(set_background_mesh, "mesh_pic_messenger"),
		(faction_get_slot, ":faction_leader", "$players_kingdom", slot_faction_leader),
		(str_store_troop_name, s3, ":faction_leader"),
		(str_store_party_name, s2, "$g_center_to_give_to_player"),
		(try_begin),
			(party_slot_eq, "$g_center_to_give_to_player", slot_party_type, spt_castle),
			(assign, reg3, 1),
			(try_for_range, ":cur_village", villages_begin, villages_end),
				(party_slot_eq, ":cur_village", slot_village_bound_center, "$g_center_to_give_to_player"),
				(str_store_party_name, s4, ":cur_village"),
			(try_end),
		(else_try),
			(assign, reg3, 0),
		(try_end),
		##diplomacy start+ use script for gender
		#(troop_get_type, reg4, ":faction_leader"),#<- OLD
		(call_script, "script_dplmc_store_troop_is_female_reg", ":faction_leader", 4),
		##diplomacy end+
	 
   ],
    [
		("continue",[],"Continue.",
			[
			(call_script, "script_give_center_to_lord", "$g_center_to_give_to_player", "trp_player", 0),
			(jump_to_menu, "mnu_give_center_to_player_2"),
			],
		),
	]
),
  


(
    "requested_castle_granted_to_player_husband", mnf_scale_picture,
    "You receive a message from your overlord, {s3}.^^\
 {reg4?She:He} has decided to grant {s2}{reg3? and the nearby village of {s4}:} to your husband, {s7}.",	 
    "none",
    [
		(set_background_mesh, "mesh_pic_messenger"),
		(faction_get_slot, ":faction_leader", "$players_kingdom", slot_faction_leader),
		(str_store_troop_name, s3, ":faction_leader"),
		(str_store_party_name, s2, "$g_center_to_give_to_player"),
		(try_begin),
			(party_slot_eq, "$g_center_to_give_to_player", slot_party_type, spt_castle),
			(assign, reg3, 1),
			(try_for_range, ":cur_village", villages_begin, villages_end),
				(party_slot_eq, ":cur_village", slot_village_bound_center, "$g_center_to_give_to_player"),
				(str_store_party_name, s4, ":cur_village"),
			(try_end),
		(else_try),
			(assign, reg3, 0),
		(try_end),
		##diplomacy start+ use script for gender
		#(troop_get_type, reg4, ":faction_leader"),#<- OLD
		(call_script, "script_dplmc_store_troop_is_female_reg", ":faction_leader", 4),
		##diplomacy end+
	 
		(troop_get_slot, ":spouse", "trp_player", slot_troop_spouse),
		(str_store_troop_name, s11, ":spouse"), 
		(str_store_string, s7, "str_to_your_husband_s11"),	 
    ],
    [
		("continue",[],"Continue.",
			[
			(troop_get_slot, ":spouse", "trp_player", slot_troop_spouse),
			(call_script, "script_give_center_to_lord", "$g_center_to_give_to_player", ":spouse", 0),
			],
		),
	]
),
  
  
  
  
(
    "requested_castle_granted_to_another",mnf_scale_picture,
    "You receive a message from your lord, {s3}.^^\
 'I was most pleased to hear of your valiant efforts in the capture of {s2}. Your victory has gladdened all our hearts.\
 You also requested me to give you ownership of the castle, but that is a favour which I fear I cannot grant,\
 as you already hold significant estates in my domain.\
 Instead I have sent you {reg6} mon to cover the expenses of your campaign, but {s2} I give to {s5}.'\
 ",
    "none",
    [(set_background_mesh, "mesh_pic_messenger"),
     (faction_get_slot, ":faction_leader", "$players_kingdom", slot_faction_leader),
     (str_store_troop_name, s3, ":faction_leader"),
     (str_store_party_name, s2, "$g_center_to_give_to_player"),
     (party_get_slot, ":new_owner", "$g_center_to_give_to_player", slot_town_lord),
     (str_store_troop_name, s5, ":new_owner"),
     (assign, reg6, 900),
	 
	 (assign, "$g_castle_requested_by_player", -1),
	 (assign, "$g_castle_requested_for_troop", -1),
	 
    ],
    [
      ("accept_decision",[],"Accept the decision.",
       [
       (call_script, "script_troop_add_gold", "trp_player", reg6),
        ##diplomacy start+ Remove gold spent by liege
        (faction_get_slot, ":faction_leader", "$players_kingdom", slot_faction_leader),
        (try_begin),
            (gt, ":faction_leader", 0),
            (neq, ":faction_leader", "trp_kingdom_heroes_including_player_begin"),
            (call_script, "script_dplmc_remove_gold_from_lord_and_holdings", reg6, ":faction_leader"),
        (try_end),
        ##diplomacy end+
       (change_screen_return),
       ]),
	   
       ("leave_faction",[],"You have been wronged! Renounce your oath to your liege! ",
       [
         ##diplomacy start+ Remove gold spent by liege
         (faction_get_slot, ":faction_leader", "$players_kingdom", slot_faction_leader),
         (try_begin),
            (gt, ":faction_leader", 0),
            (neq, ":faction_leader", "trp_kingdom_heroes_including_player_begin"),
            (call_script, "script_dplmc_remove_gold_from_lord_and_holdings", reg6, ":faction_leader"),
         (try_end),
         ##diplomacy end+
         (jump_to_menu, "mnu_leave_faction"),
         (call_script, "script_troop_add_gold", "trp_player", reg6),
        ]),
     ],
  ),
  
(
    "requested_castle_granted_to_another_female",mnf_scale_picture,
##diplomacy start+ make gender correct
    "You receive a message from your lord, {s3}.^^\
 'I was most pleased to hear of your valiant efforts in the capture of {s2}. Your victory has gladdened all our hearts.\
 You also requested me to give ownership of the castle to your {wife/husband}, but that is a favour which I fear I cannot grant,\
 as {she/he} already holds significant estates in my domain.\
 Instead I have sent you {reg6} mon to cover the expenses of your campaign, but {s2} I give to {s5}.'\
 ",
##diplomacy end+
    "none",
    [(set_background_mesh, "mesh_pic_messenger"),
     (faction_get_slot, ":faction_leader", "$players_kingdom", slot_faction_leader),
     (str_store_troop_name, s3, ":faction_leader"),
     (str_store_party_name, s2, "$g_center_to_give_to_player"),
     (party_get_slot, ":new_owner", "$g_center_to_give_to_player", slot_town_lord),
     (str_store_troop_name, s5, ":new_owner"),
     (assign, reg6, 900),

	 (assign, "$g_castle_requested_by_player", -1),
	 (assign, "$g_castle_requested_for_troop", -1),
    ],
	
    [
		("accept_decision",[],"Accept the decision.",
        [
        (call_script, "script_troop_add_gold", "trp_player", reg6),
        (change_screen_return),
        ]),
    ],
),
  

##  (
##    "castle_garrison_stationed",0,
###    "The rest of the castle garrison recognizes that their situation is hopeless and surrenders. {s1} is at your mercy now. What do you want to do with this castle?",
##    "_",
##    "none",
##    [
##        (jump_to_menu, "mnu_town"),
##    ],
##    [],
##  ),

##  (
##    "castle_choose_captain",0,
##    "You will need to assign one of your companions as the castellan. Who will it be?",
##    "none",
##    [
##        (try_for_range, ":slot_no", 0, 20),
##          (troop_set_slot, "trp_temp_troop", ":slot_no", 0),
##        (try_end),
##        (assign, ":num_captains", 0),
##        (party_clear, "p_temp_party"),
##        (party_get_num_companion_stacks, ":num_stacks", "p_main_party"),
##        (try_for_range, ":i_s", 1,":num_stacks"),
##          (party_stack_get_troop_id, ":companion","p_main_party", ":i_s"),
##          (troop_slot_eq, ":companion", slot_troop_occupation, slto_player_companion),
##          (troop_set_slot, "trp_temp_troop", ":num_captains", ":companion"),
##        (try_end),
##    ],
##    [
##      ("castellan_candidate",  [(troop_get_slot, ":captain", "trp_temp_troop", 0),(gt,":captain",0),(str_store_troop_name, s5,":captain")],
##         "{s5}",    [(troop_get_slot, "$selected_castellan", "trp_temp_troop", 0),(jump_to_menu,"mnu_castle_captain_chosen")]),
##      ("castellan_candidate",  [(troop_get_slot, ":captain", "trp_temp_troop", 1),(gt,":captain",0),(str_store_troop_name, s5,":captain")],
##         "{s5}",    [(troop_get_slot, "$selected_castellan", "trp_temp_troop", 1),(jump_to_menu,"mnu_castle_captain_chosen")]),
##      ("castellan_candidate",  [(troop_get_slot, ":captain", "trp_temp_troop", 2),(gt,":captain",0),(str_store_troop_name, s5,":captain")],
##         "{s5}",    [(troop_get_slot, "$selected_castellan", "trp_temp_troop", 2),(jump_to_menu,"mnu_castle_captain_chosen")]),
##      ("castellan_candidate",  [(troop_get_slot, ":captain", "trp_temp_troop", 3),(gt,":captain",0),(str_store_troop_name, s5,":captain")],
##         "{s5}",    [(troop_get_slot, "$selected_castellan", "trp_temp_troop", 3),(jump_to_menu,"mnu_castle_captain_chosen")]),
##      ("castellan_candidate",  [(troop_get_slot, ":captain", "trp_temp_troop", 4),(gt,":captain",0),(str_store_troop_name, s5,":captain")],
##         "{s5}",    [(troop_get_slot, "$selected_castellan", "trp_temp_troop", 4),(jump_to_menu,"mnu_castle_captain_chosen")]),
##      ("castellan_candidate",  [(troop_get_slot, ":captain", "trp_temp_troop", 5),(gt,":captain",0),(str_store_troop_name, s5,":captain")],
##         "{s5}",    [(troop_get_slot, "$selected_castellan", "trp_temp_troop", 5),(jump_to_menu,"mnu_castle_captain_chosen")]),
##      ("castellan_candidate",  [(troop_get_slot, ":captain", "trp_temp_troop", 6),(gt,":captain",0),(str_store_troop_name, s5,":captain")],
##         "{s5}",    [(troop_get_slot, "$selected_castellan", "trp_temp_troop", 6),(jump_to_menu,"mnu_castle_captain_chosen")]),
##      ("castellan_candidate",  [(troop_get_slot, ":captain", "trp_temp_troop", 7),(gt,":captain",0),(str_store_troop_name, s5,":captain")],
##         "{s5}",    [(troop_get_slot, "$selected_castellan", "trp_temp_troop", 7),(jump_to_menu,"mnu_castle_captain_chosen")]),
##      ("castellan_candidate",  [(troop_get_slot, ":captain", "trp_temp_troop", 8),(gt,":captain",0),(str_store_troop_name, s5,":captain")],
##         "{s5}",    [(troop_get_slot, "$selected_castellan", "trp_temp_troop", 8),(jump_to_menu,"mnu_castle_captain_chosen")]),
##      ("castellan_candidate",  [(troop_get_slot, ":captain", "trp_temp_troop", 9),(gt,":captain",0),(str_store_troop_name, s5,":captain")],
##         "{s5}",    [(troop_get_slot, "$selected_castellan", "trp_temp_troop", 9),(jump_to_menu,"mnu_castle_captain_chosen")]),
##      ("castellan_candidate",  [(troop_get_slot, ":captain", "trp_temp_troop", 10),(gt,":captain",0),(str_store_troop_name, s5,":captain")],
##         "{s5}",    [(troop_get_slot, "$selected_castellan", "trp_temp_troop", 10),(jump_to_menu,"mnu_castle_captain_chosen")]),
##      ("castellan_candidate",  [(troop_get_slot, ":captain", "trp_temp_troop", 11),(gt,":captain",0),(str_store_troop_name, s5,":captain")],
##         "{s5}",    [(troop_get_slot, "$selected_castellan", "trp_temp_troop", 11),(jump_to_menu,"mnu_castle_captain_chosen")]),
##      ("castellan_candidate",  [(troop_get_slot, ":captain", "trp_temp_troop", 12),(gt,":captain",0),(str_store_troop_name, s5,":captain")],
##         "{s5}",    [(troop_get_slot, "$selected_castellan", "trp_temp_troop", 12),(jump_to_menu,"mnu_castle_captain_chosen")]),
##      ("castellan_candidate",  [(troop_get_slot, ":captain", "trp_temp_troop", 13),(gt,":captain",0),(str_store_troop_name, s5,":captain")],
##         "{s5}",    [(troop_get_slot, "$selected_castellan", "trp_temp_troop", 13),(jump_to_menu,"mnu_castle_captain_chosen")]),
##      ("castellan_candidate",  [(troop_get_slot, ":captain", "trp_temp_troop", 14),(gt,":captain",0),(str_store_troop_name, s5,":captain")],
##         "{s5}",    [(troop_get_slot, "$selected_castellan", "trp_temp_troop", 14),(jump_to_menu,"mnu_castle_captain_chosen")]),
##      ("castellan_candidate",  [(troop_get_slot, ":captain", "trp_temp_troop", 15),(gt,":captain",0),(str_store_troop_name, s5,":captain")],
##         "{s5}",    [(troop_get_slot, "$selected_castellan", "trp_temp_troop", 15),(jump_to_menu,"mnu_castle_captain_chosen")]),
##      
##      ("cancel",[],
##         "Cancel...",
##         [(jump_to_menu, "mnu_town")]),
##    ],
##  ),
##  (
##    "castle_captain_chosen",0,
##    "h this castle?",
##    "none",
##    [
##        (party_add_leader, "$g_encountered_party",  "$selected_castellan"),
##        (party_remove_members, "p_main_party", "$selected_castellan",1),
##        (party_set_slot, "$g_encountered_party", slot_town_lord, "trp_player"),
##        (party_set_faction, "$g_encountered_party", "fac_player_supporters_faction"),
##        (try_for_range, ":slot_no", 0, 20), #clear temp troop slots just in case
##          (troop_set_slot, "trp_temp_troop", ":slot_no", 0),
##        (try_end),
##        (jump_to_menu, "mnu_town"),
##        (change_screen_exchange_members,0),
##    ],
##    [],
##  ),

##  (
##    "under_siege_attacked_continue",0,
##    "Nothing to see here.",
##    "none",
##    [
##        (assign, "$g_enemy_party", "$g_encountered_party_2"),
##        (assign, "$g_ally_party", "$g_encountered_party"),
##        (party_set_next_battle_simulation_time, "$g_encountered_party", 0),
##        (call_script, "script_encounter_calculate_fit"),
##        (try_begin),
##          (call_script, "script_party_count_fit_regulars", "p_collective_enemy"),
##          (assign, ":num_enemy_regulars_remaining", reg(0)),
##          (assign, ":enemy_finished",0),
##          (try_begin),
##            (eq, "$g_battle_result", 1),
##            (eq, ":num_enemy_regulars_remaining", 0), #battle won
##            (assign, ":enemy_finished",1),
##          (else_try),
##            (eq, "$g_engaged_enemy", 1),
##            (le, "$g_enemy_fit_for_battle",0),
##            (ge, "$g_friend_fit_for_battle",1),
##            (assign, ":enemy_finished",1),
##          (try_end),
##          (this_or_next|eq, ":enemy_finished",1),
##          (eq,"$g_enemy_surrenders",1),
####          (assign, "$g_center_under_siege_battle", 0),
##          (assign, "$g_next_menu", -1),
##          (jump_to_menu, "mnu_total_victory"),
##        (else_try),
##          (assign, ":battle_lost", 0),
##          (try_begin),
##            (eq, "$g_battle_result", -1),
##            (assign, ":battle_lost",1),
##          (try_end),
##          (this_or_next|eq, ":battle_lost",1),
##          (eq,"$g_player_surrenders",1),
####          (assign, "$g_center_under_siege_battle", 0),
##          (assign, "$g_next_menu", "mnu_captivity_start_under_siege_defeat"),
##          (jump_to_menu, "mnu_total_defeat"),
##        (else_try),
##    # Ordinary victory.
##          (try_begin),
##          #check whether enemy retreats
##            (eq, "$g_battle_result", 1),
##            (store_mul, ":min_enemy_str", "$g_enemy_fit_for_battle", 2),
##            (lt, ":min_enemy_str", "$g_friend_fit_for_battle"),
##            (party_set_slot, "$g_enemy_party", slot_party_retreat_flag, 1),
##
##            (try_for_range, ":troop_no", kingdom_heroes_begin, kingdom_heroes_end),
##              (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
##              (troop_slot_eq, ":troop_no", slot_troop_is_prisoner, 0),
##              (troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
##              (gt, ":party_no", 0),
##              (party_slot_eq, ":party_no", slot_party_ai_state, spai_besieging_center),
##              (party_slot_eq, ":party_no", slot_party_ai_object, "$g_encountered_party"),
##              (party_slot_eq, ":party_no", slot_party_ai_substate, 1),
##              (call_script, "script_party_set_ai_state", ":party_no", spai_undefined, -1),
##              (call_script, "script_party_set_ai_state", ":party_no", spai_besieging_center, ":center_no"),
##            (try_end),
##            (display_message, "@{!}TODO: Enemy retreated. The assault has ended, siege continues."),
##            (change_screen_return),
##          (try_end),
####          (assign, "$g_center_under_siege_battle", 0),
##        (try_end),
##        ],
##    [
##    ]
##  ),


  (
    "siege_started_defender",0,
    "{s1} is launching an assault against the walls of {s2}. You have {reg10} troops fit for battle against the enemy's {reg11}. You decide to...",
    "none",
    [
        (select_enemy,1),
        (assign, "$g_enemy_party", "$g_encountered_party_2"),
        (assign, "$g_ally_party", "$g_encountered_party"),
        (str_store_party_name, 1,"$g_enemy_party"),
        (str_store_party_name, 2,"$g_ally_party"),
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
          (eq, "$g_siege_first_encounter", 1),
          (call_script, "script_let_nearby_parties_join_current_battle", 0, 1),
		  ###diplomacy start+
		  ##If terrain advantage is on, use siege settings
          #(assign, ":save_dplmc_terrain_advantage", "$g_dplmc_terrain_advantage"),
		  #(try_begin),
		  #   (eq, "$g_dplmc_terrain_advantage", TERRAIN_ADVANTAGE_ENABLE),
		  #   (assign, "$g_dplmc_terrain_advantage", TERRAIN_ADVANTAGE_FORCE_SIEGE),
		  #(try_end),
		  ###diplomacy end+
          (call_script, "script_encounter_init_variables"),
		  ###diplomacy start+
		  ##Revert terrain advantage settings
		  #(assign, "$g_dplmc_terrain_advantage", ":save_dplmc_terrain_advantage"),
		  ###diplmacy end+
        (try_end),

        (try_begin),
          (eq, "$g_siege_first_encounter", 0),
          (try_begin),
            (call_script, "script_party_count_members_with_full_health", "p_collective_enemy"),
            (assign, ":num_enemy_regulars_remaining", reg0),
            (call_script, "script_party_count_members_with_full_health", "p_collective_friends"),
            (assign, ":num_ally_regulars_remaining", reg0),
            (assign, ":enemy_finished", 0),
            (try_begin),
              (eq, "$g_battle_result", 1),
              (eq, ":num_enemy_regulars_remaining", 0), #battle won (TODO : compare with num_routed_us)
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
            (assign, ":battle_lost", 0),
            (try_begin),
              (this_or_next|eq, "$g_battle_result", -1),
              (troop_is_wounded,  "trp_player"),
              (eq, ":num_ally_regulars_remaining", 0), #(TODO : compare with num_routed_allies)
              (assign, ":battle_lost",1),
            (try_end),
            (this_or_next|eq, ":battle_lost",1),
            (eq,"$g_player_surrenders",1),
            (assign, "$g_next_menu", "mnu_captivity_start_under_siege_defeat"),
            (jump_to_menu, "mnu_total_defeat"),
          (else_try),
            # Ordinary victory/defeat.
            (assign, ":attackers_retreat", 0),
            (try_begin),
            #check whether enemy retreats
              (eq, "$g_battle_result", 1),
  ##            (store_mul, ":min_enemy_str", "$g_enemy_fit_for_battle", 2),
  ##            (lt, ":min_enemy_str", "$g_friend_fit_for_battle"),
              (assign, ":attackers_retreat", 1),
            (else_try),
              (eq, "$g_battle_result", 0),
              (store_div, ":min_enemy_str", "$g_enemy_fit_for_battle", 3),
              (lt, ":min_enemy_str", "$g_friend_fit_for_battle"),
              (assign, ":attackers_retreat", 1),
            (else_try),
              (store_random_in_range, ":random_no", 0, 100),
              (store_mul, ":num_ally_regulars_remaining_multiplied", ":num_ally_regulars_remaining", 13),
              (val_div, ":num_ally_regulars_remaining_multiplied", 10),
              (ge, ":num_ally_regulars_remaining_multiplied", ":num_enemy_regulars_remaining"),
              (lt, ":random_no", 10),
              (neq, "$new_encounter", 1),
              (assign, ":attackers_retreat", 1),
            (try_end),
            (try_begin),
              (eq, ":attackers_retreat", 1),
              (party_get_slot, ":siege_hardness", "$g_encountered_party", slot_center_siege_hardness),
              (val_add, ":siege_hardness", 100),
              (party_set_slot, "$g_encountered_party", slot_center_siege_hardness, ":siege_hardness"),
              (party_set_slot, "$g_enemy_party", slot_party_retreat_flag, 1),

              (try_for_range, ":troop_no", active_npcs_begin, active_npcs_end),
                (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
                #(troop_slot_eq, ":troop_no", slot_troop_is_prisoner, 0),
                (neg|troop_slot_ge, ":troop_no", slot_troop_prisoner_of_party, 0),
                (troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
                (gt, ":party_no", 0),
                (party_slot_eq, ":party_no", slot_party_ai_state, spai_besieging_center),
                (party_slot_eq, ":party_no", slot_party_ai_object, "$g_encountered_party"),
                (party_slot_eq, ":party_no", slot_party_ai_substate, 1),
                (call_script, "script_party_set_ai_state", ":party_no", spai_undefined, -1),
                (call_script, "script_party_set_ai_state", ":party_no", spai_besieging_center, "$g_encountered_party"),
              (try_end),
              (display_message, "@The enemy has been forced to retreat. The assault is over, but the siege continues."),
              (assign, "$g_battle_simulation_cancel_for_party", "$g_encountered_party"),
              (leave_encounter),
              (change_screen_return),
              (assign, "$g_battle_simulation_auto_enter_town_after_battle", "$g_encountered_party"),
            (try_end),
          (try_end),
        (try_end),
        (assign, "$g_siege_first_encounter", 0),
        (assign, "$new_encounter", 0),
        ],
    [
     ##diplomacy begin
      ("dplmc_negotiate_with_besieger",
      [
        (party_slot_eq, "$current_town", slot_town_lord, "trp_player"),
        (party_slot_ge, "$current_town", slot_center_is_besieged_by, 1),
      ]
       ,"Negotiate with the besieger.",
       [
        (jump_to_menu, "mnu_dplmc_negotiate_besieger"),
        ]),
     ##diplomacy end
      ("siege_defender_join_battle",
       [
         (neg|troop_is_wounded, "trp_player"),
         ],
          "Join the battle.",[              
              (party_set_next_battle_simulation_time, "$g_encountered_party", -1),
              (assign, "$g_battle_result", 0),
              (try_begin),
                (party_slot_eq, "$g_encountered_party", slot_party_type, spt_town),
                (party_get_slot, ":battle_scene", "$g_encountered_party", slot_town_walls),
              (else_try),
                (party_get_slot, ":battle_scene", "$g_encountered_party", slot_castle_exterior),
              (try_end),
              (call_script, "script_calculate_battle_advantage"),
              (val_mul, reg0, 2),
              (val_div, reg0, 3), #scale down the advantage a bit.
              (set_battle_advantage, reg0),
              (set_party_battle_mode),
              (try_begin),
                (party_slot_eq, "$current_town", slot_center_siege_with_belfry, 1),
			    #gekokujo revise belfry attack mission sometime
                #(set_jump_mission,"mt_castle_attack_walls_belfry"),
                (set_jump_mission,"mt_castle_attack_walls_ladder"),
              (else_try),
                (set_jump_mission,"mt_castle_attack_walls_ladder"),
              (try_end),
              (jump_to_scene,":battle_scene"),
              (assign, "$g_next_menu", "mnu_siege_started_defender"),
              (jump_to_menu, "mnu_battle_debrief"),
              (change_screen_mission)]),
      ("siege_defender_troops_join_battle",[(call_script, "script_party_count_members_with_full_health", "p_main_party"),
                                            (this_or_next|troop_is_wounded,  "trp_player"),
                                            (ge, reg0, 3)],
          "Order your men to join the battle without you.",[
              (party_set_next_battle_simulation_time, "$g_encountered_party", -1),
              (select_enemy,1),
              (assign,"$g_enemy_party","$g_encountered_party_2"),
              (assign,"$g_ally_party","$g_encountered_party"),
              (assign,"$g_siege_join", 1),
              (jump_to_menu,"mnu_siege_join_defense")]),
    ]
  ),
  (
    "siege_join_defense",mnf_disable_all_keys,
    "{s4}^^Your casualties: {s8}^^Allies' casualties: {s9}^^Enemy casualties: {s10}",
    "none",
    [
	    ###diplomacy start+
		##If terrain advantage is on, use siege settings
        #(assign, ":save_dplmc_terrain_advantage", "$g_dplmc_terrain_advantage"),
		##(assign, "$g_dplmc_terrain_advantage", ":save_dplmc_terrain_advantage"),
		#(try_begin),
		#   (eq, "$g_dplmc_terrain_advantage", TERRAIN_ADVANTAGE_ENABLE),
		#   (assign, "$g_dplmc_terrain_advantage", TERRAIN_ADVANTAGE_FORCE_SIEGE),
		#(try_end),
		###diplomacy end+
        (try_begin),
          (eq, "$g_siege_join", 1),
          (call_script, "script_party_calculate_strength", "p_main_party", 1), #skip player
          (assign, ":player_party_strength", reg0),
          (val_div, ":player_party_strength", 5),
        (else_try),
          (assign, ":player_party_strength", 0),
        (try_end),
        
        (call_script, "script_party_calculate_strength", "p_collective_ally", 0),
        (assign, ":ally_party_strength", reg0),
        (val_div, ":ally_party_strength", 5),
        (call_script, "script_party_calculate_strength", "p_collective_enemy", 0),
        (assign, ":enemy_party_strength", reg0),
        (val_div, ":enemy_party_strength", 10),

        (store_add, ":friend_party_strength", ":player_party_strength", ":ally_party_strength"),
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

        (inflict_casualties_to_party_group, "$g_ally_party", ":enemy_party_strength", "p_temp_casualties"),
        (call_script, "script_print_casualties_to_s0", "p_temp_casualties", 0),
        (str_store_string_reg, s9, s0),
        (party_collect_attachments_to_party, "$g_ally_party", "p_collective_ally"),

        (inflict_casualties_to_party_group, "$g_enemy_party", ":friend_party_strength", "p_temp_casualties"),
        (call_script, "script_print_casualties_to_s0", "p_temp_casualties", 0),
        (str_store_string_reg, s10, s0),
        (party_collect_attachments_to_party, "$g_enemy_party", "p_collective_enemy"),

        (try_begin),
          (call_script, "script_party_count_members_with_full_health","p_main_party"),
          (le, reg0, 0),
          (str_store_string, s4, "str_siege_defender_order_attack_failure"),
        (else_try),
          (call_script, "script_party_count_members_with_full_health","p_collective_enemy"),
          (le, reg0, 0),
          (assign, "$g_battle_result", 1),
          (str_store_string, s4, "str_siege_defender_order_attack_success"),
        (else_try),
          (str_store_string, s4, "str_siege_defender_order_attack_continue"),
        (try_end),
		###diplomacy start+
		##Revert terrain advantage settings
		#(assign, "$g_dplmc_terrain_advantage", ":save_dplmc_terrain_advantage"),
		###diplomacy end+
    ],
    [
      ("continue",[],"Continue...",[
          (jump_to_menu,"mnu_siege_started_defender"),
          ]),
    ]
  ),
  (
    "enter_your_own_castle",0,
    "{s10}",
    "none",
    [
      (try_begin),
	  ##diplomacy start+ Add support for the player as co-ruler of an NPC faction
	    (is_between, "$players_kingdom", kingdoms_begin, kingdoms_end),
		(call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", "$players_kingdom"),
		(ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
		(try_begin),
			(eq, 1, "$character_gender"),
			(call_script, "script_dplmc_print_cultural_word_to_sreg", "trp_player", DPLMC_CULTURAL_TERM_KING_FEMALE, s10),
		(else_try),
			(call_script, "script_dplmc_print_cultural_word_to_sreg", "trp_player", DPLMC_CULTURAL_TERM_KING, s10),
		(try_end),
		(str_store_string, s10, "@As you approach, you are spotted by the castle guards, who welcome you and open the gates for their {s10}."),
	  (else_try),
	  ##diplomacy end+
        (neg|is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
        (faction_get_slot, ":faction_leader", "fac_player_supporters_faction", slot_faction_leader),
        (eq, ":faction_leader", "trp_player"),
        (str_store_string, s10, "@As you approach, you are spotted by the castle guards, who welcome you and open the gates for their {lord/lady}."),
      (else_try),  
        (str_store_string, s10, "@As you approach, you are spotted by the castle guards, who welcome you and open the gates for their {lord/lady}."),
      (try_end),  
      
      (str_store_party_name, s2, "$current_town"),
    ],
    [
      ("continue",[],"Continue...",
       [ (jump_to_menu,"mnu_town"),
        ]),
    ],
  ),
  
  #gekokujo 3.0 microfactions! start
  (
    "fort",mnf_enable_hot_keys,
    "Welcome to {s2}.",
    "none",
    [
      (assign, "$current_town", "$g_encountered_party"),
      (str_store_party_name, s2, "$current_town"),
	  
      (try_begin),
        (party_slot_eq, "$current_town", slot_fort_type, sft_mansion),
		(str_store_string, s2, "@{s2} Mansion"),
		(set_background_mesh, "mesh_gekokujo_pic_town"),
      (else_try),
        (party_slot_eq, "$current_town", slot_fort_type, sft_castle),
		(str_store_string, s2, "@{s2} Castle"),
		(set_background_mesh, "mesh_gekokujo_pic_castle"),
      (else_try),
        (party_slot_eq, "$current_town", slot_fort_type, sft_temple),
		(str_store_string, s2, "@{s2} Temple"),
		(set_background_mesh, "mesh_gekokujo_pic_village"),
      (else_try),
        (party_slot_eq, "$current_town", slot_fort_type, sft_village),
		(str_store_string, s2, "@the village of {s2}"),
		(set_background_mesh, "mesh_gekokujo_pic_village"),
      (try_end),
	  
      (try_begin),
	    (party_slot_ge, "$current_town", slot_fort_timer, 1),
	    (party_slot_eq, "$current_town", slot_fort_captured, 0),
		(str_store_string, s2, "@the burnt-out ruins of {s2}. You spot some people among the wreckage, but they flee at the sight of you"),
		(set_background_mesh, "mesh_pic_looted_village"),
      (else_try),
	    (party_slot_eq, "$current_town", slot_fort_captured, 0),
	    (eq, "$g_battle_result", -1),
		(str_store_string, s2, "@{s2}. Its defenders look triumphant after having defeated you, but you are able to escape."),
	    (set_background_mesh, "mesh_gekokujo_pic_bandits_2"),
      (else_try),
	    (party_slot_eq, "$current_town", slot_fort_captured, 0),
		(str_store_string, s2, "@{s2}. Its defenses are bristling and its defenders look ready to meet any threat"),
	    (set_background_mesh, "mesh_gekokujo_pic_bandits_1"),
      (else_try),
		(str_store_string, s2, "@{s2}. Your banners fly high and the sentries greet you, their {lord/lady}"),
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
      ("fort_attack",
        [
          (neg|troop_is_wounded, "trp_player"),
          #(gt, "$g_friend_fit_for_battle", 3),
		  (party_slot_eq, "$current_town", slot_fort_captured, 0),
		  (party_slot_eq, "$current_town", slot_fort_timer, 0),
		  
          (try_begin),
            (party_slot_eq, "$current_town", slot_fort_type, sft_mansion),
	    	(str_store_string, s41, "@mansion"),
          (else_try),
            (party_slot_eq, "$current_town", slot_fort_type, sft_castle),
		    (str_store_string, s41, "@castle"),
          (else_try),
            (party_slot_eq, "$current_town", slot_fort_type, sft_temple),
		    (str_store_string, s41, "@temple"),
          (else_try),
            (party_slot_eq, "$current_town", slot_fort_type, sft_village),
		    (str_store_string, s41, "@village"),
          (try_end),
        ],
        "Attack the {s41}", 
        [
          (party_get_slot, ":scene", "$g_encountered_party", slot_fort_exterior),
          
          (call_script, "script_calculate_renown_value"),            
          (call_script, "script_calculate_battle_advantage"),
          (assign, ":battle_advantage", reg0),
          (val_mul, ":battle_advantage", 2),
          (val_div, ":battle_advantage", 3), #scale down the advantage a bit in sieges.
          (set_battle_advantage, ":battle_advantage"),
          (set_party_battle_mode),
          (assign, ":siege_sally", 0),
          (try_begin),
            (le, ":battle_advantage", -4), #we are outnumbered, defenders sally out
            (eq, "$g_siege_sallied_out_once", 0),
            (set_jump_mission, "mt_castle_attack_walls_defenders_sally"),
            (assign, ":siege_sally", 1),
          (else_try),
            (set_jump_mission, "mt_castle_attack_walls_ladder"),
          (try_end),
		  
          (assign, "$cant_talk_to_enemy", 0),           
          (assign, "$g_next_menu", "mnu_fort_after_battle"),
          (jump_to_scene, ":scene"),
		  
          (try_begin),
            (eq, ":siege_sally", 1),
            (jump_to_menu, "mnu_siege_attack_meets_sally"),
          (else_try),
            (jump_to_menu, "mnu_battle_debrief"),
            (change_screen_mission),
          (try_end),
        ]),
      ("fort_center", [
	      (party_slot_eq, "$current_town", slot_fort_captured, 1),
		  
          (try_begin),
            (party_slot_eq, "$current_town", slot_fort_type, sft_mansion),
	    	(str_store_string, s42, "@mansion"),
          (else_try),
            (party_slot_eq, "$current_town", slot_fort_type, sft_castle),
		    (str_store_string, s42, "@castle"),
          (else_try),
            (party_slot_eq, "$current_town", slot_fort_type, sft_temple),
		    (str_store_string, s42, "@temple"),
          (else_try),
            (party_slot_eq, "$current_town", slot_fort_type, sft_village),
		    (str_store_string, s42, "@village"),
          (try_end),
	    ],
        "Take a walk around the {s42}",
        [
          (party_get_slot, ":scene", "$current_town", slot_fort_exterior),
          (modify_visitors_at_site,":scene"),
          (reset_visitors),
		  
          (party_get_slot, ":visitor", "$current_town", slot_fort_npc_1),
          (set_visitor, 12, ":visitor"), #deputy
		  
		  (try_begin),
		    (neg|party_slot_eq, "$current_town", slot_fort_npc_2_state, 3), #don't spawn recruited troop
		    (neg|party_slot_eq, "$current_town", slot_fort_npc_2_state, 4), #don't spawn promoted troop
            (party_get_slot, ":visitor", "$current_town", slot_fort_npc_2),
            (set_visitor, 13, ":visitor"), #potential companion
		  (try_end),

          (party_get_slot, ":visitor", "$current_town", slot_fort_recruit_type),
          (set_visitor, 40, ":visitor"),
          (set_visitor, 41, ":visitor"),
          (set_visitor, 42, ":visitor"),
          (set_visitor, 43, ":visitor"),
          (set_visitor, 44, ":visitor"),
          (set_visitor, 45, ":visitor"),
          (set_visitor, 46, ":visitor"),
		  
          (call_script, "script_init_town_walkers"),

          (set_jump_mission,"mt_village_center"),
          (jump_to_scene,":scene"),
          (change_screen_mission),
        ],"Door to the {s42} center."),
      ("fort_deputy_meeting", [
	      (party_slot_eq, "$current_town", slot_fort_captured, 1),
        ], 
        "Meet the deputy you left in charge", 
        [
          (party_get_slot, ":scene", "$current_town", slot_fort_exterior),
          (modify_visitors_at_site,":scene"),
          (reset_visitors),
		  
          (party_get_slot, ":visitor", "$current_town", slot_fort_npc_1),
          (set_visitor, 12, ":visitor"),

          (set_jump_mission,"mt_village_center"),
          (jump_to_scene,":scene"),
          (change_screen_map_conversation, ":visitor"),
        ]),
	  ("fort_station_troops", [
		  (party_slot_eq, "$current_town", slot_fort_captured, 1),
        ], 
		#gekokujo 3.1 fort prisoner bug
		"Manage the garrison", [
          (change_screen_exchange_members, 1),
        ]),
      ("fort_wait", [
		  (party_slot_eq, "$current_town", slot_fort_captured, 1),
        ],
        "Wait here for some time", [
          (assign, "$auto_enter_town", "$current_town"),
          (assign, "$g_town_visit_after_rest", 1),
          (assign, "$g_last_rest_center", "$current_town"),

          (try_begin),
            (party_is_active, "p_main_party"),
            (party_get_current_terrain, ":cur_terrain", "p_main_party"),
            (try_begin),
              (eq, ":cur_terrain", rt_desert),
              (unlock_achievement, ACHIEVEMENT_SARRANIDIAN_NIGHTS), #gekokujo 3.0 yes, we're keeping it in here, just in case
            (try_end),  
          (try_end),  

          (rest_for_hours_interactive, 24 * 7, 5, 0), #rest while not attackable
          (change_screen_return),
        ]),
      ("fort_cheat_capture", [
	      (eq, "$cheat_mode", 1),
		  (party_slot_eq, "$current_town", slot_fort_captured, 0),
		  (party_slot_eq, "$current_town", slot_fort_timer, 0),
		  
          (try_begin),
            (party_slot_eq, "$current_town", slot_fort_type, sft_mansion),
	    	(str_store_string, s43, "@mansion"),
          (else_try),
            (party_slot_eq, "$current_town", slot_fort_type, sft_castle),
		    (str_store_string, s43, "@castle"),
          (else_try),
            (party_slot_eq, "$current_town", slot_fort_type, sft_temple),
		    (str_store_string, s43, "@temple"),
          (else_try),
            (party_slot_eq, "$current_town", slot_fort_type, sft_village),
		    (str_store_string, s43, "@village"),
          (try_end),
		], 
		"{!}CHEAT! Capture this {s43}", [(jump_to_menu, "mnu_fort_taken")]),
      ("fort_cheat_exterior", [(eq, "$cheat_mode", 1)], 
		"{!}CHEAT! Exterior", [
	      (set_jump_mission,"mt_ai_training"),
	      (party_get_slot, ":fort_scene", "$current_town", slot_fort_exterior),
	      (jump_to_scene, ":fort_scene"),
	      (change_screen_mission)
        ]),
      ("fort_leave", [], "Leave...", [(change_screen_return, 0)]),
	],
  ),
  
  (
    "fort_after_battle",mnf_disable_all_keys,
    "Your men drag you away from the battle and you are able to retreat a little worse for wear.",
    "none",
    [
	    #Check for victory or defeat....
        (assign, "$g_enemy_party", "$g_encountered_party"),
        (assign, "$g_ally_party", -1),
        (str_store_party_name, s1,"$g_encountered_party"),
        (call_script, "script_encounter_calculate_fit"),
        
        (assign, reg11, "$g_enemy_fit_for_battle"),
        (assign, reg10, "$g_friend_fit_for_battle"),

        (try_begin),
          (eq, "$g_leave_encounter",1),
          (change_screen_return),
        (else_try),
          (call_script, "script_party_count_fit_regulars","p_collective_enemy"),
          (assign, ":enemy_finished", 0),
          (try_begin),
            (eq, "$g_battle_result", 1),
            (assign, ":enemy_finished", 1),
          (else_try),
            (le, "$g_enemy_fit_for_battle", 0),
            (ge, "$g_friend_fit_for_battle", 1),
            (assign, ":enemy_finished", 1),
          (try_end),
          (eq, ":enemy_finished", 1),
          (assign, "$g_next_menu", "mnu_fort_taken"), 
          (jump_to_menu, "mnu_total_victory"),
        (else_try),
          (call_script, "script_party_count_members_with_full_health", "p_main_party"),
          (assign, ":main_party_fit_regulars", reg0),
          (eq, "$g_battle_result", -1),
          (eq, ":main_party_fit_regulars", 0),
          (assign, "$g_next_menu", "mnu_fort"),
          (jump_to_menu, "mnu_total_defeat"),
        (try_end),
	],
    [
      ("fort_battle_leave", [], "Continue...", [(jump_to_menu, "mnu_fort")]),
	],
  ),
  
  (
    "fort_taken",mnf_disable_all_keys,
    "You have taken {s2}! What will you do from here? You have enough leadership to control {reg1} forts and currently have {reg2} under your control.",
    "none",
    [
      (str_store_party_name, s2, "$current_town"),
	  (party_clear, "$g_encountered_party"),
	  (call_script, "script_change_troop_renown", "trp_player", 5),
	  
	  (store_skill_level, reg1, "skl_leadership", "trp_player"),
	  (val_div, reg1, 2), #2 skill levels per fort
	  (val_add, reg1, 1), #0 skill should still allow 1 fort for 6 forts total at 10 leadership
	  (assign, reg2, "$num_forts_captured"),
	],
    [
	  ("fort_capture", [
	      (store_skill_level, ":cur_leadership", "skl_leadership", "trp_player"),
		  (val_div, ":cur_leadership", 2),
		  (val_add, ":cur_leadership", 1),
		  (gt, ":cur_leadership", "$num_forts_captured"),
	    ], "This is mine now!", [
	      (party_set_slot, "$current_town", slot_fort_captured, 1),
		  (val_add, "$num_forts_captured", 1),
		  (str_store_party_name, s44, "$current_town"),
		  (display_log_message, "@{playername} has taken {s44}"),
		  (jump_to_menu, "mnu_fort"),

          (party_get_slot, ":scene", "$current_town", slot_fort_exterior),
          (modify_visitors_at_site, ":scene"),
          (reset_visitors),

          (party_get_slot, ":visitor", "$current_town", slot_fort_npc_1),
          (set_visitor, 12, ":visitor"),

          (set_jump_mission,"mt_village_center"),
          (jump_to_scene,":scene"),
          (change_screen_map_conversation, ":visitor"),
		]),
	  ("fort_suppress", [], "Burn it all down!", [
	      (store_random_in_range, ":rand", 7, 15),
	      (party_set_slot, "$current_town", slot_fort_timer, ":rand"), #fort will stay suppressed for 1 to 2 weeks
	      #(party_set_slot, "$current_town", slot_fort_timer, 2), #debug version stays suppressed for 2 days
		
	      (party_set_slot, "$current_town", slot_fort_fire, 1),
		  (party_add_particle_system, "$current_town", "psys_map_village_fire"),
		  (party_add_particle_system, "$current_town", "psys_map_village_fire_smoke"),
		  (try_begin),
		    (party_slot_eq, "$current_town", slot_fort_type, sft_village), #ainu village
		    (party_set_icon, "$current_town", "icon_village_snow_burnt_a"),
		  (else_try),
  		    (party_set_icon, "$current_town", "icon_village_burnt_a"),
		  (try_end),
		
		  (change_screen_return, 0)
		]),
	],
  ),
  (
    "center_manage",0,
    "{s19}^{reg6?^^You are\
 currently building {s7}. The building will be completed after {reg8} day{reg9?s:}.:}",
    "none",
    [(assign, ":num_improvements", 0),
     (str_clear, s18),
     (try_begin),
       (party_slot_eq, "$g_encountered_party", slot_party_type, spt_village),
       (assign, ":begin", village_improvements_begin),
       (assign, ":end", village_improvements_end),
       (str_store_string, s17, "@village"),
     (else_try),
       (assign, ":begin", walled_center_improvements_begin),
       (assign, ":end", walled_center_improvements_end),
       (party_slot_eq, "$g_encountered_party", slot_party_type, spt_town),
       (str_store_string, s17, "@town"),
     (else_try),
       (str_store_string, s17, "@castle"),
     (try_end),
     
     (try_for_range, ":improvement_no", ":begin", ":end"),
       (party_slot_ge, "$g_encountered_party", ":improvement_no", 1),
       (val_add,  ":num_improvements", 1),
       (call_script, "script_get_improvement_details", ":improvement_no"),
       (try_begin),
         (eq,  ":num_improvements", 1),
         (str_store_string, s18, "@{!}{s0}"),
       (else_try),
         (str_store_string, s18, "@{!}{s18}, {s0}"),
       (try_end),
     (try_end),
     
     (try_begin),
       (eq,  ":num_improvements", 0),
       (str_store_string, s19, "@The {s17} has no improvements."),
     (else_try),
       (str_store_string, s19, "@The {s17} has the following improvements:{s18}."),
     (try_end),
     
     (assign, reg6, 0),
     (try_begin),
       (party_get_slot, ":cur_improvement", "$g_encountered_party", slot_center_current_improvement),
       (gt, ":cur_improvement", 0),
       (call_script, "script_get_improvement_details", ":cur_improvement"),
       (str_store_string, s7, s0),
       (assign, reg6, 1),
       (store_current_hours, ":cur_hours"),
       (party_get_slot, ":finish_time", "$g_encountered_party", slot_center_improvement_end_hour),
       (val_sub, ":finish_time", ":cur_hours"),
       (store_div, reg8, ":finish_time", 24),
       (val_max, reg8, 1),
       (store_sub, reg9, reg8, 1),
     (try_end),
    ],
    [
      ("center_build_manor",[(eq, reg6, 0),
                             (party_slot_eq, "$g_encountered_party", slot_party_type, spt_village),
                             (party_slot_eq, "$g_encountered_party", slot_center_has_manor, 0),
                                  ],
       "Build a manor.",[(assign, "$g_improvement_type", slot_center_has_manor),
                         (jump_to_menu, "mnu_center_improve"),]),
      ("center_build_fish_pond",[(eq, reg6, 0),
                                 (party_slot_eq, "$g_encountered_party", slot_party_type, spt_village),
                                 (party_slot_eq, "$g_encountered_party", slot_center_has_fish_pond, 0),
                                  ],
       "Build a mill.",[(assign, "$g_improvement_type", slot_center_has_fish_pond),
                             (jump_to_menu, "mnu_center_improve"),]),
      ("center_build_watch_tower",[(eq, reg6, 0),
                                   (party_slot_eq, "$g_encountered_party", slot_party_type, spt_village),
                                   (party_slot_eq, "$g_encountered_party", slot_center_has_watch_tower, 0),
                                  ],
       "Build a watch tower.",[(assign, "$g_improvement_type", slot_center_has_watch_tower),
                               (jump_to_menu, "mnu_center_improve"),]),
      ("center_build_school",[(eq, reg6, 0),
                              (party_slot_eq, "$g_encountered_party", slot_party_type, spt_village),
                              (party_slot_eq, "$g_encountered_party", slot_center_has_school, 0),
                                  ],
       "Build a shrine.",[(assign, "$g_improvement_type", slot_center_has_school),
                          (jump_to_menu, "mnu_center_improve"),]),
      ("center_build_messenger_post",[(eq, reg6, 0),
                                      (party_slot_eq, "$g_encountered_party", slot_center_has_messenger_post, 0),
                                       ],
       "Build a messenger post.",[(assign, "$g_improvement_type", slot_center_has_messenger_post),
                                  (jump_to_menu, "mnu_center_improve"),]),
      ("center_build_prisoner_tower",[(eq, reg6, 0),
                                      (this_or_next|party_slot_eq, "$g_encountered_party", slot_party_type, spt_town),
                                      (party_slot_eq, "$g_encountered_party", slot_party_type, spt_castle),
                                      (party_slot_eq, "$g_encountered_party", slot_center_has_prisoner_tower, 0),
                                       ],
       "Build a prisoner tower.",[(assign, "$g_improvement_type", slot_center_has_prisoner_tower),
                                  (jump_to_menu, "mnu_center_improve"),]),
                           
      ("go_back_dot",[],"Go back.",[(jump_to_menu, "$g_next_menu")]),
    ],
  ),
  (
    "center_improve",0,
    "{s19} As the party member with the highest engineer skill ({reg2}), {reg3?you reckon:{s3} reckons} that building the {s4} will cost you\
 {reg5} mon and will take {reg6} days.",
    "none",
    [(call_script, "script_get_improvement_details", "$g_improvement_type"),
     (assign, ":improvement_cost", reg0),
     (str_store_string, s4, s0),
     (str_store_string, s19, s1),
     (call_script, "script_get_max_skill_of_player_party", "skl_engineer"),
     (assign, ":max_skill", reg0),
     (assign, ":max_skill_owner", reg1),
     (assign, reg2, ":max_skill"),

     (store_sub, ":multiplier", 20, ":max_skill"),
     (val_mul, ":improvement_cost", ":multiplier"),
     (val_div, ":improvement_cost", 20),
     
     (store_div, ":improvement_time", ":improvement_cost", 100),
     (val_add, ":improvement_time", 3),

     (assign, reg5, ":improvement_cost"),
     (assign, reg6, ":improvement_time"),

     (try_begin),
       (eq, ":max_skill_owner", "trp_player"),
       (assign, reg3, 1),
     (else_try),
       (assign, reg3, 0),
       (str_store_troop_name, s3, ":max_skill_owner"),
     (try_end),
    ],
    [
      ##diplomacy begin
      ("dplmc_improve_cont",
      [
        (gt, "$g_player_chamberlain", 0),
        (store_troop_gold, ":cur_gold", "trp_household_possessions"),
        (ge, ":cur_gold", reg5),
      ], "Go on. (Pay from treasury)",
        [
          (call_script, "script_dplmc_withdraw_from_treasury", reg5),
          (party_set_slot, "$g_encountered_party", slot_center_current_improvement, "$g_improvement_type"),
          (store_current_hours, ":cur_hours"),
          (store_mul, ":hours_takes", reg6, 24),
          (val_add, ":hours_takes", ":cur_hours"),
          (party_set_slot, "$g_encountered_party", slot_center_improvement_end_hour, ":hours_takes"),
          (jump_to_menu,"mnu_center_manage"),
         ]
      ),
      ##diplomacy end
      ("improve_cont",[(store_troop_gold, ":cur_gold", "trp_player"),
                       (ge, ":cur_gold", reg5)],
       "Go on.", [(troop_remove_gold, "trp_player", reg5),
                  (party_set_slot, "$g_encountered_party", slot_center_current_improvement, "$g_improvement_type"),
                  (store_current_hours, ":cur_hours"),
                  (store_mul, ":hours_takes", reg6, 24),
                  (val_add, ":hours_takes", ":cur_hours"),
                  (party_set_slot, "$g_encountered_party", slot_center_improvement_end_hour, ":hours_takes"),
                  (jump_to_menu,"mnu_center_manage"),
                  ]),
      ("forget_it",[(store_troop_gold, ":cur_gold", "trp_player"),
                     ##diplomacy begin
                    (store_troop_gold, ":cur_treasury", "trp_household_possessions"),
                    (this_or_next|ge, ":cur_treasury", reg5),
                    ##diplomacy end
                    (ge, ":cur_gold", reg5)],
       "Forget it.", [(jump_to_menu,"mnu_center_manage")]),
      ("improve_not_enough_gold",[(store_troop_gold, ":cur_gold", "trp_player"),
                                  ##diplomacy begin
                                  (store_troop_gold, ":cur_treasury", "trp_household_possessions"),
                                  (this_or_next|lt, ":cur_treasury", reg5),
                                  ##diplomacy end
                                  (lt, ":cur_gold", reg5)],
       "I don't have enough money for that.", [(jump_to_menu, "mnu_center_manage"),]),
    ],
  ),
  (
    "town_bandits_failed",mnf_disable_all_keys,
    "{s4} {s5}",
    "none",
    [
#      (call_script, "script_loot_player_items", 0),
      (store_troop_gold, ":total_gold", "trp_player"),
      (store_div, ":gold_loss", ":total_gold", 30),
      (store_random_in_range, ":random_loss", 40, 100),
      (val_add, ":gold_loss", ":random_loss"),
      (val_min, ":gold_loss", ":total_gold"),
      (troop_remove_gold, "trp_player",":gold_loss"),
      (party_set_slot, "$current_town", slot_center_has_bandits, 0),
      (party_get_num_companions, ":num_companions", "p_main_party"),
      (str_store_string, s4, "@The assasins beat you down and leave you for dead. ."),
      (str_store_string, s4, "@You have fallen. The bandits quickly search your body for every coin they can find,\
 then vanish into the night. They have left you alive, if only barely."),
      (try_begin),
        (gt, ":num_companions", 2),
        (str_store_string, s5, "@Luckily some of your companions come to search for you when you do not return, and find you lying by the side of the road. They hurry you to safety and dress your wounds."),
      (else_try),
        (str_store_string, s5, "@Luckily some passing townspeople find you lying by the side of the road, and recognise you as something other than a simple beggar. They carry you to the nearest inn and dress your wounds."),
      (try_end),
    ],
    [
      ("continue",[],"Continue...",[(change_screen_return)]),
    ],
  ),
  (
    "town_bandits_succeeded",mnf_disable_all_keys,
    "The bandits fall before you as rice to a scythe! Soon you stand alone in the streets\
 while most of your attackers lie unconscious, dead or dying.\
 Searching the bodies, you find a purse which must have belonged to a previous victim of these brutes.\
 Or perhaps, it was given to them by someone who wanted to arrange a suitable ending to your life.",
    "none",
    [
      (party_set_slot, "$current_town", slot_center_has_bandits, 0),
      (assign, "$g_last_defeated_bandits_town", "$g_encountered_party"),
      (try_begin),
        (check_quest_active, "qst_deal_with_night_bandits"),
        (neg|check_quest_succeeded, "qst_deal_with_night_bandits"),
        (quest_slot_eq, "qst_deal_with_night_bandits", slot_quest_target_center, "$g_encountered_party"),
        (call_script, "script_succeed_quest", "qst_deal_with_night_bandits"),
      (try_end),
      (store_mul, ":xp_reward", "$num_center_bandits", 117),
      (add_xp_to_troop, ":xp_reward", "trp_player"),
      (store_mul, ":gold_reward", "$num_center_bandits", 50),
      (call_script, "script_troop_add_gold","trp_player",":gold_reward"),
    ],
    [
      ("continue",[],"Continue...",[(change_screen_return)]),
    ],
  ),
 
  (
    "town",mnf_enable_hot_keys|mnf_scale_picture,
    "{s10} {s14}^{s11}{s12}{s13}",
    "none",
    [    
        (try_begin),
          (eq, "$sneaked_into_town", 1),
          (call_script, "script_music_set_situation_with_culture", mtf_sit_town_infiltrate),
        (else_try),
          (call_script, "script_music_set_situation_with_culture", mtf_sit_travel),
        (try_end),
        (store_encountered_party, "$current_town"),
        (call_script, "script_update_center_recon_notes", "$current_town"),
        (assign, "$g_defending_against_siege", 0),
        (str_clear, s3),
        (party_get_battle_opponent, ":besieger_party", "$current_town"),
        (store_faction_of_party, ":encountered_faction", "$g_encountered_party"),
        (store_relation, ":faction_relation", ":encountered_faction", "fac_player_supporters_faction"),
        (try_begin),
          (gt, ":besieger_party", 0),
          (ge, ":faction_relation", 0),
          (store_faction_of_party, ":besieger_party_faction", ":besieger_party"),
          (store_relation, ":besieger_party_relation", ":besieger_party_faction", "fac_player_supporters_faction"),
          (lt, ":besieger_party_relation", 0),
          (assign, "$g_defending_against_siege", 1),
          (assign, "$g_siege_first_encounter", 1),
          (jump_to_menu, "mnu_siege_started_defender"),
        (try_end),
        
        (try_begin),
          (is_between, "$g_encountered_party", towns_begin, towns_end),
          (store_sub, ":encountered_town_no", "$g_encountered_party", towns_begin),
          (set_achievement_stat, ACHIEVEMENT_MIGRATING_COCONUTS, ":encountered_town_no", 1),

          (assign, ":there_are_villages_not_visited", 0),
          (try_for_range, ":cur_town", towns_begin, towns_end),
            (store_sub, ":encountered_town_no", ":cur_town", towns_begin),
            (get_achievement_stat, ":town_is_visited", ACHIEVEMENT_MIGRATING_COCONUTS, ":encountered_town_no"),
            (eq, ":town_is_visited", 0),
            (assign, ":there_are_villages_not_visited", 1),
          (try_end),
          
          (try_begin),
            (eq, ":there_are_villages_not_visited", 0),
            (unlock_achievement, ACHIEVEMENT_MIGRATING_COCONUTS),
          (try_end),
        (try_end),  

        #Quest menus
        
        #gekokujo 3.1 labor start
        (try_begin),
          (gt, "$auto_enter_menu_in_center", 0),
          (jump_to_menu, "$auto_enter_menu_in_center"),
          (assign, "$auto_enter_menu_in_center", 0),
        (try_end),
        #gekokujo 3.1 labor end
        
        (assign, "$qst_collect_taxes_currently_collecting", 0),
        
        (try_begin),
          (gt, "$quest_auto_menu", 0),
          (jump_to_menu, "$quest_auto_menu"),
          (assign, "$quest_auto_menu", 0),
        (try_end),

        (try_begin),
##          (eq, "$g_center_under_siege_battle", 1),
##          (jump_to_menu,"mnu_siege_started_defender"),
##        (else_try),
          (eq, "$g_town_assess_trade_goods_after_rest", 1),
          (assign, "$g_town_assess_trade_goods_after_rest", 0),
          (jump_to_menu,"mnu_town_trade_assessment"),
        (try_end),

        (assign, "$talk_context", 0),
        (assign,"$all_doors_locked",0),

        (try_begin),
          (eq, "$g_town_visit_after_rest", 1),
          (assign, "$g_town_visit_after_rest", 0),
          (assign, "$town_entered", 1),
        (try_end),

        (try_begin),
          (eq,"$g_leave_town",1),
          (assign,"$g_leave_town",0),
          (assign,"$g_permitted_to_center",0),
          (leave_encounter),
          (change_screen_return),
        (try_end),
        
        (str_store_party_name, s2, "$current_town"),
        (party_get_slot, ":center_lord", "$current_town", slot_town_lord),
        (store_faction_of_party, ":center_faction", "$current_town"),
        (str_store_faction_name, s9, ":center_faction"),
        (try_begin),
          (ge, ":center_lord", 0),
          (str_store_troop_name,s8,":center_lord"),
          (str_store_string,s7,"@{s8} of {s9}"),
        (try_end),
        
        (try_begin),
          (party_slot_eq,"$current_town",slot_party_type, spt_town),

          (str_store_string, s60, s2),
		  
		  (party_get_slot, ":prosperity", "$current_town", slot_town_prosperity),
		  (try_begin),
			(ge, "$cheat_mode", 1),
			(assign, reg4, ":prosperity",),
			(display_message, "@{!}DEBUG -- Prosperity: {reg4}"),
		  (try_end),

	 #          (val_add, ":prosperity", 5),
          (store_div, ":str_id", ":prosperity", 10),
		  (val_min, ":str_id", 9),
		  (val_add, ":str_id", "str_town_prosperity_0"),
          (str_store_string, s10, ":str_id"),

          (store_div, ":str_id", ":prosperity", 20),
		  (val_min, ":str_id", 4),
		  (val_add, ":str_id", "str_town_alt_prosperity_0"),
		  
          (str_store_string, s14, ":str_id"),

		  
        (else_try),
		  (str_clear, s14),
          (str_store_string,s10,"@You are at {s2}."),
        (try_end),
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
			(str_store_string, s11, "@former overlord"),
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
          (party_slot_eq,"$current_town",slot_party_type, spt_castle),
          (try_begin),
            (eq, ":center_lord", "trp_player"),
            (str_store_string,s11,"@ Your own banner flies over the castle gate."),
	      ##diplomacy start+ If reg0 > 0, a relation string was written to {s11} above
		  (else_try),
			(ge, reg0, 1),
			(str_store_string, s11, "@ You see the banner of your {s11} {s7} over the castle gate."),
		  ##diplomacy end+
		  (else_try),
			(gt, ":center_lord", -1),
			(troop_slot_eq, ":center_lord", slot_troop_spouse, "trp_player"),
            (str_store_string,s11,"str__you_see_the_banner_of_your_wifehusband_s7_over_the_castle_gate"),
		  (else_try),
            (ge, ":center_lord", 0),
            (str_store_string,s11,"@ You see the banner of {s7} over the castle gate."),
          (else_try),
##            (str_store_string,s11,"@ This castle seems to belong to no one."),
            (str_store_string,s11,"@ This castle has no garrison."),
          (try_end),
        (else_try),
          (try_begin),
            (eq, ":center_lord", "trp_player"),
            (str_store_string,s11,"@ Your own banner flies over the town gates."),
	      ##diplomacy start+ If reg0 > 0, a relation string was written to {s11} above
		  (else_try),
			(ge, reg0, 1),
			(str_store_string, s11, "@ The banner of your {s11} {s7} flies over the town gates."),
		  ##diplomacy end+
		  (else_try),	
			(gt, ":center_lord", -1),
			(troop_slot_eq, ":center_lord", slot_troop_spouse, "trp_player"),
            (str_store_string,s11,"str__the_banner_of_your_wifehusband_s7_flies_over_the_town_gates"),
          (else_try),
            (ge, ":center_lord", 0),
            (str_store_string,s11,"@ You see the banner of {s7} over the town gates."),
          (else_try),
##            (str_store_string,s11,"@ The townsfolk here have declared their independence."),
            (str_store_string,s11,"@ This town has no garrison."),
          (try_end),
        (try_end),
		##diplomacy start+
		(assign, reg0, ":save_reg0"),#revert variables
		(assign, reg4, ":save_reg4"),
		##diplomacy end+

        (str_clear, s12),
        (try_begin),
          (party_slot_eq,"$current_town",slot_party_type, spt_town),
          (party_get_slot, ":center_relation", "$current_town", slot_center_player_relation),
          (call_script, "script_describe_center_relation_to_s3", ":center_relation"),
          (assign, reg9, ":center_relation"),
          (str_store_string, s12, "@{!} {s3} ({reg9})."),
        (try_end),

        (str_clear, s13),
        (try_begin), 
          (gt,"$entry_to_town_forbidden",0),
          (str_store_string, s13, "@ You have successfully sneaked in."),
		(else_try),  
		  (faction_slot_eq, ":center_faction", slot_faction_ai_state, sfai_feast),
		  (faction_slot_eq, ":center_faction", slot_faction_ai_object, "$current_town"),
		  
          (str_store_string, s13, "str__the_lord_is_currently_holding_a_feast_in_his_hall"),
        (try_end),

        #forbidden to enter?
        (try_begin), 
          (store_time_of_day,reg(12)),
          (ge,reg(12),5),
          (lt,reg(12),21),
          (assign,"$town_nighttime",0),
        (else_try),
          (assign,"$town_nighttime",1),
          (party_slot_eq,"$current_town",slot_party_type, spt_town),
          (str_store_string, s13, "str_town_nighttime"),
        (try_end),

        (try_begin),
          (party_slot_ge, "$current_town", slot_town_has_tournament, 1),
          (neg|is_currently_night),
          (party_set_slot, "$current_town", slot_town_has_tournament, 1),
          (str_store_string, s13, "@{s13} A tournament will be held here soon."),
        (try_end),

        (assign,"$castle_undefended",0),
        (party_get_num_companions, ":castle_garrison_size", "p_collective_enemy"),
        (try_begin),
          (eq,":castle_garrison_size",0),
          (assign,"$castle_undefended",1),
        (try_end),

		(call_script, "script_set_town_picture"),
		
#		(str_clear, s5), #alert player that there are new rumors
#		(try_begin),
#			(eq, 1, 0),
#			(neg|is_currently_night),
#			(str_store_string, s5, "@^The buzz of excited voices as you come near the gate suggests to you that news of some import is circulating among the townsfolk."),
#			(lt, "$last_town_log_entry_checked", "$num_log_entries"),
#			(assign, "$g_town_rumor_log_entry", 0),
#			(try_for_range, ":log_entry", "$last_town_log_entry_checked", "$num_log_entries"),
#				(eq, ":log_entry", 4123), #placeholder to avoid having unused variable error message
#			(try_end),
#			(assign, "$last_town_log_entry_checked", "$num_log_entries"),
#		(try_end),
        ],
    [
      ("castle_castle",
      [        
        (party_slot_eq,"$current_town",slot_party_type, spt_castle),        
        
        (eq, "$sneaked_into_town", 0),         
        
        (str_clear, s1),
        (try_begin),
          (store_faction_of_party, ":center_faction", "$current_town"),
          (faction_slot_eq, ":center_faction", slot_faction_ai_state, sfai_feast),
          (faction_slot_eq, ":center_faction", slot_faction_ai_object, "$current_town"),
          (str_store_string, s1, "str__join_the_feast"),
        (try_end),
        ],"Go to the Lord's hall{s1}.",
       [          
           (try_begin),
             (this_or_next|eq, "$all_doors_locked", 1),
             (eq, "$sneaked_into_town", 1),           
             (display_message,"str_door_locked",0xFFFFAAAA),
           (else_try),
		     (this_or_next|neq, "$players_kingdom", "$g_encountered_party_faction"),
		     (neg|troop_slot_ge, "trp_player", slot_troop_renown, 50),
			 (neg|troop_slot_ge, "trp_player", slot_troop_renown, 125),
			 (neq, "$g_player_eligible_feast_center_no", "$current_town"),

			 (faction_slot_eq, "$g_encountered_party_faction", slot_faction_ai_state, sfai_feast),
			 (faction_slot_eq, "$g_encountered_party_faction", slot_faction_ai_object, "$g_encountered_party"),
			 
			 (neg|check_quest_active, "qst_wed_betrothed"),
			 (neg|check_quest_active, "qst_wed_betrothed_female"),
			 
			 (neg|troop_slot_ge, "trp_player", slot_troop_spouse, active_npcs_begin), #Married players always make the cut
			 
			 (jump_to_menu, "mnu_cannot_enter_court"),
		   (else_try),
             (assign, "$town_entered", 1),
             (call_script, "script_enter_court", "$current_town"),
           (try_end),
        ], "Way to the castle."),
		
      ("join_tournament", [(neg|is_currently_night),(party_slot_ge, "$current_town", slot_town_has_tournament, 1),]
      #("join_tournament", [(party_slot_eq,"$current_town",slot_party_type, spt_town),] #debug mode
       ,"Join the tournament.",
       [
           (call_script, "script_fill_tournament_participants_troop", "$current_town", 1),
           (assign, "$g_tournament_cur_tier", 0),
           (assign, "$g_tournament_player_team_won", -1),
           (assign, "$g_tournament_bet_placed", 0),
           (assign, "$g_tournament_bet_win_amount", 0),
           (assign, "$g_tournament_last_bet_tier", -1),
           (assign, "$g_tournament_next_num_teams", 0),
           (assign, "$g_tournament_next_team_size", 0),
           (jump_to_menu, "mnu_town_tournament"),
        ]),
      
      ("town_castle",[        
          (party_slot_eq,"$current_town",slot_party_type, spt_town),        
          (eq,"$entry_to_town_forbidden",0),        
          (str_clear, s1),
          (try_begin),
            (store_faction_of_party, ":center_faction", "$current_town"),
            (faction_slot_eq, ":center_faction", slot_faction_ai_state, sfai_feast),
            (faction_slot_eq, ":center_faction", slot_faction_ai_object, "$current_town"),
            (str_store_string, s1, "str__join_the_feast"),
          (try_end),

          ],"Go to the castle{s1}.",
       [           
           (try_begin),
             (this_or_next|eq, "$all_doors_locked", 1),
             (eq, "$sneaked_into_town", 1),           
             (display_message,"str_door_locked",0xFFFFAAAA),
           (else_try),
		     (this_or_next|neq, "$players_kingdom", "$g_encountered_party_faction"),
		     (neg|troop_slot_ge, "trp_player", slot_troop_renown, 50),
		     (neg|troop_slot_ge, "trp_player", slot_troop_renown, 125),
			 (neq, "$g_player_eligible_feast_center_no", "$current_town"),			 
			 
			 (faction_slot_eq, "$g_encountered_party_faction", slot_faction_ai_state, sfai_feast),
			 (faction_slot_eq, "$g_encountered_party_faction", slot_faction_ai_object, "$g_encountered_party"),

			 (neg|check_quest_active, "qst_wed_betrothed"),
			 (neg|check_quest_active, "qst_wed_betrothed_female"),
			 
			 (neg|troop_slot_ge, "trp_player", slot_troop_spouse, active_npcs_begin), #Married players always make the cut
			 
             (jump_to_menu, "mnu_cannot_enter_court"),
			(else_try),
			  (assign, "$town_entered", 1),              
              (call_script, "script_enter_court", "$current_town"),
           (try_end),
        ], "Way to the castle."),
      
#deprecated:
##Gekokujo Talk to the Major----------------------------------------------------------------------------------
#     ("talk_mayor",[
#          (party_slot_eq,"$current_town",slot_party_type, spt_town),
#          (this_or_next|eq,"$entry_to_town_forbidden",0),
#          (eq, "$sneaked_into_town",1)]
#       ,"Talk to the Guild Master.",
#       [
#           (assign, "$talk_context", 0),
#           (try_begin),
#             (call_script, "script_cf_enter_center_location_bandit_check"),
#           (else_try),
#             (party_get_slot, ":town_scene", "$current_town", slot_town_center),
#             (modify_visitors_at_site, ":town_scene"),
#             (reset_visitors),
#             (assign, "$g_mt_mode", tcm_default),
#             (store_faction_of_party, ":town_faction","$current_town"),
#             (try_begin),
#               (neq, ":town_faction", "fac_player_supporters_faction"),
#               (faction_get_slot, ":troop_prison_guard", "$g_encountered_party_faction", slot_faction_prison_guard_troop),
#               (faction_get_slot, ":troop_castle_guard", "$g_encountered_party_faction", slot_faction_castle_guard_troop),
#               (set_visitor, 23, ":troop_castle_guard"),
#               (set_visitor, 24, ":troop_prison_guard"),
#             (try_end),
#             (faction_get_slot, ":tier_2_troop", ":town_faction", slot_faction_tier_2_troop),
#             (faction_get_slot, ":tier_3_troop", ":town_faction", slot_faction_tier_3_troop),

#             (try_begin),
#               (gt,":tier_2_troop", 0),
#               (assign,reg(0),":tier_3_troop"),
#               (assign,reg(1),":tier_3_troop"),
#               (assign,reg(2),":tier_2_troop"),
#               (assign,reg(3),":tier_2_troop"),
#             (else_try),
#               (assign,reg(0),"trp_hired_warrior_veteran"),
#               (assign,reg(1),"trp_hired_warrior_veteran"),
#               (assign,reg(2),"trp_hired_gunner"),
#               (assign,reg(3),"trp_hired_warrior"),
#             (try_end),
#             (shuffle_range,0,4),
#             (set_visitor,25,reg(0)),
#             (set_visitor,26,reg(1)),
#             (set_visitor,27,reg(2)),
#             (set_visitor,28,reg(3)),

#             (party_get_slot, ":spawned_troop", "$current_town", slot_town_armorer),
#             (set_visitor, 9, ":spawned_troop"),
#             (party_get_slot, ":spawned_troop", "$current_town", slot_town_weaponsmith),
#             (set_visitor, 10, ":spawned_troop"),
#             (party_get_slot, ":spawned_troop", "$current_town", slot_town_horse_merchant),
#             (set_visitor, 12, ":spawned_troop"),
#             (party_get_slot, ":spawned_troop", "$current_town", slot_town_elder),
#             (set_visitor, 11, ":spawned_troop"),

#             (call_script, "script_init_town_walkers"),
#             (set_jump_mission,"mt_town_center"),
#             (assign, ":override_state", af_override_horse),
#             (try_begin),
#               (eq, "$sneaked_into_town", 1), #setup disguise
#               (assign, ":override_state", af_override_all),
#             (try_end),
#             (mission_tpl_entry_set_override_flags, "mt_town_center", 0, ":override_state"),
#             (mission_tpl_entry_set_override_flags, "mt_town_center", 2, ":override_state"),
#             (mission_tpl_entry_set_override_flags, "mt_town_center", 3, ":override_state"),
#             (mission_tpl_entry_set_override_flags, "mt_town_center", 4, ":override_state"),
#             (mission_tpl_entry_set_override_flags, "mt_town_center", 5, ":override_state"),
#             (mission_tpl_entry_set_override_flags, "mt_town_center", 6, ":override_state"),
#             (mission_tpl_entry_set_override_flags, "mt_town_center", 7, ":override_state"),
#             (try_begin),
#               (eq, "$town_entered", 0),
#               (assign, "$town_entered", 1),
#               (eq, "$town_nighttime", 0),
#               (set_jump_entry, 1),
#             (try_end),
#             (jump_to_scene, ":town_scene"),
#             (change_screen_map_conversation, ":spawned_troop"),
#           (try_end),
#        ],"Door to the town center."),
#----------------------------------------------------------------------------------      
	  
      ("town_center",
      [                        
        (party_slot_eq, "$current_town", slot_party_type, spt_town),
        (this_or_next|eq,"$entry_to_town_forbidden",0),
        (eq, "$sneaked_into_town",1)
      ],
      "Take a walk around the streets.",
       [
         #If the player is fighting his or her way out
         (try_begin),
           (eq, "$talk_context", tc_prison_break),
           (assign, "$talk_context", tc_escape),
           (assign, "$g_mt_mode", tcm_escape),
           (store_faction_of_party, ":town_faction", "$current_town"),
           (faction_get_slot, ":tier_2_troop", ":town_faction", slot_faction_tier_2_troop),
           (faction_get_slot, ":tier_3_troop", ":town_faction", slot_faction_tier_3_troop),
           (faction_get_slot, ":tier_4_troop", ":town_faction", slot_faction_tier_4_troop),
           (party_get_slot, ":town_scene", "$current_town", slot_town_center),
           (modify_visitors_at_site, ":town_scene"),
           (reset_visitors),
           #ideally we could alarm troops at locations
           (try_begin), 
	         #if guards have not gone to some other important happening at nearby villages, then spawn 4 guards. (example : fire)
             (party_get_slot, ":last_nearby_fire_time", "$current_town", slot_town_last_nearby_fire_time),                          
             (store_current_hours, ":cur_time"),
             (store_add, ":fire_finish_time", ":last_nearby_fire_time", fire_duration),
                                                    
             (neg|is_between, ":cur_time", ":last_nearby_fire_time", ":fire_finish_time"),
             (store_time_of_day, ":cur_day_hour"),
             (try_begin), #there are 6 guards at day time (no fire ext)
               (ge, ":cur_day_hour", 6),
               (lt, ":cur_day_hour", 22),
               (set_visitors, 25, ":tier_2_troop", 2),
               (set_visitors, 26, ":tier_2_troop", 1),
               (set_visitors, 27, ":tier_3_troop", 2),
               (set_visitors, 28, ":tier_4_troop", 1),
             (else_try),  #only 4 guards because of night
               (set_visitors, 25, ":tier_2_troop", 1),
               (set_visitors, 26, ":tier_2_troop", 1),
               (set_visitors, 27, ":tier_3_troop", 1),
               (set_visitors, 28, ":tier_4_troop", 1),
             (try_end),
           (else_try),
	         #if guards have gone to some other important happening at nearby villages, then spawn only 1 guard. (example : fire)
             (store_time_of_day, ":cur_day_hour"),
             (try_begin), #only 2 guard because there is a fire at one owned village
               (ge, ":cur_day_hour", 6),
               (lt, ":cur_day_hour", 22),
               (set_visitors, 25, ":tier_2_troop", 1),
               (set_visitors, 26, ":tier_2_troop", 0),
               (set_visitors, 27, ":tier_3_troop", 1),
               (set_visitors, 28, ":tier_4_troop", 0),
             (else_try), #only 1 guard because both night and there is a fire at one owned village
               (set_visitors, 25, ":tier_2_troop", 1),
               (set_visitors, 26, ":tier_2_troop", 0),
               (set_visitors, 27, ":tier_3_troop", 0),
               (set_visitors, 28, ":tier_4_troop", 0),
             (try_end),                   
           (try_end),
           (set_jump_mission,"mt_town_center"),
           (jump_to_scene, ":town_scene"),
           (change_screen_mission),
            #If you're already at escape, then talk context will reset
         (else_try),
           (assign, "$talk_context", 0),
           (call_script, "script_cf_enter_center_location_bandit_check"),
           #All other circumstances...
         (else_try),
           (party_get_slot, ":town_scene", "$current_town", slot_town_center),
           (modify_visitors_at_site, ":town_scene"),
           (reset_visitors),
           (assign, "$g_mt_mode", tcm_default),
           (store_faction_of_party, ":town_faction","$current_town"),
                      
           (try_begin),
             (neq, ":town_faction", "fac_player_supporters_faction"),
             (faction_get_slot, ":troop_prison_guard", "$g_encountered_party_faction", slot_faction_prison_guard_troop),
             (faction_get_slot, ":troop_castle_guard", "$g_encountered_party_faction", slot_faction_castle_guard_troop),
             (faction_get_slot, ":tier_2_troop", ":town_faction", slot_faction_tier_2_troop),
             (faction_get_slot, ":tier_3_troop", ":town_faction", slot_faction_tier_3_troop),
           (else_try),
             (party_get_slot, ":town_original_faction", "$current_town", slot_center_original_faction),
             (faction_get_slot, ":troop_prison_guard", ":town_original_faction", slot_faction_prison_guard_troop),
             (faction_get_slot, ":troop_castle_guard", ":town_original_faction", slot_faction_castle_guard_troop),
             (faction_get_slot, ":tier_2_troop", ":town_original_faction", slot_faction_tier_2_troop),
             (faction_get_slot, ":tier_3_troop", ":town_original_faction", slot_faction_tier_3_troop),
           (try_end),
           (try_begin), #think about this, should castle guard have to go nearby fire too? If he do not go, killing 2 armored guard is too hard for player. For now he goes too.
             #if guards have not gone to some other important happening at nearby villages, then spawn 4 guards. (example : fire)
             (party_get_slot, ":last_nearby_fire_time", "$current_town", slot_town_last_nearby_fire_time),
             (store_current_hours, ":cur_time"),
             (store_add, ":fire_finish_time", ":last_nearby_fire_time", fire_duration),

             (neg|is_between, ":cur_time", ":last_nearby_fire_time", ":fire_finish_time"),
             (set_visitor, 23, ":troop_castle_guard"),
           (try_end),
           (set_visitor, 24, ":troop_prison_guard"),
           
           (try_begin),
             (gt,":tier_2_troop", 0),
             (assign,reg0,":tier_3_troop"),
             (assign,reg1,":tier_3_troop"),
             (assign,reg2,":tier_2_troop"),
             (assign,reg3,":tier_2_troop"),
           (else_try),
             (assign,reg0,"trp_gekokujo_uesugi_retainer"),
             (assign,reg1,"trp_gekokujo_uesugi_retainer"),
             (assign,reg2,"trp_gekokujo_uesugi_skirmisher"),
             (assign,reg3,"trp_gekokujo_uesugi_samurai_archer"),
           (try_end),
           (shuffle_range,0,4),
         
           (try_begin),
             #if guards have not gone to some other important happening at nearby villages, then spawn 4 guards. (example : fire)
             (party_get_slot, ":last_nearby_fire_time", "$current_town", slot_town_last_nearby_fire_time),
             (store_current_hours, ":cur_time"),
             (store_add, ":fire_finish_time", ":last_nearby_fire_time", fire_duration),

             (neg|is_between, ":cur_time", ":last_nearby_fire_time", ":fire_finish_time"),
             (set_visitor,25,reg0),
             (set_visitor,26,reg1),
             (set_visitor,27,reg2),
             (set_visitor,28,reg3),
           (try_end),
         
           (party_get_slot, ":spawned_troop", "$current_town", slot_town_armorer),
           (set_visitor, 9, ":spawned_troop"),
           (party_get_slot, ":spawned_troop", "$current_town", slot_town_weaponsmith),
           (set_visitor, 10, ":spawned_troop"),
           (party_get_slot, ":spawned_troop", "$current_town", slot_town_elder),
           (set_visitor, 11, ":spawned_troop"),
           (party_get_slot, ":spawned_troop", "$current_town", slot_town_horse_merchant),
           (set_visitor, 12, ":spawned_troop"),
           (call_script, "script_init_town_walkers"),
           (set_jump_mission,"mt_town_center"),
           (assign, ":override_state", af_override_horse),
           (try_begin),
             (eq, "$sneaked_into_town", 1), #setup disguise
             (assign, ":override_state", af_override_all),
           (try_end),
           (mission_tpl_entry_set_override_flags, "mt_town_center", 0, ":override_state"),
           (mission_tpl_entry_set_override_flags, "mt_town_center", 2, ":override_state"),
           (mission_tpl_entry_set_override_flags, "mt_town_center", 3, ":override_state"),
           (mission_tpl_entry_set_override_flags, "mt_town_center", 4, ":override_state"),
           (mission_tpl_entry_set_override_flags, "mt_town_center", 5, ":override_state"),
           (mission_tpl_entry_set_override_flags, "mt_town_center", 6, ":override_state"),
           (mission_tpl_entry_set_override_flags, "mt_town_center", 7, ":override_state"),
           (try_begin),
             (eq, "$town_entered", 0),
             (assign, "$town_entered", 1),
             (eq, "$town_nighttime", 0),
             (set_jump_entry, 1),
           (try_end),
           (jump_to_scene, ":town_scene"),
           (change_screen_mission),
         (try_end),	   
      ],"Door to the town center."),
      
      ("town_tavern",[
          (party_slot_eq,"$current_town",slot_party_type, spt_town),
          (this_or_next|eq,"$entry_to_town_forbidden",0),
          (eq, "$sneaked_into_town",1),
#          (party_get_slot, ":scene", "$current_town", slot_town_tavern),
#          (scene_slot_eq, ":scene", slot_scene_visited, 1), #check if scene has been visited before to allow entry from menu. Otherwise scene will only be accessible from the town center.
          ]
       ,"Visit the inn.",
       [
           (try_begin),
             (eq,"$all_doors_locked",1),
             (display_message,"str_door_locked",0xFFFFAAAA),
           (else_try),
             (call_script, "script_cf_enter_center_location_bandit_check"),
           (else_try),
             (assign, "$town_entered", 1),
             (set_jump_mission, "mt_town_default"),
             (mission_tpl_entry_set_override_flags, "mt_town_default", 0, af_override_horse),
             (try_begin),
               (eq, "$sneaked_into_town",1),
               (mission_tpl_entry_set_override_flags, "mt_town_default", 0, af_override_all),
             (try_end),
             (party_get_slot, ":cur_scene", "$current_town", slot_town_tavern),
             (jump_to_scene, ":cur_scene"),
             (scene_set_slot, ":cur_scene", slot_scene_visited, 1),

             (assign, "$talk_context", tc_tavern_talk),
             (call_script, "script_initialize_tavern_variables"),

			 (store_random_in_range, ":randomize_attacker_placement", 0, 4),

             (modify_visitors_at_site, ":cur_scene"),
             (reset_visitors),
             
             (assign, ":cur_entry", 17),

			 #this is just a cheat right now
             #(troop_set_slot, "trp_belligerent_drunk", slot_troop_cur_center, "$g_encountered_party"),
			 (try_begin),
				(eq, "$cheat_mode", 1),
				(troop_get_slot, ":drunk_location", "trp_belligerent_drunk", slot_troop_cur_center),
				(try_begin),
					(eq, "$cheat_mode", 0),
				(else_try),
					(is_between, ":drunk_location", centers_begin, centers_end),
					(str_store_party_name, s4, ":drunk_location"),
					(display_message, "str_belligerent_drunk_in_s4"),
			    (else_try),
					(display_message, "str_belligerent_drunk_not_found"),
				(try_end),
				
				(troop_get_slot, ":promoter_location", "trp_fight_promoter", slot_troop_cur_center),
				(try_begin),
					(eq, "$cheat_mode", 0),
				(else_try),
					(is_between, ":promoter_location", centers_begin, centers_end),
					(str_store_party_name, s4, ":promoter_location"),
					(display_message, "str_roughlooking_character_in_s4"),
			    (else_try),
					(display_message, "str_roughlooking_character_not_found"),
				(try_end),				
			 (try_end),
			 
			 #this determines whether or not a lord who dislikes you will commission an assassin
			 (try_begin),
				(store_current_hours, ":hours"),
				(store_sub, ":hours_since_last_attempt", ":hours", "$g_last_assassination_attempt_time"),
				(gt, ":hours_since_last_attempt", 168),
				##diplomacy start+ Support ladies owning fiefs
				#(try_for_range, ":lord", active_npcs_begin, active_npcs_end),
				(try_for_range, ":lord", heroes_begin, heroes_end),
					(this_or_next|is_between, ":lord", active_npcs_begin, active_npcs_end),
						(troop_slot_eq, ":lord", slot_troop_occupation, slto_kingdom_hero),
					#Make sure they're not retired or dead
					(neg|troop_slot_ge, ":lord", slot_troop_occupation, slto_retirement),
					#add support for non-noble personalities
					(this_or_next|troop_slot_eq, ":lord", slot_lord_reputation_type, lrep_ambitious),#"Lady MacBeth"
					(this_or_next|troop_slot_eq, ":lord", slot_lord_reputation_type, lrep_roguish),
					##diplomacy end+
					(troop_slot_eq, ":lord", slot_lord_reputation_type, lrep_debauched),
					(troop_get_slot, ":led_party", ":lord", slot_troop_leaded_party),
					(party_is_active, ":led_party"),
					(party_get_attached_to, ":led_party_attached", ":led_party"), 
					(eq, ":led_party_attached", "$g_encountered_party"),
					(call_script, "script_troop_get_relation_with_troop", "trp_player", ":lord"),
					(lt, reg0, -20),
					(assign, "$g_last_assassination_attempt_time", ":hours"),
#					(assign, "$g_last_assassination_attempt_location", "$g_encountered_party"),
#					(assign, "$g_last_assassination_attempt_perpetrator", ":lord"),
					
					(troop_set_slot, "trp_hired_assassin", slot_troop_cur_center, "$g_encountered_party"),					
				(try_end),
				##diplomacy start+
				#"Lady MacBeth" noblewomen will also attempt to have people killed on their husbands' behalf.
				(lt, "$g_last_assassination_attempt_time", ":hours"),
				(neg|troop_slot_eq, "trp_hired_assassin", slot_troop_cur_center, "$g_encountered_party"),
				(try_for_range, ":lady", kingdom_ladies_begin, kingdom_ladies_end),
					(troop_slot_eq, ":lady", slot_troop_cur_center, "$g_encountered_party"),
					(troop_slot_eq, ":lady", slot_lord_reputation_type, lrep_ambitious),#"Lady MacBeth"
					(troop_slot_eq, ":lady", slot_troop_occupation, slto_kingdom_lady),

					(call_script, "script_troop_get_player_relation", ":lady"),
					(lt, reg0, 1),
					#Will send an assassin if she doesn't like the player, and either she or her husband
					#is at -20 or worse with the player.
					(try_begin),
						(ge, reg0, -20),
						(troop_slot_ge, ":lady", slot_troop_spouse, 1),
						(troop_get_slot, reg0, ":lady", slot_troop_spouse),
						(call_script, "script_troop_get_player_relation", reg0),
					(try_end),
					(lt, reg0, -20),

					(assign, "$g_last_assassination_attempt_time", ":hours"),
					(troop_set_slot, "trp_hired_assassin", slot_troop_cur_center, "$g_encountered_party"),
				(try_end),
				##diplomacy end+
			 (try_end),	
						
			 (try_begin),
				 (eq, ":randomize_attacker_placement", 0),
				 (call_script, "script_setup_tavern_attacker", ":cur_entry"),

				 (val_add, ":cur_entry", 1),
			 (try_end),
			 
			 (try_begin),
				(eq, 1, 0),
				(troop_slot_eq, "trp_fight_promoter", slot_troop_cur_center, "$current_town"),
                (set_visitor, ":cur_entry", "trp_fight_promoter"),

                (val_add, ":cur_entry", 1),
			 (try_end),
			 
             (party_get_slot, ":mercenary_troop", "$current_town", slot_center_mercenary_troop_type),
             (party_get_slot, ":mercenary_amount", "$current_town", slot_center_mercenary_troop_amount),
             (try_begin),
			   (gt, ":mercenary_troop", 0),
               (gt, ":mercenary_amount", 0),
               (set_visitor, ":cur_entry", ":mercenary_troop"),
               (val_add, ":cur_entry", 1),
             (try_end),

			 (try_begin),
				 (eq, ":randomize_attacker_placement", 1),
				 (call_script, "script_setup_tavern_attacker", ":cur_entry"),

				 (val_add, ":cur_entry", 1),
			 (try_end),
             
             (try_for_range, ":companion_candidate", companions_begin, companions_end),
               (troop_slot_eq, ":companion_candidate", slot_troop_occupation, 0),
               (troop_slot_eq, ":companion_candidate", slot_troop_cur_center, "$current_town"),
			   (neg|troop_slot_ge, ":companion_candidate", slot_troop_prisoner_of_party, centers_begin),
			   
               (set_visitor, ":cur_entry", ":companion_candidate"),

               (val_add, ":cur_entry", 1),
             (try_end),
			 
			 (try_begin),
				 (eq, ":randomize_attacker_placement", 2),
				 (call_script, "script_setup_tavern_attacker", ":cur_entry"),

				 (val_add, ":cur_entry", 1),
			 (try_end),
			 			 
             (try_begin), #this doubles the incidence of ransom brokers and (below) minstrels
               (party_get_slot, ":ransom_broker", "$current_town", slot_center_ransom_broker),
               (gt, ":ransom_broker", 0),
               
               (assign, reg0, ":ransom_broker"),
               (assign, reg1, "$current_town"),
			   
               (set_visitor, ":cur_entry", ":ransom_broker"),
               (val_add, ":cur_entry", 1),
			 (else_try),
			   (is_between, "$g_talk_troop", ransom_brokers_begin, ransom_brokers_end),
			   (store_add, ":alternative_town", "$current_town", 9),
			   
			   (try_begin),
				(ge, ":alternative_town", towns_end),
				#gekokujo increased number of towns
				#(val_sub, ":alternative_town", 22),
				(val_sub, ":alternative_town", 32),
			   (try_end),
			   ##diplomacy start+
			   #The above code makes assumptions about the number of towns that might not be true on other maps.
			   #Changing it to support variable sizes would not be hard, but I'm not convinced that it is so
			   #desirable in the first place.
			   (is_between, ":alternative_town", centers_begin, centers_end),
			   (party_slot_eq, ":alternative_town", slot_party_type, spt_town),
			   ##diplomacy end+
			   (try_begin),
				(eq, "$cheat_mode", 1),
			    (str_store_party_name, s3, "$current_town"),
			    (str_store_party_name, s4, ":alternative_town"),
			    (display_message, "@{!}DEBUG - Current town is {s3}, but also checking {s4}"),
			   (try_end),	
			   
               (party_get_slot, ":ransom_broker", ":alternative_town", slot_center_ransom_broker),
               (gt, ":ransom_broker", 0),
			   
               (set_visitor, ":cur_entry", ":ransom_broker"),
               (val_add, ":cur_entry", 1),
             (try_end),
			 
             (try_begin),
               (party_get_slot, ":tavern_traveler", "$current_town", slot_center_tavern_traveler),
               (gt, ":tavern_traveler", 0),
               (set_visitor, ":cur_entry", ":tavern_traveler"),
               (val_add, ":cur_entry", 1),
             (try_end),
			 
             (try_begin),
               (party_get_slot, ":tavern_minstrel", "$current_town", slot_center_tavern_minstrel),
               (gt, ":tavern_minstrel", 0),
			   
               (set_visitor, ":cur_entry", ":tavern_minstrel"),
               (val_add, ":cur_entry", 1),
			 (else_try),  
			   (store_add, ":alternative_town", "$current_town", 9),
			   (try_begin),
				(ge, ":alternative_town", towns_end),
				(val_sub, ":alternative_town", 32),
			   (try_end),
			   ##diplomacy start+
			   #The above code makes assumptions about the number of towns that might not be true on other maps.
			   #Changing it to support variable sizes would not be hard, but I'm not convinced that it is so
			   #desirable in the first place.
			   (is_between, ":alternative_town", centers_begin, centers_end),
			   (party_slot_eq, ":alternative_town", slot_party_type, spt_town),
			   ##diplomacy end+
               (party_get_slot, ":tavern_minstrel", ":alternative_town", slot_center_tavern_minstrel),			   
               (gt, ":tavern_minstrel", 0),
			   
               (set_visitor, ":cur_entry", ":tavern_minstrel"),
               (val_add, ":cur_entry", 1),
             (try_end),
			 
             (try_begin),
               (party_get_slot, ":tavern_bookseller", "$current_town", slot_center_tavern_bookseller),
               (gt, ":tavern_bookseller", 0),
               (set_visitor, ":cur_entry", ":tavern_bookseller"),
               (val_add, ":cur_entry", 1),
             (try_end),
			 
			 (try_begin),
				 (eq, ":randomize_attacker_placement", 3),
				 (call_script, "script_setup_tavern_attacker", ":cur_entry"),
				 (val_add, ":cur_entry", 1),
			 (try_end),
			 			 
             (try_begin),
               (neg|check_quest_active, "qst_eliminate_bandits_infesting_village"),
               (neg|check_quest_active, "qst_deal_with_bandits_at_lords_village"),
               (assign, ":end_cond", villages_end),
               (try_for_range, ":cur_village", villages_begin, ":end_cond"),
                 (party_slot_eq, ":cur_village", slot_village_bound_center, "$current_town"),
                 (party_slot_ge, ":cur_village", slot_village_infested_by_bandits, 1),
                 (neg|party_slot_eq, ":cur_village", slot_town_lord, "trp_player"),
                 (set_visitor, ":cur_entry", "trp_farmer_from_bandit_village"),
                 (val_add, ":cur_entry", 1),
                 (assign, ":end_cond", 0),
               (try_end),
             (try_end),
             
             (try_begin),
               (eq, "$g_starting_town", "$current_town"),
                              
               (this_or_next|neg|check_quest_finished, "qst_collect_men"),
               (this_or_next|neg|check_quest_finished, "qst_learn_where_merchant_brother_is"),
               (this_or_next|neg|check_quest_finished, "qst_save_relative_of_merchant"),
               (this_or_next|neg|check_quest_finished, "qst_save_town_from_bandits"),
               (eq,  "$g_do_one_more_meeting_with_merchant", 1),
               
			   (assign, ":troop_of_merchant", 0),	
               (try_begin),
                 (eq, "$g_encountered_party_faction", "fac_kingdom_11"),
                 (assign, ":troop_of_merchant", "trp_tsu_merchant"),
               (else_try),  
                 (eq, "$g_encountered_party_faction", "fac_kingdom_10"),
                 (assign, ":troop_of_merchant", "trp_hirosaki_merchant"),
               (else_try),                   
                 (eq, "$g_encountered_party_faction", "fac_kingdom_1"),
                 (assign, ":troop_of_merchant", "trp_niigata_merchant"),
               (else_try),  
                 (eq, "$g_encountered_party_faction", "fac_kingdom_13"),
                 (assign, ":troop_of_merchant", "trp_edo_merchant"),
               (else_try),  
                 (eq, "$g_encountered_party_faction", "fac_kingdom_7"),
                 (assign, ":troop_of_merchant", "trp_sakai_merchant"),
               (else_try),  
                 (eq, "$g_encountered_party_faction", "fac_kingdom_9"),
                 (assign, ":troop_of_merchant", "trp_hakata_merchant"),
               (try_end),
			   (gt, ":troop_of_merchant", 0),	
               
               (set_visitor, ":cur_entry", ":troop_of_merchant"),
               (val_add, ":cur_entry", 1),
             (try_end),                         
             
             (change_screen_mission),
           (try_end),
        ],"Door to the inn."),
                               
#      ("town_smithy",[
#          (eq,"$entry_to_town_forbidden",0),
#          (eq,"$town_nighttime",0),
#          ],
#       "Visit the smithy.",
#       [
#           (set_jump_mission,"mt_town_default"),
#           (jump_to_scene,"$pout_scn_smithy"),
#           (change_screen_mission,0),
#        ]),

      
      ("town_merchant",
       [(party_slot_eq,"$current_town",slot_party_type, spt_town),
           (eq, 1, 0),
           (eq,"$town_nighttime",0),
           (this_or_next|eq,"$entry_to_town_forbidden",0),
           (eq, "$sneaked_into_town",1),
#           (party_get_slot, ":scene", "$current_town", slot_town_store),
#           (scene_slot_eq, ":scene", slot_scene_visited, 1), #check if scene has been visited before to allow entry from menu. Otherwise scene will only be accessible from the town center.
           ],
       "Speak with the merchant.",
       [           
           (try_begin),
             (this_or_next|eq,"$all_doors_locked",1),
             (eq,"$town_nighttime",1),
             (display_message,"str_door_locked",0xFFFFAAAA),
           (else_try),
             (assign, "$town_entered", 1),
             (set_jump_mission, "mt_town_default"),
             (mission_tpl_entry_set_override_flags, "mt_town_default", 0, af_override_horse),
             (try_begin),
               (eq, "$sneaked_into_town",1),
               (mission_tpl_entry_set_override_flags, "mt_town_default", 0, af_override_all),
             (try_end),
             (party_get_slot, ":cur_scene", "$current_town", slot_town_store),
             (jump_to_scene, ":cur_scene"),
             (scene_set_slot, ":cur_scene", slot_scene_visited, 1),
             (change_screen_mission),
           (try_end),
        ],"Door to the shop."),       
                
      ("town_arena",
       [(party_slot_eq,"$current_town",slot_party_type, spt_town),
        (eq, "$sneaked_into_town", 0),
#           (party_get_slot, ":scene", "$current_town", slot_town_arena),
#           (scene_slot_eq,  ":scene", slot_scene_visited, 1), #check if scene has been visited before to allow entry from menu. Otherwise scene will only be accessible from the town center.
           ],
       "Enter the arena.",
       [
           (try_begin),
             (this_or_next|eq,"$all_doors_locked",1),
             (eq,"$town_nighttime",1),
             (display_message,"str_door_locked",0xFFFFAAAA),
           (else_try),
             (assign, "$g_mt_mode", abm_visit),
             (assign, "$town_entered", 1),
             (set_jump_mission, "mt_arena_melee_fight"),
             (party_get_slot, ":arena_scene", "$current_town", slot_town_arena),
             (modify_visitors_at_site, ":arena_scene"),
             (reset_visitors),
             #gekokujo 3.0 arena spectator half-assed hack (sigh) start
             #(set_visitor, 43, "trp_veteran_fighter"),
             #(set_visitor, 44, "trp_hired_warrior_veteran"),
			 (store_random_in_range, ":fighter_1", 0, 8),
			 (store_random_in_range, ":fighter_2", 8, 16),
             (set_visitor, ":fighter_1", "trp_stupid_asshole"),
             (set_visitor, ":fighter_2", "trp_stupid_asshole"),
             #gekokujo 3.0 arena spectator half-assed hack (sigh) end
             (set_jump_entry, 50),
             (jump_to_scene, ":arena_scene"),
             (scene_set_slot, ":arena_scene", slot_scene_visited, 1),
             (change_screen_mission),
           (try_end),
        ],"Way to the arena."),
      ("town_dungeon",
       [(eq, 1, 0)],
       "Never: Enter the prison.",
       [	   
           (try_begin),
		    (eq, "$talk_context", tc_prison_break),
			(gt, "$g_main_attacker_agent", 0),
			
		   	(neg|agent_is_alive, "$g_main_attacker_agent"),

			(agent_get_troop_id, ":agent_type", "$g_main_attacker_agent"),
			(try_begin),
			  (eq, "$g_encountered_party_faction", "fac_player_supporters_faction"),
			  (party_get_slot, ":prison_guard_faction", "$current_town", slot_center_original_faction),
			(else_try),
			  (assign, ":prison_guard_faction", "$g_encountered_party_faction"),
			(try_end),
			(faction_slot_eq, ":prison_guard_faction", slot_faction_prison_guard_troop, ":agent_type"),

			(call_script, "script_deduct_casualties_from_garrison"),
            (call_script, "script_enter_dungeon", "$current_town", "mt_visit_town_castle"),

		   (else_try),
             (eq,"$all_doors_locked",1),
             (display_message,"str_door_locked",0xFFFFAAAA),
           (else_try),
             (this_or_next|party_slot_eq, "$current_town", slot_town_lord, "trp_player"),
             (eq, "$g_encountered_party_faction", "$players_kingdom"),
             (assign, "$town_entered", 1),
             (call_script, "script_enter_dungeon", "$current_town", "mt_visit_town_castle"),
           (else_try),
             (display_message,"str_door_locked",0xFFFFAAAA),
           (try_end),
        ],"Door to the prison."),
		
      ("castle_inspect", 
      [
         (party_slot_eq,"$current_town",slot_party_type, spt_castle),
      ],
       "Take a walk around the courtyard.",
       [
         (try_begin),
           (eq, "$talk_context", tc_prison_break),
           (assign, "$talk_context", tc_escape),
           
           (party_get_slot, ":cur_castle_exterior", "$current_town", slot_castle_exterior),
           (modify_visitors_at_site, ":cur_castle_exterior"),
           (reset_visitors),
           
           (assign, ":guard_no", 40),
           
           (party_get_num_companion_stacks, ":num_stacks", "$g_encountered_party"),
           (try_for_range, ":troop_iterator", 0, ":num_stacks"),
             #nearby fire condition start
             (party_get_slot, ":last_nearby_fire_time", "$current_town", slot_town_last_nearby_fire_time),
             (store_current_hours, ":cur_time"),
             (store_add, ":fire_finish_time", ":last_nearby_fire_time", fire_duration),  
             (this_or_next|eq, ":guard_no", 40),
             (neg|is_between, ":cur_time", ":last_nearby_fire_time", ":fire_finish_time"),
             #nearby fire condition end

             (lt, ":guard_no", 47),
             (party_stack_get_troop_id, ":cur_troop_id", "$g_encountered_party", ":troop_iterator"),
             (neg|troop_is_hero, ":cur_troop_id"),
             (party_stack_get_size, ":stack_size","$g_encountered_party",":troop_iterator"),
             (party_stack_get_num_wounded, ":num_wounded","$g_encountered_party",":troop_iterator"),
             (val_sub, ":stack_size", ":num_wounded"),
             (gt, ":stack_size", 0),
             (party_stack_get_troop_dna,":troop_dna", "$g_encountered_party", ":troop_iterator"),
             (set_visitor, ":guard_no", ":cur_troop_id", ":troop_dna"),
             (val_add, ":guard_no", 1),
           (try_end),                      
           #(set_jump_entry, 1),           
           (set_visitor, 7, "$g_player_troop"),

           (set_jump_mission,"mt_castle_visit"),
           (jump_to_scene, ":cur_castle_exterior"),
           (change_screen_mission),
            #If you're already at escape, then talk context will reset            
         (else_try),                   
           (assign, "$talk_context", tc_town_talk),
           
           (assign, "$g_mt_mode", tcm_default),
           
           (party_get_slot, ":cur_castle_exterior", "$current_town", slot_castle_exterior),
           (modify_visitors_at_site,":cur_castle_exterior"),
           (reset_visitors),

           (try_begin),
             (neq, "$g_encountered_party_faction", "fac_player_supporters_faction"),
             (faction_get_slot, ":troop_prison_guard", "$g_encountered_party_faction", slot_faction_prison_guard_troop),
           (else_try),
             (party_get_slot, ":town_original_faction", "$current_town", slot_center_original_faction),
             (faction_get_slot, ":troop_prison_guard", ":town_original_faction", slot_faction_prison_guard_troop),
           (try_end),
           (set_visitor, 24, ":troop_prison_guard"),
           
           (assign, ":guard_no", 40),
           
           (party_get_num_companion_stacks, ":num_stacks", "$g_encountered_party"),
           (try_for_range, ":troop_iterator", 0, ":num_stacks"),
             #nearby fire condition start
             (party_get_slot, ":last_nearby_fire_time", "$current_town", slot_town_last_nearby_fire_time),
             (store_current_hours, ":cur_time"),
             (store_add, ":fire_finish_time", ":last_nearby_fire_time", fire_duration),  
             (neg|is_between, ":cur_time", ":fire_finish_time", ":last_nearby_fire_time"),

             (lt, ":guard_no", 47),
             (party_stack_get_troop_id, ":cur_troop_id", "$g_encountered_party", ":troop_iterator"),
             (neg|troop_is_hero, ":cur_troop_id"),
             (party_stack_get_size, ":stack_size","$g_encountered_party",":troop_iterator"),
             (party_stack_get_num_wounded, ":num_wounded","$g_encountered_party",":troop_iterator"),
             (val_sub, ":stack_size", ":num_wounded"),
             (gt, ":stack_size", 0),
             (party_stack_get_troop_dna,":troop_dna","$g_encountered_party",":troop_iterator"),
             (set_visitor, ":guard_no", ":cur_troop_id", ":troop_dna"),
                          
             (val_add, ":guard_no", 1),
           (try_end),
           
           (try_begin),
             (eq, "$town_entered", 0),
             (assign, "$town_entered", 1),
           (try_end),
           (set_jump_entry, 1),

           (assign, ":override_state", af_override_horse),             
           (try_begin),
             (eq, "$sneaked_into_town", 1), #setup disguise
             (assign, ":override_state", af_override_all),
           (try_end),
           (set_jump_mission, "mt_castle_visit"),

           (mission_tpl_entry_set_override_flags, "mt_castle_visit", 0, ":override_state"),
           (mission_tpl_entry_set_override_flags, "mt_castle_visit", 1, ":override_state"),
           (mission_tpl_entry_set_override_flags, "mt_castle_visit", 2, ":override_state"),
           (mission_tpl_entry_set_override_flags, "mt_castle_visit", 3, ":override_state"),
           (mission_tpl_entry_set_override_flags, "mt_castle_visit", 4, ":override_state"),
           (mission_tpl_entry_set_override_flags, "mt_castle_visit", 5, ":override_state"),
           (mission_tpl_entry_set_override_flags, "mt_castle_visit", 6, ":override_state"),
           (mission_tpl_entry_set_override_flags, "mt_castle_visit", 7, ":override_state"),           
           
           (jump_to_scene, ":cur_castle_exterior"),
           (change_screen_mission),
         (try_end),
        ], "To the castle courtyard."),
        
     ("town_enterprise",
      [
        (party_slot_eq,"$current_town",slot_party_type, spt_town),
        (party_get_slot, ":item_produced", "$current_town", slot_center_player_enterprise),
		(gt, ":item_produced", 1),
        (eq,"$entry_to_town_forbidden",0),
		(call_script, "script_get_enterprise_name", ":item_produced"),
		(str_store_string, s3, reg0),
      ],	
      "Visit your {s3}.",
      [
        (store_sub, ":town_order", "$current_town", towns_begin),
		(store_add, ":master_craftsman", "trp_town_1_master_craftsman", ":town_order"),
		#gekokujo 3.1 enterprise interiors start
		#this is no longer necessary -- there's only one enterprise scene now
        #(party_get_slot, ":item_produced", "$current_town", slot_center_player_enterprise),
		#(assign, ":enterprise_scene", "scn_enterprise_mill"),
		#(try_begin),
		#	(eq, ":item_produced", "itm_bread"),
		#	(assign, ":enterprise_scene", "scn_enterprise_mill"),
		#(else_try),
		#	(eq, ":item_produced", "itm_ale"),
		#	(assign, ":enterprise_scene", "scn_enterprise_brewery"),
		#(else_try),
		#	(eq, ":item_produced", "itm_oil"),
		#	(assign, ":enterprise_scene", "scn_enterprise_oil_press"),
		#(else_try),
		#	(eq, ":item_produced", "itm_wine"),
		#	(assign, ":enterprise_scene", "scn_enterprise_winery"),
		#(else_try),
		#	(eq, ":item_produced", "itm_leatherwork"),
		#	(assign, ":enterprise_scene", "scn_enterprise_tannery"),
		#(else_try),
		#	(eq, ":item_produced", "itm_wool_cloth"),
		#	(assign, ":enterprise_scene", "scn_enterprise_wool_weavery"),
		#(else_try),
		#	(eq, ":item_produced", "itm_linen"),
		#	(assign, ":enterprise_scene", "scn_enterprise_linen_weavery"),
		#(else_try),
		#	(eq, ":item_produced", "itm_velvet"),
		#	(assign, ":enterprise_scene", "scn_enterprise_dyeworks"),
		#(else_try),
		#	(eq, ":item_produced", "itm_tools"),
		#	(assign, ":enterprise_scene", "scn_enterprise_smithy"),
		#(try_end),
        #(modify_visitors_at_site,":enterprise_scene"),
		(modify_visitors_at_site,"scn_enterprise"),
		#gekokujo 3.1 enterprise interiors end
		(reset_visitors),
        (set_visitor,0,"trp_player"),
        (set_visitor,17,":master_craftsman"),
        (set_jump_mission,"mt_town_default"),
        #(jump_to_scene,":enterprise_scene"),
        (jump_to_scene,"scn_enterprise"), #gekokujo 3.1 enterprise interiors
        (change_screen_mission),
      ],"Door to your shop."), 

    ("visit_lady",
	[
	
	(neg|troop_slot_ge, "trp_player", slot_troop_spouse, kingdom_ladies_begin),
	
	(assign, "$love_interest_in_town", 0),
	(assign, "$love_interest_in_town_2", 0),
	(assign, "$love_interest_in_town_3", 0),
	(assign, "$love_interest_in_town_4", 0),
	(assign, "$love_interest_in_town_5", 0),
	(assign, "$love_interest_in_town_6", 0),
	(assign, "$love_interest_in_town_7", 0),
	(assign, "$love_interest_in_town_8", 0),
	
	(try_for_range, ":lady_no", kingdom_ladies_begin, kingdom_ladies_end),
		(troop_slot_eq, ":lady_no", slot_troop_cur_center, "$current_town"),
		(call_script, "script_get_kingdom_lady_social_determinants", ":lady_no"),
		(assign, ":lady_guardian", reg0),
		
		(troop_slot_eq, ":lady_no", slot_troop_spouse, -1),
		(ge, ":lady_guardian", 0), #not sure when this would not be the case

		
		#must have spoken to either father or lady
		(this_or_next|troop_slot_ge, ":lady_no", slot_troop_met, 2),
			(troop_slot_eq, ":lady_guardian", slot_lord_granted_courtship_permission, 1),
		
		(neg|troop_slot_eq, ":lady_no", slot_troop_met, 4),
		
		#must have approached father
#		(this_or_next|troop_slot_eq, ":lady_guardian", slot_lord_granted_courtship_permission, 1),
#			(troop_slot_eq, ":lady_guardian", slot_lord_granted_courtship_permission, -1),
			
		
		(try_begin),
			(eq, "$love_interest_in_town", 0),
			(assign, "$love_interest_in_town", ":lady_no"),	
		(else_try),
			(eq, "$love_interest_in_town_2", 0),
			(assign, "$love_interest_in_town_2", ":lady_no"),	
		(else_try),
			(eq, "$love_interest_in_town_3", 0),
			(assign, "$love_interest_in_town_3", ":lady_no"),	
		(else_try),
			(eq, "$love_interest_in_town_4", 0),
			(assign, "$love_interest_in_town_4", ":lady_no"),	
		(else_try),
			(eq, "$love_interest_in_town_5", 0),
			(assign, "$love_interest_in_town_5", ":lady_no"),	
		(else_try),
			(eq, "$love_interest_in_town_6", 0),
			(assign, "$love_interest_in_town_6", ":lady_no"),
		(else_try),
			(eq, "$love_interest_in_town_7", 0),
			(assign, "$love_interest_in_town_7", ":lady_no"),		
		(else_try),
			(eq, "$love_interest_in_town_8", 0),
			(assign, "$love_interest_in_town_8", ":lady_no"),		
		(try_end),	
	(try_end),
	
	(gt, "$love_interest_in_town", 0),
	],
	  "Attempt to visit a lady",
       [
        (jump_to_menu, "mnu_lady_visit"),
        ], "Door to the garden."),										

#Gekokujo Town Recruitment
       ("recruit_volunteers",
       [(call_script, "script_cf_town_castle_recruit_volunteers_cond"),]
       ,"Recruit Volunteers.",
       [(jump_to_menu, "mnu_recruit_volunteers"),]
      ),
      
      ("zhaobing", 
      [
		(ge,"$player_honor",0),
        (this_or_next|eq, "$current_town", "p_town_10"),
        (this_or_next|eq, "$current_town", "p_town_31"),
        (this_or_next|eq, "$current_town", "p_town_30"),
        (this_or_next|eq, "$current_town", "p_town_21"),
        (eq, "$current_town", "p_town_1"),
		(troop_slot_ge,"trp_player",slot_troop_renown,0),	
	  ],
         "Go to zhaobing",
     [
        (jump_to_menu,"mnu_zhaobing"),
    ]),
    
    ("ceshi", 
      [
		(eq, "$gonghe", 1),
	  ],
         "招 募 共 和 志 士！",
     [
        (jump_to_menu,"mnu_zhaobing2"),

    ]),
    
  ("ceshi2", 
     [(eq, "$daomu", 1),
	  ],
         "招 募 尊 王 志 士！",
     [
        (jump_to_menu,"mnu_zhaobing3"),	
  ]),
            
      
          
   ("ceshi3", 
     [(eq, "$zuomu", 1),
	  ],
         "招 募 佐 幕 志 士！",
     [
        (jump_to_menu,"mnu_zhaobing4"),	
  ]),
            
        ("trade_with_merchants",
       [
           (party_slot_eq,"$current_town",slot_party_type, spt_town)
        ],
         "Go to the marketplace.",
         [
           (try_begin),
             (call_script, "script_cf_enter_center_location_bandit_check"),
           (else_try),
             (jump_to_menu,"mnu_town_trade"),
           (try_end),
          ]),
          
          
       

      ("walled_center_manage",
      [
        (neg|party_slot_eq, "$current_town", slot_village_state, svs_under_siege),
        (party_slot_eq, "$current_town", slot_town_lord, "trp_player"),
        (assign, reg0, 1),
        (try_begin),
          (party_slot_eq, "$current_town", slot_party_type, spt_castle),
          (assign, reg0, 0),
        (try_end),
       ],
       "Manage this {reg0?town:castle}.",
       [
           (assign, "$g_next_menu", "mnu_town"),
           (jump_to_menu, "mnu_center_manage"),
       ]),
		
      ("walled_center_move_court",
      [
        (neg|party_slot_eq, "$current_town", slot_village_state, svs_under_siege),
		##diplomacy start+ Handle player is co-ruler of kingdom
		(assign, ":is_coruler", 0),
		(try_begin),
			(is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
			(call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", "$players_kingdom"),
			(ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
			(assign, ":is_coruler", 1),
		(try_end),
		(this_or_next|eq, ":is_coruler", 1),
		##diplomacy end+
        (faction_slot_eq, "fac_player_supporters_faction", slot_faction_leader, "trp_player"),
        (party_slot_eq, "$current_town", slot_town_lord, "trp_player"),
		##diplomacy start+ Handle player is co-ruler of kingdom
		(this_or_next|eq, "$g_encountered_party_faction", "$players_kingdom"),
			(eq, "$g_encountered_party_faction", "fac_player_supporters_faction"),
		(this_or_next|eq, ":is_coruler", 1),
		##diplomacy end+
        (eq, "$g_encountered_party_faction", "fac_player_supporters_faction"),
        (neq, "$g_player_court", "$current_town"),
      ],
      "Move your court here.",
      [
        (jump_to_menu, "mnu_establish_court"),
      ]),
								
      ("castle_station_troops",
      [	  
		(party_get_slot, ":town_lord", "$current_town", slot_town_lord),
	    (str_clear, s10),
		  
	    (assign, ":player_can_draw_from_garrison", 0), 
		(try_begin), #option 1 - player is town lord
		  (eq, ":town_lord", "trp_player"),
		  (assign, ":player_can_draw_from_garrison", 1),
		(else_try), #option 2 - town is unassigned and part of the player faction
		  (store_faction_of_party, ":faction", "$g_encountered_party"),
		  (eq, ":faction", "fac_player_supporters_faction"),			
		  (neg|party_slot_ge, "$g_encountered_party", slot_town_lord, active_npcs_begin), #ie, zero or -1

		  (assign, ":player_can_draw_from_garrison", 1),
		(else_try), #option 3 - town was captured by player
		  (lt, ":town_lord", 0), #ie, unassigned
		  (store_faction_of_party, ":castle_faction", "$g_encountered_party"),
		  (eq, "$players_kingdom", ":castle_faction"),
		  
		  (eq, "$g_encountered_party", "$g_castle_requested_by_player"),

		  (str_store_string, s10, "str_retrieve_garrison_warning"),
		  (assign, ":player_can_draw_from_garrison", 1),
		(else_try),
		  (lt, ":town_lord", 0), #ie, unassigned
		  (store_faction_of_party, ":castle_faction", "$g_encountered_party"),
		  (eq, "$players_kingdom", ":castle_faction"),
		  
		  (store_party_size_wo_prisoners, ":party_size", "$g_encountered_party"),
		  (eq, ":party_size", 0),
			
		  (str_store_string, s10, "str_retrieve_garrison_warning"),
		  (assign, ":player_can_draw_from_garrison", 1),
		(else_try),
		  (party_slot_ge, "$g_encountered_party", slot_town_lord, active_npcs_begin),
		  (store_faction_of_party, ":castle_faction", "$g_encountered_party"),
		  (eq, "$players_kingdom", ":castle_faction"),
		  ##diplomacy start+ can arise if using this to represent polygamy
		  (this_or_next|troop_slot_eq, ":town_lord", slot_troop_spouse, "trp_player"),
		     (troop_slot_eq, "trp_player", slot_troop_spouse, ":town_lord"),
		  (this_or_next|is_between, ":town_lord", heroes_begin, heroes_end),
		  ##diplomacy end+		  
		  (troop_slot_eq, "trp_player", slot_troop_spouse, ":town_lord"),		    

		  (assign, ":player_can_draw_from_garrison", 1),
		(try_end),

        (eq, ":player_can_draw_from_garrison", 1),
      ],
      "Manage the garrison {s10}",
      [
        (change_screen_exchange_members,1),
      ]),
	  ##diplomacy start+
	  #Other option to add troops to garrison
      ("dplmc_castle_give_troops",
      [
		(party_get_slot, ":town_lord", "$current_town", slot_town_lord),
		(store_faction_of_party, ":castle_faction", "$g_encountered_party"),
		(is_between, ":castle_faction", kingdoms_begin, kingdoms_end),

		#The player can add troops but not remove them:
		#Not owned by the player
		(neq, ":town_lord", "trp_player"),
		#Not unassigned
		(ge, ":town_lord", heroes_begin),
		#Not owned by the player's spouse
		(neg|troop_slot_eq, "trp_player", slot_troop_spouse, ":town_lord"),
		(neg|troop_slot_eq, ":town_lord", slot_troop_spouse, "trp_player"),
		#But nevertheless the owner will accept troops
		(call_script, "script_dplmc_player_can_give_troops_to_troop", ":town_lord"),

        (ge, reg0, 1),
      ],
      "Give troops to the garrison (cannot remove)",
      [
        (change_screen_give_members, "$current_town"),
      ]),
	  ##diplomacy end+

      ("castle_wait",
      [
        #(party_slot_eq,"$current_town",slot_party_type, spt_castle),
        (this_or_next|ge, "$g_encountered_party_relation", 0),
        (eq,"$castle_undefended",1),
        (assign, ":can_rest", 1),
        (str_clear, s1),
        (try_begin),
          (neg|party_slot_eq, "$current_town", slot_town_lord, "trp_player"),
		  (troop_get_slot, ":player_spouse", "trp_player", slot_troop_spouse),
          (neg|party_slot_eq, "$current_town", slot_town_lord, ":player_spouse"),

          (party_slot_ge, "$current_town", slot_town_lord, "trp_player"), #can rest for free in castles and towns with unassigned lords
          (store_faction_of_party, ":current_town_faction", "$current_town"),
          (neq, ":current_town_faction", "fac_player_supporters_faction"),
          (party_get_num_companions, ":num_men", "p_main_party"),
          (store_div, reg1, ":num_men", 4),
          (val_add, reg1, 1),
          (str_store_string, s1, "@ ({reg1} mon per night)"),
          (store_troop_gold, ":gold", "trp_player"),
          (lt, ":gold", reg1),
          (assign, ":can_rest", 0),
        (try_end),
        (eq, ":can_rest", 1),
      ],
      "Wait here for some time{s1}.",
      [
        (assign, "$auto_enter_town", "$current_town"),
        (assign, "$g_town_visit_after_rest", 1),
        (assign, "$g_last_rest_center", "$current_town"),
        (assign, "$g_last_rest_payment_until", -1),

        (try_begin),
          (party_is_active, "p_main_party"),
          (party_get_current_terrain, ":cur_terrain", "p_main_party"),
          (try_begin),
            (eq, ":cur_terrain", rt_desert),
            (unlock_achievement, ACHIEVEMENT_SARRANIDIAN_NIGHTS),
          (try_end),  
        (try_end),  

        (rest_for_hours_interactive, 24 * 7, 5, 0), #rest while not attackable
        (change_screen_return),
      ]),

      ("buy_gatling",
      [
        (party_slot_eq,"$current_town",slot_party_type, spt_town),
        (this_or_next|ge, "$g_encountered_party_relation", 0),
        (eq,"$castle_undefended",1),
      ],
      "Purchase Gatling Gun (50000 gold, max 2).",
      [
        (call_script, "script_try_buy_gatling"),
        (change_screen_return),
      ]),

##      ("rest_until_morning",
##       [
##           (this_or_next|ge, "$g_encountered_party_relation", 0),
##           (eq,"$castle_undefended",1),
##           (store_time_of_day,reg(1)),(neg|is_between,reg(1), 5, 18),
##           (eq, "$g_defending_against_siege", 0),
##        ],
##         "Rest until morning.",
##         [
##           (store_time_of_day,reg(1)),
##           (assign, reg(2), 30),
##           (val_sub,reg(2),reg(1)),
##           (val_mod,reg(2),24),
##           (assign,"$auto_enter_town","$current_town"),
##           (assign, "$g_town_visit_after_rest", 1),
##           (rest_for_hours_interactive, reg(2)),
##           (change_screen_return),
##          ]),
##      
##      ("rest_until_evening",
##       [
##           (this_or_next|ge, "$g_encountered_party_relation", 0),
##           (eq,"$castle_undefended",1),
##           (store_time_of_day,reg(1)), (is_between,reg(1), 5, 18),
##           (eq, "$g_defending_against_siege", 0),
##        ],
##         "Rest until evening.",
##         [
##           (store_time_of_day,reg(1)),
##           (assign, reg(2), 20),
##           (val_sub,reg(2),reg(1)),
##           (assign,"$auto_enter_town","$current_town"),
##           (assign, "$g_town_visit_after_rest", 1),
##           (rest_for_hours_interactive, reg(2)),
##           (change_screen_return),
##          ]),
      ("town_alley",
      [
        (party_slot_eq,"$current_town",slot_party_type, spt_town),
        (eq, "$cheat_mode", 1),
      ],
      "{!}CHEAT: Go to the alley.",
      [
        (party_get_slot, reg11, "$current_town", slot_town_alley),
        (set_jump_mission, "mt_ai_training"),
        (jump_to_scene, reg11),
        (change_screen_mission),
      ]),
      
      ("collect_taxes_qst",
      [
        (check_quest_active, "qst_collect_taxes"),
        (quest_slot_eq, "qst_collect_taxes", slot_quest_target_center, "$current_town"),
        (neg|quest_slot_eq, "qst_collect_taxes", slot_quest_current_state, 4),
        (quest_get_slot, ":quest_giver_troop", "qst_collect_taxes", slot_quest_giver_troop),
        (str_store_troop_name, s1, ":quest_giver_troop"),
        (quest_get_slot, reg5, "qst_collect_taxes", slot_quest_current_state),
      ],
      "{reg5?Continue collecting taxes:Collect taxes} due to {s1}.",
      [
        (jump_to_menu, "mnu_collect_taxes"),
      ]),
      ##diplomacy begin
      ("dplmc_guild_master_meeting",
       [(party_slot_eq,"$current_town",slot_party_type, spt_town),
	    ##nested diplomacy start+
		#rubik had a good idea: only enable this after meeting the guild master
		(assign, ":can_meet_guild_master", 0),
		(try_begin),
			#Always can jump to guild master in cheat mode.
			(eq, "$cheat_mode", 1),
			(assign, ":can_meet_guild_master", 1),
		(else_try),
			#Can jump to guild master after meeting him once.
			(party_get_slot, ":guild_master_troop", "$current_town",slot_town_elder),
			(ge, ":guild_master_troop", 1),
			(neg|troop_slot_eq, ":guild_master_troop", slot_troop_met, 0),
			(assign, ":can_meet_guild_master", 1),
		(else_try),
			#Always enable this in Praven for the sake of playability, since
			#the guild master there is weirdly hard to find.
			(this_or_next|eq, "$current_town", "p_town_6"),
			#Also enable in the starting town, to avoid confusing players into
			#thinking the menu item doesn't exist.
			(eq, "$g_starting_town", "$current_town"),
			(assign, ":can_meet_guild_master", 1),
		(try_end),
		(neq, ":can_meet_guild_master", 0),
		##nested diplomacy end+
        (this_or_next|eq,"$entry_to_town_forbidden",0),
        (eq, "$sneaked_into_town",1),
		],
       "Meet the guildmaster.",
       [
         (try_begin),
           (call_script, "script_cf_enter_center_location_bandit_check"),
         (else_try),
           (party_get_slot, ":town_scene", "$current_town", slot_town_center),
           (modify_visitors_at_site, ":town_scene"),
           (reset_visitors),

           (party_get_slot, ":guild_master_troop", "$current_town",slot_town_elder),
           (set_visitor,11,":guild_master_troop"),

           (set_jump_mission,"mt_town_center"),
           (jump_to_scene, ":town_scene"),
           (change_screen_map_conversation, ":guild_master_troop"),
         (try_end),
     ]),
	##nested diplomacy start+
	#If you can't jump to the guild master, explain why
    ("dplmc_guild_master_meeting_denied",
	[
		#Only show this when the player would get the rest of the town menu
		(party_slot_eq,"$current_town",slot_party_type, spt_town),
		(this_or_next|eq,"$entry_to_town_forbidden",0),
        (eq, "$sneaked_into_town",1),
	    #There is a valid guild master, and you haven't met him,
		#and there isn't another condition that enables the jump.
		(party_get_slot, ":guild_master_troop", "$current_town",slot_town_elder),
		(gt, ":guild_master_troop", 0),
		(eq, "$cheat_mode", 0),
		(neq, "$g_starting_town", "$current_town"),
		(neq, "$current_town", "p_town_6"),
		(troop_slot_eq, ":guild_master_troop", slot_troop_met, 0),
		(disable_menu_option),
		],
       "You have not met the guildmaster yet.",
       [
     ]),
	 ##nested diplomacy end+
	  ##diplomacy end      
      ("town_leave",[],"Leave...",
      [
        (assign, "$g_permitted_to_center",0),
        (change_screen_return,0),
		##diplomacy start+
		#Porting rubik's autobuy/autosell from Custom Commander
		(try_begin),
		  (neg|party_slot_ge, "$current_town", slot_village_infested_by_bandits, 1),
		  (call_script, "script_dplmc_initialize_autoloot", 0),#argument "0" means this does nothing if deemed unnecessary
		 (try_begin),
			(eq, "$g_dplmc_buy_food_when_leaving", 1),
			(party_get_slot, ":merchant_troop", "$current_town", slot_town_merchant),
			(gt, ":merchant_troop", 0),
			(call_script, "script_dplmc_auto_buy_food", "trp_player", ":merchant_troop"),
		 (try_end),
		 (try_begin),
			(eq, "$g_dplmc_sell_items_when_leaving", 1),
			(call_script, "script_dplmc_player_auto_sell_at_center", "$current_town"),
		 (try_end),
		(try_end),
		##diplomacy end+
      ],"Leave Area."),

      ("castle_cheat_interior",
      [
        (eq, "$cheat_mode", 1),
      ], 
      "{!}CHEAT! Interior.",
      [
        (set_jump_mission,"mt_ai_training"),
        (party_get_slot, ":castle_scene", "$current_town", slot_town_castle),
        (jump_to_scene,":castle_scene"),
        (change_screen_mission),
      ]),
                                                       
      ("castle_cheat_town_exterior",
      [
        (eq, "$cheat_mode", 1),
      ], 
      "{!}CHEAT! Exterior.",
      [
        (try_begin),
          (party_slot_eq, "$current_town",slot_party_type, spt_castle),
          (party_get_slot, ":scene", "$current_town", slot_castle_exterior),
        (else_try),
          (party_get_slot, ":scene", "$current_town", slot_town_center),
        (try_end),
        (set_jump_mission,"mt_ai_training"),
        (jump_to_scene,":scene"),
        (change_screen_mission),
      ]),
                                                       
      ("castle_cheat_dungeon",
      [
        (eq, "$cheat_mode", 1),
      ], 
      "{!}CHEAT! Prison.",
      [
        (set_jump_mission,"mt_ai_training"),
        (party_get_slot, ":castle_scene", "$current_town", slot_town_prison),
        (jump_to_scene,":castle_scene"),
        (change_screen_mission),
      ]),
      
      ("castle_cheat_town_walls",
      [
        (eq, "$cheat_mode", 1),
        (party_slot_eq,"$current_town",slot_party_type, spt_town),
      ], 
      "{!}CHEAT! Town Walls.",
      [
        (party_get_slot, ":scene", "$current_town", slot_town_walls),
        (set_jump_mission,"mt_ai_training"),
        (jump_to_scene,":scene"),
        (change_screen_mission),
      ]),

      ("cheat_town_start_siege",
      [
        (eq, "$cheat_mode", 1),
        (party_slot_eq, "$g_encountered_party", slot_center_is_besieged_by, -1),
        (lt, "$g_encountered_party_2", 1),
        (call_script, "script_party_count_fit_for_battle","p_main_party"),
        (gt, reg(0), 1),
        (try_begin),
          (party_slot_eq, "$g_encountered_party", slot_party_type, spt_town),
          (assign, reg6, 1),
        (else_try),
          (assign, reg6, 0),
        (try_end),
      ],
      "{!}CHEAT: Besiege the {reg6?town:castle}...",
      [
        (assign,"$g_player_besiege_town","$g_encountered_party"),
        (jump_to_menu, "mnu_castle_besiege"),
      ]),

      ("center_reports",
      [
        (eq, "$cheat_mode", 1),
      ], 
      "{!}CHEAT! Show reports.",
      [
        (jump_to_menu,"mnu_center_reports"),
      ]),

      ("sail_from_port",
      [
        (party_slot_eq,"$current_town",slot_party_type, spt_town),
        (eq, "$cheat_mode", 1),
        #(party_slot_eq,"$current_town",slot_town_near_shore, 1),
      ],
      "{!}CHEAT: Sail from port.",
      [
        (assign, "$g_player_icon_state", pis_ship),
        (party_set_flags, "p_main_party", pf_is_ship, 1),
        (party_get_position, pos1, "p_main_party"),
        (map_get_water_position_around_position, pos2, pos1, 6),
        (party_set_position, "p_main_party", pos2),
        (assign, "$g_main_ship_party", -1),
        (change_screen_return),
      ]),

    ]
   ),
      

  (
    "cannot_enter_court",0,
    "There is a feast in progress in the lord's hall, but you are not of sufficient status to be invited inside. Perhaps increasing your renown would win you admittance -- or you might also try distinguishing yourself at a tournament while the feast is in progress...",
    "none",
    [],
    [
	("continue", [],"Continue",
       [
        (jump_to_menu, "mnu_town"),
        ]),
	]),
  
  
  (
    "lady_visit",0,
    "Whom do you wish to visit?",
    "none",
    [],
    [

	("visit_lady_1",[(gt, "$love_interest_in_town", 0),(str_store_troop_name, s12, "$love_interest_in_town"),],
	"Visit {s12}",[(assign, "$love_interest_in_town", "$love_interest_in_town"),(jump_to_menu, "mnu_garden"),]),

	("visit_lady_2",[(gt, "$love_interest_in_town_2", 0),(str_store_troop_name, s12, "$love_interest_in_town_2"),],
	"Visit {s12}",[(assign, "$love_interest_in_town", "$love_interest_in_town_2"),(jump_to_menu, "mnu_garden"),]),

	("visit_lady_3",[(gt, "$love_interest_in_town_3", 0),(str_store_troop_name, s12, "$love_interest_in_town_3"),],
	"Visit {s12}",[(assign, "$love_interest_in_town", "$love_interest_in_town_3"),(jump_to_menu, "mnu_garden"),]),

	("visit_lady_4",[(gt, "$love_interest_in_town_4", 0),(str_store_troop_name, s12, "$love_interest_in_town_4"),],
	"Visit {s12}",[(assign, "$love_interest_in_town", "$love_interest_in_town_4"),(jump_to_menu, "mnu_garden"),]),

	("visit_lady_5",[(gt, "$love_interest_in_town_5", 0),(str_store_troop_name, s12, "$love_interest_in_town_5"),],
	"Visit {s12}",[(assign, "$love_interest_in_town", "$love_interest_in_town_5"),(jump_to_menu, "mnu_garden"),]),

	("visit_lady_6",[(gt, "$love_interest_in_town_6", 0),(str_store_troop_name, s12, "$love_interest_in_town_6"),],
	"Visit {s12}",[(assign, "$love_interest_in_town", "$love_interest_in_town_6"),(jump_to_menu, "mnu_garden"),]),
	
	("visit_lady_7",[(gt, "$love_interest_in_town_7", 0),(str_store_troop_name, s12, "$love_interest_in_town_7"),],
	"Visit {s12}",[(assign, "$love_interest_in_town", "$love_interest_in_town_7"),(jump_to_menu, "mnu_garden"),]),

	("visit_lady_8",[(gt, "$love_interest_in_town_8", 0),(str_store_troop_name, s12, "$love_interest_in_town_8"),],
	"Visit {s12}",[(assign, "$love_interest_in_town", "$love_interest_in_town_8"),(jump_to_menu, "mnu_garden"),]),

	
	("leave",[], "Leave",[(jump_to_menu, "mnu_town")]),

    ]
	),
	
  (
    "town_tournament_lost",0,
    "You have been eliminated from the tournament.{s8}",
    "none",
    [
	(str_clear, s8),
	(try_begin),
		(this_or_next|neq, "$players_kingdom", "$g_encountered_party_faction"),
			(neg|troop_slot_ge, "trp_player", slot_troop_renown, 50),
		(neg|troop_slot_ge, "trp_player", slot_troop_renown, 125),
		(gt, "$g_player_tournament_placement", 4),
		(faction_slot_eq, "$g_encountered_party_faction", slot_faction_ai_state, sfai_feast),
		(faction_slot_eq, "$g_encountered_party_faction", slot_faction_ai_object, "$g_encountered_party"),
		(str_store_string, s8, "str__however_you_have_sufficiently_distinguished_yourself_to_be_invited_to_attend_the_ongoing_feast_in_the_lords_castle"),
	(try_end),
	
        ],
    [
      ("continue", [], "Continue...",
       [(jump_to_menu, "mnu_town_tournament_won_by_another"),
        ]),
    ]
  ),
  (
    "town_tournament_won",mnf_disable_all_keys,
    "You have won the tournament of {s3}! You are filled with pride as the crowd cheers your name.\
 In addition to honour, fame and glory, you earn a prize of {reg9} mon. {s8}",
    "none",
    [
        (str_store_party_name, s3, "$current_town"),
        (call_script, "script_change_troop_renown", "trp_player", 20),
        (call_script, "script_change_player_relation_with_center", "$current_town", 1),   
        (assign, reg9, 200),
        (add_xp_to_troop, 250, "trp_player"),
        (troop_add_gold, "trp_player", reg9),
        (str_clear, s8),
        (store_add, ":total_win", "$g_tournament_bet_placed", "$g_tournament_bet_win_amount"),
        (try_begin),
          (gt, "$g_tournament_bet_win_amount", 0),
          (assign, reg8, ":total_win"),
          (str_store_string, s8, "@Moreover, you earn {reg8} mon from the clever bets you placed on yourself..."),
        (try_end),
		(try_begin),
			(this_or_next|neq, "$players_kingdom", "$g_encountered_party_faction"),
				(neg|troop_slot_ge, "trp_player", slot_troop_renown, 70),
			(neg|troop_slot_ge, "trp_player", slot_troop_renown, 145),

			(faction_slot_eq, "$g_encountered_party_faction", slot_faction_ai_state, sfai_feast),
			(faction_slot_eq, "$g_encountered_party_faction", slot_faction_ai_object, "$g_encountered_party"),
			(str_store_string, s8, "str_s8_you_are_also_invited_to_attend_the_ongoing_feast_in_the_castle"),
		(try_end),
        (troop_add_gold, "trp_player", ":total_win"),
        (assign, ":player_odds_sub", 0),
        (store_div, ":player_odds_sub", "$g_tournament_bet_win_amount", 5),
        (party_get_slot, ":player_odds", "$current_town", slot_town_player_odds),
        (val_sub, ":player_odds", ":player_odds_sub"),
        (val_max, ":player_odds", 250),
        (party_set_slot, "$current_town", slot_town_player_odds, ":player_odds"),
        (call_script, "script_play_victorious_sound"),
        
        (unlock_achievement, ACHIEVEMENT_MEDIEVAL_TIMES),
        ],
    [
      ("continue", [], "Continue...",
       [(jump_to_menu, "mnu_town"),
        ]),
    ]
  ),
  
  (
    "town_tournament_won_by_another",mnf_disable_all_keys,
    "As the only {reg3?fighter:man} to remain undefeated this day, {s1} wins the lists and the glory of this tournament.",
    "none",
    [
      (call_script, "script_get_num_tournament_participants"),
      (store_sub, ":needed_to_remove_randomly", reg0, 1),
      (try_begin),
        (troop_slot_eq, "trp_tournament_participants", 0, 0), #delete player from the participants
        (troop_set_slot, "trp_tournament_participants", 0, -1),
        (val_sub, ":needed_to_remove_randomly", 1),
      (try_end),
        (call_script, "script_remove_tournament_participants_randomly", ":needed_to_remove_randomly"),
        (call_script, "script_sort_tournament_participant_troops"),
        (troop_get_slot, ":winner_troop", "trp_tournament_participants", 0),
        (str_store_troop_name, s1, ":winner_troop"),
        (try_begin),
          (troop_is_hero, ":winner_troop"),
          (call_script, "script_change_troop_renown", ":winner_troop", 20),
        (try_end),
		##diplomacy start+ use script for gender
        #(troop_get_type, reg3, ":winner_troop"),#<- OLD
		(call_script, "script_dplmc_store_troop_is_female_reg", ":winner_troop", 3),
		##diplomacy end+
        ],
    [
      ("continue", [], "Continue...",
       [(jump_to_menu, "mnu_town"),
        ]),
    ]
  ),
  (
    "town_tournament",mnf_disable_all_keys,
    "{s1}You are at tier {reg0} of the tournament, with {reg1} participants remaining. In the next round, there will be {reg2} teams with {reg3} {reg4?fighters:fighter} each.",
    "none",
    [
        (party_set_slot, "$current_town", slot_town_has_tournament, 0), #No way to return back if this menu is left
        (call_script, "script_sort_tournament_participant_troops"),#Moving trp_player to the top of the list
        (call_script, "script_get_num_tournament_participants"),
        (assign, ":num_participants", reg0),
        (try_begin),
          (neg|troop_slot_eq, "trp_tournament_participants", 0, 0),#Player is defeated

          (assign, ":player_odds_add", 0),
          (store_div, ":player_odds_add", "$g_tournament_bet_placed", 5),
          (party_get_slot, ":player_odds", "$current_town", slot_town_player_odds),
          (val_add, ":player_odds", ":player_odds_add"),
          (val_min, ":player_odds", 4000),
          (party_set_slot, "$current_town", slot_town_player_odds, ":player_odds"),

          (jump_to_menu, "mnu_town_tournament_lost"),
        (else_try),
          (eq, ":num_participants", 1),#Tournament won
          (jump_to_menu, "mnu_town_tournament_won"),
        (else_try),
          (try_begin),
            (le, "$g_tournament_next_num_teams", 0),
            (call_script, "script_get_random_tournament_team_amount_and_size"),
            (assign, "$g_tournament_next_num_teams", reg0),
            (assign, "$g_tournament_next_team_size", reg1),
          (try_end),
          (assign, reg2, "$g_tournament_next_num_teams"),
          (assign, reg3, "$g_tournament_next_team_size"),
          (store_sub, reg4, reg3, 1),
          (str_clear, s1),
          (try_begin),
            (eq, "$g_tournament_player_team_won", 1),
            (str_store_string, s1, "@Victory is yours! You have won this melee, but now you must prepare yourself for the next round. "),
          (else_try),
            (eq, "$g_tournament_player_team_won", 0),
            (str_store_string, s1, "@You have been bested in this melee, but the master of ceremonies declares a recognition of your skill and bravery, allowing you to take part in the next round. "),
          (try_end),
          (assign, reg1, ":num_participants"),
          (store_add, reg0, "$g_tournament_cur_tier", 1),
        (try_end),
        ],
    [
      ("tournament_view_participants", [], "View participants.",
       [(jump_to_menu, "mnu_tournament_participants"),
        ]),
      ("tournament_bet", [(neq, "$g_tournament_cur_tier", "$g_tournament_last_bet_tier")], "Place a bet on yourself.",
       [(jump_to_menu, "mnu_tournament_bet"),
        ]),
      ("tournament_join_next_fight", [], "Fight in the next round.",
       [
           (party_get_slot, ":arena_scene", "$current_town", slot_town_arena),
           (modify_visitors_at_site, ":arena_scene"),
           (reset_visitors),
           #Assuming that there are enough participants for the teams
		   (assign, "$g_player_tournament_placement", "$g_tournament_cur_tier"),
		   (try_begin),
		     (gt, "$g_player_tournament_placement", 4),
		     (assign, "$g_player_eligible_feast_center_no", "$current_town"),
		   (try_end),
           (val_add, "$g_tournament_cur_tier", 1),
		   
           (store_mul, "$g_tournament_num_participants_for_fight", "$g_tournament_next_num_teams", "$g_tournament_next_team_size"),
           (troop_set_slot, "trp_tournament_participants", 0, -1),#Removing trp_player from the list
           (troop_set_slot, "trp_temp_array_a", 0, "trp_player"),
           (try_for_range, ":slot_no", 1, "$g_tournament_num_participants_for_fight"),
             (call_script, "script_get_random_tournament_participant"),
             (troop_set_slot, "trp_temp_array_a", ":slot_no", reg0),
           (try_end),
           (call_script, "script_shuffle_troop_slots", "trp_temp_array_a", 0, "$g_tournament_num_participants_for_fight"),


           (try_for_range, ":slot_no", 0, 4),#shuffle teams
             (troop_set_slot, "trp_temp_array_b", ":slot_no", ":slot_no"),
           (try_end),
           (call_script, "script_shuffle_troop_slots", "trp_temp_array_b", 0, 4),

           (assign, ":cur_slot", 0),
           (try_for_range, ":cur_team_offset", 0, "$g_tournament_next_num_teams"),
             (troop_get_slot, ":cur_team", "trp_temp_array_b", ":cur_team_offset"),
           
             (try_for_range, ":slot_no", 0, 8),#shuffle entry_points
               (troop_set_slot, "trp_temp_array_c", ":slot_no", ":slot_no"),
             (try_end),
             (call_script, "script_shuffle_troop_slots", "trp_temp_array_c", 0, 8),
           
             (try_for_range, ":cur_index", 0, "$g_tournament_next_team_size"),
               (store_mul, ":cur_entry_point", ":cur_team", 8),
               (troop_get_slot, ":entry_offset", "trp_temp_array_c", ":cur_index"),
               (val_add, ":cur_entry_point", ":entry_offset"),
               (troop_get_slot, ":troop_no", "trp_temp_array_a", ":cur_slot"),
               (set_visitor, ":cur_entry_point", ":troop_no"),
               (val_add, ":cur_slot", 1),
             (try_end),
           (try_end),

           (assign, "$g_tournament_next_num_teams", 0),
           (assign, "$g_tournament_next_team_size", 0),
           
           (assign, "$g_mt_mode", abm_tournament),
		   
		   #gekokujo 3.0 tournament loadouts -- this section is deprecated
           #(party_get_slot, ":town_original_faction", "$current_town", slot_center_original_faction),
           #(assign, ":town_index_within_faction", 0),
           #(assign, ":end_cond", towns_end),
           #(try_for_range, ":cur_town", towns_begin, ":end_cond"),
           #  (try_begin),
           #    (eq, ":cur_town", "$current_town"),
           #    (assign, ":end_cond", 0), #break
           #  (else_try),
           #    (party_slot_eq, ":cur_town", slot_center_original_faction, ":town_original_faction"),
           #    (val_add, ":town_index_within_faction", 1),
           #  (try_end),
           #(try_end),
		   #gekokujo 3.0 tournament loadouts -- this section is deprecated
           
           (set_jump_mission, "mt_arena_melee_fight"),
		   
		   #gekokujo 3.0 tournament loadouts -- this section is deprecated start
           #(try_begin),
           #  (eq, ":town_original_faction", "fac_kingdom_1"),
           #  #Swadia #Uesugi
           #  (store_mod, ":mod", ":town_index_within_faction", 4),
           #  (try_begin),
           #    (eq, ":mod", 0),
           #    (call_script, "script_set_items_for_tournament", 0, 0, 70, 30, 0, 0, 0, 0, "itm_gekokujo_hakama_1", -1),
           #  (else_try),
           #    (eq, ":mod", 1),
           #    (call_script, "script_set_items_for_tournament", 0, 0, 70, 30, 0, 0, 0, 0, "itm_gekokujo_hakama_1", -1),
           #  (else_try),
           #    (eq, ":mod", 2),
           #    (call_script, "script_set_items_for_tournament", 0, 0, 100, 0, 0, 0, 0, 0, "itm_gekokujo_hakama_1", -1),
           #  (else_try),
           #    (eq, ":mod", 3),
           #    (call_script, "script_set_items_for_tournament", 0, 0, 45, 20, 35, 0, 0, 0, "itm_gekokujo_hakama_1", -1),
           #  (try_end),
           #(else_try),
           #  (eq, ":town_original_faction", "fac_kingdom_2"),
           #  #Vaegirs #Date
           #  (store_mod, ":mod", ":town_index_within_faction", 4),
           #  (try_begin),
           #    (eq, ":mod", 0),
           #    (call_script, "script_set_items_for_tournament", 0, 0, 70, 20, 0, 0, 0, 0, "itm_gekokujo_hakama_1", -1),
           #  (else_try),
           #    (eq, ":mod", 1),
           #    (call_script, "script_set_items_for_tournament", 0, 0, 0, 0, 0, 40, 60, 0, "itm_gekokujo_hakama_1", -1),
           #  (else_try),
           #    (eq, ":mod", 2),
           #    (call_script, "script_set_items_for_tournament", 0, 0, 50, 0, 0, 20, 30, 0, "itm_gekokujo_hakama_1", -1),
           #  (else_try),
           #    (eq, ":mod", 3),
           #    (call_script, "script_set_items_for_tournament", 0, 0, 30, 10, 20, 0, 40, 0, "itm_gekokujo_hakama_1", -1),
           #  (try_end),
           #(else_try),
           #  (eq, ":town_original_faction", "fac_kingdom_3"),
           #  #Khergit  #Oda
           #  (store_mod, ":mod", ":town_index_within_faction", 2),
           #  (try_begin),
           #    (eq, ":mod", 0),
           #    (call_script, "script_set_items_for_tournament", 0, 0, 0, 0, 0, 40, 60, 0, "itm_gekokujo_hakama_1", -1),
           #  (else_try),
           #    (eq, ":mod", 1),
           #    (call_script, "script_set_items_for_tournament", 0, 0, 25, 0, 0, 30, 45, 0, "itm_gekokujo_hakama_1", -1),
           #  (try_end),
           #(else_try),
           #  (eq, ":town_original_faction", "fac_kingdom_4"),
           #  #Nords #Mori
           #  (store_mod, ":mod", ":town_index_within_faction", 3),
           #  (try_begin),
           #    (eq, ":mod", 0),
           #    (call_script, "script_set_items_for_tournament", 0, 0, 40, 60, 0, 0, 0, 0, "itm_gekokujo_hakama_1", -1),
           #  (else_try),
           #    (eq, ":mod", 1),
           #    (call_script, "script_set_items_for_tournament", 0, 0, 30, 40, 30, 0, 0, 0, "itm_gekokujo_hakama_1", -1),
           #  (else_try),
           #    (eq, ":mod", 2),
           #    (call_script, "script_set_items_for_tournament", 0, 0, 0, 100, 0, 0, 0, 0, "itm_gekokujo_hakama_1", -1),
           #  (try_end),
           #(else_try),
           #  #Rhodoks #Takeda
           #  (eq, ":town_original_faction", "fac_kingdom_5"),
           #  (call_script, "script_set_items_for_tournament", 0, 0, 60, 0, 30, 0, 30, 50, "itm_gekokujo_hakama_1", -1),
           #(else_try),
           #  #Sarranids #Tokugawa and everyone else
           #  (store_mod, ":mod", ":town_index_within_faction", 2),
           #  (try_begin),
           #    (eq, ":mod", 0),
           #    (call_script, "script_set_items_for_tournament", 0, 0, 60, 0, 30, 30, 0, 0, "itm_gekokujo_hakama_1", -1),
           #  (else_try),
           #    (call_script, "script_set_items_for_tournament", 0, 0, 60, 0, 30, 30, 0, 0, "itm_gekokujo_hakama_1", -1),
           #  (try_end),
           #(try_end),
           (call_script, "script_set_items_for_tournament"),
		   #gekokujo 3.0 tournament loadouts -- this section is deprecated end
		   
           (jump_to_scene, ":arena_scene"),
           (change_screen_mission),
        ]),
      ("leave_tournament",[],"Withdraw from the tournament.",
       [
           (jump_to_menu, "mnu_tournament_withdraw_verify"),
        ]),
    ]
  ),
  
  (
    "town_trade",0,
    "You head towards the marketplace.",
    "none",
    [],
    [
      #gekokujo 3.1 labor start
      ("gekokujo_labor", [], "Find work in town.",
        [
          (jump_to_menu, "mnu_labor"),
        ]),
      #gekokujo 3.1 labor end
    
	  ##diplomacy start+
	  #Begin auto-sell, credit rubik (Custom Commander)
      ## CC
      ("auto_sell",[],
       "Automatically sell items.",
       [
          (assign, "$g_next_menu", "mnu_town"),
          (jump_to_menu,"mnu_dplmc_trade_auto_sell_begin"),
        ]),
      ## CC
	  #End auto-sell, credit rubik (Custom Commander)
	  ##diplomacy start+
      ("assess_prices",
       [
         (store_faction_of_party, ":current_town_faction", "$current_town"),
         (store_relation, ":reln", ":current_town_faction", "fac_player_supporters_faction"),
         (ge, ":reln", 0),
         ],
       "Assess the local prices.",
       [
           (jump_to_menu,"mnu_town_trade_assessment_begin"),
        ]),
      ("trade_with_arms_merchant",[(party_slot_ge, "$current_town", slot_town_weaponsmith, 1)],
       "Trade with the arms merchant.",
       [
           (party_get_slot, ":merchant_troop", "$current_town", slot_town_weaponsmith),
           (change_screen_trade, ":merchant_troop"),
        ]),
      ("trade_with_armor_merchant",[(party_slot_ge, "$current_town", slot_town_armorer, 1)],
       "Trade with the armor merchant.",
       [
           (party_get_slot, ":merchant_troop", "$current_town", slot_town_armorer),
           (change_screen_trade, ":merchant_troop"),
        ]),
      ("trade_with_horse_merchant",[(party_slot_ge, "$current_town", slot_town_horse_merchant, 1)],
       "Trade with the horse merchant.",
       [
           (party_get_slot, ":merchant_troop", "$current_town", slot_town_horse_merchant),
           (change_screen_trade, ":merchant_troop"),
        ]),
      ("trade_with_goods_merchant",[(party_slot_ge, "$current_town", slot_town_merchant, 1)],
       "Trade with the goods merchant.",
       [
           (party_get_slot, ":merchant_troop", "$current_town", slot_town_merchant),
           (change_screen_trade, ":merchant_troop"),
        ]),
	  ##diplomacy start+
	  #Begin auto-buy, credit rubik (Custom Commander)
      ## CC
      ("auto_buy_food",[],
       "Automatically buy food.",
       [
          (assign, "$g_next_menu", "mnu_town"),
          (jump_to_menu,"mnu_dplmc_trade_auto_buy_food_begin"),
        ]),
      ## CC
	  ##diplomacy end+
      ("back_to_town_menu",[],"Head back.",
       [
           (jump_to_menu,"mnu_town"),
        ]),
    ]
  ),
## CC
##End auto-sell credit rubik (Custom Commander)
##diplomacy start+

  (
   "town_trade_assessment_begin",0, 
   #"You overhear the following details about the roads out of town :^(experimental feature -- this may go into dialogs)^{s42}^You also overhear several discussions about the price of trade goods across the local area.^You listen closely, trying to work out the best deals around.",
   "You overhear several discussions about the price of trade goods across the local area.^You listen closely, trying to work out the best deals around.",
    "none",
    [
	(str_clear, s42),
##	(call_script, "script_merchant_road_info_to_s42", "$g_encountered_party"),
	
    ],

    [
      ("continue",[],"Continue...",
       [
           (assign,"$auto_enter_town", "$current_town"),
           (assign, "$g_town_assess_trade_goods_after_rest", 1),
           (call_script, "script_get_max_skill_of_player_party", "skl_trade"),
           (val_div, reg0, 2),
           (store_sub, ":num_hours", 6, reg0),
           (assign, "$g_last_rest_center", "$current_town"),
           (assign, "$g_last_rest_payment_until", -1),
           (rest_for_hours, ":num_hours", 5, 0), #rest while not attackable
           (change_screen_return),
        ]),
      ("go_back_dot",[],"Go back.",
       [
           (jump_to_menu,"mnu_town_trade"),
        ]),
    ]
  ),
  (
    "town_trade_assessment",mnf_disable_all_keys,
    "As the party member with the highest trade skill ({reg2}), {reg3?you try to figure out:{s1} tries to figure out} the best goods to trade in. {s2}",
    "none",
    [

(call_script, "script_get_max_skill_of_player_party", "skl_trade"),
     (assign, ":max_skill", reg0),
     (assign, ":max_skill_owner", reg1),

     (assign, ":num_best_results", 0),
     (assign, ":best_result_1_item", -1),
     (assign, ":best_result_1_town", -1),
     (assign, ":best_result_1_profit", 0),
     (assign, ":best_result_2_item", -1),
     (assign, ":best_result_2_town", -1),
     (assign, ":best_result_2_profit", 0),
     (assign, ":best_result_3_item", -1),
     (assign, ":best_result_3_town", -1),
     (assign, ":best_result_3_profit", 0),
     (assign, ":best_result_4_item", -1),
     (assign, ":best_result_4_town", -1),
     (assign, ":best_result_4_profit", 0),
     (assign, ":best_result_5_item", -1),
     (assign, ":best_result_5_town", -1),
     (assign, ":best_result_5_profit", 0),

     (store_sub, ":num_towns", walled_centers_end, walled_centers_begin),
     (store_sub, ":num_goods", trade_goods_end, trade_goods_begin),
     (store_mul, ":max_iteration", ":num_towns", ":num_goods"),
     (val_mul, ":max_iteration", ":max_skill"),
     (val_div, ":max_iteration", 20),

     (assign, ":org_encountered_party", "$g_encountered_party"),

     (try_for_range, ":unused", 0, ":max_iteration"),
       (store_random_in_range, ":random_trade_good", trade_goods_begin, trade_goods_end),

       (store_random_in_range, ":random_town", towns_begin, towns_end),

       (party_get_slot, ":cur_merchant", ":org_encountered_party", slot_town_merchant),       
	   (assign, ":num_items_in_town_inventory", 0),
       (try_for_range, ":i_slot", num_equipment_kinds, max_inventory_items + num_equipment_kinds),
         (troop_get_inventory_slot, ":slot_item", ":cur_merchant", ":i_slot"),
         (try_begin),
           (eq, ":slot_item", ":random_trade_good"),           
		   (val_add, ":num_items_in_town_inventory", 1),
         (try_end),
       (try_end),

       (ge, ":num_items_in_town_inventory", 1),

       (assign, ":already_best", 0),
       
	   (try_begin),
         (eq, ":random_trade_good", ":best_result_1_item"),
         (eq, ":random_town", ":best_result_1_town"),
         (val_add, ":already_best", 1),
       (try_end),

	   (try_begin),
         (eq, ":random_trade_good", ":best_result_2_item"),
         (eq, ":random_town", ":best_result_2_town"),
         (val_add, ":already_best", 1),
       (try_end),

	   (try_begin),
         (eq, ":random_trade_good", ":best_result_3_item"),
         (eq, ":random_town", ":best_result_3_town"),
         (val_add, ":already_best", 1),
       (try_end),

	   (try_begin),
         (eq, ":random_trade_good", ":best_result_4_item"),
         (eq, ":random_town", ":best_result_4_town"),
         (val_add, ":already_best", 1),
       (try_end),

	   (try_begin),
         (eq, ":random_trade_good", ":best_result_5_item"),
         (eq, ":random_town", ":best_result_5_town"),
         (val_add, ":already_best", 1),
       (try_end),

       (le, ":already_best", 1),

       (store_item_value, ":random_trade_good_price", ":random_trade_good"),
       (assign, "$g_encountered_party", ":org_encountered_party"),
       (call_script, "script_game_get_item_buy_price_factor", ":random_trade_good"),
       (store_mul, ":random_trade_good_buy_price", ":random_trade_good_price", reg0),
       (val_div, ":random_trade_good_buy_price", 100),
       (val_max, ":random_trade_good_buy_price", 1),
       (assign, "$g_encountered_party", ":random_town"),
       (call_script, "script_game_get_item_sell_price_factor", ":random_trade_good"),
       (store_mul, ":random_trade_good_sell_price", ":random_trade_good_price", reg0),
       (val_div, ":random_trade_good_sell_price", 100),
       (val_max, ":random_trade_good_sell_price", 1),
       (store_sub, ":difference", ":random_trade_good_sell_price", ":random_trade_good_buy_price"),

       (try_begin),
	     (this_or_next|eq, ":best_result_1_item", ":random_trade_good"),
		 (this_or_next|eq, ":best_result_2_item", ":random_trade_good"),
		 (this_or_next|eq, ":best_result_3_item", ":random_trade_good"),
		 (this_or_next|eq, ":best_result_4_item", ":random_trade_good"),
		 (eq, ":best_result_5_item", ":random_trade_good"),

         (try_begin),
		   (eq, ":best_result_1_item", ":random_trade_good"),
		   (gt, ":difference", ":best_result_1_profit"),
           (assign, ":best_result_1_item", ":random_trade_good"),
           (assign, ":best_result_1_town", ":random_town"),
           (assign, ":best_result_1_profit", ":difference"),
         (else_try),
		   (eq, ":best_result_2_item", ":random_trade_good"),
		   (gt, ":difference", ":best_result_2_profit"),
           (assign, ":best_result_2_item", ":random_trade_good"),
           (assign, ":best_result_2_town", ":random_town"),
           (assign, ":best_result_2_profit", ":difference"),
		 (else_try),
		   (eq, ":best_result_3_item", ":random_trade_good"),
		   (gt, ":difference", ":best_result_3_profit"),
           (assign, ":best_result_3_item", ":random_trade_good"),
           (assign, ":best_result_3_town", ":random_town"),
           (assign, ":best_result_3_profit", ":difference"),
		 (else_try),
		   (eq, ":best_result_4_item", ":random_trade_good"),
		   (gt, ":difference", ":best_result_4_profit"),
           (assign, ":best_result_4_item", ":random_trade_good"),
           (assign, ":best_result_4_town", ":random_town"),
           (assign, ":best_result_4_profit", ":difference"),
		 (else_try),
		   (eq, ":best_result_5_item", ":random_trade_good"),
		   (gt, ":difference", ":best_result_5_profit"),
           (assign, ":best_result_5_item", ":random_trade_good"),
           (assign, ":best_result_5_town", ":random_town"),
           (assign, ":best_result_5_profit", ":difference"),
		 (try_end),
	   (else_try),
         (try_begin),
           (gt, ":difference", ":best_result_1_profit"),
           (val_add, ":num_best_results", 1),
           (val_min, ":num_best_results", 5),
           (assign, ":best_result_5_item", ":best_result_4_item"),
           (assign, ":best_result_5_town", ":best_result_4_town"),
           (assign, ":best_result_5_profit", ":best_result_4_profit"),
           (assign, ":best_result_4_item", ":best_result_3_item"),
           (assign, ":best_result_4_town", ":best_result_3_town"),
           (assign, ":best_result_4_profit", ":best_result_3_profit"),
           (assign, ":best_result_3_item", ":best_result_2_item"),
           (assign, ":best_result_3_town", ":best_result_2_town"),
           (assign, ":best_result_3_profit", ":best_result_2_profit"),
           (assign, ":best_result_2_item", ":best_result_1_item"),
           (assign, ":best_result_2_town", ":best_result_1_town"),
           (assign, ":best_result_2_profit", ":best_result_1_profit"),
           (assign, ":best_result_1_item", ":random_trade_good"),
           (assign, ":best_result_1_town", ":random_town"),
           (assign, ":best_result_1_profit", ":difference"),
         (else_try),
           (gt, ":difference", ":best_result_2_profit"),
           (val_add, ":num_best_results", 1),
           (val_min, ":num_best_results", 5),
           (assign, ":best_result_5_item", ":best_result_4_item"),
           (assign, ":best_result_5_town", ":best_result_4_town"),
           (assign, ":best_result_5_profit", ":best_result_4_profit"),
           (assign, ":best_result_4_item", ":best_result_3_item"),
           (assign, ":best_result_4_town", ":best_result_3_town"),
           (assign, ":best_result_4_profit", ":best_result_3_profit"),
           (assign, ":best_result_3_item", ":best_result_2_item"),
           (assign, ":best_result_3_town", ":best_result_2_town"),
           (assign, ":best_result_3_profit", ":best_result_2_profit"),
           (assign, ":best_result_2_item", ":random_trade_good"),
           (assign, ":best_result_2_town", ":random_town"),
           (assign, ":best_result_2_profit", ":difference"),
         (else_try),
           (gt, ":difference", ":best_result_3_profit"),
           (val_add, ":num_best_results", 1),
           (val_min, ":num_best_results", 5),
           (assign, ":best_result_5_item", ":best_result_4_item"),
           (assign, ":best_result_5_town", ":best_result_4_town"),
           (assign, ":best_result_5_profit", ":best_result_4_profit"),
           (assign, ":best_result_4_item", ":best_result_3_item"),
           (assign, ":best_result_4_town", ":best_result_3_town"),
           (assign, ":best_result_4_profit", ":best_result_3_profit"),
           (assign, ":best_result_3_item", ":random_trade_good"),
           (assign, ":best_result_3_town", ":random_town"),
           (assign, ":best_result_3_profit", ":difference"),
         (else_try),
           (gt, ":difference", ":best_result_4_profit"),
           (val_add, ":num_best_results", 1),
           (val_min, ":num_best_results", 5),
           (assign, ":best_result_5_item", ":best_result_4_item"),
           (assign, ":best_result_5_town", ":best_result_4_town"),
           (assign, ":best_result_5_profit", ":best_result_4_profit"),
           (assign, ":best_result_4_item", ":random_trade_good"),
           (assign, ":best_result_4_town", ":random_town"),
           (assign, ":best_result_4_profit", ":difference"),
         (else_try),
           (gt, ":difference", ":best_result_5_profit"),
           (val_add, ":num_best_results", 1),
           (val_min, ":num_best_results", 5),
           (assign, ":best_result_5_item", ":best_result_4_item"),
           (assign, ":best_result_5_town", ":best_result_4_town"),
           (assign, ":best_result_5_profit", ":best_result_4_profit"),
         (try_end),
	   (try_end),
     (try_end),

     (assign, "$g_encountered_party", ":org_encountered_party"),

     (str_clear, s3),
     
     (assign, reg2, ":max_skill"),
     (try_begin),
       (eq, ":max_skill_owner", "trp_player"),
       (assign, reg3, 1),
     (else_try),
       (assign, reg3, 0),
       (str_store_troop_name, s1, ":max_skill_owner"),
     (try_end),
     (try_begin),
       (le, ":num_best_results", 0),
       (str_store_string, s2, "@However, {reg3?You are:{s1} is} unable to find any trade goods that would bring a profit."),
     (else_try),
       (try_begin),
         (ge, ":best_result_5_item", 0),
         (assign, reg6, ":best_result_5_profit"),
         (str_store_item_name, s4, ":best_result_5_item"),
         (str_store_party_name, s5, ":best_result_5_town"),
         (str_store_string, s3, "@^Buying {s4} here and selling it at {s5} would bring a profit of {reg6} mon per item.{s3}"),
       (try_end),
       (try_begin),
         (ge, ":best_result_4_item", 0),
         (assign, reg6, ":best_result_4_profit"),
         (str_store_item_name, s4, ":best_result_4_item"),
         (str_store_party_name, s5, ":best_result_4_town"),
         (str_store_string, s3, "@^Buying {s4} here and selling it at {s5} would bring a profit of {reg6} mon per item.{s3}"),
       (try_end),
       (try_begin),
         (ge, ":best_result_3_item", 0),
         (assign, reg6, ":best_result_3_profit"),
         (str_store_item_name, s4, ":best_result_3_item"),
         (str_store_party_name, s5, ":best_result_3_town"),
         (str_store_string, s3, "@^Buying {s4} here and selling it at {s5} would bring a profit of {reg6} mon per item.{s3}"),
       (try_end),
       (try_begin),
         (ge, ":best_result_2_item", 0),
         (assign, reg6, ":best_result_2_profit"),
         (str_store_item_name, s4, ":best_result_2_item"),
         (str_store_party_name, s5, ":best_result_2_town"),
         (str_store_string, s3, "@^Buying {s4} here and selling it at {s5} would bring a profit of {reg6} mon per item.{s3}"),
       (try_end),
       (try_begin),
         (ge, ":best_result_1_item", 0),
         (assign, reg6, ":best_result_1_profit"),
         (str_store_item_name, s4, ":best_result_1_item"),
         (str_store_party_name, s5, ":best_result_1_town"),
         (str_store_string, s3, "@^Buying {s4} here and selling it at {s5} would bring a profit of {reg6} mon per item.{s3}"),
       (try_end), 
       (str_store_string, s2, "@{reg3?You find:{s1} finds} out the following:^{s3}"),
     (try_end),
     ],
    [
      ("continue",[],"Continue...",
       [
           (jump_to_menu,"mnu_town_trade"),
        ]),
    ]
  ),
  
  
  ( #pre lady visit
    "garden",0,
    "{s12}",
    "none",
    [
	
    (call_script, "script_get_kingdom_lady_social_determinants", "$love_interest_in_town"),
	(assign, ":guardian_lord", reg0),
	(str_store_troop_name, s11, "$love_interest_in_town"),
	
	(try_begin),
		(call_script, "script_npc_decision_checklist_male_guardian_assess_suitor", ":guardian_lord", "trp_player"),
		(lt, reg0, 0),
		(troop_set_slot, ":guardian_lord", slot_lord_granted_courtship_permission, -1),
	(try_end),
	
	(assign, "$nurse_assists_entry", 0),
	(try_begin),
		(troop_slot_eq, ":guardian_lord", slot_lord_granted_courtship_permission, 1),
		(str_store_string, s12, "str_the_guards_at_the_gate_have_been_ordered_to_allow_you_through_you_might_be_imagining_things_but_you_think_one_of_them_may_have_given_you_a_wink"),
	(else_try), #the circumstances under which the lady arranges for a surreptitious entry
		(call_script, "script_troop_get_relation_with_troop", "trp_player", "$love_interest_in_town"),
		(gt, reg0, 0),
		
		(assign, ":player_completed_quest", 0),
		(try_begin),
			(check_quest_active, "qst_visit_lady"),
			(quest_slot_eq, "qst_visit_lady", slot_quest_giver_troop, "$love_interest_in_town"),
			(assign, ":player_completed_quest", 1),
		(else_try),
			(check_quest_active, "qst_formal_marriage_proposal"),
			(quest_slot_eq, "qst_formal_marriage_proposal", slot_quest_giver_troop, "$love_interest_in_town"),
			(this_or_next|check_quest_succeeded, "qst_formal_marriage_proposal"),
				(check_quest_failed, "qst_formal_marriage_proposal"),
			(assign, ":player_completed_quest", 1),
		(else_try),
			(check_quest_active, "qst_duel_courtship_rival"),
			(quest_slot_eq, "qst_duel_courtship_rival", slot_quest_giver_troop, "$love_interest_in_town"),
			(this_or_next|check_quest_succeeded, "qst_duel_courtship_rival"),
				(check_quest_failed, "qst_duel_courtship_rival"),
			(assign, ":player_completed_quest", 1),
		(try_end),

		(try_begin),
			(store_current_hours, ":hours_since_last_visit"),
			(troop_get_slot, ":last_visit_time", "$love_interest_in_town", slot_troop_last_talk_time),
			(val_sub, ":hours_since_last_visit", ":last_visit_time"),
			(this_or_next|ge, ":hours_since_last_visit", 96), #at least four days
				(eq, ":player_completed_quest", 1),
				
			(try_begin),
				(is_between, "$g_encountered_party", towns_begin, towns_end),
				(str_store_string, s12, "str_the_guards_glare_at_you_and_you_know_better_than_to_ask_permission_to_enter_however_as_you_walk_back_towards_your_lodgings_an_elderly_lady_dressed_in_black_approaches_you_i_am_s11s_nurse_she_whispers_urgently_don_this_dress_and_throw_the_hood_over_your_face_i_will_smuggle_you_inside_the_castle_to_meet_her_in_the_guise_of_a_skullery_maid__the_guards_will_not_look_too_carefully_but_i_beg_you_for_all_of_our_sakes_be_discrete"),
				(assign, "$nurse_assists_entry", 1),
			(else_try),
				(str_store_string, s12, "str_the_guards_glare_at_you_and_you_know_better_than_to_ask_permission_to_enter_however_as_you_walk_back_towards_your_lodgings_an_elderly_lady_dressed_in_black_approaches_you_i_am_s11s_nurse_she_whispers_urgently_wait_for_a_while_by_the_spring_outside_the_walls_i_will_smuggle_her_ladyship_out_to_meet_you_dressed_in_the_guise_of_a_shepherdess_but_i_beg_you_for_all_of_our_sakes_be_discrete"),
				(assign, "$nurse_assists_entry", 2),
			(try_end),
		(else_try),	
			(str_store_string, s12, "str_the_guards_glare_at_you_and_you_know_better_than_to_ask_permission_to_enter_however_as_you_walk_back_towards_your_lodgings_an_elderly_lady_dressed_in_black_approaches_you_i_am_s11s_nurse_she_whispers_urgently_her_ladyship_asks_me_to_say_that_yearns_to_see_you_but_that_you_should_bide_your_time_a_bit_her_ladyship_says_that_to_arrange_a_clandestine_meeting_so_soon_after_your_last_encounter_would_be_too_dangerous"),
		(try_end),
	(else_try),
		(str_store_string, s12, "str_the_guards_glare_at_you_and_you_know_better_than_to_ask_permission_to_enter"),
	(try_end),
	
	],
    [

	("enter",
	[
    (call_script, "script_get_kingdom_lady_social_determinants", "$love_interest_in_town"),
	(troop_slot_eq, reg0, slot_lord_granted_courtship_permission, 1)
	], "Enter",
	[
	(jump_to_menu, "mnu_town"),
	(call_script, "script_setup_meet_lady", "$love_interest_in_town", "$g_encountered_party"),
	]
	),
     
	("nurse",
	[
    (eq, "$nurse_assists_entry", 1),
	], "Go with the nurse",
	[
	(jump_to_menu, "mnu_town"),
	(call_script, "script_setup_meet_lady", "$love_interest_in_town", "$g_encountered_party"),
	]
	),

	
	("nurse",
	[
    (eq, "$nurse_assists_entry", 2),
	], "Wait by the spring",
	[
	(jump_to_menu, "mnu_town"),
	(call_script, "script_setup_meet_lady", "$love_interest_in_town", "$g_encountered_party"),
	]
	),
	
	("leave",
	[], 
	"Leave",
	[(jump_to_menu, "mnu_town")]),

    ]
 
	 
  ),
]
