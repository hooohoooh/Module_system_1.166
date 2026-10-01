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


dialogs_quest_npc = [
[anyone, "merchant_quest_4_start",
[
],
"It's time! Kill them all!", "close_window",
[
(try_for_agents, ":agent_no"),
(agent_get_troop_id, ":agent_troop_id", ":agent_no"),
(ge, ":agent_troop_id", "trp_looter"),
(le, ":agent_troop_id", "trp_northern_warlord"),
(agent_set_team, ":agent_no", 1),
(try_end),

(get_player_agent_no, ":player_agent"),

(assign, ":minimum_distance", 1000),
(try_for_agents, ":agent_id_1"),
(neq, ":agent_id_1", ":player_agent"),
(agent_get_team, ":agent_team_1", ":agent_id_1"),
(eq, ":agent_team_1", 0),
(agent_get_position, pos0, ":agent_id_1"),

(try_for_agents, ":agent_id_2"),
  (agent_get_team, ":agent_team_2", ":agent_id_2"),
  (eq, ":agent_team_2", 1),
  (agent_get_position, pos1, ":agent_id_2"),

  (get_distance_between_positions, ":dist", pos0, pos1),

  (le, ":dist", ":minimum_distance"),
  (assign, ":minimum_distance", ":dist"),
  (copy_position, pos2, pos1),
(try_end),

(agent_set_scripted_destination, ":agent_id_1", pos2, 0),
(agent_set_speed_limit, ":agent_id_1", 10),
(try_end),
]],
[anyone|plyr, "bandit_leader_1a",
[
(is_between, "$g_talk_troop", "trp_rebel_leader", "trp_bandit_leaders_end"),
],
"The letters you carried in your baggage tell me who you really work for.", "bandit_leader_1b",
[]],
[anyone|plyr, "bandit_leader_1a",
[
(is_between, "$g_talk_troop", "trp_rebel_leader", "trp_bandit_leaders_end"),
],
"One of my men recognized your face and told me who your real lord is.", "bandit_leader_1b",
[]],
[anyone, "bandit_leader_1b",
[
(is_between, "$g_talk_troop", "trp_rebel_leader", "trp_bandit_leaders_end"),

(assign, ":possible_villages", 0),
(try_for_range, ":village_no", villages_begin, villages_end),
(party_slot_eq, ":village_no", slot_village_bound_center, "$g_starting_town"),
(val_add, ":possible_villages", 1),
(try_end),

(store_random_in_range, ":random_village", 0, ":possible_villages"),
(val_add, ":random_village", 1),

(try_for_range, ":village_no", villages_begin, villages_end),
(party_slot_eq, ":village_no", slot_village_bound_center, "$g_starting_town"),
(val_sub, ":random_village", 1),
(eq, ":random_village", 0),
(assign, "$lair_neighboor_village", ":village_no"),
(try_end),

(str_store_party_name_link, s9, "$lair_neighboor_village"),

(set_spawn_radius, 4),
(spawn_around_party, "$lair_neighboor_village", "pt_looter_lair"),
(party_set_flags, reg0, pf_always_visible, 1),
],
"So I guess that means you don't need me alive anymore. Very well, I am not afraid to die. But know this -- you are a fool if you think your band of rabble can assault our mansion in {s9}.", "close_window",
[
(call_script, "script_succeed_quest", "qst_learn_where_merchant_brother_is"),
(call_script, "script_end_quest", "qst_learn_where_merchant_brother_is"),

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
(str_store_troop_name, s10, ":troop_of_merchant"),

(str_store_string, s2, "str_find_the_lair_near_s9_and_free_the_brother_of_the_prominent_s10_merchant"),
(call_script, "script_start_quest", "qst_save_relative_of_merchant", ":troop_of_merchant"),
]],
[anyone|plyr, "merchant_quest_3b", #was startup
[
],
"Thanks for the money, but I still know nothing. You owe me an explanation.", "merchant_quest_4a",
[
]],
[anyone|plyr, "merchant_quest_3b", #was startup
[
],
"I'll take your money, but you better tell me everything. This is outrageous.", "merchant_quest_4a",
[
]],
[anyone, "merchant_quest_4a", #was startup
[
],
"Haha, I'm sorry about all this skullduggery, {playername}. Really, I am. At the very least, I am truthful about being a merchant in this town. And there really was a person named Minemaru that was killed by a haughty samurai. But he was not my brother, and as you've discovered, neither is Horenbo.", "merchant_quest_4b",
[
]],
[anyone|plyr, "merchant_quest_4b",
[],
"Go on, please.", "merchant_quest_4b1",
[]],
[anyone|plyr, "merchant_quest_4b",
[],
"I will hold off from killing you right here, right now.", "merchant_quest_4b1",
[]],
[anyone, "merchant_quest_4b1",
[],
"I am from a group that seeks justice. What unites us is not class, for we come from all walks of life: merchant, peasant, and even samurai. No, that which we share together is the most important thing -- devotion to the Amida Buddha and the hope of rebirth in the True Pure Land.", "merchant_quest_4b1a",
[]],
[anyone|plyr, "merchant_quest_4b1a",
[],
"You have got to be kidding me...", "merchant_quest_4b2",
[]],
[anyone, "merchant_quest_4b2",
[],
"I'm sure you've heard of our Ikko movement. Yes, we're in this city too -- we're everywhere. But we haven't been able to move openly. That is, until your great help just now.", "merchant_quest_4b3",
[]],
[anyone, "merchant_quest_4b3",
[
#gekokujo 3.0 use the town lord rather than faction leader
#(faction_get_slot, ":local_ruler", "$g_encountered_party_faction", slot_faction_leader),
#(str_store_troop_name, s4, ":local_ruler"),
(party_get_slot, ":local_ruler", "$g_starting_town", slot_town_lord),
(str_store_troop_name, s4, ":local_ruler"),
##diplomacy start+ Gender-correct, and replace "king" with "{s0}"
#(call_script, "script_dplmc_store_troop_is_female_reg", ":local_ruler", 4),
#(call_script, "script_dplmc_print_cultural_word_to_sreg", ":local_ruler", DPLMC_CULTURAL_TERM_KING, 0),
],
#"Now -- here's my plan. I could bring this to the attention of {s4}, lord of the city, but that would mean an inquiry, my word against the captain's, and witnesses can be bought and evidence destroyed, or maybe the whole thing will be forgotten if the enemy comes across the border again, and all I'll get for my trouble is a knife in the ribs. In time of war, you see, a king's eye wanders far from his domain, and his subjects suffer. So I've got another idea. I've got a small group of townsfolk together, some men in my employ and some others who've lost relatives to these bandits, and we'll storm the captain's home and bring him in chains before {s4}, hopefully with a few captured bandits to explain how things stack up.", "merchant_quest_4b4",
#"Now -- here's my plan. I could bring this to the attention of {s4}, lord of the city, but that would mean an investigation, my word against the samurai's, and witnesses can be bought and evidence destroyed, or maybe the whole thing will be forgotten if the enemy comes across the border again, and all I'll get for my trouble is a knife in the ribs. In time of war, you see, a {s0}'s eye wanders far from {reg4?her:his} domain, and {reg4?her:his} subjects suffer. So I've got another idea. I've got a small group of townsfolk together, some men in my employ and some others who've lost relatives to these bandits, and we'll storm the samurai's home and bring him in chains before {s4}, hopefully with a few captured bandits to explain how things stack up.", "merchant_quest_4b4",
"I mustn't give you all the credit, however. We have been able to get away with a lot so far thanks to some patron samurai among the officials that serve {s4}, lord of the town. Although they are minor in clout, there's a lot of them. But there are other samurai that oppose them -- oppose us -- and that is what the business of Minemaru's murder and Horenbo's kidnapping are all about. We need to take the opportunity you opened with your mansion raid to finish this once and for all. By silencing our enemies, we can embed ourselves even more deeply into the fabric of this domain.", "merchant_quest_4b4",
[]],
[anyone, "merchant_quest_4b4",
[
],
#"All I need now is someone to lead my little army into battle -- and I can't think of anyone better than you. So, what do you say?", "merchant_quest_4b5",
"Although our adversaries are weakened, we still only have the bare minimum fighting power to oppose them. I mean, we have our own samurai, but they must continue to remain above suspicion and rise in rank while we do the dirty work. This is where you come in.", "merchant_quest_4b4a",
[
]],
[anyone, "merchant_quest_4b4a",
[
],
"We have just enough armed men to ambush our enemies, slaughter them, and fade away. Your presence would tip the balance further in our favor and give us breathing room. What do you say?", "merchant_quest_4b5",
[
]],
[anyone|plyr, "merchant_quest_4b5",
[
#gekokujo 3.0 use town lord rather than faction leader
#(faction_get_slot, ":local_ruler", "$g_encountered_party_faction", slot_faction_leader),
#(str_store_troop_name, s4, ":local_ruler"),
(party_get_slot, ":local_ruler", "$g_starting_town", slot_town_lord),
(str_store_troop_name, s4, ":local_ruler"),
#diplomacy start Gender-correct
(call_script, "script_dplmc_store_troop_is_female_reg", ":local_ruler", 4),
#diplomacy end Gender-correct
],
"What is stopping me from just going up to {s4} and telling {reg4?her:him} everything?", "merchant_quest_4b6",
[
]],
[anyone, "merchant_quest_4b6",
[
#(str_store_party_name, s4, "$g_encountered_party"),
],
"Sigh. Nothing. But if you leave this inn now, our people will disappear and you will be left holding the bag, admitting to raiding the mansion of a vassal and killing his retainers. I have no illusion that you are not devoted to the Amida Buddha, but I have learned that with you, money talks. There's a pile of it waiting for you if you do me this last favor. So what do you say?", "merchant_quest_4b7",
#"Oh, well, I suppose it's possible that I found a dozen bandits who were willing to give their lives to give a passing stranger a false impression of life in old {s4}... Well, I guess you can't really know if my word is good, but I reckon you've learned by now that my money is good, and there's another 100 mon, or maybe a bit more, that's waiting for you if you'll do me this last little favor. So what do you say?", "merchant_quest_4b7",
[
]],
[anyone|plyr, "merchant_quest_4b7",
[
],
"All right. I'll follow your lead.", "merchant_quest_4b8",
[
]],
[anyone|plyr, "merchant_quest_4b7",
[
],
"I'm sorry. This is too much, too fast. I need time to think.", "merchant_quest_4_decline",
[
]],
[anyone, "merchant_quest_4b8",
[
],
"Excellent. It's been a long time since I staked so much on a single throw of the dice, and frankly I find it exhilarating. My men are ready to move once you are ready. Are you ready?", "merchant_quest_4b9",
[
]],
[anyone|plyr, "merchant_quest_4b9",
[
],
"Yes. Give them the sign.", "merchant_quest_4_accept",
[
]],
[anyone|plyr, "merchant_quest_4b9",
[
],
"Not now. I will need to rest before I can fight again.", "merchant_quest_4_decline",
[
]],
[anyone, "merchant_quest_4_accept",
[
],
"Good! Now -- strike hard, strike fast, and our enemies won't know what hit them. May heaven be with you!", "close_window",
[
(assign, "$current_startup_quest_phase", 3),
(jump_to_menu, "mnu_start_phase_3"),
(finish_mission),
]],
[anyone, "merchant_quest_4_decline", #was startup
[
],
"Right. I can keep my men standing by. If you let this go too long, then I suppose that I will have to finish this affair without you, but I would be most pleased if you could be part of it as well. For now, take what time you need.", "close_window",
[]],
[anyone|plyr, "merchant_quest_2a",
[
],
"Very well, I will capture this samurai.", "close_window",
[
(str_store_party_name, s9, "$current_town"),
(str_store_string, s2, "str_start_up_quest_message_2"),
(call_script, "script_start_quest", "qst_learn_where_merchant_brother_is", "$g_talk_troop"),

(set_spawn_radius, 2),
(spawn_around_party, "$current_town", "pt_leaded_looters"),
(assign, ":spawned_bandits", reg0),

(party_get_position, pos0, "$current_town"),
(party_set_ai_behavior, ":spawned_bandits", ai_bhvr_patrol_location),
(party_set_ai_patrol_radius, ":spawned_bandits", 3),
(party_set_ai_target_position, ":spawned_bandits", pos0),
]],
[anyone|plyr, "merchant_quest_2a",
[
],
"Why don't you come with us?", "merchant_quest_2a_whynotcome",
[
]],
[anyone, "merchant_quest_2a_whynotcome",
[
],
"I would be a liability -- If they see my face, they will raise their guard. This is the most safe course of action.", "merchant_quest_2a",
[
]],
[anyone|plyr, "merchant_quest_2a",
[
],
"I apologize, I have to put this off temporarily.", "close_window",
[
]],
[anyone|plyr, "merchant_quest_3a",
[
],
"Very well. I go now to attack the scum in their lair, and find your brother.", "close_window",
[
#no need to below three lines anymore, this quest is auto starting after player learn where bandits are hiding merchant's brother.
#(str_store_party_name, s9, "$lair_neighboor_village"),
#(str_store_string, s2, "str_start_up_quest_message_3"),
#(call_script, "script_start_quest", "qst_save_relative_of_merchant", "$g_talk_troop"),
]],
[anyone|plyr, "merchant_quest_3a",
[
],
"I apologize, I have to put this off temporarily.", "close_window",
[
#think about placing end_quest here. Because it is auto-starting. If player do not want this quest he/she should have a way to avoid it.
]],
[anyone|plyr, "merchant_quest_persuasion",
[
(neg|check_quest_finished, "qst_collect_men"),
(neg|check_quest_active, "qst_collect_men"),
],
"You make a persuasive case. I will help you.", "merchant_quest_1_prologue_3",
[
]],
[anyone|plyr, "merchant_quest_persuasion",
[
(check_quest_finished, "qst_collect_men"),
(neg|check_quest_finished, "qst_learn_where_merchant_brother_is"),
(neg|check_quest_active, "qst_learn_where_merchant_brother_is"),
],
"You make a persuasive case. I will help you.", "merchant_quest_2",
[
]],
[anyone|plyr, "merchant_quest_persuasion",
[
(check_quest_finished, "qst_collect_men"),
(check_quest_finished, "qst_learn_where_merchant_brother_is"),
(neg|check_quest_finished, "qst_save_relative_of_merchant"),
(neg|check_quest_active, "qst_save_relative_of_merchant"),
],
"You make a persuasive case. I will help you.", "merchant_quest_3",
[
]],
[anyone|plyr, "merchant_quest_persuasion",
[
(check_quest_finished, "qst_collect_men"),
(check_quest_finished, "qst_learn_where_merchant_brother_is"),
(check_quest_finished, "qst_save_relative_of_merchant"),
(neg|check_quest_finished, "qst_save_town_from_bandits"),
(neg|check_quest_active, "qst_save_town_from_bandits"),
],
"You make a persuasive case. I will help you.", "merchant_quest_4b8",
[
]],
[anyone|plyr, "merchant_quest_persuasion",
[
],
"I'm afraid I have more important things to do at the moment.", "close_window",
[
]],
[anyone|plyr,"merchant_quest_persuasion",
[
(ge, "$cheat_mode", 1),
],
"{!}[CHEAT] I have played this before, and would prefer to skip the tutorial.", "dplmc_devel_merchant_quest_skip",
[]],
[anyone, "merchant_quest_2",
[
],
"Now -- go find and defeat that samurai.", "merchant_quest_2a",
[
]],
[anyone, "merchant_quest_3",
[
],
"Now -- go attack that mansion, get my brother back, and show those oni what happens to those who threaten my house.", "merchant_quest_3a",
[
]],
[anyone,"merchant_quests_last_word",
[
],
"As long as I walk alive and free in this town, I am proof that we will overcome the rule of the samurai within my lifetime.", "close_window",
[
]],
[anyone,"merchant_quest_about_job", [], "What about it?", "merchant_quest_about_job_2",[]],
[anyone|plyr,"merchant_quest_about_job_2", [], "What if I can't finish it?", "merchant_quest_what_if_fail",[]],
[anyone|plyr,"merchant_quest_about_job_2", [], "Well, I'm still working on it.", "merchant_quest_about_job_working",[]],
[anyone,"merchant_quest_about_job_working", [], "Good. I'm sure you will handle it.", "mayor_pretalk",[]],
[anyone,"merchant_quest_last_offered_job", [], "Eh, you want to reconsider that. Good...", "merchant_quest_brief",
   [[assign,"$random_merchant_quest_no","$merchant_offered_quest"]]],
[anyone,"merchant_quest_what_if_fail", [(store_partner_quest,":partner_quest"),(eq,":partner_quest","qst_deliver_wine")],
   "I hope you don't fail. In that case, I'll have to ask for the price of the cargo you were carrying.", "mayor_pretalk",[]],
[anyone,"merchant_quest_what_if_fail", [], "Well, just do your best to finish it.", "mayor_pretalk",[]],
[anyone,"merchant_quest_taken", [], "Excellent. I am counting on you then. Good luck.", "mayor_pretalk",
   []],
[anyone,"merchant_quest_stall", [], "Well, the job will be available for a few more days I guess. Tell me if you decide to take it.", "mayor_pretalk",[]],
[anyone,"merchant_quest_requested",
   [
     (eq,"$random_merchant_quest_no","qst_deal_with_looters"),
     ],
   "Well, you look able enough. I think I might have something you could do.", "merchant_quest_brief", []],
[anyone,"merchant_quest_brief",
   [
     (eq,"$random_merchant_quest_no","qst_deal_with_looters"),
     (try_begin),
       (party_slot_eq,"$g_encountered_party",slot_party_type,spt_town),
       (str_store_string,s5,"@town"),
     (else_try),
       (party_slot_eq,"$g_encountered_party",slot_party_type,spt_village),
       (str_store_string,s5,"@village"),
     (try_end),
     ],
   "We've had some fighting near the {s5} lately, with all the chaos that comes with it,\
 and that's led some of our less upstanding locals to try and make their fortune out of looting the shops and farms during the confusion.\
 A lot of valuable goods were taken. I need somebody to teach those bastards a lesson.\
 Sound like your kind of work?", "merchant_quest_looters_choice", []],
[anyone|plyr,"merchant_quest_looters_choice", [], "Aye, I'll do it.", "merchant_quest_looters_brief", []],
[anyone|plyr,"merchant_quest_looters_choice", [], "I'm afraid I can't take the job at the moment.", "merchant_quest_stall",[]],
[anyone,"merchant_quest_looters_brief", [
   (try_begin),
	(party_slot_eq,"$g_encountered_party",slot_party_type,spt_town),
	(str_store_string,s5,"@town"),
   (else_try),
	(party_slot_eq,"$g_encountered_party",slot_party_type,spt_village),
	(str_store_string,s5,"@village"),
   (try_end),

#     (party_get_slot,":merchant","$current_town",slot_town_merchant),
#     (troop_clear_inventory,":merchant"),
   (store_random_in_range,":random_num_looters",3,7),
   (quest_set_slot,"qst_deal_with_looters",slot_quest_target_amount,":random_num_looters"),
   (try_for_range,":unused",0,":random_num_looters"),
     (store_random_in_range,":random_radius",5,14),
     (set_spawn_radius,":random_radius"),
     (spawn_around_party,"$g_encountered_party","pt_looters"),
     (party_set_flags, reg0, pf_quest_party, 1),
     (party_set_ai_behavior, reg0, ai_bhvr_patrol_location),
     (party_set_ai_patrol_radius, reg0, 2),
     (party_get_position, pos0, reg0),
     (party_set_ai_target_position, reg0, pos0),
   (try_end),
   (str_store_troop_name_link, s9, "$g_talk_troop"),
   (str_store_party_name_link, s13, "$g_encountered_party"),
   (str_store_party_name, s4, "$g_encountered_party"),
   (setup_quest_text, "qst_deal_with_looters"),
   (str_store_string, s2, "@The chief merchant of {s13} has asked you to deal with looters in the surrounding countryside."),
   (call_script, "script_start_quest", "qst_deal_with_looters", "$g_talk_troop"),
   (assign, "$g_leave_encounter",1),
  ],
   "Excellent! You'll find the looters roaming around the countryside, probably trying to rob more good people.\
 Kill or capture the bastards, I don't care what you do with them.\
 I'll pay you a bounty of 40 mon on every band of looters you destroy,\
 until all the looters are dealt with.", "close_window",
   []],
[anyone,"merchant_quest_requested", [
  (eq,"$random_merchant_quest_no","qst_retaliate_for_border_incident"),

  (quest_get_slot, ":target_faction", "qst_retaliate_for_border_incident", slot_quest_target_faction),
  (call_script, "script_faction_get_adjective_to_s10", ":target_faction"),

  (faction_get_slot, ":leader", "$g_encountered_party_faction", slot_faction_leader),
  (str_store_troop_name, s5, ":leader"),
##diplomacy start+ Use forrect gender for faction leader
  (call_script, "script_dplmc_store_troop_is_female", ":leader"),
#Next line, fix pronouns with reg0
	], "Well, there is a very great favor which you could do us... As you may have heard, some {s10}s have come across the border to attack our people. {s5} is under great pressure from some of the more bellicose of {reg0?her:his} vassals to respond with a declaration of war. Unfortunately, while the great lords of this land grow rich from bloodshed, we of the commons will be caught in the middle, and will suffer.",
	"merchant_quest_explain_2", []],
[anyone,"merchant_quest_explain_2", [
  (eq,"$random_merchant_quest_no","qst_retaliate_for_border_incident"),
  (quest_get_slot, ":target_troop", "qst_retaliate_for_border_incident", slot_quest_target_troop),
  (str_store_troop_name, s7, ":target_troop"),
##diplomacy start+ Use correct gender for faction leader
  (faction_get_slot, ":leader", "$g_encountered_party_faction", slot_faction_leader),
  (call_script, "script_dplmc_store_troop_is_female", ":leader"),
##diplomacy end+
  ],
##diplomacy start+ Fix pronouns with reg0
  "We are not saying that {s5} should overlook this aggression -- far from it! But if {reg0?she:he} charges one of {reg0?her:his} own lords to respond, then the cycle of provocation will necessarily lead to a full-fledged confrontation. Now, if an outsider were to step in and defeat a {s10} lord in battle, then honor would be done, and it would defuse the clamor for war. If the defeated lord were a known troublemaker -- {s7} -- then the {s10}s might be able to overlook it.",
  "merchant_quest_brief",[]],
[anyone,"merchant_quest_brief", [
  (eq,"$random_merchant_quest_no","qst_retaliate_for_border_incident"),
  (quest_get_slot, ":target_troop", "qst_retaliate_for_border_incident", slot_quest_target_troop),
  (str_store_troop_name, s7, ":target_troop"),
  ],
  "We need you to attack and defeat {s7}. This will not be an easy task, and that outsider would damage {his/her} relationship with the {s10}s, but we would be very grateful. We could not acknowledge a connection with that outsider, but we could be sure that {he/she} would be handsomely rewarded... Could you do this?",
  "merchant_quest_retaliate_confirm",[]],
[anyone|plyr,"merchant_quest_retaliate_confirm", [], "Aye, I can do it.", "merchant_quest_track_bandits_brief", [
#    (quest_set_slot, "qst_retaliate_for_border_incident", slot_quest_target_troop, "$g_target_leader"),
#    (quest_set_slot, "qst_retaliate_for_border_incident", slot_quest_target_faction, "$g_target_faction"),

	(str_store_faction_name, s11, "$g_encountered_party_faction"),
    (setup_quest_text, "qst_retaliate_for_border_incident"),
    (str_store_string, s2, "str_track_down_s7_and_defeat_him_defusing_calls_for_war_within_the_s11"),
    (call_script, "script_start_quest", "qst_retaliate_for_border_incident", "$g_talk_troop"),
  ]],
[anyone|plyr,"merchant_quest_retaliate_confirm", [], "I would prefer not to get mixed up in such things", "merchant_pretalk", [
	(quest_set_slot, "qst_retaliate_for_border_incident", slot_quest_dont_give_again_remaining_days, 5),
  ]],
[anyone|plyr,"merchant_quest_track_bandit_lair_choice", [], "Aye, I'll do it.", "merchant_quest_destroy_lair_brief", [

    (quest_get_slot, ":target_party", "qst_destroy_bandit_lair", slot_quest_target_party),
    (party_set_flags, ":target_party", pf_quest_party, 1),
#    (quest_set_slot, "qst_track_down_bandits", slot_quest_target_party, "$g_bandit_party_for_bounty"), #WHY IS THIS COMMENTED OUT?
    (quest_set_slot, "qst_destroy_bandit_lair", slot_quest_giver_troop, "$g_talk_troop"),
    (quest_set_slot, "qst_destroy_bandit_lair", slot_quest_giver_center, "$g_encountered_party"),

    (str_store_troop_name_link, s11, "$g_talk_troop"),
    (str_store_party_name, s9, ":target_party"),
    (setup_quest_text, "qst_destroy_bandit_lair"),
    (str_store_string, s2, "str_bandit_lair_quest_description"),
    (call_script, "script_start_quest", "qst_destroy_bandit_lair", "$g_talk_troop"),
  ]],
[anyone|plyr,"merchant_quest_track_bandit_lair_choice", [], "I'm afraid I can't take the job at the moment.", "lord_pretalk",[
  (quest_set_slot, "qst_destroy_bandit_lair", slot_quest_dont_give_again_remaining_days, 1),
  ]],
[anyone,"merchant_quest_destroy_lair_brief", [
  ], "Very good. We will await word of your success.", "close_window",
   [
   (assign, "$g_leave_encounter", 1),
   ]],
[anyone,"merchant_quest_requested", [
  (eq,"$random_merchant_quest_no", "qst_track_down_bandits"),
  ], "We have heard that {s4}, some travellers on the road {reg4?to:from} {s5} were attacked by {s7}.", "merchant_quest_brief",
   [
   (call_script,"script_merchant_road_info_to_s42", "$g_encountered_party"),
   (assign, "$g_bandit_party_for_bounty", reg0),
   (assign, ":origin", reg1),
   (assign, ":destination", reg2),
   (assign, ":hours_ago", reg3),
   (try_begin),
	(lt, ":hours_ago", 24),
	(str_store_string, s4, "str_a_short_while_ago"),
   (else_try),
	(lt, ":hours_ago", 48),
	(str_store_string, s4, "str_one_day_ago"),
   (else_try),
 	(lt, ":hours_ago", 72),
	(str_store_string, s4, "str_two_days_day_ago"),
   (else_try),
 	(lt, ":hours_ago", 144),
	(str_store_string, s4, "str_earlier_this_week"),
   (else_try),
	(str_store_string, s4, "str_about_a_week_ago"),
   (try_end),


   (try_begin),
	(eq, ":origin", "$g_encountered_party"),
	(str_store_party_name, s5, ":destination"),
	(assign, reg4, 0),
   (else_try),
	(eq, ":destination", "$g_encountered_party"),
	(str_store_party_name, s5, ":origin"),
	(assign, reg4, 1),
   (try_end),

   (str_store_party_name, s7, "$g_bandit_party_for_bounty"),
   ###
   (quest_set_slot, "qst_track_down_bandits", slot_quest_target_party, "$g_bandit_party_for_bounty"),
   ]],
[anyone,"merchant_quest_brief", [
     (eq,"$random_merchant_quest_no", "qst_track_down_bandits"),
     (quest_get_slot, ":target_party", "qst_track_down_bandits", slot_quest_target_party),
	 (str_store_party_name, s4, ":target_party"),
	 ],
	"We would like you to track these {s4} down. The merchants of the town were able to get a description of their leader, and have put together a bounty. If you can hunt them down and destroy them, we'll make it worth your while...", "merchant_quest_track_bandits_choice",
   []],
[anyone|plyr,"merchant_quest_track_bandits_choice", [], "Aye, I'll do it.", "merchant_quest_track_bandits_brief", [
    (assign, "$merchant_offered_quest", 0),
	(assign,"$merchant_quest_last_offerer", "$g_talk_troop"),

    (quest_get_slot, ":target_party", "qst_track_down_bandits", slot_quest_target_party),
    (party_set_flags, ":target_party", pf_quest_party, 1),
#    (quest_set_slot, "qst_track_down_bandits", slot_quest_target_party, "$g_bandit_party_for_bounty"), #WHY IS THIS COMMENTED OUT?
    (quest_set_slot, "qst_track_down_bandits", slot_quest_giver_troop, "$g_talk_troop"),
    (quest_set_slot, "qst_track_down_bandits", slot_quest_giver_center, "$g_encountered_party"),

    (str_store_party_name_link, s8, "$g_encountered_party"),
    (str_store_party_name, s9, ":target_party"),
    (setup_quest_text, "qst_track_down_bandits"),
    (str_store_string, s2, "str_track_down_the_s9_who_attacked_travellers_near_s8_then_report_back_to_the_town"),
    (call_script, "script_start_quest", "qst_track_down_bandits", "$g_talk_troop"),
  ]],
[anyone,"merchant_quest_track_bandits_brief", [
  ], "Very good. The band may not have lingered long in the area, but chances are that they will be spotted by other travellers on the road.", "close_window",
   [
   (assign, "$g_leave_encounter", 1),
   ]],
[anyone|plyr,"merchant_quest_track_bandits_choice", [], "I'm afraid I can't take the job at the moment.", "merchant_quest_stall",[
  (quest_set_slot, "qst_track_down_bandits", slot_quest_dont_give_again_remaining_days, 1),
  ]],
[anyone,"merchant_quest_requested", [(eq,"$random_merchant_quest_no","qst_deliver_wine"),], "You're looking for a job?\
 Actually I was looking for someone to deliver some {s4}.\
 Perhaps you can do that...", "merchant_quest_brief",
   [(quest_get_slot, ":quest_target_item", "qst_deliver_wine", slot_quest_target_item),
    (str_store_item_name, s4, ":quest_target_item"),
    ]],
[anyone,"merchant_quest_brief", [(eq,"$random_merchant_quest_no","qst_deliver_wine")],
   "I have a cargo of {s6} that needs to be delivered to the inn at {s4}.\
 If you can take {reg5} units of {s6} to {s4} in 7 days, you may earn {reg8} mon.\
 What do you say?", "merchant_quest_brief_deliver_wine",
   [(quest_get_slot, reg5, "qst_deliver_wine", slot_quest_target_amount),
    (quest_get_slot, reg8, "qst_deliver_wine", slot_quest_gold_reward),
    (quest_get_slot, ":quest_target_item", "qst_deliver_wine", slot_quest_target_item),
    (quest_get_slot, ":quest_target_center", "qst_deliver_wine", slot_quest_target_center),
    (str_store_troop_name, s9, "$g_talk_troop"),
    (str_store_party_name_link, s3, "$g_encountered_party"),
    (str_store_party_name_link, s4, ":quest_target_center"),
    (str_store_item_name, s6, ":quest_target_item"),
    (setup_quest_text,"qst_deliver_wine"),
    (str_store_string, s2, "@{s9} of {s3} asked you to deliver {reg5} units of {s6} to the inn at {s4} in 7 days."),
    #s2 should not be changed until the decision is made
   ]],
[anyone|plyr,"merchant_quest_brief_deliver_wine", [(store_free_inventory_capacity,":capacity"),
                                                     (quest_get_slot, ":quest_target_amount", "qst_deliver_wine", slot_quest_target_amount),
                                                     (ge, ":capacity", ":quest_target_amount"),
                                                     ],
      "Alright. I will make the delivery.", "merchant_quest_taken",
   [(quest_get_slot, ":quest_target_amount", "qst_deliver_wine", slot_quest_target_amount),
    (quest_get_slot, ":quest_target_item", "qst_deliver_wine", slot_quest_target_item),
    (troop_add_items, "trp_player", ":quest_target_item",":quest_target_amount"),
    (call_script, "script_start_quest", "qst_deliver_wine", "$g_talk_troop"),
    ]],
[anyone|plyr,"merchant_quest_brief_deliver_wine", [], "I am afraid I can't carry all that cargo now.", "merchant_quest_stall",[]],
[anyone,"merchant_quest_requested", [(eq,"$random_merchant_quest_no","qst_escort_merchant_caravan")], "You're looking for a job?\
 Actually I was looking for someone to escort a caravan.\
 Perhaps you can do that...", "merchant_quest_brief",
   []],
[anyone,"merchant_quest_brief", [(eq, "$random_merchant_quest_no", "qst_escort_merchant_caravan")],
   "I am going to send a caravan of goods to {s8}.\
 However with all those bandits and deserters on the roads, I don't want to send them out without an escort.\
 If you can lead that caravan to {s8} in 15 days, you will earn {reg8} mon.\
 Of course your party needs to be at least {reg4} strong to offer them any protection.", "escort_merchant_caravan_quest_brief",
   [(quest_get_slot, reg8, "qst_escort_merchant_caravan", slot_quest_gold_reward),
    (quest_get_slot, reg4, "qst_escort_merchant_caravan", slot_quest_target_amount),
    (quest_get_slot, ":quest_target_center", "qst_escort_merchant_caravan", slot_quest_target_center),
    (str_store_party_name, s8, ":quest_target_center"),
   ]],
[anyone,"merchant_quest_requested", [(eq, "$random_merchant_quest_no", "qst_troublesome_bandits")],
 "Actually, I was looking for an able adventurer like you.\
 There's this group of particularly troublesome bandits.\
 They have infested the vicinity of our town and are preying on my caravans.\
 They have avoided all the soldiers and the militias up to now.\
 If someone doesn't stop them soon, I am going to be ruined...", "merchant_quest_brief",
   []],
[anyone,"merchant_quest_brief", [(eq,"$random_merchant_quest_no", "qst_troublesome_bandits")],
  "I will pay you {reg8} mon if you hunt down those troublesome bandits.\
 It's dangerous work. But I believe that you are the {man/one} for it.\
 What do you say?", "troublesome_bandits_quest_brief",[(quest_get_slot, reg8, "qst_troublesome_bandits", slot_quest_gold_reward),
                                                       ]],
[anyone,"merchant_quest_taken_bandits", [], "You will? Splendid. Good luck to you.", "close_window",
   []],
[anyone,"merchant_quest_requested", [(eq, "$random_merchant_quest_no", "qst_kidnapped_girl")],
 "Actually, I was looking for a reliable {man/helper} that can undertake an important mission.\
 A group of bandits have kidnapped the daughter of a friend of mine and are holding her for ransom.\
 My friend is ready to pay them, but we still need\
 someone to take the money to those rascals and bring the girl back to safety.", "merchant_quest_brief",
   []],
[anyone,"merchant_quest_brief", [(eq, "$random_merchant_quest_no", "qst_kidnapped_girl")],
  "The amount the bandits ask as ransom is {reg12} mon.\
 I will give you that money once you accept to take the quest.\
 You have 15 days to take the money to the bandits who will be waiting near the village of {s4}.\
 Those bastards said that they are going to kill the poor girl if they don't get the money by that time.\
 You will get your pay of {reg8} mon when you bring the girl safely back here.",
   "kidnapped_girl_quest_brief",[(quest_get_slot, ":quest_target_center", "qst_kidnapped_girl", slot_quest_target_center),
                                 (str_store_party_name, s4, ":quest_target_center"),
                                 (quest_get_slot, reg8, "qst_kidnapped_girl", slot_quest_gold_reward),
                                 (quest_get_slot, reg12, "qst_kidnapped_girl", slot_quest_target_amount),
                                 ]],
[anyone|plyr,"merchant_quest_about_job_2", [(store_partner_quest, ":partner_quest"),
                                              (eq, ":partner_quest", "qst_kidnapped_girl"),
                                              (quest_slot_eq, "qst_kidnapped_girl", slot_quest_current_state, 3),
                                              (neg|main_party_has_troop, "trp_kidnapped_girl")],
   "Unfortunately I lost the girl on the way here...", "lost_kidnapped_girl",[]],
[anyone,"merchant_quest_about_job_5a", [],
   "At least you have the decency to return the money.", "close_window",[]],
[anyone,"merchant_quest_about_job_5b", [],
   "Do you expect me to believe that? You are going to pay that ransom fee back! Go and bring the money now!",
   "close_window",[(quest_get_slot, ":quest_target_amount", "qst_kidnapped_girl", slot_quest_target_amount),
                   (val_add, "$debt_to_merchants_guild", ":quest_target_amount"),
                   ]],
[anyone,"merchant_quest_requested", [(eq, "$random_merchant_quest_no", "qst_persuade_lords_to_make_peace"),
                                       (quest_get_slot, ":quest_target_faction", "qst_persuade_lords_to_make_peace", slot_quest_target_faction),
                                       (quest_get_slot, ":quest_object_troop", "qst_persuade_lords_to_make_peace", slot_quest_object_troop),
                                       (quest_get_slot, ":quest_target_troop", "qst_persuade_lords_to_make_peace", slot_quest_target_troop),
                                       (str_store_troop_name_link, s12, ":quest_object_troop"),
                                       (str_store_troop_name_link, s13, ":quest_target_troop"),
                                       (str_store_faction_name_link, s14, ":quest_target_faction"),
                                       (str_store_faction_name_link, s15, "$g_encountered_party_faction"),],
   "This war between {s15} and {s14} has brought our town to the verge of ruin.\
 Our caravans get raided before they can reach their destination.\
 Our merchants are afraid to leave the safety of the town walls.\
 And as if those aren't enough, the taxes to maintain the war take away the last bits of our savings.\
 If peace does not come soon, we can not hold on for much longer.", "merchant_quest_persuade_peace_1",
   []],
[anyone|plyr,"merchant_quest_persuade_peace_1", [], "You are right. But who can stop this madness called war?", "merchant_quest_brief",[]],
[anyone|plyr,"merchant_quest_persuade_peace_1", [], "It is your duty to help the samurai in their war effort. You shouldn't complain about it.", "merchant_quest_persuade_peace_reject",[]],
[anyone,"merchant_quest_persuade_peace_reject", [], "Hah. The samurai fight their wars for their greed and their dreams of glory.\
 And it is poor honest folk like us who have to bear the real burden.\
 But you obviously don't want to hear about that.", "close_window",[]],
[anyone,"merchant_quest_brief", [(eq,"$random_merchant_quest_no","qst_persuade_lords_to_make_peace"),
  ##diplomacy start+ gender correct
  (quest_get_slot, ":quest_object_troop", "qst_persuade_lords_to_make_peace", slot_quest_object_troop),
  (call_script, "script_dplmc_store_troop_is_female", ":quest_object_troop"),
  (try_begin),
     (eq, reg0, 0),
	  (quest_get_slot, ":quest_target_troop", "qst_persuade_lords_to_make_peace", slot_quest_target_troop),
	  (call_script, "script_dplmc_store_troop_is_female", ":quest_target_troop"),
  (try_end),
  #Avoid saying "men" if either/both are female
  ],
#   "There have been attempts to reconcile the two sides and reach a settlement.\
# However, there are powerful lords on both sides whose interests lie in continuing the war.\
# These men urge all others not to heed to the word of sensible men, but to keep fighting.\
# While these leaders remain influential, no peace settlement can be reached.", "merchant_quest_persuade_peace_3",[]],
   "There have been attempts to reconcile the two sides and reach a settlement.\
 However, there are powerful lords on both sides whose interests lie in continuing the war.\
 {reg0?They:These men} urge all others not to heed to the word of sensible men, but to keep fighting.\
 While these leaders remain influential, no peace settlement can be reached.", "merchant_quest_persuade_peace_3",[]],
[anyone|plyr,"merchant_quest_persuade_peace_3", [], "Who are these warmongers who block the way of peace?", "merchant_quest_persuade_peace_4",[]],
[anyone|plyr,"merchant_quest_persuade_peace_3", [], "Who are these lords you speak of?", "merchant_quest_persuade_peace_4",[]],
[anyone,"merchant_quest_persuade_peace_4", [], "They are {s12} from {s15} and {s13} from {s14}. Until they change their mind or lose their influence,\
 there will be no chance of having peace between the two sides.", "merchant_quest_persuade_peace_5",[
       (quest_get_slot, ":quest_target_faction", "qst_persuade_lords_to_make_peace", slot_quest_target_faction),
       (quest_get_slot, ":quest_object_troop", "qst_persuade_lords_to_make_peace", slot_quest_object_troop),
       (quest_get_slot, ":quest_target_troop", "qst_persuade_lords_to_make_peace", slot_quest_target_troop),
       (str_store_troop_name_link, s12, ":quest_object_troop"),
       (str_store_troop_name_link, s13, ":quest_target_troop"),
       (str_store_faction_name_link, s14, ":quest_target_faction"),
       (str_store_faction_name_link, s15, "$g_encountered_party_faction"),
     ]],
[anyone|plyr,"merchant_quest_persuade_peace_5", [], "What can be done about this?", "merchant_quest_persuade_peace_6",[]],
[anyone|plyr,"merchant_quest_persuade_peace_5", [], "Alas, it seems nothing can be done about it.", "merchant_quest_persuade_peace_6",[]],
[anyone,"merchant_quest_persuade_peace_6", [], "There is a way to resolve the issue.\
 A particularly determined person can perhaps persuade one or both of these lords to accept making peace.\
 And even if that fails, it can be possible to see that these lords are defeated by force and taken prisoner.\
 If they are captive, they will lose their influence and they can no longer oppose a settlement... What do you think? Can you do it?",
   "merchant_quest_persuade_peace_7",[]],
[anyone|plyr,"merchant_quest_persuade_peace_7", [], "It seems difficult. But I will try.", "merchant_quest_persuade_peace_8",[]],
[anyone|plyr,"merchant_quest_persuade_peace_7", [], "If the price is right, I may.", "merchant_quest_persuade_peace_8",[]],
[anyone|plyr,"merchant_quest_persuade_peace_7", [], "Forget it. This is not my problem.", "merchant_quest_persuade_peace_8",[]],
[anyone,"merchant_quest_persuade_peace_8", [], "Most of the merchants in the town will gladly open up their purses to support such a plan.\
 I think we can collect {reg12} mon between ourselves.\
 We will be happy to reward you with that sum, if you can work this out.\
 Convince {s12} and {s13} to accept a peace settlement,\
 and if either of them proves too stubborn, make sure he falls captive and can not be ransomed until a peace deal is settled.",
   "merchant_quest_persuade_peace_9",[
       (quest_get_slot, ":quest_object_troop", "qst_persuade_lords_to_make_peace", slot_quest_object_troop),
       (quest_get_slot, ":quest_target_troop", "qst_persuade_lords_to_make_peace", slot_quest_target_troop),
       (str_store_troop_name_link, s12, ":quest_object_troop"),
       (str_store_troop_name_link, s13, ":quest_target_troop"),
       (quest_get_slot, ":quest_reward", "qst_persuade_lords_to_make_peace", slot_quest_gold_reward),
       (assign, reg12, ":quest_reward")]],
[anyone|plyr,"merchant_quest_persuade_peace_9", [], "All right. I will do my best.", "merchant_quest_persuade_peace_10",[]],
[anyone|plyr,"merchant_quest_persuade_peace_9", [], "Sorry. I can not do this.", "merchant_quest_persuade_peace_no",[]],
[anyone,"merchant_quest_persuade_peace_10", [], "Excellent. You will have our blessings.\
 I hope you can deal with those two old goats.\
 We will be waiting and hoping for the good news.", "close_window",[
     (str_store_party_name_link, s4, "$g_encountered_party"),
     (quest_get_slot, ":quest_target_faction", "qst_persuade_lords_to_make_peace", slot_quest_target_faction),
     (quest_get_slot, ":quest_object_troop", "qst_persuade_lords_to_make_peace", slot_quest_object_troop),
     (quest_get_slot, ":quest_target_troop", "qst_persuade_lords_to_make_peace", slot_quest_target_troop),
     (quest_get_slot, ":quest_reward", "qst_persuade_lords_to_make_peace", slot_quest_gold_reward),
     (assign, reg12, ":quest_reward"),
     (str_store_troop_name_link, s12, ":quest_object_troop"),
     (str_store_troop_name_link, s13, ":quest_target_troop"),
     (str_store_faction_name_link, s14, ":quest_target_faction"),
     (str_store_faction_name_link, s15, "$g_encountered_party_faction"),
     (setup_quest_text,"qst_persuade_lords_to_make_peace"),
     (str_store_string, s2, "@The chief merchant of {s4} promised you {reg12} mon if you can make sure that\
 {s12} and {s13} no longer pose a threat to a peace settlement between {s15} and {s14}.\
 In order to do that, you must either convince them or make sure they fall captive and remain so until a peace agreement is made."),
     (call_script, "script_start_quest", "qst_persuade_lords_to_make_peace", "$g_talk_troop"),
     (quest_get_slot, ":quest_object_troop", "qst_persuade_lords_to_make_peace", slot_quest_object_troop),
     (quest_get_slot, ":quest_target_troop", "qst_persuade_lords_to_make_peace", slot_quest_target_troop),
     (call_script, "script_report_quest_troop_positions", "qst_persuade_lords_to_make_peace", ":quest_object_troop", 3),
     (call_script, "script_report_quest_troop_positions", "qst_persuade_lords_to_make_peace", ":quest_target_troop", 4),
     ]],
[anyone,"merchant_quest_persuade_peace_no", [], "Don't say no right away. Think about this for some time.\
 If there is a {man/lady} who can manage to do this, it is you.",
   "close_window",[]],
[anyone,"merchant_quest_requested",
   [
     (eq, "$random_merchant_quest_no", "qst_deal_with_night_bandits"),
     ],
   "Do I indeed! There's a group of bandits infesting the town, and I'm at the end of my rope as to how to deal with them.\
 They've been ambushing and robbing townspeople under the cover of night,\
 and then fading away quick as lightning when the guards finally show up. We've not been able to catch a one of them.\
 They only attack lone people, never daring to show themselves when there's a group about.\
 I need someone who can take on these bandits alone and win. That seems to be the only way of bringing them to justice.\
 Are you up to the task?", "merchant_quest_deal_with_night_bandits",
   []],
[anyone,"merchant_quest_brief",
   [
     (eq,"$random_merchant_quest_no","qst_deal_with_night_bandits"),
     ],
   "There's a group of bandits infesting the town, and I'm at the end of my rope as to how to deal with them.\
 They've been ambushing and robbing townspeople under the cover of night,\
 and then fading away quick as lightning when the guards finally show up. We've not been able to catch a one of them.\
 They only attack lone people, never daring to show themselves when there's a group about.\
 I need someone who can take on these bandits alone and win. That seems to be the only way of bringing them to justice.\
 Are you up to the task?", "merchant_quest_deal_with_night_bandits",
   []],
[anyone|plyr,"merchant_quest_deal_with_night_bandits", [],
   "Killing bandits? Why, certainly!",
   "deal_with_night_bandits_quest_taken",
   [
     (str_store_party_name_link, s14, "$g_encountered_party"),
     (setup_quest_text, "qst_deal_with_night_bandits"),
     (str_store_string, s2, "@The elder merchant of {s14} has asked you to deal with a group of bandits terrorising the streets of {s14}. They only come out at night, and only attack lone travellers on the streets."),
     (call_script, "script_start_quest", "qst_deal_with_night_bandits", "$g_talk_troop"),
     ]],
[anyone|plyr, "merchant_quest_deal_with_night_bandits", [],
   "My apologies, I'm not interested.", "merchant_quest_stall",[]],
[anyone,"merchant_quest_requested", [(eq, "$random_merchant_quest_no", "qst_move_cattle_herd"),
                                       (quest_get_slot, ":target_center", "qst_move_cattle_herd", slot_quest_target_center),
                                       (str_store_party_name,s13,":target_center"),],
   "One of the merchants here is looking for herdsmen to take his cattle to the market at {s13}.", "merchant_quest_brief",
   []],
[anyone,"merchant_quest_brief",
   [
    (eq,"$random_merchant_quest_no","qst_move_cattle_herd"),
    (quest_get_slot, reg8, "qst_move_cattle_herd", slot_quest_gold_reward),
    (quest_get_slot, ":target_center", "qst_move_cattle_herd", slot_quest_target_center),
    (str_store_party_name, s13, ":target_center"),
    ],
   "The cattle herd must be at {s13} within 30 days. Sooner is better, much better,\
 but it must be absolutely no later than 30 days.\
 If you can do that, I'd be willing to pay you {reg8} mon for your trouble. Interested?", "move_cattle_herd_quest_brief",
   []],
[anyone,"merchant_quest_requested", [], "I am afraid I can't offer you a job right now.", "mayor_pretalk",[]],
[anyone,"bandit_introduce", [
      (store_random_in_range, ":rand", 11, 15),
        (str_store_string, s11, "@I can smell a fat purse a mile away. Methinks yours could do with some lightening, eh?"),
        (str_store_string, s12, "@Why, it be another traveller, chance met upon the road! I should warn you, country here's a mite dangerous for a good {fellow/woman} like you. But for a small donation my boys and I'll make sure you get rightways to your destination, eh?"),
        (str_store_string, s13, "@Well well, look at this! You'd best start coughing up some silver, friend, or me and my boys'll have to break you."),
		(str_store_string, s14, "@There's a toll for passin' through this land, payable to us, so if you don't mind we'll just be collectin' our due from your purse..."),
        (str_store_string_reg, s5, ":rand"),
#gekokujo 3.0 no more bandit talk start
    ], "{s5}", "bandit_talk",[]],
[anyone|plyr,"bandit_talk", [], "I'll give you nothing but cold steel, you scum!", "close_window",[[encounter_attack]]],
[anyone|plyr,"bandit_talk", [], "There's no need to fight. I can pay for free passage.", "bandit_barter",[]],
[anyone,"bandit_barter",
   [(store_relation, ":bandit_relation", "fac_player_faction", "$g_encountered_party_faction"),
    (ge, ":bandit_relation", -50),
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
    (store_div, "$bandit_tribute", ":total_value", 10), #10000 gold = excellent_target
    (val_max, "$bandit_tribute", 10),
    (assign, reg5, "$bandit_tribute")
    ], "Silver without blood, that's our favourite kind! Hmm, having a look at you, I reckon you could easily come up with {reg5} mon. Pay it, and we'll let you be on your way.", "bandit_barter_2",[]],
[anyone|plyr,"bandit_barter_2", [[store_troop_gold,reg(2)],[ge,reg(2),"$bandit_tribute"],[assign,reg(5),"$bandit_tribute"]],
   "Very well, take it.", "bandit_barter_3a",[[troop_remove_gold, "trp_player","$bandit_tribute"]]],
[anyone|plyr,"bandit_barter_2", [],
   "I don't have that much money with me", "bandit_barter_3b",[]],
[anyone,"bandit_barter_3b", [],
   "That's too bad. I guess we'll just have to sell you into slavery. Take {him/her}!", "close_window",[[encounter_attack]]],
[anyone,"bandit_barter", [],
   "Hey, I've heard of you! You slaughter us freebooters like dogs, and now you expect us to let you go for a few stinking coins?\
 Forget it. You gave us no quarter, and you'll get none from us.", "close_window",[]],
[anyone,"bandit_barter_3a", [], "Heh, that wasn't so hard, was it? All right, we'll let you go now. Be off.", "close_window",[
    (store_current_hours,":protected_until"),
    (val_add, ":protected_until", 72),
    (party_set_slot,"$g_encountered_party",slot_party_ignore_player_until,":protected_until"),
    (party_ignore_player, "$g_encountered_party", 72),
    (assign, "$g_leave_encounter",1)
    ]],
[anyone|plyr,"bandit_meet", [], "Your luck has run out, wretch. Prepare to die!", "bandit_attack",
   [(store_relation, ":bandit_relation", "fac_player_faction", "$g_encountered_party_faction"),
    (val_sub, ":bandit_relation", 3),
    (val_max, ":bandit_relation", -100),
    (set_relation, "fac_player_faction", "$g_encountered_party_faction", ":bandit_relation"),
    (party_ignore_player, "$g_encountered_party", 0),
    (party_set_slot,"$g_encountered_party",slot_party_ignore_player_until, 0),
    ]],
[anyone,"bandit_attack", [
      (store_random_in_range, ":rand", 11, 15),
        (str_store_string, s11, "@Another fool come to throw {him/her}self on my weapon, eh? Fine, let's fight!"),
        (str_store_string, s12, "@We're not afraid of you, {sirrah/wench}. Time to bust some heads!"),
        (str_store_string, s13, "@That was a mistake. Now I'm going to have to make your death long and painful."),
        (str_store_string, s14, "@Brave words. Let's see you back them up with deeds, cur!"),
        (str_store_string_reg, s5, ":rand"),
      ], "{s5}", "close_window",[]],
[anyone|plyr,"bandit_meet", [], "Never mind, I have no business with you.", "close_window",[(assign, "$g_leave_encounter", 1)]],
[anyone|plyr,"merchant_quest_4e",
  [
    (try_begin),
      (eq, "$g_killed_first_bandit", 1),
      (gt, "$number_of_bandits_killed_by_player", 2),
      (str_store_string, s1, "str_you_fought_well_at_town_fight_survived_answer"),
    (else_try),
      (eq, "$g_killed_first_bandit", 1),
      (gt, "$number_of_bandits_killed_by_player", 0),
      (str_store_string, s1, "str_you_fought_normal_at_town_fight_survived_answer"),
    (else_try),
      (eq, "$g_killed_first_bandit", 1),
      (eq, "$number_of_bandits_killed_by_player", 0),
      (str_store_string, s1, "str_you_fought_bad_at_town_fight_survived_answer"),
    (else_try),
      (eq, "$g_killed_first_bandit", 0),
      (ge, "$number_of_bandits_killed_by_player", 2),
      (str_store_string, s1, "str_you_fought_well_at_town_fight_answer"),
    (else_try),
      (str_store_string, s1, "str_you_wounded_at_town_fight_answer"),
    (try_end),
  ],
  "{s1}", "merchant_finale",
  [
    (assign, "$dialog_with_merchant_ended", 1),
  ]],
[anyone|plyr,"merchant_quest_4e",
  [
  ],
  "Heaven alone grants us victory.", "merchant_finale",
[  (assign, "$dialog_with_merchant_ended", 1),
  ]],
[anyone|plyr,"merchant_quest_4e",
  [],
  "I'm glad to see that you're alive, too.", "merchant_finale",
  [
    (assign, "$dialog_with_merchant_ended", 1),
  ]],
[anyone,"merchant_quest_1_prologue_1",
  [
  ],
  "I have tried to live my life while ignoring the samurai, even in these turbulent times. I figured that if I kept my head down, none of their plots or wars would affect me. I was wrong. They... They killed my brother.", "merchant_quest_1_prologue_2",
  []],
[anyone,"merchant_quest_1_prologue_2",
  [],
  "Minemaru... He was a hothead for sure. Maybe he showed disrespect to a haughty lordling? I don't know what actually happened, but it doesn't matter to me whether he brought it upon himself or not. Nobody should be so exalted that they could kill a brother, son, or father just because they weren't grovelled to as they wished. This is no way for the rest of us to live.", "merchant_quest_1_prologue_3",
  []],
[anyone,"merchant_quest_1_prologue_3",
  [],
  "My other brother, Horenbo, tried to investigate the murder, but he's disappeared since. I originally feared the worst, but I've just come across a rumor that says he's still alive, as a captive. So here's what I ask of you: gather a small party, track down who has taken him, teach them a lesson they won't forget, and get Horenbo home safe. In return, you'll earn my eternal gratitude and a large sum of money. What do you say?", "merchant_quest_1a",
  []],
[anyone|plyr,"merchant_quest_1a",
  [
  ],
  "I am interested.", "merchant_quest_1b",[]],
[anyone|plyr,"merchant_quest_1a",
  [
  ],
  "I am not interested, have more important business to do.", "close_window",
  [
    (assign, "$dialog_with_merchant_ended", 1),
  ]],
[anyone|plyr,"merchant_quest_1a",
  [
     (ge, "$cheat_mode", 1),
  ],
  "{!}[CHEAT] I have played this before, and would prefer to skip the tutorial.", "dplmc_devel_merchant_quest_skip",
  []],
[anyone,"merchant_quest_1b",
  [
  ],
  "You won't be able to do this by yourself, though. If you try and take on a samurai and his retainers single-handedly, you will surely lose your head. You must round up a group of volunteers and form a band. There's always a few boys in the villages around here, looking for work that's more interesting than tilling the soil or hauling water. They'll follow you if you pay. So... Take this purse of 100 mon. Consider it an advance on your reward. Go round to the villages, and use the money to hire some help. I'll reckon that you need at least five men to take on these scoundrels.", "merchant_quest_1c",
  [
    (call_script, "script_troop_add_gold", "trp_player", 100),

    (str_store_troop_name, s9, "$g_talk_troop"),
    (str_store_party_name, s1, "$g_starting_town"),
    (str_store_string, s2, "str_start_up_quest_message_1"),

    (call_script, "script_start_quest", "qst_collect_men", "$g_talk_troop"),

    (party_get_position, pos1, "$current_town"),
  ]],
[anyone|plyr,"merchant_quest_1c",
  [
  ],
  "Very good, sir. I'll go collect some men from around the villages.", "merchant_quest_1d",[]],
[anyone,"merchant_quest_1d",
  [
    (str_store_party_name, s1, "$current_town"),
  ],
  "Good. You can find me again in the inn here in {s1} after you've got your group together. Then we'll speak about what we do next.", "close_window",
  [
    (assign, "$dialog_with_merchant_ended", 1),
  ]],
]
