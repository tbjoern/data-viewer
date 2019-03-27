#!/usr/bin/env python

from data_viewer.controller import Controller
from data_viewer.views.tkview import TKView
from data_viewer.mocks import DataProviderMock
from data_viewer.mocks import PlotterMock

def main():
    data_provider = DataProviderMock()
    plotter = PlotterMock()

    controller = Controller(data_provider, plotter)
    view = TKView(controller)
    controller.view = view

    controller.start()

if __name__== '__main__':
    main()

