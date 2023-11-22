import os
from static.prompts import eval_prompt_general, eval_prompt_Diabetes_UK, eval_prompt_Lord_Sugar, eval_prompt_NICE, eval_prompt_LBG, eval_prompt_KFC, eval_prompt_Shell

# prompt and completion costs for LLM models. used to calculate cost per article and running cost
# keep updated regularly to get accurate pricing
dict_model_costs = {'gpt-4':                {'prompt': 0.03, 'completion': 0.06},
                    'gpt-4-1106-preview':   {'prompt': 0.01, 'completion': 0.03},
                    'gpt-4-32k':            {'prompt': 0.06, 'completion': 0.12},
                    'gpt-3.5-turbo':        {'prompt': 0.0015, 'completion': 0.002},
                    'gpt-3.5-turbo-16k':    {'prompt': 0.003, 'completion': 0.004},}

# front end will provide one of the two keys in the dict below
# this dict will determine the current version of this model to use for analysis
# storing this here removes the requirement to edit the HTML for each model change
dict_model_current = {# 'gpt-4':              'gpt-4',
                    'gpt-4':              'gpt-4-1106-preview',
                    'gpt-3.5-turbo':        'gpt-3.5-turbo'}

# reformatted above dict to allow for easier execution of several processes
# - search all name variations for each brand/competitor for entity extraction
# - potentially send name variations for each individual brand/competitor to GPT for analysis
# - use all name variations in hard-coded auto Prominence and Noopsis
# currently testing (as of Aug 8 2023)
dict_brand_brands_2 = {
    "ASOS": {
        "ASOS":                         ["ASOS"]},
    "BDO Ireland": {
        "BDO":                          ["BDO", "BDO Ireland"]},
    "Diabetes UK": {
        "Diabetes UK":                  ["Diabetes UK"]},
    "Disney": {
        "Disney":                       ["Disney"]},
    "Failte Ireland": {
        "Failte Ireland":               ["Failte Ireland"],
        "Tourism Ireland":              ["Tourism Ireland"],
        "Irish Hotels Federation":      ["Irish Hotels Federation"],
        "Irish Tourism Industry Confederation": 
                                        ["Irish Tourism Industry Confederation"],
        "Restaurants Association of Ireland": 
                                        ["Restaurants Association of Ireland"],
        "Catherine Martin":             ["Catherine Martin"],
        "Jack Chambers":                ["Jack Chambers"],
    },
    "Federation of Small Businesses": {
        "Federation of Small Businesses": 
                                        ["Federation of Small Businesses", "FSB"]
    },
    "FirstGroup": {
        "FirstGroup":                   ["FirstGroup", "First Group", "FirstBus", "First Bus"],
        "Stagecoach":                   ["Stagecoach"],
        "National Express":             ["National Express"],
        "Go Ahead":                     ["Go Ahead", "GoAhead"],
    },
    "Go Ahead": {
        "Go Ahead":                     ["Go Ahead", "GoAhead", "Go-Ahead"],
        "Abellio":                      ["Abellio"],
        "Arriva":                       ["Arriva"],
        "Stagecoach":                   ["Stagecoach"],
        "National Express":             ["National Express"],
    },
    "KFC": {
        "KFC":                          ["KFC"],
        "Burger King":                  ["Burger King"],
        "Deliveroo":                    ["Deliveroo"],
        "Greggs":                       ["Greggs"],
        "McDonald's":                   ["McDonald's"],
        "Pizza Hut":                    ["Pizza Hut"],
        "Uber Eats":                    ["Uber Eats"],
    },
    "Lloyds Banking Group": {
        "Lloyds Banking Group":         ["Lloyds Banking Group", "Lloyds Bank", "Lloyds", "LBG"],
        "Halifax":                      ["Halifax"],
        "Bank of Scotland":             ["Bank of Scotland"],
        "MBNA":                         ["MBNA"],
        "Birmingham Midshires":         ["Birmingham Midshires"],
        "Lex auto lease":               ["Lex auto lease"],
        "Black Horse":                  ["Black Horse"],
        "Tusker":                       ["Tusker"],
        "Barclays":                     ["Barclays"],
        "HSBC":                         ["HSBC"],
        "Nationwide":                   ["Nationwide"],
        "NatWest":                      ["NatWest"],
        "RBS":                          ["RBS", "Royal Bank of Scotland"],
        "Santander":                    ["Santander"],
        "TSB":                          ["TSB"],
        "Monzo":                        ["Monzo"],
        "Starling":                     ["Starling"],
        "Paypal":                       ["Paypal"],
        "Revolut":                      ["Revolut"],
        "Metro":                        ["Metro"],
        "First Direct":                 ["First Direct"],
    },
    "Lord Sugar": { 
        "Lord Alan Sugar":              ["Lord Alan Sugar", "Lord Sugar", "Alan Sugar"],
        "The Apprentice":               ["The Apprentice", "Apprentice"]
    },
    "Molson Coors": {
        "Molson Coors":                 ["Molson", "Molson Coors", "Coors"],
        "AB InBev":                     ["AB InBev", "Anheuser-Busch"],
        "Asahi":                        ["Asahi"],
        "Carlsberg":                    ["Carlsberg"],
        "Diageo":                       ["Diageo"],
        "Heineken":                     ["Heineken"],
    },
    "NICE": {
        "NICE":                         ["NICE", "National Institute for Health and Care Excellence"]},
    "The Post Office": {
        "The Post Office":              ["Post Office"]},
    "Royal Academy of Arts": {
        "Royal Academy of Arts":        ["RAA", "Royal Academy of Arts"]},
    "Santander": { # used only for brand_consolidator function and prominence. 
                    #brand searches (which use this dict for other clients) are imported from the GI Banks column for Santander
        "Santander":                    ["Santander"],
        "Barclays":                     ["Barclays", "Barclaycard"],
        "HSBC":                         ["HSBC"],
        "Lloyds":                       ["Lloyds"],
        "RBS NatWest":                  ["RBS", "Natwest", "NatWest", "RBS Natwest", "RBS NatWest"],
    },
    "Scottish Water": {
        "Scottish Water":               ["Scottish Water"]},
    "Shell": {
        "Shell":                        ["Shell"]}, 
        # add competitors
    "Three": {
        "Three":                        ["Three"],
        "BT Mobile":                    ["BT Mobile"],
        "Carphone Warehouse":           ["Carphone Warehouse", "Dixons Carphone"],
        "EE":                           ["EE"],
        "O2":                           ["O2"],
        "Sky Mobile":                   ["Sky Mobile"],
        "Smarty":                       ["Smarty"],
        "Tesco Mobile":                 ["Tesco Mobile"],
        "Virgin Mobile":                ["Virgin Mobile"],
        "Vodafone":                     ["Vodafone"],
        "VOXI":                         ["VOXI", "Voxi"],
    },
    "Walgreens Boots Alliance": {
        "Walgreens Boots Alliance":     ["Walgreens Boots Alliance", "Walgreens", "Boots", "WBA"],
    },
    "Zoological Society of London": {
        "Zoological Society of London": ["Zoological Society of London", "London Zoological Society", "ZSL"]},
}

