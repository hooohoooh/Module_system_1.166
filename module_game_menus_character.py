# -*- coding: UTF-8 -*-
# split feature file: game_menus - module
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from module_constants import *
from ym_gatling_shop import *

game_menus_character = [
  ("start_game_0",menu_text_color(0xFF000000)|mnf_disable_all_keys,
    "Welcome, adventurer, to Gekokujo. Before beginning the game you must create your character. Remember that in the Sengoku era, war and politics are usually dominated by male members of the nobility. That does not however mean that you should not choose to play a female character, or one who is not of noble birth. Male nobles may have a somewhat easier start, but women and commoners can attain all of the same goals -- and in fact may have a much more interesting if more challenging early game.",
    "none",
    [],
    [
     ("continue",[],"Continue...",
       [
         (assign, reg60, 1),
         (start_presentation, "prsnt_vc_options"),
        ]
       ),
      ("go_back",[],"Go back",
       [
         (change_screen_quit),
       ]),
    ]
  ),

  # Native Warband default character creation chain (restored verbatim from official module system)
  ("start_game_1",menu_text_color(0xFF000000)|mnf_disable_all_keys,
    "Select your character's gender.",
    "none",
    [],
    [
      ("start_male",[],"Male",
       [
         (troop_set_type,"trp_player", 0),
         (assign,"$character_gender",tf_male),
         (jump_to_menu,"mnu_start_character_1"),
        ]
       ),
      ("start_female",[],"Female",
       [
         (troop_set_type, "trp_player", 1),
         (assign, "$character_gender", tf_female),
         (jump_to_menu,"mnu_start_character_1"),
       ]
       ),
      ("go_back",[],"Go back",
       [
         (jump_to_menu,"mnu_start_game_0"),
       ]),
    ]
  ),

  (
    "start_character_1",mnf_disable_all_keys,
    "You were born years ago, in a land far away. Your father was...",
    "none",
    [
    (str_clear,s10),
    (str_clear,s11),
    (str_clear,s12),
    (str_clear,s13),
    (str_clear,s14),
    (str_clear,s15),
    ],
    [
    ("start_noble",[],"An impoverished noble.",[
      (assign,"$background_type",cb_noble),
      (assign, reg3, "$character_gender"),
      (str_store_string,s10,"@You came into the world a {reg3?daughter:son} of declining nobility,\
 owning only the house in which they lived. However, despite your family's hardships,\
 they afforded you a good education and trained you from childhood for the rigors of aristocracy and life at court."),
      (jump_to_menu,"mnu_start_character_2"),
    ]),
    ("start_merchant",[],"A travelling merchant.",[
      (assign,"$background_type",cb_merchant),
      (assign, reg3, "$character_gender"),
      (str_store_string,s10,"@You were born the {reg3?daughter:son} of travelling merchants,\
 always moving from place to place in search of a profit. Although your parents were wealthier than most\
 and educated you as well as they could, you found little opportunity to make friends on the road,\
 living mostly for the moments when you could sell something to somebody."),
      (jump_to_menu,"mnu_start_character_2"),
    ]),
    ("start_guard",[],"A veteran warrior.",[
      (assign,"$background_type",cb_guard),
      (assign, reg3, "$character_gender"),
      (str_store_string,s10,"@As a child, your family scrabbled out a meagre living from your father's wages\
 as a guardsman to the local lord. It was not an easy existence, and you were too poor to get much of an\
 education. You learned mainly how to defend yourself on the streets, with or without a weapon in hand."),
      (jump_to_menu,"mnu_start_character_2"),
    ]),
    ("start_forester",[],"A hunter.",[
      (assign,"$background_type",cb_forester),
      (assign, reg3, "$character_gender"),
      (str_store_string,s11,"@{reg3?daughter:son}"),
      (str_store_string,s10,"@You were the {reg3?daughter:son} of a family who lived off the woods,\
 doing whatever they needed to make ends meet. Hunting, woodcutting, making arrows,\
 even a spot of poaching whenever things got tight. Winter was never a good time for your family\
 as the cold took animals and people alike, but you always lived to see another dawn,\
 though your brothers and sisters might not be so fortunate."),
      (jump_to_menu,"mnu_start_character_2"),
    ]),
    ("start_nomad",[],"A steppe nomad.",[
      (assign,"$background_type",cb_nomad),
      (assign, reg3, "$character_gender"),
      (str_store_string,s11,"@{reg3?daughter:son}"),
      (str_store_string,s10,"@You were a child of the steppe, born to a tribe of wandering nomads who lived\
 in great camps throughout the arid grasslands.\
 Like the other tribesmen, your family revered horses above almost everything else, and they taught you\
 how to ride almost before you learned how to walk. "),
      (jump_to_menu,"mnu_start_character_2"),
    ]),
    ("start_thief",[],"A thief.",[
      (assign,"$background_type",cb_thief),
      (assign, reg3, "$character_gender"),
      (str_store_string,s10,"@As the {reg3?daughter:son} of a thief, you had very little 'formal' education.\
 Instead you were out on the street, begging until you learned how to cut purses, cutting purses\
 until you learned how to pick locks, all the way through your childhood.\
 Still, these long years made you streetwise and sharp to the secrets of cities and shadowy backways."),
      (jump_to_menu,"mnu_start_character_2"),
    ]),
    ("go_back",[],"Go back",
     [(jump_to_menu,"mnu_start_game_1"),
    ]),
    ]
  ),
  (
    "start_character_2",0,
    "{s10}^^ You started to learn about the world almost as soon as you could walk and talk. You spent your early life as...",
    "none",
    [],
    [
      ("page",[
          ],"A page at a nobleman's court.",[
      (assign,"$background_answer_2", cb2_page),
      (assign, reg3, "$character_gender"),
      (str_store_string,s11,"@As a {reg3?girl:boy} growing out of childhood,\
 you were sent to live in the court of one of the nobles of the land.\
 There, your first lessons were in humility, as you waited upon the lords and ladies of the household.\
 But from their chess games, their gossip, even the poetry of great deeds and courtly love, you quickly began to learn about the adult world of conflict\
 and competition. You also learned from the rough games of the other children, who battered at each other with sticks in imitation of their elders' swords."),
      (jump_to_menu,"mnu_start_character_3"),
    ]),
      ("apprentice",[
          ],"A craftsman's apprentice.",[
      (assign,"$background_answer_2", cb2_apprentice),
      (assign, reg3, "$character_gender"),
      (str_store_string,s11,"@As a {reg3?girl:boy} growing out of childhood,\
 you apprenticed with a local craftsman to learn a trade. After years of hard work and study under your\
 new master, he promoted you to journeyman and employed you as a fully paid craftsman for as long as\
 you wished to stay."),
      (jump_to_menu,"mnu_start_character_3"),
    ]),
      ("stockboy",[
          ],"A shop assistant.",[
      (assign,"$background_answer_2",cb2_merchants_helper),
      (assign, reg3, "$character_gender"),
      (str_store_string,s11,"@As a {reg3?girl:boy} growing out of childhood,\
 you apprenticed to a wealthy merchant, picking up the trade over years of working shops and driving caravans.\
 You soon became adept at the art of buying low, selling high, and leaving the customer thinking they'd\
 got the better deal."),
      (jump_to_menu,"mnu_start_character_3"),
    ]),
      ("urchin",[
          ],"A street urchin.",[
      (assign,"$background_answer_2",cb2_urchin),
      (assign, reg3, "$character_gender"),
      (str_store_string,s11,"@As a {reg3?girl:boy} growing out of childhood,\
 you took to the streets, doing whatever you must to survive.\
 Begging, thieving and working for gangs to earn your bread, you lived from day to day in this violent world,\
 always one step ahead of the law and those who wished you ill."),
      (jump_to_menu,"mnu_start_character_3"),
    ]),
      ("nomad",[
          ],"A steppe child.",[
      (assign,"$background_answer_2",cb2_steppe_child),
      (assign, reg3, "$character_gender"),
      (str_store_string,s11,"@As a {reg3?girl:boy} growing out of childhood,\
 you rode the great steppes on a horse of your own, learning the ways of the grass and the desert.\
 Although you sometimes went hungry, you became a skillful hunter and pathfinder in this trackless country.\
 Your body too started to harden with muscle as you grew into the life of a nomad {reg3?woman:man}."),
      (jump_to_menu,"mnu_start_character_3"),
    ]),
      ("go_back",[],"Go back.",
     [(jump_to_menu,"mnu_start_character_1"),
    ]),
    ]
  ),
  (
    "start_character_3",mnf_disable_all_keys,
    "{s11}^^ Then, as a young adult, life changed as it always does. You became...",
    "none",
    [(assign, reg3, "$character_gender"),],
    [
      ("squire",[(eq,"$character_gender",tf_male)],"A squire.",[
        (assign,"$background_answer_3",cb3_squire),
      (str_store_string,s14,"@{reg3?daughter:man}"),
      (str_store_string,s12,"@Though the distinction felt sudden to you,\
 somewhere along the way you had become a {reg3?woman:man}, and the whole world seemed to change around you.\
 When you were named squire to a noble at court, you practiced long hours with weapons,\
 learning how to deal out hard knocks and how to take them, too.\
 You were instructed in your obligations to your lord, and of your duties to those who might one day be your vassals.\
 But in addition to learning the chivalric ideal, you also learned about the less uplifting side\
 -- old warriors' stories of ruthless power politics, of betrayals and usurpations,\
 of men who used guile as well as valor to achieve their aims."),
      (jump_to_menu,"mnu_start_character_4"),
        ]),
      ("lady",[(eq,"$character_gender",tf_female)],"A lady-in-waiting.",[
        (assign,"$background_answer_3",cb3_lady_in_waiting),
      (str_store_string,s14,"@{reg3?daughter:man}"),
      (str_store_string,s13,"@{reg3?woman:man}"),
      (str_store_string,s12,"@Though the distinction felt sudden to you,\
 somewhere along the way you had become a {s13}, and the whole world seemed to change around you.\
 You joined the tightly-knit circle of women at court, ladies who all did proper ladylike things,\
 the wives and mistresses of noble men as well as maidens who had yet to find a husband.\
 However, even here you found politics at work as the ladies schemed for prominence and fought each other\
 bitterly to catch the eye of whatever unmarried man was in fashion at court.\
 You soon learned ways of turning these situations and goings-on to your advantage. With it came the\
 realisation that you yourself could wield great influence in the world, if only you applied yourself\
 with a little bit of subtlety."),
      (jump_to_menu,"mnu_start_character_4"),
        ]),
      ("troubadour",[],"A troubadour.",[
        (assign,"$background_answer_3",cb3_troubadour),
      (str_store_string,s14,"@{reg3?daughter:man}"),
      (str_store_string,s13,"@{reg3?woman:man}"),
      (str_store_string,s12,"@Though the distinction felt sudden to you,\
 somewhere along the way you had become a {s13}, and the whole world seemed to change around you.\
 You set out on your own with nothing except the instrument slung over your back and your own voice.\
 It was a poor existence, with many a hungry night when people failed to appreciate your play,\
 but you managed to survive on your music alone. As the years went by you became adept at playing the\
 drunken crowds in your taverns, and even better at talking anyone out of anything you wanted."),
      (jump_to_menu,"mnu_start_character_4"),
        ]),
      ("student",[],"A university student.",[
        (assign,"$background_answer_3",cb3_student),
      (str_store_string,s12,"@Though the distinction felt sudden to you,\
 somewhere along the way you had become a {reg3?woman:man}, and the whole world seemed to change around you.\
 You found yourself as a student in the university of one of the great cities,\
 where you studied theology, philosophy, and medicine.\
 But not all your lessons were learned in the lecture halls.\
 You may or may not have joined in with your fellows as they roamed the alleys in search of wine, women, and a good fight.\
 However, you certainly were able to observe how a broken jaw is set,\
 or how an angry townsman can be persuaded to set down his club and accept cash compensation for the destruction of his shop."),
      (jump_to_menu,"mnu_start_character_4"),
        ]),
      ("peddler",[],"A goods peddler.",[
        (assign,"$background_answer_3",cb3_peddler),
      (str_store_string,s14,"@{reg3?daughter:man}"),
      (str_store_string,s13,"@{reg3?woman:man}"),
      (str_store_string,s12,"@Though the distinction felt sudden to you,\
 somewhere along the way you had become a {s13}, and the whole world seemed to change around you.\
 Heeding the call of the open road, you travelled from village to village buying and selling what you could.\
 It was not a rich existence, but you became a master at haggling even the most miserly elders into\
 giving you a good price. Soon, you knew, you would be well-placed to start your own trading empire..."),
      (jump_to_menu,"mnu_start_character_4"),
        ]),
      ("craftsman",[],"A smith.",[
        (assign,"$background_answer_3", cb3_craftsman),
      (str_store_string,s14,"@{reg3?daughter:man}"),
      (str_store_string,s13,"@{reg3?woman:man}"),
      (str_store_string,s12,"@Though the distinction felt sudden to you,\
 somewhere along the way you had become a {s13}, and the whole world seemed to change around you.\
 You pursued a career as a smith, crafting items of function and beauty out of simple metal.\
 As time wore on you became a master of your trade, and fine work started to fetch fine prices.\
 With food in your belly and logs on your fire, you could take pride in your work and your growing reputation."),
      (jump_to_menu,"mnu_start_character_4"),
        ]),
      ("poacher",[],"A game poacher.",[
        (assign,"$background_answer_3", cb3_poacher),
      (str_store_string,s14,"@{reg3?daughter:man}"),
      (str_store_string,s13,"@{reg3?woman:man}"),
      (str_store_string,s12,"@Though the distinction felt sudden to you,\
 somewhere along the way you had become a {s13}, and the whole world seemed to change around you.\
 Dissatisfied with common men's desperate scrabble for coin, you took to your local lord's own forests\
 and decided to help yourself to its bounty, laws be damned. You hunted stags, boars and geese and sold\
 the precious meat under the table. You cut down trees right under the watchmen's noses and turned them into\
 firewood that warmed many freezing homes during winter. All for a few silvers, of course."),
      (jump_to_menu,"mnu_start_character_4"),
        ]),
      ("go_back",[],"Go back.",
       [(jump_to_menu,"mnu_start_character_2"),
        ]
       ),
    ]
  ),

  (
    "start_character_4",mnf_disable_all_keys,
    "{s12}^^But soon everything changed and you decided to strike out on your own as an adventurer. What made you take this decision was...",
    "none",
    [],
    [
      ("revenge",[],"Personal revenge.",[
        (assign,"$background_answer_4", cb4_revenge),
      (str_store_string,s13,"@Only you know exactly what caused you to give up your old life and become an adventurer.\
 Still, it was not a difficult choice to leave, with the rage burning brightly in your heart.\
 You want vengeance. You want justice. What was done to you cannot be undone,\
 and these debts can only be paid in blood..."),
        (jump_to_menu,"mnu_choose_skill"),
        ]),
      ("death",[],"The loss of a loved one.",[
        (assign,"$background_answer_4",cb4_loss),
      (str_store_string,s13,"@Only you know exactly what caused you to give up your old life and become an adventurer.\
 All you can say is that you couldn't bear to stay, not with the memories of those you loved so close and so\
 painful. Perhaps your new life will let you forget,\
 or honour the name that you can no longer bear to speak..."),
        (jump_to_menu,"mnu_choose_skill"),
        ]),
      ("wanderlust",[],"Wanderlust.",[
        (assign,"$background_answer_4",cb4_wanderlust),
      (str_store_string,s13,"@Only you know exactly what caused you to give up your old life and become an adventurer.\
 You're not even sure when your home became a prison, when the familiar became mundane, but your dreams of\
 wandering have taken over your life. Whether you yearn for some faraway place or merely for the open road and the\
 freedom to travel, you could no longer bear to stay in the same place. You simply went and never looked back..."),
        (jump_to_menu,"mnu_choose_skill"),
        ]),
      ("disown",[],"Being forced out of your home.",[
        (assign,"$background_answer_4",cb4_disown),
      (str_store_string,s13,"@Only you know exactly what caused you to give up your old life and become an adventurer.\
 However, you know you cannot go back. There's nothing to go back to. Whatever home you may have had is gone\
 now, and you must face the fact that you're out in the wide wide world. Alone to sink or swim..."),
        (jump_to_menu,"mnu_choose_skill"),
        ]),
     ("greed",[],"Lust for money and power.",[
        (assign,"$background_answer_4",cb4_greed),
      (str_store_string,s13,"@Only you know exactly what caused you to give up your old life and become an adventurer.\
 To everyone else, it's clear that you're now motivated solely by personal gain.\
 You want to be rich, powerful, respected, feared.\
 You want to be the one whom others hurry to obey.\
 You want people to know your name, and tremble whenever it is spoken.\
 You want everything, and you won't let anyone stop you from having it..."),
        (jump_to_menu,"mnu_choose_skill"),
        ]),
      ("go_back",[],"Go back.",
       [(jump_to_menu,"mnu_start_character_3"),
        ]
       ),
    ]
  ),

  ("start_phase_2",mnf_disable_all_keys,
    "You hear about Japan, a land torn between rival daimyo battling each other for supremacy,\
 a haven for samurai and ronin, cutthroats and adventurers, all willing to risk their lives in pursuit of fortune, power, or glory...\
 In this land which holds great dangers and even greater opportunities, you believe you may leave your past behind and start a new life.\
 You feel that finally, you hold the key of your destiny in your hands, free to choose as you will,\
 and that whatever course you take, great adventures will await you. Drawn by the stories you hear about Japan and its provinces, you...",
    "none",
    [],
    [
      ("king_continue",[(eq, "$g_sandbox_start_done", 3),],"ride to your capital and take up your rule.",
       [
         (assign, "$g_sandbox_start_done", 0),
         (change_screen_map),
       ]),

      ("town_1",[(eq, "$current_startup_quest_phase", 0),(neq, "$g_sandbox_start_done", 3),],"join a caravan to Praven, in the Kingdom of Swadia.",
       [
         (assign, "$current_town", "p_town_1"),
         (assign, "$g_starting_town", "$current_town"),
            (call_script, "script_player_arrived"),
            (party_set_morale, "p_main_party", 100),
            (assign, ":max_dist", 0),
            (party_get_position, pos1, "$current_town"),
            (try_for_range, ":unused", 0, 10),
                (map_get_random_position_around_position, pos0, pos1, 2),
                (get_distance_between_positions, ":dist", pos0, pos1),
                (ge, ":dist", ":max_dist"),
                (assign, ":max_dist", ":dist"),
                (copy_position, pos2, pos0),
            (try_end),  
            (party_set_position, "p_main_party", pos2), 
            (change_screen_map),
		 # (jump_to_menu, "mnu_start_phase_2_5"),
#         (party_relocate_near_party, "p_main_party", "$g_starting_town", 2),
#         (change_screen_return),
       ]),
       
      ("town_2",[(eq, "$current_startup_quest_phase", 0),(neq, "$g_sandbox_start_done", 3),],"join a caravan to Reyvadin, in the Kingdom of the Vaegirs.",
       [
         (assign, "$current_town", "p_town_2"),
         (assign, "$g_starting_town", "$current_town"),
            (call_script, "script_player_arrived"),
            (party_set_morale, "p_main_party", 100),
            (assign, ":max_dist", 0),
            (party_get_position, pos1, "$current_town"),
            (try_for_range, ":unused", 0, 10),
                (map_get_random_position_around_position, pos0, pos1, 2),
                (get_distance_between_positions, ":dist", pos0, pos1),
                (ge, ":dist", ":max_dist"),
                (assign, ":max_dist", ":dist"),
                (copy_position, pos2, pos0),
            (try_end),  
            (party_set_position, "p_main_party", pos2), 
            (change_screen_map),
		 # (jump_to_menu, "mnu_start_phase_2_5"),
#         (party_relocate_near_party, "p_main_party", "$g_starting_town", 2),
#         (change_screen_return),
       ]),
       
      ("town_3",[(eq, "$current_startup_quest_phase", 0),(neq, "$g_sandbox_start_done", 3),],"join a caravan to Tulga, in the Khergit Khanate.",
       [
         (assign, "$current_town", "p_town_3"),
         (assign, "$g_starting_town", "$current_town"),
            (call_script, "script_player_arrived"),
            (party_set_morale, "p_main_party", 100),
            (assign, ":max_dist", 0),
            (party_get_position, pos1, "$current_town"),
            (try_for_range, ":unused", 0, 10),
                (map_get_random_position_around_position, pos0, pos1, 2),
                (get_distance_between_positions, ":dist", pos0, pos1),
                (ge, ":dist", ":max_dist"),
                (assign, ":max_dist", ":dist"),
                (copy_position, pos2, pos0),
            (try_end),  
            (party_set_position, "p_main_party", pos2), 
            (change_screen_map),
		 # (jump_to_menu, "mnu_start_phase_2_5"),
#         (party_relocate_near_party, "p_main_party", "$g_starting_town", 2),
#         (change_screen_return),
       ]),
       
      ("town_4",[(eq, "$current_startup_quest_phase", 0),(neq, "$g_sandbox_start_done", 3),],"take a ship to Sargoth, in the Kingdom of the Nords.",
       [
         (assign, "$current_town", "p_town_4"),
         (assign, "$g_starting_town", "$current_town"),
            (call_script, "script_player_arrived"),
            (party_set_morale, "p_main_party", 100),
            (assign, ":max_dist", 0),
            (party_get_position, pos1, "$current_town"),
            (try_for_range, ":unused", 0, 10),
                (map_get_random_position_around_position, pos0, pos1, 2),
                (get_distance_between_positions, ":dist", pos0, pos1),
                (ge, ":dist", ":max_dist"),
                (assign, ":max_dist", ":dist"),
                (copy_position, pos2, pos0),
            (try_end),  
            (party_set_position, "p_main_party", pos2), 
            (change_screen_map),
		 # (jump_to_menu, "mnu_start_phase_2_5"),
#         (party_relocate_near_party, "p_main_party", "$g_starting_town", 2),
#         (change_screen_return),
       ]),
       
      ("town_5",[(eq, "$current_startup_quest_phase", 0),(neq, "$g_sandbox_start_done", 3),],"take a ship to Jelkala, in the Kingdom of the Rhodoks.",
       [
         (assign, "$current_town", "p_town_5"),
         (assign, "$g_starting_town", "$current_town"),
            (call_script, "script_player_arrived"),
            (party_set_morale, "p_main_party", 100),
            (assign, ":max_dist", 0),
            (party_get_position, pos1, "$current_town"),
            (try_for_range, ":unused", 0, 10),
                (map_get_random_position_around_position, pos0, pos1, 2),
                (get_distance_between_positions, ":dist", pos0, pos1),
                (ge, ":dist", ":max_dist"),
                (assign, ":max_dist", ":dist"),
                (copy_position, pos2, pos0),
            (try_end),  
            (party_set_position, "p_main_party", pos2), 
            (change_screen_map),
		 # (jump_to_menu, "mnu_start_phase_2_5"),
#         (party_relocate_near_party, "p_main_party", "$g_starting_town", 2),
#         (change_screen_return),
       ]),
       
       ("town_6",[(eq, "$current_startup_quest_phase", 0),(neq, "$g_sandbox_start_done", 3),],"take a ship to Jelkala, in the Kingdom of the Rhodoks.",
       [
         (assign, "$current_town", "p_town_6"),
         (assign, "$g_starting_town", "$current_town"),
            (call_script, "script_player_arrived"),
            (party_set_morale, "p_main_party", 100),
            (assign, ":max_dist", 0),
            (party_get_position, pos1, "$current_town"),
            (try_for_range, ":unused", 0, 10),
                (map_get_random_position_around_position, pos0, pos1, 2),
                (get_distance_between_positions, ":dist", pos0, pos1),
                (ge, ":dist", ":max_dist"),
                (assign, ":max_dist", ":dist"),
                (copy_position, pos2, pos0),
            (try_end),  
            (party_set_position, "p_main_party", pos2), 
            (change_screen_map),
		 # (jump_to_menu, "mnu_start_phase_2_5"),
#         (party_relocate_near_party, "p_main_party", "$g_starting_town", 2),
#         (change_screen_return),
       ]),

	   
      ("tutorial_cheat",[(eq,1,0)],"{!}CHEAT!",
       [
         (change_screen_return),
         (assign, "$cheat_mode", 1),
         (set_show_messages, 0),
		 (add_xp_to_troop, 15000, "trp_player"),
         (troop_raise_skill, "trp_player", skl_leadership, 7),
         (troop_raise_skill, "trp_player", skl_prisoner_management, 5),
         (troop_raise_skill, "trp_player", skl_inventory_management, 10),
         (party_add_members, "p_main_party", "trp_gekokujo_takeda_hatamoto_cavalry", 20),
         (party_add_members, "p_main_party", "trp_gekokujo_tokugawa_hatamoto_gunner", 20),
         (troop_add_item, "trp_player","itm_gekokujo_okegawa_long_1",0),
         (troop_add_item, "trp_player","itm_gekokujo_suji_o_1",0),
         
         (troop_add_item, "trp_player","itm_gekokujo_naginata_1",0),
         (troop_add_item, "trp_player","itm_gekokujo_nodachi_1",0),
         (troop_add_item, "trp_player","itm_gekokujo_katana_1",0),
         (troop_add_item, "trp_player","itm_gekokujo_wakizashi_2",0),
         
         (set_show_messages, 1),

         (try_for_range, ":cur_place", scenes_begin, scenes_end),
           (scene_set_slot, ":cur_place", slot_scene_visited, 1),
         (try_end),
         
         (call_script, "script_get_player_party_morale_values"),
         (party_set_morale, "p_main_party", reg0),
       ]
	   ),
    ]
  ),
 


 
  (
    "start_game_3",mnf_disable_all_keys,
    "Choose your scenario:",
    "none",
    [
      (assign, "$g_custom_battle_scenario", 0),
      (assign, "$g_custom_battle_scenario", "$g_custom_battle_scenario"),
##      #Default banners
##      (troop_set_slot, "trp_banner_background_color_array", 126, 0xFF212221),
##      (troop_set_slot, "trp_banner_background_color_array", 127, 0xFF212221),
##      (troop_set_slot, "trp_banner_background_color_array", 128, 0xFF2E3B10),
##      (troop_set_slot, "trp_banner_background_color_array", 129, 0xFF425D7B),
##      (troop_set_slot, "trp_banner_background_color_array", 130, 0xFF394608),
      ],
    [
##      ("custom_battle_scenario_1",[], "Skirmish 1",
##       [
##           (assign, "$g_custom_battle_scenario", 0),
##           (jump_to_menu, "mnu_custom_battle_2"),
##
##        ]
##       ),
####      ("custom_battle_scenario_2",[],"Siege Attack 1",
####       [
####           (assign, "$g_custom_battle_scenario", 1),
####           (jump_to_menu, "mnu_custom_battle_2"),
####
####        ]
####       ),
##      ("custom_battle_scenario_3",[],"Skirmish 2",
##       [
##           (assign, "$g_custom_battle_scenario", 1),
##           (jump_to_menu, "mnu_custom_battle_2"),
##
##        ]
##       ),
##       ("custom_battle_scenario_4",[],"Siege Defense",
##       [
##           (assign, "$g_custom_battle_scenario", 2),
##           (jump_to_menu, "mnu_custom_battle_2"),
##        ]
##       ),
##       ("custom_battle_scenario_5",[],"Skirmish 3",
##       [
##           (assign, "$g_custom_battle_scenario", 3),
##           (jump_to_menu, "mnu_custom_battle_2"),
##        ]
##       ),
##      ("custom_battle_scenario_6",[],"Siege Attack",
##       [
##           (assign, "$g_custom_battle_scenario", 4),
##           (jump_to_menu, "mnu_custom_battle_2"),
##
##        ]
##       ),
      ("go_back",[],"Go back",
       [(change_screen_quit), 
        ]
		),
    ]
  ),
##  ("start_game_3",mnf_disable_all_keys,
##    "Choose your scenario:",
##    "none",
##    [
##      (assign, "$g_custom_battle_scenario", 0),
##      (assign, "$g_custom_battle_scenario", "$g_custom_battle_scenario"),
####      #Default banners
####      (troop_set_slot, "trp_banner_background_color_array", 126, 0xFF212221),
####      (troop_set_slot, "trp_banner_background_color_array", 127, 0xFF212221),
####      (troop_set_slot, "trp_banner_background_color_array", 128, 0xFF2E3B10),
####      (troop_set_slot, "trp_banner_background_color_array", 129, 0xFF425D7B),
####      (troop_set_slot, "trp_banner_background_color_array", 130, 0xFF394608),
##      ],
##    [
####      ("custom_battle_scenario_1",[], "Skirmish 1",
####       [
####           (assign, "$g_custom_battle_scenario", 0),
####           (jump_to_menu, "mnu_custom_battle_2"),
####
####        ]
####       ),
######      ("custom_battle_scenario_2",[],"Siege Attack 1",
######       [
######           (assign, "$g_custom_battle_scenario", 1),
######           (jump_to_menu, "mnu_custom_battle_2"),
######
######        ]
######       ),
####      ("custom_battle_scenario_3",[],"Skirmish 2",
####       [
####           (assign, "$g_custom_battle_scenario", 1),
####           (jump_to_menu, "mnu_custom_battle_2"),
####
####        ]
####       ),
####       ("custom_battle_scenario_4",[],"Siege Defense",
####       [
####           (assign, "$g_custom_battle_scenario", 2),
####           (jump_to_menu, "mnu_custom_battle_2"),
####        ]
####       ),
####       ("custom_battle_scenario_5",[],"Skirmish 3",
####       [
####           (assign, "$g_custom_battle_scenario", 3),
####           (jump_to_menu, "mnu_custom_battle_2"),
####        ]
####       ),
####      ("custom_battle_scenario_6",[],"Siege Attack",
####       [
####           (assign, "$g_custom_battle_scenario", 4),
####           (jump_to_menu, "mnu_custom_battle_2"),
####
####        ]
####       ),
##      ("go_back",[],"Go back",
##       [(change_screen_quit),
##        ]
##       ),
##    ]
##  ),

  (
    "tutorial",mnf_disable_all_keys,
    "You approach a field where the locals are training with weapons. You can practice here to improve your combat skills.",
    "none",
    [
      (try_begin),
        (eq, "$g_tutorial_entered", 1),
        (change_screen_quit),
      (else_try),
        (set_passage_menu, "mnu_tutorial"),
##        (try_begin),
##          (eq, "$tutorial_1_finished", 1),
##          (str_store_string, s1, "str_finished"),
##        (else_try),
##          (str_store_string, s1, "str_empty_string"),
##        (try_end),
##        (try_begin),
##          (eq, "$tutorial_2_finished", 1),
##          (str_store_string, s2, "str_finished"),
##        (else_try),
##          (str_store_string, s2, "str_empty_string"),
##        (try_end),
##        (try_begin),
##          (eq, "$tutorial_3_finished", 1),
##          (str_store_string, s3, "str_finished"),
##        (else_try),
##          (str_store_string, s3, "str_empty_string"),
##        (try_end),
##        (try_begin),
##          (eq, "$tutorial_4_finished", 1),
##          (str_store_string, s4, "str_finished"),
##        (else_try),
##          (str_store_string, s4, "str_empty_string"),
##        (try_end),
##        (try_begin),
##          (eq, "$tutorial_5_finished", 1),
##          (str_store_string, s5, "str_finished"),
##        (else_try),
##          (str_store_string, s5, "str_empty_string"),
##        (try_end),
        (assign, "$g_tutorial_entered", 1),
      (try_end),
    ],
    [
##      ("tutorial_1",
##      [(eq,1,0),],
##      "Tutorial #1: Basic movement and weapon selection. {s1}",
##      [
##        #(modify_visitors_at_site,"scn_tutorial_1"),(reset_visitors,0),
####           (set_jump_mission,"mt_tutorial_1"),
####           (jump_to_scene,"scn_tutorial_1"),(change_screen_mission)]),
##      ]),
##      
##      ("tutorial_2",[(eq,1,0),],"Tutorial #2: Fighting with a shield. {s2}",[
####           (modify_visitors_at_site,"scn_tutorial_2"),(reset_visitors,0),
####           (set_visitor,1,"trp_tutorial_maceman"),
####           (set_visitor,2,"trp_tutorial_archer"),
####           (set_jump_mission,"mt_tutorial_2"),
####           (jump_to_scene,"scn_tutorial_2"),(change_screen_mission)]),
##           (modify_visitors_at_site,"scn_tutorial_training_ground"),
##           (reset_visitors, 0),
##           (set_player_troop, "trp_player"),
##           (set_visitor,0,"trp_player"),
##           (set_jump_mission,"mt_ai_training"),
##           (jump_to_scene,"scn_tutorial_training_ground"),
##           (change_screen_mission)]),
##
##      ("tutorial_3",[(eq,1,0),],"Tutorial #3: Fighting without a shield. {s3}",[
##           (modify_visitors_at_site,"scn_tutorial_3"),(reset_visitors,0),
##           (set_visitor,1,"trp_tutorial_maceman"),
##           (set_visitor,2,"trp_tutorial_swordsman"),
##           (set_jump_mission,"mt_tutorial_3"),
##           (jump_to_scene,"scn_tutorial_3"),(change_screen_mission)]),
##      ("tutorial_3b",[(eq,0,1)],"Tutorial 3 b",[(try_begin),
##                                                  (ge, "$tutorial_3_state", 12),
##                                                  (modify_visitors_at_site,"scn_tutorial_3"),(reset_visitors,0),
##                                                  (set_visitor,1,"trp_tutorial_maceman"),
##                                                  (set_visitor,2,"trp_tutorial_swordsman"),
##                                                  (set_jump_mission,"mt_tutorial_3_2"),
##                                                  (jump_to_scene,"scn_tutorial_3"),
##                                                  (change_screen_mission),
##                                                (else_try),
##                                                  (display_message,"str_door_locked",0xFFFFAAAA),
##                                                (try_end)], "Next level"),
##      ("tutorial_4",[(eq,1,0),],"Tutorial #4: Riding a horse. {s4}",[
##           (modify_visitors_at_site,"scn_tutorial_training_ground"),
##           (reset_visitors, 0),
##           (set_player_troop, "trp_player"),
##           (assign, "$g_player_troop", "trp_player"),
##           (troop_raise_attribute, "$g_player_troop", ca_strength, 12),
##           (troop_raise_attribute, "$g_player_troop", ca_agility, 9),
##           (troop_raise_attribute, "$g_player_troop", ca_charisma, 5),
##           (troop_raise_skill, "$g_player_troop", skl_shield, 3),
##           (troop_raise_skill, "$g_player_troop", skl_athletics, 2),
##           (troop_raise_skill, "$g_player_troop", skl_riding, 3),
##           (troop_raise_skill, "$g_player_troop", skl_power_strike, 1),
##           (troop_raise_skill, "$g_player_troop", skl_power_draw, 5),
##           (troop_raise_skill, "$g_player_troop", skl_weapon_master, 4),
##           (troop_raise_skill, "$g_player_troop", skl_ironflesh, 1),
##           (troop_raise_skill, "$g_player_troop", skl_horse_archery, 6),
##           (troop_raise_proficiency_linear, "$g_player_troop", wpt_one_handed_weapon, 70),
##           (troop_raise_proficiency_linear, "$g_player_troop", wpt_two_handed_weapon, 70),
##           (troop_raise_proficiency_linear, "$g_player_troop", wpt_polearm, 70),
##           (troop_raise_proficiency_linear, "$g_player_troop", wpt_crossbow, 70),
##           (troop_raise_proficiency_linear, "$g_player_troop", wpt_throwing, 70),
##     
##        (troop_clear_inventory, "$g_player_troop"),
##        (troop_add_item, "$g_player_troop","itm_leather_jerkin",0),
##        (troop_add_item, "$g_player_troop","itm_leather_boots",0),
##        (troop_add_item, "$g_player_troop","itm_practice_sword",0),
##        (troop_add_item, "$g_player_troop","itm_quarter_staff",0),
##        (troop_equip_items, "$g_player_troop"),
##        (set_visitor,0,"trp_player"),
##        (set_visitor,32,"trp_tutorial_fighter_1"),
##        (set_visitor,33,"trp_tutorial_fighter_2"),
##        (set_visitor,34,"trp_tutorial_fighter_3"),
##        (set_visitor,35,"trp_tutorial_fighter_4"),
##        (set_visitor,40,"trp_tutorial_master_archer"),
##        (set_visitor,41,"trp_tutorial_archer_1"),
##        (set_visitor,42,"trp_tutorial_archer_1"),
##        (set_visitor,60,"trp_tutorial_master_horseman"),
##        (set_visitor,61,"trp_tutorial_rider_1"),
##        (set_visitor,62,"trp_tutorial_rider_1"),
##        (set_visitor,63,"trp_tutorial_rider_2"),
##        (set_visitor,64,"trp_tutorial_rider_2"),
##        (set_jump_mission,"mt_tutorial_training_ground"),
##        (jump_to_scene,"scn_tutorial_training_ground"),
##        (change_screen_mission),
##      ]),
##      
##      ("tutorial_5",
##      [
##        (eq,1,0),
##      ],
##      "Tutorial #5: Commanding a band of soldiers. {s5}",
##      [
##        (modify_visitors_at_site,"scn_tutorial_5"),(reset_visitors,0),
##        (set_visitor,0,"trp_player"),
##        (set_visitor,1,"trp_vaegir_infantry"),
##        (set_visitor,2,"trp_vaegir_infantry"),
##        (set_visitor,3,"trp_vaegir_infantry"),
##        (set_visitor,4,"trp_vaegir_infantry"),
##        (set_jump_mission,"mt_tutorial_5"),
##        (jump_to_scene,"scn_tutorial_5"),
##        (change_screen_mission),
##      ]),
##      
##      ("tutorial_edit_custom_battle_scenes",
##      [(eq,1,0),],
##      "(NO TRANSLATE) tutorial_edit_custom_battle_scenes",
##      [
##        (jump_to_menu,"mnu_custom_battle_scene"),        
##      ]),

      ("continue",[],"Continue...",
      [
        (modify_visitors_at_site,"scn_tutorial_training_ground"),
        (reset_visitors, 0),
        (set_player_troop, "trp_player"),
        (assign, "$g_player_troop", "trp_player"),
        (troop_raise_attribute, "$g_player_troop", ca_strength, 12),
        (troop_raise_attribute, "$g_player_troop", ca_agility, 9),
        (troop_raise_attribute, "$g_player_troop", ca_charisma, 5),
        (troop_raise_skill, "$g_player_troop", skl_shield, 3),
        (troop_raise_skill, "$g_player_troop", skl_athletics, 2),
        (troop_raise_skill, "$g_player_troop", skl_riding, 3),
        (troop_raise_skill, "$g_player_troop", skl_power_strike, 1),
        (troop_raise_skill, "$g_player_troop", skl_power_draw, 5),
        (troop_raise_skill, "$g_player_troop", skl_weapon_master, 4),
        (troop_raise_skill, "$g_player_troop", skl_ironflesh, 1),
        (troop_raise_skill, "$g_player_troop", skl_horse_archery, 6),
        (troop_raise_proficiency_linear, "$g_player_troop", wpt_one_handed_weapon, 70),
        (troop_raise_proficiency_linear, "$g_player_troop", wpt_two_handed_weapon, 70),
        (troop_raise_proficiency_linear, "$g_player_troop", wpt_polearm, 70),
        (troop_raise_proficiency_linear, "$g_player_troop", wpt_firearm, 70),
        (troop_raise_proficiency_linear, "$g_player_troop", wpt_throwing, 70),
     
        (troop_clear_inventory, "$g_player_troop"),
        (troop_add_item, "$g_player_troop","itm_gekokujo_hakama_5",0),
        (troop_add_item, "$g_player_troop","itm_gekokujo_sandal_1",0),
        (troop_add_item, "$g_player_troop","itm_gekokujo_practice_katana",0),
        (troop_add_item, "$g_player_troop","itm_gekokujo_practice_jo",0),
        (troop_equip_items, "$g_player_troop"),
        (set_visitor,0,"trp_player"),
        (set_visitor,32,"trp_tutorial_fighter_1"),
        (set_visitor,33,"trp_tutorial_fighter_2"),
        (set_visitor,34,"trp_tutorial_fighter_3"),
        (set_visitor,35,"trp_tutorial_fighter_4"),
        (set_visitor,40,"trp_tutorial_master_archer"),
        (set_visitor,41,"trp_tutorial_archer_1"),
        (set_visitor,42,"trp_tutorial_archer_1"),
        (set_visitor,60,"trp_tutorial_master_horseman"),
        (set_visitor,61,"trp_tutorial_rider_1"),
        (set_visitor,62,"trp_tutorial_rider_1"),
        (set_visitor,63,"trp_tutorial_rider_2"),
        (set_visitor,64,"trp_tutorial_rider_2"),
        (set_jump_mission,"mt_tutorial_training_ground"),
        (jump_to_scene,"scn_tutorial_training_ground"),
        (change_screen_mission),
        ]),

      ("go_back_dot",
      [],
      "Go back.",
       [
         (change_screen_quit),
       ]),
    ]
  ),
  
(
    "choose_skill",mnf_disable_all_keys,
    "{s13}", 
    "none",
    [(assign,"$current_string_reg",10),
	 (assign, ":difficulty", 0),
	 
	 (try_begin),
		(eq, "$character_gender", tf_female),
		(str_store_string, s14, "str_woman"),
		(val_add, ":difficulty", 1),
	 (else_try),	
		(str_store_string, s14, "str_man"),
	 (try_end),
	
	 (try_begin),
        (eq,"$background_type",cb_noble),
		(str_store_string, s15, "str_noble"),
		(val_sub, ":difficulty", 1),
	 (else_try),
		(str_store_string, s15, "str_common"),
	 (try_end),
	 
	 (try_begin),
		(eq, ":difficulty", -1),
		(str_store_string, s16, "str_may_find_that_you_are_able_to_take_your_place_among_calradias_great_lords_relatively_quickly"),
	 (else_try),
		(eq, ":difficulty", 0),
		(str_store_string, s16, "str_may_face_some_difficulties_establishing_yourself_as_an_equal_among_calradias_great_lords"),
	 (else_try),
		(eq, ":difficulty", 1),
		(str_store_string, s16, "str_may_face_great_difficulties_establishing_yourself_as_an_equal_among_calradias_great_lords"),
	 (try_end),
	],
    [
      ("begin_adventuring",[],"Become an adventurer and ride to your destiny.",[
           (set_show_messages, 0),
           (try_begin),
             (eq,"$character_gender",0),
             (troop_raise_attribute, "trp_player",ca_strength,1),
             (troop_raise_attribute, "trp_player",ca_charisma,1),
           (else_try),
             (troop_raise_attribute, "trp_player",ca_agility,1),
             (troop_raise_attribute, "trp_player",ca_intelligence,1),
           (try_end),

           (troop_raise_attribute, "trp_player",ca_strength,1),
           (troop_raise_attribute, "trp_player",ca_agility,1),
           (troop_raise_attribute, "trp_player",ca_charisma,1),
           
           (troop_raise_skill, "trp_player","skl_leadership",1),
           (troop_raise_skill, "trp_player","skl_riding",1),


      (try_begin),
        (eq,"$background_type",cb_noble),
        (eq,"$character_gender",tf_male),
        (troop_raise_attribute, "trp_player",ca_intelligence,1),
        (troop_raise_attribute, "trp_player",ca_charisma,2),
        (troop_raise_skill, "trp_player",skl_weapon_master,1),
        (troop_raise_skill, "trp_player",skl_power_draw,1),
        (troop_raise_skill, "trp_player",skl_riding,1),
        (troop_raise_skill, "trp_player",skl_tactics,1),
        (troop_raise_skill, "trp_player",skl_leadership,1),
        (troop_raise_proficiency, "trp_player",wpt_two_handed_weapon,10),
        (troop_raise_proficiency, "trp_player",wpt_archery,10),
        (troop_raise_proficiency, "trp_player",wpt_polearm,10),

        (troop_add_item, "trp_player","itm_gekokujo_tachi_1",imod_tempered),
		
		##gekokujo 3.0 change starting renown for freelancer samurai/ashigaru dichotomy
        (troop_set_slot, "trp_player", slot_troop_renown, 100),
        #(troop_set_slot, "trp_player", slot_troop_renown, 150), #take-back
		
        (call_script, "script_change_player_honor", 3),
		
        (troop_add_gold, "trp_player", 100),
      (else_try),
        (eq,"$background_type",cb_noble),
        (eq,"$character_gender",tf_female),
        (troop_raise_attribute, "trp_player",ca_intelligence,2),
        (troop_raise_attribute, "trp_player",ca_charisma,1),
        (troop_raise_skill, "trp_player",skl_wound_treatment,1),
        (troop_raise_skill, "trp_player",skl_first_aid,1),
        (troop_raise_skill, "trp_player",skl_leadership,1),
        (troop_raise_skill, "trp_player",skl_trade,1),
        (troop_raise_skill, "trp_player",skl_persuasion,1),
        (troop_raise_proficiency, "trp_player",wpt_archery,20),

		#gekokujo 3.0 change starting renown for freelancer samurai/ashigaru dichotomy
        #(troop_set_slot, "trp_player", slot_troop_renown, 50),
        (troop_set_slot, "trp_player", slot_troop_renown, 80),
		
		
        (troop_add_item, "trp_player","itm_gekokujo_tachi_1",imod_tempered),
           
        (troop_add_gold, "trp_player", 100),
      (else_try),
        (eq,"$background_type",cb_merchant),
        (troop_raise_attribute, "trp_player",ca_intelligence,2),
        (troop_raise_attribute, "trp_player",ca_charisma,1),
        (troop_raise_skill, "trp_player",skl_riding,1),
        (troop_raise_skill, "trp_player",skl_leadership,1),
        (troop_raise_skill, "trp_player",skl_trade,2),
        (troop_raise_skill, "trp_player",skl_inventory_management,1),
        (troop_raise_proficiency, "trp_player",wpt_two_handed_weapon,10),
           
        (troop_add_gold, "trp_player", 250),
        (troop_set_slot, "trp_player", slot_troop_renown, 20),
      (else_try),
        (eq,"$background_type",cb_guard),
        (troop_raise_attribute, "trp_player",ca_strength,1),
        (troop_raise_attribute, "trp_player",ca_agility,1),
        (troop_raise_attribute, "trp_player",ca_charisma,1),
        (troop_raise_skill, "trp_player","skl_ironflesh",1),
        (troop_raise_skill, "trp_player","skl_power_strike",1),
        (troop_raise_skill, "trp_player","skl_weapon_master",1),
        (troop_raise_skill, "trp_player","skl_leadership",1),
        (troop_raise_skill, "trp_player","skl_trainer",1),
        (troop_raise_proficiency, "trp_player",wpt_one_handed_weapon,10),
        (troop_raise_proficiency, "trp_player",wpt_two_handed_weapon,15),
        (troop_raise_proficiency, "trp_player",wpt_polearm,20),
        (troop_raise_proficiency, "trp_player",wpt_throwing,10),
        (troop_add_item, "trp_player","itm_gekokujo_yari_bamboo_1",imod_cracked),
		
        (troop_add_gold, "trp_player", 50),
        (troop_set_slot, "trp_player", slot_troop_renown, 10),
      (else_try),
        (eq,"$background_type",cb_forester),
        (troop_raise_attribute, "trp_player",ca_strength,1),
        (troop_raise_attribute, "trp_player",ca_agility,2),
        (troop_raise_skill, "trp_player","skl_power_draw",1),
        (troop_raise_skill, "trp_player","skl_tracking",1),
        (troop_raise_skill, "trp_player","skl_pathfinding",1),
        #(troop_raise_skill, "trp_player","skl_spotting",1),
        (troop_raise_skill, "trp_player","skl_shield",1), #shield is foraging now
        (troop_raise_skill, "trp_player","skl_athletics",1),
        (troop_raise_proficiency, "trp_player",wpt_two_handed_weapon,10),
        (troop_raise_proficiency, "trp_player",wpt_archery,30),
		
        (troop_add_gold, "trp_player", 30),
      (else_try),
        (eq,"$background_type",cb_nomad),
        (eq,"$character_gender",tf_male),
        (troop_raise_attribute, "trp_player",ca_strength,1),
        (troop_raise_attribute, "trp_player",ca_agility,1),
        (troop_raise_attribute, "trp_player",ca_intelligence,1),
        (troop_raise_skill, "trp_player","skl_power_draw",1),
        (troop_raise_skill, "trp_player","skl_horse_archery",1),
        (troop_raise_skill, "trp_player","skl_pathfinding",1),
        (troop_raise_skill, "trp_player","skl_riding",2),
        (troop_raise_proficiency, "trp_player",wpt_two_handed_weapon,10),
        (troop_raise_proficiency, "trp_player",wpt_archery,30),
        (troop_raise_proficiency, "trp_player",wpt_polearm,10),
        (troop_add_item, "trp_player","itm_gekokujo_wakizashi_2",imod_rusty),
        (troop_add_gold, "trp_player", 15),
		
		#gekokujo 3.0 change starting renown for freelancer samurai/ashigaru dichotomy
        #(troop_set_slot, "trp_player", slot_troop_renown, 25),
        (troop_set_slot, "trp_player", slot_troop_renown, 75),		
      (else_try),
        (eq,"$background_type",cb_nomad),
        (eq,"$character_gender",tf_female),
        (troop_raise_attribute, "trp_player",ca_strength,1),
        (troop_raise_attribute, "trp_player",ca_agility,1),
        (troop_raise_attribute, "trp_player",ca_intelligence,1),
        (troop_raise_skill, "trp_player","skl_wound_treatment",1),
        (troop_raise_skill, "trp_player","skl_first_aid",1),
        (troop_raise_skill, "trp_player","skl_surgery",1),
        (troop_raise_skill, "trp_player","skl_pathfinding",1),
        (troop_raise_skill, "trp_player","skl_riding",1),
        (troop_raise_proficiency, "trp_player",wpt_two_handed_weapon,5),
        (troop_raise_proficiency, "trp_player",wpt_archery,15),
        (troop_raise_proficiency, "trp_player",wpt_polearm,10),
        (troop_add_item, "trp_player","itm_gekokujo_naginata_1",imod_cracked),
		
        (troop_add_gold, "trp_player", 20),
      (else_try),
        (eq,"$background_type",cb_thief),
        (troop_raise_attribute, "trp_player",ca_agility,3),
        (troop_raise_skill, "trp_player","skl_athletics",2),
        (troop_raise_skill, "trp_player","skl_power_throw",1),
        (troop_raise_skill, "trp_player","skl_inventory_management",1),
        (troop_raise_skill, "trp_player","skl_looting",1),
        (troop_raise_proficiency, "trp_player",wpt_one_handed_weapon,20),
        (troop_raise_proficiency, "trp_player",wpt_throwing,20),
        (troop_add_item, "trp_player","itm_gekokujo_shuriken",0),
		
        (troop_add_gold, "trp_player", 25),
      (try_end),

    (try_begin),
        (eq,"$background_answer_2",cb2_page),
        (troop_raise_attribute, "trp_player",ca_charisma,1),
        (troop_raise_attribute, "trp_player",ca_strength,1),
        (troop_raise_skill, "trp_player","skl_power_strike",1),
        (troop_raise_skill, "trp_player","skl_persuasion",1),
        (troop_raise_proficiency, "trp_player",wpt_one_handed_weapon,15),
        (troop_raise_proficiency, "trp_player",wpt_polearm,5),
    (else_try),
        (eq,"$background_answer_2",cb2_apprentice),
        (troop_raise_attribute, "trp_player",ca_intelligence,1),
        (troop_raise_attribute, "trp_player",ca_strength,1),
        (troop_raise_skill, "trp_player","skl_engineer",1),
        (troop_raise_skill, "trp_player","skl_trade",1),
    (else_try),
        (eq,"$background_answer_2",cb2_urchin),
        (troop_raise_attribute, "trp_player",ca_agility,1),
        (troop_raise_attribute, "trp_player",ca_intelligence,1),
        (troop_raise_skill, "trp_player","skl_spotting",1),
        (troop_raise_skill, "trp_player","skl_looting",1),
        (troop_raise_proficiency, "trp_player",wpt_one_handed_weapon,15),
        (troop_raise_proficiency, "trp_player",wpt_throwing,5),
    (else_try),
        (eq,"$background_answer_2",cb2_steppe_child),
        (troop_raise_attribute, "trp_player",ca_strength,1),
        (troop_raise_attribute, "trp_player",ca_agility,1),
        (troop_raise_skill, "trp_player","skl_pathfinding",1),
        (troop_raise_skill, "trp_player","skl_tracking",1),
        (troop_raise_proficiency, "trp_player",wpt_archery,15),
    (else_try),
        (eq,"$background_answer_2",cb2_merchants_helper),
        (troop_raise_attribute, "trp_player",ca_intelligence,1),
        (troop_raise_attribute, "trp_player",ca_charisma,1),
        (troop_raise_skill, "trp_player","skl_inventory_management",1),
        (troop_raise_skill, "trp_player","skl_trade",1),
	(try_end),

	(try_begin),
        (eq,"$background_answer_3",cb3_poacher),
        (troop_raise_attribute, "trp_player",ca_strength,1),
        (troop_raise_attribute, "trp_player",ca_agility,1),
        (troop_raise_skill, "trp_player","skl_power_draw",1),
        (troop_raise_skill, "trp_player","skl_tracking",1),
        (troop_raise_skill, "trp_player","skl_spotting",1),
        #(troop_raise_skill, "trp_player","skl_athletics",1),
        (troop_raise_skill, "trp_player","skl_shield",1), #this is foraging now
        (troop_add_gold, "trp_player", 10),
        (troop_raise_proficiency, "trp_player",wpt_polearm,10),
        (troop_raise_proficiency, "trp_player",wpt_archery,35),
           
        (troop_add_item, "trp_player","itm_butchering_knife",0),
        (troop_add_item, "trp_player","itm_gekokujo_kimono_2_1",0),
        (troop_add_item, "trp_player","itm_gekokujo_sandal_2",0),
        (troop_add_item, "trp_player","itm_gekokujo_yumi_1",0),
        (troop_add_item, "trp_player","itm_gekokujo_arrows_1",0),
        (troop_add_item, "trp_player","itm_dried_meat",0),
        (troop_add_item, "trp_player","itm_dried_meat",0),
        (troop_add_item, "trp_player","itm_furs",0),
        (troop_add_item, "trp_player","itm_furs",0),
    (else_try),
        (eq,"$background_answer_3",cb3_craftsman),
        (troop_raise_attribute, "trp_player",ca_strength,1),
        (troop_raise_attribute, "trp_player",ca_intelligence,1),

        (troop_raise_skill, "trp_player","skl_weapon_master",1),
        (troop_raise_skill, "trp_player","skl_engineer",1),
        (troop_raise_skill, "trp_player","skl_tactics",1),
        (troop_raise_skill, "trp_player","skl_trade",1),

        (troop_raise_proficiency, "trp_player",wpt_two_handed_weapon,15),
        (troop_add_gold, "trp_player", 100),

        (troop_add_item, "trp_player","itm_gekokujo_sandal_2",imod_ragged),
        (troop_add_item, "trp_player","itm_leather_apron",imod_ragged),
           
        (troop_add_item, "trp_player","itm_gekokujo_katana_1", imod_balanced),
        (troop_add_item, "trp_player","itm_gekokujo_kunai",0),
           
        (troop_add_item, "trp_player","itm_tools",0),
        (troop_add_item, "trp_player","itm_smoked_fish",0),
    (else_try),
        (eq,"$background_answer_3",cb3_peddler),
        (troop_raise_attribute, "trp_player",ca_charisma,1),
        (troop_raise_attribute, "trp_player",ca_intelligence,1),
        (troop_raise_skill, "trp_player","skl_riding",1),
        (troop_raise_skill, "trp_player","skl_trade",1),
        (troop_raise_skill, "trp_player","skl_pathfinding",1),
        (troop_raise_skill, "trp_player","skl_inventory_management",1),
           
        (troop_add_item, "trp_player","itm_gekokujo_tekko_1",imod_plain),
        (troop_add_gold, "trp_player", 90),
        (troop_raise_proficiency, "trp_player",wpt_polearm,15),
           
        (troop_add_item, "trp_player","itm_gekokujo_kimono_2_2",0),
        (troop_add_item, "trp_player","itm_gekokujo_sandal_1",imod_ragged),
        (troop_add_item, "trp_player","itm_gekokujo_sugegasa_1",0),
        (troop_add_item, "trp_player","itm_gekokujo_jo",0),
           
        (troop_add_item, "trp_player","itm_linen",0),
        (troop_add_item, "trp_player","itm_pottery",0),
        (troop_add_item, "trp_player","itm_wool",0),
        (troop_add_item, "trp_player","itm_wool",0),
        (troop_add_item, "trp_player","itm_smoked_fish",0),
    (else_try),
        (eq,"$background_answer_3",cb3_troubadour),
        (troop_raise_attribute, "trp_player",ca_charisma,2),
           
        (troop_raise_skill, "trp_player","skl_weapon_master",1),
        (troop_raise_skill, "trp_player","skl_persuasion",1),
        (troop_raise_skill, "trp_player","skl_leadership",1),
        (troop_raise_skill, "trp_player","skl_pathfinding",1),
           
        (troop_add_gold, "trp_player", 80),
        (troop_raise_proficiency, "trp_player",wpt_one_handed_weapon,25),
        (troop_raise_proficiency, "trp_player",wpt_firearm,10),

        (troop_add_item, "trp_player","itm_gekokujo_kimono_1_2",imod_sturdy),
        (troop_add_item, "trp_player","itm_gekokujo_sandal_1",imod_ragged),
        (troop_add_item, "trp_player","itm_gekokujo_tanto_1",imod_rusty),
        (troop_add_item, "trp_player","itm_smoked_fish",0),
    (else_try),
        (eq,"$background_answer_3",cb3_squire),
        (troop_raise_attribute, "trp_player",ca_strength,1),
        (troop_raise_attribute, "trp_player",ca_agility,1),
        (troop_raise_skill, "trp_player","skl_riding",1),
        (troop_raise_skill, "trp_player","skl_weapon_master",1),
        (troop_raise_skill, "trp_player","skl_power_strike",1),
        (troop_raise_skill, "trp_player","skl_leadership",1),

        (troop_add_gold, "trp_player", 20),
        (troop_raise_proficiency, "trp_player",wpt_one_handed_weapon,30),
        (troop_raise_proficiency, "trp_player",wpt_two_handed_weapon,30),
        (troop_raise_proficiency, "trp_player",wpt_polearm,30),
        (troop_raise_proficiency, "trp_player",wpt_archery,10),
        (troop_raise_proficiency, "trp_player",wpt_firearm,10),
        (troop_raise_proficiency, "trp_player",wpt_throwing,10),

        (troop_add_item, "trp_player","itm_gekokujo_hakama_5",imod_ragged),
        (troop_add_item, "trp_player","itm_gekokujo_sandal_1",imod_tattered),
           
        (troop_add_item, "trp_player","itm_gekokujo_katana_1", imod_rusty),
        (troop_add_item, "trp_player","itm_smoked_fish",0),
    (else_try),
        (eq,"$background_answer_3",cb3_lady_in_waiting),
        #(eq,"$character_gender",tf_female),
        (troop_raise_attribute, "trp_player",ca_intelligence,1),
        (troop_raise_attribute, "trp_player",ca_charisma,1),
           
        (troop_raise_skill, "trp_player","skl_persuasion",2),
        (troop_raise_skill, "trp_player","skl_inventory_management",1),
        (troop_raise_skill, "trp_player","skl_wound_treatment",1),
           
        (troop_add_item, "trp_player","itm_gekokujo_tanto_1", 0),
        (troop_add_item, "trp_player","itm_gekokujo_kimono_2_3",imod_sturdy),
        (troop_add_item, "trp_player","itm_gekokujo_sandal_1",0),
		
        (troop_add_gold, "trp_player", 100),
        (troop_raise_proficiency, "trp_player",wpt_one_handed_weapon,10),
        (troop_raise_proficiency, "trp_player",wpt_firearm,15),
        (troop_add_item, "trp_player","itm_smoked_fish",0),
    (else_try),
        (eq,"$background_answer_3",cb3_student),
        (troop_raise_attribute, "trp_player",ca_intelligence,2),
           
        (troop_raise_skill, "trp_player","skl_weapon_master",1),
        (troop_raise_skill, "trp_player","skl_surgery",1),
        (troop_raise_skill, "trp_player","skl_wound_treatment",1),
        (troop_raise_skill, "trp_player","skl_shield",1),
           
        #(troop_add_gold, "trp_player", 80),
        (troop_raise_proficiency, "trp_player",wpt_one_handed_weapon,20),
        (troop_raise_proficiency, "trp_player",wpt_firearm,20),

        (troop_add_item, "trp_player","itm_gekokujo_kimono_2_monk",imod_sturdy),
        (troop_add_item, "trp_player","itm_gekokujo_sandal_2",0),
        (troop_add_item, "trp_player","itm_gekokujo_bo_iron", imod_cracked),
        (troop_add_item, "trp_player","itm_smoked_fish",0),
        (store_random_in_range, ":book_no", books_begin, books_end),
        (troop_add_item, "trp_player",":book_no",0),
    (else_try),
        (eq,"$background_answer_3",cb3_miko),
        #(eq,"$character_gender",tf_female),
        (troop_raise_attribute, "trp_player",ca_charisma,2),
           
        (troop_raise_skill, "trp_player","skl_power_draw",1),
        (troop_raise_skill, "trp_player","skl_shield",1),
        (troop_raise_skill, "trp_player","skl_inventory_management",1),
        (troop_raise_skill, "trp_player","skl_persuasion",1),
           
        (troop_add_gold, "trp_player", 50),
        (troop_raise_proficiency, "trp_player",wpt_one_handed_weapon,15),
        (troop_raise_proficiency, "trp_player",wpt_archery,25),
		
        (troop_add_item, "trp_player","itm_gekokujo_hakama_1_miko"),
        (troop_add_item, "trp_player","itm_gekokujo_sandal_1",0),
        #(troop_add_item, "trp_player","itm_gekokujo_yumi_1",imod_bent),
        #(troop_add_item, "trp_player","itm_gekokujo_arrows_1",0),
        (troop_add_item, "trp_player","itm_gekokujo_tanto_3",imod_chipped),
        (troop_add_item, "trp_player","itm_smoked_fish",0),
    (try_end),

      (try_begin),
        (eq,"$background_answer_4",cb4_revenge),
        (troop_raise_attribute, "trp_player",ca_strength,2),
        (troop_raise_skill, "trp_player","skl_power_strike",1),
      (else_try),
        (eq,"$background_answer_4",cb4_loss),
        (troop_raise_attribute, "trp_player",ca_charisma,2),
        (troop_raise_skill, "trp_player","skl_ironflesh",1),
      (else_try),
        (eq,"$background_answer_4",cb4_wanderlust),
        (troop_raise_attribute, "trp_player",ca_agility,2),
        (troop_raise_skill, "trp_player","skl_pathfinding",1),
      (else_try),
        (eq,"$background_answer_4",cb4_disown),
        (troop_raise_attribute, "trp_player",ca_strength,1),
        (troop_raise_attribute, "trp_player",ca_intelligence,1),
        (troop_raise_skill, "trp_player","skl_weapon_master",1),
      (else_try),
        (eq,"$background_answer_4",cb4_greed),
        (troop_raise_attribute, "trp_player",ca_agility,1),
        (troop_raise_attribute, "trp_player",ca_intelligence,1),
        (troop_raise_skill, "trp_player","skl_looting",1),
      (try_end),


           (try_begin),
             (eq, "$background_type", cb_noble),
             (jump_to_menu, "mnu_auto_return"),
#normal_banner_begin
             (start_presentation, "prsnt_banner_selection"),
#custom_banner_begin
#             (start_presentation, "prsnt_custom_banner"),
           (else_try),
             (change_screen_return, 0),
           (try_end),
           (set_show_messages, 1),
        ]),
    ]
  ),
  (
    "past_life_explanation",mnf_disable_all_keys,
    "{s3}",
    "none",
    [
     (try_begin),
       (gt,"$current_string_reg",14),
       (assign,"$current_string_reg",10),
     (try_end),
     (str_store_string_reg,s3,"$current_string_reg"),
     (try_begin),
       (ge,"$current_string_reg",14),
       (str_store_string,s5,"@Back to the beginning..."),
     (else_try),
       (str_store_string,s5,"@View next segment..."),
     (try_end),
     ],
    [
      ("view_next",[],"{s5}",[
        (val_add,"$current_string_reg",1),
        (jump_to_menu, "mnu_past_life_explanation"),
        ]),
      ("continue",[],"Continue...",
       [
        ]),
      ("go_back_dot",[],"Go back.",[
        (jump_to_menu, "mnu_choose_skill"),
        ]),
    ]
  ),
  
  ("start_phase_2_5",mnf_disable_all_keys,
    "{!}{s16}",
    "none",
    [
      (str_store_party_name, s1, "$g_starting_town"),
      (str_store_string, s16, "$g_journey_string"),
    ],
    [
      ("continue",[], "Continue...",
       [
		 (jump_to_menu, "mnu_start_phase_3"),
       ]),
    ]
  ),
  
  ("start_phase_3",mnf_disable_all_keys,
    "{s16}^^You are exhausted by the time you find the inn in {s1}, and fall asleep quickly. However, you awake before dawn and are eager to explore your surroundings. You venture out onto the streets, which are still deserted. All of a sudden, you hear a sound that stands the hairs of your neck on end -- the rasp of a blade sliding from its scabbard...",
    "none",
    [      
      (assign, ":continue", 1),
      (try_begin),
        (eq, "$current_startup_quest_phase", 1),
        (try_begin),
          (eq, "$g_killed_first_bandit", 1),
          (str_store_string, s11, "str_killed_bandit_at_alley_fight"),                    
        (else_try),
          (str_store_string, s11, "str_wounded_by_bandit_at_alley_fight"),
        (try_end),
        (jump_to_menu, "mnu_start_phase_4"),
        (assign, ":continue", 0),
      (else_try),  
        (eq, "$current_startup_quest_phase", 3),
        (try_begin),
          (eq, "$g_killed_first_bandit", 1),
          (str_store_string, s11, "str_killed_bandit_at_alley_fight"),                    
        (else_try),
          (str_store_string, s11, "str_wounded_by_bandit_at_alley_fight"),
        (try_end),
        (jump_to_menu, "mnu_start_phase_4"),
        (assign, ":continue", 0),      
      (try_end),  
      
      (str_store_party_name, s1, "$g_starting_town"),
      (str_clear, s16),
      (eq, ":continue", 1),
    ],
    [
      ("continue",[], "Continue...",
       [         
         (assign, "$g_starting_town", "$current_town"),
         (call_script, "script_player_arrived"),
         (party_set_morale, "p_main_party", 100),
         (set_encountered_party, "$current_town"),
         (call_script, "script_prepare_alley_to_fight"),
       ]),
    ]
  ),
  ("start_phase_4",mnf_disable_all_keys,
    "{s11}",
    "none",
    [      
      (assign, ":continue", 1),
      (try_begin),  
        (eq, "$current_startup_quest_phase", 2),
        (change_screen_return),       
        (assign, ":continue", 0),
      (else_try),
        (eq, "$current_startup_quest_phase", 3),
        (str_store_string, s11, "str_merchant_and_you_call_some_townsmen_and_guards_to_get_ready_and_you_get_out_from_tavern"),
      (else_try),
        (eq, "$current_startup_quest_phase", 4),
        (try_begin),
          (eq, "$g_killed_first_bandit", 1),
          (str_store_string, s11, "str_town_fight_ended_you_and_citizens_cleaned_town_from_bandits"),
        (else_try),  
          (str_store_string, s11, "str_town_fight_ended_you_and_citizens_cleaned_town_from_bandits_you_wounded"),
        (try_end),
      (try_end),            
          
      (eq, ":continue", 1),
    ],
    [
      ("continue",
      [
        (this_or_next|eq, "$current_startup_quest_phase", 1),
        (eq, "$current_startup_quest_phase", 4),
      ],
      "Continue...",
      [         
        (assign, "$town_entered", 1),
         
        (try_begin),
          (eq, "$current_town", "p_town_1"),
          (assign, ":town_merchant", "trp_edo_merchant"),
          (assign, ":town_room_scene", "scn_town_1_room"),
        (else_try),  
          (eq, "$current_town", "p_town_5"),
          (assign, ":town_merchant", "trp_sakai_merchant"),
          (assign, ":town_room_scene", "scn_town_5_room"),
        (else_try),  
          (eq, "$current_town", "p_town_6"),
          (assign, ":town_merchant", "trp_tsu_merchant"),
          (assign, ":town_room_scene", "scn_town_6_room"),
        (else_try),  
          (eq, "$current_town", "p_castle_24"),
          (assign, ":town_merchant", "trp_hirosaki_merchant"),
          (assign, ":town_room_scene", "scn_town_18_room"),
        (else_try),  
          (eq, "$current_town", "p_town_10"),
          (assign, ":town_merchant", "trp_niigata_merchant"),
          (assign, ":town_room_scene", "scn_town_10_room"),
        (else_try),  
          (eq, "$current_town", "p_town_19"),
          (assign, ":town_merchant", "trp_hakata_merchant"),
          (assign, ":town_room_scene", "scn_town_19_room"),
        (try_end),        
          
        (modify_visitors_at_site, ":town_room_scene"),     
        (reset_visitors),
        (set_visitor, 0, "trp_player"),                    
        (set_visitor, 9, ":town_merchant"),
        
        (assign, "$talk_context", tc_merchants_house),
                  
        (assign, "$dialog_with_merchant_ended", 0),                  
                  
        (set_jump_mission, "mt_meeting_merchant"),

        (jump_to_scene, ":town_room_scene"),
        (change_screen_mission),         
      ]),       

      ("continue",
      [
        (eq, "$current_startup_quest_phase", 3),
      ],
      "Continue...",
      [         
        (call_script, "script_prepare_town_to_fight"),
      ]),              
    ]
  ),
]
