#!/usr/bin/env python3
"""
Hospital Management System - Main Launcher
Runs the complete application with all modules
"""

import sys
import os

# Ensure we're in the correct directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Import and run the main application
if __name__ == "__main__":
    from username import Ui_MainWindow, LoadingScreen
    from PyQt5 import QtWidgets
    import welcome
    
    # Show loading screen
    loading = LoadingScreen()
    
    # Create and show the main login window
    app = welcome.app if 'app' in dir(welcome) else QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    
    sys.exit(app.exec_())
