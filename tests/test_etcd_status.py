import unittest

from analysis.etcd_status import leader_container_name


class EtcdStatusTests(unittest.TestCase):
    def test_leader_container_name_detects_endpoint_for_leader_member(self):
        payload = [
            {
                "Endpoint": "http://etcd1:2379",
                "Status": {"header": {"member_id": 1}, "leader": 2},
            },
            {
                "Endpoint": "http://etcd2:2379",
                "Status": {"header": {"member_id": 2}, "leader": 2},
            },
            {
                "Endpoint": "http://etcd3:2379",
                "Status": {"header": {"member_id": 3}, "leader": 2},
            },
        ]

        self.assertEqual(leader_container_name(payload), "etcd2")


if __name__ == "__main__":
    unittest.main()
