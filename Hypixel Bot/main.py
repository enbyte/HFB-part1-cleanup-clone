# IMPORTS

import requests, time, ast, discord, math, threading, nbt, io, base64

from queue import Queue
from threading import Thread

import locals
from locals import *

import utils



def main():

    print("Starting Profit Calculator (debug mode = " + str(debug_mode) + ")")

    global items_with_count, avg_lbin, collection_data, blacklist, whitelist, recipe_items, volume_data, image_url_dict, webhook_dict, debug_webhook_dict, message_ids


    items_with_count = utils.open_safe_ast(locals.paths.items_with_count)
    avg_lbin = utils.open_safe_ast(locals.paths.avg_lbin)
    collection_data = utils.open_safe_ast(locals.paths.collection_data_webhook)
    blacklist = utils.open_safe_ast(locals.paths.blacklist)
    whitelist = utils.open_safe_ast(locals.paths.whitelist)
    recipe_items = utils.open_safe_ast(locals.paths.recipe_list)
    volume_data = utils.open_safe_ast(locals.paths.volume)
    image_url_dict = utils.open_safe_ast(locals.paths.image_url)
    webhook_dict = utils.open_safe_ast(locals.paths.discord_webhook)
    debug_webhook_dict = utils.open_safe_ast(locals.paths.debug_discord_webhook)
    message_ids = utils.open_safe_ast(locals.paths.message_ids)

    global BZdata, AH_data, Itemsdata
    BZdata, AH_data, Itemsdata = utils.blocking_query_apis(['https://api.hypixel.net/skyblock/bazaar', 'https://api.hypixel.net/skyblock/auctions', 'https://api.hypixel.net/resources/skyblock/items'])

    if debug_mode == True:
        message_ids = message_ids["Debug"]
    else:
        message_ids = message_ids["Normal"]
    
    BasicTopProfitMessageID = message_ids.get("Basic_Top_Profits")
    SpecialBasicTopProfitMessageID = message_ids.get("Special_Top_Profits")
    PremiumTopProfitMessageID = message_ids.get("Premium_Top_Profits")
    PreviewPremiumTopProfitMessageID = message_ids.get("Premium_Preview")
    TopScoreMessageID = message_ids.get("Premium_Top_Score")
    TopPPHMessageID = message_ids.get("Premium_Top_PPH")

    ######################
    ######################

    # Getting Other webhook url string
    Crash_Report_discord_webhook_url = webhook_dict.get("Crash_Report_discord_webhook_url")
    Blacklist_discord_webhook_url = webhook_dict.get("Blacklist_discord_webhook_url")
    Moderation_discord_webhook_url = webhook_dict.get("Moderation_discord_webhook_url")
    # Getting Basic Plan webhook url string
    Basic_webhook_dict = webhook_dict.get("Basic")
    Basic_All_discord_webhook_url = Basic_webhook_dict.get("All_Profits_url")
    Basic_AH_discord_webhook_url = Basic_webhook_dict.get("AH_Profits_url")
    Basic_BZ_discord_webhook_url = Basic_webhook_dict.get("BZ_Profits_url")
    Basic_Forge_discord_webhook_url = Basic_webhook_dict.get("Forge_Profits_url")
    Basic_Top_Profit_discord_webhook_url = Basic_webhook_dict.get("Top_Profits_url")

    # Getting Special Plan webhook url string
    Special_webhook_dict = webhook_dict.get("Special")
    Special_All_discord_webhook_url = Special_webhook_dict.get("All_Profits_url")
    Special_AH_discord_webhook_url = Special_webhook_dict.get("AH_Profits_url")
    Special_BZ_discord_webhook_url = Special_webhook_dict.get("BZ_Profits_url")
    Special_Forge_discord_webhook_url = Special_webhook_dict.get("Forge_Profits_url")
    Special_Major_discord_webhook_url = Special_webhook_dict.get("Major_Profits_url")
    Special_Top_Profit_discord_webhook_url = Special_webhook_dict.get("Top_Profits_url")

    # Getting Premium Plan Webhook url string
    Premium_webhook_dict = webhook_dict.get("Premium")
    Premium_All_discord_webhook_url = Premium_webhook_dict.get("All_Profits_url")
    Premium_AH_discord_webhook_url = Premium_webhook_dict.get("AH_Profits_url")
    Premium_BZ_discord_webhook_url = Premium_webhook_dict.get("BZ_Profits_url")
    Premium_Forge_discord_webhook_url = Premium_webhook_dict.get("Forge_Profits_url")
    Premium_Major_discord_webhook_url = Premium_webhook_dict.get("Major_Profits_url")
    Premium_Quick_discord_webhook_url = Premium_webhook_dict.get("Quick_url")
    Premium_Listings_discord_webhook_url = Premium_webhook_dict.get("Listings_url")
    Premium_Requirements_discord_webhook_url = Premium_webhook_dict.get(
        "Requirements_url"
    )
    Premium_Top_Profits_discord_webhook_url = Premium_webhook_dict.get(
        "Top_Profits_url"
    )
    Premium_Top_Score_discord_webhook_url = Premium_webhook_dict.get("Top_Score_url")
    Premium_Top_PPH_discord_webhook_url = Premium_webhook_dict.get("Top_PPH_url")
    Premium_Preview_discord_webhook_url = Premium_webhook_dict.get("Preview_url")



    # Syncing Basic Plan webhooks
    Basic_All_discord_webhook = discord.SyncWebhook.from_url(Basic_All_discord_webhook_url)
    Basic_AH_discord_webhook = discord.SyncWebhook.from_url(Basic_AH_discord_webhook_url)
    Basic_BZ_discord_webhook = discord.SyncWebhook.from_url(Basic_BZ_discord_webhook_url)
    Basic_Forge_discord_webhook = discord.SyncWebhook.from_url(Basic_Forge_discord_webhook_url)
    Basic_Top_Profit_webhook = discord.SyncWebhook.from_url(
        Basic_Top_Profit_discord_webhook_url
    )

    # Syncing Special Plan webhooks
    Special_All_discord_webhook = discord.SyncWebhook.from_url(Special_All_discord_webhook_url)
    Special_AH_discord_webhook = discord.SyncWebhook.from_url(Special_AH_discord_webhook_url)
    Special_BZ_discord_webhook = discord.SyncWebhook.from_url(Special_BZ_discord_webhook_url)
    Special_Forge_discord_webhook = discord.SyncWebhook.from_url(
        Special_Forge_discord_webhook_url
    )
    Special_Major_discord_webhook = discord.SyncWebhook.from_url(
        Special_Major_discord_webhook_url
    )
    Special_Basic_Top_Profit_webhook = discord.SyncWebhook.from_url(
        Special_Top_Profit_discord_webhook_url
    )

    # Syncing Premium Plan Webhooks
    Premium_All_discord_webhook = discord.SyncWebhook.from_url(Premium_All_discord_webhook_url)
    Premium_AH_discord_webhook = discord.SyncWebhook.from_url(Premium_AH_discord_webhook_url)
    Premium_BZ_discord_webhook = discord.SyncWebhook.from_url(Premium_BZ_discord_webhook_url)
    Premium_Forge_discord_webhook = discord.SyncWebhook.from_url(
        Premium_Forge_discord_webhook_url
    )
    Premium_Major_discord_webhook = discord.SyncWebhook.from_url(
        Premium_Major_discord_webhook_url
    )
    Quick_discord_webhook = discord.SyncWebhook.from_url(Premium_Quick_discord_webhook_url)
    No_Listings_discord_webhook = discord.SyncWebhook.from_url(
        Premium_Listings_discord_webhook_url
    )
    No_collection_discord_webhook = discord.SyncWebhook.from_url(
        Premium_Requirements_discord_webhook_url
    )
    Premium_Top_Profit_webhook = discord.SyncWebhook.from_url(
        Premium_Top_Profits_discord_webhook_url
    )
    Top_Score_webhook = discord.SyncWebhook.from_url(Premium_Top_Score_discord_webhook_url)
    Top_PPH_webhook = discord.SyncWebhook.from_url(Premium_Top_PPH_discord_webhook_url)
    Top_Preview_webhook = discord.SyncWebhook.from_url(Premium_Preview_discord_webhook_url)

    Moderation_webhook = discord.SyncWebhook.from_url(Moderation_discord_webhook_url)

    ######################
    ######################

    # Error message if repsones failed vvv
    manadory_discord_at = "<@349574651938209793>"  # @ me if there is a crash

    # Error message if repsonses failed ^^^

    # placeholders
    global Embed_queue, No_Listings_dict, No_collection_dict, Premium_Major_dict, Special_Major_dict, Quick_dict, Premium_Forge_dict, Basic_Forge_dict, Special_Forge_dict, Premium_AH_dict, Basic_AH_dict, Special_AH_dict, Premium_BZ_dict, Basic_BZ_dict, Special_BZ_dict, Basic_All_dict, Special_All_dict, Premium_All_dict, profitable_items, embedDict

    Embed_queue = Queue(maxsize=0)

    No_Listings_dict = {}
    No_collection_dict = {}
    Premium_Major_dict = {}
    Special_Major_dict = {}
    Quick_dict = {}
    Premium_Forge_dict = {}
    Basic_Forge_dict = {}
    Special_Forge_dict = {}
    Premium_AH_dict = {}
    Basic_AH_dict = {}
    Special_AH_dict = {}
    Premium_BZ_dict = {}
    Basic_BZ_dict = {}
    Special_BZ_dict = {}
    Basic_All_dict = {}
    Special_All_dict = {}
    Premium_All_dict = {}

    profitable_items = {}  # used to store profitable items then output top items
    embedDict = {
        "I-BZ": {},
        "O-BZ": {},
        "I-BZ-MC": {},
        "O-BZ-MC": {},
        "I-AH": {},
        "O-AH": {},
        "I-AH-MC": {},
        "O-AH-MC": {},
    }  # Info for the Discord Bot

    def get_ah_dict():
        return utils.open_safe_ast(locals.paths.lowest_selling)

    AH_data_dict = get_ah_dict()

    def update_responses():
        try:
            Volume_data = utils.open_safe_ast(locals.paths.volume)
            avg_lbin = utils.open_safe_ast(locals.paths.avg_lbin)


            AH_data, BZdata, Itemsdata = utils.blocking_query_apis(['https://api.hypixel.net/skyblock/auctions', 'https://api.hypixel.net/skyblock/bazaar', 'https://api.hypixel.net/resources/skyblock/items'])
        
        except requests.exceptions.ConnectionError as e:
            print("Problem getting updated responses: ", e)
        except Exception as e:
            if debug_mode == True:
                raise
            print("Problem getting updated responses: ", e)

    def get_collection_info(id):
        info = collection_data[id]
        return info if info is not None else "None"

    def get_taxed_profit(untaxed_profit, tax_type, sell_price):
        # Taxed_profit = untaxed_profit
        tax = 0
        if tax_type == "AH":
            cost = 0.01  # %1 default
            if sell_price >= 100000000:
                # if item is created for more than $100 million creation cost is %2.5
                cost = 0.025
            elif (sell_price >= 10000000) and (sell_price < 100000000):
                # if item is created for more than $10 million but less than $100 million creation cost is %2
                cost = 0.02

            tax = ((untaxed_profit * 0.01) + 1200) + (untaxed_profit * cost)
            # Tax = ((10,000 * .01) + 1200) + (10,000 * .01)) = $1,400 (1200 for the two days -- $100 for creation cost -- $100 for general tax)
            # Add 1200 to the tax because we assume that they will put it up for two days
            # Taxed_profit = untaxed_profit - Tax
        elif tax_type == "BZ":
            tax = untaxed_profit * 0.0125
            # Taxed_profit = (
            #    untaxed_profit - Tax
            # )  # Assume player has the free Elizibeth bazaar flipper upgrade
        return tax

    def get_Item_Name(item_ID):  # Changes item id to item name (FORAGING_1_PORTAL -> Portal to Birch Park)
        realItemName = item_ID
        essence_names = {
            "ESSENCE_UNDEAD": "Undead Essence",
            "ESSENCE_WITHER": "Wither Essence",
        }

        if item_ID.startswith("ENCHANTMENT_"):
            realItemName = item_ID.replace("ENCHANTMENT_", "")
            realItemName = realItemName.replace("ULTIMATE_", "")
            realItemName = realItemName.replace("_", " ")
            realItemName = realItemName.lower()
            realItemName = realItemName.title()
            realItemName = realItemName.replace("1", "I")
            realItemName = realItemName.replace("2", "II")
            realItemName = realItemName.replace("3", "III")
            realItemName = realItemName.replace("4", "IV")
            realItemName = realItemName.replace("5", "V")
            realItemName = realItemName.replace("6", "VI")
            realItemName = realItemName.replace("7", "VII")
            realItemName = realItemName.replace("8", "VIII")
            realItemName = realItemName.replace("9", "IX")
            realItemName = realItemName.replace("10", "X")
            realItemName = realItemName.replace("11", "XI")
            realItemName = realItemName.replace("12", "XII")
        AllItems = Itemsdata["items"]
        for item in AllItems:
            if item["id"] == item_ID:
                realItemName = item["name"]
        if essence_names.get(item_ID) is not None:
            realItemName = essence_names.get(item_ID)
        return realItemName

    def get_Item_ID(itemName):
        ItemID = ""
        AllItems = Itemsdata["items"]
        for item in AllItems:
            if item["name"] == itemName:
                ItemID = item["id"]
        return ItemID

    def get_Item_Tier(itemName):
        ItemTier = "COMMON"
        AllItems = Itemsdata["items"]

        for item in AllItems:
            if itemName == "BEASTMASTER_CREST_COMMON":
                print(item)
            if str(item.get("name")) == itemName:
                ItemTier = str(item.get("tier"))
        if (ItemTier == "") or (
                ItemTier == "None"
        ):  # If an item id get passes instead of Item Name
            itemName = get_Item_Name(itemName)
            for item in AllItems:
                if str(item.get("name")) == itemName:
                    ItemTier = str(item.get("tier"))
        if ItemTier == "None":
            ItemTier = "COMMON"
        return ItemTier

    def get_bypass_price(ItemID):
        # Some items you cant buy from anywhere but are still easily obtainable... i.e. Blaze Powder can be obtained by buying Blaze rods OR Coal Blocks from Coal
        ppu = bypass_sellprice
        # if you add an item to this make sure to add it to def getBypass()
        try:
            Bypass_Unitprice = {
                "BLAZE_POWDER": (
                        0.5
                        * int(BZdata["products"]["BLAZE_ROD"]["quick_status"]["buyPrice"])
                ),
                "COAL_BLOCK": (
                        9 * int(BZdata["products"]["COAL"]["quick_status"]["buyPrice"])
                ),
                "IRON_BLOCK": (
                        9
                        * int(BZdata["products"]["IRON_INGOT"]["quick_status"]["buyPrice"])
                ),
                "GOLD_BLOCK": (
                        9
                        * int(BZdata["products"]["GOLD_INGOT"]["quick_status"]["buyPrice"])
                ),
                "GOLD_NUGGET": (
                        (1 / 9)
                        * int(BZdata["products"]["GOLD_INGOT"]["quick_status"]["buyPrice"])
                ),
                "DIAMOND_BLOCK": (
                        9 * int(BZdata["products"]["DIAMOND"]["quick_status"]["buyPrice"])
                ),
                "REDSTONE_BLOCK": (
                        9 * int(BZdata["products"]["REDSTONE"]["quick_status"]["buyPrice"])
                ),
                "EMERALD_BLOCK": (
                        9 * int(BZdata["products"]["EMERALD"]["quick_status"]["buyPrice"])
                ),
                "GLOWSTONE": (
                        4
                        * int(
                    BZdata["products"]["GLOWSTONE_DUST"]["quick_status"]["buyPrice"]
                )
                ),
                "SLIME_BLOCK": (
                        9
                        * int(BZdata["products"]["SLIME_BALL"]["quick_status"]["buyPrice"])
                ),
            }
            if ItemID in Bypass_Unitprice:
                ppu = Bypass_Unitprice.get(ItemID)
        except:
            print(f"Problem getting {ItemID} in get_bypass_price")
            pass
        return ppu

    def getBypass(material_name, _):  # Some items can be bought/crafted even if they are not on BZ. This is for that.
        # EGG - Do not add
        return material_name in [
            "WOOD_SPADE",
            "WOOD_HOE",
            "WOOD_SWORD",
            "WOOD_AXE",
            "WOOD_PICKAXE",
            "CHEST",
            "GLASS",
            "GLASS_BOTTLE",
            "BOWL",
            "MILK_BUCKET",
            "LAVA_BUCKET",
            "GOLDEN_CARROT",
            "LAVA_BUCKET",
            "WOOD",
            "SPECKLED_MELON",
            "VINE",
            "STICK",
            "INK_SACK:2",
            "INK_SACK:15",
            "FISHING_ROD",
            "BLAZE_POWDER",
            "IRON_BLOCK",
            "SLIME_BLOCK",
            "DIAMOND_BLOCK",
            "REDSTONE_BLOCK",
            "GOLD_NUGGET",
            "EMERALD_BLOCK",
            "COAL_BLOCK",
            "GLOWSTONE",
            "GOLD_BLOCK",
        ]

    def recipe_Price(_item_name, retry, retry_Number, Order_or_Instant):
        price = 0
        iteration = 0  # Which material we are computing in the materials dict
        material_list = {}
        materials = {}
        Where_To_Buy = {"AH": False, "BZ": False}
        if recipe_items.get(_item_name) is not None:
            materials = recipe_items[_item_name]  # {'HARD_STONE': 576}
            products = BZdata["products"]
            if (
                    retry == True
            ):  # search to see if double crafting will bring a profit i.e. Diamond -> Enchanted Diamond -> Enchanted Diamond Block -- starting with diamonds
                for x in range(retry_Number):
                    materials2 = {}
                    iteration2 = 0
                    for (
                            mat2
                    ) in (
                            materials
                    ):  # really stupid complex algoritm to find what is required to double craft items when items have multiple items in its recipe -- 'ULTIMATE_CARROT_CANDY': {'SUPERB_CARROT_CANDY': 8, 'ULTIMATE_CARROT_CANDY_UPGRADE': 1}
                        if recipe_items.get(
                                list(materials.keys())[iteration2]
                        ):  # if material has crafting recipe
                            material_name = list(materials.keys())[iteration2]
                            material_amount = list(materials.values())[iteration2]
                            iteration3 = 0

                            t = recipe_items.get(list(materials)[iteration2])
                            if type(t) != type(
                                    recipe_items.get("fuckall")
                            ):  # make sure t is not a NoneType
                                for mat4 in recipe_items.get(
                                        list(materials)[iteration2]
                                ):  # loop material and put it into a dict i.e (THE LAST PART) ULTIMATE_CARROT_CANDY -> SUPERB_CARROT_CANDY -> {'ENCHANTED_GOLDEN_CARROT': 24, 'GREAT_CARROT_CANDY': 1}   ----- 'ULTIMATE_CARROT_CANDY': {'SUPERB_CARROT_CANDY': 8, 'ULTIMATE_CARROT_CANDY_UPGRADE': 1} -> 'SUPERB_CARROT_CANDY': {'ENCHANTED_GOLDEN_CARROT': 24, 'GREAT_CARROT_CANDY': 1}
                                    material_amount2 = material_amount * int(
                                        list(t.values())[iteration3]
                                    )  # i.e. 160 Diamonds * 160 Enchanted Diamond = 1 Enchanted Diamond Block aka 25600 Diamonds

                                    iteration3 = iteration3 + 1

                                    if materials2.get(
                                            mat4
                                    ):  # if mat4 is already on the list just add it to the total materials
                                        materials2.update(
                                            {
                                                mat4: material_amount2
                                                      + int(materials2.get(mat4))
                                            }
                                        )  # Input new recipe to dict i.e. {'DIAMOND' : 25600}
                                    else:
                                        materials2.update(
                                            {mat4: material_amount2}
                                        )  # Input new recipe to dict i.e. {'DIAMOND' : 25600}
                        else:  # if material does not have a craft recipe
                            if materials2.get(
                                    list(materials.keys())[iteration2]
                            ):  # if material is already on the list just add it to the total materials
                                x = int(
                                    materials2.get(list(materials.keys())[iteration2])
                                ) + int(list(materials.values())[iteration2])
                                materials2.update(
                                    {list(materials.keys())[iteration2]: x}
                                )
                            else:
                                materials2.update(
                                    {
                                        list(materials.keys())[iteration2]: list(
                                            materials.values()
                                        )[iteration2]
                                    }
                                )  # since it material doesnt have a recipe for double craft just input into the dict
                        iteration2 = iteration2 + 1
                    materials = materials2  # input new matierals for double crafting i.e. ULTIMATE_CARROT_CANDY = {'ULTIMATE_CARROT_CANDY': 1, 'ENCHANTED_GOLDEN_CARROT': 192, 'GREAT_CARROT_CANDY': 8}
            for mat in materials:
                material_name = list(materials.keys())[iteration]  # ['HARD_STONE']
                material_amount = list(materials.values())[iteration]  # [576]

                material_list.update({material_name: material_amount})
                bypass = False
                if str(products.get(material_name)) == "None":
                    bypass = getBypass(
                        material_name, _item_name
                    )  # Bypass certain materials even tho you cant buy them on Bazaar. i.e. Bowl
                if (
                        (str(products.get(material_name)) != "None")
                        or (str(AH_data_dict.get(material_name)) != "None")
                        or (bypass == True)
                ):
                    buy_price = 0
                    if bypass == True:
                        # buy_price = bypass_sellprice  # average of bypass items
                        buy_price = get_bypass_price(material_name) * material_amount

                    elif str(products.get(material_name)) != "None":
                        Where_To_Buy.update({"BZ": True})
                        if Order_or_Instant == "Instant":
                            buy_price = (
                                    products[material_name]["quick_status"]["buyPrice"]
                                    * material_amount
                            )  # Get the instant buy price per unit of material
                        elif (
                                Order_or_Instant == "Order"
                        ):  # If you wanna create a buy order.
                            list_length = len(products[material_name]["sell_summary"])
                            if (
                                    list_length > 0
                            ):  # If there are no orders -------------------------------- Todo: Output this?
                                product_dict = products[material_name]["sell_summary"][
                                    0
                                ]
                                price_per_unit = product_dict.get("pricePerUnit")
                                buy_price = (
                                                price_per_unit  # Get the buy price per unit of material
                                            ) * material_amount
                            else:
                                buy_price = (
                                        products[material_name]["quick_status"]["buyPrice"]
                                        * material_amount
                                )  # Get the instant buy price per unit of material
                        else:  # else just do instant
                            buy_price = (
                                    products[material_name]["quick_status"]["buyPrice"]
                                    * material_amount
                            )  # Get the instant buy price per unit of material
                    elif str(AH_data_dict.get(material_name)) != "None":
                        # print(f"{material_amount}x {material_name} = {_item_name}")
                        try:
                            # This is to account for materials accross multiple AH's
                            # i.e Master Skull Tier 2 requires 4 Master Skull Tier 1's meaning we need to get the top 4 auctions since Master Skull's dont stack
                            materials_left = material_amount
                            buy_price = 0
                            for i in range(material_amount):
                                if materials_left > 0:
                                    try:
                                        temp_buy_price = int(
                                            AH_data_dict.get(material_name)["Bids"][i]
                                        )
                                        temp_count = int(
                                            AH_data_dict.get(material_name)["Count"][i]
                                        )
                                        buy_price = buy_price + temp_buy_price
                                        materials_left = materials_left - temp_count
                                    except IndexError:
                                        # Return -1 to indicate that there are not eough materials on AH to create said item
                                        return [
                                            -1,
                                            {},
                                            Where_To_Buy,
                                        ]
                                    except:
                                        print("Issue in AH recipes #1")
                                        if debug_mode == True:
                                            raise
                                else:
                                    break
                            Where_To_Buy.update({"AH": True})
                        except:
                            print("Issue in AH recipes #2")
                            if debug_mode == True:
                                raise

                    true_price = buy_price

                    # print(
                    #    f"Trying to make {_item_name}. True price for {material_name}: ${true_price} - {material_amount} * {buy_price}"
                    # )
                    # prices:
                    if true_price > 0:
                        price = price + true_price  # return price for all materials
                    elif (
                            true_price == 0
                    ):  # if true price comes out to 0 it means that the item cannot be bought on bazaar because no one is selling it
                        # print(f"{material_name} does not have any buy offers on Bazaar!")
                        return [-1, {}, Where_To_Buy]
                elif material_name == "COINS":
                    # print(f"Found coins for {_item_name}. {material_amount} coins")
                    true_price = true_price + material_amount
                else:
                    # print(f"{material_name} cannot be bought")
                    return [
                        -1,
                        {},
                        Where_To_Buy,
                    ]  # return -1 to signal that item has materials that cannot be bought in bazaar
                iteration = (
                        iteration + 1
                )  # Which material we are computing in the materials dict
        elif str(recipe_items.get(_item_name)) == "None":
            if retry == False:
                return [-2, {}, Where_To_Buy]  # if item has no crafting recipe
        return [price, material_list, Where_To_Buy]

    def topProfitOutput():
        # -------------------------------------------
        # --------------For Top Profits--------------
        _profitable_items = profitable_items
        profitable_items_values = []
        typeOfProfits = {
            "I-BZ": {"Coin": [], "Score": [], "PPH": []},
            "O-BZ": {"Coin": [], "Score": [], "PPH": []},
            "I-BZ-MC": {"Coin": [], "Score": [], "PPH": []},
            "O-BZ-MC": {"Coin": [], "Score": [], "PPH": []},
            "I-AH": {"Coin": [], "Score": [], "PPH": []},
            "O-AH": {"Coin": [], "Score": [], "PPH": []},
            "I-AH-MC": {"Coin": [], "Score": [], "PPH": []},
            "O-AH-MC": {"Coin": [], "Score": [], "PPH": []},
        }
        for item in _profitable_items:  # For loop profitable items
            item_data = _profitable_items.get(item)
            for itt in range(len(list(item_data.get("signifier")))):
                sig = list(item_data.get("signifier"))[itt]
                d = typeOfProfits.get(sig)
                profit = list(item_data.get("profit"))[itt]
                MCT = list(item_data.get("MultiCraftTimes"))[itt]
                Score = list(item_data.get("Score"))[itt]
                PPH = list(item_data.get("PPH"))[itt]
                d["Coin"].append(profit)
                d["Score"].append(Score)
                d["PPH"].append(PPH)
        for Type in typeOfProfits:
            typeOfProfits[Type]["Coin"].sort(reverse=True)
            typeOfProfits[Type]["Score"].sort(reverse=True)
            typeOfProfits[Type]["PPH"].sort(reverse=True)
        resorted_profitable_coin = []
        resorted_profitable_score = []
        resorted_profitable_pph = []
        for Type in typeOfProfits:  # For loop list of coin numbers
            for cashnum in typeOfProfits[Type]["Coin"]:
                for item2 in _profitable_items:  # for loop of profitiable items
                    item_data = _profitable_items.get(item2)
                    sig_data = item_data.get("signifier")
                    profit_data = item_data.get("profit")
                    MCT_data = item_data.get("MultiCraftTimes")
                    Score_Data = item_data.get("Score")
                    PPH_Data = item_data.get("PPH")
                    if Type in sig_data:
                        DataNum = sig_data.index(Type)
                        if (
                                cashnum in profit_data
                        ):  # find the coin that matches the item
                            if sig_data.index(Type) == profit_data.index(
                                    cashnum
                            ):  # Double check
                                if (
                                        len(resorted_profitable_coin) > 0
                                ):  # If items are already in list append it - else create the list
                                    for position in range(
                                            len(resorted_profitable_coin)
                                    ):
                                        if (
                                                resorted_profitable_coin[position][1]
                                                < profit_data[DataNum]
                                        ):
                                            if (
                                                    [
                                                        item2,
                                                        profit_data[DataNum],
                                                        Type,
                                                        MCT_data[DataNum],
                                                        Score_Data[DataNum],
                                                        PPH_Data[DataNum],
                                                    ]
                                                    in resorted_profitable_coin
                                            ) == False:
                                                resorted_profitable_coin.insert(
                                                    position,
                                                    [
                                                        item2,
                                                        profit_data[DataNum],
                                                        Type,
                                                        MCT_data[DataNum],
                                                        Score_Data[DataNum],
                                                        PPH_Data[DataNum],
                                                    ],
                                                )  # readd it to a new dict
                                    if (
                                            [
                                                item2,
                                                profit_data[DataNum],
                                                Type,
                                                MCT_data[DataNum],
                                                Score_Data[DataNum],
                                                PPH_Data[DataNum],
                                            ]
                                            in resorted_profitable_coin
                                    ) == False:  # If after the for loop the data was still not put in add it to the end
                                        resorted_profitable_coin.append(
                                            [
                                                item2,
                                                profit_data[DataNum],
                                                Type,
                                                MCT_data[DataNum],
                                                Score_Data[DataNum],
                                                PPH_Data[DataNum],
                                            ]
                                        )

                                else:
                                    resorted_profitable_coin.append(
                                        [
                                            item2,
                                            profit_data[DataNum],
                                            Type,
                                            MCT_data[DataNum],
                                            Score_Data[DataNum],
                                            PPH_Data[DataNum],
                                        ]
                                    )  # readd it to a new dict
            # ------------------------------------------------------------------------------------#
            for scorenum in typeOfProfits[Type]["Score"]:
                for item2 in _profitable_items:  # for loop of profitiable items
                    item_data = _profitable_items.get(item2)
                    sig_data = item_data.get("signifier")
                    profit_data = item_data.get("profit")
                    MCT_data = item_data.get("MultiCraftTimes")
                    Score_Data = item_data.get("Score")
                    PPH_Data = item_data.get("PPH")
                    if Type in sig_data:
                        DataNum = sig_data.index(Type)
                        if (
                                scorenum in Score_Data
                        ):  # find the coin that matches the item
                            if sig_data.index(Type) == Score_Data.index(
                                    scorenum
                            ):  # Double check
                                if (
                                        len(resorted_profitable_score) > 0
                                ):  # If items are already in list append it - else create the list
                                    for position in range(
                                            len(resorted_profitable_score)
                                    ):
                                        if (
                                                resorted_profitable_score[position][4]
                                                < Score_Data[DataNum]
                                        ):
                                            if (
                                                    [
                                                        item2,
                                                        profit_data[DataNum],
                                                        Type,
                                                        MCT_data[DataNum],
                                                        Score_Data[DataNum],
                                                        PPH_Data[DataNum],
                                                    ]
                                                    in resorted_profitable_score
                                            ) == False:
                                                resorted_profitable_score.insert(
                                                    position,
                                                    [
                                                        item2,
                                                        profit_data[DataNum],
                                                        Type,
                                                        MCT_data[DataNum],
                                                        Score_Data[DataNum],
                                                        PPH_Data[DataNum],
                                                    ],
                                                )  # readd it to a new dict
                                    if (
                                            [
                                                item2,
                                                profit_data[DataNum],
                                                Type,
                                                MCT_data[DataNum],
                                                Score_Data[DataNum],
                                                PPH_Data[DataNum],
                                            ]
                                            in resorted_profitable_score
                                    ) == False:  # If after the for loop the data was still not put in add it to the end
                                        resorted_profitable_score.append(
                                            [
                                                item2,
                                                profit_data[DataNum],
                                                Type,
                                                MCT_data[DataNum],
                                                Score_Data[DataNum],
                                                PPH_Data[DataNum],
                                            ]
                                        )

                                else:
                                    resorted_profitable_score.append(
                                        [
                                            item2,
                                            profit_data[DataNum],
                                            Type,
                                            MCT_data[DataNum],
                                            Score_Data[DataNum],
                                            PPH_Data[DataNum],
                                        ]
                                    )  # readd it to a new dict
            for pphnum in typeOfProfits[Type]["PPH"]:
                for item2 in _profitable_items:  # for loop of profitiable items
                    item_data = _profitable_items.get(item2)
                    sig_data = item_data.get("signifier")
                    profit_data = item_data.get("profit")
                    MCT_data = item_data.get("MultiCraftTimes")
                    Score_Data = item_data.get("Score")
                    PPH_Data = item_data.get("PPH")
                    if Type in sig_data:
                        DataNum = sig_data.index(Type)
                        if pphnum in PPH_Data:  # find the coin that matches the item
                            if sig_data.index(Type) == PPH_Data.index(
                                    pphnum
                            ):  # Double check
                                if (
                                        len(resorted_profitable_pph) > 0
                                ):  # If items are already in list append it - else create the list
                                    for position in range(len(resorted_profitable_pph)):
                                        if (
                                                resorted_profitable_pph[position][5]
                                                < PPH_Data[DataNum]
                                        ):
                                            if (
                                                    [
                                                        item2,
                                                        profit_data[DataNum],
                                                        Type,
                                                        MCT_data[DataNum],
                                                        Score_Data[DataNum],
                                                        PPH_Data[DataNum],
                                                    ]
                                                    in resorted_profitable_pph
                                            ) == False:
                                                resorted_profitable_pph.insert(
                                                    position,
                                                    [
                                                        item2,
                                                        profit_data[DataNum],
                                                        Type,
                                                        MCT_data[DataNum],
                                                        Score_Data[DataNum],
                                                        PPH_Data[DataNum],
                                                    ],
                                                )  # readd it to a new dict
                                    if (
                                            [
                                                item2,
                                                profit_data[DataNum],
                                                Type,
                                                MCT_data[DataNum],
                                                Score_Data[DataNum],
                                                PPH_Data[DataNum],
                                            ]
                                            in resorted_profitable_pph
                                    ) == False:  # If after the for loop the data was still not put in add it to the end
                                        resorted_profitable_pph.append(
                                            [
                                                item2,
                                                profit_data[DataNum],
                                                Type,
                                                MCT_data[DataNum],
                                                Score_Data[DataNum],
                                                PPH_Data[DataNum],
                                            ]
                                        )

                                else:
                                    resorted_profitable_pph.append(
                                        [
                                            item2,
                                            profit_data[DataNum],
                                            Type,
                                            MCT_data[DataNum],
                                            Score_Data[DataNum],
                                            PPH_Data[DataNum],
                                        ]
                                    )  # readd it to a new dict
        Non_Premium_Counter = 0
        Premium_Counter = 0
        Special_Counter = 0
        coin_Premium_resorted_message = []
        coin_Non_Premium_resorted_message = []
        coin_Preview_resorted_message = []
        Special_coin_Non_Premium_resorted_message = []
        for Counter in range(10000):
            if Counter < len(resorted_profitable_coin):
                IsPremiumFeature = False
                SpecialAccess = False
                itemInfo = resorted_profitable_coin[Counter]
                itemName = itemInfo[0]
                itemProfit = itemInfo[1]
                itemSig = itemInfo[2]
                itemMCT = itemInfo[3]
                itemScore = itemInfo[4]
                if itemProfit >= Basic_Plan_Max:
                    SpecialAccess = True
                res = "{:,}".format(round(itemProfit, 2))
                if itemSig.find("-") != -1:
                    itemSig = itemSig.replace("-", "/")
                if itemSig.find("I") != -1:
                    itemSig = itemSig.replace("I", "Instant")
                if itemSig.find("O") != -1:
                    IsPremiumFeature = True
                    itemSig = itemSig.replace("O", "Order")
                if itemSig.find("MC") != -1:
                    retrys = ""
                    if itemMCT >= 2:
                        IsPremiumFeature = True
                    elif itemMCT == 1:
                        SpecialAccess = True

                    if itemMCT == 1:
                        retrys = "Double"
                    elif itemMCT == 2:
                        retrys = "Triple"
                    elif itemMCT == 3:
                        retrys = "Quadruple"
                    elif itemMCT == 4:
                        retrys = "Quintuple"
                    elif itemMCT > 4:
                        retrys = f"{itemMCT}x"
                    itemSig = itemSig.replace("MC", f"{retrys} MultiCraft")
                if itemMCT > 1:  # If item is triple craft or beyond
                    IsPremiumFeature = True
                Premium_Counter = Premium_Counter + 1
                coin_Premium_resorted_message.append(
                    f"#{Premium_Counter}: __**{itemName}**__ with a __**${res}**__ profit! {itemSig}\n"
                )
                coin_Preview_resorted_message.append(
                    f"#{Premium_Counter}: __**???**__ with a __**${res}**__ profit!\n"
                )
                if IsPremiumFeature == False:
                    if SpecialAccess == True:
                        Special_Counter = Special_Counter + 1
                        Special_coin_Non_Premium_resorted_message.append(
                            f"#{Special_Counter}: __**{itemName}**__ with a __**${res}**__ profit! {itemSig}\n"
                            # Score: __**{itemScore}**__!
                        )
                    else:
                        Non_Premium_Counter = Non_Premium_Counter + 1
                        coin_Non_Premium_resorted_message.append(
                            f"#{Non_Premium_Counter}: __**{itemName}**__ with a __**${res}**__ profit! {itemSig}\n"
                            # Score: __**{itemScore}**__!
                        )
                        Special_Counter = Special_Counter + 1
                        Special_coin_Non_Premium_resorted_message.append(
                            f"#{Special_Counter}: __**{itemName}**__ with a __**${res}**__ profit! {itemSig}\n"
                            # Score: __**{itemScore}**__!
                        )
            else:
                Premium_Counter = Premium_Counter + 1
                Non_Premium_Counter = Non_Premium_Counter + 1
                Special_Counter = Special_Counter + 1
                coin_Non_Premium_resorted_message.append(
                    f"#{Non_Premium_Counter}: **None**\n"
                )
                Special_coin_Non_Premium_resorted_message.append(
                    f"#{Non_Premium_Counter}: **None**\n"
                )
                coin_Premium_resorted_message.append(f"#{Premium_Counter}: **None**\n")
                coin_Preview_resorted_message.append(f"#{Premium_Counter}: **None**\n")

        # ---------------------------------------------------------------#
        score_resorted_message = []
        for Counter in range(len(TopScoreMessageID) * 50):
            if Counter < len(resorted_profitable_score):
                itemInfo = resorted_profitable_score[Counter]
                itemName = itemInfo[0]
                itemProfit = itemInfo[1]
                itemSig = itemInfo[2]
                itemMCT = itemInfo[3]
                itemScore = itemInfo[4]
                res = "{:,}".format(round(itemScore, 2))
                if itemSig.find("-") != -1:
                    itemSig = itemSig.replace("-", "/")
                if itemSig.find("I") != -1:
                    itemSig = itemSig.replace("I", "Instant")
                if itemSig.find("O") != -1:
                    itemSig = itemSig.replace("O", "Order")
                if itemSig.find("MC") != -1:
                    retrys = ""
                    if itemMCT == 1:
                        retrys = "Double"
                    elif itemMCT == 2:
                        retrys = "Triple"
                    elif itemMCT == 3:
                        retrys = "Quadruple"
                    elif itemMCT == 4:
                        retrys = "Quintuple"
                    elif itemMCT > 4:
                        retrys = f"{itemMCT}x"
                    itemSig = itemSig.replace("MC", f"{retrys} MultiCraft")
                score_resorted_message.append(
                    f"#{Counter + 1}: __**{itemName}**__ with a __**{res}**__ score! {itemSig}\n"
                )
            else:  # If outside of resorted_profitable_score len
                score_resorted_message.append(f"#{Counter + 1}: **None**\n")

        pph_resorted_message = []
        pph_Preview_resorted_message = []
        for Counter in range(len(TopPPHMessageID) * 50):
            if Counter < len(resorted_profitable_pph):
                itemInfo = resorted_profitable_pph[Counter]
                itemName = itemInfo[0]
                itemProfit = itemInfo[1]
                itemSig = itemInfo[2]
                itemMCT = itemInfo[3]
                itemScore = itemInfo[4]
                itemPPH = itemInfo[5]
                res = "{:,}".format(round(itemPPH, 2))
                if itemSig.find("-") != -1:
                    itemSig = itemSig.replace("-", "/")
                if itemSig.find("I") != -1:
                    itemSig = itemSig.replace("I", "Instant")
                if itemSig.find("O") != -1:
                    itemSig = itemSig.replace("O", "Order")
                if itemSig.find("MC") != -1:
                    retrys = ""
                    if itemMCT == 1:
                        retrys = "Double"
                    elif itemMCT == 2:
                        retrys = "Triple"
                    elif itemMCT == 3:
                        retrys = "Quadruple"
                    elif itemMCT == 4:
                        retrys = "Quintuple"
                    elif itemMCT > 4:
                        retrys = f"{itemMCT}x"
                    itemSig = itemSig.replace("MC", f"{retrys} MultiCraft")

                pph_resorted_message.append(
                    f"#{Counter + 1}: __**{itemName}**__ with a __**{res}**__ Profit Per Hour! {itemSig}\n"
                )
                pph_Preview_resorted_message.append(
                    f"#{Counter + 1}: __**???**__ with a __**${res}**__ Profit Per Hour!\n"
                )
            else:  # If outside of resorted_profitable_score len
                pph_resorted_message.append(f"#{Counter + 1}: **None**\n")
                pph_Preview_resorted_message.append(f"#{Counter + 1}: **None**\n")

        dt = round(time.time())
        relative = f"<t:{dt}:R>"

        # ----------------------send vv----------------------------#

        str_Non_Premium_resorted_message = ""
        str_Special_Coin_resorted_message = ""
        MessageNumber = 0
        loop_number = 0
        for itteration in range(500):
            try:
                str_Non_Premium_resorted_message = (
                        str_Non_Premium_resorted_message
                        + coin_Non_Premium_resorted_message[itteration]
                )
            except IndexError as e:
                pass
            try:
                str_Special_Coin_resorted_message = (
                        str_Special_Coin_resorted_message
                        + Special_coin_Non_Premium_resorted_message[itteration]
                )
            except IndexError as e:
                pass
            loop_number = loop_number + 1
            if loop_number / 10 == round(loop_number / 10):
                # and ( MessageNumber <= (len(BasicTopProfitMessageID) - 1)):
                Non_Premium_embed = discord.Embed(
                    color=discord.Colour(0x00FF00),
                    description="",
                )
                Non_Premium_embed.add_field(
                    name=f"Top {loop_number - 9}-{loop_number} Profits",
                    value=str_Non_Premium_resorted_message,
                    inline=False,
                )
                ###
                Special_embed = discord.Embed(
                    color=discord.Colour(0x00FF00),
                    description="",
                )
                Special_embed.add_field(
                    name=f"Top {loop_number - 9}-{loop_number} Profits",
                    value=str_Special_Coin_resorted_message,
                    inline=False,
                )

                TopText = ""
                if MessageNumber == 0:
                    TopText = f"Last updated {relative}!"
                else:
                    TopText = ""
                try:
                    Basic_Top_Profit_webhook.edit_message(
                        BasicTopProfitMessageID[MessageNumber],
                        content=TopText,
                        embed=Non_Premium_embed,
                    )
                except IndexError as e:
                    pass
                except:
                    print("error at Basic top profits message")
                    if debug_mode == True:
                        raise

                try:
                    Special_Basic_Top_Profit_webhook.edit_message(
                        SpecialBasicTopProfitMessageID[MessageNumber],
                        content=TopText,
                        embed=Special_embed,
                    )
                except IndexError as e:
                    pass
                except:
                    print("error at Special Basic top profits message")
                    if debug_mode == True:
                        raise

                str_Non_Premium_resorted_message = ""
                str_Special_Coin_resorted_message = ""
                MessageNumber = MessageNumber + 1

        str_Premium_resorted_message = ""
        str_PreviewPremium_resorted_message = ""
        MessageNumber = 0
        loop_number = 0
        for itteration in range(len(coin_Premium_resorted_message)):
            try:
                str_Premium_resorted_message = (
                        str_Premium_resorted_message
                        + coin_Premium_resorted_message[itteration]
                )
            except IndexError as e:
                pass
            try:
                str_PreviewPremium_resorted_message = (
                        str_PreviewPremium_resorted_message
                        + pph_Preview_resorted_message[itteration]
                )
            except IndexError as e:
                pass
            loop_number = loop_number + 1
            if (loop_number / 10 == round(loop_number / 10)) and (
                    MessageNumber <= (len(PremiumTopProfitMessageID) - 1)
            ):
                Premium_embed = discord.Embed(
                    color=discord.Colour(0x00FF00),
                    description="",
                )
                Premium_embed.add_field(
                    name=f"Top {loop_number - 9}-{loop_number} Profits",
                    value=str_Premium_resorted_message,
                    inline=False,
                )
                TopText = ""
                if MessageNumber == 0:
                    TopText = f"Last updated {relative}!"
                try:
                    Premium_Top_Profit_webhook.edit_message(
                        PremiumTopProfitMessageID[MessageNumber],
                        content=TopText,
                        embed=Premium_embed,
                    )
                except IndexError as e:
                    pass
                except requests.exceptions.ConnectionError as e:
                    print("error at Premium top profits  message: ", e)
                except:
                    print("error at premium top profits message")
                    if debug_mode == True:
                        raise
                PreviewPremium_embed = discord.Embed(
                    color=discord.Colour(0x00FF00),
                    description="",
                )
                PreviewPremium_embed.add_field(
                    name=f"Top {loop_number - 9}-{loop_number} Premium Profits",
                    value=str_PreviewPremium_resorted_message,
                    inline=False,
                )
                TopText = ""
                if MessageNumber == 0:
                    TopText = f"Unlock the following profits with premium! - Last updated {relative}!"
                try:
                    Top_Preview_webhook.edit_message(
                        PreviewPremiumTopProfitMessageID[MessageNumber],
                        content=TopText,
                        embed=PreviewPremium_embed,
                    )
                except IndexError as e:
                    pass
                except requests.exceptions.ConnectionError as e:
                    print("error at Preview Premium top profits  message: ", e)
                except:
                    print("error at Preview Premium top profits message")
                    if debug_mode == True:
                        raise
                str_Premium_resorted_message = ""
                str_PreviewPremium_resorted_message = ""
                MessageNumber = MessageNumber + 1

        str_Score_resorted_message = ""
        MessageNumber = 0
        loop_number = 0
        for itteration in range(len(score_resorted_message)):
            str_Score_resorted_message = (
                    str_Score_resorted_message + score_resorted_message[itteration]
            )
            loop_number = loop_number + 1
            if (loop_number / 10 == round(loop_number / 10)) and (
                    MessageNumber <= (len(TopScoreMessageID) - 1)
            ):
                embed = discord.Embed(
                    color=discord.Colour(0x00FF00),
                    description="",
                )
                embed.add_field(
                    name=f"Top {loop_number - 9}-{loop_number} Profits",
                    value=str_Score_resorted_message,
                    inline=False,
                )
                TopText = ""
                if MessageNumber == 0:
                    TopText = f"Last updated {relative}!"
                try:
                    Top_Score_webhook.edit_message(
                        TopScoreMessageID[MessageNumber],
                        content=TopText,
                        embed=embed,
                    )
                except requests.exceptions.ConnectionError as e:
                    print("error at Premium top scores  message: ", e)
                except:
                    print("error at premium top scores message")
                    if debug_mode == True:
                        raise

                str_Score_resorted_message = ""
                MessageNumber = MessageNumber + 1

        str_pph_resorted_message = ""
        MessageNumber = 0
        loop_number = 0
        for itteration in range(len(pph_resorted_message)):
            str_pph_resorted_message = (
                    str_pph_resorted_message + pph_resorted_message[itteration]
            )
            loop_number = loop_number + 1
            if (loop_number / 10 == round(loop_number / 10)) and (
                    MessageNumber <= (len(TopPPHMessageID) - 1)
            ):
                embed = discord.Embed(
                    color=discord.Colour(0x00FF00),
                    description="",
                )
                embed.add_field(
                    name=f"Top {loop_number - 9}-{loop_number} Profits",
                    value=str_pph_resorted_message,
                    inline=False,
                )
                TopText = ""
                if MessageNumber == 0:
                    TopText = f"Last updated {relative}!"
                try:
                    Top_PPH_webhook.edit_message(
                        TopPPHMessageID[MessageNumber],
                        content=TopText,
                        embed=embed,
                    )
                except requests.exceptions.ConnectionError as e:
                    print("error at Premium top PPHs  message: ", e)
                except:
                    print("error at premium top PPHs message")
                    if debug_mode == True:
                        raise

                str_pph_resorted_message = ""
                MessageNumber = MessageNumber + 1
        return
        # -------------------------------------------
        # -------------------------------------------

    def get_EFT(itemID, Amount, Material_or_Item):
        productInfo = BZdata["products"].get(itemID)
        try:
            if str(productInfo) != "None":  # Bypass items return "None"
                quickStatus = productInfo.get("quick_status")
                Comp_Multiplier = 1
                if Material_or_Item == "Material":
                    if len(productInfo["sell_summary"]) > 1:
                        top_sell_summary = productInfo["sell_summary"][
                            0
                        ]  # Get top price sell order info

                        top_sell_summary_amount = top_sell_summary.get(
                            "amount"
                        )  # Get the amount of orders for the top price
                        Comp_Multiplier = (
                                                  top_sell_summary_amount + Amount
                                          ) / Amount  # Say you wanna buy 10 but there are 100 orders (100/10 = 10) meaning we want to multiply EFT by 10x because you will be in competition with those 100 orders

                        # Redo Comp Multiplier to take how often you get undercut

                        Comp_Multiplier = round(Comp_Multiplier * 0.90)  # Debuff by 10%
                        if Comp_Multiplier < 1:
                            Comp_Multiplier = 1

                    movingProduct_Week = int(quickStatus.get("sellMovingWeek"))
                    # movingProduct_Week = 604800 # 1 a second
                    movingProduct_Day = movingProduct_Week / 7
                    movingProduct_Hour = movingProduct_Day / 24
                    movingProduct_Minute = movingProduct_Hour / 60
                    movingProduct_Second = movingProduct_Minute / 60
                    """print(
                        f"MATERIAL: {MaterialAmount}x {MaterialId} will take {((Comp_Multiplier * MaterialAmount) / movingProduct_Second)} seconds to fill"
                    )"""
                    if movingProduct_Second != 0:
                        return round((Comp_Multiplier * Amount) / movingProduct_Second)
                    elif movingProduct_Minute != 0:
                        return round(
                            ((Comp_Multiplier * Amount) / movingProduct_Minute) / 60
                        )
                    elif movingProduct_Hour != 0:
                        return round(
                            ((Comp_Multiplier * Amount) / movingProduct_Hour) / 3600
                        )
                    elif movingProduct_Day != 0:
                        return round(
                            ((Comp_Multiplier * Amount) / movingProduct_Day) / 86400
                        )
                elif Material_or_Item == "Item":
                    if len(productInfo["buy_summary"]) > 1:
                        top_buy_summary = productInfo["buy_summary"][
                            0
                        ]  # Get top price sell order info
                        top_buy_summary_amount = top_buy_summary.get(
                            "amount"
                        )  # Get the amount of orders for the top price
                        Comp_Multiplier = (
                                                  top_buy_summary_amount + Amount
                                          ) / Amount  # Say you wanna buy 10 but there are 100 orders (100/10 = 10) meaning we want to multiply EFT by 10x because you will be in competition with those 100 orders

                        Comp_Multiplier = round(Comp_Multiplier * 0.75)  # Debuff by 25%
                        if Comp_Multiplier < 1:
                            Comp_Multiplier = 1

                    movingProduct_Week = int(quickStatus.get("buyMovingWeek"))
                    # movingProduct_Week = 604800 # 1 a second
                    movingProduct_Day = movingProduct_Week / 7
                    movingProduct_Hour = movingProduct_Day / 24
                    movingProduct_Minute = movingProduct_Hour / 60
                    movingProduct_Second = movingProduct_Minute / 60
                    """print(
                        f"MATERIAL: {Amount}x {itemID} will take {((Comp_Multiplier * Amount) / movingProduct_Second)} seconds to fill"
                    )"""
                    if movingProduct_Second != 0:
                        return round((Comp_Multiplier * Amount) / movingProduct_Second)
                    elif movingProduct_Minute != 0:
                        return round(
                            ((Comp_Multiplier * Amount) / movingProduct_Minute) / 60
                        )
                    elif movingProduct_Hour != 0:
                        return round(
                            ((Comp_Multiplier * Amount) / movingProduct_Hour) / 3600
                        )
                    elif movingProduct_Day != 0:
                        return round(
                            ((Comp_Multiplier * Amount) / movingProduct_Day) / 86400
                        )
            else:  # For bypass items
                return 0
        except:
            return Amount * 5  # if error guess 5 seconds per item

    def get_signifiers(
            MessageType, itemName, Order_or_Instant, isDoubleCraft, MultiCraft_Retry_Times
    ):
        # ------------ vv Sigifier Stuff vv ------------
        MultiCraftSig = ""
        signifier = ""
        Display_signifier = ""
        PremiumFeature = False
        if MultiCraft_Retry_Times == 1:
            MultiCraftSig = "DOUBLE"
        elif MultiCraft_Retry_Times == 2:
            MultiCraftSig = "TRIPLE"
        elif MultiCraft_Retry_Times == 3:
            MultiCraftSig = "QUADRUPLE"
        elif MultiCraft_Retry_Times == 4:
            MultiCraftSig = "QUINTUPLE"
        elif MultiCraft_Retry_Times > 4:
            MultiCraftSig = f"{MultiCraft_Retry_Times}x"
        if MultiCraft_Retry_Times >= 2:  # Triple craft and beyond is premiums
            PremiumFeature = True

        # For all output - signifies what type of profit it is

        if MessageType == 3:
            if Order_or_Instant == "Instant":
                signifier = "I-AH"
                Display_signifier = "Instant/AH"
            elif Order_or_Instant == "Order":
                signifier = "O-AH"
                Display_signifier = "Order/AH"
                PremiumFeature = True
            else:
                signifier = "AH"
                Display_signifier = "AH"
        elif MessageType == 4:
            if Order_or_Instant == "Instant":
                signifier = "I-BZ"
                Display_signifier = "Instant/BZ"
            elif Order_or_Instant == "Order":
                signifier = "O-BZ"
                Display_signifier = "Order/BZ"
                PremiumFeature = True
            else:
                signifier = "BZ"
                Display_signifier = "BZ"

        if isDoubleCraft == True:
            signifier = signifier + "-MC"
            Display_signifier = Display_signifier + "/MultiCraft"
            if MultiCraftSig == "":  # If is doulbe craft but no sig was found
                print(f"Problem finding Multcraft Sig for {itemName}!!!")
                MultiCraftSig = "Multicraft"
        return (signifier, Display_signifier, MultiCraftSig, PremiumFeature)
        # ------------ ^^ Sigifier Stuff ^^ ------------#

    def get_embed(
            MessageType,
            itemID,
            profit,
            materials,
            isDoubleCraft,
            MultiCraft_Retry_Times,
            materialPrice,
            lowestSelling,
            volume,
            avgPrice,
            Order_or_Instant,
            Where_to_buy_materials,
            taxes,
    ):  # Creating embeds
        """
        MessageType's:
        0 = New Query
        1 = No listings
        2 = Major
        3 = AH Minor
        4 = BZ Minor
        5 = Blacklisted
        6 = Forge
        """
        SpecialAccess = False
        ForgeItem = False
        # Collection requirements
        itemCollectionInfo = get_collection_info(itemID)
        str_CollectionRequirment = "None"
        display_Forge_time = ""  # displayed time it takes to forge an item
        int_Forge_time = 0  # Int time it takes to forge an item in seconds - for EFT
        CollectionMaterial = ""
        CollectionTier = ""
        if str(itemCollectionInfo) != "None":
            CollectionMaterial = itemCollectionInfo.get("Material")
            CollectionTier = itemCollectionInfo.get("Tier")
            str_CollectionRequirment = f"{CollectionMaterial} Tier {CollectionTier}"
            if str_CollectionRequirment.startswith("Forge") == True:
                ForgeItem = True
                if str(itemCollectionInfo.get("Time")) != "None":
                    display_Forge_time = itemCollectionInfo.get("Time")
                else:
                    print(f"Problem getting forge display time for: {itemID}")
                if str(itemCollectionInfo.get("Seconds")) != "None":
                    int_Forge_time = itemCollectionInfo.get("Seconds")
                    try:
                        int_Forge_time = int(int_Forge_time)
                    except:
                        print(
                            f"Problem turn int forge time into integer: {itemID} - Time: {int_Forge_time}"
                        )
                        if debug_mode == True:
                            raise
                else:
                    print(f"Problem getting forge int time for: {itemID}")

        collections = {}
        if CollectionMaterial != "":
            collections = {CollectionMaterial: CollectionTier}
        # Here
        if isDoubleCraft == True:
            int_Forge_time = 0
            for itt in range(MultiCraft_Retry_Times):
                r = recipe_Price(itemID, True, itt, Order_or_Instant)
                rec = r[1]
                for item in rec:
                    itemColl = get_collection_info(item)
                    if str(itemColl) != "None":
                        itemMat = itemColl["Material"]
                        itemTier = itemColl["Tier"]
                        if str(itemColl.get("Seconds")) != "None":
                            ForgeItem = True
                            int_Forge_time = int_Forge_time + int(
                                itemColl.get("Seconds")
                            )
                        if str(collections.get(itemMat)) == "None":
                            collections.update({itemMat: itemTier})
                        else:
                            if collections.get(itemMat) < itemTier:
                                collections.update({itemMat: itemTier})
            days = ""
            hours = ""
            minutes = ""
            seconds = ""
            temp_int_Forge_time = int_Forge_time
            if temp_int_Forge_time >= 86400:
                int_days = math.floor(temp_int_Forge_time / 86400)
                days = f"{int_days} Days "
                temp_int_Forge_time = temp_int_Forge_time - (int_days * 86400)
            if temp_int_Forge_time >= 3600:
                int_hours = math.floor(temp_int_Forge_time / 3600)
                hours = f"{int_hours} Hours "
                temp_int_Forge_time = temp_int_Forge_time - (int_hours * 3600)
            if temp_int_Forge_time >= 60:
                int_minutes = math.floor(temp_int_Forge_time / 60)
                minutes = f"{int_minutes} Minutes "
                temp_int_Forge_time = temp_int_Forge_time - (int_minutes * 60)
            if temp_int_Forge_time > 0:
                int_seconds = temp_int_Forge_time
                seconds = f"{int_seconds} Seconds"
                temp_int_Forge_time = 0
            display_Forge_time = f"{days}{hours}{minutes}{seconds}"
        if len(collections) > 1:
            str_CollectionRequirment = "\n"
            for mat in collections:
                tier = collections.get(mat)
                str_CollectionRequirment = (
                        str_CollectionRequirment + f"- {mat} Tier {tier}\n"
                )

        itemName = get_Item_Name(itemID)
        # Rounding
        avgPrice = round(avgPrice)
        profit = round(profit)
        taxes = round(taxes)
        materialPrice = round(materialPrice)
        lowestSelling = round(lowestSelling)

        # Get Tier color
        itemTier = get_Item_Tier(itemName)
        itemTierColor = discord.Color.from_rgb(255, 255, 255)
        int_color = [255, 255, 255]
        if itemTier == "COMMON":
            itemTierColor = discord.Color.from_rgb(255, 255, 255)
            int_color = [255, 255, 255]
        elif itemTier == "UNCOMMON":
            itemTierColor = discord.Color.from_rgb(0, 255, 0)
            int_color = [0, 255, 0]
        elif itemTier == "RARE":
            itemTierColor = discord.Color.from_rgb(0, 0, 255)
            int_color = [0, 0, 255]
        elif itemTier == "EPIC":
            itemTierColor = discord.Color.from_rgb(127, 0, 127)
            int_color = [127, 0, 127]
        elif itemTier == "LEGENDARY":
            itemTierColor = discord.Color.from_rgb(255, 150, 0)
            int_color = [255, 150, 0]
        elif itemTier == "MYTHIC":
            itemTierColor = discord.Color.from_rgb(255, 0, 255)
            int_color = [255, 0, 255]
        elif itemTier == "DIVINE":
            itemTierColor = discord.Color.from_rgb(0, 255, 255)
            int_color = [0, 255, 255]
        elif itemTier == "SPECIAL":
            itemTierColor = discord.Color.from_rgb(255, 100, 100)
            int_color = [255, 100, 100]
        else:
            itemTierColor = discord.Color.from_rgb(255, 255, 255)
            int_color = [255, 255, 255]

        avg_calc = avgPrice - lowestSelling
        if avgPrice == 0:
            avg_calc = 0
        """if (avg_calc < 0) and (avgPrice > 0) and (lowestSelling > 0):
            if (profit * 10) < abs(avg_calc):
                #print(f"1 - Returning {itemID}")
                return
            elif abs(avgPrice * 10) < abs(
                lowestSelling
            ):  # dont print super inflated outputs - put in no listings?
                #print(f"2 - Returning {itemID}")
                return"""

        # reformat to add commas i.e 123456 -> 123,456
        profit_res = "__**" + "{:,}".format(profit) + "**__"
        materialPrice_res = "{:,}".format(materialPrice)
        lowestSelling_res = "{:,}".format(lowestSelling)
        avg_calc_res = "{:,}".format(abs(avg_calc))
        avgPrice_res = "{:,}".format(avgPrice)
        taxes_res = "{:,}".format(taxes)
        volume_res = ""
        if volume > 0:
            volume_res = f"Volume: {volume} sales a day!\n"
        PremiumFeature = False  # Place holder
        # ------------ vv Sigifier Stuff vv ------------#
        sigs = get_signifiers(
            MessageType,
            itemName,
            Order_or_Instant,
            isDoubleCraft,
            MultiCraft_Retry_Times,
        )
        signifier = sigs[0]
        Display_signifier = "__**" + sigs[1] + "**__"
        MultiCraftSig = sigs[2]
        PremiumFeature = sigs[3]

        # ------------ ^^ Sigifier Stuff ^^ ------------#

        # Expected flip time if Order
        # EFT = Expected Flip Time - In seconds
        EFT = 0.0
        top_EFT = 0.0
        total_MaterialAmount = 0
        material_buffer = 15
        # ---------------------- vv Get EFT for materials vv ----------------------
        if Order_or_Instant == "Order":  # Get EFT for materials
            for k in range(len(list(materials.keys()))):
                lstMaterialKeys = list(materials.keys())
                MaterialId = lstMaterialKeys[k]
                MaterialAmount = materials.get(MaterialId)
                total_MaterialAmount = total_MaterialAmount + MaterialAmount
                new_EFT = get_EFT(MaterialId, MaterialAmount, "Material")
                if str(new_EFT) != "None":
                    if top_EFT < new_EFT:
                        top_EFT = new_EFT  # We only care about the longest item time to get because by the time you get that item the rest will be filled
        elif Order_or_Instant == "Instant":  # Get total materials
            for k in range(len(list(materials.keys()))):
                lstMaterialKeys = list(materials.keys())
                MaterialId = lstMaterialKeys[k]
                MaterialAmount = materials.get(MaterialId)
                total_MaterialAmount = total_MaterialAmount + MaterialAmount

        if total_MaterialAmount > 0:
            material_buffer = round(total_MaterialAmount / 160)
            if material_buffer < 15:
                # Will take alteast 15 seconds to craft
                material_buffer = 15
            elif material_buffer > 450:
                material_buffer = 450
                # Should never take moer than 7.5 minutes to craft an item even if it requires alot of materials
        EFT = top_EFT + material_buffer
        # We only care about the longest item time to get because by the time you get that item the rest will be filled

        # ---------------------- ^^ Get EFT for materials ^^ ----------------------

        # ---------------------- vv Get EFT for bazaar items vv ----------------------
        if (MessageType == 4) and (Order_or_Instant == "Order"):
            productInfo = BZdata["products"].get(itemID)
            if str(productInfo) != "None":  # Bypass items return "None"(
                MaterialAmount = 1
                new_EFT = get_EFT(itemID, MaterialAmount, "Item")
                if str(new_EFT) != "None":
                    EFT = EFT + new_EFT

        # ---------------------- ^^ Get EFT for bazaar items ^^ ----------------------

        # ---------------------- vv Get EFT for AH items vv ----------------------
        if (MessageType == 3) and (volume > 0):  # AH items
            volume_per_hour = volume / 24
            volume_per_minute = volume_per_hour / 60
            volume_per_second = volume_per_minute / 60

            EFT = EFT + (
                    1 / volume_per_second
            )  # the total seconds it'll take to sell 1. i.e (1/0.000277777778) = 3600 seconds or 1 an hour

        if Where_to_buy_materials.get("AH") == True:
            # Add EFT for every item you gotta buy off AH
            pass
        # ---------------------- ^^ Get EFT for AH items ^^ ----------------------

        # ---------------------- vv Get EFT for Forge items vv ----------------------
        if ForgeItem == True:  # -----------------------------------FORGE TIMES NEEDED
            EFT = EFT + int_Forge_time
        # ---------------------- ^^ Get EFT for Forge items ^^ ----------------------

        EFT = round(EFT, 5)
        EFT_res = ""
        if EFT >= 86400:
            days = math.floor(EFT / 86400)
            EFT_res = f"\n{days} Day(s) "
            tempEFT = EFT - (days * 86400)
            EFT_res = EFT_res + time.strftime(
                "%H Hour(s) %M Minute(s) %S Second(s)", time.gmtime(tempEFT)
            )
        elif EFT >= 3600:
            EFT_res = time.strftime(
                "%H Hour(s) %M Minute(s) %S Second(s)", time.gmtime(EFT)
            )
        elif EFT >= 60:
            EFT_res = time.strftime("%M Minute(s) %S Second(s)", time.gmtime(EFT))
        elif EFT > 0:
            EFT_res = time.strftime("%S Second(s)", time.gmtime(EFT))

        EFT_res = "\nExpected Flip Time: __**" + EFT_res + "**__!"
        if ((MessageType == 3) and (volume == 0)):
            # no point in outputting the EFT an AH item if we dont know the volume of because it'll get inflated like crazy and give a incorrect profit per hour
            EFT_res = ""
            EFT = 0

        # Expected flip time if Order ^^
        # EFT = Expected Flip Time - In seconds ^^

        # ---------------------- vv GET Profit Per Hour vv ----------------------
        str_profit_per_hour = ""
        profit_per_hour = 0.0
        if (EFT > 0):
            calc = profit / EFT
            profit_per_hour = round((calc * 3600), 2)
            profit_per_hour_res = "{:,}".format(profit_per_hour)
            str_profit_per_hour = (
                f"\nExpected Profit Per Hour: __**${profit_per_hour_res}**__"
            )

        # ---------------------- ^^ GET Profit Per Hour ^^ ----------------------

        score = round(
            (((((profit / 50) + (avg_calc / 5))) + ((-1 * EFT) * 300)) / 2500),
            2,
        )
        res_score = "__**" + "{:,}".format(score) + "**__"

        if itemID in blacklist:
            MessageType = 5

        # ---------------------- vv top stuff/avg message vv ----------------------
        avg_Message = ""
        if (
                (MessageType != 5) and (MessageType != 1) and (profit > 5000)
        ):  # if item is not blacklisted
            minium_avg_calc = (
                                  profit
                              ) * -1  # (profit / 3) * -1   # Minuim average price to be in top profits
            if (avg_calc >= minium_avg_calc) and ((volume > 0) or (MessageType == 4)):
                # Top Profit/Score Stuff
                if profitable_items.get(itemName) != profitable_items.get("fuckall"):
                    exsistingData = profitable_items.get(itemName)
                    exsistedSig = exsistingData.get("signifier")
                    exsistedProfit = exsistingData.get("profit")
                    exsistedMultiCraftTimes = exsistingData.get("MultiCraftTimes")
                    exsistedScores = exsistingData.get("Score")
                    exsistedPPH = exsistingData.get("PPH")

                    exsistedProfit.append(profit)
                    exsistedMultiCraftTimes.append(MultiCraft_Retry_Times)
                    exsistedScores.append(score)
                    exsistedSig.append(signifier)
                    exsistedPPH.append(profit_per_hour)
                elif itemName != "":
                    profitable_items.update(
                        {
                            itemName: {
                                "profit": [profit],
                                "signifier": [signifier],
                                "MultiCraftTimes": [MultiCraft_Retry_Times],
                                "Score": [score],
                                "PPH": [profit_per_hour],
                            }
                        }
                    )
        avg_Message = (
            f"Average Lowest Bin: ${avgPrice_res}\nLowest Bin: ${lowestSelling_res}\n"
        )
        if avg_calc >= 0:
            avg_Message = (
                    avg_Message
                    + f"(Average-Lowest) Price Difference: ${avg_calc_res} :white_check_mark:"
            )
        elif avg_calc < 0:
            abs(avg_calc)
            avg_Message = (
                    avg_Message + f"(Average-Lowest) Price Difference: -${avg_calc_res} :x:"
            )
        # ---------------------- ^^ top stuff/avg message ^^ ----------------------

        Where_to_buy_text = "Buy materials from: "

        if Where_to_buy_materials.get("AH") == True:
            Where_to_buy_text = Where_to_buy_text + "AH"

        if (Where_to_buy_materials.get("AH") == True) and (
                Where_to_buy_materials.get("BZ") == True
        ):
            Where_to_buy_text = Where_to_buy_text + " + "

        if Where_to_buy_materials.get("BZ") == True:
            Where_to_buy_text = Where_to_buy_text + "BZ"

        Where_to_buy_text = "__**" + Where_to_buy_text + "**__"

        dt = round(time.time())
        relative = f"<t:{dt}:R>"

        txtmessage = ""
        prem_txtmessage = ""
        if MessageType == 4:  # BZ
            if ForgeItem == True:
                prem_txtmessage = f"${profit_res} profit!\n{Display_signifier} - {relative}!\nForge time: __**{display_Forge_time}**__{EFT_res}{str_profit_per_hour}\nCost to craft: ${materialPrice_res}\nTaxes: ${taxes_res}\n{Where_to_buy_text}"
                txtmessage = f"${profit_res} profit!\n{Display_signifier} - {relative}\nForge time: __**{display_Forge_time}**__{str_profit_per_hour}\nCost to craft: ${materialPrice_res}\nTaxes: ${taxes_res}\n{Where_to_buy_text}"
            else:
                prem_txtmessage = f"${profit_res} profit!\n{Display_signifier} - {relative}!{EFT_res}{str_profit_per_hour}\nCost to craft: ${materialPrice_res}\nTaxes: ${taxes_res}\n{Where_to_buy_text}"
                txtmessage = f"${profit_res} profit!\n{Display_signifier} - {relative}\nCost to craft: ${materialPrice_res}\nTaxes: ${taxes_res}\n{Where_to_buy_text}"

        else:  # AH
            if ForgeItem == True:
                prem_txtmessage = f"${profit_res} profit!\n{Display_signifier} - {relative}!\nForge time: __**{display_Forge_time}**__{EFT_res}{str_profit_per_hour}\n{volume_res}{avg_Message}\nCost to craft: ${materialPrice_res}\nTaxes: ${taxes_res}\n{Where_to_buy_text}"
                txtmessage = f"${profit_res} profit!\n{Display_signifier} - {relative}!\nForge time: __**{display_Forge_time}**__\n{volume_res}Cost to craft: ${materialPrice_res}\nTaxes: ${taxes_res}\n{avg_Message}\n{Where_to_buy_text}"
            else:
                prem_txtmessage = f"${profit_res} profit!\n{Display_signifier} - {relative}!{EFT_res}{str_profit_per_hour}\n{volume_res}{avg_Message}\nCost to craft: ${materialPrice_res}\nTaxes: ${taxes_res}\n{Where_to_buy_text}"
                txtmessage = f"${profit_res} profit!\n{Display_signifier} - {relative}!\n{volume_res}Cost to craft: ${materialPrice_res}\nTaxes: ${taxes_res}\n{avg_Message}\nScore: {res_score}\n{Where_to_buy_text}"

        # Add embed fields
        if MessageType == 1:  # Print out to no listings
            prem_txtmessage = f"{relative}\nCost to craft: ${materialPrice_res}\nTaxes: ${taxes_res}\nAverage Sell Price: ${avg_calc_res}\nSuggested Sell Price: ${avg_calc_res}\n{volume_res}{EFT_res}"
        # ----------------------- vv Add required materials vv -----------------------
        strmaterials = ""
        for k in range(len(list(materials.keys()))):
            lstMaterialKeys = list(materials.keys())
            MaterialId = lstMaterialKeys[k]
            MaterialAmount = materials.get(MaterialId)
            MaterialName = get_Item_Name(MaterialId)
            resMaterialAmount = "{:,}".format(MaterialAmount)
            STRMaterialCollection = ""
            # Collection info for the materials - Make sure it tells requirement for double craft not the actual item. i.e. If it says 160 Enchanted diamonds it should show the requirement for Enchanted Diamond Block not Enchanted Diamonds

            # -----
            strmaterials = (
                    strmaterials
                    + f"- {resMaterialAmount} {MaterialName}(s){STRMaterialCollection}\n"
            )
        if isDoubleCraft == True:
            txtmessage = (
                    txtmessage + f"\n__WARNING {MultiCraftSig} CRAFT:__\n{strmaterials}"
            )
            prem_txtmessage = (
                    prem_txtmessage
                    + f"\n__WARNING {MultiCraftSig} CRAFT:__\n{strmaterials}"
            )
        else:
            txtmessage = txtmessage + f"\nRequired materials:\n{strmaterials}"
            prem_txtmessage = prem_txtmessage + f"\nRequired materials:\n{strmaterials}"
        # ----------------------- ^^ Add required materials ^^ -----------------------
        """
        -------------+------------------------+
        |    Field    |         Limit          |
        +-------------+------------------------+
        | title       | 256 characters         |
        | description | 4096 characters*       | <----
        | fields      | Up to 25 field objects |
        | field.name  | 256 characters         |
        | field.value | 1024 characters        |
        | footer.text | 2048 characters        |
        | author.name | 256 characters         |
        +-------------+------------------------+

        """
        if len(txtmessage) > 4000:
            print(f"To many characters in txtmessage: ", itemID)
            if MessageType == 4:
                if ForgeItem == True:
                    txtmessage = f"${profit_res} profit!\n{Display_signifier} - {relative}\nCost to craft: ${materialPrice_res}!\nForge time: {display_Forge_time}\n{Where_to_buy_text}"
                else:
                    txtmessage = f"${profit_res} profit!\n{Display_signifier} - {relative}\nCost to craft: ${materialPrice_res}!\n{Where_to_buy_text}"
            else:
                if ForgeItem == True:
                    txtmessage = f"${profit_res} profit!\n{Display_signifier} - {relative}\nCost to craft: ${materialPrice_res}!\nForge time: {display_Forge_time}\n{Where_to_buy_text}"
                else:
                    txtmessage = f"${profit_res} profit!\n{Display_signifier} - {relative}!\n{volume_res}Cost to craft: ${materialPrice_res}!\n{avg_Message}\nScore: {res_score}\n{Where_to_buy_text}"
        if len(prem_txtmessage) > 4000:
            print(f"To many characters in prem_txtmessage: ", itemID)
            if MessageType == 4:
                if ForgeItem == True:
                    prem_txtmessage = f"${profit_res} profit!\n{Display_signifier} - {relative}!\nCost to craft: ${materialPrice_res}!\nForge time: {display_Forge_time}\n{Where_to_buy_text}"
                else:
                    prem_txtmessage = f"${profit_res} profit!\n{Display_signifier} - {relative}!\nCost to craft: ${materialPrice_res}!\n{Where_to_buy_text}"
            else:
                if ForgeItem == True:
                    prem_txtmessage = f"${profit_res} profit!\n{Display_signifier} - {relative}!\nCost to craft: ${materialPrice_res}!\nForge time: {display_Forge_time}\n{Where_to_buy_text}"
                else:
                    prem_txtmessage = f"${profit_res} profit!\n{Display_signifier} - {relative}!{EFT_res}{str_profit_per_hour}\n{volume_res}{avg_Message}\nCost to craft: ${materialPrice_res}!\n{Where_to_buy_text}"

        # Create Embeds

        Image_Url_str = "https://th.bing.com/th/id/OIP.0bXRIqrulO7Q0LXictYN9gAAAA?pid=ImgDet&rs=1"  # Place holder thumbnail
        if str(image_url_dict.get(itemID)) != "None":
            Image_Url_str = str(image_url_dict.get(itemID))  # get thumbnail link

        NameValue = f"Collection: {str_CollectionRequirment}"
        # ------------------------ MAKE EMBED ------------------------
        embed = discord.Embed(  # create embed
            color=itemTierColor,
            title=f"**{itemTier} {itemName}**\n{NameValue}",
        )
        embed.description = txtmessage
        embed = embed.set_thumbnail(url=str(Image_Url_str))  # add thumbail
        # ------------------------ MAKE PREMIUM EMBED ------------------------
        prem_embed = discord.Embed(
            color=itemTierColor,
            title=f"**{itemTier} {itemName}**\n{NameValue}",
        )
        prem_embed.description = prem_txtmessage
        prem_embed = prem_embed.set_thumbnail(url=str(Image_Url_str))  # add thumbail

        EmbedDictTxtMessage = prem_txtmessage

        # if debug_mode == False:
        try:
            embedDict[signifier].update(
                {
                    itemID: {
                        "Color": int_color,
                        "ImageURL": Image_Url_str,
                        "Name": NameValue,
                        "Value": EmbedDictTxtMessage,
                        "Updated": relative,
                        "Premium": PremiumFeature,
                    }
                }
            )
        except:
            pass
        IsMajorProfit = False
        if (str_CollectionRequirment.find("Forge") != -1) and (MessageType != 5):
            MessageType = 6
        if (MultiCraft_Retry_Times == 1) or (profit > Basic_Plan_Max):
            SpecialAccess = True
        if MultiCraft_Retry_Times >= 2:
            PremiumFeature = True
        if profit > minium_sell_profit_ping_discord:
            IsMajorProfit = True

        Where_to_buy_text = ""
        if txtmessage == "" or prem_txtmessage == "":
            print(f"Didnt make txtmessage for {itemID}")
            return
        if MessageType > 0:  # Anything but New Query
            if (
                    MessageType == 5
            ):  # Blacklisted item - Put it first because we want to return if its blacklisted
                BlacklistMessage = {
                    "content": f"__**{itemName}**__ IS BLACKLISTED FOR HAVING A KNOWN INFLATED PRICE. __**${profit_res}**__ profit {relative}."
                }
                try:
                    requests.post(Blacklist_discord_webhook_url, data=BlacklistMessage)
                except requests.exceptions.ConnectionError as e:
                    print(f"{itemName}: error at blacklist message: ", e)
                except Exception as e:
                    print(f"{itemName}: error at blacklist message: ", e)
                    if debug_mode == True:
                        raise
                return

            if MessageType == 1:  # No Listings
                No_Listings_dict.update({profit: prem_embed})

            if str(str_CollectionRequirment) == "None":
                No_collection_dict.update({profit: prem_embed})

            if IsMajorProfit == True:  # Major
                Premium_All_dict.update({profit: prem_embed})
                if PremiumFeature == True:
                    Premium_Major_dict.update({profit: prem_embed})
                else:
                    Special_Major_dict.update({profit: embed})
                    Special_All_dict.update({profit: embed})
            if MessageType == 3:  # AH
                if profit >= ah_minium_sell_profit:
                    Premium_AH_dict.update({profit: prem_embed})
                    Premium_All_dict.update({profit: prem_embed})
                    if PremiumFeature == False:
                        if SpecialAccess == True:
                            Special_AH_dict.update({profit: embed})
                            Special_All_dict.update({profit: embed})
                        else:
                            Basic_AH_dict.update({profit: embed})
                            Special_AH_dict.update({profit: embed})
                            Basic_All_dict.update({profit: embed})
                            Special_All_dict.update({profit: embed})

                if (profit >= quick_minium_sell_profit) and (EFT <= Min_Quick_EFT):
                    Quick_dict.update({profit: prem_embed})
                return
            if MessageType == 4:  # BZ
                if profit > bz_minium_sell_profit:
                    Premium_BZ_dict.update({profit: prem_embed})
                    Premium_All_dict.update({profit: prem_embed})
                    if PremiumFeature == False:
                        if SpecialAccess == True:
                            Special_BZ_dict.update({profit: embed})
                            Special_All_dict.update({profit: embed})
                        else:
                            Basic_BZ_dict.update({profit: embed})
                            Basic_All_dict.update({profit: embed})
                            Special_BZ_dict.update({profit: embed})
                            Special_All_dict.update({profit: embed})

                return
            if MessageType == 6:  # Forge
                if profit > forge_minium_sell_profit:
                    Premium_Forge_dict.update({profit: prem_embed})
                    Premium_All_dict.update({profit: prem_embed})
                    if PremiumFeature == False:
                        if SpecialAccess == True:
                            Special_Forge_dict.update({profit: embed})
                            Special_All_dict.update({profit: embed})
                        else:
                            Basic_Forge_dict.update({profit: embed})
                            Basic_All_dict.update({profit: embed})
                            Special_Forge_dict.update({profit: embed})
                            Special_All_dict.update({profit: embed})

                return

    def get_AH_flips():
        # items = Items_data["items"]

        try:
            progress = 0
            AH_data_dict = get_ah_dict()
            for item_ID in recipe_items:
                item_itemsdata = {}  # Itemsdata["items"].get()
                for item in Itemsdata["items"]:
                    if item.get("id") == item_ID:
                        item_itemsdata = item
                if (
                        (
                                (
                                        (str(BZdata["products"].get(item_ID)) == "None")
                                        and (str(item_itemsdata.get("generator")) == "None")
                                        and (str(item_itemsdata.get("soulbound")) == "None")
                                )
                        )
                        or (str(AH_data_dict.get(item_ID)) != "None")
                        or (str(AH_data.get(item_ID)) != "None")
                ):
                    # print(item_ID)
                    progress = progress + 1
                    # if (progress % 100) == 0:  # update
                    #    AH_data_dict = get_ah_dict()
                    lowest_selling = 0
                    volume = 0
                    if str(Volume_data.get(item_ID)) != "None":
                        try:
                            volume = round(len(Volume_data.get(item_ID)) / 7, 1)
                        except:
                            pass
                    avg_price = avg_lbin.get(item_ID) or 0
                    try:
                        lowest_selling = int(AH_data_dict.get(item_ID)["Bids"][0])
                    except:
                        pass

                    # Instant stuff
                    r_Instant = recipe_Price(item_ID, False, 0, "Instant")
                    material_Price_Instant = r_Instant[0]

                    material_list_Instant = r_Instant[1]
                    Where_to_buy_materials_Instant = r_Instant[2]
                    Taxed_profit_Instant = 0

                    if (material_Price_Instant == -2) and (
                            item_ID != "NETHER_BRICK_ITEM"
                    ):
                        item_name = get_Item_Name(item_ID)
                        print(
                            f"ERROR: {item_name} ({item_ID}) DOES NOT HAVE A CRAFTING RECIPE"
                        )
                        Message = {
                            "content": f"{manadory_discord_at} ERROR: {item_name} ({item_ID}) DOES NOT HAVE A CRAFTING RECIPE"
                        }
                        if debug_mode == True:
                            Message = {
                                "content": f"DEBUG: {manadory_discord_at} ERROR: {item_name} ({item_ID}) DOES NOT HAVE A CRAFTING RECIPE"
                            }
                        requests.post(Crash_Report_discord_webhook_url, data=Message)
                    if material_Price_Instant > 1:
                        if (str(lowest_selling) != "None") and (
                                lowest_selling > 0
                        ):  # If the item is being sold by someone
                            profit_Instant = (
                                    lowest_selling - material_Price_Instant
                            )
                            if str(items_with_count.get(item_ID)) != "None":
                                profit_Instant = profit_Instant * int(
                                    items_with_count.get(item_ID)
                                )
                            Tax_Instant = get_taxed_profit(
                                profit_Instant, "AH", (lowest_selling - 1)
                            )
                            Taxed_profit_Instant = profit_Instant - Tax_Instant
                            if Taxed_profit_Instant > quick_minium_sell_profit:
                                # print(f"{item_ID} - normal")
                                Embed_queue.put(
                                    Thread(
                                        target=get_embed,
                                        args=(
                                            3,
                                            item_ID,
                                            Taxed_profit_Instant,
                                            material_list_Instant,
                                            False,
                                            0,
                                            material_Price_Instant,
                                            lowest_selling,
                                            volume,
                                            avg_price,
                                            "Instant",
                                            Where_to_buy_materials_Instant,
                                            Tax_Instant,
                                        ),
                                    )
                                )
                        else:
                            if (avg_price < material_Price_Instant * 10) and (
                                    (avg_price - material_Price_Instant) > minium_no_listing
                            ):  # Hopefully weed out "Donation" items such as emerald blocks
                                Embed_queue.put(
                                    Thread(
                                        target=get_embed,
                                        args=(
                                            1,
                                            item_ID,
                                            (avg_price - material_Price_Instant),
                                            material_list_Instant,
                                            False,
                                            0,
                                            material_Price_Instant,
                                            0,
                                            volume,
                                            avg_price,
                                            "Instant",
                                            Where_to_buy_materials_Instant,
                                            Tax_Instant,
                                        ),
                                    )
                                )
                    if (str(lowest_selling) != "None") and (lowest_selling > 0):
                        previous_Material_list = material_list_Instant
                        previous_profit = Taxed_profit_Instant
                        for retry_times in range(6):  # Multicraft loop
                            r_Instant = recipe_Price(
                                item_ID, True, (retry_times + 1), "Instant"
                            )
                            material_Price_Instant = r_Instant[0]
                            material_list_Instant = r_Instant[1]
                            Where_to_buy_materials_Instant = r_Instant[2]
                            if (
                                    material_list_Instant == previous_Material_list
                            ):  # Dont try to reloop materials that are already in its rawest form
                                pass
                                # break
                            else:
                                previous_Material_list = material_list_Instant

                                profit_Instant = (
                                        lowest_selling - material_Price_Instant
                                )
                                if str(items_with_count.get(item_ID)) != "None":
                                    profit_Instant = profit_Instant * int(
                                        items_with_count.get(item_ID)
                                    )
                                Tax_Instant = get_taxed_profit(
                                    profit_Instant,
                                    "AH",
                                    (lowest_selling - 1),
                                )
                                Taxed_profit_Instant = profit_Instant - Tax_Instant
                                if (
                                        (Taxed_profit_Instant > quick_minium_sell_profit)
                                        and (material_Price_Instant > 1)
                                        and ((previous_profit * 1.2) < Taxed_profit_Instant)
                                ):  # Dont output double craft unless the profit is much higher than normal craft

                                    previous_profit = Taxed_profit_Instant
                                    Embed_queue.put(
                                        Thread(
                                            target=get_embed,
                                            args=(
                                                3,
                                                item_ID,
                                                Taxed_profit_Instant,
                                                material_list_Instant,
                                                True,
                                                retry_times + 1,
                                                material_Price_Instant,
                                                lowest_selling,
                                                volume,
                                                avg_price,
                                                "Instant",
                                                Where_to_buy_materials_Instant,
                                                Tax_Instant,
                                            ),
                                        )
                                    )

                    # Order stuff
                    r_Order = recipe_Price(item_ID, False, 0, "Order")
                    material_Price_Order = r_Order[0]
                    material_list_Order = r_Order[1]
                    Where_to_buy_materials_Order = r_Order[2]
                    Taxed_profit_Order = 0
                    if material_Price_Order > 1:
                        if (str(lowest_selling) != "None") and (
                                lowest_selling > 0
                        ):  # If the item is being sold by someone
                            profit_Order = (
                                    lowest_selling - material_Price_Order
                            )
                            if str(items_with_count.get(item_ID)) != "None":
                                profit_Order = profit_Order * int(
                                    items_with_count.get(item_ID)
                                )
                            Tax_Order = get_taxed_profit(
                                profit_Order, "AH", (lowest_selling - 1)
                            )
                            Taxed_profit_Order = profit_Order - Tax_Order
                            if Taxed_profit_Order > quick_minium_sell_profit:
                                # print(f"{item_ID} - normal")
                                Embed_queue.put(
                                    Thread(
                                        target=get_embed,
                                        args=(
                                            3,
                                            item_ID,
                                            Taxed_profit_Order,
                                            material_list_Order,
                                            False,
                                            0,
                                            material_Price_Order,
                                            lowest_selling,
                                            volume,
                                            avg_price,
                                            "Order",
                                            Where_to_buy_materials_Order,
                                            Tax_Order,
                                        ),
                                    )
                                )
                        if (str(lowest_selling) != "None") and (lowest_selling > 0):
                            previous_Material_list = material_list_Order
                            previous_profit = Taxed_profit_Order
                            for retry_times in range(6):  # Multicraft loop
                                r_Order = recipe_Price(
                                    item_ID, True, (retry_times + 1), "Order"
                                )
                                material_Price_Order = r_Order[0]
                                material_list_Order = r_Order[1]
                                Where_to_buy_materials_Order = r_Order[2]
                                if (
                                        material_list_Order == previous_Material_list
                                ):  # Dont try to reloop materials that are already in its rawest form
                                    pass
                                    # break
                                else:
                                    previous_Material_list = material_list_Order
                                    profit_Order = (
                                            lowest_selling
                                            - material_Price_Order
                                    )
                                    if str(items_with_count.get(item_ID)) != "None":
                                        profit_Order = profit_Order * int(
                                            items_with_count.get(item_ID)
                                        )
                                    Tax_Order = get_taxed_profit(
                                        profit_Order,
                                        "AH",
                                        (lowest_selling - 1),
                                    )
                                    Taxed_profit_Order = profit_Order - Tax_Order
                                    if (
                                            (Taxed_profit_Order > quick_minium_sell_profit)
                                            and (material_Price_Order > 1)
                                            and (
                                            (previous_profit * 1.2) < Taxed_profit_Order
                                    )
                                    ):  # Dont output double craft unless the profit is much higher than normal craft

                                        previous_profit = Taxed_profit_Order
                                        # print(f"{item_ID} - multi")
                                        Embed_queue.put(
                                            Thread(
                                                target=get_embed,
                                                args=(
                                                    3,
                                                    item_ID,
                                                    Taxed_profit_Order,
                                                    material_list_Order,
                                                    True,
                                                    retry_times + 1,
                                                    material_Price_Order,
                                                    lowest_selling,
                                                    volume,
                                                    avg_price,
                                                    "Order",
                                                    Where_to_buy_materials_Order,
                                                    Tax_Order,
                                                ),
                                            )
                                        )
        except requests.exceptions.ConnectionError as e:
            print("error in AH: ", e)

        except NameError:
            print("NameError in AH")
        except Exception as e:
            print("error in AH: ", e)
            if debug_mode == True:
                raise

    def get_Bazzar_flips():

        try:
            BZdata = Bazaar_response.json()
            products = BZdata["products"]
            Totalprogress = len(list(products.keys()))
            progress = 0  # 1255 total items
            Enc_rec = {}
            for item_ID in products:
                start = time.time()
                progress = progress + 1
                # if (progress % 50) == 0:
                #    print(f"{progress}/{Totalprogress}")

                item_info = products[item_ID]
                # Order stuff:
                Order_sell_price = 0
                try:
                    Order_sell_price = item_info["buy_summary"][0][
                        "pricePerUnit"
                    ]  # item_info["quick_status"]["buyPrice"]
                    if str(items_with_count.get(item_ID)) != "None":
                        Order_sell_price = Order_sell_price * int(
                            items_with_count.get(item_ID)
                        )
                except:
                    pass
                Tax_Order = get_taxed_profit(
                    Order_sell_price, "BZ", (Order_sell_price - 0.1)
                )
                Order_Taxed_sell_price = Order_sell_price - Tax_Order
                r_Order = recipe_Price(item_ID, False, 0, "Order")
                material_Price_Order = r_Order[0]
                material_list_Order = r_Order[1]
                Where_to_buy_materials_Order = r_Order[2]
                profit_Order = Order_Taxed_sell_price - material_Price_Order
                if (profit_Order >= bz_minium_sell_profit) and (
                        material_Price_Order > 1
                ):
                    Embed_queue.put(
                        Thread(
                            target=get_embed,
                            args=(
                                4,
                                item_ID,
                                profit_Order,
                                material_list_Order,
                                False,
                                0,
                                material_Price_Order,
                                0,
                                0,
                                0,
                                "Order",
                                Where_to_buy_materials_Order,
                                Tax_Order,
                            ),
                        )
                    )
                previous_Material_list = material_list_Order
                previous_profit = profit_Order
                for retry_times in range(6):  # Multicraft loop
                    r_Order = recipe_Price(item_ID, True, (retry_times + 1), "Order")
                    material_Price_Order = r_Order[0]
                    material_list_Order = r_Order[1]
                    Where_to_buy_materials_Order = r_Order[2]
                    if (
                            material_list_Order == previous_Material_list
                    ):  # Dont try to reloop materials that are already in its rawest form
                        pass
                        # break
                    else:
                        previous_Material_list = material_list_Order
                        Tax_Order = get_taxed_profit(
                            Order_sell_price, "BZ", (Order_sell_price - 0.1)
                        )
                        Order_Taxed_sell_price = Order_sell_price - Tax_Order
                        profit_Order = Order_Taxed_sell_price - material_Price_Order
                        if (
                                (profit_Order >= bz_minium_sell_profit)
                                and (material_Price_Order > 1)
                                and ((previous_profit * 1.2) < profit_Order)
                        ):
                            previous_profit = profit_Order

                            Embed_queue.put(
                                Thread(
                                    target=get_embed,
                                    args=(
                                        4,
                                        item_ID,
                                        profit_Order,
                                        material_list_Order,
                                        True,
                                        retry_times + 1,
                                        material_Price_Order,
                                        0,
                                        0,
                                        0,
                                        "Order",
                                        Where_to_buy_materials_Order,
                                        Tax_Order,
                                    ),
                                )
                            )
                # Instant stuff:
                Instant_sell_price = 0
                try:
                    Instant_sell_price = item_info["sell_summary"][0]["pricePerUnit"]  #
                    if str(items_with_count.get(item_ID)) != "None":
                        Instant_sell_price = Instant_sell_price * int(
                            items_with_count.get(item_ID)
                        )
                except:
                    pass
                Tax_Instant = get_taxed_profit(
                    Instant_sell_price, "BZ", (Instant_sell_price - 0.1)
                )
                Instant_Taxed_sell_price = Instant_sell_price - Tax_Instant
                r_Instant = recipe_Price(item_ID, False, 0, "Instant")
                material_Price_Instant = r_Instant[0]
                material_list_Instant = r_Instant[1]
                Where_to_buy_materials_Instant = r_Instant[2]
                profit_Instant = Instant_Taxed_sell_price - material_Price_Instant
                if (
                        (profit_Instant > 0)
                        and (profit_Instant >= bz_minium_sell_profit)
                        and (material_Price_Instant > 1)
                ):
                    Embed_queue.put(
                        Thread(
                            target=get_embed,
                            args=(
                                4,
                                item_ID,
                                profit_Instant,
                                material_list_Instant,
                                False,
                                0,
                                material_Price_Instant,
                                0,
                                0,
                                0,
                                "Instant",
                                Where_to_buy_materials_Instant,
                                Tax_Instant,
                            ),
                        )
                    )

                previous_Material_list = material_list_Instant
                previous_profit = profit_Instant
                for retry_times in range(6):  # Multicraft loop
                    r_Instant = recipe_Price(
                        item_ID, True, (retry_times + 1), "Instant"
                    )
                    material_Price_Instant = r_Instant[0]
                    material_list_Instant = r_Instant[1]
                    Where_to_buy_materials_Instant = r_Instant[2]
                    if (
                            material_list_Instant == previous_Material_list
                    ):  # Dont try to reloop materials that are already in its rawest form
                        pass
                        # break
                    else:
                        previous_Material_list = material_list_Instant
                        Tax_Instant = get_taxed_profit(
                            Instant_sell_price, "BZ", (Order_sell_price - 0.1)
                        )
                        Instant_Taxed_sell_price = Instant_sell_price - Tax_Instant
                        profit_Instant = (
                                Instant_Taxed_sell_price - material_Price_Instant
                        )
                        if (
                                (profit_Instant > bz_minium_sell_profit)
                                and (material_Price_Instant > 1)
                                and ((previous_profit * 1.2) < profit_Instant)
                        ):
                            previous_profit = profit_Instant

                            Embed_queue.put(
                                Thread(
                                    target=get_embed,
                                    args=(
                                        4,
                                        item_ID,
                                        profit_Instant,
                                        material_list_Instant,
                                        True,
                                        retry_times + 1,
                                        material_Price_Instant,
                                        0,
                                        0,
                                        0,
                                        "Instant",
                                        Where_to_buy_materials_Instant,
                                        Tax_Instant,
                                    ),
                                )
                            )

        except requests.exceptions.ConnectionError as e:
            print("error in BZ: ", e)
        except NameError:
            print("NameError in BZ")
            if debug_mode == True:
                raise
        except:
            print("error in BZ")
            if debug_mode == True:
                raise

    def get_NPC_flips():

        try:
            NPC_sellprices = {}
            for item in Itemsdata["items"]:
                if str(item.get("npc_sell_price")) != "None":
                    NPC_sellprices.update({item.get("id"): int(item.get("npc_sell_price"))})
            for item_ID in NPC_sellprices:
                r_Instant = recipe_Price(item_ID, False, 0, "Instant")
                material_Price_Instant = r_Instant[0]
                material_list_Instant = r_Instant[1]
                Where_to_buy_materials_Instant = r_Instant[2]
                profit_Instant = NPC_sellprices.get(item_ID) - material_Price_Instant
                profit_Instant = round(profit_Instant, 2)
                if (profit_Instant > 0) and (material_Price_Instant > 1):
                    pass
                    # print(f"{item_ID} has a Instant profit of {profit_Instant}")

                r_Order = recipe_Price(item_ID, False, 0, "Order")
                material_Price_Order = r_Order[0]
                material_list_Order = r_Order[1]
                Where_to_buy_materials_Order = r_Order[2]
                profit_Order = NPC_sellprices.get(item_ID) - material_Price_Order
                profit_Order = round(profit_Order, 2)
                if (profit_Order > 0) and (material_Price_Order > 1):
                    pass
                    # print(f"{item_ID} has a Order profit of {profit_Order}")

        except requests.exceptions.ConnectionError as e:
            print("error in NPC_flips: ", e)
        except NameError as e:
            print("NameError in NPC_flips: ", e)
            if debug_mode == True:
                raise
        except Exception as e:
            print("error in NPC_flips: ", e)
            if debug_mode == True:
                raise

    def do_outputs():
        safemode = False
        if safemode == False:
            threads = [
                Thread(target=Basic_AH_output),
                Thread(target=Basic_BZ_output),
                Thread(target=Special_AH_output),
                Thread(target=Special_BZ_output),
                Thread(target=Premium_AH_output),
                Thread(target=Premium_BZ_output),
                Thread(target=Premium_All_output),
                Thread(target=Special_All_output),
                Thread(target=Basic_All_output),
                Thread(target=No_Listings_output),
                Thread(target=No_collection_output),
                Thread(target=Quick_output),
                Thread(target=Special_Major_output),
                Thread(target=Premium_Major_output),
                Thread(target=Basic_Forge_output),
                Thread(target=Special_Forge_output),
                Thread(target=Premium_Forge_output),
            ]
            [t.start() for t in threads]
            [t.join() for t in threads]

        else:
            # with ThreadPoolExecutor as executer:

            Premium_All_output()
            Special_All_output()
            Basic_All_output()
            No_Listings_output()
            No_collection_output()
            Quick_output()
            Special_Major_output()
            Premium_Major_output()
            Basic_Forge_output()
            Basic_Forge_output()
            Special_Forge_output()
            Premium_Forge_output()
        return

    def get_flips():
        try:
            Thread(target=get_AH_flips).start()
            Thread(target=get_Bazzar_flips).start()
            # Thread(target=get_NPC_flips).start()
            return True
        except RuntimeError:
            print("RuntimeError in get_flips")
            return False
        except Exception as e:
            print("error in get_flips: ", e)
            return False

    start = time.time()
    AH_data_dict = get_ah_dict()

    # ------------------------------------------------#
    # Get flip info + queue embeds:
    success = False
    while success == False:
        success = get_flips()
        time.sleep(5)

    # -----------------------------------------------------#
    # Make Embeds:
    while not Embed_queue.empty():
        try:
            (Embed_queue.get()).start()  # get embeds/item info
            Embed_queue.task_done()
        except RuntimeError:
            print("RuntimeError in Embed Queue waiting to cooldown")
            Embed_queue.join()

        while (threading.active_count() > 150):
            # Maximum threads going at once to prevent discord rate limit (Can get up to 750+ if let unchecked)
            time.sleep(0.2)

    # print(sorted(No_collection_dict.items()))
    Embed_queue.join()

    # if debug_mode == False:
    # Write embed info for the "Hypixel Flipper Bot" to read
    with open(EmbedInfo_path, "w") as EmbedInfoFile:
        EmbedInfoFile.write(f"{embedDict}")
    # -----------------------------------------------------#
    # Output top profits:
    # Go Ahead and display top profits

    Thread(target=topProfitOutput).start()

    # -----------------------------------------------------#
    dt = round(time.time())
    relative = f"<t:{dt}:R>"
    Moderation_webhook.edit_message(
        message_id=1139754683141988402, content=f"Bot last updated: {relative}"
    )
    # Moderation_webhook.send(content="//update") #Figure out a way to make it once every 12 hours
    # -----------------------------------------------------#
    # Output profits
    do_outputs()

    # -----------------------------------------------------#
    end = time.time()
    response = f"Main: Success!!! Took {round(end - start)} seconds! {time.ctime(time.time())}"
    print(response)
    return response
    #######################################
    #######################################
    #######################################
    #######################################
    #######################################
    #######################################
    #######################################
    #######################################
    #######################################
    #######################################
    #######################################
    #######################################

    # IMPORTS


