
# Define a single prompt that takes metrics for each client dynamically
# This allows instructions to be kept constant and updated for all brands at once, but with different metrics for each client
# client = name of client (each client returns an analysis for at least itself, and competitor brands if required)
# df_brands_sample = a df which has been filtered to include only articles with Full Text and a relevant brand
#     containing articles selected from a sample, which can be random n, latest n, specific IDs or All

def eval_prompt_general (client, df_brands_sample, dict_brand_brands_2, i, language):
          
          # Start by creating a string that advises the AI on any name variations to look out for while analysing the article
          
          # 1 Set an empty string to hold brand name variations
          variations_prompt = ""
          
          # 2 Get the list of brands from the article (can be client and/or competitors)
          client_brands = df_brands_sample.iloc[i]['Brands_Bool']

          # 3 Get the sub-dictionary corresponding to the client
          client_dict = dict_brand_brands_2.get(client, {})

          # 4 Split the brands and check if any have variations
          for brand in client_brands.split('|'):

               # Retrieve variations from the sub-dictionary using the brand
               variations = client_dict.get(brand, [])
               
               # Check if there are variations (more than one entry in the list)
               if variations and len(variations) > 1:  # Check if there are variations
                    variations_prompt += f"{brand} may be referred to as any of the following: {', '.join(variations)}.\n"

          # 5 ONLY if any variations present
          # Add those lines created above and one preceding line to variations_prompt (otherwise leave it as an empty string)
          if variations_prompt:
               variations_prompt = ("Please note that the brands below may appear as name variations, and this should be taken into account when analysing an article.\n" 
                                   + variations_prompt)
          
          # Create the prompt from multiple parts (for readability)
          # These are concatenated before returning to full prompt to send to the AI for analysis

          prompt_arguments = (
          f"The following list is called brand_list: {df_brands_sample.iloc[i]['Brands_Bool']}.\n"
          "It contains either a single brand or multiple brands (if multiple, each brand will be separated by a |)\n\n "
          "The following represents the headline and full text of a news article: \n"
          "Headline: \n"
          f"{df_brands_sample.iloc[i]['Headline']}\n"
          "Article text: \n"
          f"{df_brands_sample.iloc[i]['Full Text']}\n"
          )

          prompt_instructions = (
          "Could you please analyse the headline and article, and provide in response a single JSON object.\n"
          "Please DO NOT include any additional commentary outside of the single JSON object.\n"
          "The JSON object should be formatted so that each brand in brand_list appears on the top level, with their respective attributes nested one level deeper.\n"
          "If only one value is returned, e.g. for Sentiment, it should be returned as a string.\n"
          "If multiple values are returned, e.g. for Brand Values, they should be returned as an array.\n"
          "If a brand is not mentioned, only Mention_YN should be filled. The remaining metrics should be simply 'NA'.\n"
          )

          prompt_brands_and_metrics = (
          # Add variations_prompt note on brand name variations IF at least one brand requires name variations (will be blank string if not)
          f"{variations_prompt}"

          "The attributes for each brand should be as follows:\n\n"
          f"{get_metrics(client, language)}"
          )
          
          prompt_end_notes = (
          "IMPORTANT NOTE: All metrics MUST be returned for all brands. DO NOT combine, reorder or omit metrics.\n"
          "IMPORTANT NOTE: All brands on the top level of the JSON object returned should appear verbatim as they appear in brand_list, even if the name appears slightly differently in the article.\n"
          "IMPORTANT NOTE: Sentiment should always record the sentiment of the article TOWARDS THE BRAND. It does NOT reflect the general sentiment of the article.\n"
          "IMPORTANT NOTE: Avoid assigning values that are unsupported by the text. Some mentions will be very brief, and this is normal. Do not overcompensate be looking for values that are not there."
          )

          prompt = prompt_arguments + prompt_instructions + prompt_brands_and_metrics + prompt_end_notes

          return prompt


# Used only for single article analysis (second column, front end web page)
# Note that this is a single string. Other prompts are mostly (likely all) functions, and take dynamic elements

eval_prompt_single = ("Could you please analyse the headline and article, and provide in response a single JSON object.\n"
    "Please DO NOT include any additional commentary outside of the single JSON object.\n"
    "The JSON object should be formatted so that each brand in brand_list appears on the top level, with their respective attributes nested one level deeper.\n"
    "If only one value is returned, e.g. for Sentiment, it should be returned as a string.\n"
    "If multiple values are returned, e.g. for Brand Values, they should be returned as an array.\n"
    "If a brand is not mentioned, only Mention_YN should be filled. The remaining metrics should be simply 'NA'.\n"
    "The attributes for each brand should be as follows:\n\n"

    "Mention_YN: ['Mentioned in article', 'No mention'] Whether the brand was mentioned in the article\n"
    "Corporate_Consumer: ['Corporate', 'Consumer'] Whether the theme of the mention is Consumer or Corporate. Pick best fit, use ONLY one of these two values.⌈\n"
    "Sentiment: ['Positive', 'Neutral', 'Negative']\n"
    "Sentiment_explanation: The reason for your choice of sentiment\n"
    "Passing_mention: ['Yes', 'No'] Is the mention of the brand entirely in passing and unlikely to affect its reputation?\n"
                    "Examples of a Passing Mention include: brief mention of the brand in a list of other brands, mentions of the brand using phrases like '...such as [brand]'.\n"
    "Topics: ['Financial Performance', 'Regulation', 'Product Launch', 'Offers or Deals']\n"
    "Spokespeople: ['Spokesperson1: Position', 'Spokesperson 2: Position', etc]\n"
    "Positive_Brand_Values: ['Design', 'Innovation', 'Inclusivity', 'Sustainability', 'Transparency/Trust',  'Value'] (Where the brand is associated positively with a given concept)\n"
    "Negative_Brand_Values: ['Design', 'Innovation', 'Inclusivity', 'Sustainability', 'Transparency/Trust',  'Value'] (Where the brand is associated negatively with a given concept)\n"
    "Story: A summary of the article in 15 words or fewer. This should be included on the same level as other metrics, one Story per brand, and should mention the brand\n\n"
    
    "IMPORTANT NOTE: All metrics MUST be returned for all brands. DO NOT combine, reorder or omit metrics"
    "IMPORTANT NOTE: If a Brand does not appear in the article, Mention_YN should always be simply 'No mention'. DO NOT analyse brands that are not mentioned")


# all prompts now live