dict_brand_spokes = {
    "ASOS": {

        },
    "BDO Ireland": {

        },
    "Diabetes UK": {

        },
    "Disney": {

        },
    "Failte Ireland": {

    },
    "Federation of Small Businesses": {
        
    },
    "FirstGroup": {
        "FirstGroup":                   {
                    "Claire Mann": ["Claire Mann"],
                    "Duncan Cameron": ["Duncan Cameron"],
                    "Graeme Macfarlan": ["Graeme Macfarlan", "Graeme Macfarlane", "Graham Macfarlan", "Graham Macfarlane"],
                    "Unnamed FirstGroup Spokesperson": ["FirstGroup spokesperson", "FirstGroup spokesman", "FirstGroup spokeswoman", "spokesperson for FirstGroup", "spokesperson from FirstGroup", 
                        "spokesman for FirstGroup", "spokesman from FirstGroup", "spokeswoman for FirstGroup", "spokeswoman from FirstGroup",
                        "First Group spokesperson",  "First Group spokesman", "First Group spokeswoman", "spokesperson for First Group", "spokesperson from First Group", "FirstGroup said", "First Group said", 
                        "spokesman for First Group", "spokesman from First Group", "spokeswoman for First Group", "spokeswoman from First Group"],
                                        },
        "Stagecoach":                   {
                    "Fiona Doherty": ["Fiona Doherty"],
                    "Unnamed Stagecoach Spokesperson": ["Stagecoach spokesperson", "spokesperson for Stagecoach", "spokesperson from Stagecoach", "Stagecoach said",
                        "spokesman for Stagecoach", "spokesman from Stagecoach", "spokeswoman for Stagecoach", "spokeswoman from Stagecoach"],
                                        },
        "National Express":             {
                    "Unnamed National Express Spokesperson": ["National Express spokesperson", "spokesperson for National Express", "spokesperson from National Express", "National Express said",
                        "spokesman for National Express", "spokesman from National Express", "spokeswoman for National Express", "spokeswoman from National Express"],
                                        },
        "Go Ahead":                     {
                    "Martin Dean": ["Martin Dean"],
                    "Unnamed Go Ahead Spokesperson": ["Go Ahead spokesperson", "spokesperson for Go Ahead", "spokesperson from Go Ahead", "Go Ahead said",
                        "spokesman for Go Ahead", "spokesman from Go Ahead", "spokeswoman for Go Ahead", "spokeswoman from Go Ahead",
                        "Go-Ahead spokesperson",  "spokesperson for Go-Ahead", "spokesperson from Go-Ahead", "Go-Ahead said", 
                        "spokesman for Go-Ahead", "spokesman from Go-Ahead", "spokeswoman for Go-Ahead", "spokeswoman from Go-Ahead"],
                                        },
    },
    "Go Ahead": {
        
    },
    "KFC": {
        
    },
    "Lloyds Banking Group": {
        
    },
    "Lord Sugar": {
        "Lord Alan Sugar":                   {
                    "Lord Sugar": ["Lord Sugar", "Alan Sugar"],
                                        },
        "The Apprentice":                   {
                    "Lord Sugar": ["Lord Sugar", "Alan Sugar"],
                                        },
                                        
    },
    "Molson Coors": {

    },
    "NICE": {
        "NICE":                         {
                    "Alison Liddell": ["Alison Liddell"],
                    "Boryana Stambolova": ["Boryana Stambolova"],
                    "Cathy Stannard": ["Cathy Stannard"],
                    "Clare Morgan": ["Clare Morgan"],
                    "Cliodhna N Ghuidhir": ["Cliodhna N Ghuidhir", "Clíodhna Ní Ghuidhir"],
                    "Felix Greaves": ["Felix Greaves"],
                    "Sam Roberts": ["Sam Roberts"],
                    "Helen Knight": ["Helen Knight"],
                    "Jane Gizbert": ["Jane Gizbert"],
                    "Mark Chapman": ["Mark Chapman"],
                    "Jonathan Benger": ["Jonathan Benger"],
                    "Unnamed NICE Spokesperson": ["NICE spokesperson", "NICE said", "spokesperson for NICE", "spokesperson from NICE", 
                                        "spokesman for NICE", "spokesman from NICE", 
                                        "spokeswoman for NICE", "spokeswoman from NICE"],
                    "Paul Chrisp": ["Paul Chrisp"],
                    "Judith Richardson": ["Judith Richardson"],
                                        },
    },
    "The Post Office": {
        "The Post Office":              {
                    "Adam Shillcock": ["Adam Shillcock"],
                    "Allison Wallace": ["Allison Wallace"],
                    "Amanda Burton": ["Amanda Burton"],
                    "Angela Smith": ["Angela Smith"],
                    "Anna Thompson": ["Anna Thompson"],
                    "Anne Murphy": ["Anne Murphy"],
                    "Antoinette Chitty": ["Antoinette Chitty"],
                    "Barbara Brannon": ["Barbara Brannon"],
                    "Ben Foat": ["Ben Foat"],
                    "Billy Hughes": ["Billy Hughes"],
                    "Brian Turnbull": ["Brian Turnbull"],
                    "Carol Williams": ["Carol Williams"],
                    "Christopher Tarn": ["Christopher Tarn"],
                    "Damien Haydock": ["Damien Haydock"],
                    "Daniel Rooney": ["Daniel Rooney"],
                    "David Duff": ["David Duff"],
                    "Ed Dutton": ["Ed Dutton"],
                    "Elinor Hull": ["Elinor Hull"],
                    "Fiona Shanahan": ["Fiona Shanahan"],
                    "Gideon Hancock": ["Gideon Hancock"],
                    "Graham Brander": ["Graham Brander"],
                    "Greg Blackmore": ["Greg Blackmore"],
                    "Henry Staunton": ["Henry Staunton", "Harry Staunton"],
                    "Ian Johnson": ["Ian Johnson"],
                    "Ian Murphy": ["Ian Murphy"],
                    "Janese Sung": ["Janese Sung"],
                    "Jason Collins": ["Jason Collins"],
                    "Julie Thomas": ["Julie Thomas"],
                    "Kenny Lamont": ["Kenny Lamont"],
                    "Kevin Tomlin": ["Kevin Tomlin"],
                    "Kirsty Duncan": ["Kirsty Duncan"],
                    "Kulwant Dosanjh": ["Kulwant Dosanjh"],
                    "Laura Plunkett": ["Laura Plunkett"],
                    "Mark Cazaly": ["Mark Cazaly"],
                    "Mark Eldridge": ["Mark Eldridge"],
                    "Martin Kearsley": ["Martin Kearsley"],
                    "Martin Roberts": ["Martin Roberts"],
                    "Natalie Liff": ["Natalie Liff"],
                    "Neill O’Sullivan": ["Neill O’Sullivan", "Neill O'Sullivan"],
                    "Nick McCowan": ["Nick McCowan"],
                    "Nick Read": ["Nick Read"],
                    "Owen Woodley": ["Owen Woodley"],
                    "Paul Paddock": ["Paul Paddock"],
                    "Paul Spry": ["Paul Spry"],
                    "Rachel Bailey": ["Rachel Bailey"],
                    "Richard Clark": ["Richard Clark"],
                    "Ross Borkett": ["Ross Borkett"],
                    "Samuel Williams": ["Samuel Williams"],
                    "Scott Hamilton": ["Scott Hamilton"],
                    "Simon Recaldin": ["Simon Recaldin"],
                    "Spencer Garland": ["Spencer Garland"],
                    "Steven Simpson": ["Steven Simpson"],
                    "Thakoor Maraj": ["Thakoor Maraj"],
                    "Tig Khehra": ["Tig Khehra"],
                    "Tina Mellor": ["Tina Mellor"],
                    "Victoria Allsop": ["Victoria Allsop"],
                    "Wendy Hamilton": ["Wendy Hamilton"],
                    "Zoe Hall": ["Zoe Hall"],
                    "PO Spokesperson Unnamed or Org": ["Post Office spokesperson", "Post Office said", "spokesperson for the Post Office", "spokesperson from the Post Office", 
                                        "spokesman for the Post Office", "spokesman from the Post Office", 
                                        "spokeswoman for the Post Office", "spokeswoman from the Post Office"],
                                        },
    },
    "Royal Academy of Arts": {

    },
    "Santander": {
        "Santander":                    { # ensure brand matches exactly formatting in GI Banks metric
                    "Andrea Melville": 	["Andrea Melville"],
                    "Brad Fordham": 	["Brad Fordham", "Bradley Fordham"],
                    "Chris Ainsley": 	["Chris Ainsley"],
                    "Frances Haque": 	["Frances Haque"],
                    "Hetal Parmar": 	["Hetal Parmar"],
                    "John Carroll": 	["John Carroll"],
                    "Josie Clapham": 	["Josie Clapham"],
                    "Mark Ling": 	    ["Mark Ling"],
                    "Mike Regnier": 	["Mike Regnier"],
                                        },
        "Barclays":                     { # ensure brand matches exactly formatting in GI Banks metric
                    "Abbas Khan": 	["Abbas Khan"],
                    "Amit Goel": 	["Amit Goel"],
                    "Andrew Lobbenberg": 	["Andrew Lobbenberg"],
                    "Anna Cross": 	["Anna Cross"],
                    "CS Venkatakrishnan": 	["Venkatakrishnan"],
                    "Cathal Deasy": 	["Cathal Deasy"],
                    "Clare Francis": 	["Clare Francis"],
                    "David Bruce": 	["David Bruce"],
                    "Emily Field": 	["Emily Field"],
                    "Esme Harwood": 	["Esme Harwood"],
                    "Geoff Watson": 	["Geoff Watson"],
                    "Hannah Bernard": 	["Hannah Bernard"],
                    "Henk Potts": 	["Henk Potts"],
                    "Hiral Patel": 	["Hiral Patel"],
                    "Jamie Grant": 	["Jamie Grant"],
                    "Jo Mayer": 	["Jo Mayer"],
                    "Kirstie Mackey": 	["Kirstie Mackey"],
                    "Lianne Coupland": 	["Lianne Coupland"],
                    "Marc Pettican": 	["Marc Pettican"],
                    "Mark Cus Babic": 	["Mark Cus Babic", "Mark Cus-Babic"],
                    "Matt Hammerstein": 	["Matt Hammerstein"],
                    "Matt Thomas": 	["Matt Thomas"],
                    "Nick Stace": 	["Nick Stace"],
                    "Nigel Higgins": 	["Nigel Higgins"],
                    "Paul May": 	["Paul May"],
                    "Poonam Sharma": 	["Poonam Sharma"],
                    "Ross Martin": 	["Ross Martin"],
                    "Silvia Ardagna": 	["Silvia Ardagna"],
                    "Taylor Wright": 	["Taylor Wright"],
                    "Themos Fiotakis": 	["Themos Fiotakis"],
                    "Tom Corbett": 	["Tom Corbett"],
                    "William Hobbs": 	["William Hobbs"],
                                        },
        "HSBC":                         { # ensure brand matches exactly formatting in GI Banks metric
                    "Alistair Phil": 	["Alistair Phil"],
                    "Allan McGraw": 	["Allan McGraw"],
                    "Andrew Matson": 	["Andrew Matson"],
                    "Annabel Spring": 	["Annabel Spring"],
                    "Cameron Senior": 	["Cameron Senior"],
                    "Celine Herweijer": 	["Celine Herweijer"],
                    "Charlotte Faulkner": 	["Charlotte Faulkner"],
                    "Chris Hare": 	["Chris Hare"],
                    "Dominic Bunning": 	["Dominic Bunning"],
                    "Elizabeth Martins": 	["Elizabeth Martins"],
                    "Erin Platts": 	["Erin Platts"],
                    "Georges Elhedery": 	["Georges Elhedery"],
                    "Georgios Leontaris": 	["Georgios Leontaris"],
                    "Gina Bartlett": 	["Gina Bartlett"],
                    "Helen Durrant": 	["Helen Durrant"],
                    "Hussain Mehdi": 	["Hussain Mehdi"],
                    "Ian Coulson": 	["Ian Coulson"],
                    "Ian Stuart": 	["Ian Stuart"],
                    "Jackie Uhi": 	["Jackie Uhi"],
                    "James Shepherd": 	["James Shepherd"],
                    "John Hinshaw": 	["John Hinshaw"],
                    "Jose Carvalho": 	["Jose Carvalho"],
                    "Joseph Little": 	["Joseph Little"],
                    "Lisa Moore": 	["Lisa Moore"],
                    "Liz Martins": 	["Liz Martins"],
                    "Matthew Cooper": 	["Matthew Cooper"],
                    "Maxine Pritchard": 	["Maxine Pritchard"],
                    "Michael Farr": 	["Michael Farr"],
                    "Noel Quinn": 	["Noel Quinn"],
                    "Pella Frost": 	["Pella Frost"],
                    "Peter McIntyre": 	["Peter McIntyre"],
                    "Simon Woods": 	["Simon Woods"],
                    "Sir Sherard Cowper-Coles": 	["Sherard Cowper Coles", "Sherard Cowper-Coles"],
                    "Stephen Bramley-Jackson": 	["Stephen Bramley Jackson", "Stephen Bramley-Jackson"],
                    "Stuart McLaren": 	["Stuart McLaren"],
                    "Stuart Tait": 	["Stuart Tait"],
                                        },
        "Lloyds":                       { # ensure brand matches exactly formatting in GI Banks metric
                    "Aled Patchett": 	["Aled Patchett"],
                    "Amanda Dorel": 	["Amanda Dorel"],
                    "Andrew Asaam": 	["Andrew Asaam"],
                    "Andy Bickers": 	["Andy Bickers"],
                    "Annabel Finlay": 	["Annabel Finlay"],
                    "Becci Wicks": 	["Becci Wicks"],
                    "Charlie Nunn": 	["Charlie Nunn"],
                    "Chris Lawrie": 	["Chris Lawrie"],
                    "Claire Carr": 	["Claire Carr"],
                    "Craig Smith": 	["Craig Smith"],
                    "Dave Atkinson": 	["Dave Atkinson"],
                    "Dene Jones": 	["Dene Jones"],
                    "Elyn Corfield": 	["Elyn Corfield"],
                    "Hann-Ju Ho": 	["Hann-Ju Ho"],
                    "Jackie Leiper": 	["Jackie Leiper"],
                    "Jayne Williams": 	["Jayne Williams"],
                    "Jo Harris": 	["Jo Harris"],
                    "Kim Kinnaird": 	["Kim Kinnaird"],
                    "Lisa Francis": 	["Lisa Francis"],
                    "Liz Ziegler": 	["Liz Ziegler"],
                    "Manuel Pardavila-Gonzalez": 	["Manuel Pardavila Gonzalez", "Manuel Pardavila-Gonzalez"],
                    "Nikesh Sawjani": 	["Nikesh Sawjani"],
                    "Paul Gordon": 	["Paul Gordon"],
                    "Rhys Herbert": 	["Rhys Herbert"],
                    "Rob Taylor": 	["Rob Taylor"],
                    "Sam Noble": 	["Sam Noble"],
                    "Scott Barton": 	["Scott Barton"],
                    "Sharon Doherty": 	["Sharon Doherty"],
                    "Steve Harris": 	["Steve Harris"],
                    "Steven Knight": 	["Steven Knight"],
                    "Tim Downes": 	["Tim Downes"],
                    "Vijay Chouhan": 	["Vijay Chouhan"],
                    "William Chalmers": 	["William Chalmers"],
                                        },
        "RBS NatWest":                  { # ensure brand matches exactly formatting in GI Banks metric
                    "Alison Rose": 	["Alison Rose"],
                    "Caroline Haas": 	["Caroline Haas"],
                    "Catherine Van Weenen": 	["Catherine Van Weenen"],
                    "Claire Melling": 	["Claire Melling"],
                    "Elly Rowley": 	["Elly Rowley"],
                    "Gemma Casey": 	["Gemma Casey"],
                    "Howard Davies": 	["Howard Davies"],
                    "Imogen Bachra": 	["Imogen Bachra"],
                    "Jaimala Patel": 	["Jaimala Patel"],
                    "James Holian": 	["James Holian"],
                    "Joann Spadigam": 	["Joann Spadigam"],
                    "Judith Cruickshank": 	["Judith Cruickshank"],
                    "Katie Murray": 	["Katie Murray"],
                    "Keith Linklater": 	["Keith Linklater"],
                    "Kenny Robertson": 	["Kenny Robertson"],
                    "Kevin Morgan": 	["Kevin Morgan"],
                    "Lewis Broadie": 	["Lewis Broadie"],
                    "Malcolm Buchanan": 	["Malcolm Buchanan"],
                    "Mark Seligman": 	["Mark Seligman"],
                    "Paul Edwards": 	["Paul Edwards"],
                    "Paul Thwaite": 	["Paul Thwaite"],
                    "Peter Flavel": 	["Peter Flavel"],
                    "Phil Sheehy": 	["Phil Sheehy"],
                    "Rashel Chowdhury": 	["Rashel Chowdhury"],
                    "Ross Walker": 	["Ross Walker"],
                    "Sebastian Burnside": 	["Sebastian Burnside"],
                    "Stuart Skinner": 	["Stuart Skinner"],
                                        },
    },
    "Scottish Water": {

    },
    "Shell": {
    }, 

    "Three": {

    },
    "Walgreens Boots Alliance": {

    },
    "Zoological Society of London": {

    },
}

