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
[anyone|plyr, "fistfight_response", [],
"How's that?", "fistfight_response_2", [
]],
[anyone, "fistfight_response_2", [
],
"Good -- I'm glad you're interested. Here's the plan... It's a little complicated, so listen well. ", "fistfight_response_2a", [
]],
[anyone, "fistfight_response_2a", [
],
"You and this other fellow will start up a fight here. No weapons, no armor -- I'll sit back and take bets, and split the profits with the winner. If we make a loss, then I'll cover it. You've got nothing to lose -- except a bit of blood, of course.", "fistfight_response_3", [
]],
[anyone, "fistfight_response_3", [
],
"However, we can't organize this like one of those nice arena bouts, where everyone places their bets beforehand. People will walk in, drawn by the noise, and put a mon or two on whichever one of your two they think is winning. I'll give 'em even odds -- anything else is going to be too tricky for someone who's already on his third bottle of sake.", "fistfight_response_4", [
]],
[anyone, "fistfight_response_4", [
],
"So, as you can see, the trick is to stretch things out for as long as possible where it looks like you're losing, and people bet against you -- and then come back fast, and win, before the betting can turn. The best way to make money is for you to be battered almost to the floor, and then jump back off your feet and take the other guy down. However, you have to win in the end in order for me, and you, to make money. ", "fistfight_response_4a", [
]],
[anyone, "fistfight_response_4a", [
],
"Also, you can't stretch the fight out too long, or people will suspect a fix. So, one of you has to take a punch every so often. I don't care whose blood is spilled, but there has to be some blood.", "fistfight_response_5", [
]],
[anyone, "fistfight_response_5", [
],
"And one other thing -- my friend, your opponent, he doesn't take to well to complexity. So he's just going to come straight at you. It's up to you to supply the artistry.", "fistfight_response_5a", [
]],
[anyone, "fistfight_response_5a", [
],
"So, what do you think?", "fistfight_response_confirm", [
]],
[anyone|plyr, "fistfight_response_confirm", [
],
"{!}[Yes -- not yet implemented]", "close_window", [
]],
[anyone|plyr, "fistfight_response_confirm", [
],
"I have better things to do", "close_window", [
]],
[trp_ramun_the_slave_trader|plyr, "ramun_introduce_1", [], "Forgive me, you look like a trader, but I see none of your merchandise.", "ramun_introduce_2",[
(troop_set_slot, "$g_talk_troop", slot_troop_met_previously, 1),
]],
[trp_ramun_the_slave_trader|plyr, "ramun_introduce_1", [], "Never mind.", "close_window",[]],
[trp_ramun_the_slave_trader, "ramun_introduce_2", [], "A trader? Oh, aye, I certainly am that.\
My merchandise is a bit different from most, however. It has to be fed and watered twice a day and tries to run away if I turn my back.", "ramun_introduce_3",[]],
[trp_ramun_the_slave_trader|plyr, "ramun_introduce_3", [], "Livestock?", "ramun_introduce_4",[]],
[trp_ramun_the_slave_trader, "ramun_introduce_4", [], "Close enough. I like to call myself the man who keeps every boat on this ocean moving.\
Boats are driven by oars, you see, and oars need men to pull them or they stop. That's where I come in.", "ramun_introduce_5",[]],
[trp_ramun_the_slave_trader|plyr, "ramun_introduce_5", [], "Galley slaves.", "ramun_introduce_6",[]],
[trp_ramun_the_slave_trader, "ramun_introduce_6", [], "Now you're catching on! A trading port like this couldn't survive without them.\
The ships lose a few hands on every voyage, so there's always a high demand. The captains come to me and they pay well.", "ramun_introduce_7",[]],
[trp_ramun_the_slave_trader|plyr, "ramun_introduce_7", [], "Where do the slaves come from?", "ramun_introduce_8",[]],
[trp_ramun_the_slave_trader, "ramun_introduce_8", [], "Mostly I deal in convicted criminals bought from the authorities.\
Others are prisoners of war from various nations, brought to me because I offer the best prices.\
However, on occasion I'll buy from privateers and other . . . 'individuals'. You can't be picky about your suppliers in this line of work.\
You wouldn't happen to have any prisoners with you, would you?", "ramun_introduce_9",[]],
[trp_ramun_the_slave_trader|plyr, "ramun_introduce_9", [], "Me? ", "ramun_introduce_10",[]],
[trp_ramun_the_slave_trader, "ramun_introduce_10", [], "Why not? If you intend to set foot outside this town,\
you're going to cross swords with someone sooner or later. And, God willing, you'll come out on top.\
Why not make some extra money off the whole thing? Take them alive, bring them back to me, and I'll pay you fifty mon for each head.\
Don't much care who they are or where they come from.", "ramun_introduce_11",[]],
[trp_ramun_the_slave_trader|plyr, "ramun_introduce_11", [], "Hmm. I'll think about it.", "ramun_introduce_12",[]],
[trp_ramun_the_slave_trader, "ramun_introduce_12", [], "Do think about it!\
There's a lot of silver to be made, no mistake. More than enough for the both of us.", "close_window",[]],
[trp_ramun_the_slave_trader,"ramun_pre_talk", [], "Anything else?", "ramun_talk",[]],
[trp_ramun_the_slave_trader|plyr,"ramun_talk",
[[store_num_regular_prisoners,reg(0)],[ge,reg(0),1]],
"I've brought you some prisoners, Tuo-yi. Would you like a look?", "ramun_sell_prisoners",[]],
[trp_ramun_the_slave_trader|plyr,"ramun_talk",
   [(store_num_regular_prisoners,reg0),(ge,reg0,1)],
   "I want to sell all the prisoners I have with me.", "ramun_sell_prisoners_all",[]],