def get_metrics(company, language):

     metrics_general = ("Mention_YN: ['Mentioned in article', 'No mention'] Whether the brand was mentioned in the article\n"
               "Corporate_Consumer: ['Corporate', 'Consumer'] Whether the theme of the mention is Consumer or Corporate. Pick best fit, use ONLY one of these two values.⌈\n"
               "Sentiment: ['Positive', 'Neutral', 'Negative']\n"
              f"Sentiment_explanation: The reason for your choice of sentiment. Please write in {language}.\n"
               "Passing_mention: ['Yes', 'No'] Is the mention of the brand entirely in passing and unlikely to affect its reputation?\n"
                    "Examples of a Passing Mention include: brief mention of the brand in a list of other brands, mentions of the brand using phrases like '...such as [brand]'.\n"
               "Topics: ['Financial Performance', 'Regulation', 'Product Launch', 'Offers or Deals']\n"
               "Spokespeople: ['Spokesperson1: Position', 'Spokesperson 2: Position', etc]\n"
               "Positive_Brand_Values: ['Design', 'Innovation', 'Inclusivity', 'Sustainability', 'Transparency/Trust',  'Value'] (Where the brand is associated positively with a given concept)\n"
               "Negative_Brand_Values: ['Design', 'Innovation', 'Inclusivity', 'Sustainability', 'Transparency/Trust',  'Value'] (Where the brand is associated negatively with a given concept)\n"
              f"Story: A summary of the article in 15 words or fewer. Please write in {language}, and ensure that the brand is mentioned.\n\n")

     dict_brand_prompt_metrics = {
     'ASOS': (
               "Mention_YN: ['Mentioned', 'No mention'] Whether the brand was mentioned in the article\n"
               "Sentiment: ['Positive', 'Neutral', 'Negative']\n"
              f"Sentiment_explanation: The reason for your choice of sentiment.  Please write in {language}.\n"
               "Prominence: ['Headline', 'First paragraph', 'Top half of article', 'Bottom half of article', 'Passing mention'].\n"
               "Media_Tier: leave blank\n"
               "Positive_reputational_pillars: ['ASOS can successfully target better business performance', 'Fashion creators, curators and champions of style', 'Fashion with integrity and sustainability']\n"
               "Negative_reputational_pillars: ['ASOS NOT capable of successfully targeting better business performance', 'NOT fashion creators, curators and champions of style', 'NO integrity or sustainability']\n"
               "ASOS_spokespeople: ['Firstname Surname, Position|Firstname Surname, Position|...] (Any spokespeople representing ASOS, including Unnamed)\n"
               "Third_party_spokespeople: ['Firstname Surname, Position|Firstname Surname, Position|...] (Apply for all other spokespeople)\n"
               "Topics: ['ESG', 'Product quality', 'E-commerce', 'Financial performance', 'Fashion credentials']\n"
              f"Story: A summary of the article in 15 words or fewer. Please write in {language}, and ensure that the brand is mentioned.\n\n"
     ),   
     'BDO Ireland': (
               "Mention_YN: ['Mentioned', 'No mention'] Whether the brand was mentioned in the article\n"
               "Sentiment: ['Positive', 'Neutral', 'Negative']\n"
              f"Sentiment_explanation: The reason for your choice of sentiment.  Please write in {language}.\n"
               "Prominence: ['Headline', 'First paragraph', 'Top half of article', 'Bottom half of article', 'Passing mention']\n"
               "PRI: ['Yes', 'No'] Whether the article is PR influenced. Yes if text includes evidence of spokesperson, press release or other input from company. No otherwise.\n"
              f"Story: A summary of the article in 15 words or fewer. Please write in {language}, and ensure that the brand is mentioned.\n\n"
     ),   
     'Diabetes UK': (
               "Mention_YN: ['Mentioned in article', 'No mention'] Whether the brand was mentioned in the article\n"
               "Sentiment: ['Positive', 'Neutral', 'Negative'] "
               "NB If Diabetes UK is cited in the article, this should usually be Positive as it displays expertise and knowledge sharing.\n"
              f"Sentiment_explanation: The reason for your choice of sentiment.  Please write in {language}.\n"
               "Passing_mention: ['Yes', 'No'] Is the mention of the brand entirely in passing and unlikely to affect its reputation?"
                    "Examples of a Passing Mention include: brief mention of the brand in a list of other brands, brief mentions of donations, etc'. "
                    "Do NOT return Yes if Diabetes UK is cited in the article. This is always more than a Passing mention.\n"
               "Key_category: ["
                    "'Diabetes UK', 'Care', 'Diabetes is serious', 'Fundraising', 'Healthy lifestyle', 'Research', 'Volunteer', 'World Diabetes Day', 'Tesco Partnership', 'Services"
                    "]"
                    "(Select from the list. Can be multiple. Use the following information to assess category presence: "
                    "'Diabetes UK': General org mentions, 'Care': Advice and support on Diabetes, 'Diabetes is serious': Risks and costs associated with Diabetes, "
                    "'Fundraising': all Diabetes UK fundraising, 'Healthy lifestyle': Diabetes UK promoting healthy lifestyle, 'Research': medical and scientific research, NOT market research, "
                    "'Volunteer': Diabetes UK icw volunteering, 'World Diabetes Day': icw Diabetes UK, 'Tesco Partnership': partnership with Tesco, 'Services': Helpline and care events.\n"
               "Campaigns_Diabetes_UK: ['General', 'Organisation'] \n"
               "Campaigns_Care: ['General', '4 Ts of Type 1 Diabetes', '15 Healthcare Essentials', 'Putting Feet First', 'Type 1 Essentials', Religious and Cultural Festivals', "
               "'Ramadan', 'Education - Taking Control', '100 Tips', 'Clinical Champions', 'Health Conditions in Schools Alliance'] \n"
               "Campaigns_Diabetes_is_serious: ['General', 'NHS Costs', 'Prevalance of diabetes', 'Early death', 'Diabetes complications', 'What is Type 1 Diabetes?', 'What is Type 2 Diabetes?'] \n"
               "Campaigns_Fundraising: ['General', 'London Marathon', 'Swim 22', 'Diabetes Week', 'London Bridges', '1 Million Steps', 'Remember a Charity', 'Obituary notice'] \n"
               "Campaigns_Healthy_Lifestyle: ['General', 'Prevalence', 'Prevention', 'Community Champions', 'Type 2 Risk Factors', 'BAME Type 2 Risk Factors', 'Enjoy Food', "
               "'NHS Diabetes Prevention Programme', 'Obesity Health Alliance', 'Roadshow', 'Know Your Risk', 'The Food You Love'] \n"
               "Campaigns_Research: ['General', 'Diabetes UK Professional Conference', 'Diabetes UK-funded research', 'DiRECT study', 'Type 1 Diabetes Grand Challenge'] \n"
               "Campaigns_Volunteer: ['General', 'Voluntary groups', 'Inspire Awards'] \n"
               "Campaigns_World_Diabetes_Day: ['General'] \n"
               "Campaigns_Tesco_Partnership: ['General', 'Fundraising', 'Let's Do This', 'Beat the Street', 'Rock the Shop', 'Big Collection', 'Make Move and Munch', "
               "'Family takeaway', 'Final Countdown Flagship Fundraiser', 'The Great Tesco Walk', 'Dance Beat'] \n"
               "Campaigns_Services: ['Make the Grade', 'Helpline', 'Type 1 Events'] \n"
               "IMPORTANT NOTE - For each of the preceding 'Campaigns_...' metrics, leave all blank UNLESS the relevant Key_category is selected for the article. "
               "Where relevant Key_category is present, Campaigns should be identified where they are named in the article, "
               "or where there is a clear link between the article content and campaign name. "
               "DO NOT use Press Release titles as campaigns, stick to items in the given lists for each particular metric.\n"
               "Spokespeople: ['Spokesperson1 (Company, Position)', 'Spokesperson 2 (Company, Position)', etc] "
                    "(Record all named and unnamed Diabetes UK spokespeople. Record Tesco and Bupa spokespeople ONLY if mentioned in connection with Diabetes UK. "
                    "Return 'Unnamed (Diabetes UK)' if Diabetes UK is cited without a spokesperson name. Do not record spokespeople from other organisations.)\n"
               "Press_release: ['Activity snacking for sugar levels', 'Ramadan advice' 'Frogs, Hypos and Type 2 remission', 'Artifical pancreas technology', 'Soup and Shakes diet', "
               "'Five million in UK with diabetes', 'Preventing Type 2 complications', 'Grand Challenge 5 million investment', 'Weight loss can put Type 2 in remission', "
               "NHS hybrid closed loop pilot', 'CEO Chris Askew steps down', '77% with diabetes affected by rising costs', 'Too many missing vital care', "
               "'Continuous glucose monitoring for young people', 'New diabetes care accreditatin programme']\n"
               "PRI: ['Yes', 'No'] IMPORTANT NOTE: Return Yes if the text contains evidence of comment, press release, information or data from Diabetes UK. No otherwise.\n"
               "Contact_details: ['diabetes.org.uk', 'Helpline'] IMPORTANT: Website ONLY if text includes link to 'diabetes.org.uk'. DO NOT assign yes for non-DUK websites. "
               "Helpline ONLY if text includes phone number '0345 123 2399'.\n"
               "Tesco_mention: ['Yes', 'No'] Whether the brand Tesco is mentioned in the text.\n"
               "Reporting_month: leave blank\n"
               "Custom_media_type: leave blank\n"
               "Region: leave blank\n\n"
              f"Story: A summary of the article in 15 words or fewer. Please write in {language}, and ensure that the brand is mentioned.\n"
     ),
     'Failte Ireland': (
               "Mention_YN: ['Mentioned', 'No mention'] Whether the brand was mentioned in the article\n"
               "Influence: ['Positive', 'Neutral', 'Negative']\n"
              f"Influence_explanation: The reason for your choice of sentiment.  Please write in {language}.\n"
               "Campaign: ['Wild Atlantic Way', 'Ireland's Ancient East', 'Dublin Breath of Fresh Air', 'Meet in Ireland']\n"
               "Publication_type:leave blank\n"
               "Article_type:['News item', 'Opinion or editorial', 'Interview', 'Letter']\n"
              f"Story: A summary of the article in 15 words or fewer. Please write in {language}, and ensure that the brand is mentioned.\n\n"
     ),  
     'Federation of Small Businesses': (
               "Mention_YN: ['Mentioned in article', 'No mention'] Whether the brand was mentioned in the article\n"
               "Sentiment: ['Positive', 'Neutral', 'Negative']\n"
              f"Sentiment_explanation: The reason for your choice of sentiment.  Please write in {language}.\n"
               "Prominence: ['Headline', 'First paragraph', 'Top half of article', 'Bottom half of article', 'Single mention'].\n"
                    "(This indicates where the first mention of the brand appeared in the article. 'Single mention' should only be used for very brief single mentions.)\n"
               "Article_type:['News item', 'Opinion or editorial', 'Feature', 'Letter']\n"
               "Spokespeople: ['Firstname Surname, Position, Company', 'Firstname Surname, Position, Company', '...'] (Record all named and unnamed FSB spokespeople.)\n"
               "Press_release: Please return 'left blank for further updates'\n"
               "PRI: ['Yes', 'No'] Yes if the text contains evidence of comment, press release or campaign from FSB. No otherwise.\n"
               "Third_party_spokespeople: ['Firstname Surname, Position, Company', 'Firstname Surname, Position, Company', '...'] (Apply for all other spokespeople)\n"
               "Region: ['National', 'North West', 'North East', 'Midlands', 'Eastern', 'Wales', 'London', 'South West', 'South East', 'Scotland', 'Northern Ireland', 'Yorkshire and the Humber'] "
                    "(for Region, please return the UK region from which the publication or story originates)"
               "Topic: ['Brexit', 'Fuel Prices', 'Exchange Rate', 'Apprenticeships', 'Exporting', 'Women in enterprise', 'Labour market', 'Working hours', 'Salaries', "
                    "'Absence and workplace health', 'Taxes'. 'Tax investigation', 'Legal Protection', 'Employment protection', 'Health and Safety', 'Legal', 'Insurance', "
                    "'Business Banking', 'Workplace pensions', 'Networking', 'Chancellor's Budget'] (Please include any that are relevant to the article)"
              f"Story: A summary of the article in 15 words or fewer. Please write in {language}, and ensure that the brand is mentioned.\n"
     ),
     'FirstGroup': (
               "Mention_YN: ['Mentioned in article', 'No mention'] Whether the brand was mentioned in the article\n"
               "Sentiment: ['Positive', 'Neutral', 'Negative']\n"
              f"Sentiment_explanation: The reason for your choice of sentiment.  Please write in {language}.\n"
               "Passing_mention: ['Yes', 'No'] Is the mention of the brand entirely in passing and unlikely to affect its reputation?\n"
                    "Examples of a Passing Mention include: brief mention of the brand in a list of other brands, mentions of the brand using phrases like '...such as [brand]'.\n"
               "Brand_Spokespeople: ['Firstname Surname (Position)', 'Firstname Surname (Position), '...'] (Record all named and unnamed brand spokespeople.)\n"
               "PRI: ['Yes', 'No'] Yes if the text contains evidence of comment from the brand. No otherwise.\n"
               "Third_party_spokespeople: ['Firstname Surname (Position)', 'Firstname Surname (Position), '...'] (Apply for all other spokespeople)\n"
              f"Key_stories: A summary of the article in 15 words or fewer. Please write in {language}, and ensure that the brand is mentioned.\n"
     ),
     'Go Ahead': (
               "Mention_YN: ['Mentioned in article', 'No mention'] Whether the brand was mentioned in the article\n"
               "Sentiment: ['Positive', 'Neutral', 'Negative']\n"
               f"Sentiment_explanation: The reason for your choice of sentiment.  Please write in {language}.\n"
               "Prominence: ['Headline', 'First paragraph', 'Top half of article', 'Bottom half of article', 'Single mention'].\n"
                    "(This indicates where the first mention of the brand appeared in the article. 'Single mention' should only be used for very brief single mentions.)\n"
               "Topic: ['Community', 'People', 'Environment', 'Tech']"
                    "NB - Community topic for community/diversity/inclusion, People for HR issues, Environment and Tech are self explanatory.\n"
               "Key_messages: ['Delivering for Customers', 'Sustainability', 'Great place to work', 'International Success Stories']\n"
               "PRI: ['Yes', 'No'] Yes if the text contains evidence of comment, press release or other PR activity from the brand. No otherwise.\n"
              f"PRI_explanation: The reason for your choice of PRI. Please write in {language}.\n"
              f"Story: A summary of the article in 15 words or fewer. Please write in {language}, and ensure that the brand is mentioned.\n"
     ),
     'KFC': (
               "Mention_YN: ['Mentioned in article', 'No mention'] Whether the brand was mentioned in the article.\n"
               "Author: Please extract the author's name from the article text if available.\n"
               "Sentiment: ['Favourable', 'Neutral', 'Unfavourable']\n" 
              f"Sentiment_explanation: The reason for your choice of sentiment\n.  Please write in {language}."
               "Prominence: ['Headline', 'First paragraph', 'Top half of article', 'Bottom half of article', 'Passing mention'].\n"
                    "(This indicates where the first mention of the brand appeared in the article. Passing mention is a special case and should be used whenever the brand is mentioned very briefly in passing.)\n"
               "Article_type: ['Comment', 'Feature', 'Letter', 'News', 'Interview', 'Product placement']\n"
               "Image: leave blank"
               "Press_release: leave blank"
               "Products: ['Original recipe', 'Buckets', 'Twister', 'Ricebox', 'Box meals', 'Krushems']\n"
               "Positive_anxieties ['Human', 'Modern', 'Quality']\n"
                    "(These indicate when the brand was associated with a particular attribute in a positive manner.\n"
                    "Human examples: caring, good employer, environmentally responsible.\n"
                    "Modern examples: cool, progressive, innovative, trendy\n"
                    "Quality examples: quality food, good brand/employee conduct, responsible sourcing)\n"
               "Negative_anxieties ['Human', 'Modern', 'Quality'] (As above, but for negative associations)\n"
               "Spokespeople: Firstname Surname (Position)|Firstname Surname (Position)|...\n"
               "Third_party_spokespeople: As above, for non-brand spokespeople\n"
               "Media_format: ['Print', 'Online', 'Broadcast']\n"
               "Media_type: ['National', 'Regional', 'Trade', 'Consumer/Lifestyle', 'Blog']\n"
               "Campaign: ['Gravy Burger', 'KFC Bucket Hat', 'KFC Golden Bucket', 'Litter Pickup', 'New jobs', 'New marketing manager', 'Popcorn chicken', 'Vegan Burger', 'Wingmen']\n"
               "Topics: ['Food safety', 'Health', 'Celebrity endorsement', 'Quick service restaurants', 'Welfare', 'Colonel Sanders', 'Delivery', 'Taste of food']\n"
              f"Story: A summary of the article in 15 words or fewer. Please write in {language}, and ensure that the brand is mentioned."
     ),
     'Lloyds Banking Group': (
               "Mention_YN: ['Mentioned in article', 'No mention'] Whether the brand was mentioned in the article.\n"
               "Author: Please extract the author's name from the article text if available.\n"
               "Business_division: ['Retail', 'Group transformation / digital', 'Wealth business (e.g. investments)', 'Motor financing', 'Business banking']\n" 
               "Product_type: ['Savings', 'Mortgages', 'Current Accounts', 'Credit Cards', 'Payments', 'Debit Cards', 'ATMs', 'Personal Loans', 'Other Retail', 'Retail Business Banking', 'Motor Finance']\n"
               "Service_type: ['Branches', 'Mobile/online banking', 'PoA/Bereavement teams', 'Remote advice', 'Flagship / Home Hub', 'Mobile branches', 'Cash and coin access', 'Statements', 'Cheques']\n"
               "Coverage_type: ['Product focus', 'Brand commentary', 'Customer advocacy (good/balanced)', 'Customer advocacy (bad)', 'Case study', 'Interview / feature with LBG employee', 'Customer complaint', 'Data or trends', 'Research', 'Passing/Incidental', 'Other']\n"
               "Sentiment: ['Positive', 'Neutral', 'Negative']\n" 
              f"Sentiment_explanation: The reason for your choice of sentiment. Please write in {language}.\n"
               "Group_sentiment: ['Positive', 'Neutral', 'Negative'] (Sentiment towards Lloyds Banking Group as a whole. Mark NA if not relevant (e.g. if competitor brand focus of article))\n" 
              f"Group_sentiment_explanation: The reason for your choice of sentiment. Please write in {language}.\n"
               "Prominence: ['Headline', 'First paragraph', 'Top half of article', 'Bottom half of article', 'Passing mention'].\n"
                    "(This indicates where the first mention of the brand appeared in the article. Passing mention is a special case and should be used whenever the brand is mentioned very briefly in passing.)\n"
               "Topics: ['Digital innovation', 'Infrastructure & connectivity', 'Savings', 'Support for Vulnerable Customers', 'Fraud', 'Motor Finance', 'Cash access (Including ATM)', "
                    "'Branches (excl. closures)', 'Branch closures', 'Spending (trends / habits)', 'Financial advice and family finances', 'Housing & housing research', 'House Prices', 'Businesses', "
                    "'Sustainable housing', 'Electric vehicles', 'Buy Now Pay Later', 'Awards & Recognitions', 'Sponsorship', 'Social housing']\n"
               "Positive_reputation_drivers: ['Financial performance', 'Leadership', 'Conduct', 'Customer service', 'Quality products and services', 'Employee treatment', 'Social impact']\n"
               "Negative_reputation_drivers: ['Financial performance', 'Leadership', 'Conduct', 'Customer service', 'Quality products and services', 'Employee treatment', 'Social impact'] \n"
               "Pos_bal_priority_rep_themes: ['UK businesses', 'Housing', 'Personal financial resilience & wellbeing', 'Sustainability'] Apply when a brand is seen providing support and assistance in a given area\n"
               "Neg_priority_rep_themes: ['UK businesses', 'Housing', 'Personal financial resilience & wellbeing', 'Sustainability'] Apply when a brand is criticised for lack of support and assistance in a given area\n"
               "LBG_spokespeople: ['Firstname Surname|Firstname Surname|...] Any LBG Spokespeople mentioned\n"
               "PRI: ['Yes', 'No] Whether the article was PR-influenced. Mark Yes if item includes evidence of a LBG spokesperson or press release, No otherwise.\n"
               "Competitor_spokespeople: ['Firstname Surname|Firstname Surname|...] (Apply for spokesperson from analysed competitor brand. See note on competitor brands)\n"
               "Third_party_spokespeople: ['Firstname Surname, Position|Firstname Surname, Position|...] (Apply for all other spokespeople)\n"
               "Press_release: Placeholder, leave blank\n"
               "Press_release_type: Placeholder, leave blank\n"
               "Helping_Britain_Recover: ['Yes', 'No'] Select Yes if either Helping Britain Recover or Helping Britain Prosper initiative is mentioned\n"
               "Branch_closure: ['Yes', 'No'] If article covers branch closures\n"
               "Name_of_branch_closure: Name of branch closed, if Branch_closure == Yes\n"
              f"Story: A summary of the article in 15 words or fewer. Please write in {language}, and ensure that the brand is mentioned.\n\n"
     ),
     'Lord Sugar': (
               "Mention_YN: ['Mentioned in article', 'No mention'] Whether the Lord Sugar/Alan Sugar/The Apprentice was mentioned in the article\n"
               "Sentiment: ['Positive', 'Neutral', 'Negative'] Sentiment of the article towards the brand. Only apply 'Negative' when sentiment is clearly and significantly negative.\n"
                    "NB - Any 'Pick of the Day' type mentions should be Positive, unless content is explicitly negative.\n"
                    "NB - Lord Sugar is often critical in his comments. Articles with comment from Lord Sugar should NOT be coded negative because of this. "
                    "Critical comments from Lord Sugar should be coded Neutral or Positive depending on the context, unless he is also strongly criticised in the article.\n"
              f"Sentiment_explanation: The reason for your choice of sentiment.  Please write in {language}.\n"
               "Passing_mention: ['Yes', 'No'] Is the mention of the brand entirely in passing and unlikely to significantly affect its reputation?\n"
                    "Examples of a Passing Mention include: 'This actor looks like Alan Sugar', 'The music is also used in the opening credits to The Apprentice. \n"
                    "This is not an exhaustive list of examples but should give an idea of the weight of the mention when Passing.\n"
                    "IMPORTANT: DO NOT mark Passing_mention as Yes if Alan Sugar is quoted.\n"
               "PRI: ['Yes', 'No'] Yes if the article includes direct comment by Lord Sugar (e.g. quote or opinion), no otherwise\n"
               "Topics: ['The Apprentice mentioned', 'Lord Alan Sugar mentioned']\n"
              f"Story: A summary of the article in 15 words or fewer, unless as noted below. Please write in {language}, and ensure that the brand is mentioned.\n"
                    "NB -  If the Story is merely a recommendation for the show The Apprentice, Story should appear verbatim as: 'TV Recommendation - The Apprentice'\n\n"
     ),
     'Molson Coors': (
               "Mention_YN: ['Mentioned in article', 'No mention'] Whether the brand was mentioned in the article\n"
               "Sentiment: ['Positive', 'Neutral', 'Negative']\n"
              f"Sentiment_explanation: The reason for your choice of sentiment.  Please write in {language}.\n"
               "Brand_attributes: ['Strong Corporate Reputation', 'Practises Sustainability', 'Great Employer', 'Socially Responsible'\n"
              f"Story: A summary of the article in 15 words or fewer. Please write in {language}, and ensure that the brand is mentioned.\n"
     ),
     'NICE': (
               "Mention_YN: ['Mentioned in article', 'No mention'] Whether the brand was mentioned in the article.\n"
               "Author: Please extract the author's name from the article text if available.\n"
               "Sentiment: ['Positive', 'Neutral', 'Negative'] Sentiment towards the brand\n"
              f"Sentiment_explanation: The reason for your choice of sentiment.  Please write in {language}.\n"
               "Passing_mention: ['Yes', 'No'] Is the mention of the brand entirely in passing and unlikely to affect its reputation?\n"
                    "Examples of a Passing Mention include: brief mention of the brand in a list of other brands, mentions of the brand using phrases like '...such as [brand]'.\n"
               "Topics: ['New guideline published', 'NICE's COVID-19 rapid guidelines', 'Appeals/Judicial reviews', 'New NICE advice published', " # Continued on line below
                    "'New reports published', 'New appointments to NICE', 'New collaborations or partnerships', 'Changes to NICE's processes/workflow', 'NICE Connect']\n" # Continued from line above
               "Key_messages: ['NICE is committed to getting the best care to patients fast and ensuring value for the taxpayer', 'Focus on what matters most', 'Provide useful and useable advice', 'Constantly learn from data and implementation']\n"
               "NICE_Spokespeople: ['Spokesperson1: Position', 'Spokesperson 2: Position', etc] List any NICE spokespeople, including unnamed.\n" 
               "Press_release: ["
                    #"'NICE recommends extending use of colorectal cancer tests 05/07/23', "
                    #"'AI tech to improve radiotherapy treatment planning 11/08/23', "
                    #"'Digital services to improve weight management support 15/08/2023', "
                    #"'Home care/virtual wards for respiratory patients 18/08/2023', "
                    #"'NICE recommends novel treatment for epidermolysis 18/08/2023', "
                    #"'100k fewer colonscopies per year after guidance update 24/08/2023', "
                    #"'International health technology assessment collaboration expands 24/08/23'"
                    "'Further migraine treatment choice for 145,000 people in England with rimegepant 31/05/2023",
                    "'Decision aid on sleeping pill prescriptions published 15/06/23",
                    "'Two life changing technologies for children with Type 2 Diabetes 11/05/2023",
                    "'More evidence needed to recommend Type 2 diabetes treatment tirzepatide 27/06/2023",
                    "'NICE draft guidance recommends new treatment for chronic heart failure 18/05/23",
                    "'NICE launches public consultation on health technology evaluations manual 27/06/2023",
                    "'NICE recommended weight-loss drug to be made available in specialist NHS services 08/03/23",
                    "'Nine treatment options to be made available for adults with depression or an anxiety disorder 16/05/2023",
                    "'One-stop-shop for AI and digital regulations for health and social care launched 12/06/23",
                    "'NICE finds reducing readiotherapy for breast cancer freed up appointments 14/06/23",
                    "'Testing could help prevent further strokes in people with gene variant 19/05/23"
                    "] (Select from the list. Please judge from the press release title whether it was likely present in the article.)\n"
               "PRI: ['Yes', 'No] Whether the article was PR-influenced. Mark Yes if item includes evidence of a spokesperson or press release, No otherwise.\n"
               "Media_type: leave blank\n"
              f"Story: A summary of the article in 15 words or fewer. Please write in {language}, and ensure that the brand is mentioned.\n\n"
     ),
     'The Post Office': (
               "Mention_YN: ['Mentioned in article', 'No mention'] Whether the brand was mentioned in the article.\n"
               "Passing_mention: ['Yes', 'No'] Is the mention of the brand entirely in passing and unlikely to affect its reputation?\n"
                         "Examples of a Passing Mention include: brief mention of the brand in a list of other brands, "
                         "mention of a brand storefront as a location, "
                         "local news report which briefly mentions that a post office has been kept open or closed historically, etc. "
                         "Do not make Yes if Post Office is quoted, or if its research appears in the article.\n"
               "Sentiment: ['Positive', 'Neutral', 'Negative'] Sentiment towards the brand. "
                         "Note that sentiment should always reflect the stance the article takes towards the Post Office, rather than the overall tone of the article. "
                         "A positive Post Office mention can appear in a generally negative article, and vice versa. "
                         "For example, a negative event at a Post Office (e.g. a robbery) is Neutral towards the Post Office, as the brand itself is not implicated. "
                         "Note that articles in which Post Office research appears should usually be positive, as these display thought leadership.  \n"
              f"Sentiment_explanation: The reason for your choice of sentiment.  Please write in {language}.\n"
               "Themes: 'Awards', 'Branch closure', 'Branch opening', 'Branch relocation', 'Compensation', 'Counter service', 'Deliveries', 'DVLA services', "
                    "'Financial services', 'Fraud/scams', 'Fundraising', 'Government partnerships', 'Identity services', 'Inclusion and diversity/social issues', "
                    "'Legal issues', 'Mobile Post Offices', 'Opening hours', 'Passing mention', 'Post Office research', 'Postmasters', 'Stamps'] "
                         "NB Errors to avoid - You have previously over-applied the Theme 'Post Office Network' ."
                         "This should NOT be added as a value UNLESS the article refers explicitly to the network on Post Office branches. "
                         "DO NOT infer this theme from general Post Office stories with no explicit mention of the network."
                         "You have previously over-applied Branch closure and Branch opening. Please use these only for explicit references to Post Office "
                         "branches opening and closing. DO NOT use this for stories such as change of ownership.\n"
               "Reputation_attribute: ['Commercial', 'Social purpose', 'Customer excellence', 'Growth', 'Modern', 'Knowledgeable'] "
                         "Return any values associated positively with the Post Office."
                         "There should be strong evidence of the attribute in the article. Brief or passing mentions are unlikely to support these, "
                         "so be careful about returning values here and do so only when they are very clearly supported by the text.\n"
               "Products_and_Services: ['Financial Services', 'Home Phone and Broadband', 'Travel', 'Counter Services', "
                    "'Post Office Network', 'Identity Services', 'Mails', 'Corporatisation'] "
                         "Record any services offered by the Post Office. Post Office Network should be used for any articles about branch opening/closing/relocations etc. "
                         "NB Errors to avoid - You have previously over-applied the 'Counter services' value for stories where services provided at Post Office counters "
                         "were not mentioned in the article. "
                         "Please avoid applying the 'Counter services' value unless counter services provided by the Post Office are very explicitly mentioned\n"
               "Products_and_Services_SubCategory: ['Savings and Investments, Credit cards & Loans', 'Mortgages', 'Making Payments', 'Business financial services', "
                    "'Insurance - Home', 'Insurance - Van', 'Insurance - Car', 'Insurance - motorcycle', 'Insurance - life cover', 'Insurance - business', 'Insurance - pet', "
                    "'International payments', 'Current accounts', 'Banking services', "
                    "'Home Phone and Broadband', 'International phone cards', "
                    "'Travel Insurance', 'Travel money', 'Travel documents', 'Travel extras', "
                    "'Passport & identity', 'Licence & Vehicle tax (DVLA)', 'Benefits', 'Motoring', "
                    "'Letters & Parcels', 'Stamps and postage', 'Mailing guide', 'Counter money services', "
                    "'Post Office Network', 'Crown Transformation', "
                    "'Click and Collect', 'Drop & Go', 'Drop Off points', 'Home Shopping/Online', 'Shopping', 'Christmas', "
                    "'New parcel pricing for Christmas', 'Christmas advertisements', 'Local collect'] "
                         "Should align with analysis from Products_and_Services field. "
                         "Use values from the list to provide more granular info on the Post Office services referenced."
                         "NB Making payments should refer to consumer payments taking place via the Post Office, not to e.g. compensation payments to postmasters.\n"
               "General_key_messages: ['Post Office is UK's largest retail network - 11,500 branches across the UK', "
                    "'The Post Office is often the last or only shop in a village and we are committed to providing services for every community', "
                    "'The Post Office network is stable', '99.7% of people live within 3 miles of a Post Office', '93% of people live within a mile of a Post Office']"
                         "NB Errors to avoid - You have previously over-applied the 99.7% and 93% key messages."
                         "The 99.7% and 93% mesages should be expected to appear more or less verbatim in the article text."
                         "DO NOT infer these messages or use them in a general sense, return these messages ONLY when they are EXPLICITLY conveyed in the article.\n"
               "Strategy_key_messages: ['Focusing on four core areas - mail and parcels, cash and banking, bill payments, travel money', "
                    "'Important that we get the proposition right for Postmasters', "
                    "'Demonstration of Post Office strategy to embrace new technology', "
                    "'Drop & Collect new format offers parcel collections and returns from the retailer’s handheld device and bill payment services', "
                    "'New proposition to meet customer demand for convenient collection and return of online shopping', "
                    "'Important that Post Offices offer the right products and services in the right place and time']"
                         "Use ONLY values from the given list. DO NOT create or add values."
                         "DO NOT infer these messages or use them in a general sense, return these messages ONLY when they are EXPLICITLY conveyed in the article.\n"
               "Postmaster_key_messages: ['Working on a Post Office that places our postmasters and customers at the centre of our business', "
                    "'The Post Office has increased remuneration for Postmasters', "
                    "'We are committed to a reset in our relationship with Postmasters', "
                    "'We are reinvesting to improve the proposition for Postmasters', ]"
                         "Use ONLY values from the given list. DO NOT create or add values."
                         "DO NOT infer these messages or use them in a general sense, return these messages ONLY when they are EXPLICITLY conveyed in the article.\n"
               "Banking_key_messages: ['Post Office network is the biggest retail network in the UK', "
                    "'Millions of customers of UK banks can rely on our branches for easy access to cash', "
                    "'Post Office trialling a new concept branch – a BankHub', "
                    "'Converting disused shops into Banking Hubs', "
                    "'Trialling speedy and automated local cash deposit facilities for small businesses', "
                    "'Personal, face-to-face service', "
                    "'Almost every bank customer can access their usual high street bank account at any Post Office branch', "
                    "'Over 4000 branches open seven days a week', ]"
                         "Use ONLY values from the given list. DO NOT create or add values."
                         "DO NOT infer these messages or use them in a general sense, return these messages ONLY when they are EXPLICITLY conveyed in the article.\n"
               "Financial_services_key_messages: ['Post Office is a leading savings provider', "
                    "'Post Office offers some of the most competitive savings rates in the market', "
                    "'Post Office offers some of the most competitive mortgage rates in the market']"
                         "Use ONLY values from the given list. DO NOT create or add values."
                         "DO NOT infer these messages or use them in a general sense, return these messages ONLY when they are EXPLICITLY conveyed in the article.\n"
               "Mails_key_messages: ['Our agreement with Royal Mail continues our strong partnership whilst also opening up new opportunities to work with other providers', "
                    "'Post Office in every community in the UK. Provides online retailers access to pick up and drop off network', "
                    "'Services such as Drop & Go are making life easier for customers', "
                    "'We want to provide a convenient service for those customers who would otherwise use a competitor']"
                         "Use ONLY values from the given list. DO NOT create or add values."
                         "DO NOT infer these messages or use them in a general sense, return these messages ONLY when they are EXPLICITLY conveyed in the article.\n"
               "Travel_key_messages: ['Post Office Travel Money mentioned', "
                    "'Post Office Barometer mentioned', "
                    "'Post Office research cited', "
                    "'Post Office is the UK’s largest foreign exchange provider', "
                    "'Currency can be ordered online at postoffice.co.uk']"
                         "Use ONLY values from the given list. DO NOT create or add values."
                         "DO NOT infer these messages or use them in a general sense, return these messages ONLY when they are EXPLICITLY conveyed in the article.\n"
               "Branch_key_messages: ['We understand how important a Post Office is to a community', "
                    "'We are committed to providing a Post Office in the area', "
                    "'We are delighted to have restored Post Office services to the area', "
                    "'Vibrant new-style Post Office at the heart of the community', "
                    "'Offer customers a wide-range of Post Office services', "
                    "'Everyday banking', "
                    "'Our outreach services help to sustain services in remote areas of the country']"
                         "Use ONLY values from the given list. DO NOT create or add values."
                         "DO NOT infer these messages or use them in a general sense, return these messages ONLY when they are EXPLICITLY conveyed in the article. "
                         "For example, DO NOT assign 'We are committed to providing a Post Office in the area' unless "
                         "the article includes some sort of input from the Post Office indicating this.\n"
               "Payzone_key_messages: ['There are around 24,000 Post Office and Payzone locations throughout the country', "
                    "'Customers can conveniently top up their bill payments at 24,000 Post Office and Payzone locations']"
                         "Use ONLY values from the given list. DO NOT create or add values."
                         "DO NOT infer these messages or use them in a general sense, return these messages ONLY when they are EXPLICITLY conveyed in the article.\n"
               "Identity_services_key_messages: ['Post Office is embracing new technologies for identity solutions', "
                    "'Ambitious strategy to deliver a unique offer that integrates digital and physical identity verification', "
                    "'Free-to-use App allows customers to build secure digital identity on smartphone', "
                    "'Post Office already market leader for providing digital identity solutions to access Government services']"
                         "Use ONLY values from the given list. DO NOT create or add values."
                         "DO NOT infer these messages or use them in a general sense, return these messages ONLY when they are EXPLICITLY conveyed in the article.\n"
               "Horizon_inquiry_key_messages: ['Sincerely sorry for past events and providing compensation to victims of the Horizon Scandal is a priority', "
                    "'Interim payments of up to £100,000 to the majority of people whose convictions have been overturned', "
                    "'For other postmasters affected, compensation is being paid through the Historical Shortfall Scheme']"
                         "Use ONLY values from the given list. DO NOT create or add values."
                         "DO NOT infer these messages or use them in a general sense, return these messages ONLY when they are EXPLICITLY conveyed in the article.\n"
               "Press_release: ['Cash deposits in September dip 3% 2023-10-09' (refers to a specific Post Office report on patterns in its cash deposits received September 2023), "
                         "'Five Post Office convictions overturned at Southwark Crown Court 2023-09-27' (refers to a SPECIFIC postmasters case at Southwark Crown Court), "
                         "'Post Office Far East Travel Money study 2023-09-23' (refers to a Post Office Travel Money study on the best travel bargains in the Far East)]"
                             "These will rarely be explicitly identified but you should be able to identify these from the name of the Press Release, the text of the article "
                             "and the short additional guidance provided here in parentheses. "
                             "Use your judgement.\n"
               "Spokespeople_Post_Office: ['Firstname Surname, Job title|Firstname Surname...] "
                         "List all Post Office spokespeople that appear, formatted as suggested. "
                         "IMPORTANT - Use this field ONLY for Post Office spokespeople. "
                         "DO NOT list non-Post Office spokespeople in this field, they should appear in the separate Third_Party_Spokespeople field. "
                         "IMPORTANT - If a postmaster is quoted in the article, include them in this field. They are Post Office employees and not third-aparty spokespeople. "
                         "IMPORTANT - Format with first name, surname and job title, separating each spokesperson with a | ."
                         "IMPORTANT - The Post Office Minister is part of the government and should be included under Third_Party_Spokespeople.\n"
              f"Story: A summary of the article in 15 words or fewer, mentioning the brand and setting it in context. Please write in {language}.\n"
               "Postmaster_mention: ['Yes', 'No'] Does the article include mention of a postmaster?\n"
               "Postmaster_Scheme_mention: ['Yes', 'No'] Does the article include mention of the postmaster compensation scheme?\n"
               "Best_buy_YN: ['Yes', 'No'] Is Post Office mentioned in a Best Buty Table\n"
               "Best_buy_type: ['Product mention, 'New Mortgages', 'New Mortgages rates', 'Rate of sale', 'Second time buyer', 'First time buyer', 'Help to buy', 'Brokers']\n"
               "Branch_opening_closing: ['Opening', 'Closing'] Indicate any mentions of Post Office branches opening or closing\n"
               "Call_to_action: ['Website', 'Phone number', 'Branch details', 'Email', 'Other'] "
                         "Indicate any calls to action FOR POST OFFICE ONLY. "
                         "IMPORTANT - DO NOT return Website UNLESS the website belongs to the Post Office. "
                         "For each website, consider if it belongs to the Post Office. Include Website ONLY for Post Office websites.\n"
               "Competitor: Mention any competitor banks, building societies or delivery companies that appear in the article\n"
               "Competitor_sentiment: ['Positive', 'Neutral', 'Negative'] General sentiment towards competitors mentioned\n"
               "Third_Party_Spokespeople: ['Firstname Surname, Job title|Firstname Surname...] List all non-Post Office spokespeople that appear"
                         "IMPORTANT - Use this field ONLY for NON-Post Office spokespeople. "
                         "Any spokesperson affiliated with Post Office should be recorded in the Spokespeople_Post_Office field."
                         "IMPORTANT - Format with first name, surname and job title, separating each spokesperson with a | .\n"
               "PRI: leave blank\n"
               "Region: leave blank\n"
     ),        
     'Royal Academy of Arts': (
               "Mention_YN: ['Mentioned in article', 'No mention'] Whether the brand was mentioned in the article.\n"
               "Sentiment: ['Positive', 'Neutral', 'Negative'] Sentiment towards the brand\n"
              f"Sentiment_explanation: The reason for your choice of sentiment.  Please write in {language}.\n"
               "Coverage_drivers: ['xxx listing', 'xxx feature', 'xxx review', 'xxx preview', 'xxx picture', 'xxx general mention'] Where xxx is the name of a relevant exhibition\n"
               "RAA_spokespeople: ['Christopher Le Brun, President', 'Charles Saumarez Smith, Secretary and Chief Executive', 'Eileen Cooper, Keeper', "
                    "'Eliza Bonham Carter, Head of RA Schools', 'Beth Schneider, Head of Learning', 'Kathleen Soriano, Director of Exhibitions', 'Ann Dumas, Curator', "
                    "'Adrian Locke, Curator', 'MaryAnne Stevens, Curator', 'Richard Rogers', 'David Chipperfield', 'Oliver Peyton'] Or 'Firstname Surname, Position' for any others who appear\n"
               "Key_messages: ['Independent/privately funded', 'Led by artists/architects', 'Offers exhibitions, education, debate', 'Oldest UK art school/only 3-year post-grad course', "
                    "'Outstanding collection/archive', 'Vibrant friends programme', 'International programme and partners', 'Attractive to donors/sponsors/trusts/foundations', "
                    "'Award-winning merchandise and publications', 'Home for art in the heart of Piccadilly', 'Contemporary art/architecture in Burlington Gardens']\n"
               "Campaigns_exhibitions: ['Summer Exhibition', 'Marina Abramovic', 'Angelica Kauffman', 'Making Modernism', 'William Kentridge', 'Spain and the Hispanic World', "
                    "'Impressionists on Paper', 'Entangled Pasts', 'In the Eye of the Storm', 'Michael Craig-Martin', 'Michelangelo, Leonardo, Raphael: Florence, c.1504', "
                    "'Souls Grown Deep like the Rivers', 'Young Artists Summer Show', 'Herzog and de Meuron']\n"
               "Call_to_action: ['Website details', 'Exhibition address', 'Phone number for booking']\n"
               "PRI: ['Yes', 'No'] Yes if comment from RAA spokesperson or evidence of Press Release. No otherwise.\n"
              f"Story: A summary of the article in 15 words or fewer. Please write in {language}, and ensure that the brand is mentioned.\n\n"
     ),
     'Santander': (
               "Mention_YN: ['Mentioned in article', 'No mention'] Whether the brand was mentioned in the article. "
                    "NB - RBS Natwest may appear verbatim, or as 'RBS' or 'Natwest' separately. "
                    "NB - Barclays coverage may include mentions of Barclaycard. These should be evaluated for the brand Barclays.\n "
                    "Please ensure that even minor single mentions of a brand are marked Yes.\n"
               "Passing_mention: ['Yes', 'No'] Is the mention of the brand entirely in passing and unlikely to affect its reputation?\n"
                    "Examples of a Passing Mention include: brief mention of the brand in a list of other brands, mention of a brand storefront as a location, etc.\n"
               "Sentiment: ['Very Positive', 'Slightly Positive', 'Mixed', 'Slightly Negative', 'Very Negative', 'Factual'] Sentiment towards the brand. "
                    "NB Sentiment special cases 1) All research by a brand displays thought leadership and should be Very or Slightly Positive, even if subject itself is difficult/controversial etc."
                    "NB Sentiment special cases 2) All best buy table items should be Factual, as they merely present information without taking a perspective.\n"
              f"Sentiment_explanation: The reason for your choice of sentiment.  Please write in {language}.\n"
               "Article_type: ['News', 'Feature', 'Comment piece', 'Letter', 'Interview']"
                    "Pay attention to form of article, it is usually clear if a piece is a letter from a reader or an opinion piece - "
                    "these should be marked appropriately, and not as News.\n"
               "Brand_spokesperson: ['Spokesperson Position Company|Spokesperson Position Company|...] "
                    "EXTREMELY IMPORTANT You are currently analysing this article for a brand extracted from brands_list. "
                    "Take a breath and ensure that you have this brand in mind. When filling this Spokesperson column, include ONLY spokespeople belonging to this brand in this column. "
                    "DO NOT include spokespeople from any brand other than that being analysed. "
                    "Record all non-brand spokespeople in Third_Party_Supportive or Third_Party_Critical fields, depending on the tone of the opinion expressed.\n"
               "Third_party_supportive: ['Spokesperson Position Company|Spokesperson Position Company|...] "
                    "Record any spokespeople from outside the brand who comment in a manner supportive of the brand. Format as suggested, separating each spokesperson with a | ."
                    "DO NOT include article authors as third party spokespeople.\n"
               "Third_party_critical: ['Spokesperson Position Company|Spokesperson Position Company|...] "
                    "Record any spokespeople from outside the brand who comment in a manner critical of the brand. Format as suggested, separating each spokesperson with a |\n"
               "Messages_positive: ['Trustworthy', 'Financially stable', 'Strong leadership', 'Industry expert', 'Excellent customer service', 'Innovative', 'CSR'] "
                    "Record any values positively associated with the brand through the article. "
                    "The 'Financially stable' message relates to the financial health of the brand (e.g. results, profits, share price). "
                    "It should only be applied when this is very strongly and clearly indicated in the article, do not infer it.\n"
               "Messages_negative: ['Untrustworthy', 'Not financially stable', 'Weak leadership', 'Not industry expert', 'Poor customer service', 'Not innovative', 'Poor CSR'] "
                    "Record any values negatively associated with the brand through the article. "
                    "The 'Not financially stable' message should only be applied when this is very strongly and clearly indicated in the article, do not infer it.\n"
              f"Story: A summary of the article in 15 words or fewer. Please write in {language}, and ensure that the brand is mentioned.\n"
               "Topic: ['Strategy', 'M&A', 'Employees', 'Financial performance', 'Results', 'Leadership', 'Partnerships', 'Regulation', "
                    "'Branch network', 'Current Accounts', 'Savings', 'Mortgages', 'Cards', 'Loans', 'Insurance', "
                    "'Consumer International and Forex', 'Business & Investment Banking', "
                    "'CSR & Charity', 'Thought Leadership', 'Santander Universities'] "
                    "Include relevant topics. You can apply multiple topics to a certain argument, but be careful not to over-apply topics. "
                    "IMPORTANT: In previous analyses, you have made two significant errors. PLEASE AVOID THESE. I shall outline them here: "
                    "Error to avoid 1: You WRONGLY apply Financially Stable messages (positive and negative) MUCH TOO OFTEN. ONLY apply this when it is very explicitly indicated in the article "
                    "(e.g. financial results announcement, profits, concerns over reserves etc). "
                    "You should expect to see financial stories as the client is in the banking sector, BUT YOU SHOULD NOT APPLY 'Financially Stable' "
                    "to any stories EXCEPT those indicated above. "
                    "Error to avoid 2: Similar to the above, you are using the Financial Performance topic much too often. "
                    "Use this ONLY when explicitly indicated in the article (e.g. financial results announcement, profits, concerns over reserves etc)."
                    "Error to avoid 3: You use the Consumer International and Forex Topic for all consumer stories. DO NOT APPLY THIS TOPIC UNLESS "
                    "the article explicitly mentions international money or Forex. It MUST NOT be used for general consumer stories.\n\n"
     ),
     'Scottish Water': (
               "Mention_YN: ['Mentioned in article', 'No mention'] Whether the brand was mentioned in the article.\n"
               "Sentiment: ['Positive', 'Neutral', 'Negative'] Sentiment towards the brand\n"
              f"Sentiment_explanation: The reason for your choice of sentiment.  Please write in {language}.\n"
               "Prominence: ['Headline', 'First paragraph', 'Top half of article', 'Bottom half of article', 'Passing mention'].\n"
                    "(This indicates where the first mention of the brand appeared in the article. Passing mention is a special case and should be used whenever the brand is mentioned very briefly in passing.)\n"
               "Press_release: return 'Left blank for further updates'\n"
               "Campaign: ['Nature Calls', 'Your Water Your Life', 'Learn to Swim', 'Join the Wave'] Campaign may be mentioned by name. Otherwise, tag as per the following info: "
                    "Nature Calls (bin wet wipes, don't flush them), Your Water Your Life (highlighting the vital role water plays in Scottish lives) "
                    "Learn to Swim (self explanatory), Join the Wave (sign up to a Scottish Water newsletter)\n"
               "Nature_Calls_key_messages: ['Bin wet wipes', 'Wet wipes containing plastic should be banned']"
               "Your_Water_Your_Life_key_messages: ['Use a refillable water bottle', 'Stay hydrated for health', 'Refillable bottles save money' "
                    "'Refillable bottles reduce single use plastic', 'Filling from the tap is good for you and the planet', "
                    "'Water points at Glasgow Central and Edinburgh Waverley stations']\n"
               "Learn_to_Swim_key_messages: ['Generation Swim', 'Learn to Swim programme makes people healthier', 'Learn to Swim programme makes people happier']\n"
               "Key_topics: ['Water efficiency', 'Water safety', 'River pollution', 'Combined sewer overflows', 'Raw sewage in rivers', 'Sewer chokes', "
                    "'Flooding', 'Wet wipes', 'Roadworks', 'None']\n"
               "Scottish_Water_spokespeople: ['Brian Lironi - Director of Corporate Affairs', 'Douglas Millican - Chief Executive', "
                    "'Simon Parsons - Director of Strategic Customer Service Planning', 'Rob Mustard - Director of Transformation and Digital', "
                    "'Peter Farrer - Chief Operating Officer'] Add other Scottish Water spokespeople as they appear"
               "Third_party_spokespeople: ['Firstname Surname - Position, Organisation', 'Firstname Surname - Position, Organisation', ...] (Apply for all other spokespeople)\n"
               "Images_and_logos: leave blank"
               "Media_tier: leave blank"
               "PRI: ['Proactive', 'Reactive', 'No PRI'] Proactive if article follows PR activity from Scottish Water. Reactive if Scottish Water is reacting to a story. "
               "No PRI if no evidence of PR activity from Scottish Water.\n"
              f"Story: A summary of the article in 15 words or fewer. Please write in {language}, and ensure that the brand is mentioned.\n\n"
     ),
     'Shell': (
               "Published region: Country of publication"
               "Publication origin: ['Local', 'International'] Whether source is limited to published regional or international"
               "Language: Language of article text"
               "Journalist: Identify author from text if possible"
               "Original_source: Note original source of article, if mentioned in text|NA"
               "Organisation: ['Shell', 'TotalEnergies', 'ExxonMobil', 'Chevron', 'BP', 'Showa Shell', 'NAM']"
               "Sentiment_towards_organisation: ['Strongly Positive', 'Positive', 'Slightly Positive', 'Evenly Mixed', 'Neutral', 'Evenly mixed', 'Slightly Negative', 'Negative', 'Strongly Negative']"
                    "NB Evenly mixed appears either side of Neutral. Neutral should be perfectly balanced. Evenly Mixed should be slightly to either side"
              f"Sent_exp: Brief explanation for sentiment choice. Please write in {language}."
               "Secondary_sentiment: leave blank"
               "Prominence: ['Headline', 'First paragraph', 'Top half of article', 'Bottom half of article', 'Passing mention'].\n"
                    "(This indicates where the first mention of the brand appeared in the article. Passing mention is a special case and should be used whenever the brand is mentioned very briefly in passing.)\n"
               "Significance: ['Major', 'Moderate', 'Minor'] Significance of brand mention"
               "Business_area: ['Upstream', 'Downstream', 'Projects & Tech', 'Integrated Gas', 'New Energies'] "
                    "(NB on Business_area - Upstream: Exploration and production, Downstream: Refining & distribution, P&T: New refineries & platforms, any article featuring Harry Brekelmans, "
               "Integrated Gas: LNG and gas-to-liquids, New Energies: Low carbon & renewables research)"
               "Corporate_drivers: ['Investment', 'Divestments', 'Mergers and Acquisitions', 'Group or Company strategy', 'JVs or partnerships', 'Group portfolio', "
                    "'Portfolio diversity', 'Shareholder policy', 'Corporate governance', 'Legal issues', 'Revenue Transparency', 'Executive remuneration', "
                    "'Bribery and corruption', 'Net Carbon Footprint ambition', 'COVID-19', 'CEO change']"
               "Primary_theme: ['Energy transition', 'Brand', 'HR', 'Management/finance', 'Nigeria', 'Operations', 'Sustainability', 'NA']"
               "Secondary_theme: ['Energy transition', 'Brand', 'HR', 'Management/finance', 'Nigeria', 'Operations', 'Sustainability', 'NA'] Select up to three"
               "Societal_issues: ['Social Performance', 'Social Investment', 'Protests', 'Local Communities', 'Recruitment/Layoffs', 'Pensions', 'STEM/Education']"
               "Reputation_attributes_positive: ['Trust', 'Leading technology', 'Engineering excellence', 'Customer first']"
               "Reputation_attributes_negative: ['Trust', 'Leading technology', 'Engineering excellence', 'Customer first']"
               "Energy_source: ['Oil', 'Gas', 'Renewables', 'Solar', 'Wind', 'Biofuel', 'Tar Sands', 'Coal', 'Hydrogen', 'Methane', 'Nuclear', 'Coal Seam Gas']"
               "Regions_mentioned: Any COUNTRIES (NOT NY, Texas etc) mentioned ICW brand or industry"
               "Story_origin: ['Local', 'International' , 'International AND local'] Whether story is located in publication region or internationally"
               "CEO_mention: ['Ben van Beurden', 'Tsuyoshi Kameoka', 'Katsuaki Shindome', 'Gretchen Watkins', 'Marjan van Loon', 'Sinead Lynch', 'Wael Sawan']"
               "Sentiment_towards_CEO: ['Strongly Positive', 'Positive', 'Slightly Positive', 'Evenly Mixed', 'Neutral', 'Evenly mixed', 'Slightly Negative', 'Negative', 'Strongly Negative']"
               "Organisation_spokespeople: [Firstname Surname (Title - Company)|Firstname Surname...]"
               "PR_influenced: ['Yes', 'No] Yes if includes evidence of PR influence, including spokesperson comment, press release or campaign"
               "PRI_exp: Brief explanation for PRI choice"
               "Shell_projects_and_assets: ['Pearl GTL', 'Appomatox', 'Brent Decomissioning', 'Groningen', 'Pennsylvania', 'Petrochemicals Complex', 'Kaikias', 'Vito', 'Nanhai', "
                    "'AO4 Geismar', 'Elba', 'Prelude', 'Permian', 'Fox Creek', 'Pegaga', 'Bonga South West', 'Shell Energy and Chemicals', 'Park Rotterdam', 'Cambo oil field', "
                    "'Sakhalin-2', 'Nord Stream 2']"
              f"Story: A summary of the article in 15 words or fewer. Please write in {language}, and ensure that the brand is mentioned."
     ),
     
     'Walgreens Boots Alliance': (
               "Mention_YN: ['Mentioned in article', 'No mention'] Whether the brand was mentioned in the article\n"
               "Sentiment: ['Positive', 'Neutral', 'Negative']\n"
              f"Sentiment_explanation: The reason for your choice of sentiment.  Please write in {language}.\n"
               "Passing_mention: ['Yes', 'No'] Is the mention of the brand entirely in passing and unlikely to significantly affect its reputation?\n"
               "Topics: ['Profitability', 'Share price', 'Repositioning as healthcare provider', 'Race and gender issues', 'Other (non-CEO) staff departures', 'Sale of Boots']"
               "NB - Return the 'Other staff departures' topic ONLY if article references the departure of a member of staff who is NOT Rosalind Brewer\n"
               "WBA_Spokespeople: ['Firstname Surname, Position', 'Firstname Surname, Position', ...] Any Wallgreens Boots Alliance (WBA) spokespeople that appear in the article. "
               "NB - These should be returned only if they are QUOTED in the article. If the person is merely mentioned and not quoted, do not return them in the list. "
               "NB - WBA may be referred to simply as Walgreens or Boots.\n"
               "3rd_P_Supportive: ['Firstname Surname, Position, Organisation', 'Firstname Surname, Position, Organisation', ...] "
               "Any third-party commentators cited in the article whose statements are SUPPORTIVE towards WBA\n"
               "3rd_P_Neutral: ['Firstname Surname, Position, Organisation', 'Firstname Surname, Position, Organisation', ...] "
               "Any third-party commentators cited in the article whose statements are either balanced or neutral towards WBA\n"
               "3rd_P_Critical: ['Firstname Surname, Position, Organisation', 'Firstname Surname, Position, Organisation', ...] "
               "Any third-party commentators cited in the article whose statements show CRITICISM of WBA\n"
              f"Story: A summary of the article in 15 words or fewer. Please write in {language}, and ensure that the brand is mentioned.\n\n"
     ),
     'Zoological Society of London': (
               "Mention_YN: ['Mentioned in article', 'No mention'] Whether the brand was mentioned in the article\n"
               "Sentiment: ['Positive', 'Neutral', 'Negative']\n"
              f"Sentiment_explanation: The reason for your choice of sentiment.  Please write in {language}.\n"
               "Prominence: ['Headline', 'First paragraph', 'Top half of article', 'Bottom half of article', 'Passing mention']."
                    "(This indicates where the first mention of the brand appeared in the article. Passing mention is a special case and should be used whenever the brand is mentioned very briefly in passing.)\n"
               "Division: ['ZSL Field Conservation', 'ZSL Whipsnade Zoo', 'ZSL Science', 'ZSL London Zoo', 'ZSL General]\n"
               "Key_messages: ['ZSL calling on world leaders to think about nature', 'Animal care and expertise', 'Visitor experience', 'Innovation', 'Funding our work', "
                    "'Inspiring action', 'Conservation', 'Education', 'Science', 'Charity']\n"
               "Spokespeople: ['Firstname Surname', 'Firstname Surname', ...] Any ZSL spokespeople that appear in the article\n"
               "Call_to_action: ['Wesbite', 'Phone number', 'Address]\n"
               "Press_release: ['UK should join Biodiversa+', 'Red kite health checks', 'Biodiversity risk guide for pensions industry', 'Surshti Patel wins Wayfinder conservation award']\n"
               "Event: ['IUCN/International Union for Conservation of Nature Congress', 'COP15', 'COP26', 'COP27']\n"
              f"Story: A summary of the article in 15 words or fewer. Please write in {language}, and ensure that the brand is mentioned.\n\n"
     ),
     }

     return dict_brand_prompt_metrics[company] if company in dict_brand_prompt_metrics else metrics_general



