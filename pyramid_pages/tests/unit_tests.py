from pyramid.httpexceptions import HTTPNotFound

from pyramid_pages.resources import BasePageResource
from pyramid_pages.views import PageView

from . import NewsPage, UnitTestBase, WebPage
from pyramid_pages_example import Gallery


class TestResource(UnitTestBase):
    pass


class TestCommon(UnitTestBase):
    pass


class TestPageView(UnitTestBase):

    """ VISIBLE
    """

    def test_visible_node(self):
        """ Node is visible.
        """

        def do_it(model):
            node = model(visible=True)
            context = BasePageResource(node)
            view = PageView(context, self.request).page_with_redirect()
            self.assertEqual(view['page'], node)

        do_it(NewsPage)
        do_it(WebPage)

    def test_not_visible_node(self):
        """ Node is not visible.
        """

        def do_it(model):
            # visible is None
            node = model()
            context = BasePageResource(node)
            self.assertRaises(HTTPNotFound, PageView, context, self.request)

            # visible is False
            node = model(visible=False)
            context = BasePageResource(node)
            self.assertRaises(HTTPNotFound, PageView, context, self.request)

        do_it(NewsPage)
        do_it(WebPage)

    """ REDIRECT

    redirect_url: URI string e.g.: http://example.com/
    redirect_page: node of tree
    redirect_type: [200, 301, 302]
    """
    def test_redirect_200(self):
        """ Redirect 200 w/o page.

        redirect_type = 200
        redirect_url  = None
        redirect_page = None
        """
        node = WebPage(visible=True, redirect_type=200)
        context = BasePageResource(node)
        view = PageView(context, self.request).page_with_redirect()
        self.assertEqual(view['page'], node)

    """ 200 OK
        redirect to page
    """
    def test_redirect_200_to_self(self):
        """ Redirect 200 to itself.

        redirect_type = 200
        redirect_url  = None
        redirect_page = self
        """
        node = WebPage(
            id=1, visible=True,
            redirect_type=200, redirect_page=1
        )
        node.redirect = node
        context = BasePageResource(node)
        context.template = 'json'
        response = PageView(context, self.request).page_with_redirect()
        self.assertEqual(response.json['page'], 1)

    def test_redirect_page_with_out_type(self):
        """ Redirect to page w/o redirect type.

        redirect_type = None
        redirect_url  = None
        redirect_page = 2
        """
        node2 = WebPage(id=2)
        node = WebPage(
            id=1, visible=True,
            redirect_page=2, redirect=node2
        )
        context = BasePageResource(node)
        view = PageView(context, self.request)
        self.assertRaises(HTTPNotFound, view.page_with_redirect)

    def test_redirect_200_to_not_visible_page(self):
        """ Redirect 200 to not visible page.

        redirect_type = 200
        redirect_url  = None
        redirect_page = 2
        """
        node2 = WebPage(id=2)
        node = WebPage(
            id=1, visible=True,
            redirect_type=200, redirect_page=2, redirect=node2
        )
        context = BasePageResource(node)
        view = PageView(context, self.request)
        self.assertRaises(HTTPNotFound, view.page_with_redirect)

    def test_redirect_200_to_visible_page(self):
        """ Redirect 200 to visible page.

        redirect_type = 200
        redirect_url  = None
        redirect_page = 2
        """
        node2 = WebPage(id=2, visible=True)
        node = WebPage(
            id=1, visible=True,
            redirect_type=200, redirect_page=2, redirect=node2
        )
        context = BasePageResource(node)
        context.template = 'json'
        response = PageView(context, self.request).page_with_redirect()
        self.assertEqual(response.json['page'], 2)

    """ 300
        redirect to page
    """
    def test_redirect_300_to_self(self):
        """ Redirect 300 to itself.

        redirect_type = 300
        redirect_url  = None
        redirect_page = self
        """
        def do_it(redirect_code):
            node = WebPage(
                id=1, visible=True,
                redirect_type=redirect_code, redirect_page=1
            )
            node.redirect = node
            context = BasePageResource(node)
            view = PageView(context, self.request)
            self.assertRaises(HTTPNotFound, view.page_with_redirect)

        do_it(301)
        do_it(302)

    def test_redirect_300_to_not_visible_page(self):
        """ Redirect 300 to not visible page.

        redirect_type = 300
        redirect_url  = None
        redirect_page = 2
        """
        def do_it(redirect_code):
            node2 = WebPage(id=2)
            node = WebPage(
                id=1, visible=True,
                redirect_type=redirect_code, redirect_page=2, redirect=node2
            )
            context = BasePageResource(node)
            view = PageView(context, self.request)
            self.assertRaises(HTTPNotFound, view.page_with_redirect)

        do_it(301)
        do_it(302)

    def test_redirect_300_to_visible_page(self):
        """ Redirect 300 to visible page.

        redirect_type = 300
        redirect_url  = None
        redirect_page = 2
        """

        def do_it(redirect_code):
            self.drop_db()
            self.create_db()

            node2 = WebPage(id=2, visible=True, name='node2', slug='node2')
            node1 = WebPage(
                id=1, visible=True, name='node', slug='node',
                redirect_type=redirect_code, redirect=node2
            )
            node3 = WebPage(id=3, visible=True, name='node3', slug='node3',
                            parent_id=2)
            node4 = WebPage(
                id=4, visible=True, name='node4', slug='node4',
                redirect_type=redirect_code, redirect=node3
            )
            node5_inheritance = Gallery(
                id=5, visible=True, name='node5', slug='node5')
            node6 = WebPage(
                id=6, visible=True, name='node6', slug='node6',
                redirect_type=redirect_code, redirect_page=node5_inheritance.id
            )

            self.dbsession.add(node1)
            self.dbsession.add(node2)
            self.dbsession.flush()
            self.dbsession.add(node3)
            self.dbsession.add(node4)
            self.dbsession.add(node5_inheritance)
            self.dbsession.add(node6)
            self.dbsession.commit()

            # 301
            context = BasePageResource(node1)
            context.dbsession = self.dbsession
            view = PageView(context, self.request).page_with_redirect()
            self.assertEqual(view.status_code, redirect_code)
            self.assertEqual(view.location, 'http://example.com/node2/')

            context = BasePageResource(node4)
            view = PageView(context, self.request).page_with_redirect()
            self.assertEqual(view.status_code, redirect_code)
            self.assertEqual(view.location,
                             'http://example.com/node2/node3/')

            context = BasePageResource(node6)
            view = PageView(context, self.request).page_with_redirect()
            self.assertEqual(view.status_code, redirect_code)
            self.assertEqual(view.location,
                             'http://example.com/gallery/node5/')
            self.dbsession.close()

        do_it(301)
        do_it(302)

    """ 200 OK
        redirect to URL
    """
    def test_redirect_200_to_url(self):
        """ Redirect 200 to external URL.

        redirect_type = 200
        redirect_url  = http://example.org
        redirect_page = None
        """
        URL = 'http://example.org'
        node = WebPage(
            visible=True, redirect_type=200, redirect_url=URL
        )
        context = BasePageResource(node)
        view = PageView(context, self.request)
        self.assertRaises(HTTPNotFound, view.page_with_redirect)

    def test_redirect_url_with_out_type(self):
        """ Redirect to external URL w/o type.

        redirect_type = None
        redirect_url  = http://example.org
        redirect_page = None
        """
        URL = 'http://example.org'
        node = WebPage(
            visible=True, redirect_url=URL,
        )

        context = BasePageResource(node)
        view = PageView(context, self.request).page_with_redirect()
        self.assertEqual(view.status_code, 302)
        self.assertEqual(view.location, 'http://example.org')

    """ 300
        redirect to URL
    """
    def test_redirect_300_to_url(self):
        """ Redirect 300 to external URL.

        redirect_type = 300
        redirect_url  = http://example.org
        redirect_page = None
        """
        def do_it(redirect_code):
            URL = 'http://example.org'
            node = WebPage(
                visible=True, redirect_type=301, redirect_url=URL
            )

            # 301
            context = BasePageResource(node)
            view = PageView(context, self.request).page_with_redirect()
            self.assertEqual(view.status_code, 301)
            self.assertEqual(view.location, 'http://example.org')

        do_it(301)
        do_it(302)

    """ Bad case.
    """
    def test_redirect_simultaneously_url_and_page(self):
        """ Redirect simultaneously to URL and Page.

        redirect_type = None
        redirect_url  = http://example.org
        redirect_page = 2
        """
        URL = 'http://example.org'
        node2 = WebPage(id=2, visible=True)
        node = WebPage(
            visible=True, redirect_url=URL,
            redirect_page=2, redirect=node2
        )

        context = BasePageResource(node)
        view = PageView(context, self.request)
        self.assertRaises(HTTPNotFound, view.page_with_redirect)
