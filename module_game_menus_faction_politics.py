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

game_menus_faction_politics = [
  
  
  
  
  (
    "leave_faction",0,
    "Renouncing your oath is a grave act. Your lord may condemn you and confiscate your lands and holdings.\
 However, if you return them of your own free will, he may let the betrayal go without a fight.",
    "none",
    [
    ],
    [
      ("leave_faction_give_back", [], "Renounce your oath and give up your holdings.",
       [
#Troop commentary changes begin
#        (call_script, "script_add_log_entry", logent_renounced_allegiance,   "trp_player",  -1, "$g_talk_troop", "$g_talk_troop_faction"),
#Troop commentary changes end
        (call_script, "script_player_leave_faction", 1), #1 means give back fiefs
        (change_screen_return),
        ]),
      ("leave_faction_hold", [
          (str_store_party_name, s2, "$g_center_to_give_to_player"),
          ], "Renounce your oath and rule your lands, including {s2}, in your own name.",
       [
        (call_script, "script_give_center_to_lord", "$g_center_to_give_to_player", "trp_player", 0), #this should activate the player faction (it does not)
        (call_script, "script_player_leave_faction", 0), #"1" would mean give back fiefs
		(call_script, "script_activate_player_faction", "trp_player"), #Activating player faction should now work
        (change_screen_return),
        ]),
      ("leave_faction_cancel", [], "Remain loyal and accept the decision.",
       [
        (change_screen_return),
        ]),
    ],
  ),
  (
    "give_center_to_player",mnf_scale_picture,
##diplomacy start+ fix gender of pronoun
    "Your lord offers to extend your fiefs!\
 {s1} sends word that {reg4?she:he} is willing to grant {s2} to you in payment for your loyal service,\
 adding it to your holdings. What is your answer?",
##diplomacy end+
    "none",
    [(set_background_mesh, "mesh_pic_messenger"),
     (store_faction_of_party, ":center_faction", "$g_center_to_give_to_player"),
     (faction_get_slot, ":faction_leader", ":center_faction", slot_faction_leader),
     ##diplomacy start+ put king's gender in reg4
     (call_script, "script_dplmc_store_troop_is_female", ":faction_leader"),
     (assign, reg4, reg0),
     ##diplomacy end+
     (str_store_troop_name, s1, ":faction_leader"),
     (str_store_party_name, s2, "$g_center_to_give_to_player"),
    ],
    [
      ("give_center_to_player_accept",[],"Accept the offer.",
       [(call_script, "script_give_center_to_lord", "$g_center_to_give_to_player", "trp_player", 0),
        (jump_to_menu, "mnu_give_center_to_player_2"),
        ]),
      ("give_center_to_player_reject",[],"Reject. You have no interest in holding {s2}.",
       [(party_set_slot, "$g_center_to_give_to_player", slot_town_lord, stl_rejected_by_player),
        (change_screen_return),
        ]),
    ],
  ),
  
  (
    "give_center_to_player_2",0,
    "With a brief ceremony, you are officially confirmed as the new lord of {s2}{reg3? and its bound village {s4}:}.\
 {reg3?They:It} will make a fine part of your fiefdom.\
 You can now claim the rents and revenues from your personal estates there, draft soldiers from the populace,\
 and manage the lands as you see fit.\
 However, you are also expected to defend your fief and your people from harm,\
 as well as maintaining the rule of law and order.",
    "none",
    [
      (str_store_party_name, s2, "$g_center_to_give_to_player"),
      (assign, reg3, 0),
      (try_begin),
        (party_slot_eq, "$g_center_to_give_to_player", slot_party_type, spt_castle),
        (try_for_range, ":cur_village", villages_begin, villages_end),
          (party_slot_eq, ":cur_village", slot_village_bound_center, "$g_center_to_give_to_player"),
          (str_store_party_name, s4, ":cur_village"),
          (assign, reg3, 1),
        (try_end),
      (try_end),
    ],
    [
      ("continue",[],"Continue...",
       [(change_screen_return),
        ]),
    ],
  ),
  (
    "oath_fulfilled",0,
##diplomacy start+ fix gender of pronoun
    "You had a contract with {s1} to serve {reg4?her:him} for a certain duration.\
 Your contract has now expired. What will you do?",
##diplomacy end+
    "none",
    [
      (faction_get_slot, ":faction_leader", "$players_kingdom", slot_faction_leader),
      ##diplomacy start+ load king's gender into reg4
      (call_script, "script_dplmc_store_troop_is_female", ":faction_leader"),
      (assign, reg4, reg0),
      ##diplomacy end+
      (str_store_troop_name, s1, ":faction_leader"),
     ],
    [
      ("renew_oath",[(faction_get_slot, ":faction_leader", "$players_kingdom", slot_faction_leader),
                     (str_store_troop_name, s1, ":faction_leader")], "Renew your contract with {s1} for another month.",
       [
         (store_current_day, ":cur_day"),
         (store_add, "$mercenary_service_next_renew_day", ":cur_day", 30),
         (change_screen_return),
         ]),
      ("dont_renew_oath",[],"Become free of your bond.",
       [
         (call_script, "script_player_leave_faction", 1), #1 means give back fiefs
         (change_screen_return),
         ]),
    ]
  ),
  
  ("marshall_selection_candidate_ask",0,
   "{s15} will soon select a new strategist for {s23}. Some of the vassals have suggested your name as a likely candidate.",
   "none",
   [
     (try_begin),
       (eq, "$g_presentation_marshall_selection_ended", 1),
       (change_screen_return),
     (try_end),
     (faction_get_slot, ":king", "$players_kingdom", slot_faction_leader),
     (str_store_troop_name, s15, ":king"),
     (str_store_faction_name, s23, "$players_kingdom"),
   ],
   [
      ("marshall_candidate_accept", [], "Let {s15} learn that you are willing to serve as strategist.",
       [
         (start_presentation, "prsnt_marshall_selection"),
       ]
      ),
      ("marshall_candidate_reject", [], "Tell everyone that you are too busy these days.",
       [
         (start_presentation, "prsnt_marshall_selection"),
       ]
      ),
   ]
),
  
##    [
##      ("renew_oath",[],"Renew your oath to {s1} for another month.",[
##          (store_current_day, ":cur_day"),
##          (store_add, "$g_oath_end_day", ":cur_day", 30),
##          (change_screen_return)]),
##      ("dont_renew_oath",[],"Become free of your bond.",[
##          (assign, "$players_kingdom",0),
##          (assign, "$g_player_permitted_castles", 0),
##          (change_screen_return)]),
##    ]
##  ),


#####################################################################
## Captivity....
#####################################################################
#####################################################################
#####################################################################
#####################################################################
  (
    "captivity_avoid_wilderness",0,
    "Suddenly all the world goes black around you.\
 Many hours later you regain your conciousness and find yourself at the spot you fell.\
 Your enemies must have taken you up for dead and left you there.\
 However, it seems that none of your wound were lethal,\
 and altough you feel awful, you find out that can still walk.\
 You get up and try to look for any other survivors from your party.",
    "none",
    [
      ],
    []
  ),
  (
    "captivity_start_wilderness",0,
    "Stub",
    "none",
    [
          (assign, "$g_player_is_captive", 1),
          (try_begin),
            (eq,"$g_player_surrenders",1),
            (jump_to_menu, "mnu_captivity_start_wilderness_surrender"), 
          (else_try),
            (jump_to_menu, "mnu_captivity_start_wilderness_defeat"), 
          (try_end),
      ],
    []
  ),
  
  (
    "captivity_start_wilderness_surrender",0,
    "Stub",
    "none",
    [
       (assign, "$g_player_is_captive", 1),
       (assign,"$auto_menu",-1), #We need this since we may come here by something other than auto_menu
       (assign, "$capturer_party", "$g_encountered_party"),
       (jump_to_menu, "mnu_captivity_wilderness_taken_prisoner"),
      ],
    []
  ),
  (
    "captivity_start_wilderness_defeat",0,
    "Your enemies take you prisoner.",
    "none",
    [
       (assign, "$g_player_is_captive", 1),
       (assign,"$auto_menu",-1),
       (assign, "$capturer_party", "$g_encountered_party"),
       
       (try_begin),
         (party_stack_get_troop_id, ":party_leader", "$g_encountered_party", 0),
         (is_between, ":party_leader", active_npcs_begin, active_npcs_end),
         (troop_slot_eq, ":party_leader", slot_troop_occupation, slto_kingdom_hero),
         (store_sub, ":kingdom_hero_id", ":party_leader", active_npcs_begin),
         (set_achievement_stat, ACHIEVEMENT_BARON_GOT_BACK, ":kingdom_hero_id", 1),
       (try_end),
              
       #gekokujo 3.1 ninja rescue start
       #(jump_to_menu, "mnu_captivity_wilderness_taken_prisoner"),
       (try_begin),
         (gt, "$gekokujo_rescue_score", 0),
         (jump_to_menu, "mnu_gekokujo_captivity_avoid"),
       (else_try),
         (jump_to_menu, "mnu_captivity_wilderness_taken_prisoner"),
       (try_end),
       #gekokujo 3.1 ninja rescue end
    ],
    []
  ),
  (
    "captivity_start_castle_surrender",0,
    "Stub",
    "none",
    [
       (assign, "$g_player_is_captive", 1),
       (assign,"$auto_menu",-1),
       (assign, "$capturer_party", "$g_encountered_party"),
       (jump_to_menu, "mnu_captivity_castle_taken_prisoner"),
      ],
    []
  ),
  (
    "captivity_start_castle_defeat",0,
    "Stub",
    "none",
    [
       (assign, "$g_player_is_captive", 1),
       (assign,"$auto_menu",-1),
       (assign, "$capturer_party", "$g_encountered_party"),
       
       #gekokujo 3.1 ninja rescue start
       #(jump_to_menu, "mnu_captivity_castle_taken_prisoner"),
       (try_begin),
         (gt, "$gekokujo_rescue_score", 0),
         (jump_to_menu, "mnu_gekokujo_captivity_avoid"),
       (else_try),
         (jump_to_menu, "mnu_captivity_castle_taken_prisoner"),
       (try_end),
       #gekokujo 3.1 ninja rescue end
      ],
    []
  ),
  (
    "captivity_start_under_siege_defeat",0,
    "Your enemies take you prisoner.",
    "none",
    [
       (assign, "$g_player_is_captive", 1),
       (assign,"$auto_menu",-1),
       (assign, "$capturer_party", "$g_encountered_party"),
       #gekokujo 3.1 ninja rescue start
       #(jump_to_menu, "mnu_captivity_castle_taken_prisoner"),
       (try_begin),
         (gt, "$gekokujo_rescue_score", 0),
         (jump_to_menu, "mnu_gekokujo_captivity_avoid"),
       (else_try),
         (jump_to_menu, "mnu_captivity_castle_taken_prisoner"),
       (try_end),
       #gekokujo 3.1 ninja rescue end
    ],
    []
  ),
  #gekokujo 3.1 ninja rescue end
  
  (
    "captivity_wilderness_taken_prisoner",mnf_scale_picture,
    "Your enemies take you prisoner.",
    "none",
    [
        (set_background_mesh, "mesh_pic_prisoner_wilderness"),
     ],
    [
      ("continue",[],"Continue...",
       [
         (try_for_range, ":npc", companions_begin, companions_end),
           (main_party_has_troop, ":npc"),
           (store_random_in_range, ":rand", 0, 100),
           (lt, ":rand", 30),
           (remove_member_from_party, ":npc", "p_main_party"),
           (troop_set_slot, ":npc", slot_troop_occupation, 0),
           (troop_set_slot, ":npc", slot_troop_playerparty_history, pp_history_scattered),
           (assign, "$last_lost_companion", ":npc"),
           (store_faction_of_party, ":victorious_faction", "$g_encountered_party"),
           (troop_set_slot, ":npc", slot_troop_playerparty_history_string, ":victorious_faction"),
           (troop_set_health, ":npc", 100),
           (store_random_in_range, ":rand_town", towns_begin, towns_end),
           (troop_set_slot, ":npc", slot_troop_cur_center, ":rand_town"),
           (assign, ":nearest_town_dist", 1000),
           (try_for_range, ":town_no", towns_begin, towns_end),
             (store_faction_of_party, ":town_fac", ":town_no"),
             (store_relation, ":reln", ":town_fac", "fac_player_faction"),
             (ge, ":reln", 0),
             (store_distance_to_party_from_party, ":dist", ":town_no", "p_main_party"),
             (lt, ":dist", ":nearest_town_dist"),
             (assign, ":nearest_town_dist", ":dist"),
             (troop_set_slot, ":npc", slot_troop_cur_center, ":town_no"),
           (try_end),
         (try_end),
		 
		 #gekokujo 3.0 microfactions! start
		 #30% chance a fort companion is sent back home
         (try_for_range, ":npc", fort_companions_begin, fort_companions_end),
           (main_party_has_troop, ":npc"),
           (store_random_in_range, ":rand", 0, 100),
           (lt, ":rand", 30),
           (remove_member_from_party, ":npc", "p_main_party"),
           (troop_set_slot, ":npc", slot_troop_occupation, 0),
           (troop_set_slot, ":npc", slot_troop_playerparty_history, pp_history_scattered),
           (assign, "$last_lost_companion", ":npc"),
           (store_faction_of_party, ":victorious_faction", "$g_encountered_party"),
           (troop_set_slot, ":npc", slot_troop_playerparty_history_string, ":victorious_faction"),
           (troop_set_health, ":npc", 100),
		   (troop_get_slot, ":home", ":npc", slot_troop_home),
		   (party_set_slot, ":home", slot_fort_npc_2_state, 2), #set to "return"
         (try_end),
		 #gekokujo 3.0 microfactions! end

         (set_camera_follow_party, "$capturer_party"),
         (assign, "$g_player_is_captive", 1),
         (store_random_in_range, ":random_hours", 18, 30),         
         (call_script, "script_event_player_captured_as_prisoner"),
         (call_script, "script_stay_captive_for_hours", ":random_hours"),
         (assign,"$auto_menu","mnu_captivity_wilderness_check"),
         (change_screen_return),
         ]),
      ]
  ),
  (
    "captivity_wilderness_check",0,
    "stub",
    "none",
    [(jump_to_menu,"mnu_captivity_end_wilderness_escape")],
    []
  ),
  (
    "captivity_end_wilderness_escape", mnf_scale_picture,
    "After painful days of being dragged about as a prisoner, you find a chance and escape from your captors!",
    "none",
    [
        (play_cue_track, "track_escape"),
		#gekokujo only one escape pic type
		(set_background_mesh, "mesh_gekokujo_pic_escape"),
	#	##diplomacy start+ test gender with script
    #    #(troop_get_type, ":is_female", "trp_player"),#<- replaced
    #    (try_begin),
    #      #(eq, ":is_female", 1),#<- replaced
	#	  (eq, 1, "$character_gender"),#<- added
    #      (set_background_mesh, "mesh_pic_escape_1_fem"),
    #    (else_try),
    #      (set_background_mesh, "mesh_pic_escape_1"),
    #    (try_end),
	#	##diplomacy end+
    ],
    [
      ("continue",[],"Continue...",
       [
           (assign, "$g_player_is_captive", 0),
           (try_begin),
             (party_is_active, "$capturer_party"),
             (party_relocate_near_party, "p_main_party", "$capturer_party", 2),
           (try_end),
           (call_script, "script_set_parties_around_player_ignore_player", 2, 4),
           (assign, "$g_player_icon_state", pis_normal),
           (set_camera_follow_party, "p_main_party"),
           (rest_for_hours, 0, 0, 0), #stop resting
           ##diplomacy begin
           (assign, "$g_move_fast", 1),
           ##diplomacy end
           (change_screen_return),
        ]),
    ]
  ),
  (
    "captivity_castle_taken_prisoner",0,
    "You are quickly surrounded by guards who take away your weapons. With curses and insults, they throw you into the prison where you must while away the miserable days of your captivity.",
    "none",
    [
		##diplomacy start+ test gender with script
        #(troop_get_type, ":is_female", "trp_player"),#<- replaced
        (try_begin),
          #(eq, ":is_female", 1),#<- replaced
		  (eq, 1, "$character_gender"),#<- added
          (set_background_mesh, "mesh_pic_prisoner_fem"),
        (else_try),
          (set_background_mesh, "mesh_pic_prisoner_man"),
        (try_end),
		##diplomacy end+
    ],
    [
      ("continue",[],"Continue...",
       [
           (assign, "$g_player_is_captive", 1),
           (store_random_in_range, ":random_hours", 16, 22),
           (call_script, "script_event_player_captured_as_prisoner"),
           (call_script, "script_stay_captive_for_hours", ":random_hours"),
           (assign,"$auto_menu", "mnu_captivity_castle_check"),
           (change_screen_return)
        ]),
    ]
  ),
  (
    "captivity_rescue_lord_taken_prisoner",0,
    "You remain in disguise for as long as possible before revealing yourself.\
 The guards are outraged and beat you savagely before throwing you back into the cell for God knows how long...",
    "none",
    [
		##diplomacy start+ test gender with script
        #(troop_get_type, ":is_female", "trp_player"),#<-replaced
        (try_begin),
          #(eq, ":is_female", 1),#<-replaced
		  (eq, 1, "$character_gender"),#<- added
          (set_background_mesh, "mesh_pic_prisoner_fem"),
        (else_try),
          (set_background_mesh, "mesh_pic_prisoner_man"),
        (try_end),
		##diplomacy end+
   ],
    [
      ("continue",[],"Continue...",
       [
           (assign, "$g_player_is_captive", 1),
           (store_random_in_range, ":random_hours", 16, 22),
           (call_script, "script_event_player_captured_as_prisoner"),
           (call_script, "script_stay_captive_for_hours", ":random_hours"),
           (assign,"$auto_menu", "mnu_captivity_castle_check"),
           (change_screen_return),
        ]),
    ]
  ),
  (
    "captivity_castle_check",0,
    "stub",
    "none",
    [
        (store_random_in_range, reg(7), 0, 10),
        (try_begin),
		  (party_is_active, "$capturer_party"),
		  (store_faction_of_party, ":capturer_faction", "$capturer_party"),
		  (is_between, ":capturer_faction", kingdoms_begin, kingdoms_end),
		  (store_relation, ":relation_w_player_faction", ":capturer_faction", "fac_player_faction"),
		  (ge, ":relation_w_player_faction", 0),
          (jump_to_menu,"mnu_captivity_end_exchanged_with_prisoner"),
		(else_try),
          (lt, reg(7), 4),
                              
          (store_character_level, ":player_level", "trp_player"),
          (store_mul, "$player_ransom_amount", ":player_level", 50),
          (val_add, "$player_ransom_amount", 100),                    
          (store_troop_gold, reg3, "trp_player"),          
          (store_div, ":player_gold_div_20", reg3, 20),
          (val_add, "$player_ransom_amount", ":player_gold_div_20"),          
          
          (gt, reg3, "$player_ransom_amount"),
          (jump_to_menu,"mnu_captivity_end_propose_ransom"),
        (else_try),
          (lt, reg7, 7),
          (jump_to_menu,"mnu_captivity_end_exchanged_with_prisoner"),
        (else_try),
          (jump_to_menu,"mnu_captivity_castle_remain"),
        (try_end),
    ],
    []
  ),
  (
    "captivity_end_exchanged_with_prisoner",0,
    "After days of imprisonment, you are finally set free when your captors exchange you with another prisoner.",
    "none",
    [
      (play_cue_track, "track_escape"),
      ],
    [
      ("continue",[],"Continue...",
       [
           (assign, "$g_player_is_captive", 0),
           (try_begin),
             (party_is_active, "$capturer_party"),
             (party_relocate_near_party, "p_main_party", "$capturer_party", 2),
           (try_end),
           (call_script, "script_set_parties_around_player_ignore_player", 2, 12),
           (assign, "$g_player_icon_state", pis_normal),
           (set_camera_follow_party, "p_main_party"),
           (rest_for_hours, 0, 0, 0), #stop resting
           (change_screen_return),
        ]),
    ]
  ),
  (
    "captivity_end_propose_ransom",0,
    "You spend long hours in the sunless dank of the prison, more than you can count.\
 Suddenly one of your captors enters your cell with an offer;\
 he proposes to free you in return for {reg5} mon of your hidden wealth. You decide to...",
    "none",
    [
      (assign, reg5, "$player_ransom_amount"),
    ],
    [
      ("captivity_end_ransom_accept",
      [
        (store_troop_gold,":player_gold", "trp_player"),
        (ge, ":player_gold","$player_ransom_amount")
      ],"Accept the offer.",
      [
        (play_cue_track, "track_escape"),
        (assign, "$g_player_is_captive", 0),
        (troop_remove_gold, "trp_player", "$player_ransom_amount"), 
        (try_begin),
          (party_is_active, "$capturer_party"),
          (party_relocate_near_party, "p_main_party", "$capturer_party", 1),
        (try_end),
        (call_script, "script_set_parties_around_player_ignore_player", 2, 6),
        (assign, "$g_player_icon_state", pis_normal),
        (set_camera_follow_party, "p_main_party"),
        (rest_for_hours, 0, 0, 0), #stop resting
        (change_screen_return),
      ]),
      ("captivity_end_ransom_deny",
      [
      ],"Refuse him, wait for something better.",
      [
        (assign, "$g_player_is_captive", 1),
        (store_random_in_range, reg(8), 16, 22),
        (call_script, "script_stay_captive_for_hours", reg8),
        (assign,"$auto_menu", "mnu_captivity_castle_check"),
        (change_screen_return),
      ]),
    ]
  ),
  (
    "captivity_castle_remain",mnf_scale_picture|mnf_disable_all_keys,
    "More days pass in the darkness of your cell. You get through them as best you can,\
 enduring the kicks and curses of the guards, watching your underfed body waste away more and more...",
    "none",
    [
        ##diplomacy start+ test gender with script
		#(troop_get_type, ":is_female", "trp_player"),#<- replaced
        (try_begin),
          #(eq, ":is_female", 1),#<- replaced
		  (eq, 1, "$character_gender"),#<- added
          (set_background_mesh, "mesh_pic_prisoner_fem"),
        (else_try),
          (set_background_mesh, "mesh_pic_prisoner_man"),
        (try_end),
		##diplomacy end+
        (store_random_in_range, ":random_hours", 16, 22),
        (call_script, "script_stay_captive_for_hours", ":random_hours"),
        (assign,"$auto_menu", "mnu_captivity_castle_check"),
        
    ],
    [
      ("continue",[],"Continue...",
       [
           (assign, "$g_player_is_captive", 1),
           (change_screen_return),
        ]),
    ]
  ),
  (
    "invite_player_to_faction_without_center",mnf_scale_picture,
##diplomacy start+ fix gender of pronouns
    "You receive an offer of vassalage!^^\
 {s8} of {s9} has sent a courier to bring you an invititation in his own hand.\
 You would be granted the honour of becoming a vassal {lord/lady} of {s9},\
 and in return {s8} asks you to swear an oath of fealty to {reg4?her:him} and fight in {reg4?her:his} military campaigns,\
 although {reg4?she:he} offers you no lands or titles.\
 {reg4?She:He} will surely be offended if you do not take the offer...",
##diplomacy end+
    "none",
    [
        (set_background_mesh, "mesh_pic_messenger"),
        (faction_get_slot, "$g_invite_faction_lord", "$g_invite_faction", slot_faction_leader),
        ##diplomacy start+ store gender in reg4
        (call_script, "script_dplmc_store_troop_is_female", "$g_invite_faction_lord"),
        (assign, reg4, reg0),
        ##diplomacy start+
        (str_store_troop_name, s8, "$g_invite_faction_lord"),
        (str_store_faction_name, s9, "$g_invite_faction"),
      ],
    [
      ("faction_accept",[],"Accept!",
       [(str_store_troop_name,s1,"$g_invite_faction_lord"),
        (setup_quest_text,"qst_join_faction"),

        (str_store_troop_name_link, s3, "$g_invite_faction_lord"),
        (str_store_faction_name_link, s4, "$g_invite_faction"),
        (quest_set_slot, "qst_join_faction", slot_quest_giver_troop, "$g_invite_faction_lord"),
        (quest_set_slot, "qst_join_faction", slot_quest_expiration_days, 30),
		(quest_set_slot, "qst_join_faction", slot_quest_failure_consequence, 0),
		
		##diplomacy start+ fix gender of pronoun
        (str_store_string, s2, "@Find and speak with {s3} of {s4} to give {reg4?her:him} your oath of loyalty."),
        ##diplomacy end+
        (call_script, "script_start_quest", "qst_join_faction", "$g_invite_faction_lord"),
        (call_script, "script_report_quest_troop_positions", "qst_join_faction", "$g_invite_faction_lord", 3),
        (jump_to_menu, "mnu_invite_player_to_faction_accepted"),
        ]),
      ("faction_reject",[],"Decline the invitation.",
       [(call_script, "script_change_player_relation_with_troop", "$g_invite_faction_lord", -3),
        (call_script, "script_change_player_relation_with_faction", "$g_invite_faction", -10),
        (assign, "$g_invite_faction", 0),
        (assign, "$g_invite_faction_lord", 0),
        (assign, "$g_invite_offered_center", 0),
        (change_screen_return),
        ]),
     ]
  ),
  

  (
    "invite_player_to_faction",mnf_scale_picture,
##diplomacy start+ fix gender of pronouns
    "You receive an offer of vassalage!^^\
 {s8} of {s9} has sent a courier to bring you an invititation in {reg4?her:his} own hand.\
 You would be granted the honour of becoming a vassal {lord/lady} of {s9},\
 and in return {s8} asks you to swear an oath of fealty to {reg4?her:him} and fight in {reg4?her:his} military campaigns,\
 offering you the fief of {s2} for your loyal service.\
 {reg4?She:He} will surely be offended if you do not take the offer...",
##diplomacy end+
    "none",
    [
        (set_background_mesh, "mesh_pic_messenger"),
        (faction_get_slot, "$g_invite_faction_lord", "$g_invite_faction", slot_faction_leader),
        ##diplomacy start+ store gender in reg4
        (call_script, "script_dplmc_store_troop_is_female", "$g_invite_faction_lord"),
        (assign, reg4, reg0),
        ##diplomacy start+
        (str_store_troop_name, s8, "$g_invite_faction_lord"),
        (str_store_faction_name, s9, "$g_invite_faction"),
        (str_store_party_name, s2, "$g_invite_offered_center"),
      ],
    [
      ("faction_accept",[],"Accept!",
       [(str_store_troop_name,s1,"$g_invite_faction_lord"),
        (setup_quest_text,"qst_join_faction"),

        (str_store_troop_name_link, s3, "$g_invite_faction_lord"),
        (str_store_faction_name_link, s4, "$g_invite_faction"),
        (quest_set_slot, "qst_join_faction", slot_quest_giver_troop, "$g_invite_faction_lord"),
        (quest_set_slot, "qst_join_faction", slot_quest_expiration_days, 30),
        ##diplomacy start+ fix gender of pronoun
        (str_store_string, s2, "@Find and speak with {s3} of {s4} to give {reg4?her:him} your oath of fealty."),
        ##diplomacy end+
        (call_script, "script_start_quest", "qst_join_faction", "$g_invite_faction_lord"),
        (call_script, "script_report_quest_troop_positions", "qst_join_faction", "$g_invite_faction_lord", 3),
        (jump_to_menu, "mnu_invite_player_to_faction_accepted"),
        ]),
      ("faction_reject",[],"Decline the invitation.",
       [(call_script, "script_change_player_relation_with_troop", "$g_invite_faction_lord", -3),
        (assign, "$g_invite_faction", 0),
        (assign, "$g_invite_faction_lord", 0),
        (assign, "$g_invite_offered_center", 0),
        (change_screen_return),
        ]),
     ]
  ),
  
  (
    "invite_player_to_faction_accepted",0,
##diplomacy start+ fix gender of pronouns (king's gender should already be in reg4)
    "In order to become a vassal, you must swear an oath of fealty to {s3}.\
 You shall have to find {reg4?her:him} and give him your oath in person. {s5}",
##diplomacy end+
    "none",
    [
        (call_script, "script_get_information_about_troops_position", "$g_invite_faction_lord", 0),
        (str_store_troop_name, s3, "$g_invite_faction_lord"),
        (str_store_string, s5, "@{!}{s1}"),
      ],
    [
      ("continue",[],"Continue...",
       [(change_screen_return),
        ]),
     ]
  ),
  (
    "question_peace_offer",0,
    "You Receive a Peace Offer^^The {s1} offers you a peace agreement. What is your answer?",
    "none",
    [
      (str_store_faction_name, s1, "$g_notification_menu_var1"),
      (set_fixed_point_multiplier, 100),
      (position_set_x, pos0, 65),
      (position_set_y, pos0, 30),
      (position_set_z, pos0, 170),
      (set_game_menu_tableau_mesh, "tableau_faction_note_mesh_banner", "$g_notification_menu_var1", pos0),

      ##diplomacy begin
      (store_relation,  ":relation", "fac_player_supporters_faction", "$g_notification_menu_var1"),
      (try_begin),
        (ge, ":relation", 0),
        (change_screen_return),
      (try_end),
      ##diplomacy end
      ],
    [
      ("peace_offer_accept",[],"Accept",
       [
         (call_script, "script_diplomacy_start_peace_between_kingdoms", "fac_player_supporters_faction", "$g_notification_menu_var1", 1),
         (change_screen_return),
        ]),
        ##diplomacy begin
      ("dplmc_peace_offer_terms",[],"Dictate the peace terms",
       [
        (start_presentation, "prsnt_dplmc_peace_terms"),
        ]),
        ##diplomacy end
      ("peace_offer_reject",[],"Reject",
       [
         (call_script, "script_change_player_relation_with_faction", "$g_notification_menu_var1", -5),
         (change_screen_return),
        ]),
     ]
  ),
  (
    "notification_truce_expired",0,
    "Truce Has Expired^^The truce between {s1} and {s2} has expired.",
    "none",
    [
      (str_store_faction_name, s1, "$g_notification_menu_var1"),
      (str_store_faction_name, s2, "$g_notification_menu_var2"),
	  
      (set_fixed_point_multiplier, 100),
      (position_set_x, pos0, 65),
      (position_set_y, pos0, 30),
      (position_set_z, pos0, 170),
      (set_game_menu_tableau_mesh, "tableau_faction_note_mesh_banner", "$g_notification_menu_var1", pos0),
      ],
    [
      ("continue",[],"Continue",
       [
	   (change_screen_return),
        ]),
     ]
  ),
  
  (
    "notification_feast_quest_expired",0,
    "{s10}",
    "none",
    [
    (str_store_string, s10, "str_feast_quest_expired"),
    ],
    [
      ("continue",[],"Continue",
       [
	   (change_screen_return),
        ]),
     ]
  ),
  (
    "notification_sortie_possible",0,
    "Enemy Sighted: Enemies have been sighted outside the walls of {s4}, and {s5} and others are preparing for a sortie. You may join them if you wish.",
    "none",
    [
	(str_store_party_name, s4, "$g_notification_menu_var1"),
	(party_stack_get_troop_id, ":leader", "$g_notification_menu_var2", 0),
	(str_store_troop_name, s5, ":leader"),
      ],
    [
      ("continue",[],"Continue",
       [
	   #stop auto-clock
	   
	   (change_screen_return),
        ]),
     ]
  ),
  
  
  
  
  (
    "notification_casus_belli_expired",0,
    "Kingdom Fails to Respond^^The {s1} has not responded to the {s2}'s provocations, and {s3} suffers a loss of face among {reg4?her:his} more bellicose subjects...^",
    "none",
    [
      (str_store_faction_name, s1, "$g_notification_menu_var1"),
      (str_store_faction_name, s2, "$g_notification_menu_var2"),
	  (faction_get_slot, ":faction_leader", "$g_notification_menu_var1", slot_faction_leader),
      (str_store_troop_name, s3, ":faction_leader"),
	  ##diplomacy start+ use a script for gender
	  #(troop_get_type, reg4, ":faction_leader"),#<- OLD
	  (call_script, "script_dplmc_store_troop_is_female_reg", ":faction_leader", 4),
      ##diplomacy end+
	  
      (set_fixed_point_multiplier, 100),
      (position_set_x, pos0, 65),
      (position_set_y, pos0, 30),
      (position_set_z, pos0, 170),
      (set_game_menu_tableau_mesh, "tableau_faction_note_mesh_banner", "$g_notification_menu_var1", pos0),
      ],
    [
      ("continue",[],"Continue",
       [
	   (call_script, "script_faction_follows_controversial_policy", "$g_notification_menu_var1", logent_policy_ruler_ignores_provocation),
	   (change_screen_return),
        ]),
     ]
  ),
  (
    "notification_lord_defects",0,
##diplomacy start+ Fix gender of pronouns
    "Defection: {s4} has abandoned the {s5} and joined the {s7}, taking {reg4?her:his} his fiefs with {reg4?her:him}",
##diplomacy end+
    "none",
	[
	  (assign, ":defecting_lord", "$g_notification_menu_var1"),
	  (assign, ":old_faction", "$g_notification_menu_var2"),
	  (str_store_troop_name, s4, ":defecting_lord"),
	  (str_store_faction_name, s5, ":old_faction"),
	  (store_faction_of_troop, ":new_faction", ":defecting_lord"),
	  (str_store_faction_name, s7, ":new_faction"),
	  ##diplomacy start+ get gender with script
	  #(troop_get_type, reg4, ":defecting_lord"),#<-OLD
	  (call_script, "script_dplmc_store_troop_is_female_reg", ":defecting_lord", 4),
	  ##diplomacy end+
	  
	],
    [
      ("continue",[],"Continue",
       [
	   (change_screen_return),
        ]),
     ]
	),
	
	
  (
    "notification_treason_indictment",0,
    "Treason Indictment^^{s9}",
    "none",
    [
	  (assign, ":indicted_lord", "$g_notification_menu_var1"),
	  (assign, ":former_faction", "$g_notification_menu_var2"),
	  (faction_get_slot, ":former_faction_leader", ":former_faction", slot_faction_leader),
	  
	  #Set up string
	  (try_begin),
			(eq, ":indicted_lord", "trp_player"),
			(str_store_troop_name, s7, ":former_faction_leader"),
			(str_store_string, s9, "str_you_have_been_indicted_for_treason_to_s7_your_properties_have_been_confiscated_and_you_would_be_well_advised_to_flee_for_your_life"),
	  (else_try),	
			(str_store_troop_name, s4, ":indicted_lord"),
			(str_store_faction_name, s5, ":former_faction"),
			(str_store_troop_name, s6, ":former_faction_leader"),
		
			##diplomacy start+ get gender with script
			#(troop_get_type, reg4, ":indicted_lord"),#<-OLD
			(call_script, "script_dplmc_store_troop_is_female_reg", ":indicted_lord", 4),
			##diplomacy end+
			(store_faction_of_troop, ":new_faction", ":indicted_lord"),
			(try_begin),
				(is_between, ":new_faction", kingdoms_begin, kingdoms_end),
				(str_store_faction_name, s10, ":new_faction"),
				(str_store_string, s11, "str_with_the_s10"),
			(else_try),
				(str_store_string, s11, "str_outside_calradia"),
			(try_end),
			(str_store_string, s9, "str_by_order_of_s6_s4_of_the_s5_has_been_indicted_for_treason_the_lord_has_been_stripped_of_all_reg4herhis_properties_and_has_fled_for_reg4herhis_life_he_is_rumored_to_have_gone_into_exile_s11"),
		(try_end),
	  
	  
	],
    [
      ("continue",[],"Continue",
       [
	   (change_screen_return),
        ]),
     ]
	),
	
  (
    "notification_border_incident",0,
    "Border incident^^Word reaches you that {s9}. Though you don't know whether or not the rumors are true, you do know one thing -- this seemingly minor incident has raised passions among the {s4}, making it easier for them to go to war against the {s3}, if they want it...",
    "none",
    [
	  (assign, ":acting_village", "$g_notification_menu_var1"),
	  (assign, ":target_village", "$g_notification_menu_var2"),
	  (store_faction_of_party, ":acting_faction", ":acting_village"),
	  
	  (try_begin),
			(eq, ":target_village", -1),
			(party_get_slot, ":target_faction", ":acting_village", slot_center_original_faction),
			(try_begin),
				(this_or_next|eq, ":target_faction", ":acting_faction"),
                              		(neg|faction_slot_eq, ":target_faction", slot_faction_state, sfs_active),
				(party_get_slot, ":target_faction", ":acting_village", slot_center_ex_faction),
			(try_end),

		    (str_store_party_name, s1, ":acting_village"),
		    (str_store_faction_name, s3, ":acting_faction"),
		    (str_store_faction_name, s4, ":target_faction"),
			(faction_get_slot, ":target_leader", ":target_faction", slot_faction_leader),
		    (str_store_troop_name, s5, ":target_leader"),
			
			(str_store_string, s9, "str_local_notables_from_s1_a_village_claimed_by_the_s4_have_been_mistreated_by_their_overlords_from_the_s3_and_petition_s5_for_protection"),
			(display_log_message, "@There has been an alleged border incident: {s9}"),
			
			(call_script, "script_add_log_entry", logent_border_incident_subjects_mistreated, ":acting_village", -1, -1, ":acting_faction"),
			
	
      (else_try),	
			(store_faction_of_party, ":target_faction", ":target_village"),
		  
		    (str_store_party_name, s1, ":acting_village"),
		    (str_store_party_name, s2, ":target_village"),
			  
			(store_random_in_range, ":random", 0, 3),
			(try_begin),
				(eq, ":random", 0),

				(str_store_string, s9, "str_villagers_from_s1_stole_some_cattle_from_s2"),
				(display_log_message, "@There has been an alleged border incident: {s9}"),
				
				(call_script, "script_add_log_entry", logent_border_incident_cattle_stolen, ":acting_village", ":target_village", -1,":acting_faction"),
				
			(else_try),
				(eq, ":random", 1),

				(str_store_string, s9, "str_villagers_from_s1_abducted_a_woman_from_a_prominent_family_in_s2_to_marry_one_of_their_boys"),
				(display_log_message, "@There has been an alleged border incident: {s9}"),
				
				(call_script, "script_add_log_entry", logent_border_incident_bride_abducted, ":acting_village", ":target_village", -1, ":acting_faction"),
			(else_try),	
				(eq, ":random", 2),
				
				(str_store_string, s9, "str_villagers_from_s1_killed_some_farmers_from_s2_in_a_fight_over_the_diversion_of_a_stream"),
				(display_log_message, "@There has been an alleged border incident: {s9}"),
				
			    (call_script, "script_add_log_entry", logent_border_incident_villagers_killed, ":acting_village", ":target_village", -1,":acting_faction"),
			(try_end),
	  
	  (try_end),
	  
	  (str_store_faction_name, s3, ":acting_faction"),
	  (str_store_faction_name, s4, ":target_faction"),
	  
	  (store_add, ":slot_provocation_days", ":acting_faction", slot_faction_provocation_days_with_factions_begin),
	  (val_sub, ":slot_provocation_days", kingdoms_begin),
	  #gekokujo 3.0 provocation days increase start
	  (faction_set_slot, ":target_faction", ":slot_provocation_days", 60),
	  #(faction_set_slot, ":target_faction", ":slot_provocation_days", 30),
	  #gekokujo 3.0 provocation days increase end
	  
      ],
    [
      ("continue",[],"Continue",
       [
	   (change_screen_return),
        ]),
     ]
  ),
  
  
  
  
  (
    "notification_player_faction_active",0,
    "You now possess land in your name, without being tied to any domain. This makes you a daimyo in your own right, with your court temporarily located at {s12}. However, the other daimyo in Japan will at first consider you a threat, for if any upstart warlord can start a clan, then their own legitimacy is called into question.^^You may find it desirable at this time to pledge yourself to an existing domain. If you want to continue as a warlord, then your first priority should be to establish an independent right to rule. You can establish your right to rule through several means -- marrying into a high-born family, recruiting new lords, governing your lands, treating with other daimyo, or dispatching your companions on missions.^^At any rate, your first step should be to appoint a chief minister from among your companions, to handle affairs of state. Different companions have different capabilities.^You may appoint new ministers from time to time. You may also change the location of your court, by speaking to the minister.",
    "none",
    [
      (set_fixed_point_multiplier, 100),
      (position_set_x, pos0, 65),
      (position_set_y, pos0, 30),
      (position_set_z, pos0, 170),
      (set_game_menu_tableau_mesh, "tableau_faction_note_mesh_banner", "fac_player_supporters_faction", pos0),
      
      (unlock_achievement, ACHIEVEMENT_CALRADIAN_TEA_PARTY),
      (play_track, "track_coronation"),
	  
	  (try_for_range, ":walled_center", walled_centers_begin, walled_centers_end),
	    (lt, "$g_player_court", walled_centers_begin),
		(store_faction_of_party, ":walled_center_faction", ":walled_center"),
	    (eq, ":walled_center_faction", "fac_player_supporters_faction"),
		(assign, "$g_player_court", ":walled_center"),
		
		##diplomacy start+
		#OLD VERSION:
		#(try_begin),
		#	(troop_get_slot, ":spouse", "trp_player", slot_troop_spouse),
		#	(is_between, ":spouse", kingdom_ladies_begin, kingdom_ladies_end),
		#	(troop_set_slot, ":spouse", slot_troop_cur_center, "$g_player_court"),
		#(try_end),
		#
		#NEW VERSION:
		#For settings with polygamy, check all kingdom ladies to see if they are wives.
		#Also move unmarried daughters/sisters of the player if they exist (they cannot
		#in Native, but might in mods).
		(try_for_range, ":lady", kingdom_ladies_begin, kingdom_ladies_end),
			#Make sure the spouse hasn't been promoted, and is not a prisoner, and is not exiled/dead
			(troop_slot_eq, ":lady", slot_troop_occupation, slto_kingdom_lady),
			(neg|troop_slot_ge, ":lady", slot_troop_leaded_party, 0),
			#Make sure the lady isn't a prisoner
			(neg|troop_slot_ge, ":lady", slot_troop_prisoner_of_party, 0),
			(try_begin),
				#Check if the lady is the player's spouse
				(this_or_next|troop_slot_eq, "trp_player", slot_troop_spouse, ":lady"),
					(troop_slot_eq, ":lady", slot_troop_spouse, "trp_player"),
				#Update location
				(troop_set_slot, ":lady", slot_troop_cur_center, "$g_player_court"),
			(else_try),
				#If the lady is unmarried, check if she is the player's dependent.
				(troop_slot_eq, ":lady", slot_troop_spouse, -1),
				(this_or_next|troop_slot_eq, ":lady", slot_troop_father, "trp_player"),
				(this_or_next|troop_slot_eq, ":lady", slot_troop_mother, "trp_player"),
					(troop_slot_eq, ":lady", slot_troop_guardian, "trp_player"),
				#Update location
				(troop_set_slot, ":lady", slot_troop_cur_center, "$g_player_court"),
			(try_end),
		(try_end),
		##diplomacy end+
		
		(str_store_party_name, s12, "$g_player_court"),
	  (try_end),
	  
      ],
    [
	  ##diplomacy start+
	  #Make compatible with polygamy
      ("appoint_spouse",[
	  (troop_slot_ge, "trp_player", slot_troop_spouse, 1),
	  (troop_get_slot, ":player_spouse", "trp_player", slot_troop_spouse),
	  (neg|troop_slot_eq, ":player_spouse", slot_troop_occupation, slto_kingdom_hero),
	  ##diplomacy start+
	  #Also do not appoint the missing or the dead
	  (neg|troop_slot_ge, ":player_spouse", slot_troop_occupation, slto_retirement),
	  (call_script, "script_dplmc_store_troop_is_female", ":player_spouse"),#reg0 make gender-correct
	  ##diplomacy end+
	  (str_store_troop_name, s10, ":player_spouse"),
	  ],"Appoint your {reg0?wife:husband}, {s10}...",
       [
	   (troop_get_slot, ":player_spouse", "trp_player", slot_troop_spouse),
	   (assign, "$g_player_minister", ":player_spouse"),
	   (jump_to_menu, "mnu_minister_confirm"),
	   ]),
	  ##diplomacy end+

	  ##diplomacy start+
	  #Check for one additional spouse (polygamy may be enabled)
      ("dplmc_appoint_spouse_plus_1",[
	  (troop_slot_ge, "trp_player", slot_troop_spouse, 1),
	  (assign, ":player_spouse", -1),
	  (try_for_range_backwards, ":troop_no", heroes_begin, heroes_end),#Go backwards to ensure we end with the first match
		(troop_slot_eq, ":troop_no", slot_troop_spouse, "trp_player"),
		(neg|troop_slot_eq, "trp_player", slot_troop_spouse, ":troop_no"),#Not ordinary spouse
		(neg|troop_slot_ge, ":troop_no", slot_troop_occupation, slto_retirement),#Not retired/dead/exiled
		(neg|troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),#Not leading a party
		(assign, ":player_spouse", ":troop_no"),
	  (try_end),
	  (ge, ":player_spouse", 1),
	  (call_script, "script_dplmc_store_troop_is_female", ":player_spouse"),
	  (str_store_troop_name, s10, ":player_spouse"),
	  ],"Appoint your {reg0?wife:husband}, {s10}...",
       [
	   (assign, ":player_spouse", -1),
	   (try_for_range_backwards, ":troop_no", heroes_begin, heroes_end),#Go backwards to ensure we end with the first match
	     (troop_slot_eq, ":troop_no", slot_troop_spouse, "trp_player"),
		 (neg|troop_slot_eq, "trp_player", slot_troop_spouse, ":troop_no"),#Not ordinary spouse
		 (neg|troop_slot_ge, ":troop_no", slot_troop_occupation, slto_retirement),#Not retired/dead/exiled
		 (neg|troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),#Not leading a party
		 (assign, ":player_spouse", ":troop_no"),
	   (try_end),
	   (try_begin),
		  (lt, ":player_spouse", 1),#This shouldn't be possible
		  (troop_get_slot, ":player_spouse", "trp_player", slot_troop_spouse),
	   (try_end),

	   (assign, "$g_player_minister", ":player_spouse"),
	   (jump_to_menu, "mnu_minister_confirm"),
	   ]),
	  ##diplomacy end+

      ("appoint_npc1",[
	  (main_party_has_troop, "trp_npc1"),
	  (str_store_troop_name, s10, "trp_npc1"),
	  ],"Appoint {s10}",
       [
	   (assign, "$g_player_minister", "trp_npc1"),
	   (jump_to_menu, "mnu_minister_confirm"),
	   ]),
	   
      ("appoint_npc2",[
	  (main_party_has_troop, "trp_npc2"),
	  (str_store_troop_name, s10, "trp_npc2"),],"Appoint {s10}",
       [
	   (assign, "$g_player_minister", "trp_npc2"),
	   (jump_to_menu, "mnu_minister_confirm"),]),
	   
      ("appoint_npc3",[
	  (main_party_has_troop, "trp_npc3"),
	  (str_store_troop_name, s10, "trp_npc3"),
	  ],"Appoint {s10}",
       [
	   (assign, "$g_player_minister", "trp_npc3"),
	   (jump_to_menu, "mnu_minister_confirm"), ]),
	   
      ("appoint_npc4",[
	  (main_party_has_troop, "trp_npc4"),
	  (str_store_troop_name, s10, "trp_npc4"),
	  ],"Appoint {s10}",
       [
	   (assign, "$g_player_minister", "trp_npc4"),
	   (jump_to_menu, "mnu_minister_confirm"), ]),
	   
      ("appoint_npc5",[
	  (main_party_has_troop, "trp_npc5"),
	  (str_store_troop_name, s10, "trp_npc5"),
	  ],"Appoint {s10}",
       [
	   (assign, "$g_player_minister", "trp_npc5"),
	   (jump_to_menu, "mnu_minister_confirm"), ]),
	   
      ("appoint_npc6",[
	  (main_party_has_troop, "trp_npc6"),
	  (str_store_troop_name, s10, "trp_npc6"),
	  ],"Appoint {s10}",
       [
	   (assign, "$g_player_minister", "trp_npc6"),
	   (jump_to_menu, "mnu_minister_confirm"), ]),
	   
      ("appoint_npc7",[
	  (main_party_has_troop, "trp_npc7"),
	  (str_store_troop_name, s10, "trp_npc7"),
	  ],"Appoint {s10}",
       [
	   (assign, "$g_player_minister", "trp_npc7"),
	   (jump_to_menu, "mnu_minister_confirm"), ]),
	   
      ("appoint_npc8",[
	  (main_party_has_troop, "trp_npc8"),
	  (str_store_troop_name, s10, "trp_npc8"),
	  ],"Appoint {s10}",
       [
	   (assign, "$g_player_minister", "trp_npc8"),
	   (jump_to_menu, "mnu_minister_confirm"), ]),
	   
      ("appoint_npc9",[
	  (main_party_has_troop, "trp_npc9"),
	  (str_store_troop_name, s10, "trp_npc9"),
	  ],"Appoint {s10}",
       [
	   (assign, "$g_player_minister", "trp_npc9"),
	   (jump_to_menu, "mnu_minister_confirm"), ]),
	   
      ("appoint_npc10",[ #was npc9
	  (main_party_has_troop, "trp_npc10"),
	  (str_store_troop_name, s10, "trp_npc10"),
	  ],"Appoint {s10}",
       [
	   (assign, "$g_player_minister", "trp_npc10"),
	   (jump_to_menu, "mnu_minister_confirm"), ]),
	   
      ("appoint_npc11",[
	  (main_party_has_troop, "trp_npc11"),
	  (str_store_troop_name, s10, "trp_npc11"),
	  ],"Appoint {s10}",
       [
	   (assign, "$g_player_minister", "trp_npc11"),
	   (jump_to_menu, "mnu_minister_confirm"), ]),
	   
      ("appoint_npc12",[
	  (main_party_has_troop, "trp_npc12"),
	  (str_store_troop_name, s10, "trp_npc12"),
	  ],"Appoint {s10}",
       [
	   (assign, "$g_player_minister", "trp_npc12"),
	   (jump_to_menu, "mnu_minister_confirm"), ]),
	   
      ("appoint_npc13",[
	  (main_party_has_troop, "trp_npc13"),
	  (str_store_troop_name, s10, "trp_npc13"),
	  ],"Appoint {s10}",
       [
	   (assign, "$g_player_minister", "trp_npc13"),
	   (jump_to_menu, "mnu_minister_confirm"), ]),
	   
      ("appoint_npc14",[
	  (main_party_has_troop, "trp_npc14"),
	  (str_store_troop_name, s10, "trp_npc14"),
	  ],"Appoint {s10}",
       [
	   (assign, "$g_player_minister", "trp_npc14"),
	   (jump_to_menu, "mnu_minister_confirm"), ]),
	   
      ("appoint_npc15",[
	  (main_party_has_troop, "trp_npc15"),
	  (str_store_troop_name, s10, "trp_npc15"),
	  ],"Appoint {s10}",
       [
	   (assign, "$g_player_minister", "trp_npc15"),
	   (jump_to_menu, "mnu_minister_confirm"), ]),
	   
      ("appoint_npc16",[
	  (main_party_has_troop, "trp_npc16"),
	  (str_store_troop_name, s10, "trp_npc16"),
	  ],"Appoint {s10}",
       [
	   (assign, "$g_player_minister", "trp_npc16"),
	   (jump_to_menu, "mnu_minister_confirm"), ]),
	   
      ("appoint_npc17",[
	  (main_party_has_troop, "trp_npc17"),
	  (str_store_troop_name, s10, "trp_npc17"),
	  ],"Appoint {s10}",
       [
	   (assign, "$g_player_minister", "trp_npc17"),
	   (jump_to_menu, "mnu_minister_confirm"), ]),
	   
      ("appoint_npc18",[
	  (main_party_has_troop, "trp_npc18"),
	  (str_store_troop_name, s10, "trp_npc18"),
	  ],"Appoint {s10}",
       [
	   (assign, "$g_player_minister", "trp_npc18"),
	   (jump_to_menu, "mnu_minister_confirm"), ]),
	   
      ("appoint_npc19",[
	  (main_party_has_troop, "trp_npc19"),
	  (str_store_troop_name, s10, "trp_npc19"),
	  ],"Appoint {s10}",
       [
	   (assign, "$g_player_minister", "trp_npc19"),
	   (jump_to_menu, "mnu_minister_confirm"), ]),
	   
      ("appoint_npc20",[
	  (main_party_has_troop, "trp_npc20"),
	  (str_store_troop_name, s10, "trp_npc20"),
	  ],"Appoint {s10}",
       [
	   (assign, "$g_player_minister", "trp_npc20"),
	   (jump_to_menu, "mnu_minister_confirm"), ]),
	   
      ("appoint_npc21",[
	  (main_party_has_troop, "trp_npc21"),
	  (str_store_troop_name, s10, "trp_npc21"),
	  ],"Appoint {s10}",
       [
	   (assign, "$g_player_minister", "trp_npc21"),
	   (jump_to_menu, "mnu_minister_confirm"), ]),
	   
      ("appoint_npc22",[
	  (main_party_has_troop, "trp_npc22"),
	  (str_store_troop_name, s10, "trp_npc22"),
	  ],"Appoint {s10}",
       [
	   (assign, "$g_player_minister", "trp_npc22"),
	   (jump_to_menu, "mnu_minister_confirm"), ]),

      ("appoint_default",[],"Appoint a prominent citizen from the area...",
       [
	   (assign, "$g_player_minister", "trp_temporary_minister"),
	   (troop_set_faction, "trp_temporary_minister", "fac_player_supporters_faction"),
	   (jump_to_menu, "mnu_minister_confirm"),
        ]),				
     ]
  ),
  

  (
    "minister_confirm",0,
    "{s9}can be found at your court in {s12}. You should consult periodically, to avoid the accumulation of unresolved issues that may sap your authority...",
    "none",
    [
    (try_begin),
        (eq, "$players_kingdom_name_set", 1),
        (change_screen_return),
    (try_end),
	  
	(try_begin),
		(eq, "$g_player_minister", "trp_temporary_minister"),
		(str_store_string, s9, "str_your_new_minister_"),
	(else_try),	
		(str_store_troop_name, s10, "$g_player_minister"),
		(str_store_string, s9, "str_s10_is_your_new_minister_and_"),
	(try_end),
	
	(try_begin),
		(main_party_has_troop, "$g_player_minister"),
		(remove_member_from_party, "$g_player_minister", "p_main_party"),
	(try_end),
	],
    [
      ("continue",[],"Continue...",
       [
         (start_presentation, "prsnt_name_kingdom"),
        ]),
     ]
  ),
  
  
  
  
  (
  "notification_court_lost",0,
  "{s12}",
  "none",
  [
    (try_begin),
		(is_between, "$g_player_court", centers_begin, centers_end),
		(str_store_party_name, s10, "$g_player_court"),
		(str_store_party_name, s11, "$g_player_court"),
	(else_try),
		(str_store_string, s10, "str_your_previous_court_some_time_ago"),
		(str_store_string, s11, "str_your_previous_court_some_time_ago"),
	(try_end),	

	##diplomacy start+ Handle player is co-ruler of NPC kingdom
	(assign, ":alt_faction", "fac_player_supporters_faction"),
	(try_begin),
		(is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
		(call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", "$players_kingdom"),
		(ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
		(assign, ":alt_faction", "$players_kingdom"),
	(try_end),
	##diplomacy end+
	
	(assign, "$g_player_court", -1),
	(str_store_string, s14, "str_after_to_the_fall_of_s11_your_court_has_nowhere_to_go"),
	(try_begin),
		##diplomacy start+  Handle player is co-ruler of NPC kingdom
		(this_or_next|neg|is_between, ":alt_faction", npc_kingdoms_begin, npc_kingdoms_end),
			(neg|faction_slot_eq, ":alt_faction", slot_faction_state, sfs_active),
		##diplomacy end+
		(faction_slot_eq, "fac_player_supporters_faction", slot_faction_state, sfs_inactive),
		(str_store_string, s14, "str_as_you_no_longer_maintain_an_independent_kingdom_you_no_longer_maintain_a_court"),
	(try_end),
	
	(try_for_range, ":walled_center", walled_centers_begin, walled_centers_end),
		(eq, "$g_player_court", -1),
    ##diplomacy begin
    (neg|party_slot_eq, ":walled_center", slot_village_infested_by_bandits, "trp_peasant_woman"),
    ##diplomacy end
		(store_faction_of_party, ":walled_center_faction", ":walled_center"),
		##diplomacy start+ Handle player is co-ruler of NPC kingdom
		(this_or_next|eq, ":alt_faction", ":walled_center_faction"),
		##diplomacy end+
		(eq, ":walled_center_faction", "fac_player_supporters_faction"),
		(neg|party_slot_ge, ":walled_center", slot_town_lord, active_npcs_begin),
		
		(assign, "$g_player_court", ":walled_center"),
		(try_begin),
			(troop_get_slot, ":spouse", "trp_player", slot_troop_spouse),
			(is_between, ":spouse", kingdom_ladies_begin, kingdom_ladies_end),
			##diplomacy start+ Check that the spouse is not a hero, imprisoned (except by the player), or exiled/dead/etc.
			(neg|troop_slot_eq, ":spouse", slot_troop_occupation, slto_kingdom_hero),
			(neg|troop_slot_ge, ":spouse", slot_troop_occupation, slto_retirement),
			(neg|troop_slot_ge, ":spouse", slot_troop_prisoner_of_party, 1),
			##diplomacy end+
			(troop_set_slot, ":spouse", slot_troop_cur_center, "$g_player_court"),
			(str_store_party_name, s11, "$g_player_court"),
		(try_end),
		
		(str_store_string, s14, "str_due_to_the_fall_of_s10_your_court_has_been_relocated_to_s12"),
	(try_end),

	(try_for_range, ":walled_center", walled_centers_begin, walled_centers_end),
		(eq, "$g_player_court", -1),
		
		(store_faction_of_party, ":walled_center_faction", ":walled_center"),
		##diplomacy start+ Handle player is co-ruler of NPC kingdom
		(this_or_next|eq, ":alt_faction", ":walled_center_faction"),
		##diplomacy end+
		(eq, ":walled_center_faction", "fac_player_supporters_faction"),
		
		(assign, "$g_player_court", ":walled_center"),
		
		(try_begin),
			(troop_get_slot, ":spouse", "trp_player", slot_troop_spouse),
			(is_between, ":spouse", kingdom_ladies_begin, kingdom_ladies_end),
			##diplomacy start+ Check that the spouse is not a hero, imprisoned (except by the player), or exiled/dead/etc.
			(neg|troop_slot_eq, ":spouse", slot_troop_occupation, slto_kingdom_hero),
			(neg|troop_slot_ge, ":spouse", slot_troop_occupation, slto_retirement),
			(neg|troop_slot_ge, ":spouse", slot_troop_prisoner_of_party, 1),
			##diplomacy end+
			(troop_set_slot, ":spouse", slot_troop_cur_center, "$g_player_court"),
		(try_end),

		(party_get_slot, ":town_lord", ":walled_center", slot_town_lord),
		(str_store_party_name, s11, "$g_player_court"),
		(str_store_troop_name, s9, ":town_lord"),
		(str_store_string, s14, "str_after_to_the_fall_of_s10_your_faithful_vassal_s9_has_invited_your_court_to_s11_"),
	(try_end),
	
	(try_begin),
		##diplomacy start+  Handle player is co-ruler of NPC kingdom
		(this_or_next|neg|is_between, ":alt_faction", npc_kingdoms_begin, npc_kingdoms_end),
			(neg|faction_slot_eq, ":alt_faction", slot_faction_state, sfs_active),
		##diplomacy end+
		(faction_slot_eq, "fac_player_supporters_faction", slot_faction_state, sfs_inactive),
		(str_store_string, s14, "str_as_you_no_longer_maintain_an_independent_kingdom_you_no_longer_maintain_a_court"),
	(try_end),
	(str_store_string, s12, s14),
  ],
  [
      ("continue",[],"Continue...",[
	  (change_screen_return),
	  ]),
     ],
  ),
  
  
  
  (
    "notification_player_faction_deactive",0,
    "Your domain no longer holds any land.",
    "none",
    [
      (set_fixed_point_multiplier, 100),
      (position_set_x, pos0, 65),
      (position_set_y, pos0, 30),
      (position_set_z, pos0, 170),
      (set_game_menu_tableau_mesh, "tableau_faction_note_mesh_banner", "fac_player_supporters_faction", pos0),
      ],
    [
      ("continue",[],"Continue...",
       [
	   
	   (try_begin),
	   
	   
	   (try_end),
	   (assign, "$g_player_minister", -1),
	   (change_screen_return),
        ]),
     ]
  ),
  

  
  
  
  (
    "notification_player_wedding_day",mnf_scale_picture,
    "{s8} wishes to inform you that preparations for your wedding at {s10} have been complete, and that your presence is expected imminently .",
    "none",
    [
		(set_background_mesh, "mesh_pic_messenger"),
		(str_store_troop_name, s8, "$g_notification_menu_var1"),
		(str_store_party_name, s10, "$g_notification_menu_var2"),
      ],
    [
      ("continue",[],"Continue...",
       [(change_screen_return),
        ]),
     ]
  ),
  
  
  
  (
    "notification_player_kingdom_holds_feast",mnf_scale_picture,
    "{s11}",
    "none",
    [
		(set_background_mesh, "mesh_pic_messenger"),
		
		(str_store_troop_name, s8, "$g_notification_menu_var1"),
		(store_faction_of_troop, ":host_faction", "$g_notification_menu_var1"),
		(str_store_faction_name, s9, ":host_faction"),
		
#		(str_store_faction_name, s9, "$players_kingdom"),
		(str_store_party_name, s10, "$g_notification_menu_var2"),
		
		(str_clear, s12),
		(try_begin),
			(check_quest_active, "qst_wed_betrothed"),
			(quest_get_slot, ":giver_troop", "qst_wed_betrothed", slot_quest_giver_troop),
			(store_faction_of_troop, ":giver_troop_faction", ":giver_troop"),
			(eq, ":giver_troop_faction", "$players_kingdom"),
			(str_store_string, s12, "str_feast_wedding_opportunity"),
		(try_end),
		
		
		
		(str_store_string, s11, "str_s8_wishes_to_inform_you_that_the_lords_of_s9_will_be_gathering_for_a_feast_at_his_great_hall_in_s10_and_invites_you_to_be_part_of_this_august_assembly"),
		(try_begin),
			(eq, "$g_notification_menu_var1", 0),
			(str_store_string, s11, "str_the_great_lords_of_your_kingdom_plan_to_gather_at_your_hall_in_s10_for_a_feast"),
		(try_end),
		(str_store_string, s11, "@{!}{s11}{s12}"),
		
		(try_begin),
			(ge, "$cheat_mode", 1),
			(store_current_hours, ":hours_since_last_feast"),
			(faction_get_slot, ":last_feast_start_time", "$players_kingdom", slot_faction_last_feast_start_time),
			(val_sub, ":hours_since_last_feast", ":last_feast_start_time"),		
			(assign, reg4, ":hours_since_last_feast"),
			(display_message, "@{!}DEBUG -- Hours since last feast started: {reg4}"),
		(try_end),
		
      ],
    [
      ("continue",[],"Continue...",
       [(change_screen_return),
        ]),
     ]
  ),
  
  
  
  (
    "notification_center_under_siege",0,
    "{s1} has been besieged by {s2} of {s3}!",
    "none",
    [
      (str_store_party_name, s1, "$g_notification_menu_var1"),
      (str_store_troop_name, s2, "$g_notification_menu_var2"),
      (store_troop_faction, ":troop_faction", "$g_notification_menu_var2"),
      (str_store_faction_name, s3, ":troop_faction"),
      (set_fixed_point_multiplier, 100),
      (position_set_x, pos0, 62),
      (position_set_y, pos0, 30),
      (position_set_z, pos0, 170),
      (set_game_menu_tableau_mesh, "tableau_center_note_mesh", "$g_notification_menu_var1", pos0),
      ],
    [
      ("continue",[],"Continue...",
       [(change_screen_return),
        ]),
     ]
  ),
  

  (
    "notification_village_raided",0,
    "Enemies have Laid Waste to a Fief^^{s1} has been raided by {s2} of {s3}!",
    "none",
    [
      (str_store_party_name, s1, "$g_notification_menu_var1"),
      (str_store_troop_name, s2, "$g_notification_menu_var2"),
      (store_troop_faction, ":troop_faction", "$g_notification_menu_var2"),
      (str_store_faction_name, s3, ":troop_faction"),
      (set_fixed_point_multiplier, 100),
      (position_set_x, pos0, 62),
      (position_set_y, pos0, 30),
      (position_set_z, pos0, 170),
      (set_game_menu_tableau_mesh, "tableau_center_note_mesh", "$g_notification_menu_var1", pos0),
      ],
    [
      ("continue",[],"Continue...",
       [(change_screen_return),
        ]),
     ]
  ),
  

  (
    "notification_village_raid_started",0,
    "Your Village is under Attack!^^{s2} of {s3} is laying waste to {s1}.",
    "none",
    [
      (str_store_party_name, s1, "$g_notification_menu_var1"),
      (str_store_troop_name, s2, "$g_notification_menu_var2"),
      (store_troop_faction, ":troop_faction", "$g_notification_menu_var2"),
      (str_store_faction_name, s3, ":troop_faction"),
      (set_fixed_point_multiplier, 100),
      (position_set_x, pos0, 62),
      (position_set_y, pos0, 30),
      (position_set_z, pos0, 170),
      (set_game_menu_tableau_mesh, "tableau_center_note_mesh", "$g_notification_menu_var1", pos0),
      ],
    [
      ("continue",[],"Continue...",
       [(change_screen_return),
        ]),
     ]
  ),
  (
    "notification_one_faction_left",0,
    "Japan Conquered by One Clan^^{s1} has defeated all rivals and stands as the new shogunate.",
    "none",
    [
      (str_store_faction_name, s1, "$g_notification_menu_var1"),
      (set_fixed_point_multiplier, 100),
      (position_set_x, pos0, 65),
      (position_set_y, pos0, 30),
      (position_set_z, pos0, 170),
      (try_begin),
        (is_between, "$g_notification_menu_var1", "fac_kingdom_1", kingdoms_end), #Excluding player kingdom
        (set_game_menu_tableau_mesh, "tableau_faction_note_mesh_for_menu", "$g_notification_menu_var1", pos0),
      (else_try),
        (set_game_menu_tableau_mesh, "tableau_faction_note_mesh_banner", "$g_notification_menu_var1", pos0),
      (try_end),
	  (try_begin),
		(faction_slot_eq, "$g_notification_menu_var1", slot_faction_leader, "trp_player"),
		(unlock_achievement, ACHIEVEMENT_THE_GOLDEN_THRONE),
	  (else_try),
		(unlock_achievement, ACHIEVEMENT_MANIFEST_DESTINY),
	  (try_end),

        (try_begin),
            (troop_get_type, ":is_female", "trp_player"),
            (eq, ":is_female", 1),
            (unlock_achievement, ACHIEVEMENT_EMPRESS),
        (try_end),	  
      ],
    [
      ("continue",[],"Continue...",
       [(change_screen_return),
        ]),
     ]
  ),
  
  (
    "notification_oath_renounced_faction_defeated",0,
    "Your Old Faction was Defeated^^You won the battle against {s1}! This ends your struggle which started after you renounced your oath to them.",
    "none",
    [
      (str_store_faction_name, s1, "$g_notification_menu_var1"),
      (set_fixed_point_multiplier, 100),
      (position_set_x, pos0, 65),
      (position_set_y, pos0, 30),
      (position_set_z, pos0, 170),
      (try_begin),
        (is_between, "$g_notification_menu_var1", "fac_kingdom_1", kingdoms_end), #Excluding player kingdom
        (set_game_menu_tableau_mesh, "tableau_faction_note_mesh_for_menu", "$g_notification_menu_var1", pos0),
      (else_try),
        (set_game_menu_tableau_mesh, "tableau_faction_note_mesh_banner", "$g_notification_menu_var1", pos0),
      (try_end),
      ],
    [
      ("continue",[],"Continue...",
       [(change_screen_return),
        ]),
     ]
  ),
  (
    "notification_center_lost",0,
    "An Estate was Lost^^You have lost {s1} to {s2}.",
    "none",
    [
      (str_store_party_name, s1, "$g_notification_menu_var1"),
      (str_store_faction_name, s2, "$g_notification_menu_var2"),
      (set_fixed_point_multiplier, 100),
      (position_set_x, pos0, 62),
      (position_set_y, pos0, 30),
      (position_set_z, pos0, 170),
      (set_game_menu_tableau_mesh, "tableau_center_note_mesh", "$g_notification_menu_var1", pos0),
      ],
    [
      ("continue",[],"Continue...",
       [(change_screen_return),
        ]),
     ]
  ),
  (
    "notification_troop_left_players_faction",0,
    "Betrayal!^^{s1} has left {s2} and joined {s3}.",
    "none",
    [
      (str_store_troop_name, s1, "$g_notification_menu_var1"),
      (str_store_faction_name, s2, "$players_kingdom"),
      (str_store_faction_name, s3, "$g_notification_menu_var2"),
      (set_fixed_point_multiplier, 100),
      (position_set_x, pos0, 55),
      (position_set_y, pos0, 20),
      (position_set_z, pos0, 100),
      (set_game_menu_tableau_mesh, "tableau_troop_note_mesh", "$g_notification_menu_var1", pos0),
      ],
    [
      ("continue",[],"Continue...",
       [(change_screen_return),
        ]),
     ]
  ),
  (
    "notification_troop_joined_players_faction",0,
    "Good news!^^ {s1} has left {s2} and joined {s3}.",
    "none",
    [
      (str_store_troop_name, s1, "$g_notification_menu_var1"),
      (str_store_faction_name, s2, "$g_notification_menu_var2"),
      (str_store_faction_name, s3, "$players_kingdom"),
      (set_fixed_point_multiplier, 100),
      (position_set_x, pos0, 55),
      (position_set_y, pos0, 20),
      (position_set_z, pos0, 100),
      (set_game_menu_tableau_mesh, "tableau_troop_note_mesh", "$g_notification_menu_var1", pos0),
      ],
    [
      ("continue",[],"Continue...",
       [(change_screen_return),
        ]),
     ]
  ),
  (
    "notification_war_declared",0,
    "Declaration of War^^{s1} has declared war against {s2}!",
    "none",
    [

#	  (try_begin),
#		(eq, "$g_include_diplo_explanation", "$g_notification_menu_var1"),
#		(assign, "$g_include_diplo_explanation", 0),
#		(str_store_string, s57, "$g_notification_menu_var1"),
#	  (else_try),
#	    (str_clear, s57),
#	  (try_end),

	
	#to do the reason, have war_damage = 0 yield pre-war reasons
      (try_begin),
#        (eq, "$g_notification_menu_var1", "fac_player_supporters_faction"),
#        (str_store_faction_name, s1, "$g_notification_menu_var2"),
#        (str_store_string, s2, "@you"),
#      (else_try),
#        (eq, "$g_notification_menu_var2", "fac_player_supporters_faction"),
#        (str_store_faction_name, s1, "$g_notification_menu_var1"),
#        (str_store_string, s2, "@you"),
#      (else_try),
        (str_store_faction_name, s1, "$g_notification_menu_var1"),
        (str_store_faction_name, s2, "$g_notification_menu_var2"),
      (try_end),
	  
	  
      (set_fixed_point_multiplier, 100),
      (position_set_x, pos0, 65),
      (position_set_y, pos0, 30),
      (position_set_z, pos0, 170),
      (store_sub, ":faction_1", "$g_notification_menu_var1", kingdoms_begin),
      (store_sub, ":faction_2", "$g_notification_menu_var2", kingdoms_begin),
      (val_mul, ":faction_1", 128),
      (val_add, ":faction_1", ":faction_2"),
      (set_game_menu_tableau_mesh, "tableau_2_factions_mesh", ":faction_1", pos0),
      ],
    [
      ("continue",[],"Continue...",
       [(change_screen_return),
        ]),
     ]
  ),
  (
    "notification_peace_declared",0,
    "Peace Agreement^^{s1} and {s2} have made peace!^{s57}",
    "none",
    [

	  (try_begin),
		(eq, 1, 0), #Alas, this does not seem to work
		(eq, "$g_include_diplo_explanation", "$g_notification_menu_var1"),
		(assign, "$g_include_diplo_explanation", 0),
	  (else_try),
	    (str_clear, s57),
	  (try_end),
	
	  (str_store_faction_name, s1, "$g_notification_menu_var1"),
      (str_store_faction_name, s2, "$g_notification_menu_var2"),
      (set_fixed_point_multiplier, 100),
      (position_set_x, pos0, 65),
      (position_set_y, pos0, 30),
      (position_set_z, pos0, 170),
      (store_sub, ":faction_1", "$g_notification_menu_var1", kingdoms_begin),
      (store_sub, ":faction_2", "$g_notification_menu_var2", kingdoms_begin),
      (val_mul, ":faction_1", 128),
      (val_add, ":faction_1", ":faction_2"),
      (set_game_menu_tableau_mesh, "tableau_2_factions_mesh", ":faction_1", pos0),
      ],
    [
      ("continue",[],"Continue...",
       [(change_screen_return),
        ]),
     ]
  ),
  
  (
    "notification_faction_defeated",0,
    "Faction Eliminated^^{s1} is no more!",
    "none",
    [
      (str_store_faction_name, s1, "$g_notification_menu_var1"),
      (set_fixed_point_multiplier, 100),
      (position_set_x, pos0, 65),
      (position_set_y, pos0, 30),
      (position_set_z, pos0, 170),
      (try_begin),
        (is_between, "$g_notification_menu_var1", "fac_kingdom_1", kingdoms_end), #Excluding player kingdom
        (set_game_menu_tableau_mesh, "tableau_faction_note_mesh_for_menu", "$g_notification_menu_var1", pos0),
      (else_try),
        (set_game_menu_tableau_mesh, "tableau_faction_note_mesh_banner", "$g_notification_menu_var1", pos0),
      (try_end),
      ],
    [
      ("continue",[],"Continue...",
       [
         (try_begin),
           (is_between, "$supported_pretender", pretenders_begin, pretenders_end),
           (troop_slot_eq, "$supported_pretender", slot_troop_original_faction, "$g_notification_menu_var1"),
		   
		   #All rebels switch to kingdom
           (try_for_range, ":cur_troop", active_npcs_begin, active_npcs_end),
		     (troop_slot_eq, ":cur_troop", slot_troop_occupation, slto_kingdom_hero),
             (store_troop_faction, ":cur_faction", ":cur_troop"),
             (eq, ":cur_faction", "fac_player_supporters_faction"),
             (troop_set_faction, ":cur_troop", "$g_notification_menu_var1"),
             (call_script, "script_troop_set_title_according_to_faction", ":cur_troop", "$g_notification_menu_var1"),
             (try_begin),
               (this_or_next|eq, "$g_notification_menu_var1", "$players_kingdom"),
               (eq, "$g_notification_menu_var1", "fac_player_supporters_faction"),
               (call_script, "script_check_concilio_calradi_achievement"),
             (try_end),
		   (else_try), #all loyal lords gain a small bonus with the player	 
		     (troop_slot_eq, ":cur_troop", slot_troop_occupation, slto_kingdom_hero),
             (store_troop_faction, ":cur_faction", ":cur_troop"),
             (eq, ":cur_faction", "$g_notification_menu_var1"),
			 (call_script, "script_troop_change_relation_with_troop", ":cur_troop", "trp_player", 5),
           (try_end),
		   
           (try_for_parties, ":cur_party"),
             (store_faction_of_party, ":cur_faction", ":cur_party"),
             (eq, ":cur_faction", "fac_player_supporters_faction"),
             (party_set_faction, ":cur_party", "$g_notification_menu_var1"),
           (try_end),
		   
           (assign, "$players_kingdom", "$g_notification_menu_var1"),
		   (try_begin),
			(troop_get_slot, ":spouse", "trp_player", slot_troop_spouse),
			(is_between, ":spouse", kingdom_ladies_begin, kingdom_ladies_end),
			(troop_set_faction, ":spouse", "$g_notification_menu_var1"),
		   (try_end),
		   
		   #gekokujo 3.0 rebellion rename and rebanner factions start
		   (try_begin),
			(eq, "$supported_pretender", "trp_kingdom_1_pretender"),
			#remains Uesugi clan
			(faction_set_slot, "$g_notification_menu_var1", slot_faction_banner, "mesh_banner_h06"),
		   (else_try),
			(eq, "$supported_pretender", "trp_kingdom_2_pretender"),
			(faction_set_name, "$g_notification_menu_var1", "@Ashina Clan"),
			(faction_set_slot, "$g_notification_menu_var1", slot_faction_banner, "mesh_banner_h07"),
            #gekokujo 3.1 rebellion rename troops start
			(troop_set_name, "trp_gekokujo_date_spearman", "@Ashina Spearman"),
			(troop_set_name, "trp_gekokujo_date_skirmisher", "@Ashina Skirmisher"),
			(troop_set_name, "trp_gekokujo_date_trained_spearman", "@Ashina Trained Spearman"),
			(troop_set_name, "trp_gekokujo_date_trained_skirmisher", "@Ashina Trained Skirmisher"),
			(troop_set_name, "trp_gekokujo_date_veteran_spearman", "@Ashina Veteran Spearman"),
			(troop_set_name, "trp_gekokujo_date_veteran_skirmisher", "@Ashina Veteran Skirmisher"),
			(troop_set_name, "trp_gekokujo_date_elite_spearman", "@Ashina Elite Spearman*"),

			(troop_set_name, "trp_gekokujo_date_retainer", "@Ashina Retainer"),
			(troop_set_name, "trp_gekokujo_date_marksman", "@Ashina Marksman"),
			(troop_set_name, "trp_gekokujo_date_veteran_retainer", "@Ashina Veteran Retainer"),
			(troop_set_name, "trp_gekokujo_date_mounted_retainer", "@Ashina Mounted Retainer"),
			(troop_set_name, "trp_gekokujo_date_samurai_gunner", "@Ashina Samurai Gunner"),
			(troop_set_name, "trp_gekokujo_date_samurai_archer", "@Ashina Samurai Archer"),
			(troop_set_name, "trp_gekokujo_date_officer", "@Ashina Officer"),
			(troop_set_name, "trp_gekokujo_date_mounted_officer", "@Ashina Mounted Officer"),
			(troop_set_name, "trp_gekokujo_date_master_gunner", "@Ashina Master Gunner"),
			(troop_set_name, "trp_gekokujo_date_master_archer", "@Ashina Master Archer"),
			(troop_set_name, "trp_gekokujo_date_hatamoto_guard", "@Ashina Hatamoto Guard"),
			(troop_set_name, "trp_gekokujo_date_hatamoto_cavalry", "@Ashina Hatamoto Cavalry"),
			(troop_set_name, "trp_gekokujo_date_messenger", "@Ashina Messenger"),
			(troop_set_name, "trp_gekokujo_date_deserter", "@Ashina Deserter"),
			(troop_set_name, "trp_gekokujo_date_prison_guard", "@Ashina Prison Guard"),
			(troop_set_name, "trp_gekokujo_date_castle_guard", "@Ashina Castle Guard"),
            
			(troop_set_plural_name, "trp_gekokujo_date_spearman", "@Ashina Spearmen"),
			(troop_set_plural_name, "trp_gekokujo_date_skirmisher", "@Ashina Skirmishers"),
			(troop_set_plural_name, "trp_gekokujo_date_trained_spearman", "@Ashina Trained Spearmen"),
			(troop_set_plural_name, "trp_gekokujo_date_trained_skirmisher", "@Ashina Trained Skirmishers"),
			(troop_set_plural_name, "trp_gekokujo_date_veteran_spearman", "@Ashina Veteran Spearmen"),
			(troop_set_plural_name, "trp_gekokujo_date_veteran_skirmisher", "@Ashina Veteran Skirmishers"),
			(troop_set_plural_name, "trp_gekokujo_date_elite_spearman", "@Ashina Elite Spearmen"),

			(troop_set_plural_name, "trp_gekokujo_date_retainer", "@Ashina Retainers"),
			(troop_set_plural_name, "trp_gekokujo_date_marksman", "@Ashina Marksmen"),
			(troop_set_plural_name, "trp_gekokujo_date_veteran_retainer", "@Ashina Veteran Retainers"),
			(troop_set_plural_name, "trp_gekokujo_date_mounted_retainer", "@Ashina Mounted Retainers"),
			(troop_set_plural_name, "trp_gekokujo_date_samurai_gunner", "@Ashina Samurai Gunners"),
			(troop_set_plural_name, "trp_gekokujo_date_samurai_archer", "@Ashina Samurai Archers"),
			(troop_set_plural_name, "trp_gekokujo_date_officer", "@Ashina Officers"),
			(troop_set_plural_name, "trp_gekokujo_date_mounted_officer", "@Ashina Mounted Officers"),
			(troop_set_plural_name, "trp_gekokujo_date_master_gunner", "@Ashina Master Gunners"),
			(troop_set_plural_name, "trp_gekokujo_date_master_archer", "@Ashina Master Archers"),
			(troop_set_plural_name, "trp_gekokujo_date_hatamoto_guard", "@Ashina Hatamoto Guards"),
			(troop_set_plural_name, "trp_gekokujo_date_hatamoto_cavalry", "@Ashina Hatamoto Cavalry"),
			(troop_set_plural_name, "trp_gekokujo_date_messenger", "@Ashina Messengers"),
			(troop_set_plural_name, "trp_gekokujo_date_deserter", "@Ashina Deserters"),
			(troop_set_plural_name, "trp_gekokujo_date_prison_guard", "@Ashina Prison Guards"),
			(troop_set_plural_name, "trp_gekokujo_date_castle_guard", "@Ashina Castle Guards"),
			#gekokujo 3.1 rebellion rename troops end
		   (else_try),
			(eq, "$supported_pretender", "trp_kingdom_3_pretender"),
			(faction_set_name, "$g_notification_menu_var1", "@Saito Clan"),
			(faction_set_slot, "$g_notification_menu_var1", slot_faction_banner, "mesh_banner_h08"),
            #gekokujo 3.1 rebellion rename troops start
			(troop_set_name, "trp_gekokujo_oda_spearman", "@Saito Spearman"),
			(troop_set_name, "trp_gekokujo_oda_skirmisher", "@Saito Skirmisher"),
			(troop_set_name, "trp_gekokujo_oda_trained_spearman", "@Saito Trained Spearman"),
			(troop_set_name, "trp_gekokujo_oda_trained_skirmisher", "@Saito Trained Skirmisher"),
			(troop_set_name, "trp_gekokujo_oda_veteran_spearman", "@Saito Veteran Spearman"),
			(troop_set_name, "trp_gekokujo_oda_veteran_skirmisher", "@Saito Veteran Skirmisher"),
			(troop_set_name, "trp_gekokujo_oda_elite_skirmisher", "@Saito Elite Skirmisher"),

			(troop_set_name, "trp_gekokujo_oda_retainer", "@Saito Retainer"),
			(troop_set_name, "trp_gekokujo_oda_marksman", "@Saito Marksman"),
			(troop_set_name, "trp_gekokujo_oda_veteran_retainer", "@Saito Veteran Retainer"),
			(troop_set_name, "trp_gekokujo_oda_mounted_retainer", "@Saito Mounted Retainer"),
			(troop_set_name, "trp_gekokujo_oda_samurai_gunner", "@Saito Samurai Gunner"),
			(troop_set_name, "trp_gekokujo_oda_samurai_archer", "@Saito Samurai Archer"),
			(troop_set_name, "trp_gekokujo_oda_officer", "@Saito Officer"),
			(troop_set_name, "trp_gekokujo_oda_mounted_officer", "@Saito Mounted Officer"),
			(troop_set_name, "trp_gekokujo_oda_master_gunner", "@Saito Master Gunner"),
			(troop_set_name, "trp_gekokujo_oda_master_archer", "@Saito Master Archer"),
			(troop_set_name, "trp_gekokujo_oda_hatamoto_cavalry", "@Saito Hatamoto Cavalry"),
			(troop_set_name, "trp_gekokujo_oda_hatamoto_gunner", "@Saito Hatamoto Gunner"),
			(troop_set_name, "trp_gekokujo_oda_messenger", "@Saito Messenger"),
			(troop_set_name, "trp_gekokujo_oda_deserter", "@Saito Deserter"),
			(troop_set_name, "trp_gekokujo_oda_prison_guard", "@Saito Prison Guard"),
			(troop_set_name, "trp_gekokujo_oda_castle_guard", "@Saito Castle Guard"),
            
			(troop_set_plural_name, "trp_gekokujo_oda_spearman", "@Saito Spearmen"),
			(troop_set_plural_name, "trp_gekokujo_oda_skirmisher", "@Saito Skirmishers"),
			(troop_set_plural_name, "trp_gekokujo_oda_trained_spearman", "@Saito Trained Spearmen"),
			(troop_set_plural_name, "trp_gekokujo_oda_trained_skirmisher", "@Saito Trained Skirmishers"),
			(troop_set_plural_name, "trp_gekokujo_oda_veteran_spearman", "@Saito Veteran Spearmen"),
			(troop_set_plural_name, "trp_gekokujo_oda_veteran_skirmisher", "@Saito Veteran Skirmishers"),
			(troop_set_plural_name, "trp_gekokujo_oda_elite_skirmisher", "@Saito Elite Skirmishers"),

			(troop_set_plural_name, "trp_gekokujo_oda_retainer", "@Saito Retainers"),
			(troop_set_plural_name, "trp_gekokujo_oda_marksman", "@Saito Marksmen"),
			(troop_set_plural_name, "trp_gekokujo_oda_veteran_retainer", "@Saito Veteran Retainers"),
			(troop_set_plural_name, "trp_gekokujo_oda_mounted_retainer", "@Saito Mounted Retainers"),
			(troop_set_plural_name, "trp_gekokujo_oda_samurai_gunner", "@Saito Samurai Gunners"),
			(troop_set_plural_name, "trp_gekokujo_oda_samurai_archer", "@Saito Samurai Archers"),
			(troop_set_plural_name, "trp_gekokujo_oda_officer", "@Saito Officers"),
			(troop_set_plural_name, "trp_gekokujo_oda_mounted_officer", "@Saito Mounted Officers"),
			(troop_set_plural_name, "trp_gekokujo_oda_master_gunner", "@Saito Master Gunners"),
			(troop_set_plural_name, "trp_gekokujo_oda_master_archer", "@Saito Master Archers"),
			(troop_set_plural_name, "trp_gekokujo_oda_hatamoto_cavalry", "@Saito Hatamoto Cavalry"),
			(troop_set_plural_name, "trp_gekokujo_oda_hatamoto_gunner", "@Saito Hatamoto Gunners"),
			(troop_set_plural_name, "trp_gekokujo_oda_messenger", "@Saito Messengers"),
			(troop_set_plural_name, "trp_gekokujo_oda_deserter", "@Saito Deserters"),
			(troop_set_plural_name, "trp_gekokujo_oda_prison_guard", "@Saito Prison Guards"),
			(troop_set_plural_name, "trp_gekokujo_oda_castle_guard", "@Saito Castle Guards"),
			#gekokujo 3.1 rebellion rename troops end
		   (else_try),
			(eq, "$supported_pretender", "trp_kingdom_4_pretender"),
			(faction_set_name, "$g_notification_menu_var1", "@Ouchi Clan"),
			(faction_set_slot, "$g_notification_menu_var1", slot_faction_banner, "mesh_banner_h09"),
            #gekokujo 3.1 rebellion rename troops start
			(troop_set_name, "trp_gekokujo_mori_spearman", "@Ouchi Spearman"),
			(troop_set_name, "trp_gekokujo_mori_skirmisher", "@Ouchi Skirmisher"),
			(troop_set_name, "trp_gekokujo_mori_trained_spearman", "@Ouchi Trained Spearman"),
			(troop_set_name, "trp_gekokujo_mori_trained_skirmisher", "@Ouchi Trained Skirmisher"),
			(troop_set_name, "trp_gekokujo_mori_veteran_spearman", "@Ouchi Veteran Spearman"),
			(troop_set_name, "trp_gekokujo_mori_veteran_skirmisher", "@Ouchi Veteran Skirmisher"),
			(troop_set_name, "trp_gekokujo_mori_elite_spearman", "@Ouchi Elite Spearman"),

			(troop_set_name, "trp_gekokujo_mori_retainer", "@Ouchi Retainer"),
			(troop_set_name, "trp_gekokujo_mori_marksman", "@Ouchi Marksman"),
			(troop_set_name, "trp_gekokujo_mori_veteran_retainer", "@Ouchi Veteran Retainer"),
			(troop_set_name, "trp_gekokujo_mori_mounted_retainer", "@Ouchi Mounted Retainer"),
			(troop_set_name, "trp_gekokujo_mori_samurai_gunner", "@Ouchi Samurai Gunner"),
			(troop_set_name, "trp_gekokujo_mori_samurai_archer", "@Ouchi Samurai Archer"),
			(troop_set_name, "trp_gekokujo_mori_officer", "@Ouchi Officer"),
			(troop_set_name, "trp_gekokujo_mori_mounted_officer", "@Ouchi Mounted Officer"),
			(troop_set_name, "trp_gekokujo_mori_master_gunner", "@Ouchi Master Gunner"),
			(troop_set_name, "trp_gekokujo_mori_master_archer", "@Ouchi Master Archer"),
			(troop_set_name, "trp_gekokujo_mori_hatamoto_guard", "@Ouchi Hatamoto Guard"),
			(troop_set_name, "trp_gekokujo_mori_hatamoto_cavalry", "@Ouchi Hatamoto Cavalry"),
			(troop_set_name, "trp_gekokujo_mori_messenger", "@Ouchi Messenger"),
			(troop_set_name, "trp_gekokujo_mori_deserter", "@Ouchi Deserter"),
			(troop_set_name, "trp_gekokujo_mori_prison_guard", "@Ouchi Prison Guard"),
			(troop_set_name, "trp_gekokujo_mori_castle_guard", "@Ouchi Castle Guard"),
            
			(troop_set_plural_name, "trp_gekokujo_mori_spearman", "@Ouchi Spearmen"),
			(troop_set_plural_name, "trp_gekokujo_mori_skirmisher", "@Ouchi Skirmishers"),
			(troop_set_plural_name, "trp_gekokujo_mori_trained_spearman", "@Ouchi Trained Spearmen"),
			(troop_set_plural_name, "trp_gekokujo_mori_trained_skirmisher", "@Ouchi Trained Skirmishers"),
			(troop_set_plural_name, "trp_gekokujo_mori_veteran_spearman", "@Ouchi Veteran Spearmen"),
			(troop_set_plural_name, "trp_gekokujo_mori_veteran_skirmisher", "@Ouchi Veteran Skirmishers"),
			(troop_set_plural_name, "trp_gekokujo_mori_elite_spearman", "@Ouchi Elite Spearmen"),

			(troop_set_plural_name, "trp_gekokujo_mori_retainer", "@Ouchi Retainers"),
			(troop_set_plural_name, "trp_gekokujo_mori_marksman", "@Ouchi Marksmen"),
			(troop_set_plural_name, "trp_gekokujo_mori_veteran_retainer", "@Ouchi Veteran Retainers"),
			(troop_set_plural_name, "trp_gekokujo_mori_mounted_retainer", "@Ouchi Mounted Retainers"),
			(troop_set_plural_name, "trp_gekokujo_mori_samurai_gunner", "@Ouchi Samurai Gunners"),
			(troop_set_plural_name, "trp_gekokujo_mori_samurai_archer", "@Ouchi Samurai Archers"),
			(troop_set_plural_name, "trp_gekokujo_mori_officer", "@Ouchi Officers"),
			(troop_set_plural_name, "trp_gekokujo_mori_mounted_officer", "@Ouchi Mounted Officers"),
			(troop_set_plural_name, "trp_gekokujo_mori_master_gunner", "@Ouchi Master Gunners"),
			(troop_set_plural_name, "trp_gekokujo_mori_master_archer", "@Ouchi Master Archers"),
			(troop_set_plural_name, "trp_gekokujo_mori_hatamoto_guard", "@Ouchi Hatamoto Guards"),
			(troop_set_plural_name, "trp_gekokujo_mori_hatamoto_cavalry", "@Ouchi Hatamoto Cavalry"),
			(troop_set_plural_name, "trp_gekokujo_mori_messenger", "@Ouchi Messengers"),
			(troop_set_plural_name, "trp_gekokujo_mori_deserter", "@Ouchi Deserters"),
			(troop_set_plural_name, "trp_gekokujo_mori_prison_guard", "@Ouchi Prison Guards"),
			(troop_set_plural_name, "trp_gekokujo_mori_castle_guard", "@Ouchi Castle Guards"),
			#gekokujo 3.1 rebellion rename troops end
		   (else_try),
			(eq, "$supported_pretender", "trp_kingdom_5_pretender"),
			#remains Takeda clan
			(faction_set_slot, "$g_notification_menu_var1", slot_faction_banner, "mesh_banner_g13"),
		   (else_try),
			(eq, "$supported_pretender", "trp_kingdom_6_pretender"),
			(faction_set_name, "$g_notification_menu_var1", "@Imagawa Clan"),
			(faction_set_slot, "$g_notification_menu_var1", slot_faction_banner, "mesh_banner_g12"),
            #gekokujo 3.1 rebellion rename troops start
			(troop_set_name, "trp_gekokujo_tokugawa_spearman", "@Imagawa Spearman"),
			(troop_set_name, "trp_gekokujo_tokugawa_skirmisher", "@Imagawa Skirmisher"),
			(troop_set_name, "trp_gekokujo_tokugawa_trained_spearman", "@Imagawa Trained Spearman"),
			(troop_set_name, "trp_gekokujo_tokugawa_trained_skirmisher", "@Imagawa Trained Skirmisher"),
			(troop_set_name, "trp_gekokujo_tokugawa_veteran_spearman", "@Imagawa Veteran Spearman"),
			(troop_set_name, "trp_gekokujo_tokugawa_veteran_skirmisher", "@Imagawa Veteran Skirmisher"),
			(troop_set_name, "trp_gekokujo_tokugawa_elite_skirmisher", "@Imagawa Elite Skirmisher"),

			(troop_set_name, "trp_gekokujo_tokugawa_retainer", "@Imagawa Retainer"),
			(troop_set_name, "trp_gekokujo_tokugawa_marksman", "@Imagawa Marksman"),
			(troop_set_name, "trp_gekokujo_tokugawa_veteran_retainer", "@Imagawa Veteran Retainer"),
			(troop_set_name, "trp_gekokujo_tokugawa_mounted_retainer", "@Imagawa Mounted Retainer"),
			(troop_set_name, "trp_gekokujo_tokugawa_samurai_gunner", "@Imagawa Samurai Gunner"),
			(troop_set_name, "trp_gekokujo_tokugawa_samurai_archer", "@Imagawa Samurai Archer"),
			(troop_set_name, "trp_gekokujo_tokugawa_officer", "@Imagawa Officer"),
			(troop_set_name, "trp_gekokujo_tokugawa_mounted_officer", "@Imagawa Mounted Officer"),
			(troop_set_name, "trp_gekokujo_tokugawa_master_gunner", "@Imagawa Master Gunner"),
			(troop_set_name, "trp_gekokujo_tokugawa_master_archer", "@Imagawa Master Archer"),
			(troop_set_name, "trp_gekokujo_tokugawa_hatamoto_guard", "@Imagawa Hatamoto Guard"),
			(troop_set_name, "trp_gekokujo_tokugawa_hatamoto_gunner", "@Imagawa Hatamoto Gunner"),
			(troop_set_name, "trp_gekokujo_tokugawa_messenger", "@Imagawa Messenger"),
			(troop_set_name, "trp_gekokujo_tokugawa_deserter", "@Imagawa Deserter"),
			(troop_set_name, "trp_gekokujo_tokugawa_prison_guard", "@Imagawa Prison Guard"),
			(troop_set_name, "trp_gekokujo_tokugawa_castle_guard", "@Imagawa Castle Guard"),
            
			(troop_set_plural_name, "trp_gekokujo_tokugawa_spearman", "@Imagawa Spearmen"),
			(troop_set_plural_name, "trp_gekokujo_tokugawa_skirmisher", "@Imagawa Skirmishers"),
			(troop_set_plural_name, "trp_gekokujo_tokugawa_trained_spearman", "@Imagawa Trained Spearmen"),
			(troop_set_plural_name, "trp_gekokujo_tokugawa_trained_skirmisher", "@Imagawa Trained Skirmishers"),
			(troop_set_plural_name, "trp_gekokujo_tokugawa_veteran_spearman", "@Imagawa Veteran Spearmen"),
			(troop_set_plural_name, "trp_gekokujo_tokugawa_veteran_skirmisher", "@Imagawa Veteran Skirmishers"),
			(troop_set_plural_name, "trp_gekokujo_tokugawa_elite_skirmisher", "@Imagawa Elite Skirmisher"),

			(troop_set_plural_name, "trp_gekokujo_tokugawa_retainer", "@Imagawa Retainers"),
			(troop_set_plural_name, "trp_gekokujo_tokugawa_marksman", "@Imagawa Marksmen"),
			(troop_set_plural_name, "trp_gekokujo_tokugawa_veteran_retainer", "@Imagawa Veteran Retainers"),
			(troop_set_plural_name, "trp_gekokujo_tokugawa_mounted_retainer", "@Imagawa Mounted Retainers"),
			(troop_set_plural_name, "trp_gekokujo_tokugawa_samurai_gunner", "@Imagawa Samurai Gunners"),
			(troop_set_plural_name, "trp_gekokujo_tokugawa_samurai_archer", "@Imagawa Samurai Archers"),
			(troop_set_plural_name, "trp_gekokujo_tokugawa_officer", "@Imagawa Officers"),
			(troop_set_plural_name, "trp_gekokujo_tokugawa_mounted_officer", "@Imagawa Mounted Officers"),
			(troop_set_plural_name, "trp_gekokujo_tokugawa_master_gunner", "@Imagawa Master Gunners"),
			(troop_set_plural_name, "trp_gekokujo_tokugawa_master_archer", "@Imagawa Master Archers"),
			(troop_set_plural_name, "trp_gekokujo_tokugawa_hatamoto_guard", "@Imagawa Hatamoto Guards"),
			(troop_set_plural_name, "trp_gekokujo_tokugawa_hatamoto_gunner", "@Imagawa Hatamoto Gunners"),
			(troop_set_plural_name, "trp_gekokujo_tokugawa_messenger", "@Imagawa Messengers"),
			(troop_set_plural_name, "trp_gekokujo_tokugawa_deserter", "@Imagawa Deserters"),
			(troop_set_plural_name, "trp_gekokujo_tokugawa_prison_guard", "@Imagawa Prison Guards"),
			(troop_set_plural_name, "trp_gekokujo_tokugawa_castle_guard", "@Imagawa Castle Guards"),
			#gekokujo 3.1 rebellion rename troops end
		   (try_end),
		   #gekokujo 3.0 rebellion rename and rebanner factions end
		   
		   #gekokujo 3.0 rebellion rename pretender start
		   (str_store_troop_name_plural, s9, "$supported_pretender"),
		   (str_store_string, s9, "@Great Lord {s9}"),
		   (troop_set_name, "$supported_pretender", s9),
		   #gekokujo 3.0 rebellion rename pretender end
		   
           (call_script, "script_add_notification_menu", "mnu_notification_rebels_switched_to_faction", "$g_notification_menu_var1", "$supported_pretender"),
		   
           (faction_set_slot, "$g_notification_menu_var1", slot_faction_state, sfs_active),
           (faction_set_slot, "fac_player_supporters_faction", slot_faction_state, sfs_inactive),
		   
           (faction_get_slot, ":old_leader", "$g_notification_menu_var1", slot_faction_leader),
           (troop_set_slot, ":old_leader", slot_troop_change_to_faction, "fac_commoners"),
		   
           (faction_set_slot, "$g_notification_menu_var1", slot_faction_leader, "$supported_pretender"),
           (troop_set_faction, "$supported_pretender", "$g_notification_menu_var1"),

           (faction_get_slot, ":old_marshall", "$g_notification_menu_var1", slot_faction_marshall),
           (try_begin),
             (ge, ":old_marshall", 0),
			 (troop_get_slot, ":old_marshall_party", ":old_marshall", slot_troop_leaded_party),
             (party_is_active, ":old_marshall_party"),
             (party_set_marshall, ":old_marshall_party", 0),
           (try_end),  

           (faction_set_slot, "$g_notification_menu_var1", slot_faction_marshall, "trp_player"),
           (faction_set_slot, "$g_notification_menu_var1", slot_faction_ai_state, sfai_default),
           (faction_set_slot, "$g_notification_menu_var1", slot_faction_ai_object, -1),
           (troop_set_slot, "$supported_pretender", slot_troop_occupation, slto_kingdom_hero),
		   (troop_set_slot, "$supported_pretender", slot_troop_renown, 1000),
		   
           (party_remove_members, "p_main_party", "$supported_pretender", 1),
           (call_script, "script_set_player_relation_with_faction", "$g_notification_menu_var1", 0),
           (try_for_range, ":cur_kingdom", kingdoms_begin, kingdoms_end),
             (faction_slot_eq, ":cur_kingdom", slot_faction_state, sfs_active),
             (neq, ":cur_kingdom", "$g_notification_menu_var1"),
             (store_relation, ":reln", ":cur_kingdom", "fac_player_supporters_faction"),
             (set_relation, ":cur_kingdom", "$g_notification_menu_var1", ":reln"),
           (try_end),
           (assign, "$supported_pretender", 0),
           (assign, "$supported_pretender_old_faction", 0),
           (assign, "$g_recalculate_ais", 1),
           (call_script, "script_update_all_notes"),
         (try_end),
         (change_screen_return),
        ]),
     ]
  ),
  
  (
    "notification_rebels_switched_to_faction",0,
    "Rebellion Success^^ Your rebellion is victorious! Your faction now has the sole claim to the title of {s11}, with {s12} as the single ruler.",
    "none",
    [
      (str_store_faction_name, s11, "$g_notification_menu_var1"),
      (str_store_troop_name, s12, "$g_notification_menu_var2"),
      (set_fixed_point_multiplier, 100),
      (position_set_x, pos0, 65),
      (position_set_y, pos0, 30),
      (position_set_z, pos0, 170),
      (try_begin),
        (is_between, "$g_notification_menu_var1", "fac_kingdom_1", kingdoms_end), #Excluding player kingdom
        (set_game_menu_tableau_mesh, "tableau_faction_note_mesh_for_menu", "$g_notification_menu_var1", pos0),
      (else_try),
        (set_game_menu_tableau_mesh, "tableau_faction_note_mesh_banner", "$g_notification_menu_var1", pos0),
      (try_end),
      ],
    [
      ("continue",[],"Continue...",
       [
         (assign, "$talk_context", tc_rebel_thanks),
         (start_map_conversation, "$g_notification_menu_var2", -1),
         (change_screen_return),
        ]),
     ]
  ),
  (
    "notification_player_should_consult",0,
##diplomacy start+ Replace "Your minister" with "{reg0?Your minister:{s11}}" and "him" with "{reg4?her:him}".
#Also "sends words" to "sends word"
    "{reg0?Your minister:{s11}} sends word that there are problems brewing in your domain which, if left untreated, could sap your authority. You should consult with {reg4?her:him} at your earliest convenience",
	##diplomacy end+
    "none",
    [
      ],
    [
      ("continue",[],"Continue...",
       [
	    (setup_quest_text, "qst_consult_with_minister"),

        (str_store_troop_name, s11, "$g_player_minister"),
        (str_store_party_name, s12, "$g_player_court"),
	   
		(str_store_string, s2, "str_consult_with_s11_at_your_court_in_s12"),
	    (call_script, "script_start_quest", "qst_consult_with_minister", -1),
		##diplomacy start+ Set minister gender and reg0 for generic vs specific
		(assign, reg4, 0),
		(try_begin),
			(call_script, "script_cf_dplmc_troop_is_female", "$g_player_minister"),
			(assign, reg4, 1),
		(try_end),
		(assign, reg0, 1),
		(try_begin),
			(is_between, "$g_player_minister", heroes_begin, heroes_end),
			(assign, reg0, 0),
		(try_end),
		##diplomacy end+
		
		
		(quest_set_slot, "qst_consult_with_minister", slot_quest_expiration_days, 30),
		(quest_set_slot, "qst_consult_with_minister", slot_quest_giver_troop, "$g_player_minister"),


	    (change_screen_return),
        ]),
     ]
  ),
  
  (
    "notification_player_feast_in_progress",0,
##diplomacy start+ make gender correct
    "Feast in Preparation^^Your {wife/husband} has started preparations for a feast in your hall in {s11}",
##diplomacy end+
    "none",
    [
    (str_store_party_name, s11, "$g_notification_menu_var1"),
    ],
    [
      ("continue",[],"Continue...",
       [(change_screen_return),
        ]),
     ]
  ),
  

  (
    "notification_lady_requests_visit",0, #add this once around seven days after the last visit, or three weeks, or three months
    "An elderly woman approaches your party and passes one of your men a letter, sealed in plain wax. It is addressed to you. When you break the seal, you see it is from {s15}. It reads, 'I so enjoyed your last visit. {s14} I am currently in {s10}.{s12}'",
    "none",
    [

	  (assign, ":lady_no", "$g_notification_menu_var1"),
	  (assign, ":center_no", "$g_notification_menu_var2"),

      (str_store_troop_name, s15, ":lady_no"),
      (str_store_party_name, s10, ":center_no"),
	  
	  (store_current_hours, ":hours_since_last_visit"),
	  (troop_get_slot, ":last_visit_hours", ":lady_no", slot_troop_last_talk_time),
	  (val_sub, ":hours_since_last_visit", ":last_visit_hours"),
	  
	  (call_script, "script_get_kingdom_lady_social_determinants", ":lady_no"),
	  (assign, ":lady_guardian", reg0),
	  
	  (str_store_troop_name, s16, ":lady_guardian"),
	  (call_script, "script_troop_get_family_relation_to_troop", ":lady_guardian", ":lady_no"),
	  
	  (str_clear, s14), 
	  (try_begin),
	    (lt, ":hours_since_last_visit", 336),
		(try_begin),
			(troop_slot_eq, ":lady_no", slot_lord_reputation_type, lrep_otherworldly),
			(str_store_string, s14, "str_as_brief_as_our_separation_has_been_the_longing_in_my_heart_to_see_you_has_made_it_seem_as_many_years"),
		(else_try),
			(str_store_string, s14, "str_although_it_has_only_been_a_short_time_since_your_departure_but_i_would_be_most_pleased_to_see_you_again"),
		(try_end),
	  (else_try),
	    (ge, ":hours_since_last_visit", 336),
		(try_begin),
			(troop_slot_eq, ":lady_no", slot_lord_reputation_type, lrep_ambitious),
			(str_store_string, s14, "str_although_i_have_received_no_word_from_you_for_quite_some_time_i_am_sure_that_you_must_have_been_very_busy_and_that_your_failure_to_come_see_me_in_no_way_indicates_that_your_attentions_to_me_were_insincere_"),
		(else_try),
			(troop_slot_eq, ":lady_no", slot_lord_reputation_type, lrep_moralist),
			(str_store_string, s14, "str_i_trust_that_you_have_comported_yourself_in_a_manner_becoming_a_gentleman_during_our_long_separation_"),
		(else_try),
			(str_store_string, s14, "str_it_has_been_many_days_since_you_came_and_i_would_very_much_like_to_see_you_again"),
	    (try_end),
	  (try_end),

	  
	  (str_clear, s12), 
	  (str_clear, s18),
	  ##diplomacy start+ Store gender in register for use below
	  (assign, ":save_reg4", reg4),
	  (call_script, "script_dplmc_store_troop_is_female_reg", ":lady_guardian", 4),
	  ##diplomacy end+
	  (try_begin),
	    (troop_slot_eq, ":lady_guardian", slot_lord_granted_courtship_permission, 0),
		(str_store_string, s12, "str__you_should_ask_my_s11_s16s_permission_but_i_have_no_reason_to_believe_that_he_will_prevent_you_from_coming_to_see_me"),
		(str_store_string, s18, "str__you_should_first_ask_her_s11_s16s_permission"),
	  (else_try),
	    (troop_slot_eq, ":lady_guardian", slot_lord_granted_courtship_permission, -1),
		(str_store_string, s12, "str__alas_as_we_know_my_s11_s16_will_not_permit_me_to_see_you_however_i_believe_that_i_can_arrange_away_for_you_to_enter_undetected"),
	  (else_try),
	    (troop_slot_eq, ":lady_guardian", slot_lord_granted_courtship_permission, 1),
		(str_store_string, s12, "str__as_my_s11_s16_has_already_granted_permission_for_you_to_see_me_i_shall_expect_your_imminent_arrival"),
	  (try_end),
	  ##diplomacy start+ Revert register
	  (assign, reg4, ":save_reg4"),
	  ##diplomacy end+
      ],
    [
	
      ("continue",[],"Tell the woman to inform her mistress that you will come shortly",
       [

     	(assign, ":lady_to_visit", "$g_notification_menu_var1"),
	    (str_store_troop_name_link, s3, ":lady_to_visit"),
	    (str_store_party_name_link, s4, "$g_notification_menu_var2"),
		
		(str_store_string, s2, "str_visit_s3_who_was_last_at_s4s18"),
	    (call_script, "script_start_quest", "qst_visit_lady", ":lady_to_visit"),
		(quest_set_slot, "qst_visit_lady", slot_quest_giver_troop, ":lady_to_visit"), #don't know why this is necessary
		
		(try_begin),
			(eq, "$cheat_mode", 1),
			(quest_get_slot, ":giver_troop", "qst_visit_lady", slot_quest_giver_troop),
			(str_store_troop_name, s2, ":giver_troop"),
			(display_message, "str_giver_troop_=_s2"),
		(try_end),	
		
		(quest_set_slot, "qst_visit_lady", slot_quest_expiration_days, 30),
	    (change_screen_return),
        ]),
	
      ("continue",[],"Tell the woman to inform her mistress that you are indisposed",
       [
	    (troop_set_slot, "$g_notification_menu_var1", slot_lady_no_messages, 1),
	    (change_screen_return),
        ]),
     ]
  ),
  (
    "notification_player_faction_political_issue_resolved",0,
    "After consulting with the hereditary vassals of the clan, {s10} has decided to confer {s11} on {s12}.",
    "none",
    [
	(assign, ":faction_issue_resolved", "$g_notification_menu_var1"),
	(assign, ":faction_decision", "$g_notification_menu_var2"),
	(faction_get_slot, ":leader", "$players_kingdom", slot_faction_leader),
	(str_store_troop_name, s10, ":leader"),
	(try_begin),
		(eq, ":faction_issue_resolved", 1),
		(str_store_string, s11, "str_the_marshalship"),
	(else_try),
		(str_store_party_name, s11, ":faction_issue_resolved"),
	(try_end),
	(str_store_troop_name, s12, ":faction_decision"),

	],
    [
	   ("continue",
	   [],"Continue...",
       [
        (change_screen_return),
        ]),		
	
	
	]
  ),
  
  (
    "notification_player_faction_political_issue_resolved_for_player",0,
    "After consulting with the hereditary vassals of the clan, {s10} has decided to confer {s11} on you. You may decline the honor, but it will probably mean that you will not receive other awards for a little while.{s12}",
    "none",
    [
	(faction_get_slot, ":leader", "$players_kingdom", slot_faction_leader),
	(str_store_troop_name, s10, ":leader"),
	(faction_get_slot, ":issue", "$players_kingdom", slot_faction_political_issue),
	(try_begin),
		(eq, ":issue", 1),
		(str_store_string, s11, "str_the_marshalship"),
		(str_store_string, s12, "@^^Note that so long as you remain strategist, the hereditary vassals of the clan will be expecting you to lead them on campaign. So, if you are awaiting a feast, either for a wedding or for other purposes, you may wish to resign as strategist by speaking to your great lord."),
	(else_try),
		(str_clear, s12),
		(str_store_party_name, s11, ":issue"),
	(try_end),	
	],
    [
	   ("accept",
	   [],"Accept the honor",
       [
	    (faction_get_slot, ":issue", "$players_kingdom", slot_faction_political_issue),
		
		(try_begin),
			(eq, ":issue", 1),
		    (call_script, "script_check_and_finish_active_army_quests_for_faction", "$players_kingdom"),       
			(call_script, "script_appoint_faction_marshall", "$players_kingdom", "trp_player"), 
			(unlock_achievement, ACHIEVEMENT_AUTONOMOUS_COLLECTIVE),
		(else_try),
			(call_script, "script_give_center_to_lord", ":issue", "trp_player", 0), #Zero means don't add garrison
		(try_end),
				
		(faction_set_slot, "$players_kingdom", slot_faction_political_issue, 0),
		(try_for_range, ":active_npc", active_npcs_begin, active_npcs_end),
			(store_faction_of_troop, ":active_npc_faction", ":active_npc"),
			(eq, ":active_npc_faction", "$players_kingdom"),
			(troop_set_slot, ":active_npc", slot_troop_stance_on_faction_issue, -1),
		(try_end),
        (change_screen_return),
        ]),	

	   ("decline",
	   [],"Decline the honor",
       [
	    (faction_get_slot, ":issue", "$players_kingdom", slot_faction_political_issue),
		(try_begin),
			(is_between, ":issue", centers_begin, centers_end),
			(assign, "$g_dont_give_fief_to_player_days", 30),
		(else_try),
			(assign, "$g_dont_give_marshalship_to_player_days", 30),
		(try_end),
		
		(try_for_range, ":active_npc", active_npcs_begin, active_npcs_end),
			(store_faction_of_troop, ":active_npc_faction", ":active_npc"),
			(eq, ":active_npc_faction", "$players_kingdom"),
			(troop_set_slot, ":active_npc", slot_troop_stance_on_faction_issue, -1),
		(try_end),
        (change_screen_return),
        ]),			
	]
  ),
  ("establish_court",mnf_disable_all_keys,
    "To establish {s4} as your court will require a small refurbishment. In particular, you will need a set of tools and a bolt of silk cloth. it may also take a short while for some of your followers to relocate here. Do you wish to proceed?",
    "none",
    [
	(str_store_party_name, s4, "$g_encountered_party"),
	],
	
    [
      ("establish",[
	  (player_has_item, "itm_tools"),
	  (player_has_item, "itm_velvet"),
	  ],"Establish {s4} as your court",
       [         
		(assign, "$g_player_court", "$current_town"),
	    (troop_remove_item, "trp_player", "itm_tools"),
	    (troop_remove_item, "trp_player", "itm_velvet"),
        (jump_to_menu, "mnu_town"),         
       ]),       
	
	
      ("continue",[],"Hold off...",
       [         
         (jump_to_menu, "mnu_town"),         
       ]),       
    ]
  ),
  ("notification_relieved_as_marshal", mnf_disable_all_keys,
    "{s4} wishes to inform you that your services as strategist are no longer required. In honor of valiant efforts on behalf of the clan over the last {reg4} days, however, {reg8?she:he} offers you a purse of {reg5} mon.",
    "none",
    [
	(assign, reg4, "$g_player_days_as_marshal"),
	

	
	(store_div, ":renown_gain", "$g_player_days_as_marshal",4),
	(val_min, ":renown_gain", 20),
	(store_mul, ":denar_gain", "$g_player_days_as_marshal", 50),
	(val_max, ":denar_gain", 200),
	(val_min, ":denar_gain", 4000),
	(troop_add_gold, "trp_player", ":denar_gain"),
	(call_script, "script_change_troop_renown", "trp_player", ":renown_gain"),
	(assign, "$g_player_days_as_marshal", 0),
	(assign, "$g_dont_give_marshalship_to_player_days", 15),
	(assign, reg5, ":denar_gain"),
	
	(faction_get_slot, ":faction_leader", "$players_kingdom", slot_faction_leader),
	(str_store_troop_name, s4, ":faction_leader"),
	##diplomacy start+ get gender with script
	#(troop_get_type, reg8, ":faction_leader"),#<- OLD
	(assign, ":save_reg0", reg0),
	(call_script, "script_dplmc_store_troop_is_female", ":faction_leader"),
	(assign, reg8, reg0),
	(assign, reg0, ":save_reg0"),
	##diplomacy end+
	],
	
	 [
      ("continue",[],"Continue",
       [         
         (change_screen_return),         
       ]),         
    ]
  ),
  
  ##diplomacy begin
########################################################
# Autoloot Game Menus Begin
########################################################

	##########################################################
	# Inventory allocation / Loot allocation Game Menu  -  by Fisheye
	# Parameters:
	# $return_menu : return to this menu after managing loot.  0 if this menu is called via random encounter
	##diplomacy start+
	#Added "return_menu", renaming it to "$dplmc_return_menu"
	##diplomacy end+
	("dplmc_manage_loot_pool",
		0,
		"{s10}",
		"none",
		[
			##diplomacy start+
			#Use a different troop!
			#(assign, "$pool_troop", "trp_dplmc_chamberlain"),
			(assign, "$pool_troop", "trp_temp_troop"),
			#Make sure things are initialized
			(call_script, "script_dplmc_initialize_autoloot", 0),#argument "0" means this does nothing if deemed unnecessary
			##diplomacy end+
			(assign, reg20,0),
			(troop_get_inventory_capacity, ":inv_cap", "$pool_troop"),
				(try_for_range, ":i_slot", 0, ":inv_cap"),
					(troop_get_inventory_slot, ":item_id", "$pool_troop", ":i_slot"),
					(ge, ":item_id", 0),
					(neg|troop_has_item_equipped, "$pool_troop", ":item_id"),
					(val_add, reg20,1),
				(try_end),
				# reg20 now contains number of items in loot pool
				(try_begin),
					(eq, reg20, 0),
					(str_store_string, 10, "str_dplmc_item_pool_no_items"),
					(str_store_string, 20, "str_dplmc_item_pool_leave"),
				(else_try),
					(eq, reg20, 1),
					(str_store_string, 10, "str_dplmc_item_pool_one_item"),
					(str_store_string, 20, "str_dplmc_item_pool_abandon"),
				(else_try),
					(str_store_string, 10, "str_dplmc_item_pool_many_items"),
					(str_store_string, 20, "str_dplmc_item_pool_abandon"),
				(try_end),
		],
		[
			("dplmc_auto_loot",
				[
					(eq, "$inventory_menu_offset",0),
					(store_free_inventory_capacity, ":space", "$pool_troop"),
					(ge, ":space", 10)
				],
				##diplomacy start+
				#"Let your heroes select gear from the item pool.",
				"Let your heroes select gear from the items on the ground.",
				##diplomacy end+
				[
					##diplomacy start+
					(call_script, "script_dplmc_initialize_autoloot", 0),#argument "0" means this does nothing if deemed unnecessary
					##diplomacy end+
					(jump_to_menu, "mnu_dplmc_auto_loot")
				]
			),
			("dplmc_auto_loot_no",
				[
					(eq, "$inventory_menu_offset",0),
					(store_free_inventory_capacity, ":space", "$pool_troop"),
					(lt, ":space", 10),
					(disable_menu_option)
				],
				"Insufficient item pool space for auto-upgrade.",
				[]
			),
			("dplmc_loot",
				[],
				##diplomacy start+
				#"Access the item pool.",
				"Access the items on the ground.",
				##diplomacy end+
				[
					(change_screen_loot, "$pool_troop"),
				]
			),
      ("dplmc_auto_loot_upgrade_management", [],
##diplomacy start+
#        "Upgrade management of the NPC's equipments.",
         "Update management of NPCs' equipment.",
##diplomacy end+
        [
          (party_get_num_companion_stacks, ":num_stacks", "p_main_party"),
		  ##nested diplomcy start+ Add error check.
		  (assign, "$temp", -1),
		  ##nested diplomacy end+
          (try_for_range, ":stack_no", 0, ":num_stacks"),
            (party_stack_get_troop_id,   ":stack_troop", "p_main_party", ":stack_no"),
			#gekokujo 3.0 microfactions! include fort companions start
            #(is_between, ":stack_troop", companions_begin, companions_end),
            (is_between, ":stack_troop", companions_begin, fort_companions_end),
			#gekokujo 3.0 microfactions! include fort companions end
            (assign, "$temp", ":stack_troop"),
            (assign, ":num_stacks", 0),
          (try_end),
		  ##nested diplomacy start+   Add error check.
		  (call_script, "script_dplmc_initialize_autoloot", 0),#argument "0" means this does nothing if deemed unnecessary
		  (try_begin),#<- dplmc+ added
		    (ge, "$temp", 1),#<- dplmc+ added
			(start_presentation, "prsnt_dplmc_autoloot_upgrade_management"),
		  (try_end),
		  ##nested diplomacy end+
        ]
      ),
			("dplmc_leave",
				[],
				"{s20}",
				[
				##diplomacy start+
				#Actually abandon the lost loot
				(troop_get_inventory_capacity, ":inv_cap", "$pool_troop"),
				(try_for_range, ":i_slot", 10, ":inv_cap"),
					(troop_get_inventory_slot, ":item_id", "$pool_troop", ":i_slot"),
					(ge, ":item_id", 0),
					(neg|troop_has_item_equipped, "$pool_troop", ":item_id"),
					(troop_set_inventory_slot, "$pool_troop", ":i_slot", -1), #delete it
					(troop_inventory_slot_set_item_amount, "$pool_troop", ":i_slot", 0),
				(try_end),

				#(jump_to_menu, "mnu_camp"),
				(jump_to_menu, "$dplmc_return_menu"),
				##diplomacy end+
				]
			),
			##nested diplomacy start+
			#Leave & take everything you can
			("dplmc_leave_and_take_a",
				[
				(store_free_inventory_capacity, ":space", "trp_player"),
				(lt, ":space", reg20),
				(gt, reg20, 0),
				(gt, ":space", 0),
				(assign, reg0, ":space"),
				],
				"Gather {reg0} of the {reg20} items on the ground and leave.",
				[
					(store_free_inventory_capacity, ":space", "trp_player"),
					#Take remaining items for player
					(troop_get_inventory_capacity, ":inv_cap", "$pool_troop"),
					(try_for_range, ":i_slot", 10, ":inv_cap"),
					    (gt, ":space", 0),
					    (troop_get_inventory_slot, ":item_id", "$pool_troop", ":i_slot"),
					    (ge, ":item_id", 0),
					    (neg|troop_has_item_equipped, "$pool_troop", ":item_id"),
					    (troop_get_inventory_slot_modifier, ":imod", "$pool_troop", ":i_slot"),
					    (troop_add_item, "trp_player", ":item_id", ":imod"),#give item to player
					    (val_sub, ":space", 1),
					    (troop_set_inventory_slot, "$pool_troop", ":i_slot", -1), #remove item from pool
					    (troop_inventory_slot_set_item_amount, "$pool_troop", ":i_slot", 0),
					(try_end),
					#(jump_to_menu, "mnu_camp"),
					(jump_to_menu, "$dplmc_return_menu"),
				]
			),
			("dplmc_leave_and_take_b",
				[
				(store_free_inventory_capacity, ":space", "trp_player"),
				(ge, ":space", reg20),
				(gt, reg20, 0),#don't show if nothing is on the ground
				(store_sub, reg0, reg20, 1),
				],
				"Gather the remaining {reg20} {reg0?items:item} on the ground and leave.",
				[
					(store_free_inventory_capacity, ":space", "trp_player"),
					#Take remaining items for player
					(troop_get_inventory_capacity, ":inv_cap", "$pool_troop"),
					(try_for_range, ":i_slot", 10, ":inv_cap"),
					    (gt, ":space", 0),
					    (troop_get_inventory_slot, ":item_id", "$pool_troop", ":i_slot"),
					    (ge, ":item_id", 0),
					    (neg|troop_has_item_equipped, "$pool_troop", ":item_id"),
					    (troop_get_inventory_slot_modifier, ":imod", "$pool_troop", ":i_slot"),
					    (troop_add_item, "trp_player", ":item_id", ":imod"),#give item to player
					    (val_sub, ":space", 1),
					    (troop_set_inventory_slot, "$pool_troop", ":i_slot", -1), #remove item frlom pool
					    (troop_inventory_slot_set_item_amount, "$pool_troop", ":i_slot", 0),
					(try_end),
					#(jump_to_menu, "mnu_camp"),
					(jump_to_menu, "$dplmc_return_menu"),
				]
			),
			("dplmc_leave_and_take_c",
				[
				(store_free_inventory_capacity, ":space", "trp_player"),
				(eq, ":space", 0),
				(gt, reg20, 0),#don't show if nothing is on the ground
				(disable_menu_option),
				],
				"There is no space left in your bags.",
				[
				]
			),
			##nested diplomacy end+
		]
	),
	("dplmc_auto_loot",
		0,
##diplomacy start+
#		"Your heroes will automatically grab items from the item pool based on their pre-selected upgrade options. Heroes listed first in the party order will have first pick. Any equipment no longer needed will be placed back into the item pool. Are you sure you wish to do this?",
		"Your heroes will automatically grab items from the loot pool based on their pre-selected upgrade options. Heroes listed first in the party order will have first pick. Any equipment no longer needed will be dropped back into the loot pool.  Any items in the loot pool will be lost when you leave.  Are you sure you wish to do this?",
##diplomacy end+
		"none",
		[],
		[
			("dplmc_autoloot_no",
				[],
				"No, I've changed my mind.",
				[
					(jump_to_menu, "mnu_dplmc_manage_loot_pool"),
				]
			),
			("dplmc_autoloot_yes",
				[],
				"Yes, perform the upgrading.",
				[
					##diplomacy start+
					(call_script, "script_dplmc_initialize_autoloot", 0),#argument "0" means this does nothing if deemed unnecessary
					(assign, "$pool_troop", "trp_temp_troop"),
					##diplomacy end+
					(call_script, "script_dplmc_auto_loot_all"),
					(jump_to_menu, "mnu_dplmc_manage_loot_pool"),
				]
			),
		]
	),
  (
    "dplmc_notification_alliance_declared",0,
    "Alliance Agreement^^{s1} and {s2} have formed an alliance!^{s57}",
    "none",
    [

	  (str_clear, s57),

	  (str_store_faction_name, s1, "$g_notification_menu_var1"),
      (str_store_faction_name, s2, "$g_notification_menu_var2"),
      (set_fixed_point_multiplier, 100),
      (position_set_x, pos0, 65),
      (position_set_y, pos0, 30),
      (position_set_z, pos0, 170),
      (store_sub, ":faction_1", "$g_notification_menu_var1", kingdoms_begin),
      (store_sub, ":faction_2", "$g_notification_menu_var2", kingdoms_begin),
      (val_mul, ":faction_1", 128),
      (val_add, ":faction_1", ":faction_2"),
      (set_game_menu_tableau_mesh, "tableau_2_factions_mesh", ":faction_1", pos0),
      ],
    [
      ("dplmc_continue",[],"Continue...",
       [(change_screen_return),
        ]),
     ]
  ),
  (
    "dplmc_notification_defensive_declared",0,
    "Defensive Pact^^{s1} and {s2} have agreed to a defensive pact!^{s57}",
    "none",
    [

	  (str_clear, s57),

	  (str_store_faction_name, s1, "$g_notification_menu_var1"),
      (str_store_faction_name, s2, "$g_notification_menu_var2"),
      (set_fixed_point_multiplier, 100),
      (position_set_x, pos0, 65),
      (position_set_y, pos0, 30),
      (position_set_z, pos0, 170),
      (store_sub, ":faction_1", "$g_notification_menu_var1", kingdoms_begin),
      (store_sub, ":faction_2", "$g_notification_menu_var2", kingdoms_begin),
      (val_mul, ":faction_1", 128),
      (val_add, ":faction_1", ":faction_2"),
      (set_game_menu_tableau_mesh, "tableau_2_factions_mesh", ":faction_1", pos0),
      ],
    [
      ("dplmc_continue",[],"Continue...",
       [(change_screen_return),
        ]),
     ]
  ),
  (
    "dplmc_notification_trade_declared",0,
    "Trade Agreement^^{s1} and {s2} have signed a trade agreement!^{s57}",
    "none",
    [

	  (str_clear, s57),

	  (str_store_faction_name, s1, "$g_notification_menu_var1"),
      (str_store_faction_name, s2, "$g_notification_menu_var2"),
      (set_fixed_point_multiplier, 100),
      (position_set_x, pos0, 65),
      (position_set_y, pos0, 30),
      (position_set_z, pos0, 170),
      (store_sub, ":faction_1", "$g_notification_menu_var1", kingdoms_begin),
      (store_sub, ":faction_2", "$g_notification_menu_var2", kingdoms_begin),
      (val_mul, ":faction_1", 128),
      (val_add, ":faction_1", ":faction_2"),
      (set_game_menu_tableau_mesh, "tableau_2_factions_mesh", ":faction_1", pos0),
      ],
    [
      ("dplmc_continue",[],"Continue...",
       [(change_screen_return),
        ]),
     ]
  ),
  (
    "dplmc_notification_nonaggression_declared",0,
    "Non-aggression Treaty^^{s1} and {s2} have concluded a non-aggression treaty!^{s57}",
    "none",
    [
	  (str_clear, s57),

	  (str_store_faction_name, s1, "$g_notification_menu_var1"),
      (str_store_faction_name, s2, "$g_notification_menu_var2"),
      (set_fixed_point_multiplier, 100),
      (position_set_x, pos0, 65),
      (position_set_y, pos0, 30),
      (position_set_z, pos0, 170),
      (store_sub, ":faction_1", "$g_notification_menu_var1", kingdoms_begin),
      (store_sub, ":faction_2", "$g_notification_menu_var2", kingdoms_begin),
      (val_mul, ":faction_1", 128),
      (val_add, ":faction_1", ":faction_2"),
      (set_game_menu_tableau_mesh, "tableau_2_factions_mesh", ":faction_1", pos0),
      ],
    [
      ("dplmc_continue",[],"Continue...",
       [(change_screen_return),
        ]),
     ]
  ),
  (
    "dplmc_question_alliance_offer",0,
    "You Receive an Alliance Offer^^The {s1} wants to form an alliance with you. What is your answer?",
    "none",
    [
      (str_store_faction_name, s1, "$g_notification_menu_var1"),
      (set_fixed_point_multiplier, 100),
      (position_set_x, pos0, 65),
      (position_set_y, pos0, 30),
      (position_set_z, pos0, 170),
      (set_game_menu_tableau_mesh, "tableau_faction_note_mesh_banner", "$g_notification_menu_var1", pos0),
      ],
    [
      ("dplmc_alliance_offer_accept",[],"Accept",
       [
         (call_script, "script_dplmc_start_alliance_between_kingdoms", "fac_player_supporters_faction", "$g_notification_menu_var1", 1),
         (change_screen_return),
        ]),
      ("dplmc_alliance_offer_reject",[],"Reject",
       [
         (call_script, "script_change_player_relation_with_faction", "$g_notification_menu_var1", -2),
         (change_screen_return),
        ]),
     ]
  ),
  (
    "dplmc_question_defensive_offer",0,
    "You Receive a Pact Offer^^The {s1} offers you a defensive pact. What is your answer?",
    "none",
    [
      (str_store_faction_name, s1, "$g_notification_menu_var1"),
      (set_fixed_point_multiplier, 100),
      (position_set_x, pos0, 65),
      (position_set_y, pos0, 30),
      (position_set_z, pos0, 170),
      (set_game_menu_tableau_mesh, "tableau_faction_note_mesh_banner", "$g_notification_menu_var1", pos0),
      ],
    [
      ("dplmc_defensive_offer_accept",[],"Accept",
       [
         (call_script, "script_dplmc_start_defensive_between_kingdoms", "fac_player_supporters_faction", "$g_notification_menu_var1", 1),
         (change_screen_return),
        ]),
      ("dplmc_defensive_offer_reject",[],"Reject",
       [
         (call_script, "script_change_player_relation_with_faction", "$g_notification_menu_var1", -2),
         (change_screen_return),
        ]),
     ]
  ),
  (
    "dplmc_question_trade_offer",0,
    "You Receive a Pact Offer^^The {s1} offers you a trade pact. What is your answer?",
    "none",
    [
      (str_store_faction_name, s1, "$g_notification_menu_var1"),
      (set_fixed_point_multiplier, 100),
      (position_set_x, pos0, 65),
      (position_set_y, pos0, 30),
      (position_set_z, pos0, 170),
      (set_game_menu_tableau_mesh, "tableau_faction_note_mesh_banner", "$g_notification_menu_var1", pos0),
      ],
    [
      ("dplmc_trade_offer_accept",[],"Accept",
       [
         (call_script, "script_dplmc_start_trade_between_kingdoms", "fac_player_supporters_faction", "$g_notification_menu_var1", 1),
         (change_screen_return),
        ]),
      ("dplmc_trade_offer_reject",[],"Reject",
       [
         (call_script, "script_change_player_relation_with_faction", "$g_notification_menu_var1", -2),
         (change_screen_return),
        ]),
     ]
  ),
  (
    "dplmc_question_nonaggression_offer",0,
    "You Receive a Pact Offer^^The {s1} offers you a non-aggression treaty. What is your answer?",
    "none",
    [
      (str_store_faction_name, s1, "$g_notification_menu_var1"),
      (set_fixed_point_multiplier, 100),
      (position_set_x, pos0, 65),
      (position_set_y, pos0, 30),
      (position_set_z, pos0, 170),
      (set_game_menu_tableau_mesh, "tableau_faction_note_mesh_banner", "$g_notification_menu_var1", pos0),
      ],
    [
      ("dplmc_nonaggression_offer_accept",[],"Accept",
       [
         (call_script, "script_dplmc_start_nonaggression_between_kingdoms", "fac_player_supporters_faction", "$g_notification_menu_var1", 1),
         (change_screen_return),
        ]),
      ("dplmc_nonaggression_offer_reject",[],"Reject",
       [
         (call_script, "script_change_player_relation_with_faction", "$g_notification_menu_var1", -2),
         (change_screen_return),
        ]),
     ]
  ),
  (
    "dplmc_notification_alliance_expired",0,
    "Alliance Has Expired^^The alliance between {s1} and {s2} has expired and was degraded to a defensive pact.",
    "none",
    [
      (str_store_faction_name, s1, "$g_notification_menu_var1"),
      (str_store_faction_name, s2, "$g_notification_menu_var2"),

      (set_fixed_point_multiplier, 100),
      (position_set_x, pos0, 65),
      (position_set_y, pos0, 30),
      (position_set_z, pos0, 170),
      (set_game_menu_tableau_mesh, "tableau_faction_note_mesh_banner", "$g_notification_menu_var1", pos0),
      ],
    [
      ("dplmc_continue",[],"Continue",
       [
	   (change_screen_return),
        ]),
     ]
  ),
  (
    "dplmc_notification_defensive_expired",0,
    "Defensive Pact Has Expired^^The defensive pact between {s1} and {s2} has expired and was degraded to a trade agreement.",
    "none",
    [
      (str_store_faction_name, s1, "$g_notification_menu_var1"),
      (str_store_faction_name, s2, "$g_notification_menu_var2"),

      (set_fixed_point_multiplier, 100),
      (position_set_x, pos0, 65),
      (position_set_y, pos0, 30),
      (position_set_z, pos0, 170),
      (set_game_menu_tableau_mesh, "tableau_faction_note_mesh_banner", "$g_notification_menu_var1", pos0),
      ],
    [
      ("dplmc_continue",[],"Continue",
       [
	   (change_screen_return),
        ]),
     ]
  ),
  (
    "dplmc_notification_trade_expired",0,
    "Trade Agreement Has Expired^^The trade agreement between {s1} and {s2} has expired and was degraded to a non-aggression treaty.",
    "none",
    [
      (str_store_faction_name, s1, "$g_notification_menu_var1"),
      (str_store_faction_name, s2, "$g_notification_menu_var2"),

      (set_fixed_point_multiplier, 100),
      (position_set_x, pos0, 65),
      (position_set_y, pos0, 30),
      (position_set_z, pos0, 170),
      (set_game_menu_tableau_mesh, "tableau_faction_note_mesh_banner", "$g_notification_menu_var1", pos0),
      ],
    [
      ("dplmc_continue",[],"Continue",
       [
	   (change_screen_return),
        ]),
     ]
  ),
  ("dplmc_dictate_terms",menu_text_color(0xFF000000)|mnf_disable_all_keys,
    "Dictate your peace terms.",
    "none",
    [(set_game_menu_tableau_mesh, "tableau_faction_note_mesh_banner", "$g_notification_menu_var1", pos0),],
    [
      ("dplmc_demand_4000",[(gt, "$g_player_chamberlain", 0),],"Demand 4000 mon",
      [
        (call_script, "script_npc_decision_checklist_peace_or_war", "$g_notification_menu_var1", "fac_player_supporters_faction", -1),
        (assign, ":goodwill", reg0),
        (store_random_in_range, ":random", 0, 4),

        (call_script, "script_change_player_relation_with_faction", "$g_notification_menu_var1", -3),
        (try_begin),
          (le, ":random", ":goodwill"),
          (call_script, "script_dplmc_pay_into_treasury", 4000),
          (call_script, "script_diplomacy_start_peace_between_kingdoms", "$g_notification_menu_var1", "fac_player_supporters_faction", 1),
          (change_screen_return),
        (else_try),
          (jump_to_menu,"mnu_dplmc_deny_terms"),
        (try_end),
      ]),
      ("dplmc_demand_8000",[(gt, "$g_player_chamberlain", 0),],"Demand 8000 mon",
       [
         (call_script, "script_npc_decision_checklist_peace_or_war", "$g_notification_menu_var1", "fac_player_supporters_faction", -1),
         (assign, ":goodwill", reg0),
         (val_mul, ":goodwill", 2),
				 (store_random_in_range, ":random", 0, 10),

         (call_script, "script_change_player_relation_with_faction", "$g_notification_menu_var1", -5),
				 (try_begin),
				   (le, ":random", ":goodwill"),
           (call_script, "script_dplmc_pay_into_treasury", 8000),
           (call_script, "script_diplomacy_start_peace_between_kingdoms", "$g_notification_menu_var1", "fac_player_supporters_faction", 1),
           (change_screen_return),
         (else_try),
             (jump_to_menu,"mnu_dplmc_deny_terms"),
         (try_end),
       ]),
      ("dplmc_demand_castle",[
        (assign, ":distance", 100),
        (assign, "$demanded_castle", -1),
		##diplomacy start+ Handle player is co-ruler of NPC kingdom
		(assign, ":alt_faction", "fac_player_supporters_faction"),
		(try_begin),
			(is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
			(call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", "$players_kingdom"),
			(ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
			(assign, ":alt_faction", "$players_kingdom"),
		(try_end),
		##diplomacy end+
        (try_for_range, ":castle", castles_begin, castles_end),
          (store_faction_of_party, ":castle_faction", ":castle"),
          (eq, ":castle_faction", "$g_notification_menu_var1"),
          (try_for_range, ":center", centers_begin, centers_end),
            (store_faction_of_party, ":center_faction", ":center"),
			##diplomacy start+
			(this_or_next|eq, ":alt_faction", ":center_faction"),
			##diplomacy end+
            (eq, ":center_faction", "fac_player_supporters_faction"),
            (store_distance_to_party_from_party, ":tmp_distance", ":center", ":castle"),

            (lt, ":tmp_distance", ":distance"),
            (assign, ":distance", ":tmp_distance"),
            (assign, "$demanded_castle", ":castle"),
            (str_store_party_name, s2, ":castle"),
          (try_end),
        (try_end),
        (is_between, "$demanded_castle", castles_begin,castles_end),
      ],"Demand {s2}.",
       [
        (call_script, "script_npc_decision_checklist_peace_or_war", "$g_notification_menu_var1", "fac_player_supporters_faction", -1),
        (assign, ":goodwill", reg0),
        (val_mul, ":goodwill", 2),
        (store_random_in_range, ":random", 0, 12),

        (call_script, "script_change_player_relation_with_faction", "$g_notification_menu_var1", -6),
        (try_begin),
          (le, ":random", ":goodwill"),
			 ##diplomacy start+
			 #Chance of veto based on ownership and difficulty setting.
			 (assign, ":did_veto", 0),
			 (try_begin),
					 (party_get_slot, ":castle_lord", "$demanded_castle", slot_town_lord),
					 (ge, ":castle_lord", 1),
					 (neg|troop_slot_ge, ":castle_lord", slot_troop_prisoner_of_party, 0),
					 (try_begin),
								(this_or_next|troop_slot_eq, ":castle_lord", slot_troop_home, "$demanded_castle"),
								(party_slot_eq, "$demanded_castle", dplmc_slot_center_original_lord, ":castle_lord"),
								(store_random_in_range, ":random", 0, 24),
								(assign, ":did_veto", 1),
								(le, ":random", ":goodwill"),
								(assign, ":did_veto", 0),
 					 (else_try),
								(troop_get_slot, ":castle_lord_original_faction", ":castle_lord", slot_troop_original_faction),
								(party_slot_eq, "$demanded_castle", slot_center_original_faction, ":castle_lord_original_faction"),
								(store_random_in_range, ":random", 0, 12),
								(assign, ":did_veto", 1),
								(le, ":random", ":goodwill"),
								(assign, ":did_veto", 0),
					 (try_end),
			 (try_end),
			 (eq, ":did_veto", 0),
		  ##Handle player is co-ruler of NPC kingdom
          ##OLD:
          #(call_script, "script_give_center_to_faction", "$demanded_castle", "fac_player_supporters_faction"),
          #(call_script, "script_diplomacy_start_peace_between_kingdoms", "$g_notification_menu_var1", "fac_player_supporters_faction", 1),
		  ##NEW:
		  (assign, ":player_kingdom", "fac_player_supporters_faction"),
		  (try_begin),
		        (neg|faction_slot_eq, "fac_player_supporters_faction", slot_faction_state, sfs_active),
				(is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
				(call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", "$players_kingdom"),
				(ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
				(assign, ":player_kingdom", "$players_kingdom"),
		  (try_end),
		  (call_script, "script_give_center_to_faction", "$demanded_castle", ":player_kingdom"),
          (call_script, "script_diplomacy_start_peace_between_kingdoms", "$g_notification_menu_var1", ":player_kingdom", 1),
		  ##diplomacy end+
          (change_screen_return),
        (else_try),
          (jump_to_menu,"mnu_dplmc_deny_terms"),
        (try_end),        ]
       ),
	  ("dplmc_go_back",[],"Go back",
       [
	     (jump_to_menu,"mnu_question_peace_offer"),
       ]),
    ]
  ),
  ("dplmc_deny_terms",menu_text_color(0xFF000000)|mnf_disable_all_keys,
    "The {s1} refuses your terms and is breaking off of negotiations.",
    "none",
    [(set_game_menu_tableau_mesh, "tableau_faction_note_mesh_banner", "$g_notification_menu_var1", pos0),],
    [
	  ("dplmc_continue",[],"Continue",
       [
       (change_screen_return),
       ]),
    ]
  ),
  (
    "dplmc_village_riot_result",mnf_scale_picture,
    "{s9}",
    "none",
    [(try_begin),
       (eq, "$g_battle_result", 1),
       (jump_to_menu, "mnu_dplmc_village_riot_removed"),
     (else_try),
       (set_background_mesh, "mesh_pic_villageriot"),
       (str_store_string, s9, "@Try as you might, you could not defeat the rebelling village."),
     (try_end),
    ],
    [
      ("dplmc_continue",[],"Continue...",
       [(call_script, "script_change_player_relation_with_center", "$g_encountered_party", -3),
        (jump_to_menu, "mnu_village"),]),
    ],
  ),
  (
    "dplmc_village_riot_removed",mnf_disable_all_keys,
    "In bloody battle you and your men slaughter the rebels and regain control over the village. But there is not much left you can control.",
    "none",
    [
     (set_background_mesh, "mesh_pic_looted_village"),
     (party_set_slot, "$g_encountered_party", slot_village_infested_by_bandits, 0),
     (call_script, "script_village_set_state",  "$current_town", svs_looted),
    ],
    [
      ("dplmc_continue",[],"Continue...",
       [
         (jump_to_menu, "mnu_village"),
       ]),
    ],
  ),
  (
    "dplmc_town_riot_removed",mnf_disable_all_keys,
    "In bloody battle you and your men slaughter the rebels and regain control over the town.",
    "none",
    [],
    [
      ("dplmc_continue",[],"Continue...",
       [
        (party_set_slot, "$g_encountered_party", slot_village_infested_by_bandits, 0),
        (assign, "$new_encounter", 1),
        (try_begin),
          (party_get_slot, ":town_lord","$g_encountered_party", slot_town_lord),
          (troop_get_slot, ":cur_banner", ":town_lord", slot_troop_banner_scene_prop),
          (gt, ":cur_banner", 0),
          (val_sub, ":cur_banner", banner_scene_props_begin),
          (val_add, ":cur_banner", banner_map_icons_begin),
          (party_set_banner_icon, "$g_encountered_party", ":cur_banner"),
        (try_end),
        (jump_to_menu, "mnu_castle_outside"),
       ]),
    ],
  ),
  (
    "dplmc_riot_negotiate",mnf_disable_all_keys,
    "You approach the angry crowd and begin negotiations. The leader of the riot demands {reg0} mon. He agrees to lay down arms if you are willing to pay.",
    "none",
    [
      (party_get_slot, ":center_relation", "$g_encountered_party", slot_center_player_relation),
      (val_min, ":center_relation", 0),
      (try_begin),
        (party_slot_eq, "$g_encountered_party", slot_party_type, spt_town),
        (val_sub, ":center_relation", 75),
        (set_background_mesh, "mesh_pic_townriot"),
      (else_try),
        (val_sub, ":center_relation", 50),
        (set_background_mesh, "mesh_pic_villageriot"),
      (try_end),

      (store_skill_level, ":persuasion_level", "skl_persuasion", "trp_player"),
      (val_add, ":center_relation", ":persuasion_level"),
      (val_mul, ":center_relation", ":center_relation"),
      (assign, reg0, ":center_relation"),
    ],
    [
      ("dplmc_pay_riot_treasury",
      [
        (gt, "$g_player_chamberlain", 0),
        (store_troop_gold, ":gold", "trp_household_possessions"),
        (ge, ":gold", reg0),
      ],"Induce your treasurer to pay the money from the treasury.",
       [
        (call_script, "script_dplmc_withdraw_from_treasury", reg0),
        (party_set_slot, "$g_encountered_party", slot_village_infested_by_bandits, 0),
        (try_begin),
          (party_slot_eq, "$g_encountered_party", slot_party_type, spt_town),
          (jump_to_menu, "mnu_castle_outside"),
        (else_try),
          (jump_to_menu, "mnu_village"),
        (try_end),

       ]),
       ("dplmc_pay_riot_cash",
      [
        (store_troop_gold, ":gold", "trp_player"),
        (ge, ":gold", reg0),
      ],"Pay cash.",
       [
        (troop_remove_gold, "trp_player", reg0),
        (party_set_slot, "$g_encountered_party", slot_village_infested_by_bandits, 0),
        (try_begin),
          (party_slot_eq, "$g_encountered_party", slot_party_type, spt_town),
          (jump_to_menu, "mnu_castle_outside"),
        (else_try),
          (jump_to_menu, "mnu_village"),
        (try_end),

       ]),

      ("dplmc_back",[],"Back...",
       [
        (try_begin),
          (party_slot_eq, "$g_encountered_party", slot_party_type, spt_town),
          (jump_to_menu, "mnu_castle_outside"),
        (else_try),
          (jump_to_menu, "mnu_village"),
        (try_end),
       ]),
    ],
  ),
  (
    "dplmc_notification_riot",0,
    "The peasants of {s1} launched a riot against you! In a surprise attack, men loyal to you have been slain. The remainder joined the angry crowd.",
    "none",
    [
      (str_store_party_name, s1, "$g_notification_menu_var1"),
      (try_begin),
        (party_slot_eq, "$g_notification_menu_var1", slot_party_type, spt_town),
        (set_background_mesh, "mesh_pic_townriot"),
      (else_try),
        (set_background_mesh, "mesh_pic_villageriot"),
      (try_end),
      ],
    [
      ("dplmc_continue",[],"Continue...",
       [(change_screen_return),
        ]),
     ]
  ),
  (
    "dplmc_notification_appoint_chamberlain",0,
    "As a lord of a fief you can now appoint a treasurer who resides at you court for a weekly stipend of 15 mon. He will handle all financial affairs like collecting and determining taxes, paying wages and managing your estate. In addition he supervises money transfers between kingdoms giving you more diplomatic options.",
    "none",
    [],
    [

      ("dplmc_appoint_default",[],"Appoint a prominent samurai from the area.",
       [
        (call_script, "script_dplmc_appoint_chamberlain"),
        (jump_to_menu, "mnu_dplmc_chamberlain_confirm"),
        ]),
      ("dplmc_continue",[],"Proceed without treasurer.",
       [
         (assign, "$g_player_chamberlain", -1), #denied
         (change_screen_return),
        ]),
     ]
  ),
  (
    "dplmc_chamberlain_confirm",0,
    "Your treasurer can be found at your court. You should consult him if you want to give him any financial advice or you need greater amounts of money. You should always make sure that there is enough money in the treasury to pay for political affairs.",
    "none",
    [],
    [
      ("dplmc_continue",[],"Continue...",
       [
         (change_screen_return),
        ]),
     ]
  ),
  (
    "dplmc_notification_appoint_constable",0,
    "As a lord of a fief you can now appoint an army inspector who resides at you court for a weekly stipend of 15 mon. He will recruit new troops and provide information about your army.",
    "none",
    [],
    [

      ("dplmc_appoint_default",[],"Appoint a prominent samurai from the area.",
       [
        (call_script, "script_dplmc_appoint_constable"),
        (jump_to_menu, "mnu_dplmc_constable_confirm"),
        ]),
      ("dplmc_continue",[],"Proceed without an army inspector.",
       [
         (assign, "$g_player_constable", -1), #denied
         (assign, "$g_constable_training_center", -1),
         (change_screen_return),
        ]),
     ]
  ),
  (
    "dplmc_constable_confirm",0,
    "Your army inspector can be found at your court. You should consult him if you want to recruit new troops or get detailed information about your standing army.",
    "none",
    [],
    [
      ("dplmc_continue",[],"Continue...",
       [
         (change_screen_return),
        ]),
     ]
  ),
  (
    "dplmc_notification_appoint_chancellor",0,
    "As a lord of a fief you can now appoint a administrator who resides at you court for a weekly stipend of 20 mon. He will be the keeper of your seal and conduct the correspondence between you and other important persons.",
    "none",
    [],
    [

      ("dplmc_appoint_default",[],"Appoint a prominent samurai from the area.",
       [
        (call_script, "script_dplmc_appoint_chancellor"),
        (jump_to_menu, "mnu_dplmc_chancellor_confirm"),
        ]),
      ("dplmc_continue",[],"Proceed without administrator.",
       [
         (assign, "$g_player_chancellor", -1), #denied
         (change_screen_return),
        ]),
     ]
  ),
  (
    "dplmc_chancellor_confirm",0,
    "Your administrator can be found at your court. You should consult him if you want to send messages or gifts.",
    "none",
    [],
    [
      ("dplmc_continue",[],"Continue...",
       [
         (change_screen_return),
        ]),
     ]
  ),
  (
    "dplmc_deserters",0,
    "Some of your men don't believe that you will pay their wages and desert. Overall you lose: {s11} men.",
    "none",
    [
      (set_background_mesh, "mesh_pic_deserters"),
      (store_random_in_range, ":random", 1,  "$g_notification_menu_var1"),
      (call_script, "script_dplmc_player_troops_leave", ":random"),
      (str_store_string, s11, "@{reg0}"),
    ],
    [
      ("dplmc_continue",[],"Continue...",
       [
         (change_screen_return),
        ]),
     ]
  ),
  (
    "dplmc_negotiate_besieger",0,
    "You appear with a white flag at the top of the wall. After a while a negotiator of {s11} approaches you. He demands {s6} and all associated villages as well as {reg0} mon for safe conduct.",
    "none",
    [
      (party_get_slot, ":besieger", "$current_town", slot_center_is_besieged_by),
      (party_stack_get_troop_id, ":enemy_party_leader", ":besieger", 0),
      (str_store_troop_name, s11, ":enemy_party_leader"),
      (store_faction_of_troop, ":besieger_faction", ":enemy_party_leader"),

      ##diplomacy start+
	  #1) Support promoted kingdom ladies, mercenary parties, etc.
	  #2) Fix mistake with potentially not counting besieger party in the size calculation!
	  ##OLD:
	  #(assign, ":besieger_size", 0),
      #(try_for_range, ":lord", active_npcs_begin, active_npcs_end),
      #  (store_faction_of_troop, ":lord_faction", ":lord"),
      #  (eq, ":lord_faction", ":besieger_faction"),
      #  (troop_get_slot, ":led_party", ":lord", slot_troop_leaded_party),
      ##NEW:
      (party_get_num_companions, ":besieger_size", ":besieger"),

	  (try_for_parties, ":led_party"),
        (ge, ":led_party", spawn_points_end),
        (neq, ":led_party", ":besieger"),#don't double count
        (store_faction_of_party, ":party_faction", ":led_party"),
        (eq, ":party_faction", ":besieger_faction"),
	  ##diplomacy end+
        (party_is_active, ":led_party"),

        (party_slot_eq, ":led_party", slot_party_ai_state, spai_accompanying_army),
        (party_slot_eq, ":led_party", slot_party_ai_object, ":besieger"),

        (party_is_active, ":besieger"),
        (store_distance_to_party_from_party, ":distance_to_marshal", ":led_party", ":besieger"),
        (lt, ":distance_to_marshal", 25),
        (party_get_num_companions, ":party_size", ":led_party"),
        (val_add, ":besieger_size", ":party_size"),
      (try_end),

      (assign, ":garrison_size", 0),
      (party_get_num_companion_stacks, ":num_stacks", "$current_town"),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_size, ":stack_size", "$current_town", ":i_stack"),
        (val_add, ":garrison_size", ":stack_size"),
      (try_end),
      (val_sub, ":besieger_size", ":garrison_size"),

      (store_skill_level, ":player_persuasion_skill", "skl_persuasion", "trp_player"),
      (val_mul, ":player_persuasion_skill", 10),
      (store_sub, "$diplomacy_var", ":besieger_size", ":player_persuasion_skill"),
      (val_mul, "$diplomacy_var", 4),
      ##diplomacy start+ : include ransom cost in calculation
      (call_script, "script_calculate_ransom_amount_for_troop", "trp_player"),
      (val_add, "$diplomacy_var", reg0),
      ##diplomacy end+
      (val_max,"$diplomacy_var",500),
      (val_div, "$diplomacy_var", 100),
      (val_mul, "$diplomacy_var", 100),
      (assign, reg0, "$diplomacy_var"),

      (str_store_party_name, s6, "$current_town"),

    ],
      [
      ("dplmc_comply_treasury",
      [
        (store_troop_gold, ":gold", "trp_household_possessions"),
        (ge, ":gold", "$diplomacy_var"),
      ],"Comply and induce your treasurer to pay the money from the treasury.",
      [
        (call_script, "script_dplmc_withdraw_from_treasury", "$diplomacy_var"),
		##diplomacy start+ when the player pays, give the gold to the lord
		(party_get_slot, ":besieger", "$current_town", slot_center_is_besieged_by),
		(party_stack_get_troop_id, ":enemy_party_leader", ":besieger", 0),
		(call_script, "script_dplmc_distribute_gold_to_lord_and_holdings", "$diplomacy_var", ":enemy_party_leader"),
		##diplomacy end+
        (call_script, "script_dplmc_player_center_surrender", "$current_town"),
        (change_screen_return),
      ]),

      ("dplmc_comply",
      [
        (store_troop_gold, ":gold", "trp_player"),
        (ge, ":gold", "$diplomacy_var"),
      ],"Comply and pay the money cash.",
      [
        (troop_remove_gold, "trp_player", "$diplomacy_var"),
		##diplomacy start+ when the player pays, give the gold to the lord
		(party_get_slot, ":besieger", "$current_town", slot_center_is_besieged_by),
		(party_stack_get_troop_id, ":enemy_party_leader", ":besieger", 0),
		(call_script, "script_dplmc_distribute_gold_to_lord_and_holdings", "$diplomacy_var", ":enemy_party_leader"),
		##diplomacy end+
        (call_script, "script_dplmc_player_center_surrender", "$current_town"),
        (change_screen_return),
      ]),

      ("dplmc_break_off",[],"Break off negotiations.",
       [
          (jump_to_menu, "mnu_town"),
        ]),
     ]
  ),
  (
    "dplmc_messenger",0,
##nested diplomacy start+ "His" to "{reg4?Her:His}"
    "My {lord/lady}, I found {s10} and delivered your message. {reg4?Her:His} answer was {s11}.",
##nested diplomacy end+
    "none",
    [
        (set_background_mesh, "mesh_pic_messenger"),
        (str_store_troop_name, s10, "$g_notification_menu_var1"),
        (try_begin),
          (eq, "$g_notification_menu_var2", 1),
          (str_store_string, s11, "@positive"),
        (else_try),
          (str_store_string, s11, "@negative"),
        (try_end),
        ##nested diplomacy start+
        (try_begin),
           (call_script, "script_cf_dplmc_troop_is_female", "$g_notification_menu_var1"),
           (assign, reg4, 1),
        (else_try),
           (assign, reg4, 0),
        (try_end),
        ##nested diplomacy end+
    ],
    [
      ("dplmc_continue",[],"Continue...",
       [
         (change_screen_return),
        ]),
     ]
  ),
  (
    "dplmc_scout",0,
    "Your spy returned from {s10}^^{s11}{s12}",
    "none",
    [
    (set_background_mesh, "mesh_pic_messenger"),
    (str_store_party_name, s10, "$g_notification_menu_var1"),

    (call_script, "script_game_get_center_note", "$g_notification_menu_var1", 0),
    (str_store_string, s11, "@{!}{s0}"),
    (try_begin),
      (this_or_next|is_between, "$g_notification_menu_var1", towns_begin, towns_end),
      (is_between, "$g_notification_menu_var1", castles_begin, castles_end),
      (party_get_slot, ":center_food_store", "$g_notification_menu_var1", slot_party_food_store),
      (call_script, "script_center_get_food_consumption", "$g_notification_menu_var1"),
      (assign, ":food_consumption", reg0),
      (store_div, reg6, ":center_food_store", ":food_consumption"),
      (store_party_size, reg5, "$g_notification_menu_var1"),
      (str_store_string, s11, "@{s11}^^ The current garrison consists of {reg5} men.^The food stock lasts for {reg6} days."),
    (try_end),

    (str_clear, s12),
    (party_get_num_attached_parties, ":num_attached_parties", "$g_notification_menu_var1"),
    (try_begin),#<- dplmc+ unclosed try_begin!
      (gt, ":num_attached_parties", 0),
      (str_store_string, s12, "@^^Additional the following parties are currently inside:^"),
    (try_for_range, ":attached_party_rank", 0, ":num_attached_parties"),
      (party_get_attached_party_with_rank, ":attached_party", "$g_notification_menu_var1", ":attached_party_rank"),
      (str_store_party_name, s3, ":attached_party"),
      (store_party_size, reg1, ":attached_party"),
      (str_store_string, s12, "@{s12} {s3} with {reg1} troops.^"),
    (try_end),
	##diplomacy start+
	#Add missing try-end for (gt, ":num_attached_parties", 0),
	(try_end),
	##diplomacy end+

    (call_script, "script_update_center_recon_notes", "$g_notification_menu_var1"),
    ],
    [
      ("dplmc_continue",[],"Continue...",
       [
         (change_screen_return),
        ]),
     ]
  ),
  (
    "dplmc_domestic_policy",0,
    "You can now shape the domestic policy of your domain. Do you want to change your policy now?",
    "none",
    [
      (try_begin),
          (eq, "$g_players_policy_set", 1),
          (change_screen_return),
      (try_end),

      (set_fixed_point_multiplier, 100),
      (position_set_x, pos0, 65),
      (position_set_y, pos0, 30),
      (position_set_z, pos0, 170),
      (set_game_menu_tableau_mesh, "tableau_faction_note_mesh_banner", "fac_player_supporters_faction", pos0),
    ],
    [
      ("dplmc_yes",[],"Yes, I want to change the domestic policy.",
       [
         (start_presentation, "prsnt_dplmc_policy_management"),
        ]),
      ("dplmc_no",[],"No, I don't want to change the domestic policy.",
       [
         (change_screen_return),
        ]),
     ]
  ),
  (
    "dplmc_affiliate_end",0,
    "{!}{s11}",
    "none",
    [
      (set_background_mesh, "mesh_pic_messenger"),

      (str_store_troop_name, s9, "$g_notification_menu_var1"),
      (try_begin),
        ##nested diplomacy start+ (1) Fix a bug from the Diplomacy 3.3.2 version of this menu by getting your ex-affiliate
	    #from "$g_notification_menu_var2" instead of "$g_player_affiliated_troop".
        ##OLD: #(eq, "$g_player_affiliated_troop", "$g_notification_menu_var1"),
        (eq, "$g_notification_menu_var2", "$g_notification_menu_var1"),
        ##nested diplomacy end+
        (str_store_string, s11, "@{playername}, ^^I always knew you were a bad egg, since the day you have pledged allegiance to my clan. ^Did you really think you could set my family against me? You've dropped your mask, you snake! You are an infliction, and I will not bear it anymore. ^Hereby, I disown and ban you from my house. I have urged my family to fight you, and I will warn Japanese lords about your infamy. ^Tremble with fear, you have a deadly enemy! ^^{s9}."),
      (else_try),
        ##nested diplomacy start+ (2) Fix a bug from the Diplomacy 3.3.2 version of this menu by getting your ex-affiliate
	    #from "$g_notification_menu_var2" instead of "$g_player_affiliated_troop".
        ##OLD:
		#(is_between, "$g_player_affiliated_troop", lords_begin, kingdom_ladies_end),
        #(str_store_troop_name, s10, "$g_player_affiliated_troop"),
		##NEW:
		(ge, "$g_notification_menu_var2", walkers_end),
        (troop_is_hero, "$g_notification_menu_var2"),
		(str_store_troop_name, s10, "$g_notification_menu_var2"),
        ##### (3) Make the next line use correct pronouns, and correct term for king/queen.  TODO: Change some of the funny wording.
		##OLD:
        #(str_store_string, s11, "@{playername},^^ I've received a letter from {s9}, telling me about your disgracefull jiggery-pokery. In the present circumstances, {s9} could not provide evidence. But unlike you, {he/she} is a distinguished member of my family; and since all these years, I never had any reason to distrust {him/her}. I take {his/her} charges for granted. ^Hopefully, you failed to breakup my family unit. Hereby I reject your pledge : you are no longer related to my house. Each membership will retaliate against you in all conscience... ^I would be ashamed to confess how you maliciously fooled me, so I will not challenge you, to not be accountable for your death to my King. However I'm not used to report him every rat I crush while in wilderness, someday I may find you there ! ^^{s10}"),
		##NEW:
		(call_script, "script_dplmc_store_troop_is_female", "$g_notification_menu_var1"),
		(assign, reg1, reg0),#Move to reg1, because reg0 will be overwritten below
        (store_faction_of_troop, ":faction_var", "$g_notification_menu_var2"),
		(try_begin),
		   (gt, ":faction_var", 0),
		   (faction_get_slot, ":faction_var", ":faction_var", slot_faction_leader),
		   (gt, ":faction_var", 0),
		   (call_script, "script_dplmc_store_troop_is_female", ":faction_var"),
		   (eq, reg0, 1),
		   (call_script, "script_dplmc_print_cultural_word_to_sreg", "$g_notification_menu_var2", DPLMC_CULTURAL_TERM_KING_FEMALE, s11),
		   (assign, reg1, 1),#make sure the above didn't do anything funny with the register
		(else_try),
		   (call_script, "script_dplmc_print_cultural_word_to_sreg", "$g_notification_menu_var2", DPLMC_CULTURAL_TERM_KING, s11),
		   (assign, reg1, 0),#if there was no faction leader, reg0 might not have been initialized in the first place
		(try_end),
		#Aside from making the next line use the correct gender for the pronoun,
		#I made the wording a tiny bit less strange (although I left in "jiggery-pokery").
        (str_store_string, s11, "@{playername},^^ I've received a letter from {s9}, telling me about your disgraceful jiggery-pokery. In the present circumstances, {s9} could not provide evidence. But unlike you, {reg1?she:he} is a distinguished member of my family; and since all these years, I never had any reason to distrust {reg1?her:him}. I take {reg1?her:him} charges for granted. ^Hopefully, you failed to breakup my family unit. Hereby I reject your pledge : you are no longer related to my house. Each membership will retaliate against you in all conscience... ^I would be ashamed to confess how you maliciously fooled me, so I will not challenge you, to not be accountable for your death to my {s11}. However I'm not used to telling {reg0?her:him} about every rat I crush in the wilderness, and someday I may find you there ! ^^{s10}"),
        ##nested diplomacy end+
      (try_end),
    ],
    [
      ("dplmc_continue",[],"Continue...",
       [
         (change_screen_return),
        ]),
     ]
  ),
  (
    "dplmc_preferences",0,
	##diplomacy start+ alter for PBOD
    "Diplomacy "+DPLMC_DIPLOMACY_VERSION_STRING+" Preferences{s0}",##"Diplomacy preferences",
	##diplomacy end+
    "none",
    [
	##diplomacy start+
	(troop_get_slot, reg0, "trp_dplmc_chamberlain", dplmc_slot_troop_affiliated),
	(str_clear, s0),
	(try_begin),
		#Print a warning message for bad version numbers
		(neq, reg0, 0),
		(store_mod, ":verify", reg0, 128),
		(this_or_next|lt, reg0, 0),
			(neq, ":verify", DPLMC_VERSION_LOW_7_BITS),
		(str_store_string, s0, "@{!}{s0}^^ WARNING: Unexpected version value in slot dplmc_slot_troop_affiliated in trp_dplmc_chamberlain: {reg0}"),
	(else_try),
		#In cheat mode, print the diplomacy+ version
		(ge, "$cheat_mode", 1),
		(val_div, reg0, 128),
		(str_store_string, s0, "@{!}{s0}^^ DEBUG: Internal update code for current saved game is {reg0}.  Update code for the current release is "+str(DPLMC_CURRENT_VERSION_CODE)+"."),
	(try_end),
	##diplomacy end+
    ],
    [
## Tocan Invasion+ ##		
      ("tc_set_invasion",[(eq,"$invaded",0)],"Set when the Great Ming Army (Dark Knights) invasion begins.",
       [
        (jump_to_menu, "mnu_set_invasion"),
       ]),		
## Tocan Invasion- ##	   
      ("dplmc_disable_horse_speed",[(eq, "$g_dplmc_horse_speed", 0),],"Disable Diplomacy horse speed.",
       [
           (assign, "$g_dplmc_horse_speed", 1),
           (jump_to_menu, "mnu_dplmc_preferences"),
        ]),
      ("dplmc_enable_horse_speed",[(eq, "$g_dplmc_horse_speed", 1),],"Enable Diplomacy horse speed.",
       [
           (assign, "$g_dplmc_horse_speed", 0),
           (jump_to_menu, "mnu_dplmc_preferences"),
        ]),
      ("dplmc_disable_battle_continuation",[ (eq, "$g_dplmc_battle_continuation", 0),],"Disable Diplomacy battle continuation.",
       [
           (assign, "$g_dplmc_battle_continuation", 1),
           (jump_to_menu, "mnu_dplmc_preferences"),
        ]),
      ("dplmc_enable_battle_continuation",[ (eq, "$g_dplmc_battle_continuation", 1),],"Enable Diplomacy battle continuation.",
       [
           (assign, "$g_dplmc_battle_continuation", 0),
           (jump_to_menu, "mnu_dplmc_preferences"),
        ]),
##diplomacy start+
	#toggle terrain advantage
      ("dplmc_disable_terrain_advantage",[(eq, "$g_dplmc_terrain_advantage", DPLMC_TERRAIN_ADVANTAGE_ENABLE),],"Disable terrain advantage in Autocalc battles (currently this feature is Enabled).",
       [
           (assign, "$g_dplmc_terrain_advantage", DPLMC_TERRAIN_ADVANTAGE_DISABLE),
           (jump_to_menu, "mnu_dplmc_preferences"),
        ]),
      ("dplmc_enable_terrain_advantage",[
		(eq, "$g_dplmc_terrain_advantage", DPLMC_TERRAIN_ADVANTAGE_DISABLE),],"Enable terrain advantage in Autocalc battles (currently this feature is Disabled).",
       [
           (assign, "$g_dplmc_terrain_advantage", DPLMC_TERRAIN_ADVANTAGE_ENABLE),
           (jump_to_menu, "mnu_dplmc_preferences"),
        ]),
      ("dplmc_reset_terrain_advantage",[
		(neq, "$g_dplmc_terrain_advantage", DPLMC_TERRAIN_ADVANTAGE_DISABLE),
		(neq, "$g_dplmc_terrain_advantage", DPLMC_TERRAIN_ADVANTAGE_ENABLE),
		(assign, reg0, "$g_dplmc_terrain_advantage")
		],"You used a saved game from another mod: g_dplmc_terrain_advantage = {reg0} (click to reset)",
       [
           (assign, "$g_dplmc_terrain_advantage", 0),
           (jump_to_menu, "mnu_dplmc_preferences"),
        ]),
	#toggle lord recycling
	  ("dplmc_toggle_lord_recycling_a",[
		(eq, "$g_dplmc_lord_recycling", DPLMC_LORD_RECYCLING_DISABLE),
		],"Enable lords returning from exile (currently disabled)",
       [
           (assign, "$g_dplmc_lord_recycling", DPLMC_LORD_RECYCLING_ENABLE),
        ]),
	  ("dplmc_toggle_lord_recycling_b",[
		(this_or_next|eq, "$g_dplmc_lord_recycling", DPLMC_LORD_RECYCLING_FREQUENT),#currently this setting is not distinct
		(eq, "$g_dplmc_lord_recycling", DPLMC_LORD_RECYCLING_ENABLE),
		],"Disable lords returning from exile (currently enabled)",
       [
	 	   (assign, "$g_dplmc_lord_recycling", DPLMC_LORD_RECYCLING_DISABLE),
        ]),
      ("dplmc_toggle_lord_recycling_reset",
		[(neq, "$g_dplmc_lord_recycling", DPLMC_AI_CHANGES_DISABLE),
 		 (neq, "$g_dplmc_lord_recycling", DPLMC_LORD_RECYCLING_ENABLE),
		 (neq, "$g_dplmc_lord_recycling", DPLMC_LORD_RECYCLING_FREQUENT),
		 (assign, reg0, "$g_dplmc_lord_recycling"),],
			"You used a saved game from another mod: g_dplmc_lord_recycling = {reg0} (click to reset)",
       [
           (assign, "$g_dplmc_lord_recycling", 0),
           (jump_to_menu, "mnu_dplmc_preferences"),
        ]),
	#toggle AI changes
	  ("dplmc_toggle_ai_changes_a",[
		(eq, "$g_dplmc_ai_changes", DPLMC_AI_CHANGES_DISABLE),
		],"Enable AI changes (currently disabled)",
       [
           (assign, "$g_dplmc_ai_changes", DPLMC_AI_CHANGES_LOW),
        ]),
	  ("dplmc_toggle_ai_changes_b",[
		(eq, "$g_dplmc_ai_changes", DPLMC_AI_CHANGES_LOW),
		],"Increase AI changes (currently low)",
       [
	 	   (assign, "$g_dplmc_ai_changes",DPLMC_AI_CHANGES_MEDIUM),
        ]),

	  ("dplmc_toggle_ai_changes_c",[
		(eq, "$g_dplmc_ai_changes", DPLMC_AI_CHANGES_MEDIUM),
		],"Increase AI changes (currently medium)",
       [
	 	   (assign, "$g_dplmc_ai_changes", DPLMC_AI_CHANGES_HIGH),
        ]),
	  ("dplmc_toggle_ai_changes_d",[
		(eq, "$g_dplmc_ai_changes", DPLMC_AI_CHANGES_HIGH),
		],"Disable AI changes (currently high/experimental)",
       [
	 	   (assign, "$g_dplmc_ai_changes", DPLMC_AI_CHANGES_DISABLE),
        ]),
      ("dplmc_reset_ai_changes",
		[(neq, "$g_dplmc_ai_changes", DPLMC_AI_CHANGES_DISABLE),
 		 (neq, "$g_dplmc_ai_changes", DPLMC_AI_CHANGES_LOW),
		 (neq, "$g_dplmc_ai_changes", DPLMC_AI_CHANGES_MEDIUM),
		 (neq, "$g_dplmc_ai_changes", DPLMC_AI_CHANGES_HIGH),
		 (assign, reg0, "$g_dplmc_ai_changes"),],
			"You used a saved game from another mod: g_dplmc_ai_changes = {reg0} (click to reset)",
       [
           (assign, "$g_dplmc_ai_changes", 0),
           (jump_to_menu, "mnu_dplmc_preferences"),
        ]),
	#toggle economics changes
	  ("dplmc_toggle_gold_changes_a",[
		(eq, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_DISABLE),
		],"Set economic & behavioral changes to low (current mode: disabled)",
       [
           (assign, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_LOW),
        ]),
	  ("dplmc_toggle_gold_changes_b",[
		(eq, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_LOW),
		],"Set economic & behavioral changes to medium (current mode: low)",
       [
	 	   (assign, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_MEDIUM),
        ]),
	  ("dplmc_toggle_gold_changes_c",[
		(eq, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_MEDIUM),
		],"Set economic & behavioral changes to high/experimental (current mode: medium)",
       [
	 	   (assign, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_HIGH),
        ]),
	  ("dplmc_toggle_gold_changes_d",[
		(eq, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_HIGH),
		],"Disable economic & behavioral changes (current mode: high/experimental)",
       [
	 	   (assign, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_DISABLE),
        ]),
      ("dplmc_reset_gold_changes",
		[(neq, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_DISABLE),
 		 (neq, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_LOW),
		 (neq, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_MEDIUM),
		 (neq, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_HIGH),
		 (assign, reg0, "$g_dplmc_gold_changes"),],
			"You used a saved game from another mod: g_dplmc_gold_changes = {reg0} (click to reset)",
       [
           (assign, "$g_dplmc_gold_changes", 0),
           (jump_to_menu, "mnu_dplmc_preferences"),
        ]),
	#Toggle the default anti-woman prejudice.  This uses the already-existing
	#global variable "$g_disable_condescending_comments", and gives it additional
	#meaning.
		("dplmc_switch_woman_prejudice_1", [
			(this_or_next|eq, "$g_disable_condescending_comments", 0),
			(eq, "$g_disable_condescending_comments", 1)],
			"Change prejudice level (current level is default)",
			[(val_add, "$g_disable_condescending_comments", 2),
			(jump_to_menu, "mnu_dplmc_preferences"),]),
		("dplmc_switch_woman_prejudice_2", [
			(this_or_next|eq, "$g_disable_condescending_comments", 2),
			(eq, "$g_disable_condescending_comments", 3)],
			"Change prejudice level (current level is off)",
			[(val_sub, "$g_disable_condescending_comments", 4),
			(jump_to_menu, "mnu_dplmc_preferences"),]),
		("dplmc_switch_woman_prejudice_3", [
			(this_or_next|eq, "$g_disable_condescending_comments", -1),
			(eq, "$g_disable_condescending_comments", -2)],
			"Change prejudice level (current level is high)",
			[(val_add, "$g_disable_condescending_comments", 2),
			(jump_to_menu, "mnu_dplmc_preferences"),]),
##diplomacy end+
      ("dplmc_back",[],"Back...",
       [
           (jump_to_menu, "mnu_camp"),
        ]),
     ]
  ),
("notification_give_vassal_gift",0, #Jinnai 
    "{s4} is recognizing your loyal service as a vassal by rewarding you with a {s1}.",
    "none",
    [
      (faction_get_slot, ":faction_leader", "$players_kingdom", slot_faction_leader),
      (str_store_troop_name, s4, ":faction_leader"),
      (str_store_item_name, s1, "$g_notification_menu_var1"),
      (troop_add_items, "trp_player", "$g_notification_menu_var1", 1),
      (set_fixed_point_multiplier, 100),
      (position_set_x, pos0, 55),
      (position_set_y, pos0, 20),
      (position_set_z, pos0, 100),
      (set_game_menu_tableau_mesh, "tableau_troop_note_mesh", ":faction_leader", pos0),
      ],
    [
      ("continue",[],"Continue...",
       [(change_screen_return),
        ]),
     ]
  ),
]