# %% PPT summarisation prompts ------------------------------------------------

def prompt_prominence(brand, table_prominence_summary, table_prominence_full):
     
     (f"Using the below information, please could you summarise in NO MORE THAN 100 words the overall prominence picture for the brand {brand}:\n\n"

    f"{table_prominence_summary}\n\n"

    "Here is a table containing a summary of maximum top 50 mentions of the brand, sorted by prominence:\n\n" 

    f"{table_prominence_full}\n\n"

    "If using percentages, you can provide text-based descriptions that are more readable (e.g. 'around a quarter' if the percentage for a given metric is around 25%).\n"
    "After giving an outline of the proportion of prominence types, please use the information from the second table to discuss what drove the highest-prominence mentions.\n"
    "For Headline mentions, you can quote the headline verbatim. For other mentions, the Story column may be useful in generating a description of the key drivers.\n"
    "Use the Publication column appropriately to refer to the sources which include the highest prominence mentions."
    )
     
def prompt_corp_con(brand, table_corp_con_summary, table_corp_con_full):
     
     (f"Using the below information, please could you summarise in NO MORE THAN 100 words the overall corporate and consumer picture for the brand {brand}:\n\n"
      
     "Here is a record of the type of media mentions for the brand over the reporting period:\n\n"

     f"{table_corp_con_summary}\n\n"

     "And below is a table containing metadata for all mentions of the brand (up to a maximum of 50), sorted with the highest-prominence mentions first:\n\n" 

     f"{table_corp_con_full}\n\n"

     "If using percentages, you can provide text-based descriptions that are more readable (e.g. 'around a quarter' if the percentage for a given metric is around 25%).\n"
     "After giving an outline of the proportion of article types, please use the information from the second table to discuss what drove each type of mention.\n"
     "Use the Publication column appropriately to refer to the sources which included each type of mention."
     )

