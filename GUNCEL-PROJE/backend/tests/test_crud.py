"""CRUD birim testleri."""

from __future__ import annotations

from uuid import uuid4

from app.db.crud.base_crud import row_to_dict


class TestBaseCrud:
    def test_row_to_dict_uuid(self):
        uid = uuid4()
        result = row_to_dict({"id": uid, "name": "test"})
        assert result["id"] == str(uid)
        assert result["name"] == "test"

    def test_row_to_dict_none(self):
        assert row_to_dict(None) is None
