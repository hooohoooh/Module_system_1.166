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

dialogs_siege = [
  [anyone|plyr,"siege_won_seneschal_1", [], "Are you the seneschal?", "siege_won_seneschal_2",[]],
  [anyone,"siege_won_seneschal_2", [], "Indeed I am, my {lord/lady}.\
 I have always served the masters of {s1} to the best of my ability, whichever side they might be on.\
 Thus you may count on my utmost loyalty for as long as you are the {lord/lady} of this place.\
 Now, do you intend to keep me on as the seneschal? I promise you will not be disappointed.", "siege_won_seneschal_3",[]],
  [anyone|plyr,"siege_won_seneschal_3", [], "Very well, you may keep your post for the time being.", "siege_won_seneschal_4",[]],
  [anyone|plyr,"siege_won_seneschal_3", [], "You can stay, but I shall be keeping a close watch on you.", "siege_won_seneschal_4",[]],
  [anyone,"siege_won_seneschal_4", [], "Thank you, my {lord/lady}. If you do not mind my impudence,\
 may I inquire as to what you wish to do with the castle?", "siege_won_seneschal_5",[]],
  [anyone|plyr,"siege_won_seneschal_5", [], "I will sell it to another lord.", "siege_won_seneschal_6",[]],
  [anyone|plyr,"siege_won_seneschal_5", [], "I intend to claim it for myself.", "siege_won_seneschal_6",[]],
  [anyone|plyr,"siege_won_seneschal_5", [], "I haven't given it much thought. What are my options?", "siege_won_seneschal_list_options",[]],
  [anyone,"siege_won_seneschal_list_options", [], "According to our laws and traditions,\
 you can do one of several things.\
 First, you could station a garrison here to protect the castle from any immediate counterattacks,\
 then request an audience with some wealthy lord and ask him to make you an offer.\
 It would be worth a tidy sum, believe you me.\
 If you do not wish to sell, then you will have to find yourself a lord and protector who would accept your services.\
 Without a royal investiture and an army at your back, you would have a difficult time holding on to the castle.\
 Both you and {s1} would become great big targets for any man with a few soldiers and a scrap of ambition.\
 ", "siege_won_seneschal_list_options_2",[]],
  [anyone|plyr,"siege_won_seneschal_list_options_2", [], "What do you mean, a lord and protector? I won this place by my own hand, I don't need anyone else!", "siege_won_seneschal_list_options_3",[]],
  [anyone,"siege_won_seneschal_list_options_3", [], "Of course you don't, my {lord/lady}.\
 However, no lord in the land will recognize your claim to the castle unless it is verified by royal decree.\
 They would call {s1} an outlaw stronghold and take it from you at the earliest opportunity.\
 Surely not even you could stand against a whole army.", "siege_won_seneschal_list_options_4",[]],
  [anyone|plyr,"siege_won_seneschal_list_options_4", [], "Hmm. I'll give it some thought.", "siege_won_seneschal_6",[]],
  [anyone,"siege_won_seneschal_6", [], "I am very pleased to hear it, my {lord/lady}.\
 I am only trying to serve you to the best of my ability. Now,\
 if at any time you find you have further need of me,\
 I will be in the great hall arranging a smooth handover of the castle to your forces.\
 ", "close_window",[]],
]
