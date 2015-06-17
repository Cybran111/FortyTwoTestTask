from south.v2 import SchemaMigration


class Migration(SchemaMigration):
    """This is NOT a migration, just a workaround for bad migration history"""

    def forwards(self, orm):
        pass

    def backwards(self, orm):
        pass
