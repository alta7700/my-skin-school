from urllib import parse


def change_qsl(url: str, remove: str | tuple[str] = None, add: dict[str, str | int] = None):
    if not (remove or add):
        return url
    url = parse.urlparse(url)
    q = {key: value for key, value in parse.parse_qsl(url.query)}
    if remove:
        remove = (remove, ) if isinstance(remove, str) else remove
        for key in remove:
            try:
                del q[key]
            except KeyError:
                pass
    if add:
        q = {**q, **add}
    return url._replace(query="&".join(f"{x}={y}" for x, y in q.items())).geturl()
