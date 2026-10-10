# -*- coding: UTF-8 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *

from module_constants import *
from ym_gatling_shop import *

####################################################################################################################
#  (menu-id, menu-flags, menu_text, mesh-name, [<operations>], [<options>]),
#
#   Each game menu is a tuple that contains the following fields:
#  
#  1) Game-menu id (string): used for referencing game-menus in other files.
#     The prefix menu_ is automatically added before each game-menu-id
#
#  2) Game-menu flags (int). See header_game_menus.py for a list of available flags.
#     You can also specify menu text color here, with the menu_text_color macro
#  3) Game-menu text (string).
#  4) mesh-name (string). Not currently used. Must be the string "none"
#  5) Operations block (list). A list of operations. See header_operations.py for reference.
#     The operations block is executed when the game menu is activated.
#  6) List of Menu options (List).
#     Each menu-option record is a tuple containing the following fields:
#   6.1) Menu-option-id (string) used for referencing game-menus in other files.
#        The prefix mno_ is automatically added before each menu-option.
#   6.2) Conditions block (list). This must be a valid operation block. See header_operations.py for reference. 
#        The conditions are executed for each menu option to decide whether the option will be shown to the player or not.
#   6.3) Menu-option text (string).
#   6.4) Consequences block (list). This must be a valid operation block. See header_operations.py for reference. 
#        The consequences are executed for the menu option that has been selected by the player.
#
#
# Note: The first Menu is the initial character creation menu.
####################################################################################################################


##split modules begin
from module_game_menus_character import game_menus_character
from module_game_menus_camp_cheat import game_menus_camp_cheat
from module_game_menus_reports import game_menus_reports
from module_game_menus_encounter_battle import game_menus_encounter_battle
from module_game_menus_town_castle_siege import game_menus_town_castle_siege
from module_game_menus_village_quests import game_menus_village_quests
from module_game_menus_trade_ship import game_menus_trade_ship
from module_game_menus_tournament_training import game_menus_tournament_training
from module_game_menus_faction_politics import game_menus_faction_politics
from module_game_menus_gekokujo import game_menus_gekokujo
from module_game_menus_recruitment_lco import game_menus_recruitment_lco
from module_game_menus_core_misc import game_menus_core_misc
##split modules end

# 聚合顺序严格保持拆分前的原始顺序（Warband 引擎按固定索引访问部分菜单：
# 例如世界地图 HUD 的"报告"按钮固定跳转索引 4 = menu_reports，菜单重排会导致跳转错乱）。
# 注意：此顺序表 = 拆分前 module_game_menus.py 的原始顺序，严禁重排已有条目！
# 新增菜单：追加到对应功能子文件末尾，并在下方 _MENU_ORDER 末尾登记其菜单 id。
from freelancer_game_menus import game_menus as game_menus_freelancer

_MENU_BUCKETS = [
    ("character", game_menus_character),
    ("camp_cheat", game_menus_camp_cheat),
    ("reports", game_menus_reports),
    ("encounter_battle", game_menus_encounter_battle),
    ("town_castle_siege", game_menus_town_castle_siege),
    ("village_quests", game_menus_village_quests),
    ("trade_ship", game_menus_trade_ship),
    ("tournament_training", game_menus_tournament_training),
    ("faction_politics", game_menus_faction_politics),
    ("gekokujo", game_menus_gekokujo),
    ("recruitment_lco", game_menus_recruitment_lco),
    ("core_misc", game_menus_core_misc),
    ("freelancer", game_menus_freelancer),
]

_MENU_INDEX = {}
for _bucket_name, _bucket in _MENU_BUCKETS:
    for _menu in _bucket:
        if _menu[0] in _MENU_INDEX:
            raise ValueError("duplicate menu id in buckets: " + _menu[0])
        _MENU_INDEX[_menu[0]] = _menu

