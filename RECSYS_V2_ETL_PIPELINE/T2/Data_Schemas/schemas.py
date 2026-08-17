import pandera.pandas as pa

available_news_categories = ['lifestyle', 'news', 'health', 'sports', 'weather', 'entertainment',
 'foodanddrink', 'autos', 'travel', 'video', 'finance', 'tv', 'movies', 'music',
 'kids', 'middleeast', 'games', 'northamerica', 'entertainment', 'news', 'sport', 'music', 'crime', 'sex_and_cohabitation', 'holiday', 'cars', 'incoming', 'consumption', 'web tv', 'library', 'side9', 'the craftsman', 'plus', 'nations', 'vin', 'about_extra_bladet', 'subscription', 'services', 'video', 'horoscopes', 'public opinion', 'spacious', 'eblive', 'agenda', 'webmaster test section', 'migration_catalog', 'podcast', 'play', 'rssfeed', 'auto', 'money']

#mathcing the subcategories to only the categoirs you like for example if you like hea;lth category you should ony be shown health cattegories or not?
available_news_sub_categories = ['lifestyleroyals', 'newsscienceandtechnology', 
    'weightloss', 'medical', 'newsworld', 'voices', 'cardio', 'football_nfl', 
    'weathertopstories', 'gaming', 'recipes', 'lifestylelovesex', 'nutrition', 
    'autosenthusiasts', 'autossports', 'wellness', 'health-news', 'celebrity', 
    'travelarticle', 'autossuvs', 'newspolitics', 'more_sports', 'traveltripideas', 
    'animals', 'autosnews', 'newsbusiness', 'golf', 'newstrends', 'lifestylepetsanimals', 
    'finance-insurance', 'football_ncaa', 'lifestylebuzz', 'mma', 'fitness', 'newsus', 
    'tv-gallery', 'tvnews', 'lifestylehoroscope', 'basketball_nba', 'news', 'shop-all', 
    'newsphotos', 'lifestylemindandsoul', 'travelnews', 'basketball_ncaa', 
    'finance-real-estate', 'quickandeasy', 'tv-celebrity', 'financenews', 
    'lifestyleparenting', 'movies-gallery', 'racing', 'tipsandtricks', 'baseball_mlb', 
    'musicnews', 'autosbuying', 'shop-apparel', 'autostrucks', 'lifestyledidyouknow', 
    'finance-career-education', 'finance-retirement', 'restaurantsandnews', 
    'finance-saving-investing', 'soccer', 'viral', 'finance-taxes', 'foodnews', 
    'lifestyleshopping', 'lifestylebeauty', 'newsopinion', 'finance-companies', 
    'newscrime', 'finance-savemoney', 'mentalhealth', 'lifestylesmartliving', 
    'autosclassics', 'traveltips', 'shop-toys', 'autosluxury', 'finance-career', 
    'entertainment-books', 'newsgoodnews', 'retirement', 'lifestyleweddings', 
    'lifestylehomeandgarden', 'ads-lung-health', 'personalfinance', 'finance-top-stocks', 
    'soccer_epl', 'lifestyledecor', 'causes', 'autoshybrids', 'newsoffbeat', 
    'lifestylefashion', 'tennis', 'videos', 'lifestylepets', 'weight-loss', 
    'lifestylecareer', 'markets', 'shop-holidays', 'icehockey_nhl', 'finance-credit', 
    'movievideo', 'football_nfl_videos', 'movies-celebrity', 'finance-billstopay', 
    'lifestylecleaningandorganizing', 'lifestylecelebstyle', 'newsweather', 'popculture', 
    'beverages', 'basketball_wnba', 'lifestylefamilyandrelationships', 'music-gallery', 
    'entertainment-celebrity', 'advice', 'musicvideos', 'strength', 'autosmotorcycles', 
    'healthagingwell', 'video', 'outdoors', 'wines', 'healthnews', 'causes-green-living', 
    'autosresearchguides', 'factcheck', 'lifestyle-news-feature', 'music-celebrity', 
    'lifestyle', 'baseball_mlb_videos', 'lifestylediy', 'science', 'movienews', 
    'travel-videos', 'football_ncaa_videos', 'lifestylefamily', 'autosownership', 
    'lifestylehoroscopefish', 'shop-home-goods', 'downtime', 'newsfactcheck', 
    'travel-points-rewards', 'humor', 'finance-small-business', 'autospassenger', 
    'autossema', 'fun', 'boxing', 'peopleandplaces', 'finance-video', 'soccer_mls', 
    'lifestylerelationships', 'foodrecipes', 'lifestylevideo', 'holidays', 
    'finance-healthcare', 'music-awards', 'seasonal', 'hollywood', 'tunedin', 
    'tv-recaps', 'boxing-mma', 'tvvideos', 'autosreview', 'empowering-the-planet', 
    'causes-animals', 'lifestyletravel', 'finance-technology', 'lifestylemarriage', 
    'finance-home-loans', 'autosvideonew', 'soccer_videos', 'finance-mutual-funds', 
    'games', 'relationships', 'causes-food-insecurity', 'autoscartech', 'movies-oscars', 
    'travel-adventure-travel', 'watch', 'technologyinvesting', 
    'shop-computers-electronics', 'celebritynews', 'autostokyo', 'elections-2020-us', 
    'pregnancyparenting', 'causes-poverty', 'music-grammys', 'lifestyleanimals', 
    'lifestyle-wedding', 'music-reviews', 'finance-savingsrates', 'autosresearch', 
    'sports', 'career-news', 'newsscience', 'reviews', 'basketball_ncaa_videos', 
    'autosconvertibles', 'autoscompact', 'travel-accessible', 'finance-education', 
    'ads-latingrammys', 'finance-insidetheticker', 'olympics-videos', 'awards', 
    'golfvideos', 'autosvans', 'people-places', 'autosvideos', 'smartliving', 
    'newslocalpolitics', 'sports_news', 'familyhealth', 'middleeast-top-stories', 
    'causes-environment', 'cocktails', 'newstvmedia', 'healthandfitness', 
    'newstechnology', 'photos', 'other', 'mindandbody', 'cookingschool', 
    'basketball_nba_videos', 'mmaufc', 'tv-reviews', 'narendramodi_opinion', 
    'finance-homesandpropertysection', 'tv', 'cooking', 'games-news', 'newsnational', 
    'halloween', 'movies-awards', 'awardstyle', 'company-news', 'newsworldpolitics', 
    'othersports', 'yearinoffbeatgoodnews', 'newsrealestate', 
    'lifestyleshoppinghomegarden', 'wonder', 'cma-awards', 'technology', 'newsvideo', 
    'comedy', 'travel', 'baseball', 'topnews', 'newsother', 'foodtips', 
    'tv-golden-globes', 'causes-disaster-relief', 'finance-auto-insurance', 
    'weatherfullscreenmaps', 'causes-military-appreciation', 'newsvideos', 'indepth', 
    'healthyliving', 'lifestylewhatshot', 'lifestylestyle', 'shop-books-movies-tv', 
    'health-cancer', 'lifestyledesign', 'newselection2020', 'finance-startinvesting', 
    'spendingandborrowing', 'ustravel', 'basketball', 'internationaltravel', 
    'traveltrivia', 'soccer_bund', 'tv-golden-globes-video', 'foodanddrink', 
    'tennis_intl', 'entertainmentmusic', 'northamerica-video', 'autosmidsize', 
    'soccer_fifa_wwc', 'entertainmenttv', 'autoslosangeles', 'celebhub']

