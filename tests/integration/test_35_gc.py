"""
© Copyright 2020 HP Development Company, L.P.
SPDX-License-Identifier: GPL-2.0-only
"""
import os
import unittest
from pathlib import Path

import pytest
from hurry.filesize import size, alternative

from ml_git.ml_git_message import output_messages
from tests.integration.commands import MLGIT_COMMIT, MLGIT_PUSH, MLGIT_REPOSITORY_GC, MLGIT_CHECKOUT, MLGIT_ADD, \
    MLGIT_INIT, MLGIT_ENTITY_INIT
from tests.integration.helper import init_repository, add_file, check_output, ERROR_MESSAGE, clear, ML_GIT_DIR


@pytest.mark.usefixtures('tmp_dir', 'aws_session')
class GcAcceptanceTests(unittest.TestCase):

    def set_up_gc(self, entity):
        init_repository(entity, self)
        add_file(self, entity, '', 'test')
        self.assertNotIn(ERROR_MESSAGE, check_output(MLGIT_COMMIT % (entity, entity + '-ex', '')))
        self.assertNotIn(ERROR_MESSAGE, check_output(MLGIT_PUSH % (entity, entity + '-ex')))
        with open(os.path.join(entity, entity + '-ex', 'newfile'), 'wb') as z:
            z.write(b'0' * 1024)
        self.assertNotIn(ERROR_MESSAGE, check_output(MLGIT_ADD % (entity, entity + '-ex', '')))
        self.assertNotIn(ERROR_MESSAGE, check_output(MLGIT_COMMIT % (entity, entity + '-ex', '--version=2')))
        self.assertNotIn(ERROR_MESSAGE, check_output(MLGIT_PUSH % (entity, entity + '-ex')))
        self.assertNotIn(ERROR_MESSAGE, check_output(MLGIT_CHECKOUT % (entity, entity + '-ex --version=1')))

    def get_metadata_info(self):
        metadata_path = os.path.join(self.tmp_dir, ML_GIT_DIR)
        number_of_files = 0
        original_size = 0
        for root, dirs, files in os.walk(metadata_path):
            for file in files:
                number_of_files += 1
                original_size += Path(os.path.join(root, file)).stat().st_size
        return original_size, number_of_files

    def check_result(self, result, entity, original_size, number_of_files, expected_removed_files, expected_reclaimed_space):
        self.assertIn(output_messages['INFO_STARTING_GC'] % entity, result)
        size_of_metadata, files_in_metadata = self.get_metadata_info()
        removed_files = number_of_files - files_in_metadata
        self.assertEqual(expected_removed_files, removed_files)
        self.assertIn(output_messages['INFO_REMOVED_FILES'] % (removed_files, self.tmp_dir), result)
        reclaimed_space = size(original_size - size_of_metadata, system=alternative)
        self.assertEqual(expected_reclaimed_space, reclaimed_space)
        self.assertIn(output_messages['INFO_RECLAIMED_SPACE'] % reclaimed_space, result)

    @pytest.mark.usefixtures('start_local_git_server', 'switch_to_tmp_dir')
    def test_01_gc_dataset_entity(self):
        entity = 'dataset'
        self.set_up_gc(entity)
        original_size, number_of_files = self.get_metadata_info()
        result = check_output(MLGIT_REPOSITORY_GC)
        self.check_result(result, entity, original_size, number_of_files,
                          expected_removed_files=3, expected_reclaimed_space='2 KB')

    @pytest.mark.usefixtures('start_local_git_server', 'switch_to_tmp_dir')
    def test_02_gc_labels_entity(self):
        entity = 'labels'
        self.set_up_gc(entity)
        original_size, number_of_files = self.get_metadata_info()
        result = check_output(MLGIT_REPOSITORY_GC)
        self.check_result(result, entity, original_size, number_of_files,
                          expected_removed_files=3, expected_reclaimed_space='2 KB')

    @pytest.mark.usefixtures('start_local_git_server', 'switch_to_tmp_dir')
    def test_03_gc_model_entity(self):
        entity = 'model'
        self.set_up_gc(entity)
        original_size, number_of_files = self.get_metadata_info()
        result = check_output(MLGIT_REPOSITORY_GC)
        self.check_result(result, entity, original_size, number_of_files,
                          expected_removed_files=3, expected_reclaimed_space='2 KB')

    @pytest.mark.usefixtures('start_local_git_server', 'switch_to_tmp_dir')
    def test_04_gc_repository(self):
        self.set_up_gc('dataset')
        self.set_up_gc('model')
        self.set_up_gc('labels')
        original_size, number_of_files = self.get_metadata_info()
        result = check_output(MLGIT_REPOSITORY_GC)
        self.assertIn(output_messages['INFO_STARTING_GC'] % 'labels', result)
        self.assertIn(output_messages['INFO_STARTING_GC'] % 'model', result)
        self.check_result(result, 'dataset', original_size, number_of_files,
                          expected_removed_files=9, expected_reclaimed_space='6 KB')

    @pytest.mark.usefixtures('start_local_git_server', 'switch_to_tmp_dir')
    def test_05_gc_deleted_entity(self):
        self.set_up_gc('dataset')
        self.set_up_gc('labels')
        original_size, number_of_files = self.get_metadata_info()
        clear(os.path.join(self.tmp_dir, 'labels'))
        result = check_output(MLGIT_REPOSITORY_GC)
        self.assertIn(output_messages['INFO_STARTING_GC'] % 'labels', result)
        self.check_result(result, 'dataset', original_size, number_of_files,
                          expected_removed_files=21, expected_reclaimed_space='32 KB')

    @pytest.mark.usefixtures('start_local_git_server', 'switch_to_tmp_dir')
    def test_06_gc_without_entity_initialized(self):
        self.assertNotIn(ERROR_MESSAGE, check_output(MLGIT_INIT))
        self.assertIn(output_messages['ERROR_UNINITIALIZED_METADATA'], check_output(MLGIT_REPOSITORY_GC))

    @pytest.mark.usefixtures('start_local_git_server', 'switch_to_tmp_dir')
    def test_07_gc_basic_flow(self):
        entity = 'dataset'
        self.set_up_gc(entity)
        original_size, number_of_files = self.get_metadata_info()
        result = check_output(MLGIT_REPOSITORY_GC)
        self.check_result(result, entity, original_size, number_of_files,
                          expected_removed_files=3, expected_reclaimed_space='2 KB')
        file = os.path.join(self.tmp_dir, 'dataset', 'computer-vision', 'images', 'dataset-ex', 'file-after-gc')
        with open(file, 'wb') as z:
            z.write(b'1' * 1024)
        self.assertNotIn(ERROR_MESSAGE, check_output(MLGIT_ADD % (entity, entity + '-ex', '')))
        self.assertNotIn(ERROR_MESSAGE, check_output(MLGIT_COMMIT % (entity, entity + '-ex', '--version=3')))
        self.assertNotIn(ERROR_MESSAGE, check_output(MLGIT_PUSH % (entity, entity + '-ex')))
        clear(os.path.join(self.tmp_dir, ML_GIT_DIR, entity))
        clear(os.path.join(self.tmp_dir, entity))
        self.assertNotIn(ERROR_MESSAGE, check_output(MLGIT_ENTITY_INIT % entity))
        self.assertNotIn(ERROR_MESSAGE, check_output(MLGIT_CHECKOUT % (entity, entity + '-ex --version=3')))
        self.assertTrue(os.path.exists(file))
