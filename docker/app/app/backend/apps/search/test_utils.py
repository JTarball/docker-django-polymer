"""
    search.test_utils
    =================

    Test the functionality of autocomplete/autosuggest/search app engine

"""
from rest_framework.test import APITestCase

from taggit.managers import TaggableManager

from django.db import models
from django.db.models import signals
from django.template.defaultfilters import slugify
from django_dynamic_fixture import G

from accounts.models import AccountsUser
from search.utils import r, ZKEY_AUTOCOMPLETE, SKEY_AUTOCOMPLETE
from search.utils import add_model_to_redis, dump_redis, flush_redis, autocomplete_suggestion, search_redis


class TestModelPost(models.Model):
    """ Test Model - Post like Model """
    # =====================
    # For Redis Search Only
    # =====================
    searchable_fields = ['title', 'tags']
    redis_stored_fields = ['title', 'slug', 'get_absolute_url']
    # ======================
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    content = models.TextField()
    tags = TaggableManager(blank=True)

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ("blog:detail", (), {"slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(TestModelPost, self).save(*args, **kwargs)


##############################################################################
# Comment - type of comment (warning/ issue / comment)
##############################################################################
def reindex_redis_search(sender, instance, **kwargs):
    """ Callback function which recalculates what is searchable in redis from sender. """
    flush_redis()
    [add_model_to_redis(model) for model in TestModelPost.objects.all()]
    dump_redis()

signals.post_save.connect(reindex_redis_search, sender=TestModelPost, dispatch_uid="add_post_tags")


class SearchUtilTests(APITestCase):

    def setUp(self):
        self.staff = G(AccountsUser, is_superuser=False, is_staff=True)

    def tearDown(self):
        flush_redis()

    def test_basic_add_model_to_redis(self):
        """ Tests add of models to redis database. """
        G(TestModelPost, title="This is a test post.", slug="", author=self.staff)
        self.assertEquals(r.zrange(ZKEY_AUTOCOMPLETE, 0, -1), ['a', 'a*', 'i', 'is', 'is*', 'p', 'po', 'pos',
                                                               'post', 'post*', 't', 'te', 'tes', 'test',
                                                               'test*', 'th', 'thi', 'this', 'this is a test post*',
                                                               'this*'])
        autocomplete_list = r.keys(SKEY_AUTOCOMPLETE+'*')
        self.assertTrue(SKEY_AUTOCOMPLETE+'this' in autocomplete_list)
        self.assertTrue(SKEY_AUTOCOMPLETE+'is' in autocomplete_list)
        self.assertTrue(SKEY_AUTOCOMPLETE+'a' in autocomplete_list)
        self.assertTrue(SKEY_AUTOCOMPLETE+'test' in autocomplete_list)
        self.assertTrue(SKEY_AUTOCOMPLETE+'post' in autocomplete_list)
        self.assertTrue(SKEY_AUTOCOMPLETE+'this is a test post' in autocomplete_list)
        self.assertEquals(r.smembers('models-search.testmodelpost:1'),
                          set(['title:This is a test post.',
                               'slug:this-is-a-test-post',
                               'get_absolute_url:/blog/post/this-is-a-test-post/']))

    def test_no_value_add_model_to_redis(self):
        """ Tests add of models to redis database with no value for fields. """
        post = G(TestModelPost, title="", slug="",  author=self.staff)
        post.save()  # G should save automatically but to be sure - save again
        self.assertEquals(r.zrange(ZKEY_AUTOCOMPLETE, 0, -1), [])
        self.assertEquals(r.keys(SKEY_AUTOCOMPLETE+'*'), [])
        self.assertEquals(r.smembers('models-*'), set([]))

    def test_multiple_add_model_to_redis(self):
        """ Tests adding of multiple models to redis database. """
        G(TestModelPost, title="This is the first post.", slug="",  author=self.staff)
        G(TestModelPost, title="This is the second post.", slug="",  author=self.staff)
        G(TestModelPost, title="This is the third post. I am sure you know this.", slug="",  author=self.staff)
        self.assertEquals(r.zrange(ZKEY_AUTOCOMPLETE, 0, -1), ['a', 'am', 'am*', 'f', 'fi', 'fir', 'firs',
                                                               'first', 'first*', 'i', 'i*', 'is', 'is*',
                                                               'k', 'kn', 'kno', 'know', 'know*', 'p', 'po',
                                                               'pos', 'post', 'post*', 's', 'se', 'sec', 'seco',
                                                               'secon', 'second', 'second*', 'su', 'sur', 'sure',
                                                               'sure*', 't', 'th', 'the', 'the*', 'thi', 'thir',
                                                               'third', 'third*', 'this', 'this is the first post*',
                                                               'this is the second post*',
                                                               'this is the third post  i am sure you know this*',
                                                               'this*', 'y', 'yo', 'you', 'you*'])
        autocomplete_list = r.keys(SKEY_AUTOCOMPLETE+'*')
        self.assertTrue(SKEY_AUTOCOMPLETE+'this' in autocomplete_list)
        self.assertTrue(SKEY_AUTOCOMPLETE+'this is the third post  i am sure you know this' in autocomplete_list)
        self.assertTrue(SKEY_AUTOCOMPLETE+'know' in autocomplete_list)
        self.assertTrue(SKEY_AUTOCOMPLETE+'is' in autocomplete_list)
        self.assertTrue(SKEY_AUTOCOMPLETE+'the' in autocomplete_list)
        self.assertTrue(SKEY_AUTOCOMPLETE+'first' in autocomplete_list)
        self.assertTrue(SKEY_AUTOCOMPLETE+'this is the second post' in autocomplete_list)
        self.assertTrue(SKEY_AUTOCOMPLETE+'you' in autocomplete_list)
        self.assertTrue(SKEY_AUTOCOMPLETE+'sure' in autocomplete_list)
        self.assertTrue(SKEY_AUTOCOMPLETE+'second' in autocomplete_list)
        self.assertTrue(SKEY_AUTOCOMPLETE+'i' in autocomplete_list)
        self.assertTrue(SKEY_AUTOCOMPLETE+'third' in autocomplete_list)
        self.assertTrue(SKEY_AUTOCOMPLETE+'this is the first post' in autocomplete_list)
        self.assertTrue(SKEY_AUTOCOMPLETE+'am' in autocomplete_list)
        self.assertTrue(SKEY_AUTOCOMPLETE+'post' in autocomplete_list)
        self.assertEquals(r.smembers(SKEY_AUTOCOMPLETE+'this'), set(['search.testmodelpost:3',
                                                                     'search.testmodelpost:2',
                                                                     'search.testmodelpost:1']))
        self.assertEquals(r.smembers(SKEY_AUTOCOMPLETE+'is'), set(['search.testmodelpost:3',
                                                                   'search.testmodelpost:2',
                                                                   'search.testmodelpost:1']))
        self.assertEquals(r.smembers(SKEY_AUTOCOMPLETE+'the'), set(['search.testmodelpost:3',
                                                                    'search.testmodelpost:2',
                                                                    'search.testmodelpost:1']))
        self.assertEquals(r.smembers(SKEY_AUTOCOMPLETE+'this is the third post  i am sure you know this'),
                          set(['search.testmodelpost:3']))
        self.assertEquals(r.smembers(SKEY_AUTOCOMPLETE+'this is the second post'), set(['search.testmodelpost:2']))
        self.assertEquals(r.smembers(SKEY_AUTOCOMPLETE+'this is the first post'), set(['search.testmodelpost:1']))
        self.assertEquals(r.smembers(SKEY_AUTOCOMPLETE+'post'), set(['search.testmodelpost:3',
                                                                     'search.testmodelpost:2',
                                                                     'search.testmodelpost:1']))
        self.assertEquals(r.smembers('models-search.testmodelpost:1'),
                          set(['title:This is the first post.',
                               'get_absolute_url:/blog/post/this-is-the-first-post/',
                               'slug:this-is-the-first-post']))
        self.assertEquals(r.smembers('models-search.testmodelpost:2'),
                          set(['title:This is the second post.',
                               'get_absolute_url:/blog/post/this-is-the-second-post/',
                               'slug:this-is-the-second-post']))
        self.assertEquals(r.smembers('models-search.testmodelpost:3'),
                          set(['title:This is the third post. I am sure you know this.',
                               'get_absolute_url:/blog/post/this-is-the-third-post-i-am-sure-you-know-this/',
                               'slug:this-is-the-third-post-i-am-sure-you-know-this']))

    def test_flush_redis(self):
        """ Test of flush_redis method. """
        G(TestModelPost, title="This is a test post.", slug="", author=self.staff)
        self.assertEquals(r.zrange(ZKEY_AUTOCOMPLETE, 0, -1), ['a', 'a*', 'i', 'is', 'is*', 'p', 'po', 'pos',
                                                               'post', 'post*', 't', 'te', 'tes', 'test',
                                                               'test*', 'th', 'thi', 'this', 'this is a test post*',
                                                               'this*'])
        autocomplete_list = r.keys(SKEY_AUTOCOMPLETE+'*')
        self.assertTrue(SKEY_AUTOCOMPLETE+'this' in autocomplete_list)
        self.assertTrue(SKEY_AUTOCOMPLETE+'is' in autocomplete_list)
        self.assertTrue(SKEY_AUTOCOMPLETE+'a' in autocomplete_list)
        self.assertTrue(SKEY_AUTOCOMPLETE+'test' in autocomplete_list)
        self.assertTrue(SKEY_AUTOCOMPLETE+'post' in autocomplete_list)
        self.assertTrue(SKEY_AUTOCOMPLETE+'this is a test post' in autocomplete_list)
        self.assertEquals(r.smembers('models-search.testmodelpost:1'),
                          set(['title:This is a test post.',
                               'slug:this-is-a-test-post',
                               'get_absolute_url:/blog/post/this-is-a-test-post/']))
        flush_redis()
        self.assertEquals(r.zrange(ZKEY_AUTOCOMPLETE, 0, -1), [])
        self.assertEquals(r.keys(SKEY_AUTOCOMPLETE+'*'), [])
        self.assertEquals(r.smembers('models-*'), set([]))

    def test_autocomplete_suggestion(self):
        """ Test of autocomplete function. """
        G(TestModelPost, title="This is a test post.", slug="", author=self.staff)
        G(TestModelPost, title="post.", slug="", author=self.staff)
        G(TestModelPost, title="This is a test python.", slug="", author=self.staff)
        G(TestModelPost, title="This is a poster.", slug="", author=self.staff)
        G(TestModelPost, title="This is a test poster.", slug="", author=self.staff)
        G(TestModelPost, title="This poster is a test python.", slug="", author=self.staff)
        G(TestModelPost, title="This is a test posterise.", slug="", author=self.staff)
        self.assertEquals(autocomplete_suggestion('post', 10), set(['poster', 'post', 'posterise']))

    def test_autocomplete_suggestion_no_of_results(self):
        """ Test to check returned result for autocomplete_suggestion has the correct no of results. """
        for title in range(0, 20):
            G(TestModelPost, title="post%s" % title, slug="", author=self.staff)
        self.assertEquals(len(autocomplete_suggestion('post', 10)), 10)

    def test_novalue_autocomplete_suggestion(self):
        """ Test to check no of results returned for autocomplete_suggestion. """
        for title in range(0, 20):
            G(TestModelPost, title="post%s" % title, slug="", author=self.staff)
        self.assertEquals(len(autocomplete_suggestion('', 10)), 0)

    def test_search_function(self):
        """ Test basic search function - top search should have the highest hit count. """
        G(TestModelPost, title="This is a python post.", slug="", author=self.staff)
        G(TestModelPost, title="This is a post called attempt post.", slug="", author=self.staff)
        G(TestModelPost, title="This is a test attempt post.", slug="", author=self.staff)
        G(TestModelPost, title="This is a test case.", slug="", author=self.staff)
        G(TestModelPost, title="This is a test.", slug="", author=self.staff)
        result = search_redis("post attempt")
        self.assertEquals(result, [{'pk': 2, 'model': 'search.testmodelpost', 'fields':
                                   {'get_absolute_url': '/blog/post/this-is-a-post-called-attempt-post/',
                                    'slug': 'this-is-a-post-called-attempt-post',
                                    'title': 'This is a post called attempt post.'}},
                                   {'pk': 3, 'model': 'search.testmodelpost', 'fields':
                                   {'get_absolute_url': '/blog/post/this-is-a-test-attempt-post/',
                                    'slug': 'this-is-a-test-attempt-post', 'title': 'This is a test attempt post.'}},
                                   {'pk': 1, 'model': 'search.testmodelpost',
                                    'fields': {'get_absolute_url': '/blog/post/this-is-a-python-post/',
                                    'slug': 'this-is-a-python-post', 'title': 'This is a python post.'}}])

