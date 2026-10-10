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
[anyone,"member_castellan_pretalk", [], "Anything else?", "member_castellan_talk",[]],
[anyone|plyr,"member_castellan_talk", [],
"I want to review the castle garrison.", "member_review_castle_garrison",[]],
[anyone,"member_review_castle_garrison", [], "Of course. Here are our lists, let me know of any changes you require...", "member_castellan_pretalk",[(change_screen_exchange_members,0)]],
[anyone|plyr,"member_castellan_talk", [],
"Let me see your equipment.", "member_review_castellan_equipment",[]],
[anyone,"member_review_castellan_equipment", [], "Very well, it's all here...", "member_castellan_pretalk",[(change_screen_equip_other)]],
[anyone|plyr,"member_castellan_talk", [],
"I want you to abandon the castle and join my party.", "member_castellan_join",[]],
[anyone,"member_castellan_join", [(party_can_join_party,"$g_encountered_party","p_main_party")],
"I've grown quite fond of the place... But if it is your wish, {playername}, I'll come with you.", "close_window", [
 (assign, "$g_move_heroes", 1),
 (call_script, "script_party_add_party", "p_main_party", "$g_encountered_party"),
 (party_clear, "$g_encountered_party"),
 ]],
[anyone,"member_castellan_join", [],
"And where would we sleep? You're dragging a whole army with you, {playername}, there's no more room for all of us.", "member_castellan_pretalk",[]],
[anyone|plyr,"member_castellan_talk", [], "[Leave]", "close_window",[]],
[trp_kidnapped_girl,"member_chat", [], "Are we home yet?", "kidnapped_girl_chat_1",[]],
[anyone,"member_chat",
[
(troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_lady),
], "{playername}, when do you think we can reach our destination?", "member_lady_1",[]],
[anyone|plyr, "member_lady_1", [],  "We still have a long way ahead of us.", "member_lady_2a", []],
[anyone|plyr, "member_lady_1", [],  "Very soon. We're almost there.", "member_lady_2b", []],
[anyone ,"member_lady_2a", [],  "Ah, I am going to enjoy the road for a while longer then. I won't complain.\
I find riding out in the open so much more pleasant than sitting in the castle all day.\
You know, I envy you. You can live like this all the time.", "close_window", []],
[anyone ,"member_lady_2b", [],  "That's good news. Not that I don't like your company, but I did miss my little luxuries.\
Still I am sorry that I'll leave you soon. You must promise me, you'll come visit me when you can.", "close_window", []],
[anyone ,"member_chat", [(is_between, "$g_talk_troop", pretenders_begin, pretenders_end),],
"Greetings, {playername}, my first and foremost vassal. I await your counsel.", "supported_pretender_talk", []],
[anyone,"member_pretalk", [], "Anything else?", "member_talk",[]],
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
[anyone|plyr,"member_talk", [
(is_between, "$players_kingdom", kingdoms_begin, kingdoms_end),
(faction_slot_eq,  "$players_kingdom", slot_faction_marshall, "trp_player"),
], "As strategist, I wish you to send a message to the vassals of the clan", "member_direct_campaign",[]],
[anyone|plyr,"member_talk", [],

"Let me see your equipment.", "member_trade",[]],
[anyone,"member_trade", [], "Very well, it's all here...", "do_member_trade",[
#      (change_screen_trade)
(change_screen_equip_other),
]],
[anyone|plyr,"member_talk", [], "What can you tell me about your skills?", "view_member_char_requested",[]],
[anyone|plyr,"member_talk", [], "We need to separate for a while.", "member_separate",[
      (call_script, "script_npc_morale", "$g_talk_troop"),
      (assign, "$npc_quit_morale", reg0),
]],
[anyone,"member_separate", [
	#Determine if g_talk_troop is an enfeoffed lord in his own right who
	#had been temporarily with the party.
	(call_script, "script_get_number_of_hero_centers", "$g_talk_troop"),

	(this_or_next|gt, reg0, 0),
	(this_or_next|is_between, "$g_talk_troop", lords_begin, lords_end),
	(this_or_next|is_between, "$g_talk_troop", kings_begin, kings_end),
	(this_or_next|is_between, "$g_talk_troop", pretenders_begin, pretenders_end),
	(this_or_next|troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_hero),#<- I think that would be an error, since kingdom heroes are supposed to be leading parties, but it would mean that the character is really a lord
	(this_or_next|is_between, "$g_talk_troop", lords_begin, lords_end),
		(troop_slot_eq, "$g_talk_troop", slot_troop_playerparty_history, dplmc_pp_history_lord_rejoined),
], "Very well, I will return to managing my own estate.", "close_window",
[
	(troop_set_slot, "$g_talk_troop", slot_troop_occupation, slto_kingdom_hero),
	(remove_member_from_party, "$g_talk_troop"),
]],
[anyone,"member_separate", [
    (is_between, "$g_talk_troop", fort_companions_begin, fort_companions_end),
  ], "If you want us to separate for a while, I shall go back home and wait for you. Is that what you want?", "member_separate_confirm", []],
