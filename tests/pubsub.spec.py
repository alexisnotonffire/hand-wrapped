import pytest

class testPubSub(object):
    def testSub():
        assert False

    def testSubFailure():
        assert False

    def testPub():
        assert False

    def testPubFailure():
        assert False

    def testSchemaForce():
        schema = {
            'timestamp': None,
            'artist': None,
            'album': None,
            'track': None,
            'playlist': None,
            'length': None,
            'skipped': None
        }
        assert schemaForce() == schema
    cases = [
        (0, 'input is not a schema'),
        ('0', 'input is not a schema'),
        ([0], 'input is not a schema'),
        ({0:0}, 'input is not a schema'),
    ]
    @pytest.mark.parametrize("var,exp", cases)
    def testSchemaForceType():
        with pytest.raises(SchemaError):
            schemaForce()
        assert
