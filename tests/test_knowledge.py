import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

PACKAGE = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('knowledge', PACKAGE / 'scripts/knowledge.py')
k = importlib.util.module_from_spec(spec)
spec.loader.exec_module(k)


class KnowledgeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name) / 'os'
        shutil.copytree(PACKAGE, self.root, ignore=shutil.ignore_patterns('__pycache__', '.state'))
        self.external = Path(self.temp.name) / 'call.md'
        self.external.write_text('# Fictional call\nBuyer asked about rollout effort.\n')

    def tearDown(self):
        self.temp.cleanup()

    def imported(self):
        return k.import_file(self.root, self.external)

    def summary(self, imported):
        summary = self.root / 'wiki/sources/call.md'
        summary.parent.mkdir(exist_ok=True)
        summary.write_text('# Call summary\n\n[Original](../../' + imported['path'] + ')\n')
        return 'wiki/sources/call.md'

    def completed(self):
        record = self.imported()
        k.register(self.root, record['path'], record['sha256'], [self.summary(record)])
        return record

    def test_first_import_preserves_bytes_and_deduplicates(self):
        original = self.external.read_bytes()
        first, second = self.imported(), self.imported()
        self.assertEqual(first['path'], second['path'])
        self.assertTrue(second['duplicate'])
        self.assertEqual((self.root / first['path']).read_bytes(), original)
        self.assertEqual(self.external.read_bytes(), original)
        self.assertEqual(len(k.inspect(self.root)['pending']), 1)

    def test_missing_summary_stays_pending_then_resume_registers_once(self):
        source = self.imported()
        with self.assertRaises(ValueError):
            k.register(self.root, source['path'], source['sha256'], ['wiki/sources/missing.md'])
        self.assertEqual(k.inspect(self.root)['registered'], 0)
        summary = self.summary(source)
        k.register(self.root, source['path'], source['sha256'], [summary])
        again = k.register(self.root, source['path'], source['sha256'], [summary])
        self.assertTrue(again['already_registered'])
        self.assertEqual(k.inspect(self.root)['registered'], 1)
        self.assertEqual(k.inspect(self.root)['pending'], [])

    def test_observed_hash_prevents_registering_changed_input(self):
        source = self.imported()
        (self.root / source['path']).write_text('A different source')
        with self.assertRaisesRegex(ValueError, 'changed since'):
            k.register(self.root, source['path'], source['sha256'], [self.summary(source)])

    def test_registered_original_cannot_be_silently_refreshed(self):
        source = self.completed()
        registry_before = (self.root / '.state/sources.json').read_bytes()
        (self.root / source['path']).write_text('Changed original')
        self.assertTrue(k.check(self.root)['issues'])
        with self.assertRaises(ValueError):
            k.register(self.root, source['path'], k.sha(b'Changed original'), ['wiki/sources/call.md'])
        self.assertEqual((self.root / '.state/sources.json').read_bytes(), registry_before)

    def test_revision_preserves_original_and_links_to_it(self):
        first = self.completed()
        self.external.write_text('# Updated call\nBuyer clarified the objection.\n')
        second = self.imported()
        page = self.root / 'wiki/sources/revision.md'
        page.write_text('# Revision\nThe earlier statement was clarified.\n')
        k.register(self.root, second['path'], second['sha256'], ['wiki/sources/revision.md'], first['sha256'])
        entries = k.registry(self.root)['sources']
        self.assertEqual(len(entries), 2)
        self.assertEqual(entries[1]['revises'], entries[0]['id'])
        self.assertEqual(k.sha((self.root / first['path']).read_bytes()), first['sha256'])

    def test_unknown_revision_refused(self):
        source = self.imported()
        with self.assertRaisesRegex(ValueError, 'Unknown earlier'):
            k.register(self.root, source['path'], source['sha256'], [self.summary(source)], 'missing')

    def test_external_page_and_symlink_are_rejected(self):
        source = self.imported()
        with self.assertRaises(ValueError):
            k.register(self.root, source['path'], source['sha256'], ['../call.md'])
        (self.root / 'raw/shortcut.md').symlink_to(self.external)
        with self.assertRaisesRegex(ValueError, 'Symlink'):
            k.inspect(self.root)

    def test_lock_prevents_competing_writes(self):
        with k.writing(self.root):
            with self.assertRaisesRegex(ValueError, 'Write lock'):
                self.imported()
        self.assertFalse((self.root / '.state/write.lock').exists())
        self.assertFalse(self.imported()['duplicate'])

    def test_failed_atomic_replace_keeps_registry(self):
        from unittest.mock import patch
        self.completed()
        before = (self.root / '.state/sources.json').read_bytes()
        self.external.write_text('# Another call\nNew evidence\n')
        source = self.imported()
        with patch.object(k.os, 'replace', side_effect=OSError('simulated write failure')):
            with self.assertRaises(OSError):
                k.register(self.root, source['path'], source['sha256'], [self.summary(source)])
        self.assertEqual((self.root / '.state/sources.json').read_bytes(), before)
        self.assertEqual(len(k.inspect(self.root)['pending']), 1)
        self.assertFalse((self.root / '.state/write.lock').exists())

    def test_fresh_package_and_broken_link_detection(self):
        self.assertEqual(k.check(self.root)['issues'], [])
        (self.root / 'wiki/index.md').write_text('[Missing](does-not-exist.md)')
        self.assertTrue(any('Broken' in x for x in k.check(self.root)['issues']))

    def test_nontext_and_empty_imports_are_refused(self):
        self.external.write_bytes(b'\xff')
        with self.assertRaises(UnicodeDecodeError):
            self.imported()
        self.external.write_text('  \n')
        with self.assertRaisesRegex(ValueError, 'Empty'):
            self.imported()

    def test_missing_derived_page_is_reported(self):
        self.completed()
        (self.root / 'wiki/sources/call.md').unlink()
        self.assertTrue(any('Missing or empty' in x for x in k.inspect(self.root)['issues']))

    def test_cli_import_register_and_check(self):
        def command(*args):
            result = subprocess.run([sys.executable, str(self.root / 'scripts/knowledge.py'),
                                     '--root', str(self.root), *args], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            return json.loads(result.stdout)
        source = command('import-file', str(self.external))
        summary = self.summary(source)
        command('register', source['path'], '--sha256', source['sha256'], '--pages', summary)
        result = command('check')
        self.assertEqual(result['registered'], 1)
        self.assertEqual(result['issues'], [])

    def test_health_read_does_not_create_state(self):
        report = k.health(self.root)
        self.assertEqual(report['state'], 'not-started')
        self.assertIsNone(report['latest_registered_at'])
        self.assertEqual(report['operations'], {})
        self.assertFalse((self.root / '.state').exists())

    def test_old_event_is_not_refreshed_by_recent_ingestion(self):
        source = self.imported()
        k.register(self.root, source['path'], source['sha256'], [self.summary(source)],
                   event_date='2020-01-02', captured_at='2026-10-22T08:00:00+02:00')
        report = k.health(self.root, review_before='2026-01-01')
        self.assertEqual(report['state'], 'review-needed')
        self.assertTrue(report['sources'][0]['review_candidate'])
        self.assertEqual(report['sources'][0]['event_date'], '2020-01-02')
        self.assertEqual(report['sources'][0]['captured_at'], '2026-10-22T08:00:00+02:00')
        self.assertNotEqual(report['sources'][0]['ingested_at'], report['sources'][0]['captured_at'])
        self.assertFalse(k.health(self.root)['sources'][0]['review_candidate'])

    def test_legacy_registry_has_unknown_freshness(self):
        self.completed()
        data = k.registry(self.root)
        data['sources'][0].pop('event_date')
        data['sources'][0].pop('captured_at')
        k.save(self.root, data)
        report = k.health(self.root, '2026-10-01')
        self.assertEqual(report['freshness_unknown'], 1)
        self.assertIsNone(report['sources'][0]['event_date'])
        self.assertFalse(report['sources'][0]['review_candidate'])

    def test_duplicate_registration_keeps_original_dates(self):
        source = self.imported()
        page = self.summary(source)
        k.register(self.root, source['path'], source['sha256'], [page], event_date='2020-01-02')
        before = (self.root / '.state/sources.json').read_bytes()
        k.register(self.root, source['path'], source['sha256'], [page], event_date='2026-10-22')
        self.assertEqual((self.root / '.state/sources.json').read_bytes(), before)

    def test_invalid_dates_do_not_register_a_source(self):
        source = self.imported()
        for metadata in ({'event_date':'2026-02-30'}, {'event_date':'20261022'},
                         {'captured_at':'2026-10-22T12:00:00'}, {'captured_at':'today'}):
            with self.subTest(metadata=metadata), self.assertRaises(ValueError):
                k.register(self.root, source['path'], source['sha256'], [self.summary(source)], **metadata)
        self.assertEqual(k.registry(self.root)['sources'], [])

    def test_revision_does_not_erase_old_source_review(self):
        first = self.imported()
        k.register(self.root, first['path'], first['sha256'], [self.summary(first)], event_date='2020-01-01')
        self.external.write_text('A dated correction, not an independent corroboration.')
        second = self.imported()
        k.register(self.root, second['path'], second['sha256'], [self.summary(second)],
                   revises=first['sha256'], event_date='2026-10-22')
        report = k.health(self.root, '2026-01-01')
        self.assertTrue(report['sources'][0]['has_later_revision'])
        self.assertTrue(report['sources'][0]['review_candidate'])
        self.assertFalse(report['sources'][1]['review_candidate'])
        self.assertEqual(len(report['sources']), 2)

    def test_unreadable_pending_sources_are_identified(self):
        (self.root / 'raw/broken.md').write_bytes(b'\xff')
        (self.root / 'raw/empty.txt').write_text('  ')
        (self.root / 'raw/document.pdf').write_bytes(b'%PDF')
        pending = k.health(self.root)['pending']
        self.assertEqual(len(pending), 3)
        self.assertTrue(all(not e['supported'] and e['reason'] for e in pending))

    def test_cli_failure_and_recovery_are_observed_without_source_content(self):
        def command(*args):
            return subprocess.run([sys.executable, str(self.root / 'scripts/knowledge.py'),
                                   '--root', str(self.root), *args], capture_output=True, text=True)
        failed = command('import-file', str(self.root / 'missing.md'))
        self.assertEqual(failed.returncode, 1)
        report = json.loads(command('health').stdout)
        self.assertEqual(report['state'], 'needs-attention')
        self.assertFalse(report['operations']['import-file']['last_attempt']['ok'])
        success = command('import-file', str(self.external))
        self.assertEqual(success.returncode, 0, success.stderr)
        report = json.loads(command('health').stdout)
        self.assertEqual(report['state'], 'pending')
        self.assertTrue(report['operations']['import-file']['last_attempt']['ok'])
        self.assertIn('last_failure_at', report['operations']['import-file'])
        ledger = (self.root / '.state/ingestion-health.json').read_text()
        self.assertNotIn(str(self.external), ledger)
        self.assertNotIn('Buyer asked', ledger)

    def test_health_record_failure_preserves_previous_observation(self):
        from unittest.mock import patch
        k.record_attempt(self.root, 'import-file', True)
        before = (self.root / '.state/ingestion-health.json').read_bytes()
        with patch.object(k.os, 'replace', side_effect=OSError('write failure')):
            with self.assertRaises(OSError):
                k.record_attempt(self.root, 'register', False)
        self.assertEqual((self.root / '.state/ingestion-health.json').read_bytes(), before)
        self.assertFalse((self.root / '.state/write.lock').exists())

    def test_successful_import_reports_health_log_failure_separately(self):
        from unittest.mock import patch
        from contextlib import redirect_stdout
        from io import StringIO
        output = StringIO()
        args = ['knowledge.py', '--root', str(self.root), 'import-file', str(self.external)]
        with patch.object(sys, 'argv', args), patch.object(k, 'record_attempt', side_effect=OSError('log failure')):
            with redirect_stdout(output):
                code = k.main()
        result = json.loads(output.getvalue())
        self.assertEqual(code, 0)
        self.assertIn('health_log_warning', result)
        self.assertTrue((self.root / result['path']).is_file())

    def test_malformed_health_log_is_not_silently_reset(self):
        (self.root / '.state').mkdir()
        file = self.root / '.state/ingestion-health.json'
        file.write_text('[]')
        with self.assertRaisesRegex(ValueError, 'Invalid ingestion health log'):
            k.health(self.root)
        with self.assertRaises(ValueError):
            k.record_attempt(self.root, 'import-file', True)
        self.assertEqual(file.read_text(), '[]')


if __name__ == '__main__':
    unittest.main()