# SA_cols - columns to remove from SA data and replace with combined GI/AI analysis (usually all coded metrics)
# GI_cols - should include any required metadata and analysed columns from GI (analysed columns taken if quality sufficient to use in analysis, others will be passed to AI), 
#     as well as the Response column containing AI response if required (will be used in background either way)
# brand_metrics - used for building a table from the GPT response after client articles have been sent to GPT for analysis
#     should match exactly the metrics in the prompt in prompts.py
# brand_metrics_SA - this dict is used for inserting analysed metrics from the table containing GPT analysis into a Score App formatted worksheet
#     order should match the order of metrics that appear in current SA setup, with any additional metrics added on end
#     I believe (need to re-run tests to confirm) additional metrics can come from both GI and AI responses, 
#     and should be included in GI_cols or brand_metrics so that they are available for brand_metrics_SA
# brands_bool - whether the Brands_Bool column containing brand mentions is created in Python or copied from a column in GI
# only a small number of brands added and tested yet

dict_brand_metrics_cols = {
    "FirstGroup":   {'SA_cols': ['PRI', 'Sentiment', 'Prominence', 'Spokespeople', 'Third Party Spokesperson', 'Key Stories', 'Competitor Company', 'Competitor Sentiment'],
                     'GI_cols': ['Local Article Id', 'Url', 'Headline', 'Full Text', 'Brands_Bool', 'Response'],
                     'brand_metrics': ['Mention_YN',  
                                'Sentiment', 'Sentiment_explanation', 'Passing_mention',
                                'Brand_Spokespeople', 'PRI', 'Third_party_spokespeople',
                                'Key_stories'
                                ],
                     'brand_metrics_SA': ['Local Article Id', 'Response', 'Brand', 'PRI', 'Sentiment', 'Prominence', 'Spokespeople', 'Third_party_spokespeople', 'Key_stories', 'Brand', 'Sentiment',
                                'Sentiment_explanation', 'Brand_Spokespeople', 'Full Text', 'Mention_YN'],
                     'brands_bool': 'run'
                    },
    "Lord Sugar":   {'SA_cols': ['SENTIMENT', 'PROMINENCE', 'PRI', 'TOPIC', 'STORY'],
                     'GI_cols': ['Local Article Id', 'Url', 'Headline', 'Full Text', 'Brands_Bool', 'Response', 'Topics'],
                     'brand_metrics': ['Mention_YN', 
                                'Sentiment', 'Passing_mention', 'PRI', 'Story', 'Sentiment_explanation'
                                ],
                     'brand_metrics_SA': ['Local Article Id', 'Brand', 'Response', 'Sentiment', 'Prominence', 'PRI', 'Spokespeople', 'Topics', 'Story', 'Sentiment_explanation'],
                     'brands_bool': 'Topics'
                    },
    "NICE":         {'SA_cols': ['INDUSTRY PEER', 'SENTIMENT', 'PROMINENCE', 'PRI', 'PRESS RELEASE', 'CALL TO ACTION', 'IMAGE', 'KEY MESSAGES', 'SPOKESPERSON', 'TOPIC', 'STORY'], # From June sheet
                     'GI_cols': ['Local Article Id', 'Url', 'Headline', 'Full Text', 'Brands_Bool', 'Spokespeople', 'Response'],
                     'brand_metrics': ['Mention_YN', 'Author', 'Sentiment', 'Sentiment_explanation', 'Passing_mention', 
                                'Topics', 'Key_messages', 'NICE_Spokespeople', 'Press_release', 'PRI', 'Media_type', 'Story'
                                ],
                     'brand_metrics_SA': ['Local Article Id', 'Response', 'Sentiment', 'Prominence', 'PRI', 'Story', 'Press_release', 'Media_type', 'Key_messages', 'Spokespeople', # NB 'Spokespeople' is scripted
                                'Sentiment_explanation', 'Topics', 'Author', 'NICE_Spokespeople'], # 'NICE_Spokespeople' is analysed by GPT
                     'brands_bool': 'run'
                    },
    "The Post Office":  {'SA_cols': ['Best Buy (Yes/No)', 'Prominence', 'Sentiment', 'Products and Services', 'Products and Services sub-categories', 'Post Office Spokespeople', 
                                '3rd Party & Competitor Spokespeople', 'Theme', 'Story', 'Call to Action', 'General Key Messages', 'Postmaster Key Messages', 
                                'Banking Access to Cash Key Messages', 'Financial Services Key Messages', 'Mails Key Messages', 'Travel Key Messages', 'Payzone Key Messages', 
                                'Strategy Key Messages', 'Branch Openings Closing Relocation Key Messages', 'Identity Services Key Messages', 'Horizon Inquiry Key Messages', 
                                'PRI', 'Press Release (title)', 'Region', 'Competitor', 'Sentiment (Competitor)', 'Reputation Attribute', 'Postmaster Scheme Mentioned', 
                                'Best buy tables', 'Postmaster Mention', 'Branch Openings/Closing'
                                ],
                     'GI_cols': ['Local Article Id', 'Url', 'Headline', 'Full Text', 'Brands_Bool', 'Response'],
                     'brand_metrics': ['Best_buy_YN', 'Passing_mention', 'Sentiment', 'Products_and_Services', 'Products_and_Services_SubCategory', 'Spokespeople_Post_Office', 
                                'Third_Party_Spokespeople', 'Themes', 'Story', 'Call_to_action', 'General_key_messages', 'Postmaster_key_messages', 'Banking_key_messages', 
                                'Financial_services_key_messages', 'Mails_key_messages', 'Travel_key_messages', 'Payzone_key_messages', 'Strategy_key_messages', 
                                'Branch_key_messages', 'Identity_services_key_messages', 'Horizon_inquiry_key_messages', 'PRI', 'Press_release', 'Region', 'Competitor', 
                                'Competitor_sentiment', 'Reputation_attribute', 'Postmaster_Scheme_mention', 'Best_buy_type', 'Postmaster_mention', 'Branch_opening_closing', 
                                'Mention_YN', 'Sentiment_explanation', 'Passing_mention'
                                ],
                     'brand_metrics_SA': ['Local Article Id', 'Headline', 'Full Text', 'Response', 'Best_buy_YN', 'Prominence', 'Sentiment', 'Products_and_Services', 'Products_and_Services_SubCategory', 
                                'Spokespeople_Post_Office', 'Third_Party_Spokespeople', 'Themes', 'Story', 'Call_to_action', 'General_key_messages', 'Postmaster_key_messages', 
                                'Banking_key_messages', 'Financial_services_key_messages', 'Mails_key_messages', 'Travel_key_messages', 'Payzone_key_messages', 'Strategy_key_messages', 
                                'Branch_key_messages', 'Identity_services_key_messages', 'Horizon_inquiry_key_messages', 'PRI', 'Press_release', 'Region', 'Competitor', 
                                'Competitor_sentiment', 'Reputation_attribute', 'Postmaster_Scheme_mention', 'Best_buy_type', 'Postmaster_mention', 'Branch_opening_closing', 
                                'Mention_YN', 'Sentiment_explanation', 'Passing_mention', 'Spokespeople'],
                     'brands_bool': 'run'
                    },
    "Santander":    {'SA_cols': ['Sentiment', 'Prominence', 'Article type', 'Focus', 'Spokespeople', 'Supportive Third Party Spokespeople', 'Critical Third Party Spokespeople', 
                                 'Positive messages', 'Negative messages', 'Story', 'Santander Topic'
                                ],
                     'GI_cols': ['Local Article Id', 'Url', 'Headline', 'Full Text', 'Brands_Bool', 'Prompt', 'Response', 'Banks'],
                     'brand_metrics': ['Mention_YN', 'Passing_mention', 'Sentiment', 'Sentiment_explanation', 'Article_type', 'Brand_spokesperson', 
                                       'Third_party_supportive', 'Third_party_critical', 'Messages_positive', 'Messages_negative', 'Story', 'Topic'],
                     'brand_metrics_SA': ['Local Article Id', 'Headline', 'Full Text', 'Prompt', 'Response', 'Banks', 'Brand', 'Mention_YN', 'Prominence', 
                                          'Sentiment', 'Sentiment_explanation', 'Article_type', 'Brand_spokesperson', 'Third_party_supportive', 'Third_party_critical', 
                                          'Messages_positive', 'Messages_negative', 'Story', 'Topic', 'Spokespeople'],
                     'brands_bool': 'Banks'
                    },
    "Three":        {'SA_cols': [], 
                     'GI_cols': ['Local Article Id', 'Url', 'Headline', 'Full Text', 'Brands_Bool', 'Spokespeople', 'Response'],
                     'brand_metrics': ['Mention_YN', 
                                'Corporate_Consumer', 'Sentiment', 'Sentiment_explanation', 'Passing_mention', 'Topics', 
                                'Spokespeople', 'Positive_Brand_Values', 'Negative_Brand_Values', 
                                'Story'
                                ],
                     'brand_metrics_SA': [],
                     'brands_bool': 'run'
                    },              
}






