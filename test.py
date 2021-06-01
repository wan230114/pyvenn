#!/usr/bin/env python3
# -*- coding:utf-8 -*-

#############################################
# @ Author: Chen Jun
# @ Author Email: 1170101471@qq.com
# @ Created Date: 2021-04-25, 01:44:13
# @ Modified By: Chen Jun
# @ Last Modified: 2021-06-01, 23:51:03
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
ax, outname = venn.venn({"A-set": {1, 2, 3},
           "B-set": {1, 2, 3, 4},
           "C-set-demo": {1, 2, 3, 4, 5, 6, 7, 8, 9, 0},
          #  "D":{99, 100},
          #  "E":{99, 100},
           },
     fmt="{percentage:.1f}%\n({size})",
     figsize=(9, 9),
     fontsize=12,
     outdir="out-test",
     #   alpha=.5,
     #  cmap=["r", "g", "b"]
     #  cmap="Accent"
     #  cmap="Set2"  # 蓝 绿 紫
     #  cmap="Set3"  # 蓝 绿 黄
     #  cmap=list("rgy")  # 红 绿 黄
     cmap=list("rgby")  # 红 绿 黄
     )

#%%

ax, outname = venn.venn({"A-set": {1, 2, 3},
           "B-set": {1, 2, 3, 4},
           "C-set-demo": {1, 2, 3, 4, 5, 6, 7, 8, 9, 0},
           "D":{99, 100},
          #  "E":{99, 100},
           },
     fmt="{percentage:.1f}%\n({size})",
     figsize=(9, 9),
     fontsize=12,
     outdir="out-test",
     #   alpha=.5,
     #  cmap=["r", "g", "b"]
     #  cmap="Accent"
     #  cmap="Set2"  # 蓝 绿 紫
     #  cmap="Set3"  # 蓝 绿 黄
     #  cmap=list("rgy")  # 红 绿 黄
     # cmap=list("rgby")  # 红 绿 黄
     )
# plt.savefig(f'{outname}venn.pdf', dpi=200, bbox_inches='tight')
# plt.savefig(f'{outname}venn.png', dpi=200, bbox_inches='tight')
# plt.savefig(f'{outname}venn.svg', dpi=200, bbox_inches='tight')