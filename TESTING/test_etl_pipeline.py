import pandas as pd
import pytest
from unittest.mock import MagicMock

from RECSYS_V2_ETL_PIPELINE.T2.T2_STEP1_FILE_CHECKS import file_loading
from RECSYS_V2_ETL_PIPELINE.T2.T2_STEP2_SCHEMA_VALIDATION import dataset_schema_validation
from RECSYS_V2_ETL_PIPELINE.T2.T2_STEP3_INSERT_DATASET import remove_duplicates_and_insert
from RECSYS_V2_API.Security.exceptions import schema_validation_error as SchemaValidationError


def _valid_interaction_row(**overrides):
    row = dict(
        DATASET_NAME="mind_dataset",
        USER_ID="U1",
        ITEM_ID="N1",
        TIMESTAMP="2024-01-01 00:00:00",
        INTERACTION_TYPE="click",
        READ_TIME=10.5,
        SCROLL_PERCENTAGE=50.0,
    )
    row.update(overrides)
    return row


def test_dataset_upload_loads_validates_and_inserts_a_valid_csv(tmp_path):
    csv_path = tmp_path / "interactions.csv"
    df_in = pd.DataFrame([_valid_interaction_row()])
    df_in.to_csv(csv_path, index=False)

    loaded = file_loading(str(csv_path))
    assert isinstance(loaded, pd.DataFrame)
    assert len(loaded) == 1

    validated = dataset_schema_validation(loaded, "Interactions")
    assert len(validated) == 1

    mock_db = MagicMock()
    mock_db.execute.return_value = MagicMock(rowcount=1)
    inserted_rowcount = remove_duplicates_and_insert(validated, "Interactions", mock_db)

    assert inserted_rowcount == 1
    mock_db.commit.assert_called_once()
    mock_db.rollback.assert_not_called()


def test_dataset_schema_validation_rejects_invalid_rows_before_insert():
    df = pd.DataFrame([_valid_interaction_row(INTERACTION_TYPE="not_a_real_type")])

    with pytest.raises(SchemaValidationError):
        dataset_schema_validation(df, "Interactions")
