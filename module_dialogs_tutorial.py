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
[anyone|plyr, "archer_talk",
[
(eq, "$g_tutorial_training_ground_archer_trainer_completed_chapters", 0),
],
"Yes, show me how to use ranged weapons.", "archer_challenge", []],
# [anyone|plyr, "archer_talk",
# [
# (gt, "$g_tutorial_training_ground_archer_trainer_completed_chapters", 0),
# ],
# "{!}TODO: I want to move to the next stage.", "archer_challenge", []],

[anyone|plyr, "archer_talk",
[],
"No, not now.", "close_window", []],
[trp_tutorial_master_archer, "archer_challenge",
[
(eq, "$g_tutorial_training_ground_archer_trainer_completed_chapters", 0),
],
"All right. Your first training will be in bowmanship. The bow is a difficult weapon to master. But once you are sufficiently good at it, you can shoot quickly and with great power.\
Go pick up the bow and arrows you see over there now and shoot those targets.", "archer_challenge_2",
[]],
# [trp_tutorial_master_archer, "archer_challenge",
# [
# (eq, "$g_tutorial_training_ground_archer_trainer_completed_chapters", 1),
# ],
# "{!}TODO: Make 3 shots with crossbow.", "archer_challenge_2",
# []],

# [trp_tutorial_master_archer, "archer_challenge",
# [],
# "{!}TODO: Make 3 shots with javelin.", "archer_challenge_2",
# []],

[anyone|plyr, "archer_challenge_2",
[],
"All right. I am ready.", "close_window",
[
(assign, "$g_tutorial_training_ground_archer_trainer_state", 1),
(try_begin),
 (eq, "$g_tutorial_training_ground_archer_trainer_completed_chapters", 0),
 (assign, "$g_tutorial_training_ground_archer_trainer_item_1", "itm_gekokujo_practice_yumi"),
 (assign, "$g_tutorial_training_ground_archer_trainer_item_2", "itm_gekokujo_practice_arrows"),
(else_try),
 (eq, "$g_tutorial_training_ground_archer_trainer_completed_chapters", 1),
 (assign, "$g_tutorial_training_ground_archer_trainer_item_1", "itm_gekokujo_practice_yumi"),
 (assign, "$g_tutorial_training_ground_archer_trainer_item_2", "itm_gekokujo_practice_arrows"),
(else_try),
 (assign, "$g_tutorial_training_ground_archer_trainer_item_1", "itm_gekokujo_practice_yumi"),
 (assign, "$g_tutorial_training_ground_archer_trainer_item_2", "itm_gekokujo_practice_arrows"),
(try_end),
]],
[anyone|plyr, "archer_challenge_2",
[],
"Just a minute. I want to do something else first.", "close_window",
[]],
[trp_tutorial_master_horseman, "horsemanship_end",
[
],
"Now, you can go talk with the melee fighters or the archery trainer if you haven't already done so. You need to learn everything you can to be prepared when you have to defend yourself.", "close_window",
[]],
[anyone|plyr, "horseman_talk",
[],
"Yes, I would like to practice riding.", "horseman_challenge", []],
[anyone|plyr, "horseman_talk",
[],
"Uhm. Maybe later.", "close_window", []],
# [trp_tutorial_master_horseman, "horseman_challenge",
# [
# (eq, "$g_tutorial_training_ground_player_continue_without_basics", 0),
# (this_or_next|eq, "$g_tutorial_training_ground_melee_trainer_attack_completed", 0),
# (eq, "$g_tutorial_training_ground_archer_trainer_completed_chapters", 0),
# ],
# "Hmm. Do you know how to use your weapons? You'd better learn to use those on foot before you start to train using them on horseback.", "horseman_ask",
# []],

# [anyone|plyr, "horseman_ask",
# [],
# "Yes, I know ", "horseman_challenge",
# [
# (assign, "$g_tutorial_training_ground_player_continue_without_basics", 1),
# ]],

# [anyone|plyr, "horseman_ask",
# [],
# "{!}TODO: No", "horseman_ask_2",
# []],

# [trp_tutorial_master_horseman, "horseman_ask_2",
# [],
# "{!}TODO: Come back later then.", "close_window",
# []],

[trp_tutorial_master_horseman, "horseman_challenge",
[
(eq, "$g_tutorial_training_ground_horseman_trainer_completed_chapters", 0),
],
"Good. Now, I will give you a few exercises that'll teach you riding and horseback weapon use.\
Your first assignment is simple. Just take your horse for a ride around the course.\
Go as slow or as fast as you like.\
Come back when you feel confident as a rider and I'll give you some tougher exercises.", "horseman_melee_challenge_2",
[]],
[anyone|plyr, "horseman_melee_challenge_2",
[],
"All right. I am ready.", "close_window",
[
(assign, "$g_tutorial_training_ground_horseman_trainer_state", 1),
(try_begin),
 (eq, "$g_tutorial_training_ground_horseman_trainer_completed_chapters", 0),
 (assign, "$g_tutorial_training_ground_horseman_trainer_item_1", -1),
 (assign, "$g_tutorial_training_ground_horseman_trainer_item_2", -1),
(else_try),
 (eq, "$g_tutorial_training_ground_horseman_trainer_completed_chapters", 1),
 (assign, "$g_tutorial_training_ground_horseman_trainer_item_1", "itm_gekokujo_practice_yari"),
 (assign, "$g_tutorial_training_ground_horseman_trainer_item_2", -1),
(else_try),
 (assign, "$g_tutorial_training_ground_horseman_trainer_item_1", "itm_gekokujo_practice_yumi"),
 (assign, "$g_tutorial_training_ground_horseman_trainer_item_2", "itm_gekokujo_practice_arrows"),
(try_end),
]],
[anyone|plyr, "horseman_melee_challenge_2",
[],
"Just a minute. I need to do something else first.", "close_window", []],
[anyone, "tutorial_troop_default",
[
(try_begin),
 (eq, "$g_tutorial_training_ground_intro_message_being_displayed", 1),
 (assign, "$g_tutorial_training_ground_intro_message_being_displayed", 0),
 (tutorial_message, -1), #remove tutorial intro immediately before a conversation
(try_end),
],
"Hey, I am trying to practice here. Go, talk with the archery trainer if you need guidance about ranged weapons.", "close_window", []],
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
##    [anyone|plyr,"trainer_talk", [],
##   "I have some novice soldiers with me. Can you train them?", "trainer_train_novices_1",[]],

    [anyone|plyr,"trainer_talk", [],
   "I need to leave now. Farewell.", "close_window",[]],
    [anyone,"trainer_combat_begin", [],
   "What do you want to know?", "trainer_talk_combat",[]],
    [anyone,"trainer_combat_pretalk", [],
   "What else do you want to know?", "trainer_talk_combat",[]],
    [anyone|plyr,"trainer_talk_combat", [], "Tell me about defending myself.", "trainer_explain_defense",[]],
    [anyone|plyr,"trainer_talk_combat", [], "Tell me about attacking with weapons.", "trainer_explain_attack",[]],
    [anyone|plyr,"trainer_talk_combat", [], "Tell me about fighting on horseback.", "trainer_explain_horseback",[]],
#    [anyone|plyr,"trainer_talk_combat", [], "Tell me about using ranged weapons.", "trainer_explain_ranged",[]],
#    [anyone|plyr,"trainer_talk_combat", [], "Tell me about weapon types.", "trainer_explain_weapon_types",[]],
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
]
