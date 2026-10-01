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


dialogs_lord_faction = [
[anyone|plyr,"lord_talk", [
(le,"$talk_context", tc_party_encounter),
(ge, "$g_talk_troop_faction_relation", 0),
#(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 0),
(neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
(faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, "$g_talk_troop"),
(eq, "$players_kingdom", "$g_talk_troop_faction"),
(eq, "$player_has_homage", 1),
],
"{s66}, I want to give up a fief you enfeoffed to me.", "dplmc_lord_give_back_fief",[
]],
[anyone|plyr,"lord_talk", [(le,"$talk_context", tc_party_encounter),
                       (ge, "$g_talk_troop_faction_relation", 0),
                       #(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 0),
                       (neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
                       (faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, "$g_talk_troop"),
                       (eq, "$players_kingdom", "$g_talk_troop_faction"),
                       (eq, "$player_has_homage", 1),
                      ],
"{s66}, you should declare war on a clan.", "dplmc_lord_declare_war",[
]],
[anyone|plyr,"lord_talk_ask_something_2", [
 (call_script, "script_dplmc_is_affiliated_family_member", "$g_talk_troop"),
 (eq, reg0, 1),],
"I have done my share with your family, I want to be discharged of my pledge.", "dplmc_lord_family_affiliate_end",[
]],
[anyone|plyr,"lord_talk_ask_something_2", [
(store_current_hours, ":current_hours"),
(val_sub, ":current_hours", 24 * 6),
(ge, ":current_hours", "$g_last_affiliate_attempt"),

(ge, "$g_talk_troop_faction_relation", 0),
(neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
(eq, "$players_kingdom", "$g_talk_troop_faction"),
(eq, "$player_has_homage", 1),
##diplomacy start+
#(eq, "$g_player_affiliated_troop", 0),
(lt, "$g_player_affiliated_troop", 1),
##diplomacy end+
(troop_slot_eq, "$g_talk_troop", dplmc_slot_troop_affiliated, 0),
(call_script, "script_troop_get_player_relation", "$g_talk_troop"),
(gt, reg0, 0),
(call_script, "script_troop_get_family_relation_to_troop", "trp_player", "$g_talk_troop"),
(le, reg0, 0),
                      ],
"I have great respect for your lineage, I wish to be affiliated to your family.", "dplmc_lord_family_affiliate",[
]],
[anyone, "lord_groom_vows", [
],
#diplomacy start+ gender-correct language
"My {lord/lady}, with this assembly as my witness, I vow to take you as my {husband/wife}, to honor, cherish, and {obey/protect} you. My the heavens bless us with health, prosperity, and children.", "female_pc_marriage_vow", [
#diplomacy end+
]],
[anyone, "lord_groom_wedding_complete", [
],
"We are now husband and wife. Let the festivities commence!", "close_window",
[]],
[anyone|plyr,"lord_prison_break", [],
"I've come to get you out of here", "lord_prison_break_confirm",
[]],
[anyone|plyr,"lord_prison_break", [],
"Never mind -- just stay quiet", "close_window",
[
(troop_set_slot, "$g_talk_troop", slot_troop_mission_participation, mp_stay_out),
(assign, "$g_reset_mission_participation", 1),
]],
[anyone,"lord_prison_break_confirm", [],
"Thank the heavens! I don't know how long I could have lasted in here", "lord_prison_break_confirm_2",
[]],
[anyone,"lord_prison_break_confirm_2", [],
"But wait -- how will we escape? We'll be rushed by the garrison the moment we step out that door. I can help you hold them off -- but I'll tell you now, they have fed me nothing but watery porridge and a few scraps, and I'm not as strong as I could be.", "lord_prison_break_confirm_3",
[]],
[anyone|plyr,"lord_prison_break_confirm_3", [],
"You keep well behind me, and try to stay out of the fighting.", "lord_prison_break_confirm_4",
[
(troop_set_slot, "$g_talk_troop", slot_troop_mission_participation, mp_prison_break_stand_back),
(assign, "$g_reset_mission_participation", 1),
(agent_set_team, "$g_talk_agent", 0),
]],
[anyone|plyr,"lord_prison_break_confirm_3", [],
"I'll need you to grab a weapon and help me, despite your weakness.", "lord_prison_break_confirm_4",
[
(troop_set_slot, "$g_talk_troop", slot_troop_mission_participation, mp_prison_break_fight),
(assign, "$g_reset_mission_participation", 1),
(agent_set_team, "$g_talk_agent", 0),
]],
[anyone|plyr,"lord_prison_break_confirm_3", [],
"Actually, don't get involved in this.", "close_window",
[
(troop_set_slot, "$g_talk_troop", slot_troop_mission_participation, mp_stay_out),
(assign, "$g_reset_mission_participation", 1),
]],
[anyone,"lord_prison_break_confirm_4", [

(str_clear, s14),
(try_for_range, ":other_prisoner", active_npcs_begin, kingdom_ladies_end),
(troop_slot_eq, ":other_prisoner", slot_troop_prisoner_of_party, "$g_encountered_party"),
(neq, ":other_prisoner", "$g_talk_troop"),

(assign, ":granted_parole", 0),
(try_begin),
(call_script, "script_cf_prisoner_offered_parole", ":other_prisoner"),
(assign, ":granted_parole", 1),
(try_end),
(eq, ":granted_parole", 0),

(troop_slot_eq, ":other_prisoner", slot_troop_mission_participation, 0),

(str_store_troop_name, s15, ":other_prisoner"),

##diplomacy start+
##OLD:
#(troop_get_type, reg4, ":other_prisoner"),
##NEW:
(assign, reg4, 0),
(try_begin),
	(call_script, "script_cf_dplmc_troop_is_female", ":other_prisoner"),
	(assign, reg4, 1),
(try_end),
##diplomacy end+

(str_store_string, s14, "str__s15_is_also_being_held_here_and_you_may_wish_to_see_if_reg4shehe_will_join_us"),
(try_end),
],
"Let's go!{s14}", "close_window",
[]],
[anyone|plyr ,"lord_requests_recruitment",
[
(str_store_string, s9, "str_lord_indicted_dialog_approach_yes"),
], #And I would be honored to accept your pledge.
"{s9}", "close_window", [
(troop_set_slot, "$g_talk_troop", slot_troop_occupation, slto_kingdom_hero),
##diplomacy start+ write political events to log
(str_store_troop_name, s1, "$g_talk_troop"),
(str_store_faction_name, s2, "$g_talk_troop_faction"),
(display_log_message, "@ {s1} has been accepted as a vassal of {s2}."),
##diplomacy end+
#This should be enough, scriptwise, but if there is a string somewhere to confirm the pledge, I should link
]],
[anyone|plyr ,"lord_requests_recruitment",
[
(str_store_string, s9, "str_lord_indicted_dialog_approach_no"),
], #I'm sorry. Your service is not required.
"{s9}", "lord_requests_recruitment_refuse", []],
[anyone ,"lord_requests_recruitment_refuse",
[
(str_store_string, s9, "str_lord_indicted_dialog_rejected"),
], #Indeed? Well, perhaps your reputation is misleading. Good day, {my lord/my lady} -- I go to see if another ruler in Calradia is more appreciative of my talents.
"{s9}", "close_window", [
#Seek alternative liege
(assign, "$g_leave_encounter", 1),
##diplomacy start+ Try to avoid getting stuck with a bad occupation value
(try_begin),
   (troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_inactive),
	(troop_set_slot, "$g_talk_troop", slot_troop_occupation, slto_kingdom_hero),
(try_end),
##diplomacy end+
(call_script, "script_troop_change_relation_with_troop", "$g_talk_troop", "trp_player", -10),
(call_script, "script_lord_find_alternative_faction", "$g_talk_troop"),
(assign, ":new_faction", reg0),

(try_begin),
(is_between, ":new_faction", kingdoms_begin, kingdoms_end),
(troop_get_slot, ":old_faction", "$g_talk_troop", slot_troop_original_faction),
(str_store_troop_name, s1, "$g_talk_troop"),
(str_store_faction_name, s2, ":new_faction"),
(str_store_faction_name, s3, ":old_faction"),

#gekokujo 3.0 integrating 1.158 change start
(troop_set_slot, "$g_talk_troop", slot_troop_occupation, slto_kingdom_hero),
#gekokujo 3.0 integrating 1.158 change end
(call_script, "script_change_troop_faction", "$g_talk_troop", ":new_faction"),

##diplomacy start+
##OLD:
#(troop_get_type, reg4, "$g_talk_troop"),
##NEW:
(assign, reg4, 0),
(try_begin),
	(call_script, "script_cf_dplmc_troop_is_female", "$g_talk_troop"),
	(assign, reg4, 1),
(try_end),
(assign, reg65, reg4),
##write political events to log
(display_log_message, "str_lord_defects_ordinary"),#change display_message to display_log_message
##diplomacy end+
(else_try),
(call_script, "script_change_troop_faction", "$g_talk_troop", "fac_outlaws"),
(try_end),
]],
[anyone ,"lord_give_conclude_2", [(is_between, "$g_talk_troop", pretenders_begin, pretenders_end),
                     (neg|troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_hero),
               ],
"Forward, then! Our first task is to take hold of a castle and persuade other lords to join us. You lead the way!", "close_window", [

      (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 50), #should be higher
      (faction_set_slot, "$g_talk_troop_faction", slot_faction_state, sfs_active),
##            (faction_set_slot, "$g_talk_troop_faction", slot_faction_ai_state, sfai_nascent_rebellion),

      (party_force_add_members, "p_main_party", "$supported_pretender", 1),
      (troop_set_slot, "$supported_pretender", slot_troop_cur_center, 0),
      (troop_set_auto_equip, "$supported_pretender",0),
      (str_store_troop_name_link, s6, "$supported_pretender"),
      (display_message, "@{s6} has joined your party."),

#            (faction_get_slot, ":location", "$g_talk_troop_faction", slot_faction_inactive_leader_location),
#            (faction_set_slot, "$g_talk_troop_faction", slot_faction_inactive_leader_location, 0),

#            (call_script, "script_create_kingdom_hero_party", "$g_talk_troop", ":location"),
#            (party_set_slot, "$pout_party", slot_party_commander_party, "p_main_party"),
#            (call_script, "script_party_decide_next_ai_state_under_command", "$pout_party"),
#            (store_current_hours, ":follow_until_time"),
#            (store_add, ":follow_period", 60, "$g_talk_troop_relation"),
#            (val_div, ":follow_period", 2),
#            (val_add, ":follow_until_time", ":follow_period"),
#            (party_set_slot, "$pout_party", slot_party_follow_player_until_time, ":follow_until_time"),
#            (party_set_slot, "$pout_party", slot_party_following_player, 1),




#            (assign, ":rebellion_target", "$supported_pretender_old_faction"),
      (store_relation, ":reln", "$supported_pretender_old_faction", "fac_player_supporters_faction"),
      (val_min, ":reln", -50),
      (call_script, "script_set_player_relation_with_faction", "$supported_pretender_old_faction", ":reln"),
   (faction_get_slot, ":adjective_string", "$supported_pretender_old_faction", slot_faction_adjective),
      (str_store_string, s1, ":adjective_string"),

      (faction_set_name, "fac_player_supporters_faction", "@{s1} Rebels"),
      (faction_set_color, "fac_player_supporters_faction", 0xFF0000),

## Let us handle relation with other kingdoms later.
##            (try_for_range, ":existing_kingdom", kingdoms_begin, kingdoms_end),
##                (store_relation, ":relation", ":existing_kingdom", ":rebellion_target"),
##                (store_sub, ":relation_w_rebels", 0, ":relation"),
##                (store_relation, ":player_relation", ":existing_kingdom", "fac_player_supporters_faction"),
##                (val_div, ":player_relation", 3),
##                (val_add, ":relation_w_rebels", ":player_relation"),
##				  #WARNING: Never use set_relation!
##                (set_relation, ":existing_kingdom", "$g_talk_troop_faction", ":relation_w_rebels"),
##            (try_end),

# we have alrady joined.
##            (str_store_faction_name, 4, "$g_talk_troop_faction"),
##            (display_message, "@Player joins {s4}"),
##            (call_script, "script_player_join_faction", "$g_talk_troop_faction"),
      (call_script, "script_update_all_notes"),
      ]],
[anyone|plyr ,"lord_event_choose_friend", [],  "I assure you, {s65}, I am no friend of {s6}.", "lord_event_choose_friend_renounce", [
(call_script, "script_change_player_relation_with_troop","$g_talk_troop",5),
(call_script, "script_change_player_relation_with_troop","$temp",-10),
]],
[anyone ,"lord_event_choose_friend_renounce", [],  "Glad news, {playername}. I would fear for your safety otherwise.\
If you do encounter {s6}, be on your guard and don't believe a word.", "lord_pretalk", []],
[anyone|plyr ,"lord_event_choose_friend", [
##diplomacy start+ replace "man" with "{reg0?woman:man}" and "him" with "{reg0?her:him}"
(call_script, "script_dplmc_store_troop_is_female", "$temp"),
],  "{s6} is an honourable {reg0?woman:man}, you've no right to speak of {reg0?her:him} thus.", "lord_event_choose_friend_defend", [
##diplomacy end+
(call_script, "script_change_player_relation_with_troop","$g_talk_troop",-10),
(call_script, "script_change_player_relation_with_troop","$temp",5),
]],
[anyone ,"lord_event_choose_friend_defend", [],  "As you like, {playername}.\
A fool you might be, but a loyal fool at the least. {s6}'s loyalty may not be so steadfast, however...", "lord_pretalk", []],
[anyone|plyr ,"lord_event_choose_friend", [],  "I don't want to be involved in your quarrel with {s6}.", "lord_event_choose_friend_neutral", [
(call_script, "script_change_player_relation_with_troop","$g_talk_troop",-2),
(call_script, "script_change_player_relation_with_troop","$temp",-3),
]],
[anyone ,"lord_event_choose_friend_neutral", [],  "Hmph. As you wish, {playername}.\
Just remember that a {man/woman} needs friends in this world, and you'll never make any if you never stand with anyone.", "lord_pretalk", []],
[anyone|plyr ,"lord_invite_player_monarch_1", [],  "Yes... my lord.", "lord_invite_2",  []],
[anyone|plyr ,"lord_invite_player_monarch_1", [],  "No. That oath sticks in my throat.", "lord_enter_service_reject",  []],
[anyone|plyr ,"lord_invite_1", [],  "Thank you, {s65}, you honour me with your offer.", "lord_invite_2",  []],
[anyone|plyr ,"lord_invite_1", [],  "It is good to have my true value recognised.", "lord_invite_2",  []],
[anyone ,"lord_invite_2", [],  "Aye. Let us dispense with the formalities, {playername}; are you ready to swear loyalty to me?", "lord_invite_3",  []],
[anyone|plyr ,"lord_invite_3", [],  "Yes, {s65}.", "lord_give_oath_2",  []],
[anyone|plyr ,"lord_invite_3", [],  "No, {s65}. I cannot serve you right now.", "lord_enter_service_reject",  []],
[anyone|plyr ,"lord_female_pc_marriage_proposal", [],  "Yes. I would.", "lord_marriage_proposal_female_pc_next_step",  []],
[anyone|plyr ,"lord_female_pc_marriage_proposal", [],  "Let me think about this some more.", "lord_female_pc_marriage_proposal_postponed",  []],
[anyone|plyr ,"lord_female_pc_marriage_proposal", [],  "No. I have decided that it would not be appropriate", "lord_female_pc_marriage_proposal_rejected",  []],
[anyone ,"lord_female_pc_marriage_proposal_postponed", [],  "Of course, my {lord/lady}. Take all the time you need.", "lord_start",  []],
[anyone ,"lord_female_pc_marriage_proposal_rejected", [],  "Do you mean to reject my suit outright, my {lord/lady}?", "lord_female_pc_marriage_proposal_rejected_confirm",  []],
[anyone|plyr ,"lord_female_pc_marriage_proposal_rejected_confirm", [],  "Yes. I do.", "lord_female_pc_marriage_proposal_rejected_confirm_yes",  []],
[anyone|plyr ,"lord_female_pc_marriage_proposal_rejected_confirm", [],  "No, you misunderstand. I just need some more time to think", "lord_female_pc_marriage_proposal_postponed",  []],
[anyone ,"lord_female_pc_marriage_proposal_rejected_confirm_yes", [
(this_or_next|troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_debauched),
(this_or_next|troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_selfrighteous),
(troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_quarrelsome),
#diplomacy start+ gender-correct language
],  "Well, in that case, let me tell you something -- with those harsh words, you have removed the scales from my eyes. I would agree that it would not be appropriate for me to marry one such as you. Good day, my {lord/lady}.", "close_window",  [
#diplomacy end+
(call_script, "script_troop_change_relation_with_troop", "$g_talk_troop", "trp_player", -20),
(troop_set_slot, "$g_talk_troop", slot_troop_met, 4),
(assign, "$g_leave_encounter", 1),
]],
[anyone ,"lord_female_pc_marriage_proposal_rejected_confirm_yes", [],  "Such is your right, my {lord/lady}. If you ever wished to reconsider, I would be overwhelmed with joy.", "close_window",  [
#diplomacy end+
(call_script, "script_troop_change_relation_with_troop", "$g_talk_troop", "trp_player", -5),
(troop_set_slot, "$g_talk_troop", slot_troop_met, 4),
(assign, "$g_leave_encounter", 1),
]],
[anyone|plyr ,"lord_meet_neutral", [],  "I am {playername}.", "lord_intro", []],
[anyone|plyr ,"lord_meet_neutral", [
##diplomacy start+ use correct gender
],  "My name is {playername}. At your service {reg65?madame:sir}.", "lord_intro", []],
[anyone ,"lord_intro", [],
"{s11}", "lord_start", [(faction_get_slot, ":faction_leader", "$g_talk_troop_faction", slot_faction_leader),
                    (str_store_faction_name, s6, "$g_talk_troop_faction"),
                    (assign, reg4, 0),
                    (str_store_troop_name, s4, "$g_talk_troop"),
                    (try_begin),
                      (eq, ":faction_leader", "$g_talk_troop"),
                      (str_store_string, s9, "@I am {s4}, the ruler of {s6}", 0),
                    ##diplomacy start+ Alternate introduction
                    (else_try),
                       (assign, ":impressive_relative", -1),
                       (troop_get_slot, reg0, "$g_talk_troop", slot_troop_renown),
                       (val_add, reg0, 1),
                       (try_for_range_backwards, reg5, dplmc_slot_troop_relatives_begin, dplmc_slot_troop_relatives_end),
                          (troop_get_slot, reg5, "$g_talk_troop", reg5),
                          (ge, reg5, walkers_end),
                          (troop_is_hero, reg5),
                          (store_faction_of_troop, reg1, reg5),
                          (eq, reg1, "$g_talk_troop_faction"),
                          (this_or_next|faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, reg5),
                          (this_or_next|faction_slot_eq, "$g_talk_troop_faction", slot_faction_marshall, reg5),
                          (this_or_next|troop_slot_ge, reg5, slot_troop_renown, reg0),
                          (is_between, "$g_talk_troop", kingdom_ladies_begin, kingdom_ladies_end),
                          (assign, ":impressive_relative", reg5),
                       (try_end),
                       (gt, ":impressive_relative", -1),
                       (call_script, "script_dplmc_troop_get_family_relation_to_troop", "$g_talk_troop", ":impressive_relative"),
                       (str_store_string, s8, reg1),
                       (str_store_troop_name, s9, ":impressive_relative"),
                       (str_store_string, s9, "@I am {s4}, {s8} of {s9}"),
                    ##diplomacy end+
                    (else_try),
                      (str_store_string, s9, "@I am {s4}, a vassal of {s6}", 0),
                    (try_end),
                    (assign, ":num_centers", 0),
                    (str_clear, s8),
                    (try_for_range_backwards, ":cur_center", centers_begin, centers_end),
                      (party_slot_eq, ":cur_center", slot_town_lord, "$g_talk_troop"),
                      (try_begin),
                        (eq, ":num_centers", 0),
                        (str_store_party_name, s8, ":cur_center"),
                      (else_try),
                        (eq, ":num_centers", 1),
                        (str_store_party_name, s7, ":cur_center"),
                        (str_store_string, s8, "@{s7} and {s8}"),
                      (else_try),
                        (str_store_party_name, s7, ":cur_center"),
                        (str_store_string, s8, "@{!}{s7}, {s8}"),
                      (try_end),
                      (val_add, ":num_centers", 1),
                    (try_end),
                    (assign, reg5, ":num_centers"),
                    (str_store_string, s11, "@{s9}{reg5? and the lord of {s8}.:.", 0),
                    ]],
[anyone|plyr ,"lord_meet_enemy", [],  "I am {playername}, {s65}.", "lord_intro", []],
[anyone|plyr ,"lord_meet_enemy", [],  "They know me as {playername}. Mark it down, you shall be hearing of me a lot.", "lord_intro", []],
[anyone,"lord_start", [(gt, "$g_comment_found", 0), #changed to s32 from s62 because overlaps with setup_talk_info strings
             (str_store_string, s1, "$g_last_comment_copied_to_s42"),
             (try_begin),
               (eq, "$cheat_mode", 1),
               (display_message, "str_comment_found_s1"),
             (try_end),

                  ],  "{s42}", "lord_start", [
#                         (store_current_hours, ":cur_time"),
#                         (troop_set_slot, "$g_talk_troop", slot_troop_last_comment_time, ":cur_time"),
                   (try_begin),
                     (neq, "$log_comment_relation_change", 0),
                     (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", "$log_comment_relation_change"),
                   (try_end),


             (assign, "$g_comment_has_rejoinder", 0),
             (try_begin),
               (gt, "$g_rejoinder_to_last_comment", 0),
               (try_begin),
                 (eq, "$cheat_mode", 1),
                 (display_message, "str_rejoinder_noted"),
               (try_end),
               (assign, "$g_comment_has_rejoinder", 1),
             (try_end),

                   (assign, "$g_comment_found", 0),
                   ]],
[anyone|auto_proceed,"lord_start",
[
(check_quest_active, "qst_destroy_bandit_lair"),
(check_quest_succeeded, "qst_destroy_bandit_lair"),
(quest_slot_eq, "qst_destroy_bandit_lair", slot_quest_giver_troop, "$g_talk_troop"),
], "{!}.", "lair_quest_intermediate_1",
[
]],
[anyone|auto_proceed,"lord_start",
[
(check_quest_active, "qst_destroy_bandit_lair"),
(check_quest_failed, "qst_destroy_bandit_lair"),
(quest_slot_eq, "qst_destroy_bandit_lair", slot_quest_giver_troop, "$g_talk_troop"),
], "{!}.", "lair_quest_intermediate_2",
[]],
[anyone,"lord_start",
[
(store_partner_quest,":lords_quest"),
(eq,":lords_quest","qst_lend_surgeon"),
(quest_slot_eq, "qst_lend_surgeon", slot_quest_giver_troop, "$g_talk_troop")
], "Your surgeon managed to convince my friend and made the operation.  The matter is in God's hands now, and all we can do is pray for his recovery.\
Anyway, I thank you for lending your surgeon to me {sir/madam}. You have a noble spirit. I will not forget it.", "lord_generic_mission_completed",
[
(call_script, "script_finish_quest", "qst_lend_surgeon", 100),
(troop_set_slot, "$g_talk_troop", slot_troop_does_not_give_quest, 1),
]],
[anyone ,"lord_start", [(troop_slot_eq,"$g_talk_troop",slot_troop_occupation, slto_kingdom_hero),
              (check_quest_active, "qst_wed_betrothed"),

              (quest_slot_eq, "qst_wed_betrothed", slot_quest_giver_troop, "$g_talk_troop"),
              (quest_get_slot, ":bride", "qst_wed_betrothed", slot_quest_target_troop),
              (troop_slot_eq, ":bride", slot_troop_cur_center, "$g_encountered_party"),
              (faction_slot_eq, "$g_talk_troop_faction", slot_faction_ai_state, sfai_feast),
              (faction_slot_eq, "$g_talk_troop_faction", slot_faction_ai_object, "$g_encountered_party"),

              (call_script, "script_troop_get_family_relation_to_troop", ":bride", "$g_talk_troop"),
              (str_store_troop_name, s4, ":bride"),
               ],
"May the heavens witness that I am ready to give you my {s11} {s4}, to have in marriage...", "wedding_ceremony_bride_vow",
[
              (quest_get_slot, "$g_player_bride", "qst_wed_betrothed", slot_quest_target_troop),
]],
[anyone, "lord_start", [ (check_quest_active, "qst_wed_betrothed"),
              (quest_slot_eq, "qst_wed_betrothed", slot_quest_giver_troop, "$g_talk_troop"),
              (quest_get_slot, ":expiration_days", "qst_wed_betrothed", slot_quest_expiration_days),
              (lt, ":expiration_days", 362),
              (eq, "$g_done_wedding_comment", 0),
              (str_clear, s12),
              (try_begin),
               (neg|faction_slot_eq, "$g_talk_troop_faction", slot_faction_ai_state, sfai_feast),
               (neg|faction_slot_eq, "$g_talk_troop_faction", slot_faction_ai_state, sfai_default),
                (str_store_string, s12, "@ We will of course need to wait until the domain is no longer on campaign."),
              (try_end),

               ],
"It is good to see you, {playername}. We look forward to the wedding, as soon as we can all gather together for the feast.{s12}", "lord_wedding_reschedule",
[
(assign, "$g_done_wedding_comment", 1),
]],
[anyone|plyr, "lord_wedding_reschedule", [],
"It is no problem. I can wait.", "lord_start",
[
]],
[anyone|plyr, "lord_wedding_reschedule", [],
"I have no faith that this wedding will be concluded. Please return my dower.", "lord_return_dower", #add in new dialog
[]],
[anyone, "lord_return_dower", [],
"Well, that is your right, if you indeed have no confidence in our family's commitments. Take your money.", "close_window",
[
(quest_get_slot, ":bride", "qst_wed_betrothed", slot_quest_target_troop),
(fail_quest, "qst_wed_betrothed"),
(call_script, "script_end_quest", "qst_wed_betrothed"),

(troop_set_slot, "trp_player", slot_troop_betrothed, -1),
(troop_set_slot, ":bride", slot_troop_betrothed, -1),

(assign, "$marriage_dowry", 0),
(troop_add_gold, "trp_player", "$marriage_dower"),
(assign, "$marriage_dower", 0),

(call_script, "script_troop_change_relation_with_troop", "trp_player", "$g_talk_troop", -3),
(assign, "$g_leave_encounter", 1),
]],
[anyone,"lord_start", [(store_partner_quest,":lords_quest"),
                   (eq,":lords_quest","qst_incriminate_loyal_commander"),
                   (check_quest_succeeded, "qst_incriminate_loyal_commander"),
                   (quest_get_slot, ":quest_target_troop", "qst_incriminate_loyal_commander", slot_quest_target_troop),
                   (str_store_troop_name, s3, ":quest_target_troop"),
                   (quest_get_slot, reg5, "qst_incriminate_loyal_commander", slot_quest_gold_reward),
##diplomacy start+ fix pronouns
                   (call_script, "script_dplmc_store_troop_is_female", ":quest_target_troop"),
                   ],
#"his" to "{reg0?her:his}", "him" to "(reg0?her:him}"
"Hah! Our little plot against {s3} worked perfectly, {playername}.\
The fool has lost one of {reg0?her:his} most valuable retainers, and we are one step closer to bringing {reg0?her:him} to {reg0?her:his} knees.\
Here, this purse contains {reg5} mon, and I wish you to have it. You deserve every copper.\
And, need I remind you, there could be much more to come if you've a mind to earn it...", "lord_generic_mission_completed",[
##diplomacy end+
(call_script, "script_end_quest", "qst_incriminate_loyal_commander"),
(call_script, "script_change_player_relation_with_troop","$g_talk_troop",5),
(call_script, "script_change_player_honor", -10),
]],
[anyone,"lord_start", [(store_partner_quest,":lords_quest"),
                   (eq,":lords_quest","qst_incriminate_loyal_commander"),
                   (check_quest_failed, "qst_incriminate_loyal_commander")],
"You werent't able to complete a simple task. I had set up everything.\
The only thing you needed to do was sacrifice a messenger, and we would be celebrating now.\
But no, you were too damned honorable, weren't you?", "close_window",[
(call_script, "script_end_quest", "qst_incriminate_loyal_commander"),
(call_script, "script_change_player_relation_with_troop","$g_talk_troop",-5),
(call_script, "script_change_player_honor", 3),
]],
[anyone,"lord_start", [(store_partner_quest,":lords_quest"),
                   (eq,":lords_quest","qst_meet_spy_in_enemy_town"),
                   (check_quest_succeeded, "qst_meet_spy_in_enemy_town"),
                   ],
"Have you brought me any news about that task I gave you? You know the one I mean...", "quest_meet_spy_in_enemy_town_completed",
[]],
[anyone,"lord_start", [(store_partner_quest,":lords_quest"),
                   (eq,":lords_quest","qst_cause_provocation"),
                   (check_quest_succeeded, "qst_cause_provocation"),
                   (quest_get_slot, ":quest_target_faction", "qst_cause_provocation", slot_quest_target_faction),
                   (str_store_faction_name, s13, ":quest_target_faction"),
                   ],
"Brilliant work, {playername}! Whatever you did, the samurai of the {s13} are clamoring for war!\
Soon, the time will come for us to reap the benefits of our hard work, from fields ripe for plunder.\
This war is going to make us rich, mark my words!", "lord_pretalk",
[
(call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 10),
(try_for_range, ":vassal", active_npcs_begin, active_npcs_end),
(troop_slot_eq, ":vassal", slot_troop_occupation, slto_kingdom_hero),
(store_troop_faction, ":vassal_fac", ":vassal"),
(eq, ":vassal_fac", "$players_kingdom"),
(neq,  ":vassal", "$g_talk_troop"),
(store_random_in_range, ":rel_change", -5, 4),
(call_script, "script_change_player_relation_with_troop", ":vassal", ":rel_change"),
(try_end),
#TODO: Add gold reward notification before the quest is given. 500 gold is not mentioned anywhere.
(call_script, "script_troop_add_gold", "trp_player", 500),
(add_xp_as_reward, 2000),
(call_script, "script_change_player_honor", -5),
(call_script, "script_end_quest", "qst_cause_provocation")
]],
[anyone,"lord_start", [(store_partner_quest,":lords_quest"),
                   (eq,":lords_quest","qst_collect_debt"),
                   (quest_slot_eq, "qst_collect_debt", slot_quest_current_state, 1),
                   (quest_get_slot, ":target_troop", "qst_collect_debt", slot_quest_target_troop),
                   (str_store_troop_name, s7, ":target_troop"),
                   (quest_get_slot, ":total_collected","qst_collect_debt",slot_quest_target_amount),
                   (store_div, reg3, ":total_collected", 5),
                   (store_sub, reg4, ":total_collected", reg3)],
"I'm told that you've collected the money owed me from {s7}. Good, it's past time I had it back.\
I believe I promised to give you one-fifth of it all, eh?\
Well, that makes {reg3} mon, so if you give me my share -- that's {reg4} mon -- you can keep the rest.", "lord_collect_debt_completed", []],
[anyone|plyr,"lord_collect_debt_completed", [(store_troop_gold, ":gold", "trp_player"),
                                         (ge, ":gold", reg4)],
"Of course, {s65}. {reg4} mon, all here.", "lord_collect_debt_pay",[]],
[anyone,"lord_collect_debt_pay", [],
"I must admit I'm impressed, {playername}. I had lost hope of ever getting this money back.\
Please accept my sincere thanks.", "lord_pretalk",[
(troop_remove_gold, "trp_player", reg4),
##diplomacy start+ actually give gold to lord
(call_script, "script_dplmc_distribute_gold_to_lord_and_holdings", reg4, "$g_talk_troop"),
##diplomacy end+
(call_script, "script_change_player_relation_with_troop","$g_talk_troop", 2),
(add_xp_as_reward, 100),
(call_script, "script_end_quest", "qst_collect_debt")
]],
[anyone|plyr,"lord_collect_debt_completed", [], "I am afraid I don't have the money with me sir.", "lord_collect_debt_no_pay",[]],
[anyone,"lord_collect_debt_no_pay", [], "Is this a joke?\
I know full well that {s7} gave you the money, and I want every mon owed to me, {sir/madam}.\
As far as I'm concerned, I hold you personally in my debt until I see that silver.", "close_window",[
(call_script, "script_change_debt_to_troop", "$g_talk_troop", reg4),
(call_script, "script_end_quest", "qst_collect_debt"),

(call_script, "script_objectionable_action", tmt_honest, "str_squander_money"),
]],
[anyone,"lord_start", [(store_partner_quest,":lords_quest"),
                   (eq,":lords_quest","qst_kill_local_merchant"),
                   (check_quest_succeeded, "qst_kill_local_merchant"),
                   (quest_slot_eq, "qst_kill_local_merchant", slot_quest_current_state, 1)],
"I heard you got rid of that poxy merchant that was causing me so much grief.\
I can see you're not afraid to get your hands dirty, eh? I like that in a {man/woman}.\
Here's your reward. Remember, {playername}, stick with me and we'll go a long, long way together.", "close_window",
[ (call_script, "script_troop_add_gold", "trp_player", 600),
(call_script, "script_change_player_relation_with_troop","$g_talk_troop",4),
(add_xp_as_reward, 300),
(call_script, "script_end_quest", "qst_kill_local_merchant"),

(call_script, "script_objectionable_action", tmt_humanitarian, "str_murder_merchant"),

(assign, "$g_leave_encounter", 1)]],
[anyone,"lord_start", [(store_partner_quest,":lords_quest"),
                   (eq,":lords_quest","qst_kill_local_merchant"),
                   (check_quest_failed, "qst_kill_local_merchant")],
"Oh, it's you. Enlighten me, how exactly does one lose a simple fight to some poxy, lowborn merchant?\
Truly, if I ever need my guardsmen to take a lesson in how to lay down and die, I'll be sure to come to you.\
Just leave me be, {playername}, I have things to do.", "close_window",
[(call_script, "script_end_quest", "qst_kill_local_merchant"),
(assign, "$g_leave_encounter", 1)]],
[anyone,"lord_start", [(store_partner_quest,":lords_quest"),
                   (eq,":lords_quest","qst_kill_local_merchant"),
                   (check_quest_succeeded, "qst_kill_local_merchant"),
                   (quest_slot_eq, "qst_kill_local_merchant", slot_quest_current_state, 2)],
"You! Do you have sawdust between your ears? Did you think that when I said to kill the merchant,\
I meant you to have a nice chat with him and then let him go?! What possessed you?", "lord_kill_local_merchant_let_go",[]],
[anyone|plyr,"lord_kill_local_merchant_let_go", [],
"Sir, I made sure he will not act against you.", "lord_kill_local_merchant_let_go_2",[]],
[anyone,"lord_kill_local_merchant_let_go_2", [],
##diplomacy start+ change {men/people} to {men/women}
"Piffle. You were supposed to remove him, not give him a sermon and send him on his way.\
He had better do as you say, or you'll both regret it.\
Here, this is half the money I promised you. Don't say a word, {playername}, you're lucky to get even that.\
I have little use for {men/women} who cannot follow orders.", "lord_pretalk",
##diplomacy end+
[(call_script, "script_troop_add_gold", "trp_player", 300),
(call_script, "script_change_player_relation_with_troop","$g_talk_troop",2),
(add_xp_as_reward, 500),
(call_script, "script_end_quest", "qst_kill_local_merchant"),
(assign, "$g_leave_encounter", 1)
]],
[anyone,"lord_start", [#(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 0),
             (neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
                   (store_partner_quest,":lords_quest"),
                   (eq,":lords_quest","qst_follow_spy"),
                   (eq, "$qst_follow_spy_no_active_parties", 1),
                   (party_count_prisoners_of_type, ":num_spies", "p_main_party", "trp_spy"),
                   (party_count_prisoners_of_type, ":num_spy_partners", "p_main_party", "trp_spy_partner"),
                   (gt, ":num_spies", 0),
                   (gt, ":num_spy_partners", 0),
##diplomacy start+ Adjust pronouns in the event that "trp_spy" has been altered to a female model
                   (call_script, "script_dplmc_store_troop_is_female",  "trp_spy"),
],
#"his" to "{reg0?her:his}"
"Beautiful work, {playername}! You captured both the spy and {reg0?her:his} handler, just as I'd hoped,\
and the pair are now safely ensconced in my prison, waiting to be questioned.\
My torturer shall be busy tonight! Anyway, I'm very pleased with your success, {playername}, and I give you\
this purse as a token of my appreciation.", "lord_follow_spy_completed",
##diplomacy end+
[(party_remove_prisoners, "p_main_party", "trp_spy", 1),
(party_remove_prisoners, "p_main_party", "trp_spy_partner", 1),
(call_script, "script_change_player_relation_with_troop","$g_talk_troop",4),
(call_script, "script_troop_add_gold", "trp_player", 2000),
(add_xp_as_reward, 4000),
(call_script, "script_end_quest", "qst_follow_spy")]],
[anyone,"lord_start", [#(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 0),
             (neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
                   (store_partner_quest,":lords_quest"),
                   (eq,":lords_quest","qst_follow_spy"),
                   (eq, "$qst_follow_spy_no_active_parties", 1),
                   (party_count_prisoners_of_type, ":num_spies", "p_main_party", "trp_spy"),
                   (party_count_prisoners_of_type, ":num_spy_partners", "p_main_party", "trp_spy_partner"),
                   (gt, ":num_spies", 0),
                   (eq, ":num_spy_partners", 0),],
"Blast and damn you! I wanted TWO prisoners, {playername} -- what you've brought me is one step short of\
useless! I already know everything the spy knows, it was the handler I was after.\
Here, half a job gets you half a reward. Take it and begone.", "lord_follow_spy_half_completed",
[(party_remove_prisoners, "p_main_party", "trp_spy", 1),
(call_script, "script_change_player_relation_with_troop","$g_talk_troop",-1),
(call_script, "script_troop_add_gold", "trp_player", 1000),
(add_xp_as_reward, 400),
(call_script, "script_end_quest", "qst_follow_spy")]],
[anyone,"lord_start", [#(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 0),
              (neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
                   (store_partner_quest,":lords_quest"),
                   (eq,":lords_quest","qst_follow_spy"),
                   (eq, "$qst_follow_spy_no_active_parties", 1),
                   (party_count_prisoners_of_type, ":num_spies", "p_main_party", "trp_spy"),
                   (party_count_prisoners_of_type, ":num_spy_partners", "p_main_party", "trp_spy_partner"),
                   (eq, ":num_spies", 0),
                   (gt, ":num_spy_partners", 0),
##diplomacy start+ Adjust pronouns in the event that "trp_spy" has been altered to a female model
                   (call_script, "script_dplmc_store_troop_is_female",  "trp_spy"),
                   ],
#"he" to "{reg0?she:he}
"I asked you for two prisoners, {playername}, not one. Two. Still, I suppose you did capture the spy's handler,\
the more important one of the pair. The spy will not dare return here and will prove quite useless to\
whatever master {reg0?she:he} served. 'Tis better than nothing.\
However, you'll understand if I pay you half the promised reward for what is but half a success.", "lord_follow_spy_half_completed",
##diplomacy end+
[(party_remove_prisoners, "p_main_party", "trp_spy_partner", 1),
(call_script, "script_change_player_relation_with_troop","$g_talk_troop",1),
(call_script, "script_troop_add_gold", "trp_player", 1000),
(add_xp_as_reward, 400),
(call_script, "script_end_quest", "qst_follow_spy")]],
[anyone,"lord_start", [(store_partner_quest,":lords_quest"),
                   (eq,":lords_quest","qst_follow_spy"),
                   (eq, "$qst_follow_spy_no_active_parties", 1),
                   (party_count_prisoners_of_type, ":num_spies", "p_main_party", "trp_spy"),
                   (party_count_prisoners_of_type, ":num_spy_partners", "p_main_party", "trp_spy_partner"),
                   (eq, ":num_spies", 0),
                   (eq, ":num_spy_partners", 0),
##diplomacy start+ Adjust pronouns in the event that "trp_spy" has been altered to a female model
                   (call_script, "script_dplmc_store_troop_is_female",  "trp_spy"),
                   ],
#"his" to "{reg0?her:his}"
"Truly, {playername}, you are nothing short of totally incompetent.\
Failing to capture both the spy AND {reg0?her:his} handler plumbs astonishing new depths of failure.\
Forget any reward I offered you. You've done nothing to earn it.", "lord_follow_spy_failed",
##diplomacy end+
[
(call_script, "script_change_player_relation_with_troop","$g_talk_troop",-2),
(call_script, "script_end_quest", "qst_follow_spy"),
]],
[anyone|plyr,"lord_follow_spy_half_completed", [],
"I did my best, {s65}.", "lord_pretalk", []],
[anyone|plyr,"lord_follow_spy_completed", [],
"Thank you, {s65}.", "lord_pretalk", []],
[anyone|plyr,"lord_follow_spy_failed", [],
"Hrm. As you like, {s65}.", "lord_pretalk", []],
[anyone,"lord_start", [(store_partner_quest,":lords_quest"),
                   (eq,":lords_quest","qst_bring_back_runaway_serfs"),
                   (check_quest_succeeded, "qst_bring_back_runaway_serfs")],
"Splendid work, {playername}. All the peasants are back, properly cowed, and they're busy preparing for the harvest.\
You certainly earned your reward. Here, take it, with my compliments.", "lord_generic_mission_completed",
[(call_script, "script_change_player_relation_with_troop","$g_talk_troop", 2),
(call_script, "script_troop_add_gold", "trp_player", 300),
(add_xp_as_reward, 300),
(call_script, "script_end_quest", "qst_bring_back_runaway_serfs"),
(call_script, "script_objectionable_action", tmt_humanitarian, "str_round_up_serfs"),
]],
[anyone,"lord_start", [(store_partner_quest,":lords_quest"),
                   (eq,":lords_quest","qst_bring_back_runaway_serfs"),
                   (check_quest_failed, "qst_bring_back_runaway_serfs"),],
"{playername}. I have been waiting patiently for my peasants, yet none have returned. Have you an explanation?\
Were you outwitted by simple fieldhands, or are you merely incompetent?\
Or perhaps you are plotting with my enemies, intending to ruin me...", "lord_bring_back_runaway_serfs_failed", []],
[anyone|plyr,"lord_bring_back_runaway_serfs_failed", [],
"Forgive me, {s65}, those peasants were slippery as eels.", "lord_bring_back_runaway_serfs_failed_1a", []],
[anyone|plyr,"lord_bring_back_runaway_serfs_failed", [],
"Perhaps if you had treated them better...", "lord_bring_back_runaway_serfs_failed_1b", []],
[anyone,"lord_bring_back_runaway_serfs_failed_1a", [],
"Hmph, that is hardly an excuse for failure, {playername}.\
Now if you will excuse me, I need to recruit new men to work these fields before we all starve.", "lord_pretalk",
[(call_script, "script_change_player_relation_with_troop","$g_talk_troop",-1),
(call_script, "script_end_quest", "qst_bring_back_runaway_serfs")]],
[anyone,"lord_bring_back_runaway_serfs_failed_1b", [],
"Hah, now you reveal your true colours, traitor! Your words match your actions all too well. I should never have trusted you.", "close_window",
[(call_script, "script_change_player_relation_with_troop","$g_talk_troop",-10),
(quest_get_slot, ":home_village", "qst_bring_back_runaway_serfs", slot_quest_object_center),
(call_script, "script_change_player_relation_with_center",":home_village",6),
(call_script, "script_end_quest", "qst_bring_back_runaway_serfs"),
(assign, "$g_leave_encounter", 1),
]],
[anyone,"lord_start", [(store_partner_quest,":lords_quest"),
                   (eq,":lords_quest","qst_bring_back_runaway_serfs"),
                   (check_quest_concluded, "qst_bring_back_runaway_serfs"),
                   (assign, reg17, "$qst_bring_back_runaway_serfs_num_parties_returned")],
"You disappoint me, {playername}. There were 3 groups of peasants that I charged you to return. 3. Not {reg17}.\
I suppose the ones who did come back shall have to work twice as hard to make up for those that got away.\
As for your reward, {playername}, I'll only pay you for the peasants you returned, not the ones you let fly.\
Here. Take it, and let this business be done.", "lord_runaway_serf_half_completed",
[(store_mul, ":reward", "$qst_bring_back_runaway_serfs_num_parties_returned", 100),
(val_div, ":reward", 2),
#	(store_div, ":relation_boost", "$qst_bring_back_runaway_serfs_num_parties_returned", 1),
#    (call_script, "script_change_player_relation_with_troop","$g_talk_troop", ":relation_boost"),
(call_script, "script_troop_add_gold", "trp_player", ":reward"),
(add_xp_as_reward, ":reward"),


(call_script, "script_objectionable_action", tmt_humanitarian, "str_round_up_serfs"),

(call_script, "script_end_quest", "qst_bring_back_runaway_serfs"),
]],
[anyone|plyr,"lord_runaway_serf_half_completed", [],
"Thank you, {s65}. You are indeed generous.", "lord_pretalk", []],
[anyone|plyr,"lord_runaway_serf_half_completed", [],
"Bah, this proved to be a waste of my time.", "lord_pretalk", []],
[anyone,"lord_start", [(store_partner_quest,":lords_quest"),
                   (eq,":lords_quest","qst_deal_with_bandits_at_lords_village"),
                   (check_quest_succeeded, "qst_deal_with_bandits_at_lords_village")],
"{playername}, I was told that you have crushed the bandits at my village of {s5}. Please know that I am most grateful to you for that.\
Please, let me pay the expenses of your campaign. Here, I hope these {reg14} mon will be adequate.", "lord_deal_with_bandits_completed",
[
 (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 3),
 (store_character_level, ":level", "trp_player"),
 (store_mul, ":reward", ":level", 20),
 (val_add, ":reward", 300),
 (call_script, "script_troop_add_gold", "trp_player", ":reward"),
 (add_xp_as_reward, 350),
 (call_script, "script_end_quest", "qst_deal_with_bandits_at_lords_village"),
 (assign, reg14, ":reward"),
 (quest_get_slot, ":village", "qst_deal_with_bandits_at_lords_village", slot_quest_target_center),
 (str_store_party_name, s5, ":village"),
 ]],
[anyone|plyr, "lord_deal_with_bandits_completed", [],
"Not a problem, {s65}.", "lord_pretalk",[]],
[anyone|plyr, "lord_deal_with_bandits_completed", [],
"Glad to be of service.", "lord_pretalk",[]],
[anyone|plyr, "lord_deal_with_bandits_completed", [],
"It was mere child's play.", "lord_pretalk",[]],
[anyone,"lord_start", [(store_partner_quest,":lords_quest"),
                   (eq,":lords_quest","qst_deal_with_bandits_at_lords_village"),
                   (check_quest_concluded, "qst_deal_with_bandits_at_lords_village")],
"Damn it, {playername}. I heard that you were unable to drive off the bandits from my village of {s5}, and thanks to you, my village now lies in ruins.\
Everyone said that you were a capable warrior, but appearently, they were wrong.", "lord_pretalk",
[
 (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", -5),
 (call_script, "script_end_quest", "qst_deal_with_bandits_at_lords_village"),
 (quest_get_slot, ":village", "qst_deal_with_bandits_at_lords_village", slot_quest_target_center),
 (str_store_party_name, s5, ":village"),
 ]],
[anyone,"lord_start", [(store_partner_quest,":lords_quest"),
                   (eq, ":lords_quest", "qst_scout_waypoints"),
                   (check_quest_succeeded, "qst_scout_waypoints"),
                   (str_store_party_name, s13, "$qst_scout_waypoints_wp_1"),
                   (str_store_party_name, s14, "$qst_scout_waypoints_wp_2"),
                   (str_store_party_name, s15, "$qst_scout_waypoints_wp_3"),
                   ],
"You make a good scout, {playername}. My runner just brought me your reports of the mission to {s13}, {s14} and {s15}. Well done.", "lord_scout_waypoints_thank",
[
#TODO: Change reward
(call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 1),
#     (call_script, "script_troop_add_gold", "trp_player", 100),
(add_xp_as_reward, 100),
(call_script, "script_end_quest", "qst_scout_waypoints"),
#Reactivating follow army quest
(str_store_troop_name_link, s9, "$g_talk_troop"),
(setup_quest_text, "qst_follow_army"),
(str_store_string, s2, "str_follow_army_quest_brief_2"),
(call_script, "script_start_quest", "qst_follow_army", "$g_talk_troop"),
(assign, "$g_player_follow_army_warnings", 0),
]],
[anyone|plyr, "lord_scout_waypoints_thank", [],
"A simple task, {s65}.", "lord_pretalk",[]],
[anyone|plyr, "lord_scout_waypoints_thank", [],
"Nothing I couldn't handle.", "lord_pretalk",[]],
[anyone|plyr, "lord_scout_waypoints_thank", [],
"My pleasure, {s65}.", "lord_pretalk",[]],
[anyone, "lord_start",
[
(check_quest_active, "qst_follow_army"),
(faction_slot_eq, "$g_talk_troop_faction", slot_faction_marshall, "$g_talk_troop"),
(eq, "$g_random_army_quest", "qst_deliver_cattle_to_army"),
(quest_get_slot, ":quest_target_amount", "$g_random_army_quest", slot_quest_target_amount),
(assign, reg3, ":quest_target_amount"),
],
"The army's supplies are dwindling too quickly, {playername}. I need you to bring me {reg3} sacks of white rice so I can keep the troops fed. I care very little about where you get them, just bring them to me as soon as you can.", "lord_mission_told_deliver_cattle_to_army",
[
]
],
[anyone|plyr,"lord_mission_told_deliver_cattle_to_army", [], "Very well, I can find you some rice.", "lord_mission_told_deliver_cattle_to_army_accepted",[]],
[anyone|plyr,"lord_mission_told_deliver_cattle_to_army", [], "Sorry, sir, I have other plans.", "lord_mission_told_deliver_cattle_to_army_rejected",[]],
[anyone,"lord_mission_told_deliver_cattle_to_army_accepted", [], "Excellent! You know what to do, {playername}, now get to it. I need that cattle sooner rather than later.", "close_window",
[
(call_script, "script_end_quest", "qst_follow_army"),
(quest_get_slot, ":quest_target_amount", "$g_random_army_quest", slot_quest_target_amount),
(str_store_troop_name_link, s13, "$g_talk_troop"),
(assign, reg3, ":quest_target_amount"),
(setup_quest_text, "$g_random_army_quest"),
(str_store_string, s2, "@{s13} asked you to gather {reg3} sacks of white rice and deliver them back to him."),
(call_script, "script_start_quest", "$g_random_army_quest", "$g_talk_troop"),
#TODO: Change this value
(call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 1),
(assign, "$g_leave_encounter",1),
]],
[anyone, "lord_mission_told_deliver_cattle_to_army_rejected", [], "That . . . is unfortunate, {playername}. I shall have to find someone else who's up to the task. Please go now, I've work to do.", "close_window",
[(troop_set_slot, "$g_talk_troop", slot_troop_does_not_give_quest, 1),
(assign, "$g_leave_encounter",1),]],
[anyone,"lord_start",[(check_quest_active,"qst_report_to_army"),
                  (quest_slot_eq, "qst_report_to_army", slot_quest_target_troop, "$g_talk_troop"),
            (assign, ":kingdom_at_war", 0),
            (try_for_range, ":kingdom", kingdoms_begin, kingdoms_end),
               (store_relation, ":relation", ":kingdom", "$players_kingdom"),
               (lt, ":relation", 0),
               (assign, ":kingdom_at_war", 1),
            (try_end),
            (eq, ":kingdom_at_war", 0),
                  ],
"Thank you for answering the summons, {playername}. However, as we are now at peace, we do not need your services. You may attend to your other business.", "lord_pretalk",
[
(call_script, "script_end_quest", "qst_report_to_army"),
(quest_set_slot, "qst_report_to_army", slot_quest_giver_troop, "$g_talk_troop"),
#TODO: Change this value
(call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 1),
]],
[anyone,"lord_start",[
             (check_quest_active,"qst_report_to_army"),
                  (quest_slot_eq, "qst_report_to_army", slot_quest_target_troop, "$g_talk_troop"),
                  ],
"Ah, you have arrived at last, {playername}. We've been expecting you. I hope you have brought with you troops of sufficient number and experience.", "lord_report_to_army_asked",
[]],
[anyone|plyr,"lord_report_to_army_asked", [(quest_get_slot, ":quest_target_amount", "qst_report_to_army", slot_quest_target_amount),
                                       (call_script, "script_party_count_fit_for_battle", "p_main_party"),
                                       (gt, reg0, ":quest_target_amount"), # +1 for player
                                       ],
"I have a company of good, hardened soldiers with me. We are ready to join you.", "lord_report_to_army_completed",
[]],
[anyone|plyr,"lord_report_to_army_asked", [],
"I don't have the sufficient number of troops yet. I will need some more time.", "lord_report_to_army_continue",
[]],
[anyone,"lord_report_to_army_completed", [], "Excellent. We'll be moving soon. Now -- you are a {man/warrior} of sound judgement, and we trust that you will do what is necessary to support our campaign. I do not require you to remain close at hand, and I will not count it against you if you believe that your forces would be of better use elsewhere. But if you do choose to remain with me, to support me in battle, that would be appreciated. I may also have additional tasks for you to perform.", "close_window",[
(call_script, "script_end_quest", "qst_report_to_army"),
(quest_set_slot, "qst_report_to_army", slot_quest_giver_troop, "$g_talk_troop"),
#TODO: Change this value
(call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 1),
#Activating follow army quest
(str_store_troop_name_link, s9, "$g_talk_troop"),
(setup_quest_text, "qst_follow_army"),
(str_store_string, s2, "@{s9} wants you to follow his army until further notice."),
(call_script, "script_start_quest", "qst_follow_army", "$g_talk_troop"),
(assign, "$g_player_follow_army_warnings", 0),
(assign, "$g_leave_encounter", 1),
]],
[anyone,"lord_report_to_army_continue", [], "Then you'd better hurry. We'll be moving out soon against the enemy and I need every able hand we can muster.", "close_window",
[(assign, "$g_leave_encounter",1),
#Must be closed because of not letting player to terminate this quest on the general conversation
]],
[anyone, "lord_start",
[
(check_quest_active, "qst_follow_army"),
(faction_slot_eq, "$players_kingdom", slot_faction_marshall, "$g_talk_troop"),
(eq, "$g_random_army_quest", "qst_scout_waypoints"),
(str_store_party_name, s13, "$qst_scout_waypoints_wp_1"),
(str_store_party_name, s14, "$qst_scout_waypoints_wp_2"),
(str_store_party_name, s15, "$qst_scout_waypoints_wp_3"),
],
"{playername}, I need a volunteer to scout the area. We're sorely lacking on information,\
and I simply must have a better picture of the situation before we can proceed.\
I want you to go to {s13}, {s14} and {s15} and report back whatever you find.", "lord_mission_told_scout_waypoints",
[
]],
[anyone|plyr, "lord_mission_told_scout_waypoints", [], "You've found your volunteer, sir.", "lord_mission_told_scout_waypoints_accepted",[]],
[anyone|plyr, "lord_mission_told_scout_waypoints", [], "I fear I must decline.", "lord_mission_told_scout_waypoints_rejected",[]],
[anyone,"lord_mission_told_scout_waypoints_accepted", [], "Good {man/lass}! Simply pass near {s13}, {s14} and {s15} and check out what's there. Make a note of anything you find and return to me as soon as possible.", "close_window",
[
(call_script, "script_end_quest", "qst_follow_army"),
(str_store_troop_name_link, s9, "$g_talk_troop"),
(str_store_party_name_link, s13, "$qst_scout_waypoints_wp_1"),
(str_store_party_name_link, s14, "$qst_scout_waypoints_wp_2"),
(str_store_party_name_link, s15, "$qst_scout_waypoints_wp_3"),
(setup_quest_text, "$g_random_army_quest"),
(str_store_string, s2, "@{s9} asked you to scout {s13}, {s14} and {s15}, then report back."),
(call_script, "script_start_quest", "$g_random_army_quest", "$g_talk_troop"),
#TODO: Change this value
(call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 1),
(assign, "$g_leave_encounter",1),
]],
[anyone,"lord_mission_told_scout_waypoints_rejected", [], "Hm. I'm disappointed, {playername}. Very disappointed. We'll talk later, I need to go and find somebody to scout for us.", "lord_pretalk",
[(troop_set_slot, "$g_talk_troop", slot_troop_does_not_give_quest, 1)]],
[anyone,"lord_generic_mission_thank", [],
"You have been most helpful, {playername}. My thanks.", "lord_generic_mission_completed",[]],
[anyone|plyr,"lord_generic_mission_completed", [],
"It was an honour to serve.", "lord_pretalk",[]],
[anyone,"lord_start", [#(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 0),
                   (neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
                   (troop_get_slot, ":cur_debt", "$g_talk_troop", slot_troop_player_debt),
                   (gt, ":cur_debt", 0),
                   (assign, reg1, ":cur_debt")],
"I think you owe me {reg1} mon, {playername}. Do you intend to pay your debt anytime soon?", "lord_pay_debt_2",[]],
[anyone|plyr, "lord_pay_debt_2", [(troop_get_slot, ":cur_debt", "$g_talk_troop", slot_troop_player_debt),
                              (store_troop_gold, ":cur_gold", "trp_player"),
                              (le, ":cur_debt", ":cur_gold")],
"That is why I came, {s65}. Here it is, every mon I owe you.", "lord_pay_debt_3_1", [(troop_get_slot, ":cur_debt", "$g_talk_troop", slot_troop_player_debt),
                                             (troop_remove_gold, "trp_player", ":cur_debt"),
                              ##diplomacy start+ actually give gold to lord
                              (call_script, "script_dplmc_distribute_gold_to_lord_and_holdings", ":cur_debt", "$g_talk_troop"),
                              ##diplomacy end+
                                             (troop_set_slot, "$g_talk_troop", slot_troop_player_debt, 0)]],
[anyone|plyr, "lord_pay_debt_2", [],
"Alas, I don't have sufficient funds, {s65}. But I'll pay you soon enough.", "lord_pay_debt_3_2", []],
[anyone, "lord_pay_debt_3_1", [],
"Ah, excellent. You are a {man/woman} of honour, {playername}. I am satisfied. Your debt to me has been paid in full.", "lord_pretalk", []],
[anyone, "lord_pay_debt_3_2", [],
"Well, don't keep me waiting much longer.", "lord_pretalk", []],
[anyone,"lord_start",[
            (eq, "$g_romantic_comment_made", 0),
            (ge, "$g_talk_troop_relation", 20),
            (troop_slot_ge, "trp_player", slot_troop_renown, 250),
            (neg|troop_slot_ge, "trp_player", slot_troop_spouse, kingdom_ladies_begin),

            ##diplomacy start+
            #(troop_get_type, ":is_female", "trp_player"),
            #(eq, ":is_female", 0),

            #don't overlook marriage to female lords
		    (neg|troop_slot_ge, "trp_player", slot_troop_spouse, active_npcs_begin),
            #get courtship of female lords to work
            (assign, ":player_type", "$character_gender"),
			(call_script, "script_dplmc_store_troop_is_female", "$g_talk_troop"),
			(assign, ":troop_type", reg0),
			(assign, reg65, reg0),

            (this_or_next|neg|troop_slot_eq,"$g_talk_troop",slot_troop_spouse,-1),#added
               (eq, ":troop_type", ":player_type"),
            ##diplomacy end+
            (assign, ":third_party_introduce", 0),

            (try_for_range, ":lady", kingdom_ladies_begin, kingdom_ladies_end),
               ##diplomacy start+  if promotion is possible this check is necessary
               (troop_slot_eq, ":lady", slot_troop_occupation, slto_kingdom_lady),
               (call_script, "script_dplmc_store_troop_is_female", ":lady"),
               (assign, ":lady_type", reg0),
               #if various genders are possible this check is necessary
               (this_or_next|ge, "$g_disable_condescending_comments", 2),
                  (neq, ":lady_type", ":player_type"),
               ##diplomacy end+
               (troop_slot_eq, ":lady", slot_troop_spouse, -1),
               (troop_slot_eq, ":lady", slot_troop_betrothed, -1),
               (troop_slot_eq, ":lady", slot_troop_cur_center, "$g_encountered_party"),
               (neg|troop_slot_ge, ":lady", slot_troop_met, 4),

               (call_script, "script_get_kingdom_lady_social_determinants", ":lady"),
               (eq, reg0, "$g_talk_troop"),

               (assign, "$marriage_candidate", ":lady"),
               (call_script, "script_npc_decision_checklist_male_guardian_assess_suitor", "$g_talk_troop", "trp_player"),
               (gt, reg0, 0),

               (assign, ":third_party_introduce", ":lady"),
            (try_end),
            (gt, ":third_party_introduce", 0),
            (troop_slot_eq, ":third_party_introduce", slot_troop_met, 0),

            (call_script, "script_troop_get_family_relation_to_troop", ":third_party_introduce", "$g_talk_troop"),
            ##diplomacy start+
            #This normally cannot happen due to the way that script_get_kingdom_lady_social_determinants works, but it might
            #reasonably be changed in a mod.
            (try_begin),
               (eq, reg0, 0),
               (str_store_string, s11, "@pupil"),#just something to fill the empty space
            (try_end),
            ##diplomacy end+
            (str_store_troop_name, s14, ":third_party_introduce"),
            ],
"By the way, I hope you get a chance to meet my {s11}, {s14}.  ", "lord_start",
[
            (troop_set_slot, "$g_talk_troop", slot_lord_granted_courtship_permission, 1),
            (assign, "$g_romantic_comment_made", 1),
]],
[anyone,"lord_start",[
            (eq, "$g_romantic_comment_made", 0),
            (ge, "$g_talk_troop_relation", 20),
            (troop_slot_ge, "trp_player", slot_troop_renown, 250),
            (assign, ":third_party_introduce", 0),

            (neg|troop_slot_ge, "trp_player", slot_troop_spouse, kingdom_ladies_begin),
            #diplomacy start+
            #extra check since the wife may be a lord
            (neg|troop_slot_ge, "trp_player", slot_troop_spouse, active_npcs_begin),
            #enable this for women as well
            (assign, ":player_type", "$character_gender"),
            ##(neq, ":player_type", tf_female),
            #diplomacy end+


            (try_for_range, ":lady", kingdom_ladies_begin, kingdom_ladies_end),
               ##diplomacy start+  if promotion is possible this check is necessary
               (troop_slot_eq, ":lady", slot_troop_occupation, slto_kingdom_lady),
               (call_script, "script_dplmc_store_troop_is_female", ":lady"),
               (assign, ":lady_type", reg0),
               #if various genders are possible this check is necessary
               (this_or_next|ge, "$g_disable_condescending_comments", 2),
                  (neq, ":lady_type", ":player_type"),
               ##diplomacy end+
               (troop_slot_eq, ":lady", slot_troop_spouse, -1),
               (troop_slot_eq, ":lady", slot_troop_betrothed, -1),
               (troop_slot_eq, ":lady", slot_troop_cur_center, "$g_encountered_party"),
               (neg|troop_slot_ge, ":lady", slot_troop_met, 4),

               (call_script, "script_get_kingdom_lady_social_determinants", ":lady"),
               (eq, reg0, "$g_talk_troop"),

               (assign, "$marriage_candidate", ":lady"),
               (call_script, "script_npc_decision_checklist_male_guardian_assess_suitor", "$g_talk_troop", "trp_player"),
               (gt, reg0, 0),

               (troop_slot_ge, ":lady", slot_troop_met, 1),

               (store_current_hours, ":hours"),
               (troop_get_slot, ":lady_last_met_hour", ":lady", slot_troop_last_talk_time),
               (val_sub, ":hours", ":lady_last_met_hour"),
               (ge, ":hours", 24),

               (assign, ":third_party_introduce", ":lady"),
            (try_end),

            (gt, ":third_party_introduce", 0),
            (call_script, "script_troop_get_family_relation_to_troop", ":third_party_introduce", "$g_talk_troop"),
            ##diplomacy start+
            #This normally cannot happen due to the way that script_get_kingdom_lady_social_determinants works, but it might
            #reasonably be changed in a mod.
            (try_begin),
               (eq, reg0, 0),
               (str_store_string, s11, "@pupil"),#just something to fill the empty space
            (try_end),
            (assign, reg0, ":lady_type"),#Use the correct pronouns
            (str_store_troop_name, s14, ":third_party_introduce"),

            ],
#"her" to "{reg0?her:him}", "She" to "{reg0?She:he}", "her" to "{reg0?her:his}"
"By the way, I am sure that my {s11}, {s14}, would be delighted were you to pay {reg0?her:him} a visit. {reg0?She:He} awaits you in {reg0?her:his} chambers.", "lord_start",
##diplomacy end+
[
(troop_set_slot, "$g_talk_troop", slot_lord_granted_courtship_permission, 1),
(assign, "$g_romantic_comment_made", 1),

]],
[anyone,"lord_start", [(party_slot_eq, "$g_encountered_party",slot_town_lord, "$g_talk_troop"),#we are talking to Town's Lord.
                   (ge,"$g_talk_troop_faction_relation",0),
                   (neq, "$g_ransom_offer_rejected", 1),
                   (lt, "$g_encountered_party_2", 0), #town is not under siege
                   (hero_can_join_as_prisoner, "$g_encountered_party"),
                   (store_random_in_range, ":random_no", 0, 100),
                   (lt, ":random_no", 10),#start this conversation with a 10% chance
                   (party_get_num_prisoner_stacks,":num_prisoner_stacks","p_main_party"),
                   (assign, "$prisoner_lord_to_buy", -1),
                   (try_for_range,":i_pris_stack",0,":num_prisoner_stacks"),
                     (party_prisoner_stack_get_troop_id, ":t_id", "p_main_party", ":i_pris_stack"),
                     (troop_slot_eq, ":t_id", slot_troop_occupation, slto_kingdom_hero),
                     (store_troop_faction, ":fac", ":t_id"),
                     (store_relation, ":rel", ":fac", "$g_talk_troop_faction"),
                     (lt,  ":rel", 0),
                     (assign, "$prisoner_lord_to_buy", ":t_id"),
                   (try_end),
                   (gt, "$prisoner_lord_to_buy", 0), #we have a prisoner lord.
                   (assign, ":continue", 1),
                   (try_begin),
                     (check_quest_active, "qst_capture_enemy_hero"),
                     (store_troop_faction, ":prisoner_faction", "$prisoner_lord_to_buy"),
                     (quest_slot_eq, "qst_capture_enemy_hero", slot_quest_target_faction, ":prisoner_faction"),
                     (assign, ":continue", 0),
                   (try_end),
                   (eq, ":continue", 1),
                   (str_store_troop_name, s3, "$prisoner_lord_to_buy"),
                   (assign, reg5, "$prisoner_lord_to_buy"),
                   (call_script, "script_calculate_ransom_amount_for_troop", "$prisoner_lord_to_buy"),
                   (assign, reg6, reg0),
                   (val_div, reg6, 2),
                   (assign, "$temp", reg6),
##diplomacy start+ use the correct pronoun for the enemy lord
                   (call_script, "script_dplmc_store_troop_is_female",  "$prisoner_lord_to_buy"),
                   ],
#"he" to "{reg0?she:he}", etc.
"I heard that you have captured our enemy {s3} and {reg0?she:he} is with you at the moment.\
I can pay you {reg6} mon for {reg0?her:him} if you want to get rid of {reg0?her:him}.\
You can wait for {reg0?her:his} family to pay {reg0?her:his} ransom of course, but there is no telling how long that will take, eh?\
", "lord_buy_prisoner", []],
[anyone|plyr,"lord_buy_prisoner", [],
"I accept your offer. I'll leave {s3} to you for {reg6} mon.", "lord_buy_prisoner_accept", []],
[anyone|plyr,"lord_buy_prisoner", [],
"I fear I can't accept your offer.", "lord_buy_prisoner_deny", [(assign, "$g_ransom_offer_rejected", 1),]],
[anyone,"lord_buy_prisoner_accept", [],
"Excellent! Here's your {reg6} mon.\
I'll send some men to take him to our prison with due haste.", "lord_pretalk", [
(remove_troops_from_prisoners,  "$prisoner_lord_to_buy", 1),
(call_script, "script_troop_add_gold", "trp_player", "$temp"),
(party_add_prisoners, "$g_encountered_party", "$prisoner_lord_to_buy", 1),
#(troop_set_slot, "$prisoner_lord_to_buy", slot_troop_is_prisoner, 1),
(troop_set_slot, "$prisoner_lord_to_buy", slot_troop_prisoner_of_party, "$g_encountered_party"),
]],
[anyone,"lord_buy_prisoner_deny", [],
"Mmm. As you wish, {playername}, but you'll not get a better offer. Take it from me.", "lord_pretalk", []],
[anyone,"lord_start", [
(faction_slot_eq, "$g_talk_troop_faction", slot_faction_ai_state, sfai_feast),
(faction_slot_eq, "$g_talk_troop_faction", slot_faction_ai_object, "$g_encountered_party"),

(check_quest_active, "qst_organize_feast"),
(quest_slot_eq, "qst_organize_feast", slot_quest_target_center, "$g_encountered_party"),


(try_begin),
(eq, "$g_talk_troop_faction", "fac_kingdom_4"),
(str_store_string, s5, "str_flagon_of_mead"),
(else_try),
(store_mod, ":mode", "$g_talk_troop", 2),
(eq, ":mode", 0),
(eq, "$g_talk_troop_faction", "fac_kingdom_3"),
(str_store_string, s5, "str_skin_of_kumis"),
(else_try),
(store_mod, ":mode", "$g_talk_troop", 2),
(eq, ":mode", 0),
(eq, "$g_talk_troop_faction", "fac_kingdom_2"),
(str_store_string, s5, "str_mug_of_kvass"),
(else_try),
(str_store_string, s5, "str_cup_of_wine"),
(try_end),



],
"I lift a {s5} to your health, {playername}! You are most gracious to host us on this occasion. Now, what is it?", "lord_talk",[
(call_script, "script_internal_politics_rate_feast_to_s9", "trp_household_possessions", 120, "$players_kingdom", 0),
(assign, ":quality_of_feast", reg0),

(try_begin),
(ge, ":quality_of_feast", 20),
(ge, "$g_time_since_last_talk", 24),
(call_script, "script_troop_change_relation_with_troop", "$g_talk_troop", "trp_player", 1),
(try_end),
]],
[anyone,"lord_start", [
##diplomacy start+ Support the player as the ruler/co-ruler of an NPC kingdom.
(assign, reg0, 0),
(try_begin),
    (is_between, "$g_talk_troop_faction", npc_kingdoms_begin, npc_kingdoms_end),
    (neg|faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, "$g_talk_troop"),
    (call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", "$players_kingdom"),
(try_end),
(this_or_next|ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
##diplomacy end+
(faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, "trp_player"),
(faction_slot_eq, "$g_talk_troop_faction", slot_faction_ai_state, sfai_feast),
(faction_slot_eq, "$g_talk_troop_faction", slot_faction_ai_object, "$g_encountered_party"),

],
"To your health, Oyakata-sama. Long may you live. What do you wish to discuss?", "lord_talk",[
(try_begin),
(this_or_next|party_slot_eq, "$g_encountered_party", slot_town_lord, "trp_player"),
(party_slot_eq, "$g_encountered_party", slot_town_lord, "$g_talk_troop"),
(ge, "$g_time_since_last_talk", 24),
(ge, "$g_talk_troop_relation", 0),
(call_script, "script_troop_change_relation_with_troop", "$g_talk_troop", "trp_player", 1),
(try_end),

]],
[anyone,"lord_start", [
##diplomacy start+ Support the player as the ruler/co-ruler of an NPC kingdom.
(assign, reg0, 0),
(try_begin),
    (is_between, "$g_talk_troop_faction", npc_kingdoms_begin, npc_kingdoms_end),
    (neg|faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, "$g_talk_troop"),
    (call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", "$players_kingdom"),
(try_end),
(neg|faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, "$g_talk_troop"),
(this_or_next|ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
##diplomacy end+
(faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, "trp_player"),
],
"What do you wish to discuss?", "lord_talk",[]],
[anyone,"lord_start", [
(faction_slot_eq, "$g_talk_troop_faction", slot_faction_ai_state, sfai_feast),
(faction_slot_eq, "$g_talk_troop_faction", slot_faction_ai_object, "$g_encountered_party"),
(ge, "$g_encountered_party_relation", 0),
(party_slot_eq, "$g_encountered_party", slot_town_lord, "$g_talk_troop"),
(neq, "$talk_context", tc_castle_gate),
],
"I wish to welcome you to my hall on this auspicious occasion. Now, what is it?", "lord_talk",[
(try_begin),
(is_between, "$g_talk_troop_relation", 0, 10),
(ge, "$g_time_since_last_talk", 24),
(call_script, "script_troop_change_relation_with_troop", "$g_talk_troop", "trp_player", 2),
(try_end),
]],
[anyone,"lord_start", [
(faction_slot_eq, "$g_talk_troop_faction", slot_faction_ai_state, sfai_feast),
(faction_slot_eq, "$g_talk_troop_faction", slot_faction_ai_object, "$g_encountered_party"),
(ge, "$g_encountered_party_relation", 0),
(party_get_slot, ":town_lord", "$g_encountered_party", slot_town_lord),
(str_store_troop_name, s4, ":town_lord"),

(neq, "$talk_context", tc_castle_gate),


(try_begin),
(eq, "$g_talk_troop_faction", "fac_kingdom_4"),
(str_store_string, s5, "str_flagon_of_mead"),
(else_try),
(store_mod, ":mode", "$g_talk_troop", 2),
(eq, ":mode", 0),
(eq, "$g_talk_troop_faction", "fac_kingdom_3"),
(str_store_string, s5, "str_skin_of_kumis"),
(else_try),
(store_mod, ":mode", "$g_talk_troop", 2),
(eq, ":mode", 0),
(eq, "$g_talk_troop_faction", "fac_kingdom_2"),
(str_store_string, s5, "str_mug_of_kvass"),
(else_try),
(str_store_string, s5, "str_cup_of_wine"),
(try_end),

],
"Let us lift a {s5} to the health of our host, {s4}. Now, what is it?", "lord_talk",[]],
[anyone|plyr,"lord_talk", [
(check_quest_active, "qst_offer_gift"),
(quest_slot_eq, "qst_offer_gift", slot_quest_giver_troop, "$g_talk_troop"),

(quest_get_slot, ":target_troop", "qst_offer_gift", slot_quest_target_troop),
(str_store_troop_name, s4, ":target_troop"),
(player_has_item, "itm_furs"),
(player_has_item, "itm_velvet"),
],
"I have the materials for {s4}'s gift.", "offer_gift_quest_complete",[
]],
[anyone|plyr,"lord_talk", [
(check_quest_active, "qst_intrigue_against_lord"),
(neg|check_quest_succeeded, "qst_intrigue_against_lord"),
(neg|check_quest_failed, "qst_intrigue_against_lord"),

(quest_get_slot, ":target_troop", "qst_intrigue_against_lord", slot_quest_target_troop), #was qst_offer_gift
(store_faction_of_troop, ":target_troop_faction", ":target_troop"),
(faction_slot_eq, ":target_troop_faction", slot_faction_leader, "$g_talk_troop"),
],
##diplomacy start+ Change lord to {reg65?lady:lord}
"My {reg65?lady:lord} -- there is something I wish to tell you in confidence, about one of your vassals.", "intrigue_quest_state_complaint",[
##diplomacy end+
]],
[anyone,"lord_intrigue_quest_complaint_stated", [
(store_random_in_range, ":random", -50, 50),
(store_add, ":score", "$g_talk_troop_effective_relation", ":random"),

(quest_get_slot, ":target_troop", "qst_intrigue_against_lord", slot_quest_target_troop),
(call_script, "script_troop_get_relation_with_troop", ":target_troop", "$g_talk_troop"),
(ge, ":score", reg0),

],
"Hmm... This is troubling to hear. Although I do not encourage my vassals to speak ill of each other, I value your opinion. Perhaps I should think twice about granting {s4} any further fiefs or offices...", "lord_pretalk",[
(quest_get_slot, ":target_troop", "qst_intrigue_against_lord", slot_quest_target_troop),
(call_script, "script_troop_change_relation_with_troop", "$g_talk_troop", ":target_troop", -10),
(call_script, "script_succeed_quest", "qst_intrigue_against_lord"),
]],
[anyone,"lord_intrigue_quest_complaint_stated", [
],
"Sew discord among my vassals, will you? With everything else going on, do you think I appreciate my samurai turning on each other like quarreling dogs? Let me ask you this -- did someone put you up this?", "intrigue_quest_state_complaint_failed",[
(call_script, "script_fail_quest", "qst_intrigue_against_lord"),
(call_script, "script_troop_change_relation_with_troop", "$g_talk_troop", "trp_player", -5),
]],
[anyone|plyr,"lord_talk", [
(check_quest_active, "qst_denounce_lord"),
(neg|check_quest_succeeded, "qst_denounce_lord"),
(neg|check_quest_failed, "qst_denounce_lord"),

(quest_slot_eq, "qst_denounce_lord", slot_quest_target_troop, "$g_talk_troop"),


(troop_get_slot, ":reputation_string", "$g_talk_troop", slot_lord_reputation_type),
(val_add, ":reputation_string", "str_lord_derogatory_default"),
(str_store_string, s4, ":reputation_string"),
],
"I want to tell you something -- we have had enough of your {s4} ways", "lord_denounce_1",[
]],
[anyone,"lord_denounce_1", [
],
"I'm sorry... What did you say?", "lord_denounce_2",[
]],
[anyone|plyr,"lord_denounce_2", [

(troop_get_slot, ":reputation_string", "$g_talk_troop", slot_lord_reputation_type),
(val_add, ":reputation_string", "str_lord_derogatory_result"),
(str_store_string, s4, ":reputation_string"),

],
"You heard me. You will {s4}", "lord_denounce_3",[
(call_script, "script_troop_change_relation_with_troop", "$g_talk_troop", "trp_player", -15),


(store_div, ":impact", "$g_talk_troop_relation", 10),
(val_add, ":impact", 1),
(val_max, ":impact", 1),
(val_mul, ":impact", -1),

#Change his respect level, slightly.  In the future game, there should be more sophisticated metrics for this
(try_for_range, ":other_lord", active_npcs_begin, active_npcs_end),
(neq, "$g_talk_troop", ":other_lord"),
(store_faction_of_troop, ":other_lord_faction",":other_lord"),
(eq, ":other_lord_faction", "$g_talk_troop_faction"),
(call_script, "script_troop_get_relation_with_troop", ":other_lord", "$g_talk_troop"),
(lt, reg0, 15),
(call_script, "script_troop_change_relation_with_troop", ":other_lord", "$g_talk_troop", ":impact"),
(try_end),



]],
[anyone|plyr,"lord_denounce_2", [
],
"Never mind. You must have misheard me.", "lord_pretalk",[
]],
[anyone,"lord_denounce_3", [
(ge, "$g_talk_troop_relation", 10),
##diplomacy start+
#The "this_or_next" is almost certainly a mistake, because it will always be true.  Correcting it.
#(this_or_next|neg|troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_quarrelsome),
(neg|troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_quarrelsome),
(neg|troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_martial),
],
"Why would you say such a thing? To insult me like this, in spite of our friendship -- how much crueler is a knife in my back from an erstwhile friends, than the sword of a sworn foe. I do not know what game you are playing, but I want no part of it. Go away. I do not want to look at you.", "close_window",[
(call_script, "script_succeed_quest", "qst_denounce_lord"),
]],
[anyone,"lord_denounce_3", [
(troop_slot_ge, "trp_player", slot_troop_renown, 300),
##diplomacy start+ Support additional personality types
(assign, reg0, 0),
(try_begin),
   (troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_none),
   (this_or_next|is_between, "$g_talk_troop", kings_begin, kings_end),
   (is_between, "$g_talk_troop", pretenders_begin, pretenders_end),
   (assign, reg0, 1),
(try_end),
(this_or_next|eq, reg0, 1),
(this_or_next|troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_ambitious),
##diplomacy end+
(this_or_next|troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_cunning),
(this_or_next|troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_upstanding),
(troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_goodnatured),
],
"Hmf. Really? Is that your opinion, or did one of my rivals put those words in your mouth? Never mind. I will not play your game. Go away, and take your intrigues with you.", "close_window",[
(call_script, "script_succeed_quest", "qst_denounce_lord"),
]],
[anyone,"lord_denounce_3", [
##diplomacy start+ Support additional personality types
(this_or_next|troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_conventional),
(this_or_next|troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_otherworldly),
(this_or_next|troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_moralist),
##diplomacy end+
(this_or_next|troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_martial),
(this_or_next|troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_cunning),
(this_or_next|troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_upstanding),
(troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_goodnatured),
],
"I will not have you shame me in public, {sir/my lady}. Retract your words, or meet me on the duelling ground.", "lord_denounce_4",[
]],
[anyone,"lord_denounce_3", [
],
##diplomacy start+ Change "knave" to vary with gender
"Is that so? Well, hear this -- you're a snake, and a {knave/strumpet}, and -- if you don't meet me on the duelling ground -- a coward. What say you to that? Do you retract your words, or shall we cross swords?", "lord_denounce_4",[
##diplomacy end+
]],
[anyone|plyr,"lord_denounce_4", [
],
"It would be a pleasure to fight you.", "lord_respond_to_insult_challenge_duel_confirm",[
]],
[anyone|plyr,"lord_denounce_4", [
],
"I spoke rashly. I retract my words.", "lord_denounce_retract",[
(call_script, "script_fail_quest", "qst_denounce_lord"),

]],
[anyone,"lord_denounce_retract", [
],
"I thought as much. Now, be gone from here.", "lord_pretalk",[
]],
[anyone|plyr,"lord_talk", [
(eq, "$g_comment_has_rejoinder", 1),
(assign, "$g_comment_has_rejoinder", 0),
(str_store_string, s9, "$g_rejoinder_to_last_comment"),
],
"{s9}", "lord_respond_to_insult",[

        (try_begin),
            (troop_get_type, ":is_female", "trp_player"),
            (eq, ":is_female", 1),
(unlock_achievement, ACHIEVEMENT_SASSY),
        (try_end),
]],
[anyone,"lord_pretalk", [
(lt, "$g_encountered_party_relation", 0),
(encountered_party_is_attacker),
],
"But enough talking - yield or fight!", "party_encounter_lord_hostile_attacker_2",[]],
[anyone,"lord_pretalk", [],
"Anything else?", "lord_talk",[]],
[anyone|plyr,"lord_talk",[
                      (check_quest_active, "qst_resolve_dispute"),
               (quest_get_slot, ":lord_1", "qst_resolve_dispute", slot_quest_target_troop),
               (quest_get_slot, ":lord_2", "qst_resolve_dispute", slot_quest_object_troop),

               (assign, ":other_lord", 0),
               (try_begin),
                  (eq, ":lord_1", "$g_talk_troop"),
                  (quest_slot_eq, "qst_resolve_dispute", slot_quest_target_state, 0),
                  (assign, "$g_other_lord", ":lord_2"),
                  (assign, ":other_lord", ":lord_2"),

               (else_try),
                  (eq, ":lord_2", "$g_talk_troop"),
                  (quest_slot_eq, "qst_resolve_dispute", slot_quest_object_state, 0),
                  (assign, "$g_other_lord", ":lord_1"),
                  (assign, ":other_lord", ":lord_1"),

               (try_end),
               (gt, ":other_lord", 0),
               (str_store_troop_name, s11, "$g_other_lord"),
                      ],
"I wish to address your quarrel with {s11}", "lord_quarrel_intervention_1",
[]],
[anyone|plyr,"lord_talk",[#(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 0),
                      (neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
               (encountered_party_is_attacker),
               (neg|is_between, "$g_talk_troop", pretenders_begin, pretenders_end),
               (neg|faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, "$g_talk_troop"),

                      ],
"Stay your hand! There is something I must say to you in private.", "lord_recruit_1_relation",
[]],
[anyone|plyr,"lord_talk",
[(check_quest_active, "qst_track_down_bandits"),
(neg|check_quest_succeeded, "qst_track_down_bandits"),
(neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 1),


], "I am hunting a group of bandits with the following description... Have you seen them?", "lord_bandit_information",[]],
[anyone,"lord_bandit_information", [
(call_script, "script_get_manhunt_information_to_s15", "qst_track_down_bandits"),
], "{s15}", "lord_pretalk",[]],
[anyone|plyr,"lord_talk",[#(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 0),
                      (eq, "$g_talk_troop_faction", "$players_kingdom"),
               (faction_slot_eq, "$players_kingdom", slot_faction_political_issue, 1),
                      ],
"Who do you think should be made the strategist of our clan?", "lord_internal_politics_cur_stance",
[]],
[anyone|plyr,"lord_talk",[#(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 0),
                      (eq, "$g_talk_troop_faction", "$players_kingdom"),
               (faction_get_slot, ":political_issue", "$players_kingdom", slot_faction_political_issue),
               (is_between, ":political_issue", centers_begin, centers_end),
               (str_store_party_name, s4, ":political_issue"),
                      ],
##diplomacy start+ fix grammatical error (change "whom" to "who")
"Who do you think should receive the fief of {s4}?", "lord_internal_politics_cur_stance",
##diplomacy end+
[]],
[anyone|plyr,"lord_talk",[
               ##diplomacy start+ This seemingly redundant condition is for a polygamy implementation
               (this_or_next|troop_slot_eq, "$g_talk_troop", slot_troop_spouse, "trp_player"),
               ##diplomacy end+
               (troop_slot_eq, "trp_player", slot_troop_spouse, "$g_talk_troop"),
               (troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_hero),
               (is_between, "$players_kingdom", kingdoms_begin, kingdoms_end),
               (neq, "$g_talk_troop_faction", "$players_kingdom"),
			   ##diplomacy start+
			   (assign, ":npc_homage", 0),
			   (try_begin),
				  (is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
				  (eq, "$player_has_homage", 1),
				  (assign, ":npc_homage", 1),
			   (try_end),
			   (this_or_next|eq, ":npc_homage", 1),
			   ##diplomacy end+
               (faction_slot_eq, "fac_player_supporters_faction", slot_faction_state, sfs_active),
#							(faction_slot_eq, "fac_player_supporters_faction", slot_faction_leader, "trp_player"),
            ##diplomacy start+ Guard against invalid leader
            (try_begin),
               (faction_slot_ge, "$g_talk_troop_faction", slot_faction_leader, 1),
            ##diplomacy end+
               (faction_get_slot, ":faction_leader", "$g_talk_troop_faction", slot_faction_leader),
               (str_store_troop_name, s4, ":faction_leader"),
            ##diplomacy start+ Alternative for invalid leader
            (else_try),
               (str_store_faction_name, s4, "$g_talk_troop_faction"),
            (try_end),
            ##diplomacy end+
               (str_store_faction_name, s5, "$players_kingdom"),
                                                                                           ],
##diplomacy start+ either gender PC can marry opposite-gender lords
"I need you to renounce your allegiance to {s4} and join the {s5} now, my {reg65?wife:husband}.", "lord_husband_auto_recruit",
##diplomacy end+
[]],
[anyone,"lord_husband_auto_recruit",
[
(is_between, "$g_encountered_party", centers_begin, centers_end),
(neg|party_slot_eq, "$g_encountered_party", slot_town_lord, "$g_talk_troop"),
##diplomacy start+ load relation text into s0
(call_script, "script_dplmc_print_player_spouse_says_my_husband_wife_to_s0", "$g_talk_troop", 0),
##diplomacy end+
],
##diplomacy start+ either gender PC can marry opposite-gender lords
"Ask me again when we are outside of these walls, {s0}.", "lord_pretalk",
##diplomacy end+
[]],
[anyone,"lord_husband_auto_recruit",
[
(is_between, "$g_encountered_party", centers_begin, centers_end),
(neg|party_slot_eq, "$g_encountered_party", slot_town_lord, "$g_talk_troop"),
##diplomacy start+ load relation text into s0
(call_script, "script_dplmc_print_player_spouse_says_my_husband_wife_to_s0", "$g_talk_troop", 0),
##diplomacy end+
],
##diplomacy start+ either gender PC can marry opposite-gender lords
"Ask me again when we are outside of these walls, {s0}.", "lord_pretalk",
##diplomacy end+
[]],
[anyone,"lord_husband_auto_recruit",[
	#Don't apply it to former comrades under arms
	#gekokujo 3.0 microfactions! include fort companions start
	#(this_or_next|neg|is_between, "$g_talk_troop", companions_begin, companions_end),
	(this_or_next|neg|is_between, "$g_talk_troop", companions_begin, fort_companions_end),
	#gekokujo 3.0 microfactions! include fort companions end
		(troop_slot_eq, "$g_talk_troop", slot_troop_playerparty_history, dplmc_pp_history_nonplayer_entry),
	(this_or_next|neg|is_between, "$g_talk_troop", pretenders_begin, pretenders_end),
		(troop_slot_eq, "$g_talk_troop", slot_troop_playerparty_history, dplmc_pp_history_nonplayer_entry),
	#Only apply reluctance when being recruited from an actual kingdom
	(is_between, "$g_talk_troop_faction", kingdoms_begin, kingdoms_end),
	#Other special cases
	(faction_get_slot, ":new_leader", "$players_kingdom", slot_faction_leader),
	(faction_get_slot, ":old_leader", "$g_talk_troop_faction", slot_faction_leader),
	(ge, ":new_leader", 0),
	(ge, ":old_leader", 0),
	(neq, ":old_leader", "trp_player"),
	#Don't apply if in an alliance
	(call_script, "script_dplmc_get_faction_truce_length_with_faction", "$g_talk_troop_faction", "$players_kingdom"),
	(lt, reg0, dplmc_treaty_alliance_days_expire + 1),
	#Certain personalities are more compliant than others
	(troop_get_slot, ":reputation", "$g_talk_troop", slot_lord_reputation_type),
	(neq, ":reputation", lrep_conventional),
	(neq, ":reputation", lrep_otherworldly),

	(call_script, "script_troop_get_relation_with_troop", "$g_talk_troop", ":old_leader"),
	(assign, ":old_score", reg0),

	(assign, ":new_score", "$g_talk_troop_effective_relation"),
	(try_begin),
		(this_or_next|eq, ":new_leader", "trp_player"),
			(eq, "$players_kingdom", "fac_player_supporters_faction"),
		(val_max, ":new_score", "$g_talk_troop_effective_relation"),
		(game_get_reduce_campaign_ai, ":reduce_campaign_ai"),
		(assign, reg0, 20),#required right to rule
		(try_begin),
			(eq, ":reduce_campaign_ai", 0),#hard: penalty for every point below 75, bonus for every point above
			(assign, reg0, 75),
		(else_try),
			(eq, ":reduce_campaign_ai", 1),#normal: penalty for every point below 50, bonus for every point above
			(assign, reg0, 50),
		(else_try),
			(eq, ":reduce_campaign_ai", 2),#easy: penalty for every point below 25, bonus for every point above
			(assign, reg0, 20),
		(try_end),
		(val_add, ":new_score", "$player_right_to_rule"),
		(val_sub, ":new_score", reg0),
	(else_try),
		(call_script, "script_troop_get_relation_with_troop", "$g_talk_troop", ":new_leader"),
		(gt, reg0, "$g_talk_troop_relation"),
		#Use new leader's relation if better than relation with player
		(assign, ":new_score", reg0),
		#Modify using persuasion score
		(store_skill_level, ":persuasion", "skl_persuasion", "trp_player"),
		(ge, ":persuasion", 1),
		(try_begin),
   			(ge, ":new_score", 0),
			(store_add, reg0, ":persuasion", 10),
			(val_mul, ":new_score", reg0),
			(val_div, ":new_score", 10),
		(else_try),
			(store_sub, reg0, 20, ":persuasion"),
			(val_mul, ":new_score", reg0),
			(val_div, ":new_score", 20),
		(try_end),
	(try_end),

	(try_begin),
		(troop_slot_eq, "$g_talk_troop", slot_troop_original_faction, "$players_kingdom"),
		(store_mul, reg0, ":new_score", 2),
		(val_add, ":new_score", 10),
		(val_max, ":new_score", reg0),
	(else_try),
		(troop_slot_eq, "$g_talk_troop", slot_troop_original_faction, "$g_talk_troop_faction"),
		(store_mul, reg0, ":old_score", 2),
		(val_add, ":old_score", 10),
		(val_max, ":old_score", reg0),
		(eq, ":reputation", lrep_upstanding),
		(store_add, reg0, ":old_score", 5),
		(val_mul, ":old_score", 3),
		(val_div, ":old_score", 2),
		(val_max, ":old_score", reg0),
	(try_end),

	#Refuse to switch
	(ge, ":old_score", ":new_score"),
	(try_begin),
		(ge, "$cheat_mode", 1),
		(assign, reg0, ":old_score"),
		(assign, reg1, ":new_score"),
		(display_message, "@{!} DEBUG - current kingdom score {reg0} vs player kingdom score {reg1}"),
	(try_end),
	(str_store_faction_name, s2, "$g_talk_troop_faction"),
#TODO: customize message by personality
], "I must remain loyal to {s14}. I am sorry.", "lord_pretalk",
[]],
[anyone,"lord_husband_auto_recruit",
[
##either gender PC can marry opposite-gender lords
#load relation text into s0
(call_script, "script_dplmc_print_player_spouse_says_my_husband_wife_to_s0", "$g_talk_troop", 0),
], "As you wish, {s0}.", "close_window",
##diplomacy end+
[
(assign, "$g_leave_encounter", 1),
(call_script, "script_change_troop_faction", "$g_talk_troop", "$players_kingdom"),

(try_begin), #Actually, perhaps do provocation rather than war
  (store_relation, ":relation", "$players_kingdom", "$g_talk_troop_faction"),
  (ge, ":relation", 0),

  (try_begin),
    (eq, "$cheat_mode", 1),
    (display_message, "str_lord_recruitment_provokes_home_faction"),
  (try_end),

  (call_script, "script_add_log_entry", logent_border_incident_troop_suborns_lord, "trp_player", -1, "$g_talk_troop","$g_talk_troop_faction"),
  (store_add, ":slot_provocation_days", "$players_kingdom", slot_faction_provocation_days_with_factions_begin),
  (val_sub, ":slot_provocation_days", kingdoms_begin),
  #gekokujo 3.0 provocation days increase start
  (faction_set_slot, "$g_talk_troop_faction", ":slot_provocation_days", 60),
  #(faction_set_slot, "$g_talk_troop_faction", ":slot_provocation_days", 30),
  #gekokujo 3.0 provocation days increase end

  (faction_get_slot, ":other_liege", "$g_talk_troop_faction", slot_faction_leader),
  (call_script, "script_troop_change_relation_with_troop", "trp_player", ":other_liege", -3),
(try_end),

(try_begin),
(faction_slot_eq, "$players_kingdom", slot_faction_leader, "trp_player"),
#gekokujo 3.0 reduced RTR rewards start
#(call_script, "script_change_player_right_to_rule", 5),
(call_script, "script_change_player_right_to_rule", 2),
#gekokujo 3.0 reduced RTR rewards end
(try_end),
]],
[anyone|plyr,"lord_talk",[#(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 0),
                      ##diplomacy start+ This seemingly redundant condition is for a polygamy implementation
                      (this_or_next|troop_slot_eq, "$g_talk_troop", slot_troop_spouse, "trp_player"),
                      ##diplomacy end+
                      (troop_slot_eq, "trp_player", slot_troop_spouse, "$g_talk_troop"),
                      ],
"There is a matter which I would like to discuss in private.", "lord_recruit_1_relation",
[]],
[anyone|plyr,"lord_talk",[#(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 0),
                      (neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
               (neg|encountered_party_is_attacker),
               (neg|is_between, "$g_talk_troop", pretenders_begin, pretenders_end),
               (neg|faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, "$g_talk_troop"),
                      (neg|troop_slot_eq, "trp_player", slot_troop_spouse, "$g_talk_troop"),
               ##diplomacy start+
 			   (neg|troop_slot_eq, "$g_talk_troop", slot_troop_spouse, "trp_player"),
               (call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", "$g_talk_troop_faction"),
               (lt, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
			   (call_script, "script_dplmc_get_troop_standing_in_faction", "$g_talk_troop", "$g_talk_troop_faction"),
               (lt, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
			   #This seemingly redundant condition is for a polygamy implementation
               (neg|troop_slot_eq, "$g_talk_troop", slot_troop_spouse, "trp_player"),
               ##diplomacy end+
               (neq, "$g_talk_troop_faction", "fac_player_supporters_faction"),
               #other requirements
                      ],
"There is something which I would like to discuss with to you in private.", "lord_recruit_1_relation",
[]],
[anyone|plyr,"lord_talk",[#(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 0),
                      (troop_slot_ge, "$g_talk_troop", slot_troop_intrigue_impatience, 1),
               (eq, "$cheat_mode", 1),

               #other requirements

                      ],
"CHEAT -- Reset lord decision seed and intrigue impatience", "lord_talk",
[
(troop_set_slot, "$g_talk_troop", slot_troop_intrigue_impatience, 0),
(store_random_in_range, ":random", 0, 9999),
(troop_set_slot, "$g_talk_troop", slot_troop_temp_decision_seed, ":random"),
]],
[anyone|plyr,"lord_talk",[(eq, "$cheat_mode", 1),
                      ],
"CHEAT -- Let's duel (insult)", "lord_respond_to_insult_challenge_duel",
[
]],
[anyone,"lord_respond_to_insult", [
(eq, "$g_last_comment_copied_to_s42", "str_comment_intro_female_sadistic_admiring"),
], "Hah! I admire a quick tongue. Perhaps some day I shall remove it, with tongs, to admire it at greater leisure, but today, at least, I shall salute your wit and courage.", "lord_pretalk", [
(call_script, "script_troop_change_relation_with_troop", "trp_player", "$g_talk_troop", 5),
(call_script, "script_change_troop_renown", "trp_player", 2),
]],
[anyone,"lord_respond_to_insult", [
(this_or_next|eq, "$g_last_comment_copied_to_s42", "str_comment_intro_female_pitiless_admiring"),
(this_or_next|eq, "$g_last_comment_copied_to_s42", "str_comment_intro_female_common_upstanding"),
(this_or_next|eq, "$g_last_comment_copied_to_s42", "str_comment_intro_female_noble_upstanding"),
(this_or_next|eq, "$g_last_comment_copied_to_s42", "str_comment_intro_female_common_martial"),
(eq, "$g_last_comment_copied_to_s42", "str_comment_intro_female_badtempered_admiring"),
##diplomacy start+
], "I meant no offense, {sir/madame}.", "lord_pretalk", [#madame to {sir/madame}
##diplomacy end+
(call_script, "script_troop_change_relation_with_troop", "trp_player", "$g_talk_troop", -2),
(call_script, "script_change_troop_renown", "trp_player", 2),
]],
[anyone,"lord_respond_to_insult", [
(troop_slot_eq, "$g_talk_troop", slot_troop_leaded_party, "$g_encountered_party"),
(store_party_size_wo_prisoners, ":lord_party_size", "$g_talk_troop_party"),
(store_party_size_wo_prisoners, ":player_party_size", "p_main_party"),
(val_mul, ":player_party_size", 3),
(val_div, ":player_party_size", 2),
##diplomacy start+
#Check perceived strength as well as raw numbers
(call_script, "script_dplmc_party_calculate_strength_in_terrain", "$g_encountered_party", -1, 0, 0),
(assign, ":lord_party_score", reg1),
(call_script, "script_dplmc_party_calculate_strength_in_terrain", "p_main_party", -1, 0, 0),
(assign, ":player_party_score", reg1),
(val_mul, ":player_party_score", 3),
(val_div, ":player_party_score", 2),

#Aggressive lords require less of an advantage to fight
(call_script, "script_dplmc_store_troop_personality_caution_level", "$g_talk_troop"),
(try_begin),
	(lt, reg0, 0),#Negative caution means aggressive
	(val_mul, ":lord_party_size", 5),
	(val_div, ":lord_party_size", 4),
	(val_mul, ":lord_party_score", 5),
	(val_div, ":lord_party_score", 4),
(try_end),
(this_or_next|gt, ":lord_party_score", ":player_party_score"),
##diplomacy end+
(gt, ":lord_party_size", ":player_party_size"),
(neq, "$players_kingdom",  "$g_talk_troop_faction"),
##diplomacy start+
#Make "no obligation to duel women..." line change depending on sexism settings.
(try_begin),
   (call_script, "script_cf_dplmc_faction_has_bias_against_gender", "$g_talk_troop_faction", 1),
   (assign, reg0, 1),
   (assign, reg1, 0),
(else_try),
   (neq, reg65, 0),
   (call_script, "script_cf_dplmc_faction_has_bias_against_gender", "$g_talk_troop_faction", 0),
   (assign, reg0, 0),
   (assign, reg1, 1),
(else_try),
   (assign, reg0, 0),
   (assign, reg1, 0),
(try_end),
#], "Are you trying to provoke me? Well, I would have you know that I am under no obligation to duel women, commoners, rebels, or brigands. I could#, however, order my men to seize you and horsewhip you. Would you like them to do that?", "lord_respond_to_insult_challenge_battle",
], "Are you trying to provoke me? Well, I would have you know that I am under no obligation to duel {reg0?women:{reg1?boys:fools}}, commoners, rebels, or brigands. I could, however, order my {reg1?{reg65?women:soldiers}:{reg65?soldiers:men}} to seize you and horsewhip you. Would you like them to do that?", "lord_respond_to_insult_challenge_battle",
##diplomacy end+
[
(call_script, "script_troop_change_relation_with_troop", "trp_player", "$g_talk_troop", -10),
(call_script, "script_change_troop_renown", "trp_player", 2),
]],
[anyone,"lord_respond_to_insult", [
##diplomacy start+
#Make "no obligation to duel women..." line change depending on sexism settings.
(try_begin),
   (call_script, "script_cf_dplmc_faction_has_bias_against_gender", "$g_talk_troop_faction", 1),
   (assign, reg0, 1),
   (assign, reg1, 0),
(else_try),
   (neq, reg65, 0),
   (call_script, "script_cf_dplmc_faction_has_bias_against_gender", "$g_talk_troop_faction", 0),
   (assign, reg0, 0),
   (assign, reg1, 1),
(else_try),
   (assign, reg0, 0),
   (assign, reg1, 0),
(try_end),
#], "Are you trying to provoke me? Well, I would have you know that I am under no obligation to duel women, commoners, rebels, or brigands. However#, in your case, I would be delighted to make an exception. Are you ready for a lesson in deference to your betters, {varlot/girl}?", "lord_respond#_to_insult_challenge_duel",
], "Are you trying to provoke me? Well, I would have you know that I am under no obligation to duel {reg0?women:{reg1?boys:fools}}, commoners, rebels, or brigands. However, in your case, I would be delighted to make an exception. Are you ready for a lesson in deference to your betters, {varlot/girl}?", "lord_respond_to_insult_challenge_duel",
##diplomacy end+
[
(call_script, "script_troop_change_relation_with_troop", "trp_player", "$g_talk_troop", -10),
(call_script, "script_change_troop_renown", "trp_player", 2),
]],
[anyone,"lord_respond_to_insult", [
##diplomacy start+
#Make "no obligation to duel women..." line change depending on sexism settings.
(try_begin),
   (call_script, "script_cf_dplmc_faction_has_bias_against_gender", "$g_talk_troop_faction", 1),
   (assign, reg0, 1),
   (assign, reg1, 0),
(else_try),
   (neq, reg65, 0),
   (call_script, "script_cf_dplmc_faction_has_bias_against_gender", "$g_talk_troop_faction", 0),
   (assign, reg0, 0),
   (assign, reg1, 1),
(else_try),
   (assign, reg0, 0),
   (assign, reg1, 0),
(try_end),
#], "Are you trying to provoke me? Well, I would have you know that I am under no obligation to duel women, commoners, rebels, or brigands. You are lucky that I am in a good mood, because I am perfectly within my rights to order my men to seize you and horsewhip you. Now begone -- I have had enough of you.", "close_window",
], "Are you trying to provoke me? Well, I would have you know that I am under no obligation to duel {reg0?women:{reg1?boys:fools}}, commoners, rebels, or brigands. You are lucky that I am in a good mood, because I am perfectly within my rights to order my {reg1?{reg65?women:soldiers}:{reg65?soldiers:men}} to seize you and horsewhip you. Now begone -- I have had enough of you.", "close_window",
##diplomacy end+
[
(call_script, "script_troop_change_relation_with_troop", "trp_player", "$g_talk_troop", -10),
(call_script, "script_change_troop_renown", "trp_player", 2),
(assign, "$g_leave_encounter", 1),
]],
[anyone|plyr,"lord_respond_to_insult_challenge_battle", [
], "I would like to see them try.", "lord_respond_to_insult_challenge_battle_confirm",
[
(call_script, "script_troop_change_relation_with_troop", "trp_player", "$g_talk_troop", -10),
(call_script, "script_change_troop_renown", "trp_player", 3),
]],
[anyone|plyr,"lord_respond_to_insult_challenge_battle", [
], "This is not worth the shedding of blood.", "close_window",
[
(assign, "$g_leave_encounter", 1),
]],
[anyone,"lord_respond_to_insult_challenge_battle_confirm", [
], "Enough of this insolence! Take {him/her} down!", "close_window",
[
(assign, "$g_private_battle_with_troop", "$g_talk_troop"),
(assign, "$cant_leave_encounter", 1),
(assign, "$encountered_party_friendly", 0),
(jump_to_menu, "mnu_simple_encounter"),
]],
[anyone|plyr,"lord_respond_to_insult_challenge_duel", [
], "I am ready to teach you one.", "lord_respond_to_insult_challenge_duel_confirm",
[
(str_store_troop_name_link, s13, "$g_talk_troop"),
(setup_quest_text, "qst_duel_avenge_insult"),
##diplomacy start+ use correct pronoun for gender
(call_script, "script_dplmc_store_troop_is_female_reg", "$g_talk_troop", 4),
##diplomacy end+
(str_store_string, s2, "str_you_intend_to_challenge_s13_to_force_him_to_retract_an_insult"),

(call_script, "script_start_quest", "qst_duel_avenge_insult", "$g_talk_troop"),
(quest_set_slot, "qst_duel_avenge_insult", slot_quest_target_troop, "$g_talk_troop"),

(call_script, "script_troop_change_relation_with_troop", "trp_player", "$g_talk_troop", -10),
]],
[anyone|plyr,"lord_respond_to_insult_challenge_duel", [
], "This is not worth the shedding of blood.", "close_window",
[
(assign, "$g_leave_encounter", 1),
]],
[anyone,"lord_respond_to_insult_challenge_duel_confirm", [
], "So be it. Defend yourself!", "close_window",
[
(call_script, "script_set_up_duel_with_troop", "$g_talk_troop"),
]],
[anyone,"lord_quarrel_intervention_1", [

##diplomacy start+
(assign, ":other_lord_is_female", 0),
(try_begin),
   (call_script, "script_cf_dplmc_troop_is_female", "$g_other_lord"),
   (assign, ":other_lord_is_female", 1),
(try_end),
(assign, reg3, ":other_lord_is_female"),
(assign, reg4, ":other_lord_is_female"),
##diplomacy end+
(str_store_string, s14, "str_general_quarrel"),
(assign, "$temp", "$g_other_lord"),

(assign, ":specific_quarrel_found", 0),
(store_add, ":log_entries_plus_one", "$num_log_entries", 1),
(try_for_range, ":log_entry_no", 1, ":log_entries_plus_one"),
(troop_slot_eq, "trp_log_array_entry_type", ":log_entry_no", logent_ruler_intervenes_in_quarrel),
(troop_slot_eq, "trp_log_array_troop_object", ":log_entry_no", "$temp"),
(troop_slot_eq, "trp_log_array_center_object", ":log_entry_no", "$g_talk_troop"),
(troop_slot_eq, "trp_log_array_faction_object", ":log_entry_no", "$g_talk_troop_faction"),

(call_script, "script_get_relevant_comment_for_log_entry", ":log_entry_no"),
(str_store_string, s14, reg0),
(assign, ":specific_quarrel_found", 1),
(else_try),
(troop_slot_eq, "trp_log_array_entry_type", ":log_entry_no", logent_lord_protests_marshall_appointment),
(troop_slot_eq, "trp_log_array_actor", ":log_entry_no", "$g_talk_troop"),
(troop_slot_eq, "trp_log_array_center_object", ":log_entry_no", "$temp"),
(call_script, "script_get_relevant_comment_for_log_entry", ":log_entry_no"),
(str_store_string, s14, reg0),
(assign, ":specific_quarrel_found", 1),
(else_try),
(troop_slot_eq, "trp_log_array_entry_type", ":log_entry_no", logent_lord_blames_defeat),
(troop_slot_eq, "trp_log_array_actor", ":log_entry_no", "$g_talk_troop"),
(troop_slot_eq, "trp_log_array_center_object", ":log_entry_no", "$temp"),
(call_script, "script_get_relevant_comment_for_log_entry", ":log_entry_no"),
(str_store_string, s14, reg0),
(assign, ":specific_quarrel_found", 1),
(else_try),
(troop_slot_eq, "trp_log_array_entry_type", ":log_entry_no", logent_troop_feels_cheated_by_troop_over_land),
(troop_slot_eq, "trp_log_array_actor", ":log_entry_no", "$g_talk_troop"),
(troop_slot_eq, "trp_log_array_troop_object", ":log_entry_no",  "$temp"),
(call_script, "script_get_relevant_comment_for_log_entry", ":log_entry_no"),
(str_store_string, s14, reg0),
(assign, ":specific_quarrel_found", 1),
(else_try),
(troop_slot_eq, "trp_log_array_entry_type", ":log_entry_no", logent_lords_quarrel_over_woman),
(troop_slot_eq, "trp_log_array_actor", ":log_entry_no", "$g_talk_troop"),
(troop_slot_eq, "trp_log_array_center_object", ":log_entry_no", "$temp"),
(call_script, "script_get_relevant_comment_for_log_entry", ":log_entry_no"),
##diplomacy start+ set gender for courted lady
(troop_get_slot, ":courted_lady", "trp_log_array_troop_object", ":log_entry_no"),
(assign, reg4, 0),
(try_begin),
   (call_script, "script_cf_dplmc_troop_is_female", ":courted_lady"),
	(assign, reg4, 1),
(try_end),
##diplomacy end+
(str_store_string, s14, reg0),
(assign, ":specific_quarrel_found", 1),
(else_try),
(troop_slot_eq, "trp_log_array_entry_type",  ":log_entry_no", logent_lords_quarrel_over_woman),
(troop_slot_eq, "trp_log_array_actor", ":log_entry_no", "$temp"),
(troop_slot_eq, "trp_log_array_center_object", ":log_entry_no", "$g_talk_troop"),
(call_script, "script_get_relevant_comment_for_log_entry", ":log_entry_no"),
##diplomacy start+ set gender for courted lady
(troop_get_slot, ":courted_lady", "trp_log_array_troop_object", ":log_entry_no"),
(assign, reg4, 0),
(try_begin),
   (call_script, "script_cf_dplmc_troop_is_female", ":courted_lady"),
	(assign, reg4, 1),
(try_end),
##diplomacy end+
(str_store_string, s14, reg0),
(assign, ":specific_quarrel_found", 1),
(try_end),

(try_begin),
(eq, ":specific_quarrel_found", 0),
(call_script, "script_troop_describes_quarrel_with_troop_to_s14", "$g_talk_troop", "$temp"),
(try_end),

],
"{s14}", "lord_quarrel_intervention_2",
[]],
[anyone|plyr,"lord_quarrel_intervention_2",[],
"Ah, well. It sounds like you're in the right, then.", "lord_quarrel_intervention_3a",
[
(call_script, "script_troop_change_relation_with_troop", "trp_player", "$g_other_lord", -20),
(call_script, "script_troop_change_relation_with_troop", "trp_player", "$g_talk_troop", 10),
(try_begin),
(faction_slot_eq, "fac_player_supporters_faction", slot_faction_leader, "trp_player"),
(call_script, "script_add_log_entry", logent_ruler_intervenes_in_quarrel, "trp_player",  "$g_other_lord", "$g_talk_troop", "fac_player_supporters_faction"),
(try_end),
(call_script, "script_end_quest", "qst_resolve_dispute"),

]],
[anyone|plyr,"lord_quarrel_intervention_2",[
(faction_slot_eq, "$players_kingdom", slot_faction_leader, "trp_player"),
],
"Whatever your differences, I want you to settle them.", "lord_quarrel_intervention_3b",
[]],
[anyone|plyr,"lord_quarrel_intervention_2",[
(neg|faction_slot_eq, "$players_kingdom", slot_faction_leader, "trp_player"),
],
"Could you not be convinced to settle your differences?", "lord_quarrel_intervention_3b",
[]],
[anyone|plyr,"lord_quarrel_intervention_2",[],
"On second thought, I want nothing to do with this.", "lord_pretalk",
[
(call_script, "script_abort_quest", "qst_resolve_dispute", 1),

]],
[anyone,"lord_quarrel_intervention_3a", [
], "I'm glad that you think so.", "lord_pretalk",
[]],
[anyone,"lord_quarrel_intervention_3b", [
(store_random_in_range, ":random", 0, 21),
(le, ":random", "$g_talk_troop_effective_relation"),
(str_store_troop_name, s11, "$g_other_lord"),

], "For the sake of our friendship, I defer to your judgment. I will try to make amends with {s11}.", "lord_quarrel_intervention_4",
[
(try_begin),
(quest_slot_eq, "qst_resolve_dispute", slot_quest_target_troop, "$g_talk_troop"),
(quest_set_slot, "qst_resolve_dispute", slot_quest_target_state, 1),
(else_try),
(quest_slot_eq, "qst_resolve_dispute", slot_quest_object_troop, "$g_talk_troop"),
(quest_set_slot, "qst_resolve_dispute", slot_quest_object_state, 1),
(try_end),
]],
[anyone,"lord_quarrel_intervention_3b", [
#fails reconciliation test
(str_store_troop_name, s11, "$g_other_lord"),
], "I will not reconcile with {s11}. I know my rights.", "lord_pretalk",
[
(call_script, "script_troop_change_relation_with_troop", "trp_player", "$g_talk_troop", -15),
(call_script, "script_troop_change_relation_with_troop", "trp_player", "$g_other_lord", 10),
(try_begin),
(eq, "$players_kingdom", "fac_player_supporters_faction"),
(call_script, "script_add_log_entry", logent_ruler_intervenes_in_quarrel, "trp_player",  "$g_talk_troop", "$g_other_lord", "fac_player_supporters_faction"),
(try_end),
(call_script, "script_end_quest", "qst_resolve_dispute"),
]],
[anyone,"lord_quarrel_intervention_4", [
(quest_slot_eq, "qst_resolve_dispute", slot_quest_object_state, 1),
(quest_slot_eq, "qst_resolve_dispute", slot_quest_target_state, 1),
], "Let it be as though our quarrel never occurred.", "lord_pretalk",
[
(call_script, "script_troop_change_relation_with_troop", "$g_talk_troop", "$g_other_lord", 20),
(call_script, "script_succeed_quest", "qst_resolve_dispute"),
(call_script, "script_end_quest", "qst_resolve_dispute"),
(call_script, "script_change_player_honor", 3),
(call_script, "script_change_troop_renown", "trp_player",  25),
(add_xp_as_reward, 500),

]],
[anyone,"lord_quarrel_intervention_4", [
(str_store_troop_name, s11, "$g_other_lord"),
##diplomacy start+ change "he" to {reg0?she:he}
(call_script, "script_dplmc_store_troop_is_female", "$g_other_lord"),
], "I suppose that you should speak to {s11}, and see if {reg0?she:he} will do the same for me.", "lord_pretalk",
##diplomacy end+
[
]],
[anyone,"lord_internal_politics_cur_stance", [
(troop_slot_eq, "$g_talk_troop", slot_troop_stance_on_faction_issue, "trp_player"),
],
"I had already made up my mind to support you.", "lord_internal_politics_cur_stance_plyr_response",
[
]],
[anyone,"lord_internal_politics_cur_stance", [
(troop_get_slot, ":player_choice", "trp_player", slot_troop_stance_on_faction_issue),
(troop_slot_eq, "$g_talk_troop", slot_troop_stance_on_faction_issue, ":player_choice"),
(gt, ":player_choice", -1),
(str_store_troop_name, s4, ":player_choice"),
##diplomacy start+ Add relation descriptions
(call_script, "script_dplmc_cap_troop_describes_troop_to_troop_s1", 0, "$g_talk_troop", ":player_choice", "trp_player"),
(str_store_string_reg, s4, s1),
##diplomacy end+
],
"I had already made up my mind to support {s4}.", "lord_internal_politics_cur_stance_plyr_response",
[
]],
[anyone,"lord_internal_politics_cur_stance", [
(call_script, "script_npc_decision_checklist_take_stand_on_issue", "$g_talk_troop"),
(eq, reg0, -1),
],
"I am unable to decide at this time", "lord_internal_politics_cur_stance_plyr_response",
[
]],
[anyone,"lord_internal_politics_cur_stance", [
],
"I support {s15}. {s10}", "lord_internal_politics_cur_stance_plyr_response",
[
(call_script, "script_npc_decision_checklist_take_stand_on_issue", "$g_talk_troop"),
(assign, ":supported_candidate", reg0),
(assign, ":explainer_string", reg1),
(troop_set_slot, "$g_talk_troop", slot_troop_stance_on_faction_issue, ":supported_candidate"),

(str_store_string, s10, ":explainer_string"),
(try_begin),
(eq, ":supported_candidate", "$g_talk_troop"),
(str_clear, s10),
(try_end),
(call_script, "script_troop_describes_troop_to_s15", "$g_talk_troop", ":supported_candidate"),

]],
[anyone|plyr,"lord_internal_politics_cur_stance_plyr_response", [
(troop_slot_eq, "trp_player", slot_troop_stance_on_faction_issue, -1),
(eq, "$player_has_homage", 1),
],
"Let me tell you whom I support...", "lord_internal_politics_plyr_choose_candidate",
[

]],
[anyone|plyr,"lord_internal_politics_cur_stance_plyr_response", [
(eq, "$cheat_mode", 1),
(eq, "$player_has_homage", 1),
],
"CHEAT -- Reset support", "lord_internal_politics_cur_stance_plyr_response",
[
(troop_set_slot, "trp_player", slot_troop_stance_on_faction_issue, -1),
]],
[anyone,"lord_internal_politics_plyr_choose_candidate", [
],
"Whom do you support?", "lord_internal_politics_plyr_choose_candidate_select",
[
]],
[anyone|plyr,"lord_internal_politics_plyr_choose_candidate_select", [
],
"I would like to nominate myself for that honor", "lord_internal_politics_pretalk",
[
(troop_set_slot, "trp_player", slot_troop_stance_on_faction_issue, "trp_player"),
]],
[anyone|plyr,"lord_internal_politics_plyr_choose_candidate_select", [
(troop_get_slot, ":spouse", "trp_player", slot_troop_spouse),
##diplomacy start+ This seemingly redundant condition is for a polygamy implementation
(this_or_next|troop_slot_eq, "$g_talk_troop", slot_troop_spouse, "trp_player"),
##diplomacy end+
(neq, ":spouse", "$g_talk_troop"),

##diplomacy start+
##OLD:
#(is_between, ":spouse", active_npcs_begin, active_npcs_end),
##NEW:
(is_between, ":spouse", heroes_begin, heroes_end),
##diplomacy end+
(troop_slot_eq, ":spouse", slot_troop_occupation, slto_kingdom_hero),
(store_faction_of_troop, ":spouse_faction", ":spouse"),
(eq, ":spouse_faction", "$players_kingdom"),
(str_store_troop_name, s4, ":spouse"),
##diplomacy start+ check gender of spouse
(call_script, "script_dplmc_store_troop_is_female", ":spouse"),
],
#diplomacy start+ player may be married to female lord
"I support my {reg0?wife:husband}, {s4}", "lord_internal_politics_pretalk",
#diplomacy end+
[
(troop_get_slot, ":spouse", "trp_player", slot_troop_spouse),

(troop_set_slot, "trp_player", slot_troop_stance_on_faction_issue, ":spouse"),
]],
[anyone|plyr,"lord_internal_politics_plyr_choose_candidate_select", [
(str_store_troop_name, s4, "$g_talk_troop"),
],
"I would support you, {s4}", "lord_internal_politics_support_acknowledge",
[
]],
[anyone|plyr,"lord_internal_politics_plyr_choose_candidate_select", [

(troop_get_slot, ":talk_troop_choice", "$g_talk_troop", slot_troop_stance_on_faction_issue),
##diplomacy start+ support promoted ladies
#(is_between, ":talk_troop_choice", active_npcs_begin, active_npcs_end),#OLD
(is_between, ":talk_troop_choice", heroes_begin, heroes_end),#NEW
##diplomacy end+
(str_store_troop_name, s4, ":talk_troop_choice"),
(neq, ":talk_troop_choice", "$g_talk_troop"),
],
"I would support your choice, {s4}", "lord_internal_politics_support_same_acknowledge",
[
]],
[anyone|plyr,"lord_internal_politics_plyr_choose_candidate_select", [
],
"Never mind", "lord_pretalk",
[
]],
[anyone,"lord_internal_politics_support_acknowledge", [
(troop_get_slot, ":supported_candidate", "$g_talk_troop", slot_troop_stance_on_faction_issue),
(neq, "$g_talk_troop", ":supported_candidate"),

],
"That is most gracious of you, but I do not seek the honor, and I decline your support.", "lord_pretalk",
[
(troop_set_slot, "trp_player", slot_troop_stance_on_faction_issue, -1),
]],
[anyone,"lord_internal_politics_support_acknowledge", [
(lt, "$g_talk_troop_effective_relation", -5),
##diplomacy start+
#more forgiving for affiliates
(call_script, "script_dplmc_is_affiliated_family_member", "$g_talk_troop"),
(this_or_next|lt, reg0, 1),
	(lt, "$g_talk_troop_effective_relation", -10),
#more forgiving for player spouse
(this_or_next|neg|troop_slot_eq, "$g_talk_troop", slot_troop_spouse, "trp_player"),#This seemingly redundant condition is for a polygamy implementation
(this_or_next|neg|troop_slot_eq, "trp_player", slot_troop_spouse, "$g_talk_troop"),
	(lt, "$g_talk_troop_effective_relation", -10),
#certain spouses are even more pliable
(this_or_next|neg|troop_slot_eq, "$g_talk_troop", slot_troop_spouse, "trp_player"),#This seemingly redundant condition is for a polygamy implementation
(this_or_next|neg|troop_slot_eq, "trp_player", slot_troop_spouse, "$g_talk_troop"),
	(this_or_next|neg|troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_conventional),
	(lt, "$g_talk_troop_effective_relation", -20),
##diplomacy end+
],
"I do not trust you, and I do not need your support.", "lord_pretalk",
[
(troop_set_slot, "trp_player", slot_troop_stance_on_faction_issue, -1),
]],
[anyone,"lord_internal_politics_support_acknowledge", [
],
"That is most gracious of you", "lord_pretalk",
[
(call_script, "script_troop_change_relation_with_troop", "trp_player", "$g_talk_troop", 3),
(troop_set_slot, "trp_player", slot_troop_stance_on_faction_issue, "$g_talk_troop"),
]],
[anyone,"lord_internal_politics_support_same_acknowledge", [
(lt, "$g_talk_troop_effective_relation", -5),
##diplomacy start+
#more forgiving for affiliates
(call_script, "script_dplmc_is_affiliated_family_member", "$g_talk_troop"),
(this_or_next|lt, reg0, 1),
	(lt, "$g_talk_troop_effective_relation", -10),
#more forgiving for player spouse
(this_or_next|neg|troop_slot_eq, "trp_player", slot_troop_spouse, "$g_talk_troop"),
	(lt, "$g_talk_troop_effective_relation", -10),
#certain spouses are even more pliable
(this_or_next|neg|troop_slot_eq, "trp_player", slot_troop_spouse, "$g_talk_troop"),
(this_or_next|neg|troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_conventional),
	(lt, "$g_talk_troop_effective_relation", -20),
#make gender correct
(troop_get_slot, ":talk_troop_choice", "$g_talk_troop", slot_troop_stance_on_faction_issue),
(call_script, "script_dplmc_store_troop_is_female_reg", ":talk_troop_choice", 3),
],#make gender correct
"You may tell {reg3?her:him} that yourself. I do not trust you, and I will have no part in any game which you are playing.", "lord_pretalk",
##diplomacy end+
[
(troop_set_slot, "trp_player", slot_troop_stance_on_faction_issue, -1),
]],
[anyone,"lord_internal_politics_support_same_acknowledge", [
(troop_get_slot, ":talk_troop_choice", "$g_talk_troop", slot_troop_stance_on_faction_issue),
(call_script, "script_troop_get_relation_with_troop", "trp_player", ":talk_troop_choice"),
(lt, reg0,  -5),
##diplomacy start+
(assign, ":relation", reg0),
##You can still support affiliates/your spouse as low as -10
(call_script, "script_dplmc_is_affiliated_family_member", ":talk_troop_choice"),
(this_or_next|lt, reg0, 1),
	(lt, ":relation", -10),
(this_or_next|neg|troop_slot_eq, "trp_player", slot_troop_spouse, ":talk_troop_choice"),
	(lt, ":relation", -10),
(str_store_troop_name, s4, ":talk_troop_choice"),#unchanged line
#make gender correct
(call_script, "script_dplmc_store_troop_is_female_reg", ":talk_troop_choice", 3),
##diplomacy end+
],
##diplomacy start+ make gender correct
"Given your relation with {s4}, I do not think that {reg3?she:he} would welcome your support.", "lord_pretalk",
##diplomacy end+
[
(troop_set_slot, "trp_player", slot_troop_stance_on_faction_issue, -1),
]],
[anyone,"lord_internal_politics_support_same_acknowledge", [
(troop_get_slot, ":talk_troop_choice", "$g_talk_troop", slot_troop_stance_on_faction_issue),
(str_store_troop_name, s4, ":talk_troop_choice"),
##diplomacy start+ make gender correct
(call_script, "script_dplmc_store_troop_is_female_reg", ":talk_troop_choice", 3),
##diplomacy end+
],
##diplomacy start+ make gender correct
"I will tell {s4}. {reg3?She:He} will no doubt be grateful for your support.", "lord_pretalk",
##diplomacy end+
[
(troop_get_slot, ":talk_troop_choice", "$g_talk_troop", slot_troop_stance_on_faction_issue),
(call_script, "script_troop_change_relation_with_troop", "trp_player", ":talk_troop_choice", 2),
(call_script, "script_troop_change_relation_with_troop", "trp_player", "$g_talk_troop", 1),
(troop_set_slot, "trp_player", slot_troop_stance_on_faction_issue, ":talk_troop_choice"),

]],
[anyone|plyr|repeat_for_troops,"lord_internal_politics_plyr_choose_candidate_select", [
(store_repeat_object, ":candidate"),
(eq, 1, 0),
(troop_slot_eq, ":candidate", slot_troop_occupation, slto_kingdom_hero),
(store_faction_of_troop, ":candidate_faction", ":candidate"),
(eq, ":candidate_faction", "$players_kingdom"),
(neg|troop_slot_eq, "trp_player", slot_troop_spouse, ":candidate"),
(str_store_troop_name, s4, ":candidate"),
],
"I support {s4}", "lord_internal_politics_pretalk",
[
(store_repeat_object, ":candidate"),
(troop_set_slot, "trp_player", slot_troop_stance_on_faction_issue, ":candidate"),
]],
[anyone,"lord_internal_politics_pretalk", [
],
"Ah. Most interesting.", "lord_internal_politics_cur_stance_plyr_response",
[
]],
[anyone|plyr,"lord_internal_politics_cur_stance_plyr_response", [
(eq, "$player_has_homage" ,1),
(neg|troop_slot_eq, "$g_talk_troop", slot_troop_stance_on_faction_issue, "$g_talk_troop"),
(neg|troop_slot_ge, "trp_player", slot_troop_stance_on_faction_issue, active_npcs_begin),
(neg|troop_slot_eq, "$g_talk_troop", slot_troop_stance_on_faction_issue, "trp_player"),
],
"Can I convince you to support me instead?", "lord_internal_politics_plyr_request_support",
[
]],
[anyone|plyr,"lord_internal_politics_cur_stance_plyr_response", [
(this_or_next|faction_slot_eq, "$players_kingdom", slot_faction_leader, "trp_player"),
(eq, "$player_has_homage" ,1),
(neg|troop_slot_eq, "$g_talk_troop", slot_troop_stance_on_faction_issue, "$g_talk_troop"),
(neg|troop_slot_ge, "trp_player", slot_troop_stance_on_faction_issue, active_npcs_begin),
(troop_get_slot, ":player_choice", "trp_player", slot_troop_stance_on_faction_issue),
(neg|troop_slot_eq, "$g_talk_troop", slot_troop_stance_on_faction_issue, ":player_choice"),
#(neg|troop_slot_eq, "$g_talk_troop", slot_troop_stance_on_faction_issue, "trp_player"),
],
"Can I convince you to support someone else?", "dplmc_lord_internal_politics_plyr_request_support_1",
[
]],
[anyone|plyr,"lord_internal_politics_cur_stance_plyr_response", [
(this_or_next|faction_slot_eq, "$players_kingdom", slot_faction_leader, "trp_player"),
   (eq, "$player_has_homage" ,1),
(neg|troop_slot_eq, "$g_talk_troop", slot_troop_stance_on_faction_issue, "$g_talk_troop"),
(troop_get_slot, ":player_pick", "trp_player", slot_troop_stance_on_faction_issue),
(neg|troop_slot_eq, "$g_talk_troop", slot_troop_stance_on_faction_issue, ":player_pick"),
(is_between, ":player_pick", heroes_begin, heroes_end),
(troop_slot_eq, ":player_pick", slot_troop_occupation, slto_kingdom_hero),
(str_store_troop_name, s4, ":player_pick"),
],
"Can I convince you to support {s4}?", "dplmc_lord_internal_politics_plyr_request_support_2",
[
	#Assign it to variable instead of just reading it, since another conversation
	#path allows the player to proffer a lord without having yet committed to any
	#option.
	(troop_get_slot, "$lord_selected", "trp_player", slot_troop_stance_on_faction_issue),
]],
[anyone,"lord_internal_politics_support_same_acknowledge", [
#fail if player's relation with suggested lord is too low
(call_script, "script_troop_get_relation_with_troop", "trp_player", "$lord_selected"),
(lt, reg0,  -5),
(call_script, "script_dplmc_is_affiliated_family_member", "$g_talk_troop"),
(lt, reg0, 1),
(str_store_troop_name, s4, "$lord_selected"),
(assign, reg3, 0),
(try_begin),
	(call_script, "script_cf_dplmc_troop_is_female", "$lord_selected"),
	(assign, reg3, 1),
(try_end),
],
"Given your relation with {s4}, I do not think that {reg3?she:he} would welcome your support.", "lord_pretalk",
[
(troop_set_slot, "trp_player", slot_troop_stance_on_faction_issue, -1),
]],
[anyone|plyr,"lord_internal_politics_cur_stance_plyr_response", [
],
"Anyway, enough of politics for the time being.", "lord_pretalk",
[
]],
[anyone,"lord_internal_politics_plyr_request_support", [
(troop_slot_ge, "trp_player", slot_troop_controversy, 25),
(this_or_next|faction_slot_eq, "$players_kingdom", slot_faction_political_issue, 1),
(troop_slot_ge, "trp_player", slot_troop_controversy, 50),
],
"You have engendered too much controversy to be a viable candidate right now. I would advise you to wait a little while before seeking any further honors for yourself.", "lord_pretalk",
[
]],
[anyone,"lord_internal_politics_plyr_request_support", [
(troop_get_slot, ":current_candidate", "$g_talk_troop", slot_troop_stance_on_faction_issue),
(gt, ":current_candidate", 0),
(str_store_troop_name, s4, ":current_candidate"),
(call_script, "script_troop_get_relation_with_troop", "$g_talk_troop", ":current_candidate"),
(ge, reg0, "$g_talk_troop_effective_relation"),
##diplomacy start+ don't talk about "straining the relationship" if the other lord
#actually supports the player!
(troop_get_slot, reg0, ":current_candidate", slot_troop_stance_on_faction_issue),
(neq, reg0, "trp_player"),
##diplomacy end+
],
"I am sorry. I would not wish to strain my relationship with {s4}", "lord_pretalk",
[
]],
[anyone,"lord_internal_politics_plyr_request_support", [
(faction_get_slot, ":faction_issue", "$players_kingdom", slot_faction_political_issue),
(is_between, ":faction_issue", centers_begin, centers_end),
(troop_get_slot, ":player_renown", "trp_player", slot_troop_renown),
##diplomacy start+
(try_begin),
	#prejudice mode: high
	(lt, "$g_disable_condescending_comments", 0),
	(neq, reg65, "$character_gender"),

	(call_script, "script_cf_dplmc_faction_has_bias_against_gender", "$g_talk_troop_faction", "$character_gender"),

	(neg|troop_slot_ge, "$g_talk_troop", slot_lord_reputation_type, lrep_roguish),#non-noble or kingdom lady
	(neg|troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_goodnatured),
	(neg|troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_cunning),
	#gekokujo 3.0 microfactions! include fort companions start
	#(neg|is_between, "$g_talk_troop", companions_begin, companions_end),
	(neg|is_between, "$g_talk_troop", companions_begin, fort_companions_end),
	#gekokujo 3.0 microfactions! include fort companions end
	(val_div, ":player_renown", 2),
(try_end),
##diplomacy end+
(assign, ":total_faction_renown", ":player_renown"),

(try_for_range, ":active_npc", active_npcs_begin, active_npcs_end),
(store_faction_of_troop, ":active_npc_faction", ":active_npc"),
(eq, ":active_npc_faction", "$players_kingdom"),

(troop_get_slot, ":renown", ":active_npc", slot_troop_renown),
(val_add, ":total_faction_renown", ":renown"),
(try_end),

(assign, ":total_faction_center_value", 0),
(assign, ":center_points_held_by_player", 0),
(try_for_range, ":center", centers_begin, centers_end),
(store_faction_of_party, ":center_faction", ":center"),
(eq, ":center_faction", "$players_kingdom"),

(assign, ":center_value", 1),
(try_begin),
   (is_between, ":center", towns_begin, towns_end),
   (assign, ":center_value", 2),
(try_end),

(val_add, ":total_faction_center_value", ":center_value"),

(party_slot_eq, ":center", slot_town_lord, "trp_player"),
(val_add, ":center_points_held_by_player", ":center_value"),
(try_end),
(val_max, ":total_faction_center_value", 1),
(val_max, ":center_points_held_by_player", 1),

(store_div, ":average_renown_per_center_point", ":total_faction_renown", ":total_faction_center_value"),
(store_div, ":player_renown_per_center_point", ":player_renown", ":center_points_held_by_player"),

(store_mul, ":threshhold", ":average_renown_per_center_point", 3),
(val_div, ":threshhold", 4),
(lt, ":player_renown_per_center_point", ":threshhold"),

],
"You have already been well-rewarded with fiefs appropriate to your accomplishments, I would say.", "lord_pretalk",
[
]],
[anyone,"lord_internal_politics_plyr_request_support", [
(faction_slot_eq, "$players_kingdom", slot_faction_political_issue, 1),
(troop_get_slot, ":player_renown", "trp_player", slot_troop_renown),
##diplomacy start+
(try_begin),
	#prejudice mode: high
	(lt, "$g_disable_condescending_comments", 0),
	(neq, reg65, "$character_gender"),
	(neg|troop_slot_ge, "$g_talk_troop", slot_lord_reputation_type, lrep_roguish),#non-noble or kingdom lady
	(neg|troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_goodnatured),
	(neg|troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_cunning),
	#gekokujo 3.0 microfactions! include fort companions start
	#(neg|is_between, "$g_talk_troop", companions_begin, companions_end),
	(neg|is_between, "$g_talk_troop", companions_begin, fort_companions_end),
	#gekokujo 3.0 microfactions! include fort companions end
	(call_script, "script_cf_dplmc_faction_has_bias_against_gender", "$g_talk_troop_faction", "$character_gender"),
	(val_div, ":player_renown", 2),
(try_end),
##diplomacy end+
(lt, ":player_renown", 400),
],
"I think you would need to prove yourself further before you are eligible for that position.", "lord_pretalk",
[
]],
[anyone,"lord_internal_politics_plyr_request_support", [
(lt, "$g_talk_troop_effective_relation", 10),
],
"Hmm... That is too much to ask, given the state of our relationship. ", "lord_pretalk",
[
]],
[anyone,"lord_internal_politics_plyr_request_support", [
],
"I would support you with pleasure. ", "lord_pretalk",
[
(troop_set_slot, "$g_talk_troop", slot_troop_stance_on_faction_issue, "trp_player"),
]],
[anyone,"lord_internal_politics_plyr_request_support", [
],
"{!}[Placeholder - sorry, not yet]", "lord_pretalk",
[
]],
[anyone,"lord_recruit_1_relation", [
(troop_slot_ge, "$g_talk_troop", slot_troop_intrigue_impatience, 100),
],
"I am a bit weary of talking politics. Perhaps at a later date", "lord_pretalk",
[
(troop_get_slot, reg3, "$g_talk_troop", slot_troop_intrigue_impatience),
(try_begin),
(eq, "$cheat_mode", 1),
(display_message, "str_intrigue_impatience=_reg3_must_be_less_than_100"),
(try_end),
]],
[anyone,"lord_recruit_1_relation", [ #can't use the nearby scripts, because it would include the player party
(assign, ":continue", 1),
(try_begin),
(call_script, "script_cf_troop_can_intrigue", "$g_talk_troop", 1),
(assign, ":continue", 0),
(try_end),

(eq, ":continue", 1),

(str_store_string, s12, "str_youll_have_to_speak_to_me_at_some_other_time_then"),
(try_begin),
(lt,"$g_encountered_party_relation",0),
(encountered_party_is_attacker),
(str_store_string, s12, "str_this_is_no_time_for_words"),
(try_end),
(try_begin),
(eq, "$cheat_mode", 1),
(display_message, "str_lord_not_alone"),
(try_end),
],
"{s12}", "lord_pretalk",[]],
[anyone,"lord_recruit_1_relation", [

(is_between, "$supported_pretender", pretenders_begin, pretenders_end),
(troop_slot_eq, "$supported_pretender", slot_troop_original_faction, "$g_talk_troop_faction"),
##diplomacy start+
##OLD:
#(troop_get_type, reg3, "$supported_pretender"),
##NEW:
(assign, reg3, 0),
(try_begin),
	(call_script, "script_cf_dplmc_troop_is_female", "$supported_pretender"),
	(assign, reg3, 1),
(try_end),
##diplomacy end+
(str_store_troop_name, s16, "$supported_pretender"),
(eq, "$skip_lord_assumes_argument", 0),

],
"You have raised the standard of rebellion on behalf of {s16}. Have you come to plead {reg3?her:his} case?", "lord_recruit_pretender",[
]],
[anyone|plyr,"lord_recruit_pretender", [
],
"I have", "lord_recruit_3_dilemma_1",[
(troop_set_slot, "$g_talk_troop", slot_lord_recruitment_candidate, "$supported_pretender"),
]],
[anyone|plyr,"lord_recruit_pretender", [
],
"No, that's not it. There's another issue I wish to discuss.", "lord_recruit_1_relation",[
(assign, "$skip_lord_assumes_argument", 1),
]],
[anyone,"lord_recruit_1_relation",
[
(try_begin),
(troop_slot_eq, "trp_player", slot_troop_spouse, "$g_talk_troop"),

(assign, ":willingness_to_intrigue", 20),

(str_store_string, s13, "str_of_course_my_wife"),
(str_store_string, s14, "str_perhaps_not_our_marriage_has_become_a_bit_strained_dont_you_think"),
(str_store_string, s15, "str_why_is_that_my_wife_actually_our_marriage_has_become_such_that_i_prefer_to_have_a_witness_for_all_of_our_converations"),
(else_try),
(troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_quarrelsome),

(assign, ":willingness_to_intrigue", 6),

(str_store_string, s13, "str_all_right_then_what_do_you_have_to_say_out_with_it"),
(str_store_string, s14, "str_bah__im_in_no_mood_for_whispering_in_the_corner"),
(str_store_string, s15, "str_bah_i_dont_like_you_that_much_im_not_going_to_go_plot_with_you_in_some_corner"),
(else_try),
(troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_debauched),
(assign, ":willingness_to_intrigue", 8),

(str_store_string, s13, "str_well__now_what_do_you_have_to_propose"),
(str_store_string, s14, "str_trying_our_hand_at_intrigue_are_we_i_think_not"),
(str_store_string, s15, "str_hah_i_trust_you_as_a_i_would_a_serpent_i_think_not"),
(else_try),
##diplomacy start+ add support for lady personalities
(this_or_next|troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_moralist),
##diplomacy end+
(troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_upstanding),
(assign, ":willingness_to_intrigue", -10),

(str_store_string, s13, "str_i_do_not_like_to_conduct_my_business_in_the_shadows_but_sometimes_it_must_be_done_what_do_you_have_to_say"),
(str_store_string, s14, "str_i_would_prefer_to_conduct_our_affairs_out_in_the_open"),
(str_store_string, s15, "str_do_not_take_this_amiss_but_with_you_i_would_prefer_to_conduct_our_affairs_out_in_the_open"),
(else_try),
##diplomacy start+ add support for lady personalities
(this_or_next|troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_ambitious),
##diplomacy end+
(troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_cunning),
(assign, ":willingness_to_intrigue", 4),

(str_store_string, s13, "str_hmm_you_have_piqued_my_interest_what_do_you_have_to_say"),
(str_store_string, s14, "str_em_lets_keep_our_affairs_out_in_the_open_for_the_time_being"),
(str_store_string, s15, "str_em_lets_keep_our_affairs_out_in_the_open_for_the_time_being"),
(else_try),
(troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_selfrighteous),
(assign, ":willingness_to_intrigue", 0),

(str_store_string, s13, "str_thats_sensible__the_world_is_full_of_churls_who_poke_their_noses_into_their_betters_business_now_tell_me_what_it_is_that_you_have_to_say"),
(str_store_string, s14, "str_what_do_you_take_me_for_a_plotter"),
(str_store_string, s15, "str_hah_i_trust_you_as_a_i_would_a_serpent_i_think_not"),
(else_try),
(troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_goodnatured),
(assign, ":willingness_to_intrigue", -10),

(str_store_string, s13, "str_well_i_normally_like_to_keep_things_out_in_the_open_but_im_sure_someone_like_you_would_not_want_to_talk_in_private_unless_heshe_had_a_good_reason_what_is_it"),
(str_store_string, s14, "str_surely_we_can_discuss_whatever_you_want_to_discuss_out_here_in_the_open_cant_we"),
(str_store_string, s15, "str_surely_we_can_discuss_whatever_you_want_to_discuss_out_here_in_the_open_cant_we"),
(else_try),
(troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_martial),
(assign, ":willingness_to_intrigue", -5),

(str_store_string, s13, "str_im_a_simple__man_not_one_for_intrigue_but_id_guess_that_you_have_something_worthwhile_to_say_what_is_it"),
(str_store_string, s14, "str_forgive_me_but_im_not_one_for_going_off_in_corners_to_plot"),
(str_store_string, s15, "str_please_do_not_take_this_amiss_but_i_do_not_trust_you"),
(else_try),
(troop_slot_ge, "$g_talk_troop", slot_lord_reputation_type, lrep_roguish),
(assign, ":willingness_to_intrigue", 10),

(str_store_string, s13, "str_certainly_playername_what_is_it"),
(str_store_string, s14, "str_forgive_me_but_id_prefer_to_keep_our_conversations_in_the_open"),
(str_store_string, s15, "str_please_do_not_take_this_amiss_but_im_not_sure_you_and_i_are_still_on_those_terms"),
(try_end),

(assign, ":continue", 0),
(store_skill_level, ":persuasion", "skl_persuasion", "trp_player"),

(try_begin),
(lt, "$g_talk_troop_relation", -5),
(try_begin),
  (eq, "$cheat_mode", 1),
  (display_message, "str_persuasion__relation_less_than_5"),
(try_end),
(str_store_string, s12, "str_s15"),
(else_try),
 (store_add, ":score", ":persuasion", "$g_talk_troop_relation"),
(val_add, ":score", ":willingness_to_intrigue"),
##diplomacy start+
#write troop gender into reg3 to make some lines gender-correct ("simple man" has been changed to "simple {reg3?woman:man}")
(assign, reg3, reg65),
##diplomacy end+
(game_get_reduce_campaign_ai, ":reduce_campaign_ai"),
(try_begin),
  (eq, ":reduce_campaign_ai", 0), #hard
  (val_sub, ":score", 5),
(else_try),
  (eq, ":reduce_campaign_ai", 1), #medium
(else_try),
  (eq, ":reduce_campaign_ai", 2), #easy
   (val_add, ":score", 5),
  (try_end),

(lt, ":score", 10),

(str_store_string, s12, "str_s14"),
(try_begin),
  (eq, "$cheat_mode", 1),
  (display_message, "str_persuasion__2__lord_reputation_modifier__relation_less_than_10"),
(try_end),

(str_store_string, s12, "str_s14"),
(else_try),
(str_store_string, s12, "str_s13"),
(assign, ":continue", 1),
(try_end),
##diplomacy start+ affiliated family members will conspire if relation >= 0
(try_begin),
(eq, ":continue", 0),
(call_script, "script_dplmc_is_affiliated_family_member", "$g_talk_troop"),
(ge, reg0, 1),
(ge, "$g_talk_troop_relation", 0),
(assign, reg3, reg65),#write troop gender into reg3 for "simple {reg3?woman:man}"
(str_store_string, s12, "str_s13"),
(assign, ":continue", 1),
(try_begin),
   (ge, "$cheat_mode", 1),
   (display_message, "@{!} DEBUG -- affiliated family member, overriding logic to continue"),
(try_end),
(try_end),
##diplomacy end+
(eq, ":continue", 0),
],
"{s12}", "lord_pretalk",[]],
[anyone,"lord_recruit_1_relation", [],
"{s12}", "lord_recruit_2",[]],
[anyone|plyr,"lord_recruit_2", [
],
"What do you think, in general terms, about kings, lords, and politics?", "lord_recruit_2_philosophy",[
]],
[anyone|plyr,"lord_recruit_2", [
##diplomacy start+
##OLD:
#(troop_slot_eq, "$g_talk_troop", slot_troop_spouse, "trp_player"),
#(neq, "$players_kingdom", "fac_player_supporters_faction"),
#(troop_get_type, ":type", "$g_talk_troop"),
#(eq, ":type", 0),
#(faction_get_slot, ":faction_leader", "$g_encountered_party_faction", slot_faction_leader),
#(str_store_troop_name, s11, ":faction_leader"),
##NEW:
#Verify player is not faction leader
(call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", "$players_kingdom"),
(lt, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
#Asymmetrical spouse check
(this_or_next|is_between, "$g_talk_troop", heroes_begin, heroes_end),
   (troop_slot_eq, "trp_player", slot_troop_spouse, "$g_talk_troop"),
(this_or_next|troop_slot_eq, "$g_talk_troop", slot_troop_spouse, "trp_player"),
   (troop_slot_eq, "$g_talk_troop", slot_troop_spouse, "trp_player"),
(neq, "$players_kingdom", "fac_player_supporters_faction"),
(call_script, "script_dplmc_store_troop_is_female", "$g_talk_troop"),
(assign, reg65, reg0),
(assign, ":type", reg65),
#players of either gender can marry opposite-gender lords
(this_or_next|troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_hero),
(this_or_next|is_between, "$g_talk_troop", active_npcs_begin, active_npcs_end),
	(eq, ":type", 0),
(faction_get_slot, ":faction_leader", "$g_encountered_party_faction", slot_faction_leader),
(str_store_troop_name, s11, ":faction_leader"),
##diplomacy end+
],
##diplomacy start+ players of either gender can marry opposite-gender lords (also you->your)
"My {reg65?wife:husband}, I believe that you should rethink your allegiance to {s11}", "lord_spouse_leave_faction",[
##diplomacy end+
]],
[anyone,"lord_spouse_leave_faction", [
(faction_get_slot, ":faction_liege", "$g_talk_troop_faction", slot_faction_leader),
(call_script, "script_troop_get_relation_with_troop", "$g_talk_troop", ":faction_liege"),
(gt, reg0, 25),
(str_store_troop_name, s9, ":faction_liege"),
],
"{s9} has always been a good lord to me, but I will hear you out. What do you suggest we do?", "lord_spouse_leave_faction_2",[]],
[anyone,"lord_spouse_leave_faction", [
(faction_get_slot, ":faction_liege", "$g_talk_troop_faction", slot_faction_leader),
(call_script, "script_troop_get_relation_with_troop", "$g_talk_troop", ":faction_liege"),
(gt, reg0, -5),
(str_store_troop_name, s9, ":faction_liege"),
],
"I see no particular reason to abandon {s9}, but I will heed your advice. What do you suggest we do?", "lord_spouse_leave_faction_2",[]],
[anyone,"lord_spouse_leave_faction", [
(faction_get_slot, ":faction_liege", "$g_talk_troop_faction", slot_faction_leader),
(call_script, "script_troop_get_relation_with_troop", "$g_talk_troop", ":faction_liege"),
(str_store_troop_name, s9, ":faction_liege"),
],
"Yes -- as a great lord, {s9} is a great disappointment. What do you suggest we do?", "lord_spouse_leave_faction_2",[]],
[anyone|plyr,"lord_spouse_leave_faction_2", [
##diplomacy start+ use culturally-appropriate term, and check gender of spouse
(try_begin),
	(eq, reg65, 1),
	(call_script, "script_dplmc_print_cultural_word_to_sreg", "$g_talk_troop", DPLMC_CULTURAL_TERM_KING_FEMALE, 1),
(else_try),
	(call_script, "script_dplmc_print_cultural_word_to_sreg", "$g_talk_troop", DPLMC_CULTURAL_TERM_KING, 1),
(try_end),
],
#either gender PC can marry opposite-gender lords
"I believe you should be {s1}, my {reg65?wife:husband}!", "lord_spouse_leave_faction_husband_king",[]],
[anyone|plyr,"lord_spouse_leave_faction_2", [
#diplomacy start+ either gender PC can marry opposite-gender lords;
#also use culturally-appropriate word for "king/queen"
(try_begin),
	(eq, 1, "$character_gender"),
	(call_script, "script_dplmc_print_cultural_word_to_sreg", "$g_talk_troop", DPLMC_CULTURAL_TERM_KING_FEMALE, 0),
(else_try),
	(call_script, "script_dplmc_print_cultural_word_to_sreg", "$g_talk_troop", DPLMC_CULTURAL_TERM_KING, 0),
(try_end),
],
"I am the rightful {s0} of Japan", "lord_spouse_leave_faction_proclaim_queen",[]],
[anyone|plyr,"lord_spouse_leave_faction_2", [
],
"Never mind", "lord_pretalk",[]],
[anyone,"lord_spouse_leave_faction_proclaim_queen", [
   (this_or_next|troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_moralist),#for promoted ladies
   (this_or_next|troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_upstanding),
      (troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_martial),

   (store_skill_level, ":persuasion_skill", "skl_persuasion", "trp_player"),

   (faction_get_slot, ":faction_liege", "$g_talk_troop_faction", slot_faction_leader),
   (call_script, "script_troop_get_relation_with_troop", "$g_talk_troop", ":faction_liege"),

   (game_get_reduce_campaign_ai, ":reduce_campaign_ai"),
   (try_begin),
      (eq, ":reduce_campaign_ai", 0),#hard, fail if relation above -10
	  (val_add, reg0, 10),
   (else_try),
      (eq, ":reduce_campaign_ai", 1),#normal, fail if relation above 0
   (else_try),
      (eq, ":reduce_campaign_ai", 2),#easy, fail if relation above 10
	  (val_sub, reg0, 10),
   (try_end),

   #Must beat player's persuasion
   (ge, reg0, ":persuasion_skill"),

   #Store liege name and gender
   (str_store_troop_name, s11, ":faction_liege"),
   (call_script, "script_dplmc_store_troop_is_female", ":faction_liege"),
], "I swore an oath to serve {s11}, and {reg0?she:he} has upheld {reg0?her:his} end of the bargain.  Let us have no more of this talk.",
		"lord_pretalk",
	[
		#(faction_get_slot, ":faction_liege", "$g_talk_troop_faction", slot_faction_leader),
		#(call_script, "script_troop_get_relation_with_troop", "$g_talk_troop", ":faction_liege"),
		#(try_begin),
		#	(this_or_next|gt, reg0, "$g_talk_troop_effective_relation"),
		#		(ge, reg0, 20),
		#	(call_script, "script_change_player_relation_with_troop", ":faction_leader", -1),
		#(try_end),
		(call_script, "script_change_player_relation_with_troop", "$g_talk_troop", -1),
	]],
[anyone,"lord_spouse_leave_faction_proclaim_queen", [
	(this_or_next|is_between, "$g_talk_troop", active_npcs_begin, active_npcs_end),
		(troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_hero),

	(assign, ":liege_bonus", 0),
	(try_begin),
		#Only apply this to the lord's first kingdom.
		(troop_slot_eq, "$g_talk_troop", slot_troop_original_faction, "$g_talk_troop_faction"),
		#Don't apply it to former comrades under arms
		#gekokujo 3.0 microfactions! include fort companions start
		#(this_or_next|neg|is_between, "$g_talk_troop", companions_begin, companions_end),
		(this_or_next|neg|is_between, "$g_talk_troop", companions_begin, fort_companions_end),
		#gekokujo 3.0 microfactions! include fort companions end
			(troop_slot_eq, "$g_talk_troop", slot_troop_playerparty_history, dplmc_pp_history_nonplayer_entry),
		(this_or_next|neg|is_between, "$g_talk_troop", pretenders_begin, pretenders_end),
			(troop_slot_eq, "$g_talk_troop", slot_troop_playerparty_history, dplmc_pp_history_nonplayer_entry),
		(game_get_reduce_campaign_ai, ":reduce_campaign_ai"),
		(try_begin),
			(eq, ":reduce_campaign_ai", 0),#hard
			(assign, ":liege_bonus", 75),
		(else_try),
			(eq, ":reduce_campaign_ai", 1),#medium
			(assign, ":liege_bonus", 50),
		(else_try),
			(eq, ":reduce_campaign_ai", 2),#easy
			(assign, ":liege_bonus", 25),
		(try_end),
	(try_end),

	(call_script, "script_dplmc_get_troop_morality_value", "$g_talk_troop", tmt_honest),
	(assign, ":honesty", reg0),
	(try_begin),
		(eq, ":honesty", 0),
		(this_or_next|troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_cunning),
		(this_or_next|troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_roguish),
		(this_or_next|troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_quarrelsome),
		(this_or_next|troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_debauched),
			(troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_ambitious),
		(assign, ":honesty", -1),
	(else_try),
		(eq, ":honesty", 0),
		(this_or_next|troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_upstanding),
			(troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_moralist),
		(assign, ":honesty", 1),
	(try_end),

	#Check the target value to beat (generally this should be easy; this is just
	#to stop massively premature willingness to rebel)
	(try_begin),
		(ge, ":honesty", 1),
		(val_mul, ":liege_bonus", 3),
		(val_div, ":liege_bonus", 2),
	(else_try),
		(lt, ":honesty", 0),
		(val_div, ":liege_bonus", 2),
	(try_end),
	(faction_get_slot, ":faction_liege", "$g_talk_troop_faction", slot_faction_leader),
	(call_script, "script_troop_get_relation_with_troop", "$g_talk_troop", ":faction_liege"),
	(assign, ":liege_relation", reg0),
	(store_add, ":liege_score", ":liege_bonus", ":liege_relation"),
	(store_add, ":player_score", "$player_right_to_rule", "$g_talk_troop_effective_relation"),
	(try_begin),
		(ge, "$cheat_mode", 1),
		(assign, reg0, ":liege_score"),
		(assign, reg1, ":player_score"),
		(display_message, "@{!}DEBUG - liege score {reg0} vs player score {reg1}"),
	(try_end),
	(ge, ":liege_score", ":player_score"),
	#(call_script, "script_dplmc_store_troop_is_female", ":faction_liege"),
	(str_store_troop_name, s11, ":faction_liege"),
	], "I see no reason to turn my back on {s11} now.",
		"lord_pretalk", []],
[anyone,"lord_spouse_leave_faction_husband_king", [
(assign, ":lord_has_fortress", 0),
(try_for_range, ":walled_center", walled_centers_begin, walled_centers_end),
(this_or_next|party_slot_eq, ":walled_center", slot_town_lord, "trp_player"),
(party_slot_eq, ":walled_center", slot_town_lord, "$g_talk_troop"),
(assign, ":lord_has_fortress", 1),
(try_end),
(eq, ":lord_has_fortress", 0),
##diplomacy start+ load relation text into s0
(call_script, "script_dplmc_print_player_spouse_says_my_husband_wife_to_s0", "$g_talk_troop", 0),
##diplomacy end+
],
#diplomacy start+ either gender PC can marry opposite-gender lords.  {s1} is reused from above
"Perhaps some day, {s0} -- but before I declare myself {s1}, I should like for one of us to hold a fortress which could serve as our court before we declare ourselves publically.",
#diplomacy end+
"lord_pretalk",[]],
[anyone,"lord_spouse_leave_faction_proclaim_queen", [
(assign, ":lord_has_fortress", 0),
(try_for_range, ":walled_center", walled_centers_begin, walled_centers_end),
(this_or_next|party_slot_eq, ":walled_center", slot_town_lord, "trp_player"),
(party_slot_eq, ":walled_center", slot_town_lord, "$g_talk_troop"),
(assign, ":lord_has_fortress", 1),
(try_end),
(eq, ":lord_has_fortress", 0),
##diplomacy start+ load relation text into s0
(call_script, "script_dplmc_print_player_spouse_says_my_husband_wife_to_s0", "$g_talk_troop", 0),
##diplomacy end+
],
##diplomacy start+ either gender PC can marry opposite-gender lords
"While I do not contest your claim, {s0}, I should like for one of us to hold a fortress which could serve as our court before we declare ourselves publically.", "lord_pretalk",[]],
[anyone,"lord_spouse_leave_faction_proclaim_queen", [
(assign, ":player_has_enough_right", 0),
(try_begin),
(le, "$player_right_to_rule", 5),
##diplomacy start+
#Use culture/gender appropriate word for "queen"
(try_begin),
	(eq, 1, "$character_gender"),
	(call_script, "script_dplmc_print_cultural_word_to_sreg", "$g_talk_troop", DPLMC_CULTURAL_TERM_KING_FEMALE, 0),
(else_try),
   (call_script, "script_dplmc_print_cultural_word_to_sreg", "$g_talk_troop", DPLMC_CULTURAL_TERM_KING, 0),
(try_end),
##diplomacy end+
(str_store_string, s11, "str_really_well_this_is_the_first_i_have_heard_of_it_unless_you_build_up_support_for_that_claim_you_may_find_it_difficult_to_find_allies_however_whenever_you_see_fit_to_declare_yourself_publically_as_queen_i_should_be_honored_to_be_your_consort"),
(assign, "$player_right_to_rule", 5),
(else_try),
(lt, "$player_right_to_rule", 20),
(str_store_string, s11, "str_yes_i_have_heard_such_talk_while_it_is_good_that_you_are_building_up_your_support_i_do_not_think_that_you_are_quite_ready_to_proclaim_yourself_yet_however_i_will_let_you_be_the_judge_of_that_and_when_you_decide_i_should_be_honored_to_be_your_consort"),
(else_try),
(str_store_string, s11, "str_yes_and_many_others_in_calradia_think_so_as_well_perhaps_it_is_time_that_you_declared_yourself_and_we_shall_ride_forth_together_to_claim_your_throne_i_should_be_honored_to_be_your_consort"),
(assign, ":player_has_enough_right", 1),
(try_end),
(eq, ":player_has_enough_right", 1),
],
"{s11}", "lord_spouse_leave_faction_proclaim_queen_confirm",[]],
[anyone,"lord_spouse_leave_faction_proclaim_queen", [
],
"{s11}", "lord_pretalk",[]],
[anyone|plyr,"lord_spouse_leave_faction_proclaim_queen_confirm", [
],
#diplomacy start+ either gender PC can marry opposite-gender lords
"I am ready now, my {wife/husband}. Let us go forth to seek our power.", "close_window",[
#Apply relation loss:
	(assign, ":spouse", "$g_talk_troop"),
	(faction_get_slot, ":faction_liege", "$g_talk_troop_faction", slot_faction_leader),
	(call_script, "script_troop_get_player_relation", ":faction_liege"),
	(assign, ":faction_liege_relation", reg0),
	#The relation change with the liege is exacerbated by the number of fiefs
	#lost.  The "-10" figure is the previous relation hit for defecting; this now
	#scales up with the number of centers taken.
	(assign, ":relation_change", 0),
	(try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
		(this_or_next|party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
			(party_slot_eq, ":center_no", slot_town_lord, "$g_talk_troop"),
		(val_add, ":relation_change", -10),
	(try_end),

	#Defecting from a supposedly-beloved lord causes a greater hit to honor than if
	#the defection isn't so out-of-the-blue.
	(store_add, ":honor_change", ":faction_liege_relation", 5),
	(val_div, ":honor_change", -10),
	(val_min, ":honor_change", 0),
	#Defecting during a time of war is more dishonorable than defecting during a time
	#of peace.
	(try_begin),
		(assign, ":is_war", 0),
		(try_for_range, ":faction_no", npc_kingdoms_begin, npc_kingdoms_end),
			(faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
			(neq, ":faction_no", ":faction_liege_relation"),
			(store_relation, ":reln", ":faction_no", "$g_talk_troop_faction"),
			(lt, ":reln", 0),
			(assign, ":is_war", 1),
		(try_end),
		(gt, ":is_war", 0),
		(val_add, ":honor_change", -5),
	(try_end),
	#The baseline change is -10.  The greatest possible is -25 (100 relation with the king, and at war).
	(val_sub, ":honor_change", 10),

	#If the player was insufficiently recognized for his service, the honor loss
	#is lower.  (This will further modify the reaction of some lords.)
	(call_script, "script_dplmc_center_point_calc", "$g_talk_troop_faction", "trp_player", ":spouse", 3),
	(assign, ":avg_renown_per_center_point", reg0),
	(assign, ":player_center_points", reg1),
	(assign, ":spouse_center_points", reg2),
	(troop_get_slot, ":player_renown", "trp_player", slot_troop_renown),
	(troop_get_slot, ":spouse_renown", ":spouse", slot_troop_renown),
	(assign, ":fief_unfairness", 0),#0 = no justification on basis of unfairness, 1 = justified by unfairness

	(try_begin),
		(eq, ":player_center_points", 0),
		#Unfair if the player has no fiefs and at least 3/4 of average renown per center point
		(try_begin),
			(store_mul, reg0, ":avg_renown_per_center_point", 3),
			(val_div, reg0, 4),
			(ge, ":player_renown", reg0),
			(assign, ":fief_unfairness", 1),
			(val_add, ":honor_change", 5),
		(try_end),
	(else_try),
		#Unfair if the player's (renown / center points) is more than 5/4 the average
        (gt, ":player_center_points", 0),
		(store_div, ":player_renown_per_point", ":player_renown", ":player_center_points"),
		(store_mul, reg0, ":avg_renown_per_center_point", 5),
		(val_div, reg0, 4),
		#player is insufficiently rewarded for his renown
		(ge, ":player_renown_per_point", reg0),
		(assign, ":fief_unfairness", 1),
		(val_add, ":honor_change", 5),
	(try_end),
	#Now also try for the spouse
	(try_begin),
		(eq, ":spouse_center_points", 0),
		#Unfair if the spouse has no fiefs and at least 3/4 of average renown per center point
		(try_begin),
			(store_mul, reg0, ":avg_renown_per_center_point", 3),
			(val_div, reg0, 4),
			(ge, ":spouse_renown", reg0),
			(assign, ":fief_unfairness", 1),
			(val_add, ":honor_change", 5),
		(try_end),
	(else_try),
		#Unfair if the spouse's (renown / center points) is more than 5/4 the average
        (gt, ":spouse_center_points", 0),
		(store_div, ":spouse_renown_per_point", ":spouse_renown", ":spouse_center_points"),
		(store_mul, reg0, ":avg_renown_per_center_point", 5),
		(val_div, reg0, 4),
		#spouse is insufficiently rewarded for his renown

		(ge, ":spouse_renown_per_point", reg0),
		(assign, ":fief_unfairness", 1),
		(val_add, ":honor_change", 5),
	(try_end),

    (call_script, "script_change_player_relation_with_troop", ":faction_liege", ":relation_change"),
	(val_min, ":honor_change", 0),#honor cannot rise from this
	(try_begin),
		(lt, ":honor_change", 0),
		(call_script, "script_change_player_honor", ":honor_change"),
	(try_end),

	#If the player's departure is not justified by some other cause (such as
	#not being granted the rights to a fief that he had conquered, which Martial lords
	#would be sympathetic to at least in principle), he takes a general relations hit.
	(try_for_range, ":troop_no", heroes_begin, heroes_end),
		(troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
		(neq, ":troop_no", ":faction_liege"),
		(neq, ":troop_no", ":spouse"),
		(neq, ":troop_no", active_npcs_including_player_begin),
		(store_troop_faction, ":faction_no", ":troop_no"),
		(eq, ":faction_no", "$g_talk_troop_faction"),

		#Calculate the relationship penalty, if any
		(assign, ":relation_penalty", 0),
		(assign, ":spouse_penalty", 0),# only for lost fiefs

		#Relevant factors are:
		#The troop's relation with the player, the troop's relation with his liege,
		#the troop's primary reputation, and whether the troop has the tmt_honest
		#morality subtype (which despite its name is primarily related to keeping
		#bargains), and whether this defection is causing the troop to lose any fiefs.
		(call_script, "script_troop_get_player_relation", ":troop_no"),
		(assign, ":troop_player_relation", reg0),

		(call_script, "script_troop_get_relation_with_troop", ":troop_no", ":faction_liege"),
		(assign, ":troop_king_relation", reg0),

		(troop_get_slot, ":reputation", ":troop_no", slot_lord_reputation_type),
		(call_script, "script_dplmc_get_troop_morality_value", ":troop_no", tmt_honest),
		(assign, ":honest_val", reg0),

		(assign, ":fiefs_lost", 0),
		(assign, ":fiefs_lost_spouse", 0),
		(try_for_range, ":village_no", villages_begin, villages_end),
			(party_slot_eq, ":village_no", slot_town_lord, ":troop_no"),
			(party_get_slot, ":bound_center", ":village_no", slot_village_bound_center),
			(ge, ":bound_center", 1),
			(this_or_next|party_slot_eq, ":bound_center", slot_town_lord, ":spouse"),
				(party_slot_eq, ":bound_center", slot_town_lord, "trp_player"),
			(val_add, ":fiefs_lost", 1),
			#Blaming the spouse specifically:
			(party_slot_eq, ":bound_center", slot_town_lord, ":spouse"),
			(val_add, ":fiefs_lost_spouse", 1),
		(try_end),

		#Modify for relationship with liege
		(try_begin),
			(this_or_next|ge, ":honest_val", 1),
			(this_or_next|eq, ":reputation", lrep_upstanding),
				(eq, ":reputation", lrep_moralist),
			(ge, ":troop_king_relation", 5),
			(val_sub, ":relation_penalty", 1),
		(else_try),
			(this_or_next|lt, ":honest_val", 0),
			(this_or_next|eq, ":reputation", lrep_debauched),
			(this_or_next|eq, ":reputation", lrep_roguish),
				(eq, ":reputation", lrep_ambitious),
			(ge, ":troop_king_relation", 25),
			(val_sub, ":relation_penalty", 1),
		(else_try),
			(ge, ":troop_king_relation", 15),
			(val_sub, ":relation_penalty", 1),
		(try_end),

		#Those who like the king more than the player will take his side,
		#if they met the above relation threshold.
		(try_begin),
			(lt, ":relation_penalty", 0),
			(ge, ":troop_king_relation", ":troop_player_relation"),
			(val_sub, ":relation_penalty", 1),
		(try_end),

		#Lords who would consider the rebellion more justified if the player was "under-fiefed"
		#(some will only care if they liked the player; others have a more general sense of fairness).
		(try_begin),
			(ge, ":fief_unfairness", 1),
			(try_begin),
				(ge, ":honest_val", 0),
				(neq, ":reputation", lrep_debauched),
				(neq, ":reputation", lrep_selfrighteous),
				(neq, ":reputation", lrep_quarrelsome),
				(neq, ":reputation", lrep_cunning),
				(neq, ":reputation", lrep_ambitious),
				(ge, ":troop_player_relation", 0),
				(val_add, ":relation_penalty", ":fief_unfairness"),
			(else_try),
				(ge, ":troop_player_relation", 20),
				(val_add, ":relation_penalty", ":fief_unfairness"),
			(try_end),
		(try_end),

		#Subtract a penalty for lost fiefs
		(try_begin),
			(ge, ":fiefs_lost", 1),
			#apply -2 times fiefs lost
			(this_or_next|eq, ":reputation", lrep_custodian),
			(this_or_next|eq, ":reputation", lrep_ambitious),
            (this_or_next|eq, ":reputation", lrep_quarrelsome),
            (this_or_next|eq, ":reputation", lrep_selfrighteous),
            (this_or_next|eq, ":reputation", lrep_cunning),
            (this_or_next|eq, ":reputation", lrep_debauched),
				(eq, ":reputation", lrep_martial),
			(val_sub, ":relation_penalty", ":fiefs_lost"),
			(val_sub, ":relation_penalty", ":fiefs_lost"),
			(val_sub, ":spouse_penalty", ":fiefs_lost_spouse"),
			(val_sub, ":spouse_penalty", ":fiefs_lost_spouse"),
		(else_try),
			(ge, ":fiefs_lost", 1),
			#apply -1 times fiefs lost
			(neg|ge, ":reputation", lrep_conventional),
			(neq, ":reputation", lrep_goodnatured),
			(val_sub, ":relation_penalty", ":fiefs_lost"),
			(val_sub, ":spouse_penalty", ":fiefs_lost_spouse"),
		(try_end),

		#If the penalty for the spouse is less than zero, apply it
		(try_begin),
			(lt, ":spouse_penalty", 0),
			(call_script, "script_troop_change_relation_with_troop", ":troop_no", ":spouse", ":spouse_penalty"),
		(try_end),
		#If the penalty for the player is less than zero, apply it
		(lt, ":relation_penalty", 0),
		(call_script, "script_change_player_relation_with_troop", ":troop_no", ":relation_penalty"),
	(try_end),
#diplomacy end+
(call_script, "script_activate_player_faction", "trp_player"),
(call_script, "script_change_troop_faction", "$g_talk_troop", "fac_player_supporters_faction"),
(assign, "$g_leave_encounter", 1),
]],
[anyone|plyr,"lord_spouse_leave_faction_proclaim_queen_confirm", [
],
"Perhaps I am not yet ready.", "lord_pretalk",[]],
[anyone,"lord_spouse_leave_faction_husband_king", [
(eq, "$players_kingdom", "fac_player_supporters_faction"),
(gt, "$supported_pretender", 0),
(str_store_troop_name, s4, "$supported_pretender"),
],
"Perhaps, but I would need your full support to press that claim. You would want to resolve {s4}'s rebellion before pushing this any further.", "lord_pretalk",[]],
[anyone,"lord_spouse_leave_faction_husband_king", [
(faction_get_slot, ":talk_troop_liege", "$g_talk_troop_faction", slot_faction_leader),
(str_store_troop_name, s4, ":talk_troop_liege"),
##diplomacy start+
#Replace "king" with {s0}
(call_script, "script_dplmc_print_cultural_word_to_sreg", "$g_talk_troop", DPLMC_CULTURAL_TERM_KING, 0),
],
"Most of the great families of this land have a claim to power... Given the recent issues with the succession, I should be as legitimate a {s0} as {s4}. ", "lord_spouse_leave_faction_husband_king_2",[]],
[anyone,"lord_spouse_leave_faction_husband_king_2", [
##diplomacy start+
#Replace {queen/king} with {s0}
(try_begin),
   (eq, reg65, 0),
   (call_script, "script_dplmc_print_cultural_word_to_sreg", "$g_talk_troop", DPLMC_CULTURAL_TERM_KING, 0),
(else_try),
   (call_script, "script_dplmc_print_cultural_word_to_sreg", "$g_talk_troop", DPLMC_CULTURAL_TERM_KING_FEMALE, 0),
(try_end),
],
#next line replace {queen/king} with {s0}
"While {s0}, I will defer to your judgment in the appointment of ministers, the conduct of diplomacy, and other such matters.", "lord_spouse_leave_faction_husband_king_3",[]],
[anyone|plyr,"lord_spouse_leave_faction_husband_king_3", [
],
#diplomacy start+ either gender PC can marry opposite-gender lords
"Very well, my {wife/husband}. Let us ride forth to press your claim! ", "close_window",[
#diplomacy end+
(call_script, "script_change_troop_faction", "$g_talk_troop", "fac_player_supporters_faction"),
(call_script, "script_activate_player_faction", "$g_talk_troop"),
(assign, "$g_leave_encounter", 1),
]],
[anyone|plyr,"lord_spouse_leave_faction_husband_king_3", [
],
"Actually, let us bide out time for a bit.", "lord_pretalk",[
]],
[anyone,"lord_recruit_2_philosophy", [
(call_script, "script_lord_comment_to_s43", "$g_talk_troop", "str_political_philosophy_default"),
],
"{s43} Did you wish to speak of anything else?", "lord_recruit_2",[]],
[anyone|plyr,"lord_recruit_2", [
(troop_slot_eq, "$g_talk_troop", slot_troop_recruitment_random, 0),
(faction_get_slot, ":leader", "$g_talk_troop_faction", slot_faction_leader),
(neq, "$g_talk_troop", ":leader"),
(neq, "trp_player", ":leader"),
(str_store_troop_name, s15, ":leader"),
],
"How do you feel about {s15}?", "lord_recruit_2_discontent",[
]],
[anyone|plyr,"lord_recruit_2", [
#(troop_slot_ge, "$g_talk_troop", slot_troop_recruitment_candidate, 1),
(troop_slot_ge, "$g_talk_troop", slot_lord_recruitment_argument, 1),
(neq, "$g_talk_troop_faction", "$players_kingdom"),
],
"Do you remember what I had told you earlier?", "lord_recruit_3_a",[
]],
[anyone|plyr|repeat_for_troops,"lord_recruit_2", [
(store_repeat_object, ":troop_no"),
(is_between, ":troop_no", active_npcs_begin, active_npcs_end),
(store_faction_of_troop, ":faction", ":troop_no"),
(eq, ":faction", "$g_talk_troop_faction"),
(neg|faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, ":troop_no"), #yields wrong string
(call_script, "script_troop_get_relation_with_troop", "$g_talk_troop", ":troop_no"),
(lt, reg0, -9),
(str_store_troop_name, s16, ":troop_no"),
],
"I have heard that you have quarreled with {s16}", "lord_recruit_quarrel_describe",[
(store_repeat_object, "$temp"),
]],
[anyone,"lord_recruit_quarrel_describe",
[
##diplomacy start+
(assign, ":other_lord_is_female", 0),
(try_begin),
   (call_script, "script_cf_dplmc_troop_is_female", "$temp"),
	(assign, ":other_lord_is_female", 1),
(try_end),
(assign, reg3, ":other_lord_is_female"),
(assign, reg4, ":other_lord_is_female"),
##diplomacy end+
(assign, ":specific_quarrel_found", 0),
(store_add, ":log_entries_plus_one", "$num_log_entries", 1),
(try_for_range, ":log_entry_no", 1, ":log_entries_plus_one"),
(troop_slot_eq, "trp_log_array_entry_type", ":log_entry_no", logent_ruler_intervenes_in_quarrel),
(troop_slot_eq, "trp_log_array_troop_object", ":log_entry_no", "$temp"),
(troop_slot_eq, "trp_log_array_center_object", ":log_entry_no", "$g_talk_troop"),
(troop_slot_eq, "trp_log_array_faction_object", ":log_entry_no", "$g_talk_troop_faction"),

(call_script, "script_get_relevant_comment_for_log_entry", ":log_entry_no"),
(str_store_string, s14, reg0),
(assign, ":specific_quarrel_found", 1),
(else_try),
(troop_slot_eq, "trp_log_array_entry_type", ":log_entry_no", logent_lord_protests_marshall_appointment),
(troop_slot_eq, "trp_log_array_actor", ":log_entry_no", "$g_talk_troop"),
(troop_slot_eq, "trp_log_array_center_object", ":log_entry_no", "$temp"),
(call_script, "script_get_relevant_comment_for_log_entry", ":log_entry_no"),
(str_store_string, s14, reg0),
(assign, ":specific_quarrel_found", 1),
(else_try),
(troop_slot_eq, "trp_log_array_entry_type", ":log_entry_no", logent_lord_blames_defeat),
(troop_slot_eq, "trp_log_array_actor", ":log_entry_no", "$g_talk_troop"),
(troop_slot_eq, "trp_log_array_center_object", ":log_entry_no", "$temp"),
(call_script, "script_get_relevant_comment_for_log_entry", ":log_entry_no"),
(str_store_string, s14, reg0),
(assign, ":specific_quarrel_found", 1),
(else_try),
(troop_slot_eq, "trp_log_array_entry_type", ":log_entry_no", logent_troop_feels_cheated_by_troop_over_land),
(troop_slot_eq, "trp_log_array_actor", ":log_entry_no", "$g_talk_troop"),
(troop_slot_eq, "trp_log_array_troop_object", ":log_entry_no",  "$temp"),
(call_script, "script_get_relevant_comment_for_log_entry", ":log_entry_no"),
(str_store_string, s14, reg0),
(assign, ":specific_quarrel_found", 1),
(else_try),
(troop_slot_eq, "trp_log_array_entry_type", ":log_entry_no", logent_lords_quarrel_over_woman),
(troop_slot_eq, "trp_log_array_actor", ":log_entry_no", "$g_talk_troop"),
(troop_slot_eq, "trp_log_array_center_object", ":log_entry_no", "$temp"),
(call_script, "script_get_relevant_comment_for_log_entry", ":log_entry_no"),
##diplomacy start+ set gender for courted lady
(troop_get_slot, ":courted_lady", "trp_log_array_troop_object", ":log_entry_no"),
(assign, reg4, 0),
(try_begin),
   (call_script, "script_cf_dplmc_troop_is_female", ":courted_lady"),
	(assign, reg4, 1),
(try_end),
##diplomacy end+
(str_store_string, s14, reg0),
(assign, ":specific_quarrel_found", 1),
(else_try),
(troop_slot_eq, "trp_log_array_entry_type",  ":log_entry_no", logent_lords_quarrel_over_woman),
(troop_slot_eq, "trp_log_array_actor", ":log_entry_no", "$temp"),
(troop_slot_eq, "trp_log_array_center_object", ":log_entry_no", "$g_talk_troop"),
(call_script, "script_get_relevant_comment_for_log_entry", ":log_entry_no"),
##diplomacy start+ set gender for courted lady
(troop_get_slot, ":courted_lady", "trp_log_array_troop_object", ":log_entry_no"),
(assign, reg4, 0),
(try_begin),
   (call_script, "script_cf_dplmc_troop_is_female", ":courted_lady"),
	(assign, reg4, 1),
(try_end),
##diplomacy end+
(str_store_string, s14, reg0),
(assign, ":specific_quarrel_found", 1),
(try_end),

(try_begin),
(eq, ":specific_quarrel_found", 0),
(call_script, "script_troop_describes_quarrel_with_troop_to_s14", "$g_talk_troop", "$temp"),
(try_end),

(call_script, "script_add_rumor_string_to_troop_notes", "$g_talk_troop", "$temp", 14),
],
"It is no secret. {s14}", "lord_recruit_2",[
]],
[anyone|plyr,"lord_recruit_2", [
],
"Never mind", "lord_pretalk",[]],
[anyone,"lord_recruit_2_discontent", [
(faction_get_slot, ":leader", "$g_talk_troop_faction", slot_faction_leader),

(call_script, "script_calculate_troop_political_factors_for_liege", "$g_talk_troop", ":leader"),
(assign, ":result_for_political", reg3),

(try_begin),
(eq, "$cheat_mode", 1),
(display_message, "@{!}DEBUG : result_for_political is {reg3}"),
(try_end),

##diplomacy start+
#(call_script, "script_troop_get_relation_with_troop", "$g_talk_troop", ":leader"),
#(assign, ":liege_relation", reg0),
#(str_store_troop_name, s15, ":leader"),
#(troop_get_type, reg15, ":leader"),

(try_begin),
    (lt, ":leader", 0),#The dialogs below will be absurd if the leader is "no one", but it's better than just an error message
    (assign, ":liege_relation", 0),
    (str_store_string, s15, "str_noone"),
    (assign, reg15, 0),
(else_try),
    (call_script, "script_troop_get_relation_with_troop", "$g_talk_troop", ":leader"),
    (assign, ":liege_relation", reg0),
    (str_store_troop_name, s15, ":leader"),
    (assign, reg15, 0),
    (call_script, "script_cf_dplmc_troop_is_female", ":leader"),
    (assign, reg15, 1),
(try_end),
##diplomacy end+

(try_begin),
(troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_upstanding),
(assign, ":intrigue_willingness", -5),
(str_store_string, s12, "str_i_am_disturbed_about_my_lord_s15s_choice_of_companions"),
(else_try),
(troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_martial),
(assign, ":intrigue_willingness", -1),
(str_store_string, s12, "str_well_ill_be_honest_i_feel_that_sometimes_s15_overlooks_my_rights_and_extends_his_protection_to_the_unworthy"),
(else_try),
(troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_quarrelsome),
(assign, ":intrigue_willingness", 5),
(str_store_string, s12, "str_heh_one_thing_that_ill_say_about_s15_is_that_he_has_a_ripe_batch_of_bastards_in_his_court"),
(else_try),
(troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_goodnatured),
(assign, ":intrigue_willingness", -4),
(str_store_string, s12, "str_well_sometimes_i_have_to_say_that_i_question_s15s_judgment_regarding_those_who_he_keeps_in_his_court"),
(else_try),
(troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_selfrighteous),
(assign, ":intrigue_willingness", 1),
(str_store_string, s12, "str_s15_is_a_weak_man_who_too_easily_lends_his_ear_to_evil_council_and_gives_his_protection_to_some_who_have_done_me_wrong"),
(else_try),
(troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_cunning),
(assign, ":intrigue_willingness", 3),
(str_store_string, s12, "str_i_will_confess_that_sometimes_i_worry_about_s15s_judgment_particularly_in_the_matter_of_the_counsel_that_he_keeps"),
(else_try),
(troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_debauched),
(assign, ":intrigue_willingness", 5),
(str_store_string, s12, "str_what_do_i_think_i_think_that_s15_is_a_vile_pretender_a_friend_to_the_flatterer_and_the_hypocrite"),
(else_try),
(troop_slot_ge, "$g_talk_troop", slot_lord_reputation_type, lrep_roguish),
(assign, ":intrigue_willingness", 5),
(str_store_string, s12, "str_well_s15_is_not_like_you_ill_say_that_much"),
(try_end),

#is there a specific quarrel?
(store_add, ":log_entries_plus_one", "$num_log_entries", 1),
(try_for_range, ":log_entry_no", 1, ":log_entries_plus_one"),
(troop_slot_eq, "trp_log_array_entry_type", ":log_entry_no", logent_ruler_intervenes_in_quarrel),
(troop_slot_eq, "trp_log_array_actor", ":log_entry_no", ":leader"),
(troop_slot_eq, "trp_log_array_center_object", ":log_entry_no", "$g_talk_troop"),
(call_script, "script_get_relevant_comment_for_log_entry", ":log_entry_no"),
(str_store_string, s12, reg0),
(else_try),
(troop_slot_eq, "trp_log_array_entry_type", ":log_entry_no", logent_lord_protests_marshall_appointment),
(troop_slot_eq, "trp_log_array_actor", ":log_entry_no", "$g_talk_troop"),
(troop_slot_eq, "trp_log_array_troop_object", ":log_entry_no",  ":leader"),
(call_script, "script_get_relevant_comment_for_log_entry", ":log_entry_no"),
(str_store_string, s12, reg0),
(else_try),
(troop_slot_eq, "trp_log_array_entry_type", ":log_entry_no", logent_lord_blames_defeat),
(troop_slot_eq, "trp_log_array_actor", ":log_entry_no", "$g_talk_troop"),
(troop_slot_eq, "trp_log_array_troop_object", ":log_entry_no", ":leader"),
(call_script, "script_get_relevant_comment_for_log_entry", ":log_entry_no"),
(str_store_string, s12, reg0),
(else_try),
(troop_slot_eq, "trp_log_array_entry_type", ":log_entry_no", logent_troop_feels_cheated_by_troop_over_land),
(troop_slot_eq, "trp_log_array_actor", ":log_entry_no", "$g_talk_troop"),
(troop_slot_eq, "trp_log_array_faction_object", ":log_entry_no", "$g_talk_troop_faction"),
(call_script, "script_get_relevant_comment_for_log_entry", ":log_entry_no"),
(str_store_string, s12, reg0),
(try_end),

(val_mul, ":intrigue_willingness", 2), #-10 to 10

(assign, "$lord_might_open_up", 0),
(try_begin),
(gt, ":result_for_political", 12),
(gt, ":liege_relation", 0),
(str_store_string, s12, "str_s15_long_may_he_live"),
(else_try),
(ge, ":result_for_political", ":intrigue_willingness"),
(str_store_string, s12, "str_he_is_my_liege_that_is_all_that_i_will_say_on_this_matter"),
(assign, "$lord_might_open_up", 1),
(try_end),

(lt, ":result_for_political", ":intrigue_willingness"),

(call_script, "script_add_rumor_string_to_troop_notes", "$g_talk_troop", ":leader", 12),
],
"{s12}", "lord_recruit_2_discontent_b",[
]],
[anyone, "lord_recruit_2_discontent", [
],
"{s12}", "lord_recruit_hesitant", []],
[anyone, "lord_recruit_2_discontent_b", [  ],
"Sometimes, I do worry about the state of the clan.", "lord_recruit_3", []],
[anyone|plyr,"lord_recruit_hesitant",
[
(eq, "$lord_might_open_up", 1),
],
"Can't I persuade you to say a little more?", "lord_recruit_hesitant_persuade",[
]],
[anyone|plyr,"lord_recruit_hesitant", [],
"Ah. Very good.", "lord_pretalk", []],
[anyone, "lord_recruit_hesitant_persuade",
[
(faction_get_slot, ":leader", "$g_talk_troop_faction", slot_faction_leader),
(call_script, "script_calculate_troop_political_factors_for_liege", "$g_talk_troop", ":leader"),
(assign, ":result_for_political", reg3),
(store_sub, ":open_up_desire", 12, ":result_for_political"),
(assign, reg3, ":open_up_desire"),
(val_div, ":open_up_desire", 3),

#(store_random_in_range, ":random", -2, ":max_random_value"),
(store_sub, ":max_random_value", 14, ":open_up_desire"),
(troop_get_slot, ":temp_ai_seed", "$g_talk_troop", slot_troop_temp_decision_seed),
(store_mod, ":random", ":temp_ai_seed", ":max_random_value"),
(val_sub, ":random", 2), #random changes between -2 to (14 - (":result_for_political" div 3))

#(val_sub, ":random", 20), #open this line when you want to 100% pass this step and remove again after making tests.
(store_skill_level, ":persuasion_skill", "skl_persuasion", "trp_player"),
(lt, ":random", ":persuasion_skill"),
],
"If you put it that way, I admit that I do sometimes worry about the state of the realm.", "lord_recruit_3", []],
[anyone, "lord_recruit_hesitant_persuade", [
(troop_set_slot, "$g_talk_troop", slot_troop_intrigue_impatience, 100),
(call_script, "script_troop_change_relation_with_troop", "$g_talk_troop", "trp_player", -1),
],
"You try my patience. I said that I have nothing to say.", "lord_pretalk", []],
[anyone|plyr,"lord_recruit_3", [
      ],
"Well, I have something to tell you.", "lord_recruit_3_a",[
]],
[anyone|plyr,"lord_recruit_3", [
      ],
"Well, that's interesting to know. But enough about politics.", "lord_pretalk",[
]],
[anyone, "lord_recruit_3_a", [
(troop_slot_ge, "$g_talk_troop", slot_lord_recruitment_argument, 1),

(troop_get_slot, ":candidate", "$g_talk_troop", slot_lord_recruitment_candidate),
(str_store_troop_name, s14, ":candidate"),

(try_begin),
(eq, ":candidate", "trp_player"),
(str_store_string, s14, "@you"),
(try_end),

(try_begin),
(troop_slot_eq, "$g_talk_troop", slot_lord_recruitment_argument, argument_claim),
(eq, ":candidate", "trp_player"),
(str_store_string, s12, "str_that_you_are_the_rightful_heir_to_the_throne_of_calradia"),
(else_try),
(troop_slot_eq, "$g_talk_troop", slot_lord_recruitment_argument, argument_claim),
(str_store_troop_name, s14, ":candidate"),
(str_store_string, s12, "str_that_s14_is_the_rightful_ruler_of_calradia"),
(else_try),
(troop_slot_eq, "$g_talk_troop", slot_lord_recruitment_argument, argument_ruler),
(str_store_string, s12, "str_that_s14_will_rule_this_land_justly"),
(else_try),
(troop_slot_eq, "$g_talk_troop", slot_lord_recruitment_argument, argument_lords),
(str_store_string, s12, "str_that_s14_will_protect_our_rights_as_nobles"),
(else_try),
(troop_slot_eq, "$g_talk_troop", slot_lord_recruitment_argument, argument_victory),
(str_store_string, s12, "str_that_s14_will_unify_this_land_and_end_this_war"),
(else_try),
(troop_slot_eq, "$g_talk_troop", slot_lord_recruitment_argument, argument_benefit),
(str_store_string, s12, "str_that_s14_will_reward_me_with_a_fief"),
(try_end),
],
"{s12}", "lord_recruit_3_reset_claim", []],
[anyone|plyr, "lord_recruit_3_reset_claim", [  ],
"Yes, that's it.", "lord_recruit_3_claim", [

]],
[anyone|plyr, "lord_recruit_3_reset_claim", [  ],
"Let me phrase that a little differently.", "lord_recruit_3_a_reset", []],
[anyone, "lord_recruit_3_a",
[
#(display_message, "str_prior_arguments"),
#(assign, reg3, "$claim_arguments_made"),
#(display_message, "str_legal_reg3"),

#(assign, reg3, "$ruler_arguments_made"),
#(display_message, "str_just_king_reg3"),

#(assign, reg3, "$victory_arguments_made"),
#(display_message, "str_bring_peace_reg3"),

#(assign, reg3, "$lords_arguments_made"),
#(display_message, "str_only_best_counsel_reg3"),

#(assign, reg3, "$benefit_arguments_made"),
#(display_message, "str_reward_lords_reg3"),
],
"Yes?", "lord_recruit_3_b", []],
[anyone, "lord_recruit_3_a_reset", [],
"Yes?", "lord_recruit_3_b", []],
[anyone|plyr, "lord_recruit_3_b", [
(faction_get_slot, ":players_liege", "$players_kingdom", slot_faction_leader),
(eq, ":players_liege", "trp_player"),
],
"I ask for your support for the shogunate of Japan", "lord_recruit_3_why",
[
(troop_set_slot, "$g_talk_troop", slot_lord_recruitment_candidate, "trp_player"),
(try_begin),
 (troop_slot_eq, "$g_talk_troop", slot_troop_recruitment_random, 0),

 #(store_random_in_range, ":random", 1, 101), #replaced with below 3 lines to provide a constant history (not changable by save-loads).
 (troop_get_slot, ":temp_ai_seed", "$g_talk_troop", slot_troop_temp_decision_seed),
 (store_div, ":random", ":temp_ai_seed", 100),  #I used div instead of mod to have a different random value, value generated from (mod 100) will be used in next steps. These two values should be non-related.
 (val_add, ":random", 1),

 (troop_set_slot, "$g_talk_troop", slot_troop_recruitment_random, ":random"),
(try_end),
]],
[anyone|plyr, "lord_recruit_3_b", [
(faction_get_slot, ":players_liege", "$players_kingdom", slot_faction_leader),
(neq, ":players_liege", "trp_player"),
(neq, "$players_kingdom", "$g_talk_troop_faction"),
(str_store_troop_name, s45, ":players_liege"),

],
"I ask you to pledge allegiance to my lord, {s45}, as shogun of Japan", "lord_recruit_3_why",
[
(faction_get_slot, ":players_liege", "$players_kingdom", slot_faction_leader),
(troop_set_slot, "$g_talk_troop", slot_lord_recruitment_candidate, ":players_liege"),
(try_begin),
 (troop_slot_eq, "$g_talk_troop", slot_troop_recruitment_random, 0),

 #(store_random_in_range, ":random", 1, 101), #replaced with below 3 lines to provide a constant history (not changable by save-loads).
 (troop_get_slot, ":temp_ai_seed", "$g_talk_troop", slot_troop_temp_decision_seed),
 (store_div, ":random", ":temp_ai_seed", 100),  #I used div instead of mod to have a different random value, value generated from (mod 100) will be used in next steps. These two values should be non-related.
 (val_add, ":random", 1),

 (troop_set_slot, "$g_talk_troop", slot_troop_recruitment_random, ":random"),
(try_end),
]],
[anyone|plyr, "lord_recruit_3_b", [
],
"Never mind", "lord_pretalk",
[
]],
[anyone, "lord_recruit_3_dilemma_1", [ #explain the political dilemma
(troop_get_slot, ":players_liege", "$g_talk_troop", slot_lord_recruitment_candidate),
(str_store_troop_name, s45, ":players_liege"),
##diplomacy start+
#(troop_get_type, reg3, ":players_liege"),
(assign, reg3, 0),
(try_begin),
	(call_script, "script_cf_dplmc_troop_is_female", ":players_liege"),
	(assign, reg3, 1),
(try_end),
##diplomacy end+

(faction_get_slot, ":current_liege", "$g_talk_troop_faction", slot_faction_leader),
(str_store_troop_name, s46, ":current_liege"),

(call_script, "script_lord_comment_to_s43", "$g_talk_troop", "str_rebellion_dilemma_default"),
], "{s43}", "lord_recruit_3_dilemma_2",
[]],
[anyone, "lord_recruit_3_dilemma_2", [
(call_script, "script_lord_comment_to_s43", "$g_talk_troop", "str_rebellion_dilemma_2_default"),
], "{s43}", "lord_recruit_3_why",
[]],
[anyone, "lord_recruit_3_why",
[
(troop_slot_eq, "$g_talk_troop", slot_lord_recruitment_candidate, "trp_player"),

(assign, ":one_fortress_found", 0),
(try_for_range, ":walled_center", walled_centers_begin, walled_centers_end),
(this_or_next|party_slot_eq, ":walled_center", slot_town_lord, "$g_talk_troop"),
   (party_slot_eq, ":walled_center", slot_town_lord, "trp_player"),
(assign, ":one_fortress_found", 1),
(try_end),
(eq, ":one_fortress_found", 0),

],
"Neither of us has so much as a single fortress to our name. Would you rule your kingdom from an outlaw's den in the woods?", "lord_pretalk",
[
]],
[anyone, "lord_recruit_3_why",
[
(troop_get_slot, ":recruitment_candidate", "$g_talk_troop", slot_lord_recruitment_candidate),
(try_begin),
 (eq, ":recruitment_candidate", "trp_player"),
 (str_store_string, s44, "@you"),
(else_try),
 (str_store_troop_name, s44, ":recruitment_candidate"),
(try_end),
],
"Why should I support {s44}?", "lord_recruit_3_d",
[
(troop_get_slot, ":recruitment_candidate", "$g_talk_troop", slot_lord_recruitment_candidate),
(try_begin),
 ##diplomacy start+ Override is_female to use script
 ##(troop_get_type, ":is_female", ":recruitment_candidate"),
 (assign, ":is_female", 0),
 (try_begin),
	(call_script, "script_cf_dplmc_troop_is_female", ":recruitment_candidate"),
	(assign, ":is_female", 1),
 (try_end),
 ##diplomacy end+
 (str_store_string, s45, "str_he"),
 (str_store_string, s47, "str_king"),

 (try_begin),
   (eq, ":is_female", 1),
   (str_store_string, s45, "str_she"),
   (str_store_string, s47, "str_queen"),
 (try_end),

#gekokujo khan title (there is none)
# (try_begin),
#   (eq, ":recruitment_candidate", "$supported_pretender"),
#   (eq, "$supported_pretender_old_faction", "fac_kingdom_3"),
#   (str_store_string, s47, "str_khan"),
# (try_end),

 (try_begin),
   (eq, ":recruitment_candidate", "trp_player"),
   (str_store_string, s45, "str_i"),
 (try_end),
(try_end),
]],
[anyone|plyr,"lord_recruit_3_d",
[
(troop_get_slot, ":recruitment_candidate", "$g_talk_troop", slot_lord_recruitment_candidate),

(str_store_string, s43, "str_according_to_the_ancient_law_and_custom_of_the_calradians_s45_should_be_s47"),
(try_begin),
(gt, "$supported_pretender", 0),
(eq, ":recruitment_candidate", "$supported_pretender"),
(str_store_faction_name, s46, "$supported_pretender_old_faction"),
(str_store_string, s43, "str_because_s44_is_the_rightful_s47_of_the_s46"),
(try_end),
],
"{s43}", "lord_recruit_3_claim",
[
(troop_set_slot, "$g_talk_troop", slot_lord_recruitment_argument, argument_claim),
(val_add, "$claim_arguments_made", 1),
(assign, "$opposed_arguments_made", "$victory_arguments_made"),
]],
[anyone|plyr,"lord_recruit_3_d",
[],
"If {s45} were {s47}, {s45} would deal with all men fairly and uphold the rights of the commons.", "lord_recruit_3_claim",
[
(troop_set_slot, "$g_talk_troop", slot_lord_recruitment_argument, argument_ruler),
(val_add, "$ruler_arguments_made", 1),
(assign, "$opposed_arguments_made", "$lords_arguments_made"),
]],
[anyone|plyr,"lord_recruit_3_d",
[],
"If {s45} were {s47}, {s45} would uphold your rights as a samurai of this land.", "lord_recruit_3_claim",
[
(troop_set_slot, "$g_talk_troop", slot_lord_recruitment_argument, argument_lords),
(val_add, "$lords_arguments_made", 1),
(assign, "$opposed_arguments_made", "$ruler_arguments_made"),
]],
[anyone|plyr,"lord_recruit_3_d",
[],
"Because {s45} can unify Japan and end this discord.", "lord_recruit_3_claim",
[
(troop_set_slot, "$g_talk_troop", slot_lord_recruitment_argument, argument_victory),
(val_add, "$victory_arguments_made", 1),
(assign, "$opposed_arguments_made", "$claim_arguments_made"),
]],
[anyone|plyr,"lord_recruit_3_d",
[],
"Because {s45} will reward you with lands.", "lord_recruit_3_claim",[
(troop_set_slot, "$g_talk_troop", slot_lord_recruitment_argument, argument_benefit),
(val_add, "$benefit_arguments_made", 1),
]],
[anyone|plyr,"lord_recruit_3_d",
[],
"Never mind", "lord_pretalk",[
(troop_set_slot, "$g_talk_troop", slot_troop_recruitment_random, 0),
]],
[anyone,"lord_recruit_3_claim", [
(neg|troop_slot_eq, "$g_talk_troop", slot_lord_recruitment_argument, argument_benefit),

(gt, "$opposed_arguments_made", 0),
(troop_get_slot, ":recruitment_random", "$g_talk_troop", slot_troop_recruitment_random),
(store_mul, ":opposed_number", "$opposed_arguments_made", 10),
(val_add, ":opposed_number", ":recruitment_random"),
(gt, ":opposed_number", 100),

(try_begin),
(troop_slot_eq, "$g_talk_troop", slot_lord_recruitment_argument, argument_claim),
(str_store_string, s12, "str_you_speak_of_claims_and_legalities_yet_to_others_you_talk_of_bringing_peace_by_force"),
(else_try),
(troop_slot_eq, "$g_talk_troop", slot_lord_recruitment_argument, argument_victory),
(str_store_string, s12, "str_you_speak_of_bringing_peace_by_force_yet_to_others_you_make_legal_claims"),
(else_try),
(troop_slot_eq, "$g_talk_troop", slot_lord_recruitment_argument, argument_commons),
(str_store_string, s12, "str_you_speak_to_some_of_upholding_the_rights_of_the_commons_yet_you_speak_to_others_of_uphold_the_rights_of_nobles_what_if_those_rights_are_in_conflict"),
(else_try),
(troop_slot_eq, "$g_talk_troop", slot_lord_recruitment_argument, argument_lords),
##diplomacy start+ "lord" to s12
(call_script, "script_dplmc_print_cultural_word_to_sreg", "$g_talk_troop", DPLMC_CULTURAL_TERM_LORD, 12),
##diplomacy end+
(str_store_string, s12, "str_you_speak_to_me_of_upholding_my_rights_as_a_lord_but_to_others_you_talk_of_upholding_the_rights_of_all_commons_what_if_those_rights_come_into_conflict"),
(try_end),
],
"Do you perhaps tell each person what you think they most want to hear? {s12}", "lord_recruit_3_claim",
[
(assign, "$opposed_arguments_made", -1),
]],
[anyone,"lord_recruit_3_claim", [

(assign, "$g_persuasion_trump_used", 0),

(troop_get_slot, ":recruitment_candidate", "$g_talk_troop", slot_lord_recruitment_candidate),

(assign, ":continue", 0),

(str_store_string, s12, "str_a_claim_should_be_strong_indeed_before_one_starts_talking_about_it"),

(try_begin), #non-player candidates are automatically considered worthy
(neq, ":recruitment_candidate", "trp_player"),

(str_store_string, s12, "str_indeed_please_continue"),
(assign, ":continue", 1),
(else_try),
(troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_martial),

(str_store_string, s12, "str_a_claim_should_be_strong_indeed_before_one_starts_talking_about_it"),

#(assign, reg0, "$player_right_to_rule"),
#(assign, reg1, ":recruitment_candidate"),
#(troop_get_slot, reg2, ":recruitment_candidate", slot_troop_renown),
#(display_message, "@{!}DEBUG : player_right_to_rule = {reg0}"),
#(display_message, "@{!}DEBUG : recruitment_candidate = {reg1}"),
#(display_message, "@{!}DEBUG : renown = {reg2}"),

(ge, "$player_right_to_rule", 10),
##diplomacy start+ "king" to s12
(call_script, "script_dplmc_print_cultural_word_to_sreg", "$g_talk_troop", DPLMC_CULTURAL_TERM_KING, 12),
##diplomacy end+
(str_store_string, s12, "str_a_king_should_prove_his_valor_beyond_any_doubt_before_he_starts_talking_about_a_claim_to_the_throne"),
(troop_slot_ge, ":recruitment_candidate", slot_troop_renown, 400),

(assign, ":continue", 1),
(else_try),
(troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_goodnatured),
##diplomacy start+ "king" to s12
(call_script, "script_dplmc_print_cultural_word_to_sreg", "$g_talk_troop", DPLMC_CULTURAL_TERM_KING, 12),
##diplomacy end+
(str_store_string, s12, "str_you_must_prove_yourself_a_great_warrior_before_men_will_follow_you_as_king"),
(troop_slot_ge, ":recruitment_candidate", slot_troop_renown, 200),

(assign, ":continue", 1),
(else_try),
(troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_upstanding),

(str_store_string, s12, "str_a_claim_to_the_throne_should_be_strong_indeed_before_one_presses_it"),
(ge, "$player_right_to_rule", 20),
##diplomacy start+ "king" to s12
(call_script, "script_dplmc_print_cultural_word_to_sreg", "$g_talk_troop", DPLMC_CULTURAL_TERM_KING, 12),
##diplomacy end+
(str_store_string, s12, "str_indeed_but_a_man_must_also_prove_himself_a_great_warrior_before_men_will_follow_you_as_king"),
(troop_slot_ge, ":recruitment_candidate", slot_troop_renown, 200),

(assign, ":continue", 1),
(else_try),
(troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_quarrelsome),
##diplomacy start+ "king" to s12 and "pigherd" to s14
(call_script, "script_dplmc_print_cultural_word_to_sreg", "$g_talk_troop", DPLMC_CULTURAL_TERM_KING, 12),
(call_script, "script_dplmc_print_cultural_word_to_sreg", "$g_talk_troop", DPLMC_CULTURAL_TERM_SWINEHERD, 14),
##diplomacy end+
(str_store_string, s12, "str_my_pigherd_can_declare_himself_king_if_he_takes_he_fancy_i_think_you_need_to_break_a_few_more_heads_on_tbe_battlefield_before_men_will_follow_you"),
(troop_slot_ge, ":recruitment_candidate", slot_troop_renown, 200),

(assign, ":continue", 1),
(else_try),
(troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_selfrighteous),

(str_store_string, s12, "str_if_you_do_not_wish_to_die_on_a_scaffold_like_so_many_failed_pretenders_before_you_i_would_suggest_that_you_to_build_your_claim_on_stronger_foundations_so_that_men_will_follow_you"),
(ge, "$player_right_to_rule", 10),

(str_store_string, s12, "str_if_you_do_not_wish_to_die_on_a_scaffold_like_so_many_failed_pretenders_before_you_i_would_advise_you_prove_yourself_on_the_field_of_battle_so_that_men_will_follow_you"),
(troop_slot_ge, ":recruitment_candidate", slot_troop_renown, 200),

(assign, ":continue", 1),
(else_try),
(troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_debauched),
##diplomacy start+ Replace "their swords" with "their {s12}", and "kings" with "{s14}"
(call_script, "script_dplmc_print_cultural_word_to_sreg", "$g_talk_troop", DPLMC_CULTURAL_TERM_WEAPON_PLURAL, 12),
(call_script, "script_dplmc_print_cultural_word_to_sreg", "$g_talk_troop", DPLMC_CULTURAL_TERM_KING_PLURAL, 14),
##diplomacy end+
(str_store_string, s12, "str_talk_is_for_heralds_and_lawyers_real_kings_prove_themselves_with_their_swords"),
(troop_slot_ge, ":recruitment_candidate", slot_troop_renown, 200),

(assign, ":continue", 1),
(else_try),
(troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_cunning),

(str_store_string, s12, "str_i_were_you_i_would_try_to_prove_myself_a_bit_more_before_i_went_about_pressing_my_claim"),
(troop_slot_ge, ":recruitment_candidate", slot_troop_renown, 400),

(assign, ":continue", 1),
(try_end),

#Trump to overlook player unworthiness
(str_clear, s14),
(try_begin),
(eq, ":continue", 1),
(str_store_string, s12, "str_indeed_please_continue"),

(else_try),
(eq, ":continue", 0),
(eq, "$g_persuasion_trump_used", 0),
(assign, "$g_persuasion_trump_used", 1),
#persuasion check
(store_skill_level, ":persuasion_skill", "skl_persuasion", "trp_player"),

(troop_get_slot, ":persuasion_random", "$g_talk_troop", slot_troop_recruitment_random),

  (try_begin),
    (eq, "$cheat_mode", 1),
  #(assign, reg3, ":persuasion_skill"),
  #(assign, reg4, ":persuasion_random"),
  #(display_message, "str_trump_check_random_reg4_skill_reg3"),
(try_end),

(val_mul, ":persuasion_skill", 7),
(ge, ":persuasion_skill", ":persuasion_random"),

(assign, ":continue", 1),

(call_script, "script_lord_comment_to_s43", "$g_talk_troop", "str_changed_my_mind_default"),
(str_store_string, s14, "str_s12_s43"),
(str_store_string, s12, s14),
(try_end),

(eq, ":continue", 1),

],
"{s12}", "lord_recruit_4",[
]],
[anyone,"lord_recruit_3_claim",  [
                  ],
"{s12}", "lord_pretalk",[
]],
[anyone|plyr,"lord_recruit_4", [
(troop_get_slot, ":recruitment_candidate", "$g_talk_troop", slot_lord_recruitment_candidate),
(str_store_troop_name, s16,  ":recruitment_candidate"),

(try_begin),
(eq,  ":recruitment_candidate", "trp_player"),
(str_store_string, s16, "str_me"),
(try_end),
],
"I ask you to pledge your allegiance to {s16}.", "lord_recruit_4_objective_conditions",[]],
[anyone|plyr,"lord_recruit_4", [
(troop_set_slot, "$g_talk_troop", slot_troop_recruitment_random, 0),
                ],
"Never mind.", "lord_pretalk",[]],
[anyone,"lord_recruit_4_objective_conditions", [
   (troop_get_slot, ":recruitment_candidate", "$g_talk_troop", slot_lord_recruitment_candidate),

   (call_script, "script_calculate_troop_political_factors_for_liege", "$g_talk_troop", ":recruitment_candidate"),
   (str_store_string, s33, s14),

   (assign, ":result_for_security", reg2),
      (assign, ":result_for_political", reg4),

   #this will store
   (try_begin),
     (eq, "$cheat_mode", 1),
     (display_message, "str_preliminary_result_for_political_=_reg4"),
   (try_end),

#			(assign, ":result_for_ideological", reg6),
#			(assign, ":result_for_material", reg8),
   (assign, ":change_penalty", reg10),
   (assign, ":result_for_new_liege", reg0),

   (faction_get_slot, ":cur_liege", "$g_talk_troop_faction", slot_faction_leader),
   (call_script, "script_calculate_troop_political_factors_for_liege", "$g_talk_troop", ":cur_liege"),

   (store_sub, ":result_for_security_comparative", ":result_for_security", reg2),
   (store_sub, ":result_for_political_comparative", ":result_for_political", reg4),
#			(store_sub, ":result_for_ideological_comparative", ":result_for_ideological", reg6), #to be used if NPC lords ever have different ideologies
#			(store_sub, ":result_for_material_comparative", ":result_for_material", reg8), #result for material (meaning, promised new fiefs or bribes) currently disabled
   (assign, ":result_for_old_liege", reg0),

   (try_begin),
     (eq, "$cheat_mode", 1),
     (assign, reg31, ":result_for_new_liege"),
     (assign, reg32, ":result_for_old_liege"),

     (display_message, "@{!}DEBUG : result_for_new_liege : {reg31}"),
     (display_message, "@{!}DEBUG : result_for_old_liege : {reg32}"),
   (try_end),

   (store_sub, "$pledge_chance", ":result_for_new_liege", ":result_for_old_liege"),
   (val_add, "$pledge_chance", 50),
   (val_div, "$pledge_chance", 2),

   (try_begin),
      (lt, ":result_for_political", 0),

      (try_begin),
         (troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_upstanding),
         (str_store_string, s31, "str_i_worry_about_those_with_whom_you_have_chosen_to_surround_yourself" ),
      (else_try),
         (troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_martial),
         (str_store_string, s31, "str_there_are_some_outstanding_matters_between_me_and_some_of_your_vassals_"),
         (try_begin),
           (assign, reg41, ":result_for_political"),
           ##diplomacy start+ Only show debug messages if cheat mode is on
           (ge, "$cheat_mode", 1),
           ##diplomacy end+
           (display_message, "str_result_for_political_=_reg41"),
         (try_end),
      (else_try),
         (troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_quarrelsome),
         (str_store_string, s31, "str_my_liege_has_his_faults_but_i_dont_care_for_your_toadies"),
      (else_try),
         (troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_goodnatured),
         (str_store_string, s31, "str_i_think_youre_a_good_man_but_im_worried_that_you_might_be_pushed_in_the_wrong_direction_by_some_of_those_around_you"),
      (else_try),
         (troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_selfrighteous),
         (str_store_string, s31, "str_i_am_loathe_to_fight_alongside_you_so_long_as_you_take_under_your_wing_varlots_and_base_men"),
      (else_try),
         (troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_cunning),
         (str_store_string, s31, "str_ill_be_honest__with_some_of_those_who_follow_you_i_think_id_be_more_comfortable_fighting_against_you_than_with_you"),
      (else_try),
         (troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_debauched),
         (str_store_string, s31, "str_i_say_that_you_can_judge_a_man_by_the_company_he_keeps_and_you_have_surrounded_yourself_with_vipers_and_vultures"),
      (else_try),
         (troop_slot_ge, "$g_talk_troop", slot_lord_reputation_type, lrep_roguish),
         (str_store_string, s31, "str_you_know_that_i_have_always_had_a_problem_with_some_of_our_companions"),
      (try_end),
   (else_try),
      (lt, ":result_for_political_comparative", 0),
      (str_store_string, s31, "str_politically_i_would_be_a_better_position_in_the_court_of_my_current_liege_than_in_yours"),
   (else_try),
      (str_store_string, s31, "str_i_am_more_comfortable_with_you_and_your_companions_than_with_my_current_liege"),
   (try_end),
   #end political string

   #end
   (try_begin),
      (lt, ":result_for_security", 10),

      (try_begin),
         (this_or_next|troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_cunning),
         (troop_slot_ge, "$g_talk_troop", slot_lord_reputation_type, lrep_roguish),
         (str_store_string, s32, "str_militarily_youre_in_no_position_to_protect_me_should_i_be_attacked_id_be_reluctant_to_join_you_until_you_could"),
      (else_try),
         (troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_upstanding),
         (str_store_string, s32, "str_militarily_when_i_consider_the_lay_of_the_land_i_realize_that_to_pledge_myself_to_you_now_would_endanger_my_faithful_retainers_and_my_family"),
      (else_try),
         (troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_martial),
         (str_store_string, s32, "str_militarily_youre_in_no_position_to_come_to_my_help_if_someone_attacked_me_i_dont_mind_a_good_fight_but_i_like_to_have_a_chance_of_winning"),
      (else_try),
         (troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_goodnatured),
         (str_store_string, s32, "str_militarily_youre_in_no_position_to_come_to_my_help_if_someone_attacked_me_i_dont_mind_a_good_fight_but_i_like_to_have_a_chance_of_winning"),
      (else_try),
         (troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_debauched),
         (str_store_string, s32, "str_militarily_you_would_have_me_join_you_only_to_find_myself_isolated_amid_a_sea_of_enemies"),
      (else_try),
         (troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_selfrighteous),
         (str_store_string, s32, "str_militarily_you_would_have_me_join_you_only_to_find_myself_isolated_amid_a_sea_of_enemies"),
      (else_try),
         (troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_quarrelsome),
         (str_store_string, s32, "str_militarily_youre_in_no_position_to_come_to_my_help_if_someone_attacked_me_youd_let_me_be_cut_down_like_a_dog_id_bet"),
      (try_end),
   (else_try),
      (lt, ":result_for_security_comparative", 0),
      (str_store_string, s32, "str_militarily_i_wouldnt_be_any_safer_if_i_joined_you"),
   (else_try),
      (str_store_string, s32, "str_militarily_i_might_be_safer_if_i_joined_you"),
   (try_end),

   (try_begin),
      (gt, ":change_penalty", 40),
      (str_store_string, s34, "str_finally_there_is_a_cost_to_ones_reputation_to_change_sides_in_this_case_the_cost_would_be_very_high"),
   (else_try),
      (gt, ":change_penalty", 20),
      (str_store_string, s34, "str_finally_there_is_a_cost_to_ones_reputation_to_change_sides_in_this_case_the_cost_would_be_significant"),
   (else_try),
      (str_store_string, s34, "str_finally_there_is_a_cost_to_ones_reputation_to_change_sides_in_this_case_however_many_men_would_understand"),
   (try_end),
   ],
"Let me think...", "lord_recruit_5_security",[
]],
[anyone,"lord_recruit_5_security",  [
],
"{s32}", "lord_recruit_5_political",
[]],
[anyone,"lord_recruit_5_political",  [
],
"{s31}", "lord_recruit_5_ideological",
[]],
[anyone,"lord_recruit_5_ideological",  [
],
"{s33}", "lord_recruit_5_change_sides",
[

]],
[anyone,"lord_recruit_5_change_sides",  [
],
"{s34}", "lord_recruit_6",
[
(try_begin),
 (eq, "$cheat_mode", 1),
 (assign, reg1, "$pledge_chance"),
 (display_message, "str_chance_of_success_=_reg1"),
(try_end),
]],
[anyone|plyr,"lord_recruit_6",[
                      ],
"It is time for you to make a decision.", "lord_recruit_6_reaction",
[
]],
[anyone|plyr,"lord_recruit_6",[
                      ],
"No need to decide anything -- we can speak of this at a later time.", "lord_pretalk",
[
]],
[anyone,"lord_recruit_6_reaction",
[
],
"Very well...", "lord_recruit_7_decision",
[
(troop_set_slot, "$g_talk_troop", slot_troop_recruitment_random, 0),
]],
[anyone,"lord_recruit_7_decision",
[
#(store_random_in_range, ":random", 0, 100),
(troop_get_slot, ":temp_ai_seed", "$g_talk_troop", slot_troop_temp_decision_seed),
(store_mod, ":random", ":temp_ai_seed", 100),

(try_begin),
  (eq, "$cheat_mode", 1),
  (assign, reg3, ":random"),
  (display_message, "str_random_=_reg3"),
(try_end),

(faction_get_slot, ":leader", "$g_talk_troop_faction", slot_faction_leader),
(str_store_troop_name, s14, ":leader"),

(assign, ":continue_to_pledge", 0),

(try_begin),
  (troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_selfrighteous),
  (gt, ":random", "$pledge_chance"),
  (str_store_string, s12, "str_i_will_not_have_it_be_said_about_me_that_i_am_a_traitor_that_is_my_final_decision_i_have_nothing_more_to_say_on_this_matter"),
(else_try),
  (troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_martial),
  (gt, ":random", "$pledge_chance"),

  (str_store_string, s12, "str_i_am_pledged_to_defend_s14_i_am_sorry_though_we_may_meet_on_the_battlefield_i_hope_that_we_will_still_be_friends"),
(else_try),
  (this_or_next|troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_goodnatured),
  (troop_slot_ge, "$g_talk_troop", slot_lord_reputation_type, lrep_roguish),
  (gt, ":random", "$pledge_chance"),

  (str_store_string, s12, "str_i_really_cannot_bring_myself_to_renounce_s14_i_am_sorry_please_lets_not_talk_about_this_any_more"),
(else_try),
  (troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_upstanding),
  (gt, ":random", "$pledge_chance"),

  (str_store_string, s12, "str_however_i_have_decided_that_i_must_remain_loyal_to_s14_i_am_sorry"),
(else_try),
  (troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_debauched),
  (gt, ":random", "$pledge_chance"),

  (str_store_string, s12, "str_however_i_will_not_let_you_lead_me_into_treason_do_not_talk_to_me_of_this_again"),
(else_try),
  (troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_cunning),
  (gt, ":random", "$pledge_chance"),

  (str_store_string, s12, "str_its_not_good_to_get_a_reputation_as_one_who_abandons_his_liege_that_is_my_decision_let_us_speak_no_more_of_this_matter"),
(else_try),
  (troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_quarrelsome),
  (gt, ":random", "$pledge_chance"),

  (str_store_string, s12, "str_ive_decided_to_stick_with_s14_i_dont_want_to_talk_about_this_matter_any_more"),
(else_try),
  (assign, ":continue_to_pledge", 1),
(try_end),

(eq, ":continue_to_pledge", 0),
],
"{s12}", "lord_pretalk",
[
(troop_set_slot, "$g_talk_troop", slot_troop_intrigue_impatience, 500),
]],
[anyone,"lord_recruit_7_decision",
[
(troop_get_slot, ":recruitment_candidate", "$g_talk_troop", slot_lord_recruitment_candidate),
(str_store_troop_name, s4, ":recruitment_candidate"),

(try_begin),
  (eq, "$cheat_mode", 1),
  (display_message, "str_lord_pledges_to_s4"),
(try_end),
],
"Very well -- I am ready to pledge myself to {s4} as my {reg4?queen:king}.", "lord_recruit_pledge",
[
(troop_get_slot, ":recruitment_candidate", "$g_talk_troop", slot_lord_recruitment_candidate),

(try_begin),
##diplomacy start+
  (eq, ":recruitment_candidate", "trp_player"),
  (is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
  (call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", "$players_kingdom"),
  (ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
  #Do not activate player faction
(else_try),
##diplomacy end+
  (eq, ":recruitment_candidate", "trp_player"),
  (faction_slot_eq, "fac_player_supporters_faction", slot_faction_state, sfs_inactive),
  (call_script, "script_activate_player_faction", "trp_player"),
(try_end),

(assign, "$lord_expects_fief", 0),
(try_begin),
  (troop_slot_eq, "$g_talk_troop", slot_lord_recruitment_argument, argument_benefit),
  (assign, "$lord_expects_fief", 1),
(try_end),

(call_script, "script_change_troop_faction", "$g_talk_troop", "$players_kingdom"),

(try_begin), #Actually, perhaps do provocation rather than war
  (store_relation, ":relation", "$players_kingdom", "$g_talk_troop_faction"),
  (ge, ":relation", 0),

  (try_begin),
    (eq, "$cheat_mode", 1),
    (display_message, "str_lord_recruitment_provokes_home_faction"),
  (try_end),

  (call_script, "script_add_log_entry", logent_border_incident_troop_suborns_lord, "trp_player", -1, "$g_talk_troop","$g_talk_troop_faction"),
  (store_add, ":slot_provocation_days", "$players_kingdom", slot_faction_provocation_days_with_factions_begin),
  (val_sub, ":slot_provocation_days", kingdoms_begin),
  #gekokujo 3.0 provocation days increase start
  (faction_set_slot, "$g_talk_troop_faction", ":slot_provocation_days", 60),
  #(faction_set_slot, "$g_talk_troop_faction", ":slot_provocation_days", 30),
  #gekokujo 3.0 provocation days increase end

  (faction_get_slot, ":other_liege", "$g_talk_troop_faction", slot_faction_leader),
  (call_script, "script_troop_change_relation_with_troop", "trp_player", ":other_liege", -3),
(try_end),

(troop_get_type, reg4, ":recruitment_candidate"),
 ##diplomacy start+ Override reg4
 (assign, reg4, 0),
 (try_begin),
	(call_script, "script_cf_dplmc_troop_is_female", ":recruitment_candidate"),
	(assign, reg4, 1),
 (try_end),
 ##diplomacy end+
(try_begin),
  (eq, ":recruitment_candidate", "trp_player"),
  (str_store_string, s4, "@you"),
  #gekokujo 3.0 reduced RTR rewards start
  #(call_script, "script_change_player_right_to_rule", 5),
  (call_script, "script_change_player_right_to_rule", 2),
  #gekokujo 3.0 reduced RTR rewards end
(else_try),
  (str_store_troop_name, s4, ":recruitment_candidate"),
(try_end),
]],
[anyone,"lord_recruit_pledge",
[
(eq, "$lord_expects_fief", 1),
],
"Remember. You have promised me a fief. I will hold you to that promise.", "lord_recruit_pledge",
[
(assign, "$lord_expects_fief", 0),
(troop_set_slot, "$g_talk_troop", slot_lord_recruitment_argument, 0),
(call_script, "script_add_log_entry", logent_liege_promises_fief_to_vassal, "trp_player", 0, "$g_talk_troop", "$players_kingdom"),
(troop_set_slot, "$g_talk_troop", slot_troop_promised_fief, 1),
]],
[anyone,"lord_recruit_pledge",
[
(troop_get_slot, ":recruitment_candidate", "$g_talk_troop", slot_lord_recruitment_candidate),
(eq, ":recruitment_candidate", "trp_player"),
##diplomacy start+: Replace "sword" with culturally-appropriate word
(call_script, "script_dplmc_print_cultural_word_to_sreg", "$g_talk_troop", DPLMC_CULTURAL_TERM_WEAPON, 0),
],
#"So be it -- I pledge allegiance to you as your faithful vassal. I shall stand at your side to fight your enemies should you need my sword, and uphold your claims and those of your legitimate heirs. I expect in turn that you will protect me and recognize my rights as your vassal.", "lord_recruit_pledge_conclude",
"So be it -- I pledge allegiance to you as your faithful vassal. I shall stand at your side to fight your enemies should you need my {s0}, and uphold your claims and those of your legitimate heirs. I expect in turn that you will protect me and recognize my rights as your vassal.", "lord_recruit_pledge_conclude",
##diplomacy end+
[
(assign, "$g_leave_encounter", 1),
]],
[anyone,"lord_recruit_pledge",  [
(troop_get_slot, ":recruitment_candidate", "$g_talk_troop", slot_lord_recruitment_candidate),
(str_store_troop_name, s4, ":recruitment_candidate"),
##diplomacy start+: Replace "sword" with culturally-appropriate word, and fix some pronouns
(call_script, "script_dplmc_print_cultural_word_to_sreg", "$g_talk_troop", DPLMC_CULTURAL_TERM_WEAPON, 0),
(call_script, "script_dplmc_store_troop_is_female_reg", ":recruitment_candidate", 4),
],
#"So be it -- you may inform {s4} that I am now {reg4?her:him} faithful vassal, that I will follow {reg4?her:him} as long as my breath remains, and I will be at {reg4?her:his} side to fight your enemies should you need my sword, and that I uphold your lawful claims and those of your legitimate heirs. In turn, I expect his protection and his recognition of my rights as his vassal.", "lord_recruit_pledge_conclude",
"So be it -- you may inform {s4} that I am now {reg4?her:his} faithful vassal, that I will follow {reg4?her:him} as long as my breath remains, and I will be at {reg4?her:his} side to fight {reg4?her:his} enemies should {reg4?she:he} need my {s0}, and that I uphold {reg4?her:his} lawful claims and those of {reg4?her:his} legitimate heirs. In turn, I expect {reg4?her:his} protection and {reg4?her:his} recognition of my rights as {reg4?her:his} vassal.", "lord_recruit_pledge_conclude",
##diplomacy end+
[]],
[anyone,"lord_recruit_pledge_conclude",  [
],
"Now... It is a momentous step I have taken. I will take my leave, as I may need some time prepare myself for what comes next.", "close_window",
[]],
[anyone, "lord_start",   [

(check_quest_active, "qst_offer_gift"),
(quest_slot_eq, "qst_offer_gift", slot_quest_target_troop, "$g_talk_troop"),
(quest_slot_eq, "qst_offer_gift", slot_quest_current_state, 2),

(this_or_next|troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_upstanding),
(this_or_next|troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_goodnatured),
(troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_martial),
(store_random_in_range, ":random", 3),
(eq, ":random", 0),

(quest_get_slot, ":giver_troop", "qst_offer_gift", slot_quest_giver_troop),
(str_store_troop_name, s10, ":giver_troop"),
(call_script, "script_troop_get_family_relation_to_troop", ":giver_troop",  "$g_talk_troop"),
##diplomacy start+ change to use script_dplmc_print_subordinate_says_sir_madame_to_s0
(call_script, "script_dplmc_print_subordinate_says_sir_madame_to_s0"),
],
"I received the gift, presented to me through my {s11} {s10}. It was a noble gesture, {s0}, and I regret that we ever quarreled.", "close_window",#diplomacy: changed {sir/my lady} to {s0}
[##diplomacy end+
(call_script, "script_troop_get_relation_with_troop", "$g_talk_troop", "trp_player"),
(store_sub, ":difference", 0, reg0),
(val_add, ":difference", 5),
(val_max, ":difference", 5),
(call_script, "script_troop_change_relation_with_troop", "$g_talk_troop", "trp_player", ":difference"),
(call_script, "script_end_quest", "qst_offer_gift"),
(assign, "$g_leave_encounter", 1),

]],
[anyone,"lord_start",[
(check_quest_active, "qst_offer_gift"),
(quest_slot_eq, "qst_offer_gift", slot_quest_target_troop, "$g_talk_troop"),
(quest_slot_eq, "qst_offer_gift", slot_quest_current_state, 2),

(store_random_in_range, ":random", 3),
(neq, ":random", 0),

(quest_get_slot, ":giver_troop", "qst_offer_gift", slot_quest_giver_troop),
(str_store_troop_name, s10, ":giver_troop"),
(call_script, "script_troop_get_family_relation_to_troop", ":giver_troop",  "$g_talk_troop"),

],
"I received the gift, presented to me through my {s11} {s10}. For {reg4?her:his} sake, I am willing to let bygones be bygones.", "close_window",	[
(call_script, "script_troop_get_relation_with_troop", "$g_talk_troop", "trp_player"),
(store_sub, ":difference", 0, reg0),
(val_max, ":difference", 2),
(call_script, "script_troop_change_relation_with_troop", "$g_talk_troop", "trp_player", ":difference"),
(call_script, "script_end_quest", "qst_offer_gift"),
(assign, "$g_leave_encounter", 1),
]],
[anyone,"lord_start",[
(check_quest_active, "qst_offer_gift"),
(quest_slot_eq, "qst_offer_gift", slot_quest_target_troop, "$g_talk_troop"),
(quest_slot_eq, "qst_offer_gift", slot_quest_current_state, 2),

(this_or_next|troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_quarrelsome),
(this_or_next|troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_debauched),
(troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_selfrighteous),

(quest_get_slot, ":giver_troop", "qst_offer_gift", slot_quest_giver_troop),
(str_store_troop_name, s10, ":giver_troop"),
(call_script, "script_troop_get_family_relation_to_troop", ":giver_troop",  "$g_talk_troop"),

],
"I received the gift, presented to me through my {s11} {s10}. Bah! Do you think you can buy my friendship?", "close_window",	[
(call_script, "script_end_quest", "qst_offer_gift"),
(assign, "$g_leave_encounter", 1),

]],
[anyone,"lord_start",[
(check_quest_active, "qst_offer_gift"),
(quest_slot_eq, "qst_offer_gift", slot_quest_target_troop, "$g_talk_troop"),
(quest_slot_eq, "qst_offer_gift", slot_quest_current_state, 2),

(quest_get_slot, ":giver_troop", "qst_offer_gift", slot_quest_giver_troop),
(str_store_troop_name, s10, ":giver_troop"),
(call_script, "script_troop_get_family_relation_to_troop", ":giver_troop",  "$g_talk_troop"),

],
##diplomacy next line: replaced {reg?she:he} with {reg4?she:he}, set by family relation script
"I received the gift, presented to me through my {s11} {s10}. As dear as {reg4?she:he} is to me, however, I cannot forget our differences.", "close_window",
##diplomacy end+
[
(assign, "$g_leave_encounter", 1),
(call_script, "script_end_quest", "qst_offer_gift"),
]],
[anyone|plyr,"lord_talk",[
(check_quest_active, "qst_denounce_lord"),
(quest_slot_eq, "qst_denounce_lord", slot_quest_giver_troop, "$g_talk_troop"),
(this_or_next|check_quest_succeeded, "qst_denounce_lord"),
(check_quest_failed, "qst_denounce_lord"),
##diplomacy start+ Fixed native mistake (giver/target)
#(quest_get_slot, ":target_troop", "qst_denounce_lord", slot_quest_giver_troop),
(quest_get_slot, ":target_troop", "qst_denounce_lord", slot_quest_target_troop),
##diplomacy end+
(str_store_troop_name, s4, ":target_troop"),
],
"I did as you suggested, and denounced {s4}", "denounce_lord_results"  ,
[
]],
[anyone|plyr,"lord_talk",[
(check_quest_active, "qst_intrigue_against_lord"),
(quest_slot_eq, "qst_intrigue_against_lord", slot_quest_giver_troop, "$g_talk_troop"),

(this_or_next|check_quest_succeeded, "qst_intrigue_against_lord"),
(check_quest_failed, "qst_intrigue_against_lord"),

(quest_get_slot, ":target_troop", "qst_intrigue_against_lord", slot_quest_target_troop),
(str_store_troop_name, s4, ":target_troop"),
(faction_get_slot, ":liege", "$players_kingdom", slot_faction_leader),
(str_store_troop_name, s5, ":liege"),


],
"I did as you asked, and spoke to {s5} about the danger posed by {s4}.", "lord_quest_intrigue_result"  ,
[
]],
[anyone,"lord_quest_intrigue_result",[
(check_quest_succeeded, "qst_intrigue_against_lord"),
##diplomacy start+ Get gender of quest target
(quest_get_slot, ":target_troop", "qst_denounce_lord", slot_quest_target_troop),
(call_script, "script_dplmc_store_troop_is_female", ":target_troop"),
##diplomacy end+
],
##next line, replace "him" with "{reg0?her:him}"
"So we hear. Hopefully now {s5} will think twice before entrusting {reg0?her:him} with any additional fiefs, honors, or offices. We are grateful to you.", "lord_pretalk"  ,
##diplomacy end+
[
(call_script, "script_end_quest", "qst_intrigue_against_lord"),
(quest_set_slot, "qst_intrigue_against_lord", slot_quest_dont_give_again_remaining_days, 30),
(call_script, "script_troop_change_relation_with_troop", "$g_talk_troop", "trp_player", 8),
(add_xp_as_reward, 500),
]],
[anyone,"lord_quest_intrigue_result",[
(check_quest_failed, "qst_intrigue_against_lord"),
],
"So we hear -- but alas, {s5} seems not to have listened. Still, we are grateful to you for trying.", "close_window"  ,
[
(call_script, "script_end_quest", "qst_intrigue_against_lord"),
(quest_set_slot, "qst_intrigue_against_lord", slot_quest_dont_give_again_remaining_days, 30),
#	(call_script, "script_troop_change_relation_with_troop", "$g_talk_troop", "trp_player", 2),
]],
[anyone|plyr,"lord_talk",[#(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 0),
                      (neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
                      (check_quest_active,"qst_lend_companion"),
                      (quest_slot_eq, "qst_lend_companion", slot_quest_giver_troop, "$g_talk_troop"),
                      (store_current_day, ":cur_day"),
                      (quest_get_slot, ":quest_target_amount", "qst_lend_companion", slot_quest_target_amount),
                      (ge, ":cur_day", ":quest_target_amount"),
                      (quest_get_slot, ":quest_target_troop", "qst_lend_companion", slot_quest_target_troop),
                      (str_store_troop_name,s14,":quest_target_troop"),
					  ##diplomacy start+ Replace troop_get_type
                      (call_script, "script_dplmc_store_troop_is_female_reg", ":quest_target_troop", 3), # <- dplmc+ replaced (troop_get_type, reg3, ":quest_target_troop")
					  ##diplomacy end+
                      ],
"I should like {s14} returned to me, {s65}, if you no longer require {reg3?her:his} services.", "lord_lend_companion_end",
[]],
[anyone,"lord_lend_companion_end",[(neg|hero_can_join, "p_main_party")],
"You've too many men in your company already, {playername}. You could not lead any more at the moment.", "lord_pretalk",
[]],
[anyone,"lord_lend_companion_end",[],
"Certainly, {playername}. {reg3?She:He} is a bright {reg3?girl:fellow}, you're a lucky {man/woman} to have such worthy companions.", "lord_pretalk",
[(quest_get_slot, ":quest_target_troop", "qst_lend_companion", slot_quest_target_troop),
(party_add_members, "p_main_party", ":quest_target_troop", 1),
(call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 3),
(add_xp_as_reward, 100),
(call_script, "script_end_quest", "qst_lend_companion"),
(str_store_troop_name,s14,":quest_target_troop"),
##diplomacy start+
(call_script, "script_dplmc_store_troop_is_female_reg", ":quest_target_troop", 3), # <- dplmc+ replaced (troop_get_type, reg3, ":quest_target_troop")
##diplomacy end+
]],
[anyone|plyr,"lord_talk",[(check_quest_active,"qst_collect_debt"),
                      (quest_slot_eq,  "qst_collect_debt", slot_quest_current_state, 0),
                      (quest_get_slot, ":quest_target_troop", "qst_collect_debt", slot_quest_target_troop),
                      (eq,"$g_talk_troop",":quest_target_troop"),
                      (quest_get_slot, ":quest_giver_troop", "qst_collect_debt", slot_quest_giver_troop),
                      (str_store_troop_name,1,":quest_giver_troop")],
"I've come to collect the debt you owe to {s1}.", "lord_ask_to_collect_debt",
[(assign, "$g_convince_quest", "qst_collect_debt")]],
[anyone,"lord_ask_to_collect_debt", [
   (quest_get_slot, ":quest_giver_troop", "qst_collect_debt", slot_quest_giver_troop),
   (call_script, "script_dplmc_store_troop_is_female", ":quest_giver_troop"),
],  "Oh. Well, {s1} did lend me some silver a ways back,\
but I've done {reg0?her:him} many favours in the past and I consider that money as my due payment.", "lord_ask_to_collect_debt_2",[]],
[anyone|plyr,"lord_ask_to_collect_debt_2", [
   (quest_get_slot, ":quest_giver_troop", "qst_collect_debt", slot_quest_giver_troop),
   (call_script, "script_dplmc_store_troop_is_female", ":quest_giver_troop"),
],  "{s1} considers it a debt. {reg0?She:He} asked me to speak to you on {reg0?her:his} behalf.", "convince_begin",[]],
[anyone|plyr,"lord_ask_to_collect_debt_2", [],  "Then I will not press the matter any further.", "lord_pretalk",[]],
[anyone|plyr,"lord_talk",[(check_quest_active,"qst_persuade_lords_to_make_peace"),
                      (quest_get_slot, ":quest_target_troop", "qst_persuade_lords_to_make_peace", slot_quest_target_troop),
                      (quest_get_slot, ":quest_object_troop", "qst_persuade_lords_to_make_peace", slot_quest_object_troop),
                      (this_or_next|eq, ":quest_target_troop", "$g_talk_troop"),
                      (eq, ":quest_object_troop", "$g_talk_troop"),
                      (quest_get_slot, ":quest_target_faction", "qst_persuade_lords_to_make_peace", slot_quest_target_faction),
                      (quest_get_slot, ":quest_object_faction", "qst_persuade_lords_to_make_peace", slot_quest_object_faction),
                      (str_store_faction_name, s12, ":quest_target_faction"),
                      (str_store_faction_name, s13, ":quest_object_faction"),
                      ],
"Please, {s64}, it's time to end this war between {s12} and {s13}.", "lord_ask_to_make_peace",
[(assign, "$g_convince_quest", "qst_persuade_lords_to_make_peace")]],
[anyone,"lord_ask_to_make_peace", [], "Eh? I'm not sure I heard you right, {playername}.\
War is not easily forgotten by either side of the conflict, and I have a very long memory.\
Why should I take any interest in brokering peace with those dogs?", "lord_ask_to_make_peace_2",[]],
[anyone|plyr,"lord_ask_to_make_peace_2", [],  "Perhaps I can talk you into it...", "convince_begin",[]],
[anyone|plyr,"lord_ask_to_make_peace_2", [],  "Never mind, peace can wait for now.", "lord_pretalk",[]],
[anyone|plyr,"lord_talk",
[
(neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
(check_quest_active,"qst_duel_for_lady"),
(neg|check_quest_concluded,"qst_duel_for_lady"),
(quest_slot_eq, "qst_duel_for_lady", slot_quest_target_troop, "$g_talk_troop"),
(quest_get_slot, ":quest_giver_troop", "qst_duel_for_lady", slot_quest_giver_troop),
(str_store_troop_name, s1, ":quest_giver_troop")
],
"I want you to take back your accusations against {s1}.", "lord_challenge_duel_for_lady", []],
[anyone,"lord_challenge_duel_for_lady", [], "What accusations?\
Everyone knows that she beds her stable boys and anyone else she can lay hands on while her husband is away.\
I merely repeat the words of many.", "lord_challenge_duel_for_lady_2",[]],
[anyone|plyr,"lord_challenge_duel_for_lady_2", [
#Add gender alternative, and cultural alternative to "sword"
(call_script, "script_dplmc_print_cultural_word_to_sreg", "$g_talk_troop", DPLMC_CULTURAL_TERM_WEAPON, 0),
], "You will recant these lies, {sirrah/miss}, or prove them against my {s0}!", "lord_challenge_duel",[]],
[anyone|plyr,"lord_challenge_duel_for_lady_2", [], "If you say so...", "lord_pretalk",[]],
[anyone,"lord_challenge_duel",
[
(str_store_string, s15, "str_error__wrong_quest_type"),
(try_begin),
(check_quest_active,"qst_duel_for_lady"),
(neg|check_quest_concluded,"qst_duel_for_lady"),
(quest_slot_eq, "qst_duel_for_lady", slot_quest_target_troop, "$g_talk_troop"),
(str_store_string, s15, "@You are challenging me to a duel? How droll!\
As you wish, {playername}, it will be good sport to bash your head in."),
(else_try),
(check_quest_active,"qst_duel_courtship_rival"),
(neg|check_quest_concluded,"qst_duel_courtship_rival"),
(quest_slot_eq, "qst_duel_courtship_rival", slot_quest_target_troop, "$g_talk_troop"),
(str_store_string, s15, "str_call_me_coward_very_well_you_leave_me_no_choice"),
(try_end),
], "{s15}", "close_window",
[
(call_script, "script_change_player_relation_with_troop", "$g_talk_troop", -15),
(call_script, "script_set_up_duel_with_troop", "$g_talk_troop"),
]],
[anyone|plyr,"lord_talk",[#(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 0),
                      (neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
                      (check_quest_active,"qst_duel_courtship_rival"),
                      (neg|check_quest_concluded,"qst_duel_courtship_rival"),
                      (quest_slot_eq, "qst_duel_courtship_rival", slot_quest_target_troop, "$g_talk_troop"),
                      (quest_get_slot, ":quest_giver_troop", "qst_duel_courtship_rival", slot_quest_giver_troop),
                      (str_store_troop_name, s5, ":quest_giver_troop")],
"Relinquish your suit of {s5}!", "lord_challenge_courtship_rival", []],
[anyone,"lord_challenge_courtship_rival",[], "Or what? Do you intend to duel over a lady? I'll let you know -- our lord frowns on this sort of hot-headed challenge, when every man must stand together against our clan's enemies.", "lord_challenge_courtship_rival_2",[]],
[anyone|plyr,"lord_challenge_courtship_rival_2", [], "Do you fear to fight me?", "lord_challenge_duel",[]],
[anyone|plyr,"lord_challenge_courtship_rival_2", [], "My pardon. I have spoken rashly...", "lord_pretalk",[
(call_script, "script_end_quest", "qst_duel_courtship_rival"),
]],
[anyone|plyr,"lord_talk",[(check_quest_active,"qst_deliver_message"),
                       (quest_get_slot, ":quest_target_troop", "qst_deliver_message", slot_quest_target_troop),
                       (eq,"$g_talk_troop",":quest_target_troop"),
                       (quest_get_slot, ":quest_giver_troop", "qst_deliver_message", slot_quest_giver_troop),
                       (str_store_troop_name,s9,":quest_giver_troop")],
"I bring a message from {s9}.", "lord_message_delivered",
[]],
[anyone,"lord_message_delivered", [
##diplomacy start+
#Replace "him" with "{reg4?her:him}"
(quest_get_slot, ":quest_giver_troop", "qst_deliver_message", slot_quest_giver_troop),
(call_script, "script_dplmc_store_troop_is_female", ":quest_giver_troop"),
(assign, reg4, reg0),
], "Oh? Let me see that...\
Well, well, well! It was good of you to bring me this, {playername}. Take my seal as proof that I've received it,\
 and give my regards to {s9} when you see {reg4?her:him} again.", "lord_pretalk",[
##diplomacy end+
(call_script, "script_end_quest", "qst_deliver_message"),
(quest_get_slot, ":quest_giver", "qst_deliver_message", slot_quest_giver_troop),
(str_store_troop_name,s9,":quest_giver"),
(call_script, "script_change_player_relation_with_troop", ":quest_giver", 1),
(call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 1),
]],
[anyone|plyr,"lord_talk",[(check_quest_active,"qst_deliver_message_to_enemy_lord"),
                      (quest_get_slot, ":quest_target_troop", "qst_deliver_message_to_enemy_lord", slot_quest_target_troop),
                      (eq,"$g_talk_troop",":quest_target_troop"),
                      (quest_get_slot, ":quest_giver_troop", "qst_deliver_message_to_enemy_lord", slot_quest_giver_troop),
                      (str_store_troop_name,s9,":quest_giver_troop")],
"I bring a message from {s9}.", "lord_message_delivered_enemy",
[]],
[anyone,"lord_message_delivered_enemy", [], "Oh? Let me see that...\
Hmmm. It was good of you to bring me this, {playername}. Take my seal as proof that I've received it,\
with my thanks.", "close_window",[
(call_script, "script_end_quest", "qst_deliver_message_to_enemy_lord"),
(quest_get_slot, ":quest_giver", "qst_deliver_message_to_enemy_lord", slot_quest_giver_troop),
(call_script, "script_change_player_relation_with_troop", ":quest_giver", 1),
(call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 1),
(assign, "$g_leave_encounter", 1),
]],
[anyone|plyr,"lord_talk", [(check_quest_active,"qst_deliver_message_to_prisoner_lord"),
                       (quest_slot_eq, "qst_deliver_message_to_prisoner_lord", slot_quest_target_troop, "$g_talk_troop"),
                       (quest_get_slot, ":quest_giver_troop", "qst_deliver_message_to_prisoner_lord", slot_quest_giver_troop),
                       (str_store_troop_name, s11, ":quest_giver_troop")],
"I bring a message from {s11}.", "lord_deliver_message_prisoner",
[
#TODO: Add reward
(call_script, "script_end_quest", "qst_deliver_message_to_prisoner_lord"),
]],
[anyone,"lord_deliver_message_prisoner", [], "Can it be true?\
Oh, thank you kindly, {playername}! You have brought hope and some small ray of light to these bleak walls.\
Perhaps one day I will be able to repay you.", "lord_deliver_message_prisoner_2",[]],
[anyone|plyr,"lord_deliver_message_prisoner_2", [], " 'Twas the least I could do, {s65}.", "lord_deliver_message_prisoner_2a",[]],
[anyone,"lord_deliver_message_prisoner_2a", [], "You've no idea how grateful I am, {playername}. A thousand thanks and more.", "close_window",[]],
[anyone|plyr,"lord_deliver_message_prisoner_2", [], "Worry not, {s65}. You'll have ample opportunity once you are free again.", "lord_deliver_message_prisoner_2b",[]],
[anyone,"lord_deliver_message_prisoner_2b", [], "Hah, of course, {playername}. My eternal thanks go with you.", "close_window",[]],
[anyone|plyr,"lord_talk", [#(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 1),
                       (troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
                       (check_quest_active,"qst_rescue_lord_by_replace"),
                       (quest_slot_eq, "qst_rescue_lord_by_replace", slot_quest_target_troop, "$g_talk_troop"),
                       (neg|check_quest_succeeded, "qst_rescue_lord_by_replace")],
"Fear not, I am here to rescue you.", "lord_rescue_by_replace_offer",[]],
[anyone,"lord_rescue_by_replace_offer", [],
"By God, are you serious? What is your plan?", "lord_rescue_by_replace_offer_2",[]],
[anyone|plyr,"lord_rescue_by_replace_offer_2", [],
"A simple ruse, {s65}. If we exchange garments, I shall take your place here in prison,\
while you make your escape disguised as myself.\
I paid the guards a handsome bribe, with which I am sure they have already purchased half the sake stocks of the nearest temple.\
With some luck they'll soon get so drunk they'd have trouble\
recognising their own mothers, let alone telling one of us from the other.\
At least not until you are safely away.", "lord_rescue_by_replace_offer_3",[]],
[anyone,"lord_rescue_by_replace_offer_3", [],
"Hmm, it might just work... But what of you, my {friend/lady}? The guards won't take kindly to this trickery.\
You may end up spending some time in this cell yourself.", "lord_rescue_by_replace_offer_4",[]],
[anyone|plyr,"lord_rescue_by_replace_offer_4", [],
"Not to worry, {s65}. The place is already starting to grow on me.", "lord_rescue_by_replace_offer_5a",[]],
[anyone|plyr,"lord_rescue_by_replace_offer_4", [],
"I shall be fine as long there is an ample reward waiting at the end.", "lord_rescue_by_replace_offer_5b",[]],
[anyone,"lord_rescue_by_replace_offer_5a",[],
"You are a brave soul indeed. I won't forget this.", "lord_rescue_by_replace_offer_6",[]],
[anyone,"lord_rescue_by_replace_offer_5b",[],
"Of course, my {friend/lady}, of course! Come to me when you have regained your freedom,\
and perhaps I shall be able to repay the debt I owe you.", "lord_rescue_by_replace_offer_6",[]],
[anyone|plyr,"lord_rescue_by_replace_offer_6",[],
"Quickly, {s65}, let us change garments. It is past time you were away from here.", "close_window",
[(call_script, "script_succeed_quest", "qst_rescue_lord_by_replace"),
(quest_get_slot, ":quest_target_troop", "qst_rescue_lord_by_replace", slot_quest_target_troop),
(quest_get_slot, ":quest_target_center", "qst_rescue_lord_by_replace", slot_quest_target_center),
(party_remove_prisoners, ":quest_target_center", ":quest_target_troop", 1),
#(troop_set_slot, ":quest_target_troop", slot_troop_is_prisoner, 0),
(troop_set_slot, ":quest_target_troop", slot_troop_prisoner_of_party, -1),
(assign, "$auto_menu", -1),
(assign, "$capturer_party", "$g_encountered_party"),
(jump_to_menu, "mnu_captivity_rescue_lord_taken_prisoner"),
(finish_mission),
]],
[anyone|plyr,"lord_talk", [#(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 0),
                (neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
                       (eq, "$players_oath_renounced_against_kingdom", "$g_talk_troop_faction"),
                       (str_store_faction_name, s4, "$g_talk_troop_faction"),],
"{s66}, I wish to restore my old oath to {s4}.", "lord_ask_pardon_after_oath_renounced",[]],
[anyone,"lord_ask_pardon_after_oath_renounced",
[
(faction_get_slot, ":faction_leader", "$g_talk_troop_faction", slot_faction_leader),
(neq, ":faction_leader", "$g_talk_troop"),
(str_store_troop_name, s4, ":faction_leader"),
##diplomacy start+
#Replace "his" with "{reg0?hers:his}"
(call_script, "script_dplmc_store_troop_is_female", ":faction_leader"),
], "That is too great a matter for me to decide, {playername}. You should seek out {s4}. Such clemency is {reg0?hers:his} alone to grant or deny.", "lord_pretalk",[]],
[anyone,"lord_ask_pardon_after_oath_renounced",
[
##diplomacy start+ Assign zero (don't use implicit arguments)
#(assign, ":num_centers_captured_by_player"),
(assign, ":num_centers_captured_by_player", 0),
##diplomacy end+
(try_for_range, ":cur_center", walled_centers_begin, walled_centers_end),
 (store_faction_of_party, ":cur_center_faction", ":cur_center"),
 (eq, ":cur_center_faction", "fac_player_supporters_faction"),
 (party_slot_eq, ":cur_center", slot_center_faction_when_oath_renounced, "$g_talk_troop_faction"),
 (val_add, ":num_centers_captured_by_player", 1),
(try_end),
(store_mul, ":peace_score", ":num_centers_captured_by_player", 500),
(store_current_hours, ":cur_hours"),
(val_sub, ":cur_hours", "$players_oath_renounced_begin_time"),
(val_add, ":peace_score", ":cur_hours"),
(try_begin),
 (gt, ":peace_score", 800),
 #Do not agree to give any centers but agree to make peace
 (assign, ":given_center", -1),
 (try_begin),
   (gt, ":peace_score", 1500),
   (try_begin),
     #Agree to give one center
     (eq, "$players_oath_renounced_given_center", 0),
     (store_random_in_range, ":given_center", 0, ":num_centers_captured_by_player"),
   (try_end),
 (else_try),
   (assign, "$players_oath_renounced_given_center", 0),
 (try_end),
 (assign, ":num_centers_written", 0),
 (try_for_range, ":cur_center", walled_centers_begin, walled_centers_end),
   (store_faction_of_party, ":cur_center_faction", ":cur_center"),
   (eq, ":cur_center_faction", "fac_player_supporters_faction"),
   (party_slot_eq, ":cur_center", slot_center_faction_when_oath_renounced, "$g_talk_troop_faction"),
   (try_begin),
     (eq, ":given_center", 0),
     (assign, "$players_oath_renounced_given_center", ":cur_center"),
   (else_try),
     (neq, "$players_oath_renounced_given_center", ":cur_center"),
     (try_begin),
       (eq, ":num_centers_written", 0),
       (str_store_party_name, s17, ":cur_center"),
     (else_try),
       (eq, ":num_centers_written", 1),
       (str_store_party_name, s16, ":cur_center"),
       (str_store_string, s17, "@{s16} and {s17}"),
     (else_try),
       (str_store_party_name, s16, ":cur_center"),
       (str_store_string, s17, "@{!}{s16}, {s17}"),
     (try_end),
     (val_add, ":num_centers_written", 1),
   (try_end),
   (val_sub, ":given_center", 1),
 (try_end),
 (try_begin),
   (eq, ":num_centers_written", 0),#white peace
   (str_store_string, s11, "@Very well, I will accept you back into my ranks, if you're ready to swear your solemn oath once more."),
   (assign, "$players_oath_renounced_terms_state", 1),
 (else_try),
   (str_store_string, s11, "@A pardon will only be possible if you are willing to cede {s17} to me. Do you agree my terms?"),
   (assign, "$players_oath_renounced_terms_state", 2),
 (try_end),
(else_try),
 #Do not agree to make peace
 (str_store_string, s11, "@No. There is no chance of peace between us, I am not interested."),
 (assign, "$players_oath_renounced_terms_state", 0),
(try_end),
], "{s11}.", "lord_ask_pardon_terms",[]],
[anyone|plyr,"lord_ask_pardon_terms",
[(eq, "$players_oath_renounced_terms_state", 0),
],
"As you like, {s65}. I will accept your judgment.", "lord_pretalk",[]],
[anyone|plyr,"lord_ask_pardon_terms",
[(eq, "$players_oath_renounced_terms_state", 0),
],
"A shame, {s65}. A shame.", "lord_pretalk",[]],
[anyone|plyr,"lord_ask_pardon_terms",
[(eq, "$players_oath_renounced_terms_state", 0),
],
"Very well, go and die without me.", "lord_pretalk",[]],
[anyone|plyr,"lord_ask_pardon_terms",
[(eq, "$players_oath_renounced_terms_state", 1),
],
"Aye, I am ready.", "lord_ask_pardon_after_renounce_peace",[]],
[anyone|plyr,"lord_ask_pardon_terms",
[(eq, "$players_oath_renounced_terms_state", 1),
],
"On second thought, no. I don't wish to be in your service again.", "lord_ask_pardon_terms_rejected",[]],
[anyone|plyr,"lord_ask_pardon_terms",
[(eq, "$players_oath_renounced_terms_state", 2),
],
"Aye, I agree to those terms.", "lord_ask_pardon_after_renounce_peace",[]],
[anyone|plyr,"lord_ask_pardon_terms",
[(eq, "$players_oath_renounced_terms_state", 2),
],
"That is too high a price, {s65}. I must decline.", "lord_ask_pardon_terms_rejected",[]],
[anyone,"lord_ask_pardon_after_renounce_peace",
[], "Excellent. Though you strayed from us, {playername}, it gladdens all our hearts that you have found your way back to the right path. I hereby recognize your loyalty to me. Rise once more as an honoured {man/warrior} in my service.", "lord_pretalk",
[
(try_for_range, ":cur_center", walled_centers_begin, walled_centers_end),
 (store_faction_of_party, ":cur_center_faction", ":cur_center"),
 (eq, ":cur_center_faction", "fac_player_supporters_faction"),
 (party_slot_eq, ":cur_center", slot_center_faction_when_oath_renounced, "$g_talk_troop_faction"),
 (neq, ":cur_center", "$players_oath_renounced_given_center"),
 ##diplomacy start+ Apply relation reduction with former town lord
 (party_get_slot, ":town_lord", ":cur_center", slot_town_lord),
 (try_begin),
	#Rationale: since you gain 10 relation for granting a fief, you lose 10 relation for ceding it.
	#This is just a rough temporary measure.  It doesn't take into account villages.
	#Also, some vassals may wish to jump ship to another faction instead of going along with
	#the player.
	(ge, ":town_lord", 1),
	(call_script, "script_change_player_relation_with_troop", ":town_lord", -10),
 (try_end),
 ##diplomacy end+
 (call_script, "script_give_center_to_faction", ":cur_center", "$g_talk_troop_faction"),
(try_end),

(call_script, "script_player_join_faction", "$g_talk_troop_faction"),
(assign, "$player_has_homage", 1),
(call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 3),
]],
[anyone,"lord_ask_pardon_terms_rejected",
[], "Then get out of my sight, traitor! Begone with you, and do not come back!", "close_window",
[
(assign, "$g_leave_encounter", 1),
#TODO: Add relation drop. $players_oath_renounced_begin_time can also be reset to current time for worse conditions in the next conversation.
(call_script, "script_change_player_relation_with_troop", "$g_talk_troop", -5),
]],
[anyone|plyr,"lord_talk", [#(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 0),
                       (neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
                       (lt, "$g_talk_troop_faction_relation", 0),
				##diplomacy start+ Handle when the player is co-ruler of an NPC kingdom
				(assign, ":is_coruler", 0),
				(try_begin),
				   (is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
				   (call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", "$players_kingdom"),
                   (ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
				   (assign, ":is_coruler", 1),
				(try_end),
				##diplomacy end+

                (store_relation, ":players_kingdom_relation", "$g_talk_troop_faction", "$players_kingdom"),

                (this_or_next|ge, ":players_kingdom_relation", 0),
                       (this_or_next|eq, "$players_kingdom", 0),
				  ##diplomacy start+
				  (this_or_next|eq, ":is_coruler", 1),
				  ##diplomacy end+
                  (eq, "$players_kingdom", "fac_player_supporters_faction"),


                       (neq, "$players_oath_renounced_against_kingdom", "$g_talk_troop_faction"),
                       (assign, ":continue", 1),
                       (try_begin),
                         (gt, "$supported_pretender", 0),
                         (eq, "$supported_pretender_old_faction", "$g_talk_troop_faction"),
                         (assign, ":continue", 0),
                       (try_end),
                       (eq, ":continue", 1),
                (is_between, "$g_talk_troop_faction", kingdoms_begin, kingdoms_end),
				##diplomacy start+
				(try_begin),
				   (eq, ":is_coruler", 1),
 			       (assign, "$temp_2", 0x434F52),#is co-ruler
				(else_try),
				   (assign, "$temp_2", 0),
				(try_end),
				##diplomacy end+
                       (str_store_faction_name, s4, "$g_talk_troop_faction"),],
"I wish to make peace with the {s4}.", "lord_ask_pardon",[]],
[anyone,"lord_ask_pardon", [(lt, "$g_talk_troop_relation", -10)], "Do you indeed, {playername}? Then go and trip on your sword. Give us all peace.", "lord_pretalk",[]],
[anyone,"lord_ask_pardon",
[
(faction_slot_eq, "fac_player_supporters_faction", slot_faction_leader, "trp_player"),
(assign, ":has_center", 0),
(try_for_range, ":cur_center", centers_begin, centers_end),
 (store_faction_of_party, ":cur_center_faction", ":cur_center"),
 (eq, ":cur_center_faction", "fac_player_supporters_faction"),
 (assign, ":has_center", 1),
(try_end),
(eq, ":has_center", 1),
(lt, "$player_right_to_rule", 10),

], "{playername}, you are a {lord/lady} without a master, holding lands in your name, with only the barest scrap of a claim to legitimacy.\
No samurai in Japan would accept a lasting peace with you.", "lord_pretalk",[]],
[anyone,"lord_ask_pardon",
[
(assign, ":has_center", 0),
(try_for_range, ":cur_center", centers_begin, centers_end),
 (store_faction_of_party, ":cur_center_faction", ":cur_center"),
 (eq, ":cur_center_faction", "fac_player_supporters_faction"),
 (assign, ":has_center", 1),
(try_end),
##diplomacy start+
(this_or_next|eq, "$temp_2", 0x434F52),#is co-ruler
##diplomacy end+
(eq, ":has_center", 1),
(encountered_party_is_attacker),

], "Make peace when I have you at an advantage? I think not.", "lord_pretalk",[]],
[anyone,"lord_ask_pardon",
[
(faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, "$g_talk_troop"),

(assign, ":has_center", 0),
(try_for_range, ":cur_center", centers_begin, centers_end),
 (store_faction_of_party, ":cur_center_faction", ":cur_center"),
 (eq, ":cur_center_faction", "fac_player_supporters_faction"),
 (assign, ":has_center", 1),
(try_end),
##diplomacy start+
(this_or_next|eq, "$temp_2", 0x434F52),#is co-ruler
##diplomacy end+
(eq, ":has_center", 1),

(call_script, "script_npc_decision_checklist_peace_or_war", "$g_encountered_party_faction", "fac_player_supporters_faction", "trp_player"),
##diplomacy start+ allow the player to negotiate, as they can through a minister
(assign, "$temp", reg0),#<-- the check peace war result
(lt, reg0, -2),#<-- negotiation is impossible at -3 or worse

#Changed this line to make it clearer that negotiation isn't going to happen.
#], "I do not see it as being in my current interest to make peace.", "lord_pretalk",[]],
], "I do not see it as being in my current interest to make peace, and have no interest in negotiations.", "lord_pretalk",[]],
[anyone,"lord_ask_pardon",
[
(faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, "$g_talk_troop"),
(assign, ":check_peace_war", "$temp"),
(lt, ":check_peace_war", 1),#Normally should only be -2, -1, or 0

(assign, ":has_center", 0),
(try_for_range, ":cur_center", centers_begin, centers_end),
 (store_faction_of_party, ":cur_center_faction", ":cur_center"),
 (eq, ":cur_center_faction", "fac_player_supporters_faction"),
 (assign, ":has_center", 1),
(try_end),
##diplomacy start+
(try_begin),
	(eq, "$temp_2", 0x434F52),#is co-ruler
	(assign, ":is_coruler", 1),
(else_try),
	(assign, ":is_coruler", 0),
(try_end),
(this_or_next|eq, ":is_coruler", 1),
##diplomacy end+
(eq, ":has_center", 1),

(call_script, "script_dplmc_get_truce_pay_amount", "fac_player_supporters_faction", "$g_talk_troop_faction", ":check_peace_war"),
(assign, ":money_alone", reg0),
(assign, ":money_and_fief", reg1),

(assign, "$temp", ":money_alone"),
(assign, "$temp_2", ":money_and_fief"),

#Check if there is a valid demanded fief
(assign, reg0, -1),
(try_begin),
	(is_between, "$g_concession_demanded", centers_begin, centers_end),
	(store_faction_of_party, ":concession_faction", "$g_concession_demanded"),
	##diplomacy start+
	(assign, ":alt_faction", "fac_player_supporters_faction"),
	(try_begin),
		(eq, ":is_coruler", 1),
		(assign, ":alt_faction", "$players_kingdom"),
	(try_end),
	(this_or_next|eq, ":concession_faction", ":alt_faction"),
	##diplomacy end+
	(eq, ":concession_faction", "fac_player_supporters_faction"),
	(assign, reg0, 1),
(try_end),

#Either demanding a positive amount of money, or demanding a fief the player has
(this_or_next|ge, ":money_alone", 1),
(eq, reg0, 1),

#Store demand string to s0
(try_begin),
	#Just mon
	(neq, reg0, 1),
	(assign, reg1, ":money_alone"),
	(str_store_string, s0, "str_reg1_denars"),
(else_try),
	#A fief and mon
	(ge, ":money_and_fief", 1),
	(str_store_party_name, s0, "$g_concession_demanded"),
	(assign, reg1, ":money_and_fief"),
	(str_store_string, s1, "str_reg1_denars"),
	(str_store_string, s0, "str_dplmc_s0_and_s1"),
(else_try),
	#Just a fief
	(str_store_party_name, s0, "$g_concession_demanded"),
(try_end),

], "As things stand I do not see it as being in my current interest to make peace, but if you "+\
	"were to hand over {s0} I would be willing to agree to a truce of twenty days.",
"dplmc_lord_ask_pardon_ruler_1",[]],
[anyone,"lord_ask_pardon",
[
(faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, "$g_talk_troop"),
(assign, ":has_center", 0),
(try_for_range, ":cur_center", centers_begin, centers_end),
 (store_faction_of_party, ":cur_center_faction", ":cur_center"),
 (eq, ":cur_center_faction", "fac_player_supporters_faction"),
 (assign, ":has_center", 1),
(try_end),
##diplomacy start+ Handle when the player is co-ruler of an NPC kingdom
(assign, ":is_coruler", 0),
(try_begin),
   (is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
   (call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", "$players_kingdom"),
   (ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
   (assign, ":is_coruler", 1),
   (assign, "$temp_2", 0x434F52),#is co-ruler
(else_try),
   (assign, "$temp_2", 0),
(try_end),
(this_or_next|eq, ":is_coruler", 1),
##diplomacy end+
(eq, ":has_center", 1),
##diplomacy begin
], "Yes... I am weary of fighting you. I could offer you a truce of twenty days. If you keep your word and do not molest my lands and subjects, we may talk again...", "lord_truce_offer",[]],
[anyone|plyr,"lord_truce_offer",
[
##zerilius changes begin
#(call_script, "script_diplomacy_start_peace_between_kingdoms", "$g_encountered_party_faction", "$players_kingdom", 1),
], "I accept. Let us stop making war upon each other, for the time being anyway", "close_window",
[
(call_script, "script_diplomacy_start_peace_between_kingdoms", "$g_encountered_party_faction", "$players_kingdom", 1),
(eq,"$talk_context",tc_party_encounter),
(assign, "$g_leave_encounter", 1),
]],
[anyone|plyr,"lord_truce_offer",
[], "On second thought, such an accord would not be in my interests.", "lord_pretalk",[]],
[anyone,"lord_ask_pardon", [
(neg|faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, "$g_talk_troop"),
(faction_slot_eq, "fac_player_supporters_faction", slot_faction_leader, "trp_player"),
(assign, ":has_center", 0),
(try_for_range, ":cur_center", centers_begin, centers_end),
(store_faction_of_party, ":cur_center_faction", ":cur_center"),
(eq, ":cur_center_faction", "fac_player_supporters_faction"),
(assign, ":has_center", 1),
(try_end),
##diplomacy start+ Handle player is co-ruler of NPC kingdom
(neq, "$temp_2", 0x434F52),#is not co-ruler
##diplomacy end+
(eq, ":has_center", 0),

(store_sub, ":hostility", 4, "$g_talk_troop_faction_relation"),
(val_mul, ":hostility", ":hostility"), #square it
(store_mul, reg16, ":hostility", 10),
(str_store_faction_name, s4, "$g_talk_troop_faction"),
], "Hmm. I could use my considerable influence to arrange a pardon for you, {playername},\
but there are some who see you as an enemy and will not be satisfied unless you pay tribute.\
All in all, you'd need to bring no less than {reg16} mon to make any friends in {s4}.", "lord_ask_pardon_2",[]],
[anyone,"lord_ask_pardon",
[
(faction_get_slot, ":faction_leader", "$g_talk_troop_faction", slot_faction_leader),
(neq, "$g_talk_troop", ":faction_leader"),
(neq, "$g_talk_troop_faction", "fac_dark_knights"), ## Tocan Invasion ##
(str_store_troop_name, s7, ":faction_leader"),
], "I am in no position to offer you anything. You must speak to {s7}.", "lord_pretalk",[]],
[anyone,"lord_ask_pardon",
[
(faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, "$g_talk_troop"),
##diplomacy start+ Handle player is co-ruler of NPC faction
(neq, "$temp_2", 0x434F52),#is not co-ruler
##diplomacy end+
(neg|faction_slot_ge, "fac_player_supporters_faction", slot_faction_leader, 1),
(neq, "$g_talk_troop_faction", "fac_dark_knights"), ## Tocan Invasion ##

(store_sub, ":hostility", 4, "$g_talk_troop_faction_relation"),
(val_mul, ":hostility", ":hostility"), #square it
(store_mul, reg16, ":hostility", 10),

(str_store_faction_name, s4, "$g_talk_troop_faction"),
##diplomacy start+ Next line replace "sume" with "sum"
], "Yes... I have bigger worries than you or your followers. However, you have wronged my subjects, and wrongs demand compensation. For the sum of {reg16} mon, I suppose that I could agree to grant you a pardon. What do you say?", "lord_ask_pardon_2",[
##diplomacy end+
]],
[anyone,"lord_ask_pardon",
[
       (neq, "$g_talk_troop_faction", "fac_dark_knights"), ## Tocan Invasion ##
], "I am sorry. I am in no position to offer you a pardon", "lord_pretalk",[
]],
[anyone,"lord_ask_pardon",
[
       (eq, "$g_talk_troop_faction", "fac_dark_knights"), 
], "Peace? Maybe after we grind you into a fine dust, burn your chattels, and hear the lamentation of your kinsfolk. Then we will give you peace.", "lord_pretalk",[
	]],
[anyone|plyr,"lord_ask_pardon_2", [(store_troop_gold, ":gold","trp_player"),(ge, ":gold", reg16)], "I have the money here. {reg16} mon.", "lord_ask_pardon_tribue_accept",[]],
[anyone|plyr,"lord_ask_pardon_2", [], "I fear I cannot pay that much.", "lord_ask_pardon_tribue_deny",[]],
[anyone,"lord_ask_pardon_tribue_accept", [
(faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, "$g_talk_troop"),
], "Excellent, {playername}.\
I will use this to make amends to those you have wronged, and I will let it be known that you are no longer an enemy of the {s4}.", "close_window",
[
##diplomacy start+ transfer removed gold to bribed lords
(faction_get_slot, ":king", "$g_talk_troop_faction", slot_faction_leader),
(try_begin),
	#if king, take half and split with subjects
	(eq, ":king", "$g_talk_troop"),
	(call_script, "script_dplmc_faction_leader_splits_gold", "$g_talk_troop_faction", reg16),
(else_try),
	#if not king, take half and split with king
	(store_div, ":give_gold", reg16, 2),
	(call_script, "script_dplmc_distribute_gold_to_lord_and_holdings", ":give_gold", "$g_talk_troop"),
	(store_sub, ":give_gold", reg16, ":give_gold"),
	(call_script, "script_dplmc_distribute_gold_to_lord_and_holdings", ":give_gold", ":king"),
(try_end),
##diplomacy end+
(troop_remove_gold, "trp_player", reg16),
(store_relation, ":players_kingdom_relation", "$g_talk_troop_faction", "$players_kingdom"),

(try_begin),
 (this_or_next|eq, "$players_kingdom", 0),
(ge, ":players_kingdom_relation", 0),
 (call_script, "script_set_player_relation_with_faction", "$g_talk_troop_faction", 0),
(try_end),
(assign,"$g_leave_town_outside",1),
(assign, "$g_leave_encounter", 1),
]],
[anyone,"lord_ask_pardon_tribue_accept", [], "Excellent, {playername}.\
I'll use the coin to smooth the feathers of those that can oppose your pardon, and I'm sure that word will soon spread that you are no longer an enemy of {s4}.", "close_window",
[
##diplomacy start+ transfer removed gold to bribed lords
(try_begin),
	(neg|faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, "$g_talk_troop"),
	(store_div, ":gold_to_lord", reg16, 20),#lord takes 5% cut
	(call_script, "script_dplmc_distribute_gold_to_lord_and_holdings", ":gold_to_lord", "$g_talk_troop"),
	(assign, ":gold_to_faction", reg16),#faction splits rest of gold
	(val_sub, ":gold_to_faction", ":gold_to_lord"),
(try_end),
(call_script, "script_dplmc_faction_leader_splits_gold", "$g_talk_troop_faction",
 ":gold_to_faction"),
##diplomacy end+
(troop_remove_gold, "trp_player", reg16),
(store_relation, ":players_kingdom_relation", "$g_talk_troop_faction", "$players_kingdom"),

(try_begin),
 (this_or_next|eq, "$players_kingdom", 0),
(ge, ":players_kingdom_relation", 0),
 (call_script, "script_set_player_relation_with_faction", "$g_talk_troop_faction", 0),
(else_try),
 (call_script, "script_diplomacy_start_peace_between_kingdoms", "$g_talk_troop_faction", "$players_kingdom", 1),
(try_end),
(assign,"$g_leave_town_outside",1),
(assign, "$g_leave_encounter", 1),
]],
[anyone,"lord_ask_pardon_tribue_deny", [], "Then there's nothing I can do for you, {playername}. No silver, no pardon.", "lord_pretalk",[]],
[anyone|plyr,"lord_talk", [(store_partner_quest,":lords_quest"),
                       (ge,":lords_quest",0),
                       ],
"About the task you gave me...", "lord_active_mission_1",[]],
[anyone|plyr,"lord_talk", [#(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 0),
                       ##diplomacy start+
					   (neg|troop_slot_eq, "trp_player", slot_troop_spouse, -1),
					   #There are certain exotic situations where you would want to support marriage
					   #where the spouse slots may not match (for example, certain polygamy implementations).
					   (this_or_next|troop_slot_eq, "$g_talk_troop", slot_troop_spouse, "trp_player"),
					   ##diplomacy end+
                       (troop_slot_eq, "trp_player", slot_troop_spouse, "$g_talk_troop"),
                       ],
"Let us discuss matters related to our household.", "lord_switch_to_spouse",[]],
[anyone,"lord_switch_to_spouse", [
(assign, ":feast_venue", -1),

(try_begin),
(is_between, "$current_town", walled_centers_begin, walled_centers_end),
(this_or_next|party_slot_eq, "$current_town", slot_town_lord, "trp_player"),
   (party_slot_eq, "$current_town", slot_town_lord, "$g_talk_troop"),
(assign, ":feast_venue", "$current_town"),
(else_try),
(try_for_range, ":center", walled_centers_begin, walled_centers_end),
   (eq, ":feast_venue", -1),
   (this_or_next|party_slot_eq, ":center", slot_town_lord, "trp_player"),
      (party_slot_eq, ":center", slot_town_lord, "$g_talk_troop"),
   (assign, ":feast_venue", ":center"),
(try_end),
(is_between, ":feast_venue", walled_centers_begin, walled_centers_end), #unless there's a try/fail, will not do last check

(else_try),
(is_between, "$current_town", walled_centers_begin, walled_centers_end),
(assign, ":feast_venue", "$current_town"),
(try_end),

(neg|is_between, ":feast_venue", walled_centers_begin, walled_centers_end),
##diplomacy start+ load relation text into s0
(call_script, "script_dplmc_print_player_spouse_says_my_husband_wife_to_s0", "$g_talk_troop", 0),
##diplomacy end+
],
#diplomacy start+ either gender PC can marry opposite-gender lords
"Let us wait until we are in a hall, {s0}, as it is difficult to deal with household inventories and such matters in the field.", "lord_pretalk",[]],
[anyone,"lord_switch_to_spouse", #Ediplomacy start+[],
[#load relation text into s0
(call_script, "script_dplmc_print_player_spouse_says_my_husband_wife_to_s0", "$g_talk_troop", 0),
],
#either gender PC can marry opposite-gender lords
"Certainly, {s0}", "spouse_talk",[]],
[anyone|plyr,"lord_talk", [#(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 0),
                       (neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
                       (ge, "$g_talk_troop_faction_relation", 0),
                       (store_partner_quest,":lords_quest"),
                       (lt,":lords_quest",0),
                (neg|faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, "trp_player"),
                (neg|troop_slot_eq, "trp_player", slot_troop_spouse, "$g_talk_troop"),
                #                             (eq,"$g_talk_troop_faction","$players_kingdom")
                       ],
"Do you have any tasks for me?", "lord_request_mission_ask",[]],
[anyone|plyr,"lord_talk",
[
(eq, "$g_talk_troop_faction", "$players_kingdom"),
(eq, "$player_has_homage", 1),
(neg|faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, "trp_player"),
(neg|faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, "$g_talk_troop"),

],
"Do you think we can work together to advance our standings in this clan?", "combined_political_quests",[
(call_script, "script_get_political_quest", "$g_talk_troop"),
(assign, "$political_quest_found", reg0),
(assign, "$political_quest_target_troop", reg1),
(assign, "$political_quest_object_troop", reg2),
]],
[anyone|plyr,"lord_talk", [(le,"$talk_context", tc_party_encounter),
                       (faction_slot_eq, "$players_kingdom", slot_faction_leader, "$g_talk_troop"),
                       (faction_slot_eq, "$players_kingdom", slot_faction_marshall, "trp_player"),
                      ],
"I wish to resign as strategist", "lord_ask_resign_marshalship",[]],
[anyone,"lord_ask_resign_marshalship", [],
"So be it. I shall have to find someone else.", "lord_pretalk",[
(assign, ":faction_no", "$players_kingdom"),
(faction_set_slot, ":faction_no", slot_faction_political_issue, 1), #Appointment of marshal
(store_current_hours, ":hours"),
(val_max, ":hours", 0),
(faction_set_slot, ":faction_no", slot_faction_political_issue_time, ":hours"), #Appointment of marshal

  (faction_get_slot, ":old_marshall", ":faction_no", slot_faction_marshall),
  (try_begin),
    (ge, ":old_marshall", 0),
  (troop_get_slot, ":old_marshall_party", ":old_marshall", slot_troop_leaded_party),
    (party_is_active, ":old_marshall_party"),
    (party_set_marshall, ":old_marshall_party", 0),
  (try_end),

(faction_set_slot, ":faction_no", slot_faction_marshall, -1),

(try_for_range, ":active_npc", active_npcs_begin, active_npcs_end),
   (store_faction_of_troop, ":active_npc_faction", ":active_npc"),
   (eq, ":active_npc_faction", ":faction_no"),
   (troop_set_slot, ":active_npc", slot_troop_stance_on_faction_issue, -1),
(try_end),
(try_begin),
   (eq, "$players_kingdom", ":faction_no"),
   (troop_set_slot, "trp_player", slot_troop_stance_on_faction_issue, -1),
(try_end),
(call_script, "script_add_notification_menu", "mnu_notification_relieved_as_marshal", 0, 0),
]],
[anyone|plyr,"lord_talk", [(le,"$talk_context", tc_party_encounter),
                       (ge, "$g_talk_troop_faction_relation", 0),
                       #(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 0),
                       (neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
                       (faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, "$g_talk_troop"),
                       (neq, "$players_kingdom", "$g_talk_troop_faction"),
                       (store_partner_quest, ":lords_quest"),
                       (neq, ":lords_quest", "qst_join_faction"),
                      ],
"{s66}, I have come to offer you my sword in vassalage!", "lord_ask_enter_service",[]],
[anyone|plyr,"lord_talk", [(le,"$talk_context", tc_party_encounter),
                       (faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, "$g_talk_troop"),
                       (eq, "$players_kingdom", "$g_talk_troop_faction"),
                       (eq, "$player_has_homage", 0),
                       (store_partner_quest, ":lords_quest"),
                       (neq, ":lords_quest", "qst_join_faction"),
                      ],
"{s66}, I wish to become your sworn {man/woman} and fight for your honour.", "lord_ask_enter_service",[]],
[anyone|plyr,"lord_talk", [(le,"$talk_context", tc_party_encounter),
                       (ge, "$g_talk_troop_faction_relation", 0),
                       #(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 0),
                       (neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
                       (faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, "$g_talk_troop"),
                       (eq, "$players_kingdom", "$g_talk_troop_faction"),
                       (eq, "$player_has_homage", 1),
                       ##diplomacy start+
                       #Disable leaving the faction if you're the co-leader.  Writing separate logic
                       #to enable doing that is a low priority.
                       (neg|troop_slot_eq,"trp_player",slot_troop_spouse,"$g_talk_troop"),
                       (neg|troop_slot_eq,"$g_talk_troop",slot_troop_spouse,"trp_player"),
					   (call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", "$g_talk_troop_faction"),
					   (lt, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
                       ##diplomacy end+
                      ],
"{s66}, I wish to be released from my oath to you.", "lord_ask_leave_service",[]],
[anyone|plyr,"lord_talk", [(eq, 1, 0),(le,"$talk_context", tc_party_encounter),(ge, "$g_talk_troop_faction_relation", 0)],
"I have an offer for you.", "lord_talk_preoffer",[]],
[anyone|plyr,"lord_talk", [##diplomacy start+
	                       #Change the requirements.  Now, the player can grant troops to another lord if:
						   # - The player is the faction leader (this used to be the ONLY condition)
						   # - The player is the faction marshall
						   # - The lord is the player's spouse.
						   # - The lord is an affiliated family member.
						   # - The player is a former companion with good relations.
						   #There are additional details, for which you should check script_dplmc_player_can_give_troops_to_troop
					(neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
					(ge, "$g_talk_troop_faction_relation", 0),
					#Check really is leading a party
					(troop_get_slot, ":party_no", "$g_talk_troop", slot_troop_leaded_party),
					(ge, ":party_no", 1),
					(party_get_attached_to, ":cur_attached_party", ":party_no"),
					(lt, ":cur_attached_party", 0),
					#Logic moved to separate script:
					(call_script, "script_dplmc_player_can_give_troops_to_troop", "$g_talk_troop"),
					(ge, reg0, 1),
                    ##diplomacy end+
                       ],
"I want to give some troops to you.", "lord_give_troops",[]],
[anyone,"lord_give_troops", [
	(call_script, "script_party_get_ideal_size", "$g_talk_troop_party"),
	(assign, ":limit", reg0),
	(game_get_reduce_campaign_ai, ":reduce_campaign_ai"),
	(try_begin),
		(le, ":reduce_campaign_ai", 0),#Hard: maximum is 150% of normal size
		(val_mul, ":limit", 3),
		(val_add, ":limit", 1),
		(val_div, ":limit", 2),
		(val_max, ":limit", 100),#or 100 troops, whichever is more
	(else_try),
		(eq, ":reduce_campaign_ai", 1),#Medium: maximum is 200% of normal size
		(val_mul, ":limit", 2),
		(val_max, ":limit", 150),#or 150 troops, whichever is more
	(else_try),
		(ge, ":reduce_campaign_ai", 2),#Easy: maximum is 250% of normal size
		(val_mul, ":limit", 5),
		(val_add, ":limit", 1),
		(val_div, ":limit", 2),
		(val_max, ":limit", 200),#or 200 troops, whichever is more
	(try_end),

	(store_party_size_wo_prisoners, ":party_size", "$g_talk_troop_party"),
	(ge, ":party_size", ":limit"),
],
"I can't accomodate any more {reg65?men:soldiers} right now.  My supply lines are overtaxed as it is.", "lord_pretalk",
[
]],
[anyone,"lord_give_troops", [
	#Same behavior as normal, but print a different message.
	(call_script, "script_party_get_ideal_size", "$g_talk_troop_party"),
	(assign, ":ideal_size", reg0),
	(store_party_size_wo_prisoners, ":party_size", "$g_talk_troop_party"),
	(gt, ":party_size", ":ideal_size"),
	], "I have plenty of soldiers at the moment, but I suppose I could accomodate a few more.", "lord_pretalk",
[
(change_screen_give_members, "$g_talk_troop_party"),
]],
[anyone,"lord_give_troops", [],
"Well, I could use some good soldiers. Thank you.", "lord_pretalk",
[
(change_screen_give_members, "$g_talk_troop_party"),
]],
[anyone|plyr,"lord_talk",
[
(eq, "$g_talk_troop_faction", "$players_kingdom"),
(faction_slot_eq, "$players_kingdom", slot_faction_marshall, "trp_player"),
#(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 0),
(neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
],
"I have a new task for you.", "lord_give_order_ask",[]],
[anyone|plyr,"lord_talk",
[
(eq, "$g_talk_troop_faction", "$players_kingdom"),
(neg|faction_slot_eq, "$players_kingdom", slot_faction_marshall, "trp_player"),
#(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 0),
(neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
],
"May I suggest a course of action?", "lord_give_suggestion_ask",[]],
[anyone,"lord_give_order_ask", [],
"Yes?", "lord_give_order",[]],
[anyone,"lord_give_suggestion_ask", [
(faction_slot_eq, "$players_kingdom", slot_faction_leader, "trp_player"),
],
"I will gladly follow your direction, Oyakata-sama. If you intend to direct an extensive campaign, however, you may also wish to declare yourself our strategist, so there is no cause for confusion.", "lord_give_order",[]],
[anyone,"lord_give_suggestion_ask", [
##diplomacy start+ affiliated family members heed the player
(call_script, "script_dplmc_is_affiliated_family_member", "$g_talk_troop"),
(lt, reg0, 1),
##diplomacy end+
(lt, "$g_talk_troop_effective_relation", 5), #was five
],
"My apologies. I don't know you well enough to take your advice.", "lord_pretalk",[]],
[anyone,"lord_give_suggestion_ask", [
],
"What is it?", "lord_give_order",[
]],
[anyone|plyr,"lord_give_order", [
(faction_slot_eq, "$players_kingdom", slot_faction_marshall, "trp_player"),
],
"Follow me.", "lord_give_order_answer",
[
(assign, "$temp", spai_accompanying_army),
(assign, "$temp_2", "p_main_party"),

(store_current_hours, ":hours"),
(party_set_slot, "$g_talk_troop_party", slot_party_following_orders_of_troop, "trp_kingdom_heroes_including_player_begin"),
(party_set_slot, "$g_talk_troop_party", slot_party_orders_type, "$temp"),
(party_set_slot, "$g_talk_troop_party", slot_party_orders_object, "$temp_2"),
(party_set_slot, "$g_talk_troop_party", slot_party_orders_time, ":hours"),
]],
[anyone|plyr,"lord_give_order", [
(neg|faction_slot_eq, "$players_kingdom", slot_faction_marshall, "trp_player"),
],
"Will you follow me? I have a plan...", "lord_give_order_answer",
[
  (assign, "$temp", spai_accompanying_army),
  (assign, "$temp_2", "p_main_party"),

 (store_current_hours, ":hours"),
 (party_set_slot, "$g_talk_troop_party", slot_party_following_orders_of_troop, "trp_kingdom_heroes_including_player_begin"),
 (party_set_slot, "$g_talk_troop_party", slot_party_orders_type, "$temp"),
 (party_set_slot, "$g_talk_troop_party", slot_party_orders_object, "$temp_2"),
 (party_set_slot, "$g_talk_troop_party", slot_party_orders_time, ":hours"),
]],
[anyone|plyr,"lord_give_order", [
 ##diplomacy start+ also enable these orders as a king or to affiliated family members
 (call_script, "script_dplmc_is_affiliated_family_member", "$g_talk_troop"),
 (this_or_next|ge, reg0, 1),
 (this_or_next|faction_slot_eq, "$players_kingdom", slot_faction_leader,
    "trp_player"),
 ##diplomacy end+
 (faction_slot_eq, "$players_kingdom", slot_faction_marshall, "trp_player"),

],
"Go to...", "lord_give_order_details_ask",
[
  (assign, "$temp", spai_holding_center),
  ]],
[anyone|plyr,"lord_give_order", [
 ##diplomacy start+ also enable these orders as a king or to affiliated family members
 (call_script, "script_dplmc_is_affiliated_family_member", "$g_talk_troop"),
 (this_or_next|ge, reg0, 1),
 (this_or_next|faction_slot_eq, "$players_kingdom", slot_faction_leader,
    "trp_player"),
 ##diplomacy end+
 (faction_slot_eq, "$players_kingdom", slot_faction_marshall, "trp_player"),

],
"Raid around the village of...", "lord_give_order_details_ask",
[
  (assign, "$temp", spai_raiding_around_center),
  ]],
[anyone|plyr,"lord_give_order", [
 ##diplomacy start+ also enable these orders as a king or to affiliated family members
 (call_script, "script_dplmc_is_affiliated_family_member", "$g_talk_troop"),
 (this_or_next|ge, reg0, 1),
 (this_or_next|faction_slot_eq, "$players_kingdom", slot_faction_leader,
    "trp_player"),
 ##diplomacy end+
 (faction_slot_eq, "$players_kingdom", slot_faction_marshall, "trp_player"),
],
"Patrol around...", "lord_give_order_details_ask",
[
  (assign, "$temp", spai_patrolling_around_center),
  ]],
[anyone|plyr,"lord_give_order", [
    (party_slot_eq, "$g_talk_troop_party", slot_party_ai_state, spai_besieging_center),
     (party_get_slot, ":ai_object", "$g_talk_troop_party", slot_party_ai_object),
   (party_slot_eq, ":ai_object", slot_center_is_besieged_by, "$g_talk_troop_party"),
   (party_slot_eq, ":ai_object", slot_village_state, svs_under_siege),
   (str_store_party_name, s11, ":ai_object"),
   ],
"Together, you and I can take {s11}. You should assault immediately...", "lord_give_order_assault",
[
 #for this one and another one, if the $g_talk_troop is a _t
#     (assign, "$temp", spai_patrolling_around_center),
  ]],
[anyone|plyr,"lord_give_order", [
 (neg|faction_slot_eq, "$players_kingdom", slot_faction_marshall, "trp_player"), #not an order,  only a suggestion

],
"We are under attack, but the enemy can be repulsed. You should ride towards...", "lord_give_order_details_ask",
[
  (assign, "$temp", spai_patrolling_around_center),
  ]],
[anyone|plyr,"lord_give_order", [
 (faction_slot_eq, "$g_talk_troop_faction", slot_faction_marshall, "$g_talk_troop"),

],
"We are under attack, but the enemy can be repulsed. You should assemble the army and march to...", "lord_give_order_details_ask",
[
  (assign, "$temp", spai_patrolling_around_center),
  ]],
[anyone,"lord_give_order_assault", [
   (party_get_slot, ":ai_object", "$g_talk_troop_party", slot_party_ai_object),
   (party_get_slot, ":besieging_party", ":ai_object", slot_center_is_besieged_by),
     (neq, ":besieging_party", "$g_talk_troop_party"),
   (party_stack_get_troop_id, ":siege_commander", ":besieging_party", 0),
   (str_store_troop_name, s4, ":siege_commander"),
   (troop_get_type, reg4, ":siege_commander"),
   ##diplomacy start+ Override reg4
   (assign, reg4, 0),
   (try_begin),
	(call_script, "script_cf_dplmc_troop_is_female", ":siege_commander"),
	(assign, reg4, 1),
   (try_end),
   ##diplomacy end+
   ],
"{s4} is directing this siege. I suggest you speak to {reg4?her:him}", "lord_pretalk",
[]],
[anyone,"lord_give_order_assault", [
 (party_get_slot, ":ai_object", "$g_talk_troop_party", slot_party_ai_object),
 (party_get_slot, ":siege_begun", ":ai_object", slot_center_siege_begin_hours),
(store_current_hours, ":cur_hour"),
(store_sub, ":hours_of_siege", ":cur_hour", ":siege_begun"),

(try_begin),
   (assign, ":hours_required", 9),
(try_end),
(val_sub, ":hours_required", ":hours_of_siege"),
(gt, ":hours_required", 0),
(try_begin),
   (gt, ":hours_required", 1),
   (assign, reg3, ":hours_required"),
   (str_store_string, s11, "str_reg3_hours"),
(else_try),
   (str_store_string, s11, "str_hour"),
(try_end),
],
"Our preparations are not yet ready. We need another {s11}", "lord_pretalk",
[
  ]],
[anyone,"lord_give_order_assault", [
],
"Very well -- to the walls!", "close_window",
[
 (party_get_slot, ":ai_object", "$g_talk_troop_party", slot_party_ai_object),
(call_script, "script_begin_assault_on_center", ":ai_object"),

(party_set_slot, "$g_talk_troop_party", slot_party_under_player_suggestion, spai_besieging_center),
 (assign, "$g_leave_encounter", 1),

  ]],
[anyone|plyr,"lord_give_order", [
 (neg|faction_slot_eq, "$players_kingdom", slot_faction_marshall, "trp_player"), #not an order,  only a suggestion
],
"There is a fortress which can easily be taken. Go to..", "lord_give_order_details_ask",
[
  (assign, "$temp", spai_besieging_center),
  ]],
[anyone|plyr,"lord_give_order", [
#    (neg|faction_slot_eq, "$players_kingdom", slot_faction_marshall, "trp_player"),
],
"The enemy is coming in force. Flee in the direction of...", "lord_give_order_details_ask",
[
  (assign, "$temp", spai_retreating_to_center),
  ]],
[anyone|plyr,"lord_give_order",
[
(faction_slot_eq, "$players_kingdom", slot_faction_marshall, "trp_player"),
#    (neg|troop_slot_eq, "$g_talk_troop", slot_troop_player_order_state, spai_undefined),
  ],
"I won't need you for some time. You are free to do as you like.", "lord_give_order_stop",
[]],
[anyone|plyr,"lord_give_order",
[
(neg|faction_slot_eq, "$players_kingdom", slot_faction_marshall, "trp_player"),
(party_slot_eq, "$g_talk_troop_party", slot_party_ai_state, spai_accompanying_army),
(party_slot_eq, "$g_talk_troop_party", slot_party_ai_object, "p_main_party"),
  ],
"You no longer need to accompany me.", "lord_give_order_stop",
[]],
[anyone|plyr,"lord_give_order", [],
"Never mind.", "lord_pretalk",
[]],
[anyone,"lord_give_order_details_ask", [
 (neg|faction_slot_eq, "$players_kingdom", slot_faction_marshall, "trp_player"),
##diplomacy start+ Add support for companion personalities
(call_script, "script_dplmc_get_troop_morality_value", "$g_talk_troop", tmt_aristocratic),
(this_or_next|ge, reg0, 1),
##diplomacy end+
(troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_martial),
(eq, "$temp", spai_retreating_to_center),

],
"It is not my way to turn tail and run, without even laying eyes on the enemy.", "lord_pretalk",[]],
[anyone,"lord_give_order_details_ask", [
 (neg|faction_slot_eq, "$players_kingdom", slot_faction_marshall, "trp_player"),
(troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_debauched),
(eq, "$temp", spai_besieging_center),

],
"You want me to shed my blood outside a fortress while others stand by and watch? I think not.", "lord_pretalk",[]],
[anyone,"lord_give_order_details_ask", [],
"Where?", "lord_give_order_details",[]],
[anyone|plyr|repeat_for_parties, "lord_give_order_details",
[
  (store_repeat_object, ":party_no"),
  (store_faction_of_party, ":party_faction", ":party_no"),
  (store_relation, ":relation", ":party_faction", "$players_kingdom"),
  (assign, ":continue", 0),
  (try_begin),
    (this_or_next|eq, "$temp", spai_retreating_to_center),
      (eq, "$temp", spai_holding_center),
    (try_begin),
      (this_or_next|party_slot_eq, ":party_no", slot_party_type, spt_castle),
      (party_slot_eq, ":party_no", slot_party_type, spt_town),
      (eq, ":party_faction", "$players_kingdom"),
      (assign, ":continue", 1),
    (try_end),
  (else_try),
    (eq, "$temp", spai_raiding_around_center),
    (try_begin),
      (party_slot_eq, ":party_no", slot_party_type, spt_village),
      (lt, ":relation", 0),
      (assign, ":continue", 1),
    (try_end),
  (else_try),
    (eq, "$temp", spai_besieging_center),
    (try_begin),
      (this_or_next|party_slot_eq, ":party_no", slot_party_type, spt_castle),
      (party_slot_eq, ":party_no", slot_party_type, spt_town),
    (party_slot_eq, ":party_no", slot_center_is_besieged_by, -1),
      (lt, ":relation", 0),
      (assign, ":continue", 1),
    (try_end),
  (else_try),
    (eq, "$temp", spai_patrolling_around_center),
    (try_begin),
      (eq, ":party_faction", "$players_kingdom"),
      (is_between, ":party_no", centers_begin, centers_end),
      (assign, ":continue", 1),
   (else_try),
      (is_between, ":party_no", centers_begin, centers_end),
    (store_distance_to_party_from_party, ":distance", ":party_no", "p_main_party"),
    (le, ":distance", 25),
      (assign, ":continue", 1),
    (try_end),
  (try_end),
  (eq, ":continue", 1),
  (neq, ":party_no", "$g_encountered_party"),
  (str_store_party_name, s1, ":party_no")],
"{s1}", "lord_give_order_answer",
[
  (store_repeat_object, "$temp_2"),
  (store_current_hours, ":hours"),
  (party_set_slot, "$g_talk_troop_party", slot_party_following_orders_of_troop, "trp_kingdom_heroes_including_player_begin"),
  (party_set_slot, "$g_talk_troop_party", slot_party_orders_type, "$temp"),
  (party_set_slot, "$g_talk_troop_party", slot_party_orders_object, "$temp_2"),
  (party_set_slot, "$g_talk_troop_party", slot_party_orders_time, ":hours"),
]],
[anyone|plyr, "lord_give_order_details",
[], "Never mind.", "lord_pretalk",[]],
[anyone,"lord_give_order_stop", [],
"All right. I will stop here.", "lord_pretalk",
[
  (party_set_slot, "$g_talk_troop_party", slot_party_orders_type, spai_undefined),
  (party_set_slot, "$g_talk_troop_party", slot_party_orders_object, -1),
  #this is not set above, so should be set here
  (store_current_hours, ":hours"),
  (val_sub, ":hours", 36),
  (val_max, ":hours", 0),

  (party_set_slot, "$g_talk_troop_party", slot_party_following_orders_of_troop, "trp_kingdom_heroes_including_player_begin"),
  (party_set_slot, "$g_talk_troop_party", slot_party_orders_type, spai_undefined),
  (party_set_slot, "$g_talk_troop_party", slot_party_orders_object, -1),
  (party_set_slot, "$g_talk_troop_party", slot_party_orders_time, ":hours"),

  #same variable as above
  (troop_get_slot, ":party_no", "$g_talk_troop", slot_troop_leaded_party),
  (try_begin),
    (gt, ":party_no", 0),
    (call_script, "script_party_set_ai_state", ":party_no", spai_undefined, -1),
    (party_set_slot, ":party_no", slot_party_commander_party, -1),
  (try_end),
]],
[anyone,"lord_give_order_answer",
[
  (eq, "$temp", spai_accompanying_army),
  ##diplomacy start+ affiliated family members heed the player
  (call_script, "script_dplmc_is_affiliated_family_member", "$g_talk_troop"),
  (lt, reg0, 1),
  ##diplomacy end+
  (neg|faction_slot_eq, "$players_kingdom", slot_faction_marshall, "trp_player"),
  (neg|faction_slot_eq, "$players_kingdom", slot_faction_leader, "trp_player"),

  (call_script, "script_troop_get_player_relation", "$g_talk_troop"),
  (assign, ":player_relation", reg0),

  (troop_get_slot, ":troop_renown", "$g_talk_troop", slot_troop_renown),
  (troop_get_slot, ":player_renown", "trp_player", slot_troop_renown),
  ##diplomacy start+
  (try_begin),
    #prejudice mode: high
    (lt, "$g_disable_condescending_comments", 0),
    (neq, reg65, "$character_gender"),

    (call_script, "script_cf_dplmc_faction_has_bias_against_gender", "$g_talk_troop_faction", "$character_gender"),

	(neg|troop_slot_ge, "$g_talk_troop", slot_lord_reputation_type, lrep_roguish),#non-noble or kingdom lady
	(neg|troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_cunning),
	#gekokujo 3.0 microfactions! include fort companions start
	#(neg|is_between, "$g_talk_troop", companions_begin, companions_end),
	(neg|is_between, "$g_talk_troop", companions_begin, fort_companions_end),
	#gekokujo 3.0 microfactions! include fort companions end

    (val_div, ":player_renown", 2),
  (try_end),
  ##diplomacy end+
  #(val_mul, ":troop_renown", 3),
  #(val_div, ":troop_renown", 4),
  #(this_or_next|lt, ":player_renown", ":troop_renown"),
  #(lt, ":player_relation", 0),

  (store_skill_level, ":player_persuasion_level", "skl_persuasion", "trp_player"),
  (store_div, ":player_relation_div_5", ":player_relation", 5),
  (val_min, ":player_relation_div_5", 10),
  (store_add, ":player_persuasion_power", ":player_relation_div_5", ":player_persuasion_level"),

  (store_sub, ":needed_lowest_renown", 20, ":player_persuasion_power"),
  (val_mul, ":needed_lowest_renown", ":troop_renown"),
  (val_div, ":needed_lowest_renown", 10),

  (this_or_next|lt, ":player_renown", ":needed_lowest_renown"),
  (lt, ":player_relation", 0),
],
"That would hardly be proper. It would be more appropriate for you to follow me instead. Did you have any other ideas?", "lord_give_order",
[
  (party_set_slot, "$g_talk_troop_party", slot_party_following_orders_of_troop, 0),
  (party_set_slot, "$g_talk_troop_party", slot_party_orders_type, 0),
  (party_set_slot, "$g_talk_troop_party", slot_party_orders_object, 0),
  (party_set_slot, "$g_talk_troop_party", slot_party_orders_time, 0),
]],
[anyone,"lord_give_order_answer",
[
 (call_script, "script_npc_decision_checklist_party_ai", "$g_talk_troop"),

(eq, reg0, "$temp"),
(eq, reg1, "$temp_2"),

 (str_clear, s12),
(try_begin),
   (neg|faction_slot_eq, "$g_talk_troop_faction", slot_faction_marshall, "trp_player"),
   (neg|faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, "trp_player"),
   (str_store_string, s12, "str_but_if_this_goes_badly"),
(try_end),
],
"All right. I will do that.{s12}", "lord_pretalk",
[
  (call_script, "script_party_set_ai_state", "$g_talk_troop_party", "$temp", "$temp_2"),
  (str_clear, s12),
  (try_begin),
    (neg|faction_slot_eq, "$g_talk_troop_faction", slot_faction_marshall, "trp_player"),
    (neg|faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, "trp_player"),
    (str_store_string, s12, "str_but_if_this_goes_badly"),
  (try_end),
  #Set courage and aggressiveness in party_set_ai_astate
  (assign, "$g_leave_encounter", 1),
]],
[anyone,"lord_give_order_answer", [],
"I am sorry. I need to attend my own business at the moment.", "lord_pretalk",
[
  (call_script, "script_npc_decision_checklist_party_ai", "$g_talk_troop"),
  (call_script, "script_party_set_ai_state", "$g_talk_troop_party", reg0, reg1),
]],
[anyone,"lord_start", [],
"What is it?", "lord_talk",[]],
[anyone|plyr,"lord_talk",
[
  (eq, "$g_talk_troop_faction", "$players_kingdom"),
  (faction_slot_eq, "$players_kingdom", slot_faction_marshall, "trp_player"),
  #(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 0),
  (neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
  (this_or_next|faction_slot_eq, "$players_kingdom", slot_faction_ai_state, sfai_default),
  (faction_slot_eq, "$players_kingdom", slot_faction_ai_state, sfai_feast),
],
"I want to start a new campaign. Let us assemble the army here.", "lord_give_order_call_to_arms_verify",
[]],
[anyone,"lord_give_order_call_to_arms_verify", [],
"You wish to summon all lords for a new campaign?", "lord_give_order_call_to_arms_verify_2",[]],
[anyone|plyr,"lord_give_order_call_to_arms_verify_2", [], "Yes. We must gather all our forces before we march on the enemy.", "lord_give_order_call_to_arms",[]],
[anyone|plyr,"lord_give_order_call_to_arms_verify_2", [], "On second thought, it won't be necessary to summon everyone.", "lord_pretalk",[]],
[anyone,"lord_give_order_call_to_arms",
[],
"All right then. I will send messengers and tell everyone to come here.", "lord_pretalk",
[
 (assign, "$player_marshal_ai_state", sfai_gathering_army),
 (assign, "$player_marshal_ai_object", "p_main_party"),
  (call_script, "script_decide_faction_ai", "$players_kingdom"),
 (assign, "$g_recalculate_ais", 1),
  ]],
[anyone|plyr,"lord_talk",
[
  (eq, "$g_talk_troop_faction", "$players_kingdom"),
  (faction_slot_eq, "$players_kingdom", slot_faction_marshall, "trp_player"),
  #(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 0),
  (neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
  (neg|faction_slot_eq, "$players_kingdom", slot_faction_ai_state, sfai_default),
  (neg|faction_slot_eq, "$players_kingdom", slot_faction_ai_state, sfai_feast),
  ],
"I want to end the campaign and let everyone return home.", "lord_give_order_disband_army_verify", []],
[anyone,"lord_give_order_disband_army_verify", [],
"You want to end the current campaign and release all lords from duty?", "lord_give_order_disband_army_2",[]],
[anyone|plyr,"lord_give_order_disband_army_2", [], "Yes. We no longer need all our forces here.", "lord_give_order_disband_army",[]],
[anyone|plyr,"lord_give_order_disband_army_2", [], "On second thought, it will be better to stay together for now.", "lord_pretalk",[]],
[anyone,"lord_give_order_disband_army",
[],
"All right. I will let everyone know that they are released from duty.", "lord_pretalk",
[
  (assign, "$player_marshal_ai_state", sfai_default),
 (assign, "$player_marshal_ai_object", -1),
  (call_script, "script_decide_faction_ai", "$players_kingdom"),
  (assign, "$g_recalculate_ais", 1),
  ]],
[anyone|plyr,"lord_talk", [
 (ge,"$g_encountered_party_relation",0),
 (neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
],
"I wish to ask you something.", "lord_talk_ask_something",[]],
[anyone,"lord_talk_ask_something", [],
"Aye? What is it?", "lord_talk_ask_something_2",[]],
[anyone|plyr,"lord_talk_ask_something_2",
    [(neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
	 (ge, "$g_talk_troop_effective_relation", 0),
     (neg|troop_slot_eq, "$g_talk_troop", slot_troop_playerparty_history, dplmc_pp_history_nonplayer_entry),
	 #gekokujo 3.0 microfactions! include fort companions start
     #(this_or_next|is_between, "$g_talk_troop", companions_begin, companions_end),
     (this_or_next|is_between, "$g_talk_troop", companions_begin, fort_companions_end),
	 #gekokujo 3.0 microfactions! include fort companions end
     (is_between, "$g_talk_troop", pretenders_begin, pretenders_end),
],
"Have your skills increased since the days when we were travelling companions?", "lord_talk_ask_skill",[]],
[anyone,"lord_talk_ask_skill", [], "Let me show you...", "lord_pretalk",[(change_screen_view_character)]],
[anyone,"lord_talk_ask_something_again", [],
"Is there anything else?", "lord_talk_ask_something_2",[]],
[anyone|plyr,"lord_talk_ask_something_2", [#(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 0),
                                                   (neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
],
"I want to know the location of someone.", "lord_talk_ask_location",[]],
[anyone|plyr,"lord_talk_ask_something_2", [
 (neg|troop_slot_eq, "$g_talk_troop", slot_troop_leaded_party, -1)
],
"What are you and your men doing?", "lord_tell_objective",[
(party_get_slot, ":ai_behavior", "$g_talk_troop_party", slot_party_ai_state),
(party_get_slot, ":ai_object", "$g_talk_troop_party", slot_party_ai_object),

(try_begin),
   (eq, "$cheat_mode", 1),
   (party_get_ai_initiative, reg4, "$g_talk_troop_party"),
   (party_get_helpfulness, reg5, "$g_talk_troop_party"),
   (display_message, "@{!}DEBUG : Initiative {reg4}, helpfulness {reg5}"),
(try_end),

 (str_clear, s14),
 (str_clear, s15),
 (str_clear, s16),

 (try_begin),
  (call_script, "script_npc_decision_checklist_party_ai", "$g_talk_troop"),
  (eq, reg0, ":ai_behavior"),
  (eq, reg1, ":ai_object"),
(else_try),
  (call_script, "script_party_set_ai_state", "$g_talk_troop_party", reg0, reg1),
   (str_store_string, s14, "str_however_circumstances_have_changed_since_we_made_that_decision_and_i_may_reconsider_shortly_s16"),
  (try_begin),
   (ge, "$cheat_mode", 1),
   (display_message, "@{!}DEBUG -- ai behavior: {reg0}, ai object: {reg1}"),
  (try_end),
(try_end),
]],
[anyone|plyr,"lord_talk_ask_something_2", [
#(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 0),
(neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),

],
"What is the clan doing?", "lord_talk_ask_about_strategy",[]],
[anyone,"lord_talk_ask_about_strategy", [
 (eq, "$players_kingdom", "$g_talk_troop_faction"),
(faction_slot_eq, "$g_talk_troop_faction", slot_faction_marshall, "trp_player"),
(neg|faction_slot_eq, "$g_talk_troop_faction", slot_faction_ai_state, sfai_feast),
],
"You should decide that, as you are the strategist.", "lord_pretalk",[]],
[anyone|plyr,"lord_talk_ask_something_2", [#(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 0),
                               (neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
],
"How goes the war?", "lord_talk_ask_about_war",[]],
[anyone|plyr,"lord_talk_ask_something_2",[
(check_quest_active, "qst_formal_marriage_proposal"),
(neg|check_quest_failed, "qst_formal_marriage_proposal"),
(neg|check_quest_succeeded, "qst_formal_marriage_proposal"),

 (neg|troop_slot_ge, "trp_player", slot_troop_spouse, active_npcs_begin),

(quest_slot_eq, "qst_formal_marriage_proposal", slot_quest_target_troop, "$g_talk_troop"),
(quest_get_slot, ":bride", "qst_formal_marriage_proposal", slot_quest_giver_troop),

(str_store_troop_name, s10, ":bride"),
(call_script, "script_troop_get_family_relation_to_troop", ":bride", "$g_talk_troop"),

(call_script, "script_troop_get_relation_with_troop", "trp_player", ":bride"),

(try_begin),
   (gt, reg0, 20),
   (str_store_string, s19, "str_i_wish_to_marry_your_s11_s10_i_ask_for_your_blessing"),
(else_try),
   (str_store_string, s19, "str_i_wish_to_marry_your_s11_s10_i_ask_for_your_help"),
(try_end),

],
 "{s19}", "lord_marriage_permission",
[

]],
[anyone|plyr,"lord_talk_ask_something_2",
   [(le,"$talk_context", tc_party_encounter),
    #(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 0),
    (neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
    (eq, "$players_kingdom", "$g_talk_troop_faction"),
    (this_or_next|eq, "$player_has_homage", 1),
    (faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, "trp_player"),
    (str_store_string, s19, "str_dplmc_fief_exchange_ask_interest"),
    ],
     "{s19}", "dplmc_lord_ask_exchange_fief_1",
    [],
],
[anyone,"lord_marriage_permission", [
(neg|troop_slot_eq, "$g_talk_troop", slot_lord_granted_courtship_permission, 1),
],
"Great heaven, man -- if I haven't given you permission to see her, do you think I'm going to give you permission to marry her?", "lord_pretalk",[
(call_script, "script_fail_quest", "qst_formal_marriage_proposal"),
(call_script, "script_end_quest", "qst_formal_marriage_proposal"),
]],
[anyone,"lord_marriage_permission", [
(troop_slot_eq, "$g_talk_troop", slot_lord_granted_courtship_permission, 1),
(quest_get_slot, ":bride", "qst_formal_marriage_proposal", slot_quest_giver_troop),
(call_script, "script_troop_get_relation_with_troop", "trp_player", ":bride"),
(lt, reg0, 20),
(neg|troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_debauched),
(neg|troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_selfrighteous),
(neg|troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_quarrelsome),

(call_script, "script_troop_get_family_relation_to_troop", ":bride", "$g_talk_troop"),
],
"It is not my way to push my {s11} to marry against her will or her better judgment", "lord_pretalk",[
(call_script, "script_fail_quest", "qst_formal_marriage_proposal"),
(call_script, "script_end_quest", "qst_formal_marriage_proposal"),

]],
[anyone,"lord_marriage_permission", [
(troop_slot_eq, "$g_talk_troop", slot_lord_granted_courtship_permission, 1),
(quest_get_slot, ":bride", "qst_formal_marriage_proposal", slot_quest_giver_troop),
(call_script, "script_troop_get_relation_with_troop", "trp_player", ":bride"),
(lt, reg0, 20),
(assign, ":highest_competitor_score", "$g_talk_troop_relation"),
(try_for_range, ":competitor", lords_begin, lords_end),
   (this_or_next|troop_slot_eq, ":competitor", slot_troop_love_interest_1, ":bride"),
   (this_or_next|troop_slot_eq, ":competitor", slot_troop_love_interest_2, ":bride"),
      (troop_slot_eq, ":competitor", slot_troop_love_interest_3, ":bride"),
   (call_script, "script_troop_get_relation_with_troop", "$g_talk_troop", ":competitor"),
   (gt, reg0, ":highest_competitor_score"),
   (assign, ":highest_competitor_score", reg0),

   (str_store_troop_name, s12, ":competitor"),
(try_end),
(gt, ":highest_competitor_score", "$g_talk_troop_relation"),
(call_script, "script_troop_get_family_relation_to_troop",  ":bride", "$g_talk_troop"),

],
"Sorry -- I'm not going to make my {s11} marry you, when I'd rather see her married to {s12}", "lord_pretalk",[
(call_script, "script_fail_quest", "qst_formal_marriage_proposal"),
(call_script, "script_end_quest", "qst_formal_marriage_proposal"),
]],
[anyone,"lord_marriage_permission", [
(quest_get_slot, ":bride", "qst_formal_marriage_proposal", slot_quest_giver_troop),
(str_store_troop_name, s11, ":bride"),
],
"Splendid news, my young man -- I shall be proud to have you in our family. Now, let us talk the terms of the marriage. As per our custom, the two of us must make sure that {s11} has sufficient finances to support herself, in the event of any unforeseen circumstances..", "lord_marriage_permission_endowment",[
 (troop_get_slot, ":player_renown", "trp_player", slot_troop_renown),
 (troop_get_slot, ":guardian_renown", "$g_talk_troop", slot_troop_renown),

(store_mul, "$marriage_dowry", ":player_renown", 20),
(val_min, "$marriage_dowry", 20000),

(store_mul, "$marriage_dower", ":guardian_renown", 20),
(val_min, "$marriage_dower", 20000),
]],
[anyone,"lord_marriage_permission_endowment", [
(assign, reg3, "$marriage_dower"),
(assign, reg4, "$marriage_dowry"),
],
"I would say that, taking into consideration the prestige of our two houses, that you can provide a dower of {reg3} mon, while I will supply a dowry of {reg4} mon. This shall be her ladyship's property, as a security, lest for any reason you are unable to provide for her. What say you to that?", "lord_marriage_permission_endowment_answer",[
]],
[anyone|plyr,"lord_marriage_permission_endowment_answer", [
(store_troop_gold, ":gold", "trp_player"),
(ge, ":gold", "$marriage_dower"),
],
"Very well -- so let it be.", "lord_marriage_permission_engagement_date",[
]],
[anyone|plyr,"lord_marriage_permission_endowment_answer", [],
"I cannot afford that right now.", "lord_marriage_permission_endowment_answer_delay",[
]],
[anyone|plyr,"lord_marriage_permission_endowment_answer", [
(eq, 1, 0),
],
"That is too much to pay.", "lord_marriage_permission_endowment_answer_no",[
]],
[anyone,"lord_marriage_permission_endowment_answer_no", [],
"Well. I cannot in all decency allow my daughter to marry without some security, can I? Let me know if you change your mind.", "close_window",[
(assign, "$g_leave_encounter", 1),
]],
[anyone,"lord_marriage_permission_engagement_date", [
(quest_get_slot, ":bride", "qst_formal_marriage_proposal", slot_quest_giver_troop),
(call_script, "script_get_kingdom_lady_social_determinants", ":bride"),
(assign, ":venue", reg1),
(is_between, ":venue", walled_centers_begin, walled_centers_end),
(party_slot_eq, ":venue", slot_village_state, svs_normal),
(str_store_party_name, s24, ":venue"),
],
"Splendid! You two may now consider yourselves offically betrothed. Very well -- I shall plan to hold a great feast in {s24}, as soon as circumstances permit. We will be sure to notify you when the day comes.", "close_window",
[
(quest_get_slot, ":bride", "qst_formal_marriage_proposal", slot_quest_giver_troop),
(troop_set_slot, "trp_player", slot_troop_betrothed, ":bride"),
(troop_set_slot, ":bride", slot_troop_betrothed, "trp_player"),

(call_script, "script_end_quest", "qst_formal_marriage_proposal"),


(troop_remove_gold, "trp_player", "$marriage_dower"),
##diplomacy start+ give this gold to the lady.  this will be relevant if she ever becomes a lord.
#(troop_add_gold, ":bride", "$marriage_dower"),
##diplomacy end+
(call_script, "script_get_kingdom_lady_social_determinants", ":bride"),
(assign, ":venue", reg1),

(str_store_troop_name, s3, ":bride"),
(str_store_troop_name, s4, "$g_talk_troop"),
(str_store_party_name, s5, ":venue"),

(setup_quest_text, "qst_wed_betrothed"),
(str_store_string, s2, "str_you_plan_to_marry_s3_at_a_feast_hosted_by_s4_in_s5_you_should_be_notifed_of_the_feast_as_soon_as_it_is_held"),

(call_script, "script_start_quest", "qst_wed_betrothed", "$g_talk_troop"),

(quest_set_slot, "qst_wed_betrothed", slot_quest_expiration_days, 365),
(quest_set_slot, "qst_wed_betrothed", slot_quest_giver_troop, "$g_talk_troop"),
(quest_set_slot, "qst_wed_betrothed", slot_quest_target_troop, ":bride"),

(try_begin),
   (eq,"$talk_context",tc_party_encounter),
   (assign, "$g_leave_encounter", 1),
(try_end),

]],
[anyone,"lord_marriage_permission_engagement_date", [],
"Unfortunately, there is one final complication -- there is no safe place to hold the wedding. Let us hold off on finalizing this, for the time being.", "close_window",
[]],
[anyone,"lord_marriage_permission_endowment_answer_delay", [],
"No matter -- take the time you need to raise the money. I want her ladyship to be well looked after.", "lord_pretalk",[
]],
[anyone,"lord_marriage_permission_endowment_answer_delay", [],
"That is a shame, but I would be remiss in my duty if I allowed her ladyship to face an uncertain future.", "lord_pretalk",[
(call_script, "script_fail_quest", "qst_formal_marriage_proposal"),
(call_script, "script_end_quest", "qst_formal_marriage_proposal"),
]],
[anyone|plyr,"lord_talk_ask_something_2",[
(neg|troop_slot_eq, "$g_talk_troop", slot_lord_granted_courtship_permission, 1),

(assign, "$marriage_candidate", 0),
(try_for_range, ":lady", kingdom_ladies_begin, kingdom_ladies_end),
   (eq, "$marriage_candidate", 0),
   (troop_slot_ge, ":lady", slot_troop_courtship_state, 2),
   (neg|troop_slot_eq, ":lady", slot_troop_courtship_state, 4),
   (neg|troop_slot_ge, ":lady", slot_troop_spouse, 0),
   (call_script, "script_get_kingdom_lady_social_determinants", ":lady"),
   (eq, reg0, "$g_talk_troop"),

   (assign, "$marriage_candidate", ":lady"),

   (str_clear, s14),
   (call_script, "script_troop_get_family_relation_to_troop", ":lady", "$g_talk_troop"),
   (gt, reg0, 0),
   (str_store_string, s14, "str_your_s11_"),
(try_end),
(gt, "$marriage_candidate", 0),
(str_store_troop_name, s12, "$marriage_candidate"),

(str_clear, s10),
(try_begin),
   (troop_slot_eq, "$g_talk_troop", slot_lord_granted_courtship_permission, -1),
   (str_store_string, s10, "str_i_ask_again_may"),
(else_try),
   (str_store_string, s10, "str_may"),
(try_end),
],
 "{s10} I have the honor of visiting with {s14}{s12}?", "lord_courtship_permission",
[]],
[anyone,"lord_courtship_permission", [
(call_script, "script_dplmc_is_affiliated_family_member", "$g_talk_troop"),
(eq, reg0, 1),

(try_begin),
   (troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_goodnatured),
   (str_store_string, s12, "str_very_well_as_far_as_im_concerned_i_suppose_she_can_see_most_anyone_she_likes__within_reason_of_course"),
(else_try),
   (this_or_next|troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_debauched),
      (troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_quarrelsome),
   (str_store_string, s12, "str_very_well_an_alliance_with_you_could_be_valuable_go_chat_with_her_and_see_if_you_can_get_her_to_take_a_fancy_to_you_if_she_doesnt_and_if_we_still_want_to_conclude_this_business_then_i_can_make_her_see_reason"),
(else_try),
   (str_store_string, s12, "str_you_have_my_blessing_to_pay_suit_to_her__so_long_as_your_intentions_are_honorable_of_course_depending_on_how_things_proceed_between_you_two_we_may_have_more_to_discuss_at_a_later_date"),
(try_end),
],
 "{s12}", "lord_pretalk",
[
(troop_set_slot, "$g_talk_troop", slot_lord_granted_courtship_permission, 1),
]],
[anyone,"lord_courtship_permission", [
 (troop_slot_ge, "$marriage_candidate", slot_troop_met, 2),
(neg|troop_slot_eq, "$marriage_candidate", slot_troop_met, 4),
(this_or_next|troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_debauched),
   (troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_quarrelsome),

(call_script, "script_troop_get_relation_with_troop", "$marriage_candidate", "trp_player"),
(gt, reg0, 0),
   ],
 "From what I hear, you have already spoken to her -- without my permission. Let me tell you this: I am her lord and guardian, and I have plans for her. I will not be mocked behind my back as a man who cannot control the women of his household. I would ask you not to discuss this matter with me again.", "lord_pretalk",
[
(troop_set_slot, "$g_talk_troop", slot_lord_granted_courtship_permission, -1),
(call_script, "script_troop_change_relation_with_troop", "$g_talk_troop", "trp_player", -1),
]],
[anyone,"lord_courtship_permission", [
(call_script, "script_npc_decision_checklist_male_guardian_assess_suitor", "$g_talk_troop", "trp_player"),
(lt, reg0, 1),
(str_store_string, s14, reg1),
##diplomacy start+
#xxx TODO: replace "cross swords" with cultural alternative
##diplomacy end+
],
 "{s14}", "lord_pretalk",
[
(troop_set_slot, "$g_talk_troop", slot_lord_granted_courtship_permission, -1),
]],
[anyone,"lord_courtship_permission", [
(try_begin),
   (troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_goodnatured),
   (str_store_string, s12, "str_very_well_as_far_as_im_concerned_i_suppose_she_can_see_most_anyone_she_likes__within_reason_of_course"),
(else_try),
   (this_or_next|troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_debauched),
      (troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_quarrelsome),
   (str_store_string, s12, "str_very_well_an_alliance_with_you_could_be_valuable_go_chat_with_her_and_see_if_you_can_get_her_to_take_a_fancy_to_you_if_she_doesnt_and_if_we_still_want_to_conclude_this_business_then_i_can_make_her_see_reason"),
(else_try),
   (str_store_string, s12, "str_you_have_my_blessing_to_pay_suit_to_her__so_long_as_your_intentions_are_honorable_of_course_depending_on_how_things_proceed_between_you_two_we_may_have_more_to_discuss_at_a_later_date"),
(try_end),
],
 "{s12}", "lord_pretalk",
[
(troop_set_slot, "$g_talk_troop", slot_lord_granted_courtship_permission, 1),
]],
[anyone|plyr,"lord_talk_ask_something_2", [
(neg|troop_slot_eq, "$g_talk_troop", slot_lord_granted_courtship_permission, 1),
(neg|troop_slot_ge, "trp_player", slot_troop_spouse, active_npcs_begin),
#diplomacy start+
##OLD:
#(troop_get_type, ":is_female", "$g_talk_troop"),
#(neq, ":is_female", 1),
##NEW:
#Lords can be male or female, so don't disable for the above.
#Avoid saying this to people you're engaged to (with the possible benign
#side-effect of avoiding giving this dialog for promoted heroes with uninitialized
#family slots.
(neg|troop_slot_eq, "$g_talk_troop", slot_troop_betrothed, "trp_player"),
#If the player is engaged already, the other person must either be gone or in another kingdom
(troop_get_slot, reg0, "trp_player", slot_troop_betrothed),
(neq, reg0, "$g_talk_troop"),
(try_begin),
	(ge, reg0, 1),
	(neg|troop_slot_ge, reg0, slot_troop_occupation, slto_retirement),
	(store_faction_of_troop, reg0, reg0),
	(this_or_next|eq, reg0, "$players_kingdom"),
	(this_or_next|eq, reg0, "fac_player_supporters_faction"),
		(eq, reg0, "$g_talk_troop_faction"),
	(assign, reg0, 1),
(else_try),
	(assign, reg0, -1),
(try_end),
(lt, reg0, 1),

#Avoid saying this to relatives (distant ones are allowed for medieval settings) or people you are already married to.
(call_script, "script_dplmc_troop_get_family_relation_to_troop", "$g_talk_troop", "trp_player"),
(lt, reg0, 2),

#Just ensuring that reg65 is initialized (no reason to think it isn't,
#but this what I generally do when the dialog I'm relacing uses "troop_get_type"
#instead of just using whatever's already in reg65).
(call_script, "script_dplmc_store_troop_is_female", "$g_talk_troop"),
(assign, reg65, reg0),
##diplomacy end+
],
"What would it take to cement a lasting alliance with your house?", "lord_talk_ask_marriage_1",[]],
[anyone|plyr,"lord_talk_ask_something_2", [],
"Never mind.", "lord_pretalk",[]],
[anyone,"lord_talk_ask_location",
	[
	(lt, "$g_talk_troop_effective_relation", 0),
	#This can be called from multiple dialog branches, so you need to return
	#to the right place.
	(neg|troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_lady),
	(this_or_next|is_between, "$g_talk_troop", active_npcs_begin, active_npcs_end),
		(troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_hero),
	(assign, ":min_relation", -5),#default refuse at -6 or less
	(try_begin),
		(troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_quarrelsome),
		(assign, ":min_relation", 0),#refuse at -1 or less
	(else_try),
		(eq, "$g_talk_troop_faction", "$players_kingdom"),
		(assign, ":min_relation", -10),#refuse at -11 or less
	(try_end),
	(try_begin),
		(troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_goodnatured),
		(val_sub, ":min_relation", 5),
	(try_end),
	(lt, "$g_talk_troop_effective_relation", ":min_relation"),
	#used as a rule-of-thumb for "will work with you even if they dislike you"
	#(includes affiliate check among other things)
	(call_script, "script_dplmc_player_can_give_troops_to_troop", "$g_talk_troop"),
	(lt, reg0, 1),
	],
	#TODO: Differentiate the responses for different personalities
	"Then you will have to ask someone else.", "lord_pretalk", []],
[anyone,"lord_talk_ask_location",
	[
	(lt, "$g_talk_troop_effective_relation", 0),
	#version for ladies
	(this_or_next|is_between, "$g_talk_troop", kingdom_ladies_begin, kingdom_ladies_end),
		(troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_lady),
	(assign, ":min_relation", -4),#default refuse at -5 or less
	(try_begin),
		(troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_quarrelsome),
		(assign, ":min_relation", 0),#refuse at -1 or less
	(else_try),
		(eq, "$g_talk_troop_faction", "$players_kingdom"),
		(assign, ":min_relation", -9),#refuse at -10 or less
	(try_end),
	(try_begin),
		(troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_goodnatured),
		(val_sub, ":min_relation", 5),
	(try_end),
	(lt, "$g_talk_troop_effective_relation", ":min_relation"),
	#used as a rule-of-thumb for "will work with you even if they dislike you"
	(call_script, "script_dplmc_player_can_give_troops_to_troop", "$g_talk_troop"),
	(lt, reg0, 1),
	],"I am afraid you will have to ask someone else.", "lady_pretalk", []],
[anyone,"lord_talk_ask_location", [],
"Very well, I may or may not have an answer for you. About whom do you wish to hear?", "lord_talk_ask_location_2",[]],
[anyone|plyr|repeat_for_troops,"lord_talk_ask_location_2", [(store_repeat_object, ":troop_no"),
                                                           (neq, "$g_talk_troop", ":troop_no"),
                                                           (is_between, ":troop_no", active_npcs_begin, kingdom_ladies_end),
                                            (neq, ":troop_no", "trp_player"),
                                                           (this_or_next|troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
                                             (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_lady),
                                                           (store_troop_faction, ":faction_no", ":troop_no"),
                                                           (eq, "$g_encountered_party_faction", ":faction_no"),
                                                           (str_store_troop_name, s1, ":troop_no"),
                                            (try_begin),
                                             (faction_slot_eq, "$players_kingdom", slot_faction_marshall, ":troop_no"),
                                              (str_store_string, s1, "@Our strategist, {s1}"),
											##diplomacy start+ Add relation descriptions
											(else_try),
												(faction_slot_eq, "$players_kingdom", slot_faction_leader, ":troop_no"),
												(str_store_string, s1, "@Our leader, {s1}"),
											(else_try),
												(neg|troop_slot_eq, "$g_talk_troop", slot_troop_met, 0),
												(neg|troop_slot_eq, ":troop_no", slot_troop_met, 0),
												(call_script, "script_dplmc_cap_troop_describes_troop_to_troop_s1", 1, "trp_player", ":troop_no", "$g_talk_troop"),
											##diplomacy end+
                                            (try_end),

                                            ],
"{s1}", "lord_talk_ask_location_3",[(store_repeat_object, "$hero_requested_to_learn_location")]],
[anyone|plyr,"lord_talk_ask_location_2", [
  ##diplomacy start+
  (neg|troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_hero),#support promoted ladies
  (this_or_next|troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_lady),
  ##diplomacy end+
  (is_between, "$g_talk_troop", kingdom_ladies_begin, kingdom_ladies_end),
], "Never mind.", "lady_pretalk",[]],
[anyone|plyr,"lord_talk_ask_location_2", [
  ##diplomacy start+
  (neg|troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_lady),
  #support promoted ladies
  (this_or_next|troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_hero),
  ##diplomacy end+
  (neg|is_between, "$g_talk_troop", kingdom_ladies_begin, kingdom_ladies_end),
], "Never mind.", "lord_pretalk",[]],
[anyone,"lord_talk_ask_location_3",
[
  (is_between, "$g_talk_troop", kingdom_ladies_begin, kingdom_ladies_end),
  (call_script, "script_update_troop_location_notes", "$hero_requested_to_learn_location", 1),
  (call_script, "script_get_information_about_troops_position", "$hero_requested_to_learn_location", 0),
  ],
"{s1}", "lady_pretalk",[]],
[anyone,"lord_talk_ask_location_3",
[
  (call_script, "script_update_troop_location_notes", "$hero_requested_to_learn_location", 1),
  (call_script, "script_get_information_about_troops_position", "$hero_requested_to_learn_location", 0),
  ],
"{s1}", "lord_pretalk",[]],
[anyone,"lord_talk_ask_about_war", [],
"{s12}", "lord_talk_ask_about_war_2",[
                                                                   (assign, ":num_enemies", 0),
                                                                   (try_for_range_backwards, ":cur_faction", kingdoms_begin, kingdoms_end),
                                                                     (faction_slot_eq, ":cur_faction", slot_faction_state, sfs_active),
                                                                     (store_relation, ":cur_relation", ":cur_faction", "$g_talk_troop_faction"),
                                                                     (lt, ":cur_relation", 0),
                                                                     (try_begin),
                                                                       (eq, ":num_enemies", 0),
                                                                       (str_store_faction_name_link, s12, ":cur_faction"),
                                                                     (else_try),
                                                                       (eq, ":num_enemies", 1),
                                                                       (str_store_faction_name_link, s11, ":cur_faction"),
                                                                       (str_store_string, s12, "@{s11} and {s12}"),
                                                                     (else_try),
                                                                       (str_store_faction_name_link, s11, ":cur_faction"),
                                                                       (str_store_string, s12, "@{!}{s11}, {s12}"),
                                                                     (try_end),
                                                                     (val_add, ":num_enemies", 1),
                                                                   (try_end),
                                                                   (try_begin),
                                                                     (eq, ":num_enemies", 0),
                                                                     (str_store_string, s12, "@We are not at war with anyone."),
                                                                   (else_try),
                                                                     (str_store_string, s12, "@We are at war with {s12}."),
                                                                   (try_end),
                                                                   ]],
[anyone|plyr|repeat_for_factions, "lord_talk_ask_about_war_2", [(store_repeat_object, ":faction_no"),
                                                               (is_between, ":faction_no", kingdoms_begin, kingdoms_end),
                                                               (faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
                                                                  (store_relation, ":cur_relation", ":faction_no", "$g_talk_troop_faction"),
                                                                  (lt, ":cur_relation", 0),
                                                                  (str_store_faction_name, s1, ":faction_no")],
"Tell me more about the war with {s1}.", "lord_talk_ask_about_war_details",[(store_repeat_object, "$faction_requested_to_learn_more_details_about_the_war_against")]],
[anyone|plyr,"lord_talk_ask_about_war_2", [], "That's all I wanted to know. Thank you.", "lord_pretalk",[]],
[anyone,"lord_talk_ask_about_war_details", [],
#   "We have {reg5?{reg5}:no} {reg3?armies:army} and they have {reg6?{reg6}:none}. Overall, {s9}.",
"{s9}.",
"lord_talk_ask_about_war_2",
[#(call_script, "script_faction_get_number_of_armies", "$g_encountered_party_faction"),
 #(assign, reg5, reg0),
 #(assign, reg3, 1),
 #(try_begin),
                             #  (eq, reg5, 1),
                             #  (assign, reg3, 0),
                             #(try_end),
                             #(call_script, "script_faction_get_number_of_armies", "$faction_requested_to_learn_more_details_about_the_war_against"),
                             #(assign, reg6, reg0),
                             #(assign, reg4, 1),
                             #(try_begin),
                             #  (eq, reg6, 1),
                             #  (assign, reg4, 0),
                             #(try_end),
                             #(store_div, ":our_str", reg5, 2),
                             #(store_div, ":enemy_str", reg6, 2),
                             #(store_sub, ":advantage", ":our_str", ":enemy_str"),
                             #(val_clamp, ":advantage", -4, 5),
                             #(val_add, ":advantage", 4),
                             #(store_add, ":adv_str", "str_war_report_minus_4", ":advantage"),
                             #(str_store_string, s9, ":adv_str"),

   (store_add, ":war_damage_slot", "$faction_requested_to_learn_more_details_about_the_war_against", slot_faction_war_damage_inflicted_on_factions_begin),
   (val_sub, ":war_damage_slot", kingdoms_begin),
    (faction_get_slot, ":war_damage_inflicted", "$g_talk_troop_faction", ":war_damage_slot"),

   (store_add, ":war_damage_slot", "$g_talk_troop_faction", slot_faction_war_damage_inflicted_on_factions_begin),
   (val_sub, ":war_damage_slot", kingdoms_begin),
    (faction_get_slot, ":war_damage_suffered", "$faction_requested_to_learn_more_details_about_the_war_against", ":war_damage_slot"),

   (val_max, ":war_damage_suffered", 1),

   (store_mul, ":war_damage_ratio", ":war_damage_inflicted", 100),
   (val_div, ":war_damage_ratio", ":war_damage_suffered"),

   (try_begin),
      (eq, "$cheat_mode", 1),
      (assign, reg3, ":war_damage_inflicted"),
      (assign, reg4, ":war_damage_suffered"),
      (assign, reg5, ":war_damage_ratio"),
      (display_message, "str_war_damage_inflicted_reg3_suffered_reg4_ratio_reg5"),
   (try_end),

   (str_store_string, s9, "str_error__did_not_calculate_war_progress_string_properly"),
   (try_begin),
      (lt, ":war_damage_inflicted", 5),
      (str_store_string, s9, "str_the_war_has_barely_begun_so_and_it_is_too_early_to_say_who_is_winning_and_who_is_losing"),
   (else_try),
      (gt, ":war_damage_inflicted", 100),
      (gt, ":war_damage_ratio", 200),
      (str_store_string, s9, "str_we_have_been_hitting_them_very_hard_and_giving_them_little_chance_to_recover"),
   (else_try),
      (gt, ":war_damage_inflicted", 80),
      (gt, ":war_damage_ratio", 150),
      (str_store_string, s9, "str_the_fighting_has_been_hard_but_we_have_definitely_been_getting_the_better_of_them"),
   (else_try),
      (gt, ":war_damage_suffered", 100),
      (lt, ":war_damage_ratio", 50),
      (str_store_string, s9, "str_they_have_been_hitting_us_very_hard_and_causing_great_suffering"),
   (else_try),
      (gt, ":war_damage_suffered", 80),
      (lt, ":war_damage_ratio", 68),
      (str_store_string, s9, "str_the_fighting_has_been_hard_and_i_am_afraid_that_we_have_been_having_the_worst_of_it"),
   (else_try),
      (gt, ":war_damage_suffered", 50),
      (gt, ":war_damage_inflicted", 50),
      (gt, ":war_damage_ratio", 65),
      (str_store_string, s9, "str_both_sides_have_suffered_in_the_fighting"),
   (else_try),
      (gt, ":war_damage_ratio", 125),
      (str_store_string, s9, "str_no_clear_winner_has_yet_emerged_in_the_fighting_but_i_think_we_are_getting_the_better_of_them"),
   (else_try),
      (gt, ":war_damage_ratio", 80),
      (str_store_string, s9, "str_no_clear_winner_has_yet_emerged_in_the_fighting_but_i_fear_they_may_be_getting_the_better_of_us"),
   (else_try),
      (str_store_string, s9, "str_no_clear_winner_has_yet_emerged_in_the_fighting"),
   (try_end),

   (try_begin),
      (neg|faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, "$g_talk_troop"),
      (call_script, "script_npc_decision_checklist_peace_or_war", "$g_talk_troop_faction", "$faction_requested_to_learn_more_details_about_the_war_against", -1),
      (str_store_string, s9, "str_s9_s14"),
     (try_end),
   ]],
[anyone,"lord_talk_ask_about_strategy", [
(faction_get_slot, ":ai_state", "$g_encountered_party_faction", slot_faction_ai_state),
(faction_get_slot, ":ai_object", "$g_encountered_party_faction", slot_faction_ai_object),



(faction_get_slot, ":ai_decider", "$g_encountered_party_faction", slot_faction_marshall),
(try_begin),
(eq, ":ai_decider", -1),
(faction_get_slot, ":ai_decider", "$g_encountered_party_faction", slot_faction_leader),
(try_end),

(call_script, "script_npc_decision_checklist_faction_ai_alt", ":ai_decider"),
(assign, ":planned_state", reg0),
(assign, ":planned_object", reg1),


(try_begin),
(gt, ":ai_object", -1),
 (str_store_party_name, s8, ":ai_object"),
(try_end),

(try_begin),
(eq, ":ai_state", sfai_default),
 (str_store_string, s7, "str_there_is_no_campaign_currently_in_progress"),
(else_try),
(eq, ":ai_state", sfai_gathering_army),
 (str_store_string, s7, "str_we_are_assembling_the_army"),
(else_try),
(eq, ":ai_state", sfai_attacking_center),
 (str_store_string, s7, "str_we_aim_to_take_the_fortress_of_s8"),
(else_try),
(eq, ":ai_state", sfai_raiding_village),
 (str_store_string, s7, "str_we_are_on_a_raid_and_are_now_targeting_s8"),
(else_try),
(eq, ":ai_state", sfai_attacking_enemy_army),
 (str_store_string, s7, "str_we_are_trying_to_seek_out_and_defeat_s8"),
(else_try),
(eq, ":ai_state", sfai_attacking_enemies_around_center),
 (str_store_string, s7, "str_we_are_riding_to_the_defense_of_s8"),
(else_try),
(eq, ":ai_state", sfai_feast),
 (str_store_string, s7, "str_we_are_gathering_for_a_feast_at_s8"),
(try_end),

#Additional information for gathering the army
(str_clear, s9),
(try_begin),
(eq, ":ai_state", sfai_gathering_army),
(faction_get_slot, ":faction_marshal", "$g_talk_troop_faction", slot_faction_marshall),
(gt, ":faction_marshal", -1),
(troop_get_slot, ":marshal_party", ":faction_marshal", slot_troop_leaded_party),
(party_is_active, ":marshal_party"),

(this_or_next|eq, "$g_talk_troop", ":faction_marshal"),
   (party_slot_eq, "$g_talk_troop_party", slot_party_ai_object, ":marshal_party"),

(party_get_slot, ":marshal_object", ":marshal_party", slot_party_ai_object),

 (try_begin),
   (eq, ":marshal_object", -1),
   (str_store_string, s9, "str_we_are_waiting_here_for_vassals"),
(else_try),
   (str_store_party_name, s11, ":marshal_object"),
   (str_store_string, s9, "str_we_are_travelling_to_s11_for_vassals"),
 (try_end),
(try_end),


(try_begin),
(this_or_next|neq, ":ai_state", ":planned_state"),
   (neq, ":ai_object", ":planned_object"),

(str_store_string, s14, "str__however_that_may_change_shortly_s14"),
(try_end),

],
"{s7} {s9} {s14}", "lord_strategy_follow_evaluation",
[]],
[anyone, "lord_strategy_follow_evaluation", [
(this_or_next|faction_slot_eq, "$g_talk_troop_faction", slot_faction_marshall, "$g_talk_troop"),
(this_or_next|faction_slot_eq, "$g_talk_troop_faction", slot_faction_ai_state, sfai_default),
   (faction_slot_eq, "$g_talk_troop_faction", slot_faction_ai_state, sfai_feast),
],
"Did you have any other questions?",
"lord_talk_ask_something_2",[
]],
[anyone, "lord_strategy_follow_evaluation", [
(faction_slot_eq, "$g_talk_troop_faction", slot_faction_ai_state, sfai_gathering_army),
(call_script, "script_npc_decision_checklist_faction_ai_alt", "$g_talk_troop"),
(assign, ":talk_troop_preferred_strategy", reg0),
(neq, ":talk_troop_preferred_strategy", sfai_gathering_army),

(store_current_hours, ":hours_at_current_state"),
(faction_get_slot, ":current_state_started", "$g_talk_troop_faction", slot_faction_ai_current_state_started),
(val_sub, ":hours_at_current_state", ":current_state_started"),
(ge, ":hours_at_current_state", 40),

(faction_get_slot, ":faction_marshal", "$g_talk_troop_faction", slot_faction_marshall),
(is_between, ":faction_marshal", active_npcs_begin, active_npcs_end),
(neq, ":faction_marshal", "$g_talk_troop"),
(str_store_troop_name, s4, ":faction_marshal"),
],
"Our leader {s4} is far too cautious. {reg4?She:He} should either use the army to attack the enemy, or let it go home.",
"lord_strategy_follow_up",[
(assign, "$g_talk_troop_disagrees_with_marshal", 1),

]],
[anyone, "lord_strategy_follow_evaluation", [
(faction_slot_eq, "$g_talk_troop_faction", slot_faction_ai_state, sfai_gathering_army),

(store_current_hours, ":hours_at_current_state"),
(faction_get_slot, ":current_state_started", "$g_talk_troop_faction", slot_faction_ai_current_state_started),
(val_sub, ":hours_at_current_state", ":current_state_started"),
(ge, ":hours_at_current_state", 40),

(faction_get_slot, ":faction_marshal", "$g_talk_troop_faction", slot_faction_marshall),
(is_between, ":faction_marshal", active_npcs_begin, active_npcs_end),
(neq, ":faction_marshal", "$g_talk_troop"),

(call_script, "script_troop_get_relation_with_troop", "$g_talk_troop", ":faction_marshal"),
(lt, reg0, 5),

(str_store_troop_name, s4, ":faction_marshal"),

],
"Our army sits, doing nothing. Apparently, too few vassals have answered the call to arms. Perhaps {s4} does not enjoy the confidence of the hereditary vassals of this clan.",
"lord_strategy_follow_up",[
(assign, "$g_talk_troop_disagrees_with_marshal", 1),

]],
[anyone, "lord_strategy_follow_evaluation",
[
 (call_script, "script_npc_decision_checklist_faction_ai_alt", "$g_talk_troop"),
 (assign, ":talk_troop_preferred_strategy", reg0),

 (neg|faction_slot_eq, "$g_talk_troop_faction", slot_faction_ai_state, ":talk_troop_preferred_strategy"),

 (assign, ":continue", 1),
 (try_begin),
   (eq, ":talk_troop_preferred_strategy", sfai_raiding_village),
   (str_store_string, s4, "@go on the offensive now."),
 (else_try),
   (eq, ":talk_troop_preferred_strategy", sfai_attacking_center),
   (str_store_string, s4, "@go on the offensive now."),
 (else_try),
   (eq, ":talk_troop_preferred_strategy", sfai_attacking_enemies_around_center),
   (str_store_string, s4, "@act to defend our lands."),
 (else_try),
   (eq, ":talk_troop_preferred_strategy", sfai_gathering_army),
   (str_store_string, s4, "@take more time to gather the army."),
 (else_try),
   (assign, ":continue", 0),
 (try_end),

(eq, ":continue", 1),

(faction_get_slot, ":faction_marshal", "$g_talk_troop_faction", slot_faction_marshall),
(is_between, ":faction_marshal", active_npcs_begin, active_npcs_end),
(neq, ":faction_marshal", "$g_talk_troop"),

 (str_store_troop_name, s10, ":faction_marshal"),
 (assign, "$g_talk_troop_disagrees_with_marshal", 1),

],
"I disagree with this strategy. I would prefer to {s4}.",
"lord_strategy_follow_up", [
 (assign, "$g_talk_troop_disagrees_with_marshal", 1),

]],
[anyone, "lord_strategy_follow_evaluation",
[
 (this_or_next|faction_slot_eq, "$g_talk_troop_faction", slot_faction_ai_state, sfai_attacking_center),
 (faction_slot_eq, "$g_talk_troop_faction", slot_faction_ai_state, sfai_raiding_village),

 (call_script, "script_find_center_to_attack_alt", "$g_talk_troop", 1, 0),
 (assign, ":preferred_center", reg0),
(is_between, ":preferred_center", centers_begin, centers_end),

 (faction_get_slot, ":cur_object", "$g_talk_troop_faction", slot_faction_ai_object),
 (neq, ":cur_object", ":preferred_center"),

 #To Steve - if lord's preffered center is different from marshal's current one then this should be enough for lord to say I disagree with marshal isn't this better?
 #Because it is not easy for any lord to return minus score for a center, so if we do not do this, we will not be able to see lords which disagree with marshal.
 #Conclusion : I removed condition of (lt, reg0, 0),

 (faction_get_slot, ":faction_marshal", "$g_talk_troop_faction", slot_faction_marshall),
(is_between, ":faction_marshal", active_npcs_begin, active_npcs_end),
(neq, ":faction_marshal", "$g_talk_troop"),

 (call_script, "script_npc_decision_checklist_evaluate_enemy_center_for_attack", ":faction_marshal", ":preferred_center", 1, 0),
 #(lt, reg0, 0),

 (str_store_string, s9, reg1),
 (str_store_party_name, s8, ":preferred_center"),

 (faction_get_slot, ":faction_marshal", "$g_talk_troop_faction", slot_faction_marshall),
(is_between, ":faction_marshal", active_npcs_begin, active_npcs_end),
(neq, ":faction_marshal", "$g_talk_troop"),

 (str_store_troop_name, s10, ":faction_marshal"),

],
"I personally would prefer to attack {s8}, but our strategist {s10} believes that it {s9}",
"lord_strategy_follow_up",[
 (assign, "$g_talk_troop_disagrees_with_marshal", 1),

]],
[anyone, "lord_strategy_follow_evaluation",
[
 (faction_slot_eq, "$g_talk_troop_faction", slot_faction_ai_state, sfai_attacking_enemies_around_center),

 (call_script, "script_find_center_to_defend", "$g_talk_troop"),
 (assign, ":preferred_center", reg0),
(is_between, ":preferred_center", centers_begin, centers_end),
 (faction_get_slot, ":cur_object", "$g_talk_troop_faction", slot_faction_ai_object),
 (neq, ":cur_object", ":preferred_center"),

 (faction_get_slot, ":faction_marshal", "$g_talk_troop_faction", slot_faction_marshall),
(is_between, ":faction_marshal", active_npcs_begin, active_npcs_end),
(neq, ":faction_marshal", "$g_talk_troop"),

 (str_store_party_name, s8, ":preferred_center"),
 (str_store_party_name, s9, ":cur_object"),

],
"I personally would prefer to defend {s8}, instead of {s9}.",
"lord_strategy_follow_up",[
 (assign, "$g_talk_troop_disagrees_with_marshal", 1),
]],
[anyone, "lord_strategy_follow_evaluation",
[
(faction_get_slot, ":faction_marshal", "$g_talk_troop_faction", slot_faction_marshall),
(this_or_next|neg|is_between, ":faction_marshal", active_npcs_begin, active_npcs_end),
(eq, ":faction_marshal", "$g_talk_troop"),
],
"Is there anything else?",
"lord_talk",[
]],
[anyone, "lord_strategy_follow_evaluation",
[],
"This strategy seems reasonable to me.",
"lord_strategy_follow_up",[
(assign, "$g_talk_troop_disagrees_with_marshal", 0),
]],
[anyone|plyr, "lord_strategy_follow_up", [
(this_or_next|faction_slot_eq, "$g_talk_troop_faction", slot_faction_ai_state, sfai_attacking_center),
(faction_slot_eq, "$g_talk_troop_faction", slot_faction_ai_state, sfai_raiding_village),
],
"If you're attacking, why aren't you...",
"lord_strategy_why_not",[
]],
[anyone|plyr, "lord_strategy_follow_up", [
],
"I see....",
"lord_talk_ask_something_again",[
]],
[anyone|plyr, "lord_strategy_follow_up", [
(eq, "$g_talk_troop_disagrees_with_marshal", 1),
(neg|faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, "$g_talk_troop"),
(faction_get_slot, ":faction_marshal", "$g_talk_troop_faction", slot_faction_marshall),
(is_between, ":faction_marshal", active_npcs_begin, active_npcs_end),
(str_store_troop_name, s4, ":faction_marshal"),
],
"Would you say, then, that {s4} should no longer be the strategist?",
"lord_talk_replace_marshal",[
]],
[anyone, "lord_talk_replace_marshal", [
(faction_get_slot, ":faction_issue", "$g_talk_troop_faction", slot_faction_political_issue),
(is_between, ":faction_issue", centers_begin, centers_end),
(str_store_party_name, s4, ":faction_issue"),
],
"I believe that our clan should resolve the issue of {s4} before we begin to debate replacing the strategist.",
"lord_talk_ask_something_again",[
]],
[anyone, "lord_talk_replace_marshal", [
(faction_slot_eq, "$g_talk_troop_faction", slot_faction_political_issue, 1),
(troop_get_slot, ":stance_on_faction_issue", "$g_talk_troop", slot_troop_stance_on_faction_issue),
(faction_get_slot, ":faction_marshal", "$g_talk_troop_faction", slot_faction_marshall),
(neq, ":stance_on_faction_issue", ":faction_marshal"),
(str_store_troop_name, s4,  ":stance_on_faction_issue"),
(str_store_troop_name, s5,  ":faction_marshal"),

],
"Yes. I have already made my position on this matter clear. I believe that {s4} should be the strategist instead of {s5}.",
"lord_talk_ask_something_again",[
]],
[anyone, "lord_talk_replace_marshal", [
(faction_get_slot, ":faction_marshal", "$g_talk_troop_faction", slot_faction_marshall),
(call_script, "script_troop_get_relation_with_troop", "$g_talk_troop", ":faction_marshal"),
(assign, ":relation_with_marshal", reg0),
(gt, ":relation_with_marshal", "$g_talk_troop_effective_relation"),
],
"I will make up my mind on this matter without your persuasion, {sir/my lady}.",
"lord_talk_ask_something_again",[
]],
[anyone, "lord_talk_replace_marshal", [
],
"Hmm...",
"lord_talk_replace_marshal_decision",[
(faction_set_slot, "$g_talk_troop_faction", slot_faction_political_issue, 1),
]],
[anyone, "lord_talk_replace_marshal_decision", [
(call_script, "script_npc_decision_checklist_take_stand_on_issue", "$g_talk_troop"),
(assign, ":replacement_candidate", reg0),
(neg|faction_slot_eq, "$g_talk_troop_faction", slot_faction_marshall, ":replacement_candidate"),
(call_script, "script_troop_describes_troop_to_s15", "$g_talk_troop", ":replacement_candidate"),
],
"Yes, I would say that. At this point, I would be tempted to say that I support {s15} instead. I am glad that you and I had this discussion, so that I know that we are of the same mind on this matter.",
"lord_talk_ask_something_again",[
(call_script, "script_npc_decision_checklist_take_stand_on_issue", "$g_talk_troop"),
(assign, ":replacement_candidate", reg0),
(troop_set_slot, "$g_talk_troop", slot_troop_stance_on_faction_issue, ":replacement_candidate"),

(faction_get_slot, ":faction_marshal", "$g_talk_troop_faction", slot_faction_marshall),
(troop_get_slot, ":marshal_controversy",  ":faction_marshal", slot_troop_controversy),
(val_add, ":marshal_controversy", 5),
(troop_set_slot, ":faction_marshal", slot_troop_controversy, ":marshal_controversy"),


(call_script, "script_troop_describes_troop_to_s15", "$g_talk_troop", ":replacement_candidate"),

]],
[anyone, "lord_talk_replace_marshal_decision", [
(faction_get_slot, ":faction_marshal", "$g_talk_troop_faction", slot_faction_marshall),
(str_store_troop_name, s4, ":faction_marshal"),
],
"Not necessarily. It is possible for {s4} and I have to have an honest disagreement over strategy, without my seeking to replace him.",
"lord_talk_ask_something_again",[
]],
[anyone, "lord_strategy_why_not", [
],
"Yes?",
"lord_strategy_why_not_select",[
]],
[anyone|plyr, "lord_strategy_why_not_select", [
],
"Never mind",
"lord_talk_ask_something_again",[]],
[anyone|plyr, "lord_strategy_why_not_select",
[
 (this_or_next|faction_slot_eq, "$g_talk_troop_faction", slot_faction_ai_state, sfai_raiding_village),
 (faction_slot_eq, "$g_talk_troop_faction", slot_faction_ai_state, sfai_attacking_center),

 (faction_get_slot, ":cur_object", "$g_talk_troop_faction", slot_faction_ai_object),
 (faction_get_slot, ":faction_marshal", "$g_talk_troop_faction", slot_faction_marshall),
 (gt, ":faction_marshal", -1),
 (call_script, "script_find_center_to_attack_alt", ":faction_marshal", 1, 0),
 (neq, reg0, ":cur_object"),
 (str_store_party_name,s4, ":cur_object"),
],
"..planning to continue with the attack on {s4}?",
"lord_strategy_why_not_reason",[
]],
[anyone|plyr|repeat_for_parties, "lord_strategy_why_not_select",
[
 (store_repeat_object, ":selected_center"),
 (is_between, ":selected_center", centers_begin, centers_end),

 (store_faction_of_party, ":selected_center_faction", ":selected_center"),
 (eq, ":selected_center_faction", "$g_talk_troop_faction"),

 (neg|faction_slot_eq, "$g_talk_troop_faction", slot_faction_ai_object, ":selected_center"),
 (neq, "$g_target_after_gathering", ":selected_center"),

 (party_slot_ge, ":selected_center", slot_center_sortie_enemy_strength, 1),
 (str_store_party_name,s4, ":selected_center"),
],
"..defending {s4}?",
"lord_strategy_why_not_reason",[
(store_repeat_object, "$temp"),
]],
[anyone|plyr|repeat_for_parties, "lord_strategy_why_not_select",
[
 (store_repeat_object, ":selected_center"),
 (is_between, ":selected_center", centers_begin, centers_end),

 (store_faction_of_party, ":selected_center_faction", ":selected_center"),
 (store_relation, ":relation", ":selected_center_faction", "$g_talk_troop_faction"),
 (lt, ":relation", 0),

 (neg|faction_slot_eq, "$g_talk_troop_faction", slot_faction_ai_object, ":selected_center"),
 (str_store_party_name,s4, ":selected_center"),
],
"..attacking {s4}?",
"lord_strategy_why_not_reason",
[
  (store_repeat_object, "$temp"),

  (try_begin),
    (eq, "$cheat_mode", 1),
    (store_sub, ":faction_recce_slot", "$g_talk_troop_faction", kingdoms_begin),
    (val_add, ":faction_recce_slot", slot_center_last_reconnoitered_by_faction_time),
    (store_current_hours, ":hours_since_last_recon"),
    (party_get_slot, ":last_recon_time", "$temp", ":faction_recce_slot"),
    (val_sub, ":hours_since_last_recon", ":last_recon_time"),
  (try_end),
]],
[anyone, "lord_strategy_why_not_reason",
[
 (assign, ":selected_center", "$temp"),
 (store_faction_of_party, ":selected_center_faction", ":selected_center"),
 (eq, ":selected_center_faction", "$g_talk_troop_faction"),
 (faction_get_slot, ":faction_marshal", "$g_talk_troop_faction", slot_faction_marshall),
 (call_script, "script_find_center_to_defend", ":faction_marshal"),
 (assign, ":most_threatened_center", reg0),
 (assign, ":threat_danger_level", reg1),
 (assign, ":enemy_strength_near_threatened_center", reg2),

 (try_begin),
   (call_script, "script_find_center_to_attack_alt", ":faction_marshal", 1, 0),
   (assign, ":target_value_level", reg1),
   (call_script, "script_find_center_to_attack_alt", ":faction_marshal", 1, 1),
   (assign, ":target_value_level_all_vassals", reg1),

   (try_begin),
     (ge, ":target_value_level_all_vassals", ":target_value_level"),
     (assign, ":target_value_level_max", ":target_value_level_all_vassals"),
   (else_try),
     (assign, ":target_value_level_max", ":target_value_level"),
   (try_end),

   (gt, ":target_value_level_max", ":threat_danger_level"),
   (assign, reg4, ":target_value_level"),
   (assign, reg5, ":threat_danger_level"),
   (str_store_string, s9, "str_reason_1"),
 (else_try),
   (assign, ":continue", 0),
   (try_begin),
     (is_between, ":selected_center", villages_begin, villages_end),
     (is_between, ":most_threatened_center", walled_centers_begin, walled_centers_end),
     (assign, ":continue", 1),
   (try_end),

   (try_begin),
     (is_between, ":selected_center", castles_begin, castles_end),
     (is_between, ":most_threatened_center", towns_begin, towns_end),
     (assign, ":continue", 1),
   (try_end),

   (eq, ":continue", 1),

   (str_store_party_name, s8, ":most_threatened_center"),
   #values of centers : town > castle > village
   #Situation : We are going to defend more valueable center.
   #To Steve - Please find a better explaining string for below line.
   (str_store_string, s9, "str_reason_2"),
 (else_try),
   (neq, ":most_threatened_center", ":selected_center"),
   (str_store_party_name, s8, ":most_threatened_center"),
   (str_store_string, s9, "str_reason_3"),
 (else_try),
   (troop_get_slot, ":marshal_party", ":faction_marshal", slot_troop_leaded_party),
   (party_is_active, ":marshal_party"),
   (party_get_slot, ":cached_strength", ":marshal_party", slot_party_cached_strength),
   (party_get_slot, ":follower_strength", ":marshal_party", slot_party_follower_strength),
   (store_add, ":total_strength", ":cached_strength", ":follower_strength"),
   (ge, ":enemy_strength_near_threatened_center", ":total_strength"),
   (assign, reg4, ":enemy_strength_near_threatened_center"),
   (assign, reg5, ":total_strength"),
   (str_store_string, s9, "str_reason_4"),
 (else_try),
   (str_store_string, s9, "str_reason_5"),
 (try_end),
],
"{s9}",
"lord_talk_why_not_repeat",[]],
[anyone, "lord_strategy_why_not_reason",
[
 (assign, ":selected_center", "$temp"),
 (faction_get_slot, ":faction_marshal", "$g_talk_troop_faction", slot_faction_marshall),

 (faction_get_slot, ":faction_ai_object", "$g_talk_troop_faction", slot_faction_ai_object),

 (call_script, "script_npc_decision_checklist_evaluate_enemy_center_for_attack", ":faction_marshal", ":faction_ai_object", 1, 0),
 (assign, "$g_faction_object_score", reg0),

 (assign, "$g_do_not_skip_other_than_current_ai_object", 1),
 (call_script, "script_npc_decision_checklist_evaluate_enemy_center_for_attack", ":faction_marshal", ":selected_center", 1, 0),
 (assign, "$g_do_not_skip_other_than_current_ai_object", 0),

 (lt, reg0, 0),
 (assign, ":explainer_string", reg1),
 (try_begin),
   (eq, "$g_use_current_ai_object_as_s8", 0),
   (str_store_party_name, s8, ":selected_center"),
 (else_try),
   (str_store_party_name, s8, ":faction_ai_object"),
 (try_end),
 (str_store_string, s9, ":explainer_string"),
 (str_clear, s10),
(str_store_troop_name, s11, ":faction_marshal"),
#s10 will say that
],
"Our strategist {s11} believes that {s8} {s9}{s10}",
"lord_talk_why_not_repeat",[]],
[anyone, "lord_strategy_why_not_reason",
[
 (faction_get_slot, ":faction_marshal", "$g_talk_troop_faction", slot_faction_marshall),
 (faction_get_slot, ":cur_object", "$g_talk_troop_faction", slot_faction_ai_object),

 (call_script, "script_npc_decision_checklist_evaluate_enemy_center_for_attack", ":faction_marshal", ":cur_object", 1, 0),
 (assign, ":power_ratio_for_cur_object", reg2),
 (call_script, "script_npc_decision_checklist_evaluate_enemy_center_for_attack", ":faction_marshal", "$temp", 1, 0),
 (assign, ":power_ratio_for_selected_center", reg2),

 (try_begin),
   (eq, ":power_ratio_for_selected_center", 0),
   (str_store_string, s7, "str_reason_6"),
 (else_try),
   (lt, ":power_ratio_for_selected_center", 200),
   (str_store_string, s7, "str_reason_7"),
 (else_try),
   (is_between, ":power_ratio_for_selected_center", 200, 300),
   (str_store_string, s7, "str_reason_8"),
 (else_try),
   (ge, ":power_ratio_for_selected_center", 300),
   (str_store_string, s7, "str_reason_9"),
 (else_try),
   (str_store_string, s7, "str_error_string"),
(try_end),

(try_begin),
  (eq, ":power_ratio_for_cur_object", 0),
  (str_store_string, s8, "str_reason_6"),
(else_try),
  (lt, ":power_ratio_for_cur_object", 200),
  (str_store_string, s8, "str_reason_7"),
(else_try),
  (is_between, ":power_ratio_for_cur_object", 200, 300),
  (str_store_string, s8, "str_reason_8"),
(else_try),
  (ge, ":power_ratio_for_cur_object", 300),
  (str_store_string, s8, "str_reason_9"),
(else_try),
  (str_store_string, s8, "str_error_string"),
(try_end),

(try_begin),
  (ge, ":cur_object", 0),
  (str_store_party_name, s4, ":cur_object"),
(else_try),
  (ge, "$g_target_after_gathering", 0),
  (str_store_party_name, s4, "$g_target_after_gathering"),
(else_try),
  (str_store_party_name, s4, "str_error_string"),
(try_end),

(str_store_troop_name, s5, ":faction_marshal"),

(try_begin),
  (eq, "$cheat_mode", 1),
  (store_sub, ":faction_recce_slot", "$g_talk_troop_faction", kingdoms_begin),
  (val_add, ":faction_recce_slot", slot_center_last_reconnoitered_by_faction_time),
  (store_current_hours, ":hours_since_last_recon"),
  (party_get_slot, ":last_recon_time", "$temp", ":faction_recce_slot"),
  (val_sub, ":hours_since_last_recon", ":last_recon_time"),

  (store_sub, ":faction_recce_slot", "$g_talk_troop_faction", kingdoms_begin),
  (val_add, ":faction_recce_slot", slot_center_last_reconnoitered_by_faction_time),
  (store_current_hours, ":hours_since_last_recon"),
  (party_get_slot, ":last_recon_time", ":cur_object", ":faction_recce_slot"),
  (val_sub, ":hours_since_last_recon", ":last_recon_time"),
(try_end),

(try_begin),
  (assign, ":continue", 0),
  (try_begin),
    (party_slot_eq, "$g_talk_troop_party", slot_party_ai_state, sfai_gathering_army),
    (lt, "$g_target_after_gathering", 0), #then this means faction is gathering army to attack a center.
    (assign, ":continue", 1),
  (try_end),

   (this_or_next|eq, ":continue", 1),
  (this_or_next|faction_slot_eq, "$g_talk_troop_faction", slot_faction_ai_state, sfai_attacking_center),
  (faction_slot_eq, "$g_talk_troop_faction", slot_faction_ai_state, sfai_raiding_village),

  (str_store_string, s3, "str_has_decided_that_an_attack_on_"),
  (str_store_string, s6, "str_this_would_be_better_worth_the_effort"),
(else_try),
  (str_store_string, s3, "str_has_decided_to_defend_"),
  (str_store_party_name, s9, "$temp"),
  (str_store_string, s6, "str_before_going_offensive_we_should_protect_our_lands_if_there_is_any_threat_so_this_can_be_reason_marshall_choosed_defending_s4"),
  (str_clear, s8),
(try_end),
],
"We could go there. {s7} However, {s5} {s3} {s4}. {s6} {s8}.",
"lord_talk_why_not_repeat",[
]],
[anyone,"lord_talk_why_not_repeat", [
],
"Did you have any similar questions? Why we are not...",
"lord_strategy_why_not_select",[
]],
[anyone, "lord_talk_ask_marriage_1", [
	(faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, "$g_talk_troop"),
	(is_between, "$g_talk_troop", pretenders_begin, pretenders_end),
	(neg|troop_slot_eq, "$g_talk_troop", slot_troop_playerparty_history, dplmc_pp_history_nonplayer_entry),
	#This probably can't occur, but make sure.
	(this_or_next|troop_slot_eq,"$g_talk_troop", slot_troop_betrothed, "trp_player"),
	(troop_slot_eq, "trp_player", slot_troop_betrothed, "$g_talk_troop"),
], "Have no fear, I have no intention of changing my mind.  We will be married as soon as there is an opportunity worthy of the august event.", "lord_pretalk", []],
[anyone,"lord_talk_ask_marriage_1", [
(eq, "$g_talk_troop", "trp_kingdom_6_pretender"),#is Arwa
(faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, "$g_talk_troop"),
(is_between, "$g_talk_troop", pretenders_begin, pretenders_end),
(neg|troop_slot_eq, "$g_talk_troop", slot_troop_playerparty_history, dplmc_pp_history_nonplayer_entry),

(this_or_next|ge, "$g_disable_condescending_comments", 2),#allow same-sex marriage if "reduced prejudice" is enabled
	(neq, reg65, "$character_gender"),
(try_begin),
	(troop_get_slot, ":original_faction", "$g_talk_troop", slot_troop_original_faction),
	(is_between, ":original_faction", kingdoms_begin, kingdoms_end),
	(str_store_faction_name, s0, ":original_faction"),
(else_try),
	(str_store_faction_name, s0, "$g_talk_troop_faction"),
(try_end),
],
"I do not forget that it was your strong right arm that placed me in my position.  Do you aim to take my {husband/wife}'s place, to rule the {s0} with me as Commander of the Armies even as I am Mother of the Domain?", "dplmc_claimant_marriage_proposal_pc_confirm", []],
[anyone,"lord_talk_ask_marriage_1", [
(faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, "$g_talk_troop"),
(is_between, "$g_talk_troop", pretenders_begin, pretenders_end),
(neg|troop_slot_eq, "$g_talk_troop", slot_troop_playerparty_history, dplmc_pp_history_nonplayer_entry),

(this_or_next|ge, "$g_disable_condescending_comments", 2),#allow same-sex marriage if "reduced prejudice" is enabled
	(neq, reg65, "$character_gender"),
(try_begin),
	(troop_get_slot, ":original_faction", "$g_talk_troop", slot_troop_original_faction),
	(is_between, ":original_faction", kingdoms_begin, kingdoms_end),
	(str_store_faction_name, s0, ":original_faction"),
(else_try),
	(str_store_faction_name, s0, "$g_talk_troop_faction"),
(try_end),
],
"Are you proposing to rule the {s0} alongside me as my {husband/wife}?",
"dplmc_claimant_marriage_proposal_pc_confirm", []],
[anyone,"lord_talk_ask_marriage_1", [
(faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, "$g_talk_troop"),
(ge, "$g_talk_troop_relation", 50),#enough for the "brave champion" message
(troop_slot_ge, "trp_player", slot_troop_renown, 500),#enough for a claimant to take you seriously
(store_character_level, ":player_level", "trp_player"),
(ge, ":player_level", 15),#high enough level (in Native) to receive all quests
],
"It is our custom to seal any such alliances with marriage.  You have made quite a few waves since your arrival, and I might be willing to consider such an arrangement, but unfortunately no one in my household is eligible to wed.",
"lord_pretalk",[
]],
[anyone,"lord_talk_ask_marriage_1", [
(faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, "$g_talk_troop"),
##diplomacy start+ Use an alternative word for king
(try_begin),
	(eq, reg65, 1),
	(call_script, "script_dplmc_print_cultural_word_to_sreg", "$g_talk_troop", DPLMC_CULTURAL_TERM_KING_FEMALE, 0),
(else_try),
	(call_script, "script_dplmc_print_cultural_word_to_sreg", "$g_talk_troop", DPLMC_CULTURAL_TERM_KING, 0),
(try_end),
],
#"You will not take offense if I tell you that, as a king, I have other plans for my children.",
"You will not take offense if I tell you that, as a {s0}, I have other plans for my children.",
##diplomacy end+
"lord_pretalk",[
]],
[anyone,"lord_talk_ask_marriage_1", [
  (assign, "$marriage_candidate", -1),
  (try_begin),
    ##diplomacy start+
    #(troop_get_type, ":is_female", "trp_player"),
    (assign, ":is_female", "$character_gender"),
    ##(players of either gender may marry opposite-gender lords)
    (assign, ":lord_female", reg65),
    (this_or_next|eq, ":lord_female", 1),
    ##diplomacy end+
    (eq, ":is_female", 1),
    (troop_slot_eq, "$g_talk_troop", slot_troop_spouse, -1),
    (assign, "$marriage_candidate", "$g_talk_troop"),
  (else_try),
    ##diplomacy start+ Players of either gender may marry opposite-gender lords
    #(troop_get_type, ":is_female", "trp_player"),
    #(eq, ":is_female", 0),
    (assign, ":is_female", "$character_gender"),
    (assign, ":lord_female", reg65),
    (eq, ":lord_female", 0),##<-- xxx TODO: Test and see if I can remove this test.
    ##diplomacy end+
    (assign, "$marriage_candidate", -1),
    ##diplomacy start+
    #(try_for_range, ":lady", kingdom_ladies_begin, kingdom_ladies_end),
    ##Be a bit more efficient: stop the loop once you get a match.
    (assign, ":end_cond", kingdom_ladies_end),
    (try_for_range, ":lady", kingdom_ladies_begin, ":end_cond"),
      #Don't include dead/exiled ladies
      (neg|troop_slot_ge, ":lady", slot_troop_occupation, slto_retirement),
      ##diplomacy end+
      (troop_slot_eq, ":lady", slot_troop_spouse, -1),
      (troop_slot_eq, ":lady", slot_troop_betrothed, -1),
      (call_script, "script_get_kingdom_lady_social_determinants", ":lady"),

      (eq, reg0, "$g_talk_troop"),
      ##diplomacy start+
      (call_script, "script_dplmc_store_troop_is_female", ":lady"),
      (neq, reg0, ":is_female"),
      (assign, ":end_cond", ":lady"),
      ##diplomacy end+

      (call_script, "script_troop_get_family_relation_to_troop", ":lady", "$g_talk_troop"),
      (assign, "$marriage_candidate", ":lady"),
      (str_store_troop_name, s14, "$marriage_candidate"),

      (str_store_string, s15, "str_it_is_our_custom_to_seal_any_such_alliances_with_marriage_and_in_fact_we_have_been_looking_for_a_suitable_groom_for_my_s11_s14"),

    (try_end),
  (try_end),
  (eq, "$marriage_candidate", -1),
],
"It is our custom to seal any such alliances with marriage. Unfortunately, no one in my household is eligible to wed.",
"lord_pretalk",[
]],
[anyone,"lord_talk_ask_marriage_1", [
  ##diplomacy start+
  ##OLD:
  #(troop_get_type, ":type", "trp_player"),
  #(eq, ":type", 0),
  ##NEW:
  #get courtship of female lords to work
  (neq, "$marriage_candidate", "$g_talk_troop"),
  ##diplomacy end+
],
  "{s15}",
  "lord_courtship_pre_permission",[
]],
[anyone,"lord_talk_ask_marriage_1", [
(eq, "$marriage_candidate", "$g_talk_troop"),
],
"Are you proposing that you and I marry?",
"lord_marriage_proposal_female_pc_confirm",[
]],
[anyone|plyr,"lord_courtship_pre_permission", [
(neg|troop_slot_ge, "trp_player", slot_troop_spouse, 1),
(neg|troop_slot_ge, "trp_player", slot_troop_betrothed, 1),
#diplomacy start+ get courtship of female lords to work
(neq, reg65, 1),#not talking to a woman
(assign, ":is_female", "$character_gender"),
#(troop_get_type, ":is_female", "trp_player"),
##diplomacy end+
(eq, ":is_female", 0),

(str_clear, s15),
(try_begin),
(troop_slot_eq, "$g_talk_troop", slot_lord_granted_courtship_permission, -1),
(str_store_string, s15, "str_once_again_"),
(try_end),
],
##diplomacy start+ "groom" -> {groom/bride}
"May I {s15}suggest that I be considered as a {groom/bride}?",
##diplomacy end+
"lord_courtship_permission",[
]],
[anyone|plyr,"lord_courtship_pre_permission", [
(eq, "$cheat_mode", 2),
],
"CHEAT -- Start engagement",
"lord_marriage_permission_engagement_date",[

(setup_quest_text, "qst_formal_marriage_proposal"),
(str_store_string, s2, "str_cheat__marriage_proposal"),

(call_script, "script_start_quest", "qst_formal_marriage_proposal", "$marriage_candidate"),
(quest_set_slot, "qst_formal_marriage_proposal", slot_quest_giver_troop, "$marriage_candidate"),
]],
[anyone|plyr,"lord_courtship_pre_permission", [
],
"Never mind",
"lord_pretalk",[
]],
[anyone|plyr,"lord_marriage_proposal_female_pc_confirm", [
],
"Yes. That is my proposal.",
"lord_marriage_proposal_female_pc_reax",[
]],
[anyone|plyr,"lord_marriage_proposal_female_pc_confirm", [
],
"No, I think you have misunderstood me.",
"lord_pretalk",[
]],
[anyone|plyr,"lord_marriage_proposal_female_pc_confirm", [
(lt, "$g_disable_condescending_comments", 2),
(eq, reg65, "$character_gender"),
],
"Oh, HELL no!  No, you totally have the wrong idea... forget I said anything.",
"lord_pretalk",[
]],
[anyone,"lord_marriage_proposal_female_pc_reax", [
(call_script, "script_npc_decision_checklist_marry_female_pc", "$g_talk_troop"),
(le, reg0, 0),
],
"{s14}",
"lord_pretalk",[
]],
[anyone,"lord_marriage_proposal_female_pc_reax", [
(call_script, "script_npc_decision_checklist_marry_female_pc", "$g_talk_troop"),
(eq, reg0, 2),
],
"{s14}",
"lord_pretalk",[
(troop_set_slot, "$g_talk_troop", slot_troop_met, 2),
]],
[anyone,"lord_marriage_proposal_female_pc_reax", [
],
"{s14}",
"lord_marriage_proposal_female_pc_next_step",[
]],
[anyone,"lord_marriage_proposal_female_pc_next_step", [
	(lt, "$g_disable_condescending_comments", 2),#Never say this with bias disabled
	(neq, reg65, "$character_gender"),
	#Not some non-noble promoted troop
	(is_between, "$g_talk_troop", heroes_begin, heroes_end),
	#Not a former companion
	#gekokujo 3.0 microfactions! include fort companions start
	#(this_or_next|neg|is_between, "$g_talk_troop", companions_begin, companions_end),
	(this_or_next|neg|is_between, "$g_talk_troop", companions_begin, fort_companions_end),
	#gekokujo 3.0 microfactions! include fort companions end
		(neg|troop_slot_eq, "$g_talk_troop", slot_troop_playerparty_history, dplmc_pp_history_nonplayer_entry),
	#Not a supported pretender
	(this_or_next|neg|is_between, "$g_talk_troop", pretenders_begin, pretenders_end),
		(neg|troop_slot_eq, "$g_talk_troop", slot_troop_playerparty_history, dplmc_pp_history_nonplayer_entry),
	#Must be someone who would ask this in the first place
	(troop_get_slot, reg0, "$g_talk_troop", slot_lord_reputation_type),
	(neq, reg0, lrep_cunning),
	(neq, reg0, lrep_goodnatured),

	(this_or_next|lt, "$g_disable_condescending_comments", 0),#With bias on medium, only certain traditionalists will say this.
	(this_or_next|eq, reg0, lrep_conventional),#Usually a lord wouldn't be lrep_conventional or lrep_moralist
	(this_or_next|eq, reg0, lrep_moralist),
	(this_or_next|eq, reg0, lrep_martial),#Upstanding & martial are impossible to marry in Native
		(eq, reg0, lrep_upstanding),

	(call_script, "script_cf_dplmc_faction_has_bias_against_gender", "$g_talk_troop_faction", "$character_gender"),
	(call_script, "script_dplmc_print_cultural_word_to_sreg", "$g_talk_troop", DPLMC_CULTURAL_TERM_LORD_PLURAL, 0),
  ],#Next line: changed "man" to {woman/man}, and "other lords" to "other {s0}"
   "I must say, though. You live your life like a {woman/man}, riding where you will, with the company you choose. This will not make it easy for the other {s0} to accept our marriage. I don't suppose that you would give up adventuring, for the sake of our marriage?",
   "lord_marriage_proposal_female_pc_next_step_2",[
   ]],
[anyone|plyr,"lord_marriage_proposal_female_pc_next_step_2", [
  ],
   "I think not!",
   "lord_marriage_proposal_female_pc_next_step_5",[
   ]],
[anyone|plyr,"lord_marriage_proposal_female_pc_next_step_2", [
	#It might be a bit disappointing to be able to agree to this with no lasting effect
	#(the NPC will not even appear to remember it), so I was on the fence as to whether
	#to put this in or not without a fuller implementation.
	##(eq, 0, 1),
  ],
   "Very well.",
   "lord_marriage_proposal_female_pc_next_step_5",[
   ]],
[anyone,"lord_marriage_proposal_female_pc_next_step", [
],
"I suppose the next step would be for me to send a message to your family, asking for their permission to marry you, but I suppose that you make your own decisions.",
"lord_marriage_proposal_female_pc_next_step_4",[
]],
[anyone|plyr,"lord_marriage_proposal_female_pc_next_step_4", [
],
"You assume correctly.",
"lord_marriage_proposal_female_pc_next_step_5",[
]],
[anyone,"lord_marriage_proposal_female_pc_next_step_5", [
##diplomacy start+
(call_script, "script_dplmc_print_cultural_word_to_sreg", "$g_talk_troop", DPLMC_CULTURAL_TERM_LORD_PLURAL, 0),
],#Replace "lords" with {s0}
"Very well, then. As there are no obstacles to our marriage, should we then consider ourselves engaged to be wed? I will organize a great feast, and we can exchange our vows before all the {s0} of the clan. If you are willing, that is...",
##diplomacy end+
"lord_marriage_proposal_female_pc_confirm_engagement",[
]],
[anyone|plyr,"lord_marriage_proposal_female_pc_confirm_engagement", [
],
"I am willing.",
"lord_marriage_proposal_female_pc_confirm_engagement_yes",[
(troop_set_slot, "$g_talk_troop", slot_troop_betrothed, "trp_player"),
(troop_set_slot, "trp_player", slot_troop_betrothed, "$g_talk_troop"),

(assign, "$g_other_quest", 0),
(try_begin),
(store_partner_quest, ":other_quest", "$g_talk_troop"),
 (gt, ":other_quest", 0),
(assign, "$g_other_quest", ":other_quest"),
(try_end),

(str_store_troop_name, s4, "$g_talk_troop"),

(setup_quest_text, "qst_wed_betrothed_female"),
(str_store_string, s2, "str_you_plan_to_marry_s4_as_you_have_no_family_in_calradia_he_will_organize_the_wedding_feast"),

(call_script, "script_start_quest", "qst_wed_betrothed_female", "$g_talk_troop"),

(quest_set_slot, "qst_wed_betrothed_female", slot_quest_expiration_days, 120),
(quest_set_slot, "qst_wed_betrothed_female", slot_quest_giver_troop, "$g_talk_troop"),

]],
[anyone|plyr,"lord_marriage_proposal_female_pc_confirm_engagement", [
],
"Actually, I would like to reconsider.",
"lord_marriage_proposal_female_pc_confirm_engagement_no",[

]],
[anyone,"lord_marriage_proposal_female_pc_confirm_engagement_yes", [

(str_clear, s12),
(try_begin),
(gt, "$g_other_quest", 0),
(call_script, "script_succeed_quest", "$g_other_quest"),
(call_script, "script_end_quest", "$g_other_quest"),
(str_store_string, s12, "str_cancel_fiancee_quest"),
(try_end),
],
"Very well. Hopefully, a little over a month from now, we shall be wed.{s12}",
"close_window",[
(assign, "$g_leave_encounter", 1),
]],
[anyone,"lord_marriage_proposal_female_pc_confirm_engagement_no", [
],
#diplomacy start+ (players of either gender may marry opposite-gender lords)
"Take whatever time you need, my {lord/lady}.",
#diplomacy end+
"close_window",[
(assign, "$g_leave_encounter", 1),
]],
[anyone|plyr,"lord_talk", [(eq,"$talk_context",tc_party_encounter),
                          (lt, "$g_encountered_party_relation", 0),
                          (str_store_troop_name,s4,"$g_talk_troop")],
"I say this only once, {s4}! Surrender or die!", "party_encounter_lord_hostile_ultimatum_surrender", []],
[anyone|plyr,"lord_talk", [(eq,"$talk_context", tc_party_encounter),
                          (neq,"$g_encountered_party_faction","$players_kingdom"),
                          (ge, "$g_encountered_party_relation", 0),
                              ], "I'm here to deliver you my demands!", "lord_predemand",[]],
[anyone,"lord_predemand", [], "Eh? What do you want?", "lord_demand",[]],
[anyone|plyr,"lord_demand", [(neq,"$g_encountered_party_faction","$players_kingdom"),
                            (ge, "$g_encountered_party_relation", 0),], "I offer you one chance to surrender or die.", "lord_ultimatum_surrender",[]],
[anyone,"lord_ultimatum_surrender", [(ge, "$g_encountered_party_relation", 0)], "{s43}", "lord_attack_verify",[#originally, speak you rascal
     (call_script, "script_lord_comment_to_s43", "$g_talk_troop", "str_unprovoked_attack_default"),
    (try_begin),
      (faction_slot_ge, "$g_encountered_party_faction", slot_faction_truce_days_with_factions_begin, 1),
      (str_store_faction_name, s34, "$g_encountered_party_faction"),
      (str_store_string, s43, "str_s43_just_so_you_know_if_you_attack_me_you_will_be_in_violation_of_the_truce_you_signed_with_the_s34"),
    (try_end),
    (try_begin),
      (eq, "$players_kingdom", "fac_player_supporters_faction"),
      (faction_slot_eq, "fac_player_supporters_faction", slot_faction_leader, "trp_player"),
      (str_store_string, s43, "str_s43_also_you_should_know_that_an_unprovoked_assault_is_declaration_of_war"),
	##diplomacy start+ Handle player is co-ruler of kingdom
	(else_try),
	  (is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
	  (call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", "$players_kingdom"),
	  (ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
	  (str_store_string, s43, "str_s43_also_you_should_know_that_an_unprovoked_assault_is_declaration_of_war"),
	##diplomacy end+
    (try_end),

   ]],
[anyone|plyr,"lord_attack_verify", [], "Forgive me sir. I don't know what I was thinking.", "lord_attack_verify_cancel",[]],
[anyone,"lord_attack_verify_cancel", [], "Be gone, then.", "close_window",[(call_script, "script_change_player_relation_with_troop", "$g_talk_troop", -1),(assign, "$g_leave_encounter",1)]],
[anyone|plyr,"lord_attack_verify", [], "That is none of your business. Prepare to fight!", "lord_attack_verify_commit",[
]],
[anyone,"lord_ultimatum_surrender", [], "{s43}", "lord_attack_verify_b", #originally, you will not survive this
[
 (call_script, "script_lord_comment_to_s43", "$g_talk_troop", "str_unnecessary_attack_default"),
 (call_script, "script_make_kingdom_hostile_to_player", "$g_encountered_party_faction", -3),
 (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", -5),

 (assign,"$encountered_party_hostile",1),
 (assign,"$encountered_party_friendly",0),
 ]],
[anyone|plyr,"lord_attack_verify_b", [], "Forgive me sir. I don't know what I was thinking.", "lord_attack_verify_cancel",[]],
[anyone|plyr,"lord_attack_verify_b", [], "I stand my ground. Prepare to fight!", "lord_attack_verify_commit",[]],
[anyone,"lord_attack_verify_commit", [], "{s43}", "close_window",
[
 (call_script, "script_lord_comment_to_s43", "$g_talk_troop", "str_lord_challenged_default"),
(try_begin),
   (ge, "$g_encountered_party_relation", 0),
   (call_script, "script_diplomacy_party_attacks_neutral", "p_main_party", "$g_encountered_party"),
(try_end),
##diplomacy start+ Handle player is co-ruler of kingdom
(assign, ":is_coruler", 0),
(try_begin),
	(is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
	(call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", "$players_kingdom"),
	(ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
	(assign, ":is_coruler", 1),
(try_end),
##diplomacy end+
(try_begin), #this try is added so that a player  monarch ccannot spark a war by attacking a neutral. The player does however cause a provocation, which may allow the other side to go to war
		#If a player can create a hostile faction simply by attacking, this will allow a number of exploits. Therefore, it is quite important to keep this condition in here for active player kingdoms
   (neq, "$players_kingdom", "fac_player_supporters_faction"),
   ##diplomacy start+
   (neq, ":is_coruler", 1),
   ##diplomacy end+
   (call_script, "script_make_kingdom_hostile_to_player", "$g_encountered_party_faction", -3),
(else_try),
   ##diplomacy start+
   (this_or_next|eq, ":is_coruler", 1),
   ##diplomacy end+
   (eq, "$players_kingdom", "fac_player_supporters_faction"),
   (call_script, "script_diplomacy_start_war_between_kingdoms",  "fac_player_supporters_faction", "$g_encountered_party_faction", 1),
(try_end),

#   (call_script, "script_make_kingdom_hostile_to_player", "$g_encountered_party_faction", -3),
(assign,"$encountered_party_hostile",1),
(assign,"$encountered_party_friendly",0),
 (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", -30),
 ]],
[anyone|plyr,"lord_demand", [], "Forgive me. It's nothing.", "lord_pretalk",[]],
[anyone|plyr,"lord_talk", [
                         (faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, "$g_talk_troop"),
                         (troop_slot_eq, "$g_talk_troop", slot_troop_discussed_rebellion, 0),
                         (assign, ":pretender", 0),
                         (try_for_range, ":possible_pretender", pretenders_begin, pretenders_end),
						     ##diplomacy start+
							 #Allow use of that slot for something else for pretenders.
							 (neq, ":possible_pretender", "$g_talk_troop"),
							 ##diplomacy end+
                             (troop_slot_eq, ":possible_pretender", slot_troop_original_faction, "$g_talk_troop_faction"),
                             (assign, ":pretender", ":possible_pretender"),
                         (try_end),
                         (troop_slot_ge, ":pretender", slot_troop_met, 1),
                         (str_store_troop_name, s45, ":pretender"),
                         (troop_get_type, reg3, ":pretender"),
 						 ##diplomacy start+ Override reg3
						 (assign, reg3, 0),
						 (try_begin),
							(call_script, "script_cf_dplmc_troop_is_female", ":pretender"),
							(assign, reg3, 1),
						 (try_end),
						 ##diplomacy end+
                          ],
"I have met in my travels one who calls {reg3?herself:himself} {s45}...", "liege_defends_claim_1",[
    ]],
[anyone|plyr,"lord_talk",
[
  (eq, "$cheat_mode", 2),
  (gt, "$supported_pretender", 0),
  (eq, "$supported_pretender_old_faction", "$g_talk_troop_faction"),
  (neg|faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, "$g_talk_troop"),
  (troop_slot_ge, "$g_talk_troop", slot_troop_leaded_party, 1),
  ],
"{!}CHEAT - Join our cause by force.", "lord_join_rebellion_suggest_cheat",[]],
[anyone,"lord_join_rebellion_suggest_cheat",
[], "Cheat:Allright.",
   "close_window", # unused
[
  (troop_set_slot, "$g_talk_troop", slot_troop_discussed_rebellion, 1),
  (call_script, "script_change_troop_faction", "$g_talk_troop", "$players_kingdom"),
  (assign, "$g_leave_encounter", 1),
  ]],
[anyone|plyr,"lord_talk",
[
 (troop_get_slot, ":prison_location", "$g_talk_troop", slot_troop_prisoner_of_party),
 (is_between, ":prison_location", centers_begin, centers_end),
 (neg|party_slot_eq, ":prison_location", slot_town_lord, "trp_player"),
 (neq, "$talk_context", tc_prison_break),
],
"I've come to break you out of here.", "lord_prison_break_chains",[]],
[anyone,"lord_prison_break_chains", [],
"Thank the heavens you came! However, I'm not going anywhere with these chains on my legs. You'll need to get the key away from the guard somehow.", "close_window",[]],
[anyone|plyr,"lord_talk",
[
 (ge, "$cheat_mode", 1),
 (neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
],
"{!}CHEAT - Take the following action.", "lord_suggest_action_ask",[]],
[anyone,"lord_tell_objective",
[
 (troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
],
"What am I doing? What does it look like I'm doing?! I'm a prisoner here!", "lord_pretalk",[]],
[anyone,"lord_tell_objective",
[
 (troop_slot_eq, "$g_talk_troop", slot_troop_leaded_party, -1)
],##diplomacy start+ "men" to {reg65?soldiers:men}
"I am not commanding any {reg65?soldiers:men} at the moment.", "lord_pretalk",[]],
[anyone,"lord_tell_objective", [
(party_slot_eq, "$g_talk_troop_party", slot_party_ai_state, spai_holding_center),
(party_get_attached_to, ":cur_center_no", "$g_talk_troop_party"),
(try_begin),
 (lt, ":cur_center_no", 0),
 (party_get_cur_town, ":cur_center_no", "$g_talk_troop_party"),
(try_end),
(is_between, ":cur_center_no", centers_begin, centers_end),
],
"We are resting at {s1}. {s14}{s15}",
"lord_pretalk",
[(party_get_slot, ":ai_object", "$g_talk_troop_party", slot_party_ai_object),
 (str_store_party_name, s1, ":ai_object")]],
[anyone,"lord_tell_objective", [(party_slot_eq, "$g_talk_troop_party", slot_party_ai_state, spai_holding_center)],
"We are travelling to {s1}. {s14}{s15}", "lord_pretalk",
[(party_get_slot, ":ai_object", "$g_talk_troop_party", slot_party_ai_object),
 (str_store_party_name, s1, ":ai_object"),
]],
[anyone|auto_proceed,"lord_tell_objective", [
(faction_slot_eq, "$g_talk_troop_faction", slot_faction_marshall, "$g_talk_troop"),
(party_slot_eq, "$g_talk_troop_party", slot_party_ai_state, spai_visiting_village)],
"{!}Warning: This line should never display.", "lord_tell_objective_2",
[]],
[anyone,"lord_tell_objective_2", [],
"I am heading to the vicinity of {s1}. {s14}{s15}", "lord_pretalk",
[(party_get_slot, ":ai_object", "$g_talk_troop_party", slot_party_ai_object),
 (str_store_party_name, s1, ":ai_object")]],
[anyone,"lord_tell_objective", [
(party_slot_eq, "$g_talk_troop_party", slot_party_ai_state, spai_visiting_village)],
"We are recruiting new soldiers from {s1}. {s14}{s15}", "lord_pretalk",
[(party_get_slot, ":ai_object", "$g_talk_troop_party", slot_party_ai_object),
 (str_store_party_name, s1, ":ai_object")]],
[anyone,"lord_tell_objective", [(party_slot_eq, "$g_talk_troop_party", slot_party_ai_state, spai_patrolling_around_center)],
"We are scouting for the enemy around {s1}. {s14}{s15}", "lord_pretalk",
[(party_get_slot, ":ai_object", "$g_talk_troop_party", slot_party_ai_object),
 (str_store_party_name, s1, ":ai_object"),
]],
[anyone,"lord_tell_objective", [
(party_slot_eq, "$g_talk_troop_party", slot_party_ai_state, spai_raiding_around_center),
(party_get_slot, ":ai_object", "$g_talk_troop_party", slot_party_ai_object),
(str_store_party_name, s1, ":ai_object")
],
"We are laying waste to the village of {s1}. {s14}{s15}", "lord_pretalk",[]],
[anyone,"lord_tell_objective", [(party_slot_eq, "$g_talk_troop_party", slot_party_ai_state, spai_retreating_to_center)],
"We are retreating to {s1}. {s14}{s15}", "lord_pretalk",[(party_get_slot, ":ai_object", "$g_talk_troop_party", slot_party_ai_object),
                                                            (str_store_party_name, s1, ":ai_object")]],
[anyone,"lord_tell_objective", [(party_slot_eq, "$g_talk_troop_party", slot_party_ai_state, spai_besieging_center)],
"We are besieging {s1}. {s14}{s15}", "lord_pretalk",[(party_get_slot, ":ai_object", "$g_talk_troop_party", slot_party_ai_object),
                                                            (str_store_party_name, s1, ":ai_object")]],
[anyone,"lord_tell_objective", [(party_slot_eq, "$g_talk_troop_party", slot_party_ai_state, spai_engaging_army),
                               (party_get_slot, ":ai_object", "$g_talk_troop_party", slot_party_ai_object),
                               (party_is_active, ":ai_object"),
                               ],
"We are fighting against {s1}. {s14}{s15}", "lord_pretalk",
[
  (party_get_slot, ":ai_object", "$g_talk_troop_party", slot_party_ai_object),
  (str_store_party_name, s1, ":ai_object")
  ]],
[anyone,"lord_tell_objective", [
(party_slot_eq, "$g_talk_troop_party", slot_party_ai_state, spai_screening_army)],
"I am screening {s1}'s advance. {s14}{s15}", "lord_pretalk",[
 (party_get_slot, ":ai_object", "$g_talk_troop_party", slot_party_ai_object),
(party_stack_get_troop_id, ":ai_object_commander", ":ai_object", 0),
 (str_store_troop_name, s1, ":ai_object_commander")
]],
[anyone,"lord_tell_objective", [(party_slot_eq, "$g_talk_troop_party", slot_party_ai_state, spai_accompanying_army)],
"We are accompanying {s1}. {s14}{s15}", "lord_pretalk",[(party_get_slot, ":ai_object", "$g_talk_troop_party", slot_party_ai_object),
                                                   (str_store_party_name, s1, ":ai_object")]],
[anyone,"lord_tell_objective",
[
 (faction_slot_eq, "$g_talk_troop_faction", slot_faction_marshall, "$g_talk_troop"),
(neg|faction_slot_eq,  "$g_talk_troop_faction", slot_faction_ai_state, sfai_default),
(neg|faction_slot_eq,  "$g_talk_troop_faction", slot_faction_ai_state, sfai_feast),
  ],
"I am leading the army of the clan.", "lord_talk_ask_about_strategy",[]],
[anyone,"lord_tell_objective",
[
  (assign, ":pass", 0),
  (try_begin),
    (party_slot_eq, "$g_talk_troop_party", slot_party_ai_state, spai_undefined),
    (assign, ":pass", 1),
  (else_try),
    (party_slot_eq, "$g_talk_troop_party", slot_party_ai_state, spai_engaging_army),
    (party_get_slot, ":ai_object", "$g_talk_troop_party", slot_party_ai_object),
    (neg|party_is_active, ":ai_object"),
    (assign, ":pass", 1),
  (try_end),
  (eq, ":pass", 1),
  ],
"We are reconsidering our next objective.", "lord_pretalk",[]],
[anyone,"lord_tell_objective", [],
"I don't know: {reg1} {s1} (ERROR)", "lord_pretalk",[(party_get_slot, reg1, "$g_talk_troop_party", slot_party_ai_state),
                                             (party_get_slot, ":ai_object", "$g_talk_troop_party", slot_party_ai_object),
                                                            (str_store_party_name, s1, ":ai_object")]],
[anyone|plyr,"lord_talk",
[
  (eq, "$talk_context", tc_party_encounter),
 (eq, 1, 0),
  (eq, "$g_talk_troop_faction", "$players_kingdom"),
  (party_slot_eq, "$g_encountered_party", slot_party_following_player, 0),
  (neg|faction_slot_eq, "$g_talk_troop_faction", slot_faction_marshall, "trp_player"),
  ],
"Will you follow me? I have a plan.", "lord_ask_follow",[]],
[anyone,"lord_ask_follow", [(party_get_slot, ":dont_follow_until_time", "$g_encountered_party", slot_party_dont_follow_player_until_time),
                           (store_current_hours, ":cur_time"),
                           (lt, ":cur_time", ":dont_follow_until_time")],
"I enjoy your company, {playername}, but there are other things I must attend to. Perhaps in a few days I can ride with you again.", "close_window",
[(assign, "$g_leave_encounter",1)]],
[anyone,"lord_ask_follow", [(troop_get_slot, ":troop_renown", "$g_talk_troop", slot_troop_renown),
                           (troop_get_slot, ":player_renown", "trp_player", slot_troop_renown),
                           (val_mul, ":troop_renown", 3),
                           (val_div, ":troop_renown", 4),
                           (lt, ":player_renown", ":troop_renown"),
                           ],
"That would hardly be proper, {playername}. Why don't you follow me instead?", "close_window",
[(assign, "$g_leave_encounter",1)]],
[anyone,"lord_ask_follow", [(lt, "$g_talk_troop_effective_relation", 25)],
"{s43}", "close_window",
[
    (call_script, "script_lord_comment_to_s43", "$g_talk_troop", "str_lord_follow_refusal_default"),
    (assign, "$g_leave_encounter",1)]],
[anyone,"lord_ask_follow", [],
"Lead the way, {playername}! Let us bring death and defeat to all our enemies.", "close_window",
[(party_set_slot, "$g_talk_troop_party", slot_party_commander_party, "p_main_party"),
 #(call_script, "script_party_decide_next_ai_state_under_command", "$g_talk_troop_party"),
 (call_script, "script_npc_decision_checklist_party_ai", "$g_talk_troop"), #This handles AI for both marshal and other parties
(call_script, "script_party_set_ai_state", "$g_talk_troop_party", reg0, reg1),

 (store_current_hours, ":follow_until_time"),
 (store_add, ":follow_period", 30, "$g_talk_troop_relation"),
 (val_div, ":follow_period", 2),
 (val_add, ":follow_until_time", ":follow_period"),
 (party_set_slot, "$g_encountered_party", slot_party_follow_player_until_time, ":follow_until_time"),
 (party_set_slot, "$g_encountered_party", slot_party_following_player, 1),
 (assign, "$g_leave_encounter",1)]],
[anyone,"lord_talk_preoffer", [], "Yes?", "lord_talk_offer",[]],
[anyone|plyr,"lord_talk_offer", [(eq,1,0)],
"I wish to ransom one of your prisoners.", "knight_offer_join",[
    ]],
[anyone|plyr,"lord_talk_offer", [], "Never mind.", "lord_pretalk",[]],
[anyone,"lord_enter_service_reject", [
  (eq, "$players_kingdom", "fac_player_supporters_faction"),
], "Indeed.... Did you offer vassalage, then, just to by time? Very well -- you shall have time to reconsider, but if you are toying with me, it will do your reputation no credit.", "close_window",
[
  (assign, "$g_leave_encounter", 1),
 ]],
[anyone,"lord_give_oath_give_up", [
  (eq, "$players_kingdom", "fac_player_supporters_faction"),
], "Indeed.... Did you offer vassalage, then, just to buy time? Very well -- you shall have time to reconsider, but if you are toying with me, it will do your reputation no credit.", "close_window",
[
  (assign, "$g_leave_encounter", 1),
 ]],
[anyone,"lord_enter_service_reject", [], "What pigswill!\
And to think I would offer you a place among my hereditary vassals. Begone, beggar, before you lose your head!", "close_window",
[
  (try_begin),
    (store_partner_quest, ":lords_quest"),
    (eq, ":lords_quest", "qst_join_faction"),
    (call_script, "script_abort_quest", "qst_join_faction", 1),
  (try_end),
  (assign, "$g_invite_faction", 0),
  (assign, "$g_invite_faction_lord", 0),
  (assign, "$g_invite_offered_center", 0),
  (assign, "$g_leave_encounter", 1),
 ]],
[anyone,"lord_ask_enter_service", [(gt, "$players_kingdom", 0),
                                  (neq, "$players_kingdom", "$g_talk_troop_faction"),
                                  (faction_get_slot, ":players_lord", "$players_kingdom", slot_faction_leader),
                                  (neq, ":players_lord", "trp_player"),
                                  (str_store_troop_name, s5, ":players_lord"),
                                  ], "You are already oath-bound to serve {s5}, are you not?", "lord_give_oath_under_oath_already",[]],
[anyone|plyr ,"lord_give_oath_under_oath_already", [], "Indeed I am, {s65}. Forgive my rambling.", "lord_pretalk",[]],
[anyone,"lord_ask_enter_service", [(lt, "$g_talk_troop_effective_relation", -5)], "I accept oaths only from those I can trust to keep them, {playername}.", "lord_pretalk",[]],
[anyone,"lord_ask_enter_service", [
##diplomacy start+
#(troop_get_type, ":type", "trp_player"),
#(eq, ":type", 1),
(lt, "$g_disable_condescending_comments", 2),
(call_script, "script_cf_dplmc_faction_has_bias_against_gender", "$g_talk_troop_faction", "$character_gender"),
##diplomacy end+


(try_for_range, ":center", centers_begin, centers_end),
(party_slot_eq, ":center", slot_town_lord, "trp_player"),
 (assign, "$bypass_female_vassal_explanation", 1),
(try_end),
(eq, "$bypass_female_vassal_explanation", 0),

#  (troop_get_slot, ":husband", "trp_player", slot_troop_spouse),
##diplomacy start+ Add bizarro-world version
], "My {lord/lady}, you seem to have the makings of a good war leader. For a {man/woman} to show such skill is an uncommon thing in Japan, but not completely without precedent. {Men/Women} have often taken command of armies after their {wives/husbands} or {mothers/fathers} were slain or captured, for example.", "lord_ask_enter_service_female_2",[
(assign, "$bypass_female_vassal_explanation", 1),
##diplomacy end+
]],
[anyone,"lord_ask_enter_service_female_2", [
##diplomacy start+
(try_begin),
	(eq, reg65, 1),
	(call_script, "script_dplmc_print_cultural_word_to_sreg", "$g_talk_troop", DPLMC_CULTURAL_TERM_KING_FEMALE, 0),
(else_try),
	(call_script, "script_dplmc_print_cultural_word_to_sreg", "$g_talk_troop", DPLMC_CULTURAL_TERM_KING, 0),
(try_end),
],#next line, replace king with {s0} and gendered words with either-way equivalent
"However, I have never heard of a {s0} who granted a fief to a {man/woman}, no matter how valorous, simply because {reg65?she:he} needed an extra vassal. Were I to do such a thing, I would raise eyebrows across Japan. {People/Men} would say that I was besotted or bewitched, or that I aimed to overturn the natural order of things. As much as I regret it, I cannot afford to grant you a fief.", "lord_ask_enter_service_female_response",[]],
[anyone|plyr, "lord_ask_enter_service_female_response", [],
"What if I were to take one of your enemy's castles by force?", "lord_ask_enter_service_female_solution_capture", []],
[anyone|plyr, "lord_ask_enter_service_female_response", [
(neg|troop_slot_ge, "trp_player", slot_troop_spouse, active_npcs_begin),
],
"What if I were to marry one of your lords?", "lord_ask_enter_service_female_solution_marriage", []],
[anyone|plyr, "lord_ask_enter_service_female_response", [],
"Perhaps one of your competitors will prove to be more open-minded.", "lord_ask_enter_service_female_solution_competitor", []],
[anyone|plyr, "lord_ask_enter_service_female_response", [],
"I would be willing to fight for you, even without the fief.", "lord_ask_enter_service", []],
[anyone|plyr, "lord_ask_enter_service_female_response", [],
"Never mind.", "lord_pretalk", []],
[anyone,"lord_ask_enter_service_female_solution_marriage", [
##diplomacy start+ husband -> {wife/husband}
], "Well, I still would not be willing to grant you any fiefs. However, you would no doubt have the use of your {wife/husband}'s properties, which would allow you to act as one of my vassals in all but name. Did you have an other questions?", "lord_ask_enter_service_female_response",[]],
[anyone,"lord_ask_enter_service_female_solution_competitor", [
], "Oh, perhaps you might find someone who was truly desperate -- but then, I would think, they would not have many fiefs to bestow. Did you have an other questions?", "lord_ask_enter_service_female_response",[]],
[anyone,"lord_ask_enter_service_female_solution_capture", [
], "Well, in that case, depending on the circumstances, I might be inclined to let you keep it. Did you have an other questions?", "lord_ask_enter_service_female_response",[]],
[anyone,"lord_ask_enter_service",
[
  (assign, "$g_invite_offered_center", -1),
  (troop_get_slot, ":renown", "trp_player", slot_troop_renown),
  (store_mul, ":vassal_potential", "$g_talk_troop_effective_relation", 5),
  (val_add, ":vassal_potential", ":renown"),
  (call_script, "script_get_number_of_hero_centers", "trp_player"),
  (assign, ":num_centers_owned", reg0),
  (store_mul, ":center_affect", ":num_centers_owned", 50),
  (val_add, ":vassal_potential", ":center_affect"),
  ##diplomacy start+
  #(troop_get_type, ":is_female", "trp_player"),##Get gender from a script instead
  (assign, ":is_female", "$character_gender"),
  (assign, ":faction_prejudiced", 0),
  (try_begin),
	(lt, "$g_disable_condescending_comments", 0),#<- OPTION: Extra prejudice
	(call_script, "script_cf_dplmc_faction_has_bias_against_gender", "$g_talk_troop_faction", ":is_female"),
	(assign, ":faction_prejudiced", 1),
	(val_div, ":vassal_potential", 2),
  (try_end),
  ##diplomacy end+
  (ge, ":vassal_potential", 150),
  (try_begin),
   ##diplomacy start+
   #(eq, ":is_female", 0),#dplmc+ removed
   (this_or_next|ge, "$g_disable_condescending_comments", 2),#<- OPTION: No prejudice
	(eq, ":faction_prejudiced", 0),
   ##diplomacy end+
    (eq, ":num_centers_owned", 0),
    (call_script, "script_get_poorest_village_of_faction", "$g_talk_troop_faction"),
    (gt, reg0, 0),
    (assign, "$g_invite_offered_center", reg0),
  (try_end),
  ##diplomacy start+ Replace "sword" with cultural equivalent
  (call_script, "script_dplmc_print_cultural_word_to_sreg", "$g_talk_troop", DPLMC_CULTURAL_TERM_WEAPON, 0),
  ],#Next line replace "accept your sword" with "accept your {s0}"
"You are known as a brave {man-at-arms/warrior} and a fine leader of men, {playername}.\
I shall be pleased to accept your {s0} into my service and bestow vassalage upon you,\
if you are ready to swear loyalty to me.", "lord_give_oath_1",[]],
[anyone,"lord_ask_enter_service", [
(call_script, "script_dplmc_print_cultural_word_to_sreg", "$g_talk_troop", DPLMC_CULTURAL_TERM_WEAPON, 0),
], "You've yet to show yourself as a competent commander, {playername}.\
Take your {s0} to my enemies and prove to me that you are worthy of becoming my vassal.\
Then we may speak more of this.", "lord_pretalk",[]],
[anyone|plyr,"lord_give_oath_1", [],  "I am ready, {s65}.", "lord_give_oath_2", []],
[anyone|plyr,"lord_give_oath_1", [],  "Forgive me, {s65}, I must give the matter more thought first...", "lord_give_oath_give_up", []],
[anyone,"lord_give_oath_give_up", [
##diplomacy start+
#(troop_get_type, ":type", "trp_player"),
#(eq, ":type", 1),
(eq, 1, "$character_gender"),
##diplomacy end+
],  "Take whatever time you need, my lady.", "lord_pretalk", []],
[anyone,"lord_give_oath_give_up", [],  "What are you playing at, {playername}? Go and make up your mind, and stop wasting my time.", "close_window", [(assign, "$g_leave_encounter",1)]],
[anyone,"lord_give_oath_2", [],  "Good. Then repeat the words of the oath with me: I swear loyalty to you as lawful ruler of the {s41}.", "lord_give_oath_3", [
         (str_store_faction_name, 41, "$g_talk_troop_faction"),
         (try_begin),
             (is_between, "$g_talk_troop", pretenders_begin, pretenders_end),
         (neg|troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_hero),

             (troop_get_slot, ":rebel_faction", "$g_talk_troop", slot_troop_original_faction),
             (str_store_faction_name, 41, ":rebel_faction"),
         (try_end),
   ]],
[anyone|plyr,"lord_give_oath_3", [],  "I pledge loyalty to you as lawful ruler of the {s41}.", "lord_give_oath_4", []],
[anyone|plyr,"lord_give_oath_3", [],  "Excuse me, {reg65?my lady:sir}. But I feel I need to think about this.", "lord_give_oath_give_up", []],
[anyone,"lord_give_oath_4", [],  "I will remain as your loyal and devoted {man/follower} as long as my breath remains....", "lord_give_oath_5", []],
[anyone|plyr,"lord_give_oath_5", [],  "I will remain as your loyal and devoted {man/follower} as long as my breath remains...", "lord_give_oath_6", []],
[anyone|plyr,"lord_give_oath_5", [],  "{reg65?My lady:Sir}, may I ask for some time to think about this?", "lord_give_oath_give_up", []],
[anyone,"lord_give_oath_6", [],  "...and I will be at your side to fight your enemies should you need my sword.", "lord_give_oath_7", []],
[anyone|plyr,"lord_give_oath_7", [],  "...and I will be at your side to fight your enemies should you need my sword.", "lord_give_oath_8", []],
[anyone|plyr,"lord_give_oath_7", [],  "{reg65?My lady:My lord}, please give me more time to think about this.", "lord_give_oath_give_up", []],
[anyone,"lord_give_oath_8", [],  "Finally, I will uphold your lawful claims and those of your legitimate heirs.", "lord_give_oath_9", []],
[anyone|plyr,"lord_give_oath_9", [],  "Finally, I will uphold your lawful claims and those of your legitimate heirs.", "lord_give_oath_10", []],
[anyone|plyr,"lord_give_oath_9", [],  "{reg65?My lady:Sir}, I must have more time to consider this.", "lord_give_oath_give_up", []],
[anyone,"lord_give_oath_10", [],  "Very well. You have given me your solemn oath, {playername}. May you uphold it always, with proper courage and devotion.", "lord_give_oath_go_on_2", []],
[anyone,"lord_give_oath_go_on_2",
[
  ##diplomacy start+ Clear an erroneous value for $g_invite_offered_center (perhaps set somewhere else)
  (try_begin),
     (gt, "$g_invite_offered_center", 1),
	 (store_faction_of_party, ":center_faction", "$g_invite_offered_center"),
	 (neq, ":center_faction", "$g_talk_troop_faction"),
	 (assign, reg1, "$g_invite_offered_center"),
	 (display_message, "@{!}ERROR: Tried to offer {reg1} as a fief to the player, but it is not owned by the leader's faction."),
	 (assign, "$g_invite_offered_center", -1),
  (try_end),
  ##diplomacy end+

  (assign, reg1, 1),
  (try_begin),
    (le, "$g_invite_offered_center", 0),
    (assign, reg1, 0),
  (else_try),
    (str_store_party_name, s1, "$g_invite_offered_center"),
  (try_end),
  ],
"Let it be known that from this day forward, you are my sworn {man/follower} and vassal.\
I give you my protection and grant you the right to bear arms in my name, and I pledge that I shall not deprive you of your life, liberty or properties except by the lawful judgment of your peers or by the law and custom of the land.{reg1? Furthermore I give you the fief of {s1} with all its rents and revenues.:}", "lord_give_oath_go_on_3", []],
[anyone,"lord_give_oath_go_on_3",
[
  ],

"You have done a wise thing, {playername}. Serve me well and I promise, you will rise high.", "lord_give_conclude", []],
[anyone|plyr,"lord_give_conclude",
[
##diplomacy start+ Get gender from script
# (troop_get_type, reg39, "$g_talk_troop"),
 (assign, reg39, 0),
 (try_begin),
    (call_script, "script_cf_dplmc_troop_is_female", "$g_talk_troop"),
	(assign, reg39, 1),
 (try_end),
 (assign, reg65, reg39),
##diplomacy end+
 (try_begin), #activate husband as pretender
   ##diplomacy start+
   (this_or_next|troop_slot_eq, "trp_player", slot_troop_spouse, "$g_talk_troop"),
   ##diplomacy end+
   (troop_slot_eq, "$g_talk_troop", slot_troop_spouse, "trp_player"),
   (str_store_string, s41, "str_very_well__you_are_now_my_liege_as_well_as_my_husband"),
 (else_try),	#all other situations
   (str_store_string, s41, "str_i_thank_you_reg39my_ladylord"),
 (try_end),
],  "{s41}", "lord_give_conclude_2",
[
#Pretender changes
(assign, ":is_pretender", 0),
 (try_begin),
   (this_or_next|is_between, "$g_talk_troop", pretenders_begin, pretenders_end),
   (troop_slot_eq, "$g_talk_troop", slot_troop_spouse, "trp_player"),
   (neg|faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, "$g_talk_troop"),
   (assign, ":is_pretender", 1),

   (assign, "$supported_pretender", "$g_talk_troop"),
   (troop_get_slot, "$supported_pretender_old_faction", "$g_talk_troop", slot_troop_original_faction),
   (troop_set_faction, "$g_talk_troop", "fac_player_supporters_faction"),
   (faction_set_slot, "fac_player_supporters_faction", slot_faction_leader, "$g_talk_troop"),
   (assign, "$g_talk_troop_faction", "fac_player_supporters_faction"),

   (quest_set_slot, "qst_rebel_against_kingdom", slot_quest_giver_troop, "$g_talk_troop"),
   (quest_set_slot, "qst_rebel_against_kingdom", slot_quest_target_faction, "$supported_pretender_old_faction"),

   (str_store_faction_name_link, s14, "$supported_pretender_old_faction"),
   (str_store_troop_name_link, s13, "$g_talk_troop"),
   (setup_quest_text,"qst_rebel_against_kingdom"),
   (str_store_string, s2, "@You promised to help {s13} claim the overlordship of {s14}."),
   (call_script, "script_start_quest", "qst_rebel_against_kingdom", "$g_talk_troop"),
 (try_end),

(try_begin),
   (eq, "$players_kingdom", "fac_player_supporters_faction"),
   (call_script, "script_deactivate_player_faction"),
   (try_for_range, ":npc", active_npcs_begin, active_npcs_end),
      (store_faction_of_troop, ":npc_faction", ":npc"),
      (eq, ":npc_faction", "fac_player_supporters_faction"),
      (troop_slot_eq, ":npc", slot_troop_occupation, slto_kingdom_hero),
      (call_script, "script_change_troop_faction", ":npc", "$g_talk_troop_faction"),
   (try_end),
(try_end),

 (try_begin),
   (is_between, "$players_oath_renounced_against_kingdom", kingdoms_begin, kingdoms_end),
   (neq, "$players_oath_renounced_against_kingdom", "$g_talk_troop_faction"),
   (store_relation, ":relation", "fac_player_supporters_faction", "$players_oath_renounced_against_kingdom"),
   (val_min, ":relation", -40),
   (call_script, "script_set_player_relation_with_faction", "$players_oath_renounced_against_kingdom", ":relation"),
   (call_script, "script_update_all_notes"),
   (assign, "$g_recalculate_ais", 1),
 (try_end),

 (try_begin),
   (is_between, "$players_kingdom", kingdoms_begin, kingdoms_end),
   (neq, "$players_kingdom", "fac_player_supporters_faction"),
  (neq, "$players_kingdom", "$g_talk_troop_faction"), #ie, don't leave faction if the player is already part of the same kingdom

   (faction_get_slot, ":old_leader", "$players_kingdom", slot_faction_leader),
   (call_script, "script_add_log_entry", logent_renounced_allegiance,   "trp_player",  -1, ":old_leader", "$players_kingdom"),
   (try_begin),
     (eq, ":is_pretender", 1),
     (call_script, "script_activate_player_faction", "$g_talk_troop"),
   (try_end),
   (call_script, "script_player_leave_faction", 0),
 (try_end),

 (call_script, "script_player_join_faction", "$g_talk_troop_faction"),

 (try_begin),
   (gt, "$g_invite_offered_center", 0),
   (call_script, "script_give_center_to_lord", "$g_invite_offered_center", "trp_player", 0),
   (try_begin),
      (faction_slot_eq, "$players_kingdom", slot_faction_political_issue, "$g_invite_offered_center"),
      (faction_set_slot, "$players_kingdom", slot_faction_political_issue, -1),
   (try_end),
 (try_end),
 (call_script, "script_add_log_entry", logent_pledged_allegiance,   "trp_player",  -1, "$g_talk_troop", "$g_talk_troop_faction"),

 (try_begin),
   (check_quest_active, "qst_join_faction"),
   (eq, "$g_invite_faction_lord", "$g_talk_troop"),
   (call_script, "script_end_quest", "qst_join_faction"),
 (else_try),
   (check_quest_active, "qst_join_faction"),
   (call_script, "script_abort_quest", "qst_join_faction", 0),
 (try_end),
 (assign, "$player_has_homage" ,1),
 (assign, "$g_player_banner_granted", 1),
 (assign, "$g_invite_faction", 0),
 (assign, "$g_invite_faction_lord", 0),
 (assign, "$g_invite_offered_center", 0),
 (assign, "$g_leave_encounter",1)]],
[anyone,"lord_give_conclude_2", [
(troop_slot_eq, "$g_talk_troop", slot_troop_spouse, "trp_player"),
#diplomacy start+ either gender PC can marry opposite-gender lords
#load relation text into s0
(call_script, "script_dplmc_print_player_spouse_says_my_husband_wife_to_s0", "$g_talk_troop", 0),
],  "So be it, {s0}. May all my vassals be as valiant and loyal as you.", "close_window", [(assign, "$g_leave_encounter",1)]],
[anyone,"lord_give_conclude_2", [],  "I have great hopes for you {playername}.\
I know you shall prove yourself worthy of the trust I have placed in you.", "close_window", [(assign, "$g_leave_encounter",1)]],
[anyone,"lord_ask_enter_service", [(str_store_faction_name,5,"$g_talk_troop_faction")], "Heh, a wise move,\
{playername}. With loyal service, a {man/woman} in my service could become wealthy and powerful,\
and our enemies... Well, our enemies are as rice before a scythe.\
However, to enter my service you must first renounce all worldly oaths and bonds,\
and swear to serve only the {s5}.", "lord_enter_service_swear",[]],
[anyone|plyr ,"lord_enter_service_swear", [], "I do so swear, {s65}.", "lord_enter_service_swear_accepted",[]],
[anyone|plyr ,"lord_enter_service_swear", [], "I need some time to think about this.", "lord_enter_service_swear_denied",[]],
[anyone ,"lord_enter_service_swear_denied", [], "Are you having me on? I've no time for games, {playername}.\
Make up your mind and stop wasting my time.", "close_window",[(assign, "$g_leave_encounter",1)]],
[anyone ,"lord_enter_service_swear_accepted", [(str_store_faction_name,5,"$g_talk_troop_faction")],
"Then it is my pleasure to welcome you to the service of my house. From this day on, {playername},\
you are a soldier of the {s5} with all the duties and privileges that come with it.", "lord_enter_service_swear_accepted_2",
[
]],
[anyone ,"lord_enter_service_swear_accepted_2", [(str_store_faction_name,5,"$g_talk_troop_faction")],
"I charge you with rooting out and destroying the forces of our enemies wherever you may find them.\
Moreover, I will have special tasks for you from time to time, as may some of my other vassal lords.\
Serve, fight, and honour your oaths. These things will take you far, if you've a mind for promotion.\
May God grant us long lives and many victories to toast in my hall!", "close_window",[(assign, "$g_leave_encounter",1)]],
[anyone,"lord_ask_leave_service", [(ge, "$g_talk_troop_relation", 1)], "Hrm.\
Has your oath become burdensome, {playername}? It is unusual to request release from service,\
but in respect of your fine service, I will not hold you if you truly wish to end it.\
Though you would be sorely missed.", "lord_ask_leave_service_verify",[]],
[anyone,"lord_ask_leave_service", [], "Release from homage? Hmm, perhaps it would be for the best...\
However, {playername}, you must be sure that release is what you desire. This is not a thing done lightly.", "lord_ask_leave_service_verify",[]],
[anyone|plyr ,"lord_ask_leave_service_verify", [], "It is something I must do, {s65}.", "lord_ask_leave_service_2",[]],
[anyone|plyr ,"lord_ask_leave_service_verify", [], "You are right, {s65}. My place is here.", "lord_ask_leave_service_giveup",[]],
[anyone,"lord_ask_leave_service_giveup", [], "I am pleased to hear it, {playername}.\
I hope you'll banish such unworthy thoughts from your mind from now on.", "lord_pretalk",[]],
[anyone,"lord_ask_leave_service_2", [], "Then you are sure? Also, be aware that if you leave my services, you will be surrendering to me all the fiefs which you hold in my name.", "lord_ask_leave_service_verify_again",[]],
[anyone|plyr ,"lord_ask_leave_service_verify_again", [], "Yes, {s65}.", "lord_ask_leave_service_3",[]],
[anyone|plyr ,"lord_ask_leave_service_verify_again", [], "Of course not, {s65}. I am ever your loyal vassal.", "lord_ask_leave_service_giveup",[]],
[anyone,"lord_ask_leave_service_3", [], "As you wish. I hereby declare your oaths to be null and void.\
You will no longer hold land or titles in my name, and you are released from your duties to my house.\
You are free, {playername}.", "lord_ask_leave_service_end",
[
     (call_script, "script_add_log_entry", logent_renounced_allegiance,   "trp_player",  -1, "$g_talk_troop", "$g_talk_troop_faction"),
     (call_script, "script_player_leave_faction", 1), #1 means give back fiefs
 ]],
[anyone|plyr ,"lord_ask_leave_service_end", [], "Thank you, sir. It was an honour to serve you..", "lord_ask_leave_service_end_2",[]],
[anyone|plyr ,"lord_ask_leave_service_end", [], "My thanks. It feels good to be {a free man/free} once again.", "lord_ask_leave_service_end_2",[]],
[anyone ,"lord_ask_leave_service_end_2", [], "Farewell then, {playername}, and good luck go with you.", "close_window",
[(assign, "$g_leave_encounter", 1)]],
[anyone,"lord_active_mission_1", [(store_partner_quest,":lords_quest"),
                                 (eq,":lords_quest","qst_lend_companion"),
                                 #(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 0),
                                 (neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
                                 (check_quest_active,"qst_lend_companion"),
                                 (quest_slot_eq, "qst_lend_companion", slot_quest_giver_troop, "$g_talk_troop"),
                                 (store_current_day, ":cur_day"),
                                 (quest_get_slot, ":quest_target_amount", "qst_lend_companion", slot_quest_target_amount),
                                 (ge, ":cur_day", ":quest_target_amount"),
##                                    (quest_get_slot, ":quest_target_troop", "qst_lend_companion", slot_quest_target_troop),
##                                    (str_store_troop_name,s14,":quest_target_troop"),
##                                    (troop_get_type, reg3, ":quest_target_troop"),
                                 ],
"Oh, you want your companion back? I see...", "lord_lend_companion_end",[]],
[anyone,"lord_active_mission_1", [(store_partner_quest,":lords_quest"),
                        (eq,":lords_quest","qst_lend_companion")],
"{playername}, I must beg your patience, I still have need of your companion. Please return later when things have settled.", "lord_pretalk",[]],
[anyone,"lord_active_mission_1", [], "Yes, have you made any progress on it?", "lord_active_mission_2",[]],
[anyone|plyr,"lord_active_mission_2",[#(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 0),
                         (neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
                         (check_quest_active,"qst_capture_prisoners"),
                         (quest_slot_eq, "qst_capture_prisoners", slot_quest_giver_troop, "$g_talk_troop"),
                         (quest_get_slot, ":quest_target_amount", "qst_capture_prisoners", slot_quest_target_amount),
                         (quest_get_slot, ":quest_target_troop", "qst_capture_prisoners", slot_quest_target_troop),
                         (party_count_prisoners_of_type, ":count_prisoners", "p_main_party", ":quest_target_troop"),
                         (ge, ":count_prisoners", ":quest_target_amount"),
                         (assign, reg1, ":quest_target_amount"),
                         (str_store_troop_name_plural, s1, ":quest_target_troop")],
"Indeed. I brought you {reg1} {s1} as prisoners.", "lord_generic_mission_thank",
[(quest_get_slot, ":quest_target_amount", "qst_capture_prisoners", slot_quest_target_amount),
 (quest_get_slot, ":quest_target_troop", "qst_capture_prisoners", slot_quest_target_troop),
 (party_remove_prisoners, "p_main_party", ":quest_target_troop", ":quest_target_amount"),
 (party_add_prisoners, "$g_encountered_party", ":quest_target_troop", ":quest_target_amount"),
 (call_script, "script_finish_quest", "qst_capture_prisoners", 100)]],
[anyone|plyr,"lord_active_mission_2",
[
  #(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 0),
  (neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
  (store_partner_quest, ":lords_quest"),
  (eq, ":lords_quest", "qst_capture_enemy_hero"),
  (assign, ":has_prisoner", 0),
  (quest_get_slot, ":quest_target_faction", "qst_capture_enemy_hero", slot_quest_target_faction),
  (party_get_num_prisoner_stacks, ":num_stacks", "p_main_party"),
  (try_for_range, ":i_stack", 0, ":num_stacks"),
    (party_prisoner_stack_get_troop_id, ":stack_troop", "p_main_party", ":i_stack"),
    (troop_is_hero, ":stack_troop"),
    (store_troop_faction, ":stack_faction", ":stack_troop"),
    (eq, ":quest_target_faction", ":stack_faction"),
    (troop_slot_eq, ":stack_troop", slot_troop_occupation, slto_kingdom_hero),
    (assign, ":has_prisoner", 1),
    (quest_set_slot, "qst_capture_enemy_hero", slot_quest_target_troop, ":stack_troop"),
  (try_end),
  (eq, ":has_prisoner", 1),
  (str_store_faction_name, s13, ":quest_target_faction")
  ],
"Oh, indeed. I've captured a lord from {s13} for you.", "capture_enemy_hero_thank",
[]],
[anyone|plyr,"lord_active_mission_2", [#(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 0),
										 (neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
                                         (store_partner_quest,":lords_quest"),
                                         (eq,":lords_quest","qst_raise_troops"),
                                         (quest_get_slot, ":quest_target_troop", ":lords_quest", slot_quest_target_troop),
                                         (quest_get_slot, ":quest_target_amount", ":lords_quest", slot_quest_target_amount),
                                         (party_count_companions_of_type, ":num_companions", "p_main_party", ":quest_target_troop"),
                                         (ge, ":num_companions", ":quest_target_amount"),
                                         (assign, reg1, ":quest_target_amount"),
                                         (str_store_troop_name_plural, s13, ":quest_target_troop")],
   "Indeed. I have raised {reg1} {s13}. You can take them.", "lord_raise_troops_thank",[(quest_get_slot, ":quest_target_troop", "qst_raise_troops", slot_quest_target_troop),
                                                                                         (quest_get_slot, ":quest_target_amount", "qst_raise_troops", slot_quest_target_amount),
                                                                                         (call_script,"script_change_player_relation_with_troop","$g_talk_troop", 3),
                                                                                         (party_remove_members, "p_main_party", ":quest_target_troop", ":quest_target_amount"),
                                                                                         (call_script, "script_end_quest", "qst_raise_troops"),
                                                                                         (troop_get_slot, ":cur_lords_party", "$g_talk_troop", slot_troop_leaded_party),
                                                                                         (gt, ":cur_lords_party", 0),
                                                                                         (party_add_members, ":cur_lords_party", ":quest_target_troop", ":quest_target_amount"),
                                                                                         ]],
[anyone,"lord_raise_troops_thank", [],
   "These men may well turn the tide in my plans, {playername}. I am confident you've trained them well. My thanks and my compliments to you.", "lord_raise_troops_thank_2",[]],
[anyone|plyr,"lord_raise_troops_thank_2", [],
   "Well, the men are at your command now, sir. I am sure you will take good care of them.", "lord_pretalk",[]],
[anyone|plyr,"lord_active_mission_2", [#(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 0),
									     (neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),

#                                         (store_partner_quest,":lords_quest"),
#                                         (eq, ":lords_quest", "qst_collect_taxes"),
										  (check_quest_active, "qst_collect_taxes"),
										  (quest_slot_eq, "qst_collect_taxes", slot_quest_giver_troop, "$g_talk_troop"),

                                         (check_quest_succeeded, "qst_collect_taxes"),
                                         (eq, "$qst_collect_taxes_halve_taxes", 0),
                                         (quest_get_slot, ":quest_gold_reward", "qst_collect_taxes", slot_quest_gold_reward),
                                         (store_mul, ":required_gold", ":quest_gold_reward", 8),
                                         (val_div, ":required_gold", 10),
                                         (store_troop_gold, ":gold", "trp_player"),
                                         (ge, ":gold", ":required_gold"),
                                         (assign, reg19, ":quest_gold_reward"),
                                         (quest_get_slot, ":quest_target_center", "qst_collect_taxes", slot_quest_target_center),
                                         (str_store_party_name, s3, ":quest_target_center"),
                                         ],
   "Here are all the taxes from {s3}. It comes up to {reg19} mon.", "lord_collect_taxes_success",
   []],
[anyone|plyr,"lord_active_mission_2", [#(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 0),
                                         (neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
										  (check_quest_active, "qst_collect_taxes"),
										  (quest_slot_eq, "qst_collect_taxes", slot_quest_giver_troop, "$g_talk_troop"),

#                                         (store_partner_quest,":lords_quest"),
#                                         (eq, ":lords_quest", "qst_collect_taxes"),
                                         (check_quest_succeeded, "qst_collect_taxes"),
                                         (eq, "$qst_collect_taxes_halve_taxes", 1),
                                         (quest_get_slot, ":quest_gold_reward", "qst_collect_taxes", slot_quest_gold_reward),
                                         (store_mul, ":required_gold", ":quest_gold_reward", 95),
                                         (val_div, ":required_gold", 100),
                                         (store_troop_gold, ":gold", "trp_player"),
                                         (ge, ":gold", ":required_gold"),
                                         (assign, reg19, ":quest_gold_reward"),
                                         (quest_get_slot, ":quest_target_center", "qst_collect_taxes", slot_quest_target_center),
                                         (str_store_party_name, s3, ":quest_target_center"),
                                         ],
   "Here are the taxes from {s3}. It comes up to {reg19} mon.", "lord_collect_taxes_half_success",
   []],
[anyone|plyr,"lord_active_mission_2", [#(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 0),
										 (neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
										  (check_quest_active, "qst_collect_taxes"),
										  (quest_slot_eq, "qst_collect_taxes", slot_quest_giver_troop, "$g_talk_troop"),

#                                         (store_partner_quest,":lords_quest"),
#                                         (eq, ":lords_quest", "qst_collect_taxes"),
                                         (check_quest_failed, "qst_collect_taxes"),
                                         (quest_get_slot, ":quest_gold_reward", "qst_collect_taxes", slot_quest_gold_reward),
                                         (store_troop_gold, ":gold", "trp_player"),
                                         (ge, ":gold", ":quest_gold_reward"),
                                         (assign, reg19, ":quest_gold_reward"),
                                         (quest_get_slot, ":quest_target_center", "qst_collect_taxes", slot_quest_target_center),
                                         (str_store_party_name, s3, ":quest_target_center"),
                                         ],
   "Unfortunately, a revolt broke up while I was collecting the taxes.\
 I could only collect {reg19} mon.", "lord_collect_taxes_fail",
   []],
[anyone,"lord_collect_taxes_success", [(quest_get_slot, ":total_revenue", "qst_collect_taxes", slot_quest_gold_reward),
                                         (store_mul, ":owner_share", ":total_revenue", 8),
                                         (val_div, ":owner_share", 10),
                                         (assign, reg20, ":owner_share"),
                                         (store_sub, reg21, ":total_revenue", ":owner_share")],
   "Well done, {playername}, very well done indeed! You were truly the right {man/person} for the job.\
 I promised you a fifth of the taxes, so that amounts to {reg21} mon.\
 If you give me {reg20} mon, you may keep the difference.\
 A good result for everyone, eh?", "lord_pretalk",
   [
    (troop_remove_gold, "trp_player", reg20),
    ##diplomacy start+ actually give taxes to NPC
    (call_script, "script_dplmc_distribute_gold_to_lord_and_holdings", reg20, "$g_talk_troop"),
    ##diplomacy end+
    (quest_set_slot, "qst_collect_taxes", slot_quest_gold_reward, 0),
    (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 2),
    (call_script, "script_end_quest", "qst_collect_taxes"),
    ]],
[anyone,"lord_collect_taxes_half_success", [(quest_get_slot, ":gold_reward", "qst_collect_taxes", slot_quest_gold_reward),
                                         (val_mul, ":gold_reward", 95),
                                         (val_div, ":gold_reward", 100),
                                         (assign, reg20, ":gold_reward")],
   "What?! Is this some scheme of yours, {playername}? That's less than half the taxes I'm owed!\
 You have let them get away with murder as well as my money. What a farce!\
 You can forget the money I promised you, I'm taking {reg20} mon from what you collected,\
 and you're lucky I'm leaving you a few coins for honour's sake.", "lord_pretalk",
   [(troop_remove_gold, "trp_player", reg20),
    ##diplomacy start+ actually give taxes to NPC
    (call_script, "script_dplmc_distribute_gold_to_lord_and_holdings", reg20, "$g_talk_troop"),
    ##diplomacy end+
    (quest_set_slot, "qst_collect_taxes", slot_quest_gold_reward, 0),
    (call_script, "script_end_quest", "qst_collect_taxes"),
    ]],
[anyone,"lord_collect_taxes_fail", [],
   "God, what a bloody mess you've gotten us into, {playername}.\
This could turn very ugly if I do not take immediate action.\
I certainly hope you're not here expecting to be paid for failure.\
Hand over my {reg19} mon, if you please, and end our business together.", "lord_pretalk",
   [(call_script, "script_change_player_relation_with_troop", "$g_talk_troop", -1),
    (quest_get_slot, ":gold_reward", "qst_collect_taxes", slot_quest_gold_reward),
    (troop_remove_gold, "trp_player", ":gold_reward"),
	##diplomacy start+ actually give taxes to NPC
    (call_script, "script_dplmc_distribute_gold_to_lord_and_holdings", ":gold_reward", "$g_talk_troop"),
    ##diplomacy end+
    (quest_set_slot, "qst_collect_taxes", slot_quest_gold_reward, 0),
    (call_script, "script_end_quest", "qst_collect_taxes"),
    ]],
[anyone|plyr,"lord_active_mission_2", [ (check_quest_active, "qst_hunt_down_fugitive"),
										  (quest_slot_eq, "qst_hunt_down_fugitive", slot_quest_giver_troop, "$g_talk_troop"),

                                         (check_quest_succeeded, "qst_hunt_down_fugitive"),
                                         (quest_get_slot, ":quest_target_center", "qst_hunt_down_fugitive", slot_quest_target_center),
                                         (str_store_party_name, s3, ":quest_target_center"),
                                         (quest_get_slot, ":quest_target_dna", "qst_hunt_down_fugitive", slot_quest_target_dna),
                                         (call_script, "script_get_name_from_dna_to_s50", ":quest_target_dna"),
                                         (str_store_string, s4, s50),],
   "I found {s4} hiding at {s3} and gave him his punishment.", "lord_hunt_down_fugitive_success",
   []],
[anyone|plyr,"lord_active_mission_2", [
										(check_quest_active, "qst_hunt_down_fugitive"),
										(quest_slot_eq, "qst_hunt_down_fugitive", slot_quest_giver_troop, "$g_talk_troop"),

                                         (check_quest_failed, "qst_hunt_down_fugitive"),
                                         ],
   "I'm afraid he got away.", "lord_hunt_down_fugitive_fail",
   []],
[anyone,"lord_hunt_down_fugitive_success", [],
   "And we'll all be a lot better off without him! Thank you, {playername},\
 for removing this long-festering thorn from my side. 'Tis good to know you can be trusted to handle things\
 with an appropriate level of tactfulness.\
 A bounty I promised, and a bounty you shall have. 300 mon and not a copper less!", "lord_hunt_down_fugitive_success_2",
   [
     (add_xp_as_reward, 300),
    ]],
[anyone|plyr,"lord_hunt_down_fugitive_success_2", [],
   "Let me take the money, {s65}. Thank you.", "lord_hunt_down_fugitive_reward_accept",[]],
[anyone|plyr,"lord_hunt_down_fugitive_success_2", [],
   "This is blood money. I can't accept it.", "lord_hunt_down_fugitive_reward_reject",[]],
[anyone,"lord_hunt_down_fugitive_reward_accept", [],
   "Of course, {playername}. Here you are. Once again, you've my thanks for ridding me of that {s43}.", "lord_pretalk",[
		(call_script, "script_lord_comment_to_s43", "$g_talk_troop", "str_lord_insult_default"),

		(call_script, "script_troop_add_gold", "trp_player", 300),
		(call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 1),
		(call_script, "script_end_quest", "qst_hunt_down_fugitive"),
		]],
[anyone,"lord_hunt_down_fugitive_reward_reject", [],
   "You are a {man/woman} for whom justice is its own reward, eh? As you wish it, {playername}, as you wish it.\
 An honourable sentiment, to be true. Regardless, you've my thanks for ridding me of that {s43}.", "lord_pretalk",[

 		(call_script, "script_lord_comment_to_s43", "$g_talk_troop", "str_lord_insult_default"),


       (call_script, "script_change_player_honor", 3),
       (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 1),
       (call_script, "script_end_quest", "qst_hunt_down_fugitive"),
       ]],
[anyone,"lord_hunt_down_fugitive_fail", [],
   "It is a sad day when that {s43} manages to avoid the hand of justice yet again.\
 I thought you would be able to do this, {playername}. Clearly I was wrong.", "lord_pretalk",
   [
 	(call_script, "script_lord_comment_to_s43", "$g_talk_troop", "str_lord_insult_default"),

    (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", -1),
    (call_script, "script_end_quest", "qst_hunt_down_fugitive"),
    ]],
[anyone|plyr,"lord_active_mission_2",[(store_partner_quest,":lords_quest"),
                                        (eq, ":lords_quest", "qst_deliver_cattle_to_army"),
                                        (quest_get_slot, ":quest_target_amount", "qst_deliver_cattle_to_army", slot_quest_target_amount),
                                        (call_script, "script_get_troop_item_amount", "trp_player", "itm_bread"),
                                        (assign, ":cur_amount", reg0),
                                        (ge, ":cur_amount", ":quest_target_amount"),
                                        (assign, reg5, ":quest_target_amount"),
                                        ],
   "Indeed. I brought you {reg5} sacks of white rice.", "lord_deliver_cattle_to_army_thank",
   []],
[anyone,"lord_deliver_cattle_to_army_thank", [],
   "Ah, {playername}. My quartermaster will take your delivery right away. I'm impressed.", "lord_deliver_cattle_to_army_thank_2",
   [(quest_get_slot, ":quest_target_amount", "qst_deliver_cattle_to_army", slot_quest_target_amount),
    (troop_remove_items, "trp_player", "itm_bread", ":quest_target_amount"),
	(call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 2),
	(store_mul, ":reward", ":quest_target_amount", 80),
	(call_script, "script_troop_add_gold", "trp_player", ":reward"),
	(val_div, ":reward", 5),
	(add_xp_as_reward, ":reward"),
    (call_script, "script_end_quest", "qst_deliver_cattle_to_army"),
	#Reactivating follow army quest
	(str_store_troop_name_link, s9, "$g_talk_troop"),
	(setup_quest_text, "qst_follow_army"),
	(str_store_string, s2, "str_follow_army_quest_brief_2"),
	(call_script, "script_start_quest", "qst_follow_army", "$g_talk_troop"),
	(assign, "$g_player_follow_army_warnings", 0),
   ]],
[anyone|plyr, "lord_deliver_cattle_to_army_thank_2", [],
   "Not a problem, {s65}.", "lord_pretalk",[]],
[anyone|plyr, "lord_deliver_cattle_to_army_thank_2", [],
   "Glad to be of service.", "lord_pretalk",[]],
[anyone|plyr, "lord_deliver_cattle_to_army_thank_2", [],
   "Mere child's play.", "lord_pretalk",[]],
[anyone|plyr,"lord_active_mission_2", [], "I am still working on it.", "lord_active_mission_3",[]],
[anyone|plyr,"lord_active_mission_2", [], "I am afraid I won't be able to do this quest.", "lord_mission_failed",[]],
[anyone,"lord_active_mission_3", [], "Good. Remember, I am counting on you.", "lord_pretalk",[]],
[anyone,"lord_mission_failed", [], "{s43}", "lord_pretalk",
   [
    (call_script, "script_lord_comment_to_s43", "$g_talk_troop", "str_lord_mission_failed_default"),
    (store_partner_quest,":lords_quest"),
    (call_script, "script_abort_quest", ":lords_quest", 1)]],
[anyone,"lord_suggest_action_ask", [],
   "{!}What do you suggest?", "lord_suggest_action",[]],
[anyone|plyr,"lord_suggest_action", [],
   "{!}CHEAT: I want to join your faction.", "lord_suggest_join_faction",[]],
[anyone,"lord_suggest_join_faction", [],
   "{!}Alright then.", "lord_give_oath_5",[]],
[anyone|plyr,"lord_suggest_action", [],
   "{!}CHEAT: I want to know your leaded party ID.", "lord_suggest_learn_party_id",[]],
[anyone,"lord_suggest_learn_party_id", [
  (assign, reg1, "$g_encountered_party"),
  (troop_get_slot, reg0, "$g_talk_troop", slot_troop_leaded_party)],
   "{!}It is {reg0}. Encountered party is {reg1}", "lord_pretalk",[]],
[anyone|plyr,"lord_suggest_action", [],
   "{!}CHEAT: I want to know your AI initiative.", "lord_suggest_learn_ai_initiative",[]],
[anyone,"lord_suggest_learn_ai_initiative", [(party_get_ai_initiative, reg0, "$g_encountered_party")],
   "{!}It is {reg0}.", "lord_pretalk",[]],
[anyone|plyr,"lord_suggest_action", [(eq, "$players_kingdom", "$g_talk_troop_faction"),],
   "{!}CHEAT: I want to be your clan's strategist.", "lord_suggest_become_marshall",[]],
[anyone,"lord_suggest_become_marshall", [],
   "{!}Alright then.", "lord_pretalk",
   [
     (faction_get_slot, ":old_marshall", "$g_talk_troop_faction", slot_faction_marshall),
        (try_begin),
          (ge, ":old_marshall", 0),
		  (troop_get_slot, ":old_marshall_party", ":old_marshall", slot_troop_leaded_party),
          (party_is_active, ":old_marshall_party"),
          (party_set_marshall, ":old_marshall_party", 0),
        (try_end),

     (faction_set_slot, "$g_talk_troop_faction", slot_faction_marshall, "trp_player"),
     (faction_set_slot, "$g_talk_troop_faction", slot_faction_ai_state, sfai_default),
     (assign, "$g_recalculate_ais", 1),
   ]],
[anyone|plyr,"lord_suggest_action", [(neq, "$talk_context", tc_siege_commander)],
   "{!}CHEAT: Let us attack an enemy town or castle.", "lord_suggest_attack_enemy_castle",[]],
[anyone|plyr,"lord_suggest_action", [(neq, "$talk_context", tc_siege_commander)],
   "{!}CHEAT: Let us return back to a friendly town.", "lord_suggest_go_to_friendly_town",[]],
[anyone|plyr,"lord_suggest_action", [(neq, "$talk_context", tc_siege_commander)],
   "{!}CHEAT: Let us attack an enemy war party.", "lord_suggest_attack_enemy_party",[]],
[anyone|plyr,"lord_suggest_action", [(eq, "$talk_context", tc_siege_commander)],
   "{!}CHEAT: Let us lift this siege.", "lord_suggest_lift_siege",[]],
[anyone|plyr,"lord_suggest_action", [(neq, "$talk_context", tc_siege_commander)],
   "{!}CHEAT: Follow me.", "lord_suggest_follow_me",[]],
[anyone|plyr,"lord_suggest_action", [(neq, "$talk_context", tc_siege_commander)],
   "{!}CHEAT: Follow someone.", "lord_suggest_follow_other",[]],
[anyone|plyr,"lord_suggest_action", [(neq, "$talk_context", tc_siege_commander)],
   "{!}CHEAT: Raid a village.", "lord_suggest_raid_village",[]],
[anyone|plyr,"lord_suggest_action", [],
   "{!}CHEAT: Like me.", "lord_pretalk",[(call_script,"script_change_player_relation_with_troop","$g_talk_troop",20)]],
[anyone,"lord_suggest_lift_siege", [],
   "{!}As you wish, {playername}.", "close_window",[(call_script, "script_party_set_ai_state", "$g_talk_troop_party", spai_undefined),
                                           (party_leave_cur_battle, "$g_talk_troop_party"),
                                           (assign, "$g_leave_encounter", 1)]],
[anyone,"lord_suggest_go_to_friendly_town", [],
   "{!}Hmm. Which town or castle do you suggest we go to?", "lord_suggest_go_to_friendly_town2",[]],
[anyone|plyr|repeat_for_parties,"lord_suggest_go_to_friendly_town2", [
                                                                       (store_repeat_object, ":center_no"),
                                                                       (this_or_next|party_slot_eq,":center_no",slot_party_type, spt_castle),
                                                                       (party_slot_eq,":center_no",slot_party_type, spt_town),
                                                                       (neq, ":center_no", "$g_encountered_party"),
                                                                       (store_faction_of_party, ":town_faction", ":center_no"),
                                                                       (eq, ":town_faction", "$g_talk_troop_faction"),
                                                                       (str_store_party_name, s1, ":center_no")],
   "{!}CHEAT: {s1}", "lord_suggest_go_to_friendly_town3",[(store_repeat_object, "$town_suggested_to_go_to")]],
[anyone|plyr,"lord_suggest_go_to_friendly_town2", [],
   "{!}CHEAT: Never mind.", "lord_pretalk",[]],
[anyone,"lord_suggest_go_to_friendly_town3", [(str_store_party_name, 1, "$town_suggested_to_go_to")],
   "{!}Very well, we go to {s1}.", "lord_pretalk",
   [
       (call_script, "script_party_set_ai_state", "$g_talk_troop_party", spai_holding_center, "$town_suggested_to_go_to"),
       ]],
[anyone,"lord_suggest_attack_enemy_party", [],
   "{!}Hmm. Which party do you suggest we attack?", "lord_suggest_attack_enemy_party2",[]],
[anyone|plyr|repeat_for_parties,"lord_suggest_attack_enemy_party2", [
                                                                       (store_repeat_object, ":party_no"),
                                                                       (party_slot_eq,":party_no",slot_party_type, spt_kingdom_hero_party),
                                                                       (party_is_active, ":party_no"),
                                                                       (store_faction_of_party, ":party_faction", ":party_no"),
                                                                       (store_relation, ":party_relation", ":party_faction", "$g_talk_troop_faction"),
                                                                       (le, ":party_relation", -10),
                                                                       (call_script, "script_get_closest_walled_center", ":party_no"),
                                                                       (assign, ":center_no", reg0),
                                                                       (str_store_party_name, s3, ":center_no"),
                                                                       (str_store_faction_name, s2, ":party_faction"),
                                                                       (str_store_party_name, s1, ":party_no")],
   "{!}CHEAT: {s1} of {s2} around {s3}", "lord_suggest_attack_enemy_party3",[(store_repeat_object, "$suggested_to_attack_party")]],
[anyone|plyr,"lord_suggest_attack_enemy_party2", [],
   "{!}CHEAT: Never mind.", "lord_pretalk",[]],
[anyone,"lord_suggest_attack_enemy_party3", [(str_store_party_name, 1, "$suggested_to_attack_party")],
   "{!}As you wish, we will attack {s1}.", "lord_pretalk",
   [
       (call_script, "script_party_set_ai_state", "$g_talk_troop_party", spai_engaging_army, "$suggested_to_attack_party"),
       ]],
[anyone,"lord_suggest_attack_enemy_castle", [],
   "{!}Hmm. Which one do you suggest we attack?", "lord_suggets_attack_enemy_castle2",[]],
[anyone|plyr|repeat_for_parties,"lord_suggets_attack_enemy_castle2", [
                                                                       (store_repeat_object, ":center_no"),
                                                                       (this_or_next|party_slot_eq,":center_no",slot_party_type, spt_castle),
                                                                       (party_slot_eq,":center_no",slot_party_type, spt_town),
                                                                       (store_faction_of_party, ":town_faction", ":center_no"),
                                                                       (store_relation, ":town_relation", ":town_faction", "$g_talk_troop_faction"),
                                                                       (le, ":town_relation", -10),
                                                                       (str_store_faction_name, s2, ":town_faction"),
                                                                       (str_store_party_name, s1, ":center_no")],
   "{!}CHEAT: {s1} of {s2}", "lord_suggets_attack_enemy_castle3",[(store_repeat_object, "$suggested_to_attack_center")]],
[anyone|plyr,"lord_suggets_attack_enemy_castle2", [],
   "{!}CHEAT: Never mind my lord.", "lord_pretalk",[]],
[anyone,"lord_suggets_attack_enemy_castle3", [(str_store_party_name, 1, "$suggested_to_attack_center")],
   "That should be possible. Very well, we'll attack {s1}.", "lord_pretalk",
   [
       (call_script, "script_party_set_ai_state", "$g_talk_troop_party", spai_besieging_center, "$suggested_to_attack_center"),

       ]],
[anyone,"lord_suggest_raid_village", [],
   "{!}Hmm. Which village do you suggest we attack?", "lord_suggest_raid_village_2",[]],
[anyone|plyr|repeat_for_parties,"lord_suggest_raid_village_2", [
                                                                       (store_repeat_object, ":center_no"),
                                                                       (party_slot_eq,":center_no",slot_party_type, spt_village),
                                                                       (store_faction_of_party, ":town_faction", ":center_no"),
                                                                       (store_relation, ":town_relation", ":town_faction", "$g_talk_troop_faction"),
                                                                       (le, ":town_relation", -10),
                                                                       (str_store_faction_name, s2, ":town_faction"),
                                                                       (str_store_party_name, s1, ":center_no")],
   "{!}CHEAT: {s1} of {s2}", "lord_suggest_raid_village_3",[(store_repeat_object, "$suggested_to_attack_center")]],
[anyone|plyr,"lord_suggest_raid_village_2", [],
   "{!}CHEAT: Never mind.", "lord_pretalk",[]],
[anyone,"lord_suggest_raid_village_3", [(str_store_party_name, s1, "$suggested_to_attack_center")],
   "{!}That should be possible. Very well, we'll attack {s1}.", "lord_pretalk",
   [
     (call_script, "script_party_set_ai_state", "$g_talk_troop_party", spai_raiding_around_center, "$suggested_to_attack_center"),
   ]],
[anyone,"lord_suggest_follow_me", [],
   "{!}Aye, I'll follow you.", "lord_pretalk",
   [
     (party_set_slot, "$g_talk_troop_party", slot_party_commander_party, "p_main_party"),
     #(call_script, "script_party_decide_next_ai_state_under_command", "$g_talk_troop_party")
     (call_script, "script_npc_decision_checklist_party_ai", "$g_talk_troop"),
	 (call_script, "script_party_set_ai_state", "$g_talk_troop_party", reg0, reg1),
   ]],
[anyone,"lord_suggest_follow_other", [],
   "{!}Who do you want me to follow?", "lord_suggest_follow_other_2",[]],
[anyone|plyr|repeat_for_parties,"lord_suggest_follow_other_2", [
                                                                       (store_repeat_object, ":party_no"),
                                                                       (party_slot_eq,":party_no",slot_party_type, spt_kingdom_hero_party),
                                                                       (neq, ":party_no", "$g_talk_troop"),
                                                                       (store_faction_of_party, ":party_faction", ":party_no"),
                                                                       (eq, ":party_faction", "$g_talk_troop_faction"),
                                                                       (str_store_party_name, s1, ":party_no")],
   "{!}CHEAT: {s1}", "lord_suggest_follow_other_3",[(store_repeat_object, "$town_suggested_to_go_to")]],
[anyone|plyr,"lord_suggest_follow_other_2", [],
   "{!}CHEAT: Never mind.", "lord_pretalk",[]],
[anyone,"lord_suggest_follow_other_3", [(str_store_party_name, 1, "$town_suggested_to_go_to")],
   "{!}As you wish, I shall be accompanying {s1}.", "lord_pretalk",
   [
     (party_set_slot, "$g_talk_troop_party", slot_party_commander_party, "$town_suggested_to_go_to"),
     #(call_script, "script_party_decide_next_ai_state_under_command", "$g_talk_troop_party"),
     (call_script, "script_npc_decision_checklist_party_ai", "$g_talk_troop"),
     (call_script, "script_party_set_ai_state", "$g_talk_troop_party", reg0, reg1),
   ]],
[anyone|plyr,"lord_suggest_action", [],
   "{!}CHEAT: Nothing, {s65}. It's not important.", "lord_pretalk",[]],
[anyone|auto_proceed,"lord_request_mission_ask",
   [(eq, "$players_kingdom", 0),
    (ge, "$g_talk_troop_faction_relation", 0),
    (ge, "$g_talk_troop_relation", 0),
    (troop_slot_ge, "trp_player", slot_troop_renown, 30),
    (neg|faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, "$g_talk_troop"),
    (faction_get_slot, ":last_offer_time", "$g_talk_troop_faction", slot_faction_last_mercenary_offer_time),

    (assign, ":num_enemies", 0),
    (try_for_range, ":faction_no", kingdoms_begin, kingdoms_end),
      (faction_slot_eq, "$g_talk_troop_faction", slot_faction_state, sfs_active),
      (store_relation, ":reln", "$g_talk_troop_faction", ":faction_no"),
      (lt, ":reln", 0),
      (val_add, ":num_enemies", 1),
    (try_end),
    (ge, ":num_enemies", 1),
    (store_current_hours, ":cur_hours"),
    (store_add,  ":week_past_last_offer_time", ":last_offer_time", 7 * 24),
    (val_add,  ":last_offer_time", 24),
    (ge, ":cur_hours", ":last_offer_time"),
    (store_random_in_range, ":rand", 0, 100),
    (this_or_next|lt, ":rand", 20),
		(ge, ":cur_hours", ":week_past_last_offer_time"),


	##diplomacy start+
	##OLD:
	#(troop_get_type, ":type", "trp_player"),
	#(this_or_next|eq, ":type", 0),
	##NEW:
   	(assign, reg0, 0),
	(try_begin),
		(call_script, "script_cf_dplmc_faction_has_bias_against_gender", "$g_talk_troop_faction", "$character_gender"),
       	(assign, reg0, 1),
	(try_end),
	#gekokujo 75 renown to be mercenary
	(try_begin),
		(neg|troop_slot_ge, "trp_player", slot_troop_renown, 75),
		(assign, reg0, 1),
	(try_end),
	(this_or_next|eq, reg0, 0),
	(this_or_next|ge, "$g_disable_condescending_comments", 2),#<- OPTION: Disable prejudice
	(this_or_next|troop_slot_ge, "$g_talk_troop", slot_lord_reputation_type, lrep_roguish),
	##diplomacy end+ xxx TODO: Why exactly wouldn't this display...?
	(this_or_next|troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_cunning),
		(troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_goodnatured),
    ],
   "{!}Warning: This line should never display.", "lord_propose_mercenary",[(store_current_hours, ":cur_hours"),
                                  (faction_set_slot, "$g_talk_troop_faction", slot_faction_last_mercenary_offer_time,  ":cur_hours")]],
[anyone,"lord_propose_mercenary", [(call_script, "script_party_calculate_strength", "p_main_party", 0),
                                     (assign, ":offer_value", reg0),
                                     (val_add, ":offer_value", 100),
                                     (call_script, "script_round_value", ":offer_value"),
                                     (assign, ":offer_value", reg0),
                                     (assign, "$temp", ":offer_value"),
                                     (faction_get_slot, ":faction_leader", "$g_talk_troop_faction", slot_faction_leader),
                                     (neq, ":faction_leader", "$g_talk_troop"),
                                     (str_store_faction_name, s9, "$g_talk_troop_faction"),
                                     (str_store_troop_name, s10, ":faction_leader"),

									 ##diplomacy start+
									 #(troop_get_type, ":is_female", "trp_player"),
									 ##diplomacy end+
									 (try_begin),
										##diplomacy start+
										#Enable if prejudice has been set to "high"
										(lt, "$g_disable_condescending_comments", 0),
										(neq, reg65, "$character_gender"),
										(call_script, "script_cf_dplmc_faction_has_bias_against_gender", "$g_talk_troop_faction", "$character_gender"),
										#(eq, ":is_female", 3), #disabled
										##diplomacy end+
										(troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_martial),
									    (str_store_string, s11, "str_now_some_might_say_that_women_have_no_business_leading_mercenary_companies_but_i_suspect_that_you_would_prove_them_wrong_what_do_you_say"),
									 (else_try),
									    (str_store_string, s11, "@What do you say to temporarily entering the service of {s9} as a ronin?\
 I have no doubt that you would be up to the task."),
									 (try_end)
									 ],

   "As it happens, {playername}, I promised {s10} that I would hire a company of ronin for an upcoming campaign.\
","lord_mercenary_service", []],
[anyone|plyr,"lord_mercenary_service", [], "I'm not interested, thank you.", "lord_mercenary_service_reject", []],
[anyone|plyr,"lord_mercenary_service", [], "Aye, I'll join {s9}.", "lord_mercenary_service_accept", []],
[anyone|plyr,"lord_mercenary_service", [], "I'm interested. Please tell me more.", "lord_mercenary_elaborate_pay", []],
[anyone,"lord_mercenary_service_accept", [(str_store_faction_name, s9, "$g_talk_troop_faction")],
   "Perfect. Of course you shall have to make a formal declaration of allegiance,\
 and give your oath that you and your company will remain in service to {s9}\
 for a period of no less than one month.", "lord_mercenary_service_verify", []],
[anyone|plyr,"lord_mercenary_service_verify", [], "As you wish. Your enemies are my enemies.", "lord_mercenary_service_verify_2", []],
[anyone|plyr,"lord_mercenary_service_verify", [], "On second thought, forget it.", "lord_mercenary_service_reject", []],
[anyone,"lord_mercenary_service_verify_2", [], "That will do. You've made a wise choice, my friend.\
 {s9} does well by its loyal fighters, you will receive many rewards for your service.", "lord_mercenary_service_accept_3", [
     (call_script, "script_troop_add_gold", "trp_player", "$temp"),
     (store_current_day, ":cur_day"),
     (store_add, "$mercenary_service_next_renew_day", ":cur_day", 30),
     (call_script, "script_player_join_faction", "$g_talk_troop_faction"),
     (str_store_faction_name, s9, "$g_talk_troop_faction"),]],
[anyone,"lord_mercenary_service_accept_3", [], "Now, I suggest you prepare for a serious campaign.\
 Train and equip your retainers as best you can in the meantime, and respond quickly when you are summoned for duty.", "lord_pretalk", []],
[anyone,"lord_mercenary_service_reject", [(str_store_faction_name, s9, "$g_talk_troop_faction")],
   "I'm very sorry to hear that. You'll find no better place than {s9}, be sure of that.", "lord_pretalk", []],
[anyone,"lord_mercenary_elaborate_pay", [(assign, reg12, "$temp")],
   "I can offer you a contract for one month. At the end of this period, it can be extended on a monthly basis.\
 An initial sum of {reg12} mon will be paid to you to seal the contract.\
 After that, you'll receive wages from {s10} each week, according to the number and quality of the soldiers in your company.\
 You still have your rights to battlefield loot and salvage, as well as any prisoners you capture.\
 War can be very profitable at times...", "lord_mercenary_elaborate_1",
   [(faction_get_slot, ":faction_leader", "$g_talk_troop_faction", slot_faction_leader),
    (str_store_troop_name, s10, ":faction_leader")]],
[anyone,"lord_mercenary_service_elaborate_duty", [],
   "Duties... There are only a few, none of them difficult. The very first thing is to declare your allegiance.\
 An oath of loyalty to our cause. Once that's done, you shall be required to fulfill certain responsibilities.\
 You'll participate in military campaigns, fulfill any duties given to you by your commanders,\
 and most of all you shall attack the enemies of our kingdom wherever you might find them.", "lord_mercenary_elaborate_1",
   [(faction_get_slot, ":faction_leader", "$g_talk_troop_faction", slot_faction_leader),
    (str_store_troop_name, s10, ":faction_leader")]],
[anyone|plyr,"lord_mercenary_elaborate_1", [], "And what about my duties?", "lord_mercenary_service_elaborate_duty", []],
[anyone|plyr,"lord_mercenary_elaborate_1", [], "Can I hold on to any castles I take?", "lord_mercenary_elaborate_castle", []],
[anyone|plyr,"lord_mercenary_elaborate_1",
   [
     (neg|troop_slot_ge, "trp_player", slot_troop_banner_scene_prop, 1),
#custom_banner begin
##    (eq, "trp_player", slot_troop_custom_banner_flag_type, -1),
#custom_banner end
     ], "Can I fly my own banner?", "lord_mercenary_elaborate_banner", []],
[anyone|plyr,"lord_mercenary_elaborate_1", [], "How much will you pay me for my service?", "lord_mercenary_elaborate_pay", []],
[anyone|plyr,"lord_mercenary_elaborate_1", [], "Sounds good. I wish to enter your service as a ronin.", "lord_mercenary_service_accept", []],
[anyone|plyr,"lord_mercenary_elaborate_1", [], "Apologies, my sword is not for hire.", "lord_mercenary_service_reject", []],
[anyone,"lord_mercenary_elaborate_castle", [##diplomacy start+
  ##OLD:
  #(troop_get_type, ":type", "trp_player"),(eq, ":type", 1),
  #(faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, "$g_talk_troop")
  #NEW:
  ##Disable if sexism is off.  Also check that it's true.
  (lt, "$g_disable_condescending_comments", 2),#<- OPTION: >= 2 means disable sexism
  (faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, "$g_talk_troop"),

  (call_script, "script_cf_dplmc_faction_has_bias_against_gender", "$g_talk_troop_faction", "$character_gender"),

  #(assign, ":same_gender_vassal", active_npcs_end),
  #(try_for_range, ":active_npc", active_npcs_begin, ":same_gender_vassal"),
  #  (troop_slot_eq, ":active_npc", slot_troop_occupation, slto_kingdom_hero),
  #  (store_troop_faction, ":faction_no"),
  #  (this_or_next|troop_slot_eq, ":active_npc", slot_troop_original_faction, "$g_talk_troop_faction"),
  #     (eq, ":faction_no", "$g_talk_troop_faction"),
  #  (call_script, "script_dplmc_store_troop_is_female", ":active_npc"),
  #  (eq, reg0, "$character_gender"),
  #  (assign, ":same_gender_vassal", ":active_npc"),
  #(try_end),
  #(neg|is_between, ":same_gender_vassal", active_npcs_begin, active_npcs_end),
  ],#next line, replace "men" with "{women/men}"
   "Only my loyal vassals can own lands and castles in my domain -- and all my vassals are {women/men}. I am not inclined to depart from this tradition without a very good reason. If you prove yourself in battle, you can swear an oath of loyalty to me and become my vassal. We may then discuss how you may obtain a castle.",
##diplomacy end+
   "lord_mercenary_elaborate_1", []],
[anyone,"lord_mercenary_elaborate_castle", [##diplomacy start+
  ##OLD:
  #(troop_get_type, ":type", "trp_player"),(eq, ":type", 1),
  ##NEW:
  ##Disable is sexism is off.  Also check that it's true.
  (lt, "$g_disable_condescending_comments", 2),#<- OPTION: >= 2 means disable sexism
  (call_script, "script_cf_dplmc_faction_has_bias_against_gender", "$g_talk_troop_faction", "$character_gender"),

  (call_script, "script_dplmc_print_cultural_word_to_sreg", "$g_talk_troop", DPLMC_CULTURAL_TERM_KING_PLURAL, 0),#kings to s0
  (faction_get_slot, reg0, "$g_talk_troop_faction", slot_faction_leader),
  (call_script, "script_dplmc_store_troop_is_female", reg0),#faction leader gender to reg0
  (try_begin),
     (eq, reg0, 1),
     (call_script, "script_dplmc_print_cultural_word_to_sreg", "$g_talk_troop", DPLMC_CULTURAL_TERM_KING_FEMALE, 1),#queen to s1
  (else_try),
     (call_script, "script_dplmc_print_cultural_word_to_sreg", "$g_talk_troop", DPLMC_CULTURAL_TERM_KING, 1),#king to s1
  (try_end),
  ],#Next line, use cultural terms, fix gender, etc.
#   "Hmm... Only loyal vassals of {s10} can own lands and castles. While kings will sometimes accept vassalage from men who prove themselves in battle, and grant them land, I have never heard of a king who gave fiefs to women. You had best discuss that issue with {s10} himself.",
   "Hmm... Only loyal vassals of {s10} can own lands and castles. While {s0} will sometimes accept vassalage from {men/women} who prove themselves in battle, and grant them land, I have never heard of a {s1} who gave fiefs to {men/women}. You had best discuss that issue with {s10} {reg0?herself:himself}.",
##diplomacy end+
   "lord_mercenary_elaborate_1", []],
[anyone,"lord_mercenary_elaborate_castle", [(faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, "$g_talk_troop")],
   "Only my loyal vassals can own lands and castles in my domain.\
 A ronin can not be trusted with such a responsibility.\
 However, after serving for some time, I might retain you permanently to become become my vassal.\
 Then you will be rewarded with a fief.", "lord_mercenary_elaborate_1", []],
[anyone,"lord_mercenary_elaborate_castle", [##diplomacy start+ Make gender correct
  (faction_get_slot, reg0, "$g_talk_troop_faction", slot_faction_leader),
  (call_script, "script_dplmc_store_troop_is_female", reg0),
  ##Next line, replace "his" with {reg0?her:his}
  ], "Only loyal vassals of {s10} can own lands and castles.\
 You understand, a simple ronin cannot be trusted with such responsibility.\
 However, after serving for some time, you may earn the right to swear allegiance to {s10} and become {reg0?her:his} vassal.\
 Then you would be rewarded with a fief.", "lord_mercenary_elaborate_1", []],
[anyone,"lord_mercenary_elaborate_banner", [(faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, "$g_talk_troop")],
   "Only my hereditary vassals have the honour of carrying their own banners.\
 However, after some time in service, you may earn the opportunity to become a hereditary vassal,\
 gaining the right to choose a kamon of your own and fight under it in battle.", "lord_mercenary_elaborate_1", []],
[anyone,"lord_mercenary_elaborate_banner", [##diplomacy start+ Use correct gender
   (faction_get_slot, reg0, "$g_talk_troop_faction", slot_faction_leader),
   (call_script, "script_dplmc_store_troop_is_female", reg0),
   #Next line "his" -> {reg0?her:his}
  ], "Only vassal retainers of {s10} have the honour of carrying their own banners.\
 However, after some time of service as a ronin, perhaps you can earn the opportunity to swear allegiance to {s10} and become {reg0?her:his} vassal,\
 gaining the right to choose a kamon of your own and fight under it in battle.", "lord_mercenary_elaborate_1", []],
[anyone,"lord_request_mission_ask", [(store_partner_quest,":lords_quest"),(ge,":lords_quest",0)],
   "You still haven't finished the last job I gave you, {playername}. You should be working on that, not asking me for other things to do.", "lord_pretalk",[]],
[anyone,"lord_request_mission_ask", [(troop_slot_eq, "$g_talk_troop", slot_troop_does_not_give_quest, 1)],
   "I don't have any other jobs for you right now.", "lord_pretalk",[]],
[anyone|auto_proceed,"lord_request_mission_ask", [], "A task?", "lord_tell_mission",
   [
       (call_script, "script_get_quest", "$g_talk_troop"),
       (assign, "$random_quest_no", reg0),
   ]],
[anyone,"lord_request_mission_ask", [
  (this_or_next|troop_slot_eq, "$g_talk_troop", slot_troop_met, 2),
	(troop_slot_eq, "trp_player", slot_troop_betrothed, "$g_talk_troop"),
  ##diplomacy start+ use gender script
  #(eq, "$character_gender", 1),#<- XXX TODO: Safe to remove?
  ],##Next line, "My lady" to "My {lord/lady}
   "My {lord/lady}, by the traditions of courtship, I should be offering my services to you. Unfortunately, I have little time right now, so I beg you to take this declaration of my esteem in its place.", "lord_pretalk",[]],
[anyone,"lord_tell_mission", [
  (eq, "$player_has_homage" ,1),
  (neq, "$random_quest_no", "qst_rescue_prisoner"),
  (neq, "$random_quest_no", "qst_destroy_bandit_lair"),
  (neq, "$random_quest_no", "qst_raise_troops"),
  (neq, "$random_quest_no", "qst_escort_lady"),
  (neq, "$random_quest_no", "qst_lend_companion"),
  (neq, "$random_quest_no", "qst_capture_enemy_hero"),
  (neq, "$random_quest_no", "qst_cause_provocation"),
  ##diplomacy start+
  (neq, "$random_quest_no", "qst_collect_debt"),#currently never given, but if it were enabled it would be fine
  #Assign some variables used later to re-enable quests which are usually disabled
  #once the player has received homage.
  (assign, ":is_close", 0),
  (assign, ":nominal_superior", 0),
  #is close:
  (try_begin),
	#affiliates, and spouse
	(call_script, "script_dplmc_is_affiliated_family_member", "$g_talk_troop"),
	(this_or_next|ge, reg0, 1),
		(troop_slot_eq, "trp_player", slot_troop_spouse, "$g_talk_troop"),
	(assign, ":is_close", 1),
  (else_try),
	#in-laws, former companions, and assisted pretenders
	(ge, "$g_talk_troop_faction_relation", 0),
	(ge, "$g_talk_troop_relation", 50),
	(try_begin),
		#gekokujo 3.0 microfactions! include fort companions start
		#(this_or_next|is_between, "$g_talk_troop", companions_begin, companions_end),
		(this_or_next|is_between, "$g_talk_troop", companions_begin, fort_companions_end),
		#gekokujo 3.0 microfactions! include fort companions end
			(is_between, "$g_talk_troop", pretenders_begin, pretenders_end),
		(neg|troop_slot_eq, "$g_talk_troop", slot_troop_playerparty_history, dplmc_pp_history_nonplayer_entry),
		(assign, ":is_close", 1),
	(else_try),
		(call_script, "script_troop_get_family_relation_to_troop", "$g_talk_troop", "trp_player"),
		(ge, reg0, 2),
		(assign, ":is_close", 1),
	(try_end),
   (try_end),

	#Is nominally the social superior of the player (or even if not the superior,
	#is allowed to give the player orders in at least one context)
	(try_begin),
		#quest giver is faction leader or marshall, or player's father or mother
		(this_or_next|troop_slot_eq, "trp_player", slot_troop_father, "$g_talk_troop"),
		(this_or_next|troop_slot_eq, "trp_player", slot_troop_mother, "$g_talk_troop"),
		(this_or_next|faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, "$g_talk_troop"),
			(faction_slot_eq, "$g_talk_troop_faction", slot_faction_marshall, "$g_talk_troop"),
		(assign, ":nominal_superior", 1),
	(else_try),
		#player has less than 3/4 of the quest giver's renown
		(troop_get_slot, reg0, "$g_talk_troop", slot_troop_renown),
		(val_mul, reg0, 3),
		(val_div, reg0, 4),
		##diplomacy start+
		(assign, ":save_reg0", reg0),
		(try_begin),
			(lt, "$g_disable_condescending_comments", 0),#<- OPTION: Prejudice mode High
			(neq, reg65, "$character_gender"),
			(neg|troop_slot_ge, "$g_talk_troop", slot_lord_reputation_type, lrep_roguish),#non-noble or kingdom lady
			(neg|troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_cunning),
			(neg|troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_goodnatured),
			#gekokujo 3.0 microfactions! include fort companions start
			#(neg|is_between, "$g_talk_troop", companions_begin, companions_end),
			(neg|is_between, "$g_talk_troop", companions_begin, fort_companions_end),
			#gekokujo 3.0 microfactions! include fort companions end
			(call_script, "script_cf_dplmc_faction_has_bias_against_gender", "$g_talk_troop_faction", "trp_player"),
			(val_mul, ":save_reg0", 2),#double the renown threshold
		(try_end),
		(assign, reg0, ":save_reg0"),
		##diplomacy end+
		(neg|troop_slot_ge, "trp_player", slot_troop_renown, reg0),
		(assign, ":nominal_superior", 1),
	(else_try),
		#quest giver is player's father-in-law or mother-in-law
		(troop_get_slot, ":player_spouse", "trp_player", slot_troop_spouse),
		(is_between, ":player_spouse", heroes_begin, heroes_end),
		(this_or_next|troop_slot_eq, ":player_spouse", slot_troop_father, "$g_talk_troop"),
			(troop_slot_eq, ":player_spouse", slot_troop_mother, "$g_talk_troop"),
		(assign, ":nominal_superior", 1),
	(try_end),

  (assign, ":matched_any", 0),
  (try_begin),
	#close or nominal superior:
	(this_or_next|ge, ":is_close", 1),
		(ge, ":nominal_superior", 1),
    (this_or_next|eq, "$random_quest_no", "qst_deliver_message_to_prisoner_lord"),
    (this_or_next|eq, "$random_quest_no", "qst_meet_spy_in_enemy_town"),
	(this_or_next|eq, "$random_quest_no", "qst_deliver_message"),
	(this_or_next|eq, "$random_quest_no", "qst_collect_taxes"),
	(this_or_next|eq, "$random_quest_no", "qst_follow_spy"),
	   (eq, "$random_quest_no", "qst_capture_prisoners"),
	(assign, ":matched_any", 1),
  (else_try),
	#close only:
	(ge, ":is_close", 1),
	(this_or_next|eq, "$random_quest_no", "qst_kill_local_merchant"),
	   (eq, "$random_quest_no", "qst_incriminate_loyal_commander"),
	(assign, ":matched_any", 1),
  (try_end),
  (eq, ":matched_any", 0),
  ##Get different text if the player is the faction leader or the faction leader's spouse
  (try_begin),
    (neg|faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, "$g_talk_troop"),
    (troop_get_slot, reg0, "trp_player", slot_troop_spouse),
	(this_or_next|faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, "trp_player"),
		(faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, reg0),
	(this_or_next|faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, "trp_player"),
		(ge, reg0, 1),
	(assign, reg0, 1),
  (else_try),
	(assign, reg0, 0),
  (try_end),
  ],
  ##Allow this to also be used for liege, replaced "a sworn vassal of the realm" with "{reg0?my sworn liege:a sworn vassal of the realm}", "men" with {reg65?servants:men}
   "There are some minor errands which I need completed, but it would be more appropriate to give them to one of my own {reg65?servants:men}, not to my vassals.", "lord_tell_mission_sworn_vassal",[]],
[anyone,"lord_tell_mission_sworn_vassal", [
	(this_or_next|party_slot_eq, "$g_talk_troop_party", slot_party_ai_state, spai_besieging_center),
		(party_slot_eq, "$g_talk_troop_party", slot_party_ai_state, spai_raiding_around_center),

	(party_get_slot, ":cur_object", "$g_talk_troop_party", slot_party_ai_object),
	(is_between, ":cur_object", centers_begin, centers_end),
	(str_store_party_name, s4, ":cur_object"),
  ],##diplomacy start+ use gender-neutral term for soldiers in case it would be absurd
	"If you are looking for action against our foes, you may join our attack on {s4}. The enemy may come in force to oppose us, so it is good to have as many {reg65?soldiers:{soldiers/men}} as possible.", "lord_pretalk",[]],
[anyone,"lord_tell_mission_sworn_vassal", [
    (eq, "$g_talk_troop_faction", "$players_kingdom"),

	(party_get_slot, ":cur_object", "$g_talk_troop_party", slot_party_ai_object),
	(is_between, ":cur_object", centers_begin, centers_end),
	(party_get_slot, ":last_spotted_enemy", ":cur_object", slot_center_last_spotted_enemy),
	(party_is_active, ":last_spotted_enemy"),
	(store_faction_of_party, ":last_spotted_enemy_faction", ":last_spotted_enemy"),
	(store_relation, ":relation",":last_spotted_enemy_faction", "$g_talk_troop_faction"),
	(lt, ":relation", 0),

	(is_between, ":last_spotted_enemy_faction", kingdoms_begin, kingdoms_end),
	(str_store_party_name, s4, ":cur_object"),
	(str_store_faction_name, s5, ":last_spotted_enemy_faction"),

  ],
	"If you are looking for action against our foes, you may try venturing out to {s4}. We have received word that a force of the {s5} is in the area, and I am going there myself. I cannot guarantee you that our enemies will be there when you arrive, of course.", "lord_pretalk",[]],
[anyone,"lord_tell_mission_sworn_vassal", [
    (eq, "$g_talk_troop_faction", "$players_kingdom"),
	(assign, ":alarmed_center_found", -1),
	(assign, ":score_to_beat", 9999),

	(try_for_range, ":center_no", centers_begin, centers_end),
		(store_faction_of_party, ":center_faction", ":center_no"),
		(eq, ":center_faction", "$g_talk_troop_faction"),
		(party_get_slot, ":last_spotted_enemy", ":center_no", slot_center_last_spotted_enemy),
		(party_is_active, ":last_spotted_enemy"),
		(store_faction_of_party, ":last_spotted_enemy_faction", ":last_spotted_enemy"),
		(is_between, ":last_spotted_enemy_faction", kingdoms_begin, kingdoms_end),

		(store_relation, ":relation", ":last_spotted_enemy_faction", "$g_talk_troop_faction"),
		(lt, ":relation", 0),

		(store_distance_to_party_from_party, ":distance", ":center_no", "p_main_party"),
		(lt, ":distance", ":score_to_beat"),

		(assign, ":alarmed_center_found", ":center_no"),
		(assign, ":score_to_beat", ":distance"),
		(str_store_faction_name, s5, ":last_spotted_enemy_faction"),
	(try_end),
	(is_between, ":alarmed_center_found", centers_begin, centers_end),
	(str_store_party_name, s4, ":alarmed_center_found"),
  ],
	"If you are looking for action against our foes, you may try venturing out to {s4}. We have received word that a force of the {s5} is in the area. I am not currently headed that way, but others may be.  I cannot guarantee you that our enemies will be there when you arrive, of course.", "lord_pretalk",[]],
[anyone,"lord_tell_mission_sworn_vassal", [  ],
	"If a worthy task presents itself, however, I may have a favor to ask of you at a later date.", "lord_pretalk",[]],
[anyone,"lord_tell_mission", [
  (eq,"$random_quest_no", "qst_destroy_bandit_lair"),
  (quest_get_slot, ":bandit_lair", "qst_destroy_bandit_lair", slot_quest_target_party),

  (party_stack_get_troop_id, ":bandit_type", ":bandit_lair", 0),
  (str_store_troop_name_plural, s4, ":bandit_type"),

  ], "Yes -- there is something you can do for us. We have heard reports that a group of {s4} have established a hideout in this area, and have been attacking travellers. If you could find their lair and destroy it, we would be very grateful.", "destroy_lair_quest_brief", #s48 is bandits, s42 is the road information
   []],
[anyone,"lord_tell_mission",
  [(eq,"$random_quest_no","qst_rescue_prisoner"),
  ##diplomacy start+ Correct gender
  (assign, reg3, 0),
  (try_begin),
	(quest_get_slot, ":quest_target_troop", "$random_quest_no", slot_quest_target_troop),
	(troop_get_slot, ":quest_target_center", ":quest_target_troop", slot_troop_prisoner_of_party),
	(party_get_slot, ":captor", ":quest_target_center", slot_town_lord),
	(call_script, "script_cf_dplmc_troop_is_female", ":captor"),
    (assign, reg3, 1),
  (try_end),
  ],#Next line "he" to {reg3?she:he}, etc.
   "My {s11}, {s13}, has been taken prisoner by {s14} of the {s15}. Normally, honorable samurai will grant prisoners of great prestige the privilege of seppuku instead of beheading them outright, and treat them as honored guests before that happens.  But {s14}, instead of granting {s13} seppuku, has consigned my {s11} to {reg3?her:his} prison -- no doubt in the hope that {reg3?she:he} can demand ransom from us.", "lord_mission_rescue_prisoner",
   ##diplomcay end+
   [
     (quest_get_slot, ":quest_target_troop", "$random_quest_no", slot_quest_target_troop),
     (troop_get_slot, ":quest_target_center", ":quest_target_troop", slot_troop_prisoner_of_party),
	 (call_script, "script_troop_get_family_relation_to_troop", ":quest_target_troop", "$g_talk_troop"),

     (str_store_troop_name_link, s9, "$g_talk_troop"),
     (str_store_troop_name_link, s13, ":quest_target_troop"),
     (str_store_party_name_link, s24, ":quest_target_center"),
	 (party_get_slot, ":captor", ":quest_target_center", slot_town_lord),
     (str_store_troop_name, s14, ":captor"),
	 (store_faction_of_party, ":target_faction", ":quest_target_center"),
     (str_store_faction_name, s15, ":target_faction"),


     (setup_quest_text,"$random_quest_no"),
##     (try_begin),
##       (is_between, "$g_encountered_party", centers_begin, centers_end),
##       (setup_quest_giver, "$random_quest_no", "str_given_by_s1_at_s2"),
##     (else_try),
##       (setup_quest_giver,"$random_quest_no", "str_given_by_s1_in_wilderness"),
##     (try_end),
     (str_store_string, s2, "str_s9_asked_you_to_rescue_s13_who_is_prisoner_at_s24"),
   ]],
[anyone,"lord_mission_rescue_prisoner", [],##diplomacy start+ next line, use reg4 for gender
   "We need you to get my {s11} out of prison. You may be able to pay a ransom -- in which case we could cover your expenses, up to 5000 mon. If you have connections within {s24}, you may be able to use them to sneak {reg4?her:him} out. Or, you may try a more direct approach -- walk up to the gaoler, take the keys by force, and then fight your way out. Can you do this for us?", "lord_mission_rescue_prisoner_confirm",
   ##diplomacy end+
   [
   ]],
[anyone|plyr,"lord_mission_rescue_prisoner_confirm", [],
  "I can try.", "lord_mission_rescue_prisoner_accepted",[]],
[anyone|plyr,"lord_mission_rescue_prisoner_confirm", [], "I don't think that I can help you.", "lord_mission_rescue_prisoner_rejected",[]],
[anyone,"lord_mission_rescue_prisoner_rejected", [], "It would not have been an easy task. Perhaps we will find another way.", "close_window",[
    (assign, "$g_leave_encounter",1),
  ]],
[anyone,"lord_mission_rescue_prisoner_accepted", [], "We are most grateful. Could I ask you how you were planning to proceed?", "lord_mission_rescue_prisoner_method",
   [(call_script, "script_start_quest", "$random_quest_no", "$g_talk_troop"),
    (call_script, "script_change_player_relation_with_troop","$g_talk_troop",1),
   ]],
[anyone,"lord_mission_rescue_other_ideas", [], "Did you have any other ideas which you wished to discuss?", "lord_mission_rescue_prisoner_method",
   []],
[anyone|plyr,"lord_mission_rescue_prisoner_method", [
  (eq, 1, 0),
  ], # unused
  "{!}I am thinking of paying the ransom.", "lord_mission_rescue_prisoner_method_ransom",[]],
[anyone|plyr,"lord_mission_rescue_prisoner_method", [
  (eq, 1, 0),
  ], # unused
  "{!}I am thinking of using my connections in {s24}.", "close_window",[]],
[anyone|plyr,"lord_mission_rescue_prisoner_method", [],
  "I am thinking of breaking into the prison in {s24}, finding {s13}, and fighting my way out.", "lord_mission_rescue_prisoner_method_prisonbreak",[]],
[anyone|plyr,"lord_mission_rescue_prisoner_method", [],
  "I am thinking of taking {s24} by storm.", "lord_mission_rescue_prisoner_method_siege",[]],
[anyone|plyr,"lord_mission_rescue_prisoner_method", [],
  "I have done enough planning. Time to act!", "lord_mission_rescue_prisoner_planning_end",[]],
[anyone,"lord_mission_rescue_prisoner_planning_end", [],
  "May the heavens protect you.", "close_window",[
  (assign, "$g_leave_encounter", 1),
  ]],
[anyone,"lord_mission_rescue_prisoner_method_ransom", [],
  "{!}[Ransom option not yet implemented]", "lord_mission_rescue_other_ideas",[]],
[anyone,"lord_mission_rescue_prisoner_method_prisonbreak", [],
  "I had discussed this idea with some of my men. One could enter {s24}, either in disguise or openly, then walk up to the prison guard and try to take the keys by force. However, getting out may be difficult. The garrison may be slow to react, but even so, you are likely to find yourself fighting a half dozen or more of the enemy at once, with limited space in which to maneuver. If you can fight your way past them, though, you can probably get out.", "lord_mission_rescue_prisoner_method_prisonbreak_2",[]],
[anyone,"lord_mission_rescue_prisoner_method_prisonbreak_2", [],
  "You may find it useful to create a distraction, to divert the attention of some of the garrison. If you have any connections in the villages near {s24}, this may be a time to put them to use.", "lord_mission_rescue_other_ideas",[]],
[anyone,"lord_mission_rescue_prisoner_method_siege", [],
  "Well, that is certainly the most direct approach.", "lord_mission_rescue_other_ideas",[]],
[anyone,"lord_tell_mission", [(eq,"$random_quest_no","qst_deliver_message"),
  ##diplomacy start+ fix pronoun
  (quest_get_slot, ":quest_target_troop", "$random_quest_no", slot_quest_target_troop),
  (call_script, "script_dplmc_store_troop_is_female",  ":quest_target_troop"),
  ],#next line, change him/his based on reg0
   "I need to send a letter to {s13} who should be currently at {s4}.\
 If you will be heading towards there, would you deliver it to {reg0?her:him}?\
 The letter needs to be in {reg0?her:his} hands in 30 days.", "lord_mission_deliver_message",
  ##diplomacy end+
   [
     (quest_get_slot, ":quest_target_troop", "$random_quest_no", slot_quest_target_troop),
     (quest_get_slot, ":quest_target_center", "$random_quest_no", slot_quest_target_center),
     (str_store_troop_name_link,s9,"$g_talk_troop"),
     (str_store_troop_name_link,s13,":quest_target_troop"),
     (str_store_party_name_link,s4,":quest_target_center"),
     (setup_quest_text,"$random_quest_no"),
##     (try_begin),
##       (is_between, "$g_encountered_party", centers_begin, centers_end),
##       (setup_quest_giver, "$random_quest_no", "str_given_by_s1_at_s2"),
##     (else_try),
##       (setup_quest_giver,"$random_quest_no", "str_given_by_s1_in_wilderness"),
##     (try_end),
     (str_store_string, s2, "@{s9} asked you to take a message to {s13}. {s13} was believed to be at {s4} when you were given this quest."),
   ]],
[anyone|plyr,"lord_mission_deliver_message", [], "Certainly, I intend to pass by {s4} and it would be no trouble.", "lord_mission_deliver_message_accepted",[]],
[anyone|plyr,"lord_mission_deliver_message", [], "I doubt I'll be seeing {s13} anytime soon, {s65}. You'd best send it with someone else.", "lord_mission_deliver_message_rejected",[]],
[anyone|plyr,"lord_mission_deliver_message", [], "I am no errand {boy/girl}, {reg65?my lady:sir}. Hire a courier for your trivialities.",
  ##diplomacy end+
  "lord_mission_deliver_message_rejected_rudely",[]],
[anyone,"lord_mission_deliver_message_accepted", [##diplomacy start+ Fix gender
  (quest_get_slot, ":quest_target_troop", "$random_quest_no", slot_quest_target_troop),
  (call_script, "script_dplmc_store_troop_is_female", ":quest_target_troop"),
  ], "I appreciate it, {playername}. Here's the letter, and a small sum to cover your travel expenses. Give my regards to {s13} when you see {reg0?her:him}.", "close_window",
  ##diplomacy end+
   [(call_script, "script_start_quest", "$random_quest_no", "$g_talk_troop"),
    (call_script, "script_troop_add_gold", "trp_player", 30),    (assign, "$g_leave_encounter",1),
   ]],
[anyone,"lord_mission_deliver_message_rejected", [], "Ah, all right then. Well, I am sure I will find someone else.", "lord_pretalk",
   [(troop_set_slot, "$g_talk_troop", slot_troop_does_not_give_quest, 1)]],
[anyone,"lord_mission_deliver_message_rejected_rudely", [], "Hm, is this how you respond to a polite request\
 for a small favor? A poor show, {playername}. I didn't know you would take offence.", "lord_mission_deliver_message_rejected_rudely_2",[]],
[anyone|plyr,"lord_mission_deliver_message_rejected_rudely_2", [], "Then you shall know better from now on.", "lord_mission_deliver_message_rejected_rudely_3",[]],
[anyone|plyr,"lord_mission_deliver_message_rejected_rudely_2", [], "Forgive my temper, {s65}. I'll deliver your letter.", "lord_mission_deliver_message_accepted",[]],
[anyone,"lord_mission_deliver_message_rejected_rudely_3", [], "All right. I will remember that.", "close_window",[
    (call_script, "script_change_player_relation_with_troop","$g_talk_troop",-4),
    (quest_set_slot, "$random_quest_no", slot_quest_dont_give_again_remaining_days, 150),
    (troop_set_slot, "$g_talk_troop", slot_troop_does_not_give_quest, 1),
    (assign, "$g_leave_encounter",1),
      ]],
[anyone,"lord_tell_mission", [
	(eq,"$random_quest_no","qst_deliver_message_to_enemy_lord"),
	(quest_get_slot, ":quest_target_troop", "$random_quest_no", slot_quest_target_troop),
	(call_script, "script_dplmc_store_troop_is_female", ":quest_target_troop"),
	],
#   "I need to deliver a letter to {s13} of {s15}, who must be at {s4} currently.\
# If you are going towards there, would you deliver my letter to him? The letter needs to reach him in 40 days.", "lord_mission_deliver_message",
   "I need to deliver a letter to {s13} of {s15}, who must be at {s4} currently.\
 If you are going towards there, would you deliver my letter to {reg0?her:him}? The letter needs to reach {reg0?her:him} in 40 days.", "lord_mission_deliver_message",
##diplomacy end+
   [
     (quest_get_slot, ":quest_target_troop", "$random_quest_no", slot_quest_target_troop),
     (quest_get_slot, ":quest_target_center", "$random_quest_no", slot_quest_target_center),
     (str_store_troop_name_link,s9,"$g_talk_troop"),
##     (str_store_party_name,2,"$g_encountered_party"),
     (str_store_troop_name_link,s13,":quest_target_troop"),
     (str_store_party_name_link,s4,":quest_target_center"),
     (store_troop_faction, ":target_faction", ":quest_target_troop"),
     (str_store_faction_name_link,s15,":target_faction"),
     (setup_quest_text,"$random_quest_no"),
##     (try_begin),
##       (is_between, "$g_encountered_party", centers_begin, centers_end),
##       (setup_quest_giver, "$random_quest_no", "str_given_by_s1_at_s2"),
##     (else_try),
##       (setup_quest_giver,"$random_quest_no", "str_given_by_s1_in_wilderness"),
##     (try_end),
     (str_store_string, s2, "@{s9} asked you to take a message to {s13} of {s15}. {s13} was believed to be at {s4} when you were given this quest."),
   ]],
[anyone,"lord_tell_mission", [(eq,"$random_quest_no","qst_escort_lady")],
   "There is a small thing... My {s17} {s13} is due for a visit to {reg4?her:his} relatives at {s14}.\
 The visit has been postponed several times already with all the trouble on the roads,\
 but this time {reg4?he:she} is adamant about going. So, I want to at least make sure {reg4?she:he}'s well-guarded.\
 I trust you well, {playername} so I would be very grateful if you could escort {reg4?her:him} to {s14}\
 and make sure {reg4?she:he} arrives safe and sound.", "lord_mission_told",
   [
     (quest_get_slot, ":quest_object_troop", "$random_quest_no", slot_quest_object_troop),
     (quest_get_slot, ":quest_target_center", "$random_quest_no", slot_quest_target_center),
	 ##diplomacy start+ Change the following to allow a wider range of relations
     #(try_begin),
     #  (troop_slot_eq, ":quest_object_troop", slot_troop_father, "$g_talk_troop"),
     #  (str_store_string, s17, "str_daughter"),
     #(else_try),
     #  (str_store_string, s17, "str_wife"),
     #(try_end),
	 (call_script, "script_dplmc_troop_get_family_relation_to_troop", ":quest_object_troop", "$g_talk_troop"),
     (try_begin),
		(this_or_next|le, reg1, "str_ERROR_string"),
		(lt, reg0, 1),
		(assign, reg1, "str_dplmc_friend"),
     (try_end),
	 (str_store_string, s17, reg1),
	 (call_script, "script_dplmc_cap_troop_describes_troop_to_troop_s1", 1, "$g_talk_troop", ":quest_object_troop", "trp_player"),
	 ##diplomacy end+
     (str_store_troop_name_link, s11, "$g_talk_troop"),
     (str_store_troop_name_link, s13, ":quest_object_troop"),
     (str_store_party_name_link, s14, ":quest_target_center"),
     (setup_quest_text,"$random_quest_no"),
	 ##diplomacy start+ fix pronoun
	 (call_script, "script_dplmc_store_troop_is_female", ":quest_object_troop"),
	 (assign, reg4, reg0),
	 #"his" changed to "{reg65?her:his}"
     (str_store_string, s2, "@{s11} asked you to escort {reg65?her:his} {s17} {s13} to {s14}."),
	 ##diplomacy end+
   ]],
[anyone,"lord_tell_mission", [(eq,"$random_quest_no","qst_deal_with_bandits_at_lords_village")],
   "A group of bandits have taken refuge in my village of {s15}.\
 They are plundering nearby farms, and getting rich and fat stealing my taxes and feasting on my cattle.\
I'd like nothing better than to go out there and teach them a lesson,\
 but I have my hands full at the moment, so I can't do anything about it.", "lord_mission_deal_with_bandits_told",
   [
     (quest_get_slot, ":quest_target_center", "$random_quest_no", slot_quest_target_center),
     (str_store_party_name_link,s15,":quest_target_center"),
     (str_store_troop_name_link,s13,"$g_talk_troop"),
     (setup_quest_text,"$random_quest_no"),
	 ##diplomacy start+ fix pronoun
	 #"him" changed to "{reg65?her:him}"
     (str_store_string, s2, "@{s13} asked you to deal with the bandits who are occupying the village of {s15} and then report back to {reg65?her:him."),
	 ##diplomacy end+
   ]],
[anyone|plyr,"lord_mission_deal_with_bandits_told", [],
   "Worry not, I can go to {s15} and deal with these scum for you.", "lord_mission_deal_with_bandits_accepted",[]],
[anyone|plyr,"lord_mission_deal_with_bandits_told", [], "You shall have to find help elsewhere, I am too busy.", "lord_mission_deal_with_bandits_rejected",[]],
[anyone,"lord_mission_deal_with_bandits_accepted", [], "Will you do that?\
 Know that, I will be grateful to you. Here is some money for the expenses of your campaign.\
 Make an example of those {s43}s.", "close_window",
   [

 	(call_script, "script_lord_comment_to_s43", "$g_talk_troop", "str_lord_insult_default"),

    (call_script, "script_start_quest", "$random_quest_no", "$g_talk_troop"),
    (call_script, "script_troop_add_gold", "trp_player", 200),
    (call_script, "script_change_player_relation_with_troop","$g_talk_troop",1),
    (assign, "$g_leave_encounter",1),
   ]],
[anyone,"lord_mission_deal_with_bandits_rejected", [], "Ah... Very well then, forget I brought it up.", "lord_pretalk",
   [(troop_set_slot, "$g_talk_troop", slot_troop_does_not_give_quest, 1)]],
[anyone,"lord_tell_mission", [(eq,"$random_quest_no","qst_raise_troops"),
  ##diplomacy start+ Change "sword" to another weapon if appropriate, and likewise for "men"
  (try_begin),
     (call_script, "script_cf_dplmc_faction_has_bias_against_gender", "$g_encountered_party_faction", 0),
	 (assign, reg0, 1),
  (else_try),
     (assign, reg0, 0),
  (try_end),
  ],
   "No lord should have to admit this, {playername}, but I was inspecting my soldiers the other day and there are {reg0?{reg65?women:soldiers}:{reg65?soldiers:men}} here who don't know which end of a sword to hold. {s43} You are a warrior of renown, {playername}. Will you train some troops for me? I would be grateful to you.", "lord_tell_mission_raise_troops",[
 ##diplomacy end+
 	(call_script, "script_lord_comment_to_s43", "$g_talk_troop", "str_troop_train_request_default"),

     ]],
[anyone|plyr,"lord_tell_mission_raise_troops", [], "How many men do you need?", "lord_tell_mission_raise_troops_2",[]],
[anyone,"lord_tell_mission_raise_troops_2", [], "If you can raise {reg1} {s14} and bring them to me, that will probably be enough.", "lord_mission_raise_troops_told",
   [
     (quest_get_slot, ":quest_target_troop", "$random_quest_no", slot_quest_target_troop),
     (quest_get_slot, reg1, "$random_quest_no", slot_quest_target_amount),
     (str_store_troop_name_link,s9,"$g_talk_troop"),
     (str_store_troop_name_plural,s14,":quest_target_troop"),
     (setup_quest_text,"$random_quest_no"),
	 ##diplomacy start+ fix pronoun
	 #"him" changed to "{reg0?her:him}"
     (str_store_string, s2, "@{s9} asked you to raise {reg1} {s14} and bring them to {reg65?her:him}."),
	 ##diplomcay end+
   ]],
[anyone|plyr,"lord_mission_raise_troops_told", [(quest_get_slot, reg1, "$random_quest_no", slot_quest_target_amount)],
   "Of course, {s65}. Give me {reg1} fresh recruits and I'll train them to be {s14}.", "lord_mission_raise_troops_accepted",[]],
[anyone|plyr,"lord_mission_raise_troops_told", [], "I am too busy these days to train anyone.", "lord_mission_raise_troops_rejected",[]],
[anyone,"lord_mission_raise_troops_accepted", [], "You've taken a weight off my shoulders, {playername}.\
 I shall tell my sergeants to send you the recruits and attach them to your command.\
 Also, I'll advance you some money to help with expenses. Here, this purse should do it.\
 Thank you for your help.", "close_window",
   [(call_script, "script_start_quest", "$random_quest_no", "$g_talk_troop"),
    (call_script, "script_troop_add_gold", "trp_player", 100),
    (quest_get_slot, ":recruit_troop", "$random_quest_no", slot_quest_object_troop),
    (quest_get_slot, ":num_recruits", "$random_quest_no", slot_quest_target_amount),
    (party_add_members, "p_main_party", ":recruit_troop", ":num_recruits"),
    (call_script, "script_change_player_relation_with_troop","$g_talk_troop",1),
    (assign, "$g_leave_encounter",1),
   ]],
[anyone,"lord_mission_raise_troops_rejected", [], "Oh, of course. I had expected as much. Well, good luck to you then.", "lord_pretalk",
   [(troop_set_slot, "$g_talk_troop", slot_troop_does_not_give_quest, 1)]],
[anyone,"lord_tell_mission", [(eq,"$random_quest_no","qst_collect_taxes"),
                                (assign, reg9, 0),
                                (try_begin),
                                  (quest_get_slot, ":quest_target_center", "$random_quest_no", slot_quest_target_center),
                                  (party_slot_eq, ":quest_target_center", slot_party_type, spt_town),
                                  (assign, reg9, 1),
                                (try_end),
                                ], "You probably know that I am the lord of the {reg9?town:village} of {s3}.\
 However, it has been months since {s3} has delivered the taxes and rents due me as its rightful lord.\
 Apparently the populace there has grown unruly lately and I need someone to go there and remind them of\
 their obligations. And to . . . persuade them if they won't listen.\
 If you go there and raise the taxes they owe me, I will grant you one-fifth of everything you collect.", "lord_mission_collect_taxes_told",
   [
     (quest_get_slot, ":quest_target_center", "$random_quest_no", slot_quest_target_center),
     (str_store_troop_name_link,s9,"$g_talk_troop"),
     (str_store_party_name_link,s3,":quest_target_center"),
     (setup_quest_text,"$random_quest_no"),
	 ##diplomacy start+ fix pronoun
	 #"He" changed to "{reg65?She:He}"
     (str_store_string, s2, "@{s9} asked you to collect taxes from {s3}. {reg65?She:He} offered to leave you one-fifth of all the money you collect there."),
	 ##diplomacy end+
   ]],
[anyone|plyr,"lord_mission_collect_taxes_told", [],
   "A fair offer, {s65}. We have an agreement.", "lord_mission_collect_taxes_accepted",[]],
[anyone|plyr,"lord_mission_collect_taxes_told", [], "Forgive me, I don't have the time.", "lord_mission_collect_taxes_rejected",[]],
[anyone,"lord_mission_collect_taxes_accepted", [], "Welcome news, {playername}.\
 I will entrust this matter to you.\
 Remember, those {reg9?townsmen:peasants} are foxy beasts, they will make every excuse not to pay me my rightful incomes.\
 Do not let them fool you.", "close_window",
   [(call_script, "script_start_quest", "$random_quest_no", "$g_talk_troop"),
    (call_script, "script_change_player_relation_with_troop","$g_talk_troop",1),
    (assign, "$g_leave_encounter",1),
    (assign, reg9, 0),
    (quest_get_slot, ":quest_target_center", "$random_quest_no", slot_quest_target_center),
    (try_begin),
      (party_slot_eq, ":quest_target_center", slot_party_type, spt_town),
      (assign, reg9, 1),
    (try_end),
   ]],
[anyone,"lord_mission_collect_taxes_rejected", [], "Oh, yes. Well, good luck to you then.", "lord_pretalk",
   [(troop_set_slot, "$g_talk_troop", slot_troop_does_not_give_quest, 1)]],
[anyone,"lord_tell_mission", [(eq,"$random_quest_no","qst_hunt_down_fugitive")],
   "I have something you could help with, an issue with the lawless villain known as {s4}. \
 He murdered one of my men and has been on the run from his judgment ever since.\
 I can't let him get away with avoiding justice, so I've put a bounty of 300 mon on his head.\
 Friends of the murdered man reckon that this assassin may have taken refuge with his kinsmen at {s3}.\
 You might be able to hunt him down and give him what he deserves, and claim the bounty for yourself.", "lord_mission_hunt_down_fugitive_told",
   [
     (quest_get_slot, ":quest_target_center", "$random_quest_no", slot_quest_target_center),
     (quest_get_slot, ":quest_target_dna", "$random_quest_no", slot_quest_target_dna),
     (str_store_troop_name_link,s9, "$g_talk_troop"),
     (str_store_party_name_link,s3, ":quest_target_center"),
     (call_script, "script_get_name_from_dna_to_s50", ":quest_target_dna"),
     (str_store_string, s4, s50),
     (setup_quest_text, "$random_quest_no"),
     (str_store_string, s2, "@{s9} asked you to hunt down a fugitive named {s4}. He is currently believed to be at {s3}."),
   ]],
[anyone|plyr,"lord_mission_hunt_down_fugitive_told", [],
   "Then I will hunt him down and execute the law.", "lord_mission_hunt_down_fugitive_accepted",[]],
[anyone|plyr,"lord_mission_hunt_down_fugitive_told", [], "I am too busy to go after him at the moment.", "lord_mission_hunt_down_fugitive_rejected",[]],
[anyone,"lord_mission_hunt_down_fugitive_accepted", [], "That's excellent, {playername}.\
 I will be grateful to you and so will the family of the man he murdered.\
 And of course the bounty on his head will be yours if you can get him.\
 Well, good hunting to you.", "close_window",
   [(call_script, "script_start_quest", "$random_quest_no", "$g_talk_troop"),
    (call_script, "script_change_player_relation_with_troop","$g_talk_troop",1),
    (assign, "$g_leave_encounter",1),
   ]],
[anyone,"lord_mission_hunt_down_fugitive_rejected", [], "As you wish, {playername}.\
I suppose there are plenty of bounty hunters around to get the job done . . .", "lord_pretalk",
   [(troop_set_slot, "$g_talk_troop", slot_troop_does_not_give_quest, 1)]],
[anyone,"lord_tell_mission", [(eq,"$random_quest_no","qst_kill_local_merchant")],
   "The wretched truth is that I owe a considerable sum of money to one of the merchants here in {s3}.\
 I've no intention of paying it back, of course, but that loud-mouthed fool is making a terrible fuss about it.\
 He even had the audacity to come and threaten me -- me! --\
 with a letter of complaint to the trade guilds and bankers. Why, he'd ruin my good reputation!\
 So I need a {man/woman} I can trust, someone who will guarantee the man's silence. For good.", "lord_mission_told_kill_local_merchant",
   [
       (str_store_troop_name_link,s9,"$g_talk_troop"),
       (str_store_party_name_link,s3,"$current_town"),
       (setup_quest_text,"$random_quest_no"),
       (str_store_string, s2, "@{s9} asked you to assassinate a local merchant at {s3}."),
   ]],
[anyone|plyr,"lord_mission_told_kill_local_merchant", [], "Worry not, he shan't breathe a word.", "lord_mission_accepted_kill_local_merchant",[]],
[anyone|plyr,"lord_mission_told_kill_local_merchant", [], "I'm no common murderer, sir. Find someone else for your dirty job.", "lord_mission_rejected",[]],
[anyone,"lord_mission_accepted_kill_local_merchant", [], "Very good. I trust in your skill and discretion,\
 {playername}. Do not disappoint me.\
 Go now and wait for my word, I'll send you a message telling when and where you can catch the merchant.\
 Dispose of him for me and I shall reward you generously.", "close_window",
   [(call_script, "script_start_quest", "$random_quest_no", "$g_talk_troop"),
    (assign, "$g_leave_town",1),
    (assign, "$qst_kill_local_merchant_center", "$current_town"),
    (rest_for_hours, 10, 4, 0),
    (finish_mission),
    ]],
[anyone,"lord_tell_mission", [(eq,"$random_quest_no","qst_meet_spy_in_enemy_town"),
                                (quest_get_slot, ":quest_target_center", "$random_quest_no", slot_quest_target_center),
                                (str_store_party_name, s13, ":quest_target_center"),
                                (store_faction_of_party,":quest_target_center_faction",),
                                (str_store_faction_name, s14, ":quest_target_center_faction"),
                                ],
   "I have a sensitive matter which needs tending to, {playername}, and no trustworthy retainers to take care of it. The fact is that I have a spy in {s13} to keep an eye on things for me, and report anything that might warrant my attention. Every week I send someone to collect the spy's reports and bring them back to me. The job's yours if you wish it.", "lord_mission_told_meet_spy_in_enemy_town",
   [
   ]],
[anyone|plyr,"lord_mission_told_meet_spy_in_enemy_town", [], "I don't mind a bit of skullduggery. Count me in.", "quest_meet_spy_in_enemy_town_accepted",[]],
[anyone|plyr,"lord_mission_told_meet_spy_in_enemy_town", [], "I must decline. This cloak-and-dagger work isn't fit for me.", "quest_meet_spy_in_enemy_town_rejected",[]],
[anyone,"lord_tell_mission", [(eq,"$random_quest_no","qst_cause_provocation"),
                                (quest_get_slot, ":quest_target_faction", "$random_quest_no", slot_quest_target_faction),
                                (str_store_faction_name_link, s13, ":quest_target_faction")],
   "This peace with {s13} ill suits me, {playername}. We've let those swine have their way for far too long.\
 Now they get stronger with each passing and their arrogance knows no bounds.\
 I say, we must wage war on them before it's too late!\
 Unfortunately, some of the bleeding hearts among our clan's hereditary vassals are blocking a possible declaration of war.\
 Witless cowards with no stomach for blood.", "lord_mission_told_raid_caravan_to_start_war",
   [
   ]],
[anyone|plyr,"lord_mission_told_raid_caravan_to_start_war", [], "You are right, {s65}, but what can we do?", "lord_mission_tell_raid_caravan_to_start_war_2",[]],
[anyone|plyr,"lord_mission_told_raid_caravan_to_start_war", [], "I disagree, sir. It is better that there be peace.", "quest_raid_caravan_to_start_war_rejected_1",[]],
[anyone,"lord_mission_tell_raid_caravan_to_start_war_2", [(quest_get_slot, ":quest_target_faction", "$random_quest_no", slot_quest_target_faction),
                                                            (str_store_faction_name_link, s13, ":quest_target_faction"),
															(str_store_faction_name, s14, "$g_talk_troop_faction")],
   "Ah, 'tis good to hear someone who understands!\
 As a matter of fact, there is something we can do, {playername}. A little bit of provocation...\
 If one of our war parties managed to enter their territory and pillage one of their caravans, or raided one of their villages,\
 and perhaps left behind a little token or two of the {s14},\
 they would have ample cause to declare war on us.\
 And then, well, even the cowards among us must rise to defend themselves.\
 So what do you say? Are you interested?", "lord_mission_tell_raid_caravan_to_start_war_3",[]],
[anyone|plyr,"lord_mission_tell_raid_caravan_to_start_war_3", [], "An excellent plan. Count me in.", "quest_raid_caravan_to_start_war_accepted",[]],
[anyone|plyr,"lord_mission_tell_raid_caravan_to_start_war_3", [], "Why don't you do that yourself?", "lord_mission_tell_raid_caravan_to_start_war_4",[]],
[anyone,"lord_mission_tell_raid_caravan_to_start_war_4", [
  	], "Well, {playername}, some of the lords in our kingdom\
 won't like the idea of someone inciting a war without their consent.\
 They are already looking for an excuse to get at me, and if I did this they could make me pay for it dearly.\
 You, on the other hand, are young and well-liked and daring, so you might just get away with it.\
 And of course I will back you up and defend your actions against your opponents.\
 All in all, a few lords might be upset at your endeavour, but I am sure you won't be bothered with that.", "lord_mission_tell_raid_caravan_to_start_war_5",[]],
[anyone|plyr,"lord_mission_tell_raid_caravan_to_start_war_5", [], "That seems reasonable. I am willing to do this.", "quest_raid_caravan_to_start_war_accepted",[]],
[anyone|plyr,"lord_mission_tell_raid_caravan_to_start_war_5", [], "I don't like this. Find yourself someone else to take the blame for your schemes.", "quest_raid_caravan_to_start_war_rejected_2",[]],
[anyone,"lord_tell_mission", [(eq,"$random_quest_no","qst_bring_back_runaway_serfs")],
 "Well, some of the pesants working my fields in {s4} have run away. The ungrateful swine,\
 I let them plough my fields and rent my cottages, and this is how they repay me!\
 From what I've been hearing, they're running to {s3} as fast as they can,\
 and have split up into three groups to try and avoid capture.\
 I want you to capture all three groups and fetch them back to {s4} by whatever means necessary.\
 I should really have them hanged for attempting to escape, but we need hands for the upcoming harvest,\
 so I'll let them go off this time with a good beating.", "lord_mission_told",
   [
       (quest_get_slot, ":quest_target_center", "$random_quest_no", slot_quest_target_center),
       (quest_get_slot, ":quest_object_center", "$random_quest_no", slot_quest_object_center),

       (str_store_troop_name_link, s9, "$g_talk_troop"),
       (str_store_party_name_link, s3, ":quest_target_center"),
       (str_store_party_name_link, s4, ":quest_object_center"),
       (setup_quest_text,"$random_quest_no"),
       (str_store_string, s2, "str_s9_asked_you_to_catch_the_three_groups_of_runaway_serfs_and_bring_them_back_to_s4_alive_and_breathing_he_said_that_all_three_groups_are_heading_towards_s3"),
    ]],
[anyone,"lord_tell_mission", [(eq,"$random_quest_no","qst_follow_spy")],
 "I have good information that a man in this very town is actually an enemy spy.\
 He should be seized and hanged for his impudence,\
 but we also believe that very soon he will leave town to meet with his master,\
 the man to whom the spy feeds all his little whispers.\
 The spy himself is of little import, but the master is a dangerous man, and could tell us a great deal\
 if we could only get our hands on him...", "lord_tell_mission_follow_spy",[]],
[anyone,"lord_tell_mission_follow_spy", [],
 "I want you to wait here until the spy leaves town. Then you must follow him, stealthily, to the meeting place.\
 You must take absolute care not to be seen by the spy on your way, else he may suspect foul play and turn back.\
 When the master appears, you must ambush and arrest them and bring the pair back to me.\
 Alive, if you please.", "lord_tell_mission_follow_spy_2",
   [
    ]],
[anyone|plyr, "lord_tell_mission_follow_spy_2", [],
 "I'll do it, {s65}.", "lord_tell_mission_follow_spy_accepted", []],
[anyone|plyr, "lord_tell_mission_follow_spy_2", [],
 "No, this skulking is not for me.", "lord_tell_mission_follow_spy_rejected", []],
[anyone,"lord_tell_mission_follow_spy_accepted", [],
   "Good, I'm sure you'll do a fine job of it. One of my men will point the spy out to you when he leaves,\
 so you will know the man to follow. Remember, I want them both, and I want them alive.", "close_window",
   [
     (str_store_troop_name_link, s11, "$g_talk_troop"),
     (str_store_party_name_link, s12, "$g_encountered_party"),
     (setup_quest_text, "$random_quest_no"),
     (str_store_string, s2, "@{s11} asked you to follow the spy that will leave {s12}. Be careful not to let the spy see you on the way, or he may get suspicious and turn back. Once the spy meets with his accomplice, you are to capture them and bring them back to {s11}."),
     (call_script, "script_start_quest", "$random_quest_no", "$g_talk_troop"),
     #TODO: Change this value
     (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 1),

     (spawn_around_party, "p_main_party", "pt_spy_partners"),
     (assign, "$qst_follow_spy_spy_partners_party", reg0),
     (party_set_position, "$qst_follow_spy_spy_partners_party", pos63),
     (party_set_ai_behavior, "$qst_follow_spy_spy_partners_party", ai_bhvr_hold),
     (party_set_flags, "$qst_follow_spy_spy_partners_party", pf_default_behavior, 0),
     (set_spawn_radius, 0),
     (spawn_around_party, "$g_encountered_party", "pt_spy"),
     (assign, "$qst_follow_spy_spy_party", reg0),
     (party_set_ai_behavior, "$qst_follow_spy_spy_party", ai_bhvr_travel_to_party),
     (party_set_ai_object, "$qst_follow_spy_spy_party", "$qst_follow_spy_spy_partners_party"),
     (party_set_flags, "$qst_follow_spy_spy_party", pf_default_behavior, 0),
     (assign, "$g_leave_town", 1),
     (rest_for_hours, 2, 4, 0),
     #no need to set g_leave_encounter to 1 since this quest can only be given at a town
   ]],
[anyone,"lord_tell_mission_follow_spy_rejected", [],
   "A shame. Well, carry on as you were, {playername}...", "lord_pretalk",
   [(troop_set_slot, "$g_talk_troop", slot_troop_does_not_give_quest, 1)]],
[anyone,"lord_tell_mission", [(eq,"$random_quest_no","qst_capture_enemy_hero")],
 "There is a difficult job I need done, {playername}, and you may be the {man/one} who can carry it off.\
 I need someone to capture one of the noble lords of {s13} and bring him to me.\
 Afterwards, I'll be able to exchange him in return for a relative of mine held by {s13}.\
 It is a simple enough job, but whomever you choose will be guarded by an elite band of personal retainers.\
 Are you up for a fight?", "lord_tell_mission_capture_enemy_hero",
   [
     (quest_get_slot, ":quest_target_faction", "$random_quest_no", slot_quest_target_faction),
     (str_store_faction_name, s13, ":quest_target_faction"),
    ]],
[anyone|plyr, "lord_tell_mission_capture_enemy_hero", [],
 "Consider it done, {s65}.", "lord_tell_mission_capture_enemy_hero_accepted", []],
[anyone|plyr, "lord_tell_mission_capture_enemy_hero", [],
 "I must refuse, {s65}. I am not a kidnapper.", "lord_tell_mission_capture_enemy_hero_rejected", []],
[anyone,"lord_tell_mission_capture_enemy_hero_accepted", [],
   "I like your spirit! Go and bring me one of our enemies,\
 and I'll toast your name in my hall when you return! And reward you for your efforts, of course...", "close_window",
   [
     (quest_get_slot, ":quest_target_faction", "$random_quest_no", slot_quest_target_faction),
     (str_store_troop_name_link, s11, "$g_talk_troop"),
     (str_store_faction_name_link, s13, ":quest_target_faction"),
     (setup_quest_text, "$random_quest_no"),
     (str_store_string, s2, "@{s11} asked you to capture a lord from {s13}, any lord, and then drag your victim back to {s11} for safekeeping."),
     (call_script, "script_start_quest", "$random_quest_no", "$g_talk_troop"),
     #TODO: Change this value
     (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 1),
     (assign, "$g_leave_encounter",1),
   ]],
[anyone,"lord_tell_mission_capture_enemy_hero_rejected", [],
   "Clearly you lack the mettle I had thought you possessed. Very well, {playername}, I will find someone else.", "lord_pretalk",
   [(troop_set_slot, "$g_talk_troop", slot_troop_does_not_give_quest, 1)]],
[anyone,"lord_tell_mission", [(eq,"$random_quest_no","qst_lend_companion")],
 "I don't have a job for you right now, but your companion {s3} is a skilled {reg3?lass:fellow}\
 and I need someone with {reg3?her:his} talents. Will you lend {reg3?her:him} to me for a while?", "lord_tell_mission_lend_companion",
   [
       (quest_get_slot, ":quest_target_troop", "$random_quest_no", slot_quest_target_troop),
       (quest_get_slot, ":quest_target_amount", "$random_quest_no", slot_quest_target_amount),
       (val_add, ":quest_target_amount", 1),
       (assign, reg1, ":quest_target_amount"),
       (str_store_troop_name_link,s9,"$g_talk_troop"),
       (str_store_troop_name,s3,":quest_target_troop"),
       (setup_quest_text,"$random_quest_no"),
	   ##diplomacy start+
       (call_script, "script_dplmc_store_troop_is_female_reg", ":quest_target_troop", 3), # <- dplmc+ replaced (troop_get_type, reg3, ":quest_target_troop")
	   ##diplomacy end+
       (str_store_string, s2, "@{s9} asked you to lend your companion {s3} to him for a week."),
    ]],
[anyone|plyr,"lord_tell_mission_lend_companion", [],
 "How long will you be needing {reg3?her:him}?", "lord_tell_mission_lend_companion_2", []],
[anyone,"lord_tell_mission_lend_companion_2", [],
 "Just a few days, a week at most.", "lord_mission_lend_companion_told", []],
[anyone|plyr,"lord_mission_lend_companion_told",
   [(quest_get_slot, ":quest_target_troop", "$random_quest_no", slot_quest_target_troop),(str_store_troop_name,s3,":quest_target_troop"),],
   "Then I will leave {s3} with you for one week.", "lord_tell_mission_lend_companion_accepted", []],
[anyone|plyr,"lord_mission_lend_companion_told", [(quest_get_slot, ":quest_target_troop", "$random_quest_no", slot_quest_target_troop),
                                                    (str_store_troop_name,s3,":quest_target_troop"),],
   "I am sorry, but I cannot do without {s3} for a whole week.", "lord_tell_mission_lend_companion_rejected", []],
[anyone,"lord_tell_mission_lend_companion_accepted", [],
   "I cannot thank you enough, {playername}. Worry not, your companion shall be returned to you with due haste.", "close_window",
   [(call_script, "script_start_quest", "$random_quest_no", "$g_talk_troop"),
    (call_script, "script_change_player_relation_with_troop","$g_talk_troop",1),
    (quest_get_slot, ":quest_target_troop", "$random_quest_no", slot_quest_target_troop),
    (party_remove_members, "p_main_party", ":quest_target_troop", 1),
    (assign, "$g_leave_encounter",1),
   ]],
[anyone,"lord_tell_mission_lend_companion_rejected", [],
   "Well, that's damned unfortunate, but I suppose I cannot force you or {s3} to agree.\
 I shall have to make do without.", "lord_pretalk",
   [(troop_set_slot, "$g_talk_troop", slot_troop_does_not_give_quest, 1)]],
[anyone,"lord_tell_mission", [(eq,"$random_quest_no","qst_collect_debt"),
  ##diplomacy start+ correct gender of s3 using reg0
  (quest_get_slot, ":quest_target_troop", "$random_quest_no", slot_quest_target_troop),
  (call_script, "script_dplmc_store_troop_is_female",  ":quest_target_troop"),
  ],
  #He -> {reg0?She:He},  him -> {reg0?her:him}
   "Some time ago, I loaned out a considerable sum of money to {s3}. {reg4} mon, to be precise.\
 {reg0?She:He} was supposed to pay it back within a month but I haven't received a copper from {reg0?her:him} since.\
 That was months ago. If you could collect the debt from {reg0?her:him} on my behalf,\
 I would be grateful indeed. I would even let you keep one fifth of the money for your trouble.\
 What do you say?", "lord_tell_mission_collect_debt",
   [
     (quest_get_slot, ":quest_target_troop", "$random_quest_no", slot_quest_target_troop),
     (quest_get_slot, ":quest_target_center", "$random_quest_no", slot_quest_target_center),
     (quest_get_slot, reg4, "$random_quest_no", slot_quest_target_amount),
     (str_store_troop_name_link,s9,"$g_talk_troop"),
     (str_store_troop_name_link,s3,":quest_target_troop"),
     (str_store_party_name_link,s4,":quest_target_center"),
     (setup_quest_text,"$random_quest_no"),
	 ##Also correct pronoun in the quest text
	 #Next line: changed "him" to "{reg65?her:him}"
     (str_store_string, s2, "@{s9} asked you to collect the debt of {reg4} mon {s3} owes to {reg65?her:him}. {s3} was at {s4} when you were given this quest."),
   ]],
[anyone|plyr,"lord_tell_mission_collect_debt", [],
 "Do you know where I can find {s3}, {s65}?", "lord_tell_mission_collect_debt_2", []],
[anyone,"lord_tell_mission_collect_debt_2", [
  ##diplomacy start+ correct gender of s3 using reg0
  (quest_get_slot, ":quest_target_troop", "$random_quest_no", slot_quest_target_troop),#added
  (call_script, "script_dplmc_store_troop_is_female",  ":quest_target_troop"),#added
  ],#Next line, change pronouns:
 "If you leave now, you should be able to find {reg0?her:him} at {s4}.\
 I've no doubt that {reg0?she:he} will be suitably embarassed by {reg0?her:his} conduct and give you all the money {reg0?she:he} owes me.", "lord_tell_mission_collect_debt_3", []],
[anyone|plyr,"lord_tell_mission_collect_debt_3", [], "Then I will talk to {s3} on your behalf.", "lord_tell_mission_collect_debt_accepted", []],
[anyone|plyr,"lord_tell_mission_collect_debt_3", [], "Forgive me, {s65}, but I doubt I would be more successful than yourself.", "lord_tell_mission_collect_debt_rejected", []],
[anyone,"lord_tell_mission_collect_debt_accepted", [
##diplomacy start+ correct gender of s3 using reg0
  (quest_get_slot, ":quest_target_troop", "$random_quest_no", slot_quest_target_troop),#added
  (call_script, "script_dplmc_store_troop_is_female",  ":quest_target_troop"),#added
  #Next line, change pronoun:
  ], "You made me very happy by accepting this {playername}. Please, talk to {s3} and don't leave {reg0?her:him} without my money.", "close_window",
##diplomacy end+
   [(call_script, "script_start_quest", "$random_quest_no", "$g_talk_troop"),
    (call_script, "script_change_player_relation_with_troop","$g_talk_troop", 1),
    (assign, "$g_leave_encounter",1),
   ]],
[anyone,"lord_tell_mission_collect_debt_rejected", [], "Perhaps not, {playername}. I suppose I'm never getting that money back...", "lord_pretalk",
   [(troop_set_slot, "$g_talk_troop", slot_troop_does_not_give_quest, 1)]],
[anyone,"lord_tell_mission", [(eq, "$random_quest_no", "qst_incriminate_loyal_commander"),
                                (quest_get_slot, ":quest_target_troop", "qst_incriminate_loyal_commander", slot_quest_target_troop),
                                (quest_get_slot, ":quest_object_troop", "qst_incriminate_loyal_commander", slot_quest_object_troop),
                                (quest_get_slot, ":quest_target_center", "qst_incriminate_loyal_commander", slot_quest_target_center),
                                (str_store_troop_name_link, s13,":quest_target_troop"),
                                (str_store_party_name_link, s14,":quest_target_center"),
                                (str_store_troop_name_link, s15,":quest_object_troop"),
								##diplomacy start+ use correct gender for "s13" pronouns using reg3
								(call_script, "script_dplmc_store_troop_is_female_reg", ":quest_target_troop", 3), # <- dplmc+ replaced (troop_get_type, reg3, ":quest_target_troop")
                                ],
#Changed pronouns in next line: "his" to "{reg3?her:his}", "him" to "{reg3?her:him}", and "he" to "{reg3?she:he}"
 "I tell you, that blubbering fool {s13} is not fit to rule {s14}.\
 God knows {reg3?she:he} would be divested of {reg3?her:his} lands in an instant were it not for one of {reg3?her:his} loyal vassals, {s15}.\
 As long as {reg3?she:he} has {reg3?her:his} vassal aiding {reg3?her:him}, it will be a difficult job beating {reg3?her:him}.\
 So I need to get {s15} out of the picture, and I have a plan just to do that...\
 With your help, naturally.", "lord_tell_mission_incriminate_commander",[]],
[anyone|plyr,"lord_tell_mission_incriminate_commander", [], "{s66}, I am all ears.", "lord_tell_mission_incriminate_commander_2",[]],
[anyone|plyr,"lord_tell_mission_incriminate_commander", [], "I don't wish to involve myself in anything dishonourable against {s15}.", "lord_tell_mission_incriminate_commander_rejected",[]],
[anyone,"lord_tell_mission_incriminate_commander_rejected", [], "Dishonourable? Bah!\
 I was hoping I could count on you, {playername}, but you've shown me what a fool I was.\
 I shall have to find someone whose loyalty I can trust.", "lord_pretalk",
   [(call_script, "script_change_player_relation_with_troop","$g_talk_troop",-5),
    (call_script, "script_change_player_honor", 2)]],
[anyone,"lord_tell_mission_incriminate_commander_2", [
	##diplomacy start+ use correct gender for the other lord "s13" using reg3 (may be female)
	(quest_get_slot, ":quest_target_troop", "qst_incriminate_loyal_commander", slot_quest_target_troop),
	(call_script, "script_dplmc_store_troop_is_female_reg", ":quest_target_troop", 3),
	#Also get correct gender for "s15" using reg4
	(quest_get_slot, ":quest_object_troop", "qst_incriminate_loyal_commander", slot_quest_object_troop),
	(call_script, "script_dplmc_store_troop_is_female", ":quest_object_troop"),
	(assign, reg0, reg4),
	#Change the pronouns in the next line:
	], "I have written a fake letter to {s15},\
 bearing my own seal, which implicates {reg4?her:him} in a conspiracy with us to stage a coup in {s14}, in my favour.\
 If we can make {s13} believe the letter is genuine, {reg3?she:he} will deal with {s15} very swiftly.\
 Of course, the challenge there is to convince {s13} that the letter is indeed real...", "lord_tell_mission_incriminate_commander_3",[]],
[anyone|plyr,"lord_tell_mission_incriminate_commander_3", [], "Please continue, {s65}...", "lord_tell_mission_incriminate_commander_4",[]],
[anyone|plyr,"lord_tell_mission_incriminate_commander_3", [], "No, I will not sully myself with this dishonourable scheme.", "lord_tell_mission_incriminate_commander_rejected",[]],
[anyone,"lord_tell_mission_incriminate_commander_4", [], "This is where you come into play.\
 You'll take the letter to {s14}, then give it to one of your soldiers and instruct him to take it to {s15}.\
 I will have one of my spies inform the town garrison so that your man will be arrested on his way.\
 The guards will then find the letter and take it to {s13}.\
 They'll torture your man, of course, to try and get the truth out of him,\
 but all he knows is that you ordered the letter to be delivered to {s15} under the utmost secrecy.\
 {s13} knows you serve me, and the fool will certainly believe the whole charade.", "lord_tell_mission_incriminate_commander_5",[]],
[anyone|plyr,"lord_tell_mission_incriminate_commander_5", [], "Is that all?", "lord_tell_mission_incriminate_commander_7",[]],
[anyone,"lord_tell_mission_incriminate_commander_7", [(str_store_troop_name, s8, "$incriminate_quest_sacrificed_troop"),
                                                        (str_store_troop_name_plural, s9, "$incriminate_quest_sacrificed_troop"),
       ##diplomacy start+ use correct gender for the other lord "s13" using reg3 (may be female)
	   (quest_get_slot, ":quest_target_troop", "qst_incriminate_loyal_commander", slot_quest_target_troop),
	   (call_script, "script_dplmc_store_troop_is_female_reg", ":quest_target_troop", 3),
      ], "There is one more thing...\
 Your messenger must be someone trustworthy. If you sent the letter with a simple peasant, someone expendable,\
 {s13} might suspect a plot. {reg3?She:He} may have the wits of a snail, but even a snail can see the obvious.\
 Give the letter to someone of rank. One of your {s9}, perhaps.", "lord_tell_mission_incriminate_commander_8",[]],
[anyone|plyr,"lord_tell_mission_incriminate_commander_8", [], "What? I can't send one of my trusted {s9} to his death!", "lord_tell_mission_incriminate_commander_9",[]],
[anyone|plyr,"lord_tell_mission_incriminate_commander_8", [], "Then a {s8} it will be.", "lord_tell_mission_incriminate_commander_fin",[]],
[anyone,"lord_tell_mission_incriminate_commander_9", [], "Come now, {playername}.\
 There is a place for sentimentality, but this is not it. Believe me, you shall be generously compensated,\
 and what is the purpose of soldiers if not to die at our say-so?", "lord_tell_mission_incriminate_commander_10",[]],
[anyone|plyr,"lord_tell_mission_incriminate_commander_10", [], "A {s8} it is.", "lord_tell_mission_incriminate_commander_fin",[]],
[anyone|plyr,"lord_tell_mission_incriminate_commander_10", [], "No, I'll not sacrifice one of my chosen men.", "lord_tell_mission_incriminate_commander_rejected",[]],
[anyone,"lord_tell_mission_incriminate_commander_fin", [], "I can't tell you how pleased I am to hear that,\
 {playername}. You are removing one of the greatest obstacles in my path.\
 Here is the letter, as well as 300 mon for your expenses.\
 Remember, there'll be more once you succeed. Much, much more...", "lord_pretalk",
   [
       (quest_get_slot, ":quest_target_troop", "qst_incriminate_loyal_commander", slot_quest_target_troop),
       (quest_get_slot, ":quest_object_troop", "qst_incriminate_loyal_commander", slot_quest_object_troop),
       (quest_get_slot, ":quest_target_center", "qst_incriminate_loyal_commander", slot_quest_target_center),
       (call_script, "script_troop_add_gold", "trp_player", 300),
       (call_script, "script_change_player_relation_with_troop","$g_talk_troop",2),
       (str_store_troop_name_link, s11,"$g_talk_troop"),
       (str_store_troop_name_link, s13,":quest_target_troop"),
       (str_store_party_name_link, s14,":quest_target_center"),
       (str_store_troop_name_plural, s15,"$incriminate_quest_sacrificed_troop"),
       (str_store_troop_name_link, s16,":quest_object_troop"),
       (setup_quest_text,"$random_quest_no"),
	   ##diplomacy start+ use correct gender for the other lord "s13" using reg3 (may be female)
	   (call_script, "script_dplmc_store_troop_is_female_reg", ":quest_target_troop", 3),
       (str_store_string, s2, "@{s11} gave you a fake letter to fool {s13} into banishing his vassal {s16}.\
 You are to go near {s14}, give the letter to one of your {s15} and send him into the town as a messenger,\
 believing his orders to be genuine."),#changed "his vassal" into "{reg3?her:his} vassal"
       ##diplomacy end+
       (call_script, "script_start_quest", "$random_quest_no", "$g_talk_troop"),
    ]],
[anyone,"lord_tell_mission", [(eq,"$random_quest_no","qst_capture_prisoners")],
 "A group of my soldiers were captured in a recent skirmish with the enemy.\
 Thankfully we have a mutual agreement of prisoner exchange, and they will release my men,\
 but they want us to give them prisoners of equal rank and number. Prisoners I don't currently have.\
 So, I need a good {man/warrior} to find me {reg1} {s3} as prisoners, that I may exchange them.", "lord_mission_told",
   [
       (quest_get_slot, ":quest_target_troop", "qst_capture_prisoners", slot_quest_target_troop),
       (quest_get_slot, ":quest_target_amount", "qst_capture_prisoners", slot_quest_target_amount),
       (assign,reg1,":quest_target_amount"),
       (str_store_troop_name_link,s9,"$g_talk_troop"),
       (str_store_troop_name_by_count,s3,":quest_target_troop",":quest_target_amount"),
       (setup_quest_text,"$random_quest_no"),
       (str_store_string, s2, "@{s9} has requested you to bring him {reg1} {s3} as prisoners."),
    ]],
[anyone,"lord_tell_mission", [], "No {playername}. I do not need your help at this time.", "lord_pretalk",[]],
[anyone|plyr,"lord_mission_told", [], "You can count on me, {s65}.", "lord_mission_accepted",[]],
[anyone|plyr,"lord_mission_told", [], "I fear I cannot accept such a mission at the moment.", "lord_mission_rejected",[]],
[anyone,"lord_mission_accepted", [], "Excellent, {playername}, excellent. I have every confidence in you.", "close_window",
   [(assign, "$g_leave_encounter",1),
    (try_begin),
      (eq, "$random_quest_no", "qst_escort_lady"),
      (quest_get_slot, ":quest_object_troop", "$random_quest_no", slot_quest_object_troop),
      (troop_set_slot, ":quest_object_troop", slot_troop_cur_center, 0),
      (troop_join, ":quest_object_troop"),
##    (else_try),
##      (eq, "$random_quest_no", "qst_hunt_down_raiders"),
##      (quest_get_slot, ":quest_object_center", "$random_quest_no", slot_quest_object_center),
##      (quest_get_slot, ":quest_target_center", "$random_quest_no", slot_quest_target_center),
##      (quest_get_slot, ":quest_target_faction", "$random_quest_no", slot_quest_target_faction),
##      (set_spawn_radius, 3),
##      (call_script, "script_cf_create_kingdom_party", ":quest_target_faction", spt_raider),
###      (spawn_around_party,":quest_object_center",":quest_target_party_template"),
##      (assign, ":quest_target_party", reg0),
##      (party_relocate_near_party, reg0, ":quest_object_center"),
##      (quest_set_slot, "$random_quest_no", slot_quest_target_party, ":quest_target_party"),
##      (party_set_ai_behavior,":quest_target_party",ai_bhvr_travel_to_party),
##      (party_set_ai_object,":quest_target_party",":quest_target_center"),
##      (party_set_flags, ":quest_target_party", pf_default_behavior, 0),
##      (party_set_faction,":quest_target_party",":quest_target_faction"),
##      (str_store_troop_name,1,"$g_talk_troop"),
##      (str_store_party_name,2,"$g_encountered_party"),
##      (str_store_party_name,3,":quest_object_center"),
##      (str_store_party_name,4,":quest_target_center"),
##      (setup_quest_text,"$random_quest_no"),
##      (try_begin),
##        (is_between, "$g_encountered_party", centers_begin, centers_end),
##        (setup_quest_giver, "$random_quest_no", "str_given_by_s1_at_s2"),
##      (else_try),
##        (setup_quest_giver,"$random_quest_no", "str_given_by_s1_in_wilderness"),
##      (try_end),
##    (else_try),
##      (eq, "$random_quest_no", "qst_bring_reinforcements_to_siege"),
##      (quest_get_slot, ":quest_object_troop", "$random_quest_no", slot_quest_object_troop),
##      (quest_get_slot, ":quest_target_amount", "$random_quest_no", slot_quest_target_amount),
##      (troop_get_slot, ":cur_party", "$g_talk_troop", slot_troop_leaded_party),
##      (party_remove_members, ":cur_party", ":quest_object_troop", ":quest_target_amount"),
##      (party_add_members, "p_main_party", ":quest_object_troop", ":quest_target_amount"),
##    (else_try),
##      (eq, "$random_quest_no", "qst_bring_prisoners_to_enemy"),
##      (quest_get_slot, ":quest_object_troop", "$random_quest_no", slot_quest_object_troop),
##      (quest_get_slot, ":quest_target_amount", "$random_quest_no", slot_quest_target_amount),
##      (party_add_prisoners, "p_main_party", ":quest_object_troop", ":quest_target_amount"),
    (else_try),
      (eq, "$random_quest_no", "qst_deliver_message_to_enemy_lord"),
      (call_script, "script_troop_add_gold", "trp_player", 10),
    (else_try),
      (eq, "$random_quest_no", "qst_bring_back_runaway_serfs"),
      (quest_get_slot, ":quest_giver_center", "$random_quest_no", slot_quest_giver_center),
      (quest_get_slot, ":quest_target_center", "$random_quest_no", slot_quest_target_center),
      (quest_get_slot, ":quest_target_party_template", "$random_quest_no", slot_quest_target_party_template),

      (set_spawn_radius, 3),
      (spawn_around_party,":quest_giver_center",":quest_target_party_template"),
      (assign, "$qst_bring_back_runaway_serfs_party_1", reg0),
      (party_set_ai_behavior,"$qst_bring_back_runaway_serfs_party_1",ai_bhvr_travel_to_party),
      (party_set_ai_object,"$qst_bring_back_runaway_serfs_party_1",":quest_target_center"),
      (party_set_flags, "$qst_bring_back_runaway_serfs_party_1", pf_default_behavior, 0),
      (spawn_around_party,":quest_giver_center",":quest_target_party_template"),
      (assign, "$qst_bring_back_runaway_serfs_party_2", reg0),
      (party_set_ai_behavior,"$qst_bring_back_runaway_serfs_party_2",ai_bhvr_travel_to_party),
      (party_set_ai_object,"$qst_bring_back_runaway_serfs_party_2",":quest_target_center"),
      (party_set_flags, "$qst_bring_back_runaway_serfs_party_2", pf_default_behavior, 0),
      (spawn_around_party,":quest_giver_center",":quest_target_party_template"),
      (assign, "$qst_bring_back_runaway_serfs_party_3", reg0),
      (party_set_ai_behavior,"$qst_bring_back_runaway_serfs_party_3",ai_bhvr_travel_to_party),
      (party_set_ai_object,"$qst_bring_back_runaway_serfs_party_3",":quest_target_center"),
      (party_set_flags, "$qst_bring_back_runaway_serfs_party_3", pf_default_behavior, 0),
      (rest_for_hours, 1, 4),
##    (else_try),
##      (eq, "$random_quest_no", "qst_capture_conspirators"),
##      (quest_get_slot, ":quest_target_center", "$random_quest_no", slot_quest_target_center),
##      (spawn_around_party,"p_main_party","pt_conspirator_leader"),
##      (assign, "$qst_capture_conspirators_party_1", reg0),
##      (assign, "$qst_capture_conspirators_num_parties_spawned", 1),
##      (party_set_ai_behavior, "$qst_capture_conspirators_party_1", ai_bhvr_hold),
##      (party_set_flags, "$qst_capture_conspirators_party_1", pf_default_behavior, 0),
##      (party_get_position, pos1, ":quest_target_center"),
##      (call_script, "script_map_get_random_position_around_position_within_range", 17, 19),
##      (party_set_position, "$qst_capture_conspirators_party_1", pos2),
##      (party_get_num_companions, ":num_companions", "$qst_capture_conspirators_party_1"),
##      (val_add, "$qst_capture_conspirators_num_troops_to_capture", ":num_companions"),
##    (else_try),
##      (eq, "$random_quest_no", "qst_defend_nobles_against_peasants"),
##      (quest_get_slot, ":quest_target_center", "$random_quest_no", slot_quest_target_center),
##      (set_spawn_radius, 9),
##      (try_for_range, ":unused", 0, "$qst_defend_nobles_against_peasants_num_peasant_parties_to_spawn"),
##        (spawn_around_party, ":quest_target_center", "pt_shinano_rebels"),
##        (try_begin),
##          (le, "$qst_defend_nobles_against_peasants_peasant_party_1", 0),
##          (assign, "$qst_defend_nobles_against_peasants_peasant_party_1", reg0),
##        (else_try),
##          (le, "$qst_defend_nobles_against_peasants_peasant_party_2", 0),
##          (assign, "$qst_defend_nobles_against_peasants_peasant_party_2", reg0),
##        (else_try),
##          (le, "$qst_defend_nobles_against_peasants_peasant_party_3", 0),
##          (assign, "$qst_defend_nobles_against_peasants_peasant_party_3", reg0),
##        (else_try),
##          (le, "$qst_defend_nobles_against_peasants_peasant_party_4", 0),
##          (assign, "$qst_defend_nobles_against_peasants_peasant_party_4", reg0),
##        (else_try),
##          (le, "$qst_defend_nobles_against_peasants_peasant_party_5", 0),
##          (assign, "$qst_defend_nobles_against_peasants_peasant_party_5", reg0),
##        (else_try),
##          (le, "$qst_defend_nobles_against_peasants_peasant_party_6", 0),
##          (assign, "$qst_defend_nobles_against_peasants_peasant_party_6", reg0),
##        (else_try),
##          (le, "$qst_defend_nobles_against_peasants_peasant_party_7", 0),
##          (assign, "$qst_defend_nobles_against_peasants_peasant_party_7", reg0),
##        (else_try),
##          (le, "$qst_defend_nobles_against_peasants_peasant_party_8", 0),
##          (assign, "$qst_defend_nobles_against_peasants_peasant_party_8", reg0),
##        (try_end),
##      (try_end),
##      (set_spawn_radius, 0),
##      (party_get_position, pos1, ":quest_target_center"),
##      (try_for_range, ":unused", 0, "$qst_defend_nobles_against_peasants_num_noble_parties_to_spawn"),
##        (spawn_around_party, ":quest_target_center", "pt_noble_refugees"),
##        (assign, ":cur_noble_party", reg0),
##        (party_set_ai_behavior, ":cur_noble_party", ai_bhvr_travel_to_party),
##        (party_set_ai_object, ":cur_noble_party", ":quest_target_center"),
##	    (party_set_flags, ":cur_noble_party", pf_default_behavior, 0),
##        (call_script, "script_map_get_random_position_around_position_within_range", 13, 17),
##        (party_set_position, ":cur_noble_party", pos2),
##        (party_get_num_companions, ":num_companions", ":cur_noble_party"),
##        (val_add, "$qst_defend_nobles_against_peasants_num_nobles_to_save", ":num_companions"),
##        (try_begin),
##          (le, "$qst_defend_nobles_against_peasants_noble_party_1", 0),
##          (assign, "$qst_defend_nobles_against_peasants_noble_party_1", reg0),
##        (else_try),
##          (le, "$qst_defend_nobles_against_peasants_noble_party_2", 0),
##          (assign, "$qst_defend_nobles_against_peasants_noble_party_2", reg0),
##        (else_try),
##          (le, "$qst_defend_nobles_against_peasants_noble_party_3", 0),
##          (assign, "$qst_defend_nobles_against_peasants_noble_party_3", reg0),
##        (else_try),
##          (le, "$qst_defend_nobles_against_peasants_noble_party_4", 0),
##          (assign, "$qst_defend_nobles_against_peasants_noble_party_4", reg0),
##        (else_try),
##          (le, "$qst_defend_nobles_against_peasants_noble_party_5", 0),
##          (assign, "$qst_defend_nobles_against_peasants_noble_party_5", reg0),
##        (else_try),
##          (le, "$qst_defend_nobles_against_peasants_noble_party_6", 0),
##          (assign, "$qst_defend_nobles_against_peasants_noble_party_6", reg0),
##        (else_try),
##          (le, "$qst_defend_nobles_against_peasants_noble_party_7", 0),
##          (assign, "$qst_defend_nobles_against_peasants_noble_party_7", reg0),
##        (else_try),
##          (le, "$qst_defend_nobles_against_peasants_noble_party_8", 0),
##          (assign, "$qst_defend_nobles_against_peasants_noble_party_8", reg0),
##        (try_end),
##      (try_end),
    (try_end),
    (call_script, "script_start_quest", "$random_quest_no", "$g_talk_troop"),
    (try_begin),
      (eq, "$random_quest_no", "qst_lend_surgeon"),
      (assign, "$g_leave_town_outside", 1),
      (assign,"$auto_enter_town","$g_encountered_party"),
#      (store_current_hours, "$quest_given_time"),
      (rest_for_hours, 4),
      (assign, "$lord_requested_to_talk_to", "$g_talk_troop"),
    (try_end),
    ]],
[anyone,"lord_mission_rejected", [], "Is that so? Well, I suppose you're just not up to the task.\
 I shall have to look for somebody with more mettle.", "close_window",
   [(assign, "$g_leave_encounter",1),
    (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", -1),
    (try_begin),
      (quest_slot_eq, "$random_quest_no", slot_quest_dont_give_again_remaining_days, 0),
      (quest_set_slot, "$random_quest_no", slot_quest_dont_give_again_remaining_days, 1),
    (try_end),
    (troop_set_slot, "$g_talk_troop", slot_troop_does_not_give_quest, 1),
    ]],
[anyone|plyr,"lord_talk",
  [
    (troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
  ], "I must leave now.", "lord_leave_prison",[]],
[anyone|plyr,"lord_talk",
  [
    (lt, "$g_talk_troop_faction_relation", 0),
    (neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
  ], "This audience is over. I leave now.", "lord_leave",[]],
[anyone|plyr,"lord_talk",
     [
       (troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
       (party_slot_eq, "$current_town", slot_town_lord, "trp_player"),
     ], "You are free to go.", "dplmc_prisoner_chat_let_go",
     [
       (call_script, "script_remove_troop_from_prison", "$g_talk_troop"),
       (troop_set_slot, "$g_talk_troop", slot_troop_leaded_party, -1),
       (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 3),
       (call_script, "script_change_player_honor", 2),
       (call_script, "script_add_log_entry", logent_lord_defeated_but_let_go_by_player, "trp_player",  -1, "$g_talk_troop", "$g_talk_troop_faction"),
     ]],
[anyone|plyr,"lord_talk",
  [
    (ge, "$g_talk_troop_faction_relation", 0),
    (neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
  ], "I must beg my leave.", "lord_leave",[]],
[anyone,"lord_leave", [#(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 0),
      (neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
      (lt, "$g_talk_troop_faction_relation", 0),
      (store_partner_quest,":enemy_lord_quest"),
      (lt, ":enemy_lord_quest", 0),
      (troop_slot_eq, "$g_talk_troop", slot_troop_does_not_give_quest, 0),
      (call_script, "script_get_quest", "$g_talk_troop"),
      (assign, "$random_quest_no", reg0),
      (ge, "$random_quest_no", 0),
	  (this_or_next|eq, "$random_quest_no", "qst_lend_surgeon"), #so far only for quest lend surgeon
		(eq, 2, 1),
    ],
   "Before you go, {playername}, I have something to ask of you... We may be enemies in this war,\
 but I pray that you believe, as I do, that we can still be civil towards each other.\
 Thus I hoped that you would be kind enough to assist me in something important to me.", "lord_leave_give_quest",[]],
[anyone|plyr,"lord_leave_give_quest", [],
   "I am listening.", "enemy_lord_tell_mission",[]],
[anyone,"lord_leave_prison", [],
   "We'll meet again.", "close_window",[]],
[anyone|auto_proceed,"lord_leave", [
 ##diplomacy start+
#	(troop_get_type, ":type", "trp_player"),
#	(eq, ":type", 1),
	(eq, 1, "$character_gender"),
##diplomacy end+
	(call_script, "script_troop_get_romantic_chemistry_with_troop", "trp_player", "$g_talk_troop"),
	(gt, reg0, 7),
	(ge, "$g_talk_troop_relation", 0),
	(neg|troop_slot_ge, "$g_talk_troop", slot_troop_betrothed, active_npcs_begin),
	(neg|troop_slot_ge, "$g_talk_troop", slot_troop_spouse, active_npcs_begin),
	(neg|troop_slot_ge, "trp_player", slot_troop_betrothed, active_npcs_begin),
	(neg|troop_slot_ge, "trp_player", slot_troop_spouse, active_npcs_begin),

	(neg|faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, "$g_talk_troop"),

 ],
   "Farewell, my lady. I shall remain your most ardent admirer.", "close_window",
   [(eq,"$talk_context",tc_party_encounter),
   (assign, "$g_leave_encounter", 1)]],
[anyone|auto_proceed,"lord_leave", [(faction_slot_eq,"$g_talk_troop_faction",slot_faction_leader,"$g_talk_troop")],
   "Of course, {playername}. Farewell.", "close_window",[(eq,"$talk_context",tc_party_encounter),(assign, "$g_leave_encounter", 1)]],
[anyone|auto_proceed,"lord_leave", [(ge,"$g_talk_troop_relation",10)],
   "Good journeys to you, {playername}.", "close_window",[(eq,"$talk_context",tc_party_encounter),(assign, "$g_leave_encounter", 1)]],
[anyone|auto_proceed,"lord_leave", [(ge, "$g_talk_troop_faction_relation", 0)],
   "Yes, yes. Farewell.", "close_window",[(eq,"$talk_context",tc_party_encounter),(assign, "$g_leave_encounter", 1)]],
[anyone|auto_proceed,"lord_leave", [],
   "We will meet again.", "close_window",[(eq,"$talk_context",tc_party_encounter),(assign, "$g_leave_encounter", 1)]],
[anyone,"lady_journey_1", [],
   "I am doing quite fine, {playername}. Thank you for your concern.", "close_window",[]],
[anyone,"lady_stranded_next",
  ##diplomacy start+ change to use script_dplmc_print_subordinate_says_sir_madame_to_s0
   #[],
   [(call_script, "script_dplmc_print_subordinate_says_sir_madame_to_s0"),],#added
   "Greetings, {s0}. The tides of war have left me stranded here in this fortress, but I will shortly be departing. ", "close_window",[#changed {sir/my lady} to {s0}
   ##diplomacy end+
 ]],
[anyone|plyr,"lady_talk_refugee",
   [],
   "Of course, my lady", "close_window",[
    (troop_get_slot, ":current_location", "$g_talk_troop", slot_troop_cur_center),
	(call_script, "script_get_kingdom_lady_social_determinants", "$g_talk_troop"),
	(assign, ":new_location", reg1),
	(troop_set_slot, "$g_talk_troop", slot_troop_cur_center, ":new_location"),
	(try_begin),
		(neq, ":current_location", ":new_location"),
		(call_script, "script_troop_change_relation_with_troop", "trp_player", "$g_talk_troop", 1),
    (try_end),
 ]],
[anyone|plyr,"lady_talk_refugee",
   [],
   ##diplomacy start+ Allow the possibility of male versions of the lines
   #changed "my lady" to "{reg65?my lady:sirrah}"
   "You assume wrong, {reg65?my lady:sirrah}!", "lady_captive_talk",[
   ##diplomacy end+
 ]],
[anyone,"lady_captive_talk",
   [],
   "What?! What infamy is this?", "lady_captive_confirm",[
 ]],
[anyone|plyr,"lady_captive_confirm",
   [],
   "My apologies - you must have misunderstood me. Of course you may leave.", "close_window",[
 ]],
[anyone|plyr,"lady_captive_confirm",
   [],
   "Contact your family to arrange for a ransom, my lady.", "close_window",[
    (troop_set_slot, "$g_talk_troop", slot_troop_prisoner_of_party, "$g_encountered_party"),
	(call_script, "script_change_player_honor", -2),
	(call_script, "script_troop_change_relation_with_troop", "trp_player", "$g_talk_troop", -10),
    ##diplomacy start+
    #There are other people who this would annoy: The woman's father (usually her legal guardian
	#before she marries), her brother (especially if her father is dead), her husband or fiance,
	#and possibly any suitors.  Other relatives may be irritated to a greater or lesser degree,
	#but those will be the primary ones.
	(call_script, "script_get_kingdom_lady_social_determinants", "$g_talk_troop"),
	(assign, ":guardian", reg0),
	(store_faction_of_troop, ":guardian_faction", ":guardian"),

	(try_for_range, ":troop_no", heroes_begin, heroes_end),
		(this_or_next|troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
			(troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_lady),
		(neq, "$g_talk_troop", ":troop_no"),
		(neq, ":troop_no", active_npcs_including_player_begin),
		(store_faction_of_troop, ":troop_faction", ":troop_no"),

		(this_or_next|is_between, ":troop_no", kingdom_ladies_begin, kingdom_ladies_end),
			(eq, ":troop_faction", ":guardian_faction"),
		(assign, ":relation_change", 0),

		(try_begin),
			(eq, ":troop_no", ":guardian"),
			(val_min, ":relation_change", -10),
		(try_end),

		#family
		(call_script, "script_troop_get_family_relation_to_troop", "$g_talk_troop", ":troop_no"),
		(val_min, reg0, 10),
		(store_mul, ":relation_change", reg0, -1),

		#Family-centric characters are more upset
		(try_begin),
			(ge, reg0, 2),
			(troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_conventional),
			(val_sub, ":relation_change", 1),
		(try_end),

		(try_begin),
			#betrothed
			(troop_slot_eq, ":troop_no", slot_troop_betrothed, "$g_talk_troop"),
			(val_min, ":relation_change", -10),
		(else_try),
			(lt, reg0, 2),
			#suitors
			(is_between, ":troop_no", lords_begin, lords_end),
			(this_or_next|troop_slot_eq, ":troop_no", slot_troop_love_interest_1, "$g_talk_troop"),
			(this_or_next|troop_slot_eq, ":troop_no", slot_troop_love_interest_2, "$g_talk_troop"),
				(troop_slot_eq, ":troop_no", slot_troop_love_interest_3, "$g_talk_troop"),

			(call_script, "script_troop_get_relation_with_troop", ":troop_no", "$g_talk_troop"),
			(assign, ":fondness", reg0),

			(ge, ":fondness", 5),
			(val_min, ":relation_change", -1),
			(ge, ":fondness", 10),
			(val_min, ":relation_change", -2),
			(ge, ":fondness", 15),
			(val_min, ":relation_change", -3),
			(ge, ":fondness", 20),
			(val_min, ":relation_change", -4),
		(try_end),

		#Some lords are more prone to fury at personal offenses than others
		(try_begin),
			(troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_quarrelsome),
			(lt, ":relation_change", 0),
			(val_sub, ":relation_change", 2),
		(try_end),

		#Now apply the modification
		(lt, ":relation_change", 0),
		(call_script, "script_troop_change_relation_with_troop", "trp_player", ":troop_no", ":relation_change"),
	(try_end),
##diplomacy end+
#incomplete -- make sure ransoms are offered for ladies
 ]],
[anyone|plyr,"lady_duel_lost",
	[], "Very well - we must do as tradition demands... Farewell, my lady", "close_window", [
 ]],
[anyone|plyr,"lady_duel_lost",
	[], "Let honor and tradition hang!", "lady_duel_lost_flaunt_conventions", [
	]],
[anyone, "lady_duel_lost_flaunt_conventions",
	[], "Oh, {playername}! Although people will talk, it would so break my heart to no longer be able to see you. We shall ignore this silly, cruel tradition.", "close_window", [
	(troop_set_slot, "$g_talk_troop", slot_troop_met, 2),
	(call_script, "script_change_player_honor", -5),
	]],
[anyone, "lady_duel_lost_flaunt_conventions",
	[], "No, {playername} -- I cannot afford to fritter away my good name, and neither can you.", "close_window", [
	]],
[anyone,"lady_duel_rep_1",
   [],
   ##diplomacy start+ make an alternate gender version just in case
   "Well, {playername} --  you won your duel with {s10}. Oh, such foolishness, that {men/people} should fight over me! Sigh... But it is a bit romantic, I suppose.", "lady_start",[
   ##diplomacy end+
   (call_script, "script_end_quest", "qst_duel_courtship_rival"),
	(call_script, "script_troop_change_relation_with_troop", "trp_player", "$g_talk_troop", 1),
    (add_xp_as_reward, 1000),
 ]],
[anyone,"lady_duel_rep_2",
   [##diplomacy start+
	#check pronouns in case it's possible for the other lord to be a woman
	(quest_get_slot, ":quest_target_troop", "qst_duel_courtship_rival", slot_quest_target_troop),
	(call_script, "script_dplmc_store_troop_is_female", ":quest_target_troop"),
	],
   "Well, {playername} --  you won your duel with {s10}. Honor now demands that {reg0?she:he} and I no longer meet... I was fond of {reg0?her:him}, you know. You did me no service by fighting {reg0?her:him}, {sir/madame}.", "lady_start",[
   ##diplomacy end+
	(call_script, "script_end_quest", "qst_duel_courtship_rival"),
	(call_script, "script_troop_change_relation_with_troop", "trp_player", "$g_talk_troop", -2),
    (add_xp_as_reward, 1000),
 ]],
[anyone|plyr,"lady_qst_duel_for_lady_succeeded_1", [], "Oh, it will just have to do.", "lady_qst_duel_for_lady_succeeded_2",[
  (str_store_string,s10,"@Then take it, with my eternal thanks. You are a noble {man/woman}.\
 I will never forget that you helped me in my time of need.")
  ]],
[anyone|plyr,"lady_qst_duel_for_lady_succeeded_1", [], "{s66}, this is far too much!", "lady_qst_duel_for_lady_succeeded_2",[
  (str_store_string,s10,"@Forgive me, {playername}, but I must insist you accept it.\
 The money means little to me, and I owe you so much.\
 Here, take it, and let us speak no more of this."),
    (call_script, "script_change_player_honor", 1),
  ]],
[anyone|plyr,"lady_qst_duel_for_lady_succeeded_1", [], "Please, {s65}, no reward is necessary.", "lady_qst_duel_for_lady_succeeded_2",[
  (str_store_string,s10,"@{playername}, what a dear {man/woman} you are,\
 but I will not allow you to refuse this. I owe you far more than I can say,\
 and I am sure you can put this money to far better use than I."),
    (call_script, "script_change_player_honor", 2),
  ]],
[anyone,"lady_qst_duel_for_lady_succeeded_2", [], "{s10}", "lady_pretalk",
   [(call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 10),
    (add_xp_as_reward, 1000),
    (call_script, "script_troop_add_gold", "trp_player", 2000),
    (call_script, "script_end_quest", "qst_duel_for_lady"),
    ]],
[anyone|plyr,"lady_qst_duel_for_lady_failed", [], "I beg your forgiveness for my defeat, {s65}...", "lady_qst_duel_for_lady_failed_2",[]],
[anyone,"lady_qst_duel_for_lady_failed_2", [], "It matters not, dear {playername}. You tried.\
 The truth cannot be proven at the point of a sword, but you willingly put your life at stake for my honour.\
 That alone will convince many of my innocence.", "lady_pretalk",
   [(call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 6),
    (add_xp_as_reward, 400),
    (call_script, "script_end_quest", "qst_duel_for_lady"),
    ]],
[anyone|plyr,"lady_escort_lady_succeeded", [], "It was an honor to serve you, {s65}.", "close_window",[]],
[anyone,"lady_start", [
					(troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_lady),
					(troop_slot_ge, "$g_talk_troop", slot_troop_met, 2),
					(neg|troop_slot_eq, "$g_talk_troop", slot_troop_met, 4),
					(troop_get_slot, ":betrothed", "$g_talk_troop", slot_troop_betrothed),
					(gt, ":betrothed", -1),
					(neq, ":betrothed", "trp_player"),
					(str_store_troop_name, s5, ":betrothed"),
					(call_script, "script_troop_get_relation_with_troop", "$g_talk_troop", ":betrothed"),
					(lt, reg0, 0),
					(ge, "$g_talk_troop_relation", 10),
					],
    "I have sad news. I have become betrothed to {s5} -- against my will, I should say! Oh {playername} - I would so much rather be wed to you!", "lady_betrothed",[]],
[anyone,"lady_start", [
					(troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_lady),
					(troop_slot_ge, "$g_talk_troop", slot_troop_met, 2),
					(troop_get_slot, ":betrothed", "$g_talk_troop", slot_troop_betrothed),
					(gt, ":betrothed", -1),
					(neq, ":betrothed", "trp_player"),
					(str_store_troop_name, s5, ":betrothed"),
					],
    "Good {playername} -- I have become betrothed to {s5}. It is now no longer seemly for us to see each other like this.", "lady_betrothed",[
#	(try_begin),
#		(check_quest_active, "qst_visit_lady"),
#		(quest_slot_eq, "qst_visit_lady", slot_quest_giver_troop, "$g_talk_troop"),
#		(call_script, "script_end_quest", "qst_visit_lady"),
#	(try_end),
	]],
[anyone,"lady_start",
	[
	  (troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_lady),
	  (troop_slot_eq, "$g_talk_troop", slot_troop_met, 2),
	  (neg|troop_slot_eq, "$g_talk_troop", slot_troop_met, 4),
	  (neg|troop_slot_ge, "trp_player", slot_troop_spouse, active_npcs_begin),
	  (neg|troop_slot_ge, "$g_talk_troop", slot_troop_spouse, active_npcs_begin),

	  (gt, "$g_talk_troop_relation", 0),
	  (assign, "$romantic_rival", -1),

	  (try_for_range, ":rival_lord", lords_begin, lords_end),
	    (this_or_next|troop_slot_eq, ":rival_lord", slot_troop_love_interest_1, "$g_talk_troop"),
	    (this_or_next|troop_slot_eq, ":rival_lord", slot_troop_love_interest_2, "$g_talk_troop"),
	    (troop_slot_eq, ":rival_lord", slot_troop_love_interest_2, "$g_talk_troop"),
	    (call_script, "script_troop_get_relation_with_troop", "$g_talk_troop", ":rival_lord"),
	    (le, reg0, -4),

	    (this_or_next|troop_slot_eq, ":rival_lord", slot_lord_reputation_type, lrep_debauched),
	    (this_or_next|troop_slot_eq, ":rival_lord", slot_lord_reputation_type, lrep_quarrelsome),
	    (this_or_next|troop_slot_eq, ":rival_lord", slot_lord_reputation_type, lrep_roguish),
	    (troop_slot_eq, ":rival_lord", slot_lord_reputation_type, lrep_selfrighteous),

	    (assign, "$romantic_rival", ":rival_lord"),
	  (try_end),

	  (gt, "$romantic_rival", 0),
    ##diplomacy start+
	#check pronouns to support the possibility of female rivals
	(call_script, "script_dplmc_store_troop_is_female", "$romantic_rival"),
	],
	#Use reg3 below for "him" to "{reg0?her:him}", etc.
    "I must tell you -- there is another lord who has been paying me attentions, although I cannot abide {reg0?her:him}. I fear {reg0?she:he} has designs on me, and may try to force me to wed against my will.", "lady_other_suitor",[]],
[anyone,"lady_start", [ #friendly reminder that time is short
					(troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_lady),
					(lt, "$g_time_since_last_talk", 24),
					(troop_slot_eq, "$g_talk_troop", slot_troop_met, 2),
					(gt, "$g_talk_troop_relation", 0),
					(try_begin),
						(troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_adventurous),
						(str_store_string, s11, "str_i_do_enjoy_speaking_to_you_but_i_am_sure_you_understand_that_our_people_cluck_their_tongues_at_a_woman_to_spend_too_long_conversing_with_a_man_outside_her_family__although_the_heavens_know_its_never_the_man_who_is_held_to_blame_"),
					(else_try),
						(troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_ambitious),
						(str_store_string, s11, "str_as_much_as_i_enjoy_speaking_to_you_i_do_not_care_to_be_gossiped_about_by_others_who_might_lack_my_grace_and_beauty_"),
					(else_try),
						(troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_moralist),
						(str_store_string, s11, "str_i_do_so_enjoy_speaking_to_you_but_as_a_daughter_of_one_of_the_great_families_of_this_land_i_must_set_an_example_of_propriety_"),
					(else_try),
						(str_store_string, s11, "str_i_do_so_enjoy_speaking_to_you_but_as_a_daughter_of_good_family_i_must_protect_my_reputation_"),
					(try_end),
					],
   "{s11}It is probably not suitable for us to tarry too long here in conversation, but I would hope to see you again soon.", "lady_talk",[]],
[anyone,"lady_start", [ #unfriendly reminder that time is short
					(troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_lady),
					(lt, "$g_time_since_last_talk", 24),
					(troop_slot_eq, "$g_talk_troop", slot_troop_met, 2),
					(try_begin),
						(troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_adventurous),
						(str_store_string, s11, "str_although_it_is_kind_of_you_to_pay_me_such_attentions_i_suspect_that_you_might_find_other_ladies_who_may_be_more_inclined_to_return_your_affection"),
					(else_try),
						(troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_ambitious),
						(str_store_string, s11, "str_as_flattered_as_i_am_by_your_attentions_perhaps_you_should_seek_out_another_lady_of_somewhat_shall_we_say_different_tastes"),
					(else_try),
						(str_store_string, s11, "str_as_flattered_as_i_am_by_your_attentions_i_am_a_daughter_of_good_family_and_must_be_aware_of_my_reputation_it_is_not_seemly_that_i_converse_too_much_at_one_time_with_one_man_i_am_sure_you_understand_now_if_you_will_excuse_me"),
					(try_end),

					],
   "{s11}", "lady_talk",[]],
[anyone, "lady_start", [
	(eq, "$lady_flirtation_location", "$g_encountered_party"),
	(troop_slot_eq, "$g_talk_troop", slot_troop_met, 1),
	],  "I was planning to retire for a little while, but perhaps we may have a chance to speak more later...", "lady_talk", []],
[anyone,"lady_start", [
	(troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_lady),
	(troop_slot_eq, "$g_talk_troop", slot_troop_met, 2),
	(gt, "$g_talk_troop_relation", 0),
	(str_clear, s12),
	(try_begin),
		(troop_slot_eq, "$g_talk_troop", slot_troop_met, 2),
		(gt, "$g_talk_troop_relation", 0),
		(gt, "$g_time_since_last_talk", 24),
						(try_begin),
							(troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_otherworldly),
							(str_store_string, s12, "str_ah_my_gentle_playername_how_much_good_it_does_my_heart_to_see_you_again"),
						(else_try),
							(troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_adventurous),
							(str_store_string, s12, "str_playername__i_am_so_glad_to_see_you_again_i_must_say_i_do_envy_your_freedom_to_ride_out_and_experience_the_world"),
						(else_try),
							(troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_moralist),
							(str_store_string, s12, "str_playername__i_am_so_glad_to_see_you_i_trust_that_you_have_been_behaving_honorably_since_last_we_met"),
						(else_try),
							(troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_ambitious),
							(str_store_string, s12, "str_greetings_playername__it_is_good_to_see_you_i_hope_that_you_have_had_success_in_your_efforts_to_make_your_name_in_the_world"),
						(else_try),
							(str_store_string, s12, "str_playername__i_am_so_glad_that_you_were_able_to_come"),
						(try_end),
	(try_end),


	],"It is so delightful to have a chance to spend some time together.{s12}","lady_talk", []],
[anyone,"lady_start", [
		(troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_lady),
	],"What brings you here today?","lady_talk", []],
[anyone|plyr, "lady_proposal_pending", [],
    "No word so far...", "close_window",[]],
[anyone|plyr, "lady_proposal_pending", [],
    "On second thought, now is not the time for us to marry", "lady_proposal_pending_end",[]],
[anyone,"lady_proposal_pending_end", [
	(try_begin),
		(gt, "$g_talk_troop_effective_relation", 19),
		(str_store_string, s11, "str_very_well__i_will_let_you_choose_the_time"),
	(else_try),
		(str_store_string, s11, "str_good_i_am_glad_that_you_have_abandoned_the_notion_of_pushing_me_into_marriage_before_i_was_ready"),
	(try_end),
	],
    "{s11}", "close_window",[
	(call_script, "script_end_quest", "qst_formal_marriage_proposal"),
	]],
[anyone|plyr,"lady_betrothed", [],
    "Never! We must elope together at once!", "lady_suggest_elope",[]],
[anyone|plyr,"lady_betrothed", [
	(troop_slot_eq, "$g_talk_troop", slot_troop_betrothed, -1),
	(call_script, "script_get_kingdom_lady_social_determinants", "$g_talk_troop"),
	(call_script, "script_troop_get_family_relation_to_troop", reg0, "$g_talk_troop"),
	],
    "Perhaps I may still be able to change your {s11}'s mind", "lady_pretalk",[]],
[anyone|plyr,"lady_betrothed", [],
    "So be it -- let us then part", "lady_conclude_relationship",[
	]],
[anyone,"lady_suggest_elope", [(troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_conventional)],
    "Good {playername} -- you are a good and kind man, but a lady cannot defy her family. Such things are not done!", "lady_conclude_relationship",[]],
[anyone,"lady_suggest_elope",
    [
      (assign, "$romantic_rival", -1),
	  (try_for_range, ":possible_rival", lords_begin, lords_end),
	    (this_or_next|troop_slot_eq, ":possible_rival", slot_troop_love_interest_1, "$g_talk_troop"),
	    (this_or_next|troop_slot_eq, ":possible_rival", slot_troop_love_interest_2, "$g_talk_troop"),
	    (troop_slot_eq, ":possible_rival", slot_troop_love_interest_2, "$g_talk_troop"),
	    (call_script, "script_troop_get_relation_with_troop", "$g_talk_troop", ":possible_rival"),

	    (try_begin),
	      (eq, "$cheat_mode", 1),
	      (str_store_troop_name, s4, ":possible_rival"),
	      (display_message, "str_rival_found_s4_reg0_relation"),
		(try_end),
		(gt, reg0, "$g_talk_troop_relation"),
		(assign, "$romantic_rival", ":possible_rival"),
      (try_end),

      (gt, "$romantic_rival", -1),
    ],
	##diplomacy start+ change "gentlemen" to "{gentlemen/suitors}", and Sir to {sir/madam}
    "{Sir/Madame} -- as you may know, I have been entertaining offers from a number of {gentlemen/suitors} such as yourself. I am not yet at a stage where I can commit to any of them.", "lady_other_suitor",
	##diplomacy end+
	[
    ]],
[anyone,"lady_suggest_elope", [
	(troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_ambitious),
	(neg|troop_slot_ge, "trp_player", slot_troop_renown, 350)
	],
    "Ah {playername}, you must realize. You are still finding your way in the world. I have great affection for you, {playername}, but I will not consign myself to obscurity.", "lady_conclude_relationship",[]],
[anyone,"lady_suggest_elope", [
	(troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_moralist),
	(lt, "$player_honor", 20)
	],
	##diplomacy start+
	#Replace "my husband" with "my betrothed", as the former doesn't make sense (the gender-neutrality of the replacement is a bonus)
	#Also replace "I bare little affection" with "I bear little affection"
    "Ah {playername}, although you are kind to me, I am not certain enough of your moral fiber to risk such a thing. Although I bear little affection for my betrothed, it would be a weighty thing to go against my family's wishes, and I am not certain enough of you to take that step.", "lady_conclude_relationship",[]],
[anyone,"lady_suggest_elope", [(le, "$g_talk_troop_effective_relation", 20),],
    "Good {playername} -- to elope would be to throw away my ties with my family, which are everything to me! I have a considerable affection for you, but I am not sure that I am prepared to risk that.", "lady_conclude_relationship",[]],
[anyone,"lady_suggest_elope", [
	(assign, "$home_for_spouse", -1),
	(try_for_range, ":player_center", centers_begin, centers_end),
		(eq, "$home_for_spouse", -1),
		(party_slot_eq, ":player_center", slot_town_lord, "trp_player"),
		(is_between, ":player_center", walled_centers_begin, walled_centers_end),
#		(this_or_next|is_between, ":player_center", walled_centers_begin, walled_centers_end),
#			(party_slot_eq, ":player_center", slot_center_has_manor, 1),
		(assign, "$home_for_spouse", ":player_center"),
	(try_end),
	(eq, "$home_for_spouse", -1),
	##diplomacy start+ Allow the possibility of male versions of the lines
	],
	#Replace "wife" with "{reg65?wife:husband}" and "mistress" with "{reg65?mistress:keeper}"
    "Good {playername} -- I am not used to the hardships of campaigning as you are. I want a home to call my own. If you were lord of a castle or town with a great hall, I would gladly go there as your {reg0?wife:husband}, to be {reg0?mistress:keeper} of the household. But I do not wish to live like a hunted animal.", "lady_conclude_relationship",[]],
[anyone,"lady_suggest_elope", [
	(call_script, "script_get_kingdom_lady_social_determinants", "$g_talk_troop"),
	(call_script, "script_troop_get_family_relation_to_troop", reg0, "$g_talk_troop"),
	##diplomacy start+
	#Use correct pronouns for female guardians
	],
	#change "he" to "{reg4?she:he}", and "his" to "{reg4?her:his}"
    "Elope with you? Yes -- we could do that. It is a great step to defy my family -- but a loveless marriage, and life without you, might be a far worse thing! But be warned -- this will be a terrible blow to my {s11}'s prestige, and {reg4?she:he} will do everything in {reg4?her:his} power to bring you down.", "lady_elope_agree",[]],
[anyone|plyr,"lady_elope_agree", [],
    "Quickly, then! There is no time to lose.", "lady_elope_agree_nurse",[
	]],
[anyone|plyr,"lady_elope_agree", [],##diplomacy start+ change "his" to {reg4?her:his}
    "Everything in {reg4?her:his} power, you say? Em... Let me think about this...", "close_window",[
	##diplomacy end+
	]],
[anyone, "lady_elope_agree_nurse", [],
    "Your lordship... Your ladyship... Would you like me to witness your exchange of vows?", "lady_elope_agree_lady_vows",[
    (set_conversation_speaker_troop, trp_nurse_for_lady),
	]],
[anyone, "lady_elope_agree_lady_vows", [
	(str_store_troop_name, s4, "$g_talk_troop"),
	],##diplomacy start+ allow both genders, change "husband" to "{husband/wife}"
    "Yes, do that. For my part, I make the following vow: I, {s4}, do swear that I accept {playername} as my {husband/wife}, according to the ancient law and custom of our land...", "lady_elope_agree_nurse_2",[
	]],
[anyone, "lady_elope_agree_nurse_2", [
	##diplomacy start+ Allow the possibility of male versions of the lines
	],
	#change "wife" to "{reg65?wife:husband}"
    "Very good. Do you, {playername}, swear similarly to accept {s4} as your {reg65?wife:husband}?", "lady_elope_agree_player_vows",[
    (set_conversation_speaker_troop, trp_nurse_for_lady),
	]],
[anyone|plyr,"lady_elope_agree_player_vows", [],
    "I do.", "close_window",[
	(call_script, "script_courtship_event_bride_marry_groom", "$g_talk_troop", "trp_player", 1), #1 is elopement
	]],
[anyone|plyr,"lady_elope_agree_player_vows", [],
    "Eh, what? This is all moving too fast...", "close_window",[
	]],
[anyone|plyr,"lady_elope_agree", [
	##diplomacy start+ Allow the possibility of male versions of the lines
	],
	#replaced "lady" with "{reg65?lady:young lad}" and "her" with "{reg65?her:his}"
    "Oh, really? My dear -- I could never separate a {reg65?lady:young lad} from {reg65?her:his} family like that...", "lady_conclude_relationship",[
	##diplomacy end+
	]],
[anyone,"lady_conclude_relationship", [],
	"So I suppose our time together must come to an end...", "lady_conclude_relationship_confirm", []],
[anyone|plyr,"lady_conclude_relationship_confirm", [],
	"Yes -- it must be...", "lady_conclude_relationship_confirm_yes", []],
[anyone|plyr,"lady_conclude_relationship_confirm", [],
	"Wait -- perhaps there is still a chance for us!", "lady_conclude_relationship_confirm_no", []],
[anyone,"lady_conclude_relationship_confirm_yes", [],
	"Farewell, {playername}. We will see each other, in the palaces and castles of this land, but we must keep our distance from each other. I will remember these days fondly, nonetheless.", "close_window", [
	(troop_set_slot, "$g_talk_troop", slot_troop_met, 4),
	]],
[anyone,"lady_conclude_relationship_confirm_no", [],
	"In that case, we shall see what the future brings.", "close_window", [
	]],
[anyone|plyr,"lady_generic_mission_succeeded", [], "Always an honour to serve, {s65}.", "lady_pretalk",[]],
[anyone|plyr ,"lady_premeet", [],  "I am {playername}.", "lady_meet", []],
[anyone|plyr ,"lady_premeet", [],  "My name is {playername}. At your service.", "lady_meet", []],
[anyone, "lady_meet", [
  (troop_slot_ge, "trp_player", slot_troop_renown, 200),
  ],  "Of course. How splendid to finally make your acquaintance.", "lady_meet_end", []],
[anyone, "lady_meet", [],  "{playername}? I do not believe I've heard of you before.", "lady_meet_end", []],
[anyone, "lady_meet_end", [
	(eq, "$lady_flirtation_location", "$g_encountered_party"),
  ],  "I am about to retire for a little while, but perhaps we may have a chance to speak more later...", "lady_talk", []],
[anyone, "lady_meet_end", [
    (troop_slot_eq, "$g_talk_troop", slot_troop_spouse, -1),
	(call_script, "script_troop_get_romantic_chemistry_with_troop", "$g_talk_troop", "trp_player"),
	(le, reg0, 0),
	(call_script, "script_troop_get_relation_with_troop", "$g_talk_troop", "trp_player"),
	(le, reg0, 0),
	],  "Now, if you will excuse me...", "lady_talk", []],
[anyone, "lady_meet_end", [],  "Can I help you with anything?", "lady_talk", []],
[anyone|plyr,"lady_talk", [(neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
							 (ge, "$g_encountered_party_relation", 0),
  ],
   "I want to know the location of someone.", "lord_talk_ask_location",[]],
[anyone,"lady_pretalk", [
    (troop_slot_eq, "$g_talk_troop", slot_troop_spouse, -1),
	(call_script, "script_troop_get_romantic_chemistry_with_troop", "$g_talk_troop", "trp_player"),
	(le, reg0, 0),
	(call_script, "script_troop_get_relation_with_troop", "$g_talk_troop", "trp_player"),
	(le, reg0, 0),
], "Now, if you will excuse me...", "lady_talk",[]],
[anyone,"lady_pretalk", [], "Is there anything else?", "lady_talk",[]],
[anyone|plyr,"lady_talk",
   [(neg|eq, "$g_talk_troop_met", 0),],
   "I wished to ask about one of your relatives.", "dplmc_lady_relations2",[]],
[anyone|plyr, "lady_talk", [(neg|eq, "$g_talk_troop_met", 0),],
   "Do you know of any ongoing feasts?",
   "dplmc_lady_feasts", []],
[anyone|plyr,"lady_talk",
   ##diplomacy start+
   #[],#Don't show this option after the first meeting.  There's a separate "ask about relatives instead".
   [(eq, "$g_talk_troop_met", 0),
   ],
   #change "my lady" to "{reg0?my lady:good sir}"
   "May I have the honor of knowing more about you, {reg65?my lady:good sir}?", "lady_relations",[]],
[anyone,"lady_relations",
   [
    (str_store_string, s12, "str_i_am"),
	(assign, ":relation_found", 0),
	(assign, ":in_castle_of_relative", 0),

    (try_for_range, ":lord", active_npcs_begin, kingdom_ladies_end), #use this as the basis for "troop_describe_relation_with_troop"
		(call_script, "script_troop_get_family_relation_to_troop", "$g_talk_troop", ":lord"), #The normal order is reversed, because the lady is describing herself
		(this_or_next|gt, reg0, 5),
			(party_slot_eq, "$g_encountered_party", slot_town_lord, ":lord"),
		(gt, reg0, 0),

		(str_store_troop_name, s14, ":lord"),
		(try_begin),
			(eq, ":relation_found", 1),
			(str_store_string, s12, "str_s12"),
		(try_end),
		(str_store_string, s12, "str_s12_s11_to_s14"),
		(assign, ":relation_found", 1),

		(try_begin),
			(party_slot_eq, "$g_encountered_party", slot_town_lord, ":lord"),
			(assign, ":in_castle_of_relative", 1),
		(try_end),
    (try_end),

	(try_begin),
		(eq, ":in_castle_of_relative", 1),
		(str_store_string, s12, "str_s12"),
	(else_try),
		(eq, ":in_castle_of_relative", 0),
		(faction_slot_eq, "$g_talk_troop_faction", slot_faction_ai_state, sfai_feast),
		(faction_slot_eq, "$g_talk_troop_faction", slot_faction_ai_object, "$g_encountered_party"),
		(str_store_string, s12, "str_s12_i_am_here_for_the_feast"),
	(else_try),
		(str_store_string, s12, "str_s12"),
	(try_end),
	
	##gekokujo 3.0 debug start
	#(try_begin),
	#    (troop_slot_eq, "$g_talk_troop", slot_troop_spouse, -1),
	#	(str_store_string, s12, "@{s12} I am not married."),
	#(else_try),
	#	(str_store_string, s12, "@{s12} I am married."),
	#(try_end),
	
	#(try_begin),
	#    (troop_slot_eq, "$g_talk_troop", slot_troop_betrothed, -1),
	#	(str_store_string, s12, "@{s12} I am not bethrothed."),
	#(else_try),
	#	(str_store_string, s12, "@{s12} I am bethrothed."),
	#(try_end),
	
	#(troop_get_slot, ":spouse", "$g_talk_troop", slot_troop_spouse),
	#(str_store_troop_name, s30, ":spouse"),
	#(str_store_string, s12, "@{s12} My spouse is {s30}."),
	
	#(troop_get_slot, ":father", "$g_talk_troop", slot_troop_father),
	#(str_store_troop_name, s30, ":father"),
	#(str_store_string, s12, "@{s12} My father is {s30}."),
	
	#(troop_get_slot, ":guardian", "$g_talk_troop", slot_troop_guardian),
	#(str_store_troop_name, s30, ":guardian"),
	#(str_store_string, s12, "@{s12} My guardian is {s30}."),
	
	#(call_script, "script_get_kingdom_lady_social_determinants", "$g_talk_troop"),
	#(str_store_troop_name, s30, reg0),
	#(str_store_string, s12, "@{s12} My closest male relative is {s30}."),
	##gekokujo 3.0 debug end

   ],
   "{s12}", "lady_pretalk",[
   #diplomacy start+
       (assign, "$g_talk_troop_met", 1),
       ]],
[anyone|plyr,"lady_talk",
   [
    ##diplomacy start+
    #(troop_get_type, ":is_female", "trp_player"),#dplmc+ removed
	#(eq, ":is_female", 0), #dplmc+ removed

	(this_or_next|neq, reg65, "$character_gender"),
		(ge, "$g_disable_condescending_comments", 2),
	##diplomacy end+
    (troop_slot_eq, "$g_talk_troop", slot_troop_met, 1),
	(troop_slot_eq, "$g_talk_troop", slot_troop_spouse, -1),
    (neg|troop_slot_ge, "trp_player", slot_troop_spouse, active_npcs_begin),

	(neq, "$lady_flirtation_location", "$g_encountered_party"),
	##diplomacy start+
	#Ensure gender of addressed is correct (unnecessary in Native, but may be in mods)
	],
   "My {reg65?lady:lord}, I would like to profess myself your most ardent admirer", "lady_profess_admiration",#Changed "lady" to "{reg0?lady:lord}"
   ##diplomacy end+
	[
	(call_script, "script_troop_get_romantic_chemistry_with_troop", "$g_talk_troop", "trp_player"),
	(assign, ":reaction_change", reg0),

#	(try_begin),
#		(gt, "$g_player_tournament_placement", 3),
#		(val_sub, "$g_player_tournament_placement", 3),
#		(val_mul, "$g_player_tournament_placement", 4), #Twice normal, but is divided by two
#	(else_try),
#		(assign, "$g_player_tournament_placement", 0),
#	(try_end),

#	(try_begin),
#		(troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_conventional),
#		(val_mul, "$g_player_tournament_placement", 2),
#	(else_try),
#		(troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_moralist),
#		(val_div, "$g_player_tournament_placement", 2),
#	(try_end),

#	(val_add, ":reaction_change", "$g_player_tournament_placement"),
#	(assign, "$g_player_tournament_placement", 0),

	(val_div, ":reaction_change", 2),
	(val_max, ":reaction_change", -2),

	(call_script, "script_troop_change_relation_with_troop", "$g_talk_troop", "trp_player", ":reaction_change"),
	(assign, "$g_time_to_spare", 0),

	]],
[anyone|plyr,"lady_talk",
   [
    ##diplomacy start+
    #(troop_get_type, ":is_female", "trp_player"),
	(this_or_next|ge, "$g_disable_condescending_comments", 2),#dplmc+ added
	(neq, reg65, "$character_gender"),
	(gt, "$g_player_tournament_placement", 3),

    #Allow players to dedicate tournament victories even after marriage, though it may irritate the player's spouse
	#(neg|troop_slot_ge, "trp_player", slot_troop_spouse, active_npcs_begin),
	],
	#Ensure gender of addressed is correct (unnecessary in Native, but may be in mods)
   "My {reg65?lady:lord}, I would like to dedicate my successes in this recent tournament to you", "lady_tournament_dedication_reaction",#Changed "lady" to "{reg0?lady:lord}"
	[
	##diplomacy end+

	(try_begin),
		(gt, "$g_player_tournament_placement", 3),
		(val_sub, "$g_player_tournament_placement", 3),
		(val_mul, "$g_player_tournament_placement", 2),
	(else_try),
		(assign, "$g_player_tournament_placement", 0),
	(try_end),

    ##diplomacy start+
    #If the player has a spouse, a dedication to someone else may irritate them.
    (try_begin),
        (neg|troop_slot_eq, "trp_player", slot_troop_spouse, -1),

		(try_for_range, ":spouse", heroes_begin, heroes_end),#<- Iterate because of the possibility of polygamy
			(neg|troop_slot_eq, ":spouse", slot_troop_occupation, dplmc_slto_dead),
			(neq, ":spouse", "$g_talk_troop"),
			(this_or_next|troop_slot_eq, "trp_player", slot_troop_spouse, ":spouse"),
			(this_or_next|troop_slot_eq, ":spouse", slot_troop_spouse, "trp_player"),
				(troop_slot_eq, "trp_player", slot_troop_betrothed, ":spouse"),
			(call_script, "script_troop_change_relation_with_troop", ":spouse", "trp_player", -1),
		(try_end),
    (try_end),
    ##diplomacy end+

	(try_begin),
		(troop_slot_eq, "$g_talk_troop", slot_lady_used_tournament, 1),
		(val_div, "$g_player_tournament_placement", 3),
		(str_store_string, s9, "str_another_tournament_dedication_oh_i_suppose_it_is_always_flattering"),
	(else_try),
		(troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_conventional),
		(val_mul, "$g_player_tournament_placement", 2),
		(str_store_string, s9, "str_do_you_why_what_a_most_gallant_thing_to_say"),
	(else_try),
		(troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_moralist),
		(val_div, "$g_player_tournament_placement", 2),
		(str_store_string, s9, "str_hmm_i_cannot_say_that_i_altogether_approve_of_such_frivolity_but_i_must_confess_myself_a_bit_flattered"),
	(else_try),
		(str_store_string, s9, "str_why_thank_you_you_are_most_kind_to_do_so"),
	(try_end),

	(call_script, "script_troop_change_relation_with_troop", "$g_talk_troop", "trp_player", "$g_player_tournament_placement"),
	(assign, "$g_player_tournament_placement", 0),
	(troop_set_slot, "$g_talk_troop", slot_lady_used_tournament, 1),
	]],
[anyone,"lady_tournament_dedication_reaction", [],
   "{s9}", "lady_pretalk",
   []],
[anyone,"lady_profess_admiration", [
	(call_script, "script_troop_get_relation_with_troop", "$g_talk_troop", "trp_player"),
    (gt, reg0, 0),

	(try_begin),
		(troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_moralist),
		(str_store_string, s11, "str_you_are_most_courteous_and_courtesy_is_a_fine_virtue_"),
	(else_try),
		(troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_ambitious),
		(str_store_string, s11, "str_hmm_youre_a_bold_one_but_i_like_that_"),
	(else_try),
		(troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_adventurous),
		(str_store_string, s11, "str_ah_well_they_all_say_that_but_no_matter_a_compliment_well_delivered_is_at_least_a_good_start_"),
	(else_try),
		(troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_otherworldly),
		(str_store_string, s11, "str_oh_do_you_mean_that_such_a_kind_thing_to_say"),
	(else_try),
		(str_store_string, s11, "str_you_are_a_most_gallant_young_man_"),
	(try_end),

  ],
   "{s11}I would like it very much if we could see more of each other.", "close_window",
   [(troop_set_slot, "$g_talk_troop", slot_troop_met, 2),
	(assign, "$lady_flirtation_location", "$g_encountered_party"),
   ]],
[anyone,"lady_profess_admiration", [
  ],
   "Ah... You are too kind... My, the hour is getting rather late, isn't it? I really must be going.", "lady_pretalk",
   [(troop_set_slot, "$g_talk_troop", slot_troop_met, 2),
   ]],
[anyone|plyr,"lady_talk",
   [
	 (troop_slot_eq, "$g_talk_troop", slot_troop_met, 2),
	 (eq, "$g_time_to_spare", 1),
	 (eq, "$talk_context", tc_courtship),
     ],
	 ##diplomacy start+ "my lady" -> "my {reg65?lady:lord}"
   "Do you like poetry, my {reg65?lady:lord}?", "lady_recite_poetry",[
   ##diplomacy end+
	 (assign, "$g_time_to_spare", 0),
   ]],
[anyone,"lady_recite_poetry", [
  ],
   "That would depend on the poem. Did you intend to recite a verse?", "lady_recite_poetry",
   []],
[anyone|plyr,"lady_recite_poetry",
   [
	 (gt, "$tragic_poem_recitations", 0),
	 (troop_slot_eq, "$g_talk_troop", slot_lady_courtship_tragic_recited, 0),

     ],
   "The wind that blows the dry road's dust...", "lady_recite_poetry_response",[
   (assign, "$poem_selected", courtship_poem_tragic),
   (troop_set_slot, "$g_talk_troop", slot_lady_courtship_tragic_recited, 1),

   ]],
[anyone|plyr,"lady_recite_poetry",
   [
	 (gt, "$comic_poem_recitations", 0),
	 (troop_slot_eq, "$g_talk_troop", slot_lady_courtship_comic_recited, 0),

     ],
   "All the silks of China/All the furs of the Jurchen...", "lady_recite_poetry_response",[
   (assign, "$poem_selected", courtship_poem_comic),
   (troop_set_slot, "$g_talk_troop", slot_lady_courtship_comic_recited, 1),

   ]],
[anyone|plyr,"lady_recite_poetry",
   [
	(gt, "$mystic_poem_recitations", 0),
	(troop_slot_eq, "$g_talk_troop", slot_lady_courtship_mystic_recited, 0),

    ],
   "You are the first and the last/the outer and the inner...", "lady_recite_poetry_response",[
   (assign, "$poem_selected", courtship_poem_mystic),
   (troop_set_slot, "$g_talk_troop", slot_lady_courtship_mystic_recited, 1),

   ]],
[anyone|plyr,"lady_recite_poetry",
   [
	(gt, "$heroic_poem_recitations", 0),
	(troop_slot_eq, "$g_talk_troop", slot_lady_courtship_heroic_recited, 0),
     ],
   "A light pierced the gloom over Kyushu's cliffs...", "lady_recite_poetry_response",[
    (assign, "$poem_selected", courtship_poem_heroic),
	(troop_set_slot, "$g_talk_troop", slot_lady_courtship_heroic_recited, 1),

   ]],
[anyone|plyr,"lady_recite_poetry",
   [
	(gt, "$allegoric_poem_recitations", 0),
	(troop_slot_eq, "$g_talk_troop", slot_lady_courtship_allegoric_recited, 0),

     ],
   "I deflected her skeptical questioning darts/with armor made of purest devotion...", "lady_recite_poetry_response",[
    (assign, "$poem_selected", courtship_poem_allegoric),
	(troop_set_slot, "$g_talk_troop", slot_lady_courtship_allegoric_recited, 1),
   ]],
[anyone|plyr,"lady_recite_poetry",
   [],"Actually, I can't think of any that I would care to recite...", "lady_pretalk",[]],
[anyone,"lady_recite_poetry_response",
   [
    (call_script, "script_courtship_poem_reactions", "$g_talk_troop", "$poem_selected"),
   ],
   "{s11}", "lady_private_conversation_end",[
    (assign, ":reaction", reg0),
	(call_script, "script_troop_change_relation_with_troop", "$g_talk_troop", "trp_player", ":reaction"),
    (call_script, "script_courtship_poem_reactions", "$g_talk_troop", "$poem_selected"), #this needs to be twice, as the above resets s11
   ]],
[anyone,"lady_private_conversation_end",
	[
	(str_clear, s11),
	(try_begin),
		(call_script, "script_troop_get_relation_with_troop", "$g_talk_troop", "trp_player"),
		(gt, reg0, 0),
		(str_store_string, s11, "str__do_come_and_see_me_again_soon"),
	(try_end),
	],
	"Time is passing quickly, and we cannot linger here too long.", "lady_pretalk",
	[
	(assign, "$g_time_to_spare", 0),
	]],
[anyone|plyr,"lady_talk",
    [
	(neg|check_quest_active, "qst_formal_marriage_proposal"),
	(neg|troop_slot_ge, "trp_player", slot_troop_betrothed, active_npcs_begin),
	(neg|troop_slot_ge, "trp_player", slot_troop_spouse, active_npcs_begin),


	(troop_slot_eq, "$g_talk_troop", slot_troop_met, 2),
	(eq, "$talk_context", tc_courtship),
	##diplomacy start+ Allow the possibility of male versions of the lines
    ],
	#replace "my lady" with "{reg0?my lady:kind sir}"
    "Do you think that we may have a future together, {reg65?my lady:kind sir}?", "lady_marriage_discussion",[
	##diplomacy end+
    ]],
[anyone,"lady_marriage_discussion",
    [
	(assign, "$romantic_rival", -1),
	(try_for_range, ":possible_rival", lords_begin, lords_end),
		(this_or_next|troop_slot_eq, ":possible_rival", slot_troop_love_interest_1, "$g_talk_troop"),
		(this_or_next|troop_slot_eq, ":possible_rival", slot_troop_love_interest_2, "$g_talk_troop"),
			(troop_slot_eq, ":possible_rival", slot_troop_love_interest_2, "$g_talk_troop"),
		(call_script, "script_troop_get_relation_with_troop", "$g_talk_troop", ":possible_rival"),

		(try_begin),
			(eq, "$cheat_mode", 1),
			(str_store_troop_name, s4, ":possible_rival"),
			(display_message, "str_rival_found_s4_reg0_relation"),
		(try_end),
		(gt, reg0, "$g_talk_troop_relation"),
		(assign, "$romantic_rival", ":possible_rival"),
	(try_end),
	(gt, "$romantic_rival", -1),
	##diplomacy start+ Give gender equivalents
    ],#"Sir" to "{Sir/Madame}", and "gentlemen" to "{gentlemen/suitors}"
    "{Sir/Madame} -- as you may know, I have been entertaining offers from a number of {gentlemen/suitors} such as yourself. I am not yet at a stage where I can commit to any of them.", "lady_other_suitor",[
    ]],
[anyone,"lady_marriage_discussion",
    [
    (troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_ambitious),
	(neg|troop_slot_ge, "trp_player", slot_troop_renown, 350),
	],
    "It is good to hear that you are thinking seriously about the future. However, I would like to see you rise a little further in the world before I am ready to commit to marry you.", "lady_proposal_refused",[
    ]],
[anyone,"lady_marriage_discussion",
    [
    (troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_moralist),
	(lt, "$player_honor", 10)
	],
    "It is good to hear that your intentions are honorable. However, I have resolved only to marry a man of the strongest moral fiber. I would like you to prove yourself more in that regard.", "lady_proposal_refused",[
    ]],
[anyone,"lady_marriage_discussion",
    [
	(lt, "$g_talk_troop_relation", 20),
    ],
    "Sir -- it is comforting to hear that your intentions towards me are honorable. But perhaps we should take the time to get to allow our affections for each other to grow a little stronger, before making any such decision.", "lady_proposal_refused",[
    ]],
[anyone,"lady_marriage_discussion",
    [
	(call_script, "script_get_kingdom_lady_social_determinants", "$g_talk_troop"),
	(assign, ":guardian", reg0),
	(troop_slot_eq, ":guardian", slot_lord_granted_courtship_permission, -1),
	(str_store_troop_name, s4, reg0),
	(call_script, "script_troop_get_family_relation_to_troop", ":guardian", "$g_talk_troop"),
	],
    "Oh {playername}, how happy that would make me! But my {s11} {s4} would never allow it... Perhaps it is best that we part...", "lady_betrothed", []],
[anyone,"lady_marriage_discussion",
    [
	(call_script, "script_get_kingdom_lady_social_determinants", "$g_talk_troop"),
	(assign, ":guardian", reg0),
	(call_script, "script_troop_get_family_relation_to_troop", ":guardian", "$g_talk_troop"),
	(str_store_troop_name, s4, ":guardian"),

	],
    "Oh {playername}, how happy that would make me! Go ask my {s11} {s4} for permission!", "close_window",[
	(call_script, "script_get_kingdom_lady_social_determinants", "$g_talk_troop"),
	(assign, ":guardian", reg0),
	(str_store_troop_name, s12, ":guardian"),
	(str_store_troop_name, s15, "$g_talk_troop"),
    (setup_quest_text, "qst_formal_marriage_proposal"),
    (str_store_string, s2, "str_you_intend_to_ask_s12_for_permission_to_marry_s15"),

    (quest_set_slot, "qst_formal_marriage_proposal", slot_quest_target_troop, ":guardian"),
    (quest_set_slot, "qst_formal_marriage_proposal", slot_quest_expiration_days, 30),
    (quest_set_slot, "qst_formal_marriage_proposal", slot_quest_current_state, 0),
	(call_script, "script_start_quest", "qst_formal_marriage_proposal", "$g_talk_troop"),
	(quest_set_slot, "qst_formal_marriage_proposal", slot_quest_giver_troop, "$g_talk_troop"),

	#Repeated to ensure strings work correctly
	(call_script, "script_troop_get_family_relation_to_troop", ":guardian", "$g_talk_troop"),
	(str_store_troop_name, s4, ":guardian"),
    ]],
[anyone|plyr,"lady_proposal_refused",
    [
	(is_between, "$g_talk_troop_relation", 12, 20),
    (this_or_next|neg|troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_ambitious),
		(troop_slot_ge, "trp_player", slot_troop_renown, 350),
    (this_or_next|neg|troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_moralist),
		(ge, "$player_honor", 10),
	],
    "Perhaps I can persuade you to delay no further.", "lady_proposal_refused_persuade_check",[
    ]],
[anyone,"lady_proposal_refused_persuade_check",
    [
	],
    "What do you have to say?", "lady_proposal_refused_persuade_player_response",[

	(assign, reg4, 20),
	(call_script, "script_troop_get_relation_with_troop", "$g_talk_troop", "trp_player"),
	(assign, ":cur_relation", reg0),
	(assign, reg5, ":cur_relation"),
	(assign, reg9, 1),
    (store_skill_level, ":persuasion_level", "skl_persuasion", "trp_player"),
	(store_sub, ":difference", 20, ":cur_relation"),
	(val_mul, ":persuasion_level", 2),
	(try_begin),
		(gt, ":difference", ":persuasion_level"),
		(assign, "$g_persuasion_failure_chance", 100),
	(else_try),
		(store_mul, "$g_persuasion_failure_chance", ":difference", 100),
		(val_div, "$g_persuasion_failure_chance", ":persuasion_level"),
	(try_end),
	(assign, reg8, "$g_persuasion_failure_chance"),
	(store_sub, reg7, 100, "$g_persuasion_failure_chance"),
	(dialog_box, "str_persuasion_opportunity"),

    ]],
[anyone|plyr,"lady_proposal_refused_persuade_player_response",
    [
	##diplomacy start+ Allow the possibility of male versions of the lines
	], #Replace "lady" with "{reg0?lady:lord}"
    "Love is as a rose, my {reg65?lady:lord}. Left unplucked, it may wither.", "lady_proposal_refused_persuade_result",[
    ]],
[anyone|plyr,"lady_proposal_refused_persuade_player_response",
    [],
    "Oh, never mind.", "lady_pretalk",
    []],
[anyone,"lady_proposal_refused_persuade_result",
    [
	(store_random_in_range, ":random", 0, 100),
	(lt, ":random", "$g_persuasion_failure_chance"),
	],##diplomacy start+ change "sir" to "{sir/madame}"
    "Enough, {sir/madame}! I shall not be rushed into marriage, with you or with anyone else! You have made me very cross. Please, leave me alone for a while. I shall let you know when I am ready to speak to you again.", "close_window", [##diplomacy end+
	(call_script, "script_troop_change_relation_with_troop", "$g_talk_troop", "trp_player", -1),
	(jump_to_menu, "mnu_town"),
	(finish_mission),
	]],
[anyone,"lady_proposal_refused_persuade_result",
    [
	(call_script, "script_get_kingdom_lady_social_determinants", "$g_talk_troop"),
	(assign, ":guardian", reg0),
	(troop_slot_eq, ":guardian", slot_lord_granted_courtship_permission, -1),
	(str_store_troop_name, s4, reg0),
	(call_script, "script_troop_get_family_relation_to_troop", ":guardian", "$g_talk_troop"),
	##diplomacy start+ Use correct pronouns for female guardians
	],#Change "his" to "{reg4?her:his}"
    "Oh {playername}, I could never allow that to happen! Oh, if only we could be wed! But my {s11} {s4} would never give {reg4?her:his} permission... Perhaps it is best that we part...", "lady_betrothed", [
	##diplomacy end+
	(call_script, "script_troop_change_relation_with_troop", "$g_talk_troop", "trp_player", 5),
	]],
[anyone,"lady_proposal_refused_persuade_result",
    [
	(call_script, "script_get_kingdom_lady_social_determinants", "$g_talk_troop"),
	(assign, ":guardian", reg0),
	(call_script, "script_troop_get_family_relation_to_troop", ":guardian", "$g_talk_troop"),
	(str_store_troop_name, s4, ":guardian"),
	##diplomacy start+ Use correct pronouns for female guardians
	],#Change "his" to "{reg4?her:his}"
    "Oh {playername}, I could never allow that to happen! Go ask my {s11} {s4} {reg4?her:his} permission for us to be wed!", "close_window",[
	##diplomacy end+

	(call_script, "script_troop_change_relation_with_troop", "$g_talk_troop", "trp_player", 5),
	(call_script, "script_get_kingdom_lady_social_determinants", "$g_talk_troop"),
	(assign, ":guardian", reg0),
	(str_store_troop_name, s12, ":guardian"),
	(str_store_troop_name, s15, "$g_talk_troop"),
    (setup_quest_text, "qst_formal_marriage_proposal"),
    (str_store_string, s2, "str_you_intend_to_ask_s12_for_permission_to_marry_s15"),

    (quest_set_slot, "qst_formal_marriage_proposal", slot_quest_target_troop, ":guardian"),
    (quest_set_slot, "qst_formal_marriage_proposal", slot_quest_expiration_days, 30),
    (quest_set_slot, "qst_formal_marriage_proposal", slot_quest_current_state, 0),
	(call_script, "script_start_quest", "qst_formal_marriage_proposal", "$g_talk_troop"),
	(quest_set_slot, "qst_formal_marriage_proposal", slot_quest_giver_troop, "$g_talk_troop"),
    ]],
[anyone|plyr,"lady_proposal_refused",
    [],
    "Very well -- I shall continue to strive to be worthy of your esteem!", "close_window",[
    ]],
[anyone|plyr,"lady_proposal_refused",
    [
	##diplomacy start+
	#Enable this if "enhanced prejudice" mode is active.
    (this_or_next|ge, "$cheat_mode", 1),
	(lt, "$g_disable_condescending_comments", 0),
	##(eq, 1, 0),
	##diplomacy end+
	(neg|check_quest_active, "qst_formal_marriage_proposal"),
	],
    "I am tired of these games! I will speak to your family about arranging a wedding immediately..", "lady_player_threatens_compel",[
    ]],
[anyone,"lady_player_threatens_compel",
    [],
    "What? Do you mean that?", "lady_player_threatens_compel_2",[
    ]],
[anyone|plyr,"lady_player_threatens_compel_2",
    [],
    "No, of couse not. Please forgive my burst of temper", "lady_private_conversation_end",[
    ]],
[anyone|plyr,"lady_player_threatens_compel_2",
    [],
    "Yes -- you clearly do not know what is in your best interests.", "close_window",[
	(call_script, "script_get_kingdom_lady_social_determinants", "$g_talk_troop"),
	(assign, ":guardian", reg0),
	(str_store_troop_name, s10, "$g_talk_troop"),
	(str_store_troop_name, s12, ":guardian"),
    (setup_quest_text, "qst_formal_marriage_proposal"),
    (str_store_string, s2, "str_you_intend_to_ask_s12_to_pressure_s10_to_marry_you"),

    (quest_set_slot, "qst_formal_marriage_proposal", slot_quest_target_troop, ":guardian"),
    (quest_set_slot, "qst_formal_marriage_proposal", slot_quest_expiration_days, 30),
    (quest_set_slot, "qst_formal_marriage_proposal", slot_quest_current_state, 0),
	(call_script, "script_start_quest", "qst_formal_marriage_proposal", "$g_talk_troop"),
	(quest_set_slot, "qst_formal_marriage_proposal", slot_quest_giver_troop, "$g_talk_troop"),
    ]],
[anyone|plyr,"lady_other_suitor",
    [],
    ##diplomacy start+
    #change "my lady" to "my {reg65?lady:lord}"
	"It grieves me to hear that, my {reg65?lady:lord}, but such things must be", "lady_pretalk",
	##diplomacy end+
	[]],
[anyone|plyr,"lady_other_suitor",
	[],
	##diplomacy start+ his to {his/her}
	"Who is the miscreant! Tell me {his/her} name!", "lady_other_suitor_challenge",
	##diplomacy end+
	[]],
[anyone|plyr,"lady_other_suitor", #similar to other
    [
	##diplomacy start+
	#Enable this if "enhanced prejudice" mode is active.
	(lt, "$g_disable_condescending_comments", 0),
	#(eq, 1, 0),
	##diplomacy end+
	],
    "I am tired of these games! I will demand that your family compel you to marry me..", "lady_player_threatens_compel",[
    ]],
[anyone,"lady_other_suitor_challenge",
	[
	  (check_quest_active,"qst_duel_courtship_rival"),
      (call_script, "script_troop_get_relation_with_troop", "$g_talk_troop", "$romantic_rival"),
	  (lt, reg0, 0),
	  ##diplomacy start+ Add support for female rival
	  (call_script, "script_dplmc_store_troop_is_female",  "$romantic_rival"),
	],#He -> {reg0?She:He}, man -> {reg0?woman:man}
	"I would be so grateful! But from what I understand, you already have a duel on your hands. {reg0?She:He} is not honor-bound to fight you, if you are committed to another combat. Please, conclude your other business in a hurry, to rescue me from that {reg0?woman:man}'s attentions!.", "lady_pretalk",
	##diplomacy end+
	[]],
[anyone,"lady_other_suitor_challenge",
	[
	(check_quest_active,"qst_duel_courtship_rival"),
	##diplomacy start+
	(assign, reg0, 1),
	(try_begin),
		(eq, reg65, "$character_gender"),
		(assign, reg0, 0),
	(try_end),
	],#Next line change "You men" to "{reg0?You {men/women}:People}"
	"Ah! Such talk. But from what I hear, you already have a duel on your hands. Finish one before you start another! Sigh... {reg0?You {men/women}:People} can be so silly...", "lady_pretalk",
	##diplomacy end+
	[]],
[anyone,"lady_other_suitor_challenge",
	[
    (call_script, "script_troop_get_relation_with_troop", "$g_talk_troop", "$romantic_rival"),
	(lt, reg0, 0),
	(str_store_troop_name, s5, "$romantic_rival"),
	##diplomacy start+ Add support for female rival
    (call_script, "script_dplmc_store_troop_is_female",  "$romantic_rival"),
	],#man -> {reg0?woman:man}
	"It is {s5}. Please, rescue me from that {reg0?woman:man}'s attentions!", "lady_other_suitor_challenge_confirm",
	##diplomacy end+
	[]],
[anyone,"lady_other_suitor_challenge",
	[
	(troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_ambitious),
	(str_store_troop_name, s5, "$romantic_rival"),
	],
	"Will you now? This should be interesting. Very well. Your rival is {s5}. Let us see which of you has the greater mettle.", "lady_other_suitor_challenge_confirm",
	[
	(assign, "$quarrel_penalty", 0),
	]],
[anyone,"lady_other_suitor_challenge",
	[
	(troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_conventional),
	(str_store_troop_name, s5, "$romantic_rival"),
	],##diplomacy start+ change "men" to "{men/women}"
	"Oh, fie! I wish that this were not a matter of honor, so I could refuse such a request. But alas, I feel compelled to tell you that your rival is {s5}. I wish that heaven had not granted me such a fair visage, so that I would not inspire such passions in {men/women}!", "lady_other_suitor_challenge_confirm",
	[##diplomacy end+
	(assign, "$quarrel_penalty", -1),
	]],
[anyone,"lady_other_suitor_challenge",
	[
	(str_store_troop_name, s5, "$romantic_rival"),
	],##diplomacy start+ change "sir" to "{sir/madame}"
	"I will have none of such talk! It is nonsense for you and {s5} to fight over -- whoops! I beg of you, {sir/madame}, forget the name that just escaped my lips...", "lady_other_suitor_challenge_confirm",
	[##diplomacy end+
	(assign, "$quarrel_penalty", -3),
	]],
[anyone|plyr,"lady_other_suitor_challenge_confirm",
	[##diplomacy start+ Add support for female rival
    (call_script, "script_dplmc_store_troop_is_female",  "$romantic_rival"),],
	#Change "him" to "{reg0?her:him}"
	"So be it! I shall challenge {reg0?her:him} to a trial of arms!", "lady_other_suitor_challenge_confirm_yes",
	##diplomacy end+
	[]],
[anyone|plyr,"lady_other_suitor_challenge_confirm",
	[],
	"On second thought, I let my passions run away with me there. Never mind.", "lady_other_suitor_challenge_confirm_no",
	[]],
[anyone,"lady_other_suitor_challenge_confirm_yes",
	[
	  (try_begin),
	    (call_script, "script_troop_get_relation_with_troop", "$g_talk_troop", "$romantic_rival"),
	    (lt, reg0, 0),
	    (str_store_string, s15, "str_do_be_careful_i_am_so_much_endebted_to_you_for_this"),
	  (else_try),
	    (troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_ambitious),
	    (str_store_string, s15, "str_go_then__we_shall_see_which_of_you_triumphs"),
	  (else_try),
	    (str_store_string, s15, "str_sigh_i_will_never_truly_understand_men_and_their_rash_actions"),
	  (try_end),
	],
	"{s15}", "lady_pretalk",
	[
	  (call_script, "script_troop_change_relation_with_troop", "trp_player", "$g_talk_troop", "$quarrel_penalty"),
	  (str_store_troop_name, s11, "$g_talk_troop"),
	  (str_store_troop_name_link, s13, "$romantic_rival"),
	  (setup_quest_text, "qst_duel_courtship_rival"),
	  ##diplomacy start+ use correct pronoun for gender
	  (call_script, "script_dplmc_store_troop_is_female_reg", "$romantic_rival", 4),
	  ##diplomacy end+
	  (str_store_string, s2, "str_you_intend_to_challenge_s13_to_force_him_to_relinquish_his_suit_of_s11"),

	  (call_script, "script_start_quest", "qst_duel_courtship_rival", "$g_talk_troop"),

	  (quest_set_slot, "qst_duel_courtship_rival", slot_quest_target_troop, "$romantic_rival"),

	  (quest_set_slot, "qst_duel_courtship_rival", slot_quest_xp_reward, 400),
	  (quest_set_slot, "qst_duel_courtship_rival", slot_quest_expiration_days, 60),
	  (quest_set_slot, "qst_duel_courtship_rival", slot_quest_current_state, 0),
	]],
[anyone,"lady_other_suitor_challenge_confirm_no",
	[],
	"Good. You are wise not to let your temper guide you.", "lady_private_conversation_end",
	[]],
[anyone|plyr,"lady_talk",
   [
	 (troop_slot_ge, "$g_talk_troop", slot_troop_spouse, 0),
#     (troop_slot_ge, "$g_talk_troop", slot_troop_met, 2),
     (store_partner_quest, ":ladys_quest"),
     (lt, ":ladys_quest", 0)
     ],
   "Is there anything I can do to win your favour?", "lady_ask_for_quest",[(call_script, "script_get_quest", "$g_talk_troop"),
                                                                 (assign, "$random_quest_no", reg0)]],
[anyone,"lady_ask_for_quest",
  [
    (troop_slot_eq, "$g_talk_troop", slot_troop_does_not_give_quest, 1),
  ],
   "I don't have anything else for you to do right now.", "lady_pretalk", []],
[anyone,"lady_ask_for_quest",
  [
	 (this_or_next|eq, "$random_quest_no", "qst_rescue_lord_by_replace"),
	 (eq, "$random_quest_no", "qst_rescue_prisoner"),

     (quest_get_slot, ":quest_target_troop", "$random_quest_no", slot_quest_target_troop),
     (call_script, "script_troop_get_family_relation_to_troop", ":quest_target_troop", "$g_talk_troop"),
     (str_store_string, s17, s11),
	 ##diplomacy start+ Correct pronouns if :quest_target_troop is female
	 (call_script, "script_dplmc_store_troop_is_female",  ":quest_target_troop"),
  ],#He -> {reg0?She:He}, his -> {reg0?her:his}, him -> {reg0?her:him}
   "Oh, I fear I may never see my {s17}, {s13}, again... {reg0?She:He} is a prisoner in {s14}.\
 We have tried to negotiate {reg0?her:his} ransom, but it has been set too high.\
 We can never hope to raise that much money without selling everything we own,\
 and God knows {s13} would rather spend {reg0?her:his} life in prison than make us destitute.\
 Instead I came up with a plan to get {reg0?her:him} out of there, but it requires someone to make a great sacrifice,\
 and so far my pleas have fallen on deaf ears...", "lady_mission_told",
 ##diplomacy end+
   [
     (quest_get_slot, ":quest_target_center", "$random_quest_no", slot_quest_target_center),
     (quest_get_slot, ":quest_target_troop", "$random_quest_no", slot_quest_target_troop),
     (call_script, "script_troop_get_family_relation_to_troop", ":quest_target_troop", "$g_talk_troop"),
     (str_store_string, s17, s11),

     (str_store_troop_name, s11, "$g_talk_troop"),
     (str_store_troop_name_link, s13, ":quest_target_troop"),
     (str_store_party_name_link, s14, ":quest_target_center"),
     (setup_quest_text,"$random_quest_no"),
	 ##diplomacy start+ Correct pronouns for the quest target and quest giver (reg65 for talk troop, reg4 is set for target above)
     (try_begin),
       (eq, "$random_quest_no", "qst_rescue_lord_by_replace"),
	   #changed pronouns next line
       (str_store_string, s2, "@{s11} asked you to rescue {reg65?her:his} {s17}, {s13}, from {s14} by switching clothes and taking {reg4?her:his} place in prison."),
     (else_try),
		#changed pronouns next line
       (str_store_string, s2, "@{s11} asked you to rescue {reg65?her:his} {s17}, {s13}, from {s14}."),
     (try_end),
	 ##diplomacy end+
    ]],
[anyone,"lady_ask_for_quest", [
     (eq, "$random_quest_no", "qst_deliver_message_to_prisoner_lord"),
     (quest_get_slot, ":quest_target_troop", "$random_quest_no", slot_quest_target_troop),
     (call_script, "script_troop_get_family_relation_to_troop", ":quest_target_troop", "$g_talk_troop"),

  ],
   "My poor {s11}, {s13}, is a prisoner in {s14}.\
 The only way we can talk to each other is by exchanging letters whenever we can,\
 but the journey is so dangerous that we get little chance to do so.\
 Please, would you deliver one for me?", "lady_mission_told",
   [
     (quest_get_slot, ":quest_target_center", "$random_quest_no", slot_quest_target_center),
     (quest_get_slot, ":quest_target_troop", "$random_quest_no", slot_quest_target_troop),


     (str_store_troop_name, s11, "$g_talk_troop"),
     (str_store_troop_name_link, s13, ":quest_target_troop"),
     (str_store_party_name_link, s14, ":quest_target_center"),
     (setup_quest_text,"$random_quest_no"),
     (str_store_string, s2, "@{s11} asked you to deliver a message to {s13}, who is imprisoned at {s14}."),
    ]],
[anyone,"lady_ask_for_quest", [(eq, "$random_quest_no", "qst_duel_for_lady")],
   "Dear {playername}, you are kind to ask, but you know little of my troubles\
 and I can't possibly ask you to throw yourself into danger on my behalf.", "lady_quest_duel_for_lady",[]],
[anyone|plyr,"lady_quest_duel_for_lady", [], "Tell me what the problem is, and I can make my own decision.", "lady_quest_duel_for_lady_2",
   [
     (quest_get_slot, ":quest_target_troop", "$random_quest_no", slot_quest_target_troop),

     (str_store_troop_name, s11, "$g_talk_troop"),
     (str_store_troop_name_link, s13, ":quest_target_troop"),
     (str_store_string, s2, "@You agreed to challenge {s13} to defend {s11}'s honour."),
     (setup_quest_text,"$random_quest_no"),
    ]],
[anyone,"lady_quest_duel_for_lady_2", [
  ##diplomacy start+ Add possibility of male version
  (quest_get_slot, ":quest_target_troop", "$random_quest_no", slot_quest_target_troop),
  (call_script, "script_dplmc_store_troop_is_female",  ":quest_target_troop"),#gender of lord to challenge

  (store_sub, reg1, 1, reg65),#gender of quest-giver's spouse (0 to 1, 1 to 0)
  (try_begin),
	(troop_slot_ge, "$g_talk_troop",  slot_troop_spouse, 0),
	(troop_get_slot, ":spouse", "$g_talk_troop", slot_troop_spouse),
	(assign, reg1, 0),
	(call_script, "script_cf_dplmc_troop_is_female", ":spouse"),
	(assign, reg1, 1),
  (try_end),
  #Numerous gender changes in next line
  ], "Very well, as you wish it...\
 My {reg1?wife:husband} has made certain enemies in {reg1?her:his} life, {playername}. One of the most insidious is {s13}.\
 {reg0?She:He} is going around making terrible accusations against me, impugning my honour at every turn!\
 Because {reg0?she:he} cannot harm my {reg1?wife:husband} directly, {reg0?she:he} is using me as a target to try and stain our name.\
 You should hear the awful things {reg0?she:he}'s said! I only wish there was someone brave enough to make {reg0?her:him} recant {reg0?her:his} slander,\
 but {s13} is a very fine swordsman, and {reg0?she:he}'s widely feared...", "lady_quest_duel_for_lady_3",[]],
[anyone|plyr,"lady_quest_duel_for_lady_3", [
  ##diplomacy start+ Add possibility of fe/male version
  (quest_get_slot, ":quest_target_troop", "$random_quest_no", slot_quest_target_troop),
  (call_script, "script_dplmc_store_troop_is_female",  ":quest_target_troop"),#gender of lord to challenge
  #next line, him -> {reg0?her:him}, his -> {reg0?her:his}
  ], "I fear {reg0?her:him} not, {s65}. I will make {reg0?her:him} take back {reg0?her:his} lies.", "lady_quest_duel_for_lady_3_accepted",[]],
[anyone,"lady_quest_duel_for_lady_3_accepted", [], "Oh! I can't ask that of you, {playername}, but...\
 I would be forever indebted to you, and you are so sure. It would mean so much if you would defend my honour.\
 Thank you a thousand times, all my prayers and my favour go with you.", "close_window",
   [

     (quest_get_slot, ":quest_target_troop", "$random_quest_no", slot_quest_target_troop),
     (call_script, "script_start_quest", "$random_quest_no", "$g_talk_troop"),
     (call_script, "script_report_quest_troop_positions", "$random_quest_no", ":quest_target_troop", 3),
     (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 3),
     ]],
[anyone|plyr,"lady_quest_duel_for_lady_3", [##diplomacy start+ Use proper pronoun
  (quest_get_slot, ":quest_target_troop", "$random_quest_no", slot_quest_target_troop),
  (call_script, "script_dplmc_store_troop_is_female",  ":quest_target_troop"),#gender of lord to challenge
  ], "If {reg0?she:he}'s that dangerous, perhaps maybe it would be better to ignore {reg0?her:him}...", "lady_quest_duel_for_lady_3_rejected",[]],
[anyone,"lady_quest_duel_for_lady_3_rejected", [], "Oh... Perhaps you're right, {playername}.\
 I should let go of these silly childhood ideas of chivalry and courage. {Men/People} are not like that,\
 not anymore. Good day to you.", "close_window",
   [(troop_set_slot, "$g_talk_troop", slot_troop_does_not_give_quest, 1),
    (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", -1),
    ]],
[anyone,"lady_ask_for_quest", [], "No, {playername}, I've no need for a champion right now.", "lady_pretalk",[]],
[anyone|plyr,"lady_mission_told", [], "As you wish it, {s65}, it shall be done.", "lady_mission_accepted",[]],
[anyone|plyr,"lady_mission_told", [], "{s66}, I fear I cannot help you right now.", "lady_mission_rejected",[]],
[anyone,"lady_mission_accepted", [], "You are a true {gentleman/lady}, {playername}.\
 Thank you so much for helping me", "close_window",
   [
     (try_begin),
       (eq, "$random_quest_no", "qst_deliver_message_to_prisoner_lord"),
       (call_script, "script_troop_add_gold", "trp_player", 10),
     (try_end),
     (call_script, "script_start_quest", "$random_quest_no", "$g_talk_troop"),
    ]],
[anyone,"lady_mission_rejected", [
  #changed "woman" -> "{reg65?woman:young lad}"
  ], "You'll not help a {reg65?woman:young lad} in need? You should be ashamed, {playername}...\
 Please leave me, I have some important embroidery to catch up.", "close_window",
##diplomacy end+
   [
     (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", -1),
     (troop_set_slot, "$g_talk_troop", slot_troop_does_not_give_quest, 1),
    ]],
[anyone|plyr,"lady_talk", [
  (troop_slot_ge, "$g_talk_troop", slot_troop_spouse, 0),
  ], "I want to improve my relation with a lord. Can you help me?", "lady_restore_relation",[]],
[anyone,"lady_restore_relation", [(le, "$g_talk_troop_relation", 0)], "{playername}, I don't know you well enough to act on your behalf. I am sorry.", "lady_pretalk",[]],
[anyone,"lady_restore_relation", [], "Hmm. I guess you got on the wrong side of somebody. Very well, who do you want to restore your relation with?", "lady_restore_relation_2",[]],
[anyone|plyr|repeat_for_troops,"lady_restore_relation_2", [(store_repeat_object, ":troop_no"),
                                                             (is_between, ":troop_no", active_npcs_begin, active_npcs_end),
                                                             (store_troop_faction, ":faction_no", ":troop_no"),
                                                             (eq, "$g_talk_troop_faction", ":faction_no"),
                                                             (call_script, "script_troop_get_player_relation", ":troop_no"),
                                                             (lt, reg0, 0),
                                                             ##diplomacy start+
                                                             #enhanced functionality for relatives
                                                             (str_store_troop_name, s1, ":troop_no"),
                                                             (call_script,"script_troop_get_family_relation_to_troop",":troop_no","$g_talk_troop"),
                                                             (try_begin),
                                                                 (ge, reg0, 1),
                                                                 (str_store_string, s10, s1),
                                                                 (str_store_string, s1, "str_dplmc_your_s11_s10"),
                                                             (try_end),
                                                             ],
   "{s1}", "lady_restore_relation_2b",[(store_repeat_object, "$troop_to_restore_relations_with")]],
[anyone|plyr,"lady_restore_relation_2", [], "Never mind. I get along with everyone well enough.", "lady_pretalk",[]],
[anyone,"lady_restore_relation_2b", [(str_store_troop_name, s10, "$troop_to_restore_relations_with")], "Well I can try to help you there.\
 I am sure a few expensive gifts will make {s10} look at you more favorably.", "lady_restore_relation_3",[]],
[anyone,"lady_restore_relation_3", [(str_store_troop_name, s10, "$troop_to_restore_relations_with"),
                                      (assign, "$lady_restore_cost_1", 1000),
                                      (assign, "$lady_restore_cost_2", 2000),
                                      (assign, "$lady_restore_cost_3", 3000),
                                      ##diplomacy start+
                                      #lower cost for relatives
                                      (call_script,"script_troop_get_family_relation_to_troop","$troop_to_restore_relations_with","$g_talk_troop"),
                                      (try_begin),
                                         (ge, reg0, 10),
                                         (assign, "$lady_restore_cost_1", 750),
                                         (assign, "$lady_restore_cost_2", 1500),
                                         (assign, "$lady_restore_cost_3", 2250),
                                         (str_store_string, s10, s11),
                                      (else_try),
                                         (ge, reg0, 1),
                                         (assign, "$lady_restore_cost_1", 900),
                                         (assign, "$lady_restore_cost_2", 1800),
                                         (assign, "$lady_restore_cost_3", 2700),
                                         (str_store_string, s10, s11),
                                      (try_end),
                                      ##diplomacy end+
                                      (assign, reg10, "$lady_restore_cost_1"),
                                      (assign, reg11, "$lady_restore_cost_2"),
                                      (assign, reg12, "$lady_restore_cost_3"),
									  ##diplomacy start+ Unnecessary, since the family relation script sets this
                                      #(troop_get_type, reg4, "$troop_to_restore_relations_with"),
									  ##diplomacy end+
                                      ],
   "You can improve your relation with {s10} by sending {reg4?her:him} a gift worth {reg10} mon.\
 But if you can afford spending {reg11} mon on the gift, it would make a good impression on {reg4?her:him}.\
 And if you can go up to {reg12} mon, that would really help smooth things out.", "lady_restore_relation_4",[]],
[anyone|plyr,"lady_restore_relation_4", [(store_troop_gold,":gold", "trp_player"),
                                           (ge, ":gold", "$lady_restore_cost_1"),
                                           (assign, reg10, "$lady_restore_cost_1")],
   "I think a gift of {reg10} mon will do.", "lady_restore_relation_5",[(assign, "$temp", 1), (assign, "$temp_2", "$lady_restore_cost_1")]],
[anyone|plyr,"lady_restore_relation_4", [(store_troop_gold,":gold", "trp_player"),
                                           (ge, ":gold", "$lady_restore_cost_2"),
                                           (assign, reg11, "$lady_restore_cost_2")],
   "Maybe I can afford {reg11} mon.", "lady_restore_relation_5",[(assign, "$temp", 2), (assign, "$temp_2", "$lady_restore_cost_2")]],
[anyone|plyr,"lady_restore_relation_4", [(store_troop_gold,":gold", "trp_player"),
                                           (ge, ":gold", "$lady_restore_cost_3"),
                                           (assign, reg12, "$lady_restore_cost_3")],
   "In that case, I am ready to spend {reg12} mon.", "lady_restore_relation_5",[(assign, "$temp", 3), (assign, "$temp_2", "$lady_restore_cost_3")]],
[anyone|plyr,"lady_restore_relation_4", [], "I don't think I can afford a gift at the moment.", "lady_restore_relation_cant_afford",[]],
[anyone,"lady_restore_relation_5", [], "Excellent. Then I'll choose an appropriate gift for you and send it to {s10} with your compliments.\
 I am sure {reg4?she:he} will appreciate the gesture.", "lady_restore_relation_6",[
     (troop_remove_gold, "trp_player","$temp_2"),
     (call_script, "script_change_player_relation_with_troop", "$troop_to_restore_relations_with", "$temp"),
	 ##diplomacy start+
     #(troop_get_type, reg4, "$troop_to_restore_relations_with"),
	 (call_script, "script_dplmc_store_troop_is_female_reg", "$troop_to_restore_relations_with", 4),
	 ##diplomacy end+
     ]],
[anyone|plyr,"lady_restore_relation_6", [], "Thank you for your help, madame.", "lady_pretalk",[]],
[anyone,"lady_restore_relation_cant_afford", [], "I am afraid, I can't be of much help in that case, {playername}. I am sorry.", "lady_pretalk",[]],
[anyone|plyr,"lady_talk", [], "I must beg my leave.", "lady_leave",[]],
[anyone|auto_proceed,"lady_leave", [
  (call_script, "script_troop_get_relation_with_troop", "$g_talk_troop", "trp_player"),
  (try_begin),
	(lt, reg0, 0),
	(str_store_string, s12, "str_farewell"),
  (else_try),
	(str_store_string, s12, "str_farewell_playername"),
  (try_end),
  ], "{s12}", "close_window",[(eq,"$talk_context",tc_party_encounter),(assign, "$g_leave_encounter", 1)]],
[anyone|plyr,"lord_persuade_lords_to_make_peace_completed", [],
   "Thank you. Let me have the money.", "lord_persuade_lords_to_make_peace_pay",[]],
[anyone|plyr,"lord_persuade_lords_to_make_peace_completed", [],
   "No need for a payment. I only did what was right.", "lord_persuade_lords_to_make_peace_no_pay",[]],
[anyone ,"lord_persuade_lords_to_make_peace_pay", [],
   "Oh, yes, of course. We had already got the money for you.\
 Here, please accept these {reg12} mon together with our most sincere thanks.\
 Me and the people of our town will not forget your help.", "close_window",
   [(quest_get_slot, ":quest_reward", "qst_persuade_lords_to_make_peace", slot_quest_gold_reward),
    (call_script, "script_troop_add_gold", "trp_player", ":quest_reward"),
    (call_script, "script_change_player_relation_with_center", "$current_town", 5),
    (call_script, "script_end_quest", "qst_persuade_lords_to_make_peace"),
    (quest_get_slot, ":quest_reward", "qst_persuade_lords_to_make_peace", slot_quest_gold_reward),
    (assign, reg12, ":quest_reward")
    ]],
[anyone ,"lord_persuade_lords_to_make_peace_no_pay", [],
   "You are indeed an extraordinary person, {sir/madame}, and it is an honour for me to have known you.\
 You not only did what was impiossible and put an end to this terrible war, but you won't even accept a reward for it.\
 Very well, I will not insist on the matter, but please know that you will have our eternal respect and gratitude.", "close_window",
   [
    (call_script, "script_change_player_honor", 3),
    (call_script, "script_change_player_relation_with_center", "$current_town", 8),
    (call_script, "script_end_quest", "qst_persuade_lords_to_make_peace"),
    ]],
[anyone|plyr,"lord_deal_with_night_bandits_completed", [],
   "It was my pleasure, {s65}.", "close_window",[]],
[anyone|plyr ,"lord_ask_leave_service_verify_again", [
	##altered the condition block
	(neg|troop_slot_eq, "trp_player", slot_troop_spouse, "$g_talk_troop"),
	(neg|troop_slot_eq, "$g_talk_troop", slot_troop_spouse, "trp_player"),
	(neg|faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, "trp_player"),
	(call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", "$g_talk_troop_faction"),
	(lt, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),

	(assign, ":has_walled_center", walled_centers_end),
	(try_for_range, ":center_no", walled_centers_begin, ":has_walled_center"),
		(party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
		(assign, ":has_walled_center", ":center_no"),
	(try_end),
	(is_between, ":has_walled_center", walled_centers_begin, walled_centers_end),

  ], "I have no intention of losing my lands, {s65}.", "dplmc_lord_ask_leave_service_rebellion",[]],
]