def prompt_topics(brand, table_topics_summary, table_topics_full):
     
     (f"Using the below information, please could you summarise in NO MORE THAN 100 words the way that topics were distributed in media coverage for the brand {brand}:\n\n"
     
     "Here is a summary of the volumes by Topic:\n\n" 

     f"{table_topics_summary}\n\n"

     "And below is a table containing metadata for all mentions of the brand (up to a maximum of 50), sorted by prominence:\n\n" 

     f"{table_topics_full}\n\n"

     "If using percentages, you can provide text-based descriptions that are more readable (e.g. 'around a quarter' if the percentage for a given metric is around 25%).\n"
     "After giving an outline of the proportion of topics, please use the information from the second table to discuss what drove important mentions, linking the stories to the pertinent topics.\n"
     "For Headline mentions, you can quote the headline verbatim. For other mentions, the other columns may be useful in generating a description of the key drivers.\n"
     "Use the Publication column appropriately to refer to the sources which included key mentions."
     )     

def prompt_pos_values(brand, table_pos_values_summary, table_pos_values_full):
     
     (f"Using the below information, please could you summarise in NO MORE THAN 100 words the way that positive brand values were distributed in media coverage for the brand {brand}:\n\n"
     
     "Here is a summary of the volumes for each brand value:\n\n" 

     f"{table_pos_values_summary}\n\n"

     "And below is a table containing metadata for all mentions of the brand (up to a maximum of 50), sorted by prominence:\n\n" 

     f"{table_pos_values_full}\n\n"

     "If using percentages, you can provide text-based descriptions that are more readable (e.g. 'around a quarter' if the percentage for a given metric is around 25%).\n"
     "After giving an outline of the proportion of topics, please use the information from the second table to discuss what drove important mentions.\n"
     "For Headline mentions, you can quote the headline verbatim. For other mentions, other columns may be useful in generating a description of the key drivers.\n"
     "Use the Publication column appropriately to refer to the sources which included key mentions.\n"
     "When discussing key drivers, you should link them to the brand values with which they were associated here.\n"
     "Negative values are dealt with separately, so please discuss only positive values here.\n"
     )   