[anyone,"member_separate", [
      (gt, "$npc_quit_morale", 30),
], "Oh really? Well, I'm not just going to wait around here. I'm going to go to the towns to look for other work. Is that what you want?", "member_separate_confirm",
[]],
[anyone,"member_separate", [
], "Well, actually, there was something I needed to tell you.", "companion_quitting",
[
  (assign, "$player_can_refuse_npc_quitting", 0),
  (assign, "$player_can_persuade_npc", 0),
 ]],
[anyone|plyr,"member_separate_confirm", [], "That's right. We need to part ways.", "member_separate_yes",[]],
[anyone|plyr,"member_separate_confirm", [], "No, I'd rather have you at my side.", "do_member_trade",[]],
[anyone,"member_separate_yes", [
], "Well. I'll be off, then. Look me up if you need me.", "close_window",
[
      (troop_set_slot, "$g_talk_troop", slot_troop_occupation, 0),
      (troop_set_slot, "$g_talk_troop", slot_troop_playerparty_history, pp_history_dismissed),
	  #gekokujo 3.0 microfactions! start
	  #for fort companions, we do a couple of other things as well
	  (try_begin),
	    (is_between, "$g_talk_troop", fort_companions_begin, fort_companions_end),
	    (troop_get_slot, ":home", "$g_talk_troop", slot_troop_home),
	    (party_set_slot, ":home", slot_fort_npc_2_state, 2), #set to "return"
	  (try_end),
	  #gekokujo 3.0 microfactions! end
      (remove_member_from_party, "$g_talk_troop"),
 ]],
[anyone|plyr,"member_talk", [], "I'd like to ask you something.", "member_question",[]],
[anyone|plyr,"member_talk", [], "Never mind.", "close_window",[]],
[anyone,"member_question", [], "Very well. What did you want to ask?", "member_question_2",[]],
[anyone|plyr,"member_question_2", [], "How do you feel about the way things are going in this company?", "member_morale",[]],
[anyone|plyr,"member_question_2", [
##diplomacy start+ Prevent this from appearing for non-"companion" troops
(is_between, "$g_talk_troop", companions_begin, companions_end),
##diplomacy end+
], "Tell me your story again.", "member_background_recap",[]],
[anyone|plyr,"member_question_2", [
##diplomacy start+ Prevent this from appearing for non-"companion" troops
(is_between, "$g_talk_troop", companions_begin, companions_end),
(troop_slot_ge, "$g_talk_troop", slot_troop_home, 1),
(troop_slot_ge, "$g_talk_troop", slot_troop_home_recap, 1),
(troop_slot_ge, "$g_talk_troop", slot_troop_backstory_b, 1),
##diplomacy end+
(troop_slot_eq, "$g_talk_troop", slot_troop_kingsupport_state, 0),
], "I suppose you know that I aspire to be ruler of Japan?", "member_kingsupport_1",[]],
[anyone|plyr,"member_question_2", [
##diplomacy start+ Prevent this from appearing for non-"companion" troops
(is_between, "$g_talk_troop", companions_begin, companions_end),
##diplomacy end+
], "Do you have any connections that we could use to our advantage?", "member_intelgathering_1",[]],
[anyone|plyr,"member_question_2", [
##diplomacy start+ Prevent this from appearing for already-enfeoffed troops
(call_script, "script_get_number_of_hero_centers", "$g_talk_troop"),
(eq, reg0, 0),
(neg|troop_slot_eq, "$g_talk_troop", slot_troop_playerparty_history, dplmc_pp_history_lord_rejoined),
(neg|troop_slot_eq, "$g_talk_troop", slot_troop_playerparty_history, dplmc_pp_history_granted_fief),
(neg|troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_hero),
(neg|is_between, "$g_talk_troop", lords_begin, lords_end),
(neg|is_between, "$g_talk_troop", kings_begin, kings_end),
(neg|is_between, "$g_talk_troop", pretenders_begin, pretenders_end),
##Enable promotion when player is co-ruler
(assign, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE - 1),
(try_begin),
	(is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
	(call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", "$players_kingdom"),
(try_end),
(this_or_next|ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
##diplomacy end+
	(faction_slot_eq, "$players_kingdom", slot_faction_leader, "trp_player"),
], "Would you be interested in holding a fief?", "member_fief_grant_1",[]],
[anyone,"member_morale", [
  (call_script, "script_npc_morale", "$g_talk_troop"),
], "{s21}", "do_member_trade",[]],
[anyone,"member_background_recap", [
    (troop_get_slot, ":first_met", "$g_talk_troop", slot_troop_first_encountered),
    (str_store_party_name, 20, ":first_met"),
    (troop_get_slot, ":home", "$g_talk_troop", slot_troop_home),
    (str_store_party_name, 21, ":home"),
    (troop_get_slot, ":recap", "$g_talk_troop", slot_troop_home_recap),
    (str_store_string, 5, ":recap"),
], "{s5}", "member_background_recap_2",[]],
[anyone,"member_background_recap_2", [
    (str_clear, 19),
    (troop_get_slot, ":background", "$g_talk_troop", slot_troop_backstory_b),
    (str_store_string, 5, ":background"),
], "{s5}", "member_background_recap_3",[]],
[anyone,"member_background_recap_3", [
], "Then shortly after, I joined up with you.", "do_member_trade",[]],
[anyone,"member_kingsupport_1", [
 (troop_get_slot, ":morality_grievances", "$g_talk_troop", slot_troop_morality_penalties),
 (gt, ":morality_grievances", 10),
  ], "Um... Yes. I had heard.", "do_member_trade",[]],
[anyone,"member_kingsupport_1", [
 (store_sub, ":npc_no", "$g_talk_troop", "trp_npc1"),
 (store_add, ":string", "str_npc1_kingsupport_1", ":npc_no"),
#		 (troop_get_slot, ":string", "$g_talk_troop", slot_troop_kingsupport_string_1),
 (str_store_string, s21, ":string"),
  ], "{s21}", "member_kingsupport_1a",[]],
[anyone|plyr,"member_kingsupport_1a", [
  ], "Would you then support my cause?", "member_kingsupport_2",[]],
[anyone|plyr,"member_kingsupport_1a", [
  ], "Very good. I will keep that in mind.", "do_member_trade",[]],
[anyone,"member_kingsupport_2", [
(assign, ":companion_already_on_mission", -1),
(try_for_range, ":companion", companions_begin, companions_end),
   (troop_slot_eq, ":companion", slot_troop_occupation, slto_player_companion),
   (troop_get_slot, ":days_on_mission", ":companion", slot_troop_days_on_mission),
   (gt, ":days_on_mission", 17),
   (neg|main_party_has_troop, ":companion"),
   (assign, ":companion_already_on_mission", ":companion"),
(try_end),

(gt, ":companion_already_on_mission", -1),
(troop_get_slot, ":honorific", "$g_talk_troop", slot_troop_honorific),
(str_store_string, s21, ":honorific"),
(str_store_troop_name, s22, ":companion_already_on_mission"),

], "I would, {s21}. Moreover, I have a proposal on how I might help you attain supremacy. But you recently sent {s22} off on a similar mission. We should wait for a couple of weeks to avoid drawing too much attention to ourselves.", "do_member_trade",[]],
[anyone,"member_kingsupport_2", [
 (store_sub, ":npc_no", "$g_talk_troop", "trp_npc1"),
 (store_add, ":string", "str_npc1_kingsupport_2", ":npc_no"),
#		 (troop_get_slot, ":string", "$g_talk_troop", slot_troop_kingsupport_string_2),
 (str_store_string, s21, ":string"),
  ], "{s21}", "member_kingsupport_2a",[]],
[anyone|plyr,"member_kingsupport_2a", [
 (store_sub, ":npc_no", "$g_talk_troop", "trp_npc1"),
 (store_add, ":string", "str_npc1_kingsupport_2a", ":npc_no"),
#  		 (troop_get_slot, ":string", "$g_talk_troop", slot_troop_kingsupport_string_2a),
 (str_store_string, s21, ":string"),
  ], "{s21}", "member_kingsupport_3",[]],
[anyone|plyr,"member_kingsupport_2a", [
 (store_sub, ":npc_no", "$g_talk_troop", "trp_npc1"),
 (store_add, ":string", "str_npc1_kingsupport_2b", ":npc_no"),
#    	 (troop_get_slot, ":string", "$g_talk_troop", slot_troop_kingsupport_string_2b),
 (str_store_string, s21, ":string"),

  ], "{s21}", "do_member_trade",[]],
[anyone,"member_kingsupport_3", [
 (store_sub, ":npc_no", "$g_talk_troop", "trp_npc1"),
 (store_add, ":string", "str_npc1_kingsupport_3", ":npc_no"),
#		 (troop_get_slot, ":string", "$g_talk_troop", slot_troop_kingsupport_string_3),
 (str_store_string, s21, ":string"),
  ], "{s21}", "member_kingsupport_3a",[]],
[anyone|plyr,"member_kingsupport_3a", [
  ], "Very good. You do that", "member_kingsupport_4",[
]],
[anyone|plyr,"member_kingsupport_3a", [
  ], "On second thought, stay with me for a while", "do_member_trade",[]],
[anyone,"member_kingsupport_4", [
 (troop_set_slot, "$g_talk_troop", slot_troop_days_on_mission, 21),
 (troop_set_slot, "$g_talk_troop", slot_troop_current_mission, npc_mission_kingsupport),

 (remove_member_from_party, "$g_talk_troop", "p_main_party"),

 (troop_get_slot, ":string", "$g_talk_troop", slot_troop_honorific),
 (str_store_string, s21, ":string"),

 ], "Farewell then, {s21}, for a little while", "close_window",[]],
[anyone,"member_intelgathering_1", [
 (troop_get_slot, ":town_with_contacts", "$g_talk_troop", slot_troop_town_with_contacts),
 (str_store_party_name, s17, ":town_with_contacts"),
 (store_faction_of_party, ":contact_town_faction", ":town_with_contacts"),
 (str_store_faction_name, s18, ":contact_town_faction"),

 (store_sub, ":npc_no", "$g_talk_troop", "trp_npc1"),
 (store_add, ":connections_string", "str_npc1_intel_mission", ":npc_no"),
 (str_store_string, s21, ":connections_string"),
 ], "{s21}", "member_intelgathering_3",[]],
[anyone,"member_intelgathering_3", [ #change back to member_intelgathering_2 if this will be used
(eq, 1, 0),
], "Of course, as few people should know of this as possible. If you want to collect the information, or pull me out, then don't send a messenger. Come and get me yourself -- even if that means you have to sneak through the gates.", "member_intelgathering_3",[]],
[anyone|plyr,"member_intelgathering_3", [
 ], "Splendid idea -- you do that.", "member_intelgathering_4",[]],
[anyone|plyr,"member_intelgathering_3", [
 ], "Actually, hold off for now.", "do_member_trade",[]],
[anyone,"member_intelgathering_4", [
 (troop_set_slot, "$g_talk_troop", slot_troop_days_on_mission, 5),
 (troop_set_slot, "$g_talk_troop", slot_troop_current_mission, npc_mission_gather_intel),

 (remove_member_from_party, "$g_talk_troop", "p_main_party"),

 (troop_get_slot, ":string", "$g_talk_troop", slot_troop_honorific),
 (str_store_string, s21, ":string"),

 ], "Good. I should be ready to report in about five days. Farewell then, {s21}, for a little while.", "close_window",[]],
[anyone|plyr, "member_intel_liaison", [],
"What have you discovered?", "member_intel_liaison_results", []],
[anyone|plyr, "member_intel_liaison", [
],
"What have you discovered?", "member_intel_liaison_results", []],
[anyone|plyr, "member_intel_liaison", [],
"It's time to pull you out. Let's leave town separately, but join me soon after", "close_window", [
(assign, "$npc_to_rejoin_party", "$g_talk_troop"),
]],
[anyone|plyr, "member_intel_liaison", [],
"You're doing good work. Stay here for a little longer", "close_window", []],
[anyone, "member_intel_liaison_results", [
(store_faction_of_party, ":town_faction", "$g_encountered_party"),
(call_script, "script_update_faction_political_notes", ":town_faction"),
(assign, ":instability_index", reg0),
(val_add, ":instability_index", reg0),
(val_add, ":instability_index", reg1),
#diplomacy start+ Also include promoted kingdom ladies
#(try_for_range, ":lord", active_npcs_begin, active_npcs_end),
(try_for_range, ":lord", heroes_begin, heroes_end),
#diplomacy end+
   (troop_slot_eq, ":lord", slot_troop_occupation, slto_kingdom_hero),
   (store_faction_of_troop, ":lord_faction", ":lord"),
   (eq, ":lord_faction", ":town_faction"),
   (call_script, "script_update_troop_political_notes", ":lord"),
(try_end),

(str_store_faction_name, s12, ":town_faction"),
(try_begin),
   (gt, ":instability_index", 60),
   (str_store_string, s11, "str_the_s12_is_a_labyrinth_of_rivalries_and_grudges_lords_ignore_their_lieges_summons_and_many_are_ripe_to_defect"),
(else_try),
   (is_between, ":instability_index", 40, 60),
   (str_store_string, s11, "str_the_s12_is_shaky_many_lords_do_not_cooperate_with_each_other_and_some_might_be_tempted_to_defect_to_a_liege_that_they_consider_more_worthy"),
(else_try),
   (is_between, ":instability_index", 20, 40),
   (str_store_string, s11, "str_the_s12_is_fairly_solid_some_lords_bear_enmities_for_each_other_but_they_tend_to_stand_together_against_outside_enemies"),
(else_try),
   (lt, ":instability_index", 20),
   (str_store_string, s11, "str_the_s12_is_a_rock_of_stability_politically_speaking_whatever_the_lords_may_think_of_each_other_they_fight_as_one_against_the_common_foe"),
(try_end),

],
"{s11} I notice that you have been keeping some notes about individual lords. I have annotated those with my findings.", "member_intel_liaison", []],
[anyone,"member_fief_grant_1", [
  ], "Which fief did you have in mind?", "member_fief_grant_2",[]],
[anyone|plyr|repeat_for_parties,"member_fief_grant_2", [
(store_repeat_object, ":center"),
  (is_between, ":center", centers_begin, centers_end),
(neq, ":center", "$g_player_court"),
(store_faction_of_party, ":center_faction", ":center"),
##diplomacy start+ Handle player is co-ruler of kingdom
(assign, ":alt_faction", 0),
(try_begin),
	(eq, ":center_faction", "$players_kingdom"),
	(is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
	(call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", "$players_kingdom"),
	(ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
	(assign, ":alt_faction", 1),
(try_end),
(this_or_next|eq, ":alt_faction", 1),
##diplomacy end+
(eq, ":center_faction", "fac_player_supporters_faction"),
(neg|party_slot_ge, ":center", slot_town_lord, active_npcs_begin), #ie, owned by player or unassigned
(str_store_party_name, s11, ":center"),

  ], "{s11}", "member_fief_grant_3",[
(store_repeat_object, "$temp"),
]],
[anyone|plyr, "member_fief_grant_2", [
  ], "Never mind -- there is no fief I can offer.", "do_member_trade",[
]],
[anyone,"member_fief_grant_3", [
  ], "{s5}", "close_window",[
(call_script, "script_npc_morale", "$g_talk_troop"),
(assign, ":npc_morale", reg0),

(remove_member_from_party, "$g_talk_troop", "p_main_party"),


(try_begin),
##diplomacy start+ Spouses use your banner
    (neg|troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_hero),
	(this_or_next|troop_slot_eq, "trp_player", slot_troop_spouse, "$g_talk_troop"),
	    (troop_slot_eq, "$g_talk_troop", slot_troop_spouse, "trp_player"),
	(this_or_next|is_between, "$g_talk_troop", heroes_begin, heroes_end),
			(troop_slot_eq, "trp_player", slot_troop_spouse, "$g_talk_troop"),
	(troop_get_slot, ":banner_id", "trp_player", slot_troop_banner_scene_prop),
	(gt, ":banner_id", 0),
	(troop_set_slot, "$g_talk_troop", slot_troop_banner_scene_prop, ":banner_id"),
	(troop_set_slot, "$g_talk_troop", slot_troop_occupation, slto_kingdom_hero),
(else_try),
##diplomacy end+
    (neg|troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_hero),

    (assign, ":banner_offset", banners_end_offset),
    (val_sub, ":banner_offset", 1),
    (val_sub, ":banner_offset", "$g_companions_banner_id"),
    (store_add, ":banner_id", banner_scene_props_begin, ":banner_offset"),
    (troop_set_slot, "$g_talk_troop", slot_troop_banner_scene_prop, ":banner_id"),
    (val_add, "$g_companions_banner_id", 1),

    (troop_set_slot, "$g_talk_troop", slot_troop_occupation, slto_kingdom_hero),
(try_end),

##diplomacy start+
##Alternate use of this slot so we don't forget the enfeoffment, even if later
##the companion's occupation changes and he loses the fief.
(troop_set_slot, "$g_talk_troop", slot_troop_playerparty_history, dplmc_pp_history_granted_fief),

#Handle player is co-ruler of NPC faction
##OLD:
#(troop_set_faction, "$g_talk_troop", "fac_player_supporters_faction"),
##NEW:
(assign, ":is_coruler", 0),
(try_begin),
	(is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
	(neg|faction_slot_eq, "fac_player_supporters_faction", slot_faction_state, sfs_active),
	(call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", "$players_kingdom"),
	(ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),#player is co-ruler of an NPC faction
	(assign, ":is_coruler", 1),
	(troop_set_faction, "$g_talk_troop", "$players_kingdom"),
(else_try),
	(troop_set_faction, "$g_talk_troop", "fac_player_supporters_faction"),
(try_end),
##diplomacy end+

(call_script, "script_give_center_to_lord", "$temp", "$g_talk_troop", 0),
(try_begin),
   (faction_slot_eq, "$players_kingdom", slot_faction_political_issue, "$temp"),
   (faction_set_slot, "$players_kingdom", slot_faction_political_issue, -1),
(try_end),

(try_begin),
  (troop_slot_eq, "$g_talk_troop", slot_troop_original_faction, 0),
  (party_get_slot, ":fief_culture", "$temp", slot_center_original_faction),
  (troop_set_slot, "$g_talk_troop", slot_troop_original_faction, ":fief_culture"),
(try_end),

(store_character_level, ":renown", "$g_talk_troop"),
(val_mul, ":renown", 15),
(val_max, ":renown", 200),
(troop_set_slot, "$g_talk_troop", slot_troop_renown, ":renown"),

##diplomacy start+
##Adjust starting gold by Looting and Trade skills
##(troop_set_slot, "$g_talk_troop", slot_troop_wealth, 2500), #represents accumulated loot
(assign, ":initial_gold", 2500),
(try_begin),
	#Changes must be enabled
	(ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_MEDIUM),
	#initial gold is 2500 * (10 + trade + looting) / 10, rounded.
	(store_skill_level, ":modifier", "skl_trade", "$g_talk_troop"),
	(store_skill_level, ":skill_level", "skl_looting", "$g_talk_troop"),
	(val_add, ":modifier", ":skill_level"),
	(val_add, ":modifier", 10),
	(val_mul, ":initial_gold", ":modifier"),
	(val_add, ":initial_gold", 5),
	(val_div, ":initial_gold", 10),
(try_end),
(troop_set_slot, "$g_talk_troop", slot_troop_wealth, ":initial_gold"), #represents accumulated loot
##diplomacy end+
#		(troop_set_slot, "$g_talk_troop", slot_troop_readiness_to_join_army, 100),
#		(troop_set_slot, "$g_talk_troop", slot_troop_readiness_to_follow_orders, 100),

(str_store_troop_name_plural, s12, "$g_talk_troop"),
   ##diplomacy start+
#(troop_get_type, ":is_female", "$g_talk_troop"),
(call_script, "script_dplmc_store_troop_is_female", "$g_talk_troop"),
(assign, reg65, reg0),
(assign, ":is_female", reg65),
(try_begin),
   #gekokujo 3.0 repurpose the tribune thing to former ikko ikki, if that ever ever happens
   ##Enable the "Tribune" dialogue option for all Custodian or Benefactor companions
   ##from the Rhodok lands, instead of just Bunduk.  Currently there are no others
   ##besides him, but other mods may add them.
   #(eq, "$g_talk_troop", "trp_npc10"),
   (this_or_next|troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_benefactor),
   (troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_custodian),
   #(troop_slot_eq, "$g_talk_troop", slot_troop_original_faction, "fac_kingdom_5"), #no such thing as rhodoks in gekokujo
   (troop_slot_eq, "$g_talk_troop", slot_troop_original_faction, "fac_kingdom_20"), #but there are ikko ikki!
   ##diplomacy end+
   (str_store_string, s14, "str_tribune_s12"),
(else_try),
   (eq, ":is_female", 1),
   (str_store_string, s14, "str_lady_s12"),
(else_try),
   (str_store_string, s14, "str_lord_s12"),
(try_end),
(troop_set_name, "$g_talk_troop", s14),
          ##diplomacy start+
          ##Custom player kingdom vassal titles, credit Caba`drin start
		  (try_begin),
			(eq, ":is_coruler", 1),
			(call_script, "script_troop_set_title_according_to_faction", "$g_talk_troop", "$players_kingdom"),
		  (else_try),
			(call_script, "script_troop_set_title_according_to_faction", "$g_talk_troop", "fac_player_supporters_faction"),
		  (try_end),
          ##Custom player kingdom vassal titles, credit Caba`drin start
          ##diplomacy end+
(unlock_achievement, ACHIEVEMENT_I_DUB_THEE),

          (call_script, "script_check_concilio_calradi_achievement"),

(try_begin),
   (troop_add_item, "$g_talk_troop", "itm_gekokujo_haori_1",0),
   (troop_add_item, "$g_talk_troop", "itm_gekokujo_katana_1",0),
   (troop_add_item, "$g_talk_troop", "itm_gekokujo_wakizashi_2",0),
(try_end),
(troop_equip_items, "$g_talk_troop"),

(store_div, ":relation_boost", ":npc_morale", 3),
#		(val_add, ":relation_boost", 10),
(call_script, "script_troop_change_relation_with_troop", "$g_talk_troop", "trp_player", ":relation_boost"),

(str_store_party_name, s17, "$temp"),
#gekokujo 3.0 microfactions! start
#the microfort troops have a diffent fief acceptance speech
#(store_sub, ":npc_no", "$g_talk_troop", "trp_npc1"),
#(store_add, ":speech", "str_npc1_fief_acceptance", ":npc_no"),
(try_begin),
  (is_between, "$g_talk_troop", fort_companions_begin, fort_companions_end),
  (assign, ":speech", "str_gekokujo_fort_companion_promote"),
  (troop_get_slot, ":home", "$g_talk_troop", slot_troop_home),
  (party_set_slot, ":home", slot_fort_npc_2_state, 4), #set to "promoted"
(else_try),
  (store_sub, ":npc_no", "$g_talk_troop", "trp_npc1"),
  (store_add, ":speech", "str_npc1_fief_acceptance", ":npc_no"),
(try_end),
#gekokujo 3.0 microfactions! end
#        (troop_get_slot, ":speech", "$g_talk_troop", slot_troop_fief_acceptance_string),
  (str_store_string, s5, ":speech"),
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
[anyone, "companion_quitting", [
               (store_conversation_troop, "$map_talk_troop"),
               (troop_get_slot, ":speech", "$map_talk_troop", slot_troop_retirement_speech),
               (str_store_string, 5, ":speech")
               ],
"{s5}", "companion_quitting_2", [
 ]],
[anyone, "companion_quitting_2", [
              (call_script, "script_npc_morale", "$map_talk_troop"),
               ],
"To tell you the truth, {s21}", "companion_quitting_response", [
 ]],
[anyone|plyr, "companion_quitting_response", [
], "Very well. You be off, then.", "companion_quitting_yes", [
    ]],
[anyone|plyr, "companion_quitting_response", [
          (eq, "$player_can_persuade_npc", 1),
#], "Perhaps I can persuade you to change your mind.", "companion_quitting_persuasion", [#<- dplmc replace
], "Perhaps I can persuade you to change your mind.", "dplmc_companion_quitting_persuasion_start", [#<- dplmc add
##diplomacy end+
      (assign, "$player_can_persuade_npc", 0),
    ]],
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
[anyone|plyr, "companion_quitting_response", [
      (ge, "$cheat_mode", 1),#only enable in cheat mode
      (eq, "$player_can_refuse_npc_quitting", 1),
], "CHEAT -- We hang deserters in this company.", "companion_quitting_no", [
    ]],
[anyone, "companion_quitting_no", [
	(troop_get_slot, ":talk_troop_personality", "$g_talk_troop", slot_lord_reputation_type),
	(this_or_next|eq, ":talk_troop_personality", lrep_martial),
	(this_or_next|eq, ":talk_troop_personality", lrep_selfrighteous),
		(eq, ":talk_troop_personality", lrep_quarrelsome),
],
"I believe I misheard you.  You certainly could not have been threatening me.", "companion_quitting_no_confirm", [
 ]],
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
[anyone,"member_chat", [
  (call_script, "script_dplmc_print_subordinate_says_sir_madame_to_s0"),
  ], "Your orders {s0}?", "regular_member_talk",[]],
[anyone,"member_direct_campaign", [], "Yes, {my lord/my lady}. Which message do you wish to send to the vassals?", "member_direct_campaign_choice",
  []],
[anyone|plyr,"member_direct_campaign_choice",
   [
#     (eq, "$g_talk_troop_faction", "$players_kingdom"),
	 (this_or_next|neg|faction_slot_ge, "$players_kingdom", slot_faction_marshall, active_npcs_begin),
		(eq, "$players_kingdom", "fac_player_supporters_faction"),
     (this_or_next|faction_slot_eq, "$players_kingdom", slot_faction_ai_state, sfai_default),
		(faction_slot_eq, "$players_kingdom", slot_faction_ai_state, sfai_feast),
     ],
   "I want to start a new campaign. Let us assemble the army here.", "member_direct_campaign_call_to_arms_verify",
   [
     (faction_get_slot, ":old_marshall", "$players_kingdom", slot_faction_marshall),
     (try_begin),
        (ge, ":old_marshall", 0),
		(troop_get_slot, ":old_marshall_party", ":old_marshall", slot_troop_leaded_party),
        (party_is_active, ":old_marshall_party"),
        (party_set_marshall, ":old_marshall_party", 0),
     (try_end),

    (faction_set_slot, "$players_kingdom", slot_faction_marshall, "trp_player"),
   ]],
[anyone|plyr,"member_direct_campaign_choice",
   [
#     (eq, "$g_talk_troop_faction", "$players_kingdom"),
     (faction_slot_eq, "$players_kingdom", slot_faction_marshall, "trp_player"),
     (neg|faction_slot_eq, "$players_kingdom", slot_faction_ai_state, sfai_default),
     (neg|faction_slot_eq, "$players_kingdom", slot_faction_ai_state, sfai_feast),
     ],
   "I want to end the campaign and let everyone return home.", "member_give_order_disband_army_verify", []],
[anyone|plyr,"member_direct_campaign_choice",
   [
#     (eq, "$g_talk_troop_faction", "$players_kingdom"),
     (faction_slot_eq, "$players_kingdom", slot_faction_marshall, "trp_player"),
     (neg|faction_slot_eq, "$players_kingdom", slot_faction_ai_state, sfai_feast),
	 (check_quest_active, "qst_organize_feast"),
	 (quest_get_slot, ":venue", "qst_organize_feast", slot_quest_target_center),
	 (store_faction_of_party, ":venue_faction", ":venue"),
	 (eq, ":venue_faction", "$players_kingdom"),
	 (str_store_party_name, s4, ":venue"),
     ],
   "I wish to invite the vassals of the realm to a feast at {s4}.", "member_give_order_invite_feast_verify", []],
[anyone|plyr,"member_direct_campaign_choice",
   [
     ],
   "Never mind", "member_pretalk",
   []],
[anyone,"member_give_order_invite_feast_verify", [],
   "You wish to invite the lords of the realm to a feast?", "member_give_order_invite_feast_verify_2",[]],
[anyone|plyr,"member_give_order_invite_feast_verify_2", [], "Yes. It is time for us to strengthen the bonds that bring us together.", "member_give_order_invite_feast",[]],
[anyone|plyr,"member_give_order_invite_feast_verify_2", [], "On second thought, this is perhaps not the time.", "member_pretalk",[]],
[anyone,"member_give_order_invite_feast",
   [
	 (quest_get_slot, ":venue", "qst_organize_feast", slot_quest_target_center),
     (str_store_party_name, s4, ":venue"),
   ],
   "All right then. I shall dispatch messengers informing the vassals of the clan of your feast at {s4}.", "member_pretalk",
   [
	 (quest_get_slot, ":venue", "qst_organize_feast", slot_quest_target_center),

	 (assign, "$player_marshal_ai_state", sfai_feast),
	 (assign, "$player_marshal_ai_object", ":venue"),
     (call_script, "script_decide_faction_ai", "$players_kingdom"),
	 (assign, "$g_recalculate_ais", 1),
	 (str_store_party_name, s4, ":venue"),

     ]],
[anyone,"member_direct_campaign_call_to_arms_verify", [],
   "You wish to summon all lords for a new campaign?", "member_give_order_call_to_arms_verify_2",[]],
[anyone|plyr,"member_give_order_call_to_arms_verify_2", [], "Yes. We must gather all our forces before we march on the enemy.", "member_give_order_call_to_arms",[]],
[anyone|plyr,"member_give_order_call_to_arms_verify_2", [], "On second thought, it won't be necessary to summon everyone.", "member_pretalk",[]],
[anyone,"member_give_order_call_to_arms",
   [],
   "All right then. I will send messengers and tell everyone to come here.", "member_pretalk",
   [
	 (assign, "$player_marshal_ai_state", sfai_gathering_army),
	 (assign, "$player_marshal_ai_object", "p_main_party"),
     (call_script, "script_decide_faction_ai", "$players_kingdom"),
	 (assign, "$g_recalculate_ais", 1),
     ]],
[anyone,"member_give_order_disband_army_verify", [],
   "You want to end the current campaign and release all lords from duty?", "member_give_order_disband_army_2",[]],
[anyone|plyr,"member_give_order_disband_army_2", [], "Yes. We no longer need all our forces here.", "member_give_order_disband_army",[]],
[anyone|plyr,"member_give_order_disband_army_2", [], "On second thought, it will be better to stay together for now.", "member_pretalk",[]],
[anyone,"member_give_order_disband_army",
   [],
   "All right. I will let everyone know that they are released from duty.", "member_pretalk",
   [
	 (assign, "$player_marshal_ai_state", sfai_default),
	 (assign, "$player_marshal_ai_object", -1),
     (call_script, "script_decide_faction_ai", "$players_kingdom"),
	 (assign, "$g_recalculate_ais", 1),

     ]],
]
