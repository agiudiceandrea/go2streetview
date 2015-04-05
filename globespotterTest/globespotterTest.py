# -*- coding: utf-8 -*-
"""
/***************************************************************************
 globespotterTest
                                 A QGIS plugin
 desc
                              -------------------
        begin                : 2015-01-30
        git sha              : $Format:%H$
        copyright            : (C) 2015 by ef
        email                : enricofer@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
from PyQt4.QtNetwork import *
# Initialize Qt resources from file resources.py
import resources_rc
# Import the code for the dialog
from globespotterTest_dialog import globespotterTestDialog
import os.path


class globespotterTest:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'globespotterTest_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = globespotterTestDialog()

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&globespotterTest')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'globespotterTest')
        self.toolbar.setObjectName(u'globespotterTest')

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('globespotterTest', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/globespotterTest/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'globespotterTest'),
            callback=self.run,
            parent=self.iface.mainWindow())
        self.setProxy()


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&globespotterTest'),
                action)
            self.iface.removeToolBarIcon(action)

    def setProxy(self):
        # procedure to set proxy if needed
        s = QSettings() #getting proxy from qgis options settings
        proxyEnabled = s.value("proxy/proxyEnabled", "")
        proxyType = s.value("proxy/proxyType", "" )
        proxyHost = s.value("proxy/proxyHost", "" )
        proxyPort = s.value("proxy/proxyPort", "" )
        proxyUser = s.value("proxy/proxyUser", "" )
        proxyPassword = s.value("proxy/proxyPassword", "" )
        print proxyEnabled+"; "+proxyType+"; "+proxyHost+"; " + proxyPort+"; " + proxyUser+"; " +"*********; "
        
        if proxyEnabled == "true": # test if there are proxy settings
           self.proxy = QNetworkProxy()
           if proxyType == "DefaultProxy":
               self.proxy.setType(QNetworkProxy.DefaultProxy)
           elif proxyType == "Socks5Proxy":
               self.proxy.setType(QNetworkProxy.Socks5Proxy)
           elif proxyType == "HttpProxy":
               self.proxy.setType(QNetworkProxy.HttpProxy)
           elif proxyType == "HttpCachingProxy":
               self.proxy.setType(QNetworkProxy.HttpCachingProxy)
           elif proxyType == "FtpCachingProxy":
               self.proxy.setType(QNetworkProxy.FtpCachingProxy)
           self.proxy.setHostName(proxyHost)
           self.proxy.setPort(int(proxyPort))
           self.proxy.setUser(proxyUser)
           self.proxy.setPassword(proxyPassword)
	   QNetworkProxy.setApplicationProxy(self.proxy)
	else:
		self.proxy= None

        #self.proxy = QNetworkProxy()
        #self.proxy.setType(QNetworkProxy.HttpProxy)
        #self.proxy.setHostName("127.0.0.1")
        #self.proxy.setPort(8888)
        #QNetworkProxy.setApplicationProxy(self.proxy)

    def handleAuthenthication(self,networkReply,authenticator):
        print networkReply.header(QNetworkRequest.ContentTypeHeader)
        print networkReply.url().toString()
        print 'auth request from:',authenticator.realm()
        print 'auth options:',authenticator.options()
        authenticator.setUser("enrico.ferreguti")
        authenticator.setPassword("hnsaml4b")

    def networkAccessibleChangedManager(self,accessible):
        print 'networkAccessibleChangedManager'

    def finishedManager(self,reply):
        print 'finishedManager'
        
    def proxyAuthenticationRequiredManager(self,networkReply,authenticator):
        print 'proxyAuthenticationRequiredManager'
        
    def sslErrorsManager(self,reply,errors):
        print 'sslErrorsManager'
        
    def run(self):
        """Run method that performs all the real work"""
        # show the dialog
        self.dlg.show()
        self.dlg.webView.settings().globalSettings().setAttribute(QWebSettings.PluginsEnabled, True);

        self.dlg.webView.settings().globalSettings().setAttribute(QWebSettings.JavascriptEnabled,True);
        self.dlg.webView.settings().globalSettings().setAttribute(QWebSettings.LocalStorageEnabled,True);
        self.dlg.webView.settings().globalSettings().setAttribute(QWebSettings.JavascriptCanOpenWindows,True);
        self.dlg.webView.settings().globalSettings().setAttribute(QWebSettings.JavascriptCanCloseWindows,True);
        self.dlg.webView.settings().globalSettings().setAttribute(QWebSettings.JavascriptCanAccessClipboard,True);
        self.dlg.webView.settings().globalSettings().setAttribute(QWebSettings.SpatialNavigationEnabled,True);
        self.dlg.webView.settings().globalSettings().setAttribute(QWebSettings.OfflineStorageDatabaseEnabled,True);

        cookieJar = QNetworkCookieJar()
        self.dlg.webView.page().networkAccessManager().setCookieJar(cookieJar)
        
        diskCache = QNetworkDiskCache()
        diskCache.setCacheDirectory(os.path.join(self.plugin_dir,'cache'))
        self.dlg.webView.page().networkAccessManager().setCache(diskCache)
	
	if self.proxy:
        	self.dlg.webView.page().networkAccessManager().setProxy(self.proxy)

        self.dlg.webView.page().networkAccessManager().authenticationRequired.connect(self.handleAuthenthication)
        self.dlg.webView.page().networkAccessManager().networkAccessibleChanged .connect(self.networkAccessibleChangedManager )
        self.dlg.webView.page().networkAccessManager().finished.connect(self.finishedManager)
        self.dlg.webView.page().networkAccessManager().proxyAuthenticationRequired.connect(self.proxyAuthenticationRequiredManager)
        self.dlg.webView.page().networkAccessManager().sslErrors.connect(self.sslErrorsManager)
        
        
        self.dlg.webView.load(QUrl("http://layers.aryagis.com/aryamap/gs_api.html?posx=602897&posy=7790983"))
        #self.dlg.webView.load(QUrl("http://www.google.com"))

        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass
