from .GitObject import GitObject

class CommitObject(GitObject):
    def __init__(self, data=None):
        self.fmt = b'commit'
        super().__init__(data)

    def init(self):
        self.commitdata = dict()

    def serialize(self):
        return commit_serialize(self.commitdata)


    def deserialize(self, obj):
        self.commitdata = commit_parse(obj)


def commit_serialize(commit):
    """
    Build the commit object
    """
    data = b''
    for key,value in commit:
        # Normalize value to a list
        if type(value) != list:
            value = [value]

        for v in value:
            data += key + b' ' + v.replace(b'\n', b'\n ') + b'\n'

    data += b'\n' + commit[None]

    return data


def commit_parse(obj, start_idx, dictionary = None):
    """
'tree 29ff16c9c14e2652b22f8b78bb08a5a07930c147
parent 206941306e8a8af65b66eaaaea388a7ae24d49a0
author Thibault Polge <thibault@thb.lt> 1527025023 +0200
committer Thibault Polge <thibault@thb.lt> 1527025044 +0200
gpgsig -----BEGIN PGP SIGNATURE-----

 iQIzBAABCAAdFiEExwXquOM8bWb4Q2zVGxM2FxoLkGQFAlsEjZQACgkQGxM2FxoL
 kGQdcBAAqPP+ln4nGDd2gETXjvOpOxLzIMEw4A9gU6CzWzm+oB8mEIKyaH0UFIPh
 rNUZ1j7/ZGFNeBDtT55LPdPIQw4KKlcf6kC8MPWP3qSu3xHqx12C5zyai2duFZUU
 wqOt9iCFCscFQYqKs3xsHI+ncQb+PGjVZA8+jPw7nrPIkeSXQV2aZb1E68wa2YIL
 3eYgTUKz34cB6tAq9YwHnZpyPx8UJCZGkshpJmgtZ3mCbtQaO17LoihnqPn4UOMr
 V75R/7FjSuPLS8NaZF4wfi52btXMSxO/u7GuoJkzJscP3p4qtwe6Rl9dc1XC8P7k
 NIbGZ5Yg5cEPcfmhgXFOhQZkD0yxcJqBUcoFpnp2vu5XJl2E5I/quIyVxUXi6O6c
 /obspcvace4wy8uO0bdVhc4nJ+Rla4InVSJaUaBeiHTW8kReSFYyMmDCzLjGIu1q
 doU61OM3Zv1ptsLu3gUE6GU27iWYj2RWN3e3HE4Sbd89IFwLXNdSuM0ifDLZk7AQ
 WBhRhipCCgZhkj9g2NEk7jRVslti1NdN5zoQLaJNqSwO1MtxTmJ15Ksk3QP6kfLB
 Q52UWybBzpaP9HEd4XnR+HuQ4k2K0ns2KgNImsNvIyFwbpMUyUWLMPimaV1DWUXo
 5SBjDB/V/W2JBFR+XKHFJeFwYhj7DD/ocsGr4ZMx/lgc8rjIBkI=
 =lgTX
 -----END PGP SIGNATURE-----

Create first draft'

Deconstruct the commit object into a dictionary
"""
    # Find the index of the first space and first new line
    space_idx = obj.find(b' ', start_idx)
    new_line_idx = obj.find(b'\n', start_idx)

    # Base case
    if space_idx < 0 or new_line_idx < space_idx:
        dictionary[None] = obj[start_idx+1:]
        return dictionary

    key = obj[start_idx:space_idx]

    # Find the end of the value field
    value_end = start_idx
    while True:
        # Update the end index to be the next new line char
        value_end = obj.find(b'\n', value_end+1)
        # If the idx after the new line char is not a space, break out of the loop
        if obj[value_end+1] != ord(' '):
            break

    
    value = obj[space_idx+1:value_end].replace(b'\n ', b'\n')

    if key in dictionary:
        # If a list of values already exists
        if type(dictionary[key]) == list:
            dictionary[key].append(value)
        # Convert single value to a list and add the new value
        else:
            dictionary[key] = [dictionary[key], value]
    else:
        dictionary[key] = value


    return commit_parse(obj, value_end+1, dictionary)