# NB ALL DICTS BELOW ARE CURRENTLY OUT OF USE
# BUT MANY CONTAIN DATA THAT SHOULD BE INSERTED INTO dict_brand_metrics_cols DIRECTLY ABOVE

# NOT CURRENTLY IN USE - replaced by dict_brand_brands_2
# used by Python to identify relevant brands before passing articles to GPT for analysis
# group name variations into a sublist, e.g. ['Lloyds Banking Group', 'Lloyds Bank', 'LBG']
# the leftmost value present in the item will be analysed, e.g. 'Lloyds Banking Group' if all three present, or 'LBG' if only this value present
# currently in testing, investigating whether this works, and whether the more formal, or more used, variation works better in each case
dict_brand_brands = {
    'ASOS':                 [['ASOS']]
                            ,
    'BDO Ireland':          [['BDO']]
                            ,
    'Diabetes UK':          [['Diabetes UK']]
                            ,
    'Disney':               [['Disney']]
                            ,
    'Failte Ireland':       [['Failte Ireland'], 
                            ['Tourism Ireland'], 
                            ['Irish Hotels Federation'], 
                            ['Irish Tourism Industry Confederation'], 
                            ['Restaurants Association of Ireland'],
                            ['Catherine Martin'], 
                            ['Jack Chambers']]
                            ,
    'Federation of Small Businesses': [['Federation of Small Businesses', 'FSB']]
                            ,
    'FirstGroup':          [['FirstGroup', 'First Group'],
                            ['Stagecoach'],
                            ['National Express'],
                            ['Go Ahead']]
                            ,
    'Go Ahead':             [['Go Ahead'],
                            ['Abellio'],
                            ['Arriva'],
                            ['Stagecoach'],
                            ['National Express'],
                            ['Go Ahead']]
                            ,
    'KFC':                  [['KFC'], 
                            ['Burger King'], 
                            ['Deliveroo'], 
                            ['Greggs'], 
                            ["McDonald's"], 
                            ['Pizza Hut'], 
                            ['Uber Eats']]
                            ,
    'Lloyds Banking Group': [['Lloyds Banking Group', 'Lloyds Bank', 'Lloyds', 'LBG'], 
                             ['Halifax'], 
                             ['Bank of Scotland'], 
                             ['MBNA'], 
                             ['Birmingham Midshires'], 
                             ['Lex auto lease'], 
                             ['Black Horse'], 
                             ['Tusker'],
                                ['Barclays'], 
                                ['HSBC'], 
                                ['Nationwide'], 
                                ['NatWest'], 
                                ['RBS'], 
                                ['Santander'], 
                                ['TSB'], 
                                ['Monzo'], 
                                ['Starling'], 
                                ['Paypal'], 
                                ['Revolut'], 
                                ['Metro'], 
                                ['First Direct']]
                            ,
    'Lord Sugar':           [['Lord Sugar', 'Alan Sugar'],
                             ['The Apprentice']]
                            ,
    'Molson Coors':         [['Molson', 'Molson Coors'],
                            ['AB InBev'],
                            ['Asahi'],
                            ['Carlsberg'],
                            ['Diageo'],
                            ['Heineken']]
                            ,
    'NICE':                 [['NICE', 'National Institute for Health and Care Excellence']]
                            ,
    'Royal Academy of Arts':[['RAA', 'Royal Academy of Arts']]
                            ,
    'Scottish Water':       [['Scottish Water']]
                            ,
    'Shell':                [['Shell']]
                            , # plus competitors?
    'Three':                [['Three'], 
                            ['BT Mobile'], 
                            ['Carphone Warehouse', 'Dixons Carphone'], 
                            ['EE'], 
                            ['O2'], 
                            ['Sky Mobile'], 
                            ['Smarty'], 
                            ['Tesco Mobile'], 
                            ['Virgin Mobile'], 
                            ['Vodafone'], 
                            ['VOXI', 'Voxi']]
                            ,
    'Zoological Society of London': [['Zoological Society of London', 'London Zoological Society', 'ZSL']]
}

