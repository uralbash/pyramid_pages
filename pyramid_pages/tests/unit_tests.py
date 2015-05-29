from pyramid.httpexceptions import HTTPNotFound

from pyramid_pages.routes import PageResource
from pyramid_pages.views import page_view

from . import MPTTPages, UnitTestBase


class TestResource(UnitTestBase):
    pass


class TestCommon(UnitTestBase):
    pass


class TestPageView(UnitTestBase):

    """ VISIBLE
    """

    def test_visible_node(self):
        node = MPTTPages(visible=True)
        context = PageResource(node)
        view = page_view(context, self.request)
        self.assertEqual(view['page'], node)

    def test_not_visible_node(self):
        node = MPTTPages()
        context = PageResource(node)
        self.assertRaises(HTTPNotFound, page_view, context, self.request)

    """ REDIRECT

    redirect_url: URI string e.g.: http://example.com/
    redirect_page: node of tree
    redirect_type: [200, 301, 302]
    """
    def test_redirect_200(self):
        """
        redirect_type = 200
        redirect_url  = None
        redirect_page = None
        """
        node = MPTTPages(visible=True, redirect_type=200)
        context = PageResource(node)
        view = page_view(context, self.request)
        self.assertEqual(view['page'], node)

    """ 200 OK
        redirect to page
    """
    def test_redirect_200_to_self(self):
        """
        redirect_type = 200
        redirect_url  = None
        redirect_page = self
        """
        node = MPTTPages(
            id=1, visible=True,
            redirect_type=200, redirect_page=1
        )
        node.redirect = node
        context = PageResource(node)
        view = page_view(context, self.request)
        self.assertEqual(view['page'], node)

    def test_redirect_page_with_out_type(self):
        """
        redirect_type = None
        redirect_url  = None
        redirect_page = 2
        """
        node2 = MPTTPages(id=2)
        node = MPTTPages(
            id=1, visible=True,
            redirect_page=2, redirect=node2
        )
        context = PageResource(node)
        self.assertRaises(HTTPNotFound, page_view, context, self.request)

    def test_redirect_200_to_not_visible_page(self):
        """
        redirect_type = 200
        redirect_url  = None
        redirect_page = 2
        """
        node2 = MPTTPages(id=2)
        node = MPTTPages(
            id=1, visible=True,
            redirect_type=200, redirect_page=2, redirect=node2
        )
        context = PageResource(node)
        self.assertRaises(HTTPNotFound, page_view, context, self.request)

    def test_redirect_200_to_visible_page(self):
        """
        redirect_type = 200
        redirect_url  = None
        redirect_page = 2
        """
        node2 = MPTTPages(id=2, visible=True)
        node = MPTTPages(
            id=1, visible=True,
            redirect_type=200, redirect_page=2, redirect=node2
        )
        context = PageResource(node)
        view = page_view(context, self.request)
        self.assertEqual(view['page'], node2)

    """ 300
        redirect to page
    """
    def test_redirect_300_to_self(self):
        """
        redirect_type = 301
        redirect_url  = None
        redirect_page = self
        """
        node = MPTTPages(
            id=1, visible=True,
            redirect_type=301, redirect_page=1
        )
        node.redirect = node
        context = PageResource(node)
        self.assertRaises(HTTPNotFound, page_view, context, self.request)
        node.redirect_type = 302
        self.assertRaises(HTTPNotFound, page_view, context, self.request)

    def test_redirect_300_to_not_visible_page(self):
        """
        redirect_type = 300
        redirect_url  = None
        redirect_page = 2
        """
        node2 = MPTTPages(id=2)
        node = MPTTPages(
            id=1, visible=True,
            redirect_type=301, redirect_page=2, redirect=node2
        )
        context = PageResource(node)
        self.assertRaises(HTTPNotFound, page_view, context, self.request)
        node.redirect_type = 302
        self.assertRaises(HTTPNotFound, page_view, context, self.request)

    def test_redirect_300_to_visible_page(self):
        """
        redirect_type = 300
        redirect_url  = None
        redirect_page = 2
        """
        node = MPTTPages(
            id=1, visible=True, name='node', slug='node',
            redirect_type=301, redirect_page=2
        )
        node2 = MPTTPages(id=2, visible=True, name='node2', slug='node2')
        node3 = MPTTPages(id=3, visible=True, name='node3', slug='node3',
                          parent_id=2)
        node4 = MPTTPages(
            id=4, visible=True, name='node4', slug='node4',
            redirect_type=301, redirect_page=3
        )

        self.dbsession.add(node)
        self.dbsession.add(node2)
        self.dbsession.add(node3)
        self.dbsession.add(node4)
        self.dbsession.commit()

        # 301
        context = PageResource(node)
        view = page_view(context, self.request)
        self.assertEqual(view.status_code, 301)
        self.assertEqual(view.location, 'http://example.com/node2/')

        context = PageResource(node4)
        view = page_view(context, self.request)
        self.assertEqual(view.status_code, 301)
        self.assertEqual(view.location, 'http://example.com/node2/node3/')

        # 302
        node.redirect_type = 302
        context = PageResource(node)
        view = page_view(context, self.request)
        self.assertEqual(view.status_code, 302)
        self.assertEqual(view.location, 'http://example.com/node2/')

        node4.redirect_type = 302
        context = PageResource(node4)
        view = page_view(context, self.request)
        self.assertEqual(view.status_code, 302)
        self.assertEqual(view.location, 'http://example.com/node2/node3/')

    """ 200 OK
        redirect to URL
    """
    def test_redirect_200_to_url(self):
        """
        redirect_type = 200
        redirect_url  = http://example.org
        redirect_page = None
        """
        URL = 'http://example.org'
        node = MPTTPages(
            visible=True, redirect_type=200, redirect_url=URL
        )
        context = PageResource(node)
        self.assertRaises(HTTPNotFound, page_view, context, self.request)

    def test_redirect_url_with_out_type(self):
        """
        redirect_type = None
        redirect_url  = http://example.org
        redirect_page = None
        """
        URL = 'http://example.org'
        node = MPTTPages(
            visible=True, redirect_url=URL,
        )

        context = PageResource(node)
        view = page_view(context, self.request)
        self.assertEqual(view.status_code, 302)
        self.assertEqual(view.location, 'http://example.org')

    """ 300
        redirect to URL
    """
    def test_redirect_300_to_url(self):
        """
        redirect_type = 200
        redirect_url  = http://example.org
        redirect_page = None
        """
        URL = 'http://example.org'
        node = MPTTPages(
            visible=True, redirect_type=301, redirect_url=URL
        )

        # 301
        context = PageResource(node)
        view = page_view(context, self.request)
        self.assertEqual(view.status_code, 301)
        self.assertEqual(view.location, 'http://example.org')

        # 302
        node.redirect_type = 302
        context = PageResource(node)
        view = page_view(context, self.request)
        self.assertEqual(view.status_code, 302)
        self.assertEqual(view.location, 'http://example.org')

    """ Bad case.
    """
    def test_redirect_simultaneously_url_and_page(self):
        """
        redirect_type = None
        redirect_url  = http://example.org
        redirect_page = 2
        """
        URL = 'http://example.org'
        node2 = MPTTPages(id=2, visible=True)
        node = MPTTPages(
            visible=True, redirect_url=URL,
            redirect_page=2, redirect=node2
        )

        context = PageResource(node)
        self.assertRaises(HTTPNotFound, page_view, context, self.request)
