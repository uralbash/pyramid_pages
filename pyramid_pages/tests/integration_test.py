from . import IntegrationTestBase, IntegrationTestBaseWithIndex


class BasePageView(object):

    def test_get_root_page(self):
        self.app.get('/', status=200)

    def test_get_page_from_tree(self):
        self.app.get('/pages/about-company/', status=200)
        self.app.get('/about-company/', status=200)

    def test_redirect_301_page(self):
        self.app.get('/pages/about-company/redirect-301/',
                     status=301)

    def test_redirect_302_page(self):
        self.app.get('/pages/about-company/redirect-301/kompania-itcase/',
                     status=302)

    def test_bad_page_source(self):
        self.app.get('/I-would-like-to-be-a-page-but-Im-just-a-404-error',
                     status=404)


class TestPageView(IntegrationTestBase, BasePageView):
    pass


class TestPageViewWithIndex(IntegrationTestBaseWithIndex, BasePageView):
    pass