# columns to remove from SA data and replace with coded analysis
dict_brand_SA_cols = {
    "ASOS": [],
    "BDO Ireland": [],
    "Diabetes UK": [],
    "Disney": [],
    "Failte Ireland": [],
    "Federation of Small Businesses": [],
    "FirstGroup": ['PRI', 'Sentiment', 'Prominence', 'Spokespeople', 'Third Party Spokesperson', 'Key Stories', 'Competitor Company', 'Competitor Sentiment'],
    "Go Ahead": [],
    "KFC": [],
    "Lloyds Banking Group": [],
    "Lord Sugar": ['SENTIMENT', 'PROMINENCE', 'PRI', 'TOPIC', 'STORY'],
    "Molson Coors": [],
    # "NICE": ['Sentiment', 'Prominence', 'PRI', 'Story', 'Press Release', 'Type of Media', 'Key Messages', 'NICE Spokespeople'], # From July/Aug sheet
    "NICE": ['INDUSTRY PEER', 'SENTIMENT', 'PROMINENCE', 'PRI', 'PRESS RELEASE', 'CALL TO ACTION', 'IMAGE', 'KEY MESSAGES', 'SPOKESPERSON', 'TOPIC', 'STORY'], # From June sheet
    "Royal Academy of Arts": [],
    "Scottish Water": [],
    "Shell": [], 
    "Three": [],
    "Walgreens Boots Alliance": [],
    "Zoological Society of London": [],
}