available_interaction_types = ["click", "noclick", "like", "dislike", "share", "report"]
available_article_types = ["feature", "gallery", "video", "live_blog"]


InteractionsDataSchema = pa.DataFrameSchema({
    "DATASET_NAME": pa.Column(str, pa.Check.str_length(min_value=3, max_value=25)),
    "USER_ID": pa.Column(str, pa.Check.str_length(min_value=2, max_value=25)), #imported intercations datasets will have thir own users di in it
    "ITEM_ID": pa.Column(str, pa.Check.str_length(min_value=2, max_value=10)), #relationship checking #dont need item id from given dataset
    "TIMESTAMP": pa.Column(str), #check format of mind and ebnerd
    "INTERACTION_TYPE": pa.Column(str, pa.Check.isin(available_interaction_types)),
    "READ_TIME": pa.Column(float, pa.Check.in_range(0, 18000), nullable=True), #In seconds
    "SCROLL_PERCENTAGE": pa.Column(float, pa.Check.in_range(0.0, 100.0), nullable=True)
}, strict="filter", ordered=True)


ItemsDataSchema = pa.DataFrameSchema({
    "DATASET_NAME": pa.Column(str, pa.Check.str_length(min_value=3, max_value=25)),
    "ITEM_ID": pa.Column(str, pa.Check.str_length(min_value=2, max_value=10)),
    "CATEGORY": pa.Column(str, pa.Check.isin(available_news_categories)),
    "SUB_CATEGORY": pa.Column(str, pa.Check.isin(available_news_sub_categories)), #find categories form mind and ebnerd and make it extensible
    "TITLE": pa.Column(str, pa.Check.str_length(max_value=150)),
    "ABSTRACT": pa.Column(str, pa.Check.str_length(min_value=5)),
    "TIMESTAMP": pa.Column(str), #check format of mind and ebnerd
    "ARTICLE_TYPE": pa.Column(str, pa.Check.isin(available_article_types)) #comes from Eb-nerd articles.parquet make this increase able
    }, strict="filter", ordered=True)


dataset_schema_mapping = {
        "Interactions": InteractionsDataSchema,
        "Content": ItemsDataSchema
    }
