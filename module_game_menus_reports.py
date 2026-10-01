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

game_menus_reports = [
  ("reports",0,
   "Character Renown: {reg5}^Honor Rating: {reg6}^Party Morale: {reg8}^Party Size Limit: {reg7}^",
   "none",
   [(call_script, "script_game_get_party_companion_limit"),
    (assign, ":party_size_limit", reg0),
    (troop_get_slot, ":renown", "trp_player", slot_troop_renown),
    (assign, reg5, ":renown"),
    (assign, reg6, "$player_honor"),
    (assign, reg7, ":party_size_limit"),
    #(call_script, "script_get_player_party_morale_values"),
    #(party_set_morale, "p_main_party", reg0),
    (party_get_morale, reg8, "p_main_party"),
	
	##diplomacy begin
    (str_clear, s1),
    (try_begin),
	    (gt, "$g_next_pay_time", 0),
      (str_store_date, s1, "$g_next_pay_time"),
      (str_store_string, s1, "@ Next pay day: {s1}"),
    (try_end),

    (try_begin),
      (is_between, "$g_player_affiliated_troop", lords_begin, kingdom_ladies_end),
      (str_store_troop_name, s5, "$g_player_affiliated_troop"),
      (str_store_string, s1, "@{s1}^^Affiliated to {s5}"),
    (try_end),
    ##diplomacy end
   ],
    [
	
      ("cheat_faction_orders",[(ge,"$cheat_mode",1)],"{!}Cheat: Faction orders.",
       [(jump_to_menu, "mnu_faction_orders"),
        ]
       ),
       
       ("action_view_upgrade_trees",[],"显 示 各 国 的 兵 种 树",
       [
        (assign, "$temp", 0),
        (start_presentation, "prsnt_faction_upgrade_trees"),
        ]
       ),
	   
#gekokujo world map

      ("action_view_world_map",[],"View the world map.",
       [
        (start_presentation, "prsnt_world_map"),
        ]
       ),
	   
      ("view_character_report",[],"View character report.",
       [(jump_to_menu, "mnu_character_report"),
        ]
       ),
	   
      ("view_party_size_report",[],"View party size report.",
       [(jump_to_menu, "mnu_party_size_report"),
        ]
       ),
	   
      ("view_npc_mission_report",[],"View companion mission report.",
       [(jump_to_menu, "mnu_companion_report"),
        ]
       ),

      ("view_weekly_budget_report",[],"View weekly budget report.",
       [
         (assign, "$g_apply_budget_report_to_gold", 0),
         (start_presentation, "prsnt_budget_report"),
        ]
       ),

      ("view_morale_report",[],"View party morale report.",
       [(jump_to_menu, "mnu_morale_report"),
        ]
       ),

#NPC companion changes begin
##diplomacy start
      ("lord_relations",[],"View list of known lords by relation.",
       [
		#(jump_to_menu, "mnu_lord_relations"),
        (assign, "$g_jrider_pres_called_from_menu", 1),
        (assign, "$g_character_presentation_type", 1),
        (start_presentation, "prsnt_jrider_character_relation_report"),
        ]
       ),
##diplomacy end

	##diplomacy start+ see dplmc_affiliated_family_report
     ("view_affiliated_family_report",[
		#(this_or_next|troop_slot_ge, "trp_player", slot_troop_spouse, 1),
        (this_or_next|ge,"$cheat_mode",1),
		(is_between, "$g_player_affiliated_troop", kingdoms_begin, kingdoms_end),
		], "View affiliated family member / spouse report.",
       [
           (jump_to_menu, "mnu_dplmc_affiliated_family_report"),
        ]
       ),
	##diplomacy end+
	   
      ("courtship_relations",[],"View courtship relations.",
       [
		(jump_to_menu, "mnu_courtship_relations"),
        ]
       ),

      ("status_check",[(eq,"$cheat_mode",1)],"{!}NPC status check.",
       [
		#gekokujo 3.0 microfactions! include fort companions start
        #(try_for_range, ":npc", companions_begin, companions_end),
        (try_for_range, ":npc", companions_begin, fort_companions_end),
		#gekokujo 3.0 microfactions! include fort companions end
            (main_party_has_troop, ":npc"),
            (str_store_troop_name, 4, ":npc"),
            (troop_get_slot, reg3, ":npc", slot_troop_morality_state),
            (troop_get_slot, reg4, ":npc", slot_troop_2ary_morality_state),
            (troop_get_slot, reg5, ":npc", slot_troop_personalityclash_state),    
            (troop_get_slot, reg6, ":npc", slot_troop_personalityclash2_state),    
            (troop_get_slot, reg7, ":npc", slot_troop_personalitymatch_state),    
            (display_message, "@{!}{s4}: M{reg3}, 2M{reg4}, PC{reg5}, 2PC{reg6}, PM{reg7}"),
        (try_end),
        ]
       ),

#NPC companion changes end

##diplomacy begin
      ("view_faction_relations_report",[],"View faction relations report.",
       [
           # Jrider + REPORTS PRESENTATIONS 1.2, comment to hook faction report presentation
           ##(jump_to_menu, "mnu_faction_relations_report"),
           (start_presentation, "prsnt_jrider_faction_relations_report"),
           # Jrider -
        ]
       ),
       
     ("dplmc_show_economic_report",[],"View prosperity report.",
       [
           (jump_to_menu, "mnu_dplmc_economic_report"),
        ]
       ),
       ##diplomacy end
      ("resume_travelling",[],"Resume travelling.",
       [(change_screen_return),
        ]
       ),
	   
      ]
  ),
  ("morale_report",0,
   "{s1}",
   "none",
   [
     (call_script, "script_get_player_party_morale_values"),
     #(party_set_morale, "p_main_party", reg0),

     (assign, ":target_morale", reg0),
     (assign, reg1, "$g_player_party_morale_modifier_party_size"),
     (try_begin),
       (gt, reg1, 0),
       (str_store_string, s2, "@{!} -"),
     (else_try),
       (str_store_string, s2, "str_space"),
     (try_end),

     (assign, reg2, "$g_player_party_morale_modifier_leadership"),
     (try_begin),
       (gt, reg2, 0),
       (str_store_string, s3, "@{!} +"),
     (else_try),
       (str_store_string, s3, "str_space"),
     (try_end),

     (try_begin),
       (gt, "$g_player_party_morale_modifier_no_food", 0),
       (assign, reg7, "$g_player_party_morale_modifier_no_food"),
       (str_store_string, s5, "@^No food:  -{reg7}"),
     (else_try),
       (str_store_string, s5, "str_space"),
     (try_end),
     (assign, reg3, "$g_player_party_morale_modifier_food"),
     (try_begin),
       (gt, reg3, 0),
       (str_store_string, s4, "@{!} +"),
     (else_try),
       (str_store_string, s4, "str_space"),
     (try_end),
 
     (try_begin),
       (gt, "$g_player_party_morale_modifier_debt", 0),
       (assign, reg6, "$g_player_party_morale_modifier_debt"),
       (str_store_string, s6, "@^Wage debt:  -{reg6}"),
     (else_try),
       (str_store_string, s6, "str_space"),
     (try_end),
 
     (party_get_morale, reg5, "p_main_party"),
     (store_sub, reg4, reg5, ":target_morale"),
     (try_begin),
       (gt, reg4, 0),
       (str_store_string, s7, "@{!} +"),
     (else_try),
       (str_store_string, s7, "str_space"),
     (try_end),
     
     (assign, reg6, 50),
     
     (str_store_string, s1, "str_current_party_morale_is_reg5_current_party_morale_modifiers_are__base_morale__50_party_size_s2reg1_leadership_s3reg2_food_variety_s4reg3s5s6_recent_events_s7reg4_total__reg5___"),
        
     (try_for_range, ":kingdom_no", npc_kingdoms_begin, npc_kingdoms_end),
       (faction_get_slot, ":faction_morale", ":kingdom_no",  slot_faction_morale_of_player_troops),
       (val_div, ":faction_morale", 100),
       (neq, ":faction_morale", 0),
       (assign, reg6, ":faction_morale"),
       (str_store_faction_name, s9, ":kingdom_no"),
       (str_store_string, s1, "str_s1extra_morale_for_s9_troops__reg6_"),
     (try_end),        
    ],
    [
      ("continue",[],"Continue...",
      [
        (jump_to_menu, "mnu_reports"),
      ]),
    ]
  ),
  ("courtship_relations",0,
   "{s1}",
   "none",
   [(str_store_string, s1, "str_courtships_in_progress_"),
    (try_for_range, ":lady", kingdom_ladies_begin, kingdom_ladies_end),
		(troop_slot_eq, ":lady", slot_troop_met, 2),
		(call_script, "script_troop_get_relation_with_troop", "trp_player", ":lady"),
		(gt, reg0, 0),
		(assign, reg3, reg0),
		
		(str_store_troop_name, s2, ":lady"),
		
		(store_current_hours, ":hours_since_last_visit"),
		(troop_get_slot, ":last_visit_hour", ":lady", slot_troop_last_talk_time),
		(val_sub, ":hours_since_last_visit", ":last_visit_hour"),
		(store_div, ":days_since_last_visit", ":hours_since_last_visit", 24),
		(assign, reg4, ":days_since_last_visit"),
		
		(str_store_string, s1, "str_s1_s2_relation_reg3_last_visit_reg4_days_ago"),
	(try_end),
	
	(str_store_string, s1, "str_s1__poems_known"),
	(try_begin),
		 (gt, "$allegoric_poem_recitations", 0),
		 (str_store_string, s1, "str_s1_storming_the_castle_of_love_allegoric"),
	(try_end),
	(try_begin),
		 (gt, "$tragic_poem_recitations", 0),
		 (str_store_string, s1, "str_s1_kais_and_layali_tragic"),
	(try_end),
	(try_begin),
		 (gt, "$comic_poem_recitations", 0),
		 (str_store_string, s1, "str_s1_a_conversation_in_the_garden_comic"),
	(try_end),
	(try_begin),
		 (gt, "$heroic_poem_recitations", 0),
		 (str_store_string, s1, "str_s1_helgered_and_kara_epic"),
	(try_end),
	(try_begin),
		 (gt, "$mystic_poem_recitations", 0),
		 (str_store_string, s1, "str_s1_a_hearts_desire_mystic"),
	(try_end),
	
    ],
    [
      ("continue",[],"Continue...",
       [(jump_to_menu, "mnu_reports"),
        ]
       ),
      ]
  ),
  ("lord_relations",0,
   "{s1}",
   "none",
   [   
    ##diplomacy start+
	#Avoid unnecessary iterations, since below we only use slto_kingdom_hero troops.
    (assign, ":met_lord_count", 0),
    #Add support for promoted kingdom ladies.
    #(try_for_range, ":active_npc", active_npcs_begin, active_npcs_end),
    (try_for_range, ":active_npc", heroes_begin, heroes_end),
      (troop_slot_eq, ":active_npc", slot_troop_occupation, slto_kingdom_hero),
      (troop_slot_ge, ":active_npc", slot_troop_met, 1),
      (val_add, ":met_lord_count", 1),
    ##diplomacy end+
		(troop_set_slot, ":active_npc", slot_troop_temp_slot, 0),
	(try_end),
	
	(str_clear, s1),
    ##diplomacy start+
    #Add support for promoted kingdom ladies.
    #(try_for_range, ":unused", active_npcs_begin, active_npcs_end),#<- changed
    #We counted the number of heroes, so we can cut down on the number of
    #iterations (since expanding this from active_npcs to heroes means that
    #a lot of them will not be lords).
    (try_for_range, ":unused", 0, ":met_lord_count"),#<- added
		(assign, ":score_to_beat", -100),
		(assign, ":best_relation_remaining_npc", -1),
		#Add support for promoted kingdom ladies
		#(try_for_range, ":active_npc", active_npcs_begin, active_npcs_end),#<-changed
		(try_for_range, ":active_npc", heroes_begin, heroes_end),#<-added
	##diplomacy end+
			(troop_slot_eq, ":active_npc", slot_troop_temp_slot, 0),
			(troop_slot_eq, ":active_npc", slot_troop_occupation, slto_kingdom_hero),
			(troop_slot_ge, ":active_npc", slot_troop_met, 1),
	
			(call_script, "script_troop_get_player_relation", ":active_npc"),
			(assign, ":relation_with_player", reg0),
			(ge, ":relation_with_player", ":score_to_beat"),
			
			(assign, ":score_to_beat", ":relation_with_player"),
			(assign, ":best_relation_remaining_npc", ":active_npc"),
		(try_end),
		(gt, ":best_relation_remaining_npc", -1),
		
		(str_store_troop_name_link, s4, ":best_relation_remaining_npc"),
		(assign, reg4, ":score_to_beat"),
		(str_store_string, s1, "@{!}{s1}^{s4}: {reg4}"),
		(troop_set_slot, ":best_relation_remaining_npc", slot_troop_temp_slot, 1),
	(try_end),
   
	
    ],
    [
      ("continue",[],"Continue...",
       [(jump_to_menu, "mnu_reports"),
        ]
       ),
      ]
  ),
  
  ("companion_report",0,
   "{s7}{s1}",
   "none",
   [
   (str_clear, s1),
   (str_store_string, s7, "str_no_companions_in_service"),
   
   (try_begin),
	(troop_get_slot, ":spouse_or_betrothed", "trp_player", slot_troop_spouse),
	(try_begin),
		##diplomacy start+ Test gender with script
		#(troop_get_type, ":is_female", "trp_player"),#<- replaced
		(call_script, "script_cf_dplmc_troop_is_female", "trp_player"),
		#(eq, ":is_female", 1),#<- replaced
		##diplomacy end+
		(str_store_string, s8, "str_husband"),
	(else_try),
		(str_store_string, s8, "str_wife"),
	(try_end),
	
	(try_begin),
		(le, ":spouse_or_betrothed", 0),
		(troop_get_slot, ":spouse_or_betrothed", "trp_player", slot_troop_betrothed),
		(str_store_string, s8, "str_betrothed"),
	(try_end),	
	(gt, ":spouse_or_betrothed", 0),	
		
	(str_store_troop_name, s4, ":spouse_or_betrothed"),
	(troop_get_slot, ":cur_center", ":spouse_or_betrothed", slot_troop_cur_center),
	(try_begin),
		(is_between, ":cur_center", centers_begin, centers_end),
		(str_store_party_name, s5, ":cur_center"),
	(else_try),
		(troop_slot_eq, ":spouse_or_betrothed", slot_troop_occupation, slto_kingdom_hero),
		(str_store_string, s5, "str_leading_party"),
	(else_try),	
		(str_store_string, s5, "str_whereabouts_unknown"),
    (try_end),
	(str_store_string, s3, "str_s4_s8_s5"),
	(str_store_string, s2, s1),
	(str_store_string, s1, "str_s2_s3"),
	
   (try_end),
   
   
   (try_begin),
    (ge, "$cheat_mode", 1),
	(ge, "$npc_to_rejoin_party", 0),
    (str_store_troop_name, s5, "$npc_to_rejoin_party"),
	(str_store_string, s1, "@{!}DEBUG -- {s1}^NPC in rejoin queue: {s5}^"),
   (try_end),
   
   
   #gekokujo 3.0 microfactions! include fort companions start
   #(try_for_range, ":companion", companions_begin, companions_end),
   (try_for_range, ":companion", companions_begin, fort_companions_end),
   #gekokujo 3.0 microfactions! include fort companions end
		(str_clear, s2),
		(str_clear, s3),

		(try_begin),
			(troop_get_slot, ":days_left", ":companion", slot_troop_days_on_mission),

			(troop_slot_eq, ":companion", slot_troop_occupation, slto_player_companion),

				
			(str_store_troop_name, s4, ":companion"),

			(try_begin),
				(troop_slot_eq, ":companion", slot_troop_current_mission, npc_mission_kingsupport),
				(str_store_string, s8, "str_gathering_support"),
				(try_begin),
					(eq, ":days_left", 1),
					(str_store_string, s5, "str_expected_back_imminently"),
				(else_try),	
					(assign, reg3, ":days_left"),
					(str_store_string, s5, "str_expected_back_in_approximately_reg3_days"),
				(try_end),
			(else_try),
				(troop_slot_eq, ":companion", slot_troop_current_mission, npc_mission_gather_intel),
				(troop_get_slot, ":town_with_contacts", ":companion", slot_troop_town_with_contacts),
				(str_store_party_name, s11, ":town_with_contacts"),
				
				(str_store_string, s8, "str_gathering_intelligence"),
				(try_begin),
					(eq, ":days_left", 1),
					(str_store_string, s5, "str_expected_back_imminently"),
				(else_try),	
					(assign, reg3, ":days_left"),
					(str_store_string, s5, "str_expected_back_in_approximately_reg3_days"),
				(try_end),
			(else_try),	#This covers most diplomatic missions
				
				(troop_slot_ge, ":companion", slot_troop_current_mission, npc_mission_peace_request),
				##diplomacy begin
				(neg|troop_slot_eq, ":companion", slot_troop_current_mission, 8),
				##diplomacy end

				(troop_get_slot, ":faction", ":companion", slot_troop_mission_object),
				(str_store_faction_name, s9, ":faction"),
				(str_store_string, s8, "str_diplomatic_embassy_to_s9"),
				(try_begin),
					(eq, ":days_left", 1),
					(str_store_string, s5, "str_expected_back_imminently"),
				(else_try),	
					(assign, reg3, ":days_left"),
					(str_store_string, s5, "str_expected_back_in_approximately_reg3_days"),
				(try_end),
			(else_try),
				(eq, ":companion", "$g_player_minister"),
				(str_store_string, s8, "str_serving_as_minister"),
				(try_begin),
					(is_between, "$g_player_court", centers_begin, centers_end),
					(str_store_party_name, s9, "$g_player_court"),
					(str_store_string, s5, "str_in_your_court_at_s9"),
				(else_try),	
					(str_store_string, s5, "str_whereabouts_unknown"),
				(try_end),	
			(else_try),
				(main_party_has_troop, ":companion"),
				(str_store_string, s8, "str_under_arms"),
				(str_store_string, s5, "str_in_your_party"),
			(else_try),	
				(troop_slot_eq, ":companion", slot_troop_current_mission, npc_mission_rejoin_when_possible),
				(str_store_string, s8, "str_attempting_to_rejoin_party"),
				(str_store_string, s5, "str_whereabouts_unknown"),
			(else_try),	#Companions who are in a center
				(troop_slot_ge, ":companion", slot_troop_cur_center, 1),

				(str_store_string, s8, "str_separated_from_party"),
				(str_store_string, s5, "str_whereabouts_unknown"),
#gekokujo 3.0 integrating 1.158 start
#			(else_try), #Excludes companions who have occupation = retirement
#			
#				(troop_set_slot, ":companion", slot_troop_current_mission, npc_mission_rejoin_when_possible),
#			
#				(str_store_string, s8, "str_attempting_to_rejoin_party"),
#				(str_store_string, s5, "str_whereabouts_unknown"),
	        (else_try), #Excludes companions who have occupation = retirement
                (try_begin),
                  (check_quest_active, "qst_lend_companion"),
                  (quest_slot_eq, "qst_lend_companion", slot_quest_target_troop, ":companion"),
                  (str_store_string, s8, "@On loan,"), 
                (else_try),
                  (check_quest_active, "qst_lend_surgeon"),
                  (quest_slot_eq, "qst_lend_surgeon", slot_quest_target_troop, ":companion"),
                  (str_store_string, s8, "@On loan,"), 
                (else_try),
				  (troop_set_slot, ":companion", slot_troop_current_mission, npc_mission_rejoin_when_possible),
                  (str_store_string, s8, "str_attempting_to_rejoin_party"),                  
                (try_end),
                
	        	(str_store_string, s5, "str_whereabouts_unknown"),
#gekokujo 3.0 integrating 1.158 end
				
				(try_begin),
					(ge, "$cheat_mode", 1),
					(troop_get_slot, reg2, ":companion", slot_troop_current_mission),
					(troop_get_slot, reg3, ":companion", slot_troop_days_on_mission),
					(troop_get_slot, reg4, ":companion", slot_troop_prisoner_of_party),
					(troop_get_slot, reg5, ":companion", slot_troop_playerparty_history),
					
					(display_message, "@{!}DEBUG: {s4} current mission: {reg2}, days on mission: {reg3}, prisoner: {reg4}, pphistory: {reg5}"),
				(try_end),
			(try_end),	
			
			(str_store_string, s3, "str_s4_s8_s5"),
				
			(str_store_string, s2, s1),
			(str_store_string, s1, "str_s2_s3"),

			(str_clear, s7), #"no companions in service"
		(else_try),
			(neg|troop_slot_eq, ":companion", slot_troop_occupation, slto_kingdom_hero),
			(troop_slot_ge, ":companion", slot_troop_prisoner_of_party, centers_begin),

			(str_store_troop_name, s4, ":companion"),
			(str_store_string, s8, "str_missing_after_battle"),
			(str_store_string, s5, "str_whereabouts_unknown"),
			
			(str_store_string, s3, "str_s4_s8_s5"),
			(str_store_string, s2, s1),
			(str_store_string, s1, "str_s2_s3"),			
			(str_clear, s7), #"no companions in service"
			
		(try_end),
		
   (try_end),
   

    ],
    [
      ("continue",[],"Continue...",[
	    (jump_to_menu, "mnu_reports"),
      ]),
    ]
  ),
  
  
  
  
  
  ("faction_orders",0,
   "{!}{s9}",
   "none",
   [
    (str_clear, s9),
    (store_current_hours, ":cur_hours"),
    (try_for_range, ":faction_no", kingdoms_begin, kingdoms_end),
        (faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
        (neq, ":faction_no", "fac_player_supporters_faction"),
       
        (faction_get_slot, ":old_faction_ai_state", ":faction_no", slot_faction_ai_state),
       
	    (try_begin),
			(faction_get_slot, ":faction_marshal", ":faction_no", slot_faction_marshall),
			(gt, ":faction_marshal", -1),
			(assign, ":faction_ai_decider", ":faction_marshal"),
	    (else_try),
			(faction_get_slot, ":faction_ai_decider", ":faction_no", slot_faction_leader),
	    (try_end),
	 

        #(*1) these two lines moved to here from (*2)
        (call_script, "script_npc_decision_checklist_faction_ai_alt", ":faction_ai_decider"),
	    (assign, ":new_strategy", reg0),
	    (str_store_string, s26, s14),
	   
        #(3*) these three lines moved to here from (*4)
        (faction_get_slot, ":faction_ai_state", ":faction_no", slot_faction_ai_state),
        (faction_get_slot, ":faction_ai_object", ":faction_no", slot_faction_ai_object),
        (faction_get_slot, ":faction_marshall", ":faction_no", slot_faction_marshall),

        (faction_get_slot, ":faction_ai_offensive_max_followers", ":faction_no", slot_faction_ai_offensive_max_followers),
        (str_store_faction_name, s10, ":faction_no"),
	   
	   (try_begin),
			(faction_get_slot, ":faction_issue", ":faction_no", slot_faction_political_issue),
		   
			(try_begin),
				(eq, ":faction_issue", 1),
				(str_store_string, s11, "@Appoint next strategist"),
			(else_try),
				(is_between, ":faction_issue", centers_begin, centers_end),
				(str_store_party_name, s12, ":faction_issue"),
				(str_store_string, s11, "@Award {s12} as fief"),
			(else_try),	
				(eq, ":faction_issue", 0),
				(str_store_string, s11, "@None"),
			(else_try),	
				(assign, reg3, ":faction_issue"),
				(str_store_string, s11, "@{!}Error ({reg3})"),
			(try_end),
			
			(store_current_hours, reg4),
			(faction_get_slot, ":faction_issue_put_on_agenda", ":faction_no", slot_faction_political_issue_time),
			(val_sub, reg4, ":faction_issue_put_on_agenda"),

	        (str_store_string, s10, "@{!}{s10}^Faction political issue: {s11}"),
			(try_begin),
				(faction_slot_ge, ":faction_no", slot_faction_political_issue, 1),
				(str_store_string, s10, "@{!}{s10} (on agenda {reg4} hours)"),
			(try_end),	
	   (try_end),	   
	   
	   
       (assign, reg2, ":faction_ai_offensive_max_followers"),
       (try_begin),
         (eq, ":faction_ai_state", sfai_default),
         (str_store_string, s11, "@{!}Defending"),
       (else_try),
         (eq, ":faction_ai_state", sfai_gathering_army),
         (str_store_string, s11, "@{!}Gathering army"),
       (else_try),
         (eq, ":faction_ai_state", sfai_attacking_center),
         (str_store_party_name, s11, ":faction_ai_object"),
         (str_store_string, s11, "@{!}Besieging {s11}"),
       (else_try),
         (eq, ":faction_ai_state", sfai_raiding_village),
         (str_store_party_name, s11, ":faction_ai_object"),
         (str_store_string, s11, "@{!}Raiding {s11}"),
       (else_try),
         (eq, ":faction_ai_state", sfai_attacking_enemy_army),
         (str_store_party_name, s11, ":faction_ai_object"),
         (str_store_string, s11, "str_attacking_enemy_army_near_s11"),
       (else_try),
         (eq, ":faction_ai_state", sfai_feast),
         (str_store_party_name, s11, ":faction_ai_object"),
         (str_store_string, s11, "str_holding_feast_at_s11"),
	   (else_try), 
         (eq, ":faction_ai_state", sfai_attacking_enemies_around_center),
         (str_store_party_name, s11, ":faction_ai_object"),
         (str_store_string, s11, "@{!}Attacking enemies around {s11}"),
       (else_try),
	     (assign, reg4, ":faction_ai_state"),
		 (str_store_string, s11, "str_sfai_reg4"),
	   (try_end),

       (try_begin),
         (lt, ":faction_marshall", 0),
         (str_store_string, s12, "@No one"),
       (else_try),
         (str_store_troop_name, s12, ":faction_marshall"),
		 (troop_get_slot, reg21, ":faction_marshall", slot_troop_controversy),
		 (str_store_string, s12, "@{!}{s12} (controversy: {reg21})"),
       (try_end),

	   (try_for_parties, ":screen_party"),
			(party_slot_eq, ":screen_party", slot_party_ai_state, spai_screening_army),
			(store_faction_of_party, ":screen_party_faction", ":screen_party"),
			(eq, ":screen_party_faction", ":faction_no"),
			
			(str_store_party_name, s38, ":screen_party"),
			(str_store_string, s12, "@{!}{s12}^Screening party: {s38}"),
	   (try_end),
	   
       #(*2) these two lines moved to up (look *1)
	   #(call_script, "script_npc_decision_checklist_faction_ai", ":faction_no"),
	   #(assign, ":new_strategy", reg0),

       #(try_begin),
       #  (this_or_next|eq, ":new_strategy", sfai_default),
       #  (eq, ":new_strategy", sfai_feast),
	   #		
	   #  (store_current_hours, ":hours"),
	   #  (faction_set_slot, ":faction_no", slot_faction_ai_last_rest_time, ":hours"),		
	   #(try_end),
      (try_begin),      
         #new condition to rest, (a faction's new strategy should be feast or default) and (":hours_at_current_state" > 20)
         (this_or_next|eq, ":new_strategy", sfai_default),
         (eq, ":new_strategy", sfai_feast),                            
              
         (store_current_hours, ":hours_at_current_state"),
         (faction_get_slot, ":current_state_started", ":faction_no", slot_faction_ai_current_state_started), 
         (val_sub, ":hours_at_current_state", ":current_state_started"),
         (ge, ":hours_at_current_state", 18),
              
         (store_current_hours, ":hours"),       
         (faction_set_slot, ":faction_no", slot_faction_ai_last_rest_time, ":hours"),		
       (try_end),     

        #Change of strategy
        (try_begin),
          (neq, ":new_strategy", ":old_faction_ai_state"),
				
          (store_current_hours, ":hours"),
          (faction_set_slot, ":faction_no", slot_faction_ai_current_state_started, ":hours"),
        (try_end),

	   (call_script, "script_evaluate_realm_stability", ":faction_no"),
	   (assign, ":disgruntled_lords", reg0),
	   (assign, ":restless_lords", reg1),
	   
	   (faction_get_slot, ":last_feast_ended", ":faction_no", slot_faction_last_feast_start_time),
	   (store_sub, ":hours_since_last_feast", ":cur_hours", ":last_feast_ended"),
	   (val_sub, ":hours_since_last_feast", 72),

	   (faction_get_slot, ":current_state_started", ":faction_no", slot_faction_ai_current_state_started),
	   (store_sub, ":hours_at_current_state", ":cur_hours", ":current_state_started"),

       (faction_get_slot, ":faction_ai_last_offensive_time", ":faction_no", slot_faction_last_offensive_concluded),
       (store_sub, ":hours_since_last_offensive", ":cur_hours", ":faction_ai_last_offensive_time"),

       (faction_get_slot, ":faction_ai_last_rest", ":faction_no", slot_faction_ai_last_rest_time),
       (store_sub, ":hours_since_last_rest", ":cur_hours", ":faction_ai_last_rest"),

       (faction_get_slot, ":faction_ai_last_decisive_event", ":faction_no", slot_faction_ai_last_decisive_event),
       (store_sub, ":hours_since_last_decisive_event", ":cur_hours", ":faction_ai_last_decisive_event"),
	   
	   (assign, reg3, ":hours_at_current_state"),
	   (assign, reg4, ":hours_since_last_offensive"),
	   (assign, reg5, ":hours_since_last_feast"),
	   
	   (assign, reg7, ":disgruntled_lords"),
	   (assign, reg8, ":restless_lords"),
	   (assign, reg9, ":hours_since_last_rest"),
	   (assign, reg10, ":hours_since_last_decisive_event"),
	   (str_store_string, s14, s26),
	   
       (str_store_string, s9, "str_s9s10_current_state_s11_hours_at_current_state_reg3_current_strategic_thinking_s14_marshall_s12_since_the_last_offensive_ended_reg4_hours_since_the_decisive_event_reg10_hours_since_the_last_rest_reg9_hours_since_the_last_feast_ended_reg5_hours_percent_disgruntled_lords_reg7_percent_restless_lords_reg8__"),	   
     (try_end),
	 	 	 
     (try_begin),
       (neg|is_between, "$g_cheat_selected_faction", kingdoms_begin, kingdoms_end),
       (call_script, "script_get_next_active_kingdom", kingdoms_end),
       (assign, "$g_cheat_selected_faction", reg0),
     (try_end),
     (str_store_faction_name, s10, "$g_cheat_selected_faction"),
     (str_store_string, s9, "@Selected faction is: {s10}^^{s9}"),
    ],
    [
      ("faction_orders_next_faction", [],"{!}Select next faction.",
       [
         (call_script, "script_get_next_active_kingdom", "$g_cheat_selected_faction"),
         (assign, "$g_cheat_selected_faction", reg0),
         (jump_to_menu, "mnu_faction_orders"),
        ]
       ),
	   
      ("faction_orders_political_collapse", [],"{!}CHEAT - Cause all lords in faction to fall out with their liege.",
       [
	   (try_for_range, ":lord", active_npcs_begin, active_npcs_end),
			(troop_slot_eq, ":lord", slot_troop_occupation, slto_kingdom_hero),
			(store_faction_of_troop, ":troop_faction", ":lord"),
			(eq, ":troop_faction", "$g_cheat_selected_faction"),
			(faction_get_slot, ":faction_liege", ":troop_faction", slot_faction_leader),
			(call_script, "script_troop_change_relation_with_troop", ":lord", ":faction_liege", -200),
	   (try_end),
	   
	   ]
       ),
	   
      ("faction_orders_defend", [],"{!}Force defend.",
       [
         (faction_set_slot, "$g_cheat_selected_faction", slot_faction_ai_state, sfai_default),
         (faction_set_slot, "$g_cheat_selected_faction", slot_faction_ai_object, -1),
         (jump_to_menu, "mnu_faction_orders"),
        ]
       ),
      ("faction_orders_feast", [],"{!}Force feast.",
       [

		 (assign, ":location_high_score", 0),
		 (try_for_range, ":location", walled_centers_begin, walled_centers_end),
			(neg|party_slot_ge, ":location", slot_center_is_besieged_by, 1),
			(store_faction_of_party, ":location_faction", ":location"),
			(eq, ":location_faction", "$g_cheat_selected_faction"),
			(party_get_slot, ":location_lord", ":location", slot_town_lord),
			(troop_get_slot, ":location_score", ":location_lord", slot_troop_renown),
			(store_random_in_range, ":random", 0, 1000), #will probably be king or senior lord
			(val_add, ":location_score", ":random"),
			(gt, ":location_score", ":location_high_score"),
			(assign, ":location_high_score", ":location_score"),
			(assign, ":location_feast", ":location"),
		 (try_end),		 

		 (try_begin),
			(gt, ":location_feast", centers_begin),
			(faction_set_slot, "$g_cheat_selected_faction", slot_faction_ai_state, sfai_feast),
			(faction_set_slot, "$g_cheat_selected_faction", slot_faction_ai_object, ":location_feast"),
			(try_begin),
			  (eq, "$g_player_eligible_feast_center_no", ":location_feast"),
			  (assign, "$g_player_eligible_feast_center_no", -1),
			(try_end),
		 
			(store_current_hours, ":hours"),
			(faction_set_slot, "$g_cheat_selected_faction", slot_faction_last_feast_start_time, ":hours"),
		 (try_end),
			
	     (jump_to_menu, "mnu_faction_orders"),
        ]
       ),
	   
	   
      ("faction_orders_gather", [],"{!}Force gather army.",
       [
         (store_current_hours, ":cur_hours"),
         (faction_set_slot, "$g_cheat_selected_faction", slot_faction_ai_state, sfai_gathering_army),
         (faction_set_slot, "$g_cheat_selected_faction", slot_faction_last_offensive_concluded, ":cur_hours"),
         (faction_set_slot, "$g_cheat_selected_faction", slot_faction_ai_offensive_max_followers, 1),
         (faction_set_slot, "$g_cheat_selected_faction", slot_faction_ai_object, -1),
         (jump_to_menu, "mnu_faction_orders"),
        ]
       ),
      ("faction_orders_increase_time", [],"{!}Increase last offensive time by 24 hours.",
       [
         (faction_get_slot, ":faction_ai_last_offensive_time", "$g_cheat_selected_faction", slot_faction_last_offensive_concluded),
         (val_sub, ":faction_ai_last_offensive_time", 24),
         (faction_set_slot, "$g_cheat_selected_faction", slot_faction_last_offensive_concluded, ":faction_ai_last_offensive_time"),
         (jump_to_menu, "mnu_faction_orders"),
        ]
       ),
      ("faction_orders_rethink", [],"{!}Force rethink.",
       [
         (call_script, "script_init_ai_calculation"),
         (call_script, "script_decide_faction_ai", "$g_cheat_selected_faction"),
         (jump_to_menu, "mnu_faction_orders"),
        ]
       ),
      ("faction_orders_rethink_all", [],"{!}Force rethink for all factions.",
       [
         (call_script, "script_recalculate_ais"),
         (jump_to_menu, "mnu_faction_orders"),
        ]
       ),

	   ("enable_alt_ai",[(eq, "$g_use_alternative_ai", 2),],"{!}CHEAT! - enable alternative ai",
       [
	   (assign, "$g_use_alternative_ai", 1),
	   (jump_to_menu, "mnu_faction_orders"),
       ]
       ),	   

	   ("disable_alt_ai",[(eq, "$g_use_alternative_ai", 2)],"{!}CHEAT! - disable alternative ai",
       [
	   (assign, "$g_use_alternative_ai", 0),
	   (jump_to_menu, "mnu_faction_orders"),
       ]
       ),	   
	   
      ("faction_orders_init_econ", [],"{!}Initialize economic stats.",
       [
         (call_script, "script_initialize_economic_information"),
         (jump_to_menu, "mnu_faction_orders"),
        ]
       ),
	   
      ("go_back_dot",[],"{!}Go back.",
       [(jump_to_menu, "mnu_reports"),
        ]
       ),
      ]
  ),
  ("character_report",0,
   "{s9}",
   "none",
   [(try_begin),
      (gt, "$g_player_reading_book", 0),
      (player_has_item, "$g_player_reading_book"),
      (str_store_item_name, s8, "$g_player_reading_book"),
      (str_store_string, s9, "@You are currently reading {s8}."),
    (else_try),
      (assign, "$g_player_reading_book", 0),
      (str_store_string, s9, "@You are not reading any books."),
    (try_end),
    (assign, ":num_friends", 0),
    (assign, ":num_enemies", 0),
    (str_store_string, s6, "@none"),
    (str_store_string, s8, "@none"),
    (try_for_range, ":troop_no", active_npcs_begin, active_npcs_end),
	  (this_or_next|troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
		(troop_slot_eq, ":troop_no", slot_troop_occupation, slto_inactive_pretender),
	  (call_script, "script_troop_get_player_relation", ":troop_no"),
      (assign, ":player_relation", reg0),
      #(troop_get_slot, ":player_relation", ":troop_no", slot_troop_player_relation),
      (try_begin),
        (gt, ":player_relation", 20),
        (try_begin),
          (eq, ":num_friends", 0),
          (str_store_troop_name, s8, ":troop_no"),
        (else_try),
          (eq, ":num_friends", 1),
          (str_store_troop_name, s7, ":troop_no"),
          (str_store_string, s8, "@{s7} and {s8}"),
        (else_try),
          (str_store_troop_name, s7, ":troop_no"),
          (str_store_string, s8, "@{!}{s7}, {s8}"),
        (try_end),
        (val_add, ":num_friends", 1),
      (else_try),
        (lt, ":player_relation", -20),
        (try_begin),
          (eq, ":num_enemies", 0),
          (str_store_troop_name, s6, ":troop_no"),
        (else_try),
          (eq, ":num_enemies", 1),
          (str_store_troop_name, s5, ":troop_no"),
          (str_store_string, s6, "@{s5} and {s6}"),
        (else_try),
          (str_store_troop_name, s5, ":troop_no"),
          (str_store_string, s6, "@{!}{s5}, {s6}"),
        (try_end),
        (val_add, ":num_enemies", 1),
      (try_end),
    (try_end),
	
	#lord recruitment changes begin
	(str_clear, s12),
	(try_begin),
		(gt, "$player_right_to_rule", 0),
		(assign, reg12, "$player_right_to_rule"),
		(str_store_string, s12, "str__right_to_rule_reg12"),
	(try_end),
	
	(str_clear, s15),
	(try_begin),
		(this_or_next|gt, "$claim_arguments_made", 0),
		(this_or_next|gt, "$ruler_arguments_made", 0),
		(this_or_next|gt, "$victory_arguments_made", 0),
		(this_or_next|gt, "$lords_arguments_made", 0),
		(eq, 1, 0),
		
		(assign, reg3, "$claim_arguments_made"),
		(assign, reg4, "$ruler_arguments_made"),
		(assign, reg5, "$victory_arguments_made"),
		(assign, reg6, "$lords_arguments_made"),
		(assign, reg7, "$benefit_arguments_made"),

		(str_store_string, s15, "str_political_arguments_made_legality_reg3_rights_of_lords_reg4_unificationpeace_reg5_rights_of_commons_reg6_fief_pledges_reg7"),
	(try_end),
	
	#lord recruitment changes begin
	
    (assign, reg3, "$player_honor"),
    (troop_get_slot, reg2, "trp_player", slot_troop_renown),

    (str_store_string, s9, "str_renown_reg2_honour_rating_reg3s12_friends_s8_enemies_s6_s9"),
	
    (call_script, "script_get_number_of_hero_centers", "trp_player"),
    (assign, ":no_centers", reg0),
    (try_begin),
      (gt, ":no_centers", 0),
      (try_for_range, ":i_center", 0, ":no_centers"),
        (call_script, "script_troop_get_leaded_center_with_index", "trp_player", ":i_center"),
        (assign, ":cur_center", reg0),
        (try_begin),
          (eq, ":i_center", 0),
          (str_store_party_name, s8, ":cur_center"),
        (else_try),
          (eq, ":i_center", 1),
          (str_store_party_name, s7, ":cur_center"),
          (str_store_string, s8, "@{s7} and {s8}"),
        (else_try),
          (str_store_party_name, s7, ":cur_center"),
          (str_store_string, s8, "@{!}{s7}, {s8}"),
        (try_end),
      (try_end),
      (str_store_string, s9, "@Your estates are: {s8}.^{s9}"),
    (try_end),
    (try_begin),
      (gt, "$players_kingdom", 0),
              
      (str_store_faction_name, s8, "$players_kingdom"),
      (try_begin),
	  ##diplomacy start+ Handle player is co-ruler of NPC faction
		(is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
		(call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", "$players_kingdom"),
		(ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
		(str_store_string, s9, "str_you_are_king_queen_of_s8_s9"),
	  (else_try),
	  ##diplomacy end+
        (this_or_next|is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
        (neg|faction_slot_eq, "fac_player_supporters_faction", slot_faction_leader, "trp_player"),
        #(str_store_string, s9, "@You are a lord of {s8}.^{s9}"),
        (str_store_string, s9, "str_you_are_a_lord_lady_of_s8_s9"),
      (else_try),  
        (str_store_string, s9, "str_you_are_king_queen_of_s8_s9"),      
      (try_end),
      
    (try_end),
    ],
    [

	#lord recruitment changes begin

	("continue",[(eq,"$cheat_mode",1)],"{!}CHEAT! - increase Right to Rule",
       [
	   (val_add, "$player_right_to_rule", 10),
	   (jump_to_menu, "mnu_character_report"),
       ]
       ),


	("continue",[(eq,"$cheat_mode",1),
		(str_store_troop_name, s14, "$g_talk_troop"),
	],"{!}CHEAT! - increase your relation with {s14}",
       [
	   (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 10),
	   (jump_to_menu, "mnu_character_report"),
       ]
       ),

	   
	("continue",[(eq,"$cheat_mode",1)],"{!}CHEAT! - increase honor",
       [
	   (val_add, "$player_honor", 10),
	   (jump_to_menu, "mnu_character_report"),
       ]
       ),

	("continue",[(eq,"$cheat_mode",1)],"{!}CHEAT! - increase renown",
       [
	   (troop_get_slot, ":renown", "trp_player", slot_troop_renown),
	   (val_add, ":renown", 50),
	   (troop_set_slot, "trp_player", slot_troop_renown, ":renown"),
	   
	   (jump_to_menu, "mnu_character_report"),
       ]
       ),

	("continue",[(eq,"$cheat_mode",1)],"{!}CHEAT! - increase persuasion",
       [
	   (troop_raise_skill, "trp_player", "skl_persuasion", 1),
	   
	   (jump_to_menu, "mnu_character_report"),
       ]
       ),
	   


	("continue",[],"Continue...",
       [(jump_to_menu, "mnu_reports"),
        ]
       ),

	#lord recruitment changes end

	   ]
  ),
  ("party_size_report",0,
   "{s1}",
   "none",
   [(call_script, "script_game_get_party_companion_limit"),
    (assign, ":party_size_limit", reg0),

    (store_skill_level, ":leadership", "skl_leadership", "trp_player"),
    (val_mul, ":leadership", 5),
    (store_attribute_level, ":charisma", "trp_player", ca_charisma),

    (troop_get_slot, ":renown", "trp_player", slot_troop_renown),
	#gekokujo 3.0 increased renown bonus to party size
    #(val_div, ":renown", 25),
	(val_div, ":renown", 10),
	
    (try_begin),
      (gt, ":leadership", 0),
      (str_store_string, s2, "@{!} +"),
    (else_try),
      (str_store_string, s2, "str_space"),
    (try_end),
    (try_begin),
      (gt, ":charisma", 0),
      (str_store_string, s3, "@{!} +"),
    (else_try),
      (str_store_string, s3, "str_space"),
    (try_end),
    (try_begin),
      (gt, ":renown", 0),
      (str_store_string, s4, "@{!} +"),
    (else_try),
      (str_store_string, s4, "str_space"),
    (try_end),
    (assign, reg5, ":party_size_limit"),
    (assign, reg1, ":leadership"),
    (assign, reg2, ":charisma"),
    (assign, reg3, ":renown"),
	
	#gekokujo 3.0 correct party size reporting start
	(str_store_string, s5, "str_space"),
	(store_faction_of_party, ":faction_id", "trp_player"),
	
	(assign, ":num_walled_fiefs", 0),
	(try_for_range, ":cur_center", walled_centers_begin, walled_centers_end),
	  (party_slot_eq, ":cur_center", slot_town_lord, "trp_player"),
	  (val_add, ":num_walled_fiefs", 1),
	(try_end),
	
	#gekokujo 3.1 samurai party penalty start
	#correct reporting in the party report screen
	(try_begin),
	  (eq, "$g_gekokujo_samurai_penalty", 1),
	  (assign, ":samurai_penalty", 0),
	  (party_get_num_companion_stacks, ":num_stacks", "p_main_party"),
	  (try_for_range, ":i_stack", 0, ":num_stacks"),
	    (party_stack_get_troop_id, ":stack_troop", "p_main_party", ":i_stack"),
		(is_between, ":stack_troop", samurai_troops_begin, samurai_troops_end),
		(party_stack_get_size, ":stack_size", "p_main_party", ":i_stack"),
		(val_add, ":samurai_penalty", ":stack_size"),
	  (try_end),
	  (try_begin),
	    (gt, ":samurai_penalty", 0),
		(assign, reg5, ":samurai_penalty"),
		(str_store_string, s5, "@^Samurai Penalty: -{reg5} (from off-screen servants){s5}"),
	  (try_end),
	(try_end),
	#gekokujo 3.1 samurai party penalty end
	
	(try_begin),
	  (is_between, ":faction_id", kingdoms_begin, kingdoms_end),
	  (faction_slot_eq, ":faction_id", slot_faction_state, sfs_active),
	  (faction_slot_eq, ":faction_id", slot_faction_marshall, "trp_player"),
	  (str_store_string, s5, "@^Clan Strategist: +20{s5}"),
    (try_end),
	
	(try_begin),
	  (is_between, ":faction_id", kingdoms_begin, kingdoms_end),
	  (faction_slot_eq, ":faction_id", slot_faction_state, sfs_active),
	  (faction_slot_eq, ":faction_id", slot_faction_leader, "trp_player"),
	  (str_store_string, s5, "@^Clan Leader: +20{s5}"),
    (try_end),
	
	(try_begin),
	  (gt, ":num_walled_fiefs", 0),
	  (store_mul, reg5, ":num_walled_fiefs", 10),
	  (try_begin),
	    (eq, ":num_walled_fiefs", 1),
	    (str_store_string, s5, "@^Walled Fief: +{reg5}{s5}"),
	  (else_try),
	    (str_store_string, s5, "@^Walled Fiefs: +{reg5}{s5}"),
	  (try_end),
	(try_end),
	#gekokujo 3.0 correct party size reporting end
	
	#gekokujo 3.0 prisoner limit report start
	#we'll piggyback here so that the report menu isn't overburdened
	(call_script, "script_game_get_party_prisoner_limit"),
	(assign, ":prisoner_limit", reg0),

	(store_skill_level, ":skill", "skl_prisoner_management", "trp_player"),
	(val_mul, ":skill", 5),
	
	(call_script, "script_party_count_fit_regulars", "p_main_party"),
	(assign, ":size", reg0),
	(val_div, ":size", 10),
	
    (try_begin),
      (gt, ":skill", 0),
      (str_store_string, s6, "@{!} +"),
    (else_try),
      (str_store_string, s6, "str_space"),
    (try_end),
	
    (try_begin),
      (gt, ":size", 0),
      (str_store_string, s7, "@{!} +"),
    (else_try),
      (str_store_string, s7, "str_space"),
    (try_end),
	
    (assign, reg8, ":prisoner_limit"),
    (assign, reg6, ":skill"),
    (assign, reg7, ":size"),
	
    (str_store_string, s8, "@Current prisoner limit is {reg8}.^^\
							Prisoner Management: {s6}{reg6}^\
							Party Size Modifier: {s7}{reg7}"),
	#gekokujo 3.0 prisoner limit report end
    
    #gekokujo 3.1 bodyguard limit report start
    #i don't know why i never added this
    (store_skill_level, ":leadership", skl_leadership, "trp_player"),
    (troop_get_slot, ":renown", "trp_player", slot_troop_renown),
    (val_div, ":leadership", 3),
    (val_div, ":renown", 400),
    (store_add, ":max_guards", ":renown", ":leadership"),
    (val_min, ":max_guards", 4),
    
    (try_begin),
      (eq, ":max_guards", 0),
      (assign, ":agent_guards", 2),
    (else_try),
      (eq, ":max_guards", 1),
      (assign, ":agent_guards", 1),
    (try_end),
    
    (assign, reg10, ":max_guards"),
    (assign, reg11, ":agent_guards"),    
    (store_add, reg9, ":max_guards", ":agent_guards"),
    
    (str_store_string, s9, "@Current bodyguard limit is {reg9}.^^\
							Companions or Agents: {reg10}^\
							Agents Only: {reg11}"),
    #gekokujo 3.1 bodyguard limit report end
	
    (str_store_string, s1, "@Current party size limit is {reg5}.^^\
							Base size:  +20^\
							Leadership: {s2}{reg1}^\
							Charisma: {s3}{reg2}^\
							Renown: {s4}{reg3}{s5}^^^{s8}^^^{s9}"),
    ],
    [
      ("continue",[],"Continue...",
       [(jump_to_menu, "mnu_reports"),
        ]
       ),
      ]
  ),
  
  ("faction_relations_report",0,
   "{s1}",
   "none",
   [(str_clear, s2),
    (try_for_range, ":cur_kingdom", kingdoms_begin, kingdoms_end),
      (faction_slot_eq, ":cur_kingdom", slot_faction_state, sfs_active),
      (neq, ":cur_kingdom", "fac_player_supporters_faction"),
      (store_relation, ":cur_relation", "fac_player_supporters_faction", ":cur_kingdom"),
      (try_begin),
        (ge, ":cur_relation", 90),
        (str_store_string, s3, "@Loyal"),
      (else_try),
        (ge, ":cur_relation", 80),
        (str_store_string, s3, "@Devoted"),
      (else_try),
        (ge, ":cur_relation", 70),
        (str_store_string, s3, "@Fond"),
      (else_try),
        (ge, ":cur_relation", 60),
        (str_store_string, s3, "@Gracious"),
      (else_try),
        (ge, ":cur_relation", 50),
        (str_store_string, s3, "@Friendly"),
      (else_try),
        (ge, ":cur_relation", 40),
        (str_store_string, s3, "@Supportive"),
      (else_try),
        (ge, ":cur_relation", 30),
        (str_store_string, s3, "@Favorable"),
      (else_try),
        (ge, ":cur_relation", 20),
        (str_store_string, s3, "@Cooperative"),
      (else_try),
        (ge, ":cur_relation", 10),
        (str_store_string, s3, "@Accepting"),
      (else_try),
        (ge, ":cur_relation", 0),
        (str_store_string, s3, "@Indifferent"),
      (else_try),
        (ge, ":cur_relation", -10),
        (str_store_string, s3, "@Suspicious"),
      (else_try),
        (ge, ":cur_relation", -20),
        (str_store_string, s3, "@Grumbling"),
      (else_try),
        (ge, ":cur_relation", -30),
        (str_store_string, s3, "@Hostile"),
      (else_try),
        (ge, ":cur_relation", -40),
        (str_store_string, s3, "@Resentful"),
      (else_try),
        (ge, ":cur_relation", -50),
        (str_store_string, s3, "@Angry"),
      (else_try),
        (ge, ":cur_relation", -60),
        (str_store_string, s3, "@Hateful"),
      (else_try),
        (ge, ":cur_relation", -70),
        (str_store_string, s3, "@Revengeful"),
      (else_try),
        (str_store_string, s3, "@Vengeful"),
      (try_end),
      (str_store_faction_name, s4, ":cur_kingdom"),
      (assign, reg1, ":cur_relation"),
      (str_store_string, s2, "@{!}{s2}^{s4}: {reg1} ({s3})"),
    (try_end),
    (str_store_string, s1, "@Your relation with the factions are:^{s2}"),

	

    ],
    [
      ("continue",[],"Continue...",
       [(jump_to_menu, "mnu_reports"),
        ]
       ),
      ]
  ),
  ##diplomacy end
##diplomacy start+
  ("dplmc_affiliated_family_report",0,
   "{s0}",
   "none",
   [
    (str_clear, s0),
	(str_clear, s1),
	(try_for_range, ":troop_no", active_npcs_including_player_begin, heroes_end),
		(try_begin),
			(eq, ":troop_no", active_npcs_including_player_begin),
			(assign, ":troop_no", "trp_player"),
		(try_end),
		(call_script, "script_dplmc_store_troop_is_eligible_for_affiliate_messages", ":troop_no"),
		(this_or_next|eq, ":troop_no", "trp_player"),
           (ge, reg0, 1),

		(str_clear, s1),
		(str_store_string, s0, "str_dplmc_s0_newline_s1"),#add blank line to start

		#show name; (non-player) also show location
		(try_begin),
			(eq, ":troop_no", "trp_player"),
			(str_store_string, s1, "@{playername}"),
		(else_try),
			(call_script, "script_get_information_about_troops_position", ":troop_no", 0),#s1 = String, reg0 = knows-or-not
		(try_end),
		(str_store_string, s0, "str_dplmc_s0_newline_s1"),#add line

		#(non-player) show relation
		(try_begin),
			(neq, "trp_player", ":troop_no"),
			(call_script, "script_troop_get_player_relation", ":troop_no"),
			(assign, reg1, reg0) ,
			(str_store_string, s1, "str_relation_reg1"),
			(str_store_string, s0, "str_dplmc_s0_newline_s1"),#add line
		(try_end),

		#(non-prisoner) show party size
		(try_begin),
            (neg|troop_slot_ge, ":troop_no", slot_troop_prisoner_of_party, 0),
			(troop_get_slot, ":led_party", ":troop_no", slot_troop_leaded_party),
            (this_or_next|eq, ":led_party", 0),
			   (ge, ":led_party", spawn_points_end),
			(this_or_next|eq, ":troop_no", "trp_player"),
			   (neq, ":led_party", "p_main_party"),
			(party_is_active, ":led_party"),
			(assign, reg0, 0),
			(party_get_num_companions, reg1, ":led_party"),#number of troops
            (str_store_string, s1, "@Troops: {reg1}"),
			(str_store_string, s0, "str_dplmc_s0_newline_s1"),#add line
		(try_end),

	(try_end),
    ],
    [
	  ("lord_relations",[],"View list of all known lords by relation.",
       [
		(jump_to_menu, "mnu_lord_relations"),
        ]
       ),
      ("continue",[],"Continue...",
       [(jump_to_menu, "mnu_reports"),
        ]
       ),
      ]
  ),
  
  ##Economic report, currently just for debugging purposes
  ("dplmc_economic_report",0,
   "{s0}",
   "none",
   [
    (str_clear, s0),
    (str_clear, s1),
    (assign, reg0, 0),
    (str_store_string, s0, "@Prosperity Report^"),

    #Show average prosperity for each faction
    (try_for_range, ":faction", 0, kingdoms_end),
       (this_or_next|eq, ":faction", 0),
       (is_between, ":faction", kingdoms_begin, kingdoms_end),

       (this_or_next|eq, ":faction", 0),
       (faction_slot_eq, ":faction", slot_faction_state, sfs_active),
       
       (try_begin),
          (eq, ":faction", 0),
          (str_store_string, s1, "@Total"),
       (else_try),
          (faction_get_slot, reg0, ":faction", slot_faction_adjective),
          (gt, reg0, 0),
          (str_store_string, s1, reg0),
       (else_try),
          (str_store_faction_name, s1, ":faction"),
       (try_end),

       ##(1) Faction Prosperity, towns
       (assign, ":sum", 0),
       (assign, ":q_5", 0),
       (assign, ":q_4", 0),
       (assign, ":q_3", 0),
       (assign, ":q_2", 0),
       (assign, ":q_1", 0),
       (assign, ":num", 0),
       
       (try_for_range, ":center_no", towns_begin, towns_end),
          (store_faction_of_party, reg0, ":center_no"),
          (this_or_next|eq, ":faction", 0),
          (eq, reg0, ":faction"),
          (val_add, ":num", 1),
          (party_get_slot, reg0, ":center_no", slot_town_prosperity),
          (val_add, ":sum", reg0),
          (try_begin),
             (lt, reg0, 20),
             (val_add, ":q_1", 1),
          (else_try),
             (lt, reg0, 40),
             (val_add, ":q_2", 1),
          (else_try),
             (lt, reg0, 60),
             (val_add, ":q_3", 1),
          (else_try),
             (lt, reg0, 80),
             (val_add, ":q_4", 1),
          (else_try),
             (val_add, ":q_5", 1),
          (try_end),
       (try_end),
       
       (assign, reg0, ":num"),
       (val_max, reg0, 1),
       (store_div, reg0, ":sum", reg0),
       (str_store_string, s0, "@{s0}^{s1} Average Town Prosperity: {reg0}"),
       (assign, reg0, ":q_5"),
       (try_begin),
          (this_or_next|eq, ":faction", 0),
          (gt, reg0, 0),
          (str_store_string, s0, "@{s0}^{s1} towns with prosperity 80-100: {reg0}"),
       (try_end),
       (assign, reg0, ":q_4"),
       (try_begin),
          (this_or_next|eq, ":faction", 0),
          (gt, reg0, 0),
          (str_store_string, s0, "@{s0}^{s1} towns with prosperity 60-79: {reg0}"),
       (try_end),
       (assign, reg0, ":q_3"),
       (try_begin),
          (this_or_next|eq, ":faction", 0),
          (gt, reg0, 0),
          (str_store_string, s0, "@{s0}^{s1} towns with prosperity 40-59: {reg0}"),
       (try_end),
       (assign, reg0, ":q_2"),
       (try_begin),
          (this_or_next|eq, ":faction", 0),
          (gt, reg0, 0),
          (str_store_string, s0, "@{s0}^{s1} towns with prosperity 20-39: {reg0}"),
       (try_end),
       (assign, reg0, ":q_1"),
       (try_begin),
          (this_or_next|eq, ":faction", 0),
          (gt, reg0, 0),
          (str_store_string, s0, "@{s0}^{s1} towns with prosperity 0-19: {reg0}"),
       (try_end),
       
       (str_store_string, s0, "@{!}{s0}^"),

       ##(2) Faction Prosperity, villages
       (assign, ":sum", 0),
       (assign, ":q_5", 0),
       (assign, ":q_4", 0),
       (assign, ":q_3", 0),
       (assign, ":q_2", 0),
       (assign, ":q_1", 0),
       (assign, ":num", 0),
       
       (try_for_range, ":center_no", villages_begin, villages_end),
          (store_faction_of_party, reg0, ":center_no"),
          (this_or_next|eq, ":faction", 0),
          (eq, reg0, ":faction"),
          (val_add, ":num", 1),
          (party_get_slot, reg0, ":center_no", slot_town_prosperity),
          (val_add, ":sum", reg0),
          (try_begin),
             (lt, reg0, 20),
             (val_add, ":q_1", 1),
          (else_try),
             (lt, reg0, 40),
             (val_add, ":q_2", 1),
          (else_try),
             (lt, reg0, 60),
             (val_add, ":q_3", 1),
          (else_try),
             (lt, reg0, 80),
             (val_add, ":q_4", 1),
          (else_try),
             (val_add, ":q_5", 1),
          (try_end),
       (try_end),
       
       (assign, reg0, ":num"),
       (val_max, reg0, 1),
       (store_div, reg0, ":sum", reg0),
       (str_store_string, s0, "@{s0}^{s1} Average Village Prosperity: {reg0}"),
       (try_begin),
          (this_or_next|eq, ":faction", 0),
          (gt, ":q_5", 0),
          (assign, reg0, ":q_5"),
          (str_store_string, s0, "@{s0}^{s1} villages with prosperity 80-100: {reg0}"),
       (try_end),
       (try_begin),
          (this_or_next|eq, ":faction", 0),
          (gt, ":q_4", 0),
          (assign, reg0, ":q_4"),
          (str_store_string, s0, "@{s0}^{s1} villages with prosperity 60-79: {reg0}"),
       (try_end),
       (try_begin),
          (this_or_next|eq, ":faction", 0),
          (gt, ":q_3", 0),
          (assign, reg0, ":q_3"),
          (str_store_string, s0, "@{s0}^{s1} villages with prosperity 40-59: {reg0}"),
       (try_end),
       (try_begin),
          (this_or_next|eq, ":faction", 0),
          (gt, ":q_2", 0),
          (assign, reg0, ":q_2"),
          (str_store_string, s0, "@{s0}^{s1} villages with prosperity 20-39: {reg0}"),
       (try_end),
       (try_begin),
          (this_or_next|eq, ":faction", 0),
          (gt, ":q_1", 0),
          (assign, reg0, ":q_1"),
          (str_store_string, s0, "@{s0}^{s1} villages with prosperity 0-19: {reg0}"),
       (try_end),
       (str_store_string, s0, "@{!}{s0}^"),
    (try_end),
    ],
    [
      ("dplmc_back",[],"Continue...",
       [
           (jump_to_menu, "mnu_reports"),
        ]),
      ]
  ),
]
