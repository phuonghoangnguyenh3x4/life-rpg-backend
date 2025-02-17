def get_limit_offset(page: int, per_page: int):
    limit = per_page
    offset = (page - 1) * per_page
    return (limit, offset)