[trp_ramun_the_slave_trader,"ramun_sell_prisoners_all", [
  (store_num_regular_prisoners,reg0),
  (store_mul, reg1, reg0, 50),
  (store_sub, reg2, reg0, 1),
  ],
  "I'll take your {reg0} {reg2?prisoners:prisoner} off your hands for {reg1} mon.  We have a deal?", "ramun_sell_prisoners_all_2", []],
[trp_ramun_the_slave_trader|plyr,"ramun_sell_prisoners_all_2", [],
   "We have a deal.", "ramun_sell_prisoners_2", [
	(call_script, "script_dplmc_sell_all_prisoners", 1, 50),]
  ],
[trp_ramun_the_slave_trader|plyr,"ramun_sell_prisoners_all_2", [],
   "Let me think about it again.", "ramun_pre_talk",[]],
[trp_ramun_the_slave_trader,"ramun_sell_prisoners", [],
"Let me see what you have...", "ramun_sell_prisoners_2",
[[change_screen_trade_prisoners]]],
[trp_ramun_the_slave_trader, "ramun_sell_prisoners_2", [], "A pleasure doing business with you.", "close_window",[]],
[trp_ramun_the_slave_trader|plyr,"ramun_talk", [(neg|troop_slot_ge,"$g_talk_troop",slot_troop_met_previously,1)], "How do I take somebody as prisoner?", "ramun_ask_about_capturing",[]],
[trp_ramun_the_slave_trader|plyr,"ramun_talk", [(troop_slot_ge,"$g_talk_troop", slot_troop_met_previously, 1)], "Can you tell me again about capturing prisoners?", "ramun_ask_about_capturing",[(troop_set_slot,"$g_talk_troop", slot_troop_met_previously, 2)]],
[trp_ramun_the_slave_trader,"ramun_ask_about_capturing", [(neg|troop_slot_ge,"$g_talk_troop",slot_troop_met_previously,1)],
"You're new to this, aren't you? Let me explain it in simple terms.\
The basic rule of taking someone prisoner is knocking him down with a blunt weapon, like a mace or a club,\
rather than cutting him open with a sword. That way he goes to sleep for a little while rather than bleeding to death, you see?\
I'm assuming you have a blunt weapon with you . . .", "ramun_have_blunt_weapon",[]],
[trp_ramun_the_slave_trader|plyr,"ramun_have_blunt_weapon", [],
"Of course.", "ramun_have_blunt_weapon_yes",[]],
[trp_ramun_the_slave_trader|plyr,"ramun_have_blunt_weapon", [],
"As a matter of fact, I don't.", "ramun_have_blunt_weapon_no",[]],
[trp_ramun_the_slave_trader,"ramun_have_blunt_weapon_yes", [],
"Good. Then all you need to do is beat the bugger down with your weapon, and when the fighting's over you clap him in irons.\
It's a bit different for samurai and such, they tend to be protected enough that it won't matter what kind of weapon you use,\
but your average rabble-rouser will bleed like a stuck pig if you get him with something sharp. I don't have many requirements in my merchandise,\
but I do insist they be breathing when I buy them.", "ramun_ask_about_capturing_2",[]],
[trp_ramun_the_slave_trader,"ramun_have_blunt_weapon_no", [],
"No? Heh, well, this must be your lucky day. I've got an old club lying around that I was going to throw away.\
It a bit battered, but still good enough bash someone until he stops moving.\
Here, have it.","ramun_have_blunt_weapon_no_2",[(troop_add_item, "trp_player","itm_club",imod_cracked)]],
[trp_ramun_the_slave_trader|plyr,"ramun_have_blunt_weapon_no_2", [],
"Thanks, Tuo-yi. Perhaps I may try my hand at it.", "ramun_have_blunt_weapon_yes",[]],
[trp_ramun_the_slave_trader,"ramun_ask_about_capturing", [],
"Alright, I'll try and expain it again in simple terms. The basic rule of taking someone prisoner is knocking him down with a blunt weapon, like a mace or a club,\
rather than cutting him open with a sword. That way he goes to sleep for a little while rather than bleeding to death, you see?\
It's a bit different for samurai and such, they tend to be protected enough that it won't matter what kind of weapon you use,\
but your average rabble-rouser will bleed like a stuck pig if you get him with something sharp.", "ramun_ask_about_capturing_2",[]],
[trp_ramun_the_slave_trader|plyr,"ramun_ask_about_capturing_2", [], "Alright, I think I understand. Anything else?", "ramun_ask_about_capturing_3",[]],
[trp_ramun_the_slave_trader,"ramun_ask_about_capturing_3", [],
"Well, it's not as simple as all that. Blunt weapons don't do as much damage as sharp ones, so they won't bring your enemies down as quickly.\
And trust me, given the chance, most of the scum you run across would just as soon kill you as look at you, so don't expect any courtesy when you pull out a club instead of a sword.\
Moreover, having to drag prisoners to and fro will slow down your party, which is why some people simply set their prisoners free after the fighting's done.\
It's madness. How could anyone turn down all that silver, eh?", "ramun_ask_about_capturing_4",[]],
[trp_ramun_the_slave_trader|plyr,"ramun_ask_about_capturing_4", [],
"Is that everything?", "ramun_ask_about_capturing_5",[]],
[trp_ramun_the_slave_trader,"ramun_ask_about_capturing_5", [],
"Just one final thing. Managing prisoners safely is not an easy thing to do, you could call it a skill in itself.\
If you want to capture a lot of prisoners, you should try and learn the tricks of it yourself,\
or you won't be able to hang on to a single man you catch.", "ramun_ask_about_capturing_7",[]],
[trp_ramun_the_slave_trader|plyr,"ramun_ask_about_capturing_7", [],
"Thanks, I'll keep it in mind.", "ramun_pre_talk",[]],
[trp_ramun_the_slave_trader|plyr,"ramun_talk", [], "I'd better be going.", "ramun_leave",[]],
[trp_ramun_the_slave_trader,"ramun_leave", [], "Remember, any prisoners you've got, bring them to me. I'll pay you good silver for every one.", "close_window",[]],
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
[anyone, "tavern_mercenary_cant_lead", [], "That's a pity. Well, {reg3?we will:I will} be lingering around here for a while,\
 if you need to hire anyone.", "close_window", []],
