NODE_CONFIG = [
    {
        "node": "H1",
        "path": ".//H0/H1",
        "key_fields": ["id"],
        "display_path": "Poll/H0/H1",
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
        "key_fields": ["e", "j"],
        "display_path": "Poll/Labor/TM0(type=DAILY)/TM1",
    },
    {
        "node": "SHIFT",
        "path": ".//TM0[@type='SHIFT']/TM1",
        "key_fields": ["e", "j", "in"],
        "display_path": "Poll/Labor/TM0(type=SHIFT)/TM1",
    },
    {
        "node": "EXCEPTIONS",
        "path": ".//TM0[@type='EXCEPTIONS']/TM1",
        "key_fields": ["e", "j", "in"],
        "display_path": "Poll/Labor/TM0(type=EXCEPTIONS)/TM1",
    },
    {
        "node": "WEEKLY",
        "path": ".//TM0[@type='WEEKLY']/TM1",
        "key_fields": ["e", "j"],
        "display_path": "Poll/Labor/TM0(type=WEEKLY)/TM1",
    },
{
    "node": "PAY_PERIOD",
    "path": ".//TM0[@type='PAY_PERIOD']/TM1",
    "key_fields": ["e", "j", "dt", "r"],
    "display_path": "Poll/Labor/TM0(type=PAY_PERIOD)/TM1",
}
]
