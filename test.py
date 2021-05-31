#!/usr/bin/env python3
# -*- coding:utf-8 -*-

#############################################
# @ Author: Chen Jun
# @ Author Email: 1170101471@qq.com
# @ Created Date: 2021-04-25, 01:44:13
# @ Modified By: Chen Jun
# @ Last Modified: 2021-04-25, 23:02:31
#############################################

# %%
from importlib import reload
from matplotlib import pyplot as plt
from venn import _venn as venn
# help(venn)
reload(venn)
# plt.title("test_demo")
# plt.text(0, -0.1, "test2_demo", ha='center', ma='left',
#          url="https://www.baidu.com/s?ie=UTF-8&wd=test",
#          bbox=dict(url="https://www.baidu.com/s?ie=UTF-8&wd=test", alpha=0.001,)
#          )
venn.venn({"A": {1, 2, 3}, "B": {1, 2, 3, 4}, "C": {1, 2, 3, 4, 5}},
     fmt="{percentage:.1f}%\n({size})",
     figsize=(9, 9),
     #   alpha=.5,
     #  cmap=["r", "g", "b"]
     #  cmap="Accent"
     #  cmap="Set2"  # 蓝 绿 紫
     #  cmap="Set3"  # 蓝 绿 黄
     #  cmap=list("rgy")  # 红 绿 黄
     cmap=list("rgb")  # 红 绿 黄
     )
plt.savefig('test__venn.pdf', dpi=200, bbox_inches='tight')
plt.savefig('test__venn.png', dpi=200, bbox_inches='tight')
plt.savefig('test__venn.svg', dpi=200, bbox_inches='tight')
#%%