[anyone|plyr,"merchant_ask_for_debts", [[store_troop_gold,reg(5),"trp_player"],[ge,reg(5),"$debt_to_merchants_guild"]],
   "Alright. I'll pay my debt to you.", "merchant_debts_paid",[[troop_remove_gold, "trp_player","$debt_to_merchants_guild"],
                                                                [assign,"$debt_to_merchants_guild",0]]],
[anyone, "merchant_debts_paid", [], "Excellent. I'll let my fellow merchants know that you are clear of any debts.", "mayor_pretalk",[]],
[anyone|plyr, "merchant_ask_for_debts", [], "I'm afraid I can't pay that sum now.", "merchant_debts_not_paid",[]],
[anyone, "merchant_debts_not_paid", [(assign,reg(1),"$debt_to_merchants_guild")], "In that case, I am afraid, I can't deal with you. Guild rules...\
 Come back when you can pay the {reg1} mon.\
 And know that we'll be charging an interest to your debt.\
 So the sooner you pay it, the better.", "close_window",[]],
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
[anyone,"sell_prisoner_outlaws", [[store_troop_kind_count,0,"trp_looter"],[ge,reg(0),1],[assign,reg(1),reg(0)],[val_mul,reg(1),10],[val_mul,reg(2),reg(0)],[val_mul,reg(2),10]],
   "Hmmm. 10 mon for each looter makes {reg1} mon for all {reg0} of them.", "sell_prisoner_outlaws",
   [[call_script, "script_troop_add_gold", "trp_player", reg(1)],[add_xp_to_troop,reg(2)],[remove_member_from_party,"trp_looter"]]],
