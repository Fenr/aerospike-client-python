# -*- coding: utf-8 -*-

import pytest
import sys
import time
from test_base_class import TestBaseClass

try:
    import aerospike
except:
    print "Please install aerospike python client."
    sys.exit(1)

class TestQueryRole(TestBaseClass):

    def setup_method(self, method):

        """
        Setup method
        """
        hostlist, user, password = TestBaseClass().get_hosts()
        config = {
                "hosts": hostlist
                }
        self.client = aerospike.client(config).connect( user, password )

        self.client.admin_create_role("usr-sys-admin", [{"code": aerospike.USER_ADMIN}, {"code": aerospike.SYS_ADMIN}])
        self.delete_users = []

    def teardown_method(self, method):

        """
        Teardown method
        """

        policy = {}

        self.client.admin_drop_role("usr-sys-admin")
        self.client.close()

    def test_admin_query_role_no_parameters(self):
        """
        Query role with no parameters
        """
        with pytest.raises(TypeError) as typeError:
            self.client.admin_query_role()

        assert "Required argument 'role' (pos 1) not found" in typeError.value

    def test_admin_query_role_positive(self):
        """
            Query role positive
        """
        roles = self.client.admin_query_role("usr-sys-admin")
        assert roles[0]['privileges'] == [{'code': 0, 'ns': '', 'set': ''},
{'code': 1, 'ns': '', 'set': ''}]

    def test_admin_query_role_positive_with_policy(self):
        """
            Query role positive policy
        """
        roles = self.client.admin_query_role("usr-sys-admin", {'timeout': 1000})
        assert roles[0]['privileges'] == [{'code': 0, 'ns': '', 'set': ''},
{'code': 1, 'ns': '', 'set': ''}]

    def test_admin_query_role_incorrect_role_name(self):
        """
            Incorrect role name
        """
        with pytest.raises(Exception) as exception:
            self.client.admin_query_role("usr-sys-admin-non-existent", {'timeout': 1000})

        assert exception.value[0] == 70
        assert exception.value[1] == "AEROSPIKE_INVALID_ROLE"

    def test_admin_query_role_incorrect_role_type(self):
        """
            Incorrect role type
        """
        with pytest.raises(Exception) as exception:
            self.client.admin_query_role(None, {'timeout': 1000})

        assert exception.value[0] == -2
        assert exception.value[1] == "Role name should be a string"
