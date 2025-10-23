import pytest


@pytest.fixture(params=[[1, 2, 3], [1, 1, 4], [2, 1, 3]], scope="session")
def sample_data(request):
    print("\nCreate sample data")
    yield request.param
    print("\nClose sample data")
