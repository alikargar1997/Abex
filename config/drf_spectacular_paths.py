def preprocessing_filter_spec(endpoints):
    """
    Filters the list of API endpoints to only include those that start with "/v1/exchange/" or "/v1/auth/".

    This function is used to preprocess the list of API endpoints before generating the API documentation. It ensures that only the relevant endpoints are included in the documentation.

    Args:
        endpoints (list): A list of tuples, where each tuple contains the path, path regex, HTTP method, and callback function for an API endpoint.

    Returns:
        list: A filtered list of API endpoints that start with "/v1/exchange/" or "/v1/auth/".
    """
    
    filtered = []
    for path, path_regex, method, callback in endpoints:
        if path.startswith("/v1/exchanges/") or path.startswith("/v1/auth/"):
            filtered.append((path, path_regex, method, callback))
    return filtered
