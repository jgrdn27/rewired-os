"""Distribution boundary tests: real ZIPs, temporary installs, interrupted writes."""
import importlib.util
import json
from pathlib import Path
import stat
import tempfile
import unittest
from unittest.mock import patch
import zipfile

SPEC = importlib.util.spec_from_file_location('distribution', Path(__file__).resolve().parents[1] / 'scripts/distribution.py')
d = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(d)


class DistributionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.base = Path(self.temp.name).resolve()
        self.source = self.base / 'stock'
        self.source.mkdir()
        self.content = {'README.md': b'Original guide\n', 'AGENTS.md': b'Canonical guidance\n',
                        'CLAUDE.md': b'@AGENTS.md\n', 'preferences.json': b'{}\n',
                        'wiki/index.md': b'Empty wiki\n', 'raw/README.md': b'Source instructions\n',
                        'connections.md': b'No accounts\n', 'docs/guide.md': b'Guide one\n'}
        self.first = self.make_release('0.5.0-rewired-preview')
        self.root = self.base / 'My OS'
        d.install(self.first, self.root)

    def tearDown(self):
        self.temp.cleanup()

    def make_release(self, version):
        for p in self.source.rglob('*'):
            if p.is_file():
                p.unlink()
        for name, data in self.content.items():
            p = self.source / name
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(data)
        manifest = {'version': version, 'files': sorted([*self.content, 'release-manifest.json'])}
        (self.source / 'release-manifest.json').write_bytes(d.encoded(manifest))
        output = self.base / (version + '.zip')
        d.build(self.source, output)
        return output

    def second(self):
        self.content['README.md'] = b'New guide\n'
        self.content['docs/new.md'] = b'New file\n'
        return d.package(self.make_release('0.6.0-rewired-preview'))

    def snapshot(self):
        return {p.relative_to(self.root).as_posix(): p.read_bytes()
                for p in self.root.rglob('*') if p.is_file()}

    def test_fresh_install_and_checksum(self):
        installed, _ = d.receipt(self.root)
        self.assertEqual(installed['version'], '0.5.0-rewired-preview')
        self.assertEqual(installed['files']['wiki/index.md']['policy'], 'seed')
        with self.assertRaises(d.DistributionError):
            d.install(self.first, self.base / 'wrong-checksum', '0' * 64)
        self.assertFalse((self.base / 'wrong-checksum').exists())

    def test_install_refuses_existing_even_empty_folder(self):
        dest = self.base / 'existing'
        dest.mkdir()
        with self.assertRaises(d.DistributionError):
            d.install(self.first, dest)
        self.assertEqual(list(dest.iterdir()), [])

    def test_preview_is_read_only(self):
        incoming, _, _ = self.second()
        before = self.snapshot()
        result = d.plan(self.root, incoming)
        self.assertTrue(result['can_apply'])
        self.assertEqual(before, self.snapshot())

    def test_update_and_restore_preserve_user_data_and_unchanged_customizations(self):
        (self.root / 'wiki/index.md').write_bytes(b'Personal wiki\n')
        (self.root / 'wiki/private.md').write_bytes(b'Private content\n')
        (self.root / 'preferences.json').write_bytes(b'{"custom": true}\n')
        (self.root / 'AGENTS.md').write_bytes(b'My custom guidance\n')
        (self.root / 'raw/README.md').unlink()
        before = self.snapshot()
        incoming, contents, sha = self.second()
        result = d.apply(self.root, incoming, contents, sha)
        self.assertEqual((self.root / 'README.md').read_bytes(), b'New guide\n')
        for name in ('wiki/index.md', 'wiki/private.md', 'preferences.json', 'AGENTS.md'):
            self.assertEqual((self.root / name).read_bytes(), before[name])
        self.assertFalse((self.root / 'raw/README.md').exists())
        d.restore(self.root, result['backup'])
        for name, data in before.items():
            self.assertEqual((self.root / name).read_bytes(), data)
        self.assertFalse((self.root / 'docs/new.md').exists())

    def test_conflict_blocks_entire_update(self):
        (self.root / 'README.md').write_bytes(b'My own introduction\n')
        incoming, contents, sha = self.second()
        before = self.snapshot()
        self.assertEqual(d.plan(self.root, incoming)['conflicts'], ['README.md'])
        with self.assertRaises(d.DistributionError):
            d.apply(self.root, incoming, contents, sha)
        self.assertEqual(before, self.snapshot())

    def test_deleted_managed_file_is_conflict_when_upstream_changes(self):
        (self.root / 'README.md').unlink()
        incoming, _, _ = self.second()
        self.assertIn('README.md', d.plan(self.root, incoming)['conflicts'])

    def test_new_file_collision_is_conflict(self):
        (self.root / 'docs/new.md').write_bytes(b'My custom file\n')
        incoming, _, _ = self.second()
        self.assertIn('docs/new.md', d.plan(self.root, incoming)['conflicts'])

    def test_upstream_removal_backs_up_and_restores(self):
        del self.content['docs/guide.md']
        incoming, contents, sha = self.second()
        result = d.apply(self.root, incoming, contents, sha)
        self.assertFalse((self.root / 'docs/guide.md').exists())
        d.restore(self.root, result['backup'])
        self.assertEqual((self.root / 'docs/guide.md').read_bytes(), b'Guide one\n')

    def test_new_and_changed_seed_files_are_never_applied_on_update(self):
        self.content['context/new-default.md'] = b'Potential personal state\n'
        self.content['preferences.json'] = b'{"new_default": true}\n'
        incoming, contents, sha = self.second()
        d.apply(self.root, incoming, contents, sha)
        self.assertFalse((self.root / 'context/new-default.md').exists())
        self.assertEqual((self.root / 'preferences.json').read_bytes(), b'{}\n')

    def test_restore_refuses_to_destroy_edits_made_after_update(self):
        result = d.apply(self.root, *self.second())
        (self.root / 'README.md').write_bytes(b'Edited after update\n')
        before = self.snapshot()
        with self.assertRaises(d.DistributionError):
            d.restore(self.root, result['backup'])
        self.assertEqual(before, self.snapshot())

    def test_interrupted_update_recovers_from_durable_journal(self):
        incoming, contents, sha = self.second()
        before = self.snapshot()
        original = d.atomic
        def fail_on_new(root, name, data):
            if name == 'docs/new.md':
                raise OSError('simulated failed write')
            return original(root, name, data)
        with patch.object(d, 'atomic', side_effect=fail_on_new):
            with self.assertRaises(OSError):
                d.apply(self.root, incoming, contents, sha)
        self.assertTrue((self.root / d.PENDING).exists())
        with self.assertRaises(d.DistributionError):
            d.plan(self.root, incoming)
        d.restore(self.root)
        for name, data in before.items():
            self.assertEqual((self.root / name).read_bytes(), data)
        self.assertFalse((self.root / d.PENDING).exists())

    def test_interrupted_restore_can_resume(self):
        result = d.apply(self.root, *self.second())
        original = d.atomic
        def fail_on_receipt(root, name, data):
            if name == d.RECEIPT:
                raise OSError('simulated failure')
            return original(root, name, data)
        with patch.object(d, 'atomic', side_effect=fail_on_receipt):
            with self.assertRaises(OSError):
                d.restore(self.root, result['backup'])
        d.restore(self.root)
        self.assertEqual(d.receipt(self.root)[0]['version'], '0.5.0-rewired-preview')

    def test_restore_recovers_if_final_pending_cleanup_was_interrupted(self):
        result = d.apply(self.root, *self.second())
        original = d.remove
        def fail_on_pending(root, name):
            if name == d.PENDING:
                raise OSError('interrupted final cleanup')
            return original(root, name)
        with patch.object(d, 'remove', side_effect=fail_on_pending):
            with self.assertRaises(OSError):
                d.restore(self.root, result['backup'])
        d.restore(self.root)
        self.assertFalse((self.root / d.PENDING).exists())
        self.assertEqual(d.receipt(self.root)[0]['version'], '0.5.0-rewired-preview')

    def test_explicit_recovery_of_stale_lock_after_interruption(self):
        original = d.atomic
        def fail_on_readme(root, name, data):
            if name == 'README.md':
                raise OSError('interrupted write')
            return original(root, name, data)
        with patch.object(d, 'atomic', side_effect=fail_on_readme):
            with self.assertRaises(OSError):
                d.apply(self.root, *self.second())
        (self.root / d.LOCK).write_text('dead-process')
        with self.assertRaises(d.DistributionError):
            d.restore(self.root)
        d.restore(self.root, recover_lock=True)
        self.assertFalse((self.root / d.LOCK).exists())

    def test_direct_extraction_keeps_receipt_and_supports_updates(self):
        extracted = self.base / 'manual'
        # This archive was generated by our builder; ordinary extraction is the user fallback.
        with zipfile.ZipFile(self.first) as archive:
            archive.extractall(extracted)
        manual = extracted / 'Rewired-OS'
        self.assertEqual(d.receipt(manual)[0]['version'], '0.5.0-rewired-preview')
        result = d.apply(manual, *self.second())
        self.assertTrue(result['applied'])

    def test_preexisting_checksum_blocks_build_without_creating_zip(self):
        output = self.base / 'new.zip'
        Path(str(output) + '.sha256').write_text('keep this')
        with self.assertRaises(d.DistributionError):
            d.build(self.source, output)
        self.assertFalse(output.exists())

    def test_backup_tampering_blocks_restore(self):
        result = d.apply(self.root, *self.second())
        (self.root / '.rewired/backups' / result['backup'] / 'files/README.md').write_bytes(b'Corrupt')
        with self.assertRaises(d.DistributionError):
            d.restore(self.root, result['backup'])
        self.assertEqual((self.root / 'README.md').read_bytes(), b'New guide\n')

    def test_lock_blocks_writes(self):
        (self.root / d.LOCK).write_text('another-process\n')
        with self.assertRaises(d.DistributionError):
            d.apply(self.root, *self.second())
        self.assertEqual((self.root / d.LOCK).read_text(), 'another-process\n')

    def test_local_ingestion_lock_blocks_updates(self):
        (self.root / '.state').mkdir()
        (self.root / '.state/write.lock').write_text('locked')
        with self.assertRaises(d.DistributionError):
            d.apply(self.root, *self.second())

    def test_symlink_destination_cannot_write_outside_folder(self):
        outside = self.base / 'outside'
        outside.write_bytes(b'Keep me\n')
        (self.root / 'README.md').unlink()
        (self.root / 'README.md').symlink_to(outside)
        with self.assertRaises(d.DistributionError):
            d.apply(self.root, *self.second())
        self.assertEqual(outside.read_bytes(), b'Keep me\n')

    def test_same_and_older_versions_refused(self):
        with self.assertRaises(d.DistributionError):
            d.plan(self.root, d.package(self.first)[0])
        self.assertLess(d.version_key('1.0.0-preview.2'), d.version_key('1.0.0-preview.10'))
        self.assertLess(d.version_key('1.0.0-preview'), d.version_key('1.0.0'))

    def rewrite_zip(self, name, extra=None, replace=None):
        dest = self.base / name
        with zipfile.ZipFile(self.first) as src, zipfile.ZipFile(dest, 'w') as out:
            for info in src.infolist():
                data = src.read(info)
                if replace and info.filename == d.PREFIX + replace[0]:
                    data = replace[1]
                out.writestr(info, data)
            if extra:
                out.writestr(*extra)
        return dest

    def test_hash_mismatch_and_unlisted_file_rejected(self):
        for archive in (self.rewrite_zip('changed.zip', replace=('README.md', b'Tampered')),
                        self.rewrite_zip('extra.zip', extra=(d.PREFIX + 'extra.md', b'Hidden'))):
            with self.assertRaises(d.DistributionError):
                d.package(archive)

    def test_traversal_and_zip_symlink_rejected(self):
        for name in ('../escape', '/absolute', 'folder\\escape', 'CON.txt'):
            with self.assertRaises(d.DistributionError):
                d.package(self.rewrite_zip('bad-' + str(len(name)) + '.zip', extra=(d.PREFIX + name, b'x')))
        info = zipfile.ZipInfo(d.PREFIX + 'link')
        info.external_attr = (stat.S_IFLNK | 0o777) << 16
        with self.assertRaises(d.DistributionError):
            d.package(self.rewrite_zip('link.zip', extra=(info, b'/outside')))

    def test_case_collision_and_ownership_tampering_rejected(self):
        meta = d.package(self.first)[0]
        meta['files']['readme.md'] = meta['files']['README.md']
        with self.assertRaises(d.DistributionError):
            d.validate_receipt(meta)
        del meta['files']['readme.md']
        meta['files']['preferences.json']['policy'] = 'managed'
        with self.assertRaises(d.DistributionError):
            d.validate_receipt(meta)

    def test_installed_or_dirty_folder_cannot_build(self):
        with self.assertRaises(d.DistributionError):
            d.build(self.root, self.base / 'personal.zip')
        (self.source / 'extra-private.md').write_text('personal')
        with self.assertRaises(d.DistributionError):
            d.build(self.source, self.base / 'dirty.zip')

    def test_build_is_reproducible_and_refuses_overwrite(self):
        another = self.base / 'repeat.zip'
        d.build(self.source, another)
        self.assertEqual(another.read_bytes(), self.first.read_bytes())
        with self.assertRaises(d.DistributionError):
            d.build(self.source, another)

    def test_newer_update_must_be_restored_first(self):
        first_update = d.apply(self.root, *self.second())
        self.content['README.md'] = b'Third guide\n'
        second_update = d.apply(self.root, *d.package(self.make_release('0.7.0-rewired-preview')))
        with self.assertRaises(d.DistributionError):
            d.restore(self.root, first_update['backup'])
        d.restore(self.root, second_update['backup'])
        d.restore(self.root, first_update['backup'])
        self.assertEqual(d.receipt(self.root)[0]['version'], '0.5.0-rewired-preview')


if __name__ == '__main__':
    unittest.main()
