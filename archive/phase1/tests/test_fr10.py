"""FR-10: API Response Format — ApiResponse / PaginatedResponse.

[FR-10] Acceptance criteria:
  - ApiResponse contains success / data / error / error_code
  - PaginatedResponse inherits ApiResponse, adds total / page / limit / has_next
  - ErrorCode enum: AUTH_INVALID_SIGNATURE, RATE_LIMIT_EXCEEDED,
    KNOWLEDGE_NOT_FOUND, VALIDATION_ERROR, INTERNAL_ERROR

Citations: SRS.md FR-10 section, SAD.md 2.5.2
"""

from omnibot.api import ApiResponse, PaginatedResponse, ErrorCode


def test_api_response_success():
    """ApiResponse with success=True and data."""
    resp = ApiResponse(success=True, data={"id": 1})
    assert resp.success is True
    assert resp.data == {"id": 1}
    assert resp.error is None
    assert resp.error_code is None


def test_api_response_error():
    """ApiResponse with success=False and error details."""
    resp = ApiResponse(
        success=False,
        error="Signature invalid",
        error_code=ErrorCode.AUTH_INVALID_SIGNATURE,
    )
    assert resp.success is False
    assert resp.data is None
    assert resp.error == "Signature invalid"
    assert resp.error_code == ErrorCode.AUTH_INVALID_SIGNATURE


def test_api_response_defaults():
    """ApiResponse defaults: data/error/error_code are None."""
    resp = ApiResponse(success=True)
    assert resp.data is None
    assert resp.error is None
    assert resp.error_code is None


def test_api_response_generic_typed():
    """ApiResponse is generic over data type."""
    resp: ApiResponse[dict] = ApiResponse(success=True, data={"key": "val"})
    assert resp.data["key"] == "val"


def test_paginated_response_inherits_api():
    """PaginatedResponse inherits from ApiResponse."""
    resp = PaginatedResponse(
        success=True,
        data=[1, 2, 3],
        total=100,
        page=2,
        limit=20,
    )
    assert isinstance(resp, ApiResponse)
    assert resp.success is True
    assert resp.data == [1, 2, 3]


def test_paginated_response_fields():
    """PaginatedResponse has total/page/limit/has_next."""
    resp = PaginatedResponse(
        success=True,
        data=["a", "b"],
        total=50,
        page=1,
        limit=10,
    )
    assert resp.total == 50
    assert resp.page == 1
    assert resp.limit == 10
    assert resp.has_next is True  # page 1 of 5


def test_paginated_response_no_next_page():
    """has_next is False on last page."""
    resp = PaginatedResponse(
        success=True,
        data=[],
        total=0,
        page=1,
        limit=20,
    )
    assert resp.has_next is False


def test_paginated_response_error():
    """PaginatedResponse can carry error info like ApiResponse."""
    resp = PaginatedResponse(
        success=False,
        error="Validation failed",
        error_code=ErrorCode.VALIDATION_ERROR,
    )
    assert resp.success is False
    assert resp.error == "Validation failed"


def test_error_code_enum_values():
    """ErrorCode enum has all required members."""
    assert ErrorCode.AUTH_INVALID_SIGNATURE.value == "AUTH_INVALID_SIGNATURE"
    assert ErrorCode.RATE_LIMIT_EXCEEDED.value == "RATE_LIMIT_EXCEEDED"
    assert ErrorCode.KNOWLEDGE_NOT_FOUND.value == "KNOWLEDGE_NOT_FOUND"
    assert ErrorCode.VALIDATION_ERROR.value == "VALIDATION_ERROR"
    assert ErrorCode.INTERNAL_ERROR.value == "INTERNAL_ERROR"


def test_error_code_from_string():
    """ErrorCode can be constructed from string."""
    assert ErrorCode("AUTH_INVALID_SIGNATURE") == ErrorCode.AUTH_INVALID_SIGNATURE
    assert ErrorCode("INTERNAL_ERROR") == ErrorCode.INTERNAL_ERROR


def test_serialization_round_trip():
    """ApiResponse can serialize to JSON and parse back."""
    resp = ApiResponse(success=True, data={"id": 42})
    raw = resp.model_dump()
    assert raw == {"success": True, "data": {"id": 42}, "error": None, "error_code": None}
    parsed = ApiResponse.model_validate(raw)
    assert parsed.success == resp.success
    assert parsed.data == resp.data


def test_paginated_response_middle_page():
    """has_next is True for middle page, False on last."""
    # page 3 of 5 (total 50, 10 per page)
    resp = PaginatedResponse(success=True, data=list(range(10)), total=50, page=3, limit=10)
    assert resp.has_next is True
    # page 5 of 5 (last page)
    resp = PaginatedResponse(success=True, data=list(range(10)), total=50, page=5, limit=10)
    assert resp.has_next is False
    # page 6 (beyond total) — still False
    resp = PaginatedResponse(success=True, data=[], total=50, page=6, limit=10)
    assert resp.has_next is False