# columns to take from GI prior to analysis
dict_brand_GI_cols = {
    "ASOS": [],
    "BDO Ireland": [],
    "Diabetes UK": [],
    "Disney": [],
    "Failte Ireland": [],
    "Federation of Small Businesses": [],
    "FirstGroup": ['Local Article Id', 'Url', 'Headline', 'Full Text', 'Brands_Bool', 'Spokespeople', 'Response'],
    "Go Ahead": [],
    "KFC": [],
    "Lloyds Banking Group": [],
    "Lord Sugar": ['Local Article Id', 'Url', 'Headline', 'Full Text', 'Brands_Bool', 'Spokespeople', 'Response', 'Topics'],
    "Molson Coors": [],
    "NICE": ['Local Article Id', 'Url', 'Headline', 'Full Text', 'Brands_Bool', 'Spokespeople', 'Response'], # From June sheet
    "Royal Academy of Arts": [],
    "Scottish Water": [],
    "Shell": [], 
    "Three": ['Local Article Id', 'Url', 'Headline', 'Full Text', 'Brands_Bool', 'Spokespeople', 'Response'],
    "Walgreens Boots Alliance": [],
    "Zoological Society of London": [],
}

# used for building a table from the GPT response after client articles have been sent to GPT for analysis
# should match exactly the metrics in the prompt in prompts.py
dict_brand_metrics = {
    'ASOS': ["Mention_YN", 
            "Sentiment", "Sentiment_explanation", "Prominence", "Media_Tier",
            "Positive_reputational_pillars", "Negative_reputational_pillars",
            "ASOS_spokespeople", "Third_party_spokespeople",
            "Topics", "Story"
            ],
    'BDO Ireland': ["Mention_YN", 
            "Sentiment", "Sentiment_explanation", "Prominence", 
            "PRI", "Story"
            ],
    'Diabetes UK': ['Mention_YN',
            'Sentiment', 'Sentiment_explanation', 'Passing_mention', 'Key_category', 
            'Campaigns_Diabetes_UK', 'Campaigns_Care', 'Campaigns_Diabetes_is_serious', 'Campaigns_Fundraising', 
            'Campaigns_Healthy_Lifestyle', 'Campaigns_Research', 'Campaigns_Volunteer', 'Campaigns_World_Diabetes_Day', 'Campaigns_Tesco_Partnership', 'Campaigns_Services', 
            'Spokespeople', 'Press_release', 'PRI', 'Contact_details', 'Tesco_mention',
            'Reporting_month', 'Custom_media_type', 'Region', 'Story'
            ],  
    'Disney': ['Mention_YN', 'Corporate_Consumer',
          'Sentiment', 'Sentiment_explanation', 'Prominence', 'Topics', 'Spokespeople', 'Positive_Brand_Values', 'Negative_Brand_Values', 'Story'
            ],
    'Failte Ireland': ["Mention_YN", 
            "Influence", "Influence_explanation", "Campaign",
            "Publication_type", "Article_type",
            "Story"
            ],
    'Federation of Small Businesses': ['Mention_YN',  
            'Sentiment', 'Sentiment_explanation', 'Prominence', 'Article_type', 
            'Spokespeople', 'Press_release', 'PRI', 'Third_party_spokespeople',
            'Region', 'Topic',
            'Story'
            ],
    'FirstGroup': ['Mention_YN',  
            'Sentiment', 'Sentiment_explanation', 'Passing_mention',
            'Brand_Spokespeople', 'PRI', 'Third_party_spokespeople',
            'Key_stories'
            ],
    'Go Ahead': ['Mention_YN',  
            'Sentiment', 'Sentiment_explanation', 'Prominence', 
            'Topic', 'Key_messages', 'PRI', 'PRI_explanation', 
            'Story'
            ],
    'KFC': ['Mention_YN', 'Author', 
            'Sentiment', 'Sentiment_explanation', 'Prominence',
            'Article_type', 'Image', 'Press_release', 'Products',
            'Positive_anxieties', 'Negative_anxieties', 'Spokespeople', 'Third_party_spokespeople',
            'Media_type', 'Media_format', 'Campaign', 'Topics',
            'Story'
            ],  
    'Lloyds Banking Group': ['Mention_YN', 'Author', 
            'Business_division', 'Product_type', 'Service_type', 'Coverage_type', 
            'Sentiment', 'Sentiment_explanation', 'Group_sentiment', 'Group_sentiment_explanation', 'Prominence', 'Topics', 
            'Positive_reputation_drivers', 'Negative_reputation_drivers', 'Pos_bal_priority_rep_themes', 'Neg_priority_rep_themes', 
            'LBG_spokespeople', 'PRI', 'Competitor_spokespeople', 'Third_party_spokespeople', 
            'Press_release', 'Press_release_type', 'Helping_Britain_Recover',
            'Branch_closure', 'Name_of_branch_closure',
            'Story'
            ],
    'Lord Sugar': ['Mention_YN', 
            'Sentiment', 'Passing_mention', 'PRI', 'Story', 'Sentiment_explanation'
            ],
    'Molson Coors': ['Mention_YN',  
            'Sentiment', 'Sentiment_explanation', 'Brand_attributes'
            'Story'
            ],
    'NICE': ['Mention_YN', 'Author', 'Sentiment', 'Sentiment_explanation', 'Passing_mention', 
            'Topics', 'Key_messages', 'NICE_Spokespeople', 'Press_release', 'PRI', 'Media_type', 'Story'
            ], 
    'Royal Academy of Arts': ['Mention_YN', 
            'Sentiment', 'Sentiment_explanation', 
            'Coverage_drivers', 'RAA_spokespeople', 'Key_messages', 
            'Campaigns_exhibitions', 'Call_to_action', 'PRI'
            'Story'
            ], 
    'Scottish Water': ['Mention_YN',  
            'Key_topics', 'Sentiment', 'Sentiment_explanation', 'Prominence'
            'Press_release', 'Campaign', 'Nature_Calls_key_messages', 'Your_Water_Your_Life_key_messages', 'Learn_to_Swim_key_messages',
            'Scottish_Water_spokespeople', 'PRI', 
            'Third_party_spokespeople', 'Images_and_logos', 'Media_tier',
            'Story'
            ],
    'Shell': ['Published_region', 'Publication_origin', 'Language', 'Journalist', 'Original_source', 
            'Organisation', 'Sentiment_towards_organisation', 'Sent_exp', 'Secondary_sentiment', 'Prominence', 'Significance', 
            'Business_area', 'Corporate_drivers', 'Primary_theme', 'Secondary_theme', 'Societal_issues', 'Reputation_attributes_positive', 'Reputation_attributes_negative',
            'Energy_source', 'Regions_mentioned', 'Story_origin', 'CEO_mention', 'Sentiment_towards_CEO', 'Organisation_spokespeople', 'PR_influenced', 'PRI_exp', 
            'Shell_projects_and_assets', 'Story'
            ],
    'Three': ['Mention_YN', 
            'Corporate_Consumer', 'Sentiment', 'Sentiment_explanation', 'Passing_mention', 'Topics', 
            'Spokespeople', 'Positive_Brand_Values', 'Negative_Brand_Values', 
            'Story'
            ],
    'Walgreens Boots Alliance': ['Mention_YN', 
            'Sentiment', 'Sentiment_explanation', 'Passing_mention', 'Topics', 
            'WBA_Spokespeople', '3rd_P_Supportive', '3rd_P_Neutral', '3rd_P_Critical', 
            'Story'
            ],
    'Zoological Society of London': ['Mention_YN', 
          'Sentiment', 'Sentiment_explanation', 'Prominence', 
          'Division', 'Key_messages', 'Spokespeople', 
          'Call_to_action', 'Press_release', 'Event', 
          'Story'
            ],
}

