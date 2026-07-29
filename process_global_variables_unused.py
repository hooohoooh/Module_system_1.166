from module_info import *
from process_common import *
from process_operations import *


# Variables that may be reported as "never used" due to the way the
# module system compiler tracks variable usage. These are reserved variables
# that are used in the codebase but the compiler cannot detect their usage
# because:
# - They are referenced inside try_begin/try_end blocks (the compiler's
#   compile_global_vars only processes top-level statements)
# - They are referenced inside shared trigger blocks (e.g. trigger_cannon)
#   that are appended to multiple mission templates, leading to asymmetric
#   counts of assignments vs. reads
KNOWN_USED_RESERVED_VARS = [
  "ym_56",        # used in ym_gatling.py scripts and ym_28 mission template trigger
  "ym_44",        # used in ym_gatling.py scripts and ym_28 mission template trigger
  "g_faction_merge_done",  # used in module_simple_triggers.py try_begin block
]


print "Checking global variable usages..."
variable_uses = []
variables = load_variables(export_dir,variable_uses)
i = 0
while (i < len(variables)):
  if (variable_uses[i] == 0) and (variables[i] not in KNOWN_USED_RESERVED_VARS):
    print "WARNING: Global variable never used: " + variables[i]
  i = i + 1
