# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI\power_moniter.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_mainWindow(object):
    def setupUi(self, mainWindow):
        mainWindow.setObjectName("mainWindow")
        mainWindow.resize(1400, 1004)
        self.centralwidget = QtWidgets.QWidget(mainWindow)
        font = QtGui.QFont()
        font.setPointSize(6)
        self.centralwidget.setFont(font)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_6.setContentsMargins(300, 0, 300, 500)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_131 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(30)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.label_131.setFont(font)
        self.label_131.setStyleSheet("QLabel{color:rgb(255, 255, 255);\n"
" border: 2px solid white;\n"
"}")
        self.label_131.setScaledContents(True)
        self.label_131.setAlignment(QtCore.Qt.AlignCenter)
        self.label_131.setObjectName("label_131")
        self.verticalLayout.addWidget(self.label_131)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_138 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_138.setFont(font)
        self.label_138.setStyleSheet("QLabel{color:rgb(255, 255, 255);\n"
"         border: 2px solid white;\n"
"          transform: rotate(45deg);\n"
"\n"
"}")
        self.label_138.setAlignment(QtCore.Qt.AlignCenter)
        self.label_138.setObjectName("label_138")
        self.horizontalLayout_3.addWidget(self.label_138)
        self.label_139 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_139.setFont(font)
        self.label_139.setStyleSheet("QLabel{color:rgb(255, 255, 255);}")
        self.label_139.setAlignment(QtCore.Qt.AlignCenter)
        self.label_139.setObjectName("label_139")
        self.horizontalLayout_3.addWidget(self.label_139)
        self.lcdNumber1 = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcdNumber1.setStyleSheet("")
        self.lcdNumber1.setObjectName("lcdNumber1")
        self.horizontalLayout_3.addWidget(self.lcdNumber1)
        self.label_140 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_140.setFont(font)
        self.label_140.setStyleSheet("QLabel{color:rgb(255, 255, 255);}")
        self.label_140.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_140.setObjectName("label_140")
        self.horizontalLayout_3.addWidget(self.label_140)
        self.label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setStyleSheet("QLabel{color:rgb(255, 255, 255);}")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.horizontalLayout_3.addWidget(self.label)
        self.lcdNumber11 = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcdNumber11.setStyleSheet("")
        self.lcdNumber11.setObjectName("lcdNumber11")
        self.horizontalLayout_3.addWidget(self.lcdNumber11)
        self.label_144 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_144.setFont(font)
        self.label_144.setStyleSheet("QLabel{color:rgb(255, 255, 255);}")
        self.label_144.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_144.setObjectName("label_144")
        self.horizontalLayout_3.addWidget(self.label_144)
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet("QLabel{color:rgb(255, 255, 255);}")
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_3.addWidget(self.label_5)
        self.lcdNumber111 = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcdNumber111.setObjectName("lcdNumber111")
        self.horizontalLayout_3.addWidget(self.lcdNumber111)
        self.label_148 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_148.setFont(font)
        self.label_148.setStyleSheet("QLabel{color:rgb(255, 255, 255);}")
        self.label_148.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_148.setObjectName("label_148")
        self.horizontalLayout_3.addWidget(self.label_148)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_141 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_141.setFont(font)
        self.label_141.setStyleSheet("QLabel{color:rgb(255, 255, 255);\n"
"         border: 2px solid white;\n"
"          transform: rotate(45deg);\n"
"\n"
"}")
        self.label_141.setAlignment(QtCore.Qt.AlignCenter)
        self.label_141.setObjectName("label_141")
        self.horizontalLayout_2.addWidget(self.label_141)
        self.label_142 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_142.setFont(font)
        self.label_142.setStyleSheet("QLabel{color:rgb(255, 255, 255);}")
        self.label_142.setAlignment(QtCore.Qt.AlignCenter)
        self.label_142.setObjectName("label_142")
        self.horizontalLayout_2.addWidget(self.label_142)
        self.lcdNumber2 = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcdNumber2.setStyleSheet("")
        self.lcdNumber2.setObjectName("lcdNumber2")
        self.horizontalLayout_2.addWidget(self.lcdNumber2)
        self.label_143 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_143.setFont(font)
        self.label_143.setStyleSheet("QLabel{color:rgb(255, 255, 255);}")
        self.label_143.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_143.setObjectName("label_143")
        self.horizontalLayout_2.addWidget(self.label_143)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("QLabel{color:rgb(255, 255, 255);}")
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.lcdNumber22 = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcdNumber22.setStyleSheet("")
        self.lcdNumber22.setObjectName("lcdNumber22")
        self.horizontalLayout_2.addWidget(self.lcdNumber22)
        self.label_145 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_145.setFont(font)
        self.label_145.setStyleSheet("QLabel{color:rgb(255, 255, 255);}")
        self.label_145.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_145.setObjectName("label_145")
        self.horizontalLayout_2.addWidget(self.label_145)
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_6.setFont(font)
        self.label_6.setStyleSheet("QLabel{color:rgb(255, 255, 255);}")
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_2.addWidget(self.label_6)
        self.lcdNumber222 = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcdNumber222.setObjectName("lcdNumber222")
        self.horizontalLayout_2.addWidget(self.lcdNumber222)
        self.label_149 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_149.setFont(font)
        self.label_149.setStyleSheet("QLabel{color:rgb(255, 255, 255);}")
        self.label_149.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_149.setObjectName("label_149")
        self.horizontalLayout_2.addWidget(self.label_149)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_146 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_146.setFont(font)
        self.label_146.setStyleSheet("QLabel{color:rgb(255, 255, 255);\n"
"         border: 2px solid white;\n"
"          transform: rotate(45deg);\n"
"\n"
"}")
        self.label_146.setAlignment(QtCore.Qt.AlignCenter)
        self.label_146.setObjectName("label_146")
        self.horizontalLayout.addWidget(self.label_146)
        self.checkBox1 = QtWidgets.QCheckBox(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.checkBox1.setFont(font)
        self.checkBox1.setStyleSheet("/* 设置 QCheckBox 的文本颜色为白色 */\n"
"QCheckBox {\n"
"    color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"/* 设置 QCheckBox 被选中时的勾颜色为红色 */\n"
"QCheckBox::indicator:checked {\n"
"    background-color: green;\n"
"   \n"
"}\n"
"\n"
"")
        self.checkBox1.setObjectName("checkBox1")
        self.horizontalLayout.addWidget(self.checkBox1)
        self.checkBox11 = QtWidgets.QCheckBox(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.checkBox11.setFont(font)
        self.checkBox11.setStyleSheet("/* 设置 QCheckBox 的文本颜色为白色 */\n"
"QCheckBox {\n"
"    color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"/* 设置 QCheckBox 被选中时的勾颜色为红色 */\n"
"QCheckBox::indicator:checked {\n"
"    background-color: red;\n"
"    \n"
"   \n"
"}\n"
"")
        self.checkBox11.setObjectName("checkBox11")
        self.horizontalLayout.addWidget(self.checkBox11)
        self.checkBox2 = QtWidgets.QCheckBox(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.checkBox2.setFont(font)
        self.checkBox2.setStyleSheet("QCheckBox{color:rgb(255, 255, 255);}\n"
"QCheckBox::indicator:checked {\n"
"    color: black;\n"
"}\n"
"")
        self.checkBox2.setObjectName("checkBox2")
        self.horizontalLayout.addWidget(self.checkBox2)
        self.checkBox2_2 = QtWidgets.QCheckBox(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.checkBox2_2.setFont(font)
        self.checkBox2_2.setStyleSheet("QCheckBox{color:rgb(255, 255, 255);}\n"
"QCheckBox::indicator:checked {\n"
"    color: black;\n"
"}\n"
"")
        self.checkBox2_2.setObjectName("checkBox2_2")
        self.horizontalLayout.addWidget(self.checkBox2_2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("QLabel{color:rgb(255, 255, 255);\n"
"         border: 2px solid white;\n"
"          transform: rotate(45deg);\n"
"\n"
"}")
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_4.addWidget(self.label_3)
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_7.setFont(font)
        self.label_7.setStyleSheet("QLabel{color:rgb(255, 255, 255);\n"
"         border: 2px solid white;\n"
"          transform: rotate(45deg);\n"
"\n"
"}")
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_4.addWidget(self.label_7)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setMinimumSize(QtCore.QSize(0, 0))
        self.label_4.setText("")
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_5.addWidget(self.label_4)
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setMinimumSize(QtCore.QSize(0, 0))
        self.label_8.setText("")
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_5.addWidget(self.label_8)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_6.addLayout(self.verticalLayout)
        mainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(mainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1400, 26))
        self.menubar.setObjectName("menubar")
        mainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(mainWindow)
        self.statusbar.setObjectName("statusbar")
        mainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(mainWindow)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    def retranslateUi(self, mainWindow):
        _translate = QtCore.QCoreApplication.translate
        mainWindow.setWindowTitle(_translate("mainWindow", "实验室电力监控系统"))
        self.label_131.setText(_translate("mainWindow", "动力楼119实验室监控管理系统"))
        self.label_138.setText(_translate("mainWindow", "能效监控"))
        self.label_139.setText(_translate("mainWindow", "用电量"))
        self.label_140.setText(_translate("mainWindow", "kW/h"))
        self.label.setText(_translate("mainWindow", "电压"))
        self.label_144.setText(_translate("mainWindow", "V"))
        self.label_5.setText(_translate("mainWindow", "电流"))
        self.label_148.setText(_translate("mainWindow", "A"))
        self.label_141.setText(_translate("mainWindow", "环境监控"))
        self.label_142.setText(_translate("mainWindow", "温度"))
        self.label_143.setText(_translate("mainWindow", "℃"))
        self.label_2.setText(_translate("mainWindow", "湿度"))
        self.label_145.setText(_translate("mainWindow", "%RH"))
        self.label_6.setText(_translate("mainWindow", "烟雾浓度"))
        self.label_149.setText(_translate("mainWindow", "mg/m3"))
        self.label_146.setText(_translate("mainWindow", "报警监测"))
        self.checkBox1.setText(_translate("mainWindow", "电量监测"))
        self.checkBox11.setText(_translate("mainWindow", "功率报警"))
        self.checkBox2.setText(_translate("mainWindow", "烟雾报警"))
        self.checkBox2_2.setText(_translate("mainWindow", "气体报警"))
        self.label_3.setText(_translate("mainWindow", "30日平均功率变化图"))
        self.label_7.setText(_translate("mainWindow", "每日功率变化图"))