[anyone,"sell_prisoner_outlaws", [[store_troop_kind_count,0,"trp_bandit"],[ge,reg(0),1],[assign,reg(1),reg(0)],[val_mul,reg(1),20],[assign,reg(2),reg(0)],[val_mul,reg(2),20]],
   "Let me see. You've brought {reg0} bandits, so 20 mon for each comes up to {reg1} mon.", "sell_prisoner_outlaws",
   [[call_script, "script_troop_add_gold", "trp_player", reg(1)],[add_xp_to_troop,reg(2)],[remove_member_from_party,"trp_bandit"]]],
[anyone,"sell_prisoner_outlaws", [[store_troop_kind_count,0,"trp_brigand"],[ge,reg(0),1],[assign,reg(1),reg(0)],[val_mul,reg(1),30],[assign,reg(2),reg(0)],[val_mul,reg(2),30]],
   "Well well, you've captured {reg0} brigands. Each one is worth 30 mon, so I'll give you {reg1} for them in total.", "sell_prisoner_outlaws",
   [[call_script, "script_troop_add_gold", "trp_player", reg(1)],[add_xp_to_troop,reg(2)],[remove_member_from_party,"trp_brigand"]]],
[anyone,"sell_prisoner_outlaws", [], "I suppose that'll be all, then.", "close_window",[]],
[anyone,"trade_requested_weapons", [(call_script,"script_dplmc_print_subordinate_says_sir_madame_to_s0"),], "Ah, yes {s0}. These arms are the best you'll find anywhere.", "merchant_trade",[[change_screen_trade]]],
[anyone,"trade_requested_armor", [(call_script,"script_dplmc_print_subordinate_says_sir_madame_to_s0"),], "Of course, {s0}. You won't find better quality armour than these in all Japan.", "merchant_trade",[[change_screen_trade]]],
[anyone,"trade_requested_horse", [(call_script,"script_dplmc_print_subordinate_says_sir_madame_to_s0"),], "You have a fine eye for horses, {s0}. You won't find better beasts than these anywhere else.", "merchant_trade",[[change_screen_trade]]],
[anyone,"merchant_trade", [], "Anything else?", "town_merchant_talk",[]],
[anyone,"merchant_gossip", [], "Well, nothing new lately. Prices, weather, the war, the same old things.", "town_merchant_talk",[]],
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
]
