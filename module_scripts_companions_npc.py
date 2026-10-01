# -*- coding: utf-8 -*-
# module_scripts_companions_npc.py -- auto split from module_scripts.py (feature: 同伴 NPC/俘虏/赎金)
# entries: 27 (order preserved within this file)
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


scripts_companions_npc = [

  ("npc_get_troop_wage",
    [
      (store_script_param_1, ":troop_id"),
      (assign,":wage", 0),
      (try_begin),
        (troop_is_hero, ":troop_id"),
      (else_try),
        (store_character_level, ":wage", ":troop_id"),
        (val_mul, ":wage", ":wage"),
        (val_add, ":wage", 50),
        (val_div, ":wage", 30),
        (troop_is_mounted, ":troop_id"),
        (val_mul, ":wage", 5),
        (val_div, ":wage", 4),
      (try_end),
      (assign, reg0, ":wage"),
  ]),
  #script_update_ransom_brokers
  # INPUT: none
  # OUTPUT: none
  ("update_ransom_brokers",
    [(try_for_range, ":town_no", towns_begin, towns_end),
       (party_set_slot, ":town_no", slot_center_ransom_broker, 0),
     (try_end),
     
     (try_for_range, ":troop_no", ransom_brokers_begin, ransom_brokers_end),
       (store_random_in_range, ":town_no", towns_begin, towns_end),
       (party_set_slot, ":town_no", slot_center_ransom_broker, ":troop_no"),
     (try_end),

     (party_set_slot,"p_town_2",slot_center_ransom_broker,"trp_ramun_the_slave_trader"),
     ]),
#NPC companion changes begin
  ("initialize_npcs",
    [

# set strings

        (troop_set_slot, "trp_npc1", slot_troop_morality_type, tmt_egalitarian),  #Kojiro
        (troop_set_slot, "trp_npc1", slot_troop_morality_value, 4),  #Kojiro
        (troop_set_slot, "trp_npc1", slot_troop_2ary_morality_type, tmt_aristocratic),  #Kojiro
        (troop_set_slot, "trp_npc1", slot_troop_2ary_morality_value, -1),
        (troop_set_slot, "trp_npc1", slot_troop_personalityclash_object, "trp_npc7"),  #Kojiro - Musashi
        (troop_set_slot, "trp_npc1", slot_troop_personalityclash2_object, "trp_npc16"),  #Kojiro - Hyogonosuke
        (troop_set_slot, "trp_npc1", slot_troop_personalitymatch_object, "trp_npc2"),  #Kojiro - Youmu
        (troop_set_slot, "trp_npc1", slot_troop_home, "p_village_25"), #Kasai
        (troop_set_slot, "trp_npc1", slot_troop_payment_request, 300), 
		(troop_set_slot, "trp_npc1", slot_troop_kingsupport_argument, argument_benefit),
		(troop_set_slot, "trp_npc1", slot_troop_kingsupport_opponent, "trp_npc14"), #Sessai
		(troop_set_slot, "trp_npc1", slot_troop_town_with_contacts, "p_town_17"), #Kubota
		(troop_set_slot, "trp_npc1", slot_troop_original_faction, 0),
		(troop_set_slot, "trp_npc1", slot_lord_reputation_type, lrep_roguish),
		
		
		
        (troop_set_slot, "trp_npc2", slot_troop_morality_type, tmt_humanitarian), #Youmu
        (troop_set_slot, "trp_npc2", slot_troop_morality_value, 2),  
        (troop_set_slot, "trp_npc2", slot_troop_2ary_morality_type, tmt_honest),  
        (troop_set_slot, "trp_npc2", slot_troop_2ary_morality_value, 1),
        (troop_set_slot, "trp_npc2", slot_troop_personalityclash_object, "trp_npc5"), #Youmu - Meiling
        (troop_set_slot, "trp_npc2", slot_troop_personalityclash2_object, "trp_npc9"), #Youmu - Moko
        (troop_set_slot, "trp_npc2", slot_troop_personalitymatch_object, "trp_npc1"),  #Youmu - Kojiro
        (troop_set_slot, "trp_npc2", slot_troop_home, "p_town_1"), #Edo
        (troop_set_slot, "trp_npc2", slot_troop_payment_request, 0), 
		(troop_set_slot, "trp_npc2", slot_troop_kingsupport_argument, argument_lords),
		(troop_set_slot, "trp_npc2", slot_troop_kingsupport_opponent, "trp_npc16"), #Hyogonosuke
		(troop_set_slot, "trp_npc2", slot_troop_town_with_contacts, "p_town_1"), #Edo
		(troop_set_slot, "trp_npc2", slot_troop_original_faction, 0), 
		(troop_set_slot, "trp_npc2", slot_lord_reputation_type, lrep_martial), 

#
        (troop_set_slot, "trp_npc3", slot_troop_morality_type, tmt_humanitarian), #William
        (troop_set_slot, "trp_npc3", slot_troop_morality_value, 4),  
        (troop_set_slot, "trp_npc3", slot_troop_2ary_morality_type, tmt_aristocratic), 
        (troop_set_slot, "trp_npc3", slot_troop_2ary_morality_value, -1),
        (troop_set_slot, "trp_npc3", slot_troop_personalityclash_object, "trp_npc14"), #William - Sessai
        (troop_set_slot, "trp_npc3", slot_troop_personalityclash2_object, "trp_npc8"), #William - Francisco
        (troop_set_slot, "trp_npc3", slot_troop_personalitymatch_object, "trp_npc9"), #William - Moko
        (troop_set_slot, "trp_npc3", slot_troop_home, "p_village_5"), #Miura
        (troop_set_slot, "trp_npc3", slot_troop_payment_request, 0), 
		(troop_set_slot, "trp_npc3", slot_troop_kingsupport_argument, argument_none),
		(troop_set_slot, "trp_npc3", slot_troop_kingsupport_opponent, "trp_npc5"), #Meiling
		(troop_set_slot, "trp_npc3", slot_troop_town_with_contacts, "p_town_15"), #Sendai
		(troop_set_slot, "trp_npc3", slot_troop_original_faction, 0), 
		(troop_set_slot, "trp_npc3", slot_lord_reputation_type, lrep_benefactor), 

		
		
        (troop_set_slot, "trp_npc4", slot_troop_morality_type, tmt_aristocratic), #Gonnosuke
        (troop_set_slot, "trp_npc4", slot_troop_morality_value, 4),  
        (troop_set_slot, "trp_npc4", slot_troop_2ary_morality_type, tmt_honest), 
        (troop_set_slot, "trp_npc4", slot_troop_2ary_morality_value, -1),
        (troop_set_slot, "trp_npc4", slot_troop_personalityclash_object, "trp_npc10"), #Gonnosuke - Goemon
        (troop_set_slot, "trp_npc4", slot_troop_personalityclash2_object, "trp_npc7"), #Gonnosuke - Musashi
        (troop_set_slot, "trp_npc4", slot_troop_personalitymatch_object, "trp_npc5"), #Gonnosuke - Meiling
        (troop_set_slot, "trp_npc4", slot_troop_home, "p_village_34"), #Hakui
        (troop_set_slot, "trp_npc4", slot_troop_payment_request, 300), 
		(troop_set_slot, "trp_npc4", slot_troop_kingsupport_argument, argument_claim),
		(troop_set_slot, "trp_npc4", slot_troop_kingsupport_opponent, "trp_npc6"), #Tojiko
		(troop_set_slot, "trp_npc4", slot_troop_town_with_contacts, "p_town_3"), #Choshi
		(troop_set_slot, "trp_npc4", slot_troop_original_faction, 0), 
		(troop_set_slot, "trp_npc4", slot_lord_reputation_type, lrep_quarrelsome), 

		
        (troop_set_slot, "trp_npc5", slot_troop_morality_type, tmt_egalitarian),  #Meiling
        (troop_set_slot, "trp_npc5", slot_troop_morality_value, 3),  #Meiling
        (troop_set_slot, "trp_npc5", slot_troop_2ary_morality_type, -1),
        (troop_set_slot, "trp_npc5", slot_troop_2ary_morality_value, 0),
        (troop_set_slot, "trp_npc5", slot_troop_personalityclash_object, "trp_npc2"),  #Meiling - Youmu
        (troop_set_slot, "trp_npc5", slot_troop_personalityclash2_object, "trp_npc11"),  #Meiling- Mari
        (troop_set_slot, "trp_npc5", slot_troop_personalitymatch_object, "trp_npc4"),  #Meiling - Gonnosuke
        (troop_set_slot, "trp_npc5", slot_troop_home, "p_town_14"), #Okayama
        (troop_set_slot, "trp_npc5", slot_troop_payment_request, 400),
		(troop_set_slot, "trp_npc5", slot_troop_kingsupport_argument, argument_none),
		(troop_set_slot, "trp_npc5", slot_troop_kingsupport_opponent, "trp_npc9"), #Nagako
		(troop_set_slot, "trp_npc5", slot_troop_town_with_contacts, "p_town_10"), #Niigata
		(troop_set_slot, "trp_npc5", slot_troop_original_faction, 0), 
		(troop_set_slot, "trp_npc5", slot_lord_reputation_type, lrep_custodian), 

		
		
        (troop_set_slot, "trp_npc6", slot_troop_morality_type, tmt_humanitarian), #Tojiko
        (troop_set_slot, "trp_npc6", slot_troop_morality_value, 2),  #Tojiko
        (troop_set_slot, "trp_npc6", slot_troop_2ary_morality_type, tmt_honest),
        (troop_set_slot, "trp_npc6", slot_troop_2ary_morality_value, 1),
        (troop_set_slot, "trp_npc6", slot_troop_personalityclash_object, "trp_npc11"), #Tojiko - Mari
        (troop_set_slot, "trp_npc6", slot_troop_personalityclash2_object, "trp_npc13"), #Tojiko - Teruyo
        (troop_set_slot, "trp_npc6", slot_troop_personalitymatch_object, "trp_npc12"),  #Tojiko - Hoshi
        (troop_set_slot, "trp_npc6", slot_troop_home, "p_town_4"), #Kyoto
        (troop_set_slot, "trp_npc6", slot_troop_payment_request, 0),
		(troop_set_slot, "trp_npc6", slot_troop_kingsupport_argument, argument_ruler),
		(troop_set_slot, "trp_npc6", slot_troop_kingsupport_opponent, "trp_npc8"), #Francisco
		(troop_set_slot, "trp_npc6", slot_troop_town_with_contacts, "p_town_7"), #Himeji
		(troop_set_slot, "trp_npc6", slot_troop_original_faction, 0),
		(troop_set_slot, "trp_npc6", slot_lord_reputation_type, lrep_upstanding),

		
		
        (troop_set_slot, "trp_npc7", slot_troop_morality_type, tmt_egalitarian),  #Musashi
        (troop_set_slot, "trp_npc7", slot_troop_morality_value, 3),  #Musashi
        (troop_set_slot, "trp_npc7", slot_troop_2ary_morality_type, -1),
        (troop_set_slot, "trp_npc7", slot_troop_2ary_morality_value, 0),
        (troop_set_slot, "trp_npc7", slot_troop_personalityclash_object, "trp_npc1"),  #Musashi - Kojiro
        (troop_set_slot, "trp_npc7", slot_troop_personalityclash2_object, "trp_npc4"),  #Musashi - Gonnosuke
        (troop_set_slot, "trp_npc7", slot_troop_personalitymatch_object, "trp_npc16"),  #Musashi - Hyogonosuke
        (troop_set_slot, "trp_npc7", slot_troop_home, "p_town_3"), #Choshi
#        (troop_set_slot, "trp_npc7", slot_troop_payment_request, 300),
        (troop_set_slot, "trp_npc7", slot_troop_payment_request, 0),
		(troop_set_slot, "trp_npc7", slot_troop_kingsupport_argument, argument_lords),
		(troop_set_slot, "trp_npc7", slot_troop_kingsupport_opponent, "trp_npc3"), #William
		(troop_set_slot, "trp_npc7", slot_troop_town_with_contacts, "p_town_2"), #Mito
		(troop_set_slot, "trp_npc7", slot_troop_original_faction, 0),
		(troop_set_slot, "trp_npc7", slot_lord_reputation_type, lrep_martial),

		
		
        (troop_set_slot, "trp_npc8", slot_troop_morality_type, tmt_aristocratic), #Francisco
        (troop_set_slot, "trp_npc8", slot_troop_morality_value, 3),  #Francisco
        (troop_set_slot, "trp_npc8", slot_troop_2ary_morality_type, -1),
        (troop_set_slot, "trp_npc8", slot_troop_2ary_morality_value, 0),
        (troop_set_slot, "trp_npc8", slot_troop_personalityclash_object, "trp_npc12"), #Francisco - Hoshi
        (troop_set_slot, "trp_npc8", slot_troop_personalityclash2_object, "trp_npc3"), #Francisco - William
        (troop_set_slot, "trp_npc8", slot_troop_personalitymatch_object, "trp_npc13"),  #Francisco - Teruyo
        (troop_set_slot, "trp_npc8", slot_troop_home, "p_village_37"), #Masumida
        (troop_set_slot, "trp_npc8", slot_troop_payment_request, 500),
		(troop_set_slot, "trp_npc8", slot_troop_kingsupport_argument, argument_none),
		(troop_set_slot, "trp_npc8", slot_troop_kingsupport_opponent, "trp_npc2"), #Youmu
		(troop_set_slot, "trp_npc8", slot_troop_town_with_contacts, "p_town_12"), #Kasugayama
		(troop_set_slot, "trp_npc8", slot_troop_original_faction, 0),
		(troop_set_slot, "trp_npc8", slot_lord_reputation_type, lrep_benefactor),

		
        (troop_set_slot, "trp_npc9", slot_troop_morality_type, tmt_aristocratic), #Nagako
        (troop_set_slot, "trp_npc9", slot_troop_morality_value, 2),  #Nagako
        (troop_set_slot, "trp_npc9", slot_troop_2ary_morality_type, tmt_honest),
        (troop_set_slot, "trp_npc9", slot_troop_2ary_morality_value, 1),
        (troop_set_slot, "trp_npc9", slot_troop_personalityclash_object, "trp_npc13"), #Nagako - Teruyo
        (troop_set_slot, "trp_npc9", slot_troop_personalityclash2_object, "trp_npc2"), #Nagako - Youmu
        (troop_set_slot, "trp_npc9", slot_troop_personalitymatch_object, "trp_npc3"),  #Nagako - William
        (troop_set_slot, "trp_npc9", slot_troop_home, "p_town_13"), #Hiroshima
        (troop_set_slot, "trp_npc9", slot_troop_payment_request, 300),
		(troop_set_slot, "trp_npc9", slot_troop_kingsupport_argument, argument_ruler),
		(troop_set_slot, "trp_npc9", slot_troop_kingsupport_opponent, "trp_npc1"), #Kojiro
		(troop_set_slot, "trp_npc9", slot_troop_town_with_contacts, "p_town_8"), #Kanazawa
		(troop_set_slot, "trp_npc9", slot_troop_original_faction, 0),
		(troop_set_slot, "trp_npc9", slot_lord_reputation_type, lrep_martial),

		
        (troop_set_slot, "trp_npc10", slot_troop_morality_type, tmt_humanitarian), #Goemon
        (troop_set_slot, "trp_npc10", slot_troop_morality_value, 2),
        (troop_set_slot, "trp_npc10", slot_troop_2ary_morality_type, tmt_egalitarian),
        (troop_set_slot, "trp_npc10", slot_troop_2ary_morality_value, 1),
        (troop_set_slot, "trp_npc10", slot_troop_personalityclash_object, "trp_npc4"), #Goemon vs Gonnosuke
        (troop_set_slot, "trp_npc10", slot_troop_personalityclash2_object, "trp_npc14"), #Goemon vs Sessai
        (troop_set_slot, "trp_npc10", slot_troop_personalitymatch_object, "trp_npc11"),  #Goemon likes Mari
        (troop_set_slot, "trp_npc10", slot_troop_home, "p_castle_28"), #Tsuyama Castle
        (troop_set_slot, "trp_npc10", slot_troop_payment_request, 200),
		(troop_set_slot, "trp_npc10", slot_troop_kingsupport_argument, argument_ruler),
		(troop_set_slot, "trp_npc10", slot_troop_kingsupport_opponent, "trp_npc7"), #Musashi
		(troop_set_slot, "trp_npc10", slot_troop_town_with_contacts, "p_town_5"), #Sakai
		(troop_set_slot, "trp_npc10", slot_troop_original_faction, 0),
		(troop_set_slot, "trp_npc10", slot_lord_reputation_type, lrep_benefactor),

		
		
        (troop_set_slot, "trp_npc11", slot_troop_morality_type, tmt_egalitarian),  #Mari
        (troop_set_slot, "trp_npc11", slot_troop_morality_value, 3),
        (troop_set_slot, "trp_npc11", slot_troop_2ary_morality_type, -1),
        (troop_set_slot, "trp_npc11", slot_troop_2ary_morality_value, 0),
        (troop_set_slot, "trp_npc11", slot_troop_personalityclash_object, "trp_npc6"),  #Mari - Tojiko
        (troop_set_slot, "trp_npc11", slot_troop_personalityclash2_object, "trp_npc5"),  #Mari - Meiling
        (troop_set_slot, "trp_npc11", slot_troop_personalitymatch_object, "trp_npc10"),  #Mari - Goemon
        (troop_set_slot, "trp_npc11", slot_troop_home, "p_village_23"), #Uji
        (troop_set_slot, "trp_npc11", slot_troop_payment_request, 100),
		(troop_set_slot, "trp_npc11", slot_troop_kingsupport_argument, argument_ruler),
		(troop_set_slot, "trp_npc11", slot_troop_kingsupport_opponent, "trp_npc15"), #Yoshio
		(troop_set_slot, "trp_npc11", slot_troop_town_with_contacts, "p_town_6"), #Tsu
		(troop_set_slot, "trp_npc11", slot_troop_original_faction, 0), 
		(troop_set_slot, "trp_npc11", slot_lord_reputation_type, lrep_custodian), 
		

        (troop_set_slot, "trp_npc12", slot_troop_morality_type, tmt_humanitarian), #Hoshi
        (troop_set_slot, "trp_npc12", slot_troop_morality_value, 3),
        (troop_set_slot, "trp_npc12", slot_troop_2ary_morality_type, -1),
        (troop_set_slot, "trp_npc12", slot_troop_2ary_morality_value, 0),
        (troop_set_slot, "trp_npc12", slot_troop_personalityclash_object, "trp_npc8"), #Hoshi - Francisco
        (troop_set_slot, "trp_npc12", slot_troop_personalityclash2_object, "trp_npc15"), #Hoshi - Yoshio
        (troop_set_slot, "trp_npc12", slot_troop_personalitymatch_object, "trp_npc6"),  #Hoshi - Tojiko
        (troop_set_slot, "trp_npc12", slot_troop_home, "p_castle_16"), #Komaki Castle
        (troop_set_slot, "trp_npc12", slot_troop_payment_request, 0),
		(troop_set_slot, "trp_npc12", slot_troop_kingsupport_argument, argument_claim),
		(troop_set_slot, "trp_npc12", slot_troop_kingsupport_opponent, "trp_npc13"), #Teruyo
		(troop_set_slot, "trp_npc12", slot_troop_town_with_contacts, "p_town_14"), #Okayama
		(troop_set_slot, "trp_npc12", slot_troop_original_faction, 0), 
		(troop_set_slot, "trp_npc12", slot_lord_reputation_type, lrep_benefactor), 

		
		
        (troop_set_slot, "trp_npc13", slot_troop_morality_type, tmt_aristocratic), #Teruyo
        (troop_set_slot, "trp_npc13", slot_troop_morality_value, 3),
        (troop_set_slot, "trp_npc13", slot_troop_2ary_morality_type, -1),
        (troop_set_slot, "trp_npc13", slot_troop_2ary_morality_value, 0),
        (troop_set_slot, "trp_npc13", slot_troop_personalityclash_object, "trp_npc9"), #Teruyo - Nagako
        (troop_set_slot, "trp_npc13", slot_troop_personalityclash2_object, "trp_npc6"), #Teruyo - Tojiko
        (troop_set_slot, "trp_npc13", slot_troop_personalitymatch_object, "trp_npc8"), #Teruyo - Francisco
        (troop_set_slot, "trp_npc13", slot_troop_home, "p_castle_15"), #Sakado Castle
        (troop_set_slot, "trp_npc13", slot_troop_payment_request, 300),
		(troop_set_slot, "trp_npc13", slot_troop_kingsupport_argument, argument_claim),
		(troop_set_slot, "trp_npc13", slot_troop_kingsupport_opponent, "trp_npc10"), #Goemon
		(troop_set_slot, "trp_npc13", slot_troop_town_with_contacts, "p_town_4"), #Kyoto
		(troop_set_slot, "trp_npc13", slot_troop_original_faction, 0),
		(troop_set_slot, "trp_npc13", slot_lord_reputation_type, lrep_cunning),

		
		
        (troop_set_slot, "trp_npc14", slot_troop_morality_type, tmt_aristocratic), #Sessai
        (troop_set_slot, "trp_npc14", slot_troop_morality_value, 4),
        (troop_set_slot, "trp_npc14", slot_troop_2ary_morality_type, tmt_egalitarian),
        (troop_set_slot, "trp_npc14", slot_troop_2ary_morality_value, -1),
        (troop_set_slot, "trp_npc14", slot_troop_personalityclash_object, "trp_npc3"), #Sessai - William
        (troop_set_slot, "trp_npc14", slot_troop_personalityclash2_object, "trp_npc10"), #Sessai - Goemon
        (troop_set_slot, "trp_npc14", slot_troop_personalitymatch_object, "trp_npc15"), #Sessai - Yoshio
        (troop_set_slot, "trp_npc14", slot_troop_home, "p_castle_18"), #Shibata Castle
        (troop_set_slot, "trp_npc14", slot_troop_payment_request, 400),
		(troop_set_slot, "trp_npc14", slot_troop_kingsupport_argument, argument_victory),
		(troop_set_slot, "trp_npc14", slot_troop_kingsupport_opponent, "trp_npc11"), #Mari
		(troop_set_slot, "trp_npc14", slot_troop_town_with_contacts, "p_town_16"), #Hyogonosuke
		(troop_set_slot, "trp_npc14", slot_troop_original_faction, 0), 
		(troop_set_slot, "trp_npc14", slot_lord_reputation_type, lrep_selfrighteous), 


        (troop_set_slot, "trp_npc15", slot_troop_morality_type, tmt_egalitarian),  #Yoshio
        (troop_set_slot, "trp_npc15", slot_troop_morality_value, 2),
        (troop_set_slot, "trp_npc15", slot_troop_2ary_morality_type, tmt_honest),
        (troop_set_slot, "trp_npc15", slot_troop_2ary_morality_value, 1),
        (troop_set_slot, "trp_npc15", slot_troop_personalityclash_object, "trp_npc16"), #Yoshio - Hyogonosuke
        (troop_set_slot, "trp_npc15", slot_troop_personalityclash2_object, "trp_npc12"), #Yoshio - Hoshi
        (troop_set_slot, "trp_npc15", slot_troop_personalitymatch_object, "trp_npc14"), #Yoshio - Sessai
        (troop_set_slot, "trp_npc15", slot_troop_home, "p_town_23"), #Odawara
        (troop_set_slot, "trp_npc15", slot_troop_payment_request, 300),
		(troop_set_slot, "trp_npc15", slot_troop_kingsupport_argument, argument_lords),
		(troop_set_slot, "trp_npc15", slot_troop_kingsupport_opponent, "trp_npc4"), #Gonnosuke
 		(troop_set_slot, "trp_npc15", slot_troop_town_with_contacts, "p_town_18"), #Hirosaki
		(troop_set_slot, "trp_npc15", slot_troop_original_faction, 0), 
		(troop_set_slot, "trp_npc15", slot_lord_reputation_type, lrep_cunning), 

		
        (troop_set_slot, "trp_npc16", slot_troop_morality_type, tmt_aristocratic), #Hyogonosuke
        (troop_set_slot, "trp_npc16", slot_troop_morality_value, 4),
        (troop_set_slot, "trp_npc16", slot_troop_2ary_morality_type, tmt_humanitarian),
        (troop_set_slot, "trp_npc16", slot_troop_2ary_morality_value, -1),
        (troop_set_slot, "trp_npc16", slot_troop_personalityclash_object, "trp_npc15"), #Hyogonosuke - Yoshio
        (troop_set_slot, "trp_npc16", slot_troop_personalityclash2_object, "trp_npc1"), #Hyogonosuke - Kojiro
        (troop_set_slot, "trp_npc16", slot_troop_personalitymatch_object, "trp_npc7"),  #Hyogonosuke - Musashi
        (troop_set_slot, "trp_npc16", slot_troop_home, "p_village_20"), #Ashiya
        (troop_set_slot, "trp_npc16", slot_troop_payment_request, 200),
		(troop_set_slot, "trp_npc16", slot_troop_kingsupport_argument, argument_lords),
		(troop_set_slot, "trp_npc16", slot_troop_kingsupport_opponent, "trp_npc12"), #Hoshi
 		(troop_set_slot, "trp_npc16", slot_troop_town_with_contacts, "p_town_9"), #Kiyosu
		(troop_set_slot, "trp_npc16", slot_troop_original_faction, 0), 
		(troop_set_slot, "trp_npc16", slot_lord_reputation_type, lrep_goodnatured), 

		
		#gekokujo new npcs
        (troop_set_slot, "trp_npc17", slot_troop_morality_type, tmt_aristocratic), #Yeosong
        (troop_set_slot, "trp_npc17", slot_troop_morality_value, 4),
        (troop_set_slot, "trp_npc17", slot_troop_2ary_morality_type, tmt_humanitarian),
        (troop_set_slot, "trp_npc17", slot_troop_2ary_morality_value, -1),
        (troop_set_slot, "trp_npc17", slot_troop_personalityclash_object, "trp_npc18"), #Yeosong - Mandukhai
        (troop_set_slot, "trp_npc17", slot_troop_personalityclash2_object, "trp_npc20"), #Yeosong - Shih
        (troop_set_slot, "trp_npc17", slot_troop_personalitymatch_object, "trp_npc22"),  #Yeosong - Isosangemat
        (troop_set_slot, "trp_npc17", slot_troop_home, "p_town_19"), #Hakata
        (troop_set_slot, "trp_npc17", slot_troop_payment_request, 400),
		(troop_set_slot, "trp_npc17", slot_troop_kingsupport_argument, argument_none),
		(troop_set_slot, "trp_npc17", slot_troop_kingsupport_opponent, "trp_npc19"), #George
		#(troop_set_slot, "trp_npc17", slot_troop_kingsupport_opponent, "trp_npc21"), #Enrique
 		(troop_set_slot, "trp_npc17", slot_troop_town_with_contacts, "p_town_23"), #Odawara
		(troop_set_slot, "trp_npc17", slot_troop_original_faction, 0), 
		(troop_set_slot, "trp_npc17", slot_lord_reputation_type, lrep_quarrelsome),

		
        (troop_set_slot, "trp_npc18", slot_troop_morality_type, tmt_humanitarian), #Mandukhai
        (troop_set_slot, "trp_npc18", slot_troop_morality_value, 4),
        (troop_set_slot, "trp_npc18", slot_troop_2ary_morality_type, -1),
        (troop_set_slot, "trp_npc18", slot_troop_2ary_morality_value, 0),
        (troop_set_slot, "trp_npc18", slot_troop_personalityclash_object, "trp_npc17"), #Mandukhai - Yeosong
        (troop_set_slot, "trp_npc18", slot_troop_personalityclash2_object, "trp_npc19"), #Mandukhai - George
        (troop_set_slot, "trp_npc18", slot_troop_personalitymatch_object, "trp_npc20"),  #Mandukhai - Shih
        (troop_set_slot, "trp_npc18", slot_troop_home, "p_town_24"), #Nara
        (troop_set_slot, "trp_npc18", slot_troop_payment_request, 0),
		(troop_set_slot, "trp_npc18", slot_troop_kingsupport_argument, argument_none),
		(troop_set_slot, "trp_npc18", slot_troop_kingsupport_opponent, "trp_npc21"), #Enrique
		#(troop_set_slot, "trp_npc18", slot_troop_kingsupport_opponent, "trp_npc22"), #Isosangemat
 		(troop_set_slot, "trp_npc18", slot_troop_town_with_contacts, "p_town_19"), #Hakata
		(troop_set_slot, "trp_npc18", slot_troop_original_faction, 0), 
		(troop_set_slot, "trp_npc18", slot_lord_reputation_type, lrep_benefactor), 

		
        (troop_set_slot, "trp_npc19", slot_troop_morality_type, tmt_aristocratic), #George
        (troop_set_slot, "trp_npc19", slot_troop_morality_value, -1),
        (troop_set_slot, "trp_npc19", slot_troop_2ary_morality_type, tmt_humanitarian),
        (troop_set_slot, "trp_npc19", slot_troop_2ary_morality_value, 2),
        (troop_set_slot, "trp_npc19", slot_troop_personalityclash_object, "trp_npc18"), #George - Mandukhai
        (troop_set_slot, "trp_npc19", slot_troop_personalityclash2_object, "trp_npc22"), #George - Isosangemat
        (troop_set_slot, "trp_npc19", slot_troop_personalitymatch_object, "trp_npc21"),  #George - Enrique
        (troop_set_slot, "trp_npc19", slot_troop_home, "p_castle_7"), #Obama Castle
        (troop_set_slot, "trp_npc19", slot_troop_payment_request, 0),
		(troop_set_slot, "trp_npc19", slot_troop_kingsupport_argument, argument_none),
		(troop_set_slot, "trp_npc19", slot_troop_kingsupport_opponent, "trp_npc20"), #Shih
		#(troop_set_slot, "trp_npc19", slot_troop_kingsupport_opponent, "trp_npc17"), #Yeosong
 		(troop_set_slot, "trp_npc19", slot_troop_town_with_contacts, "p_town_21"), #Nagasaki
		(troop_set_slot, "trp_npc19", slot_troop_original_faction, 0), 
		(troop_set_slot, "trp_npc19", slot_lord_reputation_type, lrep_roguish), 

		
        (troop_set_slot, "trp_npc20", slot_troop_morality_type, tmt_honest), #Shih
        (troop_set_slot, "trp_npc20", slot_troop_morality_value, -1),
        (troop_set_slot, "trp_npc20", slot_troop_2ary_morality_type, tmt_egalitarian),
        (troop_set_slot, "trp_npc20", slot_troop_2ary_morality_value, 2),
        (troop_set_slot, "trp_npc20", slot_troop_personalityclash_object, "trp_npc17"), #Shih - Yeosong
        (troop_set_slot, "trp_npc20", slot_troop_personalityclash2_object, "trp_npc21"), #Shih - Enrique
        (troop_set_slot, "trp_npc20", slot_troop_personalitymatch_object, "trp_npc18"),  #Shih - Mandukhai
        (troop_set_slot, "trp_npc20", slot_troop_home, "p_town_21"), #Nagasaki
        (troop_set_slot, "trp_npc20", slot_troop_payment_request, 300),
		(troop_set_slot, "trp_npc20", slot_troop_kingsupport_argument, argument_none),
		(troop_set_slot, "trp_npc20", slot_troop_kingsupport_opponent, "trp_npc22"), #Isosangemat
		#(troop_set_slot, "trp_npc20", slot_troop_kingsupport_opponent, "trp_npc19"), #George
 		(troop_set_slot, "trp_npc20", slot_troop_town_with_contacts, "p_town_27"), #Yamaguchi
		(troop_set_slot, "trp_npc20", slot_troop_original_faction, 0), 
		(troop_set_slot, "trp_npc20", slot_lord_reputation_type, lrep_roguish), 

		
        (troop_set_slot, "trp_npc21", slot_troop_morality_type, tmt_aristocratic), #Enrique
        (troop_set_slot, "trp_npc21", slot_troop_morality_value, -1),
        (troop_set_slot, "trp_npc21", slot_troop_2ary_morality_type, -1),
        (troop_set_slot, "trp_npc21", slot_troop_2ary_morality_value, 0),
        (troop_set_slot, "trp_npc21", slot_troop_personalityclash_object, "trp_npc20"), #Enrique - Shih
        (troop_set_slot, "trp_npc21", slot_troop_personalityclash2_object, "trp_npc22"), #Enrique - Isosangemat
        (troop_set_slot, "trp_npc21", slot_troop_personalitymatch_object, "trp_npc19"),  #Enrique - George
        (troop_set_slot, "trp_npc21", slot_troop_home, "p_town_31"), #Kochi
        (troop_set_slot, "trp_npc21", slot_troop_payment_request, 200),
		(troop_set_slot, "trp_npc21", slot_troop_kingsupport_argument, argument_none),
		(troop_set_slot, "trp_npc21", slot_troop_kingsupport_opponent, "trp_npc17"), #Yeosong
		#(troop_set_slot, "trp_npc21", slot_troop_kingsupport_opponent, "trp_npc18"), #Mandukhai
 		(troop_set_slot, "trp_npc21", slot_troop_town_with_contacts, "p_town_13"), #Hiroshima
		(troop_set_slot, "trp_npc21", slot_troop_original_faction, 0), 
		(troop_set_slot, "trp_npc21", slot_lord_reputation_type, lrep_roguish), 

		
        (troop_set_slot, "trp_npc22", slot_troop_morality_type, tmt_aristocratic), #Isosangemat
        (troop_set_slot, "trp_npc22", slot_troop_morality_value, 2),
        (troop_set_slot, "trp_npc22", slot_troop_2ary_morality_type, -1),
        (troop_set_slot, "trp_npc22", slot_troop_2ary_morality_value, 0),
        (troop_set_slot, "trp_npc22", slot_troop_personalityclash_object, "trp_npc19"), #Isosangemat - George
        (troop_set_slot, "trp_npc22", slot_troop_personalityclash2_object, "trp_npc21"), #Isosangemat - Enrique
        (troop_set_slot, "trp_npc22", slot_troop_personalitymatch_object, "trp_npc17"),  #Isosangemat - Yeosong
        (troop_set_slot, "trp_npc22", slot_troop_home, "p_village_83"), #Ichinoseki
        (troop_set_slot, "trp_npc22", slot_troop_payment_request, 0),
		(troop_set_slot, "trp_npc22", slot_troop_kingsupport_argument, argument_claim),
		(troop_set_slot, "trp_npc22", slot_troop_kingsupport_opponent, "trp_npc18"), #Mandukhai
		#(troop_set_slot, "trp_npc22", slot_troop_kingsupport_opponent, "trp_npc20"), #Shih
 		(troop_set_slot, "trp_npc22", slot_troop_town_with_contacts, "p_town_25"), #Hamamatsu
		(troop_set_slot, "trp_npc22", slot_troop_original_faction, 0), 
		(troop_set_slot, "trp_npc22", slot_lord_reputation_type, lrep_martial), 



        (store_sub, "$number_of_npc_slots", slot_troop_strings_end, slot_troop_intro),

        (try_for_range, ":npc", companions_begin, companions_end),


            (try_for_range, ":slot_addition", 0, "$number_of_npc_slots"),
                (store_add, ":slot", ":slot_addition", slot_troop_intro),

				#gekokujo reminder: the following is the number of npc companions
                (store_mul, ":string_addition", ":slot_addition", 22),
                (store_add, ":string", "str_npc1_intro", ":string_addition"), 
                (val_add, ":string", ":npc"),
                (val_sub, ":string", companions_begin),

                (troop_set_slot, ":npc", ":slot", ":string"),
            (try_end),
        (try_end),
		

#Post 0907 changes begin
        (call_script, "script_add_log_entry", logent_game_start, "trp_player", -1, -1, -1),
#Post 0907 changes end

#Rebellion changes begin
        (troop_set_slot, "trp_kingdom_1_pretender",  slot_troop_original_faction, "fac_kingdom_1"),
        (troop_set_slot, "trp_kingdom_2_pretender",  slot_troop_original_faction, "fac_kingdom_2"),
        (troop_set_slot, "trp_kingdom_3_pretender",  slot_troop_original_faction, "fac_kingdom_3"),
        (troop_set_slot, "trp_kingdom_4_pretender",  slot_troop_original_faction, "fac_kingdom_4"),
        (troop_set_slot, "trp_kingdom_5_pretender",  slot_troop_original_faction, "fac_kingdom_5"),
        (troop_set_slot, "trp_kingdom_6_pretender",  slot_troop_original_faction, "fac_kingdom_6"),

#        (troop_set_slot, "trp_kingdom_1_pretender", slot_troop_support_base,     "p_town_4"), #suno
#        (troop_set_slot, "trp_kingdom_2_pretender", slot_troop_support_base,     "p_town_11"), #curaw
#        (troop_set_slot, "trp_kingdom_3_pretender", slot_troop_support_base,     "p_town_18"), #town_18
#        (troop_set_slot, "trp_kingdom_4_pretender", slot_troop_support_base,     "p_town_12"), #wercheg
#        (troop_set_slot, "trp_kingdom_5_pretender", slot_troop_support_base,     "p_town_3"), #veluca
        ##diplomacy start+
		(troop_set_slot, "trp_kingdom_1_pretender", slot_troop_home, "p_town_12"),#Lady Yamanouchi - Kasugayama
		(troop_set_slot, "trp_kingdom_2_pretender", slot_troop_home, "p_town_16"),#Lord Ashina - Yonezawa
		(troop_set_slot, "trp_kingdom_3_pretender", slot_troop_home, "p_town_9"),#Lord Saito - Kiyosu
		(troop_set_slot, "trp_kingdom_4_pretender", slot_troop_home, "p_town_27"),#Lord Ouchi - Yamaguchi
		(troop_set_slot, "trp_kingdom_5_pretender", slot_troop_home, "p_town_11"),#Lord Takeda - Kofu
		(troop_set_slot, "trp_kingdom_6_pretender", slot_troop_home, "p_town_25"),#Lady Imagawa - Hamamatsu
        ##diplomacy end+
        (try_for_range, ":pretender", pretenders_begin, pretenders_end),
            (troop_set_slot, ":pretender", slot_lord_reputation_type, lrep_none),
            ##diplomacy start+
            (troop_get_slot, ":home", ":pretender", slot_troop_home),
            (ge, ":home", 1),
            (neg|party_slot_ge, ":home", dplmc_slot_center_original_lord, 1),
            (party_set_slot, ":home", dplmc_slot_center_original_lord, ":pretender"),
            ##diplomacy end+
        (try_end),
#Rebellion changes end
     ]),
  ("objectionable_action",
    [
        (store_script_param_1, ":action_type"),
        (store_script_param_2, ":action_string"),

        (assign, ":grievance_minimum", -2),
        (try_for_range, ":npc", companions_begin, companions_end),
            (main_party_has_troop, ":npc"),

###Primary morality check
            (try_begin),
                (troop_slot_eq, ":npc", slot_troop_morality_type, ":action_type"),
                (troop_get_slot, ":value", ":npc", slot_troop_morality_value),
                (try_begin),
                    (troop_slot_eq, ":npc", slot_troop_morality_state, tms_acknowledged),
# npc is betrayed, major penalty to player honor and morale
                    (troop_get_slot, ":grievance", ":npc", slot_troop_morality_penalties),
                    (val_mul, ":value", 2),
                    (val_add, ":grievance", ":value"),
                    (troop_set_slot, ":npc", slot_troop_morality_penalties, ":grievance"),
                (else_try),
                    (this_or_next|troop_slot_eq, ":npc", slot_troop_morality_state, tms_dismissed),
                        (eq, "$disable_npc_complaints", 1),
# npc is quietly disappointed
                    (troop_get_slot, ":grievance", ":npc", slot_troop_morality_penalties),
                    (val_add, ":grievance", ":value"),
                    (troop_set_slot, ":npc", slot_troop_morality_penalties, ":grievance"),
                (else_try),
# npc raises the issue for the first time
                    (troop_slot_eq, ":npc", slot_troop_morality_state, tms_no_problem),
                    (gt, ":value", ":grievance_minimum"),
                    (assign, "$npc_with_grievance", ":npc"),
                    (assign, "$npc_grievance_string", ":action_string"),
                    (assign, "$npc_grievance_slot", slot_troop_morality_state),
                    (assign, ":grievance_minimum", ":value"),
                    (assign, "$npc_praise_not_complaint", 0),
                    (try_begin),
                        (lt, ":value", 0),
                        (assign, "$npc_praise_not_complaint", 1),
                    (try_end),
                (try_end),

###Secondary morality check
            (else_try),
                (troop_slot_eq, ":npc", slot_troop_2ary_morality_type, ":action_type"),
                (troop_get_slot, ":value", ":npc", slot_troop_2ary_morality_value),
                (try_begin),
                    (troop_slot_eq, ":npc", slot_troop_2ary_morality_state, tms_acknowledged),
# npc is betrayed, major penalty to player honor and morale
                    (troop_get_slot, ":grievance", ":npc", slot_troop_morality_penalties),
                    (val_mul, ":value", 2),
                    (val_add, ":grievance", ":value"),
                    (troop_set_slot, ":npc", slot_troop_morality_penalties, ":grievance"),
                (else_try),
                    (this_or_next|troop_slot_eq, ":npc", slot_troop_2ary_morality_state, tms_dismissed),
                        (eq, "$disable_npc_complaints", 1),
# npc is quietly disappointed
                    (troop_get_slot, ":grievance", ":npc", slot_troop_morality_penalties),
                    (val_add, ":grievance", ":value"),
                    (troop_set_slot, ":npc", slot_troop_morality_penalties, ":grievance"),
                (else_try),
# npc raises the issue for the first time
                    (troop_slot_eq, ":npc", slot_troop_2ary_morality_state, tms_no_problem),
                    (gt, ":value", ":grievance_minimum"),
                    (assign, "$npc_with_grievance", ":npc"),
                    (assign, "$npc_grievance_string", ":action_string"),
                    (assign, "$npc_grievance_slot", slot_troop_2ary_morality_state),
                    (assign, ":grievance_minimum", ":value"),
                    (assign, "$npc_praise_not_complaint", 0),
                    (try_begin),
                        (lt, ":value", 0),
                        (assign, "$npc_praise_not_complaint", 1),
                    (try_end),
                (try_end),
            (try_end),

            (try_begin),
                (gt, "$npc_with_grievance", 0),
                (eq, "$npc_praise_not_complaint", 0),
                (str_store_troop_name, 4, "$npc_with_grievance"),
                (display_message, "@{s4} looks upset."),
            (try_end),
        (try_end),        
     ]),
  ("post_battle_personality_clash_check",
[
            (try_for_range, ":npc", companions_begin, companions_end),
                (eq, "$disable_npc_complaints", 0),

                (main_party_has_troop, ":npc"),
                (neg|troop_is_wounded, ":npc"),

                (troop_get_slot, ":other_npc", ":npc", slot_troop_personalityclash2_object),
                (main_party_has_troop, ":other_npc"),
                (neg|troop_is_wounded, ":other_npc"),

#                (store_random_in_range, ":random", 0, 3),
                (try_begin),
                    (troop_slot_eq, ":npc", slot_troop_personalityclash2_state, 0),
                    (try_begin),
#                        (eq, ":random", 0),
                        (assign, "$npc_with_personality_clash_2", ":npc"),
                    (try_end),
                (try_end),

            (try_end),

            (try_for_range, ":npc", companions_begin, companions_end),
                (troop_slot_eq, ":npc", slot_troop_personalitymatch_state, 0),
                (eq, "$disable_npc_complaints", 0),

                (main_party_has_troop, ":npc"),
                (neg|troop_is_wounded, ":npc"),

                (troop_get_slot, ":other_npc", ":npc", slot_troop_personalitymatch_object),
                (main_party_has_troop, ":other_npc"),
                (neg|troop_is_wounded, ":other_npc"),
                (assign, "$npc_with_personality_match", ":npc"),
            (try_end),


            (try_begin),
                (gt, "$npc_with_personality_clash_2", 0),
				(try_begin),
					(eq, "$cheat_mode", 1),
					(display_message, "str_personality_clash_conversation_begins"),
				(try_end),
				
				(try_begin),
					(main_party_has_troop, "$npc_with_personality_clash_2"),
					(assign, "$npc_map_talk_context", slot_troop_personalityclash2_state),
					(start_map_conversation, "$npc_with_personality_clash_2"),
				(else_try),
					(assign, "$npc_with_personality_clash_2", 0),
				(try_end),
            (else_try),
                (gt, "$npc_with_personality_match", 0),
				(try_begin),
					(eq, "$cheat_mode", 1),
					(display_message, "str_personality_match_conversation_begins"),
				(try_end),
								
				(try_begin),
					(main_party_has_troop, "$npc_with_personality_match"),
					(assign, "$npc_map_talk_context", slot_troop_personalitymatch_state),
					(start_map_conversation, "$npc_with_personality_match"),
				(else_try),
					(assign, "$npc_with_personality_match", 0),
				(try_end), 
			(try_end),
     ]),
  #script_event_player_defeated_enemy_party
  # INPUT: none
  # OUTPUT: none
  ("event_player_defeated_enemy_party",
    [(try_begin),
       (check_quest_active, "qst_raid_caravan_to_start_war"),
       (neg|check_quest_concluded, "qst_raid_caravan_to_start_war"),
       (party_slot_eq, "$g_enemy_party", slot_party_type, spt_kingdom_caravan),
       (store_faction_of_party, ":enemy_faction", "$g_enemy_party"),
       (quest_slot_eq, "qst_raid_caravan_to_start_war", slot_quest_target_faction, ":enemy_faction"),
       (quest_get_slot, ":cur_state", "qst_raid_caravan_to_start_war", slot_quest_current_state),
       (quest_get_slot, ":quest_target_amount", "qst_raid_caravan_to_start_war", slot_quest_target_amount),
       (val_add, ":cur_state", 1),
       (quest_set_slot, "qst_raid_caravan_to_start_war", slot_quest_current_state, ":cur_state"),
       (try_begin),
         (ge, ":cur_state", ":quest_target_amount"),
         (quest_get_slot, ":quest_target_faction", "qst_raid_caravan_to_start_war", slot_quest_target_faction),
         (quest_get_slot, ":quest_giver_troop", "qst_raid_caravan_to_start_war", slot_quest_giver_troop),
         (store_troop_faction, ":quest_giver_faction", ":quest_giver_troop"),
         (call_script, "script_diplomacy_start_war_between_kingdoms", ":quest_target_faction", ":quest_giver_faction", 1),
         (call_script, "script_succeed_quest", "qst_raid_caravan_to_start_war"),
       (try_end),
     (try_end),

     ]),
  #script_event_player_captured_as_prisoner
  # INPUT: none
  # OUTPUT: none
  ("event_player_captured_as_prisoner",
    [
        (try_begin),
          (check_quest_active, "qst_raid_caravan_to_start_war"),
          (neg|check_quest_concluded, "qst_raid_caravan_to_start_war"),
          (quest_get_slot, ":quest_target_faction", "qst_raid_caravan_to_start_war", slot_quest_target_faction),
          (store_faction_of_party, ":capturer_faction", "$capturer_party"),
          (eq, ":quest_target_faction", ":capturer_faction"),
          (call_script, "script_fail_quest", "qst_raid_caravan_to_start_war"),
        (try_end),
        #Removing followers of the player
        (try_for_range, ":troop_no", active_npcs_begin, active_npcs_end),
		  (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
          (troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
          (gt, ":party_no", 0),
          (party_is_active, ":party_no"),
          (party_slot_eq, ":party_no", slot_party_ai_state, spai_accompanying_army),
          (party_slot_eq, ":party_no", slot_party_ai_object, "p_main_party"),
          (call_script, "script_party_set_ai_state", ":party_no", spai_undefined, -1),
#          (party_set_slot, ":party_no", slot_party_commander_party, -1),
          (assign, "$g_recalculate_ais", 1),
        (try_end),
     ]),
#NPC morale both returns a string and reg0 as the morale value
  ("npc_morale",
[
        (store_script_param_1, ":npc"),

        (troop_get_slot, ":morality_grievances", ":npc", slot_troop_morality_penalties),
        (troop_get_slot, ":personality_grievances", ":npc", slot_troop_personalityclash_penalties),
        (party_get_morale, ":party_morale", "p_main_party"),

        (store_sub, ":troop_morale", ":party_morale", ":morality_grievances"),
        (val_sub, ":troop_morale", ":personality_grievances"),
        (val_add, ":troop_morale", 50),

        (assign, reg8, ":troop_morale"),
        
        (val_mul, ":troop_morale", 3),
        (val_div, ":troop_morale", 4),
        (val_clamp, ":troop_morale", 0, 100),

        (assign, reg5, ":party_morale"),
        (assign, reg6, ":morality_grievances"),
        (assign, reg7, ":personality_grievances"),
        (assign, reg9, ":troop_morale"),

#        (str_store_troop_name, s11, ":npc"),
#        (display_message, "@{!}{s11}'s morale = PM{reg5} + 50 - MG{reg6} - PG{reg7} = {reg8} x 0.75 = {reg9}"),

        (try_begin),
            (lt, ":morality_grievances", 3),
            (str_store_string, 7, "str_happy"),
        (else_try),
            (lt, ":morality_grievances", 15),
            (str_store_string, 7, "str_content"),
        (else_try),
            (lt, ":morality_grievances", 30),
            (str_store_string, 7, "str_concerned"),
        (else_try),
            (lt, ":morality_grievances", 45),
            (str_store_string, 7, "str_not_happy"),
        (else_try),
            (str_store_string, 7, "str_miserable"),
        (try_end),


        (try_begin),
            (lt, ":personality_grievances", 3),
            (str_store_string, 6, "str_happy"),
        (else_try),
            (lt, ":personality_grievances", 15),
            (str_store_string, 6, "str_content"),
        (else_try),
            (lt, ":personality_grievances", 30),
            (str_store_string, 6, "str_concerned"),
        (else_try),
            (lt, ":personality_grievances", 45),
            (str_store_string, 6, "str_not_happy"),
        (else_try),
            (str_store_string, 6, "str_miserable"),
        (try_end),


        (try_begin),
            (gt, ":troop_morale", 80),
            (str_store_string, 8, "str_happy"),
            (str_store_string, 63, "str_bar_enthusiastic"),
        (else_try),
            (gt, ":troop_morale", 60),
            (str_store_string, 8, "str_content"),
            (str_store_string, 63, "str_bar_content"),
        (else_try),
            (gt, ":troop_morale", 40),
            (str_store_string, 8, "str_concerned"),
            (str_store_string, 63, "str_bar_weary"),
        (else_try),
            (gt, ":troop_morale", 20),
            (str_store_string, 8, "str_not_happy"),
            (str_store_string, 63, "str_bar_disgruntled"),
        (else_try),
            (str_store_string, 8, "str_miserable"),
            (str_store_string, 63, "str_bar_miserable"),
        (try_end),


        (str_store_string, 21, "str_npc_morale_report"),
        (assign, reg0, ":troop_morale"),

     ]),
#
  ("retire_companion",
[
    (store_script_param_1, ":npc"),
    (store_script_param_2, ":length"),

    (remove_member_from_party, ":npc", "p_main_party"),
    (troop_set_slot, ":npc", slot_troop_personalityclash_penalties, 0),
    (troop_set_slot, ":npc", slot_troop_morality_penalties, 0),
    (troop_get_slot, ":renown", "trp_player", slot_troop_renown),
    (store_add, ":return_renown", ":renown", ":length"),
    (troop_set_slot, ":npc", slot_troop_occupation, slto_retirement),
    (troop_set_slot, ":npc", slot_troop_return_renown, ":return_renown"),
    ]),
  #script_reduce_companion_morale_for_clash
  #script_calculate_ransom_amount_for_troop
  # INPUT: arg1 = troop_no for companion1 arg2 = troop_no for companion2 arg3 = slot_for_clash_state
  # slot_for_clash_state means: 1=give full penalty to companion1; 2=give full penalty to companion2; 3=give penalty equally
  ("reduce_companion_morale_for_clash",
   [
    (store_script_param, ":companion_1", 1),
    (store_script_param, ":companion_2", 2),
    (store_script_param, ":slot_for_clash_state", 3),

    (troop_get_slot, ":clash_state", ":companion_1", ":slot_for_clash_state"),
    (troop_get_slot, ":grievance_1", ":companion_1", slot_troop_personalityclash_penalties),
    (troop_get_slot, ":grievance_2", ":companion_2", slot_troop_personalityclash_penalties),
    (try_begin),
      (eq, ":clash_state", pclash_penalty_to_self),
      (val_add, ":grievance_1", 5),
    (else_try),
      (eq, ":clash_state", pclash_penalty_to_other),
      (val_add, ":grievance_2", 5),
    (else_try),
      (eq, ":clash_state", pclash_penalty_to_both),
      (val_add, ":grievance_1", 3),
      (val_add, ":grievance_2", 3),
    (try_end),
    (troop_set_slot, ":companion_1", slot_troop_personalityclash_penalties, ":grievance_1"),
    (troop_set_slot, ":companion_2", slot_troop_personalityclash_penalties, ":grievance_2"),
    ]),
  #script_calculate_ransom_amount_for_troop
  # INPUT: arg1 = troop_no
  # OUTPUT: reg0 = ransom_amount
  ("calculate_ransom_amount_for_troop",
    [(store_script_param, ":troop_no", 1),
     (store_troop_faction, ":faction_no", ":troop_no"),
     (assign, ":ransom_amount", 400),

	 (assign, ":male_relative", -9), #for kingdom ladies, otherwise a number otherwise unused in slot_town_lord
     (try_begin),
       (faction_slot_eq, ":faction_no", slot_faction_leader, ":troop_no"),
       (val_add, ":ransom_amount", 4000),
	 (else_try),  
       (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_lady),
       (val_add, ":ransom_amount", 2500), #as though a renown of 1250 -- therefore significantly higher than for roughly equivalent lords
	   (call_script, "script_get_kingdom_lady_social_determinants", ":troop_no"),
	   (assign, ":male_relative", reg0),
     (try_end),

     (assign, ":num_center_points", 0),
     (try_for_range, ":cur_center", centers_begin, centers_end),
       (this_or_next|party_slot_eq, ":cur_center", slot_town_lord, ":troop_no"),
		 (party_slot_eq, ":cur_center", slot_town_lord, ":male_relative"),
       (try_begin),
         (party_slot_eq, ":cur_center", slot_party_type, spt_town),
         (val_add, ":num_center_points", 4),
       (else_try),
         (party_slot_eq, ":cur_center", slot_party_type, spt_castle),
         (val_add, ":num_center_points", 2),
       (else_try),
         (val_add, ":num_center_points", 1),
       (try_end),
     (try_end),
     (val_mul, ":num_center_points", 500),
     (val_add, ":ransom_amount", ":num_center_points"),
     (troop_get_slot, ":renown", ":troop_no", slot_troop_renown),
     (val_mul, ":renown", 2),
     (val_add, ":ransom_amount", ":renown"),
     (store_mul, ":ransom_max_amount", ":ransom_amount", 3),
     (val_div, ":ransom_max_amount", 2),
     (store_random_in_range, ":random_ransom_amount", ":ransom_amount", ":ransom_max_amount"),
     (val_div, ":random_ransom_amount", 100),
     (val_mul, ":random_ransom_amount", 100),
     (assign, reg0, ":random_ransom_amount"),
     ]),
  #script_offer_ransom_amount_to_player_for_prisoners_in_party
  # INPUT: arg1 = party_no
  # OUTPUT: reg0 = result (1 = offered, 0 = not offered)
  ("offer_ransom_amount_to_player_for_prisoners_in_party",
    [(store_script_param, ":party_no", 1),
     (assign, ":result", 0),
     (party_get_num_prisoner_stacks, ":num_stacks", ":party_no"),
     (try_for_range, ":i_stack", 0, ":num_stacks"),
       (eq, ":result", 0),
       (party_prisoner_stack_get_troop_id, ":stack_troop", ":party_no", ":i_stack"),
       (troop_is_hero, ":stack_troop"),
       (this_or_next|troop_slot_eq, ":stack_troop", slot_troop_occupation, slto_kingdom_hero),
		 (troop_slot_eq, ":stack_troop", slot_troop_occupation, slto_kingdom_lady),
       (store_troop_faction, ":stack_troop_faction", ":stack_troop"),
       (store_random_in_range, ":random_no", 0, 100),
       (try_begin),
         (faction_slot_eq, ":stack_troop_faction", slot_faction_state, sfs_active),
         (le, ":random_no", 5),
         (neq, "$g_ransom_offer_rejected", 1),
         (assign, ":num_stacks", 0), #break
         (assign, ":result", 1),
         (assign, "$g_ransom_offer_troop", ":stack_troop"),
         (assign, "$g_ransom_offer_party", ":party_no"),
         (jump_to_menu, "mnu_enemy_offer_ransom_for_prisoner"),
       (try_end),
     (try_end),
     (assign, reg0, ":result"),
     ]),
  # script_event_hero_taken_prisoner_by_player
  # Input: arg1 = troop_no
  # Output: none
  ("event_hero_taken_prisoner_by_player",
    [
      (store_script_param_1, ":troop_no"),
      (try_begin),
        (check_quest_active, "qst_persuade_lords_to_make_peace"),
        (try_begin),
          (quest_slot_eq, "qst_persuade_lords_to_make_peace", slot_quest_target_troop, ":troop_no"),
          (val_mul, ":troop_no", -1),
          (quest_set_slot, "qst_persuade_lords_to_make_peace", slot_quest_target_troop, ":troop_no"),
          (val_mul, ":troop_no", -1),
        (else_try),
          (quest_slot_eq, "qst_persuade_lords_to_make_peace", slot_quest_object_troop, ":troop_no"),
          (val_mul, ":troop_no", -1),
          (quest_set_slot, "qst_persuade_lords_to_make_peace", slot_quest_object_troop, ":troop_no"),
          (val_mul, ":troop_no", -1),
        (try_end),
        (neg|check_quest_concluded, "qst_persuade_lords_to_make_peace"),
        (neg|quest_slot_ge, "qst_persuade_lords_to_make_peace", slot_quest_target_troop, 0),
        (neg|quest_slot_ge, "qst_persuade_lords_to_make_peace", slot_quest_object_troop, 0),
        (call_script, "script_succeed_quest", "qst_persuade_lords_to_make_peace"),
      (try_end),
      (call_script, "script_update_troop_location_notes", ":troop_no", 0),
  ]),
  # script_cf_check_hero_can_escape_from_player
  # Input: arg1 = troop_no
  # Output: none (can fail)
  ("cf_check_hero_can_escape_from_player",
    [
      (store_script_param_1, ":troop_no"),
      (assign, ":quest_target", 0),
      (try_begin),
        (check_quest_active, "qst_persuade_lords_to_make_peace"),
        (this_or_next|quest_slot_eq, "qst_persuade_lords_to_make_peace", slot_quest_target_troop, ":troop_no"),
        (quest_slot_eq, "qst_persuade_lords_to_make_peace", slot_quest_object_troop, ":troop_no"),
        (assign, ":quest_target", 1),
      (else_try),
        (ge, ":troop_no", "trp_rebel_leader"),
        (lt, ":troop_no", "trp_bandit_leaders_end"),
        (try_begin),
          (check_quest_active, "qst_learn_where_merchant_brother_is"),
          (assign, ":quest_target", 1), #always catched
        (else_try),  
          (assign, ":quest_target", -1), #always run.
        (try_end),
      (try_end),
      
      (assign, ":continue", 0),
      (try_begin),
        (eq, ":quest_target", 0), #if not quest target
        (store_random_in_range, ":rand", 0, 100),
        (lt, ":rand", hero_escape_after_defeat_chance),
        (assign, ":continue", 1),
      (else_try),  
        (eq, ":quest_target", -1), #if (always run) quest target
        (assign, ":continue", 1),
      (try_end),  
      
      (eq, ":continue", 1),
  ]),
  # script_cf_party_remove_random_regular_troop
  # Input: arg1 = party_no
  # Output: troop_id that has been removed (can fail)
  ("cf_party_remove_random_regular_troop",
    [(store_script_param_1, ":party_no"),
     (party_get_num_companion_stacks, ":num_stacks", ":party_no"),
     (assign, ":num_troops", 0),
     (try_for_range, ":i_stack", 0, ":num_stacks"),
       (party_stack_get_troop_id, ":stack_troop", ":party_no", ":i_stack"),
       (neg|troop_is_hero, ":stack_troop"),
       (party_stack_get_size, ":stack_size", ":party_no", ":i_stack"),
       (val_add, ":num_troops", ":stack_size"),
     (try_end),
     (assign, reg0, -1),
     (gt, ":num_troops", 0),
     (store_random_in_range, ":random_troop", 0, ":num_troops"),
     (try_for_range, ":i_stack", 0, ":num_stacks"),
       (party_stack_get_troop_id, ":stack_troop", ":party_no", ":i_stack"),
       (neg|troop_is_hero, ":stack_troop"),
       (party_stack_get_size, ":stack_size", ":party_no", ":i_stack"),
       (val_sub, ":random_troop", ":stack_size"),
       (lt, ":random_troop", 0),
       (assign, ":num_stacks", 0), #break
       (party_remove_members, ":party_no", ":stack_troop", 1),
       (assign, reg0, ":stack_troop"),
     (try_end),
     ]),
  # script_stay_captive_for_hours
  # Input: arg1 = num_hours
  # Output: none
  ("stay_captive_for_hours",
    [
      (store_script_param, ":num_hours", 1),
      (store_current_hours, ":cur_hours"),
      (val_add, ":cur_hours", ":num_hours"),
      (val_max, "$g_check_autos_at_hour", ":cur_hours"),
      (val_add, ":num_hours", 1),
      (rest_for_hours, ":num_hours", 0, 0),
    ]),
  # script_set_parties_around_player_ignore_player
  # Input: arg1 = ignore_range, arg2 = num_hours_to_ignore
  # Output: none
  ("set_parties_around_player_ignore_player",
    [(store_script_param, ":ignore_range", 1),
     (store_script_param, ":num_hours", 2),
     (try_for_parties, ":party_no"),
       (party_is_active, ":party_no"),
       (store_distance_to_party_from_party, ":dist", "p_main_party", ":party_no"),
       (lt, ":dist", ":ignore_range"),
       (party_ignore_player, ":party_no", ":num_hours"),
     (try_end),
     ]),
  # script_randomly_make_prisoner_heroes_escape_from_party
  # Input: arg1 = party_no, arg2 = escape_chance_mul_1000
  # Output: none
  ("randomly_make_prisoner_heroes_escape_from_party",
    [(store_script_param, ":party_no", 1),
     (store_script_param, ":escape_chance", 2),
     (assign, ":quest_troop_1", -1),
     (assign, ":quest_troop_2", -1),
     (try_begin),
       (check_quest_active, "qst_rescue_lord_by_replace"),
       (quest_get_slot, ":quest_troop_1", "qst_rescue_lord_by_replace", slot_quest_target_troop),
     (try_end),
     (try_begin),
       (check_quest_active, "qst_deliver_message_to_prisoner_lord"),
       (quest_get_slot, ":quest_troop_2", "qst_deliver_message_to_prisoner_lord", slot_quest_target_troop),
     (try_end),
     (party_get_num_prisoner_stacks, ":num_stacks", ":party_no"),
     (try_for_range_backwards, ":i_stack", 0, ":num_stacks"),
       (party_prisoner_stack_get_troop_id, ":stack_troop", ":party_no", ":i_stack"),
       (troop_is_hero, ":stack_troop"),
       (neq, ":stack_troop", ":quest_troop_1"),
       (neq, ":stack_troop", ":quest_troop_2"),
       (troop_slot_eq, ":stack_troop", slot_troop_occupation, slto_kingdom_hero),
       (store_random_in_range, ":random_no", 0, 1000),
       (lt, ":random_no", ":escape_chance"),
       (party_remove_prisoners, ":party_no", ":stack_troop", 1),
       (call_script, "script_remove_troop_from_prison", ":stack_troop"),
       (str_store_troop_name_link, s1, ":stack_troop"),
       (try_begin),
         (eq, ":party_no", "p_main_party"),
         (str_store_string, s2, "@your party"),
       (else_try),
         (str_store_party_name, s2, ":party_no"),
       (try_end),
       (assign, reg0, 0),
       (try_begin),
         (this_or_next|eq, ":party_no", "p_main_party"),
         (party_slot_eq, ":party_no", slot_town_lord, "trp_player"),
         (assign, reg0, 1),
       (try_end),
       (store_troop_faction, ":troop_faction", ":stack_troop"),
       (str_store_faction_name_link, s3, ":troop_faction"),
       (display_message, "@{reg0?One of your prisoners, :}{s1} of {s3} has escaped from captivity!"),
     (try_end),
     ]),
  ("remove_troop_from_prison",
    [
      (store_script_param, ":troop_no", 1),
      (troop_set_slot, ":troop_no", slot_troop_prisoner_of_party, -1),
      (try_begin),
        (eq, "$do_not_cancel_quest", 0),      
        (check_quest_active, "qst_rescue_lord_by_replace"),
        (quest_slot_eq, "qst_rescue_lord_by_replace", slot_quest_target_troop, ":troop_no"),        
        (call_script, "script_cancel_quest", "qst_rescue_lord_by_replace"),
      (try_end),
      (try_begin),
        (eq, "$do_not_cancel_quest", 0),      
        (check_quest_active, "qst_rescue_prisoner"),
        (quest_slot_eq, "qst_rescue_prisoner", slot_quest_target_troop, ":troop_no"),        
        (call_script, "script_cancel_quest", "qst_rescue_prisoner"),
      (try_end),
      (try_begin),
        (check_quest_active, "qst_deliver_message_to_prisoner_lord"),
        (quest_slot_eq, "qst_deliver_message_to_prisoner_lord", slot_quest_target_troop, ":troop_no"),
        (call_script, "script_cancel_quest", "qst_deliver_message_to_prisoner_lord"),
      (try_end),
      ]),
    #script_npc_decision_checklist_party_ai   
	# DECISION CHECKLISTS (OCT 14)
	# I was thinking of trying to convert as much AI decision-making as possible to the checklist format
	# While outcomes are not as nuanced and varied as a random decision using weighted chances for each outcoms, 
	# the checklist has the advantage of being much more transparent, both to developers and to players
	# The checklist can yield a string (standardized to s14) which explains the rationale for the decision
	# When the script yields a yes/no/maybe result, than that is standardized from -3 to +3
    # INPUT: troop_no
    # OUTPUT: none
	("npc_decision_checklist_party_ai", 
	[
	#this script can replace decide_kingdom_hero_ai and decide_kingdom_hero_ai_follow_or_not
	#However, it does not contain script_party_set_ai_state
	
	(store_script_param, ":troop_no", 1),
	
	(troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
    #(party_get_slot, ":our_strength", ":party_no", slot_party_cached_strength),
    #(store_div, ":min_strength_behind", ":our_strength", 2),
    #(party_get_slot, ":our_follower_strength", ":party_no", slot_party_follower_strength),

    (try_begin),
      (eq, "$cheat_mode", 1),
      (assign, "$g_talk_troop", ":troop_no"),
    (try_end),

    (store_troop_faction, ":faction_no", ":troop_no"),
    ##diplomacy start+
    #Get the centralization value for use below.  It should be a value in [-3,3].
    #A centralization value of 0 should not result in any behavior change.
    (try_begin),
       #If the player altered the kingdom policy, always apply its effects to
       #the AI of his kingdom's lords.
       (call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", ":faction_no"),
       (ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
       (faction_get_slot, ":centralization", ":faction_no", dplmc_slot_faction_centralization),
       (val_clamp, ":centralization", -3, 4),
    (else_try),
       #Currently, do not apply centralization to the AI for NPC kingdoms, since
       #NPC rulers set their policies randomly and do not gain the same monthly
       #relation bonuses/penalties from centralization that the player does.
       (assign, ":centralization", 0),
    (try_end),
    ##diplomacy end+

	(try_begin),
      (eq, ":troop_no", "$g_talk_troop"),
      (str_store_string, s15, "str__i_must_attend_to_this_matter_before_i_worry_about_the_affairs_of_the_realm"),
	(try_end),
	
    #find current center
    (party_get_attached_to, ":cur_center_no", ":party_no"),
    (try_begin),
      (lt, ":cur_center_no", 0),
      (party_get_cur_town, ":cur_center_no", ":party_no"),
    (try_end),
    (assign, ":besieger_party", -1),
    (try_begin),
      (neg|is_between, ":cur_center_no", centers_begin, centers_end),
      (assign, ":cur_center_no", -1),
    (else_try),
      (party_get_slot, ":besieger_party", ":cur_center_no", slot_center_is_besieged_by),
      (try_begin),
        (neg|party_is_active, ":besieger_party"),
        (assign, ":besieger_party", -1),
      (try_end),
    (try_end),
    
	#party_count
    (call_script, "script_party_count_fit_for_battle", ":party_no"),
    (assign, ":party_fit_for_battle", reg0),
    (call_script, "script_party_get_ideal_size", ":party_no"),
    (assign, ":ideal_size", reg0),
    (store_mul, ":party_strength_as_percentage_of_ideal", ":party_fit_for_battle", 100),
    (val_div, ":party_strength_as_percentage_of_ideal", ":ideal_size"),
    (try_begin),
      (faction_slot_eq, ":faction_no", slot_faction_num_towns, 0),
      (faction_slot_eq, ":faction_no", slot_faction_num_castles, 0),
      (assign, ":party_ratio_of_prisoners", 0), #do not let prisoners have an effect on ai calculation
    (else_try),
	  #gekokujo 3.0 integrating motomataru's campaign AI start
      #(party_get_num_prisoners, ":num_prisoners", ":party_no"),
      #(val_max, ":party_fit_for_battle", 1), #avoid division by zero error
      #(store_div, ":party_ratio_of_prisoners", ":num_prisoners", ":party_fit_for_battle"),
	  (party_get_num_prisoners, ":party_ratio_of_prisoners", ":party_no"),
	  (val_mul, ":party_ratio_of_prisoners", 100),	#MOTO I believe they're going for 35% prisoners, not 35:1 prisoners (see below)
      (val_max, ":party_fit_for_battle", 1), #avoid division by zero error
	  (val_div, ":party_ratio_of_prisoners", ":party_fit_for_battle"),	#MOTO scrimping for local var slots
	  #gekokujo 3.0 integrating motomataru's campaign AI end
    (try_end),
				
	(assign, ":faction_is_at_war", 0),
	#gekokujo 3.0 integrating motomataru's campaign AI start
	#(try_for_range, ":kingdom", kingdoms_begin, kingdoms_end),
	#  (faction_slot_eq, ":kingdom", slot_faction_state, sfs_active),
	#  (store_relation, ":relation", ":faction_no", ":kingdom"),
	(try_for_range, reg0, kingdoms_begin, kingdoms_end),
	  (faction_slot_eq, reg0, slot_faction_state, sfs_active),
	  (store_relation, ":relation", ":faction_no", reg0),
	#gekokujo 3.0 integrating motomataru's campaign AI end
	  (lt, ":relation", 0),
	  (assign, ":faction_is_at_war", 1),
	(try_end),
	
	(assign, ":operation_in_progress", 0),
	(try_begin),
	  (this_or_next|party_slot_eq, ":party_no", slot_party_ai_state, spai_raiding_around_center),
	  (party_slot_eq, ":party_no", slot_party_ai_state, spai_besieging_center),
	  
	  (party_get_slot, ":target_center", ":party_no", slot_party_ai_object),
	  (is_between, ":target_center", centers_begin, centers_end),
	  
	  #gekokujo 3.0 integrating motomataru's campaign AI start
	  #(store_faction_of_party, ":target_center_faction", ":target_center"),
	  #(store_relation, ":relation", ":faction_no", ":target_center_faction"),
	  (store_faction_of_party, ":center_faction", ":target_center"),
	  (store_relation, ":relation", ":faction_no", ":center_faction"),(lt, ":relation", 0),
	  
	  (store_distance_to_party_from_party, ":distance", ":party_no", ":target_center"),
	  (lt, ":distance", 10),
	  
	  #MOTO keep marshal from getting stranded during siege
	  (try_begin),
	    (party_slot_eq, ":target_center", slot_village_state, svs_under_siege),
	    (faction_slot_eq, ":faction_no", slot_faction_marshall, ":troop_no"),
        (neg|party_slot_ge, ":party_no", slot_party_follower_strength, 1000),	#about 50 troops
		(assign, ":marshal_stranded", 1),
	  (else_try),
	    (assign, ":marshal_stranded", 0),
	  (try_end),
	  
	  (eq, ":marshal_stranded", 0),
	  #MOTO end keep marshal from getting stranded during siege

	  (this_or_next|party_slot_eq, ":target_center", slot_village_state, svs_under_siege),
	  (this_or_next|party_slot_eq, ":target_center", slot_village_state, svs_normal),
	  (party_slot_eq, ":target_center", slot_village_state, svs_being_raided),
	  
	  (assign, ":operation_in_progress", 1),	
	  
	#MOTO include operations under commander
	(else_try),
	  (party_slot_eq, ":party_no", slot_party_ai_state, spai_accompanying_army),
	  
	  (party_get_slot, ":commander_party", ":party_no", slot_party_ai_object),
	  (gt, ":commander_party", 0),
	  (party_is_active, ":commander_party"),
	  (party_get_slot, ":target_center", ":commander_party", slot_party_ai_object),
	  (is_between, ":target_center", centers_begin, centers_end),
	  
	  (store_faction_of_party, ":center_faction", ":target_center"),
	  (store_relation, ":relation", ":faction_no", ":center_faction"),
	  #gekokujo 3.0 integrating motomataru's campaign AI end
	  (lt, ":relation", 0),
	  
	  (store_distance_to_party_from_party, ":distance", ":party_no", ":target_center"),
	  (lt, ":distance", 10),
	  (this_or_next|party_slot_eq, ":target_center", slot_village_state, svs_under_siege),
	  (this_or_next|party_slot_eq, ":target_center", slot_village_state, svs_normal),
	  (party_slot_eq, ":target_center", slot_village_state, svs_being_raided),
	  
	  (assign, ":operation_in_progress", 1),	
	(try_end),
			
	(troop_get_slot, ":troop_reputation", ":troop_no", slot_lord_reputation_type),
			
    (party_get_slot, ":old_ai_state", ":party_no", slot_party_ai_state),
    (party_get_slot, ":old_ai_object", ":party_no", slot_party_ai_object),

	(party_get_slot, ":party_cached_strength", ":party_no", slot_party_cached_strength),
	
	(store_current_hours, ":hours_since_last_rest"),
	#gekokujo 3.0 integrating motomataru's campaign AI start
	#(party_get_slot, ":last_rest_time", ":party_no", slot_party_last_in_any_center),
	#(val_sub, ":hours_since_last_rest", ":last_rest_time"),
	#
	#(store_current_hours, ":hours_since_last_home"),
	#(party_get_slot, ":last_home_time", ":party_no", slot_party_last_in_home_center),
	#(val_sub, ":hours_since_last_home", ":last_home_time"),
	#
	#(store_current_hours, ":hours_since_last_combat"),
	#(party_get_slot, ":last_combat_time", ":party_no", slot_party_last_in_combat),
	#(val_sub, ":hours_since_last_combat", ":last_combat_time"),
	#
	#(store_current_hours, ":hours_since_last_courtship"),
	#(party_get_slot, ":last_courtship_time", ":party_no", slot_party_leader_last_courted),
	#(val_sub, ":hours_since_last_courtship", ":last_courtship_time"),
	
    #(troop_get_slot, ":temp_ai_seed", ":troop_no", slot_troop_temp_decision_seed),
    #(store_mod, ":aggressiveness", ":temp_ai_seed", 73), #To derive the 
	(party_get_slot, reg0, ":party_no", slot_party_last_in_any_center),
	(val_sub, ":hours_since_last_rest", reg0),
	
	(store_current_hours, ":hours_since_last_home"),
	(party_get_slot, reg0, ":party_no", slot_party_last_in_home_center),
	(val_sub, ":hours_since_last_home", reg0),
	
	(store_current_hours, ":hours_since_last_combat"),
	(party_get_slot, reg0, ":party_no", slot_party_last_in_combat),
	(val_sub, ":hours_since_last_combat", reg0),
	
	(store_current_hours, ":hours_since_last_courtship"),
	(party_get_slot, reg0, ":party_no", slot_party_leader_last_courted),
	(val_sub, ":hours_since_last_courtship", reg0),
	
    (troop_get_slot, reg0, ":troop_no", slot_troop_temp_decision_seed),
    (store_mod, ":aggressiveness", reg0, 73), #To derive the 
	#gekokujo 3.0 integrating motomataru's campaign AI end
    (try_begin),
      (eq, ":troop_reputation", lrep_martial),
      (val_add, ":aggressiveness", 27),
    (else_try),
      (neq, ":troop_reputation", lrep_debauched),
      (neq, ":troop_reputation", lrep_quarrelsome),
      (val_add, ":aggressiveness", 14),
    (try_end),
    
    (try_begin),
      (gt, ":aggressiveness", ":hours_since_last_combat"),
      (val_add, ":aggressiveness", ":hours_since_last_combat"),
      (val_div, ":aggressiveness", 2),
    (try_end),        
    
    (try_begin),
      (eq, "$cheat_mode", 1), #100
      (eq, ":troop_no", "$g_talk_troop"),
      (str_store_troop_name, s4, ":troop_no"), 
      (assign, reg3, ":hours_since_last_rest"),
      (assign, reg4, ":hours_since_last_courtship"),
      (assign, reg5, ":hours_since_last_combat"),
      (assign, reg6, ":hours_since_last_home"),
      (assign, reg7, ":aggressiveness"),
      #(display_message, "@{!}{s4}: hours since rest {reg3}, courtship {reg4}, combat {reg5}, home {reg6}, aggressiveness {reg7}"),
    (try_end),
		
	##I am inspecting an estate (use slot_center_npc_volunteer_troop_amount)
		
	(str_store_string, s17, "str_the_other_matter_took_precedence"),
	
	#(assign, ":do_only_collecting_rents", 0), #gekokujo 3.0 integrating motomataru's campaign AI
	
	#Wait in current city (dangerous to travel with less (<=10) men)
	(try_begin),	
      #NOTE : I added also this condition to very top of list. Because if this condition does not exists in top then a bug happens. 
      #Bug is about alone wounded lords without any troop near him travels between cities, sometimes it want to return his home city 
      #to collect reinforcements, sometimes it want to patrol ext, but his party is so weak even without anyone. So we sometimes see 
      #(0/1) parties in map with only one wounded lord inside. Because after wars completely defeated lords spawn again in a walled center 
      #in 48 hours periods (by codes in module_simple_trigers). He spawns with only wounded himself. Then he should wait in there for 
      #a time to collect new men to his (0/1) party. If a lord is the only one in his party and if he is at any walled center already then he 
      #should stay where he is. He should not travel to anywhere because of any reason. If he is the only one and he is wounded and 
      #he is not in any walled center this means this situation happens because of one another bug, because any lord cannot be out of 
      #walled centers with wounded himself only. So I am adding this condition below. 
      
      #SUMMARY : If lord has not got enought troops (<10 || <10%) with himself and he is currently at a walled center he should not leave 
      #his current center because of any reason.
      
      (ge, ":cur_center_no", 0),

	  #gekokujo 3.0 integrating motomataru's campaign AI start
      #(this_or_next|le, ":party_fit_for_battle", 10),
      #(le, ":party_strength_as_percentage_of_ideal", 30),
      (le, ":party_strength_as_percentage_of_ideal", 10),
	  #gekokujo 3.0 integrating motomataru's campaign AI end

      (assign, ":action", spai_holding_center),
      (assign, ":object", ":cur_center_no"),

	  (try_begin),
	    (eq, ":troop_no", "$g_talk_troop"), 
	    (str_store_string, s14, "str_i_need_to_raise_some_men_before_attempting_anything_else"),
	    (str_store_string, s16, "str_i_need_to_raise_some_men_before_attempting_anything_else"),
	  (try_end),
	  
	#Stand in a siege
	(else_try),
	  (gt, ":besieger_party", -1),
	  (ge, ":cur_center_no", 0), #gekokujo 3.0 integrating motomataru's campaign AI
	  
	  (assign, ":action", spai_holding_center),
	  (assign, ":object", ":cur_center_no"),
	  
	  (try_begin), 
	    (eq, ":troop_no", "$g_talk_troop"),
	    (str_store_string, s14, "str_i_cannot_leave_this_fortress_now_as_it_is_under_siege"),
	    (str_store_string, s16, "str_after_all_we_are_under_siege"),
	  (try_end),
		
	#Continue retreat to walled center
	(else_try),
	  (eq, ":old_ai_state", spai_retreating_to_center),
	  (neg|party_is_in_any_town, ":party_no"),
	  
	  (ge, ":old_ai_object", 0),
	  (party_is_active, ":old_ai_object"),
	  
	  (store_faction_of_party, ":center_faction", ":old_ai_object"),
	  (eq, ":faction_no", ":center_faction"),
	  
	  (assign, ":action", spai_retreating_to_center),
	  (assign, ":object", ":old_ai_object"),
	  	  
	  (try_begin),
	    (eq, ":troop_no", "$g_talk_troop"),
	    (str_store_string, s14, "str_we_are_not_strong_enough_to_face_the_enemy_out_in_the_open"),
	    (str_store_string, s16, "str_i_should_probably_seek_shelter_behind_some_stout_walls"),
	  (try_end),

	#Stand by in current center against enemies		
	(else_try),
	  (is_between, ":cur_center_no", walled_centers_begin, walled_centers_end),
	  
	  #gekokujo 3.0 integrating motomataru's campaign AI start
	  #(party_get_slot, ":enemy_strength_in_area", ":cur_center_no", slot_center_sortie_enemy_strength),
	  #(party_get_slot, ":enemy_strength_in_area", ":cur_center_no", slot_center_sortie_enemy_strength),
	  #(ge, ":enemy_strength_in_area", 50),
	  (party_get_slot, ":enemy_strength_nearby", ":cur_center_no", slot_center_sortie_enemy_strength),
	  (ge, ":enemy_strength_nearby", ":party_cached_strength"),
	  (party_get_slot, ":center_strength", ":cur_center_no", slot_party_cached_strength),
	  (ge, ":enemy_strength_nearby", ":center_strength"),
	  #gekokujo 3.0 integrating motomataru's campaign AI end
	  
	  (assign, ":action", spai_holding_center),
	  (assign, ":object", ":cur_center_no"),
	  (try_begin),
	    (eq, ":troop_no", "$g_talk_troop"),
	    (str_store_string, s14, "str_enemies_are_reported_to_be_nearby_and_we_should_stand_ready_to_either_man_the_walls_or_sortie_out_to_do_battle"),
	    (str_store_string, s16, "str_the_enemy_is_nearby"),
	  (try_end),
	  
	  #gekokujo 3.0 integrating motomataru's campaign AI start
	  #MOTO move here to inform marshall decisions
	#Get reinforcements
	(else_try),
	  (assign, ":lowest_acceptable_strength_percentage", 30),
	  (assign, ":distance_addition", 0),	#MOTO for testing in marshal levy section
	  
	  (call_script, "script_lord_get_home_center", ":troop_no"),
	  (assign, ":center_to_visit", reg0),
	  (gt, ":center_to_visit", -1),
	  (party_slot_eq, ":center_to_visit", slot_town_lord, ":troop_no"), #newly added
	  
	  #if troop is very close to its home center increase by 20%
	  (assign, ":distance_addition", 0),
	  (party_get_position, pos0, ":center_to_visit"),
	  (party_get_position, pos1, ":party_no"),
	  (get_distance_between_positions, ":distance", pos0, pos1),	  	  
	  (try_begin),	  
	    # (le, ":dist", 9000),	MOTO this is NOT very close
	    # (store_div, ":distance_addition", ":dist", 600),
		(le, ":distance", 1500),
	    (store_div, ":distance_addition", ":distance", 100),
	    (store_sub, ":distance_addition", 15, ":distance_addition"),
	  (else_try),
	    (assign, ":distance_addition", 0),
	  (try_end),
	  (val_add, ":lowest_acceptable_strength_percentage", ":distance_addition"),
	  
	  #if there is no campaign for faction increase by 35%
	  (assign, ":no_campaign_addition", 35),
	  (try_begin),
	    (this_or_next|faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_attacking_enemy_army),
	    (this_or_next|faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_attacking_enemies_around_center),
	    (this_or_next|faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_raiding_village),
	    (this_or_next|faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_attacking_center),
	    (faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_gathering_army),
	    (assign, ":no_campaign_addition", 0),
	    
	    #If marshal is player itself and if there is a campaign then lower lowest_acceptable_strength_percentage by 10 instead of not changing it.
	    #Because players become confused when they see very less participation from AI lords to their campaigns.
	    (try_begin),	    
	      (faction_slot_eq, ":faction_no", slot_faction_marshall, "trp_player"),
	      (options_get_campaign_ai, ":reduce_campaign_ai"),
	      (try_begin),
	        (eq, ":reduce_campaign_ai", 0), #hard
	        (assign, ":no_campaign_addition", 0),
	      (else_try),  
	        (eq, ":reduce_campaign_ai", 1), #medium
	        (assign, ":no_campaign_addition", -10),
	      (else_try),  
	        (eq, ":reduce_campaign_ai", 2), #easy
	        (assign, ":no_campaign_addition", -15),
	      (try_end),  
	    (try_end),
	  (try_end),
	  (val_add, ":lowest_acceptable_strength_percentage", ":no_campaign_addition"),
	  (val_max, ":lowest_acceptable_strength_percentage", 25),
	
	  #max : 30%+15%+35% = 80% (happens when there is no campaign and player is near to its home center.)
	  (lt, ":party_strength_as_percentage_of_ideal", ":lowest_acceptable_strength_percentage"),
	  
	  #MOTO don't interrupt marshal operation for this
	  (this_or_next|eq, ":operation_in_progress", 0),
	  (neg|faction_slot_eq, ":faction_no", slot_faction_marshall, ":troop_no"),
	  #MOTO end don't interrupt marshal operation for this
	
	  (troop_get_slot, ":troop_wealth", ":troop_no", slot_troop_wealth), 
      (assign, ":hiring_budget", ":troop_wealth"),	#MOTO hiring budget/reinforcement cost comparison from script_hire_men_to_kingdom_hero_party
      (val_mul, ":hiring_budget", 3),
      (val_div, ":hiring_budget", 4),            
	  
	  (options_get_campaign_ai, ":reduce_campaign_ai"),
      (try_begin), 
        (eq, ":reduce_campaign_ai", 0), #hard
        (assign, ":reinforcement_cost", reinforcement_cost_hard),
      (else_try), 
        (eq, ":reduce_campaign_ai", 2), #easy
        (assign, ":reinforcement_cost", reinforcement_cost_easy),
      (else_try), 
        (assign, ":reinforcement_cost", reinforcement_cost_moderate),
      (try_end),
	  
	  (try_begin),
        (ge, ":hiring_budget", ":reinforcement_cost"),
	  	  	  	  	  	  
	    (assign, ":action", spai_holding_center),
	    (assign, ":object", ":center_to_visit"),
	  
	    (try_begin),
	      (eq, ":troop_no", "$g_talk_troop"),
	      (str_store_string, s14, "str_i_dont_have_enough_troops_and_i_need_to_get_some_more"),
	      (str_store_string, s16, "str_i_am_running_low_on_troops"),
	    (try_end),
		
	  (else_try),	#MOTO copy and modify visiting estates from below to avoid needlessly skipping other state choices
	    (assign, ":action", 0),	#MOTO set test for collection undertaken
	    (assign, ":center_to_visit", -1),

        #MOTO collect rents only when it actually helps recruit
        # (assign, ":score_to_beat", 300), #at least 300 gold to pick up MOTO equals reinforcement_cost_hard
		(options_get_campaign_ai, ":reduce_campaign_ai"),
		(try_begin), 
		  (eq, ":reduce_campaign_ai", 0), #hard
		  (assign, ":score_to_beat", reinforcement_cost_hard),
		(else_try), 
		  (eq, ":reduce_campaign_ai", 2), #easy
		  (assign, ":score_to_beat", reinforcement_cost_easy),
		(else_try), 
		  (assign, ":score_to_beat", reinforcement_cost_moderate),
		(try_end),
		(val_mul, ":score_to_beat", 4),    # 4/3 "hiring budget" from script_hire_men_to_kingdom_hero_party
		(val_div, ":score_to_beat", 3),
 		(val_div, ":score_to_beat", 2),    #parties that can't afford to recruit are willing to go get half of what they need
		#MOTO end collect rents only when it actually helps recruit

	    (try_begin),	    
	      (faction_get_slot, ":faction_marshal", ":faction_no", slot_faction_marshall),
	      (ge, ":faction_marshal", 0),	#MOTO avoid bug
	    
	      (assign, reg17, 0),
	      (try_begin),
	        (party_slot_eq, ":party_no", slot_party_ai_state, spai_accompanying_army),
	        # (party_slot_eq, ":party_no", slot_party_ai_object, ":faction_marshal"),	MOTO wrong
	        (troop_get_slot, ":marshal_party", ":faction_marshal", slot_troop_leaded_party),
	        (party_is_active, ":marshal_party"),
	        (party_slot_eq, ":party_no", slot_party_ai_object, ":marshal_party"),
		    #MOTO end wrong
	        (assign, reg17, 1),
	      (else_try),  	    
	        (party_slot_eq, ":party_no", slot_party_following_player, 1),
	        (assign, reg17, 1),
	      (try_end),  
	      (eq, reg17, 1),
	    
	      (try_begin),
	        (neq, ":faction_marshal", "trp_player"),
	        (neg|party_slot_eq, ":party_no", slot_party_following_player, 1),
	        (val_add, ":score_to_beat", 125),
	      (else_try),
	        (val_add, ":score_to_beat", 250),
	      (try_end),
	    (try_end),  
	  
	    (try_for_range, ":center_no", centers_begin, centers_end),
	      (party_slot_eq, ":center_no", slot_town_lord, ":troop_no"),
	    
	      (assign, reg17, 0),
	      (try_begin),
	        (is_between, ":center_no", villages_begin, villages_end),
	        (party_slot_eq, ":center_no", slot_village_state, svs_normal),
	        (assign, reg17, 1),
	      (else_try),  	    
	        (party_slot_eq, ":center_no", slot_center_is_besieged_by, -1),
	        (assign, reg17, 1),
	      (try_end),	    
	      (eq, reg17, 1),
	    
	      (party_get_slot, ":tariffs_available", ":center_no", slot_center_accumulated_tariffs),
	      (party_get_slot, ":rents_available", ":center_no", slot_center_accumulated_rents),
	      (store_add, ":money_available", ":rents_available", ":tariffs_available"),
	    	    
	      (gt, ":money_available", ":score_to_beat"),
	      (assign, ":center_to_visit", ":center_no"),
	      (assign, ":score_to_beat", ":money_available"),			
	    (try_end),
	  
	    (is_between, ":center_to_visit", centers_begin, centers_end),
	  	  
	    (try_begin),
	      (is_between, ":center_to_visit", walled_centers_begin, walled_centers_end),
	      (assign, ":action", spai_holding_center),
	      (assign, ":object", ":center_to_visit"),
	    (else_try),  
          (assign, ":action", spai_visiting_village),
  	      (assign, ":object", ":center_to_visit"),
	    (try_end),
	  
	    (try_begin),
	      (eq, ":troop_no", "$g_talk_troop"),
	      (str_store_string, s14, "str_i_need_to_inspect_my_properties_and_collect_my_dues"),
	      (str_store_string, s16, "str_it_has_been_too_long_since_i_have_inspected_my_estates"),
	    (try_end),
	  (try_end),
	  
	  (neq, ":action", 0),	#catch failure of is_between above
	  
	(else_try),	#MOTO special state - marshall levies troops
	  (faction_slot_eq, ":faction_no", slot_faction_marshall, ":troop_no"),
	  (store_sub, reg0, ":lowest_acceptable_strength_percentage", ":distance_addition"),	#MOTO ignore distance addition for this purpose
	  (lt, ":party_strength_as_percentage_of_ideal", reg0),
	  (eq, ":operation_in_progress", 0),
	  
	  (assign, ":center_to_visit", -1),
	  (assign, ":troops_to_transfer", 25),	#don't go back until center recuits 25 more
	  
	  (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
		(store_faction_of_party, ":center_faction", ":center_no"),
		(eq, ":center_faction", ":faction_no"),
		
	    (party_get_slot, ":center_max_garrison", ":center_no", slot_town_prosperity),
		(val_mul, ":center_max_garrison", 6),
		(val_add, ":center_max_garrison", 100),	#100..700, average 400
		
	    (store_party_size_wo_prisoners, ":center_strength", ":center_no"),
	    (store_sub, ":surplus_troops", ":center_strength", ":center_max_garrison"),
		(lt, ":troops_to_transfer", ":surplus_troops"),
	    (assign, ":center_to_visit", ":center_no"),
		(assign, ":troops_to_transfer", ":surplus_troops"),
	  (try_end),
	  
	  (ge, ":center_to_visit", 0),
	  (assign, ":action", spai_holding_center),
	  (assign, ":object", ":center_to_visit"),
	  
	  (try_begin),
	    (eq, ":troop_no", "$g_talk_troop"),
	    (str_store_string, s14, "str_i_dont_have_enough_troops_and_i_need_to_get_some_more"),
	    (str_store_string, s16, "str_i_am_running_low_on_troops"),
	  (try_end),
	  
	  (try_begin),
		(party_is_in_town, ":party_no", ":center_to_visit"),
		
		(try_begin),
	      (party_get_slot, ":town_lord", ":center_to_visit", slot_town_lord),
	      (neq, ":town_lord", ":troop_no"),
		  (try_begin),
			(eq, ":town_lord", "trp_player"),
			(assign, reg0, ":troops_to_transfer"),
			(str_store_party_name, s10, ":center_to_visit"),
			(display_message, "@The marshal is levying {reg0} troops from your center {s10}."),
			
		  (else_try),
		    (store_mul, ":attitude_adjustment", ":troops_to_transfer", 20),
	        (store_party_size_wo_prisoners, ":center_strength", ":center_to_visit"),
		    (val_div, ":attitude_adjustment", ":center_strength"),
		    (val_add, ":attitude_adjustment", 1),
		    (val_mul, ":attitude_adjustment", -1),
	        (call_script, "script_troop_change_relation_with_troop", ":troop_no", ":town_lord", ":attitude_adjustment"),
		  (try_end),
		(try_end),
		
		(assign, ":num_stacks", 0),
		(assign, ":cur_stack", 1),

		(try_for_range, reg0, 0, ":troops_to_transfer"),
		  (try_begin),
		    (ge, ":cur_stack", ":num_stacks"),
            (party_get_num_companion_stacks, ":num_stacks", ":center_to_visit"),
		    (assign, ":cur_stack", 1),
		  (try_end),
		  
          (party_stack_get_troop_id, ":levy_troop", ":center_to_visit", ":cur_stack"),
          (party_stack_get_size, ":stack_size", ":center_to_visit", ":cur_stack"),
		  
		  (try_begin),
		    (this_or_next|le, ":stack_size", 0),
		    (is_between, ":levy_troop", active_npcs_begin, active_npcs_end),
			(val_add, ":troops_to_transfer", 1),	#not levying this guy!
		  (else_try),
			(party_remove_members, ":center_to_visit", ":levy_troop", 1),
			(party_add_members, ":party_no", ":levy_troop", 1),
		  (try_end),
		  
		  (val_add, ":cur_stack", 1),
		(try_end),
	  (try_end),
	#MOTO end move here to inform marshall decisions
	  #gekokujo 3.0 integrating motomataru's campaign AI end
	  
	#As the marshall, lead faction campaign
	(else_try),
	  (faction_slot_eq, ":faction_no", slot_faction_marshall, ":troop_no"),
	  #gekokujo 3.0 integrating motomataru's campaign AI start
	  #MOTO attempt to replace marshal if can't raise an army
	  (try_begin),
		(eq, ":operation_in_progress", 0),
	    (store_sub, reg0, ":lowest_acceptable_strength_percentage", ":distance_addition"),	#MOTO ignore distance addition for this purpose
	    (lt, ":party_strength_as_percentage_of_ideal", reg0),
		(faction_slot_eq, ":faction_no", slot_faction_political_issue, 0),	#not already done?
        (call_script, "script_change_troop_renown", ":troop_no", -1),
		(faction_set_slot, ":faction_no", slot_faction_political_issue, 1), #Appointment of marshal
		(store_current_hours, ":hours"),
		(val_max, ":hours", 0),
		(faction_set_slot, ":faction_no", slot_faction_political_issue_time, ":hours"),
	  (try_end),
	  #MOTO end attempt to replace marshal if can't raise an army
	  
	  #Appoint screening party MOTO move here so marshall group always has a screening party
	  (try_begin),
	    (assign, ":best_screening_party", -1),
	    (assign, ":score_to_beat", 100),	#+- this amount

	    (try_for_range, ":screen_leader", active_npcs_begin, active_npcs_end),
		  # (store_faction_of_troop, ":screen_leader_faction", ":screen_leader"),
		  # (eq, ":screen_leader_faction", ":faction_no"),	MOTO neglects allies
		 
		  (troop_get_slot, ":screening_party", ":screen_leader", slot_troop_leaded_party), 
		  (party_is_active, ":screening_party"),			
		  (party_slot_eq, ":screening_party", slot_party_ai_object, ":party_no"),
		  (party_slot_eq, ":screening_party", slot_party_ai_state, spai_accompanying_army),

		  (try_begin),
            (party_slot_eq, ":screening_party", slot_party_ai_substate, 1),	#MOTO use substate to represent screening properly
			(call_script, "script_party_set_ai_state", ":screening_party", spai_accompanying_army, ":party_no"),	#turn off screening in case not chosen again
		  (try_end),
		  
          (store_distance_to_party_from_party, ":distance", ":screening_party", ":party_no"),
          (lt, ":distance", 15),
		  
		  (try_begin),
		    (ge, "$cheat_mode", 1),
		    (str_store_party_name, s4, ":screening_party"),
		    (display_message, "@{!}DEBUG -- {s4} screening for marshall"),
		  (try_end),

		  (store_party_size_wo_prisoners, ":screening_party_score", ":screening_party"),
		  (val_sub, ":screening_party_score", 150),	#closest in size to this
		  (val_abs, ":screening_party_score"),
		 
		  (lt, ":screening_party_score", ":score_to_beat"),

		  #set party and score
		  (assign, ":best_screening_party", ":screening_party"),
		  (assign, ":score_to_beat", ":screening_party_score"),
	    (try_end),			

	    (party_is_active, ":best_screening_party"),
	    (call_script, "script_party_set_ai_state", ":best_screening_party", spai_screening_army, ":party_no"),
	    (try_begin),
		  (ge, "$cheat_mode", 1),
		  (str_store_party_name, s4, ":best_screening_party"),
		  (display_message, "@{!}DEBUG -- {s4} chosen as screen"),
	    (try_end),
	  (try_end),
	  #end Appoint screening party MOTO move here so marshall group always has a screening party
	  #gekokujo 3.0 integrating motomataru's campaign AI end
	  (str_clear, s15), #Does not say that overrides faction orders
	  (faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_gathering_army),
	  
	  (party_set_ai_initiative, ":party_no", 10),
	  	  
	  #new ozan added - active gathering
	  #this code will allow marshal to travel around cities while gathering army if currently collected are less than 60%. 
	  #By ratio increases travel distances become less. Travels will be only points around walled centers.
	  (party_get_slot, ":old_ai_object", ":party_no", slot_party_ai_object),
	  #gekokujo 3.0 integrating motomataru's campaign AI start
	  #MOTO prevent marshall from gathering at enemy centers!
      (try_begin),
        (is_between, ":old_ai_object", centers_begin, centers_end),
        (store_faction_of_party, ":center_faction", ":old_ai_object"),
        (eq, ":center_faction", ":faction_no"),
        (assign, ":travel_target", ":old_ai_object"),
      (else_try),
        (assign, ":travel_target", -1),
      (try_end),
      #MOTO end prevent marshall from gathering at enemy centers!
	  #gekokujo 3.0 integrating motomataru's campaign AI end
	  (assign, ":travel_target", ":old_ai_object"),
      
      (call_script, "script_find_center_to_defend", ":troop_no"),
	  (assign, ":most_threatened_center", reg0),	  
	  (assign, ":travel_target_new_assigned", 0),
	  
      (try_begin),
        (lt, ":old_ai_object", 0),
        
        (store_random_in_range, ":random_value", 0, 8), #to eanble marshal to wait sometime during active gathering
        (this_or_next|eq, "$g_gathering_new_started", 1),
        (eq, ":random_value", 0),
        
        (assign, ":vassals_already_assembled", 0),
        (assign, ":total_vassals", 0),
        (try_for_range, ":lord", active_npcs_begin, active_npcs_end),
          (store_faction_of_troop, ":lord_faction", ":lord"),
          (eq, ":lord_faction", ":faction_no"),
          (troop_get_slot, ":led_party", ":lord", slot_troop_leaded_party),
          (party_is_active, ":led_party"),
          (val_add, ":total_vassals", 1),
          
          (party_slot_eq, ":led_party", slot_party_ai_state, spai_accompanying_army),
          (party_slot_eq, ":led_party", slot_party_ai_object, ":party_no"),
          
          (party_is_active, ":party_no"),
		  #gekokujo 3.0 integrating motomataru's campaign AI start
          #(store_distance_to_party_from_party, ":distance_to_marshal", ":led_party", ":party_no"),
          #(lt, ":distance_to_marshal", 15),
          (store_distance_to_party_from_party, ":distance", ":led_party", ":party_no"),
          (lt, ":distance", 15),
		  #gekokujo 3.0 integrating motomataru's campaign AI end
          (val_add, ":vassals_already_assembled", 1),
        (try_end),
     
        (assign, ":ratio_of_vassals_assembled", -1),
        (try_begin),
          (gt, ":total_vassals", 0),
          (store_mul, ":ratio_of_vassals_assembled", ":vassals_already_assembled", 100),
          (val_div, ":ratio_of_vassals_assembled", ":total_vassals"),
        (try_end),
          
        (try_begin),
          #if more than 35% of vassals already collected do not make any more active gathering, just hold and wait last vassals to participate.
          (le, ":ratio_of_vassals_assembled", 35), 
                      
          (assign, ":best_center_to_travel", ":most_threatened_center"),          

          (try_begin),
            (eq, "$g_gathering_new_started", 1),
            
            (assign, ":minimum_distance", 100000),
            (try_for_range, ":center_no", centers_begin, centers_end),
              (store_faction_of_party, ":center_faction", ":center_no"),
              (eq, ":center_faction", ":faction_no"), #200
              (try_begin),
                (neq, ":center_no", ":most_threatened_center"), 
				#gekokujo 3.0 integrating motomataru's campaign AI start
                (store_distance_to_party_from_party, ":distance", ":party_no", ":center_no"),                
                (lt, ":distance", ":minimum_distance"),
                (assign, ":minimum_distance", ":distance"),
				#gekokujo 3.0 integrating motomataru's campaign AI end
                (assign, ":best_center_to_travel", ":center_no"),
              (try_end), 
            (try_end),
          (else_try), 
            #active gathering            
            (assign, ":max_travel_distance", 150),
            (try_begin),
              (ge, ":ratio_of_vassals_assembled",15),
              (store_sub, ":max_travel_distance", 35, ":ratio_of_vassals_assembled"),
              (val_add, ":max_travel_distance", 5), #5..25
              (val_mul, ":max_travel_distance", 6), #30..150
            (try_end),
            
            (try_begin),
              (ge, ":most_threatened_center", 0),
              (store_distance_to_party_from_party, reg12, ":party_no", ":most_threatened_center"),
            (else_try),  
              (assign, reg12, 0),
            (try_end),
              
            (assign, ":num_centers", 0),
            (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
              (store_faction_of_party, ":center_faction", ":center_no"),
              (eq, ":center_faction", ":faction_no"),
              (try_begin),
                #(ge, ":max_travel_distance", 0),
				#gekokujo 3.0 integrating motomataru's campaign AI start
                #(store_distance_to_party_from_party, ":dist", ":party_no", ":center_no"),
                (store_distance_to_party_from_party, ":distance", ":party_no", ":center_no"),
				#gekokujo 3.0 integrating motomataru's campaign AI end
                
                (try_begin),
                  (ge, ":most_threatened_center", 0),
                  (store_distance_to_party_from_party, reg13, ":center_no", ":most_threatened_center"),
                (else_try),  
                  (assign, reg13, 0),
                (try_end),

                (store_sub, reg11, reg13, reg12),
                
                (this_or_next|ge, reg11, 40),                
                #(this_or_next|ge, ":dist", ":max_travel_distance"), #gekokujo 3.0 integrating motomataru's campaign AI
				(this_or_next|ge, ":distance", ":max_travel_distance"),
                (eq, ":center_no", ":most_threatened_center"),
              (else_try),
                #this center is a candidate so increase num_centers by one.
                (val_add, ":num_centers", 1),
              (try_end), 
            (try_end),
            
            (try_begin),
              (ge, ":num_centers", 0),
              (store_random_in_range, ":random_center_no", 0, ":num_centers"),
              (val_add, ":random_center_no", 1),
              (assign, ":num_centers", 0),
              (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
                (store_faction_of_party, ":center_faction", ":center_no"),
                (eq, ":center_faction", ":faction_no"),
                (try_begin),
                  (neq, ":center_no", ":most_threatened_center"),
				  #gekokujo 3.0 integrating motomataru's campaign AI start
                  #(store_distance_to_party_from_party, ":dist", ":party_no", ":center_no"),
                  #(lt, ":dist", ":max_travel_distance"),
                  (store_distance_to_party_from_party, ":distance", ":party_no", ":center_no"),
                  (lt, ":distance", ":max_travel_distance"),
				  #gekokujo 3.0 integrating motomataru's campaign AI end
                  
                  (try_begin),
                    (ge, ":most_threatened_center", 0),
                    (store_distance_to_party_from_party, reg13, ":center_no", ":most_threatened_center"),
                  (else_try),  
                    (assign, reg13, 0),
                  (try_end),

                  (store_sub, reg11, reg13, reg12),                
                  (lt, reg11, 40),                
                  
                  (val_sub, ":random_center_no", 1),
                  (eq, ":random_center_no", 0),
                  (assign, ":best_center_to_travel", ":center_no"),
                (try_end),
              (try_end),                            
            (try_end),
          (try_end),  
          
          (assign, ":travel_target", ":best_center_to_travel"),          
          (assign, ":travel_target_new_assigned", 1),
        (try_end),
      (else_try),
        #if party has an ai object and they are close to that object while gathering army, 
        #forget that ai object so they will select a new ai object next.
        (is_between, ":old_ai_object", centers_begin, centers_end),
		#gekokujo 3.0 integrating motomataru's campaign AI start
        #(party_get_position, pos1, ":party_no"),
        #(party_get_position, pos2, ":old_ai_object"),
        #(get_distance_between_positions, ":dist", pos1, pos2),
        #(le, ":dist", 3),
		(store_distance_to_party_from_party, ":distance", ":party_no", ":old_ai_object"),
        (le, ":distance", 3),
		#gekokujo 3.0 integrating motomataru's campaign AI end
        (assign, ":travel_target", -1),
      (try_end),
      #end ozan
     
      (try_begin),
        (eq, ":travel_target", -1),
        (assign, ":action", spai_undefined),
      (else_try),
        (assign, ":action", spai_visiting_village),
      (try_end),
     
      (assign, ":object", ":travel_target"),
     
      (try_begin),
        (eq, ":troop_no", "$g_talk_troop"),
        (try_begin),
          (eq, ":travel_target", -1),
          (str_store_string, s14, "str_as_the_marshall_i_am_assembling_the_army_of_the_realm"),
        (else_try),
          (try_begin),
            (eq, ":faction_no", "$players_kingdom"),
            (eq, ":travel_target_new_assigned", 1),
            (le, "$number_of_report_to_army_quest_notes", 13),
            (check_quest_active, "qst_report_to_army"),            
            (str_store_party_name_link, s10, ":travel_target"),                        
            
            (faction_get_slot, ":faction_marshal", ":faction_no", slot_faction_marshall), #300
            
            (str_store_troop_name_link, s11, ":faction_marshal"),
            (store_current_hours, ":hours"),
            (call_script, "script_game_get_date_text", 0, ":hours"),

            (str_store_string, s14, "str_as_the_marshall_i_am_assembling_the_army_of_the_realm_and_travel_to_lands_near_s10_to_inform_more_vassals"),
            (str_store_string, s14, "@({s1}) {s11}: {s14}"),         
            (add_quest_note_from_sreg, "qst_report_to_army", "$number_of_report_to_army_quest_notes", s14, 0),
            (val_add, "$number_of_report_to_army_quest_notes", 1),
          (try_end),  

          (assign, reg0, ":travel_target"),
          (str_store_party_name, s10, ":travel_target"),
          (str_store_string, s14, "str_as_the_marshall_i_am_assembling_the_army_of_the_realm_and_travel_to_lands_near_s10_to_inform_more_vassals"),
        (try_end),
        (str_store_string, s16, "str_i_intend_to_assemble_the_army_of_the_realm"),
      (try_end),      		 
	(else_try),
	  (faction_slot_eq, ":faction_no", slot_faction_marshall, ":troop_no"),
	  (faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_attacking_center),
	  (faction_get_slot, ":faction_object", ":faction_no", slot_faction_ai_object),
	  
	  (assign, ":action", spai_besieging_center),
	  (assign, ":object", ":faction_object"),
	  (try_begin),
	    (eq, ":troop_no", "$g_talk_troop"),
	    (str_store_string, s14, "str_as_the_marshall_i_am_leading_the_siege"),
	    (str_store_string, s16, "str_i_intend_to_begin_the_siege"),
	  (try_end),
	
	(else_try),
	  (faction_slot_eq, ":faction_no", slot_faction_marshall, ":troop_no"),
	  (faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_raiding_village),
	  (faction_get_slot, ":faction_object", ":faction_no", slot_faction_ai_object),
	    
	  (assign, ":action", spai_raiding_around_center),
	  (assign, ":object", ":faction_object"),
	  (try_begin),
	    (eq, ":troop_no", "$g_talk_troop"),
	    (str_store_string, s14, "str_as_the_marshall_i_am_leading_our_raid"),
	    (str_store_string, s16, "str_i_intend_to_start_our_raid"),
	  (try_end),
	
	(else_try),
	  (faction_slot_eq, ":faction_no", slot_faction_marshall, ":troop_no"),
	  (faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_attacking_enemies_around_center),
	  (faction_get_slot, ":faction_object", ":faction_no", slot_faction_ai_object),
	  (party_is_active, ":faction_object"),
	  
	  #moved (party_set_ai_initiative, ":party_no", 10), #new to avoid losing time of marshal with attacking unimportant targets while there is a threat in our centers.
	  
	  #gekokujo 3.0 integrating motomataru's campaign AI start
	  #(party_get_battle_opponent, ":besieger_party", ":faction_object"),
	  #
	  #(try_begin),
	  #  (gt, ":besieger_party", 0),
      #  (party_is_active, ":besieger_party"),
	  #  
	  #  (assign, ":action", spai_engaging_army),
	  #  (assign, ":object", ":besieger_party"),
	  #  (try_begin),
      #    (eq, ":troop_no", "$g_talk_troop"),
      #    (str_store_string, s14, "str_as_the_marshall_i_am_leading_our_forces_to_engage_the_enemy_in_battle"),
      #    (str_store_string, s16, "str_i_intend_to_lead_our_forces_out_to_engage_the_enemy"),
      #  (try_end),
      #(else_try),      
	  #gekokujo 3.0 integrating motomataru's campaign AI end
        (assign, ":action", spai_patrolling_around_center),                
        (assign, ":object", ":faction_object"),
        (try_begin),
          (eq, ":troop_no", "$g_talk_troop"),
          (str_store_string, s14, "str_as_the_marshall_i_am_leading_our_forces_in_search_of_the_enemy"),
          (str_store_string, s16, "str_i_intend_to_lead_our_forces_out_to_find_the_enemy"),
        (try_end),
      #(try_end),  #gekokujo 3.0 integrating motomataru's campaign AI
      
    (else_try),
      (faction_slot_eq, ":faction_no", slot_faction_marshall, ":troop_no"),
      (faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_attacking_enemy_army),
      (faction_get_slot, ":faction_object", ":faction_no", slot_faction_ai_object),
      (party_is_active, ":faction_object"),
      
      (assign, ":action", spai_engaging_army),
      (assign, ":object", ":faction_object"),
      (try_begin),
        (eq, ":troop_no", "$g_talk_troop"),
        (str_store_string, s14, "str_as_the_marshall_i_am_leading_our_forces_to_engage_the_enemy_in_battle"),
        (str_store_string, s16, "str_i_intend_to_lead_our_forces_out_to_engage_the_enemy"),
      (try_end),
		
	#Get reinforcements		
	#gekokujo 3.0 integrating motomataru's campaign AI start
	#(else_try),
	#  (assign, ":lowest_acceptable_strength_percentage", 30),
	#  
	#  #if troop has enought gold then increase by 10%
	#  #(troop_get_slot, ":cur_wealth", ":troop_no", slot_troop_wealth),            
	#  #(try_begin),
	#  #  (ge, ":cur_wealth", 2000),
	#  #  (assign, ":wealth_addition", 10),
	#  #(else_try),  
	#  #  (store_div, ":wealth_addition", ":cur_wealth", 200),
	#  #(try_end),
	#  #(val_add, ":lowest_acceptable_strength_percentage", ":wealth_addition"),
	#  
	#  (call_script, "script_lord_get_home_center", ":troop_no"),
	#  (assign, ":home_center", reg0),
	#  (gt, ":home_center", -1),
	#  (party_slot_eq, ":home_center", slot_town_lord, ":troop_no"), #newly added
	#  
	#  #if troop is very close to its home center increase by 20%
	#  (assign, ":distance_addition", 0),
	#  (party_get_position, pos0, ":home_center"),
	#  (party_get_position, pos1, ":party_no"),
	#  (get_distance_between_positions, ":dist", pos0, pos1),	  	  
	#  	  
	#  (try_begin),	  
	#    (le, ":dist", 9000),
	#    (store_div, ":distance_addition", ":dist", 600),
	#    (store_sub, ":distance_addition", 15, ":distance_addition"),
	#  (else_try),
	#    (assign, ":distance_addition", 0),
	#  (try_end),
	#  (val_add, ":lowest_acceptable_strength_percentage", ":distance_addition"),
	#  
	#  #if there is no campaign for faction increase by 35%
	#  (assign, ":no_campaign_addition", 35),
	#  (try_begin),
	#    (this_or_next|faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_attacking_enemy_army),
	#    (this_or_next|faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_attacking_enemies_around_center),
	#    (this_or_next|faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_raiding_village),
	#    (this_or_next|faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_attacking_center),
	#    (faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_gathering_army),
	#    (assign, ":no_campaign_addition", 0),
	#    
	#    #If marshal is player itself and if there is a campaign then lower lowest_acceptable_strength_percentage by 10 instead of not changing it.
	#    #Because players become confused when they see very less participation from AI lords to their campaigns.
	#    (try_begin), #400
	#      (faction_slot_eq, ":faction_no", slot_faction_marshall, "trp_player"),
	#      (game_get_reduce_campaign_ai, ":reduce_campaign_ai"),
	#      (try_begin),
	#        (eq, ":reduce_campaign_ai", 0), #hard
	#        (assign, ":no_campaign_addition", 0),
	#      (else_try),  
	#        (eq, ":reduce_campaign_ai", 1), #medium
	#        (assign, ":no_campaign_addition", -10),
	#      (else_try),  
	#        (eq, ":reduce_campaign_ai", 2), #easy
	#        (assign, ":no_campaign_addition", -15),
	#      (try_end),  
	#    (try_end),
	#  (try_end),
	#  (val_add, ":lowest_acceptable_strength_percentage", ":no_campaign_addition"),
	#  (val_max, ":lowest_acceptable_strength_percentage", 25),
	#
	#  #max : 30%+15%+35% = 80% (happens when there is no campaign and player is near to its home center.)
	#  (lt, ":party_strength_as_percentage_of_ideal", ":lowest_acceptable_strength_percentage"),
	#  
	#  (try_begin),
	#    (store_div, ":lowest_acceptable_strength_percentage_div_3", ":lowest_acceptable_strength_percentage", 3),
	#    (ge, ":party_strength_as_percentage_of_ideal", ":lowest_acceptable_strength_percentage_div_3"),
	#    (troop_get_slot, ":troop_wealth", ":troop_no", slot_troop_wealth), 
	#    (le, ":troop_wealth", 1800),
	#    (assign, ":do_only_collecting_rents", 1),
	#  (try_end),
	#  	  	  
	#  (assign, ":action", spai_holding_center),
	#  (assign, ":object", ":home_center"),
	#  
	#  (try_begin),
	#    (eq, ":troop_no", "$g_talk_troop"),
	#    (str_store_string, s14, "str_i_dont_have_enough_troops_and_i_need_to_get_some_more"),
	#    	    
	#    (str_store_string, s16, "str_i_am_running_low_on_troops"),
	#  (try_end),
	#  
	#  (eq, ":do_only_collecting_rents", 0),
	#gekokujo 3.0 integrating motomataru's campaign AI end
	
	#follow player orders
	(else_try),
	  #(eq, ":do_only_collecting_rents", 0), #gekokujo 3.0 integrating motomataru's campaign AI
	  (party_slot_ge, ":party_no", slot_party_following_orders_of_troop, "trp_kingdom_heroes_including_player_begin"),
	  
	  (party_get_slot, ":orders_type", ":party_no", slot_party_orders_type),
	  (party_get_slot, ":orders_object", ":party_no", slot_party_orders_object),
	  (party_get_slot, ":orders_time", ":party_no", slot_party_orders_time),
	  
	  (ge, ":orders_object", 0),
	  
	  (store_current_hours, ":hours_since_orders_given"),
	  (val_sub, ":hours_since_orders_given", ":orders_time"),
     ##diplomacy start+ If the player set the Centralization value, modify the
     #maximum time vassals will follow commands by a maximum of +/- 25%
     #(normally the maximum is 48 hours, so that would be +/- 12 hours).
     (store_mul, reg0, ":centralization", 4),
     (val_clamp, reg0, -12, 12),#<-- This should be unnecessary
     (val_sub, ":hours_since_orders_given", reg0),
     ##diplomacy end+
	  
	  (party_is_active, ":orders_object"),
	  (party_get_slot, ":object_state", ":orders_object", slot_village_state),
	  (store_faction_of_party, ":object_faction", ":orders_object"),	  
	  (store_relation, ":relation_with_object", ":faction_no", ":object_faction"),
	  
	  (assign, ":orders_are_appropriate", 1),
	  (try_begin),
	    (gt, ":hours_since_orders_given", 48),
	    (assign, ":orders_are_appropriate", 0),
	  (else_try),
	    (eq, ":orders_type", spai_raiding_around_center),
	    (this_or_next|ge, ":relation_with_object", 0),
	    (ge, ":object_state", 2),
	    (assign, ":orders_are_appropriate", 0),
	  (else_try),
	    (eq, ":orders_type", spai_besieging_center),
	    (ge, ":relation_with_object", 0),
	    (assign, ":orders_are_appropriate", 0),
	  (else_try),
	    (this_or_next|eq, ":orders_type", spai_holding_center),
	    (this_or_next|eq, ":orders_type", spai_retreating_to_center),
	    (this_or_next|eq, ":orders_type", spai_accompanying_army),
	    (eq, ":orders_type", spai_visiting_village),
	    (le, ":relation_with_object", 0),
	    (assign, ":orders_are_appropriate", 0),
	  (try_end),
	  
	  (eq, ":orders_are_appropriate", 1),
	  
	  (assign, ":action", ":orders_type"),
	  (assign, ":object", ":orders_object"),
	  (try_begin),
	    (eq, ":troop_no", "$g_talk_troop"),
	    (str_store_string, s14, "str_we_are_following_your_direction"),
	  (try_end),
		
	#Host of player wedding
	(else_try),
	  #(eq, ":do_only_collecting_rents", 0), #gekokujo 3.0 integrating motomataru's campaign AI
	  (eq, ":operation_in_progress", 0),
	  (check_quest_active, "qst_wed_betrothed"),
	  (quest_slot_eq, "qst_wed_betrothed", slot_quest_giver_troop, ":troop_no"),
	  (quest_get_slot, ":bride", "qst_wed_betrothed", slot_quest_target_troop),
	  (call_script, "script_get_kingdom_lady_social_determinants", ":bride"),
	  #gekokujo 3.0 integrating motomataru's campaign AI start
	  #(assign, ":wedding_venue", reg1),
	  (assign, ":center_to_visit", reg1),
	  (is_between, ":center_to_visit", walled_centers_begin, walled_centers_end),	#MOTO avoid bug
	  #gekokujo 3.0 integrating motomataru's campaign AI end
	  
	  (assign, ":action", spai_holding_center),
	  #(assign, ":object", ":wedding_venue"), #gekokujo 3.0 integrating motomataru's campaign AI
	  (assign, ":object", ":center_to_visit"),
	  
	  (try_begin),
	    (eq, ":troop_no", "$g_talk_troop"),
	    (str_store_string, s14, "str_i_need_to_make_preparations_for_your_wedding"),
	    (str_store_string, s16, "str_after_all_i_need_to_make_preparations_for_your_wedding"),
	  (try_end),
	
	#Bridegroom at player wedding
	(else_try),
	  #(eq, ":do_only_collecting_rents", 0), #gekokujo 3.0 integrating motomataru's campaign AI
	  (eq, ":operation_in_progress", 0),
	  (check_quest_active, "qst_wed_betrothed_female"),
	  (quest_slot_eq, "qst_wed_betrothed_female", slot_quest_giver_troop, ":troop_no"),
	  
	  (faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_feast),
	  #gekokujo 3.0 integrating motomataru's campaign AI start
	  #(faction_get_slot, ":feast_venue", ":faction_no", slot_faction_ai_object),
	  (faction_get_slot, ":center_to_visit", ":faction_no", slot_faction_ai_object),
	  (is_between, ":center_to_visit", walled_centers_begin, walled_centers_end),	#MOTO avoid bug
	  #gekokujo 3.0 integrating motomataru's campaign AI end
	  
	  (assign, ":action", spai_holding_center),
	  #(assign, ":object", ":feast_venue"), #gekokujo 3.0 integrating motomataru's campaign AI
	  (assign, ":object", ":center_to_visit"),
	  
	  (try_begin),
	    (eq, ":troop_no", "$g_talk_troop"),
	    (str_store_string, s14, "str_i_am_heading_to_the_site_of_our_wedding"), #500
	    (str_store_string, s16, "str_after_all_we_are_soon_to_be_wed"),
	  (try_end),
 	
	#Host of other feast
	(else_try),
	  #(eq, ":do_only_collecting_rents", 0), #gekokujo 3.0 integrating motomataru's campaign AI
	  (eq, ":operation_in_progress", 0),
	  (faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_feast),
	  #gekokujo 3.0 integrating motomataru's campaign AI start
	  #(faction_get_slot, ":feast_venue", ":faction_no", slot_faction_ai_object),
	  #(party_slot_eq, ":feast_venue", slot_town_lord, ":troop_no"),
	  (faction_get_slot, ":center_to_visit", ":faction_no", slot_faction_ai_object),
	  (is_between, ":center_to_visit", walled_centers_begin, walled_centers_end),	#MOTO avoid bug
	  (party_slot_eq, ":center_to_visit", slot_town_lord, ":troop_no"),
	  #gekokujo 3.0 integrating motomataru's campaign AI end
	  
	  (assign, ":action", spai_holding_center),
	  #(assign, ":object", ":feast_venue"), #gekokujo 3.0 integrating motomataru's campaign AI
	  (assign, ":object", ":center_to_visit"),
	  
	  (try_begin),
	    (eq, ":troop_no", "$g_talk_troop"),
	    (str_store_string, s14, "str_i_am_hosting_a_feast_there"),
	    (str_store_string, s16, "str_i_have_a_feast_to_host"),
	  (try_end),
		
	#I am the bridegroom at a feast
	(else_try),
	  #(eq, ":do_only_collecting_rents", 0), #gekokujo 3.0 integrating motomataru's campaign AI
	  (eq, ":operation_in_progress", 0),
	  (faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_feast),
	  #gekokujo 3.0 integrating motomataru's campaign AI start
	  #(troop_get_slot, ":troop_betrothed", ":troop_no", slot_troop_betrothed),
	  #(is_between, ":troop_betrothed", kingdom_ladies_begin, kingdom_ladies_end),
	  #
	  #(faction_get_slot, ":feast_venue", ":faction_no", slot_faction_ai_object),
	  (troop_get_slot, reg0, ":troop_no", slot_troop_betrothed),
	  (is_between, reg0, kingdom_ladies_begin, kingdom_ladies_end),
	  
	  (faction_get_slot, ":center_to_visit", ":faction_no", slot_faction_ai_object),
	  (is_between, ":center_to_visit", walled_centers_begin, walled_centers_end),	#MOTO avoid bug
	  #gekokujo 3.0 integrating motomataru's campaign AI end
	  
	  (assign, ":action", spai_holding_center),
	  #(assign, ":object", ":feast_venue"), #gekokujo 3.0 integrating motomataru's campaign AI
	  (assign, ":object", ":center_to_visit"),
	  
	  (try_begin),
	    (eq, ":troop_no", "$g_talk_troop"),
	    (str_store_string, s14, "str_i_am_to_be_the_bridegroom_there"),
	    (str_store_string, s16, "str_my_wedding_day_draws_near"),
	  (try_end),
	  
	#Drop off prisoners
	(else_try),
	  #(eq, ":do_only_collecting_rents", 0), #gekokujo 3.0 integrating motomataru's campaign AI
	  (gt,  ":party_ratio_of_prisoners", 35),
	  (eq, ":operation_in_progress", 0),
	  
	  (call_script, "script_lord_get_home_center", ":troop_no"),
	  #(assign, ":home_center", reg0), #gekokujo 3.0 integrating motomataru's campaign AI
	  (assign, ":center_to_visit", reg0),
	  
	  #(gt, ":home_center", -1), #gekokujo 3.0 integrating motomataru's campaign AI
	  (gt, ":center_to_visit", -1),
	  
	  (assign, ":action", spai_holding_center),
	  #(assign, ":object", ":home_center"), #gekokujo 3.0 integrating motomataru's campaign AI
	  (assign, ":object", ":center_to_visit"),
	  
	  (try_begin),
	    (eq, ":troop_no", "$g_talk_troop"),
	    (str_store_string, s14, "str_i_have_too_much_loot_and_too_many_prisoners_and_need_to_secure_them"),
	    (str_store_string, s16, "str_i_should_think_of_dropping_off_some_of_my_prisoners"),
	  (try_end),
	
	#Reinforce a weak center		
	(else_try),
	  #(eq, ":do_only_collecting_rents", 0), #gekokujo 3.0 integrating motomataru's campaign AI
	  #gekokujo 3.0 integrating motomataru's campaign AI start
	  #(assign, ":center_to_reinforce", -1),
	  #(assign, ":center_reinforce_score", 100),
	  #(eq, ":operation_in_progress", 0),
	  #
	  #(try_for_range, ":walled_center", walled_centers_begin, walled_centers_end),
	  #  (party_slot_eq, ":walled_center", slot_town_lord, ":troop_no"),
	  #  (party_get_slot, ":center_strength", ":walled_center", slot_party_cached_strength),
	  #  (lt, ":center_strength", ":center_reinforce_score"),
	  #  (assign, ":center_to_reinforce", ":walled_center"),
	  #  (assign, ":center_reinforce_score", ":center_strength"),
	  #(try_end),
	  (assign, ":center_to_visit", -1),
	  (assign, ":score_to_beat", 100),
	  (eq, ":operation_in_progress", 0),
	  
	  (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
	    (party_slot_eq, ":center_no", slot_town_lord, ":troop_no"),
	    # (party_get_slot, ":center_strength", ":walled_center", slot_party_cached_strength),	MOTO base on number of troops
	    (store_party_size_wo_prisoners, ":center_strength", ":center_no"),	#MOTO base on number of troops
		
		#MOTO add condition to limit size of prospective garrison
		#players complaining about huge armies sitting in a center
		#garrison limit from levy above
		(party_get_slot, ":center_max_garrison", ":center_no", slot_town_prosperity),
		(val_mul, ":center_max_garrison", 6),
		(val_add, ":center_max_garrison", 100),	#100..700, average 400
		(store_add, reg0, ":center_strength", ":party_fit_for_battle"),
		(lt, reg0, ":center_max_garrison"),
		#MOTO end add condition to limit size of prospective garrison

	    (lt, ":center_strength", ":score_to_beat"),
	    (assign, ":center_to_visit", ":center_no"),
	    (assign, ":score_to_beat", ":center_strength"),
	  (try_end),
	  #gekokujo 3.0 integrating motomataru's campaign AI end
	  
	  #(gt, ":center_to_reinforce", -1), #gekokujo 3.0 integrating motomataru's campaign AI
	  (gt, ":center_to_visit", -1),
	  
	  (assign, ":action", spai_holding_center),
	  #(assign, ":object", ":center_to_reinforce"), #gekokujo 3.0 integrating motomataru's campaign AI
	  (assign, ":object", ":center_to_visit"),
	  (try_begin),
	    (eq, ":troop_no", "$g_talk_troop"),
	    (str_store_string, s14, "str_i_need_to_reinforce_it_as_it_is_poorly_garrisoned"),
	    (str_store_string, s16, "str_there_is_a_hole_in_our_defenses"),
	  (try_end),

	#Continue screening, if already doing so
	(else_try),	
	  #(eq, ":do_only_collecting_rents", 0), #gekokujo 3.0 integrating motomataru's campaign AI start
	  #gekokujo 3.0 integrating motomataru's campaign AI start
	  #(eq, ":old_ai_state", spai_screening_army), #566
	  (eq, ":old_ai_state", spai_accompanying_army),
      (party_slot_eq, ":party_no", slot_party_ai_substate, 1),
	  #gekokujo 3.0 integrating motomataru's campaign AI end
	  
	  (faction_get_slot, ":faction_marshal", ":faction_no", slot_faction_marshall),
          (ge, ":faction_marshal", 0),
	  (troop_get_slot, ":marshal_party", ":faction_marshal", slot_troop_leaded_party),
	  (party_is_active, ":marshal_party"),
	  
	  (call_script, "script_npc_decision_checklist_troop_follow_or_not", ":troop_no"),
	  (eq, reg0, 1),
	  
	  (assign, ":action", spai_screening_army),
	  (assign, ":object", ":marshal_party"),
	  (try_begin),
	    (eq, "$g_talk_troop", ":troop_no"),
	    (str_store_string, s14, "str_i_am_following_the_marshals_orders"),
	    (str_store_string, s16, "str_the_marshal_has_given_me_this_command"),
	  (try_end),
		
    (else_try), #special case for sfai_attacking_enemies_around_center for village raids
      (faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_attacking_enemies_around_center),
      (is_between, ":faction_object", villages_begin, villages_end),
      
      (call_script, "script_npc_decision_checklist_troop_follow_or_not", ":troop_no"),
	  (this_or_next|faction_slot_eq, ":faction_no",  slot_faction_marshall, -1), #gekokujo 3.0 integrating motomataru's campaign AI
      (eq, reg0, 1),
      
      (faction_get_slot, ":faction_object", ":faction_no", slot_faction_ai_object),
      (party_get_slot, ":raider_party", ":faction_object", slot_village_raided_by),
      (party_is_active, ":raider_party"),
      
      #think about adding one more condition here, what if raider army is so powerfull, again lords will go and engage enemy one by one?
      (party_get_slot, ":enemy_strength_nearby", ":faction_object", slot_center_sortie_enemy_strength),
      #(lt, ":enemy_strength_nearby", 4000), #gekokujo 3.0 integrating motomataru's campaign AI
	  (lt, ":enemy_strength_nearby", ":party_cached_strength"),	#MOTO compare to party's own strength
      #end think
      
      (assign, ":action", spai_engaging_army),
      (assign, ":object", ":raider_party"),
      (try_begin),
        (eq, ":troop_no", "$g_talk_troop"),
        (str_store_string, s14, "str_our_realm_needs_my_support_there_is_enemy_raiding_one_of_our_villages_which_is_not_to_far_from_here_i_am_going_there"),
        (str_store_string, s16, "str_the_marshal_has_issued_a_summons"),
      (try_end),
      						
	#Follow the marshall's orders - if on the offensive, and the campaign has not lasted too long. Readiness is currently randomly set
	(else_try),	
	  #(eq, ":do_only_collecting_rents", 0), #gekokujo 3.0 integrating motomataru's campaign AI
	  #gekokujo 3.0 integrating motomataru's campaign AI start
	  #(call_script, "script_npc_decision_checklist_troop_follow_or_not", ":troop_no"),
	  #(eq, reg0, 1),
	  #gekokujo 3.0 integrating motomataru's campaign AI end
	  
	  (faction_get_slot, ":faction_marshal", ":faction_no", slot_faction_marshall),
          (ge, ":faction_marshal", 0),
	  (troop_get_slot, ":marshal_party", ":faction_marshal", slot_troop_leaded_party),
	  
	  #gekokujo 3.0 integrating motomataru's campaign AI start
	  (call_script, "script_npc_decision_checklist_troop_follow_or_not", ":troop_no"),
	  (eq, reg0, 1),
	  #gekokujo 3.0 integrating motomataru's campaign AI end
	  
	  (assign, ":action", spai_accompanying_army),
	  (assign, ":object", ":marshal_party"),
	  	  	  
	  (try_begin),
	    (eq, "$g_talk_troop", ":troop_no"),
	    (str_store_string, s14, "str_i_am_answering_the_marshals_summons"),
	    (str_store_string, s16, "str_the_marshal_has_issued_a_summons"),
	  (try_end),
	  
	#Support a nearby ally who is on the offensive		
	(else_try),	
	  #(eq, ":do_only_collecting_rents", 0), #gekokujo 3.0 integrating motomataru's campaign AI
	  (eq, ":faction_is_at_war", 1),
	  
	  (assign, ":party_to_support", -1),
	  (try_for_range, ":allied_hero", active_npcs_begin, active_npcs_end),
	    (troop_slot_eq, ":allied_hero", slot_troop_occupation, slto_kingdom_hero),
	    (store_faction_of_troop, ":allied_hero_faction", ":allied_hero"),
	    (eq, ":allied_hero_faction", ":faction_no"),
	  
	    (neq, ":allied_hero", ":troop_no"),
	  
	    (troop_get_slot, ":allied_hero_party", ":allied_hero", slot_troop_leaded_party),
	    (gt, ":allied_hero_party", 1),
	    (party_is_active, ":allied_hero_party"),
		
	  
	    (this_or_next|party_slot_eq, ":allied_hero_party", slot_party_ai_state, spai_raiding_around_center),
			(party_slot_eq, ":allied_hero_party", slot_party_ai_state, spai_besieging_center),
	  
	    (call_script, "script_troop_get_relation_with_troop", ":troop_no", ":allied_hero"),
		#gekokujo 3.0 integrating motomataru's campaign AI start
	    #(gt, reg0, 4),
		(store_div, ":relation", reg0, 4),	#MOTO make variable
		(gt, ":relation", 1),	#MOTO make variable
		#gekokujo 3.0 integrating motomataru's campaign AI end
	  
	    (troop_get_slot, ":troop_renown", ":troop_no", slot_troop_renown),		
	    (troop_get_slot, ":ally_renown", ":allied_hero", slot_troop_renown),		
	    (le, ":troop_renown", ":ally_renown"), #Ally to support must have higher renown
	  
	    (store_distance_to_party_from_party, ":distance", ":party_no", ":allied_hero_party"),
	  
	    #gekokujo 3.0 integrating motomataru's campaign AI start
		#(lt, ":distance", 5),
		(lt, ":distance", ":relation"),	#MOTO make variable
		#gekokujo 3.0 integrating motomataru's campaign AI end
	  
 	    (assign, ":party_to_support", ":allied_hero_party"),
	  (try_end),
	  (gt, ":party_to_support", 0),
	  	  
	  (assign, ":action", spai_accompanying_army),
	  (assign, ":object", ":party_to_support"),
	  (try_begin),
		  (eq, ":troop_no", "$g_talk_troop"),
		  (party_stack_get_troop_id, ":leader", ":object", 0),
		  (str_store_troop_name, s10, ":leader"),
		  
		  (call_script, "script_troop_get_family_relation_to_troop", ":leader", "$g_talk_troop"),
		  (try_begin),
		    (eq, reg0, 0),
		    (str_store_string, s11, "str_comradeinarms"),
		  (try_end),
		  (str_store_string, s14, "str_i_am_supporting_my_s11_s10"),
		  (str_store_string, s16, "str_i_believe_that_one_of_my_comrades_is_in_need"),
	  (try_end),
    #I have decided to attack a vulnerable fortress
	(else_try),	
	  #(eq, ":do_only_collecting_rents", 0), #gekokujo 3.0 integrating motomataru's campaign AI
	  (eq, ":faction_is_at_war", 1),
	  (eq, ":operation_in_progress", 0),
	  
	  #gekokujo 3.0 integrating motomataru's campaign AI start
	  #(assign, ":walled_center_to_attack", -1),
	  #(assign, ":walled_center_score", 50),
	  #
	  #(try_for_range, ":walled_center", walled_centers_begin, walled_centers_end),
	  #  (store_faction_of_party, ":walled_center_faction", ":walled_center"),
	  #  (store_relation, ":relation", ":faction_no", ":walled_center_faction"),
	  #  (lt, ":relation", 0),
	  #  
	  #  (party_get_slot, ":center_cached_strength", ":walled_center", slot_party_cached_strength),
	  #  (val_mul, ":center_cached_strength", 3),
	  #  (val_mul, ":center_cached_strength", 2),
	  #  
	  #  (lt, ":center_cached_strength", ":party_cached_strength"), 
	  #  (lt, ":center_cached_strength", 750),
	  #  
	  #  (party_slot_eq, ":walled_center", slot_village_state, svs_normal),
	  #  (store_distance_to_party_from_party, ":distance", ":walled_center", ":party_no"),
	  #  (lt, ":distance", ":walled_center_score"),
	  #  
	  #  (assign, ":walled_center_to_attack", ":walled_center"),
	  #  (assign, ":walled_center_score", ":distance"),
	  #(try_end),
	  (assign, ":target_center", -1),
	  (assign, ":score_to_beat", 50),
	  
	  (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
	    (store_faction_of_party, ":center_faction", ":center_no"),
	    (store_relation, ":relation", ":faction_no", ":center_faction"),
	    (lt, ":relation", 0),
	    
	    (party_get_slot, ":center_strength", ":center_no", slot_party_cached_strength),
	    (val_mul, ":center_strength", 3),
	    (val_mul, ":center_strength", 2),
	    
	    (lt, ":center_strength", ":party_cached_strength"), 
	    # (lt, ":center_strength", 750),
	    (lt, ":center_strength", 3000),	#MOTO this is about 100 troops (with defense bonus)
	    
	    (party_slot_eq, ":center_no", slot_village_state, svs_normal),
	    (store_distance_to_party_from_party, ":distance", ":center_no", ":party_no"),
	    (lt, ":distance", ":score_to_beat"),
	    
	    (assign, ":target_center", ":center_no"),
	    (assign, ":score_to_beat", ":distance"),
	  (try_end),
	  #gekokujo 3.0 integrating motomataru's campaign AI end
	  
	  #(is_between, ":walled_center_to_attack", centers_begin, centers_end), #gekokujo 3.0 integrating motomataru's campaign AI
	  (is_between, ":target_center", centers_begin, centers_end),
	  
	  (assign, ":action", spai_besieging_center),
	  #(assign, ":object", ":walled_center_to_attack"), #gekokujo 3.0 integrating motomataru's campaign AI
	  (assign, ":object", ":target_center"),
	  (try_begin),
	    (eq, "$cheat_mode", 1),
	    (str_store_faction_name, s20, ":faction_no"),
	    (str_store_party_name, s21, ":object"),
	    (display_message, "str_s20_decided_to_attack_s21"),
	  (try_end),
	  
	  (try_begin),
	    (eq, ":troop_no", "$g_talk_troop"),
	    (str_store_string, s14, "str_a_fortress_is_vulnerable"),
	    (str_store_string, s16, "str_i_believe_that_the_enemy_may_be_vulnerable"),
	  (try_end),
	  
	#I am visiting an estate
	(else_try),
	  #gekokujo 3.0 integrating motomataru's campaign AI start
	  #(assign, ":center_to_visit", -1),
	  #(assign, ":score_to_beat", 300), #at least 300 gold to pick up
	  #(troop_get_slot, ":troop_wealth", ":troop_no", slot_troop_wealth), #average troop wealth is 2000
	  #(val_div, ":troop_wealth", 10), #average troop wealth 10% is is 200
	  #(val_add, ":score_to_beat", ":troop_wealth"), #average score to beat is 500
	  #gekokujo 3.0 integrating motomataru's campaign AI end
	  (eq, ":operation_in_progress", 0),	  	  
	  	  
	  #gekokujo 3.0 integrating motomataru's campaign AI start
      #MOTO collect rents only when it actually helps recruit
	  # (assign, ":score_to_beat", 300),	#at least 300 gold to pick up MOTO equals reinforcement_cost_hard
	  (options_get_campaign_ai, ":reduce_campaign_ai"),
	  (try_begin), 
		(eq, ":reduce_campaign_ai", 0),	#hard
		(assign, ":score_to_beat", reinforcement_cost_hard),
	  (else_try), 
		(eq, ":reduce_campaign_ai", 2),	#easy
		(assign, ":score_to_beat", reinforcement_cost_easy),
	  (else_try), 
		(assign, ":score_to_beat", reinforcement_cost_moderate),
	  (try_end),
	  (val_mul, ":score_to_beat", 4),	# 4/3 "hiring budget" from script_hire_men_to_kingdom_hero_party
	  (val_div, ":score_to_beat", 3),
	  (troop_get_slot, ":troop_wealth", ":troop_no", slot_troop_wealth),	#average troop wealth is 2000
	  (try_begin),
		(lt, ":troop_wealth", ":score_to_beat"),	#parties that lack wealth...
		(val_div, ":score_to_beat", 2),	#...are willing to go get half of what they need
	  (else_try),	#parties with wealth are not so eager to collect more
		(val_sub, ":troop_wealth", ":score_to_beat"),	#MOTO add 10% of amount OVER what is needed
		(val_div, ":troop_wealth", 10),	#average troop wealth 10% is is 200 MOTO 160 with hard campaign AI
		(val_add, ":score_to_beat", ":troop_wealth"),	#average score to beat is 500 MOTO 560 with hard campaign AI
	  (try_end),
	  #MOTO end collect rents only when it actually helps recruit
	  #gekokujo 3.0 integrating motomataru's campaign AI end
	  
	  (try_begin),	    
	    (faction_get_slot, ":faction_marshal", ":faction_no", slot_faction_marshall),
	    (ge, ":faction_marshal", 0), #gekokujo 3.0 integrating motomataru's campaign AI
	    
	    (assign, reg17, 0),
	    (try_begin),
	      (party_slot_eq, ":party_no", slot_party_ai_state, spai_accompanying_army),
		  #gekokujo 3.0 integrating motomataru's campaign AI start
	      #(party_slot_eq, ":party_no", slot_party_ai_object, ":faction_marshal"),	    
	      (troop_get_slot, ":marshal_party", ":faction_marshal", slot_troop_leaded_party),
	      (party_is_active, ":marshal_party"),
	      (party_slot_eq, ":party_no", slot_party_ai_object, ":marshal_party"),
		  #gekokujo 3.0 integrating motomataru's campaign AI end
	      (assign, reg17, 1),
	    (else_try),  	    
	      (party_slot_eq, ":party_no", slot_party_following_player, 1),
	      (assign, reg17, 1),
	    (try_end),  
	    (eq, reg17, 1),
	    
	    (try_begin),
	      (neq, ":faction_marshal", "trp_player"),
	      (neg|party_slot_eq, ":party_no", slot_party_following_player, 1),
	      (val_add, ":score_to_beat", 125),
	    (else_try),
	      (val_add, ":score_to_beat", 250),
	    (try_end),
	  (try_end),  
	  
	  #gekokujo 3.0 integrating motomataru's campaign AI start
	  (assign, ":center_to_visit", -1),
	  #gekokujo 3.0 integrating motomataru's campaign AI end
	  
	  (try_for_range, ":center_no", centers_begin, centers_end),
	    (party_slot_eq, ":center_no", slot_town_lord, ":troop_no"),
	    
	    (assign, reg17, 0),
	    (try_begin),
	      (is_between, ":center_no", villages_begin, villages_end),
	      (party_slot_eq, ":center_no", slot_village_state, svs_normal),
	      (assign, reg17, 1),
	    (else_try),  	    
	      (party_slot_eq, ":center_no", slot_center_is_besieged_by, -1),
	      (assign, reg17, 1),
	    (try_end),	    
	    (eq, reg17, 1),
	    
	    (party_get_slot, ":tariffs_available", ":center_no", slot_center_accumulated_tariffs),
	    (party_get_slot, ":rents_available", ":center_no", slot_center_accumulated_rents),
	    (store_add, ":money_available", ":rents_available", ":tariffs_available"),
	    	    
	    (gt, ":money_available", ":score_to_beat"),
	    (assign, ":center_to_visit", ":center_no"),
	    (assign, ":score_to_beat", ":money_available"),			
	  (try_end),
	  
	  (is_between, ":center_to_visit", centers_begin, centers_end),
	  	  
	  (try_begin),
	    (is_between, ":center_to_visit", walled_centers_begin, walled_centers_end),
	    (assign, ":action", spai_holding_center),
	    (assign, ":object", ":center_to_visit"),
	  (else_try),  
        (assign, ":action", spai_visiting_village),
  	    (assign, ":object", ":center_to_visit"),
	  (try_end),
	  
	  (try_begin),
	    (eq, ":troop_no", "$g_talk_troop"),
	    (str_store_string, s14, "str_i_need_to_inspect_my_properties_and_collect_my_dues"),
	    (str_store_string, s16, "str_it_has_been_too_long_since_i_have_inspected_my_estates"),
	  (try_end),
	  
	#My men are weary, and I wish to return home
	(else_try),
	  #(eq, ":do_only_collecting_rents", 0), #gekokujo 3.0 integrating motomataru's campaign AI
	  (this_or_next|gt, ":hours_since_last_rest", 504), #Three weeks
	  (lt, ":aggressiveness", 25),	  
	  (gt, ":hours_since_last_rest", 168), #one week if aggressiveness < 25	
	  (eq, ":operation_in_progress", 0),
	  
	  (call_script, "script_lord_get_home_center", ":troop_no"),
	  #(assign, ":home_center", reg0), #gekokujo 3.0 integrating motomataru's campaign AI
	  (assign, ":center_to_visit", reg0),
	  
	  #(gt, ":home_center", -1), #gekokujo 3.0 integrating motomataru's campaign AI
	  (gt, ":center_to_visit", -1),
	  (assign, ":action", spai_holding_center),
	  #(assign, ":object", ":home_center"), #gekokujo 3.0 integrating motomataru's campaign AI
	  (assign, ":object", ":center_to_visit"),
	  
	  (try_begin),
	    (eq, ":troop_no", "$g_talk_troop"),
	    (str_store_string, s14, "str_my_men_are_weary_so_we_are_returning_home"),
	    (str_store_string, s16, "str_my_men_are_becoming_weary"),
	  (try_end),
	
	#I have a score to settle with the enemy
	(else_try),
	  #(eq, ":do_only_collecting_rents", 0), #gekokujo 3.0 integrating motomataru's campaign AI
	  (this_or_next|gt, ":hours_since_last_combat", 12),
	  (lt, ":hours_since_last_rest", 96),
	  (eq, ":operation_in_progress", 0),
	  #gekokujo 3.0 integrating motomataru's campaign AI start
      (gt, ":party_fit_for_battle", 30),	#MOTO size requirement
	  #gekokujo 3.0 integrating motomataru's campaign AI end
	  
	  (eq, ":faction_is_at_war", 1),
	  ##diplomacy start+ roguish lords can also do this, but humanitarian lords of any kind won't
	  (call_script, "script_dplmc_get_troop_morality_value", ":troop_no", tmt_humanitarian),
	  (lt, reg0, 1),
	  (this_or_next|eq, ":troop_reputation", lrep_roguish),
	  ##diplomacy end+
	  (this_or_next|eq, ":troop_reputation", lrep_debauched),
	  (eq, ":troop_reputation", lrep_quarrelsome),

	  #(assign, ":target_village", -1), #gekokujo 3.0 integrating motomataru's campaign AI
	  (assign, ":target_center", -1),
	  (assign, ":score_to_beat", 0), #based on relation
	  
	  #(try_for_range, ":possible_target", villages_begin, villages_end), #gekokujo 3.0 integrating motomataru's campaign AI
	  (try_for_range, ":center_no", villages_begin, villages_end),
	    #gekokujo 3.0 integrating motomataru's campaign AI start
	    #(store_faction_of_party, ":village_faction", ":possible_target"),
	    #(store_relation, ":relation", ":village_faction", ":faction_no"),
	    (store_faction_of_party, ":center_faction", ":center_no"),
	    (store_relation, ":relation", ":center_faction", ":faction_no"),
		#gekokujo 3.0 integrating motomataru's campaign AI end
	    (lt, ":relation", 0),
		
	    #gekokujo 3.0 integrating motomataru's campaign AI start
	    #(neg|party_slot_ge, ":possible_target", slot_village_state, svs_looted),
	    #(party_get_slot, ":town_lord", ":possible_target", slot_town_lord),
	    (neg|party_slot_ge, ":center_no", slot_village_state, svs_looted),
	    (party_get_slot, ":town_lord", ":center_no", slot_town_lord),
		#gekokujo 3.0 integrating motomataru's campaign AI end
	    (call_script, "script_troop_get_relation_with_troop", ":troop_no", ":town_lord"),
	    (assign, ":village_score", reg0),
	    
	    (lt, ":village_score", ":score_to_beat"),
	    (assign, ":score_to_beat", ":village_score"),
	    #(assign, ":target_village", ":possible_target"), #gekokujo 3.0 integrating motomataru's campaign AI
	    (assign, ":target_center", ":center_no"),
	  (try_end),
	  
	  #(is_between, ":target_village", centers_begin, centers_end), #gekokujo 3.0 integrating motomataru's campaign AI
	  (is_between, ":target_center", centers_begin, centers_end),
	  (assign, ":action", spai_raiding_around_center),
	  #(assign, ":object", ":target_village"), #gekokujo 3.0 integrating motomataru's campaign AI
	  (assign, ":object", ":target_center"),
	  
	  (try_begin),
	    (eq, ":troop_no", "$g_talk_troop"),
	    (str_store_string, s14, "str_i_have_a_score_to_settle_with_the_lord_there"),
	    (str_store_string, s16, "str_i_am_thinking_of_settling_an_old_score"),
	  (try_end),
	
	#I need money, so I am raiding where the money is
	(else_try),
	  #(eq, ":do_only_collecting_rents", 0), #gekokujo 3.0 integrating motomataru's campaign AI
	  (eq, ":faction_is_at_war", 1),
	  (eq, ":operation_in_progress", 0),
	  #gekokujo 3.0 integrating motomataru's campaign AI start
      (gt, ":party_fit_for_battle", 30),	#MOTO size requirement
	  #gekokujo 3.0 integrating motomataru's campaign AI end
	  
	  (this_or_next|gt, ":hours_since_last_combat", 12),
	  (lt, ":hours_since_last_rest", 96),
	  (gt, ":aggressiveness", 40),

	  ##diplomacy start+
	  #Roguish lords can also do this.  Humanitarian companions will never
	  #do this, even if they otherwise have an eligible reputation.  Companions
	  #who actively enjoy raiding can also do this, regardless of whether they
	  #have an eligible reputation.
	  (call_script, "script_dplmc_get_troop_morality_value", ":troop_no", tmt_humanitarian),
	  (lt, reg0, 1),
	  (this_or_next|lt, reg0, 0),
	  (this_or_next|eq, ":troop_reputation", lrep_roguish),
	  ##diplomacy end+
	  (this_or_next|eq, ":troop_reputation", lrep_debauched),
	  (this_or_next|eq, ":troop_reputation", lrep_selfrighteous),
	  (this_or_next|eq, ":troop_reputation", lrep_cunning),
	  (eq, ":troop_reputation", lrep_quarrelsome),
	  
	  #gekokujo 3.0 integrating motomataru's campaign AI start
	  #(troop_get_slot, ":wealth", ":troop_no", slot_troop_wealth),	
	  #(lt, ":wealth", 500),
	  #
	  #(assign, ":score_to_beat", 0),
	  #(assign, ":target_village", -1),
	  #
	  #(try_for_range, ":possible_target", villages_begin, villages_end),
	  #  (store_faction_of_party, ":village_faction", ":possible_target"),
	  #  (store_relation, ":relation", ":village_faction", ":faction_no"),
	  #  (lt, ":relation", 0),
	  #  
	  #  (this_or_next|party_slot_eq, ":possible_target", slot_village_state, svs_normal),
	  #  (party_slot_eq, ":possible_target", slot_village_state, svs_being_raided),
	  #  
	  #  (party_get_slot, reg17, ":possible_target", slot_town_prosperity),
	  #  (store_distance_to_party_from_party, ":distance", ":party_no", ":possible_target"),
	  #  (val_sub, reg17, ":distance"),
	  #  
	  #  (gt, reg17, ":score_to_beat"),
	  #  (assign, ":score_to_beat", reg17),
	  #  (assign, ":target_village", ":possible_target"),
	  #(try_end),
	  #
	  #(gt, ":target_village", -1),
	  #
	  #(assign, ":action", spai_raiding_around_center),
	  #(assign, ":object", ":target_village"),
	  
	  (troop_get_slot, ":troop_wealth", ":troop_no", slot_troop_wealth),	
	  (lt, ":troop_wealth", 500),
	  
	  (assign, ":score_to_beat", 0),
	  (assign, ":target_center", -1),
	  
	  #MOTO count lord's fiefs
	  (assign, ":num_centers", 0),
	  # (try_for_range, ":possible_target", villages_begin, villages_end),
	  (try_for_range, ":center_no", centers_begin, centers_end),
	    (party_get_slot, ":town_lord", ":center_no", slot_town_lord),
		(try_begin),
		  (eq, ":town_lord", ":troop_no"),
		  (val_add, ":num_centers", 1),
		(try_end),
	    (is_between, ":center_no", villages_begin, villages_end),
		#MOTO end count lord's fiefs
	    (store_faction_of_party, ":center_faction", ":center_no"),
	    (store_relation, ":relation", ":center_faction", ":faction_no"),
	    (lt, ":relation", 0),
	    
	    (this_or_next|party_slot_eq, ":center_no", slot_village_state, svs_normal),
	    (party_slot_eq, ":center_no", slot_village_state, svs_being_raided),
	    
	    (party_get_slot, reg17, ":center_no", slot_town_prosperity),
	    (store_distance_to_party_from_party, ":distance", ":party_no", ":center_no"),
	    (val_sub, reg17, ":distance"),
	    
	    (gt, reg17, ":score_to_beat"),
	    (assign, ":score_to_beat", reg17),
	    (assign, ":target_center", ":center_no"),
	  (try_end),
	  
	  (gt, ":num_centers", 0),	#MOTO a fief yields at least 1200 per week, so such a lord would not need to raid
	  (gt, ":target_center", -1),
	  
	  (assign, ":action", spai_raiding_around_center),
	  (assign, ":object", ":target_center"),
	  #gekokujo 3.0 integrating motomataru's campaign AI end
	  
	  (try_begin),
	    (eq, ":troop_no", "$g_talk_troop"),
	    (str_store_string, s14, "str_i_am_short_of_money_and_i_hear_that_there_is_much_wealth_there"),
	    (str_store_string, s16, "str_i_need_to_refill_my_purse_preferably_with_the_enemys_money"),
	  (try_end),
	
	#Attacking wealthiest lands
	(else_try),
	  #(eq, ":do_only_collecting_rents", 0),
		(eq, ":faction_is_at_war", 1),
		(eq, ":operation_in_progress", 0),
		(gt, ":aggressiveness", 65),
		#gekokujo 3.0 integrating motomataru's campaign AI start
        (gt, ":party_fit_for_battle", 30),	#MOTO size requirement
		#gekokujo 3.0 integrating motomataru's campaign AI end
	
		#gekokujo 3.0 integrating motomataru's campaign AI start
		#(assign, ":score_to_beat", 0),
		#(assign, ":target_village", -1),
		#
		#(try_for_range, ":possible_target", villages_begin, villages_end),
		#	(store_faction_of_party, ":village_faction", ":possible_target"),
		#	(store_relation, ":relation", ":village_faction", ":faction_no"),
		#	(lt, ":relation", 0),			
		#	(neg|party_slot_eq, ":possible_target", slot_village_state, svs_looted),			
		#	(party_get_slot, ":village_prosperity", ":possible_target", slot_town_prosperity),
		#	(val_mul, ":village_prosperity", 2),
		#
		#	(store_distance_to_party_from_party, ":distance", ":party_no", ":possible_target"),
		#	(val_sub, ":village_prosperity", ":distance"),			
		#	(gt, ":village_prosperity", ":score_to_beat"),
		#	
		#	(assign, ":score_to_beat", ":village_prosperity"),
		#	(assign, ":target_village", ":possible_target"),
		##(try_end),
		(assign, ":score_to_beat", 0),
		(assign, ":target_center", -1),
		
		(try_for_range, ":center_no", villages_begin, villages_end),
			(store_faction_of_party, ":center_faction", ":center_no"),
			(store_relation, ":relation", ":center_faction", ":faction_no"),
			(lt, ":relation", 0),			
			(neg|party_slot_eq, ":center_no", slot_village_state, svs_looted),			
			(party_get_slot, ":village_prosperity", ":center_no", slot_town_prosperity),
			(val_mul, ":village_prosperity", 2),

			(store_distance_to_party_from_party, ":distance", ":party_no", ":center_no"),
			(val_sub, ":village_prosperity", ":distance"),			
			(gt, ":village_prosperity", ":score_to_beat"),
			
			(assign, ":score_to_beat", ":village_prosperity"),
			(assign, ":target_center", ":center_no"),
		(try_end),
		#gekokujo 3.0 integrating motomataru's campaign AI end

		##diplomacy start+ companions who hate raiding will not raid
		(call_script, "script_dplmc_get_troop_morality_value", ":troop_no", tmt_humanitarian),
		(lt, reg0, 1),
		##diplomacy end+
		
		#(gt, ":target_village", -1), #gekokujo 3.0 integrating motomataru's campaign AI
		(gt, ":target_center", -1),
		
		(assign, ":action", spai_raiding_around_center),
		#(assign, ":object", ":target_village"),
		(assign, ":object", ":target_center"), #gekokujo 3.0 integrating motomataru's campaign AI
		
		(try_begin),
			(eq, ":troop_no", "$g_talk_troop"),
			(str_store_string, s14, "str_by_striking_at_the_enemys_richest_lands_perhaps_i_can_draw_them_out_to_battle"),
			(str_store_string, s16, "str_i_am_thinking_of_going_on_the_attack"),
		(try_end),

	#End the war
	(else_try),
	  #(eq, ":do_only_collecting_rents", 0),
	    ##diplomacy start+
		(assign, reg0, 0),
		(try_begin),
			#A liege in service to another lord or allied with the player can do this.
			(this_or_next|eq, ":troop_reputation", lrep_none),
			(this_or_next|is_between, ":troop_no", kings_begin, kings_end),
			(is_between, ":troop_no", pretenders_begin, pretenders_end),
			(this_or_next|neg|faction_slot_eq, ":faction_no", slot_faction_leader, ":troop_no"),
			(this_or_next|troop_slot_eq, ":troop_no", slot_troop_spouse, "trp_player"),
				(troop_slot_eq, "trp_player", slot_troop_spouse, ":troop_no"),
			(assign, reg0, 0),
		(else_try),
			#Lords who are simulatenously Martial and tmt_honest (such as Alayen),
			#or Custodian and tmt_honest (such as Artimenner) can also do this.
			(this_or_next|eq, ":troop_reputation", lrep_martial),
			(eq, ":troop_reputation", lrep_custodian),
			(call_script, "script_dplmc_get_troop_morality_value", ":troop_no", tmt_honest),
		(try_end),
		(this_or_next|ge, reg0, 1),
		##diplomacy end+
		(eq, ":troop_reputation", lrep_upstanding),
		(eq, ":faction_is_at_war", 1),
		(eq, ":operation_in_progress", 0),
		#gekokujo 3.0 integrating motomataru's campaign AI start
        (gt, ":party_fit_for_battle", 30),	#MOTO size requirement
		#gekokujo 3.0 integrating motomataru's campaign AI end

		(assign, ":faction_to_attack", -1),
		(try_for_range, ":possible_faction_to_attack", kingdoms_begin, kingdoms_end),
			(store_relation, ":relation", ":faction_no", ":possible_faction_to_attack"),
			(lt, ":relation", 0),
			(faction_slot_eq, ":possible_faction_to_attack", slot_faction_state, sfs_active),
			
			#gekokujo 3.0 integrating motomataru's campaign AI start
			#(store_add, ":war_damage_inflicted_slot", ":possible_faction_to_attack", slot_faction_war_damage_inflicted_on_factions_begin),
			#(val_sub, ":war_damage_inflicted_slot", kingdoms_begin),
			#(faction_get_slot, ":war_damage_inflicted", ":faction_no", ":war_damage_inflicted_slot"),
			#
			#(store_add, ":war_damage_suffered_slot", ":faction_no", slot_faction_war_damage_inflicted_on_factions_begin),
			#(val_sub, ":war_damage_suffered_slot", kingdoms_begin),
			#(faction_get_slot, ":war_damage_suffered", ":possible_faction_to_attack", ":war_damage_suffered_slot"),
			(store_add, ":slot", ":possible_faction_to_attack", slot_faction_war_damage_inflicted_on_factions_begin),
			(val_sub, ":slot", kingdoms_begin),
			(faction_get_slot, ":war_damage_inflicted", ":faction_no", ":slot"),

			(store_add, ":slot", ":faction_no", slot_faction_war_damage_inflicted_on_factions_begin),
			(val_sub, ":slot", kingdoms_begin),
			(faction_get_slot, ":war_damage_suffered", ":possible_faction_to_attack", ":slot"),
			#gekokujo 3.0 integrating motomataru's campaign AI end
			
			(gt, ":war_damage_inflicted", 80),
			(lt, ":war_damage_inflicted", ":war_damage_suffered"),
			(assign, ":faction_to_attack", ":possible_faction_to_attack"),
		(try_end),
		
		(gt, ":faction_to_attack", -1),

		#(assign, ":target_village", -1), #gekokujo 3.0 integrating motomataru's campaign AI
		(assign, ":target_center", -1),
		(assign, ":score_to_beat", 50),
		
		#gekokujo 3.0 integrating motomataru's campaign AI start
		#(try_for_range, ":possible_target_village", villages_begin, villages_end),
		#	(store_faction_of_party, ":village_faction", ":possible_target_village"),		
		#	(eq, ":village_faction", ":faction_to_attack"),			
		#	(neg|party_slot_eq, ":possible_target_village", slot_village_state, svs_looted),			
		#	(store_distance_to_party_from_party, ":distance", ":party_no", ":possible_target_village"),			
		#	(lt, ":distance", ":score_to_beat"),
		#	
		#	(assign, ":score_to_beat", ":distance"),
		#	(assign, ":target_village", ":possible_target_village"),
		#(try_end),
		#
		#(gt, ":target_village", -1),
        #
		#(assign, ":action", spai_raiding_around_center),
		#(assign, ":object", ":target_village"),
		(try_for_range, ":center_no", villages_begin, villages_end),
			(store_faction_of_party, ":center_faction", ":center_no"),		
			(eq, ":center_faction", ":faction_to_attack"),			
			(neg|party_slot_eq, ":center_no", slot_village_state, svs_looted),			
			(store_distance_to_party_from_party, ":distance", ":party_no", ":center_no"),			
			(lt, ":distance", ":score_to_beat"),
			
			(assign, ":score_to_beat", ":distance"),
			(assign, ":target_center", ":center_no"),
		(try_end),
		
		(gt, ":target_center", -1),

		(assign, ":action", spai_raiding_around_center),
		(assign, ":object", ":target_center"),
		#gekokujo 3.0 integrating motomataru's campaign AI end

		(try_begin),
			(eq, ":troop_no", "$g_talk_troop"),
			(str_store_string, s14, "str_perhaps_if_i_strike_one_more_blow_we_may_end_this_war_on_our_terms_"),
			(str_store_string, s16, "str_we_may_be_able_to_bring_this_war_to_a_close_with_a_few_more_blows"),
		(try_end),
	
	#I have a feast to attend
	(else_try),
	  #(eq, ":do_only_collecting_rents", 0),
		(faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_feast),
		#gekokujo 3.0 integrating motomataru's campaign AI start
		#(faction_get_slot, ":feast_venue", ":faction_no", slot_faction_ai_object),
		#(party_get_slot, ":feast_host", ":feast_venue", slot_town_lord), 
		(faction_get_slot, ":center_to_visit", ":faction_no", slot_faction_ai_object),
		(party_get_slot, ":town_lord", ":center_to_visit", slot_town_lord), 
	    (is_between, ":center_to_visit", walled_centers_begin, walled_centers_end),	#MOTO avoid bug
		#gekokujo 3.0 integrating motomataru's campaign AI end
		(eq, ":operation_in_progress", 0),
			
		#gekokujo 3.0 integrating motomataru's campaign AI start
		#(call_script, "script_troop_get_relation_with_troop", ":troop_no", ":feast_host"),
		#(assign, ":relation_with_host", reg0),
		#	
        #(ge, ":relation_with_host", 0),
		#
		#(assign, ":action", spai_holding_center),
		#(assign, ":object", ":feast_venue"),
		(call_script, "script_troop_get_relation_with_troop", ":troop_no", ":town_lord"),
			
        (ge, reg0, 0),
		
		(assign, ":action", spai_holding_center),
		(assign, ":object", ":center_to_visit"),
		#gekokujo 3.0 integrating motomataru's campaign AI end

		(try_begin),
			(eq, ":troop_no", "$g_talk_troop"),
			(str_store_string, s14, "str_i_wish_to_attend_the_feast_there"),
			(str_store_string, s16, "str_there_is_a_feast_which_i_wish_to_attend"),
		(try_end),		
	#A lady to court
	(else_try),
	  #(eq, ":do_only_collecting_rents", 0),
		(neg|troop_slot_eq, "trp_player", slot_troop_betrothed, ":troop_no"),
		(troop_slot_eq, ":troop_no", slot_troop_spouse, -1),
		(neg|is_between, ":troop_no", kings_begin, kings_end),
		(neg|is_between, ":troop_no", pretenders_begin, pretenders_end),

		
		(gt, ":hours_since_last_courtship", 72),
		(eq, ":operation_in_progress", 0),
		
		(assign, ":center_to_visit", -1),
		(assign, ":score_to_beat", 150),
		
		#gekokujo 3.0 integrating motomataru's campaign AI start
		#(try_for_range, ":love_interest_slot", slot_troop_love_interest_1, slot_troop_love_interests_end),
		#	(troop_get_slot, ":love_interest", ":troop_no", ":love_interest_slot"),
		#	(is_between, ":love_interest", kingdom_ladies_begin, kingdom_ladies_end),	
		#	(troop_get_slot, ":love_interest_center", ":love_interest", slot_troop_cur_center),
		#	(is_between, ":love_interest_center", centers_begin, centers_end),
		#	(store_faction_of_party, ":love_interest_faction_no", ":love_interest_center"),
		#	(eq, ":faction_no", ":love_interest_faction_no"),
        #    #(store_relation, ":relation", ":faction_no", ":love_interest_faction_no"),
        #    #(ge, ":relation", 0),
		#	
		#	(store_distance_to_party_from_party, ":distance", ":party_no", ":love_interest_center"),
		#	
		#	(lt, ":distance", ":score_to_beat"),
		#	(assign, ":center_to_visit", ":love_interest_center"),
		#	(assign, ":score_to_beat", ":distance"),			
        #(try_end),
		(try_for_range, ":slot", slot_troop_love_interest_1, slot_troop_love_interests_end),
			(troop_get_slot, ":love_interest", ":troop_no", ":slot"),
			(is_between, ":love_interest", kingdom_ladies_begin, kingdom_ladies_end),	
			(troop_get_slot, ":center_no", ":love_interest", slot_troop_cur_center),
			(is_between, ":center_no", centers_begin, centers_end),
			(store_faction_of_party, ":center_faction", ":center_no"),
			(eq, ":faction_no", ":center_faction"),
            #(store_relation, ":relation", ":faction_no", ":love_interest_faction_no"),
            #(ge, ":relation", 0),
			
			(store_distance_to_party_from_party, ":distance", ":party_no", ":center_no"),
			
			(lt, ":distance", ":score_to_beat"),
			(assign, ":center_to_visit", ":center_no"),
			(assign, ":score_to_beat", ":distance"),			
        (try_end),
		#gekokujo 3.0 integrating motomataru's campaign AI end
 
		(gt, ":center_to_visit", -1),
			
		(assign, ":action", spai_holding_center),
		(assign, ":object", ":center_to_visit"),

		(try_begin),
			(eq, ":troop_no", "$g_talk_troop"),
			(str_store_string, s14, "str_there_is_a_fair_lady_there_whom_i_wish_to_court"),
			(str_store_string, s16, "str_i_have_the_inclination_to_pay_court_to_a_fair_lady"),
		(try_end),
				
	#Patrolling an alarmed center
	(else_try),
	  #(eq, ":do_only_collecting_rents", 0), #gekokujo 3.0 integrating motomataru's campaign AI
		(assign, ":target_center", -1),
		(assign, ":score_to_beat", 60),
		(eq, ":operation_in_progress", 0),
		(gt, ":aggressiveness", 40),

		#gekokujo 3.0 integrating motomataru's campaign AI start
		#(try_for_range, ":center_to_patrol", centers_begin, centers_end), #find closest center that has spotted enemies.
        #    (store_faction_of_party, ":center_faction", ":center_to_patrol"),
        #    (eq, ":center_faction", ":faction_no"),
		#	(party_slot_ge, ":center_to_patrol", slot_center_last_spotted_enemy, 0),
		#	
		#	#new - begin
		#	(party_get_slot, ":sortie_strength", ":center_to_patrol", slot_center_sortie_strength),
		#	(party_get_slot, ":enemy_strength", ":center_to_patrol", slot_center_sortie_enemy_strength),
		#	(store_mul, ":enemy_strength_mul_14_div_10", ":enemy_strength", 14),
		#	(val_div, ":enemy_strength_mul_14_div_10", 10),
		#	(party_get_slot, ":party_strength", ":party_no", slot_party_cached_strength),
		#	
		#	(this_or_next|neg|party_is_in_town, ":party_no", ":center_to_patrol"),			
		#	(gt, ":sortie_strength", ":enemy_strength_mul_14_div_10"),
		#	
		#	(ge, ":party_strength", 100),
		#	#new - end
		#							
		#	(party_get_slot, reg17, ":center_to_patrol", slot_town_lord),						
		#	(call_script, "script_troop_get_relation_with_troop", reg17, ":troop_no"),
		#	
		#	(this_or_next|eq, ":troop_reputation", lrep_upstanding),
		#		(gt, reg0, -5),
		#	
        #    (store_distance_to_party_from_party, ":distance", ":party_no", ":center_to_patrol"),
		#	(lt, ":distance", ":score_to_beat"),
		#	
		#	(assign, ":target_center", ":center_to_patrol"),
		#	(assign, ":score_to_beat", ":distance"),
		#(try_end),
		(try_for_range, ":center_no", centers_begin, centers_end), #find closest center that has spotted enemies.
            (store_faction_of_party, ":center_faction", ":center_no"),
            (eq, ":center_faction", ":faction_no"),
			(party_slot_ge, ":center_no", slot_center_last_spotted_enemy, 0),
			
			#new - begin
			# (party_get_slot, ":sortie_strength", ":center_to_patrol", slot_center_sortie_strength),	MOTO use party_slot_ge below
			(party_get_slot, ":enemy_strength_mul_14_div_10", ":center_no", slot_center_sortie_enemy_strength),
			(val_mul, ":enemy_strength_mul_14_div_10", 14),
			(val_div, ":enemy_strength_mul_14_div_10", 10),
			# (party_get_slot, ":party_strength", ":party_no", slot_party_cached_strength),	MOTO use party_slot_ge below
			
			(this_or_next|neg|party_is_in_town, ":party_no", ":center_no"),			
			# (gt, ":sortie_strength", ":enemy_strength_mul_14_div_10"),
			(party_slot_ge, ":center_no", slot_center_sortie_strength, ":enemy_strength_mul_14_div_10"),
			
			# (ge, ":party_strength", 100),	MOTO this is 5 troops
			(party_slot_ge, ":party_no", slot_party_cached_strength, 2000),	#MOTO this is around 100 troops
			#new - end
									
			(party_get_slot, ":town_lord", ":center_no", slot_town_lord),						
			(call_script, "script_troop_get_relation_with_troop", ":town_lord", ":troop_no"),
			
			(this_or_next|eq, ":troop_reputation", lrep_upstanding),
				(gt, reg0, -5),
			
            (store_distance_to_party_from_party, ":distance", ":party_no", ":center_no"),
			(lt, ":distance", ":score_to_beat"),
			
			(assign, ":target_center", ":center_no"),
			(assign, ":score_to_beat", ":distance"),
		(try_end),
		#gekokujo 3.0 integrating motomataru's campaign AI end

		(is_between, ":target_center", centers_begin, centers_end),
		
		(assign, ":action", spai_patrolling_around_center),
		(assign, ":object", ":target_center"),
				
		(try_begin),
			(eq, ":troop_no", "$g_talk_troop"),
			(str_store_string, s14, "str_we_have_heard_reports_that_the_enemy_is_in_the_area"),
			(str_store_string, s16, "str_i_have_heard_reports_of_enemy_incursions_into_our_territory"),
		(try_end),
		
		#gekokujo 3.0 integrating motomataru's campaign AI start
	#Get reinforcements	MOTO copy here as low priority recruit without restriction
	(else_try),
	  (gt, ":center_to_visit", -1),
	  (party_slot_eq, ":center_to_visit", slot_town_lord, ":troop_no"), #newly added
	  
	  # (lt, ":party_strength_as_percentage_of_ideal", 100),	#MOTO recruit whenever can
	  
	  #MOTO don't interrupt marshal operation for this
	  (this_or_next|eq, ":operation_in_progress", 0),
	  (neg|faction_slot_eq, ":faction_no", slot_faction_marshall, ":troop_no"),
	  #MOTO end don't interrupt marshal operation for this
	
	  (troop_get_slot, ":troop_wealth", ":troop_no", slot_troop_wealth), 
      (assign, ":hiring_budget", ":troop_wealth"),	#MOTO hiring budget/reinforcement cost comparison from script_hire_men_to_kingdom_hero_party
      (val_mul, ":hiring_budget", 3),
      (val_div, ":hiring_budget", 4),            
	  
	  (options_get_campaign_ai, ":reduce_campaign_ai"),
      (try_begin), 
        (eq, ":reduce_campaign_ai", 0), #hard
        (assign, ":reinforcement_cost", reinforcement_cost_hard),
      (else_try), 
        (eq, ":reduce_campaign_ai", 2), #easy
        (assign, ":reinforcement_cost", reinforcement_cost_easy),
      (else_try), 
        (assign, ":reinforcement_cost", reinforcement_cost_moderate),
      (try_end),
	  
      (ge, ":hiring_budget", ":reinforcement_cost"),
	  	  	  	  	  	  
	  (assign, ":action", spai_holding_center),
	  (assign, ":object", ":center_to_visit"),
	  
	  (try_begin),
	    (eq, ":troop_no", "$g_talk_troop"),
	    (str_store_string, s14, "str_i_dont_have_enough_troops_and_i_need_to_get_some_more"),
	    (str_store_string, s16, "str_i_am_running_low_on_troops"),
	  (try_end),
		#gekokujo 3.0 integrating motomataru's campaign AI end
	
	#Time in household
	(else_try),
	  #(eq, ":do_only_collecting_rents", 0), #gekokujo 3.0 integrating motomataru's campaign AI
		(gt, ":hours_since_last_home", 168),
		(eq, ":operation_in_progress", 0),

		(call_script, "script_lord_get_home_center", ":troop_no"),
		#(assign, ":home_center", reg0), #gekokujo 3.0 integrating motomataru's campaign AI
		(assign, ":center_to_visit", reg0),
		#(gt, ":home_center", -1), #gekokujo 3.0 integrating motomataru's campaign AI
		(gt, ":center_to_visit", -1),
		
		(assign, ":action", spai_holding_center),
		#(assign, ":object", ":home_center"), #gekokujo 3.0 integrating motomataru's campaign AI
		(assign, ":object", ":center_to_visit"),
		
		(try_begin),
			(eq, ":troop_no", "$g_talk_troop"),
			(str_store_string, s14, "str_i_need_to_spend_some_time_with_my_household"),
			(str_store_string, s16, "str_it_has_been_a_long_time_since_i_have_been_able_to_spend_time_with_my_household"),
		(try_end),

	#Patrolling the borders
	(else_try),
	  #(eq, ":do_only_collecting_rents", 0),
		(eq, ":faction_is_at_war", 1),
		(gt, ":aggressiveness", 65),
		(eq, ":operation_in_progress", 0),
		
		#gekokujo 3.0 integrating motomataru's campaign AI start
		#(assign, ":center_to_patrol", -1),
		#(assign, ":score_to_beat", 75),
		#
		#(try_for_range, ":village", villages_begin, villages_end),
		#	(store_faction_of_party, ":village_faction", ":village"),
		#	(store_relation, ":relation", ":village_faction", ":faction_no"),
		#	(lt, ":relation", 0),
		#	
		#	(store_distance_to_party_from_party, ":distance", ":village", ":party_no"),
		#	(lt, ":distance", ":score_to_beat"),
		#	
		#	(assign, ":score_to_beat", ":distance"),
		#	(assign, ":center_to_patrol", ":village"),
		#(try_end),
		#
		#(is_between, ":center_to_patrol", villages_begin, villages_end),
		#		
		#(assign, ":action", spai_patrolling_around_center),
		#(assign, ":object", ":center_to_patrol"),
		(assign, ":target_center", -1),
		(assign, ":score_to_beat", 75),
		
		(try_for_range, ":center_no", villages_begin, villages_end),
			(store_faction_of_party, ":center_faction", ":center_no"),
			(store_relation, ":relation", ":center_faction", ":faction_no"),
			(lt, ":relation", 0),
			
			(store_distance_to_party_from_party, ":distance", ":center_no", ":party_no"),
			(lt, ":distance", ":score_to_beat"),
			
			(assign, ":score_to_beat", ":distance"),
			(assign, ":target_center", ":center_no"),
		(try_end),
		
		(is_between, ":target_center", villages_begin, villages_end),
				
		(assign, ":action", spai_patrolling_around_center),
		(assign, ":object", ":target_center"),
		#gekokujo 3.0 integrating motomataru's campaign AI end
		
		(try_begin),
			(eq, ":troop_no", "$g_talk_troop"),
			(str_store_string, s14, "str_i_am_watching_the_borders"),
			(str_store_string, s16, "str_i_may_be_needed_to_watch_the_borders"),
		(try_end),

	#Visiting a friend - temporarily disabled
	(else_try),
		(eq, 1, 0),
		
	#Patrolling home
	(else_try),
	  #(eq, ":do_only_collecting_rents", 0),
		(call_script, "script_lord_get_home_center", ":troop_no"),
		#(assign, ":home_center", reg0), #gekokujo 3.0 integrating motomataru's campaign AI
		(assign, ":center_to_visit", reg0),
		
		#(is_between, ":home_center", centers_begin, centers_end), #gekokujo 3.0 integrating motomataru's campaign AI
		(is_between, ":center_to_visit", centers_begin, centers_end),
		(eq, ":operation_in_progress", 0),
		
		(assign, ":action", spai_patrolling_around_center),
		#(assign, ":object", ":home_center"), #gekokujo 3.0 integrating motomataru's campaign AI
		(assign, ":object", ":center_to_visit"),
		
		(try_begin),
			(eq, ":troop_no", "$g_talk_troop"),
			(str_store_string, s14, "str_i_will_guard_the_areas_near_my_home"),
			(str_store_string, s16, "str_i_am_perhaps_needed_most_at_home"),
		(try_end),
	
	#Default end
	(else_try),
	  #(eq, ":do_only_collecting_rents", 0),
		(eq, ":operation_in_progress", 0),

		(call_script, "script_lord_get_home_center", ":troop_no"),
		#(assign, ":home_center", reg0), #gekokujo 3.0 integrating motomataru's campaign AI
		(assign, ":center_to_visit", reg0),
		#(is_between, ":home_center", walled_centers_begin, walled_centers_end), #gekokujo 3.0 integrating motomataru's campaign AI
		(is_between, ":center_to_visit", walled_centers_begin, walled_centers_end),
		
		(assign, ":action", spai_holding_center),
		#(assign, ":object", ":home_center"), #gekokujo 3.0 integrating motomataru's campaign AI
		(assign, ":object", ":center_to_visit"),
		
		(try_begin),
			(eq, ":troop_no", "$g_talk_troop"),
			(str_store_string, s14, "str_i_cant_think_of_anything_better_to_do"),
		(try_end),
	(else_try),	
	  #(eq, ":do_only_collecting_rents", 0), #gekokujo 3.0 integrating motomataru's campaign AI
		(eq, ":operation_in_progress", 1),

		(party_get_slot, ":action", ":party_no", slot_party_ai_state),
		(party_get_slot, ":object", ":party_no", slot_party_ai_object),
		
		(try_begin),
			(eq, ":troop_no", "$g_talk_troop"),
			(str_store_string, s14, "str_i_am_completing_what_i_have_already_begun"),
		(try_end),
	(else_try),
	  #(eq, ":do_only_collecting_rents", 0), #gekokujo 3.0 integrating motomataru's campaign AI
		(assign, ":action", spai_undefined),
		(assign, ":object", -1),
		
		(try_begin),
			(eq, ":troop_no", "$g_talk_troop"),
			(str_store_string, s14, "str_i_dont_even_have_a_home_to_which_to_return"),
		(try_end),
	(try_end),
		
	(try_begin),
		(eq, "$cheat_mode", 2),
		(str_store_troop_name, s10, ":troop_no"),
		(display_message, "str_debug__s10_decides_s14_faction_ai_s15"),
	(try_end),
			
    (assign, reg0, ":action"),
	(assign, reg1, ":object"),  	
	]),
	#script_npc_decision_checklist_troop_follow_or_not
    # INPUT: troop_no
    # OUTPUT: reg0
	(
	"npc_decision_checklist_troop_follow_or_not", [

	(store_script_param, ":troop_no", 1),
	(store_faction_of_troop, ":faction_no", ":troop_no"),
	(faction_get_slot, ":faction_ai_state", ":faction_no", slot_faction_ai_state),

	(troop_get_slot, ":troop_reputation", ":troop_no", slot_lord_reputation_type),
	(faction_get_slot, ":faction_marshall", ":faction_no", slot_faction_marshall),
    ##diplomacy start+
    #Get the centralization value for use below.  It should be a value in [-3,3].
    #A centralization value of 0 should not result in any behavior change.
    (try_begin),
       #If the player altered the kingdom policy, always apply its effects to
       #the AI of his kingdom's lords.
       (call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", ":faction_no"),
       (ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
       (faction_get_slot, ":centralization", ":faction_no", dplmc_slot_faction_centralization),
       (val_clamp, ":centralization", -3, 4),
    (else_try),
       #Currently, do not apply centralization to the AI for NPC kingdoms, since
       #NPC rulers set their policies randomly and do not gain the same monthly
       #relation bonuses/penalties from centralization that the player does.
       (assign, ":centralization", 0),
    (try_end),
    ##diplomacy end+

	(assign, ":result", 0),
	(try_begin),
		##diplomacy start+ add another check
		(this_or_next|lt, ":faction_marshall", 0),
		##diplomacy end+
		(eq, ":faction_marshall", -1),

		(try_begin),
			(eq, ":troop_no", "$g_talk_troop"),
			(str_store_string, s15, "str__i_am_acting_independently_because_no_marshal_is_appointed"),
		(try_end),
	(else_try),			
		(troop_get_slot, ":faction_marshall_party", ":faction_marshall", slot_troop_leaded_party),
		(neg|party_is_active, ":faction_marshall_party"),

		#Not doing an offensive
		(try_begin),
			(eq, ":troop_no", "$g_talk_troop"),
			(str_store_string, s15, "str__i_am_acting_independently_because_our_marshal_is_currently_indisposed"),
		(try_end),
	(else_try),
		(neq, ":faction_ai_state", sfai_attacking_center),
        (neq, ":faction_ai_state", sfai_raiding_village),
        (neq, ":faction_ai_state", sfai_attacking_enemies_around_center),
        (neq, ":faction_ai_state", sfai_attacking_enemy_army),
        (neq, ":faction_ai_state", sfai_gathering_army),
	
		#Not doing an offensive
		(try_begin),
			(eq, ":troop_no", "$g_talk_troop"),
			(str_store_string, s15, "str__i_am_acting_independently_because_our_realm_is_currently_not_on_campaign"),
		(try_end),
	(else_try),
		(call_script, "script_troop_get_relation_with_troop", ":troop_no", ":faction_marshall"),
		(assign, ":relation_with_marshall", reg0),
		
		(try_begin),
		  (le, ":relation_with_marshall", -10),
		  (assign, ":acceptance_level", 10000),
		(else_try),  
		  (store_mul, ":acceptance_level", ":relation_with_marshall", -1000),
		(try_end), 
		
		(val_add, ":acceptance_level", 1500),

        (game_get_reduce_campaign_ai, ":reduce_campaign_ai"),
		(try_begin),
		  (neq, ":faction_no", "$players_kingdom"),          
          (try_begin),
            (eq, ":reduce_campaign_ai", 0), #hard
            (val_add, ":acceptance_level", -1250),
          (else_try),
            (eq, ":reduce_campaign_ai", 1), #moderate
          (else_try),                        
            (eq, ":reduce_campaign_ai", 2), #easy
            (val_add, ":acceptance_level", 1250),
          (try_end),           
        (else_try), 
          (faction_slot_eq, ":faction_no", slot_faction_marshall, "trp_player"),           
          (try_begin),
            (eq, ":reduce_campaign_ai", 0), #hard/player's faction
            (val_add, ":acceptance_level", -1000),
          (else_try),
            (eq, ":reduce_campaign_ai", 1), #moderate/player's faction
            (val_add, ":acceptance_level", -1500),
          (else_try),                        
            (eq, ":reduce_campaign_ai", 2), #easy/player's faction
            (val_add, ":acceptance_level", -2000),
          (try_end),           
		(try_end),
										
		(troop_get_slot, ":temp_ai_seed", ":troop_no", slot_troop_temp_decision_seed),						
		
		(le, ":temp_ai_seed", ":acceptance_level"),				
	
		#Very low opinion of marshall
		(try_begin),
			(eq, ":troop_no", "$g_talk_troop"),
			(str_store_string, s15, "str__i_am_not_accompanying_the_marshal_because_i_fear_that_he_may_lead_us_into_disaster"),
		(try_end),
		#Make nuanced, depending on personality type
	(else_try),	
		#(troop_get_slot, ":marshal_controversy", ":faction_marshall", slot_faction_marshall), #gekokujo 3.0 integrating motomataru's campaign AI
		(troop_get_slot, ":marshal_controversy", ":faction_marshall", slot_troop_controversy),	#MOTO correction!
	
		(lt, ":relation_with_marshall", 0),
		(ge, ":marshal_controversy", 50),
		
		(try_begin),
			(eq, ":troop_no", "$g_talk_troop"),
			(str_store_string, s15, "str_i_am_not_accompanying_the_marshal_because_i_question_his_judgment"),
		(try_end),
	(else_try),	
		#(troop_get_slot, ":marshal_controversy", ":faction_marshall", slot_faction_marshall), #gekokujo 3.0 integrating motomataru's campaign AI
		(neg|faction_slot_eq, ":faction_no", slot_faction_leader, ":faction_marshall"),
		
		(lt, ":relation_with_marshall", 5),
		(ge, ":marshal_controversy", 80),
		
		(try_begin),
			(eq, ":troop_no", "$g_talk_troop"),
			(str_store_string, s15, "str_i_am_not_accompanying_the_marshal_because_will_be_reappointment"),
		(try_end),
	(else_try),
		#(lt, ":relation_with_marshall", 45),	
		#(eq, ":faction_marshall", "trp_player"), #moved below as only effector. Search "think about this".
		
		(store_sub, ":relation_with_marshal_difference", 50, ":relation_with_marshall"),
		
		#for 50 relation with marshal ":acceptance_level" will be 0
		#for 20 relation with marshal ":acceptance_level" will be 2100
		#for 10 relation with marshal ":acceptance_level" will be 2800
		#for 0 relation with marshal ":acceptance_level" will be 3500
		#for -10 relation with marshal ":acceptance_level" will be 4200
		#average is about 2500
		(store_mul, ":acceptance_level", ":relation_with_marshal_difference", 70), 
		
        (game_get_reduce_campaign_ai, ":reduce_campaign_ai"),		
		(try_begin),
		  (neq, ":faction_no", "$players_kingdom"),
          
          (try_begin),
            (eq, ":reduce_campaign_ai", 0), #hard
            (val_add, ":acceptance_level", -1200),
          (else_try),
            (eq, ":reduce_campaign_ai", 1), #moderate
          (else_try),                        
            (eq, ":reduce_campaign_ai", 2), #easy
            (val_add, ":acceptance_level", 1200),
          (try_end),           
		(else_try),        
          (eq, ":faction_marshall", "trp_player"), 
          
          (try_begin),
            (eq, ":reduce_campaign_ai", 0), #hard
            (val_add, ":acceptance_level", -1000),
          (else_try),
            (eq, ":reduce_campaign_ai", 1), #moderate
            (val_add, ":acceptance_level", -1500),
          (else_try),                        
            (eq, ":reduce_campaign_ai", 2), #easy
            (val_add, ":acceptance_level", -2000),
          (try_end),           		  
		(try_end),
		
		(try_begin),
		  (eq, ":troop_reputation", lrep_selfrighteous),
		  (val_add, ":acceptance_level", 1500),
		(else_try),  
		  (this_or_next|eq, ":troop_reputation", lrep_martial),		
		  (this_or_next|eq, ":troop_reputation", lrep_roguish),		
		  (eq, ":troop_reputation", lrep_quarrelsome),
		  (val_add, ":acceptance_level", 1000),
		(else_try),  
		  (eq, ":troop_reputation", lrep_cunning), 
		  (val_add, ":acceptance_level", 500),
		(else_try),  
		  (eq, ":troop_reputation", lrep_upstanding), #neutral
		(else_try),  
		  (this_or_next|eq, ":troop_reputation", lrep_benefactor), #helper	
		  (eq, ":troop_reputation", lrep_goodnatured),		
		  (val_add, ":acceptance_level", -500),
		(else_try),  
		  (eq, ":troop_reputation", lrep_custodian), #very helper
		  (val_add, ":acceptance_level", -1000),
		(try_end),  
		
		(try_begin),
		  (troop_slot_eq, ":faction_marshall", slot_lord_reputation_type, lrep_quarrelsome),
		  (val_add, ":acceptance_level", -750),
		(else_try),  
		  (this_or_next|troop_slot_eq, ":faction_marshall", slot_lord_reputation_type, lrep_martial),
		  (troop_slot_eq, ":faction_marshall", slot_lord_reputation_type, lrep_upstanding),
		  (val_add, ":acceptance_level", -250),
		(try_end),  
				
		(val_add, ":acceptance_level", 2000),
		#average become 2500 + 2000 = 4500, (45% of lords will not join campaign because of this reason. (33% for hard, 57% for easy, 30% for marshal player))

      ##diplomacy start+ Apply centralization.
      #Adjusting acceptance level seems a natural place to represent this.
      (store_mul, reg0, ":centralization", 100),
      (val_clamp, reg0, -300, 301),#should be unnecessary
      (val_sub, ":acceptance_level", reg0),#adjust the chance of following the marshall by +/- 1% for every step of centralization
      ##diplomacy end+
		(troop_get_slot, ":temp_ai_seed", ":troop_no", slot_troop_temp_decision_seed),

		(le, ":temp_ai_seed", ":acceptance_level"),		
		
		(try_begin),		  
		  (eq, ":troop_no", "$g_talk_troop"),		  		  		  
		  (str_store_string, s15, "str_i_am_not_accompanying_the_marshal_because_i_can_do_greater_deeds"),
		(try_end),	
		
		#(try_begin),
		#  (ge, "$cheat_mode", 1),
		#  (assign, reg7, ":acceptance_level"),
		#  (assign, reg8, ":relation_with_marshall"),
		#  (display_message, "@{!}DEBUGS : acceptance level : {reg7}, relation with marshal : {reg8}"),
		#(try_end),
	(else_try),
		(store_current_hours, ":hours_since_last_faction_rest"),
		(faction_get_slot, ":last_rest_time", ":faction_no", slot_faction_ai_last_rest_time),
		(val_sub, ":hours_since_last_faction_rest", ":last_rest_time"),				
		
		#nine days on average, marshal will usually end after 10 days
		#ozan changed, 360 hours (15 days) in average, marshal cannot end it during a siege attack/defence anymore.
		(assign, ":troop_campaign_limit", 360), 
		(store_mul, ":marshal_relation_modifier", ":relation_with_marshall", 6), #ozan changed 4 to 6.
		(val_add, ":troop_campaign_limit", ":marshal_relation_modifier"),
		
		(try_begin),
			(eq, ":troop_reputation", lrep_upstanding),
			(val_mul, ":troop_campaign_limit", 4),
			(val_div, ":troop_campaign_limit", 3),
		(try_end),
		
		(str_store_troop_name, s16, ":faction_marshall"),
	
		(gt, ":hours_since_last_faction_rest", ":troop_campaign_limit"),
		
		#Too long a campaign
		(try_begin),
			(eq, ":troop_no", "$g_talk_troop"),
			(str_store_string, s15, "str__s16_has_kept_us_on_campaign_on_far_too_long_and_there_are_other_pressing_matters_to_which_i_must_attend"),
		(try_end),
		#Also make nuanced, depending on personality type
	(else_try),	
		(troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
		(neg|party_is_active, ":party_no"),
		#This string should not occur, as it will only happen if a lord is contemplating following the player		
	(else_try),	
		(troop_get_slot, ":marshal_party", ":faction_marshall", slot_troop_leaded_party),
		
		(assign, ":information_radius", 40), 
		(try_begin),
		  (faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_gathering_army),
		  (assign, ":information_radius", 50), 
		(try_end),
		
        (game_get_reduce_campaign_ai, ":reduce_campaign_ai"),
		(try_begin),
		  (neq, ":faction_no", "fac_player_supporters_faction"),
		  (neq, ":faction_no", "$players_kingdom"),
		  ##diplomacy start+ the player may be able to become leader in other situations
		  (neg|faction_slot_eq, ":faction_no", slot_faction_leader, "trp_player"),
		  ##diplomacy end+
		  (try_begin),
		    (eq, ":reduce_campaign_ai", 2), #easy
		    (try_begin),
		      (faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_gathering_army),
		      (val_add, ":information_radius", -10),
		    (else_try),  
		      (val_add, ":information_radius", -8),
		    (try_end),
		  (else_try),
		    (eq, ":reduce_campaign_ai", 1), #moderate
		    (try_begin),
		      (faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_gathering_army),
		      (val_add, ":information_radius", -5),
		    (else_try),  
		      (val_add, ":information_radius", -4),
		    (try_end),
		  (try_end),
		(else_try),  
		  (try_begin),
		    (eq, ":reduce_campaign_ai", 2), #easy
		    (try_begin),
		      (faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_gathering_army),
		      (val_add, ":information_radius", 25),
		    (else_try),  
		      (val_add, ":information_radius", 20),
		    (try_end),
		  (else_try),
		    (eq, ":reduce_campaign_ai", 1), #moderate
		    (try_begin),
		      (faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_gathering_army),
		      (val_add, ":information_radius", 15),
		    (else_try),  
		      (val_add, ":information_radius", 12),
		    (try_end),
		  (else_try),
		    (eq, ":reduce_campaign_ai", 0), #hard
		    (try_begin),
		      (faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_gathering_army),
		      (val_add, ":information_radius", 5),
		    (else_try),  
		      (val_add, ":information_radius", 4),
		    (try_end),
		  (try_end),
		(try_end),
      ##diplomacy start+ Apply centralization to the AI here.
      (store_add, reg0, 10, ":centralization"),
      (val_clamp, reg0, 7, 14),#should be unnecessary
      (val_mul, ":information_radius", reg0),
      (val_add, ":information_radius", 5),
      (val_div, ":information_radius", 10),#Adjust +/- 10% for every level of centralization
      ##diplomacy end+
		
		(faction_get_slot, ":faction_object", ":faction_no", slot_faction_ai_object),		  
		(assign, reg17, 0),
		(try_begin),		  		  
		  (try_begin),
		    (neg|is_between, ":faction_object", villages_begin, villages_end),
		    (assign, reg17, 1),
		  (try_end),
		  (try_begin),
		    (neg|faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_attacking_enemies_around_center),
		    (assign, reg17, 1),
		  (try_end),		  
		  (eq, reg17, 1),
		  
		  (store_distance_to_party_from_party, ":distance", ":marshal_party", ":party_no"),

		  (gt, ":distance", ":information_radius"),
		
          (try_begin),
            (eq, ":troop_no", "$g_talk_troop"),
            (str_store_string, s15, "str__i_am_not_participating_in_the_marshals_campaign_because_i_do_not_know_where_to_find_our_main_army"),
  		  (try_end),  		  
		(else_try),	
		  (eq, reg17, 0),	
		  
          (assign, reg17, 1),
          (try_begin),
            #if we are already accompanying marshal forget below.
            (party_slot_eq, ":party_no", slot_party_ai_state, spai_accompanying_army),
            (party_slot_eq, ":party_no", slot_party_ai_object, ":marshal_party"),
            (assign, reg17, 0),
          (try_end),                                
          (eq, reg17, 1),
                              
		  #if faction ai is "attacking enemies around a center" is then do not find and compare distance to marshal, find and compare distance to "attacked village"
		  (party_get_slot, ":enemy_strength_nearby", ":faction_object", slot_center_sortie_enemy_strength),
		  
		  (try_begin), #changes between 70..x (as ":enemy_strength_nearby" increases, ":information_radius" increases too.),
		    (ge, ":enemy_strength_nearby", 4000),
		    (val_sub, ":enemy_strength_nearby", 4000),
		    (store_div, ":information_radius", ":enemy_strength_nearby", 200),
		    (val_add, ":information_radius", 70),
		  (else_try), #changes between 30..70
		    (store_div, ":information_radius", ":enemy_strength_nearby", 100),
		    (val_add, ":information_radius", 30),
		  (try_end),
		  
		  (store_distance_to_party_from_party, ":distance", ":faction_object", ":party_no"),

		  (gt, ":distance", ":information_radius"),
		
          (try_begin),
            (eq, ":troop_no", "$g_talk_troop"),
            (str_store_string, s15, "str__i_am_acting_independently_although_some_enemies_have_been_spotted_within_our_borders_they_havent_come_in_force_and_the_local_troops_should_be_able_to_dispatch_them"),
  		  (try_end),  		  
		(try_end),
		
		(gt, ":distance", ":information_radius"),
	(else_try),
		(try_begin),
		  (eq, ":troop_no", "$g_talk_troop"),
		  (str_store_string, s15, "str__the_needs_of_the_realm_must_come_first"),
		(try_end),
		(assign, ":result", 1),
	(try_end),
			
	(assign, reg0, ":result"),	
	]),
	#script_npc_decision_checklist_peace_or_war
   ##diplomacy start+
   #Modified this to return additional information.
	##diplomacy end+
	(
	"npc_decision_checklist_peace_or_war", 
	#this script is used to add a bit more color to diplomacy, particularly with regards to the player
	
	[
	(store_script_param, ":actor_faction", 1),
	(store_script_param, ":target_faction", 2),
	(store_script_param, ":envoy", 3),

	##diplomacy start+
	#Since "fac_player_supporters_faction" is used as a synonym for "the faction led by the player"
	#in many places, correct this here.
	(call_script, "script_dplmc_translate_inactive_player_supporter_faction_2", ":actor_faction", ":target_faction"),
	(assign, ":actor_faction", reg0),
	(assign, ":target_faction", reg1),
	##diplomacy end+

	(assign, ":actor_strength", 0),
	(assign, ":target_strength", 0),
	(assign, ":actor_centers_held_by_target", 0),

	#gekokujo 2.1 re-enabled border tracking
	(assign, ":two_factions_share_border", 0),
	(assign, ":third_party_war", 0), 
	(assign, ":num_third_party_wars", 0),

	(assign, ":active_mutual_enemy", 0), #an active enemy with which the target is at war
	(assign, "$g_concession_demanded", 0),
	##diplomacy start+
	(assign, ":last_center_lost", 0),#  last center lost to the target faction
	(assign, ":last_center_lost_time", 0),# time the last center was lost to the target faction

	#"Third party" after taking into account alliances
	#(assign, ":actual_third_party_war", 0),
	(assign, ":num_actual_third_party_wars", 0),
	##diplomacy end+
	
	(store_relation, ":current_faction_relation", ":actor_faction", ":target_faction"),
	
	(try_begin),
		(eq, ":target_faction", "fac_player_supporters_faction"),
		(assign, ":modified_honor_and_relation", "$player_honor"), #this can be affected by the emissary's skill
		
		(val_add, ":target_strength", 2), #for player party
	(else_try),
		(assign, ":modified_honor_and_relation", 0), #this can be affected by the emissary's skill
	(try_end),
	
	(faction_get_slot, ":actor_leader", ":actor_faction", slot_faction_leader),
	(faction_get_slot, ":target_leader", ":target_faction", slot_faction_leader),

	(call_script, "script_troop_get_relation_with_troop", ":actor_leader", ":target_leader"),

	(assign, ":relation_bonus", reg0),
	(val_min, ":relation_bonus", 10),
	(val_add, ":modified_honor_and_relation", ":relation_bonus"),

	(str_store_troop_name, s15, ":actor_leader"),
	(str_store_troop_name, s16, ":target_leader"),
	

	(assign, ":war_damage_suffered", 0),
	(assign, ":war_damage_inflicted", 0),

	(call_script, "script_diplomacy_faction_get_diplomatic_status_with_faction", ":actor_faction", ":target_faction"),
	(assign, ":war_peace_truce_status", reg0),
	(str_clear, s12),
	(try_begin),
		(eq, ":war_peace_truce_status", -2),
		(str_store_string, s12, "str_s15_is_at_war_with_s16_"),
		
		(store_add, ":war_damage_inflicted_slot", ":target_faction", slot_faction_war_damage_inflicted_on_factions_begin),
		(val_sub, ":war_damage_inflicted_slot", kingdoms_begin),
		(faction_get_slot, ":war_damage_inflicted", ":actor_faction", ":war_damage_inflicted_slot"),

		(store_add, ":war_damage_suffered_slot", ":actor_faction", slot_faction_war_damage_inflicted_on_factions_begin),
		(val_sub, ":war_damage_suffered_slot", kingdoms_begin),
		(faction_get_slot, ":war_damage_suffered", ":target_faction", ":war_damage_suffered_slot"),

		
	(else_try),
		#truce in effect
		(eq, ":war_peace_truce_status", 1),
		(str_store_string, s12, "str_in_the_short_term_s15_has_a_truce_with_s16_as_a_matter_of_general_policy_"),
	(else_try),
		#provocation noted
		(eq, ":war_peace_truce_status", -1),
		(str_store_string, s12, "str_in_the_short_term_s15_was_recently_provoked_by_s16_and_is_under_pressure_to_declare_war_as_a_matter_of_general_policy_"),
	(try_end),

	#clear for dialog with lords
	(try_begin),
		(is_between, "$g_talk_troop", active_npcs_begin, active_npcs_end),
		(str_clear, s12),
	(try_end),
	
	(try_begin),
		(gt, ":envoy", -1),
		(store_skill_level, ":persuasion_x_2", "skl_persuasion", ":envoy"),
		(val_mul, ":persuasion_x_2", 2),
		(val_add, ":modified_honor_and_relation", ":persuasion_x_2"),
		
		(try_begin),
			(eq, "$cheat_mode", 1),
			(assign, reg4, ":modified_honor_and_relation"),
			(display_message, "str_envoymodified_diplomacy_score_honor_plus_relation_plus_envoy_persuasion_=_reg4"),
		(try_end),

	(try_end),
		
	
	(try_for_range, ":kingdom_to_reset", kingdoms_begin, kingdoms_end),
		(faction_set_slot, ":kingdom_to_reset", slot_faction_temp_slot, 0),
	(try_end),
	
	(try_for_parties, ":party_no"),
		(assign, ":party_value", 0),
		(try_begin),
			(is_between, ":party_no", towns_begin, towns_end),
			(assign, ":party_value", 3),
		(else_try),	
			(is_between, ":party_no", castles_begin, castles_end),
			(assign, ":party_value", 2),
		(else_try),
			(is_between, ":party_no", villages_begin, villages_end),
			(assign, ":party_value", 1),
		(else_try),	
			(party_get_template_id, ":template", ":party_no"),
			(eq, ":template", "pt_kingdom_hero_party"),
			(assign, ":party_value", 2),
		(try_end),
		

		(store_faction_of_party, ":party_current_faction", ":party_no"),
		(party_get_slot, ":party_original_faction", ":party_no", slot_center_original_faction),
		(party_get_slot, ":party_ex_faction", ":party_no", slot_center_ex_faction),
		
		
		#total strengths
		(try_begin),
			(is_between, ":party_current_faction", kingdoms_begin, kingdoms_end),
			(faction_get_slot, ":faction_strength", ":party_current_faction", slot_faction_temp_slot),
			(val_add, ":faction_strength", ":party_value"),
			(faction_set_slot, ":party_current_faction", slot_faction_temp_slot, ":faction_strength"),
		(try_end),
		
		
		(try_begin),
			(eq, ":party_current_faction", ":target_faction"),
			(val_add, ":target_strength", ":party_value"),

			(try_begin),
				(this_or_next|eq, ":party_original_faction", ":actor_faction"),
					(eq, ":party_ex_faction", ":actor_faction"),
				(val_add, ":actor_centers_held_by_target", 1),
				(try_begin),
					(is_between, ":party_no", walled_centers_begin, walled_centers_end),
					(assign, "$g_concession_demanded", ":party_no"),
					(str_store_party_name, s18, "$g_concession_demanded"),
					##diplomacy start+ Also track the most recently taken walled center
					(eq, ":party_ex_faction", ":actor_faction"),
					(this_or_next|lt, ":last_center_lost", 1),
						(party_slot_ge, ":party_no", dplmc_slot_center_last_transfer_time, ":last_center_lost_time"),
					(assign, ":last_center_lost", ":party_no"),
					(party_get_slot, ":last_center_lost_time", ":party_no", dplmc_slot_center_last_transfer_time),
					##diplomacy end+
				(try_end),
			(try_end),

# Could include two factions share border, but war is unlikely to break out in the first place unless there is a common border

#gekokujo 2.1 shared borders matter now start
			(try_begin),
				(is_between, ":party_no", walled_centers_begin, walled_centers_end),
				(try_for_range, ":other_center", walled_centers_begin, walled_centers_end),
					(assign, ":two_factions_share_border", 0),
					(store_faction_of_party, ":other_faction", ":other_center"),
					(eq, ":other_faction", ":actor_faction"),
					(store_distance_to_party_from_party, ":distance", ":party_no", ":other_center"),
					#gekokujo 2.1a increase distance to 30 now that slots have been fixed
					#(le, ":distance", 30),
					#gekokujo 3.0 increase distance to 60 to see if more wars are possible
					(le, ":distance", 60),
					(assign, ":two_factions_share_border", 1),
				(try_end),
			(try_end),
#gekokujo 2.1 shared borders matter now end
		(else_try),
			(eq, ":party_current_faction", ":actor_faction"),
			(val_add, ":actor_strength", ":party_value"),
		(try_end),
	(try_end),

	#gekokujo 2.1 calculus to start war
	#Old Calradia strength = 110 x 1 (villages,), 48? x 2 castles, 22 x 3 towns, 88 x 2 lord parties = 272 + 176 = 448
	#New Japan strength = 161 x 1 (villages,), 72? x 2 castles, 32 x 3 towns, 170 x 2 lord parties = 384 + 326 = 741
	(assign, ":strongest_kingdom", -1),
	(assign, ":score_to_beat", 60),
	#gekokujo 3.0 decrease score to beat
	#(assign, ":score_to_beat", 100),
	##diplomacy start+
	#Take into account alliances
	(assign, ":strongest_kingdom_offensive", -1),
	(assign, ":strongest_kingdom_offensive_score", -1),

	(assign, ":strongest_kingdom_defensive", -1),
	(assign, ":strongest_kingdom_defensive_score", -1),

	(faction_get_slot, ":actor_offensive_score", ":actor_faction", slot_faction_temp_slot),
	(faction_get_slot, ":actor_defensive_score", ":actor_faction", slot_faction_temp_slot),

	#(faction_get_slot, ":target_offensive_score", ":target_faction", slot_faction_temp_slot),
	(faction_get_slot, ":target_defensive_score", ":target_faction", slot_faction_temp_slot),

	#Use these instead of just counting the number of factions
    (assign, ":strength_against_actor", 0),
	(assign, ":strength_against_target", 0),

	##diplomacy end+
	(try_for_range, ":strongest_kingdom_candidate", kingdoms_begin, kingdoms_end),
		(faction_get_slot, ":candidate_strength", ":strongest_kingdom_candidate", slot_faction_temp_slot),
		##diplomacy start+
		#Take into account allies
		(assign, ":candidate_offensive_score", ":candidate_strength"),
		(assign, ":candidate_defensive_score", ":candidate_strength"),
		(try_for_range, ":other_kingdom", kingdoms_begin, kingdoms_end),
		   (neq, ":other_kingdom", ":strongest_kingdom_candidate"),
			(faction_get_slot, ":other_kingdom_strength", ":other_kingdom", slot_faction_temp_slot),
			(call_script, "script_dplmc_get_faction_truce_length_with_faction", ":strongest_kingdom_candidate", ":other_kingdom"),
			#Add 90% rather than 100%, because otherwise, if several kingdoms are
			#allied all of them will have the same strength by this measurement.
			#gekokujo 3.0 new strategic ai: change it to 75% -- make clans have smaller capacity for strategic thought
			(try_begin),
					 #Full alliance
					 (gt, reg0, dplmc_treaty_alliance_days_expire),
					 #gekokujo 3.0 new strategic ai start
					 (store_mul, reg0, ":other_kingdom_strength", 75),
					 (val_div, reg0, 100),
					 #(store_mul, reg0, ":other_kingdom_strength", 9),
					 #(val_div, reg0, 10),
					 #gekokujo 3.0 new strategic ai end
					 (val_add, ":candidate_offensive_score", reg0),
					 (val_add, ":candidate_defensive_score", reg0),
			(else_try),
					 #Defensive alliance
					 (gt, reg0, dplmc_treaty_defense_days_expire),
					 #gekokujo 3.0 new strategic ai start
					 (store_mul, reg0, ":other_kingdom_strength", 75),
					 (val_div, reg0, 100),
					 #(store_mul, reg0, ":other_kingdom_strength", 9),
					 #(val_div, reg0, 10),
					 #gekokujo 3.0 new strategic ai end
					 (val_add, ":candidate_defensive_score", reg0),
			(try_end),
		(try_end),
		#Update actor/target strengths with alliances, and "strength against"
		(try_begin),
			(eq, ":strongest_kingdom_candidate", ":actor_faction"),
			(assign, ":actor_offensive_score", ":candidate_offensive_score"),
			(assign, ":actor_defensive_score", ":candidate_defensive_score"),
		(else_try),
			(store_relation, ":relation", ":strongest_kingdom_candidate", ":actor_faction"),
			(lt, ":relation", 0),
			(val_add, ":strength_against_actor", ":other_kingdom_strength"),
		(try_end),
		(try_begin),
			(eq, ":strongest_kingdom_candidate", ":target_faction"),
			#(assign, ":target_offensive_score", ":candidate_offensive_score"),
			(assign, ":target_defensive_score", ":candidate_defensive_score"),
		(else_try),
			(store_relation, ":relation", ":strongest_kingdom_candidate", ":target_faction"),
			(lt, ":relation", 0),
			(val_add, ":strength_against_target", ":other_kingdom_strength"),
		(try_end),
		#Update global max/min
		(try_begin),
			(gt, ":candidate_offensive_score", ":strongest_kingdom_offensive_score"),
			(assign, ":strongest_kingdom_offensive", ":strongest_kingdom_candidate"),
			(assign, ":strongest_kingdom_offensive_score", ":candidate_offensive_score"),
		(try_end),
		(try_begin),
			(gt, ":candidate_defensive_score", ":strongest_kingdom_defensive_score"),
			(assign, ":strongest_kingdom_defensive", ":strongest_kingdom_candidate"),
			(assign, ":strongest_kingdom_defensive_score", ":candidate_defensive_score"),
		(try_end),
		##diplomacy end+
		(gt, ":candidate_strength", ":score_to_beat"),
		(assign, ":strongest_kingdom", ":strongest_kingdom_candidate"),
		(assign, ":score_to_beat", ":candidate_strength"),
	(try_end),
	
	
	(try_begin),
		(eq, "$cheat_mode", 2),
		(gt, ":strongest_kingdom", 1),
		(str_store_faction_name, s4, ":strongest_kingdom"),
		(assign, reg3, ":score_to_beat"),
		(display_message, "@{!}DEBUG - {s4} strongest kingdom with {reg3} strength"),
		##diplomacy start+ Show strongest counting alliances if it's different
		(try_begin),
			(gt, ":strongest_kingdom_offensive", 0),
			(neq, ":strongest_kingdom_offensive", ":strongest_kingdom"),
			(str_store_faction_name, s4, ":strongest_kingdom_offensive"),
			(assign, reg3, ":strongest_kingdom_offensive_score"),
			(display_message, "@{!}DEBUG - including offensive and defensive alliances {s4} strongest kingdom with {reg3} strength"),
		(try_end),
		(try_begin),
			(gt, ":strongest_kingdom_defensive", 0),
			(neq, ":strongest_kingdom_defensive", ":strongest_kingdom"),
			(neq, ":strongest_kingdom_defensive", ":strongest_kingdom_offensive"),
			(str_store_faction_name, s4, ":strongest_kingdom_defensive"),
			(assign, reg3, ":strongest_kingdom_defensive_score"),
			(display_message, "@{!}DEBUG - including only defensive alliances {s4} strongest kingdom with {reg3} strength"),
		(try_end),
		#Revert values
		(assign, reg3, ":score_to_beat"),
		(str_store_faction_name, s4, ":strongest_kingdom"),
		##diplomacy end+
	(try_end),
	
	
	(assign, ":strength_ratio", 1),
	(try_begin),
		(gt, ":actor_strength", 0),
		(store_mul, ":strength_ratio", ":target_strength", 100),
		(val_div, ":strength_ratio", ":actor_strength"),
	(try_end),
	##diplomacy start+
	#Other strength ratios using strengths counting alliances
	(assign, ":strength_ratio_new_attack", 1),
	(try_begin),
		(gt, ":actor_offensive_score", 0),
		(store_mul, ":strength_ratio_new_attack", ":target_defensive_score", 100),
		(val_div, ":strength_ratio_new_attack", ":actor_offensive_score"),
	(try_end),
	(assign, ":strength_ratio_current_war", 1),
	(try_begin),
		(gt, ":actor_defensive_score", 0),
		(store_mul, ":strength_ratio_current_war", ":target_defensive_score", 100),
		(val_div, ":strength_ratio_current_war", ":actor_defensive_score"),
	(try_end),
	#Calculate the total magnitude of the forces hostile to the faction versus its allies
	(assign, ":strength_ratio_all_enemies_actor", 1),
	(try_begin),
		(gt, ":actor_defensive_score", 0),
		(store_mul, ":strength_ratio_all_enemies_actor", ":strength_against_actor", 100),
		(val_div, ":strength_ratio_all_enemies_actor", ":actor_defensive_score"),
	(try_end),
	##diplomacy end+
	
	(try_for_range, ":possible_mutual_enemy", kingdoms_begin, kingdoms_end),
		(neq, ":possible_mutual_enemy", ":target_faction"),
		(neq, ":possible_mutual_enemy", ":actor_faction"),
		(faction_slot_eq, ":possible_mutual_enemy", slot_faction_state, sfs_active),
		
		(store_relation, ":relation", ":possible_mutual_enemy", ":actor_faction"),
		(lt, ":relation", 0),
		(assign, ":third_party_war", ":possible_mutual_enemy"),
		(val_add, ":num_third_party_wars", 1),

		##diplomacy start+
		##ACTUAL third-party wars (i.e. not allied to the target faction)
		(call_script, "script_dplmc_get_faction_truce_length_with_faction", ":target_faction", ":possible_mutual_enemy"),
		(try_begin),
			(neg|gt, reg0, dplmc_treaty_defense_days_expire),
			#(assign, ":actual_third_party_war", ":possible_mutual_enemy"),
			(val_add, ":num_actual_third_party_wars", 1),
		(try_end),
		##diplomacy end+
		
		(store_relation, ":relation", ":possible_mutual_enemy", ":target_faction"),
		(lt, ":relation", 0),
		(assign, ":active_mutual_enemy", ":possible_mutual_enemy"),
	(try_end),
	
	(store_current_hours, ":cur_hours"),
    (faction_get_slot, ":faction_ai_last_decisive_event", ":actor_faction", slot_faction_ai_last_decisive_event),
    (store_sub, ":hours_since_last_decisive_event", ":cur_hours", ":faction_ai_last_decisive_event"),	

	##diplomacy start+ use gender script
	(call_script, "script_dplmc_store_troop_is_female_reg", ":actor_leader", 4),
	##diplomacy end+
	
	(try_begin),
		(gt, "$supported_pretender", 0),
		(this_or_next|eq, "$supported_pretender", ":actor_leader"),
			(eq, "$supported_pretender", ":target_leader"),
		(this_or_next|eq, ":actor_faction", "$supported_pretender_old_faction"),
            (eq, ":target_faction", "$supported_pretender_old_faction"),

		(assign, ":result", -3),	
		##diplomacy start+
		#(troop_get_type, reg4, ":actor_leader"),#<- commented out
		##diplomacy end+	
		(assign, ":explainer_string", "str_s12s15_cannot_negotiate_with_s16_as_to_do_so_would_undermine_reg4herhis_own_claim_to_the_throne_this_civil_war_must_almost_certainly_end_with_the_defeat_of_one_side_or_another"),
	(else_try),
		(lt, ":modified_honor_and_relation", -20),
		##diplomacy start+ Take into account strengths including alliances
		#gekokujo 3.0 new strategic ai start
		(this_or_next|lt, ":strength_ratio_current_war", 188),
		#(this_or_next|lt, ":strength_ratio_current_war", 125),
		#gekokujo 3.0 new strategic ai end
		##diplomacy end+
		#gekokujo 3.0 new strategic ai start
		(lt, ":strength_ratio", 188),
		#(lt, ":strength_ratio", 125),
		#gekokujo 3.0 new strategic ai end
		#gekokujo 3.0 new strategic ai start
		(lt, ":war_damage_suffered", 600),
		#(lt, ":war_damage_suffered", 400),
		#gekokujo 3.0 new strategic ai end
		(this_or_next|neq, ":war_peace_truce_status", -2),
			(lt, ":hours_since_last_decisive_event", 720),
		##diplomacy start+ Examine strength of enemies versus allies
		#gekokujo 3.0 new strategic ai start
		(this_or_next|lt, ":strength_ratio_all_enemies_actor", 188),
		#(this_or_next|lt, ":strength_ratio_all_enemies_actor", 125),
		#gekokujo 3.0 new strategic ai end
		##diplomacy end+		
		#gekokujo 3.0 new strategic ai start
		(this_or_next|eq, ":num_third_party_wars", 1),
		#gekokujo 3.0 new strategic ai end
		(eq, ":num_third_party_wars", 0),

		(assign, ":result", -3),	
		##diplomacy start+
		#(troop_get_type, reg4, ":actor_leader"),#<- commented out
		##diplomacy end+		
		(assign, ":explainer_string", "str_s12s15_considers_s16_to_be_dangerous_and_untrustworthy_and_shehe_wants_to_bring_s16_down"),
	(else_try),	
		(gt, ":actor_centers_held_by_target", 0),
		(try_begin),
		  (eq, "$cheat_mode", 1),
		  (display_message, "@{!}Actor centers held by target noted"),
		(try_end),
	
		#gekokujo 3.0 new strategic ai start
		(lt, ":war_damage_suffered", 300),
		#(lt, ":war_damage_suffered", 200),
		#gekokujo 3.0 new strategic ai end
		(try_begin),
		  (eq, "$cheat_mode", 1),
          (display_message, "@{!}War damage under minimum"),
		(try_end),

		##diplomacy start+ Take into account strengths including alliances
		#gekokujo 3.0 new strategic ai start
		(this_or_next|lt, ":strength_ratio_current_war", 188),
		#(this_or_next|lt, ":strength_ratio_current_war", 125),
		#gekokujo 3.0 new strategic ai end
		##diplomacy end+		
		#gekokujo 3.0 new strategic ai start
		(lt, ":strength_ratio", 188),
		#(lt, ":strength_ratio", 125),
		#gekokujo 3.0 new strategic ai end
		(try_begin),
		  (eq, "$cheat_mode", 1),
          (display_message, "@{!}Strength ratio correct"),
		(try_end),
		##diplomacy start+ Examine strength of enemies versus allies
		#gekokujo 3.0 new strategic ai start
		(this_or_next|lt, ":strength_ratio_all_enemies_actor", 188),
		#(this_or_next|lt, ":strength_ratio_all_enemies_actor", 125),
		#gekokujo 3.0 new strategic ai end
		##diplomacy end+			
		#gekokujo 3.0 new strategic ai start
		(this_or_next|eq, ":num_third_party_wars", 1),
		#gekokujo 3.0 new strategic ai end
		(eq, ":num_third_party_wars", 0),
		(try_begin),
		  (eq, "$cheat_mode", 1),
          (display_message, "@{!}Third party wars"),
		(try_end),
		
		(assign, ":result", -2),
		(assign, ":explainer_string", "str_s12s15_is_anxious_to_reclaim_old_lands_such_as_s18_now_held_by_s16"),
	(else_try),
		(eq, ":war_peace_truce_status", -2),
		##diplomacy start+ Take into account strengths including alliances
		#gekokujo 3.0 new strategic ai start
		(this_or_next|lt, ":strength_ratio_current_war", 188),
		#(this_or_next|lt, ":strength_ratio_current_war", 125),
		#gekokujo 3.0 new strategic ai end
		##diplomacy end+
		#gekokujo 3.0 new strategic ai start
		(lt, ":strength_ratio", 125),
		#(lt, ":strength_ratio", 188),
		#gekokujo 3.0 new strategic ai end
		#gekokujo 3.0 new strategic ai start
		(le, ":num_third_party_wars", 2),
		#(le, ":num_third_party_wars", 1),
		#gekokujo 3.0 new strategic ai end
		(ge, ":war_damage_inflicted", 5),
		(this_or_next|neq, ":war_peace_truce_status", -2),
			(lt, ":hours_since_last_decisive_event", 720),
		
		(store_mul, ":war_damage_suffered_x_2", ":war_damage_suffered", 2),
		(gt, ":war_damage_inflicted", ":war_damage_suffered_x_2"),

		(assign, ":result", -2),
		##diplomacy start+
		#(troop_get_type, reg4, ":actor_leader"),#<- commented out
		##diplomacy end+
		(assign, ":explainer_string", "str_s12s15_feels_that_reg4shehe_is_winning_the_war_against_s16_and_sees_no_reason_not_to_continue"),
	(else_try),
		(le, ":war_peace_truce_status", -1),
		
		(this_or_next|eq, ":war_peace_truce_status", -1), #either a war is just beginning, or there is a provocation 
			(le, ":war_damage_inflicted", 1),
		##diplomacy start+ Take into account strengths including alliances
		#gekokujo 3.0 new strategic ai start
		(this_or_next|lt, ":strength_ratio_new_attack", 225),
		#(this_or_next|lt, ":strength_ratio_new_attack", 150),
		#gekokujo 3.0 new strategic ai end
		##diplomacy end+			
		#gekokujo 3.0 new strategic ai start
		(lt, ":strength_ratio", 225),
		#(lt, ":strength_ratio", 150),
		#gekokujo 3.0 new strategic ai end
		##diplomacy start+ Examine strength of enemies versus allies
		#gekokujo 3.0 new strategic ai start
		(this_or_next|lt, ":strength_ratio_all_enemies_actor", 225),
		#(this_or_next|lt, ":strength_ratio_all_enemies_actor", 150),
		#gekokujo 3.0 new strategic ai end
		##diplomacy end+
		#gekokujo 3.0 new strategic ai start
		(this_or_next|eq, ":num_third_party_wars", 1),
		#gekokujo 3.0 new strategic ai end
		(eq, ":num_third_party_wars", 0),
		
		(faction_slot_ge, ":actor_faction", slot_faction_instability, 60),

		(assign, ":result", -1),
		(assign, ":explainer_string", "str_s12s15_faces_too_much_internal_discontent_to_feel_comfortable_ignoring_recent_provocations_by_s16s_subjects"),
	(else_try),	
		(eq, ":war_peace_truce_status", -2),
		#gekokujo 3.0 new strategic ai start
		(lt, ":war_damage_inflicted", 150),
		#(lt, ":war_damage_inflicted", 100),
		#gekokujo 3.0 new strategic ai end
		#gekokujo 3.0 new strategic ai start
		(this_or_next|eq, ":num_third_party_wars", 2),
		#gekokujo 3.0 new strategic ai end
		(eq, ":num_third_party_wars", 1),

		(assign, ":result", -1),
		##diplomacy start+
		#(troop_get_type, reg4, ":actor_leader"),#<- commented out
		##diplomacy end+	
		(assign, ":explainer_string", "str_s12even_though_reg4shehe_is_fighting_on_two_fronts_s15_is_inclined_to_continue_the_war_against_s16_for_a_little_while_longer_for_the_sake_of_honor"),

	(else_try),	
		(eq, ":war_peace_truce_status", -2),
		#gekokujo 3.0 new strategic ai start
		(lt, ":war_damage_inflicted", 150),
		#(lt, ":war_damage_inflicted", 100),
		#gekokujo 3.0 new strategic ai end
		(eq, ":num_third_party_wars", 0),

		(assign, ":result", -1),
		##diplomacy start+
		#(troop_get_type, reg4, ":actor_leader"),#<- commented out
		##diplomacy end+	
		(assign, ":explainer_string", "str_s12s15_feels_that_reg4shehe_must_pursue_the_war_against_s16_for_a_little_while_longer_for_the_sake_of_honor"),
	(else_try),
		(this_or_next|faction_slot_eq, ":actor_faction", slot_faction_ai_state, sfai_attacking_center),
		(this_or_next|faction_slot_eq, ":actor_faction", slot_faction_ai_state, sfai_raiding_village),
			(faction_slot_eq, ":actor_faction", slot_faction_ai_state, sfai_attacking_enemy_army),
		(faction_get_slot, ":offensive_object", ":actor_faction", slot_faction_ai_object),
		(party_is_active, ":offensive_object"),
		(store_faction_of_party, ":offensive_object_faction", ":offensive_object"),
		(eq, ":offensive_object_faction", ":target_faction"),
		(str_store_party_name, s17, ":offensive_object"),
		
		(assign, ":result", -1),
		(assign, ":explainer_string", "str_s12s15_is_currently_on_the_offensive_against_s17_now_held_by_s16_and_reluctant_to_negotiate"),

		
	(else_try),
		#Attack strongest kingdom, if it is also at war
		##diplomacy start+ Take into account strengths including alliances
		(this_or_next|eq, ":strongest_kingdom_offensive", ":target_faction"),
		##diplomacy end+
		(eq, ":strongest_kingdom", ":target_faction"),
		#gekokujo 3.0 new strategic ai start
		(this_or_next|eq, ":num_third_party_wars", 1),
		#gekokujo 3.0 new strategic ai end
		(eq, ":num_third_party_wars", 0),
		
		#Either not at war, or at war for two months
		(this_or_next|ge, ":war_peace_truce_status", -1),
			(lt, ":hours_since_last_decisive_event", 1440),
		
		#gekokujo 2.1 enabled border checking (also was originally at 0)
		(eq, ":two_factions_share_border", 1),

		(assign, ":at_least_one_other_faction_at_war_with_strongest", 0),
		(try_for_range, ":kingdom_to_check", kingdoms_begin, kingdoms_end),
			(neq, ":kingdom_to_check", ":actor_faction"),
			(neq, ":kingdom_to_check", ":target_faction"),
			(faction_slot_eq, ":kingdom_to_check", slot_faction_state, sfs_active),
			(store_relation, ":relation_of_factions", ":kingdom_to_check", ":target_faction"),
			(lt, ":relation_of_factions", 0),
			(assign, ":at_least_one_other_faction_at_war_with_strongest", 1),
		(try_end),
		(eq, ":at_least_one_other_faction_at_war_with_strongest", 1),
		
		
		(assign, ":result", -1),
		(assign, ":explainer_string", "str_s12s15_is_alarmed_by_the_growing_power_of_s16"),
		
	#bid to conquer all Japan
	(else_try),
		#gekokujo 3.0 new strategic ai start
		(this_or_next|eq, ":num_third_party_wars", 1),
		#gekokujo 3.0 new strategic ai end
		(eq, ":num_third_party_wars", 0),
		(try_begin),
			(ge, "$cheat_mode", 1),
			(display_message, "@{!}DEBUG -- No third party wars for {s15}"),
		(try_end),
		(eq, ":actor_faction", ":strongest_kingdom"),
		#peace with no truce or provocation

		(try_begin),
			(ge, "$cheat_mode", 1),
			(display_message, "@{!}DEBUG -- {s15} is strongest kingdom"),
		(try_end),

		
		(faction_get_slot, ":actor_strength", ":actor_faction", slot_faction_temp_slot),
		(faction_get_slot, ":target_strength", ":target_faction", slot_faction_temp_slot),
		(store_sub, ":strength_difference", ":actor_strength", ":target_strength"),
		##diplomacy start+ Include bonus from alliance
		(store_sub, reg0, ":actor_offensive_score", ":target_defensive_score"),
		(this_or_next|ge, reg0, 30),
		##diplomacy end+
		(ge, ":strength_difference", 30),

		(try_begin),
			(ge, "$cheat_mode", 1),
			(display_message, "@{!}DEBUG -- {s15} has 30 point advantage over {s16}"),
		(try_end),

		
		(assign, ":nearby_center_found", 0),
		(try_for_range, ":actor_faction_walled_center", walled_centers_begin, walled_centers_end),
			(store_faction_of_party, ":walled_center_faction_1", ":actor_faction_walled_center"),
			(eq, ":walled_center_faction_1", ":actor_faction"), 
			(try_for_range, ":target_faction_walled_center", walled_centers_begin, walled_centers_end),
				(store_faction_of_party, ":walled_center_faction_2", ":target_faction_walled_center"),
				(eq, ":walled_center_faction_2", ":target_faction"),
				(store_distance_to_party_from_party, ":distance", ":target_faction_walled_center", ":actor_faction_walled_center"),
				#gekokujo 3.0 new strategic ai -- longer distances allowed
				(lt, ":distance", 60),
				#(lt, ":distance", 25),
				(assign, ":nearby_center_found", 1),
			(try_end),
		(try_end),
		(eq, ":nearby_center_found", 1),
		
		
		(try_begin),
			(ge, "$cheat_mode", 1),
			(display_message, "@{!}DEBUG -- {s15} has proximity to {s16}"),
		(try_end),
		
		(assign, ":result", -1),
		(assign, ":explainer_string", "str_s12s15_declared_war_to_control_calradia"),
		
	(else_try),	
		(lt, ":modified_honor_and_relation", -20),
		
		(assign, ":result", 0),
		(assign, ":explainer_string", "str_s12s15_distrusts_s16_and_fears_that_any_deals_struck_between_the_two_realms_will_not_be_kept"),
		

	#wishes to deal
	(else_try),
		(lt, ":current_faction_relation", 0),
		#gekokujo 3.0 new strategic ai start
		(ge, ":num_third_party_wars", 3),
		#(ge, ":num_third_party_wars", 2),
		#gekokujo 3.0 new strategic ai end
		(assign, ":result", 3),
		
		(assign, ":explainer_string", "str_s12s15_is_at_war_on_too_many_fronts_and_eager_to_make_peace_with_s16"),
	(else_try),
		(gt, ":active_mutual_enemy", 0),
		(eq, ":actor_centers_held_by_target", 0),
		(this_or_next|ge, ":current_faction_relation", 0),
			#gekokujo 2.1 enabled faction border-checking
			(eq, ":two_factions_share_border", 0),
			#(eq, 1, 1),
			
		(assign, ":result", 3),
		(str_store_faction_name, s17, ":active_mutual_enemy"),
		##diplomacy start+
		#(troop_get_type, reg4, ":actor_leader"),#<- commented out
		##diplomacy end+
		(assign, ":explainer_string", "str_s12s15_seems_to_think_that_s16_and_reg4shehe_have_a_common_enemy_in_the_s17"),
		
	(else_try),
		(eq, ":war_peace_truce_status", -2),
		(ge, ":hours_since_last_decisive_event", 720),

		##diplomacy start+
		#(troop_get_type, reg4, ":actor_leader"),#<- commented out
		##diplomacy end+
		
		(assign, ":result", 2),
		(assign, ":explainer_string", "str_s12s15_feels_frustrated_by_reg4herhis_inability_to_strike_a_decisive_blow_against_s16"),
	
		
	(else_try),
		(lt, ":current_faction_relation", 0),
		#gekokujo 3.0 new strategic ai start
		(gt, ":war_damage_suffered", 150),
		#(gt, ":war_damage_suffered", 100),
		#gekokujo 3.0 new strategic ai end
		
		#gekokujo 3.0 new strategic ai -- war damage fix
		(store_mul, ":war_damage_suffered_x_2", ":war_damage_suffered", 2),
		#(val_mul, ":war_damage_suffered_x_2", 2),
		(lt, ":war_damage_inflicted", ":war_damage_suffered_x_2"),

		(assign, ":result", 2),
		(assign, ":explainer_string", "str_s12s15_has_suffered_enough_in_the_war_with_s16_for_too_little_gain_and_is_ready_to_pursue_a_peace"),
		
	(else_try),	
		(gt, ":third_party_war", 0),
		(ge, ":modified_honor_and_relation", 0),
		(lt, ":current_faction_relation", 0),

		(assign, ":result", 1),
		(str_store_faction_name, s17, ":third_party_war"),
		(assign, ":explainer_string", "str_s12s15_would_like_to_firm_up_a_truce_with_s16_to_respond_to_the_threat_from_the_s17"),
	(else_try),
		(gt, ":third_party_war", 0),
		(ge, ":modified_honor_and_relation", 0),

		(assign, ":result", 1),
		(str_store_faction_name, s17, ":third_party_war"),
		(assign, ":explainer_string", "str_s12s15_wishes_to_be_at_peace_with_s16_so_as_to_pursue_the_war_against_the_s17"),
	(else_try),
		#gekokujo 3.0 new strategic ai start
		(gt, ":strength_ratio", 263),
		#(gt, ":strength_ratio", 175),
		#gekokujo 3.0 new strategic ai end
		#gekokujo 2.1 re-enabled border checking
		(eq, ":two_factions_share_border", 1),
		
		(assign, ":result", 1),
		(assign, ":explainer_string", "str_s12s15_seems_to_be_intimidated_by_s16_and_would_like_to_avoid_hostilities"),
	(else_try),
		(lt, ":current_faction_relation", 0),
		
		(assign, ":result", 1),
		(assign, ":explainer_string", "str_s12s15_has_no_particular_reason_to_continue_the_war_with_s16_and_would_probably_make_peace_if_given_the_opportunity"),
	(else_try),
		(assign, ":result", 1),
		(assign, ":explainer_string", "str_s12s15_seems_to_be_willing_to_improve_relations_with_s16"),
	(try_end),
	##diplomacy start+
	#Possibly change the concession demanded
	(try_begin),
		(gt, "$g_concession_demanded", 0),
		(gt, ":last_center_lost", 0),
		(neq, "$g_concession_demanded", ":last_center_lost"),
		(try_begin),
			#This logically can't happen due to the order centers appear in
			(is_between, "$g_concession_demanded", towns_begin, towns_end),
			(neg|is_between, ":last_center_lost", towns_begin, towns_end),#Do not replace
		(else_try),
			(is_between, ":last_center_lost", towns_begin, towns_end),
			(neg|is_between, "$g_concession_demanded", towns_begin, towns_end),
			(assign, "$g_concession_demanded", ":last_center_lost"),
		(else_try),
			(party_slot_eq, ":last_center_lost", slot_center_original_faction, ":actor_faction"),
			(neg|party_slot_eq, "$g_concession_demanded", slot_center_original_faction, ":actor_faction"),
			(assign, "$g_concession_demanded", ":last_center_lost"),
		(try_end),
		(eq, "$g_concession_demanded", ":last_center_lost"),
		(str_store_party_name, s18, "$g_concession_demanded"),#change s18 to match
	(try_end),
	##diplomacy end+
	(str_store_string, s14, ":explainer_string"),
	(assign, reg0, ":result"),
	(assign, reg1, ":explainer_string"),
	
	]),
	("npc_decision_checklist_male_guardian_assess_suitor", #parameters from dialog
	[
	(store_script_param, ":lord", 1),
	(store_script_param, ":suitor", 2),
	
	(troop_get_slot, ":lord_reputation", ":lord", slot_lord_reputation_type),
	(store_faction_of_troop, ":lord_faction", ":lord"),
	
	(try_begin),
		(eq, ":suitor", "trp_player"),
		(assign, ":suitor_faction", "$players_kingdom"),
	(else_try),
		(store_faction_of_troop, ":suitor_faction", ":suitor"),
	(try_end),
	(store_relation, ":faction_relation_with_suitor", ":lord_faction", ":suitor_faction"),
	
	(call_script, "script_troop_get_relation_with_troop", ":lord", ":suitor"),
	(assign, ":lord_suitor_relation", reg0),
	


	(troop_get_slot, ":suitor_renown", ":suitor", slot_troop_renown),


	(assign, ":competitor_found", -1),
	
	(try_begin),
		(eq, ":suitor", "trp_player"),	
		(gt, "$marriage_candidate", 0),		
			
		(try_for_range, ":competitor", lords_begin, lords_end),
			(store_faction_of_troop, ":competitor_faction", ":competitor"),
			(eq, ":competitor_faction", ":lord_faction"),
			(this_or_next|troop_slot_eq, ":competitor", slot_troop_love_interest_1, "$marriage_candidate"),
			(this_or_next|troop_slot_eq, ":competitor", slot_troop_love_interest_2, "$marriage_candidate"),
				(troop_slot_eq, ":competitor", slot_troop_love_interest_3, "$marriage_candidate"),
			
			(call_script, "script_troop_get_relation_with_troop", ":competitor", ":lord"),
			(gt, reg0, 5),

			(troop_slot_ge, ":competitor", slot_troop_renown, ":suitor_renown"),  #higher renown than player
			
			(assign, ":competitor_found", ":competitor"),
			(str_store_troop_name, s14, ":competitor"),
			(str_store_troop_name, s16, "$marriage_candidate"),
		(try_end),
	(try_end),
	
	#renown	
	(try_begin),
		(lt, ":suitor_renown", 50),
		(this_or_next|troop_slot_eq, ":lord", slot_lord_reputation_type, lrep_quarrelsome),
		(this_or_next|troop_slot_eq, ":lord", slot_lord_reputation_type, lrep_debauched),
			(troop_slot_eq, ":lord", slot_lord_reputation_type, lrep_selfrighteous),
		(assign, ":explainer_string", "str_excuse_me_how_can_you_possibly_imagine_yourself_worthy_to_marry_into_our_family"),
		(assign, ":result", -3),
	(else_try),	
		(lt, ":suitor_renown", 50),
		(troop_slot_eq, ":lord", slot_lord_reputation_type, lrep_goodnatured),
		
		(assign, ":explainer_string", "str_em_with_regard_to_her_ladyship_we_were_looking_specifically_for_a_groom_of_some_distinction_fight_hard_count_your_dinars_and_perhaps_some_day_in_the_future_we_may_speak_of_such_things_my_good_man"),
		(assign, ":result", -1),
	(else_try),
		(lt, ":suitor_renown", 50),
	
		(assign, ":explainer_string", "str_em_with_regard_to_her_ladyship_we_were_looking_specifically_for_a_groom_of_some_distinction"),
		(assign, ":result", -2),
		
	(else_try),
		(lt, ":suitor_renown", 200),
		(neg|troop_slot_eq, ":lord", slot_lord_reputation_type, lrep_goodnatured),
		(assign, ":explainer_string", "str_it_is_too_early_for_you_to_be_speaking_of_such_things_you_are_still_making_your_mark_in_the_world"),

		(assign, ":result", -1),
		
	(else_try), #wrong faction
		(eq, ":suitor", "trp_player"),
		(neq, ":suitor_faction", "$players_kingdom"),
		(str_store_faction_name, s4, ":lord_faction"),
		(this_or_next|eq, ":lord_reputation", lrep_quarrelsome),
			(eq, ":lord_reputation", lrep_debauched),
		(assign, ":explainer_string", "str_you_dont_serve_the_s4_so_id_say_no_one_day_we_may_be_at_war_and_i_prefer_not_to_have_to_kill_my_inlaws_if_at_all_possible"),

		(assign, ":result", -1),
		
	(else_try),	
		(eq, ":suitor", "trp_player"),
		(neq, ":suitor_faction", "$players_kingdom"),
		(neq, ":lord_reputation", lrep_goodnatured),
		(neq, ":lord_reputation", lrep_cunning),
	
		(assign, ":explainer_string", "str_as_you_are_not_a_vassal_of_the_s4_i_must_decline_your_request_the_twists_of_fate_may_mean_that_we_will_one_day_cross_swords_and_i_would_hope_not_to_make_a_widow_of_a_lady_whom_i_am_obligated_to_protect"),
		
		(assign, ":result", -1),
	(else_try),	
		(eq, ":suitor", "trp_player"),
		(lt, ":faction_relation_with_suitor", 0),

		(assign, ":explainer_string", "str_as_you_are_not_a_vassal_of_the_s4_i_must_decline_your_request_the_twists_of_fate_may_mean_that_we_will_one_day_cross_swords_and_i_would_hope_not_to_make_a_widow_of_a_lady_whom_i_am_obligated_to_protect"),
		
		(assign, ":result", -1),
		
	(else_try),	
		(eq, ":suitor", "trp_player"),
		(neq, "$player_has_homage", 1),
		(neg|faction_slot_eq, "fac_player_supporters_faction", slot_faction_state, sfs_active),
		
		(assign, ":explainer_string", "str_as_you_are_not_a_pledged_vassal_of_our_liege_with_the_right_to_hold_land_i_must_refuse_your_request_to_marry_into_our_family"),
		
		(assign, ":result", -1),
	(else_try),	
		(gt, ":competitor_found", -1),

		(this_or_next|eq, ":lord_reputation", lrep_selfrighteous),
		(this_or_next|eq, ":lord_reputation", lrep_debauched),
		(this_or_next|eq, ":lord_reputation", lrep_martial),
			(eq, ":lord_reputation", lrep_quarrelsome),
		
		(assign, ":explainer_string",	"str_look_here_lad__the_young_s14_has_been_paying_court_to_s16_and_youll_have_to_admit__hes_a_finer_catch_for_her_than_you_so_lets_have_no_more_of_this_talk_shall_we"),
		(assign, ":result", -1),
		
	(else_try),
		(lt, ":lord_suitor_relation", -4),
		

		
		(assign, ":explainer_string", "str_i_do_not_care_for_you_sir_and_i_consider_it_my_duty_to_protect_the_ladies_of_my_household_from_undesirable_suitors"),
		(assign, ":result", -3),
	(else_try),	
		(lt, ":lord_suitor_relation", 5),

		(assign, ":explainer_string",	"str_hmm_young_girls_may_easily_be_led_astray_so_out_of_a_sense_of_duty_to_the_ladies_of_my_household_i_think_i_would_like_to_get_to_know_you_a_bit_better_we_may_speak_of_this_at_a_later_date"),
		(assign, ":result", -1),
	(else_try),	

		(assign, ":explainer_string",	"str_you_may_indeed_make_a_fine_match_for_the_young_mistress"),
		(assign, ":result", 1),
	(try_end),
	
	(assign, reg0, ":result"),
	(assign, reg1, ":explainer_string"),
	
	]),
	("npc_decision_checklist_marry_female_pc", #
	[
	(store_script_param, ":npc", 1),
    #diplomacy start+ (players of either gender may marry opposite-gender lords)
    #  Note that many of the strings used here have been altered to change based on the player's gender.
	#  Also, it should be mention that reason is written to s14.
	(assign, ":save_reg1", reg1),
	#Use gender script
	(call_script, "script_dplmc_store_is_female_troop_1_troop_2", "trp_player", ":npc"),
	(assign, ":is_female", reg0),
	(assign, ":npc_female", reg1),
    #diplomacy end+

	(troop_get_slot, ":npc_reputation_type", ":npc", slot_lord_reputation_type),
	
	(call_script, "script_troop_get_romantic_chemistry_with_troop", ":npc", "trp_player"),
	(assign, ":romantic_chemistry", reg0),
	
	(call_script, "script_troop_get_relation_with_troop", ":npc", "trp_player"),
	(assign, ":relation_with_player", reg0),
	
	(assign, ":competitor", -1),
	(try_for_range, ":competitor_candidate", kingdom_ladies_begin, kingdom_ladies_end),
		(this_or_next|troop_slot_eq, ":npc", slot_troop_love_interest_1, ":competitor_candidate"),
		(this_or_next|troop_slot_eq, ":npc", slot_troop_love_interest_2, ":competitor_candidate"),
			(troop_slot_eq, ":npc", slot_troop_love_interest_3, ":competitor_candidate"),
		(call_script, "script_troop_get_relation_with_troop", ":npc", ":competitor"),	
		(assign, ":competitor_relation", reg0),
		
		(gt, ":competitor_relation", ":relation_with_player"),
		(assign, ":competitor", ":competitor_candidate"),
	(try_end),

	(assign, ":player_possessions", 0),
	(try_for_range, ":center", centers_begin, centers_end),
		(troop_slot_eq, ":center", slot_town_lord, "trp_player"),
		(val_add, ":player_possessions", 1),
	(try_end),
	
	(assign, ":lord_agrees", 0),
	#reasons for refusal	
	(try_begin), 
		(troop_slot_ge, "trp_player", slot_troop_betrothed, active_npcs_begin),
		(neg|troop_slot_eq, "trp_player", slot_troop_betrothed, ":npc"),
		
		(str_store_string, s14, "str_my_lady_engaged_to_another"),		
	(else_try),
		#bad relationship - minor
		(lt, ":relation_with_player", -3),
		(this_or_next|eq, ":npc_reputation_type", lrep_upstanding),
		(this_or_next|eq, ":npc_reputation_type", lrep_cunning),
		##diplomacy start+ also test commoner types
		(this_or_next|eq, ":npc_reputation_type", lrep_roguish),
		(this_or_next|eq, ":npc_reputation_type", lrep_custodian),
		(this_or_next|eq, ":npc_reputation_type", lrep_benefactor),
		#And certain lady types?
		(this_or_next|eq, ":npc_reputation_type", lrep_ambitious),
		(this_or_next|eq, ":npc_reputation_type", lrep_moralist),
		##diplomacy end+
			(eq, ":npc_reputation_type", lrep_goodnatured),
		
		(str_store_string, s14, "str_madame__given_our_relations_in_the_past_this_proposal_is_most_surprising_i_do_not_think_that_you_are_the_kind_of_woman_who_can_be_bent_to_a_hushands_will_and_i_would_prefer_not_to_have_our_married_life_be_a_source_of_constant_acrimony"),
	
	(else_try), #really bad relationship
		(lt, ":relation_with_player", -10),
	
		(this_or_next|eq, ":npc_reputation_type", lrep_quarrelsome),
		(this_or_next|eq, ":npc_reputation_type", lrep_debauched),
			(eq, ":npc_reputation_type", lrep_selfrighteous),

		(str_store_string, s14, "str_i_would_prefer_to_marry_a_proper_maiden_who_will_obey_her_husband_and_is_not_likely_to_split_his_head_with_a_sword"),
	(else_try),
		(lt, ":romantic_chemistry", 5),

		(str_store_string, s14, "str_my_lady_not_sufficient_chemistry"),
		
	(else_try), #would prefer someone more ladylike
		(this_or_next|eq, ":npc_reputation_type", lrep_upstanding),
			(eq, ":npc_reputation_type", lrep_martial),
        #diplomacy start+ (players of either gender may marry opposite-gender lords)
        #I tried to keep this as symmetric as possible, but this sentence is ridiculous with reversed genders
		(neq, ":npc_female", 1),
        (eq, ":is_female", 1),
		#To reduce annoyance, I've changed this away from an absolute prohibition.
		(troop_get_slot, ":veto", ":npc", slot_troop_set_decision_seed),
		(val_add, ":veto", "$romantic_attraction_seed"),
		(val_mod, ":veto", 5),#4 out of 5 will still automatically refuse
		(try_begin),#make an exception for companions
			#gekokujo 3.0 microfactions! include fort companions start
			#(is_between, ":npc", companions_begin, companions_end),
			(is_between, ":npc", companions_begin, fort_companions_end),
			#gekokujo 3.0 microfactions! include fort companions end
			(assign, ":veto", 0),
		(else_try),
			#On diminished prejudice mode, get rid of the "80% automatically refuse" condition.
			(ge, "$g_disable_condescending_comments", 2),
			(assign, ":veto", 0),
		(try_end),
		(try_begin),
			#Skip the subsequent checks if there's no way for them to pass
			(neq, ":veto", 0),
		(else_try),
			#Requires high chemistry, high relation, and positive honor
			(this_or_next|lt, ":romantic_chemistry", 15),
			(this_or_next|lt, ":relation_with_player", 30),
				(lt, "$player_honor", 10),
			(assign, ":veto", 1),
		(else_try),
			#Relation must be above some arbitrary threshold (only if prejudice settings are not "low")
			(lt, "$g_disable_condescending_comments", 2),
			(store_sub, reg0, 100, ":romantic_chemistry"),
			(lt, ":relation_with_player", reg0),
			(assign, ":veto", 1),
		(else_try),
			#The lord's level must not be less than 75% of the player's (only if prejudice settings are not "low")
			(lt, "$g_disable_condescending_comments", 2),
			(store_character_level, reg0, "trp_player"),
			(val_mul, reg0, 3),
			(val_div, reg0, 4),
			(store_character_level, reg1, ":npc"),
			(lt, reg1, reg0),
			(assign, ":veto", 1),
		(else_try),
			#One of the lord's female relatives must like the player, if any such lords exist.
			(lt, "$g_disable_condescending_comments", 2),
			(troop_get_slot, ":npc_mother", ":npc", slot_troop_mother),
			(assign, reg1, 0),#3 = some disapproved, 2 = some approved, 1 = some existed and had no opinion, 0 = there were none
			(try_for_range, ":kingdom_lady", kingdom_ladies_begin, kingdom_ladies_end),
				(neg|troop_slot_ge, ":kingdom_lady", slot_troop_occupation, slto_retirement),
				(assign, reg0, 0),
				(try_begin),
					(troop_slot_eq, ":kingdom_lady", slot_troop_guardian, ":npc"),
					(assign, reg0, 1),
				(else_try),
					(is_between, ":npc_mother", heroes_begin, heroes_end),
					(this_or_next|eq, ":kingdom_lady", ":npc_mother"),
						(troop_slot_eq, ":kingdom_lady", slot_troop_mother, ":npc_mother"),
					(assign, reg0, 1),
				(try_end),
				(neq, reg0, 0),
				(call_script, "script_troop_get_player_relation", ":kingdom_lady"),
				(try_begin),#some were found and like the player
					(ge, reg0, 1),
					(val_max, reg1, 2),
				(else_try),#some were found and have no opinion
					(eq, reg0, 0),
					(val_max, reg1, 1),
				(else_try),#some were found and dislike the player
					(val_max, reg1, 3),
				(try_end),
			(try_end),
			(neq, reg0, 0),
			(neq, reg0, 2),
			(assign, ":veto", 1),
		(try_end),
		#Check if the veto holds
		(neq, ":veto", 0),
        #diplomacy end+

		(str_store_string, s14, "str_my_lady_while_i_admire_your_valor_you_will_forgive_me_if_i_tell_you_that_a_woman_like_you_does_not_uphold_to_my_ideal_of_the_feminine_of_the_delicate_and_of_the_pure"),
	(else_try),
		(eq, ":npc_reputation_type", lrep_quarrelsome),
		(lt, ":romantic_chemistry", 15),

		(str_store_string, s14, "str_nah_i_want_a_woman_wholl_keep_quiet_and_do_what_shes_told_i_dont_think_thats_you"),
	(else_try), #no properties
		(this_or_next|eq, ":npc_reputation_type", lrep_selfrighteous),
			(eq, ":npc_reputation_type", lrep_debauched),
	
		(ge, ":romantic_chemistry", 10),		
		(eq, ":player_possessions", 0),
		
		(str_store_string, s14, "str_my_lady_you_are_possessed_of_great_charms_but_no_properties_until_you_obtain_some_to_marry_you_would_be_an_act_of_ingratitude_towards_my_ancestors_and_my_lineage"),
		
	(else_try), #you're a nobody - I can do better
		(this_or_next|eq, ":npc_reputation_type", lrep_selfrighteous),
			(eq, ":npc_reputation_type", lrep_debauched),
	
		(eq, ":player_possessions", 0),
		
		(str_store_string, s14, "str_my_lady_you_are_a_woman_of_no_known_family_of_no_possessions__in_short_a_nobody_do_you_think_that_you_are_fit_to_marry_into_may_family"),
	(else_try), #just not that into you
		(lt, ":romantic_chemistry", 5),
		(lt, ":relation_with_player", 20),
		
		(neq, ":npc_reputation_type", lrep_debauched),
		(neq, ":npc_reputation_type", lrep_selfrighteous),
		
		(str_store_string, s14, "str_my_lady__forgive_me__the_quality_of_our_bond_is_not_of_the_sort_which_the_poets_tell_us_is_necessary_to_sustain_a_happy_marriage"),
		
	(else_try), #you're a liability, given your relation with the liege
		(eq, ":npc_reputation_type", lrep_cunning),
		(faction_get_slot, ":leader", slot_faction_leader, "$g_talk_troop_faction"),
		(str_store_troop_name, s4, ":leader"),
		(call_script, "script_troop_get_relation_with_troop", ":leader", "trp_player"),
		(lt, reg0, -10),
		
		(str_store_string, s14, "str_um_i_think_that_if_i_want_to_stay_on_s4s_good_side_id_best_not_marry_you"),
	(else_try),	#part of another faction
		(gt, "$players_kingdom", 0),
		(neq, "$players_kingdom", "$g_talk_troop_faction"),
		(faction_get_slot, ":leader", slot_faction_leader, "$g_talk_troop_faction"),
		##diplomacy start+ use gender script
		#(troop_get_type, reg4, ":leader"),
		(call_script, "script_dplmc_store_troop_is_female_reg", ":leader", 4),
		##diplomacy end+
		
		(str_store_string, s14, "str_you_serve_another_realm_i_dont_see_s4_granting_reg4herhis_blessing_to_our_union"),
	(else_try), #there's a competitor
		(gt, ":competitor", -1),
		(str_store_troop_name, s4, ":competitor"),
		
		(str_store_string, s14, "str_madame_my_heart_currently_belongs_to_s4"),
    ##diplomacy start+
	#By default these should not be reachable, but future changes may expose them
	#unintentionally.
	(else_try),#redundant: shouldn't be called for betrothed lords
	   (troop_slot_ge, ":npc", slot_troop_betrothed, 1),
	   (troop_get_slot, ":competitor", ":npc", slot_troop_betrothed),
	   (str_store_troop_name, s4, ":competitor"),
	   (str_store_string, s14, "str_madame_my_heart_currently_belongs_to_s4"),
	(else_try),#redundant: shouldn't be called for married lords
	   (troop_slot_ge, ":npc", slot_troop_spouse, 1),
	   (troop_get_slot, ":competitor", ":npc", slot_troop_spouse),
	   (str_store_troop_name, s4, ":competitor"),
	   (str_store_string, s14, "str_madame_my_heart_currently_belongs_to_s4"),
	(else_try),#redundant: shouldn't be called for claimants or kings
	   (this_or_next|is_between, ":npc", kings_begin, kings_end),
	      (is_between, ":npc", pretenders_begin, pretenders_end),
	   #This probably wouldn't ever occur, but put a string here just in case.
	   #The male version is ridiculous.
	   (str_store_string, s14, "str_my_lady_while_i_admire_your_valor_you_will_forgive_me_if_i_tell_you_that_a_woman_like_you_does_not_uphold_to_my_ideal_of_the_feminine_of_the_delicate_and_of_the_pure"),
	##diplomacy end+
	#gekokujo 3.0 lords don't marry freelancer players! start
	(else_try),
	   (neq, "$freelancer_state", 0), #no, seriously, do not marry freelancers
	   (str_store_string, s14, "str_you_are_a_freelancer_troop"), #don't!
	#gekokujo 3.0 lords don't marry freelancer players! end
	(else_try),
		(lt, ":relation_with_player", 10),
		(assign, ":lord_agrees", 2),

		(str_store_string, s14, "str_my_lady_you_are_a_woman_of_great_spirit_and_bravery_possessed_of_beauty_grace_and_wit_i_shall_give_your_proposal_consideration"),
	(else_try),
		(assign, ":lord_agrees", 1),

		(str_store_string, s14, "str_my_lady_you_are_a_woman_of_great_spirit_and_bravery_possessed_of_beauty_grace_and_wit_i_would_be_most_honored_were_you_to_become_my_wife"),
	(try_end),

    ##diplomacy start+ revert register
	(assign, reg1, ":save_reg1"),
	##diplomacy end+
	(assign, reg0, ":lord_agrees"),

	]
	),
	("npc_decision_checklist_take_stand_on_issue",
	#Called from dialogs, and from simple_triggers
	
	#This a very inefficient checklist, and if I did it again, I would score for each troop. That way the troop could answer "why not" to an individual lord
	[
	(store_script_param, ":troop_no", 1),
	(store_faction_of_troop, ":troop_faction", ":troop_no"),
	
	(assign, ":result", -1),
	(faction_get_slot, ":faction_issue", ":troop_faction", slot_faction_political_issue),
	
	(assign, ":player_declines_honor", 0),
	(try_begin),
		(is_between, ":faction_issue", centers_begin, centers_end),
	    (gt, "$g_dont_give_fief_to_player_days", 1),
		(assign, ":player_declines_honor", 1),
	(else_try),
	    (gt, "$g_dont_give_marshalship_to_player_days", 1),
		(assign, ":player_declines_honor", 1),	
	(try_end),

	##diplomacy start+
	(faction_get_slot, ":faction_leader", ":troop_faction", slot_faction_leader),
	(call_script, "script_dplmc_is_affiliated_family_member", ":troop_no"),
	(assign, ":affiliated_with_player", reg0),

	(assign, ":subaltern_gender", -1),#The gender subject to sexism (as far as leadership is concerned).
	(try_begin),
		(lt, "$g_disable_condescending_comments", 2),#Prejudice not disabled
		(neg|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_cunning),#Don't bother with the rest of the check
		(neg|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_goodnatured),#if the lord has an unbiased outlook.
		(neg|troop_slot_ge, ":troop_no", slot_lord_reputation_type, lrep_roguish),
		(call_script, "script_dplmc_store_troop_is_female", ":troop_no"),
		(store_sub, ":subaltern_gender", 1, reg0),
		(try_begin),
			(call_script, "script_cf_dplmc_faction_has_bias_against_gender", ":troop_faction", ":subaltern_gender"),
		(else_try),
			(assign, ":subaltern_gender", -1),
		(try_end),
	(try_end),

	(assign, ":faction_lord_count", 0),#Keep track of the number of lords in the faction
	##diplomacy end+

	(assign, ":total_faction_renown", 0),
	(troop_set_slot, "trp_player", slot_troop_temp_slot, 0),
	(try_begin),
		(eq, "$players_kingdom", ":troop_faction"),
		(eq, "$player_has_homage", 1),
		(troop_get_slot, ":total_faction_renown", "trp_player", slot_troop_renown),
		##diplomacy start+
		#Increment the faction lord count
		(val_add, ":faction_lord_count", 1),

		(try_begin),
			(lt, "$g_disable_condescending_comments", 0),#If the player has set the prejudice mode to "high"
			(eq, ":subaltern_gender", "$character_gender"),
			(val_mul, ":total_faction_renown", 4),
			(val_add, ":total_faction_renown", 3),
			(val_div, ":total_faction_renown", 5),
		(try_end),
		##diplomacy end+
	(try_end),

##diplomacy start+
	(try_for_range, ":active_npc", heroes_begin, heroes_end),#Changed range to include kingdom ladies
	    (troop_set_slot, ":active_npc", dplmc_slot_troop_temp_slot, 0), #this will hold distance to closest owned fief
##diplomacy end+
		(troop_set_slot, ":active_npc", slot_troop_temp_slot, 0), #reset to zero
	
		(store_faction_of_troop, ":active_npc_faction", ":active_npc"),
		(eq, ":active_npc_faction", ":troop_faction"),
		(troop_slot_eq, ":active_npc", slot_troop_occupation, slto_kingdom_hero),
		
		(troop_get_slot, ":renown", ":active_npc", slot_troop_renown),
		##diplomacy start+
		#Increment the faction lord count
		(val_add, ":faction_lord_count", 1),

		(try_begin),#If the player has set the prejudice mode to "high".
			(lt, "$g_disable_condescending_comments", 0),#If the player has set the prejudice mode to "high"
			(call_script, "script_dplmc_store_troop_is_female", ":active_npc"),
			(eq, reg0, ":subaltern_gender"),
			(val_mul, ":renown", 4),
			(val_add, ":renown", 3),
			(val_div, ":renown", 5),
		(try_end),
		##diplomacy end+
		(val_add, ":total_faction_renown", ":renown"),
	(try_end),
	
	
	(assign, ":total_faction_center_value", 0),
	(try_for_range, ":center", centers_begin, centers_end),
		(store_faction_of_party, ":center_faction", ":center"),
		(eq, ":center_faction", ":troop_faction"),
		
		(assign, ":center_value", 1),
		(try_begin),
		##diplomacy start+
		#Use different scoring scheme
			(ge, "$g_dplmc_ai_changes", DPLMC_AI_CHANGES_LOW),
			(try_begin),
			   (party_slot_eq, ":center", slot_party_type, spt_town),
  			   (assign, ":center_value", 3),
			(else_try),
			   (neg|party_slot_eq, ":center", slot_party_type, spt_village),
			   (this_or_next|party_slot_eq, ":center", slot_party_type, spt_castle),
				(is_between, ":center", walled_centers_begin, walled_centers_end),
			   (assign, ":center_value", 2),
			(try_end),
		#Otherwise fall through to old behavior
		(else_try),
		##diplomacy end+
			(is_between, ":center", towns_begin, towns_end),
			(assign, ":center_value", 2),
		(try_end),
		
		(val_add, ":total_faction_center_value", ":center_value"),
		
		(party_get_slot, ":town_lord", ":center", slot_town_lord),
		##diplomacy start+
		#The rest of the script assumes that non-player lords are heroes,
		#so add that condition here to get the count right.
		#(gt, ":town_lord", -1),
		(this_or_next|eq, ":town_lord", "trp_player"),
			(is_between, ":town_lord", heroes_begin, heroes_end),

		#Calculate distance for alternate scoring if the issue is a center
		(try_begin),
			(is_between, ":faction_issue", centers_begin, centers_end),
			(neq, ":center", ":faction_issue"),
			(troop_get_slot, ":dplmc_temp_slot", ":town_lord", dplmc_slot_troop_temp_slot),
			(store_distance_to_party_from_party, reg0, ":center", ":faction_issue"),
			(gt, reg0, 0),
			(try_begin),
				(eq, ":dplmc_temp_slot", 0),
				(assign, ":dplmc_temp_slot", reg0),
			(else_try),
				(val_min, ":dplmc_temp_slot", reg0),
			(try_end),
			(troop_set_slot, ":town_lord", dplmc_slot_troop_temp_slot, ":dplmc_temp_slot"),
		(try_end),
		##diplomacy end+

		(troop_get_slot, ":temp_slot", ":town_lord", slot_troop_temp_slot),
		(val_add, ":temp_slot", ":center_value"),
		(troop_set_slot, ":town_lord", slot_troop_temp_slot, ":temp_slot"),
	(try_end),
	(val_max, ":total_faction_center_value", 1),
	
	(store_div, ":average_renown_per_center_point", ":total_faction_renown", ":total_faction_center_value"),
	##diplomacy start+
	(val_max, ":faction_lord_count", 1),

#	(store_mul, ":avg_renown_plus_500_per_cp", ":faction_lord_count", 500),
#	(val_add, ":avg_renown_plus_500_per_cp", ":total_faction_renown"),
#	(store_add, reg0, ":total_faction_center_value", ":faction_lord_count"),
#	(val_div, ":avg_renown_plus_500_per_cp", reg0),

	#Get the standard deviation of renown per center point
	(assign, ":renown_per_center_point_variance", 0),
#	(assign, ":renown_plus_500_per_center_point_variance", 0),

	(try_for_range, ":active_npc", active_npcs_including_player_begin, heroes_end),
		(store_sub, ":active_npc_faction", ":troop_faction", 1),#guaranteed not to equal
		(try_begin),
			#handle player
			(eq, ":active_npc", active_npcs_including_player_begin),
			(assign, ":active_npc", "trp_player"),
			(eq, "$players_kingdom", ":troop_faction"),
			(eq, "$player_has_homage", 1),
			(assign, ":active_npc_faction", ":troop_faction"),
		(else_try),
			#handle kingdom heroes
			(troop_slot_eq, ":active_npc", slot_troop_occupation, slto_kingdom_hero),
			(store_faction_of_troop, ":active_npc_faction", ":active_npc"),
		(try_end),

		(eq, ":active_npc_faction", ":troop_faction"),

		(troop_get_slot, ":renown", ":active_npc", slot_troop_renown),
		(try_begin),
			(lt, "$g_disable_condescending_comments", 0),#If the player has set the prejudice mode to "high"
			(call_script, "script_dplmc_store_troop_is_female", ":active_npc"),
			(eq, reg0, ":subaltern_gender"),
			(val_mul, ":renown", 4),
			(val_add, ":renown", 3),
			(val_div, ":renown", 5),
		(try_end),
		(troop_get_slot, ":center_points", ":active_npc", slot_troop_temp_slot),
		#Variance for renown / center points
		(val_max, ":center_points", 1),
		(store_div, reg0, ":renown", ":center_points"),
		(val_sub, reg0, ":average_renown_per_center_point"),
		(val_mul, reg0, reg0),
		(val_add, ":renown_per_center_point_variance", reg0),

#		#Variance for renown + 500 / center points + 1
#		(troop_get_slot, ":center_points", ":active_npc", slot_troop_temp_slot),
#		(val_add, ":center_points", 1),
#		(store_add, reg0, ":renown", 500),
#		(val_div, reg0, ":center_points"),
#		(val_sub, reg0, ":avg_renown_plus_500_per_cp"),
#		(val_mul, reg0, reg0),
#		(val_add, ":renown_plus_500_per_center_point_variance", reg0),
	(try_end),

	#Get renown per center point standard deviation, or 10%, whichever is greater
	(store_div, reg0, ":faction_lord_count", 2),#for rounding
	(val_add, ":renown_per_center_point_variance", reg0),
	(val_div, ":renown_per_center_point_variance", 	":faction_lord_count"),

	(assign, reg0, ":renown_per_center_point_variance"),
	(convert_to_fixed_point, reg0),
	(store_sqrt, reg0, reg0),
	(convert_from_fixed_point, reg0),
	(assign, ":renown_per_center_point_standard_deviation", reg0),
	(val_add, reg0, 5),
	(val_div, reg0, 10),
	(val_max, ":renown_per_center_point_standard_deviation", reg0),
	(store_sub, ":renown_low_target", ":average_renown_per_center_point", ":renown_per_center_point_standard_deviation"),
	(val_max, ":renown_low_target", 0),

#	#Get (renown + 500) per (center point plus one) standard deviation, or 10%, whichever is greater
#	(store_div, reg0, ":faction_lord_count", 2),#for rounding
#	(val_add, ":renown_plus_500_per_center_point_variance", reg0),
#	(val_div, ":renown_plus_500_per_center_point_variance", ":faction_lord_count"),
#
#	(assign, reg0, ":renown_plus_500_per_center_point_variance"),
#	(convert_to_fixed_point, reg0),
#	(store_sqrt, reg0, reg0),
#	(convert_from_fixed_point, reg0),
#	(assign, ":renown_plus_500_per_center_point_standard_deviation", reg0),
#	(val_add, reg0, 5),
#	(val_div, reg0, 10),
#	(val_max, ":renown_plus_500_per_center_point_standard_deviation", reg0),
#	(store_sub, ":renown_500_low_target", ":avg_renown_plus_500_per_cp", ":renown_plus_500_per_center_point_standard_deviation"),
#	(val_max, ":renown_500_low_target", 0),
	##diplomacy end+

	(try_begin),
		(is_between, ":faction_issue", centers_begin, centers_end),
		#NOTE -- The algorithms here might seem a bit repetitive, but are designed that way to create internal cliques among the lords in a faction.
	
	
	
		(try_begin),#If the center is a village, and a lord has no fief, choose him
			(neg|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_debauched),
			(neg|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_selfrighteous),
			(neg|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_quarrelsome),
			
			(is_between, ":faction_issue", villages_begin, villages_end),
			(assign, ":favorite_lord_without_center", -1),
			(assign, ":score_to_beat", -1),
			##diplomacy start+
			(try_begin),
				#With changes enabled, widen the range of scores to check for certain personality types
				(ge, "$g_dplmc_ai_changes", DPLMC_AI_CHANGES_MEDIUM),
				(try_begin),
					(this_or_next|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_goodnatured),
					(this_or_next|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_upstanding),
					(this_or_next|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_benefactor),
					(this_or_next|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_conventional),
					(this_or_next|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_moralist),
					(this_or_next|is_between, ":troop_no", kings_begin, kings_end),
						(is_between, ":troop_no", pretenders_begin, pretenders_end),
					(assign, ":score_to_beat", -6),#-5 or better is indifferent
				(else_try),
					(ge, ":faction_leader", 0),
					(this_or_next|eq, ":faction_leader", ":troop_no"),
					(this_or_next|troop_slot_eq, ":faction_leader", slot_troop_spouse, ":troop_no"),
						(troop_slot_eq, ":troop_no", slot_troop_spouse, ":faction_leader"),
					(assign, ":score_to_beat", -6),#-5 or better is indifferent
				(try_end),
			(try_end),
			##diplomacy end+

			(try_begin),
				(eq, "$players_kingdom", ":troop_faction"),
				(eq, "$player_has_homage", 1),
				(eq, ":player_declines_honor", 0),	
				
				(troop_slot_eq, "trp_player", slot_troop_temp_slot, 0),
				(call_script, "script_troop_get_relation_with_troop", "trp_player", ":troop_no"),
				(assign, ":relation", reg0),
				##diplomacy start+
				#If the player doesn't have prejudice disabled, don't automatically support for a first fief
				(try_begin),
					(this_or_next|neq, ":subaltern_gender", "$character_gender"),
					#gekokujo 3.0 microfactions! include fort companions start
					#(this_or_next|is_between, ":troop_no", companions_begin, companions_end),#Former companions will support the player
					(this_or_next|is_between, ":troop_no", companions_begin, fort_companions_end),
					#gekokujo 3.0 microfactions! include fort companions end
					(this_or_next|troop_slot_eq, ":troop_no", slot_troop_spouse, "trp_player"),#Spouses will support the player
					(troop_slot_eq, "trp_player", slot_troop_spouse, ":troop_no"),
				(else_try),
					(val_sub, ":relation", 20),
				(try_end),
				##diplomacy end+

				(gt, ":relation", ":score_to_beat"),
				(neg|troop_slot_ge, "trp_player", slot_troop_controversy, 75),
				(assign, ":favorite_lord_without_center", "trp_player"),
				(assign, ":score_to_beat", ":relation"),
			(try_end),
			##diplomacy start+  Support promoted kingdom ladise
			#(try_for_range, ":active_npc", active_npcs_begin, active_npcs_end),  #<-- replace this
			(try_for_range, ":active_npc", heroes_begin, heroes_end),
			##diplomacy end+
				(store_faction_of_troop, ":active_npc_faction", ":active_npc"),
				(eq, ":active_npc_faction", ":troop_faction"),
				(troop_slot_eq, ":active_npc", slot_troop_occupation, slto_kingdom_hero),
			
				(troop_slot_eq, ":active_npc", slot_troop_temp_slot, 0),
				(try_begin),
					(eq, ":active_npc", ":troop_no"),
					(assign, ":relation", 50),
				(else_try),	
					(call_script, "script_troop_get_relation_with_troop", ":active_npc", ":troop_no"),
					(assign, ":relation", reg0),
				(try_end),
				##diplomacy start+ Disadvantage the subaltern gender
				(call_script, "script_dplmc_store_troop_is_female", ":troop_no"),
				(try_begin),
					(eq, reg0, ":subaltern_gender"),
					(val_sub, ":relation", 20),
				(try_end),
				##diplomacy end+
				(neg|troop_slot_ge, ":active_npc", slot_troop_controversy, 75),

				(gt, ":relation", ":score_to_beat"),
				(assign, ":favorite_lord_without_center", ":active_npc"),
				(assign, ":score_to_beat", ":relation"),
			(try_end),
			
			(gt, ":favorite_lord_without_center", -1),
			(assign, ":result", ":favorite_lord_without_center"),
			(assign, ":result_explainer", "str_political_explanation_lord_lacks_center"),
		##diplomacy start+
		##Faction leaders are more rational about whom they support.
	   (else_try),
			(ge, "$g_dplmc_ai_changes", DPLMC_AI_CHANGES_MEDIUM),
			(call_script, "script_dplmc_get_troop_standing_in_faction", ":troop_no", ":troop_faction"),
			(ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
			(assign, ":best_candidate", -1),
			(assign, ":best_score", -1),
			(assign, ":explanation", 0),
			(try_begin),
			   (eq,"$players_kingdom", ":troop_faction"),
				(eq, "$player_has_homage", 1),
				(eq, ":player_declines_honor", 0),
				(call_script, "script_dplmc_calculate_troop_score_for_center_aux", ":troop_no", "trp_player", ":faction_issue"),#reg0 = score, reg1 = explanation
				(assign, ":best_candidate", "trp_player"),
				(assign, ":best_score", reg0),
				(assign, ":explanation", reg1),
			(try_end),
			(try_for_range, ":active_npc", heroes_begin, heroes_end),
			   (store_faction_of_troop, ":active_npc_faction", ":active_npc"),
				(eq, ":active_npc_faction", ":troop_faction"),
				(troop_slot_eq, ":active_npc", slot_troop_occupation, slto_kingdom_hero),
				(call_script, "script_dplmc_calculate_troop_score_for_center_aux", ":troop_no", ":active_npc", ":faction_issue"),#reg0 = score, reg1 = explanation
				(this_or_next|eq, ":best_candidate", -1),
				   (gt, reg0, ":best_score"),
				(assign, ":best_candidate", ":active_npc"),
				(assign, ":best_score", reg0),
				(assign, ":explanation", reg1),
			(try_end),
			(gt, ":best_candidate", -1),
			(assign, ":result", ":best_candidate"),
			(assign, ":result_explainer", ":explanation"),
		##diplomacy end+
		(else_try),	#taken by troop
			(is_between, ":faction_issue", walled_centers_begin, walled_centers_end),
			(neg|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_debauched),
			(neg|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_selfrighteous),
			(neg|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_cunning),
			
			(party_get_slot, ":last_taken_by_troop", ":faction_issue", slot_center_last_taken_by_troop),
			(try_begin),
				(try_begin),
					(neq, ":troop_faction", "$players_kingdom"),
					(assign, ":last_taken_by_troop", -1),
				(else_try),
					(eq, "$player_has_homage", 0),
					(assign, ":last_taken_by_troop", -1),
				(else_try),
					(eq, ":faction_issue", "$g_castle_requested_by_player"),
					(assign, ":last_taken_by_troop", "trp_player"),
				(else_try),
					(eq, ":faction_issue", "$g_castle_requested_for_troop"),
					(assign, ":last_taken_by_troop", "trp_player"),
				(else_try), #ie, the fellow who took it is no longer in the faction
					(gt, ":last_taken_by_troop", -1),
					(store_faction_of_troop, ":last_take_by_troop_faction", ":last_taken_by_troop"),
					(neq, ":last_take_by_troop_faction", ":troop_faction"),
					(assign, ":last_taken_by_troop", -1),
				(try_end),
			(try_end),	
			(gt, ":last_taken_by_troop", -1),

			(try_begin),
				(eq, "$cheat_mode", 1),
				(gt, ":last_taken_by_troop", -1),
				(str_store_troop_name, s3, ":last_taken_by_troop"),
				(display_message, "@{!}Castle taken by {s3}"),
			(try_end),

			
			(call_script, "script_troop_get_relation_with_troop", ":troop_no", ":last_taken_by_troop"),
			##diplomacy start+
			#If behavior changes are enabled, increase the accepted range for certain personality types.
			(assign, ":relation", reg0),
			(try_begin),
				(ge, "$g_dplmc_ai_changes", DPLMC_AI_CHANGES_MEDIUM),
				(try_begin),
					(troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_martial),
					(val_add, reg0, 5),#i.e. accept at -5 (indifferent) or higher
				(else_try),
					(troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_upstanding),
					(val_add, reg0, 5),#i.e. accept at -5 (indifferent) or higher
				(try_end),
			(try_end),
			##diplomacy end+
			(ge, reg0, 0),
			
			(neg|troop_slot_ge, ":last_taken_by_troop", slot_troop_controversy, 25),
			
			(troop_get_slot, ":renown", ":last_taken_by_troop", slot_troop_renown),
			##diplomacy start+
			(try_begin),
				(lt, "$g_disable_condescending_comments", 0),#If the player has set the prejudice mode to "high"
				(call_script, "script_dplmc_store_troop_is_female", ":last_taken_by_troop"),
				(eq, reg0, ":subaltern_gender"),
				(val_mul, ":renown", 4),
				(val_add, ":renown", 3),
				(val_div, ":renown", 5),
			(try_end),
			##diplomacy end+
			(troop_get_slot, ":center_points", ":last_taken_by_troop", slot_troop_temp_slot),
			(val_max, ":center_points", 1),
			(store_div, ":renown_divided_by_center_points", ":renown", ":center_points"),
			(val_mul, ":renown_divided_by_center_points", 6), #was five
			(val_div, ":renown_divided_by_center_points", 4),
			
			##diplomacy start+
			(try_begin),
				(ge, "$g_dplmc_ai_changes", DPLMC_AI_CHANGES_MEDIUM),
				#Possibly raise renown_divided_by_center_points
				(store_div, reg0, ":renown", ":center_points"),
				(val_add, reg0, ":renown_per_center_point_standard_deviation"),
				(val_max, ":renown_divided_by_center_points", reg0),
			(try_end),
			##diplomacy end+
			(ge, ":renown_divided_by_center_points", ":average_renown_per_center_point"),
			
			
			(assign, ":result", ":last_taken_by_troop"),
			(assign, ":result_explainer", "str_political_explanation_lord_took_center"),
			
			
		#Check self, immediate family
		#This is done instead of a single weighted score to create cliques -- groups of NPCs who support one another
		(else_try),
			(assign, ":most_deserving_close_friend", -1),
			(assign, ":score_to_beat", ":average_renown_per_center_point"),
			(val_div, ":score_to_beat", 3),
			(val_mul, ":score_to_beat", 2),
			
			(try_begin),
				(eq, "$cheat_mode", 1),
				(assign, reg3, ":score_to_beat"),
				(display_message, "@{!}Two-thirds average_renown = {reg3}"),
			(try_end),

			###diplomacy start+
			#(try_begin),
			#	(ge, "$g_dplmc_ai_changes", DPLMC_AI_CHANGES_MEDIUM),
			#	(try_begin),
			#		(eq, "$cheat_mode", 1),
			#		(assign, reg3, ":renown_low_target"),
			#		(display_message, "@{!}Average renown per center minus one standard deviation = {reg3}"),
			#	(try_end),
			#(try_end),
			###diplomacy end+

			(try_begin),
				(eq, "$players_kingdom", ":troop_faction"),
				(eq, "$player_has_homage", 1),
				(eq, ":player_declines_honor", 0),	
				
				(call_script, "script_troop_get_relation_with_troop", "trp_player", ":troop_no"),
				(assign, ":relation", reg0),
				##diplomacy start+
				#If affiliated with player
				(this_or_next|gt, ":affiliated_with_player", 0),
				##diplomacy end+
				(ge, ":relation", 20),
				(neg|troop_slot_ge, "trp_player", slot_troop_controversy, 50),

				(troop_get_slot, ":renown", "trp_player", slot_troop_renown),
				##diplomacy start+
				(try_begin),
					(lt, "$g_disable_condescending_comments", 0),#If the player has set the prejudice mode to "high"
					(eq, ":subaltern_gender", "$character_gender"),
					(val_mul, ":renown", 4),
					(val_add, ":renown", 3),
					(val_div, ":renown", 5),
				(try_end),
				##diplomacy end+
				(troop_get_slot, ":center_points", "trp_player", slot_troop_temp_slot),
				(val_max, ":center_points", 1),
				(store_div, ":renown_divided_by_center_points", ":renown", ":center_points"),
				
				
				(assign, ":most_deserving_close_friend", "trp_player"),
				(assign, ":score_to_beat", ":renown_divided_by_center_points"),
			(try_end),
			##diplomacy start+  Support promoted kingdom ladies
			#(try_for_range, ":active_npc", active_npcs_begin, active_npcs_end), #<- replace
			(try_for_range, ":active_npc", heroes_begin, heroes_end),
			##diplomacy end+
				(store_faction_of_troop, ":active_npc_faction", ":active_npc"),
				(eq, ":active_npc_faction", ":troop_faction"),			
				(troop_slot_eq, ":active_npc", slot_troop_occupation, slto_kingdom_hero),
				
				(call_script, "script_troop_get_relation_with_troop", ":active_npc", ":troop_no"),
				(assign, ":relation", reg0),
				##diplomacy start+
				(assign, reg0, 0),
				#If affiliated with player
				(try_begin),
					(lt, ":relation", 20),
					(gt, ":affiliated_with_player", 0),
					(neq, ":active_npc", ":troop_no"),
					(call_script, "script_dplmc_is_affiliated_family_member", ":troop_no"),
				(try_end),
				(this_or_next|gt, reg0, 0),#<-- both affiliated
				##diplomacy end+
				(this_or_next|eq, ":active_npc", ":troop_no"),
					(ge, ":relation", 20),
				(neg|troop_slot_ge, ":active_npc", slot_troop_controversy, 50),
				(troop_get_slot, ":renown", ":active_npc", slot_troop_renown),
				##diplomacy start+
				(try_begin),
					(lt, "$g_disable_condescending_comments", 0),#If the player has set the prejudice mode to "high"
					(call_script, "script_dplmc_store_troop_is_female", ":active_npc"),
					(eq, reg0, ":subaltern_gender"),
					(val_mul, ":renown", 4),
					(val_add, ":renown", 3),
					(val_div, ":renown", 5),
				(try_end),
				##diplomacy end+
				(troop_get_slot, ":center_points", ":active_npc", slot_troop_temp_slot),
				(val_max, ":center_points", 1),
				(store_div, ":renown_divided_by_center_points", ":renown", ":center_points"),
				
				
				(try_begin),
					(eq, "$cheat_mode", 1),
					(str_store_troop_name, s10, ":active_npc"),
					(assign, reg3, ":renown_divided_by_center_points"),
					(display_message, "@{!}DEBUG -- Colleague test: score for {s10} = {reg3}"),
				(try_end),
				
				
				(gt, ":renown_divided_by_center_points", ":score_to_beat"),
		
				(assign, ":most_deserving_close_friend", ":active_npc"),
				(assign, ":score_to_beat", ":renown_divided_by_center_points"),
			(try_end),

			(gt, ":most_deserving_close_friend", -1),
			
			
			(assign, ":result", ":most_deserving_close_friend"),
			(assign, ":result_explainer", "str_political_explanation_most_deserving_friend"),
			

			
		(else_try),
		#Most deserving in entire faction, minus those with no relation
			(neg|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_debauched),
			(neg|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_selfrighteous),
			(neg|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_quarrelsome),
		
			(assign, ":most_deserving_in_faction", -1),
			(assign, ":score_to_beat", 0),
			
			(try_begin),
				(eq, "$players_kingdom", ":troop_faction"),
				(eq, "$player_has_homage", 1),
				(eq, ":player_declines_honor", 0),	
				
				(call_script, "script_troop_get_relation_with_troop", "trp_player", ":troop_no"),
				(assign, ":relation", reg0),
				(ge, ":relation", 0),
				(troop_get_slot, ":renown", "trp_player", slot_troop_renown),
				##diplomacy start+
				(try_begin),
					(lt, "$g_disable_condescending_comments", 0),#If the player has set the prejudice mode to "high"
					(eq, ":subaltern_gender", "$character_gender"),
					(val_mul, ":renown", 4),
					(val_add, ":renown", 3),
					(val_div, ":renown", 5),
				(try_end),
				##diplomacy end+
				(troop_get_slot, ":center_points", "trp_player", slot_troop_temp_slot),
				(neg|troop_slot_ge, "trp_player", slot_troop_controversy, 25),

				(val_max, ":center_points", 1),
				(store_div, ":renown_divided_by_center_points", ":renown", ":center_points"),
				
				(assign, ":most_deserving_in_faction", "trp_player"),
				(assign, ":score_to_beat", ":renown_divided_by_center_points"),
			(try_end),
			##diplomacy start+ add support for promoted kingdom ladies
			#(try_for_range, ":active_npc", active_npcs_begin, active_npcs_end),
			(try_for_range, ":active_npc", heroes_begin, heroes_end),
			   (this_or_next|is_between, ":active_npc", active_npcs_begin, active_npcs_end),
			      (troop_slot_eq, ":active_npc", slot_troop_occupation, slto_kingdom_hero),
			##diplomacy end+
				(store_faction_of_troop, ":active_npc_faction", ":active_npc"),
				(eq, ":active_npc_faction", ":troop_faction"),			
				(troop_slot_eq, ":active_npc", slot_troop_occupation, slto_kingdom_hero),

				(call_script, "script_troop_get_relation_with_troop", ":active_npc", ":troop_no"),
				(assign, ":relation", reg0),
				(this_or_next|eq, ":active_npc", ":troop_no"),
					(ge, ":relation", 0),
				(neg|troop_slot_ge, ":active_npc", slot_troop_controversy, 25),

				(troop_get_slot, ":renown", ":active_npc", slot_troop_renown),
				##diplomacy start+
				(try_begin),
					(lt, "$g_disable_condescending_comments", 0),#If the player has set the prejudice mode to "high"
					(call_script, "script_dplmc_store_troop_is_female", ":active_npc"),
					(eq, reg0, ":subaltern_gender"),
					(val_mul, ":renown", 4),
					(val_add, ":renown", 3),
					(val_div, ":renown", 5),
				(try_end),
				##diplomacy end+
				(troop_get_slot, ":center_points", ":active_npc", slot_troop_temp_slot),
				(val_max, ":center_points", 1),
				
				(store_div, ":renown_divided_by_center_points", ":renown", ":center_points"),
				(gt, ":renown_divided_by_center_points", ":score_to_beat"),

				(try_begin),
					(eq, "$cheat_mode", 1),
					(str_store_string, s10, ":active_npc"),
					(assign, reg3, ":renown_divided_by_center_points"),
					(display_message, "@{!}DEBUG -- Open test: score for {s10} = {reg3}"),
				(try_end),

				
				(assign, ":most_deserving_in_faction", ":active_npc"),
				(assign, ":score_to_beat", ":renown_divided_by_center_points"),
			(try_end),

			
			(gt, ":most_deserving_in_faction", -1),
			(assign, ":result", ":most_deserving_in_faction"),
			(assign, ":result_explainer", "str_political_explanation_most_deserving_in_faction"),
		##diplomacy start+
		(else_try),
			#The lord wasn't able to find any suitable candidates,
			#so now we perform the evaluation from another perspective.
			(ge, "$g_dplmc_ai_changes", DPLMC_AI_CHANGES_LOW),
			#DPLMC_AI_CHANGES >= LOW
			#DPLMC_AI_CHANGES >= MEDIUM   XOR   status >= DPLMC_FACTION_STANDING_LEADER_SPOUSE
			(call_script, "script_dplmc_get_troop_standing_in_faction", ":troop_no", ":troop_faction"),
			(this_or_next|ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
				(ge, "$g_dplmc_ai_changes", DPLMC_AI_CHANGES_MEDIUM),
			(this_or_next|lt, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
				(lt, "$g_dplmc_ai_changes", DPLMC_AI_CHANGES_MEDIUM),
			(assign, ":save_reg1", reg1),

			(assign, ":score_to_beat", 0),
			(assign, ":most_deserving_in_faction", -1),
			#(assign, ":tmp_explanation", 0),

			(try_for_range, ":active_npc", active_npcs_including_player_begin, heroes_end),
				(store_sub, ":active_npc_faction", ":troop_faction", 1),
				(try_begin),
					(eq, ":active_npc", active_npcs_including_player_begin),
					(assign, ":active_npc", "trp_player"),
					(eq, "$players_kingdom", ":troop_faction"),
					(eq, "$player_has_homage", 1),
					(assign, ":active_npc_faction", ":troop_faction"),
				(else_try),
					(troop_slot_eq, ":active_npc", slot_troop_occupation, slto_kingdom_hero),
					(store_faction_of_troop, ":active_npc_faction", ":active_npc"),
				(try_end),
				(eq, ":active_npc_faction", ":troop_faction"),

				#(call_script, "script_dplmc_aux_troop_evaluate_troop_for_center", ":troop_no", ":active_npc", ":faction_issue"),#reg0 = score, reg1 = explanation
				(call_script, "script_dplmc_calculate_troop_score_for_center_aux", ":troop_no", ":active_npc", ":faction_issue"),#reg0 = score, reg1 = explanation

				(this_or_next|eq, ":most_deserving_in_faction", -1),
					(ge, reg0, ":score_to_beat"),
				(assign, ":score_to_beat", reg0),
            (assign, ":result_explainer", reg1),
				(assign, ":most_deserving_in_faction", ":active_npc"),
			(try_end),

			(gt, ":most_deserving_in_faction", -1),
			(assign, ":result", ":most_deserving_in_faction"),
			#(assign, ":result_explainer", ":result_explainer"),#unneeded
         (assign, reg1, ":save_reg1"),
		##diplomacy end+
		(else_try),
			(assign, ":result", ":troop_no"),
			(assign, ":result_explainer", "str_political_explanation_self"),
		(try_end),

		
	(else_try),
		(eq, ":faction_issue", 1),
		
		(assign, ":relationship_threshhold", 15),
		(try_begin),
			(troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_upstanding),
			(assign, ":relationship_threshhold", 5),
		(else_try),
			(troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_debauched),
			(assign, ":relationship_threshhold", 25),
		(try_end),
		
		#For marshals, score marshals according to renown divided by controversy - first for friends and family, then for everyone
		(assign, ":marshal_candidate", -1),
		(assign, ":score_to_beat", 0),
		(try_begin),
			(eq, "$players_kingdom", ":troop_faction"),
			(eq, "$player_has_homage", 1),
			(eq, "$g_player_is_captive", 0),
			(eq, ":player_declines_honor", 0),	
			
			
			(call_script, "script_troop_get_relation_with_troop", "trp_player", ":troop_no"),
			(ge, reg0, ":relationship_threshhold"),
			(party_is_active, "p_main_party"), #gekokujo 3.0 integrating motomataru's campaign AI
			(assign, ":marshal_candidate", "trp_player"),
			(troop_get_slot, ":renown", "trp_player", slot_troop_renown),
			#gekokujo 3.0 integrating motomataru's campaign AI start
			#MOTO avoid electing small parties for marshal
			(store_party_size_wo_prisoners, ":party_size", "p_main_party"),
			(val_add, ":renown", ":party_size"),
			(val_add, ":renown", ":party_size"),
			#MOTO end avoid electing small parties for marshal
			#gekokujo 3.0 integrating motomataru's campaign AI end
			##diplomacy start+
			(try_begin),
				(lt, "$g_disable_condescending_comments", 0),#If the player has set the prejudice mode to "high"
				(eq, ":subaltern_gender", "$character_gender"),
				(val_mul, ":renown", 4),
				(val_add, ":renown", 3),
				(val_div, ":renown", 5),
			(try_end),
			##diplomacy end+
			(troop_get_slot, ":controversy_divisor", "trp_player", slot_troop_controversy),
			(val_add, ":controversy_divisor", 50),
			(store_div, ":score_to_beat", ":renown", ":controversy_divisor"),
		(try_end),
		
      ##diplomacy start+ Support promoted ladies
		#(try_for_range, ":active_npc", active_npcs_begin, active_npcs_end),
		(try_for_range, ":active_npc", heroes_begin, heroes_end),
      ##diplomacy end+
			(store_faction_of_troop, ":active_npc_faction", ":active_npc"),
			(eq, ":active_npc_faction", ":troop_faction"),		
			(troop_slot_eq, ":active_npc", slot_troop_occupation, slto_kingdom_hero),
			(troop_slot_eq, ":active_npc", slot_troop_prisoner_of_party, -1),
			
			(neg|faction_slot_eq, ":troop_faction", slot_faction_leader, ":active_npc"),
			
			(call_script, "script_troop_get_relation_with_troop", ":active_npc", ":troop_no"),
			(assign, ":relation", reg0),
			(this_or_next|eq, ":active_npc", ":troop_no"),
				(ge, ":relation", ":relationship_threshhold"),
				
			(troop_get_slot, ":renown", ":active_npc", slot_troop_renown),
			#gekokujo 3.0 integrating motomataru's campaign AI start
			#MOTO avoid electing small parties for marshal
			(troop_get_slot, ":active_party", ":active_npc", slot_troop_leaded_party),
			(party_is_active, ":active_party"),
			(store_party_size_wo_prisoners, ":party_size", ":active_party"),
			(val_add, ":renown", ":party_size"),
			(val_add, ":renown", ":party_size"),
			#MOTO end avoid electing small parties for marshal
			#gekokujo 3.0 integrating motomataru's campaign AI end
			##diplomacy start+
			(try_begin),
				(lt, "$g_disable_condescending_comments", 0),#If the player has set the prejudice mode to "high"
				(call_script, "script_dplmc_store_troop_is_female", ":troop_no"),
				(eq, reg0, ":subaltern_gender"),
				(val_mul, ":renown", 4),
				(val_add, ":renown", 3),
				(val_div, ":renown", 5),
			(try_end),
			##diplomacy end+
			(troop_get_slot, ":controversy_divisor", ":active_npc", slot_troop_controversy),
			(val_add, ":controversy_divisor", 50),
			(store_div, ":score", ":renown", ":controversy_divisor"),
		
			(gt, ":score", ":score_to_beat"),
			
			(assign, ":marshal_candidate", ":active_npc"),
			(assign, ":score_to_beat", ":score"),
		
		(try_end),
		
		(assign, ":result", ":marshal_candidate"),
		(assign, ":result_explainer", "str_political_explanation_marshal"),
	(try_end),
	
	(try_begin),
		(eq, "$cheat_mode", 1),
		(gt, ":result", -1),
		(str_store_troop_name, s8, ":troop_no"),
		(str_store_troop_name, s9, ":result"),
		(str_store_string, s10, ":result_explainer"),
		(display_message, "@{!}DEBUG -- {s8} backs {s9}:{s10}"),
	(try_end),
	
	(assign, reg0, ":result"),
	(assign, reg1, ":result_explainer"),
	
	]),
	("npc_decision_checklist_evaluate_faction_strategy",
	[
	#Decides whether the strategy is good or bad -- to be added
	]),
 	(
	"npc_decision_checklist_faction_ai_alt", #This is called from within decide_faction_ai, or from 
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
		##diplomacy start+ add support for promoted kingdom ladies
	    #(try_for_range, ":lord", active_npcs_begin, active_npcs_end),
		(try_for_range, ":lord", heroes_begin, heroes_end),
			(this_or_next|is_between, ":lord", active_npcs_begin, active_npcs_end),
				(troop_slot_eq, ":lord", slot_troop_occupation, slto_kingdom_hero),
		##diplomacy end+
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
		  
		  (call_script, "script_find_center_to_attack_alt", ":troop_no", 1, 0),
		  (assign, ":center_to_attack_all_vassals_included", reg0),
		  (assign, ":target_value_level_all_vassals_included", reg1),
		  
		  (call_script, "script_find_center_to_attack_alt", ":troop_no", 1, 1),
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
		  		  
		#gekokujo 3.0 integrating motomataru's campaign AI start
		#(try_begin),
		#  (eq, ":current_ai_state", sfai_attacking_center),
		#  (val_mul, ":target_value_level", 3),
		#  (val_div, ":target_value_level", 2),
		#(try_end),
		#gekokujo 3.0 integrating motomataru's campaign AI end

		(try_begin),
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
            (this_or_next|eq, ":current_ai_state", sfai_default),    #MOTO not going to attack anyway 
            (this_or_next|eq, ":current_ai_state", sfai_feast),    #MOTO not going to attack anyway (THIS is the emergency to stop feast) 
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
			#(party_is_active, ":marshal_party"), #gekokujo 3.0 integrating motomataru's campaign AI start
			(is_between, ":most_threatened_center", walled_centers_begin, walled_centers_end),
                        (this_or_next|eq, ":current_ai_state", sfai_default),    #MOTO not going to attack anyway 
                        (this_or_next|eq, ":current_ai_state", sfai_feast),    #MOTO not going to attack anyway (THIS is the emergency to stop feast)
			(ge, ":threat_danger_level", ":target_value_level"),
			(party_slot_ge, ":most_threatened_center", slot_center_is_besieged_by, 0),

			(assign, ":action", sfai_attacking_enemies_around_center),
			(assign, ":object", ":most_threatened_center"),
						
			(str_store_party_name, s21, ":most_threatened_center"),
			(str_store_string, s14, "str_we_should_ride_to_break_the_siege_of_s21"),
			
		#3b - DEFEAT ENEMIES NEAR CENTER - similar to above, but a different string
		(else_try),
			#(party_is_active, ":marshal_party"), #gekokujo 3.0 integrating motomataru's campaign AI start
                        (this_or_next|eq, ":current_ai_state", sfai_default),    #MOTO not going to attack anyway 
                        (this_or_next|eq, ":current_ai_state", sfai_feast),    #MOTO not going to attack anyway (THIS is the emergency to stop feast)                
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

			(lt, ":hours_at_current_state", 54), #gather army for 54 hours
			
			(lt, ":ratio_of_vassals_assembled", 12),

			(str_store_string, s14, "str_we_must_continue_to_gather_the_army_before_we_ride_forth_on_an_offensive_operation"),
			(assign, ":action", sfai_gathering_army),
			(assign, ":object", -1),

		#7-OFFENSIVE ACTIONS PART 2 : CONTINUE GATHERING
		(else_try),
		    (assign, ":minimum_possible_attackable_target_value_level", 50),
			(eq, ":at_peace_with_everyone", 0),

            (try_begin), #agressive marshal
			  ##diplomacy start+
			  ##OLD:
			  #(troop_get_slot, ":reputation", ":troop_no", slot_lord_reputation_type),
			  #(this_or_next|eq, ":reputation", lrep_martial),
			  #(this_or_next|eq, ":reputation", lrep_quarrelsome),
			  #(eq, ":reputation", lrep_selfrighteous),
			  ##NEW:
			  (call_script, "script_dplmc_store_troop_personality_caution_level", ":troop_no"),
			  (lt, reg0, 0),
			  ##diplomacy end+
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
			  ##diplomacy start+
			  ##OLD:
			  #(troop_get_slot, ":reputation", ":troop_no", slot_lord_reputation_type),
			  #(this_or_next|eq, ":reputation", lrep_martial),
			  #(this_or_next|eq, ":reputation", lrep_quarrelsome),
			  #(eq, ":reputation", lrep_selfrighteous),
			  ##NEW:
			  (call_script, "script_dplmc_store_troop_personality_caution_level", ":troop_no"),
			  (lt, reg0, 0),
			  ##diplomacy end+
			  (val_mul, ":minimum_needed_target_value_level", 9),
			  (val_div, ":minimum_needed_target_value_level", 10),
            (try_end),	  
						
			(le, ":target_value_level", ":minimum_needed_target_value_level"),
			(le, ":hours_at_current_state", 54),
		
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
		(else_try),
			(party_is_active, ":marshal_party"),
			(neq, ":current_ai_state", sfai_default),
			(neq, ":current_ai_state", sfai_feast),
			
			(assign, ":center_to_attack", ":center_to_attack_only_marshal_and_followers"),
			
			(is_between, ":center_to_attack", villages_begin, villages_end),
			
			(ge, ":target_value_level", ":minimum_possible_attackable_target_value_level"),
		
			(assign, ":action", sfai_raiding_village),
			(assign, ":object", ":center_to_attack"),
			(str_store_string, s14, "str_we_shall_leave_a_fiery_trail_through_the_heart_of_the_enemys_lands_targeting_the_wealthy_settlements_if_we_can"),
		
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
			        ##diplomacy start+
					#neither the bride nor the groom is in retirement, dead, etc.
					(neg|troop_slot_ge, ":groom", slot_troop_occupation, slto_retirement),
					(neg|troop_slot_ge, ":kingdom_lady", slot_troop_occupation, slto_retirement),
					##diplomacy end+
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
            (gt, ":hours_since_last_feast_start", 240), #If at least 10 days past after last feast. (added by ozan)

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
		
		#17-DO NOTHING
		(else_try),
			(neq, ":current_ai_state", sfai_default),
		
			(assign, ":action", sfai_default),
			(assign, ":object", -1),		
			(str_store_string, s14, "str_the_circumstances_which_led_to_this_decision_no_longer_apply_so_we_should_stop_and_reconsider_shortly"),	
	
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
]
