# -*- coding:utf-8 -*-
"""
Desc: This is Code Desc
"""
import pickle

# with open("data/home_pages.pkl", "rb") as file:
#     data = pickle.load(file)
#
#     print(data)


str1 = "hello world"
print(str1.endswith("d"))
print(str1.endswith("ld"))
print(str1.endswith("lo"))
print(str1.endswith("lo", 1, 5))
print(str1.endswith(("d", "lo")))

