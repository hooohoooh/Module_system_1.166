# -*- coding: UTF-8 -*-
# split feature file: dialogs - module
from header_common import *
from header_dialogs import *
from header_operations import *
from header_parties import *
from header_item_modifiers import *
from header_skills import *
from header_triggers import *
from ID_troops import *
from ID_party_templates import *
from header_troops import ca_intelligence
from header_terrain_types import *
from header_items import * #For ek_food, and so forth
from module_constants import *

dialogs_trade_tavern = [
[anyone|plyr,"merchant_closing_statement_2",
[],
"That sounds great!", "merchant_closing_statement_3",
[]],
[anyone|plyr,"merchant_closing_statement_2",
[],
"That sounds... Great...", "merchant_closing_statement_3",
[]],
[anyone,"merchant_closing_statement_3",
[
##diplomacy start+ fix pronouns
#gekokujo use town lord rather 
#(faction_get_slot, ":faction_leader", "$g_encountered_party_faction", slot_faction_leader),
#(call_script, "script_dplmc_store_troop_is_female_reg", ":faction_leader", 4),
(party_get_slot, ":local_ruler", "$g_starting_town", slot_town_lord),
(str_store_troop_name, s5, ":local_ruler"),
],
#"my boy" = "my girl", not "my lady"
#change "He" to "{reg4?She:He}" and so forth
"It is. It really truly is. As for me, I will spend my free time in this quiet inn, under the nose of {s5} and {reg4?her:his} so-called loyal vassals.", "merchant_closing_statement_4",
#diplomacy end+
[]],
[anyone,"merchant_closing_statement_4",
[
#diplomacy start+ fix pronouns
(call_script, "script_dplmc_print_cultural_word_to_sreg", "$g_talk_troop", DPLMC_CULTURAL_TERM_WEAPON, 0),
(faction_get_slot, ":faction_leader", "$g_encountered_party_faction", slot_faction_leader),
(call_script, "script_dplmc_store_troop_is_female_reg", ":faction_leader", 4),
],
#change "He" to "{reg4?She:He}" and so forth.  Replace "sell your sword" with "sell your {s0}".
"Anyway, please come visit me here often. If I need you to take part in our eventual uprising against the daimyo, I shall give you the first chance at giving {reg4?her:him} the death blow with your {s0}. If you are curious about our movement, I have prepared some sutras for you to read.", "close_window",
#diplomacy end+
[
(assign, "$g_do_one_more_meeting_with_merchant", 2),
]],
  [anyone,"merchant_pretalk", [], "Anything else?", "merchant_talk",[]],
  [anyone|plyr,"merchant_talk", [(le,"$talk_context", tc_party_encounter),
                                 (check_quest_active, "qst_cause_provocation"),
                                 (neg|check_quest_concluded, "qst_cause_provocation"),
                                 (quest_slot_eq, "qst_cause_provocation", slot_quest_target_faction, "$g_encountered_party_faction"),
                                 (quest_get_slot, ":giver_troop", "qst_cause_provocation", slot_quest_giver_troop),
								 (store_faction_of_troop, ":giver_troop_faction", ":giver_troop"),
                                 (str_store_faction_name, s17, ":giver_troop_faction"),
                                 ],
   "You are trespassing in the territory of the {s17}. I am confiscating this caravan and all its goods!", "caravan_start_war_quest_1",[]],
  [anyone|plyr,"merchant_talk", [(le,"$talk_context", tc_party_encounter),(eq, "$g_encountered_party_faction", "$players_kingdom")], "I have an offer for you.", "merchant_talk_offer",[]],
  [anyone,"merchant_talk_offer", [], "What is it?", "merchant_talk_offer_2",[]],
  [anyone|plyr,"merchant_talk_offer_2", [(eq,"$talk_context", tc_party_encounter),(eq, "$g_encountered_party_faction", "$players_kingdom")],
   "I can escort you to your destination for a price.", "caravan_offer_protection",[]],
##  [anyone|plyr,"merchant_talk_offer_2", [(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 0),
##                                 (neg|faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, "$g_talk_troop"), #he is not a faction leader!
##                                 (call_script, "script_get_number_of_hero_centers", "$g_talk_troop"),
##                                 (eq, reg0, 0), #he has no castles or towns
##                                 (hero_can_join),
##                             ],
##   "I need capable men like you. Will you join me?", "knight_offer_join",[
##       ]],

  [anyone|plyr,"merchant_talk_offer_2", [], "Nothing. Forget it", "merchant_pretalk",[]],
  [anyone|plyr,"merchant_talk", [(check_quest_active, "qst_track_down_bandits"),
  ], "I am hunting a group of bandits with the following description... Have you seen them?", "merchant_bandit_information",[]],
  [anyone,"merchant_bandit_information", [
	(call_script, "script_get_manhunt_information_to_s15", "qst_track_down_bandits"),
  ], "{s15}", "merchant_pretalk",[]],
  [anyone|plyr,"merchant_talk", [(eq,"$talk_context", tc_party_encounter), #TODO: For the moment don't let attacking if merchant has paid toll.
                                 ], "Tell me about your journey", "merchant_trip_explanation",[]],
  [anyone, "merchant_trip_explanation", [
  	  (party_get_slot, ":origin", "$g_encountered_party", slot_party_last_traded_center),
  	  (party_get_slot, ":destination", "$g_encountered_party", slot_party_ai_object),
	  (str_store_party_name, s11, ":origin"),
	  (str_store_party_name, s12, ":destination"),

	  (str_store_string, s14, "str___we_believe_that_there_is_money_to_be_made_selling_"),
      (store_sub, ":item_to_price_slot", slot_town_trade_good_prices_begin, trade_goods_begin),
	  (assign, ":at_least_one_item_found", 0),
	  (try_for_range, ":cur_goods", trade_goods_begin, trade_goods_end),
        (store_add, ":cur_goods_price_slot", ":cur_goods", ":item_to_price_slot"),
		(party_get_slot, ":origin_price", ":origin", ":cur_goods_price_slot"),
		(party_get_slot, ":destination_price", ":destination", ":cur_goods_price_slot"),

		(gt, ":destination_price", ":origin_price"),
		(store_sub, ":price_dif", ":destination_price", ":origin_price"),

		(gt, ":price_dif", 200),
		(str_store_item_name, s15, ":cur_goods"),
		(str_store_string, s14, "str_s14s15_"),

		(assign, ":at_least_one_item_found", 1),
	  (try_end),

	  (try_begin),
		(eq, ":at_least_one_item_found", 0),
	    (str_store_string, s14, "str__we_carry_a_selection_of_goods_although_the_difference_in_prices_for_each_is_not_so_great_we_hope_to_make_a_profit_off_of_the_whole"),
	  (else_try),
		(str_store_string, s14, "str_s14and_other_goods"),

	  (try_end),

  ], "We are coming from {s11} and heading to {s12}.{s14}", "merchant_pretalk", []],
  [anyone|plyr,"merchant_talk", [(eq,"$talk_context", tc_party_encounter), #TODO: For the moment don't let attacking if merchant has paid toll.
                                 (neg|party_slot_ge, "$g_encountered_party", slot_party_last_toll_paid_hours, "$g_current_hours"),
                                 ], "I demand something from you!", "merchant_demand",[]],
  [anyone,"merchant_demand", [(eq,"$talk_context", tc_party_encounter)], "What do you want?", "merchant_demand_2",[]],
  [anyone|plyr,"merchant_demand_2", [(neq,"$g_encountered_party_faction","$players_kingdom")], "There is a toll for free passage here!", "merchant_demand_toll",[]],
  [anyone,"merchant_demand_toll", [(gt, "$g_strength_ratio", 70),
                                        (store_div, reg6, "$g_ally_strength", 2),
                                        (val_add, reg6, 40),
                                        (assign, "$temp", reg6),
                                        ], "Please, I don't want any trouble. I can give you {reg6} mon, just let us go.", "merchant_demand_toll_2",[]],
  [anyone,"merchant_demand_toll", [(store_div, reg6, "$g_ally_strength", 4),
                                        (val_add, reg6, 10),
                                        (assign, "$temp", reg6),
                                        ], "I don't want any trouble. I can give you {reg6} mon if you'll let us go.", "merchant_demand_toll_2",[]],
  [anyone|plyr,"merchant_demand_toll_2", [], "Agreed, hand it over and you may go in peace.", "merchant_demand_toll_accept",[]],
  [anyone,"merchant_demand_toll_accept", [(assign, reg6, "$temp")], "Very well then. Here's {reg6} mon. ", "close_window",
   [(assign, "$g_leave_encounter",1),
    (call_script, "script_troop_add_gold", "trp_player", "$temp"),
    (store_add, ":toll_finish_time", "$g_current_hours", merchant_toll_duration),
    (party_set_slot, "$g_encountered_party", slot_party_last_toll_paid_hours, ":toll_finish_time"),
    (try_begin),
      (ge, "$g_encountered_party_relation", -5),
      (store_relation,":rel", "$g_encountered_party_faction","fac_player_supporters_faction"),
      (try_begin),
        (gt, ":rel", 0),
        (val_sub, ":rel", 1),
      (try_end),
      (val_sub, ":rel", 1),
      (call_script, "script_set_player_relation_with_faction", "$g_encountered_party_faction", ":rel"),
    (try_end),
### Troop commentaries changes begin
    (call_script, "script_add_log_entry", logent_caravan_accosted, "trp_player",  -1, -1, "$g_encountered_party_faction"),
### Troop commentaries changes end
    (assign, reg6, "$temp"),
    ]],
  [anyone|plyr,"merchant_demand_toll_2", [], "I changed my mind, I can't take your money.", "merchant_pretalk",[]],
  [anyone|plyr,"merchant_demand_toll_2", [], "No, I want everything you have! [Attack]", "merchant_attack",[]],
  [anyone|plyr,"merchant_demand_2", [(neq,"$g_encountered_party_faction","$players_kingdom")], "Hand over your gold and valuables now!", "merchant_attack_begin",[]],
  [anyone|plyr,"merchant_demand_2", [], "Nothing. Forget it.", "merchant_pretalk",[]],
  [anyone,"merchant_attack_begin", [], "Are you robbing us?{s11}", "merchant_attack_verify",[
  (str_clear, s11),
  (try_begin),
	(faction_slot_ge, "$g_encountered_party_faction", slot_faction_truce_days_with_factions_begin, 1),
	(str_store_string, s11, "str__have_you_not_signed_a_truce_with_our_lord"),
  (try_end),
  ]],
  [anyone|plyr,"merchant_attack_verify", [], "Robbing you? No, no! It was a joke.", "merchant_attack_verify_norob",[]],
  [anyone,"merchant_attack_verify_norob", [], "God, don't joke about that, {lad/lass}. For a moment I thought we were in real trouble.", "close_window",[(assign, "$g_leave_encounter",1)]],
  [anyone|plyr,"merchant_attack_verify", [], "Of course I'm robbing you. Now hand over your goods.", "merchant_attack",[
	(call_script, "script_diplomacy_party_attacks_neutral", "p_main_party", "$g_encountered_party"),
  ]],
  [anyone,"merchant_attack", [], "Damn you, you won't get anything from us without a fight!", "close_window",
   [(store_relation,":rel", "$g_encountered_party_faction","fac_player_supporters_faction"),
    (try_begin),
      (gt, ":rel", 0),
      (val_sub, ":rel", 10),
    (try_end),
    (val_sub, ":rel", 5),
    (call_script, "script_set_player_relation_with_faction", "$g_encountered_party_faction", ":rel"),
### Troop commentaries changes begin
	(call_script, "script_diplomacy_party_attacks_neutral", "p_main_party", "$g_encountered_party"),
### Troop commentaries changes end
    ]],
  [anyone|plyr,"merchant_talk", [(eq,"$talk_context", tc_party_encounter),(lt, "$g_talk_troop_faction_relation", 0)],
   "Not so fast. First, hand over all your goods and money.", "talk_caravan_enemy_2",[]],
  [anyone|plyr,"merchant_talk", [], "[Leave]", "close_window",[(assign, "$g_leave_encounter",1)]],
  [anyone,"tavernkeeper_pretalk", [], "Anything else?", "tavernkeeper_talk",[]],
  [anyone|plyr,"tavernkeeper_talk", [(check_quest_active,"qst_deliver_wine"),
                                     (quest_slot_eq, "qst_deliver_wine", slot_quest_target_center, "$g_encountered_party"),
                                     (quest_get_slot, ":quest_target_item", "qst_deliver_wine", slot_quest_target_item),
                                     (quest_get_slot, ":quest_target_amount", "qst_deliver_wine", slot_quest_target_amount),
                                     (store_item_kind_count, ":item_count", ":quest_target_item"),
                                     (ge, ":item_count", ":quest_target_amount"),
                                     (assign, reg9, ":quest_target_amount"),
                                     (str_store_item_name, s4, ":quest_target_item"),
                                     ],
   "I was told to deliver you {reg9} units of {s4}.", "tavernkeeper_deliver_wine",[]],
  [anyone,"tavernkeeper_deliver_wine", [],
 "At last! My stock was almost depleted.\
 I had paid the cost of the {s4} in advance.\
 Here, take these {reg5} mon. That should cover your pay.\
 And give {s9} my regards.\
 I'll put in a good word for you next time I deal with him.", "tavernkeeper_pretalk",
   [(quest_get_slot, ":quest_target_item", "qst_deliver_wine", slot_quest_target_item),
    (quest_get_slot, ":quest_target_amount", "qst_deliver_wine", slot_quest_target_amount),
    (quest_get_slot, ":quest_gold_reward", "qst_deliver_wine", slot_quest_gold_reward),
    (quest_get_slot, ":quest_giver_troop", "qst_deliver_wine", slot_quest_giver_troop),
    (troop_remove_items, "trp_player", ":quest_target_item", ":quest_target_amount"),
    (call_script, "script_troop_add_gold", "trp_player", ":quest_gold_reward"),
    (assign, ":xp_reward", ":quest_gold_reward"),
    (val_mul, ":xp_reward", 4),
    (add_xp_as_reward, ":xp_reward"),
    (assign, reg5, ":quest_gold_reward"),
    (str_store_item_name, s4, ":quest_target_item"),
    (str_store_troop_name, s9, ":quest_giver_troop"),

    (quest_get_slot, ":giver_town", "qst_deliver_wine", slot_quest_giver_center),
    (call_script, "script_change_player_relation_with_center", ":giver_town", 2),
    (call_script, "script_change_player_relation_with_center", "$current_town", 1),
    (call_script, "script_end_quest", "qst_deliver_wine"),
    ]],
  [anyone|plyr,"tavernkeeper_talk", [(check_quest_active,"qst_deliver_wine"),
                                     (quest_slot_eq, "qst_deliver_wine", slot_quest_target_center, "$g_encountered_party"),
                                     (quest_get_slot, ":quest_target_item", "qst_deliver_wine", slot_quest_target_item),
                                     (quest_get_slot, ":quest_target_amount", "qst_deliver_wine", slot_quest_target_amount),
                                     (store_item_kind_count, ":item_count", ":quest_target_item"),
                                     (lt, ":item_count", ":quest_target_amount"),
                                     (gt, ":item_count", 0),
                                     (assign, reg9, ":quest_target_amount"),
                                     (str_store_item_name, s4, ":quest_target_item"),
                                     ],
   "I was told to deliver you {reg9} units of {s4}, but I lost some of the cargo on the way.", "tavernkeeper_deliver_wine_incomplete",[]],
  [anyone,"tavernkeeper_deliver_wine_incomplete", [],
 "Attacked by bandits eh?\
 You are lucky they left you alive.\
 Anyway, I can pay you no more than {reg5} mon for this.\
 And I will let {s1} know that my order was delivered less than completely,\
 so you will probably be charged for this loss.", "tavernkeeper_pretalk",
   [(quest_get_slot, ":quest_target_item", "qst_deliver_wine", slot_quest_target_item),
    (quest_get_slot, ":quest_target_amount", "qst_deliver_wine", slot_quest_target_amount),
    (quest_get_slot, ":quest_gold_reward", "qst_deliver_wine", slot_quest_gold_reward),
    (quest_get_slot, ":quest_giver_troop", "qst_deliver_wine", slot_quest_giver_troop),
    (store_item_kind_count, ":item_count", ":quest_target_item"),
    (troop_remove_items, "trp_player", ":quest_target_item", ":item_count"),
    (val_mul, ":quest_gold_reward", ":item_count"),
    (val_div, ":quest_gold_reward", ":quest_target_amount"),
    (call_script, "script_troop_add_gold", "trp_player", ":quest_gold_reward"),
    (assign, reg5, ":quest_gold_reward"),
    (assign, ":xp_reward", ":quest_gold_reward"),
    (val_mul, ":xp_reward", 4),
    (add_xp_as_reward, ":xp_reward"),
    (str_store_troop_name, s1, ":quest_giver_troop"),
    (assign, ":debt", "$qst_deliver_wine_debt"),
    (store_sub, ":item_left", ":quest_target_amount", ":item_count"),
    (val_mul, ":debt", ":item_left"),
    (val_div, ":debt", ":quest_target_amount"),
    (val_add, "$debt_to_merchants_guild", ":debt"),
    (quest_get_slot, ":giver_town", "qst_deliver_wine", slot_quest_giver_center),
    (call_script, "script_change_player_relation_with_center", ":giver_town", 1),
    (call_script, "script_end_quest", "qst_deliver_wine"),
    ]],
  [anyone|plyr,"tavernkeeper_talk", [(check_quest_active,"qst_deliver_wine"),
                                     (quest_slot_eq, "qst_deliver_wine", slot_quest_target_center, "$g_encountered_party"),
                                     (quest_get_slot, ":quest_target_item", "qst_deliver_wine", slot_quest_target_item),
                                     (store_item_kind_count, ":item_count", ":quest_target_item"),
                                     (eq, ":item_count", 0),
                                     (quest_get_slot, reg9, "qst_deliver_wine", slot_quest_target_amount),
                                     (str_store_item_name, s4, ":quest_target_item"),
                                     ],
   "I was told to deliver you {reg9} units of {s4}, but I lost the cargo on the way.", "tavernkeeper_deliver_wine_lost",[]],
  [anyone,"tavernkeeper_deliver_wine_lost", [],
 "What? I was waiting for that {s4} for weeks!\
 And now you are telling me that you lost it?\
 You may rest assured that I will let {s1} know about this.", "tavernkeeper_pretalk",
   [(add_xp_as_reward, 40),
    (quest_get_slot, ":quest_target_item", "qst_deliver_wine", slot_quest_target_item),
    (quest_get_slot, ":quest_giver_troop", "qst_deliver_wine", slot_quest_giver_troop),
    (str_store_item_name, s4, ":quest_target_item"),
    (str_store_troop_name, s1, ":quest_giver_troop"),
    (val_add, "$debt_to_merchants_guild", "$qst_deliver_wine_debt"),
    (call_script, "script_end_quest", "qst_deliver_wine"),
   ]],
##  [anyone|plyr,"tavernkeeper_talk", [], "I need to hire some soldiers. Can you help me?", "tavernkeeper_buy_peasants",[]],
##  [anyone,"tavernkeeper_buy_peasants",
##   [
##       (store_encountered_party,reg(3)),
##       (store_faction_of_party,reg(4),reg(3)),
##       (store_relation,reg(5),"fac_player_supporters_faction",reg(4)),
##       (lt, reg(5), -3),
##    ], "I don't think anyone from this town will follow somebody like you. Try your luck elsewhere.", "tavernkeeper_buy_peasants_2",[]],
##  [anyone,"tavernkeeper_buy_peasants", [], "I know a few fellows who would follow you if you paid for their equipment.", "tavernkeeper_buy_peasants_2",[(set_mercenary_source_party,"$tavernkeeper_party"),[change_screen_buy_mercenaries]]],
##  [anyone,"tavernkeeper_buy_peasants_2", [], "Anything else?", "tavernkeeper_talk",[]],
##
##  [anyone|plyr,"tavernkeeper_talk", [], "I want to rest for a while.", "tavernkeeper_rest",[]],
###  [anyone,"tavernkeeper_rest", [], "Of course... How long do you want to rest?", "tavernkeeper_rest_2",[]],
##  [anyone,"tavernkeeper_rest",
##   [
##       (store_encountered_party,reg(3)),
##       (store_faction_of_party,reg(4),reg(3)),
##       (store_relation,reg(5),"fac_player_supporters_faction",reg(4)),
##       (lt, reg(5), -3),
##      ], "You look like trouble stranger. I can't allow you to stay for the night. No.", "close_window",
##   []],
##  [anyone,"tavernkeeper_rest", [], "Of course... That will be {reg3} mon for the room and food. How long do you want to rest?", "tavernkeeper_rest_2",
##   [(store_party_size,reg(3)),
##    (val_add,reg(3),1),
##    (val_div,reg(3),3),
##    (val_max,reg(3),1),
##    (assign,"$tavern_rest_cost",reg(3))]],
##  [anyone|plyr,"tavernkeeper_rest_2", [(store_time_of_day,reg(1)),
##                                       (val_add,reg(1),7),
##                                       (val_mod,reg(1),24),
##                                       (lt,reg(1),12),
##                                       (store_troop_gold,reg(8),"trp_player"),
##                                       (ge,reg(8),"$tavern_rest_cost"),
##                                       ],
##   "I want to rest until morning.", "close_window",
##   [(assign, reg(2), 13),(val_sub,reg(2),reg(1)),(assign, "$g_town_visit_after_rest", 1),(rest_for_hours, reg(2)),(troop_remove_gold, "trp_player","$tavern_rest_cost"),(call_script, "script_change_player_party_morale", 2)]],
##  [anyone|plyr,"tavernkeeper_rest_2", [(store_time_of_day,reg(1)),
##                                       (val_add,reg(1),7),
##                                       (val_mod,reg(1),24),
##                                       (ge,reg(1),12),
##                                       (store_troop_gold,reg(8),"trp_player"),
##                                       (ge,reg(8),"$tavern_rest_cost"),
##                                       ],
##   "I want to rest until evening.", "close_window",
##   [(assign, reg(2), 28),(val_sub,reg(2),reg(1)),(assign, "$g_town_visit_after_rest", 1),(rest_for_hours, reg(2)),(troop_remove_gold, "trp_player","$tavern_rest_cost"),(call_script, "script_change_player_party_morale", 2)]],
##  [anyone|plyr,"tavernkeeper_rest_2", [], "Forget it.", "close_window",[]],

  [anyone|plyr,"tavernkeeper_talk", [
      (store_current_hours,":cur_hours"),
      (val_sub, ":cur_hours", 24),
      (gt, ":cur_hours", "$buy_drinks_last_time"),
	  ##diplomacy start+ Replace with cultural equivalent
	  ##OLD:
      #], "I'd like to buy every man who comes in here tonight a jar of your best wine.", "tavernkeeper_buy_drinks",[]],
	  ##NEW:
	  (call_script, "script_dplmc_print_cultural_word_to_sreg", "$g_talk_troop", DPLMC_CULTURAL_TERM_TAVERNWINE, 0),
	  ], "I'd like to buy every man who comes in here tonight a jar of your best {s0}.", "tavernkeeper_buy_drinks",[]],
	  ##diplomacy end+

  [anyone,"tavernkeeper_buy_drinks",
   [
    ], "Of course, {my lord/my lady}. I reckon {reg5} mon should be enough for that. What should I tell everyone?", "tavernkeeper_buy_drinks_2",[
        (assign, "$temp", 1000),
        (assign, reg5, "$temp"),
        ]],
  [anyone|plyr,"tavernkeeper_buy_drinks_2",
   [
        (store_troop_gold, ":gold", "trp_player"),
        (ge, ":gold", "$temp"),
        (str_store_party_name, s10, "$current_town"),
    ], "Let everyone know of the generosity of {playername} to the people of {s10}.", "tavernkeeper_buy_drinks_end",[

        ]],
  [anyone,"tavernkeeper_buy_drinks_end",
  ##diplomacy start+ Replace {sir/madam} with {s0}
   #[], "Don't worry {sir/madam}. Your name will be cheered and toasted here all night.", "tavernkeeper_pretalk",
   [(call_script, "script_dplmc_print_commoner_at_arg1_says_sir_madame_to_s0", "$current_town"),
   ], "Don't worry {s0}. Your name will be cheered and toasted here all night.", "tavernkeeper_pretalk",
   ##diplomacy end+
   [
       (troop_remove_gold, "trp_player", "$temp"),
       (call_script, "script_change_player_relation_with_center", "$current_town", 1),
       (store_current_hours,":cur_hours"),
       (assign, "$buy_drinks_last_time", ":cur_hours"),
       ]],
  [anyone|plyr,"tavernkeeper_buy_drinks_2", [], "Actually, cancel that order.", "tavernkeeper_pretalk",[]],
  [anyone|plyr,"tavernkeeper_talk", [
  (neq, "$g_encountered_party_faction", "fac_player_supporters_faction"),
  ],
   "Have you heard of anyone in this domain who might have a job for a {man/woman} like myself?", "tavernkeeper_job_ask",[
   ]],
  [anyone,"tavernkeeper_job_ask",
   [
	(str_store_string, s9, "str__of_course_the_land_is_currently_at_peace_so_you_may_have_better_luck_in_other_realms"),
	(try_for_range, ":faction", kingdoms_begin, kingdoms_end),
		(store_relation, ":relation", "$g_encountered_party_faction", ":faction"),
		(lt, ":relation", 0),
		(str_clear, s9),
	(try_end),
	(faction_get_slot, ":leader",  "$g_encountered_party_faction", slot_faction_leader),
	(str_store_troop_name, s10, ":leader"),
	##diplomacy start+ Fix pronoun "his" -> {reg0?her:his}
	(call_script, "script_dplmc_store_troop_is_female", ":leader"),
   ], "Hmm... Well, {s10} is often looking for mercenaries to fight in {reg0?her:his} wars.{s9}", "tavernkeeper_job_search",
   ##diplomacy end+
    [
   (assign, "$g_troop_list_no", 0),
    ]],
  [anyone, "tavernkeeper_job_search",
  [],
  "Let me think some more...", "tavernkeeper_job_result",
  [
    (call_script, "script_npc_find_quest_for_player_to_s11", "$g_encountered_party_faction"),
	(assign, ":quest_giver", reg0),

	(call_script, "script_get_dynamic_quest", ":quest_giver"),
	(assign, ":quest_type", reg0),

	(try_begin),
		(gt, ":quest_giver", -1),
		(str_store_troop_name, s7, ":quest_giver"),
		(str_clear, s9), #location string

		(assign, ":location", -1),
		(try_begin),
			(troop_slot_eq, ":quest_giver", slot_troop_occupation, slto_kingdom_hero),
			(troop_get_slot, ":quest_giver_party", ":quest_giver", slot_troop_leaded_party),
			(party_is_active, ":quest_giver_party"),
			(party_get_attached_to, ":location", ":quest_giver_party"),
		(else_try),
			(is_between, ":quest_giver", mayors_begin, mayors_end),
			(try_for_range, ":town", towns_begin, towns_end),
				(party_slot_eq, ":town", slot_town_elder, ":quest_giver"),
				(assign, ":location", ":town"),
			(try_end),
		(try_end),

		(try_begin),
			(gt, ":location", -1),
			(try_begin),
				(eq, ":location", "$g_encountered_party"),
				(str_store_string, s8, "str_here"),
			(else_try),
				(str_store_string, s8, "str_over"),
			(try_end),
			(str_store_party_name, s12, ":location"),
			(str_store_string, s9, "str_s8_in_s12"),
		(try_end),

		##diplomacy start+ Do this first
		(call_script, "script_dplmc_store_troop_is_female_reg", ":quest_giver", 4),
		##diplomacy end+
		(try_begin),
			(eq, ":quest_type", "qst_track_down_bandits"),
			(str_store_string, s10, "str__has_put_together_a_bounty_on_some_bandits_who_have_been_attacking_travellers_in_the_area"),
		(else_try),
			(eq, ":quest_type", "qst_destroy_bandit_lair"),
			(str_store_string, s10, "str__has_been_worried_about_bandits_establishing_a_hideout_near_his_home"),
		(else_try),
			(eq, ":quest_type", "qst_retaliate_for_border_incident"),
			(str_store_string, s10, "str__is_looking_for_a_way_to_avoid_an_impending_war"),
		(else_try),
			(eq, ":quest_type", "qst_rescue_prisoner"),
			(str_store_string, s10, "str__may_need_help_rescuing_an_imprisoned_family_member"),
		(else_try),
			(eq, ":quest_type", "qst_cause_provocation"),
			(str_store_string, s10, "str__has_been_asking_around_for_someone_who_might_want_work_id_watch_yourself_with_him_though"),
		(else_try),
			(str_store_string, s10, "str_tavernkeeper_invalid_quest"),
		(try_end),

		##diplomacy start+
		#(troop_get_type, reg4, ":quest_giver"),
		(call_script, "script_dplmc_store_troop_is_female_reg", ":quest_giver", 4),
		##diplomacy end+
	(try_end),

  ]],
  [anyone, "tavernkeeper_job_result", [
  	(store_sub, ":last_troop", mayors_end, 1),
	(lt, "$g_troop_list_no", ":last_troop"),
  ], "I have heard that {s7} {s9}{s10} You may want to speak with {reg4?her:him}.", "tavernkeeper_job_search",
   [
       ]],
  [anyone, "tavernkeeper_job_result", [
  (store_sub, ":last_troop", mayors_end, 1),
  (ge, "$g_troop_list_no", ":last_troop"),
  ], "There may be other work, of course -- lords and merchants often have other tasks which we don't hear about. Also, the villages around here frequently need help, although they'd be more likely to pay you with a wedge of cheese and goodwill than with cold hard mon.", "tavernkeeper_job_result_2",
   [
       ]],
  [anyone,"tavernkeeper_job_result_2", [], "I'll keep my ears open for other opportunities. You may want to ask again from time to time.", "close_window",[]],
  [anyone|plyr,"tavernkeeper_talk", [], "I guess I should leave now.", "close_window",[]],
  [anyone,"ransom_broker_pretalk", [],
   "Anyway, if you have any prisoners, I will be happy to buy them from you.", "ransom_broker_talk",[]],
  [anyone|plyr,"ransom_broker_talk",
   [[store_num_regular_prisoners,reg(0)],[ge,reg(0),1]],
   "Then you'd better bring your purse. I have got prisoners to sell.", "ransom_broker_sell_prisoners",[]],
  ##diplomacy start+
  [anyone|plyr,"ransom_broker_talk",
   [(store_num_regular_prisoners,reg0),(ge,reg0,1)],
   "I want to sell all the prisoners I have with me.", "ransom_broker_sell_prisoners_all",[]],
  [anyone,"ransom_broker_sell_prisoners_all", [
  (call_script, "script_dplmc_sell_all_prisoners", 0, 0),#do not actually sell
  (store_num_regular_prisoners, reg2),
  (val_sub, reg2, 1),
  ],
  "Let's see...  I'll give you {reg0} mon for your {reg1} {reg2?prisoners:prisoner}.  Do we have a deal?", "ransom_broker_sell_prisoners_all_2", []],
  [anyone|plyr,"ransom_broker_sell_prisoners_all_2", [],
   "We have a deal.", "ransom_broker_sell_prisoners_2", [(call_script, "script_dplmc_sell_all_prisoners", 1, 0),]
  ],
  [anyone|plyr,"ransom_broker_sell_prisoners_all_2", [],
   "Let me think about it again.", "ransom_broker_pretalk",[]],
  ##diplomacy end+
  #gekokujo no more intro, will rewrite later
  #[anyone|plyr,"ransom_broker_talk", [], "Tell me about what you do again.", "ransom_broker_intro_2",[]],


  [anyone|plyr,"ransom_broker_talk",[
  ], "I wish to ransom one of my companions.", "ransom_broker_ransom_companion",[]],
  [anyone,"ransom_broker_ransom_companion",[], "Whom do you wish to ransom?", "ransom_broker_ransom_companion_choose",[]],
  [anyone|plyr|repeat_for_troops,"ransom_broker_ransom_companion_choose",[
  (store_repeat_object, ":imprisoned_companion"),
  (neg|troop_slot_eq, ":imprisoned_companion", slot_troop_occupation, slto_kingdom_hero),
  #gekokujo 3.0 microfactions! include fort companions start
  #(is_between, ":imprisoned_companion", companions_begin, companions_end),
  (is_between, ":imprisoned_companion", companions_begin, fort_companions_end),
  #gekokujo 3.0 microfactions! include fort companions end
  (troop_slot_ge, ":imprisoned_companion", slot_troop_prisoner_of_party, centers_begin),
  (str_store_troop_name, s4, ":imprisoned_companion"),
  ], "{s4}", "ransom_broker_ransom_companion_name_sum",[

  (store_repeat_object, "$companion_to_be_ransomed"),
  ]],
  [anyone|plyr,"ransom_broker_ransom_companion_choose",[
  ], "Never mind", "ransom_broker_pretalk",[]],
  [anyone,"ransom_broker_ransom_companion_name_sum",[], "Let me check my ledger, here... Yes. Your friend is being held in the dungeon at {s7}. How interesting! I remember hearing that the rats down there are unusually large -- like mastiffs, they say... Now... For the very reasonable sum of {reg5} mon, which includes both the ransom and my commission and expenses, we can arrange it so that {s5} can once again enjoy {reg4?her:his} freedom. What do you say?", "ransom_broker_ransom_companion_verify",[
  (str_store_troop_name, s5, "$companion_to_be_ransomed"),
  ##diplomacy start+
  #(troop_get_type, reg4, "$companion_to_be_ransomed"),
  (call_script, "script_dplmc_store_troop_is_female_reg", "$companion_to_be_ransomed", 4),
  ##diplomacy end+

  (troop_get_slot, ":prison_location", "$companion_to_be_ransomed", slot_troop_prisoner_of_party),
  (str_store_party_name, s7, ":prison_location"),

  (store_character_level, ":companion_level", "$companion_to_be_ransomed"),
  (store_add, "$companion_ransom_amount", ":companion_level", 20),
  (val_mul, "$companion_ransom_amount", ":companion_level"),
  (val_mul, "$companion_ransom_amount", 5), #Level 1: 110, level 40: 12,000
  (assign, reg5, "$companion_ransom_amount"),
  ]],
  [anyone|plyr,"ransom_broker_ransom_companion_verify",[
  (store_troop_gold, ":player_gold", "trp_player"),
  (ge, ":player_gold", "$companion_ransom_amount"),

  ], "Here's your money.", "ransom_broker_ransom_companion_accept",[
  (troop_remove_gold, "trp_player", "$companion_ransom_amount"),




  (troop_set_slot, "$companion_to_be_ransomed", slot_troop_occupation, slto_player_companion),
  (troop_set_slot, "$companion_to_be_ransomed", slot_troop_current_mission, npc_mission_rejoin_when_possible),
  (troop_set_slot, "$companion_to_be_ransomed", slot_troop_days_on_mission, 1),

  (try_begin),
	(troop_get_slot, ":held_at_prison", "$companion_to_be_ransomed", slot_troop_prisoner_of_party),
	##diplomacy start+ give ransom to one who was imprisoning the companion
	(try_begin),
		(is_between, ":held_at_prison", centers_begin, centers_end),
		(party_get_slot, ":town_lord", ":held_at_prison", slot_town_lord),
		(is_between, ":town_lord", heroes_begin, heroes_end),
		(call_script, "script_dplmc_distribute_gold_to_lord_and_holdings", "$companion_ransom_amount", ":town_lord"),
	(else_try),
	    #if the center has no lord, split it among the faction
		(store_faction_of_party, ":prison_faction", ":held_at_prison"),
		(call_script, "script_dplmc_faction_leader_splits_gold", ":prison_faction", "$companion_ransom_amount"),
	(try_end),
	##diplomacy end+
	(party_count_prisoners_of_type, ":holding_as_prisoner",  ":held_at_prison", "$companion_to_be_ransomed"),
	(gt, ":holding_as_prisoner", 0),
	(party_remove_prisoners, ":held_at_prison", "$companion_to_be_ransomed", 1),
  (try_end),
  (troop_set_slot, "$companion_to_be_ransomed", slot_troop_prisoner_of_party, -1),

  (troop_set_slot, "$companion_to_be_ransomed", slot_troop_personalityclash_penalties, 0),
  (troop_set_slot, "$companion_to_be_ransomed", slot_troop_morality_penalties, 0),

  ]],
  [anyone|plyr,"ransom_broker_ransom_companion_verify",[
  ], "I can't afford that right now.", "ransom_broker_ransom_companion_refuse",[]],
  [anyone,"ransom_broker_ransom_companion_accept",[], "Splendid! In a few days, I would think, you should find {s5} riding to rejoin you, blinking in the sunlight and no doubt very grateful! Is there any other way in which I can help you?", "ransom_broker_talk",[
  (str_store_troop_name, s5, "$companion_to_be_ransomed"),

  ]],
  [anyone,"ransom_broker_ransom_companion_refuse",[], "Of course, of course... Never mind what they say about the rats, by the way -- I've never actually seen one myself, on account of the pitch-black darkness. Anyway, I'm sure that {s5} will understand why it's important for you to control expenditures. Now... Was there anything else?", "ransom_broker_talk",[
  (str_store_troop_name, s5, "$companion_to_be_ransomed"),
  ]],
  [anyone|plyr,"ransom_broker_talk",[], "Not this time. Good-bye.", "close_window",[]],
  [anyone,"ransom_broker_sell_prisoners", [],
  "Let me see what you have...", "ransom_broker_sell_prisoners_2",
   [[change_screen_trade_prisoners]]],
#  [anyone, "ransom_broker_sell_prisoners_2", [], "You take more prisoners, bring them to me. I will pay well.", "close_window",[]],
  [anyone, "ransom_broker_sell_prisoners_2", [], "I will be staying here for a few days. Let me know if you need my services.", "close_window",[]],
  [anyone|plyr, "tavern_traveler_lost_companion_thanks", [(troop_get_type, reg3, "$last_lost_companion")], "Thanks. I'll go and find {reg3?her:him} there.", "tavern_traveler_pretalk", []],
  [anyone|plyr, "tavern_traveler_lost_companion_thanks", [], "Thanks, but I don't really care.", "tavern_traveler_pretalk", []],
  [anyone, "tavern_traveler_pretalk", [], "Yes?", "tavern_traveler_talk", []],
  [anyone|plyr, "tavern_traveler_talk", [(eq, "$traveler_land_asked", 0)], "What can you tell me about this land?", "tavern_traveler_tell_kingdoms", [(assign, "$traveler_land_asked", 1)]],
  [anyone, "tavern_traveler_tell_kingdoms", [], "Japan is divided into rival domains, which can neither manage to live in peace with their neighbours,\
 nor completely eliminate them.\
 As a result, there's seldom a break to the bitter wars which plague this land and drain its life blood.\
 Well, at least this must be a good place to be for an adventurer such as yourself.\
 With some luck and skill, you can make a name for yourself here, amass a fortune perhaps, or gain great power.\
 Opportunities are endless and so are the rewards, if you are willing to risk your life for them.", "tavern_traveler_tell_kingdoms_2", []],
  [anyone|plyr, "tavern_traveler_tell_kingdoms_2", [], "Tell me more about these opportunities.", "tavern_traveler_tell_kingdoms_3", []],
  [anyone|plyr, "tavern_traveler_tell_kingdoms_2", [], "Thank you. That was all I needed to know", "close_window", []],
  [anyone, "tavern_traveler_tell_kingdoms_3", [(gt, "$player_has_homage", 0)], "Well, you probably know everything I could tell you already. You seem to be doing pretty well.",
   "tavern_traveler_tell_kingdoms_4", []],
  [anyone, "tavern_traveler_tell_kingdoms_3", [], "The kingdoms will pay good money for mercenaries if they are engaged in a war.\
 If you have done a bit of fighting, speaking with one of their lords will probably result in being offered a ronin job.\
 However the real rewards come if you can manage to become a vassal to a daimyo.\
 A vassal can own villages, castles and towns and get rich with the taxes and revenues of these estates.\
 Normally, only hereditary vassals of the clan own land in this way,\
 but in time of war, a daimyo will not hesitate to accept someone who distinguishes {himself/herself} on the battlefield as a vassal, and grant {him/her} the right to own land.",
   "tavern_traveler_tell_kingdoms_4a", []],
  [anyone, "tavern_traveler_tell_kingdoms_4a", [], "It is not unheard-of for adventurers to renounce allegiance to a Japanese daimyo altogether, declare themselves lords, and claim land in their own name. This is a difficult path, however, as the great nobles of the land, with their long ancestries, are not likely to accept such upstarts as their monarch. Such rulers would need to be very careful in establishing their right to rule, or they would be set upon from all sides.",
   "tavern_traveler_tell_kingdoms_4", []],
  [anyone, "tavern_traveler_tell_kingdoms_4", [], "It might be easier for an adventurer like yourself to pledge support to an existing daimyo's rival.\
  There are many such pretenders in Japan -- those who are born to the right family, who go around and stir up trouble saying they have a better claim to the lordship than the current ruler.\
 If those claim holders could find supporters, they could easily start civil wars and perhaps even replace the ruler one day.",
   "tavern_traveler_tell_kingdoms_5", []],
  [anyone|plyr, "tavern_traveler_tell_kingdoms_5", [], "Interesting. Where can I find these claim holders?", "tavern_traveler_tell_kingdoms_6", []],
  [anyone|plyr, "tavern_traveler_tell_kingdoms_5", [], "I guess I heard enough already. Thank you.", "close_window", []],
  [anyone, "tavern_traveler_tell_kingdoms_6", [], "A claim holder's life would be in danger in his own country of course.\
 Therefore, they usually stay at rival courts, raising support and hoping to find someone willing to champion their cause.\
 I usually hear news about some of them, and may be able to tell you their location with some precision.\
 But of course, I would ask for a little something for such a service.",
   "tavern_traveler_pretalk", [(assign, "$traveller_claimants_mentioned", 1)]],
  [anyone|plyr, "tavern_traveler_talk", [(eq, "$traveller_claimants_mentioned", 1)], "I want to know the location of a claimant.", "tavern_traveler_pretender_location", []],
  [anyone, "tavern_traveler_pretender_location", [], "Whose location do you want to know?", "tavern_traveler_pretender_location_ask", []],
  [anyone|plyr|repeat_for_troops, "tavern_traveler_pretender_location_ask",
   [
     (store_repeat_object, ":troop_no"),
     (is_between, ":troop_no", pretenders_begin, pretenders_end),
     (neg|troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
     (troop_slot_ge, ":troop_no", slot_troop_cur_center, 1),
     (str_store_troop_name, s11, ":troop_no"),
     (neq, ":troop_no", "$supported_pretender"),
     ],  "{s11}", "tavern_traveler_pretender_location_ask_2",
   [
     (store_repeat_object, "$temp"),
     ]],
  [anyone|plyr, "tavern_traveler_pretender_location_ask",
   [],  "Never mind.", "tavern_traveler_pretalk", []],
  [anyone, "tavern_traveler_pretender_location_ask_2", [], "I can reveal this information to you for a small price, let's say 30 mon.", "tavern_traveler_pretender_location_ask_money", []],
  [anyone|plyr, "tavern_traveler_pretender_location_ask_money",
   [
     (store_troop_gold, ":cur_gold", "trp_player"),
     (ge, ":cur_gold", 30),
   ],
   "All right. Here is 30 mon.", "tavern_traveler_pretender_location_tell",
   [
     (troop_remove_gold, "trp_player", 30),
   ]],
  [anyone|plyr, "tavern_traveler_pretender_location_ask_money", [], "Never mind.", "tavern_traveler_pretalk", []],
  [anyone, "tavern_traveler_pretender_location_tell", [], "{s15} is currently at {s11}.", "tavern_traveler_pretalk",
   [
     (str_store_troop_name, s15, "$temp"),
     (troop_get_slot, ":cur_center", "$temp", slot_troop_cur_center),
     (str_store_party_name, s11, ":cur_center"),
   ]],
  ##diplomacy start+
  #The tavern travellers can give the locations of than just pretenders and
  #the player's former travelling companions.  I've decided to add book sellers
  #and ransom brokers, but not lords.
  #Another alteration is that only booksellers / ransom brokers the player has
  #met can be located.
  #Code credit to rubik's Custom Commander
  # CC
  [anyone|plyr, "tavern_traveler_talk", [], "I am looking for book merchants...", "tavern_traveler_bookseller_location", []],
  [anyone, "tavern_traveler_bookseller_location",
    [
      (assign, ":num_towns", 0),
      (try_for_range, ":town_no", towns_begin, towns_end),
        (neg|party_slot_eq, ":town_no", slot_center_tavern_bookseller, 0),
        (party_get_slot, ":seller", ":town_no", slot_center_tavern_bookseller),#addition - fixed 2011-03-29
        (troop_slot_ge, ":seller", slot_troop_met, 1),#addition # removed 2011-03-29
        (val_add, ":num_towns", 1),
      (try_end),
      (eq, ":num_towns", 0),
    ], "I am sorry I haven't run across any lately.", "tavern_traveler_pretalk", []],
  [anyone, "tavern_traveler_bookseller_location", [], "I might have crossed paths with one or two recently. For 100 mon, I'll tell you where.", "tavern_traveler_bookseller_location_ask_money", []],
  [anyone|plyr, "tavern_traveler_bookseller_location_ask_money",
   [
     (store_troop_gold, ":cur_gold", "trp_player"),
     (ge, ":cur_gold", 100),
     ], "All right. Here is 100 mon.", "tavern_traveler_bookseller_location_tell",
   [
     (troop_remove_gold, "trp_player", 100),
     ]],
  [anyone|plyr, "tavern_traveler_bookseller_location_ask_money", [], "Never mind.", "tavern_traveler_pretalk", []],
  [anyone, "tavern_traveler_bookseller_location_tell", [], "You can find them at {s11}.", "tavern_traveler_pretalk",
   [
      (assign, ":num_towns", 0),
      (try_for_range, ":town_no", towns_begin, towns_end),
        (neg|party_slot_eq, ":town_no", slot_center_tavern_bookseller, 0),
        (party_get_slot, ":seller", ":town_no", slot_center_tavern_bookseller),#addition - fixed 2011-03-29
        (troop_slot_ge, ":seller", slot_troop_met, 1),#addition
        (val_add, ":num_towns", 1),
        (try_begin),
          (eq, ":num_towns", 1),
          (str_store_party_name, s11, ":town_no"),
        (else_try),
          (eq, ":num_towns", 2),
          (str_store_party_name, s12, ":town_no"),
          (str_store_string, s11, "@{s12} and {s11}"),
        (try_end),
      (try_end),
      (display_message, "@You can find book merchants at {s11}."),
     ]],
  [anyone|plyr, "tavern_traveler_talk", [], "I am looking for ransom brokers...", "tavern_traveler_ransom_broker_location", []],
  [anyone, "tavern_traveler_ransom_broker_location",
    [
      (assign, ":num_towns", 0),
      (try_for_range, ":town_no", towns_begin, towns_end),
        (neq, ":town_no", "p_town_2"),
        (neg|party_slot_eq, ":town_no", slot_center_ransom_broker, 0),
        (party_get_slot, ":broker", ":town_no", slot_center_ransom_broker),#addition - fixed 2011-03-29
        (troop_slot_ge, ":broker", slot_troop_met, 1),#addition
        (val_add, ":num_towns", 1),
      (try_end),
      (eq, ":num_towns", 0),
    ], "I am sorry I haven't run across any lately.", "tavern_traveler_pretalk", []],
  [anyone, "tavern_traveler_ransom_broker_location", [], "I know where they are. For 50 mon, I'll tell you.", "tavern_traveler_ransom_broker_location_ask_money", []],
  [anyone|plyr, "tavern_traveler_ransom_broker_location_ask_money",
   [
     (store_troop_gold, ":cur_gold", "trp_player"),
     (ge, ":cur_gold", 50),
     ], "All right. Here is 50 mon.", "tavern_traveler_ransom_broker_location_tell",
   [
     (troop_remove_gold, "trp_player", 50),
     ]],
  [anyone|plyr, "tavern_traveler_ransom_broker_location_ask_money", [], "Never mind.", "tavern_traveler_pretalk", []],
  [anyone, "tavern_traveler_ransom_broker_location_tell", [], "You can find them at {s11}.", "tavern_traveler_pretalk",
   [
      (assign, ":num_towns", 0),
      (try_for_range, ":town_no", towns_begin, towns_end),
        (neq, ":town_no", "p_town_2"),
        (neg|party_slot_eq, ":town_no", slot_center_ransom_broker, 0),
        (party_get_slot, ":broker", ":town_no", slot_center_ransom_broker),#addition - fixed 2011-03-29
        (troop_slot_ge, ":broker", slot_troop_met, 1),#addition # removed 2011-03-29
        (val_add, ":num_towns", 1),
        (try_begin),
          (eq, ":num_towns", 1),
          (str_store_party_name, s11, ":town_no"),
        (else_try),
          (str_store_party_name, s12, ":town_no"),
          (eq, ":num_towns", 2),
          (str_store_string, s11, "@{s12} and {s11}"),
        (else_try),
          (str_store_string, s11, "@{s12}, {s11}"),
        (try_end),
      (try_end),
      (display_message, "@You can find ransom brokers at {s11}."),
     ]],
  # CC
  ##diplomacy end+

##diplomacy start+
#Allow another method of revtrieving dismissed employees
    [anyone|plyr, "tavern_traveler_talk", [
#Verify that the player in fact has dismissed employees, who are not
#already on their way back.  Also verify that the player is capable
#of taking them back.
(assign, ":player_village", villages_end),
(assign, ":player_castle", castles_end),
(assign, ":player_town", towns_end),
(try_for_range, ":center_no", villages_begin, ":player_village"),
    (party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
    (assign, ":player_village", ":center_no"),#assign and break loop
(try_end),
(try_for_range, ":center_no", castles_begin, ":player_castle"),
    (party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
    (assign, ":player_castle", ":center_no"),#assign and break loop
(try_end),
(try_for_range, ":center_no", towns_begin, ":player_town"),
    (party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
    (assign, ":player_town", ":center_no"),#assign and break loop
(try_end),

(assign, ":exist_contactable_employees", 0),
(try_begin),
#Chamberlain?
(eq, "$g_player_chamberlain", -1),
(neg|troop_slot_eq, "trp_dplmc_chamberlain", slot_troop_met, 0),
(this_or_next|is_between, ":player_village", villages_begin, villages_end),
(this_or_next|is_between, ":player_castle", castles_begin, castles_end),
   (is_between, ":player_town", towns_begin, towns_end),
(assign, ":exist_contactable_employees", 1),
(else_try),
#Constable?
(eq, "$g_player_constable", -1),
(neg|troop_slot_eq, "trp_dplmc_constable", slot_troop_met, 0),
(this_or_next|is_between, ":player_castle", castles_begin, castles_end),
   (is_between, ":player_town", towns_begin, towns_end),
(assign, ":exist_contactable_employees", 1),
(else_try),
#Chancellor?
(eq, "$g_player_chancellor", -1),
(neg|troop_slot_eq, "trp_dplmc_chancellor", slot_troop_met, 0),
(is_between, ":player_town", towns_begin, towns_end),
(assign, ":exist_contactable_employees", 1),
(try_end),

(neq, ":exist_contactable_employees", 0),

], "I am looking for one of my former employees...", "dplmc_tavern_traveler_employee_1", []],
##diplomacy end+

  [anyone|plyr, "tavern_traveler_talk", [], "I am looking for one of my companions...", "tavern_traveler_companion_location", []],
  [anyone, "tavern_traveler_companion_location", [], "Maybe I can help you. Who are you looking for?", "tavern_traveler_companion_location_ask", []],
  [anyone|plyr|repeat_for_troops, "tavern_traveler_companion_location_ask",
   [
     (store_repeat_object, ":troop_no"),
     (is_between, ":troop_no", companions_begin, companions_end),

     (troop_slot_ge, ":troop_no", slot_troop_playerparty_history, 1),
##diplomacy start+ Verify that the troops are actually former companions.
     (neg|troop_slot_eq, ":troop_no", slot_troop_playerparty_history, dplmc_pp_history_nonplayer_entry),
	 (neg|troop_slot_eq, ":troop_no", slot_troop_met, 0),
##diplomacy end+

     (assign, ":continue", 0),
     (try_begin),
       (this_or_next|troop_slot_ge, ":troop_no", slot_troop_cur_center, 1),
       (troop_slot_ge, ":troop_no", slot_troop_prisoner_of_party, 0),

       (assign, ":continue", 1),
     (try_end),

     (eq, ":continue", 1),

     (str_store_troop_name, s11, ":troop_no"),
   ],
   "{s11}", "tavern_traveler_companion_location_ask_2",
   [
     (store_repeat_object, "$temp"),
   ]],
  [anyone|plyr, "tavern_traveler_companion_location_ask",
   [],  "Never mind.", "tavern_traveler_pretalk", []],
  [anyone, "tavern_traveler_companion_location_ask_2", [(str_store_troop_name, s15, "$temp")], "I guess I know where {s15} is. For 30 mon, I'll tell you.", "tavern_traveler_companion_location_ask_money", []],
  [anyone|plyr, "tavern_traveler_companion_location_ask_money",
   [
     (store_troop_gold, ":cur_gold", "trp_player"),
     (ge, ":cur_gold", 30),
     ], "All right. Here is 30 mon.", "tavern_traveler_companion_location_tell",
   [
     (troop_remove_gold, "trp_player", 30),
     ]],
  [anyone|plyr, "tavern_traveler_companion_location_ask_money", [], "Never mind.", "tavern_traveler_pretalk", []],
  [anyone, "tavern_traveler_companion_location_tell", [], "{s15} is currently at {s11}.{s12}", "tavern_traveler_pretalk",
   [
     (str_store_troop_name, s15, "$temp"),

     (try_begin),
       (troop_slot_ge, "$temp", slot_troop_cur_center, 1),
       (troop_get_slot, ":cur_center", "$temp", slot_troop_cur_center),
       (str_store_string, s12, "str_space"),
     (else_try),
       (troop_get_slot, ":cur_center", "$temp", slot_troop_prisoner_of_party),

       (try_begin),
         (is_between, ":cur_center", towns_begin, towns_end),
         (str_store_string, s13, "str_town"),
       (else_try),
         (str_store_string, s13, "str_castle"),
       (try_end),
	   (troop_get_type, reg4, "$temp"),
       (str_store_string, s12, "str__but_he_is_holding_there_as_a_prisoner_at_dungeon_of_s13"), #[TODO : Control Grammer] New text, control grammer of text later. s13 can be "castle" or "town".
     (try_end),

	 (try_begin),
		(party_is_active, ":cur_center"),
		(str_store_party_name, s11, ":cur_center"),
	 (else_try),
		(str_store_party_name, s11, "str_prisoner_at_large"),
	 (try_end),
     ]],
  [anyone|plyr, "tavern_traveler_talk", [],
   "Farewell.", "close_window", []],
  [anyone|plyr, "tavern_traveler_answer", [(store_troop_gold, ":cur_gold", "trp_player"),
                                            (ge, ":cur_gold", 100)],
   "Here's 100 mon. Tell me what you know.", "tavern_traveler_continue", [(party_get_slot, ":info_faction", "$g_encountered_party", slot_center_traveler_info_faction),
                                           (call_script, "script_update_faction_traveler_notes", ":info_faction"),
                                           (change_screen_notes, 2, ":info_faction"),
                                           ]],
  [anyone|plyr, "tavern_traveler_answer", [],
   "Sorry friend. I am not interested.", "close_window", []],
  [anyone, "tavern_traveler_continue", [],
   "Well, that's all I can tell you. Good bye.", "close_window", [(troop_remove_gold, "trp_player", 100),]],
##diplomacy end+

  [anyone, "tavern_mercenary_cant_lead", [], "That's a pity. Well, {reg3?we will:I will} be lingering around here for a while,\
 if you need to hire anyone.", "close_window", []],
  [anyone,"master_craftsman_pretalk", [],
   "Very good, my {lord/lady}. Do you require anything else?", "master_craftsman_talk",[]],
  [anyone|plyr,"master_craftsman_talk", [],
   "Let's go over the accounts.", "master_craftsman_accounts",[]],
  [anyone|plyr,"master_craftsman_talk", [],
   "Let's check the inventories.", "master_craftsman_pretalk",[
   (change_screen_loot, "$g_talk_troop"),
   ]],
  [anyone|plyr,"master_craftsman_talk", [
  (party_slot_eq, "$g_encountered_party", slot_center_player_enterprise_production_order, 1),
  ],
   "I'd like you to sell goods as they are produced.", "master_craftsman_pretalk",[
  (party_set_slot, "$g_encountered_party", slot_center_player_enterprise_production_order, 0),
   ]],
  [anyone|plyr,"master_craftsman_talk", [
  (party_slot_eq, "$g_encountered_party", slot_center_player_enterprise_production_order, 0),
  ],
   "I'd like you to keep all goods in the warehouse until I arrive.", "master_craftsman_pretalk",[
  (party_set_slot, "$g_encountered_party", slot_center_player_enterprise_production_order, 1),
   ]],
  [anyone,"master_craftsman_accounts", [
  ], "We currently produce {s3} worth {reg1} mon each week, while the quantity of {s4} needed to manufacture it costs {reg2}, and labor and upkeep are {reg3}.{s9} This means that we theoretically make a {s12} of {reg0} mon a week, assuming that we have no raw materials in the inventories, and that we sell directly to the market.", "master_craftsman_pretalk",
  [
    (party_get_slot, ":item_produced", "$g_encountered_party", slot_center_player_enterprise),
    (call_script, "script_process_player_enterprise", ":item_produced", "$g_encountered_party"),

    (try_begin),
	  (ge, reg0, 0),
	  (str_store_string, s12, "str_profit"),
    (else_try),
	  (str_store_string, s12, "str_loss"),
    (try_end),

    (str_store_item_name, s3, ":item_produced"),
    (item_get_slot, ":primary_raw_material", ":item_produced", slot_item_primary_raw_material),
    (str_store_item_name, s4, ":primary_raw_material"),

    (item_get_slot, ":secondary_raw_material", ":item_produced", slot_item_secondary_raw_material),
    (str_clear, s9),
    (try_begin),
	  (gt, ":secondary_raw_material", 0),
	  (str_store_item_name, s11, ":secondary_raw_material"),
	  (str_store_string, s9, "str_describe_secondary_input"),
    (try_end),
  ]],
  [anyone|plyr,"master_craftsman_talk", [
  ], "Could you explain my options related to production?", "master_craftsman_production_options",[]],
  [anyone,"master_craftsman_production_options", [
  (str_store_party_name, s5, "$g_encountered_party"),
  ], "Certainly, my {lord/lady}. Most of the time, the most profitable thing for you to do would be to let us buy raw materials and sell the finished goods directly to the market. Because of our longstanding relations with the local merchants, we can usually get a very good price.", "master_craftsman_production_options_2",[]],
  [anyone,"master_craftsman_production_options_2", [
  (str_store_party_name, s5, "$g_encountered_party"),
  ], "However, if you find that you can acquire raw materials cheaper outside {s5}, you may place them in the inventories, and we will use them instead of buying from the market. Likewise, if you feel that you can get a better price for the finished goods elsewhere, then you may ask us to deposit what we produce in our warehouses for you to take.", "master_craftsman_pretalk",[]],
  [anyone|plyr,"master_craftsman_talk", [
  ], "It will no longer be possible for me to continue operating this shop.", "master_craftsman_auction_price",[]],
  [anyone,"master_craftsman_auction_price", [
  (party_get_slot, ":item_produced", "$g_encountered_party", slot_center_player_enterprise),
  (item_get_slot, ":base_price",":item_produced", slot_item_base_price),
  (item_get_slot, ":number_runs", ":item_produced", slot_item_output_per_run),
  (store_mul, "$liquidation_price", ":base_price", ":number_runs"),
  (val_mul, "$liquidation_price", 4),

  (troop_get_inventory_capacity, ":total_capacity", "$g_talk_troop"),
  (try_for_range, ":capacity_iterator", 0, ":total_capacity"),
		(troop_get_inventory_slot, ":item_in_slot", "$g_talk_troop", ":capacity_iterator"),
		(gt, ":item_in_slot", 0),
		(item_get_slot, ":price_for_inventory_item", ":item_in_slot", slot_item_base_price),
#		(troop_inventory_slot_get_item_amount, ":item_ammo", "$g_talk_troop", ":capacity_iterator"),
#		(troop_inventory_slot_get_item_max_amount, ":item_max_ammo", "$g_talk_troop", ":capacity_iterator"),
#		(try_begin),
#			(lt, ":item_ammo", ":item_max_ammo"),
#			(val_mul, ":price_for_inventory_item", ":item_ammo"),
#			(val_div, ":price_for_inventory_item", ":item_max_ammo"),
#		(try_end),

        (store_sub, ":item_slot_no", ":item_in_slot", trade_goods_begin),
        (val_add, ":item_slot_no", slot_town_trade_good_prices_begin),
        (party_get_slot, ":index", "$g_encountered_party", ":item_slot_no"),
		(val_mul, ":price_for_inventory_item", ":index"),
		(val_div, ":price_for_inventory_item", 1200),
		#modify by site
		#divide by 1200 not 1000
		(val_add, "$liquidation_price", ":price_for_inventory_item"),
  (try_end),

  (assign, reg4, "$liquidation_price"),

  ], "A pity, my {lord/lady}. If we sell the land and the equipment, and liquidate the inventories, I estimate that we can get {reg4} mon.", "master_craftsman_auction_decide",[]],
  [anyone|plyr,"master_craftsman_auction_decide", [
  ], "That sounds reasonable. Please proceed with the sale.", "master_craftsman_liquidation",[
  (troop_add_gold, "trp_player", "$liquidation_price"),
  (troop_clear_inventory, "$g_talk_troop"),
  (party_set_slot, "$g_encountered_party", slot_center_player_enterprise, 0),
  (party_set_slot, "$g_encountered_party", slot_center_player_enterprise_production_order, 0),

  ]],
  [anyone|plyr,"master_craftsman_auction_decide", [
  ], "Hmm. Let's hold off on that.", "master_craftsman_pretalk",[]],
  [anyone,"master_craftsman_liquidation", [
  ], "As you wish. It was an honor to have been in your employ.", "close_window",[
    (finish_mission),
  ]],
  [anyone|plyr,"master_craftsman_talk", [
  (eq, 1, 0),
  ], "{!}As you wish, {sir/my lady}. It was an honor to work in your employ.", "close_window",[]],
  [anyone|plyr,"master_craftsman_talk", [],
   "That is all for now.", "close_window",[]],
  [anyone|plyr,"merchant_ask_for_debts", [[store_troop_gold,reg(5),"trp_player"],[ge,reg(5),"$debt_to_merchants_guild"]],
   "Alright. I'll pay my debt to you.", "merchant_debts_paid",[[troop_remove_gold, "trp_player","$debt_to_merchants_guild"],
                                                                [assign,"$debt_to_merchants_guild",0]]],
  [anyone, "merchant_debts_paid", [], "Excellent. I'll let my fellow merchants know that you are clear of any debts.", "mayor_pretalk",[]],
  [anyone|plyr, "merchant_ask_for_debts", [], "I'm afraid I can't pay that sum now.", "merchant_debts_not_paid",[]],
  [anyone, "merchant_debts_not_paid", [(assign,reg(1),"$debt_to_merchants_guild")], "In that case, I am afraid, I can't deal with you. Guild rules...\
 Come back when you can pay the {reg1} mon.\
 And know that we'll be charging an interest to your debt.\
 So the sooner you pay it, the better.", "close_window",[]],
  [anyone|plyr,"investment_choose_enterprise",[(call_script, "script_process_player_enterprise", "itm_bread", "$g_encountered_party")], "A mill, to polish rice ({reg0} mon/week)", "investment_summary",[
  (assign, "$enterprise_production", "itm_bread"),
  ]],
  [anyone|plyr,"investment_choose_enterprise",[(call_script, "script_process_player_enterprise", "itm_ale", "$g_encountered_party")], "A brewery, to make sake from rice ({reg0} mon/week)", "investment_summary",[
  (assign, "$enterprise_production", "itm_ale"),
  ]],
  [anyone|plyr,"investment_choose_enterprise",[(call_script, "script_process_player_enterprise", "itm_leatherwork", "$g_encountered_party")], "A lacquerworks, to make lacquer ware from urushi sap ({reg0} mon/week)", "investment_summary",[
  (assign, "$enterprise_production", "itm_leatherwork"),
  ]],
  [anyone|plyr,"investment_choose_enterprise",[(call_script, "script_process_player_enterprise", "itm_wine", "$g_encountered_party")], "A brewery, to make soy sauce from soybeans ({reg0} mon/week)", "investment_summary",[
  (assign, "$enterprise_production", "itm_wine"),
  ]],
  [anyone|plyr,"investment_choose_enterprise",[(call_script, "script_process_player_enterprise", "itm_oil", "$g_encountered_party")], "A fish press, to make fish sauce from offal ({reg0} mon/week)", "investment_summary",[
  (assign, "$enterprise_production", "itm_oil"),
  ]],
  [anyone|plyr,"investment_choose_enterprise",[(call_script, "script_process_player_enterprise", "itm_tools", "$g_encountered_party")], "An smithy, to make tools from iron ({reg0} mon/week)", "investment_summary",[
  (assign, "$enterprise_production", "itm_tools"),
  ]],
  [anyone|plyr,"investment_choose_enterprise",[(call_script, "script_process_player_enterprise", "itm_velvet", "$g_encountered_party")], "A weavery and dyeworks, to make silk cloth from raw silk and dye ({reg0} mon/week)", "investment_summary",[
  (assign, "$enterprise_production", "itm_velvet"),
  ]],
  [anyone|plyr,"investment_choose_enterprise",[(call_script, "script_process_player_enterprise", "itm_wool_cloth", "$g_encountered_party")], "A weavery, to make hemp cloth from hemp fiber ({reg0} mon/week)", "investment_summary",[
  (assign, "$enterprise_production", "itm_wool_cloth"),
  ]],
  [anyone|plyr,"investment_choose_enterprise",[(call_script, "script_process_player_enterprise", "itm_linen", "$g_encountered_party")], "A weavery, to make linen from flax ({reg0} mon/week)", "investment_summary",[
  (assign, "$enterprise_production", "itm_linen"),
  ]],
  [anyone|plyr,"investment_choose_enterprise",[], "Never mind", "mayor_pretalk",[
  ]],
  [anyone,"investment_summary",[], "Very good, sir. The land and the materials on which you may build your {s3} will cost you {reg7} mon. Right now, your {s3} will produce {s4} worth {reg1} mon each week, while the {s6} needed to manufacture that batch will be {reg2} and labor and upkeep will be {reg3}.{s9} I should guess that your profit would be {reg0} mon a week. This assumes of course that prices remain constant -- which, I can virtually guarantee you, they will not. Do you wish to proceed?", "mayor_investment_confirm",
  [
    #(item_get_slot, ":base_price", "$enterprise_production", slot_item_base_price),
    #(item_get_slot, ":number_runs", "$enterprise_production", slot_item_output_per_run),
    #(store_mul, "$enterprise_cost", ":base_price", ":number_runs"),
    #(val_mul, "$enterprise_cost", 5),
    (item_get_slot, "$enterprise_cost", "$enterprise_production", slot_item_enterprise_building_cost),

    (assign, reg7, "$enterprise_cost"),

    (str_store_item_name, s4, "$enterprise_production"),

    (call_script, "script_get_enterprise_name", "$enterprise_production"),
    (str_store_string, s3, reg0),

    (call_script, "script_process_player_enterprise", "$enterprise_production", "$g_encountered_party"),
    #reg0: Profit per cycle
    #reg1: Selling price of total goods
    #reg2: Selling price of total goods

    (item_get_slot, ":primary_raw_material", "$enterprise_production", slot_item_primary_raw_material),
    (str_store_item_name, s6, ":primary_raw_material"),
	##diplomacy start+ For testing, print some additional diagnostics
	(assign, ":save_reg0", reg0),
	(assign, ":save_reg1", reg1),
	(try_begin),
		(ge, "$cheat_mode", 1),
		(ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_MEDIUM),
		(try_begin),
			(call_script, "script_dplmc_good_produced_at_center_or_its_villages", ":primary_raw_material", "$g_encountered_party"),
			(ge, reg0, 1),
			(display_message, "@{!}There is a local supply of {s6}."),
		(else_try),
			(store_sub, ":item_slot_no", ":primary_raw_material", trade_goods_begin),
			(val_add, ":item_slot_no", slot_town_trade_good_prices_begin),
			(item_get_slot, reg0, ":primary_raw_material", slot_item_base_price),
			(party_get_slot, reg1, "$g_encountered_party", ":item_slot_no"),
			(val_mul, reg0, reg1),
			(val_div, reg0, average_price_factor),
			(assign, ":base_price", reg0),
			(call_script, "script_dplmc_assess_ability_to_purchase_good_from_center", ":primary_raw_material", "$g_encountered_party"),
			(item_get_slot, reg1, ":primary_raw_material", slot_item_base_price),
			(val_mul, reg1, reg0),
			(val_div, reg1, average_price_factor),
			(assign, reg0, ":base_price"),
			(display_message, "@{!}{s6} must be imported, modifying the price from {reg0} to {reg1}."),
		(try_end),
	(try_end),
	##diplomacy end+

    (str_clear, s9),
    (assign, ":cost_of_secondary_input", reg10),
    (try_begin),
	  (gt, ":cost_of_secondary_input", 0),
	  (item_get_slot, ":secondary_raw_material", "$enterprise_production", slot_item_secondary_raw_material),
      (str_store_item_name, s11, ":secondary_raw_material"),
      (str_store_string, s9, "str_describe_secondary_input"),
    (try_end),
	##diplomacy end+
	(try_begin),
		(ge, "$cheat_mode", 1),
		(ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_MEDIUM),
		(gt, ":cost_of_secondary_input", 0),
		(try_begin),
			(call_script, "script_dplmc_good_produced_at_center_or_its_villages", ":secondary_raw_material", "$g_encountered_party"),
			(ge, reg0, 1),
			(display_message, "@{!}There is a local supply of {s11}."),
		(else_try),
			(store_sub, ":item_slot_no", ":secondary_raw_material", trade_goods_begin),
			(val_add, ":item_slot_no", slot_town_trade_good_prices_begin),
			(item_get_slot, reg0, ":secondary_raw_material", slot_item_base_price),
			(party_get_slot, reg1, "$g_encountered_party", ":item_slot_no"),
			(val_mul, reg0, reg1),
			(val_div, reg0, average_price_factor),
			(assign, ":base_price", reg0),
			(call_script, "script_dplmc_assess_ability_to_purchase_good_from_center", ":secondary_raw_material", "$g_encountered_party"),
			(item_get_slot, reg1, ":secondary_raw_material", slot_item_base_price),
			(val_mul, reg1, reg0),
			(val_div, reg1, average_price_factor),
			(assign, reg0, ":base_price"),
			(display_message, "@{!}{s9} must be imported, modifying the price from {reg0} to {reg1}."),
		(try_end),
	(try_end),
	(assign, reg0, ":save_reg0"),
	(assign, reg1, ":save_reg1"),
	##diplomacy end+
  ]],
  [anyone|plyr,"merchant_caravan_intro_1", [], "Yes. My name is {playername}. I will lead you to {s1}.",
   "merchant_caravan_intro_2",[(quest_get_slot, ":quest_target_center", "qst_escort_merchant_caravan", slot_quest_target_center),
                               (str_store_party_name, s1, ":quest_target_center"),
                               ]],
  [anyone,"merchant_caravan_intro_2", [], "Well, It is good to know we won't travel alone. What do you want us to do now?", "escort_merchant_caravan_talk",[]],
  [anyone,"merchant_caravan_follow_lead", [], "Alright. We'll be right behind you.", "close_window",[(assign, "$escort_merchant_caravan_mode", 0),
                                                                                                     (assign, "$g_leave_encounter", 1)]],
  [anyone,"merchant_caravan_stay_here", [], "Alright. We'll be waiting here for you.", "close_window",[(assign, "$escort_merchant_caravan_mode", 1),
                                                                                                       (assign, "$g_leave_encounter", 1)]],
  [anyone,"trade_info_request", [], "That information can be best obtained from caravan masters\
 and travelling merchants. If you want I can send you to the district where foreign merchants stay at when they come to the town.\
 If you spend some time there and listen to the talk,\
 you can learn a lot about what to buy and where to sell it.", "trade_info_request_2",[]],
  [anyone|plyr,"trade_info_request_2", [], "Then I'll go and spend some time with these merchants.", "close_window",
   [
       (jump_to_menu,"mnu_town_trade_assessment_begin"),
       (finish_mission),
    ]],
  [anyone|plyr,"trade_info_request_2", [], "I have no time for this right now.", "goods_merchant_pretalk",[]],
  [anyone,"sell_prisoner_outlaws", [[store_troop_kind_count,0,"trp_bandit"],[ge,reg(0),1],[assign,reg(1),reg(0)],[val_mul,reg(1),20],[assign,reg(2),reg(0)],[val_mul,reg(2),20]],
   "Let me see. You've brought {reg0} bandits, so 20 mon for each comes up to {reg1} mon.", "sell_prisoner_outlaws",
   [[call_script, "script_troop_add_gold", "trp_player", reg(1)],[add_xp_to_troop,reg(2)],[remove_member_from_party,"trp_bandit"]]],
  [anyone,"sell_prisoner_outlaws", [[store_troop_kind_count,0,"trp_brigand"],[ge,reg(0),1],[assign,reg(1),reg(0)],[val_mul,reg(1),30],[assign,reg(2),reg(0)],[val_mul,reg(2),30]],
   "Well well, you've captured {reg0} brigands. Each one is worth 30 mon, so I'll give you {reg1} for them in total.", "sell_prisoner_outlaws",
   [[call_script, "script_troop_add_gold", "trp_player", reg(1)],[add_xp_to_troop,reg(2)],[remove_member_from_party,"trp_brigand"]]],
  [anyone,"sell_prisoner_outlaws", [], "I suppose that'll be all, then.", "close_window",[]],
  [anyone|plyr,"town_merchant_talk", [(is_between,"$g_talk_troop",weapon_merchants_begin,weapon_merchants_end)],
   "I want to buy a new weapon. Show me your wares.", "trade_requested_weapons",[]],
  [anyone|plyr,"town_merchant_talk", [(is_between,"$g_talk_troop",armor_merchants_begin,armor_merchants_end)],
   "I am looking for some equipment. Show me what you have.", "trade_requested_armor",[]],
  [anyone|plyr,"town_merchant_talk", [(is_between,"$g_talk_troop",horse_merchants_begin,horse_merchants_end)],
   "I am thinking of buying a horse.", "trade_requested_horse",[]],
##diplomacy start+ Auto-sell hooks
  [anyone|plyr,"town_merchant_talk", [
   (is_between,"$g_talk_troop",weapon_merchants_begin,weapon_merchants_end),],
   "I'd like to sell some weapons.", "dplmc_trade_autosell_1",[
	(assign, "$temp", weapons_begin),
	(assign, "$temp_2", ranged_weapons_end),#this range includes shields
	]],
  [anyone|plyr,"town_merchant_talk", [
   (is_between,"$g_talk_troop",armor_merchants_begin,armor_merchants_end),],
   "I'd like to sell some armor.", "dplmc_trade_autosell_1",[
	(assign, "$temp", armors_begin),
	(assign, "$temp_2", armors_end),
	]],
  [anyone|plyr,"town_merchant_talk", [
   (is_between, "$g_talk_troop", horse_merchants_begin, horse_merchants_end),],
   "I'd like to sell some horses to you.", "dplmc_trade_autosell_1",[
	(assign, "$temp", horses_begin),
	(assign, "$temp_2", horses_end),
	]],
##diplomacy end+

##diplomacy start+ change to use script_dplmc_print_subordinate_says_sir_madame_to_s0
  [anyone,"trade_requested_weapons", [(call_script,"script_dplmc_print_subordinate_says_sir_madame_to_s0"),], "Ah, yes {s0}. These arms are the best you'll find anywhere.", "merchant_trade",[[change_screen_trade]]],
  [anyone,"trade_requested_armor", [(call_script,"script_dplmc_print_subordinate_says_sir_madame_to_s0"),], "Of course, {s0}. You won't find better quality armour than these in all Japan.", "merchant_trade",[[change_screen_trade]]],
  [anyone,"trade_requested_horse", [(call_script,"script_dplmc_print_subordinate_says_sir_madame_to_s0"),], "You have a fine eye for horses, {s0}. You won't find better beasts than these anywhere else.", "merchant_trade",[[change_screen_trade]]],
##diplomacy end+

  [anyone,"merchant_trade", [], "Anything else?", "town_merchant_talk",[]],
  [anyone|plyr,"town_merchant_talk", [], "Tell me. What are people talking about these days?", "merchant_gossip",[]],
  [anyone,"merchant_gossip", [], "Well, nothing new lately. Prices, weather, the war, the same old things.", "town_merchant_talk",[]],
  [anyone|plyr,"town_merchant_talk", [], "Good-bye.", "close_window",[]],
                    ##diplomacy end+
  [anyone|plyr,"town_dweller_talk", [(check_quest_active, "qst_hunt_down_fugitive"),
                                     (neg|check_quest_concluded, "qst_hunt_down_fugitive"),
                                      (quest_slot_eq, "qst_hunt_down_fugitive", slot_quest_target_center, "$current_town"),
                                      (quest_get_slot, ":quest_target_dna", "qst_hunt_down_fugitive", slot_quest_target_dna),
                                      (call_script, "script_get_name_from_dna_to_s50", ":quest_target_dna"),
                                      (str_store_string, s4, s50),
                                      ],
   "I am looking for a man by the name of {s4}. I was told he may be hiding here.", "town_dweller_ask_fugitive",[]],
  ##diplomacy start+ replace {sir/madame} with {my lord/my lady} or {your highness} as appropriate
  [anyone ,"town_dweller_ask_fugitive", #[],
   [(call_script,"script_dplmc_print_subordinate_says_sir_madame_to_s0"),],
   "Strangers come and go to our village, {s0}. If he is hiding here, you will surely find him if you look around.", "close_window",[]],
  ##diplomacy end+

# Ryan BEGIN
  [anyone|plyr,"town_dweller_talk",
   [
     (eq, 1, 0),
     (check_quest_active, "qst_meet_spy_in_enemy_town"),
     (neg|check_quest_succeeded, "qst_meet_spy_in_enemy_town"),
     (quest_slot_eq, "qst_meet_spy_in_enemy_town", slot_quest_target_center, "$current_town"),
     (str_store_item_name,s5,"$spy_item_worn"),
     ],
   "Pardon me, but is that a {s5} you're wearing?", "town_dweller_quest_meet_spy_in_enemy_town_ask_item",
   [
     ]],
  [anyone, "town_dweller_quest_meet_spy_in_enemy_town_ask_item", [
     (str_store_item_name,s5,"$spy_item_worn"),

     (try_begin),
     (troop_has_item_equipped,"$g_talk_troop","$spy_item_worn"),
     (str_store_string,s6,"@A {s5}? Well... Yes, I suppose it is. What a strange thing to ask."),
     (else_try),
     (str_store_string,s6,"@Eh? No, it most certainly is not a {s5}. I'd start questioning my eyesight if I were you."),
     (try_end),
  ],
   "{s6}", "town_dweller_talk",[]],
  [anyone|plyr|repeat_for_100,"town_dweller_talk",
   [
     (store_repeat_object,":object"),
     (lt,":object",4), # repeat only 4 times

     (check_quest_active, "qst_meet_spy_in_enemy_town"),
     (neg|check_quest_succeeded, "qst_meet_spy_in_enemy_town"),
     (quest_slot_eq, "qst_meet_spy_in_enemy_town", slot_quest_target_center, "$current_town"),

     (store_add,":string",":object","str_secret_sign_1"),
     (str_store_string, s4, ":string"),
     ],
   "{s4}", "town_dweller_quest_meet_spy_in_enemy_town",
   [
     (store_repeat_object,":object"),
     (assign, "$temp", ":object"),
     ]],
  [anyone ,"town_dweller_quest_meet_spy_in_enemy_town",
   [
     (call_script, "script_agent_get_town_walker_details", "$g_talk_agent"),
     (assign, ":walker_type", reg0),
     (eq, ":walker_type", walkert_spy),
     (quest_get_slot, ":secret_sign", "qst_meet_spy_in_enemy_town", slot_quest_target_amount),
     (val_sub, ":secret_sign", secret_signs_begin),
     (eq, ":secret_sign", "$temp"),
     (store_add, ":countersign", ":secret_sign", countersigns_begin),
     (str_store_string, s4, ":countersign"),
     ],
   "{s4}", "town_dweller_quest_meet_spy_in_enemy_town_know",[]],
  [anyone, "town_dweller_quest_meet_spy_in_enemy_town", [],
   "Eh? What kind of gibberish is that?", "town_dweller_quest_meet_spy_in_enemy_town_dont_know",[]],
  [anyone|plyr, "town_dweller_quest_meet_spy_in_enemy_town_dont_know", [],
   "Never mind.", "close_window",[]],
  [anyone|plyr, "town_dweller_quest_meet_spy_in_enemy_town_know", [
     (quest_get_slot, ":quest_giver", "qst_meet_spy_in_enemy_town", slot_quest_giver_troop),
     (str_store_troop_name, s4, ":quest_giver"),
  ],
   "{s4} sent me to collect your reports. Do you have them with you?", "town_dweller_quest_meet_spy_in_enemy_town_chat",[]],
  [anyone, "town_dweller_quest_meet_spy_in_enemy_town_chat", [
     (quest_get_slot, ":quest_giver", "qst_meet_spy_in_enemy_town", slot_quest_giver_troop),
     (str_store_troop_name, s4, ":quest_giver"),
  ],
   "I've been expecting you. Here they are, make sure they reach {s4} intact and without delay.", "town_dweller_quest_meet_spy_in_enemy_town_chat_2",[
     (call_script, "script_succeed_quest", "qst_meet_spy_in_enemy_town"),
     (call_script, "script_center_remove_walker_type_from_walkers", "$current_town", walkert_spy),
   ]],
  [anyone|plyr, "town_dweller_quest_meet_spy_in_enemy_town_chat_2", [],
   "Farewell.", "close_window",
   [
     ]],
# Ryan END

  [anyone|plyr,"town_dweller_talk", [(party_slot_eq, "$current_town", slot_party_type, spt_village),
                                     (eq, "$info_inquired", 0)], "What can you tell me about this village?", "town_dweller_ask_info",[(assign, "$info_inquired", 1)]],
  [anyone|plyr,"town_dweller_talk", [(party_slot_eq, "$current_town", slot_party_type, spt_town),
                                     (eq, "$info_inquired", 0)], "What can you tell me about this town?", "town_dweller_ask_info",[(assign, "$info_inquired", 1)]],
  [anyone,"town_dweller_ask_info", [(str_store_party_name, s5, "$current_town"),
                                    (assign, reg4, 0),
                                    (try_begin),
                                      (party_slot_eq, "$current_town", slot_party_type, spt_town),
                                      (assign, reg4, 1),
                                    (try_end),
									#diplomacy start+
									#replace {sir/madame} with {my lord/my lady} or {your highness} if appropriate
									(call_script, "script_dplmc_print_subordinate_says_sir_madame_to_s0"),
                                    (str_store_string, s6, "@This is the {reg4?town:village} of {s5}, {s0}."),
									##diplomacy end+
                                    (str_clear, s10),
                                    (try_begin),
                                      (party_slot_eq, "$current_town", slot_town_lord, "trp_player"),
                                      (str_store_string, s10, "@{s6} Our {reg4?town:village} and the surrounding lands belong to you of course, my {lord/lady}."),
                                    (else_try),
                                      (party_get_slot, ":town_lord", "$current_town", slot_town_lord),
                                      (ge, ":town_lord", 0),
                                      (str_store_troop_name, s7, ":town_lord"),
                                      (store_troop_faction, ":town_lord_faction", ":town_lord"),
                                      (str_store_faction_name, s8, ":town_lord_faction"),
                                      (str_store_string, s10, "@{s6} Our {reg4?town:village} and the surrounding lands belong to {s7} of {s8}."),
                                    (try_end),
                                    (str_clear, s5),
                                    (assign, ":number_of_goods", 0),
                                    (try_for_range, ":cur_good", trade_goods_begin, trade_goods_end),
                                      #(store_sub, ":cur_good_slot", ":cur_good", trade_goods_begin),
                                      #(val_add, ":cur_good_slot", slot_town_trade_good_productions_begin),
                                      #(party_get_slot, ":production", "$g_encountered_party", ":cur_good_slot"),

                                      (call_script, "script_center_get_production", "$g_encountered_party", ":cur_good"),
                                      (assign, ":production", reg0),
                                      (ge, ":production", 20),

                                      (str_store_item_name, s3, ":cur_good"),
                                      (try_begin),
                                        (eq, ":number_of_goods", 0),
                                        (str_store_string, s5, s3),
                                      (else_try),
                                        (eq, ":number_of_goods", 1),
                                        (str_store_string, s5, "@{s3} and {s5}"),
                                      (else_try),
                                        (str_store_string, s5, "@{!}{s3}, {s5}"),
                                      (try_end),
                                      (val_add, ":number_of_goods", 1),
                                    (try_end),
									(try_begin),
										(gt, ":number_of_goods", 0),
										(assign, reg20, 1),
									(else_try),
										(assign, reg20, 0),
									(try_end),

                                    (str_store_string, s11, "@{reg20?We mostly produce {s5} here:We don't produce much here these days}.\
 If you would like to learn more, you can speak with the {reg4?chief merchant:village headman}. He is nearby, right over there."),
                                    ],
   "{s10} {s11}", "close_window",[]],
  [anyone|plyr,"town_dweller_talk", [(party_slot_eq, "$current_town", slot_party_type, spt_village),
                                     (eq, "$welfare_inquired", 0)], "How is life here?", "town_dweller_ask_situation",[(assign, "$welfare_inquired", 1)]],
  [anyone|plyr,"town_dweller_talk", [(party_slot_eq, "$current_town", slot_party_type, spt_town),
                                     (eq, "$welfare_inquired", 0)], "How is life here?", "town_dweller_ask_situation",[(assign, "$welfare_inquired", 1)]],
  [anyone,"town_dweller_ask_situation", [(call_script, "script_agent_get_town_walker_details", "$g_talk_agent"),
                                         (assign, ":walker_type", reg0),
                                         (eq, ":walker_type", walkert_needs_money),
										 #diplomacy start+ replace {sir/madame} with {my lord/my lady} or {your highness} if appropriate
										 (call_script, "script_dplmc_print_subordinate_says_sir_madame_to_s0"),
										 #diplomacy end+
                                         (party_slot_eq, "$current_town", slot_party_type, spt_village)],
   #diplomacy start+ replace {sir/madame} with {my lord/my lady} or {your highness} if appropriate
   "Disaster has struck my family, {s0}. We have no land of our own, and the others have no money to pay for our labor, or even to help us. My poor children lie at home hungry and sick. I don't know what we'll do.", "town_dweller_poor",[]],
   #diplomacy end+
  [anyone,"town_dweller_ask_situation", [(call_script, "script_agent_get_town_walker_details", "$g_talk_agent"),
                                         (assign, ":walker_type", reg0),
										 #diplomacy start+ replace {sir/madame} with {my lord/my lady} or {your highness} if appropriate
										 (call_script, "script_dplmc_print_subordinate_says_sir_madame_to_s0"),
										 #diplomacy end+
                                         (eq, ":walker_type", walkert_needs_money)],
   #diplomacy start+ replace {sir/madame} with {my lord/my lady} or {your highness} if appropriate
   "My life is miserable, {s0}. I haven't been able to find a job for months, and my poor children go to bed hungry each night.\
 My neighbours are too poor themselves to help me.", "town_dweller_poor",[]],
   #diplomacy end+
  [anyone|plyr,"town_dweller_poor", [(store_troop_gold, ":gold", "trp_player"),
                                     (ge, ":gold", 300),
                                     ],
   "Then take these 300 mon. I hope this will help you and your family.", "town_dweller_poor_paid",
   [(troop_remove_gold, "trp_player", 300),
    ]],
  [anyone|plyr,"town_dweller_poor", [],
   "Then clearly you must travel somewhere else, or learn another trade.", "town_dweller_poor_not_paid",[]],
  [anyone,"town_dweller_poor_not_paid", [], "Yes {sir/madam}. I will do as you say.", "close_window",[]],
  [anyone,"town_dweller_poor_paid", [], "{My lord/My good lady}. \
 You are so good and generous. I will tell everyone how you helped us.", "close_window",
   [(call_script, "script_change_player_relation_with_center", "$g_encountered_party", 1),
    (call_script, "script_agent_get_town_walker_details", "$g_talk_agent"),
    (assign, ":walker_no", reg2),
    (call_script, "script_center_set_walker_to_type", "$g_encountered_party", ":walker_no", walkert_needs_money_helped),
    ]],
  [anyone,"town_dweller_ask_situation", [(call_script, "script_agent_get_town_walker_details", "$g_talk_agent"),
                                         (assign, ":walker_type", reg0),
                                         (eq, ":walker_type", walkert_needs_money_helped),
										 #diplomacy start+ replace {sir/madame} with {my lord/my lady} or {your highness} if appropriate
										 (call_script, "script_dplmc_print_subordinate_says_sir_madame_to_s0"),
										 #diplomacy end+
                                         ],
   #diplomacy start+ replace {sir/madame} with {my lord/my lady} or {your highness} if appropriate
   "Thank you for your kindness {s0}. With your help our lives will be better. I will pray for you everyday.", "close_window",[]],
   #diplomacy end+
  [anyone,"town_dweller_ask_situation", [(neg|party_slot_ge, "$current_town", slot_town_prosperity, 30),
  #diplomacy start+ replace {sir/madame} with {my lord/my lady} or {your highness} if appropriate
  (call_script, "script_dplmc_print_subordinate_says_sir_madame_to_s0"),],
   "Times are hard, {s0}. We work hard all day and yet we go to sleep hungry most nights.", "town_dweller_talk",[]],
   ##diplomacy end+

  [anyone,"town_dweller_ask_situation", [(neg|party_slot_ge, "$current_town", slot_town_prosperity, 70),#],
   #diplomacy start+ replace {sir/madame} with {my lord/my lady} or {your highness} if appropriate
   (call_script, "script_dplmc_print_subordinate_says_sir_madame_to_s0"),],
   "Times are hard, {s0}. But we must count our blessings.", "town_dweller_talk",[]],
   #diplomacy end+
  [anyone,"town_dweller_ask_situation",
  ##diplomacy start+ replace {sir/madame} with {my lord/my lady} or {your highness} if appropriate
  [(call_script, "script_dplmc_print_subordinate_says_sir_madame_to_s0"),],
   "We are not doing too badly {s0}. We must count our blessings.", "town_dweller_talk",[]],
  ##diplomacy end+

  [anyone|plyr,"town_dweller_talk", [], "What is your trade?", "town_dweller_ask_trade",[]],
  [anyone,"town_dweller_ask_trade", [
  (call_script, "script_town_walker_occupation_string_to_s14", "$g_talk_agent"),
  ],
   "{s14}", "town_dweller_talk",[]],
  [anyone|plyr,"town_dweller_talk", [(eq, "$rumors_inquired", 0)], "What is the latest rumor around here?", "town_dweller_ask_rumor",[(assign, "$rumors_inquired", 1)]],
  ##diplomacy start+ The player's persuasive abilities can coax a rumor from the less friendly.
  ##OLD:
  #[anyone,"town_dweller_ask_rumor", [(neg|party_slot_ge, "$current_town", slot_center_player_relation, -5)], "I don't know anything that would be of interest to you.", "town_dweller_talk",[]],
  ##NEW:
  [anyone,"town_dweller_ask_rumor", [
  (store_skill_level, reg0, "skl_persuasion", "trp_player"),
  (store_sub, reg0, -5, reg0),
  (neg|party_slot_ge, "$current_town", slot_center_player_relation, reg0),
  ],
  "I don't know anything that would be of interest to you.", "town_dweller_talk",[]],
  ##diplomacy end+

  [anyone,"town_dweller_ask_rumor", [(store_mul, ":rumor_id", "$current_town", 197),
                                     (val_add,  ":rumor_id", "$g_talk_agent"),
                                     (call_script, "script_get_rumor_to_s61", ":rumor_id"),
                                     (gt, reg0, 0)], "{s61}", "town_dweller_talk",[]],
  [anyone,"town_dweller_ask_rumor", [], "I haven't heard anything interesting lately.", "town_dweller_talk",[]],
  
  #gekokujo 3.1 crimes against townspeople and villagers start
  [anyone|plyr,"town_dweller_talk", [], "[Action]", "town_dweller_crime_1", []],
  
  [anyone,"town_dweller_crime_1", [], "{Sir/Madam}?...", "town_dweller_crime_2", []],
  
  #beg -- this is not a crime, but let's use the same base system
  [anyone|plyr,"town_dweller_crime_2", 
    [
      (get_player_agent_no, ":player"),
      
      (assign, reg30, 0), #total holiness score
      
      #first run, check for monk's clothes and accoutrements
      (try_for_range, ":ek_slot", ek_item_0, ek_foot),
        (agent_get_item_slot, ":item", ":player", ":ek_slot"),
        (gt, ":item", 0),
        
        (try_begin),
          (eq, ":item", "itm_gekokujo_kimono_2_monk"), #+45 for monk's clothes
          (val_add, reg30, 45),
        (else_try),
          (eq, ":item", "itm_gekokujo_monk_headwrap"), #+30 for monk's cowl
          (val_add, reg30, 30),
        (else_try),
          (eq, ":item", "itm_gekokujo_sugegasa_1"), #+15 for sugegasa
          (val_add, reg30, 15),
        (else_try),
          (is_between, ":item", "itm_gekokujo_jo", "itm_gekokujo_otsuchi"), #+15 for bo or jo *wielded*
          (agent_get_wielded_item, ":wielded", ":player", 0),
          (eq, ":wielded", ":item"),
          (val_add, reg30, 15),
        (try_end),
      (try_end),
      
      #second run, flat 75 for wearing miko's clothes
      (agent_get_item_slot, ":item", ":player", ek_body),
      (try_begin),
        (eq, ":item", "itm_gekokujo_hakama_1_miko"),
        (assign, reg30, 75), #override any monk bonuses
      (try_end),
      
      #third run, -15 for each large weapon, helmet, and armor
      (try_for_range, ":ek_slot", ek_item_0, ek_foot),
        (agent_get_item_slot, ":item", ":player", ":ek_slot"),
        (gt, ":item", 0),
        
        (this_or_next|is_between, ":item", "itm_gekokujo_katana_1", "itm_gekokujo_tanto_1"), #large 1
        (this_or_next|is_between, ":item", "itm_gekokujo_ninjato_1", "itm_gekokujo_kama_1"), #large 2
        (this_or_next|is_between, ":item", "itm_gekokujo_otsuchi", "itm_gekokujo_bullets_1"), #large 3
        (this_or_next|is_between, ":item", "itm_gekokujo_tatami_short_1", "itm_gekokujo_sugegasa_1"), #armor
        (is_between, ":item", "itm_gekokujo_hari_o_1", "itm_gekokujo_tabi"), #helmets
        
        (val_sub, reg30, 15),
      (try_end),
      
      (val_min, reg30, 90),
      (val_max, reg30, 0),
    ], 
    "[Beg] - {reg30}% to succeed", "town_dweller_beg_result", 
    [
      #check if the begging was a success
      (store_random_in_range, ":beg_roll", 0, 100),
      (try_begin),
        (ge, reg30, ":beg_roll"),
        (assign, "$gekokujo_beg_result", 1),
      (else_try),
        (assign, "$gekokujo_beg_result", 0),
      (try_end),
    ]],
  
    
  #let's process the begging
  [anyone, "town_dweller_beg_result", 
    [
      (store_random_in_range, ":variation", 0, 5),
      
      (try_begin),
        (eq, "$gekokujo_beg_result", 1),
        (store_add, ":reply", "str_gekokujo_beg_success_reply_1", ":variation"),
      (else_try),
        (store_add, ":reply", "str_gekokujo_beg_fail_reply_1", ":variation"),
      (try_end),
      
      (str_store_string, s35, ":reply"),
    ], 
    "{s35}", "close_window",
    [
      (jump_to_menu, "mnu_beg"),
      (finish_mission),
    ]],
  
  #mug
  [anyone|plyr,"town_dweller_crime_2", 
    [
      (get_player_agent_no, ":player"),
      
      (assign, reg5, 0), #total intimidation score
      (assign, reg6, 90), #total getaway score
      
      (try_for_range, ":ek_slot", ek_item_0, ek_head),
        (agent_get_item_slot, ":item", ":player", ":ek_slot"),
        (gt, ":item", 0),
        
        (assign, ":weapon_score", 0),
        (assign, ":getaway_score", 0),
        
        (try_begin),
          #basic weapons are +10% to steal, -15% to get away
          (this_or_next|is_between, ":item", "itm_wooden_stick", "itm_gekokujo_katana_1"),
          (is_between, ":item", "itm_gekokujo_kama_1", "itm_gekokujo_bo_iron"),
          (assign, ":weapon_score", 10),
          (assign, ":getaway_score", -15),
        (else_try),
          #ranged weapons are +20% to steal, -30% to get away
          (is_between, ":item", "itm_gekokujo_yumi_1", "itm_gekokujo_bullets_1"),
          (assign, ":weapon_score", 20),
          (assign, ":getaway_score", -30),
        (else_try),
          #large weapons are +30% to steal, -35% to get away
          (this_or_next|is_between, ":item", "itm_gekokujo_katana_1", "itm_gekokujo_tanto_1"),
          (this_or_next|is_between, ":item", "itm_gekokujo_sabakato_blunt", "itm_gekokujo_kama_1"),
          (is_between, ":item", "itm_gekokujo_bo_iron", "itm_gekokujo_yumi_1"),
          (assign, ":weapon_score", 30),
          (assign, ":getaway_score", -35),
        (else_try),
          #ninja weapons and tantos are +50% to steal, -10% to get away
          (is_between, ":item", "itm_gekokujo_tanto_1", "itm_gekokujo_sabakato_blunt"),
          (assign, ":weapon_score", 50),
          (assign, ":getaway_score", -10),
        (try_end),
        
        #having the weapon out doubles the scores
        (try_begin),
          (agent_get_wielded_item, ":wielded", ":player", 0),
          (eq, ":wielded", ":item"),
          (val_mul, ":weapon_score", 2),
          (val_mul, ":getaway_score", 2),
        (try_end),
        
        (val_add, reg5, ":weapon_score"),
        (val_add, reg6, ":getaway_score"),
      (try_end),
      
      (val_min, reg5, 100),
      (val_max, reg5, 0),
      
      (val_min, reg6, 100),
      (val_max, reg6, 0),
    ], 
    "[Mug] - {reg5}% to steal, {reg6}% to escape", "town_dweller_crime_result", 
    [
      (assign, "$gekokujo_crime_type", 1), #1 = mugging
      
      #check if the mugging was a success
      (store_random_in_range, ":crime_roll", 0, 100),
      (try_begin),
        (ge, reg5, ":crime_roll"),
        (assign, "$gekokujo_crime_result", 1),
      (else_try),
        (assign, "$gekokujo_crime_result", 0),
      (try_end),
      
      #DEBUG start
      #(assign, reg9, ":crime_roll"),
      #(display_message, "@Mug Chance: {reg5}, Mug Roll: {reg9}"),
      #DEBUG end
      
      #check if the getaway was a success
      (store_random_in_range, ":crime_roll", 0, 100),
      (try_begin),
        (gt, reg6, ":crime_roll"),
        (assign, "$gekokujo_getaway_result", 1),
      (else_try),
        (assign, "$gekokujo_getaway_result", 0),
      (try_end),
      
      #DEBUG start
      #(assign, reg9, ":crime_roll"),
      #(display_message, "@Getaway Chance: {reg6}, Getaway Roll: {reg9}"),
      #DEBUG end
    ]],
  
    
  #pickpocket
  [anyone|plyr,"town_dweller_crime_2", 
    [
      (store_skill_level, reg7, "skl_looting", "trp_player"), #stealing skill
      (store_skill_level, reg8, "skl_athletics", "trp_player"), #getaway skill
      
      #pickpocket chance should range 10% to 90%
      (val_mul, reg7, 8),
      (val_add, reg7, 10),
      
      #getaway chance should be +4% per athletics skill
      (val_mul, reg8, 4),
      
      #getaway chance modified by the clothing and headgear you wear
      (get_player_agent_no, ":player"),
      (agent_get_item_slot, ":body", ":player", ek_body),
      (try_begin),
        #+50% for 'normal' clothes
        (is_between, ":body", "itm_gekokujo_kimono_1_1", "itm_gekokujo_tatami_half_1"),
        (val_add, reg8, 50),
      (else_try),
        #+24% for light armors, foreign clothes, and nude (too conspicuous)
        (this_or_next|is_between, ":body", "itm_gekokujo_ezo_armor_1", "itm_pilgrim_hood"),
        (is_between, ":body", "itm_gekokujo_tatami_half_1", "itm_gekokujo_okegawa_short_1"),
        (neg|gt, ":body", 0),
        (val_add, reg8, 24),
      (try_end),
      (agent_get_item_slot, ":head", ":player", ek_head),
      (try_begin),
        #+50% for cowls
        (is_between, ":head", "itm_gekokujo_monk_headwrap", "itm_gekokujo_jingasa_1"),
        (eq, ":head", "itm_pilgrim_hood"),
        (val_add, reg8, 50),
      (else_try),
        #+24% for sugegasa and jingasa
        (is_between, ":head", "itm_gekokujo_jingasa_1", "itm_gekokujo_hari_o_1"),
        (eq, ":head", "itm_gekokujo_sugegasa_1"),
        (val_add, reg8, 24),
      (try_end),
      #+0% for everything else
      
      (val_min, reg8, 100),
      (val_max, reg8, 0),
    ], 
    "[Pickpocket] - {reg7}% to steal, {reg8}% to escape", "town_dweller_crime_result", 
    [
      (assign, "$gekokujo_crime_type", 2), #2 = pickpocketing
      
      #check if the pickpocketing was a success
      (store_random_in_range, ":crime_roll", 0, 100),
      (try_begin),
        (gt, reg7, ":crime_roll"),
        (assign, "$gekokujo_crime_result", 1),
      (else_try),
        (assign, "$gekokujo_crime_result", 0),
      (try_end),
      
      #DEBUG start
      #(assign, reg10, ":crime_roll"),
      #(display_message, "@Pickpocket Chance: {reg7}, Pickpocket Roll: {reg10}"),
      #DEBUG end
      
      #check if the getaway was a success
      (store_random_in_range, ":crime_roll", 0, 100),
      (try_begin),
        (gt, reg8, ":crime_roll"),
        (assign, "$gekokujo_getaway_result", 1),
      (else_try),
        (assign, "$gekokujo_getaway_result", 0),
      (try_end),
      
      #DEBUG start
      #(assign, reg10, ":crime_roll"),
      #(display_message, "@Getaway Chance: {reg8}, Getaway Roll: {reg10}"),
      #DEBUG end
    ]],
    
  [anyone|plyr,"town_dweller_crime_2", 
    [
      (store_skill_level, reg11, "skl_tracking", "trp_player"), #stalking skill
      
      #stalking chance should be +4% per tracking skill
      (val_mul, reg11, 4),
      
      #stalking chance modified by the clothing and headgear you wear
      (get_player_agent_no, ":player"),
      (agent_get_item_slot, ":body", ":player", ek_body),
      (try_begin),
        #+50% for 'normal' clothes
        (is_between, ":body", "itm_gekokujo_kimono_1_1", "itm_gekokujo_tatami_half_1"),
        (val_add, reg11, 50),
      (else_try),
        #+24% for light armors, foreign clothes, and nude (too conspicuous)
        (this_or_next|is_between, ":body", "itm_gekokujo_ezo_armor_1", "itm_pilgrim_hood"),
        (is_between, ":body", "itm_gekokujo_tatami_half_1", "itm_gekokujo_okegawa_short_1"),
        (neg|gt, ":body", 0),
        (val_add, reg11, 24),
      (try_end),
      (agent_get_item_slot, ":head", ":player", ek_head),
      (try_begin),
        #+50% for cowls
        (is_between, ":head", "itm_gekokujo_monk_headwrap", "itm_gekokujo_jingasa_1"),
        (eq, ":head", "itm_pilgrim_hood"),
        (val_add, reg11, 50),
      (else_try),
        #+24% for sugegasa and jingasa
        (is_between, ":head", "itm_gekokujo_jingasa_1", "itm_gekokujo_hari_o_1"),
        (eq, ":head", "itm_gekokujo_sugegasa_1"),
        (val_add, reg11, 24),
      (try_end),
      #+0% for everything else
      
      (val_min, reg11, 100),
      (val_max, reg11, 0),
    ], 
    "[Follow Home] - {reg11}% to stalk", "town_dweller_crime_result", 
    [
      (assign, "$gekokujo_crime_type", 3), #3 = stalking
      
      #check if the stalking was a success
      (store_random_in_range, ":crime_roll", 0, 100),
      (try_begin),
        (gt, reg11, ":crime_roll"),
        (assign, "$gekokujo_crime_result", 1),
      (else_try),
        (assign, "$gekokujo_crime_result", 0),
      (try_end),
      
      (assign, "$gekokujo_getaway_result", 1), #you can't get caught stalking
      
      #(jump_to_menu, "mnu_crime"),
      #(finish_mission),
    ]],
    
  [anyone|plyr,"town_dweller_crime_2", [], "Nevermind.", "close_window", []],
  
  #let's process the crime
  [anyone, "town_dweller_crime_result", 
    [
      (store_random_in_range, ":variation", 0, 5),
      
      (try_begin),
        (eq, "$gekokujo_crime_result", 1),
        (try_begin),
          (eq, "$gekokujo_crime_type", 1), #mugging
          (store_add, ":reply", "str_gekokujo_mug_success_reply_1", ":variation"),
        (else_try),
          (eq, "$gekokujo_crime_type", 2), #pickpocketing
          (store_add, ":reply", "str_gekokujo_pickpocket_success_reply_1", ":variation"),
        (else_try),
          #stalking
          (store_add, ":reply", "str_gekokujo_stalking_reply_1", ":variation"),
        (try_end),
      (else_try),
        (try_begin),
          (eq, "$gekokujo_crime_type", 1), #mugging
          (store_add, ":reply", "str_gekokujo_mug_fail_reply_1", ":variation"),
        (else_try),
          (eq, "$gekokujo_crime_type", 2), #pickpocketing
          (store_add, ":reply", "str_gekokujo_pickpocket_fail_reply_1", ":variation"),
        (else_try),
          #stalking
          (store_add, ":reply", "str_gekokujo_stalking_reply_1", ":variation"),
        (try_end),
      (try_end),
      
      (str_store_string, s5, ":reply"),
    ], 
    "{s5}", "close_window",
    [
      (jump_to_menu, "mnu_crime"),
      (finish_mission),
    ]],
  
  #gekokujo 3.1 crimes against townspeople and villagers end

  [anyone|plyr,"town_dweller_talk", [], "[Leave]", "close_window",[]],
  [anyone, "merchant_end", [],
  "Heh! I must really be in a tight spot, to place my hopes in a passing stranger. However, something about you tells me that my trust is not misplaced. Now, go see if you can round up some volunteers.", "close_window", []],
  [anyone,"merchant_finale", [
  (faction_get_slot, ":faction_leader", "$g_encountered_party_faction", slot_faction_leader),
  (str_store_troop_name, s5, ":faction_leader"),
  ],
  "All of our enemies are dead, and nobody knows who killed them or why. Our samurai in {s5}'s hatamoto are obstructing the investigation. As far as everyone knows, this was just a feud among lower vassals that went too far. It looks like we are in and that we will stay. If you later see my severed head on display, then I have been premature, haha. I will see you around, {playername}.", "close_window",
  #"Yes, yes... Now, a couple of my boys have the watch captain pinned down in a back room, with a knife at his throat. I''ll need to go drag him before {s5} and explain what this breach of the peace is all about. You don't need to be part of that, though. I'll tell you what -- if all goes well, I'll meet you in the tavern again shortly, and let you know how it all came out. If you don't see me in the tavern, but instead see my head on a spike over the city gate, I'll assume you know enough to stay out of town for a while and forget this whole episode ever happened. So -- hopefully we'll meet again!", "close_window",
[
(assign, "$g_do_one_more_meeting_with_merchant", 2),
# (assign, "$g_do_one_more_meeting_with_merchant", 1), no need to this, do not open this line, it is already assigning while leaving mission.
# (jump_to_menu, "mnu_town"),
# (finish_mission, 0),
]],
  
#gekokujo 3.0 microfactions! end

  #[anyone, "merchant_all_quest_completed",
  #[
  #],
  #"TODO-STARTUP : You can leave now.", "close_window",
  #[
  #]],

  [anyone,"start", [], "Surrender or die. Make your choice", "battle_reason_stated",[]],
]