# this dict is used for inserting analysed metrics from GPT into a Score App formatted worksheet
# order should match the order of metrics that appear in current SA setup, with any additional added on end
# only a small number of brands added and tested yet
dict_brand_metrics_SA = {
    'ASOS': [],
    'BDO Ireland': [],
    'Diabetes UK': [],  
    'Disney': [],
    'Failte Ireland': [],
    'Federation of Small Businesses': [],
    'FirstGroup': ['Local Article Id', 'Response', 'PRI', 'Sentiment', 'Prominence', 'Spokespeople', 'Third_party_spokespeople', 'Key_stories', 'Brand', 'Sentiment',
                    'Sentiment_explanation', 'Brand_Spokespeople'],
    'Go Ahead': [],
    'KFC': [],  
    'Lloyds Banking Group': [],
    'Lord Sugar': ['Local Article Id', 'Sentiment', 'Prominence', 'PRI', 'Spokespeople', 'Topics', 'Story', 'Sentiment_explanation'],
    'Molson Coors': [],
    'NICE': ['Local Article Id', 'Response', 'Sentiment', 'Prominence', 'PRI', 'Story', 'Press_release', 'Media_type', 'Key_messages', 'Spokespeople', # NB 'Spokespeople' is scripted
             'Sentiment_explanation', 'Topics', 'Author', 'NICE_Spokespeople'], # 'NICE_Spokespeople' is analysed by GPT
    'Royal Academy of Arts': [], 
    'Scottish Water': [],
    'Shell': [],
    'Three': [],
    'Walgreens Boots Alliance': [],
    'Zoological Society of London': [],
}




