==============================================================================
Part 5: Testing Generic Setup
==============================================================================

Template
--------

test_setup.py::

  from Products.CMFCore.utils import getToolByName
  import unittest2 as unittest
  from collective.mypackage.testing import \
      COLLECTIVE_MYPACKAGE_INTEGRATION_TESTING


  class TestExample(unittest.TestCase):

      layer = COLLECTIVE_MYPACKAGE_INTEGRATION_TESTING

      def setUp(self):
          self.app = self.layer['app']
          self.portal = self.layer['portal']
          self.qi_tool = getToolByName(self.portal, 'portal_quickinstaller')

      def test_product_is_installed(self):
          """ Validate that our products GS profile has been run and the product
              installed
          """
          pid = 'puxam.policy'
          installed = [p['id'] for p in self.qi_tool.listInstalledProducts()]
          self.assertTrue(pid in installed,
                          'package appears not to have been installed')



Dependencies
------------

Test if dependencies have been installed::

    def test_product_is_installed(self):
        """ Validate that our products GS profile has been run and the product
            has been installed.
        """
        pid = 'collective.mailchimp'
        installed = [p['id'] for p in self.qi_tool.listInstalledProducts()]
        self.assertTrue(
            pid in installed,
            "The package '%s' appears not to have been installed." % pid')

setup.py::

    install_requires=[
      'setuptools',
      'collective.mailchimp',
    ],

profiles/default/metadata.xml::

    <?xml version="1.0"?>
    <metadata>
      <version>1</version>
      <dependencies>
        <dependency>profile-collective.mailchimp:default</dependency>
      </dependencies>
    </metadata>


Javascript Registration
-----------------------

Test if a Javascript file has been registered::

    def test_js_available(self):
        jsreg = getToolByName(self.portal, 'portal_javascripts')
        script_ids = jsreg.getResourceIds()
        self.assertTrue('BarackSlideshow.js' in script_ids)


CSS Registration
----------------

Test if a CSS file has been registered::

    def test_mailchimp_css_available(self):
        cssreg = getToolByName(self.portal, "portal_css")
        stylesheets_ids = cssreg.getResourceIds()
        self.assertTrue(
            '++resource++collective.mailchimp.stylesheets/mailchimp.css'
            in stylesheets_ids
        )

Test if a CSS has been enabled in the CSS registry::

     def test_mailchimp_css_enabled(self):
        cssreg = getToolByName(self.portal, "portal_css")
        self.assertTrue(
            cssreg.getResource(
                '++resource++collective.mailchimp.stylesheets/mailchimp.css'
            ).getEnabled()
        )


Layer registered
----------------

interfaces.py::

  from zope.interface import Interface

  class IMyCompanyTheme(Interface):
      """"""

browserlayer.xml::

  <layers>
    <layer
      name="mycompany.theme"
      interface="mycompany.theme.interfaces.IMyCompanyTheme"
      />
  </layers>

test_setup.py::

    def test_barackslideshow_layer_available(self):
        from plone.browserlayer import utils
        from collective.barackslideshow.tests.layer import IBarackSlideshowLayer
        self.failUnless(IBarackSlideshowLayer in utils.registered_layers())


Exclude From Search
-------------------

Exclude a content type from search::

    def makeTypeSearchable(portal, type_id, searchable):
        ptool = getToolByName(portal, 'portal_properties')
        blacklisted = list(ptool.site_properties.getProperty('types_not_searched'))
        if searchable and type_id in blacklisted:
            blacklisted.remove(type_id)
        elif not searchable and type_id not in blacklisted:
            blacklisted.append(type_id)
        ptool.site_properties.manage_changeProperties(
            types_not_searched=blacklisted)

    makeTypeSearchable(portal, 'Image', searchable=False)

Test::

    def test_exclude_images_from_search(self):
        self.assertTrue(
            'Image' in \
            self.ptool.site_properties.getProperty("types_not_searched"))


Resource Directories
--------------------

test_setup.py::

    def test_resources_directory(self):
        self.assertTrue(
            self.portal.restrictedTraverse(
                "++theme++dkg.contenttypes/medical-information.png"
            )
        )

configure.zcml::

  <plone:static
    type="theme"
    directory="resources"
    />


Image
-----

Test::

    def test_method_render_grafik(self):
        self.portal.mi.eb.invokeFactory('grafik', 'text1')
        image_file = os.path.join(os.path.dirname(__file__), u'logo.jpg')
        self.portal.mi.eb.text1.grafik = NamedBlobImage(
        data=open(image_file, 'r').read(),
        contentType='image/jpg',
        filename=u'logo.jpg'
        )
        self.assertTrue(self.portal.mi.eb.text1.render())

Test if code is run as test

    if self.request['URL'] == 'http://nohost':
        # test run


Catalog Index
-------------

Test if catalog index 'total_comments' has been installed::

    def test_catalog_index_total_comments_installed(self):
        catalog = getToolByName(self.portal, "portal_catalog")
        self.assertTrue(
            'total_comments' in
            catalog.indexes()
        )

profiles/default/catalog.xml::

    <?xml version="1.0"?>
    <object name="portal_catalog">

      <index name="total_comments" meta_type="FieldIndex">
        <indexed_attr value="total_comments"/>
      </index>

    </object>


Catalog Metadata
----------------

Test if catalog metadata has been installed::

    def test_catalog_metadata_installed(self):
        self.portal.invokeFactory('Document',
                                  'doc')
        self.portal.article.catchword = "Foo"
        self.portal.article.reindexObject()
        self.assertTrue('catchword' in self.catalog.schema())
        result = self.catalog.searchResults(
            path='/'.join(self.portal.article.getPhysicalPath()))
        self.assertTrue(len(result), 1)
        self.assertEquals(result[0].catchword, "Foo")

profiles/default/catalog.xml::

  <?xml version="1.0"?>
  <object name="portal_catalog" meta_type="Plone Catalog Tool">
    <index name="autor_in" meta_type="FieldIndex">
      <indexed_attr value="autor_in" />
    </index>
   <column value="autor_in" />
  </object>


Searchable Index
----------------

Test if index is searchable::

    def test_subjects_searchable(self):
        self.folder.invokeFactory("Document", "doc1")
        doc1 = self.folder.doc1
        doc1.setSubject([u"Python", u"Pyramid"])
        doc1.reindexObject()
        result = self.catalog.searchResults(dict(
            SearchableText = "Python"
            ))
        self.assertTrue(len(result), 1)
        self.assertTrue(result[0].title, "doc1")


Hide content type from navigation
---------------------------------

Test if content type is hidden from navigation::

    def test_hide_types_form_navigation(self):
        navtree_properties = self.portal.portal_properties.navtree_properties
        self.assertTrue(navtree_properties.hasProperty('metaTypesNotToList'))
        self.assertTrue('mycompany.membership.emailresetter' in
            navtree_properties.metaTypesNotToList)
        self.assertTrue('mycompany.membership.member' in
            navtree_properties.metaTypesNotToList)
        self.assertTrue('mycompany.membership.passwordresetter' in
            navtree_properties.metaTypesNotToList)
        self.assertTrue('mycompany.membership.registrator' in
            navtree_properties.metaTypesNotToList)

profiles/default/propertiestool.xml::

    <?xml version="1.0"?>
    <object name="portal_properties" meta_type="Plone Properties Tool">
     <object name="navtree_properties" meta_type="Plone Property Sheet">
      <property name="title">NavigationTree properties</property>
      <property name="metaTypesNotToList" type="lines">
       <element value="mycompany.membership.emailresetter"/>
       <element value="mycompany.membership.passwordresetter"/>
       <element value="mycompany.membership.registrator"/>
      </property>
     </object>
    </object>


Do not search content type
--------------------------

Test if content type is excluded from search::

    def test_types_not_searched(self):
        types_not_searched = self.portal.portal_properties\
            .site_properties.types_not_searched
        self.assertTrue('mycompany.membership.emailresetter'
                        in types_not_searched)
        self.assertTrue('mycompany.membership.passwordresetter'
                        in types_not_searched)
        self.assertTrue('mycompany.membership.registrator'
                        in types_not_searched)

profiles/default/propertiestool.xml::

    <?xml version="1.0"?>
    <object name="portal_properties">
      <object name="site_properties">
        <property name="types_not_searched" purge="false">
          <element value="mycompany.membership.emailresetter"/>
          <element value="mycompany.membership.passwordresetter"/>
          <element value="mycompany.membership.registrator"/>
        </property>
      </object>
    </object>


Portal Actions
--------------

Test if portal actions have been added properly::

    def test_actions(self):
        user_actions = self.portal.portal_actions.user
        self.assertTrue("preferences" in user_actions.objectIds())
        self.assertTrue('@@my-profile' in user_actions.preferences.url_expr)
        self.assertEquals(user_actions.preferences.visible, True)

profiles/default/actions.xml::

    <?xml version="1.0"?>
    <object name="portal_actions"
       xmlns:i18n="http://xml.zope.org/namespaces/i18n">
     <object name="user">
      <object name="preferences" meta_type="CMF Action" i18n:domain="mycompany.membership">
       <property name="title" i18n:translate="">Preferences</property>
       <property name="description" i18n:translate=""></property>
       <property
          name="url_expr">string:${globals_view/navigationRootUrl}/@@my-profile</property>
       <property name="icon_expr"></property>
       <property name="available_expr">python:member is not None</property>
       <property name="permissions">
        <element value="View"/>
       </property>
       <property name="visible">True</property>
      </object>
     </object>
    </object>

Enable user folder
------------------

Test if user folder has been enabled::

        self.mtool = self.portal.portal_membership
        self.assertEquals(self.mtool.memberareaCreationFlag, 1)
        self.assertEquals(self.mtool.memberarea_type, 'mycompany.membership.member')
        self.assertEquals(self.mtool.getMembersFolder().absolute_url(),
                          'http://nohost/plone/autoren')

setuphandlers.py::

        membership_tool.membersfolder_id = MEMBERS_FOLDER_ID
        logger.info("Members folder set up: %s\n" % MEMBERS_FOLDER_ID)

        # Configure member areas
        membership_tool.setMemberAreaType(MEMBER_AREA_TYPE)
        logger.info("Member area type: %s\n" % MEMBER_AREA_TYPE)

        membership_tool.setMemberareaCreationFlag()
        logger.info("Member area creation active\n")

Workflow
--------

Test if workflow has been installed::

    def test_workflows_installed(self):
        """Make sure both comment workflows have been installed properly.
        """
        self.assertTrue('one_state_workflow' in
                        self.portal.portal_workflow.objectIds())
        self.assertTrue('comment_review_workflow' in
                        self.portal.portal_workflow.objectIds())

Test default workflow for a certain content type::

    def test_default_workflow(self):
        """Make sure one_state_workflow is the default workflow.
        """
        self.assertEqual(('one_state_workflow',),
                          self.portal.portal_workflow.getChainForPortalType(
                              'Discussion Item'))


Users and Groups
----------------

Test that a user has been added::

    def test_users_installed(self):
        pas = getToolByName(self.portal, 'acl_users')
        user_ids = [x['login'] for x in pas.searchUsers()]
        self.assertTrue('john' in user_ids)

setuphandlers.py::

    def setupGroups(portal):
        acl_users = getToolByName(portal, 'acl_users')
        if not acl_users.searchGroups(name='Editorial'):
            gtool = getToolByName(portal, 'portal_groups')
            gtool.addGroup('Editorial', roles=[])

Test that a group has been added::

    def test_editorial_group_installed(self):
        self.assertTrue(
            'Editorial' in self.utool.source_groups.getGroupNames())

Roles
-----

test_setup.py::

    def test_mycompany_site_administrator_role_installed(self):
        self.assertTrue(
            "MyCompany Site Administrator" in self.portal.valid_roles())


profiles/default/roles.xml::

    <?xml version="1.0"?>
    <rolemap>
      <roles>
        <role name="Freitag Site Administrator" />
      </roles>
    </rolemap>


Mock Mailhost
-------------

Mock Mailhost::

    from zope.component import getSiteManager

    from Products.MailHost.interfaces import IMailHost
    from Products.CMFPlone.tests.utils import MockMailHost


    class EasyNewsletterTests(unittest.TestCase):

        layer = EASYNEWSLETTER_INTEGRATION_TESTING

        def setUp(self):
            # Set up a mock mailhost
            self.portal._original_MailHost = self.portal.MailHost
            self.portal.MailHost = mailhost = MockMailHost('MailHost')
            sm = getSiteManager(context=self.portal)
            sm.unregisterUtility(provided=IMailHost)
            sm.registerUtility(mailhost, provided=IMailHost)
            # We need to fake a valid mail setup
            self.portal.email_from_address = "portal@plone.test"
            self.mailhost = self.portal.MailHost

        def test_send_email(self):
            self.assertEqual(len(self.mailhost.messages), 1)
            self.assertTrue(self.mailhost.messages[0])
            msg = str(self.mailhost.messages[0])
            self.assertTrue('To: john@plone.test' in msg)
            self.assertTrue('From: portal@plone.test' in msg)


Versioning
----------

(Dexterity/plone.app.versioningbehavior only)

profiles/default/types/MyCustomType.xml::

    <property name="behaviors">
      <element value="plone.app.versioningbehavior.behaviors.IVersionable" />
    </property>

Test::

    def test_versioning_behavior_enabled(self):
        self.portal.mi.sec.tc.invokeFactory('AudienceText', 'text1')
        from plone.app.versioningbehavior.behaviors import IVersioningSupport
        self.assertTrue(
            IVersioningSupport.providedBy(self.portal.mi.sec.tc.text1)
        )

profiles/default/repositorytool.xml::

  <?xml version="1.0"?>
  <repositorytool>
    <policymap>
      <type name="MyCustomType">
        <policy name="at_edit_autoversion"/>
        <policy name="version_on_revert"/>
      </type>
    </policymap>
  </repositorytool>

Test::

    def test_versioning_enabled(self):
        self.portal.mi.sec.tc.invokeFactory('AudienceText', 'text1')
        repository_tool = getToolByName(self.portal, "portal_repository")
        self.assertTrue(
            repository_tool.isVersionable(self.portal.mi.sec.tc.text1)
        )
        self.assertTrue(
            repository_tool.supportsPolicy(
                self.portal.mi.sec.tc.text1,
                'at_edit_autoversion'
            )
        )
