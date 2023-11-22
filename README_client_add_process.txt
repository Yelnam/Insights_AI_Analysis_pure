Adding a new client:

Add prompt to get_metrics function in file prompts.py
- Metrics should match brief, with additional instructions if necessary
- Formatting of prompt should match pre-existing prompts

Update client entry in the following dicts in dicts_data_analysis.py:
-------- dict_brand_brands_2
-- include any brands to be analysed for the client, including client and any competitors

-------- dict_brand_spokes
-- add any spokespeople to be tracked, including name variations

-------- dict_brand_metrics_cols (four separate values for each company key)

---- SA_cols
-- used to remove columns from SA datasheet, leaving metadata and article IDs
-- any analyses will be later transplanted onto the empty SA metadata

---- GI_cols
-- any columns to take from GI prior to analysis
-- this should always include 'Local Article Id', 'Url', 'Headline', 'Full Text', 'Brands_Bool' 
-- AND any metrics already filled in GI

---- brand_metrics
-- these should match the metrics in the prompt stored in prompts.py
-- used to build a table from the response supplied by GPT

---- brand_metrics_SA
-- used to insert the metrics returned from GPT into a SA formatted worksheet
-- should match the order of the original SA metrics, with any additional metrics you want to include (e.g. sentiment_explanation) added on the right
-- this simply makes it easier to append the resulting output to any existing Score App-based datasets an analyst will be working with