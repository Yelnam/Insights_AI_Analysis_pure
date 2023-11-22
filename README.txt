NB:
Do not transfer OpenAIKey file to a new user - this is an owned API key which should be used only by the owner

-- TO DO:

- Handle long article texts with 32k (built into script, updated model_long when 32k available)
- Add timeout for individual articles
- Handle errors if submitted articles contain no relevant articles
- Add input box to provide list of Article IDs
- Ensure response and dummy response match (e.g. if taking full response rather than index)
- Set brand sentiment text live for PPT generation (consider optional demo mode)
- Too many dicts for brand metrics. Make one dict with various values per key