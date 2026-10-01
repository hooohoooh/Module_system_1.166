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

dialogs_town_governance = [
[anyone|plyr,"village_farmer_talk",
[(check_quest_active, "qst_track_down_bandits"),
(neg|check_quest_succeeded, "qst_track_down_bandits"),

], "I am hunting a group of bandits with the following description... Have you seen them?", "farmer_bandit_information",[]],
[anyone|plyr,"village_farmer_talk",
[
(store_faction_of_party, ":faction_of_villager", "$g_encountered_party"),

(neq, ":faction_of_villager", "$players_kingdom"),
(neq, ":faction_of_villager", "fac_player_supporters_faction"),
],
"We'll see how poor you are after I take what you've got!", "close_window",
[(party_get_slot, ":home_center", "$g_encountered_party", slot_party_home_center),
(party_get_slot, ":market_town", ":home_center", slot_village_market_town),
(party_get_slot, ":village_owner", ":home_center", slot_town_lord),
(call_script, "script_change_player_relation_with_center", ":home_center", -4),
(call_script, "script_change_player_relation_with_center", ":market_town", -2),
(call_script, "script_change_player_relation_with_troop", ":village_owner", -2),
(call_script, "script_diplomacy_party_attacks_neutral", "p_main_party", "$g_encountered_party"),

(store_relation,":rel", "$g_encountered_party_faction","fac_player_supporters_faction"),
(try_begin),
(gt, ":rel", 0),
(val_sub, ":rel", 5),
(try_end),

(val_sub, ":rel", 3),
(call_script, "script_set_player_relation_with_faction", "$g_encountered_party_faction", ":rel"),

(assign,"$encountered_party_hostile",1),
(assign,"$encountered_party_friendly",0),
]],
[anyone|plyr,"village_farmer_talk", [], "Carry on, then. Farewell.", "close_window",[(assign, "$g_leave_encounter",1)]],
  [anyone,"mayor_begin", [(check_quest_active, "qst_persuade_lords_to_make_peace"),
                          (quest_slot_eq, "qst_persuade_lords_to_make_peace", slot_quest_giver_troop, "$g_talk_troop"),
                          (check_quest_succeeded, "qst_persuade_lords_to_make_peace"),
                          (quest_get_slot, ":quest_target_troop", "qst_persuade_lords_to_make_peace", slot_quest_target_troop),
                          (quest_get_slot, ":quest_object_troop", "qst_persuade_lords_to_make_peace", slot_quest_object_troop),
                          (val_mul, ":quest_target_troop", -1),
                          (val_mul, ":quest_object_troop", -1),
                          (quest_get_slot, ":quest_target_faction", "qst_persuade_lords_to_make_peace", slot_quest_target_faction),
                          (quest_get_slot, ":quest_object_faction", "qst_persuade_lords_to_make_peace", slot_quest_object_faction),
                          (str_store_troop_name, s12, ":quest_target_troop"),
                          (str_store_troop_name, s13, ":quest_object_troop"),
                          (str_store_faction_name, s14, ":quest_target_faction"),
                          (str_store_faction_name, s15, ":quest_object_faction"),
                          (str_store_party_name, s19, "$current_town"),
                         ],
   "{playername}, it was an incredible feat to get {s14} and {s15} make peace, and you made it happen.\
 Your involvement has not only saved our town from disaster, but it has also saved thousands of lives, and put an end to all the grief this bitter war has caused.\
 As the townspeople of {s19}, know that we'll be good on our word, and we are ready to pay the {reg12} mon we promised.", "lord_persuade_lords_to_make_peace_completed",
   [(quest_get_slot, ":quest_target_faction", "qst_persuade_lords_to_make_peace", slot_quest_target_faction),
    (quest_get_slot, ":quest_object_faction", "qst_persuade_lords_to_make_peace", slot_quest_object_faction),
    #Forcing 2 factions to make peace within 72 hours.
    (assign, "$g_force_peace_faction_1", ":quest_target_faction"),
    (assign, "$g_force_peace_faction_2", ":quest_object_faction"),
    (quest_get_slot, ":quest_reward", "qst_persuade_lords_to_make_peace", slot_quest_gold_reward),
    (assign, reg12, ":quest_reward"),
    #TODO: Change these values
    (add_xp_as_reward, 4000),
    ]],
  [anyone,"mayor_begin", [(check_quest_active, "qst_deal_with_night_bandits"),
                          (quest_slot_eq, "qst_deal_with_night_bandits", slot_quest_giver_troop, "$g_talk_troop"),
                          (check_quest_succeeded, "qst_deal_with_night_bandits"),
                         ],
   "Very nice work, {playername}, you made short work of those lawless curs.\
 Thank you kindly for all your help, and please accept this bounty of 150 mon.", "lord_deal_with_night_bandits_completed",
   [
     (add_xp_as_reward,200),
     (call_script, "script_troop_add_gold", "trp_player", 150),
     (call_script, "script_change_player_relation_with_center", "$current_town", 1),
     (call_script, "script_end_quest", "qst_deal_with_night_bandits"),
    ]],
# Ryan BEGIN
  [anyone,"mayor_begin", [(check_quest_active, "qst_deal_with_looters"),
                          (quest_slot_eq, "qst_deal_with_looters", slot_quest_giver_troop, "$g_talk_troop"),
                         ],
   "Ah, {playername}. Have you any progress to report?", "mayor_looters_quest_response",
   [
    ]],
  [anyone|plyr,"mayor_looters_quest_response",
   [
     (store_num_parties_destroyed_by_player, ":num_looters_destroyed", "pt_looters"),
     (party_template_get_slot,":previous_looters_destroyed","pt_looters",slot_party_template_num_killed),
     (val_sub,":num_looters_destroyed",":previous_looters_destroyed"),
     (quest_get_slot,":looters_paid_for","qst_deal_with_looters",slot_quest_current_state),
     (lt,":looters_paid_for",":num_looters_destroyed"),
     ],
   "I've killed some looters.", "mayor_looters_quest_destroyed",[]],
  [anyone|plyr,"mayor_looters_quest_response", [(eq,1,0)
  ],
   "I've brought you some goods.", "mayor_looters_quest_goods",[]],
  [anyone|plyr,"mayor_looters_quest_response", [
  ],
   "Not yet, sir. Farewell.", "close_window",[]],
  [anyone,"mayor_looters_quest_destroyed", [],
   "Aye, my scouts saw the whole thing. That should make anyone else think twice before turning outlaw!\
 The bounty is 40 mon for every band, so that makes {reg1} in total. Here is your money, as promised.",
   "mayor_looters_quest_destroyed_2",[
      (store_num_parties_destroyed_by_player, ":num_looters_destroyed", "pt_looters"),
      (party_template_get_slot,":previous_looters_destroyed","pt_looters",slot_party_template_num_killed),
      (val_sub,":num_looters_destroyed",":previous_looters_destroyed"),
      (quest_get_slot,":looters_paid_for","qst_deal_with_looters",slot_quest_current_state),
      (store_sub,":looter_bounty",":num_looters_destroyed",":looters_paid_for"),
      (val_mul,":looter_bounty",40),
      (assign,reg1,":looter_bounty"),
      (call_script, "script_troop_add_gold", "trp_player", ":looter_bounty"),
      (assign,":looters_paid_for",":num_looters_destroyed"),
      (quest_set_slot,"qst_deal_with_looters",slot_quest_current_state,":looters_paid_for"),
      ]],
  [anyone,"mayor_looters_quest_destroyed_2", [
      (quest_get_slot,":total_looters","qst_deal_with_looters",slot_quest_target_amount),
      (quest_slot_ge,"qst_deal_with_looters",slot_quest_current_state,":total_looters"), # looters paid for >= total looters
      (quest_get_slot,":xp_reward","qst_deal_with_looters",slot_quest_xp_reward),
      (quest_get_slot,":gold_reward","qst_deal_with_looters",slot_quest_gold_reward),
      (add_xp_as_reward, ":xp_reward"),
      (call_script, "script_troop_add_gold", "trp_player", ":gold_reward"),
      (call_script, "script_change_troop_renown", "trp_player", 1),
      (call_script, "script_change_player_relation_with_center", "$current_town", 5),
      (call_script, "script_end_quest", "qst_deal_with_looters"),
      (try_for_parties, ":cur_party_no"),
        (party_get_template_id, ":cur_party_template", ":cur_party_no"),
        (eq, ":cur_party_template", "pt_looters"),
        (party_set_flags, ":cur_party_no", pf_quest_party, 0),
      (try_end),
  ],
   "And that's not the only good news! Thanks to you, the looters have ceased to be a threat. We've not had a single attack reported for some time now.\
   If there are any of them left, they've either run off or gone deep into hiding. That's good for business,\
   and what's good for business is good for the town!\
   I think that concludes our arrangement, {playername}. Please accept this silver as a token of my gratitude. Thank you, and farewell.",
   "close_window",[
      ]],
  [anyone,"mayor_looters_quest_destroyed_2", [],
   "Anything else you need?",
   "mayor_looters_quest_response",[
      ]],
  [anyone,"mayor_looters_quest_goods", [
      (quest_get_slot,reg1,"qst_deal_with_looters",slot_quest_target_item),
  ],
   "Hah, I knew I could count on you! Just tell me which item to take from your baggage, and I'll send some men to collect it.\
 I still need {reg1} mon' worth of goods.",
   "mayor_looters_quest_goods_response",[
      ]],
  [anyone|plyr|repeat_for_100,"mayor_looters_quest_goods_response", [
      (store_repeat_object,":goods"),
      (val_add,":goods",trade_goods_begin),
      (is_between,":goods",trade_goods_begin,trade_goods_end),
      (player_has_item,":goods"),
      (str_store_item_name,s5,":goods"),
  ],
   "{s5}.", "mayor_looters_quest_goods_2",[
      (store_repeat_object,":goods"),
      (val_add,":goods",trade_goods_begin),
      (troop_remove_items,"trp_player",":goods",1),
      (assign,":value",reg0),
      (call_script, "script_troop_add_gold", "trp_player", ":value"),
      (quest_get_slot,":gold_num","qst_deal_with_looters",slot_quest_target_item),
      (val_sub,":gold_num",":value"),
      (quest_set_slot,"qst_deal_with_looters",slot_quest_target_item,":gold_num"),
      (str_store_item_name,s6,":goods"),
   ]],
  [anyone|plyr,"mayor_looters_quest_goods_response", [
  ],
   "Nothing at the moment, sir.", "mayor_looters_quest_goods_3",[]],
  [anyone,"mayor_looters_quest_goods_3", [
  ],
   "Anything else you need?",
   "mayor_looters_quest_response",[
      ]],
  [anyone,"mayor_looters_quest_goods_2", [
      (quest_slot_ge,"qst_deal_with_looters",slot_quest_target_item,1),
      (quest_get_slot,reg1,"qst_deal_with_looters",slot_quest_target_item),
  ],
   "Excellent, here is the money for your {s6}. Do you have any more goods to give me? I still need {reg1} mon' worth of goods.",
   "mayor_looters_quest_goods_response",[
      ]],
  [anyone,"mayor_looters_quest_goods_2", [
      (neg|quest_slot_ge,"qst_deal_with_looters",slot_quest_target_item,1),
      (quest_get_slot,":xp_reward","qst_deal_with_looters",slot_quest_xp_reward),
      (quest_get_slot,":gold_reward","qst_deal_with_looters",slot_quest_gold_reward),
      (add_xp_as_reward, ":xp_reward"),
      (call_script, "script_troop_add_gold", "trp_player", ":gold_reward"),
#      (call_script, "script_change_troop_renown", "trp_player", 1),
      (call_script, "script_change_player_relation_with_center", "$current_town", 3),
      (call_script, "script_end_quest", "qst_deal_with_looters"),
      (try_for_parties, ":cur_party_no"),
        (party_get_template_id, ":cur_party_template", ":cur_party_no"),
        (eq, ":cur_party_template", "pt_looters"),
        (party_set_flags, ":cur_party_no", pf_quest_party, 0),
      (try_end),
  ],
   "Well done, {playername}, that's the last of the goods I need. Here is the money for your {s6}, and a small bonus for helping me out.\
 I'm afraid I won't be paying for any more goods, nor bounties on looters, but you're welcome to keep hunting the bastards if any remain.\
 Thank you for your help, I won't forget it.",
   "close_window",[
      ]],
# Ryan END



  [anyone,"mayor_begin", [(check_quest_active, "qst_move_cattle_herd"),
                          (quest_slot_eq, "qst_move_cattle_herd", slot_quest_giver_troop, "$g_talk_troop"),
                          (check_quest_succeeded, "qst_move_cattle_herd"),
                          ],
   "Good to see you again {playername}. I have heard that you have delivered the cattle successfully.\
 I will tell the merchants how reliable you are.\
 And here is your pay, {reg8} mon.", "close_window",
   [(quest_get_slot, ":quest_gold_reward", "qst_move_cattle_herd", slot_quest_gold_reward),
    (call_script, "script_troop_add_gold", "trp_player", ":quest_gold_reward"),
    (store_div, ":xp_reward", ":quest_gold_reward", 3),
    (add_xp_as_reward, ":xp_reward"),
    (call_script, "script_change_troop_renown", "trp_player", 1),
    (call_script, "script_change_player_relation_with_center", "$current_town", 3),
    (call_script, "script_end_quest", "qst_move_cattle_herd"),
    (assign, reg8, ":quest_gold_reward"),
    ]],
  [anyone,"mayor_begin", [(check_quest_active, "qst_move_cattle_herd"),
                          (quest_slot_eq, "qst_move_cattle_herd", slot_quest_giver_troop, "$g_talk_troop"),
                          (check_quest_failed, "qst_move_cattle_herd"),
                          ],
   "I heard that you have lost the cattle herd on your way to {s9}.\
 I had a very difficult time explaining your failure to the owner of that herd, {sir/madam}.\
 Do you have anything to say?", "move_cattle_herd_failed",
   []],
  [anyone,"mayor_begin", [(check_quest_active, "qst_kidnapped_girl"),
                          (quest_slot_eq, "qst_kidnapped_girl", slot_quest_current_state, 4),
                          (quest_slot_eq, "qst_kidnapped_girl", slot_quest_giver_troop, "$g_talk_troop"),
                          ],
   "{playername} -- I am in your debt for bringing back my friend's daughter.\
  Please take these {reg8} mon that I promised you.\
  My friend wished he could give more but paying that ransom brought him to his knees.", "close_window",
   [(quest_get_slot, ":quest_gold_reward", "qst_kidnapped_girl", slot_quest_gold_reward),
    (call_script, "script_troop_add_gold", "trp_player", ":quest_gold_reward"),
    (assign, reg8, ":quest_gold_reward"),
    (assign, ":xp_reward", ":quest_gold_reward"),
    (val_mul, ":xp_reward", 2),
    (val_add, ":xp_reward", 100),
    (add_xp_as_reward, ":xp_reward"),
    (call_script, "script_change_troop_renown", "trp_player", 3),
    (call_script, "script_change_player_relation_with_center", "$current_town", 2),
    (call_script, "script_end_quest", "qst_kidnapped_girl"),
    ]],
  [anyone,"mayor_begin", [(check_quest_active, "qst_track_down_bandits"),
                          (check_quest_succeeded, "qst_track_down_bandits"),
                          (quest_slot_eq, "qst_track_down_bandits", slot_quest_giver_troop, "$g_talk_troop"),
                          ],
   "Well -- it sounds like you were able to track down the bandits, and show them what happens to those who would disrupt the flow of commerce.\
 Here is your reward: {reg5} mon.\
 It is well earned, and we are most grateful.",
   "mayor_friendly_pretalk", [(quest_get_slot, ":quest_gold_reward", "qst_track_down_bandits", slot_quest_gold_reward),
                              (call_script, "script_troop_add_gold", "trp_player", ":quest_gold_reward"),
                              (assign, ":xp_reward", ":quest_gold_reward"),
                              (val_mul, ":xp_reward", 2),
                              (add_xp_as_reward, ":xp_reward"),
                              (call_script, "script_change_player_relation_with_center", "$current_town", 2),
                              (call_script, "script_change_troop_renown", "trp_player", 3),
                              (call_script, "script_end_quest", "qst_track_down_bandits"),
                              (assign, reg5, ":quest_gold_reward"),
                              ]],
  [anyone,"mayor_begin", [(check_quest_active, "qst_troublesome_bandits"),
                          (check_quest_succeeded, "qst_troublesome_bandits"),
                          (quest_slot_eq, "qst_troublesome_bandits", slot_quest_giver_troop, "$g_talk_troop"),
                          ],
   "I have heard about your deeds. You have given those bandits the punishment they deserved.\
 You are really as good as they say.\
 Here is your reward: {reg5} mon.\
 I would like to give more but those bandits almost brought me to bankruptcy.",
   "mayor_friendly_pretalk", [(quest_get_slot, ":quest_gold_reward", "qst_troublesome_bandits", slot_quest_gold_reward),
                              (call_script, "script_troop_add_gold", "trp_player", ":quest_gold_reward"),
                              (assign, ":xp_reward", ":quest_gold_reward"),
                              (val_mul, ":xp_reward", 2),
                              (add_xp_as_reward, ":xp_reward"),
                              (call_script, "script_change_player_relation_with_center", "$current_town", 2),
                              (call_script, "script_change_troop_renown", "trp_player", 3),
                              (call_script, "script_end_quest", "qst_troublesome_bandits"),
                              (assign, reg5, ":quest_gold_reward"),
                              ]],
  #destroy lair quest end dialogs taken from here

  [anyone,"mayor_begin", [(ge, "$debt_to_merchants_guild", 50)],
   "According to my accounts, you owe the merchants guild {reg1} mon.\
 I'd better collect that now.", "merchant_ask_for_debts",[(assign,reg(1),"$debt_to_merchants_guild")]],
  [anyone,"mayor_begin", [], "What can I do for you?", "mayor_talk", []],
  [anyone,"mayor_friendly_pretalk", [], "Now... What else may I do for you?", "mayor_talk",[]],
  [anyone,"mayor_pretalk", [], "Yes?", "mayor_talk",[]],
  [anyone|plyr,"mayor_talk", [], "Can you tell me about what you do?", "mayor_info_begin",[]],
  [anyone|plyr,"mayor_talk", [(store_partner_quest, ":partner_quest"),
                              (lt, ":partner_quest", 0),
                              (neq, "$merchant_quest_last_offerer", "$g_talk_troop")],
   "Do you happen to have a special job for me?", "merchant_quest_requested",[
     (assign,"$merchant_quest_last_offerer", "$g_talk_troop"),
     (call_script, "script_get_quest", "$g_talk_troop"),
     (assign, "$random_merchant_quest_no", reg0),
     (assign,"$merchant_offered_quest","$random_merchant_quest_no"),
     ]],
  [anyone|plyr,"mayor_talk", [(store_partner_quest, ":partner_quest"),
                              (lt, ":partner_quest", 0),
                              (eq,"$merchant_quest_last_offerer", "$g_talk_troop"),
                              (gt,"$merchant_offered_quest", 0) #not sure why was zero
                              ],
   "About that special job you offered me...", "merchant_quest_last_offered_job",[]],
  [anyone|plyr,"mayor_talk", [(store_partner_quest,reg(2)),(ge,reg(2),0)],
   "About the special job you gave me...", "merchant_quest_about_job",[]],
  
  #gekokujo 3.1 labor start
  [anyone|plyr,"mayor_talk", 
    [
      (party_get_num_companions, ":num_companions", "p_main_party"),
      (try_begin),
        (gt, ":num_companions", 2),
        (str_store_string, s10, "str_gekokujo_labor_town_ask_2"), #plural
      (else_try),
        (str_store_string, s10, "str_gekokujo_labor_town_ask_1"), #singular
      (try_end),
    ],
    "{s10}", "mayor_labor_answer", []],
    
  [anyone,"mayor_labor_answer", 
    [
      (troop_get_slot, ":renown", "trp_player", slot_troop_renown),
      (try_begin),
        (gt, "$players_kingdom", 0), #a lord
        (str_store_string, s11, "str_gekokujo_labor_town_answer_lord"),
      (else_try),
        (ge, ":renown", 100), #renowned
        (str_store_string, s11, "str_gekokujo_labor_town_answer_renowned"),
      (else_try),
        #a commoner
        (str_store_string, s11, "str_gekokujo_labor_town_answer_normal"),
      (try_end),
    ],
    "{s11}", "mayor_labor_decision", []],
    
  [anyone|plyr,"mayor_labor_decision", [], "That sounds good to me.", "close_window", 
    [
      (jump_to_menu, "mnu_labor"),
      (finish_mission),
    ]],
    
  [anyone|plyr,"mayor_labor_decision", [], "Actually, nevermind.", "mayor_pretalk", []],
  #gekokujo 3.1 labor end

  [anyone|plyr,"mayor_talk",[], "I have some questions of a political nature.", "mayor_political_talk",[]],
  [anyone|plyr,"mayor_talk",[], "How is trade around here?", "mayor_economy_report_1",[
  (call_script, "script_merchant_road_info_to_s42", "$g_encountered_party"), #also does items to s32
  ]],
  [anyone|plyr,"mayor_talk",[
  ], "How does the wealth of this region compare with the rest of Japan?", "mayor_wealth_comparison_1",[
  ]],
  [anyone|plyr,"mayor_talk",[
  (item_slot_ge, "itm_velvet", slot_item_secondary_raw_material, "itm_raw_dyes"), #ie, the item information has been updated, to ensure savegame compatibility
  ], "I wish to join the local guild and establish myself as a merchant", "mayor_investment_possible",[
  ]],
  [anyone,"mayor_investment_possible",[
  (party_slot_ge, "$g_encountered_party", slot_center_player_enterprise, 1),
  (party_get_slot, ":item_produced", "$g_encountered_party", slot_center_player_enterprise),
  (call_script, "script_get_enterprise_name", ":item_produced"),
  (str_store_string, s4, reg0),
  ], "But you already operate a {s4} here. The other merchant and craftsmen would be scandalized, I am sorry.", "mayor_pretalk",[
  ]],
  [anyone,"mayor_investment_possible",[
  (ge, "$cheat_mode", 3)
  ], "{!}CHEAT: Yes, we're playtesting this feature, and you're in cheat mode. Go right ahead.", "mayor_investment_advice",[
  ]],
  [anyone,"mayor_investment_possible",[
  (lt,"$g_encountered_party_relation",0),
  (str_store_string, s9, "str_enterprise_enemy_realm"),
	], "{s9}", "mayor_pretalk",[
	]],
  [anyone,"mayor_investment_possible",[
  (party_slot_eq, "$g_encountered_party", slot_town_lord, "trp_player"),
  ##diplomacy start+ Replace {sir/my lady} with {s0}
  (call_script, "script_dplmc_print_subordinate_says_sir_madame_to_s0"),
#  ], "Of course, {sir/my lady}. You are the lord of this town, and no one is going to stop you.", "mayor_investment_advice",[
  ], "Of course, {lord/lady} {s0}. Though it is a bit strange to see a samurai take interest in our kind of work.", "mayor_investment_advice",[
##diplomacy end+
  ]],
  [anyone,"mayor_investment_possible",[
  (party_get_slot, ":town_liege", "$g_encountered_party", slot_town_lord),
  ##diplomacy start+ Add support for ladies etc.
  #(is_between, ":town_liege", active_npcs_begin, active_npcs_end),
  (is_between, ":town_liege", heroes_begin, heroes_end),
  ##diplomacy end+
  (call_script, "script_troop_get_relation_with_troop", "trp_player", ":town_liege"),
  (assign, ":relation", reg0),
  (lt, ":relation", 0),
  (str_store_troop_name, s4, ":town_liege"),
  ], "Well... Given your relationship with our leader, {s4}, I think that you will not find many members of the guild who are brave enough to vote you in.", "mayor_investment",[
  ]],
  [anyone|auto_proceed,"mayor_investment",[], "{!}.", "mayor_pretalk",[]],
  [anyone,"mayor_investment_possible",[
  ##diplomacy start+ Optional economic change, increase relation required
  ##OLD:
  #	(neg|party_slot_ge, "$current_town", slot_center_player_relation, 0),
  ##NEW:
  #gekokujo 3.0 change merchant requirements start
  #(assign, ":required_relation", 0),#need 0+ normally
  (try_begin),
    (is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end), #player is a vassal
    (assign, ":required_relation", 0), #vassals need 1+ in gekokujo 3.0
  (else_try),
    (assign, ":required_relation", 5), #normally need 5+ in gekokujo 3.0
  (try_end),
  #gekokujo 3.0 change merchant requirements end
  (try_begin),
	(ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_MEDIUM),
	(neq, "$g_encountered_party", "$g_starting_town"),
	#(val_add, ":required_relation", 1),#need 1+ with economic changes on medium+
	(val_add, ":required_relation", 5),#need 15+ with economic changes on medium+ in gekokujo 3.0
  (try_end),
  (neg|party_slot_ge, "$current_town", slot_center_player_relation, ":required_relation"),
  ##diplomacy end+
  ], "Well... To be honest, I think that we in the guild would like you to build a stronger relationship with the town first. We can be very particular about outsiders coming in and joining us.", "mayor_pretalk",[
  ]],
  [anyone,"mayor_investment_possible",[
  ##diplomacy start+ Replace {sir/my lady} with {s0}
  (call_script, "script_dplmc_print_commoner_at_arg1_says_sir_madame_to_s0", "$g_encountered_party"),
#  ], "Very good, {sir/my lady}. We in the guild know and trust you, and I think I could find someone to sell you the land you need.", "mayor_investment_advice",[]],
  ], "Very good, {s0}. We in the guild know and trust you, and would be willing to make room for you.", "mayor_investment_advice",[]],
##diplomacy end+

  [anyone,"mayor_investment_advice",[], "A couple of things to keep in mind -- skilled laborers are always at a premium, so I doubt that you will be able to open up more than one business here. In order to make a profit for yourself, you should choose a commodity which is in relatively short supply, but for which the raw materials are cheap. What sort of shop would you like to start?", "investment_choose_enterprise",[
  ]],
  [anyone|plyr,"mayor_investment_confirm",[
  (store_troop_gold, ":player_gold", "trp_player"),
  (ge, ":player_gold","$enterprise_cost"),
  ], "Yes. Here is money for the land.", "mayor_investment_purchase",[
  (party_set_slot, "$g_encountered_party", slot_center_player_enterprise, "$enterprise_production"),
  (party_set_slot, "$g_encountered_party", slot_center_player_enterprise_days_until_complete, 7),

  (troop_remove_gold, "trp_player", "$enterprise_cost"),
  (store_sub, ":current_town_order", "$current_town", towns_begin),
  (store_add, ":craftsman_troop", ":current_town_order", "trp_town_1_master_craftsman"),
  (try_begin),
	(eq, "$enterprise_production", "itm_bread"),
    (troop_set_name, ":craftsman_troop", "str_master_miller"),
  (else_try),
	(eq, "$enterprise_production", "itm_ale"),
    (troop_set_name, ":craftsman_troop", "str_master_brewer"),
  (else_try),
	(eq, "$enterprise_production", "itm_oil"),
    (troop_set_name, ":craftsman_troop", "str_master_presser"),
  (else_try),
	(eq, "$enterprise_production", "itm_tools"),
    (troop_set_name, ":craftsman_troop", "str_master_smith"),
  (else_try),
	(eq, "$enterprise_production", "itm_wool_cloth"),
    (troop_set_name, ":craftsman_troop", "str_master_weaver"),
  (else_try),
	(eq, "$enterprise_production", "itm_linen"),
    (troop_set_name, ":craftsman_troop", "str_master_weaver"),
  (else_try),
	(eq, "$enterprise_production", "itm_leatherwork"),
    (troop_set_name, ":craftsman_troop", "str_master_tanner"),
  (else_try),
	(eq, "$enterprise_production", "itm_velvet"),
    (troop_set_name, ":craftsman_troop", "str_master_dyer"),
  (else_try),
	(eq, "$enterprise_production", "itm_wine"),
    (troop_set_name, ":craftsman_troop", "str_master_vinter"),
  (try_end),
  ]],
  [anyone|plyr,"mayor_investment_confirm",[], "No -- that's not economical for me at the moment.", "mayor_pretalk",[
  ]],
  [anyone,"mayor_investment_purchase",[], "Very good. Your shop should be up and running in about a week. When next you come, and thereafter, you should speak to your {s4} about its operations.", "mayor_pretalk",[
  (store_sub, ":current_town_order", "$current_town", towns_begin),
  (store_add, ":craftsman_troop", ":current_town_order", "trp_town_1_master_craftsman"),
  (str_store_troop_name, s4, ":craftsman_troop"),

  ]],
  [anyone|plyr,"mayor_talk", [], "[Leave]", "close_window",[]],
  [anyone, "mayor_info_begin", [(str_store_party_name, s9, "$current_town")],
   "I am the chief merchant of {s9}. You can say I am the leader of the commoners of {s9}.\
 I can help you find a job if you are looking for some honest work.", "mayor_info_talk",[(assign, "$mayor_info_lord_told",0)]],
  [anyone|plyr,"mayor_info_talk",[(eq, "$mayor_info_lord_told",0)], "Who rules this town?", "mayor_info_lord",[]],
  ##diplomacy start+ make gender correct
  [anyone, "mayor_info_lord", [(party_get_slot, ":town_lord","$current_town",slot_town_lord),(str_store_troop_name, s10, ":town_lord"),
  (call_script, "script_dplmc_store_troop_is_female", ":town_lord"),],#Next line, He -> {reg0?She:He}
   "Our town's lord and protector is {s10}. {reg0?She:He} owns the castle and sometimes resides there, and collects taxes from the town.\
 However we regulate ourselves in most of the matters that concern ourselves.\
 As the most elder merchant in the town, I have the privilege of speaking for the rest.", "mayor_info_talk",[(assign, "$mayor_info_lord_told",1)]],
 ##diplomacy end+

  [anyone|plyr,"mayor_info_talk",[], "That's all I need to know. Thanks.", "mayor_pretalk",[]],
  [anyone, "mayor_political_talk", [(faction_get_slot, ":faction_leader","$g_encountered_party_faction",slot_faction_leader),
									(str_store_troop_name, s10, ":faction_leader"),
									(party_get_slot, ":town_lord","$current_town",slot_town_lord),
									(try_begin),
										(eq, ":town_lord", "trp_player"),
										(str_store_string, s10, "str_your_excellency"),
									(else_try),
										(is_between, ":town_lord", active_npcs_begin, active_npcs_end),
										(neq, ":town_lord", ":faction_leader"),
										(str_store_troop_name, s11, ":town_lord"),
										(neq, ":town_lord", ":faction_leader"),
										(str_store_string, s10, "str_s10_and_s11"),
									(try_end),
									],
   "Politics? Good heaven, the guild has nothing to do with politics. We are loyal servants of {s10}. We merely govern our own affairs, and pass on the townspeople's concerns to our lords and masters, and maybe warn them from time to time against evil advice. Anyway, what did you wish to ask?", "mayor_political_questions",[]],
  [anyone,"mayor_prepolitics",[ (faction_get_slot, ":faction_leader","$g_encountered_party_faction",slot_faction_leader),
								(try_begin),
									(eq, ":faction_leader", "trp_player"),
									(str_store_string, s9, "str_your_loyal_subjects"),
								(else_try),
									(str_store_troop_name, s10, ":faction_leader"),
									(str_store_string, s9, "str_loyal_subjects_of_s10"),
								(try_end),
  ], "Did I mention that we here are all {s9}? Because I can't stress that enough... Anyway... Is there anything else?", "mayor_political_questions",[]],
   [anyone|plyr,"mayor_political_questions",[], "What is the cause of all these wars in Japan?", "mayor_war_description_1",[
  ]],
  [anyone,"mayor_war_description_1",[ (faction_get_slot, ":faction_leader","$g_encountered_party_faction",slot_faction_leader),
								(str_store_troop_name, s10, ":faction_leader"),
								(str_store_string, s22, "str_the"),
								(try_begin),
									(eq, "$g_encountered_party_faction", "fac_kingdom_5"),
									(str_store_string, s22, "str_we"),
								(try_end),
								(val_max, "$g_mayor_given_political_dialog", 1),

  ], "Well, to answer your question generally, each daimyo claims to be the rightful holder to the office of old Muromachi shugo. In theory, any one realm has the right to declare war on any other realm at any time.", "mayor_war_description_2",[]],
  [anyone,"mayor_war_description_2",[ (faction_get_slot, ":faction_leader","$g_encountered_party_faction",slot_faction_leader),
								(str_store_troop_name, s10, ":faction_leader"),
								(troop_get_type, reg4, ":faction_leader"),
  ], "In practice, to make war is exhausting work. It is easy enough to lay waste to the enemy's farmland, but crops will grow back, and it is a far different matter to capture an enemy stronghold and to hold it. So the daimyo of Japan will fight a little, sign a truce, fight a little more, and so on and so forth. Often, a daimyo will go to war when another clan provokes them. At such times, some bad influences who look to enrich themselves with ransoms and pillage will clamor for retribution, and thus the damage caused by war to a monarch's treasury is less than the damage caused by doing nothing would be to his authority... I'm of course not talking about {s10}, as no one would ever question {reg4?her:his} authority", "mayor_war_description_3",[]],
  [anyone,"mayor_war_description_3",[
 	(faction_get_slot, ":faction_leader","$g_encountered_party_faction",slot_faction_leader),
	(troop_get_type, reg4, ":faction_leader"),

  ], "I would stress again that we in the guild have nothing to do with politics. But if {s10} were to ask for my advice on these matters, as a loyal subject, I would tell {reg4?her:him} that while {reg4?her:his} claim to all of Japan is truly just, even the most legitimate claim must be backed by armed men, and armed men want money, and money comes from trade, and war ruins trade, so sometimes the best way to push a claim is not to push it, if you know what I mean...", "mayor_war_description_4",[]],
  [anyone,"mayor_war_description_4",[
    (str_store_party_name, s4, "$g_encountered_party"),
	(faction_get_slot, ":faction_leader","$g_encountered_party_faction",slot_faction_leader),
	(troop_get_type, reg4, ":faction_leader"),

  ], "You may tell {s10} this if you see {reg4?her:him}. Don't mention my name specifically -- just say 'the people of {s4}' told you this. Our personal opinion, of course, as to what would be in {s10}'s best interests. None of us would ever dream of questioning a monarch's sovereign right to push {reg4?her:his} legitimate claims.", "mayor_prepolitics",[
  ]],
  [anyone|plyr,"mayor_political_questions",[
	(faction_get_slot, ":faction_leader","$g_encountered_party_faction",slot_faction_leader),
	(str_store_troop_name, s10, ":faction_leader"),
	(ge, "$g_mayor_given_political_dialog", 1),
	(assign, ":continue", 0),
	(try_for_range, ":cur_faction", kingdoms_begin, kingdoms_end),
	  (faction_slot_eq, ":cur_faction", slot_faction_state, sfs_active),
	  (neq, ":cur_faction", "$g_encountered_party_faction"),
	  (assign, ":continue", 1), #at least 1 faction is active
	(try_end),
	(eq, ":continue", 1),
  ], "What is {s10}'s policy in regards to the other domains of Japan?", "mayor_politics_assess",[
  ]],
  [anyone,"mayor_politics_assess",[], "Which domain did you have in mind?", "mayor_politics_assess_realm",[
  ]],
  [anyone|plyr|repeat_for_factions,"mayor_politics_assess_realm",[
  (store_repeat_object, ":faction"),
  (is_between, ":faction", kingdoms_begin, kingdoms_end),
  (faction_slot_eq, ":faction", slot_faction_state, sfs_active),
  (neq, ":faction", "$g_encountered_party_faction"),
  (str_store_faction_name, s11, ":faction"),
  ], "{s11}", "mayor_politics_give_realm_assessment",[
  (store_repeat_object, "$faction_selected"),
  ]],
  [anyone,"mayor_politics_give_realm_assessment",[], "{s14}", "mayor_prepolitics",[
  (call_script, "script_npc_decision_checklist_peace_or_war", "$g_encountered_party_faction", "$faction_selected", -1),
  ]],
   [anyone|plyr,"mayor_political_questions",[], "What can you say about the internal politics of the clans?", "mayor_internal_politics",[
  ]],
  [anyone,"mayor_internal_politics",[
  (str_store_faction_name, s4, "$g_encountered_party_faction"),
  (faction_get_slot, ":leader", "$g_encountered_party_faction", slot_faction_leader),
  (str_store_troop_name, s5, ":leader"),
  (troop_get_type, reg4, ":leader"),
  ], "Well, here in the {s4} we are all united by our love for {s5} and support for {reg4?her:his} legitimate claim to the rulership of all Japan. But I have heard some talk of internal bickering in other domains...", "mayor_internal_politics_2",[
  ]],
  [anyone,"mayor_internal_politics_2",[], "The hereditary vassals of a clan often have very different ideas about honor, strategy, and the way a samurai should behave. In addition, they compete with each other for the ruler's favor, and are constantly weighing up their position -- how they stand, how their friends and family stand, and how their enemies stand.", "mayor_internal_politics_3", []],
  [anyone,"mayor_internal_politics_3",[], "Underlying all the tensions is the possibility that a lord may abandon his leader, and pledge vassalhood to another. In theory, each lord has sworn an oath of vassalage, but in practice, a vassal can always find an excuse to absolve himself. The vassal may claim that the leader has failed to hold up his end of the bargain, to protect the vassal and treat him justly. Or, the vassal may claim that his leader is in fact a usurper, and another has a better claim to overlordship.", "mayor_internal_politics_4", []],
  [anyone,"mayor_internal_politics_4",[], "Overlords and vassals still watch each other carefully. If a daimyo believes that his vassal is going to change sides or rebel, he may indict the vassal for treason and seize his properties. Likewise, if a vassal fears that he will be indicted, he may rebel. Usually, whoever makes the first move will be able to control the vassal's fortresses.", "mayor_internal_politics_5", []],
  [anyone,"mayor_internal_politics_5",[], "Now, men do not trust a vassal who turns coat easily, nor do they trust an overlord who lightly throws around charges of treason. Those two factors can keep a domain together. But if relations between a vassal and an overlord deteriorates far enough, things can become very tense indeed... In other lands, of course. These things could never happen here in the {s4}.", "mayor_prepolitics", []],
  [anyone|plyr, "mayor_political_questions", [], "That is all. Thank you.", "mayor_pretalk", []],
  [anyone,"mayor_economy_report_1", [], "{s32}", "mayor_economy_report_2",
   []],
  [anyone,"mayor_economy_report_2", [], "{s42}", "mayor_economy_report_3",
   []],
   [anyone,"mayor_economy_report_3", [], "{s47}", "mayor_pretalk",
   []],
  [anyone,"village_elder_deliver_cattle_thank", [],
   "My good {lord/lady}, please, is there anything I can do for you?", "village_elder_talk",[]],
#replaced {sir/madam} with {s0}
  ##diplomacy end+

  [anyone ,"village_elder_pretalk", [],
   "Is there anything else I can do for you?", "village_elder_talk",[]],
  [anyone|plyr,"village_elder_talk", [(check_quest_active, "qst_hunt_down_fugitive"),
                                      (neg|check_quest_concluded, "qst_hunt_down_fugitive"),
                                      (quest_slot_eq, "qst_hunt_down_fugitive", slot_quest_target_center, "$current_town"),
                                      (quest_get_slot, ":quest_target_dna", "qst_hunt_down_fugitive", slot_quest_target_dna),
                                      (call_script, "script_get_name_from_dna_to_s50", ":quest_target_dna"),
                                      (str_store_string, s4, s50),
                                      ],
   "I am looking for a man by the name of {s4}. I was told he may be hiding here.", "village_elder_ask_fugitive",[]],
  [anyone ,"village_elder_ask_fugitive", [
  ##diplomacy start+
   (call_script, "script_dplmc_print_commoner_at_arg1_says_sir_madame_to_s0", "$current_town"),#added (used in next two)
   (is_currently_night),
   ],
   "Strangers come and go to our village, {s0}. But I doubt you'll run into him at this hour of the night. You would have better luck during the day.", "village_elder_pretalk",[]],
#changed {sir/madam} to {s0}
  [anyone ,"village_elder_ask_fugitive", [],
   "Strangers come and go to our village, {s0}. If he is hiding here, you will surely find him if you look around.", "close_window",[]],
#changed {sir/madam} to {s0}
  ##diplomacy end+

  [anyone|plyr,"village_elder_talk", [(store_partner_quest,":elder_quest"),(ge,":elder_quest",0)],
   "About the special task you asked of me...", "village_elder_active_mission_1",[]],
  [anyone|plyr,"village_elder_talk", [(ge, "$g_talk_troop_faction_relation", 0),(store_partner_quest,":elder_quest"),(lt,":elder_quest",0)],
   "Do you have any special tasks I can help you with?", "village_elder_request_mission_ask",[]],
   
  #gekokujo 3.1 labor start
  [anyone|plyr,"village_elder_talk", 
    [
      (party_get_num_companions, ":num_companions", "p_main_party"),
      (try_begin),
        (gt, ":num_companions", 2),
        (str_store_string, s10, "str_gekokujo_labor_village_ask_2"), #plural
      (else_try),
        (str_store_string, s10, "str_gekokujo_labor_village_ask_1"), #singular
      (try_end),
    ],
    "{s10}", "village_elder_labor_answer", []],
    
  [anyone,"village_elder_labor_answer", 
    [
      (troop_get_slot, ":renown", "trp_player", slot_troop_renown),
      (try_begin),
        (gt, "$players_kingdom", 0), #a lord
        (str_store_string, s11, "str_gekokujo_labor_village_answer_lord"),
      (else_try),
        (ge, ":renown", 100), #renowned
        (str_store_string, s11, "str_gekokujo_labor_village_answer_renowned"),
      (else_try),
        #a commoner
        (str_store_string, s11, "str_gekokujo_labor_village_answer_normal"),
      (try_end),
    ],
    "{s11}", "village_elder_labor_decision", []],
    
  [anyone|plyr,"village_elder_labor_decision", [], "That sounds good to me.", "close_window", 
    [
      (jump_to_menu, "mnu_labor"),
      (finish_mission),
    ]],
    
  [anyone|plyr,"village_elder_labor_decision", [], "Actually, nevermind.", "village_elder_pretalk", []],
  #gekokujo 3.1 labor end

  [anyone|plyr,"village_elder_talk", [(party_slot_eq, "$current_town", slot_village_state, 0),
                                      (neg|party_slot_ge, "$current_town", slot_village_infested_by_bandits, 1),],
   "I want to buy some supplies. I will pay with gold.", "village_elder_trade_begin",[]],
  [anyone ,"village_elder_trade_begin", [], "Of course, {sir/madam}. Do you want to buy goods or cattle?", "village_elder_trade_talk",[]],
  [anyone|plyr,"village_elder_trade_talk", [], "I want to buy food and supplies.", "village_elder_trade",[]],
  [anyone ,"village_elder_trade", [],
   "We have some food and other supplies in our storehouse. Come have a look.", "village_elder_pretalk",[(change_screen_trade, "$g_talk_troop"),]],
  [anyone|plyr,"village_elder_trade_talk", [(party_slot_eq, "$current_town", slot_village_state, 0),
                                      (neg|party_slot_ge, "$current_town", slot_village_infested_by_bandits, 1),
                                      (assign, ":quest_village", 0),
                                      (try_begin),
                                        (check_quest_active, "qst_deliver_cattle"),
                                        (quest_slot_eq, "qst_deliver_cattle", slot_quest_target_center, "$current_town"),
                                        (assign, ":quest_village", 1),
                                      (try_end),
                                      (eq, ":quest_village", 0),
                                      ],
   "I want to buy some cattle.", "village_elder_buy_cattle",[]],
  [anyone|plyr,"village_elder_trade_talk", [], "I changed my mind. I don't need to buy anything.", "village_elder_pretalk",[]],
  [anyone|plyr,"village_elder_talk",
   [
     ],
   "Have you seen any enemies around here recently?", "village_elder_ask_enemies",[]],
  [anyone,"village_elder_ask_enemies",
   [
     (assign, ":give_report", 0),
     (party_get_slot, ":original_faction", "$g_encountered_party", slot_center_original_faction),
     (store_relation, ":original_faction_relation", ":original_faction", "fac_player_supporters_faction"),
     (try_begin),
       (gt, ":original_faction_relation", 0),
       (party_slot_ge, "$g_encountered_party", slot_center_player_relation, 0),
       (assign, ":give_report", 1),
     (else_try),
       (party_slot_ge, "$g_encountered_party", slot_center_player_relation, 30),
       (assign, ":give_report", 1),
     (try_end),
     (eq, ":give_report", 0),
	 ##diplomacy start+
	 (call_script, "script_dplmc_print_commoner_at_arg1_says_sir_madame_to_s0", "$current_town"),#added
     ],
   "I am sorry, {s0}. We have neither seen nor heard of any war parties in this area.", "village_elder_pretalk",#replaced {sir/madam} with {s0}
   ##diplomacy end+
   []],
  [anyone,"village_elder_ask_enemies",
   [],
   "Hmm. Let me think about it...", "village_elder_tell_enemies",
   [
     (assign, "$temp", 0),
     ]],
  [anyone,"village_elder_tell_enemies",
   [
     (assign, ":target_hero_index", "$temp"),
     (assign, ":end_cond", active_npcs_end),
     (try_for_range, ":cur_troop", active_npcs_begin, ":end_cond"),
	   (troop_slot_eq, ":cur_troop", slot_troop_occupation, slto_kingdom_hero),
       (troop_get_slot, ":cur_party", ":cur_troop", slot_troop_leaded_party),
       (gt, ":cur_party", 0),
       (store_troop_faction, ":cur_faction", ":cur_troop"),
       (store_relation, ":reln", ":cur_faction", "fac_player_supporters_faction"),
       (lt, ":reln", 0),
       (store_distance_to_party_from_party, ":dist", "$g_encountered_party", ":cur_party"),
       (lt, ":dist", 10),
       (call_script, "script_get_information_about_troops_position", ":cur_troop", 0),
       (eq, reg0, 1), #Troop's location is known.
       (val_sub, ":target_hero_index", 1),
       (lt, ":target_hero_index", 0),
       (assign, ":end_cond", 0),
       (str_store_string, s2, "@He is not commanding any men at the moment."),
       (assign, ":num_troops", 0),
       (assign, ":num_wounded_troops", 0),
       (party_get_num_companion_stacks, ":num_stacks", ":cur_party"),
       (try_for_range_backwards, ":i_stack", 0, ":num_stacks"),
         (party_stack_get_troop_id, ":stack_troop", ":cur_party", ":i_stack"),
         (neg|troop_is_hero, ":stack_troop"),
         (party_stack_get_size, ":stack_size", ":cur_party", ":i_stack"),
         (party_stack_get_num_wounded, ":num_wounded", ":cur_party", ":i_stack"),
         (val_add, ":num_troops", ":stack_size"),
         (val_add, ":num_wounded_troops", ":num_wounded"),
       (try_end),
       (gt, ":num_troops", 0),
       (call_script, "script_round_value", ":num_wounded_troops"),
       (assign, reg1, reg0),
       (call_script, "script_round_value", ":num_troops"),
       (str_store_string, s2, "@He currently commands {reg0} men{reg1?, of which around {reg1} are wounded:}."),
     (try_end),
     (eq, ":end_cond", 0),
     ],
   "{s1} {s2}", "village_elder_tell_enemies",
   [
     (val_add, "$temp", 1),
     ]],
  [anyone,"village_elder_tell_enemies",
  ##diplomacy start+
   [(eq, "$temp", 0),
   	(call_script, "script_dplmc_print_commoner_at_arg1_says_sir_madame_to_s0", "$current_town"),#added
   ],
   "No, {s0}. We haven't seen any war parties in this area for some time.", "village_elder_pretalk",#replaced {sir/madam} with {s0}
  ##diplomacy end+
   []],
  [anyone,"village_elder_tell_enemies",
   [],
   "Well, I guess that was all.", "village_elder_pretalk",
   []],
  #(fire set up dialogs begin) Asking village elder to set up fire for making prison break easier.
  [anyone|plyr,"village_elder_talk",
  [
    (party_get_slot, ":bound_center", "$current_town", slot_village_bound_center),

    (assign, ":num_heroes_in_dungeon", 0),
    (assign, ":num_heroes_given_parole", 0),

    (party_get_num_prisoner_stacks, ":num_stacks", ":bound_center"),
    (try_for_range, ":i_stack", 0, ":num_stacks"),
      (party_prisoner_stack_get_troop_id, ":stack_troop",":bound_center",":i_stack"),
      (troop_is_hero, ":stack_troop"),
      (try_begin),
        (call_script, "script_cf_prisoner_offered_parole", ":stack_troop"),
        (party_add_members, "p_temp_party_2", ":stack_troop", 1),
        (val_add, ":num_heroes_given_parole", 1),
      (else_try),
        (party_add_members, "p_temp_party", ":stack_troop", 1),
        (val_add, ":num_heroes_in_dungeon", 1),
      (try_end),
    (try_end),

    (ge, ":num_heroes_in_dungeon", 1),
  ],
   "I need you to set a large fire on the outskirts of this village.", "village_elder_ask_set_fire",[]],
  [anyone,"village_elder_ask_set_fire",
   [
     ##diplomacy start+
	 (call_script, "script_dplmc_print_commoner_at_arg1_says_sir_madame_to_s0", "$current_town"),#added (re-used several times below)
	 ##diplomacy end+
     (eq, "$g_village_elder_did_not_liked_money_offered", 0),
     (party_get_slot, ":bound_center", "$current_town", slot_village_bound_center),
     (party_get_slot, ":fire_time", ":bound_center", slot_town_last_nearby_fire_time),
     (store_current_hours, ":cur_time"),
     (ge, ":fire_time", ":cur_time"),
   ],
   ##diplomacy start+
   "We have already agreed upon this, {s0}. I will do my best. You can trust me.", "close_window",[]],
#changed {sir/my lady} to {s0}
   ##diplomacy end+

  [anyone,"village_elder_ask_set_fire",
   [
     (eq, "$g_village_elder_did_not_liked_money_offered", 0),
   ],
   ##diplomacy start+
   "A fire, {s0}! Fires are dangerous! Why would you want such a thing?", "village_elder_ask_set_fire_1",[]],
#changed {sir/madam} to {s0}
   ##diplomacy end+

  [anyone,"village_elder_ask_set_fire", #elder did not accepted 100 mon before
   [
     (eq, "$g_village_elder_did_not_liked_money_offered", 1),
   ],
   ##diplomacy start+
   "I believe that we have already discussed this issue, {s0}.", "village_elder_ask_set_fire_5",[]],
#changed {sir/my lady} to {s0}
   ##diplomacy end+

  [anyone,"village_elder_ask_set_fire", #elder did not accepted 100 and 200 mon before
   [
     (eq, "$g_village_elder_did_not_liked_money_offered", 2),
   ],
   ##diplomacy start+
   #changed {sir/madam} to {s0}, and moved it to the other side of the word "before"
   "We talked about this before {s0} and your previous offers were low compared to risk you want me to take.",
   ##diplomacy end+
   "village_elder_ask_set_fire_5",[]],
  [anyone|plyr,"village_elder_ask_set_fire_1",[],
   "I have my reasons, and you will have yours -- a purse of silver. Will you do it, or not?", "village_elder_ask_set_fire_2",[]],
  [anyone|plyr,"village_elder_ask_set_fire_1",[],
  "Given the risk you are taking, you are entitled to know my plan.", "village_elder_ask_set_fire_explain_plan",[]],
  [anyone|plyr,"village_elder_ask_set_fire_explain_plan",[
  (party_get_slot, ":bound_center", "$g_encountered_party", slot_village_bound_center),
  (str_store_party_name, s4, ":bound_center"),
  ],
   "I wish to rescue a prisoner from {s4}. When you light the fire, the guards in {s4} will see the smoke, and some of them will rush outside to see what is going on. ", "village_elder_ask_set_fire_2",[]],
  [anyone,"village_elder_ask_set_fire_2",[
  (gt, "$g_talk_troop_effective_relation", 9),
  ],
##diplomacy start+ change {sir/my lady} to {s0}
   "As you wish, {s0}. You have been a good friend to this village, and, even though there is a risk, we should be glad to return the favor. When do you want this fire to start?", "village_elder_ask_set_fire_9",[]],
##diplomacy end+

  [anyone,"village_elder_ask_set_fire_2",[
  (lt, "$g_talk_troop_relation", 0),
  ],
##diplomacy start+ change {sir/my lady} to {s0}
   "I'm sorry, {s0}. You will forgive me for saying this, but we don't exactly have good reason to trust you. This is too dangerous.", "close_window",[]],
##diplomacy end+

  [anyone,"village_elder_ask_set_fire_2",[],
 ##diplomacy start+ change {sir/my lady} to {s0}
   "As you say, {s0}. But in doing this, we are taking a very great risk. What's in it for us?", "village_elder_ask_set_fire_3",[]],
##diplomacy end+

  [anyone|plyr,"village_elder_ask_set_fire_3",
  [
    (store_troop_gold, ":cur_gold", "trp_player"),
    (ge, ":cur_gold", 100),
  ],
   "I can give you 100 mon.", "village_elder_ask_set_fire_4",[(assign, "$g_last_money_offer_to_elder", 100),]],
  [anyone|plyr,"village_elder_ask_set_fire_3",
  [
    (store_troop_gold, ":cur_gold", "trp_player"),
    (ge, ":cur_gold", 200),
  ],
   "I can give you 200 mon.", "village_elder_ask_set_fire_6",[(assign, "$g_last_money_offer_to_elder", 200),]],
  [anyone|plyr,"village_elder_ask_set_fire_3",
  [
    (store_troop_gold, ":cur_gold", "trp_player"),
    (ge, ":cur_gold", 300),
  ],
   "I can give you 300 mon.", "village_elder_ask_set_fire_6",[(assign, "$g_last_money_offer_to_elder", 300),]],
  [anyone|plyr,"village_elder_ask_set_fire_3",[],
   "Never mind.", "close_window",[]],
  [anyone,"village_elder_ask_set_fire_4",
   [
     (eq, "$g_village_elder_did_not_liked_money_offered", 0),
   ],
   "This is madness. I cannot take such a risk.", "village_elder_talk",
   [
     (assign, "$g_village_elder_did_not_liked_money_offered", 1),
   ]],
  [anyone|plyr,"village_elder_ask_set_fire_5",
   [
     (eq, "$g_village_elder_did_not_liked_money_offered", 1),
     (store_troop_gold, ":cur_gold", "trp_player"),
     (ge, ":cur_gold", 200),
   ],
   "Then let's increase your reward to 200 mon.", "village_elder_ask_set_fire_7", [(assign, "$g_last_money_offer_to_elder", 200),]],
  [anyone|plyr,"village_elder_ask_set_fire_5",
   [
     (eq, "$g_village_elder_did_not_liked_money_offered", 1),
     (store_troop_gold, ":cur_gold", "trp_player"),
     (ge, ":cur_gold", 300),
   ],
   "Then let's increase your reward to 300 mon.", "village_elder_ask_set_fire_6",[(assign, "$g_last_money_offer_to_elder", 300),]],
  [anyone|plyr,"village_elder_ask_set_fire_5",
   [
     (eq, "$g_village_elder_did_not_liked_money_offered", 2),
     (store_troop_gold, ":cur_gold", "trp_player"),
     (ge, ":cur_gold", 300),
   ],
   "Then let's increase your reward to 300 mon. This is my last offer.", "village_elder_ask_set_fire_6",[(assign, "$g_last_money_offer_to_elder", 300),]],
  [anyone|plyr,"village_elder_ask_set_fire_5",[],
   "Never mind.", "close_window",[]],
  [anyone,"village_elder_ask_set_fire_6",[],
   "Very well. You are asking me to take a very great risk, but I will do it. When do you want this fire to start?", "village_elder_ask_set_fire_9",
   [
     (troop_remove_gold, "trp_player", "$g_last_money_offer_to_elder"),
   ]],
  [anyone,"village_elder_ask_set_fire_7",[],
   "I cannot do such a dangerous thing for 200 mon.", "village_elder_talk",
   [
     (assign, "$g_village_elder_did_not_liked_money_offered", 2),
   ]],
  [anyone|plyr,"village_elder_ask_set_fire_9",[],
   "Continue with your preparations. One hour from now, I need that fire.", "village_elder_ask_set_fire_10",
   [
     (party_get_slot, ":bound_center", "$current_town", slot_village_bound_center),
     (store_current_hours, ":cur_time"),
	 (val_add, ":cur_time", 1),
     (assign, ":fire_time", ":cur_time"),
     (party_set_slot, ":bound_center", slot_town_last_nearby_fire_time, ":fire_time"),
     (try_begin),
       (is_between, "$next_center_will_be_fired", villages_begin, villages_end),
       (party_get_slot, ":is_there_already_fire", "$next_center_will_be_fired", slot_village_smoke_added),
       (eq, ":is_there_already_fire", 0),
       (party_get_slot, ":fire_time", "$next_center_will_be_fired", slot_town_last_nearby_fire_time),
       (store_current_hours, ":cur_hours"),
       (store_sub, ":cur_time_sub_fire_duration", ":cur_hours", fire_duration),
       (val_sub, ":cur_time_sub_fire_duration", 1),
       (ge, ":fire_time", ":cur_time_sub_fire_duration"),
       (party_clear_particle_systems, "$next_center_will_be_fired"),
     (try_end),
     (assign, "$next_center_will_be_fired", "$current_town"),
     (assign, "$g_village_elder_did_not_liked_money_offered", 0),
   ]],
  [anyone|plyr,"village_elder_ask_set_fire_9",
   [
     (store_time_of_day, ":cur_day_hour"),
     (ge, ":cur_day_hour", 6),
     (lt, ":cur_day_hour", 23),
   ],
   "Do this in at the stroke of midnight. I will wait exactly one hour.", "village_elder_ask_set_fire_11",
   [
     (party_get_slot, ":bound_center", "$current_town", slot_village_bound_center),
     (store_time_of_day, ":cur_day_hour"),
     (store_current_hours, ":cur_time"),
     (store_sub, ":difference", 24, ":cur_day_hour"), #fire will be at 24 midnight today
     (store_add, ":fire_time", ":cur_time", ":difference"),
     (party_set_slot, ":bound_center", slot_town_last_nearby_fire_time, ":fire_time"),
     (try_begin),
       (is_between, "$next_center_will_be_fired", villages_begin, villages_end),
       (party_get_slot, ":is_there_already_fire", "$next_center_will_be_fired", slot_village_smoke_added),
       (eq, ":is_there_already_fire", 0),
       (party_get_slot, ":fire_time", "$next_center_will_be_fired", slot_town_last_nearby_fire_time),
       (store_current_hours, ":cur_hours"),
       (store_sub, ":cur_time_sub_fire_duration", ":cur_hours", fire_duration),
       (val_sub, ":cur_time_sub_fire_duration", 1),
       (ge, ":fire_time", ":cur_time_sub_fire_duration"),
       (party_clear_particle_systems, "$next_center_will_be_fired"),
     (try_end),
     (assign, "$next_center_will_be_fired", "$current_town"),
     (assign, "$g_village_elder_did_not_liked_money_offered", 0),
    ]],
  [anyone,"village_elder_ask_set_fire_10",[],
   "Very well, {sir/my lady}. We will make our preparations. Now you make yours.", "close_window",
   [
   (assign, ":maximum_distance", -1),
   (try_for_agents, ":cur_agent"),
     (agent_get_troop_id, ":troop_id", ":cur_agent"),
     (is_between, ":troop_id", village_elders_begin, village_elders_end),
     (agent_get_position, pos0, ":cur_agent"),
     (try_for_range, ":entry_point_id", 0, 64),
       (entry_point_get_position, pos1, ":entry_point_id"),
       (get_distance_between_positions, ":dist", pos0, pos1),
       (gt, ":dist", ":maximum_distance"),
       (assign, ":maximum_distance", ":dist"),
       (copy_position, pos2, pos1),
       (assign, ":village_elder_agent", ":cur_agent"),
     (try_end),
     (try_begin),
       (gt, ":maximum_distance", -1),
       (agent_set_scripted_destination, ":village_elder_agent", pos2),
     (try_end),
   (try_end),
   ]],
  [anyone,"village_elder_ask_set_fire_11",[],
   "As you wish, {sir/my lady}. May the heavens protect you.", "close_window",[]],
  #(fire set up dialogs end)






  [anyone|plyr,"village_elder_talk", [(call_script, "script_cf_village_recruit_volunteers_cond"),],
   "Are there any men from this village willing to join me?", "village_elder_recruit_start",[]],
  [anyone|plyr,"village_elder_talk", [],
   "[Leave]", "close_window",[]],
  [anyone ,"village_elder_buy_cattle", [(party_get_slot, reg5, "$g_encountered_party", slot_village_number_of_cattle),
                                        (gt, reg5, 0),
                                        (store_item_value, ":cattle_cost", "itm_cattle_meat"),
                                        (call_script, "script_game_get_item_buy_price_factor", "itm_cattle_meat"),
                                        (val_mul, ":cattle_cost", reg0),
                                        #Multiplied by 2 and divided by 100
                                        (val_div, ":cattle_cost", 50),
                                        (assign, "$temp", ":cattle_cost"),
                                        (assign, reg6, ":cattle_cost"),
                                        ],
   "We have {reg5} heads of cattle, each for {reg6} mon. How many do you want to buy?", "village_elder_buy_cattle_2",[]],
  [anyone ,"village_elder_buy_cattle", [],
   "I am afraid we have no cattle left in the village {sir/madam}.", "village_elder_buy_cattle_2",[]],
  [anyone|plyr,"village_elder_buy_cattle_2", [(party_get_slot, ":num_cattle", "$g_encountered_party", slot_village_number_of_cattle),
                                              (ge, ":num_cattle", 1),
                                              (store_troop_gold, ":gold", "trp_player"),
                                              (ge, ":gold", "$temp"),],
   "One.", "village_elder_buy_cattle_complete",[(call_script, "script_buy_cattle_from_village", "$g_encountered_party", 1, "$temp"),
                                                       ]],
  [anyone|plyr,"village_elder_buy_cattle_2", [(party_get_slot, ":num_cattle", "$g_encountered_party", slot_village_number_of_cattle),
                                              (ge, ":num_cattle", 2),
                                              (store_troop_gold, ":gold", "trp_player"),
                                              (store_mul, ":cost", "$temp", 2),
                                              (ge, ":gold", ":cost"),],
   "Two.", "village_elder_buy_cattle_complete",[(call_script, "script_buy_cattle_from_village", "$g_encountered_party", 2, "$temp"),
                                                       ]],
  [anyone|plyr,"village_elder_buy_cattle_2", [(party_get_slot, ":num_cattle", "$g_encountered_party", slot_village_number_of_cattle),
                                              (ge, ":num_cattle", 3),
                                              (store_troop_gold, ":gold", "trp_player"),
                                              (store_mul, ":cost", "$temp", 3),
                                              (ge, ":gold", ":cost"),],
   "Three.", "village_elder_buy_cattle_complete",[(call_script, "script_buy_cattle_from_village", "$g_encountered_party", 3, "$temp"),
                                                       ]],
  [anyone|plyr,"village_elder_buy_cattle_2", [(party_get_slot, ":num_cattle", "$g_encountered_party", slot_village_number_of_cattle),
                                              (ge, ":num_cattle", 4),
                                              (store_troop_gold, ":gold", "trp_player"),
                                              (store_mul, ":cost", "$temp", 4),
                                              (ge, ":gold", ":cost"),],
   "Four.", "village_elder_buy_cattle_complete",[(call_script, "script_buy_cattle_from_village", "$g_encountered_party", 4, "$temp"),
                                                       ]],
  [anyone|plyr,"village_elder_buy_cattle_2", [(party_get_slot, ":num_cattle", "$g_encountered_party", slot_village_number_of_cattle),
                                              (ge, ":num_cattle", 5),
                                              (store_troop_gold, ":gold", "trp_player"),
                                              (store_mul, ":cost", "$temp", 5),
                                              (ge, ":gold", ":cost"),],
   "Five.", "village_elder_buy_cattle_complete",[(call_script, "script_buy_cattle_from_village", "$g_encountered_party", 5, "$temp"),
                                                       ]],
  [anyone|plyr,"village_elder_buy_cattle_2", [],
   "Forget it.", "village_elder_pretalk",[]],
  [anyone ,"village_elder_buy_cattle_complete", [],
   "I will tell the herders to round up the animals and bring them to you, {sir/madam}. I am sure you will be satisfied with your purchase.", "village_elder_pretalk",[]],
  [anyone ,"village_elder_recruit_start", [(party_get_slot, ":num_volunteers", "$current_town", slot_center_volunteer_troop_amount),
                                           (party_get_free_companions_capacity, ":free_capacity", "p_main_party"),
                                           (val_min, ":num_volunteers", ":free_capacity"),
                                           (store_troop_gold, ":gold", "trp_player"),
                                           (store_div, ":gold_capacity", ":gold", 10),#10 mon per man
                                           (val_min, ":num_volunteers", ":gold_capacity"),
                                           (le, ":num_volunteers", 0),
                                           ],
   "I don't think anyone would be interested, {sir/madam}. Is there anything else I can do for you?", "village_elder_talk",[]],
  [anyone ,"village_elder_recruit_start", [(party_get_slot, ":num_volunteers", "$current_town", slot_center_volunteer_troop_amount),
                                           (party_get_free_companions_capacity, ":free_capacity", "p_main_party"),
                                           (val_min, ":num_volunteers", ":free_capacity"),
                                           (store_troop_gold, ":gold", "trp_player"),
                                           (store_div, ":gold_capacity", ":gold", 10),#10 mon per man
                                           (val_min, ":num_volunteers", ":gold_capacity"),
                                           (assign, "$temp",  ":num_volunteers"),
                                           (assign, reg5, ":num_volunteers"),
                                           (store_add, reg7, ":num_volunteers", -1),
                                           ],
   "I can think of {reg5} whom I suspect would jump at the chance. If you could pay 10 mon {reg7?each for their equipment:for his equipment}.\
 Does that suit you?", "village_elder_recruit_decision",[]],
#not used:
##  [anyone|plyr,"village_elder_recruit_decision", [(party_get_slot, ":num_volunteers", "$current_town", slot_center_volunteer_troop_amount),
##                                                  (party_get_free_companions_capacity, ":free_capacity", "p_main_party"),
##                                                  (val_min, ":num_volunteers", ":free_capacity"),
##                                                  (store_troop_gold, ":gold", "trp_player"),
##                                                  (store_div, ":gold_capacity", ":gold", 10),#10 mon per man
##                                                  (val_min, ":num_volunteers", ":gold_capacity"),
##                                                  (eq, ":num_volunteers", 0),],
##   "So be it.", "village_elder_pretalk",
##   [
##     (try_begin),
##       (party_slot_eq, "$current_town", slot_center_volunteer_troop_amount, 0), #do not change the value if it is above 0
##       (party_set_slot, "$current_town", slot_center_volunteer_troop_amount, -1),
##     (try_end),]],

  [anyone|plyr,"village_elder_recruit_decision", [(assign, ":num_volunteers", "$temp"),
                                                  (ge, ":num_volunteers", 1),
                                                  (store_add, reg7, ":num_volunteers", -1)],
   "Tell {reg7?them:him} to make ready.", "village_elder_pretalk",[(call_script, "script_village_recruit_volunteers_recruit"),]],
  [anyone|plyr,"village_elder_recruit_decision", [(party_slot_ge, "$current_town", slot_center_volunteer_troop_amount, 1)],
   "No, not now.", "village_elder_pretalk",[]],
  [anyone,"village_elder_active_mission_1", [], "Yes {sir/madam}, have you made any progress on it?", "village_elder_active_mission_2",[]],
  [anyone|plyr,"village_elder_active_mission_2",[(store_partner_quest,":elder_quest"),
                                                 (eq, ":elder_quest", "qst_deliver_grain"),
                                                 (quest_get_slot, ":quest_target_amount", "qst_deliver_grain", slot_quest_target_amount),
                                                 (call_script, "script_get_troop_item_amount", "trp_player", "itm_grain"),
                                                 (assign, ":cur_amount", reg0),
                                                 (ge, ":cur_amount", ":quest_target_amount"),
                                                 (assign, reg5, ":quest_target_amount"),
                                                 ],
   "Indeed. I brought you {reg5} sacks of brown rice.", "village_elder_deliver_grain_thank",
   []],
  [anyone,"village_elder_deliver_grain_thank", [(str_store_party_name, s13, "$current_town")],
   "My good {lord/lady}. You have saved us from hunger and desperation. We cannot thank you enough, but you'll always be in our prayers.\
 The village of {s13} will not forget what you have done for us.", "village_elder_deliver_grain_thank_2",
   [(quest_get_slot, ":quest_target_amount", "qst_deliver_grain", slot_quest_target_amount),
    (troop_remove_items, "trp_player", "itm_grain", ":quest_target_amount"),
    (add_xp_as_reward, 400),
    (call_script, "script_change_center_prosperity", "$current_town", 4),
    (call_script, "script_change_player_relation_with_center", "$current_town", 5),
    (call_script, "script_end_quest", "qst_deliver_grain"),
#Troop commentaries begin
    (call_script, "script_add_log_entry", logent_helped_peasants, "trp_player",  "$current_town", -1, -1),
#Troop commentaries end
   ]],
  [anyone,"village_elder_deliver_grain_thank_2", [],
   "My good {lord/lady}, please, is there anything I can do for you?", "village_elder_talk",[]],
  [anyone|plyr,"village_elder_active_mission_2", [], "I am still working on it.", "village_elder_active_mission_3",[]],
  [anyone|plyr,"village_elder_active_mission_2", [], "I am afraid I won't be able to finish it.", "village_elder_mission_failed",[]],
  [anyone,"village_elder_active_mission_3",
  ##diplomacy start+ change to use script_dplmc_print_subordinate_says_sir_madame_to_s0
  #[], "Thank you, {sir/madam}. We are praying for your success everyday.", "village_elder_pretalk",[]],
  [(call_script, "script_dplmc_print_subordinate_says_sir_madame_to_s0"),],
  "Thank you, {s0}. We are praying for your success everyday.", "village_elder_pretalk",[]],
  ##diplomacy end+

  ##diplomacy start+ change to use script_dplmc_print_subordinate_says_sir_madame_to_s0
  [anyone,"village_elder_mission_failed", #[], "Ah, I am sorry to hear that {sir/madam}. I'll try to think of something else.",
  [(call_script, "script_dplmc_print_subordinate_says_sir_madame_to_s0"),],
  "Ah, I am sorry to hear that {s0}. I'll try to think of something else.",
  ##diplomacy end+
  "village_elder_pretalk",
   [(store_partner_quest,":elder_quest"),
    (call_script, "script_abort_quest", ":elder_quest", 1)]],
##
##  [anyone,"village_elder_generic_mission_thank", [],
##   "You have been so helpful {sir/madam}. I do not know how to thank you.", "village_elder_generic_mission_completed",[]],
##
##  [anyone|plyr,"village_elder_generic_mission_completed", [],
##   "Speak not of it. I only did what needed to be done.", "village_elder_pretalk",[]],

# Currently not needed.
##  [anyone|plyr,"village_elder_generic_mission_failed", [],
##   "TODO: I'm sorry I failed you sir. It won't happen again.", "village_elder_pretalk",
##   [(store_partner_quest,":elder_quest"),
##    (call_script, "script_finish_quest", ":elder_quest", 0),
##    ]],


  [anyone,"village_elder_request_mission_ask",
  ##diplomacy start+ change to use script_dplmc_print_subordinate_says_sir_madame_to_s0
  #[(store_partner_quest,":elder_quest"),(ge,":elder_quest",0)],
  [(store_partner_quest,":elder_quest"),
   (ge,":elder_quest",0),
   (call_script, "script_dplmc_print_subordinate_says_sir_madame_to_s0"),],
  #"Well {sir/madam}, you are already engaged with a task helping us. We cannot ask more from you.", "village_elder_pretalk",[]],
  "Well {s0} you are already engaged with a task helping us. We cannot ask more from you.", "village_elder_pretalk",[]],
  ##diplomacy end+

  ##diplomacy start+ change to use script_dplmc_print_subordinate_says_sir_madame_to_s0
  [anyone,"village_elder_request_mission_ask", #[(troop_slot_eq, "$g_talk_troop", slot_troop_does_not_give_quest, 1)],
   [(troop_slot_eq, "$g_talk_troop", slot_troop_does_not_give_quest, 1),
    (call_script, "script_dplmc_print_subordinate_says_sir_madame_to_s0"),],
   #"No {sir/madam}, We don't have any other tasks for you.", "village_elder_pretalk",[]],
   "No {s0}, We don't have any other tasks for you.", "village_elder_pretalk",[]],
   ##diplomacy end+

  [anyone|auto_proceed,"village_elder_request_mission_ask", [], "A task?", "village_elder_tell_mission",
   [
       (call_script, "script_get_quest", "$g_talk_troop"),
       (assign, "$random_quest_no", reg0),
   ]],
  [anyone,"village_elder_tell_mission", [(eq,"$random_quest_no","qst_deliver_grain")],
   "{My good sir/My good lady}, our village has been going through such hardships lately.\
 The harvest has been bad, and recently some merciless bandits took away our seed that we had reserved for the planting season.\
 If we cannot find some rice soon, we will not be able to plant our fields and then we will have nothing to eat for the coming year.\
 If you can help us, we would be indebted to you forever.", "village_elder_tell_deliver_grain_mission",
   [
     (quest_get_slot, ":quest_target_center", "$random_quest_no", slot_quest_target_center),
     (str_store_party_name_link,s3,":quest_target_center"),
     (quest_get_slot, reg5, "$random_quest_no", slot_quest_target_amount),
     (setup_quest_text,"$random_quest_no"),
     (str_store_string, s2, "@The elder of the village of {s3} asked you to bring them {reg5} sacks of brown rice."),
   ]],
  [anyone|plyr,"village_elder_tell_deliver_grain_mission", [],
   "Hmmm. How much rice do you need?", "village_elder_tell_deliver_grain_mission_2",[]],
  [anyone|plyr,"village_elder_tell_deliver_grain_mission", [],
   "I can't be bothered with this. Ask help from someone else.", "village_elder_deliver_grain_mission_reject",[]],
  [anyone,"village_elder_tell_deliver_grain_mission_2", [(quest_get_slot, reg5, "$random_quest_no", slot_quest_target_amount)],
   "I think {reg5} sacks of brown rice will get us through the next planting. Hopefully, we can find charitable people to help us with the rest.", "village_elder_tell_deliver_grain_mission_3",[]],
  [anyone|plyr,"village_elder_tell_deliver_grain_mission_3", [],
   "Then I will go and find you the brown rice you need.", "village_elder_deliver_grain_mission_accept",[]],
  [anyone|plyr,"village_elder_tell_deliver_grain_mission_3", [],
   "I am afraid I don't have time for this. You'll need to find help elsewhere.", "village_elder_deliver_grain_mission_reject",[]],
  ##diplomacy start+ replace {sir/madam} with {my lord/my lady} or your highness if appropriate
  [anyone,"village_elder_deliver_grain_mission_accept", #[], "Thank you, {sir/madam}. We'll be praying for you night and day.", "close_window",
   [(call_script, "script_dplmc_print_subordinate_says_sir_madame_to_s0"),],
   "Thank you, {s0}. We'll be praying for you night and day.", "close_window",
  ##diplomacy end+
   [(assign, "$g_leave_encounter",1),
    (call_script, "script_change_player_relation_with_center", "$current_town", 5),
    (call_script, "script_start_quest", "$random_quest_no", "$g_talk_troop"),
    ]],
##diplomacy start+ replace {sir/madam} with {my lord/my lady} or your highness if appropriate
  [anyone,"village_elder_deliver_grain_mission_reject", #[], "Yes {sir/madam}, of course. I am sorry if I have bothered you with our troubles.", "close_window",
  [(call_script, "script_dplmc_print_subordinate_says_sir_madame_to_s0"),], "Yes {s0}, of course. I am sorry if I have bothered you with our troubles.", "close_window",
##diplomacy end+
   [(troop_set_slot, "$g_talk_troop", slot_troop_does_not_give_quest, 1),
    ]],
  [anyone,"village_elder_tell_mission", [(eq,"$random_quest_no", "qst_train_peasants_against_bandits")],
   "We are suffering greatly at the hands of a group of bandits. They take our food and livestock,\
 and kill anyone who doesn't obey them immediately. Our men are angry that we cannot defend ourselves, but we are only simple farmers...\
 However, with some help, I think that some of the people here could be more than that.\
 We just need an experienced warrior to teach us how to fight.",
   "village_elder_tell_train_peasants_against_bandits_mission",
   [
     (quest_get_slot, ":quest_target_center", "$random_quest_no", slot_quest_target_center),
     (str_store_party_name_link, s13, ":quest_target_center"),
     (quest_get_slot, reg5, "$random_quest_no", slot_quest_target_amount),
     (setup_quest_text, "$random_quest_no"),
     (str_store_string, s2, "@The elder of the village of {s13} asked you to train {reg5} peasants to fight against local bandits."),
   ]],
  [anyone|plyr, "village_elder_tell_train_peasants_against_bandits_mission", [],
   "I can teach you how to defend yourself.", "village_elder_train_peasants_against_bandits_mission_accept",[]],
  [anyone|plyr, "village_elder_tell_train_peasants_against_bandits_mission", [],
   "You peasants have no business taking up arms. Just pay the bandits and be off with it.", "village_elder_train_peasants_against_bandits_mission_reject",[]],
  ##diplomacy start+ replace {sir/madam} with {my lord/my lady} or your highness if appropriate
  [anyone,"village_elder_train_peasants_against_bandits_mission_accept",
   [(call_script, "script_dplmc_print_subordinate_says_sir_madame_to_s0"),],
   "You will? Oh, splendid! We would be deeply indebted to you, {s0}. I'll instruct the village folk to assemble here and receive your training. If you can teach us how to defend ourselves, I promise you'll receive everything we can give you in return for your efforts.", "close_window",
	##diplomacy end+
   [
     (assign, "$g_leave_encounter",1),
     #TODO: Change this value
     (call_script, "script_change_player_relation_with_center", "$current_town", 3),
     (call_script, "script_start_quest", "$random_quest_no", "$g_talk_troop"),
     ]],
##diplomacy start+ replace {sir/madam} with {my lord/my lady} or your highness if appropriate
  [anyone,"village_elder_train_peasants_against_bandits_mission_reject", #[], "Yes, of course {sir/madam}.\
  [(call_script, "script_dplmc_print_subordinate_says_sir_madame_to_s0"),],
  "Yes, of course {s0}.  Thank you for your counsel.", "close_window",
##diplomacy end+
   [
     (troop_set_slot, "$g_talk_troop", slot_troop_does_not_give_quest, 1),
     ]],
  [anyone,"village_elder_tell_mission", [(eq,"$random_quest_no","qst_deliver_cattle")],
   "Bandits have driven away our cattle. Our pastures are empty. If we had just a few heads of cattle we could start to raise a herd again.",
   "village_elder_tell_deliver_cattle_mission",
   [
     (quest_get_slot, ":quest_target_center", "$random_quest_no", slot_quest_target_center),
     (str_store_party_name_link,s3,":quest_target_center"),
     (quest_get_slot, reg5, "$random_quest_no", slot_quest_target_amount),
     (setup_quest_text,"$random_quest_no"),
     (str_store_string, s2, "@The elder of the village of {s3} asked you to bring them {reg5} heads of cattle."),
   ]],
  [anyone|plyr,"village_elder_tell_deliver_cattle_mission", [],
   "How many animals do you need?", "village_elder_tell_deliver_cattle_mission_2",[]],
  [anyone|plyr,"village_elder_tell_deliver_cattle_mission", [],
   "I don't have time for this. Ask help from someone else.", "village_elder_deliver_cattle_mission_reject",[]],
  [anyone,"village_elder_tell_deliver_cattle_mission_2", [(quest_get_slot, reg5, "$random_quest_no", slot_quest_target_amount)],
   "I think {reg5} heads will suffice for a small herd.", "village_elder_tell_deliver_cattle_mission_3",[]],
  [anyone|plyr,"village_elder_tell_deliver_cattle_mission_3", [],
   "Then I will bring you the cattle you need.", "village_elder_deliver_cattle_mission_accept",[]],
  [anyone|plyr,"village_elder_tell_deliver_cattle_mission_3", [],
   "I am afraid I don't have time for this. You'll need to find help elsewhere.", "village_elder_deliver_cattle_mission_reject",[]],
  ##diplomacy start+ replace {sir/madam} with {my lord/my lady} or your highness if appropriate
  [anyone,"village_elder_deliver_cattle_mission_accept", [(call_script, "script_dplmc_print_subordinate_says_sir_madame_to_s0"),], "Thank you, {s0}. We'll be praying for you night and day.", "close_window",
  ##diplomacy end+
   [(assign, "$g_leave_encounter",1),
    (call_script, "script_change_player_relation_with_center", "$current_town", 3),
    (call_script, "script_start_quest", "$random_quest_no", "$g_talk_troop"),
    ]],
  ##diplomacy start+ replace {sir/madam} with {my lord/my lady} or your highness if appropriate
  [anyone,"village_elder_deliver_cattle_mission_reject", [(call_script, "script_dplmc_print_subordinate_says_sir_madame_to_s0"),], "Yes {s0}, of course. I am sorry if I have bothered you with our troubles.", "close_window",
  ##diplomacy end+
   [(troop_set_slot, "$g_talk_troop", slot_troop_does_not_give_quest, 1),
    ]],
  #diplomacy start+ replace {sir/madam} with {my lord/my lady} or your highness if appropriate
  [anyone,"village_elder_tell_mission", [(call_script, "script_dplmc_print_subordinate_says_sir_madame_to_s0"),], "Thank you, {s0}, but we do not really need anything right now.", "village_elder_pretalk",[]],
  #diplomacy end+

##  [anyone|plyr,"village_elder_mission_told", [], "TODO: As you wish sir. You can count on me.", "village_elder_mission_accepted",[]],
##  [anyone|plyr,"village_elder_mission_told", [], "TODO: I'm afraid I can't carry out this mission right now, sir.", "village_elder_mission_rejected",[]],
##
##  [anyone,"village_elder_mission_accepted", [], "TODO: Excellent. Do this {playername}. I really have high hopes for you.", "close_window",
##   [(assign, "$g_leave_encounter",1),
##    (try_begin),
##    #TODO: Add quest initializations here
##    (try_end),
##    (call_script, "script_start_quest", "$random_quest_no", "$g_talk_troop"),
##    ]],

##  [anyone,"village_elder_mission_rejected", [], "TODO: Is that so? Perhaps you are not up for the task anyway...", "close_window",
##   [(assign, "$g_leave_encounter",1),
##    (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", -1),
##    (troop_set_slot, "$g_talk_troop", slot_troop_does_not_give_quest, 1),
##    ]],




#Goods Merchants

  [anyone ,"start", [(is_between,"$g_talk_troop",goods_merchants_begin,goods_merchants_end),
                     (party_slot_eq, "$current_town", slot_town_lord, "trp_player")],
   "{My lord/my lady}, you honour my humble shop with your presence.", "goods_merchant_talk",[]],
	
  [anyone, "fort_deputy_discuss", [], "Anything else?","fort_deputy_discuss_options", []],
	
  #ask deputy about potential companion
  [anyone|plyr, "fort_deputy_discuss_options", [
      (party_get_slot, ":companion", "$current_town", slot_fort_npc_2),
      (troop_slot_ge, ":companion", slot_troop_met, 1),
	  (str_store_troop_name, s2, ":companion"),
	  (try_begin),
	    (this_or_next|party_slot_eq, "$current_town", slot_fort_npc_2_state, 3), #companion has been recruited
	    (party_slot_eq, "$current_town", slot_fort_npc_2_state, 4), #companion has been promoted to lord
        (str_store_string, s2, "@Would you like to know how {s2} has been doing?"),
	  (else_try),
        (str_store_string, s2, "@I wish to ask about {s2}."), #default request
	  (try_end),
    ], "{s2}", "fort_deputy_discuss_companion", []],
  #deputy responds about companion
  [anyone, "fort_deputy_discuss_companion", [ 
      (store_sub, ":offset", "$current_town", forts_begin),
	  (try_begin),
	    (party_slot_eq, "$current_town", slot_fort_npc_2_state, 4), #companion has been promoted to lord
	    (store_add, ":deputy_talk", "str_gekokujo_fort_1_deputy_ask_companion_promoted", ":offset"),
	  (else_try),
	    (party_slot_eq, "$current_town", slot_fort_npc_2_state, 3), #companion has been recruited
	    (store_add, ":deputy_talk", "str_gekokujo_fort_1_deputy_ask_companion_recruited", ":offset"),
	  (else_try),
	    (party_slot_eq, "$current_town", slot_fort_npc_2_state, 2), #companion has returned temporarily
        (party_get_slot, ":companion", "$current_town", slot_fort_npc_2),
		(str_store_troop_name, s3, ":companion"),
        (assign, ":deputy_talk", "str_gekokujo_fort_deputy_ask_companion_returned"),
	  (else_try),
        (store_add, ":deputy_talk", "str_gekokujo_fort_1_deputy_ask_companion", ":offset"), #default response
	  (try_end),
      (str_store_string, s45, ":deputy_talk"),
    ], "{s45}","fort_deputy_discuss", []],
	
  #ask deputy permission for the companion to join
  [anyone|plyr, "fort_deputy_discuss_options", [
      (party_slot_eq, "$current_town", slot_fort_npc_2_state, 1), #this should only show up if you've already asked companion to join
      (party_get_slot, ":companion", "$current_town", slot_fort_npc_2),
      (troop_slot_ge, ":companion", slot_troop_met, 1),
	  (str_store_troop_name, s2, ":companion"),
    ], "I wish for {s2} to join me.", "fort_deputy_discuss_companion_recruit", []],
  
  #deputy responds about companion joining
  [anyone, "fort_deputy_discuss_companion_recruit", [ 
      (store_sub, ":offset", "$current_town", forts_begin),
      (store_add, ":deputy_talk", "str_gekokujo_fort_1_deputy_ask_companion_recruit", ":offset"),
      (str_store_string, s45, ":deputy_talk"),
    ], "{s45}","fort_deputy_discuss", [
	  (party_set_slot, "$current_town", slot_fort_npc_2_state, 3), #set to "companion recruited"
	  (party_get_slot, ":companion", "$current_town", slot_fort_npc_2),
	  #(party_add_members, "p_main_party", ":companion", 1),
	  (call_script, "script_recruit_troop_as_companion", ":companion")
	]],
  
  #deputy - ask about fort specialties
  [anyone|plyr, "fort_deputy_discuss_options", [
      (str_store_party_name, s3, "$current_town"),
    ], "What does {s3} have to offer?", "fort_deputy_discuss_specialty", []],
  [anyone, "fort_deputy_discuss_specialty", [
      (store_sub, ":offset", "$current_town", forts_begin),
      (store_add, ":deputy_talk", "str_gekokujo_fort_1_deputy_ask_specialty", ":offset"),
      (str_store_string, s45, ":deputy_talk"),
    ], "{s45}","fort_deputy_discuss", []],
  
  #deputy - ask for troops (we add it to the garrison)
  [anyone|plyr, "fort_deputy_discuss_options", [
      (party_slot_eq, "$current_town", slot_fort_timer, 0),
    ], "I wish to recruit some men.", "fort_deputy_discuss_recruit", []],
	
  [anyone, "fort_deputy_discuss_recruit", [], "Very well.", "fort_deputy_discuss", [
      (party_set_slot, "$current_town", slot_fort_timer, 7), #reset the timer
      (store_random_in_range, ":rand_recruits", 15, 31), #15 to 31 recruits
      (party_get_slot, ":recruit", "$current_town", slot_fort_recruit_type), #determine the type of recruits
      (party_add_members, "$current_town", ":recruit", ":rand_recruits"), #give them to the town garrison
      (change_screen_exchange_members, 1, "$current_town"), #change to the garrison screen
    ]],
  
  #deputy - ask for trade goods (we add it to the warehouse)
  [anyone|plyr, "fort_deputy_discuss_options", [
      (party_slot_eq, "$current_town", slot_fort_timer, 0),
    ], "I wish to produce some goods.", "fort_deputy_discuss_produce", []],
	
  [anyone, "fort_deputy_discuss_produce", [], "They are ready to be shipped, my {lord/lady}.", "fort_deputy_discuss", [
      (party_set_slot, "$current_town", slot_fort_timer, 7), #reset the timer
	  
      (try_begin),
	    (eq, "$current_town", "p_fort_1"), #sado produces 5-10 dried sea fish
        (store_random_in_range, ":rand_goods", 5, 11),
        (assign, ":goods", "itm_smoked_fish"),
      (else_try),
	    (eq, "$current_town", "p_fort_2"), #tsushima produces 1-3 spice
        (store_random_in_range, ":rand_goods", 1, 4),
        (assign, ":goods", "itm_spice"),
      (else_try),
	    (eq, "$current_town", "p_fort_3"), #kokawa-dera produces 5-8 lacquer ware
        (store_random_in_range, ":rand_goods", 5, 9),
        (assign, ":goods", "itm_leatherwork"),
      (else_try),
	    (eq, "$current_town", "p_fort_4"), #mii-dera produces 4-8 linen cloth
        (store_random_in_range, ":rand_goods", 4, 9),
        (assign, ":goods", "itm_linen"),
      (else_try),
	    (eq, "$current_town", "p_fort_5"), #niputay produces 4-7 iron
        (store_random_in_range, ":rand_goods", 4, 8),
        (assign, ":goods", "itm_iron"),
      (else_try),
	    (eq, "$current_town", "p_fort_6"), #otasut produces 3-4 furs
        (store_random_in_range, ":rand_goods", 3, 5),
        (assign, ":goods", "itm_furs"),
      (try_end),
	  
      (troop_add_items, "$g_talk_troop", ":goods", ":rand_goods"), #give them to the deputy aka warehouse inventory
      (change_screen_loot, "$g_talk_troop"), #change to the warehouse inventry screen
    ]],
  
  #deputy - ask for work status (timer)
  [anyone|plyr, "fort_deputy_discuss_options", [
      (party_slot_ge, "$current_town", slot_fort_timer, 1),
    ], "When are you able to recruit men or produce goods again?", "fort_deputy_discuss_timer", []],
	
  [anyone, "fort_deputy_discuss_timer", [
      (party_get_slot, reg2, "$current_town", slot_fort_timer),
	  (try_begin),
	    (gt, reg2, 1),
		(str_store_string, s3, "@{reg2} days"),
	  (else_try),
		(str_store_string, s3, "@another day"),
	  (try_end),
    ], "At the pace we are going, surely no more than {s3}.", "fort_deputy_discuss", []],
  
  #deputy - ask to see fort's warehouse
  [anyone|plyr,"fort_deputy_discuss_options", [],
    "Let's check the warehouse inventories.", "fort_deputy_discuss", [
      (change_screen_loot, "$g_talk_troop"),
    ]],
	
  #deputy - ask to see equipment
  [anyone|plyr,"fort_deputy_discuss_options", [], "Let me see your equipment.", "fort_deputy_discuss_equipment", []],
  [anyone,"fort_deputy_discuss_equipment", [], "Very well, it's all here...", "fort_deputy_discuss", [(change_screen_equip_other)]],
  #deputy - end dialogue
  [anyone|plyr,"fort_deputy_discuss_options", [],
    "That is all for now.", "close_window", []],
  [anyone,"mayor_wealth_comparison_1",[

  (assign, ":wealthiest_center", "$g_encountered_party"),
  (assign, ":poorer_centers", 0),
  (assign, ":richer_centers", 0),

  (party_get_slot, ":wealthiest_center_wealth", "$g_encountered_party", slot_town_prosperity),
  (party_get_slot, ":mayor_center_wealth", "$g_encountered_party", slot_town_prosperity),

  (try_for_range, ":other_center", towns_begin, towns_end),
	(neq, ":other_center", "$g_encountered_party"),
	(party_get_slot, ":other_center_wealth", ":other_center", slot_town_prosperity),
	(try_begin),
		(gt, ":other_center_wealth", ":wealthiest_center_wealth"),
		(val_add, ":richer_centers", 1),
		(assign, ":wealthiest_center", ":other_center"),
		(assign, ":wealthiest_center_wealth", ":other_center_wealth"),
    (else_try),
		(gt, ":other_center_wealth", ":mayor_center_wealth"),
		(val_add, ":richer_centers", 1),
    (else_try),
		(val_add, ":poorer_centers", 1),
    (try_end),
  (try_end),

  (assign, reg4, ":richer_centers"),
  (assign, reg5, ":poorer_centers"),
  (str_store_party_name, s5, "$g_encountered_party"),
  (str_store_party_name, s4, ":wealthiest_center"),

  ], "Overall, the wealthiest town in Japan is known to be {s4}. Here in {s5}, we are poorer than {reg4} towns, and richer than {reg5}.", "mayor_wealth_comparison_2",[
  ]],
  #Production of this town
  #Production of the hinterland
  #Volume of trade

  [anyone,"mayor_wealth_comparison_2",[

  (assign, ":wealthiest_center", "$g_encountered_party"),
  (assign, ":poorer_centers", 0),
  (assign, ":richer_centers", 0),

  (assign, ":mayor_town_production", 0),
  (try_for_range, ":item_kind_id", trade_goods_begin, trade_goods_end),
	(call_script, "script_center_get_production", "$g_encountered_party", ":item_kind_id"),
	(val_add, ":mayor_town_production", reg0),
  (try_end),
  (assign, ":wealthiest_town_production", ":mayor_town_production"),

  (try_begin),
	(ge, "$cheat_mode", 1),
	(assign, reg4, ":mayor_town_production"),
	(str_store_party_name, s4, "$g_encountered_party"),
	(display_message, "@{!}DEBUG -- Total production for {s4}: {reg4}"),
  (try_end),


  (try_for_range, ":other_center", towns_begin, towns_end),
	(neq, ":other_center", "$g_encountered_party"),
	(assign, ":other_town_production", 0),
	(try_for_range, ":item_kind_id", trade_goods_begin, trade_goods_end),
		(call_script, "script_center_get_production", ":other_center", ":item_kind_id"),
		(val_add, ":other_town_production", reg0),
	(try_end),
	(try_begin),
		(ge, "$cheat_mode", 1),
		(assign, reg4, ":other_town_production"),
		(str_store_party_name, s4, ":other_center"),
		(display_message, "@{!}DEBUG -- Total production for {s4}: {reg4}"),
	(try_end),

	(try_begin),
		(gt, ":other_town_production", ":wealthiest_town_production"),
		(val_add, ":richer_centers", 1),
		(assign, ":wealthiest_center", ":other_center"),
		(assign, ":wealthiest_town_production", ":other_town_production"),
    (else_try),
		(gt, ":other_town_production", ":mayor_town_production"),
		(val_add, ":richer_centers", 1),
    (else_try),
		(val_add, ":poorer_centers", 1),
    (try_end),
  (try_end),

  (assign, reg4, ":richer_centers"),
  (assign, reg5, ":poorer_centers"),
  (str_store_party_name, s5, "$g_encountered_party"),
  (str_store_party_name, s4, ":wealthiest_center"),

  ], "In terms of local industry, the most productive town in Japan is known to be {s4}. Here in {s5}, we produce less than {reg4} towns, and produce more than {reg5}. Production is of course affected by the supply of raw materials, as well as by the overall prosperity of the town.", "mayor_wealth_comparison_3",[
  ]],
  [anyone,"mayor_wealth_comparison_3",[

  (assign, ":wealthiest_center", "$g_encountered_party"),
  (assign, ":poorer_centers", 0),
  (assign, ":richer_centers", 0),

  (try_for_range, ":town", towns_begin, towns_end),
	(party_set_slot, ":town", slot_party_temp_slot_1, 0),
  (try_end),

  (try_for_range, ":village", villages_begin, villages_end),
	(assign, ":village_good_production", 0),
	(try_for_range, ":item_kind_id", trade_goods_begin, trade_goods_end),
		(call_script, "script_center_get_production", ":village", ":item_kind_id"),
		(val_add, ":village_good_production", reg0),
	(try_end),
	(party_get_slot, ":market_town", ":village", slot_village_market_town),
	(party_get_slot, ":market_center_production", ":market_town", slot_party_temp_slot_1),
	(val_add, ":market_center_production", ":village_good_production"),
	(party_set_slot, ":market_town", slot_party_temp_slot_1, ":market_center_production"),
  (try_end),


  (party_get_slot, ":mayor_town_production", "$g_encountered_party", slot_party_temp_slot_1),
  (assign, ":wealthiest_town_production", ":mayor_town_production"),

  (try_begin),
	(ge, "$cheat_mode", 1),
	(assign, reg4, ":mayor_town_production"),
	(str_store_party_name, s4, "$g_encountered_party"),
	(display_message, "@{!}DEBUG -- Total rural production for {s4} region: {reg4}"),
  (try_end),


  (try_for_range, ":other_center", towns_begin, towns_end),
	(neq, ":other_center", "$g_encountered_party"),
	(party_get_slot, ":other_town_production", ":other_center", slot_party_temp_slot_1),

	(try_begin),
		(ge, "$cheat_mode", 1),
		(assign, reg4, ":other_town_production"),
		(str_store_party_name, s4, ":other_center"),
		(display_message, "@{!}DEBUG -- Total rural production for {s4} region: {reg4}"),
	(try_end),

	(try_begin),
		(gt, ":other_town_production", ":wealthiest_town_production"),
		(val_add, ":richer_centers", 1),
		(assign, ":wealthiest_center", ":other_center"),
		(assign, ":wealthiest_town_production", ":other_town_production"),
    (else_try),
		(gt, ":other_town_production", ":mayor_town_production"),
		(val_add, ":richer_centers", 1),
    (else_try),
		(val_add, ":poorer_centers", 1),
    (try_end),
  (try_end),

  (assign, reg4, ":richer_centers"),
  (assign, reg5, ":poorer_centers"),
  (str_store_party_name, s5, "$g_encountered_party"),
  (str_store_party_name, s4, ":wealthiest_center"),

  ], "In terms of the output of the surrounding villages, the town of {s4} is the richest in Japan. Here in {s5}, the villages produce less than the hinterland around {reg4} towns, and produce more than {reg5}. The wealth of a town's hinterland, of course, is heavily dependent on the tides of war. Looting and pillage, and shifts in territory, can make a major impact.", "mayor_wealth_comparison_4",[
  ]],
  [anyone,"mayor_wealth_comparison_4",[

  (assign, ":wealthiest_center", "$g_encountered_party"),
  (assign, ":poorer_centers", 0),
  (assign, ":richer_centers", 0),

  (try_for_range, ":town", towns_begin, towns_end),
	(party_set_slot, ":town", slot_party_temp_slot_1, 0),
  (try_end),

  (try_for_range, ":log_entry_iterator", 0, "$num_log_entries"),
	(store_sub, ":log_entry_no", "$num_log_entries", ":log_entry_iterator"),
    (troop_slot_eq, "trp_log_array_entry_type", ":log_entry_no", logent_party_traded),

    (troop_get_slot, ":event_time",            "trp_log_array_entry_time",              ":log_entry_no"),
	(store_current_hours, ":cur_hour"),
	(store_sub, ":hours_ago", ":cur_hour", ":event_time"),
	(lt, ":hours_ago", 1344),

    (troop_get_slot, ":origin",    "trp_log_array_center_object",          ":log_entry_no"),
	(is_between, ":origin", towns_begin, towns_end), #exclude village trading here

    (troop_get_slot, ":destination",    "trp_log_array_troop_object",          ":log_entry_no"),
	(party_get_slot, ":num_visits", ":destination", slot_party_temp_slot_1),
	(val_add, ":num_visits", 1),
	(party_set_slot, ":destination", slot_party_temp_slot_1, ":num_visits"),
  (try_end),

  (party_get_slot, ":mayor_town_production", "$g_encountered_party", slot_party_temp_slot_1),
  (assign, ":wealthiest_town_production", ":mayor_town_production"),

  (try_begin),
	(ge, "$cheat_mode", 1),
	(assign, reg4, ":mayor_town_production"),
	(str_store_party_name, s4, "$g_encountered_party"),
	(display_message, "@{!}DEBUG -- Total trade for {s4}: {reg4}"),
  (try_end),


  (try_for_range, ":other_center", towns_begin, towns_end),
	(neq, ":other_center", "$g_encountered_party"),
	(party_get_slot, ":other_town_production", ":other_center", slot_party_temp_slot_1),

	(try_begin),
		(ge, "$cheat_mode", 1),
		(assign, reg4, ":other_town_production"),
		(str_store_party_name, s4, ":other_center"),
		(display_message, "@{!}DEBUG -- Total trade for {s4}: {reg4}"),
	(try_end),

	(try_begin),
		(gt, ":other_town_production", ":wealthiest_town_production"),
		(val_add, ":richer_centers", 1),
		(assign, ":wealthiest_center", ":other_center"),
		(assign, ":wealthiest_town_production", ":other_town_production"),
    (else_try),
		(gt, ":other_town_production", ":mayor_town_production"),
		(val_add, ":richer_centers", 1),
    (else_try),
		(val_add, ":poorer_centers", 1),
    (try_end),
  (try_end),

  (assign, reg4, ":richer_centers"),
  (assign, reg5, ":poorer_centers"),
  (str_store_party_name, s5, "$g_encountered_party"),
  (str_store_party_name, s4, ":wealthiest_center"),

  ], "In terms of trade, the town of {s4} is believed to have received the most visits from caravans over the past few months. Here in {s5}, we are less visited than {reg4} towns, and more visited than {reg5}. ", "mayor_wealth_comparison_5",[
  ]],
  [anyone,"mayor_wealth_comparison_5",[

  (assign, ":wealthiest_center", "$g_encountered_party"),
  (assign, ":poorer_centers", 0),
  (assign, ":richer_centers", 0),

  (try_for_range, ":town", towns_begin, towns_end),
	(party_set_slot, ":town", slot_party_temp_slot_1, 0),
  (try_end),

  (try_for_range, ":log_entry_iterator", 0, "$num_log_entries"),
	(store_sub, ":log_entry_no", "$num_log_entries", ":log_entry_iterator"),
    (troop_slot_eq, "trp_log_array_entry_type", ":log_entry_no", logent_traveller_attacked),

    (troop_get_slot, ":event_time",            "trp_log_array_entry_time",              ":log_entry_no"),
	(store_current_hours, ":cur_hour"),
	(store_sub, ":hours_ago", ":cur_hour", ":event_time"),
	(lt, ":hours_ago", 1344),

    (troop_get_slot, ":origin",    "trp_log_array_center_object",          ":log_entry_no"),
    (troop_get_slot, ":destination",    "trp_log_array_troop_object",          ":log_entry_no"),

	(try_begin),
		(is_between, ":destination", towns_begin, towns_end),
		(party_get_slot, ":num_attacks", ":destination", slot_party_temp_slot_1),
		(val_add, ":num_attacks", 1),
		(party_set_slot, ":destination", slot_party_temp_slot_1, ":num_attacks"),
	(try_end),

	(try_begin),
		(is_between, ":origin", towns_begin, towns_end),
		(party_get_slot, ":num_attacks", ":origin", slot_party_temp_slot_1),
		(val_add, ":num_attacks", 1),
		(party_set_slot, ":origin", slot_party_temp_slot_1, ":num_attacks"),
	(try_end),
  (try_end),

  (party_get_slot, ":mayor_town_production", "$g_encountered_party", slot_party_temp_slot_1),
  (assign, ":wealthiest_town_production", ":mayor_town_production"),

  (try_begin),
	(ge, "$cheat_mode", 1),
	(assign, reg4, ":mayor_town_production"),
	(str_store_party_name, s4, "$g_encountered_party"),
	(display_message, "@{!}DEBUG -- Total attacks for {s4}: {reg4}"),
  (try_end),


  (try_for_range, ":other_center", towns_begin, towns_end),
	(neq, ":other_center", "$g_encountered_party"),
	(party_get_slot, ":other_town_production", ":other_center", slot_party_temp_slot_1),

	(try_begin),
		(ge, "$cheat_mode", 1),
		(assign, reg4, ":other_town_production"),
		(str_store_party_name, s4, ":other_center"),
		(display_message, "@{!}DEBUG -- Total attacks for {s4}: {reg4}"),
	(try_end),

	(try_begin),
		(gt, ":other_town_production", ":wealthiest_town_production"),
		(val_add, ":richer_centers", 1),
		(assign, ":wealthiest_center", ":other_center"),
		(assign, ":wealthiest_town_production", ":other_town_production"),
    (else_try),
		(gt, ":other_town_production", ":mayor_town_production"),
		(val_add, ":richer_centers", 1),
    (else_try),
		(val_add, ":poorer_centers", 1),
    (try_end),
  (try_end),

  (assign, reg4, ":richer_centers"),
  (assign, reg5, ":poorer_centers"),
  (str_store_party_name, s5, "$g_encountered_party"),
  (str_store_party_name, s4, ":wealthiest_center"),

  ], "In terms of attacks on travellers, the town of {s4} is believed to be the most dangerous. Here in {s5}, we are less afflicted by bandits and raiders than {reg4} towns, and more afflicted than {reg5}. ", "mayor_pretalk",[
  ]],
]
