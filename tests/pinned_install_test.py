"""Verify this fork cannot check upstream, replace itself, or refresh a model tag."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
TMP = tempfile.TemporaryDirectory()
os.environ.update(SURVIVAL_LLM_APP_DIR=TMP.name, SURVIVAL_LLM_FILES=TMP.name + '/files',
                  SURVIVAL_LLM_LIBRARY=TMP.name + '/library', OLLAMA_HOST='127.0.0.1:9',
                  SURVIVAL_LLM_MANIFEST='https://invalid.example/catalog.json',
                  SURVIVAL_LLM_UPDATES='https://invalid.example/update.json')
sys.path.insert(0, str(ROOT / 'app'))
import server


class PinnedInstall(unittest.TestCase):
    def test_updates_and_catalog_never_contact_network(self):
        with patch('urllib.request.urlopen', side_effect=AssertionError('unexpected network')):
            server.check_updates()
            server.check_updates(force=True)
            server.auto_check_updates()
            self.assertTrue(server.update_report()['disabled'])
            self.assertIsNone(server.newer_app())
            self.assertIsNone(server.newer_library())
            server.manifest.update(packs=None, failed_at=0)
            self.assertEqual(server.library_packs(), json.loads((ROOT / 'library-packs.json').read_text())['packs'])
            with self.assertRaisesRegex(RuntimeError, 'disabled'):
                server.app_update_worker('test')
            with self.assertRaisesRegex(RuntimeError, 'disabled'):
                server.pull_worker('test', 'granite4.2:8b')

    def test_remote_inference_address_rejected(self):
        result = subprocess.run([sys.executable, '-c', 'import core'], cwd=ROOT,
                                env={**os.environ, 'OLLAMA_HOST': 'example.com:11434'},
                                capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('loopback', result.stderr)

    def test_no_replacement_helpers_or_upstream_links(self):
        for name in ('install_mac', 'install_windows', 'restart_into', 'WINDOWS_SWAP'):
            self.assertFalse(hasattr(server, name), name)
        source = (ROOT / 'app/server.py').read_text()
        self.assertNotIn('anonnerdfrenzy.github.io', source)
        self.assertNotIn('brangus.io', source)
        self.assertNotIn('target=auto_check_updates', source)
        html = (ROOT / 'app/static/index.html').read_text()
        self.assertNotIn('updates-btn', html)
        self.assertNotIn('updates-dialog', html)


if __name__ == '__main__':
    unittest.main()
