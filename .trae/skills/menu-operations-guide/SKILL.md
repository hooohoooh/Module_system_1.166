---
name: "menu-operations-guide"
description: "Warband 模块菜单（game_menus）拆分架构下的操作规范与陷阱提醒。当用户要新增/删除/重排菜单、修改 module_game_menus.py 或其子文件、或遇到菜单跳转错乱（如点报告变新档）时使用。"
---

# 菜单操作规范（Gekokujo - Ishin no Arashi / Module_system_1.166）

module_game_menus.py 已按功能拆分（门面聚合 + 12 个功能子文件），菜单顺序是引擎硬约束。任何菜单改动必须遵循以下规则，否则会导致跳转错乱、菜单缺失或编译失败。

## 1. 核心硬约束

- **引擎固定索引访问菜单**：世界地图 HUD"报告"按钮固定跳转 idx4（= menu_reports）。菜单重排会让 idx4 变成其他菜单（如 start_game_1 → 点报告变成创建新游戏）。
- **菜单总数结构**：293 项主列表（不含 freelancer）+ modmerger 编译时追加 freelancer 8 项 = 301 项，与拆前一致。

## 2. 聚合机制（module_game_menus.py 门面文件）

```python
_MENU_BUCKETS  # 12 个功能子文件的菜单列表
_MENU_INDEX    # id → 菜单 映射（重复 id 会 raise ValueError）
_MENU_ORDER    # 293 项主列表的 id，按拆前原始顺序
game_menus = [_MENU_INDEX[_menu_id] for _menu_id in _MENU_ORDER]
```

- **严禁把 freelancer 的 8 个菜单放进 _MENU_ORDER**：它们由 modmerger 在编译时 extend 追加到尾部，放入会导致重复追加 → 309 项、ID 全部错位。
- 文件末尾的 modmerger 块保持拆前原样（`try` + `var_set` + 显式 `modmerge(var_set)` 调用），不要改成"仅 import"——顶层只 import 不调用会 IndentationError。

## 3. 新增菜单（两步，缺一不可）

1. 在功能子文件（`module_game_menus_<feature>.py`）**末尾追加**菜单元组，不重排已有条目；id 建议带 `<feature>_` 前缀防撞名。
2. 在 `_MENU_ORDER` 中把新 id **插入到按拆前顺序应出现的位置**，并加桶注释（如 `# <- camp_cheat`）。

后果：漏掉第 2 步 → 新菜单不出现在编译产物；插入位置错误 → 该位置之后所有菜单索引 +1，固定索引访问错乱。

## 4. 删除 / 重命名

- 删除：子文件删条目 + `_MENU_ORDER` 删对应 id。漏删 `_MENU_ORDER` 中的 id 会编译报 KeyError（fail-fast，是好事）。
- 重命名 id：两处（子文件条目 + `_MENU_ORDER`）同步改。

## 5. 编译验证流程

1. 把 `module_info.py` 的 `export_dir` 临时指向 `Module_system_1.166/_build_test/`（游戏运行锁定根目录 txt 时也必须这样做）。
2. 用 python27 按 `build_module.bat` 顺序跑全部 29 个 process（`C:\Program Files (x86)\python27\python.exe`，读库受限需禁用沙箱）。
3. 比对 `_build_test/menus.txt` 与 `_prebuild/menus.txt` 的菜单名序列：301 项一致、idx4=reports 即通过。
4. 恢复 `export_dir` 原值。
5. **部署由用户手动执行**：把 `_build_test` 的 `*.txt` 复制到模块根目录（工具进程沙箱白名单不含根目录，无法代写）。注意 `game_variables.txt`、`map.txt`、`slot_names.txt`、`更新记录.txt` 是非编译文件，不要覆盖；全量覆盖时须用同一次全链编译的配套 txt（variables.txt 与 scripts/menus 等必须配套，否则变量 ID 错位）。

## 6. 已知陷阱

- 功能子文件必须自包含完整 import 头（`header_game_menus`、`module_constants` 等），否则 `assign` 等操作符 NameError。
- 中文注释：`module_game_menus.py` 聚合块内可用中文；`module_meshes.py` 等无编码声明头的主文件，注释只能用 ASCII 英文，中文字符会 SyntaxError。
- 多人并行：各 feature 子文件独立追加不冲突；冲突只集中在 `_MENU_ORDER`（纯 id 拼接，易手工合并）。
- 新增菜单后建议跑一次菜单名集合/数量校验（同 dialogs 的做法），确认与预期一致。
