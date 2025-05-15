import pytest
from unittest.mock import MagicMock, patch

# Example unit test for demonstration purposes
# Replace with actual unit tests for your application

# Sample function to test
def add_numbers(a, b):
    return a + b


class TestSample:
    """Sample test class to demonstrate pytest usage."""

    def test_add_numbers(self):
        """Test the add_numbers function."""
        # Arrange
        a, b = 1, 2
        expected = 3
        
        # Act
        result = add_numbers(a, b)
        
        # Assert
        assert result == expected

    @pytest.mark.parametrize(
        "a,b,expected",
        [
            (1, 2, 3),
            (0, 0, 0),
            (-1, 1, 0),
            (100, -50, 50),
        ],
    )
    def test_add_numbers_parametrized(self, a, b, expected):
        """Test the add_numbers function with multiple inputs."""
        result = add_numbers(a, b)
        assert result == expected

    def test_with_mock(self, mocker):
        """Test using the mocker fixture to mock dependencies."""
        # Create a mock object
        mock_obj = mocker.MagicMock()
        mock_obj.some_method.return_value = 42
        
        # Use the mock
        result = mock_obj.some_method()
        
        # Assert
        assert result == 42
        mock_obj.some_method.assert_called_once()

    @pytest.mark.asyncio
    async def test_async_function(self):
        """Test an asynchronous function."""
        # Define an async function to test
        async def async_add(a, b):
            return a + b
        
        # Call the async function and await it
        result = await async_add(3, 4)
        
        # Assert
        assert result == 7 