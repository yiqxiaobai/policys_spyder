# -*- coding:utf-8 -*-
"""
Desc: This is Code Desc
"""
import pickle

with open("data/home_pages.pkl", "rb") as file:
    data = pickle.load(file)

    print(data)

