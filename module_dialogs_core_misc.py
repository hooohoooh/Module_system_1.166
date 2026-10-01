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

dialogs_core_misc = [
[anyone ,"start", [(store_conversation_troop, "$g_talk_troop"),
               (store_conversation_agent, "$g_talk_agent"),
               (store_troop_faction, "$g_talk_troop_faction", "$g_talk_troop"),
#                     (troop_get_slot, "$g_talk_troop_relation", "$g_talk_troop", slot_troop_player_relation),
               (call_script, "script_troop_get_player_relation", "$g_talk_troop"),
               (assign, "$g_talk_troop_relation", reg0),

          #This may be different way to handle persuasion, which might be a little more transparent to the player in its effects
          #Persuasion will affect the player's relation with the other character -- but only for 1 on 1 conversations
          (store_skill_level, ":persuasion", "skl_persuasion", "trp_player"),
          (assign, "$g_talk_troop_effective_relation", "$g_talk_troop_relation"),
          (val_add, "$g_talk_troop_effective_relation", ":persuasion"),
          (try_begin),
            (gt, "$g_talk_troop_effective_relation", 0),
            (store_add, ":persuasion_modifier", 10, ":persuasion"),
            (val_mul, "$g_talk_troop_effective_relation", ":persuasion_modifier"),
            (val_div, "$g_talk_troop_effective_relation", 10),
          (else_try),
            (lt, "$g_talk_troop_effective_relation", 0),
            (store_sub, ":persuasion_modifier", 20, ":persuasion"),
            (val_mul, "$g_talk_troop_effective_relation", ":persuasion_modifier"),
            (val_div, "$g_talk_troop_effective_relation", 20),
          (try_end),
          (val_clamp, "$g_talk_troop_effective_relation", -100, 101),
          (try_begin),
            (eq, "$cheat_mode", 1),
            (assign, reg3, "$g_talk_troop_effective_relation"),
            (display_message, "str_test_effective_relation_=_reg3"),
          (try_end),

               (try_begin),
                 (this_or_next|is_between, "$g_talk_troop", village_elders_begin, village_elders_end),
                 (is_between, "$g_talk_troop", mayors_begin, mayors_end),
                 (party_get_slot, "$g_talk_troop_relation", "$current_town", slot_center_player_relation),
               (try_end),
               (store_relation, "$g_talk_troop_faction_relation", "$g_talk_troop_faction", "fac_player_faction"),

               (assign, "$g_talk_troop_party", "$g_encountered_party"),
               (try_begin),
                 (troop_slot_ge, "$g_talk_troop", slot_troop_leaded_party, 1),
                 (troop_get_slot, "$g_talk_troop_party", "$g_talk_troop", slot_troop_leaded_party),
               (try_end),

#                     (assign, "$g_talk_troop_kingdom_relation", 0),
#                     (try_begin),
#                       (gt, "$players_kingdom", 0),
#                       (store_relation, "$g_talk_troop_kingdom_relation", "$g_talk_troop_faction", "$players_kingdom"),
#                     (try_end),



               (store_current_hours, "$g_current_hours"),
               (troop_get_slot, "$g_talk_troop_last_talk_time", "$g_talk_troop", slot_troop_last_talk_time),
               (troop_set_slot, "$g_talk_troop", slot_troop_last_talk_time, "$g_current_hours"),
               (store_sub, "$g_time_since_last_talk","$g_current_hours","$g_talk_troop_last_talk_time"),
               (troop_get_slot, "$g_talk_troop_met", "$g_talk_troop", slot_troop_met),
          (val_min, "$g_talk_troop_met", 1), #the global variable goes no higher than one
          (try_begin),
             (troop_slot_eq, "$g_talk_troop", slot_troop_met, 0),
            (troop_set_slot, "$g_talk_troop", slot_troop_met, 1),

            #Possible later activations of notes
            (try_begin),
               (is_between, "$g_talk_troop", kingdom_ladies_begin, kingdom_ladies_end),
            (try_end),

          (try_end),

               (try_begin),
#                       (this_or_next|eq, "$talk_context", tc_party_encounter),
#                       (this_or_next|eq, "$talk_context", tc_castle_commander),
                 ##diplomacy start+
				 (try_begin),
					#Use terrain advantage if appropriate
			        (ge, "$g_dplmc_terrain_advantage", DPLMC_TERRAIN_ADVANTAGE_ENABLE),
					(assign, ":terrain_code", -1),
				    (try_begin),
						(encountered_party_is_attacker),
						(call_script, "script_dplmc_get_terrain_code_for_battle", "$g_encountered_party", "p_main_party"),
						(assign, ":terrain_code", reg0),
				    (else_try),
						(call_script, "script_dplmc_get_terrain_code_for_battle", "p_main_party", "$g_encountered_party"),
						(assign, ":terrain_code", reg0),
				    (try_end),
					#Call adjusting for terrain
					(call_script, "script_dplmc_party_calculate_strength_in_terrain", "p_collective_enemy",":terrain_code",0,1),
					(assign, "$g_enemy_strength", reg0),
					(call_script, "script_dplmc_party_calculate_strength_in_terrain", "p_main_party",":terrain_code",0,1),
					(assign, "$g_ally_strength", reg0),
				 (else_try),
				     #Old method: no terrain advantage
					 (call_script, "script_party_calculate_strength", "p_collective_enemy",0),
					 (assign, "$g_enemy_strength", reg0),
					 (call_script, "script_party_calculate_strength", "p_main_party",0),
					 (assign, "$g_ally_strength", reg0),
		         (try_end),
				 ##diplomacy end+
                 (store_mul, "$g_strength_ratio", "$g_ally_strength", 100),
            (assign, ":enemy_strength", "$g_enemy_strength"), #these two lines added to avoid div by zero error
            (val_max, ":enemy_strength", 1),
                 (val_div, "$g_strength_ratio", ":enemy_strength"),
               (try_end),

               (assign, "$g_comment_found", 0),

          (assign, "$g_comment_has_rejoinder", 0),
          (assign, "$g_romantic_comment_made", 0),
          (assign, "$skip_lord_assumes_argument", 0), #a lord pre-empts a player's issue, ie, when the player is conducting a rebellion
          (assign, "$bypass_female_vassal_explanation", 0),
          (assign, "$g_done_wedding_comment", 0),

#					 (assign, "$g_time_to_spare", 0),


               (try_begin),
                 (troop_is_hero, "$g_talk_troop"),
                 (talk_info_show, 1),
                 (call_script, "script_setup_talk_info"),
               (try_end),

          (assign, "$g_last_comment_copied_to_s42", 0),
               (try_begin),
                 (troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_hero),
                 (call_script, "script_get_relevant_comment_to_s42"),
                 (assign, "$g_comment_found", reg0),
               (try_end),

			   ##diplomacy start+
			   #(troop_get_type, reg65, "$g_talk_troop"),
			   ##Override reg65 with script for gender
		           (assign, reg65, 0),
		           (try_begin),
		              (call_script, "script_cf_dplmc_troop_is_female", "$g_talk_troop"),
		              (assign, reg65, 1),
		           (try_end),
			   ##diplomacy end+
               (try_begin),
                 (faction_slot_eq,"$g_talk_troop_faction",slot_faction_leader,"$g_talk_troop"),
                 (str_store_string,s64,"@{reg65?my Lady:my Lord}"), #bug fix
                 (str_store_string,s65,"@{reg65?my Lady:my Lord}"),
                 (str_store_string,s66,"@{reg65?My Lady:My Lord}"),
                 (str_store_string,s67,"@{reg65?My Lady:My Lord}"), #bug fix
               (else_try),
                 (str_store_string,s64,"@{reg65?madame:sir}"), #bug fix
                 (str_store_string,s65,"@{reg65?madame:sir}"),
                 (str_store_string,s66,"@{reg65?Madame:Sir}"),
                 (str_store_string,s67,"@{reg65?Madame:Sir}"), #bug fix
               (try_end),

          (try_begin),
            (gt, "$cheat_mode", 0),
            (assign, reg4, "$talk_context"),
            (display_message, "@{!}DEBUG -- Talk context: {reg4}"),
          (try_end),

          (try_begin),
            (gt, "$cheat_mode", 0),
            (assign, reg4, "$g_time_since_last_talk"),
            (display_message, "@{!}DEBUG -- Time since last talk: {reg4}"),
          (try_end),


          (try_begin),
            (eq, "$cheat_mode", 0),
            (store_partner_quest, ":quest"),
            (ge, ":quest", 0),
            (str_store_quest_name, s4, ":quest"),

          (try_end),

               (eq, 1, 0)],
"{!}Warning: This line is never displayed. It is just for storing conversation variables.", "close_window", []],
[anyone ,"event_triggered", [(store_conversation_troop, "$g_talk_troop"),
                     (try_begin),
					 
						 #gekokujo 3.0 microfactions! include fort companions start
                         #(is_between, "$g_talk_troop", companions_begin, companions_end),
                         (is_between, "$g_talk_troop", companions_begin, fort_companions_end),
						 #gekokujo 3.0 microfactions! include fort companions end
                         (talk_info_show, 1),
                         (call_script, "script_setup_talk_info_companions"),
                     (try_end),

	 			##diplomacy start+ Get gender for troop
				##OLD:
				#(troop_get_type, reg65, "$g_talk_troop"),
				##NEW:
				(try_begin),
					(call_script, "script_cf_dplmc_troop_is_female", "$g_talk_troop"),
					(assign, reg65, 1),
				(else_try),
					(assign, reg65, 0),
				(try_end),
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


               (eq, 1, 0)],
"{!}Warning: This line is never displayed. It is just for storing conversation variables.", "close_window", []],
[anyone, "event_triggered",
[
(eq, "$talk_context", tc_give_center_to_fief),

(assign, ":there_are_vassals", 0),
##diplomacy start+ Handle player is co-ruler of kingdom
(assign, ":alt_faction", "fac_player_supporters_faction"),
(try_begin),
	(is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
	(call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", "$players_kingdom"),
	(ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
	(assign, ":alt_faction", "$players_kingdom"),
(try_end),
#Support promoted ladies
#(assign, ":end_cond", active_npcs_end),
(assign, ":end_cond", heroes_end),
##diplomacy end+
(try_for_range, ":troop_no", active_npcs_begin, ":end_cond"),
 (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
 (neq, "trp_player", ":troop_no"),
 (store_troop_faction, ":faction_no", ":troop_no"),
 ##diplomacy start+
 (this_or_next|eq, ":faction_no", ":alt_faction"),
 ##diplomacy end+
 (eq, ":faction_no", "fac_player_supporters_faction"),
 (val_add, ":there_are_vassals", 1),
 (assign, ":end_cond", 0),
(try_end),

(try_begin),
 (gt, ":there_are_vassals", 0),
 (str_store_string, s2, "str_do_you_wish_to_award_it_to_one_of_your_vassals"),
(else_try),
 (str_store_string, s2, "str_who_do_you_wish_to_give_it_to"),
(try_end),

(str_store_party_name, s1, "$g_center_taken_by_player_faction"),
(str_store_string, s5, "str_sire_my_lady_we_have_taken_s1_s2"),
],
"{!}{s5}", "award_fief_to_vassal",
[]],
# Awarding fiefs in rebellion...

[anyone, "event_triggered",
[
##diplomacy start+ Handle g_talk_troop and player are co-rulers of kingdom
(assign, ":is_coruler", 0),
(try_begin),
	(is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
	(faction_slot_eq, "$players_kingdom", slot_faction_leader, "$g_talk_troop"),
	(call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", "$players_kingdom"),
	(ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
	(assign, ":is_coruler", 1),
(try_end),
(this_or_next|eq, ":is_coruler", 1),
##diplomacy end+
(faction_slot_eq, "fac_player_supporters_faction", slot_faction_leader, "$g_talk_troop"),
(ge, "$g_center_taken_by_player_faction", 0),
(str_store_party_name, s1, "$g_center_taken_by_player_faction"),
],
"{s1} is not being managed by anyone. Who shall be put in charge?", "center_captured_rebellion",
[]],
#TUTORIAL START
[anyone, "start",
[
(is_between, "$g_talk_troop", tutorial_fighters_begin, tutorial_fighters_end),
(eq, "$g_tutorial_training_ground_conversation_state", 0),
(eq, "$g_tutorial_fighter_talk_before", 0)],
"Hello there. We are polishing off our combat skills here with a bit of sparring practice.\
You look like you could use a bit of training. Why don't you join us, and we can show you a few tricks.\
And if you need explanation of any combat concepts, just ask, and I will do my best to fill you in.", "fighter_talk",
[
(try_begin),
 (eq, "$g_tutorial_training_ground_intro_message_being_displayed", 1),
 (assign, "$g_tutorial_training_ground_intro_message_being_displayed", 0),
 (tutorial_message, -1), #remove tutorial intro immediately before a conversation
(try_end),
(assign, "$g_tutorial_fighter_talk_before", 1)]],
[anyone, "start",
[(is_between, "$g_talk_troop", tutorial_fighters_begin, tutorial_fighters_end),
(eq, "$g_tutorial_training_ground_conversation_state", 0)],
"What do you want to practice?", "fighter_talk", []],
[anyone, "start",
[(is_between, "$g_talk_troop", tutorial_fighters_begin, tutorial_fighters_end),
(eq, "$g_tutorial_training_ground_conversation_state", 1)], #parry complete
"Good. You were able to block my attacks successfully. You may repeat this practice and try to get faster each time, until you are confident of your defense skills. Do you want to have another go?", "fighter_parry_try_again",
[
(assign, "$g_tutorial_training_ground_conversation_state", 0),
]],
[anyone, "start",
[(is_between, "$g_talk_troop", tutorial_fighters_begin, tutorial_fighters_end),
(eq, "$g_tutorial_training_ground_conversation_state", 2)], #player knocked down in parry
"Well that didn't go too well, did it? (Remember, you must press and hold down the right mouse button to keep your block effective.) Do you want to try again?", "fighter_parry_try_again",
[
(assign, "$g_tutorial_training_ground_conversation_state", 0),
]],
[anyone, "start",
[(is_between, "$g_talk_troop", tutorial_fighters_begin, tutorial_fighters_end),
(eq, "$g_tutorial_training_ground_conversation_state", 3)], #trainer knocked down in parry
"Hey! We are doing a blocking practice! You are supposed to block my attacks, not attack me back.", "fighter_parry_warn",
[
(assign, "$g_tutorial_training_ground_conversation_state", 0),
]],
[anyone, "start",
[(is_between, "$g_talk_troop", tutorial_fighters_begin, tutorial_fighters_end),
(eq, "$g_tutorial_training_ground_conversation_state", 4)], #player knocked down in combat
"Well that didn't go too well, did it?  Don't feel bad, and try not to do same mistakes next time. Do you want to have a go again?", "fighter_combat_try_again",
[
(assign, "$g_tutorial_training_ground_conversation_state", 0),
]],
[anyone, "start",
[(is_between, "$g_talk_troop", tutorial_fighters_begin, tutorial_fighters_end),
(eq, "$g_tutorial_training_ground_conversation_state", 5)], #trainer knocked down in combat
"Hey, that was good sparring. You defeated me, but next time I'll be more careful. Do you want to have a go again?", "fighter_combat_try_again",
[
(assign, "$g_tutorial_training_ground_conversation_state", 0),
]],
# [anyone, "start",
# [(is_between, "$g_talk_troop", tutorial_fighters_begin, tutorial_fighters_end),
# (eq, "$g_tutorial_training_ground_conversation_state", 6)], #chamber complete
# "{!}TODO: Congratulations. Anything else?", "fighter_talk",
# [
# (assign, "$g_tutorial_training_ground_conversation_state", 0),
# ]],

# [anyone, "start",
# [(is_between, "$g_talk_troop", tutorial_fighters_begin, tutorial_fighters_end),
# (eq, "$g_tutorial_training_ground_conversation_state", 7)], #player knocked down in chamber
# "{!}TODO: Want to try again?", "fighter_chamber_try_again",
# [
# (assign, "$g_tutorial_training_ground_conversation_state", 0),
# ]],

# [anyone|plyr, "fighter_chamber_try_again",
# [],
# "{!}TODO: OK let's try again.", "fighter_talk_train_chamber", []],

# [anyone|plyr, "fighter_chamber_try_again",
# [],
# "TODO: No, let's leave it there.", "fighter_talk_leave_chamber", []],

# [anyone, "fighter_talk_leave_chamber",
# [],
# "{!}TODO: OK. Bye.", "close_window", []],

[anyone, "start",
[(is_between, "$g_talk_troop", tutorial_fighters_begin, tutorial_fighters_end),
(eq, "$g_tutorial_training_ground_conversation_state", 8)], #trainer knocked down in chamber
"{!}TODO: What are you doing? Don't attack me except while chambering!", "fighter_chamber_warn",
[
(assign, "$g_tutorial_training_ground_conversation_state", 0),
]],
[anyone, "start",
[(is_between, "$g_talk_troop", tutorial_fighters_begin, tutorial_fighters_end),
(eq, "$g_tutorial_training_ground_conversation_state", 9)], #attack complete
"Very good. You have learned how to attack from any direction you want. If you like we can try this again or move to a different exercise.", "fighter_talk",
[
(assign, "$g_tutorial_training_ground_conversation_state", 0),
]],
[trp_tutorial_archer_1|auto_proceed, "start",
[],
"{!}.", "tutorial_troop_default",
[]],
[trp_tutorial_master_archer, "start",
[
(eq, "$g_tutorial_training_ground_archer_trainer_completed_chapters", 1),
],
"Not bad. Not bad at all! You seem to have grasped the basics of archery. Now, try to do the same thing with a crossbow.\
Take the crossbow and the bolts over there and shoot those three targets. The crossbow is much easier to shoot with compared with the bow,\
but you need to reload it after each shot.", "archer_challenge_2", []],
[trp_tutorial_master_archer, "start",
[
(eq, "$g_tutorial_training_ground_archer_trainer_completed_chapters", 2),
],
"Good. You didn't have too much difficulty using the crossbow either. Next you will learn to use throwing weapons.\
Pick up the javelins you see over there and try to hit those three targets. ",
"archer_challenge_2", []],
[trp_tutorial_master_archer, "start",
[
(eq, "$g_tutorial_training_ground_archer_trainer_completed_chapters", 3),
],
"Well, with that you have recevied the basic skills to use all three types of ranged weapons. The rest will come with practice. Train each and every day, and in time you will be as good as the best marksmen in Japan.",
"ranged_end", []],
[trp_tutorial_master_archer, "ranged_end", [],
"Now, you can go talk with the melee fighters or the horsemanship trainer if you haven't already done so. They can teach you important skills too.",
"close_window", []],
[trp_tutorial_master_archer, "start",
[
(try_begin),
 (eq, "$g_tutorial_training_ground_intro_message_being_displayed", 1),
 (assign, "$g_tutorial_training_ground_intro_message_being_displayed", 0),
 (tutorial_message, -1), #remove tutorial intro immediately before a conversation
(try_end),

],
"Good day to you, young fellow. I spend my days teaching about ranged weapons to anyone that is willing to learn.\
If you need a tutor, let me know and I'll teach you how to use the bow, the crossbow and the javelin.", "archer_talk",
[]],
[trp_tutorial_master_horseman, "start",
[
(eq, "$g_tutorial_training_ground_horseman_trainer_completed_chapters", 1),
],
"I hope you enjoyed the ride. Now we move on to something a bit more difficult. Grab the lance you see over there and ride around the course hitting each target at least once.",
"horseman_melee_challenge_2", []],
[trp_tutorial_master_horseman, "start",
[
(eq, "$g_tutorial_training_ground_horseman_trainer_completed_chapters", 2),
],
"Good! You have been able to hit all targets on horseback. That's no easy feat for a starter. Your next challange will be using a bow and arrows to shoot at the archery targets by the road. You need to put an arrow to each target to consider yourself successful.",
"horseman_melee_challenge_2", []],
[trp_tutorial_master_horseman, "start",
[
(eq, "$g_tutorial_training_ground_horseman_trainer_completed_chapters", 3),
],
"Very good. You were able to shoot all targets from horseback. Keep riding and practicing each day and in time you will be an expert horseman.", "horsemanship_end",
[
]],
[trp_tutorial_master_horseman, "start",
[
(try_begin),
 (eq, "$g_tutorial_training_ground_intro_message_being_displayed", 1),
 (assign, "$g_tutorial_training_ground_intro_message_being_displayed", 0),
 (tutorial_message, -1), #remove tutorial intro immediately before a conversation
(try_end),
],
"Good day! I have come here for some riding practice, but my old bones are aching badly so I decided to give myself a rest today.\
If you would like to practice your horsemanship, you can take my horse here. The exercise would be good for her.", "horseman_talk",
[]],
[trp_tutorial_rider_1|auto_proceed, "start",
[],
"{!}Warning: This line is never displayed.", "tutorial_troop_default",
[]],
[trp_tutorial_rider_2|auto_proceed, "start",
[],
"{!}Warning: This line is never displayed.", "tutorial_troop_default",
[]],
#PRISON BREAK START
[anyone,"start",
[
(eq, "$talk_context", tc_prison_break),
(troop_slot_eq, "$g_talk_troop", slot_troop_prisoner_of_party, "$g_encountered_party"),
(troop_slot_ge, "$g_talk_troop", slot_troop_mission_participation, mp_stay_out),
],
"Is there a change of plans?", "lord_prison_break_confirm_3",[]],
[anyone,"start",
[
(eq, "$talk_context", tc_prison_break),
(try_begin),
 (eq, "$cheat_mode", 1),
 (assign, reg0, "$g_talk_troop"),
 (assign, reg1, "$g_encountered_party"),
 (troop_get_slot, reg2, "$g_talk_troop", slot_troop_prisoner_of_party),
 (display_message, "@{!}g_talk_troop = {reg0} , g_encountered_party = {reg1} , slot value = {reg2}"),
(try_end),
(troop_slot_eq, "$g_talk_troop", slot_troop_prisoner_of_party, "$g_encountered_party"),
],
"What's going on?", "lord_prison_break",[]],
#TAVERN DRUNK DIALOGS
[anyone, "start",
[
(eq, "$g_talk_troop", "trp_belligerent_drunk"),
],
"What are you looking at?", "drunk_response",
[
(try_begin),
 (eq, "$g_main_attacker_agent", 0),
 (call_script, "script_activate_tavern_attackers"),
(try_end),
(mission_disable_talk),
]],
[anyone, "start",
[
(eq, "$g_talk_troop", "trp_hired_assassin"),
],
"Are you looking at me?", "drunk_response",
[
(try_begin),
 (eq, "$g_main_attacker_agent", 0),
 (call_script, "script_activate_tavern_attackers"),
(try_end),
(mission_disable_talk),
]],
[anyone, "start",
[
(eq, "$g_talk_troop", "trp_hired_assassin"),
(eq,1,0),
],
"{!}Added to match dialog ids with translations.", "close_window",
[]],
[anyone, "start", [
(is_between, "$g_talk_troop", tavernkeepers_begin, tavernkeepers_end),
(gt, "$g_main_attacker_agent", 0),
(neg|agent_is_alive, "$g_main_attacker_agent"),

(try_begin),
(neg|agent_is_alive, "$g_main_attacker_agent"),
(agent_get_troop_id, ":type", "$g_main_attacker_agent"),
(eq, ":type", "trp_hired_assassin"),

(str_store_string, s9, "str_strange_that_one_didnt_seem_like_your_ordinary_troublemaker_he_didnt_drink_all_that_much__he_just_stood_there_quietly_and_watched_the_door_you_may_wish_to_consider_whether_you_have_any_enemies_who_know_you_are_in_town_a_pity_that_blood_had_to_be_spilled_in_my_establishment"),

(assign, "$g_main_attacker_agent", 0),
(troop_add_gold, "trp_player", 50),
(troop_add_item, "trp_player", "itm_gekokujo_wakizashi_1", 0),

(else_try),
#(display_message, "str_wielded_item_reg3"),

(lt, "$g_attacker_drawn_weapon", "itm_tutorial_spear"),
(str_store_string, s9, "str_you_never_let_him_draw_his_weapon_still_it_looked_like_he_was_going_to_kill_you_take_his_sword_and_purse_i_suppose_he_was_trouble_but_its_not_good_for_an_establishment_to_get_a_name_as_a_place_where_men_are_killed"),

(assign, "$g_main_attacker_agent", 0),
(troop_add_gold, "trp_player", 50),
(troop_add_item, "trp_player", "itm_gekokujo_wakizashi_1", 0),
(call_script, "script_troop_change_relation_with_troop", "trp_player", "$g_talk_troop", -1),
(else_try),
(neg|agent_is_alive, "$g_main_attacker_agent"),
(str_store_string, s9, "str_well_id_say_that_he_started_it_that_entitles_you_to_his_sword_and_purse_i_suppose_have_a_drink_on_the_house_as_i_daresay_youve_saved_a_patron_or_two_a_broken_skull_still_i_hope_he_still_has_a_pulse_its_not_good_for_an_establishment_to_get_a_name_as_a_place_where_men_are_killed"),
(assign, "$g_main_attacker_agent", 0),
(troop_add_gold, "trp_player", 50),
(troop_add_item, "trp_player", "itm_gekokujo_wakizashi_1", 0),
(call_script, "script_troop_change_relation_with_troop", "trp_player", "$g_talk_troop", 1),
(try_end),
(troop_set_slot, "trp_hired_assassin", slot_troop_cur_center, -1),
],
"{!}{s9}", "player_duel_response", [
]],
#gekokujo get rid of the no ranged weapons rule
#[anyone, "start", [
#(is_between, "$g_talk_troop", tavernkeepers_begin, tavernkeepers_end),
#(gt, "$g_main_attacker_agent", 0),
#(try_begin),
#(get_player_agent_no, ":player_agent"),
#(agent_get_wielded_item, ":wielded_item", ":player_agent", 0),
#(is_between, ":wielded_item", "itm_gekokujo_practice_jo", "itm_gekokujo_practice_kunai"),
#(neq, ":wielded_item", "itm_gekokujo_practice_yumi"),
#(str_store_string, s9, "str_stop_no_shooting_no_shooting"),

#(assign, ":default_item", -1),
#(troop_get_inventory_capacity, ":end_cond", "trp_player"),
#(try_for_range, ":i_slot", 0, ":end_cond"),
#(troop_get_inventory_slot, ":item_id", "trp_player", ":i_slot"),

#(is_between, ":item_id", weapons_begin, weapons_end),
#(neg|is_between, ":item_id", ranged_weapons_begin, ranged_weapons_end),

#(assign, ":default_item", ":item_id"),
#(assign, ":end_cond", 0), #break
#(try_end),

#(agent_set_wielded_item, ":player_agent", ":default_item"),
#(else_try),
#(str_store_string, s9, "str_em_ill_stay_out_of_this"),
#(try_end),
#],
#"{!}{s9}", "close_window", [
#]],

[anyone|plyr, "player_duel_response", [],
"Such a waste...", "close_window", [
]],
[anyone|plyr, "player_duel_response", [],
"Better him than me", "close_window", [
]],
[anyone|plyr, "drunk_response", [],
"I'm not sure... Some sort of animal, clearly", "drunk_fight_start", [
]],
[anyone|plyr, "drunk_response", [],
##diplomacy start+ Change this so there is some chance of success
#to avoid a fight.
##OLD:
#"Excuse me -- please accept my apologies", "drunk_fight_start", [
#]],
##NEW:
"Excuse me -- please accept my apologies", "dplmc_drunk_attempt_placate", [
]],
##diplomacy end+

[anyone, "drunk_fight_start", [],
"I'll wipe that smirk right off your face!", "close_window", [
(troop_set_slot, "trp_belligerent_drunk", slot_troop_cur_center, 0),
]],
[anyone|plyr, "drunk_response",
[
##diplomacy start+
#In Native this only shows up when it is guaranteed to succeed, but that
#isn't particularly interesting.
##REMOVED:
#(troop_slot_ge, "trp_player", slot_troop_renown, 150),
##diplomacy end+
],
"Do you have any idea who I am?", "drunk_player_high_renown", [
]],
[anyone, "drunk_player_high_renown", [
##diplomacy start+ Failure is also possible because you can get to this line with insufficient renown
(this_or_next|neg|troop_slot_ge, "trp_player", slot_troop_renown, 150),
##diplomacy end+
(eq, "$g_talk_troop", "trp_hired_assassin"),
],
"Do I care?", "drunk_fight_start", [
]],
##diplomacy start+ If prejudice is high, possibly increase the renown threshold required
[anyone, "drunk_player_high_renown", [
   (lt, "$g_disable_condescending_comments", 0),#prejudice mode: high
   (call_script, "script_cf_dplmc_faction_has_bias_against_gender", "$g_encountered_party_faction", "$character_gender"),
   (neg|troop_slot_ge, "trp_player", slot_troop_renown, 300),
],
"Big talk from a little runt.  I'll put you in your place!", "drunk_fight_start", [
]],
##diplomacy end+

[anyone, "drunk_player_high_renown", [
##diplomacy start+ change to use script_dplmc_print_subordinate_says_sir_madame_to_s0
(call_script, "script_dplmc_print_subordinate_says_sir_madame_to_s0"),
##diplomacy end+
],
##diplomacy start+ change to use script_dplmc_print_subordinate_says_sir_madame_to_s0
"Emmm... Actually... Yes, yes, I do know who you are, {s0}. Please forgive me, {playername}-dono -- it must be the drink. I'll be leaving, now...", "drunk_player_high_renown", [
##diplomacy end+
]],
[anyone|plyr, "drunk_player_high_renown", [],
"Why, if you want a fight, you shall have one!", "drunk_fight_start", [
]],
[anyone|plyr, "drunk_player_high_renown", [],
"I thought as much. Now, remove yourself from here", "close_window",
[
(assign, "$drunks_dont_pick_fights", 1),
(troop_set_slot, "trp_belligerent_drunk", slot_troop_cur_center, 0),

(call_script, "script_deactivate_tavern_attackers"),

(assign, "$g_belligerent_drunk_leaving", "$g_main_attacker_agent"),

(mission_enable_talk),

(try_for_agents, ":agent"),
 (agent_is_alive, ":agent"),
 (agent_get_position, pos4, ":agent"),
 (agent_set_scripted_destination, ":agent", pos4),
(try_end),

(entry_point_get_position, pos1, 0),
(agent_set_scripted_destination, "$g_main_attacker_agent", pos1),

(assign, "$g_main_attacker_agent", 0),
]],
[anyone, "start",
[
(eq, "$g_talk_troop", "trp_fight_promoter"),
],
"You look like someone who can take a few hard knocks -- and deal them out, too. I have a business proposition for you.", "fistfight_response", [
]],
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
[trp_ramun_the_slave_trader, "start", [
(troop_slot_eq, "$g_talk_troop", slot_troop_met_previously, 0),
], "Good day to you, {young man/lassie}.", "ramun_introduce_1",[]],
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
[trp_ramun_the_slave_trader,"start", [], "Hello, {playername}.", "ramun_talk",[]],
[trp_ramun_the_slave_trader,"ramun_pre_talk", [], "Anything else?", "ramun_talk",[]],
[trp_ramun_the_slave_trader|plyr,"ramun_talk",
[[store_num_regular_prisoners,reg(0)],[ge,reg(0),1]],
"I've brought you some prisoners, Tuo-yi. Would you like a look?", "ramun_sell_prisoners",[]],
##diplomacy start+
#Sell all prisoneers, a la rubik's Custom Commander, except when you are asked
#to confirm he tells you the number/price.
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
##diplomacy end+
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
[trp_nurse_for_lady, "start", [
#  (eq, "$talk_context", tc_garden),
##diplomacy start+ just in case make gender-correct
], "I humbly request that your {lordship/ladyship} keeps {his/her} hands where I can see them.", "close_window",[]],
##diplomacy end+

##  [trp_tutorial_trainer, "start", [(eq, "$tutorial_1_state", 1),], "TODO: Watch me.", "tutorial_1_1_1",[]],
##  [trp_tutorial_trainer, "tutorial_1_1_1", [], "TODO: This is up.", "tutorial_1_1_2",[(agent_set_attack_action, "$g_talk_agent", 3),]],
##  [trp_tutorial_trainer, "tutorial_1_1_2", [], "TODO: This is left.", "tutorial_1_1_3",[(agent_set_attack_action, "$g_talk_agent", 2),]],
##  [trp_tutorial_trainer, "tutorial_1_1_3", [], "TODO: This is right.", "tutorial_1_1_4",[(agent_set_attack_action, "$g_talk_agent", 1),]],
##  [trp_tutorial_trainer|plyr, "tutorial_1_1_4", [], "TODO: OK.", "close_window",[]],


#old tutorial is below

##  [trp_tutorial_trainer,"start", [(eq, "$tutorial_quest_award_taken", 1),], "I think you have trained enough. Perhaps you should go to Zendar for the next step of your adventure.", "close_window",[]],
##  [trp_tutorial_trainer,"start", [(store_character_level, ":player_level", "trp_player"),(gt, ":player_level", 1)], "I think you have trained enough. Perhaps you should go to Zendar for the next step of your adventure.", "close_window",[]],
##  [trp_tutorial_trainer,"start", [(eq, "$tutorial_quest_taken", 0),], "Greetings stranger. What's your name?", "tutorial1_1",[]],
##  [trp_tutorial_trainer|plyr, "tutorial1_1", [], "Greetings sir, it's {playername}.", "tutorial1_2", []],
##  [trp_tutorial_trainer, "tutorial1_2", [], "Well {playername}, this place you see is the training ground. Locals come here to practice their combat skills. Since you are here you may have a go as well.", "tutorial1_3", []],
##  [trp_tutorial_trainer|plyr, "tutorial1_3", [], "I'd like that very much sir. Thank you.", "tutorial1_4", []],
##  [trp_tutorial_trainer, "tutorial1_4", [], "You will learn the basics of weapons and riding a horse here.\
##  First you'll begin with melee weapons. Then you'll enter an archery range to test your skills. And finally you'll see a horse waiting for you.\
##  I advise you to train in all these 3 areas. But you can skip some of them, it's up to you.", "tutorial1_6", []],
##  [trp_tutorial_trainer, "tutorial1_6", [], "Tell you what, if you destroy at least 10 dummies while training, I will give you my old knife as a reward. It's a little rusty but it's a good blade.", "tutorial1_7", []],
##  [trp_tutorial_trainer|plyr, "tutorial1_7", [], "Sounds nice, I'm ready for training.", "tutorial1_9", []],
##  [trp_tutorial_trainer, "tutorial1_9", [], "Good. Return to me when you have earned your reward.", "close_window", [(eq, "$tutorial_quest_taken", 0),
##                                                                                                                     (str_store_troop_name, 1, "trp_tutorial_trainer"),
##                                                                                                                     (str_store_party_name, 2, "p_training_ground"),
##                                                                                                                     (setup_quest_giver, "qst_destroy_dummies", "str_given_by_s1_at_s2"),
##                                                                                                                     (str_store_string, s2, "@Trainer ordered you to destroy 10 dummies in the training camp."),
##                                                                                                                     (call_script, "script_start_quest", "qst_destroy_dummies", "$g_talk_troop"),
##                                                                                                                     (assign, "$tutorial_quest_taken", 1)]],
##
##  [trp_tutorial_trainer,"start", [(eq, "$tutorial_quest_taken", 1),
##                                  (eq, "$tutorial_quest_succeeded", 1),], "Well done {playername}. Now you earned this knife. There you go.", "tutorial2_1",[]],
##  [trp_tutorial_trainer|plyr, "tutorial2_1", [], "Thank you master.", "close_window", [(call_script, "script_end_quest", "qst_destroy_dummies"),(assign, "$tutorial_quest_award_taken", 1),(add_xp_to_troop, 100, "trp_player"),(troop_add_item, "trp_player","itm_knife",imod_chipped),]],
##
##  [trp_tutorial_trainer,"start", [(eq, "$tutorial_quest_taken", 1),
##                                  (eq, "$tutorial_quest_succeeded", 1),], "Greetings {playername}. Feel free to train with the targets.", "tutorial2_1",[]],
##
##  [trp_tutorial_trainer,"start", [(eq, "$tutorial_quest_taken", 1),
##                                  (eq, "$tutorial_quest_succeeded", 0),], "I don't see 10 dummies on the floor from here. You haven't earned your reward yet.", "tutorial3_1",[]],
##  [trp_tutorial_trainer|plyr, "tutorial3_1", [], "Alright alright, I was just tired and wanted to talk to you while resting.", "tutorial3_2", []],
##  [trp_tutorial_trainer, "tutorial3_2", [], "Less talk, more work.", "close_window", []],


##  [party_tpl|pt_peasant,"start", [(eq,"$talk_context",tc_party_encounter)], "Greetings traveller.", "peasant_talk_1",[(play_sound,"snd_encounter_farmers")]],
##  [party_tpl|pt_peasant|plyr,"peasant_talk_1", [[eq,"$quest_accepted_zendar_looters"]], "Greetings to you too.", "close_window",[(assign, "$g_leave_encounter",1)]],
##  [party_tpl|pt_peasant|plyr,"peasant_talk_1", [[neq,"$quest_accepted_zendar_looters"],[eq,"$peasant_misunderstanding_said"]], "I have been charged with hunting down outlaws in this area...", "peasant_talk_2",[[assign,"$peasant_misunderstanding_said",1]]],
##  [party_tpl|pt_peasant|plyr,"peasant_talk_1", [[neq,"$quest_accepted_zendar_looters"],[neq,"$peasant_misunderstanding_said"]], "Greetings. I am hunting outlaws. Have you seen any around here?", "peasant_talk_2b",[]],
##  [party_tpl|pt_peasant,"peasant_talk_2", [], "I swear to God {sir/madam}. I am not an outlaw... I am just a simple peasant. I am taking my goods to the market, see.", "peasant_talk_3",[]],
##  [party_tpl|pt_peasant|plyr,"peasant_talk_3", [], "I was just going to ask if you saw any outlaws around here.", "peasant_talk_4",[]],
##  [party_tpl|pt_peasant,"peasant_talk_4", [], "Oh... phew... yes, outlaws are everywhere. They are making life miserable for us.\
## I pray to God you will kill them all.", "close_window",[(assign, "$g_leave_encounter",1)]],
##  [party_tpl|pt_peasant,"peasant_talk_2b", [], "Outlaws? They are everywhere. They are making life miserable for us.\
## I pray to God you will kill them all.", "close_window",[(assign, "$g_leave_encounter",1)]],

[party_tpl|pt_manhunters,"start", [(eq,"$talk_context",tc_party_encounter)], "Hey, you there! You seen any bandits around here?", "manhunter_talk_b",[]],
[party_tpl|pt_manhunters|plyr,"manhunter_talk_b", [], "Yes, they went this way about an hour ago.", "manhunter_talk_b1",[]],
[party_tpl|pt_manhunters,"manhunter_talk_b1", [], "I knew it! Come on, boys, lets go get these bastards! Thanks a lot, friend.", "close_window",[(assign, "$g_leave_encounter",1)]],
[party_tpl|pt_manhunters|plyr,"manhunter_talk_b", [], "No, haven't seen any bandits lately.", "manhunter_talk_b2",[]],
[party_tpl|pt_manhunters,"manhunter_talk_b2", [], "Bah. They're holed up in this country like rats, but we'll smoke them out sooner or later.", "close_window",[(assign, "$g_leave_encounter",1)]],
[party_tpl|pt_looters|auto_proceed,"start", [(eq,"$talk_context",tc_party_encounter),(encountered_party_is_attacker),], "{!}Warning: This line should never be displayed.", "looters_1",[
(str_store_string, s11, "@It's your money or your life, {dono/hime}. No sudden moves or we'll run you through."),
(str_store_string, s12, "@Lucky for you, you caught me in a good mood. Give us all your valuables and I might just let you live."),
(str_store_string, s13, "@This a robbery, eh? I'm givin' you one chance to hand over everythin' you got, or we'll kill you. Understand?"),
(store_random_in_range, ":random", 11, 14),
#gekokujo 3.0 no more bandit talk start
(str_store_string_reg, s4, ":random")
#(str_store_string_reg, s4, ":random"),
#(play_sound, "snd_encounter_looters")
#gekokujo 3.0 no more bandit talk end
]],
[party_tpl|pt_looters,"looters_1", [], "{s4}", "looters_2",[]],
[party_tpl|pt_looters|plyr,"looters_2", [[store_character_level,reg(1),"trp_player"],[lt,reg(1),4]], "I'm not afraid of you. Come at me!", "close_window",
[[encounter_attack]]],
[party_tpl|pt_looters|plyr,"looters_2", [[store_character_level,reg(1),"trp_player"],[ge,reg(1),4]], "You'll have nothing of mine but cold steel.", "close_window",
[[encounter_attack]]],
[party_tpl|pt_village_farmers,"start", [(eq,"$talk_context",tc_party_encounter),
                                    (agent_play_sound, "$g_talk_agent", "snd_encounter_farmers"),
],
" My {lord/lady}, we're only poor farmers from the village of {s11}. {reg1?We are taking our products to the market at {s12}.:We are returning from the market at {s12} back to our village.}", "village_farmer_talk",
[(party_get_slot, ":target_center", "$g_encountered_party", slot_party_ai_object),
(party_get_slot, ":home_center", "$g_encountered_party", slot_party_home_center),
(party_get_slot, ":market_town", ":home_center", slot_village_market_town),
(str_store_party_name, s11, ":home_center"),
(str_store_party_name, s12, ":market_town"),
(assign, reg1, 1),
(try_begin),
(party_slot_eq, ":target_center", slot_party_type, spt_village),
(assign, reg1, 0),
(try_end),
]],
[anyone,"farmer_bandit_information", [
(call_script, "script_get_manhunt_information_to_s15", "qst_track_down_bandits"),
], "{s15}", "village_farmer_talk",[]],
### COMPANIONS

[anyone,"start", [(gt,"$g_talk_troop", 0),
              (eq, "$g_talk_troop", "$g_player_minister"),
		 ##diplomacy start+ Handle non-reflexive spouse slots (for example, for polygamy)
		 (this_or_next|neg|is_between, "$g_talk_troop", heroes_begin, heroes_end),#slot_troop_spouse may not be initialized to -1
			(neg|troop_slot_eq, "$g_talk_troop", slot_troop_spouse, "trp_player"),
		 ##diplomacy end+
         (neg|troop_slot_eq, "trp_player", slot_troop_spouse, "$g_talk_troop")],
"I am at your service, oyakata-sama", "minister_issues",[]],
[anyone,"start", [(eq,"$g_talk_troop", "trp_temporary_minister"),
              (neq, "$g_talk_troop", "$g_player_minister")],
"It has been an honor to serve you, oyakata-sama", "close_window",[]],
[anyone,"start", [(troop_slot_eq,"$g_talk_troop", slot_troop_occupation, slto_player_companion),
              (party_slot_eq, "$g_encountered_party", slot_party_type, spt_castle),
              (party_get_num_companion_stacks, ":num_stacks", "$g_encountered_party"),
              (ge, ":num_stacks", 1),
              (party_stack_get_troop_id, ":castle_leader", "$g_encountered_party", 0),
              (eq, ":castle_leader", "$g_talk_troop"),
              (eq, "$talk_context", 0)],
"Yes, {playername}-dono? What can I do for you?", "member_castellan_talk",[]],
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
[anyone,"start", [(troop_slot_eq,"$g_talk_troop", slot_troop_occupation, slto_player_companion),
              (neg|main_party_has_troop,"$g_talk_troop"),
              (eq, "$talk_context", tc_party_encounter)],
   "{!}Do you want me to rejoin you?", "close_window",[]],
 # unused
  [anyone,"start", [(neg|main_party_has_troop,"$g_talk_troop"),(eq, "$g_encountered_party", "p_four_ways_inn")], "{!}Do you want me to rejoin you?", "close_window",[]],
 # unused
#  [anyone,"member_separate_inn", [], "I don't know what you will do without me, but you are the boss. I'll wait for you at the Four Ways inn.", "close_window",
#  [anyone,"member_separate_inn", [], "All right then. I'll meet you at the four ways inn. Good luck.", "close_window",
#   [(remove_member_from_party,"$g_talk_troop", "p_main_party"),(add_troop_to_site, "$g_talk_troop", "scn_four_ways_inn", borcha_inn_entry)]],

#Quest heroes member chats

[trp_kidnapped_girl,"member_chat", [], "Are we home yet?", "kidnapped_girl_chat_1",[]],
[trp_kidnapped_girl|plyr,"kidnapped_girl_chat_1", [], "Not yet.", "kidnapped_girl_chat_2",[]],
[trp_kidnapped_girl,"kidnapped_girl_chat_2", [], "I can't wait to get back. I've missed my family so much, I'd give anything to see them again.", "close_window",[]],
[anyone|plyr, "member_lady_1", [],  "We still have a long way ahead of us.", "member_lady_2a", []],
[anyone|plyr, "member_lady_1", [],  "Very soon. We're almost there.", "member_lady_2b", []],
[anyone ,"member_lady_2a", [],  "Ah, I am going to enjoy the road for a while longer then. I won't complain.\
I find riding out in the open so much more pleasant than sitting in the castle all day.\
You know, I envy you. You can live like this all the time.", "close_window", []],
[anyone ,"member_lady_2b", [],  "That's good news. Not that I don't like your company, but I did miss my little luxuries.\
Still I am sorry that I'll leave you soon. You must promise me, you'll come visit me when you can.", "close_window", []],
[anyone ,"supported_pretender_pretalk", [],
"Anything else?", "supported_pretender_talk", []],
[anyone|plyr,"supported_pretender_talk", [],
"What do you think about our progress so far?", "pretender_progress",[]],
[anyone,"pretender_progress", [
 (assign, reg11, 0),(assign, reg13, 0),(assign, reg14, 0),(assign, reg15, 0),
 (assign, reg21, 0),(assign, reg23, 0),(assign, reg24, 0),(assign, reg25, 0),

 (try_for_range, ":troop_no", active_npcs_begin, active_npcs_end),
  (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
   (store_troop_faction, ":troop_faction", ":troop_no"),
   (try_begin),
     (eq, ":troop_faction", "fac_player_supporters_faction"),
     (neq, ":troop_no", "trp_player"),
     (neq, ":troop_no", "$supported_pretender"),
     (val_add, reg11, 1),
   (else_try),
     (eq, ":troop_faction", "$supported_pretender_old_faction"),
     (neg|faction_slot_eq, "$supported_pretender_old_faction", slot_faction_leader, ":troop_no"),
     (val_add, reg21, 1),
   (try_end),
 (try_end),
 (try_for_range, ":center_no", centers_begin, centers_end),
   (store_faction_of_party, ":center_faction", ":center_no"),
   (try_begin),
     (eq, ":center_faction", "fac_player_supporters_faction"),
     (try_begin),
       (party_slot_eq, ":center_no", slot_party_type, spt_town),
       (val_add, reg13, 1),
     (else_try),
       (party_slot_eq, ":center_no", slot_party_type, spt_castle),
       (val_add, reg14, 1),
     (else_try),
       (party_slot_eq, ":center_no", slot_party_type, spt_village),
       (val_add, reg15, 1),
     (try_end),
   (else_try),
     (eq, ":center_faction", "$supported_pretender_old_faction"),
     (try_begin),
       (party_slot_eq, ":center_no", slot_party_type, spt_town),
       (val_add, reg23, 1),
     (else_try),
       (party_slot_eq, ":center_no", slot_party_type, spt_castle),
       (val_add, reg24, 1),
     (else_try),
       (party_slot_eq, ":center_no", slot_party_type, spt_village),
       (val_add, reg25, 1),
     (try_end),
   (try_end),
 (try_end),
 (store_add, reg19, reg13, reg14),
 (val_add, reg19, reg15),
 (store_add, reg29, reg23, reg24),
 (val_add, reg29, reg25),
 (store_add, ":our_score", reg13, reg14),
 (val_add, ":our_score", reg11),
 (store_add, ":their_score", reg23, reg24),
 (val_add, ":their_score", reg21),
 (store_add, ":total_score", ":our_score", ":their_score"),
 (val_mul, ":our_score", 100),
 (store_div, ":our_ratio", ":our_score", ":total_score"),
 (try_begin),
   (lt, ":our_ratio", 10),
   (str_store_string, s30, "@we have made very little progress so far"),
 (else_try),
   (lt, ":our_ratio", 30),
   (str_store_string, s30, "@we have suceeded in gaining some ground, but we still have a long way to go"),
 (else_try),
   (lt, ":our_ratio", 50),
   (str_store_string, s30, "@we have become a significant force, and we have an even chance of victory"),
 (else_try),
   (lt, ":our_ratio", 75),
   (str_store_string, s30, "@we are winning the war, but our enemies are still holding on."),
 (else_try),
   (str_store_string, s30, "@we are on the verge of victory. The remaining enemies pose no threat, but we still need to hunt them down."),
 (try_end),
 (faction_get_slot, ":enemy_king", "$supported_pretender_old_faction", slot_faction_leader),
 (str_store_troop_name, s9, ":enemy_king"),
##diplomacy start+: Replace "lords" with "{s0}"; "no lord" with "no {s0}"; and use correct gender for enemy king
(call_script, "script_dplmc_print_cultural_word_to_sreg", "$g_talk_troop", DPLMC_CULTURAL_TERM_LORD_PLURAL, 0),
(call_script, "script_dplmc_store_troop_is_female", ":enemy_king"),
],
##OLD:
#"{reg11?We have {reg11} lords on our side:We have no lord with us yet},\
#whereas {reg21?{s9} still has {reg21} lords supporting him:{s9} has no loyal lords left}.\
#{reg19?We control {reg13?{reg13} towns:} {reg14?{reg14} castles:} {reg15?and {reg15} villages:}:We don't control any settlements},\
#while {reg29?they have {reg23?{reg23} towns:} {reg24?{reg24} castles:} {reg25?and {reg25} villages:}:they have no remaining settlements}.\
#Overall, {s30}.", "pretender_progress_2",[]],
##NEW:
"{reg11?We have {reg11} {s0} on our side:We have no {s0} with us yet},\
whereas {reg21?{s9} still has {reg21} {s0} supporting {reg0?her:him}:{s9} has no loyal {s0} left}.\
{reg19?We control {reg13?{reg13} towns:} {reg14?{reg14} castles:} {reg15?and {reg15} villages:}:We don't control any settlements},\
while {reg29?they have {reg23?{reg23} towns:} {reg24?{reg24} castles:} {reg25?and {reg25} villages:}:they have no remaining settlements}.\
Overall, {s30}.", "pretender_progress_2",[]],
##diplomacy end+

[anyone|plyr,"pretender_progress_2", [],
"Then, we must keep fighting and rally our supporters!", "supported_pretender_pretalk",[]],
[anyone|plyr,"pretender_progress_2", [],
"It seems this rebellion is not going anywhere. We must give up.", "pretender_quit_rebel_confirm",[]],
[anyone,"pretender_quit_rebel_confirm", [],
"{playername}, you can't abandon me now. Are you serious?", "pretender_quit_rebel_confirm_2",[]],
[anyone|plyr,"pretender_quit_rebel_confirm_2", [],
"Indeed, I am. I can't support you any longer.", "pretender_quit_rebel_confirm_3",[]],
[anyone|plyr,"pretender_quit_rebel_confirm_2", [],
"I was joking. I will fight for you until we win.", "supported_pretender_pretalk",[]],
[anyone,"pretender_quit_rebel_confirm_3", [],
"Are you absolutely sure? I will never forgive you if you abandon my cause.", "pretender_quit_rebel_confirm_4",[]],
[anyone|plyr,"pretender_quit_rebel_confirm_4", [],
"I am sure.", "pretender_quit_rebel",[]],
[anyone|plyr,"pretender_quit_rebel_confirm_4", [],
"Let me think about this some more.", "supported_pretender_pretalk",[]],
[anyone,"pretender_quit_rebel", [],
"So be it. Then my cause is lost. There is only one thing to do for me now. I will go from Japan and never come back. With me gone, you may try to make your peace with {s4}.", "close_window",
[
(troop_get_slot, ":original_faction", "$g_talk_troop", slot_troop_original_faction),
(faction_get_slot, ":original_faction_leader", ":original_faction", slot_faction_leader),
(str_store_troop_name, s4, ":original_faction_leader"),

##diplomacy start+ Support promoted kingdom ladies
#(try_for_range, ":cur_troop", active_npcs_begin, active_npcs_end),##OLD
(try_for_range, ":cur_troop", heroes_begin, heroes_end),##NEW
##diplomacy end+
(troop_slot_eq, ":cur_troop", slot_troop_occupation, slto_kingdom_hero),
(neq, "$supported_pretender", ":cur_troop"),
 (store_troop_faction, ":cur_faction", ":cur_troop"),
 (eq, ":cur_faction", "fac_player_supporters_faction"),
 (call_script, "script_change_troop_faction", ":cur_troop", ":original_faction"),
(try_end),
(troop_set_faction, "$g_talk_troop", "fac_neutral"),
(faction_set_slot, "fac_player_supporters_faction", slot_faction_leader, "trp_player"),
(assign, ":has_center", 0),
(try_for_range, ":cur_center", centers_begin, centers_end),
 (store_faction_of_party, ":cur_faction", ":cur_center"),
 (eq, ":cur_faction", "fac_player_supporters_faction"),
 (assign, ":has_center", 1),
 (neg|party_slot_eq, ":cur_center", slot_town_lord, "trp_player"),
 (call_script, "script_give_center_to_lord", ":cur_center", "trp_player", 0),
(try_end),
(party_remove_members, "p_main_party", "$supported_pretender", 1),
(faction_set_slot, ":original_faction", slot_faction_has_rebellion_chance, 0),
(assign, "$supported_pretender", 0),
(try_begin), #Still has center
 (eq, ":has_center", 1),
 (faction_set_color, "fac_player_supporters_faction", 0xFF0000),
(try_begin), #added to prevent no minister if player gives up rebellion
(eq, "$g_player_minister", 0),
(assign, "$g_player_minister", "trp_temporary_minister"),
(try_end),
(else_try), #No center
 (call_script, "script_deactivate_player_faction"),
(try_end),
(call_script, "script_change_player_honor", -20),
(call_script, "script_fail_quest", "qst_rebel_against_kingdom"),
(call_script, "script_end_quest", "qst_rebel_against_kingdom"),
]],
[anyone|plyr,"supported_pretender_talk", [],
"{reg65?My lady:My lord}, would you allow me to check out your equipment?", "supported_pretender_equip",[]],
[anyone,"supported_pretender_equip", [], "Very well, it's all here...", "supported_pretender_pretalk",[
(change_screen_equip_other),
]],
[anyone|plyr,"supported_pretender_talk", [], "If it would please you, can you tell me about your skills?", "pretneder_view_char_requested",[]],
[anyone,"pretneder_view_char_requested", [], "Well, all right.", "supported_pretender_pretalk",[(change_screen_view_character)]],
[anyone|plyr,"supported_pretender_talk", [
##diplomacy start+ Handle player is co-ruler of NPC kingdom
(assign, ":alt_faction", "fac_player_supporters_faction"),
(try_begin),
	(is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
	(call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", "$players_kingdom"),
	(ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
	(assign, ":alt_faction", "$players_kingdom"),
(try_end),
##diplomacy end+
(assign, ":center_found", 0),
(try_for_range, ":fief_to_grant", centers_begin, centers_end),
(store_faction_of_party, ":fief_faction", ":fief_to_grant"),
##diplomacy start+
(this_or_next|eq, ":fief_faction", ":alt_faction"),
##diplomacy end+
(eq, ":fief_faction", "fac_player_supporters_faction"),
(party_slot_eq, ":fief_to_grant", slot_town_lord, -1),
(assign, ":center_found", 1),
(try_end),
(eq, ":center_found", 1),

],
"I suggest that you decide who should hold a fief that does not have a lord.", "supported_pretender_grant_fief",[]],
[anyone,"supported_pretender_grant_fief", [
],
"Which fief did you have in mind?", "supported_pretender_grant_fief_select",[]],
[anyone|plyr|repeat_for_parties,"supported_pretender_grant_fief_select", [
(store_repeat_object, ":fief_to_grant"),
(is_between, ":fief_to_grant", centers_begin, centers_end),
(store_faction_of_party, ":fief_faction", ":fief_to_grant"),
##diplomacy start+ Handle player is co-ruler of NPC kingdom
(assign, ":alt_faction", "fac_player_supporters_faction"),
(try_begin),
	(is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
	(call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", "$players_kingdom"),
	(ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
	(assign, ":alt_faction", "$players_kingdom"),
(try_end),
(this_or_next|eq, ":fief_faction", ":alt_faction"),
##diplomacy end+
(eq, ":fief_faction", "fac_player_supporters_faction"),
(party_slot_eq, ":fief_to_grant", slot_town_lord, -1),
(str_store_party_name, s4, ":fief_to_grant"),
],
"{s4}", "supported_pretender_grant_fief_choose_recipient",[
(store_repeat_object, "$g_center_taken_by_player_faction"),
]],
[anyone,"supported_pretender_grant_fief_choose_recipient", [
],
"And who should receive it?", "center_captured_rebellion",[
(str_store_party_name, s4, "$g_center_taken_by_player_faction"),
]],
[anyone|plyr,"supported_pretender_grant_fief_select", [
],
"Never mind.", "supported_pretender_pretalk",[]],
[anyone|plyr,"supported_pretender_talk", [],
"Let us keep going, {reg65?my lady:sir}.", "close_window",[]],
[anyone,"do_member_trade", [], "Anything else?", "member_talk",[]],
[anyone,"member_pretalk", [], "Anything else?", "member_talk",[]],
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
[anyone,"do_member_trade", [], "Anything else?", "member_talk",[]],
[anyone|plyr,"member_talk", [], "What can you tell me about your skills?", "view_member_char_requested",[]],
[anyone,"view_member_char_requested", [], "All right, let me tell you...", "do_member_view_char",[(change_screen_view_character)]],
[anyone|plyr,"member_talk", [], "We need to separate for a while.", "member_separate",[
      (call_script, "script_npc_morale", "$g_talk_troop"),
      (assign, "$npc_quit_morale", reg0),
]],
##diplomacy start+
#Kingdom hero leaves party
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
##diplomacy end+

#gekokujo 3.0 microfactions! start
#separation for fort companions is slightly different
[anyone,"member_separate", [
    (is_between, "$g_talk_troop", fort_companions_begin, fort_companions_end),
  ], "If you want us to separate for a while, I shall go back home and wait for you. Is that what you want?", "member_separate_confirm", []],
#gekokujo 3.0 microfactions! end

#gekokujo 3.1 bogmir's quests start
#####################################################################################################
  [trp_smithy_master, "start", [],"Good day {sir/madam}, will you be looking at my weapons?", "smithy_master_talk", []],
  [trp_smithy_master|plyr, "smithy_master_talk", [], "Yes. Show me what you have for sale.", "smithy_master_buy", []],
   
  [trp_smithy_master,"smithy_master_buy", [], "Of course {sir/madam}.", "smithy_trade_completed",[[change_screen_trade]]],
  [trp_smithy_master,"smithy_trade_completed", [], "Anything else?", "smithy_master_talk",[]],
  [trp_smithy_master|plyr, "smithy_master_talk", [(troop_has_item_equipped,"trp_player","itm_calradia_broken_sword")], "You can reforge the sword?", "smithy_sword_1", []],
  [trp_smithy_master,"smithy_sword_1", [], "Show that you have.", "smithy_sword_2",[]],
  [trp_smithy_master|plyr, "smithy_sword_2", [], "Here.", "smithy_sword_3",[(troop_remove_item, "trp_player","itm_calradia_broken_sword")]],
  [trp_smithy_master,"smithy_sword_3", [], "Mmm.. good steel, I can reforge, but I need more iron. Bring me oil and iron.", "smithy_sword_4",
  [
    (str_store_string, s2, "str_find_some_iron"),
    (call_script, "script_start_quest", "qst_find_iron_for_reforge", "trp_smithy_master"),
  ]],
  [trp_smithy_master|plyr,"smithy_sword_4", [], "Thanks.", "close_window",[]],
  [trp_smithy_master|plyr, "smithy_master_talk",
  [
    (check_quest_active, "qst_find_iron_for_reforge"),
    (player_has_item, "itm_oil"),
    (player_has_item, "itm_iron"),
  ],
  "I'm find materials.", "iron_for_smith", []],
  [trp_smithy_master, "iron_for_smith", [], "Great, give me materials.", "iron_for_smith_1", 
  [
   (troop_remove_item, "trp_player", "itm_oil"),
   (troop_remove_item, "trp_player", "itm_iron"),
   ]],
  [trp_smithy_master|plyr,"iron_for_smith_1", [], "Sword reforged?", "iron_for_smith_2",[]],
  [trp_smithy_master,"iron_for_smith_2", [], "Oh... yes, take your sword.", "close_window",
  [
    (troop_add_item, "trp_player","itm_calradia_steel_sword",imod_tempered),
    (add_xp_as_reward, 500),
    (call_script, "script_succeed_quest", "qst_find_iron_for_reforge"),
    (call_script, "script_end_quest", "qst_find_iron_for_reforge"),
  ]],
  [trp_smithy_master|plyr,"smithy_master_talk", [], "Nothing. Thanks.", "close_window",[]],
#####################################################################################################
  [trp_black_swordsman,"start",[[eq,"$brok_sword",0]],"Hello, stranger.", "swordmaster_talk",[]],
  [trp_black_swordsman|plyr,"swordmaster_talk", [], "Hello, who are you?", "swordmaster_talk_2",[]],
  [trp_black_swordsman|plyr, "swordmaster_talk", [], "Please forgive me, I'll be leaving, now...", "close_window",[]],
  [trp_black_swordsman,"swordmaster_talk_2",[],"I wandering warrior, You can help me?", "swordmaster_talk_3",[]],
  [trp_black_swordsman|plyr, "swordmaster_talk_3", [], "Help?", "swordmaster_talk_4",[]],
  [trp_black_swordsman,"swordmaster_talk_4",[],"Yes, my old sword is broken in last battle, you can restore it?", "swordmaster_talk_5",[]],
  [trp_black_swordsman|plyr, "swordmaster_talk_5", [], "Hmm. I'll think about it.", "close_window",[[assign,"$brok_sword",1]]],
  [trp_black_swordsman,"start", [[eq,"$brok_sword",1]], "Hello, {playername}.That you decide?", "swordmaster_help",[]],
  [trp_black_swordsman|plyr,"swordmaster_help", [], "Think, I can help.", "swordmaster_help_2",[]],
  [trp_black_swordsman|plyr, "swordmaster_help", [], "Later.", "close_window",[]],
  [trp_black_swordsman,"swordmaster_help_2", [], "Great! Heh, well, this must be my lucky day.Here, take my sword.","swordmaster_help_3",[(troop_add_item, "trp_player","itm_calradia_broken_sword")]],
  [trp_black_swordsman|plyr,"swordmaster_help_3", [], "I'd better be going.", "close_window",[[assign,"$brok_sword",2]]],
  [trp_black_swordsman, "start", [[eq,"$brok_sword",2]], "Did you find the sword?","sword_restored",[]],
  [trp_black_swordsman|plyr, "sword_restored", [(player_has_item,"itm_calradia_steel_sword")], "Yes! It was quite difficult.", "sword_restored_1",[(troop_remove_item, "trp_player","itm_calradia_steel_sword")]],
  [trp_black_swordsman,"sword_restored_1",[],"Yes, my old sword, thanks man.", "sword_restored_2",
   [   
     (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 7),
     (add_xp_as_reward, 2000),
     (call_script, "script_troop_add_gold", "trp_player", 500),
     ]],
  [trp_black_swordsman|plyr,"sword_restored_2",[],"A pleasure doing business with you, goodbye.", "close_window",[[assign,"$brok_sword",3]]],
  [trp_black_swordsman|plyr, "sword_restored", [], "No, not yet.", "close_window",[]],
#####################################################################################################
  [trp_black_swordsman, "start", [(eq,"$brok_sword",3)], "What?","black_question",[]],
  [trp_black_swordsman|plyr, "black_question", [(neg|main_party_has_troop, "$g_talk_troop")], "Join to my party.", "black_question_1",[]],
  [trp_black_swordsman|plyr, "black_question", [], "Nothing, go", "close_window",[]],
  [trp_black_swordsman,"black_question_1",[(hero_can_join,"p_main_party")],"I am at your service, {sire/my lady}.", "close_window",[
       (assign, "$g_move_heroes", 1),
       (call_script, "script_recruit_troop_as_companion", "$g_talk_troop"),
       ]],
  [trp_black_swordsman,"black_question_1",[(neg|hero_can_join, "p_main_party")], "Not place in your party for me.", "close_window",[]],
#####################################################################################################
#gekokujo 3.1 bogmir's quests end

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
[anyone,"do_member_view_char", [], "Anything else?", "member_talk",[]],
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
[anyone|auto_proceed, "start",
[
(is_between, "$g_talk_troop", "trp_tsu_merchant", "trp_startup_merchants_end"),
(eq, "$talk_context", tc_town_talk),
],
"{!}.", "merchant_quest_4_start",
[
]],
[anyone, "start",
[
(is_between, "$g_talk_troop", "trp_relative_of_merchant", "trp_relative_of_merchants_end"),

(try_begin),
(check_quest_active, "qst_save_relative_of_merchant"),
(call_script, "script_succeed_quest", "qst_save_relative_of_merchant"),
(try_end),

(str_store_party_name, s9, "$g_starting_town"),

(assign, "$relative_of_merchant_is_found", 1),
],
"Thank you! Thank you, stranger, for rescuing me from those fiends. I can return to {s9} on my own -- let me just pick up one of these weapons conveniently dropped on the ground, heh.", "relative_saved_1a",
[
]],
[anyone|plyr, "relative_saved_1a",
[],
"Horenbo? Your brother hired me to find and rescue you. I'm a little surprised -- he didn't say anything about you being a monk.", "relative_saved_1b",
[
]],
[anyone, "relative_saved_1b",
[
(str_store_party_name, s9, "$g_starting_town"),
],
"Brother? I don't have a brother, haha. My friend, I believe someone in {s9} owes you an explanation. As for me, off I go!", "relative_saved_1c",
[
]],
[anyone|plyr, "relative_saved_1c",
[],
"...", "close_window",
[
]],
[anyone, "start",
[
(is_between, "$g_talk_troop", "trp_rebel_leader", "trp_bandit_leaders_end"),
(eq,"$talk_context",tc_hero_defeated),

(party_get_slot, ":town_lord", "$g_starting_town", slot_town_lord),
(str_store_troop_name, s4, ":town_lord"),
],
"How dare you! I am a key vassal of {s4}!", "bandit_leader_1a",
[]],
[anyone,"start",
[
(eq,"$talk_context",tc_party_encounter),
(is_between, "$g_talk_troop", "trp_rebel_leader", "trp_bandit_leaders_end"),
],
"Who are you? Why are you talking to me?", "looter_leader_1",
[]],
[anyone|plyr,"looter_leader_1",
[
(store_faction_of_party, ":starting_town_faction", "$g_starting_town"),
(try_begin),
(eq, ":starting_town_faction", "fac_kingdom_11"),
(assign, ":troop_of_merchant", "trp_tsu_merchant"),
(else_try),
(eq, ":starting_town_faction", "fac_kingdom_10"),
(assign, ":troop_of_merchant", "trp_hirosaki_merchant"),
(else_try),
(eq, ":starting_town_faction", "fac_kingdom_1"),
(assign, ":troop_of_merchant", "trp_niigata_merchant"),
(else_try),
(eq, ":starting_town_faction", "fac_kingdom_13"),
(assign, ":troop_of_merchant", "trp_edo_merchant"),
(else_try),
(eq, ":starting_town_faction", "fac_kingdom_7"),
(assign, ":troop_of_merchant", "trp_sakai_merchant"),
(else_try),
(eq, ":starting_town_faction", "fac_kingdom_9"),
(assign, ":troop_of_merchant", "trp_hakata_merchant"),
(try_end),

(str_store_troop_name, s9, ":troop_of_merchant"),
],
"I've been looking for you. Tell me who your lord is and where he lives, and I will let you go.", "looter_leader_2",
[]],
[anyone|plyr,"looter_leader_1",
[],
"Nothing. I apologize for getting in your way.", "close_window",
[
(assign, "$g_leave_encounter", 1),
]],
[anyone,"looter_leader_2",
[],
"Are you serious? You've just told me that you wanted to die.", "looter_leader_3",
[]],
[anyone|plyr,"looter_leader_3",
[],
"We shall see who dies today.", "close_window",
[]],
[anyone,"start", [
(troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_hero),
(check_quest_active, "qst_rescue_prisoner"),
(check_quest_succeeded, "qst_rescue_prisoner"),
(quest_slot_eq, "qst_rescue_prisoner", slot_quest_giver_troop, "$g_talk_troop"),
(quest_get_slot, ":cur_lord", "qst_rescue_prisoner", slot_quest_target_troop),
(call_script, "script_troop_get_family_relation_to_troop", ":cur_lord", "$g_talk_troop"),
],
##diplomacy start+ Use correct pronoun (family relation script wrote gender to reg4)
"{playername}, you saved {reg4?her:him}! Thank you ever so much for rescuing my {s11}.\
Please, take this as some small repayment for your noble deed.", "rescue_prisoner_succeed_2",
##diplomacy end+
[
(call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 8),
(add_xp_as_reward, 2000),
(call_script, "script_troop_add_gold", "trp_player", 1500),
(call_script, "script_end_quest", "qst_rescue_prisoner"),
]],
#Quest 0 - Alley talk
[anyone|auto_proceed, "start",
[
(is_between, "$g_talk_troop", "trp_tsu_merchant", "trp_startup_merchants_end"),
(eq, "$talk_context", tc_back_alley),
(eq, "$talked_with_merchant", 0),
],
"{!}.", "start_up_quest_1_next",
[]],
[anyone, "start_up_quest_1_next",
[],
"Are you all right? Well... I guess you're alive, at any rate. I'm not sure that we can say the same for the ronin. That's one less murderous maniac to trouble our streets, although the gods know he won't be the last... Anyway, maybe you can help me with something... Let's talk more inside. Out here, we don't know who's listening", "close_window",
[
(assign, "$talked_with_merchant", 1),
(mission_disable_talk),
]],
#Quest 1 - Repeating dialog sentence
[anyone|auto_proceed, "start",
[
(is_between, "$g_talk_troop", "trp_tsu_merchant", "trp_startup_merchants_end"),
(eq, "$talk_context", tc_tavern_talk),

(call_script, "script_party_count_members_with_full_health", "p_main_party"),
(assign, ":total_party_size", reg0),

(assign, ":continue", 0),
(try_begin),
(check_quest_active, "qst_collect_men"),
(neg|check_quest_succeeded, "qst_collect_men"),

(le, ":total_party_size", 4),

(try_begin),
  (le, ":total_party_size", 1),
  (str_store_string, s11, "str_please_sir_my_lady_go_find_some_volunteers_i_do_not_know_how_much_time_we_have"),
(else_try),
  (str_store_string, s11, "str_you_need_more_men_sir_my_lady"),
(try_end),
(assign, ":continue", 1),
(else_try),
(check_quest_active, "qst_learn_where_merchant_brother_is"),
(neg|check_quest_succeeded, "qst_learn_where_merchant_brother_is"),
(str_store_string, s11, "str_do_not_waste_time_go_and_learn_where_my_brother_is"),
(assign, ":continue", 1),
(try_end),
(eq, ":continue", 1),
],
"{!}.", "start_up_quest_2_next",
[]],
[anyone, "start_up_quest_2_next",
[],
"{!}{s11}", "close_window",
[]],
#Quest 2 - First dialog sentence
[anyone, "start",
[
(is_between, "$g_talk_troop", "trp_tsu_merchant", "trp_startup_merchants_end"),
(eq, "$talk_context", tc_tavern_talk),

(check_quest_active, "qst_collect_men"),
(neg|check_quest_succeeded, "qst_duel_for_lady"),
(call_script, "script_party_count_members_with_full_health", "p_main_party"),
(ge, reg0, 5),

(str_store_party_name, s9, "$current_town"),
],
"Excellent. You have hired enough men to take on any country samurai, especially if they don't know you're coming. Now -- travellers entering {s9} have told us that there is one waiting outside of town, with a small group of retainers. I peeked at them myself and I am certain that this one is employed by the same people that that took Horenbo. Hunt him down and defeat him, and make him disclose the location of his master!", "merchant_quest_2a",
[
(call_script, "script_succeed_quest", "qst_collect_men"),
(call_script, "script_end_quest", "qst_collect_men"),
]],
#Quest 3 - First dialog sentence/Repeating dialog sentence
[anyone, "start",
[
(is_between, "$g_talk_troop", "trp_tsu_merchant", "trp_startup_merchants_end"),
(eq, "$talk_context", tc_tavern_talk),

(check_quest_active, "qst_save_relative_of_merchant"),
(neg|check_quest_succeeded, "qst_save_relative_of_merchant"),

(str_store_party_name, s9, "$current_town"),
],
"So, you've found out where they hid Horenbo? Good work. I flatter myself that I'm a fine judge of character, and you look to be a {man/woman} who can get things done. Now, go out and save his hide!", "merchant_quest_3a",
[
]],
#Quest 3 - All succeeded - First dialog sentence
[anyone, "start",
[
(is_between, "$g_talk_troop", "trp_tsu_merchant", "trp_startup_merchants_end"),
(eq, "$talk_context", tc_tavern_talk),

(check_quest_active, "qst_save_relative_of_merchant"),
(check_quest_succeeded, "qst_save_relative_of_merchant"),
],
"Welcome back, friend. Horenbo arrived here before you, so I know that you know... In any case, here's the rest of your reward.", "merchant_quest_3b",
#"Well... Gengoro is home safe. I'm not sure what to do with him -- maybe pack him off to a temple outside the province. That way, if he gets knocked on the head in a street brawl, no one can say it's my fault. But that's not your problem. Here's the rest of your reward. It was well-earned.", "merchant_quest_3b",
[
(call_script, "script_finish_quest", "qst_save_relative_of_merchant", 100),
(troop_add_gold, "trp_player", 200),
]],
[anyone, "start",
[
(is_between, "$g_talk_troop", "trp_tsu_merchant", "trp_startup_merchants_end"),

(this_or_next|eq, "$talk_context", tc_tavern_talk),
(neq, "$dialog_with_merchant_ended", 0),

(assign, ":continue", 0),
(try_begin),
(neg|check_quest_succeeded, "qst_collect_men"),
(neg|check_quest_active, "qst_collect_men"),
(assign, ":continue", 1),
(else_try),
(neg|check_quest_active, "qst_collect_men"),
(neg|check_quest_succeeded, "qst_learn_where_merchant_brother_is"),
(neg|check_quest_active, "qst_learn_where_merchant_brother_is"),
(assign, ":continue", 1),
(else_try),
(neg|check_quest_active, "qst_collect_men"),
(neg|check_quest_active, "qst_learn_where_merchant_brother_is"),
(neg|check_quest_succeeded, "qst_save_relative_of_merchant"),
(neg|check_quest_active, "qst_save_relative_of_merchant"),
(assign, ":continue", 1),
(try_end),

(eq, ":continue", 1),
],
##diplomacy start+ replaced "a rich men" with "a rich {reg65?woman:man}"
#"You may do as you wish, {sir/my lady}, but I am disappointed. You would do well to reconsider. I am a rich men, and would show you my gratitude in coin.", "merchant_quest_persuasion",
"Do as you wish, {sir/madam}, but this is disappointing. Please reconsider. I am a rich {reg65?woman:man}, and know how to show gratitude with my wealth.", "merchant_quest_persuasion",
##diplomacy end+
[
]],
[anyone|auto_proceed, "start",
[
(is_between, "$g_talk_troop", "trp_tsu_merchant", "trp_startup_merchants_end"),

(this_or_next|eq, "$talk_context", tc_tavern_talk),
(neq, "$dialog_with_merchant_ended", 0),

(check_quest_finished, "qst_save_relative_of_merchant"),
(neg|check_quest_succeeded, "qst_save_town_from_bandits"),
(neg|check_quest_active, "qst_save_town_from_bandits"),
],
"{!}.", "merchant_quest_4b4",
[
]],
[anyone, "start",
[
(is_between, "$g_talk_troop", "trp_relative_of_merchant", "trp_relative_of_merchant"),
],
  "Oh -- thank the gods... Thank the gods... Am I safe?", "close_window",
[]],
[anyone,"start",
[
(is_between, "$g_talk_troop", "trp_tsu_merchant", "trp_startup_merchants_end"),
(eq, "$g_do_one_more_meeting_with_merchant", 1),
#gekokujo 3.0 use town lord rather than faction leader
#(faction_get_slot, ":faction_leader", "$g_encountered_party_faction", slot_faction_leader),
#(str_store_troop_name, s5, ":faction_leader"),
(party_get_slot, ":local_ruler", "$g_starting_town", slot_town_lord),
(str_store_troop_name, s5, ":local_ruler"),
##diplomacy start+ fix the pronouns
(call_script, "script_dplmc_store_troop_is_female_reg", ":local_ruler", 4),
],
"Haha! {playername}! Things went well as I had hoped. {s5} is none the wiser about what happened and who are truly running this town. {reg4?She:He}'s not as strong as he thinks. As long as you see me walk freely in this town, you will know the victory of the Ikko Ikki. It's only a matter of time until we can overthrow {s5} and declare this city peasant-ruled.", "merchant_closing_statement_2",
##diplomacy end+
[]],
[anyone|auto_proceed, "start",
[
(is_between, "$g_talk_troop", "trp_tsu_merchant", "trp_startup_merchants_end"),
(check_quest_finished, "qst_save_town_from_bandits"),
(eq, "$g_do_one_more_meeting_with_merchant", 2),
],
"{!}.", "merchant_quests_last_word",
[]],
[anyone|plyr, "member_intel_liaison", [],
"What have you discovered?", "member_intel_liaison_results", []],
[anyone, "start", [
			   #gekokujo 3.0 microfactions! include fort companions start
               #(is_between, "$g_talk_troop", companions_begin, companions_end),
               (is_between, "$g_talk_troop", companions_begin, fort_companions_end),
			   #gekokujo 3.0 microfactions! include fort companions end
               (eq, "$talk_context", tc_tavern_talk),
               (troop_slot_eq, "$g_talk_troop", slot_troop_current_mission, npc_mission_gather_intel)],
"Greetings, stranger.", "member_intel_liaison", []],
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
#gekokujo 3.0 no recruiting of companions while a freelancer on vacation start
[anyone, "start", [
		(is_between, "$g_talk_troop", companions_begin, companions_end),
		(this_or_next|eq, "$talk_context", tc_tavern_talk),
		(this_or_next|eq, "$talk_context", tc_town_talk),
		(eq, "$talk_context", tc_court_talk),
		#(main_party_has_troop, "$g_talk_troop"), #gekokujo 3.1 why was this even on here
		(eq, "$freelancer_state", 2)
	],
	"{Sir/Madam}?^^(You're a troop, remember?)", "close_window", []],
#gekokujo 3.0 no recruiting of companions while a freelancer on vacation end

[anyone, "start", [(is_between, "$g_talk_troop", companions_begin, companions_end),
               (this_or_next|eq, "$talk_context", tc_tavern_talk),
			   (this_or_next|eq, "$talk_context", tc_town_talk), #Gekokujo Bodyguard
            (eq, "$talk_context", tc_court_talk),
               (main_party_has_troop, "$g_talk_troop")],
"Let's leave whenever you are ready.", "close_window", []],
[anyone, "start", [(is_between, "$g_talk_troop", companions_begin, companions_end),
               (troop_slot_eq, "$g_talk_troop", slot_troop_occupation, 0),
               (troop_slot_eq, "$g_talk_troop", slot_troop_turned_down_twice, 1),
],
"Please do not waste any more of my time today, {sir/madame}. Perhaps we shall meet again in our travels.", "close_window", [
 ]],
[anyone, "start", [(is_between, "$g_talk_troop", companions_begin, companions_end),
               (troop_slot_eq, "$g_talk_troop", slot_troop_occupation, 0),
               (eq, "$g_talk_troop_met", 0),
               (troop_get_slot, ":intro", "$g_talk_troop", slot_troop_intro),
               (str_store_string, 5, ":intro"),
               (str_store_party_name, 20, "$g_encountered_party"),
],
"{s5}", "companion_recruit_intro_response", [
              (troop_set_slot, "$g_talk_troop", slot_troop_first_encountered, "$g_encountered_party"),
 ]],
[anyone, "start", [(is_between, "$g_talk_troop", companions_begin, companions_end),
               (troop_slot_eq, "$g_talk_troop", slot_troop_occupation, 0),
               (troop_slot_eq, "$g_talk_troop", slot_troop_met_previously, 1),
               (troop_slot_eq, "$g_talk_troop", slot_troop_playerparty_history, 0),

],
"We meet again.", "companion_recruit_meet_again", [
               (troop_set_slot, "$g_talk_troop", slot_troop_turned_down_twice, 1),
 ]],
[anyone, "start", [(is_between, "$g_talk_troop", companions_begin, companions_end),
               (troop_slot_eq, "$g_talk_troop", slot_troop_occupation, 0),
               (troop_slot_eq, "$g_talk_troop", slot_troop_met_previously, 0),
               (troop_slot_eq, "$g_talk_troop", slot_troop_playerparty_history, 0),
],
"Yes?", "companion_recruit_secondchance", [
               (troop_set_slot, "$g_talk_troop", slot_troop_turned_down_twice, 1),
 ]],
### Rehire dialogues
[anyone, "start", [
    (is_between, "$g_talk_troop", companions_begin, companions_end),
    (neg|troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_hero),
    (troop_slot_eq, "$g_talk_troop", slot_troop_playerparty_history, pp_history_indeterminate),

    (troop_get_slot, ":prison_center", "$g_talk_troop", slot_troop_prisoner_of_party),
    (lt, ":prison_center", centers_begin),
  ], "My offer to rejoin you still stands, if you'll have me.", "companion_rehire", []],
### If the companion and the player were separated in battle
[anyone, "start",
[
(is_between, "$g_talk_troop", companions_begin, companions_end),
(neg|troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_hero),
(troop_slot_eq, "$g_talk_troop", slot_troop_playerparty_history, pp_history_scattered),

(this_or_next|eq, "$talk_context", tc_hero_freed),
(neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),

(neq, "$talk_context", tc_prison_break),

(assign, ":battle_fate", "str_battle_fate_1"),
(store_random_in_range, ":fate_roll", 0, 5),
(val_add, ":battle_fate", ":fate_roll"),
(str_store_string, s6, ":battle_fate"),
(troop_get_slot, ":honorific", "$g_talk_troop", slot_troop_honorific),
(str_store_string, s5, ":honorific"),
],
"It is good to see you alive, {s5}! {s6}, and I did not know whether you had been captured, or beheaded, or got away. I've been roaming around since then, looking for you. Shall I get my gear together and rejoin you?","companion_rehire",
[
(troop_set_slot, "$g_talk_troop", slot_troop_playerparty_history, pp_history_indeterminate),
(troop_set_slot, "$g_talk_troop", slot_troop_prisoner_of_party, -1),
]],
[anyone|plyr,"start",
[
#gekokujo 3.0 microfactions! include fort companions start
#(is_between, "$g_talk_troop", companions_begin, companions_end),
(is_between, "$g_talk_troop", companions_begin, fort_companions_end),
#gekokujo 3.0 microfactions! include fort companions end
(neg|troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_hero),
(troop_slot_eq, "$g_talk_troop", slot_troop_playerparty_history, pp_history_scattered),

(troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),

(neq, "$talk_context", tc_prison_break),

(assign, ":battle_fate", "str_battle_fate_1"),
(store_random_in_range, ":fate_roll", 0, 5),
(val_add, ":battle_fate", ":fate_roll"),
(str_store_string, s6, ":battle_fate"),
(troop_get_slot, ":honorific", "$g_talk_troop", slot_troop_honorific),
(str_store_string, s5, ":honorific"),
],
"I've come to break you out of here.", "companion_prison_break_chains",[]],
### If the player and the companion parted on bad terms
[anyone, "start", [(is_between, "$g_talk_troop", companions_begin, companions_end),
               (troop_slot_eq, "$g_talk_troop", slot_troop_occupation, 0),
               (troop_slot_eq, "$g_talk_troop", slot_troop_turned_down_twice, 0),
               (troop_slot_eq, "$g_talk_troop", slot_troop_playerparty_history, pp_history_quit),
               (troop_get_slot, ":speech", "$g_talk_troop", slot_troop_rehire_speech),
               (str_store_string, 5, ":speech"),
],
"{s5}", "companion_rehire", [
               (troop_set_slot, "$g_talk_troop", slot_troop_playerparty_history, pp_history_indeterminate),
]],
###If the player and the companion parted on good terms
[anyone, "start", [(is_between, "$g_talk_troop", companions_begin, companions_end),
               (troop_slot_eq, "$g_talk_troop", slot_troop_occupation, 0),
               (troop_slot_eq, "$g_talk_troop", slot_troop_playerparty_history, pp_history_dismissed),
               (troop_get_slot, ":honorific", "$g_talk_troop", slot_troop_honorific),
               (str_store_string, 21, ":honorific"),
               (troop_get_slot, ":speech", "$g_talk_troop", slot_troop_backstory_delayed),
               (str_store_string, 5, ":speech"),
],
"It is good to see you, {s21}! To tell you the truth, I had hoped to run into you.",
"companion_was_dismissed", [
               (troop_set_slot, "$g_talk_troop", slot_troop_playerparty_history, pp_history_indeterminate),
]],
#Default dialog added - for rehire
[anyone, "start", [
##gekokujo 3.0 microfactions! include fort companions start #yeah this is not what i wanted
(is_between, "$g_talk_troop", companions_begin, companions_end),
#(is_between, "$g_talk_troop", companions_begin, fort_companions_end),
##gekokujo 3.0 microfactions! include fort companions end
(neg|troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_hero),

(troop_get_slot, ":prison_center", "$g_talk_troop", slot_troop_prisoner_of_party),
(lt, ":prison_center", centers_begin),
], "So... Do you want me back yet?", "companion_rehire",
[]],
   [anyone,"offer_gift_quest_complete", [
   (quest_get_slot, ":target_troop", "qst_offer_gift", slot_quest_target_troop),
   (troop_get_type, reg4, ":target_troop"),
   ],
   "Ah, let me take those. Hopefully this will mend the quarrel between you two. You may wish to speak to {reg4?her:him}, and see if I had any success.", "close_window",[
   (quest_set_slot, "qst_offer_gift", slot_quest_current_state, 2),
   (quest_set_slot, "qst_offer_gift", slot_quest_expiration_days, 365),
   (troop_remove_item, "trp_player", "itm_furs"),
   (troop_remove_item, "trp_player", "itm_velvet"),
   (assign, "$g_leave_encounter", 1),
]],
##diplomacy begin
# Recruiter kit begin
[trp_dplmc_recruiter, "start", [
##diplomacy start+ replace {reg65?madame:sir} with {s0}.  Also replace "okay to you" with "okay with you".
(call_script, "script_dplmc_print_subordinate_says_sir_madame_to_s0"),
], "Hello {s0}. If it's ok with you, I would like to get on with my assignment.", "dplmc_recruiter_talk",[]],
##diplomacy end+
# Recruiter kit end

##Messenger
[trp_dplmc_messenger, "start", [], "Greetings. Sorry but I don't have time to talk now. I am delivering a very important message to {s6}.", "dplmc_messenger_talk", []],
##patrol
[anyone, "start",
[
(party_slot_eq, "$g_encountered_party", slot_party_type, spt_patrol),
(party_slot_eq, "$g_encountered_party", dplmc_slot_party_mission_diplomacy, "trp_player"),
(party_get_slot, ":target_party", "$g_encountered_party", slot_party_ai_object),
(str_store_party_name, s6, ":target_party"),
##nested diplomacy start+ Replace "Sire" with {s0}
(call_script, "script_dplmc_print_subordinate_says_sir_madame_to_s0"),
#], "Greetings, Sire. We are still patrolling {s6}. Do you have new orders?", "dplmc_patrol_talk", []
], "Greetings, {s0}. We are still patrolling {s6}. Do you have new orders?", "dplmc_patrol_talk", []
##nested diplomacy end+
],
##gift caravan
[pt_dplmc_gift_caravan|party_tpl, "start",
[
(party_slot_eq, "$g_talk_troop_party", slot_party_type, dplmc_spt_gift_caravan),
(party_get_slot, ":target_party", "$g_talk_troop_party", slot_party_ai_object),
(party_get_slot, ":gift", "$g_talk_troop_party", dplmc_slot_party_mission_diplomacy),
(str_store_item_name, s12, ":gift"),

(try_begin),
(party_slot_ge, "$g_talk_troop_party",  slot_party_orders_object,  0),
(party_get_slot, ":target_troop", "$g_talk_troop_party",  slot_party_orders_object),
(str_store_troop_name, s13, ":target_troop"),
(else_try),
(str_store_party_name, s13, ":target_party"),
(try_end),

],
"Greetings. I am currently delivering {s12} to {s13}.", "dplmc_gift_talk", []],
[trp_dplmc_scout, "start",
[], "My {lord/lady}, I haven't finished my mission yet.", "dplmc_scout_talk",
[]],
##Chancellor
[anyone,"start",
[
(eq, "$g_player_chancellor","$g_talk_troop"),
],
##nested diplomacy start+ Change "Milord" to "Milord/Milady"
"{Milord/Milady}?", "dplmc_chancellor_talk",[
##nested diplomacy end+
]],
##Constable
[anyone,"start",
[
(eq, "$g_player_constable","$g_talk_troop"),
],
"Always at your service!", "dplmc_constable_talk",[
]],
[anyone,"start",
[
(eq, "$g_player_chamberlain","$g_talk_troop"),
],
"Yes, my {lord/lady}?", "dplmc_chamberlain_talk",[
]],
[anyone|plyr,"script_dplmc_affiliate_confirm", [],
"I do not want to be related to your house anymore.", "dplmc_lord_family_affiliate_leave",[
]],
[anyone|plyr,"script_dplmc_affiliate_confirm", [],
"Oh nothing.", "lord_pretalk",[
]],
##companion returning after threaten request
[anyone, "event_triggered", [
(store_conversation_troop, "$map_talk_troop"),
(eq, "$map_talk_troop", "$npc_to_rejoin_party"),
(troop_slot_eq, "$g_talk_troop", slot_troop_current_mission, dplmc_npc_mission_threaten_request),
(troop_get_slot, ":string", "$map_talk_troop", slot_troop_honorific),
(str_store_string, 21, ":string"),
  (troop_get_slot, ":mission_object", "$g_talk_troop", slot_troop_mission_object),
   (str_store_faction_name, s31, ":mission_object"),
(call_script, "script_npc_decision_checklist_peace_or_war", ":mission_object", "fac_player_supporters_faction", "$g_talk_troop"),
(assign, "$g_mission_result", reg0),
],
"Well, {s21}, at last I've found you. I have returned from my mission to {s31}.","dplmc_companion_threaten_request_response",
[
(troop_get_slot, ":mission_object", "$g_talk_troop", slot_troop_mission_object),
(store_relation, ":player_relation", ":mission_object", "fac_player_supporters_faction"),
(val_sub, ":player_relation", 3),
(val_max, ":player_relation", 0),
(set_relation, ":mission_object", "fac_player_supporters_faction", ":player_relation"),
]],
##companion returning after gift request
[anyone, "event_triggered", [
(store_conversation_troop, "$map_talk_troop"),
(eq, "$map_talk_troop", "$npc_to_rejoin_party"),
(troop_get_slot, ":mission", "$g_talk_troop", slot_troop_current_mission),
(this_or_next|eq, ":mission", dplmc_npc_mission_gift_fief_request),
(eq, ":mission", dplmc_npc_mission_gift_horses_request),
(troop_get_slot, ":string", "$map_talk_troop", slot_troop_honorific),
(str_store_string, 21, ":string"),
(troop_get_slot, ":mission_object", "$g_talk_troop", slot_troop_mission_object),
(str_store_faction_name, s31, ":mission_object"),
],
"Well, {s21}, at last I've found you. I have returned from my mission to {s31}. They were agreeably surprised.","companion_rejoin_response", [
(troop_get_slot, ":dipomacy_var", "$g_talk_troop", dplmc_slot_troop_mission_diplomacy),
(troop_get_slot, ":mission", "$g_talk_troop", slot_troop_current_mission),
(try_begin),
(troop_get_slot, ":mission_object", "$g_talk_troop", slot_troop_mission_object),
(eq, ":mission", dplmc_npc_mission_gift_fief_request),
(call_script, "script_give_center_to_faction", ":dipomacy_var", ":mission_object"),
(assign, ":concession_value", 1),
(try_begin),
 (is_between, ":dipomacy_var", towns_begin, towns_end),
 (assign, ":concession_value", 6),
(else_try),
  (is_between, ":dipomacy_var", castles_begin, castles_end),
  (assign, ":concession_value", 4),
(else_try),
  (is_between, ":dipomacy_var", villages_begin, villages_end),
  (assign, ":concession_value", 2),
(try_end),
(call_script, "script_change_troop_renown", "trp_player", ":concession_value"),
(val_mul, ":concession_value", 2),
(call_script, "script_change_player_relation_with_faction", ":mission_object", ":concession_value"),
(else_try),
(eq, ":mission", dplmc_npc_mission_gift_horses_request),
(try_begin),
  (le, ":dipomacy_var", 3000),
  (call_script, "script_change_player_relation_with_faction", ":mission_object", 2),
  (call_script, "script_change_troop_renown", "trp_player", 1),
(else_try),
  (gt, ":dipomacy_var", 3000),
  (call_script, "script_change_player_relation_with_faction", ":mission_object", 4),
  (call_script, "script_change_troop_renown", "trp_player", 2),
(try_end),
(try_end),
]],
##companion returning after exchange request
[anyone, "event_triggered", [
(store_conversation_troop, "$map_talk_troop"),
(eq, "$map_talk_troop", "$npc_to_rejoin_party"),

(troop_get_slot, ":mission", "$g_talk_troop", slot_troop_current_mission),
  (eq, ":mission", dplmc_npc_mission_prisoner_exchange),

(troop_get_slot, ":enemy_prisoner", "$g_talk_troop", dplmc_slot_troop_mission_diplomacy),
(troop_get_slot, ":own_prisoner", "$g_talk_troop", dplmc_slot_troop_mission_diplomacy2),

(troop_get_slot, ":own_prison", ":enemy_prisoner", slot_troop_prisoner_of_party),
(troop_get_slot, ":enemy_prison", ":own_prisoner", slot_troop_prisoner_of_party),
(is_between, ":own_prison", walled_centers_begin, walled_centers_end),
(is_between, ":enemy_prison", walled_centers_begin, walkers_end),


(call_script, "script_calculate_ransom_amount_for_troop", ":enemy_prisoner"),
(assign, ":enemy_value", reg0),
(call_script, "script_calculate_ransom_amount_for_troop", ":own_prisoner"),
(assign, ":own_value", reg0),
(ge, ":enemy_value", ":own_value"),

(troop_get_slot, ":string", "$map_talk_troop", slot_troop_honorific),
(str_store_string, 21, ":string"),
(str_store_troop_name, s32, ":enemy_prisoner"),
(str_store_troop_name, s33, ":own_prisoner"),
##diplomacy start+ Make pronouns correct
(call_script, "script_dplmc_store_troop_is_female", ":enemy_prisoner"),
(assign, reg4, reg0),
               ],#Next line, "exchange {s32} against {s33}"  -> "exchange {s32} for {s33}"
"Well, {s21}, at last I've found you.They agreed to exchange {s32} for {s33}. {s33} has accompanied me back here. Do you want to set {s32} free?","dplmc_companion_prisoner_exchange_confirm", [
              ]],
[anyone, "event_triggered", [
(store_conversation_troop, "$map_talk_troop"),
(eq, "$map_talk_troop", "$npc_to_rejoin_party"),

(troop_get_slot, ":mission", "$g_talk_troop", slot_troop_current_mission),
  (eq, ":mission", dplmc_npc_mission_prisoner_exchange),

(troop_get_slot, ":enemy_prisoner", "$g_talk_troop", dplmc_slot_troop_mission_diplomacy),
(troop_get_slot, ":own_prisoner", "$g_talk_troop", dplmc_slot_troop_mission_diplomacy2),

(troop_get_slot, ":string", "$map_talk_troop", slot_troop_honorific),
(str_store_string, 21, ":string"),
(str_store_troop_name, s32, ":enemy_prisoner"),
(str_store_troop_name, s33, ":own_prisoner"),
               ],##diplomacy start+ Change "exchange against" to "exchange for"
"Well, {s21}, at last I've found you. They didn't agree to exchange {s32} for {s33}.","companion_rejoin_response", [
              ]],
##companion returning after persuasion request
[anyone, "event_triggered", [
(store_conversation_troop, "$map_talk_troop"),
(eq, "$map_talk_troop", "$npc_to_rejoin_party"),
(troop_get_slot, ":mission", "$g_talk_troop", slot_troop_current_mission),
  (eq, ":mission", dplmc_npc_mission_persuasion),
(troop_get_slot, ":string", "$map_talk_troop", slot_troop_honorific),
(str_store_string, 21, ":string"),
  (troop_get_slot, ":mission_object", "$g_talk_troop", slot_troop_mission_object),
   (str_store_faction_name, s30, ":mission_object"),
   (troop_get_slot, ":target_troop", "$g_talk_troop", dplmc_slot_troop_mission_diplomacy),
(str_store_troop_name, s14, ":target_troop"),
 (troop_set_slot, "$g_talk_troop", slot_troop_intrigue_impatience, 500),


(assign, ":no_join", 0),
(str_clear, s40),

  #player is still king
(faction_get_slot, ":faction_leader", "fac_player_supporters_faction", slot_faction_leader),
(try_begin),
  (neq, ":faction_leader", "trp_player"),
  (str_store_string, s40, "@Your leader is not even a daimyo and I shall join you?"),
  (assign, ":no_join", 1),
(try_end),

#player has fief
(assign, ":one_fortress_found", 0),
(try_for_range, ":walled_center", walled_centers_begin, walled_centers_end),
   (this_or_next|party_slot_eq, ":walled_center", slot_town_lord, "$g_talk_troop"),
  (party_slot_eq, ":walled_center", slot_town_lord, "trp_player"),
   (assign, ":one_fortress_found", 1),
(try_end),

(try_begin),
  (eq, ":one_fortress_found", 0),
  (str_store_string, s40, "@{s40} I would never join someone who doesn't own a town or castle."),
  (assign, ":no_join", 1),
(try_end),

(assign, ":enough_renown", 1),
(try_begin),
  (troop_slot_eq, ":target_troop", slot_lord_reputation_type, lrep_martial),
  (this_or_next|lt, "$player_right_to_rule", 10),
  (neg|troop_slot_ge, "trp_player", slot_troop_renown, 400),
  (assign, ":enough_renown", 0),
(else_try),
  (troop_slot_eq, ":target_troop", slot_lord_reputation_type, lrep_upstanding),
  (this_or_next|lt, "$player_right_to_rule", 20),
  (neg|troop_slot_ge, "trp_player", slot_troop_renown, 200),
  (assign, ":enough_renown", 0),
(else_try),
  (troop_slot_eq, ":target_troop", slot_lord_reputation_type, lrep_selfrighteous),
  (this_or_next|lt, "$player_right_to_rule", 10),
  (neg|troop_slot_ge, "trp_player", slot_troop_renown, 200),
  (assign, ":enough_renown", 0),
(else_try),
  (troop_slot_eq, ":target_troop", slot_lord_reputation_type, lrep_cunning),
  (neg|troop_slot_ge, "trp_player", slot_troop_renown, 400),
    (assign, ":enough_renown", 0),
(else_try),
  (neg|troop_slot_ge, "trp_player", slot_troop_renown, 200),
  (assign, ":enough_renown", 0),
(try_end),

(try_begin),
  (eq, ":enough_renown", 0),
  ##diplomacy start+ "to" to "too"
  (str_store_string, s40, "@{s40} I know too little about your leader."),
  ##diplomacy end+
  (assign, ":no_join", 1),
(try_end),

#init random seed
(troop_get_slot, ":temp_ai_seed", ":target_troop", slot_troop_temp_decision_seed),
(store_div, ":persuasion_random", ":temp_ai_seed", 100),  #I used div instead of mod to have a different random value, value generated from (mod 100) will be used in next steps. These two values should be non-related.
##diplomacy start+
(troop_get_slot, ":target_reputation", ":target_troop", slot_lord_reputation_type),
(try_begin),
	(store_mod, reg0, ":target_troop", 2),
	(eq, reg0, 0),
	(val_add, ":persuasion_random", 50),#because we take mod 100, the average effect of this is zero, but it addresses problems such as "all high" or "all low"
(try_end),
(val_mod, ":persuasion_random", 100),#should take mod 100 after division
##diplomacy end+
(val_add, ":persuasion_random", 1),
(store_skill_level, ":persuasion_skill", "skl_persuasion", "$g_talk_troop"),
(val_mul, ":persuasion_skill", 7),
##diplomacy start+
#Add a base success chance, so that skill 5 has a 50% chance of failure instead of a 65% chance of failure.
(val_add, ":persuasion_skill", 15),
##diplomacy end+
(try_begin),
  (lt, ":persuasion_skill", ":persuasion_random"),
##diplomacy start+
##OLD:
#  (str_store_string, s40, "@{s40} Next time I prefer to talk to someone who doesn't act like a fool."),
#  (assign, ":no_join", 1),
##NEW:
  (try_begin),
     (ge, "$cheat_mode", 1),
	 (assign, reg0, ":persuasion_random"),
	 (assign, reg1, ":persuasion_skill"),
	 (display_message, "@{!} Emissary persuasion attempt: skill factor {reg1} versus random number {reg0}"),
  (try_end),
  (store_mul, reg0, ":persuasion_skill", 2),
  (try_begin),
     (this_or_next|ge, reg0, ":persuasion_random"),
		(eq, ":target_reputation", lrep_goodnatured),
	 (neq, ":target_reputation", lrep_debauched),
	 (neq, ":target_reputation", lrep_quarrelsome),
	 (str_store_string, s40, "@{s40} I found your messenger unconvincing."),
  (else_try),
	 (this_or_next|eq, ":target_reputation", lrep_debauched),
	 (this_or_next|eq, ":target_reputation", lrep_quarrelsome),
	 (this_or_next|eq, ":target_reputation", lrep_selfrighteous),
	 (this_or_next|eq, ":target_reputation", lrep_ambitious),
		(is_between, ":target_reputation", lrep_roguish, lrep_conventional),
     (str_store_string, s40, "@{s40} Next time I would prefer to talk to someone who doesn't act like a fool."),
  (else_try),
     (str_store_string, s40, "@{s40} Next time I would prefer to talk to someone more versed in courtly manners."),
  (try_end),
  (assign, ":no_join", 1),
(try_end),
##diplomacy end+

   (call_script, "script_calculate_troop_political_factors_for_liege", ":target_troop", "trp_player"),
   (assign, ":result_for_security", reg2),
(assign, ":result_for_political", reg4),
   (assign, ":change_penalty", reg10),
   (assign, ":result_for_new_liege", reg0),
   (store_faction_of_troop, ":target_faction", ":target_troop"),
   (faction_get_slot, ":cur_liege", ":target_faction", slot_faction_leader),
   (call_script, "script_calculate_troop_political_factors_for_liege", ":target_troop", ":cur_liege"),

   (store_sub, ":result_for_security_comparative", ":result_for_security", reg2),
   (store_sub, ":result_for_political_comparative", ":result_for_political", reg4),
   (assign, ":result_for_old_liege", reg0),
   (store_sub, "$pledge_chance", ":result_for_new_liege", ":result_for_old_liege"),
   (val_add, "$pledge_chance", 50),
   (val_div, "$pledge_chance", 2),

(store_mod, ":random", ":temp_ai_seed", 100),

(try_begin),
  (eq, "$cheat_mode", 1),
  (assign, reg2, ":result_for_security"),
  (display_message, "@{!}DEBUG - result_for_security: {reg2} > 10"),
  (assign, reg2, ":result_for_political"),
  (display_message, "@{!}DEBUG - result_for_political: {reg2} > 0"),
  (assign, reg2, ":change_penalty"),
  (display_message, "@{!}DEBUG - change_penalty: {reg2} < 20"),
  (assign, reg2, ":random"),
  (display_message, "@{!}DEBUG - random: {reg2}"),
  (assign, reg2, "$pledge_chance"),
  (display_message, "@{!}DEBUG - > pledge_chance: {reg2}"),
  (assign, reg2, ":result_for_security_comparative"),
  (display_message, "@{!}DEBUG - result_for_security_comparative: {reg2} > 0"),
  (assign, reg2, ":result_for_political_comparative"),
  (display_message, "@{!}DEBUG - result_for_political_comparative: {reg2} > 0"),
(try_end),

(try_begin),
  (le, ":random", "$pledge_chance"),
  (assign, ":no_join", 1),
  (str_store_string, s40, "@{s40} I rather stay with my current overlord."),
(try_end),

(try_begin),
  (eq, ":no_join", 0),
   (try_begin),
      (lt, ":result_for_political", 0),
    (assign, ":no_join", 1),

      (try_begin),
         (troop_slot_eq, ":target_troop", slot_lord_reputation_type, lrep_upstanding),
         (str_store_string, s31, "str_i_worry_about_those_with_whom_you_have_chosen_to_surround_yourself" ),
      (else_try),
         (troop_slot_eq, ":target_troop", slot_lord_reputation_type, lrep_martial),
         (str_store_string, s31, "str_there_are_some_outstanding_matters_between_me_and_some_of_your_vassals_"),
         (try_begin),
           (assign, reg41, ":result_for_political"),
           ##diplomacy start+ Only show debug messages with cheat mode on
           (ge, "$cheat_mode", 1),
           ##diplomacy end+
           (display_message, "str_result_for_political_=_reg41"),
         (try_end),
      (else_try),
         (troop_slot_eq, ":target_troop", slot_lord_reputation_type, lrep_quarrelsome),
         (str_store_string, s31, "str_my_liege_has_his_faults_but_i_dont_care_for_your_toadies"),
      (else_try),
         (troop_slot_eq, ":target_troop", slot_lord_reputation_type, lrep_goodnatured),
         (str_store_string, s31, "str_i_think_youre_a_good_man_but_im_worried_that_you_might_be_pushed_in_the_wrong_direction_by_some_of_those_around_you"),
      (else_try),
         (troop_slot_eq, ":target_troop", slot_lord_reputation_type, lrep_selfrighteous),
         (str_store_string, s31, "str_i_am_loathe_to_fight_alongside_you_so_long_as_you_take_under_your_wing_varlots_and_base_men"),
      (else_try),
         (troop_slot_eq, ":target_troop", slot_lord_reputation_type, lrep_cunning),
         (str_store_string, s31, "str_ill_be_honest__with_some_of_those_who_follow_you_i_think_id_be_more_comfortable_fighting_against_you_than_with_you"),
      (else_try),
         (troop_slot_eq, ":target_troop", slot_lord_reputation_type, lrep_debauched),
         (str_store_string, s31, "str_i_say_that_you_can_judge_a_man_by_the_company_he_keeps_and_you_have_surrounded_yourself_with_vipers_and_vultures"),
      (else_try),
         (troop_slot_ge, ":target_troop", slot_lord_reputation_type, lrep_roguish),
         (str_store_string, s31, "str_you_know_that_i_have_always_had_a_problem_with_some_of_our_companions"),
      (try_end),
   (else_try),
      (lt, ":result_for_political_comparative", 0),
      (assign, ":no_join", 1),
      (str_store_string, s31, "str_politically_i_would_be_a_better_position_in_the_court_of_my_current_liege_than_in_yours"),
   (else_try),
      (str_store_string, s31, "str_i_am_more_comfortable_with_you_and_your_companions_than_with_my_current_liege"),
   (try_end),

   (try_begin),
      (lt, ":result_for_security", 10),
      (assign, ":no_join", 1),

      (try_begin),
         (this_or_next|troop_slot_eq, ":target_troop", slot_lord_reputation_type, lrep_cunning),
         (troop_slot_ge, ":target_troop", slot_lord_reputation_type, lrep_roguish),
         (str_store_string, s32, "str_militarily_youre_in_no_position_to_protect_me_should_i_be_attacked_id_be_reluctant_to_join_you_until_you_could"),
      (else_try),
         (troop_slot_eq, ":target_troop", slot_lord_reputation_type, lrep_upstanding),
         (str_store_string, s32, "str_militarily_when_i_consider_the_lay_of_the_land_i_realize_that_to_pledge_myself_to_you_now_would_endanger_my_faithful_retainers_and_my_family"),
      (else_try),
         (troop_slot_eq, ":target_troop", slot_lord_reputation_type, lrep_martial),
         (str_store_string, s32, "str_militarily_youre_in_no_position_to_come_to_my_help_if_someone_attacked_me_i_dont_mind_a_good_fight_but_i_like_to_have_a_chance_of_winning"),
      (else_try),
         (troop_slot_eq, ":target_troop", slot_lord_reputation_type, lrep_goodnatured),
         (str_store_string, s32, "str_militarily_youre_in_no_position_to_come_to_my_help_if_someone_attacked_me_i_dont_mind_a_good_fight_but_i_like_to_have_a_chance_of_winning"),
      (else_try),
         (troop_slot_eq, ":target_troop", slot_lord_reputation_type, lrep_debauched),
         (str_store_string, s32, "str_militarily_you_would_have_me_join_you_only_to_find_myself_isolated_amid_a_sea_of_enemies"),
      (else_try),
         (troop_slot_eq, ":target_troop", slot_lord_reputation_type, lrep_selfrighteous),
         (str_store_string, s32, "str_militarily_you_would_have_me_join_you_only_to_find_myself_isolated_amid_a_sea_of_enemies"),
      (else_try),
         (troop_slot_eq, ":target_troop", slot_lord_reputation_type, lrep_quarrelsome),
         (str_store_string, s32, "str_militarily_youre_in_no_position_to_come_to_my_help_if_someone_attacked_me_youd_let_me_be_cut_down_like_a_dog_id_bet"),
      (try_end),
   (else_try),
      (lt, ":result_for_security_comparative", 0),
      (assign, ":no_join", 1),
      (str_store_string, s32, "str_militarily_i_wouldnt_be_any_safer_if_i_joined_you"),
   (else_try),
      (str_store_string, s32, "str_militarily_i_might_be_safer_if_i_joined_you"),
   (try_end),

   (try_begin),
      (gt, ":change_penalty", 40),
      (assign, ":no_join", 1),
      (str_store_string, s34, "str_finally_there_is_a_cost_to_ones_reputation_to_change_sides_in_this_case_the_cost_would_be_very_high"),
   (else_try),
      (gt, ":change_penalty", 20),
      (assign, ":no_join", 1),
      (str_store_string, s34, "str_finally_there_is_a_cost_to_ones_reputation_to_change_sides_in_this_case_the_cost_would_be_significant"),
   (else_try),
      (str_store_string, s34, "str_finally_there_is_a_cost_to_ones_reputation_to_change_sides_in_this_case_however_many_men_would_understand"),
   (try_end),
   (str_store_string, s40, "@{s31} {s32} {s34}"),
(try_end),

(eq, ":no_join", 1),
##diplomacy start+ use reg0 for gender
(call_script, "script_dplmc_store_troop_is_female", ":target_troop"),
],#Next line "He" to {reg0?She:he}
"Well, {s21}, at last I've found you. I have returned from my persuasion mission to {s30}. {s14} doesn't want to join you. {reg0?She:He} said: {s40}","companion_rejoin_response",
##diplomacy end+
[
]],
##companion returning after persuasion request
[anyone, "event_triggered", [
(store_conversation_troop, "$map_talk_troop"),
(eq, "$map_talk_troop", "$npc_to_rejoin_party"),
(troop_get_slot, ":mission", "$g_talk_troop", slot_troop_current_mission),
  (eq, ":mission", dplmc_npc_mission_persuasion),
(troop_get_slot, ":string", "$map_talk_troop", slot_troop_honorific),
(str_store_string, 21, ":string"),
  (troop_get_slot, ":mission_object", "$g_talk_troop", slot_troop_mission_object),
   (str_store_faction_name, s31, ":mission_object"),
   (troop_get_slot, ":target_troop", "$g_talk_troop", dplmc_slot_troop_mission_diplomacy),

(str_store_troop_name, s14, ":target_troop"),
               ],
"Well, {s21}, at last I've found you. I have returned from my persuasion mission to {s31}. {s14} agreed to join you.","companion_rejoin_response", [
   (troop_get_slot, ":target_troop", "$g_talk_troop", dplmc_slot_troop_mission_diplomacy),
(call_script, "script_change_troop_faction", ":target_troop", "$players_kingdom"),

(store_faction_of_troop, ":target_faction", ":target_troop"),
(faction_get_slot, ":other_liege", ":target_faction", slot_faction_leader),
(try_begin),
  (store_relation, ":relation", "$players_kingdom", ":target_faction"),
  (ge, ":relation", 0),

  (call_script, "script_add_log_entry", logent_border_incident_troop_suborns_lord, "trp_player", -1, ":target_troop",":target_faction"),
  (store_add, ":slot_provocation_days", "$players_kingdom", slot_faction_provocation_days_with_factions_begin),
  (val_sub, ":slot_provocation_days", kingdoms_begin),
  #gekokujo 3.0 provocation days increase start
  (faction_set_slot, ":target_faction", ":slot_provocation_days", 60),
  #(faction_set_slot, ":target_faction", ":slot_provocation_days", 30),
  #gekokujo 3.0 provocation days increase end

  (faction_get_slot, ":other_liege", ":target_faction", slot_faction_leader),
  (call_script, "script_troop_change_relation_with_troop", "trp_player", ":other_liege", -3),
(try_end),

  (call_script, "script_change_player_right_to_rule", 2),
]],
##companion returning after spy request
[anyone, "event_triggered", [
    (store_conversation_troop, "$map_talk_troop"),
    (eq, "$map_talk_troop", "$npc_to_rejoin_party"),
    (troop_get_slot, ":mission", "$g_talk_troop", slot_troop_current_mission),
    (eq, ":mission", dplmc_npc_mission_spy_request),
    (troop_get_slot, ":emissary_caught", "$g_talk_troop", dplmc_slot_troop_mission_diplomacy),
    (troop_get_slot, ":mission_object", "$g_talk_troop", slot_troop_mission_object),
    (this_or_next|eq, ":emissary_caught", 0),
    (faction_slot_eq, ":mission_object", slot_faction_state, sfs_defeated),
    (troop_get_slot, ":string", "$map_talk_troop", slot_troop_honorific),
    (str_store_string, 21, ":string"),
    (str_store_faction_name, s31, ":mission_object"),
],
"Well, {s21}, at last I've found you. I have returned from my reconnaissance mission to {s31}. About which location do you need information?","dplmc_companion_spy_request_select_center", [
              ]],
##companion caught after spy request
[trp_hired_warrior_veteran, "event_triggered", [
    (store_conversation_troop, "$map_talk_troop"),
    (troop_get_slot, "$g_talk_troop", "$g_talk_troop", slot_troop_mission_object), #switching npc
    (troop_get_slot, ":mission", "$g_talk_troop", slot_troop_current_mission),
    (eq, ":mission", dplmc_npc_mission_spy_request),
    (troop_get_slot, ":emissary_caught", "$g_talk_troop", dplmc_slot_troop_mission_diplomacy),
	(gt, ":emissary_caught", 0),

    (troop_get_slot, ":mission_object", "$g_talk_troop", slot_troop_mission_object),
    (str_store_faction_name, s31, ":mission_object"),
    (str_store_troop_name, s11, "$g_talk_troop"),
               ],
"My, lord. I am coming back from the reconnaissance mission to {s31}. I am sorry, we were caught  off  guard and they got {s11}. I barely escaped.","close_window", [
  (troop_set_slot, "$g_talk_troop", slot_troop_current_mission, 0),
  (troop_set_slot, "$g_talk_troop", slot_troop_days_on_mission, 0),
  (troop_set_slot, "$g_talk_troop", slot_troop_occupation, 0),
  (assign, "$npc_to_rejoin_party", 0),

  (troop_get_slot, ":mission_object", "$g_talk_troop", slot_troop_mission_object),

  (call_script, "script_change_player_relation_with_faction", ":mission_object", -3),
  (call_script, "script_change_player_honor", -2),
  (call_script, "script_change_troop_renown", "trp_player", -5),

  (faction_get_slot, ":faction_leader", ":mission_object", slot_faction_leader),
  (call_script, "script_lord_get_home_center", ":faction_leader"),
  (try_begin),
    (neq, reg0, -1),
    (assign, ":target_party", reg0),
  (else_try),
    (try_for_range, ":walled_center", walled_centers_begin, walled_centers_end),
      (store_faction_of_party, ":center_faction", ":walled_center"),
         (eq, ":mission_object", ":center_faction"),
         (assign, ":target_party", ":walled_center"),
       (try_end),
  (try_end),
  (try_begin),
    (is_between, ":target_party", walled_centers_begin, walled_centers_end),
    (party_add_prisoners, ":target_party", "$g_talk_troop", 1),
  (try_end),
]],
##companion returning after alliance request
[anyone, "event_triggered", [
     (store_conversation_troop, "$map_talk_troop"),
     (eq, "$map_talk_troop", "$npc_to_rejoin_party"),
     (troop_get_slot, ":mission", "$g_talk_troop", slot_troop_current_mission),
          (eq, ":mission", dplmc_npc_mission_alliance_request),

          (troop_get_slot, ":string", "$map_talk_troop", slot_troop_honorific),
     (str_store_string, 21, ":string"),
          (troop_get_slot, ":mission_object", "$g_talk_troop", slot_troop_mission_object),
          (str_store_faction_name, s31, ":mission_object"),

          (call_script, "script_npc_decision_checklist_peace_or_war", ":mission_object", "fac_player_supporters_faction", "$g_talk_troop"),
          (assign, "$g_mission_result_with_player", reg0),
               ],
"Well, {s21}, at last I've found you. I have returned from my mission to {s31}. ","dplmc_companion_alliance_request_response", [
              ]],
##companion returning after defensive request
[anyone, "event_triggered", [
     (store_conversation_troop, "$map_talk_troop"),
     (eq, "$map_talk_troop", "$npc_to_rejoin_party"),
     (troop_get_slot, ":mission", "$g_talk_troop", slot_troop_current_mission),
          (eq, ":mission", dplmc_npc_mission_defensive_request),

          (troop_get_slot, ":string", "$map_talk_troop", slot_troop_honorific),
     (str_store_string, 21, ":string"),
          (troop_get_slot, ":mission_object", "$g_talk_troop", slot_troop_mission_object),
          (str_store_faction_name, s31, ":mission_object"),

          (call_script, "script_npc_decision_checklist_peace_or_war", ":mission_object", "fac_player_supporters_faction", "$g_talk_troop"),
          (assign, "$g_mission_result_with_player", reg0),
               ],
"Well, {s21}, at last I've found you. I have returned from my mission to {s31}. ","dplmc_companion_defensive_request_response", [
              ]],
##companion returning after trade request
[anyone, "event_triggered", [
     (store_conversation_troop, "$map_talk_troop"),
     (eq, "$map_talk_troop", "$npc_to_rejoin_party"),
     (troop_get_slot, ":mission", "$g_talk_troop", slot_troop_current_mission),
          (eq, ":mission", dplmc_npc_mission_trade_request),

          (troop_get_slot, ":string", "$map_talk_troop", slot_troop_honorific),
     (str_store_string, 21, ":string"),
          (troop_get_slot, ":mission_object", "$g_talk_troop", slot_troop_mission_object),
          (str_store_faction_name, s31, ":mission_object"),

          (call_script, "script_npc_decision_checklist_peace_or_war", ":mission_object", "fac_player_supporters_faction", "$g_talk_troop"),
          (assign, "$g_mission_result_with_player", reg0),
               ],
"Well, {s21}, at last I've found you. I have returned from my mission to {s31}. ","dplmc_companion_trade_request_response", [
              ]],
##companion returning after nonaggression request
[anyone, "event_triggered", [
     (store_conversation_troop, "$map_talk_troop"),
     (eq, "$map_talk_troop", "$npc_to_rejoin_party"),
     (troop_get_slot, ":mission", "$g_talk_troop", slot_troop_current_mission),
          (eq, ":mission", dplmc_npc_mission_nonaggression_request),

          (troop_get_slot, ":string", "$map_talk_troop", slot_troop_honorific),
     (str_store_string, 21, ":string"),
          (troop_get_slot, ":mission_object", "$g_talk_troop", slot_troop_mission_object),
          (str_store_faction_name, s31, ":mission_object"),

          (call_script, "script_npc_decision_checklist_peace_or_war", ":mission_object", "fac_player_supporters_faction", "$g_talk_troop"),
          (assign, "$g_mission_result_with_player", reg0),
               ],
"Well, {s21}, at last I've found you. I have returned from my mission to {s31}. ","dplmc_companion_nonaggression_request_response", [
              ]],
##companion returning after war request
[anyone, "event_triggered", [
(store_conversation_troop, "$map_talk_troop"),
(eq, "$map_talk_troop", "$npc_to_rejoin_party"),
(troop_get_slot, ":mission", "$g_talk_troop", slot_troop_current_mission),
(eq, ":mission", dplmc_npc_mission_war_request),

(troop_get_slot, ":string", "$map_talk_troop", slot_troop_honorific),
(str_store_string, 21, ":string"),
(troop_get_slot, ":mission_object", "$g_talk_troop", slot_troop_mission_object),
(str_store_faction_name, s31, ":mission_object"),

(call_script, "script_npc_decision_checklist_peace_or_war", ":mission_object", "fac_player_supporters_faction", "$g_talk_troop"),
(assign, "$g_mission_result_with_player", reg0),
(call_script, "script_npc_decision_checklist_peace_or_war", ":mission_object", "$diplomacy_var", -1),
(assign, "$g_mission_result_with_target", reg0),
##diplomacy start+
#Disable agreeing to declare war when the kingdoms are allied.
#Make it less likely when they have other treaties.
(call_script, "script_dplmc_get_faction_truce_length_with_faction", ":mission_object", "$diplomacy_var"),
(try_begin),
	#TODO: Later there should be other intrigue options, but for now let's just
	#make it so refusal is automatic for alliances, and possible for other types.
	(gt, reg0, dplmc_treaty_defense_days_expire),
	(val_max, "$g_mission_result_with_target", 3),#Positive means does not want war
(else_try),
	(gt, reg0, dplmc_treaty_truce_days_expire),
	(store_random_in_range, reg0, 0, 2),
	(try_begin),
		(eq, reg0, 1),
		(val_max, "$g_mission_result_with_target", 3),#Positive means does not want war
	(else_try),
		(val_add, "$g_mission_result_with_target", 1),#If was undecided, choose no
		(val_max, "$g_mission_result_with_target", 0),#Best result is "undecided"
	(try_end),
(try_end),
##diplomacy end+
               ],
"Well, {s21}, at last I've found you. I have returned from my mission to {s31}. ","dplmc_companion_war_request_response", [
              ]],
[anyone, "event_triggered", [
               (eq, "$g_infinite_camping", 0),
               (store_conversation_troop, "$map_talk_troop"),
          (is_between, "$map_talk_troop", companions_begin, companions_end),
               (eq, "$map_talk_troop", "$npc_is_quitting"),
               (troop_get_slot, ":honorific", "$map_talk_troop", slot_troop_honorific),
               (str_store_string, 5, ":honorific")],
"Excuse me {s5} -- there is something I need to tell you.", "companion_quitting", [
              (assign, "$npc_is_quitting", 0),
              (assign, "$player_can_persuade_npc", 1),
              (assign, "$player_can_refuse_npc_quitting", 1),
 ]],
#Morality objections
[anyone, "event_triggered", [
               (store_conversation_troop, "$map_talk_troop"),
          (is_between, "$map_talk_troop", companions_begin, companions_end),

               (eq, "$map_talk_troop", "$npc_with_grievance"),
               (eq, "$npc_map_talk_context", slot_troop_morality_state),


               (try_begin),
                   (eq, "$npc_grievance_slot", slot_troop_morality_state),
                   (troop_get_slot, ":speech", "$map_talk_troop", slot_troop_morality_speech),
               (else_try),
                   (troop_get_slot, ":speech", "$map_talk_troop", slot_troop_2ary_morality_speech),
               (try_end),
               (str_store_string, 21, "$npc_grievance_string"),
               (str_store_string, 5, ":speech"),
               ],
"{s5}", "companion_objection_response", [
              (assign, "$npc_with_grievance", 0),
 ]],
[anyone, "event_triggered", [
               (eq, "$g_infinite_camping", 0),
               (eq, "$npc_map_talk_context", slot_troop_home),
               (store_conversation_troop, "$map_talk_troop"),
          (is_between, "$map_talk_troop", companions_begin, companions_end),

               (troop_get_slot, ":speech", "$map_talk_troop", slot_troop_home_intro),
               (str_store_string, s5, ":speech"),
               ],
"{s5}", "companion_home_description", [
              (troop_set_slot, "$map_talk_troop", slot_troop_home_speech_delivered, 1),
 ]],
[anyone,"event_triggered", [
(eq, "$talk_context", tc_rebel_thanks),
(store_conversation_troop, "$g_talk_troop"),
(is_between, "$g_talk_troop", pretenders_begin, pretenders_end),

(troop_get_slot, ":old_faction", "$g_talk_troop", slot_troop_original_faction),
(str_store_faction_name, s3, ":old_faction"),
(str_store_string, s6, "@{playername}, when we started our long walk, few people had the courage to support me.\
And fewer still would be willing to put their lives at risk for my cause.\
But you didn't hesitate for a moment in throwing yourself at my enemies.\
We have gone through a lot together, and there were times I came close to losing all hope.\
But with God's help, we prevailed. It is now time for me to leave your company and take what's rightfully mine.\
From now on, I will carry out the great responsibility of ruling {s3}.\
There still lie many challanges ahead and I count on your help in overcoming those.\
And of course, you will always remain as my foremost vassal."),
],
"{s6}", "rebel_thanks_answer",
[

(unlock_achievement, ACHIEVEMENT_KINGMAKER),
(call_script, "script_end_quest", "qst_rebel_against_kingdom"),

     (try_begin),
       (troop_get_type, ":is_female", "trp_player"),
       (eq, ":is_female", 1),

       (troop_get_type, ":is_female", "$g_talk_troop"),
       (eq, ":is_female", 1),

       (unlock_achievement, ACHIEVEMENT_GIRL_POWER),
     (try_end),
 ]],
[anyone|plyr,"rebel_thanks_answer", [], "It was an honour to fight for your cause, {reg65?madame:my lord}.", "rebel_thanks_answer_2", []],
[anyone|plyr,"rebel_thanks_answer", [], "You will always have my loyal support, {reg65?my lady:sir}.", "rebel_thanks_answer_2", []],
[anyone,"rebel_thanks_answer_2", [], "I will miss living this life of adventure with you, but my duties await me. So... farewell for now, {playername}.\
I hope I'll see you again soon.", "close_window", []],
[anyone, "event_triggered", [
               (store_conversation_troop, "$map_talk_troop"),
          (is_between, "$map_talk_troop", companions_begin, companions_end),

               (eq, "$map_talk_troop", "$npc_with_political_grievance"),
               (eq, "$npc_map_talk_context", slot_troop_kingsupport_objection_state),

          (store_sub, ":npc_no", "$g_talk_troop", "trp_npc1"),
          (store_add, ":string", "str_npc1_kingsupport_objection", ":npc_no"),
#					 (troop_get_slot, ":string", "$map_talk_troop", slot_troop_kingsupport_objection_string),
               (str_store_string, 21, ":string"),
               ],
"{s21}", "companion_political_grievance_response", [
              (assign, "$npc_with_political_grievance", 0),
         (troop_set_slot, "$map_talk_troop", slot_troop_kingsupport_objection_state, 2),

 ]],
[anyone, "event_triggered", [
               (store_conversation_troop, "$map_talk_troop"),
		  #gekokujo 3.0 microfactions! include fort companions start
          #(is_between, "$map_talk_troop", companions_begin, companions_end),
          (is_between, "$map_talk_troop", companions_begin, fort_companions_end),
		  #gekokujo 3.0 microfactions! include fort companions end

               (eq, "$map_talk_troop", "$npc_to_rejoin_party"),
          (neg|main_party_has_troop, "$map_talk_troop"),

               (troop_slot_eq, "$map_talk_troop", slot_troop_current_mission, npc_mission_rejoin_when_possible),
          (troop_slot_eq, "$map_talk_troop", slot_troop_occupation, slto_player_companion),
          (troop_get_slot, ":string", "$map_talk_troop", slot_troop_honorific),
               (str_store_string, 21, ":string"),
          ],
"Greetings, {s21}. Are you ready for me to rejoin you?"	,
          "companion_rejoin_response",
         [
              (assign, "$npc_to_rejoin_party", 0),
         ]],
[anyone, "event_triggered", [
               (store_conversation_troop, "$map_talk_troop"),
          (is_between, "$map_talk_troop", companions_begin, companions_end),

               (eq, "$map_talk_troop", "$npc_to_rejoin_party"),
#                     (eq, "$npc_map_talk_context", slot_troop_days_on_mission),
               (troop_slot_eq, "$g_talk_troop", slot_troop_current_mission, npc_mission_kingsupport),

          (troop_get_slot, ":string", "$map_talk_troop", slot_troop_honorific),
               (str_store_string, 21, ":string"),
               ],
"Well, {s21}, at last I've found you. I've been out spreading the word about your claim, and am now ready to rejoin the company.", "companion_rejoin_response", [
              (assign, "$npc_to_rejoin_party", 0),
         (call_script, "script_change_player_right_to_rule", 3),
         (troop_set_slot, "$g_talk_troop", slot_troop_kingsupport_state, 1),

         (try_begin),
            (is_between, "$player_right_to_rule", 10, 15),
            (call_script, "script_add_log_entry", logent_player_claims_throne_1, "trp_player", 0, 0, 0),
         (else_try),
            (is_between, "$player_right_to_rule", 20, 25),
            (call_script, "script_add_log_entry", logent_player_claims_throne_2, "trp_player", 0, 0, 0),
         (try_end),
         ]],
[anyone, "event_triggered", [
 (store_conversation_troop, "$map_talk_troop"),
#gekokujo 3.0 microfactions! include fort companions start
#(is_between, "$map_talk_troop", companions_begin, companions_end),
(is_between, "$map_talk_troop", companions_begin, fort_companions_end),
#gekokujo 3.0 microfactions! include fort companions end
 (eq, "$map_talk_troop", "$npc_to_rejoin_party"),
#                     (eq, "$npc_map_talk_context", slot_troop_days_on_mission),
 (troop_slot_eq, "$map_talk_troop", slot_troop_current_mission, npc_mission_gather_intel),

(troop_get_slot, ":string", "$map_talk_troop", slot_troop_honorific),
 (str_store_string, 21, ":string"),

(troop_get_slot, ":town_with_contacts", "$map_talk_troop", slot_troop_town_with_contacts),
(store_faction_of_party, ":town_faction", ":town_with_contacts"),

(call_script, "script_update_faction_political_notes", ":town_faction"),
(assign, ":instability_index", reg0),
(val_add, ":instability_index", reg0),
(val_add, ":instability_index", reg1),


(str_store_faction_name, s12, ":town_faction"),
(try_begin),
   (ge, ":instability_index", 60),
   (str_store_string, s11, "str_the_s12_is_a_labyrinth_of_rivalries_and_grudges_lords_ignore_their_lieges_summons_and_many_are_ripe_to_defect"),
(else_try),
   (ge, ":instability_index", 40),
   (str_store_string, s11, "str_the_s12_is_shaky_many_lords_do_not_cooperate_with_each_other_and_some_might_be_tempted_to_defect_to_a_liege_that_they_consider_more_worthy"),
(else_try),
   (ge, ":instability_index", 20),
   (str_store_string, s11, "str_the_s12_is_fairly_solid_some_lords_bear_enmities_for_each_other_but_they_tend_to_stand_together_against_outside_enemies"),
(else_try),
   (str_store_string, s11, "str_the_s12_is_a_rock_of_stability_politically_speaking_whatever_the_lords_may_think_of_each_other_they_fight_as_one_against_the_common_foe"),
(try_end),

(try_for_range, ":lord", active_npcs_begin, active_npcs_end),
   (troop_slot_eq, ":lord", slot_troop_occupation, slto_kingdom_hero),
   (store_faction_of_troop, ":lord_faction", ":lord"),
   (eq, ":lord_faction", ":town_faction"),
   (call_script, "script_update_troop_political_notes", ":lord"),
(try_end),

 ],
"Well, {s21}, at last I've found you. {s11}. The rest of my report I submit to you in writing.", "companion_rejoin_response", [
]],
[anyone, "event_triggered", [
               (store_conversation_troop, "$map_talk_troop"),
		  #gekokujo 3.0 microfactions! include fort companions start
          #(is_between, "$map_talk_troop", companions_begin, companions_end),
          (is_between, "$map_talk_troop", companions_begin, fort_companions_end),
		  #gekokujo 3.0 microfactions! include fort companions end

               (eq, "$map_talk_troop", "$npc_to_rejoin_party"),
#                     (eq, "$npc_map_talk_context", slot_troop_days_on_mission),
               (troop_get_slot, ":mission", "$g_talk_troop", slot_troop_current_mission),
          (this_or_next|eq, ":mission", npc_mission_peace_request),
          (this_or_next|eq, ":mission", npc_mission_pledge_vassal),
          (this_or_next|eq, ":mission", npc_mission_test_waters),
          (this_or_next|eq, ":mission", npc_mission_non_aggression),
            (eq, ":mission", npc_mission_seek_recognition),

          (troop_get_slot, ":string", "$map_talk_troop", slot_troop_honorific),
               (str_store_string, 21, ":string"),
          (troop_get_slot, ":mission_object", "$g_talk_troop", slot_troop_mission_object),
          (str_store_faction_name, s31, ":mission_object"),

          (call_script, "script_npc_decision_checklist_peace_or_war", ":mission_object", "fac_player_supporters_faction", "$g_talk_troop"),
          (assign, "$g_mission_result", reg0),
##diplomacy start+
		(try_begin),
			(ge, "$cheat_mode", 1),
			(display_message, "@{!} DEBUG - Native checklist-peace-or-war result {reg0}, because {s14}"),
		(try_end),
		#make gender correct
		(faction_get_slot, ":emissary_object", ":mission_object", slot_faction_leader),
		(call_script, "script_dplmc_store_troop_is_female", ":emissary_object"),
               ],#next line "him" to {reg0?her:him}
#diplomacy begin
"Well, {s21}, at last I've found you. I have returned from my mission to {s31}. In general, I would say, {s14}. Nevertheless I tried to convince {reg0?her:him}.","companion_embassy_results", [
#diplomacy end
         ]],
[anyone, "event_triggered", [
#gekokujo 3.0 microfactions! include fort companions start
#(is_between, "$g_talk_troop", companions_begin, companions_end),
(is_between, "$g_talk_troop", companions_begin, fort_companions_end),
#gekokujo 3.0 microfactions! include fort companions end
(neg|troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_hero),
(neg|main_party_has_troop, "$g_talk_troop"),
               ],
"Would you have me rejoin you?", "companion_rejoin_response", [
(assign, "$map_talk_troop", "$g_talk_troop"),
 ]],
#caravan merchants
[anyone, "event_triggered",
[(eq, "$caravan_escort_state",1),
(eq, "$g_encountered_party","$caravan_escort_party_id"),
(le, "$talk_context",tc_party_encounter),
(store_distance_to_party_from_party, reg0, "$caravan_escort_destination_town", "$caravan_escort_party_id"),
(lt, reg0, 5),
(str_store_party_name, s3, "$caravan_escort_destination_town"),
(assign, reg3, "$caravan_escort_agreed_reward"),
],
"There! I can see the walls of {s3} in the distance. We've made it safely.\
Here, take this purse of {reg3} mon, as I promised. I hope we can travel together again someday.", "close_window",
[
(assign,"$caravan_escort_state",0),
(call_script, "script_troop_add_gold", "trp_player", "$caravan_escort_agreed_reward"),
(assign,reg(4), "$caravan_escort_agreed_reward"),
(val_mul,reg(4), 1),
(add_xp_as_reward,reg(4)),
(assign, "$g_leave_encounter",1),
]],
#gekokujo 3.1 random encounters start
[anyone, "event_triggered", 
  [
    (eq, "$npc_map_talk_context", tc_gekokujo_encounter),
    (store_conversation_troop, "$encounter_talk_troop"),
    (eq, "$encounter_talk_troop", "$gekokujo_encounter_boss"),
    
    (store_random_in_range, ":offset", 0, 20),
    (val_add, ":offset", "str_gekokujo_encounter_dialogue_1"),
    (str_store_string, s5, ":offset"),
    
    #let's hope this works
    (store_random_in_range, "$gekokujo_encounter_reply_1", 0, 10),
    (val_add, "$gekokujo_encounter_reply_1", "str_gekokujo_encounter_choice_1"),
    
    (store_random_in_range, "$gekokujo_encounter_reply_2", 0, 9),
    (try_begin),
      (eq, "$gekokujo_encounter_reply_1", "$gekokujo_encounter_reply_2"),
      (val_add, "$gekokujo_encounter_reply_2", 1),
    (try_end),
    (val_add, "$gekokujo_encounter_reply_2", "str_gekokujo_encounter_choice_1"),
  ],
  "{s5}", 
  "gekokujo_encounter_reply_1", []],
#gekokujo 3.1 random encounters end

[anyone, "event_triggered", [
               ],
"{!}Sorry -- just talking to myself [ERROR- {s51}]", "close_window", [
 ]],
#KINGDOM LORD DIALOGS BEGINS HERE




#gekokujo 3.0 freelancer return to lord after defeat start
#this should be in freelancer_dialogs but i don't wanna fuck with the modmerger framework, i really really don't
[anyone,"start",
	[
		(eq, "$g_talk_troop", "$enlisted_lord"),
		(eq, "$freelancer_state", 3),
		(neg|troop_slot_eq, "$g_talk_troop", slot_troop_prisoner_of_party, "$g_encountered_party"), #this shouldn't happen in prison
		(neg|eq, "$talk_context", tc_hero_freed), #this also shouldn't happen immediately after the prison break
		#(ge, "$g_talk_troop_faction_relation", 0),
		#(neq, "$players_kingdom", "$g_talk_troop_faction"),
		#(eq, "$players_kingdom", 0),
		#(ge, "$g_talk_troop_relation", 0),
	],
        "{playername}, you survived! And to return to me after what happened? You are what all samurai should aspire to.", "lord_pretalk",
	[
        (call_script, "script_dismiss_companions"), #gekokujo 3.0 dismiss companions at enlistment
		(call_script, "script_party_copy", "p_freelancer_party_backup", "p_main_party"),
		(remove_member_from_party, "trp_player","p_freelancer_party_backup"),
		
		(call_script, "script_freelancer_equip_troop", "$player_cur_troop"),
		
		(call_script, "script_troop_change_relation_with_troop", "$g_talk_troop", "trp_player", 10),
		(call_script, "script_change_troop_renown", "trp_player", 10),
		(call_script, "script_change_player_honor", 10),
		
        (call_script, "script_event_player_returns_defeat"),
	]
],
	
#gekokujo 3.0 freelancer return to lord after defeat end

#FEMALE PLAYER CHACTER WEDDING (also go to the feast, 'lift a glass' speeches for npc lords)
#Feast not yet organized
[anyone, "start", [
(lt, "$talk_context", tc_siege_commander),

(check_quest_active, "qst_wed_betrothed_female"),
(quest_slot_eq, "qst_wed_betrothed_female", slot_quest_giver_troop, "$g_talk_troop"),
(neg|faction_slot_eq, "$g_talk_troop_faction", slot_faction_ai_state, sfai_feast),

(store_current_hours, ":hours_since_betrothal"),
(troop_get_slot, ":betrothal_time", "$g_talk_troop", slot_troop_betrothal_time),
(val_sub, ":hours_since_betrothal", ":betrothal_time"),
(lt, ":hours_since_betrothal", 720), #30 days
(str_clear, s12),
(try_begin),
(neg|faction_slot_eq, "$g_talk_troop_faction", slot_faction_ai_state, sfai_feast),
(neg|faction_slot_eq, "$g_talk_troop_faction", slot_faction_ai_state, sfai_default),
(str_store_string, s12, "@ We will of course need to wait until the domain is no longer on campaign."),
(try_end),
],
#diplomacy start+ gender-correct language
"My {lord/lady}, I look forward to our marriage, as soon as there is an opportunity to hold a proper feast.{s12}", "lord_start", [
#diplomacy end+
]],
#Feast, but not at the venue
[anyone, "start", [
(lt, "$talk_context", tc_siege_commander),

(check_quest_active, "qst_wed_betrothed_female"),
(quest_slot_eq, "qst_wed_betrothed_female", slot_quest_giver_troop, "$g_talk_troop"),
(faction_slot_eq, "$g_talk_troop_faction", slot_faction_ai_state, sfai_feast),
(faction_get_slot, ":feast_venue", "$g_talk_troop_faction", slot_faction_ai_object),
(party_slot_eq, "$g_talk_troop_party", slot_party_ai_state, spai_holding_center),
(party_slot_eq, "$g_talk_troop_party", slot_party_ai_object, ":feast_venue"),

(neq, ":feast_venue", "$g_encountered_party"),
(str_store_party_name, s4, ":feast_venue"),
],
#diplomacy start+ gender-correct language
"My {lord/lady}, if you wish to marry, we can proceed to the feast at {s4} to exchange vows before the hereditary vassals of the clan.", "lord_start", [
#diplomacy end+
]],
#Over a month, and heading to a center
[anyone, "start", [
(lt, "$talk_context", tc_siege_commander),

(check_quest_active, "qst_wed_betrothed_female"),
(quest_slot_eq, "qst_wed_betrothed_female", slot_quest_giver_troop, "$g_talk_troop"),

(store_current_hours, ":hours_since_betrothal"),
(troop_get_slot, ":betrothal_time", "$g_talk_troop", slot_troop_betrothal_time),
(val_sub, ":hours_since_betrothal", ":betrothal_time"),
(ge, ":hours_since_betrothal", 720), #30 days

(party_get_attached_to, ":attached", "$g_talk_troop_party"),
(neg|is_between, ":attached", walled_centers_begin, walled_centers_end),

(party_slot_eq, "$g_talk_troop_party", slot_party_ai_state, spai_holding_center),
(party_get_slot, ":object", "$g_talk_troop_party", slot_party_ai_object),
(str_store_party_name, s4, ":object"),
],
#diplomacy start+ gender-correct language
"My {lord/lady}, I grow tired of waiting for the lords of this domain to assemble. Come with me to {s4} exchange our vows.", "lord_start", [
#diplomacy end+
]],
#Over a month, but not in a center
[anyone, "start", [
(lt, "$talk_context", tc_siege_commander),
(check_quest_active, "qst_wed_betrothed_female"),
(quest_slot_eq, "qst_wed_betrothed_female", slot_quest_giver_troop, "$g_talk_troop"),

(store_current_hours, ":hours_since_betrothal"),
(troop_get_slot, ":betrothal_time", "$g_talk_troop", slot_troop_betrothal_time),
(val_sub, ":hours_since_betrothal", ":betrothal_time"),
(ge, ":hours_since_betrothal", 0), #30 days

(party_get_attached_to, ":attached", "$g_talk_troop_party"),
(neg|is_between, ":attached", walled_centers_begin, walled_centers_end),

],
#diplomacy start+ gender-correct language
"My {lord/lady}, I grow tired of waiting for the lords of this domain to assemble. Perhaps we should take the first opportunity to marry, in any great hall that is open to us.", "lord_start", [
#diplomacy end+
]],
[anyone, "start", [
(lt, "$talk_context", tc_siege_commander),
(check_quest_active, "qst_wed_betrothed_female"),
(quest_slot_eq, "qst_wed_betrothed_female", slot_quest_giver_troop, "$g_talk_troop"),
(this_or_next|neg|faction_slot_eq, "$g_talk_troop_faction", slot_faction_ai_state, sfai_feast),
(neg|faction_slot_eq, "$g_talk_troop_faction", slot_faction_ai_object, "$g_encountered_party"),
],
#diplomacy start+ gender-correct language
"My {lord/lady}, I have grown tired of waiting. Let us proceed with the vows immediately.", "lord_groom_vows", [
#diplomacy end+
]],
[anyone, "start", [
(lt, "$talk_context", tc_siege_commander),
(check_quest_active, "qst_wed_betrothed_female"),
(quest_slot_eq, "qst_wed_betrothed_female", slot_quest_giver_troop, "$g_talk_troop"),
],
#diplomacy start+ gender-correct language
"My {lord/lady}, my eyes rejoice to see you. We may proceed with the vows.", "lord_groom_vows", [
#diplomacy end+
]],
[anyone|plyr, "female_pc_marriage_vow", [
],
#diplomacy start+ (female player/male lord) or (male player/female lord)
"I vow to take you as my {reg65?wife:husband}.", "lord_groom_wedding_complete", [
#diplomacy end+
(call_script, "script_courtship_event_bride_marry_groom", "trp_player", "$g_talk_troop", 0),
(call_script, "script_end_quest", "qst_wed_betrothed_female"),
]],
[anyone|plyr, "female_pc_marriage_vow", [
],
"Wait -- I need to think about this.", "close_window", [
(assign, "$g_leave_encounter", 1),
]],
# KINGDOM LORD DUEL OUTCOMES
[anyone,"start",
[(eq, "$talk_context", tc_after_duel),
(check_quest_active, "qst_denounce_lord"),
(check_quest_succeeded, "qst_denounce_lord"),
(quest_slot_eq, "qst_denounce_lord", slot_quest_target_troop, "$g_talk_troop"),
],
"Very well. You've made your point. I have nothing more to say.", "close_window", [
(call_script, "script_change_troop_renown", "trp_player", 10),
(assign, "$g_leave_encounter", 1),
]],
[anyone,"start",
[(eq, "$talk_context", tc_after_duel),
(check_quest_active, "qst_denounce_lord"),
(check_quest_failed, "qst_denounce_lord"),
(quest_slot_eq, "qst_denounce_lord", slot_quest_target_troop, "$g_talk_troop"),
],
"Well, {sir/my lady}! Please, do not trouble yourself to rise from the ground, as I would simply have to knock you down again. I shall take your silence as an apology. Good day to you.", "close_window", [
(call_script, "script_change_troop_renown", "trp_player", -10),
(assign, "$g_leave_encounter", 1),
]],
[anyone,"start",
[(eq, "$talk_context", tc_after_duel),
(assign, "$temp", 0),
(try_begin),
(check_quest_active, "qst_duel_avenge_insult"),
(check_quest_succeeded, "qst_duel_avenge_insult"),
(quest_slot_eq, "qst_duel_avenge_insult", slot_quest_target_troop, "$g_talk_troop"),
(assign, "$temp", 1),
(else_try),
(check_quest_active, "qst_duel_for_lady"),
(check_quest_succeeded, "qst_duel_for_lady"),
(quest_slot_eq, "qst_duel_for_lady", slot_quest_target_troop, "$g_talk_troop"),
(assign, "$temp", 2),
(try_end),
(gt, "$temp", 0),
],
"Very well. You've made your point. I retract what I said. I hope you have obtained satisfaction.", "close_window", [
(try_begin),
(eq, "$temp", 1),
(call_script, "script_change_troop_renown", "trp_player", 10),
(call_script, "script_end_quest", "qst_duel_avenge_insult"),
(try_end),
(assign, "$g_leave_encounter", 1),
]],
[anyone,"start",
[(eq, "$talk_context", tc_after_duel),
(assign, "$temp", 0),
(try_begin),
(check_quest_active, "qst_duel_avenge_insult"),
(check_quest_failed, "qst_duel_avenge_insult"),
(quest_slot_eq, "qst_duel_avenge_insult", slot_quest_target_troop, "$g_talk_troop"),
(assign, "$temp", 1),
(else_try),
(check_quest_active, "qst_duel_for_lady"),
(check_quest_failed, "qst_duel_for_lady"),
(quest_slot_eq, "qst_duel_for_lady", slot_quest_target_troop, "$g_talk_troop"),
(assign, "$temp", 2),
(try_end),
(gt, "$temp", 0),
],
"Hah! Not so gallant now, are we? Now trouble me no more.", "close_window", [
(try_begin),
(eq, "$temp", 1),
(call_script, "script_change_troop_renown", "trp_player", -10),
(call_script, "script_end_quest", "qst_duel_avenge_insult"),
(try_end),
(assign, "$g_leave_encounter", 1),
]],
[anyone,"start",
[(eq, "$talk_context", tc_after_duel),
(check_quest_active, "qst_duel_courtship_rival"),
(check_quest_succeeded, "qst_duel_courtship_rival"),
(quest_slot_eq, "qst_duel_courtship_rival", slot_quest_target_troop, "$g_talk_troop"),
(quest_get_slot, ":duel_object", "qst_duel_courtship_rival", slot_quest_giver_troop),
(str_store_troop_name, s10, ":duel_object"),
],
##diplomacy start+ replace bastard with gender-appropriate insult
#(TODO: perhaps a culturally-appropriate reference instead)
"Very well -- you have won. Let all those present today witness that you have defeated me, and I shall abandon my suit of {s10}. Are you satisfied, you heartless {bastard/bitch}?", "close_window", [
##diplomacy end+
(quest_get_slot, ":duel_object", "qst_duel_courtship_rival", slot_quest_giver_troop),
(call_script, "script_courtship_event_lady_break_relation_with_suitor", ":duel_object", "$g_talk_troop"),
(assign, "$g_leave_encounter", 1),
]],
[anyone,"start",
[(eq, "$talk_context", tc_after_duel),
(check_quest_active, "qst_duel_courtship_rival"),
(check_quest_failed, "qst_duel_courtship_rival"),
(quest_slot_eq, "qst_duel_courtship_rival", slot_quest_target_troop, "$g_talk_troop"),
(quest_get_slot, ":duel_object", "qst_duel_courtship_rival", slot_quest_giver_troop),
(str_store_troop_name, s10, ":duel_object"),
##diplomacy start+
(call_script, "script_dplmc_store_troop_is_female", ":duel_object"),#enable the male version
],
##replace "man" with "{man/woman}", and "her" with "{reg0?her:him}"
"Get up. Let all those present today witness that I have defeated you, and you are now bound to relinquish your suit of the {s10}. I will permit you one final visit, to make your farewells. After that, if you persist in attempting to see {reg0?her:him}, everyone shall know that you are a {man/woman} of scant honor.", "close_window", [
##diplomacy end+
(assign, "$g_leave_encounter", 1),
]],
[anyone,"start", [(eq, "$talk_context", tc_castle_commander)],
"What do you want?", "player_siege_castle_commander_1", []],
[anyone|plyr,"player_siege_castle_commander_1", [],
"Surrender! Your situation is hopeless!", "player_siege_ask_surrender", []],
[anyone|plyr,"player_siege_castle_commander_1", [], "Nothing. I'll leave you now.", "close_window", []],
[anyone,"player_siege_ask_surrender", [(lt, "$g_enemy_strength", 100), (store_mul,":required_str","$g_enemy_strength",5),(ge, "$g_ally_strength", ":required_str")],
"Perhaps... Do you give your word of honour that we'll be treated well?", "player_siege_ask_surrender_treatment", []],
[anyone,"player_siege_ask_surrender", [(lt, "$g_enemy_strength", 200), (store_mul,":required_str","$g_enemy_strength",3),(ge, "$g_ally_strength", ":required_str")],
"We are ready to leave this castle to you and march away if you give me your word of honour that you'll let us leave unmolested.", "player_siege_ask_leave_unmolested", []],
##diplomacy start+
#Make the AI willing to surrender in other situations when it is utterly outclassed
[anyone,"player_siege_ask_surrender", [
	(ge, "$g_dplmc_ai_changes", DPLMC_AI_CHANGES_LOW),#only enable if AI changes are active
	(assign, reg0, 0),
	(try_begin),
		#I assume that $g_encountered_party is the town, but this could be wrong
		(neg|party_slot_eq, "$g_encountered_party", slot_party_type, spt_castle),
		(neg|party_slot_eq, "$g_encountered_party", slot_party_type, spt_town),
		(try_begin),
			(ge, "$cheat_mode", 1),
			(assign, reg0, "$g_encountered_party"),
			(str_store_party_name, s0, "$g_encountered_party"),
			(party_get_slot, reg1, "$g_encountered_party", slot_party_type),
			(display_message, "@{!}Party at address {reg0} named {s0} has slot_party_type {reg1} (not castle or town)"),
		(try_end),
		(assign, reg0, 1),#<- don't continue
	(try_end),
	(eq, reg0, 0),
	#Don't bother continuing if the attackers don't outnumber the defenders by a decent ratio.
	(store_mul, reg0,"$g_enemy_strength", 3),
	(ge, "$g_ally_strength", reg0),

	#Enemy must be below a certain strength to even consider giving up.
	(game_get_reduce_campaign_ai, ":reduce_campaign_ai"),
	(this_or_next|lt, "$g_enemy_strength", 500),# Hard (would be described as "small bands" on the world map)
		(ge, ":reduce_campaign_ai", 1),
	(this_or_next|lt, "$g_enemy_strength", 1000),# Medium ("enemy patrols")
		(ge, ":reduce_campaign_ai", 2),
	(lt, "$g_enemy_strength", 2000),# Easy ("medium-sized group")

	#Prevent forts from surrendering to five men and a mule.
	(assign, ":defender_str", "$g_enemy_strength"),
	(val_max, ":defender_str", 5),#establish a minimum (if you can't just walk in, there must be some defenders)
	(try_begin),
		#Not that it matters much, given how extremely low it is, but increase the minimum for towns.
		(party_slot_eq, "$g_encountered_party", slot_party_type, spt_town),
		(val_max, ":defender_str", 10),
	(try_end),

	#Count fortresses and original fortresses for use below
	(assign, ":forts_held", 0),
	(assign, ":starting_forts", 0),
	(try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
		(store_faction_of_party, reg0, ":center_no"),
		(try_begin),
			(eq, reg0, "$g_encountered_party_faction"),
			(val_add, ":forts_held", 1),
		(try_end),
		(try_begin),
			(party_slot_eq, ":center_no", slot_center_original_faction, "$g_encountered_party_faction"),
			(val_add, ":starting_forts", 1),
		(try_end),
	(try_end),

	#Always refuse to retreat if this is the last fortress
	(gt, ":forts_held", 1),

	#Always refuse to abandon a fort if they don't have more than 50% of their original size.
	(store_mul, reg0, ":forts_held", 2),
	(gt, reg0, ":starting_forts"),

	#Always refuse to abandon a native fort if they don't have more than 100% of their original size
	(assign, ":is_native", 0),
	(try_begin),
		(is_between, "$g_encountered_party_faction", npc_kingdoms_begin, npc_kingdoms_end),#this bonus is only intended for ordinary factions
		(this_or_next|party_slot_eq, "$g_talk_troop", slot_troop_original_faction, "$g_encountered_party_faction"),
			(party_slot_eq, "$g_encountered_party", slot_center_original_faction, "$g_encountered_party_faction"),
		(assign, ":is_native", 1),
	(try_end),

	(this_or_next|gt, ":forts_held", ":starting_forts"),
		(eq, ":is_native", 0),

	#Now determine the number of attacking troops required to surrender.
	#Default requirement is being outnumbered 8-to-1
	(assign, ":surrender_ratio_10", 80),

	#Adjust values based on defending commander's personality
	(try_begin),
		#Companions who like retreating are more likely to surrender
		(call_script, "script_dplmc_get_troop_morality_value", "$g_talk_troop", tmt_aristocratic),
		(lt, reg0, 0),
		#On normal will agree if outnumbered 4-to-1
		(val_div, ":surrender_ratio_10", 2),
	(else_try),
		#Companions who dislike retreating will be less likely to surrender
		(this_or_next|ge, reg0, 1),#<- value for tmt_aristocratic
		#The same goes for martial, self-righteous, and quarrelsome lords.
		(this_or_next|troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_martial),
		(this_or_next|troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_quarrelsome),
		(troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_selfrighteous),
		#Exaggerate the effect of this to make it more noticable.
		#On normal will agree if outnumbered 16-to-1.
		(val_mul, ":surrender_ratio_10", 2),
	(else_try),
		#Faction leaders are more tenacious either when defending native territory, or when
		#their faction is at less than 80% strength.
		(this_or_next|is_between, "$g_talk_troop", kings_begin, kings_end),
		(this_or_next|is_between, "$g_talk_troop", pretenders_begin, pretenders_end),
			(faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, "$g_talk_troop"),
		(store_mul, reg0, ":forts_held", 5),
		(val_div, reg0, 4),
		(this_or_next|lt, reg0, ":starting_forts"),
			(ge, ":is_native", 1),
		#On normal will agree if outnumbered 16-to-1.
		(val_mul, ":surrender_ratio_10", 2),
	(else_try),
		#Ladies with traditional upbringings (other than adventurous ones) are also more likely to run away.
		#So are roguish commoners without a positive tmt_aristocratic value.
		(neg|troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_adventurous),
		(this_or_next|troop_slot_ge, "$g_talk_troop", slot_lord_reputation_type, lrep_conventional),
		(troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_roguish),
		#On normal will agree if outnumbered 4-to-1
		(val_div, ":surrender_ratio_10", 2),
	(try_end),

	#Certain lords consider certain locations "native" and will not easily surrender their homes.
	#Normally the following is just for companions, but I've set it to also include things
	#like Lord Harringoth and Harringoth Castle, etc.  This is applied after personality factors,
	#since it can enhance or counteract someone's native disposition.
	(try_begin),
		(is_between, "$g_talk_troop", active_npcs_begin, kingdom_ladies_end),
		(troop_slot_eq, "$g_talk_troop", slot_troop_home, "$g_encountered_party"),
		#On normal, most will agree if outnumbered 16-to-1, 8-to-1 if cowardly, 32-to-1 if brave
		(val_mul, ":surrender_ratio_10", 2),
	(try_end),

	(val_clamp, ":surrender_ratio_10", 40, 320),#If the value is not in this range, there was a coding mistake
	#Adjust threshold for campaign difficulty
	(try_begin),
		(lt, ":reduce_campaign_ai", 1),#hard, 150% (ordinarily 14-to-1, 8-to-1 for cowards, 28-to-1 for brave)
		(val_mul, ":surrender_ratio_10", 3),
		(val_div, ":surrender_ratio_10", 2),
	(else_try),
		(eq, ":reduce_campaign_ai", 0),#medium, 100% (ordinarily 8-to-1, 4-to-1 for cowards, 16-to-1 for brave)
	(else_try),
		(ge, ":reduce_campaign_ai", 2),#easy, 75% (ordinarily 6-to-1, 3-to-1 for cowards, 12-to-1 for brave)
		(val_mul, ":surrender_ratio_10", 3),
		(val_add, ":surrender_ratio_10", 2),
		(val_div, ":surrender_ratio_10", 4),
	(try_end),

	#Compare the besiegers' strength to the "surrender threshold"
	(store_mul, ":required_strength", ":defender_str", ":surrender_ratio_10"),
	(store_mul, reg0, "$g_ally_strength", 10),
	(ge, reg0, ":required_strength"),
	],
	"We are ready to leave this castle to you and march away if you give me your word of honour that you'll let us leave unmolested.", "player_siege_ask_leave_unmolested", []],
#Make a defiant remark if the enemy is vastly outnumbered but refusing to surrender.
[anyone,"player_siege_ask_surrender", [
	#I assume that $g_encountered_party is the town, but this could be wrong
	(this_or_next|party_slot_eq, "$g_encountered_party", slot_party_type, spt_castle),
		(party_slot_eq, "$g_encountered_party", slot_party_type, spt_town),
	(is_between, "$g_encountered_party_faction", kingdoms_begin, kingdoms_end),
	#The attackers outnumber the defenders by a decent ratio.
	(store_mul, reg0,"$g_enemy_strength", 4),
	(ge, "$g_ally_strength", reg0),
	#The attack is on native soil, or the odds are REALLY bad.
	(store_mul, reg0, "$g_enemy_strength", 8),
	(this_or_next|party_slot_eq, "$g_encountered_party", slot_center_original_faction, "$g_encountered_party_faction"),
		(ge, "$g_ally_strength", reg0),
	#Store name of castle and name of faction
	(str_store_faction_name, s0, "$g_talk_troop_faction"),
	(str_store_party_name, s1, "$g_encountered_party"),],
	"The {s0} will never abandon {s1}!", "close_window", []],
##diplomacy end+
[anyone,"player_siege_ask_surrender", [],
"Surrender? Hah! We can hold these walls until we all die of old age.", "close_window", []],
[anyone|plyr,"player_siege_ask_surrender_treatment", [],
"I give you nothing. Surrender now or prepare to die!", "player_siege_ask_surrender_treatment_reject", []],
[anyone,"player_siege_ask_surrender_treatment_reject", [
##diplomacy start+ Make both-gender version.
],
"{Bastard/Bitch}. We will fight you to the last man!", "close_window", []],
##diplomacy end+
[anyone|plyr,"player_siege_ask_surrender_treatment", [],
"You will be ransomed and your soldiers will live. I give you my word.", "player_siege_ask_surrender_treatment_accept", []],
[anyone,"player_siege_ask_surrender_treatment_accept", [],
"Very well then. Under those terms, I offer you my surrender.", "close_window", [(assign,"$g_enemy_surrenders",1)]],
[anyone|plyr,"player_siege_ask_leave_unmolested", [],
"You have my word. You will not come under attack if you leave the castle.", "player_siege_ask_leave_unmolested_accept", []],
[anyone,"player_siege_ask_leave_unmolested_accept", [],
"Very well. Then we leave this castle to you. You have won this day. But we'll meet again.", "close_window", [(assign,"$g_castle_left_to_player",1)]],
[anyone|plyr,"player_siege_ask_leave_unmolested", [],
"Unacceptable. I want prisoners.", "player_siege_ask_leave_unmolested_reject", []],
[anyone,"player_siege_ask_leave_unmolested_reject", [],
"Then we will defend this castle to the death, and this parley is done. Farewell.", "close_window", []],
#After battle texts

[anyone,"start", [
(eq, "$talk_context", tc_hero_freed),
(troop_slot_eq,"$g_talk_troop",slot_troop_occupation, slto_kingdom_hero)],
"I am in your debt for freeing me, friend.", "freed_lord_answer",
[
(try_begin),
 (check_quest_active, "qst_rescue_lord_by_replace"),
 (quest_slot_eq, "qst_rescue_lord_by_replace", slot_quest_target_troop, "$g_talk_troop"),
 (call_script, "script_succeed_quest", "qst_rescue_lord_by_replace"),
 (assign, "$do_not_cancel_quest", 1),
(try_end),

(try_begin),
 (check_quest_active, "qst_rescue_prisoner"),
 (quest_slot_eq, "qst_rescue_prisoner", slot_quest_target_troop, "$g_talk_troop"),
 (call_script, "script_succeed_quest", "qst_rescue_prisoner"),
 (assign, "$do_not_cancel_quest", 1),
(try_end),

(call_script, "script_remove_troop_from_prison", "$g_talk_troop"),
(assign, "$do_not_cancel_quest", 0),
]],
[anyone|plyr,"freed_lord_answer", [(lt, "$g_talk_troop_faction_relation", 0)],
"You're not going anywhere, 'friend'. You're my prisoner now.", "freed_lord_answer_1",
[#(troop_set_slot, "$g_talk_troop", slot_troop_is_prisoner, 1),
(troop_set_slot, "$g_talk_troop", slot_troop_prisoner_of_party, "p_main_party"),
(party_force_add_prisoners, "p_main_party", "$g_talk_troop", 1),
(call_script, "script_change_player_relation_with_troop", "$g_talk_troop", -30),
(call_script, "script_change_player_relation_with_faction_ex", "$g_talk_troop_faction", -2),
(call_script, "script_event_hero_taken_prisoner_by_player", "$g_talk_troop"),
]],
#take prisoner

[anyone,"freed_lord_answer_1", [],
##diplomacy start+ make insult switch by gender
"I'll have your head on a pike for this, you {bastard/bitch}! Someday!", "close_window", []],
##diplomacy end+

[anyone|plyr,"freed_lord_answer", [
],
"You are free to go wherever you want, sir.", "freed_lord_answer_2",
[(call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 7),
(call_script, "script_change_player_honor", 2),
#    (troop_get_slot, ":cur_rank", "$g_talk_troop", slot_troop_kingdom_rank),
#    (val_mul, ":cur_rank", 1),
##diplomacy start+
#Relationship boost for freeing lords.
(call_script, "script_dplmc_is_affiliated_family_member", "$g_talk_troop"),
(assign, ":talk_troop_is_affiliate", reg0),
(try_for_range, ":npc", heroes_begin, heroes_end),
	(store_troop_faction, ":npc_faction", ":npc"),
	(store_relation, reg0, ":npc_faction", "$g_talk_troop_faction"),
	(this_or_next|eq, ":npc_faction", "$g_talk_troop_faction"),
		(ge, reg0, 0),
	(neq, ":npc", "$g_talk_troop"),
	(neg|troop_slot_eq, ":npc", slot_troop_occupation, dplmc_slto_dead),
	(call_script, "script_troop_get_player_relation", ":npc"),
	(assign, ":relation_with_player", reg0),
	(assign, ":player_relation_change", 0),
	(try_begin),
		#Affiliate to a family: improve relations for freeing lords
		(ge, ":talk_troop_is_affiliate", 1),
		(call_script, "script_dplmc_is_affiliated_family_member", ":npc"),
		(ge, reg0, 1),

		(try_begin),
			(lt, ":relation_with_player", 0),
			(assign, ":player_relation_change", 2),
		(else_try),
			(lt, ":relation_with_player", 10),
			(assign, ":player_relation_change", 2),
		(else_try),
			(lt, ":relation_with_player", 20),
			(store_random_in_range, ":player_relation_change", 0, 2),
		(else_try),
			(lt, ":relation_with_player", 40),
			(store_random_in_range, ":player_relation_change", -1, 2),
			(val_max, ":player_relation_change", 0),
		(try_end),
		(gt, ":player_relation_change", 0),
		(call_script, "script_change_player_relation_with_troop", ":npc", ":player_relation_change"),
	(else_try),
		#Lords friendly and/or related to the troop
		(call_script, "script_troop_get_relation_with_troop", ":npc", "$g_talk_troop"),
		(assign, ":relation", reg0),
		(try_begin),
			(ge, ":relation", 20),
			(store_random_in_range, reg0, 0, 2),
			(this_or_next|ge, ":relation", ":relation_with_player"),
				(eq, reg0, 1),
			(assign, ":player_relation_change", 1),
		(try_end),
		(try_begin),
			(ge, ":relation", 0),
			(troop_slot_eq, ":npc", slot_troop_betrothed, "$g_talk_troop"),
			(val_add, ":player_relation_change", 1),
		(else_try),
			(ge, ":relation", 0),
			(this_or_next|troop_slot_eq, ":npc", slot_troop_occupation, slto_kingdom_lady),
				(is_between, ":npc", kingdom_ladies_begin, kingdom_ladies_end),
			(call_script, "script_troop_get_family_relation_to_troop", ":npc", "$g_talk_troop"),
			(ge, reg0, 4),
			(store_random_in_range, reg0, 0, 2),
			(this_or_next|troop_slot_eq, ":npc", slot_lord_reputation_type, lrep_conventional),
			   (eq, reg0, 1),
			(val_add, ":player_relation_change", 1),
		(try_end),
		(gt, ":player_relation_change", 0),
		(call_script, "script_change_player_relation_with_troop", ":npc", ":player_relation_change"),
	(try_end),
(try_end),
##diplomacy end+
(call_script, "script_change_player_relation_with_faction_ex", "$g_talk_troop_faction", 2)]],
[anyone,"freed_lord_answer_2", [],
"Thank you. I never forget someone who's done me a good turn.", "close_window",
[
(assign, "$g_leave_encounter", 1), #Not sure why this is necessary
]],
##  [anyone|plyr,"freed_lord_answer", [(neg|faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, "$g_talk_troop"), #he is not a faction leader!
##                                     (call_script, "script_get_number_of_hero_centers", "$g_talk_troop"),
##                                     (eq, reg0, 0), #he has no castles or towns
##                                     (hero_can_join)],
##   "I need capable men like you. Would you like to join me?", "knight_offer_join",
##   []],
##
##  [anyone,"freed_lord_answer_3", [(store_random_in_range, ":random_no",0,2),(eq, ":random_no", 0)],
##   "Alright I will join you.", "close_window",
##   [
###     (troop_set_slot, "$g_talk_troop", slot_troop_is_player_companion, 1),
##     (troop_set_slot, "$g_talk_troop", slot_troop_occupation, slto_player_companion),
##     (store_conversation_troop, ":cur_troop_id"),
##     (party_add_members, "p_main_party", ":cur_troop_id", 1),#join hero
##   ]],
##
##  [anyone,"freed_lord_answer_3", [],
##   "No, I want to go on my own.", "close_window", []],


#Troop commentary changes begin
[anyone,"start", [(eq,"$talk_context",tc_hero_defeated),
              (troop_slot_eq,"$g_talk_troop",slot_troop_occupation, slto_kingdom_hero)],
"{s43}", "defeat_lord_answer",
[(troop_set_slot, "$g_talk_troop", slot_troop_leaded_party, -1),
(call_script, "script_lord_comment_to_s43", "$g_talk_troop", "str_surrender_offer_default"),
]],
[anyone|plyr,"defeat_lord_answer", [],
"You are my prisoner now.", "defeat_lord_answer_1",
[
#(troop_set_slot, "$g_talk_troop", slot_troop_is_prisoner, 1),
(troop_set_slot, "$g_talk_troop", slot_troop_prisoner_of_party, "p_main_party"),
(party_force_add_prisoners, "p_main_party", "$g_talk_troop", 1),#take prisoner
(call_script, "script_change_player_relation_with_troop", "$g_talk_troop", -3),
(call_script, "script_change_player_relation_with_faction_ex", "$g_talk_troop_faction", -3),
(call_script, "script_event_hero_taken_prisoner_by_player", "$g_talk_troop"),
(call_script, "script_add_log_entry", logent_lord_captured_by_player, "trp_player",  -1, "$g_talk_troop", "$g_talk_troop_faction"),
]],
[anyone,"defeat_lord_answer_1", [],
"I am at your mercy.", "close_window", []],
[anyone|plyr,"defeat_lord_answer", [],
"You have fought well. You are free to go.", "defeat_lord_answer_2",
[(call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 5),
(call_script, "script_change_player_honor", 3),
(call_script, "script_add_log_entry", logent_lord_defeated_but_let_go_by_player, "trp_player",  -1, "$g_talk_troop", "$g_talk_troop_faction")]],
[anyone,"defeat_lord_answer_2", [],
"{s43}", "close_window", [
(call_script, "script_lord_comment_to_s43", "$g_talk_troop", "str_prisoner_released_default"),
 ]],
#Troop commentary changes end

#Troop commentaries changes begin
[anyone,"start", [(eq,"$talk_context",tc_party_encounter),
              (troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_hero),
              (lt,"$g_encountered_party_relation",0),
              (encountered_party_is_attacker),
              (eq, "$g_talk_troop_met", 1),                    ],
"{playername}!", "party_encounter_lord_hostile_attacker", [
              ]],
[anyone,"start", [(eq,"$talk_context",tc_party_encounter),
              (troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_hero),
              (lt,"$g_encountered_party_relation",0),
              (encountered_party_is_attacker),                ],
"Halt!", "party_encounter_lord_hostile_attacker", [
              ]],
[anyone,"party_encounter_lord_hostile_attacker", [
(gt, "$g_comment_found", 0),
              ],
"{s42}", "party_encounter_lord_hostile_attacker", [
                   (try_begin),
                     (neq, "$log_comment_relation_change", 0),
                     (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", "$log_comment_relation_change"),
                   (try_end),
                   (assign, "$g_comment_found", 0),
              ]],
#Troop commentaries changes end
[anyone,"party_encounter_lord_hostile_attacker", [
              ],
"{s43}", "party_encounter_lord_hostile_attacker_2",
[
(call_script, "script_lord_comment_to_s43", "$g_talk_troop", "str_surrender_demand_default"),
 ]],
[anyone|plyr,"party_encounter_lord_hostile_attacker_2", [
              ],
"We will fight you to the end!", "close_window", []],
[anyone|plyr,"party_encounter_lord_hostile_attacker_2", [
##diplomacy start+ Support promoted ladies
#(is_between, "$g_talk_troop", active_npcs_begin, active_npcs_end),
(is_between, "$g_talk_troop", heroes_begin, heroes_end),
##diplomacy end+
(neg|faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, "$g_talk_troop"),
              ],
"Stay your hand! There is something I must tell you in private.", "lord_recruit_1_relation", []],
[anyone|plyr,"party_encounter_lord_hostile_attacker_2", [
              ],
"Is there no way to avoid this battle? I don't want to fight with you.", "party_encounter_offer_dont_fight", []],
#TODO: Add a verification step.
[anyone|plyr,"party_encounter_lord_hostile_attacker_2", [
              ],
"Don't attack! We surrender.", "close_window", [(assign,"$g_player_surrenders",1)]],
[anyone, "party_encounter_offer_dont_fight", [(gt, "$g_talk_troop_effective_relation", 30),
#TODO: Add adition conditions, lord personalities, battle advantage, etc...
              ],
"I owe you a favor, don't I. Well... all right then. I will let you go just this once.", "close_window", [
(call_script, "script_change_player_relation_with_troop","$g_talk_troop", -7),
(store_current_hours,":protected_until"),
(val_add, ":protected_until", 72),
(party_set_slot,"$g_encountered_party",slot_party_ignore_player_until,":protected_until"),
(party_ignore_player, "$g_encountered_party", 72),
(assign, "$g_leave_encounter",1)
 ]],
##diplomacy begin
[anyone, "party_encounter_offer_dont_fight", [
(troop_get_slot,":reputation", "$g_talk_troop", slot_lord_reputation_type),
(neq, ":reputation", lrep_upstanding),
(neq, ":reputation", lrep_debauched),
##diplomacy start+
(neq, ":reputation", lrep_moralist),
#Martial does not accept when marshall
(this_or_next|neq, ":reputation", lrep_martial),
   (neg|faction_slot_eq, "$g_talk_troop_faction", slot_faction_marshall, "$g_talk_troop"),

#Leaders of kingdoms never accept this (for lieges this shouldn't appear anyway)
(this_or_next|neg|is_between, "$g_talk_troop_faction", kingdoms_begin, kingdoms_end),
   (neg|faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, "$g_talk_troop"),

(assign, ":can_intrigue", 0),
(try_begin),
   (neg|is_between, "$g_talk_troop_faction", kingdoms_begin, kingdoms_end),
   (assign, ":can_intrigue", 1),
(else_try),
   (call_script, "script_cf_troop_can_intrigue", "$g_talk_troop", 1),
   (assign, ":can_intrigue", 1),
(try_end),
(eq, ":can_intrigue", 1),
##diplomacy end+

(gt, "$g_talk_troop_effective_relation", 0),
(store_mul, ":rel_sq", "$g_talk_troop_effective_relation", "$g_talk_troop_effective_relation"),
(val_mul, ":rel_sq", 5),
(store_random_in_range, ":random", 5000, 10000),
(store_sub, ":amount", ":random", ":rel_sq"),
(val_max, ":amount", 0),
##diplomacy start+ Alternate calculation, since the player is effectively "ransoming himself"
(call_script, "script_calculate_ransom_amount_for_troop", "trp_player"),
(game_get_reduce_campaign_ai, ":reduce_campaign_ai"),
(try_begin),
   (le, ":reduce_campaign_ai", 0),#Hard
   (val_mul, reg0, 3),
   (val_div, reg0, 4),
(else_try),
   (le, ":reduce_campaign_ai", 1),#Medium
   (val_div, reg0, 2),
(else_try),
   (ge, ":reduce_campaign_ai", 2),#Easy
   (val_div, reg0, 4),
(try_end),
(val_max, ":amount", reg0),
##diplomacy end+

(party_get_num_companion_stacks, ":num_stacks", "p_main_party"),
(try_for_range, ":i_stack", 0, ":num_stacks"),
(party_stack_get_size, ":stack_size", "p_main_party", ":i_stack"),
(val_mul, ":stack_size", 12),
(val_add, ":amount", ":stack_size"),
(try_end),

(val_div, ":amount", 10),
(val_mul, ":amount", 10),
(assign, reg0, ":amount"),
],
"If you pay me {reg0} mon cash I will let you go, recreant.", "party_encounter_offer_money", [
 ]],
[anyone|plyr,"party_encounter_offer_money", [
(store_troop_gold, ":cur_gold", "trp_player"),
(gt, ":cur_gold", reg0),
],
"Don't attack! I pay.", "close_window", [
##nested diplomacy start+ actually give the gold to the enemy lord
(troop_remove_gold, "trp_player", reg0),
(try_begin),
   (troop_is_hero, "$g_talk_troop"),
   (call_script, "script_dplmc_distribute_gold_to_lord_and_holdings", reg0, "$g_talk_troop"),
(try_end),
##nested diplomacy end+
(call_script, "script_change_player_relation_with_troop","$g_talk_troop", -2),
(call_script, "script_change_player_honor", -2),
(store_current_hours,":protected_until"),
(val_add, ":protected_until",  72),
(party_set_slot,"$g_encountered_party",slot_party_ignore_player_until,":protected_until"),
(party_ignore_player, "$g_encountered_party",  72),
(assign, "$g_leave_encounter",1)]
],
[anyone|plyr,"party_encounter_offer_money", [
              ],
"Let's fight!", "party_encounter_offer_money_no",
[]
],
[anyone, "party_encounter_offer_money_no", [
(call_script, "script_lord_comment_to_s43", "$g_talk_troop", "str_lord_declines_negotiation_offer_default"),
              ],
"{s43}", "close_window", []],
##diplomacy end

[anyone, "party_encounter_offer_dont_fight", [
(call_script, "script_lord_comment_to_s43", "$g_talk_troop", "str_lord_declines_negotiation_offer_default"),
              ],
"{s43}", "close_window", []],
##  [anyone,"start", [(eq,"$talk_context",tc_party_encounter),
##                    (troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_hero),
##                    (lt,"$g_encountered_party_relation",0),
##                    (neg|encountered_party_is_attacker),
##                    ],
##   "What do you want?", "party_encounter_lord_hostile_defender",
##   []],


#  [anyone|plyr,"party_encounter_lord_hostile_defender", [],
#   "Nothing. We'll leave you in peace.", "close_window", [(assign, "$g_leave_encounter",1)]],




#Betrayal texts should go here


##  [anyone ,"start", [(troop_slot_eq,"$g_talk_troop",slot_troop_occupation, slto_kingdom_hero),
##                     (troop_slot_eq,"$g_talk_troop",slot_troop_last_quest_betrayed, 1),
##                     (troop_slot_eq,"$g_talk_troop",slot_troop_last_quest, "qst_deliver_message_to_lover"),
##                     (le,"$talk_context",tc_siege_commander),
##                     ],
##   "I had trusted that letter to you, thinking you were a {man/lady} of honor, and you handed it directly to the girl's father.\
## I should have known you were not to be trusted. Anyway, I have learned my lesson and I won't make that mistake again.", "close_window",
##   [(call_script, "script_clear_last_quest", "$g_talk_troop")]],


#Lord to be recruited

[anyone ,"start",
[
##diplomacy start+ Handle player is co-ruler of kingdom
(call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", "$g_talk_troop_faction"),
(this_or_next|ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
##diplomacy end+
(eq, "$g_talk_troop_faction", "fac_player_supporters_faction"),
(is_between, "$g_talk_troop", active_npcs_begin, active_npcs_end),
(troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_inactive),
(neq, "$g_talk_troop", "$g_player_minister"),
(troop_get_slot, ":original_faction", "$g_talk_troop", slot_troop_original_faction),
(faction_get_slot, ":original_faction_leader", ":original_faction", slot_faction_leader),
(str_store_troop_name, s10, ":original_faction_leader"),
(str_store_string, s9, "str_lord_indicted_dialog_approach"),
],
#Greetings, {my lord/my lady}. You may have heard of my ill treatment at the hands of {s10}. You have a reputation as one who treats {his/her} vassals well, and if you will have me, I would be honored to pledge myself as your vassal.
"{s9}", "lord_requests_recruitment", []],
#Rebellion changes begin
[anyone ,"start",
[
(is_between, "$g_talk_troop", pretenders_begin, pretenders_end),
(eq, "$g_talk_troop", "$supported_pretender"),
],
"I await your counsel, {playername}.", "supported_pretender_talk", [
]],
[anyone ,"start",
[
(is_between, "$g_talk_troop", pretenders_begin, pretenders_end),
(neg|troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_hero),
(assign, "$pretender_told_story", 0),
(eq, "$g_talk_troop_met", 0),
(neg|faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, "$g_talk_troop"),
],
"Do I know you?.", "pretender_intro_1", []],
[anyone|plyr ,"pretender_intro_1", [], "My name is {playername}. At your service.", "pretender_intro_2", []],
[anyone|plyr ,"pretender_intro_1", [], "I am {playername}. Perhaps you have heard of my exploits.", "pretender_intro_2", []],
[anyone ,"pretender_intro_2", [(troop_get_slot, ":rebellion_string", "$g_talk_troop", slot_troop_original_faction),
                           (val_sub, ":rebellion_string", "fac_kingdom_1"),
                           (val_add, ":rebellion_string", "str_swadian_rebellion_pretender_intro"),
                           (str_store_string, 48, ":rebellion_string"),],
"{s48}", "pretender_intro_3", []],
[anyone|plyr ,"pretender_intro_3", [(troop_get_slot, ":original_faction", "$g_talk_troop", slot_troop_original_faction),
                                (str_store_faction_name, s12, ":original_faction"),
                                (faction_get_slot, ":original_ruler", ":original_faction", slot_faction_leader),
                                (str_store_troop_name, s11, ":original_ruler"),],
#gekokujo 3.0 pretender dialogue tweaks start
#"I thought {s12} was ruled by {s11}?", "pretender_rebellion_cause_1", [
"Isn't that ruled by {s11} of the {s12}?", "pretender_rebellion_cause_1", [
#gekokujo 3.0 pretender dialogue tweaks end
(troop_set_slot, "$g_talk_troop", slot_troop_discussed_rebellion, 1)
]],
[anyone ,"start",
[
(is_between, "$g_talk_troop", pretenders_begin, pretenders_end),
(neg|faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, "$g_talk_troop"),
(neg|troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_hero),
##diplomacy start+ Detect completed quest
(neg|troop_slot_eq, "$g_talk_troop", slot_troop_playerparty_history, dplmc_pp_history_granted_fief),
(neg|troop_slot_eq, "$g_talk_troop", slot_troop_playerparty_history, dplmc_pp_history_lord_rejoined),
##diplomacy end+
],
"Greetings, {playername}", "pretender_start", [(assign, "$pretender_told_story", 0)]],
[anyone|plyr ,"pretender_start",
[
(troop_slot_eq, "$g_talk_troop", slot_troop_discussed_rebellion, 1),
(eq, "$pretender_told_story", 0)
],
"What was your story again, {reg65?my lady:sir}?", "pretender_rebellion_cause_prelim", [
]],
[anyone,"pretender_rebellion_cause_prelim", [],
"I shall tell you.", "pretender_rebellion_cause_1", [
               ]],
[anyone,"pretender_rebellion_cause_1", [],
"{s48}", "pretender_rebellion_cause_2", [
               (assign, "$pretender_told_story", 1),
               (troop_get_slot, ":rebellion_string", "$g_talk_troop", slot_troop_original_faction),
               (val_sub, ":rebellion_string", "fac_kingdom_1"),
               (val_add, ":rebellion_string", "str_swadian_rebellion_pretender_story_1"),
               (str_store_string, 48, ":rebellion_string"),
               ]],
[anyone,"pretender_rebellion_cause_2", [],
"{s48}", "pretender_rebellion_cause_3", [
               (troop_get_slot, ":rebellion_string", "$g_talk_troop", slot_troop_original_faction),
               (val_sub, ":rebellion_string", "fac_kingdom_1"),
               (val_add, ":rebellion_string", "str_swadian_rebellion_pretender_story_2"),
               (str_store_string, 48, ":rebellion_string"),
               ]],
[anyone,"pretender_rebellion_cause_3", [],
"{s48}", "pretender_start", [
               (troop_get_slot, ":rebellion_string", "$g_talk_troop", slot_troop_original_faction),
               (val_sub, ":rebellion_string", "fac_kingdom_1"),
               (val_add, ":rebellion_string", "str_swadian_rebellion_pretender_story_3"),
               (str_store_string, 48, ":rebellion_string"),
               ]],
[anyone|plyr ,"pretender_start", [
              (troop_slot_eq, "$g_talk_troop", slot_troop_discussed_rebellion, 1),
               ],
"I want to take up your cause and help you reclaim your clan!", "pretender_discuss_rebellion_1", [
]],
[anyone|plyr ,"pretender_start", [
               ],
"I must leave now.", "pretender_end", [
]],
[anyone ,"pretender_discuss_rebellion_1", [(troop_get_slot, ":original_faction", "$g_talk_troop", slot_troop_original_faction),
                                       (faction_get_slot, ":original_ruler", ":original_faction", slot_faction_leader),
##diplomacy start+ Change "lords" to {s0}
                                       (call_script, "script_dplmc_print_cultural_word_to_sreg", "$g_talk_troop", DPLMC_CULTURAL_TERM_LORD_PLURAL,0),
                                       (str_store_troop_name, s11, ":original_ruler")],
"Are you sure you will be up to the task, {playername}? Reclaiming my clan will be no simple matter.\
The {s0} of our domain have all sworn oaths of loyalty to {s11}.\
Such oaths to a usurper are of course invalid, and we can expect some of the {s0} to side with us, but it will be a very tough and challenging struggle ahead.", "pretender_discuss_rebellion_2a", []],
##diplomacy end+

[anyone ,"pretender_discuss_rebellion_2a",[
                           (troop_get_slot, ":original_faction", "$g_talk_troop", slot_troop_original_faction),
                                      (faction_get_slot, ":original_ruler", ":original_faction", slot_faction_leader),
                           (str_store_troop_name, s12, ":original_ruler"),
                                      (call_script, "script_evaluate_realm_stability", ":original_faction"),
                           (assign, ":instability_index", reg0),
                           (val_add, ":instability_index", reg0),
                           (val_add, ":instability_index", reg1),
                           (try_begin),
                              (gt, ":instability_index", 60),
                              (str_store_string, s11, "str_one_thing_in_our_favor_is_that_s12s_grip_is_very_shaky_he_rules_over_a_labyrinth_of_rivalries_and_grudges_lords_often_fail_to_cooperate_and_many_would_happily_seek_a_better_liege"),
                           (else_try),
                              (is_between, ":instability_index", 40, 60),
                              (str_store_string, s11, "str_thankfully_s12s_grip_is_fairly_shaky_many_lords_do_not_cooperate_with_each_other_and_some_might_be_tempted_to_seek_a_better_liege"),
                           (else_try),
                              (is_between, ":instability_index", 20, 40),
                              (str_store_string, s11, "str_unfortunately_s12s_grip_is_fairly_strong_until_we_can_shake_it_we_may_have_to_look_long_and_hard_for_allies"),
                           (else_try),
                              (lt, ":instability_index", 20),
                              (str_store_string, s11, "str_unfortunately_s12s_grip_is_very_strong_unless_we_can_loosen_it_it_may_be_difficult_to_find_allies"),
                           (try_end),
                            ],
"{s11}", "pretender_discuss_rebellion_2", []],
[anyone|plyr ,"pretender_discuss_rebellion_2", [],  "I am ready for this struggle.", "pretender_discuss_rebellion_3", []],
[anyone|plyr ,"pretender_discuss_rebellion_2", [],  "You are right. Perhaps, I should think about this some more.", "pretender_end", []],
[anyone ,"pretender_discuss_rebellion_3", [(this_or_next|neg|faction_slot_eq, "fac_player_supporters_faction", slot_faction_state, sfs_active),
                            (neg|faction_slot_eq, "fac_player_supporters_faction", slot_faction_leader, "trp_player"),
                            (neg|troop_slot_ge, "trp_player",slot_troop_renown, 200),
                                       (troop_get_slot, ":original_faction", "$g_talk_troop", slot_troop_original_faction),
                                       (faction_get_slot, ":original_ruler", ":original_faction", slot_faction_leader),
                                       (str_store_troop_name, s11, ":original_ruler")],
"I have no doubt that your support for my cause is heartfelt, {playername}, and I am grateful to you for it. \
But I don't think we have much of a chance of success. \
If you can gain renown in the battlefield and make a name for yourself as a great commander, then our friends would not hesitate to join our cause, \
and our enemies would be wary to take up arms against us. When that time comes, I will come with you gladly. \
But until that time, it will be wiser not to openly challange the usurper, {s11}.", "close_window", []],
[anyone ,"pretender_discuss_rebellion_3", [(this_or_next|neg|faction_slot_eq, "fac_player_supporters_faction", slot_faction_state, sfs_active),
                            (neg|faction_slot_eq, "fac_player_supporters_faction", slot_faction_leader, "trp_player"),
                            (gt, "$supported_pretender", 0),
                                       (str_store_troop_name, s17, "$supported_pretender")],
"Haven't you already taken up the cause of {s17}? \
You must have a very strong sense of justice, indeed. \
But no, thank you. I will not be part of your game.", "close_window", []],
[anyone ,"pretender_discuss_rebellion_3", [(this_or_next|neg|faction_slot_eq, "fac_player_supporters_faction", slot_faction_state, sfs_active),
                            (neg|faction_slot_eq, "fac_player_supporters_faction", slot_faction_leader, "trp_player"),
                            (gt, "$players_kingdom", 0),
                                       (neq, "$players_kingdom", "fac_player_supporters_faction"),
                                       (neq, "$players_kingdom", "fac_player_faction"),
                                       (troop_get_slot, ":original_faction", "$g_talk_troop", slot_troop_original_faction),
                                       (neq, "$players_kingdom", ":original_faction"),
                                       (eq, "$player_has_homage", 1),

                                       (str_store_faction_name, s16, "$players_kingdom"),
                                       (faction_get_slot, ":player_ruler", "$players_kingdom", slot_faction_leader),
                                       (str_store_troop_name, s15, ":player_ruler"),
                                       (str_store_faction_name, s17, ":original_faction"),
                                       ],
"{playername}, you are already oath-bound to serve {s15}.\
As such, I cannot allow you to take up my cause, and let my enemies claim that I am but a mere puppet of {s16}.\
No, if I am to have the overlordship of {s17}, I must do it due to the righteousness of my cause and the support of my vassals alone.\
If you want to help me, you must first free yourself of your oath to {s15}.", "close_window", []],
[anyone ,"pretender_discuss_rebellion_3", [(faction_slot_eq, "fac_player_supporters_faction", slot_faction_state, sfs_active),
                            (faction_slot_eq, "fac_player_supporters_faction", slot_faction_leader, "trp_player")],
"You are a monarch in your own right, {sir/my lady}. If you were to back me, I would be merely your puppet.", "close_window", []],
[anyone ,"pretender_discuss_rebellion_3", [(troop_get_slot, ":original_faction", "$g_talk_troop", slot_troop_original_faction),
                                       (str_store_faction_name, s12, ":original_faction"),
                                       (faction_get_slot, ":original_ruler", ":original_faction", slot_faction_leader),
                                       (str_store_troop_name, s11, ":original_ruler"),
##diplomacy start+ replace "his" with "{reg0?her:his}"
(call_script, "script_dplmc_store_troop_is_female", ":original_ruler"),
],
"You are a capable warrior, {playername}, and I am sure with your renown as a commander, and my righteous cause, the samurai and the good people of {s12} will flock to our support.\
The time is ripe for us to act! I will come with you, and together, we will topple the usurper {s11} and take the overlordship from {reg0?her:his} bloodied hands.\
But first, you must give me your oath of loyalty and accept me as your overlord {reg65?lady:lord}.", "pretender_rebellion_ready", []],
##diplomacy end+

[anyone|plyr ,"pretender_rebellion_ready", [
			##diplomacy start+
            ##OLD:   (troop_get_type, reg3, "$g_talk_troop"),
			(assign, reg3, 0),
			(try_begin),
				(call_script, "script_cf_dplmc_troop_is_female", "$g_talk_troop"),
				(assign, reg3, 1),
			(try_end),
			(assign, reg65, reg3),
			##diplomacy end+
               ],
"I am ready to pledge myself to your cause, {reg3?my lady:sir}.", "lord_give_oath_2", [
]],
[anyone|plyr ,"pretender_rebellion_ready", [
               ],
"Let us bide our time a little longer.", "pretender_end", [
]],
[anyone ,"pretender_end", [
               ],
"Farewell for now, then.", "close_window", [
]],
# Events....
# Choose friend.
#Post 0907 changes begin
[anyone ,"start", [(troop_slot_eq,"$g_talk_troop",slot_troop_occupation, slto_kingdom_hero),
               (neq, "$g_talk_troop_met", 0),
               (gt, "$g_time_since_last_talk", 24),
               (gt, "$g_talk_troop_relation", -10),
               (store_random_in_range, ":random_num", 0, 100),
               (lt, ":random_num", 30),
               (eq,"$talk_context",tc_town_talk),
               (call_script, "script_cf_troop_get_random_enemy_troop_with_occupation", "$g_talk_troop", slto_kingdom_hero),
               (assign, ":other_lord",reg0),
               (troop_get_slot, ":other_lord_relation", ":other_lord", slot_troop_player_relation),
               (ge, ":other_lord_relation", 20),
               (str_store_troop_name, s6, ":other_lord"),
               (assign, "$temp", ":other_lord"),
##diplomacy start+ replace "man" with "{reg0?woman:man}" and "him" with "{reg0?her:him}"
(call_script, "script_dplmc_store_troop_is_female", ":other_lord"),
               ],
"I heard that you have befriended that {s43} called {s6}.\
Believe me, you can't trust that {reg0?woman:man}.\
You should end your dealings with {reg0?her:him}.", "lord_event_choose_friend", [
##diplomacy end+
(call_script, "script_lord_comment_to_s43", "$g_talk_troop", "str_lord_insult_default"),

]],
#Meeting.
[anyone ,"start", [(troop_slot_eq, "$g_talk_troop",slot_troop_occupation, slto_kingdom_hero),
               ##diplomacy start+ This seemingly redundant condition is for a polygamy implementation
               (this_or_next|troop_slot_eq, "$g_talk_troop", slot_troop_spouse, "trp_player"),
               ##diplomacy end+
               (troop_slot_eq, "trp_player", slot_troop_spouse, "$g_talk_troop"),
          ##diplomacy start+ load relation text into s0
		  (call_script, "script_dplmc_print_player_spouse_says_my_husband_wife_to_s0", "$g_talk_troop", 0),
          ##diplomacy end+
               ],
##diplomacy start+ either gender PC can marry opposite-gender lords
"Yes, {s0}?", "lord_start",#changed "my wife" to {s0}
[]],
#Reversed the order of this condition and the next one.  Otherwise this would never
#occur when the player was the faction leader.
[anyone ,"start", [
	#gekokujo 3.0 microfactions! include fort companions start
	#(is_between, "$g_talk_troop", companions_begin, companions_end),
	(is_between, "$g_talk_troop", companions_begin, fort_companions_end),
	#gekokujo 3.0 microfactions! include fort companions end
    (troop_slot_eq,"$g_talk_troop",slot_troop_occupation, slto_kingdom_hero),
    (le,"$talk_context",tc_siege_commander),
	##Added extra conditions
	(ge, "$g_talk_troop_relation", 20),
	(neg|troop_slot_eq, "$g_talk_troop", slot_troop_playerparty_history, dplmc_pp_history_nonplayer_entry),
	##Suppress this message sometimes when your companion is your vassal
	(assign, ":stop", 0),
	(try_begin),
		(faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, "trp_player"),
		(store_random_in_range, ":rand", 0, 100),
		(this_or_next|ge, ":rand", "$g_talk_troop_relation"),
			(ge, ":rand", 95),#at least 1-in-20 chance of standard message
		(assign, ":stop", 1),
	(try_end),
	(eq, ":stop", 0),
    ],
"It is good to see you, old friend", "lord_start",
[]],
[anyone ,"start", [
	##Add support for player is co-ruler
	(assign, reg0, 0),
	(try_begin),
		(neq, "$g_talk_troop_faction", "fac_player_supporters_faction"),
		(call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", "$g_talk_troop_faction"),
	(try_end),
	(this_or_next|ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
    #(this_or_next|eq, "$g_talk_troop_faction", "fac_player_supporters_faction"),#added # then removed
	(faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, "trp_player"),
	(troop_slot_eq,"$g_talk_troop",slot_troop_occupation, slto_kingdom_hero),
    (le,"$talk_context",tc_siege_commander),
               ],
"Yes, my {lord/lady}?", "lord_start",
[]],
##diplomacy end+

[anyone ,"start", [(troop_slot_eq,"$g_talk_troop",slot_troop_occupation, slto_kingdom_hero),
               (check_quest_active, "qst_join_faction"),
               (eq, "$g_invite_faction_lord", "$g_talk_troop"),
          (eq, "$players_kingdom", "fac_player_supporters_faction"),
               ],
#TODO: change conversations according to relation.
"Well, {playername}. I am willing to forgive your impudence in proclaiming yourself an overlord, and will welcome you into my domain with full honor, as one of my vassals. Shall we proceed to an oath of allegiance?", "lord_invite_player_monarch_1",
[]],
[anyone ,"start", [(troop_slot_eq,"$g_talk_troop",slot_troop_occupation, slto_kingdom_hero),
               (check_quest_active, "qst_join_faction"),
               (eq, "$g_invite_faction_lord", "$g_talk_troop"),
               (try_begin),
                 (gt, "$g_invite_offered_center", 0),
                 (store_faction_of_party, ":offered_center_faction", "$g_invite_offered_center"),
                 (neq, ":offered_center_faction", "$g_talk_troop_faction"),
                 (call_script, "script_get_poorest_village_of_faction", "$g_talk_troop_faction"),
                 (assign, "$g_invite_offered_center", reg0),
               (try_end),
               ],
#TODO: change conversations according to relation.
"{playername}, I've been expecting you. Word has reached my ears of your exploits.\
Why, I keep hearing such tales of prowess and bravery that my mind was quickly made up.\
I knew that I had found someone worthy of becoming my vassal.", "lord_invite_1",
[]],
[anyone ,"start", [(troop_slot_eq,"$g_talk_troop",slot_troop_met, 2),
               (gt, "$g_talk_troop_relation", 10),
          (gt, "$g_time_since_last_talk", 3),
		   ##diplomacy start+ Use script for gender
          #(troop_get_type, ":is_female", "trp_player"),
		  (assign, ":is_female", "$character_gender"),
          #male player + female lord
          (assign, ":lord_female", reg65),
          (this_or_next|eq, ":is_female", 1),
              (eq, ":lord_female", 1),
          (this_or_next|troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_hero),#bugfix
              (neg|is_between, "$g_talk_troop", kingdom_ladies_begin, kingdom_ladies_end),#bugfix
          #diplomacy end+
          (troop_slot_eq, "trp_player", slot_troop_spouse, -1),
          (troop_slot_eq, "trp_player", slot_troop_betrothed, -1),
          (troop_slot_eq, "$g_talk_troop", slot_troop_spouse, -1),
          (troop_slot_eq, "$g_talk_troop", slot_troop_betrothed, -1),
          (call_script, "script_npc_decision_checklist_marry_female_pc", "$g_talk_troop"),
          (ge, reg0, 1),
               ],
#diplomacy start+ gender-correct language
"My {lord/lady}, I have been giving much thought to our recent conversation. It is time for me to ask. Would you do me the honor of becoming my {husband/wife}?", "lord_female_pc_marriage_proposal",  [
#diplomacy end+
         ]],
[anyone ,"start", [(troop_slot_eq,"$g_talk_troop",slot_troop_met, 2),
               (gt, "$g_time_since_last_talk", 24),
               (gt, "$g_talk_troop_relation", 0),
	  #diplomacy start+ (players of either gender may marry opposite-gender lords)
          #(troop_get_type, ":is_female", "trp_player"),
	  (assign, ":is_female", "$character_gender"),
          (neg|troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_lady),
          #(troop_get_type, ":lord_female", "$g_talk_troop"),
	  (assign, ":lord_female", reg65),
          (this_or_next|troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_hero),
             (neq, ":lord_female", 1),
          (this_or_next|eq, ":lord_female", 1),
          #diplomacy end+
          (eq, ":is_female", 1),
          (troop_slot_eq, "trp_player", slot_troop_spouse, -1),
          (troop_slot_eq, "trp_player", slot_troop_betrothed, -1),
          (troop_slot_eq, "$g_talk_troop", slot_troop_spouse, -1),
          (troop_slot_eq, "$g_talk_troop", slot_troop_betrothed, -1),
               ],
#diplomacy start+ gender-corrected
"My {lord/lady}, it brings my heart great joy to see you again...", "lord_start",  [
          (call_script, "script_troop_change_relation_with_troop", "trp_player", "$g_talk_troop", 2),
#diplomacy end+
         ]],
[anyone ,"start", [(troop_slot_eq,"$g_talk_troop",slot_troop_met, 2),
               (gt, "$g_talk_troop_relation", 0),
##diplomacy start+ Consider when to enable this for male PCs
#          (troop_get_type, ":is_female", "trp_player"),
#          (eq, ":is_female", 1),
          (neg|troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_lady),
          (assign, ":lord_type", reg65),
          (assign, ":player_type", "$character_gender"),
          (this_or_next|ge, "$g_disable_condescending_comments", 2),
             (neq, ":lord_type", ":player_type"),#probably not necessary, unless "slot_troop_met" is also being used for something else
          (this_or_next|troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_hero),
          (troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_robber_knight),
               ],
#"lady" -> "{lord/lady}"
"My {lord/lady}, I am always your humble servant", "lord_start",  [
##diplomacy end+
         ]],
[anyone ,"start", [(troop_slot_eq,"$g_talk_troop",slot_troop_occupation, slto_kingdom_hero),
               (neq, "$g_talk_troop_met", 0),
               (gt, "$g_time_since_last_talk", 24),
               (gt, "$g_talk_troop_relation", 50),
               (gt, "$g_talk_troop_faction_relation", 10),
               (le,"$talk_context",tc_siege_commander),
               ],
"If it isn't my brave champion, {playername}...", "lord_start",  []],
[anyone ,"start", [(troop_slot_eq,"$g_talk_troop",slot_troop_occupation, slto_kingdom_hero),
               (neq, "$g_talk_troop_met", 0),
               (gt, "$g_time_since_last_talk", 24),
               (gt, "$g_talk_troop_relation", 10),
               (le,"$talk_context",tc_siege_commander),
               ],
"Good to see you again {playername}...", "lord_start", []],
[anyone ,"start", [(troop_slot_eq,"$g_talk_troop",slot_troop_occupation, slto_kingdom_hero),
               (neq, "$g_talk_troop_met", 0),
               (gt, "$g_time_since_last_talk", 24),
#                     (lt, "$g_talk_troop_faction_relation", 0),
               (le,"$talk_context",tc_siege_commander),
               ],
"We meet again, {playername}...", "lord_start", []],
[anyone ,"start", [(troop_slot_eq,"$g_talk_troop",slot_troop_occupation, slto_kingdom_hero),
               (eq, "$g_talk_troop_met", 0),
               (ge, "$g_talk_troop_faction_relation", 0),
               (le,"$talk_context",tc_siege_commander),
               ],
"Do I know you?", "lord_meet_neutral", []],
#  [anyone ,"start", [(troop_slot_eq,"$g_talk_troop",slot_troop_occupation, slto_kingdom_hero),
#                     (eq, "$g_talk_troop_met", 0),
#                     (ge, "$g_talk_troop_faction_relation", 0),
#                     (le,"$talk_context",tc_siege_commander),
#                     ],
#   "Who is this then?", "lord_meet_ally", []],
#  [anyone|plyr ,"lord_meet_ally", [],  "I am {playername} sir. A warrior of {s4}.", "lord_start", []],
#  [anyone|plyr ,"lord_meet_ally", [],  "I am but a soldier of {s4} sir. My name is {playername}.", "lord_start", []],

[anyone ,"start", [(troop_slot_eq,"$g_talk_troop",slot_troop_occupation, slto_kingdom_hero),
               (eq, "$g_talk_troop_met", 0),
               (lt, "$g_talk_troop_faction_relation", 0),
#                     (str_store_faction_name, s4,  "$players_kingdom"),
               (le,"$talk_context",tc_siege_commander),
               ],
"{s43}", "lord_meet_enemy", [
(call_script, "script_lord_comment_to_s43", "$g_talk_troop", "str_enemy_meet_default"),
 ]],
[anyone,"lair_quest_intermediate_1",
[
], "Splendid work, {playername} -- your audacious attack is the talk of the clan. No doubt they, or others like them, will soon be back, but for a short while you have bought this land a small respite. We are most grateful to you.", "lord_pretalk",
[
(quest_get_slot, ":quest_gold_reward", "qst_destroy_bandit_lair", slot_quest_gold_reward),
(call_script, "script_troop_add_gold", "trp_player", ":quest_gold_reward"),
(assign, ":xp_reward", ":quest_gold_reward"),
(val_mul, ":xp_reward", 2),
(add_xp_as_reward, ":xp_reward"),
(call_script, "script_change_troop_renown", "trp_player", 3),
(call_script, "script_troop_change_relation_with_troop", "trp_player", "$g_talk_troop", 4),
(call_script, "script_end_quest", "qst_destroy_bandit_lair"),
(assign, reg5, ":quest_gold_reward"),
]],
[anyone,"lair_quest_intermediate_2",
[], "Well, {playername}, I guess that at least some of those brigands eluded you -- and of course, it will be the peaceful travellers of this land who will pay the price. Still, it was good of you to try.", "lord_pretalk",
[
(call_script, "script_end_quest", "qst_destroy_bandit_lair"),
]],
[anyone,"offer_gift_quest_complete", [
(quest_get_slot, ":target_troop", "qst_offer_gift", slot_quest_target_troop),
##diplomacy start+
#(troop_get_type, reg4, ":target_troop"),
(call_script, "script_dplmc_store_troop_is_female_reg", ":target_troop", 4),
##diplomacy end+
],
"Ah, let me take those. Hopefully this will mend the quarrel between you two. You may wish to speak to {reg4?her:him}, and see if I had any success.", "close_window",[
(quest_set_slot, "qst_offer_gift", slot_quest_current_state, 2),
#gekokujo 3.0 integrating 1.158 change start
(quest_set_slot, "qst_offer_gift", slot_quest_expiration_days, 365),
#gekokujo 3.0 integrating 1.158 change end
(troop_remove_item, "trp_player", "itm_furs"),
(troop_remove_item, "trp_player", "itm_velvet"),
(assign, "$g_leave_encounter", 1),
]],
[anyone,"intrigue_quest_state_complaint", [
(assign, ":continue", 1),
(try_begin),
(call_script, "script_cf_troop_can_intrigue", "$g_talk_troop", 1),
(assign, ":continue", 0),
(try_end),
(eq, ":continue", 1),
],
"Whatever you have to say, I would ask you to wait until we are alone.", "lord_pretalk",[
]],
[anyone,"intrigue_quest_state_complaint", [
],
##diplomacy start+ change "sew" to "sow"
"What is it? I value your opinion, although I hope that you are not trying to sow dissension among my vassals? ", "intrigue_quest_state_complaint_plyr",[
##diplomacy end+

(quest_get_slot, ":target_troop", "qst_intrigue_against_lord", slot_quest_target_troop),
(call_script, "script_troop_get_relation_with_troop", ":target_troop", "$g_talk_troop"),
(assign, reg4, reg0),
(str_store_troop_name, s4, ":target_troop"),
(assign, reg5, "$g_talk_troop_effective_relation"),

(try_begin),
(eq, "$cheat_mode", 1),
(str_store_string, s12, "str_intrigue_success_chance"),
(display_message, "str_s12"),
(try_end),
]],
[anyone|plyr,"intrigue_quest_state_complaint_plyr", [
(check_quest_active, "qst_intrigue_against_lord"),
(quest_get_slot, ":target_troop", "qst_intrigue_against_lord", slot_quest_target_troop),
(str_store_troop_name, s4, ":target_troop"),
(troop_get_slot, ":reputation_string", ":target_troop", slot_lord_reputation_type),
(val_add, ":reputation_string", "str_lord_derogatory_default"),
(str_store_string, s5, ":reputation_string"),
],
"Oyakata-sama -- {s4} is widely held by your vassals to be {s5}, and a liability to your domain", "lord_intrigue_quest_complaint_stated",[
]],
[anyone|plyr,"intrigue_quest_state_complaint_plyr", [
],
"Actually, oyakata-sama, never mind.", "lord_pretalk",[
(call_script, "script_fail_quest", "qst_intrigue_against_lord"),
]],
[anyone|plyr,"intrigue_quest_state_complaint_failed", [
],
"I stand by my words, oyakata-sama.", "intrigue_quest_state_accept_blame",[
(call_script, "script_change_player_honor", 1),
]],
[anyone|plyr,"intrigue_quest_state_complaint_failed", [
(quest_get_slot, ":giver_troop", "qst_intrigue_against_lord", slot_quest_giver_troop),
(quest_get_slot, ":target_troop", "qst_intrigue_against_lord", slot_quest_target_troop),

(str_store_troop_name, s4, ":giver_troop"),
(str_store_troop_name, s5, ":target_troop"),
],
"Yes, my {lord/lady} -- {s4} put me up to denouncing {s5}!", "intrigue_quest_state_deflect_blame",[
(quest_get_slot, ":giver_troop", "qst_intrigue_against_lord", slot_quest_giver_troop),
(call_script, "script_troop_change_relation_with_troop", "$g_talk_troop", ":giver_troop", -5),
(call_script, "script_troop_change_relation_with_troop", "$g_talk_troop", "trp_player", 4),
(call_script, "script_change_player_honor", -2),
]],
[anyone,"intrigue_quest_state_accept_blame", [
],
"Indeed. You may stand by your words, but keep them to yourself. I will not have you undercutting my faithful follower {s4}.", "lord_pretalk",[
]],
[anyone,"intrigue_quest_state_deflect_blame", [
],
"I thought as much. Here's some advice for you, {lad/lassie} -- don't meddle in the quarrels of others. Now, enough of this.", "lord_pretalk",[
]],
[anyone,"hero_pretalk", [],
"Anything else?", "lord_talk",[]],
[anyone,"denounce_lord_results",[
(check_quest_succeeded, "qst_denounce_lord"),
(faction_get_slot, ":faction_leader", "$g_talk_troop_faction", slot_faction_leader),
(str_store_troop_name, s4, ":faction_leader"),
##diplomacy start+ Get gender of quest target
(quest_get_slot, ":target_troop", "qst_denounce_lord", slot_quest_target_troop),
(call_script, "script_dplmc_store_troop_is_female", ":target_troop"),
##diplomacy end+

],
##diplomacy start+ replace "him" with "{reg0?her:him}"
"Yes, and hopefully now {s4} will think twice before entrusting {reg0?her:him} with any additional fiefs, honors, or offices. We are grateful to you.", "lord_pretalk",
##diplomacy end+
[
(call_script, "script_succeed_quest", "qst_denounce_lord"),
(call_script, "script_end_quest", "qst_denounce_lord"),
(call_script, "script_troop_change_relation_with_troop", "$g_talk_troop", "trp_player", 8),
(add_xp_as_reward, 1000),
]],
[anyone,
"denounce_lord_results",[
#	(check_quest_failed, "qst_denounce_lord"),
##diplomacy start+ Get gender of quest target
(quest_get_slot, ":target_troop", "qst_denounce_lord", slot_quest_target_troop),
(call_script, "script_dplmc_store_troop_is_female", ":target_troop"),
##diplomacy end+
],
##diplomacy start+ next line, replace "he" with "{reg0?she:he}"
"So you did -- and we have heard that {reg0?she:he} forced you to retract your words, and thus emerged from this affair looking stronger than before. You will forgive me, {sir/my lady}, if my gratitude to you is somewhat muted.", "close_window",
##diplomacy end+
[
(call_script, "script_end_quest", "qst_denounce_lord"),

]],
[anyone,"convince_accept",[(check_quest_active, "qst_collect_debt"),
                       (quest_slot_eq, "qst_collect_debt", slot_quest_target_troop, "$g_talk_troop"),
                       (quest_get_slot, ":quest_giver_troop", "qst_collect_debt", slot_quest_giver_troop),
                       (str_store_troop_name,s8,":quest_giver_troop"),
                       ##diplomacy start+ #Store gender of creditor
                       (call_script, "script_dplmc_store_troop_is_female", ":quest_giver_troop"),
                       ##diplomacy end+
                       (quest_get_slot, reg10, "qst_collect_debt", slot_quest_target_amount)],
##diplomacy start+ Next lines, replace "him" with "{reg0?her:him}"
"My debt to {s8} has long been overdue and was a source of great discomfort to me.\
Thank you for accepting to take the money to {reg0?her:him}.\
Please give {reg0?her:him} these {reg10} mon and thank {reg0?her:him} on my behalf.", "close_window",
##diplomacy end+
[(call_script, "script_troop_add_gold", "trp_player", reg10),
(quest_set_slot,  "qst_collect_debt", slot_quest_current_state, 1),
(call_script, "script_succeed_quest", "qst_collect_debt"),
(assign, "$g_leave_encounter", 1),
]],
[anyone,"convince_accept",[(check_quest_active, "qst_persuade_lords_to_make_peace"),
                       (this_or_next|quest_slot_eq, "qst_persuade_lords_to_make_peace", slot_quest_target_troop, "$g_talk_troop"),
                       (quest_slot_eq, "qst_persuade_lords_to_make_peace", slot_quest_object_troop, "$g_talk_troop"),
                       (quest_get_slot, ":quest_object_faction", "qst_persuade_lords_to_make_peace", slot_quest_object_faction),
                       (quest_get_slot, ":quest_target_faction", "qst_persuade_lords_to_make_peace", slot_quest_target_faction),
                       (str_store_faction_name, s12, ":quest_object_faction"),
                       (str_store_faction_name, s13, ":quest_target_faction"),
                       (try_begin), # store name of other faction
                         (eq,":quest_object_faction","$g_talk_troop_faction"),
                         (str_store_faction_name, s14, ":quest_target_faction"),
                         (else_try),
                         (str_store_faction_name, s14, ":quest_object_faction"),
                       (try_end),
                       ],
"You... have convinced me, {playername}. Very well then, you've my blessing to bring a peace offer to {s14}. I cannot guarantee they will accept it, but on the off-chance they do, I will stand by it.", "close_window",
[(store_mul, ":new_value", "$g_talk_troop", -1),
(try_begin),
(quest_slot_eq, "qst_persuade_lords_to_make_peace", slot_quest_target_troop, "$g_talk_troop"),
(quest_set_slot, "qst_persuade_lords_to_make_peace", slot_quest_target_troop, ":new_value"),
(else_try),
(quest_set_slot, "qst_persuade_lords_to_make_peace", slot_quest_object_troop, ":new_value"),
(try_end),
(quest_set_slot, "qst_persuade_lords_to_make_peace", slot_quest_convince_value, 1500),#reseting convince value for the second persuasion
(assign, "$g_leave_encounter", 1),
(neg|quest_slot_ge, "qst_persuade_lords_to_make_peace", slot_quest_target_troop, 0),
(neg|quest_slot_ge, "qst_persuade_lords_to_make_peace", slot_quest_object_troop, 0),
(call_script, "script_succeed_quest", "qst_persuade_lords_to_make_peace"),
]],
[anyone,"party_encounter_lord_hostile_ultimatum_surrender", [],
"{s43}", "close_window", [
    (call_script, "script_lord_comment_to_s43", "$g_talk_troop", "str_lord_challenged_default"),

    (call_script, "script_make_kingdom_hostile_to_player", "$g_encountered_party_faction", -3),

    (try_begin),
      (gt, "$g_talk_troop_relation", -10),
      (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", -1),
    (try_end),
    (assign,"$encountered_party_hostile",1),
    (assign,"$encountered_party_friendly",0),]],
[anyone,"liege_defends_claim_1", [],
"Oh really? It is not everyone who dares mention that name in my presence. I am not sure whether to reward your bravery, or punish you for your impudence.", "liege_defends_claim_2", [
                         (troop_set_slot, "$g_talk_troop", slot_troop_discussed_rebellion, 1),
                 ]],
[anyone,"liege_defends_claim_2", [],
"Very well. I will indulge your curiosity. But listen closely, because I do not wish to speak of this matter again.", "liege_defends_claim_3", [
                 ]],
[anyone,"liege_defends_claim_3", [],
"{s48}", "liege_defends_claim_4", [
                  (store_sub, ":rebellion_string", "$g_talk_troop_faction", "fac_kingdom_1"),
                  (val_add, ":rebellion_string", "str_swadian_rebellion_monarch_response_1"),
                  (str_store_string, 48, ":rebellion_string"),
                  ]],
[anyone,"liege_defends_claim_4", [],
"{s48}", "lord_talk", [
                  (store_sub, ":rebellion_string", "$g_talk_troop_faction", "fac_kingdom_1"),
                  (val_add, ":rebellion_string", "str_swadian_rebellion_monarch_response_2"),
                  (str_store_string, 48, ":rebellion_string"),
                  ]],
[anyone|plyr,"party_encounter_lord_hostile_attacker_2",
[
  (eq, "$cheat_mode", 2),
  (gt, "$supported_pretender", 0),
  (eq, "$supported_pretender_old_faction", "$g_talk_troop_faction"),
  (neg|faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, "$g_talk_troop"),
  (troop_slot_ge, "$g_talk_troop", slot_troop_leaded_party, 1),
  ],
"{!}CHEAT - Join our cause by force.", "lord_join_rebellion_suggest_cheat",[]],
#  [anyone|plyr,"party_encounter_lord_hostile_attacker_2", [
#                             (gt, "$supported_pretender", 0),
#                             (eq, "$supported_pretender_old_faction", "$g_talk_troop_faction"),
#                             (neg|troop_slot_ge, "$g_talk_troop", slot_troop_intrigue_impatience, 100),
#                             (neg|faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, "$g_talk_troop"),
#                             (troop_slot_ge, "$g_talk_troop", slot_troop_leaded_party, 1),
#                             (str_store_troop_name, s12, "$supported_pretender"),
#                             (str_store_faction_name, s14, "$supported_pretender_old_faction"),
#                             (faction_get_slot, ":old_faction_lord", "$supported_pretender_old_faction", slot_faction_leader),
#                             (str_store_troop_name, s15, ":old_faction_lord"),
#                             ],
#   "{s12} is your rightful ruler. Join our cause against the usurper, {s15}!", "lord_join_rebellion_suggest",[]],



#  [anyone,"lord_join_rebellion_suggest", [
#                    (eq,"$talk_context",tc_party_encounter),
#                    (encountered_party_is_attacker),
#                    (lt, "$g_talk_troop_relation", -5),
#      ], "I have no time to bandy words with the likes of you. Now defend yourself!",
#   "party_encounter_lord_hostile_attacker_2",
#   [
#    (try_begin),
#		(neg|troop_slot_ge, "$g_talk_troop", slot_troop_intrigue_impatience, 100),
#		(troop_set_slot, "$g_talk_troop", slot_troop_intrigue_impatience, 100),
#	(try_end),

#    ]],


#removed a number of rebellion scripts...

#Rebellion changes end


[anyone|plyr,"lord_talk",
[
 (troop_get_slot, ":prison_location", "$g_talk_troop", slot_troop_prisoner_of_party),
 (is_between, ":prison_location", centers_begin, centers_end),
 (neg|party_slot_eq, ":prison_location", slot_town_lord, "trp_player"),
 (neq, "$talk_context", tc_prison_break),
],
"I've come to break you out of here.", "lord_prison_break_chains",[]],
[anyone ,"knight_offer_join", [(call_script, "script_cf_is_quest_troop", "$g_talk_troop")],
"I fear I cannot join you at the moment, {playername}, I've important business to attend to and it cannot wait.", "hero_pretalk",[]],
[anyone ,"knight_offer_join", [(lt, "$g_talk_troop_relation", 5),
                              (store_character_level,":player_level","trp_player"),
                              (store_character_level,":talk_troop_level","$g_talk_troop"),
                              (val_mul,":player_level",2),
                              (lt, ":player_level", ":talk_troop_level")],
"You forget your place, {sir/madam}. I do not take orders from the likes of you.", "hero_pretalk",[]],
[anyone ,"knight_offer_join", [
    (assign, ":num_player_companions",0),
    (try_for_range, ":hero_id", heroes_begin, heroes_end),
      (troop_slot_eq, ":hero_id",slot_troop_occupation, slto_player_companion),
      (val_add, ":num_player_companions",1),
    (try_end),
    (assign, reg5, ":num_player_companions"),
    (store_add, reg6, reg5, 1),
    (val_mul, reg6,reg6),
    (val_mul, reg6, 1000),
    (gt, reg6,0)], #note that we abuse the value of reg6 in the next line.
"I would be glad to fight at your side, my friend, but there is a problem...\
The thing is, I've found myself in a bit of debt that I must repay very soon. {reg6} mon altogether,\
and I am honour-bound to return every coin. Unless you've got {reg6} mon with you that you can spare,\
I've to keep my mind on getting this weight off my neck.", "knight_offer_join_2",[]],
[anyone ,"knight_offer_join", [(gt,reg6, 100000)], "Join you? I think not.", "close_window",[]],
[anyone ,"knight_offer_join", [], "Aye, my friend, I'll be happy to join you.", "knight_offer_join_2",[]],
[anyone|plyr,"knight_offer_join_2", [(gt, reg6,0),(store_troop_gold, ":gold", "trp_player"),(gt,":gold",reg6)],
"Here, take it, all {reg6} mon you need. 'Tis only money.", "knight_offer_join_accept",[(troop_remove_gold, "trp_player",reg6)]],
[anyone|plyr,"knight_offer_join_2", [(le, reg6,0)], "Then let us ride together, my friend.", "knight_offer_join_accept",[]],
[anyone|plyr,"knight_offer_join_2", [(eq, "$talk_context", tc_hero_freed)], "That's good to know. I will think on it.", "close_window",[]],
[anyone|plyr,"knight_offer_join_2", [(neq, "$talk_context", tc_hero_freed)], "That's good to know. I will think on it.", "hero_pretalk",[]],
[anyone ,"knight_offer_join_accept", [(troop_slot_ge, "$g_talk_troop", slot_troop_leaded_party, 1)],
"I've some trusted men in my band who could be of use to you. What do you wish to do with them?", "knight_offer_join_accept_party",[
   ]],
[anyone ,"knight_offer_join_accept", [], "Ah, certainly, it might be fun!", "close_window",[
   (call_script, "script_recruit_troop_as_companion", "$g_talk_troop"),
   (assign, "$g_leave_encounter",1)
   ]],
[anyone|plyr,"knight_offer_join_accept_party", [], "You may disband your men. I've no need for other troops.", "knight_join_party_disband",[]],
[anyone|plyr,"knight_offer_join_accept_party", [(troop_get_slot, ":companions_party","$g_talk_troop", slot_troop_leaded_party),
                                    (party_can_join_party,":companions_party","p_main_party"),
   ], "Your men may join as well. We need every soldier we can muster.", "knight_join_party_join",[]],
[anyone|plyr,"knight_offer_join_accept_party", [(is_between,"$g_encountered_party",centers_begin, centers_end)], "Lead your men out of the town. I shall catch up with you on the road.", "knight_join_party_lead_out",[]],
[anyone|plyr,"knight_offer_join_accept_party", [(neg|is_between,"$g_encountered_party",centers_begin, centers_end)],
"Keep doing what you were doing. I'll catch up with you later.", "knight_join_party_lead_out",[]],
[anyone ,"knight_join_party_disband", [], "Ah . . . Very well, {playername}. Much as I dislike losing good men,\
the decision is yours. I'll disband my troops and join you.", "close_window",[
   (call_script, "script_recruit_troop_as_companion", "$g_talk_troop"),

   (troop_get_slot, ":companions_party","$g_talk_troop", slot_troop_leaded_party),
   (party_detach, ":companions_party"),
   (remove_party, ":companions_party"),
   (assign, "$g_leave_encounter",1)
   ]],
[anyone ,"knight_join_party_join", [], "Excellent.\
My lads and I will ride with you.", "close_window",[
   (call_script, "script_recruit_troop_as_companion", "$g_talk_troop"),
   (party_remove_members, "p_main_party", "$g_talk_troop", 1),

   (troop_get_slot, ":companions_party","$g_talk_troop", slot_troop_leaded_party),
   (assign, "$g_move_heroes", 1),
   (call_script, "script_party_add_party", "p_main_party", ":companions_party"),
   (party_detach, ":companions_party"),
   (remove_party, ":companions_party"),
   (assign, "$g_leave_encounter",1)
   ]],
[anyone ,"knight_join_party_lead_out", [], "Very well then.\
I shall maintain a patrol of this area. Return if you have further orders for me.", "close_window",[
   (call_script, "script_recruit_troop_as_companion", "$g_talk_troop"),
   (party_remove_members, "p_main_party", "$g_talk_troop", 1),

   (troop_get_slot, ":companions_party","$g_talk_troop", slot_troop_leaded_party),
   (party_set_faction, ":companions_party", "fac_player_supporters_faction"),
   (party_detach, ":companions_party"),
   (party_set_ai_behavior, ":companions_party", ai_bhvr_patrol_location),
   (party_set_flags, ":companions_party", pf_default_behavior, 0),
   ]],
[anyone,"capture_enemy_hero_thank", [],
"Many thanks, my friend. He will serve very well for a bargain. You've done a fine work here. Please accept these {reg5} mon for your help.", "capture_enemy_hero_thank_2",
[(quest_get_slot, ":quest_target_troop", "qst_capture_enemy_hero", slot_quest_target_troop),
  (quest_get_slot, ":quest_target_faction", "qst_capture_enemy_hero", slot_quest_target_faction),
  (party_remove_prisoners, "p_main_party", ":quest_target_troop", 1),
  (store_relation, ":reln", "$g_encountered_party_faction", ":quest_target_faction"),
  (try_begin),
    (lt, ":reln", 0),
    (party_add_prisoners, "$g_encountered_party", ":quest_target_troop", 1), #Adding him to the dungeon
  (else_try),
    #Do not add a non-enemy lord to the dungeon (due to recent diplomatic changes or due to a neutral town/castle)
    #(troop_set_slot, ":quest_target_troop", slot_troop_is_prisoner, 0),
    (troop_set_slot, ":quest_target_troop", slot_troop_prisoner_of_party, -1),
  (try_end),
  (quest_get_slot, ":reward", "qst_capture_enemy_hero", slot_quest_gold_reward),
  (assign, reg5, ":reward"),
  (call_script, "script_troop_add_gold", "trp_player", ":reward"),
  (add_xp_as_reward, 2500),
  (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 4),
  (call_script, "script_end_quest", "qst_capture_enemy_hero"),
]],
[anyone|plyr,"capture_enemy_hero_thank_2", [],
"Certainly, {s65}.", "lord_pretalk",[]],
[anyone|plyr,"capture_enemy_hero_thank_2", [],
"It was nothing.", "lord_pretalk",[]],
[anyone|plyr,"capture_enemy_hero_thank_2", [],
"Give me more of a challenge next time.", "lord_pretalk",[]],
  [anyone,"enemy_lord_tell_mission", [(eq,"$random_quest_no","qst_lend_surgeon")],
   "I have a friend here, an old warrior, who is very sick. Pestilence has infected an old battle wound,\
 and unless he is seen to by a surgeon soon,  he will surely die. This man is dear to me, {playername},\
 but he's also stubborn as a hog and refuses to have anyone look at his injury because he doesn't trust the physicians here.\
 I have heard that you've a capable surgeon with you. If you would let your surgeon come here and have a look,\
 {reg3?she:he} may be able to convince him to give his consent to an operation.\
 Please, I will be deeply indebted to you if you grant me this request.", "lord_mission_told",
   [
     (quest_get_slot, ":quest_object_troop", "$random_quest_no", slot_quest_object_troop),
     (str_store_troop_name_link,1,"$g_talk_troop"),
##     (str_store_party_name,2,"$g_encountered_party"),
     (str_store_troop_name,3,":quest_object_troop"),
	 ##diplomacy start+ Use script for gender
     #(troop_get_type, reg3, ":quest_object_troop"),
	 (assign, reg3, 0),
	 (try_begin),
		(call_script, "script_cf_dplmc_troop_is_female", ":quest_object_troop"),
		(assign, reg3, 1),
	 (try_end),
	 ##diplomacy end+
     (setup_quest_text,"$random_quest_no"),
##     (try_begin),
##       (is_between, "$g_encountered_party", centers_begin, centers_end),
##       (setup_quest_giver, "$random_quest_no", "str_given_by_s1_at_s2"),
##     (else_try),
##       (setup_quest_giver,"$random_quest_no", "str_given_by_s1_in_wilderness"),
##     (try_end),
     (str_store_string, s2, "@Lend your experienced surgeon {s3} to {s1}."),
   ]],
  [anyone,"enemy_lord_tell_mission", [(str_store_quest_name, s7, "$random_quest_no")],
   "{!}ERROR: MATCHED WITH QUEST: {s7}.", "close_window",
   []],
#Spouse
  [anyone,"start",
   [
    (troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_lady),
#    (troop_slot_eq, "$g_talk_troop", slot_troop_spouse, "trp_player"),
    ##diplomacy start+
	(this_or_next|troop_slot_eq, "trp_player", slot_troop_spouse, "$g_talk_troop"),
		(troop_slot_eq, "$g_talk_troop", slot_troop_spouse, "trp_player"),
	(this_or_next|is_between, "$g_talk_troop", heroes_begin, heroes_end),
	##diplomacy end+
    (troop_slot_eq, "trp_player", slot_troop_spouse, "$g_talk_troop"),
	##diplomacy start+ load relation text into s0
    (call_script, "script_dplmc_print_player_spouse_says_my_husband_wife_to_s0", "$g_talk_troop", 0),
    ##diplomacy end+
    ],
	##diplomacy start+ use relation string
   "Yes, {s0}", "spouse_talk",[
    ##diplomacy end+
 ]],
   [anyone,"offer_gift_quest_complete", [
   (quest_get_slot, ":target_troop", "qst_offer_gift", slot_quest_target_troop),
   (troop_get_type, reg4, ":target_troop"),
   ],
   "Ah, let me take those. Hopefully this will mend the quarrel between you two. You may wish to speak to {reg4?her:him}, and see if I had any success.", "close_window",[
   (quest_set_slot, "qst_offer_gift", slot_quest_current_state, 2),
   (quest_set_slot, "qst_offer_gift", slot_quest_expiration_days, 365),
   (troop_remove_item, "trp_player", "itm_furs"),
   (troop_remove_item, "trp_player", "itm_velvet"),
   (assign, "$g_leave_encounter", 1),
]],
#Bride
  [anyone,"wedding_ceremony_bride_vow",
   [
#    (troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_lady),
#	(check_quest_active, "qst_wed_betrothed"),
#	(quest_slot_eq, "qst_wed_betrothed", slot_quest_target_troop, "$g_talk_troop"),
#	(quest_slot_eq, "qst_wed_betrothed", slot_quest_current_state, 2),
#	(neg|quest_slot_ge, "qst_wed_betrothed", slot_quest_expiration_days, 2),
    ],
   "My husband, I hearby pledge to be your wife, to stand with you in good times and bad. May the heavens smile upon us and bless us with children, livestock, and land.", "wedding_ceremony_player_vow",[
   (quest_get_slot, ":bride", "qst_wed_betrothed", slot_quest_target_troop),
   (set_conversation_speaker_troop, ":bride"),
 ]],
  [anyone|plyr,"wedding_ceremony_player_vow",
   [],
   "I pledge the same. Let us be husband and wife.", "wedding_ceremony_vows_complete",[
 ]],
  [anyone|plyr,"wedding_ceremony_player_vow",
   [],
   "Wait -- hold on... I'm not quite ready for this.", "close_window",[
 ]],
  [anyone,"wedding_ceremony_vows_complete",
   [],
   "I now declare you and {s3} to be husband and wife. Go now to the chamber prepared for you, and we shall make arrangements for your bride to join you in your hall in {s11}.", "close_window",[
   	(call_script, "script_courtship_event_bride_marry_groom", "$g_player_bride", "trp_player", 0), #parameters from dialog
	(call_script, "script_get_kingdom_lady_social_determinants", "$g_player_bride"),
	(str_store_troop_name, s3, "$g_player_bride"),

    (try_begin),
		(neq, reg0, "trp_player"),
		(str_store_string, s11, "str_error__player_not_logged_as_groom"),
	(else_try),
		(str_store_party_name, s11, reg1),
		(troop_set_slot, "$g_player_bride", slot_troop_cur_center, reg1),
	(try_end),
 ]],
  [anyone,"start",	#too early
   [
    (troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_lady),
	(check_quest_active, "qst_wed_betrothed"),
	(quest_slot_eq, "qst_wed_betrothed", slot_quest_target_troop, "$g_talk_troop"),
	(quest_slot_ge, "qst_wed_betrothed", slot_quest_expiration_days, 2),
    ],
   "How wonderful it is... In a short while we shall be married! However, I should point out that, in the remaining few days, it is not customary for us to speak too much together.", "close_window",[
	(try_begin),
		(check_quest_active, "qst_visit_lady"),
		(quest_slot_eq, "qst_visit_lady", slot_quest_giver_troop, "$g_talk_troop"),
		(call_script, "script_end_quest", "qst_visit_lady"),
	(try_end),
 ]],
  [anyone,"start",
   [
    (troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_lady),
	(check_quest_active, "qst_wed_betrothed"),
	(quest_slot_eq, "qst_wed_betrothed", slot_quest_target_troop, "$g_talk_troop"),
	(call_script, "script_get_kingdom_lady_social_determinants", "$g_talk_troop"),
	(assign, ":guardian", reg0),
#	(call_script, "script_get_heroes_attached_to_center", "$g_encountered_party", "p_temp_party"),
	(troop_get_slot, ":guardian_led_party", ":guardian", slot_troop_leaded_party),
	(party_is_active, ":guardian_led_party"),
	(party_get_attached_to, ":guardian_led_party_attached", ":guardian_led_party"),
	(eq, ":guardian_led_party_attached", "$g_encountered_party"),

	(call_script, "script_troop_get_family_relation_to_troop", ":guardian", "$g_talk_troop"),
	(str_store_troop_name, s4, ":guardian"),
	#use current location, or party is in?
    ],
   "Em, {playername}, you might not be used to our wedding customs, but I had hoped that someone would tell you... Speak first to my {s11}, {s4}.", "close_window",[
 ]],
  [anyone,"start",
   [
    (troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_lady),
	(check_quest_active, "qst_wed_betrothed"),
	(quest_slot_eq, "qst_wed_betrothed", slot_quest_target_troop, "$g_talk_troop"),
	(quest_get_slot, ":giver_troop", "qst_wed_betrothed", slot_quest_giver_troop),
	(call_script, "script_troop_get_family_relation_to_troop", ":giver_troop", "$g_talk_troop"),
    (str_store_troop_name, s10, ":giver_troop"),
	##diplomacy start+
	#check pronouns/gendered words in case it's changed so the guardian can be a woman
    ],
   "I do not know where to find my {s11} {s10}, who by tradition should preside over our wedding. Perhaps we should wait until {reg4?she:he} can be found...", "close_window",[
    ##diplomacy end+
   (assign, "$g_leave_encounter", 1),
 ]],
#Captive
  [anyone,"start",
   [
    (troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_lady),
	(neq, "$g_talk_troop_faction", "$g_encountered_party_faction"),
        ##diplomacy start+ slot_town_lord is 7... there's no way this can work
	#(party_get_slot, ":town_lord", "$g_encountered_party"),
        (party_get_slot, ":town_lord", "$g_encountered_party", slot_town_lord),
        ##diplomacy end+
	(ge, ":town_lord", active_npcs_begin),
	(str_store_troop_name, s12, ":town_lord"),
    ],
   "The honorable {s12} has agreed to allow us to return home to our families. We shall be departing shortly.", "close_window",[
 ]],
  [anyone,"start", #default for time since last talk
   [
    (troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_lady),
	(neg|troop_slot_eq, "trp_player", slot_troop_spouse, "$g_talk_troop"),
	(neq, "$g_talk_troop_faction", "$g_encountered_party_faction"),
    (troop_slot_eq, "$g_talk_troop", slot_troop_prisoner_of_party, "$g_encountered_party"),
	(gt, "$g_time_since_last_talk", 24),
    ],
   "So great is my loneliness! How I miss my family!", "kingdom_lady_captive",[
 ]],
  [anyone,"start",
   [
    (troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_lady),
	(neg|troop_slot_eq, "trp_player", slot_troop_spouse, "$g_talk_troop"),
	(neq, "$g_talk_troop_faction", "$g_encountered_party_faction"),
    (troop_slot_eq, "$g_talk_troop", slot_troop_prisoner_of_party, "$g_encountered_party"),
	(lt, "$g_talk_troop_relation", 1),
    ],
##diplomacy start+ Allow the possibility of male versions of the lines
   "You are a cad, {sir/madame}, to hold a {reg65?lady:free-spirited lad} like this...", "kingdom_lady_captive",[#"a lady" -> "a {reg65?lady:free-spirited lad}"
 ]],
##diplomacy end+

  [anyone,"start",
   [
    (troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_lady),
	(neg|troop_slot_eq, "trp_player", slot_troop_spouse, "$g_talk_troop"),
	(neq, "$g_talk_troop_faction", "$g_encountered_party_faction"),
    (troop_slot_eq, "$g_talk_troop", slot_troop_prisoner_of_party, "$g_encountered_party"),
	(lt, "$g_talk_troop_relation", 11),
    ],
   "It is strange. On occasion you have shown me such kindness, and yet you continue to hold me here against my will.", "kingdom_lady_captive",[
 ]],
  [anyone,"start",
   [
    (troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_lady),
	(neg|troop_slot_eq, "trp_player", slot_troop_spouse, "$g_talk_troop"),
	(neq, "$g_talk_troop_faction", "$g_encountered_party_faction"),
    (troop_slot_eq, "$g_talk_troop", slot_troop_prisoner_of_party, "$g_encountered_party"),
    ],
   "Why haven't my family paid my ransom? You may hold me as prisoner, but it seems that you care for me more than they do!", "kingdom_lady_captive",[
 ]],
  [anyone|auto_proceed, "start",
  [
    (troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_lady),
	(neg|troop_slot_eq, "trp_player", slot_troop_spouse, "$g_talk_troop"),
	(neq, "$g_talk_troop_faction", "$g_encountered_party_faction"),
    (troop_slot_eq, "$g_talk_troop", slot_troop_cur_center, "$g_encountered_party"),

	(call_script, "script_get_kingdom_lady_social_determinants", "$g_talk_troop"),
	(assign, ":guardian", reg0),
	(neq, "$g_encountered_party_faction", "fac_player_supporters_faction"),

	(store_faction_of_troop, ":guardian_faction", ":guardian"),
	(neq, ":guardian_faction", "$g_encountered_party_faction"),
  ],
  "{!}.", "lady_stranded_next",
  []],
  [anyone,"start",
   [
    (troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_lady),
	(neg|troop_slot_eq, "trp_player", slot_troop_spouse, "$g_talk_troop"),
	(neq, "$g_talk_troop_faction", "$g_encountered_party_faction"),
    (troop_slot_eq, "$g_talk_troop", slot_troop_cur_center, "$g_encountered_party"),

	(call_script, "script_get_kingdom_lady_social_determinants", "$g_talk_troop"),
	(assign, ":guardian", reg0),
	(store_faction_of_troop, ":guardian_faction", ":guardian"),
	(neq, ":guardian_faction", "$g_encountered_party_faction"),

    ],
	#Changed "ladies" to "{reg65?ladies:lads}"
   "{playername} -- I assume that you, as a {man/lady} of honor, will accord high-born {reg65?ladies:men} such as ourselves the right to return to our families, and not demand a ransom.", "lady_talk_refugee",[
   ##diplomacy end+
 ]],
  [anyone,"start",
   [
    (troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_lady),
	(neg|troop_slot_eq, "trp_player", slot_troop_spouse, "$g_talk_troop"),
	(neq, "$g_talk_troop_faction", "$g_encountered_party_faction"),
    (troop_get_slot, ":new_location", "$g_talk_troop", slot_troop_cur_center),
	(str_clear, s5),
	(try_begin),
		(is_between, ":new_location", centers_begin, centers_end),
		(str_store_party_name, s4, ":new_location"),
		(str_store_string, s5, "str_for_s4"),
	(try_end),
    ],
   "We will shortly depart{s5}. It is good to know that some people in this world retain a sense of honor.", "close_window",[
 ]],
#incomplete





#Kingdom ladies quest resolution

  [anyone,"start",
   [
    (troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_lady),
	(check_quest_active, "qst_duel_courtship_rival"),
    (check_quest_failed, "qst_duel_courtship_rival"),
    (quest_slot_eq, "qst_duel_courtship_rival", slot_quest_giver_troop, "$g_talk_troop"),
    (quest_get_slot, ":quest_target_troop", "qst_duel_courtship_rival", slot_quest_target_troop),
    (str_store_troop_name, s10, ":quest_target_troop"),
	(lt, "$g_talk_troop_relation", 0),
    ],
   "Well, {playername} -- you fought a duel with {s10}, and lost. According to our custom and tradition, I should no longer receive you. Farewell, {playername}.", "close_window",[
    (call_script, "script_end_quest", "qst_duel_courtship_rival"),
	(troop_set_slot, "$g_talk_troop", slot_troop_met, 4),
 ]],
#incomplete


  [anyone,"start",
   [
    (troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_lady),
	(check_quest_active, "qst_duel_courtship_rival"),
    (check_quest_failed, "qst_duel_courtship_rival"),
    (quest_slot_eq, "qst_duel_courtship_rival", slot_quest_giver_troop, "$g_talk_troop"),
    (quest_get_slot, ":quest_target_troop", "qst_duel_courtship_rival", slot_quest_target_troop),
    (str_store_troop_name, s10, ":quest_target_troop"),
	##diplomacy start+
	#check pronouns/gendered words in case it's possible for the other lord to be a woman
	(call_script, "script_dplmc_store_troop_is_female_reg", ":quest_target_troop", 3),
    ],
   "Oh {playername} -- I heard of your duel with {s10}. I wish now that you had never fought {reg3?her:him}, for our honor and tradition demand that, having lost to {reg3?her:him}, you now break off your suit with me. Farewell, {playername}.", "lady_duel_lost",[
    ##diplomacy end+
    (troop_set_slot, "$g_talk_troop", slot_troop_met, 4),
    (call_script, "script_end_quest", "qst_duel_courtship_rival"),
 ]],
  [anyone,"start",
   [
    (troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_lady),
	(check_quest_active, "qst_duel_courtship_rival"),
    (check_quest_succeeded, "qst_duel_courtship_rival"),
    (quest_slot_eq, "qst_duel_courtship_rival", slot_quest_giver_troop, "$g_talk_troop"),
    (quest_get_slot, ":quest_target_troop", "qst_duel_courtship_rival", slot_quest_target_troop),
	(call_script, "script_troop_get_relation_with_troop", "$g_talk_troop", ":quest_target_troop"),
	(lt, reg0, 0),
    (str_store_troop_name_link, s10, ":quest_target_troop"),
	##diplomacy start+
	#check pronouns/gendered words in case it's possible for the other lord to be a woman
	(call_script, "script_dplmc_store_troop_is_female_reg", ":quest_target_troop", 3),
    ],
   "Oh, {playername} -- I have heard that you won your duel with {s10}. I'm grateful that you have delivered me from that {reg3?woman:man}'s attentions!",
   ##diplomacy end+
   "lady_start",[
	(call_script, "script_end_quest", "qst_duel_courtship_rival"),
	(call_script, "script_troop_change_relation_with_troop", "trp_player", "$g_talk_troop", 3),
    (add_xp_as_reward, 1000),

 ]],
#incomplete


 [anyone,"start",
   [
    (troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_lady),
	(check_quest_active, "qst_duel_courtship_rival"),
    (check_quest_succeeded, "qst_duel_courtship_rival"),
    (quest_slot_eq, "qst_duel_courtship_rival", slot_quest_giver_troop, "$g_talk_troop"),
    (quest_get_slot, ":quest_target_troop", "qst_duel_courtship_rival", slot_quest_target_troop),
	(troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_ambitious),
	(call_script, "script_troop_get_relation_with_troop", "$g_talk_troop", ":quest_target_troop"),
    (str_store_troop_name_link, s10, ":quest_target_troop"),
	##diplomacy start+
	#check pronouns/gendered words in case it's possible for the other lord to be a woman
	(call_script, "script_dplmc_store_troop_is_female_reg", ":quest_target_troop", 3),
    ],
   "Well, {playername} --  you won your duel with {s10}. Clearly, {reg3?she:he} was not worthy of my affections.", "lady_start",[
    ##diplomacy end+
   (call_script, "script_end_quest", "qst_duel_courtship_rival"),
	(call_script, "script_troop_change_relation_with_troop", "trp_player", "$g_talk_troop", 2),
    (add_xp_as_reward, 1000),
 ]],
[anyone|auto_proceed,"start",
   [
    (troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_lady),
	(check_quest_active, "qst_duel_courtship_rival"),
    (check_quest_succeeded, "qst_duel_courtship_rival"),
    (quest_slot_eq, "qst_duel_courtship_rival", slot_quest_giver_troop, "$g_talk_troop"),
    (quest_get_slot, ":quest_target_troop", "qst_duel_courtship_rival", slot_quest_target_troop),
	(troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_conventional),
	(call_script, "script_troop_get_relation_with_troop", "$g_talk_troop", ":quest_target_troop"),
    (str_store_troop_name_link, s10, ":quest_target_troop"),
    ],
   "{!}.", "lady_duel_rep_1",[]],
   [anyone|auto_proceed,"start",
   [
    (troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_lady),
	(check_quest_active, "qst_duel_courtship_rival"),
    (check_quest_succeeded, "qst_duel_courtship_rival"),
    (quest_slot_eq, "qst_duel_courtship_rival", slot_quest_giver_troop, "$g_talk_troop"),
    (quest_get_slot, ":quest_target_troop", "qst_duel_courtship_rival", slot_quest_target_troop),
	(call_script, "script_troop_get_relation_with_troop", "$g_talk_troop", ":quest_target_troop"),
    (str_store_troop_name_link, s10, ":quest_target_troop"),
    ],
   "{!}.", "lady_duel_rep_2",[]],
  [anyone,"start",
   [
    (troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_lady),
    (check_quest_active, "qst_duel_for_lady"),
    (check_quest_succeeded, "qst_duel_for_lady"),
    (quest_slot_eq, "qst_duel_for_lady", slot_quest_giver_troop, "$g_talk_troop"),
    (le, "$talk_context", tc_siege_commander),
    (quest_get_slot, ":quest_target_troop", "qst_duel_for_lady", slot_quest_target_troop),
    (str_store_troop_name_link, s13, ":quest_target_troop"),
	##diplomacy start+
	#check pronouns in case it's possible for the other lord to be a woman
	(call_script, "script_dplmc_store_troop_is_female_reg", ":quest_target_troop", 3),
    ],
   "My dear {playername}, how joyous to see you again! I heard you gave that vile {s13} a well-deserved lesson.\
 I hope {reg3?she:he} never forgets {reg3?her:his} humiliation.\
 I've a reward for you, but I fear it's little compared to what you've done for me.", "lady_qst_duel_for_lady_succeeded_1",[]],
  [anyone,"start",
   [
     (troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_lady),
     (check_quest_active, "qst_duel_for_lady"),
     (check_quest_failed, "qst_duel_for_lady"),
     (quest_slot_eq, "qst_duel_for_lady", slot_quest_giver_troop, "$g_talk_troop"),
     (le, "$talk_context", tc_siege_commander),
     (quest_get_slot, ":quest_target_troop", "qst_duel_for_lady", slot_quest_target_troop),
     (str_store_troop_name_link, s13, ":quest_target_troop"),
     ],
   "I was told that you sought satisfaction from {s13} to prove my innocence, {playername}.\
 It was a fine gesture, and I thank you for your efforts.", "lady_qst_duel_for_lady_failed", []],
  [anyone,"start", [(troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_lady),
                    (check_quest_active, "qst_escort_lady"),
                    (eq, "$talk_context", tc_entering_center_quest_talk),
                    (quest_slot_eq, "qst_escort_lady", slot_quest_object_troop, "$g_talk_troop")],
   "Thank you for escorting me here, {playername}. Please accept this gift as a token of my gratitude.\
 I hope we shall meet again sometime in the future.", "lady_escort_lady_succeeded",
   [
     (quest_get_slot, ":cur_center", "qst_escort_lady", slot_quest_target_center),
     (add_xp_as_reward, 300),
     (call_script, "script_troop_add_gold", "trp_player", 250),
     (call_script, "script_end_quest", "qst_escort_lady"),
     (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 2),
     (troop_set_slot, "$g_talk_troop", slot_troop_cur_center, ":cur_center"),
     (remove_member_from_party,"$g_talk_troop"),
     ]],
	[anyone,"start", [
	(troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_lady),
  	(troop_set_slot, "$g_talk_troop", slot_lady_no_messages, 0), #do this for all
    (check_quest_active, "qst_visit_lady"),
    (quest_slot_eq, "qst_visit_lady", slot_quest_giver_troop, "$g_talk_troop"),
	], "Ah {playername} - you must have received my message. How happy I am that you could come!", "lady_start",[
	(call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 1),
    (call_script, "script_end_quest", "qst_visit_lady"),
#	(assign, "$g_time_to_spare", 1),
	]],
	[anyone,"start", [
	(troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_lady),
    (check_quest_active, "qst_formal_marriage_proposal"),
    (quest_slot_eq, "qst_formal_marriage_proposal", slot_quest_giver_troop, "$g_talk_troop"),
	(neg|check_quest_succeeded, "qst_formal_marriage_proposal"),
	(neg|check_quest_failed, "qst_formal_marriage_proposal"),
	], "{playername} - is there any word from my family?", "lady_proposal_pending",[
	]],
	[anyone,"start",
	[
	(troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_lady),
    (check_quest_active, "qst_formal_marriage_proposal"),
    (quest_slot_eq, "qst_formal_marriage_proposal", slot_quest_giver_troop, "$g_talk_troop"),
	(check_quest_failed, "qst_formal_marriage_proposal"),
	(call_script, "script_get_kingdom_lady_social_determinants", "$g_talk_troop"),
	(assign, ":guardian", reg0),
	(call_script, "script_troop_get_family_relation_to_troop", ":guardian", "$g_talk_troop"),
    ],
   "I hear that my {s11} has refused your request to marry me. Does that mean that we must part?", "lady_betrothed",[
	(call_script, "script_end_quest", "qst_formal_marriage_proposal"),
   ]],
	#Marriage success


  [anyone,"start", [
    (troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_lady),
    (le, "$talk_context", tc_siege_commander),
    (check_quest_active, "qst_rescue_lord_by_replace"),
    (check_quest_succeeded, "qst_rescue_lord_by_replace"),
    (quest_slot_eq, "qst_rescue_lord_by_replace", slot_quest_giver_troop, "$g_talk_troop"),
	(quest_get_slot, ":cur_lord", "qst_rescue_lord_by_replace", slot_quest_target_troop),
    (call_script, "script_troop_get_family_relation_to_troop", ":cur_lord", "$g_talk_troop"),
	##diplomacy start+ check pronouns in case the quest is altered to allow rescuing female prisoners
    ],
   "Oh, {playername}, you brought {reg4?her:him} back to me! Thank you ever so much for rescuing my {s11}.\
 Please, take this as some small repayment for your noble deed.", "lady_generic_mission_succeeded",
    ##diplomacy end+
   [
     (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 8),
     (add_xp_as_reward, 2000),
     (call_script, "script_troop_add_gold", "trp_player", 1500),
     (call_script, "script_end_quest", "qst_rescue_lord_by_replace"),
     ]],
  [anyone,"start", [
    (troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_lady),
    (check_quest_active, "qst_rescue_prisoner"),
    (check_quest_succeeded, "qst_rescue_prisoner"),
    (quest_slot_eq, "qst_rescue_prisoner", slot_quest_giver_troop, "$g_talk_troop"),
	(quest_get_slot, ":cur_lord", "qst_rescue_prisoner", slot_quest_target_troop),
    (call_script, "script_troop_get_family_relation_to_troop", ":cur_lord", "$g_talk_troop"),
	##diplomacy start+ check pronouns in case the quest is altered to allow rescuing female prisoners
    ],
   "Oh, {playername}, you brought {reg4?her:him} back to me! Thank you ever so much for rescuing my {s11}.\
 Please, take this as some small repayment for your noble deed.", "rescue_prisoner_succeed_1",
    ##diplomacy end+
    [
     (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 8),
     (add_xp_as_reward, 2000),
     (call_script, "script_troop_add_gold", "trp_player", 1500),
     (call_script, "script_end_quest", "qst_rescue_prisoner"),
     ]],
  #first time greetings
	[anyone ,"start", [(troop_slot_eq,"$g_talk_troop",slot_troop_occupation, slto_kingdom_lady),
                     (eq, "$g_talk_troop_met", 0),
                     (gt, "$g_player_tournament_placement", 4),
					 (str_clear, s8),

                     ],
   "You must be {playername}. We have just had the honor of watching you distinguish yourself in the recent tournament{s8}.",
   "lady_meet_end", []],
  [anyone ,"start", [(troop_slot_eq,"$g_talk_troop",slot_troop_occupation, slto_kingdom_lady),
                     (eq, "$g_talk_troop_met", 0),
                     (le,"$talk_context",tc_siege_commander),

					 (assign, ":known_by_relative", 0),
					 (str_clear, s15),
					 (try_for_range, ":lord", lords_begin, lords_end),
						(call_script, "script_troop_get_family_relation_to_troop", ":lord", "$g_talk_troop"),
						(gt, reg0, 5),

						(call_script, "script_troop_get_relation_with_troop", "trp_player", ":lord"),
						(gt, reg0, 10),

						(str_store_string, s15, s11),
						(str_store_troop_name, s16, ":lord"),
						(assign, ":known_by_relative", ":lord"),
					 (try_end),


					 (gt, ":known_by_relative", 0),

                     ],
   "You must be {playername}. My {s15} {s16} has spoken most highly of you. I am delighted to make your acquaintance.",
   "lady_meet_end", []],
  [anyone ,"start", [(troop_slot_eq,"$g_talk_troop",slot_troop_occupation, slto_kingdom_lady),
                     (eq, "$g_talk_troop_met", 0),
                     (le,"$talk_context",tc_siege_commander),
                     ],
   "I say, you don't look familiar...", "lady_premeet", []],
   #default greet
  [anyone,"start",
   [(troop_slot_eq, "$g_talk_troop", slot_troop_met, 4),
    (lt, "$g_talk_troop_relation", 0),
    ],
   "Ah, {playername}. How good it is to see you again. However, I believe that I am required elsewhere.", "close_window",[]],
  [anyone,"start",
   [(troop_slot_eq, "$g_talk_troop", slot_troop_met, 4),
    ],
   "{playername} -- how good it is to see you. (Whispers:) I still remember your visits fondly.", "lady_start",[]],
	[anyone ,"start", [(troop_slot_eq,"$g_talk_troop",slot_troop_occupation, slto_kingdom_lady),
                     (eq, "$g_talk_troop_met", 0),
                     (gt, "$g_player_tournament_placement", 4),
					 (ge, "$g_talk_troop_relation", 0),
                     ],
   "Ah, {playername}. How spendid it was to see you distinguish yourself in the recent tournament.",
   "lady_meet_end", []],
  [anyone,"start", [
					(troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_lady),
					(str_store_string, s12, "str_hello_playername"),
#					(assign, "$g_time_to_spare", 1),
                    ],
   "{s12}", "lady_start",[]],
#Convincing bargaining
  [anyone,"convince_begin", [], "I still don't see why I should accept what you're asking of me.", "convince_options",
   [(quest_get_slot, "$convince_value", "$g_convince_quest", slot_quest_convince_value),
    ]],
  [anyone|plyr,"convince_options", [(assign, reg8, "$convince_value")], "Then I'll make it worth your while. ({reg8} mon)", "convince_bribe",[]],
  [anyone|plyr,"convince_options",
  [(store_div, "$convince_relation_penalty", "$convince_value", 300),
   (val_add, "$convince_relation_penalty", 1),
   (assign, reg9, "$convince_relation_penalty")],
   "Please, do it for the sake of our friendship. (-{reg9} to relation)", "convince_friendship",[]],
  [anyone|plyr,"convince_options", [], "Let me try and convince you. (Persuasion)", "convince_persuade_begin", []],
  [anyone|plyr,"convince_options", [], "Never mind.", "lord_pretalk",[]],
  [anyone,"convince_bribe", [], "Mmm, a generous gift to my coffers would certainly help matters...\
 {reg8} mon should do it. If you agree, then I'll go with your suggestion.", "convince_bribe_verify",[]],
  [anyone|plyr,"convince_bribe_verify", [(store_troop_gold, ":gold", "trp_player"),
                                         (lt, ":gold", "$convince_value")],
   "I'm afraid my finances will not allow for such a gift.", "convince_bribe_cant_afford",[]],
  [anyone|plyr,"convince_bribe_verify", [(store_troop_gold, ":gold", "trp_player"),
                                         (ge, ":gold", "$convince_value")],
  "Very well, please accept these {reg8} mon as a token of my gratitude.", "convince_bribe_goon",[]],
  [anyone|plyr,"convince_bribe_verify", [], "Let me think about this some more.", "convince_begin",[]],
  [anyone,"convince_bribe_cant_afford", [], "Ah. In that case, there is little I can do,\
 unless you have some further argument to make.", "convince_options",[]],
   [anyone,"convince_bribe_goon", [], "My dear {playername}, your generous gift has led me to reconsider what you ask,\
 and I have come to appreciate the wisdom of your proposal.", "convince_accept",[
 ##diplomacy start+ add removed gold to bribed lord
 (call_script, "script_dplmc_distribute_gold_to_lord_and_holdings", "$convince_value", "$g_talk_troop"),
 ##diplomacy end+
 (troop_remove_gold, "trp_player","$convince_value")]],
  [anyone,"convince_friendship",
   [(store_add, ":min_relation", 5, "$convince_relation_penalty"),
    (ge, "$g_talk_troop_effective_relation", ":min_relation")], "You've done well by me in the past, {playername},\
 and for that I will go along with your request, but know that I do not like you using our relationship this way.", "convince_friendship_verify",[]],
  [anyone|plyr,"convince_friendship_verify", [], "I am sorry, my friend, but I need your help in this.", "convince_friendship_go_on",[]],
  [anyone|plyr,"convince_friendship_verify", [], "If it will not please you, then I'll try something else.", "lord_pretalk",[]],
  [anyone,"convince_friendship_go_on", [], "All right then, {playername}, I will accept this for your sake. But remember, you owe me for this.", "convince_accept",
   [(store_sub, ":relation_change", 0, "$convince_relation_penalty"),
    (call_script, "script_change_player_relation_with_troop","$g_talk_troop",":relation_change")]],
  [anyone,"convince_friendship",
   [(ge, "$g_talk_troop_relation", -5)], "I don't think I owe you such a favor {playername}.\
 I see no reason to accept this for you.", "lord_pretalk",[]],
  [anyone,"convince_friendship", [], "Is this a joke? You've some nerve asking me for favours, {playername},\
 and let me assure you you'll get none.", "lord_pretalk",[]],
  [anyone,"convince_persuade_begin",
  [(troop_get_slot, ":last_persuasion_time", "$g_talk_troop", slot_troop_last_persuasion_time),
   (store_current_hours, ":cur_hours"),
   (store_add, ":valid_time", ":last_persuasion_time", 24),
   (gt, ":cur_hours", ":valid_time"),
   ],
   "Very well. Make your case.", "convince_persuade_begin_2",[]],
  [anyone|plyr,"convince_persuade_begin_2", [], "[Attempt to persuade]", "convince_persuade",[
        (try_begin),
          (store_random_in_range, ":rand", 0, 100),
          (lt, ":rand", 30),
          (store_current_hours, ":cur_hours"),
          (troop_set_slot, "$g_talk_troop", slot_troop_last_persuasion_time, ":cur_hours"),
        (try_end),
        (store_skill_level, ":persuasion_level", "skl_persuasion", "trp_player"),
        (store_add, ":persuasion_potential", ":persuasion_level", 5),

        (store_random_in_range, ":random_1", 0, ":persuasion_potential"),
        (store_random_in_range, ":random_2", 0, ":persuasion_potential"),
        (store_add, ":rand", ":random_1", ":random_2"),

        (assign, ":persuasion_difficulty", "$convince_value"),
        (convert_to_fixed_point, ":persuasion_difficulty"),
        (store_sqrt, ":persuasion_difficulty", ":persuasion_difficulty"),
        (convert_from_fixed_point, ":persuasion_difficulty"),
        (val_div, ":persuasion_difficulty", 10),
        (val_add, ":persuasion_difficulty", 4),

        (store_sub, "$persuasion_strength", ":rand", ":persuasion_difficulty"),
        (val_mul, "$persuasion_strength", 20),
        (assign, reg5, "$persuasion_strength"),
        (val_sub, "$convince_value", "$persuasion_strength"),
        (quest_set_slot, "$g_convince_quest", slot_quest_convince_value, "$convince_value"),
        (str_store_troop_name, s50, "$g_talk_troop"),
		##diplomacy start+
		##OLD:
        #(troop_get_type, reg51, "$g_talk_troop"),
		##NEW:
		(try_begin),
			(call_script, "script_cf_dplmc_troop_is_female", "$g_talk_troop"),
			(assign, reg51, 1),
			(assign, reg65, 1),
		(else_try),
			(assign, reg51, 0),
			(assign, reg65, 0),
		(try_end),
		##diplomacy end+
        (try_begin),
          (lt, "$persuasion_strength", -30),
          (str_store_string, s5, "str_persuasion_summary_very_bad"),
        (else_try),
          (lt, "$persuasion_strength", -10),
          (str_store_string, s5, "str_persuasion_summary_bad"),
        (else_try),
          (lt, "$persuasion_strength", 10),
          (str_store_string, s5, "str_persuasion_summary_average"),
        (else_try),
          (lt, "$persuasion_strength", 30),
          (str_store_string, s5, "str_persuasion_summary_good"),
        (else_try),
          (str_store_string, s5, "str_persuasion_summary_very_good"),
        (try_end),
        (dialog_box, "@{s5} (Persuasion strength: {reg5})", "@Persuasion Attempt"),
  ]],
  [anyone|plyr,"convince_persuade_begin_2", [], "Wait, perhaps there is another way to convince you.", "convince_begin",[]],
  [anyone,"convince_persuade_begin", [], "By God's grace, {playername}!\
 Haven't we talked enough already? I am tired of listening to you,\
 and I do not want to hear any more of it right now.", "lord_pretalk",[]],
  [anyone,"convince_persuade", [(le, "$convince_value", 0)], "All right, all right. You have persuaded me to it.\
 I'll go ahead with what you suggest.", "convince_accept",[]],
  [anyone,"convince_persuade", [(gt, "$persuasion_strength", 5)], "You've a point, {playername},\
 I'll admit that much. However I am not yet convinced I should do as you bid.", "convince_options",[]],
  [anyone,"convince_persuade", [(gt, "$persuasion_strength", -5)], "Enough, {playername}.\
 You've a lot of arguments, but I find none of them truly convincing. I stand by what I said before.", "convince_options",[]],
  [anyone,"convince_persuade", [], "Truthfully, {playername}, I fail to see the virtue of your reasoning.\
 What you ask for makes even less sense now than it did before.", "convince_options",[]],
#Seneschal

  [anyone,"start", [(troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_seneschal),
                    (eq, "$talk_context", tc_siege_won_seneschal),
                    (str_store_party_name, s1, "$g_encountered_party"),
                    ],
   "I must congratulate you on your victory, my {lord/lady}. Welcome to {s1}.\
 We, the housekeepers of this castle, are at your service.", "siege_won_seneschal_1",[]],
  [anyone,"start", [(troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_seneschal),(eq,"$g_talk_troop_met",0),(str_store_party_name,s1,"$g_encountered_party")],
   "Good day, {sir/madam}. I do nott believe I've seen you here before.\
 Let me extend my welcome to you as the seneschal of {s1}.", "seneschal_intro_1",[]],
  [anyone|plyr,"seneschal_intro_1", [],  "A pleasure to meet you, {s65}.", "seneschal_intro_1a",[]],
  [anyone,"seneschal_intro_1a", [], "How can I help you?", "seneschal_talk",[]],
  [anyone|plyr,"seneschal_intro_1", [],  "What exactly do you do here?", "seneschal_intro_1b",[]],
  [anyone,"seneschal_intro_1b", [], "Ah, a seneschal's duties are many, good {sire/woman}.\
 For example, I collect the rents from my lord's estates, I manage the castle's storerooms,\
 I deal with the local peasantry, I take care of castle staff, I arrange supplies for the garrison...\
 All mundane matters on this fief are my responsibility, on behalf of my lord.\
 Everything except commanding the soldiers themselves.", "seneschal_talk",[]],
  [anyone,"start", [(troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_seneschal)],
   "Good day, {sir/madam}.", "seneschal_talk",[]],
  [anyone,"seneschal_pretalk", [], "Anything else?", "seneschal_talk",[]],
##### TODO: QUESTS COMMENT OUT BEGIN
##  [anyone|plyr,"seneschal_talk", [(check_quest_active, "qst_deliver_supply_to_center_under_siege"),
##                                  (quest_slot_eq, "qst_deliver_supply_to_center_under_siege", slot_quest_target_troop, "$g_talk_troop"),
##                                  (quest_slot_eq, "qst_deliver_supply_to_center_under_siege", slot_quest_current_state, 1),
##                                  (store_item_kind_count, ":no_supplies", "itm_siege_supply"),
##                                  (quest_get_slot, ":target_amount", "qst_deliver_supply_to_center_under_siege", slot_quest_target_amount),
##                                  (ge, ":no_supplies", ":target_amount")],
##   "TODO: Here are the supplies.", "seneschal_supplies_given",[]],
##
##  [anyone|plyr,"seneschal_talk", [(check_quest_active, "qst_deliver_supply_to_center_under_siege"),
##                                  (quest_slot_eq, "qst_deliver_supply_to_center_under_siege", slot_quest_target_troop, "$g_talk_troop"),
##                                  (quest_slot_eq, "qst_deliver_supply_to_center_under_siege", slot_quest_current_state, 1),
##                                  (store_item_kind_count, ":no_supplies", "itm_siege_supply"),
##                                  (quest_get_slot, ":target_amount", "qst_deliver_supply_to_center_under_siege", slot_quest_target_amount),
##                                  (lt, ":no_supplies", ":target_amount"),
##                                  (gt, ":no_supplies", 0)],
##   "TODO: Here are the supplies, but some of them are missing.", "seneschal_supplies_given_missing",[]],
##
##  [anyone|plyr,"seneschal_talk", [(check_quest_active, "qst_deliver_supply_to_center_under_siege"),
##                                  (quest_slot_eq, "qst_deliver_supply_to_center_under_siege", slot_quest_object_troop, "$g_talk_troop"),
##                                  (quest_slot_eq, "qst_deliver_supply_to_center_under_siege", slot_quest_current_state, 0)],
##   "TODO: Give me the supplies.", "seneschal_supplies",[]],
##
##  [anyone,"seneschal_supplies", [(store_free_inventory_capacity, ":free_inventory"),
##                                 (quest_get_slot, ":quest_target_amount", "qst_deliver_supply_to_center_under_siege", slot_quest_target_amount),
##                                 (ge, ":free_inventory", ":quest_target_amount"),
##                                 (quest_get_slot, ":quest_target_center", "qst_deliver_supply_to_center_under_siege", slot_quest_target_center),
##                                 (str_store_party_name, 0, ":quest_target_center"),
##                                 (troop_add_items, "trp_player", "itm_siege_supply", ":quest_target_amount")],
##   "TODO: Here, take these supplies. You must deliver them to {s0} as soon as possible.", "seneschal_pretalk",[(quest_set_slot, "qst_deliver_supply_to_center_under_siege", slot_quest_current_state, 1)]],
##
##  [anyone,"seneschal_supplies", [],
##   "TODO: You don't have enough space to take the supplies. Free your inventory and return back to me.", "seneschal_pretalk",[]],
##
##
##  [anyone,"seneschal_supplies_given", [],
##   "TODO: Thank you.", "seneschal_pretalk",[(party_get_slot, ":town_siege_days", "$g_encountered_party", slot_town_siege_days),
##                                            (quest_get_slot, ":target_amount", "qst_deliver_supply_to_center_under_siege", slot_quest_target_amount),
##                                            (val_sub, ":town_siege_days", ":target_amount"),
##                                            (try_begin),
##                                              (lt, ":town_siege_days", 0),
##                                              (assign, ":town_siege_days", 0),
##                                            (try_end),
##                                            (party_set_slot, "$g_encountered_party", slot_town_siege_days, ":town_siege_days"),
##                                            (troop_remove_items, "trp_player", "itm_siege_supply", ":target_amount"),
##                                            (call_script, "script_finish_quest", "qst_deliver_supply_to_center_under_siege", 100)]],
##
##  [anyone,"seneschal_supplies_given_missing", [],
##   "TODO: Thank you but it's not enough...", "seneschal_pretalk",[(store_item_kind_count, ":no_supplies", "itm_siege_supply"),
##                                                                  (quest_get_slot, ":target_amount", "qst_deliver_supply_to_center_under_siege", slot_quest_target_amount),
##                                                                  (assign, ":percentage_completed", 100),
##                                                                  (val_mul, ":percentage_completed", ":no_supplies"),
##                                                                  (val_div, ":percentage_completed", ":target_amount"),
##                                                                  (call_script, "script_finish_quest", "qst_deliver_supply_to_center_under_siege", ":percentage_completed"),
##                                                                  (party_get_slot, ":town_siege_days", "$g_encountered_party", slot_town_siege_days),
##                                                                  (val_sub, ":town_siege_days", ":no_supplies"),
##                                                                  (try_begin),
##                                                                    (lt, ":town_siege_days", 0),
##                                                                    (assign, ":town_siege_days", 0),
##                                                                  (try_end),
##                                                                  (party_set_slot, "$g_encountered_party", slot_town_siege_days, ":town_siege_days"),
##                                                                  (troop_remove_items, "trp_player", "itm_siege_supply", ":no_supplies"),
##                                                                  (call_script, "script_end_quest", "qst_deliver_supply_to_center_under_siege")]],
##
##### TODO: QUESTS COMMENT OUT END

  [anyone|plyr,"seneschal_talk", [(store_relation, ":cur_rel", "fac_player_supporters_faction", "$g_encountered_party_faction"),
                                  (ge, ":cur_rel", 0),],
   "I would like to ask you a question...", "seneschal_ask_something",[]],
  [anyone|plyr,"seneschal_talk", [(store_relation, ":cur_rel", "fac_player_supporters_faction", "$g_encountered_party_faction"),
                                  (ge, ":cur_rel", 0),],
   "I wish to know more about someone...", "seneschal_ask_about_someone",[]],
  [anyone,"seneschal_ask_about_someone", [],
   "Perhaps I may be able to help. Whom did you have in mind?", "seneschal_ask_about_someone_2",[]],
#  [anyone|plyr|repeat_for_troops,"seneschal_ask_about_someone_2", [(store_repeat_object, ":troop_no"),
#                                                                 (is_between, ":troop_no", heroes_begin, heroes_end),
#                                                                  (store_troop_faction, ":faction_no", ":troop_no"),
 #                                                                 (eq, "$g_encountered_party_faction", ":faction_no"),
 #                                                                 (str_store_troop_name, s1, ":troop_no")],
 #  "{s1}", "seneschal_ask_about_someone_3",[(store_repeat_object, "$hero_requested_to_learn_relations")]],

  [anyone|plyr,"seneschal_ask_about_someone_2", [], "Never mind.", "seneschal_pretalk",[]],
#  [anyone, "seneschal_ask_about_someone_3", [(call_script, "script_troop_write_family_relations_to_s1", "$hero_requested_to_learn_relations"),
 #                                          (call_script, "script_troop_write_owned_centers_to_s2", "$hero_requested_to_learn_relations")
#										   ],
#   "{s2}{s1}", "seneschal_ask_about_someone_4",[(add_troop_note_from_dialog, "$hero_requested_to_learn_relations", 2)]],

#  [anyone, "seneschal_ask_about_someone_relation", [(call_script, "script_troop_count_number_of_enemy_troops", "$hero_requested_to_learn_relations"),
#                                            (assign, ":no_enemies", reg0),
#                                            (try_begin),
#                                              (gt, ":no_enemies", 1),
#                                              (try_for_range, ":i_enemy", 1, ":no_enemies"),
#                                                (store_add, ":slot_no", slot_troop_enemies_begin, ":i_enemy"),
#                                                (troop_get_slot, ":cur_enemy", "$hero_requested_to_learn_relations", ":slot_no"),
#                                                (str_store_troop_name_link, s50, ":cur_enemy"),
#                                                (try_begin),
#                                                  (eq, ":i_enemy", 1),
#                                                  (troop_get_slot, ":cur_enemy", "$hero_requested_to_learn_relations", slot_troop_enemy_1),
#                                                  (str_store_troop_name_link, s51, ":cur_enemy"),
#                                                  (str_store_string, s51, "str_s50_and_s51"),
#                                                (else_try),
#                                                  (str_store_string, s51, "str_s50_comma_s51"),
#                                                (try_end),
#                                              (try_end),
#                                            (else_try),
#                                              (eq, ":no_enemies", 1),
#                                              (troop_get_slot, ":cur_enemy", "$hero_requested_to_learn_relations", slot_troop_enemy_1),
#                                              (str_store_troop_name_link, s51, ":cur_enemy"),
#                                            (else_try),
#                                              (str_store_string, s51, "str_noone"),
#                                            (try_end),
#                                            (troop_get_type, reg1, "$hero_requested_to_learn_relations")],
#   "{reg1?She:He} hates {s51}.", "seneschal_ask_about_someone_4",[(add_troop_note_from_dialog, "$hero_requested_to_learn_relations", 3)]],
# Ryan END

#  [anyone|plyr,"seneschal_ask_about_someone_4", [], "Where does {s1} stand with others?.", "seneschal_ask_about_someone_relation",[]],
#  [anyone|plyr,"seneschal_ask_about_someone_4", [], "My thanks, that was helpful.", "seneschal_pretalk",[]],


  [anyone|plyr,"seneschal_talk", [], "I must take my leave of you now. Farewell.", "close_window",[]],
  [anyone,"seneschal_ask_something", [],
   "I'll do what I can to help, of course. What did you wish to ask?", "seneschal_ask_something_2",[]],
  [anyone|plyr,"seneschal_ask_something_2", [],
   "Perhaps you know where to find someone...", "seneschal_ask_location",[]],
  [anyone,"seneschal_ask_location", [],
   "Well, a man in my position does hear a lot of things. Of whom were you thinking?", "seneschal_ask_location_2",[]],
  [anyone|plyr|repeat_for_troops,"seneschal_ask_location_2", [(store_repeat_object, ":troop_no"),
                                                              (is_between, ":troop_no", heroes_begin, heroes_end),
                                                              (store_troop_faction, ":faction_no", ":troop_no"),
                                                              (eq, "$g_encountered_party_faction", ":faction_no"),
                                                              (str_store_troop_name, s1, ":troop_no")],
   "{s1}", "seneschal_ask_location_3",[(store_repeat_object, "$hero_requested_to_learn_location")]],
  [anyone|plyr,"seneschal_ask_location_2", [], "Never mind.", "seneschal_pretalk",[]],
  [anyone,"seneschal_ask_location_3", [(call_script, "script_get_information_about_troops_position", "$hero_requested_to_learn_location", 0)],
   "{s1}", "seneschal_pretalk",[]],
#caravan merchants
  [anyone,"start",
   [(eq, "$caravan_escort_state",1),
    (eq, "$g_encountered_party","$caravan_escort_party_id"),
    (le, "$talk_context",tc_party_encounter),
    (store_distance_to_party_from_party, reg0, "$caravan_escort_destination_town", "$caravan_escort_party_id"),
    (lt, reg0, 5),
    (str_store_party_name, s3, "$caravan_escort_destination_town"),
    (assign, reg3, "$caravan_escort_agreed_reward"),
    ],
   "There! I can see the walls of {s3} in the distance. We've made it safely.\
 Here, take this purse of {reg3} mon, as I promised. I hope we can travel together again someday.", "close_window",
   [
    (assign,"$caravan_escort_state",0),
    (call_script, "script_troop_add_gold", "trp_player", "$caravan_escort_agreed_reward"),
    (assign,reg(4), "$caravan_escort_agreed_reward"),
    (val_mul,reg(4), 1),
    (add_xp_as_reward,reg(4)),
    (assign, "$g_leave_encounter",1),
    ]],
  [anyone,"start",
   [(eq, "$caravan_escort_state", 1),
    (eq, "$g_encountered_party", "$caravan_escort_party_id"),
    (eq, "$talk_context", tc_party_encounter),
    ],
   "We've made it this far... Is everything clear up ahead?", "talk_caravan_escort",[]],
  [anyone|plyr,"talk_caravan_escort", [],
   "There might be bandits nearby. Stay close.", "talk_caravan_escort_2a",[]],
  [anyone,"talk_caravan_escort_2a", [],
   "Trust me, {playername}, we're already staying as close to you as we can. Lead the way.", "close_window",[(assign, "$g_leave_encounter",1)]],
  [anyone|plyr,"talk_caravan_escort", [],
   "No sign of trouble, we can breathe easy.", "talk_caravan_escort_2b",[]],
  [anyone,"talk_caravan_escort_2b", [],
   "I'll breathe easy when we reach {s1} and not a moment sooner. Let's keep moving.", "close_window",[[str_store_party_name,s1,"$caravan_escort_destination_town"],(assign, "$g_leave_encounter",1)]],
  [anyone,"start", [(eq,"$talk_context", tc_party_encounter),
                    (eq, "$g_encountered_party_type", spt_kingdom_caravan),
                    (party_slot_ge, "$g_encountered_party", slot_party_last_toll_paid_hours, "$g_current_hours"),
                    ],
   "What do you want? We paid our toll to you less than three days ago.", "merchant_talk",[]],
  [anyone,"start", [(eq,"$talk_context", tc_party_encounter),(eq, "$g_encountered_party_type", spt_kingdom_caravan),(ge,"$g_encountered_party_relation",0)],
   "Hail, friend.", "merchant_talk",[]],
  [anyone,"start", [(eq,"$talk_context", tc_party_encounter),
                    (eq, "$g_encountered_party_type", spt_kingdom_caravan),
                    (lt,"$g_encountered_party_relation",0),
                    (eq, "$g_encountered_party_faction", "fac_merchants"),
                    ],
   "What do you want? We are but simple merchants, we've no quarrel with you, so leave us alone.", "merchant_talk",[]],
  [anyone,"start", [(eq,"$talk_context", tc_party_encounter),
                    (eq, "$g_encountered_party_type", spt_kingdom_caravan),
                    (lt,"$g_encountered_party_relation",0),
                    (faction_get_slot, ":faction_leader", "$g_encountered_party_faction",slot_faction_leader),
                    (str_store_troop_name, s9, ":faction_leader"),
                    ],
   "This caravan is under the protection of {s9}!\
 Step out of our way or you will face his wrath!", "merchant_talk",[]],
  [anyone,"start", [(party_slot_eq, "$g_encountered_party", slot_party_type, spt_kingdom_caravan),(this_or_next|eq,"$talk_context", tc_party_encounter),(eq,"$talk_context", 0)],
   "Yes? What do you want?", "merchant_talk",[]],
  [anyone,"caravan_start_war_quest_1", [(quest_get_slot, ":giver_troop", "qst_cause_provocation", slot_quest_giver_troop),
								 (store_faction_of_troop, ":giver_troop_faction", ":giver_troop"),
                                 (str_store_faction_name, s17, ":giver_troop_faction"),
  ],
   "What? What nonsense is this? We are at peace with the {s17}, and are free to cross its lands!", "caravan_start_war_quest_2",[]],
  [anyone|plyr,"caravan_start_war_quest_2", [], "We'll see about that! Defend yourselves!", "merchant_attack",[]],
  [anyone|plyr,"caravan_start_war_quest_2", [], "Hmm. Maybe this was all a misunderstanding. Farewell.", "close_window",[(assign, "$g_leave_encounter",1)]],
  [anyone,"caravan_offer_protection", [],
   "These roads are dangerous indeed. One can never have enough protection.", "caravan_offer_protection_2",
   [(get_party_ai_object,":caravan_destination","$g_encountered_party"),
    (store_distance_to_party_from_party, "$caravan_distance_to_target",":caravan_destination","$g_encountered_party"),
    (assign,"$caravan_escort_offer","$caravan_distance_to_target"),
    (val_sub, "$caravan_escort_offer", 10),
    (call_script, "script_party_calculate_strength", "p_main_party", 0),
    (assign, ":player_strength", reg0),
    (val_min, ":player_strength", 200),
    (val_add, ":player_strength", 20),
    (val_mul,"$caravan_escort_offer",":player_strength"),
    (val_div,"$caravan_escort_offer",50),
    (val_max, "$caravan_escort_offer", 5),
    ]],
  [anyone,"caravan_offer_protection_2", [[lt,"$caravan_distance_to_target",10]],
   "An escort? We're almost there already! Thank you for the offer, though.", "close_window",[(assign, "$g_leave_encounter",1)]],
  [anyone,"caravan_offer_protection_2", [(get_party_ai_object,":caravan_destination","$g_encountered_party"),
    (str_store_party_name,1,":caravan_destination"),
    (assign,reg(2),"$caravan_escort_offer")],
   "We are heading to {s1}. I will pay you {reg2} mon if you escort us there.", "caravan_offer_protection_3",
   []],
  [anyone|plyr,"caravan_offer_protection_3", [],
   "Agreed.", "caravan_offer_protection_4",[]],
  [anyone,"caravan_offer_protection_4", [],
   "I want you to stay close to us along the way.\
 We'll need your help if we get ambushed by bandits.", "caravan_offer_protection_5",[]],
  [anyone|plyr,"caravan_offer_protection_5", [],
   "Don't worry, you can trust me.", "caravan_offer_protection_6",[]],
  [anyone,"caravan_offer_protection_6", [(get_party_ai_object,":caravan_destination","$g_encountered_party"),
    (str_store_party_name,1,":caravan_destination")],
   "Good. Come and collect your money when we're within sight of {s1}. For now, let's just get underway.", "close_window",
   [(get_party_ai_object,":caravan_destination","$g_encountered_party"),
    (assign, "$caravan_escort_destination_town", ":caravan_destination"),
    (assign, "$caravan_escort_party_id", "$g_encountered_party"),
    (assign, "$caravan_escort_agreed_reward", "$caravan_escort_offer"),
    (assign, "$caravan_escort_state", 1),
    (assign, "$g_leave_encounter",1)
   ]],
  [anyone|plyr,"caravan_offer_protection_3", [],
   "Forget it.", "caravan_offer_protection_4b",[]],
  [anyone,"caravan_offer_protection_4b", [],
   "Perhaps another time, then.", "close_window",[(assign, "$g_leave_encounter",1)]],
  [anyone,"talk_caravan_enemy_2", [],
   "Never. It is our duty to protect these goods. You shall have to fight us, brigand!", "close_window",
   [
    (store_relation,":rel","$g_encountered_party_faction","fac_player_supporters_faction"),
    (val_min,":rel",0),
    (val_sub,":rel",4),
    (call_script, "script_set_player_relation_with_faction", "$g_encountered_party_faction", ":rel"),
	(call_script, "script_diplomacy_party_attacks_neutral", "p_main_party", "$g_encountered_party"),
    ]],
# Prison Guards
  [anyone,"start", [(eq, "$talk_context", 0),(faction_slot_eq, "$g_encountered_party_faction", slot_faction_prison_guard_troop, "$g_talk_troop"),
					##diplomacy start+ Handle player is co-ruler of NPC kingdom
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
                    (this_or_next|eq, "$g_encountered_party_faction", "fac_player_supporters_faction"),
                    (             party_slot_eq, "$g_encountered_party", slot_town_lord, "trp_player"),
					##diplomacy start+
					#it may be appropriate to use "your highness" instead of "my {lord/lady}"
					(call_script, "script_dplmc_print_subordinate_says_sir_madame_to_s0"),#added
                    ],
   "Good day, {s0}. Will you be visiting the prison?", "prison_guard_players",[]],
#changed "my {lord/lady}" to "{s0}"
   ##diplomacy end+
  [anyone|plyr,"prison_guard_players", [],
   "Yes. Unlock the door.", "close_window",[(call_script, "script_enter_dungeon", "$current_town", "mt_visit_town_castle")]],
  [anyone|plyr,"prison_guard_players", [],
   "No, not now.", "close_window",[]],
  [anyone,"start", [(eq, "$talk_context", 0),(faction_slot_eq, "$g_encountered_party_faction", slot_faction_prison_guard_troop, "$g_talk_troop")],
   "Yes? What do you want?", "prison_guard_talk",[]],
  [anyone|plyr,"prison_guard_talk", [],
   "Who is imprisoned here?", "prison_guard_ask_prisoners",[]],
  [anyone|plyr,"prison_guard_talk", [],
   "I want to speak with a prisoner.", "prison_guard_visit_prison",[]],
##diplomacy begin
  [anyone|plyr,"prison_guard_talk", [
    (party_slot_eq, "$g_encountered_party", slot_town_lord, "trp_player"),
    ],
   "I want to release a prisoner.", "dplmc_prison_guard_talk_ask_prisoner",[]],
##diplomacy end
  [anyone,"prison_guard_ask_prisoners", [],
   "Currently, {s50} {reg1?are:is} imprisoned here.{s49}","prison_guard_talk",[
    (party_clear, "p_temp_party"),
	(party_clear, "p_temp_party_2"),
    (assign, ":num_heroes_in_dungeon", 0),
    (assign, ":num_heroes_given_parole", 0),

    (party_get_num_prisoner_stacks, ":num_stacks","$g_encountered_party"),
    (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_prisoner_stack_get_troop_id, ":stack_troop","$g_encountered_party",":i_stack"),
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
    (call_script, "script_print_party_members", "p_temp_party"),
	(str_store_string, s50, "str_s51"),
    (try_begin),
        (gt, ":num_heroes_in_dungeon", 1),
        (assign, reg1, 1),
    (else_try),
        (assign, reg1, 0),
    (try_end),

	(str_clear, s49),
    (try_begin),
        (ge, ":num_heroes_given_parole", 1),
		(call_script, "script_print_party_members", "p_temp_party_2"),
		(try_begin),
			(ge, ":num_heroes_given_parole", 2),
			(assign, reg2, 1),
		(else_try),
			(assign, reg2, 0),
		(try_end),
		(str_store_string, s49, "str__meanwhile_s51_reg2areis_being_held_in_the_castle_but_reg2havehas_made_pledges_not_to_escape_and_reg2areis_being_held_in_more_comfortable_quarters" ), #somewhat awkward wording prevents both gender and singular/plural pronoun issues
    (try_end)


	]],
  [anyone,"prison_guard_visit_prison",
  [
    (this_or_next|faction_slot_eq, "$g_encountered_party_faction", slot_faction_marshall, "trp_player"),
    (this_or_next|party_slot_eq, "$g_encountered_party", slot_town_lord, "trp_player"),
    (eq, "$g_encountered_party_faction", "$players_kingdom"),
  ],
   "Of course, {sir/madam}. Go in.", "close_window",
   [
     (call_script, "script_enter_dungeon", "$current_town", "mt_visit_town_castle")
   ]],
  [anyone, "prison_guard_visit_prison",
  [
    #below condition is added by ozan, please lets discuss if it is needed or not. But I think this condition is needed because if there is nobody in prison
    #prison guard should not say you need to get permission, or take me money ext to let player go inside.
    (assign, ":num_heroes_in_dungeon", 0),
    (party_get_num_prisoner_stacks, ":num_stacks", "$g_encountered_party"),
    (assign, ":end_condition", ":num_stacks"),
    (try_for_range, ":i_stack", 0, ":end_condition"),
      (party_prisoner_stack_get_troop_id, ":stack_troop","$g_encountered_party",":i_stack"),
      (troop_is_hero, ":stack_troop"),
      (try_begin),
        (call_script, "script_cf_prisoner_offered_parole", ":stack_troop"),
      (else_try),
        (val_add, ":num_heroes_in_dungeon", 1),
        (assign, ":end_condition", 0),
      (try_end),
    (try_end),

    (ge, ":num_heroes_in_dungeon", 1),
   ],
   "You need to get permission from the lord to talk to prisoners.", "prison_guard_visit_prison_2",[]],
  [anyone, "prison_guard_visit_prison", [], "There is nobody inside, therefore you can freely go inside and look around.", "prison_guard_visit_prison_nobody", []],
  [anyone|plyr,"prison_guard_visit_prison_nobody", [], "All right then. I'll take a look at the prison.", "close_window",
  [
    (call_script, "script_enter_dungeon", "$current_town", "mt_visit_town_castle"),
  ]],
  [anyone|plyr,"prison_guard_visit_prison_nobody", [], "I have more important business to do.", "close_window",[]],
  [anyone|plyr,"prison_guard_visit_prison_2", [], "All right then. I'll try that.", "close_window",[]],
  [anyone|plyr,"prison_guard_visit_prison_2", [], "Come on now. I thought you were the boss here.", "prison_guard_visit_prison_3",[]],
  [anyone,"prison_guard_visit_prison_3", [], "He-heh. You got that right. Still, I can't let you into the prison.", "prison_guard_visit_prison_4",[]],
  [anyone|plyr,"prison_guard_visit_prison_4", [], "All right then. I'll leave now.", "close_window",[]],
  [anyone|plyr,"prison_guard_visit_prison_4", [(store_troop_gold,":gold","trp_player"),(ge,":gold",100)],
   "I found a purse with 100 mon a few paces away. I reckon it belongs to you.", "prison_guard_visit_prison_5",[]],
  [anyone,"prison_guard_visit_prison_5", [], "Ah! I was looking for this all day. How good of you to bring it back {sir/madam}.\
 Well, now that I know what an honest {man/lady} you are, there can be no harm in letting you inside for a look. Go in.... Just so you know, though -- I'll be hanging onto the keys, in case you were thinking about undoing anyone's chains.", "close_window",
 [(troop_remove_gold, "trp_player",100),(call_script, "script_enter_dungeon", "$current_town", "mt_visit_town_castle")]],
  [anyone|plyr,"prison_guard_visit_prison_4", [],
   "Give me the keys to the cells -- now!", "prison_guard_visit_break",[
   ]],
  [anyone,"prison_guard_visit_break", [], "Help! Help! Prison break!", "close_window",[
  (call_script, "script_activate_town_guard"),
  (assign, "$g_main_attacker_agent", "$g_talk_agent"),
  (assign, "$talk_context", tc_prison_break),
#  (try_begin),
#		(store_relation, ":relation", "fac_player_faction", "$g_encountered_party_faction"),
#	Reduce relation with town
# (try_end),

	 (assign, ":end_cond", kingdom_ladies_end),
     (try_for_range, ":prisoner", active_npcs_begin, ":end_cond"),
	   (troop_set_slot, ":prisoner", slot_troop_mission_participation, 0), #new
	 (try_end),
  ]],
  [anyone|plyr,"prison_guard_talk", [],
   "Never mind.", "close_window",[]],
# Castle Guards
  [anyone,"start", [(eq, "$talk_context", 0),(faction_slot_eq, "$g_encountered_party_faction", slot_faction_castle_guard_troop, "$g_talk_troop"),
  					##diplomacy start+ Handle player is co-ruler of NPC kingdom
					(assign, ":is_coruler", 0),
					(try_begin),
						(eq, "$g_encountered_party_faction", "$players_kingdom"),
						(is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
						(call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", "$players_kingdom"),
						(ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
						(assign, ":is_coruler", 1),#ruler or co-ruler of faction
					(try_end),
					(this_or_next|eq, ":is_coruler", 1),
					##diplomacy end+
                    (this_or_next|eq, "$g_encountered_party_faction", "fac_player_supporters_faction"),
                    (             party_slot_eq, "$g_encountered_party", slot_town_lord, "trp_player")
                    ],
   "Your orders, {Lord/Lady}?", "castle_guard_players",[]],
  [anyone|plyr,"castle_guard_players", [],
   "Open the door. I'll go in.", "close_window",[(call_script, "script_enter_court", "$current_town")]],
  [anyone|plyr,"castle_guard_players", [],
   "Never mind.", "close_window",[]],
  [anyone,"start", [(eq, "$talk_context", 0),(faction_slot_eq, "$g_encountered_party_faction", slot_faction_castle_guard_troop, "$g_talk_troop"),(eq, "$sneaked_into_town",1),
                    (gt,"$g_time_since_last_talk",0)],
   "Get out of my sight, beggar! You stink!", "castle_guard_sneaked_intro_1",[]],
  [anyone,"start", [(eq, "$talk_context", 0),(faction_slot_eq, "$g_encountered_party_faction", slot_faction_castle_guard_troop, "$g_talk_troop"),(eq, "$sneaked_into_town",1)],
   "Get lost before I lose my temper you vile beggar!", "close_window",[]],
  [anyone|plyr,"castle_guard_sneaked_intro_1", [], "I want to enter the hall and speak to the lord.", "castle_guard_sneaked_intro_2",[]],
  [anyone|plyr,"castle_guard_sneaked_intro_1", [], "[Leave]", "close_window",[]],
  [anyone,"castle_guard_sneaked_intro_2", [], "Are you out of your mind, {man/woman}?\
 Beggars are not allowed into the hall. Now get lost or I'll beat you bloody.", "close_window",[]],
  [anyone,"start", [(eq, "$talk_context", 0),(faction_slot_eq, "$g_encountered_party_faction", slot_faction_castle_guard_troop, "$g_talk_troop")],
   "What do you want?", "castle_guard_intro_1",[]],
  [anyone|plyr,"castle_guard_intro_1", [],
   "I want to enter the hall and speak to the lord.", "castle_guard_intro_2",[]],
  [anyone|plyr,"castle_guard_intro_1", [],
   "Never mind.", "close_window",[]],
   [anyone,"castle_guard_intro_2", [
	(faction_slot_eq, "$g_encountered_party_faction", slot_faction_ai_state, sfai_feast),
	(faction_slot_eq, "$g_encountered_party_faction", slot_faction_ai_object, "$current_town"),

	(this_or_next|neq, "$players_kingdom", "$g_encountered_party_faction"),
		(neg|troop_slot_ge, "trp_player", slot_troop_renown, 50),

	(neg|troop_slot_ge, "trp_player", slot_troop_renown, 125),
	(neq, "$g_player_eligible_feast_center_no", "$current_town"),

	(neg|check_quest_active, "qst_wed_betrothed"),
	(neg|check_quest_active, "qst_wed_betrothed_female"),

	(neg|troop_slot_ge, "trp_player", slot_troop_spouse, 1), #Married players always make the cut

   ], "I'm afraid there is a feast in progress, and you are not invited.", "close_window",
   []],
   [anyone,"castle_guard_intro_2", [], "You can go in after leaving your weapons with me. No one is allowed to carry arms into the lord's hall.", "castle_guard_intro_3",
   []],
  [anyone|plyr,"castle_guard_intro_3", [], "Here, take my arms. I'll go in.", "close_window", [(call_script, "script_enter_court", "$current_town")]],
  [anyone|plyr,"castle_guard_intro_3", [], "No, I give my arms to no one.", "castle_guard_intro_2b", []],
  [anyone,"castle_guard_intro_2b", [], "Then you can't go in.", "close_window", []],
##  [anyone|plyr,"castle_guard_intro_1", [],
##   "Never mind.", "close_window",[]],
##  [anyone,"castle_guard_intro_2", [],
##   "Does the lord expect you?", "castle_guard_intro_3",[]],
##  [anyone|plyr,"castle_guard_intro_3", [], "Yes.", "castle_guard_intro_check",[]],
##  [anyone|plyr,"castle_guard_intro_3", [], "No.", "castle_guard_intro_no",[]],
##  [anyone,"castle_guard_intro_check", [], "Hmm. All right {sir/madam}.\
## You can go in. But you must leave your weapons with me. Noone's allowed into the court with weapons.", "close_window",[]],
##  [anyone,"castle_guard_intro_check", [], "You liar!\
## Our lord would have no business with a filthy vagabond like you. Get lost now before I kick your butt.", "close_window",[]],
##  [anyone,"castle_guard_intro_no", [], "Well... What business do you have here then?", "castle_guard_intro_4",[]],
##  [anyone|plyr,"castle_guard_intro_4", [], "I wish to present the lord some gifts.", "castle_guard_intro_gifts",[]],
##  [anyone|plyr,"castle_guard_intro_4", [], "I have an important matter to discuss with the lord. Make way now.", "castle_guard_intro_check",[]],
##  [anyone,"castle_guard_intro_gifts", [], "Really? What gifts?", "castle_guard_intro_5",[]],
##  [anyone|plyr,"castle_guard_intro_4", [], "Many gifts. For example, I have a gift of 20 mon here for his loyal servants.", "castle_guard_intro_gifts",[]],
##  [anyone|plyr,"castle_guard_intro_4", [], "My gifts are of no concern to you. They are for your lords and ladies..", "castle_guard_intro_check",[]],
##  [anyone,"castle_guard_intro_gifts", [], "Oh! you can give those 20 mon to me. I can distribute them for you.\
## You can enter the court and present your gifts to the lord. I'm sure he'll be pleased.\
## But you must leave your weapons with me. Noone's allowed into the court with weapons.", "close_window",[]],

#Kingdom Parties
#  [anyone,"start", [(this_or_next|eq,"$g_encountered_party_template","pt_swadian_foragers"),
#                    (eq,"$g_encountered_party_template","pt_vaegir_foragers"),
##  [anyone,"start", [(this_or_next|party_slot_eq,"$g_encountered_party",slot_party_type, spt_forager),
##                    (this_or_next|party_slot_eq,"$g_encountered_party",slot_party_type, spt_scout),
##                    (party_slot_eq,"$g_encountered_party",slot_party_type, spt_patrol),
##                    (str_store_faction_name,5,"$g_encountered_party_faction")],
##   "In the name of the {s5}.", "kingdom_party_encounter",[]],
##
##  [anyone,"kingdom_party_encounter", [(le,"$g_encountered_party_relation",-10)],
##   "Surrender now, and save yourself the indignity of defeat!", "kingdom_party_encounter_war",[]],
##  [anyone|plyr,"kingdom_party_encounter_war", [],  "[Go to Battle]", "close_window",[(encounter_attack)]],
##
##  [anyone,"kingdom_party_encounter", [(ge,"$g_encountered_party_relation",10)],
##   "Greetings, fellow warrior.", "close_window",[(eq,"$talk_context",tc_party_encounter),(assign, "$g_leave_encounter", 1)]],
##
##  [anyone,"kingdom_party_encounter", [],
##   "You can go.", "close_window",[]],








#Player Parties
##  [party_tpl|pt_old_garrison,"start", [],
##   "They told us to leave the castle to the new garrison {sir/madam}. So we left and came to rejoin you.", "player_old_garrison_encounter",[]],
##
##  [anyone|plyr,"player_old_garrison_encounter", [(party_can_join)],
##   "You have done well. You'll join my command now.", "close_window",[(assign, "$g_move_heroes", 1),
##                                        (call_script, "script_party_add_party", "p_main_party", "$g_encountered_party"),
##                                        (remove_party, "$g_encountered_party"),
##                                        (assign, "$g_leave_encounter", 1)]],
##  [anyone|plyr,"player_old_garrison_encounter", [(assign, reg1, 0),
##                                                 (try_begin),
##                                                   (neg|party_can_join),
##                                                   (assign, reg1, 1),
##                                                 (try_end)],
##   "You can't join us now{reg1?, I can't command all the lot of you:}. Follow our lead.", "close_window",[(party_set_ai_behavior, "$g_encountered_party", ai_bhvr_attack_party),
##                                                                         (party_set_ai_object, "$g_encountered_party", "p_main_party"),
##                                                                         (party_set_flags, "$g_encountered_party", pf_default_behavior, 0),
##                                                                         (assign, "$g_leave_encounter", 1)]],
##
##  [anyone|plyr,"player_old_garrison_encounter", [(assign, reg1, 0),
##                                                 (try_begin),
##                                                   (neg|party_can_join),
##                                                   (assign, reg1, 1),
##                                                 (try_end)],
##   "You can't join us now{reg1?, I can't command all the lot of you:}. Stay here and wait for me.", "close_window",[
##       (party_set_ai_behavior, "$g_encountered_party", ai_bhvr_travel_to_point),
##       (party_get_position, pos1, "$g_encountered_party"),
##       (party_set_ai_target_position, "$g_encountered_party", pos1),
##       (party_set_flags, "$g_encountered_party", pf_default_behavior, 0),
##       (assign, "$g_leave_encounter", 1)]],
##






  [anyone,"start", [(eq, "$talk_context", tc_castle_gate)],
   "What do you want?", "castle_gate_guard_talk",[]],
  [anyone,"castle_gate_guard_pretalk", [],
   "Yes?", "castle_gate_guard_talk",[]],
  [anyone|plyr,"castle_gate_guard_talk", [(ge, "$g_encountered_party_relation", 0)],
  "We need shelter for the night. Will you let us in?", "castle_gate_open",[]],
  [anyone|plyr,"castle_gate_guard_talk", [(party_slot_ge, "$g_encountered_party", slot_town_lord, 1)], "I want to speak with the lord of the castle.", "request_meeting_castle_lord",[]],
  [anyone|plyr,"castle_gate_guard_talk", [], "I want to speak with someone in the castle.", "request_meeting_other",[]],
  [anyone|plyr,"castle_gate_guard_talk", [], "[Leave]", "close_window",[]],
  [anyone,"request_meeting_castle_lord", [(party_get_slot, ":castle_lord", "$g_encountered_party", slot_town_lord),
                                         (call_script, "script_get_troop_attached_party", ":castle_lord"),
                                         (eq, "$g_encountered_party", reg0),
                                         (str_store_troop_name, s2, ":castle_lord"),
                                         (assign, "$lord_requested_to_talk_to", ":castle_lord"),
                                          ],  "Wait here. {s2} will see you.", "close_window",[]],
  [anyone,"request_meeting_castle_lord", [],  "My lord is not here now.", "castle_gate_guard_pretalk",[]],
  [anyone,"request_meeting_other", [],  "Who is that?", "request_meeting_3",[]],
  [anyone|plyr|repeat_for_troops,"request_meeting_3", [(store_repeat_object, ":troop_no"),
                                                       (troop_is_hero, ":troop_no"),
                                                       (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
                                                       (call_script, "script_get_troop_attached_party", ":troop_no"),
                                                       (eq, "$g_encountered_party", reg0),
                                                       (str_store_troop_name, s3, ":troop_no"),
                                                       ],
   "{s3}", "request_meeting_4",[(store_repeat_object, "$lord_requested_to_talk_to")]],
  [anyone|plyr,"request_meeting_3", [], "Never mind.", "close_window",[(assign, "$lord_requested_to_talk_to", 0)]],
  [anyone,"request_meeting_4", [##diplomacy start+ correct pronoun
  (call_script, "script_dplmc_store_troop_is_female",  "$lord_requested_to_talk_to"),
], "Wait there. I'll send {reg0?her:him} your request.", "request_meeting_5",[]],
#"him" to "{reg0?her:him}"
##diplomacy end+

  [anyone|plyr,"request_meeting_5", [], "I'm waiting...", "request_meeting_6",[]],
  [anyone,"request_meeting_6",
   [
     (call_script, "script_troop_get_player_relation", "$lord_requested_to_talk_to"),
     (assign, ":lord_relation", reg0),
     (gt, ":lord_relation", -20),
    ], "All right. {s2} will talk to you now.", "close_window",[(str_store_troop_name, s2, "$lord_requested_to_talk_to")]],
  [anyone,"request_meeting_6", [(str_store_troop_name, s2, "$lord_requested_to_talk_to"),
  ##diplomacy start+ correct pronoun
  (call_script, "script_dplmc_store_troop_is_female",  "$lord_requested_to_talk_to"),
  ], "{s2} says {reg0?she:he} will not see you. Begone now.", "close_window",[]],
#"he" to "{reg0?she:he}"
  ##diplomacy end+

  [anyone,"castle_gate_open", [(party_get_slot, ":castle_lord", "$g_encountered_party", slot_town_lord),
                                         (call_script, "script_get_troop_attached_party", ":castle_lord"),
                                         (eq, "$g_encountered_party", reg0),
                                         (ge, "$g_encountered_party_relation", 0),
                                         (call_script, "script_troop_get_player_relation", ":castle_lord"),
                                         (assign, ":castle_lord_relation", reg0),
                                         #(troop_get_slot, ":castle_lord_relation", ":castle_lord", slot_troop_player_relation),
                                         (ge, ":castle_lord_relation", 5),
                                         (str_store_troop_name, s2, ":castle_lord")
                                         ],  "My lord {s2} will be happy to see you {sir/madam}.\
 Come on in. I am opening the gates for you.", "close_window",[(assign,"$g_permitted_to_center",1)]],
  [anyone,"castle_gate_open", [(party_get_slot, ":castle_lord", "$g_encountered_party", slot_town_lord),
                                         (call_script, "script_get_troop_attached_party", ":castle_lord"),
                                         (neq, "$g_encountered_party", reg0),
                                         (ge, "$g_encountered_party_relation", 0),
                                         (call_script, "script_troop_get_player_relation", ":castle_lord"),
                                         (assign, ":castle_lord_relation", reg0),
                                         #(troop_get_slot, ":castle_lord_relation", ":castle_lord", slot_troop_player_relation),
                                         (ge, ":castle_lord_relation", 5),
                                         (str_store_troop_name, s2, ":castle_lord")
                                         ],  "My lord {s2} is not in the castle now.\
 But I think he would approve of you taking shelter here.\
 Come on in. I am opening the gates for you.", "close_window",[(assign,"$g_permitted_to_center",1)]],
  [anyone,"castle_gate_open", [(party_get_slot, ":castle_lord", "$g_encountered_party", slot_town_lord),
                               (call_script, "script_troop_get_player_relation", ":castle_lord"),
                               (assign, ":castle_lord_relation", reg0),
                               #(troop_get_slot, ":castle_lord_relation", ":castle_lord", slot_troop_player_relation),
                               (ge, ":castle_lord_relation", -2),
                                         ],  "Come on in. I am opening the gates for you.", "close_window",[(assign,"$g_permitted_to_center",1)]],
  [anyone,"castle_gate_open", [(party_get_slot, ":castle_lord", "$g_encountered_party", slot_town_lord),
                               (call_script, "script_troop_get_player_relation", ":castle_lord"),
                               (assign, ":castle_lord_relation", reg0),
                               #(troop_get_slot, ":castle_lord_relation", ":castle_lord", slot_troop_player_relation),
                               (ge, ":castle_lord_relation", -19),
                               (str_store_troop_name, s2, ":castle_lord")
                                         ],  "Come on in. But make sure your men behave sensibly within the walls.\
 My lord {s2} does not want trouble here.", "close_window",[(assign,"$g_permitted_to_center",1)]],
  [anyone,"castle_gate_open", [(party_get_slot, ":castle_lord", "$g_encountered_party", slot_town_lord),
                               (str_store_troop_name, s2, ":castle_lord"),
  ],  "My lord {s2} does not want you here. Begone now.", "close_window",[]],
#Enemy Kingdom Meetings


#  [anyone,"start", [(eq, "$talk_context", tc_lord_talk_in_center)],
#   "Greetings {playername}.", "request_meeting_1",[]],

#  [anyone,"request_meeting_pretalk", [(eq, "$talk_context", tc_lord_talk_in_center)],
#   "Yes?", "request_meeting_1",[]],

#  [anyone|plyr,"request_meeting_1", [(ge, "$g_encountered_party_faction", 0)], "Open the gates and let me in!", "request_meeting_open_gates",[]],

#  [anyone|plyr,"request_meeting_1", [(party_slot_ge, "$g_encountered_party", slot_town_lord, 1)], "I want to speak with the lord of the castle.", "request_meeting_castle_lord",[]],
#  [anyone|plyr,"request_meeting_1", [], "I want to speak with someone in the castle.", "request_meeting_other",[]],

##### TODO: QUESTS COMMENT OUT BEGIN
##  [anyone|plyr,"request_meeting_1",[(check_quest_active,"qst_bring_prisoners_to_enemy"),
##                                    (neg|check_quest_succeeded, "qst_bring_prisoners_to_enemy"),
##                                    (quest_get_slot, ":quest_giver_troop", "qst_bring_prisoners_to_enemy", slot_quest_giver_troop),
##                                    (quest_get_slot, ":quest_target_amount", "qst_bring_prisoners_to_enemy", slot_quest_target_amount),
##                                    (quest_get_slot, ":quest_object_troop", "qst_bring_prisoners_to_enemy", slot_quest_object_troop),
##                                    (quest_slot_eq, "qst_bring_prisoners_to_enemy", slot_quest_target_center, "$g_encountered_party"),
##                                    (party_count_prisoners_of_type, ":num_prisoners", "p_main_party", ":quest_object_troop"),
##                                    (ge, ":num_prisoners", ":quest_target_amount"),
##                                    (str_store_troop_name,1,":quest_giver_troop"),
##                                    (assign, reg1, ":quest_target_amount"),
##                                    (str_store_troop_name_plural,2,":quest_object_troop")],
##   "TODO: Sir, lord {s1} ordered me to bring {reg1} {s2} for ransom.", "guard_prisoners_brought",
##   [(quest_get_slot, ":quest_target_amount", "qst_bring_prisoners_to_enemy", slot_quest_target_amount),
##    (quest_get_slot, ":quest_target_center", "qst_bring_prisoners_to_enemy", slot_quest_target_center),
##    (quest_get_slot, ":quest_object_troop", "qst_bring_prisoners_to_enemy", slot_quest_object_troop),
##    (party_remove_prisoners, "p_main_party", ":quest_object_troop", ":quest_target_amount"),
##    (party_add_members, ":quest_target_center", ":quest_object_troop", ":quest_target_amount"),
##    (call_script, "script_game_get_join_cost", ":quest_object_troop"),
##    (assign, ":reward", reg0),
##    (val_mul, ":reward", ":quest_target_amount"),
##    (val_div, ":reward", 2),
##    (call_script, "script_troop_add_gold", "trp_player", ":reward"),
##    (party_get_slot, ":cur_lord", "$g_encountered_party", slot_town_lord),#Removing gold from the town owner's wealth
##    (troop_get_slot, ":cur_wealth", ":cur_lord", slot_troop_wealth),
##    (val_sub, ":cur_wealth", ":reward"),
##    (troop_set_slot, ":cur_lord", slot_troop_wealth, ":cur_wealth"),
##    (quest_set_slot, "qst_bring_prisoners_to_enemy", slot_quest_target_amount, ":reward"),
##    (succeed_quest, "qst_bring_prisoners_to_enemy"),
##    ]],
##
##  [anyone|plyr,"request_meeting_1",[(check_quest_active,"qst_bring_prisoners_to_enemy"),
##                                    (neg|check_quest_succeeded, "qst_bring_prisoners_to_enemy"),
##                                    (quest_get_slot, ":quest_giver_troop", "qst_bring_prisoners_to_enemy", slot_quest_giver_troop),
##                                    (quest_get_slot, ":quest_target_amount", "qst_bring_prisoners_to_enemy", slot_quest_target_amount),
##                                    (quest_get_slot, ":quest_object_troop", "qst_bring_prisoners_to_enemy", slot_quest_object_troop),
##                                    (quest_slot_eq, "qst_bring_prisoners_to_enemy", slot_quest_target_center, "$g_encountered_party"),
##                                    (party_count_prisoners_of_type, ":num_prisoners", "p_main_party", ":quest_object_troop"),
##                                    (lt, ":num_prisoners", ":quest_target_amount"),
##                                    (gt, ":num_prisoners", 0),
##                                    (str_store_troop_name,1,":quest_giver_troop"),
##                                    (assign, reg1, ":quest_target_amount"),
##                                    (str_store_troop_name_plural,2,":quest_object_troop")],
##   "TODO: Sir, lord {s1} ordered me to bring {reg1} {s2} for ransom, but some of them died during my expedition.", "guard_prisoners_brought_some",
##   [(quest_get_slot, ":quest_target_amount", "qst_bring_prisoners_to_enemy", slot_quest_target_amount),
##    (quest_get_slot, ":quest_target_center", "qst_bring_prisoners_to_enemy", slot_quest_target_center),
##    (quest_get_slot, ":quest_object_troop", "qst_bring_prisoners_to_enemy", slot_quest_object_troop),
##    (party_count_prisoners_of_type, ":num_prisoners", "p_main_party", ":quest_object_troop"),
##    (party_remove_prisoners, "p_main_party", ":quest_object_troop", ":num_prisoners"),
##    (party_add_members, ":quest_target_center", ":quest_object_troop", ":num_prisoners"),
##    (call_script, "script_game_get_join_cost", ":quest_object_troop"),
##    (assign, ":reward", reg0),
##    (val_mul, ":reward", ":num_prisoners"),
##    (val_div, ":reward", 2),
##    (call_script, "script_troop_add_gold", "trp_player", ":reward"),
##    (party_get_slot, ":cur_lord", "$g_encountered_party", slot_town_lord),#Removing gold from the town owner's wealth
##    (troop_get_slot, ":cur_wealth", ":cur_lord", slot_troop_wealth),
##    (val_sub, ":cur_wealth", ":reward"),
##    (troop_set_slot, ":cur_lord", slot_troop_wealth, ":cur_wealth"),
##    (call_script, "script_game_get_join_cost", ":quest_object_troop"),
##    (assign, ":reward", reg0),
##    (val_mul, ":reward", ":quest_target_amount"),
##    (val_div, ":reward", 2),
##    (quest_set_slot, "qst_bring_prisoners_to_enemy", slot_quest_current_state, 1),#Some of the prisoners are given, so it's state will change for remembering that.
##    (quest_set_slot, "qst_bring_prisoners_to_enemy", slot_quest_target_amount, ":reward"),#Still needs to pay the lord the full price of the prisoners
##    (succeed_quest, "qst_bring_prisoners_to_enemy"),
##    ]],
##
##
##  [anyone,"guard_prisoners_brought", [],
##   "TODO: Thank you. Here is the money for prisoners.", "request_meeting_pretalk",[]],
##
##  [anyone,"guard_prisoners_brought_some", [],
##   "TODO: Thank you, but that's not enough. Here is the money for prisoners.", "request_meeting_pretalk",[]],

#  [anyone|plyr,"request_meeting_1", [], "[Leave]", "close_window",[]],





##  [anyone,"request_meeting_open_gates", [(party_get_slot, ":castle_lord", "$g_encountered_party", slot_town_lord),
##                                         (call_script, "script_get_troop_attached_party", ":castle_lord"),
##                                         (eq, "$g_encountered_party", reg0),
##                                         (str_store_troop_name, 1, ":castle_lord")
##                                         ],  "My lord {s1} is in the castle now. You must ask his permission to enter.", "request_meeting_pretalk",[]],
##
##  [anyone,"request_meeting_open_gates", [(party_get_slot, ":castle_lord", "$g_encountered_party", slot_town_lord),
##                                         (call_script, "script_get_troop_attached_party", ":castle_lord"),
##                                         (neq, "$g_encountered_party", reg0),
##                                         (ge, "$g_encountered_party_relation", 0),
##                                         (troop_get_slot, ":castle_lord_relation", ":castle_lord", slot_troop_player_relation),
##                                         (ge, ":castle_lord_relation", 20),
##                                         (str_store_troop_name, 1, ":castle_lord")
##                                         ],  "My lord {s1} is not in the castle now.\
## But I think he would approve of you taking shelter here, {sir/madam}.\
## Come on in. I am opening the gates for you.", "close_window",[]],
##
##  [anyone,"request_meeting_open_gates", [(party_get_slot, ":castle_lord", "$g_encountered_party", slot_town_lord),(str_store_troop_name, 1, ":castle_lord")],
##   "My lord {s1} is not in the castle now. I can't allow you into the castle without his orders.", "request_meeting_pretalk",[]],




# Quest conversations

##### TODO: QUESTS COMMENT OUT BEGIN

##  [party_tpl|pt_shinano_rebels,"start", [],
##   "TODO: What.", "peasant_rebel_talk",[]],
##  [anyone|plyr, "peasant_rebel_talk", [], "TODO: Die.", "close_window",[]],
##  [anyone|plyr, "peasant_rebel_talk", [], "TODO: Nothing.", "close_window",[(assign, "$g_leave_encounter",1)]],
##
##  [party_tpl|pt_noble_refugees,"start", [],
##   "TODO: What.", "noble_refugee_talk",[]],
##  [anyone|plyr, "noble_refugee_talk", [], "TODO: Nothing.", "close_window",[(assign, "$g_leave_encounter",1)]],
##


  [anyone,"start", [(eq,"$talk_context",tc_join_battle_ally),
                    ],
   "You have come just in time. Let us join our forces now and teach our enemy a lesson.", "close_window",
   []],
  [anyone,"start", [(eq,"$talk_context",tc_join_battle_enemy),
                    ],
   "You are making a big mistake by fighting against us.", "close_window",
   []],
  [anyone,"start", [(eq,"$talk_context",tc_ally_thanks),
                    (troop_is_hero, "$g_talk_troop"),
                    (eq, "$g_talk_troop_met", 0),
                    (ge, "$g_talk_troop_relation", 17),
                    ],
   "I don't think we have met properly my friend. You just saved my life out there, and I still don't know your name...", "ally_thanks_meet", []],
  [anyone,"start", [(eq,"$talk_context",tc_ally_thanks),
                    (troop_is_hero, "$g_talk_troop"),
                    (eq, "$g_talk_troop_met", 0),
                    (ge, "$g_talk_troop_relation", 5),
					(str_store_troop_name, s1, "$g_talk_troop"),
                    ],
   "Your help was most welcome stranger. My name is {s1}. Can I learn yours?", "ally_thanks_meet", []],
  [anyone,"start", [(eq,"$talk_context",tc_ally_thanks),
                    (troop_is_hero, "$g_talk_troop"),
                    (eq, "$g_talk_troop_met", 0),
                    (ge, "$g_talk_troop_relation", 0),
                    (str_store_troop_name, s1, "$g_talk_troop"),
                    ],
   "Thanks for your help, stranger. We haven't met properly yet, have we? What is your name?", "ally_thanks_meet", []],
#Post 0907 changes begin
  [anyone,"start", [(eq,"$talk_context",tc_ally_thanks),
                    (troop_is_hero, "$g_talk_troop"),
                    (ge, "$g_talk_troop_relation", 30),
                    (ge, "$g_relation_boost", 10),
                    ],
   "Again you save our necks, {playername}! Truly, you are the best of friends. {s43}", "close_window", [
       (call_script, "script_lord_comment_to_s43", "$g_talk_troop", "str_battle_won_default"),
       (try_begin),
         (party_stack_get_troop_id, ":enemy_party_leader", "p_encountered_party_backup", 0),
         (is_between, ":enemy_party_leader", active_npcs_begin, active_npcs_end),
         (call_script, "script_add_log_entry", logent_lord_helped_by_player, "trp_player",  -1, ":enemy_party_leader", -1),
       (try_end),
       ]],
  [anyone,"start", [(eq,"$talk_context",tc_ally_thanks),
                    (troop_is_hero, "$g_talk_troop"),
                    (ge, "$g_talk_troop_relation", 20),
                    (ge, "$g_relation_boost", 5),
                    ],
   "You arrived just in the nick of time! {playername}. You have my deepest thanks! {s43}", "close_window", [
       (call_script, "script_lord_comment_to_s43", "$g_talk_troop", "str_battle_won_default"),
#       (try_begin),
#         (party_stack_get_troop_id, ":enemy_party_leader", "p_encountered_party_backup", 0),
#         (is_between, ":enemy_party_leader", active_npcs_begin, active_npcs_end),
       (call_script, "script_add_log_entry", logent_lord_helped_by_player, "trp_player",  -1, "$g_talk_troop", -1),
#       (try_end),
       ]],
  [anyone,"start", [(eq,"$talk_context",tc_ally_thanks),
                    (troop_is_hero, "$g_talk_troop"),
                    (ge, "$g_talk_troop_relation", 0),
                    (ge, "$g_relation_boost", 3),
                    ],
   "You turned up just in time, {playername}. I will not forget your help. {s43}", "close_window", [
       (call_script, "script_lord_comment_to_s43", "$g_talk_troop", "str_battle_won_default"),
#       (try_begin),
#         (party_stack_get_troop_id, ":enemy_party_leader", "p_encountered_party_backup", 0),
#         (is_between, ":enemy_party_leader", active_npcs_begin, active_npcs_end),
       (call_script, "script_add_log_entry", logent_lord_helped_by_player, "trp_player",  -1, "$g_talk_troop", -1),
#       (try_end),
       ]],
  [anyone,"start", [(eq,"$talk_context",tc_ally_thanks),
                    (troop_is_hero, "$g_talk_troop"),
                    (ge, "$g_talk_troop_relation", -5),
                    ],
   "Good to see you here, {playername}. {s43}", "close_window", [
                    (call_script, "script_lord_comment_to_s43", "$g_talk_troop", "str_battle_won_default"),
					(call_script, "script_troop_change_relation_with_troop", "$g_talk_troop", "trp_player", 1),
       ]],
  [anyone,"start", [(eq,"$talk_context",tc_ally_thanks),
                    (troop_is_hero, "$g_talk_troop"),
                    (ge, "$g_relation_boost", 4),
                    ],
   "{s43}", "close_window", [
                    (call_script, "script_lord_comment_to_s43", "$g_talk_troop", "str_battle_won_grudging_default"),
                    ]],
  [anyone,"start", [(eq,"$talk_context",tc_ally_thanks),
                    (troop_is_hero, "$g_talk_troop"),
                    ],
   "{s43}", "close_window", [
                    (call_script, "script_lord_comment_to_s43", "$g_talk_troop", "str_battle_won_unfriendly_default"),
                    ]],
#  [anyone,"start", [(eq,"$talk_context",tc_ally_thanks),
#                    (troop_is_hero, "$g_talk_troop"),
#                    (ge, "$g_talk_troop_relation", -20),
#                    ],
#   "So, this is {playername}. Well, your help wasn't really needed, but I guess you had nothing better to do, right?", "close_window", []],

#  [anyone,"start", [(eq,"$talk_context",tc_ally_thanks),
#                    (troop_is_hero, "$g_talk_troop"),
#                    ],
#   "Who told you to come to our help? I certainly didn't. Begone now. I want nothing from you and I will not let you steal my victory.", "close_window", []],

#Post 0907 changes begin

  [anyone,"start", [(eq,"$talk_context",tc_ally_thanks),
                    (ge, "$g_relation_boost", 10),
                    (party_get_num_companions, reg1, "$g_encountered_party"),
                    (val_sub, reg1, 1),
                    ],
   "Thank you for your help {sir/madam}. You saved {reg1?our lives:my life} out there.", "close_window", []],
  [anyone,"start", [(eq,"$talk_context",tc_ally_thanks),
                    (ge, "$g_relation_boost", 5),
                    ],
   "Thank you for your help {sir/madam}. Things didn't look very well for us but then you came up and everything changed.", "close_window", []],
  [anyone,"start", [(eq,"$talk_context",tc_ally_thanks)],
   "Thank you for your help, {sir/madam}. It was fortunate to have you nearby.", "close_window", []],
  [anyone,"start", [(eq, "$talk_context", tc_hero_freed),
                    (store_conversation_troop,":cur_troop"),
                    (eq,":cur_troop","trp_kidnapped_girl"),],
   "Oh {sir/madam}. Thank you so much for rescuing me. Will you take me to my family now?", "kidnapped_girl_liberated_battle",[]],
  [anyone,"start", [(eq,"$talk_context",tc_hero_freed)],
   "I am in your debt for freeing me friend.", "freed_hero_answer",
   []],
  [anyone|plyr,"freed_hero_answer", [],
   "You're not going anywhere. You'll be my prisoner now!", "freed_hero_answer_1",
   [
     (store_conversation_troop, ":cur_troop_id"),
     (party_add_prisoners, "p_main_party", ":cur_troop_id", 1),#take prisoner
    ]],
  [anyone,"freed_hero_answer_1", [],
   "Alas. Will my luck never change?", "close_window",
   []],
  [anyone|plyr,"freed_hero_answer", [],
   "You're free to go, {s65}.", "freed_hero_answer_2",
   [
    ]],
  [anyone,"freed_hero_answer_2", [],
   "Thank you. I never forget someone who's done me a good turn.", "close_window",
   []],
  [anyone|plyr,"freed_hero_answer", [],
   "Would you like to join me?", "freed_hero_answer_3",
   []],
  [anyone,"freed_hero_answer_3", [(store_random_in_range, ":random_no",0,2),(eq, ":random_no", 0)],
   "All right I will join you.", "close_window",
   [
     (store_conversation_troop, ":cur_troop_id"),
     (party_add_members, "p_main_party", ":cur_troop_id", 1),#join hero
   ]],
  [anyone,"freed_hero_answer_3", [],
   "No, I want to go on my own.", "close_window",
   [
    ]],
  [anyone,"start", [(eq,"$talk_context",tc_hero_defeated)],
   "You'll not live long to enjoy your victory. My kinsmen will soon wipe out the stain of this defeat.", "defeat_hero_answer",
   [
    ]],
  [anyone|plyr,"defeat_hero_answer", [],
   "You are my prisoner now.", "defeat_hero_answer_1",
   [
     (party_add_prisoners, "p_main_party", "$g_talk_troop", 1),#take prisoner
     #(troop_set_slot, "$g_talk_troop", slot_troop_is_prisoner, 1),
     (troop_set_slot, "$g_talk_troop", slot_troop_prisoner_of_party, "p_main_party"),
     (call_script, "script_event_hero_taken_prisoner_by_player", "$g_talk_troop"),
    ]],
  [anyone,"defeat_hero_answer_1", [],
   "Damn you. You will regret this.", "close_window",
   []],
  [anyone|plyr,"defeat_hero_answer", [],
   "You're free to go this time, but don't cross my path again.", "defeat_hero_answer_2",
   []],
  [anyone,"defeat_hero_answer_2", [],
   "We will meet again.", "close_window",
   []],
  [anyone,"political_quest_follow_on", [
  (eq, "$political_quest_found", "qst_resolve_dispute"),
	],
   "I think that is a wise move. Good luck to you.", "close_window",
   [
    (assign, "$g_leave_encounter", 1),
    (setup_quest_text,"qst_resolve_dispute"),

	(quest_get_slot, ":lord_1", "qst_resolve_dispute", slot_quest_target_troop),
	(str_store_troop_name_link, s11, ":lord_1"),

	(quest_get_slot, ":lord_2", "qst_resolve_dispute", slot_quest_object_troop),
	(str_store_troop_name_link, s12, ":lord_2"),

	(str_store_string, s2, "str_resolve_the_dispute_between_s11_and_s12"),
	(call_script, "script_start_quest", "qst_resolve_dispute", -1),
	(quest_set_slot, "qst_resolve_dispute", slot_quest_expiration_days, 30),
	(quest_set_slot, "qst_resolve_dispute", slot_quest_giver_troop, "$g_talk_troop"),
	(quest_set_slot, "qst_resolve_dispute", slot_quest_target_state, 0),
	(quest_set_slot, "qst_resolve_dispute", slot_quest_object_state, 0),

	(quest_get_slot, ":lord_1", "qst_resolve_dispute", slot_quest_target_troop), #this block just to check if the slots work
	(str_store_troop_name, s11, ":lord_1"),
	(quest_get_slot, ":lord_2", "qst_resolve_dispute", slot_quest_object_troop),
	(str_store_troop_name, s12, ":lord_2"),
	],
   ],
  [anyone,"political_quest_follow_on", [
  (eq, "$political_quest_found", "qst_offer_gift"),
  ],
   "Splendid. I shall await the materials.", "close_window",
   [
   (assign, "$g_leave_encounter", 1),
    (setup_quest_text,"qst_offer_gift"),

	(quest_get_slot, ":lord_1", "qst_offer_gift", slot_quest_target_troop),
	(str_store_troop_name, s14, ":lord_1"),
	(str_store_troop_name, s12, "$g_talk_troop"),
	##diplomacy start+
	#(troop_get_type, reg4, "$g_talk_troop"),
	(assign, reg4, reg65),
	##diplomacy end+

	(str_store_string, s2, "str_you_intend_to_bring_gift_for_s14"),

   (call_script, "script_start_quest", "qst_offer_gift", "$g_talk_troop"),
   (quest_set_slot, "qst_offer_gift", slot_quest_expiration_days, 30),
   ]],
	[anyone,"political_quest_follow_on", [
	(eq, "$political_quest_found", "qst_denounce_lord"),
	(this_or_next|eq, "$g_talk_troop", "$g_player_minister"),
		(troop_slot_eq, "trp_player", slot_troop_spouse, "$g_talk_troop"),
  ],
   "We appreciate what you are doing. I find such intrigues distasteful, but it is all for the good of the {s5}.", "close_window",
   [
   (quest_set_slot, "qst_denounce_lord", slot_quest_target_troop, "$political_quest_target_troop"),

   (quest_get_slot, ":target_troop", "qst_denounce_lord", slot_quest_target_troop),
   (str_store_troop_name_link, s14, ":target_troop"),
   (str_store_troop_name_link, s12, "$g_talk_troop"),

   (str_store_string, s2, "str_you_intend_to_denounce_s14_to_his_face_on_behalf_of_s14"),
   (setup_quest_text, "qst_denounce_lord"),

   (call_script, "script_start_quest", "$political_quest_found", "$g_talk_troop"),
   (quest_set_slot, "qst_denounce_lord", slot_quest_expiration_days, 60),

   (str_store_faction_name, s5, "$players_kingdom"),
   (assign, "$g_leave_encounter", 1),
   ]],
	[anyone,"political_quest_follow_on", [
	(eq, "$political_quest_found", "qst_denounce_lord"),
  ],
   "Very well. It is always risky to involve yourself in intrigues of this sort, but in this case, I think you will benefit.", "close_window",
   [
   (quest_set_slot, "qst_denounce_lord", slot_quest_target_troop, "$political_quest_target_troop"),

   (quest_get_slot, ":target_troop", "qst_denounce_lord", slot_quest_target_troop),
   (str_store_troop_name_link, s14, ":target_troop"),
   (str_store_troop_name_link, s12, "$g_talk_troop"),

   (str_store_string, s2, "str_you_intend_to_denounce_s14_to_his_face_on_behalf_of_s14"),
   (setup_quest_text, "qst_denounce_lord"),

   (call_script, "script_start_quest", "$political_quest_found", "$g_talk_troop"),
   (assign, "$g_leave_encounter", 1),
]],
   #Intrigue lord for
	[anyone,"political_quest_follow_on", [
	(eq, "$political_quest_found", "qst_intrigue_against_lord"),
#	(this_or_next|eq, "$g_talk_troop", "$g_player_minister"),
#		(troop_slot_eq, "trp_player", slot_troop_spouse, "$g_talk_troop"),
    (str_store_faction_name, s5, "$players_kingdom"),

  ],
   "We appreciate what you are doing. I find such intrigues distasteful, but it is all for the good of the {s5}.", "close_window",
   [
   (quest_set_slot, "qst_intrigue_against_lord", slot_quest_target_troop, "$political_quest_target_troop"),

   (quest_get_slot, ":target_troop", "qst_intrigue_against_lord", slot_quest_target_troop),
   (store_faction_of_troop, ":target_troop_faction", ":target_troop"),
   (faction_get_slot, ":faction_liege", ":target_troop_faction", slot_faction_leader),
   (str_store_troop_name_link, s14, ":target_troop"),
   (str_store_troop_name_link, s13, ":faction_liege"),
   (str_store_troop_name_link, s12, "$g_talk_troop"),

   (str_store_string, s2, "str_you_intend_to_denounce_s14_to_s13_on_behalf_of_s12"),
   (setup_quest_text, "qst_intrigue_against_lord"),

   (call_script, "script_start_quest", "$political_quest_found", "$g_talk_troop"),
   (quest_set_slot, "qst_intrigue_against_lord", slot_quest_expiration_days, 60),
   (assign, "$g_leave_encounter", 1),
   ]],
  [anyone|plyr,"political_quest_suggested", [
  (gt, "$political_quest_found", 0),
  ],
   "I like that idea.", "political_quest_follow_on",
   [
   ]],
  [anyone|plyr,"political_quest_suggested", [
  (gt, "$political_quest_found", 0),
  ],
   "Hmm.. Maybe you can think of something else?", "combined_political_quests",
   [
   (quest_set_slot, "$political_quest_found", slot_quest_dont_give_again_remaining_days, 3),
   (call_script, "script_get_political_quest", "$g_talk_troop"),
   (assign, "$political_quest_found", reg0),
   (assign, "$political_quest_target_troop", reg1),
   (assign, "$political_quest_object_troop", reg2),

   ]],
  [anyone|plyr,"political_quest_suggested", [],
   "Let us discuss another topic", "political_quests_end",
   []],
  [anyone,"political_quests_end", [
  (troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_hero),
  ],
   "Very well.", "lord_pretalk",
   []],
  [anyone,"political_quests_end", [
  (troop_slot_eq, "trp_player", slot_troop_spouse, "$g_talk_troop"),
  ],
   "Very well.", "spouse_pretalk",
   []],
  [anyone,"political_quests_end", [
  (eq, "$g_talk_troop", "$g_player_minister"),
  ],
   "Very well.", "minister_pretalk",
   []],
  [anyone,"political_quests_end", [
  ],
   "Very well.", "close_window",
   [
   (assign, "$g_leave_encounter", 1),
   ]],
# Local merchant

  [trp_local_merchant,"start", [], "Mercy! Please don't kill me!", "local_merchant_mercy",[]],
  [anyone|plyr,"local_merchant_mercy", [(quest_get_slot, ":quest_giver_troop", "qst_kill_local_merchant", slot_quest_giver_troop),(str_store_troop_name, s2, ":quest_giver_troop"),
  ##diplomacy start+ Initialize reg4 for use below
  (assign, reg4, 0),
  (try_begin),
	(call_script, "script_cf_dplmc_troop_is_female", ":quest_giver_troop"),
	(assign, reg4, 1),
  (try_end),
  ],#next line man to {reg65?woman:man}
   "I have nothing against you {reg65?woman:man}. But {s2} wants you dead. Sorry.", "local_merchant_mercy_no",[]],
   ##diplomacy end+
  [anyone,"local_merchant_mercy_no", [], "Damn you! May you burn in Hell!", "close_window",[]],
  [anyone|plyr,"local_merchant_mercy", [], "I'll let you live, if you promise me...", "local_merchant_mercy_yes",[]],
  [anyone,"local_merchant_mercy_yes", [], "Of course, I promise, I'll do anything. Just spare my life... ", "local_merchant_mercy_yes_2",[]],
  ##diplomacy start+ use reg4 from before to make gender correct
  [anyone|plyr,"local_merchant_mercy_yes_2", [], "You are going to forget about {s2}'s debt to you. And you will sign a paper stating that {reg4?she:he} owes you nothing.", "local_merchant_mercy_yes_3",[]],
  ##diplomacy end+
  [anyone,"local_merchant_mercy_yes_3", [], "Yes, of course. I'll do as you say.", "local_merchant_mercy_yes_4",[]],
  [anyone|plyr,"local_merchant_mercy_yes_4", [], "And if my lord hears so much of a hint of a complaint about this issue, then I'll come back for you,\
 and it won't matter how much you scream for mercy then.\
 Do you understand me?", "local_merchant_mercy_yes_5",[]],
  [anyone,"local_merchant_mercy_yes_5", [], "Yes {sir/madam}. Don't worry. I won't make any complaint.", "local_merchant_mercy_yes_6",[]],
  [anyone|plyr,"local_merchant_mercy_yes_6", [], "Good. Go now, before I change my mind.", "close_window",
   [(quest_set_slot, "qst_kill_local_merchant", slot_quest_current_state, 2),
    (call_script, "script_succeed_quest", "qst_kill_local_merchant"),
    (finish_mission),
    ]],
# Village traitor

  [trp_fugitive,"start", [], "What do you want?", "fugitive_1",[]],
  [anyone|plyr,"sacrificed_messenger_1", [(quest_get_slot, ":quest_target_center", "qst_incriminate_loyal_commander", slot_quest_target_center),
                                          (str_store_party_name, s1, ":quest_target_center"),
                                          (quest_get_slot, ":quest_object_troop", "qst_incriminate_loyal_commander", slot_quest_object_troop),
                                          (str_store_troop_name, s2, ":quest_object_troop"),],
   "Take this letter to {s1} and give it to {s2}.", "sacrificed_messenger_2",[]],
  [anyone|plyr,"sacrificed_messenger_1", [],
   "Nothing. Nothing at all.", "close_window",[]],
  [anyone,"sacrificed_messenger_2", [],
   "Yes {sir/madam}. You can trust me. I will not fail you.", "sacrificed_messenger_3",[]],
  [anyone|plyr,"sacrificed_messenger_3", [],
   "Good. I will not forget your service. You will be rewarded when you return.", "close_window",[(party_remove_members, "p_main_party", "$g_talk_troop", 1),
                                     (set_spawn_radius, 0),
                                     (spawn_around_party, "p_main_party", "pt_sacrificed_messenger"),
                                     (assign, ":new_party", reg0),
                                     (party_add_members, ":new_party", "$g_talk_troop", 1),
                                     (party_set_ai_behavior, ":new_party", ai_bhvr_travel_to_party),
                                     (quest_get_slot, ":quest_target_center", "qst_incriminate_loyal_commander", slot_quest_target_center),
                                     (party_set_ai_object, ":new_party", ":quest_target_center"),
                                     (party_set_flags, ":new_party", pf_default_behavior, 0),
                                     (quest_set_slot, "qst_incriminate_loyal_commander", slot_quest_current_state, 2),
                                     (quest_set_slot, "qst_incriminate_loyal_commander", slot_quest_target_party, ":new_party")]],
  [anyone|plyr,"sacrificed_messenger_3", [], "Arggh! I can't do this. I can't send you to your own death!", "sacrificed_messenger_cancel",[]],
  [anyone,"sacrificed_messenger_cancel", [], "What do you mean {sir/madam}", "sacrificed_messenger_cancel_2",[]],
  [anyone|plyr,"sacrificed_messenger_cancel_2", [(quest_get_slot, ":quest_giver", "qst_incriminate_loyal_commander", slot_quest_giver_troop),
                                                 (str_store_troop_name, s3, ":quest_giver"),
      ], "There's a trap set up for you in the town.\
 {s3} ordered me to sacrifice one of my chosen warriors to fool the enemy,\
 but he will just need to find another way.", "sacrificed_messenger_cancel_3",[
     (quest_get_slot, ":quest_giver", "qst_incriminate_loyal_commander", slot_quest_giver_troop),
     (quest_set_slot, "qst_incriminate_loyal_commander", slot_quest_current_state, 1),
     (call_script, "script_change_player_relation_with_troop",":quest_giver",-5),
     (call_script, "script_change_player_honor", 3),
     (call_script, "script_fail_quest", "qst_incriminate_loyal_commander"),
     ]],
  [anyone,"sacrificed_messenger_cancel_3", [], "Thank you, {sir/madam}.\
 I will follow you to the gates of hell. But this would not be a good death.", "close_window",[]],
  [party_tpl|pt_sacrificed_messenger,"start", [],
   "Don't worry, {sir/madam}, I'm on my way.", "close_window",[(assign, "$g_leave_encounter",1)]],
#Spy

  [party_tpl|pt_spy,"start", [], "Good day {sir/madam}. Such fine weather don't you think? If you'll excuse me now I must go on my way.", "follow_spy_talk",[]],
  [anyone|plyr, "follow_spy_talk",
   [
     (quest_get_slot, ":quest_giver", "qst_follow_spy", slot_quest_giver_troop),
     (str_store_troop_name, s1, ":quest_giver"),
     ],
   "In the name of {s1}, you are under arrest!", "follow_spy_talk_2", []],
  [anyone, "follow_spy_talk_2", [], "You won't get me alive!", "close_window", []],
  [anyone|plyr, "follow_spy_talk", [], "Never mind me. I was just passing by.", "close_window", [(assign, "$g_leave_encounter",1)]],
  [party_tpl|pt_spy_partners,"start", [], "Greetings.", "spy_partners_talk",[]],
###Conspirator
##
##  [party_tpl|pt_conspirator_leader,"start", [], "TODO: Hello.", "conspirator_talk",[]],
##  [party_tpl|pt_conspirator,"start", [], "TODO: Hello.", "conspirator_talk",[]],
##
##  [anyone|plyr,"conspirator_talk", [(gt, "$qst_capture_conspirators_leave_meeting_counter", 0),
##                                    (quest_get_slot,":quest_giver","qst_capture_conspirators",slot_quest_giver_troop),
##                                    (str_store_troop_name,s1,":quest_giver")],
##   "TODO: In the name of {s1}, you are under arrest!", "conspirator_talk_2",[]],
##
##  [anyone|plyr,"conspirator_talk", [], "TODO: Bye.", "close_window",[(assign, "$g_leave_encounter",1)]],
##
##  [anyone,"conspirator_talk_2", [], "You won't get me alive!", "close_window",[]],
##
#Runaway Peasants


  [party_tpl|pt_runaway_serfs,"start", [(party_slot_eq, "$g_encountered_party", slot_town_center, 0)],#slot_town_center is used for first time meeting
   "Good day {sir/madam}.", "runaway_serf_intro_1",
   [(party_set_slot, "$g_encountered_party", slot_town_center, 1)]],
  [anyone|plyr,"runaway_serf_intro_1", [(quest_get_slot, ":lord", "qst_bring_back_runaway_serfs", slot_quest_giver_troop),
                                        (str_store_troop_name, s4, ":lord")],
   "I have been sent by your {s4} whom you are running from. He will not punish you if you return now.", "runaway_serf_intro_2",[]],
  [anyone,"runaway_serf_intro_2", [(quest_get_slot, ":target_center", "qst_bring_back_runaway_serfs", slot_quest_target_center),
                                   (str_store_party_name, s6, ":target_center"),
                                   (quest_get_slot, ":quest_object_center", "qst_bring_back_runaway_serfs", slot_quest_object_center),
                                   (str_store_party_name, s1, ":quest_object_center")],
   "My good {sir/madam}. Our lives at our village {s1} was unbearable. We worked all day long and still went to bed hungry.\
 We are going to {s6} to start a new life, where we will be treated like humans.", "runaway_serf_intro_3",[]],
  [anyone|plyr,"runaway_serf_intro_3", [(quest_get_slot, ":quest_object_center", "qst_bring_back_runaway_serfs", slot_quest_object_center),
                                        (str_store_party_name, s1, ":quest_object_center"),],
   "You have gone against our laws by running from your bondage. You will go back to {s1} now!", "runaway_serf_go_back",
   [(quest_get_slot, ":quest_object_center", "qst_bring_back_runaway_serfs", slot_quest_object_center),
    (call_script, "script_change_player_relation_with_center", ":quest_object_center", -1)]],
  [anyone|plyr,"runaway_serf_intro_3", [], "Well, maybe you are right. All right then. If anyone asks, I haven't seen you.", "runaway_serf_let_go",
   [(quest_get_slot, ":quest_object_center", "qst_bring_back_runaway_serfs", slot_quest_object_center),
    (call_script, "script_change_player_relation_with_center", ":quest_object_center", 1)]],
  [party_tpl|pt_runaway_serfs,"runaway_serf_go_back", [(quest_get_slot, ":home_center", "qst_bring_back_runaway_serfs", slot_quest_object_center),
                                                       (str_store_party_name, s5, ":home_center")],
   "All right {sir/madam}. As you wish. We'll head back to {s5} now.", "close_window",
   [(quest_get_slot, ":quest_object_center", "qst_bring_back_runaway_serfs", slot_quest_object_center),
    (party_set_ai_object, "$g_encountered_party", ":quest_object_center"),
    (assign, "$g_leave_encounter",1)]],
  [anyone,"runaway_serf_let_go", [], "God bless you, {sir/madam}. We will not forget your help.", "close_window",
   [(party_set_slot, "$g_encountered_party", slot_town_castle, 1),
    (assign, "$g_leave_encounter",1)]],
  [party_tpl|pt_runaway_serfs,"start", [(party_slot_eq, "$g_encountered_party", slot_town_castle, 1),
                                        ],
   "Good day {sir/madam}. Don't worry. If anyone asks, we haven't seen you.", "runaway_serf_reconsider",[]],
  [anyone|plyr,"runaway_serf_reconsider", [], "I have changed my mind. You must back to your village!", "runaway_serf_go_back",
   [(party_set_slot, "$g_encountered_party", slot_town_castle, 0),
    (quest_get_slot, ":quest_object_center", "qst_bring_back_runaway_serfs", slot_quest_object_center),
    (call_script, "script_change_player_relation_with_center", ":quest_object_center", -2)]],
  [anyone|plyr,"runaway_serf_reconsider", [], "Good. Go quickly now before I change my mind.", "runaway_serf_let_go",[]],
  [party_tpl|pt_runaway_serfs,"start", [(party_slot_eq, "$g_encountered_party", slot_town_castle, 0),
                                        (get_party_ai_object, ":cur_ai_object"),
                                        (quest_get_slot, ":home_center", "qst_bring_back_runaway_serfs", slot_quest_object_center),
                                        (neq, ":home_center", ":cur_ai_object")],
   "Good day {sir/madam}. We were heading back to {s5}, but I am afraid we lost our way.", "runaway_serf_talk_caught",[]],
  [anyone|plyr,"runaway_serf_talk_caught", [], "Do not test my patience. You are going back now!", "runaway_serf_go_back",[]],
  [anyone|plyr,"runaway_serf_talk_caught", [], "Well, if you are that eager to go, then go.", "runaway_serf_let_go",
   [(quest_get_slot, ":quest_object_center", "qst_bring_back_runaway_serfs", slot_quest_object_center),
    (call_script, "script_change_player_relation_with_center", ":quest_object_center", 1)]],
  [party_tpl|pt_runaway_serfs,"start",
   [(quest_get_slot, ":home_center", "qst_bring_back_runaway_serfs", slot_quest_object_center),
    (str_store_party_name, s5, ":home_center")], "We are on our way back to {s5} {sir/madam}.", "runaway_serf_talk_again_return",[]],
  [anyone|plyr,"runaway_serf_talk_again_return", [], "Make haste now. The sooner you return the better.", "runaway_serf_talk_again_return_2",[]],
  [anyone|plyr,"runaway_serf_talk_again_return", [], "Good. Keep going.", "runaway_serf_talk_again_return_2",[]],
  [anyone|plyr,"runaway_serf_talk_again_return_2", [], "Yes {sir/madam}. As you wish.", "close_window",[(assign, "$g_leave_encounter",1)]],
#Quest bandits
  [anyone,"start", [
  (check_quest_active, "qst_track_down_bandits"),
  (quest_slot_eq, "qst_track_down_bandits", slot_quest_target_party, "$g_encountered_party"),
  (neg|is_between, "$g_encountered_party_faction", kingdoms_begin, kingdoms_end), #ie, the party has not respawned as a non-bandit
  ],
   "This must be your unlucky day. We're just about the worst people you could run into, in these parts.", "troublesome_bandits_intro_1",[
   ]],
 [anyone|plyr,"troublesome_bandits_intro_1", [],
   "Heh. For me, you are nothing more than walking money bags.\
 A merchant in {s1} offered me good money for your heads.",
   "troublesome_bandits_intro_2", [(quest_get_slot, ":quest_giver_center", "qst_track_down_bandits", slot_quest_giver_center),
                                   (str_store_party_name, s1, ":quest_giver_center")
                                   ]],
  [anyone,"troublesome_bandits_intro_2", [],
   "A bounty hunter! Kill {him/her}! Kill {him/her} now!", "close_window",[
   (encounter_attack)]],
#Deserters
  [party_tpl|pt_deserters, "start", [(eq,"$talk_context",tc_party_encounter),
                                     (party_get_slot,":protected_until_hours", "$g_encountered_party",slot_party_ignore_player_until),
                                     (store_current_hours,":cur_hours"),
                                     (store_sub, ":protection_remaining",":protected_until_hours",":cur_hours"),
                                     (gt, ":protection_remaining", 0)], "What do you want?\
 You want to pay us some more money?", "deserter_paid_talk",[]],
  [anyone|plyr,"deserter_paid_talk", [], "Sorry to trouble you. I'll be on my way now.", "deserter_paid_talk_2a",[]],
  [anyone,"deserter_paid_talk_2a", [], "Yeah. Stop fooling around and go make some money.\
 I want to see that purse full next time I see you.", "close_window",[(assign, "$g_leave_encounter",1)]],
  [anyone|plyr,"deserter_paid_talk", [], "No. It's your turn to pay me this time.", "deserter_paid_talk_2b",[]],
  [anyone,"deserter_paid_talk_2b", [], "What nonsense are you talking about? You want trouble? You got it.", "close_window",[
       (party_set_slot,"$g_encountered_party",slot_party_ignore_player_until,0),
       (party_ignore_player, "$g_encountered_party", 0),
    ]],
  [party_tpl|pt_deserters,"start", [
      (eq,"$talk_context",tc_party_encounter)
                    ], "We are the free brothers.\
 We will fight only for ourselves from now on.\
 Now give us your money or taste our steel.", "deserter_talk",[]],
##  [anyone|plyr,"deserter_talk", [(check_quest_active, "qst_bring_back_deserters"),
##                                 (quest_get_slot, ":target_deserter_troop", "qst_bring_back_deserters", slot_quest_target_troop),
##                                 (party_count_members_of_type, ":num_deserters", "$g_encountered_party",":target_deserter_troop"),
##                                 (gt, ":num_deserters", 1)],
##   "If you surrender to me now, you will rejoin the army of your kingdom without being punished. Otherwise you'll get a taste of my sword.", "deserter_join_as_prisoner",[]],
  [anyone|plyr,"deserter_talk", [], "When I'm done with you, you'll regret ever leaving your army.", "close_window",[]],
  [anyone|plyr,"deserter_talk", [], "There's no need to fight. I am ready to pay for free passage.", "deserter_barter",[]],
##  [anyone,"deserter_join_as_prisoner", [(call_script, "script_party_calculate_strength", "p_main_party"),
##                                        (assign, ":player_strength", reg0),
##                                        (store_encountered_party,":encountered_party"),
##                                        (call_script, "script_party_calculate_strength", ":encountered_party"),
##                                        (assign, ":enemy_strength", reg0),
##                                        (val_mul, ":enemy_strength", 2),
##                                        (ge, ":player_strength", ":enemy_strength")],
##   "All right we join you then.", "close_window",[(assign, "$g_enemy_surrenders", 1)]],
##  [anyone,"deserter_join_as_prisoner", [], "TODO: We will never surrender!", "close_window",[(encounter_attack)]],

  [anyone,"deserter_barter", [], "Good. You are clever. Now, having a look at your baggage, I reckon a fellow like you could pretty easily afford {reg5} mon. We wouldn't want to be too greedy, now would we? Pay us, and then you can go.", "deserter_barter_2",[
    (store_troop_gold, ":total_value", "trp_player"),
    (troop_get_inventory_capacity, ":inv_size", "trp_player"),
    (try_for_range, ":i_slot", 0, ":inv_size"),
         (troop_get_inventory_slot, ":item_id", "trp_player", ":i_slot"),
         (ge, ":item_id", 0),
         (try_begin),
           (is_between, ":item_id", trade_goods_begin, trade_goods_end),
           (store_item_value, ":item_value", ":item_id"),
           (val_add, ":total_value", ":item_value"),
         (try_end),
    (try_end),
    (store_div, "$g_tribute_amount", ":total_value", 10), #10000 gold = excellent_target
    (val_max, "$g_tribute_amount", 10),
    (assign,reg(5),"$g_tribute_amount")]],
  [anyone|plyr,"deserter_barter_2", [(store_troop_gold,reg(2)),(ge,reg(2),"$g_tribute_amount"),(assign,reg(5),"$g_tribute_amount")],
   "All right here's your {reg5} mon.", "deserter_barter_3a",[(troop_remove_gold, "trp_player","$g_tribute_amount")]],
  [anyone|plyr,"deserter_barter_2", [],
   "I don't have that much money with me", "deserter_barter_3b",[]],
  [anyone,"deserter_barter_3b", [],
   "Too bad. Then we'll have to sell you to the slavers.", "close_window",[]],
  [anyone,"deserter_barter_3a", [], "Heh. That wasn't difficult, now, was it? All right. Go now.", "close_window",[
    (store_current_hours,":protected_until"),
    (val_add, ":protected_until", 72),
    (party_set_slot,"$g_encountered_party",slot_party_ignore_player_until,":protected_until"),
    (party_ignore_player, "$g_encountered_party", 72),

    (assign, "$g_leave_encounter",1)
    ]],
##### TODO: QUESTS COMMENT OUT END

#Tavernkeepers

  [anyone ,"start", [(store_conversation_troop,reg(1)),(ge,reg(1),tavernkeepers_begin),(lt,reg(1),tavernkeepers_end)],
   "Good day dear {sir/madam}. How can I help you?", "tavernkeeper_talk",
   [
#    (store_encountered_party,reg(2)),
#    (party_get_slot,"$tavernkeeper_party",reg(2),slot_town_mercs),
    ]],
#Tavern Talk (with travelers)
  [anyone, "start", [(is_between, "$g_talk_troop", tavern_travelers_begin, tavern_travelers_end),
                     (str_store_troop_name, s10, "$g_talk_troop"),
                     (eq,"$g_talk_troop_met",0),
                     ],
   "Greetings, friend. You look like the kind of {man/person} who'd do well to know me.\
 I travel a lot all across Japan and keep an open ear.\
 I can provide you information that you might find useful. For a meager price of course.", "tavern_traveler_talk", [(assign, "$traveler_land_asked", 0)]],
  [anyone, "start",
   [
     (is_between, "$g_talk_troop", tavern_travelers_begin, tavern_travelers_end),
     (gt, "$last_lost_companion", 0),
     (assign, ":companion_found_town", -1),
     (troop_get_slot, ":companion_found_town", "$last_lost_companion", slot_troop_cur_center),
     (is_between, ":companion_found_town", towns_begin, towns_end),
     (str_store_troop_name, s10, "$last_lost_companion"),
     (str_store_party_name, s11, ":companion_found_town"),
     ],
   "Greetings, {playername}. I saw your companion {s10} at an inn at {s11} some days ago. I thought you might like to know.", "tavern_traveler_lost_companion_thanks",
   [(assign, "$last_lost_companion", 0)]],
  [anyone, "start", [(is_between, "$g_talk_troop", tavern_travelers_begin, tavern_travelers_end),
                     ],
   "Greetings, {playername}.", "tavern_traveler_talk", [(assign, "$traveler_land_asked", 0)]],
  [anyone, "start", [(is_between, "$g_talk_troop", tavern_travelers_begin, tavern_travelers_end),
                     (party_get_slot, ":info_faction", "$g_encountered_party", slot_center_traveler_info_faction),
                     (str_store_faction_name, s17, ":info_faction"),
                     ],
   "Greetings. They say you're the kind of {man/woman} who'd be interested to hear that I travel frequently to {s17}. I'll tell you all I know for a mere 100 mon.", "tavern_traveler_answer", []],
#Tavern Talk (with book sellers)
  [anyone, "start", [(is_between, "$g_talk_troop", tavern_booksellers_begin, tavern_booksellers_end),
                     ],
   "Good day {sir/madam}, will you be looking at my books?", "bookseller_talk", []],
  [anyone|plyr, "bookseller_talk", [], "Yes. Show me what you have for sale.", "bookseller_buy", []],
  [anyone,"bookseller_buy", [], "Of course {sir/madam}.", "book_trade_completed",[[change_screen_trade]]],
  [anyone,"book_trade_completed", [], "Anything else?", "bookseller_talk",[]],
  [anyone|plyr,"bookseller_talk", [], "Nothing. Thanks.", "close_window",[]],
#Tavern Talk (with minstrels)
  [anyone, "start", [(is_between, "$g_talk_troop", tavern_minstrels_begin, tavern_minstrels_end),
                     ],
   "Greetings to you, {most noble sir/most noble lady}.", "minstrel_1", []],
  [anyone|plyr, "minstrel_1", [(eq, "$minstrels_introduced", 0),],
   "What is it you do?", "minstrel_job_description",
   [(assign, "$minstrels_introduced", 1), ]],
  [anyone|plyr, "minstrel_1", [(eq, "$minstrels_introduced", 1)  ],
   "I have some questions about courtship in Japan",
   "minstrel_courtship_questions", []],
  [anyone|plyr, "minstrel_1", [(eq, "$minstrels_introduced", 1)  ],
   "Can you teach me any poems?",
   "minstrel_courtship_poem", []],
  [anyone, "minstrel_courtship_poem", [
    (eq, "$allegoric_poem_recitations", 0),
	(this_or_next|eq, "$g_talk_troop", "trp_tavern_minstrel_1"),
		(eq, "$g_talk_troop", "trp_tavern_minstrel_5"),
  ],
   "I can teach you the poem, 'The Storming of the Castle of Love.' It is short enough to be easily learned. It is an allegoric poem, replete with symbols and metaphor. It describes how a brave but rough warrior wins the heart of his lady by upholding, becoming a dutiful and honorable samurai. Its theme -- that the role of a woman is to inspire but also civilize a man -- is appreciated by some noble ladies, but not all.",
   "minstrel_courtship_poem_teach", [
    (assign, "$poem_selected", courtship_poem_allegoric),
   ]],
  [anyone, "minstrel_courtship_poem", [
    (eq, "$mystic_poem_recitations", 0),
	(this_or_next|eq, "$g_talk_troop", "trp_tavern_minstrel_3"),
		(eq, "$g_talk_troop", "trp_tavern_minstrel_1"),
  ],
   "I can teach you the poem, 'The Heart's Desire.' It is a lyrical poem, which can be interpreted either erotically or spiritually. The lover realizes the majesty of the divine by gazing upon the body of his beloved. I believe that it appeals to women of a certain romantic temperament, but you risk scandalizing or boring others.",
   "minstrel_courtship_poem_teach", [
   (assign, "$poem_selected", courtship_poem_mystic),
   ]],
#ashik poem
  [anyone, "minstrel_courtship_poem", [
  	(eq, "$tragic_poem_recitations", 0),
	(this_or_next|eq, "$g_talk_troop", "trp_tavern_minstrel_3"),
		(eq, "$g_talk_troop", "trp_tavern_minstrel_2"),  ],
   "I can teach you the tale of Naniha and Futo no Kata. It is a sad and simple story -- the farmhand Naniha and the nobleman's daughter Futo no Kata love each other, but they can never marry. The poem is Naniha's lament as he wanders alone, unwilling to forget his true love, driving himself mad with longing. Some ladies melt at the sweetness of his sorrows; others glaze over at his self-pity.",
   "minstrel_courtship_poem_teach", [
   (assign, "$poem_selected", courtship_poem_tragic),

   ]],
#nord saga
  [anyone, "minstrel_courtship_poem", [
	(eq, "$heroic_poem_recitations", 0),
	(this_or_next|eq, "$g_talk_troop", "trp_tavern_minstrel_4"),
		(eq, "$g_talk_troop", "trp_tavern_minstrel_2"),

  ],
   "I can teach you part of the saga of Yoshinaka and Tomoe. It is a heroic tale, full of blood and battle. The maiden Tomoe chooses the warrior Yoshinaka as her lover, as he is the only man who can defeat her in combat. Her father, who pledged her to another, comes with his sons and his samurai to kill Yoshinaka. They fight, and Yoshinaka and Tomoe slaughter the entire host except for Tomoe's beloved younger brother -- who, alas, grows up to avenge his father by slaying Yoshinaka. The depiction of warrior and maiden as equals will appeal to some women, but a yoroi-wearing, blood-spattered heroine will shock and repulse others.",
   "minstrel_courtship_poem_teach", [
   (assign, "$poem_selected", courtship_poem_heroic),
   ]],
  [anyone, "minstrel_courtship_poem", [
    (eq, "$comic_poem_recitations", 0),
	(this_or_next|eq, "$g_talk_troop", "trp_tavern_minstrel_5"),
		(eq, "$g_talk_troop", "trp_tavern_minstrel_4"),
  ],
   "I can teach you the poem, 'An Argument in the Garden.' It is a comic poem, which satirizes the conventions of courtly love. A lover steals into a garden in Kyoto, and plies her with lots of witty lines to persuade his lover to submit to his embraces. She shoots down all of his advances one by one, then when he is downcast, she takes him in her arms and tells him that she wanted him all along, except on her terms, not his. A lady with a sense of humor may find it amusing, but others might feel that they are the ones who are being mocked.",
   "minstrel_courtship_poem_teach", [
   (assign, "$poem_selected", courtship_poem_comic),
   ]],
  [anyone, "minstrel_courtship_poem_teach", [],
   "To teach it to you, I will need some hours of your time -- and, of course, a small fee for my services. About 300 mon would suffice.",
   "minstrel_courtship_poem_teach_2", []],
  [anyone, "minstrel_courtship_poem", [],
   "I believe you already know the poems I am best equipped to teach.",
   "minstrel_pretalk", []],
  [anyone|plyr, "minstrel_courtship_poem_teach_2", [
  (store_troop_gold, ":gold", "trp_player"),
  (ge, ":gold", 300),
  ],
   "Yes -- teach me that one",
   "minstrel_courtship_poem_teach_3", []],
  [anyone|plyr, "minstrel_courtship_poem_teach_2", [],
   "Never mind",
   "minstrel_pretalk", []],
  [anyone, "minstrel_courtship_poem_teach_3", [
  (eq, "$poem_selected", courtship_poem_allegoric),
  ],
   "Very well -- repeat after me:^\
   I deflected her skeptical questioning darts^\
   with armor made of purest devotion^\
   purged in the forge of my heart^\
   from the slag of any baser emotion",
   "minstrel_courtship_poem_teach_4", []],
  [anyone, "minstrel_courtship_poem_teach_3", [
  (eq, "$poem_selected", courtship_poem_mystic),
  ],
   "Very well -- repeat after me:^\
   You are the first and the last^\
   the outer and the inner^\
   When I drink from the cup of love^\
   I escape the tread of time^\
   A moment in solitude with you^\
   Would have no beginning and no end",
   "minstrel_courtship_poem_teach_4", []],
  [anyone, "minstrel_courtship_poem_teach_3", [
  (eq, "$poem_selected", courtship_poem_tragic),
  ],
  "Very well -- repeat after me:^\
  The wind that blows the dry road's dust^\
  Stirs the curtains in your tower^\
  The moon that lights my drunken path home^\
  Looks on you sleeping in your bower^\
  If I cried out to the wind^\
  Could it carry a message from my lips?^\
  If I wept before the moon^\
  Would it grant me just a glimpse?",
  "minstrel_courtship_poem_teach_4", [
   ]],
  [anyone, "minstrel_courtship_poem_teach_3", [
  (eq, "$poem_selected", courtship_poem_heroic),
  ],
  "Very well -- repeat after me:^\
   A light pierced the gloom over Kyushu's cliffs...^\
   Where charge of surf broke on the wall of the shore^\
   Grey-helmed and grey-cloaked the maiden stood^\
   On wave-steed's prow, the sailcloth snapping^\
   Over din of oars, of timbers cracking^\
   She cried out to her own brothers, arrayed for war",
   "minstrel_courtship_poem_teach_4", [
   ]],
  [anyone, "minstrel_courtship_poem_teach_3", [
  (eq, "$poem_selected", courtship_poem_comic),
  ],
  "Very well -- repeat after me:^All the silks of China, all the furs of the Jurchen^\
   Would buy you not the briefest kiss^What I bestow, I bestow for love^\
   And the sake of my own happiness^But brought you a gift? Let us see! Let us see!^\
   Or should tell my father how you came to see me?",
  "minstrel_courtship_poem_teach_4", [
   ]],
  [anyone|plyr, "minstrel_courtship_poem_teach_4", [
  (eq, "$poem_selected", courtship_poem_allegoric),
  ],
  "'I deflected her skeptical questioning darts...'",
  "minstrel_learn_poem_continue", [
    (troop_remove_gold, "trp_player", 300),
    (val_add, "$allegoric_poem_recitations", 1),
  ]],
  [anyone|plyr, "minstrel_courtship_poem_teach_4", [
  (eq, "$poem_selected", courtship_poem_mystic),
  ],
  "'You are the first and the last..'",
  "minstrel_learn_poem_continue", [
    (troop_remove_gold, "trp_player", 300),
    (val_add, "$mystic_poem_recitations", 1),
  ]],
  [anyone|plyr, "minstrel_courtship_poem_teach_4", [
  (eq, "$poem_selected", courtship_poem_tragic),
  ],
  "'The wind that blows the dry road's dust...'",
  "minstrel_learn_poem_continue", [
    (troop_remove_gold, "trp_player", 300),
	(val_add, "$tragic_poem_recitations", 1),
  ]],
  [anyone|plyr, "minstrel_courtship_poem_teach_4", [
  (eq, "$poem_selected", courtship_poem_heroic),
  ],
  "'A light pierced the gloom over Kyushu's cliffs...'",
  "minstrel_learn_poem_continue", [
    (troop_remove_gold, "trp_player", 300),
	(val_add, "$heroic_poem_recitations", 1),
  ]],
  [anyone|plyr, "minstrel_courtship_poem_teach_4", [
  (eq, "$poem_selected", courtship_poem_comic),
  ],
  "'All the silks of China...'",
  "minstrel_learn_poem_continue", [
    (troop_remove_gold, "trp_player", 300),
	(val_add, "$comic_poem_recitations", 1),
  ]],
  [anyone|plyr, "minstrel_courtship_poem_teach_4", [
  ],
  "Bah... What kind of filth are you trying to teach me?",
  "minstrel_courtship_poem_teach_reject", []],
  [anyone, "minstrel_courtship_poem_teach_reject", [
  ],
  "Very well. If the poem is not to your taste, then keep your money. But remember -- with poets and with lovers, what is important is not what pleases you. What is important is what your pleases your audience. If you wish to learn the poem, I am still willing to teach.",
  "minstrel_pretalk", []],
  [anyone, "minstrel_learn_poem_continue", [
  ],
   "Very good -- but there are many stanzas to go. Now, listen closely...", "close_window",
   [
    (try_begin),
      (try_begin),
        (eq, "$poem_selected", courtship_poem_mystic),
        (set_achievement_stat, ACHIEVEMENT_ROMANTIC_WARRIOR, 0, 1),
      (else_try),
        (eq, "$poem_selected", courtship_poem_tragic),
        (set_achievement_stat, ACHIEVEMENT_ROMANTIC_WARRIOR, 1, 1),
      (else_try),
        (eq, "$poem_selected", courtship_poem_heroic),
        (set_achievement_stat, ACHIEVEMENT_ROMANTIC_WARRIOR, 2, 1),
      (else_try),
        (eq, "$poem_selected", courtship_poem_comic),
        (set_achievement_stat, ACHIEVEMENT_ROMANTIC_WARRIOR, 3, 1),
      (else_try),
        (eq, "$poem_selected", courtship_poem_allegoric),
        (set_achievement_stat, ACHIEVEMENT_ROMANTIC_WARRIOR, 4, 1),
      (try_end),

      (assign, ":number_of_poems_player_know", 0),
      (try_for_range, ":poem_number", 0, 5),
        (get_achievement_stat, ":poem_is_known", ACHIEVEMENT_ROMANTIC_WARRIOR, ":poem_number"),
        (eq, ":poem_is_known", 1),
        (val_add, ":number_of_poems_player_know", 1),
      (try_end),

      (try_begin),
        (ge, ":number_of_poems_player_know", 3),
        (unlock_achievement, ACHIEVEMENT_ROMANTIC_WARRIOR),
      (try_end),
    (try_end),

    (assign, "$g_leave_town",1),
    (rest_for_hours, 2, 2, 0),
    (finish_mission),
   ]],
  [anyone|plyr, "minstrel_1", [(eq, "$minstrels_introduced", 1)  ],
   "Can you tell me anything about the eligible maidens in this domain?",
   "minstrel_gossip", [
   ]],
  [anyone, "minstrel_gossip",
  [],
   "About whom did you wish to know?",
   "minstrel_gossip_select", []],
  [anyone|plyr,"minstrel_gossip_select",
   [],
   "Just tell me the latest piece of gossip",
   "minstrel_gossip_maiden_selected_2", [

    (assign, "$lady_selected", -1),
	(assign, "$romantic_rival", -1),

    (try_for_range, ":log_entry", 0, "$num_log_entries"),
		(troop_get_slot, ":lady", "trp_log_array_actor", ":log_entry"),
		(is_between, ":lady", kingdom_ladies_begin, kingdom_ladies_end),
		(neg|troop_slot_eq, "trp_player", slot_troop_spouse, ":lady"),

		(troop_get_slot, ":type", "trp_log_array_entry_type", ":log_entry"),
		(is_between, ":type", 50, 65), #excludes log entries in which a party is an actor

		(store_faction_of_troop, ":lady_faction", ":lady"),
		(store_faction_of_party, ":town_faction", "$g_encountered_party"),
		(eq, ":lady_faction", ":town_faction"),
		(assign, "$lady_selected", ":lady"),
		(try_begin),
			(eq, "$cheat_mode", 1),
			(str_store_troop_name, s4, ":lady"),
			(troop_get_slot, reg4, "trp_log_array_entry_type", ":log_entry"),
			(assign, reg5, "$num_log_entries"),
			(display_message, "str_log_entry_type_reg4_for_s4_total_entries_reg5"),
		(try_end),
	(try_end),

   ]],
  [anyone|plyr|repeat_for_troops,"minstrel_gossip_select",
   [
   (store_repeat_object, "$temp"),
   (troop_slot_eq, "$temp", slot_troop_occupation, slto_kingdom_lady),
   (troop_slot_eq, "$temp", slot_troop_spouse, -1),
   (store_faction_of_troop, ":lady_faction", "$temp"),
   (store_faction_of_party, ":town_faction", "$g_encountered_party"),
   (eq, ":lady_faction", ":town_faction"),
   (str_store_troop_name, s10, "$temp"),
   ],
   "{s10}",
   "minstrel_gossip_maiden_selected", [
    (store_repeat_object, "$lady_selected"),
   ]],
  [anyone|plyr,"minstrel_gossip_select",
   [], "Never mind", "minstrel_pretalk", []],
   [anyone,"minstrel_gossip_maiden_selected",
   [
	(try_begin),
		(eq, "$cheat_mode", 1),
		(assign, reg3, "$lady_selected"),
		(display_message, "@{!}DEBUG: Gossip for troop {reg3}"),
		(gt, reg3, -1),
		(display_message, "@{!}DEBUG: {s3}"),
	(try_end),

	(try_begin),
	   (gt, "$lady_selected", -1),
	   (str_store_troop_name, s9, "$lady_selected"), #lady

      ##diplomacy start+ Make gender-correct
      (try_begin),
         (call_script, "script_cf_dplmc_troop_is_female", "$lady_selected"),
         (assign, reg4, 1),
      (else_try),
         (assign, reg4, 0),
      (try_end),
      #the strings below have been modified to use reg4 for gender
      ##diplomacy end+
	   (str_store_string, s10, "str_error__reputation_type_for_s9_not_within_range"),
	   (try_begin),
			(troop_slot_eq, "$lady_selected", slot_lord_reputation_type, lrep_conventional),
			(str_store_string, s16, "str_they_say_that_s9_is_a_most_conventional_maiden__devoted_to_her_family_of_a_kind_and_gentle_temperament_a_lady_in_all_her_way"),
	   (else_try),
			(troop_slot_eq, "$lady_selected", slot_lord_reputation_type, lrep_otherworldly),
			(str_store_string, s16, "str_they_say_that_s9_is_a_bit_of_a_romantic_a_dreamer__of_a_gentle_temperament_yet_unpredictable_she_is_likely_to_be_led_by_her_passions_and_will_be_trouble_for_her_family_ill_wager"),
	   (else_try),
			(troop_slot_eq, "$lady_selected", slot_lord_reputation_type, lrep_ambitious),
			(str_store_string, s16, "str_they_say_that_s9_is_determined_to_marry_well_and_make_her_mark_in_the_world_she_may_be_a_tremendous_asset_for_her_husband__provided_he_can_satisfy_her_ambition"),
	   (else_try),
			(troop_slot_eq, "$lady_selected", slot_lord_reputation_type, lrep_adventurous),
			(str_store_string, s16, "str_they_say_that_s9_loves_to_hunt_and_ride_maybe_she_wishes_she_were_a_man_whoever_she_marries_will_have_a_tough_job_keeping_the_upper_hand_i_would_say"),
	   (else_try),
			(troop_slot_eq, "$lady_selected", slot_lord_reputation_type, lrep_moralist),
			(str_store_string, s16, "str_they_say_that_s9_is_a_lady_of_the_highest_moral_standards_very_admirable_very_admirable__and_very_hard_to_please_ill_warrant"),
	   (try_end),

	   (call_script, "script_add_rumor_string_to_troop_notes", "$lady_selected", -1, 16),
   (try_end),
   ],
   "{s16}",
   "minstrel_gossip_maiden_selected_2", [
   ]],
   [anyone,"minstrel_gossip_maiden_selected_2",
   [
	##diplomacy+
	##OLD:
	#(troop_slot_eq, "trp_player", slot_troop_spouse, "$lady_selected"),
	#(is_between, "$lady_selected", kingdom_ladies_begin, kingdom_ladies_end),
	##NEW:
	(is_between, "$lady_selected", heroes_begin, heroes_end),
	(this_or_next|troop_slot_eq, "$lady_selected", slot_troop_spouse, "trp_player"),
		(troop_slot_eq, "trp_player", slot_troop_spouse, "$lady_selected"),
	(call_script, "script_dplmc_store_troop_is_female",  "$lady_selected"),#Add support for male version
	],#Next line, "She" -> {reg0?She:He} , "she" -> {reg0?she:he}
	"{reg0?She:He} is married to you, of course! Clearly, no one would dream that {reg0?she:he} would do anything to engender gossip.",
   "minstrel_postgossip",
   ##diplomacy end+
	[]],
   [anyone,"minstrel_gossip_maiden_selected_2",
   [
    (gt, "$lady_selected", -1),
	(assign, ":lady", "$lady_selected"),
	(neg|troop_slot_ge, ":lady", slot_troop_spouse, active_npcs_begin),
	(troop_get_slot, ":betrothed", ":lady", slot_troop_betrothed),
	(is_between, ":betrothed", active_npcs_begin, active_npcs_end),

	(str_store_troop_name, s9, ":lady"),
	(str_store_troop_name, s11, ":betrothed"),

	(str_store_string, s12, "str_s9_is_now_betrothed_to_s11_soon_we_believe_there_shall_be_a_wedding"),
	(try_begin),
		(troop_slot_eq, ":lady", slot_troop_met, 2),
		(assign, "$romantic_rival", ":betrothed"),
	(try_end),
	],
	"{s12}.",
   "minstrel_postgossip", []],
   [anyone,"minstrel_gossip_maiden_selected_2",
   [
      ##diplomacy start+ Make gender-correct
      #xxx TODO ensure this actually works, untangle how this is used
      #The strings below have been modified to use reg4 for gender
     (try_begin),
        (call_script, "script_cf_dplmc_troop_is_female", "$lady_selected"),
        (assign, reg4, 1),
	 (else_try),
        (assign, reg4, 0),
     (try_end),
      ##diplomacy end+
    (try_begin),
		(is_between, "$lady_selected", kingdom_ladies_begin, kingdom_ladies_end),
	    (str_store_string, s12, "str_i_have_not_heard_any_news_about_her"),

		(str_store_troop_name, s9, "$lady_selected"), #lady

		(try_begin),
			(eq, "$cheat_mode", 1), #for some reason, speaking to tavern merchant does not yield rumor. Try for Lady Baoth, Lord Etr
			(display_message, "str_searching_for_rumors_for_s9"),
		(try_end),

		(assign, "$romantic_rival", -1),
		(assign, ":last_lady_noted", 0),
		(try_for_range, ":log_entry", 0, "$num_log_entries"),
			(troop_slot_eq, "trp_log_array_actor", ":log_entry", "$lady_selected"),


			#Presumably possible for some events involving a lady to not involve troops
			(troop_get_slot, ":suitor", "trp_log_array_troop_object", ":log_entry"),
			(str_clear, s11),
			(try_begin),
				(is_between, ":suitor", 0, kingdom_ladies_end),
				(str_store_troop_name, s11, ":suitor"),
			(try_end),

			(troop_get_slot, ":third_party", "trp_log_array_center_object", ":log_entry"),
			(str_clear, s10),
			(try_begin),
				(is_between, ":third_party", 0, kingdom_ladies_end),
				(str_store_troop_name, s10, ":third_party"),
			(try_end),

			(assign, ":lady", "$lady_selected"),

			(try_begin),
				(troop_slot_eq, "trp_log_array_entry_type",  ":log_entry", logent_lady_favors_suitor),
				(str_store_string, s12, "str_they_say_that_s9_has_shown_favor_to_s11_perhaps_it_will_not_be_long_until_they_are_betrothed__if_her_family_permits"),
				(assign, ":last_lady_noted", ":lady"),
				(assign, ":last_suitor_noted", ":suitor"),

				(try_begin),
					(troop_slot_eq, ":lady", slot_troop_met, 2),
					(this_or_next|troop_slot_eq, ":suitor", slot_troop_love_interest_1, ":lady"),
					(this_or_next|troop_slot_eq, ":suitor", slot_troop_love_interest_2, ":lady"),
						(troop_slot_eq, ":suitor", slot_troop_love_interest_3, ":lady"),

					(assign, "$romantic_rival", ":suitor"),
				(try_end),
			(else_try),
				(troop_slot_eq, "trp_log_array_entry_type",  ":log_entry", logent_lady_betrothed_to_suitor_by_family),
				(str_store_string, s12, "str_they_say_that_s9_has_been_forced_by_her_family_into_betrothal_with_s11"),
				(assign, ":last_lady_noted", ":lady"),
				(assign, ":last_suitor_noted", ":suitor"),

				(try_begin),
					(troop_slot_eq, ":lady", slot_troop_met, 2),
					(assign, "$romantic_rival", ":suitor"),
				(try_end),
			(else_try),
				(troop_slot_eq, "trp_log_array_entry_type",  ":log_entry", logent_lady_betrothed_to_suitor_by_choice),
				(str_store_string, s12, "str_they_say_that_s9_has_agreed_to_s11s_suit_and_the_two_are_now_betrothed"),
				(assign, ":last_lady_noted", ":lady"),
				(assign, ":last_suitor_noted", ":suitor"),

				(try_begin),
					(troop_slot_eq, ":lady", slot_troop_met, 2),
					(this_or_next|troop_slot_eq, ":suitor", slot_troop_love_interest_1, ":lady"),
					(this_or_next|troop_slot_eq, ":suitor", slot_troop_love_interest_2, ":lady"),
						(troop_slot_eq, ":suitor", slot_troop_love_interest_3, ":lady"),


					(assign, "$romantic_rival", ":suitor"),
				(try_end),

			(else_try),
				(troop_slot_eq, "trp_log_array_entry_type",  ":log_entry", logent_lady_betrothed_to_suitor_by_pressure),
				(str_store_string, s12, "str_they_say_that_s9_under_pressure_from_her_family_has_agreed_to_betrothal_with_s11"),
				(assign, ":last_lady_noted", ":lady"),
				(assign, ":last_suitor_noted", ":suitor"),

				(try_begin),
					(troop_slot_eq, ":lady", slot_troop_met, 2),
					(this_or_next|troop_slot_eq, ":suitor", slot_troop_love_interest_1, ":lady"),
					(this_or_next|troop_slot_eq, ":suitor", slot_troop_love_interest_2, ":lady"),
						(troop_slot_eq, ":suitor", slot_troop_love_interest_3, ":lady"),

					(assign, "$romantic_rival", ":suitor"),
				(try_end),

			(else_try),

				(troop_slot_eq, "trp_log_array_entry_type",  ":log_entry", logent_lady_rejects_suitor),
				(str_store_string, s12, "str_they_say_that_s9_has_refused_s11s_suit"),
				(assign, ":last_lady_noted", ":lady"),
				(assign, ":last_suitor_noted", ":suitor"),

			(else_try),

				(troop_slot_eq, "trp_log_array_entry_type",  ":log_entry", logent_lady_rejected_by_suitor),
				(str_store_string, s12, "str_they_say_that_s11_has_tired_of_pursuing_s9"),
				(assign, ":last_lady_noted", ":lady"),
				(assign, ":last_suitor_noted", ":suitor"),


			(else_try),
				(troop_slot_eq, "trp_log_array_entry_type",  ":log_entry", logent_lady_father_rejects_suitor),
				(str_store_string, s12, "str_they_say_that_s9s_family_has_forced_her_to_renounce_s11_whom_she_much_loved"),
				(assign, ":last_lady_noted", ":lady"),
				(assign, ":last_suitor_noted", ":suitor"),

			(else_try),
				(troop_slot_eq, "trp_log_array_entry_type",  ":log_entry", logent_lady_elopes_with_lord),
				(str_store_string, s12, "str_they_say_that_s9_has_run_away_with_s11_causing_her_family_much_grievance"),
				(assign, ":last_lady_noted", ":lady"),
				(assign, ":last_suitor_noted", ":suitor"),

			(else_try),
				(troop_slot_eq, "trp_log_array_entry_type",  ":log_entry", logent_lady_marries_lord),
				(str_store_string, s12, "str_they_say_that_s9_and_s11_have_wed"),
				(assign, ":last_lady_noted", ":lady"),
				(assign, ":last_suitor_noted", ":suitor"),
			(else_try),
				(troop_get_slot, ":suitor", ":lady", slot_lady_last_suitor),
				(is_between, ":suitor", active_npcs_begin, active_npcs_end),
				(str_store_troop_name, s11, ":suitor"),

				(str_store_string, s12, "str_they_say_that_s9_was_recently_visited_by_s11_who_knows_where_that_might_lead"),
				(assign, ":last_lady_noted", ":lady"),
				(assign, ":last_suitor_noted", ":suitor"),
				(try_begin),
					(troop_slot_eq, ":lady", slot_troop_met, 2),
					(this_or_next|troop_slot_eq, ":suitor", slot_troop_love_interest_1, ":lady"),
					(this_or_next|troop_slot_eq, ":suitor", slot_troop_love_interest_2, ":lady"),
						(troop_slot_eq, ":suitor", slot_troop_love_interest_3, ":lady"),

					(assign, "$romantic_rival", ":suitor"),
				(try_end),
			(try_end),

		(try_end),

		(try_begin),
			(neq, ":last_suitor_noted", "$romantic_rival"),
			(assign, "$romantic_rival", -1),
		(try_end),

		(try_begin),
			(gt, ":last_lady_noted", 0),
			(call_script, "script_add_rumor_string_to_troop_notes", ":last_lady_noted", ":last_suitor_noted", 12),
		(try_end),
	(else_try),
		(eq, "$lady_selected", -1),
		(str_store_string, s12, "str_there_is_not_much_to_tell_but_it_is_still_early_in_the_season"),
	(else_try),
		(assign, reg4, "$lady_selected"),
		(str_store_troop_name, s9, "$lady_selected"),
		(str_store_string, s12, "str_error_lady_selected_=_s9"),
	(try_end),
   ],
   "{s12}.",
   "minstrel_postgossip", []],
  [anyone|plyr, "minstrel_postgossip", [],
   "Very interesting -- but let us speak of something else.",
   "minstrel_pretalk", []],
  [anyone|plyr, "minstrel_postgossip", [],
   "Very interesting -- is there any more news?",
   "minstrel_gossip", []],
  [anyone|plyr, "minstrel_postgossip", [
  (is_between, "$romantic_rival", active_npcs_begin, active_npcs_end),
  (neg|check_quest_active, "qst_duel_courtship_rival"),
  (neg|troop_slot_ge, "trp_player", slot_troop_spouse, kingdom_ladies_begin),
  #diplomacy start+ extra check since the wife may be a lord
  (neg|troop_slot_ge, "trp_player", slot_troop_spouse, active_npcs_begin),
  #diplomacy end+
  ],
   "What? I'll make that miscreant face my sword",
   "minstrel_duel_confirm", []],
  [anyone, "minstrel_duel_confirm", [
  (str_store_troop_name, s11, "$romantic_rival"),
  ],
   "Do you mean that? {s11} will be honor-bound to fight you, but challenging a lord to duel over a woman is seen as a bit hot-headed, even in this warlike age.",
   "minstrel_duel_confirm_2", []],
  [anyone|plyr, "minstrel_duel_confirm_2", [
  (str_store_troop_name, s11, "$romantic_rival"),
  (str_store_troop_name, s12, "$lady_selected"),
  ],
   "Yes -- I intend to force {s11} to relinquish his suit of {s12}",
   "minstrel_duel_issued", []],
  [anyone|plyr, "minstrel_duel_confirm_2", [
  ],
   "No -- I let my passions run away with me, there",
   "minstrel_pretalk", []],
  [anyone, "minstrel_duel_issued", [
  ],
   "As you wish. I'll spead the word of your intentions, so that {s13} does not try to back out...",
   "minstrel_pretalk", [
	(str_store_troop_name, s11, "$lady_selected"),
    (str_store_troop_name_link, s13, "$romantic_rival"),
	 ##diplomacy start+ use correct pronoun for gender
	 (call_script, "script_dplmc_store_troop_is_female_reg", "$romantic_rival", 4),
	 ##diplomacy end+
    (str_store_string, s2, "str_you_intend_to_challenge_s13_to_force_him_to_relinquish_his_suit_of_s11"),
    (setup_quest_text, "qst_duel_courtship_rival"),
    (call_script, "script_start_quest", "qst_duel_courtship_rival", "$lady_selected"),
    (quest_set_slot, "qst_duel_courtship_rival", slot_quest_giver_troop, "$lady_selected"),

    (quest_set_slot, "qst_duel_courtship_rival", slot_quest_target_troop, "$romantic_rival"),
    (quest_set_slot, "qst_duel_courtship_rival", slot_quest_xp_reward, 400),
    (quest_set_slot, "qst_duel_courtship_rival", slot_quest_expiration_days, 60),
    (quest_set_slot, "qst_duel_courtship_rival", slot_quest_current_state, 0),
   ]],
  [anyone|plyr, "minstrel_1", [(eq, "$minstrels_introduced", 1)  ],
   "Do you know of any ongoing feasts?",
   "minstrel_courtship_locations", []],
  [anyone, "minstrel_courtship_locations", [

  (str_clear, s12),
  (assign, ":feast_found", 0),
  (try_for_range, ":kingdom", kingdoms_begin, kingdoms_end),
	##zerilius changes begin
	##Bug Fix since they tell about feasts of eliminated kingdoms also.
	(faction_slot_eq, ":kingdom", slot_faction_state, sfs_active),
	##zerilius changes end
	(faction_slot_eq, ":kingdom", slot_faction_ai_state, sfai_feast),
    (assign, ":feast_found", 1),

	(faction_get_slot, ":feast_venue", ":kingdom", slot_faction_ai_object),
	(str_store_party_name, s4, ":feast_venue"),
	(str_store_faction_name, s3, ":kingdom"),

	(store_current_hours, ":hour"),
	(store_sub, ":hours_since_start", ":hour", 72),
	(faction_get_slot, ":feast_time", ":kingdom", slot_faction_last_feast_start_time),
	(val_add, ":hours_since_start", ":feast_time"),

	(try_begin),
		(gt, ":hours_since_start", 48),
		(str_store_string, s12, "str_s12there_is_a_feast_of_the_s3_in_progress_at_s4_but_it_has_been_going_on_for_a_couple_of_days_and_is_about_to_end_"),
	(else_try),
		(gt, ":hours_since_start", 24),
		(str_store_string, s12, "str_s12there_is_a_feast_of_the_s3_in_progress_at_s4_which_should_last_for_at_least_another_day_"),
	(else_try),
		(str_store_string, s12, "str_s12there_is_a_feast_of_the_s3_in_progress_at_s4_which_has_only_just_begun_"),
	(try_end),
  (try_end),

  (try_begin),
    (eq, ":feast_found", 0),
	(str_store_string, s12, "str_not_at_this_time_no"),
  (else_try),
	(str_store_string, s12, "str_s12the_great_lords_bring_their_daughters_and_sisters_to_these_occasions_to_see_and_be_seen_so_they_represent_an_excellent_opportunity_to_make_a_ladys_acquaintance"),
  (try_end),

  ],
   "{s12}",
"minstrel_pretalk", []],
  [anyone|plyr, "minstrel_1", [],
   "Good-bye.", "close_window", []],
  [anyone, "minstrel_courtship_questions", [],
   "What do you wish to know?",
"minstrel_courtship_questions_2", []],
  [anyone, "minstrel_courtship_prequestions", [],
   "Can I answer any other questions for you?",
"minstrel_courtship_questions_2", []],
  [anyone|plyr, "minstrel_courtship_questions_2", [
  (eq, "$minstrels_discussed_love", 1),
  ],
   "Is there a place for me in the game of love?",
   "minstrel_player_role", [
   (assign, "$minstrels_discussed_player_role", 1),
   ]],
  [anyone|plyr, "minstrel_courtship_questions_2", [
   (eq, "$minstrels_discussed_player_role", 1),
  ],
   "How would a suitor meet a lady?",
   "minstrel_player_advice_meet", [
    (assign, "$minstrels_discussed_meetings", 1),
   ]],
  [anyone|plyr, "minstrel_courtship_questions_2", [
   (eq, "$minstrels_discussed_meetings", 1),
  ],
   "Having met a lady, how would the suitor woo her?",
   "minstrel_player_advice_woo", [
   ]],
  [anyone|plyr, "minstrel_courtship_questions_2", [],
   "Tell me about marriage and love among the nobility of Japan",
   "minstrel_nobles", [
   (assign, "$minstrels_discussed_love", 1),
   ]],
  [anyone, "minstrel_nobles", [],
   "Nobles are an odd lot. In Japan, a daughter is a political asset, to be given away to a lord with whom her father wishes to make an alliance. Yet the great families of this land idealize pure love between man and woman, and I have seen many a hardened warrior weep copious tears at the doomed ardour of Sahira and Janun in the songs -- even as he made plans to break his own daughter's heart.",
"minstrel_nobles_2", []],
  [anyone, "minstrel_nobles_2", [],
   "Fathers differ, of course. Some parents will let their daughters choose a husband who pleases them. Others, however, feel that to allow their daughters any choice at all would be to diminish their own authority, and insist on imposing a groom whether she likes it or not.",
"minstrel_nobles_3", []],
  [anyone, "minstrel_nobles_3", [], "But the majority will steer a middle course -- they will want to make the final decision about a groom, but will weigh their daughter's preferences heavily. Among other factors, a happy marriage is more likely to produce heirs. So, there is a place for courtship, and for the use of skill and passion to win a lady's heart.",
"minstrel_prequestions", []],
  [anyone|plyr, "minstrel_courtship_questions_2", [
  (eq, "$minstrels_discussed_love", 1),
  ],
   "What if a lady and her father disagree about a suitor?",
   "minstrel_daughter_father", []],
  [anyone, "minstrel_daughter_father", [], "It happens sometimes that a bride elopes. This is a major blow to the father's prestige, leading to lasting enmities. Indeed, it is possible that a war may be fought over a woman. Now, that is a fine topic for a song.",
   "minstrel_daughter_father_2", []],
  [anyone, "minstrel_daughter_father_2", [], "In the end, however, most brides will submit to their parents' choice. A noblewoman's family is everything to her, and few are brave enough to risk its disapproval for the sake of man she barely knows. She may pine for her lover, but still accept the groom -- and without tragic love, what would we have to sing about?",
   "minstrel_prequestions", []],
   [anyone, "minstrel_player_role", [
   (troop_get_type, ":is_female", "trp_player"),
   (eq, ":is_female", 0),
   ], "Of course! Samurai make a great deal of lineage, but in the end, lands and money speak louder than one's ancestors. Even though you are a foreigner, if you are coming up in the world, then many parents will consider you a fine catch.",
   "minstrel_player_role_2", []],
   [anyone, "minstrel_player_role_2", [
   ], "You will have to compete with many other lords of your domain, however, who will have an advantage -- they have known these ladies from childhood, and will have been sized up as grooms by carefully discerning mothers and aunts. Some ladies may be fascinated by the stranger, yet opt for the familiar.",
   "minstrel_player_role_3", []],
   [anyone, "minstrel_player_role_3", [
   ], "So know this -- you may have your heart broken. But to enter the arena of love fearing heartbreak is like entering the battlefield fearing the enemy's arrows. Be brave, and shrug off the sting of rejection, and victory may yet be yours.",
   "minstrel_prequestions", []],
##diplomacy start+ Make either-gender version, if gender roles are reversed
  [anyone, "minstrel_player_role", [
   ], "{Sir/Lady} -- I will speak bluntly. Most of the {ladies/lords} of this land are looking for a demure {lad/maiden}, whose skin as fair as snow -- and your skin is burnt brown by the sun. They want a {boy/maiden} whose voice is soft as bells -- and your voice is hoarse from commanding {soldiers/men} in battle. Also, athough the {ladies/lords} of Japan appreciate poems about love, most also want heirs, and few {men/women} can ride and fight while {caring for their children/with child}.",
   "minstrel_female_player_3", []],
  [anyone, "minstrel_female_player_3", [
   ], "However, not all {ladies/lords} will be so conventionally minded. We poets sing of shield {boys/maidens} and of {hunters/huntresses}, of {men/women} who forged their own path without having sacrificed the chance for love. I would not tell you that it would be easy for you to find a devoted {wife/husband} who will accept your ways, but I would not say that it is impossible.",
   "minstrel_prequestions", []],
##diplomacy end+

  [anyone|plyr, "minstrel_courtship_questions_2", [
  (eq, "$minstrels_discussed_love", 1),
  ],
   "What advantage is there in seeking a {wife/husband}?",
   "minstrel_spouse_benefits", []],
  [anyone, "minstrel_spouse_benefits", [
  (troop_get_type, ":is_female", "trp_player"),
  (eq, ":is_female", 0),
  ],
   "Ah! You are quite the romantic, I see! Well, aside from the obvious benefits of love, companionship and other, em, domestic matters, to marry among the nobility brings great assets. You may forge a strong alliance with the bride's family, and a wife may also assist you in manipulating the politics of the clan to your advantage.",
   "minstrel_wife_benefits_2", []],
  [anyone, "minstrel_wife_benefits_2", [
  ],
   "What's more, most of the great samurai families of Japan have at some point intermarried with court nobility, which would boost your own claim to rule -- should you ever choose to assert it...",
   "minstrel_prequestions", []],
  [anyone, "minstrel_spouse_benefits", [
  (troop_get_type, ":is_female", "trp_player"),
  (eq, ":is_female", 1),
  ],
   "Ah! You are quite the romantic, I see! Well, aside from the obvious benefits of love, companionship and other, em, domestic matters, to marry among the nobility brings great assets. You may have access to the groom's castles and properties, and be able to work with him to advance both of your standings in the clan.",
   "minstrel_wife_benefits_2", []],
   [anyone, "minstrel_player_advice_meet", [
   ], "Every so often, a samurai lord of Japan will hold a feast. In towns they will often be accompanied by tournaments, and in castles they will be accompanied by hunts. The feasts provide a chance for the lords to repair some of the rivalries that may undermine the strength of the clan. They also provide an opportunity for families to show off their eligible daughters, and ladies will often be allowed to mingle unsupervised with the guests.",
   "minstrel_player_advice_meet_2", []],
   [anyone, "minstrel_player_advice_meet_2", [
   ], "If you have the opportunity, you may attempt to pay the lady a compliment. This indicates to her that you are a potential suitor, and she will usually know if she wishes you to continue your suit. Incidentally, if you come to her fresh from having distinguished yourself in the tournament or in the hunt, then you may make a stronger first impression than otherwise.",
   "minstrel_prequestions", []],
  [anyone, "minstrel_player_advice_woo", [
   ], "To woo a lady takes a certain amount of time and patience, and several meetings spaced over a period of months. A lady who is interested in you will often find ways of letting you know if she wishes you to come visit her. Alternately, you may simply go and ask her father or brother for permission. If you do not have permission from her guardian, it may be possible to arrange an assignation through other means.",
   "minstrel_player_advice_woo_2", []],
  [anyone, "minstrel_player_advice_woo_2", [
   ], "Having arranged an assignment, you may then attempt to charm her and win her favor. Perhaps one of the most difficult aspects of this is finding a topic of conversation. Most Japanese noblewomen lead a cloistered life, at least until they are married, and thus will have little to say that will interest you. On other hand, she will soon tire of hearing of your own deeds in the outside world.",
   "minstrel_player_advice_woo_3", []],
  [anyone, "minstrel_player_advice_woo_3", [
   ], "One time-tested mode of courtship is simply to recite a popular poem, and discuss it. This way, you are both on an equal footing, and neither will have an advantage in knowledge or experience. Of course, different ladies will have different tastes in poetry.",
   "minstrel_player_advice_woo_4", []],
  [anyone, "minstrel_player_advice_woo_4", [
   ], "At some point, you will be able to discuss directly the issue of marriage. She will then let you know if you measure up to what she wants in a husband. Some ladies will coolly assess who is the most prestigious of her suitors, others will be guided by their passions. Some will look to your companions, to see whether you are the kind of husband who will treat her as an equal, while others will follow the lead of their fathers.",
   "minstrel_player_advice_woo_5", []],
  [anyone, "minstrel_player_advice_woo_5", [
   ], "At any rate, it is a challenging business -- and do not forget, you may find that your suit prospers with a lady, only to have it falter on a father's political ambitions. So you must ask yourself: are you willing to risk disappointment and heartbreak? Alternately, are you willing to throw away your standing in society, to make enemies of allies, in pursuit of a forbidden love? Because if you are, then perhaps some day we will write poems about you.",
   "minstrel_prequestions", []],
  [anyone|plyr, "minstrel_courtship_questions_2", [],
   "What is it that you poets and musicians do again?",
   "minstrel_job_description", []],
   [anyone, "minstrel_job_description", [],
   "I compose and write songs for the lords of the land, and their ladies. Sometimes I sing about war, sometimes about the virtues of kings, and sometimes, for the more sophisticated audiences, about the virtues of sake. For most audiences, however, I sing of love.", "minstrel_courtship_prequestions", []],
  [anyone|plyr, "minstrel_courtship_questions_2", [],
   "No, that is all.",
   "minstrel_pretalk", []],
  [anyone, "minstrel_prequestions", [
   ], "Do you have any other questions?",
   "minstrel_courtship_questions_2", []],
  [anyone, "minstrel_pretalk", [],
   "Is there anything else?",
   "minstrel_1", []],
##diplomacy start+
##Tavern Talk (with farmers)
##Alternate opening lines when the farmer should know who the player is.
  [anyone, "start", [(eq, "$talk_context", tc_tavern_talk),
                     (eq, "$g_talk_troop", "trp_farmer_from_bandit_village"),
                     (neg|check_quest_active, "qst_eliminate_bandits_infesting_village"),
                     (neg|check_quest_active, "qst_deal_with_bandits_at_lords_village"),
                     (assign, ":end_cond", villages_end),
                     (try_for_range, ":cur_village", villages_begin, ":end_cond"),
                       (party_slot_eq, ":cur_village", slot_village_bound_center, "$g_encountered_party"),
                       (party_slot_ge, ":cur_village", slot_village_infested_by_bandits, 1),
                       (neg|party_slot_eq, ":cur_village", slot_village_infested_by_bandits, "trp_peasant_woman"),#not insurrection
                       (str_store_party_name, s1, ":cur_village"),
                       (quest_set_slot, "qst_eliminate_bandits_infesting_village", slot_quest_target_center, ":cur_village"),
                       (quest_set_slot, "qst_eliminate_bandits_infesting_village", slot_quest_current_state, 0),
                       (party_get_slot, ":village_elder", ":cur_village", slot_town_elder),
                       (quest_set_slot, "qst_eliminate_bandits_infesting_village", slot_quest_giver_troop, ":village_elder"),
                       (quest_set_slot, "qst_eliminate_bandits_infesting_village", slot_quest_giver_center, ":cur_village"),
                       (assign, ":end_cond", 0),
                     (try_end),
                    #Player is a lord in this kingdom, or a notable lord is his own kingdom
                    (call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", "$g_encountered_party_faction"),
                    (this_or_next|gt, reg0, DPLMC_FACTION_STANDING_MEMBER),#i.e. not just a mercenary
                       (troop_slot_ge, "trp_player", slot_troop_renown, 600),

                     (assign, "$temp", ":cur_village"),#Save the village for later use in the conversation
                     (assign, "$temp_2", 1),#Player is famous

							(call_script, "script_dplmc_print_commoner_at_arg1_says_sir_madame_to_s0", "$g_encountered_party"),
							(val_sub, reg0, 2),
							(val_max, reg0, 0),#i.e. only non-zero if >= 3
							(str_clear, s0),
                     ],
   "{reg0?Your highness:My {lord/lady}}, we are in dire need of assistance.  Will you hear my plea?", "farmer_from_bandit_village_1", []],
##diplomacy end+
#Tavern Talk (with farmers)
  [anyone, "start", [(eq, "$talk_context", tc_tavern_talk),
                     (eq, "$g_talk_troop", "trp_farmer_from_bandit_village"),
                     (neg|check_quest_active, "qst_eliminate_bandits_infesting_village"),
                     (neg|check_quest_active, "qst_deal_with_bandits_at_lords_village"),
                     (assign, ":end_cond", villages_end),
                     (try_for_range, ":cur_village", villages_begin, ":end_cond"),
                       (party_slot_eq, ":cur_village", slot_village_bound_center, "$g_encountered_party"),
                       (party_slot_ge, ":cur_village", slot_village_infested_by_bandits, 1),
                       ##diplomacy begin
                       (neg|party_slot_eq, ":cur_village", slot_village_infested_by_bandits, "trp_peasant_woman"),
                       ##diplomacy_end
                       (str_store_party_name, s1, ":cur_village"),
                       (quest_set_slot, "qst_eliminate_bandits_infesting_village", slot_quest_target_center, ":cur_village"),
                       (quest_set_slot, "qst_eliminate_bandits_infesting_village", slot_quest_current_state, 0),
                       (party_get_slot, ":village_elder", ":cur_village", slot_town_elder),
                       (quest_set_slot, "qst_eliminate_bandits_infesting_village", slot_quest_giver_troop, ":village_elder"),
                       (quest_set_slot, "qst_eliminate_bandits_infesting_village", slot_quest_giver_center, ":cur_village"),
                       (assign, ":end_cond", 0),
                     (try_end),
                     ##diplomacy start+ Save the village for use later in the conversation
                     (assign, "$temp", ":cur_village"),
                     (assign, "$temp_2", 1),#player is not a lord of this faction or a well-known lord of another faction
                     ##diplomacy end+
                     ],
   "{My lord/Madam}, you look like a {man/lady} of the sword and someone who could help us.\
 Will you hear my plea?", "farmer_from_bandit_village_1", []],
  [anyone|plyr, "farmer_from_bandit_village_1", [
  ##diplomacy start+ either gender
  ],# "man" -> "{reg65?woman:man}"
   "What is the matter, my good {reg65?woman:man}?", "farmer_from_bandit_village_2", []],
   ##diplomacy end+

   [anyone|plyr, "farmer_from_bandit_village_1", [],
   "What are you burbling about peasant? Speak out.", "farmer_from_bandit_village_2", []],
##diplomacy start+
##Add this if the lord is the player, to skip the "why don't you ask your lord?" line.
  [anyone, "farmer_from_bandit_village_2", [
   (assign, ":lord_is_player", 0),
   (try_begin),
      (party_slot_eq, "$temp", slot_town_lord, "trp_player"),
      (store_faction_of_party, ":village_faction", "$temp"),
      (this_or_next|eq, ":village_faction", "$players_kingdom"),
         (eq, ":village_faction", "fac_player_supporters_faction"),
      (assign, ":lord_is_player", 1),
   (try_end),
   (neq, ":lord_is_player", 0),

  (call_script, "script_dplmc_print_subordinate_says_sir_madame_to_s0"),
  ],
   "A band of brigands have taken refuge in our village. They take everything we have, force us to serve them, and do us much evil.\
 If one of us so much as breathes a word of protest, they kill the poor soul on the spot right away.\
 Our lives have become unbearable. I risked my skin and ran away to find someone who can help us.\
 Please {s0}, you are a {man/lady} of valor and a fearsome warrior, with many friends and soldiers at your service.\
 If there is anyone who can help us, it's you.", "farmer_from_bandit_village_5", [(assign, "$temp", 0)]],
##diplomacy end+

  [anyone, "farmer_from_bandit_village_2", [],
   "A band of brigands have taken refuge in our village. They take everything we have, force us to serve them, and do us much evil.\
 If one of us so much as breathes a word of protest, they kill the poor soul on the spot right away.\
 Our lives have become unbearable. I risked my skin and ran away to find someone who can help us.", "farmer_from_bandit_village_3", []],
##diplomacy start+
## If the town has a lord that the player has met, use the correct gender.
#  [anyone|plyr, "farmer_from_bandit_village_3", []
#   "Why don't you go to the lord of your village? He should take care of the vermin.", "farmer_from_bandit_village_4", []],
  [anyone|plyr, "farmer_from_bandit_village_3", [
     (assign, reg0, 0),
	  (try_begin),
	     (gt, "$temp", 1),
		  (party_slot_ge, "$temp", slot_town_lord, 1),
		  (party_get_slot, ":town_lord", "$temp", slot_town_lord),
		  (troop_slot_ge, ":town_lord", slot_troop_met, 1),
		  (call_script, "script_dplmc_store_troop_is_female", ":town_lord"),
	  (try_end),
  ],
   "Why don't you go to the {reg0?mistress:lord} of your village? {reg0?She:He} should take care of the vermin.", "farmer_from_bandit_village_4", []],
##Different line if the village lord is in captivity
  [anyone, "farmer_from_bandit_village_4", [
  (gt, "$temp", 1),
  (party_slot_ge, "$temp", slot_town_lord, 1),
  (party_get_slot, ":town_lord", "$temp", slot_town_lord),
  (troop_slot_ge, ":town_lord", slot_troop_prisoner_of_party, 0),
  (call_script, "script_dplmc_print_commoner_at_arg1_says_sir_madame_to_s0", "$g_encountered_party"),
  (call_script, "script_dplmc_store_troop_is_female", ":town_lord"),
  (assign, reg1, "$temp_2"),
  ],
   "Our {reg0?lady:lord} is imprisoned, so we cannot go to {reg0?her:him} for protection.\
 Please {s0}, you {reg1?are:look like} a {man/lady} of valor, {reg1?with:and you have no doubt} many friends and soldiers at your service. \
 If there is anyone who can help us, it's you.", "farmer_from_bandit_village_5", [(assign, "$temp", 0)]],
##Different line if the village has no lord
  [anyone, "farmer_from_bandit_village_4", [
  (gt, "$temp", 1),
  (neg|party_slot_ge, "$temp", slot_town_lord, 1),
  (call_script, "script_dplmc_print_commoner_at_arg1_says_sir_madame_to_s0", "$g_encountered_party"),
  (assign, reg1, "$temp_2"),
  ],
   "We have no lord, so we cannot go to him for protection.\
 Please {s0}, you {reg1?are:look like} a {man/lady} of valor, {reg1?with:and you have no doubt} many friends and soldiers at your service. \
 If there is anyone who can help us, it's you.", "farmer_from_bandit_village_5", [(assign, "$temp", 0)]],
##Alter the default line to be different when the player is recognized
  [anyone, "farmer_from_bandit_village_4", [
  (call_script, "script_dplmc_print_commoner_at_arg1_says_sir_madame_to_s0", "$g_encountered_party"),
  (party_get_slot, ":town_lord", "$temp", slot_town_lord),
  (call_script, "script_dplmc_store_troop_is_female", ":town_lord"),
  (assign, reg1, "$temp_2"),
  ],
   "I did, {s0}, but our {reg0?lady:lord}'s {reg0?servants:men} did not let me see {reg0?her:him} and said {reg0?she:he} was occupied with more important matters and that we should deal with our own problem ourselves.\
 Please {s0}, you {reg1?are:look like} a {man/lady} of valor and a fearsome warrior, {reg1?with:and you have no doubt} many friends and soldiers at your service. \
 If there is anyone who can help us, it's you.", "farmer_from_bandit_village_5", [(assign, "$temp", 0)]],
##diplomacy end+

  [anyone|plyr, "farmer_from_bandit_village_5", [],
   "Very well, I'll help you. Where is this village?", "farmer_from_bandit_village_accepted", []],
  [anyone|plyr, "farmer_from_bandit_village_5", [],
   "I can't be bothered with this right now.", "farmer_from_bandit_village_denied", []],
  [anyone|plyr, "farmer_from_bandit_village_5", [(eq, "$temp", 0)],
   "Why would I fight these bandits? What's in it for me?", "farmer_from_bandit_village_barter", []],
  [anyone, "farmer_from_bandit_village_accepted", [##diplomacy start+
    (call_script, "script_dplmc_print_commoner_at_arg1_says_sir_madame_to_s0", "$g_encountered_party"),
  ],#Next line, replace {sir/madam} with {s0}
   #"God bless you, {sir/madam}. Our village is {s7}. It is not too far from here.", "close_window",
   "God bless you, {s0}. Our village is {s7}. It is not too far from here.", "close_window",
   ##diplomacy end+
   [(quest_get_slot, ":target_center", "qst_eliminate_bandits_infesting_village", slot_quest_target_center),
    (str_store_party_name_link,s7,":target_center"),
    (setup_quest_text, "qst_eliminate_bandits_infesting_village"),
    (str_store_string, s2, "@A villager from {s7} begged you to save their village from the bandits that took refuge there."),
    (call_script, "script_start_quest", "qst_eliminate_bandits_infesting_village", "$g_talk_troop"),
    ]],
  [anyone, "farmer_from_bandit_village_denied", [],"As you say {sir/madam}. Forgive me for bothering you.", "close_window", []],
  [anyone, "farmer_from_bandit_village_barter", [##diplomacy start+
  (call_script, "script_dplmc_print_commoner_at_arg1_says_sir_madame_to_s0", "$g_encountered_party"),
    ],#Next line, replace {sir/madam} with {s0}
   "We are but poor farmers {s0}, and the bandits have already got most of what we have on this world.\
 but we'll be glad to share with you whatever we have got.\
 And we'll always be in your gratitude if you help us.", "farmer_from_bandit_village_5", [(assign, "$temp", 1)]],
##diplomacy end+

  [anyone, "start", [(eq, "$talk_context", tc_tavern_talk),
                     (eq, "$g_talk_troop", "trp_farmer_from_bandit_village"),
                     (check_quest_active, "qst_eliminate_bandits_infesting_village"),
    ##diplomacy start+
    ##OLD:
    #                 ],
    #"Thank you for helping us {sir/madam}. Crush those bandits!", "close_window", []],
    ##NEW:
                     (call_script, "script_dplmc_print_commoner_at_arg1_says_sir_madame_to_s0", "$g_encountered_party"),
                      ],
    "Thank you for helping us {s0}. Crush those bandits!", "close_window", []],
    ##diplomacy end+


#Tavern Talk (with troops)

  [anyone, "start", [
                     (eq, "$talk_context", tc_tavern_talk),
					 (neg|troop_is_hero, "$g_talk_troop"),
                     (neg|is_between, "$g_talk_troop", "trp_tsu_merchant", "trp_startup_merchants_end"),
                     (party_get_slot, ":mercenary_troop", "$g_encountered_party", slot_center_mercenary_troop_type),
                     (party_get_slot, ":mercenary_amount", "$g_encountered_party", slot_center_mercenary_troop_amount),
					 #gekokujo ninja bodyguards start
					 #prevent hiring mercs through a ninja bodyguard unless the merc type is also a ninja
					 (eq, "$g_talk_troop", ":mercenary_troop"),
					 #gekokujo ninja bodyguards end
                     (gt, ":mercenary_amount", 0),
                     (store_sub, reg3, ":mercenary_amount", 1),
                     (store_sub, reg4, reg3, 1),
                     (call_script, "script_game_get_join_cost", ":mercenary_troop"),
                     (assign, ":join_cost", reg0),
                     (store_mul, reg5, ":mercenary_amount", reg0),
                     (party_get_free_companions_capacity, ":free_capacity", "p_main_party"),
                     (val_min, ":mercenary_amount", ":free_capacity"),
                     (store_troop_gold, ":cur_gold", "trp_player"),
                     (try_begin),
                       (gt, ":join_cost", 0),
                       (val_div, ":cur_gold", ":join_cost"),
                       (val_min, ":mercenary_amount", ":cur_gold"),
                     (try_end),
                     (assign, "$temp", ":mercenary_amount"),
					 #gekokujo ninja bodyguards start
					 #prevent weird language if hiring an agent through a bodyguard
					 (try_begin),
					   (this_or_next|eq, "$g_talk_troop", "trp_hired_agent"),
					   (eq, "$g_talk_troop", "trp_hired_agent_experienced"),
					   (main_party_has_troop, "$g_talk_troop"),
					   (str_store_string, s11, "@Do you have a need for more agents, {sir/madam}? {reg3?{reg4} of my comrades are:One of my comrades is} looking for a master. {reg3?They'll:He'll} join you for {reg5} mon."),
					 (else_try),
					   (str_store_string, s11, "@Do you have a need for mercenaries, {sir/madam}? {reg3?Me and {reg4?{reg3} of my comrades:one of my comrades} are:I am} looking for a master. We'll join you for {reg5} mon."),
					 (try_end),
                     ], "{s11}", "mercenary_tavern_talk", []],
#                     ],
#   "Do you have a need for mercenaries, {sir/madam}?\
# {reg3?Me and {reg4?{reg3} of my comrades:one of my comrades} are:I am} looking for a master.\
# We'll join you for {reg5} mon.", "mercenary_tavern_talk", []],
#gekokujo ninja bodyguards end

  [anyone, "start", [
  (eq, "$talk_context", tc_tavern_talk),
  ],
   "Any orders, {sir/madam}?", "mercenary_after_recruited", []],
#Trainers
  [anyone,"start", [(is_between, "$g_talk_troop", training_gound_trainers_begin, training_gound_trainers_end),
                    (eq, "$g_talk_troop_met", 0)],
   "Good day to you {lad/lass}. You look like another adventurer who has come to try {his/her} chance in these lands.\
 Well, trust my word, you won't be able to survive long here unless you know how to fight yourself out of a tight spot.", "trainer_intro_1",[]],
 [anyone,"start", [(is_between, "$g_talk_troop", training_gound_trainers_begin, training_gound_trainers_end),
                   (neq,"$waiting_for_training_fight_result", 0),
                   (neq,"$training_fight_won", 0)],
 "That was a good fight. ", "trainer_practice_1",
  [(val_sub, "$num_opponents_to_beat_in_a_row", 1),
   (assign,"$waiting_for_training_fight_result",0),
   ]],
  [anyone,"start", [(is_between, "$g_talk_troop", training_gound_trainers_begin, training_gound_trainers_end),
                    (neq, "$waiting_for_training_fight_result", 0)],
 "Ha! Looks like you've developed a bit of a limp there. Don't worry, even losses have their value, provided you learn from them. Shake the stars out of your eyes and get back in there. There's no other way to win.", "trainer_practice_1",
   [(assign,"$num_opponents_to_beat_in_a_row",3),(assign,"$waiting_for_training_fight_result",0)]],
    [anyone,"start", [(is_between, "$g_talk_troop", training_gound_trainers_begin, training_gound_trainers_end)],
   "Good day. Ready for some training today?", "trainer_talk",[]],
  [anyone|plyr,"novicemaster_finish_training", [], "Thank you master.", "novicemaster_finish_training_2",[]],
  [anyone,"novicemaster_finish_training_2", [], "I wish you good luck in the tournaments. And, don't forget,\
  if you want to practice your swordwork anytime, just come and say the word.", "close_window",[]],
  [anyone|plyr,"novicemaster_are_you_ready", [], "Yes I am.", "novicemaster_ready_to_fight",[]],
  [anyone,"novicemaster_ready_to_fight", [], "Here you go then. Good luck.", "close_window",
   [
     (assign, "$training_fight_won", 0),
     (assign, "$waiting_for_training_fight_result", 1),
     (modify_visitors_at_site, "$g_training_ground_melee_training_scene"),
     (reset_visitors),
     (assign, reg0, 0),
     (assign, reg1, 1),
     (assign, reg2, 2),
     (assign, reg3, 3),
     (shuffle_range, 0, 4),
     (set_visitor, reg0, "trp_player"),
     (set_visitor, reg1, "$novicemaster_opponent_troop"),
     (set_visitor, 4, "$g_talk_troop"),
     (set_jump_mission, "mt_training_ground_trainer_training"),
     (jump_to_scene, "$g_training_ground_melee_training_scene"),
     ]],
  [anyone|plyr,"novicemaster_are_you_ready", [], "Just a minute. I am not ready yet.", "novicemaster_not_ready",[]],
  [anyone,"novicemaster_not_ready", [], "Hey, You will never make it if you don't practice.", "close_window",[]],
#Crooks

##  [anyone ,"start", [(is_between,"$g_talk_troop",crooks_begin,crooks_end),(eq,"$g_talk_troop_met",0),(eq,"$sneaked_into_town",0),(store_random_in_range, reg2, 2)],
##   "You {reg2?looking for:want} something?:", "crook_intro_1",[]],
##  [anyone|plyr,"crook_intro_1",[],"I am trying to learn my way around the town.", "crook_intro_2",[]],
##
##  [anyone,"crook_intro_2",[(eq,"$crook_talk_order",0),(val_add,"$crook_talk_order",1),(str_store_troop_name,s1,"$g_talk_troop")],
##"Then you came to the right guy. My name is {s1}, and I know everyone and everything that goes around in this town.\
## Anyone you want to meet, I can arrange it. Anything you need to know, I can find out. For the the right price, of course. Do you have gold?", "crook_intro_2a",[]],
##  [anyone|plyr,"crook_intro_2a",[],"I have gold. Plenty of it.", "crook_intro_2a_1a",[]],
##  [anyone|plyr,"crook_intro_2a",[],"Not really.", "crook_intro_2a_1b",[]],
##  [anyone,"crook_intro_2a_1a",[],"Good. That means you and I will be great friends.", "crook_talk",[]],
##  [anyone,"crook_intro_2a_1b",[],"Then you should look into earning some. Listen to me now, for I'll give you some free advice.\
## The easiest way to make money is to fight in the tournaments and bet on yourself. If you are good, you'll quickly get yourself enough money to get going.", "crook_talk",[]],
##
##  [anyone,"crook_intro_2",[(eq,"$crook_talk_order",1),(val_add,"$crook_talk_order",1),(str_store_troop_name,s1,"$g_talk_troop")],
##"Then you need to go no further. I am {s1}, and I can provide you anything... For the the right price.", "crook_intro_2b",[]],
##  [anyone|plyr,"crook_intro_2b",[],"Are you a dealer?", "crook_intro_2b_1",[]],
##  [anyone,"crook_intro_2b_1",[],"A dealer? Yes. I deal in knowledge... connections.. lies... secrets... Those are what I deal in. Interested?", "crook_talk",[]],
##
##  [anyone,"crook_intro_2",[(eq,"$crook_talk_order",2),(val_add,"$crook_talk_order",1),(str_store_troop_name,s1,"$g_talk_troop")],
##"Then this is your lucky day. Because you are talking to {s1}, and I know every piss-stained brick of this wicked town.\
##I know every person, every dirty little secret. And all that knowledge can be yours. For a price.", "crook_talk",[]],
##
##  [anyone,"crook_intro_2",[(val_add,"$crook_talk_order",1),(str_store_troop_name,s1,"$g_talk_troop")],
## "Then {s1} is at your service {sir/madam}. If you want to know what's really going on in this town, or arrange a meeting in secret, then come to me. I can help you.", "crook_talk",[]],
##
##  [anyone ,"start", [(is_between,"$g_talk_troop",crooks_begin,crooks_end),(eq,"$g_talk_troop_met",0),(eq,"$sneaked_into_town",1),(eq,"$crook_sneak_intro_order",0),(val_add,"$crook_sneak_intro_order",1)],
##   "Good day. {playername} right?", "crook_intro_sneak_1",[]],
##  [anyone|plyr,"crook_intro_sneak_1", [], "You must be mistaken. I'm just a poor pilgrim. I don't answer to that name.", "crook_intro_sneak_2",[]],
##  [anyone,"crook_intro_sneak_2", [(str_store_troop_name,s1,"$g_talk_troop")], "Of course you do. And if the town guards knew you were here, they'd be upon you this minute.\
## But don't worry. Noone knows it is {playername} under that hood. Except me of course. But I am {s1}. It is my business to know things.", "crook_intro_sneak_3",[]],
##  [anyone|plyr,"crook_intro_sneak_3", [], "You won't tip off the guards about my presence?", "crook_intro_sneak_4",[]],
##  [anyone,"crook_intro_sneak_4", [], "What? Of course not! Well, maybe I would, but the new captain of the guards is a dung-eating cheat.\
## I led him to this fugitive, and the man was worth his weight in silver as prize money. But I swear, I didn't see a penny of it.\
## The bastard took it all to himself. So your secret is safe with me.", "crook_intro_sneak_5",[]],
##  [anyone,"crook_intro_sneak_5", [], "Besides, I heard you have a talent for surviving any kind of ordeal.\
## I wouldn't want you to survive this one as well and then come after me with a sword. Ha-hah.", "crook_talk",[]],
##
##
##  [anyone ,"start", [(is_between,"$g_talk_troop",crooks_begin,crooks_end),(eq,"$g_talk_troop_met",0),(eq,"$sneaked_into_town",1),(str_store_troop_name,s1,"$g_talk_troop")],
##   "{s1} is at your service {sir/madam}. If you want to know what's really going on in this town, or arrange a meeting in secret, then come to me. I can help you.", "crook_talk",[]],
##
##  [anyone ,"start", [(is_between,"$g_talk_troop",crooks_begin,crooks_end),(store_character_level, ":cur_level", "trp_player"),(lt,":cur_level",8)],
##   "{You again?/Delighted to see you again my pretty.}", "crook_talk",[]],
##  [anyone ,"start", [(is_between,"$g_talk_troop",crooks_begin,crooks_end)],
##   "I see that you need my services {sir/madam}...", "crook_talk",[]],
##  [anyone ,"crook_pretalk", [],
##   "Is that all?", "crook_talk",[]],



##  [anyone|plyr,"crook_talk", [], "I'm looking for a person...", "crook_search_person",[]],
##  [anyone|plyr,"crook_talk", [], "I want you to arrange me a meeting with someone...", "crook_request_meeting",[]],
##  [anyone|plyr,"crook_talk", [], "[Leave]", "close_window",[]],



#  [anyone,"crook_enter_dungeon", [],
#   "Alright but this will cost you 50 mon.", "crook_enter_dungeon_2", []],

#  [anyone|plyr, "crook_enter_dungeon_2", [(store_troop_gold, ":cur_gold", "trp_player"),
#                                            (ge, ":cur_gold", 50)],
#   "TODO: Here it is. 50 mon.", "crook_enter_dungeon_3_1",[(troop_remove_gold, "trp_player", 50)]],

#  [anyone|plyr, "crook_enter_dungeon_2", [(store_troop_gold, ":cur_gold", "trp_player"),
#                                            (ge, ":cur_gold", 50)],
#   "Never mind then.", "crook_pretalk",[]],

#  [anyone|plyr, "crook_enter_dungeon_2", [(store_troop_gold, ":cur_gold", "trp_player"),
#                                            (lt, ":cur_gold", 50)],
#   "TODO: I don't have that much money.", "crook_enter_dungeon_3_2",[]],

#  [anyone,"crook_enter_dungeon_3_1", [],
#   "TODO: There you go.", "close_window", [(call_script, "script_enter_dungeon", "$current_town", "mt_visit_town_castle")]],

#  [anyone,"crook_enter_dungeon_3_2", [],
#   "TODO: Come back later then.", "crook_pretalk",[]],


##  [anyone, "crook_request_meeting", [],
##   "Who do you want to meet with?", "crook_request_meeting_2",[]],
##  [anyone|plyr|repeat_for_troops,"crook_request_meeting_2", [(store_encountered_party, ":center_no"),
##                                                             (store_repeat_object, ":troop_no"),
##                                                             (is_between, ":troop_no", heroes_begin, heroes_end),
##                                                             (troop_get_slot, ":cur_center", ":troop_no", slot_troop_cur_center),
##                                                             (call_script, "script_get_troop_attached_party", ":troop_no"),
##                                                             (assign, ":cur_center_2", reg0),
##                                                             (this_or_next|eq, ":cur_center", ":center_no"),
##                                                             (eq, ":cur_center_2", ":center_no"),
##                                                             (neg|party_slot_eq, ":center_no", slot_town_lord, ":troop_no"),#Neglect the ruler of the center
##                                                             (str_store_troop_name, s1, ":troop_no")],
##   "{s1}", "crook_request_meeting_3", [(store_repeat_object, "$selected_troop")]],
##
##  [anyone|plyr,"crook_request_meeting_2", [], "Never mind.", "crook_pretalk", []],
##
##  [anyone,"crook_request_meeting_3", [],
##   "Alright but this will cost you 50 mon.", "crook_request_meeting_4", []],
##
##  [anyone|plyr, "crook_request_meeting_4", [(store_troop_gold, ":cur_gold", "trp_player"),
##                                            (ge, ":cur_gold", 50)],
##   "TODO: Here it is. 50 mon.", "crook_search_person_5_1",[(troop_remove_gold, "trp_player", 50)]],
##
##  [anyone|plyr, "crook_request_meeting_4", [(store_troop_gold, ":cur_gold", "trp_player"),
##                                            (ge, ":cur_gold", 50)],
##   "Never mind then.", "crook_pretalk",[]],
##
##  [anyone|plyr, "crook_request_meeting_4", [(store_troop_gold, ":cur_gold", "trp_player"),
##                                            (lt, ":cur_gold", 50)],
##   "TODO: I don't have that much money.", "crook_search_person_5_2",[]],
##
##  [anyone, "crook_search_person_5_1", [],
##   "TODO: Ok.", "close_window",[(party_get_slot, ":town_alley", "$g_encountered_party", slot_town_alley),
##                                (modify_visitors_at_site,":town_alley"),(reset_visitors),
##                                (set_visitor,0,"trp_player"),
##                                (set_visitor,17,"$selected_troop"),
##                                (set_jump_mission,"mt_conversation_encounter"),
##                                (jump_to_scene,":town_alley"),
##                                (assign, "$talk_context", tc_back_alley),
##                                (change_screen_map_conversation, "$selected_troop")]],
##
##  [anyone, "crook_search_person_5_2", [],
##   "TODO: Come back later then.", "crook_pretalk",[]],
##
##  [anyone, "crook_search_person", [],
##   "TODO: Who are you searching for?", "crook_search_person_2",[]],
##  [anyone|plyr|repeat_for_factions,"crook_search_person_2", [(store_repeat_object, ":faction_no"),
##                                                             (is_between, ":faction_no", kingdoms_begin, kingdoms_end),
##                                                             (str_store_faction_name, s1, ":faction_no")],
##   "TODO: I'm looking for a {s1}.", "crook_search_person_3", [(store_repeat_object, "$selected_faction")]],
##
##  [anyone|plyr,"crook_search_person_2", [], "Never mind.", "crook_pretalk", []],
##
##
##  [anyone, "crook_search_person_3", [],
##   "TODO: Who?", "crook_search_person_4",[]],
##
##  [anyone|plyr|repeat_for_troops,"crook_search_person_4", [(store_repeat_object, ":troop_no"),
##                                                           (is_between, ":troop_no", heroes_begin, heroes_end),
##                                                           (store_troop_faction, ":faction_no", ":troop_no"),
##                                                           (eq, ":faction_no", "$selected_faction"),
##                                                           (str_store_troop_name, s1, ":troop_no")],
##   "{s1}", "crook_search_person_5", [(store_repeat_object, "$selected_troop")]],
##
##  [anyone|plyr,"crook_search_person_4", [], "Never mind.", "crook_pretalk", []],
##
##  [anyone, "crook_search_person_5", [(call_script, "script_get_information_about_troops_position", "$selected_troop", 0),
##                                     (eq, reg0, 1),
##                                     (str_store_troop_name, s1, "$selected_troop")],
##   "TODO: I know where {s1} is at the moment, but hearing it will cost you 50 mon.", "crook_search_person_6",[]],
##
##  [anyone, "crook_search_person_5", [],
##   "TODO: Sorry I don't know anything.", "crook_pretalk",[]],
##
##  [anyone|plyr, "crook_search_person_6", [(store_troop_gold, ":cur_gold", "trp_player"),
##                                          (ge, ":cur_gold", 50)],
##   "TODO: Here it is. 50 mon.", "crook_search_person_7_1",[(troop_remove_gold, "trp_player", 50)]],
##
##  [anyone|plyr, "crook_search_person_6", [(store_troop_gold, ":cur_gold", "trp_player"),
##                                          (ge, ":cur_gold", 50)],
##   "Never mind then.", "crook_pretalk",[]],
##
##  [anyone|plyr, "crook_search_person_6", [(store_troop_gold, ":cur_gold", "trp_player"),
##                                          (lt, ":cur_gold", 50)],
##   "TODO: I don't have that much money.", "crook_search_person_7_2",[]],
##
##  [anyone, "crook_search_person_7_1", [(call_script, "script_get_information_about_troops_position", "$selected_troop", 0)],
##   "{s1}", "crook_pretalk",[]],
##
##  [anyone, "crook_search_person_7_2", [],
##   "TODO: Come back later then.", "crook_pretalk",[]],
##

  [anyone|auto_proceed,"start", [
  (is_between,"$g_talk_troop","trp_town_1_master_craftsman", "trp_zendar_chest"),
  (party_get_slot, ":days_until_complete", "$g_encountered_party", slot_center_player_enterprise_days_until_complete),
  (ge, ":days_until_complete", 2),
  (assign, reg4, ":days_until_complete"),
  ],
   "{!}.", "start_craftsman_soon",[]],
  [anyone,"start_craftsman_soon", [
  ],
   "Good day, my {lord/lady}. We hope to begin production in about {reg4} days", "close_window",[]],
  [anyone,"start", [
  (is_between,"$g_talk_troop","trp_town_1_master_craftsman", "trp_zendar_chest"),
  ],
   "Good day, my {lord/lady}. We are honored that you have chosen to visit us. What do you require?", "master_craftsman_talk",[]],
#Mayor talk (town elder)

  [anyone ,"start", [(is_between,"$g_talk_troop",mayors_begin,mayors_end),(eq,"$g_talk_troop_met",0),
                     (this_or_next|eq, "$players_kingdom", "$g_encountered_party_faction"),
                     (             eq, "$g_encountered_party_faction", "fac_player_supporters_faction"),
					 ##diplomacy start+
					 #Change "my lord" to "my lord/my lady" or "your highnes" as appropriate.
					 (call_script, "script_dplmc_print_subordinate_says_sir_madame_to_s0"),#Write {sir/madame} or replacement to {s0}
					 ],
   "Good day, {s0}.", "mayor_begin",[]],
#Changed "my lord" to {s0}
   ##diplomacy end+
  [anyone ,"start", [(is_between,"$g_talk_troop",mayors_begin,mayors_end),(eq,"$g_talk_troop_met",0),
                     (str_store_party_name, s9, "$current_town")],
   "Hello stranger, you seem to be new to {s9}. I am the elder amongst the merchants and artisans of the town.", "mayor_talk",[]],
  [anyone ,"start", [(is_between,"$g_talk_troop",mayors_begin,mayors_end)],
   "Good day, {playername}.", "mayor_begin",
   [
     #Delete last offered quest if peace is formed.
     (try_begin),
       (eq, "$merchant_offered_quest", "qst_persuade_lords_to_make_peace"),
       (party_get_slot, ":target_faction", "qst_persuade_lords_to_make_peace", slot_quest_target_faction),
       (party_get_slot, ":object_faction", "qst_persuade_lords_to_make_peace", slot_quest_object_faction),
       (store_relation, ":reln", ":target_faction", ":object_faction"),
       (ge, ":reln", 0),
       (assign, "$merchant_quest_last_offerer", -1),
       (assign, "$merchant_offered_quest", -1),
     (try_end),
     ]],
  [anyone|plyr ,"move_cattle_herd_failed", [],
   "I am sorry. But I was attacked on the way.", "move_cattle_herd_failed_2",[]],
  [anyone|plyr ,"move_cattle_herd_failed", [],
   "I am sorry. The stupid animals wandered off during the night.", "move_cattle_herd_failed_2",[]],
  [anyone,"move_cattle_herd_failed_2", [],
   "Well, it was your responsibility to deliver that herd safely, no matter what.\
 You should know that the owner of the herd demanded to be compensated for his loss, and I had to pay him 1000 mon.\
 So you now owe me that money.", "merchant_ask_for_debts",
   [(assign, "$debt_to_merchants_guild", 1000),
    (call_script, "script_end_quest", "qst_move_cattle_herd"),]],
  [anyone,"destroy_lair_quest_brief", [
     (eq,"$random_quest_no", "qst_destroy_bandit_lair"),
	 (quest_get_slot, ":bandit_lair", "qst_destroy_bandit_lair", slot_quest_target_party),
	 (party_get_template_id, ":bandit_type", ":bandit_lair"),
	 (eq, ":bandit_type", "pt_kinai_rebel_lair"),
	 ],
	#gekokujo "sea raiders" now get mountain hideout
	#"The raiders are likely to have laid up their ships in a well-concealed cove, somewhere along the coastline, preferably next to a small stream where they have some water. The best way to discover its location would be to find a group of sea raiders who appear to be heading back to their base to resupply, and follow them.", "merchant_quest_track_bandit_lair_choice",
	"Bandits such as these will usually operate from mansions in the countryside. The best way to discover its location would be to find a group of rebels who appear to be heading home to resupply, and follow them.", "merchant_quest_track_bandit_lair_choice",
   []],
  [anyone,"destroy_lair_quest_brief", [
     (eq,"$random_quest_no", "qst_destroy_bandit_lair"),
	 (quest_get_slot, ":bandit_lair", "qst_destroy_bandit_lair", slot_quest_target_party),
	 (party_get_template_id, ":bandit_type", ":bandit_lair"),
	 (eq, ":bandit_type", "pt_northern_raider_lair"),
	 ],
	#desert bandits now get forest hideout
	#"Bandits such as these usually establish their hideouts in the foothills on the edge of the desert, often in a canyon near a spring. This gives them both water and concealment. The best way to discover its location would be to find a group of desert bandits who appear to be heading back to their base to resupply, and follow them.", "merchant_quest_track_bandit_lair_choice",
	"Bandits such as these will usually set up their encampments far north, where it is cold. The best way to discover its location would be to find a group of warriors who appear to be heading back to their base to resupply, and follow them.", "merchant_quest_track_bandit_lair_choice",
   []],
  [anyone,"destroy_lair_quest_brief", [
     (eq,"$random_quest_no", "qst_destroy_bandit_lair"),
	 (quest_get_slot, ":bandit_lair", "qst_destroy_bandit_lair", slot_quest_target_party),
	 (party_get_template_id, ":bandit_type", ":bandit_lair"),
	 (eq, ":bandit_type", "pt_woku_pirate_lair"),
	 ],
	"Bandits such as these will usually establish a base on the coast. The best way to discover its location would be to find a group of pirates who appear to be heading back to their base to resupply, and follow them.", "merchant_quest_track_bandit_lair_choice",
   []],
  [anyone,"destroy_lair_quest_brief", [
     (eq,"$random_quest_no", "qst_destroy_bandit_lair"),
	 (quest_get_slot, ":bandit_lair", "qst_destroy_bandit_lair", slot_quest_target_party),
	 (party_get_template_id, ":bandit_type", ":bandit_lair"),
	 (eq, ":bandit_type", "pt_shinano_rebel_lair"),
	 ],
	"Bandits such as these usually operate in a far-flung mansion deep in the woods, in a hidden valley. The best way to discover its location would be to find a group of rebels who appear to be heading back home to resupply, and follow them.", "merchant_quest_track_bandit_lair_choice",
   []],
  [anyone,"destroy_lair_quest_brief", [
     (eq,"$random_quest_no", "qst_destroy_bandit_lair"),
	 (quest_get_slot, ":bandit_lair", "qst_destroy_bandit_lair", slot_quest_target_party),
	 (party_get_template_id, ":bandit_type", ":bandit_lair"),
	 (eq, ":bandit_type", "pt_seto_pirate_lair"),
	 ],
	#gekokujo "steppe bandits" now get mountain hideout
	#"Bandits such as these will usually set up their encampments in the woodland on the steppe, where they have some concealment. The best way to discover its location would be to find a group of steppe bandits who appear to be heading back to their base to resupply, and follow them.", "merchant_quest_track_bandit_lair_choice",
	"Bandits such as these will usually establish a base among the small islands of the inland sea. This makes them difficult to assault. The best way to discover its location would be to find a group of pirates who appear to be heading back to their base to resupply, and follow them.", "merchant_quest_track_bandit_lair_choice",
   []],
  [anyone,"destroy_lair_quest_brief", [
     (eq,"$random_quest_no", "qst_destroy_bandit_lair"),
	 (quest_get_slot, ":bandit_lair", "qst_destroy_bandit_lair", slot_quest_target_party),
	 (party_get_template_id, ":bandit_type", ":bandit_lair"),
	 (eq, ":bandit_type", "pt_kanto_rebel_lair"),
	 ],
	"Bandits such as these usually operate from out of the way fortified mansions. The best way to discover its location would be to find a group of rebels who appear to be heading back to their mansion to resupply, and follow them.", "merchant_quest_track_bandit_lair_choice",
   []],
  #gekokujo 3.0 monk bandit lair dialogue fix start
  [anyone,"destroy_lair_quest_brief", [
     (eq,"$random_quest_no", "qst_destroy_bandit_lair"),
	 (quest_get_slot, ":bandit_lair", "qst_destroy_bandit_lair", slot_quest_target_party),
	 (party_get_template_id, ":bandit_type", ":bandit_lair"),
	 (eq, ":bandit_type", "pt_monk_rebel_lair"),
	 ],
	"Bandits such as these will usually set up their encampments in rural temples, probably fortified. The best way to discover its location would be to find a group of monks who appear to be heading back to their temple to resupply, and follow them.", "merchant_quest_track_bandit_lair_choice",
   []],
  [party_tpl|pt_merchant_caravan,"start", [(quest_get_slot, ":quest_target_party", "qst_escort_merchant_caravan", slot_quest_target_party),
                                           (eq,"$g_encountered_party",":quest_target_party"),
                                           (quest_slot_eq,"qst_escort_merchant_caravan", slot_quest_current_state, 2),
                                           ],
   "We can cover the rest of the way ourselves. Thanks.", "close_window",[(assign, "$g_leave_encounter", 1)]],
  [party_tpl|pt_merchant_caravan,"start", [(quest_get_slot, ":quest_target_party", "qst_escort_merchant_caravan", slot_quest_target_party),
                                           (eq,"$g_encountered_party",":quest_target_party"),
                                           (quest_get_slot, ":quest_target_center", "qst_escort_merchant_caravan", slot_quest_target_center),
                                           (store_distance_to_party_from_party, ":dist", ":quest_target_center",":quest_target_party"),
                                           (lt,":dist",4),
                                           (quest_slot_eq, "qst_escort_merchant_caravan", slot_quest_current_state, 1),
                                           ],
   "Well, we have almost reached {s21}. We can cover the rest of the way ourselves.\
 Here's your pay... {reg14} mon.\
 Thanks for escorting us. Good luck.", "close_window",[(quest_get_slot, ":quest_target_party", "qst_escort_merchant_caravan", slot_quest_target_party),
                                                       (quest_get_slot, ":quest_target_center", "qst_escort_merchant_caravan", slot_quest_target_center),
                                                       (quest_get_slot, ":quest_giver_center", "qst_escort_merchant_caravan", slot_quest_giver_center),
                                                       (quest_get_slot, ":quest_gold_reward", "qst_escort_merchant_caravan", slot_quest_gold_reward),
                                                       (party_set_ai_behavior, ":quest_target_party", ai_bhvr_travel_to_party),
                                                       (party_set_ai_object, ":quest_target_party", ":quest_target_center"),
                                                       (party_set_flags, ":quest_target_party", pf_default_behavior, 0),
                                                       (str_store_party_name, s21, ":quest_target_center"),
                                                       (call_script, "script_change_player_relation_with_center", ":quest_giver_center", 1),
                                                       (call_script, "script_end_quest","qst_escort_merchant_caravan"),
                                                       (quest_set_slot, "qst_escort_merchant_caravan", slot_quest_current_state, 2),
                                                       (call_script, "script_troop_add_gold", "trp_player", ":quest_gold_reward"),
                                                       (assign, ":xp_reward", ":quest_gold_reward"),
                                                       (val_mul, ":xp_reward", 5),
                                                       (val_add, ":xp_reward", 100),
                                                       (add_xp_as_reward, ":xp_reward"),
                                                       (call_script, "script_change_troop_renown", "trp_player", 2),
                                                       (assign, reg14, ":quest_gold_reward"),
                                                       (assign, "$g_leave_encounter", 1),
                                                       ]],
  [party_tpl|pt_merchant_caravan,"start", [(quest_get_slot, ":quest_target_party", "qst_escort_merchant_caravan", slot_quest_target_party),
                                           (eq,"$g_encountered_party",":quest_target_party"),
                                           (quest_slot_eq, "qst_escort_merchant_caravan", slot_quest_current_state, 0),
                                           ],
   "Greetings. You must be our escort, right?", "merchant_caravan_intro_1",[(quest_set_slot, "qst_escort_merchant_caravan", slot_quest_current_state, 1),]],
  [party_tpl|pt_merchant_caravan,"start", [(quest_get_slot, ":quest_target_party", "qst_escort_merchant_caravan", slot_quest_target_party),
                                           (eq, "$g_encountered_party", ":quest_target_party"),
                                           ],
   "Eh. We've made it this far... What do you want us to do?", "escort_merchant_caravan_talk",[]],
  [anyone|plyr,"troublesome_bandits_quest_brief", [],
   "Very well. I will hunt down those bandits.", "merchant_quest_taken_bandits",
   [(set_spawn_radius,7),
    (quest_get_slot, ":quest_giver_center", "qst_troublesome_bandits", slot_quest_giver_center),
    (spawn_around_party,":quest_giver_center","pt_troublesome_bandits"),
    (quest_set_slot, "qst_troublesome_bandits", slot_quest_target_party, reg0),
    (store_num_parties_destroyed,"$qst_troublesome_bandits_eliminated","pt_troublesome_bandits"),
    (store_num_parties_destroyed_by_player, "$qst_troublesome_bandits_eliminated_by_player", "pt_troublesome_bandits"),
    (str_store_troop_name, s9, "$g_talk_troop"),
    (str_store_party_name_link, s4, "$g_encountered_party"),
    (setup_quest_text,"qst_troublesome_bandits"),
    (str_store_string, s2, "@Merchant {s9} of {s4} asked you to hunt down the troublesome bandits in the vicinity of the town."),
    (call_script, "script_start_quest", "qst_troublesome_bandits", "$g_talk_troop"),
    ]],
  [anyone|plyr,"troublesome_bandits_quest_brief", [],
   "Sorry. I don't have time for this right now.", "merchant_quest_stall",[]],
  [anyone|plyr,"kidnapped_girl_quest_brief", [],
      "All right. I will take the ransom money to the bandits and bring back the girl.",
   "kidnapped_girl_quest_taken",[(set_spawn_radius, 4),
                                 (quest_get_slot, ":quest_target_center", "qst_kidnapped_girl", slot_quest_target_center),
                                 (quest_get_slot, ":quest_target_amount", "qst_kidnapped_girl", slot_quest_target_amount),
                                 (spawn_around_party,":quest_target_center","pt_bandits_awaiting_ransom"),
                                 (assign, ":quest_target_party", reg0),
                                 (quest_set_slot, "qst_kidnapped_girl", slot_quest_target_party, ":quest_target_party"),
                                 (party_set_ai_behavior, ":quest_target_party", ai_bhvr_hold),
                                 (party_set_ai_object, ":quest_target_party", "p_main_party"),
                                 (party_set_flags, ":quest_target_party", pf_default_behavior, 0),
                                 (call_script, "script_troop_add_gold", "trp_player", ":quest_target_amount"),
                                 (assign, reg12, ":quest_target_amount"),
                                 (str_store_troop_name, s1, "$g_talk_troop"),
                                 (str_store_party_name_link, s4, "$g_encountered_party"),
                                 (str_store_party_name_link, s3, ":quest_target_center"),
                                 (setup_quest_text, "qst_kidnapped_girl"),
                                 (str_store_string, s2, "@The chief merchant of {s4} gave you {reg12} mon to pay the ransom of a girl kidnapped by bandits.\
 You are to meet the bandits near {s3} and pay them the ransom fee.\
 After that you are to bring the girl back to {s4}."),
                                 (call_script, "script_start_quest", "qst_kidnapped_girl", "$g_talk_troop"),
                                 ]],
  [anyone,"kidnapped_girl_quest_taken", [], "Good. I knew we could trust you at this.\
 Here is the ransom money, {reg12} mon.\
 Count it before taking it.\
 And please, don't attempt to do anything rash.\
 Keep in mind that the girl's well being is more important than anything else...", "close_window",
   []],
  [anyone|plyr,"kidnapped_girl_quest_brief", [],
   "Sorry. I don't have time for this right now.", "merchant_quest_stall",[]],
  [trp_kidnapped_girl,"start",
   [
     (eq, "$talk_context", tc_entering_center_quest_talk),
     ],
   "Thank you so much for bringing me back!\
  I can't wait to see my family. Good-bye.",
   "close_window",
   [(remove_member_from_party, "trp_kidnapped_girl"),
    (quest_set_slot, "qst_kidnapped_girl", slot_quest_current_state, 4),
    ]],
  [trp_kidnapped_girl|plyr,"kidnapped_girl_liberated_map", [], "Yes. Come with me. We are going home.", "kidnapped_girl_liberated_map_2a",[]],
  [trp_kidnapped_girl,"kidnapped_girl_liberated_map_2a", [(neg|party_can_join)], "Unfortunately. You do not have room in your party for me.", "close_window",[(assign, "$g_leave_encounter",1)]],
  [trp_kidnapped_girl,"kidnapped_girl_liberated_map_2a", [], "Oh really? Thank you so much!",
   "close_window", [(party_join),
                    (quest_set_slot, "qst_kidnapped_girl", slot_quest_current_state, 3),
                    (assign, "$g_leave_encounter",1)]],
  [trp_kidnapped_girl|plyr,"kidnapped_girl_liberated_map", [], "Wait here a while longer. I'll come back for you.", "kidnapped_girl_liberated_map_2b",[]],
  [trp_kidnapped_girl,"kidnapped_girl_liberated_map_2b", [], "Oh, please {sir/madam}, do not leave me here all alone!", "close_window",[(assign, "$g_leave_encounter",1)]],
  [trp_kidnapped_girl,"start", [],
   "Oh {sir/madam}. Thank you so much for rescuing me. Will you take me to my family now?", "kidnapped_girl_liberated_map",[]],
  [trp_kidnapped_girl|plyr,"kidnapped_girl_liberated_battle", [], "Yes. Come with me. We are going home.", "kidnapped_girl_liberated_battle_2a",[]],
  [trp_kidnapped_girl,"kidnapped_girl_liberated_battle_2a", [(neg|hero_can_join, "p_main_party")], "Unfortunately. You do not have room in your party for me.", "kidnapped_girl_liberated_battle_2b",[]],
  [trp_kidnapped_girl,"kidnapped_girl_liberated_battle_2a", [], "Oh really? Thank you so much!",
   "close_window",[(party_add_members, "p_main_party","trp_kidnapped_girl",1),
                   (quest_set_slot, "qst_kidnapped_girl", slot_quest_current_state, 3),
                   ]],
  [trp_kidnapped_girl|plyr,"kidnapped_girl_liberated_battle", [], "Wait here a while longer. I'll come back for you.", "kidnapped_girl_liberated_battle_2b",[]],
  [trp_kidnapped_girl,"kidnapped_girl_liberated_battle_2b", [], "Oh, please {sir/madam}, do not leave me here all alone!",
   "close_window", [(add_companion_party,"trp_kidnapped_girl"),
                    (assign, "$g_leave_encounter",1)]],
  [trp_kidnapped_girl,"start", [], "Can I come with you now?", "kidnapped_girl_liberated_map",[]],
  [party_tpl|pt_bandits_awaiting_ransom,"start", [(quest_slot_eq, "qst_kidnapped_girl", slot_quest_current_state, 0),],
   "Are you the one that brought the ransom?\
 Quick, give us the money now.", "bandits_awaiting_ransom_intro_1",[(quest_set_slot, "qst_kidnapped_girl", slot_quest_current_state, 1),]],
  [party_tpl|pt_bandits_awaiting_ransom,"start", [(quest_slot_eq, "qst_kidnapped_girl", slot_quest_current_state, 1),],
   "You came back?\
 Quick, give us the money now.", "bandits_awaiting_ransom_intro_1",[]],
  [party_tpl|pt_bandits_awaiting_ransom,"start", [(quest_slot_ge, "qst_kidnapped_girl", slot_quest_current_state, 2),],
   "What's it? You have given us the money. We have no more business.", "bandits_awaiting_remeet",[]],
  [party_tpl|pt_kidnapped_girl,"start", [],
   "Oh {sir/madam}. Thank you so much for rescuing me. Will you take me to my family now?", "kidnapped_girl_encounter_1",[]],
  [anyone|plyr,"kidnapped_girl_encounter_1", [], "Yes. Come with me. I'll take you home.", "kidnapped_girl_join",[]],
  [anyone,"kidnapped_girl_join", [(neg|party_can_join)], "Unfortunately. You do not have room in your party for me.", "close_window",[(assign, "$g_leave_encounter",1)]],
  [anyone,"kidnapped_girl_join", [], "Oh, thank you so much!",
   "close_window",[(party_join),
                   (quest_set_slot, "qst_kidnapped_girl", slot_quest_current_state, 3),
                   (assign, "$g_leave_encounter",1)]],
  [anyone|plyr,"kidnapped_girl_encounter_1", [], "Wait here a while longer. I'll come back for you.", "kidnapped_girl_wait",[]],
  [anyone,"kidnapped_girl_wait", [], "Oh, please {sir/madam}, do not leave me here all alone!", "close_window",[(assign, "$g_leave_encounter",1)]],
  [anyone,"lost_kidnapped_girl", [],
   "Oh no! How am I going to tell this to my friend?", "lost_kidnapped_girl_2",[]],
  [anyone|plyr,"lost_kidnapped_girl_2", [],
   "I'm sorry. I could do nothing about it.", "lost_kidnapped_girl_3",[]],
  [anyone,"lost_kidnapped_girl_3", [],
   "You let me down {playername}. I had trusted you.\
 I will let people know of your incompetence at this task.\
 Also, I want back that {reg8} mon I gave you as the ransom fee.", "lost_kidnapped_girl_4",
   [(quest_get_slot, reg8, "qst_kidnapped_girl", slot_quest_target_amount),
    (try_for_parties, ":cur_party"),
      (party_count_members_of_type, ":num_members", ":cur_party", "trp_kidnapped_girl"),
      (gt, ":num_members", 0),
      (party_remove_members, ":cur_party", "trp_kidnapped_girl", 1),
      (party_remove_prisoners, ":cur_party", "trp_kidnapped_girl", 1),
    (try_end),
    (call_script, "script_end_quest", "qst_kidnapped_girl"),
    (call_script, "script_change_troop_renown", "trp_player", -5),
    ]],
  [anyone|plyr, "lost_kidnapped_girl_4", [(store_troop_gold,":gold"),
                                          (quest_get_slot, ":quest_target_amount", "qst_kidnapped_girl", slot_quest_target_amount),
                                          (ge,":gold",":quest_target_amount"),
                                          ],
   "Of course. Here you are...", "merchant_quest_about_job_5a",[(quest_get_slot, ":quest_target_amount", "qst_kidnapped_girl", slot_quest_target_amount),
                                                                (troop_remove_gold, "trp_player",":quest_target_amount"),
                                                                ]],
  [anyone|plyr,"lost_kidnapped_girl_4", [],
   "Sorry. I don't have that amount with me.", "merchant_quest_about_job_5b",[]],
  [anyone,"deal_with_night_bandits_quest_taken", [], "That takes a weight off my shoulders, {playername}.\
 You can expect a fine reward if you come back successful. Just don't get yourself killed, eh?", "mayor_pretalk",[]],
  [anyone|plyr,"move_cattle_herd_quest_brief", [],  "Aye, I can take the herd to {s13}.",
   "move_cattle_herd_quest_taken",
   [
     (call_script, "script_create_cattle_herd", "$g_encountered_party", 0),
     (quest_set_slot, "qst_move_cattle_herd", slot_quest_target_party, reg0),
     (str_store_party_name_link, s10,"$g_encountered_party"),
     (quest_get_slot, ":target_center", "qst_move_cattle_herd", slot_quest_target_center),
     (str_store_party_name_link, s13, ":target_center"),
     (quest_get_slot, reg8, "qst_move_cattle_herd", slot_quest_gold_reward),
     (setup_quest_text, "qst_move_cattle_herd"),
     (str_store_string, s2, "@The elder merchant of {s10} asked you to move a cattle herd to {s13}. You will earn {reg8} mon in return."),
     (call_script, "script_start_quest", "qst_move_cattle_herd", "$g_talk_troop"),
     ]],
  [anyone|plyr,"move_cattle_herd_quest_brief", [],
   "I am sorry, but no.", "merchant_quest_stall",[]],
  [anyone,"move_cattle_herd_quest_taken", [], "Splendid. You can find the herd right outside the town.\
 After you take the animals to {s13}, return back to me and I will give you your pay.", "mayor_pretalk",[]],
#Village elders

  [anyone,"start", [(is_between,"$g_talk_troop",village_elders_begin,village_elders_end),
                    (store_partner_quest,":elder_quest"),
                    (eq,":elder_quest","qst_deliver_cattle"),
                    (check_quest_succeeded, ":elder_quest"),
                    (quest_get_slot, reg5, "qst_deliver_cattle", slot_quest_target_amount)],
   "My good {sir/madam}. Our village is grateful for your help. Thanks to the {reg5} heads of cattle you have brought, we can now raise our own herd.", "village_elder_deliver_cattle_thank",
   [(add_xp_as_reward, 400),
#    (quest_get_slot, ":num_cattle", "qst_deliver_cattle", slot_quest_target_amount),
#    (party_set_slot, "$current_town", slot_village_number_of_cattle, ":num_cattle"),
    (call_script, "script_change_center_prosperity", "$current_town", 4),
    (call_script, "script_change_player_relation_with_center", "$current_town", 5),
    (call_script, "script_end_quest", "qst_deliver_cattle"),
#Troop commentaries begin
    (call_script, "script_add_log_entry", logent_helped_peasants, "trp_player",  "$current_town", -1, -1),
#Troop commentaries end

    ]],
##  [anyone,"start",
##   [
##     (is_between, "$g_talk_troop", village_elders_begin, village_elders_end),
##     (store_partner_quest, ":elder_quest"),
##     (eq, ":elder_quest", "qst_train_peasants_against_bandits"),
##     (check_quest_succeeded, ":elder_quest"),
##     (quest_get_slot, reg5, "qst_train_peasants_against_bandits", slot_quest_target_amount)],
##   "Oh, thank you so much for training our men. Now we may stand a chance against those accursed bandits if they come again.", "village_elder_train_peasants_against_bandits_thank",
##   [
##     (add_xp_as_reward, 400),
##     (call_script, "script_change_player_relation_with_center", "$current_town", 5),
##     (call_script, "script_end_quest", "qst_train_peasants_against_bandits"),
##     (call_script, "script_add_log_entry", logent_helped_peasants, "trp_player",  "$current_town", -1, -1),
##    ]],

#  [anyone,"village_elder_train_peasants_against_bandits_thank", [],
#   "Now, good {sire/lady}, is there anything I can do for you?", "village_elder_talk",[]],


##diplomacy start+
##
#Move this village_elder_talk line below, otherwise it wouldn't be able to trigger.
#  [anyone,"start", [(is_between,"$g_talk_troop", village_elders_begin, village_elders_end),(eq,"$g_talk_troop_met",0),
#                    (str_store_party_name, s9, "$current_town")],
#   "Good day, {sir/madam}, and welcome to {s9}. I am the elder of this village.", "village_elder_talk",[]],
##diplomacy end+

  [anyone,"start", [(is_between,"$g_talk_troop", village_elders_begin, village_elders_end),(eq,"$g_talk_troop_met",0),
                    (str_store_party_name, s9, "$current_town"),
                    (party_slot_eq, "$current_town", slot_town_lord, "trp_player"),
					##diplomacy start+
					#Replace "my {lord/lady}" with "your highness" if appropriate.
					(call_script, "script_dplmc_print_subordinate_says_sir_madame_to_s0"),
					(try_begin),
						#override default behavior to write "my {lord/lady}" if a less respectful form of address would have ben chosen
						(lt, reg0, 2),
						(str_store_string, s0, "str_dplmc_my_lordlady"),
					(try_end),
					],
   "Welcome to {s9}, {s0}. We were rejoiced by the news that you are the new {lord/lady} of our humble village.\
 I am the village elder and I will be honoured to serve you in any way I can.", "village_elder_talk",[]],
#Replced "my {lord/lady}" with "{s0}"

##Moved this village_elder_talk line from above, otherwise it wouldn't be able to trigger.
  [anyone,"start", [(is_between,"$g_talk_troop", village_elders_begin, village_elders_end),(eq,"$g_talk_troop_met",0),
                    (str_store_party_name, s9, "$current_town"),
					(call_script, "script_dplmc_print_commoner_at_arg1_says_sir_madame_to_s0", "$current_town"),#added this line
					],
   "Good day, {s0}, and welcome to {s9}. I am the elder of this village.", "village_elder_talk",[]],
#replaced {sir/madam} with {s0}

##Replace "My {lord/lady}" with "Your highness" if appropriate.
   [anyone ,"start", [(is_between,"$g_talk_troop",village_elders_begin,village_elders_end),
                     (party_slot_eq, "$current_town", slot_town_lord, "trp_player"),
					 #We aren't going to use the contents of {s0}, just checking the return value
					 (call_script, "script_dplmc_print_subordinate_says_sir_madame_to_s0"),
					 (ge, reg0, 3),#"your highness"
					 ],
   "You honour our humble village with your presence.", "village_elder_talk",[]],
  ##diplomacy end+

  [anyone ,"start", [(is_between,"$g_talk_troop",village_elders_begin,village_elders_end),
                     (party_slot_eq, "$current_town", slot_town_lord, "trp_player")],
   "{My lord/My lady}, you honour our humble village with your presence.", "village_elder_talk",[]],
  [anyone ,"start", [(is_between,"$g_talk_troop",village_elders_begin,village_elders_end),
  ##diplomacy start+
  (call_script, "script_dplmc_print_commoner_at_arg1_says_sir_madame_to_s0", "$current_town"),
  ],
   "Good day, {s0}.", "village_elder_talk",[]],
  ##diplomacy start+ replace {sir/madam} with {my lord/my lady} or your highness if appropriate
  [anyone ,"start", [(is_between,"$g_talk_troop",goods_merchants_begin,goods_merchants_end),
			         (call_script, "script_dplmc_print_subordinate_says_sir_madame_to_s0"),],
   "Welcome {s0}. What can I do for you?", "goods_merchant_talk",[]],
  ##diplomacy end+
#  [trp_salt_mine_merchant,"start", [], "Hello.", "goods_merchant_talk",[]],

#  [anyone,"merchant_begin", [], " What can I do for you?", "goods_merchant_talk",[]],

  [anyone,"goods_merchant_pretalk", [], "Anything else?", "goods_merchant_talk",[]],
  [anyone|plyr,"goods_merchant_talk", [], "I want to buy a few items... and perhaps sell some.", "goods_trade_requested",[]],
  [anyone,"goods_trade_requested", [], "Sure, sure... Here, have a look at my stock...", "goods_trade_completed",[[change_screen_trade]]],
  [anyone,"goods_trade_completed", [], "Anything else?", "goods_merchant_talk",[]],
  [anyone|plyr,"goods_merchant_talk", [], "What goods should I buy here to trade with other towns?", "trade_info_request",[]],
  [anyone|plyr,"goods_merchant_talk", [], "Nothing. Thanks.", "close_window",[]],
#  [anyone|plyr,"goods_merchant_talk", [], "What do caravans buy and sell in this town?", "goods_merchant_town_info",[]],
#  [anyone,"goods_merchant_town_info_completed", [], "Anything else?", "goods_merchant_talk",[]],


##  [anyone,"goods_merchant_town_info", [],
##   "TODO: We produce {s1}, and we consume {s2}.", "goods_merchant_town_info_completed",
##   [(call_script, "script_print_productions_above_or_below_50", "$g_encountered_party", 1),
##    (str_store_string_reg, s1, s51),
##    (call_script, "script_print_productions_above_or_below_50", "$g_encountered_party", -1),
##    (str_store_string_reg, s2, s51)]],
##
##  [anyone,"goods_merchant_town_info", [(store_encountered_party,reg(1)),(eq,reg(1),"p_zendar")],
##"You can buy tools from here at a very good price.\
## The best place to sell them would be Tulga. Heard they pay quite well for tools over there.\
## And next time you come here bring some salt. I will pay well for salt.", "goods_merchant_town_info_completed",[]],
##  [anyone,"goods_merchant_town_info", [(store_encountered_party,reg(1)),(eq,reg(1),"p_town_1")],
##"Sargoth is famous for its fine linen. Many caravans come here to buy that.\
## I heard you can sell it at Halmar and make a nice profit.\
## And next time you come here bring some iron. I will pay well for iron.", "goods_merchant_town_info_completed",[]],
##  [anyone,"goods_merchant_town_info", [[store_encountered_party,reg(1)],[eq,reg(1),"p_town_2"]],
##"I can sell you some smoked fish with a special price.\
## I heard that caravans take smoked fish to Uxkhal and make a good profit.\
## And next time you come here bring some wool. I will pay you well for wool.", "goods_merchant_town_info_completed",[]],
##  [anyone,"goods_merchant_town_info", [[store_encountered_party,reg(1)],[eq,reg(1),"p_town_3"]],
##"I can sell you some wine with a special price.\
## I heard that caravans buy wine from here and sell it at Wercheg, making a good profit.\
## And next time you come here, bring some dried meat. I will pay you well for dried meat.", "goods_merchant_town_info_completed",[]],
##  [anyone,"goods_merchant_town_info", [[store_encountered_party,reg(1)],[eq,reg(1),"p_town_4"]],
##"I have a stock of oil which I can sell you with a good price.\
## They say they offer a fortune for oil in Rivacheg, so maybe you can sell it there.\
## And next time you come here, bring some furs. I will pay you well for furs.", "goods_merchant_town_info_completed",[]],
##  [anyone,"goods_merchant_town_info", [[store_encountered_party,reg(1)],[eq,reg(1),"p_town_5"]],
##"Jelkala is famous for its velvet. Many caravans come here to buy that.\
## They say merchants will buy it at insane prices in Reyvadin, so maybe you can take it there.\
## And next time you come here, bring some pottery. I will pay you well for pottery.", "goods_merchant_town_info_completed",[]],
##  [anyone,"goods_merchant_town_info", [[store_encountered_party,reg(1)],[eq,reg(1),"p_town_6"]],
##"We produce some excellent ale here in Praven. Most caravans come here to buy that.\
## They say that the folks at Khudan will sell their right arms for ale, so maybe you can take it there.\
## And next time you come here, bring some spice. I have sold out my stock of spice and I will pay you well for it.", "goods_merchant_town_info_completed",[]],
##  [anyone,"goods_merchant_town_info", [[store_encountered_party,reg(1)],[eq,reg(1),"p_town_7"]],
##"We produce mostly wheat here in Uxkhal. I would suggest you buy that.\
## I heard you can sell it with a good profit in Tulga, so maybe you can take it there.\
## And next time you come here, bring some smoked fish. I will pay you well for it.", "goods_merchant_town_info_completed",[]],
##
##  [anyone,"goods_merchant_town_info", [[store_encountered_party,reg(1)],[eq,reg(1),"p_town_8"]],
##"Most caravans come to Reyvadin to buy wool.\
## I heard that they take it to Tihr where they pay well for wool.\
## And next time you come here, bring some velvet. I will buy it from you at a good price.", "goods_merchant_town_info_completed",[]],
##  [anyone,"goods_merchant_town_info", [[store_encountered_party,reg(1)],[eq,reg(1),"p_town_9"]],
##"Most caravans come to Khudan to buy furs.\
## I heard that they take it to Suno where they pay well for it.\
## And next time you come here, bring some ale. I will buy it from you at a good price.", "goods_merchant_town_info_completed",[]],
##  [anyone,"goods_merchant_town_info", [[store_encountered_party,reg(1)],[eq,reg(1),"p_town_10"]],
##"Most caravans come to Tulga to buy spice.\
## They say that in Praven they pay well for spice, so you may think of selling it to the mechants there.\
## And next time you come here, bring some wheat. I will buy it from you at a good price.", "goods_merchant_town_info_completed",[]],
##  [anyone,"goods_merchant_town_info", [[store_encountered_party,reg(1)],[eq,reg(1),"p_town_11"]],
##"We mine a lot of iron here in Curaw. I would suggest you buy that.\
## I heard you can take it to Sargoth and sell it with a good profit.\
## And next time you come here, bring some dried meat. I will pay you well for it.", "goods_merchant_town_info_completed",[]],
##  [anyone,"goods_merchant_town_info", [[store_encountered_party,reg(1)],[eq,reg(1),"p_town_12"]],
##"I can sell you some smoked fish with a special price.\
## I heard that caravans take smoked fish to Uxkhal and make a good profit.\
## And next time you come here bring some wine. I will pay you well for wine.", "goods_merchant_town_info_completed",[]],
##  [anyone,"goods_merchant_town_info", [[store_encountered_party,reg(1)],[eq,reg(1),"p_town_13"]],
##"I have a stock of dried meat which I can sell you with a good price.\
## They say they pay very well for dried meat in Veluca, so maybe you can sell it there.\
## And next time you come here, bring some oil. I have sold out my stock of oil and I will pay you well for it.", "goods_merchant_town_info_completed",[]],
##  [anyone,"goods_merchant_town_info", [[store_encountered_party,reg(1)],[eq,reg(1),"p_town_14"]],
##"We produce some good quality pottery here in Halmar. Most caravans come here to buy that.\
## I heard that caravans buy pottery from here and sell it at Jelkala, making a good profit.\
## And next time you come here, bring some linen. I have sold out my stock of linen and I will pay you well for it.", "goods_merchant_town_info_completed",[]],
##
##  [anyone,"goods_merchant_town_info", [[store_encountered_party,reg(1)],[eq,reg(1),"p_salt_mine"]],
##"Heh. Are you joking with me? This is the salt mine. Merchants come here to buy salt.", "goods_merchant_town_info_completed",[]],
##
##  [anyone,"goods_merchant_town_info", [
##                                       (store_encountered_party,reg(9)),
##                                       (party_get_slot,reg(5),reg(9),slot_town_export_good),
##                                       (party_get_slot,reg(6),reg(9),slot_town_import_good),
##                                       (ge,reg(5),1),
##                                       (ge,reg(6),1),
##                                       (str_store_item_name,1,reg(5)),
##                                       (str_store_item_name,2,reg(6)),
##                                       ],
##  "I can sell you some {s1} with a special price.\
##And next time you come here bring some {s2}. I will pay you well for that.", "goods_merchant_town_info_completed",[]],
##
##  [anyone,"goods_merchant_town_info", [
##                                       (store_encountered_party,reg(9)),
##                                       (party_get_slot,reg(5),reg(9),slot_town_export_good),
##                                       (ge,reg(5),1),
##                                       (str_store_item_name,1,reg(5)),
##                                       ],
##  "I can sell you some {s1} with a special price.", "goods_merchant_town_info_completed",[]],
##
##  [anyone,"goods_merchant_town_info", [
##                                       (store_encountered_party,reg(9)),
##                                       (party_get_slot,reg(6),reg(9),slot_town_import_good),
##                                       (ge,reg(6),1),
##                                       (str_store_item_name,2,reg(6)),
##                                       ],
##  "If you have some {s2} with you, I am ready to pay you good money for it.", "goods_merchant_town_info_completed",[]],
##
##  [anyone,"goods_merchant_town_info", [],
##"Sorry. Caravans hardly ever trade anything here.", "goods_merchant_town_info_completed",[]],






#############################################################################
#### ARENA MASTERS
#############################################################################
  [anyone ,"start", [(store_conversation_troop,reg(1)),
                     (is_between,reg(1),arena_masters_begin,arena_masters_end),
                     (assign, "$arena_reward_asked", 0), #set some variables.
                     (assign, "$arena_tournaments_asked", 0),
                     (eq,1,0),
                     ],
   "{!}.", "arena_intro_1",[]],
  [anyone ,"start", [(store_conversation_troop,reg(1)),
                     (is_between,reg(1),arena_masters_begin,arena_masters_end),
                     (eq,"$arena_master_first_talk", 0),
                     ],
   "Good day friend. If you came to watch the tournaments you came in vain. There won't be a tournament here anytime soon.", "arena_intro_1",[(assign,"$arena_master_first_talk", 1)]],
  [anyone|plyr,"arena_intro_1", [], "Tournaments? So they hold the tournaments here...", "arena_intro_2",[]],
  [anyone,"arena_intro_2", [], "Yes. You should see this place during one of the tournament fights.\
 Everyone from the town and nearby villages comes here. The crowd becomes mad with excitement.\
 Anyway, as I said, there won't be an event here soon, so there isn't much to see.\
 Except, there is an official duel every now and then, and  of course we have melee fights almost every day.", "arena_intro_3",[]],
  [anyone|plyr,"arena_intro_3", [], "Tell me about the melee fights.", "arena_training_melee_intro",[]],
  [anyone,"arena_training_melee_intro", [], "The ashigaru and samurai get bored waiting for the next tournament,\
 so they have invented the training melee. It is a simple idea really.\
 Fighters jump into the arena with a weapon. There are no rules, no teams.\
 Everyone beats at each other until there is only one fighter left standing.\
 Sounds like fun, eh?", "arena_training_melee_intro_2",[]],
  [anyone|plyr,"arena_training_melee_intro_2", [(eq, "$arena_reward_asked", 0)], "Is there a reward?", "arena_training_melee_intro_reward",[(assign, "$arena_reward_asked", 1)]],
  [anyone,"arena_training_melee_intro_reward", [(assign, reg1, arena_tier1_opponents_to_beat),(assign, reg11, arena_tier1_prize),
      (assign, reg2, arena_tier2_opponents_to_beat),(assign, reg12, arena_tier2_prize),
      (assign, reg3, arena_tier3_opponents_to_beat),(assign, reg13, arena_tier3_prize),
      (assign, reg4, arena_tier4_opponents_to_beat),(assign, reg14, arena_tier4_prize),
      (assign, reg15, arena_grand_prize)
    ], "There is, actually. Some of the wealthy townsmen offer prizes for those fighters who show great skill in the fights.\
 If you can beat {reg1} opponents before going down, you'll earn {reg11} mon. You'll get {reg12} mon for striking down at least {reg2} opponents,\
 {reg13} mon if you can defeat {reg3} opponents, and {reg14} mon if you can survive long enough to beat {reg4} opponents.\
 If you can manage to be the last {man/fighter} standing, you'll earn the great prize of the fights, {reg15} mon. Sounds good, eh?", "arena_training_melee_intro_2",[(assign, "$arena_tournaments_asked", 1),]],
  [anyone,"arena_training_melee_explain_reward", [
      (assign, reg1, arena_tier1_opponents_to_beat),(assign, reg11, arena_tier1_prize),
      (assign, reg2, arena_tier2_opponents_to_beat),(assign, reg12, arena_tier2_prize),
      (assign, reg3, arena_tier3_opponents_to_beat),(assign, reg13, arena_tier3_prize),
      (assign, reg4, arena_tier4_opponents_to_beat),(assign, reg14, arena_tier4_prize),
      (assign, reg15, arena_grand_prize)
      ], "Some of the wealthy townsmen offer prizes for those fighters who show great skill in the fights.\
 If you can beat {reg1} opponents before going down, you'll earn {reg11} mon. You'll get {reg12} mon for striking down at least {reg2} opponents,\
 {reg13} mon if you can defeat {reg3} opponents, and {reg14} mon if you can survive long enough to beat {reg4} opponents.\
 If you can manage to be the last {man/fighter} standing, you'll earn the great prize of the fights, {reg15} mon. Sounds good, eh?", "arena_master_melee_pretalk",[]],
  [anyone|plyr,"arena_training_melee_intro_2", [], "Can I join too?", "arena_training_melee_intro_3",[]],
  [anyone,"arena_training_melee_intro_3", [], "Ha ha. You would have to be out of your mind not to. Of course. The melee fights are open to all.\
 Actually there is going to be a fight soon. You can go and hop in if you want to.", "arena_master_melee_talk",[]],
  [anyone ,"start", [(store_conversation_troop,reg(1)),
                     (is_between,reg(1),arena_masters_begin,arena_masters_end),
                     (eq,"$g_talk_troop_met", 0),
                     ],
   "Hello. You seem to be new here. Care to share your name?", "arena_master_intro_1",[]],
  [anyone|plyr,"arena_master_intro_1", [], "I am {playername}.", "arena_master_intro_2",[]],
  [anyone,"arena_master_intro_2", [(store_encountered_party,reg(2)),(str_store_party_name,1,reg(2))],
   "Well met {playername}. I am the master of the tournaments here at {s1}. Talk to me if you want to join the fights.", "arena_master_pre_talk",[]],
  [anyone|auto_proceed ,"start", [(store_conversation_troop,reg(1)),(is_between,reg(1),arena_masters_begin,arena_masters_end),
                     (eq, "$last_training_fight_town", "$current_town"),
                     (store_current_hours,":cur_hours"),
                     (val_add, ":cur_hours", -4),
                     (lt, ":cur_hours", "$training_fight_time")],
   ".", "arena_master_fight_result",[(assign, "$arena_reward_asked", 0)]],
  [anyone ,"arena_master_fight_result",
   [
     (eq, "$g_arena_training_won", 0),
     (eq, "$g_arena_training_kills", 0)
     ],
   "Ha-ha, that's quite the bruise you're sporting. But don't worry; everybody gets trounced once in awhile. The important thing is to pick yourself up, dust yourself off and keep fighting. That's what champions do.", "arena_master_pre_talk",[(assign, "$last_training_fight_town", -1)]],
  [anyone ,"arena_master_fight_result",
   [
     (eq, "$g_arena_training_won", 0),
     (lt, "$g_arena_training_kills", arena_tier1_opponents_to_beat),
     (assign, reg8, "$g_arena_training_kills")
     ],
   "Hey, you managed to take down {reg8} opponents. Not bad. But that won't bring you any prize money.\
 Now, if I were you, I would go back there and show everyone what I can do...", "arena_master_pre_talk",[(assign, "$last_training_fight_town", -1)]],
  [anyone ,"arena_master_fight_result",
   [
     (eq, "$g_arena_training_won", 0),
     (lt, "$g_arena_training_kills", arena_tier2_opponents_to_beat),
     (assign, reg8, "$g_arena_training_kills"),
     (assign, reg10, arena_tier1_prize),
     ],
   "You put up quite a good fight there. Good moves. You definitely show promise.\
 And you earned a prize of {reg10} mon for knocking down {reg8} opponents.", "arena_master_pre_talk",[
     (call_script, "script_troop_add_gold", "trp_player", arena_tier1_prize),
     (add_xp_to_troop,5,"trp_player"),
     (assign, "$last_training_fight_town", -1)]],
  [anyone ,"arena_master_fight_result",
   [
     (eq, "$g_arena_training_won", 0),
     (lt, "$g_arena_training_kills", arena_tier3_opponents_to_beat),
     (assign, reg8, "$g_arena_training_kills"),
     (assign, reg10, arena_tier2_prize),
     (assign, reg12, arena_tier2_opponents_to_beat),
     ],
   "That was a good fight you put up there. You managed to take down no less than {reg8} opponents.\
 And of course, you earned a prize money of {reg10} mon.", "arena_master_pre_talk",[
     (call_script, "script_troop_add_gold", "trp_player", arena_tier2_prize),
     (add_xp_to_troop,10,"trp_player"),
     (assign, "$last_training_fight_town", -1)]],
  [anyone ,"arena_master_fight_result",
   [
     (eq, "$g_arena_training_won", 0),
     (lt, "$g_arena_training_kills", arena_tier4_opponents_to_beat),
     (assign, reg8, "$g_arena_training_kills"),
     (assign, reg10, arena_tier3_prize)
     ],
   "Your performance was amazing! You are without doubt a very skilled fighter.\
 Not everyone can knock down {reg8} people in the fights. Of course you deserve a prize with that performance: {reg10} mon. Nice, eh?", "arena_master_pre_talk",[
     (call_script, "script_troop_add_gold", "trp_player", arena_tier3_prize),
     (add_xp_to_troop,10,"trp_player"),
     (assign, "$last_training_fight_town", -1)]],
  [anyone ,"arena_master_fight_result",
   [
     (eq, "$g_arena_training_won", 0),
     (assign, reg8, "$g_arena_training_kills"),
     (assign, reg10, arena_tier4_prize),
     ],
   "That was damned good fighting, {playername}. You have very good moves, excellent tactics.\
 And you earned a prize of {reg10} mon for knocking down {reg8} opponents.", "arena_master_pre_talk",
   [
     (call_script, "script_troop_add_gold", "trp_player", arena_tier4_prize),
     (add_xp_to_troop,10,"trp_player"),
     (assign, "$last_training_fight_town", -1),
     ]],
  [anyone ,"arena_master_fight_result", [(assign, reg10, arena_grand_prize)],
   "Congratulations champion! Your fight there was something to remember! You managed to be the last fighter standing beating down everyone else. And of course you won the grand prize of the fights: {reg10} mon.", "arena_master_pre_talk",[
     (call_script, "script_troop_add_gold", "trp_player", arena_grand_prize),
     (add_xp_to_troop,200,"trp_player"),
     (assign, "$last_training_fight_town", -1)]],
  [anyone ,"start", [(store_conversation_troop,reg(1)),(is_between,reg(1),arena_masters_begin,arena_masters_end)],
   "Hello {playername}. Good to see you again.", "arena_master_pre_talk",[(assign, "$arena_reward_asked", 0)]],
  [anyone,"arena_master_pre_talk", [], "What would you like to do?", "arena_master_talk",[]],
#  [anyone|plyr,"arena_master_talk", [], "About the arena fights...", "arena_master_melee",[]],
  [anyone|plyr,"arena_master_talk", [], "About the melee fights...", "arena_master_melee_pretalk",[]],
  [anyone|plyr,"arena_master_talk", [(eq, "$arena_tournaments_asked", 0)], "Will there be a tournament in nearby towns soon?", "arena_master_ask_tournaments",[(assign, "$arena_tournaments_asked", 1)]],
  [anyone|plyr,"arena_master_talk", [], "I need to leave now. Good bye.", "close_window",[]],
  [anyone,"arena_master_ask_tournaments", [], "{reg2?There won't be any tournaments any time soon.:{reg1?Tournaments are:A tournament is} going to be held at {s15}.}", "arena_master_talk",
   [
       (assign, ":num_tournaments", 0),
       (try_for_range_backwards, ":town_no", towns_begin, towns_end),
         (party_slot_ge, ":town_no", slot_town_has_tournament, 1),
         (val_add, ":num_tournaments", 1),
         (try_begin),
           (eq, ":num_tournaments", 1),
           (str_store_party_name, s15, ":town_no"),
         (else_try),
           (str_store_party_name, s16, ":town_no"),
           (eq, ":num_tournaments", 2),
           (str_store_string, s15, "@{s16} and {s15}"),
         (else_try),
           (str_store_string, s15, "@{!}{s16}, {s15}"),
         (try_end),
       (try_end),
       (try_begin),
         (eq, ":num_tournaments", 0),
         (assign, reg2, 1),
       (else_try),
         (assign, reg2, 0),
         (store_sub, reg1, ":num_tournaments", 1),
       (try_end),
   ]],
  [anyone,"arena_master_melee_pretalk", [], "There will be a fight here soon. You can go and jump in if you like.", "arena_master_melee_talk",[]],
  [anyone|plyr,"arena_master_melee_talk", [], "Good. That's what I am going to do.", "close_window",
   [
    (assign, "$last_training_fight_town", "$current_town"),
    (store_current_hours,"$training_fight_time"),
    (assign, "$g_mt_mode", abm_training),
    (party_get_slot, ":scene","$current_town",slot_town_arena),
    (modify_visitors_at_site,":scene"),
    (reset_visitors),
    (store_random_in_range, "$g_player_entry_point", 32, 40),
    (set_visitor, "$g_player_entry_point", "trp_player"),
    (set_jump_mission,"mt_arena_melee_fight"),
    (jump_to_scene, ":scene"),
    ]],
  [anyone|plyr,"arena_master_melee_talk", [], "Thanks. But I will give my bruises some time to heal.", "arena_master_melee_reject",[]],
  [anyone,"arena_master_melee_reject", [], "Good {man/girl}. That's clever of you.", "arena_master_pre_talk",[]],
  [anyone|plyr,"arena_master_melee_talk", [(eq, "$arena_reward_asked", 0)], "Actually, can you tell me about the rewards again?", "arena_training_melee_explain_reward",[(assign, "$arena_reward_asked", 1)]],
#  [anyone,"arena_master_pre_talk",
#   [(eq,"$arena_join_or_watch",1),
#    (ge,"$arena_bet_amount",1),
#    (eq,"$arena_bet_team","$arena_winner_team"),
#    (assign,reg(5),"$arena_win_amount")],
# "You've won the bet, eh? Let me see. The sum you have earned amounts to {reg5} mon. Here you go.", "arena_master_pre_talk",
#   [(call_script, "script_troop_add_gold", "trp_player", "$arena_win_amount"),
#    (assign,"$arena_bet_amount",0),
#    (assign,"$arena_win_amount",0),
#    ]],

#  [anyone,"arena_master_pre_talk",
#   [(eq,"$arena_join_or_watch",0),
#    (ge,"$arena_bet_amount",1),
#    (eq,"$arena_fight_won",1),
#    (assign,reg(5),"$arena_win_amount"),
#   ],
# "And you had the good sense to bet on yourself too. Hmm let me see. You have won yourself some {reg5} mon. Here you are.", "arena_master_pre_talk",
#   [(call_script, "script_troop_add_gold", "trp_player", "$arena_win_amount"),
#    (assign,"$arena_bet_amount",0),
#    (assign,"$arena_win_amount",0)]],

#  [anyone,"start", [(store_conversation_troop,reg(1)),(is_between,reg(1),arena_masters_begin,arena_masters_end),(eq,"$waiting_for_arena_fight_result",1),(eq,"$arena_join_or_watch",0),(eq,"$arena_fight_won",1)],
# "Congratulations champion. You made some pretty good moves out there. Here is your share of share of the prize money, 2 mon.", "arena_master_pre_talk",
#   [(assign,"$waiting_for_arena_fight_result",0),(add_xp_to_troop,20,"trp_player"),(call_script, "script_troop_add_gold", "trp_player",2)]],
#  [anyone,"start", [(store_conversation_troop,reg(1)),(is_between,reg(1),arena_masters_begin,arena_masters_end),(eq,"$waiting_for_arena_fight_result",1),(eq,"$arena_join_or_watch",0)],
# "That's quite the bruise you're sporting. But don't worry; everybody gets trounced once in awhile. The important thing is to pick yourself up, dust yourself off and keep fighting. That's what champions do.", "arena_master_pre_talk",[[assign,"$waiting_for_arena_fight_result"]]],
#  [anyone,"start", [(store_conversation_troop,reg(1)),(is_between,reg(1),arena_masters_begin,arena_masters_end),(eq,"$waiting_for_arena_fight_result",1)],
# "That was exciting wasn't it? Nothing like a good fight to get the blood flowing.", "arena_master_pre_talk",[(assign,"$waiting_for_arena_fight_result",0)]],

##  [anyone,"arena_master_melee", [], "The next arena fight will start in a while. Hurry up if you want to take part in it.", "arena_master_melee_talk",[
##    (party_get_slot, ":arena_cur_tier","$current_town",slot_town_arena_melee_cur_tier),
##    (try_begin), #reg3 = num teams, reg4 = team size
##      (eq, ":arena_cur_tier", 0),
##      (party_get_slot, "$_num_teams","$current_town",slot_town_arena_melee_1_num_teams),
##      (party_get_slot, "$_team_size","$current_town",slot_town_arena_melee_1_team_size),
##    (else_try),
##      (eq, ":arena_cur_tier", 1),
##      (party_get_slot, "$_num_teams","$current_town",slot_town_arena_melee_2_num_teams),
##      (party_get_slot, "$_team_size","$current_town",slot_town_arena_melee_2_team_size),
##    (else_try),
##      (party_get_slot, "$_num_teams","$current_town",slot_town_arena_melee_3_num_teams),
##      (party_get_slot, "$_team_size","$current_town",slot_town_arena_melee_3_team_size),
##    (try_end),
##   ]],
##  [anyone|plyr,"arena_master_melee_talk", [], "I want to join the next fight", "arena_master_next_melee_join",[(assign,"$arena_join_or_watch",0)]],
##  [anyone|plyr,"arena_master_melee_talk", [], "I would like to watch the next fight", "arena_master_next_melee_watch",
##   [(assign,"$arena_join_or_watch",1)]],
##  [anyone|plyr,"arena_master_melee_talk", [], "No. perhaps later.", "arena_master_we_will_fight_not",[]],
##  [anyone,"arena_master_we_will_fight_not", [], "Alright. Talk to me when you are ready.", "close_window",[]],
##  [anyone,"arena_master_next_melee_join", [
##    (assign,"$arena_bet_amount"),
##    (assign,"$arena_bet_team",0),
##    (party_get_slot, ":player_odds", "$g_encountered_party", slot_town_player_odds),
##    (store_div, ":divider", ":player_odds", 20),
##    (store_mul, ":odds_simple", ":divider", 20),
##    (val_sub, ":odds_simple", ":player_odds"),
##    (try_begin),
##      (lt, ":odds_simple", 0),
##      (val_add, ":divider", 1),
##    (try_end),
##    (val_max, ":divider", 50),
##    (store_div, ":odds_player", ":player_odds", ":divider"),
##    (store_div, ":odds_other", 1000, ":divider"),
##    (try_for_range, ":unused", 0, 5),
##      (assign, ":last_divider", 21),
##      (try_for_range, ":cur_divider", 2, ":last_divider"),
##        (store_div, ":odds_player_test", ":odds_player", ":cur_divider"),
##        (val_mul, ":odds_player_test", ":cur_divider"),
##        (eq, ":odds_player_test", ":odds_player"),
##        (store_div, ":odds_other_test", ":odds_other", ":cur_divider"),
##        (val_mul, ":odds_other_test", ":cur_divider"),
##        (eq, ":odds_other_test", ":odds_other"),
##        (val_div, ":odds_player", ":cur_divider"),
##        (val_div, ":odds_other", ":cur_divider"),
##        (assign, ":last_divider", 0),
##      (try_end),
##    (try_end),
##    (assign, reg5, ":odds_player"),
##    (assign, reg6, ":odds_other"),], "Do you want to place a bet on yourself? The odds against you are {reg5} to {reg6}.", "arena_master_will_you_bet",
##   []],
##
##  [anyone|plyr,"arena_master_will_you_bet", [], "No.", "arena_master_start_fight",[]],
##  [anyone|plyr,"arena_master_will_you_bet", [(store_troop_gold,reg(0)),(ge,reg(0),10)], "I want to bet 10 mon.",
##   "arena_master_bet_placed",[(assign,"$arena_bet_amount",10),(troop_remove_gold, "trp_player",10)]],
##  [anyone|plyr,"arena_master_will_you_bet", [(store_troop_gold,reg(0)),(ge,reg(0),50)], "I want to bet 50 mon.",
##   "arena_master_bet_placed",[(assign,"$arena_bet_amount",50),(troop_remove_gold, "trp_player",50)]],
##  [anyone|plyr,"arena_master_will_you_bet", [(store_troop_gold,reg(0)),(ge,reg(0),100)], "I want to bet 100 mon.",
##   "arena_master_bet_placed",[(assign,"$arena_bet_amount",100),(troop_remove_gold, "trp_player",100)]],
##  [anyone,"arena_master_next_melee_watch", [], "Do you want to place a bet?", "arena_master_will_you_bet",[]],
##  [anyone,"arena_master_bet_placed", [(eq,"$arena_join_or_watch",1)], "Hmm. That's good. If you win, you'll get {reg5} mon. And which team do you want to place your bet on?", "arena_master_select_team",
##   [(store_mul, "$arena_win_amount", "$arena_bet_amount", "$_num_teams"),
##    (val_mul, "$arena_win_amount", 9),
##    (val_div, "$arena_win_amount", 10),
##    (assign, reg5, "$arena_win_amount"),
##    ]],
##  [anyone|plyr,"arena_master_select_team", [], "The red team. I have a feeling they will win this one.",
##   "arena_master_start_fight",[(assign,"$arena_bet_team",0)]],
##  [anyone|plyr,"arena_master_select_team", [], "The blue team. They will sweep the ground with the reds.",
##   "arena_master_start_fight",[(assign,"$arena_bet_team",1)]],
##  [anyone|plyr,"arena_master_select_team", [(ge,"$_num_teams",3)], "The green team. My money is on them this time.",
##   "arena_master_start_fight",[(assign,"$arena_bet_team",2)]],
##  [anyone|plyr,"arena_master_select_team", [(ge,"$_num_teams",4)], "The yellow team. They will be victorious.",
##   "arena_master_start_fight",[(assign,"$arena_bet_team",3)]],
##  [anyone,"arena_master_bet_placed", [], "That's good. Let me record that. If you win, you'll get {reg5} mon.", "arena_master_start_fight",
##   [(store_mul,"$arena_win_amount", "$arena_bet_amount", "$_num_teams"),
##    (party_get_slot, ":player_odds", "$g_encountered_party", slot_town_player_odds),
##    (val_sub, "$arena_win_amount", "$arena_bet_amount"),
##    (val_mul, "$arena_win_amount", ":player_odds"),
##    (val_div, "$arena_win_amount", 1000),
##    (val_add, "$arena_win_amount", "$arena_bet_amount"),
##    (val_mul, "$arena_win_amount", 9),
##    (val_div, "$arena_win_amount", 10),
##    (assign, reg5, "$arena_win_amount"),
##    ]],
##
##  [anyone,"arena_master_start_fight", [], "Very well. The fight starts in a moment. Good luck.", "close_window",
##   [
##    (store_encountered_party,"$current_town"),
##    (party_get_slot, ":arena_scene","$current_town",slot_town_arena),
##    (modify_visitors_at_site,":arena_scene"),
##    (reset_visitors),
##
##    #Assemble participants
##    (assign, ":slot_no", 0),
##    (troop_set_slot, "trp_temp_array_a", ":slot_no", "trp_kaihime"),
##    (val_add, ":slot_no", 1),
##    (troop_set_slot, "trp_temp_array_a", ":slot_no", "trp_keiji"),
##    (val_add, ":slot_no", 1),
##    (troop_set_slot, "trp_temp_array_a", ":slot_no", "trp_yukimura"),
##    (val_add, ":slot_no", 1),
##    (try_for_range, reg(4), 0, 10),
##      (lt, ":slot_no", 48),
##      (troop_set_slot, "trp_temp_array_a", ":slot_no", "trp_regular_fighter"),
##      (val_add, ":slot_no", 1),
##    (try_end),
##    (try_for_range, reg(4), 0, 10),
##      (lt, ":slot_no", 48),
##      (troop_set_slot, "trp_temp_array_a", ":slot_no", "trp_veteran_fighter"),
##      (val_add, ":slot_no", 1),
##    (try_end),
##    (try_for_range, reg(4), 0, 10),
##      (lt, ":slot_no", 48),
##      (troop_set_slot, "trp_temp_array_a", ":slot_no", "trp_champion_fighter"),
##      (val_add, ":slot_no", 1),
##    (try_end),
##    (try_for_range, reg(4), 0, 5),
##      (lt, ":slot_no", 48),
##      (troop_set_slot, "trp_temp_array_a", ":slot_no", "trp_onnabushi_elite"),
##      (val_add, ":slot_no", 1),
##    (try_end),
##    (try_for_range, reg(4), 0, 10),
##      (lt, ":slot_no", 48),
##      (troop_set_slot, "trp_temp_array_a", ":slot_no", "trp_hired_warrior_veteran"),
##      (val_add, ":slot_no", 1),
##    (try_end),
##    (try_for_range, reg(4), 0, 10),
##      (lt, ":slot_no", 48),
##      (troop_set_slot, "trp_temp_array_a", ":slot_no", "trp_mercenary"),
##      (val_add, ":slot_no", 1),
##    (try_end),
##    (assign, "$pin_troop", "trp_temp_array_a"),
##    (call_script, "script_shuffle_troop_slots", 0, 48),
##
##    (try_for_range, reg(12), 0, 48),
##      (troop_set_slot, "trp_temp_array_b", reg(12),reg(12)), #Initialize temp_array_b such that temp_array_b[i] = i
##    (try_end),
##
##    (store_random_in_range, "$arena_player_team", 0, "$_num_teams"),
##    (try_for_range, ":i_team", 0, "$_num_teams"), # repeat for num_teams; reg(55) = cur_team
##      (assign, ":team_slots_start", ":i_team"),
##      (val_mul, ":team_slots_start", 8),
##      (assign, ":team_slots_end", ":team_slots_start"),
##      (val_add, ":team_slots_end", 8),
##      (assign, "$pin_troop", "trp_temp_array_b"),
##      (call_script, "script_shuffle_troop_slots", ":team_slots_start", ":team_slots_end"),
##      (assign, ":cur_slot", ":team_slots_start"),
##      (try_for_range, reg(6), 0, "$_team_size"), # repeat for team_size;
##        (troop_get_slot, ":cur_slot_troop", "trp_temp_array_a", ":cur_slot"),
##        (try_begin), #place player
##          (eq,"$arena_join_or_watch",0),
##          (eq, ":i_team", "$arena_player_team"),
##          (eq, reg(6), 0),
##          (assign, ":cur_slot_troop", "trp_player"),
##        (try_end),
##        (troop_get_slot, ":cur_entry_no", "trp_temp_array_b", ":cur_slot"),
##        (set_visitor,":cur_entry_no",":cur_slot_troop"),
##        (val_add, ":cur_slot", 1),
##      (try_end),
##    (try_end),
##
##    (try_begin),
##      (eq, "$arena_join_or_watch", 1),
##      (set_visitor, 33, "trp_player"),#entry point 51
##    (try_end),
##    (assign, "$arena_fight_won", 0),
##    (assign, "$arena_winner_team", -1),
##    (assign, "$waiting_for_arena_fight_result", 1),
##    (assign, "$g_mt_mode", abm_fight),
##    (party_get_slot, reg(6),"$current_town",slot_town_arena_melee_cur_tier),
##    (val_add,reg(6),1),
##    (val_mod,reg(6),3),
##    (party_set_slot, "$current_town",slot_town_arena_melee_cur_tier, reg(6)),
###    (set_jump_mission,"mt_arena_melee_fight"),
##    (party_get_slot, ":arena_mission_template", "$current_town", slot_town_arena_template),
##    (set_jump_mission, ":arena_mission_template"),
##    (party_get_slot, reg(7), "$current_town", slot_town_arena),
##    (jump_to_scene, reg(7)),
##    ]],



######################################################################################
  [trp_galeas,"start", [], "Hello {boy/girl}. If you have any prisoners, I will be happy to buy them from you.", "galeas_talk",[]],
  [trp_galeas|plyr,"galeas_talk",
   [[store_num_regular_prisoners,reg(0)],[ge,reg(0),1]],
   "Then you'd better bring your purse. I have got prisoners to sell.", "galeas_sell_prisoners",[]],
  [trp_galeas|plyr,"galeas_talk",[], "Not this time. Good-bye.", "close_window",[]],
  [trp_galeas,"galeas_sell_prisoners", [],
  "Let me see what you have...", "galeas_sell_prisoners_2",
   [[change_screen_trade_prisoners]]],
  [trp_galeas, "galeas_sell_prisoners_2", [], "You take more prisoners, bring them to me. I will pay well.", "close_window",[]],
##  [party_tpl|pt_refugees,"start", [], "We have been driven out of our homes because of this war.", "close_window",[(assign, "$g_leave_encounter",1)]],
##  [party_tpl|pt_farmers,"start", [], "We are just simple farmers.", "close_window",[(assign, "$g_leave_encounter",1)]],


# Random Quest related conversations
#  [trp_nobleman, "start", [],
#   "Who are you? What do you want? Be warned, we are fully armed and more than capable to defend ourselves. Go to your way now or you will regret it.", "nobleman_talk_1",
#   [(play_sound,"snd_encounter_nobleman")]],
#  [trp_nobleman|plyr, "nobleman_talk_1", [],
#   "I demand that you surrender to me.", "nobleman_talk_2",[]],
#  [trp_nobleman|plyr, "nobleman_talk_1", [],
#   "I am sorry sir. You may go.", "close_window",[(assign, "$g_leave_encounter",1)]],
#  [trp_nobleman, "nobleman_talk_2", [],
#   "Surrender to a puny peasant like you? Hah. Not likely.", "close_window",[[encounter_attack]]],
#
#  [trp_nobleman,"enemy_defeated", [], "Parley! I am of noble birth, and I ask for my right to surrender.", "nobleman_defeated_1",[]],
#  [trp_nobleman|plyr,"nobleman_defeated_1", [], "And I will grant you that. If you can be ransomed of course...", "nobleman_defeated_2",[]],
#  [trp_nobleman,"nobleman_defeated_2", [], "Oh, you need not worry about that. My family would pay a large ransom for me.", "nobleman_defeated_3",[]],
#  [trp_nobleman|plyr,"nobleman_defeated_3", [[str_store_troop_name,1,"$nobleman_quest_giver"]], "Hmm. {s1} will be happy about this... Then you are my prisoner.", "close_window",
#   [[assign,"$nobleman_quest_succeeded",1],[assign,"$nobleman_quest_nobleman_active",0]]],

# Prisoner Trains
##  [anyone,"start", [(eq,"$g_encountered_party_type",spt_prisoner_train)],
##   "What do you want?", "prisoner_train_talk",[]],
##
##  [anyone|plyr,"prisoner_train_talk", [],
##   "Set those prisoners free now!", "prisoner_train_talk_ultimatum",[]],
##  [anyone,"prisoner_train_talk_ultimatum", [],
##   "Or what? Are you going to attack us?", "prisoner_train_talk_ultimatum_2",[]],
##  [anyone|plyr,"prisoner_train_talk_ultimatum_2", [],
##   "Yes I will. Consider yourself warned!", "prisoner_train_talk_ultimatum_2a",[]],
##  [anyone,"prisoner_train_talk_ultimatum_2a", [],
##   "We'll see that.", "close_window",[
##    (call_script, "script_make_kingdom_hostile_to_player", "$g_encountered_party_faction", -3),
##    ]],
##
##  [anyone|plyr,"prisoner_train_talk_ultimatum_2", [],
##   "Attack you? Hell no! I just took pity on those poor souls.", "prisoner_train_talk_ultimatum_2b",[]],
##  [anyone,"prisoner_train_talk_ultimatum_2b", [],
##   "Find something else to take pity on.", "close_window",[(assign, "$g_leave_encounter",1)]],
##  [anyone|plyr,"prisoner_train_talk", [],
##   "Better watch those prisoners well. They may try to run away.", "prisoner_train_smalltalk",[]],
##  [anyone,"prisoner_train_smalltalk", [],
##   "Don't worry. They aren't going anywhere.", "close_window",[(assign, "$g_leave_encounter",1)]],



##  [anyone,"start", [(eq, "$g_encountered_party_type", spt_forager), (is_between, "$g_encountered_party_relation", -9, 1)],
##   "Hold it right there. Who are you?", "soldiers_interrogation",[(play_sound,"snd_encounter_vaegirs_neutral")]],
##  [anyone,"start", [(eq, "$g_encountered_party_type", spt_forager), (le, "$g_encountered_party_relation", -10)],
##   "You will not survive this!", "close_window",
##   [(store_relation, reg(5),"$g_encountered_party_faction"), (val_sub,reg(5),1), (set_relation,"$g_encountered_party_faction",0,reg(5)),(encounter_attack,0)]],
##  [anyone,"start", [(eq, "$g_encountered_party_type", spt_forager),(ge, "$g_encountered_party_relation", 1)],
##   "Our lands have been invaded. But we will drive them back.", "close_window",[(assign, "$g_leave_encounter",1),(play_sound,"snd_encounter_vaegirs_ally"),]],
##
##  [anyone,"start", [(eq, "$g_encountered_party_type", spt_scout),(is_between, "$g_encountered_party_relation", -9, 1)],
##   "Hold it right there. Who are you?", "soldiers_interrogation",[]],
##  [anyone,"start", [(eq, "$g_encountered_party_type", spt_scout),(le, "$g_encountered_party_relation", -10)],
##   "You deserve to die a thousand deaths!", "close_window",
##   [(store_relation, reg(5),"$g_encountered_party_faction"), (val_sub,reg(5),2), (set_relation,"$g_encountered_party_faction",0,reg(5)),(encounter_attack,0)]],
##  [anyone,"start", [(eq, "$g_encountered_party_type", spt_scout),(ge, "$g_encountered_party_relation", 1)],
##   "Venture deep into the enemy territory and find myself a caravan to raid. That's the way I will get rich.", "close_window",[(assign, "$g_leave_encounter",1)]],
##
##  [anyone,"start", [(this_or_next|eq, "$g_encountered_party_type", spt_patrol),(eq, "$g_encountered_party_type", spt_war_party),(is_between, "$g_encountered_party_relation", -9, 1)],
##   "Hold it right there. Who are you?", "soldiers_interrogation",[]],
##  [anyone,"start", [(this_or_next|eq, "$g_encountered_party_type", spt_patrol),(eq, "$g_encountered_party_type", spt_war_party),(le, "$g_encountered_party_relation", -10)],
##   "You will not survive this!", "close_window",
##   [(store_relation, reg(5),"$g_encountered_party_type"), (val_sub,reg(5),3), (set_relation,"$g_encountered_party_type",0,reg(5)),(encounter_attack,0)]],
##  [anyone,"start", [(this_or_next|eq, "$g_encountered_party_type", spt_patrol),(eq, "$g_encountered_party_type", spt_war_party),(ge, "$g_encountered_party_relation", 1)],
##   "Sooner or later, friend. Victory will belong to us.", "close_window",[(assign, "$g_leave_encounter",1)]],

#swadian parties
##  [anyone|plyr,"soldiers_interrogation", [], "I am {playername}.", "soldiers_interrogation_2",[]],
##  [anyone,"soldiers_interrogation_2", [], "What are you doing here?", "soldiers_interrogation_3",[]],
##  [anyone|plyr,"soldiers_interrogation_3", [], "I am carrying some merchandise.", "soldiers_interrogation_4",[]],
##  [anyone|plyr,"soldiers_interrogation_3", [], "I am just admiring the sights.", "soldiers_interrogation_4",[]],
##  [anyone,"soldiers_interrogation_4", [], "Hmm. All right. You may go now. But be careful. There is a war going on. The roads are not safe for travellers.", "close_window",[(assign, "$g_leave_encounter",1)]],





# Bandits
##  [party_tpl|pt_woku_pirates,"start", [(this_or_next|eq, "$g_encountered_party_template", "pt_woku_pirates"),(eq, "$g_encountered_party_template", "pt_shinano_rebels"),
##                                           (eq,"$talk_context",tc_party_encounter),
##                                           (party_get_slot,":protected_until_hours", "$g_encountered_party",slot_party_ignore_player_until),
##                                           (store_current_hours,":cur_hours"),
##                                           (store_sub, ":protection_remaining",":protected_until_hours",":cur_hours"),
##                                           (ge, ":protection_remaining", 0)], "What do you want?\
## You want to pay us some more money?", "bandit_paid_talk",[]],
##
##  [anyone|plyr,"bandit_paid_talk", [], "Sorry to trouble you. I'll be on my way now.", "bandit_paid_talk_2a",[]],
##  [anyone,"bandit_paid_talk_2a", [], "Yeah. Stop fooling around and go make some money.\
## I want to see that purse full next time I see you.", "close_window",[(assign, "$g_leave_encounter",1)]],
##  [anyone|plyr,"bandit_paid_talk", [], "No. It's your turn to pay me this time.", "bandit_paid_talk_2b",[]],
##  [anyone,"bandit_paid_talk_2b", [], "What nonsense are you talking about? You want trouble? You got it.", "close_window",[
##       (party_set_slot,"$g_encountered_party",slot_party_ignore_player_until,0),
##       (party_ignore_player, "$g_encountered_party", 0),
##    ]],

# Ryan BEGIN
  [party_tpl|pt_woku_pirates|auto_proceed,"start", [(eq,"$talk_context",tc_party_encounter),(encountered_party_is_attacker)],
   "{!}Warning: This line should never display.", "bandit_introduce",[]],
  [party_tpl|pt_shinano_rebels|auto_proceed,"start", [(eq,"$talk_context",tc_party_encounter),(encountered_party_is_attacker)],
   "{!}Warning: This line should never display.", "bandit_introduce",[]],
  [party_tpl|pt_kanto_rebels|auto_proceed,"start", [(eq,"$talk_context",tc_party_encounter),(encountered_party_is_attacker)],
   "{!}Warning: This line should never display.", "bandit_introduce",[]],
  [party_tpl|pt_seto_pirates|auto_proceed,"start", [(eq,"$talk_context",tc_party_encounter),(encountered_party_is_attacker)],
   "{!}Warning: This line should never display.", "bandit_introduce",[]],
  [party_tpl|pt_northern_raiders|auto_proceed,"start", [(eq,"$talk_context",tc_party_encounter),(encountered_party_is_attacker)],
   "{!}Warning: This line should never display.", "bandit_introduce",[]],
  #gekokujo 3.0 new bandit types start
  [party_tpl|pt_monk_rebels|auto_proceed,"start", [(eq,"$talk_context",tc_party_encounter),(encountered_party_is_attacker)],
   "{!}Warning: This line should never display.", "bandit_introduce",[]],
#    ], "{s5}", "bandit_talk",[(play_sound,"snd_encounter_bandits")]],
#gekokujo 3.0 no more bandit talk end

  [anyone|plyr,"bandit_talk", [], "I'll give you nothing but cold steel, you scum!", "close_window",[[encounter_attack]]],
  [anyone,"start", [(this_or_next|eq, "$g_encountered_party_template", "pt_woku_pirates"),(eq, "$g_encountered_party_template", "pt_shinano_rebels")],
   "Eh? What is it?", "bandit_meet",[]],
# Ryan END



  [party_tpl|pt_rescued_prisoners,"start", [(eq,"$talk_context",tc_party_encounter)], "Do you want us to follow you?", "disbanded_troop_ask",[]],
  [anyone|plyr,"disbanded_troop_ask", [], "Yes. Let us ride together.", "disbanded_troop_join",[]],
  [anyone|plyr,"disbanded_troop_ask", [], "No. Not at this time.", "close_window",[(assign, "$g_leave_encounter",1)]],
  [anyone,"disbanded_troop_join", [[neg|party_can_join]], "Unfortunately. You do not have room in your party for us.", "close_window",[(assign, "$g_leave_encounter",1)]],
  [anyone,"disbanded_troop_join", [], "We are at your command.", "close_window",[[party_join],(assign, "$g_leave_encounter",1)]],
  [party_tpl|pt_enemy,"start", [(eq,"$talk_context",tc_party_encounter)], "You will not capture me again. Not this time.", "enemy_talk_1",[]],
  [party_tpl|pt_enemy|plyr,"enemy_talk_1", [], "You don't have a chance against me. Give up.", "enemy_talk_2",[]],
  [party_tpl|pt_enemy,"enemy_talk_2", [], "I will give up when you are dead!", "close_window",[[encounter_attack]]],
######################################
# ROUTED WARRIORS
######################################

  [party_tpl|pt_routed_warriors, "start", [(eq,"$talk_context",tc_party_encounter)],
   "I beg you, please leave us alone.", "party_encounter_routed_agents_are_caught",
   []],
  [party_tpl|pt_routed_warriors|plyr, "party_encounter_routed_agents_are_caught", [],
   "Do you think you can run away from me? You will be my prisoner or die!", "party_encounter_routed_agents_are_caught2",
   []],
  [party_tpl|pt_routed_warriors|plyr,"party_encounter_routed_agents_are_caught", [],
   "Ok. We'll leave you in peace for this time, do not face with us again.", "close_window", [(assign, "$g_leave_encounter",1)]],
  [party_tpl|pt_routed_warriors, "party_encounter_routed_agents_are_caught2",
   [
     #(store_party_size_wo_prisoners, ":routed_party_size", "$g_encountered_party"),
     #(store_party_size_wo_prisoners, ":main_party_size", "p_main_party"),

    # calculate power of routed party
    (assign, ":routed_party_power", 0),
    (party_get_num_companion_stacks, ":num_stacks", "$g_encountered_party"),
    (try_for_range, ":i_stack", 0, ":num_stacks"),
      (party_stack_get_troop_id, ":stack_troop", "$g_encountered_party", ":i_stack"),
      (store_character_level, ":troop_level", ":stack_troop"),
      (try_begin),
        (troop_is_mounted, ":stack_troop"),
        (val_add, ":troop_level", 5),
      (try_end),
      (party_stack_get_size, ":stack_size", "$g_encountered_party", ":i_stack"),
      (val_mul, ":troop_level", ":stack_size"),
      (val_add, ":routed_party_power", ":troop_level"),
    (try_end),

    # calculate power of our party
    (assign, ":main_party_power", 0),
    (party_get_num_companion_stacks, ":num_stacks", "p_main_party"),
    (try_for_range, ":i_stack", 0, ":num_stacks"),
      (party_stack_get_troop_id, ":stack_troop", "p_main_party", ":i_stack"),
      (store_character_level, ":troop_level", ":stack_troop"),
      (try_begin),
        (troop_is_mounted, ":stack_troop"),
        (val_add, ":troop_level", 5),
      (try_end),
      (party_stack_get_size, ":stack_size", "p_main_party", ":i_stack"),
      (val_mul, ":troop_level", ":stack_size"),
      (val_add, ":main_party_power", ":troop_level"),
    (try_end),

    (store_div, ":main_party_power_divided_by_5", ":main_party_power", 5),

    #find num attached parties to routed warriors
    (party_get_num_attached_parties, ":num_attached_parties", "$g_encountered_party"),

    (this_or_next|gt, ":num_attached_parties", 0), #always fight
    (ge, ":routed_party_power", ":main_party_power_divided_by_5"),
    ],
   "Haven't you got any mercy? Ok, we will fight you to the last man!", "close_window",
   []],
  [party_tpl|pt_routed_warriors, "party_encounter_routed_agents_are_caught2",
    [
      #(store_party_size_wo_prisoners, ":routed_party_size", "$g_encountered_party"),
      #(store_party_size_wo_prisoners, ":main_party_size", "p_main_party"),

      # calculate power of routed party
      (assign, ":routed_party_population", 0),
      (assign, ":routed_party_power", 0),
      (party_get_num_companion_stacks, ":num_stacks", "$g_encountered_party"),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop", "$g_encountered_party", ":i_stack"),
        (store_character_level, ":troop_level", ":stack_troop"),
        (try_begin),
          (troop_is_mounted, ":stack_troop"),
          (val_add, ":troop_level", 5),
        (try_end),
        (party_stack_get_size, ":stack_size", "$g_encountered_party", ":i_stack"),
        (val_mul, ":troop_level", ":stack_size"),
        (val_add, ":routed_party_power", ":troop_level"),
        (val_add, ":routed_party_population", ":stack_size"),
      (try_end),

      # calculate power of our party
      (assign, ":main_party_power", 0),
      (party_get_num_companion_stacks, ":num_stacks", "p_main_party"),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop", "p_main_party", ":i_stack"),
        (store_character_level, ":troop_level", ":stack_troop"),
        (try_begin),
          (troop_is_mounted, ":stack_troop"),
          (val_add, ":troop_level", 5),
        (try_end),
        (party_stack_get_size, ":stack_size", "p_main_party", ":i_stack"),
        (val_mul, ":troop_level", ":stack_size"),
        (val_add, ":main_party_power", ":troop_level"),
      (try_end),

      (store_div, ":main_party_power_divided_by_5", ":main_party_power", 5),
      (lt, ":routed_party_power", ":main_party_power_divided_by_5"),

      (store_party_size_wo_prisoners, ":routed_party_size", "$g_encountered_party"),
      (assign, reg3, ":routed_party_size"),

      (try_begin),
        (gt, ":routed_party_population", 1),
        (str_store_string, s1, "str_we_resign"),
      (else_try),
        (str_store_string, s1, "str_i_resign"),
      (try_end),
    ],
    "{s1}", "close_window",
    [(assign,"$g_enemy_surrenders", 1),
     (call_script, "script_party_wound_all_members", "$g_encountered_party"),
     (call_script, "script_party_copy", "p_total_enemy_casualties", "$g_encountered_party"),
     #(change_screen_exchange_with_party, "$g_encountered_party"),
     ]],
  #[party_tpl|pt_routed_warriors,"close_window_anythink_else", [],
  # "Anythink else.", "close_window", [(assign, "$g_leave_encounter",1)]],


# Ryan BEGIN
  [anyone,"sell_prisoner_outlaws", [[store_troop_kind_count,0,"trp_looter"],[ge,reg(0),1],[assign,reg(1),reg(0)],[val_mul,reg(1),10],[val_mul,reg(2),reg(0)],[val_mul,reg(2),10]],
   "Hmmm. 10 mon for each looter makes {reg1} mon for all {reg0} of them.", "sell_prisoner_outlaws",
   [[call_script, "script_troop_add_gold", "trp_player", reg(1)],[add_xp_to_troop,reg(2)],[remove_member_from_party,"trp_looter"]]],
# Ryan END

  [anyone|plyr,"prisoner_chat", [], "Do not try running away or trying something stupid. I will be watching you.", "prisoner_chat_2",[]],
  [anyone,"prisoner_chat_2", [], "No, I swear I won't.", "close_window",[]],
  [anyone,"start", [(party_slot_eq, "$current_town", slot_town_lord, "trp_player"),
                    (this_or_next|is_between,"$g_talk_troop",weapon_merchants_begin,weapon_merchants_end),
                    (this_or_next|is_between,"$g_talk_troop",armor_merchants_begin, armor_merchants_end),
                    (             is_between,"$g_talk_troop",horse_merchants_begin, horse_merchants_end),
					##diplomacy start+
					#Replace "your lordship" with "your highness" if appropriate.
					(call_script,"script_dplmc_print_subordinate_says_sir_madame_to_s0"),
					(try_begin),
						(le, reg0, 2),
						(str_store_string, s0, "str_dplmc_my_lordlady"),
						(call_script, "script_dplmc_store_troop_is_female",  "trp_player"),
						(neq, reg0, 1),
						(str_store_string, s0, "@your lordship"),
					(try_end),
                    ],
   "Greetings, {s0}. How can I serve you today?", "town_merchant_talk",[]],
#change {your lordship/my lady} to {s0}
   ##diplomacy end+

  [anyone,"start", [(this_or_next|is_between,"$g_talk_troop",weapon_merchants_begin,weapon_merchants_end),
                    (this_or_next|is_between,"$g_talk_troop",armor_merchants_begin, armor_merchants_end),
                    (             is_between,"$g_talk_troop",horse_merchants_begin, horse_merchants_end)], "Good day. What can I do for you?", "town_merchant_talk",[]],
##  [anyone,"start", [(eq, "$talk_context", 0),
##                    (is_between,"$g_talk_troop",walkers_begin, walkers_end),
##                    (eq, "$sneaked_into_town",1),
##                     ], "Stay away beggar!", "close_window",[]],

  [anyone,"start", [(eq, "$talk_context", 0),
                    (is_between,"$g_talk_troop",walkers_begin, walkers_end),
                    (party_slot_eq, "$current_town", slot_town_lord, "trp_player"),
                     ], "My {lord/lady}?", "town_dweller_talk",[(assign, "$welfare_inquired",0),(assign, "$rumors_inquired",0),(assign, "$info_inquired",0)]],
  [anyone,"start", [(eq, "$talk_context", 0),
                    (is_between,"$g_talk_troop",walkers_begin, walkers_end),
					##diplomacy start+ replace {sir/madame} with {my lord/my lady} or {your highness} as appropriate
					(call_script,"script_dplmc_print_subordinate_says_sir_madame_to_s0"),
                     ], "Good day, {s0}.", "town_dweller_talk",[(assign, "$welfare_inquired", 0),(assign, "$rumors_inquired",0),(assign, "$info_inquired",0)]],
  [anyone,"start", [(eq, "$talk_context", 0),
                    (is_between,"$g_talk_troop",regular_troops_begin, regular_troops_end),
                    (party_slot_eq,"$current_town",slot_town_lord, "trp_player"),
					#diplomacy start+ replace {sir/madame} with {my lord/my lady} or {your highness} if appropriate
   				    (call_script, "script_dplmc_print_subordinate_says_sir_madame_to_s0"),
                     ], "Yes {s0}?", "player_castle_guard_talk",[]],
#diplomacy end+
  [anyone|plyr,"player_castle_guard_talk", [], "How goes the watch, soldier?", "player_castle_guard_talk_2",[]],
  #diplomacy start+ replace {sir/madame} with {my lord/my lady} or {your highness} if appropriate
  [anyone,"player_castle_guard_talk_2", [], "All is quiet {s0}. Nothing to report.", "player_castle_guard_talk_3",[]],
  #diplomacy end+
  [anyone|plyr,"player_castle_guard_talk_3", [], "Good. Keep your eyes open.", "close_window",[]],
  [anyone,"start", [(eq, "$talk_context", 0),
                    (is_between,"$g_talk_troop",regular_troops_begin, regular_troops_end),
                    (is_between,"$g_encountered_party_faction",kingdoms_begin, kingdoms_end),
                    (eq, "$players_kingdom", "$g_encountered_party_faction"),
                    (troop_slot_ge, "trp_player", slot_troop_renown, 100),
                    (str_store_party_name, s10, "$current_town"),
					#diplomacy start+ replace {sir/madame} with {my lord/my lady} or {your highness} if appropriate
   				    (call_script, "script_dplmc_print_subordinate_says_sir_madame_to_s0"),
                     ], "Good day, {s0}. Always an honor to have you here in {s10}.", "close_window",[]],
					#diplomacy end+
                    
  #gekokujo 3.1 ninja bodyguards while walking around start
  [anyone,"start", [(eq, "$talk_context", 0),
                    (this_or_next|is_between, "$g_talk_troop", "trp_yojimbo", "trp_mercenaries_end"),
                    (is_between, "$g_talk_troop", "trp_female_agent", "trp_refugee"),
                    (is_between,"$g_encountered_party_faction",kingdoms_begin, kingdoms_end),
                     ], "Sir?", "close_window",[]],
  #gekokujo 3.1 ninja bodyguards while walking around end

  [anyone,"start", [(eq, "$talk_context", 0),
                    (is_between,"$g_talk_troop",regular_troops_begin, regular_troops_end),
                    (is_between,"$g_encountered_party_faction",kingdoms_begin, kingdoms_end),
                     ], "Mind your manners and we'll have no trouble.", "close_window",[]],
  [anyone,"start", [(eq, "$talk_context", tc_court_talk),
                    (is_between,"$g_talk_troop",regular_troops_begin, regular_troops_end),
                    (is_between,"$g_encountered_party_faction",kingdoms_begin, kingdoms_end),
                    (party_slot_eq,"$current_town",slot_town_lord, "trp_player"),
					#diplomacy start+ replace {my lord/my lady} with {your highness} if appropriate
					(call_script, "script_dplmc_print_subordinate_says_sir_madame_to_s0"),
                     ], "Your orders, {s0}?", "hall_guard_talk",[]],
					#diplomacy end+

  [anyone,"start", [(eq, "$talk_context", tc_court_talk),
                    (is_between,"$g_talk_troop",regular_troops_begin, regular_troops_end),
                    (is_between,"$g_encountered_party_faction",kingdoms_begin, kingdoms_end),
					#diplomacy start+ replace {sir/madame} with {my lord/my lady} or {your highness} if appropriate
   				    (call_script, "script_dplmc_print_subordinate_says_sir_madame_to_s0"),
                     ], "We are not supposed to talk while on guard, {s0}.", "close_window",[]],
                    #diplomacy end+
  [anyone|plyr,"hall_guard_talk", [], "Stay on duty and let me know if anyone comes to see me.", "hall_guard_duty",[]],
  #diplomacy start+ replace {sir/madame} with {my lord/my lady} or {your highness} if appropriate
  [anyone,"hall_guard_duty", [(call_script, "script_dplmc_print_subordinate_says_sir_madame_to_s0"),], "Yes, {s0}. As you wish.", "close_window",[]],
  #diplomacy end+

  [anyone|plyr,"hall_guard_talk", [
  (eq, 1, 0),
  ], "I want you to arrest this man immediately!", "hall_guard_arrest",[]],
  #diplomacy start+ replace {sir/madame} with {my lord/my lady} or {your highness} if appropriate
  [anyone,"hall_guard_arrest", [(call_script, "script_dplmc_print_subordinate_says_sir_madame_to_s0"),], "Who do you want arrested {s0}?", "hall_guard_arrest_2",[]],
  #diplomacy end+
  [anyone|plyr,"hall_guard_arrest_2", [], "Ah, never mind my high spirits.", "close_window",[]],
  [anyone|plyr,"hall_guard_arrest_2", [], "Forget it. I will find another way to deal with this.", "close_window",[]],
  [anyone,"enemy_defeated", [], "Arggh! I hate this.", "close_window",[]],
  [anyone,"party_relieved", [], "Thank you for helping us against those bastards.", "close_window",[]],
  #gekokujo 3.0 no more bandit talk start
  #[anyone,"start", [(eq,"$talk_context", tc_party_encounter),(store_encountered_party, reg(5)),(party_get_template_id,reg(7),reg(5)),(eq,reg(7),"pt_kinai_rebels")],
  # "I will drink from your skull!", "battle_reason_stated",[(play_sound,"snd_encounter_kinai_rebels")]],
  [anyone,"start", [(eq,"$talk_context", tc_party_encounter),(store_encountered_party, reg(5)),(party_get_template_id,reg(7),reg(5)),(eq,reg(7),"pt_kinai_rebels")],
   "Prepare to die!", "battle_reason_stated",[]],
  [anyone|plyr,"regular_member_talk", [], "Tell me about yourself", "view_regular_char_requested",[]],
  [anyone,"view_regular_char_requested", [(call_script, "script_dplmc_print_subordinate_says_sir_madame_to_s0"),], "Aye {s0}. Let me tell you all there is to know about me.", "do_regular_member_view_char",[[change_screen_view_character]]],
##diplomacy end+
  [anyone,"do_regular_member_view_char", [], "Anything else?", "regular_member_talk",[]],
##diplomacy start+
#Allow viewing (but not changing) of the equipment of the troops you are leading.
#Code credit to rubik's Custom Commander, with minor string changes.
## CC view regular's equipment
  [anyone|plyr,"regular_member_talk", [],
   "Let me see your equipment.", "dplmc_view_regular_inventory", []
  ],
## CC view regular's equipment
##diplomacy end+

  [anyone|plyr,"regular_member_talk", [], "Nothing. Keep moving.", "close_window",[]],
######################################
# GENERIC PARTY ENCOUNTER
######################################

  [anyone,"start", [(eq,"$talk_context",tc_party_encounter),
                    (gt,"$encountered_party_hostile",0),
                    (encountered_party_is_attacker),
                    ],
#gekokujo 3.0 no more bandit talk start
   "You have no chance against us. Surrender now or we will kill you all...", "party_encounter_hostile_attacker",[]],
#   "You have no chance against us. Surrender now or we will kill you all...", "party_encounter_hostile_attacker",
#   [(try_begin),
#      (eq,"$g_encountered_party_template","pt_seto_pirates"),
#      (play_sound, "snd_encounter_seto_pirates"),
#    (try_end)]],
#gekokujo 3.0 no more bandit talk end
   
#  [anyone|plyr,"party_encounter_hostile_attacker", [
#                    ],
#   "I will pay you 1000 mon if you just let us go.", "close_window", []],
  [anyone|plyr,"party_encounter_hostile_attacker", [
                    ],
   "We will fight you to the end!", "close_window", []],
  [anyone|plyr,"party_encounter_hostile_attacker", [
                    ],
   "Don't attack! We surrender.", "close_window", [(assign,"$g_player_surrenders",1)]],
  [anyone,"start", [(eq,"$talk_context",tc_party_encounter),
                    (neg|encountered_party_is_attacker),
                    ],
   "What do you want?", "party_encounter_hostile_defender",
   []],
  [anyone|plyr,"party_encounter_hostile_defender", [],
   "Surrender or die!", "party_encounter_hostile_ultimatum_surrender", [

       ]],
#post 0907 changes begin
  [anyone,"party_encounter_hostile_ultimatum_surrender", [],
   "{s43}", "close_window", [
       (call_script, "script_lord_comment_to_s43", "$g_talk_troop", "str_lord_challenged_default"),
       ]],
#post 0907 changes end

  [anyone|plyr,"party_encounter_hostile_defender", [],
   "Nothing. We'll leave you in peace.", "close_window", [(assign, "$g_leave_encounter",1)]],
  [anyone|auto_proceed, "start",
  [
    (is_between, "$g_talk_troop", "trp_tsu_merchant", "trp_startup_merchants_end"),
    (check_quest_active, "qst_collect_men"),
    #(neq, "$talk_context", tc_tavern_talk),
    #(neq, "$talk_context", tc_back_alley),
    (eq, "$talk_context", tc_merchants_house),
  ],
  "{!}.", "merchant_end", []],
  [anyone, "start",
  [
    (is_between, "$g_talk_troop", "trp_tsu_merchant", "trp_startup_merchants_end"),
    (eq, "$talk_context", tc_merchants_house),
    (check_quest_active, "qst_save_town_from_bandits"),

    (store_div, ":number_of_civilian_loses_div_2", "$number_of_civilian_loses", 2),

    (try_begin),
      (eq, "$g_killed_first_bandit", 1),
      (store_add, ":player_success", "$number_of_bandits_killed_by_player", 1),
    (else_try),
      (store_add, ":player_success", "$number_of_bandits_killed_by_player", 0),
    (try_end),

    (val_sub, ":player_success", ":number_of_civilian_loses_div_2"),
    (val_max, ":player_success", 0),

    (call_script, "script_change_player_relation_with_center", "$g_starting_town", ":player_success"),

    (try_begin),
      (eq, "$g_killed_first_bandit", 1),
      (gt, "$number_of_bandits_killed_by_player", 2),
      (str_store_string, s3, "str_you_fought_well_at_town_fight_survived"),
      (troop_add_gold, "trp_player", 200),
    (else_try),
      (eq, "$g_killed_first_bandit", 1),
      (gt, "$number_of_bandits_killed_by_player", 0),
      (str_store_string, s3, "str_you_fought_normal_at_town_fight_survived"),
      (troop_add_gold, "trp_player", 200),
    (else_try),
      (eq, "$g_killed_first_bandit", 1),
      (eq, "$number_of_bandits_killed_by_player", 0),
      (str_store_string, s3, "str_you_fought_bad_at_town_fight_survived"),
      (troop_add_gold, "trp_player", 100),
    (else_try),
      (eq, "$g_killed_first_bandit", 0),
      (ge, "$number_of_bandits_killed_by_player", 2),
      (str_store_string, s3, "str_you_fought_well_at_town_fight"),
      (troop_add_gold, "trp_player", 100),
    (else_try),
      (str_store_string, s3, "str_you_wounded_at_town_fight"),
      (troop_add_gold, "trp_player", 100),
    (try_end),

    (try_begin),
      (ge, "$number_of_civilian_loses", 1),
      (assign, reg0, "$number_of_civilian_loses"),
      (str_store_string, s2, "str_unfortunately_reg0_civilians_wounded_during_fight_more"),
    (else_try),
      (eq, "$number_of_civilian_loses", 1),
      (assign, reg0, "$number_of_civilian_loses"),
      (str_store_string, s2, "str_unfortunately_reg0_civilians_wounded_during_fight"),
    (else_try),
      (str_store_string, s2, "str_also_one_another_good_news_is_any_civilians_did_not_wounded_during_fight"),
    (try_end),

    (call_script, "script_succeed_quest", "qst_save_town_from_bandits"),
    (call_script, "script_end_quest", "qst_save_town_from_bandits"),
  ],
  "{s3}{s2}", "merchant_quest_4e",
  []],
  #[anyone|auto_proceed, "start",
  #[
  #  (is_between, "$g_talk_troop", "trp_tsu_merchant", "trp_startup_merchants_end"),
  #  (eq, "$talk_context", tc_merchants_house),
  #  (check_quest_finished, "qst_save_town_from_bandits"),
  #],
  #"{!}.", "merchant_all_quest_completed",
  #[
  #]],


  [anyone|plyr,"merchant_quest_4e",
  [
  ],
  "Heaven alone grants us victory.", "merchant_finale",
[  (assign, "$dialog_with_merchant_ended", 1),
  ]],
  [anyone, "start",
  [
    (is_between, "$g_talk_troop", "trp_tsu_merchant", "trp_startup_merchants_end"),
    (eq, "$talk_context", tc_merchants_house),
    (neg|check_quest_finished, "qst_collect_men"),
    (eq, "$current_startup_quest_phase", 1),

    (try_begin),
      (eq, "$g_killed_first_bandit", 1),
      (str_store_string, s1, "str_are_you_all_right"),
    (else_try),
      (str_store_string, s1, "str_you_are_awake"),
    (try_end),
  ],
  "{s1}", "merchant_quest_1_prologue_1",
  []],
#gekokujo 3.0 microfactions! start

  #guard troops when you talk to them
  [anyone, "start", [
      (is_between, "$g_talk_troop", fort_troops_begin, fort_troops_end),
      (store_sub, ":offset", "$current_town", forts_begin),
      (store_add, ":guard_talk", "str_gekokujo_fort_1_guard_talk", ":offset"),
      (str_store_string, s45, ":guard_talk"),
    ], "{s45}", "close_window", []],
  #deputy's line when player conquers their fort
  [anyone, "start", [
      (is_between, "$g_talk_troop", fort_deputies_begin, fort_deputies_end),
	  (eq, "$g_talk_troop_met", 0),
      (store_sub, ":offset", "$current_town", forts_begin),
      (store_add, ":deputy_talk", "str_gekokujo_fort_1_deputy_conquer", ":offset"),
      (str_store_string, s45, ":deputy_talk"),
    ], "{s45}","fort_conquest_response", []],
  #player's response to deputy when they conquer their fort
  [anyone|plyr, "fort_conquest_response", [
      (store_sub, ":offset", "$current_town", forts_begin),
      (store_add, ":conquer_response", "str_gekokujo_fort_1_deputy_conquer_response", ":offset"),
      (str_store_string, s46, ":conquer_response"),
    ], "{s46}","close_window", []],
  #deputy's line when you talk to them
  [anyone, "start", [
      (is_between, "$g_talk_troop", fort_deputies_begin, fort_deputies_end),
	  (neq, "$g_talk_troop_met", 0),
      (store_sub, ":offset", "$current_town", forts_begin),
      (store_add, ":deputy_talk", "str_gekokujo_fort_1_deputy_intro", ":offset"),
      (str_store_string, s45, ":deputy_talk"),
    ], "{s45}","fort_deputy_discuss_options", []],
  
  #potential companion's line when you talk to them (first time)
  [anyone, "start", [
      (is_between, "$g_talk_troop", fort_companions_begin, fort_companions_end),
	  (eq, "$g_talk_troop_met", 0),
      (store_sub, ":offset", "$current_town", forts_begin),
      (store_add, ":companion_talk", "str_gekokujo_fort_1_companion_meet", ":offset"),
      (str_store_string, s45, ":companion_talk"),
    ], "{s45}","fort_companion_discuss_options", []],
	
  #potential companion's line when you talk to them (normal)
  [anyone, "start", [
      (is_between, "$g_talk_troop", fort_companions_begin, fort_companions_end),
	  (neq, "$g_talk_troop_met", 0),
      (store_sub, ":offset", "$current_town", forts_begin),
      (store_add, ":companion_talk", "str_gekokujo_fort_1_companion_intro", ":offset"),
      (str_store_string, s45, ":companion_talk"),
    ], "{s45}","fort_companion_discuss_options", []],
	
  [anyone, "fort_companion_discuss", [], "Anything else?","fort_companion_discuss_options", []],
  
  #companion - ask them about themselves
  [anyone|plyr, "fort_companion_discuss_options", [], 
    "Could you tell me a little about yourself?", "fort_companion_discuss_companion", []],
  [anyone, "fort_companion_discuss_companion", [
      (store_sub, ":offset", "$current_town", forts_begin),
      (store_add, ":companion_talk", "str_gekokujo_fort_1_companion_about", ":offset"),
      (str_store_string, s45, ":companion_talk"),
    ], "{s45}","fort_companion_discuss", []],
  
  #companion - ask them to rejoin
  [anyone|plyr, "fort_companion_discuss_options", [
      (party_slot_eq, "$current_town", slot_fort_npc_2_state, 2), #temporarily returned
	  (party_get_free_companions_capacity, ":free_capacity","p_main_party"),
	  (ge, ":free_capacity", 1),
    ], 
    "I would like for you to rejoin me.", "fort_companion_discuss_companion_rejoin", []],
  [anyone, "fort_companion_discuss_companion_rejoin", [], "Very well, {playername}.","fort_companion_discuss", [
	  (party_set_slot, "$current_town", slot_fort_npc_2_state, 3), #set to "companion recruited"
	  (call_script, "script_recruit_troop_as_companion", "$g_talk_troop")
	]],
	
  #companion - ask them to join 
  [anyone|plyr, "fort_companion_discuss_options", [
      (this_or_next|party_slot_eq, "$current_town", slot_fort_npc_2_state, 0), #haven't asked yet
      (party_slot_eq, "$current_town", slot_fort_npc_2_state, 1), #already asked, but haven't confirmed
	  (party_get_free_companions_capacity, ":free_capacity","p_main_party"),
	  (ge, ":free_capacity", 1),
    ], 
    "I would like for you to join me on my travels.", "fort_companion_discuss_companion_recruit", []],
  #companion - reply to player about asking to join
  [anyone, "fort_companion_discuss_companion_recruit", [
      (party_slot_eq, "$current_town", slot_fort_npc_2_state, 0), #haven't asked yet
      (store_sub, ":offset", "$current_town", forts_begin),
      (store_add, ":companion_talk", "str_gekokujo_fort_1_companion_recruit", ":offset"),
      (str_store_string, s45, ":companion_talk"),
    ], "{s45}", "fort_companion_discuss_companion_recruit_2", []],
  #companion - reply to player asking to join (if already asked -- allows changing your mind)
  [anyone, "fort_companion_discuss_companion_recruit", [
      (party_slot_eq, "$current_town", slot_fort_npc_2_state, 1), #already asked, but haven't confirmed
	  (party_get_slot, ":deputy", "$current_town", slot_fort_npc_1),
	  (str_store_troop_name, s2, ":deputy"),
    ], "Have you spoken to {s2} about allowing me to join you?", "fort_companion_discuss_companion_recruit_2", []],
	
  #companion - confirm about joining
  [anyone|plyr, "fort_companion_discuss_companion_recruit_2", [
      (party_slot_eq, "$current_town", slot_fort_npc_2_state, 0), #haven't asked yet
	], 
    "Yes. Please join me.", "fort_companion_discuss_companion_recruit_3", [
	  (party_set_slot, "$current_town", slot_fort_npc_2_state, 1), #set to "already asked"
	]],
	
  #companion - confirm reminder about talking to deputy
  [anyone|plyr, "fort_companion_discuss_companion_recruit_2", [
      (party_slot_eq, "$current_town", slot_fort_npc_2_state, 1), #already asked, but haven't confirmed
    ], 
    "Not yet.", "fort_companion_discuss", []],
	
  #companion - changing mind about recruitment
  [anyone|plyr, "fort_companion_discuss_companion_recruit_2", [], 
    "On second thought, forget it.", "fort_companion_discuss", [
	  (party_set_slot, "$current_town", slot_fort_npc_2_state, 0), #reset to "not asked"
	]],
	
  [anyone, "fort_companion_discuss_companion_recruit_3", [
      (party_get_slot, ":deputy", "$current_town", slot_fort_npc_1),
	  (str_store_troop_name, s2, ":deputy"),
    ], 
    "I would love to go, but it is not up to me. Please ask {s2} for permission on my behalf.", "fort_companion_discuss", []],
	  
  #companion - end dialogue
  [anyone|plyr,"fort_companion_discuss_options", [],
    "That is all for now.", "close_window", []],
  [anyone|plyr,"battle_reason_stated", [], "I am not afraid of you. I will fight.", "close_window",[[encounter_attack]]],
  [anyone,"start", [], "Hello. What can I do for you?", "free",[]],
  [anyone|plyr,"free", [[neg|in_meta_mission]], "Tell me about yourself", "view_char_requested",[]],
  [anyone,"view_char_requested", [], "Very well, listen to this...", "view_char",[[change_screen_view_character]]],
  [anyone,"view_char", [], "Anything else?", "free",[]],
  [anyone|plyr,"end", [], "[Done]", "close_window",[]],
  [anyone|plyr,"start", [], "Drop your weapons and surrender if you want to live", "threaten_1",[]],
  [anyone,"threaten_1", [], "We will fight you first", "end",[[encounter_attack]]],
#  [anyone|plyr,"free", [[partner_is_mercmaster]], "I need to hire some mercenaries.", "mercenaries_requested",[]],
#  [anyone,"mercenaries_requested", [], "I have the toughest fighters in all Calradia.", "buy_mercenaries",[[change_screen_buy_mercenaries]]],
#  [anyone,"buy_mercenaries", [], "Anything else?", "free",[]],

#  [anyone|plyr,"free", [[partner_is_recruitable]], "I need a capable sergeant like yourself. How much do you ask to work for me?", "employ_mercenary_requested",[]],
#  [anyone,"employ_mercenary_requested", [[store_mercenary_price,0],[store_mercenary_wage,1]], "I want {reg0} mon now and {reg1} mon as monthly payment.", "employ_mercenary_2",[]],
#  [anyone|plyr,"employ_mercenary_2", [], "I see I need to think of this.", "employ_mercenary_giveup",[]],
#  [anyone|plyr,"employ_mercenary_2", [[neg|hero_can_join]], "I don't have any more room in my party right now. I will talk to you again later.", "employ_mercenary_giveup",[]],
#  [anyone|plyr,"employ_mercenary_2", [[player_gold_ge,reg(0)],[hero_can_join]], "That's fine. Here's the {reg0} mon. From now on you work for me.", "employ_mercenary_commit",[[troop_remove_gold, "trp_player",reg(0)],[recruit_mercenary]]],
#  [anyone,"employ_mercenary_giveup", [], "Suits me.", "free",[]],
#  [anyone,"employ_mercenary_commit", [], "You got yourself the best fighter in the land.", "end",[]],


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
## Floris - Rebellion Option
##diplomacy end+

# #gekokujo 3.0 zaitenko's reinforcement script start
# # Reinforcements
  # [party_tpl|pt_reinforcements,"start", [(eq,"$talk_context",tc_party_encounter),
                                         # (party_get_slot, ":ai_object", "$g_encountered_party", slot_party_ai_object),
                                         # (str_store_party_name,s21,":ai_object"),
                                         # (str_store_party_name, s20, "$g_encountered_party")],
   # "Refrain from approaching!\ We are {s20}, on our way to {s21}.", "reinforcements_intro",[]],
  # [anyone|plyr, "reinforcements_intro", [], "I am {playername}. I'm just passing by.", "close_window",[]],
  # [anyone|plyr, "reinforcements_intro", [], "I am {playername}. I'm here to stop you from reaching your destination!", "reinforcement_hostile",[]],
  # [party_tpl|pt_reinforcements,"reinforcement_hostile", [(faction_get_slot, ":faction_leader", "$g_encountered_party_faction",slot_faction_leader),
                                                         # (str_store_troop_name, s9, ":faction_leader"),],
                                                         # "Then we shall deliver your head to {s9}!", "reinforcements_attack",[]],
  # [anyone|plyr, "reinforcements_attack", [], "I will kill him next when I'm done with you!", "close_window",[(call_script, "script_make_kingdom_hostile_to_player", "$g_encountered_party_faction", -1),
                                                                                                                          # (encounter_attack,0)]],
  # [anyone|plyr, "reinforcements_attack", [], "There has been a misunderstanding. You may go.", "close_window",[]],
# #gekokujo 3.0 zaitenko's reinforcement script end

  [anyone|plyr,"free", [[in_meta_mission]], " Good-bye.", "close_window",[]],
  [anyone|plyr,"free", [[neg|in_meta_mission]], " [Leave]", "close_window",[]],
#  [anyone,"free", [], "NO MATCHING SENTENCE!", "close_window",[]],

# LAV MODIFICATIONS START (COMPANIONS OVERSEER MOD)
  [anyone, "lco_conversation_end", [(troop_is_hero,"$g_lco_target"),(assign,"$g_lco_operation",lco_run_presentation)], "Nice to know you are not forgetting me!", "close_window", [(change_screen_return)]],
]