def decode_inventory_data(raw_data):
    data = nbt.nbt.NBTFile(fileobj=io.BytesIO(base64.b64decode(raw_data)))
    return (
        data["i"][0]["tag"]["ExtraAttributes"]["id"].value,
        data["i"][0]["Count"].value,
    )


def volume():
    try:
        with open("volume_ignore.txt", "r") as volume_ignore_file:
            volume_ignore = ast.literal_eval(volume_ignore_file.read())
    except FileNotFoundError as e:
        with open("volume_ignore.txt", "w") as volume_ignore_file:
            volume_ignore_file.write("{}")

    # -----vv Volume Creator vv-----#
    try:
        print(f"writing volume... {time.ctime(time.time())}")
        start = time.time()
        try:
            with open("volume.txt", "r") as volume_file:
                volume_data = ast.literal_eval(volume_file.read())
        except FileNotFoundError as e:
            with open("volume.txt", "w") as volume_file:
                volume_file.write("{}")

        try:
            with open("all_time_volume.txt", "r") as all_time_volume_file:
                all_time_volume_data = ast.literal_eval(all_time_volume_file.read())
        except FileNotFoundError as e:
            with open("all_time_volume.txt", "w") as all_time_volume_file:
                all_time_volume_file.write("{}")

        AH_response = False
        while (AH_response == False):
            try:
                AH_response = requests.get("https://api.hypixel.net/skyblock/auctions_ended", timeout=3)
            except:
                pass
        AH_json = AH_response.json()
        AH_ended = AH_json["auctions"]
        for data in AH_ended:
            EPOCH = int(time.time())
            auc_id = data.get("auction_id")

            if (
                    (data.get("bin") == True)
                    and (len(data.get("buyer")) > 20)
                    and (volume_ignore.get(auc_id) is None)
            ):
                item_data = decode_inventory_data(data.get("item_bytes"))
                item_id = item_data[0]
                item_id = f"{item_id}"
                amount = int(item_data[1])

                volume_ignore.update({auc_id: EPOCH})
                if str(volume_data.get(item_id)) == "None":
                    volume_data.update({item_id: [EPOCH]})
                else:
                    EPOCH_list = volume_data.get(item_id)
                    for i in range(amount):
                        # Go by items bought not sale
                        EPOCH_list.append(EPOCH)

                if str(all_time_volume_data.get(item_id)) == "None":
                    all_time_volume_data.update({item_id: [EPOCH]})
                else:
                    all_time_EPOCH_list = all_time_volume_data.get(item_id)
                    for i in range(amount):
                        # Go by items bought not sale
                        all_time_EPOCH_list.append(EPOCH)

                    all_time_volume_data.update({item_id: all_time_EPOCH_list})

        EPOCH = int(time.time())
        for item_id in volume_data:
            EPOCH_list = volume_data.get(item_id)
            rList = []
            for e in EPOCH_list:
                # 14 days : 1209600
                # 10 days : 864000
                # 7 days : 604800
                # 3 days : 259200
                if e < int(EPOCH - 604800):
                    rList.append(e)
            for r in rList:
                EPOCH_list.remove(r)
            volume_data.update({item_id: EPOCH_list})

        oldest_all_time_vol = 0
        for item_id in all_time_volume_data:
            EPOCH_list = all_time_volume_data.get(item_id)
            for e in EPOCH_list:
                if (e < oldest_all_time_vol) or (oldest_all_time_vol == 0):
                    oldest_all_time_vol = e

        print(
            f"Oldest all time vol is {round(((EPOCH - oldest_all_time_vol) / 86400), 3)} days old"
        )
        oldest_vol = 0
        for item_id in volume_data:
            EPOCH_list = volume_data.get(item_id)
            for e in EPOCH_list:
                if (e < oldest_vol) or (oldest_vol == 0):
                    oldest_vol = e

        print(f"Oldest vol is {round(((EPOCH - oldest_vol) / 86400), 3)} days old")

        with open("volume.txt", "w") as volume_file:
            volume_file.write(f"{volume_data}")

        with open("all_time_volume.txt", "w") as all_time_volume_file:
            all_time_volume_file.write(f"{all_time_volume_data}")

        # Remove old auc_id's to ignore to prevent flooding
        items_to_pop = []
        for aucid in volume_ignore:
            e = int(volume_ignore.get(aucid))
            if e < int(EPOCH - 90):
                items_to_pop.append(aucid)
                # print(f"Removing {aucid} for being {EPOCH - e} seconds old")
        for item in items_to_pop:
            volume_ignore.pop(item)

        with open("volume_ignore.txt", "w") as volume_ignore_file:
            volume_ignore_file.write(f"{volume_ignore}")

        end = time.time()
        response = f"Volume Done! Took {round(end - start)} seconds! Oldest vol is {round(((EPOCH - oldest_vol) / 86400), 3)} days old"
        print(response)
    except Exception as e:
        print("error in volume_creator: ", e)

    # -----^^ Volume Creator ^^-----#


