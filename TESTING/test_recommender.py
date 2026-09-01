import pandas as pd

from RECSYS_V2_RECOMMENDER.RContentBasedFiltering import CategoryMeanRecommender


def _synthetic_content_df():
    return pd.DataFrame([
        {
            "DATASET_NAME": "mind",
            "ITEM_ID": "N1",
            "CATEGORY": "news",
            "SUB_CATEGORY": "newsworld",
            "TITLE": "World leaders meet",
            "ABSTRACT": "world leaders meet to discuss global politics and economy",
            "TIMESTAMP": "2024-01-01",
            "ARTICLE_TYPE": "feature",
        },
        {
            "DATASET_NAME": "mind",
            "ITEM_ID": "N2",
            "CATEGORY": "news",
            "SUB_CATEGORY": "newsworld",
            "TITLE": "Election results",
            "ABSTRACT": "election results announced across the country amid politics",
            "TIMESTAMP": "2024-01-02",
            "ARTICLE_TYPE": "feature",
        },
        {
            "DATASET_NAME": "mind",
            "ITEM_ID": "S1",
            "CATEGORY": "sports",
            "SUB_CATEGORY": "football_nfl",
            "TITLE": "Championship game recap",
            "ABSTRACT": "the championship football game ended with a dramatic win",
            "TIMESTAMP": "2024-01-03",
            "ARTICLE_TYPE": "feature",
        },
        {
            "DATASET_NAME": "mind",
            "ITEM_ID": "S2",
            "CATEGORY": "sports",
            "SUB_CATEGORY": "basketball_nba",
            "TITLE": "Basketball season preview",
            "ABSTRACT": "basketball season preview with team rankings and predictions",
            "TIMESTAMP": "2024-01-04",
            "ARTICLE_TYPE": "feature",
        },
    ])


def test_recommend_returns_all_items_ranked_for_one_preferred_category():
    recommender = CategoryMeanRecommender()
    df = _synthetic_content_df()
    recommender.fit(df)

    recommended_ids = recommender.recommend(["news"])

    # Every item in the catalogue should come back, just ranked - and the
    # two "news" items should be ranked above both "sports" items.
    assert set(recommended_ids) == {"N1", "N2", "S1", "S2"}
    ranked_list = list(recommended_ids)
    news_positions = [ranked_list.index("N1"), ranked_list.index("N2")]
    sports_positions = [ranked_list.index("S1"), ranked_list.index("S2")]
    assert max(news_positions) < min(sports_positions)


def test_recommend_returns_all_items_ranked_for_two_preferred_categories():
    recommender = CategoryMeanRecommender()
    df = _synthetic_content_df()
    recommender.fit(df)

    recommended_ids = recommender.recommend(["news", "sports"])

    # With both categories preferred, recommendations should still be
    # produced without error and should still cover the full catalogue.
    assert set(recommended_ids) == {"N1", "N2", "S1", "S2"}
    assert len(recommended_ids) == len(df)
