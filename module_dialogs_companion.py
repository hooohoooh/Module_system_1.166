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

dialogs_companion = [
[anyone ,"member_chat", [
         (store_conversation_troop, "$g_talk_troop"),
              (try_begin),
				  #gekokujo 3.0 microfactions! include fort companions start
                  #(is_between, "$g_talk_troop", companions_begin, companions_end),
                  (is_between, "$g_talk_troop", companions_begin, fort_companions_end),
				  #gekokujo 3.0 microfactions! include fort companions end
                  (talk_info_show, 1),
                  (call_script, "script_setup_talk_info_companions"),
              (else_try),
                  (is_between, "$g_talk_troop", pretenders_begin, pretenders_end),
                  (talk_info_show, 1),
                  (call_script, "script_setup_talk_info"),
              (try_end),

			##diplomacy start+ Get gender for troop
			##OLD: #(troop_get_type, reg65, "$g_talk_troop"),
			(assign, reg65, 0),
			(try_begin),
				(call_script, "script_cf_dplmc_troop_is_female", "$g_talk_troop"),
				(assign, reg65, 1),
			(try_end),

            ##ALSO OLD: #  (troop_get_type, reg65, "$g_talk_troop"),
 			##diplomacy end+
              (try_begin),
                  (faction_slot_eq,"$g_talk_troop_faction",slot_faction_leader,"$g_talk_troop"),
                  (str_store_string,s64,"@{reg65?my Lady:my Lord}"), #bug fix
                  (str_store_string,s65,"@{reg65?my Lady:my Lord}"),
                  (str_store_string,s66,"@{reg65?My Lady:My Lord}"),
              (else_try),
                  (str_store_string,s64,"@{reg65?madame:sir}"), #bug fix
                  (str_store_string,s65,"@{reg65?madame:sir}"),
                  (str_store_string,s66,"@{reg65?Madame:Sir}"),
              (try_end),

         (store_current_hours, "$g_current_hours"),
         (troop_set_slot, "$g_talk_troop", slot_troop_last_talk_time, "$g_current_hours"),

              (eq, 1, 0)],
"{!}Warning: This line is never displayed. It is just for storing conversation variables.", "close_window", []],
[anyone,"member_chat",
[
(troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_lady),
], "{playername}, when do you think we can reach our destination?", "member_lady_1",[]],
[anyone ,"member_chat", [(is_between, "$g_talk_troop", pretenders_begin, pretenders_end),],
"Greetings, {playername}, my first and foremost vassal. I await your counsel.", "supported_pretender_talk", []],
[anyone,"member_chat", [
    (store_conversation_troop,"$g_talk_troop"),
    (troop_is_hero,"$g_talk_troop"),
	(try_begin),
	  (is_between, "$g_talk_troop", fort_companions_begin, fort_companions_end),
      (str_store_string, s5, "@tono"),
	(else_try),
      (troop_get_slot, ":honorific", "$g_talk_troop", slot_troop_honorific),
      (str_store_string, s5, ":honorific"),
	(try_end),
  ], "Yes, {s5}?", "member_talk", [
    (try_begin),
      #gekokujo 3.0 microfactions! include fort companions start
      #(is_between, "$g_talk_troop", companions_begin, companions_end),
      (is_between, "$g_talk_troop", companions_begin, fort_companions_end),
      #gekokujo 3.0 microfactions! include fort companions end
      (unlock_achievement, ACHIEVEMENT_TALKING_HELPS),
    (try_end),
  ]],
[anyone|plyr, "companion_recruit_intro_response", [
               (troop_get_slot, ":intro_response", "$g_talk_troop", slot_troop_intro_response_1),
               (str_store_string, 6, ":intro_response")
], "{s6}", "companion_recruit_backstory_a", []],
[anyone|plyr, "companion_recruit_intro_response", [
               (troop_get_slot, ":intro_response", "$g_talk_troop", slot_troop_intro_response_2),
               (str_store_string, 7, ":intro_response")
],  "{s7}", "close_window", [
    ]],
[anyone, "companion_recruit_backstory_a", [(troop_get_slot, ":backstory_a", "$g_talk_troop", slot_troop_backstory_a),
               (str_store_string, 5, ":backstory_a"),
               (str_store_string, 19, "str_here_plus_space"),
               (str_store_party_name, 20, "$g_encountered_party"),
],
"{s5}", "companion_recruit_backstory_b", []],
[anyone, "companion_recruit_backstory_b", [(troop_get_slot, ":backstory_b", "$g_talk_troop", slot_troop_backstory_b),
               (str_store_string, 5, ":backstory_b"),
               (str_store_party_name, 20, "$g_encountered_party"),
],
"{s5}", "companion_recruit_backstory_c", []],
[anyone, "companion_recruit_backstory_c", [(troop_get_slot, ":backstory_c", "$g_talk_troop", slot_troop_backstory_c),
               (str_store_string, 5, ":backstory_c"),
],
"{s5}", "companion_recruit_backstory_response", []],
[anyone|plyr, "companion_recruit_backstory_response", [
               (troop_get_slot, ":backstory_response", "$g_talk_troop", slot_troop_backstory_response_1),
               (str_store_string, 6, ":backstory_response")
], "{s6}", "companion_recruit_signup", []],
[anyone|plyr, "companion_recruit_backstory_response", [
               (troop_get_slot, ":backstory_response", "$g_talk_troop", slot_troop_backstory_response_2),
               (str_store_string, 7, ":backstory_response")
],  "{s7}", "close_window", [
    ]],
[anyone, "companion_recruit_signup", [(troop_get_slot, ":signup", "$g_talk_troop", slot_troop_signup),
               (str_store_string, 5, ":signup"),
               (str_store_party_name, 20, "$g_encountered_party"),

],
"{s5}", "companion_recruit_signup_b", []],
[anyone, "companion_recruit_signup_b", [
(troop_get_slot, ":signup", "$g_talk_troop", slot_troop_signup_2),
(troop_get_slot, reg3, "$g_talk_troop", slot_troop_payment_request),#

(str_store_string, 5, ":signup"),
(str_store_party_name, 20, "$g_encountered_party"),

],
"{s5}", "companion_recruit_signup_response", []],
[anyone|plyr, "companion_recruit_signup_response", [(neg|hero_can_join, "p_main_party"),], "Unfortunately, I can't take on any more hands in my party right now.", "close_window", [
]],
[anyone|plyr, "companion_recruit_signup_response", [
              (hero_can_join, "p_main_party"),
              (troop_get_slot, ":signup_response", "$g_talk_troop", slot_troop_signup_response_1),
              (str_store_string, 6, ":signup_response")
], "{s6}", "companion_recruit_payment", []],
[anyone|plyr, "companion_recruit_signup_response", [
              (hero_can_join, "p_main_party"),
               (troop_get_slot, ":signup_response", "$g_talk_troop", slot_troop_signup_response_2),
               (str_store_string, 7, ":signup_response")
],  "{s7}", "close_window", [
    ]],
[anyone|auto_proceed, "companion_recruit_payment", [
(troop_slot_eq, "$g_talk_troop", slot_troop_payment_request, 0),
],
".", "companion_recruit_signup_confirm", []],
[anyone, "companion_recruit_payment", [
(store_sub, ":npc_offset", "$g_talk_troop", "trp_npc1"),
(store_add, ":dialog_line", "str_npc1_payment", ":npc_offset"),
(str_store_string, s5, ":dialog_line"),
(troop_get_slot, reg3, "$g_talk_troop", slot_troop_payment_request),
(str_store_party_name, s20, "$g_encountered_party"),
],
"{s5}", "companion_recruit_payment_response", []],
[anyone|plyr, "companion_recruit_payment_response", [
              (hero_can_join, "p_main_party"),
              (troop_get_slot, ":amount_requested", "$g_talk_troop", slot_troop_payment_request),#
              (store_troop_gold, ":gold", "trp_player"),#
              (ge, ":gold", ":amount_requested"),#
              (assign, reg3, ":amount_requested"),
              (store_sub, ":npc_offset", "$g_talk_troop", "trp_npc1"),
              (store_add, ":dialog_line", "str_npc1_payment_response", ":npc_offset"),
              (str_store_string, s6, ":dialog_line"),
], "{s6}", "companion_recruit_signup_confirm", [
              (troop_get_slot, ":amount_requested", "$g_talk_troop", slot_troop_payment_request),#
              (gt, ":amount_requested", 0),#
              (troop_remove_gold, "trp_player", ":amount_requested"),  #
              (troop_set_slot, "$g_talk_troop", slot_troop_payment_request, 0),#
    ]],
[anyone|plyr, "companion_recruit_payment_response", [
               (troop_get_slot, ":signup_response", "$g_talk_troop", slot_troop_signup_response_2),
               (str_store_string, s7, ":signup_response")
],  "Sorry. I can't afford that at the moment.", "close_window", [
    ]],
[anyone|plyr, "companion_recruit_meet_again", [
], "So... What have you been doing since our last encounter?", "companion_recruit_backstory_delayed", []],
[anyone|plyr, "companion_recruit_meet_again", [
],  "Good day to you.", "close_window", [
    ]],
[anyone|plyr, "companion_recruit_secondchance", [
], "My apologies if I was rude, earlier. What was your story again?", "companion_recruit_backstory_b", []],
[anyone|plyr, "companion_recruit_secondchance", [
],  "Never mind.", "close_window", [
    ]],
[anyone, "companion_recruit_backstory_delayed",
[(troop_get_slot, ":backstory_delayed", "$g_talk_troop", slot_troop_backstory_delayed),
(str_store_string, 5, ":backstory_delayed")
],
"{s5}", "companion_recruit_backstory_delayed_response", []],
[anyone|plyr, "companion_recruit_backstory_delayed_response", [
], "I might be able to use you as a retainer under my banners.", "companion_recruit_signup_b", [
    ]],
[anyone|plyr, "companion_recruit_backstory_delayed_response", [
],  "I'll let you know if I hear of anything.", "close_window", [
    ]],
[anyone, "companion_recruit_signup_confirm", [], "Good! Give me a few moments to prepare and I'll be ready to move.", "close_window",
[(call_script, "script_recruit_troop_as_companion", "$g_talk_troop")]],
[anyone,"companion_prison_break_chains", [],
"Thank the gods you came! However, I'm not going anywhere with these chains on my legs. You'll need to get the key away from the guard somehow.", "close_window",[]],
[anyone, "companion_was_dismissed", [
          (neg|troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_hero),
                (troop_get_slot, ":speech", "$g_talk_troop", slot_troop_backstory_delayed),
               (str_store_string, 5, ":speech"),
],
"{s5}. Would you want me to rejoin your company?", "companion_rehire", [
]],
[anyone|plyr, "companion_rehire",
[
(hero_can_join, "p_main_party"),
], "Welcome back, my friend!", "companion_recruit_signup_confirm", []],
[anyone|plyr, "companion_rehire",
[],
"Sorry, I can't take on anyone else right now.", "companion_rehire_refused", []],
[anyone, "companion_rehire_refused", [], "Well... Look me up if you change your mind, eh?", "close_window",
[
(troop_get_slot, ":current_town_no", "$g_talk_troop", slot_troop_cur_center),

(try_begin),
 (neg|is_between, ":current_town_no", towns_begin, towns_end),

 (store_random_in_range, ":town_no", towns_begin, towns_end),
 (troop_set_slot, "$g_talk_troop", slot_troop_cur_center, ":town_no"),

 (try_begin),
   (ge, "$cheat_mode", 1),
   (assign, reg1, ":current_town_no"),
   (str_store_party_name, s7, ":town_no"),
   (display_message, "@{!}current town was {reg1}, now moved to {s7}"),
 (try_end),
(try_end),
]],
##he doesn't want a center but we can pay him
[anyone, "companion_embassy_results", [
(troop_slot_eq, "$g_talk_troop", slot_troop_current_mission, npc_mission_peace_request),
(troop_get_slot, ":mission_object", "$g_talk_troop", slot_troop_mission_object),
##diplomacy start+ save the results of the script to avoid unnecessary repeated calls,
#which may introduce unexpected behavior if it's changed to used random numbers.
(call_script, "script_dplmc_get_truce_pay_amount", "fac_player_supporters_faction", ":mission_object", "$g_mission_result"),
(assign, "$temp", reg0),
(assign, "$temp_2", reg1),
##diplomacy end+
(faction_get_slot, ":emissary_object", ":mission_object", slot_faction_leader),
(str_store_troop_name, s12, ":emissary_object"),
(is_between, "$g_mission_result", -2, 1), #-2 or -1 or 0
##diplomacy start+
#(call_script, "script_dplmc_get_truce_pay_amount", "fac_player_supporters_faction", ":mission_object", "$g_mission_result"),
(gt, "$temp", 0),
(lt, "$temp_2", 0),
(assign, reg4, 0),#Use reg4 for gender
(try_begin),
	(call_script, "script_cf_dplmc_troop_is_female", ":emissary_object"),
	(assign, reg4, 1),
(try_end),
],
"{s12} says that {reg4?she:he} is willing to consider a truce of twenty days if you pay {reg4?her:him} {reg0} mon.","dplmc_companion_truce_pay", [
         ]],
##diplomacy end+

##we can pay him or pay him and give a center
[anyone, "companion_embassy_results", [
(troop_slot_eq, "$g_talk_troop", slot_troop_current_mission, npc_mission_peace_request),
(troop_get_slot, ":mission_object", "$g_talk_troop", slot_troop_mission_object),
(faction_get_slot, ":emissary_object", ":mission_object", slot_faction_leader),
(str_store_troop_name, s12, ":emissary_object"),
(is_between, "$g_mission_result", -2, 1), #-2 or -1 or 0
##diplomacy start+
#(call_script, "script_dplmc_get_truce_pay_amount", "fac_player_supporters_faction", ":mission_object", "$g_mission_result"),
(gt, "$temp", 0),
(gt, "$temp_2", 0),
(assign, reg0, "$temp"),
(assign, reg1, "$temp_2"),
(str_store_party_name, s18, "$g_concession_demanded"),
(assign, reg4, 0),#Use reg4 for gender
(try_begin),
	(call_script, "script_cf_dplmc_troop_is_female", ":emissary_object"),
	(assign, reg4, 1),
(try_end),
],
##next line fixed diplomacy bug, companion_truce_pay -> dplmc_companion_truce_pay; also gender from reg4
"{s12} says that {reg4?she:he} is willing to consider a truce of twenty days if you yield to {reg4?her:his} terms. Either you pay {reg0} mon or you pay {reg1} mon and give {reg4?her:him} {s18}.","dplmc_companion_truce_pay", [
         ]],
##diplomacy end+

##diplomacy start+
#Missing options: will only accept a center / will only accept a center and money
[anyone, "companion_embassy_results", [
(troop_slot_eq, "$g_talk_troop", slot_troop_current_mission, npc_mission_peace_request),
(troop_get_slot, ":mission_object", "$g_talk_troop", slot_troop_mission_object),
(faction_get_slot, ":emissary_object", ":mission_object", slot_faction_leader),
(str_store_troop_name, s12, ":emissary_object"),
(is_between, "$g_mission_result", -2, 1), #-2 or -1 or 0,
(le, "$temp", 0),
(eq, "$temp_2", 0),
(str_store_party_name, s18, "$g_concession_demanded"),
(assign, reg4, 0),
(try_begin),
	(call_script, "script_cf_dplmc_troop_is_female", ":emissary_object"),
	(assign, reg4, 1),
(try_end),
],#Next line: gender from reg4
"{s12} says that {reg4?she:he} is willing to consider a truce of twenty days if you give {reg4?her:him} {s18}.","dplmc_companion_truce_pay", [
         ]],
 ##diplomacy end+

[anyone, "companion_embassy_results", [
(troop_slot_eq, "$g_talk_troop", slot_troop_current_mission, npc_mission_peace_request),
(troop_get_slot, ":mission_object", "$g_talk_troop", slot_troop_mission_object),
(faction_get_slot, ":emissary_object", ":mission_object", slot_faction_leader),
(str_store_troop_name, s12, ":emissary_object"),
(is_between, "$g_mission_result", -2, 1), #-2 or -1 or 0,
(le, "$temp", 0),
(ge, "$temp_2", 1),
(assign, reg0, "$temp_2"),
(str_store_party_name, s18, "$g_concession_demanded"),
##diplomacy start+ Make gender correct
(assign, reg4, 0),
(try_begin),
	(call_script, "script_cf_dplmc_troop_is_female", ":emissary_object"),
	(assign, reg4, 1),
(try_end),
],#Next line: gender from reg4
"{s12} says that {reg4?she:he} is willing to consider a truce of twenty days if you pay {reg4?her:him} {reg0} mon and give {reg4?her:him} {s18}.","dplmc_companion_truce_pay", [
         ]],
##diplomacy end+

##we can pay him or give the center
[anyone, "companion_embassy_results", [
(troop_slot_eq, "$g_talk_troop", slot_troop_current_mission, npc_mission_peace_request),
(troop_get_slot, ":mission_object", "$g_talk_troop", slot_troop_mission_object),
(faction_get_slot, ":emissary_object", ":mission_object", slot_faction_leader),
(str_store_troop_name, s12, ":emissary_object"),
(is_between, "$g_mission_result", -2, 1), #-2 or -1 or 0
##diplomacy start+
#(call_script, "script_dplmc_get_truce_pay_amount", "fac_player_supporters_faction", ":mission_object", "$g_mission_result"),
(gt, "$temp", 0),
(eq, "$temp_2", 0),
(assign, reg0, "$temp"),
(str_store_party_name, s18, "$g_concession_demanded"),
(assign, reg4, 0),
(try_begin),
	(call_script, "script_cf_dplmc_troop_is_female", ":emissary_object"),
	(assign, reg4, 1),
(try_end),
],#Next line gender from reg4
"{s12} says that {reg4?she:he} is willing to consider a truce of twenty days if you pay {reg4?her:him} {reg0} or give {reg4?her:him} {s18}.","dplmc_companion_truce_pay", [
         ]],
#This was bugged, and should logically never occur.
##we have so many prisoners we don't have to pay
#[anyone, "companion_embassy_results", [
#  (troop_slot_eq, "$g_talk_troop", slot_troop_current_mission, npc_mission_peace_request),#
#		(troop_get_slot, ":mission_object", "$g_talk_troop", slot_troop_mission_object),
#		(faction_get_slot, ":emissary_object", ":mission_object", slot_faction_leader),
#		(str_store_troop_name, s12, ":emissary_object"),
#		(is_between, "$g_mission_result", -2, 1), #-2 or -1 or 0
#  (call_script, "script_dplmc_get_truce_pay_amount", "fac_player_supporters_faction", ":mission_object", "$g_mission_result"),
#  (eq, reg0, 0),
#  (le, reg1, 0),
#],
# "{s12} says that he is willing to consider a truce of twenty days.","companion_truce_confirm", [
#					]],
##diplomacy end+

##option to pay him
[anyone|plyr, "dplmc_companion_truce_pay", [
(troop_get_slot, ":mission_object", "$g_talk_troop", slot_troop_mission_object),
(str_store_faction_name, s4, ":mission_object"),
(store_troop_gold, ":gold", "trp_player"),#
##diplomacy start+
(assign, reg0, "$temp"),
(gt, reg0, 0),
(ge, ":gold", reg0),
],
"Pay {reg0} mon and let the truce with the {s4} be concluded","companion_rejoin_response", [
(troop_get_slot, ":mission_object", "$g_talk_troop", slot_troop_mission_object),
(troop_remove_gold, "trp_player", "$temp"),#todo change amount
#actually give gold to other kingdom
(call_script, "script_dplmc_faction_leader_splits_gold", ":mission_object", "$temp"),
##diplomacy end+
(call_script, "script_diplomacy_start_peace_between_kingdoms", ":mission_object", "$players_kingdom", 1),
(str_store_faction_name, s4, ":mission_object"),
]],
### This is also where the dialogue jumps if the player initiates quitting dialogue and the companion has low morale
##diplomacy start+
#Hijack this for lorded companions who temporarily rejoined your party, and the like.
[anyone, "companion_quitting", [
               (store_conversation_troop, "$map_talk_troop"),
			   (assign, ":has_fief", 0),
			   (try_for_range_backwards, ":center_no", centers_begin, centers_end),
			      (party_slot_eq, ":center_no", slot_town_lord, "$map_talk_troop"),
				  (assign, ":has_fief", 1),
			   (try_end),
			   (this_or_next|eq, ":has_fief", 1),
			   (this_or_next|is_between, "$map_talk_troop", lords_begin, lords_end),
			   (this_or_next|is_between, "$map_talk_troop", pretenders_begin, pretenders_end),
			   (this_or_next|is_between, "$map_talk_troop", kings_begin, kings_end),
               (this_or_next|troop_slot_eq, "$map_talk_troop", slot_troop_occupation, slto_kingdom_hero),
			   (this_or_next|troop_slot_eq, "$map_talk_troop", slot_troop_playerparty_history, dplmc_pp_history_granted_fief),
               (troop_slot_eq, "$map_talk_troop", slot_troop_playerparty_history, dplmc_pp_history_lord_rejoined),
               ],
"It has been good travelling with you, but I must return to my own affairs.", "dplmc_companion_quitting_lord_1",
	[]],
##diplomacy end+
### This is also where the dialogue jumps if the player initiates quitting dialogue and the companion has low morale
[anyone, "companion_quitting", [
               (store_conversation_troop, "$map_talk_troop"),
               (troop_get_slot, ":speech", "$map_talk_troop", slot_troop_retirement_speech),
               (str_store_string, 5, ":speech")
               ],
"{s5}", "companion_quitting_2", [
 ]],
## The companion explains his/her reasons for quitting
[anyone, "companion_quitting_2", [
              (call_script, "script_npc_morale", "$map_talk_troop"),
               ],
"To tell you the truth, {s21}", "companion_quitting_response", [
 ]],
[anyone|plyr, "companion_quitting_response", [
], "Very well. You be off, then.", "companion_quitting_yes", [
    ]],
##diplomacy start+  Alter the "persuade to stay" conversation, and redirect it.
[anyone|plyr, "companion_quitting_response", [
          (eq, "$player_can_persuade_npc", 1),
#], "Perhaps I can persuade you to change your mind.", "companion_quitting_persuasion", [#<- dplmc replace
], "Perhaps I can persuade you to change your mind.", "dplmc_companion_quitting_persuasion_start", [#<- dplmc add
##diplomacy end+
      (assign, "$player_can_persuade_npc", 0),
    ]],
##diplomacy end+

[anyone, "companion_quitting_persuasion", [
          (store_random_in_range, ":random", -2, 13),
          (store_skill_level, ":persuasion", "skl_persuasion", "trp_player"),
  		  ##diplomacy start+
	  	  #Because this pertains to the handling of subordinates, in my
		  #opinion skl_leadership is also directly relevant (especially since
		  #this is how it works with non-hero troops, where your leadership
		  #raises their morale and makes them less likely to desert).
 		  (store_skill_level, reg0, "skl_leadership", "trp_player"),
		  (val_max, ":persuasion", reg0),
		  ##diplomacy end+

          (le, ":random", ":persuasion"),
               ],
"Hm. When you put it like that, I suppose I can stay a while longer, see if things improve.", "close_window",
[
          (troop_get_slot, ":morality_penalties", "$map_talk_troop", slot_troop_morality_penalties),
          (val_div, ":morality_penalties", 2),
          (troop_set_slot, "$map_talk_troop", slot_troop_morality_penalties, ":morality_penalties"),

          (troop_get_slot, ":personalityclash_penalties", "$map_talk_troop", slot_troop_personalityclash_penalties),
          (val_div, ":personalityclash_penalties", 2),
          (troop_set_slot, "$map_talk_troop", slot_troop_personalityclash_penalties, ":personalityclash_penalties"),
 ]],
[anyone, "companion_quitting_persuasion", [
               ],
"I'm sorry, but I don't see your point. I am leaving whether you like it or not.", "companion_quitting_response",
[
 ]],
##diplomacy start+
#Enable refusing to allow party members to quit in cheat mode.
#
#OLD VERSION:
#[anyone|plyr, "companion_quitting_response", [
#      (eq, 1, 0),
#      (eq, "$player_can_refuse_npc_quitting", 1),
#], "We hang deserters in this company.", "companion_quitting_no", [
#    ]],
#
[anyone|plyr, "companion_quitting_response", [
      (ge, "$cheat_mode", 1),#only enable in cheat mode
      (eq, "$player_can_refuse_npc_quitting", 1),
], "CHEAT -- We hang deserters in this company.", "companion_quitting_no", [
    ]],
#Add a response with a slightly different flavor for less mild personalities.
[anyone, "companion_quitting_no", [
	(troop_get_slot, ":talk_troop_personality", "$g_talk_troop", slot_lord_reputation_type),
	(this_or_next|eq, ":talk_troop_personality", lrep_martial),
	(this_or_next|eq, ":talk_troop_personality", lrep_selfrighteous),
		(eq, ":talk_troop_personality", lrep_quarrelsome),
],
"I believe I misheard you.  You certainly could not have been threatening me.", "companion_quitting_no_confirm", [
 ]],
##diplomacy end+

[anyone, "companion_quitting_no", [],
"Oh... Right... Do you mean that?", "companion_quitting_no_confirm", [
 ]],
[anyone|plyr, "companion_quitting_no_confirm", [],
"Absolutely. You either leave this company by my command, or are carried out in a head bag.", "companion_quitting_no_confirmed", [
##diplomacy start+
#I imagine that most companions wouldn't be too happy about being threatened
#with death.
(call_script, "script_dplmc_get_troop_morality_value", "$g_talk_troop", tmt_egalitarian),
(try_begin),
	(lt, reg0, 0),
	#I am adding an exception.  If you know who this applies to in Native, you
	#might agree with this character interpretation.  My reasons for adding this
	#are:
	# (1) I like it when companions react to circumstances differently.
	# (2) I find this possible scenario funny.
	(call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 1),
(else_try),
	#This is the default case.  A larger relation drop might be more
	#appropriate.  I started off with -5.
	(call_script, "script_change_player_relation_with_troop", "$g_talk_troop", -5),
(try_end),

#It might be interesting to develop this branch further (for example, being
#challenged to single combat) but I'm not sure something like this would have
#wide enough appeal to justify it.

##Approval/disapproval from other NPCs
(try_for_range, ":npc", companions_begin, companions_end),
   (neq, ":npc", "$g_talk_troop"),
   (main_party_has_troop, ":npc"),
   (call_script, "script_dplmc_get_troop_morality_value", ":npc", tmt_egalitarian),
   (try_begin),
	  (lt, reg0, 0),
	  (call_script, "script_change_player_relation_with_troop", ":npc", 1),
   (else_try),
      (gt, reg0, 0),
	  (call_script, "script_change_player_relation_with_troop", ":npc", -1),
   (try_end),
(try_end),
##diplomacy end+
 ]],
[anyone|plyr, "companion_quitting_no_confirm", [],
"No, actually I don't mean that. You are free to leave.", "companion_quitting_yes", [
 ]],
[anyone, "companion_quitting_yes", [
               ],
"Then this is goodbye. Perhaps I'll see you around, {playername}.", "close_window", [
    (troop_set_slot, "$map_talk_troop", slot_troop_playerparty_history, pp_history_quit),
    (call_script, "script_retire_companion", "$map_talk_troop", 100),
 ]],
[anyone, "companion_quitting_no_confirmed", [
],
"Hm. I suppose I'm staying, then.", "close_window", [
 ]],
[anyone|plyr, "companion_objection_response", [
              (eq, "$npc_praise_not_complaint", 1),
], "Thanks, I appreciate your support.", "close_window", [
              (troop_set_slot, "$map_talk_troop", "$npc_grievance_slot", tms_acknowledged),
    ]],
[anyone|plyr, "companion_objection_response", [
              (eq, "$npc_praise_not_complaint", 0),
], "Hopefully it won't happen again.", "close_window", [
              (troop_set_slot, "$map_talk_troop", "$npc_grievance_slot", tms_acknowledged),
    ]],
[anyone|plyr, "companion_objection_response", [
              (eq, "$npc_praise_not_complaint", 0),
],  "Your objection is noted. Now fall back in line.", "close_window", [
              (troop_set_slot, "$map_talk_troop", "$npc_grievance_slot", tms_dismissed),
              (troop_get_slot, ":grievance", "$map_talk_troop", slot_troop_morality_penalties),
              (val_add, ":grievance", 10),
              (troop_set_slot, "$map_talk_troop", slot_troop_morality_penalties, ":grievance"),
    ]],
##  [anyone|plyr, "companion_objection_response", [
##      ],  "I prefer my followers to keep their opinions to themselves.", "close_window", [
##                    (troop_set_slot, "$map_talk_troop", "$npc_grievance_slot", tms_dismissed),
##                    (troop_get_slot, ":grievance", "$map_talk_troop", slot_troop_morality_penalties),
##                    (val_add, ":grievance", 10),
##                    (troop_set_slot, "$map_talk_troop", slot_troop_morality_penalties, ":grievance"),
##                    (assign, "$disable_npc_complaints", 1),
##          ]],



# Personality clash 2 objections
[anyone, "event_triggered", [
               (store_conversation_troop, "$map_talk_troop"),
          (is_between, "$map_talk_troop", companions_begin, companions_end),

               (eq, "$map_talk_troop", "$npc_with_personality_clash_2"),
               (eq, "$npc_map_talk_context", slot_troop_personalityclash2_state),

               (troop_get_slot, ":speech", "$map_talk_troop", slot_troop_personalityclash2_speech),
               (troop_get_slot, ":object", "$map_talk_troop", slot_troop_personalityclash2_object),
               (str_store_troop_name, 11, ":object"),
               (str_store_string, 5, ":speech"),
               ],
"{s5}", "companion_personalityclash2_b", [
              (assign, "$npc_with_personality_clash_2", 0),
              (troop_get_slot, ":grievance", "$map_talk_troop", slot_troop_personalityclash_penalties),
              (val_add, ":grievance", 5),
              (troop_set_slot, "$map_talk_troop", slot_troop_personalityclash_penalties, ":grievance"),

              (troop_get_slot, ":object", "$map_talk_troop", slot_troop_personalityclash2_object),
         (call_script, "script_troop_change_relation_with_troop", "$map_talk_troop", ":object", -15),
 ]],
[anyone, "companion_personalityclash2_b", [
],  "{s5}", "companion_personalityclash2_response", [
               (troop_get_slot, ":speech", "$map_talk_troop", slot_troop_personalityclash2_speech_b),
               (troop_get_slot, ":object", "$map_talk_troop", slot_troop_personalityclash2_object),
               (str_store_troop_name, 11, ":object"),
               (str_store_string, 5, ":speech"),
    ]],
[anyone|plyr, "companion_personalityclash2_response", [
(troop_get_slot, ":object", "$map_talk_troop", slot_troop_personalityclash2_object),
(str_store_troop_name, s11, ":object"),
##diplomacy start+
##OLD:
#(troop_get_type, reg11, ":object"),
##NEW:
(assign, reg11, 0),
(try_begin),
	(call_script, "script_cf_dplmc_troop_is_female", ":object"),
	(assign, reg11, 1),
(try_end),
##diplomacy end+
],  "{s11} is a valuable member of this company. I don't want you picking any more fights with {reg11?her:him}.", "close_window", [
              (troop_set_slot, "$map_talk_troop", slot_troop_personalityclash2_state, pclash_penalty_to_self),
    ]],
[anyone|plyr, "companion_personalityclash2_response", [
(troop_get_slot, ":object", "$map_talk_troop", slot_troop_personalityclash2_object),
(str_store_troop_name, s11, ":object"),
##diplomacy start+
##OLD:
#(troop_get_type, reg11, ":object"),
##NEW:
(assign, reg11, 0),
(try_begin),
	(call_script, "script_cf_dplmc_troop_is_female", ":object"),
	(assign, reg11, 1),
(try_end),
##diplomacy end+
],  "Tell {s11} you have my support in this, and {reg11?she:he} should hold {reg11?her:his} tongue.", "close_window", [
              (troop_set_slot, "$map_talk_troop", slot_troop_personalityclash2_state, pclash_penalty_to_other),
    ]],
[anyone|plyr, "companion_personalityclash2_response", [
],  "I don't have time for your petty dispute. Do not bother me with this again.", "close_window", [
              (troop_set_slot, "$map_talk_troop", slot_troop_personalityclash2_state, pclash_penalty_to_both),
    ]],
##  [anyone|plyr, "companion_personalityclash2_response", [
##      ],  "Your grievance is noted. Now fall back in line.", "close_window", [
##                    (troop_set_slot, "$map_talk_troop", slot_troop_personalityclash2_state, 1),
##          ]],

##  [anyone|plyr, "companion_personalityclash2_response", [
##      ],  "I prefer my followers to keep their opinions to themselves.", "close_window", [
##                    (troop_set_slot, "$map_talk_troop", slot_troop_personalityclash2_state, 1),
##                    (assign, "$disable_npc_complaints", 1),
##          ]],




# Personality clash objections

[anyone, "event_triggered", [
               (store_conversation_troop, "$map_talk_troop"),
          (is_between, "$map_talk_troop", companions_begin, companions_end),

               (eq, "$map_talk_troop", "$npc_with_personality_clash"),
               (eq, "$npc_map_talk_context", slot_troop_personalityclash_state),

               (troop_get_slot, ":speech", "$map_talk_troop", slot_troop_personalityclash_speech),
               (troop_get_slot, ":object", "$map_talk_troop", slot_troop_personalityclash_object),
               (str_store_troop_name, 11, ":object"),
               (str_store_string, 5, ":speech"),
               ],
"{s5}", "companion_personalityclash_b", [
              (assign, "$npc_with_personality_clash", 0),
              (troop_get_slot, ":grievance", "$map_talk_troop", slot_troop_personalityclash_penalties),
              (val_add, ":grievance", 5),
              (troop_set_slot, "$map_talk_troop", slot_troop_personalityclash_penalties, ":grievance"),

              (troop_get_slot, ":object", "$map_talk_troop", slot_troop_personalityclash_object),
         (call_script, "script_troop_change_relation_with_troop", "$map_talk_troop", ":object", -15),

 ]],
[anyone, "companion_personalityclash_b", [
],  "{s5}", "companion_personalityclash_response", [
               (troop_get_slot, ":speech", "$map_talk_troop", slot_troop_personalityclash_speech_b),
               (troop_get_slot, ":object", "$map_talk_troop", slot_troop_personalityclash_object),
               (str_store_troop_name, 11, ":object"),
               (str_store_string, 5, ":speech"),
    ]],
[anyone|plyr, "companion_personalityclash_response", [
(troop_get_slot, ":object", "$map_talk_troop", slot_troop_personalityclash_object),
(str_store_troop_name, s11, ":object"),
##diplomacy start+
##OLD:
#(troop_get_type, reg11, ":object"),
##NEW:
(assign, reg11, 0),
(try_begin),
	(call_script, "script_cf_dplmc_troop_is_female", ":object"),
	(assign, reg11, 1),
(try_end),
##diplomacy end+
],  "{s11} is a capable member of this company. I don't want you picking any more fights with {reg11?her:him}.", "close_window", [
              (troop_set_slot, "$map_talk_troop", slot_troop_personalityclash_state, pclash_penalty_to_self),
    ]],
[anyone|plyr, "companion_personalityclash_response", [
(troop_get_slot, ":object", "$map_talk_troop", slot_troop_personalityclash_object),
(str_store_troop_name, s11, ":object"),
##diplomacy start+
##OLD:
#(troop_get_type, reg11, ":object"),
##NEW:
(assign, reg11, 0),
(try_begin),
	(call_script, "script_cf_dplmc_troop_is_female", ":object"),
	(assign, reg11, 1),
(try_end),
##diplomacy end+
],  "Tell {s11} you have my support in this, and {reg11?she:he} should hold {reg11?her:his} tongue.", "close_window", [
              (troop_set_slot, "$map_talk_troop", slot_troop_personalityclash_state, pclash_penalty_to_other),
    ]],
[anyone|plyr, "companion_personalityclash_response", [
],  "I don't have time for your petty dispute. Do not bother me with this again.", "close_window", [
              (troop_set_slot, "$map_talk_troop", slot_troop_personalityclash_state, pclash_penalty_to_both),
    ]],
##  [anyone|plyr, "companion_personalityclash_response", [
##      ],  "Your grievance is noted. Now fall back in line.", "close_window", [
##                    (troop_set_slot, "$map_talk_troop", slot_troop_personalityclash_state, 1),
##          ]],

##  [anyone|plyr, "companion_personalityclash_response", [
##      ],  "I prefer my followers to keep their opinions to themselves.", "close_window", [
##                    (troop_set_slot, "$map_talk_troop", slot_troop_personalityclash_state, 1),
##                    (assign, "$disable_npc_complaints", 1),
##          ]],



# Personality match

[anyone, "event_triggered", [
               (eq, "$npc_map_talk_context", slot_troop_personalitymatch_state),
               (store_conversation_troop, "$map_talk_troop"),
          (is_between, "$map_talk_troop", companions_begin, companions_end),

               (eq, "$map_talk_troop", "$npc_with_personality_match"),

               (troop_get_slot, ":speech", "$map_talk_troop", slot_troop_personalitymatch_speech),
               (troop_get_slot, ":object", "$map_talk_troop", slot_troop_personalitymatch_object),
               (str_store_troop_name, 11, ":object"),
               (str_store_string, 5, ":speech"),

               ],
"{s5}", "companion_personalitymatch_b", [
              (assign, "$npc_with_personality_match", 0),
              (troop_get_slot, ":object", "$map_talk_troop", slot_troop_personalitymatch_object),
         (call_script, "script_troop_change_relation_with_troop", "$map_talk_troop", ":object", 15),

 ]],
[anyone, "companion_personalitymatch_b", [
              (troop_get_slot, ":speech", "$map_talk_troop", slot_troop_personalitymatch_speech_b),
              (troop_get_slot, ":object", "$map_talk_troop", slot_troop_personalitymatch_object),
              (str_store_troop_name, 11, ":object"),
              (str_store_string, 5, ":speech"),

               ],
"{s5}", "companion_personalitymatch_response", [
 ]],
[anyone|plyr, "companion_personalitymatch_response", [
],  "Very good.", "close_window", [
              (troop_set_slot, "$map_talk_troop", slot_troop_personalitymatch_state, 1),

         ]],
##  [anyone|plyr, "companion_personalitymatch_response", [
##      ],  "I prefer my followers to keep their opinions to themselves.", "close_window", [
##                    (troop_set_slot, "$map_talk_troop", slot_troop_personalitymatch_state, 1),
##                    (assign, "$disable_npc_complaints", 1),
##          ]],

[anyone, "event_triggered", [
               (eq, "$npc_map_talk_context", slot_troop_woman_to_woman_string),
               (store_conversation_troop, "$map_talk_troop"),
          (is_between, "$map_talk_troop", companions_begin, companions_end),

             (store_sub, ":npc_no", "$map_talk_troop", "trp_npc1"),
             (store_add, ":speech", "str_npc1_woman_to_woman", ":npc_no"),
#                     (troop_get_slot, ":speech", "$map_talk_troop", slot_troop_woman_to_woman_string),
               (str_store_string, s5, ":speech"),
               ],
"{s5}", "companion_sisterly_advice", [
              (troop_set_slot, "$map_talk_troop", slot_troop_woman_to_woman_string, -1),
         (assign, "$npc_with_sisterly_advice", 0),
 ]],
[anyone|plyr, "companion_sisterly_advice", [
],  "Thank you.", "close_window", [
    ]],
[anyone|plyr, "companion_sisterly_advice", [
],  "I would prefer not to discuss such things.", "close_window", [
(assign, "$disable_sisterly_advice", 1),
    ]],
[anyone|plyr, "companion_home_description", [
],  "Tell me more.", "companion_home_description_2", [
    ]],
[anyone|plyr, "companion_home_description", [
],  "We don't have time to chat just now.", "close_window", [
    ]],
[anyone|plyr, "companion_home_description", [
],  "I prefer my companions not to bother me with such trivialities.", "close_window", [
              (assign, "$disable_local_histories", 1),
    ]],
[anyone, "companion_home_description_2", [
               (troop_get_slot, ":speech", "$map_talk_troop", slot_troop_home_description),
               (str_store_string, 5, ":speech"),
],  "{s5}", "companion_home_description_3", [
    ]],
[anyone, "companion_home_description_3", [
               (troop_get_slot, ":speech", "$map_talk_troop", slot_troop_home_description_2),
               (str_store_string, 5, ":speech"),
],  "{s5}", "close_window", [
    ]],
[anyone|plyr, "companion_political_grievance_response", [
#                    (eq, "$npc_praise_not_complaint", 0),
],  "Your opinion is noted.", "close_window", [
              (troop_get_slot, ":grievance", "$map_talk_troop", slot_troop_morality_penalties),
              (val_add, ":grievance", 25),
              (troop_set_slot, "$map_talk_troop", slot_troop_morality_penalties, ":grievance"),
    ]],
##diplomacy end+

##diplomacy start+ Alternate check for recognition
[anyone, "companion_embassy_results", [
	(troop_slot_eq, "$g_talk_troop", slot_troop_current_mission, npc_mission_seek_recognition),
	(troop_get_slot, ":target_faction", "$g_talk_troop", slot_troop_mission_object),
	(neg|faction_slot_ge, ":target_faction", slot_faction_recognized_player, 1),
	(assign, ":check_peace_war", "$g_mission_result"),#Negative is wants war, positive is wants peace, 0 is undecided
	(ge, ":check_peace_war", 0),

	#Check to see if the player might be ruler of an NPC faction
	(assign, ":player_faction", "fac_player_supporters_faction"),
	(try_begin),
		(neg|faction_slot_eq, "fac_player_supporters_faction", slot_faction_state, sfs_active),
		(is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
		(assign, ":player_faction", "$players_kingdom"),
	(try_end),

	#Must either be at peace or want to be at peace
	(store_relation, reg0, ":player_faction", ":target_faction"),
	(this_or_next|ge, reg0, 0),
		(ge, ":check_peace_war", 1),

	(is_between, "$g_player_court", centers_begin, centers_end),
	(faction_get_slot, ":target_liege", ":target_faction", slot_faction_leader),
	(neg|party_slot_eq, "$g_player_court", dplmc_slot_center_original_lord, ":target_liege"),
	(neg|troop_slot_eq, ":target_liege", slot_troop_home, "$g_player_court"),

	(assign, ":global_points", 0),
	(assign, ":target_points", 0),
	(assign, ":player_points", 0),

	(store_current_hours, ":now"),
	(store_sub, ":recently", ":now", 24 * 21),#within last 3 weeks

	#2 points for a castle, 4 points for a town, ignore villages
	(try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
		(assign, ":center_value", 2),
		(try_begin),
			(party_slot_eq, ":center_no", slot_party_type, spt_town),
			(assign, ":center_value", 4),
		(try_end),
		(val_add, ":global_points", ":center_value"),

		(store_faction_of_party, ":center_faction", ":center_no"),

		(try_begin),
			(eq, ":center_faction", ":target_faction"),
			(val_add, ":target_points", ":center_value"),
		(else_try),
			(assign, ":is_occupied", 0),
			(try_begin),
				(this_or_next|troop_slot_eq, ":target_liege", slot_troop_home, ":center_no"),
				(this_or_next|party_slot_eq, ":center_no", slot_center_original_faction, ":target_faction"),
					(party_slot_eq, ":center_no", dplmc_slot_center_original_lord, ":target_liege"),
				(assign, ":is_occupied", 1),
			(else_try),
				(this_or_next|party_slot_eq, ":center_no", dplmc_slot_center_ex_lord, ":target_liege"),
					(party_slot_eq, ":center_no", slot_center_ex_faction, ":target_faction"),
				(party_slot_ge, ":center_no", dplmc_slot_center_last_transfer_time, ":recently"),
				(assign, ":is_occupied", 1),
			(try_end),
			(eq, ":is_occupied", 0),
			(this_or_next|eq, ":center_faction", "fac_player_supporters_faction"),
				(eq, ":center_faction", "$players_kingdom"),
			(val_add, ":player_points", ":center_value"),
		(try_end),
	(try_end),

	#Needs to hold territory (aside from territory the target faction considers to belong to itself)
	(try_begin),
		(ge, "$cheat_mode", 1),
		(lt,  ":player_points", 1),
		(display_message, "@{!} Recognition refused because player owns no fortresses not claimed by target faction"),
	(try_end),
	(ge, ":player_points", 1),

	#2 points for a lord
	(val_add, ":global_points", 2),#for the player
	(val_add, ":player_points", 2),
	(try_for_range, ":active_npc", heroes_begin, heroes_end),
		(assign, ":lord_value", 2),
		(try_begin),
			#Give less weight to commoners
			(troop_slot_ge, ":active_npc", slot_lord_reputation_type, lrep_roguish),
			(assign, ":lord_value", 1),
		(try_end),
		(try_begin),
			#current lords + original lords
			(this_or_next|is_between, ":active_npc", kings_begin, kings_end),
			(this_or_next|is_between, ":active_npc", lords_begin, lords_end),
			(troop_slot_eq, ":active_npc", slot_troop_occupation, slto_kingdom_hero),
			(val_add, ":global_points", ":lord_value"),
		(try_end),
		(troop_slot_eq, ":active_npc", slot_troop_occupation, slto_kingdom_hero),
		(store_faction_of_troop, ":cur_faction", ":active_npc"),
		(try_begin),
			(eq, ":cur_faction", ":target_faction"),
			(val_add, ":target_points", ":lord_value"),
		(else_try),
			(this_or_next|eq, ":cur_faction", "fac_player_supporters_faction"),
			(eq, ":cur_faction", "$players_kingdom"),
			(val_add, ":player_points", ":lord_value"),
		(try_end),
	(try_end),

	(store_sub, ":num_kingdoms", npc_kingdoms_end, npc_kingdoms_begin),#Not necessarily number of active kingdoms
	(val_max, ":num_kingdoms", 2),
	(store_div, ":average_points", ":global_points", ":num_kingdoms"),

	(try_begin),
		(ge, "$cheat_mode", 1),
		(assign, reg0, ":player_points"),
		(assign, reg1, ":target_points"),
		(assign, reg2, ":average_points"),
		(display_message, "@{!} Military strength check: Player faction score {reg0}, target faction score {reg1}, benchmark score {reg2}"),
	(try_end),

	#Calculate adjustment for player score
	(store_add, ":subjective_percent_modifier", "$player_right_to_rule", 1),#Because it is capped at 99 instead of 100 in Native
	(val_mul, ":subjective_percent_modifier", 2),
	(val_add, ":subjective_percent_modifier", 2),
	(val_div, ":subjective_percent_modifier", 5),
	(val_add, ":subjective_percent_modifier", 60),#100 if you have full right-to-rule, 60 if you have no right-to-rule
	(call_script, "script_troop_get_player_relation", ":target_liege"),
	(try_begin),
		#Maximum positive modifier +20%
		(ge, reg0, 0),
		(val_div, reg0, 5),
	(else_try),
		#Minimum negative modifier -40%
		(lt, reg0, 0),
		(val_mul, reg0, 2),
		(val_div, reg0, 5),
	(try_end),
	(val_add, ":subjective_percent_modifier", reg0),#adjusts % by +20 to -40; minimum possible is 20, maximum possible is 120

	#Apply adjustment to player score
	(val_clamp, ":subjective_percent_modifier", 20, 121),#<-- This should have no effect unless there is a mistake above
	(val_mul, ":player_points", ":subjective_percent_modifier"),
	(val_div, ":player_points", 100),

	#Calculate adjustment for target score
	#Adjust standards towards the mean
	(try_begin),
		(le, ":check_peace_war", -1),
		#Right now the code can't get this far if the check-peace-war
		#result was negative, but leave this in here to handle it if
		#that gets changed.
		(val_max, ":target_points", ":average_points"),
	(else_try),
		(le, ":check_peace_war", 1),
		(val_add, ":target_points", ":average_points"),
		(val_div, ":target_points", 2),
	(else_try),
		(ge, ":check_peace_war", 2),
		(val_min, ":target_points", ":average_points"),
	(try_end),
	#For some variability, adjust the target score by + or - 10%
	(store_random_in_range, reg0, 0, 21),
	(store_add, ":subjective_percent_modifier", 90, reg0),
	#Apply modifier based on check_peace_war
	(val_max, ":check_peace_war", -5),#In Native this result won't ever reach these bounds, but add these in case
	(val_min, ":check_peace_war", 5),#the script behavior is altered later.
	(store_mul, reg0, ":check_peace_war", -10),
	(try_begin),
		(lt, ":check_peace_war", 0),
		(val_mul, reg0, 2),
	(try_end),
	(val_add, ":subjective_percent_modifier", reg0),
	#Apply penalty based on war and/or betrayal
	(try_begin),
		(eq, ":target_faction", "$players_oath_renounced_against_kingdom"),
		(val_add, ":subjective_percent_modifier", 20),
	(else_try),
		(store_relation, reg0, ":player_faction", ":target_faction"),
		(lt, reg0, 0),
		(lt, ":check_peace_war", 1),
		(val_add, ":subjective_percent_modifier", 10),
	(try_end),

	#Apply adjustment to target score
	(val_mul, ":target_points", reg0),
	(val_div, ":target_points", 100),

	(try_begin),
		(ge, "$cheat_mode", 1),
		(assign, reg0, ":player_points"),
		(assign, reg1, ":target_points"),
		(display_message, "@{!} Player faction score for recognition is {reg0}, needs to be at least {reg1}"),
	(try_end),
	#Moment of truth
	(ge, ":player_points", ":target_points"),

	(str_store_troop_name, s12, ":target_liege"),
	(str_store_party_name, s4, "$g_player_court"),
],
"In this letter, {s12} addresses you as {Lord/Lady} of {s4}, which implies some sort of recognition that you are a sovereign and independent monarch.","companion_rejoin_response", [
            (troop_get_slot, ":mission_object", "$g_talk_troop", slot_troop_mission_object),
         (try_begin),
            (faction_slot_eq, ":mission_object", slot_faction_recognized_player, 0),
            (faction_set_slot, ":mission_object", slot_faction_recognized_player, 1),
			#gekokujo 3.0 reduced RTR rewards start
            #(call_script, "script_change_player_right_to_rule", 10),
            (call_script, "script_change_player_right_to_rule", 3),
			#gekokujo 3.0 reduced RTR rewards end
         (try_end),
         ]],
##For the standard refusal logic, give more insight into why they refused.
[anyone, "companion_embassy_results", [
	(troop_slot_eq, "$g_talk_troop", slot_troop_current_mission, npc_mission_seek_recognition),
	(troop_get_slot, ":mission_object", "$g_talk_troop", slot_troop_mission_object),
	(faction_get_slot, ":emissary_object", ":mission_object", slot_faction_leader),
	#Would have recognized
	(this_or_next|ge, "$g_mission_result", 2),
		(faction_slot_eq, ":mission_object", slot_faction_recognized_player, 1),
	#Except there is no court
	(neg|is_between, "$g_player_court", centers_begin, centers_end),
	(str_store_troop_name, s12, ":emissary_object"),
	(call_script, "script_dplmc_store_troop_is_female", ":emissary_object"),
],
"In {reg0?her:his} letter, {s12} merely refers to you as {playername}, omitting any title. This does not constitute recognition of your right to rule. The letter implies that {reg0?she:he} is unwilling to extend recognition due to your lack of a court.","companion_rejoin_response", [
         ]],
[anyone, "companion_embassy_results", [
	(troop_slot_eq, "$g_talk_troop", slot_troop_current_mission, npc_mission_seek_recognition),
	(troop_get_slot, ":mission_object", "$g_talk_troop", slot_troop_mission_object),
	(faction_get_slot, ":emissary_object", ":mission_object", slot_faction_leader),
	#Would have recognized
	(this_or_next|ge, "$g_mission_result", 2),
		(faction_slot_eq, ":mission_object", slot_faction_recognized_player, 1),
	(is_between, "$g_player_court", centers_begin, centers_end),
	#Except our court is in one of his original centers, or we occupy a fief
	#that is a sticking point.
	(assign, ":number_of_fiefs", 0),
	(str_clear, s0),
	(str_clear, s1),
	(try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
		(store_faction_of_party, ":center_faction", ":center_no"),
		(this_or_next|eq, ":center_faction", "fac_player_supporters_faction"),
			(eq, ":center_faction", "$players_kingdom"),
		(assign, reg0, 0),
		(try_begin),
			(this_or_next|party_slot_eq, ":center_no", dplmc_slot_center_original_lord, ":emissary_object"),
				(troop_slot_eq, ":emissary_object", slot_troop_home, ":center_no"),
			(assign, reg0, 1),
		(else_try),
			(eq, ":center_no", "$g_player_court"),
			(party_slot_eq, ":center_no", slot_center_original_faction, ":mission_object"),
			(assign, reg0, 1),
		(try_end),
		(eq, reg0, 1),
		(try_begin),
			(ge, ":number_of_fiefs", 2),
			(str_store_string, s0, "str_dplmc_s0_comma_s1"),
		(else_try),
			(eq, ":number_of_fiefs", 1),
			(str_store_string_reg, s0, s1),
		(try_end),
		(str_store_party_name, s1, ":center_no"),
		(val_add, ":number_of_fiefs", 1),
	(try_end),
	#Fief objections found
	(ge, ":number_of_fiefs", 1),
	(try_begin),
		(eq, ":number_of_fiefs", 1),
		(str_store_string_reg, s0, s1),
	(else_try),
		(str_store_string, s0, "str_dplmc_s0_and_s1"),
	(try_end),
	(str_clear, s1),

	(str_store_troop_name, s12, ":emissary_object"),
	(call_script, "script_dplmc_store_troop_is_female", ":emissary_object"),
],
"In {reg0?her:his} letter, {s12} merely refers to you as {playername}, omitting any title. This does not constitute recognition of your right to rule. The letter implies that {reg0?she:he} is unwilling to extend recognition due to your occupation of {s0}.","companion_rejoin_response", [
         ]],
##diplomacy end+

[anyone, "companion_embassy_results", [
             (troop_slot_eq, "$g_talk_troop", slot_troop_current_mission, npc_mission_seek_recognition),
         (troop_get_slot, ":mission_object", "$g_talk_troop", slot_troop_mission_object),

         (this_or_next|ge, "$g_mission_result", 2),
            (faction_slot_eq, ":mission_object", slot_faction_recognized_player, 1),

         (is_between, "$g_player_court", centers_begin, centers_end),

         (faction_get_slot, ":emissary_object", ":mission_object", slot_faction_leader),
         (str_store_troop_name, s12, ":emissary_object"),
         (neg|party_slot_eq, "$g_player_court", slot_center_original_faction, ":mission_object"),
 		 ##diplomacy start+
		 ##Add a check regarding any territory that would be a sore point with the liege.
		 (assign, ":end_cond", walled_centers_end),
		 (try_for_range, ":center_no", walled_centers_begin, ":end_cond"),
			(store_faction_of_party, ":center_faction", ":center_no"),
			(this_or_next|eq, ":center_faction", "fac_player_supporters_faction"),
				(eq, ":center_faction", "$players_kingdom"),
			(this_or_next|troop_slot_eq, ":emissary_object", slot_troop_home, ":center_no"),
				(party_slot_eq, ":center_no", dplmc_slot_center_original_lord, ":emissary_object"),
			(assign, ":end_cond", ":center_no"),
		 (try_end),
		 (eq, ":end_cond", walled_centers_end),
		 ##diplomacy end+
         (str_store_party_name, s4, "$g_player_court"),
],
"In this letter, {s12} addresses you as {Lord/Lady} of {s4}, which implies some sort of recognition that you are a sovereign and independent monarch.","companion_rejoin_response", [
            (troop_get_slot, ":mission_object", "$g_talk_troop", slot_troop_mission_object),
         (try_begin),
            (faction_slot_eq, ":mission_object", slot_faction_recognized_player, 0),
            (faction_set_slot, ":mission_object", slot_faction_recognized_player, 1),
			#gekokujo 3.0 reduced RTR rewards start
            #(call_script, "script_change_player_right_to_rule", 10),
            (call_script, "script_change_player_right_to_rule", 3),
			#gekokujo 3.0 reduced RTR rewards end
         (try_end),
         ]],
##diplomacy start+
#For flavor, if the recognition mission failed, give an alternate refusal message
#when the player is co-ruler of a kingdom.
[anyone, "companion_embassy_results", [
	(troop_slot_eq, "$g_talk_troop", slot_troop_current_mission, npc_mission_seek_recognition),
	(troop_get_slot, ":mission_object", "$g_talk_troop", slot_troop_mission_object),
	(faction_get_slot, ":emissary_object", ":mission_object", slot_faction_leader),
	#Check in case the player faction shouldn't be fac_player_supporters_faction
	(assign, ":player_faction", "fac_player_supporters_faction"),
	(try_begin),
		(neg|faction_slot_eq, ":player_faction", slot_faction_state, sfs_active),
		(is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
		(assign, ":player_faction", "$players_kingdom"),
	(try_end),
	#The player is not the sole faction leader
	(faction_get_slot, ":player_faction_leader", ":player_faction", slot_faction_leader),
	(neq, ":player_faction_leader", "trp_player"),
	#The leader is a king or pretender
	(this_or_next|is_between, ":player_faction_leader", kings_begin, kings_end),
		(is_between, ":player_faction_leader", pretenders_begin, pretenders_end),
	(str_store_troop_name, s0, ":player_faction_leader"),
	(str_store_troop_name, s12, ":emissary_object"),
	(call_script, "script_dplmc_store_troop_is_female", ":emissary_object"),
	],
	"In this letter, {s12} addresses {reg0?her:his} response to {s0}, referring to you only as {s0}'s faithful vassal. This does not constitute recognition of your right to rule.","companion_rejoin_response", [
	]],
##diplomacy end+
[anyone, "companion_embassy_results", [
              (troop_slot_eq, "$g_talk_troop", slot_troop_current_mission, npc_mission_seek_recognition),
         (troop_get_slot, ":mission_object", "$g_talk_troop", slot_troop_mission_object),
         (faction_get_slot, ":emissary_object", ":mission_object", slot_faction_leader),
         (str_store_troop_name, s12, ":emissary_object"),
		##diplomacy start+ Use proper pronoun
		(call_script, "script_dplmc_store_troop_is_female", ":emissary_object"),
],#Next line replace "his" with {reg0?her:his}
"In {reg0?her:his} letter, {s12} merely refers to you as {playername}, omitting any title. This does not constitute recognition of your right to rule.","companion_rejoin_response", [
##diplomacy end+
         ]],
[anyone, "companion_embassy_results", [
              (troop_slot_eq, "$g_talk_troop", slot_troop_current_mission, npc_mission_peace_request),
         (troop_get_slot, ":mission_object", "$g_talk_troop", slot_troop_mission_object),
         (faction_slot_ge, ":mission_object", slot_faction_truce_days_with_factions_begin, 1),
         (faction_get_slot, ":emissary_object", ":mission_object", slot_faction_leader),
         (str_store_troop_name, s12, ":emissary_object"),

],
"{s12} says that your current truce should suffice.","companion_rejoin_response", [
         ]],
[anyone, "companion_embassy_results", [
              (troop_slot_eq, "$g_talk_troop", slot_troop_current_mission, npc_mission_peace_request),
         (ge, "$g_mission_result", 1),
         (troop_get_slot, ":mission_object", "$g_talk_troop", slot_troop_mission_object),
         (faction_get_slot, ":emissary_object", ":mission_object", slot_faction_leader),
         (str_store_troop_name, s12, ":emissary_object"),
##diplomacy start+ make gender correct
(call_script, "script_dplmc_store_troop_is_female", ":emissary_object"),
],#Next line "he" to {reg0?she:he}
##diplomacy begin
"{s12} says that {reg0?she:he} is willing to consider a truce of twenty days.","companion_truce_confirm", [
##diplomacy end
##diplomacy end+
         ]],
[anyone, "companion_embassy_results", [
             (troop_slot_eq, "$g_talk_troop", slot_troop_current_mission, npc_mission_peace_request),
         (troop_get_slot, ":mission_object", "$g_talk_troop", slot_troop_mission_object),
         (faction_get_slot, ":emissary_object", ":mission_object", slot_faction_leader),
         (str_store_troop_name, s12, ":emissary_object"),
##diplomacy start+ make gender correct
(call_script, "script_dplmc_store_troop_is_female", ":emissary_object"),
],#Next line "he" to {reg0?she:he}
"{s12} says that {reg0?she:he} is unwilling to conclude a peace.","companion_rejoin_response", [
##diplomacy end+
         ]],
[anyone|plyr, "companion_truce_confirm", [
(troop_get_slot, ":mission_object", "$g_talk_troop", slot_troop_mission_object),
(str_store_faction_name, s4, ":mission_object"),
],
"Very well - let this truce with the {s4} be concluded.","companion_rejoin_response", [
(troop_get_slot, ":mission_object", "$g_talk_troop", slot_troop_mission_object),
(call_script, "script_diplomacy_start_peace_between_kingdoms", ":mission_object", "$players_kingdom", 1),
(str_store_faction_name, s4, ":mission_object"),
]],
[anyone|plyr, "companion_truce_confirm", [],
"On second thought, perhaps this is currently not in our interests.","companion_rejoin_response", [
         ]],
[anyone, "companion_embassy_results", [
              (troop_slot_eq, "$g_talk_troop", slot_troop_current_mission, npc_mission_pledge_vassal),
#					(troop_get_slot, ":mission_object", "$g_talk_troop", slot_troop_mission_object),
         (this_or_next|check_quest_active, "qst_join_faction"),
            (is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
         (troop_get_slot, ":mission_object", "$g_talk_troop", slot_troop_mission_object),
         (faction_get_slot, ":emissary_object", ":mission_object", slot_faction_leader),
         (str_store_troop_name, s12, ":emissary_object"),

],
"{s12} says that you are already pledged to another ruler.","companion_rejoin_response", [
         ]],
[anyone, "companion_embassy_results", [
              (troop_slot_eq, "$g_talk_troop", slot_troop_current_mission, npc_mission_pledge_vassal),
#					(troop_get_slot, ":mission_object", "$g_talk_troop", slot_troop_mission_object),
         (lt, "$g_mission_result", -2),
         (troop_get_slot, ":mission_object", "$g_talk_troop", slot_troop_mission_object),
         (faction_get_slot, ":emissary_object", ":mission_object", slot_faction_leader),
         (str_store_troop_name, s12, ":emissary_object"),
##diplomacy start+ make gender correct
(call_script, "script_dplmc_store_troop_is_female", ":emissary_object"),
],#next line "he" to {reg0?she:he}
"{s12} says that {reg0?she:he} does not believe that you would honor your obligations as a vassal, and suspects that your offer is just a ploy.","companion_rejoin_response", [
         ]],
##diplomacy end+

[anyone, "companion_embassy_results", [
              (troop_slot_eq, "$g_talk_troop", slot_troop_current_mission, npc_mission_pledge_vassal),
         (troop_get_slot, ":mission_object", "$g_talk_troop", slot_troop_mission_object),
         (faction_get_slot, ":emissary_object", ":mission_object", slot_faction_leader),
         (str_store_troop_name, s12, ":emissary_object"),
##diplomacy start+ make gender correct
(call_script, "script_dplmc_store_troop_is_female", ":emissary_object"),
],#next line "he" to {reg0?she:he}, etc.
"{s12} says that {reg0?she:he} accepts your offer of vassalage. {reg0?She:He} will give you 20 days to seek {reg0?her:him} out, in which time {reg0?she:he} will refrain from making war on you.","vassalage_offer_confirm", [
         ]],
[anyone|plyr, "companion_rejoin_response", [
(hero_can_join, "p_main_party"),
(neg|main_party_has_troop, "$map_talk_troop"),
],  "Welcome back, friend!", "close_window", [
  (party_add_members, "p_main_party", "$map_talk_troop", 1),
(assign, "$npc_to_rejoin_party", 0),
  (troop_set_slot, "$map_talk_troop", slot_troop_current_mission, 0),
(troop_set_slot, "$map_talk_troop", slot_troop_days_on_mission, 0),
    ]],
[anyone|plyr, "companion_rejoin_response", [
],  "Unfortunately, I cannot take you back just yet.", "companion_rejoin_refused", [
  (troop_set_slot, "$map_talk_troop", slot_troop_current_mission, npc_mission_rejoin_when_possible),
(troop_set_slot, "$map_talk_troop", slot_troop_days_on_mission, 0),
(assign, "$npc_to_rejoin_party", 0),
    ]],
[anyone, "companion_rejoin_refused", [
],  "As you wish. I will take care of some business, and try again in a few days.", "close_window", [
    ]],
#Royal family members


  [anyone|plyr,"member_chat", [(troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_lady)],
   "Are you enjoying the journey, {s65}?", "lady_journey_1",[]],
  [anyone,"member_chat", [(check_quest_active, "qst_incriminate_loyal_commander"),
                          (quest_slot_eq, "qst_incriminate_loyal_commander", slot_quest_current_state, 0),
                          (store_conversation_troop, "$g_talk_troop"),
                          (eq, "$g_talk_troop", "$incriminate_quest_sacrificed_troop"),
                          (quest_get_slot, ":quest_target_center", "qst_incriminate_loyal_commander", slot_quest_target_center),
                          (store_distance_to_party_from_party, ":distance", "p_main_party", ":quest_target_center"),
                          (lt, ":distance", 10),
                          ], "Yes {sir/madam}?", "sacrificed_messenger_1",[]],
#Tavern Talk (with companions)
#  [anyone, "companion_recruit_yes", [(neg|hero_can_join, "p_main_party"),], "I don't think can lead any more men than you do now.\
# You need to release someone from service if you want me to join your party.", "close_window", []],




#Tavern Talk (with ransom brokers)

#gekokujo ransom brokers don't need the long intro anymore
#  [anyone,"start", [(is_between, "$g_talk_troop", ransom_brokers_begin, ransom_brokers_end),
#                    (eq, "$g_talk_troop_met", 0),
#					##diplomacy start+
#					#Use proper style of address in lieu of sir/madam if necessary (althoguh since these first-time
#					#meetings are likely to occur near the game's start, this will usually not make a difference).
#					(call_script, "script_dplmc_print_subordinate_says_sir_madame_to_s0"),#Write {sir/madame} or replacement to {s0}
#					],
#   "Greetings to you, {s0}. You look like someone who should get to know me.", "ransom_broker_intro",[]],#changed {sir/madam} to {s0}
#   ##diplomacy end+
#
#  [anyone|plyr,"ransom_broker_intro",[], "Why is that?", "ransom_broker_intro_2",[]],
#  [anyone, "ransom_broker_intro_2", [], "I broker ransoms for the poor wretches who are captured in these endless wars.\
# Normally I travel between the salt mines and the slave markets on the coast, on commission from those whose relatives have gone missing.\
# But if I'm out on my errands of mercy, and I come across a fellow dragging around a captive or two,\
# well, there's no harm in a little speculative investment, is there?\
# And you look like the type who might have a prisoner to sell.", "ransom_broker_info_talk",[(assign, "$ransom_broker_families_told",0),
#                                                                                            (assign, "$ransom_broker_prices_told",0),
#                                                                                            (assign, "$ransom_broker_ransom_me_told",0),
#                                                                                            ]],
#
#  [anyone|plyr,"ransom_broker_info_talk",[(eq, "$ransom_broker_families_told",0)], "What if their families can't pay?", "ransom_broker_families",[]],
#  [anyone, "ransom_broker_families", [], "Oh, then I spin them a few heartwarming tales of life on the galleys.\
# You'd be surprised what sorts of treasures a peasant can dig out of his cowshed or wheedle out of his cousins,\
# assuming he's got the proper motivation!\
# And if in the end they cannot come up with the silver, then there are always a market for slaves.\
# One cannot do Heaven's work with an empty purse, you see.", "ransom_broker_info_talk",[(assign, "$ransom_broker_families_told",1)]],
#  [anyone|plyr,"ransom_broker_info_talk",[(eq, "$ransom_broker_prices_told",0)], "What can I get for a prisoner?", "ransom_broker_prices",[]],
#  [anyone, "ransom_broker_prices", [], "It varies. I fancy that I have a fine eye for assessing a ransom.\
# There are a dozen little things about a man that will tell you whether he goes to bed hungry, or dines each night on soft dumplings and goose.\
# The real money of course is in the samurai, and if you ever want to do my job you'll want to learn about every landowning family in Japan,\
# their estates, their heraldry, their offspring both lawful and bastard, and, of course, their credit with the merchants.", "ransom_broker_info_talk",[(assign, "$ransom_broker_prices_told",1)]],
#  [anyone|plyr,"ransom_broker_info_talk",[(eq, "$ransom_broker_ransom_me_told",0)], "Would you be able to ransom me if I were taken?", "ransom_broker_ransom_me",[]],
#  [anyone, "ransom_broker_ransom_me", [], "Of course. I'm welcome in every palace in Japan.\
# There's not many who can say that! So always be sure to keep a pot of mon buried somewhere,\
# and a loyal servant who can find it in a hurry.", "ransom_broker_info_talk",[(assign, "$ransom_broker_ransom_me_told",1)]],
#  [anyone|plyr,"ransom_broker_info_talk",[], "That's all I need to know. Thank you.", "ransom_broker_pretalk",[]],
#  [anyone|plyr,"ransom_broker_info_talk",[], "Ugh, a slaver in this day and age. How distasteful.", "ransom_broker_pretalk",[]],

  [anyone,"start", [(is_between, "$g_talk_troop", ransom_brokers_begin, ransom_brokers_end),
  ],
   "Greetings. If you have any prisoners, I will be happy to buy them from you.", "ransom_broker_talk",[]],
  #gekokujo 3.0 no more bandit talk end

######################################
# GENERIC MEMBER CHAT
######################################
##diplomacy start+ replace instances of {sir/madam} with {my lord/my lady} or {your highness} if appropriate,
#using s0 and script_dplmc_print_subordinate_says_sir_madame_to_s0"
  [anyone,"member_chat", [(call_script, "script_dplmc_print_subordinate_says_sir_madame_to_s0"),], "Your orders {s0}?", "regular_member_talk",[]],
]
