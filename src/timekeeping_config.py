NODE_CONFIG = [
    {
        "node": "KEY",
        "path": ".//KEY",
        "key_fields": ["c"],
        "display_path": "Poll/KEYS/KEY",
    },
    {
        "node": "H1",
        "path": ".//H0/H1",
        "key_fields": ["id"],
        "display_path": "Poll/H0/H1",
    },
    {
        "node": "NV",
        "path": ".//H0/H1/NV",
        "key_fields": ["n"],
        "display_path": "Poll/H0/H1/NV",
    },
    {
        "node": "JOBCODE",
        "path": ".//Labor/JobCodes/J",
        "key_fields": ["c"],
        "display_path": "Poll/Labor/JobCodes/J",
    },
    {
        "node": "DAILY",
        "path": ".//TM0[@type='DAILY']/TM1",
        "key_fields": ["e", "j", "dt"],
        "display_path": "Poll/Labor/TM0(type=DAILY)/TM1",
    },
    {
        "node": "EXCEPTIONS",
        "path": ".//TM0[@type='EXCEPTIONS']/TM1",
        "key_fields": ["e", "j", "in"],
        "display_path": "Poll/Labor/TM0(type=EXCEPTIONS)/TM1",
    },
    {
        "node": "SHIFT",
        "path": ".//TM0[@type='SHIFT']/TM1",
        "key_fields": ["e", "j", "dt", "in"],
        "display_path": "Poll/Labor/TM0(type=SHIFT)/TM1",
    },
    {
        "node": "WEEKLY",
        "path": ".//TM0[@type='WEEKLY']/TM1",
        "key_fields": ["e", "j", "dt"],
        "display_path": "Poll/Labor/TM0(type=WEEKLY)/TM1",
    },
]
