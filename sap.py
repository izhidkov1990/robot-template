import subprocess
import win32com


class SAP:

    """Стандартный набор по автоматизации SAP"""

    def __init__(self):
        pass

    def start_session(self):
        try:
            check_gui = False            
            subprocess.check_call(['C:\Program Files (x86)\SAP\FrontEnd\SAPgui\\sapshcut.exe', '-system=DCG210', '-client=100', '-user=USERNAME', '-pw=PASSWORD'])
            while not shell.AppActivate(WinTitle):
                time.sleep(5)
            while not check_gui:
                try:
                    sap_gui_auto = win32com.client.GetObject("SAPGUI")
                    application = sap_gui_auto.GetScriptingEngine
                    self.session = application.FindById("ses[0]")
                    check_gui = True
                except:
                    time.sleep(5)
            self.session.findById("wnd[0]").maximize()
            # self.logger.info('SAP успешно запущен')
            return self.session
        except Exception as err:
            pass

    def close_session(self):
        pass