_MENU_ORDER = [
    "start_game_0", "start_phase_2", "start_game_3", "tutorial", "reports", "custom_battle_scene", "custom_battle_end",
    "choose_skill", "past_life_explanation", "auto_return", "morale_report",
    "courtship_relations", "lord_relations", "companion_report", "faction_orders", "character_report", "party_size_report", "faction_relations_report", "camp",
    "camp_cheat", "camp_gekokujo", "cheat_gekokujo", "gekokujo_companions", "cheat_enter_scene", "cheat_enter_scene_p2", "cheat_enter_scene_p3", "gekokujo_bio",
    "cheat_find_item", "cheat_change_weather", "camp_action", "camp_recruit_prisoners", "camp_no_prisoners", "camp_action_read_book", "camp_action_read_book_start", "retirement_verify",
    "end_game", "cattle_herd", "cattle_herd_kill", "cattle_herd_kill_end", "arena_duel_fight", "arena_duel_conclusion", "simple_encounter", "encounter_retreat_confirm",
    "encounter_retreat", "order_attack_begin", "order_attack_2", "battle_debrief", "total_victory", "enemy_slipped_away", "total_defeat", "permanent_damage",
    "pre_join", "join_battle", "join_order_attack", "zendar", "salt_mine", "four_ways_inn", "test_scene", "battlefields",
    "dhorak_keep", "join_siege_outside", "cut_siege_without_fight", "besiegers_camp_with_allies", "castle_outside", "castle_guard", "castle_entry_granted", "castle_entry_denied",
    "castle_meeting", "castle_meeting_selected", "castle_besiege", "siege_attack_meets_sally", "castle_besiege_inner_battle", "construct_ladders", "send_agents", "besiege_kyoto",
    "castle_attack_walls_simulate", "castle_attack_walls_with_allies_simulate", "castle_taken_by_friends", "castle_taken", "castle_taken_2", "requested_castle_granted_to_player", "requested_castle_granted_to_player_husband", "requested_castle_granted_to_another",
    "requested_castle_granted_to_another_female", "leave_faction", "give_center_to_player", "give_center_to_player_2", "oath_fulfilled", "siege_started_defender", "siege_join_defense", "enter_your_own_castle",
    "fort", "fort_after_battle", "fort_taken", "encounter", "encounter_setup", "encounter_won", "encounter_lost", "beg",
    "crime", "getaway_failed", "getaway_succeeded", "labor", "labor_complete", "rebellion", "hidden_village", "village",
    "village_hostile_action", "recruit_volunteers", "village_hunt_down_fugitive_defeated", "village_infest_bandits_result", "village_infestation_removed", "center_manage", "center_improve", "town_bandits_failed",
    "town_bandits_succeeded", "village_steal_cattle_confirm", "village_steal_cattle", "village_take_food_confirm", "village_take_food", "village_start_attack", "village_loot_no_resist", "village_loot_complete",
    "village_loot_defeat", "village_loot_continue", "close", "town", "cannot_enter_court", "lady_visit", "town_tournament_lost", "town_tournament_won",
    "town_tournament_won_by_another", "town_tournament", "tournament_withdraw_verify", "tournament_bet", "tournament_bet_confirm", "tournament_participants", "collect_taxes", "collect_taxes_complete",
    "collect_taxes_rebels_killed", "collect_taxes_failed", "collect_taxes_revolt_warning", "collect_taxes_revolt", "train_peasants_against_bandits", "train_peasants_against_bandits_ready", "train_peasants_against_bandits_training_result", "train_peasants_against_bandits_attack",
    "train_peasants_against_bandits_attack_result", "train_peasants_against_bandits_success", "disembark", "ship_reembark", "center_reports", "price_and_production", "town_trade", "dplmc_trade_auto_sell_begin",
    "dplmc_trade_auto_buy_food_begin", "town_trade_assessment_begin", "town_trade_assessment", "sneak_into_town_suceeded", "sneak_into_town_caught", "sneak_into_town_caught_dispersed_guards", "sneak_into_town_caught_ran_away", "enemy_offer_ransom_for_prisoner",
    "training_ground", "training_ground_selection_details_melee_1", "training_ground_selection_details_melee_2", "training_ground_selection_details_mounted", "training_ground_selection_details_ranged_1", "training_ground_selection_details_ranged_2", "training_ground_description", "training_ground_training_result",
    "marshall_selection_candidate_ask", "captivity_avoid_wilderness", "captivity_start_wilderness", "captivity_start_wilderness_surrender", "captivity_start_wilderness_defeat", "captivity_start_castle_surrender", "captivity_start_castle_defeat", "captivity_start_under_siege_defeat",
    "gekokujo_captivity_avoid", "captivity_wilderness_taken_prisoner", "captivity_wilderness_check", "captivity_end_wilderness_escape", "captivity_castle_taken_prisoner", "captivity_rescue_lord_taken_prisoner", "captivity_castle_check", "captivity_end_exchanged_with_prisoner",
    "captivity_end_propose_ransom", "captivity_castle_remain", "kingdom_army_quest_report_to_army", "kingdom_army_quest_messenger", "kingdom_army_quest_join_siege_order", "kingdom_army_follow_failed", "invite_player_to_faction_without_center", "invite_player_to_faction",
    "invite_player_to_faction_accepted", "question_peace_offer", "notification_truce_expired", "notification_feast_quest_expired", "notification_sortie_possible", "notification_casus_belli_expired", "notification_lord_defects", "notification_treason_indictment",
    "notification_border_incident", "notification_player_faction_active", "minister_confirm", "notification_court_lost", "notification_player_faction_deactive", "notification_player_wedding_day", "notification_player_kingdom_holds_feast", "notification_center_under_siege",
    "notification_village_raided", "notification_village_raid_started", "notification_one_faction_left", "notification_oath_renounced_faction_defeated", "notification_center_lost", "notification_troop_left_players_faction", "notification_troop_joined_players_faction", "notification_war_declared",
    "notification_peace_declared", "notification_faction_defeated", "notification_rebels_switched_to_faction", "notification_player_should_consult", "notification_player_feast_in_progress", "notification_lady_requests_visit", "garden", "kill_local_merchant_begin",
    "debug_alert_from_s65", "auto_return_to_map", "bandit_lair", "notification_player_faction_political_issue_resolved", "notification_player_faction_political_issue_resolved_for_player", "start_phase_2_5", "start_phase_3", "start_phase_4",
    "lost_tavern_duel", "establish_court", "notification_relieved_as_marshal", "dplmc_manage_loot_pool", "dplmc_auto_loot", "dplmc_notification_alliance_declared", "dplmc_notification_defensive_declared", "dplmc_notification_trade_declared",
    "dplmc_notification_nonaggression_declared", "dplmc_question_alliance_offer", "dplmc_question_defensive_offer", "dplmc_question_trade_offer", "dplmc_question_nonaggression_offer", "dplmc_notification_alliance_expired", "dplmc_notification_defensive_expired", "dplmc_notification_trade_expired",
    "dplmc_dictate_terms", "dplmc_deny_terms", "dplmc_village_riot_result", "dplmc_village_riot_removed", "dplmc_town_riot_removed", "dplmc_riot_negotiate", "dplmc_notification_riot", "dplmc_notification_appoint_chamberlain",
    "dplmc_chamberlain_confirm", "dplmc_notification_appoint_constable", "dplmc_constable_confirm", "dplmc_notification_appoint_chancellor", "dplmc_chancellor_confirm", "dplmc_deserters", "dplmc_negotiate_besieger", "dplmc_messenger",
    "dplmc_scout", "dplmc_domestic_policy", "dplmc_affiliate_end", "dplmc_preferences", "dplmc_affiliated_family_report", "dplmc_economic_report", "zhaobing",
    "zhaobing2", "zhaobing3", "zhaobing4", "xinzhengfuchengli", "niaoyufujianzhizhan", "dk_invasion_start_warning", "set_invasion", "notification_give_vassal_gift",
    "lco_presentation", "lco_view_character", "lco_auto_return", "upgrade_template", "troops_overview",
    "start_game_1", "start_character_1", "start_character_2", "start_character_3", "start_character_4",
]

game_menus = [_MENU_INDEX[_menu_id] for _menu_id in _MENU_ORDER]

# modmerger_start version=201 type=2
try:
    component_name = "game_menus"
    var_set = { "game_menus" : game_menus }
    from modmerger import modmerge
    modmerge(var_set)
except:
    raise
# modmerger_end
