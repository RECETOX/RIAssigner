import pytest

from tests.builders import ValidateSimpleDataBuilder



# @pytest.mark.parametrize("retention_times, retention_indices, expected", [
#     ([None, 45.9], None,"Retention time data is invalid."), # contains None
#     ([-24.9, 100.2], None,"Retention time data is invalid."), # contains negative rt
#     (("200.3", 56.7), None,"Retention time data is invalid."), # contains string
#     ([2056.8, 100], None, "Retention time data has to be sorted."), # is not sorted
#     ([12.0, 100.9], [100], "Retention times and index data are of different length."),
#     ([12.0, 100.9], [200, 100], "Retention indices data has to be sorted.")
# ])
# def test_constructor_exception(retention_times, retention_indices, expected):
#     with pytest.raises(ValueError) as exception:
#         builder = ValidateSimpleDataBuilder().with_rt(retention_times).with_ri(retention_indices)
#         builder.build()

#     message = exception.value.args[0]
#     assert message == expected, message


@pytest.mark.parametrize("retention_times, retention_indices, expected", [
    ([None, 45.9], None, (TypeError, "Retention times must be a list and cannot contain None.")), # contains None
    ([-24.9, 100.2], None, (ValueError, "Retention time data is invalid.")), # contains negative rt
    (["200.3", 56.7], None, (ValueError, "Retention time data is invalid.")), # contains string
    ([2056.8, 100], None, (ValueError, "Retention time data has to be sorted.")), # is not sorted
    ([12.0, 100.9], [100], (ValueError, "Retention times and index data are of different length.")),
    ([12.0, 100.9], [200, 100], (ValueError, "Retention indices data has to be sorted."))
])
def test_constructor_exception(retention_times, retention_indices, expected):
    with pytest.raises(expected[0]) as exception:
        builder = ValidateSimpleDataBuilder().with_rt(retention_times).with_ri(retention_indices)
        builder.build()

    message = exception.value.args[0]
    assert message == expected[1], message