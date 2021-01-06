"""
Setup expectations for test sub classes
Run discovery for as a prerequisite for most tests
"""
import unittest
import os

from tap_tester import connections, menagerie, runner


class MambuBaseTest(unittest.TestCase):
    """
    Setup expectations for test sub classes
    Run discovery for as a prerequisite for most tests
    """
    AUTOMATIC_FIELDS = "automatic"
    REPLICATION_KEYS = "valid-replication-keys"
    PRIMARY_KEYS = "table-key-properties"
    FOREIGN_KEYS = "table-foreign-key-properties"
    REPLICATION_METHOD = "forced-replication-method"
    API_LIMIT = "max-row-limit"
    INCREMENTAL = "INCREMENTAL"
    FULL_TABLE = "FULL_TABLE"
    START_DATE_FORMAT = "%Y-%m-%dT00:00:00Z"

    @staticmethod
    def tap_name():
        """The name of the tap"""
        return "tap-mambu"

    @staticmethod
    def get_type():
        """the expected url route ending"""
        return "platform.mambu"

    def expected_streams(self):
        """A set of expected stream names"""
        return set(self.expected_metadata().keys())

    def expected_metadata(self):
        return {
            "branches": {
                self.PRIMARY_KEYS: {
                    "id"
                },
                self.REPLICATION_METHOD: "INCREMENTAL",
                self.REPLICATION_KEYS: {
                    "last_modified_date"
                }
            },
            "cards": {
                self.PRIMARY_KEYS: {
                    "deposit_id",
                    "reference_token"
                },
                self.REPLICATION_METHOD: "FULL_TABLE",
            },
            "communications": {
                self.PRIMARY_KEYS: {
                    "encoded_key"
                },
                self.REPLICATION_METHOD: "INCREMENTAL",
                self.REPLICATION_KEYS: {
                    "creation_date"
                }
            },
            "centres": {
                self.PRIMARY_KEYS: {
                    "id"
                },
                self.REPLICATION_METHOD: "INCREMENTAL",
                self.REPLICATION_KEYS: {
                    "last_modified_date"
                }
            },
            "clients": {
                self.PRIMARY_KEYS: {
                    "id"
                },
                self.REPLICATION_METHOD: "INCREMENTAL",
                self.REPLICATION_KEYS: {
                    "last_modified_date"
                }
            },
            "credit_arrangements": {
                self.PRIMARY_KEYS: {
                    "id"
                },
                self.REPLICATION_METHOD: "INCREMENTAL",
                self.REPLICATION_KEYS: {
                    "last_modified_date"
                }
            },
            "custom_field_sets": {
                self.PRIMARY_KEYS: {
                    "id"
                },
                self.REPLICATION_METHOD: "FULL_TABLE",
            },
            "deposit_accounts": {
                self.PRIMARY_KEYS: {
                    "id"
                },
                self.REPLICATION_METHOD: "INCREMENTAL",
                self.REPLICATION_KEYS: {
                    "last_modified_date"
                }
            },
            "deposit_products": {
                self.PRIMARY_KEYS: {
                    "id"
                },
                self.REPLICATION_METHOD: "INCREMENTAL",
                self.REPLICATION_KEYS: {
                    "last_modified_date"
                }
            },
            "deposit_transactions": {
                self.PRIMARY_KEYS: {
                    "encoded_key"
                },
                self.REPLICATION_METHOD: "INCREMENTAL",
                self.REPLICATION_KEYS: {
                    "creation_date"
                }
            },
            "groups": {
                self.PRIMARY_KEYS: {
                    "id"
                },
                self.REPLICATION_METHOD: "INCREMENTAL",
                self.REPLICATION_KEYS: {
                    "last_modified_date"
                }
            },
            "loan_accounts": {
                self.PRIMARY_KEYS: {
                    "id"
                },
                self.REPLICATION_METHOD: "INCREMENTAL",
                self.REPLICATION_KEYS: {
                    "last_modified_date"
                }
            },
            "loan_repayments": {
                self.PRIMARY_KEYS: {
                    "encoded_key"
                },
                self.REPLICATION_METHOD: "FULL_TABLE",
            },
            "loan_products": {
                self.PRIMARY_KEYS: {
                    "id"
                },
                self.REPLICATION_METHOD: "INCREMENTAL",
                self.REPLICATION_KEYS: {
                    "last_modified_date"
                }
            },
            "loan_transactions": {
                self.PRIMARY_KEYS: {
                    "encoded_key"
                },
                self.REPLICATION_METHOD: "INCREMENTAL",
                self.REPLICATION_KEYS: {
                    "creation_date"
                }
            },
            "tasks": {
                self.PRIMARY_KEYS: {
                    "id"
                },
                self.REPLICATION_METHOD: "INCREMENTAL",
                self.REPLICATION_KEYS: {
                    "last_modified_date"
                }
            },
            "users": {
                self.PRIMARY_KEYS: {
                    "id"
                },
                self.REPLICATION_METHOD: "INCREMENTAL",
                self.REPLICATION_KEYS: {
                    "last_modified_date"
                }
            },
            "gl_accounts": {
                self.PRIMARY_KEYS: {
                    "gl_code"
                },
                self.REPLICATION_METHOD: "INCREMENTAL",
                self.REPLICATION_KEYS: {
                    "last_modified_date"
                }
            },
            "gl_journal_entries": {
                self.PRIMARY_KEYS: {
                    "entry_id"
                },
                self.REPLICATION_METHOD: "INCREMENTAL",
                self.REPLICATION_KEYS: {
                    "booking_date"
                }
            },
            "activities": {
                self.PRIMARY_KEYS: {
                    "encoded_key"
                },
                self.REPLICATION_METHOD: "INCREMENTAL",
                self.REPLICATION_KEYS: {
                    "timestamp"
                }
            },
            "index_rate_sources": {
                self.PRIMARY_KEYS: {
                    "encoded_key"
                },
                self.REPLICATION_METHOD: "FULL_TABLE",
            },
            "installments": {
                self.PRIMARY_KEYS: {
                    "encoded_key"
                },
                self.REPLICATION_METHOD: "INCREMENTAL",
                self.REPLICATION_KEYS: {
                    "last_paid_date"
                }
            }
        }


    def create_connection(self, original_properties: bool = True):
        """Create a new connection with the test name"""
        # Create the connection
        conn_id = connections.ensure_connection(self, original_properties)

        # Run a check job using orchestrator (discovery)
        check_job_name = runner.run_check_mode(self, conn_id)

        # Assert that the check job succeeded
        exit_status = menagerie.get_exit_status(conn_id, check_job_name)
        menagerie.verify_check_exit_status(self, exit_status, check_job_name)
        return conn_id

    def get_properties(self):
        return {
            'start_date': '2019-01-01T00:00:00Z',
            "username": os.environ['TAP_MAMBU_USERNAME'],
            "subdomain": os.environ['TAP_MAMBU_SUBDOMAIN']
            }

    def get_credentials(self):
        return {
            "password": os.environ['TAP_MAMBU_PASSWORD']
            }

    def expected_primary_keys(self):
        """
        return a dictionary with key of table name
        and value as a set of primary key fields
        """
        return {table: properties.get(self.PRIMARY_KEYS, set())
                for table, properties
                in self.expected_metadata().items()}

    def expected_replication_keys(self):
        """
        return a dictionary with key of table name
        and value as a set of replication key fields
        """
        return {table: properties.get(self.REPLICATION_KEYS, set())
                for table, properties
                in self.expected_metadata().items()}

    def expected_automatic_fields(self):
        """
        return a dictionary with key of table name and value as a set of
        primary key and replication key fields
        """
        return {table : self.expected_primary_keys()[table] | self.expected_replication_keys()[table]
                for table in self.expected_metadata().keys()}

    def expected_replication_method(self):
        """return a dictionary with key of table name nd value of replication method"""
        return {table: properties.get(self.REPLICATION_METHOD, None)
                for table, properties
                in self.expected_metadata().items()}

    @staticmethod
    def select_all_streams_and_fields(conn_id, catalogs, select_all_fields: bool = True):
        """Select all streams and all fields within streams"""
        for catalog in catalogs:
            schema = menagerie.get_annotated_schema(conn_id, catalog['stream_id'])

            non_selected_properties = []
            if not select_all_fields:
                # get a list of all properties so that none are selected
                non_selected_properties = schema.get('annotated-schema', {}).get(
                    'properties', {}).keys()

            connections.select_catalog_and_fields_via_metadata(
                conn_id, catalog, schema, [], non_selected_properties)

    def verify_field_selection(self, conn_id, expected_stream_ids):
        """
        Verify only expected selected fields are selected
        """

        catalogs = menagerie.get_catalogs(conn_id)
        for cat in catalogs:
            with self.subTest(tap_stream_id=cat.get('tap_stream_id')):
                # Call  menagerie.get_annotated_schema(conn_id, cat['stream_id'])
                # Grab `metadata` off of that response
                # for the empty breadcrumb, if it's selected, assert it's in `expected_stream_ids`
                #  - if not selected assertFalse
                # for other breadcrumbs, if it's selected, assert it's in `expected_selected_fields`
                #  - if not selected assertFalse

                mdata = menagerie.get_annotated_schema(conn_id, cat['stream_id']).get('metadata',[])

                self.assertTrue(cat.get('metadata').get('selected'),
                                msg="Stream not selected.")

                for item in mdata:
                    if item.get('breadcrumb') == []:
                        if item.get('metadata').get('selected'):
                            self.assertTrue(cat.get('tap_stream_id') in expected_stream_ids)
                        else:
                            self.assertFalse(cat.get('tap_stream_id') in expected_stream_ids)
                    else:
                        # TODO: dont assert on fields of unselected streams
                        self.assertTrue(item.get('metadata').get('selected'))


    def run_and_verify_sync(self, conn_id):
        """
        Run a sync job and make sure it exited properly.
        Return a dictionary with keys of streams synced
        and values of records synced for each stream
        """
        # Run a sync job using orchestrator
        sync_job_name = runner.run_sync_mode(self, conn_id)

        # Verify tap and target exit codes
        exit_status = menagerie.get_exit_status(conn_id, sync_job_name)
        menagerie.verify_sync_exit_status(self, exit_status, sync_job_name)

        # Verify actual rows were synced
        sync_record_count = runner.examine_target_output_file(
            self, conn_id, self.expected_streams(), self.expected_primary_keys())
        self.assertGreater(
            sum(sync_record_count.values()), 0,
            msg="failed to replicate any data: {}".format(sync_record_count)
        )
        print("total replicated row count: {}".format(sum(sync_record_count.values())))

        return sync_record_count
