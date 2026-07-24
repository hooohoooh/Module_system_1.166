# -*- coding: UTF-8 -*-
from header_common import *
from header_operations import *
from module_constants import *

# 购买加特林的脚本
gatling_shop_scripts = [
    ("try_buy_gatling",
     [
       (assign, ":can_buy", 0),
       (assign, ":reason", 0),
       
       (try_begin),
         # 检查玩家金钱
         (store_troop_gold, ":gold", "trp_player"),
         (lt, ":gold", 50000),
         (assign, ":reason", 1),  # 金钱不足
       (else_try),
         # 检查已购买的加特林数量
         (ge, "$ym_gatling_purchased", 1),
         (assign, ":reason", 2),  # 已达上限
       (else_try),
         (assign, ":can_buy", 1),  # 可以购买
       (try_end),
       
       (try_begin),
        (eq, ":can_buy", 1),
        # 扣除金钱
        (troop_remove_gold, "trp_player", 50000),
        # 增加已购买计数
        (val_add, "$ym_gatling_purchased", 1),
        # 显示购买成功消息
        (display_message, "@成功购买加特林炮台！花费 50000 金币。战场自动生成。"),
      (else_try),
         (eq, ":reason", 1),
         (display_message, "@金钱不足！需要 50000 金币"),
       (else_try),
         (eq, ":reason", 2),
         (display_message, "@加特林数量已达上限（1 台）"),
       (try_end),
     ]),
]