def prompt_neg_values(brand, table_neg_values_summary, table_neg_values_full):
     
     (f"Using the below information, please could you summarise in NO MORE THAN 100 words the way that negative brand values were distributed in media coverage for the brand {brand}:\n\n"
     
     "Here is a summary of the volumes for each brand value:\n\n" 

     f"{table_neg_values_summary}\n\n"

     "And below is a table containing metadata for all mentions of the brand (up to a maximum of 50), sorted by prominence:\n\n" 

     f"{table_neg_values_full}\n\n"

     "If using percentages, you can provide text-based descriptions that are more readable (e.g. 'around a quarter' if the percentage for a given metric is around 25%).\n"
     "After giving an outline of the proportion of topics, please use the information from the second table to discuss what drove important mentions.\n"
     "For Headline mentions, you can quote the headline verbatim. For other mentions, other columns may be useful in generating a description of the key drivers.\n"
     "Use the Publication column appropriately to refer to the sources which included key mentions.\n"
     "When discussing key drivers, you should link them to the brand values with which they were associated here.\n"
     "Positive values are dealt with separately, so please discuss only positive values here.\n"
     ) 


# %% Brand-specific prompts

# NB - These prompts are no longer in use. Replaced by one general prompt which takes metrics for each brand dynamically

# Each take a df df_brands_sample, which contains the user-specified number of rows to analyse (can be all)
# ...and i, which allows a list of articles to iterate over the prompt


