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


dialogs_recruit_mercenary = [
[anyone, "fighter_pretalk", [],
"Tell me what kind of practice you want.", "fighter_talk", []],
[anyone|plyr, "fighter_talk",
[],
"I want to practice attacking.", "fighter_talk_train_attack", []],
[anyone|plyr, "fighter_talk",
[],
"I want to practice blocking with my weapon.", "fighter_talk_train_parry", []],
[anyone|plyr, "fighter_talk",
[],
"Let's do some sparring practice.", "fighter_talk_train_combat", []],
[anyone|plyr, "fighter_talk",
[(eq,1,0)],
"{!}TODO: Let's train chamber blocking.", "fighter_talk_train_chamber", []],
[anyone|plyr, "fighter_talk",
[],
"[Leave]", "close_window", []],
[anyone, "fighter_talk_train_attack",
[
(get_player_agent_no, ":player_agent"),
(agent_has_item_equipped, ":player_agent", "itm_gekokujo_practice_katana"), #TODO: add other melee weapons
],
"All right. There are four principle directions for attacking. These are overhead swing, right swing, left swing and thrust.\
Now, I will tell you which direction to attack from and you must try to do the correct attack.\
^^(Move your mouse while you press the left mouse button to specify attack direction. For example, to execute an overhead attack, move the mouse up at the instant you press the left mouse button.\
The icons on your screen will help you do the correct action.)" , "fighter_talk_train_attack_2",
[]],
[anyone|plyr, "fighter_talk_train_attack_2",  [],
"Let's begin then. I am ready.", "close_window",
[
(assign, "$g_tutorial_training_ground_melee_trainer_attack", "$g_talk_troop"),
(assign, "$g_tutorial_training_ground_melee_state", 0),
(assign, "$g_tutorial_training_ground_melee_trainer_action_state", 0),
(assign, "$g_tutorial_training_ground_current_score", 0),
(assign, "$g_tutorial_training_ground_current_score_2", 0),
(assign, "$g_tutorial_update_mouse_presentation", 0),
]],
[anyone|plyr, "fighter_talk_train_attack_2",  [],
"Actually I want to do something else.", "fighter_pretalk", []],
[anyone, "fighter_talk_train_attack",
[(str_store_string, s3, "str_tutorial_training_ground_warning_no_weapon")],
"{!}{s3}", "close_window",
[]],
[anyone, "fighter_talk_train_parry",
[
(get_player_agent_no, ":player_agent"),
(agent_has_item_equipped, ":player_agent", "itm_gekokujo_practice_katana"), #TODO: add other melee weapons
],
"Unlike a shield, blocking with a weapon can only stop attacks coming from one direction.\
For example if you block up, you'll deflect overhead attacks, but you can still be hit by side swings or thrust attacks.\
^^(You must press and hold down the right mouse button to block.)", "fighter_talk_train_parry_2", [ ]],
[anyone, "fighter_talk_train_parry_2", [],
"I'll now attack you with different types of strokes, and I will wait until you do the correct block before attacking.\
Try to do the correct block as soon as you can.\
^^(This practice is easy to do with the 'automatic block direction' setting which is the default.\
If you go to the Options menu and change defend direction control to 'mouse movement' or 'keyboard', you'll need to manually choose block direction. This is much more challenging, but makes the game much more interesting.\
This practice can be very useful if you use manual blocking.)", "fighter_talk_train_parry_3",
[]],
[anyone|plyr, "fighter_talk_train_parry_3",  [],
"Let's begin then. I am ready.", "close_window",
[
(assign, "$g_tutorial_training_ground_melee_trainer_parry", "$g_talk_troop"),
(assign, "$g_tutorial_training_ground_melee_state", 0),
(assign, "$g_tutorial_training_ground_melee_trainer_action_state", 0),
(assign, "$g_tutorial_training_ground_current_score", 0),
]],
[anyone|plyr, "fighter_talk_train_parry_3",  [],
"Actually I want to do something else.", "fighter_pretalk", []],
[anyone, "fighter_talk_train_parry",
[(str_store_string, s3, "str_tutorial_training_ground_warning_no_weapon")],
"{!}{s3}", "close_window",
[]],
[anyone, "fighter_talk_train_chamber",
[
(get_player_agent_no, ":player_agent"),
(agent_has_item_equipped, ":player_agent", "itm_gekokujo_practice_katana"), #TODO: add other melee weapons
],
"{!}TODO: OK.", "close_window",
[
(assign, "$g_tutorial_training_ground_melee_trainer_chamber", "$g_talk_troop"),
(assign, "$g_tutorial_training_ground_melee_state", 0),
(assign, "$g_tutorial_training_ground_melee_trainer_action_state", 0),
(assign, "$g_tutorial_training_ground_current_score", 0),
]],
[anyone, "fighter_talk_train_chamber",
[(str_store_string, s3, "str_tutorial_training_ground_warning_no_weapon")],
"{!}{s3}", "close_window",
[]],
[anyone, "fighter_talk_train_combat",
[
(get_player_agent_no, ":player_agent"),
(agent_has_item_equipped, ":player_agent", "itm_gekokujo_practice_katana"), #TODO: add other melee weapons
],
"Sparring is an excellent way to prepare for actual combat.\
We'll fight each other with non-lethal weapons now, until one of us falls to the ground.\
You can get some bruises of course, but better that than being cut down in the real thing.", "fighter_talk_train_combat_2",
[]],
[anyone|plyr, "fighter_talk_train_combat_2",  [],
"Let's begin then. I am ready.", "close_window", [
(assign, "$g_tutorial_training_ground_melee_trainer_combat", "$g_talk_troop"),
(assign, "$g_tutorial_training_ground_melee_state", 0),
(assign, "$g_tutorial_training_ground_melee_trainer_action_state", 0),
]],
[anyone|plyr, "fighter_talk_train_combat_2",  [],
"Actually I want to do something else.", "fighter_pretalk", []],
[anyone, "fighter_talk_train_combat",
[(str_store_string, s3, "str_tutorial_training_ground_warning_no_weapon")],
"{!}{s3}", "close_window",
[]],
[anyone|plyr, "fighter_parry_try_again",
[],
"Yes. Let's try again.", "fighter_talk_train_parry", []],
[anyone|plyr, "fighter_parry_try_again",
[],
"No, I think I am done for now.", "fighter_talk_leave_parry", []],
[anyone|plyr, "fighter_parry_warn",
[],
"I am sorry. Let's try once again.", "fighter_talk_train_parry", []],
[anyone|plyr, "fighter_parry_warn",
[],
"Sorry. I must leave this practice now.", "fighter_talk_leave_parry", []],
[anyone, "fighter_talk_leave_parry",
[],
"All right. As you wish.", "close_window", []],
[anyone|plyr, "fighter_combat_try_again",
[],
"Yes. Let's do another round.", "fighter_talk_train_combat", []],
[anyone|plyr, "fighter_combat_try_again",
[],
"No. That was enough for me.", "fighter_talk_leave_combat", []],
[anyone, "fighter_talk_leave_combat",
[],
"Well, all right. Talk to me again if you change your mind.", "close_window", []],
[anyone|plyr, "fighter_chamber_warn", # unused
[],
"{!}TODO: Sorry, let's try once again.", "fighter_talk_train_chamber", []],
[anyone|plyr, "fighter_chamber_warn", # unused
[],
   "{!}TODO: Sorry. I want to leave the exercise.", "close_window", []],
[party_tpl|pt_manhunters|plyr,"manhunter_talk_b", [], "Yes, they went this way about an hour ago.", "manhunter_talk_b1",[]],
[party_tpl|pt_manhunters,"manhunter_talk_b1", [], "I knew it! Come on, boys, lets go get these bastards! Thanks a lot, friend.", "close_window",[(assign, "$g_leave_encounter",1)]],
[party_tpl|pt_manhunters|plyr,"manhunter_talk_b", [], "No, haven't seen any bandits lately.", "manhunter_talk_b2",[]],
[party_tpl|pt_manhunters,"manhunter_talk_b2", [], "Bah. They're holed up in this country like rats, but we'll smoke them out sooner or later.", "close_window",[(assign, "$g_leave_encounter",1)]],
# gekokujo: hostile patrol only - player answers "right in front of you" and starts the fight
[party_tpl|pt_manhunters|plyr,"manhunter_talk_b", [
(store_faction_of_party, ":player_faction", "p_main_party"),
(store_faction_of_party, ":encountered_faction", "$g_encountered_party"),
(store_relation, ":relation", ":player_faction", ":encountered_faction"),
(lt, ":relation", 0),
], "Right in front of you!", "close_window",
[[encounter_attack]]],
[anyone|plyr, "mercenary_after_recruited", [],
   "Make your preparations. We'll be moving at dawn.", "mercenary_after_recruited_2", []],
[anyone|plyr, "mercenary_after_recruited", [],
   "Take your time. We'll be staying in this town for a while.", "mercenary_after_recruited_2", []],
[anyone, "mercenary_after_recruited_2", [], "Yes {sir/madam}. We'll be ready when you tell us to leave.", "close_window", []],
[anyone|plyr, "mercenary_tavern_talk", [(party_get_slot, ":mercenary_amount", "$g_encountered_party", slot_center_mercenary_troop_amount),
                                          (eq, ":mercenary_amount", "$temp"),
                                          (party_get_slot, ":mercenary_troop", "$g_encountered_party", slot_center_mercenary_troop_type),
                                          (call_script, "script_game_get_join_cost", ":mercenary_troop"),
                                          (store_mul, reg5, "$temp", reg0),
                                          ],
   "All right. I will hire all of you. Here is {reg5} mon.", "mercenary_tavern_talk_hire", []],
[anyone|plyr, "mercenary_tavern_talk", [(party_get_slot, ":mercenary_amount", "$g_encountered_party", slot_center_mercenary_troop_amount),
                                          (lt, "$temp", ":mercenary_amount"),
                                          (gt, "$temp", 0),
                                          (assign, reg6, "$temp"),
                                          (party_get_slot, ":mercenary_troop", "$g_encountered_party", slot_center_mercenary_troop_type),
                                          (call_script, "script_game_get_join_cost", ":mercenary_troop"),
                                          (store_mul, reg5, "$temp", reg0),
                                          ],
   "All right. But I can only hire {reg6} of you. Here is {reg5} mon.", "mercenary_tavern_talk_hire", []],
[anyone, "mercenary_tavern_talk_hire", [(store_random_in_range, ":rand", 0, 4),
                                          (try_begin),
                                            (eq, ":rand", 0),
                                            (gt, "$temp", 1),
											##diplomacy start+ lads -> {reg65?companions:lads}; {sir/madame} -> {s0}
											(call_script, "script_dplmc_print_subordinate_says_sir_madame_to_s0"),
                                            (str_store_string, s17,
                                             "@You chose well, {s0}. My {reg65?companions:lads} know how to keep their word and earn their pay."),
											 ##diplomacy end+
                                          (else_try),
                                            (eq, ":rand", 1),
											##diplomacy start+ {sir/madame} -> {s0}
											(call_script, "script_dplmc_print_subordinate_says_sir_madame_to_s0"),
                                            (str_store_string, s17,
                                             "@Well done, {s0}. Keep the money and sake coming our way, and there's no foe in Japan you need fear."),
											 ##diplomacy end+
                                          (else_try),
                                            (eq, ":rand", 2),
											##diplomacy start+ {sir/madame} -> {s0}
											(call_script, "script_dplmc_print_subordinate_says_sir_madame_to_s0"),
                                            (str_store_string, s17,
                                             "@We are at your service, {s0}. Point us in the direction of those who need hurting, and we'll do the rest."),
											 ##diplomacy end+
                                          (else_try),
                                            (str_store_string, s17,
                                             "str_you_will_not_be_disappointed_sirmadam_you_will_not_find_better_warriors_in_all_calradia"),
                                          (try_end),],
   "{s17}", "close_window", [
                                          (party_get_slot, ":mercenary_troop", "$g_encountered_party", slot_center_mercenary_troop_type),
                                          (call_script, "script_game_get_join_cost", ":mercenary_troop"),
                                          (store_mul, ":total_cost", "$temp", reg0),
                                          (troop_remove_gold, "trp_player", ":total_cost"),
                                          (party_add_members, "p_main_party", ":mercenary_troop", "$temp"),
                                          (party_set_slot, "$g_encountered_party", slot_center_mercenary_troop_amount, 0),
                                          ]],
[anyone|plyr, "mercenary_tavern_talk", [(eq, "$temp", 0),
                                          (party_get_free_companions_capacity, ":free_capacity", "p_main_party"),
                                          (ge, ":free_capacity", 1)],
##diplomacy start+ Gender-check to avoid accidental absurdities if there are female mercenaries
   "That sounds good. But I can't afford to hire any more {reg65?soldiers:men} right now.", "tavern_mercenary_cant_lead", []],
[anyone|plyr, "mercenary_tavern_talk", [(eq, "$temp", 0),
                                          (party_get_free_companions_capacity, ":free_capacity", "p_main_party"),
                                          (eq, ":free_capacity", 0)],
##diplomacy start+ Gender-check to avoid accidental absurdities if there are female mercenaries
   "That sounds good. But I can't lead any more {reg65?soldiers:men} right now.", "tavern_mercenary_cant_lead", []],
[anyone|plyr, "mercenary_tavern_talk", [],
   "Sorry. I don't need any other men right now.", "close_window", []],
[anyone|plyr, "trainer_intro_1", [],
   "Thank you for your advice. This place looks like a training field. Maybe I can learn about fighting here?", "trainer_intro_2", []],
[anyone,"trainer_intro_2", [],
   "Indeed you can. I am a veteran soldier... fought a good deal in the wars in my time. But these days, I train young novices in this area.\
 I can find you some opponents to practice with if you like. Or if you have any questions about the theory of combat, feel free to ask.", "trainer_intro_3",[]],
[anyone|plyr, "trainer_intro_3", [],
   "Yes, I do have a few questions.", "trainer_intro_4a", []],
[anyone|plyr, "trainer_intro_3", [],
   "Actually, I can move on to practice.", "trainer_intro_4b", []],
[anyone, "trainer_intro_4a", [],
   "Well, ask anything you like.", "trainer_talk_combat", []],
[anyone, "trainer_intro_4b", [],
   "Good. It's good to find someone eager for practice. Let's see what you will do.", "trainer_practice_1", []],
[anyone,"trainer_pretalk", [],
   "Ah, are you ready for some training?", "trainer_talk",[]],
[anyone|plyr,"trainer_talk", [],
   "I am ready for some practice.", "trainer_practice_1",[]],
[anyone|plyr,"trainer_talk", [],
   "First, tell me something about combat...", "trainer_combat_begin",[]],
[anyone|plyr,"trainer_talk", [],
   "I need to leave now. Farewell.", "close_window",[]],
[anyone,"trainer_combat_begin", [],
   "What do you want to know?", "trainer_talk_combat",[]],
[anyone,"trainer_combat_pretalk", [],
   "What else do you want to know?", "trainer_talk_combat",[]],
[anyone|plyr,"trainer_talk_combat", [], "Tell me about defending myself.", "trainer_explain_defense",[]],
[anyone|plyr,"trainer_talk_combat", [], "Tell me about attacking with weapons.", "trainer_explain_attack",[]],
[anyone|plyr,"trainer_talk_combat", [], "Tell me about fighting on horseback.", "trainer_explain_horseback",[]],
[anyone|plyr,"trainer_talk_combat", [], "I guess I know all the theory I need. Let's talk about something else.", "trainer_pretalk",[]],
[anyone,"trainer_explain_defense", [], "Good question. The first thing you should know as a fighter is how to defend yourself.\
 Keeping yourself out of harm's way is the first rule of combat, and it is much more important than giving harm to others.\
 Everybody can swing a sword around and hope to cut some flesh, but only those fighters that are experts at defense live to tell of it.",
	"trainer_explain_defense_2",[]],
[anyone,"trainer_explain_defense_2", [], "Now. Defending yourself is easiest if you are equipped with a shield.\
 Just block with your shield. [Hold down the right mouse button to defend yourself with the shield.] In this state, you will be able to deflect all attacks that come from your front. However, you will still be open to strikes from your sides or your back.", "trainer_explain_defense_3",[]],
[anyone|plyr,"trainer_explain_defense_3", [], "What if I don't have a shield?", "trainer_explain_defense_4",[]],
[anyone,"trainer_explain_defense_4", [], "Then you will have to use your weapon to block your opponent.\
 This is a bit more difficult than defending with a shield.\
 Defending with a weapon, you can block against only ONE attack direction.\
 That is, you block against either overhead swings, side swings or thrusts.\
 Therefore you must watch your opponent carefully and start to block AFTER he starts his attack.\
 In this way you will be able to block against the direction of his current attack.\
 If you start to block BEFORE he makes his move, he may just attack in another direction than the one you are blocking against and score a hit.", "trainer_combat_pretalk",[]],
[anyone,"trainer_explain_attack", [], "Good question. Attacking is the best defence, they say.\
 A tactic many fighters find useful is taking an offensive stance and readying your weapon for attack, waiting for the right moment for swinging it.\
 [You can ready your weapon for attack by pressing and holding down the left mouse button.]", "trainer_explain_attack_2",[]],
[anyone|plyr,"trainer_explain_attack_2", [], "That sounds useful.", "trainer_explain_attack_3",[]],
[anyone,"trainer_explain_attack_3", [], "It is a good tactic, but remember that, your opponent may see that and take a defensive stance against the direction you are swinging your weapon.\
 If that happens, you must break your attack and quickly attack from another direction\
 [You may cancel your current attack by quickly tapping the right mouse button].", "trainer_explain_attack_4",[]],
[anyone|plyr,"trainer_explain_attack_4", [], "If my opponent is defending against the direction I am attacking from, I will break and use another direction.", "trainer_explain_attack_5",[]],
[anyone,"trainer_explain_attack_5", [], "Yes, selecting the direction you swing your weapon is a crucial skill.\
 There are four main directions you may use: right swing, left swing, overhead swing and thrust. You must use each one wisely.\
 [to control your swing direction with default controls, move your mouse in the direction you want to swing from as you press the left mouse button].", "trainer_combat_pretalk",[]],
[anyone,"trainer_explain_horseback", [], "Very good question. A horse may be a warrior's most powerful weapon in combat.\
 It gives you speed, height, power and initiative. A lot of deadly weapons will become even deadlier on horseback.\
 However you must pay particular attention to horse-mounted enemies couching their lances, as they may take down any opponent in one hit.\
 [To use the couched lance yourself, wield a lance or similar weapon, and speed up your horse without pressing attack or defense buttons.\
 after you reach a speed, you'll lower your lance. Then try to target your enemies by maneuvering your horse.]", "trainer_combat_pretalk",[]],
[anyone,"trainer_practice_1", [(eq,"$training_system_explained", 0)],
 "I train novices in four stages, each tougher than the one before.\
 To finish a stage and advance to the next one, you have to win three fights in a row.", "trainer_practice_1",
   [
     (assign, "$num_opponents_to_beat_in_a_row", 3),
     (assign, "$novicemaster_opponent_troop", "trp_novice_fighter"),
     (assign, "$training_system_explained", 1),
     ]],
[anyone,"trainer_practice_1",
   [(ge,"$novice_training_difficulty",4)],
 "You have passed all stages of training. But if you want you can still practice. Are you ready?", "novicemaster_are_you_ready",
   [(assign,"$num_opponents_to_beat_in_a_row",99999)]],
[anyone,"trainer_practice_1",
   [(eq,"$num_opponents_to_beat_in_a_row",0),(eq,"$novice_training_difficulty",0)],
 "Way to go {lad/lass}. With this victory, you have advanced to the next training level. From now on your opponents will be regular fighters, not the riff-raff off the street, so be on your toes.",
   "trainer_practice_1",
   [[assign,"$num_opponents_to_beat_in_a_row",3],
    [val_add,"$novice_training_difficulty",1],
    [add_xp_to_troop,100],
    [assign,"$novicemaster_opponent_troop","trp_regular_fighter"]]],
[anyone,"trainer_practice_1",
   [[eq,"$num_opponents_to_beat_in_a_row",0],[eq,"$novice_training_difficulty",1]],
 "Way to go {lad/lass}. Welcome to the third training level. From now on your opponents will be veteran fighters; soldiers and arena regulars and the like. These guys know some dirty tricks, so keep your defense up.",
   "trainer_practice_1",
   [[assign,"$num_opponents_to_beat_in_a_row",3],
    [val_add,"$novice_training_difficulty",1],
    [add_xp_to_troop,100],
    [assign,"$novicemaster_opponent_troop","trp_veteran_fighter"]]],
[anyone,"trainer_practice_1",
   [[eq,"$num_opponents_to_beat_in_a_row",0],[eq,"$novice_training_difficulty",2]],
 "You've got the heart of a champion, {lad/lass}, and the sword arm to match. From now on your opponents will be champion fighters.\
 These are the cream of the crop, the finest warriors I have trained. If you can best three of them in a row, you will join their ranks.",
   "trainer_practice_1",
   [[assign,"$num_opponents_to_beat_in_a_row",3],
    [val_add,"$novice_training_difficulty",1],
    [add_xp_to_troop,100],
    [assign,"$novicemaster_opponent_troop","trp_champion_fighter"]]],
[anyone,"trainer_practice_1",
   [[eq,"$num_opponents_to_beat_in_a_row",0],[eq,"$novice_training_difficulty",3]],
 "It does my heart good to see such a promising talent. You have passed all tiers of training. You can now tell everyone that you have been trained by the master of the training field.",
   "novicemaster_finish_training",
   [[assign,"$num_opponents_to_beat_in_a_row",3],
    [val_add,"$novice_training_difficulty",1],
    [add_xp_to_troop,300]]],
[anyone,"trainer_practice_1",
   [
     (assign, reg8, "$num_opponents_to_beat_in_a_row"),
     (str_store_troop_name, s9, "$novicemaster_opponent_troop"),
     ],
 "Your next opponent will be a {s9}. You need to win {reg8} more\
 fights in a row to advance to the next stage. Are you ready?", "novicemaster_are_you_ready",
   []],
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
[anyone|plyr,"arena_master_intro_1", [], "I am {playername}.", "arena_master_intro_2",[]],
[anyone,"arena_master_intro_2", [(store_encountered_party,reg(2)),(str_store_party_name,1,reg(2))],
   "Well met {playername}. I am the master of the tournaments here at {s1}. Talk to me if you want to join the fights.", "arena_master_pre_talk",[]],
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
[anyone,"arena_master_pre_talk", [], "What would you like to do?", "arena_master_talk",[]],
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
]
