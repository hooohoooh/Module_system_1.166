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

game_menus_gekokujo = [
  #gekokujo 3.0 cheat menu consolidation end
  
  #gekokujo 3.0 all companion report start
  ("gekokujo_companions",0,
   "{s1}",
   "none",
   [
    (str_clear, s1),
	
	(try_for_range, ":companion", companions_begin, fort_companions_end),
	  (str_store_troop_name, s2, ":companion"),
	  
	  (try_begin),
		(main_party_has_troop, ":companion"), #companion is currently in the party
		(str_store_string, s3, "@In {playername}'s party"),
	  (else_try),
	    (is_between, ":companion", companions_begin, companions_end), #this only applies to normal companions
	    (troop_slot_ge, ":companion", slot_troop_cur_center, 1), #companion is waiting at an inn
		(troop_get_slot, ":cur_center", ":companion", slot_troop_cur_center),
		(str_store_party_name, s3, ":cur_center"),
		(str_store_string, s3, "@{s3} Inn"),
	  (else_try),
	    (is_between, ":companion", fort_companions_begin, fort_companions_end), #this only applies to fort companions
		(troop_get_slot, ":cur_center", ":companion", slot_troop_home),
		(neg|party_slot_eq, ":cur_center", slot_fort_npc_2_state, 3), #companion has not joined
		(neg|party_slot_eq, ":cur_center", slot_fort_npc_2_state, 4), #companion is not a lord
		(str_store_party_name, s3, ":cur_center"),
	  (else_try),
	    (troop_slot_ge, ":companion", slot_troop_prisoner_of_party, 0), #companion is imprisoned
	    (troop_get_slot, ":cur_center", ":companion", slot_troop_prisoner_of_party),
		(try_begin),
		  (party_is_active, ":cur_center"),
		  (str_store_party_name, s3, ":cur_center"),
		  (str_store_string, s3, "@{s3} Prison"),
		(else_try),
		  (str_store_string, s3, "@Captured (Travelling)"),
		(try_end),
	  (else_try),
	    (troop_slot_ge, ":companion", slot_troop_current_mission, 1), #companion is on or returning from mission
		(str_store_string, s3, "@On a mission/returning from mission"),
	  (else_try),
		(troop_slot_eq, ":companion", slot_troop_occupation, slto_kingdom_hero), #companion is a lord
		(str_store_string, s3, "@General"),
	  (try_end),
	  
	  (str_store_string, s1, "@{s1}^{s2}: {s3}"),
	(try_end),
    ],
    [
      ("continue",[],"Back to Gekokujo cheat menu.",
       [(jump_to_menu, "mnu_cheat_gekokujo"),
        ]
       ),
      ]
  ),
  #gekokujo 3.1 new scenes end
  
  #gekokujo 3.1 biography page start
  ("gekokujo_bio",0,
    "{s1}",
    "none",
    [
      (str_clear, s1),
	  (assign, reg3, "$character_gender"),
	  
	  #family background
	  (try_begin),
	    (eq, "$background_type", cb_noble), #kuge
		(str_store_string, s1, "@{playername} came from a family of court nobility in Kyoto's Imperial court."),
	  (else_try),
	    (eq, "$background_type", cb_nomad), #jizamurai
		(str_store_string, s1, "@{playername} came from a family of country samurai."),
	  (else_try),
	    (eq, "$background_type", cb_merchant), #travelling merchant
		(str_store_string, s1, "@{playername} came from a family of travelling merchants."),
	  (else_try),
	    (eq, "$background_type", cb_guard), #ashigaru
		(str_store_string, s1, "@{playername} came from a family of common ashigaru retainers that served in the armies of the samurai."),
	  (else_try),
	    (eq, "$background_type", cb_forester), #hunter
		(str_store_string, s1, "@{playername} was raised in the wilderness by a family that lived off the land."),
	  (else_try),
	    (eq, "$background_type", cb_thief), #thief
		(str_store_string, s1, "@{playername}'s family was supported by {reg3?her:his} father's criminal activities."),
	  (try_end),
	  
	  #childhood
	  (str_store_string, s1, "@{s1} Growing up, {reg3?she:he}"),
	  (try_begin),
	    (eq, "$background_answer_2", cb2_page), #Daimyo's attendant
		(eq,"$character_gender",tf_male),
		(str_store_string, s1, "@{s1} joined the household of a great samurai family as an attendant to the lord."),
	  (else_try),
	    (eq, "$background_answer_2", cb2_page), #Noblewoman's attendant (kyoto option)
		(eq, "$background_type", cb_noble),
		(eq,"$character_gender",tf_female),
		(str_store_string, s1, "@{s1} joined the household of a great aristocratic family as an attendant to the lady of the house."),
	  (else_try),
	    (eq, "$background_answer_2", cb2_page), #Noblewoman's attendant (everywhere else)
		(eq,"$character_gender",tf_female),
		(str_store_string, s1, "@{s1} joined the household of a great samurai family as an attendant to the lady of the house."),
	  (else_try),
	    (eq, "$background_answer_2", cb2_apprentice), #Craftman's apprentice
		(str_store_string, s1, "@{s1} learned a craft and apprenticed under a master until {reg3?she:he} could earn her own way."),
	  (else_try),
	    (eq, "$background_answer_2", cb2_merchants_helper), #Shop assistant
		(str_store_string, s1, "@{s1} apprenticed under a trader until {reg3?she:he} could earn her own way."),
	  (else_try),
	    (eq, "$background_answer_2", cb2_urchin), #Street urchin
		(str_store_string, s1, "@{s1} lived on the streets, surviving by begging and stealing."),
	  (else_try),
	    (eq, "$background_answer_2", cb2_steppe_child), #Mountain child
		(str_store_string, s1, "@{s1} lived deep in the mountains, learning how to survive, discovering its secrets."),
	  (try_end),
	  
	  #coming of age
	  (str_store_string, s1, "@{s1}^^After {reg3?she:he} came of age, {reg3?she:he}"),
	  (try_begin),
	    (eq, "$background_answer_3", cb3_squire), #Armed retainer
		(str_store_string, s1, "@{s1} swore fealty to a provincial warlord, guarding his castle and fighting his battles."),
	  (else_try),
	    (eq, "$background_answer_3", cb3_lady_in_waiting), #Court lady in kyoto
		(str_store_string, s1, "@{s1} joined the Emperor's court in Kyoto, helping preserving its ancient customs and what little of its prestige remained."),
	  (else_try),
	    (eq, "$background_answer_3", cb3_student), #Travelling musician
		(str_store_string, s1, "@{s1} wandered across the country, playing music and entertaining to earn just enough to live another day."),
	  (else_try),
	    (eq, "$background_answer_3", cb3_student), #Monk
		(str_store_string, s1, "@{s1} joined a Buddhist monastery, training his body and spirit, strengthening his faith and the power of his sect."),
	  (else_try),
	    (eq, "$background_answer_3", cb3_miko), #Miko
		(str_store_string, s1, "@{s1} became a Miko at a Shinto shrine, helping connect the people of her community with the world of the gods."),
	  (else_try),
	    (eq, "$background_answer_3", cb3_peddler), #Peddler
		(str_store_string, s1, "@{s1} peddled trinkets and wares in villages across the country."),
	  (else_try),
	    (eq, "$background_answer_3", cb3_craftsman), #Smith
		(str_store_string, s1, "@{s1} set up shop as a smith in a castle town, forging and repairing tools for the other craftsmen, and weapons and armor for the local lord."),
	  (else_try),
	    (eq, "$background_answer_3", cb3_poacher), #Poacher
		(str_store_string, s1, "@{s1} lived off the land like a hermit, only returning occasionally to civilization to sell the furs and meat of game animals."),
	  (try_end),
	  
	  #call to adventure
	  (str_store_string, s1, "@{s1}^^But it was not to last."),
	  (try_begin),
	    (eq, "$background_answer_4", cb4_revenge),
		(str_store_string, s1, "@{s1} A great wrong was done to {playername}, and {reg3?she:he} had to leave {reg3?her:his} life behind until {reg3?she:he} was powerful enough to right it..."),
	  (else_try),
	    (eq, "$background_answer_4", cb4_loss),
		(str_store_string, s1, "@{s1} {playername} lost someone precious to {reg3?her:him}. Rather than staying where {reg3?she:he} was and letting {reg3?her:his} emotional wound to fester, {reg3?she:he} started {reg3?her:his} life anew..."),
	  (else_try),
	    (eq, "$background_answer_4", cb4_wanderlust),
		(str_store_string, s1, "@{s1} A desire to see the world burned inside {playername}, and {reg3?she:he} had to leave {reg3?her:his} life behind to see it all..."),
	  (else_try),
	    (eq, "$background_answer_4", cb4_disown),
		(str_store_string, s1, "@{s1} Suddenly and without warning, it was all taken away from {reg3?her:him}. Friends became enemies. Family became strangers. {playername} was all alone in the world..."),
	  (else_try),
	    (eq, "$background_answer_4", cb4_greed),
		(str_store_string, s1, "@{s1} {playername} knew {reg3?she:he} was destined to be great. {reg3?She:he} decided one day to stop waiting for it, and to fulfill it with {reg3?her:his} own will and power..."),
	  (try_end),
    ],
    [
      ("continue",[],"{!}Back to Gekokujo options.", [
         (jump_to_menu, "mnu_camp_gekokujo"),
      ]),
    ]
  ),
  #gekokujo 3.1 begging end
  
  #gekokujo 3.1 crimes against townspeople and villagers start
  (
    "crime",0,
    "{s6}",
    "none",
    [
      (set_background_mesh, "mesh_gekokujo_pic_bandits_2"),
      
      #process crimes
      (try_begin),
        (this_or_next|eq, "$gekokujo_crime_type", 1), #muggings
        (eq, "$gekokujo_crime_type", 2), #pickpocketings
        
        (try_begin),
          (eq, "$gekokujo_crime_result", 1), #the player succeeded
          
          (store_random_in_range, reg10, 0, 10), #stealing from peasants usually gives poor yields
          (try_begin),
            (eq, reg10, 0),
            (store_random_in_range, reg10, 10, 100), #but there is a chance for a jackpot
          (try_end),
          (assign, "$gekokujo_crime_loot", reg10), #save in case you are caught
          (troop_add_gold, "trp_player", reg10),
          
          #muggings may result in lost center relations even on success
          (store_random_in_range, ":chance", 0, 4), #25% chance
          (try_begin),
            (eq, "$gekokujo_crime_type", 1),
            (eq, ":chance", 0),
            (display_message, "@Your mark got a good look at your face and spread the word."),
            (call_script, "script_change_player_relation_with_center", "$current_town", -1),
          (try_end),
          
          (str_store_string, s6, "str_gekokujo_crime_success"),
        (else_try),
          #the player failed
          (call_script, "script_change_player_relation_with_center", "$current_town", -1),
          (str_store_string, s6, "str_gekokujo_crime_fail"),
        (try_end),
      (else_try),
        (eq, "$gekokujo_crime_type", 3), #crime type 3 = stalking
        (try_begin),
          (eq, "$gekokujo_crime_result", 1),
          (str_store_string, s6, "str_gekokujo_stalking_success"),
          
          (store_random_in_range, "$gekokujo_crime_target", 0, 4), #determine target 0 to 3
          #display target
          (try_begin),
            (is_between, "$g_encountered_party", towns_begin, towns_end), #in town
            (assign, ":target", "str_gekokujo_burglary_town_1"),
          (else_try),
            #in a village
            (assign, ":target", "str_gekokujo_burglary_village_1"),
          (try_end),
          (val_add, ":target", "$gekokujo_crime_target"),
          (str_store_string, s6, ":target"),
          
          #display odds of success
          (store_skill_level, reg12, "skl_looting", "trp_player"),  #skl_looting to steal
          (store_skill_level, reg13, "skl_spotting", "trp_player"),  #skl_spotting to avoid battle
          
          #stealing is 20-100%
          (val_mul, reg12, 8),
          (val_add, reg12, 20),
          
          #avoiding battle is 30-100%
          (val_mul, reg13, 7),
          (val_add, reg13, 30),
          
          (str_store_string, s6, "str_gekokujo_burglary_odds"),
          
        (else_try),
          #the player failed
          (str_store_string, s6, "str_gekokujo_stalking_fail"), #no consequences except wasted time
        (try_end),
      (else_try),
        (eq, "$gekokujo_crime_type", 4), #crime type 4 = burglary attempt
        (try_begin),
          (eq, "$gekokujo_crime_result", 1),
          (try_begin),
            (is_between, "$g_encountered_party", towns_begin, towns_end), #in town
            (try_begin),
              (eq, "$gekokujo_crime_target", 0),
              (store_random_in_range, reg10, 10, 101), #tenements give 10 to 100
            (else_try),
              (eq, "$gekokujo_crime_target", 1),
              (store_random_in_range, reg10, 100, 251), #shops give 100 to 250
            (else_try),
              (eq, "$gekokujo_crime_target", 2),
              (store_random_in_range, reg10, 250, 501), #merchant mansions give 250 to 500
            (else_try),
              (eq, "$gekokujo_crime_target", 3),
              (store_random_in_range, reg10, 100, 651), #samurai mansions give 100 to 650
            (try_end),
          (else_try),
            #in a village
            (store_random_in_range, reg10, 5, 21), #all villagers give 5 to 20
          (try_end),
          (assign, "$gekokujo_crime_loot", reg10), #save in case you are caught
          (troop_add_gold, "trp_player", reg10),
          (str_store_string, s6, "str_gekokujo_burglary_success"),
        (else_try),
          #the player failed
          (str_store_string, s6, "str_gekokujo_burglary_fail"),
        (try_end),
      (try_end),
      
      #process honor penalty
      (try_begin),
        (eq, "$gekokujo_crime_type", 1), #muggings no matter what
        (call_script, "script_change_player_honor", -1),
      (else_try),
        (eq, "$gekokujo_crime_type", 2), #pickpocketings that are caught
        (eq, "$gekokujo_getaway_result", 0),
        (call_script, "script_change_player_honor", -1),
      (else_try),
        (eq, "$gekokujo_crime_type", 4), #burglary attempts that result in battles
        (eq, "$gekokujo_getaway_result", 0),
        (call_script, "script_change_player_honor", -1),
      (try_end),
      
      #process NPC objection
      (try_begin),
        (this_or_next|eq, "$gekokujo_crime_type", 1), #muggings
        (eq, "$gekokujo_crime_type", 4), #burglary attempt
        (call_script, "script_objectionable_action", tmt_humanitarian, "str_loot_village"),
      (else_try),
        (eq, "$gekokujo_crime_type", 2), #pickpocketings
        (call_script, "script_objectionable_action", tmt_humanitarian, "str_steal_from_villagers"),
      (try_end),
      
      #process getaways
      (try_begin),
        (neq, "$gekokujo_crime_type", 3), #stalking doesn't count
        (eq, "$gekokujo_getaway_result", 1),
        (str_store_string, s6, "str_gekokujo_getaway_success"),
      (else_try),
        #if the player does not get away, figure out who they have to fight
        (neq, "$gekokujo_crime_type", 3), #stalking doesn't count
        
        (try_begin),
          (eq, "$gekokujo_crime_type", 4), #burglaries
          
          (try_begin),
            (is_between, "$g_encountered_party", towns_begin, towns_end), #in town
            (assign, ":target", "str_gekokujo_burglary_fight_town_1_easy"),
          (else_try),
            #in a village
            (assign, ":target", "str_gekokujo_burglary_fight_village_1_easy"),
          (try_end),
          (val_add, ":target", "$gekokujo_crime_target"),
          
          (store_random_in_range, "$gekokujo_crime_target_difficulty", 0, 2), #0 = easy, 1 = hard
          (try_begin),
            (eq, "$gekokujo_crime_target_difficulty", 1),
            (val_add, ":target", 4),
          (try_end),
          
          (str_store_string, s7, ":target"),
        (else_try),
          #muggings and pickpocketings
          (try_begin),
            (is_between, "$g_encountered_party", towns_begin, towns_end), #towns have guards
            (str_store_string, s7, "str_gekokujo_crime_fight_town_type"),
          (else_try),
            #villages have angry mobs
            (str_store_string, s7, "str_gekokujo_crime_fight_village_type"),
          (try_end),
        (try_end),
        
        (str_store_string, s6, "str_gekokujo_getaway_fail"),
      (try_end),
      
    ],
    [
      ("burglary_recon_success_rob", 
        [
          (eq, "$gekokujo_crime_type", 3), #stalking success
          (eq, "$gekokujo_crime_result", 1),
        ], 
        "Wait a little then go for it", 
        [
          (assign, "$gekokujo_crime_type", 4),
          
          #assign crime success/fail
          (store_random_in_range, ":crime_roll", 0, 100),
          (try_begin),
            (gt, reg12, ":crime_roll"),
            (assign, "$gekokujo_crime_result", 1),
          (else_try),
            (assign, "$gekokujo_crime_result", 0),
          (try_end),
          
          #assign getaway success/fail
          (store_random_in_range, ":crime_roll", 0, 100),
          (try_begin),
            (gt, reg13, ":crime_roll"),
            (assign, "$gekokujo_getaway_result", 1),
          (else_try),
            (assign, "$gekokujo_getaway_result", 0),
          (try_end),
          
          (jump_to_menu, "mnu_crime"),
        ]),
      ("burglary_recon_success_leave", 
        [
          (eq, "$gekokujo_crime_type", 3), #stalking success
          (eq, "$gekokujo_crime_result", 1),
        ], 
        "Leave", 
        [
          (rest_for_hours, 2, 2, 0),
          (change_screen_return),
        ]),
      ("crime_getaway_success", 
        [          
          (eq, "$gekokujo_getaway_result", 1),
          
          #do not show when stalking succeeds
          (assign, ":continue", 1),
          (try_begin),
            (eq, "$gekokujo_crime_type", 3),
            (eq, "$gekokujo_crime_result", 1),
            (val_sub, ":continue", 1),
          (try_end),
          (gt, ":continue", 0),
        ], 
        "Hide until things cool off", 
        [
          (rest_for_hours, 2, 2, 0),
          (change_screen_return),
        ]),
      ("crime_getaway_fail", 
        [
          (eq, "$gekokujo_getaway_result", 0),
        ], 
        "Fight your way out", 
        [
          (assign, "$gekokujo_encounter_mode", 3), #3 = getaway
          (set_jump_mission, "mt_gekokujo_encounter"),
          
          (try_begin),
            (this_or_next|eq, "$gekokujo_crime_type", 1), #muggings
            (eq, "$gekokujo_crime_type", 2), #pickpocketings
          
            (try_begin),
              (is_between, "$current_town", towns_begin, towns_end),
              (assign, ":scene", "scn_encounter_alley"),
              (store_faction_of_party, ":town_faction", "$current_town"),
              (faction_get_slot, ":enemy_1", ":town_faction", slot_faction_tier_1_troop),
              (faction_get_slot, ":enemy_2", ":town_faction", slot_faction_tier_3_troop),
              (store_random_in_range, ":enemy_1_count", 1, 4), #1 to 3 tier 1 guards
              (store_random_in_range, ":enemy_2_count", 0, 2), #0 to 1 tier 3 guards
            (else_try),
              (assign, ":scene", "scn_encounter_farm"), #change to a random forest encounter
              (assign, ":enemy_1", "trp_farmer"),
              (assign, ":enemy_2", "trp_peasant_woman"),
              (store_random_in_range, ":enemy_1_count", 1, 9), #2 to 8 peasant men
              (store_random_in_range, ":enemy_2_count", 0, 4), #0 to 3 peasant women
            (try_end),
          (else_try),
            (eq, "$gekokujo_crime_type", 4), #burglaries
            (try_begin),
              (is_between, "$current_town", towns_begin, towns_end), #towns
              
              (try_begin),
                (eq, "$gekokujo_crime_target", 0), #tenement
                (assign, ":scene", "scn_encounter_alley"),
                (try_begin),
                  (eq, "$gekokujo_crime_target_difficulty", 0), #easy
                  (assign, ":enemy_1", "trp_town_walker_1"),
                  (assign, ":enemy_2", "trp_town_walker_2"),
                  (store_random_in_range, ":enemy_1_count", 0, 2), #0-1 trp_town_walker_1
                  (store_random_in_range, ":enemy_2_count", 1, 3), #1-2 trp_town_walker_2
                (else_try),
                  #hard
                  (assign, ":enemy_1", "trp_town_walker_1"),
                  (assign, ":enemy_2", "trp_town_walker_2"),
                  (store_random_in_range, ":enemy_1_count", 1, 6), #1-5 trp_town_walker_1
                  (store_random_in_range, ":enemy_2_count", 1, 6), #1-5 trp_town_walker_2
                (try_end),
              (else_try),
                (eq, "$gekokujo_crime_target", 1), #shop
                (assign, ":scene", "scn_encounter_shop"),
                (try_begin),
                  (eq, "$gekokujo_crime_target_difficulty", 0), #easy
                  (assign, ":enemy_1", "trp_town_walker_1"),
                  (assign, ":enemy_2", "trp_town_walker_2"),
                  (store_random_in_range, ":enemy_1_count", 0, 3), #0-2 trp_town_walker_1
                  (store_random_in_range, ":enemy_2_count", 1, 4), #1-3 trp_town_walker_2
                (else_try),
                  #hard
                  (assign, ":enemy_1", "trp_town_walker_1"),
                  (assign, ":enemy_2", "trp_town_walker_2"),
                  (store_random_in_range, ":enemy_1_count", 2, 7), #2-6 trp_town_walker_1
                  (store_random_in_range, ":enemy_2_count", 2, 7), #2-6 trp_town_walker_2
                (try_end),
              (else_try),
                (eq, "$gekokujo_crime_target", 2), #merchant mansion
                (assign, ":scene", "scn_encounter_mansion"),
                (try_begin),
                  (eq, "$gekokujo_crime_target_difficulty", 0), #easy
                  (assign, ":enemy_1", "trp_town_walker_1"),
                  (assign, ":enemy_2", "trp_town_walker_2"),
                  (store_random_in_range, ":enemy_1_count", 2, 7), #2-6 trp_town_walker_1
                  (store_random_in_range, ":enemy_2_count", 2, 7), #2-6 trp_town_walker_2
                (else_try),
                  #hard
                  (assign, ":enemy_1", "trp_hired_guard"),
                  (assign, ":enemy_2", "trp_yojimbo"),
                  (store_random_in_range, ":enemy_1_count", 1, 5), #1-4 trp_hired_guard
                  (store_random_in_range, ":enemy_2_count", 0, 3), #0-2 trp_yojimbo
                (try_end),
              (else_try),
                (eq, "$gekokujo_crime_target", 3), #samurai mansion
                (assign, ":scene", "scn_encounter_mansion"),
                (try_begin),
                  (eq, "$gekokujo_crime_target_difficulty", 0), #easy
                  (assign, ":enemy_1", "trp_town_walker_1"),
                  (assign, ":enemy_2", "trp_town_walker_2"),
                  (store_random_in_range, ":enemy_1_count", 2, 7), #2-6 trp_town_walker_1
                  (store_random_in_range, ":enemy_2_count", 2, 7), #2-6 trp_town_walker_2
                (else_try),
                  #hard
                  (store_faction_of_party, ":town_faction", "$current_town"),
                  (faction_get_slot, ":enemy_1", ":town_faction", slot_faction_tier_1_troop),
                  (faction_get_slot, ":enemy_2", ":town_faction", slot_faction_tier_3_troop),
                  (store_random_in_range, ":enemy_1_count", 1, 5), #1 to 4 tier 1 guards
                  (store_random_in_range, ":enemy_2_count", 0, 3), #0 to 2 tier 3 guards
                (try_end),
              (try_end),
            (else_try),
              #villages
              (try_begin),
                (eq, "$gekokujo_crime_target", 0), #farmhouse
                (assign, ":scene", "scn_encounter_farm"),
              (else_try),
                (eq, "$gekokujo_crime_target", 1), #road
                (assign, ":scene", "scn_encounter_road"),
              (else_try),
                (eq, "$gekokujo_crime_target", 2), #forest
                (assign, ":scene", "scn_encounter_forest"),
              (else_try),
                (eq, "$gekokujo_crime_target", 3), #river
                (assign, ":scene", "scn_encounter_river"),
              (try_end),
              #easy: 1 trp_farmer or trp_peasant_woman
              #hard: 1-4 trp_farmer, 1-4 trp_peasant_woman
              (try_begin),
                (eq, "$gekokujo_crime_target_difficulty", 0), #easy
                (store_random_in_range, ":random", 0, 2), #0 = man, 1 = woman
                (try_begin),
                  (eq, ":random", 0),
                  (assign, ":enemy_1", "trp_farmer"),
                (else_try),
                  (assign, ":enemy_1", "trp_peasant_woman"),
                (try_end),
                (assign, ":enemy_1_count", 1),
                
                (assign, ":enemy_2", "trp_farmer"),
                (assign, ":enemy_2_count", 0),
              (else_try),
                #hard
                (assign, ":enemy_1", "trp_farmer"),
                (assign, ":enemy_2", "trp_peasant_woman"),
                (store_random_in_range, ":enemy_1_count", 1, 5), #1 to 4 peasant men
                (store_random_in_range, ":enemy_2_count", 1, 5), #1 to 4 peasant women
              (try_end),
            (try_end),
          (try_end),
          
          (modify_visitors_at_site, ":scene"),
          (reset_visitors),
          
          (set_visitor, 2, "trp_player"),
          (set_visitors, 0, ":enemy_1", ":enemy_1_count"),
          (try_begin),
            (gt, ":enemy_2_count", 0),
            (set_visitors, 1, ":enemy_2", ":enemy_2_count"),
          (try_end),
          
          (jump_to_scene, ":scene"),
          (change_screen_mission),
        ]),
    ],
  ),
  
  (
    "getaway_failed",mnf_disable_all_keys,
    "{s4}",
    "none",
    [
      (store_troop_gold, ":total_gold", "trp_player"),
      (val_sub, ":total_gold", "$gekokujo_crime_loot"),
      (store_div, ":gold_loss", ":total_gold", 30),
      (store_random_in_range, ":random_loss", 40, 100),
      (val_add, ":gold_loss", ":random_loss"),
      (val_min, ":gold_loss", ":total_gold"),
      (val_add, ":gold_loss", "$gekokujo_crime_loot"),
      (troop_remove_gold, "trp_player",":gold_loss"),
      
      (try_begin),
        (eq, "$gekokujo_crime_type", 4), #burglary
        (is_between, "$g_encountered_party", towns_begin, towns_end), #in town
        (this_or_next|eq, "$gekokujo_crime_target", 2), #merchant mansion
        (eq, "$gekokujo_crime_target", 3), #samurai mansion
        (eq, "$gekokujo_crime_target_difficulty", 1), #hard (guards)
        (str_store_string, s4, "str_gekokujo_burglary_fight_guards_fail"),
      (else_try),
        (eq, "$gekokujo_crime_type", 4), #burglary
        (is_between, "$g_encountered_party", towns_begin, towns_end), #in town
        (str_store_string, s4, "str_gekokujo_burglary_fight_town_fail"),
      (else_try),
        (eq, "$gekokujo_crime_type", 4), #burglary
        (is_between, "$g_encountered_party", towns_begin, towns_end), #in a village
        (str_store_string, s4, "str_gekokujo_burglary_fight_village_fail"),
      (else_try),
        #pickpockets/mugging (town)
        (is_between, "$g_encountered_party", towns_begin, towns_end), #towns have guards
        (str_store_string, s4, "str_gekokujo_crime_fight_town_fail"),
      (else_try),
        #pickpockets/mugging (village)
        #villages have angry mobs
        (str_store_string, s4, "str_gekokujo_crime_fight_village_fail"),
      (try_end),
      
      #if you killed a guard rather than using a blunt weapon, you lose faction relations
      #if you killed a villager, you lose extra center relation
      (assign, ":relation", -1),
      (try_begin),
        (gt, "$gekokujo_crime_getaway_lethal", 0),
        
        (try_begin),
          (is_between, "$g_encountered_party", towns_begin, towns_end),
          (store_faction_of_party, ":center_faction", "$current_town"),
          (call_script, "script_change_player_relation_with_faction", ":center_faction", -1),
        (else_try),
          (val_add, ":relation", -2),
          (call_script, "script_objectionable_action", tmt_humanitarian, "str_murder_merchant"), #you're the bad guy
        (try_end),
        
        (assign, "$gekokujo_crime_getaway_lethal", 0), #reset
      (try_end),
      (call_script, "script_change_player_relation_with_center", "$current_town", ":relation"),
      
      (assign, "$gekokujo_encounter_mode", 0), #reset
    ],
    [
      ("continue",[],"Continue...",
        [
          (rest_for_hours, 2, 2, 0),
          (change_screen_return),
        ]),
    ],
  ),
  (
    "getaway_succeeded",mnf_disable_all_keys,
    "{s5}",
    "none",
    [
      (try_begin),
        (eq, "$gekokujo_crime_type", 4), #burglary
        (is_between, "$g_encountered_party", towns_begin, towns_end), #in town
        (this_or_next|eq, "$gekokujo_crime_target", 2), #merchant mansion
        (eq, "$gekokujo_crime_target", 3), #samurai mansion
        (eq, "$gekokujo_crime_target_difficulty", 1), #hard (guards)
        (str_store_string, s5, "str_gekokujo_burglary_fight_guards_success"),
        (assign, ":xp_reward", 200),
      (else_try),
        (eq, "$gekokujo_crime_type", 4), #burglary
        (is_between, "$g_encountered_party", towns_begin, towns_end), #in town
        (str_store_string, s5, "str_gekokujo_burglary_fight_town_success"),
        (assign, ":xp_reward", 50),
      (else_try),
        (eq, "$gekokujo_crime_type", 4), #burglary
        #in a village
        (str_store_string, s5, "str_gekokujo_burglary_fight_village_success"),
        (assign, ":xp_reward", 50),
      (else_try),
        #pickpockets/mugging (town)
        (is_between, "$g_encountered_party", towns_begin, towns_end), #towns have guards
        (str_store_string, s5, "str_gekokujo_crime_fight_town_success"),
        (assign, ":xp_reward", 250),
      (else_try),
        #pickpockets/mugging (village)
        #villages have angry mobs
        (str_store_string, s5, "str_gekokujo_crime_fight_village_success"),
        (assign, ":xp_reward", 50),
      (try_end),
      
      (add_xp_to_troop, ":xp_reward", "trp_player"),
      
      (call_script, "script_change_player_relation_with_center", "$current_town", -2),
      
      
      #if you killed a town guard rather than using a blunt weapon, you lose faction relations
      #if you killed a townsman, villager, or private guard, you lose even more center relation
      (try_begin),
        (gt, "$gekokujo_crime_getaway_lethal", 0),
        
        (try_begin),
          (neq, "$gekokujo_crime_type", 4), #non-burglary town fight means town guard escape attempt
          (is_between, "$g_encountered_party", towns_begin, towns_end),
          (store_faction_of_party, ":center_faction", "$current_town"),
          (call_script, "script_change_player_relation_with_faction", ":center_faction", -1),
        (else_try),
          (call_script, "script_change_player_relation_with_center", "$current_town", -2),
        (try_end),
        
        (assign, "$gekokujo_crime_getaway_lethal", 0), #reset
      (try_end),
      
      (assign, "$gekokujo_encounter_mode", 0), #reset
    ],
    [
      ("continue",[],"Continue...",
        [
          (rest_for_hours, 2, 2, 0),
          (change_screen_return),
        ]),
    ],
  ),
  #gekokujo 3.1 crimes against townspeople and villagers end
  
  #gekokujo 3.1 labor start
  (
    "labor",0,
    "{s20} {s22} {s23} {s24}", #s20 = employer, #s22 = description, #s23 = skill bonus, #s24 = notes
    "none",
    [
      (try_begin),
        (is_between, "$current_town", towns_begin, towns_end),
        
        (set_background_mesh, "mesh_gekokujo_pic_town"),
        
        #random employer (and work site)
        #s21 is the placename associated with the employer, used by #s22 for towns
        (store_random_in_range, ":seed", 0, 40),
        (store_add, ":selection", "str_gekokujo_labor_town_employer_1", ":seed"),
        (str_store_string, s20, ":selection"),
        (store_add, ":selection", "str_gekokujo_labor_town_site_1", ":seed"),
        (str_store_string, s21, ":selection"),
        
        #random description
        (store_random_in_range, ":seed", 0, 10),
        (store_add, ":selection", "str_gekokujo_labor_town_need_1", ":seed"),
        (str_store_string, s22, ":selection"),
        
        #notes
        (str_store_string, s24, "str_gekokujo_labor_town_notes"),
      (else_try),
        (set_background_mesh, "mesh_gekokujo_pic_village"),
        
        #random employer
        (store_random_in_range, ":seed", 0, 10),
        (store_add, ":selection", "str_gekokujo_labor_village_employer_1", ":seed"),
        (str_store_string, s20, ":selection"),
        
        #random description
        (store_random_in_range, ":seed", 0, 10),
        (store_add, ":selection", "str_gekokujo_labor_village_need_1", ":seed"),
        (str_store_string, s22, ":selection"),
        
        #notes
        (str_store_string, s24, "str_gekokujo_labor_village_notes"),
      (try_end),
      
      #random skill bonus (50% chance that it is nothing)
      #reg30 is where the skill is stored until the job is accepted
      (store_random_in_range, ":seed", 0, 2),
      (try_begin),
        (eq, ":seed", 1),
        (store_random_in_range, ":seed", 1, 10),
      (try_end),
      
      (try_begin),
        (is_between, "$current_town", towns_begin, towns_end),
        (store_add, ":selection", "str_gekokujo_labor_town_skill_1", ":seed"),
      (else_try),
        (store_add, ":selection", "str_gekokujo_labor_village_skill_1", ":seed"),
      (try_end),
      (str_store_string, s23, ":selection"),
      
      (try_begin),
        (eq, ":seed", 1),
        (assign, reg30, "skl_ironflesh"),
      (else_try),
        (eq, ":seed", 2),
        (assign, reg30, "skl_power_strike"),
      (else_try),
        (eq, ":seed", 3),
        (assign, reg30, "skl_power_throw"),
      (else_try),
        (eq, ":seed", 4),
        (assign, reg30, "skl_power_draw"),
      (else_try),
        (eq, ":seed", 5),
        (is_between, "$current_town", towns_begin, towns_end),
        (assign, reg30, "skl_weapon_master"),
      (else_try),
        (eq, ":seed", 5),
        (assign, reg30, "skl_shield"),
      (else_try),
        (eq, ":seed", 6),
        (assign, reg30, "skl_athletics"),
      (else_try),
        (eq, ":seed", 7),
        (assign, reg30, "skl_riding"),
      (else_try),
        (eq, ":seed", 8),
        (assign, reg30, "skl_trainer"),
      (else_try),
        (eq, ":seed", 9),
        (is_between, "$current_town", towns_begin, towns_end),
        (assign, reg30, "skl_inventory_management"),
      (else_try),
        (eq, ":seed", 9),
        (assign, reg30, "skl_engineer"),
      (else_try),
        (assign, reg30, -1),
      (try_end),
      
      #skill bonus is (skill level / 3) + 1
      (try_begin),
        (neq, reg30, -1),
        (store_skill_level, ":skill_level", reg30, "trp_player"),
        (val_div, ":skill_level", 3),
        (val_add, ":skill_level", 1),
        #(val_mul, reg31, ":skill_level"),
      (else_try),
        (assign, ":skill_level", 1),
      (try_end),
      
      #base pay
      #towns: 5 mon x skill bonus, which is (skill level / 3) + 1
      #villages: 1 item (skill bonus gives relations)
      (try_begin),
        (is_between, "$current_town", towns_begin, towns_end),
        (assign, reg31, 5), #reg31 = base wage, for towns
        (val_mul, reg31, ":skill_level"), #multiply by skill bonus
        (assign, reg34, 0), #reg34 = relationship bonus (unused for towns)
      (else_try),
        (assign, reg31, 1), #reg31 = items, for towns
        (assign, reg34, ":skill_level"), #villages get relationship increases
      (try_end),
      
      #other workers
      (party_get_num_companion_stacks, ":num_stacks", "p_main_party"),
      (assign, reg32, 0), #reg32 = number of additional workers
      (assign, reg33, 0), #reg33 = number of samurai
      (try_for_range, ":cur_stack", 1, ":num_stacks"), #go through every party member except player
        (party_stack_get_troop_id, ":return_troop", "p_main_party", ":cur_stack"),
        (party_stack_get_size, ":stack_size", "p_main_party", ":cur_stack"),
        (try_begin),
          (is_between, ":return_troop", samurai_troops_begin, samurai_troops_end),
          (val_add, reg33, ":stack_size"),
        (else_try),
          (val_add, reg32, ":stack_size"),
          (party_stack_get_num_wounded, ":stack_size", "p_main_party", ":cur_stack"),
          (val_sub, reg32, ":stack_size"),
        (try_end),
      (try_end),
            
      (try_begin),
        (is_between, "$current_town", towns_begin, towns_end),
        (assign, ":bonus", reg32), #+1 mon per worker
      (else_try),
        (store_div, ":bonus", reg32, 10), #+1 item per 10 workers
      (try_end),
      (val_add, reg31, ":bonus"),
      
      #notes
      (try_begin),
        (is_between, "$current_town", towns_begin, towns_end),
        (str_store_string, s24, "str_gekokujo_labor_town_notes"),
      (else_try),
        (str_store_string, s24, "str_gekokujo_labor_village_notes"),
      (try_end),
      
      (try_begin),
        (gt, reg32, 0), #if the player is bringing laborers
        (str_store_string, s24, "str_gekokujo_labor_availability"),
        (try_begin),
          (gt, reg33, 0), #if the player has samurai in addition to laborers
          (str_store_string, s24, "str_gekokujo_labor_samurai"),
        (try_end),
      (try_end),
    ],
    [
      ("work", [], "Take the job.", 
        [
          #(assign, "$gekokujo_labor_skill", reg30),
          #(assign, "$gekokujo_labor_workers", reg32),
          #(assign, "$gekokujo_labor_samurai", reg33),
          (assign, "$gekokujo_labor_pay", reg31),
          (assign, "$gekokujo_labor_extra", reg34),
          (try_begin),
            (is_between, "$current_town", towns_begin, towns_end),
            (rest_for_hours, 8, 20, 0),
          (else_try),
            (rest_for_hours, 72, 20, 0),
          (try_end),
          (assign, "$gekokujo_labor_disable_food", 1), #disable eating and encounters
          (assign, "$auto_enter_town", "$current_town"),
          (assign, "$g_town_visit_after_rest", 1),
          (assign, "$auto_enter_menu_in_center", "mnu_labor_complete"),
          (change_screen_return),
        ]),
      ("wait", [], "Wait for a better job.", 
        [
          (rest_for_hours, 1, 5, 0),
          (assign, "$auto_enter_town", "$current_town"),
          (assign, "$g_town_visit_after_rest", 1),
          (assign, "$auto_enter_menu_in_center", "mnu_labor"),
          (change_screen_return),
        ]),
      ("nevermind", [], "Nevermind...", 
        [
          (try_begin),
            (is_between, "$current_town", towns_begin, towns_end),
            (jump_to_menu, "mnu_town_trade"),
          (else_try),
            (jump_to_menu, "mnu_village"),
          (try_end),
        ]),
    ]
  ),
  
  (
    "labor_complete",0,
    "{s10}",
    "none",
    [
      (assign, "$gekokujo_labor_disable_food", 0), #re-enable eating and encounters
      
      (assign, reg31, "$gekokujo_labor_pay"),
      (assign, reg34, "$gekokujo_labor_extra"),
      (try_begin),
        (is_between, "$current_town", towns_begin, towns_end),
        (troop_add_gold, "trp_player", reg31),
        (str_store_string, s10, "str_gekokujo_labor_town_complete"),
      (else_try),
        #select the reward item
        (store_random_in_range, ":seed", 0, 4),
        
        #prevent rice from being a reward if qst_deliver_grain is active in the village
        (try_begin),
          (check_quest_active, "qst_deliver_grain"),
          (quest_slot_eq, "qst_deliver_grain", slot_quest_target_center, "$current_town"),
          (eq, ":seed", 0),
          (store_random_in_range, ":seed", 1, 4),
        (try_end),
        
        #give the reward item
        (try_begin),
          (eq, ":seed", 0),
          (assign, ":reward", "itm_grain"), #rice
        (else_try),
          (eq, ":seed", 1),
          (assign, ":reward", "itm_raw_grapes"), #soybeans
        (else_try),
          (eq, ":seed", 2),
          (assign, ":reward", "itm_cabbages"), #vegetables
        (else_try),
          (assign, ":reward", "itm_apples"), #fruit
        (try_end),
        (troop_add_items, "trp_player", ":reward", reg31),
        
        #display the reward item
        (try_begin),
          (eq, reg31, 1),
          (store_add, ":selection", "str_gekokujo_labor_village_reward_1_singular", ":seed"),
        (else_try),
          (store_add, ":selection", "str_gekokujo_labor_village_reward_1_plural", ":seed"),
        (try_end),
        (str_store_string, s11, ":selection"),
        
        #if there's a bonus, give it as a relationship change
        (try_begin),
          (gt, reg34, 0),
          (call_script, "script_change_player_relation_with_center", "$current_town", reg34),
        (try_end),
        
        (str_store_string, s10, "str_gekokujo_labor_village_complete"),
      (try_end),
    ],
    [
      ("continue", [], "Continue...", 
      [
        (try_begin),
          (is_between, "$current_town", towns_begin, towns_end),
          (jump_to_menu, "mnu_town_trade"),
        (else_try),
          (jump_to_menu, "mnu_village"),
        (try_end),
        #(change_screen_return)
      ]),
    ]
  ),
  #gekokujo 3.1 labor end
  
  #gekokujo 3.1 rebellions start
  (
    "rebellion",0,
    "{s5} loyalists have rebelled, forming armies in the lands around {s6}.",
    "none",
    [
      (set_background_mesh, "mesh_gekokujo_pic_bandits_3"),
      
      (str_store_faction_name, s5, "$gekokujo_rebel_faction"),
      (str_store_party_name, s6, "$gekokujo_rebel_stronghold"),
    ],
    [
      ("continue", [], "Continue...", [(change_screen_return)]),
    ]
  ),
  
  #gekokujo 3.1 ninja rescue start
  (
    "gekokujo_captivity_avoid", mnf_scale_picture,
    "The agents in your party sacrificed their own lives to prevent your capture! They did their duty for you, but did you do your duty for them?",
    "none",
    [
        (play_cue_track, "track_escape"),
		(set_background_mesh, "mesh_gekokujo_pic_escape"),
    ],
    [
      ("continue",[],"Continue...",
       [
           (val_sub, "$gekokujo_rescue_score", 1), #the player themselves costs 1 point
           (val_div, "$gekokujo_rescue_score", 2), #companion heroes cost 2 points each
           (val_max, "$gekokujo_rescue_score", 0), #don't go below 0
           
           #figure out which non-fort npcs got lost
           (try_for_range, ":npc", companions_begin, companions_end),
             (main_party_has_troop, ":npc"),
             (try_begin),
               (gt, "$gekokujo_rescue_score", 0), #if there are still rescueable NPCs
               (assign, ":continue", 0), #save this NPC instead
               (val_sub, "$gekokujo_rescue_score", 1), #lower the count
             (else_try),
               (assign, ":continue", 1),
             (try_end),
             (eq, ":continue", 1),
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
		 
		   #figure out which fort companions get lost
           (try_for_range, ":npc", fort_companions_begin, fort_companions_end),
             (main_party_has_troop, ":npc"),
             (try_begin),
               (gt, "$gekokujo_rescue_score", 0), #if there are still rescueable NPCs
               (assign, ":continue", 0), #save this NPC instead
               (val_sub, "$gekokujo_rescue_score", 1), #lower the count
             (else_try),
               (assign, ":continue", 1),
             (try_end),
             (eq, ":continue", 1),
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
           
           (assign, "$gekokujo_rescue_score", 0), #redundancy department of redundancy, bad coding practices
           
           (store_distance_to_party_from_party, ":nearest_town_dist", "p_town_5", "p_town_9"), #sakai to kiyosu
           (store_distance_to_party_from_party, ":furthest_town_dist", "p_town_5", "p_town_2"), #sakai to mito
           (assign, ":continue", 1),
           (try_for_range, ":town_no", towns_begin, towns_end),
             (eq, ":continue", 1),
             (store_faction_of_party, ":town_fac", ":town_no"),
             (store_relation, ":reln", ":town_fac", "fac_player_faction"),
             (ge, ":reln", 0),
             (store_distance_to_party_from_party, ":dist", ":town_no", "p_main_party"),
             (gt, ":dist", ":nearest_town_dist"),
             (lt, ":dist", ":furthest_town_dist"),
             (assign, ":continue", 0), #find the first one
           (try_end),
           (party_relocate_near_party, "p_main_party", ":town_no", 2),
           
           (assign, "$g_player_is_captive", 0),
           (call_script, "script_set_parties_around_player_ignore_player", 2, 4),
           (assign, "$g_player_icon_state", pis_normal),
           (set_camera_follow_party, "p_main_party"),
           (rest_for_hours, 6, 5, 0), #rest for 6 hours
           (assign, "$g_move_fast", 1), #from diplomacy
           
           (change_screen_return),
        ]),
    ]
  ),
    ("xinzhengfuchengli",mnf_scale_picture,
    "王 政 复 古 大 号 令 颁 布，新 政 府 宣 告 成 立!",
    "none",
    [
		(set_background_mesh, "mesh_dazhengfenghuan"),   
       (try_end),
        ],
    [
		("continue",[],"Continue...",
			[
			(change_screen_return),
			],
		),
	]
),
 ("niaoyufujianzhizhan",mnf_scale_picture,
    "鸟 羽 伏  见  之  战                                                                                                                                   ；自 大 政 奉 还 以 来 ，幕 府 与 新 政 府 的 对 峙 彻 底 破 裂 。 德 川 庆 喜 拒 不 接 受 新 政 府 剥 夺 幕 府 实 权 的 政 令 ， 集 结 幕 府 直 属 精 锐 、 会 津 藩 、 桑 名 藩 等 亲 幕 诸 藩 大 军 ， 自 大 阪 北 上 ， 意 欲 武 力 入 京 、 清 剿 萨 长 倒 幕 势 力 .",
    "none",
    [
		(set_background_mesh, "mesh_niaoyufujian"),   
       (try_end),
        ],
    [
		("continue",[],"Continue...",
			[
			(change_screen_return),
			],
		),
	]
),
]
