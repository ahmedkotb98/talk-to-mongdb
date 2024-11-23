class ConfigLLM:
    TABLE_SCHEMA = """
        "_id": "ObjectId",
        "Creation Date": "Date",
        "Purchase Date": "Date",
        "Fiscal Year": "string",
        "LPA Number": "string",
        "Purchase Order Number": "string",
        "Requisition Number": "string",
        "Acquisition Type": "string",
        "Sub-Acquisition Type": "string",
        "Acquisition Method": "string",
        "Sub-Acquisition Method": "string",
        "Department Name": "string",
        "Supplier Code": "Double",
        "Supplier Name": "string",
        "Supplier Qualifications": "string",
        "Supplier Zip Code": "string",
        "CalCard": "string",
        "Item Name": "string",
        "Item Description": "string",
        "Quantity": "Double",
        "Unit Price": "string",
        "Total Price": "string",
        "Classification Codes": "string",
        "Normalized UNSPSC": "string",
        "Commodity Title": "string",
        "Class": "string",
        "Class Title": "string",
        "Family": "string",
        "Family Title": "string",
        "Segment": "string",
        "Segment Title": "string"
    """
    SCHEMA_DESCRIPTION = """
    Here is the description of fields  to determine what each key represents:

    1. **Field Name:** Creation Date  
    **Field Description:** System Date

    2. **Field Name:** Purchase Date  
    **Field Description:** Date of purchase order is entered by the user. This date can be backdated; therefore, the creation date is primarily used.

    3. **Field Name:** Fiscal Year  
    **Field Description:** Fiscal year derived based on creation date. State of California fiscal year starts on July 1 and ends on June 30.

    4. **Field Name:** LPA Number  
    **Field Description:** Leveraged Procurement Agreement (LPA) Number, aka Contract Number. If there is a contract number in this field, the amount is considered contract spend.

    5. **Field Name:** Purchase Order Number  
    **Field Description:** Purchase Order Numbers are not unique; different departments can have the same purchase order number.

    6. **Field Name:** Requisition Number  
    **Field Description:** Requisition Numbers are not unique; different departments can have the same purchase order number.

    7. **Field Name:** Acquisition Type  
    **Field Description:** Type of Acquisition: Non-IT Goods, Non-IT Services, IT Goods, IT Services.

    8. **Field Name:** Sub-Acquisition Type  
    **Field Description:** A sub-acquisition type depends on the acquisition type used. Please see the data dictionary for additional information.

    9. **Field Name:** Acquisition Method  
    **Field Description:** Type of acquisition used to make a purchase. Please see the data dictionary and supplemental acquisition method document for further information.

    10. **Field Name:** Sub-Acquisition Method  
        **Field Description:** A sub-acquisition method depends on the acquisition method used. Please see the data dictionary for additional information.

    11. **Field Name:** Department Name  
        **Field Description:** Name of the purchasing department. Normalized field.

    12. **Field Name:** Supplier Code  
        **Field Description:** Supplier code. Normalized field.

    13. **Field Name:** Supplier Name  
        **Field Description:** Supplier name entered by the supplier at the time of registration with the state.

    14. **Field Name:** Supplier Qualifications  
        **Field Description:** Identifies supplier qualifications as a certified small business (SB), small business enterprise (SBE), disabled veteran business enterprise (DVBE), non-profits (NP), and micro-business (MB). These qualifications are not mutually exclusive; a supplier can be any combination of these.

    15. **Field Name:** Supplier Zip Code  
        **Field Description:** Supplier Zip Code.

    16. **Field Name:** CalCard  
        **Field Description:** State credit card (CalCard) used for purchase? Yes/No.

    17. **Field Name:** Item Name  
        **Field Description:** Name of items being purchased.

    18. **Field Name:** Item Description  
        **Field Description:** Description of items being purchased.

    19. **Field Name:** Quantity  
        **Field Description:** Quantity of items being purchased.

    20. **Field Name:** Unit Price  
        **Field Description:** Unit price of items.

    21. **Field Name:** Total Price  
        **Field Description:** Total price of items. This does not include taxes or shipping.

    22. **Field Name:** Classification Codes  
        **Field Description:** United Nations Standard Products and Services Code® (UNSPSC) v. 14 of items purchased. This field may have more than one UNSPSC number based on the line items in the purchase order entered into eSCPRS.

    23. **Field Name:** Normalized UNSPSC  
        **Field Description:** Normalized UNSPSC (United Nations Standard Products and Services Code® v. 14) number. The first 8 digits of the classification code identify the entire purchase order.

    24. **Field Name:** Commodity Title  
        **Field Description:** Correlated commodity title based on the 8-digit Normalized UNSPSC"".

    25. **Field Name:** Class  
        **Field Description:** Correlated class number based on the 8-digit Normalized UNSPSC"".

    26. **Field Name:** Class Title  
        **Field Description:** Correlated class title based on the 8-digit Normalized UNSPSC"".

    27. **Field Name:** Family  
        **Field Description:** Correlated family number based on the 8-digit Normalized UNSPSC"".

    28. **Field Name:** Family Title  
        **Field Description:** Correlated family title based on the 8-digit Normalized UNSPSC"".

    29. **Field Name:** Segment  
        **Field Description:** Correlated segment number based on the 8-digit Normalized UNSPSC"".
    """

    FEW_SHOT_EXAMPLE_1 = """
    [
        {
            "$match": {
                "Creation Date": {
                    "$gte": datetime(2010, 1, 1),
                    "$lte": datetime(2013, 12, 31, 23, 59, 59, 999000)
                }
            }
        },
        {
            "$count": "Total Number of Orders"
        }
    ]
    """

    FEW_SHOT_EXAMPLE_2 = """
    [
        {
            "$addFields": {
                "Numeric Total Price": {
                    "$convert": {
                        "input": {"$substr": ["$Total Price", 1, -1]},
                        "to": "double",
                        "onError": None,
                        "onNull": None
                    }
                }
            }
        },
        {
            "$group": {
                "_id": None,
                "Total Price Sum": {"$sum": "$Numeric Total Price"}
            }
        },
        {
            "$project": {
                "_id": 0,
                "Total Price Sum": 1
            }
        }
    ]
    """

    FEW_SHOT_EXAMPLE_3 = """
    [
        {
            "$addFields": {
                "Numeric Total Price": {
                    "$convert": {
                        "input": {"$substr": ["$Total Price", 1, -1]},
                        "to": "double",
                        "onError": None,
                        "onNull": None
                    }
                }
            }
        },
        {
            "$group": {
                "_id": {
                    "Year": {"$year": "$Creation Date"},
                    "Quarter": {"$ceil": {"$divide": [{"$month": "$Creation Date"}, 3]}}
                },
                "Total Spending": {"$sum": "$Numeric Total Price"}
            }
        },
        {
            "$sort": {"Total Spending": -1}
        },
        {
            "$limit": 1
        },
        {
            "$project": {
                "Quarter": "$_id.Quarter",
                "Year": "$_id.Year",
                "Total Spending": 1,
                "_id": 0
            }
        }
    ]
    """
    FEW_SHOT_EXAMPLE_4 = """    
    [
        {
            "$addFields": {
                "numeric_price": {
                    "$convert": {
                        "input": { "$substr": ["$Total Price", 1, -1] },  
                        "to": "double",
                        "onError": 0,  
                        "onNull": 0    
                    }
                }
            }
        },
        {
            "$group": {
                "_id": "$Acquisition Type",
                "total_spending": { "$sum": "$numeric_price" }
            }
        },
        { "$sort": { "total_spending": -1 } }  
    ]    
    """