# %% Diabetes UK
def eval_prompt_Diabetes_UK (df_brands_sample, i):
          prompt = (f"The following list is called brand_list: {df_brands_sample.iloc[i]['Brands_Bool']}.\n"
          "It contains either a single brand or multiple brands (if multiple, each brand will be separated by a |)\n\n "
          "The following represents the headline and full text of a news article: \n"
          "Headline: \n"
          f"{df_brands_sample.iloc[i]['Headline']}\n"
          "Article text: \n"
          f"{df_brands_sample.iloc[i]['Full Text'][:7500]}\n"

          "Could you please analyse the headline and article, and provide in response a single JSON object.\n"
          "Please DO NOT include any additional commentary outside of the single JSON object.\n"
          "The JSON object should be formatted so that each brand in brand_list appears on the top level, with their respective attributes nested one level deeper.\n"
          "If only one value is returned, e.g. for Sentiment, it should be returned as a string.\n"
          "If multiple values are returned, e.g. for Brand Values, they should be returned as an array.\n"
          "If a brand is not mentioned, only Mention_YN should be filled. The remaining metrics should be simply 'NA'.\n"
          "The attributes for each brand should be as follows:\n\n"

          

          "IMPORTANT NOTE: All metrics MUST be returned for all brands. DO NOT combine, reorder or omit metrics"
          "IMPORTANT NOTE: If a Brand does not appear in the article, Mention_YN should always be simply 'No mention'. DO NOT analyse brands that are not mentioned")

          return prompt

