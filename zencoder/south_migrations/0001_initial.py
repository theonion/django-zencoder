from south.db import db
from south.v2 import SchemaMigration


class Migration(SchemaMigration):
    def forwards(self, orm):
        # Adding model 'Video'
        db.create_table(u'zencoder_video', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('poster', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('input', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal(u'zencoder', ['Video'])

        # Adding model 'Source'
        db.create_table(u'zencoder_source', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('video',
             self.gf('django.db.models.fields.related.ForeignKey')(related_name='sources', to=orm['zencoder.Video'])),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('content_type', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('width', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('bitrate', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'zencoder', ['Source'])

        # Adding model 'Job'
        db.create_table(u'zencoder_job', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('video', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['zencoder.Video'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('job_id', self.gf('django.db.models.fields.IntegerField')()),
            ('data', self.gf('json_field.fields.JSONField')(default=u'null')),
        ))
        db.send_create_signal(u'zencoder', ['Job'])

    def backwards(self, orm):
        # Deleting model 'Video'
        db.delete_table(u'zencoder_video')

        # Deleting model 'Source'
        db.delete_table(u'zencoder_source')

        # Deleting model 'Job'
        db.delete_table(u'zencoder_job')

    models = {
        u'zencoder.job': {
            'Meta': {'ordering': "('created',)", 'object_name': 'Job'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'data': ('json_field.fields.JSONField', [], {'default': "u'null'"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job_id': ('django.db.models.fields.IntegerField', [], {}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'video': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['zencoder.Video']"})
        },
        u'zencoder.source': {
            'Meta': {'ordering': "('width', 'bitrate')", 'object_name': 'Source'},
            'bitrate': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'content_type': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'video': ('django.db.models.fields.related.ForeignKey', [],
                      {'related_name': "'sources'", 'to': u"orm['zencoder.Video']"}),
            'width': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'zencoder.video': {
            'Meta': {'object_name': 'Video'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'input': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'poster': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['zencoder']