# used in prompt_tester.py. not required for app.py when running properly from front end
dict_brand_source = {
    'Diabetes UK': 'RSS',
    'Disney': 'Excel',
    'KFC': 'Excel',
    'Lloyds Banking Group': 'Excel',
    'Lord Sugar': 'RSS',
    'NICE': 'RSS',
    'Shell': 'Excel',
    'Three': 'Excel'
}

# only required for brands where data sourced from RSS. not required for app.py when running properly from front end IF URL is provided by user (not decided yet)
dict_brand_RSS_url = {
    'Diabetes UK':  "https://cdn.reputation.onclusive.com/Rss.aspx?crypt=52D43006FB86659B1CA9A44136BBC341E251FD5DAF03FB1895AE942C463079B9",
    'Lord Sugar':   "https://cdn.reputation.onclusive.com/Rss.aspx?crypt=BE63E81F6396EA52E01B3371BF69D8CAA13879C82BD5D371F277D648ACE49078",
    'NICE':         "https://cdn.reputation.onclusive.com/Rss.aspx?crypt=95A6F836CBEBBEF7B8EF38B2A6F2F766C70691E59263C63775398BB134333E69",
}

# used for testing through prompt_tester.py only. not required for front end analysis
dict_brand_file = {
    # 'NICE': os.path.join('Data_Raw', 'NICE', 'Data_NICE.xlsx'),           # moved to RSS
    'Lloyds Banking Group': os.path.join('Data_Raw', 'LBG', 'Data_LBG.xlsx'),
    # 'Lord Sugar': 'NA',                                                   # Included for reference. Uses RSS feed rather than Excel. 
    'KFC': os.path.join('Data_Raw', 'KFC', 'Data_KFC.xlsx'),
    'Shell': os.path.join('Data_Raw', 'Shell', 'Data_Shell.xlsx')
}

# dict not currently in use
# all analysis at front end currently through eval_prompt_general, with metrics dynamically inserted for each client
# (this is determined through the get_metrics function in the file prompts.py, the dict_brand_metrics dict below is used for building a table from the GPT response)
dict_brand_prompt = {
    'Diabetes UK': eval_prompt_Diabetes_UK,
    'Disney': eval_prompt_general,
    'KFC': eval_prompt_KFC,
    'Lloyds Banking Group': eval_prompt_LBG,
    'Lord Sugar': eval_prompt_Lord_Sugar,
    'NICE': eval_prompt_NICE,
    'Shell': eval_prompt_Shell,
    'Three': eval_prompt_general,
}