########################################################################################
########################################################################################
########################################################################################
########################################################################################
########################################################################################


def lowest():
    start = time.time()

    def get_new_Page(page):
        New_AH_response = False
        while (New_AH_response == False):
            try:
                New_AH_response = requests.get("https://api.hypixel.net/skyblock/auctions", params={"page": page},
                                               timeout=5)
            except:
                pass
        New_AH_data = New_AH_response.json()

        return New_AH_data

    def decode_inventory_data(raw_data):
        # Decode NBT data
        data = nbt.nbt.NBTFile(fileobj=io.BytesIO(base64.b64decode(raw_data)))
        return (
            data["i"][0]["tag"]["ExtraAttributes"]["id"].value,
            data["i"][0]["Count"].value,
        )

    def fetch_auction_data(page):
        New_AH_data = get_new_Page(page)
        if "auctions" in New_AH_data:
            return New_AH_data["auctions"]
        return []

    def get_all_auctions():
        # while True:
        AH_request = requests.get("https://api.hypixel.net/skyblock/auctions",
                                  timeout=5)  # re-get response to re-check total pages
        AH_data = AH_request.json()
        AH_data_dict = {}
        total_pages = AH_data["totalPages"]
        All_auctions = {}
        i = 0
        ID = 0

        # Fetch all the pages of auctions and put them in a dict with a unique ID
        for page in range(total_pages):
            try:
                data = fetch_auction_data(page)

                for auction in data:
                    All_auctions.update({ID: auction})
                    ID = ID + 1
                # print(f"Got page {page}/{total_pages}")
            except:
                print("Problem getting page #", page)

        sorted_auctions = {}

        # Iterate through the list of unique auctions, find auctions with identical itemIDs and put them in a list in the dict... IE:
        # BEFORE:{0: AUCINFO, 1: AUCINFO, 2: AUCINFO}
        # AFTER: {"DIAMOND_SWORD":[{"starting_bid":1, "Count":1, "item_name":"Diamond Sword"}, {"starting_bid":2, "Count":1, "item_name":"Diamond Sword"}, {"starting_bid":0.5, "Count":1, "item_name":"Diamond Sword"}]}
        for auc in All_auctions.values():
            if auc["bin"] and auc["starting_bid"] is not None:
                itemName = auc["item_name"]
                item_bytes = auc["item_bytes"]
                bid = auc["starting_bid"]
                data = decode_inventory_data(str(item_bytes))
                auc_ItemID = data[0]
                count = data[1]

                if sorted_auctions.get(auc_ItemID) is not None:
                    sorted_auctions[auc_ItemID].append(
                        {
                            "starting_bid": bid,
                            "Count": count,
                            "item_name": itemName,
                        }
                    )
                else:
                    sorted_auctions[auc_ItemID] = [
                        {
                            "starting_bid": bid,
                            "Count": count,
                            "item_name": itemName,
                        }
                    ]
        return sorted_auctions  # All_auctions

    def write_AH_dict():
        print(f"writing lowest selling... {time.ctime(time.time())}")
        lbin = {}
        AH_data_dict = {}
        # -----vv Get lowest selling prices and write it into a txt file vv-----#
        try:
            sorted_auctions = get_all_auctions()  # Get all auction

            for auc_ItemID in sorted_auctions:
                aucs = sorted_auctions.get(auc_ItemID)
                # FORMAT: {"DIAMOND_SWORD":[{"starting_bid":1, "Count":1, "item_name":"Diamond Sword"}, {"starting_bid":2, "Count":1, "item_name":"Diamond Sword"}, {"starting_bid":0.5, "Count":1, "item_name":"Diamond Sword"}]}
                for auc in aucs:
                    # auc = {"starting_bid":1, "Count":1, "item_name":"Diamond Sword"}
                    itemName = auc["item_name"]
                    count = auc["Count"]
                    bid = auc["starting_bid"] / count
                    EPOCH = time.time()

                    if auc_ItemID in AH_data_dict:
                        bidlist = AH_data_dict[auc_ItemID]["Bids"]
                        countlist = AH_data_dict[auc_ItemID]["Count"]
                        combined_data = sorted(
                            zip(bidlist, countlist), key=lambda x: x[0]
                        )
                        bidlist, countlist = zip(*combined_data)

                        if bid not in bidlist:
                            bidlist += (bid,)
                            countlist += (count,)

                        AH_data_dict[auc_ItemID] = {
                            "Bids": list(bidlist),
                            "Count": list(countlist),
                        }

                    else:
                        AH_data_dict[auc_ItemID] = {"Bids": [bid], "Count": [count]}

                    if auc_ItemID in lbin and bid < lbin[auc_ItemID]["Price"]:
                        lbin[auc_ItemID] = {"EPOCH": EPOCH, "Price": bid}
                    elif auc_ItemID not in lbin:
                        lbin[auc_ItemID] = {"EPOCH": EPOCH, "Price": bid}
            # print(AH_data_dict)
            with open("lowest_selling.txt", "w") as lowest_selling_file:
                lowest_selling_file.write(f"{AH_data_dict}")




        except NameError:
            print("NameErorr in main!")

        except Exception as e:
            print(f"Problem occured in write_AH_dict! {e}")
        return lbin

    complete_lbin = write_AH_dict()
    # = data[1]
    # complete_AH_data_dict = data[0]

    # Write data into files to store
    try:
        with open("alltime_lbin_data.txt", "r") as alltime_lbin_file:
            alltime_lbin_data = ast.literal_eval(alltime_lbin_file.read())
    except FileNotFoundError as e:
        with open("alltime_lbin_data.txt", "w") as alltime_lbin_file:
            alltime_lbin_file.write("{}")

    # add lbins to alltime data
    for itemID in complete_lbin:
        if str(alltime_lbin_data.get(itemID)) == "None":
            info = complete_lbin.get(itemID)
            EPOCH = info.get("EPOCH")
            Price = info.get("Price")
            alltime_lbin_data.update({itemID: {"EPOCH": [EPOCH], "Price": [Price]}})
        else:
            info = complete_lbin.get(itemID)
            EPOCH = info.get("EPOCH")
            Price = info.get("Price")
            rewritten_info = alltime_lbin_data.get(itemID)
            rewritten_EPOCH = rewritten_info.get("EPOCH")
            rewritten_Price = rewritten_info.get("Price")
            if len(rewritten_Price) > 0:
                if rewritten_Price[-1] != Price:
                    # Make sure we aren't getting the same lbin twice
                    rewritten_Price.append(Price)
                    rewritten_EPOCH.append(EPOCH)
            else:
                print(rewritten_Price)
                rewritten_Price.append(Price)
                rewritten_EPOCH.append(EPOCH)

    avg_lbin = {}

    # Remove 30 day old lbins & make lbin average
    for itemID in alltime_lbin_data:
        data = alltime_lbin_data.get(itemID)
        EPOCH_list = data.get("EPOCH")
        Price_list = data.get("Price")
        Current_EPOCH = time.time()

        ########
        # Remove items older than 30 days vv
        remove_items = []
        for EPOCH in EPOCH_list:
            if EPOCH < (Current_EPOCH - 2592000):
                remove_items.append(EPOCH_list.index(EPOCH))
        remove_items.sort(
            reverse=True
        )  # start with biggest so we dont mess up index order
        for indexx in remove_items:
            EPOCH_list.remove(EPOCH_list[indexx])
            Price_list.remove(Price_list[indexx])
        # Remove items older than 30 days ^^
        ########

        ###Avg out all the Lbins in the last 30 days vv
        total = 0
        itt = 0
        for Price in Price_list:
            total = total + Price
            itt = itt + 1
        if (itt > 0) and (total > 0):
            avg_lbin.update({itemID: int(total / itt)})

    with open("alltime_lbin_data.txt", "w") as lbin_file:
        lbin_file.write(f"{alltime_lbin_data}")

    with open("avg_lbin.txt", "w") as avg_lbin_file:
        avg_lbin_file.write(f"{avg_lbin}")

    end = time.time()
    response = f"LBin: Done! Took {round(end - start)} seconds!"
    print(response)


loop = True
if loop == True:
    loopnum = 0
    while True:

        loopnum = loopnum + 1
        print("")
        print(f"Starting loop number: {loopnum}")
        Thread(target=volume, name="Volume").start()
        Thread(target=lowest, name="Lowest").start()
        Thread(target=main, name="Main").start()
        volume_itt = 0
        # Volume needs to be updated every 50 seconds or else we risk volume being inaccurate
        while threading.active_count() > 1:
            volume_itt = volume_itt + 1
            time.sleep(1)
            if volume_itt > 45:
                Thread(target=volume, name="Volume").start()
                volume_itt = 0
else:
    Thread(target=volume, name="Volume").start()
    Thread(target=lowest, name="Lowest").start()
    Thread(target=main, name="Main").start()
    while threading.active_count() > 1:
        time.sleep(1)
        # print(f"{time.ctime(time.time())}: running... {threading.active_count()}  --- {threading.enumerate()}")