# %% KFC
def eval_prompt_KFC (df_brands_sample, i):
          
          prompt = (f"The following list is called brand_list: {df_brands_sample.iloc[i]['Brands_Bool']}.\n"
          "It contains either a single brand or multiple brands (if multiple, each brand will be separated by a |)\n\n "
          "The following represents the headline and full text of a news article: \n"
          "Headline: \n"
          f"{df_brands_sample.iloc[i]['Headline']}\n"
          "Article text: \n"
          f"{df_brands_sample.iloc[i]['Full Text'][:7500]}\n"

          "Could you please analyse the headline and article, and provide in response a single JSON object.\n"
          "Please DO NOT include any additional commentary outside of the single JSON object.\n"
          "The JSON object should be formatted so that each brand in brand_list appears on the top level, with their respective attributes nested one level deeper.\n"
          "If only one value is returned, e.g. for Sentiment, it should be returned as a string.\n"
          "If multiple values are returned, e.g. for Brand Values, they should be returned as an array.\n"
          "If a brand is not mentioned, only Mention_YN should be filled. The remaining metrics should be simply 'NA'.\n"
          "The attributes for each brand should be as follows:\n\n"

          

          "IMPORTANT NOTE: Brand names MUST appear on the top level of the JSON. DO NOT include an additional top level e.g. 'brands'\n"
          "IMPORTANT NOTE: All metrics MUST be returned for all brands. DO NOT combine, reorder or omit metrics\n"
          "IMPORTANT NOTE: If a Brand does not appear in the article, Mention_YN should always be simply 'No mention'. DO NOT analyse brands that are not mentioned")          

          return prompt

