from locallang import LangInit


localisation = LangInit()

local = localisation.get_localisation("en_us")

print(local.hello)

local = localisation.get_localisation("fr_be")

print(local.hello)
