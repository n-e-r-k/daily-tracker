from log_config import create_logger
import os
import json

# create logger for module
logger = create_logger('Manifest Controller')

class Manifest():
    def __init__(self, manifest_path: str):
        self.manifest_path = manifest_path

        self._manifest_buffer = None
        self._startup()

    def _startup(self) -> None:
        # confirm manifest existence
        if not os.path.exists(self.manifest_path):
            logger.info('no manifest exists at %s, creating new manifest off template', \
                self.manifest_path)

            self._create_new_manifest()

        else:
            logger.info('manifest found at %s', self.manifest_path)

    # --- sudo-private functions ---

    def _create_new_manifest(self) -> None:
        default_manifest = {
            'schema' : {
                'header' : {
                    'date' : 'date-string',
                    'log-uuid' : 'uuid4-sting'
                },
                'example_section' : [
                    {
                        'question_text' : 'Taken Medication?',
                        'response_type' : 'bool'
                    },
                    {
                        'question_text' : 'Creative Fullfillment',
                        'response_type' : 'option',
                        'options' : [
                            'Godot Game',
                            'Python Projects'
                        ]
                    },
                    {
                        'question_text' : 'Any Additional Information',
                        'response_type' : 'option',
                        'options' : [
                            'No',
                            {
                                'option_text' : 'yes',
                                'response_type' : 'str'
                            }
                        ]
                    }
                ]
            },
            'data' : {}
        }

        self._manifest_buffer = default_manifest
        self._write_manifest()

    def _read_manifest(self) -> None:
        # verify no over-write attempt
        if self._manifest_buffer is not None:
            logger.error('attempted to over-write already occupied manifest buffer. Skipping instruction')
            return

        else:
            logger.debug('reading manifest file into buffer')

        with open(self.manifest_path, 'r') as manifest_file:
            self._manifest_buffer = json.loads(manifest_file.read())

    def _write_manifest(self) -> None:
        # verify no empty-write
        if self._manifest_buffer is None:
            logger.error('attempted to write to manifest with empty buffer. Skipping instruction')
            return

        else:
            logger.debug('writing manifest from buffer to file')

        with open(self.manifest_path, 'w') as manifest_file:
            #                                                   VVV--- fancy json formatting
            manifest_file.write(json.dumps(self._manifest_buffer, sort_keys=True, indent=4))

        self._dump_manifest()

    def _dump_manifest(self) -> None:
        # verify no empty-dump
        if self._manifest_buffer is None:
            logger.error('attempted to dump already empty buffer. Skipping instruction')

        else:
            logger.debug('dumping manifest buffer')

        self._manifest_buffer = None

    # --- public functions ---

    def get_schema(self) -> dict:
        logger.info('request recieved to get schema')

        self._read_manifest()
        schema = self._manifest_buffer['schema']
        self._dump_manifest()

        return schema

    def put_schema(self, schema: dict) -> None:
        logger.info('request recieved to put schema')

        self._read_manifest()
        self._manifest_buffer['schema'] = schema
        self._write_manifest()

    def get_all_entries(self) -> list:
        logger.info('reqeust recieved to get all entries')

        self._read_manifest()
        results = self._manifest_buffer['data']
        self._dump_manifest()

        return results

    def get_entry(self, date_code: str) -> dict:
        logger.info('reqeust recieved to get entry with datecode %s', date_code)

        self._read_manifest()
        result = self._manifest_buffer['data'][date_code]
        self._dump_manifest()

        return result

    def put_entry(self, entry: dict, date_code: str) -> None:
        logger.info('reqeust recieved to put entry with datecode %s', date_code)

        self._read_manifest()
        self._manifest_buffer['data'][date_code] = entry
        self._write_manifest()
