# -*- coding: utf-8 -*-
# module_scripts_dk_invasion.py -- auto split from module_scripts.py (feature: Dark Knights 入侵)
# entries: 6 (order preserved within this file)
from header_presentations import *
from header_common import *
from header_operations import *
from module_constants import *
from module_constants import *
from header_parties import *
from header_skills import *
from header_mission_templates import *
from header_items import *
from header_triggers import *
from header_terrain_types import *
from header_music import *
from header_map_icons import *
from ID_animations import *
from ym_gatling import *
from ym_gatling_shop import *
from zhenyinghebing import *
from lco_scripts import lco_scripts
from upgrade_scripts import upgrade_scripts
##diplomacy start+
from module_factions import dplmc_factions_begin, dplmc_factions_end, dplmc_non_generic_factions_begin
##diplomacy end+
from header_presentations import tf_left_align
  #### Autoloot improved by rubik begin
from module_items import *


scripts_dk_invasion = [

  ("create_kingdom_hero_party_dk",
    [
      (store_script_param, ":troop_no", 1),
      (store_script_param, ":center_no", 2),
     
      (store_troop_faction, ":troop_faction_no", ":troop_no"),
      
	  
	  
	 (str_store_faction_name, s4, ":troop_faction_no"),
	 (str_store_troop_name, s5, ":troop_no"),
     # (display_message, "@{!}DEBUG -- Faction {s4} troop fucking {s5}"),
			
      (assign, "$pout_party", -1),
      (set_spawn_radius, 2),
      (spawn_around_party, ":center_no", "pt_kingdom_hero_party"),   
      (assign, "$pout_party", reg0),
      
      (party_set_faction, "$pout_party", ":troop_faction_no"),
      (party_set_slot, "$pout_party", slot_party_type, spt_kingdom_hero_party),
      (call_script, "script_party_set_ai_state", "$pout_party", spai_undefined, -1),
      (troop_set_slot, ":troop_no", slot_troop_leaded_party, "$pout_party"),
      (party_add_leader, "$pout_party", ":troop_no"),
      (str_store_troop_name, s5, ":troop_no"),
      (party_set_name, "$pout_party", "str_s5_s_party"),
      
      (party_set_slot, "$pout_party", slot_party_commander_party, -1), #we need this because 0 is player's party!

      #Setting the flag icon
      #normal_banner_begin
      # (troop_get_slot, ":cur_banner", ":troop_no", slot_troop_banner_scene_prop),
      (try_begin),
        # (gt, ":cur_banner", 0),
        # (val_sub, ":cur_banner", banner_scene_props_begin),
        # (val_add, ":cur_banner", banner_map_icons_begin),
        (party_set_banner_icon, "$pout_party", "icon_banner_01"), ## Tocan Invasion ## Test :cur_banner
      #custom_banner_begin
      #(troop_get_slot, ":flag_icon", ":troop_no", slot_troop_custom_banner_map_flag_type),
      #(try_begin),
      #  (ge, ":flag_icon", 0),
      #  (val_add, ":flag_icon", custom_banner_map_icons_begin),
      #  (party_set_banner_icon, "$pout_party", ":flag_icon"),
      (try_end),

      (try_begin),
        #because of below two lines, lords can only hire more than one party_template(stack) at game start once a time during all game.
        (troop_slot_eq, ":troop_no", slot_troop_spawned_before, 0),
        (troop_set_slot, ":troop_no", slot_troop_spawned_before, 1),
        (assign, ":num_tries", 20), ##Tocan should be the troop size ##Invasion 20
        (try_begin),
          (store_troop_faction, ":troop_kingdom", ":troop_no"),
          (faction_slot_eq, ":troop_kingdom", slot_faction_leader, ":troop_no"),
          (assign, ":num_tries", 50), ##Tocan should be the troop size ##Invasion 50
        (try_end),

        #(str_store_troop_name, s0, ":troop_no"),
        #(display_message, "{!}str_debug__hiring_men_to_party_for_s0"),

        (try_for_range, ":unused", 0, ":num_tries"),
          (call_script, "script_hire_men_to_kingdom_hero_party", ":troop_no"),
        (try_end),
        
        (assign, ":xp_rounds", 0),

        (game_get_reduce_campaign_ai, ":reduce_campaign_ai"),
        (try_begin),
          (this_or_next|eq, ":troop_faction_no", "$players_kingdom"),
          (eq, ":troop_faction_no", "fac_player_supporters_faction"),
          (assign, ":xp_rounds", 0),
        (else_try),
          (eq, ":reduce_campaign_ai", 0), #hard
          (assign, ":xp_rounds", 2),
        (else_try),
          (eq, ":reduce_campaign_ai", 1), #moderate
          (assign, ":xp_rounds", 1),
        (else_try),                        
          (eq, ":reduce_campaign_ai", 2), #easy
          (assign, ":xp_rounds", 0),
        (try_end),           

        (troop_get_slot, ":renown", ":troop_no", slot_troop_renown),
        (store_div, ":renown_xp_rounds", ":renown", 100),
        (val_add, ":xp_rounds", ":renown_xp_rounds"),
        (try_for_range, ":unused", 0, ":xp_rounds"),
          (call_script, "script_upgrade_hero_party", "$pout_party", 4000),
        (try_end),
      (try_end),      
  ]),
  ("decide_faction_ai_dk2",
  #This handles political issues and faction issues
   [
    (store_script_param_1, ":faction_no"),
	   
	   
    (faction_get_slot, ":old_faction_ai_state", ":faction_no", slot_faction_ai_state),
    (faction_get_slot, ":old_faction_ai_object", ":faction_no", slot_faction_ai_object),
	(faction_get_slot, ":faction_marshal", ":faction_no", slot_faction_marshall),

	 
	#Remove marshal if he has become too controversial,, or he has defected, or has been taken prisoner
	(try_begin),
        (faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
		(neq, ":faction_no", "fac_player_supporters_faction"),
		(ge, ":faction_marshal", "trp_player"),
		
		(store_faction_of_troop, ":marshal_faction", ":faction_marshal"),
		(try_begin),
			(eq, ":faction_marshal", "trp_player"),
			(assign, ":marshal_faction", "$players_kingdom"),
		(try_end),
		
		
		(assign, ":player_marshal_is_prisoner", 0),
		(try_begin),
			(eq, ":faction_marshal", "trp_player"),
			(eq, "$g_player_is_captive", 1),
			(assign, ":player_marshal_is_prisoner", 1),
		(try_end),
		
		
		#High controversy level, or marshal has defected, or is prisoner
		(this_or_next|neq, ":marshal_faction", ":faction_no"),		
		(this_or_next|troop_slot_ge, ":faction_marshal", slot_troop_controversy, 80),
		(this_or_next|eq, ":player_marshal_is_prisoner", 1),
			(troop_slot_ge, ":faction_marshal", slot_troop_prisoner_of_party, 0),
		
		(assign, ":few_following_player_campaign", 0),
		(try_begin),
			(eq, ":faction_marshal", "trp_player"),
			(assign, ":vassals_following_player_campaign", 0),
			(gt, "$g_player_days_as_marshal", 1),
			(try_for_range, ":vassal", active_npcs_begin, active_npcs_end),
				(troop_slot_eq, ":vassal", slot_troop_occupation, slto_kingdom_hero),
				(store_faction_of_troop, ":vassal_faction", ":vassal"),
				(eq, ":vassal_faction", ":faction_no"),
				(call_script, "script_npc_decision_checklist_troop_follow_or_not", ":vassal"),
				(eq, reg0, 1),
				(val_add, ":vassals_following_player_campaign", 1),
			(try_end),
			(lt, ":vassals_following_player_campaign", 4),
			(assign, ":few_following_player_campaign", 1),
		(try_end),
		
		#Only remove marshal for controversy if offensive campaign in progress
		(this_or_next|eq, ":old_faction_ai_state", sfai_default),
		(this_or_next|eq, ":old_faction_ai_state", sfai_feast),		
		(this_or_next|neq, ":marshal_faction", ":faction_no"),
		(this_or_next|eq, ":few_following_player_campaign", 1),
		(this_or_next|eq, ":player_marshal_is_prisoner", 1),
			(troop_slot_ge, ":faction_marshal", slot_troop_prisoner_of_party, 0),
		
		#No current issue on the agenda
		(this_or_next|faction_slot_eq, ":faction_no", slot_faction_political_issue, 0),
		(this_or_next|eq, ":player_marshal_is_prisoner", 1),
			(troop_slot_ge, ":faction_marshal", slot_troop_prisoner_of_party, 0),
		
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

		(try_begin),
			(eq, "$players_kingdom", ":faction_no"),
			(faction_slot_eq, "$players_kingdom", slot_faction_marshall, "trp_player"),
			(call_script, "script_add_notification_menu", "mnu_notification_relieved_as_marshal", 0, 0),
		(else_try),
			(neq, ":old_marshall", "trp_player"),
			(call_script, "script_change_troop_renown", ":old_marshall", 15),
		(try_end),
		(faction_set_slot, ":faction_no", slot_faction_marshall, -1),
		(assign, ":faction_marshal", -1),
		
		
		
		(try_for_range, ":active_npc", active_npcs_begin, active_npcs_end),
			(store_faction_of_troop, ":active_npc_faction", ":active_npc"),
			(eq, ":active_npc_faction", ":faction_no"),
			(troop_set_slot, ":active_npc", slot_troop_stance_on_faction_issue, -1),
		(try_end),		
		(try_begin),
			(eq, "$players_kingdom", ":faction_no"),
			(troop_set_slot, "trp_player", slot_troop_stance_on_faction_issue, -1),
		(try_end),
		
	(else_try),	 #If marshal not present, and not already on agenda, make political issue
		(eq, ":faction_marshal", -1),
		(neg|faction_slot_ge, ":faction_no", slot_faction_political_issue, 1), #This to avoid resetting votes every time
	
        (faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
		(neq, ":faction_no", "fac_player_supporters_faction"),
		
		(faction_set_slot, ":faction_no", slot_faction_political_issue, 1), #Appointment of marshal
		(store_current_hours, ":hours"),
		(val_max, ":hours", 0),
		(faction_set_slot, ":faction_no", slot_faction_political_issue_time, ":hours"), #Appointment of marshal
		
		(try_for_range, ":active_npc", active_npcs_begin, active_npcs_end),
			(store_faction_of_troop, ":active_npc_faction", ":active_npc"),
			(eq, ":active_npc_faction", ":faction_no"),
			(troop_set_slot, ":active_npc", slot_troop_stance_on_faction_issue, -1),
		(try_end),		
		(try_begin),
			(eq, "$players_kingdom", ":faction_no"),
			(troop_set_slot, "trp_player", slot_troop_stance_on_faction_issue, -1),
		(try_end),
		
		
	(else_try),	#If player is marshal, but not part of faction
		(eq, ":faction_marshal", "trp_player"),
		(neq, "$players_kingdom", ":faction_no"),

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
		(assign, ":faction_marshal", -1),
		
		(try_for_range, ":active_npc", active_npcs_begin, active_npcs_end),
			(store_faction_of_troop, ":active_npc_faction", ":active_npc"),
			(eq, ":active_npc_faction", ":faction_no"),
			(troop_set_slot, ":active_npc", slot_troop_stance_on_faction_issue, -1),
		(try_end),		
		(try_begin),
			(eq, "$players_kingdom", ":faction_no"),
			(troop_set_slot, "trp_player", slot_troop_stance_on_faction_issue, -1),
		(try_end),
		
	(try_end),
	 
	#If the faction issue is a center no longer under faction control, remove and reset 
	(try_begin), 
		(faction_get_slot, ":faction_political_issue", ":faction_no", slot_faction_political_issue),
		(is_between, ":faction_political_issue", centers_begin, centers_end),
		(store_faction_of_party, ":disputed_center_faction", ":faction_political_issue"),
		(neq, ":disputed_center_faction", ":faction_no"),
		
		(try_begin),
			(eq, "$cheat_mode", 1),
			(str_store_faction_name, s4, ":faction_no"),
			(str_store_party_name, s5, ":disputed_center_faction"),
			(display_message, "@{!}DEBUG -- {s4} drops {s5} as issue as it has changed hands"),
		(try_end),
		
		#Reset political issue
		(faction_set_slot, ":faction_no", slot_faction_political_issue, 0),
		(try_for_range, ":active_npc", active_npcs_begin, active_npcs_end),
			(store_faction_of_troop, ":active_npc_faction", ":active_npc"),
			(eq, ":active_npc_faction", ":faction_no"),
			(troop_set_slot, ":active_npc", slot_troop_stance_on_faction_issue, -1),
		(try_end),		
		(try_begin),
			(eq, "$players_kingdom", ":faction_no"),
			(troop_set_slot, "trp_player", slot_troop_stance_on_faction_issue, -1),
		(try_end),
		
	(try_end),
	
	
	#Resolve the political issue on the agenda
	(try_begin),
		(faction_slot_ge, ":faction_no", slot_faction_political_issue, 1),
		(neq, ":faction_no", "fac_player_supporters_faction"),
		
		#Do not switch marshals during a campaign
		(this_or_next|faction_slot_ge, ":faction_no", slot_faction_political_issue, centers_begin),
		(this_or_next|faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_default),
			(faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_feast),
		
		
		(faction_get_slot, ":faction_leader", ":faction_no", slot_faction_leader),
		
		(assign, ":total_lords", 0),
		(assign, ":lords_who_have_voted", 0),
		(assign, ":popular_favorite", -1),
	
		#Reset number of votes
		(troop_set_slot, "trp_player", slot_troop_temp_slot, 0),
		(try_for_range, ":active_npc", active_npcs_begin, active_npcs_end),
			(troop_set_slot, ":active_npc", slot_troop_temp_slot, 0),
		(try_end),

		#Tabulate votes
		(try_for_range, ":voting_lord", active_npcs_begin, active_npcs_end),
			(store_faction_of_troop, ":voting_lord_faction", ":voting_lord"),
			(eq, ":voting_lord_faction", ":faction_no"),
			(val_add, ":total_lords", 1),
			(troop_get_slot, ":lord_chosen_candidate", ":voting_lord", slot_troop_stance_on_faction_issue),								
			(gt, ":lord_chosen_candidate", -1),									
			(val_add, ":lords_who_have_voted", 1),			
			(troop_get_slot, ":total_votes", ":lord_chosen_candidate", slot_troop_temp_slot),
			(val_add, ":total_votes", 1),
			(troop_set_slot, ":lord_chosen_candidate", slot_troop_temp_slot, ":total_votes"),			
			(try_begin),
				(gt, ":popular_favorite", -1),
				(troop_get_slot, ":current_winner_votes", ":popular_favorite", slot_troop_temp_slot),
				(gt, ":total_votes", ":current_winner_votes"),
				(assign, ":popular_favorite", ":lord_chosen_candidate"),
			(else_try),	
				(eq, ":popular_favorite", -1),
				(assign, ":popular_favorite", ":lord_chosen_candidate"),
			(try_end),
		(try_end),	

		#Check to see if enough lords have voted
		(store_div, ":number_required_for_quorum", ":total_lords", 5),
		(val_mul, ":number_required_for_quorum", 4),
		
		
#		(gt, ":lords_who_have_voted", ":number_required_for_quorum"),

		(store_current_hours, ":hours_on_agenda"),
		(faction_get_slot, ":hours_when_put_on_agenda", ":faction_no", slot_faction_political_issue_time), #Appointment of marshal
		(val_sub, ":hours_on_agenda", ":hours_when_put_on_agenda"),
		
		(this_or_next|gt, ":lords_who_have_voted", ":number_required_for_quorum"),
			(ge, ":hours_on_agenda", 10), #Ne 120 to 10

		(try_begin),
			(eq, "$cheat_mode", 1),
			(assign, reg4, ":lords_who_have_voted"),
			(assign, reg5, ":number_required_for_quorum"),
			(assign, reg7, ":hours_on_agenda"),
			(str_store_faction_name, s4, ":faction_no"),
			(display_message, "@{!}DEBUG -- Issue resolution for {s4}: {reg4} votes for a quorum of {reg5}, {reg7} hours on agenda"),
		(try_end),


		(try_begin),
		  (eq, "$cheat_mode", 1),
		  (display_message, "@{!}DEBUG -- Faction resolves political issue"),
		(try_end),

	
		#Resolve faction political issue
		(assign, ":winning_candidate", -1),
		(try_begin),
			(call_script, "script_troop_get_relation_with_troop", ":faction_leader", ":popular_favorite"),
			
			(this_or_next|ge, reg0, 10),
			(this_or_next|troop_slot_eq, ":faction_leader", slot_troop_stance_on_faction_issue, ":popular_favorite"),
				(troop_slot_eq, ":faction_leader", slot_troop_stance_on_faction_issue, -1),
						
			(assign, ":winning_candidate", ":popular_favorite"),
		(else_try),#Lord overrules lords' opinion		
			(gt, ":faction_leader", -1), #not sure why this is necessary
			(troop_get_slot, ":liege_choice", ":faction_leader", slot_troop_stance_on_faction_issue),
			(ge, ":liege_choice", -1),
							
			(assign, ":winning_candidate", ":liege_choice"),
		(try_end),

		#Carry out faction decision
		(try_begin), #Nothing happens
			(eq, ":winning_candidate", -1),
			
		(else_try), #For player, create a menu to accept or refuse
			(eq, ":winning_candidate", "trp_player"),
			(eq, "$players_kingdom", ":faction_no"),
			(call_script, "script_add_notification_menu", "mnu_notification_player_faction_political_issue_resolved_for_player", 0, 0),
		(else_try),
			(eq, ":winning_candidate", "trp_player"),
			(neq, "$players_kingdom", ":faction_no"),

			(try_begin),
				(eq, "$cheat_mode", 1),
				(str_store_faction_name, s4, ":faction_no"),
				(str_store_party_name, s5, ":winning_candidate"),
				(display_message, "@{!}DEBUG -- {s4} drops {s5} as winner, for having changed sides"),
			(try_end),
			
			(try_for_range, ":active_npc", active_npcs_begin, active_npcs_end),
				(store_faction_of_troop, ":active_npc_faction", ":active_npc"),
				(eq, ":active_npc_faction", ":faction_no"),
				(troop_set_slot, ":active_npc", slot_troop_stance_on_faction_issue, -1),
			(try_end),		
			(try_begin),
				(eq, "$players_kingdom", ":faction_no"),
				(troop_set_slot, "trp_player", slot_troop_stance_on_faction_issue, -1),
			(try_end),
			
		(else_try),	#If candidate is not of winning faction, reset lrod votes
			(store_faction_of_troop, ":winning_candidate_faction", ":winning_candidate"),
			(neq, ":winning_candidate_faction", ":faction_no"),
			
			(try_begin),
				(eq, "$cheat_mode", 1),
				(str_store_faction_name, s4, ":faction_no"),
				(str_store_party_name, s5, ":winning_candidate"),
				(display_message, "@{!}DEBUG -- {s4} drops {s5} as winner, for having changed sides"),
			(try_end),
			
			(try_for_range, ":active_npc", active_npcs_begin, active_npcs_end),
				(store_faction_of_troop, ":active_npc_faction", ":active_npc"),
				(eq, ":active_npc_faction", ":faction_no"),
				(troop_set_slot, ":active_npc", slot_troop_stance_on_faction_issue, -1),
			(try_end),		
			(try_begin),
				(eq, "$players_kingdom", ":faction_no"),
				(troop_set_slot, "trp_player", slot_troop_stance_on_faction_issue, -1),
			(try_end),
			
		(else_try), #Honor awarded to another
			(faction_get_slot, ":issue_on_table", ":faction_no", slot_faction_political_issue),
			(try_begin), #A marshalship awarded to another
				(eq, ":issue_on_table", 1),
				(is_between, ":winning_candidate", active_npcs_begin, active_npcs_end),
				
				(this_or_next|is_between, ":winning_candidate", active_npcs_begin, active_npcs_end), #Prevents bug in which player given marshaldom of kingdom of which he/she is not a member
					(eq, "$players_kingdom", ":faction_no"),
				
				(assign, ":faction_marshal", ":winning_candidate"),
			(else_try), #A fief awarded to another
				(is_between, ":issue_on_table", centers_begin, centers_end),
				
				#If given to the player, resolved above
				(call_script, "script_give_center_to_lord", ":issue_on_table", ":winning_candidate", 0), #Zero means don't add garrison
				
				#If the player had requested a captured castle
				(try_begin),
					(eq, ":issue_on_table", "$g_castle_requested_by_player"),
					(party_slot_ge, ":issue_on_table", slot_town_lord, active_npcs_begin),
					(store_faction_of_party, ":faction_of_issue", ":issue_on_table"),
					(eq, ":faction_of_issue", "$players_kingdom"),
					(assign, "$g_center_to_give_to_player", ":issue_on_table"),
					(try_begin),
						(troop_get_slot, ":husband", "trp_player", slot_troop_spouse),
						(is_between, ":husband", active_npcs_begin, active_npcs_end),
						(eq, "$g_castle_requested_for_troop", ":husband"),
						(neq, ":winning_candidate", ":husband"),
						(jump_to_menu, "mnu_requested_castle_granted_to_another_female"),
					(else_try),
						(jump_to_menu, "mnu_requested_castle_granted_to_another"),
					(try_end),	
				(try_end),
				
			(try_end),
		
			(try_begin),
				(eq, ":faction_no", "$players_kingdom"),
				(call_script, "script_add_notification_menu", "mnu_notification_player_faction_political_issue_resolved", ":issue_on_table", ":winning_candidate"),
			(try_end),
		
		#Reset political issue
			(faction_set_slot, ":faction_no", slot_faction_political_issue, 0),
			(try_for_range, ":active_npc", active_npcs_begin, active_npcs_end),
				(store_faction_of_troop, ":active_npc_faction", ":active_npc"),
				(eq, ":active_npc_faction", ":faction_no"),
				(troop_set_slot, ":active_npc", slot_troop_stance_on_faction_issue, -1),
			(try_end),
			(try_begin),
				(eq, "$players_kingdom", ":faction_no"),
				(troop_set_slot, "trp_player", slot_troop_stance_on_faction_issue, -1),
			(try_end),			
		(try_end),
	(try_end),

	#Add fief to faction issues
	(try_begin),
		(faction_get_slot, ":faction_issue", ":faction_no", slot_faction_political_issue),
		(le, ":faction_issue", 0),
		
		(assign, ":landless_lords", 0),
		(assign, ":unassigned_centers", 0),
		(assign, ":first_unassigned_center_found", 0),
		
		(troop_set_slot, "trp_player", slot_troop_temp_slot, 0),
		(try_for_range, ":active_npc", active_npcs_begin, active_npcs_end),
			(troop_set_slot, ":active_npc", slot_troop_temp_slot, 0),
		(try_end),
		
		(try_for_range, ":center", centers_begin, centers_end),
			(store_faction_of_party, ":center_faction", ":center"),
			(eq, ":center_faction", ":faction_no"),
			
			(party_get_slot, ":town_lord", ":center", slot_town_lord),
			
			(try_begin),
				(lt, ":town_lord", 0),
				(val_add, ":unassigned_centers", 1),
				(try_begin),
					(eq, ":first_unassigned_center_found", 0),
					(assign, ":first_unassigned_center_found", ":center"),
				(try_end),
			(else_try),
				(troop_set_slot, ":town_lord", slot_troop_temp_slot, 1),			
			(try_end),
		(try_end),
		
		(store_add, ":landless_lords_plus_unassigned_centers", ":landless_lords", ":unassigned_centers"),
		(ge, ":landless_lords_plus_unassigned_centers", 2),		
			
		(faction_set_slot, ":faction_no", slot_faction_political_issue, ":first_unassigned_center_found"),	
		(store_current_hours, ":hours"),
		(faction_set_slot, ":faction_no", slot_faction_political_issue_time, ":hours"), #Fief put on agenda
		
		(try_for_range, ":active_npc", active_npcs_begin, active_npcs_end),
			(store_faction_of_troop, ":active_npc_faction", ":active_npc"),
			(eq, ":active_npc_faction", ":faction_no"),
			(troop_set_slot, ":active_npc", slot_troop_stance_on_faction_issue, -1),
		(try_end),
		(try_begin),
			(eq, "$players_kingdom", ":faction_no"),
			(troop_set_slot, "trp_player", slot_troop_stance_on_faction_issue, -1),
		(try_end),				
	(try_end),
	 
	 
    (try_begin), #If the marshal is changed
       (neg|faction_slot_eq, ":faction_no", slot_faction_marshall, ":faction_marshal"),
       #(assign, ":marshall_changed", 1),
       (eq, "$players_kingdom", ":faction_no"),
       (str_store_troop_name_link, s1, ":faction_marshal"),
       (str_store_faction_name_link, s2, ":faction_no"),
       (display_message, "@{s1} is the new marshal of {s2}."),
       (call_script, "script_check_and_finish_active_army_quests_for_faction", ":faction_no"),       
    (try_end),	 
	 
    (try_begin), #If the marshal is changed
       (neg|faction_slot_eq, ":faction_no", slot_faction_marshall, ":faction_marshal"),
	   (gt, ":faction_marshal", -1),
       (call_script, "script_appoint_faction_marshall", ":faction_no", ":faction_marshal"),   
    (try_end),	 
		 
	#DO FACTION AI HERE
	(try_begin),
		(eq, ":faction_no", "$players_kingdom"),
		(eq, ":faction_marshal", "trp_player"),
	    (assign, ":faction_ai_decider", "trp_player"),
	(else_try),
		(is_between, ":faction_marshal", active_npcs_begin, active_npcs_end),
		(assign, ":faction_ai_decider", ":faction_marshal"),
	(else_try),
		(faction_get_slot, ":faction_ai_decider", ":faction_no", slot_faction_leader),
	(try_end),
 
    (call_script, "script_npc_decision_checklist_faction_ai_alt_dk2",  ":faction_ai_decider"),
    (assign, ":new_strategy", reg0),
    (assign, ":new_object", reg1),
    	     
    ###new ozan
    (try_begin),
       (neq, ":new_strategy", ":old_faction_ai_state"),
       (eq, ":new_strategy", sfai_gathering_army),
       (faction_get_slot, ":faction_marshal", ":faction_no", slot_faction_marshall),
       (troop_get_slot, ":marshal_party", ":faction_marshal", slot_troop_leaded_party),
       (party_set_slot, ":marshal_party", slot_party_ai_object, -1),
       (assign, "$g_gathering_new_started", 1),
       (call_script, "script_npc_decision_checklist_party_ai", ":faction_marshal"), #This handles AI for both marshal and other parties		
       (call_script, "script_party_set_ai_state", ":marshal_party", reg0, reg1),
       (assign, "$g_gathering_new_started", 0),
    (else_try),      
       #check if marshal arrived his target city during active gathering
       
       #for now i disabled below lines because after always/active gathering armies become very large.
       #in current style marshal makes active gathering only at first, it travels to a city and waits there.
       
       (eq, ":new_strategy", ":old_faction_ai_state"),
       (eq, ":new_strategy", sfai_gathering_army),
       (faction_get_slot, ":faction_marshal", ":faction_no", slot_faction_marshall),
       (troop_get_slot, ":marshal_party", ":faction_marshal", slot_troop_leaded_party),
       (party_get_slot, ":party_ai_object", ":marshal_party", slot_party_ai_object),
       (ge, ":party_ai_object", 0),
       (store_distance_to_party_from_party, ":dist", ":marshal_party", ":party_ai_object"),
       (le, ":dist", 5),
       (party_set_slot, ":marshal_party", slot_party_ai_object, -1),
    (try_end),
     ##end ozan
	   	   	   
     #The following logic is mostly transplanted to the new decision_checklist 
     #Decision_checklist is used because I want to be able to reproduce the logic for strings
     #(call_script, "script_old_faction_ai"), 
     #ozan - I collected all comment-out lines in here (faction ai script) and placed most bottom of scripts.py to avoid confusing.	   		 	
     
    (faction_set_slot, ":faction_no", slot_faction_ai_state, ":new_strategy"),
    (faction_set_slot, ":faction_no", slot_faction_ai_object, ":new_object"),

    (call_script, "script_update_report_to_army_quest_note", ":faction_no", ":new_strategy", ":old_faction_ai_state"),

    (try_begin),
       (eq, ":new_strategy", sfai_feast),
       
       (store_current_hours, ":hours"),
       (faction_set_slot, ":faction_no", slot_faction_last_feast_start_time, ":hours"), #new
       
       (try_begin),
         (eq, "$g_player_eligible_feast_center_no", ":new_object"),
         (assign, "$g_player_eligible_feast_center_no", -1), #reset needed
       (try_end),
       (try_begin),
         (is_between, ":new_object", towns_begin, towns_end),
         (party_set_slot, ":new_object", slot_town_has_tournament, 2),
       (try_end),
    (try_end),	
	
     #Change of strategy
    (try_begin),
       (neq, ":new_strategy", ":old_faction_ai_state"),
		
       (try_begin),
         (ge, "$cheat_mode", 1),
         (str_store_faction_name, s5, ":faction_no"),
         (display_message, "str_s5_decides_s14"),
       (try_end),
		
       (store_current_hours, ":hours"),
       (faction_set_slot, ":faction_no", slot_faction_ai_current_state_started, ":hours"),

       #Feast ends
       (try_begin),
         (eq, ":old_faction_ai_state", sfai_feast),
         (call_script, "script_faction_conclude_feast", ":faction_no", ":old_faction_ai_object"),
       (try_end),

	   
       #Feast begins
       (try_begin),
         (eq, ":new_strategy", sfai_feast),
         (faction_get_slot, ":faction_object", ":faction_no", slot_faction_ai_object),
		 
##         (str_store_faction_name, s1, ":faction_no"),
##         (str_store_party_name, s2, ":faction_object"),
##         (display_message, "str_lords_of_the_s1_gather_for_a_feast_at_s2"),
		
         (party_get_slot, ":feast_host", ":faction_object", slot_town_lord),

         (try_begin),
           (check_quest_active, "qst_wed_betrothed"),
		   
           (quest_slot_eq, "qst_wed_betrothed", slot_quest_giver_troop, ":feast_host"),
           (neg|quest_slot_ge, "qst_wed_betrothed", slot_quest_expiration_days, 362),
           (call_script, "script_add_notification_menu", "mnu_notification_player_wedding_day", ":feast_host", ":faction_object"),
		 (else_try),
           (check_quest_active, "qst_wed_betrothed_female"),
		   
           (quest_get_slot, ":player_betrothed", "qst_wed_betrothed", slot_quest_giver_troop),
		   (store_faction_of_troop, ":player_betrothed_faction", ":player_betrothed"),
		   (eq, ":player_betrothed_faction", ":faction_no"),
           (neg|quest_slot_ge, "qst_wed_betrothed", slot_quest_expiration_days, 362),
           (call_script, "script_add_notification_menu", "mnu_notification_player_kingdom_holds_feast", ":feast_host", ":faction_object"),
         (else_try),
           (eq, "$players_kingdom", ":faction_no"),
           (troop_slot_ge, "trp_player", slot_troop_renown, 150),
		   
		   
           (party_get_slot, ":feast_host", ":faction_object", slot_town_lord),
           (call_script, "script_add_notification_menu", "mnu_notification_player_kingdom_holds_feast", ":feast_host", ":faction_object"),
         (try_end),
       (try_end),
		

       #Offensive begins
       (try_begin),
         (eq, ":old_faction_ai_state", sfai_gathering_army),
         (is_between, ":new_strategy", sfai_attacking_center, sfai_feast),
		 (try_begin),
			(eq, "$cheat_mode", 1),
			(str_store_faction_name, s5, ":faction_no"),
			(display_message, "str_s5_begins_offensive"),
		 (try_end),
			
         #Appoint screening party
         (try_begin),
           (assign, ":total_lords_participating", 0),
           (assign, ":best_screening_party", -1),
           (assign, ":score_to_beat", 30), #closest in size to 50
           (troop_get_slot, ":faction_marshal_party", ":faction_marshal", slot_troop_leaded_party),
           (party_is_active, ":faction_marshal_party"),							

           (try_for_range, ":screen_leader", active_npcs_begin, active_npcs_end),
             (store_faction_of_troop, ":screen_leader_faction", ":screen_leader"),
             (eq, ":screen_leader_faction", ":faction_no"),
			 
             (troop_get_slot, ":screening_party", ":screen_leader_faction", slot_troop_leaded_party), 
             (party_is_active, ":screening_party"),			
             (party_slot_eq, ":screening_party", slot_party_ai_state, spai_accompanying_army),
             (party_slot_eq, ":screening_party", slot_party_ai_object, ":faction_marshal_party"),
             (val_add, ":total_lords_participating", 1),

		     (try_begin),
			  (ge, "$cheat_mode", 1),
		      (str_store_party_name, s4, ":screening_party"),
			  (display_message, "@{!}DEBUG -- {s4} participates in offensive"),
		     (try_end),

			 
             (store_party_size_wo_prisoners, ":screening_party_score", ":screening_party"),
             (val_sub, ":screening_party_score", 50),
			 (val_abs, ":screening_party_score"),
			 
			 
			 (lt, ":screening_party_score", ":score_to_beat"),

             #set party and score
             (assign, ":best_screening_party", ":screening_party"),
             (assign, ":score_to_beat", ":screening_party_score"),
           (try_end),			

           (gt, ":total_lords_participating", 2),
           (party_is_active, ":best_screening_party"),
           (party_is_active, ":faction_marshal_party"),
           (call_script, "script_party_set_ai_state", ":best_screening_party", spai_screening_army, ":faction_marshal_party"),
		   (try_begin),
			(ge, "$cheat_mode", 1),
		    (str_store_party_name, s4, ":best_screening_party"),
			(display_message, "@{!}DEBUG -- {s4} chosen as screen"),
		   (try_end),
           #after this - dialogs on what doing, npc_decision_checklist
         (try_end),	
		 
       #Offensive concludes
       (else_try),
	     (store_current_hours, ":hours"),
         (this_or_next|eq, ":old_faction_ai_state", sfai_gathering_army),
         (this_or_next|eq, ":old_faction_ai_state", sfai_attacking_center),
         (this_or_next|eq, ":old_faction_ai_state", sfai_raiding_village),
		 #(this_or_next|eq, ":old_faction_ai_state", sfai_attacking_enemies_around_center),
			(eq, ":old_faction_ai_state", sfai_attacking_enemy_army),
		 
         (this_or_next|eq, ":new_strategy", sfai_default),
			(eq, ":new_strategy", sfai_feast),				
						
         (call_script, "script_check_and_finish_active_army_quests_for_faction", ":faction_no"),       		 
         (faction_set_slot, ":faction_no", slot_faction_last_offensive_concluded, ":hours"),
        (try_end),
    (try_end),
	
    (try_begin),
       (eq, "$players_kingdom", ":faction_no"),
       (neg|faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_attacking_center),
       (check_quest_active, "qst_join_siege_with_army"),
       (call_script, "script_abort_quest", "qst_join_siege_with_army", 0),
    (try_end),

    (try_begin),
       #old condition to rest, I changed below part - ozan, to rest (a faction's old strategy should be feast or default) and (a faction's new strategy should be feast or default)
       #(this_or_next|eq, ":new_strategy", sfai_default),
       #(this_or_next|eq, ":new_strategy", sfai_feast),
       #(this_or_next|eq, ":old_faction_ai_state", sfai_default),
       #(eq, ":old_faction_ai_state", sfai_feast),
       
       #new condition to rest, (a faction's new strategy should be feast or default) and (":hours_at_current_state" > 20)
       (this_or_next|eq, ":new_strategy", sfai_default),
		(eq, ":new_strategy", sfai_feast),                            
              
       (store_current_hours, ":hours_at_current_state"),
       (faction_get_slot, ":current_state_started", ":faction_no", slot_faction_ai_current_state_started), 
       (val_sub, ":hours_at_current_state", ":current_state_started"),
       (ge, ":hours_at_current_state", 18), #Must have at least 18 hours to reset
              
       (store_current_hours, ":hours"),       
       (faction_set_slot, ":faction_no", slot_faction_ai_last_rest_time, ":hours"),		
    (try_end),     
  ]),
 	(
	"npc_decision_checklist_faction_ai_alt_dk2", #This is called from within decide_faction_ai, or from 
	[
		(store_script_param, ":troop_no", 1),
		
		(store_faction_of_troop, ":faction_no", ":troop_no"),
		
		(str_store_troop_name, s4, ":troop_no"),
		(str_store_faction_name, s33, ":faction_no"),
		(try_begin),
			(eq, "$cheat_mode", 1),
		    (display_message, "@{!}DEBUG -- {s4} produces a faction strategy for {s33}"),
		(try_end),
		  		  
		#INFORMATIONS COLLECTING STEP 0: Here we obtain general information about current faction like how much parties that faction has, which lord is the marshall, current ai state and current ai target object
		#(faction_get_slot, ":faction_strength", ":faction_no", slot_faction_number_of_parties),
		(faction_get_slot, ":faction_marshal", ":faction_no", slot_faction_marshall),
		(faction_get_slot, ":current_ai_state", ":faction_no", slot_faction_ai_state),
		(faction_get_slot, ":current_ai_object", ":faction_no", slot_faction_ai_object),
		
		(assign, ":marshal_party", -1),
		(assign, ":marshal_party_strength", 0),
		  
		(try_begin),
		  (gt, ":faction_marshal", 0),
		  (troop_get_slot, ":marshal_party", ":faction_marshal", slot_troop_leaded_party),
		  (party_is_active, ":marshal_party"),
		  (party_get_slot, ":marshal_party_itself_strength", ":marshal_party", slot_party_cached_strength),
		  (party_get_slot, ":marshal_party_follower_strength", ":marshal_party", slot_party_follower_strength),
		  (store_add, ":marshal_party_strength", ":marshal_party_itself_strength", ":marshal_party_follower_strength"),
	    (try_end),
					
	    #INFORMATIONS COLLECTING STEP 1: Here we are learning how much hours past from last offensive situation/feast concluded/current state started
	    (store_current_hours, ":hours_since_last_offensive"),
	    (faction_get_slot, ":last_offensive_time", ":faction_no", slot_faction_last_offensive_concluded),
	    (val_sub, ":hours_since_last_offensive", ":last_offensive_time"),
	      
	    (store_current_hours, ":hours_since_last_feast_start"),
	    (faction_get_slot, ":last_feast_time", ":faction_no", slot_faction_last_feast_start_time),
	    (val_sub, ":hours_since_last_feast_start", ":last_feast_time"),
	      
	    (store_current_hours, ":hours_at_current_state"),
	    (faction_get_slot, ":current_state_started", ":faction_no", slot_faction_ai_current_state_started),
	    (val_sub, ":hours_at_current_state", ":current_state_started"),
	      
	    (store_current_hours, ":hours_since_last_faction_rest"),
	    (faction_get_slot, ":last_rest_time", ":faction_no", slot_faction_ai_last_rest_time),
	    (val_sub, ":hours_since_last_faction_rest", ":last_rest_time"),
			  
	    (try_begin), #calculating ":last_offensive_time_score", this will be used in #11 and #12
	        (ge, ":hours_since_last_offensive", 1080), #more than 45 days (100p)
	        (assign, ":last_offensive_time_score", 100),
	    (else_try),
	        (ge, ":hours_since_last_offensive", 480), #more than 20 days (65p..99p)
	        (store_sub, ":last_offensive_time_score", ":hours_since_last_offensive", 480),
	        (val_div, ":last_offensive_time_score", 20), 
	        (val_add, ":last_offensive_time_score", 64),
	    (else_try),
	        (ge, ":hours_since_last_offensive", 240), #more than 10 days (41p..64p)
	        (store_sub, ":last_offensive_time_score", ":hours_since_last_offensive", 240),
	        (val_div, ":last_offensive_time_score", 10), 
	        (val_add, ":last_offensive_time_score", 40),
	    (else_try), #less than 10 days (0p..40p)
	        (store_div, ":last_offensive_time_score", ":hours_since_last_offensive", 6), #0..40
	    (try_end),
									
	    #INFORMATION COLLECTING STEP 3: Here we are finding the most threatened center
	    (call_script, "script_find_center_to_defend", ":troop_no"),
	    (assign, ":most_threatened_center", reg0),
	    (assign, ":threat_danger_level", reg1),
	    (assign, ":enemy_strength_near_most_threatened_center", reg2), #NOTE! This will be off by as much as 50%
		  		 	      		
	    #INFORMATION COLLECTING STEP 4: Here we are finding number of vassals who are already following the marshal, and the assigned vassal ratio of current faction.
	    (assign, ":vassals_already_assembled", 0),
	    (assign, ":total_vassals", 0),	
	    (try_for_range, ":lord", active_npcs_begin, active_npcs_end),
	        (store_faction_of_troop, ":lord_faction", ":lord"),
	        (eq, ":lord_faction", ":faction_no"),
	        (troop_get_slot, ":led_party", ":lord", slot_troop_leaded_party),
	        (party_is_active, ":led_party"),
	        (val_add, ":total_vassals", 1),
			
	        (party_slot_eq, ":led_party", slot_party_ai_state, spai_accompanying_army),
	        (party_slot_eq, ":led_party", slot_party_ai_object, ":marshal_party"),
			
	        (party_is_active, ":marshal_party"),
	        (store_distance_to_party_from_party, ":distance_to_marshal", ":led_party", ":marshal_party"),
	        (lt, ":distance_to_marshal", 15),
	        (val_add, ":vassals_already_assembled", 1),
	    (try_end),
	    (assign, ":ratio_of_vassals_assembled", -1),
	    (try_begin),
	        (gt, ":total_vassals", 0),
	        (store_mul, ":ratio_of_vassals_assembled", ":vassals_already_assembled", 100),
	        (val_div, ":ratio_of_vassals_assembled", ":total_vassals"),
	    (try_end),
		
	    #50% of vassals means that the campaign hour limit is ten days
	    (store_mul, ":campaign_hour_limit", ":ratio_of_vassals_assembled", 3),
	    (val_add, ":campaign_hour_limit", 90), 
	    
	    #To Steve - I understand your concern about some marshals will gather army and some will not be able to find any valueable center to attack after gathering,
	    #and these marshals will be questioned by other marshals ext. This is ok but if we search for a target without adding all other vassals what if 
	    #AI cannot find any target for long time because of its low power ratio if enemy cities are equal defended? Do not forget if we do not count other vassals in 
	    #faction while making target search we can only add marshal army's power and vassals around him. And if there is any threat in our centers even it is smaller, 
	    #its threat_danger_level will be more than target_value_level if marshal new started gathering for ofensive. Because we only assume marshal and around vassals 
	    #will join attack. And in our scenarios currently there are less vassals are around him. So power ratio will be low and any small threat will be enought to stop 
	    #an offensive. Then when players finds out this they periodically will take under siege to enemy's any center and they will be saved from any kind of newly started 
	    #offensive they will be faced. So we have to calculate both attack levels and select highest one to compare with threat level. Please do not change this part.
		
		(try_begin),
	 
		  (ge, ":faction_marshal", 0),
		  (ge, ":marshal_party", 0),
		  (party_is_active, ":marshal_party"),

		  (call_script, "script_party_count_fit_for_battle", ":marshal_party"),
		  (assign, ":number_of_fit_soldiers_in_marshal_party", reg0),
		  (ge, ":number_of_fit_soldiers_in_marshal_party", 40),
		  
		  (call_script, "script_find_center_to_attack_alt_dk2", ":troop_no", 1, 0),
		  (assign, ":center_to_attack_all_vassals_included", reg0),
		  (assign, ":target_value_level_all_vassals_included", reg1),
		  
		  (call_script, "script_find_center_to_attack_alt_dk2", ":troop_no", 1, 1),
		  (assign, ":center_to_attack_only_marshal_and_followers", reg0),
		  (assign, ":target_value_level_only_marshal_and_followers", reg1),
		(else_try),  
		  (assign, ":target_value_level_all_vassals_included", 0),
		  (assign, ":target_value_level_only_marshal_and_followers", 0),
		  (assign, ":center_to_attack_all_vassals_included", -1),
		  (assign, ":center_to_attack_only_marshal_and_followers", -1),
		(try_end),
		
		(try_begin),
		  (ge, ":target_value_level_all_vassals_included", ":center_to_attack_only_marshal_and_followers"),
		  (assign, ":center_to_attack", ":center_to_attack_all_vassals_included"),
		  (assign, ":target_value_level", ":target_value_level_all_vassals_included"),
		(else_try),  
		  (assign, ":center_to_attack", ":center_to_attack_only_marshal_and_followers"),
		  (assign, ":target_value_level", ":target_value_level_only_marshal_and_followers"),
		(try_end),
		  		  
		(try_begin),
		  (eq, ":current_ai_state", sfai_attacking_center),
		  (val_mul, ":target_value_level", 3),
		  (val_div, ":target_value_level", 2),
		(try_end),

		(try_begin), #NE
		  (eq, "$cheat_mode", 1),
		  (try_begin),
		    (is_between, ":center_to_attack", centers_begin, centers_end),
		    (str_store_party_name, s4, ":center_to_attack"),
		    (display_message, "@{!}Best offensive target {s4} has value level of {reg1}"),
		  (else_try),
		    (display_message, "@{!}No center found to attack"),
		  (try_end),	
		
		  (try_begin),
		    (is_between, ":most_threatened_center", centers_begin, centers_end),
		    (str_store_party_name, s4, ":most_threatened_center"),
		    (assign, reg1, ":threat_danger_level"),
		    (display_message, "@{!}Best threat of {s4} has value level of {reg1}"),
		  (else_try),
		    (display_message, "@{!}No center found to defend"),
		  (try_end),  
		(try_end),
		
		(try_begin),
		  (eq, "$cheat_mode", 1),
		  
		  (try_begin),
  		    (is_between, ":most_threatened_center", centers_begin, centers_end),
 		    (str_store_party_name, s4, ":most_threatened_center"),
		    (assign, reg1, ":threat_danger_level"),
		    (display_message, "@Best threat of {s4} has value level of {reg1}"),
		  (else_try),
		    (display_message, "@No center found to defend"),
		  (try_end),  
		(try_end),  
				
	    (assign, "$g_target_after_gathering", -1),
	    
	    (store_current_hours, ":hours"),	      
	    (try_begin),
	      (ge, ":target_value_level", ":threat_danger_level"),
	      (faction_set_slot, ":faction_no", slot_faction_last_safe_hours, ":hours"),	  
	    (try_end),  
	    (faction_get_slot, ":last_safe_hours", ":faction_no", slot_faction_last_safe_hours),
	    (try_begin),
	      (eq, ":last_safe_hours", 0),
	      (faction_set_slot, ":faction_no", slot_faction_last_safe_hours, ":hours"),	  
	    (try_end),
	    (faction_get_slot, ":last_safe_hours", ":faction_no", slot_faction_last_safe_hours),
	    (store_sub, ":hours_since_days_defensive_started", ":hours", ":last_safe_hours"),
	    (str_store_faction_name, s7, ":faction_no"),

		(assign, ":at_peace_with_everyone", 1),
		(try_for_range, ":faction_at_war", kingdoms_begin, kingdoms_end),
			(store_relation, ":relation", ":faction_no", ":faction_at_war"),
			(lt, ":relation", 0),
			(assign, ":at_peace_with_everyone", 0),
		(try_end),

	    
	    #INFORMATIONS ARE COLLECTED, NOW CHECK ALL POSSIBLE ACTIONS AND DECIDE WHAT TO DO	NEXT
		#Player marshal
		(try_begin), # a special case to end long-running feasts
			(eq, ":troop_no", "trp_player"),
				
			(eq, ":current_ai_state", sfai_feast),
			(ge, ":hours_at_current_state", 72),
		
			(assign, ":action", sfai_default),
			(assign, ":object", -1),
			
			#Normally you are not supposed to set permanent values in this state, but this is a special case to end player-called feasts
			(assign, "$player_marshal_ai_state", sfai_default),
			(assign, "$player_marshal_ai_object", -1),
		(else_try), #another special state, to make player-called feasts last for a while when the player is the leader of the faction, but not the marshal
			(eq, "$players_kingdom", "fac_player_supporters_faction"),
			(faction_slot_eq, "$players_kingdom", slot_faction_leader, "trp_player"),
			(neq, ":troop_no", "trp_player"),
			
			(eq, ":current_ai_state", sfai_feast),
			(le, ":hours_at_current_state", 48),
			
			(party_slot_eq, ":current_ai_object", slot_town_lord, "trp_player"),
			(store_faction_of_party, ":current_ai_object_faction", ":current_ai_object"),
			(eq, ":current_ai_object_faction", "$players_kingdom"),
			
			(assign, ":action", sfai_feast),
			(assign, ":object", ":current_ai_object"),

			
		(else_try), #this is the main player marshal state
			(eq, ":troop_no", "trp_player"),
			
			(str_clear, s14),
			(assign, ":action", "$player_marshal_ai_state"),
			(assign, ":object", "$player_marshal_ai_object"),
			
	    #1-RESTING IF NEEDED 
	    #If not currently attacking a besieging a center and vassals did not rest for long time, let them rest.
	    #If we do not take this part to toppest level, tired vassals already did not accept any order, so that 
	    #faction cannot do anything already. So first let vassals rest if they need. Thats why it should be toppest.
		(else_try),
			(neq, ":current_ai_state", sfai_default),
			(neq, ":current_ai_state", sfai_feast),
			(party_is_active, ":marshal_party"),
		
			(party_slot_eq, ":marshal_party", slot_party_ai_state, spai_retreating_to_center),
			
			(assign, ":action", sfai_default),
			(assign, ":object", -1),
			(str_store_string, s14, "str_the_enemy_temporarily_has_the_field"),
				
		(else_try), 
		    (neq, ":current_ai_state", sfai_feast),
		    
		    (assign, ":currently_besieging", 0),
		    (try_begin),
			    (eq, ":current_ai_state", sfai_attacking_center),
			    (is_between, ":current_ai_object", walled_centers_begin, walled_centers_end),
			    (party_get_slot, ":besieger_party", ":current_ai_object", slot_center_is_besieged_by),
			    (party_is_active, ":besieger_party"),
			    (store_faction_of_party, ":besieger_faction", ":besieger_party"),
			    (eq, ":besieger_faction", ":faction_no"),
			    (assign, ":currently_besieging", 1),
		    (try_end),
		    
		    (assign, ":currently_defending_center", 0),
	        (try_begin),
		        (eq, ":current_ai_state", sfai_attacking_enemies_around_center),
		        (gt, ":marshal_party", 0),
		        (party_is_active, ":marshal_party"),

				(assign, ":besieged_center", -1),          
				(try_begin),
					(party_slot_eq, ":marshal_party", slot_party_ai_state, spai_holding_center), #if commander is holding a center
					(party_get_slot, ":marshal_object", ":marshal_party", slot_party_ai_object), #get commander's ai object (center they are holding)
					(party_get_battle_opponent, ":besieger_enemy", ":marshal_object"), #get this object's battle opponent
					(ge, ":besieger_enemy", 0),
					(assign, ":besieged_center", ":marshal_object"),
				(else_try),
					(party_slot_eq, ":marshal_party", slot_party_ai_state, spai_engaging_army), #if commander is engaging an army
					(party_get_slot, ":marshal_object", ":marshal_party", slot_party_ai_object), #get commander's ai object (army which they engaded)
					(ge, ":marshal_object", 0), #if commander has an object
					(neg|is_between, ":marshal_object", centers_begin, centers_end), #if this object is not a center, so it is a party
					(party_is_active, ":marshal_object"),
					(party_get_battle_opponent, ":besieged_center", ":marshal_object"), #get this object's battle opponent
				(try_end),
	          
				(eq, ":besieged_center", ":current_ai_object"),
				(assign, ":currently_defending_center", 1),
	        (try_end),

		    (eq, ":currently_besieging", 0),	    
		    (eq, ":currently_defending_center", 0),
		    (ge, ":hours_since_last_faction_rest", 1240),

			(assign, ":action", sfai_default),
			(assign, ":object", -1),
			(str_store_string, s14, "str_the_vassals_are_tired_we_let_them_rest_for_some_time"),	    
		
	  #2-DEFENSIVE ACTIONS : GATHERING ARMY FOR DEFENDING
          (else_try),
            (party_is_active, ":marshal_party"),
			(eq, ":at_peace_with_everyone", 0),
            
            (is_between, ":most_threatened_center", centers_begin, centers_end),
            (gt, ":threat_danger_level", ":target_value_level"),
                        
            (assign, ":continue_gathering", 0),
            (assign, ":start_gathering", 0),
            
            (try_begin),
              (is_between, ":most_threatened_center", villages_begin, villages_end),

              (assign, ":continue_gathering", 0),
            (else_try),
              (try_begin),
                (lt, ":hours_since_days_defensive_started", 3),
                (assign, ":multiplier", 150),
              (else_try),
                (lt, ":hours_since_days_defensive_started", 6),
                (assign, ":multiplier", 140),
              (else_try),
                (lt, ":hours_since_days_defensive_started", 9),
                (assign, ":multiplier", 132),
              (else_try),
                (lt, ":hours_since_days_defensive_started", 12),
                (assign, ":multiplier", 124),
              (else_try),
                (lt, ":hours_since_days_defensive_started", 15),
                (assign, ":multiplier", 118),
              (else_try),
                (lt, ":hours_since_days_defensive_started", 18),
                (assign, ":multiplier", 114),
              (else_try),
                (lt, ":hours_since_days_defensive_started", 21),
                (assign, ":multiplier", 110),
              (else_try),
                (lt, ":hours_since_days_defensive_started", 24),
                (assign, ":multiplier", 106),
              (else_try),
                (lt, ":hours_since_days_defensive_started", 27),
                (assign, ":multiplier", 102),
              (else_try),
                (lt, ":hours_since_days_defensive_started", 31), 
                (assign, ":multiplier", 98),
              (else_try),
                (lt, ":hours_since_days_defensive_started", 34),
                (assign, ":multiplier", 94),
              (else_try),
                (lt, ":hours_since_days_defensive_started", 37),
                (assign, ":multiplier", 90),
              (else_try),
                (lt, ":hours_since_days_defensive_started", 40),
                (assign, ":multiplier", 86),
              (else_try),
                (lt, ":hours_since_days_defensive_started", 43),
                (assign, ":multiplier", 82),
              (else_try),
                (lt, ":hours_since_days_defensive_started", 46),
                (assign, ":multiplier", 79),
              (else_try),
                (lt, ":hours_since_days_defensive_started", 49),
                (assign, ":multiplier", 76),
              (else_try),
                (lt, ":hours_since_days_defensive_started", 52),
                (assign, ":multiplier", 73),
              (else_try),
                (lt, ":hours_since_days_defensive_started", 56),
                (assign, ":multiplier", 70),
              (else_try),
                (lt, ":hours_since_days_defensive_started", 60),
                (assign, ":multiplier", 68),
              (else_try),
                (lt, ":hours_since_days_defensive_started", 66),
                (assign, ":multiplier", 66),
              (else_try),
                (lt, ":hours_since_days_defensive_started", 72),
                (assign, ":multiplier", 64),
              (else_try),
                (lt, ":hours_since_days_defensive_started", 80),
                (assign, ":multiplier", 62),
              (else_try),
                (lt, ":hours_since_days_defensive_started", 90),
                (assign, ":multiplier", 60),
              (else_try),
                (lt, ":hours_since_days_defensive_started", 100),
                (assign, ":multiplier", 58),
              (else_try),
                (assign, ":multiplier", 56),
              (try_end),
		  
              (store_mul, ":enemy_strength_multiplied", ":enemy_strength_near_most_threatened_center", ":multiplier"),
              (val_div, ":enemy_strength_multiplied", 100),
		  
              (try_begin),		  
                (lt, ":marshal_party_strength", ":enemy_strength_multiplied"),
                (assign, ":continue_gathering", 1),
              (try_end),
            (else_try),  
              (eq, ":current_ai_state", sfai_attacking_enemies_around_center),
              (neq, ":most_threatened_center", ":current_ai_object"),
		  
              (assign, ":marshal_is_already_defending_a_center", 0),
              (try_begin),
                (gt, ":marshal_party", 0),
                (party_is_active, ":marshal_party"),
       
                (assign, ":besieged_center", -1),          
                (try_begin),
                  (party_slot_eq, ":marshal_party", slot_party_ai_state, spai_holding_center), #if commander is holding a center
                  (party_get_slot, ":marshal_object", ":marshal_party", slot_party_ai_object), #get commander's ai object (center they are holding)
                  (party_get_battle_opponent, ":besieger_enemy", ":marshal_object"), #get this object's battle opponent
                  (ge, ":besieger_enemy", 0),
                  (assign, ":besieged_center", ":marshal_object"),
                (else_try),              
                  (party_slot_eq, ":marshal_party", slot_party_ai_state, spai_engaging_army), #if commander is engaging an army
                  (party_get_slot, ":marshal_object", ":marshal_party", slot_party_ai_object), #get commander's ai object (army which they engaded)
                  (ge, ":marshal_object", 0), #if commander has an object
                  (neg|is_between, ":marshal_object", centers_begin, centers_end), #if this object is not a center, so it is a party
				  (party_is_active, ":marshal_object"),
                  (party_get_battle_opponent, ":besieged_center", ":marshal_object"), #get this object's battle opponent
                (try_end),

                (eq, ":besieged_center", ":current_ai_object"),
            
                (assign, ":marshal_is_already_defending_a_center", 1),
              (try_end),
                    
              (eq, ":marshal_is_already_defending_a_center", 0),
		  
              (store_mul, ":enemy_strength_multiplied", ":enemy_strength_near_most_threatened_center", 80),
              (val_div, ":enemy_strength_multiplied", 100),
              (lt, ":marshal_party_strength", ":enemy_strength_multiplied"),
              
              (this_or_next|is_between, ":most_threatened_center", walled_centers_begin, walled_centers_end),
              (neq, ":faction_no", "$players_kingdom"),              
              
              (assign, ":start_gathering", 1),
            (try_end),
		
            (this_or_next|eq, ":continue_gathering", 1),
            (eq, ":start_gathering", 1),
		
            (assign, ":action", sfai_gathering_army),
            (assign, ":object", -1),		
            (str_store_party_name, s21, ":most_threatened_center"),
            (str_store_string, s14, "str_we_should_prepare_to_defend_s21_but_we_should_gather_our_forces_until_we_are_strong_enough_to_engage_them"),
            
            (try_begin),
              (eq, ":faction_no", "$players_kingdom"),
              (assign, "$g_gathering_reason", ":most_threatened_center"),
            (try_end),
			
	    #3-DEFENSIVE ACTIONS : RIDE TO BREAK ENEMY SIEGE / DEFEAT ENEMIES NEAR OUR CENTER
		(else_try),
			(party_is_active, ":marshal_party"),
			(is_between, ":most_threatened_center", walled_centers_begin, walled_centers_end),
			(ge, ":threat_danger_level", ":target_value_level"),
			(party_slot_ge, ":most_threatened_center", slot_center_is_besieged_by, 0),

			(assign, ":action", sfai_attacking_enemies_around_center),
			(assign, ":object", ":most_threatened_center"),
						
			(str_store_party_name, s21, ":most_threatened_center"),
			(str_store_string, s14, "str_we_should_ride_to_break_the_siege_of_s21"),
			
		#3b - DEFEAT ENEMIES NEAR CENTER - similar to above, but a different string
		(else_try),
			(party_is_active, ":marshal_party"),
			(ge, ":threat_danger_level", ":target_value_level"),
			(is_between, ":most_threatened_center", villages_begin, villages_end),
		
			(assign, ":action", sfai_attacking_enemies_around_center),
			(assign, ":object", ":most_threatened_center"),
			(str_store_party_name, s21, ":most_threatened_center"),
			(str_store_string, s14, "str_we_should_ride_to_defeat_the_enemy_gathered_near_s21"),
				
		#4-DEMOBILIZATION
		#Let vassals attend their own business
		(else_try),
			(this_or_next|eq, ":current_ai_state", sfai_gathering_army), 				
			(this_or_next|eq, ":current_ai_state", sfai_attacking_center),
			(eq, ":current_ai_state", sfai_raiding_village),

			(ge, ":hours_since_last_faction_rest", ":campaign_hour_limit"), #Effected by ratio of vassals
			(ge, ":hours_at_current_state", 24),
			
			#Ozan : I am adding some codes here because sometimes armies demobilize during last seconds of an important event like taking a castle, ext.
			(assign, ":there_is_an_important_situation", 0),
			(try_begin), #do not demobilize during taking a castle/town (fighting in the castle)
				(is_between, ":current_ai_object", walled_centers_begin, walled_centers_end),
				(party_get_battle_opponent, ":besieger_party", ":current_ai_object"),
				(party_is_active, ":besieger_party"),
				(store_faction_of_party, ":besieger_faction", ":besieger_party"),
				(this_or_next|eq, ":besieger_faction", ":faction_no"),
				(eq, ":besieger_faction", "fac_player_faction"),
				(assign, ":there_is_an_important_situation", 1),
			(else_try), #do not demobilize during besieging a siege (holding around castle)
				(is_between, ":current_ai_object", walled_centers_begin, walled_centers_end),
				(party_get_slot, ":besieger_party", ":current_ai_object", slot_center_is_besieged_by),
				(party_is_active, ":besieger_party"),
				(store_faction_of_party, ":besieger_faction", ":besieger_party"),
				(this_or_next|eq, ":besieger_faction", ":faction_no"),
				(eq, ":besieger_faction", "fac_player_faction"),		  
				(assign, ":there_is_an_important_situation", 1),
			(else_try), #do not demobilize during raiding a village (holding around village)
				(is_between, ":current_ai_object", centers_begin, centers_end),
				(neg|is_between, ":current_ai_object", walled_centers_begin, walled_centers_end),		  
				(party_slot_eq, ":current_ai_object", slot_village_state, svs_being_raided),
				(assign, ":there_is_an_important_situation", 1),
			(try_end),
			
			(eq, ":there_is_an_important_situation", 0),
			#end addition ozan
						
			(assign, reg7, ":hours_since_last_faction_rest"),
			(assign, reg8, ":campaign_hour_limit"),
		
			(str_store_string, s14, "str_this_offensive_needs_to_wind_down_soon_so_the_vassals_can_attend_to_their_own_business"),		
			(assign, ":action", sfai_default),
			(assign, ":object", -1),
			
		#6-GATHERING BECAUSE OF NO REASON
		#Start to gather the army
		(else_try),
			(party_is_active, ":marshal_party"),
			(eq, ":at_peace_with_everyone", 0),
			
			
			(eq, ":current_ai_state", sfai_default),
			(ge, ":hours_since_last_offensive", 60),
			(lt, ":hours_since_last_faction_rest", 120),
			
			#There should not be a center as a precondition for attack	
			#Otherwise, we are unlikely to have a situation in which the army gathers, but does nothing -- which is important to have for role-playing purposes
			
			(assign, ":action", sfai_gathering_army),
			(assign, ":object", -1),	
			(str_store_string, s14, "str_it_is_time_to_go_on_the_offensive_and_we_must_first_assemble_the_army"),
		
            (try_begin),
              (eq, ":faction_no", "$players_kingdom"),
              (assign, "$g_gathering_reason", -1),
            (try_end),

		#7-OFFENSIVE ACTIONS : CONTINUE GATHERING
		(else_try),		
			(party_is_active, ":marshal_party"),
			(eq, ":current_ai_state", sfai_gathering_army),
			(eq, ":at_peace_with_everyone", 0),

			(lt, ":hours_at_current_state", 24), #gather army for 54 hours   #NE 24 hours
			
			(lt, ":ratio_of_vassals_assembled", 12),

			(str_store_string, s14, "str_we_must_continue_to_gather_the_army_before_we_ride_forth_on_an_offensive_operation"),
			(assign, ":action", sfai_gathering_army),
			(assign, ":object", -1),

		#7-OFFENSIVE ACTIONS PART 2 : CONTINUE GATHERING
		(else_try),
		    (assign, ":minimum_possible_attackable_target_value_level", 50),
			(eq, ":at_peace_with_everyone", 0),

            (try_begin), #agressive marshal            
			  (troop_get_slot, ":reputation", ":troop_no", slot_lord_reputation_type),
			  (this_or_next|eq, ":reputation", lrep_martial),
			  (this_or_next|eq, ":reputation", lrep_quarrelsome),
			  (eq, ":reputation", lrep_selfrighteous),
			  (val_mul, ":minimum_possible_attackable_target_value_level", 9),
			  (val_div, ":minimum_possible_attackable_target_value_level", 10),
            (try_end),		              

			(party_is_active, ":marshal_party"),
			(eq, ":current_ai_state", sfai_gathering_army),
								
			(try_begin),
				(lt, ":hours_at_current_state", 6),
				(assign, ":minimum_needed_target_value_level", 1500),
			(else_try),
				(lt, ":hours_at_current_state", 10),
				(assign, ":minimum_needed_target_value_level", 1000),
			(else_try),  
		        (lt, ":hours_at_current_state", 14),
		        (assign, ":minimum_needed_target_value_level", 720),
			(else_try),  
				(lt, ":hours_at_current_state", 18),
				(assign, ":minimum_needed_target_value_level", 480),
			(else_try),  
				(lt, ":hours_at_current_state", 22),
				(assign, ":minimum_needed_target_value_level", 360),
			(else_try),  
				(lt, ":hours_at_current_state", 26),
				(assign, ":minimum_needed_target_value_level", 240),
			(else_try),  
				(lt, ":hours_at_current_state", 30),
				(assign, ":minimum_needed_target_value_level", 180),
			(else_try),  
				(lt, ":hours_at_current_state", 34),
				(assign, ":minimum_needed_target_value_level", 120),
			(else_try),  
				(lt, ":hours_at_current_state", 38),
				(assign, ":minimum_needed_target_value_level", 100),
			(else_try),  
				(lt, ":hours_at_current_state", 42),
				(assign, ":minimum_needed_target_value_level", 80),
			(else_try),  
				(lt, ":hours_at_current_state", 46),
				(assign, ":minimum_needed_target_value_level", 65),
			(else_try),  
				(lt, ":hours_at_current_state", 50),
				(assign, ":minimum_needed_target_value_level", 55),
			(else_try),	
				(assign, ":minimum_needed_target_value_level", ":minimum_possible_attackable_target_value_level"),
			(try_end),  

            (try_begin), #agressive marshal            
			  (troop_get_slot, ":reputation", ":troop_no", slot_lord_reputation_type),
			  (this_or_next|eq, ":reputation", lrep_martial),
			  (this_or_next|eq, ":reputation", lrep_quarrelsome),
			  (eq, ":reputation", lrep_selfrighteous),
			  (val_mul, ":minimum_needed_target_value_level", 9),
			  (val_div, ":minimum_needed_target_value_level", 10),
            (try_end),		  
						
			(le, ":target_value_level", ":minimum_needed_target_value_level"),
			(le, ":hours_at_current_state", 24),  #NE 24
		
			(str_store_string, s14, "str_we_have_assembled_some_vassals"),
			(assign, ":action", sfai_gathering_army),
			(assign, ":object", -1),
				
		#8-ATTACK AN ENEMY CENTER case 1, reconnaissance against walled center
		#(else_try),
			#(party_is_active, ":marshal_party"),
			#(neq, ":current_ai_state", sfai_default),
			#(neq, ":current_ai_state", sfai_feast),
			#(is_between, ":center_to_attack", walled_centers_begin, walled_centers_end),

			#(store_sub, ":faction_recce_slot", ":faction_no", kingdoms_begin),
			#(val_add, ":faction_recce_slot", slot_center_last_reconnoitered_by_faction_time),
			#(store_current_hours, ":hours_since_last_recon"),			
			#(party_get_slot, ":last_recon_time", ":center_to_attack", ":faction_recce_slot"), 
			#(val_sub, ":hours_since_last_recon", ":last_recon_time"),
			#(this_or_next|eq, ":last_recon_time", 0),
			#(gt, ":hours_since_last_recon", 96),
						
		    #(assign, ":action", sfai_attacking_center),
			#(assign, ":object", ":center_to_attack"),
			#(str_store_string, s14, "str_we_are_conducting_recce"),
			
		#8-ATTACK AN ENEMY CENTER case 2, reconnaissance against village
		#(else_try),  
			#(party_is_active, ":marshal_party"),
			#(neq, ":current_ai_state", sfai_default),
			#(neq, ":current_ai_state", sfai_feast),
			#(is_between, ":center_to_attack", villages_begin, villages_end),

			#(store_sub, ":faction_recce_slot", ":faction_no", kingdoms_begin),
			#(val_add, ":faction_recce_slot", slot_center_last_reconnoitered_by_faction_time),
			#(store_current_hours, ":hours_since_last_recon"),
			#(party_get_slot, ":last_recon_time", ":center_to_attack", ":faction_recce_slot"), 
			#(val_sub, ":hours_since_last_recon", ":last_recon_time"),
			#(this_or_next|eq, ":last_recon_time", 0),
			#(gt, ":hours_since_last_recon", 96),

			
			#(assign, ":action", sfai_raiding_village),
			#(assign, ":object", ":center_to_attack"),
			#(str_store_string, s14, "str_we_are_conducting_recce"),
		(else_try),
			(party_is_active, ":marshal_party"),
			(neq, ":current_ai_state", sfai_default),
			(neq, ":current_ai_state", sfai_feast),
			
			(assign, ":center_to_attack", ":center_to_attack_only_marshal_and_followers"),
			
			(is_between, ":center_to_attack", walled_centers_begin, walled_centers_end),
			
			(ge, ":target_value_level", ":minimum_possible_attackable_target_value_level"),
						
		    (assign, ":action", sfai_attacking_center),
			(assign, ":object", ":center_to_attack"),
			(str_store_string, s14, "str_we_believe_the_fortress_will_be_worth_the_effort_to_take_it"),
		# (else_try), #NE
			# (party_is_active, ":marshal_party"),
			# (neq, ":current_ai_state", sfai_default),
			# (neq, ":current_ai_state", sfai_feast),
			
			# (assign, ":center_to_attack", ":center_to_attack_only_marshal_and_followers"),
			
			# (is_between, ":center_to_attack", villages_begin, villages_end),
			
			# (ge, ":target_value_level", ":minimum_possible_attackable_target_value_level"),
		
			# (assign, ":action", sfai_raiding_village),
			# (assign, ":object", ":center_to_attack"),
			# (str_store_string, s14, "str_we_shall_leave_a_fiery_trail_through_the_heart_of_the_enemys_lands_targeting_the_wealthy_settlements_if_we_can"),
		
		#9 -- DISBAND THE ARMY
		(else_try),
			(eq, ":current_ai_state", sfai_gathering_army),			

			(str_store_string, s14, "str_the_army_will_be_disbanded_because_we_have_been_waiting_too_long_without_a_target"),

			(assign, ":action", sfai_default),
			(assign, ":object", -1),
		#OFFENSIVE OPERATIONS END

		#FEAST-RELATED OPERATIONS BEGIN
		#10-CONCLUDE CURRENT FEAST
		(else_try),
			(eq, ":current_ai_state", sfai_feast),
			(gt, ":hours_at_current_state", 72),
		
			(assign, ":action", sfai_default),
			(assign, ":object", -1),		
			(str_store_string, s14, "str_it_is_time_for_the_feast_to_conclude"),

		#11-CONTINE FEAST UNLESS THERE IS AN EMERGENCY
		(else_try),
			(eq, ":current_ai_state", sfai_feast),
			(le, ":hours_at_current_state", 72),
			
			(assign, ":action", sfai_feast),
			(assign, ":object", ":current_ai_object"),		
			(str_store_string, s14, "str_we_should_continue_the_feast_unless_there_is_an_emergency"),
		
		#12-HOLD A FEAST BECAUSE THE PLAYER WANTS TO ORGANIZE ONE
		(else_try),
			(check_quest_active, "qst_organize_feast"),
			(eq, "$players_kingdom", ":faction_no"),
		
			(quest_get_slot, ":target_center", "qst_organize_feast", slot_quest_target_center),
			
			(assign, ":action", sfai_feast),
			(assign, ":object", ":target_center"),		
			(str_store_string, s14, "str_you_had_wished_to_hold_a_feast"),
		
		#13-HOLD A FEAST BECAUSE FEMALE PLAYER SCHEDULED TO GET MARRIED
		(else_try),
			(check_quest_active, "qst_wed_betrothed_female"),
				 
			(quest_get_slot, ":groom", "qst_wed_betrothed_female", slot_quest_giver_troop),
			(troop_slot_eq, ":groom", slot_troop_prisoner_of_party, -1),
		
			(store_faction_of_troop, ":groom_faction", ":groom"),
			(eq, ":groom_faction", ":faction_no"),
				 
			(faction_get_slot, ":faction_leader", ":groom_faction", slot_faction_leader),
				 
			(assign, ":location_feast", -1),
			(try_for_range, ":possible_location", walled_centers_begin, walled_centers_end),
			   (eq, ":location_feast", -1),
			    (party_slot_eq, ":possible_location", slot_town_lord, ":groom"),
			    (party_slot_ge, ":possible_location", slot_center_is_besieged_by, 0),
			    (assign, ":location_feast", ":possible_location"),
			(try_end),
			
			(try_for_range, ":possible_location", walled_centers_begin, walled_centers_end),
				(eq, ":location_feast", -1),
				(party_slot_eq, ":possible_location", slot_town_lord, ":faction_leader"),
				(party_slot_ge, ":possible_location", slot_center_is_besieged_by, 0),
				(assign, ":location_feast", ":possible_location"),
			(try_end),
		 
			(is_between, ":location_feast", walled_centers_begin, walled_centers_end),

			(assign, ":action", sfai_feast),
			(assign, ":object", ":location_feast"),		
			(str_store_string, s14, "str_your_wedding_day_approaches_my_lady"),
		
		#14-HOLD A FEAST BECAUSE A MALE CHARACTER WANTS TO GET MARRIED
		(else_try),
			(check_quest_active, "qst_wed_betrothed"),
			(neg|quest_slot_ge, "qst_wed_betrothed", slot_quest_expiration_days, 362),
		
			(quest_get_slot, ":bride", "qst_wed_betrothed", slot_quest_target_troop),
			(call_script, "script_get_kingdom_lady_social_determinants", ":bride"),
			(assign, ":feast_host", reg0),
			(store_faction_of_troop, ":feast_host_faction", ":feast_host"),
			(eq, ":feast_host_faction", ":faction_no"),
		
			(troop_slot_eq, ":feast_host", slot_troop_prisoner_of_party, -1),
			(assign, ":wedding_venue", reg1),
		
			(is_between, ":wedding_venue", centers_begin, centers_end),
			(party_slot_eq, ":wedding_venue", slot_center_is_besieged_by, -1),
		
			(assign, ":action", sfai_feast),
			(assign, ":object", ":wedding_venue"),		
			(str_store_string, s14, "str_your_wedding_day_approaches"),
		
		#15-HOLD A FEAST BECAUSE AN NPC WANTS TO GET MARRIED
		(else_try),	
            (ge, ":hours_since_last_feast_start", 192), #If at least eight days past last feast start time
		
			(assign, ":location_feast", -1),
		
			(try_for_range, ":kingdom_lady", kingdom_ladies_begin, kingdom_ladies_end),
				(troop_get_slot, ":groom", ":kingdom_lady", slot_troop_betrothed),
				(gt, ":groom", 0), #not the player

				(store_faction_of_troop, ":lady_faction", ":kingdom_lady"),
				(store_faction_of_troop, ":groom_faction", ":groom"),
				
				(try_begin), #The groom checks if he wants to continue or break off relations. This causes actions, rather than just returns a value, so it probably should be moved elsewhere
					(troop_slot_ge, ":groom", slot_troop_prisoner_of_party, 0),		
				(else_try),
					(neq, ":groom_faction", ":lady_faction"),
					(neq, ":groom_faction", "fac_player_faction"),
					(call_script, "script_courtship_event_lady_break_relation_with_suitor", ":kingdom_lady", ":groom"),
				(else_try),
		            (eq, ":lady_faction", ":faction_no"),
		            (store_current_hours, ":hours_since_betrothal"),
		            (troop_get_slot, ":betrothal_time", ":kingdom_lady", slot_troop_betrothal_time),
		            (val_sub, ":hours_since_betrothal", ":betrothal_time"),
		            (ge, ":hours_since_betrothal", 719), #30 days
							
					(call_script, "script_get_kingdom_lady_social_determinants", ":kingdom_lady"), 
					(assign, ":wedding_venue", reg1),
				
		            (assign, ":location_feast", ":wedding_venue"),
		            (assign, ":final_bride", ":kingdom_lady"),
		            (assign, ":final_groom", ":groom"),
				(try_end),	
			(try_end),
		
			(ge, ":location_feast", centers_begin),
				 
			(assign, ":action", sfai_feast),
			(assign, ":object", ":location_feast"),
				
			(str_store_troop_name, s22, ":final_bride"),
			(str_store_troop_name, s23, ":final_groom"),		
			(str_store_string, s14, "str_s22_and_s23_wish_to_marry"),

		#16-HOLD A FEAST ANYWAY
		(else_try),
			(eq, ":current_ai_state", sfai_default),
            (gt, ":hours_since_last_feast_start", 740), #If at least 10 days past after last feast. (added by ozan)  #NE used to be 240

			(assign, ":location_high_score", 0),
			(assign, ":location_feast", -1),
        
			(try_for_range, ":location", walled_centers_begin, walled_centers_end),
				(store_faction_of_party, ":location_faction", ":location"),
				(eq, ":location_faction", ":faction_no"),

				(try_begin),
			        (neg|party_slot_eq, ":location", slot_village_state, svs_under_siege),
		            (party_get_slot, ":location_lord", ":location", slot_town_lord),
		            (is_between, ":location_lord", active_npcs_begin, active_npcs_end),
		            (troop_get_slot, ":location_score", ":location_lord", slot_troop_renown),
		            (store_random_in_range, ":random", 0, 1000), #will probably be king or senior lord
		            (val_add, ":location_score", ":random"),
		            (gt, ":location_score", ":location_high_score"),
		            (assign, ":location_high_score", ":location_score"),
		            (assign, ":location_feast", ":location"),				
				(else_try), #do not start new feasts if any place is under siege or being raided
		            (this_or_next|party_slot_eq, ":location", slot_village_state, svs_under_siege),
						(party_slot_eq, ":location", slot_village_state, svs_being_raided),
		            (assign, ":location_high_score", 9999),
		            (assign, ":location_feast", -1),
				(try_end),
			(try_end),

			(is_between, ":location_feast", walled_centers_begin, walled_centers_end),
			(party_get_slot, ":feast_host", ":location_feast", slot_town_lord),
			(troop_slot_eq, ":feast_host", slot_troop_prisoner_of_party, -1),
		
			(assign, ":action", sfai_feast),
			(assign, ":object", ":location_feast"),		
			(str_store_string, s14, "str_it_has_been_a_long_time_since_the_lords_of_the_realm_gathered_for_a_feast"),	
		
		#17-DO NOTHING #NE
		# (else_try),
			# (neq, ":current_ai_state", sfai_default),
		
			# (assign, ":action", sfai_default),
			# (assign, ":object", -1),		
			# (str_store_string, s14, "str_the_circumstances_which_led_to_this_decision_no_longer_apply_so_we_should_stop_and_reconsider_shortly"),	
	
		#18-DO NOTHING
		(else_try),
			(eq, ":current_ai_state", sfai_default),

			(eq, ":at_peace_with_everyone", 1),
				
		    (assign, ":action", sfai_default),
		    (assign, ":object", -1),		
			(str_store_string, s14, "str_we_are_currently_at_peace"),		
		(else_try),
			(eq, ":current_ai_state", sfai_default),
			(faction_slot_eq, ":faction_no", slot_faction_marshall, -1),				
		    (assign, ":action", sfai_default),
		    (assign, ":object", -1),		
			(str_store_string, s14, "str_we_are_waiting_for_selection_of_marshal"),		
		
		(else_try),
			(eq, ":current_ai_state", sfai_default),
								
		    (assign, ":action", sfai_default),
		    (assign, ":object", -1),		
			(str_store_string, s14, "str_the_vassals_still_need_time_to_attend_to_their_own_business"),		
		(try_end),
				
		(assign, reg0, ":action"),
		(assign, reg1, ":object"),		
	]),
####################################	
	    ("find_center_to_attack_alt_dk2",
    [
      (store_script_param, ":troop_no", 1),
      (store_script_param, ":attack_by_faction", 2),
      (store_script_param, ":all_vassals_included", 3),
      
      (assign, ":result", -1),
      (assign, ":score_to_beat", 0),
      
      (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),            #NE changed to Walled
        (call_script, "script_npc_decision_checklist_evaluate_enemy_center_for_attack_dk2",	":troop_no", ":center_no", ":attack_by_faction", ":all_vassals_included"),
        (assign, ":score", reg0),
		
	    # (assign, reg1,  ":score"),
		# (str_store_party_name, s8, ":center_no"),       
          # (display_message, "@FUCK : attack of {s8} score to beat:{reg1}"),
                
        (gt, ":score", ":score_to_beat"),
        
        (assign, ":result", ":center_no"),
        (assign, ":score_to_beat", ":score"),
		

		  
      (try_end),
      

      (assign, reg0, ":result"),
      (assign, reg1, ":score_to_beat"),      
	  

		  
		  
	]),
  ("npc_decision_checklist_evaluate_enemy_center_for_attack_dk2",
    [
      #NOTES -- LAST OFFENSIVE TIME SCORE IS NOT USED
      
      (store_script_param, ":troop_no", 1),
      (store_script_param, ":potential_target", 2),
      (store_script_param, ":attack_by_faction", 3),
      (store_script_param, ":all_vassals_included", 4),
      
      (assign, ":result", -1),
      (assign, ":explainer_string", -1),
      #(assign, ":reason_is_obvious", 0),
      (assign, ":power_ratio", 0),
      #(assign, ":hours_since_last_recce", -1),
      
      #(assign, ":value_of_target", 0),
      #(assign, ":difficulty_of_capture", 0),
      (store_faction_of_troop, ":faction_no", ":troop_no"),
      
      (try_begin),
        (eq, ":attack_by_faction", 1),
        (faction_get_slot, ":faction_marshal", ":faction_no", slot_faction_marshall),
        (ge, ":faction_marshal", 0), #STEVE ADDITION TO AVOID MESSAGE SPAM
        (troop_get_slot, ":party_no", ":faction_marshal", slot_troop_leaded_party),
      (else_try),
        (troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
      (try_end),
      
      (assign, "$g_use_current_ai_object_as_s8", 0),
            
      #THE FIRST BATCH OF DISQUALIFYING CONDITIONS DO NOT REQUIRE THE ATTACKING PARTY TO HAVE CURRENT INTELLIGENCE ON THE TARGET
      (try_begin),
        (neg|party_is_active, ":party_no"),
        
        (assign, ":result", -1),
        (assign, ":explainer_string", "str_center_party_not_active"),
        #(assign, ":reason_is_obvious", 1),
      (else_try), 
        (store_faction_of_party, ":potential_target_faction", ":potential_target"),
        (store_relation, ":relation", ":potential_target_faction", ":faction_no"),
        (ge, ":relation", 0),
        
        (assign, ":result", -1),
        (assign, ":explainer_string", "str_center_is_friendly"),
        #(assign, ":reason_is_obvious", 1),
      (else_try),
        (is_between, ":potential_target", walled_centers_begin, walled_centers_end),
        (assign, ":faction_of_besieger_party", -1),
        (try_begin),
          (neg|party_slot_eq, ":potential_target", slot_center_is_besieged_by, -1), 
          (party_get_slot, ":besieger_party", ":potential_target", slot_center_is_besieged_by),
          (party_is_active, ":besieger_party"),
          (store_faction_of_party, ":faction_of_besieger_party", ":besieger_party"),
        (try_end),
        
        (neq, ":faction_of_besieger_party", -1),
        (neq, ":faction_of_besieger_party", ":faction_no"),	
        
        (assign, ":result", -1),
        (assign, ":explainer_string", "str_center_is_already_besieged"),
        #(assign, ":reason_is_obvious", 1),
      (else_try),
        (is_between, ":potential_target", villages_begin, villages_end),
        (assign, ":village_is_looted_or_raided_already", 0),
        (try_begin),
          (party_slot_eq, ":potential_target", slot_village_state, svs_being_raided),
          (party_get_slot, ":raider_party", ":potential_target", slot_village_raided_by),
		  (party_is_active, ":raider_party"),
          (store_faction_of_party, ":raider_faction", ":raider_party"),
          (neq, ":raider_faction", ":faction_no"),
          (assign, ":raiding_by_one_other_faction", 1),
        (else_try),
          (assign, ":raiding_by_one_other_faction", 0),
        (try_end),
        
        (try_begin),
          (this_or_next|party_slot_eq, ":potential_target", slot_village_state, svs_looted),
          (eq, ":raiding_by_one_other_faction", 1),
          (assign, ":village_is_looted_or_raided_already", 1),
        (try_end),
        
        (eq, ":village_is_looted_or_raided_already", 1),
        
        (assign, ":result", -1),
        (assign, ":explainer_string", "str_center_is_looted_or_raided_already"),
        #(assign, ":reason_is_obvious", 1),
      (else_try),
        # (this_or_next|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_upstanding), #NE
        # (troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_goodnatured),
        
        (is_between, ":potential_target", villages_begin, villages_end),	
        (assign, ":result", -1),
        (assign, ":explainer_string", "str_center_marshal_does_not_want_to_attack_innocents"),
      #(else_try),
        # (assign, ":distance_from_our_closest_walled_center", 1000),
        # (try_for_range, ":cur_center", walled_centers_begin, walled_centers_end),
           # (store_faction_of_party, ":cur_center_faction", ":cur_center"),
           # (eq, ":cur_center_faction", ":faction_no"),
           # (store_distance_to_party_from_party, ":distance_from_cur_center", ":cur_center", ":potential_target"),
           # (lt, ":distance_from_cur_center", ":distance_from_our_closest_walled_center"),
           # (assign, ":distance_from_our_closest_walled_center", ":distance_from_cur_center"),
        # (try_end),
                                                
        # (gt, ":distance_from_our_closest_walled_center", 75),
        # (this_or_next|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_upstanding),
        # (this_or_next|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_debauched),
        # (this_or_next|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_goodnatured),
        # (troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_cunning),
        
        # (assign, ":result", -1),
        # (assign, ":explainer_string", "str_center_far_away_our_cautious_marshal_does_not_wish_to_reconnoiter"),	

        #NE - DKs won't have a base at start so take that into account
		
       # (assign, ":distance_from_our_closest_walled_center", 1000),
		# (assign, ":have_center", 0), 
        # (try_for_range, ":cur_center", walled_centers_begin, walled_centers_end),
           # (store_faction_of_party, ":cur_center_faction", ":cur_center"),
		   # (try_begin), 
           # (eq, ":cur_center_faction", "fac_dark_knights"),
		   # (assign, ":have_center", 1), 
		   # (try_end), 
        # (try_end), 		

		# (try_begin),
		# (eq, ":have_center", 1), 
        #######(assign, ":distance_from_our_closest_walled_center", 1000),
          # (try_for_range, ":cur_center", walled_centers_begin, walled_centers_end),
           # (store_faction_of_party, ":cur_center_faction", ":cur_center"),
           # (eq, ":cur_center_faction", ":faction_no"),
           # (store_distance_to_party_from_party, ":distance_from_cur_center", ":cur_center", ":potential_target"),
           # (lt, ":distance_from_cur_center", ":distance_from_our_closest_walled_center"),
           # (assign, ":distance_from_our_closest_walled_center", ":distance_from_cur_center"),
          # (try_end),	
		
		# (else_try), 
		   # (assign, ":distance_from_cur_center", 10),		   
           # (lt, ":distance_from_cur_center", ":distance_from_our_closest_walled_center"),
           # (assign, ":distance_from_our_closest_walled_center", ":distance_from_cur_center"),
		# (try_end), 
                                             
		
        # (gt, ":distance_from_our_closest_walled_center", 75),
        # (assign, ":result", -1),
        # (assign, ":explainer_string", "str_center_far_away_our_cautious_marshal_does_not_wish_to_reconnoiter"),				
  	  
		
      #RECONNOITERING BEGINS HERE - VALUE WILL BE TEN OR LESS
      # (else_try),
        # (gt, ":distance_from_our_closest_walled_center", 90),
        
        # (assign, ":result", -1),
        # (assign, ":explainer_string", "str_center_far_away_even_for_our_aggressive_marshal_to_reconnoiter"),
        ####(assign, ":reason_is_obvious", 1),	
      # (else_try),
        # (is_between, ":potential_target", walled_centers_begin, walled_centers_end),
        ###(neg|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_martial),
        ###(neg|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_quarrelsome),
        ###(neg|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_selfrighteous),
        #NE
		# (assign, ":have_center", 0), 
        # (try_for_range, ":cur_center", walled_centers_begin, walled_centers_end),
           # (store_faction_of_party, ":cur_center_faction", ":cur_center"),
		   # (try_begin), 
           # (eq, ":cur_center_faction", "fac_dark_knights"),
		   # (assign, ":have_center", 1), 
		   # (try_end), 
        # (try_end), 	
		
		# (try_begin), 
		# (eq, ":have_center", 1), #NE
        # (assign, ":close_center_found", 0),
        # (try_for_range, ":friendly_walled_center", walled_centers_begin, walled_centers_end),
          # (eq, ":close_center_found", 0),
          # (store_faction_of_party, ":friendly_walled_center_faction", ":friendly_walled_center"),
          # (eq, ":friendly_walled_center_faction", ":faction_no"),
          # (store_distance_to_party_from_party, ":distance_from_walled_center", ":potential_target", ":friendly_walled_center"),
          # (lt, ":distance_from_walled_center", 60),
          # (assign, ":close_center_found", 1),
		  
		
		
        # (try_end),
        # (eq, ":close_center_found", 0),
        
        # (assign, ":result", -1),
        # (assign, ":explainer_string", "str_center_is_indefensible"),	
		# (else_try), 
		
		
		# (try_end), #NE
      #(else_try),
        #For now it is removed as Armagan's decision, we can add this option in later patchs. I and Armagan accept it has good potential. But this system needs also
        #scouting quests and scouting AI added together. If we only add this then we limit AI very much, it can attack only very few of centers, this damages 
        #variability of game and surprise attacks of AI. Player can predict where AI will attack and he can full garnisons of only this center. 
        #We can add asking travellers about how good defended center X by paying 100 denars for example to equalize situations of AI and human player.
        #But these needs much work and detailed AI tests so Armagan decided to skip this for now.
        
        #(store_sub, ":faction_recce_slot", ":faction_no", kingdoms_begin),
        #(val_add, ":faction_recce_slot", slot_center_last_reconnoitered_by_faction_time),
        #(party_get_slot, ":last_recce_time", ":potential_target", ":faction_recce_slot"),
        #(store_current_hours, ":hours_since_last_recce"),
        #(val_sub, ":hours_since_last_recce", ":last_recce_time"),
        
        #(this_or_next|eq, ":last_recce_time", 0),
        #(gt, ":hours_since_last_recce", 96), #Information is presumed to be accurate for four days
        
        #(store_sub, ":150_minus_distance_div_by_10", 150, ":distance_from_party"),
        #(val_div, ":150_minus_distance_div_by_10", 10),
        
        #(assign, ":result", ":150_minus_distance_div_by_10"),
        #(assign, ":explainer_string", "str_center_has_not_been_scouted"),
      #DECISIONS BASED ON ENEMY STRENGTH BEGIN HERE
	  #NE
      # (else_try),
        # (party_get_slot, ":party_strength", ":party_no", slot_party_cached_strength),
        # (party_get_slot, ":follower_strength", ":party_no", slot_party_follower_strength),
        # (party_get_slot, ":strength_of_nearby_friend", ":party_no", slot_party_nearby_friend_strength),                
        
        # (store_add, ":total_strength", ":party_strength", ":follower_strength"),
        # (val_add, ":total_strength", ":strength_of_nearby_friend"),
        
       ## (party_get_slot, ":potential_target_nearby_enemy_exact_strength", ":potential_target", slot_party_nearby_friend_strength),
        #(assign, ":potential_target_nearby_enemy_strength", ":potential_target_nearby_enemy_exact_strength"),                
        # (try_begin),
          # (is_between, ":potential_target", villages_begin, villages_end),
          # (assign, ":enemy_strength", 10),
        # (else_try),
          # (party_get_slot, ":enemy_strength", ":potential_target", slot_party_cached_strength),
          # (party_get_slot, ":enemy_strength_nearby", ":potential_target", slot_party_nearby_friend_strength),
          # (val_add, ":enemy_strength", ":enemy_strength_nearby"),
        # (try_end),
        # (val_max, ":enemy_strength", 1),                

        # (this_or_next|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_martial),
        # (this_or_next|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_quarrelsome),
        # (troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_selfrighteous),
        
        # (store_mul, ":power_ratio", ":total_strength", 100),
        # (val_div, ":power_ratio", ":enemy_strength"),
        # (lt, ":power_ratio", 150), 
        
        # (assign, ":result", -1),
        # (assign, ":explainer_string", "str_center_protected_by_enemy_army_aggressive"),
      # (else_try),
        # (ge, ":enemy_strength", ":total_strength"), #if enemy is powerful
        
        # (assign, ":result", -1),
        # (assign, ":explainer_string", "str_center_protected_by_enemy_army_cautious"),
      # (else_try),               
        # (store_mul, ":power_ratio", ":total_strength", 100),
        # (val_div, ":power_ratio", ":enemy_strength"),
        # (lt, ":power_ratio", 185), 
        
        # (this_or_next|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_upstanding),
        # (this_or_next|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_debauched),
        # (this_or_next|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_goodnatured),
        # (troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_cunning),
        
       ## equations here
        # (assign, ":result", -1),
        # (assign, ":explainer_string", "str_center_cautious_marshal_believes_center_too_difficult_to_capture"),
      # (else_try),
        # (lt, ":power_ratio", 140), #it was 140
        
        # (assign, ":result", -1),
        # (assign, ":explainer_string", "str_center_even_aggressive_marshal_believes_center_too_difficult_to_capture"),
      ##To Steve - I moved below two if statement here from upper places, to enable in answering different different answers even 
      ##if we are close to an unlooted enemy village. For example now it can say "center X" is too far too while our army is 
      ##looting a village because of its closeness.
      (else_try),
        #if the party has already started the siege
        (faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_raiding_village),
        (faction_get_slot, ":current_object", ":faction_no", slot_faction_ai_object),
        (is_between, ":current_object", villages_begin, villages_end),
        (neq, ":potential_target", ":current_object"),
        (party_slot_eq, ":current_object", slot_village_state, svs_under_siege),
        
        (store_current_hours, ":hours_since_siege_began"),
        (party_get_slot, ":hour_that_siege_began", ":current_object", slot_center_siege_begin_hours),
        (val_sub, ":hours_since_siege_began", ":hour_that_siege_began"),
        (gt, ":hours_since_siege_began", 4),
        
        (call_script, "script_npc_decision_checklist_evaluate_enemy_center_for_attack_dk2", ":troop_no", ":current_object", ":attack_by_faction", 0),
        (gt, reg0, -1),
        
        (assign, ":result", -1),
        (assign, ":explainer_string", "str_center_we_have_already_committed_too_much_time_to_our_present_siege_to_move_elsewhere"),
		###NE
      #(else_try),
        #If the party is close to an unlooted village
        # (faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_raiding_village),
        # (faction_get_slot, ":current_object", ":faction_no", slot_faction_ai_object),       
        # (neq, ":potential_target", ":current_object"),
        # (is_between, ":current_object", villages_begin, villages_end),
        # (store_distance_to_party_from_party, ":distance_to_cur_object", ":party_no", ":current_object"),
        # (lt, ":distance_to_cur_object", 10),
        
        # (call_script, "script_npc_decision_checklist_evaluate_enemy_center_for_attack", ":troop_no", ":current_object", ":attack_by_faction", 0),
        # (gt, reg0, -1),
        
        # (assign, "$g_use_current_ai_object_as_s8", 1),
                
        # (assign, ":result", -1),
        # (assign, ":explainer_string", "str_center_we_are_already_here_we_should_at_least_loot_the_village"),
      #DECISION TO ATTACK IS HERE
      #(else_try),
        #To Steve - I removed below lines, as here decided. We will use pre-function to evaluate assailability scores for centers rather than below lines to make AI 
        #selecting better targets. If you want to make some marshals to select not-best options I can add that option into script_calculate_center_assailability_score, 
        #for that we can need seed values for each center and for each lord, so we can add these seed values to create variability, clever marshals have seeds with less 
        #standard deviation and less values and less-clever marshals have bigger seeds. Then probability of some lords to disagree marshal increases because their seed 
        #values will be different from marshal's. If Steve wants it from me to implement I can add this.
      
        #(try_begin),
        #  (is_between, ":potential_target", villages_begin, villages_end),
        #  (party_get_slot, ":score", ":potential_target", slot_town_prosperity),
        #  (val_add, ":score", 50), #average 100
        #(else_try),
        #  (is_between, ":potential_target", castles_begin, castles_end),
        #  (assign, ":score", ":power_ratio"), #ie, at least 140
        #(else_try),	
        #  (party_get_slot, ":score", ":potential_target", slot_town_prosperity),
        #  (val_add, ":score", 75),
        #  (val_mul, ":score", ":power_ratio"),
        #  (val_div, ":score", 100), #ie, at least about 200
        #(try_end),
        # 
        #(val_sub, ":score", ":distance_from_party"),
        #(lt, ":score", -1),
      
        #(assign, ":result", -1),
        #(assign, ":explainer_string", "str_center_value_outweighed_by_difficulty_of_capture"),
     (else_try),
        (try_begin),
          (eq, "$cheat_mode", 1),
          (eq, ":faction_no", "fac_kingdom_3"),
          (store_faction_of_party, ":potential_target_faction", ":potential_target"),
          (store_relation, ":relation", ":potential_target_faction", ":faction_no"),
          (lt, ":relation", 0),
        (try_end),  
         # (display_message, "@ Calculating assailability"),
        (call_script, "script_calculate_center_assailability_score_dk2", ":troop_no", ":potential_target", ":all_vassals_included"),
        (assign, ":score", reg0),
        (assign, ":power_ratio", reg1),
        #(assign, ":distance_score", reg2),
      
        (assign, ":result", ":score"),
		
		#####NE
		# (str_store_party_name, s11, ":potential_target"),
		####HERE HERE 
	    # (display_message, "@ Target: {s11}, Score: {reg0}, power ratio {reg1}"),
		# (val_add, ":power_ratio", 200),
      
        (try_begin),
          (le, ":power_ratio", 100),
          (try_begin),
            (this_or_next|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_upstanding),
            (this_or_next|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_debauched),
            (this_or_next|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_goodnatured),
            (troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_cunning),	      	      
            (assign, ":explainer_string", "str_center_cautious_marshal_believes_center_too_difficult_to_capture"),
          (else_try),
            (assign, ":explainer_string", "str_center_even_aggressive_marshal_believes_center_too_difficult_to_capture"),
          (try_end),
        (else_try),
          (le, ":power_ratio", 150),
        
          (try_begin),
	        (this_or_next|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_upstanding),
	        (this_or_next|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_debauched),
	        (this_or_next|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_goodnatured),
	        (troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_cunning),	      	      
	        (assign, ":explainer_string", "str_center_protected_by_enemy_army_cautious"),
	      (else_try),
	        (assign, ":explainer_string", "str_center_protected_by_enemy_army_aggressive"),
	      (try_end),
	    (else_try),
	      (try_begin),
	        (le, ":score", "$g_faction_object_score"),
	        (assign, ":explainer_string", "str_center_value_outweighed_by_difficulty_of_capture"),
	      (else_try),
	        #To Steve, does not this sentence needs to explain why we are not attacking that city? 
	        #This sentence says it justifies, so why we are not attacking?
	        (assign, ":explainer_string", "str_center_value_justifies_the_difficulty_of_capture"),
	      (try_end),
	    (try_end),
	  (try_end),
	  	  
		  
		 ##### # NE 
     # (str_store_string, s7, ":explainer_string"),
	 # (str_store_party_name, s8, ":potential_target"),
      
     # (display_message, "@DEBUG : attack of {s8} is {s7}"),
	
	  (assign, reg0, ":result"),
	  (assign, reg1, ":explainer_string"),
	  (assign, reg2, ":power_ratio"),	  	

     ]),
			  ################################
    #script_calculate_center_assailability_score
    # INPUT: faction_no
    # param1: faction_no 
    # param2: all_vassals_included, (becomes 1 if we want to find attackable center if we collected 20% of vassals during gathering army phase)
    # OUTPUT: 
    # reg0 = center_to_attack (-1 if none is logical)
    # reg1 = maximum_attack_score
    (
    "calculate_center_assailability_score_dk2", 
    [		
      (store_script_param, ":troop_no", 1),
      (store_script_param, ":potential_target", 2),
      (store_script_param, ":all_vassals_included", 3),
      
      (assign, ":target_score", -1),
      
      (store_faction_of_troop, ":faction_no", ":troop_no"),
  
      (store_current_hours, ":hours_since_last_offensive"),
      (faction_get_slot, ":last_offensive_time", ":faction_no", slot_faction_last_offensive_concluded),
      (val_sub, ":hours_since_last_offensive", ":last_offensive_time"),
      
      (store_div, ":last_offensive_time_score", ":hours_since_last_offensive", 12), #30..50
      (val_add, ":last_offensive_time_score", 30),
      (val_min, ":last_offensive_time_score", 100),

      (faction_get_slot, ":faction_marshal", ":faction_no", slot_faction_marshall),
    
      (assign, ":marshal_party", -1),
      (assign, ":marshal_strength", 0),
      #(assign, ":strength_of_nearby_friend", 0),
      
      (try_begin),
        (gt, ":faction_marshal", 0),
        (troop_get_slot, ":marshal_party", ":faction_marshal", slot_troop_leaded_party),
        (party_is_active, ":marshal_party"),
        (party_get_slot, ":marshal_strength", ":marshal_party", slot_party_cached_strength),
        #(eq, ":all_vassals_included", 0),
        (party_get_slot, ":strength_of_current_followers", ":marshal_party", slot_party_follower_strength),
        #(party_get_slot, ":strength_of_nearby_friend", ":marshal_party", slot_party_nearby_friend_strength),
      (try_end),
  
      #(try_begin),
      #  (eq, ":all_vassals_included", 0),
      #    
      #  (try_begin),
      #    (gt, ":faction_marshal", 0),
      #    (troop_get_slot, ":marshal_party", ":faction_marshal", slot_troop_leaded_party),
      #    (party_is_active, ":marshal_party"),
      #    (party_get_slot, ":strength_of_potential_followers", ":marshal_party", slot_party_follower_strength),
      #  (try_end),                
      #(else_try),
      #  (eq, ":all_vassals_included", 1),
      #      
      #  (assign, ":strength_of_potential_followers", 0),
      #          
      #  (try_for_parties, ":party_no"),
      #    (store_faction_of_party, ":party_faction", ":party_no"),
      #    (eq, ":party_faction", ":faction_no"),
      #    (neq, ":party_no", ":marshal_party"),          
      #    (party_slot_eq, ":party_no", slot_party_type, spt_kingdom_hero_party),
      #    (call_script, "script_party_calculate_strength", ":party_no", 0),
      #    (val_add, ":strength_of_potential_followers", reg0),
      #  (try_end),    
      #  
      #  (val_div, ":strength_of_potential_followers", 2), #Ozan - Think about this, will you divide strength_of_potential_followers to 3 or 2.5 or 2
      #(else_try),
      #  (assign, ":strength_of_potential_followers", 0),      
      #(try_end),
      
      (faction_get_slot, ":last_attacked_center", ":faction_no", slot_faction_last_attacked_center),
      (faction_get_slot, ":last_attacked_hours", ":faction_no", slot_faction_last_attacked_hours),
            
      (try_begin),
        (store_current_hours, ":hours"),
        (store_add, ":last_attacked_hours_plus_24", ":last_attacked_hours", 24),
        (gt, ":hours", ":last_attacked_hours_plus_24"),
        (faction_set_slot, ":faction_no", slot_faction_last_attacked_center, 0),
        (assign, ":last_attacked_center", 0),
      (try_end),
                
      (try_begin),        
        (this_or_next|eq, ":last_attacked_center", 0),
        (this_or_next|eq, ":last_attacked_center", ":potential_target"),
        (this_or_next|eq, "$g_do_not_skip_other_than_current_ai_object", 1),
        (neg|faction_slot_eq, ":faction_no", slot_faction_marshall, ":troop_no"),
        
        (party_is_active, ":potential_target"),
        (store_faction_of_party, ":potential_target_faction", ":potential_target"),
          
        (store_relation, ":relation", ":potential_target_faction", ":faction_no"),	      
        (lt, ":relation", 0),
        
        #attack if and only if we are already besieging that center or anybody do not making besiege.
        (assign, ":faction_of_besieger_party", -1),
        (try_begin),        
          (is_between, ":potential_target", walled_centers_begin, walled_centers_end),      
          (neg|party_slot_eq, ":potential_target", slot_center_is_besieged_by, -1), 
          (party_get_slot, ":besieger_party", ":potential_target", slot_center_is_besieged_by),
          (party_is_active, ":besieger_party"),
          (store_faction_of_party, ":faction_of_besieger_party", ":besieger_party"),
        (try_end),	
        			     
        (this_or_next|eq, ":faction_of_besieger_party", -1), 
        (eq, ":faction_of_besieger_party", ":faction_no"),
        
        #attack if and only if this center is not a village or if it is village it should not be raided or looted
        (assign, ":village_is_looted_or_raided_already", 0),
        (try_begin),
          (is_between, ":potential_target", villages_begin, villages_end),
          (try_begin),
            (party_slot_eq, ":potential_target", slot_village_state, svs_being_raided),
            (party_get_slot, ":raider_party", ":potential_target", slot_village_raided_by),
			(party_is_active, ":raider_party"),
			
            (store_faction_of_party, ":raider_faction", ":raider_party"),
            (neq, ":raider_faction", ":faction_no"),
            (assign, ":raiding_by_one_other_faction", 1),
          (else_try),
            (assign, ":raiding_by_one_other_faction", 0),
          (try_end),  
          (this_or_next|party_slot_eq, ":potential_target", slot_village_state, svs_looted),
          (eq, ":raiding_by_one_other_faction", 1),
          (assign, ":village_is_looted_or_raided_already", 1),
        (try_end),        
        (eq, ":village_is_looted_or_raided_already", 0),

        #if ":potential_target" is faction object of some other faction which is enemy to owner of 
        #":potential_target" then this target cannot be new target we are looking for.
        (assign, ":this_potantial_target_is_target_of_some_other_faction", 0),
        (try_for_range, ":cur_faction", kingdoms_begin, kingdoms_end),
          (is_between, ":cur_faction", "fac_kingdom_1", kingdoms_end), #Excluding player kingdom
          (neq, ":cur_faction", ":faction_no"),
          (faction_get_slot, ":faction_object", ":cur_faction", slot_faction_ai_object),
          (eq, ":faction_object", ":potential_target"),
          (store_relation, ":rel", ":potential_target_faction", ":cur_faction"),
          (lt, ":rel", 0),
          (assign, ":this_potantial_target_is_target_of_some_other_faction", 1),          
        (try_end),      
        (eq, ":this_potantial_target_is_target_of_some_other_faction", 0),                                            
    		  				
        (try_begin),
          (is_between, ":potential_target", walled_centers_begin, walled_centers_end),      
          (party_get_slot, ":potential_target_inside_strength", ":potential_target", slot_party_cached_strength),
          (party_get_slot, ":potential_target_nearby_enemy_strength", ":potential_target", slot_party_nearby_friend_strength),    
          (val_div, ":potential_target_nearby_enemy_strength", 2),        
          (store_add, ":potential_target_strength", ":potential_target_inside_strength", ":potential_target_nearby_enemy_strength"),

          #(try_begin),
            #(eq, ":faction_no", "fac_kingdom_4"),
            #(assign, reg0, ":potential_target_inside_strength"),
            #(assign, reg1, ":potential_target_nearby_enemy_strength"),
            #(assign, reg2, ":marshal_strength"),
            #(assign, reg3, ":strength_of_potential_followers"),
            #(assign, reg4, ":strength_of_nearby_friend"),
            #(assign, reg6, ":marshal_party"),
            #(str_store_party_name, s8, ":potential_target"),
            #(eq, ":all_vassals_included", 0),
            #(display_message, "@DEBUG : {s8}:{reg0}, neare {reg1}, our {reg2}, follow {reg3}, nearf {reg4}"),
          #(try_end),
                    
          (val_mul, ":potential_target_strength", 4), #in walled centers defenders have advantage.
          (val_div, ":potential_target_strength", 3),
                              
          #(store_add, ":army_strength", ":marshal_strength", ":strength_of_potential_followers"),
          (assign, ":army_strength", ":marshal_strength"),
          (val_add, ":army_strength", ":strength_of_current_followers"),
          (store_mul, ":power_ratio", ":army_strength", 100),
          
          #this ratio ":power_ratio" shows (our total army power) / (their total army power)
          (try_begin),
            (gt, ":potential_target_strength", 0),
            (val_div, ":power_ratio", ":potential_target_strength"),
          (else_try),
            (assign, ":power_ratio", 1000),
          (try_end),  
        (else_try),        
          (party_get_slot, ":potential_target_nearby_enemy_strength", ":potential_target", slot_party_nearby_friend_strength),                      
          (assign, ":potential_target_strength", 1000),
                    
          #(store_add, ":army_strength", ":marshal_strength", ":strength_of_potential_followers"),
          (assign, ":army_strength", ":marshal_strength"),
          (val_add, ":army_strength", ":strength_of_current_followers"),
          (store_mul, ":power_ratio", ":army_strength", 100),
                                                            
          (try_begin),
            (gt, ":potential_target_strength", 0),
            (val_div, ":power_ratio", ":potential_target_strength"),
          (else_try),
            (assign, ":power_ratio", 1000),
          (try_end),            
        (try_end),
                            
        (ge, ":power_ratio", 60), #attack if and only if our army is at least 1.2 times powerfull		#NE half this to 60		
        (store_sub, ":power_ratio_sub_120", ":power_ratio", 60),
        
        (try_begin),
          (lt, ":power_ratio_sub_120", 100), #changes between 20..120
          (store_add, ":power_ratio_score", ":power_ratio_sub_120", 20),
        (else_try),
          (lt, ":power_ratio_sub_120", 200), #changes between 120..170
          (store_sub, ":power_ratio_score", ":power_ratio_sub_120", 100),
          (val_div, ":power_ratio_score", 2),
          (val_add, ":power_ratio_score", 120),
        (else_try),
          (lt, ":power_ratio_sub_120", 400), #changes between 170..210
          (store_sub, ":power_ratio_score", ":power_ratio_sub_120", 200),
          (val_div, ":power_ratio_score", 5),
          (val_add, ":power_ratio_score", 170),
        (else_try),
          (lt, ":power_ratio_sub_120", 800), #changes between 210..250
          (store_sub, ":power_ratio_score", ":power_ratio_sub_120", 400),
          (val_div, ":power_ratio_score", 10),
          (val_add, ":power_ratio_score", 210),
        (else_try),
          (assign, ":power_ratio_score", 250),
        (try_end),
          
        (assign, ":number_of_walled_centers", 0),
        (assign, ":total_distance", 0),
        (try_for_range, ":walled_center", walled_centers_begin, walled_centers_end),
          (store_faction_of_party, ":walled_center_faction", ":walled_center"),
          (eq, ":walled_center_faction", ":faction_no"),
                
          (store_distance_to_party_from_party, ":dist", ":walled_center", ":potential_target"),            
          (val_add, ":total_distance", ":dist"),
                
          (val_add, ":number_of_walled_centers", 1),
        (try_end),
                
        (try_begin),
          (gt, ":number_of_walled_centers", 0),
          (store_div, ":average_distance", ":total_distance", ":number_of_walled_centers"),
          #(assign, reg0, ":average_distance"),                    
          #(str_store_faction_name, s7, ":faction_no"),
          #(str_store_party_name, s8, ":potential_target"),
          #(display_message, "@average distance for {s7} for {s8} is {reg0}"),
          
          (try_begin),
            (ge, ":marshal_party", 0),
            (party_is_active, ":marshal_party"),
            (store_distance_to_party_from_party, ":marshal_dist_to_potential_target", ":marshal_party", ":potential_target"),
          (else_try),
            (assign, ":marshal_dist_to_potential_target", 100),
          (try_end),
                      
          (try_begin),  
            #if currently our target is attacking to an enemy center and that center is besieged/raided by one of our parties then 
            #divide marshal_distance for other center's to "2" instead of "3" and add some small more distance to avoid easily 
            #changing mind during siege because of small score differences.
              
            (faction_get_slot, ":current_ai_state", ":faction_no", slot_faction_ai_state),
            (eq, ":current_ai_state", sfai_attacking_center),
            (faction_get_slot, ":current_ai_object", ":faction_no", slot_faction_ai_object),
            
            (ge, ":current_ai_object", 0),
            (neq, ":current_ai_object", ":potential_target"),
              
            (try_begin),
              (ge, ":power_ratio_score", 300), #200 max
              (assign, ":power_ratio_score", 200),
            (else_try),
              (ge, ":power_ratio_score", 100), #100..200
              (val_sub, ":power_ratio_score", 100),
              (val_div, ":power_ratio_score", 2),
              (val_add, ":power_ratio_score", 100),
            (try_end),  
            
            (try_begin),
              (faction_slot_eq, ":faction_no", slot_faction_marshall, ":troop_no"),
              (eq, "$g_do_not_skip_other_than_current_ai_object", 0),
              (assign, ":power_ratio_score", 0), #lets completely forget all other choices if we are already besieging one center.
            (try_end),  
            
            (faction_set_slot, ":faction_no", slot_faction_last_attacked_center, ":current_ai_object"),
            (store_current_hours, ":hours"),
            (faction_set_slot, ":faction_no", slot_faction_last_attacked_hours, ":hours"),

            (eq, ":all_vassals_included", 0),

            (store_div, ":marshal_dist_to_potential_target_div_x", ":marshal_dist_to_potential_target", 2),
            (assign, ":marshal_dist_to_potential_target_div_x", ":marshal_dist_to_potential_target"),
          (else_try),
            (store_div, ":marshal_dist_to_potential_target_div_x", ":marshal_dist_to_potential_target", 3),
          (try_end),
            
          (store_add, ":total_distance", ":average_distance", ":marshal_dist_to_potential_target_div_x"), #in average ":total_distance" is about 150, min : 0, max : 1000
        (else_try),
          (assign, ":total_distance", 100),
        (try_end),                

        (try_begin),
          #according to cautious troop distance is more important

	      (this_or_next|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_upstanding),
	      (this_or_next|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_debauched),
	      (this_or_next|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_goodnatured),
	      (troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_cunning),	      	      

          (try_begin),
            (lt, ":total_distance", 30), #very close (100p)
            (assign, ":distance_score", 100),
          (else_try),
            (lt, ":total_distance", 80), #close (50p-100p)
            (store_sub, ":distance_score", ":total_distance", 30),
            (val_div, ":distance_score", 1),
            (store_sub, ":distance_score", 100, ":distance_score"),
          (else_try),  
            (lt, ":total_distance", 160), #far (10p-50p)
            (store_sub, ":distance_score", ":total_distance", 80),
            (val_div, ":distance_score", 2),
            (store_sub, ":distance_score", 50, ":distance_score"),
          (else_try),
            (assign, ":distance_score", 10), #very far
          (try_end),
        (else_try),  
          #according to agressive troop distance is less important
          
          (try_begin),
            (lt, ":total_distance", 40), #very close (100p)
            (assign, ":distance_score", 100),
          (else_try),
            (lt, ":total_distance", 140), #close (50p-100p)
            (store_sub, ":distance_score", ":total_distance", 40),
            (val_div, ":distance_score", 2),
            (store_sub, ":distance_score", 100, ":distance_score"),
          (else_try),  
            (lt, ":total_distance", 300), #far (10p-50p)
            (store_sub, ":distance_score", ":total_distance", 140),
            (val_div, ":distance_score", 4),
            (store_sub, ":distance_score", 50, ":distance_score"),
          (else_try),
            (assign, ":distance_score", 10), #very far
          (try_end),
        (try_end),
                                                                                           
        (store_mul, ":target_score", ":distance_score", ":power_ratio_score"),
        (val_mul, ":target_score", ":last_offensive_time_score"),
        (val_div, ":target_score", 100), #target score is between 0..10000 generally here

        (call_script, "script_find_total_prosperity_score", ":potential_target"),                
        (assign, ":total_prosperity_score", reg0),
            
        #(try_begin), #new for increase attackability of villages by ai
          #(is_between, ":potential_target", villages_begin, villages_end), 
          (val_mul, ":total_prosperity_score", 3),
          (val_div, ":total_prosperity_score", 2),
        #(try_end),

        (val_mul, ":target_score", ":total_prosperity_score"),
          
        (try_begin), #if both that center was our (original center) and (ex center) than bonus is 1.2x
          (party_slot_eq, ":potential_target", slot_center_ex_faction, ":faction_no"),
          (party_slot_eq, ":potential_target", slot_center_original_faction, ":faction_no"),
          (val_mul, ":target_score", 12),
          (val_div, ":target_score", 10),
        (else_try), #if either that center was our (original center) or (ex center) than bonus is 1.1x
          (this_or_next|party_slot_eq, ":potential_target", slot_center_ex_faction, ":faction_no"),
          (party_slot_eq, ":potential_target", slot_center_original_faction, ":faction_no"),
          (val_mul, ":target_score", 11),
          (val_div, ":target_score", 10),
        (try_end),
            
        (val_div, ":target_score", 1000), #target score is between 0..1000 generally here
        
        (try_begin),
          (eq, ":potential_target_faction", "fac_player_supporters_faction"),
          (game_get_reduce_campaign_ai, ":reduce_campaign_ai"),
          
          (assign, ":number_of_walled_centers_player_have", 0),
          (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
            (store_faction_of_party, ":center_faction", ":center_no"),
            (eq, ":center_faction", "fac_player_supporters_faction"),
            (val_add, ":number_of_walled_centers_player_have", 1),
          (try_end),
          
          (try_begin),
            (eq, ":reduce_campaign_ai", 2), #easy
            
            (try_begin),
              (le, ":number_of_walled_centers_player_have", 2),
              (assign, ":hardness_score", 0),              
            (else_try),
              (eq, ":number_of_walled_centers_player_have", 3),
              (assign, ":hardness_score", 20),
            (else_try),
              (eq, ":number_of_walled_centers_player_have", 4),
              (assign, ":hardness_score", 40),
            (else_try),
              (eq, ":number_of_walled_centers_player_have", 5),
              (eq, ":number_of_walled_centers_player_have", 6),
              (assign, ":hardness_score", 55),
            (else_try),
              (eq, ":number_of_walled_centers_player_have", 7),
              (eq, ":number_of_walled_centers_player_have", 8),
              (eq, ":number_of_walled_centers_player_have", 9),
              (assign, ":hardness_score", 70),
            (else_try),
              (assign, ":hardness_score", 85),
            (try_end),
          (else_try),  
            (eq, ":reduce_campaign_ai", 1), #medium

            (try_begin),
              (le, ":number_of_walled_centers_player_have", 1),
              (assign, ":hardness_score", 25),
            (else_try),
              (eq, ":number_of_walled_centers_player_have", 2),
              (assign, ":hardness_score", 45),
            (else_try),
              (eq, ":number_of_walled_centers_player_have", 3),
              (assign, ":hardness_score", 60),
            (else_try),
              (eq, ":number_of_walled_centers_player_have", 4),
              (eq, ":number_of_walled_centers_player_have", 5),
              (assign, ":hardness_score", 75),
            (else_try),
              (eq, ":number_of_walled_centers_player_have", 6),
              (eq, ":number_of_walled_centers_player_have", 7),
              (eq, ":number_of_walled_centers_player_have", 8),
              (assign, ":hardness_score", 85),
            (else_try),
              (assign, ":hardness_score", 92),
            (try_end),
          (else_try), #hard
            (assign, ":hardness_score", 100), 
          (try_end),
          
          (val_mul, ":target_score", ":hardness_score"),
          (val_div, ":target_score", 100),
        (try_end),

        (try_begin), #NE
          (ge, "$cheat_mode", 1),
          (eq, ":faction_no", "fac_kingdom_4"),
          (ge, ":target_score", -1),
          (assign, reg0, ":target_score"),
          (assign, reg7, ":total_prosperity_score"),
          (assign, reg8, ":power_ratio_score"),
          (assign, reg9, ":distance_score"),
          (assign, reg10, ":last_offensive_time_score"),
          (str_store_party_name, s8, ":potential_target"),
          (eq, ":all_vassals_included", 0),
          (assign, reg11, ":all_vassals_included"),          
          (display_message, "@DEBUG : attack of {s8} is {reg0}({reg11}), prs:{reg7}, pow:{reg8}, dis:{reg9}, lst:{reg10}"),
        (try_end),  
      (try_end),
                                                     
      (assign, reg0, ":target_score"),
      (assign, reg1, ":power_ratio"),
      (assign, reg2, ":distance_score"),
      (assign, reg3, ":total_prosperity_score"),
    ]),
]