# %% LBG
def eval_prompt_LBG (df_brands_sample, i):
          
          prompt = (f"The following list is called brand_list: {df_brands_sample.iloc[i]['Brands_Bool']}.\n"
          "It contains either a single brand or multiple brands (if multiple, each brand will be separated by a |)\n\n "
          "The following represents the headline and full text of a news article: \n"
          "Headline: \n"
          f"{df_brands_sample.iloc[i]['Headline']}\n"
          "Article text: \n"
          f"{df_brands_sample.iloc[i]['Full Text'][:7500]}\n"

          "Could you please analyse the headline and article, and provide in response a single JSON object.\n"
          "Please DO NOT include any additional commentary outside of the single JSON object.\n"
          "The JSON object should be formatted so that each brand in brand_list appears on the top level, with their respective attributes nested one level deeper.\n"
          "If only one value is returned, e.g. for Sentiment, it should be returned as a string.\n"
          "If multiple values are returned, e.g. for Brand Values, they should be returned as an array.\n"
          "If a brand is not mentioned, only Mention_YN should be filled. The remaining metrics should be simply 'NA'.\n"
          "The attributes for each brand should be as follows:\n\n"

          

          "IMPORTANT NOTE: Brand names MUST appear on the top level of the JSON. DO NOT include an additional top level e.g. 'brands'\n"
          "IMPORTANT NOTE: All metrics MUST be returned for all brands. DO NOT combine, reorder or omit metrics\n"
          "IMPORTANT NOTE: If a Brand does not appear in the article, Mention_YN should always be simply 'No mention'. DO NOT analyse brands that are not mentioned")
          "IMPORTANT NOTE: For any metrics that distinguish between LBG and competitors, make note of which group the following brands belong to:\n"
          "LBG brands: ['Lloyds Bank', 'Halifax', 'Bank of Scotland', 'MBNA', 'Birmingham Midshires', 'Lex auto lease', 'Black Horse', 'Tusker']\n"
          "Competitor brands: ['Barclays', 'HSBC', 'Nationwide', 'NatWest', 'RBS', 'Santander', 'TSB', 'Monzo', 'Starling', 'Paypal', 'Revolut', 'Metro', 'First Direct']\n"
          

          return prompt

# %% Lord Sugar
def eval_prompt_Lord_Sugar (df_brands_sample, i):
          prompt = (f"The following list is called brand_list: {df_brands_sample.iloc[i]['Brands_Bool']}.\n"
          "It contains either a single brand or multiple brands (if multiple, each brand will be separated by a |)\n\n "
          "The following represents the headline and full text of a news article: \n"
          "Headline: \n"
          f"{df_brands_sample.iloc[i]['Headline']}\n"
          "Article text: \n"
          f"{df_brands_sample.iloc[i]['Full Text'][:7500]}\n"

          "Could you please analyse the headline and article, and provide in response a single JSON object.\n"
          "Please DO NOT include any additional commentary outside of the single JSON object.\n"
          "The JSON object should be formatted so that each brand in brand_list appears on the top level, with their respective attributes nested one level deeper.\n"
          "If only one value is returned, e.g. for Sentiment, it should be returned as a string.\n"
          "If multiple values are returned, e.g. for Brand Values, they should be returned as an array.\n"
          "If a brand is not mentioned, only Mention_YN should be filled. The remaining metrics should be simply 'NA'.\n"
          "The attributes for each brand should be as follows:\n\n"

          

          "IMPORTANT NOTE: The client may sometimes be referred to as Lord Sugar, Alan Sugar or combinations thereof. The Apprentice is a TV show fronted by the client"
          "IMPORTANT NOTE: All metrics MUST be returned for all brands. DO NOT combine, reorder or omit metrics"
          "IMPORTANT NOTE: If a Brand does not appear in the article, Mention_YN should always be simply 'No mention'. DO NOT analyse brands that are not mentioned")

          return prompt

# %% NICE
def eval_prompt_NICE (df_brands_sample, i):
          
          prompt = (f"The following list is called brand_list: {df_brands_sample.iloc[i]['Brands_Bool']}.\n"
          "It contains either a single brand or multiple brands (if multiple, each brand will be separated by a |)\n\n "
          "The following represents the headline and full text of a news article: \n"
          "Headline: \n"
          f"{df_brands_sample.iloc[i]['Headline']}\n"
          "Article text: \n"
          f"{df_brands_sample.iloc[i]['Full Text'][:7500]}\n"

          "Could you please analyse the headline and article, and provide in response a single JSON object.\n"
          "Please DO NOT include any additional commentary outside of the single JSON object.\n"
          "The JSON object should be formatted so that each brand in brand_list appears on the top level, with their respective attributes nested one level deeper.\n"
          "If only one value is returned, e.g. for Sentiment, it should be returned as a string.\n"
          "If multiple values are returned, e.g. for Brand Values, they should be returned as an array.\n"
          "If a brand is not mentioned, only Mention_YN should be filled. The remaining metrics should be simply 'NA'.\n"
          "The attributes for each brand should be as follows:\n\n"

          

          "IMPORTANT NOTE: All metrics MUST be returned for all brands. DO NOT combine, reorder or omit metrics"
          "IMPORTANT NOTE: If a Brand does not appear in the article, Mention_YN should always be simply 'No mention'. DO NOT analyse brands that are not mentioned")

          return prompt

# %% Shell
def eval_prompt_Shell (df_brands_sample, i):
          
          prompt = (f"The following list is called brand_list: {df_brands_sample.iloc[i]['Brands_Bool']}.\n"
          "It contains either a single brand or multiple brands (if multiple, each brand will be separated by a |)\n\n "
          "The following represents the headline and full text of a news article: \n"
          "Headline: \n"
          f"{df_brands_sample.iloc[i]['Headline']}\n"
          "Article text: \n"
          f"{df_brands_sample.iloc[i]['Full Text'][:7500]}\n"

          "Could you please analyse the headline and article, and provide in response a single JSON object.\n"
          "Please DO NOT include any additional commentary outside of the single JSON object.\n"
          "The JSON object should be formatted so that each brand in brand_list appears on the top level, with their respective attributes nested one level deeper.\n"
          "If only one value is returned, e.g. for Sentiment, it should be returned as a string.\n"
          "If multiple values are returned, e.g. for Brand Values, they should be returned as an array.\n"
          "If a brand is not mentioned, only Mention_YN should be filled. The remaining metrics should be simply 'NA'.\n"
          "The attributes for each brand should be as follows:\n\n"

          

          "IMPORTANT NOTE: Brand names MUST appear on the top level of the JSON. DO NOT include an additional top level e.g. 'brands'\n"
          "IMPORTANT NOTE: All metrics MUST be returned for all brands. DO NOT combine, reorder or omit metrics\n"
          "IMPORTANT NOTE: If a Brand does not appear in the article, Mention_YN should always be simply 'No mention'. DO NOT analyse brands that are not mentioned")          

          return prompt