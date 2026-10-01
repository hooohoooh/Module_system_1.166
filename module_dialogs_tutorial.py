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


dialogs_tutorial = [
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
[anyone, "tutorial_troop_default",
[
(try_begin),
 (eq, "$g_tutorial_training_ground_intro_message_being_displayed", 1),
 (assign, "$g_tutorial_training_ground_intro_message_being_displayed", 0),
 (tutorial_message, -1), #remove tutorial intro immediately before a conversation
(try_end),
],
"Hey, I am trying to practice here. Go, talk with the archery trainer if you need guidance about ranged weapons.", "close_window", []],
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
[anyone, "start",
[
(eq, "$g_talk_troop", "trp_fight_promoter"),
],
"You look like someone who can take a few hard knocks -- and deal them out, too. I have a business proposition for you.", "fistfight_response", [
]],
[trp_ramun_the_slave_trader, "start", [
(troop_slot_eq, "$g_talk_troop", slot_troop_met_previously, 0),
], "Good day to you, {young man/lassie}.", "ramun_introduce_1",[]],
[trp_ramun_the_slave_trader,"start", [], "Hello, {playername}.", "ramun_talk",[]],
[trp_nurse_for_lady, "start", [
#  (eq, "$talk_context", tc_garden),
##diplomacy start+ just in case make gender-correct
], "I humbly request that your {lordship/ladyship} keeps {his/her} hands where I can see them.", "close_window",[]],
[party_tpl|pt_manhunters,"start", [(eq,"$talk_context",tc_party_encounter)], "Hey, you there! You seen any bandits around here?", "manhunter_talk_b",[]],
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
[anyone,"start", [(troop_slot_eq,"$g_talk_troop", slot_troop_occupation, slto_player_companion),
              (neg|main_party_has_troop,"$g_talk_troop"),
              (eq, "$talk_context", tc_party_encounter)],
   "{!}Do you want me to rejoin you?", "close_window",[]],
[anyone,"start", [(neg|main_party_has_troop,"$g_talk_troop"),(eq, "$g_encountered_party", "p_four_ways_inn")], "{!}Do you want me to rejoin you?", "close_window",[]],
[trp_smithy_master, "start", [],"Good day {sir/madam}, will you be looking at my weapons?", "smithy_master_talk", []],
[trp_black_swordsman,"start",[[eq,"$brok_sword",0]],"Hello, stranger.", "swordmaster_talk",[]],
[trp_black_swordsman,"start", [[eq,"$brok_sword",1]], "Hello, {playername}.That you decide?", "swordmaster_help",[]],
[trp_black_swordsman, "start", [[eq,"$brok_sword",2]], "Did you find the sword?","sword_restored",[]],
[trp_black_swordsman, "start", [(eq,"$brok_sword",3)], "What?","black_question",[]],
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
[anyone|auto_proceed, "start",
[
(is_between, "$g_talk_troop", "trp_tsu_merchant", "trp_startup_merchants_end"),
(eq, "$talk_context", tc_back_alley),
(eq, "$talked_with_merchant", 0),
],
"{!}.", "start_up_quest_1_next",
[]],
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
[anyone, "start", [
			   #gekokujo 3.0 microfactions! include fort companions start
               #(is_between, "$g_talk_troop", companions_begin, companions_end),
               (is_between, "$g_talk_troop", companions_begin, fort_companions_end),
			   #gekokujo 3.0 microfactions! include fort companions end
               (eq, "$talk_context", tc_tavern_talk),
               (troop_slot_eq, "$g_talk_troop", slot_troop_current_mission, npc_mission_gather_intel)],
"Greetings, stranger.", "member_intel_liaison", []],
[anyone, "start", [
		(is_between, "$g_talk_troop", companions_begin, companions_end),
		(this_or_next|eq, "$talk_context", tc_tavern_talk),
		(this_or_next|eq, "$talk_context", tc_town_talk),
		(eq, "$talk_context", tc_court_talk),
		#(main_party_has_troop, "$g_talk_troop"), #gekokujo 3.1 why was this even on here
		(eq, "$freelancer_state", 2)
	],
	"{Sir/Madam}?^^(You're a troop, remember?)", "close_window", []],
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
[anyone, "start", [
    (is_between, "$g_talk_troop", companions_begin, companions_end),
    (neg|troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_hero),
    (troop_slot_eq, "$g_talk_troop", slot_troop_playerparty_history, pp_history_indeterminate),

    (troop_get_slot, ":prison_center", "$g_talk_troop", slot_troop_prisoner_of_party),
    (lt, ":prison_center", centers_begin),
  ], "My offer to rejoin you still stands, if you'll have me.", "companion_rehire", []],
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
[trp_dplmc_recruiter, "start", [
##diplomacy start+ replace {reg65?madame:sir} with {s0}.  Also replace "okay to you" with "okay with you".
(call_script, "script_dplmc_print_subordinate_says_sir_madame_to_s0"),
], "Hello {s0}. If it's ok with you, I would like to get on with my assignment.", "dplmc_recruiter_talk",[]],
[trp_dplmc_messenger, "start", [], "Greetings. Sorry but I don't have time to talk now. I am delivering a very important message to {s6}.", "dplmc_messenger_talk", []],
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
[anyone,"start",
[
(eq, "$g_player_chancellor","$g_talk_troop"),
],
##nested diplomacy start+ Change "Milord" to "Milord/Milady"
"{Milord/Milady}?", "dplmc_chancellor_talk",[
##nested diplomacy end+
]],
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
[anyone,"start", [(eq,"$talk_context",tc_hero_defeated),
              (troop_slot_eq,"$g_talk_troop",slot_troop_occupation, slto_kingdom_hero)],
"{s43}", "defeat_lord_answer",
[(troop_set_slot, "$g_talk_troop", slot_troop_leaded_party, -1),
(call_script, "script_lord_comment_to_s43", "$g_talk_troop", "str_surrender_offer_default"),
]],
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
[anyone ,"start", [(troop_slot_eq,"$g_talk_troop",slot_troop_occupation, slto_kingdom_hero),
               (eq, "$g_talk_troop_met", 0),
               (lt, "$g_talk_troop_faction_relation", 0),
#                     (str_store_faction_name, s4,  "$players_kingdom"),
               (le,"$talk_context",tc_siege_commander),
               ],
"{s43}", "lord_meet_enemy", [
(call_script, "script_lord_comment_to_s43", "$g_talk_troop", "str_enemy_meet_default"),
 ]],
[anyone ,"start", [(troop_slot_eq,"$g_talk_troop",slot_troop_occupation, slto_kingdom_hero),
               (le,"$talk_context",tc_siege_commander),
          (try_begin),
             ##diplomacy start+ Add commoner personalities
             (this_or_next|troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_roguish),
             ##diplomacy end+
             (this_or_next|troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_debauched),
               (troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_quarrelsome),
             (lt, "$g_talk_troop_relation", -15),
            (str_store_string, s8, "str_playername_come_to_plague_me_some_more_have_you"),
          (else_try),
             (lt, "$g_talk_troop_relation", -5),
            (str_store_string, s8, "str_ah_it_is_you_again"),
          (else_try),
            (str_store_string, s8, "str_well_playername"),
          (try_end),
               ],
"{s8}", "lord_start",
[]],
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
[anyone,"start", [(troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_seneschal),
                    (eq, "$talk_context", tc_siege_won_seneschal),
                    (str_store_party_name, s1, "$g_encountered_party"),
                    ],
   "I must congratulate you on your victory, my {lord/lady}. Welcome to {s1}.\
 We, the housekeepers of this castle, are at your service.", "siege_won_seneschal_1",[]],
[anyone,"start", [(troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_seneschal),(eq,"$g_talk_troop_met",0),(str_store_party_name,s1,"$g_encountered_party")],
   "Good day, {sir/madam}. I do nott believe I've seen you here before.\
 Let me extend my welcome to you as the seneschal of {s1}.", "seneschal_intro_1",[]],
[anyone,"start", [(troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_seneschal)],
   "Good day, {sir/madam}.", "seneschal_talk",[]],
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
[anyone,"start", [(eq, "$talk_context", 0),(faction_slot_eq, "$g_encountered_party_faction", slot_faction_prison_guard_troop, "$g_talk_troop")],
   "Yes? What do you want?", "prison_guard_talk",[]],
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
[anyone,"start", [(eq, "$talk_context", 0),(faction_slot_eq, "$g_encountered_party_faction", slot_faction_castle_guard_troop, "$g_talk_troop"),(eq, "$sneaked_into_town",1),
                    (gt,"$g_time_since_last_talk",0)],
   "Get out of my sight, beggar! You stink!", "castle_guard_sneaked_intro_1",[]],
[anyone,"start", [(eq, "$talk_context", 0),(faction_slot_eq, "$g_encountered_party_faction", slot_faction_castle_guard_troop, "$g_talk_troop"),(eq, "$sneaked_into_town",1)],
   "Get lost before I lose my temper you vile beggar!", "close_window",[]],
[anyone,"start", [(eq, "$talk_context", 0),(faction_slot_eq, "$g_encountered_party_faction", slot_faction_castle_guard_troop, "$g_talk_troop")],
   "What do you want?", "castle_guard_intro_1",[]],
[anyone,"start", [(eq, "$talk_context", tc_castle_gate)],
   "What do you want?", "castle_gate_guard_talk",[]],
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
[anyone,"start", [(eq,"$talk_context",tc_hero_defeated)],
   "You'll not live long to enjoy your victory. My kinsmen will soon wipe out the stain of this defeat.", "defeat_hero_answer",
   [
    ]],
[trp_local_merchant,"start", [], "Mercy! Please don't kill me!", "local_merchant_mercy",[]],
[trp_fugitive,"start", [], "What do you want?", "fugitive_1",[]],
[party_tpl|pt_sacrificed_messenger,"start", [],
   "Don't worry, {sir/madam}, I'm on my way.", "close_window",[(assign, "$g_leave_encounter",1)]],
[party_tpl|pt_spy,"start", [], "Good day {sir/madam}. Such fine weather don't you think? If you'll excuse me now I must go on my way.", "follow_spy_talk",[]],
[party_tpl|pt_spy_partners,"start", [], "Greetings.", "spy_partners_talk",[]],
[party_tpl|pt_runaway_serfs,"start", [(party_slot_eq, "$g_encountered_party", slot_town_center, 0)],#slot_town_center is used for first time meeting
   "Good day {sir/madam}.", "runaway_serf_intro_1",
   [(party_set_slot, "$g_encountered_party", slot_town_center, 1)]],
[party_tpl|pt_runaway_serfs,"start", [(party_slot_eq, "$g_encountered_party", slot_town_castle, 1),
                                        ],
   "Good day {sir/madam}. Don't worry. If anyone asks, we haven't seen you.", "runaway_serf_reconsider",[]],
[party_tpl|pt_runaway_serfs,"start", [(party_slot_eq, "$g_encountered_party", slot_town_castle, 0),
                                        (get_party_ai_object, ":cur_ai_object"),
                                        (quest_get_slot, ":home_center", "qst_bring_back_runaway_serfs", slot_quest_object_center),
                                        (neq, ":home_center", ":cur_ai_object")],
   "Good day {sir/madam}. We were heading back to {s5}, but I am afraid we lost our way.", "runaway_serf_talk_caught",[]],
[party_tpl|pt_runaway_serfs,"start",
   [(quest_get_slot, ":home_center", "qst_bring_back_runaway_serfs", slot_quest_object_center),
    (str_store_party_name, s5, ":home_center")], "We are on our way back to {s5} {sir/madam}.", "runaway_serf_talk_again_return",[]],
[anyone,"start", [
  (check_quest_active, "qst_track_down_bandits"),
  (quest_slot_eq, "qst_track_down_bandits", slot_quest_target_party, "$g_encountered_party"),
  (neg|is_between, "$g_encountered_party_faction", kingdoms_begin, kingdoms_end), #ie, the party has not respawned as a non-bandit
  ],
   "This must be your unlucky day. We're just about the worst people you could run into, in these parts.", "troublesome_bandits_intro_1",[
   ]],
[party_tpl|pt_deserters, "start", [(eq,"$talk_context",tc_party_encounter),
                                     (party_get_slot,":protected_until_hours", "$g_encountered_party",slot_party_ignore_player_until),
                                     (store_current_hours,":cur_hours"),
                                     (store_sub, ":protection_remaining",":protected_until_hours",":cur_hours"),
                                     (gt, ":protection_remaining", 0)], "What do you want?\
 You want to pay us some more money?", "deserter_paid_talk",[]],
[party_tpl|pt_deserters,"start", [
      (eq,"$talk_context",tc_party_encounter)
                    ], "We are the free brothers.\
 We will fight only for ourselves from now on.\
 Now give us your money or taste our steel.", "deserter_talk",[]],
[anyone ,"start", [(store_conversation_troop,reg(1)),(ge,reg(1),tavernkeepers_begin),(lt,reg(1),tavernkeepers_end)],
   "Good day dear {sir/madam}. How can I help you?", "tavernkeeper_talk",
   [
#    (store_encountered_party,reg(2)),
#    (party_get_slot,"$tavernkeeper_party",reg(2),slot_town_mercs),
    ]],
[anyone,"start", [(is_between, "$g_talk_troop", ransom_brokers_begin, ransom_brokers_end),
  ],
   "Greetings. If you have any prisoners, I will be happy to buy them from you.", "ransom_broker_talk",[]],
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
[anyone, "start", [(is_between, "$g_talk_troop", tavern_booksellers_begin, tavern_booksellers_end),
                     ],
   "Good day {sir/madam}, will you be looking at my books?", "bookseller_talk", []],
[anyone, "start", [(is_between, "$g_talk_troop", tavern_minstrels_begin, tavern_minstrels_end),
                     ],
   "Greetings to you, {most noble sir/most noble lady}.", "minstrel_1", []],
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
[anyone, "start", [
  (eq, "$talk_context", tc_tavern_talk),
  ],
   "Any orders, {sir/madam}?", "mercenary_after_recruited", []],
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
[anyone|auto_proceed,"start", [
  (is_between,"$g_talk_troop","trp_town_1_master_craftsman", "trp_zendar_chest"),
  (party_get_slot, ":days_until_complete", "$g_encountered_party", slot_center_player_enterprise_days_until_complete),
  (ge, ":days_until_complete", 2),
  (assign, reg4, ":days_until_complete"),
  ],
   "{!}.", "start_craftsman_soon",[]],
[anyone,"start", [
  (is_between,"$g_talk_troop","trp_town_1_master_craftsman", "trp_zendar_chest"),
  ],
   "Good day, my {lord/lady}. We are honored that you have chosen to visit us. What do you require?", "master_craftsman_talk",[]],
[anyone ,"start", [(is_between,"$g_talk_troop",mayors_begin,mayors_end),(eq,"$g_talk_troop_met",0),
                     (this_or_next|eq, "$players_kingdom", "$g_encountered_party_faction"),
                     (             eq, "$g_encountered_party_faction", "fac_player_supporters_faction"),
					 ##diplomacy start+
					 #Change "my lord" to "my lord/my lady" or "your highnes" as appropriate.
					 (call_script, "script_dplmc_print_subordinate_says_sir_madame_to_s0"),#Write {sir/madame} or replacement to {s0}
					 ],
   "Good day, {s0}.", "mayor_begin",[]],
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
[trp_kidnapped_girl,"start", [],
   "Oh {sir/madam}. Thank you so much for rescuing me. Will you take me to my family now?", "kidnapped_girl_liberated_map",[]],
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
[anyone,"start", [(is_between,"$g_talk_troop", village_elders_begin, village_elders_end),(eq,"$g_talk_troop_met",0),
                    (str_store_party_name, s9, "$current_town"),
					(call_script, "script_dplmc_print_commoner_at_arg1_says_sir_madame_to_s0", "$current_town"),#added this line
					],
   "Good day, {s0}, and welcome to {s9}. I am the elder of this village.", "village_elder_talk",[]],
[anyone ,"start", [(is_between,"$g_talk_troop",village_elders_begin,village_elders_end),
                     (party_slot_eq, "$current_town", slot_town_lord, "trp_player"),
					 #We aren't going to use the contents of {s0}, just checking the return value
					 (call_script, "script_dplmc_print_subordinate_says_sir_madame_to_s0"),
					 (ge, reg0, 3),#"your highness"
					 ],
   "You honour our humble village with your presence.", "village_elder_talk",[]],
[anyone ,"start", [(is_between,"$g_talk_troop",village_elders_begin,village_elders_end),
                     (party_slot_eq, "$current_town", slot_town_lord, "trp_player")],
   "{My lord/My lady}, you honour our humble village with your presence.", "village_elder_talk",[]],
[anyone ,"start", [(is_between,"$g_talk_troop",village_elders_begin,village_elders_end),
  ##diplomacy start+
  (call_script, "script_dplmc_print_commoner_at_arg1_says_sir_madame_to_s0", "$current_town"),
  ],
   "Good day, {s0}.", "village_elder_talk",[]],
[anyone ,"start", [(is_between,"$g_talk_troop",goods_merchants_begin,goods_merchants_end),
                     (party_slot_eq, "$current_town", slot_town_lord, "trp_player")],
   "{My lord/my lady}, you honour my humble shop with your presence.", "goods_merchant_talk",[]],
[anyone ,"start", [(is_between,"$g_talk_troop",goods_merchants_begin,goods_merchants_end),
			         (call_script, "script_dplmc_print_subordinate_says_sir_madame_to_s0"),],
   "Welcome {s0}. What can I do for you?", "goods_merchant_talk",[]],
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
[anyone ,"start", [(store_conversation_troop,reg(1)),
                     (is_between,reg(1),arena_masters_begin,arena_masters_end),
                     (eq,"$g_talk_troop_met", 0),
                     ],
   "Hello. You seem to be new here. Care to share your name?", "arena_master_intro_1",[]],
[anyone|auto_proceed ,"start", [(store_conversation_troop,reg(1)),(is_between,reg(1),arena_masters_begin,arena_masters_end),
                     (eq, "$last_training_fight_town", "$current_town"),
                     (store_current_hours,":cur_hours"),
                     (val_add, ":cur_hours", -4),
                     (lt, ":cur_hours", "$training_fight_time")],
   ".", "arena_master_fight_result",[(assign, "$arena_reward_asked", 0)]],
[anyone ,"start", [(store_conversation_troop,reg(1)),(is_between,reg(1),arena_masters_begin,arena_masters_end)],
   "Hello {playername}. Good to see you again.", "arena_master_pre_talk",[(assign, "$arena_reward_asked", 0)]],
[trp_galeas,"start", [], "Hello {boy/girl}. If you have any prisoners, I will be happy to buy them from you.", "galeas_talk",[]],
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
[party_tpl|pt_monk_rebels|auto_proceed,"start", [(eq,"$talk_context",tc_party_encounter),(encountered_party_is_attacker)],
   "{!}Warning: This line should never display.", "bandit_introduce",[]],
[anyone,"start", [(this_or_next|eq, "$g_encountered_party_template", "pt_woku_pirates"),(eq, "$g_encountered_party_template", "pt_shinano_rebels")],
   "Eh? What is it?", "bandit_meet",[]],
[party_tpl|pt_rescued_prisoners,"start", [(eq,"$talk_context",tc_party_encounter)], "Do you want us to follow you?", "disbanded_troop_ask",[]],
[party_tpl|pt_enemy,"start", [(eq,"$talk_context",tc_party_encounter)], "You will not capture me again. Not this time.", "enemy_talk_1",[]],
[party_tpl|pt_routed_warriors, "start", [(eq,"$talk_context",tc_party_encounter)],
   "I beg you, please leave us alone.", "party_encounter_routed_agents_are_caught",
   []],
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
[anyone,"start", [(this_or_next|is_between,"$g_talk_troop",weapon_merchants_begin,weapon_merchants_end),
                    (this_or_next|is_between,"$g_talk_troop",armor_merchants_begin, armor_merchants_end),
                    (             is_between,"$g_talk_troop",horse_merchants_begin, horse_merchants_end)], "Good day. What can I do for you?", "town_merchant_talk",[]],
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
[anyone,"start", [(eq, "$talk_context", 0),
                    (is_between,"$g_talk_troop",regular_troops_begin, regular_troops_end),
                    (is_between,"$g_encountered_party_faction",kingdoms_begin, kingdoms_end),
                    (eq, "$players_kingdom", "$g_encountered_party_faction"),
                    (troop_slot_ge, "trp_player", slot_troop_renown, 100),
                    (str_store_party_name, s10, "$current_town"),
					#diplomacy start+ replace {sir/madame} with {my lord/my lady} or {your highness} if appropriate
   				    (call_script, "script_dplmc_print_subordinate_says_sir_madame_to_s0"),
                     ], "Good day, {s0}. Always an honor to have you here in {s10}.", "close_window",[]],
[anyone,"start", [(eq, "$talk_context", 0),
                    (this_or_next|is_between, "$g_talk_troop", "trp_yojimbo", "trp_mercenaries_end"),
                    (is_between, "$g_talk_troop", "trp_female_agent", "trp_refugee"),
                    (is_between,"$g_encountered_party_faction",kingdoms_begin, kingdoms_end),
                     ], "Sir?", "close_window",[]],
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
[anyone,"start", [(eq, "$talk_context", tc_court_talk),
                    (is_between,"$g_talk_troop",regular_troops_begin, regular_troops_end),
                    (is_between,"$g_encountered_party_faction",kingdoms_begin, kingdoms_end),
					#diplomacy start+ replace {sir/madame} with {my lord/my lady} or {your highness} if appropriate
   				    (call_script, "script_dplmc_print_subordinate_says_sir_madame_to_s0"),
                     ], "We are not supposed to talk while on guard, {s0}.", "close_window",[]],
[anyone,"start", [(eq,"$talk_context", tc_party_encounter),(store_encountered_party, reg(5)),(party_get_template_id,reg(7),reg(5)),(eq,reg(7),"pt_kinai_rebels")],
   "Prepare to die!", "battle_reason_stated",[]],
[anyone,"start", [(eq,"$talk_context",tc_party_encounter),
                    (gt,"$encountered_party_hostile",0),
                    (encountered_party_is_attacker),
                    ],
#gekokujo 3.0 no more bandit talk start
   "You have no chance against us. Surrender now or we will kill you all...", "party_encounter_hostile_attacker",[]],
[anyone,"start", [(eq,"$talk_context",tc_party_encounter),
                    (neg|encountered_party_is_attacker),
                    ],
   "What do you want?", "party_encounter_hostile_defender",
   []],
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
[anyone, "start", [
      (is_between, "$g_talk_troop", fort_troops_begin, fort_troops_end),
      (store_sub, ":offset", "$current_town", forts_begin),
      (store_add, ":guard_talk", "str_gekokujo_fort_1_guard_talk", ":offset"),
      (str_store_string, s45, ":guard_talk"),
    ], "{s45}", "close_window", []],
[anyone, "start", [
      (is_between, "$g_talk_troop", fort_deputies_begin, fort_deputies_end),
	  (eq, "$g_talk_troop_met", 0),
      (store_sub, ":offset", "$current_town", forts_begin),
      (store_add, ":deputy_talk", "str_gekokujo_fort_1_deputy_conquer", ":offset"),
      (str_store_string, s45, ":deputy_talk"),
    ], "{s45}","fort_conquest_response", []],
[anyone, "start", [
      (is_between, "$g_talk_troop", fort_deputies_begin, fort_deputies_end),
	  (neq, "$g_talk_troop_met", 0),
      (store_sub, ":offset", "$current_town", forts_begin),
      (store_add, ":deputy_talk", "str_gekokujo_fort_1_deputy_intro", ":offset"),
      (str_store_string, s45, ":deputy_talk"),
    ], "{s45}","fort_deputy_discuss_options", []],
[anyone, "start", [
      (is_between, "$g_talk_troop", fort_companions_begin, fort_companions_end),
	  (eq, "$g_talk_troop_met", 0),
      (store_sub, ":offset", "$current_town", forts_begin),
      (store_add, ":companion_talk", "str_gekokujo_fort_1_companion_meet", ":offset"),
      (str_store_string, s45, ":companion_talk"),
    ], "{s45}","fort_companion_discuss_options", []],
[anyone, "start", [
      (is_between, "$g_talk_troop", fort_companions_begin, fort_companions_end),
	  (neq, "$g_talk_troop_met", 0),
      (store_sub, ":offset", "$current_town", forts_begin),
      (store_add, ":companion_talk", "str_gekokujo_fort_1_companion_intro", ":offset"),
      (str_store_string, s45, ":companion_talk"),
    ], "{s45}","fort_companion_discuss_options", []],
[anyone,"start", [], "Surrender or die. Make your choice", "battle_reason_stated",[]],
[anyone,"start", [], "Hello. What can I do for you?", "free",[]],
[anyone|plyr,"start", [], "Drop your weapons and surrender if you want to live", "threaten_1",[]],
]
